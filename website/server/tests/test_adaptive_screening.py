"""Adaptive continuation through real HTTP, with offline screening responses."""

import asyncio
from copy import deepcopy
import json
import time
from threading import Event

import httpx
from openai import AsyncOpenAI
import pytest

from bayesian_auditing.selection import select_collection, SelectionIncomplete
from website.server import item_review
from website.server.tests.test_benchmark_screening import (
    assessment, export, mock_screener, seed_retrieval, start_screening,
)
from website.server.tests.test_benchmark_selection import seed_screening, start_selection
from website.server.tests.test_item_review import BODY, KEY, HF_KEY, client
from website.server.tests.test_onet_grounding import response_body


def seed_selected(*, facets=1, per_facet=56):
    access = seed_screening(facets=facets, per_facet=per_facet)
    job = item_review.jobs[access["run_id"]]
    job.request = job.request.model_copy(update={"mode": "selection"})
    job.selection = select_collection(
        item_review.Requirements.model_validate(job.requirements), job.screening["items"])
    job.selection_run_id = job.run_id
    return access


def start_adaptive(client, source, body=None):
    response = client.post(f"/api/item-review/runs/{source['run_id']}/adapt", json=body or {}, headers={
        "X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY,
    })
    assert response.status_code == 202, response.text
    assert response.headers["cache-control"] == "no-store"
    return response.json()


def finished(client, access):
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        response = client.get(f"/api/item-review/runs/{access['run_id']}",
                              headers={"X-Review-Token": access["run_secret"]})
        assert response.status_code == 200
        if response.json()["status"] not in {"preparing", "running"}:
            return response
        time.sleep(.01)
    pytest.fail("Adaptive screening did not finish")


def forbid_retrieval(monkeypatch):
    for name in ("get_token", "inventory", "retrieve_benchmarks"):
        monkeypatch.setattr(item_review, name, lambda *args, **kwargs: pytest.fail("Use saved retrieval"))


def test_initial_selection_snapshot_is_independent_of_later_collection_changes(client):
    from bayesian_auditing.screening_budget import AdaptiveSettings
    from website.server import adaptive_review

    source = seed_selected(per_facet=3)
    job = item_review.jobs[source["run_id"]]
    original = deepcopy(job.selection)
    state = adaptive_review.initialize(job, AdaptiveSettings())
    assert state["initial_selection"] == original
    assert state["initial_selection_run_id"] == source["run_id"]

    job.selection["selected_item_ids"].clear()
    job.selection["task_coverage"][0]["selected_count"] = 0
    job.selection_run_id = "later-adaptive-run"
    assert state["initial_selection"] == original
    assert state["initial_selection_run_id"] == source["run_id"]


def test_caps_total_at_160_uses_eight_unseen_per_batch_and_keeps_initial_outcomes(client, monkeypatch):
    source = seed_selected(per_facet=180)
    original = finished(client, source).json()
    calls = mock_screener(monkeypatch)
    forbid_retrieval(monkeypatch)
    access = start_adaptive(client, source, {"seed": 7})
    result = finished(client, access).json()
    assert result["mode"] == "adaptive" and result["status"] == "completed", result["message"]
    adaptive = result["adaptive"]
    assert adaptive["initial_selection"] == original["selection"]
    assert adaptive["initial_selection_run_id"] == source["run_id"]
    assert adaptive["frozen"] is True and adaptive["stop_reason"] == "candidate_limit"
    assert adaptive["screened_count"] == adaptive["acquired_count"] == 160
    assert len(calls) == 112
    rows = [json.loads(call["input"])["item"]["id"] for call in calls]
    assert len(set(rows)) == 112 and all(int(row.split("-")[1]) >= 48 for row in rows)
    batches = adaptive["batches"]
    assert batches[0]["number"] == 0 and batches[0]["kind"] == "initial"
    assert len(batches[0]["item_ids"]) == 48
    assert batches[0]["selected_item_ids"] == original["selection"]["selected_item_ids"]
    assert [len(batch["item_ids"]) for batch in batches[1:]] == [8] * 14
    assert all(batch["status"] == "committed" for batch in batches)
    assert len({item_id for batch in batches for item_id in batch["item_ids"]}) == 160
    initial_outcomes = batches[0]["outcomes"]
    assert sum(outcome["retained"] for outcome in initial_outcomes) == 30
    assert {outcome["item_id"] for outcome in initial_outcomes if outcome["retained"]} == set(
        original["selection"]["selected_item_ids"])
    successes = sum(outcome["retained"] for batch in batches for outcome in batch["outcomes"])
    assert len(adaptive["queue_statistics"]) == 2
    for stats in adaptive["queue_statistics"]:
        assert stats["successes"] == successes and stats["failures"] == 160 - successes
        assert stats["alpha"] == successes + 1 and stats["beta"] == 161 - successes
        assert stats["remaining"] == 20 and stats["coverage_weight"] == 1
        assert stats["priority"] == stats["estimated_yield"]
    assert result["selection"]["selected_count"] == 30
    assert result["selection"]["task_coverage"][0]["selected_count"] == 30
    assert len(result["screening"]["items"]) == 160
    assert result["screening"]["allocation"] == original["screening"]["allocation"]
    assert result["usage"]["input_tokens"] == 11200
    assert finished(client, source).json() == original
    exported = export(client, access)
    assert exported.json()["adaptive"] == adaptive
    assert exported.json()["selection"] == result["selection"]
    assert exported.json()["retrieval"] == item_review.jobs[source["run_id"]].benchmark_retrieval
    assert "adaptive" in exported.headers["content-disposition"]
    for secret in (KEY, HF_KEY, source["run_secret"], access["run_secret"]):
        assert secret not in exported.text


def test_adaptive_nonliteral_evidence_is_preserved_through_export_and_restart(client, monkeypatch):
    source = seed_selected(per_facet=49)

    returned_evidence = "\nExplain why the sum of two even numbers must also be even.\n"

    def nonliteral_failure(value, row):
        value["ratings"]["input_form"].update(score=2, evidence=[returned_evidence])
        return value

    calls = mock_screener(monkeypatch, nonliteral_failure)
    access = start_adaptive(client, source)
    result = finished(client, access).json()
    assert result["status"] == "completed", result["message"]
    assert len(calls) == 1
    original_row = json.loads(calls[0]["input"])["item"]
    record = next(item for item in result["screening"]["items"]
                  if item["screened_run_id"] == access["run_id"])
    assert record["status"] == "complete" and record["gate"]["status"] == "fail"
    assert record["evidence"]["item"] == original_row
    assert record["assessment"]["ratings"]["input_form"]["evidence"] == [returned_evidence]
    assert "evidence_adjustments" not in record
    assert record["item_id"] not in result["selection"]["selected_item_ids"]
    assert export(client, access).json()["screening"] == result["screening"]
    item_review.jobs.clear()
    assert finished(client, access).json() == result
    assert export(client, access).json()["screening"] == result["screening"]
    assert len(calls) == 1


def test_small_exhausted_pool_freezes_without_opening_model_client(client, monkeypatch):
    source = seed_selected(per_facet=3)
    original = finished(client, source).json()
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("No unseen items"))
    result = finished(client, start_adaptive(client, source)).json()
    assert result["status"] == "completed", result["message"]
    assert result["adaptive"]["frozen"] is True
    assert result["adaptive"]["stop_reason"] == "queues_exhausted"
    assert result["adaptive"]["screened_count"] == 3
    assert len(result["adaptive"]["batches"]) == 1
    assert result["selection"] == original["selection"]
    assert result["selection_run_id"] == source["run_id"]
    assert result["usage"] == {}


def test_same_rows_in_all_source_and_source_queue_are_screened_once(client, monkeypatch):
    source = seed_selected(per_facet=61)
    calls = mock_screener(monkeypatch)
    result = finished(client, start_adaptive(client, source)).json()
    assert result["status"] == "completed", result["message"]
    adaptive = result["adaptive"]
    assert adaptive["stop_reason"] == "queues_exhausted"
    assert [len(batch["item_ids"]) for batch in adaptive["batches"]] == [48, 8, 5]
    assert len(calls) == 13
    assert len({item["item_id"] for item in result["screening"]["items"]}) == 61
    assert result["selection"]["selected_count"] == 30


def test_compact_retrieval_flows_through_screening_selection_and_adaptive_with_complete_public_rows(client, monkeypatch):
    source = seed_retrieval(facets=1, per_facet=61)
    source_job = item_review.jobs[source["run_id"]]
    stage_jobs = [source_job]
    original_retrieval = deepcopy(source_job.benchmark_retrieval)
    original_candidates = original_retrieval["rankings"][0]["candidates"]
    original_rows = {item["item_id"]: item["evidence"]["item"] for item in original_candidates}
    store = item_review.candidate_store()
    for ranking in source_job.benchmark_retrieval["rankings"]:
        ranking["candidates"] = [store.compact(item) for item in ranking["candidates"]]
    compact_retrieval = deepcopy(source_job.benchmark_retrieval)
    calls = mock_screener(monkeypatch)
    forbid_retrieval(monkeypatch)

    screening_access = start_screening(client, source)
    initial = finished(client, screening_access).json()
    assert initial["status"] == "completed", initial["message"]
    assert len(calls) == len(initial["screening"]["items"]) == 48
    stage_jobs.append(item_review.jobs[screening_access["run_id"]])
    selection_access = start_selection(client, screening_access)
    selected = finished(client, selection_access).json()
    assert selected["status"] == "completed", selected["message"]
    assert selected["selection"]["selected_count"] == 30
    assert len(calls) == 48
    stage_jobs.append(item_review.jobs[selection_access["run_id"]])

    access = start_adaptive(client, selection_access)
    result = finished(client, access).json()
    stage_jobs.append(item_review.jobs[access["run_id"]])
    assert result["status"] == "completed", result["message"]
    assert result["adaptive"]["frozen"] is True
    assert result["adaptive"]["stop_reason"] == "queues_exhausted"
    assert [len(batch["item_ids"]) for batch in result["adaptive"]["batches"]] == [48, 8, 5]
    assert all(batch["status"] == "committed" for batch in result["adaptive"]["batches"])
    assert result["selection"]["selected_count"] == 30
    assert result["selection"]["fully_satisfied"] is True
    assert len(calls) == len(result["screening"]["items"]) == 61
    sent_rows = [json.loads(call["input"])["item"] for call in calls]
    assert {row["id"]: row for row in sent_rows} == {row["id"]: row for row in original_rows.values()}

    exported = export(client, access).json()
    assert exported["retrieval"] == original_retrieval
    assert exported["screening"] == result["screening"]
    assert exported["selection"] == result["selection"]
    for item in exported["screening"]["items"]:
        assert item["evidence"]["item"] == original_rows[item["item_id"]]
        assert item["status"] == "complete" and item["gate"]["status"] == "pass"
    assert "_candidate_ref" not in json.dumps(exported)

    queue = next(queue for queue in original_retrieval["queues"] if queue["source"] is None)
    browsed = []
    for page in range(1, (61 + item_review.RESULTS_PAGE_SIZE - 1) // item_review.RESULTS_PAGE_SIZE + 1):
        response = client.get(f"/api/item-review/runs/{access['run_id']}/candidates",
                              params={"queue_id": queue["queue_id"], "page": page},
                              headers={"X-Review-Token": access["run_secret"]})
        assert response.status_code == 200
        browsed.extend(response.json()["items"])
    assert browsed == original_candidates

    for job in stage_jobs:
        assert job.benchmark_retrieval == compact_retrieval
        if job.screening is not None:
            assert all("_candidate_ref" in item and "evidence" not in item for item in job.screening["items"])
    restored, _ = item_review.checkpoints().load(access["run_id"], access["run_secret"])
    assert restored["benchmark_retrieval"] == compact_retrieval
    assert restored["screening"] == item_review.jobs[access["run_id"]].screening


def test_requires_private_finished_selection_complete_initial_results_and_fresh_key(client):
    source = seed_selected(per_facet=3)
    job = item_review.jobs[source["run_id"]]
    url = f"/api/item-review/runs/{source['run_id']}/adapt"
    headers = {"X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY}
    assert client.post(url).status_code == 404
    assert client.post(url, headers={**headers, "X-Review-Token": "wrong"}).status_code == 404
    assert client.post(url, headers={"X-Review-Token": source["run_secret"]}).status_code == 401
    assert client.post(url, headers={**headers, "X-OpenAI-Key": "x" * 513}).status_code == 400
    job.finished_at = None
    assert client.post(url, headers=headers).status_code == 409
    job.finished_at = time.monotonic()
    job.request = job.request.model_copy(update={"mode": "screening"})
    assert client.post(url, headers=headers).status_code == 409
    job.request = job.request.model_copy(update={"mode": "selection"})
    saved = job.screening["items"].pop()
    assert client.post(url, headers=headers).status_code == 409
    job.screening["items"].append({**saved, "status": "error", "error": "Invalid response"})
    assert client.post(url, headers=headers).status_code == 409
    assert client.post("/api/item-review/runs", json={**BODY, "mode": "adaptive"},
                       headers={"X-OpenAI-Key": KEY}).status_code == 400


@pytest.mark.parametrize("body", [
    {"budget": 200}, {"batch_size": 9}, {"seed": -1}, {"seed": True}, {"seed": 2 ** 32},
    {"max_cost_usd": 0}, {"max_cost_usd": 1},
    {"input_price_per_million": 1},
    {"max_cost_usd": 1, "input_price_per_million": 1,
     "cached_input_price_per_million": 2, "output_price_per_million": 2},
])
def test_rejects_invalid_settings_and_fixed_policy_overrides(client, body):
    source = seed_selected(per_facet=1)
    response = client.post(f"/api/item-review/runs/{source['run_id']}/adapt", json=body, headers={
        "X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY})
    assert response.status_code == 422


def test_owner_capacity_is_inherited(client):
    source = seed_selected(per_facet=1)
    job = item_review.jobs[source["run_id"]]
    occupied = item_review.ReviewJob("occupied", "secret", job.owner_hash, job.request, inventory={})
    item_review.jobs[occupied.run_id] = occupied
    response = client.post(f"/api/item-review/runs/{source['run_id']}/adapt", headers={
        "X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY})
    assert response.status_code == 429


def test_cost_limit_can_freeze_before_any_paid_request(client, monkeypatch):
    source = seed_selected()
    original = finished(client, source).json()
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("Budget cannot fund request"))
    result = finished(client, start_adaptive(client, source, {
        "max_cost_usd": .000001, "input_price_per_million": 1,
        "cached_input_price_per_million": .5, "output_price_per_million": 2,
    })).json()
    assert result["status"] == "completed", result["message"]
    adaptive = result["adaptive"]
    assert adaptive["frozen"] is True and adaptive["stop_reason"] == "cost_limit"
    assert adaptive["screened_count"] == adaptive["acquired_count"] == 48
    assert adaptive["cost"]["spent_usd"] == adaptive["cost"]["reserved_usd"] == 0
    assert adaptive["cost"]["scope"] == "adaptive_screening"
    assert adaptive["attempts"] == []
    assert result["selection"] == original["selection"]


def test_cost_uses_cached_tokens_and_only_new_calls(client, monkeypatch):
    source = seed_selected()
    calls = mock_screener(monkeypatch)
    result = finished(client, start_adaptive(client, source, {
        "max_cost_usd": 10, "input_price_per_million": 1,
        "cached_input_price_per_million": .5, "output_price_per_million": 2,
    })).json()
    assert result["status"] == "completed", result["message"]
    assert len(calls) == 8
    cost = result["adaptive"]["cost"]
    assert cost["spent_usd"] == pytest.approx(8 * (90 + 10 * .5 + 90 * 2) / 1_000_000)
    assert cost["reserved_usd"] == 0 and cost["unknown_attempts"] == 0
    assert len(result["adaptive"]["attempts"]) == 8


@pytest.mark.parametrize("complete_breakdown", [True, False])
def test_cache_write_usage_survives_sdk_and_export_and_settles_only_when_known(client, monkeypatch, complete_breakdown):
    source = seed_selected(per_facet=49)

    def respond(request):
        row = json.loads(json.loads(request.content)["input"])["item"]
        body = response_body(assessment(row))
        details = body["usage"]["input_tokens_details"]
        details.update(cache_write_tokens=70)
        if complete_breakdown:
            details["cache_write_tokens_details"] = {"ttl_30m_tokens": 30, "ttl_12h_tokens": 40}
        return httpx.Response(200, json=body)

    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: AsyncOpenAI(
        **kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))))
    access = start_adaptive(client, source, {
        "max_cost_usd": 10, "input_price_per_million": 1,
        "cached_input_price_per_million": .5, "output_price_per_million": 2,
    })
    result = finished(client, access).json()
    assert result["status"] == "completed", result["message"]
    adaptive = result["adaptive"]
    attempt = adaptive["attempts"][0]
    assert attempt["usage"]["input_tokens_details"]["cache_write_tokens"] == 70
    assert adaptive["cost"]["policy"]["version"] == 2
    if complete_breakdown:
        # 20 ordinary, 10 reads, 30 short writes, 40 long writes, 90 output.
        assert adaptive["cost"]["spent_usd"] == pytest.approx((20 + 10 * .5 + 30 * 1.25 + 40 * 2.5 + 90 * 2) / 1_000_000)
        assert adaptive["cost"]["reserved_usd"] == 0
        assert adaptive["cost"]["unknown_attempts"] == 0
    else:
        assert attempt["cost_usd"] is None and adaptive["cost"]["spent_usd"] == 0
        assert adaptive["cost"]["reserved_usd"] == attempt["reserved_usd"] > 0
        assert adaptive["cost"]["unknown_attempts"] == 1
    assert export(client, access).json()["adaptive"] == adaptive


def test_older_cost_policy_cannot_resume_with_silently_repriced_ledger(client, monkeypatch):
    source = seed_selected()
    mock_screener(monkeypatch, lambda value, row: {**value, "coverage": ["invalid"]})
    access = start_adaptive(client, source)
    assert finished(client, access).json()["status"] == "failed"
    job = item_review.jobs[access["run_id"]]
    job.adaptive["cost"].pop("policy")
    original = deepcopy(job.adaptive)
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("Obsolete cost policy"))
    response = client.post(f"/api/item-review/runs/{access['run_id']}/adapt", json={}, headers={
        "X-Review-Token": access["run_secret"], "X-OpenAI-Key": KEY})
    assert response.status_code == 409
    assert job.adaptive == original


def test_frozen_result_cannot_resume_or_bypass_history_with_screen_or_select(client, monkeypatch):
    source = seed_selected(per_facet=2)
    access = start_adaptive(client, source)
    result = finished(client, access).json()
    assert result["adaptive"]["frozen"] is True
    for action in ("adapt", "screen", "select"):
        response = client.post(f"/api/item-review/runs/{access['run_id']}/{action}", json={}, headers={
            "X-Review-Token": access["run_secret"], "X-OpenAI-Key": KEY})
        assert response.status_code == 409


def test_invalid_response_keeps_pending_batch_and_resume_retries_only_unfinished_items(client, monkeypatch):
    source = seed_selected()
    original_selection = deepcopy(item_review.jobs[source["run_id"]].selection)

    def invalid_one(value, row):
        if row["id"] == "0-48":
            value["ratings"]["input_content"]["score"] = 6
        return value

    first_calls = mock_screener(monkeypatch, invalid_one)
    first = start_adaptive(client, source, {"seed": 42})
    paused = finished(client, first).json()
    assert paused["status"] == "failed", paused["message"]
    adaptive = paused["adaptive"]
    assert adaptive["initial_selection"] == original_selection
    assert adaptive["initial_selection_run_id"] == source["run_id"]
    assert adaptive["frozen"] is False and adaptive["stop_reason"] is None
    assert len(adaptive["batches"]) == 2
    assert adaptive["batches"][1]["status"] != "committed"
    assert adaptive["batches"][1]["outcomes"] == []
    assert paused["selection"] == original_selection
    assert all(stats["successes"] == 30 and stats["failures"] == 18
               for stats in adaptive["queue_statistics"])
    successful = {item["item_id"] for item in paused["screening"]["items"] if item["status"] == "complete"}
    invalid = [item for item in paused["screening"]["items"] if item["status"] == "error"]
    assert len(invalid) == 1 and len(first_calls) >= 1
    changed = client.post(f"/api/item-review/runs/{first['run_id']}/adapt", json={"seed": 43}, headers={
        "X-Review-Token": first["run_secret"], "X-OpenAI-Key": KEY})
    assert changed.status_code in {409, 422}
    calls = mock_screener(monkeypatch)
    resumed = start_adaptive(client, first)
    result = finished(client, resumed).json()
    assert result["status"] == "completed", result["message"]
    assert result["adaptive"]["frozen"] is True
    assert result["adaptive"]["batches"][1]["item_ids"] == adaptive["batches"][1]["item_ids"]
    assert result["adaptive"]["batches"][0] == adaptive["batches"][0]
    assert result["adaptive"]["settings"] == adaptive["settings"]
    assert result["adaptive"]["initial_selection"] == original_selection
    assert result["adaptive"]["initial_selection_run_id"] == source["run_id"]
    assert len(calls) == 56 - len(successful)
    assert len(result["adaptive"]["attempts"]) == len(first_calls) + len(calls)
    assert len(result["screening"]["items"]) == 56
    assert all(item["status"] == "complete" for item in result["screening"]["items"])
    assert finished(client, first).json() == paused


def test_legacy_history_without_initial_selection_snapshot_can_resume(client, monkeypatch):
    source = seed_selected(per_facet=49)
    mock_screener(monkeypatch, lambda value, row: {**value, "coverage": ["invalid"]})
    first = start_adaptive(client, source)
    assert finished(client, first).json()["status"] == "failed"
    state = item_review.jobs[first["run_id"]].adaptive
    state.pop("initial_selection")
    state.pop("initial_selection_run_id")
    original_ids = list(state["batches"][0]["selected_item_ids"])

    mock_screener(monkeypatch)
    result = finished(client, start_adaptive(client, first)).json()
    assert result["status"] == "completed", result["message"]
    assert result["adaptive"]["batches"][0]["selected_item_ids"] == original_ids
    assert "initial_selection" not in result["adaptive"]
    assert "initial_selection_run_id" not in result["adaptive"]


def test_incomplete_selection_retains_pending_batch_and_resume_uses_saved_assessments(client, monkeypatch):
    source = seed_selected()
    initial = deepcopy(item_review.jobs[source["run_id"]].selection)
    calls = mock_screener(monkeypatch)

    def timeout(*args, **kwargs):
        raise SelectionIncomplete("Private solver details")

    monkeypatch.setattr(item_review, "select_collection", timeout)
    first = start_adaptive(client, source)
    failed = finished(client, first).json()
    assert failed["status"] == "failed" and len(calls) == 8
    assert failed["selection"] == initial and failed["selection_run_id"] == source["run_id"]
    assert failed["adaptive"]["batches"][1]["outcomes"] == []
    assert all(stats["successes"] + stats["failures"] == 48
               for stats in failed["adaptive"]["queue_statistics"])
    assert "Private solver details" not in json.dumps(failed)
    monkeypatch.setattr(item_review, "select_collection", select_collection)
    resumed_calls = mock_screener(monkeypatch)
    resumed = start_adaptive(client, first)
    result = finished(client, resumed).json()
    assert result["status"] == "completed", result["message"]
    assert resumed_calls == []
    assert result["adaptive"]["batches"][1]["status"] == "committed"
    assert len(result["adaptive"]["batches"][1]["outcomes"]) == 8
    assert result["selection_run_id"] == resumed["run_id"]
    assert result["selection"]["previous_selected_item_ids"] == initial["selected_item_ids"]
    assert finished(client, first).json() == failed


def test_cancel_drains_pending_solver_and_keeps_last_accepted_collection(client, monkeypatch):
    source = seed_selected()
    original = deepcopy(item_review.jobs[source["run_id"]].selection)
    mock_screener(monkeypatch)
    started, stopped = Event(), Event()

    def wait_for_cancel(*args, cancelled, **kwargs):
        started.set()
        while not cancelled():
            time.sleep(.001)
        stopped.set()
        raise InterruptedError("cancelled")

    monkeypatch.setattr(item_review, "select_collection", wait_for_cancel)
    access = start_adaptive(client, source)
    assert started.wait(3)
    response = client.post(f"/api/item-review/runs/{access['run_id']}/cancel",
                           headers={"X-Review-Token": access["run_secret"]})
    assert response.status_code == 200
    result = response.json()
    assert stopped.is_set() and result["status"] == "cancelled"
    assert result["selection"] == original
    assert result["adaptive"]["frozen"] is False
    assert result["adaptive"]["batches"][1]["outcomes"] == []
    assert result["adaptive"]["screened_count"] == 56


def test_provider_error_is_one_unknown_attempt_and_not_a_selection_failure(client, monkeypatch):
    source = seed_selected()
    requests = []
    configurations = []

    def respond(request):
        requests.append(request)
        return httpx.Response(503, json={"error": {"message": "Private provider failure"}})

    def client_factory(**kwargs):
        configurations.append(kwargs)
        return AsyncOpenAI(**kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond)))

    monkeypatch.setattr(item_review, "AsyncOpenAI", client_factory)
    first = start_adaptive(client, source, {
        "max_cost_usd": 10, "input_price_per_million": 1,
        "cached_input_price_per_million": .5, "output_price_per_million": 2,
    })
    failed = finished(client, first).json()
    assert failed["status"] == "failed" and len(requests) == 1
    assert configurations[0]["max_retries"] == 0
    adaptive = failed["adaptive"]
    assert adaptive["cost"]["unknown_attempts"] == 1
    assert adaptive["cost"]["reserved_usd"] > 0 and adaptive["cost"]["spent_usd"] == 0
    assert len(adaptive["attempts"]) == 1 and adaptive["batches"][1]["outcomes"] == []
    assert all(stats["successes"] + stats["failures"] == 48 for stats in adaptive["queue_statistics"])
    assert "Private provider failure" not in json.dumps(failed)
    calls = mock_screener(monkeypatch)
    result = finished(client, start_adaptive(client, first)).json()
    assert result["status"] == "completed", result["message"]
    assert len(calls) == 8
    assert len(result["adaptive"]["attempts"]) == 9
    assert result["adaptive"]["cost"]["unknown_attempts"] == 1
    assert result["adaptive"]["cost"]["reserved_usd"] == adaptive["cost"]["reserved_usd"]


def test_cancel_inflight_request_retains_attempt_without_crediting_incomplete_batch(client, monkeypatch):
    source = seed_selected()
    original = deepcopy(item_review.jobs[source["run_id"]].selection)
    entered, drained = Event(), Event()
    calls = []

    async def respond(request):
        body = json.loads(request.content)
        calls.append(body)
        if len(calls) == 1:
            row = json.loads(body["input"])["item"]
            return httpx.Response(200, json=response_body(assessment(row)))
        entered.set()
        try:
            while True:
                await asyncio.sleep(.001)
        finally:
            drained.set()

    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: AsyncOpenAI(
        **kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))))
    access = start_adaptive(client, source)
    assert entered.wait(3)
    response = client.post(f"/api/item-review/runs/{access['run_id']}/cancel",
                           headers={"X-Review-Token": access["run_secret"]})
    result = response.json()
    assert response.status_code == 200 and result["status"] == "cancelled" and drained.is_set()
    assert result["selection"] == original
    assert result["adaptive"]["batches"][1]["outcomes"] == []
    assert result["adaptive"]["screened_count"] == 49
    assert len(result["adaptive"]["attempts"]) == 2
    assert result["adaptive"]["cost"]["unknown_attempts"] == 1


def test_cost_limited_resume_freezes_valid_subset_and_keeps_unfinished_ids_explicit(client, monkeypatch):
    from website.server import adaptive_review

    source = seed_selected()
    initial_selection = deepcopy(item_review.jobs[source["run_id"]].selection)
    requests = []
    committed_checkpoints = []
    real_freeze = adaptive_review.freeze

    def freeze_after_checkpoint(job, state, reason):
        # Capture the narrow restart window after committing a partial batch,
        # before freeze() has updated the final status and message.
        committed_checkpoints.append(item_review.checkpoints().run_path(job.run_id).read_bytes())
        real_freeze(job, state, reason)

    monkeypatch.setattr(adaptive_review, "freeze", freeze_after_checkpoint)
    # Two requests fit initially. One settled charge plus the second unknown
    # reservation leaves too little budget for an explicit retry.
    monkeypatch.setattr(adaptive_review, "request_reservation", lambda *args: .01)

    def respond(request):
        requests.append(request)
        if len(requests) == 1:
            row = json.loads(json.loads(request.content)["input"])["item"]
            value = assessment(row)
            for dimension in ("input_ontology", "input_content", "input_form", "output_ontology"):
                value["ratings"][dimension]["score"] = 5
            return httpx.Response(200, json=response_body(value))
        return httpx.Response(503, json={"error": {"message": "Unavailable"}})

    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: AsyncOpenAI(
        **kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))))
    first = start_adaptive(client, source, {
        "max_cost_usd": .02, "input_price_per_million": 1,
        "cached_input_price_per_million": .5, "output_price_per_million": 2,
    })
    failed = finished(client, first).json()
    assert failed["status"] == "failed" and len(requests) == 2
    assert failed["adaptive"]["batches"][1]["outcomes"] == []
    assert failed["adaptive"]["batches"][1]["budget_limited"] is True
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("Retry cannot be funded"))
    resumed = start_adaptive(client, first)
    result = finished(client, resumed).json()
    assert result["status"] == "completed", result["message"]
    adaptive = result["adaptive"]
    assert adaptive["frozen"] is True and adaptive["stop_reason"] == "cost_limit"
    assert adaptive["screened_count"] == 49 and adaptive["acquired_count"] == 50
    batch = adaptive["batches"][1]
    assert batch["status"] == "committed" and len(batch["outcomes"]) == 1
    assert batch["outcomes"][0]["retained"] is True
    assert batch["unresolved_item_ids"] == batch["item_ids"][1:]
    assert result["selection"]["total_quality"] == 121
    assert adaptive["initial_selection"] == initial_selection
    assert adaptive["initial_selection"]["selected_item_ids"] != result["selection"]["selected_item_ids"]
    assert adaptive["initial_selection_run_id"] == source["run_id"]
    assert result["selection_run_id"] == resumed["run_id"]
    assert adaptive["cost"] == failed["adaptive"]["cost"]
    assert all(stats["successes"] == 31 and stats["failures"] == 18
               for stats in adaptive["queue_statistics"])
    assert finished(client, first).json() == failed
    assert len(committed_checkpoints) == 1
    item_review.jobs.clear()
    item_review.checkpoints().run_path(resumed["run_id"]).write_bytes(committed_checkpoints[0])
    restored = finished(client, resumed).json()
    assert restored["status"] == "completed"
    assert restored["adaptive"] == adaptive
    adaptive_review.validate_history(item_review.jobs[resumed["run_id"]])


@pytest.mark.parametrize("change", ["row", "assessment", "allocation", "duplicate", "selected_id"])
def test_corrupt_initial_source_is_rejected_before_provider(client, monkeypatch, change):
    source = seed_selected(per_facet=2)
    job = item_review.jobs[source["run_id"]]
    if change == "row":
        job.screening["items"][0]["evidence"]["item"]["content"] = "Changed original row"
    elif change == "assessment":
        job.screening["items"][0]["assessment"]["task"]["matched_facet_ids"] = ["invented-task"]
    elif change == "allocation":
        job.screening["allocation"]["budget"] = 51
    elif change == "duplicate":
        job.screening["items"].append(deepcopy(job.screening["items"][0]))
    else:
        job.selection["selected_item_ids"][0] = "unknown-item"
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("Invalid source"))
    response = client.post(f"/api/item-review/runs/{source['run_id']}/adapt", json={}, headers={
        "X-Review-Token": source["run_secret"], "X-OpenAI-Key": KEY})
    assert response.status_code == 409


@pytest.mark.parametrize("change", [
    "outcome", "statistics", "priority", "remaining", "batch_ids", "cost", "selection", "initial_selection",
])
def test_corrupt_adaptive_history_is_rejected_before_resume(client, monkeypatch, change):
    source = seed_selected()
    mock_screener(monkeypatch, lambda value, row: {**value, "coverage": ["invalid"]})
    access = start_adaptive(client, source)
    assert finished(client, access).json()["status"] == "failed"
    job = item_review.jobs[access["run_id"]]
    if change == "outcome":
        outcome = job.adaptive["batches"][0]["outcomes"][0]
        outcome["retained"] = not outcome["retained"]
    elif change == "statistics":
        job.adaptive["queue_statistics"][0]["successes"] += 1
    elif change in {"priority", "remaining"}:
        job.adaptive["queue_statistics"][0][change] += 1
    elif change == "batch_ids":
        job.adaptive["batches"][1]["item_ids"].reverse()
    elif change == "cost":
        job.adaptive["cost"]["spent_usd"] = 100
    elif change == "initial_selection":
        job.adaptive["initial_selection"]["selected_item_ids"] = []
    else:
        job.selection["selected_item_ids"] = []
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("Invalid history"))
    response = client.post(f"/api/item-review/runs/{access['run_id']}/adapt", json={}, headers={
        "X-Review-Token": access["run_secret"], "X-OpenAI-Key": KEY})
    assert response.status_code == 409


@pytest.mark.parametrize("change", ["settled_cost", "reservation", "batch_number"])
def test_paired_attempt_and_total_edits_cannot_hide_corrupt_cost_history(client, monkeypatch, change):
    source = seed_selected()

    def respond(request):
        if change == "settled_cost":
            row = json.loads(json.loads(request.content)["input"])["item"]
            value = {**assessment(row), "coverage": ["invalid"]}
            return httpx.Response(200, json=response_body(value))
        return httpx.Response(503, json={"error": {"message": "Unavailable"}})

    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: AsyncOpenAI(
        **kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))))
    access = start_adaptive(client, source, {
        "max_cost_usd": 10, "input_price_per_million": 1,
        "cached_input_price_per_million": .5, "output_price_per_million": 2,
    })
    assert finished(client, access).json()["status"] == "failed"
    job = item_review.jobs[access["run_id"]]
    assert len(job.adaptive["attempts"]) == 1
    attempt = job.adaptive["attempts"][0]
    if change == "settled_cost":
        assert attempt["cost_usd"] > 0 and attempt["usage"] is not None
        attempt["cost_usd"] = 0
        job.adaptive["cost"]["spent_usd"] = 0
    elif change == "reservation":
        assert attempt["reserved_usd"] > 0 and attempt["usage"] is None
        attempt["reserved_usd"] = 0
        job.adaptive["cost"]["reserved_usd"] = 0
    else:
        attempt["batch_number"] = 0
    monkeypatch.setattr(item_review, "AsyncOpenAI", lambda **kwargs: pytest.fail("Corrupt attempt history"))
    response = client.post(f"/api/item-review/runs/{access['run_id']}/adapt", json={}, headers={
        "X-Review-Token": access["run_secret"], "X-OpenAI-Key": KEY})
    assert response.status_code == 409


def test_export_snapshots_adaptive_history_and_selection_together(client, monkeypatch):
    source = seed_selected(per_facet=2)
    access = start_adaptive(client, source)
    original = finished(client, access).json()
    job = item_review.jobs[access["run_id"]]

    async def download():
        response = await item_review.export_review(job.run_id, job.secret)
        assert job.downloads == 1
        job.adaptive = {**job.adaptive, "batches": []}
        job.selection = {**job.selection, "selected_item_ids": []}
        job.screening = {**job.screening, "items": []}
        return "".join([chunk async for chunk in response.body_iterator])

    result = json.loads(asyncio.run(download()))
    assert result["adaptive"] == original["adaptive"]
    assert result["selection"] == original["selection"]
    assert result["screening"] == original["screening"]
    assert job.downloads == 0
