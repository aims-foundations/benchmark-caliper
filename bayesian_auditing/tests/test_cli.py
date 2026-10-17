import json
import sys
from contextlib import nullcontext

import pytest

from bayesian_auditing.__main__ import main


@pytest.fixture(autouse=True)
def local_retriever(monkeypatch):
    """Exercise the CLI boundary without downloading model weights in tests."""
    from bayesian_auditing import retrieval

    calls = []

    class FakeIndex:
        def __init__(self, items, cache_dir=None):
            rows = list(items)
            grouped = {}
            for row in rows:
                key = row["evidence_hash"]
                grouped.setdefault(key, {"evidence_hash": key, "evidence": row["evidence"], "sources": []})
                grouped[key]["sources"].append(row["source"])
            self.items = list(grouped.values())
            self.total, self.source_rows_seen, self.contentless_items = len(self.items), len(rows), 0
            self.indexed_items = self.total
            self.cache_dir = cache_dir

        def search(self, query, top_k):
            calls.append((query, top_k, self.cache_dir))
            return [{**item, "retrieval_rank": rank, "retrieval_score": 0.9 / rank, "exact_match": False}
                    for rank, item in enumerate(self.items[:top_k], 1)]

    monkeypatch.setattr(retrieval, "ItemIndex", FakeIndex)
    return calls


def arguments(corpus, tmp_path):
    inventory = tmp_path / "inventory.json"
    inventory.write_text(json.dumps(corpus[0]))
    deployment = tmp_path / "deployment.txt"
    deployment.write_text("A text mathematics tutor")
    return ["bayesian_auditing", "run", "--inventory", str(inventory),
            "--deployment", str(deployment), "--output-dir", str(tmp_path / "output")]


def test_cli_preview_and_resume_without_api_key(corpus, tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    args = arguments(corpus, tmp_path) + ["--dry-run", "--limit-per-table", "1"]
    monkeypatch.setattr(sys, "argv", args)
    assert main() == 0
    config = json.loads((tmp_path / "output/run.json").read_text())
    assert config["model"] == "gpt-6-luna"
    assert config["reasoning_effort"] == "high"
    assert config["max_output_tokens"] == 25_000
    assert config["retrieval"]["requested_k"] == 20
    assert config["retrieval"]["indexed_items"] == 1
    before = (tmp_path / "output/assessments.jsonl").read_bytes()
    from bayesian_auditing import __main__ as cli

    def no_retrieval(*args, **kwargs):
        raise AssertionError("Resume must use its frozen shortlist")

    monkeypatch.setattr(cli, "retrieve_candidates", no_retrieval)
    monkeypatch.setattr(sys, "argv", args + ["--resume"])
    assert main() == 0
    assert (tmp_path / "output/assessments.jsonl").read_bytes() == before


def test_cli_requires_key_before_creating_live_run(corpus, tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(sys, "argv", arguments(corpus, tmp_path))
    assert main() == 1
    assert "Set OPENAI_API_KEY" in capsys.readouterr().err
    assert not (tmp_path / "output").exists()


def test_reference_question_and_shortlist_limit(corpus, tmp_path, monkeypatch, local_retriever):
    question = tmp_path / "question.txt"
    question.write_text("  Compute 1 + 1.\n")
    cache = tmp_path / "embedding-cache"
    args = arguments(corpus, tmp_path) + ["--dry-run", "--retrieve-k", "1",
                                         "--retrieval-query", str(question),
                                         "--embedding-cache-dir", str(cache)]
    monkeypatch.setattr(sys, "argv", args)
    assert main() == 0
    assert local_retriever == [("  Compute 1 + 1.\n", 1, cache)]
    summary = json.loads((tmp_path / "output/summary.json").read_text())
    assert summary["indexed_items"] == 3
    assert summary["retrieved_candidates"] == summary["previews"] == 1
    assert summary["full_inventory_indexed"]
    assert not summary["full_inventory_scored"]


def test_live_run_only_judges_the_retrieved_shortlist(corpus, tmp_path, monkeypatch, assessment_dict):
    from bayesian_auditing import __main__ as cli
    from bayesian_auditing.scoring import Assessment, score_summary
    import openai

    calls = []

    def judge(evidence):
        calls.append(evidence)
        assessment = Assessment.model_validate(assessment_dict)
        return {"status": "complete", **score_summary(assessment), "assessment": assessment.model_dump()}

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(openai, "OpenAI", lambda **kwargs: nullcontext(object()))
    monkeypatch.setattr(cli, "Judge", lambda *args, **kwargs: judge)
    monkeypatch.setattr(sys, "argv", arguments(corpus, tmp_path) + ["--retrieve-k", "1"])
    assert main() == 0
    assert len(calls) == 1
    ranks = json.loads((tmp_path / "output/ranked_items.json").read_text())
    assert ranks[0]["retrieval_rank"] == 1
    assert ranks[0]["retrieval_score"] == 0.9
    assert len(ranks[0]["sources"]) == 2


@pytest.mark.parametrize("option", ["--retrieve-k", "--top-k", "--limit-per-table"])
def test_invalid_limits_rejected_before_retrieval(corpus, tmp_path, monkeypatch, local_retriever, option):
    monkeypatch.setattr(sys, "argv", arguments(corpus, tmp_path) + ["--dry-run", option, "0"])
    assert main() == 1
    assert local_retriever == []


@pytest.mark.parametrize("change", ["query", "policy", "retrieve_k"])
def test_resume_rejects_changed_retrieval_without_reindexing(corpus, tmp_path, monkeypatch, change, capsys):
    from bayesian_auditing import __main__ as cli, retrieval

    args = arguments(corpus, tmp_path) + ["--dry-run"]
    monkeypatch.setattr(sys, "argv", args)
    assert main() == 0
    monkeypatch.setattr(cli, "retrieve_candidates", lambda *args, **kwargs: pytest.fail("Unexpected reindex"))
    if change == "policy":
        monkeypatch.setattr(retrieval, "RETRIEVAL_POLICY", {**retrieval.RETRIEVAL_POLICY, "version": -1})
    elif change == "query":
        question = tmp_path / "different.txt"
        question.write_text("Another reference question")
        args += ["--retrieval-query", str(question)]
    else:
        args += ["--retrieve-k", "1"]
    monkeypatch.setattr(sys, "argv", args + ["--resume"])
    assert main() == 1
    assert "Retrieval settings changed" in capsys.readouterr().err
