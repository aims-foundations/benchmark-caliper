"""Step 6 HTTP continuation with the real local selector and saved fixtures."""

import asyncio
from copy import deepcopy
import json
import time
from threading import Event

import pytest

from bayesian_auditing.screening import AsyncItemScreener, ScreeningAssessment, SCREENING_VERSION, gate_for
from bayesian_auditing.screening_queue import allocate_initial_screening
from bayesian_auditing.selection import SelectionIncomplete
from website.server import item_review
from website.server.tests.test_benchmark_screening import (
    assessment, export, mock_screener, seed_retrieval, start_screening,
)
from website.server.tests.test_item_review import BODY, KEY, HF_KEY, client, finished


def seed_screening(*, facets=3, per_facet=24):
    access = seed_retrieval(facets=facets, per_facet=per_facet)
    job = item_review.jobs[access["run_id"]]
    job.request = job.request.model_copy(update={"mode": "screening"})
    screener = AsyncItemScreener(None)
    allocation = allocate_initial_screening(job.benchmark_retrieval["queues"])
    originals = item_review.screening_candidates(
        job.benchmark_retrieval, item_review.Requirements.model_validate(job.requirements))
    items = []
    for entry in allocation["items"]:
        candidate = originals[entry["facet_id"], entry["item_id"]]
        value = assessment(candidate["evidence"]["item"], entry["facet_id"])
        items.append({**deepcopy(candidate), "status": "complete", "assessment": value,
                      "gate": gate_for(ScreeningAssessment.model_validate(value)),
                      "acquisition": {key: entry[key] for key in ("queue_id", "facet_id")},
                      "screened_run_id": job.run_id, "usage": {"input_tokens": 100}})
    job.screening = {
        "policy": {"version": SCREENING_VERSION, "initial_budget": 48},
        "allocation": allocation, "items": items,
        "model": {"version": SCREENING_VERSION, "model": screener.model, "prompt": screener.prompt,
                  "reasoning_effort": screener.reasoning_effort,
                  "max_output_tokens": screener.max_output_tokens,
                  "output_schema": ScreeningAssessment.model_json_schema()},
    }
    return access


def test_selection_reports_unavailable_stored_screening_evidence(client, monkeypatch):
    access = seed_screening(facets=1, per_facet=1)
    job = item_review.jobs[access["run_id"]]
    store = item_review.candidate_store()
    reference = store.compact(job.screening["items"][0])
    job.screening["items"] = [reference]
    (store.directory / f"{reference['_candidate_ref']}.json.gz").unlink()
    monkeypatch.setattr(item_review, "select_collection", lambda *args, **kwargs: pytest.fail("Do not start selection"))
    response = client.post(f"/api/item-review/runs/{access['run_id']}/select", json={},
                           headers={"X-Review-Token": access["run_secret"]})
    assert response.status_code == 503
    assert "saved candidate evidence" in response.json()["detail"].lower()
    assert reference["_candidate_ref"] not in response.text
    assert str(store.directory) not in response.text
    assert len(item_review.jobs) == 1


def start_selection(client, source):
    response = client.post(f"/api/item-review/runs/{source['run_id']}/select", json={},
                           headers={"X-Review-Token": source["run_secret"]})
    assert response.status_code == 202, response.text
    assert response.headers["cache-control"] == "no-store"
    return response.json()


def forbid_external_calls(monkeypatch):
    for name in ("AsyncOpenAI", "get_token", "inventory", "retrieve_benchmarks", "screen_benchmarks"):
        monkeypatch.setattr(item_review, name, lambda *args, **kwargs: pytest.fail("Selection is entirely local"))


def test_selects_thirty_total_preserves_every_task_and_full_export(client, monkeypatch):
    source = seed_screening()
    original = finished(client, source).json()
    forbid_external_calls(monkeypatch)
    access = start_selection(client, source)
    result = finished(client, access).json()
    assert result["mode"] == "selection" and result["status"] == "completed"
    selection = result["selection"]
    assert selection["limit"] == selection["selected_count"] == 30
    assert selection["eligible_count"] == 48 and selection["fully_satisfied"] is True
    assert all(entry["minimum"] == 1 and entry["selected_count"] >= 1 for entry in selection["task_coverage"])
    assert sum(entry["selected_count"] for entry in selection["task_coverage"]) == 30
    assert selection["total_quality"] == 120
    assert all(entry["quality_score"] == 4 for entry in selection["items"])
    assert result["selection_run_id"] == access["run_id"]
    assert result["selection_input"] == {"allocated": 48, "screened": 48, "errors": 0, "pending": 0}
    assert result["usage"] == {} and result["screening"] == original["screening"]
    assert finished(client, source).json() == original
    exported = export(client, access)
    assert exported.json()["selection"] == selection
    assert exported.json()["retrieval"] == item_review.jobs[source["run_id"]].benchmark_retrieval
    assert "benchmark-selection-" in exported.headers["content-disposition"]
    for secret in (KEY, HF_KEY, source["run_secret"], access["run_secret"]):
        assert secret not in exported.text


def test_partial_screening_uses_valid_results_and_recomputes_gate(client, monkeypatch):
    source = seed_screening()
    job = item_review.jobs[source["run_id"]]
    job.status = "cancelled"
    job.screening["items"] = job.screening["items"][:6]
    job.screening["items"][1].update(status="error", error="Invalid model response")
    # A stale saved pass flag cannot admit an item whose current gated rating fails.
    job.screening["items"][2]["assessment"]["ratings"]["input_content"]["score"] = 2
    forbid_external_calls(monkeypatch)
    result = finished(client, start_selection(client, source)).json()
    assert result["status"] == "completed"
    assert result["selection_input"] == {"allocated": 48, "screened": 5, "errors": 1, "pending": 42}
    assert result["selection"]["selected_count"] == 4
    assert result["selection"]["excluded_counts"]["errors"] == 1
    assert result["selection"]["excluded_counts"]["gate_fail"] == 1


def test_missing_task_reports_gap_without_lowering_threshold(client, monkeypatch):
    source = seed_screening(facets=3, per_facet=2)
    job = item_review.jobs[source["run_id"]]
    for item in job.screening["items"]:
        if item["acquisition"]["facet_id"] == "task-2":
            item["assessment"]["ratings"]["output_ontology"]["score"] = 2
    forbid_external_calls(monkeypatch)
    result = finished(client, start_selection(client, source)).json()["selection"]
    assert result["selected_count"] == 4 and result["constraints_feasible"] is False
    assert result["fully_satisfied"] is False
    assert result["task_coverage"][2] == {"facet_id": "task-2", "minimum": 1,
                                          "eligible_count": 0, "selected_count": 0, "shortfall": 1}
    assert any("task-2" in gap for gap in result["gaps"])


def test_all_ineligible_produces_empty_collection_and_coverage_gaps(client, monkeypatch):
    source = seed_screening(facets=2, per_facet=1)
    for item in item_review.jobs[source["run_id"]].screening["items"]:
        item["assessment"]["ratings"]["input_ontology"]["score"] = 1
    forbid_external_calls(monkeypatch)
    result = finished(client, start_selection(client, source)).json()
    assert result["status"] == "completed"
    assert result["selection"]["selected_item_ids"] == [] and result["selection"]["total_quality"] == 0
    assert all(entry["shortfall"] == 1 for entry in result["selection"]["task_coverage"])


def test_selection_requires_finished_private_source_and_rejects_limit_override(client):
    source = seed_screening(facets=1, per_facet=1)
    job = item_review.jobs[source["run_id"]]
    url = f"/api/item-review/runs/{source['run_id']}/select"
    headers = {"X-Review-Token": source["run_secret"]}
    assert client.post(url).status_code == 404
    assert client.post(url, headers={"X-Review-Token": "wrong"}).status_code == 404
    assert client.post(url, headers=headers, json={"limit": 30}).status_code == 422
    assert client.post(url, headers=headers, json={"per_task": 30}).status_code == 422
    job.finished_at = None
    assert client.post(url, headers=headers).status_code == 409
    job.finished_at = time.monotonic()
    job.request = job.request.model_copy(update={"mode": "retrieval"})
    assert client.post(url, headers=headers).status_code == 409
    job.request = job.request.model_copy(update={"mode": "screening"})
    job.finished_at -= item_review.RETENTION_SECONDS + 1
    continued = client.post(url, headers=headers)
    assert continued.status_code == 202
    assert finished(client, continued.json()).json()["status"] == "completed"
    assert client.post("/api/item-review/runs", json={**BODY, "mode": "selection"},
                       headers={"X-OpenAI-Key": KEY}).status_code == 400


@pytest.mark.parametrize("change", ["row", "assessment", "quote", "allocation", "duplicate", "sources"])
def test_corrupt_source_is_rejected_before_solver(client, monkeypatch, change):
    source = seed_screening(facets=1, per_facet=1)
    job = item_review.jobs[source["run_id"]]
    item = job.screening["items"][0]
    if change == "row":
        item["evidence"]["item"]["content"] = "changed row"
    elif change == "assessment":
        item["assessment"]["task"]["matched_facet_ids"] = ["not-extracted"]
    elif change == "quote":
        item["assessment"]["task"]["evidence"] = ["not present in item"]
    elif change == "allocation":
        job.screening["allocation"]["budget"] = 51
    elif change == "duplicate":
        job.screening["items"].append(deepcopy(item))
    else:
        item["sources"][0]["row"] = 999
    monkeypatch.setattr(item_review, "select_collection", lambda *args, **kwargs: pytest.fail("Invalid source"))
    response = client.post(f"/api/item-review/runs/{source['run_id']}/select",
                           headers={"X-Review-Token": source["run_secret"]})
    assert response.status_code == 409


def test_capacity_is_inherited_without_requesting_an_api_key(client):
    source = seed_screening(facets=1, per_facet=1)
    job = item_review.jobs[source["run_id"]]
    occupied = item_review.ReviewJob("occupied", "secret", job.owner_hash, job.request, inventory={})
    item_review.jobs[occupied.run_id] = occupied
    response = client.post(f"/api/item-review/runs/{source['run_id']}/select",
                           headers={"X-Review-Token": source["run_secret"]})
    assert response.status_code == 429


def test_timeout_keeps_previous_accepted_collection_and_origin(client, monkeypatch):
    source = seed_screening(facets=1, per_facet=2)
    first = start_selection(client, source)
    original = finished(client, first).json()

    def timeout(*args, **kwargs):
        raise SelectionIncomplete("private solver diagnostics")

    monkeypatch.setattr(item_review, "select_collection", timeout)
    second = start_selection(client, first)
    result = finished(client, second).json()
    assert result["status"] == "failed"
    assert result["selection"] == original["selection"]
    assert result["selection_run_id"] == first["run_id"]
    assert "private solver diagnostics" not in json.dumps(result)
    assert finished(client, first).json() == original


def test_cancel_drains_solver_without_publishing_result(client, monkeypatch):
    source = seed_screening(facets=1, per_facet=2)
    started, stopped = Event(), Event()

    def wait_for_cancel(*args, cancelled, **kwargs):
        started.set()
        while not cancelled():
            time.sleep(.001)
        stopped.set()
        raise InterruptedError("cancelled")

    monkeypatch.setattr(item_review, "select_collection", wait_for_cancel)
    access = start_selection(client, source)
    assert started.wait(2)
    result = client.post(f"/api/item-review/runs/{access['run_id']}/cancel",
                         headers={"X-Review-Token": access["run_secret"]}).json()
    assert stopped.is_set() and result["status"] == "cancelled"
    assert result["selection"] is None and result["selection_run_id"] is None


def test_continue_screening_after_selection_preserves_achieved_coverage(client, monkeypatch):
    source = seed_screening(facets=2, per_facet=2)
    job = item_review.jobs[source["run_id"]]
    job.status = "cancelled"
    job.screening["items"] = job.screening["items"][:1]
    first_selection = start_selection(client, source)
    initial = finished(client, first_selection).json()
    assert initial["selection"]["selected_count"] == 1
    calls = mock_screener(monkeypatch)
    screening = start_screening(client, first_selection)
    completed = finished(client, screening).json()
    assert completed["status"] == "completed" and len(calls) == 3
    assert completed["selection"] == initial["selection"]
    forbid_external_calls(monkeypatch)
    next_selection = start_selection(client, screening)
    updated = finished(client, next_selection).json()
    assert updated["selection"]["selected_count"] == 4
    assert updated["selection"]["previous_selected_item_ids"] == initial["selection"]["selected_item_ids"]
    assert updated["selection"]["preserved_coverage"]["tasks"] == [{"facet_id": "task-0", "minimum": 1}]


def test_selection_export_preserves_accepted_snapshot_during_retry(client):
    access = start_selection(client, seed_screening(facets=1, per_facet=1))
    original = finished(client, access).json()
    job = item_review.jobs[access["run_id"]]

    async def download():
        response = await item_review.export_review(job.run_id, job.secret)
        job.selection = {"new": "future result"}
        return "".join([chunk async for chunk in response.body_iterator])

    exported = json.loads(asyncio.run(download()))
    assert exported["selection"] == original["selection"]
    assert job.downloads == 0
