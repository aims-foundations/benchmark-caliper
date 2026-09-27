"""Discover pinned item tables and read their evidence without embedding retrieval."""

from __future__ import annotations

import hashlib
import json
from contextlib import contextmanager
from pathlib import Path, PurePosixPath

from huggingface_hub import HfApi, HfFileSystem, hf_hub_download
import pyarrow.parquet as pq
import yaml

REPO = "aims-foundations/measurement-db"
BRANCHES = ("main", "migration/tabular-builders-20260924")
DATA_VERSION = 1

# Omit aggregate model performance: it is not evidence of deployment compatibility.
BENCHMARK_FIELDS = (
    "name", "description", "one_line_description", "testing_condition", "domain",
    "modality", "multi_single_turn", "response_type", "response_scale", "categorical",
    "item_type", "granularity", "has_ground_truth", "benchmark_features",
)
ITEM_FIELDS = (
    "item_id", "benchmark_id", "content", "grading_criterion", "reference_answer",
    "verifier", "item_features", "asset_manifest",
)


def fingerprint(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def discover_inventory(branches=BRANCHES, benchmarks=None, *, api=None) -> dict:
    """Inspect only benchmark roots and formatted_tables/, never raw/ or traces."""
    api = api or HfApi()
    refs = {ref.name: ref.target_commit for ref in api.list_repo_refs(REPO, repo_type="dataset").branches}
    inventory = {"repo": REPO, "branches": {}, "tables": [], "missing_item_tables": []}
    requested = set(benchmarks or [])
    found = set()
    for branch in dict.fromkeys(branches):
        if branch not in refs:
            raise ValueError(f"Branch {branch!r} does not exist; available: {sorted(refs)}")
        commit = refs[branch]
        inventory["branches"][branch] = commit
        root = list(api.list_repo_tree(REPO, repo_type="dataset", revision=commit))
        directories = sorted(entry.path for entry in root if not hasattr(entry, "size"))
        for benchmark in directories:
            if requested and benchmark not in requested:
                continue
            found.add(benchmark)
            entries = list(api.list_repo_tree(
                REPO, repo_type="dataset", revision=commit, path_in_repo=benchmark,
            ))
            paths = {entry.path for entry in entries}
            if f"{benchmark}/formatted_tables" in paths:
                paths.update(entry.path for entry in api.list_repo_tree(
                    REPO, repo_type="dataset", revision=commit,
                    path_in_repo=f"{benchmark}/formatted_tables",
                ))
            item_paths = sorted(p for p in paths if p.endswith("/items.parquet"))
            if not item_paths:
                inventory["missing_item_tables"].append({"branch": branch, "benchmark": benchmark})
            for path in item_paths:
                parent = str(PurePosixPath(path).parent)
                inventory["tables"].append({
                    "branch": branch, "commit": commit, "benchmark": benchmark,
                    "items_path": path,
                    "benchmarks_path": f"{parent}/benchmarks.parquet" if f"{parent}/benchmarks.parquet" in paths else None,
                    "metadata_path": f"{benchmark}/metadata.yaml" if f"{benchmark}/metadata.yaml" in paths else None,
                })
    if requested - found:
        raise ValueError(f"Unknown benchmarks: {sorted(requested - found)}")
    if not inventory["tables"]:
        raise ValueError("No item tables found in the selected branches and benchmarks")
    return inventory


def _download(inventory: dict, table: dict, path: str, token: str | None = None) -> Path:
    return Path(hf_hub_download(
        inventory["repo"], path, repo_type="dataset", revision=table["commit"],
        **({"token": token} if token else {}),
    ))


def _decode(value):
    """Some table fields contain JSON, while others contain ordinary prose."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    return value


def _context(inventory: dict, table: dict, token: str | None = None) -> tuple[dict, dict]:
    by_id = {}
    if table["benchmarks_path"]:
        for row in pq.read_table(_download(inventory, table, table["benchmarks_path"], token)).to_pylist():
            by_id[str(row["benchmark_id"])] = {
                key: _decode(row[key]) for key in BENCHMARK_FIELDS if row.get(key) is not None
            }
    documentation = {}
    if table["metadata_path"]:
        metadata = yaml.safe_load(_download(inventory, table, table["metadata_path"], token).read_text(encoding="utf-8"))
        # The benchmark section contains source descriptions; build instructions
        # and historical model responses do not belong in the judging prompt.
        documentation = (metadata or {}).get("benchmark", {})
        # YAML may parse dates into date objects; normalize them to JSON strings.
        documentation = json.loads(json.dumps(documentation, default=str))
    return by_id, documentation


@contextmanager
def open_item_table(inventory: dict, table: dict, *, token=None, streaming=False):
    """The hosted reader uses HTTP ranges instead of caching multi-GB tables."""
    if streaming:
        filesystem = HfFileSystem(token=token)
        path = f"datasets/{inventory['repo']}@{table['commit']}/{table['items_path']}"
        with filesystem.open(path, "rb", block_size=1024 * 1024, cache_type="readahead") as source:
            with pq.ParquetFile(source) as parquet:
                yield parquet
    else:
        with pq.ParquetFile(_download(inventory, table, table["items_path"], token)) as parquet:
            yield parquet


def _table_rows(parquet, columns, selected_rows=None):
    """Keep original 1-based row numbers, reading only needed row groups."""
    wanted = None if selected_rows is None else set(selected_rows)
    if wanted is not None and any(row < 1 or row > parquet.metadata.num_rows for row in wanted):
        raise ValueError("Selected row outside the item table")
    start = 1
    for group in range(parquet.metadata.num_row_groups):
        end = start + parquet.metadata.row_group(group).num_rows
        if wanted is None or any(start <= row < end for row in wanted):
            row_number = start
            for batch in parquet.iter_batches(batch_size=128, columns=columns, row_groups=[group]):
                for row in batch.to_pylist():
                    if wanted is None or row_number in wanted:
                        yield row_number, row
                    row_number += 1
        start = end


def iter_items(inventory: dict, limit_per_table: int | None = None, *, token: str | None = None,
               streaming: bool = False, selected_rows: dict | None = None):
    """Yield full text evidence and provenance in deterministic table/row order.

    A table read failure raises instead of silently omitting part of the corpus.
    Media references are preserved, but this text demo does not load their assets.
    """
    if limit_per_table is not None and limit_per_table <= 0:
        raise ValueError("limit_per_table must be positive")
    for table in inventory["tables"]:
        rows = None if selected_rows is None else selected_rows.get((table["branch"], table["items_path"]), [])
        if rows == []:
            continue
        by_id, documentation = _context(inventory, table, token)
        with open_item_table(inventory, table, token=token, streaming=streaming) as parquet:
            if not {"item_id", "content"}.issubset(parquet.schema_arrow.names):
                raise ValueError(f"Missing item_id/content columns: {table['items_path']}")
            columns = [name for name in ITEM_FIELDS if name in parquet.schema_arrow.names]
            for count, (row_number, row) in enumerate(_table_rows(parquet, columns, rows)):
                if limit_per_table is not None and count >= limit_per_table:
                    break
                if row["item_id"] is None:
                    raise ValueError(f"Missing item ID in {table['items_path']}, row {row_number}")
                source = {
                    "repo": inventory["repo"], "branch": table["branch"],
                    "commit": table["commit"], "benchmark": table["benchmark"],
                    "items_path": table["items_path"], "item_id": str(row["item_id"]),
                    "row": row_number,
                }
                grading = _decode(row.get("grading_criterion"))
                if grading is None and row.get("reference_answer") is not None:
                    grading = {"reference_answer": _decode(row["reference_answer"])}
                benchmark_id = str(row.get("benchmark_id", table["benchmark"]))
                evidence = {
                    "item": {
                        "content": row.get("content"), "grading_criterion": grading,
                        "verifier": _decode(row.get("verifier")),
                        "item_features": _decode(row.get("item_features")),
                        "asset_manifest": _decode(row.get("asset_manifest")),
                    },
                    "benchmark": by_id.get(benchmark_id, {}),
                    "documentation": documentation,
                    "media_assets_included": False,
                }
                yield {"source": source, "evidence": evidence, "evidence_hash": fingerprint(evidence)}
