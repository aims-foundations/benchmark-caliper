"""Catalog refresh validates every discovered table, without paid model calls."""

from contextlib import contextmanager
from types import SimpleNamespace

import pytest

from website.server import item_review_catalog as catalog


@pytest.mark.parametrize("valid", [True, False])
def test_refresh_reads_only_main_and_rejects_incompatible_tables(monkeypatch, valid):
    inventory = {"repo": "fixture", "branches": {"main": "a"},
                 "tables": [{"branch": "main", "items_path": "math/items.parquet"},
                            {"branch": "main", "items_path": "coding/formatted_tables/items.parquet"}]}
    seen = []
    def discover(*, branches):
        assert branches == ("main",)
        return inventory
    monkeypatch.setattr(catalog, "discover_inventory", discover)
    monkeypatch.setattr(catalog, "get_token", lambda: "server-secret")

    @contextmanager
    def open_table(data, table, *, token, streaming):
        assert data is inventory and token == "server-secret" and streaming
        seen.append(table["items_path"])
        yield SimpleNamespace(metadata=SimpleNamespace(num_rows=42),
                              schema_arrow=SimpleNamespace(names=["custom_field"] if valid else ["item_id", "item_id"]))

    monkeypatch.setattr(catalog, "open_item_table", open_table)
    if not valid:
        with pytest.raises(ValueError, match="column names must be unique"):
            catalog.refresh_inventory()
    else:
        result = catalog.refresh_inventory()
        assert set(seen) == {"math/items.parquet", "coding/formatted_tables/items.parquet"}
        assert sum(table["row_count"] for table in result["tables"]) == 84
        assert result["branches"] == inventory["branches"]
