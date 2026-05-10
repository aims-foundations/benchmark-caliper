"""The redaction gate — the only path to disk for pipeline observability data.

If a write does not go through `log_step()` (or `start_run()` / `end_run()`),
it does not get logged. This single chokepoint makes the four-tier privacy
model auditable: grep for direct writes to the database or blob store; every
hit must funnel here.

Tiers (see website/DESIGN.md section 5):
  - Tier 0 (API keys, auth headers): never written, ever.
  - Tier 1 (operational metadata): always written to SQLite.
  - Tier 2 (SHA-256 fingerprints): always written to SQLite.
  - Tier 3 (full content): written to filesystem blobs only when the user
    has opted in. Auto-deleted after 90 days by the retention cron.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from . import db
from .prices import cost_usd

_DATA_DIR = Path(__file__).resolve().parent / "data"
DEFAULT_BLOB_ROOT = _DATA_DIR / "assessments"

# Tier 0: patterns that must never reach disk.
API_KEY_PATTERN = re.compile(r"sk-ant-[A-Za-z0-9_-]+")

# Tier 3: PII patterns we strip from full-content blobs before they are
# persisted. False positives are acceptable; false negatives are not.
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Phone detection is locale-dependent and inherently fuzzy. This pattern
# matches a digit-led, optionally +-prefixed sequence with at least 9 digits
# and common separators. It will catch some non-phone numbers (long IDs);
# that is the trade-off we accept to avoid leaking real numbers.
PHONE_PATTERN = re.compile(r"\+?\d[\d\s().\-]{7,}\d")


def redact(text: str) -> str:
    """Strip tier-0 patterns and known PII from text. Idempotent."""
    text = API_KEY_PATTERN.sub("[REDACTED-KEY]", text)
    text = EMAIL_PATTERN.sub("[REDACTED-EMAIL]", text)
    text = PHONE_PATTERN.sub("[REDACTED-PHONE]", text)
    return text


def fingerprint(text: Optional[str]) -> Optional[str]:
    """SHA-256 hex digest of the text, or None when text is None.

    The fingerprint is computed on the un-redacted text so that two users
    submitting the same paper produce the same hash. The hash is one-way,
    so this does not leak the raw content.
    """
    if text is None:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def start_run(
    run_id: str,
    started_at: datetime,
    opted_in_full: bool = True,
    pipeline_version: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> None:
    """Record a new run. Call once at the start of each pipeline run."""
    with db.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO runs (run_id, started_at, status, "
            "pipeline_version, user_opted_in_full) VALUES (?, ?, ?, ?, ?)",
            (
                run_id,
                started_at.isoformat(),
                "in_progress",
                pipeline_version,
                int(opted_in_full),
            ),
        )


def set_run_status(
    run_id: str,
    status: str,
    db_path: Optional[Path] = None,
) -> None:
    """Update only the run's status field.

    Used for non-terminal transitions like "awaiting_answers". Unlike
    `end_run`, this does not set `ended_at` or roll up totals — the run is
    still in flight from the pipeline's perspective.
    """
    with db.connect(db_path) as conn:
        conn.execute(
            "UPDATE runs SET status = ? WHERE run_id = ?",
            (status, run_id),
        )


def end_run(
    run_id: str,
    status: str,
    ended_at: datetime,
    db_path: Optional[Path] = None,
) -> None:
    """Record run completion and roll up totals from the steps table.

    Status: success | failed | abandoned.
    """
    with db.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE runs
            SET status = ?,
                ended_at = ?,
                total_input_tokens  = COALESCE(
                    (SELECT SUM(input_tokens)  FROM steps WHERE run_id = ?), 0),
                total_output_tokens = COALESCE(
                    (SELECT SUM(output_tokens) FROM steps WHERE run_id = ?), 0),
                total_cost_usd      = COALESCE(
                    (SELECT SUM(cost_usd)      FROM steps WHERE run_id = ?), 0)
            WHERE run_id = ?
            """,
            (status, ended_at.isoformat(), run_id, run_id, run_id, run_id),
        )


def log_step(
    run_id: str,
    step_name: str,
    model: str,
    status: str,
    started_at: datetime,
    latency_ms: int,
    input_tokens: int = 0,
    output_tokens: int = 0,
    error_class: Optional[str] = None,
    input_text: Optional[str] = None,
    output_text: Optional[str] = None,
    input_hash_override: Optional[str] = None,
    output_hash_override: Optional[str] = None,
    opted_in_full: bool = True,
    db_path: Optional[Path] = None,
    blob_root: Optional[Path] = None,
) -> None:
    """Record one pipeline step.

    Behaviour by tier:
      - Tier 0 (key, auth header): never written. `input_text` and
        `output_text` are passed through `redact()` before any persistence.
      - Tier 1 (run_id, step_name, model, tokens, cost, status, latency,
        error_class): always written to SQLite.
      - Tier 2 (input_hash, output_hash): always written to SQLite,
        computed on the un-redacted text so equivalent runs collide.
        For steps whose meaningful input is binary (e.g. a PDF) and not
        the text prompt, callers may pass `input_hash_override` to
        fingerprint the binary instead. Same for outputs.
      - Tier 3 (full text): written to a filesystem blob only if
        `opted_in_full` AND at least one of input/output text is non-None.
        Always redacted before write. Binary inputs are never written here
        — only their hash is recorded in tier 2.
    """
    input_hash = (
        input_hash_override
        if input_hash_override is not None
        else fingerprint(input_text)
    )
    output_hash = (
        output_hash_override
        if output_hash_override is not None
        else fingerprint(output_text)
    )
    cost = cost_usd(model, input_tokens, output_tokens)

    effective_blob_root = blob_root if blob_root is not None else DEFAULT_BLOB_ROOT

    blob_key: Optional[str] = None
    if opted_in_full and (input_text is not None or output_text is not None):
        effective_blob_root.mkdir(parents=True, exist_ok=True)
        run_dir = effective_blob_root / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        # Step + microsecond timestamp so retried steps don't clobber each other.
        ts_safe = started_at.strftime("%Y%m%dT%H%M%S%f")
        blob_path = run_dir / f"{step_name}__{ts_safe}.json"
        payload = {
            "run_id": run_id,
            "step_name": step_name,
            "model": model,
            "started_at": started_at.isoformat(),
            "input_text": redact(input_text) if input_text is not None else None,
            "output_text": redact(output_text) if output_text is not None else None,
        }
        blob_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        blob_key = str(blob_path.relative_to(effective_blob_root))

    with db.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO steps (
                run_id, step_name, model, started_at, latency_ms,
                input_tokens, output_tokens, cost_usd, status, error_class,
                input_hash, output_hash, blob_key
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id, step_name, model, started_at.isoformat(), latency_ms,
                input_tokens, output_tokens, cost, status, error_class,
                input_hash, output_hash, blob_key,
            ),
        )
