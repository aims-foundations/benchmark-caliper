"""Remote retrieval preserves evidence and avoids loading models on Render."""

import asyncio
from copy import deepcopy
import gzip
import json

import httpx
import pytest

from bayesian_auditing.benchmark_data import row_fingerprint, row_search_text
from bayesian_auditing.benchmark_index import _policy
from bayesian_auditing.benchmark_queries import build_screening_queues
from bayesian_auditing.data import fingerprint
from bayesian_auditing.onet import MODEL_ID, MODEL_REVISION
from website.server import item_review, remote_retrieval
from website.server.remote_retrieval import RemoteRetrieval, RemoteRetrievalError
from website.server.tests.test_item_review import client, finished, KEY, HF_KEY
from website.server.tests.test_onet_grounding import (
    CANDIDATE, mock_mapper, seed_requirements, start_grounding,
)
from website.server.tests.test_benchmark_retrieval import seed_grounding, start_retrieval, export


URL = "https://retrieval.private.invalid"
TOKEN = "test-shared-retrieval-secret"
INVENTORY = {
    "repo": "fixture", "branches": {"main": "pinned"}, "missing_item_tables": [],
    "tables": [{"benchmark": "math", "branch": "main", "commit": "pinned",
                "items_path": "math/items.parquet", "row_count": 1}],
}


def onet_result():
    return {"candidates": [deepcopy(CANDIDATE)], "policy": {
        "method": "bge_bm25_rrf", "candidate_limits": {"dense_k": 50, "bm25_k": 50, "limit": 20},
        "embedding": {"model": MODEL_ID, "revision": MODEL_REVISION},
    }}


def benchmark_result():
    row = {"content": "Explain a mathematical idea.", "grading_criterion": "Correct explanation.",
           "nested": {"unchanged": [1, None, "\t a\n"]}}
    item_id = row_fingerprint(row)
    candidate = {
        "item_id": item_id, "evidence_hash": item_id, "evidence": {"item": row},
        "sources": [{"repo": "fixture", "branch": "main", "commit": "pinned",
                     "benchmark": "math", "items_path": "math/items.parquet", "row": 1, "item_id": None}],
        "rank": 1, "dense_rank": 1, "bm25_rank": 1, "dense_score": .8,
        "bm25_score": .1, "rrf_score": 2 / 61, "search_text": row_search_text(row),
        "question_text": row["content"],
    }
    return {"candidates": [candidate], "policy": _policy(None),
            "stats": {"source_rows": 1, "indexed_items": 1, "cache_hit": True},
            "inventory_hash": fingerprint(INVENTORY)}


@pytest.fixture
def configured(monkeypatch):
    monkeypatch.setenv("ITEM_REVIEW_RETRIEVAL_URL", URL)
    monkeypatch.setenv("ITEM_REVIEW_RETRIEVAL_TOKEN", TOKEN)
    monkeypatch.setattr(remote_retrieval, "POLL_SECONDS", .001)
    return RemoteRetrieval.from_environment()


def mock_remote(monkeypatch, respond):
    original = httpx.AsyncClient

    class Client(original):
        def __init__(self, **kwargs):
            if str(kwargs.get("base_url", "")).startswith(URL):
                kwargs["transport"] = httpx.MockTransport(respond)
            super().__init__(**kwargs)

    monkeypatch.setattr(remote_retrieval.httpx, "AsyncClient", Client)


def successful_service(monkeypatch, result_factory, *, compressed=False):
    requests, submitted = [], {}

    def respond(request):
        requests.append(request)
        assert request.headers["authorization"] == f"Bearer {TOKEN}"
        if request.method == "POST":
            body = json.loads(request.content)
            job_id = f"search-{len(submitted)}"
            submitted[job_id] = body
            return httpx.Response(202, json={"job_id": job_id, "status": "queued"})
        if request.method == "DELETE":
            return httpx.Response(200, json={"status": "cancelled"})
        body = {"status": "completed", "result": result_factory()}
        if compressed:
            return httpx.Response(200, content=gzip.compress(json.dumps(body, ensure_ascii=False).encode("utf-8")),
                                  headers={"Content-Encoding": "gzip", "Content-Type": "application/json"})
        return httpx.Response(200, json=body)

    mock_remote(monkeypatch, respond)
    return requests, submitted


@pytest.mark.parametrize("url", ["https://service.example", "http://127.0.0.1:8001", "http://[::1]:8001", "http://localhost:8001"])
def test_valid_service_addresses(monkeypatch, url):
    monkeypatch.setenv("ITEM_REVIEW_RETRIEVAL_URL", url)
    monkeypatch.setenv("ITEM_REVIEW_RETRIEVAL_TOKEN", TOKEN)
    assert RemoteRetrieval.from_environment().url == url


@pytest.mark.parametrize("url,token", [
    ("http://service.example", TOKEN), ("https://user:password@service.example", TOKEN),
    ("https://service.example?token=secret", TOKEN), ("https://service.example/#secret", TOKEN),
    ("https://service.example:bad", TOKEN), (URL, ""), ("", TOKEN),
])
def test_invalid_or_incomplete_configuration_fails_closed(monkeypatch, url, token):
    monkeypatch.setenv("ITEM_REVIEW_RETRIEVAL_URL", url)
    monkeypatch.setenv("ITEM_REVIEW_RETRIEVAL_TOKEN", token)
    with pytest.raises(RemoteRetrievalError) as error:
        RemoteRetrieval.from_environment()
    assert TOKEN not in str(error.value) and URL not in str(error.value)


def test_no_configuration_keeps_local_path(monkeypatch):
    monkeypatch.delenv("ITEM_REVIEW_RETRIEVAL_URL", raising=False)
    monkeypatch.delenv("ITEM_REVIEW_RETRIEVAL_TOKEN", raising=False)
    assert RemoteRetrieval.from_environment() is None


@pytest.mark.parametrize("compressed", [False, True])
def test_remote_benchmark_preserves_exports_queues_and_full_rows(client, monkeypatch, configured, compressed):
    monkeypatch.setattr(item_review, "inventory", lambda: deepcopy(INVENTORY))
    for name in ("prepare_benchmark_index", "iter_benchmark_items", "fetch_benchmark_rows", "OnetIndex"):
        monkeypatch.setattr(item_review, name, lambda *a, **kw: pytest.fail("Remote mode must not load local retrieval data"))
    requests, submitted = successful_service(monkeypatch, benchmark_result, compressed=compressed)
    source = seed_grounding(facets=2)
    access = start_retrieval(client, source)
    result = finished(client, access).json()
    assert result["status"] == "completed"
    retrieval = export(client, access).json()["retrieval"]
    expected = benchmark_result()
    assert retrieval["policy"] == expected["policy"]
    assert retrieval["stats"] == expected["stats"]
    assert retrieval["inventory"] == INVENTORY
    assert len(retrieval["rankings"]) == 2
    assert all(ranking["candidates"] == expected["candidates"] for ranking in retrieval["rankings"])
    assert retrieval["queues"] == build_screening_queues(retrieval["rankings"])
    assert [body["query"] for body in submitted.values()] == [query["query"] for query in retrieval["queries"]]
    assert all(set(body) == {"kind", "query", "inventory_hash"} and body["inventory_hash"] == fingerprint(INVENTORY)
               for body in submitted.values())
    assert sum(request.method == "DELETE" for request in requests) == 2
    for secret in (URL, TOKEN, KEY, HF_KEY):
        assert secret not in json.dumps(result)
        assert secret not in json.dumps(list(submitted.values()))
    catalog = client.get("/api/item-review/catalog").json()
    assert catalog["retrieval_mode"] == "remote" and URL not in json.dumps(catalog)


def test_remote_onet_reaches_mapper_with_original_evidence(client, monkeypatch, configured):
    monkeypatch.setattr(item_review, "OnetIndex", lambda *a, **kw: pytest.fail("Must not load local O*NET"))
    requests, submitted = successful_service(monkeypatch, onet_result)
    mapper_requests = mock_mapper(monkeypatch)
    access = start_grounding(client, seed_requirements(facets=2))
    result = finished(client, access).json()
    assert result["status"] == "completed"
    assert result["grounding"]["retrieval"] == onet_result()["policy"]
    assert len(mapper_requests) == len(submitted) == 2
    assert all(json.loads(request["input"])["candidates"] == [CANDIDATE] for request in mapper_requests)
    assert all(set(body) == {"kind", "query"} and body["kind"] == "onet" for body in submitted.values())
    assert sum(request.method == "DELETE" for request in requests) == 2


@pytest.mark.parametrize("status,expected", [(401, "authentication"), (409, "pinned item bank"), (429, "busy"), (503, "unavailable")])
def test_remote_http_errors_are_safe_and_actionable(monkeypatch, configured, status, expected):
    mock_remote(monkeypatch, lambda request: httpx.Response(status, text=f"Private error {URL} {TOKEN}"))
    with pytest.raises(RemoteRetrievalError, match=expected) as error:
        asyncio.run(configured.search("onet", "private query"))
    assert URL not in str(error.value) and TOKEN not in str(error.value)


def test_remote_failure_has_no_local_fallback(client, monkeypatch, configured):
    monkeypatch.setattr(item_review, "inventory", lambda: deepcopy(INVENTORY))
    monkeypatch.setattr(item_review, "prepare_benchmark_index", lambda *a, **kw: pytest.fail("Must not fall back"))
    mock_remote(monkeypatch, lambda request: httpx.Response(503, text="private server details"))
    result = finished(client, start_retrieval(client, seed_grounding())).json()
    assert result["status"] == "failed" and "retrieval server is unavailable" in result["message"]
    assert "private server details" not in result["message"]


def test_remote_job_error_is_redacted_and_released(monkeypatch, configured):
    requests = []

    def respond(request):
        requests.append(request.method)
        if request.method == "POST":
            return httpx.Response(202, json={"job_id": "failed", "status": "queued"})
        return httpx.Response(200, json={"status": "failed", "error": f"private query {URL} {TOKEN}"})

    mock_remote(monkeypatch, respond)
    with pytest.raises(RemoteRetrievalError, match="could not complete") as error:
        asyncio.run(configured.search("onet", "private query"))
    assert requests[-1] == "DELETE"
    assert all(secret not in str(error.value) for secret in (URL, TOKEN, "private query"))


def test_remote_network_error_is_redacted(monkeypatch, configured):
    def respond(request):
        raise httpx.ConnectError(f"Cannot connect to {URL} with {TOKEN}", request=request)

    mock_remote(monkeypatch, respond)
    with pytest.raises(RemoteRetrievalError, match="Could not reach") as error:
        asyncio.run(configured.search("onet", "private query"))
    assert URL not in str(error.value) and TOKEN not in str(error.value)


@pytest.mark.parametrize("mutation", [
    lambda value: value.update(inventory_hash="different"),
    lambda value: value["candidates"][0]["evidence"]["item"].pop("nested"),
    lambda value: value["candidates"][0]["sources"][0].update(commit="different"),
    lambda value: value["candidates"][0]["sources"][0].update(row=0),
    lambda value: value["candidates"].clear(),
    lambda value: value["policy"]["candidate_limits"].update(dense_k=20),
    lambda value: value.pop("candidates"),
])
def test_incompatible_or_incomplete_evidence_is_rejected_and_released(monkeypatch, configured, mutation):
    result = benchmark_result()
    mutation(result)
    requests, _ = successful_service(monkeypatch, lambda: result)
    with pytest.raises(RemoteRetrievalError, match="incomplete or incompatible"):
        asyncio.run(configured.search("benchmark", "a task", inventory=INVENTORY))
    assert requests[-1].method == "DELETE"


@pytest.mark.parametrize("during_submission", [False, True])
def test_cancellation_cleans_up_even_during_submission(monkeypatch, configured, during_submission):
    async def scenario():
        entered, release = asyncio.Event(), asyncio.Event()
        requests = []

        async def respond(request):
            requests.append(request.method)
            if request.method == "POST":
                if during_submission:
                    entered.set()
                    await release.wait()
                return httpx.Response(202, json={"job_id": "active", "status": "queued"})
            if request.method == "GET":
                entered.set()
                return httpx.Response(200, json={"status": "running"})
            return httpx.Response(200, json={"status": "cancelled"})

        mock_remote(monkeypatch, respond)
        task = asyncio.create_task(configured.search("onet", "a private task"))
        await entered.wait()
        task.cancel()
        release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert requests[-1] == "DELETE"

    asyncio.run(scenario())


def test_overall_timeout_cancels_remote_job(monkeypatch, configured):
    requests = []

    def respond(request):
        requests.append(request.method)
        if request.method == "POST":
            return httpx.Response(202, json={"job_id": "active", "status": "queued"})
        return httpx.Response(200, json={"status": "running"})

    mock_remote(monkeypatch, respond)
    monkeypatch.setattr(remote_retrieval, "SEARCH_TIMEOUT_SECONDS", .01)
    with pytest.raises(RemoteRetrievalError, match="timed out"):
        asyncio.run(configured.search("onet", "a private task"))
    assert requests[-1] == "DELETE"
