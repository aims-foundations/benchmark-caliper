"""FastAPI app for the validity-analyzer website (v0).

Exposes `POST /api/runs` (multipart + SSE) which runs Steps 0–2 of the
pipeline and streams progress events. The user's Anthropic API key arrives
in the `X-Anthropic-Key` header, is held in the request scope only, and is
discarded when the response stream completes. Nothing is persisted that
goes through any other path than `logging_gate.log_step()`.

Hardening applied:
  - Strict security headers on every response (CSP, HSTS, X-Frame-Options,
    Referrer-Policy, X-Content-Type-Options, Permissions-Policy).
  - CORS allowlist limited to configured frontend origins.
  - Request body size capped at 50 MB (matches SECURITY.md).
  - No global state holds keys or user content.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import shutil
import uuid

import yaml
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, AsyncIterator, Awaitable, Callable, Optional

from fastapi import (
    FastAPI,
    File,
    Form,
    Header,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse

from . import (
    active_runs,
    dataset_analysis,
    db,
    email_notify,
    logging_gate,
    mock_anthropic,
    pdf_utils,
    pipeline_assets,
    pipeline_runner,
    quote_registry,
)
from .anthropic_client import WEB_SEARCH_TOOL, call_text_async
from .elicitation import ALLOWED_DIMENSIONS, ParseError, parse as parse_questions
from .sse import format_event


# ---------- configuration ----------

ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "WEBSITE_ALLOWED_ORIGINS", "http://localhost:5173"
    ).split(",")
    if o.strip()
]

MAX_BODY_BYTES = 50 * 1024 * 1024  # 50 MB hard cap (SECURITY.md)
MAX_PDF_BYTES = 32 * 1024 * 1024  # Anthropic's per-document limit
MAX_DESCRIPTION_LEN = 10_000

_PACKAGE_ROOT = (
    Path(__file__).resolve().parent.parent.parent
    / "anthropic_api_package_release"
)
PROMPTS_DIR = _PACKAGE_ROOT / "prompts"

# Put the release package on sys.path so `scripts.repair_scoring_json` (used
# by `_parse_scoring_json` as a structural-repair fallback) is importable
# without each helper having to do its own sys.path dance.
import sys as _sys  # noqa: E402
if str(_PACKAGE_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PACKAGE_ROOT))


# ---------- security headers ----------

SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    ),
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": (
        "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
    ),
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        for name, value in SECURITY_HEADERS.items():
            response.headers[name] = value
        return response


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        cl = request.headers.get("content-length")
        if cl is not None and int(cl) > MAX_BODY_BYTES:
            return Response("request body too large", status_code=413)
        return await call_next(request)


# ---------- app ----------


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    # Refuses to boot if MOCK_ANTHROPIC=1 collides with prod signals.
    mock_anthropic.assert_safe_to_enable()
    if mock_anthropic.is_mock_enabled():
        print(
            "⚠️  MOCK_ANTHROPIC=1 — using fixtures, no real Anthropic calls. "
            f"Fixture dir: {mock_anthropic.fixture_dir()}",
            flush=True,
        )
    db.init_db()
    yield


app = FastAPI(title="Validity Analyzer", version="0.1.0", lifespan=lifespan)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(BodySizeLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,  # we never use cookies for auth
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Anthropic-Key"],
)


# ---------- routes ----------


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/runs")
async def create_run(
    pdf: Annotated[UploadFile, File()],
    deployment_description: Annotated[str, Form()],
    opted_in_full: Annotated[bool, Form()] = False,
    hf_dataset_id: Annotated[Optional[str], Form()] = None,
    hf_config: Annotated[Optional[str], Form()] = None,
    x_anthropic_key: Annotated[
        str | None, Header(alias="X-Anthropic-Key")
    ] = None,
) -> StreamingResponse:
    """Run Steps 0–2 of the pipeline, streaming SSE progress.

    BYOK contract: the key arrives in the `X-Anthropic-Key` header, is
    captured into local scope, and is discarded when the request finishes.
    It is never logged, never written to disk, never echoed in any response.
    """
    if not x_anthropic_key:
        raise HTTPException(401, "missing X-Anthropic-Key header")

    description = deployment_description.strip()
    if not description:
        raise HTTPException(400, "deployment_description is required")
    if len(description) > MAX_DESCRIPTION_LEN:
        raise HTTPException(
            400, f"deployment_description exceeds {MAX_DESCRIPTION_LEN} chars"
        )

    pdf_bytes = await pdf.read()
    if len(pdf_bytes) == 0:
        raise HTTPException(400, "pdf is empty")
    if len(pdf_bytes) > MAX_PDF_BYTES:
        raise HTTPException(
            413, f"pdf exceeds {MAX_PDF_BYTES // (1024 * 1024)} MB"
        )

    try:
        pdf_first_pages = pdf_utils.first_pages(pdf_bytes, n_pages=2)
    except ValueError as e:
        raise HTTPException(400, f"pdf rejected: {e}") from e

    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()
    pdf_pages = pdf_utils.page_count(pdf_bytes)

    # Capture the key in the closure scope of the stream coroutine. When the
    # stream completes (success or error), this binding is the last reference
    # and is collected. No global, no cache.
    api_key = x_anthropic_key
    run_id = str(uuid.uuid4())

    # Stash the PDF bytes + key in the per-run in-memory store so subsequent
    # phases (whether driven step-by-step by the client or in auto-mode by a
    # background task) can read them without re-upload. Cleared on run
    # completion in `_finalize_active_run`. Never written to disk.
    active_runs.store.start(
        run_id=run_id,
        api_key=api_key,
        pdf_bytes=pdf_bytes,
        opted_in_full=opted_in_full,
        deployment_description=description,
        hf_dataset_id=(hf_dataset_id or None),
        hf_config=(hf_config or None),
    )

    async def stream() -> AsyncIterator[str]:
        run_started = datetime.now(timezone.utc)
        logging_gate.start_run(
            run_id=run_id,
            started_at=run_started,
            opted_in_full=opted_in_full,
            pipeline_version="0.2.0",
        )

        try:
            # ---------- Step 0: slug ----------
            yield format_event("step-started", {"step": "0-slug"})
            slug_result = await _call_and_log(
                step="0-slug",
                family="haiku",
                api_key=api_key,
                system=_load_prompt("slug_from_description.md"),
                user=description,
                run_id=run_id,
                opted_in_full=opted_in_full,
                input_text=description,
                max_tokens=64,
            )
            slug = slug_result.text.strip()
            _active = active_runs.store.get(run_id)
            if _active is not None:
                _active.slug = slug
            yield format_event(
                "step-completed",
                {"step": "0-slug", "output": {"slug": slug}},
            )

            # ---------- Step 1: metadata (Haiku, pages 1-2) ----------
            yield format_event("step-started", {"step": "1-metadata"})
            metadata = await _call_and_log(
                step="1-metadata",
                family="haiku",
                api_key=api_key,
                system=_load_prompt("metadata_extract.md"),
                user="Extract metadata from the attached benchmark paper (pages 1-2).",
                pdf_bytes=pdf_first_pages,
                run_id=run_id,
                opted_in_full=opted_in_full,
                input_text=(
                    f"[PDF attachment: sha256={pdf_hash}, pages={pdf_pages}]\n"
                    "Extract metadata from the attached benchmark paper (pages 1-2)."
                ),
                input_hash_override=pdf_hash,
                max_tokens=1024,
            )
            yield format_event(
                "step-completed",
                {"step": "1-metadata", "output": {"metadata": metadata.text}},
            )

            # ---------- Step 2-questions: elicitation ----------
            yield format_event("step-started", {"step": "2-questions"})
            elicit_user = (
                "## Lightweight benchmark metadata\n\n"
                f"{metadata.text}\n\n"
                "## Deployment description\n\n"
                f"{description}\n"
            )
            qresult = await _call_and_log(
                step="2-questions",
                family="sonnet",
                api_key=api_key,
                system=_load_prompt("elicitation_questions.md"),
                user=elicit_user,
                run_id=run_id,
                opted_in_full=opted_in_full,
                input_text=elicit_user,
                max_tokens=2048,
            )
            try:
                questions = parse_questions(qresult.text)
            except ParseError as e:
                raise RuntimeError(f"elicitation parse failed: {e}") from e
            yield format_event(
                "step-completed",
                {
                    "step": "2-questions",
                    "output": {
                        "questions": [q.to_dict() for q in questions],
                        "metadata": metadata.text,
                        "run_id": run_id,
                        "slug": slug,
                    },
                },
            )

            # The run is paused waiting for the user to answer the
            # questions. The /answers endpoint will pick it up and run
            # Step 2-summary.
            logging_gate.set_run_status(run_id, "awaiting_answers")
            yield format_event(
                "awaiting-answers",
                {"run_id": run_id, "slug": slug},
            )
        except Exception as e:
            logging_gate.end_run(
                run_id=run_id,
                status="failed",
                ended_at=datetime.now(timezone.utc),
            )
            # Surface only the exception class — never any provider details.
            yield format_event(
                "error",
                {"error_class": type(e).__name__, "run_id": run_id},
            )

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disable proxy buffering
        },
    )


# ---------- answers endpoint ----------


class _QuestionItem(BaseModel):
    id: str = Field(min_length=1, max_length=10)
    dimension: str
    question: str = Field(min_length=1, max_length=2000)

    @field_validator("dimension")
    @classmethod
    def _check_dimension(cls, v: str) -> str:
        if v not in ALLOWED_DIMENSIONS:
            raise ValueError(
                f"dimension must be one of {sorted(ALLOWED_DIMENSIONS)}"
            )
        return v


class _AnswerItem(BaseModel):
    id: str = Field(min_length=1, max_length=10)
    answer: str = Field(min_length=1, max_length=5000)


_EMAIL_RE = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


class PostAnswersRequest(BaseModel):
    deployment_description: str = Field(min_length=1, max_length=10_000)
    metadata: str = Field(min_length=1, max_length=10_000)
    questions: list[_QuestionItem] = Field(min_length=1, max_length=10)
    answers: list[_AnswerItem] = Field(min_length=1, max_length=10)
    opted_in_full: bool = False
    # When set, the report-ready email is sent to this address at the end
    # of the pipeline (regardless of auto vs step-by-step mode). The
    # address is persisted on the runs row only; never written to tier-3
    # blobs.
    email: Optional[str] = Field(default=None, max_length=320)
    # When `auto_run` is true the client will not drive subsequent phases;
    # the caller should POST /auto-run after this endpoint returns. We do
    # not act on the flag here other than for symmetry / future use.
    auto_run: bool = False

    @field_validator("email")
    @classmethod
    def _check_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        if not _EMAIL_RE.match(v):
            raise ValueError("email is not a valid address")
        return v


@app.post("/api/runs/{run_id}/answers")
async def post_answers(
    run_id: str,
    body: PostAnswersRequest,
    x_anthropic_key: Annotated[
        str | None, Header(alias="X-Anthropic-Key")
    ] = None,
) -> StreamingResponse:
    """Run Step 2-summary on user-supplied answers and stream the result.

    The request is intentionally stateless from the server's perspective:
    the client sends back the metadata, questions, and answers, so the
    server doesn't need a session store. This matches the BYOK ethos —
    the user's data lives with the user.
    """
    if not x_anthropic_key:
        raise HTTPException(401, "missing X-Anthropic-Key header")

    # Verify the run exists and is in the right phase.
    with db.connect() as conn:
        row = conn.execute(
            "SELECT status, user_opted_in_full FROM runs WHERE run_id = ?",
            (run_id,),
        ).fetchone()
    if row is None:
        raise HTTPException(404, "run not found")
    if row["status"] != "awaiting_answers":
        raise HTTPException(
            409,
            f"run is in status {row['status']}, expected awaiting_answers",
        )

    # Per-question answers must match the question set exactly.
    qids = [q.id for q in body.questions]
    aids = {a.id for a in body.answers}
    if set(qids) != aids:
        raise HTTPException(
            400, "every question must have exactly one matching answer"
        )

    # Honour the run's original tier-3 opt-in regardless of what the
    # client passes for this leg — preserves consistency across steps.
    opted_in_full = bool(row["user_opted_in_full"])

    # Persist the email both on the durable run row (so subsequent phases
    # can pick it up) and on the in-memory active_runs entry (so an
    # auto-run background task can grab it without an extra SQL round
    # trip). NULL/empty addresses are no-ops.
    if body.email:
        logging_gate.set_email(run_id, body.email)
        active_runs.store.set_email(run_id, body.email)

    api_key = x_anthropic_key

    user_msg = _build_summary_prompt(
        body.deployment_description, body.metadata, body.questions, body.answers
    )

    async def stream() -> AsyncIterator[str]:
        try:
            yield format_event("step-started", {"step": "2-summary"})
            result = await _call_and_log(
                step="2-summary",
                family="sonnet",
                api_key=api_key,
                system=_load_prompt("elicitation_summary.md"),
                user=user_msg,
                run_id=run_id,
                opted_in_full=opted_in_full,
                input_text=user_msg,
                max_tokens=4096,
            )
            yield format_event(
                "step-completed",
                {
                    "step": "2-summary",
                    "output": {"summary": result.text, "run_id": run_id},
                },
            )

            logging_gate.end_run(
                run_id=run_id,
                status="success",
                ended_at=datetime.now(timezone.utc),
            )
            yield format_event("run-complete", {"run_id": run_id})
        except Exception as e:
            logging_gate.end_run(
                run_id=run_id,
                status="failed",
                ended_at=datetime.now(timezone.utc),
            )
            yield format_event(
                "error",
                {"error_class": type(e).__name__, "run_id": run_id},
            )

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


def _build_summary_prompt(
    description: str,
    metadata: str,
    questions: list[_QuestionItem],
    answers: list[_AnswerItem],
) -> str:
    """Build the user message Step 2-summary's prompt expects."""
    answers_by_id = {a.id: a.answer for a in answers}
    qa_blocks: list[str] = []
    for q in questions:
        n = q.id.lstrip("Q") or q.id
        qa_blocks.append(
            f"{q.id} [{q.dimension}]: {q.question}\nA{n}: {answers_by_id[q.id]}"
        )
    qa_text = "\n\n".join(qa_blocks)
    return (
        "## Deployment description\n\n"
        f"{description}\n\n"
        "## Lightweight benchmark metadata\n\n"
        f"{metadata}\n\n"
        "## Q/A block\n\n"
        f"{qa_text}\n"
    )


# ---------- extract endpoint (Step 3a) ----------


# Cap on concurrent Haiku calls during page fan-out. Anthropic accepts a
# generous default rate; this keeps us friendly to small accounts and
# prevents runaway parallelism on a 100-page PDF.
EXTRACT_CONCURRENCY = 8


@app.post("/api/runs/{run_id}/extract")
async def post_extract(
    run_id: str,
    pdf: Annotated[Optional[UploadFile], File()] = None,
    elicitation_summary: Annotated[str, Form()] = "",
    x_anthropic_key: Annotated[
        str | None, Header(alias="X-Anthropic-Key")
    ] = None,
) -> StreamingResponse:
    """Run Step 3a: parallel per-page Haiku extraction + Sonnet consolidation.

    The PDF is sourced in priority order: (1) a fresh upload on this
    request, (2) the bytes still in `active_runs.store` from the initial
    `/api/runs` upload. Step-by-step clients omit the upload and let the
    server reuse what it already has; legacy clients that re-upload still
    work.

    Streams `step-progress` events as each page completes so the UI can
    show "page X / N".
    """
    if not x_anthropic_key:
        raise HTTPException(401, "missing X-Anthropic-Key header")

    with db.connect() as conn:
        run = conn.execute(
            "SELECT status, user_opted_in_full FROM runs WHERE run_id = ?",
            (run_id,),
        ).fetchone()
    if run is None:
        raise HTTPException(404, "run not found")
    if run["status"] != "success":
        raise HTTPException(
            409,
            f"run is in status {run['status']}, expected success",
        )
    opted_in_full = bool(run["user_opted_in_full"])

    pdf_bytes: bytes
    if pdf is not None:
        pdf_bytes = await pdf.read()
    else:
        active = active_runs.store.get(run_id)
        if active is None or not active.pdf_bytes:
            raise HTTPException(
                400,
                "pdf not provided and no stored copy found for this run",
            )
        pdf_bytes = active.pdf_bytes
    if len(pdf_bytes) == 0:
        raise HTTPException(400, "pdf is empty")
    if len(pdf_bytes) > MAX_PDF_BYTES:
        raise HTTPException(
            413, f"pdf exceeds {MAX_PDF_BYTES // (1024 * 1024)} MB"
        )

    try:
        page_pdfs = pdf_utils.split_pages(pdf_bytes)
    except ValueError as e:
        raise HTTPException(400, f"pdf rejected: {e}") from e

    if not page_pdfs:
        raise HTTPException(400, "pdf has no pages")

    api_key = x_anthropic_key
    extract_prompt_template = _load_prompt("pdf_extract_page.md")
    consolidate_prompt = _load_prompt("pdf_extract_consolidate.md")
    select_prompt = _load_prompt("benchmark_example_selection.md")
    synthesis_prompt = _load_prompt("benchmark_synthesis.md")
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()
    available_examples = pipeline_assets.list_benchmark_examples()
    examples_manifest = pipeline_assets.benchmark_manifest()
    # Elicitation summary is optional — if the run was opted-out the user
    # may not have it. Without it, 3b-synthesize loses some priority hints
    # but the YAML still synthesizes correctly.
    elicitation_text = elicitation_summary.strip()

    async def stream() -> AsyncIterator[str]:
        logging_gate.set_run_status(run_id, "extracting")

        try:
            # Step 3a-extract: fan out across pages.
            yield format_event(
                "step-started",
                {"step": "3a-extract", "total": len(page_pdfs)},
            )

            sem = asyncio.Semaphore(EXTRACT_CONCURRENCY)
            page_extracts: list[
                quote_registry.PageExtract | None
            ] = [None] * len(page_pdfs)

            async def extract_one(
                idx: int, page_bytes: bytes
            ) -> tuple[int, str]:
                async with sem:
                    page_num = idx + 1
                    system_prompt = extract_prompt_template.replace(
                        "{page_num}", str(page_num)
                    )
                    page_hash = hashlib.sha256(page_bytes).hexdigest()
                    started = datetime.now(timezone.utc)
                    try:
                        result = await call_text_async(
                            api_key=api_key,
                            family="haiku",
                            system=system_prompt,
                            user="Extract from the attached single-page PDF.",
                            pdf_bytes=page_bytes,
                            max_tokens=2048,
                        )
                    except Exception as e:
                        logging_gate.log_step(
                            run_id=run_id,
                            step_name=f"3a-extract-page-{page_num}",
                            model="haiku",
                            status="failed",
                            started_at=started,
                            latency_ms=0,
                            error_class=type(e).__name__,
                            input_text=f"[per-page PDF: sha256={page_hash}]",
                            input_hash_override=page_hash,
                            opted_in_full=opted_in_full,
                        )
                        raise

                    logging_gate.log_step(
                        run_id=run_id,
                        step_name=f"3a-extract-page-{page_num}",
                        model=result.model,
                        status="success",
                        started_at=started,
                        latency_ms=result.latency_ms,
                        input_tokens=result.input_tokens,
                        output_tokens=result.output_tokens,
                        input_text=f"[per-page PDF: sha256={page_hash}]",
                        output_text=result.text,
                        input_hash_override=page_hash,
                        opted_in_full=opted_in_full,
                    )
                    return idx, result.text

            tasks = [
                asyncio.create_task(extract_one(i, p))
                for i, p in enumerate(page_pdfs)
            ]
            completed = 0
            try:
                for coro in asyncio.as_completed(tasks):
                    idx, raw = await coro
                    page_extracts[idx] = quote_registry.parse_page_json(
                        raw, page=idx + 1
                    )
                    completed += 1
                    yield format_event(
                        "step-progress",
                        {
                            "step": "3a-extract",
                            "completed": completed,
                            "total": len(page_pdfs),
                        },
                    )
            except Exception:
                # If any page errored, cancel the rest and drain their
                # exceptions before propagating — otherwise asyncio warns
                # "Task exception was never retrieved" for siblings.
                for t in tasks:
                    if not t.done():
                        t.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                raise

            yield format_event("step-completed", {"step": "3a-extract"})

            # Assemble Quote Registry from per-page extracts.
            registry = quote_registry.assemble(
                [e for e in page_extracts if e is not None]
            )

            # Step 3a-consolidate: one Sonnet call.
            yield format_event("step-started", {"step": "3a-consolidate"})
            consolidate_user = (
                f"## Pre-assembled Quote Registry\n\n{registry}"
            )
            consolidated = await _call_and_log(
                step="3a-consolidate",
                family="sonnet",
                api_key=api_key,
                system=consolidate_prompt,
                user=consolidate_user,
                run_id=run_id,
                opted_in_full=opted_in_full,
                input_text=consolidate_user,
                input_hash_override=pdf_hash,
                max_tokens=8192,
            )
            paper_summary = consolidated.text

            yield format_event(
                "step-completed",
                {
                    "step": "3a-consolidate",
                    "output": {"paper_summary": paper_summary},
                },
            )

            # ---------- Step 3b-select: Haiku picks ICL examples ----------
            yield format_event("step-started", {"step": "3b-select"})
            select_user = (
                "## Available manifest\n"
                f"{examples_manifest}\n\n"
                "## Paper summary\n"
                f"{paper_summary}\n"
            )
            select_result = await _call_and_log(
                step="3b-select",
                family="haiku",
                api_key=api_key,
                system=select_prompt,
                user=select_user,
                run_id=run_id,
                opted_in_full=opted_in_full,
                input_text=select_user,
                max_tokens=128,
            )
            picked = _parse_example_selection(
                select_result.text, available_examples
            )
            yield format_event(
                "step-completed",
                {
                    "step": "3b-select",
                    "output": {"selected": picked},
                },
            )

            # ---------- Step 3b-synthesize: Sonnet writes the YAML ----------
            yield format_event("step-started", {"step": "3b-synthesize"})
            example_blocks: list[str] = []
            for name in picked:
                try:
                    body = pipeline_assets.load_benchmark_example(name)
                except FileNotFoundError:
                    continue
                example_blocks.append(
                    f"### Reference example: {name}\n\n```yaml\n{body}\n```"
                )
            synth_user_parts = ["## Paper summary\n", paper_summary, "\n"]
            if example_blocks:
                synth_user_parts.append("\n## Reference examples\n\n")
                synth_user_parts.append("\n\n".join(example_blocks))
                synth_user_parts.append("\n")
            if elicitation_text:
                synth_user_parts.append(
                    "\n## Elicitation summary\n\n"
                )
                synth_user_parts.append(elicitation_text)
                synth_user_parts.append("\n")
            synth_user = "".join(synth_user_parts)

            synth_result = await _call_and_log(
                step="3b-synthesize",
                family="sonnet",
                api_key=api_key,
                system=synthesis_prompt,
                user=synth_user,
                run_id=run_id,
                opted_in_full=opted_in_full,
                input_text=synth_user,
                max_tokens=8192,
            )
            benchmark_yaml = synth_result.text
            yield format_event(
                "step-completed",
                {
                    "step": "3b-synthesize",
                    "output": {"benchmark_yaml": benchmark_yaml},
                },
            )

            logging_gate.set_run_status(run_id, "synthesized")
            yield format_event(
                "extract-complete",
                {
                    "run_id": run_id,
                    "page_count": len(page_pdfs),
                    "selected_examples": picked,
                },
            )
        except Exception as e:
            logging_gate.end_run(
                run_id=run_id,
                status="failed",
                ended_at=datetime.now(timezone.utc),
            )
            yield format_event(
                "error",
                {"error_class": type(e).__name__, "run_id": run_id},
            )

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ---------- region endpoint (Steps 4 + 5) ----------


class RegionRequest(BaseModel):
    elicitation_summary: str = Field(min_length=1, max_length=20_000)
    benchmark_yaml: str = Field(min_length=1, max_length=40_000)
    skip_web_search: bool = False


@app.post("/api/runs/{run_id}/region")
async def post_region(
    run_id: str,
    body: RegionRequest,
    x_anthropic_key: Annotated[
        str | None, Header(alias="X-Anthropic-Key")
    ] = None,
) -> StreamingResponse:
    """Run Steps 4a (template select), 4b (region YAML scaffold), and 5
    (web-search enrichment).

    Stateless server pattern: the client sends back the elicitation
    summary and benchmark YAML so we don't need a session store. The run
    must be in `synthesized` status (post-Step-3b).

    Web search is billed by Anthropic at $10/1000 searches in addition
    to normal token costs.
    """
    if not x_anthropic_key:
        raise HTTPException(401, "missing X-Anthropic-Key header")

    with db.connect() as conn:
        run = conn.execute(
            "SELECT status, user_opted_in_full FROM runs WHERE run_id = ?",
            (run_id,),
        ).fetchone()
    if run is None:
        raise HTTPException(404, "run not found")
    if run["status"] != "synthesized":
        raise HTTPException(
            409,
            f"run is in status {run['status']}, expected synthesized",
        )
    opted_in_full = bool(run["user_opted_in_full"])

    api_key = x_anthropic_key
    template_select_prompt = _load_prompt("region_template_selection.md")
    region_synth_prompt = _load_prompt("region_synthesis.md")
    web_search_prompt = _load_prompt("web_search_guide.md")
    available_templates = pipeline_assets.list_region_templates()
    templates_manifest = pipeline_assets.region_manifest()

    async def stream() -> AsyncIterator[str]:
        logging_gate.set_run_status(run_id, "regioning")

        try:
            # ---------- Step 4a: template select ----------
            yield format_event("step-started", {"step": "4a-template"})
            select_user = (
                "## Available templates\n"
                f"{templates_manifest}\n\n"
                "## Elicitation summary (target population fields)\n"
                f"{body.elicitation_summary}\n"
            )
            select_result = await _call_and_log(
                step="4a-template",
                family="haiku",
                api_key=api_key,
                system=template_select_prompt,
                user=select_user,
                run_id=run_id,
                opted_in_full=opted_in_full,
                input_text=select_user,
                max_tokens=128,
            )
            picked = _parse_example_selection(
                select_result.text, available_templates
            )
            yield format_event(
                "step-completed",
                {"step": "4a-template", "output": {"selected": picked}},
            )

            # ---------- Step 4b: region synthesis (no tools) ----------
            yield format_event("step-started", {"step": "4b-synthesize"})
            template_blocks: list[str] = []
            for name in picked:
                try:
                    body_text = pipeline_assets.load_region_template(name)
                except FileNotFoundError:
                    continue
                template_blocks.append(
                    f"### Template: {name}\n\n```yaml\n{body_text}\n```"
                )
            synth_parts = []
            if template_blocks:
                synth_parts.append("## Selected templates\n\n")
                synth_parts.append("\n\n".join(template_blocks))
                synth_parts.append("\n\n")
            synth_parts.append(
                f"## Elicitation summary\n\n{body.elicitation_summary}\n\n"
                f"## Benchmark YAML\n\n```yaml\n{body.benchmark_yaml}\n```\n"
            )
            synth_user = "".join(synth_parts)
            synth_result = await _call_and_log(
                step="4b-synthesize",
                family="sonnet",
                api_key=api_key,
                system=region_synth_prompt,
                user=synth_user,
                run_id=run_id,
                opted_in_full=opted_in_full,
                input_text=synth_user,
                max_tokens=8192,
            )
            scaffold_yaml = synth_result.text
            yield format_event(
                "step-completed",
                {
                    "step": "4b-synthesize",
                    "output": {"region_scaffold": scaffold_yaml},
                },
            )

            # ---------- Step 5: web search enrichment ----------
            if body.skip_web_search:
                yield format_event(
                    "step-completed",
                    {
                        "step": "5-web-search",
                        "output": {
                            "region_yaml": scaffold_yaml,
                            "skipped": True,
                        },
                    },
                )
                final_yaml = scaffold_yaml
            else:
                yield format_event("step-started", {"step": "5-web-search"})
                enrich_user = (
                    "## Region YAML scaffold (from Step 4b)\n\n"
                    f"```yaml\n{scaffold_yaml}\n```\n\n"
                    "## Elicitation summary (for context)\n\n"
                    f"{body.elicitation_summary}\n"
                )
                enrich_result = await _call_and_log(
                    step="5-web-search",
                    family="sonnet",
                    api_key=api_key,
                    system=web_search_prompt,
                    user=enrich_user,
                    run_id=run_id,
                    opted_in_full=opted_in_full,
                    input_text=enrich_user,
                    tools=[WEB_SEARCH_TOOL],
                    max_tokens=8192,
                )
                final_yaml = enrich_result.text
                yield format_event(
                    "step-completed",
                    {
                        "step": "5-web-search",
                        "output": {"region_yaml": final_yaml},
                    },
                )

            logging_gate.set_run_status(run_id, "regioned")
            yield format_event(
                "region-complete",
                {
                    "run_id": run_id,
                    "selected_templates": picked,
                    "web_search_used": not body.skip_web_search,
                },
            )
        except Exception as e:
            logging_gate.end_run(
                run_id=run_id,
                status="failed",
                ended_at=datetime.now(timezone.utc),
            )
            yield format_event(
                "error",
                {"error_class": type(e).__name__, "run_id": run_id},
            )

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ---------- dataset-analysis endpoint (Step 5b) ----------


class DatasetAnalysisRequest(BaseModel):
    benchmark_yaml: str = Field(min_length=1, max_length=40_000)
    elicitation_summary: str = Field(default="", max_length=20_000)
    web_search_text: str = Field(default="", max_length=80_000)
    # Optional explicit overrides. If unset, we look up the benchmark
    # name in `anthropic_api_package_release/benchmarks/hf_links.json`.
    hf_dataset_id: Optional[str] = Field(default=None, max_length=200)
    hf_config: Optional[str] = Field(default=None, max_length=100)
    benchmark_name: Optional[str] = Field(default=None, max_length=200)


@app.post("/api/runs/{run_id}/dataset-analysis")
async def post_dataset_analysis(
    run_id: str,
    body: DatasetAnalysisRequest,
    x_anthropic_key: Annotated[
        str | None, Header(alias="X-Anthropic-Key")
    ] = None,
) -> StreamingResponse:
    """Run Step 5b: HuggingFace dataset analysis (deterministic profiling
    + Sonnet interpretation).

    Sits between Step 5 (web search) and Step 7 (scoring). The returned
    `dataset_analysis_text` is passed to `/score` as
    `dataset_analysis_text`, which the composer pastes into the Opus
    prompt under `## Dataset Analysis Findings`.

    Resolution order matches the CLI's `_resolve_hf_info`: explicit
    `hf_dataset_id` first, then a lookup of `benchmark_name` in
    `hf_links.json`. If nothing resolves we emit a `da-skipped` event
    and return — the client should proceed to `/score` without DA.

    This step can take 3-10 minutes (HF download + sampling +
    Sonnet interpretation). Uvicorn (and any reverse proxy in front
    of it) must allow request timeouts long enough for that.
    """
    if not x_anthropic_key:
        raise HTTPException(401, "missing X-Anthropic-Key header")
    api_key = x_anthropic_key

    with db.connect() as conn:
        run = conn.execute(
            "SELECT status FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
    if run is None:
        raise HTTPException(404, "run not found")
    # The endpoint is callable from `regioned` (post Step 5) through any
    # later status, so we don't gate on status here — the client can
    # rerun DA after scoring if they want.

    async def stream() -> AsyncIterator[str]:
        try:
            yield format_event("step-started", {"step": "5b-resolve"})
            target = await asyncio.to_thread(
                dataset_analysis.resolve_target,
                hf_dataset_id=body.hf_dataset_id,
                hf_config=body.hf_config,
                benchmark_name=body.benchmark_name,
            )
            if target is None:
                yield format_event(
                    "da-skipped",
                    {
                        "run_id": run_id,
                        "reason": (
                            "no hf_dataset_id supplied and benchmark_name "
                            "not in hf_links.json (or dataset requires "
                            "remote code)"
                        ),
                    },
                )
                return
            yield format_event(
                "step-completed",
                {"step": "5b-resolve", "output": {"target": target}},
            )

            # Bridge dataset_analysis's emit callback into this SSE
            # generator via a queue, same pattern used by rerun-scoring.
            queue: asyncio.Queue = asyncio.Queue()

            async def forward(name: str, payload: dict) -> None:
                await queue.put((name, payload))

            async def drive() -> str:
                try:
                    if target["mode"] == "single":
                        text = await dataset_analysis.run_single(
                            api_key=api_key,
                            hf_dataset_id=target["hf_dataset_id"],
                            hf_config=target.get("hf_config"),
                            benchmark_yaml=body.benchmark_yaml,
                            elicitation_summary=body.elicitation_summary,
                            web_search_text=body.web_search_text,
                            emit=forward,
                        )
                    else:
                        text = await dataset_analysis.run_org(
                            api_key=api_key,
                            hf_org=target["hf_org"],
                            benchmark_yaml=body.benchmark_yaml,
                            elicitation_summary=body.elicitation_summary,
                            web_search_text=body.web_search_text,
                            emit=forward,
                        )
                    await queue.put(("__done__", text))
                except Exception as exc:
                    await queue.put(("__error__", exc))

            task = asyncio.create_task(drive())
            da_text: str = ""
            while True:
                item = await queue.get()
                tag = item[0]
                if tag == "__done__":
                    da_text = item[1]
                    break
                if tag == "__error__":
                    raise item[1]
                name, payload = item
                yield format_event(name, payload)
            await task

            yield format_event(
                "da-complete",
                {"run_id": run_id, "dataset_analysis_text": da_text},
            )
        except Exception as e:
            yield format_event(
                "error",
                {"error_class": type(e).__name__, "run_id": run_id},
            )

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ---------- compose-prompt endpoint (Step 6, preview only) ----------


class ComposePromptRequest(BaseModel):
    benchmark_yaml: str = Field(min_length=1, max_length=40_000)
    region_yaml: str = Field(min_length=1, max_length=40_000)
    elicitation_summary: str = Field(min_length=1, max_length=20_000)
    dataset_analysis_text: str = Field(default="", max_length=200_000)


@app.post("/api/runs/{run_id}/compose-prompt")
async def post_compose_prompt(
    run_id: str,
    body: ComposePromptRequest,
) -> dict:
    """Step 6: deterministic Opus-prompt assembly for inspection.

    Step-by-step UI calls this between Step 5 and Step 7 so the user can
    review the full composed prompt before authorizing the Opus call
    (which costs them $1–1.50). No LLM, no Anthropic key required;
    bearer-style auth via the run_id.
    """
    with db.connect() as conn:
        run = conn.execute(
            "SELECT status FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
    if run is None:
        raise HTTPException(404, "run not found")
    if run["status"] != "regioned":
        raise HTTPException(
            409,
            f"run is in status {run['status']}, expected regioned",
        )
    framework_yaml = pipeline_assets.load_framework()
    composed = _compose_score_prompt(
        framework_yaml=framework_yaml,
        benchmark_yaml=body.benchmark_yaml,
        region_yaml=body.region_yaml,
        elicitation_summary=body.elicitation_summary,
        dataset_analysis_text=body.dataset_analysis_text,
    )
    return {"composed_prompt": composed, "run_id": run_id}


# ---------- score endpoint (Steps 6 + 7) ----------


class ScoreRequest(BaseModel):
    paper_summary: str = Field(min_length=1, max_length=200_000)
    benchmark_yaml: str = Field(min_length=1, max_length=40_000)
    region_yaml: str = Field(min_length=1, max_length=40_000)
    elicitation_summary: str = Field(min_length=1, max_length=20_000)
    dataset_analysis_text: str = Field(default="", max_length=200_000)


@app.post("/api/runs/{run_id}/score")
async def post_score(
    run_id: str,
    body: ScoreRequest,
    x_anthropic_key: Annotated[
        str | None, Header(alias="X-Anthropic-Key")
    ] = None,
) -> StreamingResponse:
    """Run Step 7: the single Opus scoring call.

    Step 6 (deterministic prompt assembly) is inlined here as a Python
    string-build — no LLM. Step 7 is the lone Opus call in the entire
    pipeline; everything else is Haiku/Sonnet.
    """
    if not x_anthropic_key:
        raise HTTPException(401, "missing X-Anthropic-Key header")

    with db.connect() as conn:
        run = conn.execute(
            "SELECT status, user_opted_in_full FROM runs WHERE run_id = ?",
            (run_id,),
        ).fetchone()
    if run is None:
        raise HTTPException(404, "run not found")
    if run["status"] != "regioned":
        raise HTTPException(
            409,
            f"run is in status {run['status']}, expected regioned",
        )
    opted_in_full = bool(run["user_opted_in_full"])

    api_key = x_anthropic_key
    framework_yaml = pipeline_assets.load_framework()
    scoring_system = _load_prompt("opus_scoring_framing.md")
    composed = _compose_score_prompt(
        framework_yaml=framework_yaml,
        benchmark_yaml=body.benchmark_yaml,
        region_yaml=body.region_yaml,
        elicitation_summary=body.elicitation_summary,
        dataset_analysis_text=body.dataset_analysis_text,
    )

    async def stream() -> AsyncIterator[str]:
        logging_gate.set_run_status(run_id, "scoring")
        try:
            yield format_event("step-started", {"step": "7-score"})
            result = await _call_and_log(
                step="7-score",
                family="opus",
                api_key=api_key,
                system=scoring_system,
                user=composed,
                run_id=run_id,
                opted_in_full=opted_in_full,
                input_text=composed,
                # Matches anthropic_api_package_release/run_pipeline.py:7_score.
                # 8192 was too small: the 6-dimension schema (per-dim
                # score + justification + strengths + 4 evidence lists +
                # checklist + evidence_map + gaps, plus overall_summary
                # + practical_guidance + remediation_suggestions) is
                # routinely larger and gets truncated mid-JSON.
                max_tokens=32768,
            )
            scoring = _parse_scoring_json(result.text)
            yield format_event(
                "step-completed",
                {
                    "step": "7-score",
                    "output": {
                        "scoring": scoring,
                        "raw": result.text,
                    },
                },
            )

            # ---------- Steps 8 + 9: report.md + review.pdf ----------
            active = active_runs.store.get(run_id)
            deployment_description = (
                active.deployment_description if active is not None else ""
            )
            pipeline_runner.write_tuple_inputs(
                run_id,
                scoring=scoring,
                composed_prompt=composed,
                deployment_description=deployment_description,
                benchmark_yaml=body.benchmark_yaml,
                region_yaml=body.region_yaml,
                dataset_analysis_text=body.dataset_analysis_text,
                pdf_bytes=active.pdf_bytes if active is not None else None,
            )

            yield format_event("step-started", {"step": "8-report"})
            report_md = await asyncio.to_thread(
                pipeline_runner.build_report, run_id, scoring
            )
            yield format_event(
                "step-completed",
                {"step": "8-report", "output": {"report_md": report_md}},
            )

            yield format_event("step-started", {"step": "9-review-pdf"})
            review_path = await asyncio.to_thread(
                pipeline_runner.build_review_pdf, run_id
            )
            yield format_event(
                "step-completed",
                {
                    "step": "9-review-pdf",
                    "output": {
                        "review_pdf_url": f"/api/runs/{run_id}/review.pdf",
                        "bytes": review_path.stat().st_size,
                    },
                },
            )

            logging_gate.end_run(
                run_id=run_id,
                status="success",
                ended_at=datetime.now(timezone.utc),
            )
            # Fire-and-forget the report-ready email if the user provided
            # one upstream. Email failures must not fail the run — the
            # report is still available via /report.
            slug_for_email = _lookup_slug(run_id) or ""
            email_status = await _maybe_send_report_email(
                run_id=run_id,
                slug=slug_for_email,
                scoring=scoring,
                raw_text=result.text,
            )
            active_runs.store.end(run_id)
            yield format_event(
                "run-complete",
                {"run_id": run_id, "email": email_status},
            )
        except Exception as e:
            logging_gate.end_run(
                run_id=run_id,
                status="failed",
                ended_at=datetime.now(timezone.utc),
            )
            active_runs.store.end(run_id)
            yield format_event(
                "error",
                {"error_class": type(e).__name__, "run_id": run_id},
            )

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


def _lookup_slug(run_id: str) -> Optional[str]:
    """Pull the run's slug from the first '0-slug' step's output blob, if any.

    The slug is also held on the active_runs entry while the run is in
    flight, but for completeness we fall back to the SQLite step row.
    Returns None if the slug can't be recovered (e.g. tier-3 blobs were
    not written because the user opted out).
    """
    active = active_runs.store.get(run_id)
    if active is not None and getattr(active, "slug", None):
        return active.slug  # type: ignore[attr-defined]
    return None


async def _maybe_send_report_email(
    *,
    run_id: str,
    slug: str,
    scoring: dict,
    raw_text: str,
) -> dict:
    """Look up the email on the runs row and send if present. Returns a
    small status dict surfaced to the client in `run-complete`.
    """
    with db.connect() as conn:
        row = conn.execute(
            "SELECT email FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
    email = row["email"] if row is not None else None
    if not email:
        return {"requested": False}
    # Resend's Python SDK is synchronous. Run it off the event loop so we
    # don't block streaming responses if the network is slow.
    result = await asyncio.to_thread(
        email_notify.send_report_ready,
        to=email,
        run_id=run_id,
        slug=slug,
        scoring=scoring,
        raw_text=raw_text,
    )
    if result.sent:
        logging_gate.mark_email_sent(run_id, datetime.now(timezone.utc))
    return {
        "requested": True,
        "sent": result.sent,
        "fallback": result.fallback,
        "error": result.error,
    }


def _compose_score_prompt(
    *,
    framework_yaml: str,
    benchmark_yaml: str,
    region_yaml: str,
    elicitation_summary: str,
    dataset_analysis_text: str = "",
) -> str:
    """Step 6: assemble the Opus user message via the CLI's compose_prompt.

    Delegates to `scripts/compose_prompt.compose_prompt` from the release
    package so the website's Opus input is byte-equivalent to the CLI's:
    same instructions header, same scoring-rubric formatting, same web
    source registry extraction from the region dict, same separated quote
    tables. Earlier the website pasted each YAML as a fenced blob, which
    fed Opus the same data in a less structured form.

    Paper-summary content is *not* a separate input here: Step 3b
    (benchmark_synthesis) embeds it into the benchmark YAML as the
    `documentation_excerpts` and `verbatim_quotes` fields, which is what
    the CLI composer reads.
    """
    composer = pipeline_runner._load_release_module(
        "scripts.compose_prompt", "scripts/compose_prompt.py"
    )

    return composer.compose_prompt(
        _parse_yaml_blob(benchmark_yaml),
        _parse_yaml_blob(region_yaml),
        _parse_yaml_blob(framework_yaml),
        elicitation_text=elicitation_summary,
        dataset_analysis_text=dataset_analysis_text,
    )


def _parse_yaml_blob(blob: str) -> dict:
    """Strip an optional ```yaml fence and parse into a dict.

    Sonnet's YAML synthesis steps often wrap the output in code fences;
    `yaml.safe_load` would treat the backticks as a literal string. JSON
    is a valid subset of YAML, so a JSON-formatted region body also
    parses correctly.
    """
    fence = re.search(r"```(?:yaml|json)?\s*\n?(.*?)\n?```", blob, re.DOTALL)
    body = (fence.group(1) if fence else blob).strip()
    try:
        parsed = yaml.safe_load(body)
    except yaml.YAMLError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _parse_scoring_json(raw: str) -> dict:
    """Best-effort JSON parse of Opus output, matching the CLI's two-stage cleanup.

    The 6-dimension scoring schema is ~14k tokens of nested objects, and
    Opus drifts from strict JSON in two predictable ways on a response
    that size: (1) raw newlines/tabs inside long justification strings,
    which `json.loads` rejects unless `strict=False`, and (2) trailing
    commas before `}` / `]`. Strict strategies handle those.

    For deeper malformations (missing closing braces, dangling commas in
    awkward spots), this function falls back to `json_repair.repair_json`
    — the same library `parse_llm_output.py` uses in the CLI pipeline.
    `repair_json` silently re-nests subsequent keys inside the last open
    object when it patches a missing brace, which produces valid JSON
    with the wrong tree structure (e.g. `output_form` ends up inside
    `output_content`). `repair_scoring_json.repair_scoring` is invoked
    on every parsed result to undo that re-nesting — it's a no-op on
    well-formed inputs, so calling it unconditionally is safe.

    Falls back to `{}` only after every strategy fails. The raw text is
    also returned in the SSE event so the frontend can show it for
    manual recovery; the validity report email always includes the raw
    text as a fallback when parsing fails.
    """
    if not raw:
        return {}

    parsed = _strict_parse_scoring(raw)
    if parsed is None:
        parsed = _json_repair_parse_scoring(raw)
    if parsed is None:
        return {}
    return _structural_repair_scoring(parsed)


def _strict_parse_scoring(raw: str) -> Optional[dict]:
    """Cheap strict-ish parsers. Returns dict on success, None on total failure."""
    candidates: list[str] = []
    # Strategy 1: every fenced code block, ```json or bare ```.
    for fence in re.finditer(r"```(?:json)?\s*\n?(.*?)\n?```", raw, re.DOTALL):
        candidates.append(fence.group(1))
    # Strategy 2: the whole text (handles "no prose, no fences" — what we ask for).
    candidates.append(raw)

    decoder = json.JSONDecoder(strict=False)

    for body in candidates:
        body = body.strip()
        if not body:
            continue
        start = body.find("{")
        if start < 0:
            continue
        # Strategy a: raw_decode finds the first complete JSON object
        # from `start`, ignoring anything after. Handles prose suffixes.
        try:
            parsed, _ = decoder.raw_decode(body[start:])
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        # Strategy b: substring from first '{' to last '}', strict=False.
        end = body.rfind("}")
        if end > start:
            substring = body[start : end + 1]
            try:
                parsed = json.loads(substring, strict=False)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
            # Strategy c: also strip trailing commas before } or ].
            sanitized = re.sub(r",(\s*[}\]])", r"\1", substring)
            try:
                parsed = json.loads(sanitized, strict=False)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
    return None


def _json_repair_parse_scoring(raw: str) -> Optional[dict]:
    """Last-resort fallback: coerce malformed JSON via `json_repair`.

    Mirrors the fallback in the CLI's parse_llm_output.py. The caller is
    expected to follow this with _structural_repair_scoring, because
    repair_json patches missing braces by silently re-nesting subsequent
    keys — well-formed JSON, wrong tree.
    """
    try:
        from json_repair import repair_json
    except ImportError:
        return None

    fence = re.search(r"```(?:json)?\s*\n(.*?)\n```", raw, re.DOTALL)
    body = (fence.group(1) if fence else raw).strip()
    start = body.find("{")
    if start < 0:
        return None
    body = body[start:]
    body = re.sub(r",(\s*[}\]])", r"\1", body)
    try:
        parsed = repair_json(body, return_objects=True)
    except Exception:
        return None
    return parsed if isinstance(parsed, dict) else None


def _structural_repair_scoring(parsed: dict) -> dict:
    """Schema-aware unwinding of json_repair's silent re-nesting.

    Wraps `anthropic_api_package_release/scripts/repair_scoring_json.repair_scoring`.
    No-op on clean inputs (idempotent), so safe to call after every successful
    parse.
    """
    try:
        rsj = pipeline_runner._load_release_module(
            "scripts.repair_scoring_json", "scripts/repair_scoring_json.py"
        )
    except (ImportError, FileNotFoundError):
        return parsed
    if not rsj.detect_corruption(parsed):
        return parsed
    repaired, _log = rsj.repair_scoring(parsed)
    return repaired


# ---------- export and delete (data-subject rights) ----------


@app.get("/api/runs/{run_id}/export")
def export_run(run_id: str) -> dict:
    """Return everything we have for one run.

    Includes the run row, all step rows, and the contents of any tier-3
    blobs still on disk. The response is JSON; binary content is not
    expected because PDFs are never stored, only their hashes.

    Auth: the run_id (a UUID4) is the only credential. Anyone holding a
    valid run_id can fetch — that's the same posture as Stripe payment IDs
    and similar opaque resource handles. Documented in DESIGN.md.
    """
    blob_root = logging_gate.DEFAULT_BLOB_ROOT
    with db.connect() as conn:
        run = conn.execute(
            "SELECT * FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
        if run is None:
            raise HTTPException(404, "run not found")
        steps = conn.execute(
            "SELECT * FROM steps WHERE run_id = ? ORDER BY started_at",
            (run_id,),
        ).fetchall()

    blobs: list[dict] = []
    for step in steps:
        if not step["blob_key"]:
            continue
        blob_path = blob_root / step["blob_key"]
        if not blob_path.exists():
            continue
        try:
            blobs.append(
                {
                    "step_name": step["step_name"],
                    "started_at": step["started_at"],
                    "blob_key": step["blob_key"],
                    "content": json.loads(blob_path.read_text()),
                }
            )
        except (OSError, json.JSONDecodeError):
            # Corrupt blob — skip rather than fail the whole export.
            continue

    return {
        "run": dict(run),
        "steps": [dict(s) for s in steps],
        "blobs": blobs,
    }


@app.delete("/api/runs/{run_id}", status_code=204)
def delete_run(run_id: str) -> Response:
    """Hard-delete a run: rows and blobs.

    `steps` rows are removed by cascade (see db.py). The per-run blob
    directory is removed with `shutil.rmtree`. After this call returns,
    no record of the run remains in our system.
    """
    blob_root = logging_gate.DEFAULT_BLOB_ROOT
    with db.connect() as conn:
        existed = conn.execute(
            "SELECT 1 FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
        if existed is None:
            raise HTTPException(404, "run not found")
        conn.execute("DELETE FROM runs WHERE run_id = ?", (run_id,))

    run_dir = blob_root / run_id
    if run_dir.exists():
        shutil.rmtree(run_dir, ignore_errors=True)
    # Step 8/9 workspace lives outside the tier-3 blob root.
    pipeline_runner.reset(run_id, scoring_only=False)

    # Drop the in-memory entry too — key + PDF bytes go out of scope here.
    active_runs.store.end(run_id)

    return Response(status_code=204)


# ---------- admin: post-hoc evidence verification ----------


def _require_admin_token(x_admin_token: Optional[str]) -> None:
    """Gate admin endpoints behind a shared-secret header.

    The token lives in the `WEBSITE_ADMIN_TOKEN` env var. If unset, the
    endpoint returns 503 so a forgotten config doesn't accidentally leave
    admin routes wide open. `secrets.compare_digest` avoids leaking timing
    information about partial matches.
    """
    import secrets

    expected = os.environ.get("WEBSITE_ADMIN_TOKEN", "").strip()
    if not expected:
        raise HTTPException(503, "admin endpoints disabled (WEBSITE_ADMIN_TOKEN unset)")
    if not x_admin_token or not secrets.compare_digest(x_admin_token, expected):
        raise HTTPException(401, "invalid admin token")


@app.post("/api/runs/{run_id}/verify")
async def post_verify_evidence(
    run_id: str,
    skip_web: bool = False,
    skip_hf: bool = False,
    x_admin_token: Annotated[Optional[str], Header(alias="X-Admin-Token")] = None,
) -> dict:
    """Run the release package's evidence verifier on a completed run.

    Wraps `scripts.verify_evidence` from anthropic_api_package_release. Reads
    the per-run workspace at `data/tuples/<run_id>/` (populated by Step 7)
    and runs structural + L1/L2 checks on quotes, web sources, and dataset
    citations. PDF-dependent checks are always skipped because the website
    does not retain the source PDF after extraction.

    Query params:
        skip_web — skip HTTP liveness checks (L2 for web sources)
        skip_hf  — skip HuggingFace re-sampling (L2 for dataset citations)

    Auth: `X-Admin-Token` header must match the `WEBSITE_ADMIN_TOKEN` env var.
    """
    _require_admin_token(x_admin_token)

    workspace = pipeline_runner.workspace_dir(run_id)
    if not (workspace / "scoring.json").exists():
        raise HTTPException(
            404, f"no scoring.json in workspace for run {run_id} (run not completed)"
        )

    try:
        result = await asyncio.to_thread(
            pipeline_runner.verify_evidence,
            run_id,
            skip_web=skip_web,
            skip_hf=skip_hf,
        )
    except Exception as exc:
        raise HTTPException(500, f"verifier crashed: {exc}") from exc

    return result


# ---------- auto-run, events, report (new in v0.3) ----------


class SetEmailRequest(BaseModel):
    email: Optional[str] = Field(default=None, max_length=320)

    @field_validator("email")
    @classmethod
    def _check_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        if not _EMAIL_RE.match(v):
            raise ValueError("email is not a valid address")
        return v


@app.post("/api/runs/{run_id}/email", status_code=204)
def post_email(run_id: str, body: SetEmailRequest) -> Response:
    """Store (or clear) the recipient address for the report-ready email.

    Called by the UI after the user fills in the email-and-mode form
    that follows the elicitation summary. Storing the address is a
    separate step from kicking off the run so the same endpoint serves
    both auto-mode (followed by /auto-run) and step-by-step mode
    (followed by /extract etc.).
    """
    with db.connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(404, "run not found")
    logging_gate.set_email(run_id, body.email)
    active_runs.store.set_email(run_id, body.email)
    return Response(status_code=204)


_FEEDBACK_CATEGORIES = {
    "incorrect_score",
    "hallucination",
    "evidence_mismatch",
    "other",
}


class FeedbackRequest(BaseModel):
    category: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1, max_length=5000)
    contact_email: Optional[str] = Field(default=None, max_length=320)

    @field_validator("category")
    @classmethod
    def _check_category(cls, v: str) -> str:
        v = v.strip()
        if v not in _FEEDBACK_CATEGORIES:
            raise ValueError(
                f"category must be one of: {sorted(_FEEDBACK_CATEGORIES)}"
            )
        return v

    @field_validator("contact_email")
    @classmethod
    def _check_contact(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        if not _EMAIL_RE.match(v):
            raise ValueError("contact_email is not a valid address")
        return v


@app.post("/api/runs/{run_id}/feedback", status_code=201)
async def post_feedback(run_id: str, body: FeedbackRequest) -> dict[str, object]:
    """Record user feedback about an assessment and notify the team.

    The user clicks "Report an issue" after viewing the scoring report. We
    persist the message in the `feedback` table (tier-1 metadata only — no
    paper/PDF contents) and fire an email to FEEDBACK_TO via Resend. Email
    failures are not fatal: the row is committed regardless so feedback is
    never lost to a flaky provider.
    """
    with db.connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(404, "run not found")
        submitted_at = datetime.now(timezone.utc).isoformat()
        cur = conn.execute(
            "INSERT INTO feedback "
            "(run_id, category, message, contact_email, submitted_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                run_id,
                body.category,
                body.message,
                body.contact_email,
                submitted_at,
            ),
        )
        feedback_id = cur.lastrowid

    result = await asyncio.to_thread(
        email_notify.send_feedback_notification,
        run_id=run_id,
        category=body.category,
        message=body.message,
        contact_email=body.contact_email,
    )
    return {
        "feedback_id": feedback_id,
        "notified": result.sent,
        "fallback": result.fallback,
    }


@app.post("/api/runs/{run_id}/auto-run", status_code=202)
async def post_auto_run(run_id: str) -> dict[str, str]:
    """Kick off the pipeline (steps 3a → 7) as a background task.

    The active_runs store holds the BYOK key + PDF bytes, so no header or
    body is needed here — auth is implicit in the unguessable run_id.
    Returns 202 immediately. Progress is observable via `/events`; the
    final report is available via `/report` once the task completes. If
    an email was stored on the runs row, it is sent at the end (success
    only).
    """
    active = active_runs.store.get(run_id)
    if active is None:
        raise HTTPException(404, "no active run with this id")

    with db.connect() as conn:
        row = conn.execute(
            "SELECT status FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(404, "run not found")
    if row["status"] != "success":
        # The run must have completed Step 2-summary first (status=success
        # in the existing schema means "elicitation summary done"). The
        # auto-run picks up from there.
        raise HTTPException(
            409,
            f"run is in status {row['status']}, expected success",
        )

    # Background task survives the response returning. The orchestrator
    # is responsible for marking the run finished and clearing
    # active_runs in all paths.
    asyncio.create_task(_orchestrate_auto_run(run_id))
    return {"status": "started", "run_id": run_id}


@app.get("/api/runs/{run_id}/events")
async def get_events(
    run_id: str,
    last_event_id: Annotated[
        Optional[str], Header(alias="Last-Event-ID")
    ] = None,
) -> StreamingResponse:
    """SSE tail of an in-flight (or just-finished) auto-run.

    Honours the `Last-Event-ID` reconnection header: a client that lost
    its connection mid-stream can resume from the next event after the
    id it last saw, as long as the event is still in the in-memory ring
    buffer. If the run has already finished, the buffered events are
    replayed and the stream closes — `run-complete` / `error` will be
    among them.
    """
    active = active_runs.store.get(run_id)
    if active is None:
        raise HTTPException(404, "no active run with this id")

    last_seq: Optional[int] = None
    if last_event_id is not None:
        try:
            last_seq = int(last_event_id)
        except ValueError:
            last_seq = None

    async def stream() -> AsyncIterator[str]:
        async for ev in active_runs.store.subscribe(run_id, last_seq=last_seq):
            yield format_event(ev.name, ev.payload, event_id=str(ev.seq))

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/runs/{run_id}/report")
def get_report(run_id: str) -> dict:
    """Return the final scoring + slug for the report-landing page.

    Auth: holding the run_id is the only credential, same posture as
    /export. The endpoint reads from the most-recent `7-score` blob if
    it's still on disk (tier-3 opt-in users), or — if the run is still
    in active_runs — from the in-memory artifacts dict (auto-run path).
    Returns 404 if neither source has the score.
    """
    with db.connect() as conn:
        row = conn.execute(
            "SELECT status FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(404, "run not found")

    # Prefer in-memory artifacts (always populated by the auto-run
    # orchestrator; truthful even when tier-3 logging is opted out).
    active = active_runs.store.get(run_id)
    if active is not None and "scoring" in active.artifacts:
        return {
            "run_id": run_id,
            "slug": active.slug or "",
            "scoring": active.artifacts.get("scoring") or {},
            "raw": active.artifacts.get("raw_text") or "",
        }

    # Otherwise try to recover from the 7-score blob if tier-3 is on.
    blob_root = logging_gate.DEFAULT_BLOB_ROOT
    with db.connect() as conn:
        srow = conn.execute(
            "SELECT blob_key FROM steps "
            "WHERE run_id = ? AND step_name = '7-score' AND status = 'success' "
            "ORDER BY started_at DESC LIMIT 1",
            (run_id,),
        ).fetchone()
    if srow is None or not srow["blob_key"]:
        raise HTTPException(404, "no scored output available for this run")
    try:
        blob = json.loads((blob_root / srow["blob_key"]).read_text())
    except (OSError, json.JSONDecodeError) as e:
        raise HTTPException(404, "scored output not readable") from e
    raw = blob.get("output_text") or ""
    return {
        "run_id": run_id,
        "slug": "",
        "scoring": _parse_scoring_json(raw),
        "raw": raw,
    }


# ---------- Step 8 / Step 9 artifact downloads ----------


@app.get("/api/runs/{run_id}/report.md")
def get_report_markdown(run_id: str) -> Response:
    """Return Step 8 report.md (text/markdown)."""
    path = pipeline_runner.report_path(run_id)
    if not path.exists():
        raise HTTPException(404, "report not yet generated")
    return Response(
        content=path.read_bytes(),
        media_type="text/markdown; charset=utf-8",
        headers={
            "Content-Disposition": f'inline; filename="report-{run_id}.md"',
        },
    )


@app.get("/api/runs/{run_id}/review.pdf")
def get_review_pdf(run_id: str) -> Response:
    """Return Step 9 review.pdf (application/pdf)."""
    path = pipeline_runner.review_pdf_path(run_id)
    if not path.exists():
        raise HTTPException(404, "review.pdf not yet generated")
    return Response(
        content=path.read_bytes(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="review-{run_id}.pdf"',
        },
    )


# ---------- rerun endpoints (mirror --rerun-scoring / --rerun-all) ----------


@app.post("/api/runs/{run_id}/rerun-scoring")
async def rerun_scoring(
    run_id: str,
    body: ScoreRequest,
    x_anthropic_key: Annotated[
        str | None, Header(alias="X-Anthropic-Key")
    ] = None,
) -> StreamingResponse:
    """Equivalent of `--rerun-scoring`: wipe scoring.json/report.md/pdfs/
    and re-run Steps 7+8+9 with the same upstream artifacts.

    The client sends the same body as `/score`; the run's status is moved
    back to `regioned` so the scoring stream can run again.
    """
    if not x_anthropic_key:
        raise HTTPException(401, "missing X-Anthropic-Key header")

    with db.connect() as conn:
        run = conn.execute(
            "SELECT status, user_opted_in_full FROM runs WHERE run_id = ?",
            (run_id,),
        ).fetchone()
    if run is None:
        raise HTTPException(404, "run not found")
    opted_in_full = bool(run["user_opted_in_full"])

    pipeline_runner.reset(run_id, scoring_only=True)
    logging_gate.set_run_status(run_id, "regioned")

    api_key = x_anthropic_key
    active = active_runs.store.get(run_id)
    deployment_description = (
        active.deployment_description if active is not None else ""
    )

    async def stream() -> AsyncIterator[str]:
        # _run_score_phase emits via an async callback (designed for the
        # auto-run orchestrator). Bridge those callbacks into our SSE
        # generator via a queue so we can yield them as they happen.
        try:
            queue: asyncio.Queue = asyncio.Queue()

            async def forward(name: str, payload: dict) -> None:
                await queue.put((name, payload))

            async def drive() -> None:
                try:
                    await _run_score_phase(
                        emit=forward,
                        api_key=api_key,
                        run_id=run_id,
                        paper_summary=body.paper_summary,
                        benchmark_yaml=body.benchmark_yaml,
                        region_yaml=body.region_yaml,
                        elicitation_summary=body.elicitation_summary,
                        deployment_description=deployment_description,
                        dataset_analysis_text=body.dataset_analysis_text,
                        opted_in_full=opted_in_full,
                    )
                    await queue.put(None)
                except Exception as exc:
                    await queue.put(("__error__", exc))

            task = asyncio.create_task(drive())
            while True:
                item = await queue.get()
                if item is None:
                    break
                if isinstance(item, tuple) and item[0] == "__error__":
                    raise item[1]
                name, payload = item
                yield format_event(name, payload)
            await task

            logging_gate.end_run(
                run_id=run_id,
                status="success",
                ended_at=datetime.now(timezone.utc),
            )
            yield format_event("run-complete", {"run_id": run_id, "rerun": True})
        except Exception as e:
            logging_gate.end_run(
                run_id=run_id,
                status="failed",
                ended_at=datetime.now(timezone.utc),
            )
            yield format_event(
                "error",
                {"error_class": type(e).__name__, "run_id": run_id},
            )

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/api/runs/{run_id}/rerun-all", status_code=204)
def rerun_all(run_id: str) -> Response:
    """Equivalent of `--rerun-all`: destructively wipe everything for this
    run.

    Mirrors the CLI's behaviour of clearing the assessment directory
    while preserving the run_id itself. The client should treat this as a
    "start over" and re-POST to `/api/runs` (or the step-by-step
    endpoints) to drive a fresh run. DB rows for this run_id are removed
    along with the on-disk workspace.
    """
    blob_root = logging_gate.DEFAULT_BLOB_ROOT
    with db.connect() as conn:
        existed = conn.execute(
            "SELECT 1 FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
        if existed is None:
            raise HTTPException(404, "run not found")
        conn.execute("DELETE FROM runs WHERE run_id = ?", (run_id,))

    run_dir = blob_root / run_id
    if run_dir.exists():
        shutil.rmtree(run_dir, ignore_errors=True)
    pipeline_runner.reset(run_id, scoring_only=False)
    active_runs.store.end(run_id)
    return Response(status_code=204)


# ---------- auto-run orchestrator ----------


# Number of in-memory pipeline assets we read upfront so the orchestrator
# doesn't re-hit the filesystem between phases. Cheap, dozens of KB.
async def _orchestrate_auto_run(run_id: str) -> None:
    """Drive steps 3a → 7 in sequence, emitting events to active_runs.

    Mirrors what `/extract`, `/region`, and `/score` do when driven by the
    client; the difference is the events flow into the in-memory queue
    instead of being yielded out of an SSE response, so the client can
    close its tab and reconnect later (or just wait for the email).
    """
    active = active_runs.store.get(run_id)
    if active is None:
        return

    async def emit(name: str, payload: dict) -> None:
        active.append(name, payload)

    api_key = active.api_key
    pdf_bytes = active.pdf_bytes
    opted_in_full = active.opted_in_full
    elicitation_summary = active.artifacts.get("elicitation_summary", "")
    if not elicitation_summary:
        # Pull from the last 2-summary blob if available (tier-3 only).
        # Otherwise downstream YAML synthesis loses priority hints but
        # still runs.
        elicitation_summary = _load_recent_step_output(
            run_id, "2-summary"
        ) or ""

    try:
        extract_result = await _run_extract_phase(
            emit=emit,
            api_key=api_key,
            run_id=run_id,
            pdf_bytes=pdf_bytes,
            elicitation_summary=elicitation_summary,
            opted_in_full=opted_in_full,
        )
        active.artifacts.update(extract_result)
        region_result = await _run_region_phase(
            emit=emit,
            api_key=api_key,
            run_id=run_id,
            elicitation_summary=elicitation_summary,
            benchmark_yaml=extract_result["benchmark_yaml"],
            opted_in_full=opted_in_full,
            skip_web_search=False,
        )
        active.artifacts.update(region_result)
        da_result = await _run_dataset_analysis_phase(
            emit=emit,
            api_key=api_key,
            run_id=run_id,
            benchmark_yaml=extract_result["benchmark_yaml"],
            elicitation_summary=elicitation_summary,
            web_search_text=region_result.get("region_yaml", ""),
            hf_dataset_id=active.hf_dataset_id,
            hf_config=active.hf_config,
        )
        active.artifacts.update(da_result)
        score_result = await _run_score_phase(
            emit=emit,
            api_key=api_key,
            run_id=run_id,
            paper_summary=extract_result["paper_summary"],
            benchmark_yaml=extract_result["benchmark_yaml"],
            region_yaml=region_result["region_yaml"],
            elicitation_summary=elicitation_summary,
            deployment_description=active.deployment_description,
            dataset_analysis_text=da_result.get("dataset_analysis_text", ""),
            opted_in_full=opted_in_full,
        )
        active.artifacts.update(score_result)
        logging_gate.end_run(
            run_id=run_id,
            status="success",
            ended_at=datetime.now(timezone.utc),
        )
        email_status = await _maybe_send_report_email(
            run_id=run_id,
            slug=active.slug or "",
            scoring=score_result["scoring"],
            raw_text=score_result["raw_text"],
        )
        await emit(
            "run-complete",
            {"run_id": run_id, "email": email_status},
        )
    except Exception as e:
        logging_gate.end_run(
            run_id=run_id,
            status="failed",
            ended_at=datetime.now(timezone.utc),
        )
        await emit(
            "error",
            {"error_class": type(e).__name__, "run_id": run_id},
        )
    finally:
        # The in-memory entry can go now — events queued before this call
        # are still drainable by subscribers because `end` puts a sentinel
        # (None) onto each subscriber queue rather than dropping events
        # already in flight.
        active_runs.store.end(run_id)


def _load_recent_step_output(run_id: str, step_name: str) -> Optional[str]:
    """Best-effort: read the most-recent success blob for a step name.

    Returns None if tier-3 logging is off or the file is missing.
    """
    blob_root = logging_gate.DEFAULT_BLOB_ROOT
    with db.connect() as conn:
        srow = conn.execute(
            "SELECT blob_key FROM steps "
            "WHERE run_id = ? AND step_name = ? AND status = 'success' "
            "ORDER BY started_at DESC LIMIT 1",
            (run_id, step_name),
        ).fetchone()
    if srow is None or not srow["blob_key"]:
        return None
    try:
        blob = json.loads((blob_root / srow["blob_key"]).read_text())
    except (OSError, json.JSONDecodeError):
        return None
    out = blob.get("output_text")
    return out if isinstance(out, str) else None


async def _run_extract_phase(
    *,
    emit: Callable[[str, dict], Awaitable[None]],
    api_key: str,
    run_id: str,
    pdf_bytes: bytes,
    elicitation_summary: str,
    opted_in_full: bool,
) -> dict:
    """Run the four extract sub-steps (3a-extract, 3a-consolidate, 3b-select,
    3b-synthesize). Mirrors the body of `/extract` minus the SSE plumbing.
    """
    logging_gate.set_run_status(run_id, "extracting")
    try:
        page_pdfs = pdf_utils.split_pages(pdf_bytes)
    except ValueError as e:
        raise RuntimeError(f"pdf rejected: {e}") from e
    if not page_pdfs:
        raise RuntimeError("pdf has no pages")

    extract_prompt_template = _load_prompt("pdf_extract_page.md")
    consolidate_prompt = _load_prompt("pdf_extract_consolidate.md")
    select_prompt = _load_prompt("benchmark_example_selection.md")
    synthesis_prompt = _load_prompt("benchmark_synthesis.md")
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()
    available_examples = pipeline_assets.list_benchmark_examples()
    examples_manifest = pipeline_assets.benchmark_manifest()

    await emit(
        "step-started",
        {"step": "3a-extract", "total": len(page_pdfs)},
    )

    sem = asyncio.Semaphore(EXTRACT_CONCURRENCY)
    page_extracts: list[quote_registry.PageExtract | None] = [None] * len(page_pdfs)

    async def extract_one(idx: int, page_bytes: bytes) -> tuple[int, str]:
        async with sem:
            page_num = idx + 1
            system_prompt = extract_prompt_template.replace(
                "{page_num}", str(page_num)
            )
            page_hash = hashlib.sha256(page_bytes).hexdigest()
            started = datetime.now(timezone.utc)
            try:
                result = await call_text_async(
                    api_key=api_key,
                    family="haiku",
                    system=system_prompt,
                    user="Extract from the attached single-page PDF.",
                    pdf_bytes=page_bytes,
                    max_tokens=2048,
                )
            except Exception as e:
                logging_gate.log_step(
                    run_id=run_id,
                    step_name=f"3a-extract-page-{page_num}",
                    model="haiku",
                    status="failed",
                    started_at=started,
                    latency_ms=0,
                    error_class=type(e).__name__,
                    input_text=f"[per-page PDF: sha256={page_hash}]",
                    input_hash_override=page_hash,
                    opted_in_full=opted_in_full,
                )
                raise
            logging_gate.log_step(
                run_id=run_id,
                step_name=f"3a-extract-page-{page_num}",
                model=result.model,
                status="success",
                started_at=started,
                latency_ms=result.latency_ms,
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
                input_text=f"[per-page PDF: sha256={page_hash}]",
                output_text=result.text,
                input_hash_override=page_hash,
                opted_in_full=opted_in_full,
            )
            return idx, result.text

    tasks = [
        asyncio.create_task(extract_one(i, p))
        for i, p in enumerate(page_pdfs)
    ]
    completed = 0
    try:
        for coro in asyncio.as_completed(tasks):
            idx, raw = await coro
            page_extracts[idx] = quote_registry.parse_page_json(
                raw, page=idx + 1
            )
            completed += 1
            await emit(
                "step-progress",
                {
                    "step": "3a-extract",
                    "completed": completed,
                    "total": len(page_pdfs),
                },
            )
    except Exception:
        for t in tasks:
            if not t.done():
                t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        raise

    await emit("step-completed", {"step": "3a-extract"})

    registry = quote_registry.assemble(
        [e for e in page_extracts if e is not None]
    )

    await emit("step-started", {"step": "3a-consolidate"})
    consolidate_user = f"## Pre-assembled Quote Registry\n\n{registry}"
    consolidated = await _call_and_log(
        step="3a-consolidate",
        family="sonnet",
        api_key=api_key,
        system=consolidate_prompt,
        user=consolidate_user,
        run_id=run_id,
        opted_in_full=opted_in_full,
        input_text=consolidate_user,
        input_hash_override=pdf_hash,
        max_tokens=8192,
    )
    paper_summary = consolidated.text
    await emit(
        "step-completed",
        {"step": "3a-consolidate", "output": {"paper_summary": paper_summary}},
    )

    await emit("step-started", {"step": "3b-select"})
    select_user = (
        "## Available manifest\n"
        f"{examples_manifest}\n\n"
        "## Paper summary\n"
        f"{paper_summary}\n"
    )
    select_result = await _call_and_log(
        step="3b-select",
        family="haiku",
        api_key=api_key,
        system=select_prompt,
        user=select_user,
        run_id=run_id,
        opted_in_full=opted_in_full,
        input_text=select_user,
        max_tokens=128,
    )
    picked = _parse_example_selection(select_result.text, available_examples)
    await emit(
        "step-completed",
        {"step": "3b-select", "output": {"selected": picked}},
    )

    await emit("step-started", {"step": "3b-synthesize"})
    example_blocks: list[str] = []
    for name in picked:
        try:
            body_text = pipeline_assets.load_benchmark_example(name)
        except FileNotFoundError:
            continue
        example_blocks.append(
            f"### Reference example: {name}\n\n```yaml\n{body_text}\n```"
        )
    synth_user_parts = ["## Paper summary\n", paper_summary, "\n"]
    if example_blocks:
        synth_user_parts.append("\n## Reference examples\n\n")
        synth_user_parts.append("\n\n".join(example_blocks))
        synth_user_parts.append("\n")
    if elicitation_summary:
        synth_user_parts.append("\n## Elicitation summary\n\n")
        synth_user_parts.append(elicitation_summary)
        synth_user_parts.append("\n")
    synth_user = "".join(synth_user_parts)
    synth_result = await _call_and_log(
        step="3b-synthesize",
        family="sonnet",
        api_key=api_key,
        system=synthesis_prompt,
        user=synth_user,
        run_id=run_id,
        opted_in_full=opted_in_full,
        input_text=synth_user,
        max_tokens=8192,
    )
    benchmark_yaml = synth_result.text
    await emit(
        "step-completed",
        {"step": "3b-synthesize", "output": {"benchmark_yaml": benchmark_yaml}},
    )

    logging_gate.set_run_status(run_id, "synthesized")
    await emit(
        "extract-complete",
        {
            "run_id": run_id,
            "page_count": len(page_pdfs),
            "selected_examples": picked,
        },
    )
    return {
        "paper_summary": paper_summary,
        "benchmark_yaml": benchmark_yaml,
        "page_count": len(page_pdfs),
        "selected_examples": picked,
    }


async def _run_region_phase(
    *,
    emit: Callable[[str, dict], Awaitable[None]],
    api_key: str,
    run_id: str,
    elicitation_summary: str,
    benchmark_yaml: str,
    opted_in_full: bool,
    skip_web_search: bool,
) -> dict:
    """Run Steps 4a, 4b, and (optionally) 5. Mirrors the body of `/region`."""
    logging_gate.set_run_status(run_id, "regioning")
    template_select_prompt = _load_prompt("region_template_selection.md")
    region_synth_prompt = _load_prompt("region_synthesis.md")
    web_search_prompt = _load_prompt("web_search_guide.md")
    available_templates = pipeline_assets.list_region_templates()
    templates_manifest = pipeline_assets.region_manifest()

    await emit("step-started", {"step": "4a-template"})
    select_user = (
        "## Available templates\n"
        f"{templates_manifest}\n\n"
        "## Elicitation summary (target population fields)\n"
        f"{elicitation_summary}\n"
    )
    select_result = await _call_and_log(
        step="4a-template",
        family="haiku",
        api_key=api_key,
        system=template_select_prompt,
        user=select_user,
        run_id=run_id,
        opted_in_full=opted_in_full,
        input_text=select_user,
        max_tokens=128,
    )
    picked = _parse_example_selection(select_result.text, available_templates)
    await emit(
        "step-completed",
        {"step": "4a-template", "output": {"selected": picked}},
    )

    await emit("step-started", {"step": "4b-synthesize"})
    template_blocks: list[str] = []
    for name in picked:
        try:
            body_text = pipeline_assets.load_region_template(name)
        except FileNotFoundError:
            continue
        template_blocks.append(
            f"### Template: {name}\n\n```yaml\n{body_text}\n```"
        )
    synth_parts: list[str] = []
    if template_blocks:
        synth_parts.append("## Selected templates\n\n")
        synth_parts.append("\n\n".join(template_blocks))
        synth_parts.append("\n\n")
    synth_parts.append(
        f"## Elicitation summary\n\n{elicitation_summary}\n\n"
        f"## Benchmark YAML\n\n```yaml\n{benchmark_yaml}\n```\n"
    )
    synth_user = "".join(synth_parts)
    synth_result = await _call_and_log(
        step="4b-synthesize",
        family="sonnet",
        api_key=api_key,
        system=region_synth_prompt,
        user=synth_user,
        run_id=run_id,
        opted_in_full=opted_in_full,
        input_text=synth_user,
        max_tokens=8192,
    )
    scaffold_yaml = synth_result.text
    await emit(
        "step-completed",
        {"step": "4b-synthesize", "output": {"region_scaffold": scaffold_yaml}},
    )

    if skip_web_search:
        await emit(
            "step-completed",
            {
                "step": "5-web-search",
                "output": {"region_yaml": scaffold_yaml, "skipped": True},
            },
        )
        final_yaml = scaffold_yaml
    else:
        await emit("step-started", {"step": "5-web-search"})
        enrich_user = (
            "## Region YAML scaffold (from Step 4b)\n\n"
            f"```yaml\n{scaffold_yaml}\n```\n\n"
            "## Elicitation summary (for context)\n\n"
            f"{elicitation_summary}\n"
        )
        enrich_result = await _call_and_log(
            step="5-web-search",
            family="sonnet",
            api_key=api_key,
            system=web_search_prompt,
            user=enrich_user,
            run_id=run_id,
            opted_in_full=opted_in_full,
            input_text=enrich_user,
            tools=[WEB_SEARCH_TOOL],
            max_tokens=8192,
        )
        final_yaml = enrich_result.text
        await emit(
            "step-completed",
            {"step": "5-web-search", "output": {"region_yaml": final_yaml}},
        )

    logging_gate.set_run_status(run_id, "regioned")
    await emit(
        "region-complete",
        {
            "run_id": run_id,
            "selected_templates": picked,
            "web_search_used": not skip_web_search,
        },
    )
    return {
        "region_yaml": final_yaml,
        "scaffold_yaml": scaffold_yaml,
        "selected_templates": picked,
        "web_search_used": not skip_web_search,
    }


async def _run_dataset_analysis_phase(
    *,
    emit: Callable[[str, dict], Awaitable[None]],
    api_key: str,
    run_id: str,
    benchmark_yaml: str,
    elicitation_summary: str,
    web_search_text: str,
    hf_dataset_id: Optional[str],
    hf_config: Optional[str],
) -> dict:
    """Run Step 5b (HF dataset analysis) for the auto-run orchestrator.

    Skips silently if no HF target resolves — auto-mode without an HF
    dataset behaves exactly as before this feature landed. Returns a
    dict containing `dataset_analysis_text` (empty string when skipped)
    that `_run_score_phase` pastes into the Opus prompt.
    """
    benchmark_name: Optional[str] = None
    # Best-effort extract of `name:` from the synthesized benchmark YAML
    # so we can look it up in hf_links.json. The YAML is small enough
    # that a regex is fine here.
    match = re.search(r"^name:\s*(\S+)", benchmark_yaml, flags=re.MULTILINE)
    if match:
        benchmark_name = match.group(1).strip('"').strip("'")

    target = await asyncio.to_thread(
        dataset_analysis.resolve_target,
        hf_dataset_id=hf_dataset_id,
        hf_config=hf_config,
        benchmark_name=benchmark_name,
    )
    if target is None:
        await emit(
            "da-skipped",
            {"run_id": run_id, "reason": "no hf target resolved"},
        )
        return {"dataset_analysis_text": ""}

    await emit(
        "step-started",
        {"step": "5b-resolve", "output": {"target": target}},
    )
    try:
        if target["mode"] == "single":
            text = await dataset_analysis.run_single(
                api_key=api_key,
                hf_dataset_id=target["hf_dataset_id"],
                hf_config=target.get("hf_config"),
                benchmark_yaml=benchmark_yaml,
                elicitation_summary=elicitation_summary,
                web_search_text=web_search_text,
                emit=emit,
            )
        else:
            text = await dataset_analysis.run_org(
                api_key=api_key,
                hf_org=target["hf_org"],
                benchmark_yaml=benchmark_yaml,
                elicitation_summary=elicitation_summary,
                web_search_text=web_search_text,
                emit=emit,
            )
    except Exception as e:
        # DA failures should not abort the whole run — score with what we
        # have. Surface the failure as an event so the client can show
        # "DA skipped (error)" in the UI without losing the rest.
        await emit(
            "da-failed",
            {"run_id": run_id, "error_class": type(e).__name__},
        )
        return {"dataset_analysis_text": ""}

    await emit(
        "da-complete",
        {"run_id": run_id, "dataset_analysis_text": text},
    )
    return {"dataset_analysis_text": text}


async def _run_score_phase(
    *,
    emit: Callable[[str, dict], Awaitable[None]],
    api_key: str,
    run_id: str,
    paper_summary: str,
    benchmark_yaml: str,
    region_yaml: str,
    elicitation_summary: str,
    deployment_description: str,
    dataset_analysis_text: str,
    opted_in_full: bool,
) -> dict:
    """Run Steps 7 (Opus scoring), 8 (report.md), and 9 (review.pdf).

    Mirrors the tail of `/score`. Step 7 is the lone Opus call; Steps 8
    and 9 are deterministic Python (no API) imported from the release
    package via `pipeline_runner`. Step 5b's `dataset_analysis_text`, if
    present, is pasted into the Opus prompt as the CLI does.
    """
    logging_gate.set_run_status(run_id, "scoring")
    framework_yaml = pipeline_assets.load_framework()
    scoring_system = _load_prompt("opus_scoring_framing.md")
    composed = _compose_score_prompt(
        framework_yaml=framework_yaml,
        benchmark_yaml=benchmark_yaml,
        region_yaml=region_yaml,
        elicitation_summary=elicitation_summary,
        dataset_analysis_text=dataset_analysis_text,
    )
    await emit("step-started", {"step": "7-score"})
    result = await _call_and_log(
        step="7-score",
        family="opus",
        api_key=api_key,
        system=scoring_system,
        user=composed,
        run_id=run_id,
        opted_in_full=opted_in_full,
        input_text=composed,
        max_tokens=32768,
    )
    scoring = _parse_scoring_json(result.text)
    await emit(
        "step-completed",
        {"step": "7-score", "output": {"scoring": scoring, "raw": result.text}},
    )

    # ---------- Steps 8 + 9 ----------
    _auto_active = active_runs.store.get(run_id)
    pipeline_runner.write_tuple_inputs(
        run_id,
        scoring=scoring,
        composed_prompt=composed,
        deployment_description=deployment_description,
        benchmark_yaml=benchmark_yaml,
        region_yaml=region_yaml,
        dataset_analysis_text=dataset_analysis_text,
        pdf_bytes=_auto_active.pdf_bytes if _auto_active is not None else None,
    )

    await emit("step-started", {"step": "8-report"})
    report_md = await asyncio.to_thread(
        pipeline_runner.build_report, run_id, scoring
    )
    await emit(
        "step-completed",
        {"step": "8-report", "output": {"report_md": report_md}},
    )

    await emit("step-started", {"step": "9-review-pdf"})
    review_path = await asyncio.to_thread(
        pipeline_runner.build_review_pdf, run_id
    )
    await emit(
        "step-completed",
        {
            "step": "9-review-pdf",
            "output": {
                "review_pdf_url": f"/api/runs/{run_id}/review.pdf",
                "bytes": review_path.stat().st_size,
            },
        },
    )

    return {
        "scoring": scoring,
        "raw_text": result.text,
        "report_md": report_md,
    }


# ---------- helpers ----------


def _load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text()


def _parse_example_selection(raw: str, allowed: list[str]) -> list[str]:
    """Parse the Haiku selection output (a JSON array of filenames) and
    filter against the actual available example list, capping at 2.

    Falls back to an empty list on parse failure or if the model returned
    no valid filenames — the synthesis step then proceeds with no
    reference examples (less ideal output, but does not abort the run).
    """
    fence = re.search(r"```(?:json)?\s*\n(.*?)\n```", raw, re.DOTALL)
    body = fence.group(1).strip() if fence else raw.strip()
    start, end = body.find("["), body.rfind("]")
    if start < 0 or end < start:
        return []
    try:
        items = json.loads(body[start : end + 1])
    except json.JSONDecodeError:
        return []
    if not isinstance(items, list):
        return []
    allowed_set = set(allowed)
    out: list[str] = []
    for x in items:
        if isinstance(x, str) and x in allowed_set and x not in out:
            out.append(x)
        if len(out) >= 2:
            break
    return out


async def _call_and_log(
    *,
    step: str,
    family: str,
    api_key: str,
    system: str,
    user: str,
    run_id: str,
    opted_in_full: bool,
    input_text: str,
    pdf_bytes: bytes | None = None,
    tools: list[dict] | None = None,
    input_hash_override: str | None = None,
    max_tokens: int = 1024,
):
    started = datetime.now(timezone.utc)
    try:
        result = await call_text_async(
            api_key=api_key,
            family=family,
            system=system,
            user=user,
            pdf_bytes=pdf_bytes,
            tools=tools,
            max_tokens=max_tokens,
        )
    except Exception as e:
        logging_gate.log_step(
            run_id=run_id,
            step_name=step,
            model=family,
            status="failed",
            started_at=started,
            latency_ms=0,
            error_class=type(e).__name__,
            input_text=input_text,
            input_hash_override=input_hash_override,
            opted_in_full=opted_in_full,
        )
        raise

    logging_gate.log_step(
        run_id=run_id,
        step_name=step,
        model=result.model,
        status="success",
        started_at=started,
        latency_ms=result.latency_ms,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        input_text=input_text,
        output_text=result.text,
        input_hash_override=input_hash_override,
        opted_in_full=opted_in_full,
    )
    return result
