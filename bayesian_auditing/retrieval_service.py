"""Serve prepared retrieval indexes to the website through authenticated jobs.

Run one Uvicorn worker. Searches share one dedicated thread, so the SQLite
connection stays on its creating thread and full-bank scans never overlap.
There is intentionally no index builder or missing-cache fallback here.
"""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager, closing, suppress
from dataclasses import dataclass, field
import json
import logging
import os
from pathlib import Path
import secrets
import sqlite3
from threading import Event
import time
from typing import Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, ConfigDict, model_validator

from .benchmark_encoding import FullRowBGEEncoder
from .benchmark_index import BenchmarkIndex, _policy
from .data import fingerprint
from .onet import DEFAULT_MATERIALS_DIR, OnetIndex


logger = logging.getLogger(__name__)


class ResultLimitError(ValueError):
    """An operational limit with a safe, service-authored client message."""


class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["onet", "benchmark"]
    query: str
    inventory_hash: str | None = None

    @model_validator(mode="after")
    def validate_search(self):
        if not self.query.strip():
            raise ValueError("Search query must contain non-whitespace text")
        if self.kind == "benchmark" and not self.inventory_hash:
            raise ValueError("Benchmark searches require inventory_hash")
        return self


class PreparedResources:
    """Open existing artifacts and reject an incompatible or unfinished bank."""

    def __init__(self):
        raw_path = os.environ.get("RETRIEVAL_BENCHMARK_INDEX")
        if not raw_path:
            raise RuntimeError("Set RETRIEVAL_BENCHMARK_INDEX to the completed SQLite index")
        path = Path(raw_path).resolve(strict=True)
        if not path.is_file():
            raise ValueError("RETRIEVAL_BENCHMARK_INDEX must be a completed SQLite file")
        threads = int(os.environ.get("RETRIEVAL_CPU_THREADS", "4"))
        if threads < 1:
            raise ValueError("RETRIEVAL_CPU_THREADS must be positive")
        import torch

        torch.set_num_threads(threads)
        encoder = FullRowBGEEncoder(device="cpu")
        with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as connection:
            metadata = {key: json.loads(value) for key, value in connection.execute(
                "SELECT key, value FROM metadata"
            )}
        if metadata.get("complete") is not True:
            raise ValueError("Benchmark cache is incomplete; finish preparation before serving")
        if metadata.get("policy") != _policy(encoder):
            raise ValueError("Prepared benchmark policy does not match the serving encoder")
        inventory = metadata["inventory"]
        expected_key = fingerprint({"inventory": inventory, "policy": metadata["policy"]})
        if metadata.get("cache_key") != expected_key:
            raise ValueError("Prepared benchmark cache identity does not match its inventory and policy")
        self.inventory_hash = fingerprint(inventory)
        self.benchmark = BenchmarkIndex(path, encoder=encoder)
        try:
            self.onet = OnetIndex(materials_dir=os.environ.get(
                "ITEM_REVIEW_ONET_DIR", str(DEFAULT_MATERIALS_DIR),
            ))
            # Keep OnetIndex's standard pinned-model provenance. Passing an
            # injected encoder to its constructor labels the policy "custom".
            self.onet._encoder.device = "cpu"
        except BaseException:
            self.benchmark.close()
            raise

    def health(self):
        return {"ready": True, "inventory_hash": self.inventory_hash,
                "stats": self.benchmark.stats,
                "onet": {"records": self.onet.policy["record_count"]}}

    def search(self, request: SearchRequest, cancelled):
        index = self.benchmark if request.kind == "benchmark" else self.onet
        candidates = index.search(request.query, cancelled=cancelled)
        result = {"candidates": candidates, "policy": index.policy}
        if request.kind == "benchmark":
            result.update(stats=index.stats, inventory_hash=self.inventory_hash)
        return result

    def close(self):
        self.benchmark.close()


@dataclass
class SearchJob:
    request: SearchRequest
    created: float
    job_id: str = field(default_factory=lambda: uuid4().hex)
    status: str = "queued"
    cancelled: Event = field(default_factory=Event)
    result: dict | None = None
    result_bytes: int = 0
    error: str | None = None

    def response(self):
        response = {"job_id": self.job_id, "status": self.status}
        if self.request.kind == "benchmark":
            response["inventory_hash"] = self.request.inventory_hash
        if self.result is not None:
            response["result"] = self.result
        if self.error is not None:
            response["error"] = self.error
        return response


class SearchJobs:
    """Bound pending work and retained results; release them on DELETE or expiry."""

    def __init__(self, resources, executor, *, max_queued=8, max_jobs=32,
                 ttl_seconds=3600, max_result_bytes=64 * 1024**2,
                 max_retained_bytes=256 * 1024**2, clock=time.monotonic):
        if min(max_queued, max_jobs, ttl_seconds, max_result_bytes, max_retained_bytes) <= 0:
            raise ValueError("Retrieval queue, retention, and memory limits must be positive")
        self.resources, self.executor = resources, executor
        self.max_jobs, self.ttl_seconds = max_jobs, ttl_seconds
        self.max_result_bytes, self.max_retained_bytes = max_result_bytes, max_retained_bytes
        self.clock, self.retained_bytes = clock, 0
        self.jobs: dict[str, SearchJob] = {}
        self.queue = asyncio.Queue(maxsize=max_queued)
        self.closing = False
        self.worker = asyncio.create_task(self._work())
        self.cleaner = asyncio.create_task(self._clean())

    def cancel(self, job):
        job.cancelled.set()
        self.retained_bytes -= job.result_bytes
        job.result, job.result_bytes, job.error = None, 0, None
        job.status = "cancelled"

    def expire(self):
        deadline = self.clock() - self.ttl_seconds
        for job_id, job in list(self.jobs.items()):
            if job.created <= deadline:
                self.cancel(job)
                del self.jobs[job_id]

    def submit(self, request):
        self.expire()
        if self.closing:
            raise HTTPException(503, "Retrieval service is shutting down")
        if request.kind == "benchmark" and request.inventory_hash != self.resources.inventory_hash:
            raise HTTPException(409, "Prepared index inventory differs from the requested pinned inventory")
        if len(self.jobs) >= self.max_jobs or self.queue.full():
            raise HTTPException(429, "Retrieval capacity is full; release finished jobs or retry later",
                                headers={"Retry-After": "5"})
        job = SearchJob(request=request, created=self.clock())
        self.jobs[job.job_id] = job
        self.queue.put_nowait(job)
        return job

    def get(self, job_id):
        self.expire()
        if job_id not in self.jobs:
            raise HTTPException(404, "Search does not exist or has expired")
        return self.jobs[job_id]

    def _search(self, job):
        if job.cancelled.is_set():
            raise InterruptedError("Retrieval was cancelled")
        result = self.resources.search(job.request, job.cancelled.is_set)
        size = len(json.dumps(result, ensure_ascii=False, allow_nan=False).encode("utf-8"))
        if size > self.max_result_bytes:
            raise ResultLimitError("Search result exceeds the service's configured retention limit")
        return result, size

    async def _work(self):
        loop = asyncio.get_running_loop()
        while True:
            job = await self.queue.get()
            try:
                if job is None:
                    return
                if job.cancelled.is_set():
                    continue
                job.status = "running"
                try:
                    result, size = await loop.run_in_executor(self.executor, self._search, job)
                    if not job.cancelled.is_set():
                        if self.retained_bytes + size > self.max_retained_bytes:
                            raise ResultLimitError("Retained search results exceed the service's memory limit")
                        job.result, job.result_bytes = result, size
                        self.retained_bytes += size
                        job.status = "completed"
                except InterruptedError:
                    self.cancel(job)
                except Exception as exc:
                    if not job.cancelled.is_set():
                        # Provider errors can embed signed download URLs or
                        # credentials. Do not expose or log their raw messages.
                        category = type(exc).__name__
                        logger.error("Retrieval job %s failed (%s)", job.job_id, category)
                        job.status = "failed"
                        job.error = (str(exc) if isinstance(exc, ResultLimitError) else
                                     f"Retrieval failed ({category}); service job {job.job_id}")
                finally:
                    result = None
            finally:
                self.queue.task_done()
                job = None

    async def _clean(self):
        while True:
            await asyncio.sleep(min(30, self.ttl_seconds))
            self.expire()

    async def close(self):
        self.closing = True
        self.cleaner.cancel()
        with suppress(asyncio.CancelledError):
            await self.cleaner
        for job in self.jobs.values():
            self.cancel(job)
        await self.queue.put(None)
        await self.worker
        self.jobs.clear()


def create_app(*, token=None, resource_factory=PreparedResources, **job_options):
    """Create a service; dependency injection keeps tests offline and inexpensive."""
    configured_token = token

    @asynccontextmanager
    async def lifespan(application):
        nonlocal configured_token
        configured_token = configured_token or os.environ.get("RETRIEVAL_SERVICE_TOKEN", "")
        if len(configured_token) < 32:
            raise RuntimeError("Set RETRIEVAL_SERVICE_TOKEN to a secret with at least 32 characters")
        executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="prepared-retrieval")
        resources = manager = None
        loop = asyncio.get_running_loop()
        try:
            resources = await loop.run_in_executor(executor, resource_factory)
            manager = SearchJobs(resources, executor, **job_options)
            application.state.searches = manager
            application.state.health = resources.health()
            yield
        finally:
            if manager is not None:
                await manager.close()
            if resources is not None:
                await loop.run_in_executor(executor, resources.close)
            executor.shutdown(wait=True, cancel_futures=True)

    async def authenticate(authorization: str | None = Header(default=None)):
        expected = f"Bearer {configured_token}".encode("utf-8")
        if not secrets.compare_digest((authorization or "").encode("utf-8"), expected):
            raise HTTPException(401, "Bearer authentication required", headers={"WWW-Authenticate": "Bearer"})

    application = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None,
                          dependencies=[Depends(authenticate)])

    @application.middleware("http")
    async def prevent_response_caching(request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response

    @application.get("/healthz")
    async def health():
        return application.state.health

    @application.post("/v1/searches", status_code=202)
    async def submit(request: SearchRequest):
        return application.state.searches.submit(request).response()

    @application.get("/v1/searches/{job_id}")
    async def get(job_id: str):
        return application.state.searches.get(job_id).response()

    @application.delete("/v1/searches/{job_id}")
    async def cancel(job_id: str):
        manager = application.state.searches
        job = manager.get(job_id)
        manager.cancel(job)
        del manager.jobs[job_id]
        return job.response()

    return application


app = create_app()
