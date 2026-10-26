"""Offline checks for isolated classifier requests and durable continuation."""

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from item_analysis.classify import classification_request, read_results, run
from item_analysis.generate import generate_spec
from item_analysis.prepare import prepare
from item_analysis.report import generate_report
from item_analysis.storage import parse_response, read_json, run_lock

FIXTURE = Path(__file__).parent / "fixtures" / "item_analysis_generic_context.json"
CLASSIFIER_IDS = ("input_ontology", "input_content", "output_ontology", "output_content")


def request_payload(request):
    return json.loads(request["user"].split("\n\nPrevious response:", 1)[0])


@pytest.fixture
def prepared(tmp_path):
    source = tmp_path / "source.parquet"
    pq.write_table(pa.Table.from_pylist([
        {"item_id": str(i), "content": f"Question {i}\nA. yes\nB. no", "reference_answer": "A"}
        for i in range(5)
    ]), source)
    assessment = tmp_path / "assessment"
    assessment.mkdir()
    (assessment / "scoring.json").write_text(json.dumps({"benchmark": "mmlu", "dimensions": {}}))
    for name in ("deployment_description.txt", "elicitation_summary.md", "dataset_analysis_report.md"):
        (assessment / name).write_text("Hindi-medium exam preparation with mathematics tasks.")
    directory = tmp_path / "run"
    prepare(assessment, source, directory)
    generate_spec(directory, supplied=FIXTURE)
    return directory


class Judge:
    def __init__(self, directory, responses=None):
        self.spec = read_json(directory / "classifier_spec.json")
        self.calls = []
        self.responses = list(responses or [])

    def __call__(self, **request):
        self.calls.append(request)
        if self.responses:
            response = self.responses.pop(0)
            if isinstance(response, Exception):
                raise response
            return response
        return self.response(request_payload(request)["classifier"]["id"])

    def response(self, classifier_id, *, insufficient=False):
        label = "match" if classifier_id == "input_ontology" else "no_issue_identified"
        judgment = {
            "label": "insufficient_evidence" if insufficient else label,
            "evidence": ["content: Question"],
            "justification": ("Required comparison evidence is missing." if insufficient else
                              "Fixture evidence supports this label."),
        }
        if classifier_id == "input_ontology":
            judgment["matched_category_ids"] = ([] if insufficient else [
                self.spec["input_category_inventory"]["categories"][0]["id"]
            ])
            judgment["scope_exclusion_source_ids"] = []
        return json.dumps({"labels": {classifier_id: judgment}})


def test_checkpoint_continues_to_all_without_repeating_completed_items(prepared):
    judge = Judge(prepared)
    first = run(prepared, limit=2, call=judge, model_id="test-model")
    assert first["complete"] == 2 and not first["full_dataset_complete"]
    first_ids = set(read_results(prepared / "results.jsonl"))
    final = run(prepared, limit=None, resume=True, call=judge, model_id="test-model")
    assert final["complete"] == 5 and final["full_dataset_complete"]
    assert final["attempted_this_invocation"] == 3
    assert len(judge.calls) == 20
    assert first["target_item_classifier_judgments"] == 2 * len(judge.spec["classifiers"])
    assert final["completed_item_classifier_judgments"] == 5 * len(judge.spec["classifiers"])
    assert final["request_calls_this_invocation"] == 12
    assert set(final["selected_item_ids"]) == set(read_results(prepared / "results.jsonl"))
    called_ids = [request_payload(request)["item"]["item_id"] for request in judge.calls]
    assert len(set(called_ids)) == 5
    assert set(called_ids[:8]) == first_ids
    assert set(Counter(called_ids).values()) == {4}
    assert all(sum(request_payload(request)["classifier"]["id"] == cid
                   for request in judge.calls) == 5 for cid in CLASSIFIER_IDS)
    assert all(request["model"] == "test-model" for request in judge.calls)
    assert all(request["reasoning_effort"] == "low" for request in judge.calls)
    summary = generate_report(prepared)
    assert summary["complete_snapshot"]
    assert {key: summary["classification"][key]
            for key in ("provider", "model_id", "reasoning_effort", "max_tokens")} == {
        "provider": "openai", "model_id": "test-model", "reasoning_effort": "low", "max_tokens": 4096,
    }
    assert summary["classification"]["request_mode"] == "per_classifier"
    assert "test-model" in (prepared / "report.html").read_text()
    assert (prepared / "report.html").exists()
    config = read_json(prepared / "run.json")
    assert config["version"] == 4 and config["request_mode"] == "per_classifier"
    assert set(config["prompts"]) == set(config["prompt_sha256"]) == set(CLASSIFIER_IDS)
    assert set(config["output_schemas"]) == set(CLASSIFIER_IDS)


def test_dry_run_saves_complete_requests_without_results_or_api_calls(prepared):
    judge = Judge(prepared)
    state = run(prepared, dry_run=True, limit=2, call=judge)
    assert state["model_calls"] == 0 and not judge.calls
    assert not (prepared / "run.json").exists()
    assert not (prepared / "results.jsonl").exists()
    previews = [json.loads(line) for line in (prepared / "preview_requests.jsonl").read_text().splitlines()]
    assert len(previews) == state["primary_requests"] == 8
    for preview in previews:
        payload = request_payload(preview["request"])
        cid = preview["classifier_id"]
        assert payload["item"]["reference_answer"] == "A"
        assert payload["classifier"] == next(c for c in judge.spec["classifiers"] if c["id"] == cid)
        assert "classifiers" not in payload and "context_by_classifier" not in payload
        assert payload["context"] == judge.spec["context_by_classifier"][cid]
        assert payload["output_schema"]["properties"]["labels"]["required"] == [cid]
        assert set(payload["output_schema"]["properties"]["labels"]["properties"]) == {cid}
        assert payload["source_registry"] == {
            key: value for key, value in judge.spec["source_registry"].items()
            if judge.spec["source_roles"][key] == "deployment_requirement"
        }
        assert ("input_category_inventory" in payload) == (cid == "input_ontology")
        assert preview["request"]["step"] == f"item_classification.{cid}"
    assert len({preview["request"]["system"] for preview in previews}) == 4


@pytest.mark.parametrize("classifier_id", CLASSIFIER_IDS)
def test_request_uses_only_its_dimension_context_and_relevant_sources(prepared, classifier_id):
    spec = read_json(prepared / "classifier_spec.json")
    for cid in CLASSIFIER_IDS:
        source_id = f"{cid}_standard.md"
        spec["source_registry"][source_id] = f"Documented standard for {cid}."
        spec["source_roles"][source_id] = "benchmark_evidence"
        spec["context_by_classifier"][cid]["benchmark_evidence"].append({
            "statement": f"The documented {cid} comparison.", "source_ids": [source_id],
        })
    # Scope boundaries may remain in the original deployment evidence even if
    # the context generator did not extract them into a statement.
    spec["source_registry"]["scope.md"] = "Only mathematics exam preparation is in scope."
    spec["source_roles"]["scope.md"] = "deployment_requirement"
    item = {"item_id": "example", "content": "Question", "reference_answer": "A"}
    original = deepcopy(spec)
    request = classification_request(item, spec, spec["deployment"], classifier_id)
    payload = request_payload(request)
    assert spec == original  # Filtering does not mutate the frozen specification.
    assert payload["classifier"] == next(c for c in spec["classifiers"] if c["id"] == classifier_id)
    assert payload["context"] == spec["context_by_classifier"][classifier_id]
    assert payload["source_registry"][f"{classifier_id}_standard.md"] == f"Documented standard for {classifier_id}."
    assert payload["source_registry"]["scope.md"] == spec["source_registry"]["scope.md"]
    assert payload["source_roles"]["scope.md"] == "deployment_requirement"
    for other in set(CLASSIFIER_IDS) - {classifier_id}:
        assert f"{other}_standard.md" not in payload["source_registry"]
        spec["context_by_classifier"][other]["benchmark_evidence"][0]["statement"] = "Unrelated revision."
    assert classification_request(item, spec, spec["deployment"], classifier_id) == request
    assert set(payload["source_registry"]) == set(payload["source_roles"])
    assert payload["item"] == item and payload["dataset_profile"] == spec["dataset_profile"]
    if classifier_id == "input_ontology":
        assert payload["input_category_inventory"] == spec["input_category_inventory"]
    else:
        assert "input_category_inventory" not in payload


def test_each_received_response_is_a_durable_cumulative_checkpoint(prepared):
    run(prepared, limit=1, call=Judge(prepared))
    records = [json.loads(line) for line in (prepared / "results.jsonl").read_text().splitlines()]
    assert len(records) == 4
    assert [record["status"] for record in records] == ["partial", "partial", "partial", "complete"]
    for count, record in enumerate(records, 1):
        assert record["schema_version"] == "caliper_item_result_v3"
        assert set(record["labels"]) == set(CLASSIFIER_IDS[:count])
        assert not record["classifier_errors"]
        assert len(record["attempts"]) == count
        assert [entry["classifier_id"] for entry in record["attempts"]] == list(CLASSIFIER_IDS[:count])
    assert read_results(prepared / "results.jsonl") == {records[-1]["item_id"]: records[-1]}


@pytest.mark.parametrize("invalid_response", ["combined", "sibling"])
def test_one_dimension_cannot_accept_sibling_judgments_or_repair_them(prepared, invalid_response):
    fixture = Judge(prepared)
    if invalid_response == "combined":
        labels = {}
        for cid in CLASSIFIER_IDS:
            labels.update(json.loads(fixture.response(cid))["labels"])
        invalid = json.dumps({"labels": labels})
    else:
        invalid = fixture.response("input_content")
    judge = Judge(prepared, [fixture.response("input_ontology"),
                            fixture.response("input_content"), invalid])
    state = run(prepared, limit=1, call=judge)
    assert state["complete"] == 1 and state["errors"] == 0
    assert [request["step"] for request in judge.calls] == [
        "item_classification.input_ontology", "item_classification.input_content",
        "item_classification.output_ontology", "item_classification_repair.output_ontology",
        "item_classification.output_content",
    ]
    assert request_payload(judge.calls[2]) == request_payload(judge.calls[3])
    records = [json.loads(line) for line in (prepared / "results.jsonl").read_text().splitlines()]
    failed = records[2]
    assert set(failed["labels"]) == {"input_ontology", "input_content"}
    assert set(failed["classifier_errors"]) == {"output_ontology"}
    assert set(records[3]["labels"]) == set(CLASSIFIER_IDS[:3])
    assert not records[3]["classifier_errors"]
    assert records[-1]["labels"]["input_content"] == records[1]["labels"]["input_content"]


def test_api_failure_mid_item_preserves_success_and_resumes_only_missing_dimensions(prepared):
    success = Judge(prepared).response("input_ontology")
    broken = Judge(prepared, [success, RuntimeError("quota unavailable")])
    state = run(prepared, limit=None, call=broken)
    assert state["complete"] == 0 and state["errors"] == 1 and state["pending"] == 4
    assert state["completed_item_classifier_judgments"] == 1
    assert "quota" in state["fatal_error"]
    assert len(broken.calls) == 2
    record = next(iter(read_results(prepared / "results.jsonl").values()))
    assert set(record["labels"]) == {"input_ontology"}
    assert set(record["classifier_errors"]) == {"input_content"}
    assert [attempt["classifier_id"] for attempt in record["attempts"]] == ["input_ontology", "input_content"]
    recovered = Judge(prepared)
    result = run(prepared, limit=None, resume=True, call=recovered)
    assert result["full_dataset_complete"]
    assert len(recovered.calls) == 19
    assert request_payload(recovered.calls[0])["classifier"]["id"] == "input_content"
    first_item_calls = [request_payload(request)["classifier"]["id"] for request in recovered.calls
                        if request_payload(request)["item"]["item_id"] == record["item_id"]]
    assert first_item_calls == list(CLASSIFIER_IDS[1:])
    final_record = read_results(prepared / "results.jsonl")[record["item_id"]]
    assert final_record["labels"]["input_ontology"] == record["labels"]["input_ontology"]
    assert not final_record["classifier_errors"]
    assert len(final_record["attempts"]) == 5
    assert generate_report(prepared)["completed_items"] == 5


def test_progress_callback_observes_saved_results_and_stop_is_resumable(prepared):
    saved = []

    def on_result(record):
        assert read_results(prepared / "results.jsonl")[record["item_id"]] == record
        saved.append(record)

    judge = Judge(prepared)
    state = run(prepared, limit=None, call=judge, on_result=on_result,
                should_stop=lambda: len(saved) == 2)
    assert state["cancelled"] and state["complete"] == 0 and state["pending"] == 4
    assert state["partial"] == 1 and state["errors"] == 0
    assert state["completed_item_classifier_judgments"] == 2
    assert len(judge.calls) == 2
    assert [set(record["labels"]) for record in saved] == [
        {"input_ontology"}, {"input_ontology", "input_content"},
    ]
    assert all(record["status"] == "partial" for record in saved)
    resumed = Judge(prepared)
    assert run(prepared, limit=None, call=resumed, resume=True)["full_dataset_complete"]
    assert len(resumed.calls) == 18
    assert request_payload(resumed.calls[0])["classifier"]["id"] == "output_ontology"


def test_cancellation_before_repair_prevents_another_paid_call(prepared):
    judge = Judge(prepared, ['{"labels": {}}'])
    state = run(prepared, limit=None, call=judge, should_stop=lambda: bool(judge.calls))
    assert state["cancelled"] and state["errors"] == 1
    assert len(judge.calls) == 1
    assert len(read_results(prepared / "results.jsonl")) == 1


def test_already_cancelled_run_makes_no_calls(prepared):
    judge = Judge(prepared)
    state = run(prepared, call=judge, should_stop=lambda: True)
    assert state["cancelled"] and state["complete"] == 0
    assert state["pending"] == 5 and not judge.calls


def test_invalid_labels_receive_only_one_repair_and_are_errors_not_negatives(prepared):
    judge = Judge(prepared, ['{"labels": {}}', '{"labels": {}}'])
    state = run(prepared, limit=1, call=judge)
    assert len(judge.calls) == 5
    assert state["errors"] == 1 and state["complete"] == 0
    assert state["completed_item_classifier_judgments"] == 3
    assert "structural errors" in judge.calls[1]["user"]
    assert [request["step"] for request in judge.calls] == [
        "item_classification.input_ontology", "item_classification_repair.input_ontology",
        *[f"item_classification.{cid}" for cid in CLASSIFIER_IDS[1:]],
    ]
    record = next(iter(read_results(prepared / "results.jsonl").values()))
    assert set(record["labels"]) == set(CLASSIFIER_IDS[1:])
    assert set(record["classifier_errors"]) == {"input_ontology"}
    summary = generate_report(prepared)
    for classifier in summary["classifiers"]:
        if classifier["id"] == "input_ontology":
            assert classifier["valid_judgments"] == 0 and classifier["errors"] == 1
        else:
            assert classifier["valid_judgments"] == 1 and classifier["errors"] == 0
    recovered = Judge(prepared)
    assert run(prepared, limit=1, resume=True, call=recovered)["complete"] == 1
    assert len(recovered.calls) == 1
    assert request_payload(recovered.calls[0])["classifier"]["id"] == "input_ontology"
    final = read_results(prepared / "results.jsonl")[record["item_id"]]
    assert all(final["labels"][cid] == value for cid, value in record["labels"].items())
    assert final["attempts"][:5] == record["attempts"] and len(final["attempts"]) == 6


def test_insufficient_evidence_is_completed_and_separate_from_determinate_judgments(prepared):
    judge = Judge(prepared)
    responses = [judge.response(cid, insufficient=True) for cid in CLASSIFIER_IDS]
    state = run(prepared, limit=1, call=Judge(prepared, responses))
    assert state["complete"] == 1
    summary = generate_report(prepared)
    assert all(c["insufficient_evidence"] == 1 and c["determinate_judgments"] == 0
               for c in summary["classifiers"] if c["applicable"])


@pytest.mark.parametrize("change", ["model", "provider", "reasoning", "tokens", "spec", "dataset", "evidence"])
def test_changed_inputs_rejected_before_spending_resume_calls(prepared, change):
    run(prepared, limit=1, call=Judge(prepared), model_id="first-model")
    kwargs = {"model_id": "first-model"}
    if change == "model":
        kwargs["model_id"] = "different-model"
    elif change == "provider":
        kwargs["provider"] = "another-provider"
    elif change == "reasoning":
        kwargs["reasoning_effort"] = "high"
    elif change == "tokens":
        kwargs["max_tokens"] = 2000
    else:
        path = prepared / {"spec": "classifier_spec.json", "dataset": "items.jsonl", "evidence": "evidence.json"}[change]
        path.write_text(path.read_text() + " ")
    judge = Judge(prepared)
    with pytest.raises(ValueError, match="changed"):
        run(prepared, limit=None, resume=True, call=judge, **kwargs)
    assert not judge.calls


def test_recover_truncated_tail_then_continue_without_repeating_first_item(prepared):
    run(prepared, limit=1, call=Judge(prepared))
    with (prepared / "results.jsonl").open("ab") as stream:
        stream.write(b'{"item_id": "incomplete')
    judge = Judge(prepared)
    state = run(prepared, limit=None, resume=True, call=judge)
    assert state["full_dataset_complete"] and len(judge.calls) == 16


@pytest.mark.parametrize("contents", [
    '{"item_id":"0","status":"bogus"}',
    '{"item_id":"0","status":"complete"}',
    '{"status":"error"}',
    'bad json\n',
])
def test_semantic_or_complete_line_corruption_is_never_silently_repaired(tmp_path, contents):
    path = tmp_path / "results.jsonl"
    path.write_text(contents)
    with pytest.raises(ValueError):
        read_results(path, repair_tail=True)
    assert path.read_text() == contents


@pytest.mark.parametrize("field", ["labels", "attempts"])
def test_checkpoint_cannot_erase_saved_success_or_attempt_history(prepared, field):
    run(prepared, limit=1, call=Judge(prepared))
    path = prepared / "results.jsonl"
    records = [json.loads(line) for line in path.read_text().splitlines()]
    if field == "labels":
        del records[1]["labels"]["input_ontology"]
    else:
        records[1]["attempts"] = records[1]["attempts"][1:]
    path.write_text("".join(json.dumps(record) + "\n" for record in records))
    with pytest.raises(ValueError, match="cannot change or disappear"):
        read_results(path, repair_tail=True)


def test_concurrent_writer_rejected_before_model_call(prepared):
    judge = Judge(prepared)
    with run_lock(prepared):
        with pytest.raises(ValueError, match="Another process"):
            run(prepared, call=judge)
    assert not judge.calls


def test_interrupt_leaves_completed_records_resumable(prepared):
    judge = Judge(prepared)
    calls = 0

    def interrupted(**request):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise KeyboardInterrupt()
        return judge(**request)

    with pytest.raises(KeyboardInterrupt):
        run(prepared, limit=None, call=interrupted)
    assert len(read_results(prepared / "results.jsonl")) == 1
    resumed = Judge(prepared)
    assert run(prepared, limit=None, resume=True, call=resumed)["full_dataset_complete"]
    assert len(resumed.calls) == 19
    assert request_payload(resumed.calls[0])["classifier"]["id"] == "input_content"


def test_fenced_json_preserves_unicode_separators_in_evidence():
    value = {"evidence": "before\u2028middle\u2029after\u0085end"}
    response = "```json\n" + json.dumps(value, ensure_ascii=False) + "\n```"
    assert parse_response(response) == value


def test_full_namespace_cli_calls_openai_adapter_and_saves_usage(prepared, monkeypatch, capsys):
    from anthropic_api_package_release.item_analysis import __main__ as cli
    from anthropic_api_package_release.item_analysis import model_client

    judge = Judge(prepared)

    def fake_call(*, api_key, **request):
        assert api_key == "test-openai-key"
        assert "step" not in request
        return SimpleNamespace(text=judge(**request), model=request["model"],
                               input_tokens=120, output_tokens=30, cached_input_tokens=20,
                               reasoning_tokens=10, latency_ms=1)

    monkeypatch.setattr(model_client, "call_text", fake_call)
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    assert cli.main(["classify", "--run-dir", str(prepared), "--limit", "1"]) == 0
    assert read_json(prepared / "usage.json")["input_tokens"] == 480
    assert [entry["step"] for entry in read_json(prepared / "usage_ledger.json")] == [
        f"item_classification.{cid}" for cid in CLASSIFIER_IDS
    ]
    assert read_json(prepared / "run.json")["model_id"] == "gpt-6-luna"
    assert cli.main(["classify", "--run-dir", str(prepared), "--all", "--resume"]) == 0
    assert len(judge.calls) == 20
    usage = read_json(prepared / "usage.json")
    assert usage["input_tokens"] == 2400 and usage["output_tokens"] == 600
    assert usage["cached_input_tokens"] == 400 and usage["reasoning_tokens"] == 200
    assert usage["calls"] == 20
    assert "test-openai-key" not in (prepared / "usage_ledger.json").read_text()
    assert read_json(prepared / "summary.json")["complete_snapshot"]
    assert cli.main(["report", "--run-dir", str(prepared)]) == 0
    assert cli.main(["validate", "--run-dir", str(prepared), "--review", str(prepared / "review.csv")]) == 0


def test_cli_dry_run_never_configures_api(prepared, monkeypatch):
    from anthropic_api_package_release.item_analysis import __main__ as cli

    def unexpected(directory):
        raise AssertionError("An offline preview must not configure API access")

    monkeypatch.setattr(cli, "_api", unexpected)
    assert cli.main(["classify", "--run-dir", str(prepared), "--dry-run"]) == 0
    assert not (prepared / "run.json").exists()


def test_cli_requires_openai_key_instead_of_legacy_provider_key(prepared, monkeypatch, capsys):
    from anthropic_api_package_release.item_analysis import __main__ as cli

    monkeypatch.setenv("OPENAI_API_KEY", "")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "legacy-test-key")
    assert cli.main(["classify", "--run-dir", str(prepared), "--all"]) == 1
    assert "Set OPENAI_API_KEY" in capsys.readouterr().err
    assert not (prepared / "run.json").exists()


def test_cli_records_billable_incomplete_response_before_stopping(prepared, monkeypatch):
    from anthropic_api_package_release.item_analysis import __main__ as cli
    from anthropic_api_package_release.item_analysis import model_client

    calls = []

    def incomplete(**request):
        calls.append(request)
        result = model_client.CallResult(
            text="", model="gpt-6-luna", input_tokens=120, output_tokens=4096,
            latency_ms=1, reasoning_tokens=4096,
        )
        raise model_client.ModelResponseError("OpenAI did not complete the response.", result)

    monkeypatch.setattr(model_client, "call_text", incomplete)
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    assert cli.main(["classify", "--run-dir", str(prepared), "--all"]) == 1
    assert len(calls) == 1
    usage = read_json(prepared / "usage.json")
    assert usage["calls"] == 1
    assert usage["output_tokens"] == 4096 and usage["reasoning_tokens"] == 4096
    assert read_json(prepared / "summary.json")["error_items"] == 1


def test_report_rejects_mutated_specification_after_scoring(prepared):
    run(prepared, limit=1, call=Judge(prepared))
    path = prepared / "classifier_spec.json"
    changed = read_json(path)
    changed["classifiers"][0]["question"] = "A different definition of relevance."
    path.write_text(json.dumps(changed))
    with pytest.raises(ValueError, match="specification changed"):
        generate_report(prepared)


@pytest.mark.parametrize("prompt_file", [
    *[f"classify_{cid}.md" for cid in CLASSIFIER_IDS], "generate_spec.md", "generate_user.md",
])
def test_changed_prompt_blocks_resume_before_api(prepared, tmp_path, monkeypatch, prompt_file):
    import shutil
    from item_analysis import classify

    run(prepared, limit=1, call=Judge(prepared))
    prompts = tmp_path / "changed_prompts"
    shutil.copytree(classify.PROMPT_DIR, prompts)
    path = prompts / prompt_file
    path.write_text(path.read_text() + "\nChanged task instructions.\n")
    monkeypatch.setattr(classify, "PROMPT_DIR", prompts)
    judge = Judge(prepared)
    with pytest.raises(ValueError, match="changed"):
        run(prepared, limit=2, resume=True, call=judge)
    assert not judge.calls


def test_changed_catalog_contents_block_resume_even_without_version_bump(prepared, monkeypatch):
    from item_analysis import classify

    run(prepared, limit=1, call=Judge(prepared))
    changed = classify.get_catalog()
    changed[0]["question"] = "A different fixed question"
    monkeypatch.setattr(classify, "get_catalog", lambda: changed)
    judge = Judge(prepared)
    with pytest.raises(ValueError, match="changed"):
        run(prepared, limit=2, resume=True, call=judge)
    assert not judge.calls


def test_legacy_specification_is_readable_but_cannot_start_a_new_run(prepared):
    from item_analysis.data import file_sha256
    from item_analysis.schema import validate_spec
    from item_analysis.storage import write_json

    legacy_path = Path(__file__).parent / "fixtures" / "item_analysis_spec.json"
    legacy = read_json(legacy_path)
    assert validate_spec(legacy)["classifiers"]
    write_json(prepared / "classifier_spec.json", legacy)
    metadata = read_json(prepared / "specification.json")
    metadata["spec_sha256"] = file_sha256(prepared / "classifier_spec.json")
    write_json(prepared / "specification.json", metadata)
    judge = Judge(prepared)
    with pytest.raises(ValueError, match="Historical"):
        run(prepared, call=judge)
    assert not judge.calls


def test_resume_rejects_result_from_a_different_catalog(prepared):
    run(prepared, limit=1, call=Judge(prepared))
    path = prepared / "results.jsonl"
    records = [json.loads(line) for line in path.read_text().splitlines()]
    records[-1]["fixed_catalog_version"] = "a_different_catalog"
    path.write_text("".join(json.dumps(record) + "\n" for record in records))
    judge = Judge(prepared)
    with pytest.raises(ValueError, match="catalog changed"):
        run(prepared, limit=2, resume=True, call=judge)
    assert not judge.calls


def test_old_combined_request_run_cannot_resume_as_split_requests(prepared):
    run(prepared, limit=1, call=Judge(prepared))
    path = prepared / "run.json"
    config = read_json(path)
    config.update(version=3, schema_version="caliper_item_result_v2", request_mode="combined")
    path.write_text(json.dumps(config))
    judge = Judge(prepared)
    with pytest.raises(ValueError, match="changed"):
        run(prepared, limit=2, resume=True, call=judge)
    assert not judge.calls


def test_resume_cannot_shrink_selected_population(prepared):
    run(prepared, limit=3, call=Judge(prepared))
    judge = Judge(prepared)
    with pytest.raises(ValueError, match="only grow"):
        run(prepared, limit=2, resume=True, call=judge)
    assert not judge.calls
