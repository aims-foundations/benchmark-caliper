#!/usr/bin/env python3
"""Text statistics: length distribution, encoding detection, script histogram.

Usage:
    python text_stats.py \
        --repo_id sentence-transformers/parallel-sentences-ccmatrix \
        --config en-lb --split train --columns en lb --sample_size 200
"""

import argparse
import json
import os
import sys
import unicodedata
from collections import Counter

import numpy as np
from charset_normalizer import from_bytes
from datasets import load_dataset
from tqdm import tqdm


def unicode_script_histogram(text):
    """Count characters by Unicode script."""
    scripts = Counter()
    for ch in text:
        if ch.isspace() or ch in '.,;:!?-"\'()[]{}':
            continue
        try:
            name = unicodedata.name(ch, "UNKNOWN")
            if "LATIN" in name:
                scripts["Latin"] += 1
            elif "ARABIC" in name:
                scripts["Arabic"] += 1
            elif "CJK" in name:
                scripts["CJK"] += 1
            elif "CYRILLIC" in name:
                scripts["Cyrillic"] += 1
            elif "DEVANAGARI" in name:
                scripts["Devanagari"] += 1
            elif "THAI" in name:
                scripts["Thai"] += 1
            elif "HANGUL" in name:
                scripts["Hangul"] += 1
            elif "HEBREW" in name:
                scripts["Hebrew"] += 1
            elif "GREEK" in name:
                scripts["Greek"] += 1
            elif "DIGIT" in name or "NUMBER" in name:
                scripts["Numeric"] += 1
            else:
                scripts["Other"] += 1
        except ValueError:
            scripts["Other"] += 1
    return scripts


def detect_encoding(texts, max_samples=50):
    """Detect encoding from raw bytes of sampled texts."""
    # Concatenate a sample of texts and check encoding
    sample_text = "\n".join(texts[:max_samples])
    raw_bytes = sample_text.encode("utf-8", errors="replace")
    result = from_bytes(raw_bytes)
    best = result.best()
    if best:
        return {"encoding": best.encoding, "confidence": round(1.0 - best.chaos, 3)}
    return {"encoding": "unknown", "confidence": 0.0}


def main():
    parser = argparse.ArgumentParser(description="Text statistics")
    parser.add_argument("--repo_id", required=True)
    parser.add_argument("--config", default=None)
    parser.add_argument("--split", default="train")
    parser.add_argument("--columns", nargs="+", required=True)
    parser.add_argument("--sample_size", type=int, default=200)
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
        json.dump({"script": "text_stats", "error": str(e)}, sys.stdout, indent=2)
        return

    samples = list(tqdm(ds.take(args.sample_size), total=args.sample_size, desc="Streaming"))

    per_column = {}
    for col in args.columns:
        texts = [str(s.get(col, "") or "") for s in samples]
        lengths_chars = [len(t) for t in texts]
        lengths_words = [len(t.split()) for t in texts]
        n_null = sum(1 for t in texts if not t.strip())

        # Length percentiles
        if lengths_chars:
            arr = np.array(lengths_chars)
            length_stats = {
                "p5": int(np.percentile(arr, 5)),
                "p25": int(np.percentile(arr, 25)),
                "p50": int(np.percentile(arr, 50)),
                "p75": int(np.percentile(arr, 75)),
                "p95": int(np.percentile(arr, 95)),
                "mean": round(float(arr.mean()), 1),
            }
            word_arr = np.array(lengths_words)
            word_stats = {
                "p50": int(np.percentile(word_arr, 50)),
                "p95": int(np.percentile(word_arr, 95)),
            }
        else:
            length_stats = {}
            word_stats = {}

        # Script histogram (aggregate across all texts)
        total_scripts = Counter()
        for t in texts:
            total_scripts.update(unicode_script_histogram(t))
        total_chars = sum(total_scripts.values())
        script_pct = {
            s: round(100.0 * c / total_chars, 2) if total_chars > 0 else 0
            for s, c in total_scripts.most_common()
        }

        # Encoding detection
        encoding = detect_encoding(texts)

        # Anomaly detection
        anomalies = []
        if n_null > 0:
            anomalies.append(f"{n_null} empty/null values ({round(100*n_null/len(texts),1)}%)")
        unexpected = {s for s in script_pct if s not in {"Latin", "Numeric", "Other"} and script_pct[s] > 1.0}
        if unexpected:
            anomalies.append(
                f"Non-Latin scripts: {', '.join(f'{s} ({script_pct[s]}%)' for s in unexpected)}"
            )

        per_column[col] = {
            "n_samples": len(texts),
            "null_rate": round(n_null / len(texts), 4) if texts else 0,
            "length_chars": length_stats,
            "length_words": word_stats,
            "encoding": encoding,
            "script_histogram_pct": script_pct,
            "anomalies": anomalies,
        }

    result = {
        "script": "text_stats",
        "repo_id": args.repo_id,
        "config": args.config,
        "split": args.split,
        "sample_size": args.sample_size,
        "columns": per_column,
    }
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
