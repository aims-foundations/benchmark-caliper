"""Complete Parquet row preservation and identity without network access."""

from copy import deepcopy
from datetime import date, datetime
from decimal import Decimal
import hashlib
import json
import sqlite3

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from bayesian_auditing import benchmark_data, data
from bayesian_auditing.benchmark_data import iter_benchmark_items, row_fingerprint, row_search_text, row_text


@pytest.fixture
def bank(tmp_path, monkeypatch):
    inventory = {"repo": "fixture/full-rows", "branches": {"main": "pinned-main"}, "tables": []}
    opened, downloads = [], []

    def add(name, rows=None, *, table=None, commit="pinned-main", row_group_size=2):
        path = f"{name}/formatted_tables/items.parquet"
        local = tmp_path / commit / path
        local.parent.mkdir(parents=True, exist_ok=True)
        table = pa.Table.from_pylist(rows) if table is None else table
        pq.write_table(table, local, row_group_size=row_group_size)
        inventory["tables"].append({
            "benchmark": name, "branch": "main", "commit": commit, "items_path": path,
            "row_count": table.num_rows,
            # These paths must never be fetched by the full-row reader.
            "benchmarks_path": f"{name}/formatted_tables/benchmarks.parquet",
            "metadata_path": f"{name}/metadata.yaml",
        })
        return local

    class FileSystem:
        def __init__(self, token):
            assert token == "fixture-token"

        def open(self, path, mode, **kwargs):
            commit, filename = path.split("@", 1)[1].split("/", 1)
            stream = (tmp_path / commit / filename).open(mode)
            opened.append(stream)
            return stream

    def download(repo, filename, *, repo_type, revision, token):
        assert repo == inventory["repo"] and repo_type == "dataset" and token == "fixture-token"
        assert filename.endswith("/items.parquet"), "Only original item tables may be downloaded"
        downloads.append((revision, filename))
        return str(tmp_path / revision / filename)

    monkeypatch.setattr(data, "HfFileSystem", FileSystem)
    monkeypatch.setattr(data, "hf_hub_download", download)
    monkeypatch.setattr(data, "_context", lambda *args, **kwargs: pytest.fail("Do not load benchmark metadata"))
    return inventory, add, opened, downloads


def test_reader_keeps_every_original_column_and_json_string(bank):
    inventory, add, opened, downloads = bank
    row = {
        "item_id": "question-1", "benchmark_id": "mathematics", "content": "What is 1 + 1?",
        "grading_criterion": ' { "answer": 2, "rule" : "exact" }\n',
        "reference_answer": '"2"', "verifier": '{ "kind": "exact" }',
        "item_features": '[ "text", "math" ]', "asset_manifest": None,
        "extra_field": "  Source text: café\n", "new_flag": True,
    }
    add("mathematics", [row])
    loaded, = iter_benchmark_items(inventory, token="fixture-token")
    assert loaded["evidence"] == {"item": row}
    assert loaded["evidence_hash"] == row_fingerprint(row)
    assert loaded["source"] == {
        "repo": inventory["repo"], "branch": "main", "commit": "pinned-main",
        "benchmark": "mathematics", "items_path": "mathematics/formatted_tables/items.parquet",
        "item_id": "question-1", "row": 1,
    }
    assert json.loads(row_text(loaded["evidence"]["item"])) == row
    assert len(opened) == 1 and opened[0].closed
    assert downloads == []


def test_ids_json_whitespace_and_additional_columns_define_row_identity(bank):
    inventory, add, _, _ = bank
    original = {"item_id": "one", "benchmark_id": "math", "content": "Same question",
                "grading_criterion": '{"answer":2}', "extra": "original"}
    rows = [original, {**original, "item_id": "two"}, {**original, "benchmark_id": "other"},
            {**original, "grading_criterion": '{ "answer": 2 }'}, {**original, "extra": "changed"}]
    add("math", rows)
    loaded = list(iter_benchmark_items(inventory, token="fixture-token"))
    assert len({item["evidence_hash"] for item in loaded}) == 5
    assert [item["evidence"]["item"] for item in loaded] == rows
    assert [item["source"]["row"] for item in loaded] == [1, 2, 3, 4, 5]


def test_identical_rows_at_different_sources_keep_same_identity(bank):
    inventory, add, _, _ = bank
    row = {"item_id": "same", "benchmark_id": "original-bank", "content": "Same original row"}
    add("first", [row, row])
    add("second", [row], commit="other-pin")
    loaded = list(iter_benchmark_items(inventory, token="fixture-token"))
    assert len({item["evidence_hash"] for item in loaded}) == 1
    assert len({json.dumps(item["source"], sort_keys=True) for item in loaded}) == 3
    assert all(item["evidence"] == {"item": row} for item in loaded)


def test_reader_does_not_sample_filter_release_or_require_content(bank):
    inventory, add, _, _ = bank
    rows = [{"item_id": str(i), "release": "withheld" if i % 2 else "public", "input": f"Input {i}"}
            for i in range(160)]
    add("all-rows", rows, row_group_size=70)
    loaded = list(iter_benchmark_items(inventory, token="fixture-token"))
    assert [item["evidence"]["item"] for item in loaded] == rows
    assert [item["source"]["row"] for item in loaded] == list(range(1, 161))


def test_local_and_streaming_readers_match_and_close_on_early_stop(bank):
    inventory, add, opened, downloads = bank
    add("math", [{"item_id": str(i), "content": "Question"} for i in range(4)])
    expected = list(iter_benchmark_items(inventory, token="fixture-token", streaming=False))
    assert list(iter_benchmark_items(inventory, token="fixture-token")) == expected
    assert len(downloads) == 1
    stream = iter_benchmark_items(inventory, token="fixture-token")
    assert next(stream) == expected[0]
    assert not opened[-1].closed
    stream.close()
    assert opened[-1].closed


def test_serialization_is_stable_lossless_and_does_not_mutate_rows():
    row = {"z": [1, 1.0, True, None, "é", {"b": 2, "a": 1}],
           "a": ' {"b": 2, "a": 1} ', "item_id": "one"}
    original = deepcopy(row)
    encoded = row_text(row)
    assert encoded.startswith('{"a":') and "é" in encoded
    assert json.loads(encoded) == row
    reordered = {"item_id": "one", "a": row["a"], "z": [*row["z"][:-1], {"a": 1, "b": 2}]}
    assert row_text(reordered) == encoded
    assert row_fingerprint(row) == hashlib.sha256(encoded.encode("utf-8")).hexdigest()
    assert row == original


def test_search_representation_keeps_all_fields_and_original_string_whitespace():
    row = {"item_id": "question-1", "content": "Blood\npressure", "grading_criterion": "select\ntherapy",
           "new_column": ' { "literal": "JSON cell" } ', "metadata": {"note": "New\ncontext"},
           "array": ["first\noption", None, True, 1, 1.5], "empty": [], "object": {}}
    original = deepcopy(row)
    canonical, identity = row_text(row), row_fingerprint(row)
    text = row_search_text(row)
    assert text == "\n".join([
        "array: [first\noption,\nnull,\ntrue,\n1,\n1.5]", "content: Blood\npressure", "empty: []",
        "grading_criterion: select\ntherapy", "item_id: question-1", "metadata: {note: New\ncontext}",
        'new_column:  { "literal": "JSON cell" } ', "object: {}",
    ])
    assert row_search_text(dict(reversed(list(row.items())))) == text
    assert row == original and row_text(row) == canonical and row_fingerprint(row) == identity


@pytest.mark.parametrize("term", ["pressure", "therapy", "identifier", "context", "newfield", "option"])
def test_search_text_preserves_keyword_boundaries_in_every_field(term):
    row = {"item_id": "source\nidentifier", "content": "Blood\npressure",
           "grading_criterion": "Select\ntherapy", "metadata": {"note": "Relevant\ncontext"},
           "new_column": "Additional\nnewfield", "options": ["First\noption"]}
    with sqlite3.connect(":memory:") as connection:
        connection.execute("CREATE VIRTUAL TABLE words USING fts5(text)")
        connection.execute("INSERT INTO words(text) VALUES (?)", (row_search_text(row),))
        assert connection.execute("SELECT COUNT(*) FROM words WHERE words MATCH ?", (term,)).fetchone()[0] == 1


@pytest.mark.parametrize("left,right", [
    ({"value": "1"}, {"value": 1}), ({"value": 1}, {"value": 1.0}),
    ({"value": True}, {"value": 1}), ({"value": None}, {"value": "null"}),
    ({"value": [1, 2]}, {"value": [2, 1]}), ({"a": 1}, {"a": 1, "b": None}),
    ({"value": '{"a":1}'}, {"value": {"a": 1}}),
])
def test_distinct_row_values_do_not_collapse_during_serialization(left, right):
    assert row_fingerprint(left) != row_fingerprint(right)


def test_json_compatible_arrow_types_round_trip_without_casts(bank):
    inventory, add, _, _ = bank
    row = {"item_id": "typed", "string": "literal", "flag": True, "integer": 2**60,
           "number": 1.5, "array": ["first", None], "object": {"nested": "value"}, "empty": None}
    add("types", [row])
    loaded, = iter_benchmark_items(inventory, token="fixture-token")
    assert loaded["evidence"]["item"] == row
    assert json.loads(row_text(loaded["evidence"]["item"])) == row


@pytest.mark.parametrize("value", [b"binary", date(2026, 10, 24), datetime(2026, 10, 24, 12, 30), Decimal("1.00")])
def test_unsupported_arrow_scalars_fail_explicitly_and_close_reader(bank, value):
    inventory, add, opened, _ = bank
    add("unsupported", [{"item_id": "one", "extra": value}])
    with pytest.raises(ValueError, match="Unsupported benchmark row value type"):
        list(iter_benchmark_items(inventory, token="fixture-token"))
    assert opened[-1].closed


@pytest.mark.parametrize("row", [
    {"number": float("nan")}, {"number": float("inf")}, {"object": {1: "numeric key"}},
    {"array": (1, 2)}, [1, 2],
])
def test_serialization_rejects_lossy_or_nonfinite_values(row):
    with pytest.raises(ValueError):
        row_text(row)


@pytest.mark.parametrize("row", [{"content": "Question"}, {"item_id": None, "content": "Question"}])
def test_missing_source_identifier_does_not_drop_an_original_row(bank, row):
    inventory, add, _, _ = bank
    add("missing-id", [row])
    loaded, = iter_benchmark_items(inventory, token="fixture-token")
    assert loaded["evidence"]["item"] == row
    assert loaded["source"]["item_id"] is None
    assert loaded["source"]["row"] == 1
    assert loaded["evidence_hash"] == row_fingerprint(row)


def test_duplicate_columns_fail_instead_of_losing_original_values(bank):
    inventory, add, opened, _ = bank
    table = pa.Table.from_arrays([pa.array(["one"]), pa.array(["two"])], names=["item_id", "item_id"])
    add("invalid", table=table)
    with pytest.raises(ValueError, match="unique column names"):
        list(iter_benchmark_items(inventory, token="fixture-token"))
    assert opened[-1].closed


@pytest.mark.parametrize("expected", [0, 2, None, True, -1])
def test_pinned_table_counts_must_match_actual_parquet_rows(bank, expected):
    inventory, add, opened, _ = bank
    add("wrong-count", [{"item_id": "one"}])
    inventory["tables"][0]["row_count"] = expected
    with pytest.raises(ValueError, match="row count"):
        list(iter_benchmark_items(inventory, token="fixture-token"))
    assert opened[-1].closed


def test_resume_reader_skips_completed_tables_and_keeps_original_row_numbers(bank):
    inventory, add, opened, _ = bank
    add('first', [{'item_id': str(i), 'content': 'first'} for i in range(5)])
    add('second', [{'item_id': str(i), 'content': 'second'} for i in range(8)])
    expected = list(iter_benchmark_items(inventory, token='fixture-token'))
    opened.clear()
    actual = list(iter_benchmark_items(inventory, token='fixture-token', skip_rows=9))
    assert actual == expected[9:]
    assert [row['source']['row'] for row in actual] == [5, 6, 7, 8]
    assert len(opened) == 1 and opened[0].closed
    opened.clear()
    assert list(iter_benchmark_items(inventory, token='fixture-token', skip_rows=13)) == []
    assert not opened
    with pytest.raises(ValueError, match='exceeds'):
        list(iter_benchmark_items(inventory, token='fixture-token', skip_rows=14))


@pytest.mark.parametrize('offset', [-1, True, 1.5])
def test_resume_reader_rejects_invalid_offset(bank, offset):
    inventory, _, _, _ = bank
    with pytest.raises(ValueError, match='nonnegative integer'):
        list(iter_benchmark_items(inventory, token='fixture-token', skip_rows=offset))
