"""Hosted item review: real HTTP handlers, no paid calls or dataset downloads."""

import asyncio
import copy
import json
import time
from threading import Event

from fastapi.testclient import TestClient
from openai import OpenAIError
import pytest

from bayesian_auditing.scoring import Assessment, DIMENSIONS, score_summary
from website.server import app as app_module, db, item_review
from bayesian_auditing import sampling

REAL_REVIEW_ITEMS = item_review.review_items

KEY = "sk-test-item-review-secret"
HF_KEY = "hf_test_server_secret"
BODY = {
    "deployment": {"task": "A mathematics tutor for secondary school", "users": "English-speaking students",
                   "inputs": "Text questions", "outputs": "Text explanations", "success": "Correct and helpful answers", "constraints": ""},
}
ITEM = {"evidence_hash": "item-a", "evidence": {"item": {"content": "1+1", "grading_criterion": "2"}},
        "sources": [{"benchmark": "matharena", "branch": "main", "item_id": "a", "row": 1}]}
INVENTORY = {"repo": "fixture", "branches": {"main": "a", "migration": "b"}, "missing_item_tables": [],
             "tables": [{"benchmark": name, "branch": branch, "row_count": 1}
                        for name, branch in [("matharena", "main"), ("coding", "migration"), ("customer_support", "migration")]]}


def source_item(key="item-a", branch="main", content="1+1"):
    return {"evidence_hash": key, "evidence": {"item": {"content": content, "grading_criterion": "2"}},
            "sources": [{"benchmark": "matharena" if branch == "main" else "coding", "branch": branch,
                         "item_id": key, "row": 1}]}


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
    monkeypatch.setattr(item_review, "get_token", lambda: HF_KEY)
    monkeypatch.setattr(item_review, "inventory", lambda: copy.deepcopy(INVENTORY))
    async def sample(job):
        job.source_rows = 3
        job.prepared_benchmarks = 3
        return iter([source_item(), source_item(branch="migration"), source_item("item-b", "migration")]), 2
    monkeypatch.setattr(item_review, "review_items", sample)

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
            return assessment(3 + self.count % 2)

    monkeypatch.setattr(item_review, "AsyncOpenAI", FakeClient)
    monkeypatch.setattr(item_review, "AsyncJudge", FakeJudge)
    with TestClient(app_module.app) as test_client:
        yield test_client


def start(client, body=None):
    response = client.post("/api/item-review/runs", json=body or BODY,
                           headers={"X-OpenAI-Key": KEY})
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
    assert catalog["dataset_access_configured"] is True
    assert {b["id"] for b in catalog["benchmarks"]} == {"matharena", "coding", "customer_support"}
    assert catalog["source_rows"] == 3 and catalog["table_count"] == 3
    assert catalog["sample_max_items"] == 3
    assert catalog["sampling"]["items_per_benchmark"] == 50
    assert HF_KEY not in json.dumps(catalog)
    access = start(client)
    response = finished(client, access)
    result = response.json()
    assert result["status"] == "completed"
    assert [row["overall_score"] for row in result["ranked_items"]] == [4, 3]
    assert result["processed"] == 2 and result["source_rows"] == 3
    assert result["scope"]["sample_only"] is True
    assert result["sample_complete"] is True
    assert len(next(item for item in result["ranked_items"] if item["evidence_hash"] == "item-a")["sources"]) == 2
    assert result["usage"]["output_tokens"] == 100
    assert response.headers["cache-control"] == "no-store"
    assert KEY not in response.text + caplog.text
    assert HF_KEY not in response.text + caplog.text
    assert access["run_secret"] not in response.text


def test_access_token_required_for_results_and_cancel(client):
    access = start(client)
    assert client.get(f"/api/item-review/runs/{access['run_id']}").status_code == 404
    assert client.get(f"/api/item-review/runs/{access['run_id']}/export").status_code == 404
    assert client.post(f"/api/item-review/runs/{access['run_id']}/cancel",
                       headers={"X-Review-Token": "wrong"}).status_code == 404


def test_missing_keys_and_invalid_scope_make_no_jobs(client, monkeypatch):
    assert client.post("/api/item-review/runs", json=BODY).status_code == 401
    monkeypatch.setattr(item_review, "get_token", lambda: None)
    assert client.get("/api/item-review/catalog").json()["dataset_access_configured"] is False
    response = client.post("/api/item-review/runs", json=BODY, headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 503
    assert "contact the site maintainer" in response.json()["detail"]
    # A client-supplied HF header cannot replace the server's dataset access.
    assert client.post("/api/item-review/runs", json=BODY,
                       headers={"X-OpenAI-Key": KEY, "X-HuggingFace-Key": HF_KEY}).status_code == 503
    for body in ({**BODY, "benchmarks": ["arbitrary-path"]}, {**BODY, "items_per_table": 1000},
                 {**BODY, "deployment": {**BODY["deployment"], "task": " "}}):
        response = client.post("/api/item-review/runs", json=body, headers={"X-OpenAI-Key": KEY})
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
    directory = item_review.jobs[access["run_id"]].results.directory.name
    item_review.jobs[access["run_id"]].finished_at = time.monotonic() - 3601
    response = client.get(f"/api/item-review/runs/{access['run_id']}", headers={"X-Review-Token": access["run_secret"]})
    assert response.status_code == 404
    assert access["run_id"] not in item_review.jobs
    from pathlib import Path
    assert not Path(directory).exists()


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
    job.results.close()


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


def test_sample_review_crosses_result_page_size_and_exports_every_rank(client, monkeypatch):
    rows = [source_item(str(index), "main" if index < 35 else "migration", "last" if index == 44 else "normal")
            for index in range(45)]
    rows.append({**rows[0], "sources": [{**rows[0]["sources"][0], "branch": "migration"}]})
    calls = []

    class Judge:
        def __init__(self, *args):
            pass

        async def __call__(self, evidence):
            calls.append(evidence)
            return assessment(5 if evidence["item"]["content"] == "last" else 3)

    async def sample(job):
        job.source_rows = 46
        job.prepared_benchmarks = 3
        return iter(rows), 45
    monkeypatch.setattr(item_review, "review_items", sample)
    monkeypatch.setattr(item_review, "AsyncJudge", Judge)
    access = start(client)
    first = finished(client, access).json()
    assert first["processed"] == first["complete"] == len(calls) == 45
    assert first["source_rows"] == 46 and first["sample_complete"]
    assert first["ranked_items"][0]["evidence_hash"] == "44"
    assert len(first["ranked_items"]) == 20
    headers = {"X-Review-Token": access["run_secret"]}
    url = f"/api/item-review/runs/{access['run_id']}"
    second = client.get(url + "?page=2", headers=headers).json()
    third = client.get(url + "?page=3", headers=headers).json()
    assert second["ranked_items"][0]["rank"] == 21
    assert len(third["ranked_items"]) == 5
    exported = client.get(url + "/export", headers=headers).json()
    assert len(exported["ranked_items"]) == 45
    assert [item["rank"] for item in exported["ranked_items"]] == list(range(1, 46))
    assert len(next(item for item in exported["ranked_items"] if item["evidence_hash"] == "0")["sources"]) == 2
    assert "pagination" not in exported


def test_item_failure_keeps_partial_results_and_does_not_claim_complete_sample(client, monkeypatch):
    async def broken_items(job):
        job.source_rows = 3
        def rows():
            yield source_item()
            raise ValueError("Unreadable selected item")
        return rows(), 2

    monkeypatch.setattr(item_review, "review_items", broken_items)
    result = finished(client, start(client)).json()
    assert result["status"] == "failed"
    assert result["complete"] == 1 and result["sample_complete"] is False


def test_web_review_assesses_only_the_fixed_sample_and_reuses_it(client, monkeypatch):
    rows = []
    for branch, numbers in (("main", range(250)), ("migration", range(200, 450))):
        for number in numbers:
            item = source_item(str(number), branch, str(number))
            source = {**item.pop("sources")[0], "benchmark": "matharena", "row": number + 1,
                      "items_path": f"{branch}/items.parquet"}
            rows.append({**item, "source": source})
    data = {**INVENTORY, "tables": [
        {"benchmark": "matharena", "branch": branch, "commit": branch,
         "items_path": f"{branch}/items.parquet", "row_count": 250}
        for branch in ("main", "migration")]}

    def reader(inventory, *, selected_rows=None, **kwargs):
        for row in rows:
            source = row["source"]
            if selected_rows is None or source["row"] in selected_rows.get((source["branch"], source["items_path"]), []):
                yield row

    monkeypatch.setattr(item_review, "inventory", lambda: copy.deepcopy(data))
    monkeypatch.setattr(item_review, "review_items", REAL_REVIEW_ITEMS)
    monkeypatch.setattr(sampling, "iter_items", reader)
    first = start(client)
    result = finished(client, first).json()
    assert result["processed"] == result["total"] == 50
    assert result["source_rows"] == 500 and result["prepared_benchmarks"] == 1
    assert result["sample_complete"] and result["scope"]["sample_only"]
    assert result["scope"]["sampling"]["seed"] == sampling.SAMPLE_SEED
    headers = {"X-Review-Token": first["run_secret"]}
    exported = client.get(f"/api/item-review/runs/{first['run_id']}/export", headers=headers).json()
    keys = {item["evidence_hash"] for item in exported["ranked_items"]}
    assert any(int(key) < 200 for key in keys) and any(int(key) >= 250 for key in keys)

    monkeypatch.setattr(sampling, "iter_items", lambda *a, **kw: pytest.fail("Should reuse the cached sample"))
    second = start(client, {"deployment": {**BODY["deployment"], "outputs": "Concise text explanations"}})
    assert finished(client, second).json()["processed"] == 50
    exported_again = client.get(f"/api/item-review/runs/{second['run_id']}/export",
                                headers={"X-Review-Token": second["run_secret"]}).json()
    assert {item["evidence_hash"] for item in exported_again["ranked_items"]} == keys


def test_preparation_can_be_cancelled_before_any_provider_call(client, monkeypatch):
    entered = Event()

    def prepare(data, cache, *, token, progress, cancelled):
        entered.set()
        assert cancelled.wait(3), "Cancellation did not reach the dataset reader"
        raise InterruptedError("Cancelled")

    monkeypatch.setattr(item_review, "review_items", REAL_REVIEW_ITEMS)
    monkeypatch.setattr(item_review, "prepare_samples", prepare)
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kw: pytest.fail("No provider calls during preparation"))
    access = start(client)
    assert entered.wait(1)
    response = client.post(f"/api/item-review/runs/{access['run_id']}/cancel",
                           headers={"X-Review-Token": access["run_secret"]})
    assert response.json()["status"] == "cancelled"
    assert response.json()["processed"] == 0


def test_preparation_failure_makes_no_provider_calls(client, monkeypatch):
    def broken(*args, **kwargs):
        raise ValueError("Missing later table")
    monkeypatch.setattr(item_review, "review_items", REAL_REVIEW_ITEMS)
    monkeypatch.setattr(item_review, "prepare_samples", broken)
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kw: pytest.fail("No provider calls before preparation succeeds"))
    result = finished(client, start(client)).json()
    assert result["status"] == "failed" and result["processed"] == 0
    assert not result["sample_complete"]
