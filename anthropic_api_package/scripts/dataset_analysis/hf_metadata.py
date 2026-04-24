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


def auth_header(token=None):
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def get_hub_info(repo_id, token=None):
    """Hub /api/datasets/{repo_id}?full=true — always works, even for gated."""
    url = f"https://huggingface.co/api/datasets/{repo_id}"
    resp = requests.get(url, params={"full": "true"}, headers=auth_header(token), timeout=30)
    if resp.status_code == 404:
        return {"error": "DATASET_NOT_FOUND", "status_code": 404}
    resp.raise_for_status()
    return resp.json()


def get_is_valid(repo_id, token=None):
    """Dataset-server /is-valid — cheap gate check."""
    url = "https://datasets-server.huggingface.co/is-valid"
    try:
        resp = requests.get(url, params={"dataset": repo_id}, headers=auth_header(token), timeout=15)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def get_splits(repo_id, token=None):
    """Dataset-server /splits — enumerate configs and splits."""
    url = "https://datasets-server.huggingface.co/splits"
    try:
        resp = requests.get(url, params={"dataset": repo_id}, headers=auth_header(token), timeout=15)
        if resp.status_code != 200:
            return {"error": f"HTTP {resp.status_code}", "body": resp.text[:200]}
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


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
            if dtype == "string":
                modalities.add("text")
    if not modalities:
        modalities.add("unknown")
    if len(modalities) > 1 and "text" in modalities:
        return sorted(modalities)
    return sorted(modalities)


def summarize_features(features):
    """Compact feature summary for LLM consumption."""
    summary = {}
    for col_name, col_info in features.items():
        if isinstance(col_info, list):
            if col_info and isinstance(col_info[0], dict):
                inner_type = col_info[0].get("_type", "Value")
                inner_dtype = col_info[0].get("dtype", "")
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
            inner = col_info.get("feature", {})
            if isinstance(inner, list):
                summary[col_name] = "Sequence[list]"
            else:
                inner_type = inner.get("_type", "Value")
                inner_dtype = inner.get("dtype", "")
                summary[col_name] = f"Sequence[{inner_dtype or inner_type}]"
        elif _type == "ClassLabel":
            names = col_info.get("names", [])
            summary[col_name] = f"ClassLabel({len(names)} classes)"
        elif _type in ("Image", "Audio"):
            summary[col_name] = _type
        else:
            summary[col_name] = dtype or _type
    return summary


def main():
    parser = argparse.ArgumentParser(description="HF zero-download metadata extraction")
    parser.add_argument("--repo_id", required=True, help="HuggingFace dataset ID")
    parser.add_argument("--config", default=None, help="Dataset config/subset name")
    parser.add_argument("--token", default=None, help="HF token (or set HF_TOKEN env var)")
    args = parser.parse_args()

    token = args.token or os.environ.get("HF_TOKEN")
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
    hub = get_hub_info(args.repo_id, token)
    if "error" in hub:
        result["errors"].append(f"Hub API: {hub['error']}")
        result["access"]["accessible"] = False
        json.dump(result, sys.stdout, indent=2)
        return

    result["access"] = {
        "accessible": True,
        "private": hub.get("private", False),
        "gated": hub.get("gated", False),
        "downloads": hub.get("downloads", 0),
        "likes": hub.get("likes", 0),
    }

    card = hub.get("cardData", {}) or {}
    result["card"] = {
        "languages": card.get("language", []),
        "task_categories": card.get("task_categories", []),
        "license": card.get("license", "not specified"),
        "size_categories": card.get("size_categories", []),
        "tags": hub.get("tags", []),
    }

    # === Step 2: is-valid gate check ===
    valid = get_is_valid(args.repo_id, token)
    if "error" in valid:
        result["warnings"].append(f"is-valid check failed: {valid['error']}")
        viewer_ok = False
    else:
        viewer_ok = valid.get("viewer", False)
        result["access"]["viewer_supported"] = viewer_ok

    # === Step 3: splits ===
    splits_resp = get_splits(args.repo_id, token)
    if "error" not in splits_resp:
        splits_list = splits_resp.get("splits", [])
        configs = sorted(set(s.get("config", "") for s in splits_list))
        result["splits_info"]["configs"] = configs
        result["splits_info"]["splits_by_config"] = {}
        for cfg in configs:
            cfg_splits = [s["split"] for s in splits_list if s.get("config") == cfg]
            result["splits_info"]["splits_by_config"][cfg] = cfg_splits
    else:
        result["warnings"].append(f"splits API failed: {splits_resp['error']}")

    # === Step 4: /info for requested config ===
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
                "features": summarize_features(features),
                "features_raw": features,
            }
            result["modality"] = detect_modality(features)

            # Extract split sizes
            splits = ds_info.get("splits", {})
            result["schema"]["splits"] = {
                name: {
                    "num_examples": s.get("num_examples", 0),
                    "num_bytes": s.get("num_bytes", 0)
                }
                for name, s in splits.items()
            }

            # Extract label names if ClassLabel present
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
    size_resp = get_size(args.repo_id, token)
    if "error" not in size_resp:
        size_data = size_resp.get("size", {})
        dataset_size = size_data.get("dataset", {})
        result["size"] = {
            "total_rows": dataset_size.get("num_rows", 0),
            "total_bytes_parquet": dataset_size.get("num_bytes_parquet_files", 0),
            "total_bytes_memory": dataset_size.get("num_bytes_memory", 0),
        }
    else:
        result["warnings"].append(f"/size failed: {size_resp.get('error', 'unknown')}")

    # === Remove raw features to keep output compact ===
    if "features_raw" in result.get("schema", {}):
        del result["schema"]["features_raw"]

    json.dump(result, sys.stdout, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
