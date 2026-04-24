#!/usr/bin/env python3
"""Schema probe: stream a few examples to extract actual column types and sample values.

Usage:
    python schema_probe.py \
        --repo_id sentence-transformers/parallel-sentences-ccmatrix \
        --config en-lb --split train
"""

import argparse
import json
import os
import sys

from datasets import load_dataset
from tqdm import tqdm


def infer_type(val):
    """Infer the type of a value for schema reporting."""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "bool"
    if isinstance(val, int):
        return "int"
    if isinstance(val, float):
        return "float"
    if isinstance(val, str):
        return "string"
    if isinstance(val, list):
        if len(val) == 0:
            return "list[empty]"
        inner = infer_type(val[0])
        return f"list[{inner}]"
    if isinstance(val, dict):
        return "dict"
    if isinstance(val, bytes):
        return "bytes"
    return type(val).__name__


def truncate(val, max_len=100):
    """Truncate a value for preview."""
    s = str(val)
    if len(s) > max_len:
        return s[:max_len] + "..."
    return s


def main():
    parser = argparse.ArgumentParser(description="Schema probe via streaming")
    parser.add_argument("--repo_id", required=True)
    parser.add_argument("--config", default=None)
    parser.add_argument("--split", default="train")
    parser.add_argument("--n", type=int, default=5, help="Number of examples to probe")
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
        json.dump({"script": "schema_probe", "error": str(e)}, sys.stdout, indent=2)
        return

    samples = list(tqdm(ds.take(args.n), total=args.n, desc="Probing schema"))

    if not samples:
        json.dump({"script": "schema_probe", "error": "No samples returned"}, sys.stdout, indent=2)
        return

    # Infer schema from all probed samples
    columns = list(samples[0].keys())
    schema = {}
    for col in columns:
        types_seen = set()
        null_count = 0
        for s in samples:
            val = s.get(col)
            if val is None:
                null_count += 1
            types_seen.add(infer_type(val))
        schema[col] = {
            "types_observed": sorted(types_seen),
            "null_count": null_count,
            "sample_values": [truncate(s.get(col)) for s in samples[:3]],
        }

    result = {
        "script": "schema_probe",
        "repo_id": args.repo_id,
        "config": args.config,
        "split": args.split,
        "n_probed": len(samples),
        "columns": columns,
        "schema": schema,
    }
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
