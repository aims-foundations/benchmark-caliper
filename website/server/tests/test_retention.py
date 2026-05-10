"""Tests for the retention cron.

Each test corresponds to a verifiable claim in website/SECURITY.md item 5
(retention) and DESIGN.md section 5 ("Retention enforcement").
"""

from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from website.server import db, logging_gate, retention


@pytest.fixture
def fresh_db(tmp_path: Path) -> tuple[Path, Path]:
    db_path = tmp_path / "test.db"
    blob_root = tmp_path / "blobs"
    db.init_db(db_path)
    return db_path, blob_root


def _seed_run(db_path: Path, run_id: str, started_at: datetime) -> None:
    logging_gate.start_run(
        run_id=run_id,
        started_at=started_at,
        opted_in_full=True,
        db_path=db_path,
    )


def _seed_step(
    db_path: Path,
    blob_root: Path,
    *,
    run_id: str,
    step_name: str,
    started_at: datetime,
    model: str = "haiku",
    status: str = "success",
    input_tokens: int = 100,
    output_tokens: int = 50,
    write_blob: bool = True,
) -> None:
    logging_gate.log_step(
        run_id=run_id,
        step_name=step_name,
        model=model,
        status=status,
        started_at=started_at,
        latency_ms=100,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        input_text="some text" if write_blob else None,
        output_text="some output" if write_blob else None,
        opted_in_full=write_blob,
        db_path=db_path,
        blob_root=blob_root,
    )


# ---------- aggregate_yesterday ----------


def test_aggregate_yesterday_empty_returns_zero(
    fresh_db: tuple[Path, Path],
) -> None:
    db_path, _ = fresh_db
    n = retention.aggregate_yesterday(db_path=db_path)
    assert n == 0


def test_aggregate_yesterday_groups_by_model_and_step(
    fresh_db: tuple[Path, Path],
) -> None:
    db_path, blob_root = fresh_db
    today = datetime(2026, 5, 6, 12, 0, tzinfo=timezone.utc)
    yesterday = today - timedelta(days=1)

    _seed_run(db_path, "r1", yesterday)
    _seed_step(db_path, blob_root, run_id="r1", step_name="0-slug",
               started_at=yesterday, model="haiku")
    _seed_step(db_path, blob_root, run_id="r1", step_name="1-metadata",
               started_at=yesterday + timedelta(seconds=1), model="haiku")
    _seed_run(db_path, "r2", yesterday)
    _seed_step(db_path, blob_root, run_id="r2", step_name="0-slug",
               started_at=yesterday + timedelta(seconds=2), model="haiku")

    n = retention.aggregate_yesterday(db_path=db_path, today=today)
    assert n == 2  # two (model, step_name) groups

    with db.connect(db_path) as conn:
        rows = {
            (r["step_name"], r["model"]): r
            for r in conn.execute(
                "SELECT * FROM daily_aggregates WHERE date = ?",
                (yesterday.date().isoformat(),),
            )
        }
    assert rows[("0-slug", "haiku")]["run_count"] == 2
    assert rows[("0-slug", "haiku")]["total_tokens"] == 300  # 2 * (100+50)
    assert rows[("1-metadata", "haiku")]["run_count"] == 1


def test_aggregate_yesterday_is_idempotent(
    fresh_db: tuple[Path, Path],
) -> None:
    db_path, blob_root = fresh_db
    today = datetime(2026, 5, 6, 12, 0, tzinfo=timezone.utc)
    yesterday = today - timedelta(days=1)

    _seed_run(db_path, "r1", yesterday)
    _seed_step(db_path, blob_root, run_id="r1", step_name="0-slug",
               started_at=yesterday)

    retention.aggregate_yesterday(db_path=db_path, today=today)
    retention.aggregate_yesterday(db_path=db_path, today=today)

    with db.connect(db_path) as conn:
        rows = list(
            conn.execute(
                "SELECT * FROM daily_aggregates WHERE date = ?",
                (yesterday.date().isoformat(),),
            )
        )
    assert len(rows) == 1
    assert rows[0]["run_count"] == 1


def test_aggregate_yesterday_counts_failed_steps(
    fresh_db: tuple[Path, Path],
) -> None:
    db_path, blob_root = fresh_db
    today = datetime(2026, 5, 6, 12, 0, tzinfo=timezone.utc)
    yesterday = today - timedelta(days=1)

    _seed_run(db_path, "r1", yesterday)
    _seed_step(db_path, blob_root, run_id="r1", step_name="0-slug",
               started_at=yesterday, status="success")
    _seed_step(db_path, blob_root, run_id="r1", step_name="0-slug",
               started_at=yesterday + timedelta(seconds=1), status="failed")
    _seed_step(db_path, blob_root, run_id="r1", step_name="0-slug",
               started_at=yesterday + timedelta(seconds=2), status="failed")

    retention.aggregate_yesterday(db_path=db_path, today=today)

    with db.connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM daily_aggregates WHERE step_name = '0-slug'"
        ).fetchone()
    assert row["error_count"] == 2


# ---------- prune_blobs ----------


def _set_mtime(path: Path, days_ago: int) -> None:
    target = time.time() - days_ago * 86400
    os.utime(path, (target, target))


def test_prune_blobs_keeps_recent_files(
    fresh_db: tuple[Path, Path],
) -> None:
    _, blob_root = fresh_db
    blob_root.mkdir(parents=True, exist_ok=True)
    (blob_root / "r1").mkdir()
    blob = blob_root / "r1" / "step.json"
    blob.write_text("{}")
    # mtime ~now (default)

    n = retention.prune_blobs(blob_root=blob_root, retention_days=90)
    assert n == 0
    assert blob.exists()


def test_prune_blobs_removes_old_files(
    fresh_db: tuple[Path, Path],
) -> None:
    _, blob_root = fresh_db
    blob_root.mkdir(parents=True, exist_ok=True)
    (blob_root / "r1").mkdir()
    old = blob_root / "r1" / "old.json"
    old.write_text("{}")
    _set_mtime(old, days_ago=120)
    new = blob_root / "r1" / "new.json"
    new.write_text("{}")
    _set_mtime(new, days_ago=10)

    n = retention.prune_blobs(blob_root=blob_root, retention_days=90)
    assert n == 1
    assert not old.exists()
    assert new.exists()


def test_prune_blobs_removes_empty_run_dirs(
    fresh_db: tuple[Path, Path],
) -> None:
    _, blob_root = fresh_db
    blob_root.mkdir(parents=True, exist_ok=True)
    run_dir = blob_root / "r1"
    run_dir.mkdir()
    blob = run_dir / "old.json"
    blob.write_text("{}")
    _set_mtime(blob, days_ago=120)

    retention.prune_blobs(blob_root=blob_root, retention_days=90)
    assert not run_dir.exists()


def test_prune_blobs_no_blob_root(tmp_path: Path) -> None:
    n = retention.prune_blobs(
        blob_root=tmp_path / "does-not-exist", retention_days=90
    )
    assert n == 0


# ---------- reconcile_blob_keys ----------


def test_reconcile_nulls_keys_for_missing_blobs(
    fresh_db: tuple[Path, Path],
) -> None:
    db_path, blob_root = fresh_db
    started = datetime.now(timezone.utc)
    _seed_run(db_path, "r1", started)
    _seed_step(db_path, blob_root, run_id="r1", step_name="0-slug",
               started_at=started)

    # Confirm the blob exists and the row points at it
    with db.connect(db_path) as conn:
        row = conn.execute(
            "SELECT blob_key FROM steps WHERE run_id = ?", ("r1",)
        ).fetchone()
    assert row["blob_key"] is not None

    # Wipe the blob
    for f in blob_root.rglob("*.json"):
        f.unlink()

    nulled = retention.reconcile_blob_keys(
        db_path=db_path, blob_root=blob_root
    )
    assert nulled == 1

    with db.connect(db_path) as conn:
        row = conn.execute(
            "SELECT blob_key FROM steps WHERE run_id = ?", ("r1",)
        ).fetchone()
    assert row["blob_key"] is None


def test_reconcile_leaves_keys_for_existing_blobs(
    fresh_db: tuple[Path, Path],
) -> None:
    db_path, blob_root = fresh_db
    started = datetime.now(timezone.utc)
    _seed_run(db_path, "r1", started)
    _seed_step(db_path, blob_root, run_id="r1", step_name="0-slug",
               started_at=started)

    nulled = retention.reconcile_blob_keys(
        db_path=db_path, blob_root=blob_root
    )
    assert nulled == 0


# ---------- end-to-end run_retention ----------


def test_run_retention_end_to_end(fresh_db: tuple[Path, Path]) -> None:
    db_path, blob_root = fresh_db
    today = datetime(2026, 5, 6, 12, 0, tzinfo=timezone.utc)
    yesterday = today - timedelta(days=1)

    _seed_run(db_path, "old", today - timedelta(days=120))
    _seed_step(db_path, blob_root, run_id="old", step_name="0-slug",
               started_at=today - timedelta(days=120))
    # Backdate the old blob's mtime so prune treats it as old
    for f in blob_root.rglob("*.json"):
        _set_mtime(f, days_ago=120)

    _seed_run(db_path, "y", yesterday)
    _seed_step(db_path, blob_root, run_id="y", step_name="0-slug",
               started_at=yesterday)

    result = retention.run_retention(
        db_path=db_path,
        blob_root=blob_root,
        retention_days=90,
        now=today,
    )

    assert result["blobs_pruned"] == 1
    assert result["blob_keys_nulled"] == 1
    assert result["aggregated_groups"] == 1

    # The old run's blob is gone, blob_key NULL'd, but the row survives.
    with db.connect(db_path) as conn:
        old_row = conn.execute(
            "SELECT blob_key FROM steps WHERE run_id = 'old'"
        ).fetchone()
    assert old_row is not None
    assert old_row["blob_key"] is None

    # Recent run's blob is intact.
    with db.connect(db_path) as conn:
        y_row = conn.execute(
            "SELECT blob_key FROM steps WHERE run_id = 'y'"
        ).fetchone()
    assert y_row["blob_key"] is not None