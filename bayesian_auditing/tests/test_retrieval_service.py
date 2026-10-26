"""Offline contract, lifecycle, and prepared-cache checks for remote retrieval."""

from copy import deepcopy
import json
import sqlite3
import sys
from threading import Event, get_ident
import time
from types import SimpleNamespace

from fastapi.testclient import TestClient
import pytest

from bayesian_auditing import retrieval_service as service
from bayesian_auditing.data import fingerprint


TOKEN = "offline-test-secret-" + "a" * 32
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
INVENTORY = {"repo": "test/bank", "branches": {"main": "fixed-commit"}, "tables": []}
INVENTORY_HASH = fingerprint(INVENTORY)


class FakeResources:
    inventory_hash = INVENTORY_HASH

    def __init__(self, search=None):
        self.thread = get_ident()
        self.closed = False
        self.calls = []
        self.search_impl = search

    def health(self):
        return {"ready": True, "inventory_hash": self.inventory_hash,
                "stats": {"indexed_items": 3}, "onet": {"records": 2}}

    def search(self, request, cancelled):
        assert get_ident() == self.thread
        self.calls.append(request)
        if self.search_impl is not None:
            return self.search_impl(request, cancelled)
        result = {"candidates": [{"original_row": {"arbitrary_field": "preserved"}}],
                  "policy": {"method": "bge_bm25_rrf"}}
        if request.kind == "benchmark":
            result.update(stats={"indexed_items": 3}, inventory_hash=self.inventory_hash)
        return result

    def close(self):
        assert get_ident() == self.thread
        self.closed = True


def make_app(search=None, **options):
    resources = []

    def factory():
        value = FakeResources(search)
        resources.append(value)
        return value

    return service.create_app(token=TOKEN, resource_factory=factory, **options), resources


def submit(client, *, kind="onet", query="clinical documentation", **extra):
    if kind == "benchmark":
        extra.setdefault("inventory_hash", INVENTORY_HASH)
    return client.post("/v1/searches", json={"kind": kind, "query": query, **extra}, headers=HEADERS)


def wait_for(client, job_id, status="completed"):
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        response = client.get(f"/v1/searches/{job_id}", headers=HEADERS)
        assert response.status_code == 200, response.text
        job = response.json()
        if job["status"] == status:
            return job
        if job["status"] in {"failed", "cancelled", "completed"}:
            pytest.fail(f"Unexpected terminal search status: {job}")
        time.sleep(0.005)
    pytest.fail(f"Search did not reach {status}")


def test_authentication_is_required_on_every_endpoint():
    app, _ = make_app()
    with TestClient(app) as client:
        for method, path, kwargs in (
            ("get", "/healthz", {}),
            ("post", "/v1/searches", {"json": {"kind": "onet", "query": "query"}}),
            ("get", "/v1/searches/unknown", {}),
            ("delete", "/v1/searches/unknown", {}),
        ):
            for headers in ({}, {"Authorization": "Bearer wrong"}):
                response = getattr(client, method)(path, headers=headers, **kwargs)
                assert response.status_code == 401
                assert response.headers["www-authenticate"] == "Bearer"
                assert response.headers["cache-control"] == "no-store"
        health = client.get("/healthz", headers=HEADERS)
        assert health.json()["ready"] is True
        assert health.headers["cache-control"] == "no-store"
        assert client.get("/docs").status_code == 404


@pytest.mark.parametrize("token", [None, "short"])
def test_startup_requires_a_nontrivial_secret(monkeypatch, token):
    monkeypatch.delenv("RETRIEVAL_SERVICE_TOKEN", raising=False)
    app = service.create_app(token=token, resource_factory=lambda: pytest.fail("Must reject before loading"))
    with pytest.raises(RuntimeError, match="at least 32"):
        with TestClient(app):
            pass


def test_inventory_mismatch_and_invalid_requests_never_search():
    app, resources = make_app()
    with TestClient(app) as client:
        assert submit(client, kind="benchmark", inventory_hash="different").status_code == 409
        for body in (
            {"kind": "benchmark", "query": "query"},
            {"kind": "onet", "query": "  "},
            {"kind": "other", "query": "query"},
            {"kind": "onet", "query": "query", "dense_k": 1},
        ):
            assert client.post("/v1/searches", json=body, headers=HEADERS).status_code == 422
        assert resources[0].calls == []


@pytest.mark.parametrize("kind", ["onet", "benchmark"])
def test_results_preserve_index_output_and_delete_releases_capacity(kind):
    app, resources = make_app(max_jobs=1)
    with TestClient(app) as client:
        response = submit(client, kind=kind)
        assert response.status_code == 202
        job_id = response.json()["job_id"]
        job = wait_for(client, job_id)
        assert job["result"]["candidates"][0]["original_row"] == {"arbitrary_field": "preserved"}
        assert job["result"]["policy"] == {"method": "bge_bm25_rrf"}
        if kind == "benchmark":
            assert job["result"]["inventory_hash"] == INVENTORY_HASH
            assert job["result"]["stats"]["indexed_items"] == 3
        assert app.state.searches.retained_bytes > 0
        assert submit(client).status_code == 429
        assert client.delete(f"/v1/searches/{job_id}", headers=HEADERS).json()["status"] == "cancelled"
        assert app.state.searches.retained_bytes == 0
        assert client.get(f"/v1/searches/{job_id}", headers=HEADERS).status_code == 404
        assert submit(client).status_code == 202
    assert resources[0].closed


def test_searches_are_serialized_and_running_cancellation_reaches_index():
    entered, cancelled_seen = Event(), Event()

    def blocking(request, cancelled):
        if request.query == "first":
            entered.set()
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if cancelled():
                    cancelled_seen.set()
                    raise InterruptedError("cancelled")
                time.sleep(0.005)
            pytest.fail("Running search was not cancelled")
        return {"candidates": [], "policy": {}}

    app, resources = make_app(blocking, max_queued=1)
    with TestClient(app) as client:
        first = submit(client, query="first").json()["job_id"]
        assert entered.wait(2)
        second = submit(client, query="second").json()["job_id"]
        assert client.get(f"/v1/searches/{second}", headers=HEADERS).json()["status"] == "queued"
        assert submit(client, query="third").status_code == 429
        assert [call.query for call in resources[0].calls] == ["first"]
        assert client.delete(f"/v1/searches/{first}", headers=HEADERS).status_code == 200
        assert cancelled_seen.wait(2)
        wait_for(client, second)
        assert [call.query for call in resources[0].calls] == ["first", "second"]


def test_shutdown_cancels_running_and_skips_queued_work():
    entered, cancelled_seen = Event(), Event()

    def blocking(request, cancelled):
        entered.set()
        while not cancelled():
            time.sleep(0.005)
        cancelled_seen.set()
        raise InterruptedError("shutdown")

    app, resources = make_app(blocking)
    with TestClient(app) as client:
        submit(client, query="first")
        assert entered.wait(2)
        submit(client, query="never started")
    assert cancelled_seen.is_set()
    assert resources[0].closed
    assert [call.query for call in resources[0].calls] == ["first"]


def test_job_expiry_releases_results_and_capacity():
    now = [100.0]
    app, _ = make_app(max_jobs=1, ttl_seconds=30, clock=lambda: now[0])
    with TestClient(app) as client:
        job_id = submit(client).json()["job_id"]
        wait_for(client, job_id)
        now[0] += 31
        assert client.get(f"/v1/searches/{job_id}", headers=HEADERS).status_code == 404
        assert app.state.searches.retained_bytes == 0
        assert submit(client).status_code == 202


def test_worker_recovers_after_search_error_without_exposing_credentials(caplog):
    def search(request, cancelled):
        if request.query == "broken":
            raise ValueError("Download failed: https://host/file?token=private-credential")
        return {"candidates": [], "policy": {}}

    app, _ = make_app(search)
    with TestClient(app) as client:
        failed = submit(client, query="broken").json()["job_id"]
        error = wait_for(client, failed, "failed")["error"]
        assert "ValueError" in error
        assert failed in error
        assert "private-credential" not in error + caplog.text
        good = submit(client, query="good").json()["job_id"]
        wait_for(client, good)


def test_oversized_results_fail_without_being_retained():
    app, _ = make_app(max_result_bytes=10)
    with TestClient(app) as client:
        job_id = submit(client).json()["job_id"]
        result = wait_for(client, job_id, "failed")
        assert "retention limit" in result["error"]
        assert "result" not in result
        assert app.state.searches.retained_bytes == 0


def test_total_retained_result_limit_is_released_after_delete():
    app, _ = make_app(max_retained_bytes=200)
    with TestClient(app) as client:
        first = submit(client).json()["job_id"]
        wait_for(client, first)
        second = submit(client).json()["job_id"]
        assert "memory limit" in wait_for(client, second, "failed")["error"]
        client.delete(f"/v1/searches/{first}", headers=HEADERS)
        third = submit(client).json()["job_id"]
        wait_for(client, third)


@pytest.fixture
def prepared_metadata(tmp_path, monkeypatch):
    path = tmp_path / "prepared.sqlite3"
    policy = service._policy(None)
    metadata = {"complete": True, "inventory": INVENTORY, "policy": policy,
                "stats": {"indexed_items": 3},
                "cache_key": fingerprint({"inventory": INVENTORY, "policy": policy})}

    def write(changes=None):
        values = deepcopy(metadata)
        values.update(changes or {})
        with sqlite3.connect(path) as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT)")
            connection.execute("DELETE FROM metadata")
            connection.executemany("INSERT INTO metadata VALUES (?, ?)",
                                   [(key, json.dumps(value)) for key, value in values.items()])

    monkeypatch.setenv("RETRIEVAL_BENCHMARK_INDEX", str(path))
    monkeypatch.setitem(sys.modules, "torch", SimpleNamespace(set_num_threads=lambda n: None))
    write()
    return path, write, metadata


@pytest.mark.parametrize("changes, message", [
    ({"complete": False}, "incomplete"),
    ({"policy": {"version": -1}}, "policy"),
    ({"cache_key": "wrong"}, "identity"),
    ({"inventory": {"repo": "wrong/bank"}}, "identity"),
])
def test_resources_reject_mismatched_or_incomplete_indexes(prepared_metadata, monkeypatch, changes, message):
    _, write, _ = prepared_metadata
    write(changes)
    monkeypatch.setattr(service, "BenchmarkIndex", lambda *a, **kw: pytest.fail("Must reject before opening"))
    with pytest.raises(ValueError, match=message):
        service.PreparedResources()


def test_missing_prepared_index_fails_without_creating_a_file(tmp_path, monkeypatch):
    path = tmp_path / "absent.sqlite3"
    monkeypatch.setenv("RETRIEVAL_BENCHMARK_INDEX", str(path))
    with pytest.raises(FileNotFoundError):
        service.PreparedResources()
    assert not path.exists()


def test_prepared_resources_use_cpu_and_preserve_pinned_identity(prepared_metadata, monkeypatch):
    path, _, _ = prepared_metadata
    before = path.read_bytes()
    opened = []

    def benchmark(actual_path, *, encoder):
        assert actual_path == path
        assert encoder.device == "cpu"
        index = SimpleNamespace(stats={"indexed_items": 3}, close=lambda: None)
        opened.append(index)
        return index

    onet = SimpleNamespace(_encoder=SimpleNamespace(device=None), policy={"record_count": 2})
    monkeypatch.setattr(service, "BenchmarkIndex", benchmark)
    monkeypatch.setattr(service, "OnetIndex", lambda **kwargs: onet)
    resources = service.PreparedResources()
    assert resources.inventory_hash == INVENTORY_HASH
    assert resources.health()["stats"]["indexed_items"] == 3
    assert onet._encoder.device == "cpu"
    assert len(opened) == 1
    resources.close()
    assert path.read_bytes() == before
