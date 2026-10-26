"""Saved website analyses remain private, resumable, and independently exportable."""

import asyncio
import io
import json
from pathlib import Path
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pytest

from anthropic_api_package_release.item_analysis import model_client
from anthropic_api_package_release.item_analysis.storage import read_json, write_json
from website.server import item_analysis as analysis, item_analysis_store as store
from website.server.tests.test_item_analysis import (
    KEY, client, model, current_assessment, classify, headers, request_payload,
    settled, start, start_linked, url,
)


def test_no_default_expiry_restores_after_cache_eviction_without_plaintext_credentials(client, model):
    access = start(client)
    ready = settled(client, access)
    job = analysis.jobs[access["run_id"]]
    job.updated_at = time.time() - 14 * 86400
    analysis.persist(job)
    metadata_text = (job.directory / store.METADATA).read_text()
    assert KEY not in metadata_text and access["run_secret"] not in metadata_text
    assert read_json(job.directory / store.METADATA)["secret_digest"] == store.token_digest(access["run_secret"])
    analysis.jobs.clear()
    assert client.get(url(access), headers={"X-Review-Token": "wrong"}).status_code == 404
    assert not analysis.jobs
    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["status"] == "ready" and restored["spec"] == ready["spec"]
    assert restored["retention"] == {"automatic_expiry": False, "expires_at": None}
    assert restored["created_at"] == ready["created_at"] and not model
    assert client.delete(url(access)).status_code == 404
    assert client.delete(url(access), headers=headers(access)).status_code == 204
    assert not job.directory.exists()
    assert client.get(url(access), headers=headers(access)).status_code == 404


def test_shutdown_preserves_checkpoint_and_resume_reuses_frozen_judgments(client, model, monkeypatch):
    monkeypatch.setattr(analysis, "CHECKPOINT_SIZE", 2)
    access = start(client, mode="generate")
    settled(client, access)
    before = classify(client, access)
    assert before["status"] == "checkpoint" and before["completed_judgments"] == 8
    directory = analysis.jobs[access["run_id"]].directory
    client.portal.call(analysis.shutdown)
    assert not analysis.jobs and directory.exists()
    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["status"] == "checkpoint" and restored["usage"] == before["usage"]
    assert restored["can_continue"] and restored["completed_judgments"] == 8
    complete = classify(client, access, "all")
    assert complete["status"] == "complete" and len(model) == 41
    ledger = [json.loads(line) for line in (directory / "usage_ledger.jsonl").read_text().splitlines()]
    requests = [json.loads(line) for line in (directory / "requests.jsonl").read_text().splitlines()]
    assert len(ledger) == len(requests) == 41
    assert {row["sequence"] for row in ledger} == set(range(1, 42))
    assert all(row["usage_known"] and row["status"] == "complete" for row in ledger)
    assert ledger[0]["step"] == requests[0]["step"] == "item_specification"
    assert all(row["started_at"] and row["finished_at"] for row in ledger)
    assert read_json(directory / "usage.json")["input_tokens"] == complete["usage"]["input_tokens"]
    usage = read_json(directory / "usage.json")
    assert usage["calls"] == usage["calls_with_usage"] == 41 and usage["calls_without_usage"] == 0


def test_interrupted_classification_restores_partial_success_and_unknown_failed_usage(client, model, monkeypatch):
    access = start(client)
    settled(client, access)
    original = model_client.call_text_async

    async def fail_second(**arguments):
        if request_payload(arguments["user"])["classifier"]["id"] == "input_content":
            raise model_client.ModelRequestError(code="connection")
        return await original(**arguments)

    monkeypatch.setattr(model_client, "call_text_async", fail_second)
    failed = classify(client, access)
    assert failed["completed_judgments"] == 1
    job = analysis.jobs[access["run_id"]]
    job.status = "running"  # Simulate restart before the final phase metadata write.
    analysis.persist(job)
    analysis.jobs.clear()
    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["status"] == "cancelled" and restored["completed_judgments"] == 1
    assert restored["remaining_judgments"]["pilot"] == 39
    ledger = [json.loads(line) for line in (job.directory / "usage_ledger.jsonl").read_text().splitlines()]
    assert ledger[-1]["status"] == "failed" and ledger[-1]["usage_known"] is False
    assert "input_tokens" not in ledger[-1]
    assert read_json(job.directory / "usage.json")["calls_without_usage"] == 1
    monkeypatch.setattr(model_client, "call_text_async", original)
    assert classify(client, access)["status"] == "complete"
    pairs = [(payload["item"]["item_id"], payload["classifier"]["id"]) for _, payload in model]
    assert len(pairs) == len(set(pairs)) == 40


def test_incomplete_context_is_restored_as_safe_failure(client, model):
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    (job.directory / "classifier_spec.json").unlink()
    job.status = "generating"
    analysis.persist(job)
    analysis.jobs.clear()
    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["status"] == "failed" and restored["spec"] is None
    assert restored["failure"]["code"] == "interrupted" and not model
    assert client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access, key=True)).status_code == 409


def test_saved_run_count_does_not_block_new_runs_and_evicted_access_still_works(client, monkeypatch):
    monkeypatch.setattr(analysis, "MAX_RETAINED", 2)
    accesses = []
    for _ in range(4):
        access = start(client)
        assert settled(client, access)["status"] == "ready"
        accesses.append(access)
    analysis.sweep()
    assert len(analysis.jobs) <= 2
    assert len(list(analysis.storage_root().iterdir())) == 4
    assert client.get(url(accesses[0]), headers=headers(accesses[0])).json()["status"] == "ready"


def test_parent_deletion_removes_linked_runs_even_when_not_cached(client, current_assessment):
    access = start_linked(client, current_assessment, rows=[{"content": "Question"}])
    settled(client, access)
    directory = analysis.jobs[access["run_id"]].directory
    analysis.jobs.clear()
    client.portal.call(analysis.delete_for_assessment, current_assessment["assessment_id"])
    assert not directory.exists()
    assert client.get(url(access), headers=headers(access)).status_code == 404


def test_package_is_private_complete_archive_of_partial_run_without_credentials(client, model, monkeypatch):
    monkeypatch.setattr(analysis, "CHECKPOINT_SIZE", 2)
    access = start(client, mode="generate")
    settled(client, access)
    checkpoint = classify(client, access)
    assert checkpoint["status"] == "checkpoint"
    directory = analysis.jobs[access["run_id"]].directory
    assert client.get(url(access) + "/package").status_code == 404
    response = client.get(url(access) + "/package", headers=headers(access))
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "application/zip"
    assert ".zip" in response.headers["content-disposition"]
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        names = archive.namelist()
        assert "report.html" in names and "review/blank_review.csv" in names
        assert not any(store.METADATA in name for name in names)
        for name in names:
            data = archive.read(name)
            assert KEY.encode() not in data and access["run_secret"].encode() not in data
            assert store.token_digest(access["run_secret"]).encode() not in data
        assert any(name.endswith("requests.jsonl") for name in names)
        assert any(name.endswith("usage_ledger.jsonl") for name in names)
    assert analysis.jobs[access["run_id"]].downloads == 0
    assert directory.exists()


def test_optional_expiry_also_prunes_uncached_runs(client, monkeypatch):
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    job.updated_at = time.time() - 3601
    analysis.persist(job)
    analysis.jobs.clear()
    monkeypatch.setenv("ITEM_ANALYSIS_RETENTION_SECONDS", "3600")
    assert client.get(url(access), headers=headers(access)).status_code == 404
    assert not job.directory.exists()


def test_restart_recovers_unknown_usage_and_sequence_before_metadata_commit(client):
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    request = {"sequence": 1, "step": "item_classification.input_ontology", "model": job.model["model_id"],
               "reasoning_effort": job.model["reasoning_effort"], "max_tokens": 100,
               "started_at": store.timestamp(time.time()), "system": "rules", "user": "item"}
    store.append_jsonl(job.directory / "requests.jsonl", request)
    # The process died before receiving usage or updating the metadata sequence.
    job.status = "running"
    analysis.persist(job)
    with (job.directory / "usage_ledger.jsonl").open("ab") as handle:
        handle.write(b'{"sequence":')
    analysis.jobs.clear()
    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["status"] == "cancelled" and restored["usage"]["input_tokens"] == 0
    usage = read_json(job.directory / "usage.json")
    assert usage["calls"] == usage["calls_without_usage"] == 1 and usage["calls_with_usage"] == 0
    ledger = [json.loads(line) for line in (job.directory / "usage_ledger.jsonl").read_text().splitlines()]
    assert len(ledger) == 1 and ledger[0]["status"] == "interrupted" and ledger[0]["finished_at"] is None
    assert classify(client, access)["status"] == "complete"
    requests = [json.loads(line) for line in (job.directory / "requests.jsonl").read_text().splitlines()]
    assert [entry["sequence"] for entry in requests] == list(range(1, 42))


def test_package_guard_blocks_new_phases_discard_and_cache_eviction(client, monkeypatch):
    from anthropic_api_package_release.item_analysis import package

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
    with ThreadPoolExecutor() as pool:
        pending = pool.submit(client.get, url(access) + "/package", headers=headers(access))
        try:
            assert started.wait(2)
            assert client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access, key=True)).status_code == 409
            assert client.delete(url(access), headers=headers(access)).status_code == 409
            assert client.get(url(access) + "/download/report", headers=headers(access)).status_code == 409
            monkeypatch.setattr(analysis, "MAX_RETAINED", 0)
            monkeypatch.setenv("ITEM_ANALYSIS_RETENTION_SECONDS", "1")
            job.updated_at = time.time() - 3601
            analysis.sweep()
            assert analysis.jobs[access["run_id"]] is job and job.directory.exists()
        finally:
            release.set()
        assert pending.result().status_code == 200
    assert job.downloads == 0


def test_cancelled_file_send_releases_download_guard(client, monkeypatch):
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    job.downloads = 1

    async def disconnected(*_):
        raise asyncio.CancelledError

    monkeypatch.setattr(analysis.FileResponse, "__call__", disconnected)
    response = analysis.AnalysisFileResponse(job.directory / "report.html", job=job)
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(response({}, None, None))
    assert job.downloads == 0


def test_cancelled_package_build_drains_writer_then_releases_guard(client, monkeypatch):
    from anthropic_api_package_release.item_analysis import package

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

    async def exercise():
        task = asyncio.create_task(analysis.download_package(access["run_id"], access["run_secret"]))
        try:
            assert await asyncio.to_thread(started.wait, 2)
            task.cancel()
            await asyncio.sleep(0)
            assert job.downloads == 1  # The writing thread must finish before unlocking.
        finally:
            release.set()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(exercise())
    assert job.downloads == 0 and job.directory.exists()


@pytest.mark.parametrize("symlink", [False, True])
def test_original_assessment_pdf_is_frozen_only_from_safe_local_file(client, current_assessment, tmp_path, symlink):
    assessment = analysis.item_analysis_assessment.resolve("run", current_assessment["assessment_id"])
    pdf = Path(assessment["evidence_directory"]) / "pdfs" / "review.pdf"
    pdf.parent.mkdir()
    original = b"%PDF-1.4\nOriginal benchmark report"
    if symlink:
        outside = tmp_path / "unrelated.pdf"
        outside.write_bytes(original)
        pdf.symlink_to(outside)
    else:
        pdf.write_bytes(original)
    access = start_linked(client, current_assessment, rows=[{"content": "Question"}])
    settled(client, access)
    directory = analysis.jobs[access["run_id"]].directory
    frozen = directory / "original_benchmark_report.pdf"
    assert frozen.exists() is not symlink
    if not symlink:
        pdf.write_bytes(b"Changed later")
        response = client.get(url(access) + "/package", headers=headers(access))
        assert response.status_code == 200
        with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
            assert archive.read("original_benchmark_report.pdf") == original


def test_restore_repairs_complete_audit_tail_before_later_append(tmp_path):
    request = {"sequence": 1, "step": "item_classification.input_ontology", "model": "fixture",
               "reasoning_effort": "none", "max_tokens": 100, "started_at": store.timestamp(time.time()),
               "system": "rules", "user": "item"}
    usage = {**request, "usage_known": True, "input_tokens": 5, "output_tokens": 2, "status": "complete"}
    (tmp_path / "requests.jsonl").write_text(json.dumps(request))
    (tmp_path / "usage_ledger.jsonl").write_text(json.dumps(usage))
    totals, sequence = store.load_usage(tmp_path)
    assert sequence == 1 and totals["input_tokens"] == 5
    store.append_jsonl(tmp_path / "requests.jsonl", {**request, "sequence": 2})
    store.record_call(tmp_path, {**usage, "sequence": 2}, totals)
    restored, sequence = store.load_usage(tmp_path)
    assert sequence == 2 and restored["input_tokens"] == 10
    assert read_json(tmp_path / "usage.json")["calls_with_usage"] == 2
    assert all(len(list(store.saved_records(tmp_path / filename))) == 2
               for filename in ("requests.jsonl", "usage_ledger.jsonl"))
