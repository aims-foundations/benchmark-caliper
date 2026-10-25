import csv
import hashlib

import numpy as np
import pytest

from bayesian_auditing.onet import (
    CSV_FIELDS, DEFAULT_MATERIALS_DIR, MODEL_ID, MODEL_REVISION, OnetIndex,
    QUERY_INSTRUCTION, RRF_K,
)


RECORDS = [
    {"doc_id": "z", "kind": "activity", "name": "Treatment", "text": "Evaluate treatment risks.", "occupation_id": ""},
    {"doc_id": "b", "kind": "activity_edge", "name": "Diagnosis", "text": "Diagnose illnesses using clinical evidence.", "occupation_id": "29-0000.00"},
    {"doc_id": "a", "kind": "skill", "name": "Listening", "text": "Listen carefully to patient concerns.", "occupation_id": ""},
    {"doc_id": "d", "kind": "knowledge", "name": "Computing", "text": "Program computers and software.", "occupation_id": ""},
]
VECTORS = np.asarray([[1, 0], [0.8, 0.6], [0.8, 0.6], [0, 1]], dtype=np.float32)


def write_materials(directory, *, records=None, vectors=None, ids=None):
    records = RECORDS if records is None else records
    with (directory / "ONET_index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(records)
    np.savez(directory / "ONET_embeddings.npz", vectors=VECTORS if vectors is None else vectors,
             doc_ids=np.asarray([record["doc_id"] for record in records]) if ids is None else ids)


class FakeEncoder:
    def __init__(self):
        self.calls = []
        self.values = {record["text"]: vector for record, vector in zip(RECORDS, VECTORS)}
        self.query_vector = [1, 0]

    def encode(self, texts):
        self.calls.append(list(texts))
        return np.asarray([self.values.get(text, self.query_vector) for text in texts], dtype=np.float32)


@pytest.fixture
def index(tmp_path):
    write_materials(tmp_path)
    return OnetIndex(tmp_path, encoder=FakeEncoder())


def test_dense_bm25_fusion_preserves_records_and_supporting_text(index):
    candidates = index.search("treatment", dense_k=2, bm25_k=2, limit=2)
    assert [candidate["doc_id"] for candidate in candidates] == ["z", "a"]
    assert {key: candidates[0][key] for key in CSV_FIELDS} == RECORDS[0]
    assert candidates[0]["dense_rank"] == candidates[0]["bm25_rank"] == 1
    assert candidates[0]["rrf_score"] == pytest.approx(2 / (RRF_K + 1))
    assert candidates[1]["dense_rank"] == 2
    assert candidates[1]["bm25_rank"] is None
    assert candidates[1]["rrf_score"] == pytest.approx(1 / (RRF_K + 2))
    assert len({candidate["doc_id"] for candidate in candidates}) == len(candidates)


def test_compatibility_checks_documents_without_prefix_then_prefixes_queries(index):
    index.search("first query")
    index.search("second query")
    assert index._encoder.calls == [
        [record["text"] for record in RECORDS],
        [QUERY_INSTRUCTION + "first query"], [QUERY_INSTRUCTION + "second query"],
    ]
    check = index.policy["embedding"]["compatibility"]
    assert check["status"] == "passed"
    assert check["sample_record_ids"] == ["z", "b", "a", "d"]
    assert check["minimum_cosine"] >= check["required_minimum_cosine"]


def test_equal_dense_scores_use_id_order_and_return_bounded_shortlist(index):
    results = index.search("query", bm25_k=0, limit=3)
    assert [candidate["doc_id"] for candidate in results] == ["z", "a", "b"]
    assert [candidate["dense_rank"] for candidate in results] == [1, 2, 3]


def test_bm25_casefolds_and_excludes_unmatched_records_without_loading_encoder(index):
    results = index.search("TREATMENT!", dense_k=0)
    assert [candidate["doc_id"] for candidate in results] == ["z"]
    assert results[0]["dense_rank"] is None
    assert index.search("nonexistent", dense_k=0) == []
    assert index.search("?!", dense_k=0) == []
    assert index._encoder.calls == []
    assert index.policy["embedding"]["compatibility"]["status"] == "not_checked"


def test_ranking_and_policy_cannot_be_modified_through_returned_objects(index):
    result = index.search("treatment", dense_k=3, bm25_k=4, limit=2)
    result[0]["text"] = "changed"
    policy = index.policy
    assert policy["candidate_limits"] == {"dense_k": 3, "bm25_k": 4, "limit": 2}
    policy["embedding"]["model"] = "changed"
    assert index.search("treatment")[0]["text"] == RECORDS[0]["text"]
    assert index.policy["embedding"]["model"] == "custom"


def test_policy_includes_dataset_identity_and_documented_encoder_settings(tmp_path):
    write_materials(tmp_path)
    index = OnetIndex(tmp_path)
    policy = index.policy
    assert index._encoder._model is None
    assert policy["record_count"] == 4
    assert "healthcare" in policy["scope"]
    assert policy["embedding"]["model"] == MODEL_ID
    assert policy["embedding"]["revision"] == MODEL_REVISION
    assert policy["embedding"]["max_tokens"] == 512
    assert policy["embedding"]["pooling"] == "cls"
    assert policy["fusion"]["k"] == 60
    assert policy["files"]["ONET_index.csv"]["sha256"] == hashlib.sha256((tmp_path / "ONET_index.csv").read_bytes()).hexdigest()


@pytest.mark.parametrize("changes,match", [
    ({"ids": np.array(["b", "z", "a", "d"])}, "same order"),
    ({"ids": np.array([["z", "b", "a", "d"]])}, "one-dimensional"),
    ({"ids": np.array([1, 2, 3, 4])}, "string array"),
    ({"vectors": np.ones((3, 2))}, "one nonempty vector"),
    ({"vectors": np.ones(4)}, "one nonempty vector"),
    ({"vectors": np.empty((4, 0))}, "one nonempty vector"),
    ({"vectors": np.full((4, 2), float("nan"))}, "finite"),
    ({"vectors": np.full((4, 2), float("inf"))}, "finite"),
    ({"vectors": np.zeros((4, 2))}, "nonzero"),
    ({"vectors": VECTORS * 2}, "L2-normalized"),
])
def test_invalid_arrays_fail_before_search(tmp_path, changes, match):
    write_materials(tmp_path, **changes)
    with pytest.raises(ValueError, match=match):
        OnetIndex(tmp_path, encoder=FakeEncoder())


def test_pickled_object_arrays_are_never_loaded(tmp_path):
    write_materials(tmp_path, ids=np.array(["z", "b", "a", "d"], dtype=object))
    with pytest.raises(ValueError, match="allow_pickle=False"):
        OnetIndex(tmp_path)


def test_missing_npz_fields_rejected(tmp_path):
    write_materials(tmp_path)
    np.savez(tmp_path / "ONET_embeddings.npz", vectors=VECTORS)
    with pytest.raises(ValueError, match="vectors and doc_ids"):
        OnetIndex(tmp_path)


@pytest.mark.parametrize("records,match", [
    ([], "at least one"),
    ([RECORDS[0], RECORDS[0]], "unique"),
    ([{**RECORDS[0], "text": "  "}], "nonempty"),
    ([{**RECORDS[0], "doc_id": "  "}], "nonempty"),
    ([{**RECORDS[0], "text": "!!!"}], "searchable words"),
])
def test_invalid_records_rejected(tmp_path, records, match):
    write_materials(tmp_path, records=records, vectors=np.tile([1, 0], (len(records), 1)))
    with pytest.raises(ValueError, match=match):
        OnetIndex(tmp_path)


def test_wrong_csv_columns_rejected(tmp_path):
    write_materials(tmp_path)
    (tmp_path / "ONET_index.csv").write_text("id,text\nx,something\n")
    with pytest.raises(ValueError, match="CSV must contain"):
        OnetIndex(tmp_path)


def test_malformed_csv_rows_rejected(tmp_path):
    write_materials(tmp_path)
    with (tmp_path / "ONET_index.csv").open("a") as handle:
        handle.write("missing,columns\n")
    with pytest.raises(ValueError, match="malformed"):
        OnetIndex(tmp_path)


def test_incompatible_embeddings_fail_instead_of_producing_candidates(index):
    index._encoder.values[RECORDS[0]["text"]] = [0, 1]
    with pytest.raises(ValueError, match="Rebuild document vectors"):
        index.search("treatment")
    assert index.policy["embedding"]["compatibility"]["status"] == "not_checked"
    assert len(index._encoder.calls) == 1


@pytest.mark.parametrize("vector,match", [
    ([1, 0, 0], "dimensions differ"),
    ([float("nan"), 0], "finite"),
    ([0, 0], "nonzero"),
])
def test_invalid_query_vector_rejected(index, vector, match):
    index._encoder.query_vector = vector
    with pytest.raises(ValueError, match=match):
        index.search("query")


@pytest.mark.parametrize("query", ["", " \n ", None, 123])
def test_empty_or_nontext_query_rejected(index, query):
    with pytest.raises(ValueError, match="nonempty text"):
        index.search(query)


@pytest.mark.parametrize("options", [
    {"dense_k": -1}, {"bm25_k": -1}, {"limit": 0}, {"limit": True},
    {"dense_k": 2.5}, {"dense_k": 0, "bm25_k": 0},
])
def test_invalid_limits_rejected(index, options):
    with pytest.raises(ValueError):
        index.search("query", **options)


def test_cancellation_prevents_loading_or_search(tmp_path, index):
    with pytest.raises(InterruptedError, match="cancelled"):
        OnetIndex(tmp_path, cancelled=lambda: True)
    with pytest.raises(InterruptedError, match="cancelled"):
        index.search("query", cancelled=lambda: True)
    assert not index._encoder.calls


def test_cancellation_after_encoding_does_not_publish_compatibility(index):
    with pytest.raises(InterruptedError, match="cancelled"):
        index.search("query", cancelled=lambda: bool(index._encoder.calls))
    assert index.policy["embedding"]["compatibility"]["status"] == "not_checked"


def test_supplied_materials_have_aligned_records_and_vectors():
    if not DEFAULT_MATERIALS_DIR.is_dir():
        pytest.skip("Supplied O*NET materials are not present")
    index = OnetIndex()
    assert index.policy["record_count"] == 3197
    assert index.policy["embedding"]["dimensions"] == 384
    candidates = index.search("Assess the risks and benefits of therapies for allergic and immunologic disorders", dense_k=0)
    assert "dwa:4.A.2.a.1.f.4::29-1229.01" in [candidate["doc_id"] for candidate in candidates]
