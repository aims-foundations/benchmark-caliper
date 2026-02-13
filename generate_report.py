#!/usr/bin/env python3
"""
Generate radar charts and markdown reports from validity analysis results.

Usage:
    python generate_report.py                    # Generate reports for all results
    python generate_report.py --result helm_sea  # Generate report for a single result
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime

import yaml
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family'] = 'sans-serif'


DIMENSION_ORDER = [
    "input_ontology",
    "input_content",
    "input_form",
    "output_ontology",
    "output_content",
    "output_form",
]

DIMENSION_LABELS = [
    'Input\nOntology',
    'Input\nContent',
    'Input\nForm',
    'Output\nTaxonomy',
    'Output\nLabels',
    'Output\nForm',
]

DIMENSION_DISPLAY = {
    "input_ontology": "Input Ontology",
    "input_content": "Input Content",
    "input_form": "Input Form",
    "output_ontology": "Output Ontology",
    "output_content": "Output Content",
    "output_form": "Output Form",
}

COLORS = [
    '#E74C3C',  # red
    '#2ECC71',  # green
    '#3498DB',  # blue
    '#F39C12',  # orange
    '#9B59B6',  # purple
    '#1ABC9C',  # teal
    '#E67E22',  # dark orange
    '#34495E',  # dark blue-gray
]


def load_result(result_path: Path) -> dict:
    """Load an LLM evaluation result JSON file."""
    with open(result_path) as f:
        return json.load(f)


def load_ground_truth(framework_path: Path) -> dict:
    """Load ground-truth scores from framework.yaml."""
    with open(framework_path) as f:
        framework = yaml.safe_load(f)
    return framework.get("ground_truth", {})


def extract_scores(result: dict) -> list:
    """Extract scores in dimension order from a result dict."""
    scores = []
    for dim in DIMENSION_ORDER:
        dim_data = result.get("dimensions", {}).get(dim, {})
        if isinstance(dim_data, dict):
            scores.append(dim_data.get("score", 0))
        elif isinstance(dim_data, (int, float)):
            scores.append(int(dim_data))
        else:
            scores.append(0)
    return scores


def generate_radar_chart(results: list[dict], output_path: Path, title: str = ""):
    """Generate a radar chart comparing multiple benchmark validity profiles."""
    N = len(DIMENSION_LABELS)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=8, color='#888888')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIMENSION_LABELS, fontsize=10, fontweight='bold', color='#333333')

    ax.yaxis.grid(True, color='#DDDDDD', linewidth=0.5)
    ax.xaxis.grid(True, color='#CCCCCC', linewidth=0.5)
    ax.spines['polar'].set_visible(False)

    for i, result in enumerate(results):
        name = result.get("label", result.get("benchmark", f"Benchmark {i+1}"))
        scores = result.get("scores", extract_scores(result))
        values = scores + scores[:1]
        color = COLORS[i % len(COLORS)]

        ax.plot(angles, values, 'o-', linewidth=2.2, markersize=6,
                label=name, color=color, zorder=3)
        ax.fill(angles, values, alpha=0.08, color=color)

    legend = ax.legend(
        loc='upper right',
        bbox_to_anchor=(1.28, 1.12),
        fontsize=10,
        frameon=True,
        fancybox=True,
        shadow=False,
        edgecolor='#CCCCCC',
    )
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.9)

    if title:
        ax.set_title(title, fontsize=13, fontweight='bold', color='#2C3E50', pad=25)

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  Radar chart saved to {output_path}")


def generate_markdown_report(result: dict, output_path: Path, gt_scores: dict = None):
    """Generate a markdown report for a single benchmark-region evaluation."""
    benchmark = result.get("benchmark", "Unknown")
    region = result.get("region", "Unknown")

    lines = [
        f"# Validity Analysis: {benchmark.upper()} -> {region}",
        f"",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"",
        f"## Score Summary",
        f"",
        f"| Dimension | LLM Score | Confidence | {'GT Score | Error |' if gt_scores else ''} Key Concern |",
        f"|-----------|-----------|------------|{'-----------|-------|' if gt_scores else ''} ------------|",
    ]

    for dim in DIMENSION_ORDER:
        dim_data = result.get("dimensions", {}).get(dim, {})
        if isinstance(dim_data, dict):
            score = dim_data.get("score", "?")
            confidence = dim_data.get("confidence", "?")
            justification = dim_data.get("justification", "")
            short_concern = justification[:80] + "..." if len(justification) > 80 else justification

            if gt_scores:
                gt = gt_scores.get(dim, "?")
                error = abs(score - gt) if isinstance(score, int) and isinstance(gt, int) else "?"
                lines.append(f"| {DIMENSION_DISPLAY[dim]} | {score} | {confidence} | {gt} | {error} | {short_concern} |")
            else:
                lines.append(f"| {DIMENSION_DISPLAY[dim]} | {score} | {confidence} | {short_concern} |")

    # Dimension details
    lines.extend(["", "## Dimension Details", ""])
    for dim in DIMENSION_ORDER:
        dim_data = result.get("dimensions", {}).get(dim, {})
        if isinstance(dim_data, dict):
            lines.extend([
                f"### {DIMENSION_DISPLAY[dim]} (Score: {dim_data.get('score', '?')}/5, Confidence: {dim_data.get('confidence', '?')})",
                f"",
                f"**Justification**: {dim_data.get('justification', 'N/A')}",
                f"",
            ])

            evidence = dim_data.get("evidence_quotes", [])
            if evidence:
                lines.append("**Evidence**:")
                for e in evidence:
                    lines.append(f"- \"{e}\"")
                lines.append("")

            gaps = dim_data.get("information_gaps", [])
            if gaps:
                lines.append("**Information Gaps**:")
                for g in gaps:
                    lines.append(f"- {g}")
                lines.append("")

            expert = dim_data.get("requires_expert_verification", [])
            if expert:
                lines.append("**Requires Expert Verification**:")
                for e in expert:
                    lines.append(f"- {e}")
                lines.append("")

            checklist = dim_data.get("checklist_responses", {})
            if checklist:
                lines.append("**Checklist Responses**:")
                for k, v in checklist.items():
                    lines.append(f"- [{k}] {v}")
                lines.append("")

    # Overall summary
    overall = result.get("overall_summary", "")
    risk = result.get("risk_assessment", "")
    remediation = result.get("remediation_suggestions", "")
    if overall or risk or remediation:
        lines.extend(["## Overall Assessment", ""])
        if overall:
            lines.extend([f"**Summary**: {overall}", ""])
        if risk:
            lines.extend([f"**Risk Level**: {risk}", ""])
        if remediation:
            lines.extend([f"**Suggested Remediation**: {remediation}", ""])

    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    print(f"  Report saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate reports from validity analysis results")
    parser.add_argument("--result", type=str, help="Specific result file name (without .json)")
    parser.add_argument("--compare", nargs="+", help="Compare multiple results in one radar chart")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    results_dir = base_dir / "results"
    framework_path = base_dir / "framework.yaml"

    gt = load_ground_truth(framework_path) if framework_path.exists() else {}

    if args.compare:
        # Compare multiple results in one chart
        chart_data = []
        for name in args.compare:
            result_path = results_dir / f"{name}.json"
            if result_path.exists():
                result = load_result(result_path)
                chart_data.append({
                    "label": result.get("benchmark", name).upper(),
                    "scores": extract_scores(result),
                })
            else:
                print(f"Warning: {result_path} not found, skipping")
        if chart_data:
            output = results_dir / "comparison_radar.png"
            generate_radar_chart(chart_data, output, title="Validity Comparison")
    elif args.result:
        # Single result
        result_path = results_dir / f"{args.result}.json"
        if not result_path.exists():
            print(f"Error: {result_path} not found")
            sys.exit(1)
        result = load_result(result_path)
        benchmark = result.get("benchmark", "")
        region = result.get("region", "")

        # Find ground truth
        gt_scores = None
        for key, gt_data in gt.items():
            if gt_data.get("benchmark") == benchmark and gt_data.get("region") == region:
                gt_scores = gt_data.get("scores")
                break

        generate_markdown_report(result, results_dir / f"{args.result}_report.md", gt_scores)
        generate_radar_chart(
            [{"label": benchmark.upper(), "scores": extract_scores(result)}],
            results_dir / f"{args.result}_radar.png",
        )
    else:
        # All results
        result_files = sorted(results_dir.glob("*.json"))
        if not result_files:
            print("No result files found in results/")
            return

        chart_data = []
        for result_file in result_files:
            if result_file.name in ("summary.json",):
                continue
            result = load_result(result_file)
            name = result_file.stem
            benchmark = result.get("benchmark", "")
            region = result.get("region", "")

            gt_scores = None
            for key, gt_data in gt.items():
                if gt_data.get("benchmark") == benchmark and gt_data.get("region") == region:
                    gt_scores = gt_data.get("scores")
                    break

            generate_markdown_report(result, results_dir / f"{name}_report.md", gt_scores)
            chart_data.append({
                "label": f"{benchmark.upper()} -> {region}",
                "scores": extract_scores(result),
            })

        if chart_data:
            generate_radar_chart(chart_data, results_dir / "all_radar.png", title="Validity Analysis Results")


if __name__ == "__main__":
    main()
