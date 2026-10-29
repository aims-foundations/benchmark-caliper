"""Authenticated archive pieces preserve bytes across retries and cache pressure."""

import asyncio
import base64
from io import BytesIO
import json
import random
from threading import Event
from types import SimpleNamespace
from uuid import UUID
from zipfile import ZipFile

import pytest
from fastapi import HTTPException

from website.server import item_review, review_exports
from website.server.tests.test_item_review import client
from website.server.tests.test_onet_grounding import seed_requirements
from website.server.tests.test_background_result_package import endpoint, headers, wait_for_package


def prepared_fixture():
    access = seed_requirements()
    job = item_review.jobs[access["run_id"]]
    output = BytesIO()
    original = {"full_item": base64.b64encode(random.Random(17).randbytes(2 * review_exports.CHUNK_BYTES + 19)).decode()}
    with ZipFile(output, "w") as archive:
        archive.writestr("report.html", "<html>Saved result</html>")
        archive.writestr("selected_items.csv", "item_id\noriginal-item\n")
        archive.writestr("results.json", json.dumps(original))
    content = output.getvalue()
    job.package.file, job.package.size, job.package.filename = output, len(content), "saved-results.zip"
    job.package.refresh_lease()
    return access, job, content, original


def piece(client, access, package_id, offset):
    return client.get(endpoint(access) + "/chunk", params={"package_id": package_id, "offset": offset},
                      headers=headers(access))


def test_chunks_reconstruct_original_zip_and_retries_return_identical_bytes(client):
    access, job, original_zip, original_result = prepared_fixture()
    state = client.get(endpoint(access) + "/status", headers=headers(access)).json()
    assert state["chunk_bytes"] == review_exports.CHUNK_BYTES == 1048576
    assert str(UUID(state["package_id"])) == state["package_id"]
    assert state["bytes"] == len(original_zip)
    parts = []
    for offset in range(0, state["bytes"], state["chunk_bytes"]):
        response = piece(client, access, state["package_id"], offset)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"
        assert response.headers["cache-control"] == "no-store, no-transform"
        assert response.headers["x-package-id"] == state["package_id"]
        assert response.headers["x-package-offset"] == str(offset)
        assert len(response.content) == int(response.headers["content-length"]) == min(state["chunk_bytes"], state["bytes"] - offset)
        assert response.content == original_zip[offset:offset + state["chunk_bytes"]]
        assert piece(client, access, state["package_id"], offset).content == response.content
        parts.append(response.content)
    reconstructed = b"".join(parts)
    assert reconstructed == original_zip
    with ZipFile(BytesIO(reconstructed)) as archive:
        assert archive.testzip() is None
        assert archive.namelist() == ["report.html", "selected_items.csv", "results.json"]
        assert json.loads(archive.read("results.json")) == original_result
    # A dropped final response can still be retried during the finite grace.
    assert job.package.pinned() and job.downloads == 0 and not job.package.transferring


def test_chunk_access_rejects_wrong_tokens_ids_and_offsets(client):
    access, job, original_zip, _ = prepared_fixture()
    route = endpoint(access) + "/chunk"
    params = {"package_id": job.package.package_id, "offset": 0}
    assert client.get(route, params=params).status_code == 404
    assert client.get(route, params=params, headers={"X-Review-Token": "wrong"}).status_code == 404
    for wrong_id in ("wrong", "غير صحيح", ""):
        assert piece(client, access, wrong_id, 0).status_code == 412
    for invalid in (-1, len(original_zip), len(original_zip) + 1, "1.5", "not-an-offset"):
        assert piece(client, access, job.package.package_id, invalid).status_code == 416
    assert job.downloads == 0 and not job.package.transferring


def test_chunk_lease_survives_cache_pressure_then_expires_without_losing_saved_run(client, monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr(review_exports, "time", SimpleNamespace(monotonic=lambda: clock[0]))
    access, job, _, _ = prepared_fixture()
    item_review.checkpoint(job)
    artifact, package_id = job.package.file, job.package.package_id
    item_review.trim_pipeline_cache(limit=0)
    assert job.run_id in item_review.jobs and not artifact.closed
    clock[0] += 200
    assert piece(client, access, package_id, 0).status_code == 200
    assert job.package.lease_until == clock[0] + review_exports.DOWNLOAD_IDLE_SECONDS
    clock[0] += 200
    monkeypatch.setattr(item_review, "MAX_RETAINED", 0)
    item_review.make_cache_room()
    assert job.run_id in item_review.jobs and not artifact.closed
    clock[0] += review_exports.DOWNLOAD_IDLE_SECONDS + 1
    item_review.trim_pipeline_cache(limit=0)
    assert job.run_id not in item_review.jobs and artifact.closed
    assert piece(client, access, package_id, review_exports.CHUNK_BYTES).status_code == 412
    response = client.get(f"/api/item-review/runs/{job.run_id}", headers=headers(access))
    assert response.status_code == 200 and response.json()["requirements"] == job.requirements


def test_rebuilding_same_snapshot_uses_new_archive_identity(client):
    access = seed_requirements()
    assert client.post(endpoint(access), headers=headers(access)).status_code == 202
    first = wait_for_package(client, access)
    job = item_review.jobs[access["run_id"]]
    key = job.package.key
    job.package.close()
    assert client.post(endpoint(access), headers=headers(access)).status_code == 202
    second = wait_for_package(client, access)
    assert key == job.package.key and first["package_id"] != second["package_id"]
    assert piece(client, access, first["package_id"], 0).status_code == 412
    assert piece(client, access, second["package_id"], 0).status_code == 200


def test_new_download_click_renews_the_cached_archive_lease(client, monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr(review_exports, "time", SimpleNamespace(monotonic=lambda: clock[0]))
    access = seed_requirements()
    assert client.post(endpoint(access), headers=headers(access)).status_code == 202
    first = wait_for_package(client, access)
    job = item_review.jobs[access["run_id"]]
    clock[0] += review_exports.DOWNLOAD_IDLE_SECONDS + 1
    assert not job.package.pinned()
    response = client.post(endpoint(access), headers=headers(access))
    assert response.status_code == 200 and response.json()["package_id"] == first["package_id"]
    assert job.package.pinned() and job.package.lease_until == clock[0] + review_exports.DOWNLOAD_IDLE_SECONDS


def test_cancelled_read_drains_before_another_request_can_seek(monkeypatch):
    async def exercise():
        monkeypatch.setattr(item_review, "jobs", {})
        access = seed_requirements()
        job = item_review.jobs[access["run_id"]]
        entered, release = Event(), Event()
        content = b"abcdef" * review_exports.CHUNK_BYTES

        class BlockingFile(BytesIO):
            def read(self, size=-1):
                assert 0 < size <= review_exports.CHUNK_BYTES
                entered.set()
                assert release.wait(5)
                return super().read(size)

        artifact = BlockingFile(content)
        job.package.file, job.package.size = artifact, len(content)
        package_id = job.package.package_id
        task = asyncio.create_task(item_review.get_package_chunk(job.run_id, package_id, "0", job.secret))
        try:
            assert await asyncio.to_thread(entered.wait, 1)
            with pytest.raises(HTTPException) as busy:
                await item_review.get_package_chunk(job.run_id, package_id, "1", job.secret)
            assert busy.value.status_code == 429
            with pytest.raises(HTTPException) as whole:
                await item_review.export_package(job.run_id, job.secret, prepared=True)
            assert whole.value.status_code == 409
            with pytest.raises(HTTPException):
                await item_review.start_package(job.run_id, job.secret)
            task.cancel()
            await asyncio.sleep(.01)
            assert not task.done() and job.downloads == 1 and job.package.transferring
        finally:
            release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert job.downloads == 0 and not job.package.transferring and job.package.read_task is None
        response = await item_review.get_package_chunk(job.run_id, package_id, "7", job.secret)
        assert response.body == content[7:7 + review_exports.CHUNK_BYTES]
        job.package.close()

    asyncio.run(exercise())


def test_short_archive_read_reports_safe_error_and_invalidates_broken_cache(client, caplog):
    access = seed_requirements()
    job = item_review.jobs[access["run_id"]]
    artifact = BytesIO(b"short")
    job.package.file, job.package.size = artifact, 100
    package_id = job.package.package_id
    response = piece(client, access, package_id, 0)
    assert response.status_code == 503 and "saved results are retained" in response.json()["detail"]
    assert "Incomplete prepared archive" not in response.text + caplog.text
    assert artifact.closed and job.package.file is None and job.downloads == 0
    assert piece(client, access, package_id, 0).status_code == 412


def test_shutdown_finishes_pending_chunk_read_before_closing_archive(monkeypatch):
    async def exercise():
        monkeypatch.setattr(item_review, "jobs", {})
        monkeypatch.setattr(item_review, "checkpoint", lambda job: None)
        access = seed_requirements()
        job = item_review.jobs[access["run_id"]]
        entered, release = Event(), Event()

        class BlockingFile(BytesIO):
            def read(self, size=-1):
                entered.set()
                assert release.wait(5)
                return super().read(size)

        artifact = BlockingFile(b"archive bytes")
        job.package.file, job.package.size = artifact, 13
        request = asyncio.create_task(item_review.get_package_chunk(job.run_id, job.package.package_id, "0", job.secret))
        assert await asyncio.to_thread(entered.wait, 1)
        shutdown = asyncio.create_task(item_review.shutdown())
        try:
            await asyncio.sleep(.01)
            assert not shutdown.done() and not artifact.closed
        finally:
            release.set()
        response = await request
        await shutdown
        assert response.body == b"archive bytes"
        assert artifact.closed and job.downloads == 0 and not item_review.jobs

    asyncio.run(exercise())
