import copy
import sqlite3
import stat
import sys
from types import SimpleNamespace

import numpy as np
import pytest

from bayesian_auditing.retrieval import ItemIndex, MAX_TOKENS, MODEL_ID, MODEL_REVISION, QwenEncoder, question_text


def item(content, *, key=None, source="main", answer=None, **evidence):
    record = {"evidence": {"item": {"content": content, "grading_criterion": answer}, **evidence},
              "source": {"branch": source, "row": 1}}
    if key is not None:
        record["evidence_hash"] = key
    return record


class FakeEncoder:
    dimensions = 2
    cache_namespace = "retrieval-tests-v1"

    def __init__(self, vectors=None):
        self.vectors = vectors or {}
        self.calls = []

    def encode(self, texts):
        self.calls.append(list(texts))
        return np.asarray([self.vectors.get(text, [3, 4]) for text in texts], dtype=np.float32)


def test_normalized_single_dot_product_ranking(tmp_path):
    encoder = FakeEncoder({"query": [10, 0], "first": [30, 40], "second": [0, 8], "third": [-2, 0]})
    index = ItemIndex([item("third", key="c"), item("second", key="b"), item("first", key="a")],
                      cache_dir=tmp_path, encoder=encoder)
    ranked = index.search("query")
    assert [result["evidence_hash"] for result in ranked] == ["a", "b", "c"]
    assert [result["retrieval_score"] for result in ranked] == pytest.approx([0.6, 0.0, -1.0])
    assert [result["retrieval_rank"] for result in ranked] == [1, 2, 3]
    assert all(not result["exact_match"] for result in ranked)
    assert all("rank" not in result and "assessment" not in result and "confidence" not in result for result in ranked)
    assert np.linalg.norm(index._vectors, axis=1) == pytest.approx([1.0, 1.0, 1.0])


def test_literal_exact_match_beats_score_and_hash(tmp_path):
    encoder = FakeEncoder({"question": [0, 1], "different question": [1, 0]})
    index = ItemIndex([item("different question", key="a"), item("question", key="z")],
                      cache_dir=tmp_path, encoder=encoder)
    # Even a mismatched query vector must not displace literal equality.
    encoder.vectors["question"] = [1, 0]
    ranked = index.search("question")
    assert [result["evidence_hash"] for result in ranked] == ["z", "a"]
    assert ranked[0]["exact_match"] and ranked[0]["retrieval_score"] == 0
    assert not ranked[1]["exact_match"] and ranked[1]["retrieval_score"] == 1


def test_identical_prefixes_are_not_literal_matches(tmp_path):
    prefix = "word " * (MAX_TOKENS + 1)
    question = prefix + "original tail"
    different = prefix + "different tail"
    # Simulate truncation producing identical vectors for two distinct questions.
    index = ItemIndex([item(different, key="a"), item(question, key="z")],
                      cache_dir=tmp_path, encoder=FakeEncoder())
    ranked = index.search(question)
    assert [result["evidence_hash"] for result in ranked] == ["z", "a"]
    assert [result["exact_match"] for result in ranked] == [True, False]
    assert ranked[0]["evidence"]["item"]["content"] == question
    assert ranked[1]["evidence"]["item"]["content"] == different
    assert len(question) > MAX_TOKENS


def test_symmetric_identical_text_has_unit_similarity_and_literal_case_matters(tmp_path):
    index = ItemIndex([item("Question", key="a"), item("question", key="b"), item(" question", key="c")],
                      cache_dir=tmp_path, encoder=FakeEncoder())
    ranked = index.search("question")
    assert ranked[0]["evidence_hash"] == "b"
    assert ranked[0]["retrieval_score"] == pytest.approx(1.0)
    assert [result["exact_match"] for result in ranked] == [True, False, False]
    assert all(-1 <= result["retrieval_score"] <= 1 for result in ranked)


def test_same_question_shares_vector_but_different_answers_remain_candidates(tmp_path):
    first = item("arithmetic", source="main", answer="2")
    duplicate = item("arithmetic", source="migration", answer="2")
    alternate = item("arithmetic", answer="3")
    encoder = FakeEncoder()
    index = ItemIndex([first, duplicate, first, alternate], cache_dir=tmp_path, encoder=encoder)
    assert encoder.calls == [["arithmetic"]]
    ranked = index.search("arithmetic")
    assert index.total == 2 and index.source_rows_seen == 4 and index.source_references == 3
    assert index.unique_questions == 1 and len(ranked) == 2
    assert all(result["exact_match"] for result in ranked)
    result = next(result for result in ranked if result["evidence"]["item"]["grading_criterion"] == "2")
    assert {source["branch"] for source in result["sources"]} == {"main", "migration"}


def test_cache_reuses_document_vectors_across_runs_but_never_query_vectors(tmp_path):
    first = FakeEncoder()
    ItemIndex([item("question", answer="old answer")], cache_dir=tmp_path, encoder=first).search("query")
    second = FakeEncoder()
    index = ItemIndex([item("question", answer="new answer", source="other")], cache_dir=tmp_path, encoder=second)
    assert index.cache_hits == 1 and index.embedded_questions == 0 and second.calls == []
    index.search("query")
    index.search("query")
    assert second.calls == [["query"], ["query"]]
    with sqlite3.connect(tmp_path / "vectors.sqlite3") as connection:
        assert connection.execute("SELECT COUNT(*) FROM vectors").fetchone()[0] == 1
    assert stat.S_IMODE(tmp_path.stat().st_mode) == 0o700


def test_cache_identity_includes_full_tail_and_encoder_namespace(tmp_path):
    encoder = FakeEncoder()
    prefix = "x " * MAX_TOKENS
    ItemIndex([item(prefix + "a"), item(prefix + "b")], cache_dir=tmp_path, encoder=encoder)
    assert sorted(text for call in encoder.calls for text in call) == [prefix + "a", prefix + "b"]
    second = FakeEncoder()
    second.cache_namespace = "other-encoder"
    ItemIndex([item(prefix + "a")], cache_dir=tmp_path, encoder=second)
    assert second.calls == [[prefix + "a"]]


def test_corrupt_cache_vector_is_recomputed(tmp_path):
    ItemIndex([item("question")], cache_dir=tmp_path, encoder=FakeEncoder())
    with sqlite3.connect(tmp_path / "vectors.sqlite3") as connection:
        connection.execute("UPDATE vectors SET vector = ?", (np.array([np.nan, 1], dtype="<f4").tobytes(),))
    encoder = FakeEncoder()
    index = ItemIndex([item("question")], cache_dir=tmp_path, encoder=encoder)
    assert encoder.calls == [["question"]] and index.cache_hits == 0


def test_question_only_embedding_preserves_original_evidence(tmp_path):
    original = item("Question exactly as written.  ", answer="SECRET ANSWER", benchmark={"name": "SECRET METADATA"})
    before = copy.deepcopy(original)
    encoder = FakeEncoder()
    index = ItemIndex([original], cache_dir=tmp_path, encoder=encoder)
    assert encoder.calls == [["Question exactly as written.  "]]
    assert original == before and index.items[0]["evidence"] == original["evidence"]
    structured = {"item": {"content": {"messages": [{"role": "user", "content": "What is arithmetic?"},
                                                   {"role": "assistant", "content": "SECRET"}],
                                      "reference_answer": "SECRET", "metadata": "SECRET"}}}
    assert question_text(structured) == "What is arithmetic?"


def test_missing_content_and_blank_queries_do_not_call_encoder(tmp_path):
    encoder = FakeEncoder()
    index = ItemIndex([item(None), item("  "), item({"image_url": "https://example.com/image"})],
                      cache_dir=tmp_path, encoder=encoder)
    assert index.total == 3 and index.contentless_items == 3 and index.indexed_items == 0
    assert index.search("question") == index.search("") == []
    assert encoder.calls == []
    with_text = ItemIndex([item("question")], cache_dir=tmp_path, encoder=encoder)
    calls = copy.deepcopy(encoder.calls)
    assert with_text.search("\n ") == [] and encoder.calls == calls


def test_ties_and_source_order_are_deterministic(tmp_path):
    records = [item("question", key="b", source="migration"),
               item("question", key="a"), item("question", key="b")]
    forward = ItemIndex(records, cache_dir=tmp_path, encoder=FakeEncoder()).search("query")
    reverse = ItemIndex(reversed(records), cache_dir=tmp_path, encoder=FakeEncoder()).search("query")
    assert forward == reverse
    assert [result["evidence_hash"] for result in forward] == ["a", "b"]


@pytest.mark.parametrize("vector", [[0, 0], [float("nan"), 1], [float("inf"), 1]])
def test_invalid_vectors_fail_clearly(tmp_path, vector):
    with pytest.raises(ValueError, match="finite|nonzero"):
        ItemIndex([item("question")], cache_dir=tmp_path, encoder=FakeEncoder({"question": vector}))


def test_query_dimension_mismatch_fails(tmp_path):
    encoder = FakeEncoder()
    index = ItemIndex([item("question")], cache_dir=tmp_path, encoder=encoder)
    encoder.vectors["query"] = [1, 2, 3]
    with pytest.raises(ValueError, match="dimensions"):
        index.search("query")


@pytest.mark.parametrize("top_k", [0, -1, True, 1.5])
def test_invalid_top_k(tmp_path, top_k):
    with pytest.raises(ValueError, match="top_k"):
        ItemIndex([], cache_dir=tmp_path, encoder=FakeEncoder()).search("query", top_k=top_k)


def test_cancellation_is_per_operation_and_progress_is_reported(tmp_path):
    with pytest.raises(InterruptedError, match="cancelled"):
        ItemIndex([item("question")], cache_dir=tmp_path, encoder=FakeEncoder(), cancelled=lambda: True)
    progress = []
    cancellation = [False]
    index = ItemIndex([item("question")], cache_dir=tmp_path, encoder=FakeEncoder(),
                      cancelled=lambda: cancellation[0], progress=progress.append)
    assert progress[-1] == {"stage": "embedding", "completed": 1, "total": 1, "cache_hits": 0}
    cancellation[0] = True
    assert len(index.search("question")) == 1
    with pytest.raises(InterruptedError):
        index.search("question", cancelled=lambda: True)


def test_conflicting_evidence_hash_fails(tmp_path):
    with pytest.raises(ValueError, match="Conflicting evidence"):
        ItemIndex([item("arithmetic", key="same"), item("poetry", key="same")],
                  cache_dir=tmp_path, encoder=FakeEncoder())


def test_qwen_encoder_uses_pinned_revision_and_8192_token_truncation(monkeypatch):
    torch = pytest.importorskip("torch")
    if not hasattr(torch, "tensor"):
        pytest.skip("A working torch installation is required for encoder pooling test")
    tokenizer_calls = []
    loads = []

    class Inputs(dict):
        def to(self, device):
            return self

    class Tokenizer:
        def __call__(self, texts, **kwargs):
            tokenizer_calls.append((texts, kwargs))
            return Inputs(input_ids=torch.tensor([[1, 2] for _ in texts]),
                          attention_mask=torch.tensor([[1, 1] for _ in texts]))

    class Model:
        device = "cpu"

        def to(self, device):
            return self

        def eval(self):
            return self

        def __call__(self, **inputs):
            return SimpleNamespace(last_hidden_state=torch.tensor([[[1., 0.], [3., 4.]] for _ in inputs["input_ids"]]))

    def load_tokenizer(model, **kwargs):
        loads.append(("tokenizer", model, kwargs))
        return Tokenizer()

    def load_model(model, **kwargs):
        loads.append(("model", model, kwargs))
        return Model()

    monkeypatch.setitem(sys.modules, "transformers", SimpleNamespace(
        AutoTokenizer=SimpleNamespace(from_pretrained=load_tokenizer),
        AutoModel=SimpleNamespace(from_pretrained=load_model),
    ))
    encoder = QwenEncoder(device="cpu")
    vector = encoder.encode(["word " * 9000])
    assert vector.tolist()[0] == pytest.approx([0.6, 0.8])
    assert tokenizer_calls[0][1] == {"padding": True, "truncation": True, "max_length": 8192, "return_tensors": "pt"}
    assert all(model == MODEL_ID and kwargs["revision"] == MODEL_REVISION for _, model, kwargs in loads)
    assert loads[0][2]["padding_side"] == "left" and loads[0][2]["truncation_side"] == "right"
    assert tokenizer_calls[0][0] == ["word " * 9000]
