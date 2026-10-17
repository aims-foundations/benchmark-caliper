"""Prepare the demo sample and optionally cache local Qwen question vectors.

Run: python -m website.server.item_review_sample
Uses the pinned inventory and the server's configured Hugging Face access.
"""

import argparse
import json

from huggingface_hub import get_token

from bayesian_auditing.sampling import iter_sample_items, prepare_samples
from . import db
from .item_review_catalog import INVENTORY_PATH


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-index", action="store_true", help="Precompute local Qwen question embeddings; no paid API calls")
    args = parser.parse_args()
    inventory = json.loads(INVENTORY_PATH.read_text())
    completed = -1

    def progress(benchmark, count, rows):
        global completed
        if count != completed:
            print(f"{count} collections prepared; {rows:,} source rows considered; {benchmark}", flush=True)
            completed = count

    paths, count = prepare_samples(inventory, db.DEFAULT_DB_PATH.parent / "item-review-samples",
                                   token=get_token(), progress=progress)
    print(f"Ready: {count:,} distinct items across {len(paths)} benchmark collections.")
    if args.build_index:
        from bayesian_auditing.retrieval import ItemIndex

        index = ItemIndex(iter_sample_items(paths), cache_dir=db.DEFAULT_DB_PATH.parent / "item-review-embeddings")
        print(f"Cached question vectors for {index.indexed_items:,} distinct evidence records; "
              f"{index.contentless_items:,} records have no question text.")
