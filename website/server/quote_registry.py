"""Assemble a Quote Registry from per-page Haiku extracts.

The Step 3a-consolidate prompt expects a markdown registry with sequential
Q IDs, page numbers, categories, and verbatim text. The existing CLI
pipeline does a Haiku cross-page merge first (joins quotes split across
page boundaries) — Phase 1A skips that optimisation; quotes from each
page are emitted as-is.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PageExtract:
    """Parsed Haiku output for one page."""
    page: int
    page_summary: str
    quotes: list[dict]
    continues_from_previous: bool
    continues_to_next: bool


def parse_page_json(raw: str, page: int) -> PageExtract:
    """Parse the JSON Haiku returned for one page. Tolerant of fences."""
    fence = re.search(r"```(?:json)?\s*\n(.*?)\n```", raw, re.DOTALL)
    body = fence.group(1).strip() if fence else raw.strip()
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        # If the model returned malformed JSON, surface an empty extract
        # rather than failing the whole run. Tier-2 fingerprint records the
        # raw output for debugging.
        return PageExtract(
            page=page,
            page_summary="",
            quotes=[],
            continues_from_previous=False,
            continues_to_next=False,
        )
    return PageExtract(
        page=page,
        page_summary=str(data.get("page_summary", "")),
        quotes=[q for q in data.get("quotes", []) if isinstance(q, dict)],
        continues_from_previous=bool(data.get("continues_from_previous", False)),
        continues_to_next=bool(data.get("continues_to_next", False)),
    )


def assemble(extracts: list[PageExtract]) -> str:
    """Build the markdown Quote Registry that Sonnet's consolidate prompt
    expects. Quotes get sequential Q1..QN IDs in page order."""
    lines: list[str] = ["## Quote Registry", ""]
    qid = 1
    for ext in sorted(extracts, key=lambda e: e.page):
        for q in ext.quotes:
            text = str(q.get("text", "")).strip()
            category = str(q.get("category", "")).strip() or "uncategorized"
            if not text:
                continue
            lines.append(f"- Q{qid} (page {ext.page}, {category}): {text!r}")
            qid += 1
    lines.append("")
    lines.append("## Page Summaries")
    lines.append("")
    for ext in sorted(extracts, key=lambda e: e.page):
        if ext.page_summary:
            lines.append(f"- page {ext.page}: {ext.page_summary}")
    return "\n".join(lines) + "\n"
