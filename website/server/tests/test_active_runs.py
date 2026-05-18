"""Tests for the in-memory active-runs store.

The store is the privacy-sensitive helper that holds BYOK keys + PDF
bytes server-side for the duration of an auto-run. The tests below pin
behaviour we care about:

  - start/end is symmetric: end drops the entry so the key + PDF bytes
    become unreachable for GC.
  - subscribe replays buffered events to a late-joining listener, then
    tails live events.
  - the sweeper drops entries older than the TTL.
"""

from __future__ import annotations

import asyncio

import pytest

from website.server import active_runs


@pytest.fixture
def store() -> active_runs.ActiveRunStore:
    return active_runs.ActiveRunStore()


def test_start_then_get(store: active_runs.ActiveRunStore) -> None:
    store.start("r1", api_key="sk-ant-fake", pdf_bytes=b"%PDF-1.4\n", opted_in_full=False)
    got = store.get("r1")
    assert got is not None
    assert got.api_key == "sk-ant-fake"
    assert got.pdf_bytes == b"%PDF-1.4\n"
    assert got.opted_in_full is False
    assert got.email is None


def test_set_email(store: active_runs.ActiveRunStore) -> None:
    store.start("r1", api_key="k", pdf_bytes=b"p", opted_in_full=False)
    store.set_email("r1", "alice@example.org")
    assert store.get("r1").email == "alice@example.org"
    store.set_email("r1", None)
    assert store.get("r1").email is None


def test_end_drops_entry(store: active_runs.ActiveRunStore) -> None:
    store.start("r1", api_key="k", pdf_bytes=b"p", opted_in_full=False)
    store.end("r1")
    assert store.get("r1") is None


def test_end_is_idempotent_on_missing(store: active_runs.ActiveRunStore) -> None:
    store.end("never-existed")  # must not raise


def test_sweeper_drops_stale_entries(store: active_runs.ActiveRunStore) -> None:
    run = store.start("r1", api_key="k", pdf_bytes=b"p", opted_in_full=False)
    # Backdate the run far past the stale threshold.
    run.created_at -= 10_000
    dropped = store.sweep()
    assert dropped == 1
    assert store.get("r1") is None


def test_append_buffers_events(store: active_runs.ActiveRunStore) -> None:
    run = store.start("r1", api_key="k", pdf_bytes=b"p", opted_in_full=False)
    ev = run.append("step-started", {"step": "3a-extract"})
    assert ev.seq == 0
    assert ev.name == "step-started"
    assert ev.payload == {"step": "3a-extract"}
    assert len(run.events) == 1


def test_subscribe_replays_then_tails(store: active_runs.ActiveRunStore) -> None:
    run = store.start("r1", api_key="k", pdf_bytes=b"p", opted_in_full=False)
    run.append("step-started", {"step": "a"})
    run.append("step-completed", {"step": "a"})

    async def go() -> list[str]:
        seen: list[str] = []
        async for ev in store.subscribe("r1"):
            seen.append(ev.name)
            if ev.name == "step-completed":
                # Push one more live event before exiting.
                run.append("run-complete", {"run_id": "r1"})
            if ev.name == "run-complete":
                store.end("r1")
        return seen

    seen = asyncio.run(go())
    assert seen == ["step-started", "step-completed", "run-complete"]


def test_subscribe_resumes_from_last_seq(store: active_runs.ActiveRunStore) -> None:
    run = store.start("r1", api_key="k", pdf_bytes=b"p", opted_in_full=False)
    a = run.append("step-started", {"step": "a"})
    run.append("step-completed", {"step": "a"})

    async def go() -> list[int]:
        seen: list[int] = []
        async for ev in store.subscribe("r1", last_seq=a.seq):
            seen.append(ev.seq)
            if ev.seq >= 1:
                store.end("r1")
        return seen

    seen = asyncio.run(go())
    # The first replayed event has seq > last_seq, so we should NOT see seq 0.
    assert seen == [1]
