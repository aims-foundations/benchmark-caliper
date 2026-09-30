"""The website exercises the real item-analysis pipeline without paid calls."""

import asyncio
from contextlib import asynccontextmanager
from copy import deepcopy
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
from website.server import db, item_analysis as analysis

KEY = "sk-test-private-item-analysis-key"
BODY = {"example_id": "illustrative", "specification_mode": "provided"}


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


def prepared_snapshot(tmp_path, monkeypatch, count=105):
    """Make a small local snapshot using the shared production preparation step."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    fixture = read_json(analysis.FIXTURE_PATH)
    source, output = tmp_path / "source", tmp_path / "prepared"
    source.mkdir()
    write_json(source / "scoring.json", fixture["assessment"])
    for filename, key in (("deployment_description.txt", "deployment"),
                          ("elicitation_summary.md", "elicitation_summary"),
                          ("dataset_analysis_report.md", "dataset_analysis_report")):
        (source / filename).write_text(fixture[key], encoding="utf-8")
    rows = [dict(deepcopy(fixture["items"][i % len(fixture["items"])]), item_id=f"test-{i:04d}") for i in range(count)]
    pq.write_table(pa.Table.from_pylist(rows), source / "items.parquet")
    prepare.prepare(source, source / "items.parquet", output, source_repo="test-only", source_revision="fixture")
    write_json(output / "classifier_spec.original.json", fixture["classifier_spec"])
    monkeypatch.setenv("ITEM_ANALYSIS_PREPARED_DIR", str(output))
    return output


def remote_source(monkeypatch, prepared=None, *, available=True):
    """Exercise the HTTP adapter's remote branch without contacting Hugging Face."""
    monkeypatch.delenv("ITEM_ANALYSIS_PREPARED_DIR", raising=False)
    entry = {
        "id": "mmlu", "title": "MMLU", "description": "Pinned Hugging Face snapshot.",
        "benchmark": "mmlu", "deployment": "The catalog deployment.",
        "source_label": "measurement-db-pp MMLU", "item_count": 14015,
        "available": available, "supplied_spec_available": True,
        "source_url": "https://huggingface.co/datasets/aims-foundations/measurement-db-pp/tree/main/mmlu",
        "source_revision": "advertised-revision",
    }
    if not available:
        entry["unavailable_reason"] = "The MMLU dataset is unavailable on this server."
    monkeypatch.setattr(analysis.item_analysis_source, "source_entry", lambda: deepcopy(entry))
    calls = []

    def prepare_remote(directory, stopped=None):
        assert stopped is not None and not stopped()
        assert prepared is not None, "This test must not prepare or download a dataset"
        calls.append(directory)
        for name in analysis.PREPARED_FILES:
            shutil.copyfile(prepared / name, directory / name)
        supplied = directory / "provided_spec.json"
        shutil.copyfile(prepared / "classifier_spec.original.json", supplied)
        return supplied

    monkeypatch.setattr(analysis.item_analysis_source, "prepare_source", prepare_remote)
    return calls


def test_default_catalog_puts_real_mmlu_before_illustrative_example(client, monkeypatch):
    calls = remote_source(monkeypatch)
    catalog = client.get("/api/item-analysis/catalog").json()
    assert [entry["id"] for entry in catalog["examples"]] == ["mmlu", "illustrative"]
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
    assert calls == [directory]
    assert "path" not in read_json(directory / "dataset.json")["source"]
    assert "assessment_dir" not in read_json(directory / "evidence.json")


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
    directory = analysis.jobs[access["run_id"]].directory
    assert all(KEY not in path.read_text() for path in directory.iterdir() if path.is_file())
    monkeypatch.setattr(model_client, "call_text_async", original)
    finished = classify(client, access)
    assert finished["status"] == "complete" and finished["errors"] == 0


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
