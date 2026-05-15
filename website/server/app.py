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
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, AsyncIterator

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

from . import db, logging_gate, pdf_utils, pipeline_assets, quote_registry
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

PROMPTS_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "anthropic_api_package"
    / "prompts"
)


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


class PostAnswersRequest(BaseModel):
    deployment_description: str = Field(min_length=1, max_length=10_000)
    metadata: str = Field(min_length=1, max_length=10_000)
    questions: list[_QuestionItem] = Field(min_length=1, max_length=10)
    answers: list[_AnswerItem] = Field(min_length=1, max_length=10)
    opted_in_full: bool = False


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
    pdf: Annotated[UploadFile, File()],
    elicitation_summary: Annotated[str, Form()] = "",
    x_anthropic_key: Annotated[
        str | None, Header(alias="X-Anthropic-Key")
    ] = None,
) -> StreamingResponse:
    """Run Step 3a: parallel per-page Haiku extraction + Sonnet consolidation.

    The user re-uploads their PDF (we don't keep it from the elicitation
    leg). We split it into single-page PDFs, fan out Haiku across pages
    with a small concurrency cap, then assemble a Quote Registry and
    hand it to Sonnet for consolidation.

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

    pdf_bytes = await pdf.read()
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


# ---------- score endpoint (Steps 6 + 7) ----------


class ScoreRequest(BaseModel):
    paper_summary: str = Field(min_length=1, max_length=200_000)
    benchmark_yaml: str = Field(min_length=1, max_length=40_000)
    region_yaml: str = Field(min_length=1, max_length=40_000)
    elicitation_summary: str = Field(min_length=1, max_length=20_000)


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
        paper_summary=body.paper_summary,
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
                # Matches anthropic_api_package/run_pipeline.py:7_score.
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


def _compose_score_prompt(
    *,
    framework_yaml: str,
    benchmark_yaml: str,
    region_yaml: str,
    elicitation_summary: str,
    paper_summary: str,
) -> str:
    """Step 6: deterministic assembly of the Opus user message.

    The existing CLI pipeline's `compose_prompt.py` builds a richer
    structure with separated quote tables; this v0 version pastes each
    artifact as a labelled section and lets Opus parse the markdown. Same
    inputs, slightly less structure — we can refine to match the CLI
    output exactly in a follow-up slice if scoring quality drifts.
    """
    return (
        "I need you to perform a validity analysis of an AI benchmark "
        "for a specific deployment context.\n\n"
        "## Validity framework\n\n"
        "```yaml\n"
        f"{framework_yaml}\n"
        "```\n\n"
        "## Benchmark YAML\n\n"
        "```yaml\n"
        f"{benchmark_yaml}\n"
        "```\n\n"
        "## Regional context YAML\n\n"
        "```yaml\n"
        f"{region_yaml}\n"
        "```\n\n"
        "## Deployment context (elicitation summary)\n\n"
        f"{elicitation_summary}\n\n"
        "## Paper summary (interpretive narrative + verbatim quote registry)\n\n"
        f"{paper_summary}\n\n"
        "Return the scoring as a single valid JSON document, per the rules "
        "in your system prompt. No prose, no fences."
    )


def _parse_scoring_json(raw: str) -> dict:
    """Best-effort JSON parse of Opus output. Falls back to {} if the
    model returned something we can't parse — the raw text is also
    returned in the SSE event so the frontend can show it."""
    fence = re.search(r"```(?:json)?\s*\n(.*?)\n```", raw, re.DOTALL)
    body = fence.group(1).strip() if fence else raw.strip()
    start, end = body.find("{"), body.rfind("}")
    if start < 0 or end < start:
        return {}
    try:
        parsed = json.loads(body[start : end + 1])
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


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

    return Response(status_code=204)


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
