#!/usr/bin/env python3
"""Language identification on text columns using fasttext lid.176.ftz.

Streams N samples from a HuggingFace dataset and runs per-text LID,
producing a language distribution histogram with confidence buckets.

Usage:
    python lang_profile.py \
        --repo_id sentence-transformers/parallel-sentences-ccmatrix \
        --config en-lb --split train --columns lb --sample_size 200
"""

import argparse
import json
import os
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import fasttext
from datasets import load_dataset
from tqdm import tqdm


# === Resolve bundled model path ===
MODEL_DIR = Path(__file__).parent / "models"
DEFAULT_MODEL = MODEL_DIR / "lid.176.ftz"


def load_lid_model(model_path=None):
    path = model_path or str(DEFAULT_MODEL)
    if not os.path.exists(path):
        print(f"ERROR: LID model not found at {path}", file=sys.stderr)
        print("Download lid.176.ftz from https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz", file=sys.stderr)
        sys.exit(1)
    # Suppress fasttext warnings about deprecated load_model
    return fasttext.load_model(path)


def detect_language(model, text):
    """Run fasttext LID on a single text. Returns (lang_code, confidence)."""
    if not text or not text.strip():
        return ("empty", 0.0)
    # fasttext expects single-line input
    clean = text.replace("\n", " ").strip()
    predictions = model.predict(clean, k=1)
    label = predictions[0][0].replace("__label__", "")
    confidence = float(predictions[1][0])
    return (label, confidence)


def unicode_script_histogram(text):
    """Count characters by Unicode script/block."""
    scripts = Counter()
    for ch in text:
        if ch.isspace() or ch in '.,;:!?-"\'()[]{}':
            continue
        try:
            name = unicodedata.name(ch, "UNKNOWN")
            # Extract script from Unicode name (first word is usually the script)
            if "LATIN" in name:
                scripts["Latin"] += 1
            elif "ARABIC" in name:
                scripts["Arabic"] += 1
            elif "CJK" in name or "CHINESE" in name:
                scripts["CJK"] += 1
            elif "CYRILLIC" in name:
                scripts["Cyrillic"] += 1
            elif "DEVANAGARI" in name:
                scripts["Devanagari"] += 1
            elif "THAI" in name:
                scripts["Thai"] += 1
            elif "HANGUL" in name:
                scripts["Hangul"] += 1
            elif "HIRAGANA" in name or "KATAKANA" in name:
                scripts["Japanese"] += 1
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
    return dict(scripts)


def main():
    parser = argparse.ArgumentParser(description="Language profile via fasttext LID")
    parser.add_argument("--repo_id", required=True)
    parser.add_argument("--config", default=None)
    parser.add_argument("--split", default="train")
    parser.add_argument("--columns", nargs="+", required=True, help="Text columns to profile")
    parser.add_argument("--sample_size", type=int, default=200)
    parser.add_argument("--model_path", default=None, help="Path to lid.176.ftz")
    parser.add_argument("--token", default=None)
    args = parser.parse_args()

    token = args.token or os.environ.get("HF_TOKEN")

    # === Load model ===
    model = load_lid_model(args.model_path)

    # === Stream dataset ===
    load_kwargs = {"path": args.repo_id, "split": args.split, "streaming": True}
    if args.config:
        load_kwargs["name"] = args.config
    if token:
        load_kwargs["token"] = token

    try:
        ds = load_dataset(**load_kwargs)
    except Exception as e:
        result = {
            "script": "lang_profile",
            "error": str(e),
            "status": "DATASET_LOAD_FAILED"
        }
        json.dump(result, sys.stdout, indent=2)
        return

    # === Profile each column ===
    per_column = {}
    samples = list(tqdm(ds.take(args.sample_size), total=args.sample_size, desc="Streaming samples"))

    for col in args.columns:
        lang_counts = Counter()
        confidence_sum = Counter()
        confidence_buckets = {"high_gt90": 0, "medium_50_90": 0, "low_lt50": 0}
        script_counts = Counter()
        n_empty = 0
        n_processed = 0

        for sample in tqdm(samples, desc=f"LID on '{col}'"):
            text = sample.get(col, "")
            if text is None:
                text = ""
            text = str(text)

            if not text.strip():
                n_empty += 1
                continue

            lang, conf = detect_language(model, text)
            lang_counts[lang] += 1
            confidence_sum[lang] += conf
            n_processed += 1

            if conf >= 0.9:
                confidence_buckets["high_gt90"] += 1
            elif conf >= 0.5:
                confidence_buckets["medium_50_90"] += 1
            else:
                confidence_buckets["low_lt50"] += 1

            # Aggregate script histogram
            for script, count in unicode_script_histogram(text).items():
                script_counts[script] += count

        # Build per-language summary
        lang_distribution = {}
        for lang, count in lang_counts.most_common():
            avg_conf = confidence_sum[lang] / count if count > 0 else 0
            lang_distribution[lang] = {
                "count": count,
                "pct": round(100.0 * count / n_processed, 1) if n_processed > 0 else 0,
                "avg_confidence": round(avg_conf, 3)
            }

        # Normalize script histogram to percentages
        total_chars = sum(script_counts.values())
        script_pct = {
            script: round(100.0 * count / total_chars, 2) if total_chars > 0 else 0
            for script, count in script_counts.most_common()
        }

        per_column[col] = {
            "n_processed": n_processed,
            "n_empty": n_empty,
            "language_distribution": lang_distribution,
            "confidence_buckets": confidence_buckets,
            "script_histogram_pct": script_pct,
        }

        # === Detect anomalies ===
        anomalies = []

        # Check if the column name suggests a language and the data doesn't match
        col_lang = col.lower()
        if col_lang in lang_distribution:
            pct = lang_distribution[col_lang]["pct"]
            if pct < 70:
                anomalies.append(
                    f"Column '{col}' suggests language '{col_lang}' but only {pct}% "
                    f"of samples detected as '{col_lang}'. Top language: "
                    f"{lang_counts.most_common(1)[0][0]} ({lang_distribution[lang_counts.most_common(1)[0][0]]['pct']}%)"
                )
        elif len(col_lang) == 2 or len(col_lang) == 3:
            # Column name looks like a language code but isn't in results
            top_lang = lang_counts.most_common(1)[0][0] if lang_counts else "none"
            anomalies.append(
                f"Column '{col}' may be a language code but '{col_lang}' not detected. "
                f"Top detected language: {top_lang}"
            )

        # Check for unexpected scripts
        expected_scripts = {"Latin", "Numeric"}
        unexpected = {s for s in script_pct if s not in expected_scripts and script_pct[s] > 1.0}
        if unexpected:
            anomalies.append(
                f"Unexpected scripts in '{col}': {', '.join(f'{s} ({script_pct[s]}%)' for s in unexpected)}"
            )

        per_column[col]["anomalies"] = anomalies

    result = {
        "script": "lang_profile",
        "repo_id": args.repo_id,
        "config": args.config,
        "split": args.split,
        "sample_size": args.sample_size,
        "method": "fasttext_lid176ftz",
        "columns": per_column,
    }

    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
