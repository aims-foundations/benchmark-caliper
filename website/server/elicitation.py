"""Parsing for the elicitation-questions step output.

Mirrors anthropic_api_package_release/scripts/parse_elicitation_questions.py: strip
optional code fences, then validate the JSON shape and dimension tags so
upstream prompt drift surfaces loudly here instead of silently downstream.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

REQUIRED_FIELDS = {"id", "dimension", "question"}
ALLOWED_DIMENSIONS = {"IO", "IC", "IF", "OO", "OC", "OF"}


@dataclass(frozen=True)
class Question:
    id: str
    dimension: str
    question: str

    def to_dict(self) -> dict[str, str]:
        return {"id": self.id, "dimension": self.dimension, "question": self.question}


class ParseError(ValueError):
    pass


def strip_fences(raw: str) -> str:
    fence = re.search(r"```(?:json)?\s*\n(.*?)\n```", raw, re.DOTALL)
    if fence:
        return fence.group(1).strip()
    start, end = raw.find("["), raw.rfind("]")
    if start >= 0 and end > start:
        return raw[start : end + 1]
    return raw.strip()


def parse(raw: str) -> list[Question]:
    try:
        items = json.loads(strip_fences(raw))
    except json.JSONDecodeError as e:
        raise ParseError(f"could not parse JSON: {e}") from e

    if not isinstance(items, list):
        raise ParseError(f"expected a JSON array, got {type(items).__name__}")

    out: list[Question] = []
    for i, q in enumerate(items):
        if not isinstance(q, dict):
            raise ParseError(f"question {i} is not an object")
        missing = REQUIRED_FIELDS - q.keys()
        if missing:
            raise ParseError(f"question {i} missing fields: {sorted(missing)}")
        if q["dimension"] not in ALLOWED_DIMENSIONS:
            raise ParseError(
                f"question {q['id']!r} has invalid dimension {q['dimension']!r}; "
                f"expected one of {sorted(ALLOWED_DIMENSIONS)}"
            )
        out.append(
            Question(
                id=str(q["id"]), dimension=str(q["dimension"]), question=str(q["question"])
            )
        )
    return out
