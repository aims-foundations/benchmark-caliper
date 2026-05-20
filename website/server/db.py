"""SQLite storage for pipeline runs (tier 1 + tier 2 + aggregates).

Tier 3 (full content) is stored as filesystem blobs by the redaction gate.
This module knows nothing about tier 3 contents — only about pointers (`blob_key`).

See website/DESIGN.md section 5 for the four-tier model.
"""

from __future__ import annotations

import sqlite3
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

_DEFAULT_DATA_DIR = Path(__file__).resolve().parent / "data"
_DATA_DIR = Path(os.environ.get("WEBSITE_DATA_DIR", str(_DEFAULT_DATA_DIR)))
DEFAULT_DB_PATH = _DATA_DIR / "runs.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
  run_id              TEXT PRIMARY KEY,
  started_at          TEXT NOT NULL,
  ended_at            TEXT,
  status              TEXT NOT NULL,
  total_input_tokens  INTEGER NOT NULL DEFAULT 0,
  total_output_tokens INTEGER NOT NULL DEFAULT 0,
  total_cost_usd      REAL    NOT NULL DEFAULT 0.0,
  pipeline_version    TEXT,
  -- Default 0 (opt-OUT) matches project policy decided 2026-05-04. Code
  -- in logging_gate.start_run always sets this explicitly, so the default
  -- only kicks in for hand-written INSERTs.
  user_opted_in_full  INTEGER NOT NULL DEFAULT 0,
  -- Recipient for the "report ready" email, set when the user submits the
  -- email form after answering elicitation questions. NULL when the user
  -- did not provide one. Cleared by delete-my-data along with the row.
  email               TEXT,
  email_sent_at       TEXT
);

CREATE TABLE IF NOT EXISTS steps (
  run_id        TEXT    NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  step_name     TEXT    NOT NULL,
  model         TEXT,
  started_at    TEXT    NOT NULL,
  latency_ms    INTEGER,
  input_tokens  INTEGER NOT NULL DEFAULT 0,
  output_tokens INTEGER NOT NULL DEFAULT 0,
  cost_usd      REAL    NOT NULL DEFAULT 0.0,
  status        TEXT    NOT NULL,
  error_class   TEXT,
  input_hash    TEXT,
  output_hash   TEXT,
  blob_key      TEXT,
  PRIMARY KEY (run_id, step_name, started_at)
);

CREATE INDEX IF NOT EXISTS idx_steps_run_id     ON steps(run_id);
CREATE INDEX IF NOT EXISTS idx_steps_started_at ON steps(started_at);
CREATE INDEX IF NOT EXISTS idx_runs_started_at  ON runs(started_at);

CREATE TABLE IF NOT EXISTS daily_aggregates (
  date           TEXT    NOT NULL,
  model          TEXT    NOT NULL,
  step_name      TEXT    NOT NULL,
  run_count      INTEGER NOT NULL DEFAULT 0,
  total_tokens   INTEGER NOT NULL DEFAULT 0,
  total_cost_usd REAL    NOT NULL DEFAULT 0.0,
  error_count    INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (date, model, step_name)
);

CREATE TABLE IF NOT EXISTS feedback (
  feedback_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id        TEXT REFERENCES runs(run_id) ON DELETE CASCADE,
  category      TEXT NOT NULL,
  message       TEXT NOT NULL,
  contact_email TEXT,
  submitted_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_feedback_run_id ON feedback(run_id);
"""


def init_db(path: Path | None = None) -> None:
    """Create the schema if it does not already exist. Idempotent.

    Also runs lightweight ADD COLUMN migrations for columns introduced after
    the initial schema (CREATE TABLE IF NOT EXISTS is a no-op on existing
    tables, so we patch new columns in here).
    """
    p = path if path is not None else DEFAULT_DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(p) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SCHEMA)
        _ensure_column(conn, "runs", "email", "TEXT")
        _ensure_column(conn, "runs", "email_sent_at", "TEXT")


def _ensure_column(
    conn: sqlite3.Connection, table: str, column: str, decl: str
) -> None:
    cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


@contextmanager
def connect(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    """Yield a connection that commits on clean exit and rolls back on error.

    Resolves the default path at call time so monkeypatching `DEFAULT_DB_PATH`
    in tests propagates to callers that omit the argument.
    """
    p = path if path is not None else DEFAULT_DB_PATH
    conn = sqlite3.connect(p)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
