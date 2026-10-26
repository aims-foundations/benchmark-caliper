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


OFFLINE_ROWS = {}


@pytest.fixture(autouse=True)
def reset_offline_rows():
    OFFLINE_ROWS.clear()


def load_rows(requests, *, cancelled=None):
    return {request["item_id"]: deepcopy(OFFLINE_ROWS[request["item_id"]]) for request in requests}


def prepare(tmp_path, items, encoder=None, **kwargs):
    def capture(rows):
        try:
            for row in rows:
                original = row["evidence"]["item"]
                OFFLINE_ROWS[row_fingerprint(original)] = deepcopy(original)
                yield row
        finally:
            if hasattr(rows, "close"):
                rows.close()

    source = (lambda offset: capture(items(offset))) if callable(items) else capture(items)
    kwargs.setdefault("row_loader", load_rows)
    return prepare_benchmark_index(source, tmp_path, INVENTORY,
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


@pytest.mark.parametrize("fail_fetch", [False, True])
def test_search_timing_logs_locate_failures_without_private_data(tmp_path, caplog, fail_fetch):
    secret_query, secret_content = "private-query-123", "private-content-456"
    secret_source, secret_error = "private-source-789", "https://private.invalid/?token=secret"

    def fetch(requests, *, cancelled=None):
        if fail_fetch:
            raise RuntimeError(secret_error)
        return load_rows(requests, cancelled=cancelled)

    index = prepare(tmp_path, [item(secret_content, benchmark=secret_source)], row_loader=fetch)
    try:
        with caplog.at_level("INFO", logger=module.__name__):
            if fail_fetch:
                with pytest.raises(RuntimeError):
                    index.search(secret_query)
            else:
                assert len(index.search(secret_query)) == 1
    finally:
        index.close()

    assert "Benchmark dense search: seconds=" in caplog.text
    assert "Benchmark BM25 search: seconds=" in caplog.text
    assert "Benchmark search finished: seconds=" in caplog.text
    assert f"final_stage={'row_fetch' if fail_fetch else 'complete'}" in caplog.text
    if not fail_fetch:
        assert "Benchmark row fetch: seconds=" in caplog.text
        assert "requested_rows=1" in caplog.text
    for private in (secret_query, secret_content, secret_source, secret_error):
        assert private not in caplog.text


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
        assert [column[1] for column in connection.execute("PRAGMA table_info(items)")] == ["item_id", "row_digest"]
        assert connection.execute("SELECT search_text FROM search_fts").fetchall() == [(None,)]
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
        assert progress[-1] == {"stage": "indexing", "completed": 11, "total": 11, "cache_hits": 0}
        assert [row["item_id"] for row in index.search("query", dense_k=5, bm25_k=0)] == sorted(row["evidence_hash"] for row in rows)[:5]
        policy = index.policy
        assert policy["version"] == 3 and policy["embedding"]["truncation"] == "none"
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


def test_resume_loading_uses_only_committed_offset_and_retains_original_sources(tmp_path):
    rows = [item(f"row {i}", row=i + 1) for i in range(1030)]
    offsets, closed = [], []

    def source(offset):
        offsets.append(offset)
        try:
            yield from rows[offset:]
        finally:
            closed.append(offset)

    def interrupt(state):
        if state['stage'] == 'indexing' and state['completed'] == 1024:
            raise InterruptedError('fixture stop')

    with pytest.raises(InterruptedError):
        prepare(tmp_path, source, resume=True, progress=interrupt)
    checkpoint, = tmp_path.glob('*.building.sqlite3')
    with pytest.raises(ValueError, match='incomplete'):
        module.BenchmarkIndex(checkpoint, FakeEncoder())
    with sqlite3.connect(checkpoint) as connection:
        assert connection.execute('SELECT COUNT(*) FROM items').fetchone()[0] == 1024
    index = prepare(tmp_path, source, resume=True)
    try:
        assert offsets == closed == [0, 1024]
        assert index.stats['source_rows'] == index.stats['unique_documents'] == 1030
        assert index.stats['source_references'] == 1030
        assert not checkpoint.exists()
    finally:
        index.close()


def test_resume_loading_rolls_back_uncommitted_source_rows(tmp_path):
    rows = [item(f"row {i}", row=i + 1) for i in range(1030)]

    def broken(offset):
        yield from rows[offset:1027]
        raise RuntimeError('fixture source outage')

    with pytest.raises(RuntimeError, match='source outage'):
        prepare(tmp_path, broken, resume=True)
    offsets = []

    def source(offset):
        offsets.append(offset)
        return iter(rows[offset:])

    index = prepare(tmp_path, source, resume=True)
    try:
        assert offsets == [1024]
        assert index.stats['source_rows'] == index.stats['source_references'] == 1030
    finally:
        index.close()


def test_resume_streaming_skips_committed_rows_and_vectors(tmp_path, monkeypatch):
    monkeypatch.setattr(module, 'ENCODING_BATCH_SIZE', 2)
    rows = [item(f'row {i}') for i in range(5)]
    first = FakeEncoder()

    def interrupt(state):
        if state['stage'] == 'indexing' and state['completed'] == 2:
            raise InterruptedError('fixture stop')

    with pytest.raises(InterruptedError):
        prepare(tmp_path, rows, first, resume=True, progress=interrupt)
    assert first.calls == [[row_search_text(row['evidence']['item']) for row in rows[:2]]]

    offsets = []

    def remaining(offset):
        offsets.append(offset)
        return iter(rows[offset:])

    second = FakeEncoder()
    index = prepare(tmp_path, remaining, second, resume=True)
    try:
        assert offsets == [2]
        assert [text for batch in second.calls for text in batch] == [row_search_text(row['evidence']['item']) for row in rows[2:]]
        assert index.stats['embedded_documents'] == 5
        assert len(index.search('row')) == 5
    finally:
        index.close()


def test_resume_publishes_checkpoint_finalized_before_prior_process_exit(tmp_path):
    index = prepare(tmp_path, [item('one')], resume=True)
    complete = index.path
    index.close()
    checkpoint = complete.with_name(complete.stem + '.building.sqlite3')
    complete.replace(checkpoint)

    def forbidden(offset):
        pytest.fail('A finalized checkpoint must not be rebuilt')

    index = prepare(tmp_path, forbidden, resume=True)
    try:
        assert index.path == complete and not checkpoint.exists()
        assert index.stats['embedded_documents'] == 1
    finally:
        index.close()


def test_resume_rejects_checkpoint_identity_mismatch(tmp_path):
    def interrupt(state):
        raise InterruptedError('fixture stop')

    with pytest.raises(InterruptedError):
        prepare(tmp_path, [item('one')], resume=True, progress=interrupt)
    checkpoint, = tmp_path.glob('*.building.sqlite3')
    with sqlite3.connect(checkpoint) as connection:
        connection.execute("UPDATE metadata SET value = '\"wrong-key\"' WHERE key = 'cache_key'")
    with pytest.raises(ValueError, match='checkpoint identity'):
        prepare(tmp_path, [item('one')], resume=True)
    assert checkpoint.exists()


def test_build_lock_wait_is_cancellable_and_does_not_touch_checkpoint(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    import fcntl
    import os

    descriptor = os.open(tmp_path, os.O_RDONLY)
    fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    stopped = Event()
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            task = pool.submit(prepare, tmp_path, [item('one')], cancelled=stopped.is_set, resume=True)
            assert not stopped.wait(.15)
            assert not task.done()
            stopped.set()
            with pytest.raises(InterruptedError):
                task.result(timeout=2)
    finally:
        os.close(descriptor)
    assert list(tmp_path.iterdir()) == []


def test_disk_reserve_retains_checkpoint_and_allows_cached_reads(tmp_path, monkeypatch):
    from collections import namedtuple
    usage = namedtuple('usage', 'total used free')
    monkeypatch.setattr(module.shutil, 'disk_usage', lambda path: usage(100, 95, 5))
    with pytest.raises(OSError, match='reserve'):
        prepare(tmp_path, [item('one')], resume=True, minimum_free_bytes=10)
    assert len(list(tmp_path.glob('*.building.sqlite3'))) == 1
    monkeypatch.setattr(module.shutil, 'disk_usage', lambda path: usage(100, 80, 20))
    index = prepare(tmp_path, [item('one')], resume=True, minimum_free_bytes=10)
    index.close()
    monkeypatch.setattr(module.shutil, 'disk_usage', lambda path: usage(100, 95, 5))
    index = prepare(tmp_path, [], resume=True, minimum_free_bytes=10)
    try:
        assert index.stats['cache_hit'] is True
    finally:
        index.close()


def test_contentless_bm25_exactly_matches_external_content_reference(tmp_path):
    import re

    texts = [
        'needle needle CAFÉ Straße', 'needle café', 'other topic',
        'Blood\npressure is measured repeatedly. Pressure, pressure!',
        'Unicode Ελληνικά Straße naïve résumé', '',
        'context ' * 1200 + 'rareword café',
        'short needle', 'unrelated ' * 500,
    ]
    rows = [item(text, identifier=str(number), answer='grading\ncontext')
            for number, text in enumerate(texts)]
    index = prepare(tmp_path, rows)
    reference = sqlite3.connect(':memory:')
    reference.executescript("""
        CREATE TABLE items (item_id TEXT, search_text TEXT);
        CREATE VIRTUAL TABLE search_fts USING fts5(
            search_text, content='items', content_rowid='rowid',
            tokenize='unicode61 remove_diacritics 2'
        );
    """)
    for row in rows:
        text = row_search_text(row['evidence']['item'])
        cursor = reference.execute('INSERT INTO items VALUES (?, ?)', (row['evidence_hash'], text))
        reference.execute('INSERT INTO search_fts(rowid, search_text) VALUES (?, ?)', (cursor.lastrowid, text))
    try:
        for query in ('needle', 'needle cafe', 'Straße', 'pressure', 'Ελληνικά résumé',
                      'rareword context', '"needle" OR (absent)', 'grading', 'missing'):
            words = list(dict.fromkeys(re.findall(r'\b\w+\b', query)))
            expression = ' OR '.join('"' + word + '"' for word in words)
            expected = [(key, -score) for key, score in reference.execute(
                'SELECT i.item_id, bm25(search_fts) AS score FROM search_fts '
                'JOIN items i ON i.rowid = search_fts.rowid WHERE search_fts MATCH ? '
                'ORDER BY score ASC, i.item_id ASC LIMIT 600', (expression,))]
            assert index._keyword(query, 600) == expected
    finally:
        index.close()
        reference.close()


def test_contentless_storage_does_not_keep_original_rows_or_rendered_copies(tmp_path):
    from bayesian_auditing.benchmark_data import row_text

    row = item('A complete distinctive sentence: not stored as a raw row!\nSecond line.',
               answer='Reference answer with punctuation; and literal spacing.  ', arbitrary=[None, 1, True])
    index = prepare(tmp_path, [row])
    path = index.path
    try:
        with sqlite3.connect(path) as connection:
            assert [column[1] for column in connection.execute('PRAGMA table_info(items)')] == ['item_id', 'row_digest']
            digest, = connection.execute('SELECT row_digest FROM items').fetchone()
            assert isinstance(digest, bytes) and len(digest) == 64
            assert connection.execute('SELECT search_text FROM search_fts').fetchall() == [(None,)]
            assert not connection.execute("SELECT name FROM sqlite_master WHERE name = 'search_fts_content'").fetchall()
            # Token counts and positions remain available to the same BM25 formula.
            assert connection.execute('SELECT COUNT(*) FROM search_fts_docsize').fetchone()[0] == 1
        raw = path.read_bytes()
        assert row_text(row['evidence']['item']).encode() not in raw
        assert row_search_text(row['evidence']['item']).encode() not in raw
        assert row['evidence']['item']['content'].encode() not in raw
        assert index.search('distinctive', dense_k=0)[0]['evidence'] == row['evidence']
    finally:
        index.close()


def test_streaming_embeds_before_exhausting_source_and_commits_all_artifacts_together(tmp_path, monkeypatch):
    monkeypatch.setattr(module, 'ENCODING_BATCH_SIZE', 2)
    rows = [item(f'row {i}', row=i + 1) for i in range(5)]
    encoder = FakeEncoder()
    observed = []

    def source(offset):
        for number, row in enumerate(rows[offset:], offset):
            if number == 2:
                assert len(encoder.calls) == 1
            yield row

    def inspect(state):
        if state['completed'] == 2:
            checkpoint, = tmp_path.glob('*.building.sqlite3')
            with sqlite3.connect(checkpoint) as connection:
                counts = [connection.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                          for table in ('items', 'sources', 'vectors', 'search_fts')]
                observed.append(counts)

    index = prepare(tmp_path, source, encoder, resume=True, progress=inspect)
    try:
        assert observed == [[2, 2, 2, 2]]
        assert [len(batch) for batch in encoder.calls] == [2, 2, 1]
        assert index.stats['source_rows'] == index.stats['embedded_documents'] == 5
    finally:
        index.close()


def test_failed_embedding_rolls_back_identity_postings_sources_and_offset(tmp_path, monkeypatch):
    import json

    monkeypatch.setattr(module, 'ENCODING_BATCH_SIZE', 2)
    rows = [item(f'row {i}', row=i + 1) for i in range(5)]

    class FailingEncoder(FakeEncoder):
        def encode(self, texts):
            if self.calls:
                raise RuntimeError('fixture embedding failure')
            return super().encode(texts)

    with pytest.raises(RuntimeError, match='embedding failure'):
        prepare(tmp_path, rows, FailingEncoder(), resume=True)
    checkpoint, = tmp_path.glob('*.building.sqlite3')
    with sqlite3.connect(checkpoint) as connection:
        for table in ('items', 'sources', 'vectors', 'search_fts'):
            assert connection.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0] == 2
        state = json.loads(connection.execute("SELECT value FROM metadata WHERE key = 'build_state'").fetchone()[0])
        assert state['source_rows'] == state['stats']['embedded_documents'] == 2
    offsets = []

    def source(offset):
        offsets.append(offset)
        return iter(rows[offset:])

    encoder = FakeEncoder()
    index = prepare(tmp_path, source, encoder, resume=True)
    try:
        assert offsets == [2]
        assert sum(map(len, encoder.calls)) == 3
        assert index.stats['source_rows'] == index.stats['embedded_documents'] == 5
    finally:
        index.close()


def test_duplicates_across_committed_batches_add_sources_without_reembedding(tmp_path, monkeypatch):
    monkeypatch.setattr(module, 'ENCODING_BATCH_SIZE', 2)
    a, b, c = item('first', row=1), item('second', row=2), item('third', row=4)
    duplicate = item('first', benchmark='another', row=3)
    encoder = FakeEncoder()
    index = prepare(tmp_path, [a, b, duplicate, c], encoder)
    try:
        assert [len(batch) for batch in encoder.calls] == [2, 1]
        assert index.stats['source_rows'] == index.stats['source_references'] == 4
        assert index.stats['embedded_documents'] == 3
        match, = index.search('first', dense_k=0)
        assert {source['benchmark'] for source in match['sources']} == {'medicine', 'another'}
    finally:
        index.close()


def test_hydration_fetches_only_final_union_once_and_preserves_complete_contract(tmp_path):
    rows = [item('semantic answer', identifier='semantic'), item('keyword answer', identifier='lexical'),
            item('neither', identifier='excluded')]
    encoder = FakeEncoder({row_search_text(row['evidence']['item']): vector
                           for row, vector in zip(rows, ([1, 0], [-1, 0], [0, 1]))})
    encoder.vectors[QUERY_INSTRUCTION + 'keyword'] = [1, 0]
    calls = []

    def loader(requests, *, cancelled=None):
        calls.append(deepcopy(requests))
        result = load_rows(requests)
        # Resolver inputs cannot mutate returned provenance.
        requests[0]['sources'].clear()
        return result

    index = prepare(tmp_path, rows, encoder, row_loader=loader)
    try:
        matches = index.search('keyword', dense_k=1, bm25_k=1)
        selected = {rows[0]['evidence_hash'], rows[1]['evidence_hash']}
        assert len(calls) == 1 and {request['item_id'] for request in calls[0]} == selected
        assert all(set(request) == {'item_id', 'sources'} and request['sources'] for request in calls[0])
        assert {match['item_id'] for match in matches} == selected
        for match in matches:
            assert match['sources']
            original = OFFLINE_ROWS[match['item_id']]
            assert match['evidence'] == {'item': original}
            assert match['search_text'] == row_search_text(original)
            assert set(match) == {'item_id', 'evidence_hash', 'dense_rank', 'bm25_rank', 'dense_score',
                                  'bm25_score', 'rrf_score', 'rank', 'sources', 'evidence', 'search_text', 'question_text'}
        assert index.search('absent', dense_k=0) == []
        assert len(calls) == 1
    finally:
        index.close()


@pytest.mark.parametrize('mode', ['missing', 'extra', 'changed', 'digest'])
def test_hydration_rejects_missing_extra_or_mismatched_rows(tmp_path, mode):
    record = item('original')

    def loader(requests, *, cancelled=None):
        rows = load_rows(requests)
        if mode == 'missing':
            return {}
        if mode == 'extra':
            rows['unexpected'] = {'content': 'unrelated'}
        if mode == 'changed':
            rows[record['evidence_hash']]['content'] = 'changed'
        return rows

    index = prepare(tmp_path, [record], row_loader=loader)
    try:
        if mode == 'digest':
            with sqlite3.connect(index.path) as connection:
                connection.execute('UPDATE items SET row_digest = ?', (b'wrong digest',))
        with pytest.raises(ValueError, match='shortlisted|indexed identity'):
            index.search('original')
    finally:
        index.close()


def test_hydration_cancellation_never_returns_partial_candidates(tmp_path):
    stopped = False

    def loader(requests, *, cancelled=None):
        nonlocal stopped
        assert cancelled is not None
        stopped = True
        return load_rows(requests)

    index = prepare(tmp_path, [item('first'), item('second')], row_loader=loader)
    try:
        with pytest.raises(InterruptedError, match='cancelled'):
            index.search('first', cancelled=lambda: stopped)
    finally:
        index.close()


def test_default_hydrator_uses_saved_pinned_inventory_only_when_needed(tmp_path, monkeypatch):
    from bayesian_auditing import benchmark_rows

    record = item('needle')
    calls = []

    def fetch(inventory, requests, *, cancelled=None):
        calls.append((deepcopy(inventory), deepcopy(requests)))
        return {record['evidence_hash']: deepcopy(record['evidence']['item'])}

    monkeypatch.setattr(benchmark_rows, 'fetch_benchmark_rows', fetch)
    index = prepare_benchmark_index([record], tmp_path, INVENTORY, FakeEncoder())
    try:
        assert calls == []
        assert index.search('absent', dense_k=0) == []
        assert calls == []
        match, = index.search('needle', dense_k=0)
        assert match['evidence'] == record['evidence']
        assert calls == [(INVENTORY, [{'item_id': record['evidence_hash'], 'sources': [record['source']]}])]
    finally:
        index.close()


class ParallelFakeEncoder(FakeEncoder):
    max_parallel_batches = 3

    def __init__(self, vectors=None):
        super().__init__(vectors)
        self.windows = []

    def encode_batches(self, batches, *, cancelled=None):
        self.windows.append(deepcopy(batches))
        return [self.encode(batch) for batch in batches]


def test_parallel_build_matches_serial_batches_rows_sources_vectors_and_search(tmp_path):
    rows = [item(f'needle row {i}', row=i + 1) for i in range(1100)]
    # Repeats cross both batch and transaction boundaries. Every source stays.
    for position in range(10, 1100, 17):
        rows.insert(position, item('needle row 0', benchmark='another', row=position + 1))
    vectors = {row_search_text(row['evidence']['item']): [number + 1, 1]
               for number, row in enumerate(rows)}
    original = deepcopy(rows)
    serial_encoder, parallel_encoder = FakeEncoder(vectors), ParallelFakeEncoder(vectors)
    serial = prepare(tmp_path / 'serial', rows, serial_encoder, resume=True)
    parallel = prepare(tmp_path / 'parallel', rows, parallel_encoder, resume=True)
    try:
        assert rows == original
        assert serial.policy == parallel.policy and serial.stats == parallel.stats
        assert serial.path.name == parallel.path.name
        assert serial_encoder.calls == parallel_encoder.calls
        assert max(map(len, parallel_encoder.windows)) == 3
        for table, order in [('items', 'rowid'), ('vectors', 'item_id'),
                             ('sources', 'item_id, source_hash'), ('search_fts_docsize', 'id')]:
            assert serial._connection.execute(f'SELECT * FROM {table} ORDER BY {order}').fetchall() == \
                parallel._connection.execute(f'SELECT * FROM {table} ORDER BY {order}').fetchall()
        assert serial.search('needle row 14', dense_k=12, bm25_k=12) == \
            parallel.search('needle row 14', dense_k=12, bm25_k=12)
    finally:
        serial.close()
        parallel.close()


@pytest.mark.parametrize('failure', ['worker', 'invalid_vector', 'missing_batch', 'cancel', 'source'])
def test_parallel_failure_rolls_back_whole_window_and_resumes(tmp_path, monkeypatch, failure):
    import json

    monkeypatch.setattr(module, 'ENCODING_BATCH_SIZE', 2)
    rows = [item(f'row {i}', row=i + 1) for i in range(13)]
    stopped = False

    class FailingParallel(ParallelFakeEncoder):
        def encode_batches(self, batches, *, cancelled=None):
            nonlocal stopped
            values = super().encode_batches(batches, cancelled=cancelled)
            if len(self.windows) == 2:
                if failure == 'worker':
                    raise RuntimeError('worker failed after another worker finished')
                if failure == 'invalid_vector':
                    values[-1][:] = np.nan
                if failure == 'missing_batch':
                    values.pop()
                if failure == 'cancel':
                    stopped = True
            return values

    def source(offset):
        for number, row in enumerate(rows[offset:], offset):
            if failure == 'source' and number == 9:
                raise RuntimeError('source failed within a parallel window')
            yield row

    with pytest.raises((RuntimeError, ValueError, InterruptedError)):
        prepare(tmp_path, source, FailingParallel(), resume=True, cancelled=lambda: stopped)
    checkpoint, = tmp_path.glob('*.building.sqlite3')
    assert list(tmp_path.glob('*.sqlite3')) == [checkpoint]
    with sqlite3.connect(checkpoint) as connection:
        for table in ('items', 'vectors', 'sources', 'search_fts'):
            assert connection.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0] == 6
        state = json.loads(connection.execute("SELECT value FROM metadata WHERE key='build_state'").fetchone()[0])
        assert state['source_rows'] == state['stats']['embedded_documents'] == 6
        assert not connection.execute("SELECT value FROM metadata WHERE key='complete'").fetchone()
    offsets = []

    def resume(offset):
        offsets.append(offset)
        return iter(rows[offset:])

    encoder = FakeEncoder()
    index = prepare(tmp_path, resume, encoder, resume=True)
    try:
        assert offsets == [6]
        assert sum(map(len, encoder.calls)) == 7
        assert index.stats['source_rows'] == index.stats['embedded_documents'] == 13
        assert {match['item_id'] for match in index.search('row')} == {row['evidence_hash'] for row in rows}
    finally:
        index.close()


def test_parallel_resume_reuses_single_worker_checkpoint(tmp_path, monkeypatch):
    monkeypatch.setattr(module, 'ENCODING_BATCH_SIZE', 2)
    rows = [item(f'row {i}', row=i + 1) for i in range(9)]

    def stop(state):
        if state['completed'] == 2:
            raise InterruptedError('switch hardware after checkpoint')

    with pytest.raises(InterruptedError):
        prepare(tmp_path, rows, FakeEncoder(), resume=True, progress=stop)
    offsets = []

    def source(offset):
        offsets.append(offset)
        return iter(rows[offset:])

    encoder = ParallelFakeEncoder()
    index = prepare(tmp_path, source, encoder, resume=True)
    try:
        assert offsets == [2]
        assert [text for batch in encoder.calls for text in batch] == [
            row_search_text(row['evidence']['item']) for row in rows[2:]]
        assert index.stats['source_rows'] == index.stats['embedded_documents'] == 9
    finally:
        index.close()
