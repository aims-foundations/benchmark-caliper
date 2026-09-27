"""Selection properties: duplicates, branches, reproducibility, and pinned cache."""

import copy
import json
from threading import Event

import pytest

from bayesian_auditing import sampling


def row(number, branch="main", *, benchmark="math", evidence_hash=None):
    return {"evidence_hash": evidence_hash or str(number), "evidence": {"item": {"content": str(number)}},
            "source": {"branch": branch, "benchmark": benchmark, "items_path": f"{branch}/items.parquet",
                       "row": number + 1, "item_id": str(number)}}


def inventory(rows):
    return {"repo": "fixture", "branches": {"main": "a", "migration": "b"}, "tables": [
        {"benchmark": "math", "branch": branch, "items_path": f"{branch}/items.parquet", "commit": branch,
         "row_count": sum(r["source"]["branch"] == branch for r in rows)}
        for branch in sorted({r["source"]["branch"] for r in rows})]}


def mock_reader(monkeypatch, rows):
    def read(data, *, selected_rows=None, **kwargs):
        for item in rows:
            source = item["source"]
            if selected_rows is None or source["row"] in selected_rows.get((source["branch"], source["items_path"]), []):
                yield copy.deepcopy(item)
    monkeypatch.setattr(sampling, "iter_items", read)


def test_exact_size_reproducible_and_independent_of_row_order(monkeypatch):
    rows = [row(i) for i in range(300)] + [row(i, "migration") for i in range(250, 500)]
    data = inventory(rows)
    mock_reader(monkeypatch, rows)
    first = sampling.select_benchmark(data)
    assert len(first["items"]) == 50
    assert first["distinct_items"] == 500 and first["source_rows"] == 550
    keys = [item["evidence_hash"] for item in first["items"]]
    assert len(set(keys)) == 50
    assert any(int(key) >= 300 for key in keys)  # Not just the first rows.
    assert any(int(key) < 250 for key in keys)  # Main-exclusive evidence.
    mock_reader(monkeypatch, list(reversed(rows)))
    assert sampling.select_benchmark(data)["items"] == first["items"]
    assert [item["evidence_hash"] for item in sampling.select_benchmark(data, seed=7)["items"]] != keys


def test_duplicates_have_one_lottery_entry_and_all_sources(monkeypatch):
    rows = [row(i) for i in range(150)]
    data = inventory(rows)
    mock_reader(monkeypatch, rows)
    first = sampling.select_benchmark(data)
    selected = first["items"][20]["evidence_hash"]
    duplicates = [row(i + 1000, evidence_hash=selected) for i in range(200)]
    # Duplicate evidence, despite differing row/item identifiers.
    for duplicate in duplicates:
        duplicate["evidence"] = {"item": {"content": selected}}
    mock_reader(monkeypatch, duplicates + rows)
    second = sampling.select_benchmark(data)
    assert [r["evidence_hash"] for r in first["items"]] == [r["evidence_hash"] for r in second["items"]]
    assert len(next(r for r in second["items"] if r["evidence_hash"] == selected)["sources"]) == 201


def test_small_collection_includes_every_distinct_item_and_both_branches(monkeypatch):
    rows = [row(0), row(0, "migration"), row(1, "migration")]
    mock_reader(monkeypatch, rows)
    result = sampling.select_benchmark(inventory(rows))
    assert len(result["items"]) == 2
    assert len(next(r for r in result["items"] if r["evidence_hash"] == "0")["sources"]) == 2


def test_minority_branch_exclusive_item_is_reserved(monkeypatch):
    # Choose an exclusive item whose lottery priority would miss the global sample.
    rows = [row(i) for i in range(500)]
    worst = max(range(500), key=lambda i: sampling._priority(sampling.SAMPLE_SEED, "math", str(i)))
    rows[worst] = row(worst, "migration")
    mock_reader(monkeypatch, rows)
    assert str(worst) in {r["evidence_hash"] for r in sampling.select_benchmark(inventory(rows))["items"]}


def test_cache_reused_and_invalidated_by_seed_and_pins(tmp_path, monkeypatch):
    rows = [row(i) for i in range(120)]
    mock_reader(monkeypatch, rows)
    data = inventory(rows)
    paths, total = sampling.prepare_samples(data, tmp_path)
    assert total == 50 and len(list(sampling.iter_sample_items(paths))) == 50
    original = sampling.select_benchmark
    monkeypatch.setattr(sampling, "select_benchmark", lambda *a, **kw: pytest.fail("Cache should avoid dataset access"))
    assert sampling.prepare_samples(data, tmp_path) == (paths, total)
    monkeypatch.setattr(sampling, "select_benchmark", original)
    data["tables"][0]["commit"] = "new-revision"
    assert sampling.prepare_samples(data, tmp_path)[0] != paths
    monkeypatch.setattr(sampling, "SAMPLE_SEED", 1)
    assert sampling.prepare_samples(data, tmp_path)[0] != paths


def test_cancelled_preparation_publishes_no_partial_cache(tmp_path, monkeypatch):
    rows = [row(i) for i in range(120)]
    mock_reader(monkeypatch, rows)
    cancelled = Event()
    def progress(*args):
        cancelled.set()
    with pytest.raises(InterruptedError):
        sampling.prepare_samples(inventory(rows), tmp_path, cancelled=cancelled, progress=progress)
    assert not list(tmp_path.iterdir())


def test_real_parquet_round_trip_preserves_duplicate_sources(corpus):
    data, _, _ = corpus
    sample = sampling.select_benchmark(data, streaming=False)
    assert sample["source_rows"] == 4 and sample["distinct_items"] == 3
    assert len(sample["items"]) == 3
    assert sorted(len(item["sources"]) for item in sample["items"]) == [1, 1, 2]


def test_oversized_cache_is_rejected_before_review(tmp_path, monkeypatch):
    rows = [row(i) for i in range(120)]
    mock_reader(monkeypatch, rows)
    data = inventory(rows)
    paths, _ = sampling.prepare_samples(data, tmp_path)
    cached = json.loads(paths[0].read_text())
    cached["items"].append(cached["items"][0])
    paths[0].write_text(json.dumps(cached))
    with pytest.raises(ValueError, match="Invalid cached benchmark sample"):
        sampling.prepare_samples(data, tmp_path)
