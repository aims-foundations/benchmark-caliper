#!/usr/bin/env python3
"""Analyze results from the culture-agnostic validity gradation experiment.

Reads scoring.json from each completed assessment and produces:

  1. Per-dimension score tables for each benchmark/triplet
  2. Monotonicity checks (great ≥ ok ≥ terrible) per dimension
  3. Sensitivity analysis (which dimensions discriminate most)
  4. Aggregate summary across all triplets

Usage:
    python culture_agnostic/analyze_results.py
    python culture_agnostic/analyze_results.py --output culture_agnostic/results.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

EXPERIMENT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = EXPERIMENT_DIR.parent
ASSESSMENTS_DIR = PACKAGE_ROOT / "assessments"

DIMENSION_KEYS = [
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
]
DIM_SHORT = {
    "input_ontology": "IO", "input_content": "IC", "input_form": "IF",
    "output_ontology": "OO", "output_content": "OC", "output_form": "OF",
}
FIT_ORDER = ["great", "ok", "terrible"]
FIT_LABELS = {"great": "Great", "ok": "Ok", "terrible": "Terrible"}


def fatal(msg: str) -> None:
    print(f"\nFATAL: {msg}", file=sys.stderr)
    sys.exit(1)


def load_assessments() -> tuple[dict, list[dict]]:
    yaml_path = EXPERIMENT_DIR / "assessments.yaml"
    if not yaml_path.exists():
        fatal(f"assessments.yaml not found at {yaml_path}")
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return data["benchmarks"], data["assessments"]


def find_slug_dir(benchmark_key: str, assessment: dict) -> Path | None:
    root = ASSESSMENTS_DIR / benchmark_key
    if not root.exists():
        return None
    for slug_dir in root.iterdir():
        if not slug_dir.is_dir():
            continue
        desc_file = slug_dir / "deployment_description.txt"
        if desc_file.exists():
            if desc_file.read_text().strip() == assessment["deployment_description"].strip():
                return slug_dir
    return None


def load_scores(benchmark_key: str, assessment: dict) -> dict | None:
    """Load per-dimension scores from scoring.json. Returns None if not found.

    scoring.json nests dimensions under a "dimensions" key:
      {"dimensions": {"input_ontology": {"score": 4, ...}, ...}}
    Also handles flat layout (dimensions at top level) for robustness.
    """
    slug_dir = find_slug_dir(benchmark_key, assessment)
    if slug_dir is None:
        return None
    scoring_path = slug_dir / "scoring.json"
    if not scoring_path.exists():
        return None
    try:
        data = json.loads(scoring_path.read_text())
    except json.JSONDecodeError:
        return None
    dims = data.get("dimensions", data)
    scores = {}
    for dim_key in DIMENSION_KEYS:
        if dim_key in dims and isinstance(dims[dim_key], dict):
            score = dims[dim_key].get("score")
            if score is not None:
                scores[dim_key] = score
    return scores if scores else None


def format_score_table(triplet_scores: dict[str, dict[str, float]]) -> str:
    """Format a triplet's scores as a markdown table."""
    lines = []
    short_names = [DIM_SHORT[d] for d in DIMENSION_KEYS]
    header = "| Fit | " + " | ".join(short_names) + " | Mean |"
    sep = "|" + "|".join(["---"] * (len(DIMENSION_KEYS) + 2)) + "|"
    lines.append(header)
    lines.append(sep)

    for fit in FIT_ORDER:
        scores = triplet_scores.get(fit, {})
        vals = [scores.get(d) for d in DIMENSION_KEYS]
        cells = [f"{v:.1f}" if v is not None else "—" for v in vals]
        numeric = [v for v in vals if v is not None]
        mean = f"{sum(numeric)/len(numeric):.1f}" if numeric else "—"
        lines.append(f"| {FIT_LABELS[fit]} | " + " | ".join(cells) + f" | {mean} |")

    return "\n".join(lines)


def check_monotonicity(triplet_scores: dict[str, dict[str, float]]) -> dict[str, str]:
    """Check if scores decrease monotonically: great ≥ ok ≥ terrible.

    Returns {short_dim_name: "pass" | "partial" | "fail" | "missing"}.
    """
    results = {}
    for dim in DIMENSION_KEYS:
        short = DIM_SHORT[dim]
        vals = []
        for fit in FIT_ORDER:
            s = triplet_scores.get(fit, {}).get(dim)
            if s is None:
                results[short] = "missing"
                break
            vals.append(s)
        else:
            if vals[0] >= vals[1] >= vals[2]:
                results[short] = "pass"
            elif vals[0] > vals[2]:
                results[short] = "partial"
            else:
                results[short] = "fail"
    return results


def compute_sensitivity(triplet_scores: dict[str, dict[str, float]]) -> dict[str, float]:
    """Compute score spread (great - terrible) per dimension."""
    spreads = {}
    for dim in DIMENSION_KEYS:
        short = DIM_SHORT[dim]
        g = triplet_scores.get("great", {}).get(dim)
        t = triplet_scores.get("terrible", {}).get(dim)
        if g is not None and t is not None:
            spreads[short] = g - t
    return spreads


def main() -> None:
    p = argparse.ArgumentParser(description="Analyze culture-agnostic experiment results.")
    p.add_argument("--output", "-o", help="Write report to file (default: stdout)")
    args = p.parse_args()

    benchmarks, assessments = load_assessments()

    # Group assessments by benchmark and triplet
    grouped: dict[str, dict[str, dict[str, dict]]] = {}
    for a in assessments:
        bkey = a["benchmark"]
        triplet = a["triplet"]
        fit = a["fit"]
        grouped.setdefault(bkey, {}).setdefault(triplet, {})[fit] = a

    # Collect scores
    all_scores: dict[str, dict[str, dict[str, dict]]] = {}
    missing = []
    for bkey, triplets in grouped.items():
        for triplet, fits in triplets.items():
            for fit, assessment in fits.items():
                scores = load_scores(bkey, assessment)
                if scores is None:
                    missing.append(assessment["slug"])
                else:
                    all_scores.setdefault(bkey, {}).setdefault(triplet, {})[fit] = scores

    if missing:
        print(f"WARNING: {len(missing)} assessments without scores: "
              f"{', '.join(missing)}", file=sys.stderr)

    if not all_scores:
        fatal("No completed assessments found. Run the experiment first.")

    # Build report
    lines = ["# Culture-Agnostic Validity Gradation — Results\n"]

    all_mono: list[dict[str, str]] = []
    all_sensitivity: list[dict[str, float]] = []

    for bkey in ["gsm8k", "humaneval", "folio"]:
        if bkey not in all_scores:
            continue
        binfo = benchmarks[bkey]
        lines.append(f"## {bkey.upper()}")
        lines.append(f"Domain: {binfo['domain']}\n")

        for triplet, fit_scores in sorted(all_scores[bkey].items()):
            lines.append(f"### Triplet: {triplet}\n")
            lines.append(format_score_table(fit_scores))
            lines.append("")

            # Monotonicity
            mono = check_monotonicity(fit_scores)
            all_mono.append(mono)
            mono_summary = ", ".join(f"{d}={v}" for d, v in mono.items())
            lines.append(f"**Monotonicity:** {mono_summary}\n")

            # Sensitivity
            sens = compute_sensitivity(fit_scores)
            all_sensitivity.append(sens)
            if sens:
                sorted_dims = sorted(sens.items(), key=lambda x: x[1], reverse=True)
                sens_summary = ", ".join(f"{d}={v:+.1f}" for d, v in sorted_dims)
                lines.append(f"**Sensitivity (great−terrible):** {sens_summary}\n")
            lines.append("")

    # Aggregate
    lines.append("## Aggregate Summary\n")

    # Monotonicity pass rate per dimension
    short_names = [DIM_SHORT[d] for d in DIMENSION_KEYS]
    lines.append("### Monotonicity Pass Rate\n")
    lines.append("| Dimension | Pass | Partial | Fail | Missing |")
    lines.append("|---|---|---|---|---|")
    for short in short_names:
        counts = {"pass": 0, "partial": 0, "fail": 0, "missing": 0}
        for mono in all_mono:
            counts[mono.get(short, "missing")] += 1
        total = sum(counts.values())
        lines.append(f"| {short} | {counts['pass']}/{total} | "
                     f"{counts['partial']}/{total} | {counts['fail']}/{total} | "
                     f"{counts['missing']}/{total} |")
    lines.append("")

    # Average sensitivity per dimension
    if all_sensitivity:
        lines.append("### Average Sensitivity (great − terrible)\n")
        lines.append("| Dimension | Avg Spread |")
        lines.append("|---|---|")
        for short in short_names:
            vals = [s.get(short) for s in all_sensitivity if short in s]
            if vals:
                avg = sum(vals) / len(vals)
                lines.append(f"| {short} | {avg:+.2f} |")
            else:
                lines.append(f"| {short} | — |")
        lines.append("")

    report = "\n".join(lines)

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
