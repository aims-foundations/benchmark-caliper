"""Durable pipeline access and recovery; all model/retrieval calls are offline."""

import asyncio
from copy import deepcopy
import gzip
import json
from threading import Event
import time

import httpx
from openai import AsyncOpenAI
import pytest

from website.server import adaptive_review, item_review
from website.server.review_checkpoints import AccessDenied, CheckpointError, Checkpoints
from website.server.tests.test_item_review import (
    BODY, KEY, HF_KEY, client, extracted_requirements, finished, mock_extraction_provider, start,
)
from website.server.tests.test_onet_grounding import (
    local_index, mock_mapper, response_body, seed_requirements, start_grounding,
)
from website.server.tests.test_benchmark_retrieval import full_bank, start_retrieval
from website.server.tests.test_benchmark_screening import (
    assessment, mock_screener, seed_retrieval, start_screening,
)
from website.server.tests.test_adaptive_screening import seed_selected, start_adaptive


def headers(access):
    return {"X-Review-Token": access["run_secret"]}


def saved_record(access):
    return json.loads(gzip.decompress(item_review.checkpoints().run_path(access["run_id"]).read_bytes()))


def restart_from_inflight_checkpoint(client, access):
    """Recreate the disk state at a hard stop, while draining the test's task."""
    path = item_review.checkpoints().run_path(access["run_id"])
    before_stop = path.read_bytes()
    assert client.post(f"/api/item-review/runs/{access['run_id']}/cancel", headers=headers(access)).status_code == 200
    item_review.jobs.clear()
    path.write_bytes(before_stop)


def test_private_atomic_json_and_shared_evidence_authenticates_before_loading(tmp_path, monkeypatch):
    store = Checkpoints(tmp_path / "private")
    evidence = {"rankings": [{"candidates": [{"question": "Keep the full question."}]}]}
    reference = store.save("first", "private-token", {"run_id": "first"}, retrieval=evidence)
    same = store.save("second", "second-token", {"run_id": "second"}, retrieval=deepcopy(evidence))
    assert same == reference
    assert len(list(store.directory.glob("evidence-*.json.gz"))) == 1
    assert store.directory.stat().st_mode & 0o777 == 0o700
    for path in store.directory.glob("*.json.gz"):
        assert path.stat().st_mode & 0o777 == 0o600
        assert "private-token" not in gzip.decompress(path.read_bytes()).decode()

    original = store.run_path("first").read_bytes()
    real_replace = __import__("os").replace

    def no_replace(source, target):
        if target == store.run_path("first"):
            raise OSError("Disk write failed")
        real_replace(source, target)

    monkeypatch.setattr("website.server.review_checkpoints.os.replace", no_replace)
    with pytest.raises(CheckpointError):
        store.save("first", "private-token", {"run_id": "first", "changed": True},
                   retrieval=evidence, retrieval_ref=reference)
    assert store.run_path("first").read_bytes() == original
    assert not list(store.directory.glob(".saving-*"))

    (store.directory / f"evidence-{reference}.json.gz").unlink()
    with pytest.raises(AccessDenied, match="invalid_token"):
        store.load("first", "wrong-token")
    with pytest.raises(CheckpointError):
        store.load("first", "private-token")


@pytest.mark.parametrize("damage", ["run", "evidence"])
def test_truncated_checkpoint_is_a_sanitized_storage_error(tmp_path, damage):
    store = Checkpoints(tmp_path / "private")
    reference = store.save("run", "access", {"run_id": "run"}, retrieval={"private": "evidence"})
    path = store.run_path("run") if damage == "run" else store.directory / f"evidence-{reference}.json.gz"
    path.write_bytes(path.read_bytes()[:14])
    with pytest.raises(CheckpointError, match="Could not read the review checkpoint"):
        store.load("run", "access")


def test_grounded_review_survives_long_pause_and_restart_then_retrieves(client, monkeypatch, local_index, request):
    calls = mock_mapper(monkeypatch)
    access = start_grounding(client, seed_requirements())
    original = finished(client, access).json()
    job = item_review.jobs[access["run_id"]]
    job.finished_at = time.monotonic() - 365 * 86400
    assert client.get(f"/api/item-review/runs/{job.run_id}", headers=headers(access)).json() == original
    asyncio.run(item_review.shutdown())
    assert not item_review.jobs

    url = f"/api/item-review/runs/{access['run_id']}"
    assert client.get(url).status_code == 404
    assert client.get(url, headers={"X-Review-Token": "incorrect"}).status_code == 404
    assert not item_review.jobs
    assert client.get(url, headers=headers(access)).json() == original
    assert len(calls) == 1  # Reopening a saved result makes no paid request.
    request.getfixturevalue("full_bank")
    retrieved = finished(client, start_retrieval(client, access)).json()
    assert retrieved["status"] == "completed"
    assert retrieved["grounding"] == original["grounding"]
    assert retrieved["requirements"] == original["requirements"]

    for path in item_review.checkpoints().directory.glob("*.json.gz"):
        text = gzip.decompress(path.read_bytes()).decode()
        for secret in (KEY, HF_KEY, access["run_secret"]):
            assert secret not in text


def test_completed_cache_eviction_does_not_expire_saved_runs(client, monkeypatch):
    monkeypatch.setattr(item_review, "MAX_RETAINED", 3)
    mock_extraction_provider(monkeypatch, extracted_requirements(BODY["deployment"]))
    reviews = []
    for _ in range(8):
        access = start(client, {**BODY, "mode": "requirements"})
        result = finished(client, access).json()
        assert result["status"] == "completed"
        reviews.append((access, result))
        assert len(item_review.jobs) <= 1
    assert reviews[0][0]["run_id"] not in item_review.jobs
    assert len(list(item_review.checkpoints().directory.glob("*.json.gz"))) == 8
    for access, original in reviews:
        assert client.get(f"/api/item-review/runs/{access['run_id']}", headers=headers(access)).json() == original
        assert len(item_review.jobs) <= 1


def test_pipeline_cache_eviction_keeps_active_runs_and_open_downloads(client):
    for run_id, active, downloads in (("old", False, 0), ("active", True, 0),
                                      ("download", False, 1), ("latest", False, 0)):
        job = item_review.ReviewJob(run_id, "access", "owner",
                                   item_review.ReviewRequest(**BODY, mode="requirements"),
                                   inventory={}, downloads=downloads,
                                   finished_at=None if active else time.monotonic())
        item_review.checkpoint(job)
        item_review.jobs[run_id] = job
    item_review.sweep()
    assert set(item_review.jobs) == {"active", "download", "latest"}
    assert item_review.checkpoints().load("old", "access")[0]["run_id"] == "old"


def test_storage_failure_before_launch_makes_no_paid_calls(client, monkeypatch, caplog):
    def cannot_save(*args, **kwargs):
        raise CheckpointError("Private failure detail")

    monkeypatch.setattr(Checkpoints, "save", cannot_save)
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("No paid client may be opened"))
    response = client.post("/api/item-review/runs", json={**BODY, "mode": "requirements"},
                           headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 503
    assert "No work was started" in response.text
    assert not item_review.jobs
    assert KEY not in response.text + caplog.text


def test_completion_write_failure_does_not_claim_results_are_saved(client, monkeypatch):
    real_save = Checkpoints.save

    def fail_finished(self, run_id, secret, state, **kwargs):
        if state["finished"]:
            raise CheckpointError("Disk is full")
        return real_save(self, run_id, secret, state, **kwargs)

    monkeypatch.setattr(Checkpoints, "save", fail_finished)
    mock_extraction_provider(monkeypatch, extracted_requirements(BODY["deployment"]))
    access = start(client, {**BODY, "mode": "requirements"})
    result = finished(client, access).json()
    assert result["status"] == "failed"
    assert "could not save" in result["message"]
    assert result["requirements"] is not None
    assert item_review.jobs[access["run_id"]]._checkpoint_saved is False
    assert saved_record(access)["run"]["requirements"] is None


def block_second_assessment(monkeypatch):
    entered, calls = Event(), []

    async def respond(request):
        row = json.loads(json.loads(request.content)["input"])["item"]
        calls.append(row["id"])
        if len(calls) == 2:
            entered.set()
            await asyncio.Event().wait()
        return httpx.Response(200, json=response_body(assessment(row)))

    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: AsyncOpenAI(
        **kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))))
    return entered, calls


def test_partial_screening_restart_retains_assessments_and_reuses_evidence_blob(client, monkeypatch):
    monkeypatch.setattr(item_review, "REVIEW_CONCURRENCY", 1)
    entered, original_calls = block_second_assessment(monkeypatch)
    access = start_screening(client, seed_retrieval(facets=1, per_facet=3))
    assert entered.wait(3)
    record = saved_record(access)
    assert record["run"]["finished"] is False
    assert len(record["run"]["screening"]["items"]) == 1
    assert record["retrieval_ref"]
    restart_from_inflight_checkpoint(client, access)

    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("Reopening is read-only"))
    restored = client.get(f"/api/item-review/runs/{access['run_id']}", headers=headers(access)).json()
    assert restored["status"] == "cancelled"
    assert "server restart" in restored["message"]
    assert len(restored["screening"]["items"]) == 1
    calls = mock_screener(monkeypatch)
    resumed = start_screening(client, access)
    result = finished(client, resumed).json()
    assert result["status"] == "completed"
    assert len(calls) == 2
    assert result["screening"]["items"][0]["screened_run_id"] == access["run_id"]
    assert saved_record(resumed)["retrieval_ref"] == record["retrieval_ref"]
    assert len(list(item_review.checkpoints().directory.glob("evidence-*.json.gz"))) == 1
    assert original_calls == ["0-0", "0-1"]


def test_adaptive_restart_preserves_unknown_charge_and_completed_assessment(client, monkeypatch):
    entered, original_calls = block_second_assessment(monkeypatch)
    access = start_adaptive(client, seed_selected(per_facet=50), {
        "input_price_per_million": 1.0, "cached_input_price_per_million": 0.5,
        "output_price_per_million": 2.0,
    })
    assert entered.wait(3)
    original = saved_record(access)["run"]["adaptive"]
    assert [attempt["status"] for attempt in original["attempts"]] == ["complete", "pending"]
    restart_from_inflight_checkpoint(client, access)
    restored = client.get(f"/api/item-review/runs/{access['run_id']}", headers=headers(access)).json()
    assert restored["status"] == "cancelled"
    state = restored["adaptive"]
    assert [attempt["status"] for attempt in state["attempts"]] == ["complete", "unknown"]
    assert state["cost"] == original["cost"]
    assert state["cost"]["reserved_usd"] > 0
    calls = mock_screener(monkeypatch)
    resumed = start_adaptive(client, access)
    result = finished(client, resumed).json()
    assert result["status"] == "completed", result["message"]
    assert len(calls) == 1
    assert json.loads(calls[0]["input"])["item"]["id"] == "0-49"
    assert original_calls == ["0-48", "0-49"]
    assert [attempt["status"] for attempt in result["adaptive"]["attempts"]] == ["complete", "unknown", "complete"]
    assert result["adaptive"]["cost"]["reserved_usd"] == state["cost"]["reserved_usd"]


def test_access_diagnostics_distinguish_missing_run_and_bad_token_without_secrets(client, caplog):
    access = seed_requirements()
    job = item_review.jobs[access["run_id"]]
    item_review.checkpoint(job)
    item_review.jobs.clear()
    with caplog.at_level("INFO", logger=item_review.__name__):
        assert client.get("/api/item-review/runs/missing", headers={"X-Review-Token": "wrong"}).status_code == 404
        assert client.get(f"/api/item-review/runs/{job.run_id}", headers={"X-Review-Token": "wrong"}).status_code == 404
        assert client.get(f"/api/item-review/runs/{job.run_id}").status_code == 404
    assert "reason=missing_run" in caplog.text
    assert "reason=invalid_token" in caplog.text
    assert "reason=missing_token" in caplog.text
    assert job.secret not in caplog.text and KEY not in caplog.text
