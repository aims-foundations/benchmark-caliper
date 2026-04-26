#!/usr/bin/env python3
"""format_results.py — Format validity analysis results as a markdown report.

Renders the scoring JSON into a three-tier report:
  1. Dashboard: scores, risk, practical guidance
  2. Dimension detail: justification, strengths, checklist, evidence
  3. Remediation: prioritized gaps and recommendations

Usage:
    python3 scripts/format_results.py results/<scoring>.json
    python3 scripts/format_results.py results/<scoring>.json --output report.md
"""

import json
import re
import sys
from pathlib import Path

DIM_LABELS = {
    "input_ontology": "Input Ontology",
    "input_content": "Input Content",
    "input_form": "Input Form",
    "output_ontology": "Output Ontology",
    "output_content": "Output Content",
    "output_form": "Output Form",
}

DIM_DEFINITIONS = {
    "input_ontology": "Whether the benchmark's test case categories cover the query types expected in deployment.",
    "input_content": "Whether individual datapoint content is culturally and contextually appropriate for the target region.",
    "input_form": "Whether the input signal encoding (text, audio, image parameters) matches deployment conditions.",
    "output_ontology": "Whether the benchmark's output categories and scoring criteria reflect regionally valid decision boundaries.",
    "output_content": "Whether ground-truth labels align with the judgments of regional stakeholders.",
    "output_form": "Whether the expected output modality matches regional deployment needs and accessibility.",
}

SCORE_LABELS = {
    1: "Serious concern",
    2: "Significant gaps",
    3: "Moderate gaps",
    4: "Minor gaps",
    5: "Strong alignment",
}


def _score_indicator(score) -> str:
    if not isinstance(score, (int, float)):
        return ""
    s = int(score)
    return SCORE_LABELS.get(s, "")


def _section(title: str, level: int = 2) -> str:
    return f"{'#' * level} {title}\n"


def format_dashboard(result: dict) -> list[str]:
    lines = []
    benchmark = result.get("benchmark", "unknown")
    region = result.get("region", "unknown")
    risk = result.get("risk_assessment", "N/A")

    lines.append(f"# Validity Analysis: {benchmark}")
    lines.append(f"**Target context:** {region}")
    lines.append(f"**Overall risk:** {risk.upper()}")
    lines.append("")

    # Score table
    dims = result.get("dimensions", {})
    lines.append(_section("Dimension Scores"))
    lines.append("| Dimension | Score | Rating | Confidence |")
    lines.append("|-----------|:-----:|--------|:----------:|")

    total, count = 0, 0
    highest = result.get("highest_concern_dimensions", [])
    strongest = result.get("strongest_dimensions", [])

    for key, label in DIM_LABELS.items():
        dim_data = dims.get(key, {})
        score = dim_data.get("score", "N/A")
        confidence = dim_data.get("confidence", "N/A")
        rating = _score_indicator(score)
        flag = ""
        if key in highest:
            flag = " ⚠"
        elif key in strongest:
            flag = " ✓"
        lines.append(f"| {label}{flag} | {score} | {rating} | {confidence} |")
        if isinstance(score, (int, float)):
            total += score
            count += 1

    if count > 0:
        avg = total / count
        lines.append(f"| **Average** | **{avg:.1f}** | | |")
    lines.append("")

    lines.append("> ⚠ = highest concern &nbsp; ✓ = strongest dimension")
    lines.append("")

    # Dimension key
    lines.append(_section("Dimension Key", 3))
    lines.append("| Abbr. | Dimension | Definition |")
    lines.append("|:-----:|-----------|------------|")
    abbrevs = {"input_ontology": "IO", "input_content": "IC", "input_form": "IF",
               "output_ontology": "OO", "output_content": "OC", "output_form": "OF"}
    for key, label in DIM_LABELS.items():
        lines.append(f"| {abbrevs[key]} | {label} | {DIM_DEFINITIONS[key]} |")
    lines.append("")

    # Overall summary
    summary = result.get("overall_summary", "")
    if summary:
        lines.append(_section("Overall Summary"))
        lines.append(summary)
        lines.append("")

    # Practical guidance
    guidance = result.get("practical_guidance", {})
    if guidance:
        lines.append(_section("Practical Guidance"))

        measure = guidance.get("what_this_benchmark_measures", "")
        if measure:
            lines.append(_section("What This Benchmark Measures", 3))
            lines.append(measure)
            lines.append("")

        depth = guidance.get("construct_depth", "")
        if depth:
            lines.append(_section("Construct Depth", 3))
            lines.append(depth)
            lines.append("")

        supp = guidance.get("supplementation_needed", "")
        if supp:
            lines.append(_section("What Else You Need", 3))
            lines.append(supp)
            lines.append("")

    return lines


def format_dimension_detail(key: str, dim_data: dict) -> list[str]:
    label = DIM_LABELS.get(key, key)
    score = dim_data.get("score", "N/A")
    confidence = dim_data.get("confidence", "N/A")
    rating = _score_indicator(score)

    lines = []
    lines.append(_section(f"{label} — {score}/5 ({rating})", 3))
    lines.append(f"**Confidence:** {confidence}")
    lines.append("")

    # Justification
    justification = dim_data.get("justification", "")
    if justification:
        lines.append("**Justification:**")
        lines.append(justification)
        lines.append("")

    # Strengths
    strengths = dim_data.get("strengths", [])
    if strengths:
        lines.append("**Strengths:**")
        for s in strengths:
            lines.append(f"- {s}")
        lines.append("")

    # Checklist responses
    checklist = dim_data.get("checklist_responses", {})
    if checklist:
        lines.append("**Checklist:**")
        lines.append("")
        evidence_map = dim_data.get("evidence_map", {})
        for item_id, response in checklist.items():
            sources = evidence_map.get(item_id, [])
            source_str = ""
            if sources:
                source_str = " — _Sources: " + ", ".join(sources) + "_"
            lines.append(f"- **{item_id}**: {response}{source_str}")
        lines.append("")

    # Evidence
    quotes = dim_data.get("evidence_quotes", [])
    web = dim_data.get("evidence_web_sources", [])
    dataset = dim_data.get("evidence_dataset", [])
    has_evidence = quotes or web or dataset

    if has_evidence:
        lines.append("<details>")
        lines.append("<summary><b>Evidence cited</b></summary>")
        lines.append("")
        if quotes:
            lines.append("*Paper quotes:*")
            for q in quotes:
                lines.append(f"- {q}")
            lines.append("")
        if web:
            lines.append("*Web sources:*")
            for w in web:
                lines.append(f"- {w}")
            lines.append("")
        if dataset:
            lines.append("*Dataset analysis:*")
            for d in dataset:
                lines.append(f"- {d}")
            lines.append("")
        lines.append("</details>")
        lines.append("")

    # Information gaps
    gaps = dim_data.get("information_gaps", [])
    if gaps:
        lines.append("**Information gaps:**")
        for g in gaps:
            lines.append(f"- {g}")
        lines.append("")

    # Expert verification needed
    expert = dim_data.get("requires_expert_verification", [])
    if expert:
        lines.append("**Requires expert verification:**")
        for e in expert:
            lines.append(f"- {e}")
        lines.append("")

    lines.append("---")
    lines.append("")
    return lines


def format_remediation(result: dict) -> list[str]:
    lines = []
    remediation = result.get("remediation_suggestions", [])
    if not remediation:
        return lines

    highest = result.get("highest_concern_dimensions", [])

    lines.append(_section("Remediation Suggestions"))

    if not isinstance(remediation, list):
        lines.append(str(remediation))
        lines.append("")
        return lines

    # Sort: highest-concern dimensions first
    def _sort_key(item):
        if isinstance(item, dict):
            dim = item.get("dimension", "")
            if dim in highest:
                return (0, highest.index(dim))
            return (1, dim)
        return (2, "")

    for item in sorted(remediation, key=_sort_key):
        if isinstance(item, dict):
            dim = item.get("dimension", "")
            gap = item.get("gap", "")
            rec = item.get("recommendation", "")
            dim_label = DIM_LABELS.get(dim, dim)
            priority = " ⚠" if dim in highest else ""
            lines.append(f"### {dim_label}{priority}")
            lines.append("")
            lines.append(f"**Gap:** {gap}")
            lines.append("")
            lines.append(f"**Recommendation:** {rec}")
            lines.append("")
        else:
            lines.append(f"- {item}")
            lines.append("")

    return lines


def format_deployment_context(assessment_dir: Path) -> list[str]:
    dep_path = assessment_dir / "deployment_description.txt"
    if not dep_path.exists():
        return []
    lines = []
    text = dep_path.read_text(encoding="utf-8").strip()
    lines.append(_section("Deployment Context"))
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("use case and domain:"):
            lines.append(f"**Use case:** {line.split(':', 1)[1].strip()}")
        elif line.lower().startswith("target population:"):
            lines.append(f"**Target population:** {line.split(':', 1)[1].strip()}")
        else:
            lines.append(line)
    lines.append("")
    return lines


def _extract_section(text: str, heading: str) -> str | None:
    pattern = re.compile(
        r"^#{1,4}\s+" + re.escape(heading) + r"\s*$",
        re.MULTILINE,
    )
    m = pattern.search(text)
    if not m:
        return None
    start = m.end()
    next_heading = re.search(r"^#{1,4}\s+", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def format_evidence_registries(assessment_dir: Path) -> list[str]:
    lines = []
    composed = assessment_dir / "composed_prompt.md"
    if not composed.exists():
        return lines

    text = composed.read_text(encoding="utf-8")

    quotes = _extract_section(text, "Verbatim Quote Registry")
    web = _extract_section(text, "Web Source Registry")

    da_report = assessment_dir / "dataset_analysis_report.md"
    has_da = da_report.exists()

    if not quotes and not web and not has_da:
        return lines

    lines.append(_section("Evidence Registries"))

    if quotes:
        lines.append(_section("Verbatim Quote Registry", 3))
        lines.append(quotes)
        lines.append("")

    if web:
        lines.append(_section("Web Source Registry", 3))
        lines.append(web)
        lines.append("")

    if has_da:
        lines.append(_section("Dataset Analysis", 3))
        da_text = da_report.read_text(encoding="utf-8").strip()
        lines.append(da_text)
        lines.append("")

    return lines


def format_report(result: dict, assessment_dir: Path | None = None) -> str:
    lines = []

    # Deployment context
    if assessment_dir:
        lines.extend(format_deployment_context(assessment_dir))

    # Tier 1: Dashboard
    lines.extend(format_dashboard(result))

    # Tier 2: Dimension detail
    dims = result.get("dimensions", {})
    lines.append(_section("Dimension Details"))

    for key in DIM_LABELS:
        dim_data = dims.get(key, {})
        if dim_data:
            lines.extend(format_dimension_detail(key, dim_data))

    # Tier 3: Remediation
    lines.extend(format_remediation(result))

    # Appendix: Evidence registries
    if assessment_dir:
        lines.extend(format_evidence_registries(assessment_dir))

    return "\n".join(lines)


def main():
    import argparse
    p = argparse.ArgumentParser(description="Format scoring JSON as markdown report")
    p.add_argument("results_json", help="Path to scoring.json")
    p.add_argument("--output", "-o", help="Write to file instead of stdout")
    args = p.parse_args()

    path = Path(args.results_json)
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)

    result = json.loads(path.read_text(encoding="utf-8"))
    assessment_dir = path.parent
    report = format_report(result, assessment_dir)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
