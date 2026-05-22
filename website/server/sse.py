"""Tiny SSE (Server-Sent Events) helpers.

We roll our own because the format is trivial and we'd rather not pull in
another dependency. Each event is:

    id: <seq>            (optional, supports Last-Event-ID reconnects)
    event: <name>
    data: <json>
    <blank line>
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, AsyncIterator, Optional

# How often to emit a heartbeat while an SSE stream is otherwise idle.
KEEPALIVE_INTERVAL = 15.0


async def with_keepalive(
    events: AsyncIterator[str], interval: float = KEEPALIVE_INTERVAL
) -> AsyncIterator[str]:
    """Wrap an SSE event generator, emitting a comment heartbeat whenever
    it goes quiet for `interval` seconds.

    The longest pipeline steps — the Opus scoring call, web-search
    enrichment, dataset analysis — produce no events for minutes. With no
    traffic on the connection, proxies between the browser and the
    backend drop it as idle, and the step's result is lost. A
    `: keepalive` comment line is ignored by the SSE client (it carries
    no `event:`) but keeps the connection from going idle.
    """
    queue: asyncio.Queue = asyncio.Queue()
    done = object()

    async def _drain() -> None:
        try:
            async for item in events:
                await queue.put(item)
        except Exception as exc:  # surface generator errors to the consumer
            await queue.put(exc)
        else:
            await queue.put(done)

    pump = asyncio.create_task(_drain())
    try:
        while True:
            try:
                item = await asyncio.wait_for(queue.get(), timeout=interval)
            except asyncio.TimeoutError:
                yield ": keepalive\n\n"
                continue
            if item is done:
                return
            if isinstance(item, Exception):
                raise item
            yield item
    finally:
        pump.cancel()
        try:
            await pump
        except BaseException:
            pass


def format_event(name: str, payload: Any, event_id: Optional[str] = None) -> str:
    """Format one SSE event. The payload is JSON-serialized.

    When `event_id` is supplied, an `id:` line is emitted so the browser
    will send it back in the `Last-Event-ID` header on reconnect — used
    by the `/events` tail endpoint to resume an in-flight auto-run.
    """
    body = json.dumps(payload, ensure_ascii=False)
    # SSE requires \n line endings; data lines must not contain newlines.
    body_safe = body.replace("\n", " ")
    prefix = f"id: {event_id}\n" if event_id is not None else ""
    return f"{prefix}event: {name}\ndata: {body_safe}\n\n"
