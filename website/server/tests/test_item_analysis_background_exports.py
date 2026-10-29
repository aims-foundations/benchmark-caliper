"""Large exports finish independently of the short preparation/status requests."""

import asyncio
import errno
import io
import json
from threading import Event
import time
from zipfile import ZipFile

import pytest

from anthropic_api_package_release.item_analysis import package
from website.server import item_analysis as analysis
from website.server.tests.test_item_analysis import client, headers, settled, start, url
from website.server.tests.test_item_analysis_scores import model, score_all


def package_ready(client, access):
    for _ in range(400):
        response = client.get(url(access) + "/package/status", headers=headers(access))
        assert response.status_code == 200, response.text
        state = response.json()
        if state["status"] != "preparing":
            return state
        time.sleep(.01)
    pytest.fail("Package did not finish")


def begin(client, access):
    return client.post(url(access) + "/package", headers=headers(access))


def test_slow_export_returns_immediately_and_survives_request_completion(client, model, monkeypatch):
    access = start(client)
    settled(client, access)
    score_all(client, access)
    job = analysis.jobs[access["run_id"]]
    calls = len(model)
    original = package.build_results_package
    started, release = Event(), Event()
    builds = []

    def blocked(*args, **kwargs):
        builds.append(True)
        started.set()
        assert release.wait(5)
        return original(*args, **kwargs)

    monkeypatch.setattr(package, "build_results_package", blocked)
    try:
        response = begin(client, access)
        assert response.status_code == 202 and response.json()["status"] == "preparing"
        assert response.headers["cache-control"] == "no-store"
        assert started.wait(2)
        assert begin(client, access).status_code == 202
        state = client.get(url(access) + "/package/status", headers=headers(access))
        assert state.json()["status"] == "preparing"
        assert state.headers["cache-control"] == "no-store"
        assert len(builds) == 1 and job.downloads == 1
        assert client.get(url(access), headers=headers(access)).status_code == 200
        assert client.delete(url(access), headers=headers(access)).status_code == 409
        assert client.post(url(access) + "/classify", json={"scope": "all"}, headers=headers(access, key=True)).status_code == 409
        assert client.get(url(access) + "/package?prepared=true", headers=headers(access)).status_code == 409
        assert client.get(url(access) + "/download/items", headers=headers(access)).status_code == 409
        monkeypatch.setattr(analysis, "MAX_RETAINED", 0)
        analysis.sweep()
        assert analysis.jobs[access["run_id"]] is job
    finally:
        release.set()
    state = package_ready(client, access)
    assert state["status"] == "ready" and state["bytes"] > 0
    response = client.get(url(access) + "/package?prepared=true", headers=headers(access))
    assert response.status_code == 200
    with ZipFile(io.BytesIO(response.content)) as archive:
        assert json.loads(archive.read("manifest.json"))["counts"]["selected_completed_items"] == 10
    assert job.downloads == 0 and len(model) == calls and len(builds) == 1


def test_cached_package_reused_across_downloads_and_restoration(client, model, monkeypatch):
    access = start(client)
    settled(client, access)
    score_all(client, access)
    assert begin(client, access).status_code == 202
    assert package_ready(client, access)["status"] == "ready"
    first = client.get(url(access) + "/package?prepared=true", headers=headers(access))
    calls = len(model)

    def unexpected(*args, **kwargs):
        pytest.fail("An unchanged saved run must reuse its completed archive")

    monkeypatch.setattr(package, "build_results_package", unexpected)
    for restore in (False, True):
        if restore:
            analysis.jobs.clear()
        assert begin(client, access).status_code == 200
        assert package_ready(client, access)["status"] == "ready"
        response = client.get(url(access) + "/package?prepared=true", headers=headers(access))
        assert response.status_code == 200 and response.content == first.content
    assert len(model) == calls


def test_resume_invalidates_archive_and_exports_new_scores(client, model, monkeypatch):
    monkeypatch.setattr(analysis, "CHECKPOINT_SIZE", 2)
    access = start(client)
    settled(client, access)
    assert client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access, key=True)).status_code == 202
    assert settled(client, access)["complete"] == 2
    begin(client, access)
    assert package_ready(client, access)["status"] == "ready"
    first = client.get(url(access) + "/package?prepared=true", headers=headers(access))
    assert score_all(client, access)["complete"] == 10
    assert client.get(url(access) + "/package?prepared=true", headers=headers(access)).status_code == 409
    assert begin(client, access).status_code == 202
    assert package_ready(client, access)["status"] == "ready"
    latest = client.get(url(access) + "/package?prepared=true", headers=headers(access))
    assert latest.status_code == 200 and latest.content != first.content
    with ZipFile(io.BytesIO(latest.content)) as archive:
        assert json.loads(archive.read("manifest.json"))["counts"]["selected_completed_items"] == 10
    assert len(model) == 10


@pytest.mark.parametrize("error, code", [(RuntimeError("private server detail"), 500),
                                        (OSError(errno.ENOSPC, "private server detail"), 507)])
def test_failed_background_build_exposes_safe_error_and_can_retry(client, model, monkeypatch, error, code):
    access = start(client)
    settled(client, access)
    score_all(client, access)
    job = analysis.jobs[access["run_id"]]
    saved = (job.directory / "results.jsonl").read_bytes()

    def fail(*args, **kwargs):
        raise error

    with monkeypatch.context() as fault:
        fault.setattr(package, "build_results_package", fail)
        assert begin(client, access).status_code == 202
        state = package_ready(client, access)
    assert state["status"] == "failed" and state["error_status"] == code
    assert "private server detail" not in json.dumps(state)
    assert job.downloads == 0 and job.status == "complete"
    assert (job.directory / "results.jsonl").read_bytes() == saved
    assert begin(client, access).status_code == 202
    assert package_ready(client, access)["status"] == "ready"


@pytest.mark.parametrize("method, suffix", [("post", "/package"), ("get", "/package/status"),
                                           ("get", "/package?prepared=true")])
def test_export_preparation_status_and_file_require_private_access(client, method, suffix):
    access = start(client)
    settled(client, access)
    response = getattr(client, method)(url(access) + suffix)
    assert response.status_code == 404
    assert analysis.jobs[access["run_id"]].package_task is None


def test_status_and_prepared_download_do_not_start_work(client, monkeypatch):
    access = start(client)
    settled(client, access)

    def unexpected(*args, **kwargs):
        pytest.fail("Only explicit preparation may start a background export")

    monkeypatch.setattr(package, "build_results_package", unexpected)
    assert package_ready(client, access)["status"] == "not_started"
    assert client.get(url(access) + "/package?prepared=true", headers=headers(access)).status_code == 409


@pytest.mark.parametrize("corruption", ["metadata", "archive", "path", "symlink"])
def test_invalid_cache_is_never_served(client, tmp_path, corruption):
    access = start(client)
    settled(client, access)
    begin(client, access)
    state = package_ready(client, access)
    job = analysis.jobs[access["run_id"]]
    directory = job.directory / "generated_exports"
    metadata = directory / analysis.exports.CACHE_NAME
    if corruption == "metadata":
        metadata.write_text("broken JSON")
    elif corruption == "archive":
        (directory / state["filename"]).write_bytes(b"truncated")
    elif corruption == "path":
        cached = json.loads(metadata.read_text())
        cached["filename"] = "../private.zip"
        metadata.write_text(json.dumps(cached))
    else:
        archive = directory / state["filename"]
        outside = tmp_path / "private.zip"
        outside.write_bytes(archive.read_bytes())
        archive.unlink()
        archive.symlink_to(outside)
    assert package_ready(client, access)["status"] == "not_started"
    assert client.get(url(access) + "/package?prepared=true", headers=headers(access)).status_code == 409


def test_shutdown_drains_background_export_and_keeps_completed_package(client, monkeypatch):
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    original = package.build_results_package
    started, release = Event(), Event()

    def blocked(*args, **kwargs):
        started.set()
        assert release.wait(5)
        return original(*args, **kwargs)

    monkeypatch.setattr(package, "build_results_package", blocked)
    begin(client, access)
    assert started.wait(2)

    async def exercise():
        shutdown = asyncio.create_task(analysis.shutdown())
        try:
            await asyncio.sleep(.02)
            assert not shutdown.done() and job.downloads == 1
        finally:
            release.set()
        await shutdown

    client.portal.call(exercise)
    assert not analysis.jobs and job.downloads == 0
    assert package_ready(client, access)["status"] == "ready"


def test_exports_for_different_runs_are_serialized(client, monkeypatch):
    accesses = [start(client), start(client)]
    for access in accesses:
        settled(client, access)
    original = package.build_results_package
    started, release = Event(), Event()
    builds = []

    def blocked(*args, **kwargs):
        builds.append(kwargs["run_id"])
        if len(builds) == 1:
            started.set()
            assert release.wait(5)
        return original(*args, **kwargs)

    monkeypatch.setattr(package, "build_results_package", blocked)
    try:
        assert begin(client, accesses[0]).status_code == 202
        assert started.wait(2)
        assert begin(client, accesses[1]).status_code == 202
        time.sleep(.02)
        assert builds == [accesses[0]["run_id"]]
        assert all(analysis.jobs[access["run_id"]].downloads == 1 for access in accesses)
    finally:
        release.set()
    assert all(package_ready(client, access)["status"] == "ready" for access in accesses)
    assert builds == [access["run_id"] for access in accesses]


def test_cancelled_background_task_drains_writer_and_retains_ready_archive(client, monkeypatch):
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    original = package.build_results_package
    started, release = Event(), Event()

    def blocked(*args, **kwargs):
        started.set()
        assert release.wait(5)
        return original(*args, **kwargs)

    monkeypatch.setattr(package, "build_results_package", blocked)
    begin(client, access)
    assert started.wait(2)

    async def exercise():
        job.package_task.cancel()
        try:
            await asyncio.sleep(.02)
            assert not job.package_task.done() and job.downloads == 1
        finally:
            release.set()
        with pytest.raises(asyncio.CancelledError):
            await job.package_task

    client.portal.call(exercise)
    assert job.downloads == 0
    assert package_ready(client, access)["status"] == "ready"
