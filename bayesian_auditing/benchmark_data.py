"""Read complete benchmark rows without changing their values or item identity.

Step 4 keeps every items.parquet column. Source locations are recorded separately
and never change whether two original rows are identical.
"""

import hashlib
import json
import math

from .data import _table_rows, open_item_table


BENCHMARK_DATA_VERSION = 1


def _check_json_value(value) -> None:
    """Reject values that JSON would silently coerce or cannot preserve."""
    if value is None or type(value) in {str, bool, int}:
        return
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("Benchmark rows cannot contain non-finite numeric values.")
        return
    if type(value) is list:
        for nested in value:
            _check_json_value(nested)
        return
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise ValueError("Benchmark row objects require string field names.")
        for nested in value.values():
            _check_json_value(nested)
        return
    raise ValueError(f"Unsupported benchmark row value type: {type(value).__name__}.")


def row_text(row: dict) -> str:
    """Serialize every original field canonically for exact-row identity.

    JSON-compatible Arrow values retain their types, including nulls and nested
    arrays/objects. JSON stored inside a string cell is not parsed or normalized.
    Column/object key order does not affect identity; list order and string
    contents do. Unsupported Arrow scalar types fail rather than being cast to
    strings or dropped.
    """
    if type(row) is not dict:
        raise ValueError("A benchmark item must be a complete row object.")
    _check_json_value(row)
    return json.dumps(row, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def row_fingerprint(row: dict) -> str:
    """Hash original column names and values, excluding external provenance."""
    return hashlib.sha256(row_text(row).encode("utf-8")).hexdigest()


def row_search_text(row: dict) -> str:
    """Represent all fields for search, keeping string whitespace verbatim.

    JSON escaping would turn an actual newline before "pressure" into the text
    "\\npressure", changing its keyword token. Search uses readable field labels
    and original string values; canonical row_text still determines identity.
    """
    if type(row) is not dict:
        raise ValueError("A benchmark item must be a complete row object.")
    _check_json_value(row)

    def render(value):
        if type(value) is str:
            return value
        if type(value) is list:
            return "[" + ",\n".join(render(part) for part in value) + "]"
        if type(value) is dict:
            return "{" + ",\n".join(f"{key}: {render(value[key])}" for key in sorted(value)) + "}"
        return json.dumps(value, ensure_ascii=False, allow_nan=False)

    return "\n".join(f"{key}: {render(row[key])}" for key in sorted(row))


def iter_benchmark_items(inventory: dict, *, token: str | None = None,
                         streaming: bool = True):
    """Yield every complete row and its pinned source; never fetch other tables.

    The inventory establishes the branch and collection scope. This reader
    neither filters release labels nor samples rows. It closes the current
    Parquet source when exhausted, cancelled through generator.close(), or failed.
    """
    for table in inventory["tables"]:
        with open_item_table(inventory, table, token=token, streaming=streaming) as parquet:
            names = parquet.schema_arrow.names
            if len(set(names)) != len(names):
                raise ValueError("Benchmark tables must have unique column names.")
            if "row_count" in table:
                expected = table["row_count"]
                if type(expected) is not int or expected < 0:
                    raise ValueError("Pinned benchmark table row counts must be nonnegative integers.")
                if parquet.metadata.num_rows != expected:
                    raise ValueError(f"Benchmark table row count differs from the pinned inventory: {table['items_path']}")
            for row_number, row in _table_rows(parquet, columns=None):
                yield {
                    "evidence": {"item": row},
                    "evidence_hash": row_fingerprint(row),
                    "source": {
                        "repo": inventory["repo"], "branch": table["branch"],
                        "commit": table["commit"], "benchmark": table["benchmark"],
                        "items_path": table["items_path"], "item_id": row.get("item_id"),
                        "row": row_number,
                    },
                }
