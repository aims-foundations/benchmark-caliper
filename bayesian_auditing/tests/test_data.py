import pytest

from bayesian_auditing.data import BRANCHES, discover_inventory, iter_items


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
