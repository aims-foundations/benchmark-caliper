"""Refresh the hosted inventory without downloading item bodies.

Run from the repository root: python -m website.server.item_review_catalog
Only paths, pinned revisions, and row counts are saved; credentials stay in HF.
"""

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

from huggingface_hub import get_token

from bayesian_auditing.data import discover_inventory, open_item_table

INVENTORY_PATH = Path(__file__).with_name("item_review_inventory.json")


def refresh_inventory() -> dict:
    data = discover_inventory()
    token = get_token()

    def inspect(table):
        with open_item_table(data, table, token=token, streaming=True) as parquet:
            if not {"item_id", "content"}.issubset(parquet.schema_arrow.names):
                raise ValueError(f"Missing item_id/content columns: {table['items_path']}")
            return {**table, "row_count": parquet.metadata.num_rows}

    with ThreadPoolExecutor(max_workers=4) as workers:
        data["tables"] = list(workers.map(inspect, data["tables"]))
    return data


if __name__ == "__main__":
    inventory = refresh_inventory()
    INVENTORY_PATH.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(inventory['tables'])} tables and "
          f"{sum(t['row_count'] for t in inventory['tables']):,} source rows.")
