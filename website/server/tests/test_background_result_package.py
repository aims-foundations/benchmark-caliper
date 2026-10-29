"""Prepare archives without holding an HTTP request open during compression."""

import asyncio
from copy import deepcopy
import errno
from io import BytesIO
from threading import Event, Lock
import time

import pytest
from fastapi import HTTPException
from starlette.requests import ClientDisconnect

from website.server import item_review
from website.server.candidate_store import CandidateStoreError
from website.server.tests.test_item_review import client
from website.server.tests.test_onet_grounding import seed_requirements
from website.server.tests.test_adaptive_screening import seed_selected
from website.server.tests.test_result_package_api import unpack


def endpoint(access):
    return f"/api/item-review/runs/{access['run_id']}/package"


def headers(access):
    return {"X-Review-Token": access["run_secret"]}


def wait_for_package(client, access):
    for _ in range(200):
        response = client.get(endpoint(access) + "/status", headers=headers(access))
        assert response.status_code == 200
        if response.json()["status"] != "preparing":
            return response.json()
        time.sleep(.01)
    pytest.fail("Package preparation did not finish")


def test_prepare_returns_before_build_finishes_and_reuses_private_immutable_zip(client, monkeypatch):
    access = seed_selected(per_facet=3)
    job = item_review.jobs[access["run_id"]]
    entered, release = Event(), Event()
    original = deepcopy(job.screening)
    real_build = item_review.build_results_package
    calls = []

    def blocked(snapshot, *, expand=None):
        calls.append(snapshot)
        entered.set()
        assert release.wait(5)
        return real_build(snapshot, expand=expand)

    monkeypatch.setattr(item_review, "build_results_package", blocked)
    assert client.post(endpoint(access)).status_code == 404
    assert client.get(endpoint(access) + "/status").status_code == 404
    assert client.get(endpoint(access) + "?prepared=true", headers=headers(access)).status_code == 409
    try:
        response = client.post(endpoint(access), headers=headers(access))
        assert response.status_code == 202 and response.json()["status"] == "preparing"
        assert entered.wait(1)
        assert job.downloads == 1
        assert client.get(endpoint(access) + "/status", headers=headers(access)).json()["status"] == "preparing"
        assert client.post(endpoint(access), headers=headers(access)).status_code == 202
        job.screening["items"][0]["assessment"]["task"]["justification"] = "A later saved explanation."
    finally:
        release.set()
    ready = wait_for_package(client, access)
    assert ready["status"] == "ready" and ready["bytes"] > 0
    assert job.downloads == 0 and len(calls) == 1
    response = client.get(endpoint(access) + "?prepared=true", headers=headers(access))
    snapshot, _ = unpack(response)
    assert snapshot["screening"] == original
    assert snapshot["retrieval"] == job.benchmark_retrieval
    assert int(response.headers["content-length"]) == len(response.content) == ready["bytes"]
    assert response.headers["x-accel-buffering"] == "no"
    assert job.downloads == 0
    # Restore the exact captured source, so another click reuses its archive.
    job.screening = original
    assert client.post(endpoint(access), headers=headers(access)).status_code == 200
    second = client.get(endpoint(access) + "?prepared=true", headers=headers(access))
    assert second.content == response.content and len(calls) == 1
    old_file = job.package.file
    job.usage.update(input_tokens=7)
    assert client.post(endpoint(access), headers=headers(access)).status_code == 202
    assert old_file.closed
    assert wait_for_package(client, access)["status"] == "ready"
    snapshot, _ = unpack(client.get(endpoint(access) + "?prepared=true", headers=headers(access)))
    assert snapshot["usage"]["input_tokens"] == 7 and len(calls) == 2


@pytest.mark.parametrize("error,status", [
    (CandidateStoreError("private path and evidence"), 503),
    (OSError(errno.ENOSPC, "private temporary path"), 507),
    (RuntimeError("private provider text"), 500),
])
def test_failure_is_safe_and_retry_keeps_the_saved_run(client, monkeypatch, caplog, error, status):
    access = seed_requirements()
    job = item_review.jobs[access["run_id"]]
    original = deepcopy(job.requirements)
    real_build = item_review.build_results_package

    def broken(*args, **kwargs):
        raise error

    monkeypatch.setattr(item_review, "build_results_package", broken)
    assert client.post(endpoint(access), headers=headers(access)).status_code == 202
    state = wait_for_package(client, access)
    assert state["status"] == "failed" and state["error_status"] == status
    assert "saved results are retained" in state["message"]
    assert "private" not in str(state) + caplog.text
    assert job.downloads == 0 and job.requirements == original
    assert client.get(endpoint(access) + "?prepared=true", headers=headers(access)).status_code == status
    monkeypatch.setattr(item_review, "build_results_package", real_build)
    assert client.post(endpoint(access), headers=headers(access)).status_code == 202
    assert wait_for_package(client, access)["status"] == "ready"


def test_eviction_closes_ready_file_and_restoration_can_rebuild(client):
    access = seed_selected(per_facet=1)
    job = item_review.jobs[access["run_id"]]
    item_review.checkpoint(job)
    assert client.post(endpoint(access), headers=headers(access)).status_code == 202
    assert wait_for_package(client, access)["status"] == "ready"
    artifact = job.package.file
    item_review.trim_pipeline_cache(limit=0)
    assert artifact.closed and job.run_id not in item_review.jobs
    state = client.get(endpoint(access) + "/status", headers=headers(access)).json()
    assert state["status"] == "not_started"
    assert client.get(endpoint(access) + "?prepared=true", headers=headers(access)).status_code == 409
    assert client.post(endpoint(access), headers=headers(access)).status_code == 202
    assert wait_for_package(client, access)["status"] == "ready"
    snapshot, _ = unpack(client.get(endpoint(access) + "?prepared=true", headers=headers(access)))
    assert snapshot["selection"] == job.selection


def test_uncached_restoration_cannot_start_an_untracked_package(client, monkeypatch):
    access = seed_requirements()
    job = item_review.jobs[access["run_id"]]
    item_review.checkpoint(job)
    item_review.jobs.clear()
    monkeypatch.setattr(item_review, "MAX_RETAINED", 0)
    monkeypatch.setattr(item_review, "build_results_package", lambda *a, **kw: pytest.fail("No untracked worker"))
    response = client.post(endpoint(access), headers=headers(access))
    assert response.status_code == 429
    assert "saved results are retained" in response.json()["detail"]
    assert not item_review.jobs
    # The underlying saved review remains readable even without a cache slot.
    response = client.get(f"/api/item-review/runs/{job.run_id}", headers=headers(access))
    assert response.status_code == 200 and response.json()["requirements"] == job.requirements


@pytest.mark.parametrize("fail_on", ["http.response.start", "http.response.body"])
def test_concurrent_transfers_are_rejected_and_disconnect_releases_cached_handle(monkeypatch, fail_on):
    async def exercise():
        monkeypatch.setattr(item_review, "jobs", {})
        access = seed_requirements()
        job = item_review.jobs[access["run_id"]]
        package = BytesIO(b"prepared archive")
        job.package.file, job.package.size, job.package.filename = package, 16, "example.zip"
        response = await item_review.export_package(job.run_id, job.secret, prepared=True)
        assert job.downloads == 1 and job.package.transferring
        with pytest.raises(HTTPException) as caught:
            await item_review.export_package(job.run_id, job.secret, prepared=True)
        assert caught.value.status_code == 409
        with pytest.raises(HTTPException):
            await item_review.start_package(job.run_id, job.secret)

        async def send(message):
            if message["type"] == fail_on:
                raise OSError("client disconnected")

        async def receive():
            return {"type": "http.disconnect"}

        with pytest.raises(ClientDisconnect):
            await response({"type": "http", "asgi": {"spec_version": "2.4"}}, receive, send)
        assert job.downloads == 0 and not job.package.transferring and not package.closed
        job.package.close()
        assert package.closed

    asyncio.run(exercise())


def test_shutdown_drains_package_worker_and_closes_its_temporary_file(monkeypatch):
    async def exercise():
        monkeypatch.setattr(item_review, "jobs", {})
        monkeypatch.setattr(item_review, "checkpoint", lambda job: None)
        access = seed_requirements()
        job = item_review.jobs[access["run_id"]]
        entered, release = Event(), Event()
        package = BytesIO(b"fixture")

        def blocked(*args, **kwargs):
            entered.set()
            assert release.wait(5)
            return package

        monkeypatch.setattr(item_review, "build_results_package", blocked)
        await item_review.start_package(job.run_id, job.secret)
        assert await asyncio.to_thread(entered.wait, 1)
        shutdown = asyncio.create_task(item_review.shutdown())
        await asyncio.sleep(.01)
        assert not shutdown.done() and not package.closed
        release.set()
        await shutdown
        assert package.closed and job.downloads == 0 and not item_review.jobs

    asyncio.run(exercise())


def test_preparation_cancelled_before_first_turn_releases_lease(monkeypatch):
    async def exercise():
        monkeypatch.setattr(item_review, "jobs", {})
        monkeypatch.setattr(item_review, "checkpoint", lambda job: None)
        access = seed_requirements()
        job = item_review.jobs[access["run_id"]]
        await item_review.start_package(job.run_id, job.secret)
        await item_review.shutdown()
        assert job.downloads == 0 and not item_review.jobs
    asyncio.run(exercise())


def test_builds_for_different_runs_are_serialized(client, monkeypatch):
    first, second = seed_requirements(), seed_requirements()
    # Fixture IDs are normally identical; retain two distinct private jobs.
    second_job = item_review.jobs[second["run_id"]]
    second_job.run_id = "second-package-run"
    item_review.jobs[second_job.run_id] = second_job
    first = seed_requirements()
    second = {"run_id": second_job.run_id, "run_secret": second_job.secret}
    entered, release, guard = Event(), Event(), Lock()
    active, peak = 0, 0

    def blocked(*args, **kwargs):
        nonlocal active, peak
        with guard:
            active += 1
            peak = max(peak, active)
        entered.set()
        assert release.wait(5)
        with guard:
            active -= 1
        return BytesIO(b"fixture archive")

    monkeypatch.setattr(item_review, "build_results_package", blocked)
    try:
        assert client.post(endpoint(first), headers=headers(first)).status_code == 202
        assert entered.wait(1)
        assert client.post(endpoint(second), headers=headers(second)).status_code == 202
        assert active == peak == 1
    finally:
        release.set()
    assert wait_for_package(client, first)["status"] == "ready"
    assert wait_for_package(client, second)["status"] == "ready"
    assert peak == 1
