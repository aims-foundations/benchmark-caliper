"""Prepare the demo sample without an OpenAI key or any model calls.

Run: python -m website.server.item_review_sample
Uses the pinned inventory and the server's configured Hugging Face access.
"""

import json

from huggingface_hub import get_token

from bayesian_auditing.sampling import prepare_samples
from . import db
from .item_review_catalog import INVENTORY_PATH


if __name__ == "__main__":
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
