"""Prepare the website's complete pinned benchmark cache without model API calls.

Run ``python -m bayesian_auditing.prepare_benchmark_index --help``. Repeating the
same command resumes committed indexing work or verifies the completed cache.
The cache stores search structures and source locations. Complete candidate
rows are fetched from the pinned Hugging Face files during verification/search.
The website uses the same identity and filesystem lock.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import signal
import time

from huggingface_hub import get_token

from .benchmark_data import iter_benchmark_items, row_fingerprint
from .benchmark_encoding import FullRowBGEEncoder
from .benchmark_index import DEFAULT_MINIMUM_FREE_BYTES, prepare_benchmark_index
from .benchmark_rows import fetch_benchmark_rows


ROOT = Path(__file__).resolve().parents[1]
SMOKE_QUERY = "Clinical diagnosis, investigation and management of an adult patient with chest pain"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=ROOT / "website/server/item_review_inventory.json")
    parser.add_argument("--cache-dir", type=Path, required=True,
                        help="Use WEBSITE_DATA_DIR/benchmark-retrieval-index for the website")
    parser.add_argument("--device", default=None, help="Torch device; defaults to CUDA when available")
    parser.add_argument("--batch-size", type=int, default=64, help="BGE chunks per inference batch")
    parser.add_argument("--cpu-threads", type=int, default=4)
    parser.add_argument("--minimum-free-gb", type=float, default=DEFAULT_MINIMUM_FREE_BYTES / 1e9,
                        help="Stop safely below this free-disk reserve; committed progress is retained")
    parser.add_argument("--progress-seconds", type=float, default=30)
    args = parser.parse_args(argv)
    if args.batch_size < 1 or args.cpu_threads < 1 or args.minimum_free_gb < 0 or args.progress_seconds <= 0:
        parser.error("Batch/CPU sizes and progress interval must be positive; disk reserve cannot be negative")

    import torch

    torch.set_num_threads(args.cpu_threads)
    os.umask(0o077)
    args.cache_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    inventory = json.loads(args.inventory.read_text())
    token = get_token()
    encoder = FullRowBGEEncoder(device=args.device, batch_size=args.batch_size)
    started = time.monotonic()
    last_report = 0.0
    stage_started, stage_initial, previous_stage = started, 0, None
    stopped = False
    status = {"status": "starting", "pid": os.getpid(), "inventory": str(args.inventory.resolve()),
              "branches": inventory["branches"], "tables": len(inventory["tables"]),
              "source_rows": sum(table["row_count"] for table in inventory["tables"]),
              "batch_size": args.batch_size, "minimum_free_gb": args.minimum_free_gb}
    status_path = args.cache_dir / "preparation-status.json"

    def save_status(**changes):
        status.update(changes, updated_at=datetime.now(timezone.utc).isoformat(),
                      elapsed_seconds=round(time.monotonic() - started, 1))
        temporary = status_path.with_suffix(f".{os.getpid()}.tmp")
        temporary.write_text(json.dumps(status, indent=2) + "\n")
        temporary.replace(status_path)

    def handle_signal(signum, frame):
        nonlocal stopped
        stopped = True

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    def progress(state):
        nonlocal last_report, stage_started, stage_initial, previous_stage
        now = time.monotonic()
        new_stage = state["stage"] != previous_stage
        if new_stage:
            stage_started, stage_initial, previous_stage = now, state["completed"], state["stage"]
        free_bytes = shutil.disk_usage(args.cache_dir).free
        if new_stage or now - last_report >= args.progress_seconds or state["completed"] == state["total"]:
            rate = (state["completed"] - stage_initial) / max(now - stage_started, 0.001)
            remaining = (state["total"] - state["completed"]) / rate if rate > 0 else None
            save_status(status="building", progress=state, free_gb=round(free_bytes / 1e9, 2),
                        rows_per_second=round(rate, 2),
                        estimated_stage_remaining_seconds=round(remaining) if remaining is not None else None)
            print(json.dumps(status), flush=True)
            last_report = now

    def rows(offset):
        return iter_benchmark_items(inventory, token=token, streaming=True, skip_rows=offset)

    def load_rows(requests, *, cancelled=None):
        return fetch_benchmark_rows(inventory, requests, token=token, cancelled=cancelled)

    index = None
    save_status()
    try:
        index = prepare_benchmark_index(rows, args.cache_dir, inventory, encoder,
                                        cancelled=lambda: stopped, progress=progress, resume=True,
                                        minimum_free_bytes=int(args.minimum_free_gb * 1e9),
                                        row_loader=load_rows)
        save_status(status="verifying", cache_path=str(index.path.resolve()), stats=index.stats)
        candidates = index.search(SMOKE_QUERY, cancelled=lambda: stopped)
        assert candidates, "The completed full index returned no smoke-query candidates"
        assert len({row["item_id"] for row in candidates}) == len(candidates)
        assert all(row_fingerprint(row["evidence"]["item"]) == row["item_id"] for row in candidates)
        query_summary = {
            "query": SMOKE_QUERY, "candidates": len(candidates),
            "dense_candidates": sum(row["dense_rank"] is not None for row in candidates),
            "bm25_candidates": sum(row["bm25_rank"] is not None for row in candidates),
            "source_collections": sorted({source["benchmark"] for row in candidates for source in row["sources"]}),
            "top_item_ids": [row["item_id"] for row in candidates[:10]],
        }
        index.close()
        index = None

        def must_not_load(offset):
            raise AssertionError("A completed cache unexpectedly consumed the item bank")

        index = prepare_benchmark_index(must_not_load, args.cache_dir, inventory, encoder,
                                        resume=True, row_loader=load_rows)
        assert index.stats["cache_hit"], "Completed cache was not reused"
        save_status(status="completed", stats=index.stats, smoke_search=query_summary,
                    cache_bytes=index.path.stat().st_size, cache_reuse_verified=True)
        print(json.dumps(status), flush=True)
    except Exception as exc:
        save_status(status="interrupted" if stopped else "failed", error=f"{type(exc).__name__}: {exc}")
        print(json.dumps(status), flush=True)
        raise
    finally:
        if index is not None:
            index.close()


if __name__ == "__main__":
    main()
