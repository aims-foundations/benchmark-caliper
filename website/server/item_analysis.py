"""Temporary, private website runs of the Caliper item-analysis pipeline.

The CLI and website share preparation, specification generation, classification,
and reports. Only this adapter knows about HTTP, BYOK credentials, and job life
cycles. Model calls use the website client; credentials never enter saved inputs.
"""

from __future__ import annotations

import asyncio
from concurrent.futures import CancelledError as FutureCancelledError
from dataclasses import dataclass, field
import hashlib
from itertools import islice
import json
import math
import os
from pathlib import Path
import secrets
import shutil
from tempfile import TemporaryDirectory
from threading import Event
import time
from typing import Annotated, Literal

from fastapi import APIRouter, Header, HTTPException, Query, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict
from starlette.background import BackgroundTask

from anthropic_api_package_release.item_analysis import classify, generate, prepare, report
from anthropic_api_package_release.item_analysis.data import file_sha256
from anthropic_api_package_release.item_analysis.storage import check_prepared, read_json, write_json
from . import anthropic_client, db

router = APIRouter(prefix="/api/item-analysis", tags=["Item analysis"])
FIXTURE_PATH = Path(__file__).with_name("item_analysis_demo.json")
DEFAULT_PREPARED_DIR = Path(__file__).resolve().parents[2] / "results/item_analysis/mmlu_demo"
CHECKPOINT_SIZE = 100
PAGE_SIZE = 20
MAX_ACTIVE = 3
MAX_RETAINED = 10
RETENTION_SECONDS = 3600
ACTIVE_STATUSES = {"preparing", "generating", "running"}
PREPARED_FILES = ("dataset.json", "profile.json", "evidence.json", "items.jsonl")
ARTIFACTS = {
    "spec": ("classifier_spec.json", "application/json"),
    "items": ("items.csv", "text/csv"),
    "summary": ("summary.json", "application/json"),
    "report": ("report.html", "text/html"),
    "review": ("review.csv", "text/csv"),
}


class NewRun(BaseModel):
    model_config = ConfigDict(extra="forbid")
    example_id: Literal["illustrative", "mmlu"]
    specification_mode: Literal["generate", "provided"]


class Classification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scope: Literal["pilot", "all"]


@dataclass
class AnalysisJob:
    run_id: str
    secret: str = field(repr=False)
    example: dict
    directory: Path = field(repr=False)
    status: str = "preparing"
    message: str = "Preparing the item snapshot and assessment evidence."
    spec: dict | None = None
    summary: dict | None = None
    total: int = 0
    scope: str | None = None
    results: dict = field(default_factory=dict, repr=False)
    usage: dict = field(default_factory=lambda: {"input_tokens": 0, "output_tokens": 0})
    task: asyncio.Task | None = field(default=None, repr=False)
    provider_call: object | None = field(default=None, repr=False)
    provider_tasks: set = field(default_factory=set, repr=False)
    data_ready: bool = False
    stopped: Event = field(default_factory=Event, repr=False)
    owner_hash: str | None = field(default=None, repr=False)
    checkpoint_seen: bool = False
    updated_at: float = field(default_factory=time.monotonic)
    downloads: int = 0


jobs: dict[str, AnalysisJob] = {}


def prepared_directory() -> Path:
    return Path(os.environ.get("ITEM_ANALYSIS_PREPARED_DIR", str(DEFAULT_PREPARED_DIR))).expanduser()


def examples() -> list[dict]:
    fixture = read_json(FIXTURE_PATH)
    entries = [{"id": "illustrative", **{key: fixture[key] for key in (
        "title", "description", "benchmark", "deployment", "source_label")},
        "item_count": len(fixture["items"]), "available": True, "supplied_spec_available": True}]
    directory = prepared_directory()
    # Source paths come only from server configuration, never HTTP parameters.
    try:
        dataset = read_json(directory / "dataset.json")
        evidence = read_json(directory / "evidence.json")
        available = all((directory / name).is_file() for name in PREPARED_FILES)
        if available:
            entries.append({
                "id": "mmlu", "title": "MMLU · Hindi-medium exam preparation",
                "description": "The configured measurement-db snapshot and original Caliper assessment. Review 100 items, then continue across the full snapshot.",
                "benchmark": dataset["benchmark"], "deployment": evidence["deployment"],
                "source_label": "Prepared measurement-db snapshot with its original assessment; counts apply to this snapshot.",
                "item_count": dataset["item_count"], "available": True,
                "supplied_spec_available": (directory / "classifier_spec.original.json").is_file(),
            })
    except (OSError, ValueError, KeyError, TypeError):
        pass  # The bundled example remains runnable on a fresh checkout.
    return entries


def sweep() -> None:
    now = time.monotonic()
    for run_id, job in list(jobs.items()):
        if (not job.task or job.task.done()) and not job.downloads and now - job.updated_at > RETENTION_SECONDS:
            jobs.pop(run_id, None)
            shutil.rmtree(job.directory, ignore_errors=True)


async def shutdown() -> None:
    # Stop requests first, then drain every worker before removing its files.
    for job in list(jobs.values()):
        stop(job)
    await asyncio.gather(*(job.task for job in jobs.values() if job.task), return_exceptions=True)
    for job in jobs.values():
        shutil.rmtree(job.directory, ignore_errors=True)
    jobs.clear()


def authorize(run_id: str, secret: str | None) -> AnalysisJob:
    sweep()
    job = jobs.get(run_id)
    if job is None or not secret or not secrets.compare_digest(job.secret, secret):
        raise HTTPException(404, "Analysis not found or expired. Start a new analysis.")
    return job


def key_required(value: str | None) -> str:
    if not value or not value.strip():
        raise HTTPException(401, "An Anthropic API key is required for model calls.")
    if len(value) > 512:
        raise HTTPException(400, "Invalid credential length.")
    return value.strip()


def reserve_worker(api_key: str | None, current: AnalysisJob | None = None) -> str | None:
    active = [job for job in jobs.values() if job is not current and job.status in ACTIVE_STATUSES]
    owner = hashlib.sha256(api_key.encode()).hexdigest() if api_key else None
    if len(active) >= MAX_ACTIVE or (owner and any(job.owner_hash == owner for job in active)):
        raise HTTPException(429, "An analysis is already running for this key, or the demo is busy. Try again shortly.")
    return owner


def public_job(job: AnalysisJob, page: int = 1) -> dict:
    complete = sum(record["status"] == "complete" for record in job.results.values())
    errors = sum(record["status"] == "error" for record in job.results.values())
    pages = max(1, math.ceil(job.total / PAGE_SIZE))
    page = min(page, pages)
    rows = []
    if job.data_ready:
        with (job.directory / "items.jsonl").open(encoding="utf-8") as stream:
            for line in islice(stream, (page - 1) * PAGE_SIZE, page * PAGE_SIZE):
                item = json.loads(line)
                result = job.results.get(item["item_id"], {})
                rows.append({
                    "item_id": item["item_id"], "content": item.get("content"),
                    "reference_answer": item.get("reference_answer"),
                    "status": result.get("status", "pending"), "labels": result.get("labels"),
                    "error": "No valid classification was saved. Retry this phase to reassess the item." if result.get("status") == "error" else None,
                })
    return {
        "run_id": job.run_id, "status": job.status, "message": job.message,
        "example": job.example, "spec": job.spec, "summary": job.summary,
        "processed": len(job.results), "total": job.total, "complete": complete, "errors": errors,
        "items": rows, "pagination": {"page": page, "page_size": PAGE_SIZE, "total_pages": pages},
        "usage": dict(job.usage), "scope": job.scope,
        "can_continue": job.checkpoint_seen and job.status in {"checkpoint", "cancelled", "failed"},
        "error": job.message if job.status == "failed" else None,
    }


def prepare_job(job: AnalysisJob, example_id: str) -> Path:
    """Prepare immutable inputs, returning the optional provided-spec location."""
    if example_id == "mmlu":
        source = prepared_directory()
        check_prepared(source)
        for name in PREPARED_FILES:
            shutil.copyfile(source / name, job.directory / name)
        supplied = source / "classifier_spec.original.json"
        if supplied.is_file():
            shutil.copyfile(supplied, job.directory / "provided_spec.json")
        check_prepared(job.directory)
    else:
        import pyarrow as pa
        import pyarrow.parquet as pq

        fixture = read_json(FIXTURE_PATH)
        with TemporaryDirectory(prefix="inputs-", dir=job.directory.parent) as temporary:
            inputs = Path(temporary)
            write_json(inputs / "scoring.json", fixture["assessment"])
            for filename, key in (("deployment_description.txt", "deployment"),
                                  ("elicitation_summary.md", "elicitation_summary"),
                                  ("dataset_analysis_report.md", "dataset_analysis_report")):
                (inputs / filename).write_text(fixture[key], encoding="utf-8")
            items_path = inputs / "items.parquet"
            pq.write_table(pa.Table.from_pylist(fixture["items"]), items_path)
            prepare.prepare(inputs, items_path, job.directory,
                            source_repo="caliper-authored-illustrative-example",
                            source_revision=file_sha256(FIXTURE_PATH), source_table=FIXTURE_PATH.name)
        write_json(job.directory / "provided_spec.json", fixture["classifier_spec"])
    # Preserve checksums/revisions without exporting private server filesystem paths.
    dataset = read_json(job.directory / "dataset.json")
    dataset["source"].pop("path", None)
    evidence = read_json(job.directory / "evidence.json")
    evidence.pop("assessment_dir", None)
    write_json(job.directory / "evidence.json", evidence)
    dataset["evidence_sha256"] = file_sha256(job.directory / "evidence.json")
    write_json(job.directory / "dataset.json", dataset)
    return job.directory / "provided_spec.json"


def model_bridge(job: AnalysisJob, api_key: str):
    """Adapt the shared synchronous model callback to a request-scoped async client.

    The worker blocks on the event loop's request. Cancellation cancels that
    request and signals the shared classifier to stop before another item.
    Only this closure holds the credential; provider exception text is discarded.
    """
    loop = asyncio.get_running_loop()

    async def request(arguments):
        task = asyncio.current_task()
        job.provider_tasks.add(task)
        try:
            try:
                result = await anthropic_client.call_text_async(
                    api_key=api_key, family=arguments["model"], system=arguments["system"],
                    user=arguments["user"], max_tokens=arguments["max_tokens"],
                )
            except asyncio.CancelledError:
                raise
            except Exception:
                raise RuntimeError("Anthropic request failed. Check key access, quota, and model availability.") from None
            job.usage["input_tokens"] += result.input_tokens
            job.usage["output_tokens"] += result.output_tokens
            return result.text.replace(api_key, "[redacted]")
        finally:
            job.provider_tasks.discard(task)

    def call(**arguments):
        if job.stopped.is_set():
            raise InterruptedError("Analysis stopped.")
        future = asyncio.run_coroutine_threadsafe(request(arguments), loop)
        job.provider_call = future
        # Cover cancellation between the first check and future registration.
        if job.stopped.is_set():
            future.cancel()
        try:
            return future.result()
        except FutureCancelledError:
            raise InterruptedError("Analysis stopped.") from None
        finally:
            job.provider_call = None

    return call


async def drained_thread(function, *args, **kwargs):
    """Never abandon a thread that may still be writing a run directory."""
    worker = asyncio.create_task(asyncio.to_thread(function, *args, **kwargs))
    try:
        return await asyncio.shield(worker)
    except asyncio.CancelledError:
        await asyncio.gather(worker, return_exceptions=True)
        raise


async def drain_provider(job: AnalysisJob) -> None:
    # A cancelled cross-thread Future can finish before the underlying async
    # client's finally block closes its sockets. Wait for that cleanup too.
    await asyncio.sleep(0)
    while job.provider_tasks:
        await asyncio.gather(*list(job.provider_tasks), return_exceptions=True)


async def refresh_report(job: AnalysisJob) -> None:
    job.summary = await drained_thread(report.generate_report, job.directory)


async def initialize(job: AnalysisJob, mode: str, api_key: str | None) -> None:
    try:
        supplied = await drained_thread(prepare_job, job, job.example["id"])
        job.total = read_json(job.directory / "dataset.json")["item_count"]
        job.data_ready = True
        if job.stopped.is_set():
            return
        if mode == "generate":
            job.status, job.message = "generating", "Sonnet is turning the assessment into item-level classification rules."
        job.spec = await drained_thread(
            generate.generate_spec, job.directory,
            supplied=supplied if mode == "provided" else None,
            call=model_bridge(job, api_key) if api_key else None,
            model_id=anthropic_client.MODELS["sonnet"],
        )
        metadata = read_json(job.directory / "specification.json")
        metadata.get("source", {}).pop("path", None)
        write_json(job.directory / "specification.json", metadata)
        await refresh_report(job)
        job.status, job.message = "ready", "Review the classifier rules, then classify the first items."
    except Exception:
        job.status, job.message = "failed", "Could not prepare a valid specification. Check the example, model access, and API key, then start a new analysis."
    finally:
        await drain_provider(job)
        api_key = None
        finish_phase(job)


def finish_phase(job: AnalysisJob) -> None:
    if job.stopped.is_set():
        job.status, job.message = "cancelled", "Analysis stopped. Completed results are retained."
    job.owner_hash = None
    job.updated_at = time.monotonic()


async def classify_job(job: AnalysisJob, api_key: str) -> None:
    loop = asyncio.get_running_loop()

    def save_result(record):
        # Keep raw model attempts private; the website only needs validated labels.
        visible = {key: record[key] for key in ("item_id", "status", "labels") if key in record}
        loop.call_soon_threadsafe(job.results.__setitem__, record["item_id"], visible)

    try:
        execution = await drained_thread(
            classify.run, job.directory, limit=CHECKPOINT_SIZE if job.scope == "pilot" else None,
            resume=(job.directory / "run.json").exists(), call=model_bridge(job, api_key),
            model_id=anthropic_client.MODELS["haiku"], on_result=save_result,
            should_stop=job.stopped.is_set,
        )
        await refresh_report(job)
        if execution["fatal_error"]:
            job.status, job.message = "failed", "The model request failed. Check your API key, quota, or model access, then retry to resume saved progress."
        elif execution["full_dataset_complete"]:
            job.status, job.message = "complete", "Every item in this snapshot has a saved classification. Review the labels and export the results."
        elif job.scope == "pilot" and not execution["pending"]:
            job.checkpoint_seen = True
            job.status = "checkpoint"
            job.message = "The first items are ready for review. Inspect their labels and evidence before continuing across the snapshot."
        else:
            job.status, job.message = "failed", "Some items still need valid classifications. Retry to resume; completed items are retained."
    except Exception:
        job.status, job.message = "failed", "The analysis could not finish. Completed results are retained; retry with the same frozen specification."
    finally:
        await drain_provider(job)
        api_key = ""
        finish_phase(job)


def stop(job: AnalysisJob) -> None:
    job.stopped.set()
    if job.provider_call is not None:
        job.provider_call.cancel()


@router.get("/catalog")
async def catalog(response: Response) -> dict:
    response.headers["Cache-Control"] = "no-store"
    return {"examples": examples(), "checkpoint_size": CHECKPOINT_SIZE}


@router.post("/runs", status_code=202)
async def create_run(body: NewRun, response: Response,
                     x_anthropic_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    api_key = key_required(x_anthropic_key) if body.specification_mode == "generate" else None
    example = next((entry for entry in examples() if entry["id"] == body.example_id), None)
    if example is None:
        raise HTTPException(404, "This example is not configured on the server.")
    if body.specification_mode == "provided" and not example["supplied_spec_available"]:
        raise HTTPException(409, "This example requires generating a specification.")
    sweep()
    if len(jobs) >= MAX_RETAINED:
        raise HTTPException(429, "The demo is at capacity. Try again later.")
    owner = reserve_worker(api_key)
    run_id = secrets.token_hex(16)
    directory = db.DEFAULT_DB_PATH.parent / "item-analysis" / run_id
    directory.mkdir(mode=0o700, parents=True)
    job = AnalysisJob(run_id, secrets.token_urlsafe(32), example, directory,
                      total=example["item_count"], owner_hash=owner)
    jobs[run_id] = job
    job.task = asyncio.create_task(initialize(job, body.specification_mode, api_key))
    return {**public_job(job), "run_secret": job.secret}


@router.get("/runs/{run_id}")
async def get_run(run_id: str, response: Response,
                  x_review_token: Annotated[str | None, Header()] = None,
                  page: Annotated[int, Query(ge=1)] = 1) -> dict:
    response.headers["Cache-Control"] = "no-store"
    return public_job(authorize(run_id, x_review_token), page)


@router.post("/runs/{run_id}/classify", status_code=202)
async def start_classification(run_id: str, body: Classification, response: Response,
                               x_review_token: Annotated[str | None, Header()] = None,
                               x_anthropic_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    job = authorize(run_id, x_review_token)
    api_key = key_required(x_anthropic_key)
    if job.downloads:
        raise HTTPException(409, "Wait for the artifact download to finish before starting another phase.")
    if job.spec is None or (job.task and not job.task.done()) or job.status == "complete":
        raise HTTPException(409, "Wait for a valid specification or the current phase to finish.")
    if body.scope == "all" and not job.checkpoint_seen:
        raise HTTPException(409, "Classify and review the first items before continuing across the full snapshot.")
    if body.scope == "pilot" and job.scope == "all":
        raise HTTPException(409, "Resume the full-snapshot phase to keep this run's scope consistent.")
    job.owner_hash = reserve_worker(api_key, job)
    job.stopped.clear()
    job.scope = body.scope
    job.status = "running"
    job.message = "Classifying the first items for review." if body.scope == "pilot" else "Continuing across all items using the same classifier rules."
    job.task = asyncio.create_task(classify_job(job, api_key))
    return public_job(job)


@router.post("/runs/{run_id}/cancel")
async def cancel_run(run_id: str, response: Response,
                     x_review_token: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    job = authorize(run_id, x_review_token)
    if job.task and not job.task.done():
        stop(job)
        await asyncio.shield(job.task)
    return public_job(job)


@router.get("/runs/{run_id}/download/{artifact}")
async def download(run_id: str, artifact: str,
                   x_review_token: Annotated[str | None, Header()] = None):
    job = authorize(run_id, x_review_token)
    if artifact not in ARTIFACTS:
        raise HTTPException(404, "Unknown artifact.")
    if job.status in ACTIVE_STATUSES and artifact != "spec":
        raise HTTPException(409, "Download results after the current phase finishes.")
    filename, media_type = ARTIFACTS[artifact]
    path = job.directory / filename
    if not path.is_file():
        raise HTTPException(404, "This artifact is not ready yet.")
    job.downloads += 1

    def finished():
        job.downloads -= 1

    return FileResponse(path, media_type=media_type, filename=filename,
                        headers={"Cache-Control": "no-store"}, background=BackgroundTask(finished))
