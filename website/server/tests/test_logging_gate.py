"""Tests for the redaction gate.

Each test corresponds to a verifiable claim in website/SECURITY.md section 5.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from website.server import db, logging_gate
from website.server.logging_gate import (
    fingerprint,
    log_step,
    redact,
)


# ---------- redact() ----------


def test_redact_strips_api_key() -> None:
    text = "Here is my key: sk-ant-abc123_DEF-XYZ and that's it"
    out = redact(text)
    assert "sk-ant-" not in out
    assert "[REDACTED-KEY]" in out


def test_redact_strips_email() -> None:
    text = "Contact me at user@example.com please"
    out = redact(text)
    assert "@example.com" not in out
    assert "[REDACTED-EMAIL]" in out


def test_redact_strips_phone() -> None:
    text = "Call +1 (555) 123-4567 if you need to"
    out = redact(text)
    assert "555" not in out


def test_redact_is_idempotent() -> None:
    text = "key sk-ant-FOO and email x@y.io"
    once = redact(text)
    twice = redact(once)
    assert once == twice


def test_redact_handles_empty() -> None:
    assert redact("") == ""


def test_redact_strips_multiple_keys() -> None:
    text = "first sk-ant-AAA and second sk-ant-BBB"
    out = redact(text)
    assert "sk-ant-" not in out
    assert out.count("[REDACTED-KEY]") == 2


# ---------- fingerprint() ----------


def test_fingerprint_is_stable() -> None:
    a = fingerprint("hello world")
    b = fingerprint("hello world")
    assert a == b
    assert a is not None
    assert len(a) == 64


def test_fingerprint_differs_for_different_text() -> None:
    assert fingerprint("a") != fingerprint("b")


def test_fingerprint_none_returns_none() -> None:
    assert fingerprint(None) is None


# ---------- log_step ----------


@pytest.fixture
def fresh_db(tmp_path: Path) -> tuple[Path, Path]:
    db_path = tmp_path / "test.db"
    blob_root = tmp_path / "blobs"
    db.init_db(db_path)
    return db_path, blob_root


@pytest.fixture
def started_run(fresh_db: tuple[Path, Path]) -> tuple[str, Path, Path]:
    db_path, blob_root = fresh_db
    run_id = "test-run-1"
    logging_gate.start_run(
        run_id=run_id,
        started_at=datetime.now(timezone.utc),
        opted_in_full=True,
        db_path=db_path,
    )
    return run_id, db_path, blob_root


def test_log_step_writes_tier_1_metadata(
    started_run: tuple[str, Path, Path],
) -> None:
    run_id, db_path, blob_root = started_run
    log_step(
        run_id=run_id,
        step_name="3a-extract",
        model="claude-haiku-4-5",
        status="success",
        started_at=datetime.now(timezone.utc),
        latency_ms=1234,
        input_tokens=1000,
        output_tokens=500,
        db_path=db_path,
        blob_root=blob_root,
    )
    with db.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM steps WHERE run_id = ?", (run_id,)
        ).fetchall()
    assert len(rows) == 1
    row = rows[0]
    assert row["step_name"] == "3a-extract"
    assert row["model"] == "claude-haiku-4-5"
    assert row["input_tokens"] == 1000
    assert row["output_tokens"] == 500
    assert row["cost_usd"] > 0


def test_log_step_does_not_write_blob_when_opted_out(
    fresh_db: tuple[Path, Path],
) -> None:
    db_path, blob_root = fresh_db
    run_id = "opt-out-run"
    logging_gate.start_run(
        run_id=run_id,
        started_at=datetime.now(timezone.utc),
        opted_in_full=False,
        db_path=db_path,
    )
    log_step(
        run_id=run_id,
        step_name="3a-extract",
        model="claude-haiku-4-5",
        status="success",
        started_at=datetime.now(timezone.utc),
        latency_ms=100,
        input_tokens=10,
        output_tokens=5,
        input_text="some input",
        output_text="some output",
        opted_in_full=False,
        db_path=db_path,
        blob_root=blob_root,
    )
    if blob_root.exists():
        assert list(blob_root.rglob("*.json")) == []
    with db.connect(db_path) as conn:
        row = conn.execute(
            "SELECT blob_key, input_hash FROM steps WHERE run_id = ?",
            (run_id,),
        ).fetchone()
    assert row["blob_key"] is None
    # Tier-2 hashes are still recorded even when tier-3 is suppressed.
    assert row["input_hash"] is not None


def test_log_step_writes_blob_when_opted_in(
    started_run: tuple[str, Path, Path],
) -> None:
    run_id, db_path, blob_root = started_run
    log_step(
        run_id=run_id,
        step_name="3a-extract",
        model="claude-haiku-4-5",
        status="success",
        started_at=datetime.now(timezone.utc),
        latency_ms=100,
        input_tokens=10,
        output_tokens=5,
        input_text="hello",
        output_text="world",
        opted_in_full=True,
        db_path=db_path,
        blob_root=blob_root,
    )
    blobs = list(blob_root.rglob("*.json"))
    assert len(blobs) == 1


def test_log_step_blob_never_contains_api_key(
    started_run: tuple[str, Path, Path],
) -> None:
    """SECURITY.md item 5.3: tier 0 (API keys) never written to any store."""
    run_id, db_path, blob_root = started_run
    leaked_key = "sk-ant-LEAKED_VERY_BAD_DO_NOT_STORE_xyz"
    log_step(
        run_id=run_id,
        step_name="3a-extract",
        model="claude-haiku-4-5",
        status="success",
        started_at=datetime.now(timezone.utc),
        latency_ms=100,
        input_tokens=10,
        output_tokens=5,
        input_text=f"my key is {leaked_key} please use it",
        output_text=f"acknowledging key {leaked_key}",
        opted_in_full=True,
        db_path=db_path,
        blob_root=blob_root,
    )
    for blob in blob_root.rglob("*.json"):
        content = blob.read_text()
        assert "sk-ant-" not in content
        assert "LEAKED" not in content


def test_log_step_blob_never_contains_email(
    started_run: tuple[str, Path, Path],
) -> None:
    run_id, db_path, blob_root = started_run
    log_step(
        run_id=run_id,
        step_name="2-elicit",
        model="claude-sonnet-4-6",
        status="success",
        started_at=datetime.now(timezone.utc),
        latency_ms=100,
        input_tokens=10,
        output_tokens=5,
        input_text="email me at user@example.com",
        opted_in_full=True,
        db_path=db_path,
        blob_root=blob_root,
    )
    for blob in blob_root.rglob("*.json"):
        content = blob.read_text()
        assert "user@example.com" not in content


def test_log_step_db_never_contains_api_key(
    started_run: tuple[str, Path, Path],
) -> None:
    """The structured store also must not contain key fragments anywhere."""
    run_id, db_path, blob_root = started_run
    leaked = "sk-ant-LEAKED123"
    log_step(
        run_id=run_id,
        step_name="3a-extract",
        model="claude-haiku-4-5",
        status="success",
        started_at=datetime.now(timezone.utc),
        latency_ms=100,
        input_tokens=10,
        output_tokens=5,
        input_text=leaked,
        output_text=leaked,
        opted_in_full=True,
        db_path=db_path,
        blob_root=blob_root,
    )
    db_bytes = Path(db_path).read_bytes()
    assert b"sk-ant-" not in db_bytes
    assert b"LEAKED" not in db_bytes


def test_log_step_records_hashes_of_inputs(
    started_run: tuple[str, Path, Path],
) -> None:
    run_id, db_path, blob_root = started_run
    log_step(
        run_id=run_id,
        step_name="3a-extract",
        model="claude-haiku-4-5",
        status="success",
        started_at=datetime.now(timezone.utc),
        latency_ms=100,
        input_tokens=10,
        output_tokens=5,
        input_text="hello",
        output_text="world",
        opted_in_full=False,
        db_path=db_path,
        blob_root=blob_root,
    )
    with db.connect(db_path) as conn:
        row = conn.execute(
            "SELECT input_hash, output_hash FROM steps WHERE run_id = ?",
            (run_id,),
        ).fetchone()
    assert row["input_hash"] == fingerprint("hello")
    assert row["output_hash"] == fingerprint("world")


# ---------- end_run rollup ----------


def test_end_run_aggregates_step_totals(
    started_run: tuple[str, Path, Path],
) -> None:
    run_id, db_path, blob_root = started_run
    for i in range(3):
        log_step(
            run_id=run_id,
            step_name=f"step-{i}",
            model="claude-sonnet-4-6",
            status="success",
            started_at=datetime.now(timezone.utc),
            latency_ms=100,
            input_tokens=100,
            output_tokens=50,
            db_path=db_path,
            blob_root=blob_root,
        )
    logging_gate.end_run(
        run_id=run_id,
        status="success",
        ended_at=datetime.now(timezone.utc),
        db_path=db_path,
    )
    with db.connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
    assert row["status"] == "success"
    assert row["total_input_tokens"] == 300
    assert row["total_output_tokens"] == 150
    assert row["total_cost_usd"] > 0
