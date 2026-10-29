"""Goal-conditioned pipeline with private durable checkpoints.

API keys remain in memory. Run secrets protect polling, downloads, and
continuation. The separate legacy sample-review mode still uses temporary data.
"""

from __future__ import annotations

import asyncio
from collections import Counter
from contextlib import closing
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
import errno
import hashlib
import json
import logging
import os
from pathlib import Path
import secrets
import time
from threading import Event, Lock
from typing import Annotated, Literal

from fastapi import APIRouter, Header, HTTPException, Query, Response
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.concurrency import iterate_in_threadpool, run_in_threadpool
from huggingface_hub import get_token
from openai import AsyncOpenAI, AuthenticationError, RateLimitError, OpenAIError
from pydantic import BaseModel, ConfigDict, Field, field_validator

from bayesian_auditing.sampling import (
    SAMPLE_SIZE, iter_sample_items, prepare_samples, sample_upper_bound, sampling_policy,
)
from bayesian_auditing.scoring import SCORING_POLICY
from bayesian_auditing.data import fingerprint
from bayesian_auditing.benchmark_data import iter_benchmark_items, row_fingerprint
from bayesian_auditing.benchmark_index import DEFAULT_MINIMUM_FREE_BYTES, prepare_benchmark_index
from bayesian_auditing.benchmark_rows import fetch_benchmark_rows
from bayesian_auditing.benchmark_queries import build_benchmark_queries, build_screening_queues
from bayesian_auditing.retrieval import ItemIndex, RETRIEVAL_POLICY
from bayesian_auditing.judge import (
    AsyncJudge, DEFAULT_MODEL, DEFAULT_REASONING_EFFORT, DEFAULT_MAX_OUTPUT_TOKENS, PROMPT_PATH,
)
from bayesian_auditing.requirements import AsyncRequirementExtractor, EXTRACTION_VERSION, Requirements
from bayesian_auditing.onet import OnetIndex, DEFAULT_MATERIALS_DIR
from bayesian_auditing.onet_mapping import AsyncOnetMapper, OnetMapping, MAPPING_VERSION, build_onet_query
from bayesian_auditing.screening import (
    AsyncItemScreener, ScreeningAssessment, SCREENING_VERSION, GATED_DIMENSIONS,
)
from bayesian_auditing.screening_queue import allocate_initial_screening, INITIAL_SCREENING_BUDGET
from bayesian_auditing.selection import select_collection, SelectionIncomplete
from bayesian_auditing.screening_budget import AdaptiveSettings
from . import adaptive_review
from . import review_exports
from .item_review_store import ReviewStore
from .result_package import build_results_package, package_filename
from .remote_retrieval import RemoteRetrieval, RemoteRetrievalError
from .review_checkpoints import AccessDenied, CheckpointError, Checkpoints
from .candidate_store import CandidateStore, CandidateStoreError
from . import streaming_json
from . import db

router = APIRouter(prefix="/api/item-review", tags=["Item review"])
INVENTORY_PATH = Path(__file__).with_name("item_review_inventory.json")
MAX_ACTIVE = 3
MAX_RETAINED = 30
MAX_CACHED_PIPELINE = 1
RETENTION_SECONDS = 3600
PIPELINE_MODES = {"requirements", "grounding", "retrieval", "screening", "selection", "adaptive"}
logger = logging.getLogger(__name__)
RESULTS_PAGE_SIZE = 20
DEFAULT_RETRIEVE_K = 20
MAX_RETRIEVE_K = 100
REVIEW_CONCURRENCY = int(os.environ.get("ITEM_REVIEW_CONCURRENCY", "4"))
if not 1 <= REVIEW_CONCURRENCY <= 16:
    raise ValueError("ITEM_REVIEW_CONCURRENCY must be between 1 and 16")


def inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


class Deployment(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    task: str
    users: str
    inputs: str
    outputs: str
    success: str
    constraints: str = ""

    @field_validator("task", "users", "inputs", "outputs", "success")
    @classmethod
    def require_answer(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("An answer is required")
        # Preserve submitted text for review and export.
        return value

    def describe(self) -> str:
        labels = {"task": "Task and setting", "users": "Users, language, and location",
                  "inputs": "Expected inputs and interaction", "outputs": "Expected outputs",
                  "success": "Success criteria", "constraints": "Constraints and failures to check"}
        return "\n\n".join(f"{labels[key]}:\n{value if value.strip() else 'Unspecified'}" for key, value in self.model_dump().items())


class ReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    deployment: Deployment
    run_name: str = ""
    mode: Literal["item_review", "requirements", "grounding", "retrieval", "screening", "selection", "adaptive"] = "item_review"
    retrieve_k: int = Field(default=DEFAULT_RETRIEVE_K, ge=1, le=MAX_RETRIEVE_K, strict=True)
    retrieval_query: str = Field(default="", max_length=100_000)

    def query(self) -> str:
        return self.retrieval_query if self.retrieval_query.strip() else self.deployment.describe()


class BenchmarkRetrievalRequest(BaseModel):
    """Step 4 always searches the complete pinned main inventory."""
    model_config = ConfigDict(extra="forbid", strict=True)


class ScreeningRequest(BaseModel):
    """The initial budget is fixed; continuations reuse the same allocation."""
    model_config = ConfigDict(extra="forbid", strict=True)


class SelectionRequest(BaseModel):
    """Collection construction uses the agreed total limit of 30 items."""
    model_config = ConfigDict(extra="forbid", strict=True)


@dataclass
class ReviewJob:
    run_id: str
    secret: str = field(repr=False)
    owner_hash: str = field(repr=False)
    request: ReviewRequest = field(repr=False)
    inventory: dict = field(default_factory=lambda: inventory(), repr=False)
    created_at: float = field(default_factory=time.monotonic)
    finished_at: float | None = None
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    finished_at_utc: str | None = None
    usage_history: list[dict] = field(default_factory=list, repr=False)
    task: asyncio.Task | None = field(default=None, repr=False)
    status: str = "preparing"
    message: str = "Preparing the fixed sample for local retrieval. No paid calls yet."
    source_rows: int = 0
    total: int = 0
    indexed_items: int = 0
    contentless_items: int = 0
    retrieved_items: int = 0
    sample_complete: bool = False
    prepared_benchmarks: int = 0
    downloads: int = 0
    results: ReviewStore | None = field(default=None, repr=False)
    usage: Counter = field(default_factory=Counter)
    requirements: dict | None = field(default=None, repr=False)
    extraction: dict | None = field(default=None, repr=False)
    source_run_id: str | None = None
    grounding: dict | None = field(default=None, repr=False)
    benchmark_retrieval: dict | None = field(default=None, repr=False)
    screening: dict | None = field(default=None, repr=False)
    selection: dict | None = field(default=None, repr=False)
    selection_run_id: str | None = None
    adaptive: dict | None = field(default=None, repr=False)
    _checkpoint_saved: bool = field(default=False, repr=False)
    _checkpoint_retrieval: dict | None = field(default=None, repr=False)
    _checkpoint_retrieval_ref: str | None = field(default=None, repr=False)
    package: review_exports.PreparedPackage = field(default_factory=review_exports.PreparedPackage, repr=False)

    def __post_init__(self):
        if self.request.mode == "item_review" and self.results is None:
            self.results = ReviewStore()


jobs: dict[str, ReviewJob] = {}
# Only dataset evidence/vectors are reusable. Deployment queries, keys,
# and judgments stay with their private job. Serialize local model inference to
# avoid allocating one model or inference batch per concurrent visitor.
_retrieval_lock = Lock()
_cached_index: tuple[str, ItemIndex] | None = None
_cached_onet_index: tuple[Path, OnetIndex] | None = None


def sweep() -> None:
    now = time.monotonic()
    for run_id, job in list(jobs.items()):
        if (job.request.mode == "item_review" and job.finished_at is not None
                and not job.downloads and now - job.finished_at > RETENTION_SECONDS):
            jobs.pop(run_id, None)
            job.results.close()
    trim_pipeline_cache()


# Explicitly exclude API clients/tasks, access tokens, temporary sample results,
# and process-relative monotonic clocks from the durable record.
_CHECKPOINT_FIELDS = (
    "run_id", "owner_hash", "inventory", "created_at_utc", "finished_at_utc",
    "usage_history", "status", "message", "requirements", "extraction",
    "source_run_id", "grounding", "screening", "selection", "selection_run_id", "adaptive",
)


def checkpoints() -> Checkpoints:
    return Checkpoints(db.DEFAULT_DB_PATH.parent / "review-runs")


def candidate_store() -> CandidateStore:
    return CandidateStore(checkpoints().directory / "candidates")


def expand_candidate(record: dict) -> dict:
    return candidate_store().expand(record)


def screened_records(job):
    """Supply the solver one complete assessment and original row at a time."""
    store = candidate_store()
    for record in job.screening["items"]:
        yield store.expand(record)


def _expand_output(path, record):
    # Original rows have arbitrary column names; only pipeline record positions
    # may contain our private references. Never interpret nested evidence keys.
    if ((len(path) == 5 and path[:2] == ("retrieval", "rankings")
         and type(path[2]) is int and path[3] == "candidates" and type(path[4]) is int)
            or (len(path) == 3 and path[:2] == ("screening", "items") and type(path[2]) is int)
            or (len(path) == 2 and path[0] == "items" and type(path[1]) is int)):
        return expand_candidate(record)
    return record


def _json_chunks(snapshot):
    """Expand private references into bounded chunks of the unchanged API JSON."""
    pending, length = [], 0
    for chunk in streaming_json.iterencode(snapshot, expand=_expand_output):
        pending.append(chunk)
        length += len(chunk)
        if length >= 64 * 1024:
            yield "".join(pending)
            pending, length = [], 0
    if pending:
        yield "".join(pending)


def checkpoint(job: ReviewJob) -> None:
    if job.request.mode not in PIPELINE_MODES:
        return
    state = {name: getattr(job, name) for name in _CHECKPOINT_FIELDS}
    state.update(request=job.request.model_dump(), usage=dict(job.usage),
                 finished=job.finished_at is not None)
    reference = (job._checkpoint_retrieval_ref
                 if job._checkpoint_retrieval is job.benchmark_retrieval else None)
    try:
        reference = checkpoints().save(job.run_id, job.secret, state,
                                       retrieval=job.benchmark_retrieval, retrieval_ref=reference)
    except CheckpointError:
        job._checkpoint_saved = False
        raise
    job._checkpoint_retrieval = job.benchmark_retrieval
    job._checkpoint_retrieval_ref = reference
    job._checkpoint_saved = True


def restore_review(run_id: str, secret: str) -> ReviewJob:
    state, reference = checkpoints().load(run_id, secret)
    try:
        request = ReviewRequest.model_validate(state["request"])
        if request.mode not in PIPELINE_MODES:
            raise ValueError("Not a saved pipeline run")
        job = ReviewJob(secret=secret, request=request,
                        **{name: state[name] for name in _CHECKPOINT_FIELDS})
        job.usage = Counter(state["usage"])
        job.benchmark_retrieval = state["benchmark_retrieval"]
        job._checkpoint_retrieval = job.benchmark_retrieval
        job._checkpoint_retrieval_ref = reference
        job._checkpoint_saved = True
        job.finished_at = time.monotonic()
        if not state["finished"]:
            job.status = "cancelled"
            job.message = ("This stage was interrupted by a server restart. Saved results are retained. "
                           "Review them before continuing or retrying unfinished work.")
            job.finished_at_utc = datetime.now(timezone.utc).isoformat()
            if job.adaptive:
                for attempt in job.adaptive["attempts"]:
                    if attempt["status"] == "pending":
                        attempt["status"] = "unknown"
                # Unknown calls retain their reservations and are not replayed.
                if job.adaptive["frozen"]:
                    job.status = "completed"
                    job.message = "The frozen collection was restored from its last saved checkpoint. Review the selected items and remaining coverage gaps."
            checkpoint(job)
        return job
    except (ValueError, TypeError, KeyError) as exc:
        raise CheckpointError("Could not restore the review checkpoint.") from exc


def trim_pipeline_cache(*, keep: str | None = None, limit: int = MAX_CACHED_PIPELINE) -> None:
    """Large candidate rankings should not accumulate in finished ancestors."""
    completed = [job for job in jobs.values()
                 if job.finished_at is not None and not job.downloads
                 and not job.package.pinned() and job._checkpoint_saved]
    excess = len(completed) - limit
    for job in completed:
        if excess <= 0:
            break
        if job.run_id != keep:
            job.package.close()
            jobs.pop(job.run_id, None)
            excess -= 1


def make_cache_room() -> None:
    """Keep the in-memory cache bounded without deleting saved pipeline runs."""
    for run_id, job in list(jobs.items()):
        if len(jobs) < MAX_RETAINED:
            break
        if (job.finished_at is not None and not job.downloads
                and not job.package.pinned() and job._checkpoint_saved):
            job.package.close()
            jobs.pop(run_id)


def launch_review(job: ReviewJob, api_key: str, *, source: ReviewJob | None = None) -> dict:
    """Save before starting work, so storage failures cannot start paid calls."""
    if (source is not None and job.benchmark_retrieval is not None
            and source._checkpoint_retrieval is source.benchmark_retrieval):
        # Continuations copy immutable rankings; share their existing disk blob.
        job._checkpoint_retrieval = job.benchmark_retrieval
        job._checkpoint_retrieval_ref = source._checkpoint_retrieval_ref
    try:
        checkpoint(job)
    except CheckpointError:
        logger.error("Review checkpoint save failed before launch run_id=%r", job.run_id)
        raise HTTPException(503, "The server could not save this review. No work was started. Please try again or contact the site maintainer.") from None
    if job.request.mode in PIPELINE_MODES:
        trim_pipeline_cache(limit=0)
    jobs[job.run_id] = job
    job.task = asyncio.create_task(evaluate(job, api_key))
    return {"run_id": job.run_id, "run_secret": job.secret}


async def shutdown() -> None:
    global _cached_index, _cached_onet_index
    tasks = [task for job in jobs.values() for task in (job.task, job.package.task)
             if task is not None and not task.done()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    # A bounded archive read may still be executing after its request was
    # cancelled. Finish it before closing a shared temporary handle.
    await asyncio.gather(*(finish_worker(job.package.read_task) for job in jobs.values()
                           if job.package.read_task is not None))
    for job in jobs.values():
        job.package.close()
        try:
            checkpoint(job)
        except CheckpointError:
            logger.error("Review checkpoint save failed during shutdown run_id=%r", job.run_id)
        if job.results is not None:
            job.results.close()
    jobs.clear()
    _cached_index = None
    _cached_onet_index = None


@router.get("/catalog")
async def catalog(response: Response) -> dict:
    response.headers["Cache-Control"] = "no-store"
    data = inventory()
    benchmarks = sorted({table["benchmark"] for table in data["tables"]})
    return {
        "model": DEFAULT_MODEL, "reasoning_effort": DEFAULT_REASONING_EFFORT,
        "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS,
        "scoring_policy": SCORING_POLICY,
        "retrieval_policy": RETRIEVAL_POLICY,
        "default_retrieve_k": DEFAULT_RETRIEVE_K, "max_retrieve_k": MAX_RETRIEVE_K,
        "branches": data["branches"], "dataset_access_configured": bool(get_token()),
        "retrieval_mode": "remote" if os.environ.get("ITEM_REVIEW_RETRIEVAL_URL") or os.environ.get("ITEM_REVIEW_RETRIEVAL_TOKEN") else "local",
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


def usage_record(job: ReviewJob) -> dict:
    """One run's new calls, without counting retained assessments again."""
    return {"run_id": job.run_id, "mode": job.request.mode, "status": job.status,
            "created_at": job.created_at_utc, "finished_at": job.finished_at_utc,
            "usage": dict(job.usage)}


def continued_usage(source: ReviewJob) -> list[dict]:
    return deepcopy([*source.usage_history, usage_record(source)])


def result_metadata(job: ReviewJob) -> dict:
    state = "partial"
    if job.status == "completed":
        state = "frozen" if job.adaptive and job.adaptive.get("frozen") else "stage_complete"
    return {"export_version": 1, "run_name": job.request.run_name,
            "created_at": job.created_at_utc, "finished_at": job.finished_at_utc,
            "result_state": state, "usage_scope": "current_run"}


def public_job(job: ReviewJob, page: int = 1, *, include_items: bool = True) -> dict:
    if job.request.mode in {"requirements", "grounding", "retrieval", "screening", "selection", "adaptive"}:
        result = {
            "run_id": job.run_id, "status": job.status, "message": job.message,
            "mode": job.request.mode, "model": DEFAULT_MODEL,
            "reasoning_effort": DEFAULT_REASONING_EFFORT,
            "deployment": job.request.deployment.model_dump(),
            "requirements": job.requirements, "extraction": job.extraction,
            "usage": dict(job.usage),
            "metadata": result_metadata(job),
            "stage_usage": [*deepcopy(job.usage_history), usage_record(job)],
        }
        if job.request.mode in {"grounding", "retrieval", "screening", "selection", "adaptive"}:
            result.update(source_run_id=job.source_run_id, grounding=job.grounding)
        if job.request.mode in {"retrieval", "screening", "selection", "adaptive"}:
            retrieval = job.benchmark_retrieval
            result["retrieval"] = None
            if retrieval is not None:
                result["retrieval"] = {
                    **{key: retrieval[key] for key in ("policy", "scope", "stats", "queries")},
                    "queues": [{"queue_id": queue["queue_id"], "facet_id": queue["facet_id"],
                                "source": queue["source"], "item_count": len(queue["item_ids"])}
                               for queue in retrieval["queues"]],
                }
        if job.request.mode in {"screening", "selection", "adaptive"}:
            result["screening"] = job.screening
            if job.screening:
                result["model"] = job.screening["model"]["model"]
                result["reasoning_effort"] = job.screening["model"]["reasoning_effort"]
        if job.request.mode == "selection" or job.selection is not None:
            result.update(selection=job.selection, selection_run_id=job.selection_run_id)
        if job.request.mode in {"selection", "adaptive"}:
            screening = job.screening
            items = screening["items"]
            allocated = len(adaptive_review.acquisitions(screening, job.adaptive))
            result["selection_input"] = {
                "allocated": allocated,
                "screened": sum(item["status"] == "complete" for item in items),
                "errors": sum(item["status"] == "error" for item in items),
                "pending": allocated - len(items),
            }
        if job.request.mode == "adaptive":
            result["adaptive"] = job.adaptive
        return result
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
        "mode": "item_review",
        "model": DEFAULT_MODEL, "reasoning_effort": DEFAULT_REASONING_EFFORT,
        "deployment": job.request.deployment.model_dump(),
        "scoring_policy": SCORING_POLICY,
        "retrieval_policy": RETRIEVAL_POLICY, "retrieval_query": job.request.query(),
        "indexed_items": job.indexed_items, "retrieved_items": job.retrieved_items,
        "contentless_items": job.contentless_items,
        "scope": {"benchmarks": sorted({t["benchmark"] for t in job.inventory["tables"]}),
                  "table_count": len(job.inventory["tables"]),
                  "source_rows": sum(t["row_count"] for t in job.inventory["tables"]),
                  "branches": job.inventory["branches"], "sample_only": True,
                  "sampling": sampling_policy(), "sample_max_items": sample_upper_bound(job.inventory),
                  "retrieve_k": job.request.retrieve_k},
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
    failure = "Review unavailable. Return to the browser where you started it, or start a new review."
    if not secret:
        logger.warning("Review access denied run_id=%r reason=missing_token", run_id)
        raise HTTPException(404, failure)
    job = jobs.get(run_id)
    if job is None:
        try:
            job = restore_review(run_id, secret)
        except AccessDenied as exc:
            logger.warning("Review access denied run_id=%r reason=%s", run_id, exc.reason)
            raise HTTPException(404, failure) from None
        except CheckpointError:
            logger.error("Review checkpoint restore failed run_id=%r", run_id)
            raise HTTPException(503, "The server could not open the saved review. Please try again or contact the site maintainer.") from None
        make_cache_room()
        if len(jobs) < MAX_RETAINED:
            jobs[run_id] = job
            trim_pipeline_cache(keep=run_id)
    elif not secrets.compare_digest(job.secret, secret):
        logger.warning("Review access denied run_id=%r reason=invalid_token", run_id)
        raise HTTPException(404, failure)
    return job


def check_run_capacity(api_key: str | None) -> tuple[str, str]:
    """Apply the same credential and capacity checks to every paid run."""
    if not api_key or not api_key.strip():
        raise HTTPException(401, "An OpenAI API key is required.")
    if len(api_key) > 512:
        raise HTTPException(400, "Invalid credential length.")
    key = api_key.strip()
    owner = hashlib.sha256(key.encode()).hexdigest()
    check_owner_capacity(owner)
    return key, owner


def check_owner_capacity(owner: str) -> None:
    """Continuations inherit their source owner, including local-only runs."""
    sweep()
    active = [job for job in jobs.values() if job.finished_at is None]
    if len(active) >= MAX_ACTIVE or any(job.owner_hash == owner for job in active):
        raise HTTPException(429, "A review is already running for this key, or the demo is busy. Try again shortly.")
    make_cache_room()
    if len(jobs) >= MAX_RETAINED:
        raise HTTPException(429, "The demo is at capacity. Please try again later.")


@router.post("/runs", status_code=202)
async def start_review(body: ReviewRequest, response: Response,
                       x_openai_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    if body.mode in {"grounding", "retrieval", "screening", "selection", "adaptive"}:
        raise HTTPException(400, "Continue grounding, retrieval, screening, or selection from its preceding pipeline run.")
    key, owner = check_run_capacity(x_openai_key)
    if body.mode == "item_review" and not get_token():
        raise HTTPException(503, "Dataset access is not configured on this server. Please contact the site maintainer or try again later.")
    job = ReviewJob(secrets.token_hex(16), secrets.token_urlsafe(32), owner, body,
                    inventory=inventory() if body.mode == "item_review" else {})
    if body.mode == "requirements":
        job.message = "Preparing to extract requirements from your six answers."
    return launch_review(job, key)


@router.post("/runs/{run_id}/ground", status_code=202)
async def start_grounding(run_id: str, response: Response,
                         x_review_token: Annotated[str | None, Header()] = None,
                         x_openai_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    source = authorize(run_id, x_review_token)
    if (source.request.mode not in {"requirements", "grounding"} or source.finished_at is None
            or not source.requirements):
        raise HTTPException(409, "Finish a valid requirements extraction before grounding with O*NET.")
    if not source.requirements["task_facets"]:
        raise HTTPException(409, "No task facets were extracted. Clarify your deployment and extract requirements again.")
    key, owner = check_run_capacity(x_openai_key)
    # Copy the accepted extraction; a grounding run never repeats Step 2 or
    # rewrites its source run, even when the user retries a stopped mapping.
    request = ReviewRequest(deployment=source.request.deployment, mode="grounding", run_name=source.request.run_name)
    job = ReviewJob(secrets.token_hex(16), secrets.token_urlsafe(32), owner, request, inventory={},
                    requirements=deepcopy(source.requirements), extraction=deepcopy(source.extraction),
                    source_run_id=source.run_id, usage_history=continued_usage(source),
                    message="Preparing O*NET search for your extracted tasks.")
    return launch_review(job, key, source=source)


@router.post("/runs/{run_id}/retrieve", status_code=202)
async def start_benchmark_retrieval(run_id: str, body: BenchmarkRetrievalRequest, response: Response,
                                   x_review_token: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    source = authorize(run_id, x_review_token)
    if (source.request.mode not in {"grounding", "retrieval"} or source.finished_at is None
            or (source.request.mode == "grounding" and source.status != "completed")
            or not source.requirements or not source.grounding):
        raise HTTPException(409, "Complete O*NET grounding before retrieving benchmark items.")
    try:
        requirements = Requirements.model_validate(source.requirements)
        queries = build_benchmark_queries(source.request.deployment.model_dump(), requirements, source.grounding)
        if not queries:
            raise ValueError("No extracted tasks")
    except (ValueError, TypeError, KeyError):
        raise HTTPException(409, "Complete valid O*NET mappings for every extracted task before retrieval.") from None
    data = inventory()
    if (set(data["branches"]) != {"main"} or not data["tables"]
            or any(table["branch"] != "main" or table["commit"] != data["branches"]["main"]
                   for table in data["tables"])):
        raise HTTPException(503, "The benchmark inventory must use one pinned main revision. Refresh the server catalog.")
    if not get_token():
        raise HTTPException(503, "Dataset access is not configured on this server. Please contact the site maintainer or try again later.")
    check_owner_capacity(source.owner_hash)
    job = ReviewJob(
        secrets.token_hex(16), secrets.token_urlsafe(32), source.owner_hash,
        ReviewRequest(deployment=source.request.deployment, mode="retrieval", run_name=source.request.run_name), inventory=data,
        usage_history=continued_usage(source),
        requirements=deepcopy(source.requirements), extraction=deepcopy(source.extraction),
        grounding=deepcopy(source.grounding), source_run_id=source.run_id,
        message="Preparing to search all benchmark collections from the pinned main revision.",
        benchmark_retrieval={
            "policy": None, "stats": {}, "queries": queries, "queues": [], "rankings": [],
            "inventory": deepcopy(data),
            "scope": {"repo": data["repo"], "branches": data["branches"],
                      "benchmarks": sorted({table["benchmark"] for table in data["tables"]}),
                      "table_count": len(data["tables"]),
                      "source_rows": sum(table["row_count"] for table in data["tables"]),
                      "sample_only": False, "release_filter": None},
        },
    )
    return launch_review(job, "", source=source)


def screening_candidates(retrieval: dict, requirements: Requirements) -> dict[tuple[str, str], dict]:
    """Check the saved queues and full-row identities before opening a paid client."""
    rankings = retrieval["rankings"]
    facet_ids = [facet.facet_id for facet in requirements.task_facets]
    if not facet_ids or [ranking["facet_id"] for ranking in rankings] != facet_ids:
        raise ValueError("Every extracted task needs a completed ranking.")
    if retrieval["queues"] != build_screening_queues(rankings):
        raise ValueError("Saved queues do not match the candidate rankings.")
    candidates = {}
    for ranking in rankings:
        for candidate in ranking["candidates"]:
            item_id = candidate["item_id"]
            original = expand_candidate(candidate)
            if (item_id != row_fingerprint(original["evidence"]["item"])
                    or candidate["evidence_hash"] != item_id):
                raise ValueError("A candidate does not retain its original row identity.")
            candidates[ranking["facet_id"], item_id] = candidate
    return candidates


@router.post("/runs/{run_id}/screen", status_code=202)
async def start_screening(run_id: str, response: Response,
                          body: ScreeningRequest = ScreeningRequest(),
                          x_review_token: Annotated[str | None, Header()] = None,
                          x_openai_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    source = authorize(run_id, x_review_token)
    if (source.request.mode not in {"retrieval", "screening", "selection"} or source.finished_at is None
            or (source.request.mode == "retrieval" and source.status != "completed")
            or not source.requirements or not source.grounding or not source.benchmark_retrieval):
        raise HTTPException(409, "Complete benchmark retrieval before screening its candidates.")
    try:
        requirements = Requirements.model_validate(source.requirements)
        build_benchmark_queries(source.request.deployment.model_dump(), requirements, source.grounding)
        screening_candidates(source.benchmark_retrieval, requirements)
        allocation = allocate_initial_screening(source.benchmark_retrieval["queues"])
    except CandidateStoreError:
        raise HTTPException(503, "Saved candidate evidence could not be read. Contact the site maintainer before continuing.") from None
    except (ValueError, TypeError, KeyError):
        raise HTTPException(409, "Screening requires valid requirements, grounding, and complete candidate queues.") from None

    # A continuation finishes the same initial set, without paying again for
    # successful assessments (including valid fail and unresolved gate outcomes).
    retained = []
    if source.request.mode in {"screening", "selection"}:
        if not source.screening or source.screening["allocation"] != allocation:
            raise HTTPException(409, "The saved screening allocation cannot be continued.")
        if (source.screening["policy"]["version"] != SCREENING_VERSION
                or source.screening["model"]["output_schema"] != ScreeningAssessment.model_json_schema()):
            raise HTTPException(409, "The saved screening schema has changed. Start screening from the retrieval run.")
        retained = [deepcopy(item) for item in source.screening["items"] if item["status"] == "complete"]
        if len(retained) == allocation["allocated"]:
            raise HTTPException(409, "Every allocated item already has a valid screening result.")
    key, owner = check_run_capacity(x_openai_key)
    screener = AsyncItemScreener(None)
    job = ReviewJob(
        secrets.token_hex(16), secrets.token_urlsafe(32), owner,
        ReviewRequest(deployment=source.request.deployment, mode="screening", run_name=source.request.run_name),
        usage_history=continued_usage(source),
        inventory=deepcopy(source.inventory), source_run_id=source.run_id,
        requirements=deepcopy(source.requirements), extraction=deepcopy(source.extraction),
        grounding=deepcopy(source.grounding), benchmark_retrieval=deepcopy(source.benchmark_retrieval),
        selection=deepcopy(source.selection), selection_run_id=source.selection_run_id,
        message="Preparing the initial candidates for screening with GPT-6 Luna.",
        screening={
            "policy": {
                "version": SCREENING_VERSION, "initial_budget": INITIAL_SCREENING_BUDGET,
                "initial_allocation": "round_robin_all_source_queues",
                "allocation_order": "saved_task_order", "exhausted_queue_share": "redistributed",
                "gated_dimensions": list(GATED_DIMENSIONS), "minimum_score": 3,
                "task_match": "actual_requested_decision_matches_an_extracted_task",
                "unknown_gate": "unresolved_unless_another_gate_definitely_fails",
                "reported_only_dimensions": ["output_content", "output_form"],
            },
            "model": {
                "version": SCREENING_VERSION, "model": screener.model,
                "reasoning_effort": screener.reasoning_effort,
                "max_output_tokens": screener.max_output_tokens,
                "prompt": screener.prompt, "output_schema": ScreeningAssessment.model_json_schema(),
            },
            "allocation": allocation, "items": retained,
        },
    )
    if source.request.mode in {"screening", "selection"}:
        # Continue with the exact prompt/settings used for retained assessments,
        # even if the prompt file has been edited since the first attempt.
        job.screening["model"] = deepcopy(source.screening["model"])
        job.screening["policy"] = deepcopy(source.screening["policy"])
    return launch_review(job, key, source=source)


def validate_selection_source(source: ReviewJob) -> Requirements:
    """Check the saved screening against its original allocation and evidence."""
    requirements = Requirements.model_validate(source.requirements)
    build_benchmark_queries(source.request.deployment.model_dump(), requirements, source.grounding)
    candidates = screening_candidates(source.benchmark_retrieval, requirements)
    screening = source.screening
    if (screening["policy"]["version"] != SCREENING_VERSION
            or screening["model"]["output_schema"] != ScreeningAssessment.model_json_schema()
            or screening["allocation"] != allocate_initial_screening(source.benchmark_retrieval["queues"])):
        raise ValueError("The saved screening contract has changed.")
    acquisition_list = adaptive_review.acquisitions(screening, source.adaptive)
    allocated = {item["item_id"]: item for item in acquisition_list}
    if len(allocated) != len(acquisition_list):
        raise ValueError("A candidate may be acquired only once.")
    seen = set()
    for item in screening["items"]:
        item_id = item["item_id"]
        if item_id in seen or item_id not in allocated or item["status"] not in {"complete", "error"}:
            raise ValueError("Screening results do not match the original allocation.")
        seen.add(item_id)
        original = expand_candidate(candidates[allocated[item_id]["facet_id"], item_id])
        item = expand_candidate(item)
        if (item["evidence"] != original["evidence"] or item["evidence_hash"] != item_id
                or item["sources"] != original["sources"]
                or item["acquisition"] != {key: allocated[item_id][key] for key in ("queue_id", "facet_id")}):
            raise ValueError("Screening must retain original item evidence and sources.")
        if item["status"] == "complete":
            assessment = ScreeningAssessment.model_validate(item["assessment"])
            assessment.validate_context(requirements)
    return requirements


@router.post("/runs/{run_id}/select", status_code=202)
async def start_selection(run_id: str, response: Response,
                           body: SelectionRequest = SelectionRequest(),
                           x_review_token: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    source = authorize(run_id, x_review_token)
    if (source.request.mode not in {"screening", "selection"} or source.finished_at is None
            or not source.screening or not source.requirements or not source.grounding
            or not source.benchmark_retrieval):
        raise HTTPException(409, "Finish or stop screening before selecting from its saved results.")
    try:
        validate_selection_source(source)
    except CandidateStoreError:
        raise HTTPException(503, "Saved candidate evidence could not be read. Contact the site maintainer before continuing.") from None
    except (ValueError, KeyError, TypeError):
        raise HTTPException(409, "Selection requires valid saved screening results and original item evidence.") from None
    check_owner_capacity(source.owner_hash)
    job = ReviewJob(
        secrets.token_hex(16), secrets.token_urlsafe(32), source.owner_hash,
        ReviewRequest(deployment=source.request.deployment, mode="selection", run_name=source.request.run_name),
        usage_history=continued_usage(source),
        inventory=deepcopy(source.inventory), source_run_id=source.run_id,
        requirements=deepcopy(source.requirements), extraction=deepcopy(source.extraction),
        grounding=deepcopy(source.grounding), benchmark_retrieval=deepcopy(source.benchmark_retrieval),
        screening=deepcopy(source.screening), selection=deepcopy(source.selection),
        selection_run_id=source.selection_run_id,
        message="Selecting up to 30 total items using saved ratings and coverage requirements.",
    )
    return launch_review(job, "", source=source)


@router.post("/runs/{run_id}/adapt", status_code=202)
async def start_adaptive_screening(run_id: str, response: Response,
                                   body: AdaptiveSettings = AdaptiveSettings(),
                                   x_review_token: Annotated[str | None, Header()] = None,
                                   x_openai_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    source = authorize(run_id, x_review_token)
    if (source.request.mode not in {"selection", "adaptive"} or source.finished_at is None
            or not source.selection or not source.screening or not source.requirements
            or not source.grounding or not source.benchmark_retrieval):
        raise HTTPException(409, "Finish initial screening and select a collection before adaptive screening.")
    try:
        validate_selection_source(source)
        if source.request.mode == "adaptive":
            adaptive_review.validate_history(source)
            if source.adaptive["frozen"]:
                raise ValueError("This collection has already been frozen.")
            if any(getattr(body, key) != source.adaptive["settings"][key] for key in body.model_fields_set):
                raise ValueError("Continue with the original adaptive settings.")
            state = deepcopy(source.adaptive)
        else:
            if source.status != "completed":
                raise ValueError("Complete initial collection selection first.")
            state = adaptive_review.initialize(source, body)
    except CandidateStoreError:
        raise HTTPException(503, "Saved candidate evidence could not be read. Contact the site maintainer before continuing.") from None
    except (ValueError, TypeError, KeyError):
        raise HTTPException(409, "Adaptive screening requires a valid selected collection and complete initial assessments. Resume only unfinished adaptive runs with their original settings.") from None
    key, _ = check_run_capacity(x_openai_key)
    check_owner_capacity(source.owner_hash)
    job = ReviewJob(
        secrets.token_hex(16), secrets.token_urlsafe(32), source.owner_hash,
        ReviewRequest(deployment=source.request.deployment, mode="adaptive", run_name=source.request.run_name),
        usage_history=continued_usage(source),
        inventory=deepcopy(source.inventory), source_run_id=source.run_id,
        requirements=deepcopy(source.requirements), extraction=deepcopy(source.extraction),
        grounding=deepcopy(source.grounding), benchmark_retrieval=deepcopy(source.benchmark_retrieval),
        screening=deepcopy(source.screening), selection=deepcopy(source.selection),
        selection_run_id=source.selection_run_id, adaptive=state,
        message="Preparing adaptive screening from saved queues and the selected collection.",
    )
    return launch_review(job, key, source=source)


@router.get("/runs/{run_id}/candidates")
async def benchmark_candidates(run_id: str, queue_id: str, response: Response,
                               x_review_token: Annotated[str | None, Header()] = None,
                               page: Annotated[int, Query(ge=1)] = 1) -> dict:
    response.headers["Cache-Control"] = "no-store"
    job = authorize(run_id, x_review_token)
    retrieval = job.benchmark_retrieval if job.request.mode in {"retrieval", "screening", "selection", "adaptive"} else None
    queue = next((queue for queue in retrieval["queues"] if queue["queue_id"] == queue_id), None) if retrieval else None
    if queue is None:
        raise HTTPException(404, "Candidate queue not found.")
    ranking = next(ranking for ranking in retrieval["rankings"] if ranking["facet_id"] == queue["facet_id"])
    candidates = {item["item_id"]: item for item in ranking["candidates"]}
    total = len(queue["item_ids"])
    pages = max(1, (total + RESULTS_PAGE_SIZE - 1) // RESULTS_PAGE_SIZE)
    page = min(page, pages)
    start = (page - 1) * RESULTS_PAGE_SIZE
    snapshot = {"queue_id": queue_id, "facet_id": queue["facet_id"], "page": page,
            "page_size": RESULTS_PAGE_SIZE, "total_pages": pages, "total_items": total,
            "items": [candidates[key] for key in queue["item_ids"][start:start + RESULTS_PAGE_SIZE]]}
    return StreamingResponse(_json_chunks(snapshot), media_type="application/json",
                             headers={"Cache-Control": "no-store"})


@router.get("/runs/{run_id}")
async def get_review(run_id: str, response: Response,
               x_review_token: Annotated[str | None, Header()] = None,
               page: Annotated[int, Query(ge=1)] = 1) -> dict:
    response.headers["Cache-Control"] = "no-store"
    snapshot = deepcopy(public_job(authorize(run_id, x_review_token), page))
    return StreamingResponse(_json_chunks(snapshot), media_type="application/json",
                             headers={"Cache-Control": "no-store"})


@router.get("/runs/{run_id}/export")
async def export_review(run_id: str, x_review_token: Annotated[str | None, Header()] = None):
    job = authorize(run_id, x_review_token)
    snapshot = public_job(job, include_items=False)
    if job.request.mode in {"retrieval", "screening", "selection", "adaptive"}:
        # The worker replaces its snapshot after each completed facet. Holding
        # this reference keeps a download consistent while retrieval continues.
        snapshot["retrieval"] = job.benchmark_retrieval
        job.downloads += 1
        closed = False

        def release_download():
            nonlocal closed
            if not closed:
                closed = True
                job.downloads -= 1

        async def retrieval_content():
            try:
                async for chunk in iterate_in_threadpool(_json_chunks(snapshot)):
                    yield chunk
            finally:
                release_download()

        class RetrievalResponse(StreamingResponse):
            async def __call__(self, scope, receive, send):
                try:
                    await super().__call__(scope, receive, send)
                finally:
                    release_download()

        return RetrievalResponse(retrieval_content(), media_type="application/json", headers={
            "Cache-Control": "no-store",
            "Content-Disposition": f'attachment; filename="benchmark-{job.request.mode}-{run_id}.json"',
        })
    if job.request.mode in {"requirements", "grounding"}:
        name = "onet-grounding" if job.request.mode == "grounding" else "requirements"
        return JSONResponse(snapshot, headers={
            "Cache-Control": "no-store",
            "Content-Disposition": f'attachment; filename="{name}-{run_id}.json"',
        })
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


def package_snapshot(job: ReviewJob) -> dict:
    if job.request.mode == "item_review":
        raise HTTPException(409, "Results packages are available for the goal-conditioned construction pipeline.")
    # Capture all fields together before yielding to a running pipeline worker.
    # The package includes full rankings, not the paginated polling preview.
    snapshot = public_job(job, include_items=False)
    if "retrieval" in snapshot:
        snapshot["retrieval"] = job.benchmark_retrieval
    return deepcopy(snapshot)


def package_error(error: Exception) -> dict:
    if isinstance(error, CandidateStoreError):
        return {"error_status": 503, "message": "Saved candidate evidence could not be read. Your saved results are retained; retry the download or contact the site maintainer."}
    if isinstance(error, OSError) and error.errno in {errno.ENOSPC, errno.EDQUOT}:
        return {"error_status": 507, "message": "The server has insufficient temporary space to prepare the package. Your saved results are retained; contact the site maintainer."}
    return {"error_status": 500, "message": "The results package could not be prepared. Retry the download; your saved results are retained."}


async def prepare_package(job: ReviewJob, snapshot: dict) -> None:
    state = job.package
    started = time.monotonic()
    package = None
    worker = asyncio.create_task(asyncio.to_thread(
        review_exports.build, snapshot, builder=build_results_package, expand=expand_candidate))
    try:
        package = await asyncio.shield(worker)
        size = package.seek(0, 2)
        package.seek(0)
        state.file, state.size = package, size
        state.refresh_lease()
        logger.info("Review results package ready run_id=%r bytes=%d seconds=%.1f",
                    job.run_id, size, time.monotonic() - started)
    except asyncio.CancelledError:
        await finish_worker(worker)
        if not worker.cancelled() and worker.exception() is None:
            worker.result().close()
        state.error = {"error_status": 503, "message": "Package preparation was interrupted. Retry the download; your saved results are retained."}
        raise
    except Exception as error:
        if package is not None:
            package.close()
        state.error = package_error(error)
        logger.warning("Review results package failed run_id=%r error=%s seconds=%.1f",
                       job.run_id, type(error).__name__, time.monotonic() - started)


def package_preparation_finished(job: ReviewJob, state, task) -> None:
    # A task cancelled before its first turn cannot run a coroutine's finally.
    job.downloads -= 1
    if task.cancelled() and state.error is None:
        state.error = {"error_status": 503, "message": "Package preparation was interrupted. Retry the download; your saved results are retained."}


@router.post("/runs/{run_id}/package")
async def start_package(run_id: str, x_review_token: Annotated[str | None, Header()] = None):
    job = authorize(run_id, x_review_token)
    if jobs.get(job.run_id) is not job:
        # Synchronous reads can use an uncached restored run, but a background
        # preparation must stay registered for polling and shutdown cleanup.
        raise HTTPException(429, "The server is busy preparing other reviews or downloads. Retry shortly; your saved results are retained.")
    state = job.package
    if state.task is not None and not state.task.done():
        return JSONResponse(state.public(), status_code=202, headers={"Cache-Control": "no-store"})
    if state.transferring:
        raise HTTPException(409, "A package download is already in progress. Wait for it to finish before downloading again.")
    snapshot = package_snapshot(job)
    key = review_exports.snapshot_key(snapshot)
    if state.file is not None and state.key == key:
        state.refresh_lease()
        return JSONResponse(state.public(), headers={"Cache-Control": "no-store"})
    state.close()
    snapshot["metadata"]["exported_at"] = datetime.now(timezone.utc).isoformat()
    job.package = review_exports.PreparedPackage(key=key, filename=package_filename(snapshot))
    job.downloads += 1
    job.package.task = asyncio.create_task(prepare_package(job, snapshot))
    job.package.task.add_done_callback(lambda task, state=job.package: package_preparation_finished(job, state, task))
    return JSONResponse(job.package.public(), status_code=202, headers={"Cache-Control": "no-store"})


@router.get("/runs/{run_id}/package/status")
async def get_package_status(run_id: str, response: Response,
                             x_review_token: Annotated[str | None, Header()] = None):
    response.headers["Cache-Control"] = "no-store"
    job = authorize(run_id, x_review_token)
    if job.request.mode == "item_review":
        raise HTTPException(409, "Results packages are available for the goal-conditioned construction pipeline.")
    return job.package.public()


@router.get("/runs/{run_id}/package/chunk")
async def get_package_chunk(run_id: str, package_id: str, offset: str,
                            x_review_token: Annotated[str | None, Header()] = None):
    job = authorize(run_id, x_review_token)
    state = job.package
    if state.file is None or state.package_id != package_id:
        raise HTTPException(412, "The prepared package is no longer available. Retry the download to prepare it again from your saved results.")
    try:
        position = int(offset)
    except ValueError:
        raise HTTPException(416, "The requested package offset is invalid.") from None
    if not 0 <= position < state.size:
        raise HTTPException(416, "The requested package offset is outside the archive.")
    if state.transferring:
        raise HTTPException(429, "Another package read is in progress. Retry this part shortly.")
    state.transferring = True
    state.refresh_lease()
    job.downloads += 1
    expected = min(review_exports.CHUNK_BYTES, state.size - position)

    def read():
        state.file.seek(position)
        data = state.file.read(expected)
        if len(data) != expected:
            raise OSError("Incomplete prepared archive")
        return data

    worker = asyncio.create_task(asyncio.to_thread(read))
    state.read_task = worker
    try:
        data = await asyncio.shield(worker)
        # Keep the finite grace period even for the final piece: its response
        # can still be interrupted, in which case the client retries this offset.
        return Response(data, media_type="application/zip", headers={
            "Cache-Control": "no-store, no-transform", "Content-Length": str(len(data)),
            "X-Package-Id": state.package_id, "X-Package-Offset": str(position),
            "X-Accel-Buffering": "no",
        })
    except asyncio.CancelledError:
        # A cancelled HTTP request must not release the shared cursor while its
        # thread is still reading; retries then cannot corrupt each other's data.
        await finish_worker(worker)
        raise
    except Exception as error:
        state.close()
        state.error = {"error_status": 503, "message": "The prepared package could not be read. Retry the download; your saved results are retained."}
        logger.warning("Review package read failed run_id=%r error=%s", job.run_id, type(error).__name__)
        raise HTTPException(503, state.error["message"]) from None
    finally:
        state.read_task = None
        state.transferring = False
        job.downloads -= 1


def prepared_package_response(job: ReviewJob):
    state = job.package
    if state.transferring:
        raise HTTPException(409, "A package download is already in progress. Wait for it to finish before downloading again.")
    if state.file is None:
        if state.error:
            raise HTTPException(state.error["error_status"], state.error["message"])
        raise HTTPException(409, "The package is not ready. Retry the download to prepare it from saved results.")
    state.file.seek(0)
    state.transferring = True
    job.downloads += 1
    released = False

    def release():
        nonlocal released
        if not released:
            released = True
            state.transferring = False
            job.downloads -= 1

    async def contents():
        try:
            while chunk := await run_in_threadpool(state.file.read, 64 * 1024):
                yield chunk
        finally:
            release()

    class PreparedResponse(StreamingResponse):
        async def __call__(self, scope, receive, send):
            try:
                await super().__call__(scope, receive, send)
            finally:
                release()

    return PreparedResponse(contents(), media_type="application/zip", headers={
        "Cache-Control": "no-store", "Content-Length": str(state.size),
        "X-Accel-Buffering": "no",
        "Content-Disposition": f'attachment; filename="{state.filename}"',
    })


@router.get("/runs/{run_id}/package")
async def export_package(run_id: str, x_review_token: Annotated[str | None, Header()] = None,
                         prepared: bool = False):
    job = authorize(run_id, x_review_token)
    if prepared:
        return prepared_package_response(job)
    # Older clients still receive a direct export. Current clients prepare and
    # poll first, so the file request itself never waits for compression.
    snapshot = package_snapshot(job)
    snapshot["metadata"]["exported_at"] = datetime.now(timezone.utc).isoformat()
    job.downloads += 1
    package = None
    closed = False

    def close_package():
        nonlocal closed
        if not closed:
            closed = True
            if package is not None:
                package.close()
            job.downloads -= 1

    worker = asyncio.create_task(asyncio.to_thread(
        review_exports.build, snapshot, builder=build_results_package, expand=expand_candidate))
    try:
        # Compression runs off the event loop. A disconnected client must not
        # leave a thread writing an unowned temporary file.
        try:
            package = await asyncio.shield(worker)
        except asyncio.CancelledError:
            await finish_worker(worker)
            if not worker.cancelled() and worker.exception() is None:
                package = worker.result()
            raise

        async def contents():
            try:
                while chunk := await run_in_threadpool(package.read, 64 * 1024):
                    yield chunk
            finally:
                close_package()

        class PackageResponse(StreamingResponse):
            async def __call__(self, scope, receive, send):
                # Header/send failures can precede the generator's first yield;
                # response background tasks do not run on every disconnect.
                try:
                    await super().__call__(scope, receive, send)
                finally:
                    close_package()

        size = package.seek(0, 2)
        package.seek(0)
        return PackageResponse(contents(), media_type="application/zip", headers={
            "Cache-Control": "no-store",
            "Content-Length": str(size), "X-Accel-Buffering": "no",
            "Content-Disposition": f'attachment; filename="{package_filename(snapshot)}"',
        })
    except Exception as error:
        close_package()
        failure = package_error(error)
        logger.warning("Review results package failed run_id=%r error=%s", job.run_id, type(error).__name__)
        raise HTTPException(failure["error_status"], failure["message"]) from None
    except BaseException:
        close_package()
        raise


@router.post("/runs/{run_id}/cancel")
async def cancel_review(run_id: str, response: Response,
                        x_review_token: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    job = authorize(run_id, x_review_token)
    if job.task and not job.task.done():
        job.task.cancel()
        await asyncio.gather(job.task, return_exceptions=True)
        # A task cancelled before its coroutine starts cannot run its finally.
        job.status = "cancelled"
        job.message = stopped_message(job)
        job.finished_at = time.monotonic()
        job.finished_at_utc = datetime.now(timezone.utc).isoformat()
        try:
            checkpoint(job)
        except CheckpointError:
            job.status = "failed"
            job.message = "The server could not save the stopped review. Download its results now; they may not survive a server restart."
            logger.error("Review checkpoint save failed during cancellation run_id=%r", job.run_id)
    return StreamingResponse(_json_chunks(deepcopy(public_job(job))), media_type="application/json",
                             headers={"Cache-Control": "no-store"})


def stopped_message(job: ReviewJob) -> str:
    return {
        "requirements": "Requirement extraction stopped.",
        "grounding": "O*NET grounding stopped. Completed facet mappings are retained.",
        "retrieval": "Benchmark retrieval stopped. Completed task rankings and queues are retained.",
        "screening": "Screening stopped. Completed item results are retained; continue to finish the initial set.",
        "selection": "Selection stopped. Any previously accepted collection is retained.",
        "adaptive": "Adaptive screening stopped. Completed assessments and the last accepted collection are retained; resume to finish the pending batch.",
        "item_review": "Review stopped. Completed assessments are retained.",
    }[job.request.mode]


async def finish_worker(work: asyncio.Task) -> None:
    """Drain a thread task even if Stop and shutdown cancel its parent twice."""
    while not work.done():
        try:
            await asyncio.shield(work)
        except asyncio.CancelledError:
            continue
        except Exception:
            break
    if not work.cancelled():
        work.exception()  # Consume a worker failure; the parent preserves cancellation.


async def prepare_review(job):
    cancelled = Event()

    def progress(benchmark, completed, rows):
        job.prepared_benchmarks = completed
        job.source_rows = rows
        job.message = f"Preparing sample from {benchmark}. No paid calls yet."

    prepare = asyncio.create_task(asyncio.to_thread(
        prepare_samples, job.inventory, db.DEFAULT_DB_PATH.parent / "item-review-samples",
        token=get_token(), progress=progress, cancelled=cancelled,
    ))
    try:
        return await asyncio.shield(prepare)
    except asyncio.CancelledError:
        cancelled.set()
        await finish_worker(prepare)
        raise


async def review_items(job):
    paths, total = await prepare_review(job)
    return iter_sample_items(paths), total


async def retrieve_items(job: ReviewJob, items) -> list[dict]:
    """Select a small candidate set locally before opening a paid API client."""
    cancelled = Event()

    def select():
        global _cached_index
        acquired = False
        try:
            # Keep generator reads and close in the same thread, including when
            # the coroutine is cancelled while a disk read is in progress.
            rows = []
            for item in items:
                if cancelled.is_set():
                    raise InterruptedError("Retrieval cancelled")
                rows.append(item)
            key = fingerprint({"policy": RETRIEVAL_POLICY, "items": [
                {"hash": item["evidence_hash"], "sources": item.get("sources", [])}
                for item in rows
            ]})
            while not acquired:
                if cancelled.is_set():
                    raise InterruptedError("Retrieval cancelled")
                acquired = _retrieval_lock.acquire(timeout=0.1)
            if _cached_index is None or _cached_index[0] != key:
                job.message = "Embedding sample questions locally with Qwen3. No paid calls yet."

                def progress(state):
                    job.message = (f"Preparing local question vectors: {state['completed']:,} of "
                                   f"{state['total']:,} ready ({state['cache_hits']:,} cached). No paid calls yet.")

                index = ItemIndex(rows, cache_dir=db.DEFAULT_DB_PATH.parent / "item-review-embeddings",
                                  cancelled=cancelled.is_set, progress=progress)
                if cancelled.is_set():
                    raise InterruptedError("Retrieval cancelled")
                _cached_index = (key, index)
            index = _cached_index[1]
            job.indexed_items = index.indexed_items
            job.contentless_items = index.contentless_items
            job.message = "Finding reference items with normalized question vectors. No paid calls yet."
            selected = index.search(job.request.query(), top_k=job.request.retrieve_k,
                                    cancelled=cancelled.is_set)
            if cancelled.is_set():
                raise InterruptedError("Retrieval cancelled")
            return selected
        finally:
            if acquired:
                _retrieval_lock.release()
            if hasattr(items, "close"):
                items.close()

    work = asyncio.create_task(asyncio.to_thread(select))
    try:
        return await asyncio.shield(work)
    except asyncio.CancelledError:
        cancelled.set()
        # Let an in-flight local batch finish before releasing the shared index
        # or allowing shutdown to delete files used by this worker.
        await finish_worker(work)
        raise


async def next_item(items):
    # Wait for an in-flight read before closing its generator on cancellation.
    read = asyncio.create_task(asyncio.to_thread(next, items, None))
    try:
        return await asyncio.shield(read)
    except asyncio.CancelledError:
        await finish_worker(read)
        raise


def record_usage(job: ReviewJob, usage: dict | None) -> None:
    usage = usage or {}
    for name in ("input_tokens", "output_tokens"):
        job.usage[name] += usage.get(name, 0)
    job.usage["reasoning_tokens"] += (usage.get("output_tokens_details") or {}).get("reasoning_tokens", 0)
    job.usage["cached_input_tokens"] += (usage.get("input_tokens_details") or {}).get("cached_tokens", 0)


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
                    field: item[field] for field in ("retrieval_rank", "retrieval_score", "exact_match")
                    if field in item}, **{
                    field: assessment[field] for field in (
                        "status", "assessment", "overall_score", "response_model", "response_id",
                        "compatibility_score", "scored_dimensions", "needs_review",
                    ) if field in assessment}}
                if assessment["status"] == "error":
                    result["error"] = "The model did not return a complete, valid assessment."
                job.results.append(result)
                record_usage(job, assessment.get("usage"))
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


async def extract_requirements(job: ReviewJob, api_key: str) -> None:
    job.status, job.message = "running", "Extracting evidence-linked requirements with GPT-6 Luna."
    async with AsyncOpenAI(api_key=api_key, base_url="https://api.openai.com/v1",
                           max_retries=2, timeout=600) as client:
        extractor = AsyncRequirementExtractor(client)
        job.extraction = {
            "version": EXTRACTION_VERSION, "model": extractor.model,
            "reasoning_effort": extractor.reasoning_effort,
            "max_output_tokens": extractor.max_output_tokens,
            "prompt": extractor.prompt, "output_schema": Requirements.model_json_schema(),
        }
        result = await extractor(job.request.deployment.model_dump())
    record_usage(job, result.get("usage"))
    for name in ("response_id", "response_model"):
        job.extraction[name] = result.get(name)
    job.extraction["usage"] = deepcopy(result.get("usage"))
    if result["status"] != "complete":
        job.status = "failed"
        job.message = f"Requirement extraction failed: {result['error']} Start a new extraction to retry."
        return
    job.requirements = result["requirements"]
    job.status = "completed"
    job.message = "Requirements extracted. Review the interpretation alongside its source evidence."


async def retrieve_onet(job: ReviewJob, requirements: Requirements) -> tuple[list[dict], dict]:
    """Search each facet before making any mapping requests."""
    remote = RemoteRetrieval.from_environment()
    if remote is not None:
        searches, policy = [], None
        for number, facet in enumerate(requirements.task_facets, 1):
            job.message = (f"Searching O*NET descriptions for task {number} of "
                           f"{len(requirements.task_facets)}. No paid mapping calls yet.")
            query = build_onet_query(requirements, facet)
            result = await remote.search("onet", query)
            if policy is not None and policy != result["policy"]:
                raise RemoteRetrievalError("The O*NET retrieval policy changed between tasks. Please retry grounding.")
            policy = result["policy"]
            searches.append({"facet_id": facet.facet_id, "query": query, "candidates": result["candidates"]})
        return searches, policy
    cancelled = Event()
    materials = Path(os.environ.get("ITEM_REVIEW_ONET_DIR", str(DEFAULT_MATERIALS_DIR))).resolve()

    def search():
        global _cached_onet_index
        acquired = False
        try:
            while not acquired:
                if cancelled.is_set():
                    raise InterruptedError("O*NET retrieval cancelled")
                acquired = _retrieval_lock.acquire(timeout=0.1)
            if _cached_onet_index is None or _cached_onet_index[0] != materials:
                job.message = "Loading the local healthcare O*NET catalog. No paid mapping calls yet."
                index = OnetIndex(materials_dir=materials, cancelled=cancelled.is_set)
                if cancelled.is_set():
                    raise InterruptedError("O*NET retrieval cancelled")
                _cached_onet_index = (materials, index)
            index = _cached_onet_index[1]
            results = []
            for number, facet in enumerate(requirements.task_facets, 1):
                if cancelled.is_set():
                    raise InterruptedError("O*NET retrieval cancelled")
                job.message = (f"Searching local O*NET descriptions for task {number} of "
                               f"{len(requirements.task_facets)}. No paid mapping calls yet.")
                query = build_onet_query(requirements, facet)
                candidates = index.search(query, cancelled=cancelled.is_set)
                results.append({"facet_id": facet.facet_id, "query": query, "candidates": candidates})
            if cancelled.is_set():
                raise InterruptedError("O*NET retrieval cancelled")
            return results, deepcopy(index.policy)
        finally:
            if acquired:
                _retrieval_lock.release()

    work = asyncio.create_task(asyncio.to_thread(search))
    try:
        return await asyncio.shield(work)
    except asyncio.CancelledError:
        cancelled.set()
        await finish_worker(work)
        raise


async def ground_requirements(job: ReviewJob, api_key: str) -> None:
    requirements = Requirements.model_validate(job.requirements)
    answers = job.request.deployment.model_dump()
    requirements.validate_evidence(answers)
    searches, retrieval_policy = await retrieve_onet(job, requirements)
    async with AsyncOpenAI(api_key=api_key, base_url="https://api.openai.com/v1",
                           max_retries=2, timeout=600) as client:
        mapper = AsyncOnetMapper(client)
        job.grounding = {
            "retrieval": retrieval_policy,
            "mapping": {
                "version": MAPPING_VERSION, "model": mapper.model,
                "reasoning_effort": mapper.reasoning_effort,
                "max_output_tokens": mapper.max_output_tokens,
                "prompt": mapper.prompt, "output_schema": OnetMapping.model_json_schema(),
            },
            "facets": [],
        }
        for number, (facet, search) in enumerate(zip(requirements.task_facets, searches), 1):
            job.status = "running"
            job.message = (f"Mapping O*NET descriptions to task {number} of "
                           f"{len(requirements.task_facets)} with GPT-6 Luna.")
            if search["candidates"]:
                result = await mapper(answers, requirements, facet, search["candidates"])
            else:
                result = {"status": "complete", "mapping": {
                    "facet_id": facet.facet_id, "records": [], "refinements": [],
                    "unresolved_details": ["No O*NET candidates were retrieved for this task."],
                }}
            record_usage(job, result.get("usage"))
            job.grounding["facets"].append({**search, "mapping": None, **result})
            checkpoint(job)
            if result["status"] != "complete":
                job.status = "failed"
                job.message = "O*NET mapping failed validation. Completed facet mappings are retained; review the error before retrying."
                return
    job.status = "completed"
    job.message = "O*NET grounding is ready. Review the supporting passages and applicability for each task."


async def retrieve_benchmarks(job: ReviewJob) -> None:
    """Search the configured index and retain rankings for each parent task."""
    remote = RemoteRetrieval.from_environment()
    if remote is not None:
        job.status = "running"
        state = job.benchmark_retrieval
        for number, query in enumerate(state["queries"], 1):
            job.message = f"Retrieving benchmark candidates for task {number} of {len(state['queries'])}."
            result = await remote.search("benchmark", query["query"], inventory=job.inventory,
                                         candidate_store=candidate_store())
            if state["policy"] is not None and (state["policy"] != result["policy"] or state["stats"] != result["stats"]):
                raise RemoteRetrievalError("The benchmark index changed between tasks. Please retry retrieval.")
            state = {**state, "policy": result["policy"], "stats": result["stats"]}
            state = record_benchmark_ranking(state, query, number, result["candidates"])
            job.benchmark_retrieval = state
            checkpoint(job)
        job.status = "completed"
        job.message = "Benchmark candidates and task/source queues are ready for review. Relevance screening is the next step."
        return
    cancelled = Event()

    def progress(state):
        stage = {"indexing": "Preparing benchmark search",
                 "cache": "Using the prepared benchmark index"}[state["stage"]]
        job.message = f"{stage}: {state['completed']:,} of {state['total']:,}."

    def search():
        acquired, items, index = False, None, None
        try:
            while not acquired:
                if cancelled.is_set():
                    raise InterruptedError("Benchmark retrieval cancelled")
                acquired = _retrieval_lock.acquire(timeout=0.1)
            token = get_token()
            items = lambda offset: iter_benchmark_items(
                job.inventory, token=token, streaming=True, skip_rows=offset,
            )

            def load_rows(requests, *, cancelled=None):
                return fetch_benchmark_rows(job.inventory, requests, token=token, cancelled=cancelled)

            index = prepare_benchmark_index(
                items, cache_dir=db.DEFAULT_DB_PATH.parent / "benchmark-retrieval-index",
                inventory=job.inventory, cancelled=cancelled.is_set, progress=progress, resume=True,
                minimum_free_bytes=DEFAULT_MINIMUM_FREE_BYTES, row_loader=load_rows,
            )
            state = {**job.benchmark_retrieval, "policy": index.policy, "stats": index.stats}
            job.benchmark_retrieval = state
            job.status = "running"
            queries = state["queries"]
            for number, query in enumerate(queries, 1):
                if cancelled.is_set():
                    raise InterruptedError("Benchmark retrieval cancelled")
                job.message = f"Retrieving benchmark candidates for task {number} of {len(queries)}."
                candidates = index.search(query["query"], cancelled=cancelled.is_set)
                if cancelled.is_set():
                    raise InterruptedError("Benchmark retrieval cancelled")
                state = record_benchmark_ranking(state, query, number, candidates)
                job.benchmark_retrieval = state
                checkpoint(job)
        finally:
            try:
                if index is not None:
                    index.close()
            finally:
                try:
                    if hasattr(items, "close"):
                        items.close()
                finally:
                    if acquired:
                        _retrieval_lock.release()

    work = asyncio.create_task(asyncio.to_thread(search))
    try:
        await asyncio.shield(work)
    except asyncio.CancelledError:
        cancelled.set()
        await finish_worker(work)
        raise
    job.status = "completed"
    job.message = "Benchmark candidates and task/source queues are ready for review. Relevance screening is the next step."


def record_benchmark_ranking(state: dict, query: dict, number: int, candidates: list[dict]) -> dict:
    """Use the same saved evidence and queue construction for either host."""
    store = candidate_store()
    candidates = [store.compact(candidate) for candidate in candidates]
    rankings = [*state["rankings"], {**query, "candidates": candidates}]
    state = {**state, "rankings": rankings, "queues": build_screening_queues(rankings),
             "queries": [*state["queries"]]}
    state["queries"][number - 1] = {**query, "candidate_count": len(candidates)}
    return state


async def screen_benchmarks(job: ReviewJob, api_key: str) -> None:
    """Screen the fixed initial allocation; collection selection comes later."""
    requirements = Requirements.model_validate(job.requirements)
    answers = job.request.deployment.model_dump()
    requirements.validate_evidence(answers)
    candidates = screening_candidates(job.benchmark_retrieval, requirements)
    allocation = job.screening["allocation"]
    done = {item["item_id"] for item in job.screening["items"]}
    pending = iter(item for item in allocation["items"] if item["item_id"] not in done)
    order = {item["item_id"]: index for index, item in enumerate(allocation["items"])}
    job.status = "running"
    if not allocation["allocated"]:
        job.status, job.message = "completed", "No candidates were available to screen. No paid calls were made."
        return

    async with AsyncOpenAI(api_key=api_key, base_url="https://api.openai.com/v1",
                           max_retries=2, timeout=600) as client:
        settings = job.screening["model"]
        screener = AsyncItemScreener(client, prompt=settings["prompt"], model=settings["model"],
                                     reasoning_effort=settings["reasoning_effort"],
                                     max_output_tokens=settings["max_output_tokens"])

        async def worker():
            # next() and the result update contain no awaits, so workers cannot
            # reserve the same item or overwrite one another's saved results.
            for acquisition in pending:
                reference = candidates[acquisition["facet_id"], acquisition["item_id"]]
                candidate = expand_candidate(reference)
                result = await screener(answers, requirements, candidate["evidence"]["item"])
                saved = {
                    **candidate_store().compact(candidate),
                    "acquisition": {key: acquisition[key] for key in ("queue_id", "facet_id")},
                    "screened_run_id": job.run_id,
                    **{key: result[key] for key in (
                        "status", "assessment", "gate", "response_id", "response_model", "usage",
                    ) if key in result},
                }
                if result["status"] == "error":
                    saved["error"] = result["error"]
                record_usage(job, result.get("usage"))
                items = sorted([*job.screening["items"], saved], key=lambda item: order[item["item_id"]])
                job.screening = {**job.screening, "items": items}
                job.message = f"Screening initial candidates: {len(items)} of {allocation['allocated']} processed."
                checkpoint(job)

        workers = [asyncio.create_task(worker()) for _ in range(REVIEW_CONCURRENCY)]
        try:
            await asyncio.gather(*workers)
        finally:
            for task in workers:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*workers, return_exceptions=True)
    errors = sum(item["status"] == "error" for item in job.screening["items"])
    job.status = "completed"
    job.message = (
        f"Initial screening finished with {errors} response error{'s' if errors != 1 else ''}. Continue to retry the affected items."
        if errors else "Initial screening is ready. Review task matches, ratings, and construction gate outcomes."
    )


async def select_benchmarks(job: ReviewJob) -> None:
    """Run local optimization off the event loop and publish only a complete solve."""
    requirements = validate_selection_source(job)
    previous_ids = job.selection["selected_item_ids"] if job.selection is not None else None
    cancelled = Event()
    job.status, job.message = "running", "Choosing up to 30 items while enforcing coverage and rating priorities."
    work = asyncio.create_task(asyncio.to_thread(
        select_collection, requirements, screened_records(job),
        previous_selected_ids=previous_ids, cancelled=cancelled.is_set,
    ))
    try:
        selection = await asyncio.shield(work)
    except asyncio.CancelledError:
        cancelled.set()
        await finish_worker(work)
        raise
    # A cancelled or incomplete solve cannot replace an accepted collection.
    job.selection = selection
    job.selection_run_id = job.run_id
    checkpoint(job)
    job.status = "completed"
    count = selection["selected_count"]
    job.message = (
        f"Selected {count} items in total. All specified coverage requirements are satisfied."
        if selection["fully_satisfied"] else
        f"Selected {count} items in total. Review the reported coverage gaps and unresolved requirements."
    )


async def evaluate(job: ReviewJob, api_key: str) -> None:
    items = None
    try:
        if job.request.mode == "requirements":
            await extract_requirements(job, api_key)
            return
        if job.request.mode == "grounding":
            await ground_requirements(job, api_key)
            return
        if job.request.mode == "retrieval":
            await retrieve_benchmarks(job)
            return
        if job.request.mode == "screening":
            await screen_benchmarks(job, api_key)
            return
        if job.request.mode == "selection":
            await select_benchmarks(job)
            return
        if job.request.mode == "adaptive":
            await adaptive_review.adapt_benchmarks(job, api_key)
            return
        items, job.total = await review_items(job)
        selected = await retrieve_items(job, items)
        items = iter(selected)
        job.retrieved_items = job.total = len(selected)
        job.status, job.message = "running", f"Assessing {job.total} retrieved items across all six validity dimensions."
        if not selected:
            job.sample_complete = True
            job.status, job.message = "completed", "No items with question text were available for retrieval. No paid calls were made."
            return
        async with AsyncOpenAI(api_key=api_key, base_url="https://api.openai.com/v1",
                               max_retries=2, timeout=600) as client:
            judge = AsyncJudge(client, job.request.deployment.describe(), PROMPT_PATH.read_text(encoding="utf-8"))
            await assess_items(job, items, judge)
        job.sample_complete = True
        job.status = "completed"
        job.message = "The retrieved shortlist has been assessed. Other sample items were not sent to the judge."
    except asyncio.CancelledError:
        job.status = "cancelled"
        job.message = stopped_message(job)
    except SelectionIncomplete:
        job.status = "failed"
        job.message = "Selection did not finish proving the best collection. Any previously accepted collection is retained; retry selection to try again."
        if job.request.mode == "adaptive":
            job.message = "Adaptive selection did not finish proving the best collection. The batch results and previous collection are retained; resume to retry selection without repeating valid screening."
    except AuthenticationError:
        job.status, job.message = "failed", "OpenAI rejected the API key. Check its access and start a new review."
    except RateLimitError:
        job.status, job.message = "failed", "OpenAI reported a rate or quota limit. Completed results are retained."
    except OpenAIError:
        job.status, job.message = "failed", "The OpenAI request failed. Check model access and try again."
    except RemoteRetrievalError as exc:
        job.status, job.message = "failed", str(exc)
    except CandidateStoreError:
        job.status = "failed"
        job.message = "The server could not save or read candidate evidence, so this stage stopped. Contact the site maintainer to check storage before continuing."
        logger.error("Candidate evidence storage failed during work run_id=%r", job.run_id)
    except CheckpointError:
        job.status = "failed"
        job.message = "The server could not save progress, so this stage stopped. Download the available results and contact the site maintainer before continuing."
        logger.error("Review checkpoint save failed during work run_id=%r", job.run_id)
    except Exception:
        job.status = "failed"
        if job.request.mode == "grounding":
            job.message = "Could not complete O*NET grounding. Check the local catalog and embedding model setup, or contact the site maintainer."
        elif job.request.mode == "requirements":
            job.message = "Could not extract requirements. Please try again later or contact the site maintainer."
        elif job.request.mode == "retrieval":
            job.message = "Could not complete benchmark retrieval. Check dataset access, local model setup, and disk space. Completed task rankings are retained."
        elif job.request.mode == "screening":
            job.message = "Could not complete screening. Completed item results are retained; continue to retry unfinished items."
        elif job.request.mode == "selection":
            job.message = "Could not complete collection selection. Saved screening results and any previously accepted collection are retained."
        elif job.request.mode == "adaptive":
            job.message = "Could not complete adaptive screening. Saved assessments, batch history, and the previous collection are retained; resume to retry unfinished work."
        else:
            job.message = "Could not load or process evaluation items. Please try again later or contact the site maintainer."
    finally:
        if hasattr(items, "close"):
            items.close()
        api_key = ""
        job.finished_at = time.monotonic()
        job.finished_at_utc = datetime.now(timezone.utc).isoformat()
        try:
            checkpoint(job)
        except CheckpointError:
            job.status = "failed"
            job.message = "The server could not save this stage's latest results. Download them now; only earlier saved progress may survive a server restart."
            logger.error("Review checkpoint save failed at completion run_id=%r", job.run_id)
        trim_pipeline_cache(keep=job.run_id)
