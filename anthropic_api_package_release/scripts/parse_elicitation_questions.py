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


# Minimum schema every question object must satisfy.
# These three fields are consumed by downstream stages: id for tracking,
# dimension for bucketing answers into validity axes, question for the prompt text.
REQUIRED_FIELDS = {"id", "dimension", "question"}

# Six validity dimensions from the framework: Internal/External × Objective/Construct/Face
# Two-letter codes: first letter = scope (I=internal, O=external), second = dimension type.
# Enforcing this at parse time ensures Stage 3 answer routing never silently drops data.
ALLOWED_DIMENSIONS = {"IO", "IC", "IF", "OO", "OC", "OF"}


# Normalize raw LLM output down to a plain JSON string, stripping any prose
# or markdown wrapper the model may have added around the array.
# Returns the narrowest string that json.loads() can consume directly.
def strip_fences(raw: str) -> str:
    # === Primary: extract content inside ```json ... ``` or ``` ... ``` fences ===
    # re.DOTALL so '.' matches newlines — the JSON array can span many lines.
    # The (?:json)? group handles both annotated and unannotated fences.
    fence = re.search(r"```(?:json)?\s*\n(.*?)\n```", raw, re.DOTALL)
    if fence:
        return fence.group(1).strip()

    # === Fallback: trim to outermost [...] ===
    # LLMs sometimes omit fences but still emit valid JSON preceded by a preamble
    # sentence. Slicing to the first '[' and last ']' discards that prose wrapper.
    # rfind for ']' (not find) guards against nested arrays or objects inside items.
    start = raw.find("[")
    end = raw.rfind("]")
    if start >= 0 and end > start:
        return raw[start : end + 1]

    # Last resort: return trimmed raw text and let json.loads surface the error.
    # This path fires when the model emitted neither fences nor a recognizable array —
    # the json.loads call in main() will then produce a descriptive error message.
    return raw.strip()


# Entry point: read raw LLM output from a file or stdin, parse and validate the
# question array, then emit clean JSON to stdout. Exits non-zero on any error so
# the calling pipeline can detect and report upstream prompt drift immediately.
def main():
    # === Stage 1: Read input ===
    if len(sys.argv) != 2:
        print("usage: parse_elicitation_questions.py <file|->", file=sys.stderr)
        sys.exit(2)

    # '-' is a Unix convention for "read from stdin" — supports pipe chaining
    # (e.g., llm_call.py | parse_elicitation_questions.py -)
    raw = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1]).read()

    # === Stage 2: Parse JSON ===
    # strip_fences normalises the variable formatting LLMs use around JSON output
    # before we attempt to deserialise — avoids spurious decode errors on valid data.
    try:
        questions = json.loads(strip_fences(raw))
    except json.JSONDecodeError as e:
        print(f"ERROR: failed to parse JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # The prompt asks for an array; a dict or scalar means the model went off-schema.
    # Better to fail here than to iterate a dict and produce nonsensical question objects.
    if not isinstance(questions, list):
        print(f"ERROR: expected a JSON array, got {type(questions).__name__}", file=sys.stderr)
        sys.exit(1)

    # === Stage 3: Validate each question object ===
    for i, q in enumerate(questions):
        # Guard: every element must be a JSON object, not a bare string or number.
        # A model sometimes wraps the array in an extra layer or emits a flat string list.
        if not isinstance(q, dict):
            print(f"ERROR: question {i} is not an object", file=sys.stderr)
            sys.exit(1)

        # Fail fast if any required field is absent — missing fields indicate the
        # model truncated or reformatted the output, which would silently corrupt
        # downstream answer extraction (Stage 3 keys into these fields by name).
        missing = REQUIRED_FIELDS - q.keys()
        if missing:
            print(f"ERROR: question {i} missing fields: {sorted(missing)}", file=sys.stderr)
            sys.exit(1)

        # Dimension codes drive which validity axis the answer maps to in Stage 3;
        # an unknown code would silently route data to the wrong bucket.
        # We reject here rather than warn so that partial runs don't produce
        # a misleadingly complete-looking output file.
        if q["dimension"] not in ALLOWED_DIMENSIONS:
            print(
                f"ERROR: question {q['id']} has invalid dimension {q['dimension']!r}; "
                f"expected one of {sorted(ALLOWED_DIMENSIONS)}",
                file=sys.stderr,
            )
            sys.exit(1)

    # === Stage 4: Emit validated output ===
    # Indented for human readability when debugging; ensure_ascii=False preserves
    # non-Latin characters that appear in question text for non-English corpora.
    print(json.dumps(questions, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
