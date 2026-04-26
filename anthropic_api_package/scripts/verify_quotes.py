#!/usr/bin/env python3
"""verify_quotes.py — Mechanical verification of quote provenance chain.

Performs the non-LLM checks from Step 1c:
  1. Count check: quotes in YAML == quotes in paper summary
  2. Coverage check: every validity dimension has at least one quote
  3. ID continuity: quote IDs are sequential (Q1, Q2, ..., QN)

Usage:
    python3 scripts/verify_quotes.py benchmarks/<name>.yaml papers/<name>/paper_summary.md

Exit codes:
    0 = all checks pass
    1 = failures found (details printed to stderr)
"""

import sys
import re
import yaml
from pathlib import Path


# Parse the Quote Registry table embedded in the paper summary markdown and
# return the number of rows found. The registry is the ground truth for how
# many quotes were identified during paper summarization — any divergence from
# the YAML count indicates a copy/paste or editing error downstream.
def count_registry_quotes(summary_path: str) -> int:
    """Count quotes in the paper summary's Quote Registry table."""
    text = Path(summary_path).read_text(encoding="utf-8")
    # Match rows like: | Q1 | 20 | task_taxonomy | "..." |
    # Anchoring with ^ + MULTILINE ensures we don't match embedded pipe characters
    # inside cell text — only genuine row-start delimiters.
    pattern = r"^\|\s*Q(\d+)\s*\|"
    matches = re.findall(pattern, text, re.MULTILINE)
    return len(matches)


# Load the benchmark YAML and return the verbatim_quotes list. Returns an
# empty list (not an error) when the key is absent — upstream checks catch the
# resulting count mismatch rather than crashing here.
def extract_yaml_quotes(yaml_path: str) -> list[dict]:
    """Extract verbatim_quotes from benchmark YAML."""
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("verbatim_quotes", [])


# Surface-level count parity: the YAML must carry exactly as many quote objects
# as the paper summary registry. A mismatch means a quote was added, removed,
# or duplicated at some point in the curation workflow.
def check_count(yaml_quotes: list, registry_count: int) -> list[str]:
    """Check that YAML quote count matches registry count. Returns list of error strings."""
    errors = []
    yaml_count = len(yaml_quotes)
    if yaml_count != registry_count:
        errors.append(
            f"COUNT MISMATCH: YAML has {yaml_count} quotes, "
            f"paper summary registry has {registry_count}"
        )
    return errors


# Verify that quote IDs form an unbroken sequence Q1..QN. Gaps (e.g., Q3
# missing) or duplicates would break downstream code that resolves quotes by
# numeric index and would make the provenance trail ambiguous.
def check_id_continuity(yaml_quotes: list) -> list[str]:
    """Check that quote IDs are sequential Q1..QN. Returns list of error strings."""
    errors = []
    ids = []

    # === Stage 1: Parse IDs ===
    for q in yaml_quotes:
        qid = q.get("id", "")
        # Extract the numeric suffix; reject anything that doesn't match Q<int>
        match = re.match(r"Q(\d+)", str(qid))
        if match:
            ids.append(int(match.group(1)))
        else:
            errors.append(f"INVALID ID: '{qid}' is not a valid quote ID (expected Q<number>)")

    # === Stage 2: Gap and collision detection ===
    if ids:
        ids_sorted = sorted(ids)
        # Expected = {1, 2, ..., N} — any deviation is an authoring error
        expected = list(range(1, len(ids) + 1))
        if ids_sorted != expected:
            missing = set(expected) - set(ids_sorted)
            extra = set(ids_sorted) - set(expected)
            if missing:
                errors.append(f"MISSING IDs: {', '.join(f'Q{i}' for i in sorted(missing))}")
            # "extra" IDs arise from duplicates or out-of-range values (e.g., Q99
            # when there are only 10 quotes total)
            if extra:
                errors.append(f"UNEXPECTED IDs: {', '.join(f'Q{i}' for i in sorted(extra))}")
    return errors


# Every one of the 6 IO-validity dimensions must have at least one anchoring
# quote. A dimension with zero quotes isn't just a gap — it's a substantive
# finding about the paper's reporting practices and must be flagged explicitly
# rather than silently omitted.
def check_dimension_coverage(yaml_quotes: list) -> list[str]:
    """Check that all 6 validity dimensions have at least one quote. Returns list of error strings."""
    # The 6 dimensions map onto the IO-validity framework: 3 input facets x
    # 3 output facets (ontology / content / form for each).
    required_dims = {
        "input_ontology", "input_content", "input_form",
        "output_ontology", "output_content", "output_form"
    }
    found_dims = set()
    for q in yaml_quotes:
        dim = q.get("dimension", "")
        # Only count dimensions that belong to the required set; unknown
        # dimension values (typos, extra categories) don't satisfy coverage.
        if dim in required_dims:
            found_dims.add(dim)

    errors = []
    missing = required_dims - found_dims
    if missing:
        for dim in sorted(missing):
            errors.append(
                f"NO COVERAGE: dimension '{dim}' has zero quotes. "
                "This absence is a validity-relevant finding."
            )
    return errors


def main():
    # === Argument validation ===
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <benchmark.yaml> <paper_summary.md>", file=sys.stderr)
        sys.exit(2)

    yaml_path = sys.argv[1]
    summary_path = sys.argv[2]

    # Validate files exist before attempting to parse — gives a cleaner error
    # than the cryptic FileNotFoundError that yaml/pathlib would raise otherwise.
    for path in [yaml_path, summary_path]:
        if not Path(path).exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(2)

    # === Run all mechanical checks ===
    yaml_quotes = extract_yaml_quotes(yaml_path)
    registry_count = count_registry_quotes(summary_path)

    # Accumulate errors across all checks so the user sees every problem at
    # once rather than fixing one failure and re-running to discover the next.
    all_errors = []
    all_errors.extend(check_count(yaml_quotes, registry_count))
    all_errors.extend(check_id_continuity(yaml_quotes))
    all_errors.extend(check_dimension_coverage(yaml_quotes))

    # === Report ===
    # Always print the summary header to stdout so the caller can log it;
    # individual failures go to stderr so they can be separated by the shell.
    print(f"=== Quote Verification Report ===")
    print(f"YAML quotes:     {len(yaml_quotes)}")
    print(f"Registry quotes:  {registry_count}")
    # Inline dimension count: filters to the canonical 6 dims only to avoid
    # inflating the count with stray dimension values.
    print(f"Dimensions covered: {len(set(q.get('dimension','') for q in yaml_quotes if q.get('dimension','') in {'input_ontology','input_content','input_form','output_ontology','output_content','output_form'}))}/6")
    print()

    if all_errors:
        print(f"FAILURES ({len(all_errors)}):", file=sys.stderr)
        for err in all_errors:
            print(f"  ✗ {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print("All mechanical checks passed.")
        print("  ✓ Quote counts match")
        print("  ✓ IDs are sequential")
        print("  ✓ All 6 dimensions covered")
        print()
        # Remind the caller that these checks are structural only — verifying
        # that quote text actually matches the cited PDF page requires an LLM
        # (handled separately in the pipeline as Step 1c text spot-check).
        print("NOTE: Text spot-check (comparing quote text to PDF) still requires LLM.")
        sys.exit(0)


if __name__ == "__main__":
    main()
