"""In-memory store for the BYOK secrets and PDF bytes of an active run.

Holds, per run_id:
  - the Anthropic API key (so the auto-run background task can keep making
    Anthropic calls after the user's tab closes),
  - the uploaded PDF bytes (so steps 3a/3b don't require the user to
    re-upload between phases),
  - a small ring buffer of progress events + an asyncio.Queue so a freshly
    opened tab can subscribe to the live stream of an in-flight run.

Everything in this module is process-local, in-memory only. The redaction
gate is still the only path to disk; nothing here ever touches the database
or blob store. When `end_run` is called we drop our references to the key
and the PDF bytes so the next GC pass reclaims them.

DESIGN.md §4 has the user-facing description of this tradeoff: the server
holds the key in memory for the run's duration (typically 3-7 minutes) so
that auto-mode runs can complete even if the user navigates away. Memory
holds, not disk holds; the rest of the BYOK contract is unchanged.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import AsyncIterator, Optional


# How long a run may sit idle in the store before the sweeper drops it.
# 1 hour is well past any plausible auto-run duration; it's a safety net,
# not a primary cleanup mechanism (end_run is).
_STALE_AFTER_SECONDS = 60 * 60

# Cap the per-run event buffer. We only keep enough to let a reconnecting
# tab catch up on what it missed; anything older has already been seen.
_MAX_EVENTS_BUFFERED = 256


@dataclass
class _Event:
    seq: int
    name: str
    payload: dict


@dataclass
class ActiveRun:
    run_id: str
    api_key: str
    pdf_bytes: bytes
    opted_in_full: bool
    deployment_description: str = ""
    hf_dataset_id: Optional[str] = None
    hf_config: Optional[str] = None
    created_at: float = field(default_factory=time.monotonic)
    email: Optional[str] = None
    slug: Optional[str] = None
    # Runtime artifacts produced by earlier phases that later phases need:
    # metadata, elicitation_summary, paper_summary, benchmark_yaml,
    # region_yaml, scoring, raw_text. The auto-run orchestrator writes
    # these progressively; /report reads `scoring` + `raw_text` after
    # completion. Never written to disk.
    artifacts: dict = field(default_factory=dict)
    events: list[_Event] = field(default_factory=list)
    next_seq: int = 0
    subscribers: list[asyncio.Queue] = field(default_factory=list)
    finished: bool = False

    def append(self, name: str, payload: dict) -> _Event:
        ev = _Event(seq=self.next_seq, name=name, payload=payload)
        self.next_seq += 1
        self.events.append(ev)
        if len(self.events) > _MAX_EVENTS_BUFFERED:
            # Drop oldest; subscribers that connected fresh will only see
            # what's still buffered. The `seq` value preserves ordering for
            # any reconnect using Last-Event-ID.
            self.events.pop(0)
        for q in self.subscribers:
            # Best-effort fan-out: a slow subscriber should not block us.
            try:
                q.put_nowait(ev)
            except asyncio.QueueFull:
                pass
        return ev


class ActiveRunStore:
    """Process-local map of run_id -> ActiveRun."""

    def __init__(self) -> None:
        self._runs: dict[str, ActiveRun] = {}
        self._lock = asyncio.Lock()

    def start(
        self,
        run_id: str,
        api_key: str,
        pdf_bytes: bytes,
        opted_in_full: bool,
        deployment_description: str = "",
        hf_dataset_id: Optional[str] = None,
        hf_config: Optional[str] = None,
    ) -> ActiveRun:
        run = ActiveRun(
            run_id=run_id,
            api_key=api_key,
            pdf_bytes=pdf_bytes,
            opted_in_full=opted_in_full,
            deployment_description=deployment_description,
            hf_dataset_id=hf_dataset_id,
            hf_config=hf_config,
        )
        self._runs[run_id] = run
        return run

    def get(self, run_id: str) -> Optional[ActiveRun]:
        return self._runs.get(run_id)

    def set_email(self, run_id: str, email: Optional[str]) -> None:
        run = self._runs.get(run_id)
        if run is not None:
            run.email = email

    def end(self, run_id: str) -> None:
        """Drop the run's entry. Key and PDF bytes go out of scope here.

        We intentionally do NOT keep a tombstone with the email or any
        other artifact; once the run is done, this module forgets about
        it. The runs table in SQLite is the only durable record.
        """
        run = self._runs.pop(run_id, None)
        if run is None:
            return
        run.finished = True
        # Wake any subscribers so their generators can exit.
        for q in run.subscribers:
            try:
                q.put_nowait(None)
            except asyncio.QueueFull:
                pass

    def sweep(self, now: Optional[float] = None) -> int:
        """Drop runs older than `_STALE_AFTER_SECONDS`. Returns how many."""
        cutoff = (now if now is not None else time.monotonic()) - _STALE_AFTER_SECONDS
        stale = [
            rid for rid, r in self._runs.items() if r.created_at < cutoff
        ]
        for rid in stale:
            self.end(rid)
        return len(stale)

    async def subscribe(
        self,
        run_id: str,
        last_seq: Optional[int] = None,
    ) -> AsyncIterator[_Event]:
        """Async-iterate events for a run, from `last_seq` exclusive onward.

        Yields buffered events first (so a tab reconnecting after a hiccup
        catches up), then live events as they arrive. Exits when the run
        ends.
        """
        run = self._runs.get(run_id)
        if run is None:
            return
        q: asyncio.Queue = asyncio.Queue(maxsize=128)
        run.subscribers.append(q)

        # Replay buffered events the caller hasn't seen. The queue is attached
        # before replay starts so events appended during replay are not lost.
        replay_from = -1 if last_seq is None else last_seq
        last_replayed = replay_from
        try:
            for ev in list(run.events):
                if ev.seq > replay_from:
                    last_replayed = max(last_replayed, ev.seq)
                    yield ev
            if run.finished:
                return
            while True:
                item = await q.get()
                if item is None:
                    return
                if item.seq <= last_replayed:
                    continue
                yield item
        finally:
            try:
                run.subscribers.remove(q)
            except ValueError:
                pass


# Module-level singleton. FastAPI instantiates the app once per process; the
# store rides along for the process lifetime. Tests may swap it out.
store = ActiveRunStore()
