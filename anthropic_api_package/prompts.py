"""Thin prompt loader.

All prompt text lives in `prompts/*.md`. This module just reads those files
and optionally `.format()`s them. Two helpers:

    load(name)         -> raw contents of prompts/<name>.md
    render(name, **kw) -> load(name).format(**kw)

Prompts that embed literal braces (e.g. JSON schema examples) must escape them
as `{{` / `}}` so `.format()` leaves them intact.
"""

from __future__ import annotations

from pathlib import Path

_DIR = Path(__file__).parent / "prompts"


def load(name: str) -> str:
    """Return the raw contents of prompts/<name>.md."""
    return (_DIR / f"{name}.md").read_text()


def render(name: str, **kwargs) -> str:
    """Load a prompt and substitute `{placeholder}` vars via str.format."""
    return load(name).format(**kwargs)
