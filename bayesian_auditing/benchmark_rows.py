"""Fetch complete shortlisted rows from their pinned benchmark source tables.

The search index keeps hashes and source locations. This reader restores the
original rows only when they are needed, grouping requests by Parquet table so
each relevant row group is read once. It never persists fetched row contents.
"""

from contextlib import closing
import re

from huggingface_hub import get_token

from .benchmark_data import row_fingerprint, row_text
from .data import _table_rows, open_item_table


_TABLE_FIELDS = ("branch", "commit", "benchmark", "items_path")


def _check_cancelled(cancelled):
    if cancelled is not None and cancelled():
        raise InterruptedError("Benchmark row retrieval was cancelled")


class _CancellableTable:
    """Check cancellation even while skipping unrequested rows in a row group."""

    def __init__(self, parquet, cancelled):
        self.metadata = parquet.metadata
        self._parquet = parquet
        self._cancelled = cancelled

    def iter_batches(self, **kwargs):
        batches = self._parquet.iter_batches(**kwargs)
        try:
            while True:
                _check_cancelled(self._cancelled)
                try:
                    batch = next(batches)
                except StopIteration:
                    return
                _check_cancelled(self._cancelled)
                yield batch
        finally:
            if hasattr(batches, "close"):
                batches.close()


def _requests_by_table(inventory, requests, cancelled):
    """Validate all provenance before opening any source, then choose one per ID."""
    if not isinstance(inventory, dict) or not isinstance(inventory.get("repo"), str) or not inventory["repo"]:
        raise ValueError("A pinned benchmark repository is required")
    if not isinstance(inventory.get("tables"), list):
        raise ValueError("A pinned benchmark table inventory is required")
    if "branches" in inventory and not isinstance(inventory["branches"], dict):
        raise ValueError("Pinned benchmark branches must map to their commits")
    tables = {}
    for table in inventory.get("tables", []):
        if (not isinstance(table, dict)
                or any(not isinstance(table.get(key), str) or not table[key] for key in _TABLE_FIELDS)):
            raise ValueError("Benchmark inventory tables require pinned source locations")
        if "row_count" in table and (type(table["row_count"]) is not int or table["row_count"] < 0):
            raise ValueError("Pinned benchmark table row counts must be nonnegative integers")
        if "branches" in inventory and inventory["branches"].get(table["branch"]) != table["commit"]:
            raise ValueError("Benchmark table commit differs from its pinned branch")
        key = tuple(table[field] for field in _TABLE_FIELDS)
        if key in tables and tables[key].get("row_count") != table.get("row_count"):
            raise ValueError("Benchmark inventory has conflicting table row counts")
        tables[key] = table

    sources_by_id = {}
    for request in requests:
        _check_cancelled(cancelled)
        if not isinstance(request, dict) or not isinstance(request.get("item_id"), str) or not re.fullmatch(r"[0-9a-f]{64}", request["item_id"]):
            raise ValueError("Requested benchmark item IDs must be complete row hashes")
        sources = request.get("sources")
        if not isinstance(sources, list) or not sources:
            raise ValueError("Every requested benchmark item requires source provenance")
        for source in sources:
            _check_cancelled(cancelled)
            if (not isinstance(source, dict) or source.get("repo") != inventory["repo"]
                    or any(not isinstance(source.get(key), str) for key in _TABLE_FIELDS)):
                raise ValueError("Benchmark source differs from the pinned inventory")
            table = tables.get(tuple(source[field] for field in _TABLE_FIELDS))
            if table is None:
                raise ValueError("Benchmark source differs from the pinned inventory")
            if (type(source.get("row")) is not int or source["row"] < 1
                    or ("row_count" in table and source["row"] > table["row_count"])):
                raise ValueError("Benchmark source row is outside its pinned table")
            sources_by_id.setdefault(request["item_id"], []).append(source)

    grouped = {}
    for item_id, sources in sources_by_id.items():
        source = min(sources, key=lambda value: (value["commit"], value["items_path"], value["row"],
                                                 value["branch"], value["benchmark"]))
        table = tables[tuple(source[field] for field in _TABLE_FIELDS)]
        key = inventory["repo"], source["commit"], source["items_path"]
        entry = grouped.setdefault(key, {"table": table, "rows": {}})
        if entry["table"].get("row_count") != table.get("row_count"):
            raise ValueError("Benchmark inventory has conflicting table row counts")
        previous = entry["rows"].setdefault(source["row"], item_id)
        if previous != item_id:
            raise ValueError("One benchmark source row cannot identify different items")
    return sources_by_id, grouped


def fetch_benchmark_rows(inventory: dict, requests: list[dict], *, token: str | None = None,
                         cancelled=None) -> dict[str, dict]:
    """Restore and verify full rows for ``{item_id, sources}`` requests.

    Every source must belong to the supplied pinned inventory. A deterministic
    representative supplies each distinct item; duplicate requests share the
    same read. All original columns are read without parsing JSON string cells
    or coercing unsupported values. Errors and cancellation close the current
    table and return no partial result. No source is silently substituted.
    """
    _check_cancelled(cancelled)
    if not isinstance(requests, list):
        raise ValueError("Benchmark row requests must be a list")
    if not requests:
        return {}
    sources_by_id, grouped = _requests_by_table(inventory, requests, cancelled)
    token = get_token() if token is None else token
    found = {}
    for key in sorted(grouped):
        _check_cancelled(cancelled)
        table, wanted = grouped[key]["table"], grouped[key]["rows"]
        with open_item_table(inventory, table, token=token, streaming=True) as parquet:
            _check_cancelled(cancelled)
            if len(set(parquet.schema_arrow.names)) != len(parquet.schema_arrow.names):
                raise ValueError("Benchmark tables must have unique column names")
            if "row_count" in table and parquet.metadata.num_rows != table["row_count"]:
                raise ValueError("Benchmark table row count differs from the pinned inventory")
            rows = _table_rows(_CancellableTable(parquet, cancelled), columns=None, selected_rows=wanted)
            returned = set()
            with closing(rows):
                for row_number, row in rows:
                    _check_cancelled(cancelled)
                    item_id = wanted[row_number]
                    if row_fingerprint(row) != item_id:
                        raise ValueError("Fetched benchmark row does not match its indexed item hash")
                    original_id = row_text({"item_id": row.get("item_id")})
                    for source in sources_by_id[item_id]:
                        if "item_id" in source and row_text({"item_id": source["item_id"]}) != original_id:
                            raise ValueError("Fetched benchmark row differs from its source item identifier")
                    found[item_id] = row
                    returned.add(row_number)
            if returned != set(wanted):
                raise ValueError("Requested benchmark rows are missing from their pinned table")
    _check_cancelled(cancelled)
    return {item_id: found[item_id] for item_id in sources_by_id}
