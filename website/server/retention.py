"""Retention and aggregation cron.

Runs daily. Three responsibilities, each idempotent:

  1. Roll up the previous day's `steps` rows into `daily_aggregates`. The
     aggregates table is small and we keep it forever — it is the basis for
     long-term cost / latency / error-rate trends after tier-3 data is
     purged.

  2. Prune tier-3 blobs older than `retention_days` (default 90). Anthropic
     prompts and responses for those runs cease to exist on our disk after
     this runs.

  3. Reconcile `steps.blob_key` so it does not point to deleted files. This
     is what makes "the blob_key column means the blob exists" hold.

Invoke from a cron job:

    python -m website.server.retention

See website/SECURITY.md item 5 ("Tier 3 retained 90 days, then auto-
deleted") for the verifiable claims this enforces.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from . import db, logging_gate

DEFAULT_RETENTION_DAYS = 90


def aggregate_yesterday(
    *,
    db_path: Optional[Path] = None,
    today: Optional[datetime] = None,
) -> int:
    """Roll up the previous calendar day's `steps` rows into
    `daily_aggregates`, grouped by (date, model, step_name).

    Idempotent — uses INSERT OR REPLACE on the composite primary key.

    Returns the number of (model, step) groups written.
    """
    today_d = (today or datetime.now(timezone.utc)).date()
    yesterday = today_d - timedelta(days=1)
    yesterday_iso = yesterday.isoformat()

    with db.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT
                COALESCE(model, '') AS model,
                step_name,
                COUNT(DISTINCT run_id)                                AS run_count,
                SUM(input_tokens + output_tokens)                     AS total_tokens,
                SUM(cost_usd)                                         AS total_cost_usd,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END)    AS error_count
            FROM steps
            WHERE started_at LIKE ?
            GROUP BY model, step_name
            """,
            (f"{yesterday_iso}%",),
        ).fetchall()

        for r in rows:
            conn.execute(
                """
                INSERT OR REPLACE INTO daily_aggregates
                  (date, model, step_name, run_count, total_tokens,
                   total_cost_usd, error_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    yesterday_iso,
                    r["model"],
                    r["step_name"],
                    r["run_count"],
                    r["total_tokens"] or 0,
                    r["total_cost_usd"] or 0.0,
                    r["error_count"],
                ),
            )
    return len(rows)


def prune_blobs(
    *,
    blob_root: Optional[Path] = None,
    retention_days: int = DEFAULT_RETENTION_DAYS,
    now: Optional[datetime] = None,
) -> int:
    """Delete blob files older than `retention_days`. Empty run-id
    directories are removed too. Returns the count of files removed."""
    effective_root = (
        blob_root if blob_root is not None else logging_gate.DEFAULT_BLOB_ROOT
    )
    if not effective_root.exists():
        return 0

    cutoff_ts = (
        (now or datetime.now(timezone.utc)) - timedelta(days=retention_days)
    ).timestamp()

    removed = 0
    for blob in effective_root.rglob("*.json"):
        if blob.stat().st_mtime < cutoff_ts:
            blob.unlink()
            removed += 1

    # Sweep empty per-run dirs.
    for run_dir in effective_root.iterdir():
        if run_dir.is_dir() and not any(run_dir.iterdir()):
            run_dir.rmdir()

    return removed


def reconcile_blob_keys(
    *,
    db_path: Optional[Path] = None,
    blob_root: Optional[Path] = None,
) -> int:
    """Set `steps.blob_key` to NULL for every step whose blob no longer
    exists on disk. Returns count of rows updated."""
    effective_root = (
        blob_root if blob_root is not None else logging_gate.DEFAULT_BLOB_ROOT
    )
    nulled = 0
    with db.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT run_id, step_name, started_at, blob_key "
            "FROM steps WHERE blob_key IS NOT NULL"
        ).fetchall()
        for r in rows:
            blob_path = effective_root / r["blob_key"]
            if not blob_path.exists():
                conn.execute(
                    "UPDATE steps SET blob_key = NULL "
                    "WHERE run_id = ? AND step_name = ? AND started_at = ?",
                    (r["run_id"], r["step_name"], r["started_at"]),
                )
                nulled += 1
    return nulled


def run_retention(
    *,
    db_path: Optional[Path] = None,
    blob_root: Optional[Path] = None,
    retention_days: int = DEFAULT_RETENTION_DAYS,
    now: Optional[datetime] = None,
) -> dict[str, int]:
    """Run the full retention pass. Idempotent."""
    return {
        "aggregated_groups": aggregate_yesterday(db_path=db_path, today=now),
        "blobs_pruned": prune_blobs(
            blob_root=blob_root, retention_days=retention_days, now=now
        ),
        "blob_keys_nulled": reconcile_blob_keys(
            db_path=db_path, blob_root=blob_root
        ),
    }


def main() -> None:
    """CLI entry. Print the result as JSON for log scrapers."""
    db.init_db()
    result = run_retention()
    json.dump(result, sys.stdout)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
