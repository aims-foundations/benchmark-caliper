"""Seeded sample reviews with temporary indexed results.

Keys and deployment answers remain in memory. A run secret protects polling,
downloads, and cancellation. No worker queue or durable resume is required.
"""

from __future__ import annotations

import asyncio
from collections import Counter
from contextlib import closing
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import secrets
import time
from threading import Event
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from huggingface_hub import get_token
from openai import AsyncOpenAI, AuthenticationError, RateLimitError, OpenAIError
from pydantic import BaseModel, ConfigDict, Field

from bayesian_auditing.sampling import (
    SAMPLE_SIZE, iter_sample_items, prepare_samples, sample_upper_bound, sampling_policy,
)
from bayesian_auditing.scoring import SCORING_POLICY
from bayesian_auditing.judge import (
    AsyncJudge, DEFAULT_MODEL, DEFAULT_REASONING_EFFORT, DEFAULT_MAX_OUTPUT_TOKENS, PROMPT_PATH,
)
from .item_review_store import ReviewStore
from . import db

router = APIRouter(prefix="/api/item-review", tags=["Item review"])
INVENTORY_PATH = Path(__file__).with_name("item_review_inventory.json")
MAX_ACTIVE = 3
MAX_RETAINED = 30
RETENTION_SECONDS = 3600
RESULTS_PAGE_SIZE = 20
REVIEW_CONCURRENCY = int(os.environ.get("ITEM_REVIEW_CONCURRENCY", "4"))
if not 1 <= REVIEW_CONCURRENCY <= 16:
    raise ValueError("ITEM_REVIEW_CONCURRENCY must be between 1 and 16")


def inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


class Deployment(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    task: str = Field(min_length=10, max_length=4000)
    users: str = Field(min_length=3, max_length=2000)
    inputs: str = Field(min_length=3, max_length=2000)
    outputs: str = Field(min_length=3, max_length=2000)
    success: str = Field(min_length=3, max_length=2000)
    constraints: str = Field(default="", max_length=2000)

    def describe(self) -> str:
        labels = {"task": "Task and setting", "users": "Users, language, and location",
                  "inputs": "Expected inputs and interaction", "outputs": "Expected outputs",
                  "success": "Success criteria", "constraints": "Constraints and failures to check"}
        return "\n\n".join(f"{labels[key]}:\n{value or 'Unspecified'}" for key, value in self.model_dump().items())


class ReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    deployment: Deployment


@dataclass
class ReviewJob:
    run_id: str
    secret: str = field(repr=False)
    owner_hash: str = field(repr=False)
    request: ReviewRequest = field(repr=False)
    inventory: dict = field(default_factory=lambda: inventory(), repr=False)
    created_at: float = field(default_factory=time.monotonic)
    finished_at: float | None = None
    task: asyncio.Task | None = field(default=None, repr=False)
    status: str = "preparing"
    message: str = "Preparing the fixed sample from both dataset branches. No model calls yet."
    source_rows: int = 0
    total: int = 0
    sample_complete: bool = False
    prepared_benchmarks: int = 0
    downloads: int = 0
    results: ReviewStore = field(default_factory=ReviewStore, repr=False)
    usage: Counter = field(default_factory=Counter)


jobs: dict[str, ReviewJob] = {}


def sweep() -> None:
    now = time.monotonic()
    for run_id, job in list(jobs.items()):
        if job.finished_at is not None and not job.downloads and now - job.finished_at > RETENTION_SECONDS:
            jobs.pop(run_id, None)
            job.results.close()


async def shutdown() -> None:
    tasks = [job.task for job in jobs.values() if job.task and not job.task.done()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    for job in jobs.values():
        job.results.close()
    jobs.clear()


@router.get("/catalog")
async def catalog(response: Response) -> dict:
    response.headers["Cache-Control"] = "no-store"
    data = inventory()
    benchmarks = sorted({table["benchmark"] for table in data["tables"]})
    return {
        "model": DEFAULT_MODEL, "reasoning_effort": DEFAULT_REASONING_EFFORT,
        "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS,
        "scoring_policy": SCORING_POLICY,
        "branches": data["branches"], "dataset_access_configured": bool(get_token()),
        "table_count": len(data["tables"]),
        "source_rows": sum(table["row_count"] for table in data["tables"]),
        "sampling": sampling_policy(), "sample_max_items": sample_upper_bound(data),
        "missing_item_tables": data["missing_item_tables"],
        "benchmarks": [{"id": name, "name": name.replace("_", " ").title(),
                        "table_count": sum(t["benchmark"] == name for t in data["tables"]),
                        "source_rows": sum(t["row_count"] for t in data["tables"] if t["benchmark"] == name),
                        "sample_max_items": min(SAMPLE_SIZE, sum(t["row_count"] for t in data["tables"] if t["benchmark"] == name))}
                       for name in benchmarks],
    }


def public_job(job: ReviewJob, page: int = 1, *, include_items: bool = True) -> dict:
    counts = job.results.counts
    processed = job.results.processed
    pages = max(1, (processed + RESULTS_PAGE_SIZE - 1) // RESULTS_PAGE_SIZE)
    page = min(page, pages)
    offset = (page - 1) * RESULTS_PAGE_SIZE
    ranked, unranked, failed = [], [], []
    if include_items:
        if offset < job.results.ranked:
            ranked = list(job.results.records("complete", scored=True, offset=offset, limit=RESULTS_PAGE_SIZE))
        unranked = list(job.results.records("complete", scored=False,
                                            offset=max(0, offset - job.results.ranked),
                                            limit=RESULTS_PAGE_SIZE - len(ranked)))
        failed = list(job.results.records("error", offset=max(0, offset - counts["complete"]),
                                          limit=RESULTS_PAGE_SIZE - len(ranked) - len(unranked)))
    return {
        "run_id": job.run_id, "status": job.status, "message": job.message,
        "model": DEFAULT_MODEL, "reasoning_effort": DEFAULT_REASONING_EFFORT,
        "deployment": job.request.deployment.model_dump(),
        "scoring_policy": SCORING_POLICY,
        "scope": {"benchmarks": sorted({t["benchmark"] for t in job.inventory["tables"]}),
                  "table_count": len(job.inventory["tables"]),
                  "source_rows": sum(t["row_count"] for t in job.inventory["tables"]),
                  "branches": job.inventory["branches"], "sample_only": True,
                  "sampling": sampling_policy(), "sample_max_items": sample_upper_bound(job.inventory)},
        "source_rows": job.source_rows, "total": job.total, "processed": processed,
        "sample_complete": job.sample_complete, "prepared_benchmarks": job.prepared_benchmarks,
        "complete": counts["complete"], "errors": counts["error"],
        "ranked": job.results.ranked, "unranked": job.results.unranked,
        "needs_review": job.results.needs_review,
        "usage": dict(job.usage),
        "pagination": {"page": page, "page_size": RESULTS_PAGE_SIZE, "total_pages": pages},
        "ranked_items": ranked, "unranked_items": unranked, "failed_items": failed,
    }


def authorize(run_id: str, secret: str | None) -> ReviewJob:
    sweep()
    job = jobs.get(run_id)
    if job is None or not secret or not secrets.compare_digest(job.secret, secret):
        raise HTTPException(404, "Review not found or expired. Start a new review.")
    return job


@router.post("/runs", status_code=202)
async def start_review(body: ReviewRequest, response: Response,
                       x_openai_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    if not x_openai_key or not x_openai_key.strip():
        raise HTTPException(401, "An OpenAI API key is required.")
    if len(x_openai_key) > 512:
        raise HTTPException(400, "Invalid credential length.")
    if not get_token():
        raise HTTPException(503, "Dataset access is not configured on this server. Please contact the site maintainer or try again later.")
    sweep()
    owner = hashlib.sha256(x_openai_key.strip().encode()).hexdigest()
    active = [job for job in jobs.values() if job.finished_at is None]
    if len(active) >= MAX_ACTIVE or any(job.owner_hash == owner for job in active):
        raise HTTPException(429, "A review is already running for this key, or the demo is busy. Try again shortly.")
    if len(jobs) >= MAX_RETAINED:
        raise HTTPException(429, "The demo is at capacity. Please try again later.")
    job = ReviewJob(secrets.token_hex(16), secrets.token_urlsafe(32), owner, body)
    jobs[job.run_id] = job
    job.task = asyncio.create_task(evaluate(job, x_openai_key.strip()))
    return {"run_id": job.run_id, "run_secret": job.secret}


@router.get("/runs/{run_id}")
async def get_review(run_id: str, response: Response,
               x_review_token: Annotated[str | None, Header()] = None,
               page: Annotated[int, Query(ge=1)] = 1) -> dict:
    response.headers["Cache-Control"] = "no-store"
    return public_job(authorize(run_id, x_review_token), page)


@router.get("/runs/{run_id}/export")
async def export_review(run_id: str, x_review_token: Annotated[str | None, Header()] = None):
    job = authorize(run_id, x_review_token)
    snapshot = public_job(job, include_items=False)
    cutoff = snapshot["processed"]
    for key in ("pagination", "ranked_items", "unranked_items", "failed_items"):
        snapshot.pop(key)
    job.downloads += 1

    async def content():
        try:
            yield json.dumps(snapshot)[:-1]
            for status, key, scored in (("complete", "ranked_items", True),
                                        ("complete", "unranked_items", False), ("error", "failed_items", None)):
                yield f', "{key}": ['
                with closing(job.results.records(status, cutoff=cutoff, scored=scored)) as records:
                    for index, item in enumerate(records):
                        yield ("," if index else "") + json.dumps(item)
                yield "]"
            yield "}"
        finally:
            job.downloads -= 1

    return StreamingResponse(content(), media_type="application/json", headers={
        "Cache-Control": "no-store", "Content-Disposition": f'attachment; filename="item-review-{run_id}.json"',
    })


@router.post("/runs/{run_id}/cancel")
async def cancel_review(run_id: str, response: Response,
                        x_review_token: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    job = authorize(run_id, x_review_token)
    if job.task and not job.task.done():
        job.task.cancel()
        await asyncio.gather(job.task, return_exceptions=True)
        # A task cancelled before its coroutine starts cannot run its finally.
        job.status, job.message = "cancelled", "Review stopped. Completed assessments are retained."
        job.finished_at = time.monotonic()
    return public_job(job)


async def prepare_review(job):
    cancelled = Event()

    def progress(benchmark, completed, rows):
        job.prepared_benchmarks = completed
        job.source_rows = rows
        job.message = f"Preparing sample from {benchmark}. No model calls yet."

    prepare = asyncio.create_task(asyncio.to_thread(
        prepare_samples, job.inventory, db.DEFAULT_DB_PATH.parent / "item-review-samples",
        token=get_token(), progress=progress, cancelled=cancelled,
    ))
    try:
        return await asyncio.shield(prepare)
    except asyncio.CancelledError:
        cancelled.set()
        await asyncio.gather(prepare, return_exceptions=True)
        raise


async def review_items(job):
    paths, total = await prepare_review(job)
    return iter_sample_items(paths), total


async def next_item(items):
    # Wait for an in-flight read before closing its generator on cancellation.
    read = asyncio.create_task(asyncio.to_thread(next, items, None))
    try:
        return await asyncio.shield(read)
    except asyncio.CancelledError:
        await read
        raise


async def assess_items(job: ReviewJob, items, judge) -> None:
    # Share the lazy iterator without overlapping its threaded reads. Reserve
    # hashes before awaiting the judge so duplicate evidence is assessed once,
    # even when its first assessment is still in flight.
    read_lock = asyncio.Lock()
    in_flight: set[str] = set()

    async def worker():
        while True:
            async with read_lock:
                item = await next_item(items)
                if item is None:
                    return
                key = item["evidence_hash"]
                for source in item["sources"]:
                    job.results.add_source(key, source)
                if key in in_flight or job.results.contains(key):
                    continue
                in_flight.add(key)
            try:
                assessment = await judge(item["evidence"])
                # Never retain raw model output or provider exception text.
                result = {"evidence_hash": key, "evidence": item["evidence"], **{
                    field: assessment[field] for field in (
                        "status", "assessment", "overall_score", "response_model", "response_id",
                        "compatibility_score", "scored_dimensions", "needs_review",
                    ) if field in assessment}}
                if assessment["status"] == "error":
                    result["error"] = "The model did not return a complete, valid assessment."
                job.results.append(result)
                usage = assessment.get("usage") or {}
                for field in ("input_tokens", "output_tokens"):
                    job.usage[field] += usage.get(field, 0)
                job.usage["reasoning_tokens"] += (usage.get("output_tokens_details") or {}).get("reasoning_tokens", 0)
                job.usage["cached_input_tokens"] += (usage.get("input_tokens_details") or {}).get("cached_tokens", 0)
            finally:
                in_flight.remove(key)

    workers = [asyncio.create_task(worker()) for _ in range(REVIEW_CONCURRENCY)]
    try:
        await asyncio.gather(*workers)
    finally:
        # gather propagates the original provider error, but does not cancel
        # siblings itself. Drain every worker before closing the client/iterator.
        for task in workers:
            if not task.done():
                task.cancel()
        await asyncio.gather(*workers, return_exceptions=True)


async def evaluate(job: ReviewJob, api_key: str) -> None:
    items = None
    try:
        items, job.total = await review_items(job)
        job.status, job.message = "running", "Assessing the selected sample."
        async with AsyncOpenAI(api_key=api_key, base_url="https://api.openai.com/v1",
                               max_retries=2, timeout=600) as client:
            judge = AsyncJudge(client, job.request.deployment.describe(), PROMPT_PATH.read_text(encoding="utf-8"))
            await assess_items(job, items, judge)
        job.sample_complete = True
        job.status = "completed"
        job.message = "The selected sample has been assessed."
    except asyncio.CancelledError:
        job.status, job.message = "cancelled", "Review stopped. Completed assessments are retained."
    except AuthenticationError:
        job.status, job.message = "failed", "OpenAI rejected the API key. Check its access and start a new review."
    except RateLimitError:
        job.status, job.message = "failed", "OpenAI reported a rate or quota limit. Completed assessments are retained."
    except OpenAIError:
        job.status, job.message = "failed", "The OpenAI request failed. Check model access and try again."
    except Exception:
        job.status = "failed"
        job.message = "Could not load or process evaluation items. Please try again later or contact the site maintainer."
    finally:
        if hasattr(items, "close"):
            items.close()
        api_key = ""
        job.finished_at = time.monotonic()
