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

# Anchor prompt directory relative to this file so the package works regardless
# of the caller's cwd — avoids fragile os.getcwd() assumptions.
_DIR = Path(__file__).parent / "prompts"


# Read a prompt file verbatim; use this when the template has no placeholders
# or when you need to inspect/log the raw text before rendering.
def load(name: str) -> str:
    """Return the raw contents of prompts/<name>.md."""
    return (_DIR / f"{name}.md").read_text()


# Convenience wrapper that combines load + str.format in one call.
# Prompt files that include literal braces (e.g. JSON schema examples) must
# escape them as {{ / }} so .format() leaves them intact — see module docstring.
def render(name: str, **kwargs) -> str:
    """Load a prompt and substitute `{placeholder}` vars via str.format."""
    return load(name).format(**kwargs)
