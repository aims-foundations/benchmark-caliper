"""Website scoring uses summaries; portable files are generated on demand."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
import csv
import errno
import io
from threading import Event
from zipfile import ZipFile

import pytest

from website.server import item_analysis as analysis
from website.server.tests.test_item_analysis import client, headers, settled, start, url
from website.server.tests.test_item_analysis_scores import model, score_all


def assert_deferred(job):
    assert (job.directory / "summary.json").is_file()
    assert not any((job.directory / name).exists() for name in ("items.csv", "report.html", "review.csv"))


def test_preparation_scoring_and_interrupted_restore_defer_exports(client, model):
    access = start(client)
    assert settled(client, access)["status"] == "ready"
    job = analysis.jobs[access["run_id"]]
    assert_deferred(job)
    completed = score_all(client, access)
    assert completed["status"] == "complete"
    assert_deferred(job)
    saved = (job.directory / "results.jsonl").read_bytes()
    calls = len(model)
    job.status = "running"
    analysis.persist(job)
    analysis.jobs.clear()
    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["status"] == "cancelled"
    assert restored["summary"]["dimensions"] == completed["summary"]["dimensions"]
    assert_deferred(analysis.jobs[access["run_id"]])
    assert len(model) == calls
    assert (job.directory / "results.jsonl").read_bytes() == saved


@pytest.mark.parametrize("artifact", ["items", "report"])
def test_download_rebuilds_stale_export_after_scoring(client, model, artifact):
    access = start(client)
    settled(client, access)
    initial = client.get(url(access) + f"/download/{artifact}", headers=headers(access))
    assert initial.status_code == 200
    assert not model
    job = analysis.jobs[access["run_id"]]
    filename = analysis.ARTIFACTS[artifact][0]
    completed = score_all(client, access)
    assert completed["status"] == "complete"
    assert (job.directory / filename).read_bytes() == initial.content
    calls = len(model)
    latest = client.get(url(access) + f"/download/{artifact}", headers=headers(access))
    assert latest.status_code == 200 and latest.content != initial.content
    if artifact == "items":
        rows = list(csv.DictReader(io.StringIO(latest.text)))
        assert len(rows) == completed["total"]
        assert all(row["status"] == "complete" and row["input_content.score"] == "4" for row in rows)
    else:
        assert "Prepared snapshot complete" in latest.text
    assert len(model) == calls and job.downloads == 0


def test_complete_package_materializes_deferred_files(client, model):
    access = start(client)
    settled(client, access)
    score_all(client, access)
    job = analysis.jobs[access["run_id"]]
    assert_deferred(job)
    calls = len(model)
    response = client.get(url(access) + "/package", headers=headers(access))
    assert response.status_code == 200
    with ZipFile(io.BytesIO(response.content)) as archive:
        assert {"report.html", "items.csv", "summary.json", "review.csv"} <= set(archive.namelist())
        assert "Prepared snapshot complete" in archive.read("report.html").decode()
    assert len(model) == calls and job.downloads == 0


def test_export_guard_covers_generation_and_releases_after_send(client, model, monkeypatch):
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    original = analysis.report.generate_report
    started, release = Event(), Event()

    def blocked(*args, **kwargs):
        started.set()
        assert release.wait(5)
        return original(*args, **kwargs)

    monkeypatch.setattr(analysis.report, "generate_report", blocked)
    with ThreadPoolExecutor() as pool:
        pending = pool.submit(client.get, url(access) + "/download/report", headers=headers(access))
        try:
            assert started.wait(2)
            assert job.downloads == 1
            assert client.post(url(access) + "/classify", json={"scope": "all"}, headers=headers(access, key=True)).status_code == 409
            assert client.delete(url(access), headers=headers(access)).status_code == 409
            assert client.get(url(access) + "/package", headers=headers(access)).status_code == 409
            assert client.get(url(access) + "/download/items", headers=headers(access)).status_code == 409
        finally:
            release.set()
        assert pending.result().status_code == 200
    assert job.downloads == 0 and not model


@pytest.mark.parametrize("error, status", [(RuntimeError("private detail"), 500), (OSError(errno.ENOSPC, "private detail"), 507)])
def test_failed_export_releases_guard_without_losing_scores(client, model, monkeypatch, error, status):
    access = start(client)
    settled(client, access)
    score_all(client, access)
    job = analysis.jobs[access["run_id"]]
    saved = (job.directory / "results.jsonl").read_bytes()

    def fail(*args, **kwargs):
        raise error

    with monkeypatch.context() as fault:
        fault.setattr(analysis.report, "generate_report", fail)
        response = client.get(url(access) + "/download/report", headers=headers(access))
    assert response.status_code == status and "private detail" not in response.text
    assert job.downloads == 0 and job.status == "complete"
    assert (job.directory / "results.jsonl").read_bytes() == saved
    assert client.get(url(access) + "/download/report", headers=headers(access)).status_code == 200


def test_cancelled_export_drains_writer_before_releasing_guard(client, monkeypatch):
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    original = analysis.report.generate_report
    started, release = Event(), Event()

    def blocked(*args, **kwargs):
        started.set()
        assert release.wait(5)
        return original(*args, **kwargs)

    monkeypatch.setattr(analysis.report, "generate_report", blocked)

    async def exercise():
        task = asyncio.create_task(analysis.download(access["run_id"], "report", access["run_secret"]))
        try:
            assert await asyncio.to_thread(started.wait, 2)
            task.cancel()
            await asyncio.sleep(0)
            assert job.downloads == 1
        finally:
            release.set()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(exercise())
    assert job.downloads == 0 and (job.directory / "report.html").is_file()
