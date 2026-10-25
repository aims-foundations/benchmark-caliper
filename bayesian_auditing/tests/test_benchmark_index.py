"""Offline tests for full-row retrieval, exact row identity, and disk caching."""

from copy import deepcopy
import sqlite3
import stat

import numpy as np
import pytest

from bayesian_auditing import benchmark_index as module
from bayesian_auditing.benchmark_data import row_fingerprint, row_search_text
from bayesian_auditing.benchmark_index import prepare_benchmark_index
from bayesian_auditing.onet import QUERY_INSTRUCTION


INVENTORY = {"repo": "test/benchmark", "branches": {"main": "fixed-commit"},
             "tables": [{"branch": "main", "commit": "fixed-commit", "benchmark": "medicine",
                         "items_path": "medicine/items.parquet"}]}


def item(content, *, identifier="original-id", benchmark="medicine", branch="main", answer=None, row=1, **extra):
    original = {"item_id": identifier, "content": content, "grading_criterion": answer, **extra}
    return {"evidence": {"item": original}, "evidence_hash": row_fingerprint(original),
            "source": {"benchmark": benchmark, "branch": branch, "row": row}}


class FakeEncoder:
    dimensions = 2
    cache_namespace = "benchmark-fullrow-tests-v1"

    def __init__(self, vectors=None):
        self.vectors = vectors or {}
        self.calls = []

    def encode(self, texts):
        self.calls.append(list(texts))
        return np.asarray([self.vectors.get(text, [3, 4]) for text in texts], dtype=np.float32)


def prepare(tmp_path, items, encoder=None, **kwargs):
    return prepare_benchmark_index(items, tmp_path, INVENTORY,
                                   encoder=encoder if encoder is not None else FakeEncoder(), **kwargs)


def test_dense_normalization_and_full_union_of_independent_rankings(tmp_path):
    semantic, lexical, other = item("semantic"), item("needle"), item("unrelated")
    encoder = FakeEncoder({row_search_text(record["evidence"]["item"]): vector for record, vector in
                           ((semantic, [10, 0]), (lexical, [-10, 0]), (other, [0, 1]))})
    encoder.vectors[QUERY_INSTRUCTION + "needle"] = [1, 0]
    index = prepare(tmp_path, [lexical, other, semantic], encoder)
    try:
        matches = index.search("needle", dense_k=1, bm25_k=1)
        assert [row["item_id"] for row in matches] == sorted([semantic["evidence_hash"], lexical["evidence_hash"]])
        dense = next(row for row in matches if row["dense_rank"] is not None)
        keyword = next(row for row in matches if row["bm25_rank"] is not None)
        assert dense["item_id"] == semantic["evidence_hash"] and dense["dense_score"] == pytest.approx(1)
        assert keyword["item_id"] == lexical["evidence_hash"]
        assert all(row["rrf_score"] == 1 / 61 for row in matches)
        assert [row["rank"] for row in matches] == [1, 2]
        assert encoder.calls[-1] == [QUERY_INSTRUCTION + "needle"]
        assert index.policy["candidate_limits"] == {"dense_k": 1, "bm25_k": 1}
    finally:
        index.close()


def test_entire_original_row_is_embedded_and_keyword_searchable(tmp_path):
    original = item({"question": "visible", "answer": "nestedanswer"}, identifier="uniqueidentifier",
                    answer="gradingsecret", verifier="verifiersecret", reference_answer="referencesecret",
                    asset_manifest={"url": "assetsecret"}, arbitrary_new_column="extracolumnsecret")
    original["evidence"]["benchmark"] = {"description": "externalmetadata"}
    original["source"]["branch"] = "sourcebranchsecret"
    encoder = FakeEncoder()
    index = prepare(tmp_path, [original], encoder)
    try:
        assert encoder.calls == [[row_search_text(original["evidence"]["item"])]]
        for query in ("uniqueidentifier", "gradingsecret", "nestedanswer", "verifiersecret",
                      "referencesecret", "assetsecret", "arbitrary_new_column", "extracolumnsecret"):
            results = index.search(query, dense_k=0)
            assert len(results) == 1
            assert results[0]["search_text"] == row_search_text(original["evidence"]["item"])
            assert results[0]["evidence"] == {"item": original["evidence"]["item"]}
        for excluded in ("externalmetadata", "sourcebranchsecret"):
            assert index.search(excluded, dense_k=0) == []
    finally:
        index.close()


def test_default_union_keeps_up_to_1200_rows(tmp_path):
    rows = [item(f"semantic {i}") for i in range(610)] + [item(f"needle {i}") for i in range(610)]
    encoder = FakeEncoder({row_search_text(row["evidence"]["item"]):
                           [1, 0] if row["evidence"]["item"]["content"].startswith("semantic") else [-1, 0]
                           for row in rows})
    encoder.vectors[QUERY_INSTRUCTION + "needle"] = [1, 0]
    index = prepare(tmp_path, rows, encoder)
    try:
        matches = index.search("needle")
        assert len(matches) == len({row["item_id"] for row in matches}) == 1200
        assert sum(row["dense_rank"] is not None for row in matches) == 600
        assert sum(row["bm25_rank"] is not None for row in matches) == 600
    finally:
        index.close()


def test_overlap_fuses_ranks_and_stable_row_ids_break_ties(tmp_path):
    rows = [item("needle"), item("another example")]
    index = prepare(tmp_path, rows)
    try:
        results = index.search("needle", dense_k=2, bm25_k=2)
        assert results[0]["item_id"] == rows[0]["evidence_hash"]
        assert results[0]["rrf_score"] == pytest.approx(1 / 61 + 1 / (60 + results[0]["dense_rank"]))
        assert results[1]["bm25_rank"] is None
        assert [row["item_id"] for row in index.search("unmatched", dense_k=2, bm25_k=0)] == sorted(row["evidence_hash"] for row in rows)
    finally:
        index.close()


def test_exact_full_rows_deduplicate_across_sources_but_differing_fields_do_not(tmp_path):
    first = item("same question", answer="answer")
    duplicate = item("same question", benchmark="other", branch="migration", answer="answer")
    duplicate["evidence"]["benchmark"] = {"description": "ignored outer context"}
    other_answer = item("same question", answer="other answer")
    other_id = item("same question", answer="answer", identifier="different-id")
    encoder = FakeEncoder()
    index = prepare(tmp_path, [first, duplicate, first, other_answer, other_id], encoder)
    try:
        assert len(encoder.calls[0]) == 3
        assert index.stats == {"source_rows": 5, "total_items": 3, "indexed_items": 3,
                               "contentless_items": 0, "source_references": 4,
                               "unique_documents": 3, "embedded_documents": 3, "cache_hit": False}
        results = index.search("question", dense_k=0)
        shared = next(row for row in results if row["item_id"] == first["evidence_hash"])
        assert {source["benchmark"] for source in shared["sources"]} == {"medicine", "other"}
        assert shared["evidence"] == first["evidence"]
    finally:
        index.close()


def test_raw_json_strings_are_never_decoded_or_collapsed_for_identity(tmp_path):
    first = item('{"question":"same"}')
    second = item('{ "question": "same" }')
    structured = item({"question": "same"})
    index = prepare(tmp_path, [first, second, structured])
    try:
        results = index.search("same")
        assert len(results) == 3
        assert len({row["item_id"] for row in results}) == 3
        assert {row["search_text"] for row in results} == {row_search_text(row["evidence"]["item"]) for row in (first, second, structured)}
        assert next(row for row in results if row["item_id"] == first["evidence_hash"])["evidence"]["item"]["content"] == '{"question":"same"}'
    finally:
        index.close()


def test_rows_without_question_content_still_search_ids_and_other_fields(tmp_path):
    rows = [item(None, identifier="findnull", answer="nullanswer"), item(" ", identifier="findblank")]
    encoder = FakeEncoder()
    index = prepare(tmp_path, rows, encoder)
    try:
        assert index.stats["indexed_items"] == 2 and index.stats["contentless_items"] == 0
        assert len(encoder.calls[0]) == 2
        assert len(index.search("nullanswer", dense_k=0)) == 1
        assert len(index.search("findblank", dense_k=0)) == 1
    finally:
        index.close()


def test_fts_syntax_is_literal_and_unicode_normalization_is_consistent(tmp_path):
    index = prepare(tmp_path, [item("needle Straße café"), item("unrelated")])
    try:
        for query in ('"needle" OR (missing)', 'needle NOT missing', "needle'; DROP TABLE items; --",
                      "Straße", "straße", "CAFÉ", "cafe"):
            assert len(index.search(query, dense_k=0)) == 1
        assert index.search('" * : ()', dense_k=0) == []
    finally:
        index.close()


def test_cache_hit_never_consumes_source_and_queries_are_not_saved(tmp_path):
    record = item("document")
    index = prepare(tmp_path, [record])
    path = index.path
    index.close()

    def forbidden():
        raise AssertionError("Cache hit consumed source iterator")
        yield

    encoder = FakeEncoder()
    index = prepare(tmp_path, forbidden(), encoder)
    try:
        assert index.stats["cache_hit"] is True and encoder.calls == []
        index.search("private query")
        index.search("private query")
        assert encoder.calls == [[QUERY_INSTRUCTION + "private query"], [QUERY_INSTRUCTION + "private query"]]
    finally:
        index.close()
    with sqlite3.connect(path) as connection:
        assert connection.execute("SELECT search_text FROM items").fetchall() == [(row_search_text(record["evidence"]["item"]),)]
        assert connection.execute("SELECT COUNT(*) FROM vectors").fetchone()[0] == 1
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    assert stat.S_IMODE(tmp_path.stat().st_mode) == 0o700


@pytest.mark.parametrize("change", ["commit", "scope", "loader", "policy", "encoder"])
def test_cache_invalidates_when_corpus_or_encoding_changes(tmp_path, monkeypatch, change):
    first = prepare(tmp_path, [item("original")])
    first_path = first.path
    first.close()
    inventory, encoder = deepcopy(INVENTORY), FakeEncoder()
    if change == "commit":
        inventory["tables"][0]["commit"] = "newcommit"
    elif change == "scope":
        inventory["tables"].append({**inventory["tables"][0], "benchmark": "additional"})
    elif change == "loader":
        monkeypatch.setattr(module, "BENCHMARK_DATA_VERSION", 999)
    elif change == "policy":
        monkeypatch.setattr(module, "INDEX_VERSION", 999)
    else:
        encoder.cache_namespace = "newencoder"
    second = prepare_benchmark_index([item("new")], tmp_path, inventory, encoder=encoder)
    try:
        assert second.path != first_path and second.stats["cache_hit"] is False
        assert encoder.calls == [[row_search_text(item("new")["evidence"]["item"])]]
    finally:
        second.close()


def test_cancellation_and_source_failure_never_publish_partial_cache(tmp_path):
    stopped = False

    def rows():
        nonlocal stopped
        yield item("first")
        stopped = True
        yield item("second")

    with pytest.raises(InterruptedError, match="cancelled"):
        prepare(tmp_path, rows(), cancelled=lambda: stopped)
    assert list(tmp_path.iterdir()) == []

    def broken():
        yield item("first")
        raise RuntimeError("source unavailable")

    with pytest.raises(RuntimeError, match="source unavailable"):
        prepare(tmp_path, broken())
    assert list(tmp_path.iterdir()) == []


def test_embedding_and_search_cancellation_preserve_completed_cache(tmp_path):
    stopped = False

    class CancellingEncoder(FakeEncoder):
        def encode(self, texts):
            nonlocal stopped
            stopped = True
            return super().encode(texts)

    with pytest.raises(InterruptedError):
        prepare(tmp_path, [item("first")], CancellingEncoder(), cancelled=lambda: stopped)
    assert list(tmp_path.iterdir()) == []
    index = prepare(tmp_path, [item("first")])
    try:
        with pytest.raises(InterruptedError):
            index.search("query", cancelled=lambda: True)
        assert len(index.search("query")) == 1
    finally:
        index.close()


def test_supplied_hash_must_match_original_row_and_sources_are_required(tmp_path):
    record = item("question")
    record["evidence_hash"] = "forgedhash"
    with pytest.raises(ValueError, match="must match"):
        prepare(tmp_path, [record])
    for source in (None, {}, {"benchmark": ""}, {"benchmark": 3}):
        record = item("question")
        record["source"] = source
        with pytest.raises(ValueError, match="benchmark identifier"):
            prepare(tmp_path, [record])
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("vectors", [[[0, 0]], [[np.nan, 1]], [[np.inf, 1]], [[1, 2, 3]]])
def test_invalid_vectors_fail_without_publishing(tmp_path, vectors):
    class BadEncoder(FakeEncoder):
        def encode(self, texts):
            return vectors
    with pytest.raises(ValueError):
        prepare(tmp_path, [item("question")], BadEncoder())
    assert list(tmp_path.iterdir()) == []


def test_build_and_scan_batches_are_bounded_and_policy_is_a_snapshot(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "ENCODING_BATCH_SIZE", 3)
    monkeypatch.setattr(module, "SCAN_BATCH_SIZE", 2)
    rows = [item(f"text {number}") for number in range(11)]
    encoder, progress = FakeEncoder(), []
    index = prepare(tmp_path, iter(rows), encoder, progress=progress.append)
    try:
        assert [len(batch) for batch in encoder.calls] == [3, 3, 3, 2]
        assert progress[-1] == {"stage": "embedding", "completed": 11, "total": 11, "cache_hits": 0}
        assert [row["item_id"] for row in index.search("query", dense_k=5, bm25_k=0)] == sorted(row["evidence_hash"] for row in rows)[:5]
        policy = index.policy
        assert policy["version"] == 2 and policy["embedding"]["truncation"] == "none"
        policy["embedding"]["model"] = "changed"
        assert index.policy["embedding"]["model"] == "custom"
    finally:
        index.close()


@pytest.mark.parametrize("kwargs", [{"dense_k": -1}, {"bm25_k": True}, {"dense_k": 1.2}, {"dense_k": 0, "bm25_k": 0}])
def test_invalid_search_limits(tmp_path, kwargs):
    index = prepare(tmp_path, [item("question")])
    try:
        with pytest.raises(ValueError):
            index.search("query", **kwargs)
    finally:
        index.close()


@pytest.mark.parametrize("query", ["", " ", None, 5])
def test_invalid_query(tmp_path, query):
    index = prepare(tmp_path, [item("question")])
    try:
        with pytest.raises(ValueError, match="nonempty"):
            index.search(query)
    finally:
        index.close()


def test_inventory_is_pinned_and_row_counts_are_complete(tmp_path):
    for inventory in (None, {}, {"tables": []}, {"tables": [{"benchmark": "unversioned"}]}):
        with pytest.raises(ValueError):
            prepare_benchmark_index([], tmp_path, inventory, encoder=FakeEncoder())
    inventory = deepcopy(INVENTORY)
    inventory["tables"][0]["row_count"] = 2
    with pytest.raises(ValueError, match="row count differs"):
        prepare_benchmark_index([item("partial")], tmp_path, inventory, encoder=FakeEncoder())
    assert list(tmp_path.iterdir()) == []


def test_bm25_preserves_multiline_words_across_content_and_grading_fields(tmp_path):
    original = item("Blood\npressure", answer="systolic\tthreshold", verifier={"note": "check\nmeasurement"})
    encoder = FakeEncoder()
    index = prepare(tmp_path, [original], encoder)
    try:
        for word in ("Blood", "pressure", "systolic", "threshold", "check", "measurement"):
            results = index.search(word, dense_k=0)
            assert len(results) == 1
            assert results[0]["evidence"]["item"] == original["evidence"]["item"]
        assert "Blood\npressure" in encoder.calls[0][0]
        assert "systolic\tthreshold" in encoder.calls[0][0]
        assert index.search("npressure", dense_k=0) == []
    finally:
        index.close()


def test_identical_search_text_cannot_collapse_distinct_original_row_types(tmp_path):
    rows = [item(None), item("null")]
    index = prepare(tmp_path, rows)
    try:
        assert index.stats["total_items"] == 2
        matches = index.search("null")
        assert {row["item_id"] for row in matches} == {row["evidence_hash"] for row in rows}
        assert {type(row["evidence"]["item"]["content"]) for row in matches} == {type(None), str}
    finally:
        index.close()


def test_row_hash_collision_checks_original_evidence_not_search_text(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "row_fingerprint", lambda row: "forcedcollision")
    monkeypatch.setattr(module, "row_search_text", lambda row: "same searchable text")
    rows = [item(None), item("null")]
    for row in rows:
        row.pop("evidence_hash")
    with pytest.raises(ValueError, match="Conflicting original rows"):
        prepare(tmp_path, rows)
    assert list(tmp_path.iterdir()) == []
