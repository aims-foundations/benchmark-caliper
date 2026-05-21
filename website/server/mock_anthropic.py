"""Replay-from-fixture mode for the Anthropic client (DEV ONLY).

When `MOCK_ANTHROPIC=1` is set in the environment, every `call_text_async()`
invocation short-circuits to a fixture lookup instead of hitting Anthropic.
This lets you click through the website end-to-end for free during UI work.

Never enable in production. `assert_safe_to_enable()` refuses to boot if any
environment signal looks like a real deployment (ENV=production, non-local
CORS origins). The default-off pattern (`os.getenv(...) == "1"`) means an
unset, empty, or typo'd variable leaves real mode on.

Fixtures come from one already-paid assessment under
`anthropic_api_package_release/assessments/`. Override the source directory
with `MOCK_ANTHROPIC_FIXTURE=/abs/path/to/<expert>__<benchmark>/<slug>`.

If a new pipeline step is added, the dispatcher will raise loudly on the
first call with an unknown prompt prefix — silent empty responses would be
much worse for debugging.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Callable

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_FIXTURE = (
    _REPO_ROOT
    / "anthropic_api_package_release"
    / "assessments"
    / "expert_1a429e941728__mathdial"
    / "india_urban_english_tutoring"
)


def is_mock_enabled() -> bool:
    return os.getenv("MOCK_ANTHROPIC") == "1"


def fixture_dir() -> Path:
    override = os.getenv("MOCK_ANTHROPIC_FIXTURE")
    return Path(override) if override else _DEFAULT_FIXTURE


def assert_safe_to_enable() -> None:
    """Refuse to boot the server if mock + prod signals are both present."""
    if not is_mock_enabled():
        return

    env = (os.getenv("ENV") or os.getenv("ENVIRONMENT") or "").lower()
    if env in ("production", "prod", "staging"):
        raise RuntimeError(
            f"MOCK_ANTHROPIC=1 but ENV={env!r} looks like a real deployment. "
            "Refusing to start. Unset MOCK_ANTHROPIC before deploying."
        )

    origins_raw = os.getenv("WEBSITE_ALLOWED_ORIGINS", "")
    non_local = [
        o.strip()
        for o in origins_raw.split(",")
        if o.strip() and "localhost" not in o and "127.0.0.1" not in o
    ]
    if non_local:
        raise RuntimeError(
            "MOCK_ANTHROPIC=1 but WEBSITE_ALLOWED_ORIGINS contains "
            f"non-local origins {non_local}. Refusing to start."
        )

    fdir = fixture_dir()
    if not fdir.is_dir():
        raise RuntimeError(
            f"MOCK_ANTHROPIC=1 but fixture directory not found: {fdir}. "
            "Set MOCK_ANTHROPIC_FIXTURE to an existing assessment dir."
        )


@lru_cache(maxsize=64)
def _trace_output(trace_filename: str) -> str:
    """Pull `output` from the first record of a trace JSONL file."""
    path = fixture_dir() / "traces" / trace_filename
    with path.open(encoding="utf-8") as f:
        first = json.loads(f.readline())
    out = first.get("output")
    if not isinstance(out, str):
        raise RuntimeError(
            f"mock fixture {path} has no string `output` field"
        )
    return out


@lru_cache(maxsize=4)
def _questions_fenced_json() -> str:
    path = fixture_dir() / "elicitation_questions.json"
    return "```json\n" + path.read_text(encoding="utf-8").strip() + "\n```"


@lru_cache(maxsize=4)
def _slug_text() -> str:
    """Read the slug from the parent dir's active_slug.txt, fall back to dirname."""
    slug_path = fixture_dir().parent / "active_slug.txt"
    try:
        return slug_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return fixture_dir().name


def _metadata_stub() -> str:
    # Plausible, fixed; only used as text context in downstream prompts that
    # the mock also short-circuits, so exact content doesn't matter.
    return (
        "- Title: MATHDIAL: A Good Teacher Knows When to Tell\n"
        "- Authors: Macina et al.\n"
        "- Year: 2023\n"
        "- Task: pedagogical dialogue tutoring on math problems\n"
        "- Data: 3,000 teacher-student dialogues\n"
        "- Language: English\n"
    )


# Match on the leading bytes of each prompt's `system` text. Every prompt
# under anthropic_api_package_release/prompts/ has a distinctive opening, so
# startswith() is sufficient — order is not load-bearing.
_DISPATCH: list[tuple[str, Callable[[], str]]] = [
    ("Produce a short slug", _slug_text),
    ("You are extracting lightweight metadata", _metadata_stub),
    ("# Elicitation: Generate Questions", _questions_fenced_json),
    ("# Elicitation: Produce Summary",
        lambda: _trace_output("2_summary.jsonl")),
    # Per-page extract: prompt has `{page_num}` substituted, so we match the
    # prefix before the number and reuse one page's output for every page.
    ("You are extracting validity-relevant quotes from page",
        lambda: _trace_output("3a_extract.jsonl")),
    ("You will write the Metadata and Narrative Context",
        lambda: _trace_output("3a_consolidate.jsonl")),
    ("Pick the 1 or 2 benchmark YAMLs",
        lambda: _trace_output("3b_select.jsonl")),
    ("Synthesize a benchmark YAML",
        lambda: _trace_output("3b_synthesize.jsonl")),
    ("Pick the 1 or 2 base region template",
        lambda: _trace_output("4a_template.jsonl")),
    ("Produce an assessment-specific region",
        lambda: _trace_output("4b_synthesize.jsonl")),
    ("# Web search enrichment for the region",
        lambda: _trace_output("5_web_search.jsonl")),
    ("You are the validity analysis scorer",
        lambda: _trace_output("7_score.jsonl")),
]


def replay(family: str, system: str) -> str:
    """Return the canned response text for a given system prompt.

    Raises RuntimeError if no prefix matches — that signals a new pipeline
    step was added and the dispatcher needs a new entry. Loud failure here
    is far better than the model silently getting an empty string.
    """
    stripped = system.lstrip()
    for prefix, loader in _DISPATCH:
        if stripped.startswith(prefix):
            return loader()
    raise RuntimeError(
        "MOCK_ANTHROPIC=1: no fixture matches system prompt prefix "
        f"{stripped[:80]!r} (family={family!r}). Add an entry to "
        "_DISPATCH in website/server/mock_anthropic.py."
    )
