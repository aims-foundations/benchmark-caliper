#!/usr/bin/env python3
"""Extract a JSON array of elicitation questions from a raw LLM response.

Expected shape after fence stripping:
    [{"id": "Q1", "dimension": "IC", "question": "..."}, ...]

Validates each question object has id / dimension / question fields. Fails loud
on malformed input so the pipeline can surface upstream prompt drift.

Usage:
    python parse_elicitation_questions.py <file|->
"""

import json
import re
import sys


REQUIRED_FIELDS = {"id", "dimension", "question"}
ALLOWED_DIMENSIONS = {"IO", "IC", "IF", "OO", "OC", "OF"}


def strip_fences(raw: str) -> str:
    fence = re.search(r"```(?:json)?\s*\n(.*?)\n```", raw, re.DOTALL)
    if fence:
        return fence.group(1).strip()
    # === Fallback: trim to outermost [...] ===
    start = raw.find("[")
    end = raw.rfind("]")
    if start >= 0 and end > start:
        return raw[start : end + 1]
    return raw.strip()


def main():
    if len(sys.argv) != 2:
        print("usage: parse_elicitation_questions.py <file|->", file=sys.stderr)
        sys.exit(2)

    raw = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1]).read()

    try:
        questions = json.loads(strip_fences(raw))
    except json.JSONDecodeError as e:
        print(f"ERROR: failed to parse JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(questions, list):
        print(f"ERROR: expected a JSON array, got {type(questions).__name__}", file=sys.stderr)
        sys.exit(1)

    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            print(f"ERROR: question {i} is not an object", file=sys.stderr)
            sys.exit(1)
        missing = REQUIRED_FIELDS - q.keys()
        if missing:
            print(f"ERROR: question {i} missing fields: {sorted(missing)}", file=sys.stderr)
            sys.exit(1)
        if q["dimension"] not in ALLOWED_DIMENSIONS:
            print(
                f"ERROR: question {q['id']} has invalid dimension {q['dimension']!r}; "
                f"expected one of {sorted(ALLOWED_DIMENSIONS)}",
                file=sys.stderr,
            )
            sys.exit(1)

    print(json.dumps(questions, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
