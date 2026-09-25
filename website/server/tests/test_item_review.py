"""Hosted item review: real HTTP handlers, no paid calls or dataset downloads."""

import asyncio
import copy
import json
import time

from fastapi.testclient import TestClient
from openai import OpenAIError
import pytest

from bayesian_auditing.scoring import Assessment, DIMENSIONS, score_summary
from website.server import app as app_module, db, item_review

KEY = "sk-test-item-review-secret"
HF_KEY = "hf_test_read_secret"
BODY = {
    "deployment": {"task": "A mathematics tutor for secondary school", "users": "English-speaking students",
                   "inputs": "Text questions", "outputs": "Text explanations", "success": "Correct and helpful answers", "constraints": ""},
    "benchmarks": ["matharena", "afrimedqa"], "items_per_table": 2, "top_k": 10,
}
ITEM = {"evidence_hash": "item-a", "evidence": {"item": {"content": "1+1", "grading_criterion": "2"}},
        "sources": [{"benchmark": "matharena", "branch": "main", "item_id": "a", "row": 1}]}


def assessment(score=4):
    dimensions = {
        dimension: {"score": score, "justification": "Relevant to the described task.",
                    "confidence": "high", "confidence_rationale": "Direct textual evidence.",
                    "evidence": ["item.content: 1+1"], "information_gaps": []} for dimension in DIMENSIONS}
    return {"status": "complete", **score_summary(Assessment.model_validate(dimensions)), "assessment": dimensions,
        "usage": {"input_tokens": 100, "output_tokens": 50, "output_tokens_details": {"reasoning_tokens": 20}}}


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DEFAULT_DB_PATH", tmp_path / "runs.db")
    monkeypatch.setattr(item_review, "jobs", {})
    monkeypatch.setattr(item_review, "get_token", lambda: "server-hf-token")
    monkeypatch.setattr(item_review, "load_sample", lambda *_: (3, [copy.deepcopy(ITEM), {**copy.deepcopy(ITEM), "evidence_hash": "item-b"}]))

    class FakeClient:
        def __init__(self, **kwargs):
            assert kwargs["api_key"] == KEY
            assert kwargs["base_url"] == "https://api.openai.com/v1"

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

    class FakeJudge:
        def __init__(self, client, deployment, prompt):
            assert "mathematics tutor" in deployment
            assert "input_ontology" in prompt
            self.count = 0

        async def __call__(self, evidence):
            self.count += 1
            return assessment(self.count + 2)

    monkeypatch.setattr(item_review, "AsyncOpenAI", FakeClient)
    monkeypatch.setattr(item_review, "AsyncJudge", FakeJudge)
    with TestClient(app_module.app) as test_client:
        yield test_client


def start(client, body=None):
    response = client.post("/api/item-review/runs", json=body or BODY,
                           headers={"X-OpenAI-Key": KEY, "X-HuggingFace-Key": HF_KEY})
    assert response.status_code == 202, response.text
    return response.json()


def finished(client, access):
    for _ in range(100):
        response = client.get(f"/api/item-review/runs/{access['run_id']}",
                              headers={"X-Review-Token": access["run_secret"]})
        assert response.status_code == 200
        if response.json()["status"] not in {"preparing", "running"}:
            return response
        time.sleep(.01)
    pytest.fail("Review did not finish")


def test_catalog_and_ranked_review(client, caplog):
    catalog = client.get("/api/item-review/catalog").json()
    assert catalog["reasoning_effort"] == "high"
    assert len(catalog["branches"]) == 2
    assert catalog["requires_hf_token"] is False
    access = start(client)
    response = finished(client, access)
    result = response.json()
    assert result["status"] == "completed"
    assert [row["overall_score"] for row in result["ranked_items"]] == [4, 3]
    assert result["processed"] == 2 and result["source_rows"] == 3
    assert result["scope"]["sample_only"] is True
    assert result["usage"]["output_tokens"] == 100
    assert response.headers["cache-control"] == "no-store"
    assert KEY not in response.text + caplog.text
    assert HF_KEY not in response.text + caplog.text
    assert access["run_secret"] not in response.text


def test_access_token_required_for_results_and_cancel(client):
    access = start(client)
    assert client.get(f"/api/item-review/runs/{access['run_id']}").status_code == 404
    assert client.post(f"/api/item-review/runs/{access['run_id']}/cancel",
                       headers={"X-Review-Token": "wrong"}).status_code == 404


def test_missing_keys_and_invalid_scope_make_no_jobs(client, monkeypatch):
    assert client.post("/api/item-review/runs", json=BODY).status_code == 401
    monkeypatch.setattr(item_review, "get_token", lambda: None)
    assert client.get("/api/item-review/catalog").json()["requires_hf_token"] is True
    assert client.post("/api/item-review/runs", json=BODY, headers={"X-OpenAI-Key": KEY}).status_code == 400
    for body in ({**BODY, "benchmarks": ["arbitrary-path"]}, {**BODY, "items_per_table": 1000},
                 {**BODY, "deployment": {**BODY["deployment"], "task": " "}}):
        response = client.post("/api/item-review/runs", json=body, headers={"X-OpenAI-Key": KEY, "X-HuggingFace-Key": HF_KEY})
        assert response.status_code in {400, 422}
    assert not item_review.jobs


def test_provider_error_is_sanitized(client, monkeypatch):
    class BrokenJudge:
        def __init__(self, *args):
            pass

        async def __call__(self, _):
            raise OpenAIError(f"Request containing {KEY} and {HF_KEY} failed")

    monkeypatch.setattr(item_review, "AsyncJudge", BrokenJudge)
    response = finished(client, start(client))
    assert response.json()["status"] == "failed"
    assert KEY not in response.text and HF_KEY not in response.text


def test_cancellation_prevents_more_calls_and_duplicate_running_key(client, monkeypatch):
    calls = []

    class SlowJudge:
        def __init__(self, *args):
            pass

        async def __call__(self, evidence):
            calls.append(evidence)
            await asyncio.sleep(100)
            return assessment()

    monkeypatch.setattr(item_review, "AsyncJudge", SlowJudge)
    access = start(client)
    duplicate = client.post("/api/item-review/runs", json=BODY, headers={"X-OpenAI-Key": KEY})
    assert duplicate.status_code == 429
    response = client.post(f"/api/item-review/runs/{access['run_id']}/cancel",
                           headers={"X-Review-Token": access["run_secret"]})
    assert response.json()["status"] == "cancelled"
    assert len(calls) <= 1
    assert item_review.jobs[access["run_id"]].task.done()


def test_partial_assessment_is_ranked_with_confidence_and_policy(client, monkeypatch):
    class UnknownJudge:
        def __init__(self, *args):
            pass

        async def __call__(self, _):
            result = assessment()
            result["assessment"]["output_content"].update(score=None, confidence="insufficient", information_gaps=["Reference not available"])
            result.update(score_summary(Assessment.model_validate(result["assessment"])))
            return result

    monkeypatch.setattr(item_review, "AsyncJudge", UnknownJudge)
    result = finished(client, start(client)).json()
    assert result["complete"] == result["needs_review"] == 2
    assert len(result["ranked_items"]) == 2 and result["failed_items"] == []
    assert result["scoring_policy"]["version"] == 2
    for item in result["ranked_items"]:
        assert item["overall_score"] == pytest.approx(23 / 6)
        assert item["scored_dimensions"] == 5 and item["needs_review"]
        assert item["assessment"]["output_content"]["confidence"] == "insufficient"


def test_expired_review_is_removed(client):
    access = start(client)
    finished(client, access)
    item_review.jobs[access["run_id"]].finished_at = time.monotonic() - 3601
    response = client.get(f"/api/item-review/runs/{access['run_id']}", headers={"X-Review-Token": access["run_secret"]})
    assert response.status_code == 404
    assert access["run_id"] not in item_review.jobs


def test_ten_items_with_eight_partial_assessments_all_rank():
    job = item_review.ReviewJob("fixture", "secret", "owner", item_review.ReviewRequest(**BODY))
    for index in range(10):
        result = assessment()
        if index >= 2:
            result["assessment"]["output_content"].update(
                score=None, confidence="insufficient", information_gaps=["Reference not available"])
            result.update(score_summary(Assessment.model_validate(result["assessment"])))
        job.results.append({**copy.deepcopy(ITEM), **result, "evidence_hash": str(index)})
    report = item_review.public_job(job)
    assert report["complete"] == 10 and report["needs_review"] == 8
    assert len(report["ranked_items"]) == 10
    assert report["failed_items"] == []


def test_invalid_response_stays_failed_and_has_no_invented_score(client, monkeypatch):
    class InvalidJudge:
        def __init__(self, *args):
            pass

        async def __call__(self, _):
            return {"status": "error", "error": f"Bad provider output containing {KEY}"}

    monkeypatch.setattr(item_review, "AsyncJudge", InvalidJudge)
    response = finished(client, start(client))
    report = response.json()
    assert report["complete"] == 0 and report["errors"] == 2
    assert len(report["failed_items"]) == 2 and report["ranked_items"] == []
    assert all("overall_score" not in item for item in report["failed_items"])
    assert KEY not in response.text


def test_sample_uses_pinned_tables_and_preserves_duplicate_sources(monkeypatch):
    seen = {}

    def items(data, limit, *, token):
        seen.update(data=data, limit=limit, token=token)
        for branch in data["branches"]:
            yield {"evidence_hash": "same", "evidence": ITEM["evidence"], "source": {"branch": branch}}

    monkeypatch.setattr(item_review, "iter_items", items)
    count, unique = item_review.load_sample(item_review.ReviewRequest(**BODY), HF_KEY)
    assert count == 2 and len(unique) == 1 and len(unique[0]["sources"]) == 2
    assert len(seen["data"]["tables"]) == 3
    assert seen["token"] == HF_KEY and seen["limit"] == 2
