#!/usr/bin/env python3
"""Generate heatmap visualization for validity analysis results."""

import json
import glob
import os
import numpy as np
import yaml
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
BENCHMARKS_DIR = os.path.join(BASE_DIR, 'benchmarks')

DIMS = ['input_ontology', 'input_content', 'input_form',
        'output_ontology', 'output_content', 'output_form']
DIM_LABELS = ['Input\nOntology', 'Input\nContent', 'Input\nForm',
              'Output\nOntology', 'Output\nContent', 'Output\nForm']

STRATEGY_ORDER = ['ground_up', 'mixed', 'adapted', 'regional_exams',
                  'parallel', 'translation', 'none', 'unknown']
STRATEGY_LABELS = {
    'ground_up': 'Ground-Up', 'mixed': 'Mixed', 'adapted': 'Adapted',
    'regional_exams': 'Regional Exams', 'parallel': 'Parallel',
    'translation': 'Translation', 'none': 'Western Baseline', 'unknown': 'Unknown'
}
STRATEGY_COLORS = {
    'ground_up': '#27AE60', 'mixed': '#2ECC71', 'adapted': '#F39C12',
    'regional_exams': '#E67E22', 'parallel': '#3498DB',
    'translation': '#E74C3C', 'none': '#8E44AD', 'unknown': '#95A5A6'
}

REGION_SHORT = {
    'sub_saharan_africa': 'SSA', 'Sub-Saharan Africa': 'SSA',
    'southeast_asia': 'SEA', 'Southeast Asia': 'SEA',
    'east_asia': 'EA', 'latin_america_indigenous': 'LatAm',
    'iran_persian': 'Iran', 'iberian': 'Iberian', 'mena': 'MENA'
}


def load_results():
    rows = []
    # Pre-load benchmark YAMLs
    bench_map = {}
    for yf in glob.glob(os.path.join(BENCHMARKS_DIR, '*.yaml')):
        yd = yaml.safe_load(open(yf))
        key = yd.get('name', '').lower().replace('-', '').replace(' ', '').replace('_', '')
        bench_map[key] = yd.get('porting_strategy', 'unknown')

    for f in sorted(glob.glob(os.path.join(RESULTS_DIR, '*.json'))):
        data = json.load(open(f))
        b = data.get('benchmark', '')
        r = data.get('region', '')
        scores = []
        for d in DIMS:
            val = data.get('dimensions', {}).get(d)
            if isinstance(val, (int, float)):
                scores.append(int(val))
            elif isinstance(val, dict):
                scores.append(val.get('score', 0))
            else:
                scores.append(0)
        avg = sum(scores) / len(scores)

        bkey = b.lower().replace('-', '').replace(' ', '').replace('_', '')
        strat = bench_map.get(bkey, 'unknown')

        region_short = REGION_SHORT.get(r, r.replace('_', ' ').title())
        display = f"{b.upper()} \u2192 {region_short}"
        rows.append((display, b, r, strat, scores, avg))
    return rows


def generate_heatmap(rows, output_prefix='validity_heatmap'):
    # Sort by strategy then avg descending
    def sort_key(row):
        strat = row[3]
        si = STRATEGY_ORDER.index(strat) if strat in STRATEGY_ORDER else len(STRATEGY_ORDER)
        return (si, -row[5])
    rows.sort(key=sort_key)

    n_benchmarks = len(rows)
    n_dims = len(DIMS)
    matrix = np.zeros((n_benchmarks, n_dims))
    labels_list = []
    strats_list = []
    avgs_list = []
    for i, (display, b, r, strat, scores, avg) in enumerate(rows):
        matrix[i] = scores
        labels_list.append(display)
        strats_list.append(strat)
        avgs_list.append(avg)

    # Figure
    fig_height = max(10, n_benchmarks * 0.38 + 3)
    fig, ax = plt.subplots(figsize=(10, fig_height))
    fig.patch.set_facecolor('white')

    # Colormap
    cmap = mcolors.LinearSegmentedColormap.from_list(
        'validity', ['#C0392B', '#E74C3C', '#F39C12', '#F1C40F', '#2ECC71', '#27AE60'], N=256)
    norm = mcolors.Normalize(vmin=1, vmax=5)

    im = ax.imshow(matrix, cmap=cmap, norm=norm, aspect='auto', interpolation='nearest')

    # Score text in cells
    for i in range(n_benchmarks):
        for j in range(n_dims):
            val = int(matrix[i, j])
            text_color = 'white' if val <= 2 else '#2C3E50'
            ax.text(j, i, str(val), ha='center', va='center',
                    fontsize=11, fontweight='bold', color=text_color)

    # Strategy color strip on left
    for i, strat in enumerate(strats_list):
        color = STRATEGY_COLORS.get(strat, '#95A5A6')
        rect = plt.Rectangle((-0.85, i - 0.4), 0.25, 0.8,
                              facecolor=color, edgecolor='none', clip_on=False)
        ax.add_patch(rect)

    # Group dividers
    prev_strat = None
    for i, strat in enumerate(strats_list):
        if prev_strat is not None and strat != prev_strat:
            ax.axhline(y=i - 0.5, color='#2C3E50', linewidth=2, linestyle='-')
        prev_strat = strat

    # Axes
    ax.set_xticks(range(n_dims))
    ax.set_xticklabels(DIM_LABELS, fontsize=10, fontweight='bold')
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.set_yticks(range(n_benchmarks))
    ax.set_yticklabels(labels_list, fontsize=8.5, ha='right')

    # Avg annotations
    for i, avg in enumerate(avgs_list):
        color = '#C0392B' if avg < 2.0 else '#E67E22' if avg < 3.0 else '#27AE60' if avg >= 3.5 else '#2C3E50'
        ax.annotate(f'{avg:.1f}', xy=(1.02, i), xycoords=('axes fraction', 'data'),
                    fontsize=9, fontweight='bold', color=color, va='center', ha='left',
                    annotation_clip=False)

    ax.annotate('Avg', xy=(1.02, -1.2), xycoords=('axes fraction', 'data'),
                fontsize=10, fontweight='bold', color='#2C3E50', va='center', ha='left',
                annotation_clip=False)

    # Strategy legend
    seen = set()
    legend_items = []
    for strat in strats_list:
        if strat not in seen:
            seen.add(strat)
            legend_items.append(strat)

    legend_patches = [plt.Rectangle((0, 0), 1, 1, facecolor=STRATEGY_COLORS.get(s, '#95A5A6'),
                                     edgecolor='none') for s in legend_items]
    legend_lbls = [STRATEGY_LABELS.get(s, s) for s in legend_items]
    leg = ax.legend(legend_patches, legend_lbls,
                    title='Porting Strategy', title_fontsize=10,
                    loc='upper center', bbox_to_anchor=(0.5, -0.02),
                    fontsize=9, frameon=True, fancybox=True,
                    edgecolor='#CCCCCC', ncol=4)
    leg.get_frame().set_facecolor('white')

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.08,
                         shrink=0.55, aspect=25)
    cbar.set_ticks([1, 2, 3, 4, 5])
    cbar.set_ticklabels(['1 Major\nviolations', '2 Significant\nconcerns',
                          '3 Partially\naddressed', '4 Well\naddressed',
                          '5 No\nconcerns'])
    cbar.ax.tick_params(labelsize=8)

    # Grid
    for i in range(n_dims + 1):
        ax.axvline(x=i - 0.5, color='white', linewidth=1.5)
    for i in range(n_benchmarks + 1):
        ax.axhline(y=i - 0.5, color='white', linewidth=0.5)

    ax.set_xlim(-0.5, n_dims - 0.5)
    ax.set_title('Validity Analysis: 32 AI Benchmarks \u00d7 7 Global South Regions\n',
                 fontsize=14, fontweight='bold', color='#2C3E50', pad=15)

    plt.tight_layout()
    out_png = os.path.join(RESULTS_DIR, f'{output_prefix}.png')
    out_pdf = os.path.join(RESULTS_DIR, f'{output_prefix}.pdf')
    plt.savefig(out_png, bbox_inches='tight', dpi=300, facecolor='white')
    plt.savefig(out_pdf, bbox_inches='tight', dpi=300, facecolor='white')
    print(f"Saved: {out_png}")
    print(f"Saved: {out_pdf}")
    plt.close()


if __name__ == '__main__':
    rows = load_results()
    generate_heatmap(rows)
