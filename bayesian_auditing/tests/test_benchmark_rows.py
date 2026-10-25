"""Shortlist hydration from real Parquet fixtures, without network requests."""

from contextlib import contextmanager
from copy import deepcopy
from datetime import date

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from bayesian_auditing import benchmark_rows as module
from bayesian_auditing.benchmark_data import row_fingerprint
from bayesian_auditing.benchmark_rows import fetch_benchmark_rows


@pytest.fixture
def bank(tmp_path, monkeypatch):
    inventory = {"repo": "fixture/bank", "branches": {"main": "pinned"}, "tables": []}
    opened, reads, hooks = [], [], {}

    def add(name, rows=None, *, arrow=None, row_group_size=2, branch="main", commit="pinned"):
        table = {"branch": branch, "commit": commit, "benchmark": name,
                 "items_path": f"{name}/items.parquet"}
        arrow = pa.Table.from_pylist(rows) if arrow is None else arrow
        table["row_count"] = arrow.num_rows
        inventory["branches"][branch] = commit
        inventory["tables"].append(table)
        path = tmp_path / commit / table["items_path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(arrow, path, row_group_size=row_group_size)
        return table

    @contextmanager
    def open_source(actual_inventory, table, *, token, streaming):
        assert actual_inventory is inventory and token == "fixture-token" and streaming is True
        path = tmp_path / table["commit"] / table["items_path"]
        with path.open("rb") as handle:
            opened.append((table["items_path"], handle))
            with pq.ParquetFile(handle) as parquet:
                class RecordedTable:
                    metadata = parquet.metadata
                    schema_arrow = parquet.schema_arrow

                    def iter_batches(self, **kwargs):
                        reads.append((table["items_path"], kwargs["row_groups"], kwargs["columns"]))
                        for batch in parquet.iter_batches(**kwargs):
                            if callback := hooks.get("on_batch"):
                                callback()
                            yield batch

                yield RecordedTable()

    monkeypatch.setattr(module, "open_item_table", open_source)
    monkeypatch.setattr(module, "get_token", lambda: "fixture-token")
    return inventory, add, opened, reads, hooks


def request(inventory, table, row, number):
    return {"item_id": row_fingerprint(row), "sources": [{
        "repo": inventory["repo"], **{key: table[key] for key in module._TABLE_FIELDS},
        "row": number, "item_id": row.get("item_id"),
    }]}


def test_complete_original_rows_and_unknown_columns_remain_unchanged(bank):
    inventory, add, opened, reads, _ = bank
    row = {"item_id": "q1", "content": "Literal\nquestion", "grading_criterion": ' { "answer": 1 } ',
           "reference_answer": '"one"', "new_column": {"flag": True, "integer": 2**60},
           "options": [" first ", None, "é"], "null": None, "number": 1.0}
    table = add("first", [row])
    wanted = [request(inventory, table, row, 1)]
    original = deepcopy(wanted)
    assert fetch_benchmark_rows(inventory, wanted) == {wanted[0]["item_id"]: row}
    assert wanted == original
    assert reads == [("first/items.parquet", [0], None)]
    assert len(opened) == 1 and opened[0][1].closed


def test_requests_share_one_table_open_and_only_needed_row_groups(bank):
    inventory, add, opened, reads, _ = bank
    rows = [{"item_id": str(i), "content": f"Question {i}"} for i in range(8)]
    table = add("first", rows)
    wanted = [request(inventory, table, rows[i], i + 1) for i in (5, 1, 0)]
    wanted.append(deepcopy(wanted[0]))
    actual = fetch_benchmark_rows(inventory, wanted, token="fixture-token")
    assert actual == {row_fingerprint(rows[i]): rows[i] for i in (5, 1, 0)}
    assert len(opened) == 1 and opened[0][1].closed
    assert reads == [("first/items.parquet", [0], None), ("first/items.parquet", [2], None)]


def test_duplicate_source_representative_is_deterministic_and_requests_merge(bank):
    inventory, add, opened, _, _ = bank
    row = {"item_id": "same", "content": "Identical entire row"}
    z, a = add("z", [row]), add("a", [row])
    requests = [request(inventory, z, row, 1), request(inventory, a, row, 1)]
    first = fetch_benchmark_rows(inventory, requests)
    second = fetch_benchmark_rows(inventory, list(reversed(requests)))
    assert first == second == {row_fingerprint(row): row}
    assert [path for path, _ in opened] == ["a/items.parquet", "a/items.parquet"]


def test_distinct_commits_are_opened_separately(bank):
    inventory, add, opened, _, _ = bank
    first, second = {"item_id": "old", "content": "First"}, {"item_id": "new", "content": "Second"}
    old = add("bank", [first])
    new = add("bank", [second], branch="other", commit="other-pin")
    result = fetch_benchmark_rows(inventory, [request(inventory, old, first, 1), request(inventory, new, second, 1)])
    assert result == {row_fingerprint(first): first, row_fingerprint(second): second}
    assert len(opened) == 2 and all(handle.closed for _, handle in opened)


def test_branch_aliases_of_one_pinned_table_share_the_same_read(bank):
    inventory, add, opened, reads, _ = bank
    rows = [{"item_id": "one"}, {"item_id": "two"}]
    first = add("bank", rows)
    alias = {**first, "branch": "alias"}
    inventory["branches"]["alias"] = first["commit"]
    inventory["tables"].append(alias)
    wanted = [request(inventory, first, rows[0], 1), request(inventory, alias, rows[1], 2)]
    assert fetch_benchmark_rows(inventory, wanted) == {row_fingerprint(row): row for row in rows}
    assert len(opened) == 1 and reads == [("bank/items.parquet", [0], None)]


@pytest.mark.parametrize("field,value", [
    ("repo", "different/repository"), ("commit", "unpinned"), ("branch", "other"),
    ("benchmark", "other"), ("items_path", "other/items.parquet"),
    ("row", 0), ("row", -1), ("row", 2), ("row", True), ("row", "1"), ("row", 1.0),
])
def test_every_source_is_validated_before_any_read_including_unchosen_sources(bank, field, value):
    inventory, add, opened, _, _ = bank
    row = {"item_id": "one"}
    table = add("bank", [row])
    wanted = request(inventory, table, row, 1)
    wanted["sources"].append({**wanted["sources"][0], field: value})
    with pytest.raises(ValueError, match="source"):
        fetch_benchmark_rows(inventory, [wanted])
    assert not opened


def test_missing_hash_source_and_invalid_requests_fail_without_io(bank):
    inventory, _, opened, _, _ = bank
    for wanted in (None, {}, [None], [{}], [{"item_id": "bad", "sources": []}],
                   [{"item_id": "a" * 64, "sources": []}], [{"item_id": "a" * 64, "sources": [None]}]):
        with pytest.raises(ValueError):
            fetch_benchmark_rows(inventory, wanted)
    assert not opened


def test_empty_requests_do_not_access_credentials_or_sources(monkeypatch):
    monkeypatch.setattr(module, "get_token", lambda: pytest.fail("Empty shortlist requires no credentials"))
    monkeypatch.setattr(module, "open_item_table", lambda *args, **kwargs: pytest.fail("Empty shortlist requires no source"))
    assert fetch_benchmark_rows({}, []) == {}


def test_hash_mismatch_and_source_identifier_mismatch_close_the_table(bank):
    inventory, add, opened, _, _ = bank
    row = {"item_id": "actual", "content": "Original"}
    table = add("bank", [row])
    wanted = request(inventory, table, row, 1)
    wanted["item_id"] = "0" * 64
    with pytest.raises(ValueError, match="hash"):
        fetch_benchmark_rows(inventory, [wanted])
    assert opened[-1][1].closed
    wanted = request(inventory, table, row, 1)
    wanted["sources"][0]["item_id"] = "different"
    with pytest.raises(ValueError, match="source item identifier"):
        fetch_benchmark_rows(inventory, [wanted])
    assert opened[-1][1].closed


def test_one_source_row_cannot_claim_different_item_hashes(bank):
    inventory, add, opened, _, _ = bank
    row = {"item_id": "actual"}
    table = add("bank", [row])
    wanted = request(inventory, table, row, 1)
    other = {**wanted, "item_id": "0" * 64}
    with pytest.raises(ValueError, match="different items"):
        fetch_benchmark_rows(inventory, [wanted, other])
    assert not opened


def test_changed_table_count_and_missing_requested_row_fail_explicitly(bank, monkeypatch):
    inventory, add, opened, _, _ = bank
    row = {"item_id": "one"}
    table = add("bank", [row])
    wanted = request(inventory, table, row, 1)
    table["row_count"] = 2
    with pytest.raises(ValueError, match="row count"):
        fetch_benchmark_rows(inventory, [wanted])
    assert opened[-1][1].closed
    table["row_count"] = 1
    # Use a closing-capable empty generator to model a reader omitting a row.
    def no_rows(*args, **kwargs):
        yield from ()
    monkeypatch.setattr(module, "_table_rows", no_rows)
    with pytest.raises(ValueError, match="missing"):
        fetch_benchmark_rows(inventory, [wanted])
    assert opened[-1][1].closed


def test_duplicate_columns_and_unsupported_values_fail_without_coercion(bank):
    inventory, add, opened, _, _ = bank
    arrow = pa.Table.from_arrays([pa.array(["first"]), pa.array(["second"])], names=["item_id", "item_id"])
    table = add("duplicate-columns", arrow=arrow)
    wanted = request(inventory, table, {"item_id": "first"}, 1)
    with pytest.raises(ValueError, match="unique column"):
        fetch_benchmark_rows(inventory, [wanted])
    assert opened[-1][1].closed
    table = add("unsupported", [{"item_id": "one", "date": date(2026, 10, 25)}])
    wanted = request(inventory, table, {"item_id": "one"}, 1)
    with pytest.raises(ValueError, match="Unsupported"):
        fetch_benchmark_rows(inventory, [wanted])
    assert opened[-1][1].closed


def test_missing_table_and_access_errors_are_not_silently_skipped(bank, monkeypatch):
    inventory, add, _, _, _ = bank
    row = {"item_id": "one"}
    table = add("bank", [row])
    def denied(*args, **kwargs):
        raise PermissionError("Source access denied")
    monkeypatch.setattr(module, "open_item_table", denied)
    with pytest.raises(PermissionError, match="Source access denied"):
        fetch_benchmark_rows(inventory, [request(inventory, table, row, 1)])


def test_cancellation_before_open_avoids_credentials_and_io(bank, monkeypatch):
    inventory, add, opened, _, _ = bank
    row = {"item_id": "one"}
    table = add("bank", [row])
    monkeypatch.setattr(module, "get_token", lambda: pytest.fail("Already cancelled"))
    with pytest.raises(InterruptedError, match="cancelled"):
        fetch_benchmark_rows(inventory, [request(inventory, table, row, 1)], cancelled=lambda: True)
    assert not opened


def test_cancellation_while_skipping_rows_checks_each_batch_and_closes_source(bank):
    inventory, add, opened, reads, hooks = bank
    rows = [{"item_id": str(i)} for i in range(600)]
    table = add("bank", rows, row_group_size=600)
    stopped, batches = False, 0
    def on_batch():
        nonlocal stopped, batches
        batches += 1
        stopped = True
    hooks["on_batch"] = on_batch
    with pytest.raises(InterruptedError, match="cancelled"):
        fetch_benchmark_rows(inventory, [request(inventory, table, rows[-1], 600)], cancelled=lambda: stopped)
    assert batches == 1 and reads == [("bank/items.parquet", [0], None)]
    assert len(opened) == 1 and opened[0][1].closed


def test_failure_in_a_later_table_returns_no_partial_result_and_closes_all(bank):
    inventory, add, opened, _, _ = bank
    one, two = {"item_id": "one"}, {"item_id": "two"}
    a, b = add("a", [one]), add("b", [two])
    wanted = [request(inventory, a, one, 1), request(inventory, b, two, 1)]
    wanted[1]["item_id"] = "0" * 64
    with pytest.raises(ValueError, match="hash"):
        fetch_benchmark_rows(inventory, wanted)
    assert len(opened) == 2 and all(handle.closed for _, handle in opened)
