"""Tiny SSE (Server-Sent Events) helpers.

We roll our own because the format is trivial and we'd rather not pull in
another dependency. Each event is:

    event: <name>
    data: <json>
    <blank line>
"""

from __future__ import annotations

import json
from typing import Any


def format_event(name: str, payload: Any) -> str:
    """Format one SSE event. The payload is JSON-serialized."""
    body = json.dumps(payload, ensure_ascii=False)
    # SSE requires \n line endings; data lines must not contain newlines.
    body_safe = body.replace("\n", " ")
    return f"event: {name}\ndata: {body_safe}\n\n"
