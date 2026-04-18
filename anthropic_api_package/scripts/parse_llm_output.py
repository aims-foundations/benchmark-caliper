#!/usr/bin/env python3
"""Extract JSON or YAML from a raw LLM response.

Strips ```fenced``` code blocks if present; otherwise trims leading/trailing prose
down to the first plausible JSON/YAML body. Optionally validates against a JSON
schema. Pretty-prints the parsed result to stdout.

Usage:
  python parse_llm_output.py --format {json,yaml} [--schema PATH] <file|->
"""

import argparse
import json
import re
import sys

import yaml


def strip_fences(raw: str, fmt: str) -> str:
    # === Try fenced block first — the common LLM output shape ===
    fence = re.search(rf"```(?:{fmt})?\s*\n(.*?)\n```", raw, re.DOTALL)
    if fence:
        return fence.group(1).strip()

    stripped = raw.strip()

    # === JSON fallback: find first { or [ ===
    if fmt == "json":
        candidates = [i for i in (stripped.find("{"), stripped.find("[")) if i >= 0]
        if candidates:
            return stripped[min(candidates):]

    # === YAML fallback: assume the whole body is YAML ===
    return stripped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", choices=["json", "yaml"], required=True)
    ap.add_argument("--schema", help="optional JSON-schema file for validation")
    ap.add_argument("source", help="file path or '-' for stdin")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.source == "-" else open(args.source).read()
    cleaned = strip_fences(raw, args.format)

    try:
        parsed = json.loads(cleaned) if args.format == "json" else yaml.safe_load(cleaned)
    except Exception as e:
        print(f"ERROR: failed to parse {args.format}: {e}", file=sys.stderr)
        print("--- cleaned input (first 500 chars) ---", file=sys.stderr)
        print(cleaned[:500], file=sys.stderr)
        sys.exit(1)

    if args.schema:
        try:
            import jsonschema
        except ImportError:
            print("WARN: jsonschema not installed, skipping validation", file=sys.stderr)
        else:
            with open(args.schema) as f:
                schema = json.load(f)
            try:
                jsonschema.validate(parsed, schema)
            except jsonschema.ValidationError as e:
                print(f"ERROR: schema validation failed: {e.message}", file=sys.stderr)
                sys.exit(1)

    if args.format == "json":
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    else:
        print(yaml.safe_dump(parsed, sort_keys=False, allow_unicode=True))


if __name__ == "__main__":
    main()
