"""Durable, private website runs of the Caliper item-analysis pipeline.

The CLI and website share preparation, specification generation, classification,
and reports. Only this adapter knows about HTTP, BYOK credentials, and job life
cycles. Model calls use the shared OpenAI client; credentials never enter saved inputs.
"""

from __future__ import annotations

import asyncio
from concurrent.futures import CancelledError as FutureCancelledError
from copy import deepcopy
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

from fastapi import APIRouter, File, Form, Header, HTTPException, Query, Response, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from anthropic_api_package_release.item_analysis import classify, generate, model_client, prepare, report, score_report, scoring
from anthropic_api_package_release.item_analysis.data import file_sha256
from anthropic_api_package_release.item_analysis.catalog import CATALOG_VERSION
from anthropic_api_package_release.item_analysis.storage import check_prepared, read_json, write_json
from . import db, item_analysis_assessment, item_analysis_databank, item_analysis_direct, item_analysis_source
from . import item_analysis_store as store

router = APIRouter(prefix="/api/item-analysis", tags=["Item analysis"])
FIXTURE_PATH = Path(__file__).with_name("item_analysis_demo.json")
CHECKPOINT_SIZE = 100
PAGE_SIZE = 20
MAX_ACTIVE = 3
MAX_RETAINED = 10  # Idle in-memory cache size; saved runs are not limited to ten.
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
    example_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]{0,159}$")
    # Retained for older clients; new runs always assemble the fixed scoring context.
    specification_mode: Literal["generate", "provided"] = "generate"


class Classification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scope: Literal["pilot", "all"]
    pilot_review_confirmed: bool = False


@dataclass
class AnalysisJob:
    run_id: str
    secret_digest: str = field(repr=False)
    example: dict
    directory: Path = field(repr=False)
    status: str = "preparing"
    message: str = "Preparing the item snapshot and assessment evidence."
    spec: dict | None = None
    summary: dict | None = None
    total: int = 0
    scope: str | None = None
    results: dict = field(default_factory=dict, repr=False)
    model: dict = field(default_factory=lambda: {
        "provider": model_client.PROVIDER,
        "model_id": model_client.MODEL_ID,
        "reasoning_effort": model_client.REASONING_EFFORT,
    })
    usage: dict = field(default_factory=lambda: {
        "input_tokens": 0, "output_tokens": 0,
        "cached_input_tokens": 0, "reasoning_tokens": 0,
    })
    task: asyncio.Task | None = field(default=None, repr=False)
    provider_call: object | None = field(default=None, repr=False)
    provider_tasks: set = field(default_factory=set, repr=False)
    provider_error: dict | None = None
    failure: dict | None = None
    data_ready: bool = False
    pilot_item_ids: set[str] = field(default_factory=set, repr=False)
    stopped: Event = field(default_factory=Event, repr=False)
    owner_hash: str | None = field(default=None, repr=False)
    checkpoint_seen: bool = False
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    downloads: int = 0
    assessment: dict | None = field(default=None, repr=False)
    source: dict | None = field(default=None, repr=False)
    call_sequence: int = 0


jobs: dict[str, AnalysisJob] = {}


class AnalysisFileResponse(FileResponse):
    """Release the phase guard even if a download disconnects or is cancelled."""

    def __init__(self, path: Path, *, job: AnalysisJob, **kwargs):
        super().__init__(path, **kwargs)
        self.job = job

    async def __call__(self, scope, receive, send):
        try:
            await super().__call__(scope, receive, send)
        finally:
            self.job.downloads -= 1


def storage_root() -> Path:
    return db.DEFAULT_DB_PATH.parent / "item-analysis"


def persist(job: AnalysisJob) -> None:
    store.save_metadata(job.directory, {
        "run_id": job.run_id, "secret_digest": job.secret_digest,
        "example": job.example, "status": job.status, "message": job.message,
        "total": job.total, "scope": job.scope, "model": job.model,
        "created_at": job.created_at, "updated_at": job.updated_at,
        "checkpoint_seen": job.checkpoint_seen, "data_ready": job.data_ready,
        "call_sequence": job.call_sequence,
        "failure": job.failure, "provider_error": job.provider_error,
        "assessment": item_analysis_assessment.public_assessment(job.assessment) if job.assessment else None,
    })


def visible_result(record: dict) -> dict:
    visible = deepcopy({key: record[key] for key in (
        "item_id", "status", "labels", "dimensions", "analysis_type") if key in record})
    visible["classifier_errors"] = {
        classifier_id: "No valid judgment was saved. Retry this phase."
        for classifier_id in record.get("classifier_errors", {})
    }
    return visible


def restore_job(directory: Path, metadata: dict) -> AnalysisJob:
    job = AnalysisJob(metadata["run_id"], metadata["secret_digest"], metadata["example"], directory,
                      **{key: metadata[key] for key in (
                          "status", "message", "total", "scope", "model", "created_at", "updated_at",
                          "checkpoint_seen", "data_ready", "failure", "provider_error", "assessment", "call_sequence") if key in metadata})
    interrupted = job.status in ACTIVE_STATUSES
    try:
        job.usage, saved_sequence = store.load_usage(directory)
        job.call_sequence = max(job.call_sequence, saved_sequence)
        if job.data_ready:
            check_prepared(directory)
            with (directory / "items.jsonl").open(encoding="utf-8") as stream:
                job.pilot_item_ids = {json.loads(line)["item_id"] for line in islice(stream, CHECKPOINT_SIZE)}
        if (directory / "classifier_spec.json").is_file():
            from anthropic_api_package_release.item_analysis.storage import check_specification
            check_specification(directory)
            job.spec = read_json(directory / "classifier_spec.json")
        if job.spec:
            job.results = {key: visible_result(value) for key, value in classify.read_results(
                directory / "results.jsonl", repair_tail=True).items()}
            if interrupted:
                job.summary = report.generate_report(directory)
            elif (directory / "summary.json").is_file():
                job.summary = read_json(directory / "summary.json")
            if scoring.is_score_spec(job.spec) and (
                not job.summary or len(job.summary.get("dimensions", [])) != len(scoring.DIMENSIONS)
                or any("mean_score" not in dimension for dimension in job.summary["dimensions"])
            ):
                # Existing six-score runs gain derived averages without changing
                # their frozen scoring inputs or making additional model calls.
                job.summary = report.generate_report(
                    directory, run_metadata=job.summary.get("run") if job.summary else None)
        if interrupted:
            if job.spec:
                job.status, job.message = "cancelled", "The server stopped during this phase. Saved judgments are retained; resume with your OpenAI key."
            else:
                job.status, job.message = "failed", "Context preparation was interrupted. Start a new analysis to prepare the context again."
                job.failure = {"stage": "specification", "code": "interrupted", "message": job.message}
            job.provider_error = None
            persist(job)
    except (OSError, ValueError, KeyError, TypeError):
        job.status, job.message = "failed", "Saved analysis files could not be restored. Start a new analysis or contact the maintainer."
        job.failure = {"stage": "restoration", "code": "saved_files_invalid", "message": job.message}
        job.data_ready = False
        job.spec = None
    return job


def prepared_directory() -> Path | None:
    """Use a local snapshot only when an administrator explicitly configures it."""
    configured = os.environ.get("ITEM_ANALYSIS_PREPARED_DIR", "").strip()
    return Path(configured).expanduser() if configured else None


def usable_context_file(path: Path) -> bool:
    """Historical induced rules remain downloadable artifacts, never new-run rules."""
    try:
        return read_json(path).get("fixed_catalog_version") == CATALOG_VERSION
    except (OSError, ValueError, TypeError):
        return False


def examples() -> list[dict]:
    fixture = read_json(FIXTURE_PATH)
    illustrative = {"id": "illustrative", **{key: fixture[key] for key in (
        "title", "description", "benchmark", "deployment", "source_label")},
        "item_count": len(fixture["items"]), "available": True, "supplied_spec_available": True}
    directory = prepared_directory()
    if directory is None:
        return [*item_analysis_source.source_entries(), illustrative]
    entries = []
    # Source paths come only from server configuration, never HTTP parameters.
    try:
        dataset = read_json(directory / "dataset.json")
        evidence = read_json(directory / "evidence.json")
        available = all((directory / name).is_file() for name in PREPARED_FILES)
        if available:
            entries.append({
                # Preserve the legacy override ID while displaying its actual benchmark.
                "id": "mmlu", "title": f"{dataset['benchmark']} · Prepared assessment",
                "benchmark_title": dataset["benchmark"], "assessment_title": "Prepared assessment",
                "description": "The configured benchmark snapshot and original Caliper assessment. Review 100 items, then continue across the full snapshot.",
                "benchmark": dataset["benchmark"], "deployment": evidence["deployment"],
                "source_label": "Prepared benchmark snapshot with its original assessment; counts apply to this snapshot.",
                "item_count": dataset["item_count"], "available": True,
                "supplied_spec_available": usable_context_file(directory / "classifier_spec.original.json"),
            })
    except (OSError, ValueError, KeyError, TypeError):
        pass  # The bundled example remains runnable on a fresh checkout.
    return [*entries, illustrative]


def sweep() -> None:
    now = time.time()
    retention = store.retention_seconds()
    for run_id, job in list(jobs.items()):
        if retention and (not job.task or job.task.done()) and not job.downloads and now - job.updated_at > retention:
            jobs.pop(run_id, None)
            shutil.rmtree(job.directory, ignore_errors=True)
    if retention and storage_root().is_dir():
        for directory in storage_root().iterdir():
            if directory.name in jobs or store.directory_for(storage_root(), directory.name) is None:
                continue
            try:
                metadata = store.load_metadata(directory)
                if now - metadata["updated_at"] > retention:
                    shutil.rmtree(directory, ignore_errors=True)
            except (OSError, ValueError, KeyError, TypeError):
                continue
    # Drop only cached objects. Frozen input/results and access digests remain on disk.
    idle = sorted((job for job in jobs.values() if (not job.task or job.task.done()) and not job.downloads),
                  key=lambda job: job.updated_at)
    for job in idle[:max(0, len(jobs) - MAX_RETAINED)]:
        jobs.pop(job.run_id, None)


async def shutdown() -> None:
    # Stop and drain writers, retaining their frozen inputs and completed judgments.
    for job in list(jobs.values()):
        if job.task and not job.task.done():
            stop(job)
    await asyncio.gather(*(job.task for job in jobs.values() if job.task), return_exceptions=True)
    for job in jobs.values():
        persist(job)
    jobs.clear()


async def delete_for_assessment(run_id: str) -> None:
    """Honor deletion of the benchmark run across its linked item stages."""
    linked = [job for job in jobs.values() if job.assessment
              and job.assessment["kind"] == "run" and job.assessment["id"] == run_id]
    for job in linked:
        stop(job)
    await asyncio.gather(*(job.task for job in linked if job.task), return_exceptions=True)
    for job in linked:
        # Keep active jobs visible until drained: otherwise authorization could
        # restore the still-existing directory while its writer is stopping.
        jobs.pop(job.run_id, None)
        shutil.rmtree(job.directory, ignore_errors=True)
    if storage_root().is_dir():
        for directory in storage_root().iterdir():
            if store.directory_for(storage_root(), directory.name) is None:
                continue
            try:
                assessment = store.load_metadata(directory).get("assessment") or {}
                if assessment.get("kind") == "run" and assessment.get("id") == run_id:
                    shutil.rmtree(directory, ignore_errors=True)
            except (OSError, ValueError, TypeError):
                continue


def authorize(run_id: str, secret: str | None) -> AnalysisJob:
    sweep()
    job = jobs.get(run_id)
    digest = store.token_digest(secret) if secret and len(secret) <= 512 else ""
    if job is None and digest:
        directory = store.directory_for(storage_root(), run_id)
        try:
            metadata = store.load_metadata(directory) if directory else {}
            if secrets.compare_digest(metadata.get("secret_digest", ""), digest):
                job = restore_job(directory, metadata)
                jobs[run_id] = job
        except (OSError, ValueError, TypeError):
            pass
    if job is None or not digest or not secrets.compare_digest(job.secret_digest, digest):
        raise HTTPException(404, "Analysis not found, deleted, or expired under this server's retention policy.")
    return job


def key_required(value: str | None) -> str:
    if not value or not value.strip():
        raise HTTPException(401, "An OpenAI API key is required for model calls.")
    if len(value) > 512:
        raise HTTPException(400, "Invalid credential length.")
    return value.strip()


def reserve_worker(api_key: str | None, current: AnalysisJob | None = None) -> str | None:
    active = [job for job in jobs.values() if job is not current and job.status in ACTIVE_STATUSES]
    owner = hashlib.sha256(api_key.encode()).hexdigest() if api_key else None
    if len(active) >= MAX_ACTIVE or (owner and any(job.owner_hash == owner for job in active)):
        raise HTTPException(429, "An analysis is already running for this key, or the demo is busy. Try again shortly.")
    return owner


def current_score_summary(job: AnalysisJob, complete: int, errors: int) -> dict | None:
    """Expose all saved item scores while a phase is still running.

    The persisted report is rebuilt at phase boundaries. Its in-memory summary
    can otherwise lag behind saved results, including when expanding a pilot.
    """
    if not job.summary or not scoring.is_score_spec(job.spec):
        return job.summary
    selected = (job.total if job.scope == "all" else min(CHECKPOINT_SIZE, job.total)
                if job.scope == "pilot" else len(job.results))
    if (job.summary.get("completed_items") == complete and job.summary.get("error_items") == errors
            and job.summary.get("experiment", {}).get("selected_items") == selected):
        return job.summary
    dimensions = score_report.summarize_dimensions(job.spec["classifiers"], job.results, selected)
    return {
        **job.summary, "dimensions": dimensions, "classifiers": dimensions,
        "completed_items": complete, "error_items": errors,
        "pending_items": job.total - complete - errors,
        "complete_snapshot": job.total > 0 and complete == job.total,
        "scope": "all items in the prepared snapshot" if job.total > 0 and complete == job.total
                 else "incomplete run over the prepared snapshot",
        "experiment": {
            **job.summary.get("experiment", {}),
            "selected_items": selected, "selected_completed_items": complete,
            "selected_error_items": errors, "selected_pending_items": selected - complete - errors,
            "expected_item_classifier_judgments": selected * len(scoring.DIMENSIONS),
            "completed_item_classifier_judgments": complete * len(scoring.DIMENSIONS),
            "error_item_classifier_judgments": errors * len(scoring.DIMENSIONS),
            "pending_item_classifier_judgments": (selected - complete - errors) * len(scoring.DIMENSIONS),
            "expected_primary_requests": selected,
            "recorded_api_calls": job.call_sequence,
        },
    }


def public_job(job: AnalysisJob, page: int = 1) -> dict:
    six_scores = scoring.is_score_spec(job.spec or {})
    complete = sum(record["status"] == "complete" for record in job.results.values())
    errors = sum(record["status"] == "error" for record in job.results.values())
    classifier_ids = {classifier["id"] for classifier in (job.spec or {}).get("classifiers", [])
                      if classifier["applicable"]}
    judgment_key = "dimensions" if six_scores else "labels"
    completed_judgments = sum(len(classifier_ids.intersection(record.get(judgment_key, {})))
                              for record in job.results.values())
    pilot_judgments = sum(len(classifier_ids.intersection(record.get(judgment_key, {})))
                          for item_id, record in job.results.items() if item_id in job.pilot_item_ids)
    pilot_complete = sum(record["status"] == "complete" for item_id, record in job.results.items()
                         if item_id in job.pilot_item_ids)
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
                    **{key: item.get(key) for key in ("grading_criterion", "item_features", "asset_manifest", "verifier")},
                    "status": result.get("status", "pending"), "labels": result.get("labels"),
                    **({"dimensions": result.get("dimensions")} if six_scores else {}),
                    "classifier_errors": result.get("classifier_errors", {}),
                    "error": ("No valid assessment was saved. Retry this item." if six_scores else
                              "Some classifiers need a retry. Saved judgments are retained.") if result.get("status") == "error" else None,
                })
    return {
        "run_id": job.run_id, "status": job.status, "message": job.message,
        **({"analysis_type": "six_scores"} if six_scores or job.spec is None else {}),
        "created_at": store.timestamp(job.created_at), "updated_at": store.timestamp(job.updated_at),
        "retention": {"automatic_expiry": bool(store.retention_seconds()),
                      "expires_at": store.timestamp(job.updated_at + store.retention_seconds())
                      if store.retention_seconds() and job.status not in ACTIVE_STATUSES else None},
        "example": job.example, "spec": job.spec, "summary": current_score_summary(job, complete, errors),
        "assessment": item_analysis_assessment.public_assessment(job.assessment) if job.assessment else None,
        "processed": len(job.results), "total": job.total, "complete": complete, "errors": errors,
        "completed_judgments": completed_judgments,
        "remaining_judgments": {
            "pilot": max(0, min(CHECKPOINT_SIZE, job.total) * len(classifier_ids) - pilot_judgments),
            "all": max(0, job.total * len(classifier_ids) - completed_judgments),
        },
        **({"remaining_requests": {
            "pilot": max(0, min(CHECKPOINT_SIZE, job.total) - pilot_complete),
            "all": max(0, job.total - complete),
        }} if six_scores else {}),
        "items": rows, "pagination": {"page": page, "page_size": PAGE_SIZE, "total_pages": pages},
        "usage": dict(job.usage), "model": dict(job.model), "scope": job.scope,
        "can_continue": (six_scores or job.checkpoint_seen) and job.spec is not None
                        and job.status in {"ready", "checkpoint", "cancelled", "failed"},
        "error": job.message if job.status == "failed" else None,
        "provider_error": dict(job.provider_error) if job.status == "failed" and job.provider_error else None,
        "failure": dict(job.failure) if job.status == "failed" and job.failure else None,
    }


def prepare_job(job: AnalysisJob, example_id: str) -> Path:
    """Prepare immutable inputs, returning the optional provided-spec location."""
    if example_id != "illustrative":
        source = prepared_directory()
        if source is None:
            with TemporaryDirectory(prefix="prepared-", dir=job.directory.parent) as temporary:
                prepared = Path(temporary)
                item_analysis_source.prepare_source(prepared, stopped=job.stopped.is_set, example_id=example_id)
                for path in prepared.iterdir():
                    if path.is_file():
                        shutil.copyfile(path, job.directory / path.name)
        else:
            try:
                check_prepared(source)
                for name in PREPARED_FILES:
                    shutil.copyfile(source / name, job.directory / name)
                supplied = source / "classifier_spec.original.json"
                if supplied.is_file():
                    shutil.copyfile(supplied, job.directory / "provided_spec.json")
                check_prepared(job.directory)
            except (OSError, ValueError, KeyError, TypeError):
                raise item_analysis_source.DatasetPreparationError(
                    "The configured benchmark snapshot could not be prepared. Ask the website administrator to check its files."
                ) from None
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
            prepared = inputs / "prepared"
            prepare.prepare(inputs, items_path, prepared,
                            source_repo="caliper-authored-illustrative-example",
                            source_revision=file_sha256(FIXTURE_PATH), source_table=FIXTURE_PATH.name)
            for path in prepared.iterdir():
                if path.is_file():
                    shutil.copyfile(path, job.directory / path.name)
        write_json(job.directory / "provided_spec.json", fixture["classifier_spec"])
    # Preserve checksums/revisions without exporting private server filesystem paths.
    dataset = read_json(job.directory / "dataset.json")
    dataset["source"].pop("path", None)
    evidence = read_json(job.directory / "evidence.json")
    evidence.pop("assessment_dir", None)
    write_json(job.directory / "evidence.json", evidence)
    dataset["evidence_sha256"] = file_sha256(job.directory / "evidence.json")
    write_json(job.directory / "dataset.json", dataset)
    # Catalog counts describe the advertised source. A run always displays the
    # exact snapshot and deployment that its frozen inputs actually contain.
    job.example = {
        **job.example, "benchmark": dataset["benchmark"],
        "deployment": evidence["deployment"], "item_count": dataset["item_count"],
        **{f"source_{key}": dataset["source"].get(key) for key in ("repo", "revision", "table", "sha256")},
    }
    return job.directory / "provided_spec.json"


def model_bridge(job: AnalysisJob, api_key: str):
    """Adapt the shared synchronous model callback to a request-scoped async client.

    The worker blocks on the event loop's request. Cancellation cancels that
    request and signals the shared classifier to stop before another classifier call.
    Only this closure holds the credential. The client maps provider failures to
    safe diagnostic messages; unrecognized exception details are discarded.
    """
    loop = asyncio.get_running_loop()

    def record_usage(arguments, sequence, started_at, result=None, *, status="complete", error_code=None):
        store.record_call(job.directory, {
            "sequence": sequence, "step": arguments["step"], "provider": "openai",
            "model": result.model if result else arguments["model"],
            "reasoning_effort": arguments["reasoning_effort"], "max_tokens": arguments["max_tokens"],
            "started_at": store.timestamp(started_at), "finished_at": store.timestamp(time.time()),
            "status": status, "error_code": error_code, "usage_known": result is not None,
            **({key: getattr(result, key) for key in store.COUNTERS} if result else {}),
            **({"latency_ms": result.latency_ms} if result else {}),
        }, job.usage)

    def redacted(value):
        if isinstance(value, str):
            return value.replace(api_key, "[redacted]")
        if isinstance(value, dict):
            return {key: redacted(item) for key, item in value.items()}
        if isinstance(value, list):
            return [redacted(item) for item in value]
        return value

    def provider_failure(error):
        # public_message is derived from an allowlisted code, never an SDK body.
        message = error.public_message
        job.provider_error = {"code": error.code, "status_code": error.status_code, "message": message}
        return RuntimeError(message)

    async def request(arguments):
        task = asyncio.current_task()
        job.provider_tasks.add(task)
        started_at = time.time()
        job.call_sequence += 1
        sequence = job.call_sequence
        try:
            store.append_jsonl(job.directory / "requests.jsonl", {
                "sequence": sequence, "started_at": store.timestamp(started_at),
                **redacted({key: arguments[key] for key in (
                    "model", "system", "user", "max_tokens", "reasoning_effort", "step")}),
            })
            persist(job)
            try:
                result = await model_client.call_text_async(
                    api_key=api_key, model=arguments["model"], system=arguments["system"],
                    user=arguments["user"], max_tokens=arguments["max_tokens"],
                    reasoning_effort=arguments["reasoning_effort"],
                )
            except asyncio.CancelledError:
                record_usage(arguments, sequence, started_at, status="cancelled", error_code="interrupted")
                raise
            except model_client.ModelResponseError as error:
                record_usage(arguments, sequence, started_at, error.result, status="failed", error_code=error.code)
                raise provider_failure(error) from None
            except model_client.ModelRequestError as error:
                record_usage(arguments, sequence, started_at, status="failed", error_code=error.code)
                raise provider_failure(error) from None
            except Exception:
                error = model_client.ModelRequestError(code="internal_error")
                record_usage(arguments, sequence, started_at, status="failed", error_code=error.code)
                raise provider_failure(error) from None
            record_usage(arguments, sequence, started_at, result)
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


def prepare_assessment_job(job: AnalysisJob, upload: dict | None) -> Path:
    if upload is None:
        item_analysis_databank.prepare_candidate(job.directory, job.source, stopped=job.stopped.is_set)
    else:
        item_analysis_assessment.prepare_upload(job.directory, job.assessment, **upload)
    if job.assessment["kind"] == "direct":
        item_analysis_direct.attach_context(job.directory, job.assessment, confirmed_source=job.source is not None)
    else:
        item_analysis_assessment.attach_assessment(job.directory, job.assessment, confirmed_source=job.source is not None)
    check_prepared(job.directory)
    dataset = read_json(job.directory / "dataset.json")
    job.example = {**job.example, "benchmark": job.assessment["benchmark"],
                   "deployment": job.assessment["deployment"], "item_count": dataset["item_count"],
                   **{f"source_{key}": dataset["source"].get(key) for key in ("repo", "revision", "table", "sha256")}}
    return job.directory / "provided_spec.json"


async def initialize(job: AnalysisJob, mode: str, api_key: str | None, upload: dict | None = None) -> None:
    phase = "preparation"
    try:
        if job.assessment:
            supplied = await drained_thread(prepare_assessment_job, job, upload)
        else:
            supplied = await drained_thread(prepare_job, job, job.example["id"])
        upload = None
        job.total = read_json(job.directory / "dataset.json")["item_count"]
        with (job.directory / "items.jsonl").open(encoding="utf-8") as stream:
            job.pilot_item_ids = {json.loads(line)["item_id"] for line in islice(stream, CHECKPOINT_SIZE)}
        job.data_ready = True
        write_json(job.directory / "website_provenance.json", {
            "version": 2, "analysis_type": "six_scores",
            "created_at": store.timestamp(job.created_at), "model": job.model,
            "context_preparation": "deterministic; no model calls",
            "implementation_sha256": {name: file_sha256(Path(module.__file__)) for name, module in (
                ("classify.py", classify), ("scoring.py", scoring), ("model_client.py", model_client))},
        })
        if job.assessment and job.assessment.get("evidence_directory"):
            original = Path(job.assessment["evidence_directory"])
            pdf = original / "pdfs" / "review.pdf"
            if (pdf.is_file() and not pdf.is_symlink() and pdf.resolve().is_relative_to(original.resolve())
                    and pdf.stat().st_size <= 32 * 1024 * 1024):
                shutil.copyfile(pdf, job.directory / "original_benchmark_report.pdf")
        persist(job)
        if job.stopped.is_set():
            return
        phase = "specification"
        job.message = "Preparing shared deployment evidence and the fixed six-dimension rubric."
        persist(job)
        job.spec = await drained_thread(scoring.prepare_context, job.directory)
        phase = "report"
        metadata = read_json(job.directory / "specification.json")
        metadata.get("source", {}).pop("path", None)
        write_json(job.directory / "specification.json", metadata)
        await refresh_report(job)
        job.status, job.message = "ready", "Context and items are ready. Choose how many items to score on all six dimensions."
    except (item_analysis_source.DatasetAccessError, item_analysis_source.DatasetPreparationError,
            item_analysis_databank.DataBankError) as error:
        job.status, job.message = "failed", str(error)
        job.failure = {"stage": phase, "code": "dataset_unavailable", "message": job.message}
    except generate.SpecificationValidationError as error:
        job.status, job.message = "failed", error.public_message
        job.failure = {"stage": phase, "code": error.code, "message": job.message}
    except Exception:
        job.status = "failed"
        if job.provider_error:
            job.message = job.provider_error["message"]
            code = job.provider_error["code"]
        else:
            # Keep diagnostics specific to the failed stage without echoing
            # exception bodies, model output, source text, or credentials.
            code, job.message = {
                "preparation": ("preparation_failed", "The website could not prepare the benchmark items or deployment evidence. No model calls were made. Share this error with the maintainer."),
                "specification": ("specification_failed", "The website could not prepare the shared scoring context. No model calls were made. Share this error with the maintainer."),
                "report": ("report_failed", "The scoring context is ready, but the website could not prepare its results view. No items have been scored. Share this error with the maintainer."),
            }[phase]
        job.failure = {"stage": phase, "code": code, "message": job.message}
    finally:
        await drain_provider(job)
        api_key = None
        finish_phase(job)


def finish_phase(job: AnalysisJob) -> None:
    if job.stopped.is_set():
        job.status, job.message = "cancelled", "Analysis stopped. Completed results are retained."
    job.owner_hash = None
    job.updated_at = time.time()
    persist(job)


async def classify_job(job: AnalysisJob, api_key: str) -> None:
    loop = asyncio.get_running_loop()

    def save_result(record):
        # Keep raw model attempts private; the website only needs validated labels.
        visible = visible_result(record)
        loop.call_soon_threadsafe(job.results.__setitem__, record["item_id"], visible)

    try:
        execution = await drained_thread(
            classify.run, job.directory, limit=CHECKPOINT_SIZE if job.scope == "pilot" else None,
            resume=(job.directory / "run.json").exists(), call=model_bridge(job, api_key),
            **job.model, on_result=save_result,
            should_stop=job.stopped.is_set,
        )
        await refresh_report(job)
        if execution["fatal_error"]:
            job.status = "failed"
            job.message = (job.provider_error["message"] if job.provider_error else
                           "The model request failed. Retry to resume saved progress; if it persists, contact the website maintainer.")
        elif execution["full_dataset_complete"]:
            job.status, job.message = "complete", "Every item in this snapshot has a saved assessment. Inspect the evidence and export the results."
        elif job.scope == "pilot" and execution["complete"] == execution["target_items"]:
            job.checkpoint_seen = True
            job.status = "checkpoint"
            job.message = "The selected items are ready. Inspect their assessments or continue across the snapshot."
        else:
            job.status, job.message = "failed", "Some items still need valid assessments. Retry to resume; completed items are retained."
    except Exception:
        job.status = "failed"
        job.message = (job.provider_error["message"] if job.provider_error else
                       "The analysis could not finish. Completed results are retained; retry with the same frozen specification.")
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


@router.get("/assessment")
async def assessment_context(response: Response,
                             kind: Literal["run", "gallery"],
                             id: Annotated[str, Query(min_length=1, max_length=160)]) -> dict:
    response.headers["Cache-Control"] = "no-store"
    assessment = item_analysis_assessment.resolve(kind, id)
    return await setup_context(assessment)


async def setup_context(assessment: dict, query: str | None = None) -> dict:
    discovery = await drained_thread(item_analysis_databank.search_candidates, assessment, query)
    return {
        "assessment": item_analysis_assessment.public_assessment(assessment),
        "benchmark_identity": assessment["benchmark_identity"],
        "sources": discovery["candidates"], "checkpoint_size": CHECKPOINT_SIZE,
        "catalog": {key: value for key, value in discovery.items() if key != "candidates"},
        "upload": {"max_bytes": item_analysis_assessment.MAX_UPLOAD_BYTES,
                   "max_items": item_analysis_assessment.MAX_UPLOAD_ITEMS,
                   "formats": ["csv", "json"], "required_fields": ["content"],
                   "optional_fields": ["item_id", "reference_answer", "grading_criterion", "verifier", "item_features", "asset_manifest"],
                   "item_id": "Generated from the row number when omitted.",
                   "json_shape": "An array of item objects."},
    }


@router.post("/direct/setup")
async def direct_context(body: item_analysis_direct.DirectSetup, response: Response) -> dict:
    """Discover datasets without saving context or making provider requests."""
    response.headers["Cache-Control"] = "no-store"
    context = item_analysis_direct.DirectContext.model_validate(body.model_dump(exclude={"q"}))
    return await setup_context(item_analysis_direct.resolve(context), body.q)


@router.get("/sources")
async def search_sources(response: Response,
                         kind: Literal["run", "gallery"],
                         id: Annotated[str, Query(min_length=1, max_length=160)],
                         q: Annotated[str | None, Query(max_length=200)] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    assessment = item_analysis_assessment.resolve(kind, id)
    discovery = await drained_thread(item_analysis_databank.search_candidates, assessment, q)
    return {"sources": discovery["candidates"], "benchmark_identity": assessment["benchmark_identity"],
            "catalog": {key: value for key, value in discovery.items() if key != "candidates"}}


@router.post("/runs/from-assessment", status_code=202)
async def create_assessment_run(
        response: Response,
        assessment_kind: Annotated[Literal["run", "gallery"], Form()],
        assessment_id: Annotated[str, Form(min_length=1, max_length=160)],
        source_id: Annotated[str | None, Form(max_length=300)] = None,
        source_revision: Annotated[str | None, Form(max_length=80)] = None,
        benchmark_confirmed: Annotated[bool, Form()] = False,
        items_file: Annotated[UploadFile | None, File()] = None,
        x_openai_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    assessment = item_analysis_assessment.resolve(assessment_kind, assessment_id)
    return await create_context_job(assessment, source_id, source_revision, benchmark_confirmed, items_file)


@router.post("/runs/from-context", status_code=202)
async def create_direct_run(
        response: Response,
        context_json: Annotated[str, Form(min_length=1, max_length=300_000)],
        source_id: Annotated[str | None, Form(max_length=300)] = None,
        source_revision: Annotated[str | None, Form(max_length=80)] = None,
        benchmark_confirmed: Annotated[bool, Form()] = False,
        items_file: Annotated[UploadFile | None, File()] = None,
        x_openai_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    assessment = item_analysis_direct.resolve(item_analysis_direct.parse_context(context_json))
    return await create_context_job(assessment, source_id, source_revision, benchmark_confirmed, items_file)


async def create_context_job(assessment: dict, source_id: str | None, source_revision: str | None,
                             benchmark_confirmed: bool, items_file: UploadFile | None, api_key: str | None = None) -> dict:
    """Both starting points share dataset confirmation, preparation, and privacy."""
    if not benchmark_confirmed:
        raise HTTPException(400, "Confirm the benchmark identity and selected item snapshot before starting item analysis.")
    if bool(source_id) == bool(items_file):
        raise HTTPException(400, "Select a matching dataset snapshot or upload an item file.")
    if items_file and source_revision:
        raise HTTPException(400, "Choose one item source: an uploaded file or a confirmed Data Bank snapshot.")
    upload = None
    source = None
    if items_file:
        try:
            payload = await items_file.read(item_analysis_assessment.MAX_UPLOAD_BYTES + 1)
            rows = item_analysis_assessment.parse_upload(payload, items_file.filename or "")
            upload = {"rows": rows, "payload_sha256": hashlib.sha256(payload).hexdigest(),
                      "suffix": Path(items_file.filename).suffix.lower()}
        finally:
            await items_file.close()
        example = {"id": "upload", "title": "Uploaded benchmark items", "benchmark": assessment["benchmark"],
                   "deployment": assessment["deployment"], "source_label": "Uploaded item snapshot",
                   "item_count": len(rows), "available": True, "supplied_spec_available": False}
    else:
        if not source_revision:
            raise HTTPException(409, "Select and confirm the Data Bank snapshot again; its revision is required.")
        try:
            source = deepcopy(await drained_thread(item_analysis_databank.resolve_candidate, source_id))
        except item_analysis_databank.DataBankError as error:
            raise HTTPException(409, str(error)) from None
        if source_revision != source["source_revision"]:
            raise HTTPException(409, "The selected snapshot revision changed. Search and confirm the dataset again.")
        if not source["available"]:
            raise HTTPException(503, source.get("unavailable_reason") or "This dataset is unavailable. Upload the matching items instead.")
        example = {**source, "deployment": assessment["deployment"], "supplied_spec_available": False}
    sweep()
    owner = reserve_worker(api_key)
    run_id = secrets.token_hex(16)
    directory = storage_root() / run_id
    directory.mkdir(mode=0o700, parents=True)
    secret = secrets.token_urlsafe(32)
    job = AnalysisJob(run_id, store.token_digest(secret), example, directory,
                      total=example["item_count"], owner_hash=owner, assessment=assessment, source=source)
    if assessment["kind"] == "direct":
        job.message = "Preparing the confirmed item snapshot and your deployment requirements."
    jobs[run_id] = job
    persist(job)
    job.task = asyncio.create_task(initialize(job, "generate", api_key, upload))
    return {**public_job(job), "run_secret": secret}


@router.post("/runs", status_code=202)
async def create_run(body: NewRun, response: Response,
                     x_openai_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    api_key = None  # Preparing shared evidence never requires or retains a provider key.
    example = next((entry for entry in examples() if entry["id"] == body.example_id), None)
    if example is None:
        raise HTTPException(404, "This example is not configured on the server.")
    if not example["available"]:
        raise HTTPException(503, example.get("unavailable_reason") or "This dataset is currently unavailable. Try again later.")
    sweep()
    owner = reserve_worker(api_key)
    run_id = secrets.token_hex(16)
    directory = storage_root() / run_id
    directory.mkdir(mode=0o700, parents=True)
    secret = secrets.token_urlsafe(32)
    job = AnalysisJob(run_id, store.token_digest(secret), example, directory,
                      total=example["item_count"], owner_hash=owner)
    jobs[run_id] = job
    persist(job)
    job.task = asyncio.create_task(initialize(job, body.specification_mode, api_key))
    return {**public_job(job), "run_secret": secret}


@router.get("/runs/{run_id}")
async def get_run(run_id: str, response: Response,
                  x_review_token: Annotated[str | None, Header()] = None,
                  page: Annotated[int, Query(ge=1)] = 1) -> dict:
    response.headers["Cache-Control"] = "no-store"
    return public_job(authorize(run_id, x_review_token), page)


@router.post("/runs/{run_id}/classify", status_code=202)
async def start_classification(run_id: str, body: Classification, response: Response,
                               x_review_token: Annotated[str | None, Header()] = None,
                               x_openai_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    job = authorize(run_id, x_review_token)
    api_key = key_required(x_openai_key)
    if job.downloads:
        raise HTTPException(409, "Wait for the artifact download to finish before starting another phase.")
    if job.spec is None or (job.task and not job.task.done()) or job.status == "complete":
        raise HTTPException(409, "Wait for a valid specification or the current phase to finish.")
    six_scores = scoring.is_score_spec(job.spec)
    if body.scope == "all" and not job.checkpoint_seen and not six_scores:
        raise HTTPException(409, "Classify and review the first items before continuing across the full snapshot.")
    if (not six_scores and body.scope == "all" and job.assessment and job.assessment["kind"] == "direct"
            and not body.pilot_review_confirmed):
        raise HTTPException(400, "Confirm that you reviewed the pilot judgments and criteria before continuing across the full snapshot.")
    if body.scope == "pilot" and job.scope == "all":
        raise HTTPException(409, "Resume the full-snapshot phase to keep this run's scope consistent.")
    job.owner_hash = reserve_worker(api_key, job)
    job.stopped.clear()
    job.provider_error = None
    job.failure = None
    job.scope = body.scope
    job.status = "running"
    job.message = ("Scoring the selected items on all six dimensions." if body.scope == "pilot" else
                   "Scoring all items in this snapshot on all six dimensions.") if six_scores else (
                       "Classifying the first items for review." if body.scope == "pilot" else
                       "Continuing across all items using the same classifier rules.")
    persist(job)
    job.task = asyncio.create_task(classify_job(job, api_key))
    return public_job(job)


@router.delete("/runs/{run_id}", status_code=204)
async def delete_analysis(run_id: str, x_review_token: Annotated[str | None, Header()] = None):
    job = authorize(run_id, x_review_token)
    if job.downloads:
        raise HTTPException(409, "Wait for the artifact download to finish before discarding this analysis.")
    if job.task and not job.task.done():
        stop(job)
        await asyncio.shield(job.task)
    jobs.pop(run_id, None)
    shutil.rmtree(job.directory)
    return Response(status_code=204, headers={"Cache-Control": "no-store"})


@router.get("/runs/{run_id}/package")
async def download_package(run_id: str, x_review_token: Annotated[str | None, Header()] = None):
    from anthropic_api_package_release.item_analysis.package import build_results_package

    job = authorize(run_id, x_review_token)
    if job.status in ACTIVE_STATUSES or (job.task and not job.task.done()) or job.downloads:
        raise HTTPException(409, "Wait for the current phase or download to finish before exporting the results package.")
    if not job.spec:
        raise HTTPException(409, "Prepare valid criteria before exporting a results package.")
    job.downloads += 1
    try:
        path = await drained_thread(build_results_package, job.directory,
                                    run_id=job.run_id, status=job.status, scope=job.scope,
                                    created_at=store.timestamp(job.created_at), updated_at=store.timestamp(job.updated_at),
                                    usage=job.usage, model=job.model)
    except asyncio.CancelledError:
        job.downloads -= 1
        raise
    except Exception:
        job.downloads -= 1
        raise HTTPException(500, "The results package could not be prepared. Saved results are retained.") from None

    return AnalysisFileResponse(path, job=job, media_type="application/zip", filename=path.name,
                                headers={"Cache-Control": "no-store"})


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
    if job.downloads:
        raise HTTPException(409, "Wait for the current download to finish before downloading another artifact.")
    if artifact not in ARTIFACTS:
        raise HTTPException(404, "Unknown artifact.")
    if job.status in ACTIVE_STATUSES and artifact != "spec":
        raise HTTPException(409, "Download results after the current phase finishes.")
    filename, media_type = ARTIFACTS[artifact]
    path = job.directory / filename
    if not path.is_file():
        raise HTTPException(404, "This artifact is not ready yet.")
    job.downloads += 1

    return AnalysisFileResponse(path, job=job, media_type=media_type, filename=filename,
                                headers={"Cache-Control": "no-store"})
