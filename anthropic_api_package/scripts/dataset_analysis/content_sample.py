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


# Returns True if this feature type should be excluded from text output
# (binary blobs are useless noise for an LLM reading the content)
def _skip_column(feat):
    """True for columns containing non-text media (Image, Audio)."""
    if isinstance(feat, (Image, Audio)):
        return True
    # Also skip sequences of media, e.g. a list-of-images column
    if isinstance(feat, Sequence) and isinstance(feat.feature, (Image, Audio)):
        return True
    return False


# Returns the column name to use for class-stratified sampling, or None
# if the dataset has no suitable ClassLabel column.
# Checks canonical names first ("label", "labels") before falling back
# to any ClassLabel column — avoids misidentifying auxiliary label fields.
def _find_label_column(features):
    """Find the best simple ClassLabel column for stratification."""
    for name in ("label", "labels"):
        if name in features and isinstance(features[name], ClassLabel):
            return name
    # Fallback: first ClassLabel column found by iteration order
    for name, feat in features.items():
        if isinstance(feat, ClassLabel):
            return name
    return None


# Returns a markdown-safe string representation of a single field value.
# Hard-truncates long values so one large field can't blow the character budget.
def _format_value(val):
    """Format a value for markdown display."""
    if val is None:
        return "*null*"
    if isinstance(val, list):
        s = str(val)
        # Append item count so the reader knows how much was cut
        if len(s) > _MAX_FIELD_CHARS:
            return s[:_MAX_FIELD_CHARS] + f"... [{len(val)} items total]"
        return s
    s = str(val)
    if len(s) > _MAX_FIELD_CHARS:
        return s[:_MAX_FIELD_CHARS] + "..."
    return s


# Returns an integer character count for one dataset row across all displayed columns.
# Used to track budget consumption before committing a row to the output.
def _example_chars(row, show_cols):
    """Approximate character cost of rendering one example."""
    return sum(len(_format_value(row.get(col))) for col in show_cols)


# Returns a list of rows that fit within char_budget, selecting greedily
# in round-robin class order when label_col is provided.
# min_examples acts as a floor: the first N examples are always included
# regardless of budget so the output is never empty on small datasets.
def _select_examples(buffer, show_cols, char_budget, min_examples, label_col=None):
    """Fill to char_budget, with round-robin across classes when stratifying."""
    selected = []
    total_chars = 0

    # Closure captures selected/total_chars so the greedy accept logic
    # stays in one place and is reused by both code paths below.
    def _accept(row):
        nonlocal total_chars
        cost = _example_chars(row, show_cols)
        # Always accept until min_examples is reached, then gate on budget
        if len(selected) >= min_examples and total_chars + cost > char_budget:
            return False
        selected.append(row)
        total_chars += cost
        return True

    # === Stratified path: interleave examples across class labels ===
    # Round-robin ensures every class appears in the output even when
    # the budget is tight and one class dominates the buffer.
    if label_col is not None:
        by_label = defaultdict(list)
        for row in buffer:
            by_label[row[label_col]].append(row)

        # Per-class cursor tracks how far we've consumed each class's rows
        cursors = {lbl: 0 for lbl in by_label}
        while cursors:
            exhausted = []
            # Sort for deterministic ordering across runs
            for lbl in sorted(cursors):
                idx = cursors[lbl]
                if idx >= len(by_label[lbl]):
                    exhausted.append(lbl)
                    continue
                # Budget exceeded mid-round — stop immediately (no partial round)
                if not _accept(by_label[lbl][idx]):
                    return selected
                cursors[lbl] = idx + 1
            # Remove labels whose rows are fully consumed
            for lbl in exhausted:
                del cursors[lbl]

    # === Non-stratified path: simple sequential greedy fill ===
    else:
        for row in buffer:
            if not _accept(row):
                break

    return selected


def main():
    # === Argument parsing ===
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

    # === Dataset loading ===
    # Prefer CLI token, fall back to standard HF environment variable
    token = args.token or os.environ.get("HF_TOKEN")

    load_kwargs = {"path": args.repo_id, "split": args.split, "streaming": True}
    if args.config:
        load_kwargs["name"] = args.config
    if token:
        load_kwargs["token"] = token

    # Emit structured JSON error so the pipeline step can parse failures uniformly
    try:
        ds = load_dataset(**load_kwargs)
    except Exception as e:
        json.dump({"script": "content_sample", "error": str(e)},
                  sys.stdout, indent=2)
        return

    # === Column filtering ===
    # Build the set of columns to display, dropping media blobs that
    # can't be rendered as text (images, audio, sequences of either)
    features = ds.features
    skip_cols = {name for name, feat in features.items() if _skip_column(feat)}
    show_cols = [name for name in features if name not in skip_cols]

    # Detect label column for stratification; label_names maps int → class string
    label_col = _find_label_column(features)
    label_names = features[label_col].names if label_col else None

    # === Buffer streaming ===
    # Pull a fixed-size prefix from the stream so selection is fast and
    # reproducible — full dataset iteration would be slow and unnecessary
    buffer = list(tqdm(ds.take(args.buffer_size), total=args.buffer_size,
                       desc="Streaming"))

    # Shuffle before selection so the sample isn't biased toward the
    # dataset's natural ordering (e.g., all examples of one domain first)
    random.seed(args.seed)
    random.shuffle(buffer)

    # === Example selection ===
    examples = _select_examples(
        buffer, show_cols, args.char_budget, args.min_examples, label_col)

    total_chars = sum(_example_chars(r, show_cols) for r in examples)

    # === Build markdown ===
    # The markdown block is embedded in the JSON output so the pipeline
    # step can pass it verbatim to an LLM prompt without extra parsing.
    md = []

    # Show class distribution over the buffer (not just selected examples)
    # so the downstream analyst can see whether the sample is representative
    if label_col and label_names:
        dist = Counter(row[label_col] for row in buffer)
        md.append(f"**Stratified on** `{label_col}` ({len(label_names)} classes)")
        md.append(f"**Buffer** (n={len(buffer)}):")
        for idx in sorted(dist):
            # Guard against label indices that exceed the names list
            name = label_names[idx] if idx < len(label_names) else f"class_{idx}"
            md.append(f"  {name}: {dist[idx]}")
        md.append("")

    md.append(f"**Examples:** {len(examples)} from `{args.split}` split "
              f"({total_chars:,} chars)")
    md.append(f"**Columns:** {', '.join(show_cols)}")
    if skip_cols:
        md.append(f"**Skipped (media):** {', '.join(sorted(skip_cols))}")
    md.append("\n---\n")

    # Render each example as a named section with optional class label in the header
    for i, row in enumerate(examples, 1):
        header = f"### Example {i}"
        if label_col and label_names:
            idx = row.get(label_col)
            # Only annotate header if the label resolves to a known class name
            if idx is not None and idx < len(label_names):
                header += f" [{label_names[idx]}]"
        md.append(header)
        md.append("")
        for col in show_cols:
            md.append(f"**{col}:** {_format_value(row.get(col))}")
        md.append("\n---\n")

    markdown = "\n".join(md)

    # === JSON output ===
    # Structured result consumed by the pipeline orchestrator;
    # the "markdown" field is what gets forwarded to the LLM
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
