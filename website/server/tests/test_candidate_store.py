"""Lossless disk-backed candidate evidence; no retrieval or model calls."""

from copy import deepcopy
import gzip
import json
import tracemalloc

import pytest

from bayesian_auditing.benchmark_data import row_fingerprint, row_search_text
from website.server.candidate_store import CandidateStore, CandidateStoreError, has_ref


def candidate():
    row = {"item_id": "source-id", "content": "  Keep\nthis question with café text.  ",
           "nested": {"null": None, "list": [True, 4, 3.25, "literal \\n"]}}
    identity = row_fingerprint(row)
    return {"item_id": identity, "evidence_hash": identity,
            "evidence": {"item": row, "unknown_evidence_field": ["preserved"]},
            "search_text": row_search_text(row), "question_text": row["content"],
            "rank": 3, "sources": [{"benchmark": "fixture", "row": 9}],
            "unknown_metadata": {"keep": [None, True]}}


def test_round_trip_retains_every_field_and_metadata_variant_shares_evidence(tmp_path):
    store = CandidateStore(tmp_path / "review-runs" / "candidates")
    original = candidate()
    before = deepcopy(original)
    reference = store.put(original)
    assert original == before
    assert has_ref(reference)
    assert not {"evidence", "search_text", "question_text"} & reference.keys()
    assert store.resolve(reference) == original
    assert store.compact(reference) == reference
    assert CandidateStore(store.directory).expand(reference) == original
    screened = {**original, "rank": 7, "assessment": {"verdict": "pass"},
                "acquisition": {"facet_id": "task-2"}, "status": "complete"}
    screened_reference = store.compact(screened)
    assert screened_reference["_candidate_ref"] == reference["_candidate_ref"]
    assert store.expand(screened_reference) == screened
    assert len(list(store.directory.glob("*.json.gz"))) == 1
    assert store.directory.stat().st_mode & 0o777 == 0o700
    path = next(store.directory.glob("*.json.gz"))
    assert path.stat().st_mode & 0o777 == 0o600
    payload = json.loads(gzip.decompress(path.read_bytes()))
    assert set(payload) == {"evidence", "search_text", "question_text"}


def test_optional_fields_and_legacy_records_are_preserved(tmp_path):
    store = CandidateStore(tmp_path / "candidates")
    original = candidate()
    del original["question_text"]
    assert store.expand(original) is original
    assert store.expand(store.compact(original)) == original
    original["question_text"] = None
    assert store.expand(store.compact(original)) == original


@pytest.mark.parametrize("damage", ["missing", "truncated", "replaced", "wrong_identity"])
def test_corrupt_evidence_has_a_safe_error(tmp_path, damage):
    store = CandidateStore(tmp_path / "private-path")
    original = candidate()
    reference = store.compact(original)
    path = store.directory / f"{reference['_candidate_ref']}.json.gz"
    if damage == "missing":
        path.unlink()
    elif damage == "truncated":
        path.write_bytes(path.read_bytes()[:14])
    elif damage == "replaced":
        changed = {key: original[key] for key in ("evidence", "search_text", "question_text")}
        changed["question_text"] = "Unexpected replacement"
        path.write_bytes(gzip.compress(json.dumps(changed).encode()))
    else:
        reference["item_id"] = "other-row"
    with pytest.raises(CandidateStoreError) as failure:
        store.expand(reference)
    assert str(failure.value) == "Could not read candidate evidence."
    assert "private-path" not in str(failure.value)


@pytest.mark.parametrize("reference", ["../outside", "/private/file", "a" * 63, "A" * 64, None, {}])
def test_malformed_reference_cannot_choose_a_path(tmp_path, reference):
    store = CandidateStore(tmp_path / "candidates")
    record = {"_candidate_ref": reference}
    assert has_ref(record)
    with pytest.raises(CandidateStoreError, match="Could not read candidate evidence"):
        store.expand(record)
    with pytest.raises(CandidateStoreError, match="Could not save candidate evidence"):
        store.compact(record)
    assert not store.directory.exists()


def test_reference_cannot_override_large_fields_or_row_identity(tmp_path):
    store = CandidateStore(tmp_path / "candidates")
    original = candidate()
    reference = store.compact(original)
    reference["question_text"] = "Override original text"
    with pytest.raises(CandidateStoreError):
        store.expand(reference)
    with pytest.raises(CandidateStoreError):
        store.compact(reference)
    original["evidence_hash"] = "not-the-row-hash"
    with pytest.raises(CandidateStoreError):
        store.compact(original)


def test_failed_atomic_write_preserves_existing_evidence_and_cleans_temporary_file(tmp_path, monkeypatch):
    store = CandidateStore(tmp_path / "candidates")
    original = candidate()
    reference = store.compact(original)
    path = store.directory / f"{reference['_candidate_ref']}.json.gz"
    before = path.read_bytes()

    def fail_replace(source, destination):
        raise OSError("Private filesystem error")

    monkeypatch.setattr("website.server.candidate_store.os.replace", fail_replace)
    with pytest.raises(CandidateStoreError, match="Could not save candidate evidence"):
        store.compact(original)
    assert path.read_bytes() == before
    assert store.expand(reference) == original
    assert not list(store.directory.glob(".saving-*"))


def test_storing_many_large_candidates_does_not_retain_their_payloads(tmp_path):
    store = CandidateStore(tmp_path / "candidates")
    references = []
    tracemalloc.start()
    try:
        for number in range(12):
            record = candidate()
            row = record["evidence"]["item"]
            row["content"] = f"Question {number}: " + "x" * (384 * 1024)
            identity = row_fingerprint(row)
            record.update(item_id=identity, evidence_hash=identity,
                          search_text=row_search_text(row), question_text=row["content"])
            references.append(store.compact(record))
            del record, row
        retained, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert retained < 512 * 1024
    assert peak < 8 * 1024 * 1024
    for number, reference in enumerate(references):
        assert store.expand(reference)["evidence"]["item"]["content"].startswith(f"Question {number}: ")
