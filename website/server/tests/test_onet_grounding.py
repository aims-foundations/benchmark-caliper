"""Grounding continuation through real HTTP routes and mocked model responses."""

import asyncio
from copy import deepcopy
import json
import time
from threading import Event

import httpx
from openai import AsyncOpenAI, OpenAIError
import pytest

from website.server import item_review
from website.server.tests.test_item_review import (
    BODY, KEY, HF_KEY, client, extracted_requirements, finished,
    mock_extraction_provider, start,
)


CANDIDATE = {
    "doc_id": "activity:teaching", "kind": "activity", "name": "Explain mathematics",
    "text": "Explain mathematical ideas to students.", "occupation_id": "",
    "dense_rank": 1, "bm25_rank": 1, "rrf_score": 2 / 61,
}


@pytest.fixture
def local_index(monkeypatch):
    searches, builds = [], []

    class Index:
        policy = {"scope": "healthcare", "record_count": 1, "fixture": True}

        def __init__(self, materials_dir, cancelled=None):
            builds.append(materials_dir)

        def search(self, query, cancelled=None):
            searches.append(query)
            assert not cancelled()
            return [deepcopy(CANDIDATE)]

    monkeypatch.setattr(item_review, "OnetIndex", Index)
    monkeypatch.setattr(item_review, "_cached_onet_index", None)
    return searches, builds


def seed_requirements(*, facets=1):
    requirements = extracted_requirements(BODY["deployment"])
    requirements["task_facets"] = [
        {**deepcopy(requirements["task_facets"][0]), "facet_id": f"task-{i}"} for i in range(facets)
    ]
    job = item_review.ReviewJob(
        "extraction", "source-secret", "source-owner",
        item_review.ReviewRequest(**BODY, mode="requirements"), inventory={},
        requirements=requirements, extraction={"prompt": "Original extraction prompt"},
        status="completed", finished_at=time.monotonic(),
    )
    item_review.jobs[job.run_id] = job
    return {"run_id": job.run_id, "run_secret": job.secret}


def start_grounding(client, source):
    response = client.post(f"/api/item-review/runs/{source['run_id']}/ground", headers={
        "X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY,
    })
    assert response.status_code == 202, response.text
    assert response.headers["cache-control"] == "no-store"
    return response.json()


def mapping(facet_id):
    return {
        "facet_id": facet_id,
        "records": [{"record_id": CANDIDATE["doc_id"],
                     "supporting_passage": CANDIDATE["text"],
                     "applicability": "partially_applicable",
                     "rationale": "The description supports explanatory wording for this tutoring task.",
                     "search_terms": ["mathematical ideas"]}],
        "refinements": [], "unresolved_details": [],
    }


def response_body(value):
    return {
        "id": "resp_mapping", "object": "response", "created_at": 1, "model": "gpt-6-luna",
        "status": "completed",
        "output": [{"type": "message", "id": "msg_mapping", "status": "completed", "role": "assistant",
                    "content": [{"type": "output_text", "text": json.dumps(value), "annotations": []}]}],
        "usage": {"input_tokens": 100, "output_tokens": 90, "total_tokens": 190,
                  "input_tokens_details": {"cached_tokens": 10},
                  "output_tokens_details": {"reasoning_tokens": 30}},
    }


def mock_mapper(monkeypatch, transform=lambda value: value):
    requests = []

    def respond(request):
        body = json.loads(request.content)
        requests.append(body)
        data = json.loads(body["input"])
        return httpx.Response(200, json=response_body(transform(mapping(data["facet"]["facet_id"]))))

    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: AsyncOpenAI(
        **kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))))
    return requests


def test_grounding_continues_exact_extraction_without_dataset_and_exports(client, monkeypatch, local_index):
    answers = {**BODY["deployment"], "task": " \nA mathematics tutor for secondary school.\t "}
    expected = extracted_requirements(answers)
    extraction_calls = mock_extraction_provider(monkeypatch, expected)
    source = start(client, {"deployment": answers, "mode": "requirements"})
    original = finished(client, source).json()
    requests = mock_mapper(monkeypatch)
    monkeypatch.setattr(item_review, "get_token", lambda: pytest.fail("No dataset access needed"))
    monkeypatch.setattr(item_review, "inventory", lambda: pytest.fail("No benchmark inventory needed"))
    monkeypatch.setattr(item_review, "AsyncRequirementExtractor", lambda *a: pytest.fail("Do not repeat extraction"))
    monkeypatch.setattr(item_review, "review_items", lambda *a: pytest.fail("No item retrieval"))
    access = start_grounding(client, source)
    result = finished(client, access).json()
    assert result["status"] == "completed" and result["mode"] == "grounding"
    assert result["source_run_id"] == source["run_id"]
    assert result["deployment"] == answers and result["requirements"] == expected
    assert result["extraction"] == original["extraction"]
    assert len(extraction_calls) == len(requests) == 1
    provider_input = json.loads(requests[0]["input"])
    assert provider_input["answers"] == answers
    assert provider_input["requirements"] == expected
    assert provider_input["facet"] == expected["task_facets"][0]
    assert provider_input["candidates"][0]["doc_id"] == CANDIDATE["doc_id"]
    assert result["grounding"]["mapping"]["prompt"] == requests[0]["instructions"]
    assert result["grounding"]["mapping"]["output_schema"] == requests[0]["text"]["format"]["schema"]
    facet, = result["grounding"]["facets"]
    assert facet["mapping"] == mapping("tutoring")
    assert facet["candidates"] == [CANDIDATE]
    assert facet["query"] == local_index[0][0]
    assert result["usage"]["output_tokens"] == 90
    assert finished(client, source).json() == original
    url = f"/api/item-review/runs/{access['run_id']}/export"
    assert client.get(url).status_code == 404
    exported = client.get(url, headers={"X-Review-Token": access["run_secret"]})
    assert exported.json() == result
    assert "onet-grounding-" in exported.headers["content-disposition"]
    for secret in (KEY, HF_KEY, source["run_secret"], access["run_secret"]):
        assert secret not in exported.text


def test_grounding_requires_source_access_key_and_finished_facets(client, monkeypatch):
    source = seed_requirements()
    url = f"/api/item-review/runs/{source['run_id']}/ground"
    headers = {"X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY}
    assert client.post(url, headers={"X-OpenAI-Key": KEY}).status_code == 404
    assert client.post(url, headers={**headers, "X-Review-Token": "wrong"}).status_code == 404
    assert client.post(url, headers={"X-Review-Token": source["run_secret"]}).status_code == 401
    assert client.post(url, headers={**headers, "X-OpenAI-Key": "x" * 513}).status_code == 400
    job = item_review.jobs[source["run_id"]]
    job.finished_at = None
    assert client.post(url, headers=headers).status_code == 409
    job.finished_at = time.monotonic()
    job.requirements["task_facets"] = []
    assert client.post(url, headers=headers).status_code == 409
    assert client.post("/api/item-review/runs", json={**BODY, "mode": "grounding"},
                       headers={"X-OpenAI-Key": KEY}).status_code == 400
    job.finished_at = time.monotonic() - item_review.RETENTION_SECONDS - 1
    # Pausing no longer removes the run; the invalid empty facets still block grounding.
    assert client.post(url, headers=headers).status_code == 409


def test_no_applicable_records_is_successful_and_keeps_requirements(client, monkeypatch, local_index):
    source = seed_requirements()
    def no_match(value):
        value["records"] = []
        value["unresolved_details"] = ["No candidate supports this task in the supplied healthcare catalog."]
        return value
    mock_mapper(monkeypatch, no_match)
    result = finished(client, start_grounding(client, source)).json()
    assert result["status"] == "completed"
    assert result["grounding"]["facets"][0]["mapping"]["records"] == []
    assert result["requirements"] == item_review.jobs[source["run_id"]].requirements


@pytest.mark.parametrize("field,value", [("record_id", "unknown"), ("supporting_passage", "invented passage"),
                                         ("search_terms", ["invented duty"])])
def test_invalid_mapping_fails_closed_without_more_calls(client, monkeypatch, local_index, field, value):
    source = seed_requirements(facets=2)
    def corrupt(result):
        result["records"][0][field] = value
        return result
    requests = mock_mapper(monkeypatch, corrupt)
    result = finished(client, start_grounding(client, source)).json()
    assert result["status"] == "failed"
    assert len(requests) == 1
    facet, = result["grounding"]["facets"]
    assert facet["status"] == "error" and facet["mapping"] is None
    assert "invented" not in json.dumps(result)
    assert result["requirements"] == item_review.jobs[source["run_id"]].requirements


def test_local_retrieval_failure_prevents_mapping_and_hides_exception(client, monkeypatch):
    source = seed_requirements()
    def broken(**kwargs):
        raise ValueError(f"Bad local data {KEY}")
    monkeypatch.setattr(item_review, "_cached_onet_index", None)
    monkeypatch.setattr(item_review, "OnetIndex", broken)
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kw: pytest.fail("No client before retrieval succeeds"))
    response = finished(client, start_grounding(client, source))
    assert response.json()["status"] == "failed"
    assert response.json()["grounding"] is None
    assert KEY not in response.text


def test_index_reused_but_queries_and_mappings_remain_per_run(client, monkeypatch, local_index):
    source = seed_requirements()
    calls = mock_mapper(monkeypatch)
    first = start_grounding(client, source)
    assert finished(client, first).json()["status"] == "completed"
    second = start_grounding(client, first)
    assert finished(client, second).json()["status"] == "completed"
    assert len(local_index[1]) == 1 and len(local_index[0]) == len(calls) == 2
    assert second["run_id"] != first["run_id"]


def test_cancel_local_search_reaches_worker_without_paid_calls(client, monkeypatch):
    source = seed_requirements()
    entered = Event()
    class SlowIndex:
        def __init__(self, materials_dir, cancelled):
            entered.set()
            deadline = time.monotonic() + 3
            while not cancelled() and time.monotonic() < deadline:
                time.sleep(.01)
            assert cancelled(), "Cancellation did not reach O*NET loader"
            raise InterruptedError("Cancelled")
    monkeypatch.setattr(item_review, "_cached_onet_index", None)
    monkeypatch.setattr(item_review, "OnetIndex", SlowIndex)
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kw: pytest.fail("No provider during retrieval"))
    access = start_grounding(client, source)
    assert entered.wait(2)
    stopped = client.post(f"/api/item-review/runs/{access['run_id']}/cancel",
                          headers={"X-Review-Token": access["run_secret"]})
    assert stopped.json()["status"] == "cancelled"
    assert stopped.json()["requirements"] == item_review.jobs[source["run_id"]].requirements


def test_cancel_mapping_preserves_completed_facets_and_blocks_duplicate_run(client, monkeypatch, local_index):
    source = seed_requirements(facets=2)
    entered, stopped = Event(), Event()
    calls = []
    async def respond(request):
        data = json.loads(json.loads(request.content)["input"])
        calls.append(data)
        if len(calls) == 1:
            return httpx.Response(200, json=response_body(mapping(data["facet"]["facet_id"])))
        entered.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            stopped.set()
            raise
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: AsyncOpenAI(
        **kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))))
    access = start_grounding(client, source)
    assert entered.wait(2)
    duplicate = client.post(f"/api/item-review/runs/{source['run_id']}/ground", headers={
        "X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY})
    assert duplicate.status_code == 429
    result = client.post(f"/api/item-review/runs/{access['run_id']}/cancel",
                         headers={"X-Review-Token": access["run_secret"]}).json()
    assert stopped.is_set() and result["status"] == "cancelled"
    facet, = result["grounding"]["facets"]
    assert facet["mapping"] == mapping("task-0")
    assert result["usage"]["output_tokens"] == 90


def test_mapping_provider_error_keeps_completed_results_and_hides_key(client, monkeypatch, local_index):
    source = seed_requirements(facets=2)
    calls = []
    async def respond(request):
        data = json.loads(json.loads(request.content)["input"])
        calls.append(data)
        if len(calls) == 2:
            raise OpenAIError(f"Provider failure {KEY}")
        return httpx.Response(200, json=response_body(mapping(data["facet"]["facet_id"])))
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: AsyncOpenAI(
        **{**kwargs, "max_retries": 0}, http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))))
    response = finished(client, start_grounding(client, source))
    result = response.json()
    assert result["status"] == "failed" and len(result["grounding"]["facets"]) == 1
    assert KEY not in response.text
