"""Catalog refresh validates every discovered table, without paid model calls."""

from contextlib import contextmanager
from types import SimpleNamespace

import pytest

from website.server import item_review_catalog as catalog


@pytest.mark.parametrize("valid", [True, False])
def test_refresh_reads_both_branches_and_rejects_incompatible_tables(monkeypatch, valid):
    inventory = {"repo": "fixture", "branches": {"main": "a", "migration": "b"},
                 "tables": [{"branch": "main", "items_path": "math/items.parquet"},
                            {"branch": "migration", "items_path": "coding/formatted_tables/items.parquet"}]}
    seen = []
    monkeypatch.setattr(catalog, "discover_inventory", lambda: inventory)
    monkeypatch.setattr(catalog, "get_token", lambda: "server-secret")

    @contextmanager
    def open_table(data, table, *, token, streaming):
        assert data is inventory and token == "server-secret" and streaming
        seen.append(table["branch"])
        yield SimpleNamespace(metadata=SimpleNamespace(num_rows=42),
                              schema_arrow=SimpleNamespace(names=["item_id", "content"] if valid else ["item_id"]))

    monkeypatch.setattr(catalog, "open_item_table", open_table)
    if not valid:
        with pytest.raises(ValueError, match="Missing item_id/content"):
            catalog.refresh_inventory()
    else:
        result = catalog.refresh_inventory()
        assert set(seen) == {"main", "migration"}
        assert sum(table["row_count"] for table in result["tables"]) == 84
        assert result["branches"] == inventory["branches"]
