"""Offline six-score behavior: grounded unknowns, one-call items and safe resume."""

from copy import deepcopy
import json

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from item_analysis.classify import read_results, run
from item_analysis.data import prepare_data
from item_analysis.prepare import attach_direct_context, prepare
from item_analysis.scoring import (
    DIMENSIONS, RESULT_SCHEMA_VERSION, is_score_spec, prepare_context, scoring_request,
    validate_dimensions,
)
from item_analysis.storage import read_json


def response(*, unknown=None):
    dimensions = {cid: {
        "score": 4, "justification": "The item aligns with the documented deployment task.",
        "evidence": ["content: What is 2 + 2?", "direct_context.json#/task_requirements: arithmetic"],
        "information_gaps": [],
    } for cid in DIMENSIONS}
    if unknown:
        dimensions[unknown].update(score=None, evidence=[], information_gaps=["No reference answer was supplied."])
    return {"dimensions": dimensions}


@pytest.fixture
def score_directory(tmp_path):
    source = tmp_path / "items.parquet"
    pq.write_table(pa.Table.from_pylist([
        {"item_id": str(i), "content": "What is 2 + 2?", "reference_answer": "4"}
        for i in range(4)
    ]), source)
    directory = tmp_path / "run"
    prepare_data(source, directory, benchmark="arithmetic")
    attach_direct_context(directory, {
        "benchmark": "arithmetic", "deployment": "Text-based arithmetic tutoring.",
        "task_requirements": "Help learners solve arithmetic questions.",
        "answer_requirements": "Return a short textual answer.",
        "validity_concerns": "A prior hypothesis about regional differences, not an established fact.",
    })
    prepare_context(directory)
    return directory


class Judge:
    def __init__(self, responses=()):
        self.calls = []
        self.responses = list(responses)

    def __call__(self, **request):
        self.calls.append(request)
        result = self.responses.pop(0) if self.responses else json.dumps(response())
        if isinstance(result, Exception):
            raise result
        return result


def test_prepared_context_has_six_fixed_dimensions_without_generation(score_directory):
    spec = read_json(score_directory / "classifier_spec.json")
    assert is_score_spec(spec)
    assert [dimension["id"] for dimension in spec["classifiers"]] == list(DIMENSIONS)
    assert spec["assessment_status"] == "not_run"
    assert "prior_hypothesis" not in spec["source_roles"].values()
    assert "framework.yaml" not in spec["source_registry"]
    assert not any(key.startswith("items.jsonl") for key in spec["source_registry"])
    assert not (score_directory / "generation_request.json").exists()
    assert read_json(score_directory / "specification.json")["source"]["kind"] == "deterministic"


def test_benchmark_context_retains_paired_elicitation_sources_without_prior_scores(tmp_path):
    source = tmp_path / "items.parquet"
    pq.write_table(pa.Table.from_pylist([{"item_id": "1", "content": "Arithmetic question"}]), source)
    assessment = tmp_path / "assessment"
    assessment.mkdir()
    (assessment / "scoring.json").write_text(json.dumps({
        "benchmark": "arithmetic", "dimensions": {"input_content": {"score": 1, "justification": "PRIOR_SCORE_SENTINEL"}},
    }))
    for filename, content in {
        "deployment_description.txt": "Arithmetic tutoring in English.",
        "elicitation_summary.md": "Users need arithmetic practice.",
        "dataset_analysis_report.md": "PRIOR_HYPOTHESIS_SENTINEL",
        "elicitation_questions.json": json.dumps([
            {"id": "Q1", "question": "Must this deployment support text, spoken questions, or both?"},
        ]),
        "elicitation_answers.json": json.dumps({"Q1": "Both of the mentioned modalities are required."}),
        "benchmark.yaml": "The benchmark's original arithmetic instructions.",
        "region.yaml": "Documented regional evidence.",
    }.items():
        (assessment / filename).write_text(content)
    directory = tmp_path / "analysis"
    prepare(assessment, source, directory)
    spec = prepare_context(directory)
    request = scoring_request({"item_id": "1", "content": "Arithmetic question"}, spec)
    assert all(text not in request["user"] for text in (
        "PRIOR_SCORE_SENTINEL", "PRIOR_HYPOTHESIS_SENTINEL",
    ))
    payload = json.loads(request["user"])
    assert payload["source_registry"]["region.yaml"] == "Documented regional evidence."
    assert "benchmark.yaml" in payload["source_registry"]
    questions = json.loads(payload["source_registry"]["elicitation_questions.json"])
    answers = json.loads(payload["source_registry"]["elicitation_answers.json"])
    assert questions[0]["id"] == "Q1" and "spoken questions" in questions[0]["question"]
    assert answers[questions[0]["id"]] == "Both of the mentioned modalities are required."
    assert payload["source_roles"]["elicitation_questions.json"] == "elicitation_question"
    assert payload["source_roles"]["elicitation_answers.json"] == "deployment_requirement"
    assert payload["assessment_status"] == "complete"
    assert json.loads((directory / "evidence.json").read_text())["scoring"]["dimensions"]["input_content"]["score"] == 1


def test_preview_and_request_have_one_complete_request_per_item(score_directory):
    judge = Judge()
    state = run(score_directory, dry_run=True, limit=2, call=judge)
    requests = [json.loads(line) for line in (score_directory / "preview_requests.jsonl").read_text().splitlines()]
    assert state["primary_requests"] == len(requests) == 2
    assert state["target_item_classifier_judgments"] == 12
    assert state["model_calls"] == 0 and not judge.calls
    assert not (score_directory / "run.json").exists()
    for request in requests:
        payload = json.loads(request["request"]["user"])
        assert set(payload["output_schema"]["properties"]["dimensions"]["properties"]) == set(DIMENSIONS)
        assert payload["item"]["item_id"] == request["item_id"]
        assert request["request"]["step"] == "item_scoring"
        assert "input_form" in request["request"]["system"]


def test_one_call_returns_all_six_and_resume_only_scores_new_items(score_directory):
    judge = Judge()
    first = run(score_directory, limit=2, call=judge)
    assert first["complete"] == len(judge.calls) == 2
    assert first["completed_item_classifier_judgments"] == 12
    saved = read_results(score_directory / "results.jsonl")
    assert all(record["schema_version"] == RESULT_SCHEMA_VERSION and set(record["dimensions"]) == set(DIMENSIONS)
               for record in saved.values())
    final = run(score_directory, limit=None, resume=True, call=judge)
    assert final["complete"] == len(judge.calls) == 4
    assert final["request_calls_this_invocation"] == 2 and final["full_dataset_complete"]
    assert all("labels" not in record for record in read_results(score_directory / "results.jsonl").values())


def test_unknown_is_complete_and_never_retried(score_directory):
    judge = Judge([json.dumps(response(unknown="output_content"))])
    first = run(score_directory, limit=1, call=judge)
    assert first["complete"] == 1 and first["errors"] == 0
    run(score_directory, limit=1, resume=True, call=judge)
    assert len(judge.calls) == 1
    record = next(iter(read_results(score_directory / "results.jsonl").values()))
    assert record["dimensions"]["output_content"]["score"] is None


@pytest.mark.parametrize("invalid", [True, False, 0, 6, 2.0, "4"])
def test_invalid_numeric_scores_are_rejected(invalid):
    payload = response()
    payload["dimensions"]["input_form"]["score"] = invalid
    with pytest.raises(ValueError, match="integer 1–5 or null"):
        validate_dimensions(payload)


def test_numeric_evidence_unknown_gaps_and_all_dimensions_are_required():
    payload = response()
    del payload["dimensions"]["input_form"]
    with pytest.raises(ValueError, match="all six"):
        validate_dimensions(payload)
    payload = response()
    payload["dimensions"]["input_form"]["evidence"] = []
    with pytest.raises(ValueError, match="supporting evidence"):
        validate_dimensions(payload)
    payload = response()
    payload["dimensions"]["input_form"]["score"] = None
    with pytest.raises(ValueError, match="information gaps"):
        validate_dimensions(payload)


def test_structural_repair_is_bounded_and_failed_items_retry_on_resume(score_directory):
    judge = Judge(["not JSON", "still not JSON"])
    first = run(score_directory, limit=2, call=judge)
    assert len(judge.calls) == 3
    assert first["complete"] == 1 and first["errors"] == 1
    records = read_results(score_directory / "results.jsonl")
    failed_id = next(key for key, record in records.items() if record["status"] == "error")
    assert records[failed_id]["dimensions"] == {}
    assert judge.calls[1]["step"] == "item_scoring_repair"
    final = run(score_directory, limit=2, resume=True, call=judge)
    assert len(judge.calls) == 4 and final["complete"] == 2
    assert final["request_calls_this_invocation"] == 1
    assert len(read_results(score_directory / "results.jsonl")[failed_id]["attempts"]) == 3


def test_api_failure_stops_spending_and_is_distinct_from_unknown(score_directory):
    judge = Judge([RuntimeError("provider unavailable")])
    state = run(score_directory, limit=None, call=judge)
    assert len(judge.calls) == 1 and state["errors"] == 1 and state["pending"] == 3
    assert state["fatal_error"] == "RuntimeError: provider unavailable"
    failed = next(iter(read_results(score_directory / "results.jsonl").values()))
    assert failed["dimensions"] == {} and failed["attempts"][0]["kind"] == "api"
    assert run(score_directory, limit=None, resume=True, call=judge)["complete"] == 4


def test_cancellation_saves_returned_result_before_stopping(score_directory):
    judge = Judge()
    observed = []
    state = run(score_directory, limit=None, call=judge, on_result=observed.append,
                should_stop=lambda: len(judge.calls) >= 1)
    assert state["cancelled"] and state["complete"] == 1 and len(observed) == 1
    assert len(read_results(score_directory / "results.jsonl")) == 1
    assert run(score_directory, limit=None, resume=True, call=judge)["complete"] == 4


def test_cancellation_after_malformed_response_saves_failure_without_repair(score_directory):
    judge = Judge(["invalid"])
    state = run(score_directory, limit=1, call=judge, should_stop=lambda: len(judge.calls) >= 1)
    assert state["cancelled"] and state["errors"] == 1 and len(judge.calls) == 1
    assert run(score_directory, limit=1, resume=True, call=judge)["complete"] == 1


def test_changed_prompt_or_model_blocks_resume_before_api(score_directory, tmp_path, monkeypatch):
    from item_analysis import scoring

    judge = Judge()
    run(score_directory, limit=1, call=judge)
    with pytest.raises(ValueError, match="changed"):
        run(score_directory, limit=2, resume=True, call=judge, model_id="changed-model")
    prompt = tmp_path / "changed_prompt.md"
    prompt.write_text(scoring.PROMPT_PATH.read_text() + "\nChanged rubric.")
    monkeypatch.setattr(scoring, "PROMPT_PATH", prompt)
    with pytest.raises(ValueError, match="changed"):
        run(score_directory, limit=2, resume=True, call=judge)
    assert len(judge.calls) == 1


def test_saved_result_corruption_is_rejected_and_only_truncated_tail_is_repaired(score_directory):
    judge = Judge()
    run(score_directory, limit=1, call=judge)
    path = score_directory / "results.jsonl"
    valid = path.read_text()
    path.write_text(valid + '{"item_id":')
    with pytest.raises(ValueError, match="Invalid results record"):
        read_results(path)
    assert len(read_results(path, repair_tail=True)) == 1
    assert path.read_text() == valid
    path.write_text(valid + "broken\n")
    with pytest.raises(ValueError, match="Invalid results record"):
        read_results(path, repair_tail=True)
    record = json.loads(valid)
    record["dimensions"]["input_content"]["score"] = False
    path.write_text(json.dumps(record) + "\n")
    with pytest.raises(ValueError, match="integer 1–5 or null"):
        run(score_directory, limit=2, resume=True, call=judge)
    assert len(judge.calls) == 1


def test_completed_results_cannot_be_overwritten(score_directory):
    run(score_directory, limit=1, call=Judge())
    path = score_directory / "results.jsonl"
    original = path.read_text()
    changed = deepcopy(json.loads(original))
    changed["dimensions"]["input_content"]["score"] = 2
    path.write_text(original + json.dumps(changed) + "\n")
    with pytest.raises(ValueError, match="Duplicate completed"):
        read_results(path)
