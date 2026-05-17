"""Tiny SSE (Server-Sent Events) helpers.

We roll our own because the format is trivial and we'd rather not pull in
another dependency. Each event is:

    id: <seq>            (optional, supports Last-Event-ID reconnects)
    event: <name>
    data: <json>
    <blank line>
"""

from __future__ import annotations

import json
from typing import Any, Optional


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
