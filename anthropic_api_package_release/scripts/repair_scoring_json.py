#!/usr/bin/env python3
"""Deterministic repair for scoring.json files corrupted by json_repair.

When Opus outputs scoring JSON with brace mismatches, the json_repair
library (fallback in parse_llm_output.py) nests subsequent keys inside
the last open JSON object rather than failing. This produces valid JSON
with a wrong tree structure: dimensions, summaries, and root-level keys
get buried inside a preceding dimension dict.

This script detects and repairs that corruption using the known scoring
schema — no API calls required.

Usage:
    python repair_scoring_json.py scoring.json              # repaired JSON to stdout
    python repair_scoring_json.py scoring.json --in-place   # overwrite file
    python repair_scoring_json.py -                         # stdin to stdout (pipeline)
    python repair_scoring_json.py --check scoring.json      # exit 0 clean, 1 corrupt
"""

import argparse
import copy
import json
import sys

DIMENSION_NAMES = {
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
}

PER_DIM_KEYS = {
    "score", "justification", "strengths", "weaknesses",
    "checklist_responses", "evidence_quotes", "evidence_web_sources",
    "evidence_dataset", "evidence_map", "confidence",
    "information_gaps", "requires_expert_verification",
}

ROOT_KEYS = {
    "overall_summary", "risk_assessment", "practical_guidance",
    "remediation_suggestions", "highest_concern_dimensions",
    "strongest_dimensions",
}


def detect_corruption(data: dict) -> list[str]:
    """Return human-readable descriptions of structural problems. Empty = clean."""
    issues = []

    dims = data.get("dimensions")
    if not isinstance(dims, dict):
        issues.append("missing or non-dict 'dimensions' key at root")
        return issues

    for dim_name in DIMENSION_NAMES:
        if dim_name not in dims:
            issues.append(f"dimension '{dim_name}' missing from dimensions (may be nested)")

    for dim_name, dim_dict in dims.items():
        if dim_name not in DIMENSION_NAMES or not isinstance(dim_dict, dict):
            continue
        for key in dim_dict:
            if key in DIMENSION_NAMES:
                issues.append(f"dimension '{key}' nested inside '{dim_name}'")
            elif key in ROOT_KEYS:
                issues.append(f"root key '{key}' nested inside dimension '{dim_name}'")
            elif key not in PER_DIM_KEYS:
                # Check inside checklist_responses for hoisted per-dim keys
                pass

        cr = dim_dict.get("checklist_responses")
        if isinstance(cr, dict):
            for key in cr:
                if key in PER_DIM_KEYS:
                    issues.append(
                        f"per-dimension key '{key}' nested inside "
                        f"checklist_responses of '{dim_name}'"
                    )

    for key in ROOT_KEYS:
        if key not in data:
            issues.append(f"root key '{key}' missing from top level")

    return issues


def _extract_from_dimension(dim_dict: dict, hoisted_dims: dict,
                            hoisted_root: dict, log: list[str],
                            parent_name: str) -> None:
    """Pull misplaced keys out of a single dimension dict (mutates in place)."""
    foreign = []
    for key in list(dim_dict):
        if key in DIMENSION_NAMES:
            hoisted_dims[key] = dim_dict[key]
            foreign.append(key)
            log.append(f"hoisted dimension '{key}' out of '{parent_name}'")
        elif key in ROOT_KEYS:
            hoisted_root[key] = dim_dict[key]
            foreign.append(key)
            log.append(f"hoisted root key '{key}' out of '{parent_name}'")
    for key in foreign:
        del dim_dict[key]

    # === Fix per-dimension keys that got nested inside checklist_responses ===
    cr = dim_dict.get("checklist_responses")
    if isinstance(cr, dict):
        cr_foreign = []
        for key in list(cr):
            if key in PER_DIM_KEYS:
                dim_dict[key] = cr[key]
                cr_foreign.append(key)
                log.append(
                    f"hoisted '{key}' from checklist_responses to "
                    f"dimension level in '{parent_name}'"
                )
        for key in cr_foreign:
            del cr[key]


def repair_scoring(data: dict) -> tuple[dict, list[str]]:
    """Repair structural corruption. Returns (repaired_copy, change_log)."""
    data = copy.deepcopy(data)
    log: list[str] = []

    dims = data.get("dimensions")
    if not isinstance(dims, dict):
        return data, ["no 'dimensions' key — cannot repair"]

    hoisted_dims: dict = {}
    hoisted_root: dict = {}

    # === Pass 0: extract root keys swallowed by any root-level dict ===
    # When the model forgets a closing brace (e.g., practical_guidance is
    # missing its "}"), the JSON parser folds subsequent root keys into
    # that dict. Scan all root-level dicts — both `dimensions` and others
    # like `practical_guidance` — for misplaced ROOT_KEYS.
    for parent_key in list(data):
        parent_val = data[parent_key]
        if not isinstance(parent_val, dict):
            continue
        for key in list(parent_val):
            if key in ROOT_KEYS:
                hoisted_root[key] = parent_val[key]
                del parent_val[key]
                log.append(f"hoisted root key '{key}' out of '{parent_key}'")

    # === Pass 1: extract misplaced keys from existing dimensions ===
    for dim_name in list(dims):
        dim_dict = dims[dim_name]
        if not isinstance(dim_dict, dict):
            continue
        _extract_from_dimension(dim_dict, hoisted_dims, hoisted_root,
                                log, dim_name)

    # === Pass 2: recursively process hoisted dimensions ===
    # A hoisted dimension may itself contain further nested dimensions
    # or root keys (e.g., output_content inside output_ontology, with
    # output_form inside output_content).
    queue = list(hoisted_dims.items())
    while queue:
        dim_name, dim_dict = queue.pop(0)
        if not isinstance(dim_dict, dict):
            continue
        inner_dims: dict = {}
        _extract_from_dimension(dim_dict, inner_dims, hoisted_root,
                                log, dim_name)
        for k, v in inner_dims.items():
            hoisted_dims[k] = v
            queue.append((k, v))

    # === Place hoisted dimensions back into dimensions dict ===
    for dim_name, dim_dict in hoisted_dims.items():
        if dim_name not in dims:
            dims[dim_name] = dim_dict
            log.append(f"restored dimension '{dim_name}' to dimensions dict")
        else:
            log.append(f"WARN: '{dim_name}' already in dimensions, keeping original")

    # === Place hoisted root keys back at top level ===
    for key, val in hoisted_root.items():
        if key not in data:
            data[key] = val
            log.append(f"restored root key '{key}' to top level")
        else:
            log.append(f"WARN: '{key}' already at root, keeping original")

    return data, log


def main():
    ap = argparse.ArgumentParser(
        description="Detect and repair scoring.json structural corruption")
    ap.add_argument("source", nargs="?", default="-",
                    help="scoring.json path or '-' for stdin")
    ap.add_argument("--in-place", action="store_true",
                    help="overwrite the source file with repaired output")
    ap.add_argument("--check", action="store_true",
                    help="exit 0 if clean, exit 1 if corrupt (no output)")
    args = ap.parse_args()

    if args.source == "-":
        raw = sys.stdin.read()
    else:
        raw = open(args.source).read()

    data = json.loads(raw)
    issues = detect_corruption(data)

    if args.check:
        if issues:
            for issue in issues:
                print(f"CORRUPT: {issue}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    if not issues:
        # Clean — pass through unchanged
        if args.in_place:
            pass
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    for issue in issues:
        print(f"WARN: {issue}", file=sys.stderr)

    repaired, log = repair_scoring(data)

    for entry in log:
        print(f"  REPAIR: {entry}", file=sys.stderr)

    remaining = detect_corruption(repaired)
    if remaining:
        for issue in remaining:
            print(f"  STILL CORRUPT: {issue}", file=sys.stderr)
        print("ERROR: repair did not fully resolve corruption", file=sys.stderr)
        sys.exit(1)

    output = json.dumps(repaired, indent=2, ensure_ascii=False)
    if args.in_place:
        if args.source == "-":
            print("ERROR: --in-place requires a file path, not stdin",
                  file=sys.stderr)
            sys.exit(1)
        with open(args.source, "w") as f:
            f.write(output + "\n")
        print(f"Repaired {args.source}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
