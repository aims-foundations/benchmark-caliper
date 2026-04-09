#!/usr/bin/env python3
"""format_results.py — Format validity analysis results as a summary report.

Replaces the LLM-based Step 6 with deterministic formatting.

Usage:
    python3 scripts/format_results.py results/<benchmark>_<region>.json
"""

import json
import sys
from pathlib import Path


def format_report(result: dict) -> str:
    """Format JSON results into a readable markdown summary."""
    lines = []

    benchmark = result.get("benchmark", "unknown")
    region = result.get("region", "unknown")

    lines.append(f"# Validity Analysis: {benchmark} → {region}")
    lines.append("")

    # Score summary table
    dims = result.get("dimensions", {})
    lines.append("## Dimension Scores")
    lines.append("")
    lines.append("| Dimension | Score | Confidence |")
    lines.append("|-----------|-------|------------|")

    dim_labels = {
        "input_ontology": "Input Ontology",
        "input_content": "Input Content",
        "input_form": "Input Form",
        "output_ontology": "Output Ontology",
        "output_content": "Output Content",
        "output_form": "Output Form",
    }

    total_score = 0
    count = 0
    for key, label in dim_labels.items():
        dim_data = dims.get(key, {})
        score = dim_data.get("score", "N/A")
        confidence = dim_data.get("confidence", "N/A")
        lines.append(f"| {label} | {score} | {confidence} |")
        if isinstance(score, (int, float)):
            total_score += score
            count += 1

    if count > 0:
        avg = total_score / count
        lines.append(f"| **Average** | **{avg:.1f}** | |")
    lines.append("")

    # Risk assessment
    risk = result.get("risk_assessment", "N/A")
    lines.append(f"## Overall Risk: {risk.upper()}")
    lines.append("")

    # Summary
    summary = result.get("overall_summary", "")
    if summary:
        lines.append("## Summary")
        lines.append("")
        lines.append(summary)
        lines.append("")

    # Top concerns
    concerns = result.get("highest_concern_dimensions", [])
    if concerns:
        lines.append("## Highest Concern Dimensions")
        lines.append("")
        for c in concerns:
            lines.append(f"- {c}")
        lines.append("")

    # Strongest
    strongest = result.get("strongest_dimensions", [])
    if strongest:
        lines.append("## Strongest Dimensions")
        lines.append("")
        for s in strongest:
            lines.append(f"- {s}")
        lines.append("")

    # Remediation
    remediation = result.get("remediation_suggestions", "")
    if remediation:
        lines.append("## Remediation Suggestions")
        lines.append("")
        lines.append(remediation)
        lines.append("")

    # Information gaps across dimensions
    lines.append("## Information Gaps (all dimensions)")
    lines.append("")
    for key, label in dim_labels.items():
        dim_data = dims.get(key, {})
        gaps = dim_data.get("information_gaps", [])
        if gaps:
            lines.append(f"**{label}**:")
            for g in gaps:
                lines.append(f"- {g}")
            lines.append("")

    # Artifacts
    lines.append("## Artifacts")
    lines.append("")
    lines.append(f"- Results JSON: `results/{benchmark}_{region}.json`")
    lines.append(f"- Benchmark YAML: `benchmarks/{benchmark}.yaml`")
    lines.append(f"- Region YAML: `regions/{region}.yaml`")
    lines.append(f"- Paper summary: `papers/{benchmark}_paper_summary.md`")
    lines.append(f"- Evaluation prompt: `.claude/prompts/{benchmark}/variant_a_neutral.md`")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <results.json>", file=sys.stderr)
        sys.exit(2)

    result_path = sys.argv[1]
    if not Path(result_path).exists():
        print(f"ERROR: File not found: {result_path}", file=sys.stderr)
        sys.exit(1)

    with open(result_path, encoding="utf-8") as f:
        result = json.load(f)

    report = format_report(result)
    print(report)


if __name__ == "__main__":
    main()
