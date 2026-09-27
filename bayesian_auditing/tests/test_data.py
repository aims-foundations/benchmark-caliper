import pytest

from bayesian_auditing.data import BRANCHES, discover_inventory, iter_items
from bayesian_auditing import data


def test_both_layouts_are_pinned_and_read(corpus):
    inventory, _, _ = corpus
    assert list(inventory["branches"]) == list(BRANCHES)
    assert [table["items_path"] for table in inventory["tables"]] == [
        "math/items.parquet", "math/formatted_tables/items.parquet",
    ]
    items = list(iter_items(inventory))
    assert len(items) == 4
    assert items[0]["evidence"]["item"]["grading_criterion"]["reference_answer"] == "2"
    assert items[0]["evidence"]["documentation"] == {"description": "Simple arithmetic"}
    assert "coverage" not in items[0]["evidence"]["benchmark"]
    assert items[0]["source"]["commit"] == "a" * 40
    assert items[2]["source"]["commit"] == "b" * 40


def test_duplicates_require_identical_grading_and_context(corpus):
    items = list(iter_items(corpus[0]))
    assert items[0]["evidence_hash"] == items[2]["evidence_hash"]
    assert items[0]["source"] != items[2]["source"]
    assert items[0]["evidence_hash"] != items[3]["evidence_hash"]


def test_limit_reaches_both_tables(corpus):
    items = list(iter_items(corpus[0], limit_per_table=1))
    assert len(items) == 2
    assert {item["source"]["branch"] for item in items} == set(BRANCHES)


def test_unknown_branch_and_benchmark_are_errors(corpus):
    _, api, _ = corpus
    with pytest.raises(ValueError, match="does not exist"):
        discover_inventory(["unknown"], api=api)
    with pytest.raises(ValueError, match="Unknown benchmarks"):
        discover_inventory(benchmarks=["unknown"], api=api)


def test_streaming_reads_both_layouts_and_closes_files(corpus, monkeypatch):
    inventory, _, root = corpus
    opened = []

    class FileSystem:
        def __init__(self, token):
            assert token is None

        def open(self, path, mode, **options):
            assert options['block_size'] == 1024 * 1024
            commit, filename = path.split('@', 1)[1].split('/', 1)
            stream = (root / commit / filename).open(mode)
            opened.append(stream)
            return stream

    monkeypatch.setattr(data, "HfFileSystem", FileSystem)
    assert list(iter_items(inventory, streaming=True)) == list(iter_items(inventory))
    assert len(opened) == 2 and all(stream.closed for stream in opened)


def test_selected_rows_keep_original_positions_across_row_groups(corpus):
    import pyarrow as pa
    import pyarrow.parquet as pq
    inventory, _, root = corpus
    table = inventory["tables"][0]
    path = root / table["commit"] / table["items_path"]
    first = pq.read_table(path).to_pylist()[0]
    pq.write_table(pa.Table.from_pylist([
        {**first, "item_id": str(number), "content": f"Question {number}"}
        for number in range(1, 10)
    ]), path, row_group_size=3)
    rows = list(iter_items(inventory, selected_rows={(table["branch"], table["items_path"]): [9, 4]}))
    assert [row["source"]["row"] for row in rows] == [4, 9]
    assert [row["evidence"]["item"]["content"] for row in rows] == ["Question 4", "Question 9"]
    with pytest.raises(ValueError, match="outside the item table"):
        list(iter_items(inventory, selected_rows={(table["branch"], table["items_path"]): [10]}))
