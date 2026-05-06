#!/usr/bin/env python3
"""Label frequency, entropy, and cross-split divergence analysis.

Usage:
    python label_stats.py \
        --repo_id masakhane/masakhaner2 \
        --config bam --column ner_tags --splits train test --sample_size 500
"""

import argparse
import json
import os
import sys
from collections import Counter

import numpy as np
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon
from datasets import load_dataset
from tqdm import tqdm


def compute_label_stats(labels):
    """Compute frequency, entropy, and class balance for a list of labels."""
    counts = Counter(labels)
    total = sum(counts.values())
    freqs = np.array([c / total for c in counts.values()])
    ent = float(entropy(freqs, base=2))
    max_ent = float(np.log2(len(counts))) if len(counts) > 1 else 0
    return {
        "unique_labels": len(counts),
        "total_count": total,
        "label_counts": dict(counts.most_common()),
        "entropy_bits": round(ent, 3),
        "max_entropy_bits": round(max_ent, 3),
        "normalized_entropy": round(ent / max_ent, 3) if max_ent > 0 else 0,
    }


def compute_js_divergence(labels_a, labels_b):
    """Jensen-Shannon divergence between two label distributions."""
    all_labels = sorted(set(list(labels_a.keys()) + list(labels_b.keys())))
    total_a = sum(labels_a.values())
    total_b = sum(labels_b.values())
    if total_a == 0 or total_b == 0:
        return None
    p = np.array([labels_a.get(l, 0) / total_a for l in all_labels])
    q = np.array([labels_b.get(l, 0) / total_b for l in all_labels])
    return round(float(jensenshannon(p, q)), 4)


def flatten_labels(sample, column):
    """Extract labels from a sample, handling both flat and sequence columns."""
    val = sample.get(column)
    if val is None:
        return []
    if isinstance(val, list):
        return [str(v) for v in val]
    return [str(val)]


def main():
    parser = argparse.ArgumentParser(description="Label distribution analysis")
    parser.add_argument("--repo_id", required=True)
    parser.add_argument("--config", default=None)
    parser.add_argument("--column", required=True, help="Label column name")
    parser.add_argument("--splits", nargs="+", default=["train"], help="Splits to analyze")
    parser.add_argument("--sample_size", type=int, default=500)
    parser.add_argument("--token", default=None)
    args = parser.parse_args()

    token = args.token or os.environ.get("HF_TOKEN")

    per_split = {}
    split_counts = {}

    for split in args.splits:
        load_kwargs = {"path": args.repo_id, "split": split, "streaming": True}
        if args.config:
            load_kwargs["name"] = args.config
        if token:
            load_kwargs["token"] = token

        try:
            ds = load_dataset(**load_kwargs)
        except Exception as e:
            per_split[split] = {"error": str(e)}
            continue

        samples = list(tqdm(ds.take(args.sample_size), total=args.sample_size, desc=f"Split: {split}"))

        all_labels = []
        for s in samples:
            all_labels.extend(flatten_labels(s, args.column))

        if not all_labels:
            per_split[split] = {"error": f"No labels found in column '{args.column}'"}
            continue

        stats = compute_label_stats(all_labels)
        per_split[split] = stats
        split_counts[split] = Counter(all_labels)

    # Cross-split JS divergence
    cross_split = {}
    split_names = [s for s in args.splits if s in split_counts]
    for i, s1 in enumerate(split_names):
        for s2 in split_names[i+1:]:
            key = f"{s1}_vs_{s2}"
            js = compute_js_divergence(split_counts[s1], split_counts[s2])
            if js is not None:
                cross_split[key] = js

    # Anomaly detection
    anomalies = []
    for split, stats in per_split.items():
        if "error" in stats:
            continue
        if stats.get("normalized_entropy", 1.0) < 0.5:
            anomalies.append(
                f"Split '{split}': low normalized entropy ({stats['normalized_entropy']}) "
                f"suggests severe class imbalance"
            )
    for key, js in cross_split.items():
        if js > 0.1:
            anomalies.append(
                f"Cross-split divergence {key}: JS={js} (>0.1 suggests different label distributions)"
            )

    result = {
        "script": "label_stats",
        "repo_id": args.repo_id,
        "config": args.config,
        "column": args.column,
        "sample_size": args.sample_size,
        "per_split": per_split,
        "cross_split_js_divergence": cross_split,
        "anomalies": anomalies,
    }
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
