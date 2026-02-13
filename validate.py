#!/usr/bin/env python3
"""
Validate LLM-generated validity scores against ground-truth human expert scores.

Usage:
    python validate.py                          # Compare all results against ground truth
    python validate.py --result helm_sea.json   # Compare a single result file
"""

import json
import argparse
import sys
from pathlib import Path

import yaml


DIMENSION_ORDER = [
    "input_ontology",
    "input_content",
    "input_form",
    "output_ontology",
    "output_content",
    "output_form",
]

DIMENSION_DISPLAY = {
    "input_ontology": "Input Ontology",
    "input_content": "Input Content",
    "input_form": "Input Form",
    "output_ontology": "Output Ontology",
    "output_content": "Output Content",
    "output_form": "Output Form",
}


def load_ground_truth(framework_path: Path) -> dict:
    """Load ground-truth scores from framework.yaml."""
    with open(framework_path) as f:
        framework = yaml.safe_load(f)
    return framework.get("ground_truth", {})


def load_result(result_path: Path) -> dict:
    """Load an LLM evaluation result JSON file."""
    with open(result_path) as f:
        return json.load(f)


def compute_metrics(llm_scores: dict, gt_scores: dict) -> dict:
    """Compute comparison metrics between LLM and ground-truth scores."""
    dimensions = []
    abs_errors = []
    for dim in DIMENSION_ORDER:
        llm = llm_scores.get(dim)
        gt = gt_scores.get(dim)
        if llm is not None and gt is not None:
            error = abs(llm - gt)
            abs_errors.append(error)
            dimensions.append({
                "dimension": DIMENSION_DISPLAY[dim],
                "llm_score": llm,
                "gt_score": gt,
                "abs_error": error,
                "match": "EXACT" if error == 0 else ("CLOSE" if error <= 1 else "DIVERGENT"),
            })

    mae = sum(abs_errors) / len(abs_errors) if abs_errors else float("nan")
    max_error = max(abs_errors) if abs_errors else float("nan")
    exact_matches = sum(1 for e in abs_errors if e == 0)
    close_matches = sum(1 for e in abs_errors if e <= 1)

    return {
        "dimensions": dimensions,
        "mae": mae,
        "max_error": max_error,
        "exact_matches": f"{exact_matches}/{len(abs_errors)}",
        "close_matches": f"{close_matches}/{len(abs_errors)}",
        "passes_threshold": mae <= 1.0,
    }


def print_comparison(benchmark_name: str, region_name: str, metrics: dict):
    """Print a formatted comparison table."""
    print(f"\n{'='*70}")
    print(f"  {benchmark_name} -> {region_name}")
    print(f"{'='*70}")
    print(f"  {'Dimension':<20} {'LLM':>5} {'GT':>5} {'Error':>7} {'Status':>10}")
    print(f"  {'-'*20} {'-'*5} {'-'*5} {'-'*7} {'-'*10}")

    for d in metrics["dimensions"]:
        status_color = {
            "EXACT": "\033[92m",      # green
            "CLOSE": "\033[93m",      # yellow
            "DIVERGENT": "\033[91m",  # red
        }
        reset = "\033[0m"
        color = status_color.get(d["match"], "")
        print(f"  {d['dimension']:<20} {d['llm_score']:>5} {d['gt_score']:>5} {d['abs_error']:>7} {color}{d['match']:>10}{reset}")

    print(f"\n  Mean Absolute Error: {metrics['mae']:.2f}")
    print(f"  Max Error:           {metrics['max_error']}")
    print(f"  Exact Matches:       {metrics['exact_matches']}")
    print(f"  Close (<=1):         {metrics['close_matches']}")
    threshold_status = "\033[92mPASS\033[0m" if metrics["passes_threshold"] else "\033[91mFAIL\033[0m"
    print(f"  MAE <= 1.0:          {threshold_status}")


def validate_single(result_path: Path, ground_truth: dict):
    """Validate a single result file against ground truth."""
    result = load_result(result_path)
    benchmark = result.get("benchmark", "")
    region = result.get("region", "")

    # Find matching ground truth
    gt_key = f"{benchmark}_to_{region}"
    # Also try alternate key formats
    for key, gt_data in ground_truth.items():
        if gt_data.get("benchmark") == benchmark and gt_data.get("region") == region:
            gt_key = key
            break

    if gt_key not in ground_truth:
        print(f"  No ground truth found for {benchmark} -> {region}")
        return None

    gt_scores = ground_truth[gt_key]["scores"]

    # Extract LLM scores from result
    llm_scores = {}
    for dim_key in DIMENSION_ORDER:
        dim_data = result.get("dimensions", {}).get(dim_key, {})
        if isinstance(dim_data, dict):
            llm_scores[dim_key] = dim_data.get("score")
        elif isinstance(dim_data, (int, float)):
            llm_scores[dim_key] = int(dim_data)

    metrics = compute_metrics(llm_scores, gt_scores)
    print_comparison(benchmark.upper(), region, metrics)
    return metrics


def validate_all(results_dir: Path, ground_truth: dict):
    """Validate all result files in the results directory."""
    result_files = sorted(results_dir.glob("*.json"))
    if not result_files:
        print("No result files found in results/")
        print("Run evaluations first, then place JSON results in the results/ directory.")
        return

    all_metrics = []
    for result_file in result_files:
        if result_file.name == "summary.json":
            continue
        metrics = validate_single(result_file, ground_truth)
        if metrics:
            all_metrics.append(metrics)

    if all_metrics:
        overall_mae = sum(m["mae"] for m in all_metrics) / len(all_metrics)
        all_pass = all(m["passes_threshold"] for m in all_metrics)
        print(f"\n{'='*70}")
        print(f"  OVERALL")
        print(f"{'='*70}")
        print(f"  Average MAE across benchmarks: {overall_mae:.2f}")
        print(f"  All pass MAE <= 1.0:           {'YES' if all_pass else 'NO'}")


def generate_csv(results_dir: Path, output_path: Path):
    """Generate a summary CSV from all result files for human review."""
    import csv

    result_files = sorted(results_dir.glob("*.json"))
    rows = []

    for result_file in result_files:
        if result_file.name == "summary.json":
            continue
        result = load_result(result_file)
        benchmark = result.get("benchmark", "")
        region = result.get("region", "")

        for dim_key in DIMENSION_ORDER:
            dim_data = result.get("dimensions", {}).get(dim_key, {})
            if isinstance(dim_data, dict):
                rows.append({
                    "benchmark": benchmark,
                    "region": region,
                    "dimension": DIMENSION_DISPLAY[dim_key],
                    "llm_score": dim_data.get("score", ""),
                    "confidence": dim_data.get("confidence", ""),
                    "justification": dim_data.get("justification", ""),
                    "information_gaps": "; ".join(dim_data.get("information_gaps", [])),
                    "human_score": "",
                    "human_notes": "",
                })

    if rows:
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "benchmark", "region", "dimension", "llm_score", "confidence",
                "justification", "information_gaps", "human_score", "human_notes",
            ])
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nCSV written to {output_path}")
    else:
        print("No results to write to CSV.")


def main():
    parser = argparse.ArgumentParser(description="Validate LLM validity scores against ground truth")
    parser.add_argument("--result", type=str, help="Path to a single result JSON file")
    parser.add_argument("--csv", action="store_true", help="Generate summary CSV for human review")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    framework_path = base_dir / "framework.yaml"
    results_dir = base_dir / "results"

    if not framework_path.exists():
        print(f"Error: {framework_path} not found")
        sys.exit(1)

    ground_truth = load_ground_truth(framework_path)

    if args.csv:
        generate_csv(results_dir, results_dir / "summary.csv")
    elif args.result:
        result_path = Path(args.result)
        if not result_path.exists():
            result_path = results_dir / args.result
        if not result_path.exists():
            print(f"Error: {args.result} not found")
            sys.exit(1)
        validate_single(result_path, ground_truth)
    else:
        validate_all(results_dir, ground_truth)


if __name__ == "__main__":
    main()
