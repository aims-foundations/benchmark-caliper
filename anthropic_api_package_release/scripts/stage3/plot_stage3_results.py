#!/usr/bin/env python3
"""plot_stage3_results.py -- Generate summary plots from Stage 3 expert responses.

Reads primary_assessments.json and comparative_assessments.json from
stage3_results/ and produces 6 plots in stage3_results/plots/.

Usage:
    python3 scripts/stage3/plot_stage3_results.py
    python3 scripts/stage3/plot_stage3_results.py --results-dir stage3_results
"""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


# === Expert display labels (ordered by descending mean Likert for visual clarity) ===

EXPERT_ORDER = [
    "expert_7f59a7837eda",
    "expert_b81915e01b62",
    "expert_3fcd1181e6a6",
    "expert_1a429e941728",
    "expert_80eb33f0e871",
]

EXPERT_LABELS = {
    "expert_7f59a7837eda": "E1 (FR/LU)",
    "expert_b81915e01b62": "E2 (ET)",
    "expert_3fcd1181e6a6": "E3 (EC/AR)",
    "expert_1a429e941728": "E4 (IN)",
    "expert_80eb33f0e871": "E5 (BD)",
}

DIM_KEYS = [
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
]

DIM_SHORT = {
    "input_ontology": "IO", "input_content": "IC", "input_form": "IF",
    "output_ontology": "OO", "output_content": "OC", "output_form": "OF",
}

COMPARATOR_BENCHMARKS = {
    "mmlu", "blurb", "glue", "mathdial", "cnn_dailymail", "crisisbench",
    "asap_pp", "civil_comments", "flores200", "massive",
}

STYLE_KWARGS = dict(edgecolor="white", linewidth=0.5)


def load_data(results_dir):
    results_dir = Path(results_dir)
    primary = json.loads((results_dir / "primary_assessments.json").read_text())
    comparative = json.loads(
        (results_dir / "comparative_assessments.json").read_text())
    return primary, comparative


# =========================================================================
# Plot 1: Per-expert mean Likert heatmap
# =========================================================================

def plot_heatmap(primary, plots_dir):
    col_keys = [
        "mean_dim_score_appropriate",
        "mean_dim_justification_adequate",
        "mean_dim_evidence_support",
        "mean_dim_checklist_complete",
        "mean_context_likert",
        "mean_usefulness_likert",
    ]
    col_labels = [
        "Score\nAppropriate",
        "Justification\nAdequate",
        "Evidence\nSupport",
        "Checklist\nComplete",
        "Context\n(Summary)",
        "Usefulness &\nActionability",
    ]

    # === Group by expert, average across tuples ===
    expert_vals = defaultdict(lambda: defaultdict(list))
    for r in primary:
        eid = r["expert_id"]
        agg = r.get("aggregates", {})
        for k in col_keys:
            v = agg.get(k)
            if v is not None:
                expert_vals[eid][k].append(v)

    matrix = []
    ylabels = []
    for eid in EXPERT_ORDER:
        if eid not in expert_vals:
            continue
        row = []
        for k in col_keys:
            vals = expert_vals[eid][k]
            row.append(np.mean(vals) if vals else np.nan)
        matrix.append(row)
        ylabels.append(EXPERT_LABELS.get(eid, eid[:8]))

    matrix = np.array(matrix)

    fig, ax = plt.subplots(figsize=(8, 3.8))
    cmap = plt.cm.RdYlGn
    norm = mcolors.Normalize(vmin=1, vmax=5)
    im = ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(range(len(col_labels)))
    ax.set_xticklabels(col_labels, fontsize=9, ha="center")
    ax.set_yticks(range(len(ylabels)))
    ax.set_yticklabels(ylabels, fontsize=10)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            v = matrix[i, j]
            if np.isnan(v):
                continue
            color = "white" if v < 3.5 else "black"
            ax.text(j, i, f"{v:.1f}", ha="center", va="center",
                    fontsize=10, fontweight="bold", color=color)

    cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label("Mean Likert (1–5)", fontsize=9)
    cbar.set_ticks([1, 2, 3, 4, 5])

    ax.set_title("Expert Agreement with Pipeline Assessments (mean across 4 tuples)",
                 fontsize=11, pad=30)
    fig.tight_layout()
    fig.savefig(plots_dir / "1_likert_heatmap.png", dpi=200, bbox_inches="tight")
    fig.savefig(plots_dir / "1_likert_heatmap.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Plot 1: likert_heatmap")


# =========================================================================
# Plot 1b: Grand-mean Likert bar with std dev (across all 20 tuples)
# =========================================================================

def plot_likert_grand_mean(primary, plots_dir):
    col_keys = [
        "mean_dim_score_appropriate",
        "mean_dim_justification_adequate",
        "mean_dim_evidence_support",
        "mean_dim_checklist_complete",
        "mean_context_likert",
        "mean_usefulness_likert",
    ]
    col_labels = [
        "Score\nAppropriate",
        "Justification\nAdequate",
        "Evidence\nSupport",
        "Checklist\nComplete",
        "Context\n(Summary)",
        "Usefulness &\nActionability",
    ]

    all_vals = defaultdict(list)
    for r in primary:
        agg = r.get("aggregates", {})
        for k in col_keys:
            v = agg.get(k)
            if v is not None:
                all_vals[k].append(v)

    means = [np.mean(all_vals[k]) for k in col_keys]
    stds = [np.std(all_vals[k]) for k in col_keys]

    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(col_keys))
    bars = ax.bar(x, means, yerr=stds, capsize=4, color="#5a9bd5",
                  width=0.55, error_kw={"linewidth": 1.2}, **STYLE_KWARGS)

    for bar, m, s in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width() / 2, m + s + 0.12,
                f"{m:.2f}", ha="center", va="bottom", fontsize=10,
                fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(col_labels, fontsize=9)
    ax.set_ylabel("Mean Likert (1–5)", fontsize=10)
    ax.set_ylim(0, 5.8)
    ax.axhline(y=3, color="#cccccc", linewidth=0.8, linestyle="--")
    ax.set_title("Grand Mean Expert Agreement Across All Tuples (N=20)",
                 fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(plots_dir / "1b_likert_grand_mean.png", dpi=200,
                bbox_inches="tight")
    fig.savefig(plots_dir / "1b_likert_grand_mean.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Plot 1b: likert_grand_mean")


# =========================================================================
# Plot 2: Risk agreement stacked bar
# =========================================================================

def plot_risk_agreement(primary, plots_dir):
    categories = [
        "Too conservative (risk is lower)",
        "About right",
        "Too lenient (risk is higher)",
        "Cannot assess",
    ]
    cat_short = ["Too conservative", "About right", "Too lenient", "Cannot assess"]
    colors = ["#4393c3", "#2ca02c", "#d6604d", "#999999"]

    expert_counts = defaultdict(lambda: Counter())
    for r in primary:
        eid = r["expert_id"]
        val = r.get("context", {}).get("risk_agreement", "")
        expert_counts[eid][val] += 1

    fig, ax = plt.subplots(figsize=(7, 3.5))
    x = np.arange(len(EXPERT_ORDER))
    bottoms = np.zeros(len(EXPERT_ORDER))
    bars_drawn = []

    for cat, label, color in zip(categories, cat_short, colors):
        heights = [expert_counts[eid][cat] for eid in EXPERT_ORDER]
        b = ax.bar(x, heights, bottom=bottoms, color=color, label=label,
                   width=0.6, **STYLE_KWARGS)
        bars_drawn.append(b)
        bottoms += heights

    ax.set_xticks(x)
    ax.set_xticklabels([EXPERT_LABELS[e] for e in EXPERT_ORDER], fontsize=10)
    ax.set_ylabel("Number of tuples", fontsize=10)
    ax.set_ylim(0, 5)
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.legend(fontsize=8, loc="upper right", framealpha=0.9)
    ax.set_title("Expert Agreement with Pipeline Risk Rating", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(plots_dir / "2_risk_agreement.png", dpi=200, bbox_inches="tight")
    fig.savefig(plots_dir / "2_risk_agreement.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Plot 2: risk_agreement")


# =========================================================================
# Plot 3: Novel insights distribution
# =========================================================================

def plot_novel_insights(primary, plots_dir):
    categories = [
        "Yes — several new concerns",
        "Yes — one or two",
        "No — but it confirmed my existing concerns",
        "No — it missed concerns I already knew about",
    ]
    cat_short = [
        "Several new\nconcerns",
        "One or two\nnew",
        "Confirmed\nexisting",
        "Missed known\nconcerns",
    ]
    colors = ["#2ca02c", "#98df8a", "#aec7e8", "#d6604d"]

    counts = Counter()
    for r in primary:
        val = r.get("usefulness", {}).get("novel_insights", "")
        counts[val] += 1

    heights = [counts[c] for c in categories]

    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.bar(range(len(categories)), heights, color=colors, width=0.6,
                  **STYLE_KWARGS)
    for bar, h in zip(bars, heights):
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.2,
                    str(h), ha="center", va="bottom", fontsize=11,
                    fontweight="bold")

    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(cat_short, fontsize=9)
    ax.set_ylabel("Number of tuples (N=20)", fontsize=10)
    ax.set_ylim(0, max(heights) + 2)
    ax.set_title("Did the Assessment Surface New Validity Concerns?", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(plots_dir / "3_novel_insights.png", dpi=200, bbox_inches="tight")
    fig.savefig(plots_dir / "3_novel_insights.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Plot 3: novel_insights")


# =========================================================================
# Plot 4: Value vs. expert review
# =========================================================================

def plot_value_vs_expert(primary, plots_dir):
    categories = [
        "Comparable to expert review",
        "Useful complement to expert review",
        "Starting point that needs substantial revision",
        "Not useful",
    ]
    cat_short = [
        "Comparable to\nexpert review",
        "Useful\ncomplement",
        "Starting point\n(needs revision)",
        "Not\nuseful",
    ]
    colors = ["#2ca02c", "#98df8a", "#fdae61", "#d6604d"]

    counts = Counter()
    for r in primary:
        val = r.get("usefulness", {}).get("value_vs_expert", "")
        counts[val] += 1

    heights = [counts[c] for c in categories]

    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.bar(range(len(categories)), heights, color=colors, width=0.6,
                  **STYLE_KWARGS)
    for bar, h in zip(bars, heights):
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.2,
                    str(h), ha="center", va="bottom", fontsize=11,
                    fontweight="bold")

    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(cat_short, fontsize=9)
    ax.set_ylabel("Number of tuples (N=20)", fontsize=10)
    ax.set_ylim(0, max(heights) + 2)
    ax.set_title("Assessment Value Relative to Manual Expert Review", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(plots_dir / "4_value_vs_expert.png", dpi=200, bbox_inches="tight")
    fig.savefig(plots_dir / "4_value_vs_expert.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Plot 4: value_vs_expert")


# =========================================================================
# Plot 5: Confidence calibration grouped bar (per dimension)
# =========================================================================

def plot_confidence_calibration(primary, plots_dir):
    cal_categories = ["Overconfident", "About right", "Underconfident", "Cannot assess"]
    colors = ["#d6604d", "#2ca02c", "#4393c3", "#999999"]

    dim_counts = defaultdict(lambda: Counter())
    for r in primary:
        for dk in DIM_KEYS:
            val = r.get("dimensions", {}).get(dk, {}).get(
                "confidence_calibration", "")
            if val:
                dim_counts[dk][val] += 1

    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(DIM_KEYS))
    n_cats = len(cal_categories)
    bar_width = 0.18
    offsets = np.arange(n_cats) * bar_width - (n_cats - 1) * bar_width / 2

    for i, (cat, color) in enumerate(zip(cal_categories, colors)):
        heights = [dim_counts[dk][cat] for dk in DIM_KEYS]
        ax.bar(x + offsets[i], heights, bar_width, color=color, label=cat,
               **STYLE_KWARGS)

    ax.set_xticks(x)
    ax.set_xticklabels([DIM_SHORT[dk] for dk in DIM_KEYS], fontsize=11)
    ax.set_ylabel("Count (N=20 per dimension)", fontsize=10)
    ax.set_ylim(0, 22)
    ax.legend(fontsize=8, loc="upper right", framealpha=0.9)
    ax.set_title("Pipeline Confidence Calibration by Dimension", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(plots_dir / "5_confidence_calibration.png", dpi=200,
                bbox_inches="tight")
    fig.savefig(plots_dir / "5_confidence_calibration.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Plot 5: confidence_calibration")


# =========================================================================
# Plot 6: Comparative ordering agreement
# =========================================================================

def plot_comparative_ordering(comparative, plots_dir):
    code_labels = {
        "about_right": "About right",
        "regional_higher": "Regional\nhigher",
        "comparator_higher": "Comparator\nhigher",
        "equal": "Approx.\nequal",
        "cannot_assess": "Cannot\nassess",
    }
    code_order = ["about_right", "regional_higher", "comparator_higher",
                  "equal", "cannot_assess"]
    colors = ["#2ca02c", "#4393c3", "#d6604d", "#fdae61", "#999999"]

    overall_counts = Counter()
    for r in comparative:
        code = r.get("overall_ordering_code", "")
        if code:
            overall_counts[code] += 1

    dim_counts = defaultdict(lambda: Counter())
    for r in comparative:
        for dk, code in r.get("dimension_ordering_codes", {}).items():
            dim_counts[dk][code] += 1

    # === Combined plot: overall + per-dimension ===
    group_labels = ["Overall"] + [DIM_SHORT[dk] for dk in DIM_KEYS]
    n_groups = len(group_labels)

    # === Room to grow data ===
    rtg_vals = [r["room_to_grow"] for r in comparative
                if r.get("room_to_grow") is not None]
    rtg_mean = np.mean(rtg_vals) if rtg_vals else 0
    rtg_std = np.std(rtg_vals) if rtg_vals else 0

    # === Two-panel figure: ordering (left) + room to grow (right) ===
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11, 4),
                                  gridspec_kw={"width_ratios": [5, 1],
                                               "wspace": 0.35})

    # --- Left panel: ordering agreement ---
    x = np.arange(n_groups)
    n_cats = len(code_order)
    bar_width = 0.14
    offsets = np.arange(n_cats) * bar_width - (n_cats - 1) * bar_width / 2

    for i, (code, color) in enumerate(zip(code_order, colors)):
        heights = [overall_counts[code]]
        for dk in DIM_KEYS:
            heights.append(dim_counts[dk][code])
        ax.bar(x + offsets[i], heights, bar_width, color=color,
               label=code_labels[code], **STYLE_KWARGS)

    ax.axvline(0.5, color="#cccccc", linewidth=0.8, linestyle="--")
    ax.set_xticks(x)
    ax.set_xticklabels(group_labels, fontsize=10)
    ax.set_ylabel("Count (N=10 pairs)", fontsize=10)
    ax.set_ylim(0, 12)
    ax.legend(fontsize=8, loc="upper right", ncol=2, framealpha=0.9)
    ax.set_title("Ordering Agreement", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # --- Right panel: room to grow ---
    bar = ax2.bar([0], [rtg_mean], yerr=[rtg_std], capsize=5,
                  color="#5a9bd5", width=0.45,
                  error_kw={"linewidth": 1.2}, **STYLE_KWARGS)
    ax2.text(0, rtg_mean + rtg_std + 0.15, f"{rtg_mean:.1f}",
             ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax2.set_xticks([0])
    ax2.set_xticklabels(["Room to\nGrow"], fontsize=10)
    ax2.set_ylabel("Mean Likert (1–5)", fontsize=10)
    ax2.set_ylim(0, 5.8)
    ax2.axhline(y=3, color="#cccccc", linewidth=0.8, linestyle="--")
    ax2.set_title("Score Headroom", fontsize=11)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle("Expert Agreement with Comparative Benchmark Ordering",
                 fontsize=12, y=1.02)
    fig.savefig(plots_dir / "6_comparative_ordering.png", dpi=200,
                bbox_inches="tight")
    fig.savefig(plots_dir / "6_comparative_ordering.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Plot 6: comparative_ordering (with room-to-grow panel)")


# =========================================================================
# Plot 7: Regional vs. comparator pipeline scores by dimension
# =========================================================================

def plot_regional_vs_comparator(primary, assessments_dir, plots_dir):
    assessments_dir = Path(assessments_dir)

    # === Regional scores from primary assessments (already loaded) ===
    regional_vals = defaultdict(list)
    for r in primary:
        for dk in DIM_KEYS:
            v = r.get("pipeline_scores", {}).get(dk)
            if v is not None:
                regional_vals[dk].append(v)

    # === Comparator scores from assessments directory ===
    comp_vals = defaultdict(list)
    for expert_bench_dir in sorted(assessments_dir.glob("expert_*")):
        if not expert_bench_dir.is_dir():
            continue
        parts = expert_bench_dir.name.split("__", 1)
        if len(parts) != 2:
            continue
        benchmark_slug = parts[1]
        if benchmark_slug not in COMPARATOR_BENCHMARKS:
            continue
        for slug_dir in sorted(expert_bench_dir.iterdir()):
            scoring_path = slug_dir / "scoring.json"
            if not scoring_path.exists():
                continue
            scoring = json.loads(scoring_path.read_text())
            dims = scoring.get("dimensions", {})
            for dk in DIM_KEYS:
                v = dims.get(dk, {}).get("score")
                if v is not None:
                    comp_vals[dk].append(v)

    n_regional = len(regional_vals[DIM_KEYS[0]])
    n_comp = len(comp_vals[DIM_KEYS[0]])

    if not n_comp:
        print("  Plot 7: SKIPPED (no comparator scoring.json found in "
              f"{assessments_dir})")
        return

    # === Compute means and stds ===
    r_means = [np.mean(regional_vals[dk]) for dk in DIM_KEYS]
    r_stds = [np.std(regional_vals[dk]) for dk in DIM_KEYS]
    c_means = [np.mean(comp_vals[dk]) for dk in DIM_KEYS]
    c_stds = [np.std(comp_vals[dk]) for dk in DIM_KEYS]

    # === Plot ===
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(DIM_KEYS))
    w = 0.32

    bars_r = ax.bar(x - w / 2, r_means, w, yerr=r_stds, capsize=4,
                    color="#5a9bd5", label=f"Regional (N={n_regional})",
                    error_kw={"linewidth": 1.0}, **STYLE_KWARGS)
    bars_c = ax.bar(x + w / 2, c_means, w, yerr=c_stds, capsize=4,
                    color="#ed7d31", label=f"Global comparator (N={n_comp})",
                    error_kw={"linewidth": 1.0}, **STYLE_KWARGS)

    for bar, m, s in zip(bars_r, r_means, r_stds):
        ax.text(bar.get_x() + bar.get_width() / 2, m + s + 0.12,
                f"{m:.1f}", ha="center", va="bottom", fontsize=9,
                fontweight="bold", color="#3a6fa0")
    for bar, m, s in zip(bars_c, c_means, c_stds):
        ax.text(bar.get_x() + bar.get_width() / 2, m + s + 0.12,
                f"{m:.1f}", ha="center", va="bottom", fontsize=9,
                fontweight="bold", color="#b85d1e")

    ax.set_xticks(x)
    ax.set_xticklabels([DIM_SHORT[dk] for dk in DIM_KEYS], fontsize=11)
    ax.set_ylabel("Pipeline score (1–5)", fontsize=10)
    ax.set_ylim(0, 5.8)
    ax.axhline(y=3, color="#cccccc", linewidth=0.8, linestyle="--")
    ax.legend(fontsize=9, loc="upper right", framealpha=0.9)
    ax.set_title(
        "Pipeline Validity Scores: Regional vs. Global Comparator Benchmarks",
        fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    r_grand = np.mean([v for dk in DIM_KEYS for v in regional_vals[dk]])
    c_grand = np.mean([v for dk in DIM_KEYS for v in comp_vals[dk]])
    ax.annotate(
        f"Grand mean — Regional: {r_grand:.2f}  |  Comparator: {c_grand:.2f}",
        xy=(0.5, 0.02), xycoords="axes fraction", ha="center",
        fontsize=9, color="#555555")

    fig.tight_layout()
    fig.savefig(plots_dir / "7_regional_vs_comparator.png", dpi=200,
                bbox_inches="tight")
    fig.savefig(plots_dir / "7_regional_vs_comparator.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Plot 7: regional_vs_comparator")


# =========================================================================
# Main
# =========================================================================

def main():
    p = argparse.ArgumentParser(
        description="Generate summary plots from Stage 3 expert responses")
    p.add_argument("--results-dir", default="stage3_results",
                   help="Path to results directory (default: stage3_results/)")
    p.add_argument("--assessments-dir", default="assessments",
                   help="Path to assessments directory (default: assessments/)")
    args = p.parse_args()

    primary, comparative = load_data(args.results_dir)
    plots_dir = Path(args.results_dir) / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating plots from {len(primary)} primary + "
          f"{len(comparative)} comparative results...\n")

    plot_heatmap(primary, plots_dir)
    plot_likert_grand_mean(primary, plots_dir)
    plot_risk_agreement(primary, plots_dir)
    plot_novel_insights(primary, plots_dir)
    plot_value_vs_expert(primary, plots_dir)
    plot_confidence_calibration(primary, plots_dir)
    plot_comparative_ordering(comparative, plots_dir)
    plot_regional_vs_comparator(primary, args.assessments_dir, plots_dir)

    print(f"\nDone. Plots saved to {plots_dir}/")


if __name__ == "__main__":
    main()
