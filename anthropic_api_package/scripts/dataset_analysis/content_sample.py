#!/usr/bin/env python3
"""Content-focused example sampler for validity assessment.

Streams examples from a HuggingFace dataset and fills to a character
budget. When a ClassLabel column exists, samples round-robin across
classes for diversity. Outputs clean markdown for LLM content analysis.

Usage:
    python content_sample.py --repo_id DrBenchmark/QUAERO
    python content_sample.py --repo_id DrBenchmark/FrenchMedMCQA --char_budget 80000
"""

import argparse
import json
import os
import random
import sys
from collections import Counter, defaultdict

from datasets import load_dataset, Audio, ClassLabel, Image, Sequence
from tqdm import tqdm

_MAX_FIELD_CHARS = 5000
_DEFAULT_CHAR_BUDGET = 50_000
_DEFAULT_MIN_EXAMPLES = 5
_DEFAULT_BUFFER = 500


def _skip_column(feat):
    """True for columns containing non-text media (Image, Audio)."""
    if isinstance(feat, (Image, Audio)):
        return True
    if isinstance(feat, Sequence) and isinstance(feat.feature, (Image, Audio)):
        return True
    return False


def _find_label_column(features):
    """Find the best simple ClassLabel column for stratification."""
    for name in ("label", "labels"):
        if name in features and isinstance(features[name], ClassLabel):
            return name
    for name, feat in features.items():
        if isinstance(feat, ClassLabel):
            return name
    return None


def _format_value(val):
    """Format a value for markdown display."""
    if val is None:
        return "*null*"
    if isinstance(val, list):
        s = str(val)
        if len(s) > _MAX_FIELD_CHARS:
            return s[:_MAX_FIELD_CHARS] + f"... [{len(val)} items total]"
        return s
    s = str(val)
    if len(s) > _MAX_FIELD_CHARS:
        return s[:_MAX_FIELD_CHARS] + "..."
    return s


def _example_chars(row, show_cols):
    """Approximate character cost of rendering one example."""
    return sum(len(_format_value(row.get(col))) for col in show_cols)


def _select_examples(buffer, show_cols, char_budget, min_examples, label_col=None):
    """Fill to char_budget, with round-robin across classes when stratifying."""
    selected = []
    total_chars = 0

    def _accept(row):
        nonlocal total_chars
        cost = _example_chars(row, show_cols)
        if len(selected) >= min_examples and total_chars + cost > char_budget:
            return False
        selected.append(row)
        total_chars += cost
        return True

    if label_col is not None:
        by_label = defaultdict(list)
        for row in buffer:
            by_label[row[label_col]].append(row)

        cursors = {lbl: 0 for lbl in by_label}
        while cursors:
            exhausted = []
            for lbl in sorted(cursors):
                idx = cursors[lbl]
                if idx >= len(by_label[lbl]):
                    exhausted.append(lbl)
                    continue
                if not _accept(by_label[lbl][idx]):
                    return selected
                cursors[lbl] = idx + 1
            for lbl in exhausted:
                del cursors[lbl]
    else:
        for row in buffer:
            if not _accept(row):
                break

    return selected


def main():
    parser = argparse.ArgumentParser(
        description="Content-focused example sampler for validity assessment")
    parser.add_argument("--repo_id", required=True)
    parser.add_argument("--config", default=None)
    parser.add_argument("--split", default="train")
    parser.add_argument("--char_budget", type=int, default=_DEFAULT_CHAR_BUDGET,
                        help="Target character budget for sampled content")
    parser.add_argument("--min_examples", type=int, default=_DEFAULT_MIN_EXAMPLES,
                        help="Minimum examples regardless of budget")
    parser.add_argument("--buffer_size", type=int, default=_DEFAULT_BUFFER,
                        help="Rows to stream into selection buffer")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for shuffling buffer")
    parser.add_argument("--token", default=None)
    args = parser.parse_args()

    token = args.token or os.environ.get("HF_TOKEN")

    load_kwargs = {"path": args.repo_id, "split": args.split, "streaming": True}
    if args.config:
        load_kwargs["name"] = args.config
    if token:
        load_kwargs["token"] = token

    try:
        ds = load_dataset(**load_kwargs)
    except Exception as e:
        json.dump({"script": "content_sample", "error": str(e)},
                  sys.stdout, indent=2)
        return

    features = ds.features
    skip_cols = {name for name, feat in features.items() if _skip_column(feat)}
    show_cols = [name for name in features if name not in skip_cols]

    label_col = _find_label_column(features)
    label_names = features[label_col].names if label_col else None

    buffer = list(tqdm(ds.take(args.buffer_size), total=args.buffer_size,
                       desc="Streaming"))

    random.seed(args.seed)
    random.shuffle(buffer)

    examples = _select_examples(
        buffer, show_cols, args.char_budget, args.min_examples, label_col)

    total_chars = sum(_example_chars(r, show_cols) for r in examples)

    # === Build markdown ===
    md = []

    if label_col and label_names:
        dist = Counter(row[label_col] for row in buffer)
        md.append(f"**Stratified on** `{label_col}` ({len(label_names)} classes)")
        md.append(f"**Buffer** (n={len(buffer)}):")
        for idx in sorted(dist):
            name = label_names[idx] if idx < len(label_names) else f"class_{idx}"
            md.append(f"  {name}: {dist[idx]}")
        md.append("")

    md.append(f"**Examples:** {len(examples)} from `{args.split}` split "
              f"({total_chars:,} chars)")
    md.append(f"**Columns:** {', '.join(show_cols)}")
    if skip_cols:
        md.append(f"**Skipped (media):** {', '.join(sorted(skip_cols))}")
    md.append("\n---\n")

    for i, row in enumerate(examples, 1):
        header = f"### Example {i}"
        if label_col and label_names:
            idx = row.get(label_col)
            if idx is not None and idx < len(label_names):
                header += f" [{label_names[idx]}]"
        md.append(header)
        md.append("")
        for col in show_cols:
            md.append(f"**{col}:** {_format_value(row.get(col))}")
        md.append("\n---\n")

    markdown = "\n".join(md)

    result = {
        "script": "content_sample",
        "repo_id": args.repo_id,
        "config": args.config,
        "split": args.split,
        "n_exported": len(examples),
        "total_chars": total_chars,
        "char_budget": args.char_budget,
        "columns_shown": show_cols,
        "columns_skipped": sorted(skip_cols),
        "stratified_on": label_col,
        "label_names": label_names,
        "markdown": markdown,
    }
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
