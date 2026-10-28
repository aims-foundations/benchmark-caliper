"""Storage exhaustion must stop work, expose a useful error, and retain saved scores."""

import errno
import json
from pathlib import Path

import pytest

from website.server import item_analysis as analysis
from website.server.tests.test_item_analysis import (
    client, current_assessment, headers, settled, start, start_linked, url,
)
from website.server.tests.test_item_analysis_scores import model, score_all


PRIVATE_PATH = "/private/server/path/must-not-appear"


def disk_full(error_number=errno.ENOSPC):
    return OSError(error_number, "Storage write failed", PRIVATE_PATH)


def assert_storage_failure(payload):
    assert payload["status"] == "failed", payload
    assert payload["failure"]["code"] == "storage_full", payload
    assert "server storage is full" in payload["message"].lower()
    assert payload["provider_error"] is None
    assert PRIVATE_PATH not in json.dumps(payload)


@pytest.mark.parametrize("endpoint", ["example", "assessment", "direct"])
@pytest.mark.parametrize("operation", ["mkdir", "metadata"])
@pytest.mark.parametrize("error_number", [errno.ENOSPC, errno.EDQUOT])
def test_new_run_storage_failure_is_507_without_an_orphan_worker(
        client, current_assessment, monkeypatch, model, endpoint, operation, error_number):
    original_mkdir = Path.mkdir

    def failing_mkdir(path, *args, **kwargs):
        if path.is_relative_to(analysis.storage_root()):
            raise disk_full(error_number)
        return original_mkdir(path, *args, **kwargs)

    def failing_metadata(*args, **kwargs):
        raise disk_full(error_number)

    with monkeypatch.context() as fault:
        if operation == "mkdir":
            fault.setattr(Path, "mkdir", failing_mkdir)
        else:
            fault.setattr(analysis, "persist", failing_metadata)
        if endpoint == "example":
            response = client.post("/api/item-analysis/runs", json={"example_id": "illustrative"})
        else:
            fields = current_assessment if endpoint == "assessment" else {
                "context_json": json.dumps({
                    "benchmark": "Arithmetic", "deployment": "An English math tutor.",
                    "task_requirements": "Addition.", "answer_requirements": "Explain the answer.",
                }),
                "benchmark_confirmed": "true",
            }
            response = client.post(f"/api/item-analysis/runs/from-{endpoint if endpoint == 'assessment' else 'context'}",
                                   data=fields, files={"items_file": ("items.json", '[{"content":"2+2?"}]')})
        assert response.status_code == 507, response.text
        assert "server storage is full" in response.json()["detail"].lower()
        assert PRIVATE_PATH not in response.text
        assert not analysis.jobs
        assert not model


@pytest.mark.parametrize("error_number", [errno.ENOSPC, errno.EDQUOT])
def test_failed_classification_transition_retains_scope_and_saved_items(
        client, monkeypatch, model, error_number):
    monkeypatch.setattr(analysis, "CHECKPOINT_SIZE", 1)
    access = start(client)
    ready = settled(client, access)
    assert client.post(url(access) + "/classify", json={"scope": "pilot"},
                       headers=headers(access, key=True)).status_code == 202
    checkpoint = settled(client, access)
    assert checkpoint["status"] == "checkpoint" and len(model) == 1
    saved_item = checkpoint["items"][0]

    def failing_metadata(*args, **kwargs):
        raise disk_full(error_number)

    with monkeypatch.context() as fault:
        fault.setattr(analysis, "persist", failing_metadata)
        response = client.post(url(access) + "/classify", json={"scope": "all"},
                               headers=headers(access, key=True))
        assert response.status_code == 507, response.text
        assert "server storage is full" in response.json()["detail"].lower()
        failed = settled(client, access)
        assert_storage_failure(failed)
        assert failed["scope"] == "pilot"
        assert failed["complete"] == 1 and failed["items"][0] == saved_item
        assert len(model) == 1
        assert analysis.jobs[access["run_id"]].owner_hash is None

    completed = score_all(client, access)
    assert completed["status"] == "complete", completed
    assert completed["items"][0] == saved_item
    assert len(model) == ready["total"]


@pytest.mark.parametrize("phase", ["preparation", "wrapped_preparation", "specification", "report", "metadata"])
@pytest.mark.parametrize("error_number", [errno.ENOSPC, errno.EDQUOT])
def test_background_preparation_storage_failure_finishes_without_model_calls(
        client, current_assessment, monkeypatch, model, phase, error_number):
    original_persist = analysis.persist

    def failing_write(*args, **kwargs):
        raise disk_full(error_number)

    def failing_wrapped_preparation(*args, **kwargs):
        try:
            raise disk_full(error_number)
        except OSError:
            # Dataset preparation intentionally sanitizes exception text. Its
            # cause must still identify local storage exhaustion correctly.
            raise analysis.item_analysis_databank.DataBankError("Dataset preparation failed.") from None

    def failing_prepared_metadata(job):
        if job.data_ready:
            raise disk_full(error_number)
        return original_persist(job)

    with monkeypatch.context() as fault:
        if phase == "preparation":
            fault.setattr(analysis, "prepare_assessment_job", failing_write)
        elif phase == "wrapped_preparation":
            fault.setattr(analysis, "prepare_assessment_job", failing_wrapped_preparation)
        elif phase == "specification":
            fault.setattr(analysis.scoring, "prepare_context", failing_write)
        elif phase == "report":
            fault.setattr(analysis.report, "generate_report", failing_write)
        else:
            fault.setattr(analysis, "persist", failing_prepared_metadata)
        access = start_linked(client, current_assessment, rows=[{"content": "2+2?"}])
        failed = settled(client, access)
        assert_storage_failure(failed)
        assert failed["processed"] == 0 and not model


@pytest.mark.parametrize("operation", ["request_journal", "metadata"])
def test_scoring_storage_failure_preserves_checkpoint_and_resumes(
        client, monkeypatch, model, operation):
    monkeypatch.setattr(analysis, "CHECKPOINT_SIZE", 1)
    access = start(client)
    ready = settled(client, access)
    assert client.post(url(access) + "/classify", json={"scope": "pilot"},
                       headers=headers(access, key=True)).status_code == 202
    checkpoint = settled(client, access)
    assert checkpoint["status"] == "checkpoint" and len(model) == 1
    saved_item = checkpoint["items"][0]
    original_append = analysis.store.append_jsonl
    original_persist = analysis.persist
    saved_sequence = analysis.jobs[access["run_id"]].call_sequence

    def failing_request_journal(path, entry):
        if path.name == "requests.jsonl":
            raise disk_full()
        return original_append(path, entry)

    def failing_scoring_metadata(job):
        if job.call_sequence > saved_sequence:
            raise disk_full()
        return original_persist(job)

    with monkeypatch.context() as fault:
        if operation == "request_journal":
            fault.setattr(analysis.store, "append_jsonl", failing_request_journal)
        else:
            fault.setattr(analysis, "persist", failing_scoring_metadata)
        failed = score_all(client, access)
        assert_storage_failure(failed)
        assert failed["complete"] == 1 and failed["items"][0] == saved_item
        assert len(model) == 1, "A request must not start if its durable journal cannot be saved"

    # Recover through disk restoration, as after an operator expands the disk
    # and restarts the server; the completed item must never be billed again.
    analysis.jobs.clear()
    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["items"][0] == saved_item
    completed = score_all(client, access)
    assert completed["status"] == "complete", completed
    assert completed["items"][0] == saved_item
    assert len(model) == ready["total"]


def test_final_report_storage_failure_preserves_all_scores_and_resumes_without_calls(
        client, monkeypatch, model):
    access = start(client)
    ready = settled(client, access)

    def failing_report(*args, **kwargs):
        raise disk_full()

    with monkeypatch.context() as fault:
        fault.setattr(analysis.report, "generate_report", failing_report)
        failed = score_all(client, access)
        assert_storage_failure(failed)
        assert failed["complete"] == ready["total"]
        assert len(model) == ready["total"]
        saved_items = failed["items"]

    analysis.jobs.clear()
    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["items"] == saved_items
    completed = score_all(client, access)
    assert completed["status"] == "complete", completed
    assert completed["items"] == saved_items
    assert len(model) == ready["total"], "Rebuilding a report must not rescore completed items"


@pytest.mark.parametrize("operation", ["usage", "report"])
def test_reopening_an_interrupted_run_on_full_disk_still_shows_saved_scores(
        client, monkeypatch, model, operation):
    monkeypatch.setattr(analysis, "CHECKPOINT_SIZE", 1)
    access = start(client)
    ready = settled(client, access)
    assert client.post(url(access) + "/classify", json={"scope": "pilot"},
                       headers=headers(access, key=True)).status_code == 202
    checkpoint = settled(client, access)
    assert checkpoint["status"] == "checkpoint" and len(model) == 1
    saved_item = checkpoint["items"][0]
    job = analysis.jobs[access["run_id"]]
    job.status = "running"
    analysis.persist(job)
    analysis.jobs.clear()

    def failing_write(*args, **kwargs):
        raise disk_full()

    with monkeypatch.context() as fault:
        if operation == "usage":
            fault.setattr(analysis.store, "write_usage", failing_write)
        else:
            fault.setattr(analysis.report, "generate_report", failing_write)
        response = client.get(url(access), headers=headers(access))
        assert response.status_code == 200, response.text
        restored = response.json()
        assert_storage_failure(restored)
        assert restored["spec"] is not None and restored["can_continue"]
        assert restored["complete"] == 1 and restored["items"][0] == saved_item
        assert len(model) == 1

    completed = score_all(client, access)
    assert completed["status"] == "complete", completed
    assert completed["items"][0] == saved_item
    assert len(model) == ready["total"]


def test_retry_after_full_disk_reload_recovers_unrecorded_request_sequence(
        client, monkeypatch, model):
    monkeypatch.setattr(analysis, "CHECKPOINT_SIZE", 1)
    access = start(client)
    ready = settled(client, access)
    assert client.post(url(access) + "/classify", json={"scope": "pilot"},
                       headers=headers(access, key=True)).status_code == 202
    checkpoint = settled(client, access)
    assert checkpoint["status"] == "checkpoint" and len(model) == 1
    saved_item = checkpoint["items"][0]
    directory = analysis.jobs[access["run_id"]].directory
    original_persist = analysis.persist
    original_append = analysis.store.append_jsonl

    def failing_metadata_after_second_request(job):
        if job.call_sequence >= 2:
            raise disk_full()
        return original_persist(job)

    def failing_usage_recovery(path, entry):
        if path.name == "usage_ledger.jsonl" and entry["sequence"] == 2:
            raise disk_full()
        return original_append(path, entry)

    with monkeypatch.context() as fault:
        fault.setattr(analysis, "persist", failing_metadata_after_second_request)
        fault.setattr(analysis.store, "append_jsonl", failing_usage_recovery)
        failed = score_all(client, access)
        assert_storage_failure(failed)
        # The request journal has sequence 2, but its metadata update failed
        # before the provider was called. The old metadata still has sequence 1.
        job = analysis.jobs[access["run_id"]]
        client.portal.call(lambda: job.task)
        assert analysis.store.load_metadata(directory)["call_sequence"] == 1
        assert len(model) == 1
        analysis.jobs.clear()
        restored = client.get(url(access), headers=headers(access)).json()
        assert_storage_failure(restored)
        assert restored["items"][0] == saved_item
        assert analysis.jobs[access["run_id"]].call_sequence == 1

        # Restoration could not reconcile the usage journal while disk was full.
        # Retrying in this cached state must fail before another paid request.
        response = client.post(url(access) + "/classify", json={"scope": "all"},
                               headers=headers(access, key=True))
        assert response.status_code == 507, response.text
        assert len(model) == 1

    completed = score_all(client, access)
    assert completed["status"] == "complete", completed
    assert completed["items"][0] == saved_item
    assert len(model) == ready["total"]
    requests = [json.loads(line) for line in (directory / "requests.jsonl").read_text().splitlines()]
    ledger = [json.loads(line) for line in (directory / "usage_ledger.jsonl").read_text().splitlines()]
    expected_sequences = list(range(1, ready["total"] + 2))
    assert [entry["sequence"] for entry in requests] == expected_sequences
    assert [entry["sequence"] for entry in ledger] == expected_sequences
    assert ledger[1]["status"] == "interrupted" and not ledger[1]["usage_known"]

    analysis.jobs.clear()
    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["status"] == "complete" and restored["failure"] is None
    assert restored["items"] == completed["items"]
    assert restored["usage"] == completed["usage"]
    assert len(model) == ready["total"]
