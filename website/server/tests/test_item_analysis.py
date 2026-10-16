"""The website exercises the real item-analysis pipeline without paid calls."""

import asyncio
from contextlib import asynccontextmanager
from copy import deepcopy
import csv
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import shutil
from threading import Event
import time

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from anthropic_api_package_release.item_analysis import model_client, prepare
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


@pytest.fixture
def model(monkeypatch):
    calls = []

    async def fake_call(**arguments):
        assert arguments["api_key"] == KEY
        payload = json.loads(arguments["user"])
        calls.append((arguments["model"], payload))
        assert arguments["model"] == model_client.MODEL_ID
        assert arguments["reasoning_effort"] == model_client.REASONING_EFFORT
        if "item" not in payload:
            spec = read_json(analysis.FIXTURE_PATH)["classifier_spec"]
            spec["benchmark"], spec["deployment"] = payload["benchmark"], payload["deployment"]
            if payload.get("analysis_basis") == "deployment_requirements":
                for classifier in spec["classifiers"]:
                    classifier["grounded_in"] = ["direct_context.json#/task_requirements", "deployment_description.txt"]
            text = json.dumps(spec)
        else:
            slots = payload["output_schema"]["properties"]["labels"]["properties"]
            labels = {slot: {"label": definition["properties"]["label"]["enum"][0],
                             "evidence": ["The supplied question and answer choices."],
                             "justification": "Deterministic test response, not a genuine assessment."}
                      for slot, definition in slots.items()}
            if payload["item"]["item_id"].endswith("01"):
                labels["IC.region_fit"]["label"] = None
            text = json.dumps({"labels": labels})
        return model_client.CallResult(text, arguments["model"], 100, 30, 1,
                                      cached_input_tokens=20, reasoning_tokens=7)

    monkeypatch.setattr(model_client, "call_text_async", fake_call)
    return calls


@pytest.fixture
def client(tmp_path, monkeypatch, model):
    monkeypatch.setattr(db, "DEFAULT_DB_PATH", tmp_path / "data/runs.db")
    monkeypatch.setattr(analysis, "jobs", {})
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
        fixture["classifier_spec"]["deployment"] = fixture["deployment"]
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
    assert calls == [(directory, "mmlu")]
    assert "path" not in read_json(directory / "dataset.json")["source"]
    assert "assessment_dir" not in read_json(directory / "evidence.json")


@pytest.mark.parametrize("example_id,benchmark,assessment_context", REMOTE_CONTEXTS)
def test_selected_context_drives_generation_classification_and_exports(
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
    assert ready["summary"]["specification"]["source"]["kind"] == "generated"
    directory = analysis.jobs[access["run_id"]].directory
    assert calls == [(directory, example_id)]
    generation = [payload for _, payload in model if "item" not in payload]
    assert len(generation) == 1
    assert generation[0]["benchmark"] == benchmark
    assert generation[0]["deployment"] == evidence["deployment"]
    assert generation[0]["evidence_registry"] == evidence["registry"]
    assert {item["item_id"]: item for item in generation[0]["example_items"]} == expected_items

    result = classify(client, access)
    assert result["status"] == "complete", result
    assert result["complete"] == result["processed"] == result["total"] == 3
    classification = [payload for _, payload in model if "item" in payload]
    assert len(classification) == 3
    assert {payload["item"]["item_id"]: payload["item"] for payload in classification} == expected_items
    assert all(payload["deployment"] == payload["contextualized_deployment"] == evidence["deployment"]
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
def test_remote_benchmark_without_supplied_criteria_requires_generation(client, monkeypatch, model, example_id):
    calls = remote_source(monkeypatch)
    entry = next(entry for entry in client.get("/api/item-analysis/catalog").json()["examples"]
                 if entry["id"] == example_id)
    assert entry["available"] and not entry["supplied_spec_available"]
    response = client.post("/api/item-analysis/runs", json={"example_id": example_id, "specification_mode": "provided"})
    assert response.status_code == 409
    assert not analysis.jobs and not calls and not model
    assert not (db.DEFAULT_DB_PATH.parent / "item-analysis").exists()


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
    assert "Illustrative" in job["example"]["source_label"]
    assert job["summary"]["original_assessment"]["input_form"]["score"] is None
    assert job["summary"]["specification"]["source"]["kind"] == "provided"
    assert not model
    assert not next(c for c in job["spec"]["classifiers"] if c["id"] == "OO.output_category")["applicable"]


@pytest.mark.parametrize("mode", ["provided", "generate"])
def test_real_pipeline_generates_or_imports_then_classifies_and_exports(client, model, mode):
    access = start(client, mode=mode)
    ready = settled(client, access)
    assert ready["status"] == "ready"
    expected_model = {"provider": "openai", "model_id": "gpt-6-luna", "reasoning_effort": "low"}
    assert ready["model"] == access["model"] == expected_model
    assert ready["summary"]["specification"]["source"]["kind"] == ("generated" if mode == "generate" else "provided")
    if mode == "generate":
        source = ready["summary"]["specification"]["source"]
        assert {key: source[key] for key in expected_model} == expected_model
    result = classify(client, access)
    assert result["status"] == "complete"
    assert result["complete"] == result["processed"] == result["total"] == 10
    assert result["errors"] == 0 and result["summary"]["complete_snapshot"]
    regional = next(c for c in result["summary"]["classifiers"] if c["id"] == "IC.region_fit")
    assert regional["unknown"] == 1 and regional["known"] == 9
    call_count = 11 if mode == "generate" else 10
    assert result["usage"] == {"input_tokens": 100 * call_count, "output_tokens": 30 * call_count,
                               "cached_input_tokens": 20 * call_count, "reasoning_tokens": 7 * call_count}
    assert sum("item" not in payload for _, payload in model) == (mode == "generate")
    for artifact, (filename, _) in analysis.ARTIFACTS.items():
        response = client.get(url(access) + f"/download/{artifact}", headers=headers(access))
        assert response.status_code == 200
        assert filename in response.headers["content-disposition"]
        assert KEY not in response.text
    worksheet = client.get(url(access) + "/download/review", headers=headers(access)).text
    assert "justification" not in worksheet and "Deterministic test" not in worksheet
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
    assert client.post(url(access) + "/classify", json={"scope": "all"}, headers=headers(access, key=True)).status_code == 409
    pilot = classify(client, access)
    assert pilot["status"] == "checkpoint" and pilot["can_continue"]
    assert (pilot["processed"], pilot["total"]) == (100, 105)
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
    assert client.post("/api/item-analysis/runs", json={**BODY, "specification_mode": "generate"}).status_code == 401
    wrong_header = client.post("/api/item-analysis/runs", json={**BODY, "specification_mode": "generate"},
                               headers={"X-Anthropic-Key": KEY})
    assert wrong_header.status_code == 401
    assert "OpenAI" in wrong_header.json()["detail"]
    assert not analysis.jobs and not model
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


@pytest.mark.parametrize("mode", ["generate", "provided"])
@pytest.mark.parametrize("code,status_code,parameter", [
    ("authentication", 401, None),
    ("model_unavailable", 404, "model"),
    ("permission", 403, None),
    ("quota", 429, None),
    ("rate_limit", 429, None),
    ("invalid_request", 400, "reasoning.effort"),
])
def test_safe_provider_diagnostics_reach_generation_and_classification(
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
    failed = classify(client, access) if mode == "provided" else state
    assert failed["status"] == "failed"
    assert failed["message"] == failed["error"] == error.public_message
    assert failed["provider_error"] == {
        "code": code, "status_code": status_code, "message": error.public_message,
    }
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
        for label in payload["labels"].values():
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
    assert duplicate.status_code == 429
    stopped = client.post(url(access) + "/cancel", headers=headers(access)).json()
    assert stopped["status"] == "cancelled" and cancelled.is_set()
    assert analysis.jobs[access["run_id"]].task.done()
    assert calls == [model_client.MODEL_ID]
    monkeypatch.setattr(model_client, "call_text_async", original)
    assert classify(client, access)["status"] == "complete"


def test_generation_can_be_cancelled_and_sweep_never_removes_live_worker(client, monkeypatch):
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
    assert started.wait(2)
    job = analysis.jobs[access["run_id"]]
    job.updated_at = time.monotonic() - analysis.RETENTION_SECONDS - 1
    analysis.sweep()
    assert job.directory.exists() and job.run_id in analysis.jobs
    response = client.post(url(access) + "/cancel", headers=headers(access)).json()
    assert response["status"] == "cancelled" and cancelled.is_set() and job.task.done()
    job.updated_at = time.monotonic() - analysis.RETENTION_SECONDS - 1
    analysis.sweep()
    assert not job.directory.exists() and job.run_id not in analysis.jobs


def test_expiry_invalidates_secret_and_removes_all_files(client):
    access = start(client)
    settled(client, access)
    job = analysis.jobs[access["run_id"]]
    job.updated_at = time.monotonic() - analysis.RETENTION_SECONDS - 1
    assert client.get(url(access), headers=headers(access)).status_code == 404
    assert not job.directory.exists()


def test_configured_missing_original_spec_allows_generation_only(client, tmp_path, monkeypatch):
    directory = prepared_snapshot(tmp_path, monkeypatch)
    (directory / "classifier_spec.original.json").unlink()
    entry = next(entry for entry in client.get("/api/item-analysis/catalog").json()["examples"] if entry["id"] == "mmlu")
    assert not entry["supplied_spec_available"]
    response = client.post("/api/item-analysis/runs", json={"example_id": "mmlu", "specification_mode": "provided"})
    assert response.status_code == 409 and not analysis.jobs
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


def test_invalid_generated_spec_repairs_once_then_fails_without_classifying(client, monkeypatch):
    calls = []

    async def invalid(**arguments):
        calls.append(arguments["model"])
        return model_client.CallResult("{}", "fixture", 1, 1, 1)

    monkeypatch.setattr(model_client, "call_text_async", invalid)
    access = start(client, mode="generate")
    job = settled(client, access)
    assert job["status"] == "failed" and job["processed"] == 0
    assert calls == [model_client.MODEL_ID, model_client.MODEL_ID]
    assert client.post(url(access) + "/classify", json={"scope": "pilot"}, headers=headers(access, key=True)).status_code == 409


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
    assert ready["summary"]["specification"]["source"]["kind"] == "generated"
    assert ready["summary"]["original_assessment"]["input_form"]["score"] == 2
    assert {item["item_id"] for item in ready["items"]} == {"uploaded-1", "custom-id"}
    assert next(item for item in ready["items"] if item["item_id"] == "uploaded-1")["content"] == rows[0]["content"]
    payload = model[0][1]
    assert payload["evidence_registry"]["elicitation_summary.md"] == "Current elicitation requires Spanish explanations."
    assert payload["evidence_registry"]["dataset_analysis_report.md"] == "Current dataset review found English-only prompts."
    assert payload["evidence_registry"]["scoring.json#/dimensions/input_form/score"] == 2
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


def test_linked_snapshot_replaces_every_preset_context_and_always_generates(client, current_assessment, tmp_path, monkeypatch, model):
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
    assert ready["summary"]["specification"]["source"]["kind"] == "generated"
    assert len(model) == 1
    assert "old unrelated use case" not in json.dumps(model[0][1])
    assert model[0][1]["evidence_registry"]["scoring.json#/dimensions/input_form/score"] == 2
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
    assert client.post(endpoint, data=current_assessment, files=files).status_code == 401
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
    assert ready["example"]["release"] == release and len(model) == 1
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
