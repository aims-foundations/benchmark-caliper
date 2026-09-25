"""Small, in-memory website jobs using the shared six-dimension item judge.

Only source dataset downloads are cached on disk. Keys, deployment descriptions,
and assessments remain in memory. A run secret protects polling/cancellation.
The single-instance deployment deliberately uses no database or job queue here.
"""

from __future__ import annotations

import asyncio
from collections import Counter
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import secrets
import time
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Response
from huggingface_hub import get_token
from openai import AsyncOpenAI, AuthenticationError, RateLimitError, OpenAIError
from pydantic import BaseModel, ConfigDict, Field

from bayesian_auditing.data import iter_items
from bayesian_auditing.judge import (
    AsyncJudge, DEFAULT_MODEL, DEFAULT_REASONING_EFFORT, DEFAULT_MAX_OUTPUT_TOKENS, PROMPT_PATH,
)

router = APIRouter(prefix="/api/item-review", tags=["Item review"])
INVENTORY_PATH = Path(__file__).with_name("item_review_inventory.json")
MAX_ACTIVE = 3
MAX_RETAINED = 30
RETENTION_SECONDS = 3600
MAX_RUN_SECONDS = 3600
BENCHMARK_NAMES = {"matharena": "MathArena · mathematics", "afrimedqa": "AfriMed-QA · medical questions"}


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
    benchmarks: list[str] = Field(min_length=1, max_length=2)
    items_per_table: int = Field(default=2, ge=1, le=10, strict=True)
    top_k: int = Field(default=10, ge=1, le=30, strict=True)


@dataclass
class ReviewJob:
    run_id: str
    secret: str = field(repr=False)
    owner_hash: str = field(repr=False)
    request: ReviewRequest = field(repr=False)
    created_at: float = field(default_factory=time.monotonic)
    finished_at: float | None = None
    task: asyncio.Task | None = field(default=None, repr=False)
    status: str = "preparing"
    message: str = "Loading the selected sample from both dataset branches."
    source_rows: int = 0
    total: int = 0
    results: list[dict] = field(default_factory=list)
    usage: Counter = field(default_factory=Counter)


jobs: dict[str, ReviewJob] = {}


def inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def sweep() -> None:
    now = time.monotonic()
    for run_id, job in list(jobs.items()):
        if job.finished_at is not None and now - job.finished_at > RETENTION_SECONDS:
            jobs.pop(run_id, None)


async def shutdown() -> None:
    tasks = [job.task for job in jobs.values() if job.task and not job.task.done()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    jobs.clear()


@router.get("/catalog")
async def catalog(response: Response) -> dict:
    response.headers["Cache-Control"] = "no-store"
    data = inventory()
    return {
        "model": DEFAULT_MODEL, "reasoning_effort": DEFAULT_REASONING_EFFORT,
        "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS,
        "branches": data["branches"], "requires_hf_token": not bool(get_token()),
        "max_items_per_table": 10,
        "benchmarks": [{"id": name, "name": BENCHMARK_NAMES[name],
                        "table_count": sum(t["benchmark"] == name for t in data["tables"])}
                       for name in BENCHMARK_NAMES],
    }


def public_job(job: ReviewJob) -> dict:
    counts = Counter(item["status"] for item in job.results)
    ranked = sorted((item for item in job.results if item["status"] == "complete"),
                    key=lambda item: (-item["overall_score"], item["evidence_hash"]))
    return {
        "run_id": job.run_id, "status": job.status, "message": job.message,
        "model": DEFAULT_MODEL, "reasoning_effort": DEFAULT_REASONING_EFFORT,
        "deployment": job.request.deployment.model_dump(),
        "scope": {"benchmarks": job.request.benchmarks, "items_per_table": job.request.items_per_table,
                  "branches": inventory()["branches"], "sample_only": True},
        "source_rows": job.source_rows, "total": job.total, "processed": len(job.results),
        "complete": counts["complete"], "unresolved": counts["unresolved"], "errors": counts["error"],
        "usage": dict(job.usage),
        "ranked_items": [{**item, "rank": n} for n, item in enumerate(ranked[:job.request.top_k], 1)],
        "unresolved_items": [item for item in job.results if item["status"] != "complete"],
    }


def authorize(run_id: str, secret: str | None) -> ReviewJob:
    sweep()
    job = jobs.get(run_id)
    if job is None or not secret or not secrets.compare_digest(job.secret, secret):
        raise HTTPException(404, "Review not found or expired. Start a new review.")
    return job


@router.post("/runs", status_code=202)
async def start_review(body: ReviewRequest, response: Response,
                       x_openai_key: Annotated[str | None, Header()] = None,
                       x_huggingface_key: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    if not x_openai_key or not x_openai_key.strip():
        raise HTTPException(401, "An OpenAI API key is required.")
    if len(x_openai_key) > 512 or (x_huggingface_key and len(x_huggingface_key) > 512):
        raise HTTPException(400, "Invalid credential length.")
    if set(body.benchmarks) - BENCHMARK_NAMES.keys() or len(set(body.benchmarks)) != len(body.benchmarks):
        raise HTTPException(400, "Choose benchmarks from the demo catalog.")
    if not x_huggingface_key and not get_token():
        raise HTTPException(400, "Hugging Face access to measurement-db is required. Supply a read token.")
    sweep()
    owner = hashlib.sha256(x_openai_key.strip().encode()).hexdigest()
    active = [job for job in jobs.values() if job.finished_at is None]
    if len(active) >= MAX_ACTIVE or any(job.owner_hash == owner for job in active):
        raise HTTPException(429, "A review is already running for this key, or the demo is busy. Try again shortly.")
    if len(jobs) >= MAX_RETAINED:
        raise HTTPException(429, "The demo is at capacity. Please try again later.")
    job = ReviewJob(secrets.token_hex(16), secrets.token_urlsafe(32), owner, body)
    jobs[job.run_id] = job
    job.task = asyncio.create_task(evaluate(job, x_openai_key.strip(), x_huggingface_key))
    return {"run_id": job.run_id, "run_secret": job.secret}


@router.get("/runs/{run_id}")
async def get_review(run_id: str, response: Response,
               x_review_token: Annotated[str | None, Header()] = None) -> dict:
    response.headers["Cache-Control"] = "no-store"
    return public_job(authorize(run_id, x_review_token))


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


def load_sample(body: ReviewRequest, hf_token: str | None) -> tuple[int, list[dict]]:
    data = inventory()
    data["tables"] = [table for table in data["tables"] if table["benchmark"] in body.benchmarks]
    unique: dict[str, dict] = {}
    rows = 0
    for item in iter_items(data, body.items_per_table, token=hf_token):
        rows += 1
        key = item["evidence_hash"]
        if key not in unique:
            unique[key] = {"evidence_hash": key, "evidence": item["evidence"], "sources": []}
        unique[key]["sources"].append(item["source"])
    return rows, list(unique.values())


async def evaluate(job: ReviewJob, api_key: str, hf_token: str | None) -> None:
    try:
        async with asyncio.timeout(MAX_RUN_SECONDS):
            job.source_rows, items = await asyncio.to_thread(load_sample, job.request, hf_token)
            hf_token = None
            job.total = len(items)
            if not items:
                job.status, job.message = "failed", "The selected sample has no evaluation items."
                return
            job.status, job.message = "running", "Assessing all six validity dimensions for each item."
            async with AsyncOpenAI(api_key=api_key, base_url="https://api.openai.com/v1",
                                   max_retries=2, timeout=600) as client:
                judge = AsyncJudge(client, job.request.deployment.describe(), PROMPT_PATH.read_text(encoding="utf-8"))
                for item in items:
                    assessment = await judge(item["evidence"])
                    # Keep actionable assessment fields; never expose SDK exceptions
                    # or raw provider responses, which can include credential text.
                    result = {**item, **{key: assessment[key] for key in (
                        "status", "assessment", "overall_score", "response_model", "response_id"
                    ) if key in assessment}}
                    if assessment["status"] == "error":
                        result["error"] = "The model did not return a complete, valid assessment."
                    job.results.append(result)
                    usage = assessment.get("usage") or {}
                    for key in ("input_tokens", "output_tokens"):
                        job.usage[key] += usage.get(key, 0)
                    job.usage["reasoning_tokens"] += (usage.get("output_tokens_details") or {}).get("reasoning_tokens", 0)
                    job.usage["cached_input_tokens"] += (usage.get("input_tokens_details") or {}).get("cached_tokens", 0)
            job.status = "completed"
            job.message = "Sample review complete. Only items with six supported scores are ranked."
    except asyncio.CancelledError:
        job.status, job.message = "cancelled", "Review stopped. Completed assessments are retained."
    except AuthenticationError:
        job.status, job.message = "failed", "OpenAI rejected the API key. Check its access and start a new review."
    except RateLimitError:
        job.status, job.message = "failed", "OpenAI reported a rate or quota limit. Completed assessments are retained."
    except OpenAIError:
        job.status, job.message = "failed", "The OpenAI request failed. Check model access and try again."
    except TimeoutError:
        job.status, job.message = "failed", "The review reached its one-hour time limit. Completed assessments are retained."
    except Exception:
        job.status = "failed"
        job.message = "Could not finish the review. Check Hugging Face dataset access and try again."
    finally:
        api_key, hf_token = "", None
        job.finished_at = time.monotonic()
