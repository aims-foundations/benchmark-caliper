"""Six-score website workflow using real preparation/storage and an offline judge."""

import asyncio
import json
from zipfile import ZipFile
import io
from threading import Event

import pytest

from anthropic_api_package_release.item_analysis import model_client, scoring
from anthropic_api_package_release.item_analysis.storage import read_json, write_json
from website.server import item_analysis as analysis
from website.server.tests.test_item_analysis import (
    KEY, client, current_assessment, headers, request_payload, settled, start, url,
)


@pytest.fixture
def model(monkeypatch):
    calls = []

    async def fake_call(**arguments):
        assert arguments["api_key"] == KEY
        payload = request_payload(arguments["user"])
        calls.append(payload)
        assert "item" in payload, "Context preparation must not call a model"
        assert set(payload["output_schema"]["properties"]["dimensions"]["properties"]) == set(scoring.DIMENSIONS)
        unknown = payload["item"].get("reference_answer") is None
        result = {"dimensions": {
            dimension: {
                "score": None if dimension == "output_content" and unknown else 4,
                "justification": "Test response based on supplied item and deployment evidence.",
                "evidence": ["item.content: " + str(payload["item"]["content"])],
                "information_gaps": ["Reference answer is not supplied."] if dimension == "output_content" and unknown else [],
            } for dimension in scoring.DIMENSIONS
        }}
        return model_client.CallResult(json.dumps(result), arguments["model"], 100, 30, 1)

    monkeypatch.setattr(model_client, "call_text_async", fake_call)
    return calls


def score_all(client, access):
    response = client.post(url(access) + "/classify", json={"scope": "all"}, headers=headers(access, key=True))
    assert response.status_code == 202, response.text
    return settled(client, access)


def test_prepare_without_key_then_one_request_per_item_and_six_scores(client, model):
    response = client.post("/api/item-analysis/runs", json={"example_id": "illustrative"})
    assert response.status_code == 202
    access = response.json()
    ready = settled(client, access)
    assert ready["status"] == "ready", ready
    assert ready["analysis_type"] == "six_scores"
    assert ready["spec"]["analysis_type"] == "six_scores"
    assert len(ready["spec"]["classifiers"]) == 6
    assert ready["remaining_requests"]["all"] == ready["total"]
    assert ready["remaining_judgments"]["all"] == ready["total"] * 6
    assert all(dimension["mean_score"] is None and dimension["known"] == 0
               for dimension in ready["summary"]["dimensions"])
    assert not model
    assert client.post(url(access) + "/classify", json={"scope": "all"}, headers=headers(access)).status_code == 401
    complete = score_all(client, access)
    assert complete["status"] == "complete", complete
    assert len(model) == complete["total"]
    assert complete["completed_judgments"] == complete["total"] * 6
    assert complete["remaining_requests"] == {"all": 0, "pilot": 0}
    assert all(set(item["dimensions"]) == set(scoring.DIMENSIONS) for item in complete["items"])
    assert complete["summary"]["analysis_type"] == "six_scores"


def test_direct_upload_unknown_is_completed_and_exports_all_six_dimensions(client, model):
    context = {"benchmark": "Teaching items", "deployment": "English math tutor in India.",
               "task_requirements": "Arithmetic and fractions.", "answer_requirements": "Explain each step."}
    response = client.post("/api/item-analysis/runs/from-context", data={
        "context_json": json.dumps(context), "benchmark_confirmed": "true",
    }, files={"items_file": ("items.json", json.dumps([
        {"item_id": "q1", "content": "What is 2+2?", "reference_answer": "4", "grading_criterion": "Exact answer"},
        {"item_id": "q2", "content": "Explain fractions.", "asset_manifest": [{"path": "unavailable.png"}]},
    ]))})
    assert response.status_code == 202, response.text
    access = response.json()
    assert settled(client, access)["status"] == "ready"
    assert not model
    completed = score_all(client, access)
    assert completed["status"] == "complete", completed
    missing = next(item for item in completed["items"] if item["item_id"] == "q2")
    assert missing["dimensions"]["output_content"]["score"] is None
    assert missing["status"] == "complete" and completed["errors"] == 0
    assert missing["asset_manifest"] == [{"path": "unavailable.png"}]
    assert next(item for item in completed["items"] if item["item_id"] == "q1")["grading_criterion"] == "Exact answer"
    assert len(model) == 2
    averages = {dimension["id"]: dimension for dimension in completed["summary"]["dimensions"]}
    assert averages["input_content"]["mean_score"] == 4
    assert averages["input_content"]["known"] == 2
    assert averages["output_content"]["mean_score"] == 4
    assert averages["output_content"]["known"] == 1
    assert averages["output_content"]["unknown"] == 1
    assert all(not any(key.startswith("scoring.json") for key in request["source_registry"]) for request in model)
    csv_response = client.get(url(access) + "/download/items", headers=headers(access))
    assert csv_response.status_code == 200
    assert all(dimension + ".score" in csv_response.text for dimension in scoring.DIMENSIONS)
    package = client.get(url(access) + "/package", headers=headers(access))
    assert package.status_code == 200, package.text
    with ZipFile(io.BytesIO(package.content)) as archive:
        assert "report.html" in archive.namelist()
        assert b"output_form" in archive.read("items.csv")
        exported = json.loads(archive.read("summary.json"))
        assert exported["dimensions"] == completed["summary"]["dimensions"]
        assert b"Average scores across evaluated items" in archive.read("report.html")
        assert KEY.encode() not in b"".join(archive.read(name) for name in archive.namelist())


def test_existing_assessment_sources_reused_without_numerical_score_anchoring(client, current_assessment, model):
    response = client.post("/api/item-analysis/runs/from-assessment", data={
        **current_assessment,
    }, files={"items_file": ("items.json", '[{"content":"Question","reference_answer":"Answer"}]')})
    assert response.status_code == 202, response.text
    access = response.json()
    ready = settled(client, access)
    assert ready["status"] == "ready", ready
    assert not model
    complete = score_all(client, access)
    assert complete["status"] == "complete", complete
    assert len(model) == 1
    request = model[0]
    assert not any(key.startswith("scoring.json") for key in request["source_registry"])
    assert "scoring" not in request and "original_assessment" not in request
    directory = analysis.jobs[access["run_id"]].directory
    assert read_json(directory / "evidence.json")["scoring"]  # Still preserved for the separate original report.


def test_checkpoint_restore_and_continue_reuses_complete_six_score_records(client, model, monkeypatch):
    monkeypatch.setattr(analysis, "CHECKPOINT_SIZE", 1)
    access = start(client)
    ready = settled(client, access)
    response = client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access, key=True))
    assert response.status_code == 202
    checkpoint = settled(client, access)
    assert checkpoint["status"] == "checkpoint" and len(model) == 1
    saved = checkpoint["items"][0]["dimensions"]
    analysis.jobs.clear()
    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["analysis_type"] == "six_scores"
    assert restored["items"][0]["dimensions"] == saved
    final = score_all(client, access)
    assert final["status"] == "complete", final
    assert len(model) == ready["total"]
    assert final["items"][0]["dimensions"] == saved


def test_provider_failure_retains_prior_items_and_retry_only_requests_missing_items(client, model, monkeypatch):
    original = model_client.call_text_async
    attempts = []

    async def fail_second(**arguments):
        attempts.append(arguments)
        if len(attempts) == 2:
            raise model_client.ModelRequestError(code="rate_limit")
        return await original(**arguments)

    monkeypatch.setattr(model_client, "call_text_async", fail_second)
    access = start(client)
    settled(client, access)
    failed = score_all(client, access)
    assert failed["status"] == "failed", failed
    assert failed["complete"] == 1
    assert failed["errors"] == 1
    successful_id = model[0]["item"]["item_id"]
    final = score_all(client, access)
    assert final["status"] == "complete", final
    assert sum(request["item"]["item_id"] == successful_id for request in model) == 1
    assert len(model) == final["total"]


def test_averages_update_during_scoring_and_use_all_results_across_pages(client, model, monkeypatch):
    original = model_client.call_text_async
    started, release = Event(), Event()
    attempts = 0

    async def pause_second(**arguments):
        nonlocal attempts
        attempts += 1
        if attempts == 2:
            started.set()
            assert await asyncio.to_thread(release.wait, 5)
        return await original(**arguments)

    monkeypatch.setattr(model_client, "call_text_async", pause_second)
    monkeypatch.setattr(analysis, "PAGE_SIZE", 1)
    access = start(client)
    settled(client, access)
    response = client.post(url(access) + "/classify", json={"scope": "all"}, headers=headers(access, key=True))
    assert response.status_code == 202
    try:
        assert started.wait(2)
        live = client.get(url(access) + "?page=2", headers=headers(access)).json()
        assert live["status"] == "running" and live["complete"] == 1
        assert live["items"][0]["status"] == "pending"
        dimension = live["summary"]["dimensions"][0]
        assert dimension["mean_score"] == 4 and dimension["known"] == 1
        assert dimension["pending"] == live["total"] - 1
        assert live["summary"]["experiment"]["selected_completed_items"] == 1
        assert live["summary"]["experiment"]["selected_items"] == live["total"]
    finally:
        release.set()
    complete = settled(client, access)
    assert complete["status"] == "complete"
    second_page = client.get(url(access) + "?page=2", headers=headers(access)).json()
    assert complete["items"] != second_page["items"]
    assert complete["summary"]["dimensions"] == second_page["summary"]["dimensions"]
    assert len(model) == complete["total"]


def test_saved_six_score_runs_gain_means_and_exports_without_rescoring(client, model):
    access = start(client)
    settled(client, access)
    complete = score_all(client, access)
    directory = analysis.jobs[access["run_id"]].directory
    preserved = {name: (directory / name).read_bytes() for name in (
        "results.jsonl", "classifier_spec.json", "run.json", "evidence.json")}
    old_summary = read_json(directory / "summary.json")
    for key in ("dimensions", "classifiers"):
        for dimension in old_summary[key]:
            dimension.pop("mean_score")
    write_json(directory / "summary.json", old_summary)
    (directory / "report.html").write_text("Old report without means", encoding="utf-8")
    calls = len(model)
    analysis.jobs.clear()

    restored = client.get(url(access), headers=headers(access)).json()
    assert restored["status"] == "complete"
    assert restored["summary"]["dimensions"] == complete["summary"]["dimensions"]
    assert len(model) == calls
    assert all((directory / name).read_bytes() == content for name, content in preserved.items())
    exported = client.get(url(access) + "/download/summary", headers=headers(access)).json()
    assert exported["dimensions"] == restored["summary"]["dimensions"]
    html = client.get(url(access) + "/download/report", headers=headers(access)).text
    assert "Average scores across evaluated items" in html
