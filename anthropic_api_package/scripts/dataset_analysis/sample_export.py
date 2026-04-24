#!/usr/bin/env python3
"""Export N formatted examples for direct LLM reading.

Usage:
    python sample_export.py \
        --repo_id sentence-transformers/parallel-sentences-ccmatrix \
        --config en-lb --split train --n 5 --columns en lb
"""

import argparse
import json
import os
import sys

from datasets import load_dataset
from tqdm import tqdm


def format_value(val, max_len=300):
    """Format a value for display, truncating if needed."""
    s = str(val)
    if len(s) > max_len:
        return s[:max_len] + "..."
    return s


def main():
    parser = argparse.ArgumentParser(description="Export formatted examples for LLM reading")
    parser.add_argument("--repo_id", required=True)
    parser.add_argument("--config", default=None)
    parser.add_argument("--split", default="train")
    parser.add_argument("--n", type=int, default=5, help="Number of examples to export")
    parser.add_argument("--columns", nargs="*", default=None, help="Columns to include (default: all)")
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
        json.dump({"script": "sample_export", "error": str(e)}, sys.stdout, indent=2)
        return

    samples = list(tqdm(ds.take(args.n), total=args.n, desc="Exporting samples"))

    # Determine columns
    if args.columns:
        columns = args.columns
    elif samples:
        columns = list(samples[0].keys())
    else:
        columns = []

    # Build markdown-formatted examples
    examples = []
    for i, sample in enumerate(samples):
        example = {"index": i + 1}
        for col in columns:
            val = sample.get(col, "<missing>")
            example[col] = format_value(val)
        examples.append(example)

    # Also build a markdown string for direct LLM consumption
    md_lines = [f"## Sample Examples ({len(examples)} of {args.n} requested)\n"]
    for ex in examples:
        md_lines.append(f"### Example {ex['index']} (config={args.config}, split={args.split})")
        for col in columns:
            md_lines.append(f"- **{col}**: {ex.get(col, '<missing>')}")
        md_lines.append("")

    result = {
        "script": "sample_export",
        "repo_id": args.repo_id,
        "config": args.config,
        "split": args.split,
        "n_exported": len(examples),
        "columns": columns,
        "examples": examples,
        "markdown": "\n".join(md_lines),
    }
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
