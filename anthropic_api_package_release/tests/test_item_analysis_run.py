"""Offline end-to-end checks for the review checkpoint and full continuation."""

import json
from pathlib import Path
from types import SimpleNamespace

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from item_analysis.classify import read_results, run
from item_analysis.generate import generate_spec
from item_analysis.prepare import prepare
from item_analysis.report import generate_report
from item_analysis.storage import parse_response, read_json, run_lock

FIXTURE = Path(__file__).parent / "fixtures" / "item_analysis_spec.json"


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
        labels = {}
        for classifier in self.spec["classifiers"]:
            if not classifier["applicable"]:
                continue
            operation = classifier["operation"]
            label = classifier["category_set"][0] if operation == "assignment" else 2 if operation == "ordinal" else 0
            labels[classifier["id"]] = {
                "label": label, "evidence": ["content: Question"],
                "justification": "Fixture evidence supports this label.",
            }
        return json.dumps({"labels": labels})


def test_checkpoint_continues_to_all_without_repeating_completed_items(prepared):
    judge = Judge(prepared)
    first = run(prepared, limit=2, call=judge, model_id="test-model")
    assert first["complete"] == 2 and not first["full_dataset_complete"]
    first_ids = set(read_results(prepared / "results.jsonl"))
    final = run(prepared, limit=None, resume=True, call=judge, model_id="test-model")
    assert final["complete"] == 5 and final["full_dataset_complete"]
    assert final["attempted_this_invocation"] == 3
    assert len(judge.calls) == 5
    called_ids = [json.loads(request["user"])["item"]["item_id"] for request in judge.calls]
    assert len(set(called_ids)) == 5
    assert set(called_ids[:2]) == first_ids
    assert all(request["model"] == "haiku" for request in judge.calls)
    summary = generate_report(prepared)
    assert summary["complete_snapshot"]
    assert (prepared / "report.html").exists()


def test_dry_run_saves_complete_requests_without_results_or_api_calls(prepared):
    judge = Judge(prepared)
    state = run(prepared, dry_run=True, limit=2, call=judge)
    assert state["model_calls"] == 0 and not judge.calls
    assert not (prepared / "run.json").exists()
    assert not (prepared / "results.jsonl").exists()
    previews = [json.loads(line) for line in (prepared / "preview_requests.jsonl").read_text().splitlines()]
    assert len(previews) == 2
    payload = json.loads(previews[0]["request"]["user"])
    assert payload["item"]["reference_answer"] == "A"
    assert len(payload["classifiers"]) == 4  # MCQ output-category slot is explicitly N/A.


def test_api_failure_stops_preserves_progress_and_resume_retries_failed_item(prepared):
    success = Judge(prepared)()
    broken = Judge(prepared, [success, RuntimeError("quota unavailable")])
    state = run(prepared, limit=None, call=broken)
    assert state["complete"] == 1 and state["errors"] == 1 and state["pending"] == 3
    assert "quota" in state["fatal_error"]
    assert len(broken.calls) == 2
    recovered = Judge(prepared)
    result = run(prepared, limit=None, resume=True, call=recovered)
    assert result["full_dataset_complete"]
    assert len(recovered.calls) == 4
    assert generate_report(prepared)["completed_items"] == 5


def test_progress_callback_observes_saved_results_and_stop_is_resumable(prepared):
    saved = []

    def on_result(record):
        assert read_results(prepared / "results.jsonl")[record["item_id"]] == record
        saved.append(record)

    judge = Judge(prepared)
    state = run(prepared, limit=None, call=judge, on_result=on_result,
                should_stop=lambda: len(saved) == 2)
    assert state["cancelled"] and state["complete"] == 2 and state["pending"] == 3
    assert len(judge.calls) == 2
    resumed = Judge(prepared)
    assert run(prepared, limit=None, call=resumed, resume=True)["full_dataset_complete"]
    assert len(resumed.calls) == 3


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
    assert len(judge.calls) == 2
    assert state["errors"] == 1 and state["complete"] == 0
    assert "structural errors" in judge.calls[1]["user"]
    summary = generate_report(prepared)
    for classifier in summary["classifiers"]:
        if classifier["applicable"]:
            assert classifier["known"] == 0 and classifier["errors"] == 1


def test_null_is_completed_but_excluded_from_prevalence_denominator(prepared):
    response = json.loads(Judge(prepared)())
    for judgment in response["labels"].values():
        judgment.update(label=None, evidence=[], justification="Required deployment evidence is missing.")
    state = run(prepared, limit=1, call=Judge(prepared, [json.dumps(response)]))
    assert state["complete"] == 1
    summary = generate_report(prepared)
    assert all(c["unknown"] == 1 and c["known"] == 0 for c in summary["classifiers"] if c["applicable"])


@pytest.mark.parametrize("change", ["model", "tokens", "spec", "dataset", "evidence"])
def test_changed_inputs_rejected_before_spending_resume_calls(prepared, change):
    run(prepared, limit=1, call=Judge(prepared), model_id="first-model")
    kwargs = {"model_id": "first-model"}
    if change == "model":
        kwargs["model_id"] = "different-model"
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
    assert state["full_dataset_complete"] and len(judge.calls) == 4


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
    assert len(resumed.calls) == 4


def test_fenced_json_preserves_unicode_separators_in_evidence():
    value = {"evidence": "before\u2028middle\u2029after\u0085end"}
    response = "```json\n" + json.dumps(value, ensure_ascii=False) + "\n```"
    assert parse_response(response) == value


def test_full_namespace_cli_calls_shared_client_and_saves_usage(prepared, monkeypatch, capsys):
    from anthropic_api_package_release.item_analysis import __main__ as cli

    judge = Judge(prepared)
    client = SimpleNamespace(
        MODELS={"haiku": "test-haiku"}, call=judge,
        save_ledger=lambda path: path.write_text('{"ledger": true}'),
        dump_cost_ledger=lambda path: path.write_text('{"usage": true}'),
    )
    monkeypatch.setattr(cli, "_api", lambda directory: client)
    assert cli.main(["classify", "--run-dir", str(prepared), "--limit", "1"]) == 0
    assert (prepared / "usage.json").exists()
    assert (prepared / "usage_ledger.json").exists()
    assert read_json(prepared / "run.json")["model_id"] == "test-haiku"
    assert cli.main(["classify", "--run-dir", str(prepared), "--all", "--resume"]) == 0
    assert len(judge.calls) == 5
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


def test_report_rejects_mutated_specification_after_scoring(prepared):
    run(prepared, limit=1, call=Judge(prepared))
    path = prepared / "classifier_spec.json"
    changed = read_json(path)
    changed["classifiers"][0]["criterion"] = "A different definition of relevance."
    path.write_text(json.dumps(changed))
    with pytest.raises(ValueError, match="specification changed"):
        generate_report(prepared)
