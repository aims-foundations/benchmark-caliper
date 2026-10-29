"""Private, consistent result packages and usage provenance over HTTP."""

import asyncio
from copy import deepcopy
from datetime import datetime
from io import BytesIO
import json
from threading import Event
import time
from zipfile import ZipFile

import pytest
from starlette.requests import ClientDisconnect

from website.server import item_review
from website.server.tests.test_item_review import (
    BODY, KEY, HF_KEY, client, extracted_requirements, finished, mock_extraction_provider, start,
)
from website.server.tests.test_onet_grounding import seed_requirements
from website.server.tests.test_benchmark_retrieval import seed_grounding
from website.server.tests.test_benchmark_screening import seed_retrieval
from website.server.tests.test_benchmark_selection import seed_screening
from website.server.tests.test_adaptive_screening import seed_selected


def download(client, access):
    return client.get(f"/api/item-review/runs/{access['run_id']}/package",
                      headers={"X-Review-Token": access["run_secret"]})


def unpack(response):
    assert response.status_code == 200, response.text if response.status_code != 200 else ""
    with ZipFile(BytesIO(response.content)) as archive:
        assert set(archive.namelist()) == {"report.html", "selected_items.csv", "results.json"}
        return json.loads(archive.read("results.json")), archive.read("report.html").decode()


def test_package_preserves_full_selection_evidence_and_private_access(client, monkeypatch):
    access = seed_selected(per_facet=3)
    job = item_review.jobs[access["run_id"]]
    job.request = job.request.model_copy(update={"run_name": "Algebra example"})
    for name in ("AsyncOpenAI", "get_token", "inventory"):
        monkeypatch.setattr(item_review, name, lambda *a, **kw: pytest.fail("Export is local"))
    url = f"/api/item-review/runs/{job.run_id}/package"
    assert client.get(url).status_code == 404
    assert client.get(url, headers={"X-Review-Token": "wrong"}).status_code == 404
    response = download(client, access)
    snapshot, report = unpack(response)
    assert response.headers["content-type"] == "application/zip"
    assert response.headers["cache-control"] == "no-store"
    assert "algebra-example" in response.headers["content-disposition"].lower()
    assert snapshot["retrieval"] == job.benchmark_retrieval
    assert snapshot["screening"] == job.screening
    assert snapshot["selection"] == job.selection
    assert snapshot["metadata"]["run_name"] == "Algebra example"
    assert snapshot["metadata"]["result_state"] == "stage_complete"
    assert datetime.fromisoformat(snapshot["metadata"]["exported_at"]).tzinfo is not None
    assert job.downloads == 0
    for secret in (KEY, HF_KEY, access["run_secret"]):
        assert secret not in json.dumps(snapshot) + report
    job.finished_at = time.monotonic() - item_review.RETENTION_SECONDS - 1
    assert download(client, access).status_code == 200


def test_package_expands_stored_evidence_without_changing_saved_compact_results(client, monkeypatch):
    access = seed_selected(per_facet=3)
    job = item_review.jobs[access["run_id"]]
    retrieval, screening = deepcopy(job.benchmark_retrieval), deepcopy(job.screening)
    store = item_review.candidate_store()
    for ranking in job.benchmark_retrieval["rankings"]:
        ranking["candidates"] = [store.compact(item) for item in ranking["candidates"]]
    job.screening["items"] = [store.compact(item) for item in job.screening["items"]]
    compact_retrieval, compact_screening = deepcopy(job.benchmark_retrieval), deepcopy(job.screening)
    for name in ("AsyncOpenAI", "get_token", "inventory"):
        monkeypatch.setattr(item_review, name, lambda *a, **kw: pytest.fail("Export is local"))

    snapshot, report = unpack(download(client, access))
    assert snapshot["retrieval"] == retrieval
    assert snapshot["screening"] == screening
    assert snapshot["selection"] == job.selection
    assert "extra_original_column" in report
    assert "_candidate_ref" not in json.dumps(snapshot) + report
    assert str(store.directory) not in json.dumps(snapshot) + report
    assert job.benchmark_retrieval == compact_retrieval
    assert job.screening == compact_screening
    assert job.downloads == 0


@pytest.mark.parametrize("status", ["preparing", "running", "failed", "cancelled"])
def test_unfinished_requirement_packages_are_explicit_partial_snapshots(client, status):
    access = seed_requirements()
    job = item_review.jobs[access["run_id"]]
    job.status, job.requirements = status, None
    snapshot, report = unpack(download(client, access))
    assert snapshot["metadata"]["result_state"] == "partial"
    assert "partial" in report.lower()
    assert snapshot["requirements"] is None
    assert "selection" not in snapshot


def test_initial_run_records_name_dates_and_extraction_usage(client, monkeypatch):
    mock_extraction_provider(monkeypatch, extracted_requirements(BODY["deployment"]))
    access = start(client, {**BODY, "mode": "requirements", "run_name": "  Example α  "})
    result = finished(client, access).json()
    assert result["metadata"]["run_name"] == "  Example α  "
    created = datetime.fromisoformat(result["metadata"]["created_at"])
    finished_at = datetime.fromisoformat(result["metadata"]["finished_at"])
    assert created.tzinfo is not None and finished_at >= created
    assert result["extraction"]["usage"]["input_tokens"] == result["usage"]["input_tokens"]
    assert result["stage_usage"][0]["usage"] == result["usage"]


@pytest.mark.parametrize("route,seed", [
    ("ground", seed_requirements), ("retrieve", seed_grounding),
    ("screen", seed_retrieval), ("select", seed_screening), ("adapt", seed_selected),
])
def test_continuations_keep_name_and_usage_without_counting_retained_calls_twice(client, monkeypatch, route, seed):
    source = seed()
    job = item_review.jobs[source["run_id"]]
    job.request = job.request.model_copy(update={"run_name": "Shared example"})
    job.usage.update(input_tokens=23, output_tokens=5)
    job.usage_history = [{"run_id": "earlier-run", "mode": "requirements", "status": "completed",
                          "created_at": job.created_at_utc, "finished_at": job.created_at_utc,
                          "usage": {"input_tokens": 11}}]
    expected = deepcopy([*job.usage_history, item_review.usage_record(job)])
    monkeypatch.setattr(item_review, "inventory", lambda: {
        "repo": "fixture", "branches": {"main": "pinned"}, "missing_item_tables": [],
        "tables": [{"benchmark": "fixture", "branch": "main", "commit": "pinned", "row_count": 1}],
    })

    async def evaluate(new_job, _key):
        new_job.usage.update(input_tokens=7)
        new_job.status = "completed"
        new_job.finished_at = time.monotonic()

    monkeypatch.setattr(item_review, "evaluate", evaluate)
    response = client.post(f"/api/item-review/runs/{job.run_id}/{route}", json={},
                           headers={"X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY})
    assert response.status_code == 202, response.text
    result = finished(client, response.json()).json()
    assert result["metadata"]["run_name"] == "Shared example"
    assert result["stage_usage"][:-1] == expected
    assert result["stage_usage"][-1]["usage"] == result["usage"] == {"input_tokens": 7}
    assert job.usage == {"input_tokens": 23, "output_tokens": 5}
    assert len(job.usage_history) == 1


def test_package_snapshot_does_not_change_while_worker_builds(client, monkeypatch):
    access = seed_selected(per_facet=3)
    job = item_review.jobs[access["run_id"]]
    original = deepcopy(job.screening)
    real_build = item_review.build_results_package

    def build(snapshot, *, expand=None):
        # This emulates the pipeline publishing new results after snapshot capture.
        job.screening["items"][0]["evidence"]["item"]["content"] = "Later change"
        job.usage.update(input_tokens=999)
        return real_build(snapshot, expand=expand)

    monkeypatch.setattr(item_review, "build_results_package", build)
    snapshot, _ = unpack(download(client, access))
    assert snapshot["screening"] == original
    assert snapshot["usage"] == {}


def test_build_failure_releases_download_lease(client, monkeypatch):
    access = seed_requirements()
    job = item_review.jobs[access["run_id"]]

    def broken(_snapshot, *, expand=None):
        raise RuntimeError("fixture build failure")

    monkeypatch.setattr(item_review, "build_results_package", broken)
    response = download(client, access)
    assert response.status_code == 500
    assert "saved results are retained" in response.json()["detail"]
    assert "fixture build failure" not in response.text
    assert job.downloads == 0


def test_cancellation_closes_a_package_still_being_built(monkeypatch):
    async def exercise():
        monkeypatch.setattr(item_review, "jobs", {})
        access = seed_requirements()
        job = item_review.jobs[access["run_id"]]
        entered, release = Event(), Event()
        package = BytesIO(b"fixture")

        def build(_snapshot, *, expand=None):
            entered.set()
            assert release.wait(5)
            return package

        monkeypatch.setattr(item_review, "build_results_package", build)
        task = asyncio.create_task(item_review.export_package(job.run_id, job.secret))
        try:
            assert await asyncio.to_thread(entered.wait, 5)
            task.cancel()
            release.set()
            with pytest.raises(asyncio.CancelledError):
                await task
            assert package.closed and job.downloads == 0
        finally:
            release.set()

    asyncio.run(exercise())


@pytest.mark.parametrize("fail_on", ["http.response.start", "http.response.body"])
def test_disconnect_closes_package_even_before_streaming_starts(monkeypatch, fail_on):
    async def exercise():
        monkeypatch.setattr(item_review, "jobs", {})
        access = seed_requirements()
        job = item_review.jobs[access["run_id"]]
        package = BytesIO(b"fixture package bytes")
        monkeypatch.setattr(item_review, "build_results_package", lambda _, *, expand=None: package)
        response = await item_review.export_package(job.run_id, job.secret)
        assert job.downloads == 1

        async def send(message):
            if message["type"] == fail_on:
                raise OSError("client disconnected")

        async def receive():
            return {"type": "http.disconnect"}

        with pytest.raises(ClientDisconnect):
            await response({"type": "http", "asgi": {"spec_version": "2.4"}}, receive, send)
        assert package.closed and job.downloads == 0

    asyncio.run(exercise())
