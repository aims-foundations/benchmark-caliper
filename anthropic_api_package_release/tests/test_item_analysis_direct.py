"""Direct item analysis uses explicit requirements, without invented assessments."""

from copy import deepcopy
import csv
import json
import re

import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from jsonschema import Draft202012Validator

from item_analysis.classify import run
from item_analysis.data import file_sha256, prepare_data
from item_analysis.generate import SpecificationValidationError, generate_spec, generation_request
from item_analysis.prepare import attach_direct_context
from item_analysis.report import generate_report
from item_analysis.schema import ROSTER
from item_analysis.storage import check_prepared, read_json, write_json


CONTEXT = {
    "benchmark": "example", "deployment": "English-text tutoring for Indian metropolitan schools.",
    "task_requirements": "Required tasks: arithmetic and Indian history. Exclude physics.",
    "answer_requirements": "Give the correct answer and a short English explanation.",
    "validity_concerns": "Check whether the questions cover the required tasks.",
}


@pytest.fixture
def raw_dataset(tmp_path):
    source = tmp_path / "items.parquet"
    pq.write_table(pa.Table.from_pylist([
        {"item_id": "math", "content": "What is one plus one?\nA. two\nB. three", "reference_answer": "A", "subject": "arithmetic"},
        {"item_id": "physics", "content": "Which unit measures force?\nA. newton\nB. meter", "reference_answer": "A", "subject": "physics"},
    ]), source)
    directory = tmp_path / "run"
    prepare_data(source, directory, benchmark="example", source_repo="user-upload")
    return directory


@pytest.fixture
def direct(raw_dataset):
    canonical = "Deployment context:\n" + CONTEXT["deployment"] + "\n\nTask requirements:\n" + CONTEXT["task_requirements"]
    canonical += "\n\nAnswer requirements:\n" + CONTEXT["answer_requirements"] + "\n\nValidity concerns:\n" + CONTEXT["validity_concerns"]
    attach_direct_context(raw_dataset, CONTEXT, deployment=canonical)
    return raw_dataset


def _spec(directory):
    evidence = read_json(directory / "evidence.json")
    return {"fixed_catalog_version": "caliper_generic_items_v1", "benchmark": "example",
            "deployment_description": evidence["deployment"],
            "input_category_inventory": {
                "completeness": "partial", "completeness_source_ids": [],
                "categories": [{"id": "required_001", "name": "Arithmetic", "definition": "Arithmetic tasks.",
                                "source_ids": ["direct_context.json#/task_requirements"]}],
                "evidence_gaps": ["The requirements do not assert a complete inventory."]},
            "context_by_classifier": {cid: {
                "deployment_requirements": [{"statement": "The required tasks include arithmetic.",
                                             "source_ids": ["direct_context.json#/task_requirements"]}],
                "benchmark_evidence": [], "prior_hypotheses": [], "evidence_gaps": ["No additional standards supplied."]}
                for cid in ROSTER}}


def tagged(user, tag):
    return re.search(rf"<{tag}>\n(.*?)\n</{tag}>", user, re.S).group(1)


def test_direct_evidence_freezes_requirements_and_actual_items_without_scoring(direct):
    evidence = read_json(direct / "evidence.json")
    dataset = check_prepared(direct)
    assert evidence["analysis_basis"] == "deployment_requirements"
    assert evidence["assessment_status"] == "not_run"
    assert evidence["direct_context"] == CONTEXT
    assert read_json(direct / "direct_context.json") == CONTEXT
    assert evidence["requirements"]["task_requirements"] == CONTEXT["task_requirements"]
    assert evidence["registry"]["direct_context.json#/task_requirements"] == CONTEXT["task_requirements"]
    assert evidence["registry"]["deployment_description.txt"] == evidence["deployment"]
    assert "framework.yaml" in evidence["registry"]
    assert "scoring" not in evidence
    assert not any(key.startswith("scoring.json") for key in evidence["registry"])
    assert not (direct / "scoring.json").exists()
    assert dataset["item_count"] == 2
    assert dataset["direct_context_sha256"] == file_sha256(direct / "direct_context.json")


@pytest.mark.parametrize("field", ["benchmark", "deployment", "task_requirements", "answer_requirements"])
def test_direct_missing_requirement_rejected_before_context_is_frozen(raw_dataset, field):
    invalid = {**CONTEXT, field: " "}
    with pytest.raises(ValueError, match=field):
        attach_direct_context(raw_dataset, invalid)
    assert not (raw_dataset / "evidence.json").exists()
    assert not (raw_dataset / "direct_context.json").exists()


def test_confirmed_alias_preserves_source_identity_and_context_cannot_be_replaced(raw_dataset):
    context = {**CONTEXT, "benchmark": "Example official release"}
    with pytest.raises(ValueError, match="does not match"):
        attach_direct_context(raw_dataset, context)
    attach_direct_context(raw_dataset, context, confirmed_source=True)
    dataset = check_prepared(raw_dataset)
    assert dataset["source_benchmark"] == "example"
    assert dataset["benchmark"] == "Example official release"
    with pytest.raises(ValueError, match="already frozen"):
        attach_direct_context(raw_dataset, CONTEXT)


def test_direct_generation_request_distinguishes_required_tasks_from_observed_subjects(direct):
    request = generation_request(direct)
    registry = json.loads(tagged(request["user"], "source_registry"))
    assert registry["direct_context.json#/task_requirements"]["content"] == CONTEXT["task_requirements"]
    assert registry["direct_context.json#/task_requirements"]["role"] == "deployment_requirement"
    assert registry["direct_context.json#/validity_concerns"]["role"] == "prior_hypothesis"
    assert json.loads(tagged(request["user"], "dataset_profile"))["row_count"] == 2
    assert {item["item_id"] for item in json.loads(tagged(request["user"], "example_items"))} == {"math", "physics"}
    assert not any(key.startswith("scoring.json") for key in registry)
    assert "Dataset contents show what the benchmark contains" in request["system"]


def test_direct_specification_requires_deployment_grounding_and_retains_provenance(direct):
    valid = _spec(direct)
    invalid = deepcopy(valid)
    invalid["input_category_inventory"]["categories"][0]["source_ids"] = ["framework.yaml"]
    calls = []

    def fake(**request):
        calls.append(request)
        return json.dumps(invalid if len(calls) == 1 else valid)

    canonical = generate_spec(direct, call=fake)
    assert len(calls) == 2 and "source role cannot ground" in calls[1]["user"]
    assert canonical["analysis_basis"] == "deployment_requirements"
    assert canonical["assessment_status"] == "not_run"
    assert canonical["dataset_profile"] == read_json(direct / "profile.json")
    assert canonical["input_category_inventory"]["categories"][0]["id"] == "required_001"
    metadata = read_json(direct / "specification.json")
    assert metadata["unassessed_dimensions"] == ["input_form", "output_form"]
    assert "No benchmark assessment was run" in metadata["note"]


def test_exhausted_direct_task_grounding_failure_has_safe_specific_diagnostic(direct):
    invalid = _spec(direct)
    invalid["input_category_inventory"]["categories"][0]["source_ids"] = ["framework.yaml"]
    calls = []

    def fake(**request):
        calls.append(request)
        return json.dumps(invalid)

    with pytest.raises(SpecificationValidationError, match="after one repair") as caught:
        generate_spec(direct, call=fake)
    assert caught.value.code == "task_grounding"
    assert "task requirements" in caught.value.public_message
    assert CONTEXT["task_requirements"] not in caught.value.public_message
    assert len(calls) == 2 and not (direct / "classifier_spec.json").exists()


@pytest.mark.parametrize("artifact", ["direct_context.json", "evidence.json"])
def test_direct_context_mutation_is_rejected_before_generation(direct, artifact):
    path = direct / artifact
    path.write_text(path.read_text() + "\n")
    calls = []
    with pytest.raises(ValueError, match="changed"):
        generate_spec(direct, call=lambda **request: calls.append(request))
    assert calls == []


def test_direct_evidence_rejects_a_benchmark_score_even_when_manifest_hash_is_updated(direct):
    evidence = read_json(direct / "evidence.json")
    evidence["scoring"] = {"dimensions": {"input_form": {"score": 5}}}
    write_json(direct / "evidence.json", evidence)
    dataset = read_json(direct / "dataset.json")
    dataset["evidence_sha256"] = file_sha256(direct / "evidence.json")
    write_json(direct / "dataset.json", dataset)
    with pytest.raises(ValueError, match="cannot include a benchmark assessment"):
        check_prepared(direct)


def test_direct_pilot_and_full_classification_export_item_only_provenance_without_scores(direct):
    canonical = generate_spec(direct, call=lambda **request: json.dumps(_spec(direct)))
    calls = []

    def judge(**request):
        payload = json.loads(request["user"])
        calls.append(payload)
        labels = {classifier["id"]: {
            "label": "insufficient_evidence", "evidence": [payload["item"]["content"]],
            "justification": "Offline fixture: the supplied standard is insufficient.",
        } for classifier in canonical["classifiers"]}
        labels["input_ontology"].update(matched_category_ids=[], scope_exclusion_source_ids=[])
        return json.dumps({"labels": labels})

    pilot = run(direct, limit=1, call=judge)
    assert pilot["complete"] == 1 and not pilot["full_dataset_complete"]
    assert generate_report(direct)["pending_items"] == 1
    full = run(direct, resume=True, limit=None, call=judge)
    assert full["full_dataset_complete"]
    assert len(calls) == 2
    assert all(payload["assessment_status"] == "not_run" for payload in calls)
    assert all("scoring" not in payload for payload in calls)
    summary = generate_report(direct)
    assert summary["complete_snapshot"]
    assert summary["analysis_scope"] == "item_only"
    assert summary["analysis_basis"] == "deployment_requirements"
    assert summary["assessment_status"] == "not_run"
    assert summary["original_assessment"] is None
    assert summary["unassessed_dimensions"] == ["input_form", "output_form"]
    assert summary["requirements"]["answer_requirements"] == CONTEXT["answer_requirements"]
    assert "not to a complete benchmark validity assessment" in summary["interpretation"]
    assert "overall_score" not in summary
    html = (direct / "report.html").read_text()
    assert "Benchmark assessment not run" in html
    assert "Input Form and Output Form are not assessed" in html
    assert "Fixed decision rules and sourced context" in html
    assert "<th>Original score</th>" not in html
    assert "These benchmark-level scores are retained" not in html
    for filename in ("items.csv", "review.csv"):
        with (direct / filename).open(newline="") as file:
            rows = list(csv.DictReader(file))
        # Existing blind review is preserved when later items are completed.
        assert len(rows) == (2 if filename == "items.csv" else 1)
        assert all(row["analysis_basis"] == "deployment_requirements" for row in rows)
        assert all(row["assessment_status"] == "not_run" for row in rows)
        assert all(json.loads(row["unassessed_dimensions"]) == ["input_form", "output_form"] for row in rows)
        assert all(row["direct_context_sha256"] == summary["direct_context_sha256"] for row in rows)
    assert all(row["input_ontology"] == "" for row in rows)  # Blind review remains blank.


def test_direct_report_rejects_mutated_frozen_context(direct):
    generate_spec(direct, call=lambda **request: json.dumps(_spec(direct)))
    path = direct / "direct_context.json"
    path.write_text(path.read_text() + "\n")
    with pytest.raises(ValueError, match="changed"):
        generate_report(direct)
