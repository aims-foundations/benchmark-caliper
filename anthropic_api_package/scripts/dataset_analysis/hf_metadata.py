#!/usr/bin/env python3
"""Zero-download HF metadata extraction for LLM planning context.

Queries HuggingFace APIs to extract dataset schema, access status, languages,
modality, and split sizes without downloading any data.

Usage:
    python hf_metadata.py --repo_id sentence-transformers/parallel-sentences-ccmatrix --config en-lb
"""

import argparse
import json
import os
import sys

import requests


# Build an Authorization header dict when a token is provided.
# Returns an empty dict when no token is given so callers can always pass it
# directly to requests — avoids sprinkling None-checks everywhere.
def auth_header(token=None):
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


# Fetch top-level dataset metadata from the Hub REST API.
# Returns the full JSON payload (visibility, gating status, card data, tags, etc.).
# The ?full=true param also surfaces cardData, which is absent by default.
# Critically, this endpoint works even for gated datasets before the user has
# accepted the access conditions — useful as a cheap existence/visibility check.
def get_hub_info(repo_id, token=None):
    """Hub /api/datasets/{repo_id}?full=true — always works, even for gated."""
    url = f"https://huggingface.co/api/datasets/{repo_id}"
    resp = requests.get(url, params={"full": "true"}, headers=auth_header(token), timeout=30)
    if resp.status_code == 404:
        return {"error": "DATASET_NOT_FOUND", "status_code": 404}
    resp.raise_for_status()
    return resp.json()


# Ask the dataset-server whether this dataset is ready for programmatic access
# (i.e., Parquet conversion completed and viewer is functional).
# A False/missing `viewer` flag means /splits and /info may still succeed but the
# dataset-server doesn't guarantee completeness — captured as a warning downstream.
def get_is_valid(repo_id, token=None):
    """Dataset-server /is-valid — cheap gate check."""
    url = "https://datasets-server.huggingface.co/is-valid"
    try:
        resp = requests.get(url, params={"dataset": repo_id}, headers=auth_header(token), timeout=15)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


# Retrieve the list of all (config, split) pairs exposed by the dataset-server.
# Many multi-lingual or multi-task datasets have multiple configs (subsets);
# this is the canonical way to enumerate them without loading any data.
def get_splits(repo_id, token=None):
    """Dataset-server /splits — enumerate configs and splits."""
    url = "https://datasets-server.huggingface.co/splits"
    try:
        resp = requests.get(url, params={"dataset": repo_id}, headers=auth_header(token), timeout=15)
        if resp.status_code != 200:
            # Include a short body snippet to surface error messages (e.g., "gated dataset")
            return {"error": f"HTTP {resp.status_code}", "body": resp.text[:200]}
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


# Fetch the full schema for one config: column types, split row/byte counts, label names.
# A config must be specified because multi-config datasets may have different schemas
# per subset — the server rejects requests without an explicit config name.
def get_info(repo_id, config, token=None):
    """Dataset-server /info — full schema with types, split sizes, label names."""
    url = "https://datasets-server.huggingface.co/info"
    try:
        resp = requests.get(
            url, params={"dataset": repo_id, "config": config},
            headers=auth_header(token), timeout=15
        )
        if resp.status_code != 200:
            return {"error": f"HTTP {resp.status_code}", "body": resp.text[:200]}
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


# Get aggregate row counts and byte sizes for the entire dataset (all configs combined).
# Useful for estimating compute / API cost before committing to analysis.
def get_size(repo_id, token=None):
    """Dataset-server /size — row counts and byte sizes."""
    url = "https://datasets-server.huggingface.co/size"
    try:
        resp = requests.get(url, params={"dataset": repo_id}, headers=auth_header(token), timeout=15)
        if resp.status_code != 200:
            return {"error": f"HTTP {resp.status_code}"}
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


# Infer the dominant modality (text / image / audio) from the HF feature _type fields.
# Returns a sorted list so multi-modal datasets (e.g., image + text) surface both.
# Falls back to ["unknown"] when no recognizable typed columns are present — this
# guards against purely numeric/tabular datasets where dtype != "string".
def detect_modality(features):
    """Infer modality from feature _type fields."""
    modalities = set()
    for col_name, col_info in features.items():
        if not isinstance(col_info, dict):
            continue
        _type = col_info.get("_type", "")
        if _type == "Image":
            modalities.add("image")
        elif _type == "Audio":
            modalities.add("audio")
        elif _type in ("Value", "ClassLabel"):
            dtype = col_info.get("dtype", "")
            # Only count string-typed Value columns as text; int/float columns are
            # metadata / labels and shouldn't drive the modality classification
            if dtype == "string":
                modalities.add("text")
    if not modalities:
        modalities.add("unknown")
    # Return sorted so output is deterministic regardless of dict iteration order
    if len(modalities) > 1 and "text" in modalities:
        return sorted(modalities)
    return sorted(modalities)


# Flatten the raw HF features dict into a concise string-valued mapping suitable for
# including in an LLM prompt (token-efficient, no deeply nested JSON).
# Handles the three structural variants the dataset-server may return:
#   1. A bare Python list  — sequence without explicit HF Sequence wrapper
#   2. A dict with _type=="Sequence" — HF-typed sequence with inner feature spec
#   3. A plain dict — scalar Value, ClassLabel, Image, Audio
def summarize_features(features):
    """Compact feature summary for LLM consumption."""
    summary = {}
    for col_name, col_info in features.items():
        # --- Variant 1: bare list (uncommon but valid in older datasets) ---
        if isinstance(col_info, list):
            if col_info and isinstance(col_info[0], dict):
                inner_type = col_info[0].get("_type", "Value")
                inner_dtype = col_info[0].get("dtype", "")
                # Prefer dtype string (e.g., "int32") over abstract type name when available
                summary[col_name] = f"Sequence[{inner_dtype or inner_type}]"
            else:
                summary[col_name] = "Sequence[unknown]"
            continue
        if not isinstance(col_info, dict):
            summary[col_name] = str(col_info)
            continue

        _type = col_info.get("_type", "Value")
        dtype = col_info.get("dtype", "")

        if _type == "Sequence":
            # --- Variant 2: HF Sequence wrapper ---
            inner = col_info.get("feature", {})
            if isinstance(inner, list):
                # Nested list-of-features — just flag it without drilling further
                summary[col_name] = "Sequence[list]"
            else:
                inner_type = inner.get("_type", "Value")
                inner_dtype = inner.get("dtype", "")
                summary[col_name] = f"Sequence[{inner_dtype or inner_type}]"
        elif _type == "ClassLabel":
            # Report class count rather than full names list — keeps the summary compact
            names = col_info.get("names", [])
            summary[col_name] = f"ClassLabel({len(names)} classes)"
        elif _type in ("Image", "Audio"):
            # These types carry no useful dtype; the type name alone is informative
            summary[col_name] = _type
        else:
            # --- Variant 3: scalar Value — prefer dtype (e.g., "float32") over "_type" ---
            summary[col_name] = dtype or _type
    return summary


# Orchestrates all API calls, assembles results into a single structured JSON blob,
# and writes it to stdout. The output is consumed by the pipeline's step 5b-da
# prompt to give the LLM grounding about the dataset before generating analysis code.
def main():
    parser = argparse.ArgumentParser(description="HF zero-download metadata extraction")
    parser.add_argument("--repo_id", required=True, help="HuggingFace dataset ID")
    parser.add_argument("--config", default=None, help="Dataset config/subset name")
    parser.add_argument("--token", default=None, help="HF token (or set HF_TOKEN env var)")
    args = parser.parse_args()

    # Token lookup: CLI flag takes priority, env var is the fallback for CI / scripted calls
    token = args.token or os.environ.get("HF_TOKEN")

    # Skeleton result dict — all fields pre-populated so downstream consumers can
    # always expect the same keys regardless of which API calls succeed or fail
    result = {
        "script": "hf_metadata",
        "repo_id": args.repo_id,
        "config_requested": args.config,
        "access": {},
        "card": {},
        "schema": {},
        "splits_info": {},
        "size": {},
        "modality": [],
        "warnings": [],
        "errors": []
    }

    # === Step 1: Hub info ===
    # This is the only call that can definitively tell us the dataset doesn't exist.
    # If it fails, there's nothing more to fetch — bail early with accessible=False.
    hub = get_hub_info(args.repo_id, token)
    if "error" in hub:
        result["errors"].append(f"Hub API: {hub['error']}")
        result["access"]["accessible"] = False
        json.dump(result, sys.stdout, indent=2)
        return

    result["access"] = {
        "accessible": True,
        "private": hub.get("private", False),
        # gated=True means users must agree to T&C before accessing data;
        # a token with accepted access is required for /splits and /info to work
        "gated": hub.get("gated", False),
        "downloads": hub.get("downloads", 0),
        "likes": hub.get("likes", 0),
    }

    # cardData may be None (dataset has no model card) — guard with `or {}`
    card = hub.get("cardData", {}) or {}
    result["card"] = {
        "languages": card.get("language", []),
        "task_categories": card.get("task_categories", []),
        "license": card.get("license", "not specified"),
        "size_categories": card.get("size_categories", []),
        # tags come from the hub payload, not cardData — they include auto-generated tags
        "tags": hub.get("tags", []),
    }

    # === Step 2: is-valid gate check ===
    # viewer=True means the dataset-server has converted the dataset to Parquet and
    # its viewer is live; subsequent /splits and /info calls are likely to succeed.
    # viewer=False is a soft signal — we still try the other endpoints (some datasets
    # serve partial results even when the viewer flag is off).
    valid = get_is_valid(args.repo_id, token)
    if "error" in valid:
        result["warnings"].append(f"is-valid check failed: {valid['error']}")
        viewer_ok = False
    else:
        viewer_ok = valid.get("viewer", False)
        result["access"]["viewer_supported"] = viewer_ok

    # === Step 3: splits ===
    # Enumerate all (config, split) pairs so we know what configs exist even before
    # requesting schema details. Needed to auto-select a config in Step 4 when the
    # caller doesn't pass --config explicitly.
    splits_resp = get_splits(args.repo_id, token)
    if "error" not in splits_resp:
        splits_list = splits_resp.get("splits", [])
        # De-duplicate and sort so the config list is deterministic
        configs = sorted(set(s.get("config", "") for s in splits_list))
        result["splits_info"]["configs"] = configs
        result["splits_info"]["splits_by_config"] = {}
        for cfg in configs:
            cfg_splits = [s["split"] for s in splits_list if s.get("config") == cfg]
            result["splits_info"]["splits_by_config"][cfg] = cfg_splits
    else:
        result["warnings"].append(f"splits API failed: {splits_resp['error']}")

    # === Step 4: /info for requested config ===
    # If the user didn't specify a config, fall back to the first one from /splits.
    # This heuristic works for most datasets; multi-config datasets may need an
    # explicit --config to get the right schema.
    config = args.config
    if not config and result["splits_info"].get("configs"):
        config = result["splits_info"]["configs"][0]

    if config:
        info = get_info(args.repo_id, config, token)
        if "error" not in info:
            ds_info = info.get("dataset_info", {})
            features = ds_info.get("features", {})
            result["schema"] = {
                "config": config,
                # Compact human/LLM-readable column summary
                "features": summarize_features(features),
                # Raw features preserved temporarily for modality detection and label extraction;
                # stripped before output in Step 6 to keep JSON size manageable
                "features_raw": features,
            }
            result["modality"] = detect_modality(features)

            # Extract split sizes from /info rather than /size because /info gives
            # per-config split breakdown, while /size aggregates across all configs
            splits = ds_info.get("splits", {})
            result["schema"]["splits"] = {
                name: {
                    "num_examples": s.get("num_examples", 0),
                    "num_bytes": s.get("num_bytes", 0)
                }
                for name, s in splits.items()
            }

            # Pull label class names for ClassLabel columns — important context for the
            # LLM to understand the output space of classification tasks
            for col_name, col_info in features.items():
                if isinstance(col_info, dict) and col_info.get("_type") == "ClassLabel":
                    result["schema"]["label_names"] = {
                        col_name: col_info.get("names", [])
                    }
        else:
            result["warnings"].append(f"/info failed for config '{config}': {info['error']}")
    else:
        result["warnings"].append("No config specified and none found via /splits")

    # === Step 5: /size ===
    # Aggregate byte/row counts across all configs — gives a dataset-level size signal
    # independent of the per-config schema info fetched above.
    size_resp = get_size(args.repo_id, token)
    if "error" not in size_resp:
        size_data = size_resp.get("size", {})
        dataset_size = size_data.get("dataset", {})
        result["size"] = {
            "total_rows": dataset_size.get("num_rows", 0),
            # Parquet footprint is typically much smaller than in-memory due to compression
            "total_bytes_parquet": dataset_size.get("num_bytes_parquet_files", 0),
            "total_bytes_memory": dataset_size.get("num_bytes_memory", 0),
        }
    else:
        result["warnings"].append(f"/size failed: {size_resp.get('error', 'unknown')}")

    # === Step 6: Strip raw features before output ===
    # features_raw was only needed internally for detect_modality / label extraction;
    # dropping it keeps the JSON output token-efficient for downstream LLM consumption
    if "features_raw" in result.get("schema", {}):
        del result["schema"]["features_raw"]

    json.dump(result, sys.stdout, indent=2)
    print()  # trailing newline for clean shell output


if __name__ == "__main__":
    main()
