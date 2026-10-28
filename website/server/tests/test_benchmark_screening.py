"""Initial screening through HTTP and the real SDK with an offline transport."""

import asyncio
from copy import deepcopy
import json
import time
from threading import Event

import httpx
from openai import AsyncOpenAI, OpenAIError
import pytest

from bayesian_auditing.benchmark_data import row_fingerprint, row_search_text
from bayesian_auditing.benchmark_queries import build_screening_queues
from bayesian_auditing.scoring import DIMENSIONS
from website.server import item_review
from website.server.tests.test_benchmark_retrieval import seed_grounding
from website.server.tests.test_item_review import BODY, KEY, HF_KEY, client, finished
from website.server.tests.test_onet_grounding import response_body


def seed_retrieval(*, facets=3, per_facet=24, shared=False):
    access = seed_grounding(facets=facets)
    job = item_review.jobs[access["run_id"]]
    job.request = job.request.model_copy(update={"mode": "retrieval"})
    rankings = []
    for facet in range(facets):
        candidates = []
        for number in range(per_facet):
            row = {"id": f"{'shared' if shared else facet}-{number}",
                   "content": "Explain why adding two even numbers gives an even number.",
                   "grading_criterion": "A correct explanation using divisibility by two.",
                   "extra_original_column": {"values": [None, True, 2], "spacing": "  Keep\nthis. "}}
            item_id = row_fingerprint(row)
            candidates.append({
                "item_id": item_id, "evidence_hash": item_id, "evidence": {"item": row},
                "search_text": row_search_text(row), "question_text": row["content"],
                "sources": [{"benchmark": "fixture", "branch": "main", "commit": "pinned-main",
                             "row": number, "items_path": "fixture/items.parquet"}],
                "rank": number + 1, "dense_rank": number + 1, "bm25_rank": None,
                "dense_score": 1.0, "bm25_score": None, "rrf_score": 1 / (61 + number),
            })
        rankings.append({"facet_id": f"task-{facet}", "query": f"query {facet}", "candidates": candidates})
    job.benchmark_retrieval = {
        "policy": {"fixture": True}, "scope": {"branches": {"main": "pinned-main"}, "sample_only": False},
        "stats": {}, "inventory": {"fixture": True},
        "queries": [{"facet_id": entry["facet_id"], "query": entry["query"]} for entry in rankings],
        "rankings": rankings, "queues": build_screening_queues(rankings),
    }
    return access


def test_screening_reports_unavailable_stored_evidence_before_paid_calls(client, monkeypatch):
    access = seed_retrieval(facets=1, per_facet=1)
    job = item_review.jobs[access["run_id"]]
    store = item_review.candidate_store()
    ranking = job.benchmark_retrieval["rankings"][0]
    reference = store.compact(ranking["candidates"][0])
    ranking["candidates"] = [reference]
    (store.directory / f"{reference['_candidate_ref']}.json.gz").unlink()
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("No paid client may start"))
    response = client.post(f"/api/item-review/runs/{access['run_id']}/screen", json={}, headers={
        "X-Review-Token": access["run_secret"], "X-OpenAI-Key": KEY,
    })
    assert response.status_code == 503
    assert "saved candidate evidence" in response.json()["detail"].lower()
    assert reference["_candidate_ref"] not in response.text
    assert str(store.directory) not in response.text
    assert len(item_review.jobs) == 1


def rating(item, score=4):
    return {"score": score, "evidence": [item["content"]],
            "justification": "The question asks for a mathematical explanation.",
            "information_gaps": [] if score is not None else ["The reference has not been independently checked."]}


def assessment(item, facet_id="task-0"):
    return {
        "task": {"status": "matched", "decision": "Explain a mathematical property.",
                 "matched_facet_ids": [facet_id], "evidence": [item["content"]],
                 "justification": "The question directly asks for an explanation.", "information_gaps": []},
        "ratings": {dimension: rating(item, None if dimension == "output_content" else 4)
                    for dimension in DIMENSIONS},
        "coverage": [],
    }


def mock_screener(monkeypatch, transform=lambda value, row: value):
    requests = []

    def respond(request):
        body = json.loads(request.content)
        requests.append(body)
        data = json.loads(body["input"])
        value = transform(assessment(data["item"]), data["item"])
        return httpx.Response(200, json=response_body(value))

    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: AsyncOpenAI(
        **kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))))
    return requests


def start_screening(client, source):
    response = client.post(f"/api/item-review/runs/{source['run_id']}/screen", headers={
        "X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY,
    })
    assert response.status_code == 202, response.text
    assert response.headers["cache-control"] == "no-store"
    return response.json()


def export(client, access):
    return client.get(f"/api/item-review/runs/{access['run_id']}/export",
                      headers={"X-Review-Token": access["run_secret"]})


def test_forty_eight_items_even_allocation_full_rows_independent_tasks_and_export(client, monkeypatch):
    source = seed_retrieval()
    original = finished(client, source).json()
    requests = mock_screener(monkeypatch)
    monkeypatch.setattr(item_review, "get_token", lambda: pytest.fail("Screening needs no dataset access"))
    monkeypatch.setattr(item_review, "inventory", lambda: pytest.fail("Use the saved inventory"))
    monkeypatch.setattr(item_review, "retrieve_benchmarks", lambda *args: pytest.fail("Do not retrieve again"))
    access = start_screening(client, source)
    result = finished(client, access).json()
    assert result["mode"] == "screening" and result["status"] == "completed"
    screening = result["screening"]
    assert screening["policy"]["initial_budget"] == 48
    assert screening["allocation"]["allocated"] == 48 and screening["allocation"]["shortfall"] == 0
    assert [allocation["allocated"] for allocation in screening["allocation"]["allocations"]] == [16, 16, 16]
    assert len(screening["items"]) == len(requests) == 48
    assert len({item["item_id"] for item in screening["items"]}) == 48
    for item, acquisition in zip(screening["items"], screening["allocation"]["items"]):
        assert item["item_id"] == acquisition["item_id"] == row_fingerprint(item["evidence"]["item"])
        assert item["status"] == "complete" and item["gate"]["status"] == "pass"
        assert item["assessment"]["task"]["matched_facet_ids"] == ["task-0"]
        assert item["assessment"]["ratings"]["output_content"]["score"] is None
        assert item["screened_run_id"] == access["run_id"]
    assert screening["items"][1]["acquisition"]["facet_id"] == "task-1"
    for body in requests:
        sent = json.loads(body["input"])
        assert set(sent) == {"answers", "requirements", "item"}
        assert sent["answers"] == BODY["deployment"]
        assert sent["requirements"] == result["requirements"]
        assert sent["item"]["extra_original_column"] == {"values": [None, True, 2], "spacing": "  Keep\nthis. "}
        assert body["store"] is False
        assert body["instructions"] == screening["model"]["prompt"]
        assert body["text"]["format"]["schema"] == screening["model"]["output_schema"]
    assert result["usage"]["input_tokens"] == 4800
    assert finished(client, source).json() == original
    exported = export(client, access)
    assert exported.status_code == 200
    assert exported.json()["screening"] == screening
    assert exported.json()["retrieval"] == item_review.jobs[source["run_id"]].benchmark_retrieval
    assert "benchmark-screening-" in exported.headers["content-disposition"]
    for secret in (KEY, HF_KEY, access["run_secret"], source["run_secret"]):
        assert secret not in exported.text


def test_shared_items_count_once_and_shortfall_is_explicit(client, monkeypatch):
    source = seed_retrieval(per_facet=7, shared=True)
    requests = mock_screener(monkeypatch)
    result = finished(client, start_screening(client, source)).json()["screening"]
    assert len(requests) == len(result["items"]) == 7
    assert result["allocation"]["shortfall"] == 41
    assert [entry["allocated"] for entry in result["allocation"]["allocations"]] == [3, 2, 2]


def test_empty_union_finishes_without_opening_paid_client(client, monkeypatch):
    source = seed_retrieval(per_facet=0)
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("No candidates to judge"))
    result = finished(client, start_screening(client, source)).json()
    assert result["status"] == "completed" and result["screening"]["items"] == []
    assert result["screening"]["allocation"]["shortfall"] == 48 and result["usage"] == {}


def test_gate_failures_unknowns_and_invalid_output_are_distinct(client, monkeypatch):
    source = seed_retrieval(facets=1, per_facet=4)

    def transform(value, row):
        if row["id"] == "0-0":
            value["ratings"]["input_content"] = rating(row, 2)
        elif row["id"] == "0-1":
            value["ratings"]["input_form"] = rating(row, None)
        elif row["id"] == "0-2":
            value["task"].update(status="no_match", matched_facet_ids=[])
        else:
            value["task"]["matched_facet_ids"] = ["invented-task"]
        return value

    mock_screener(monkeypatch, transform)
    result = finished(client, start_screening(client, source)).json()
    items = result["screening"]["items"]
    assert [item.get("gate", {}).get("status") for item in items] == ["fail", "unresolved", "fail", None]
    assert [item["status"] for item in items] == ["complete", "complete", "complete", "error"]
    assert result["status"] == "completed" and "1 response error." in result["message"]


def test_continuation_retries_only_errors_retains_results_and_usage_origins(client, monkeypatch):
    source = seed_retrieval(facets=1, per_facet=3)

    def invalid_one(value, row):
        if row["id"] == "0-1":
            value["ratings"]["input_content"]["score"] = 6
        else:
            value["ratings"]["input_content"]["score"] = 2  # Valid gate failures are retained.
        return value

    first_calls = mock_screener(monkeypatch, invalid_one)
    first = start_screening(client, source)
    original = finished(client, first).json()
    calls = mock_screener(monkeypatch)
    resumed = start_screening(client, first)
    result = finished(client, resumed).json()
    assert len(first_calls) == 3 and len(calls) == 1
    assert json.loads(calls[0]["input"])["item"]["id"] == "0-1"
    assert result["screening"]["allocation"] == original["screening"]["allocation"]
    assert result["usage"]["input_tokens"] == 100
    assert [item["screened_run_id"] for item in result["screening"]["items"]] == [first["run_id"], resumed["run_id"], first["run_id"]]
    assert finished(client, first).json() == original
    response = client.post(f"/api/item-review/runs/{resumed['run_id']}/screen", headers={
        "X-Review-Token": resumed["run_secret"], "X-OpenAI-Key": KEY})
    assert response.status_code == 409


def test_continuation_reuses_original_prompt_settings_after_file_edit(client, monkeypatch, tmp_path):
    from bayesian_auditing import screening

    source = seed_retrieval(facets=1, per_facet=1)
    mock_screener(monkeypatch, lambda value, row: {**value, "coverage": ["invalid"]})
    first = start_screening(client, source)
    original = finished(client, first).json()["screening"]["model"]
    changed_prompt = tmp_path / "screen_item.md"
    changed_prompt.write_text("An edited prompt for future runs.")
    monkeypatch.setattr(screening, "PROMPT_PATH", changed_prompt)
    calls = mock_screener(monkeypatch)
    result = finished(client, start_screening(client, first)).json()
    assert result["screening"]["model"] == original
    assert calls[0]["instructions"] == original["prompt"]
    assert calls[0]["model"] == original["model"]
    assert calls[0]["max_output_tokens"] == original["max_output_tokens"]


def test_export_keeps_coherent_screening_snapshot_and_releases_download(client, monkeypatch):
    source = seed_retrieval(facets=1, per_facet=2)
    mock_screener(monkeypatch)
    access = start_screening(client, source)
    original = finished(client, access).json()
    job = item_review.jobs[access["run_id"]]

    async def download():
        response = await item_review.export_review(job.run_id, job.secret)
        assert job.downloads == 1
        job.screening = {**job.screening, "items": []}
        job.usage["input_tokens"] += 100
        return "".join([chunk async for chunk in response.body_iterator])

    result = json.loads(asyncio.run(download()))
    assert result["screening"] == original["screening"]
    assert result["usage"] == original["usage"]
    assert job.downloads == 0


def test_screening_requires_private_complete_valid_source_and_key(client, monkeypatch):
    source = seed_retrieval()
    job = item_review.jobs[source["run_id"]]
    url = f"/api/item-review/runs/{source['run_id']}/screen"
    headers = {"X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY}
    assert client.post(url).status_code == 404
    assert client.post(url, headers={**headers, "X-Review-Token": "wrong"}).status_code == 404
    assert client.post(url, headers={"X-Review-Token": source["run_secret"]}).status_code == 401
    assert client.post(url, headers={**headers, "X-OpenAI-Key": "x" * 513}).status_code == 400
    assert client.post(url, json={"budget": 500}, headers=headers).status_code == 422
    job.finished_at = None
    assert client.post(url, headers=headers).status_code == 409
    job.finished_at = time.monotonic()
    job.status = "cancelled"
    assert client.post(url, headers=headers).status_code == 409
    job.status = "completed"
    job.benchmark_retrieval["rankings"].pop()
    assert client.post(url, headers=headers).status_code == 409
    assert client.post("/api/item-review/runs", json={**BODY, "mode": "screening"}, headers=headers).status_code == 400


@pytest.mark.parametrize("corruption", ["row", "queue", "quote"])
def test_invalid_saved_evidence_fails_before_paid_calls(client, monkeypatch, corruption):
    source = seed_retrieval(facets=1, per_facet=1)
    job = item_review.jobs[source["run_id"]]
    if corruption == "row":
        job.benchmark_retrieval["rankings"][0]["candidates"][0]["evidence"]["item"]["content"] = "changed"
    elif corruption == "queue":
        job.benchmark_retrieval["queues"][0]["item_ids"] = []
    else:
        job.requirements["task_facets"][0]["task"]["evidence"][0]["quote"] = "invented quotation"
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("Invalid source"))
    response = client.post(f"/api/item-review/runs/{source['run_id']}/screen", headers={
        "X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY})
    assert response.status_code == 409


def test_cancel_retains_completed_items_and_continue_finishes_pending(client, monkeypatch):
    source = seed_retrieval(facets=1, per_facet=3)
    monkeypatch.setattr(item_review, "REVIEW_CONCURRENCY", 1)
    mock_screener(monkeypatch)
    real_screener = item_review.AsyncItemScreener
    blocked = Event()

    class PausingScreener(real_screener):
        async def __call__(self, answers, requirements, item):
            if item["id"] == "0-1":
                blocked.set()
                await asyncio.Event().wait()
            return await super().__call__(answers, requirements, item)

    monkeypatch.setattr(item_review, "AsyncItemScreener", PausingScreener)
    first = start_screening(client, source)
    assert blocked.wait(2)
    response = client.post(f"/api/item-review/runs/{first['run_id']}/cancel",
                           headers={"X-Review-Token": first["run_secret"]})
    assert response.json()["status"] == "cancelled"
    assert len(response.json()["screening"]["items"]) == 1
    monkeypatch.setattr(item_review, "AsyncItemScreener", real_screener)
    calls = mock_screener(monkeypatch)
    result = finished(client, start_screening(client, first)).json()
    assert result["status"] == "completed" and len(result["screening"]["items"]) == 3
    assert len(calls) == 2


def test_provider_failure_is_sanitized_and_keeps_completed_items(client, monkeypatch):
    source = seed_retrieval(facets=1, per_facet=3)
    monkeypatch.setattr(item_review, "REVIEW_CONCURRENCY", 1)
    mock_screener(monkeypatch)
    real_screener = item_review.AsyncItemScreener

    class FailingScreener(real_screener):
        async def __call__(self, answers, requirements, item):
            if item["id"] == "0-1":
                raise OpenAIError(f"Private provider text {KEY}")
            return await super().__call__(answers, requirements, item)

    monkeypatch.setattr(item_review, "AsyncItemScreener", FailingScreener)
    access = start_screening(client, source)
    result = finished(client, access)
    assert result.json()["status"] == "failed"
    assert len(result.json()["screening"]["items"]) == 1
    assert "Private provider text" not in result.text and KEY not in export(client, access).text


def test_requests_are_bounded_and_return_to_allocation_order(client, monkeypatch):
    source = seed_retrieval(facets=1, per_facet=8)
    monkeypatch.setattr(item_review, "REVIEW_CONCURRENCY", 3)
    mock_screener(monkeypatch)
    real_screener = item_review.AsyncItemScreener
    running, maximum, completed = 0, 0, []

    class ConcurrentScreener(real_screener):
        async def __call__(self, answers, requirements, item):
            nonlocal running, maximum
            running += 1
            maximum = max(maximum, running)
            try:
                await asyncio.sleep(.03 if item["id"] == "0-0" else .001)
                result = await super().__call__(answers, requirements, item)
                completed.append(item["id"])
                return result
            finally:
                running -= 1

    monkeypatch.setattr(item_review, "AsyncItemScreener", ConcurrentScreener)
    result = finished(client, start_screening(client, source)).json()
    assert maximum == 3 and running == 0 and completed[0] != "0-0"
    assert [item["evidence"]["item"]["id"] for item in result["screening"]["items"]] == [f"0-{i}" for i in range(8)]
