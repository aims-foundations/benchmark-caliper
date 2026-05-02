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


# Isolate the structured payload from a raw LLM string that may include prose,
# markdown fences, or both. Returns the cleaned body ready for parsing.
def strip_fences(raw: str, fmt: str) -> str:
    # === Try fenced block first — the common LLM output shape ===
    # Regex captures content between ```<lang> and ```, where the language tag
    # is optional (some models emit plain ``` with no language hint).
    # re.DOTALL makes '.' match newlines so multiline JSON/YAML is captured.
    fence = re.search(rf"```(?:{fmt})?\s*\n(.*?)\n```", raw, re.DOTALL)
    if fence:
        return fence.group(1).strip()

    # No fence found — the model returned inline text. Strip outer whitespace
    # before applying format-specific heuristics.
    stripped = raw.strip()

    # === JSON fallback: find first { or [ ===
    # LLMs often prepend a sentence like "Here is the JSON:" before the payload.
    # Scanning for the first object/array delimiter lets us skip that preamble.
    # Both delimiters are checked because the top-level structure could be either
    # an object ({}) or an array ([]).
    if fmt == "json":
        candidates = [i for i in (stripped.find("{"), stripped.find("[")) if i >= 0]
        if candidates:
            # Take whichever delimiter appears first in the string.
            return stripped[min(candidates):]

    # === YAML fallback: assume the whole body is YAML ===
    # YAML has no reliable structural delimiter to scan for, so we pass the
    # full stripped string and let the parser complain if it's truly malformed.
    return stripped


# Entry point: reads an LLM output file (or stdin), cleans it, parses it,
# optionally validates against a JSON schema, then pretty-prints to stdout.
def main():
    # === Argument parsing ===
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", choices=["json", "yaml"], required=True)
    ap.add_argument("--schema", help="optional JSON-schema file for validation")
    ap.add_argument("source", help="file path or '-' for stdin")
    args = ap.parse_args()

    # === Ingest raw LLM output ===
    # '-' as source is a Unix convention for stdin, allowing the script to sit
    # in a shell pipeline (e.g., `curl ... | python parse_llm_output.py --format json -`).
    raw = sys.stdin.read() if args.source == "-" else open(args.source).read()
    cleaned = strip_fences(raw, args.format)

    # === Parse structured data ===
    # yaml.safe_load is used instead of full_load to block arbitrary Python
    # object construction — important when processing untrusted model output.
    try:
        if args.format == "json":
            cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
            parsed = json.loads(cleaned)
        else:
            parsed = yaml.safe_load(cleaned)
    except (json.JSONDecodeError, Exception) as e:
        if args.format == "json":
            try:
                from json_repair import repair_json
                parsed = repair_json(cleaned, return_objects=True)
                print(f"WARN: strict JSON parse failed, repaired with json_repair: {e}",
                      file=sys.stderr)
            except Exception as e2:
                print(f"ERROR: failed to parse {args.format} (also failed repair): {e}",
                      file=sys.stderr)
                print("--- cleaned input (first 500 chars) ---", file=sys.stderr)
                print(cleaned[:500], file=sys.stderr)
                sys.exit(1)
        else:
            print(f"ERROR: failed to parse {args.format}: {e}", file=sys.stderr)
            print("--- cleaned input (first 500 chars) ---", file=sys.stderr)
            print(cleaned[:500], file=sys.stderr)
            sys.exit(1)

    # === Optional JSON schema validation ===
    # jsonschema is a soft dependency — warn and continue rather than crash,
    # so the script stays usable in environments where it isn't installed.
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

    # === Emit pretty-printed output ===
    # ensure_ascii=False preserves non-ASCII characters (e.g., Spanish accents
    # in validity study quotes) rather than escaping them to \uXXXX.
    # sort_keys=False keeps YAML field order stable, matching the model's output.
    if args.format == "json":
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    else:
        print(yaml.safe_dump(parsed, sort_keys=False, allow_unicode=True))


if __name__ == "__main__":
    main()
