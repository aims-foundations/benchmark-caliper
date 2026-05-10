"""Tests for the SQLite schema and connection management."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from website.server import db


def test_init_db_creates_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    db.init_db(db_path)
    with db.connect(db_path) as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
    assert {"runs", "steps", "daily_aggregates"}.issubset(tables)


def test_init_db_is_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    db.init_db(db_path)
    db.init_db(db_path)  # second call must not raise


def test_foreign_keys_enforced(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    db.init_db(db_path)
    with pytest.raises(sqlite3.IntegrityError):
        with db.connect(db_path) as conn:
            conn.execute(
                "INSERT INTO steps (run_id, step_name, started_at, status) "
                "VALUES (?, ?, ?, ?)",
                ("nonexistent-run", "step", "2026-01-01T00:00:00", "success"),
            )


def test_connect_commits_on_success(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    db.init_db(db_path)
    with db.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO runs (run_id, started_at, status) VALUES (?, ?, ?)",
            ("r1", "2026-01-01T00:00:00", "in_progress"),
        )
    with db.connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM runs WHERE run_id = ?", ("r1",)
        ).fetchone()
    assert row is not None


def test_connect_rolls_back_on_error(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    db.init_db(db_path)
    with pytest.raises(ValueError):
        with db.connect(db_path) as conn:
            conn.execute(
                "INSERT INTO runs (run_id, started_at, status) VALUES (?, ?, ?)",
                ("r1", "2026-01-01T00:00:00", "in_progress"),
            )
            raise ValueError("simulated error")
    with db.connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM runs WHERE run_id = ?", ("r1",)
        ).fetchone()
    assert row is None
