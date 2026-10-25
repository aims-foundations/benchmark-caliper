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
from website.server.tests.test_benchmark_screening import assessment, export, mock_screener
from website.server.tests.test_benchmark_selection import seed_screening
from website.server.tests.test_item_review import BODY, KEY, HF_KEY, client
from website.server.tests.test_onet_grounding import response_body


def seed_selected(*, facets=1, per_facet=58):
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


def test_caps_total_at_160_uses_eight_unseen_per_batch_and_keeps_initial_outcomes(client, monkeypatch):
    source = seed_selected(per_facet=180)
    original = finished(client, source).json()
    calls = mock_screener(monkeypatch)
    forbid_retrieval(monkeypatch)
    access = start_adaptive(client, source, {"seed": 7})
    result = finished(client, access).json()
    assert result["mode"] == "adaptive" and result["status"] == "completed", result["message"]
    adaptive = result["adaptive"]
    assert adaptive["frozen"] is True and adaptive["stop_reason"] == "candidate_limit"
    assert adaptive["screened_count"] == adaptive["acquired_count"] == 160
    assert len(calls) == 110
    rows = [json.loads(call["input"])["item"]["id"] for call in calls]
    assert len(set(rows)) == 110 and all(int(row.split("-")[1]) >= 50 for row in rows)
    batches = adaptive["batches"]
    assert batches[0]["number"] == 0 and batches[0]["kind"] == "initial"
    assert len(batches[0]["item_ids"]) == 50
    assert batches[0]["selected_item_ids"] == original["selection"]["selected_item_ids"]
    assert [len(batch["item_ids"]) for batch in batches[1:]] == [8] * 13 + [6]
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
    assert result["usage"]["input_tokens"] == 11000
    assert finished(client, source).json() == original
    exported = export(client, access)
    assert exported.json()["adaptive"] == adaptive
    assert exported.json()["selection"] == result["selection"]
    assert exported.json()["retrieval"] == item_review.jobs[source["run_id"]].benchmark_retrieval
    assert "adaptive" in exported.headers["content-disposition"]
    for secret in (KEY, HF_KEY, source["run_secret"], access["run_secret"]):
        assert secret not in exported.text


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
    assert [len(batch["item_ids"]) for batch in adaptive["batches"]] == [50, 8, 3]
    assert len(calls) == 11
    assert len({item["item_id"] for item in result["screening"]["items"]}) == 61
    assert result["selection"]["selected_count"] == 30


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
    assert adaptive["screened_count"] == adaptive["acquired_count"] == 50
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
        if row["id"] == "0-50":
            value["ratings"]["input_content"]["score"] = 6
        return value

    first_calls = mock_screener(monkeypatch, invalid_one)
    first = start_adaptive(client, source, {"seed": 42})
    paused = finished(client, first).json()
    assert paused["status"] == "failed", paused["message"]
    adaptive = paused["adaptive"]
    assert adaptive["frozen"] is False and adaptive["stop_reason"] is None
    assert len(adaptive["batches"]) == 2
    assert adaptive["batches"][1]["status"] != "committed"
    assert adaptive["batches"][1]["outcomes"] == []
    assert paused["selection"] == original_selection
    assert all(stats["successes"] == 30 and stats["failures"] == 20
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
    assert len(calls) == 58 - len(successful)
    assert len(result["adaptive"]["attempts"]) == len(first_calls) + len(calls)
    assert len(result["screening"]["items"]) == 58
    assert all(item["status"] == "complete" for item in result["screening"]["items"])
    assert finished(client, first).json() == paused


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
    assert all(stats["successes"] + stats["failures"] == 50
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
    assert result["adaptive"]["screened_count"] == 58


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
    assert all(stats["successes"] + stats["failures"] == 50 for stats in adaptive["queue_statistics"])
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
    assert result["adaptive"]["screened_count"] == 51
    assert len(result["adaptive"]["attempts"]) == 2
    assert result["adaptive"]["cost"]["unknown_attempts"] == 1


def test_cost_limited_resume_freezes_valid_subset_and_keeps_unfinished_ids_explicit(client, monkeypatch):
    from website.server import adaptive_review

    source = seed_selected()
    requests = []
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
    assert adaptive["screened_count"] == 51 and adaptive["acquired_count"] == 52
    batch = adaptive["batches"][1]
    assert batch["status"] == "committed" and len(batch["outcomes"]) == 1
    assert batch["outcomes"][0]["retained"] is True
    assert batch["unresolved_item_ids"] == batch["item_ids"][1:]
    assert result["selection"]["total_quality"] == 121
    assert result["selection_run_id"] == resumed["run_id"]
    assert adaptive["cost"] == failed["adaptive"]["cost"]
    assert all(stats["successes"] == 31 and stats["failures"] == 20
               for stats in adaptive["queue_statistics"])
    assert finished(client, first).json() == failed


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


@pytest.mark.parametrize("change", ["outcome", "statistics", "priority", "remaining", "batch_ids", "cost", "selection"])
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
