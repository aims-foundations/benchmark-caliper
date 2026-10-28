"""The website exercises the real item-analysis pipeline without paid calls."""

import asyncio
from contextlib import asynccontextmanager
from copy import deepcopy
import csv
from datetime import datetime, timezone
import io
import json
import re
from pathlib import Path
import shutil
from threading import Event
import time

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from anthropic_api_package_release.item_analysis import model_client, prepare
from anthropic_api_package_release.item_analysis.scoring import DIMENSIONS, dimension_descriptors
from anthropic_api_package_release.item_analysis.storage import read_json, write_json
from website.server import db, item_analysis as analysis, item_analysis_assessment, logging_gate, pipeline_runner

KEY = "sk-test-private-item-analysis-key"
CATALOG_REVISION = "a" * 40
BODY = {"example_id": "illustrative", "specification_mode": "provided"}
REMOTE_CONTEXTS = (
    ("gsm8k", "gsm8k", "US K–8 math tutoring"),
    ("humaneval", "humaneval", "US Python code review"),
    ("toxigen", "toxigen", "Bangladesh Gausa clinical toxicity"),
    ("toxigen-south-asia", "toxigen", "South Asia academic toxicity research"),
)


def request_payload(user):
    """Decode the fixed generation template or the per-item JSON request."""
    if user.lstrip().startswith('{'):
        return json.JSONDecoder().raw_decode(user)[0]
    payload = {}
    for tag in ('benchmark', 'deployment_description', 'source_registry', 'dataset_profile', 'example_items'):
        match = re.search(fr'<{tag}>\n(.*?)\n</{tag}>', user, re.S)
        assert match, tag
        payload[tag] = json.loads(match[1]) if tag in {'source_registry', 'dataset_profile', 'example_items'} else match[1]
    payload["source_registry"] = {key: entry["content"] for key, entry in payload["source_registry"].items()}
    return payload


def context_response(payload):
    registry = payload['source_registry']
    source = 'direct_context.json#/task_requirements' if 'direct_context.json#/task_requirements' in registry else 'deployment_description.txt'
    return {
        'fixed_catalog_version': 'caliper_generic_items_v1', 'benchmark': payload['benchmark'],
        'deployment_description': payload['deployment_description'],
        'input_category_inventory': {'completeness': 'partial', 'completeness_source_ids': [],
            'categories': [{'id': 'required_001', 'name': 'Declared deployment tasks',
                            'definition': registry[source], 'source_ids': [source]}],
            'evidence_gaps': ['No exhaustive category inventory supplied.']},
        'context_by_classifier': {id: {'deployment_requirements': [{'statement': registry[source], 'source_ids': [source]}],
            'benchmark_evidence': [], 'prior_hypotheses': [],
            'evidence_gaps': ['Test fixture has no domain or stakeholder comparison evidence.']}
            for id in ('input_ontology', 'input_content', 'output_ontology', 'output_content')},
    }


@pytest.fixture
def model(monkeypatch):
    calls = []

    async def fake_call(**arguments):
        assert arguments["api_key"] == KEY
        payload = request_payload(arguments["user"])
        calls.append((arguments["model"], payload))
        assert arguments["model"] == model_client.MODEL_ID
        assert arguments["reasoning_effort"] == model_client.REASONING_EFFORT
        if "dimensions" in payload.get("output_schema", {}).get("properties", {}):
            slots = payload["output_schema"]["properties"]["dimensions"]["properties"]
            assert set(slots) == set(DIMENSIONS)
            dimensions = {cid: {"score": 4,
                                "evidence": ["content: The supplied question and answer choices."],
                                "justification": "Deterministic test response, not a genuine assessment.",
                                "information_gaps": []} for cid in slots}
            if payload["item"]["item_id"].endswith("01"):
                dimensions["input_content"].update(score=None, information_gaps=["No regional comparison evidence was supplied."])
            text = json.dumps({"dimensions": dimensions})
        elif "item" not in payload:
            text = json.dumps(context_response(payload))
        else:
            slots = payload["output_schema"]["properties"]["labels"]["properties"]
            labels = {slot: {"label": definition["properties"]["label"]["enum"][0],
                             "evidence": ["The supplied question and answer choices."],
                             "justification": "Deterministic test response, not a genuine assessment."}
                      for slot, definition in slots.items()}
            assert len(slots) == 1
            if 'input_ontology' in labels:
                labels['input_ontology'].update(matched_category_ids=[payload['input_category_inventory']['categories'][0]['id']], scope_exclusion_source_ids=[])
            if 'input_content' in labels and payload["item"]["item_id"].endswith("01"):
                labels["input_content"]["label"] = 'insufficient_evidence'
            text = json.dumps({"labels": labels})
        return model_client.CallResult(text, arguments["model"], 100, 30, 1,
                                      cached_input_tokens=20, reasoning_tokens=7)

    monkeypatch.setattr(model_client, "call_text_async", fake_call)
    return calls

@pytest.fixture
def client(tmp_path, monkeypatch, model):
    monkeypatch.setattr(db, "DEFAULT_DB_PATH", tmp_path / "data/runs.db")
    monkeypatch.setattr(analysis, "jobs", {})
    monkeypatch.delenv("ITEM_ANALYSIS_RETENTION_SECONDS", raising=False)
    monkeypatch.setenv("ITEM_ANALYSIS_PREPARED_DIR", str(tmp_path / "not-configured"))
    monkeypatch.setattr(analysis.item_analysis_databank, "search_candidates", lambda assessment, query=None: {
        "candidates": [], "status": "ready", "message": "No matching Data Bank snapshot.",
        "repo": "aims-foundations/measurement-db-pp", "revision": CATALOG_REVISION, "requires_confirmation": True,
    })

    @asynccontextmanager
    async def lifespan(_):
        yield
        await analysis.shutdown()

    app = FastAPI(lifespan=lifespan)
    app.include_router(analysis.router)
    with TestClient(app) as test_client:
        yield test_client


def start(client, *, example="illustrative", mode="provided"):
    response = client.post("/api/item-analysis/runs", json={"example_id": example, "specification_mode": mode},
                           headers={"X-OpenAI-Key": KEY} if mode == "generate" else {})
    assert response.status_code == 202, response.text
    return response.json()


def headers(access, *, key=False):
    return {"X-Review-Token": access["run_secret"], **({"X-OpenAI-Key": KEY} if key else {})}


def url(access):
    return f"/api/item-analysis/runs/{access['run_id']}"


def settled(client, access):
    for _ in range(400):
        response = client.get(url(access), headers=headers(access))
        assert response.status_code == 200, response.text
        if response.json()["status"] not in analysis.ACTIVE_STATUSES:
            return response.json()
        time.sleep(.01)
    pytest.fail("Analysis did not finish its phase")


def classify(client, access, scope="pilot"):
    response = client.post(url(access) + "/classify", json={"scope": scope}, headers=headers(access, key=True))
    assert response.status_code == 202, response.text
    return settled(client, access)


def prepared_snapshot(tmp_path, monkeypatch, count=105, *, benchmark=None, assessment_context=None):
    """Make a small local snapshot using the shared production preparation step."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    fixture = read_json(analysis.FIXTURE_PATH)
    if benchmark is not None:
        context = assessment_context or benchmark
        fixture["assessment"]["benchmark"] = benchmark
        fixture["assessment"]["dimensions"]["input_form"] = {
            "score": 4, "justification": f"Original {context} input-form assessment.",
        }
        fixture["deployment"] = f"The original deployment requirements for {context}."
        fixture["classifier_spec"]["benchmark"] = benchmark
        fixture["classifier_spec"]["deployment_description"] = fixture["deployment"]
        for item in fixture["items"]:
            item["benchmark_id"] = benchmark
            item["content"] = f"{benchmark} source item: {item['content']}"
    source, output = tmp_path / "source", tmp_path / "prepared"
    source.mkdir()
    write_json(source / "scoring.json", fixture["assessment"])
    for filename, key in (("deployment_description.txt", "deployment"),
                          ("elicitation_summary.md", "elicitation_summary"),
                          ("dataset_analysis_report.md", "dataset_analysis_report")):
        (source / filename).write_text(fixture[key], encoding="utf-8")
    rows = [dict(deepcopy(fixture["items"][i % len(fixture["items"])]),
                 item_id=f"{benchmark or 'test'}-{i:04d}") for i in range(count)]
    pq.write_table(pa.Table.from_pylist(rows), source / "items.parquet")
    prepare.prepare(source, source / "items.parquet", output, source_repo="test-only", source_revision="fixture")
    write_json(output / "classifier_spec.original.json", fixture["classifier_spec"])
    monkeypatch.setenv("ITEM_ANALYSIS_PREPARED_DIR", str(output))
    return output


def remote_source(monkeypatch, prepared=None, *, available=True):
    """Exercise the HTTP adapter's remote branch without contacting Hugging Face."""
    monkeypatch.delenv("ITEM_ANALYSIS_PREPARED_DIR", raising=False)
    entries = [{
        "id": "mmlu", "title": "MMLU", "description": "Pinned Hugging Face snapshot.",
        "benchmark": "mmlu", "deployment": "The catalog deployment.",
        "source_label": "measurement-db-pp MMLU", "item_count": 14015,
        "available": available, "supplied_spec_available": True,
        "source_url": "https://huggingface.co/datasets/aims-foundations/measurement-db-pp/tree/main/mmlu",
        "source_revision": "advertised-revision",
    }]
    for example_id, benchmark, assessment_context in REMOTE_CONTEXTS:
        entries.append({
            "id": example_id, "title": f"{benchmark.upper()} · {assessment_context}",
            "assessment_title": assessment_context,
            "description": "Pinned benchmark snapshot.", "benchmark": benchmark,
            "deployment": f"The advertised {assessment_context} deployment.",
            "source_label": f"Original {benchmark} dataset", "item_count": 1000,
            "available": available, "supplied_spec_available": False,
            "source_url": f"https://huggingface.co/datasets/test/{benchmark}",
            "source_revision": f"advertised-{benchmark}-revision",
        })
    if not available:
        for entry in entries:
            entry["unavailable_reason"] = f"The {entry['title']} dataset is unavailable on this server."
    monkeypatch.setattr(analysis.item_analysis_source, "source_entries", lambda: deepcopy(entries))
    monkeypatch.setattr(analysis.item_analysis_source, "source_entry", lambda example_id="mmlu":
                        deepcopy(next(entry for entry in entries if entry["id"] == example_id)))
    calls = []

    def prepare_remote(directory, stopped=None, *, example_id="mmlu"):
        assert stopped is not None and not stopped()
        assert prepared is not None, "This test must not prepare or download a dataset"
        assert example_id in {entry["id"] for entry in entries}
        source = prepared[example_id] if isinstance(prepared, dict) else prepared
        calls.append((directory, example_id))
        for name in analysis.PREPARED_FILES:
            shutil.copyfile(source / name, directory / name)
        supplied = directory / "provided_spec.json"
        if (source / "classifier_spec.original.json").is_file():
            shutil.copyfile(source / "classifier_spec.original.json", supplied)
        return supplied

    monkeypatch.setattr(analysis.item_analysis_source, "prepare_source", prepare_remote)
    return calls


def test_default_catalog_lists_all_real_benchmarks_before_illustrative_example(client, monkeypatch):
    calls = remote_source(monkeypatch)
    catalog = client.get("/api/item-analysis/catalog").json()
    assert [entry["id"] for entry in catalog["examples"]] == [
        "mmlu", "gsm8k", "humaneval", "toxigen", "toxigen-south-asia", "illustrative",
    ]
    toxicity_contexts = [entry for entry in catalog["examples"] if entry["benchmark"] == "toxigen"]
    assert len(toxicity_contexts) == 2
    assert len({entry["assessment_title"] for entry in toxicity_contexts}) == 2
    assert catalog["examples"][0]["item_count"] == 14015
    assert "measurement-db-pp" in catalog["examples"][0]["source_url"]
    assert analysis.prepared_directory() is None
    assert not calls


def test_remote_preparation_uses_actual_frozen_metadata_and_hides_paths(client, tmp_path, monkeypatch, model):
    prepared = prepared_snapshot(tmp_path, monkeypatch)
    calls = remote_source(monkeypatch, prepared)
    access = start(client, example="mmlu")
    ready = settled(client, access)
    assert ready["status"] == "ready" and ready["total"] == 105
    assert ready["example"]["item_count"] == 105
    assert ready["example"]["deployment"] == read_json(prepared / "evidence.json")["deployment"]
    assert ready["example"]["source_revision"] == "fixture"
    assert ready["example"]["source_repo"] == "test-only"
    assert len(ready["example"]["source_sha256"]) == 64
    assert ready["processed"] == 0 and not model
    directory = analysis.jobs[access["run_id"]].directory
    assert len(calls) == 1 and calls[0][1] == "mmlu"
    assert calls[0][0].parent == directory.parent and not calls[0][0].exists()
    assert "path" not in read_json(directory / "dataset.json")["source"]
    assert "assessment_dir" not in read_json(directory / "evidence.json")


@pytest.mark.parametrize("example_id,benchmark,assessment_context", REMOTE_CONTEXTS)
def test_selected_context_drives_preparation_scoring_and_exports(
        client, tmp_path, monkeypatch, model, example_id, benchmark, assessment_context):
    prepared = prepared_snapshot(tmp_path, monkeypatch, count=3, benchmark=benchmark,
                                 assessment_context=assessment_context)
    (prepared / "classifier_spec.original.json").unlink()
    calls = remote_source(monkeypatch, {example_id: prepared})
    evidence = read_json(prepared / "evidence.json")
    expected_items = {item["item_id"]: item for item in (
        json.loads(line) for line in (prepared / "items.jsonl").read_text().splitlines())}

    access = start(client, example=example_id, mode="generate")
    ready = settled(client, access)
    assert ready["status"] == "ready", ready
    assert ready["example"]["id"] == example_id
    assert ready["example"]["benchmark"] == benchmark
    assert ready["example"]["assessment_title"] == assessment_context
    assert ready["example"]["deployment"] == evidence["deployment"]
    assert ready["example"]["item_count"] == ready["total"] == 3
    assert ready["example"]["source_revision"] == "fixture"
    assert ready["spec"]["benchmark"] == benchmark
    assert ready["spec"]["deployment"] == evidence["deployment"]
    assert ready["summary"]["specification"]["source"]["kind"] == "deterministic"
    directory = analysis.jobs[access["run_id"]].directory
    assert len(calls) == 1 and calls[0][1] == example_id
    assert calls[0][0].parent == directory.parent and not calls[0][0].exists()
    assert not model
    assert ready["spec"]["source_registry"]["deployment_description.txt"] == evidence["deployment"]
    assert not any(key.startswith("scoring.json") for key in ready["spec"]["source_registry"])

    result = classify(client, access)
    assert result["status"] == "complete", result
    assert result["complete"] == result["processed"] == result["total"] == 3
    classification = [payload for _, payload in model if "item" in payload]
    assert len(classification) == 3
    assert {payload["item"]["item_id"]: payload["item"] for payload in classification} == expected_items
    assert all(payload["deployment_description"] == evidence["deployment"]
               for payload in classification)
    exports = {artifact: client.get(url(access) + f"/download/{artifact}", headers=headers(access))
               for artifact in analysis.ARTIFACTS}
    assert all(response.status_code == 200 for response in exports.values())
    assert exports["spec"].json()["benchmark"] == benchmark
    summary = exports["summary"].json()
    assert summary["benchmark"] == benchmark
    assert summary["deployment"] == summary["original_deployment"] == evidence["deployment"]
    assert summary["original_assessment"] == evidence["scoring"]["dimensions"]
    item_rows = list(csv.DictReader(io.StringIO(exports["items"].text)))
    assert {row["item_id"] for row in item_rows} == set(expected_items)
    assert all(benchmark + " source item:" in row["content"] for row in item_rows)
    assert evidence["deployment"] in exports["report"].text
    assert evidence["scoring"]["dimensions"]["input_form"]["justification"] in exports["report"].text


@pytest.mark.parametrize("example_id", [context[0] for context in REMOTE_CONTEXTS])
def test_remote_benchmark_without_supplied_criteria_uses_fixed_context(client, tmp_path, monkeypatch, model, example_id):
    source = prepared_snapshot(tmp_path, monkeypatch, count=2)
    (source / "classifier_spec.original.json").unlink()
    calls = remote_source(monkeypatch, {example_id: source})
    entry = next(entry for entry in client.get("/api/item-analysis/catalog").json()["examples"] if entry["id"] == example_id)
    assert entry["available"] and not entry["supplied_spec_available"]
    access = start(client, example=example_id)
    ready = settled(client, access)
    assert ready["status"] == "ready" and ready["spec"]["analysis_type"] == "six_scores"
    assert len(calls) == 1 and not model


@pytest.mark.parametrize("mode", ["provided", "generate"])
def test_unknown_benchmark_cannot_prepare_data_or_call_model(client, monkeypatch, model, mode):
    calls = remote_source(monkeypatch)
    response = client.post("/api/item-analysis/runs", json={"example_id": "unlisted_benchmark", "specification_mode": mode},
                           headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 404
    assert not analysis.jobs and not calls and not model
    assert not (db.DEFAULT_DB_PATH.parent / "item-analysis").exists()


def test_local_override_displays_actual_benchmark_and_prepared_assessment(client, tmp_path, monkeypatch, model):
    prepared_snapshot(tmp_path, monkeypatch, count=3, benchmark="gsm8k")
    entries = client.get("/api/item-analysis/catalog").json()["examples"]
    assert [entry["id"] for entry in entries] == ["mmlu", "illustrative"]
    entry = entries[0]
    assert entry["title"] == "gsm8k · Prepared assessment"
    assert entry["benchmark"] == entry["benchmark_title"] == "gsm8k"
    assert entry["assessment_title"] == "Prepared assessment"
    ready = settled(client, start(client, example="mmlu"))
    assert ready["status"] == "ready"
    assert ready["example"]["title"] == entry["title"]
    assert ready["spec"]["benchmark"] == "gsm8k" and not model


@pytest.mark.parametrize("failure", ["DatasetAccessError", "DatasetPreparationError"])
def test_dataset_failure_is_distinct_from_model_key_failure(client, monkeypatch, model, failure):
    remote_source(monkeypatch)
    message = "The MMLU source could not be loaded. Ask the website administrator to check dataset access."

    def broken(*args, **kwargs):
        raise getattr(analysis.item_analysis_source, failure)(message)

    monkeypatch.setattr(analysis.item_analysis_source, "prepare_source", broken)
    access = start(client, example="mmlu")
    failed = settled(client, access)
    assert failed["status"] == "failed" and failed["error"] == message
    assert failed["items"] == [] and failed["processed"] == 0
    assert "API key" not in failed["message"] and not model


def test_unavailable_remote_source_cannot_start_a_run(client, monkeypatch, model):
    calls = remote_source(monkeypatch, available=False)
    response = client.post("/api/item-analysis/runs", json={"example_id": "mmlu", "specification_mode": "provided"})
    assert response.status_code == 503
    assert "dataset is unavailable" in response.json()["detail"]
    assert not analysis.jobs and not calls and not model


def test_bundled_example_always_available_and_no_predictions(client, model):
    catalog = client.get("/api/item-analysis/catalog")
    assert catalog.headers["cache-control"] == "no-store"
    assert catalog.json()["checkpoint_size"] == 100
    assert [entry["id"] for entry in catalog.json()["examples"]] == ["illustrative"]
    access = start(client)
    job = settled(client, access)
    assert job["status"] == "ready" and job["total"] == 10
    assert job["processed"] == 0 and all(item["status"] == "pending" for item in job["items"])
    assert job["completed_judgments"] == 0
    assert job["remaining_judgments"] == {"pilot": 60, "all": 60}
    assert "Illustrative" in job["example"]["source_label"]
    assert job["summary"]["original_assessment"]["input_form"]["score"] is None
    assert job["summary"]["specification"]["source"]["kind"] == "deterministic"
    assert not model
    assert all(c["applicable"] for c in job["spec"]["classifiers"])
    assert {c["id"] for c in job["spec"]["classifiers"]} == set(DIMENSIONS)


@pytest.mark.parametrize("mode", ["provided", "generate"])
def test_real_pipeline_prepares_context_then_scores_and_exports(client, model, mode):
    access = start(client, mode=mode)
    ready = settled(client, access)
    assert ready["status"] == "ready"
    expected_model = {"provider": "openai", "model_id": "gpt-6-luna", "reasoning_effort": "low"}
    assert ready["model"] == access["model"] == expected_model
    assert ready["summary"]["specification"]["source"]["kind"] == "deterministic"
    assert not model
    result = classify(client, access)
    assert result["status"] == "complete"
    assert result["complete"] == result["processed"] == result["total"] == 10
    assert result["errors"] == 0 and result["summary"]["complete_snapshot"]
    assert result["completed_judgments"] == 60
    assert result["remaining_judgments"] == {"pilot": 0, "all": 0}
    regional = next(c for c in result["summary"]["classifiers"] if c["id"] == "input_content")
    assert regional["unknown"] == 1 and regional["known"] == 9
    call_count = 10
    assert result["usage"] == {"input_tokens": 100 * call_count, "output_tokens": 30 * call_count,
                               "cached_input_tokens": 20 * call_count, "reasoning_tokens": 7 * call_count}
    assert all("item" in payload for _, payload in model)
    for artifact, (filename, _) in analysis.ARTIFACTS.items():
        response = client.get(url(access) + f"/download/{artifact}", headers=headers(access))
        assert response.status_code == 200
        assert filename in response.headers["content-disposition"]
        assert KEY not in response.text
    worksheet = client.get(url(access) + "/download/review", headers=headers(access)).text
    assert "Deterministic test" not in worksheet
    assert all(not row["input_content.justification"] for row in csv.DictReader(io.StringIO(worksheet)))
    assert client.get(url(access) + "/download/evidence", headers=headers(access)).status_code == 404
    directory = analysis.jobs[access["run_id"]].directory
    run = read_json(directory / "run.json")
    assert {key: run[key] for key in expected_model} == expected_model
    assert all(KEY not in path.read_text() for path in directory.iterdir() if path.is_file())


@pytest.mark.parametrize("source_kind", ["configured", "remote"])
def test_first_100_checkpoint_full_continuation_and_no_duplicate_calls(client, model, tmp_path, monkeypatch, source_kind):
    source = prepared_snapshot(tmp_path, monkeypatch, count=105)
    if source_kind == "remote":
        remote_source(monkeypatch, source)
    access = start(client, example="mmlu")
    assert settled(client, access)["status"] == "ready"
    pilot = classify(client, access)
    assert pilot["status"] == "checkpoint" and pilot["can_continue"]
    assert (pilot["processed"], pilot["total"]) == (100, 105)
    assert pilot["completed_judgments"] == 600
    assert pilot["remaining_judgments"] == {"pilot": 0, "all": 30}
    first_ids = [payload["item"]["item_id"] for _, payload in model if "item" in payload]
    assert len(first_ids) == len(set(first_ids)) == 100
    complete = classify(client, access, scope="all")
    assert complete["status"] == "complete" and complete["complete"] == 105
    assert sum("item" in payload for _, payload in model) == 105
    page = client.get(url(access) + "?page=6", headers=headers(access)).json()
    assert page["pagination"] == {"page": 6, "page_size": 20, "total_pages": 6}
    assert len(page["items"]) == 5
    assert client.post(url(access) + "/classify", json={"scope": "all"}, headers=headers(access, key=True)).status_code == 409


def test_private_endpoints_and_keys_and_body_validation(client, model):
    response = client.post("/api/item-analysis/runs", json={**BODY, "specification_mode": "generate"})
    assert response.status_code == 202
    assert settled(client, response.json())["status"] == "ready"
    assert not model
    for bad in ({**BODY, "input_path": "/etc/passwd"}, {**BODY, "example_id": "../secret"},
                {**BODY, "model": "another-model"}):
        assert client.post("/api/item-analysis/runs", json=bad).status_code == 422
    access = start(client)
    settled(client, access)
    for suffix in ("", "/download/spec"):
        assert client.get(url(access) + suffix).status_code == 404
    for suffix, body in (("/cancel", {}), ("/classify", {"scope": "pilot"})):
        assert client.post(url(access) + suffix, json=body, headers={"X-Review-Token": "wrong"}).status_code == 404
    assert client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access)).status_code == 401
    assert client.post(url(access) + "/classify", json={"scope": "pilot"},
                       headers={**headers(access), "X-Anthropic-Key": KEY}).status_code == 401
    assert not model


def test_provider_failure_is_sanitized_and_can_resume(client, monkeypatch, model):
    access = start(client)
    settled(client, access)
    original = model_client.call_text_async

    async def broken(**arguments):
        raise ValueError(f"Provider error includes {KEY} and arbitrary sensitive text")

    monkeypatch.setattr(model_client, "call_text_async", broken)
    failed = classify(client, access)
    assert failed["status"] == "failed" and failed["errors"] == 1
    assert KEY not in json.dumps(failed)
    assert "arbitrary sensitive text" not in json.dumps(failed)
    assert failed["provider_error"]["code"] == "internal_error"
    assert failed["message"] == failed["provider_error"]["message"]
    directory = analysis.jobs[access["run_id"]].directory
    assert all(KEY not in path.read_text() for path in directory.iterdir() if path.is_file())
    monkeypatch.setattr(model_client, "call_text_async", original)
    finished = classify(client, access)
    assert finished["status"] == "complete" and finished["errors"] == 0
    assert finished["provider_error"] is None
    assert analysis.jobs[access["run_id"]].provider_error is None


def test_provider_failure_preserves_completed_items_and_retries_only_missing_ones(client, monkeypatch, model):
    access = start(client)
    ready = settled(client, access)
    first_id, failed_id = [item["item_id"] for item in ready["items"][:2]]
    original = model_client.call_text_async

    async def fail_second_item(**arguments):
        if request_payload(arguments["user"])["item"]["item_id"] == failed_id:
            raise ValueError(f"Private failure {KEY}")
        return await original(**arguments)

    monkeypatch.setattr(model_client, "call_text_async", fail_second_item)
    failed = classify(client, access)
    assert failed["status"] == "failed" and failed["errors"] == failed["complete"] == 1
    assert failed["completed_judgments"] == 6
    assert failed["remaining_judgments"] == {"pilot": 54, "all": 54}
    first = next(item for item in failed["items"] if item["item_id"] == first_id)
    assert set(first["dimensions"]) == set(DIMENSIONS)
    assert next(item for item in failed["items"] if item["item_id"] == failed_id)["dimensions"] == {}
    assert "Private failure" not in json.dumps(failed) and KEY not in json.dumps(failed)
    monkeypatch.setattr(model_client, "call_text_async", original)
    complete = classify(client, access)
    assert complete["status"] == "complete" and complete["completed_judgments"] == 60
    ids = [payload["item"]["item_id"] for _, payload in model]
    assert len(ids) == len(set(ids)) == 10


def test_invalid_item_response_repairs_once_and_preserves_other_completed_items(client, monkeypatch, model):
    access = start(client)
    first_id = settled(client, access)["items"][0]["item_id"]
    original = model_client.call_text_async
    invalid_calls = []

    async def invalid_item(**arguments):
        if request_payload(arguments["user"])["item"]["item_id"] == first_id:
            invalid_calls.append(arguments)
            return model_client.CallResult('{"dimensions": {}}', arguments["model"], 100, 30, 1)
        return await original(**arguments)

    monkeypatch.setattr(model_client, "call_text_async", invalid_item)
    failed = classify(client, access)
    assert len(invalid_calls) == 2
    assert failed["status"] == "failed"
    assert failed["complete"] == 9 and failed["errors"] == 1 and failed["completed_judgments"] == 54
    assert failed["remaining_judgments"] == {"pilot": 6, "all": 6}
    first = next(item for item in failed["items"] if item["item_id"] == first_id)
    assert first["dimensions"] == {} and first["status"] == "error"
    monkeypatch.setattr(model_client, "call_text_async", original)
    complete = classify(client, access, scope="all")
    assert complete["status"] == "complete" and complete["completed_judgments"] == 60
    ids = [payload["item"]["item_id"] for _, payload in model]
    assert len(ids) == len(set(ids)) == 10


@pytest.mark.parametrize("mode", ["generate", "provided"])
@pytest.mark.parametrize("code,status_code,parameter", [
    ("authentication", 401, None),
    ("model_unavailable", 404, "model"),
    ("permission", 403, None),
    ("quota", 429, None),
    ("rate_limit", 429, None),
    ("invalid_request", 400, "reasoning.effort"),
])
def test_safe_provider_diagnostics_reach_scoring_after_free_preparation(
        client, monkeypatch, mode, code, status_code, parameter):
    error = model_client.ModelRequestError(
        f"Raw provider response contains {KEY} and confidential provider text",
        code=code, status_code=status_code, parameter=parameter,
    )

    async def rejected(**arguments):
        raise error

    monkeypatch.setattr(model_client, "call_text_async", rejected)
    access = start(client, mode=mode)
    state = settled(client, access)
    assert state["status"] == "ready"
    failed = classify(client, access)
    assert failed["status"] == "failed"
    assert failed["message"] == failed["error"] == error.public_message
    assert failed["provider_error"] == {
        "code": code, "status_code": status_code, "message": error.public_message,
    }
    assert failed["failure"] is None
    assert KEY not in json.dumps(failed)
    assert "confidential provider text" not in json.dumps(failed)
    directory = analysis.jobs[access["run_id"]].directory
    for path in directory.iterdir():
        if path.is_file():
            assert KEY not in path.read_text()
            assert "confidential provider text" not in path.read_text()


def test_incomplete_response_counts_billed_usage_without_saving_provider_text(client, monkeypatch):
    access = start(client)
    settled(client, access)

    async def incomplete(**arguments):
        result = model_client.CallResult(KEY, arguments["model"], 100, 30, 1,
                                         cached_input_tokens=20, reasoning_tokens=7)
        raise model_client.ModelResponseError(f"Incomplete response contains {KEY}", result)

    monkeypatch.setattr(model_client, "call_text_async", incomplete)
    failed = classify(client, access)
    assert failed["status"] == "failed" and failed["errors"] == 1
    assert failed["usage"] == {"input_tokens": 100, "output_tokens": 30,
                               "cached_input_tokens": 20, "reasoning_tokens": 7}
    assert KEY not in json.dumps(failed)
    assert "Incomplete response contains" not in json.dumps(failed)
    assert failed["provider_error"]["code"] == "incomplete_response"
    assert failed["message"] == failed["provider_error"]["message"]
    directory = analysis.jobs[access["run_id"]].directory
    assert all(KEY not in path.read_text() for path in directory.iterdir() if path.is_file())


def test_model_echo_of_key_is_redacted_before_saving(client, monkeypatch, model):
    access = start(client)
    settled(client, access)
    original = model_client.call_text_async

    async def echo_key(**arguments):
        result = await original(**arguments)
        payload = json.loads(result.text)
        for label in payload["dimensions"].values():
            label["justification"] = f"The model echoed {KEY} in its explanation."
        return model_client.CallResult(json.dumps(payload), result.model, result.input_tokens,
                                       result.output_tokens, result.latency_ms)

    monkeypatch.setattr(model_client, "call_text_async", echo_key)
    complete = classify(client, access)
    assert complete["status"] == "complete"
    assert KEY not in json.dumps(complete) and "[redacted]" in json.dumps(complete)
    directory = analysis.jobs[access["run_id"]].directory
    assert all(KEY not in path.read_text() for path in directory.iterdir() if path.is_file())


def test_cancel_stops_current_request_drains_thread_and_resumes(client, monkeypatch, model):
    access = start(client)
    settled(client, access)
    original = model_client.call_text_async
    started, cancelled = Event(), Event()
    calls = []

    async def blocked(**arguments):
        calls.append(arguments["model"])
        if len(calls) == 1:
            return await original(**arguments)
        started.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    monkeypatch.setattr(model_client, "call_text_async", blocked)
    response = client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access, key=True))
    assert response.status_code == 202
    assert started.wait(2)
    duplicate = client.post("/api/item-analysis/runs", json={**BODY, "specification_mode": "generate"}, headers={"X-OpenAI-Key": KEY})
    assert duplicate.status_code == 202
    other = duplicate.json()
    assert settled(client, other)["status"] == "ready"
    assert client.post(url(other) + "/classify", json={"scope": "all"}, headers=headers(other, key=True)).status_code == 429
    stopped = client.post(url(access) + "/cancel", headers=headers(access)).json()
    assert stopped["status"] == "cancelled" and cancelled.is_set()
    assert stopped["completed_judgments"] == 6
    assert stopped["remaining_judgments"] == {"pilot": 54, "all": 54}
    assert analysis.jobs[access["run_id"]].task.done()
    assert calls == [model_client.MODEL_ID, model_client.MODEL_ID]
    monkeypatch.setattr(model_client, "call_text_async", original)
    assert classify(client, access)["status"] == "complete"
    ids = [payload["item"]["item_id"] for _, payload in model]
    assert len(ids) == len(set(ids)) == 10


def test_scoring_can_be_cancelled_and_sweep_never_removes_live_worker(client, monkeypatch):
    monkeypatch.setenv("ITEM_ANALYSIS_RETENTION_SECONDS", "3600")
    started, cancelled = Event(), Event()

    async def blocked(**arguments):
        started.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    monkeypatch.setattr(model_client, "call_text_async", blocked)
    access = start(client, mode="generate")
    assert settled(client, access)["status"] == "ready"
    assert client.post(url(access) + "/classify", json={"scope": "all"}, headers=headers(access, key=True)).status_code == 202
    assert started.wait(2)
    job = analysis.jobs[access["run_id"]]
    job.updated_at = time.time() - 3601
    analysis.sweep()
    assert job.directory.exists() and job.run_id in analysis.jobs
    response = client.post(url(access) + "/cancel", headers=headers(access)).json()
    assert response["status"] == "cancelled" and cancelled.is_set() and job.task.done()
    job.updated_at = time.time() - 3601
    analysis.sweep()
    assert not job.directory.exists() and job.run_id not in analysis.jobs


def test_configured_expiry_invalidates_secret_and_removes_all_files(client, monkeypatch):
    monkeypatch.setenv("ITEM_ANALYSIS_RETENTION_SECONDS", "3600")
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    job.updated_at = time.time() - 3601
    assert client.get(url(access), headers=headers(access)).status_code == 404
    assert not job.directory.exists()


def test_configured_missing_original_spec_still_prepares_fixed_context(client, tmp_path, monkeypatch):
    directory = prepared_snapshot(tmp_path, monkeypatch)
    (directory / "classifier_spec.original.json").unlink()
    entry = next(entry for entry in client.get("/api/item-analysis/catalog").json()["examples"] if entry["id"] == "mmlu")
    assert not entry["supplied_spec_available"]
    response = client.post("/api/item-analysis/runs", json={"example_id": "mmlu", "specification_mode": "provided"})
    assert response.status_code == 202
    assert settled(client, response.json())["status"] == "ready"
    access = start(client, example="mmlu", mode="generate")
    assert settled(client, access)["status"] == "ready"


def test_app_registers_router():
    from website.server.app import app
    assert any(route.path == "/api/item-analysis/catalog" for route in app.routes)


def test_cancellation_waits_for_async_provider_cleanup(client, monkeypatch):
    access = start(client)
    settled(client, access)
    started, cleaned = Event(), Event()

    async def blocked(**arguments):
        started.set()
        try:
            await asyncio.Event().wait()
        finally:
            await asyncio.sleep(.05)
            cleaned.set()

    monkeypatch.setattr(model_client, "call_text_async", blocked)
    assert client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access, key=True)).status_code == 202
    assert started.wait(2)
    response = client.post(url(access) + "/cancel", headers=headers(access))
    assert response.json()["status"] == "cancelled"
    assert cleaned.is_set(), "The async client's cleanup must finish before cancellation returns"
    job = analysis.jobs[access["run_id"]]
    assert job.task.done() and not job.provider_tasks


def test_partial_preparation_is_never_read_and_cancellation_drains_writer(client, monkeypatch, model):
    started, exited = Event(), Event()

    def slow_prepare(job, example_id):
        (job.directory / "items.jsonl").write_text('{"item_id": "partial', encoding="utf-8")
        started.set()
        assert job.stopped.wait(2)
        exited.set()
        raise InterruptedError("Preparation stopped")

    monkeypatch.setattr(analysis, "prepare_job", slow_prepare)
    access = start(client)
    assert started.wait(2)
    during = client.get(url(access), headers=headers(access))
    assert during.status_code == 200 and during.json()["items"] == []
    after = client.post(url(access) + "/cancel", headers=headers(access)).json()
    assert after["status"] == "cancelled" and after["items"] == []
    assert exited.is_set() and analysis.jobs[access["run_id"]].task.done()
    assert not model


def test_phase_waits_for_downloads_and_only_immutable_spec_downloads_while_running(client, monkeypatch):
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    job.downloads = 1
    response = client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access, key=True))
    assert response.status_code == 409
    job.downloads = 0
    started = Event()

    async def blocked(**arguments):
        started.set()
        await asyncio.Event().wait()

    monkeypatch.setattr(model_client, "call_text_async", blocked)
    assert client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access, key=True)).status_code == 202
    assert started.wait(2)
    assert client.get(url(access) + "/download/items", headers=headers(access)).status_code == 409
    assert client.get(url(access) + "/download/spec", headers=headers(access)).status_code == 200
    assert client.post(url(access) + "/cancel", headers=headers(access)).status_code == 200


def test_context_preparation_does_not_call_provider_even_when_provider_would_fail(client, monkeypatch):
    calls = []

    async def invalid(**arguments):
        calls.append(arguments)
        return model_client.CallResult("{}", "fixture", 1, 1, 1)

    monkeypatch.setattr(model_client, "call_text_async", invalid)
    access = start(client, mode="generate")
    ready = settled(client, access)
    assert ready["status"] == "ready" and ready["processed"] == 0 and not calls
    assert ready["summary"]["specification"]["source"]["kind"] == "deterministic"
    failed = classify(client, access)
    assert failed["status"] == "failed" and failed["errors"] == 10
    assert len(calls) == 20  # One primary request and one structural repair per item.


def test_prepared_source_is_never_modified_and_each_run_is_private(client, tmp_path, monkeypatch):
    source = prepared_snapshot(tmp_path, monkeypatch)
    before = {path.name: path.read_bytes() for path in source.iterdir() if path.is_file()}
    first, second = start(client, example="mmlu"), start(client, example="mmlu")
    assert settled(client, first)["status"] == settled(client, second)["status"] == "ready"
    assert before == {path.name: path.read_bytes() for path in source.iterdir() if path.is_file()}
    directories = [analysis.jobs[access["run_id"]].directory for access in (first, second)]
    assert directories[0] != directories[1]
    assert all(directory.stat().st_mode & 0o777 == 0o700 for directory in directories)
    assert client.get(url(first), headers=headers(second)).status_code == 404


@pytest.fixture
def current_assessment(client, tmp_path, monkeypatch):
    """A completed private run, with no opt-in log blobs or active secrets."""
    db.init_db()
    monkeypatch.setattr(pipeline_runner, "_WORKSPACE_ROOT", tmp_path / "tuples")
    scoring = deepcopy(read_json(analysis.FIXTURE_PATH)["assessment"])
    scoring["benchmark"] = "my-new-benchmark"
    scoring["dimensions"]["input_form"] = {
        "score": 2, "justification": "The current assessment requires Spanish classroom interaction.",
    }
    run_id = "existing-benchmark-run"
    logging_gate.start_run(run_id=run_id, started_at=datetime.now(timezone.utc), opted_in_full=False)
    pipeline_runner.write_tuple_inputs(
        run_id, scoring=scoring, composed_prompt="Current composed assessment",
        deployment_description="Spanish classrooms in the current user deployment.",
        elicitation_summary="Current elicitation requires Spanish explanations.",
        dataset_analysis_text="Current dataset review found English-only prompts.",
    )
    return {"assessment_kind": "run", "assessment_id": run_id, "benchmark_confirmed": "true"}


def start_linked(client, assessment, *, source_id=None, rows=None, filename="items.json"):
    fields = {**assessment, "benchmark_confirmed": "true",
              **({"source_id": source_id, "source_revision": CATALOG_REVISION} if source_id else {})}
    files = {"items_file": (filename, json.dumps(rows), "application/json")} if rows is not None else None
    response = client.post("/api/item-analysis/runs/from-assessment", data=fields, files=files,
                           headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 202, response.text
    return response.json()


def databank_catalog(monkeypatch, prepared=None, *, benchmark="mmlu", release="public"):
    """Pinned Data Bank-only fixture; the API tests never contact the network."""
    candidate = {
        "id": f"databank:{CATALOG_REVISION}:{benchmark}", "title": benchmark.upper(), "benchmark": benchmark,
        "item_count": read_json(prepared / "dataset.json")["item_count"] if prepared else 2,
        "available": True, "source_revision": CATALOG_REVISION, "revision": CATALOG_REVISION,
        "source_label": "Data Bank full item table", "repo": "aims-foundations/measurement-db-pp", "release": release,
        "source_url": f"https://huggingface.co/datasets/aims-foundations/measurement-db-pp/blob/{CATALOG_REVISION}/{benchmark}/items.parquet",
        "version": "test-v1", "split": "test", "match_reasons": ["Benchmark name matches"],
        "conflicts": [], "match_type": "exact_name", "requires_confirmation": True,
    }
    monkeypatch.setattr(analysis.item_analysis_databank, "search_candidates", lambda assessment, query=None: {
        "candidates": [deepcopy(candidate)], "status": "ready", "message": "Review and confirm the candidate.",
        "repo": candidate["repo"], "revision": CATALOG_REVISION, "requires_confirmation": True,
    })

    def resolve(candidate_id):
        if candidate_id != candidate["id"]:
            raise analysis.item_analysis_databank.DataBankError("The selected Data Bank snapshot is unavailable. Search and confirm again.")
        return deepcopy(candidate)

    def prepare_candidate(directory, selected, stopped=None):
        assert prepared is not None and selected["id"] == candidate["id"]
        assert stopped is not None and not stopped()
        for name in ("items.jsonl", "profile.json", "dataset.json"):
            shutil.copyfile(prepared / name, directory / name)
        return read_json(directory / "dataset.json")

    monkeypatch.setattr(analysis.item_analysis_databank, "resolve_candidate", resolve)
    monkeypatch.setattr(analysis.item_analysis_databank, "prepare_candidate", prepare_candidate)
    return candidate


def test_upload_continues_actual_assessment_without_matching_preset(client, current_assessment, model):
    context = client.get("/api/item-analysis/assessment", params={
        "kind": "run", "id": current_assessment["assessment_id"],
    })
    assert context.status_code == 200 and context.headers["cache-control"] == "no-store"
    assert context.json()["sources"] == []
    assert context.json()["upload"]["required_fields"] == ["content"]
    rows = [{"content": {"prompt": "¿Cuánto es 2 + 2?", "choices": ["3", "4"]}, "reference_answer": "4"},
            {"item_id": "custom-id", "content": "Explain your calculation.", "item_features": {"language": "es"}}]
    access = start_linked(client, current_assessment, rows=rows)
    ready = settled(client, access)
    assert ready["status"] == "ready", ready
    assert ready["assessment"]["id"] == current_assessment["assessment_id"]
    assert ready["assessment"]["benchmark"] == "my-new-benchmark"
    assert ready["spec"]["deployment"] == "Spanish classrooms in the current user deployment."
    assert ready["summary"]["specification"]["source"]["kind"] == "deterministic"
    assert ready["summary"]["original_assessment"]["input_form"]["score"] == 2
    assert {item["item_id"] for item in ready["items"]} == {"uploaded-1", "custom-id"}
    assert next(item for item in ready["items"] if item["item_id"] == "uploaded-1")["content"] == rows[0]["content"]
    assert not model
    payload = ready["spec"]
    assert payload["source_registry"]["elicitation_summary.md"] == "Current elicitation requires Spanish explanations."
    assert "dataset_analysis_report.md" not in payload["source_registry"]
    assert not any(key.startswith("scoring.json") for key in payload["source_registry"])
    directory = analysis.jobs[access["run_id"]].directory
    dataset = read_json(directory / "dataset.json")
    assert dataset["source"]["repo"] == "user-upload" and "path" not in dataset["source"]
    assert "assessment_dir" not in read_json(directory / "evidence.json")
    assert classify(client, access)["status"] == "complete"
    assert client.get(url(access)).status_code == 404
    with db.connect() as conn:
        conn.execute("DELETE FROM runs WHERE run_id = ?", (current_assessment["assessment_id"],))
    # Restoring an item run is authorized by its own secret and retains the
    # frozen assessment even after the original benchmark run is unavailable.
    restored = client.get(url(access), headers=headers(access))
    assert restored.status_code == 200 and restored.json()["assessment"] == ready["assessment"]
    assert all(KEY not in path.read_text() for path in directory.iterdir() if path.is_file())


def test_linked_snapshot_replaces_every_preset_context_without_model_calls(client, current_assessment, tmp_path, monkeypatch, model):
    source = prepared_snapshot(tmp_path, monkeypatch, count=2, benchmark="mmlu", assessment_context="old unrelated use case")
    before = {path.name: path.read_bytes() for path in source.iterdir() if path.is_file()}
    workspace = pipeline_runner._WORKSPACE_ROOT / current_assessment["assessment_id"]
    scoring = read_json(workspace / "scoring.json")
    scoring["benchmark"] = "mmlu"
    write_json(workspace / "scoring.json", scoring)
    candidate = databank_catalog(monkeypatch, source)
    access = start_linked(client, current_assessment, source_id=candidate["id"])
    # Later changes to the source assessment cannot change an in-flight run.
    scoring["dimensions"]["input_form"]["score"] = 5
    write_json(workspace / "scoring.json", scoring)
    ready = settled(client, access)
    assert ready["status"] == "ready", ready
    assert ready["summary"]["original_assessment"]["input_form"]["score"] == 2
    assert ready["example"]["deployment"] == ready["spec"]["deployment"] == "Spanish classrooms in the current user deployment."
    assert ready["summary"]["specification"]["source"]["kind"] == "deterministic"
    assert not model
    assert "old unrelated use case" not in json.dumps(ready["spec"])
    assert not any(key.startswith("scoring.json") for key in ready["spec"]["source_registry"])
    directory = analysis.jobs[access["run_id"]].directory
    assert not (directory / "provided_spec.json").exists()
    assert read_json(directory / "dataset.json")["source"]["sha256"] == read_json(source / "dataset.json")["source"]["sha256"]
    assert before == {path.name: path.read_bytes() for path in source.iterdir() if path.is_file()}


def test_linked_csv_upload_and_no_implicit_reference_answer(client, current_assessment):
    response = client.post("/api/item-analysis/runs/from-assessment", data=current_assessment,
                           files={"items_file": ("items.csv", "content,reference_answer\nQuestion 1,Answer 1\nQuestion 2,\n", "text/csv")},
                           headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 202, response.text
    ready = settled(client, response.json())
    assert ready["status"] == "ready" and ready["total"] == 2
    assert next(row for row in ready["items"] if row["item_id"] == "uploaded-2")["reference_answer"] == ""


def test_structured_csv_evidence_matches_equivalent_json_upload(client, current_assessment):
    rows = [{"item_id": "q1", "content": {"question": "Which answer?", "choices": ["A", "B"]},
             "reference_answer": {"correct": "B"}, "item_features": {"language": "es", "subject": "math"}}]
    json_access = start_linked(client, current_assessment, rows=rows)
    json_ready = settled(client, json_access)
    assert json_ready["status"] == "ready"
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerow({key: json.dumps(value) if isinstance(value, (dict, list)) else value
                     for key, value in rows[0].items()})
    response = client.post("/api/item-analysis/runs/from-assessment", data=current_assessment,
                           files={"items_file": ("items.csv", stream.getvalue(), "text/csv")},
                           headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 202, response.text
    csv_access = response.json()
    csv_ready = settled(client, csv_access)
    assert csv_ready["status"] == "ready"
    assert csv_ready["items"] == json_ready["items"]
    csv_profile = read_json(analysis.jobs[csv_access["run_id"]].directory / "profile.json")
    json_profile = read_json(analysis.jobs[json_access["run_id"]].directory / "profile.json")
    assert csv_profile == json_profile
    assert csv_profile["is_mcq"]
    assert csv_profile["item_feature_value_counts"]["language"] == [{"value": "es", "count": 1}]


@pytest.mark.parametrize("malformation", ["empty", "missing", "null", "list"])
def test_incomplete_benchmark_dimensions_rejected_before_model_calls(client, current_assessment, model, malformation):
    path = pipeline_runner._WORKSPACE_ROOT / current_assessment["assessment_id"] / "scoring.json"
    scoring = read_json(path)
    if malformation == "empty":
        scoring["dimensions"] = {}
    elif malformation == "missing":
        del scoring["dimensions"]["output_form"]
    else:
        scoring["dimensions"]["output_form"] = None if malformation == "null" else []
    write_json(path, scoring)
    response = client.get("/api/item-analysis/assessment", params={
        "kind": "run", "id": current_assessment["assessment_id"],
    })
    assert response.status_code == 409
    response = client.post("/api/item-analysis/runs/from-assessment", data=current_assessment,
                           files={"items_file": ("items.json", '[{"content": "Question"}]')},
                           headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 409
    assert not analysis.jobs and not model


@pytest.mark.parametrize("filename,payload", [
    ("items.json", '{"items": []}'),
    ("items.json", '[{"content": ""}]'),
    ("items.json", '[{"question": "missing content"}]'),
    ("items.json", '[{"item_id": "same", "content": "a"}, {"item_id": "same", "content": "b"}]'),
    ("items.json", '[{"content": NaN}]'),
    ("items.csv", 'content,content\na,b\n'),
    ("items.parquet", 'not parquet'),
])
def test_bad_linked_upload_rejected_before_any_model_calls(client, current_assessment, model, filename, payload):
    response = client.post("/api/item-analysis/runs/from-assessment", data=current_assessment,
                           files={"items_file": (filename, payload)}, headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 400, response.text
    assert not model and not analysis.jobs


def test_linked_inputs_credentials_and_size_checked_before_work(client, current_assessment, model, monkeypatch):
    endpoint = "/api/item-analysis/runs/from-assessment"
    files = {"items_file": ("items.json", '[{"content": "hello"}]')}
    assert client.post(endpoint, data=current_assessment, headers={"X-OpenAI-Key": KEY}).status_code == 400
    assert client.post(endpoint, data={**current_assessment, "source_id": "mmlu"},
                       headers={"X-OpenAI-Key": KEY}).status_code == 409
    assert client.post(endpoint, data={**current_assessment, "source_id": "mmlu"}, files=files,
                       headers={"X-OpenAI-Key": KEY}).status_code == 400
    assert client.post(endpoint, data={**current_assessment, "assessment_id": "../private"}, files=files,
                       headers={"X-OpenAI-Key": KEY}).status_code == 404
    monkeypatch.setattr(item_analysis_assessment, "MAX_UPLOAD_BYTES", 4)
    assert client.post(endpoint, data=current_assessment, files=files,
                       headers={"X-OpenAI-Key": KEY}).status_code == 400
    assert not analysis.jobs and not model


@pytest.mark.parametrize("confirmed", [None, "false"])
@pytest.mark.parametrize("dataset", ["source", "upload"])
def test_benchmark_confirmation_is_required_before_any_work(client, current_assessment, monkeypatch, model, confirmed, dataset):
    candidate = databank_catalog(monkeypatch)
    fields = {key: value for key, value in current_assessment.items() if key != "benchmark_confirmed"}
    if confirmed is not None:
        fields["benchmark_confirmed"] = confirmed
    files = None
    if dataset == "source":
        fields.update(source_id=candidate["id"], source_revision=CATALOG_REVISION)
    else:
        files = {"items_file": ("items.json", '[{"content":"Question"}]')}
    response = client.post("/api/item-analysis/runs/from-assessment", data=fields, files=files,
                           headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 400 and "Confirm" in response.json()["detail"]
    assert not analysis.jobs and not model


@pytest.mark.parametrize("selection", ["missing_revision", "wrong_revision", "old_revision_id", "private_preset", "arbitrary_url"])
def test_unbound_or_unlisted_source_selection_is_rejected(client, current_assessment, monkeypatch, model, selection):
    candidate = databank_catalog(monkeypatch)
    fields = {**current_assessment, "source_id": candidate["id"], "source_revision": CATALOG_REVISION}
    if selection == "missing_revision":
        del fields["source_revision"]
    elif selection == "wrong_revision":
        fields["source_revision"] = "b" * 40
    elif selection == "old_revision_id":
        fields["source_id"] = fields["source_id"].replace(CATALOG_REVISION, "b" * 40)
    elif selection == "private_preset":
        fields["source_id"] = "mmlu"
    else:
        fields["source_id"] = "https://huggingface.co/datasets/arbitrary/private/items.parquet"
    response = client.post("/api/item-analysis/runs/from-assessment", data=fields, headers={"X-OpenAI-Key": KEY})
    assert response.status_code == 409
    assert not analysis.jobs and not model


def test_catalog_search_keeps_assessment_pending_without_model_calls(client, current_assessment, monkeypatch, model):
    candidate = databank_catalog(monkeypatch)
    queries = []
    search = analysis.item_analysis_databank.search_candidates

    def capture(assessment, query=None):
        queries.append((assessment["benchmark"], query))
        return search(assessment, query)

    monkeypatch.setattr(analysis.item_analysis_databank, "search_candidates", capture)
    response = client.get("/api/item-analysis/sources", params={
        "kind": "run", "id": current_assessment["assessment_id"], "q": "MMLU alternative name",
    })
    assert response.status_code == 200 and response.headers["cache-control"] == "no-store"
    assert response.json()["sources"][0]["id"] == candidate["id"]
    assert response.json()["catalog"]["requires_confirmation"]
    assert queries == [("my-new-benchmark", "MMLU alternative name")]
    assert not analysis.jobs and not model


def test_identity_uses_persisted_benchmark_fields_and_never_deployment(client, current_assessment, monkeypatch):
    directory = pipeline_runner._WORKSPACE_ROOT / current_assessment["assessment_id"]
    (directory / "benchmark.yaml").write_text(
        "name: original-benchmark\nfull_name: Original Benchmark\npaper_url: https://arxiv.org/abs/1234.56789\n"
        "source_url: https://github.com/example/original\nyear: 2024\nlanguages: [en, es]\nversion: UNKNOWN\n"
        "source_urls: ['javascript:alert(1)', 'data:text/html,bad', 'https://user:secret@example.com/private']\n"
        "description: Another paper https://arxiv.org/abs/9999.99999 is only a reference.\n"
    )
    (directory / "metadata.txt").write_text("- version: v2\n- paper_url: https://example.com/less-specific\n")
    (directory / "deployment_description.txt").write_text("Evaluate unrelated French deployment-v9 at https://deployment.example/model.")
    response = client.get("/api/item-analysis/assessment", params={"kind": "run", "id": current_assessment["assessment_id"]})
    assert response.status_code == 200
    identity = response.json()["benchmark_identity"]
    assert identity == response.json()["assessment"]["benchmark_identity"]
    assert identity["name"] == "original-benchmark" and identity["full_name"] == "Original Benchmark"
    assert identity["paper_urls"] == ["https://arxiv.org/abs/1234.56789"]
    assert identity["source_urls"] == ["https://github.com/example/original"]
    assert identity["year"] == "2024" and identity["languages"] == ["en", "es"]
    assert identity["version"] == "v2" and "my-new-benchmark" in identity["aliases"]
    assert identity["evidence"]["paper_urls"] == "benchmark.yaml:paper_url"
    assert identity["evidence"]["version"] == "metadata:version"
    assert "deployment" not in json.dumps(identity) and "9999" not in json.dumps(identity)


def test_confirmed_databank_alias_preserves_source_and_original_assessment(client, current_assessment, tmp_path, monkeypatch):
    source = prepared_snapshot(tmp_path, monkeypatch, count=2, benchmark="mmlu")
    candidate = databank_catalog(monkeypatch, source)
    access = start_linked(client, current_assessment, source_id=candidate["id"])
    ready = settled(client, access)
    assert ready["status"] == "ready", ready
    assert ready["assessment"]["benchmark"] == ready["spec"]["benchmark"] == "my-new-benchmark"
    dataset = read_json(analysis.jobs[access["run_id"]].directory / "dataset.json")
    assert dataset["benchmark"] == "my-new-benchmark" and dataset["source_benchmark"] == "mmlu"
    assert dataset["benchmark_identity_confirmed"]
    assert read_json(analysis.jobs[access["run_id"]].directory / "profile.json")["benchmark_identity"]["requested"] == "mmlu"


@pytest.mark.parametrize("release", ["private", None])
def test_confirmed_eligible_source_is_not_filtered_by_release_flag(client, current_assessment, tmp_path, monkeypatch, model, release):
    prepared = prepared_snapshot(tmp_path, monkeypatch, count=2, benchmark="mmlu")
    candidate = databank_catalog(monkeypatch, prepared, release=release)
    setup = client.get("/api/item-analysis/assessment", params={"kind": "run", "id": current_assessment["assessment_id"]})
    assert setup.status_code == 200
    assert setup.json()["sources"][0]["release"] == release
    assert setup.json()["sources"][0]["available"]
    access = start_linked(client, current_assessment, source_id=candidate["id"])
    ready = settled(client, access)
    assert ready["status"] == "ready" and ready["total"] == 2, ready
    assert ready["example"]["release"] == release and not model
    assert ready["summary"]["original_assessment"]["input_form"]["score"] == 2


def test_unavailable_snapshot_fails_safely_before_paid_generation(client, current_assessment, monkeypatch, model):
    candidate = databank_catalog(monkeypatch)

    def unavailable(*args, **kwargs):
        raise analysis.item_analysis_databank.DataBankError("The confirmed snapshot could not be loaded. No model calls were made.")

    monkeypatch.setattr(analysis.item_analysis_databank, "prepare_candidate", unavailable)
    access = start_linked(client, current_assessment, source_id=candidate["id"])
    failed = settled(client, access)
    assert failed["status"] == "failed" and "No model calls" in failed["message"]
    assert not model


def test_linked_gallery_keeps_selected_deployment_with_databank_candidates(client, tmp_path, monkeypatch, model):
    from website.server import gallery

    root = tmp_path / "gallery"
    directory = root / "expert__toxigen" / "selected-context"
    directory.mkdir(parents=True)
    scoring = read_json(analysis.FIXTURE_PATH)["assessment"]
    scoring["benchmark"] = "toxigen"
    write_json(directory / "scoring.json", scoring)
    (directory / "deployment_description.txt").write_text("The selected gallery deployment.")
    (directory / "elicitation_summary.md").write_text("The selected gallery elicitation.")
    monkeypatch.setattr(gallery, "_ASSESSMENTS_ROOT", root)
    gallery.list_entries.cache_clear()
    try:
        candidate = databank_catalog(monkeypatch, benchmark="toxigen")
        response = client.get("/api/item-analysis/assessment", params={"kind": "gallery", "id": "expert__toxigen"})
        assert response.status_code == 200
        context = response.json()
        assert context["assessment"]["deployment"] == "The selected gallery deployment."
        assert [source["id"] for source in context["sources"]] == [candidate["id"]]
        assert context["catalog"]["requires_confirmation"]
        assert "suggested_source_id" not in context
        assert all("deployment" not in source and "assessment_title" not in source for source in context["sources"])
        access = start_linked(client, {"assessment_kind": "gallery", "assessment_id": "expert__toxigen"}, rows=[{"content": "Example text"}])
        ready = settled(client, access)
        assert ready["status"] == "ready"
        assert ready["spec"]["deployment"] == "The selected gallery deployment."
        assert ready["assessment"]["kind"] == "gallery"
        assert client.get("/api/item-analysis/assessment", params={"kind": "gallery", "id": "../private"}).status_code == 404
    finally:
        gallery.list_entries.cache_clear()


def test_completed_no_optin_report_and_item_context_survive_active_run_cleanup(client, current_assessment):
    from website.server import app as app_module

    original = app_module.get_report(current_assessment["assessment_id"])
    assert original["scoring"]["benchmark"] == "my-new-benchmark"
    assert original["deployment_description"] == "Spanish classrooms in the current user deployment."
    assert original["elicitation_summary"] == "Current elicitation requires Spanish explanations."
    with db.connect() as conn:
        assert not conn.execute("SELECT 1 FROM steps WHERE blob_key IS NOT NULL").fetchone()


@pytest.mark.parametrize("running", [False, True])
def test_deleting_benchmark_run_also_deletes_its_linked_item_data(client, current_assessment, monkeypatch, running):
    from website.server import app as app_module

    client.app.add_api_route("/api/runs/{run_id}", app_module.delete_run, methods=["DELETE"])
    access = start_linked(client, current_assessment, rows=[{"content": "Question"}])
    assert settled(client, access)["status"] == "ready"
    directory = analysis.jobs[access["run_id"]].directory
    started, stopped = Event(), Event()
    if running:
        async def blocked(**arguments):
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                stopped.set()

        monkeypatch.setattr(model_client, "call_text_async", blocked)
        assert client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access, key=True)).status_code == 202
        assert started.wait(2)
    response = client.delete(f"/api/runs/{current_assessment['assessment_id']}")
    assert response.status_code == 204
    assert not directory.exists()
    assert access["run_id"] not in analysis.jobs
    assert client.get(url(access), headers=headers(access)).status_code == 404
    if running:
        assert stopped.is_set()


@pytest.mark.parametrize("code", ["invalid_json", "schema", "evidence", "deployment"])
def test_context_preparation_failure_is_safe_and_makes_no_model_calls(client, monkeypatch, model, code):
    private_marker = "PRIVATE-CONTEXT-MUST-NOT-APPEAR"

    def invalid_context(*args, **kwargs):
        raise ValueError(f"{code}: {private_marker} {KEY}")

    monkeypatch.setattr(analysis.scoring, "prepare_context", invalid_context)
    access = start(client, mode="generate")
    failed = settled(client, access)
    assert failed["status"] == "failed" and failed["provider_error"] is None
    assert failed["failure"]["stage"] == "specification"
    assert failed["failure"]["code"] == "specification_failed"
    assert failed["processed"] == 0 and failed["spec"] is None and not model
    assert private_marker not in json.dumps(failed) and KEY not in json.dumps(failed)
    assert not (analysis.jobs[access["run_id"]].directory / "results.jsonl").exists()


@pytest.mark.parametrize("phase", ["preparation", "specification", "report"])
def test_unexpected_initialization_failure_identifies_phase_without_exposing_exception(
        client, current_assessment, monkeypatch, model, phase):
    private_marker = "PRIVATE-SERVER-EXCEPTION-MUST-NOT-APPEAR"

    def fail(*args, **kwargs):
        raise RuntimeError(f"{private_marker} {KEY} /private/server/path")

    if phase == "preparation":
        monkeypatch.setattr(analysis, "prepare_assessment_job", fail)
    elif phase == "specification":
        monkeypatch.setattr(analysis.scoring, "prepare_context", fail)
    else:
        monkeypatch.setattr(analysis.report, "generate_report", fail)
    access = start_linked(client, current_assessment, rows=[{"content": "Explain 2+2.", "reference_answer": "4"}])
    failed = settled(client, access)
    assert failed["status"] == "failed" and failed["provider_error"] is None
    assert failed["failure"] == {"stage": phase, "code": f"{phase}_failed", "message": failed["message"]}
    assert failed["error"] == failed["message"] and failed["processed"] == 0
    assert private_marker not in json.dumps(failed) and KEY not in json.dumps(failed)
    assert "/private/server/path" not in json.dumps(failed)
    assert "Check the example, model access, and API key" not in failed["message"]
    if phase == "report":
        assert failed["spec"] is not None and failed["summary"] is None
        assert "scoring context is ready" in failed["message"] and not model
        assert all("item" not in payload for _, payload in model)
    else:
        assert not model and failed["spec"] is None
        if phase == "preparation":
            assert "No model calls were made" in failed["message"]
    assert not (analysis.jobs[access["run_id"]].directory / "results.jsonl").exists()


def test_initialization_failure_is_cleared_before_a_later_classification_failure(client, monkeypatch):
    original_report = analysis.report.generate_report

    def broken_report(*args, **kwargs):
        raise RuntimeError("Temporary local report failure")

    monkeypatch.setattr(analysis.report, "generate_report", broken_report)
    access = start(client)
    initial = settled(client, access)
    assert initial["failure"]["code"] == "report_failed" and initial["spec"] is not None
    monkeypatch.setattr(analysis.report, "generate_report", original_report)

    async def rejected(**arguments):
        raise model_client.ModelRequestError(code="authentication", status_code=401)

    monkeypatch.setattr(model_client, "call_text_async", rejected)
    failed = classify(client, access)
    assert failed["status"] == "failed" and failed["provider_error"]["code"] == "authentication"
    assert failed["failure"] is None
    assert "results view" not in failed["message"]


def test_fixed_six_dimension_rubric_reaches_each_item_and_counts_judgments(client, model):
    access = start(client)
    ready = settled(client, access)
    assert ready["spec"]["schema_version"] == "caliper_item_context_v1"
    assert ready["spec"]["rubric_version"] == "caliper_item_rubric_v1"
    assert ready["spec"]["classifiers"] == dimension_descriptors()
    assert ready["summary"]["specification"]["semantic_validation"] == "unreviewed"
    assert isinstance(ready["spec"]["dataset_profile"], dict)
    assert client.get(url(access) + "/download/review", headers=headers(access)).status_code == 404
    result = classify(client, access)
    assert len(model) == result["complete"]
    for _, payload in model:
        assert payload["classifiers"] == dimension_descriptors()
        assert set(payload["output_schema"]["properties"]["dimensions"]["properties"]) == set(DIMENSIONS)
        assert payload["source_registry"] == ready["spec"]["source_registry"]
        assert not any(key.startswith("scoring.json") for key in payload["source_registry"])
    experiment = result["summary"]["experiment"]
    assert experiment["completed_item_classifier_judgments"] == result["complete"] * 6
    assert experiment["selected_items"] == result["total"]
    content = next(c for c in result["summary"]["classifiers"] if c["id"] == "input_content")
    assert content["unknown"] == 1 and content["known"] == 9


def test_browser_demo_catalog_is_identical_to_code_owned_rules():
    from anthropic_api_package_release.item_analysis.catalog import get_catalog, CATALOG_VERSION

    bundled = read_json(Path(__file__).parents[2] / 'client/src/demo/genericItemCatalog.json')
    assert bundled['version'] == CATALOG_VERSION
    assert bundled['classifiers'] == get_catalog()


def test_linked_run_freezes_available_source_contents_and_keeps_secrets_out(client, current_assessment, monkeypatch):
    from types import SimpleNamespace

    artifacts = {
        'paper_summary': 'Actual paper documentation: responses are scored for correctness and explanation.',
        'region_yaml': 'target_standard: explain reasoning clearly',
        'scaffold_yaml': 'stakeholder_disagreement: unresolved',
        'elicitation_answers': [{'id': 'Q1', 'answer': 'Arithmetic explanations are required.'}],
        'elicitation_questions': [{'id': 'Q1', 'question': 'Which tasks are required?'}],
        'private_internal_value': KEY,
    }
    active = SimpleNamespace(artifacts=artifacts, deployment_description='', api_key=KEY)
    monkeypatch.setattr(item_analysis_assessment.active_runs.store, 'get', lambda _run_id: active)
    access = start_linked(client, current_assessment, rows=[{'content': 'Explain 2+2.'}])
    state = settled(client, access)
    assert state['status'] == 'ready', state
    sources = state['spec']['source_registry']
    assert sources['paper_summary.md'] == artifacts['paper_summary']
    assert sources['region.yaml'] == artifacts['region_yaml']
    assert sources['region_scaffold.yaml'] == artifacts['scaffold_yaml']
    assert json.loads(sources['elicitation_answers.json']) == artifacts['elicitation_answers']
    assert state['spec']['source_roles']['elicitation_answers.json'] == 'deployment_requirement'
    assert isinstance(state['spec']['dataset_profile'], dict)
    assert not any(key.startswith('items.jsonl#/') for key in sources)
    assert json.loads(sources['elicitation_questions.json']) == artifacts['elicitation_questions']
    assert state['spec']['source_roles']['elicitation_questions.json'] == 'elicitation_question'
    assert KEY not in json.dumps(state)


def test_missing_assessment_documents_remain_gaps_not_fabricated_sources(client, current_assessment):
    workspace = pipeline_runner._WORKSPACE_ROOT / current_assessment['assessment_id']
    (workspace / 'elicitation_summary.md').unlink()
    (workspace / 'dataset_analysis_report.md').unlink()
    access = start_linked(client, current_assessment, rows=[{'content': 'Explain 2+2.'}])
    state = settled(client, access)
    assert state['status'] == 'ready', state
    sources = state['spec']['source_registry']
    assert 'elicitation_summary.md' not in sources
    assert 'dataset_analysis_report.md' not in sources
    assert any('no available elicitation_summary.md contents' in gap for gap in state['spec']['evidence_gaps'])
    assert any('no available dataset_analysis_report.md contents' in gap for gap in state['spec']['evidence_gaps'])
