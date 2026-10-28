"""The direct entry point freezes declared requirements without benchmark scores."""

from copy import deepcopy
import json
import time

import pytest

from anthropic_api_package_release.item_analysis.storage import check_prepared, read_json
from website.server import item_analysis as analysis, item_analysis_assessment
from website.server.tests.test_item_analysis import (
    CATALOG_REVISION, KEY, client, model, classify, databank_catalog, headers,
    prepared_snapshot, settled, url,
)


CONTEXT = {
    "benchmark": "New classroom benchmark",
    "deployment": "Spanish-speaking teachers reviewing classroom tutoring.",
    "task_requirements": "Grade 5 arithmetic and explanations suitable for the curriculum.",
    "answer_requirements": "A correct answer with a Spanish explanation; accept regional variants.",
    "validity_concerns": "Check whether references permit multiple valid explanations.",
}
ENDPOINT = "/api/item-analysis/runs/from-context"


def start_direct(client, context=None, *, rows=None, source=None):
    fields = {"context_json": json.dumps(context or CONTEXT), "benchmark_confirmed": "true"}
    if source:
        fields.update(source_id=source["id"], source_revision=source["source_revision"])
    response = client.post(ENDPOINT, data=fields,
                           files={"items_file": ("items.json", json.dumps(rows or [{"content": "Explain 2+2.", "reference_answer": "4"}]))} if not source else None,
                           headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 202, response.text
    return response.json()


def test_setup_is_stateless_and_uses_declared_identity_without_scoring(client, monkeypatch, model):
    candidate = databank_catalog(monkeypatch)
    calls = []
    search = analysis.item_analysis_databank.search_candidates

    def capture(assessment, query=None):
        calls.append((deepcopy(assessment), query))
        return search(assessment, query)

    monkeypatch.setattr(analysis.item_analysis_databank, "search_candidates", capture)
    monkeypatch.setattr(item_analysis_assessment, "resolve", lambda *args: pytest.fail("Direct setup must not resolve a scored assessment"))
    response = client.post("/api/item-analysis/direct/setup", json={**CONTEXT, "q": "alternate benchmark name"})
    assert response.status_code == 200 and response.headers["cache-control"] == "no-store"
    setup = response.json()
    assessment = setup["assessment"]
    assert assessment["kind"] == "direct" and assessment["id"].startswith("direct-")
    assert assessment["assessment_status"] == "not_run" and assessment["analysis_basis"] == "deployment_requirements"
    assert "scoring" not in assessment and "elicitation_summary" not in assessment
    assert assessment["direct_context"] == CONTEXT
    assert assessment["benchmark_identity"]["name"] == CONTEXT["benchmark"]
    assert assessment["benchmark_identity"]["source_urls"] == []
    assert "declared" in assessment["benchmark_identity"]["evidence"]["name"]
    assert setup["sources"][0]["id"] == candidate["id"]
    assert setup["catalog"]["requires_confirmation"]
    assert setup["upload"]["required_fields"] == ["content"]
    assert calls == [(assessment, "alternate benchmark name")]
    assert not analysis.jobs and not model
    assert not analysis.db.DEFAULT_DB_PATH.exists()


def test_context_identity_is_stable_after_trimming_and_changes_with_requirements(client, model):
    base = client.post("/api/item-analysis/direct/setup", json=CONTEXT).json()["assessment"]
    trimmed = client.post("/api/item-analysis/direct/setup", json={key: f"  {value}\n" for key, value in reversed(list(CONTEXT.items()))}).json()["assessment"]
    changed = client.post("/api/item-analysis/direct/setup", json={**CONTEXT, "answer_requirements": "A numerical answer only."}).json()["assessment"]
    assert base == trimmed and changed["id"] != base["id"]
    assert base["deployment"] == (f"Deployment context:\n{CONTEXT['deployment']}\n\nTask requirements:\n{CONTEXT['task_requirements']}\n\n"
                                   f"Answer requirements:\n{CONTEXT['answer_requirements']}")
    assert not model and not analysis.jobs


def test_optional_concerns_default_to_empty_and_invalid_search_or_unicode_is_rejected(client, model):
    context = {key: value for key, value in CONTEXT.items() if key != "validity_concerns"}
    response = client.post("/api/item-analysis/direct/setup", json=context)
    assert response.status_code == 200
    assert response.json()["assessment"]["direct_context"]["validity_concerns"] == ""
    assert "Validity concerns:" not in response.json()["assessment"]["deployment"]
    assert client.post("/api/item-analysis/direct/setup", json={**context, "q": "q" * 201}).status_code == 422
    malformed = client.post("/api/item-analysis/direct/setup", content=json.dumps({**context, "deployment": "\ud800"}),
                            headers={"Content-Type": "application/json"})
    assert malformed.status_code == 422
    assert client.post(ENDPOINT, data={"context_json": "{broken", "benchmark_confirmed": "true"}, headers={"X-OpenAI-Key": KEY}).status_code == 422
    assert not model and not analysis.jobs


@pytest.mark.parametrize("field,value", [("benchmark", " "), ("task_requirements", "\n"), ("answer_requirements", ""),
                                        ("deployment", 12), ("benchmark", "x" * 201), ("deployment", "x" * 12_001),
                                        ("validity_concerns", None), ("scoring", {"score": 5})])
def test_invalid_direct_context_is_rejected_before_any_work(client, model, field, value):
    context = {**CONTEXT, field: value}
    assert client.post("/api/item-analysis/direct/setup", json=context).status_code == 422
    response = client.post(ENDPOINT, data={"context_json": json.dumps(context), "benchmark_confirmed": "true"},
                           files={"items_file": ("items.json", '[{"content":"Question"}]')}, headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 422
    assert not model and not analysis.jobs


@pytest.mark.parametrize("confirmed", [None, "false"])
@pytest.mark.parametrize("selection", ["source", "upload"])
def test_direct_confirmation_is_mandatory(client, monkeypatch, model, confirmed, selection):
    candidate = databank_catalog(monkeypatch)
    fields = {"context_json": json.dumps(CONTEXT)}
    if confirmed is not None:
        fields["benchmark_confirmed"] = confirmed
    files = None
    if selection == "source":
        fields.update(source_id=candidate["id"], source_revision=CATALOG_REVISION)
    else:
        files = {"items_file": ("items.json", '[{"content":"Question"}]')}
    response = client.post(ENDPOINT, data=fields, files=files, headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 400 and "Confirm" in response.json()["detail"]
    assert not model and not analysis.jobs


@pytest.mark.parametrize("selection", ["missing_revision", "stale_revision", "unlisted", "private_preset", "arbitrary_path"])
def test_direct_snapshot_must_be_catalog_allowlisted_and_revision_bound(client, monkeypatch, model, selection):
    candidate = databank_catalog(monkeypatch)
    fields = {"context_json": json.dumps(CONTEXT), "benchmark_confirmed": "true", "source_id": candidate["id"], "source_revision": CATALOG_REVISION}
    if selection == "missing_revision":
        del fields["source_revision"]
    elif selection == "stale_revision":
        fields["source_revision"] = "b" * 40
    else:
        fields["source_id"] = {"unlisted": "databank:" + CATALOG_REVISION + ":secret", "private_preset": "mmlu", "arbitrary_path": "/private/items.parquet"}[selection]
    response = client.post(ENDPOINT, data=fields, headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 409
    assert not model and not analysis.jobs


def test_direct_upload_freezes_requirements_and_completes_without_benchmark_scores(client, monkeypatch, model):
    monkeypatch.setattr(item_analysis_assessment, "resolve", lambda *args: pytest.fail("Direct runs must not resolve scoring"))
    monkeypatch.setattr(analysis, "CHECKPOINT_SIZE", 1)
    context = deepcopy(CONTEXT)
    rows = [{"item_id": "q1", "content": {"question": "¿Cuánto es 2+2?", "choices": ["3", "4"]}, "reference_answer": {"correct": "4"}},
            {"content": "Explain the calculation in Spanish."}]
    access = start_direct(client, context, rows=rows)
    context["answer_requirements"] = "Changed after submission"
    ready = settled(client, access)
    assert ready["status"] == "ready", ready
    assert ready["assessment"]["direct_context"] == CONTEXT
    assert ready["assessment"]["kind"] == "direct"
    assert "scoring" not in ready["assessment"]
    assert ready["spec"]["deployment"] == ready["assessment"]["deployment"]
    assert ready["spec"]["analysis_basis"] == "deployment_requirements"
    assert ready["summary"]["assessment_status"] == "not_run"
    assert ready["summary"].get("original_assessment") is None
    assert {d["id"] for d in ready["summary"]["dimensions"]} == {"input_ontology", "input_content", "input_form", "output_ontology", "output_content", "output_form"}
    assert next(item for item in ready["items"] if item["item_id"] == "q1")["content"] == rows[0]["content"]
    assert not model
    payload = ready["spec"]
    assert "direct_context.json#/task_requirements" in payload["source_registry"]
    assert not any(key.startswith("scoring.json") for key in payload["source_registry"])
    assert payload["source_registry"]["direct_context.json#/answer_requirements"] == CONTEXT["answer_requirements"]
    directory = analysis.jobs[access["run_id"]].directory
    assert read_json(directory / "direct_context.json") == CONTEXT
    assert "scoring" not in read_json(directory / "evidence.json")
    assert check_prepared(directory)["assessment"]["id"] == ready["assessment"]["id"]
    assert not (directory / "scoring.json").exists()
    assert classify(client, access)["status"] == "checkpoint"
    assert len(model) == 1
    response = client.post(url(access) + "/classify", json={"scope": "all"}, headers=headers(access, key=True))
    assert response.status_code == 202, response.text
    complete = settled(client, access)
    assert complete["status"] == "complete" and complete["complete"] == 2
    assert client.get(url(access)).status_code == 404
    assert client.get(url(access), headers={"X-Review-Token": "wrong-token"}).status_code == 404
    assert client.get(url(access), headers=headers(access)).json()["assessment"] == ready["assessment"]
    report = client.get(url(access) + "/download/report", headers=headers(access))
    assert report.status_code == 200 and "no benchmark assessment was supplied" in report.text.lower()
    assert all(KEY not in path.read_text() for path in directory.iterdir() if path.is_file())
    assert directory.stat().st_mode & 0o777 == 0o700
    analysis.jobs[access["run_id"]].updated_at = time.time() - 3601
    assert client.get(url(access), headers=headers(access)).status_code == 200
    assert client.delete(url(access), headers=headers(access)).status_code == 204
    assert not directory.exists()


def test_direct_catalog_alias_preserves_full_source_without_old_assessment(client, tmp_path, monkeypatch, model):
    source = prepared_snapshot(tmp_path, monkeypatch, count=3, benchmark="mmlu", assessment_context="Old unrelated deployment")
    candidate = databank_catalog(monkeypatch, source)
    access = start_direct(client, source=candidate)
    ready = settled(client, access)
    assert ready["status"] == "ready" and ready["total"] == 3, ready
    directory = analysis.jobs[access["run_id"]].directory
    dataset = read_json(directory / "dataset.json")
    assert dataset["source_benchmark"] == "mmlu" and dataset["benchmark"] == CONTEXT["benchmark"]
    assert dataset["source"]["sha256"] == read_json(source / "dataset.json")["source"]["sha256"]
    assert "path" not in dataset["source"]
    assert not any(key.startswith("scoring.json") for key in ready["spec"]["source_registry"])
    assert "Old unrelated deployment" not in json.dumps(ready["spec"])
    assert ready["summary"].get("original_assessment") is None


def test_direct_source_preparation_failure_makes_no_paid_calls(client, monkeypatch, model):
    candidate = databank_catalog(monkeypatch)

    def fail(*args, **kwargs):
        raise analysis.item_analysis_databank.DataBankError("The selected snapshot could not be prepared. No model calls were made.")

    monkeypatch.setattr(analysis.item_analysis_databank, "prepare_candidate", fail)
    failed = settled(client, start_direct(client, source=candidate))
    assert failed["status"] == "failed" and "No model calls" in failed["message"]
    assert not model


def test_direct_start_requires_one_source_and_capacity_but_no_provider_key(client, monkeypatch, model):
    fields = {"context_json": json.dumps(CONTEXT), "benchmark_confirmed": "true"}
    files = {"items_file": ("items.json", '[{"content":"Question"}]')}
    assert client.post(ENDPOINT, data=fields, headers={"X-OpenAI-Key": KEY}).status_code == 400
    assert client.post(ENDPOINT, data={**fields, "source_id": "source", "source_revision": CATALOG_REVISION}, files=files, headers={"X-OpenAI-Key": KEY}).status_code == 400
    assert client.post(ENDPOINT, data={**fields, "source_revision": CATALOG_REVISION}, files=files, headers={"X-OpenAI-Key": KEY}).status_code == 400
    monkeypatch.setattr(analysis, "MAX_ACTIVE", 0)
    assert client.post(ENDPOINT, data=fields, files=files, headers={"X-OpenAI-Key": KEY}).status_code == 429
    assert not model and not analysis.jobs


def test_direct_preparation_succeeds_without_provider_key(client, model):
    response = client.post(ENDPOINT, data={"context_json": json.dumps(CONTEXT), "benchmark_confirmed": "true"},
                           files={"items_file": ("items.json", '[{"content":"Question"}]')})
    assert response.status_code == 202
    assert settled(client, response.json())["status"] == "ready" and not model
