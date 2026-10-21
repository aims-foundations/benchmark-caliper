"""Prepare real source snapshots and fixed contextual specifications, without API calls."""
from copy import deepcopy
import json
from pathlib import Path
import re

import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from jsonschema import Draft202012Validator

from item_analysis.catalog import get_catalog
from item_analysis.data import file_sha256
from item_analysis.generate import SpecificationValidationError, generate_spec, generation_request
from item_analysis.prepare import prepare
from item_analysis.schema import CONTEXT_SCHEMA, SPEC_SCHEMA

FIXTURES = Path(__file__).parent / "fixtures"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def tagged(user, tag):
    return re.search(rf"<{tag}>\n(.*?)\n</{tag}>", user, re.S).group(1)


@pytest.fixture
def source_artifacts(tmp_path):
    context = read(FIXTURES / "item_analysis_generic_context.json")
    assessment = tmp_path / "assessment"
    assessment.mkdir()
    scoring = {"benchmark": "mmlu", "dimensions": {
        "input_ontology": {"score": 2, "evidence": {"key/with~escapes": ["A real source excerpt."]}},
        "input_form": {"score": 2, "justification": "English text."},
    }}
    documents = {
        "scoring.json": json.dumps(scoring), "deployment_description.txt": context["deployment_description"],
        "elicitation_summary.md": "The deployment includes mathematics tasks.",
        "elicitation_answers.json": json.dumps({"task": "mathematics"}),
        "dataset_analysis_report.md": "Items have answer choices and A references.",
        "benchmark.yaml": "labels: [A, B]\nscoring: exact correct option\n",
        "domain_standards.md": "One plus one equals two.",
        "stakeholder_evidence.md": "A documented teacher prefers short explanations; other teachers disagree.",
    }
    for name, text in documents.items():
        (assessment / name).write_text(text, encoding="utf-8")
    source = tmp_path / "items.parquet"
    pq.write_table(pa.Table.from_pylist([
        {"item_id": "first", "content": "What is one plus one?\nA. two\nB. three", "reference_answer": "A"},
        {"item_id": "second", "content": "What is two plus two?\nA. four\nB. three", "reference_answer": "A"},
    ]), source)
    return assessment, source, tmp_path / "run"


@pytest.fixture
def prepared(source_artifacts):
    assessment, source, directory = source_artifacts
    prepare(assessment, source, directory, benchmark="mmlu", seed=17, source_revision="test-revision", source_table="mmlu/items.parquet")
    return directory


def context_for(directory):
    context = read(FIXTURES / "item_analysis_generic_context.json")
    context["deployment_description"] = read(directory / "evidence.json")["deployment"]
    return context


class FakeCall:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, **request):
        self.calls.append(deepcopy(request))
        if not self.responses:
            raise AssertionError("Unexpected additional model call")
        value = self.responses.pop(0)
        if isinstance(value, Exception):
            raise value
        return value


def test_prepare_registers_actual_contents_roles_and_exact_pointers(prepared, source_artifacts):
    assessment, _, _ = source_artifacts
    evidence = read(prepared / "evidence.json")
    registry, roles = evidence["registry"], evidence["source_roles"]
    key = "scoring.json#/dimensions/input_ontology/evidence/key~1with~0escapes/0"
    assert registry[key] == "A real source excerpt."
    assert roles[key] == "prior_assessment"
    assert roles["dataset_analysis_report.md"] == "prior_assessment"
    for name in ("deployment_description.txt", "elicitation_answers.json", "benchmark.yaml", "domain_standards.md", "stakeholder_evidence.md"):
        assert registry[name] == (assessment / name).read_text()
    assert registry["profile.json"] == read(prepared / "profile.json")
    assert registry["items.jsonl#/0"]["item_id"] in {"first", "second"}
    assert roles["benchmark.yaml"] == "benchmark_evidence"
    assert roles["elicitation_answers.json"] == "deployment_requirement"
    assert roles["stakeholder_evidence.md"] == "stakeholder_evidence"
    manifest = read(prepared / "dataset.json")
    assert manifest["evidence_sha256"] == file_sha256(prepared / "evidence.json")
    (assessment / "deployment_description.txt").write_text("Changed upstream")
    assert read(prepared / "evidence.json") == evidence


def test_generation_uses_approved_templates_and_joins_actual_rules(prepared):
    raw = context_for(prepared)
    fake = FakeCall(json.dumps(raw))
    result = generate_spec(prepared, call=fake)
    request = fake.calls[0]
    assert request["model"] == "gpt-6-luna" and request["reasoning_effort"] == "low"
    assert tagged(request["user"], "benchmark") == "mmlu"
    registry = json.loads(tagged(request["user"], "source_registry"))
    assert registry["profile.json"]["content"]["row_count"] == 2
    assert registry["benchmark.yaml"]["role"] == "benchmark_evidence"
    assert len(json.loads(tagged(request["user"], "example_items"))) == 2
    assert "Do not classify the example items" in request["user"]
    assert "FIXED CLASSIFIER CATALOG: caliper_generic_items_v1" in request["system"]
    assert result["classifiers"] == get_catalog()
    assert all(c["applicable"] for c in result["classifiers"])
    assert result["dataset_profile"] == read(prepared / "profile.json")
    assert result["source_registry"] == read(prepared / "evidence.json")["registry"]
    assert result["semantic_validation"] == "unreviewed"
    assert read(prepared / "classifier_spec.original.json") == raw
    metadata = read(prepared / "specification.json")
    assert metadata["evidence_references_checked"] and metadata["semantic_validation"] == "unreviewed"
    assert metadata["source"]["provider"] == "openai"
    Draft202012Validator.check_schema(CONTEXT_SCHEMA)
    Draft202012Validator.check_schema(SPEC_SCHEMA)
    assert not list(Draft202012Validator(SPEC_SCHEMA).iter_errors(result))


@pytest.mark.parametrize("code", ["invalid_json", "schema", "evidence", "deployment", "task_grounding"])
def test_validation_repairs_once_and_reports_safe_category(prepared, code):
    invalid = context_for(prepared)
    private = "PRIVATE-MODEL-CONTENT-SENTINEL"
    if code == "invalid_json":
        response = '{"unfinished": "' + private
    else:
        if code == "schema":
            invalid["classifiers"] = private
        elif code == "evidence":
            invalid["input_category_inventory"]["categories"][0]["source_ids"] = [private]
        elif code == "deployment":
            invalid["deployment_description"] = private
        else:
            invalid["input_category_inventory"]["categories"][0]["source_ids"] = ["profile.json"]
        response = json.dumps(invalid)
    fake = FakeCall(response, response)
    with pytest.raises(SpecificationValidationError) as caught:
        generate_spec(prepared, call=fake)
    assert caught.value.code == code
    assert private not in caught.value.public_message and private not in str(caught.value)
    assert len(fake.calls) == 2
    assert len(read(prepared / "generation_attempts.json")) == 2
    assert not (prepared / "classifier_spec.json").exists()


def test_repair_receives_all_unknown_sources(prepared):
    valid = context_for(prepared)
    invalid = deepcopy(valid)
    for cid, context in invalid["context_by_classifier"].items():
        context["benchmark_evidence"] = [{"statement": "Unsupported", "source_ids": [cid + "_invented"]}]
    fake = FakeCall(json.dumps(invalid), json.dumps(valid))
    generate_spec(prepared, call=fake)
    assert all(cid + "_invented" in fake.calls[1]["user"] for cid in valid["context_by_classifier"])


def test_exact_deployment_copy_includes_whitespace(prepared):
    valid = context_for(prepared)
    wrong = {**valid, "deployment_description": valid["deployment_description"] + " "}
    fake = FakeCall(json.dumps(wrong), json.dumps(valid))
    generate_spec(prepared, call=fake)
    assert len(fake.calls) == 2 and "copy the supplied deployment text exactly" in fake.calls[1]["user"]


def test_legacy_import_is_rejected_without_overwriting_source(prepared):
    supplied = FIXTURES / "item_analysis_spec.json"
    before = supplied.read_bytes()
    with pytest.raises(ValueError, match="historical specifications are readable only"):
        generate_spec(prepared, supplied=supplied)
    assert supplied.read_bytes() == before and not (prepared / "classifier_spec.json").exists()


def test_imported_generic_context_has_same_reference_validation(prepared, tmp_path):
    invalid = context_for(prepared)
    invalid["input_category_inventory"]["categories"][0]["source_ids"] = ["invented"]
    path = tmp_path / "context.json"
    path.write_text(json.dumps(invalid))
    with pytest.raises(ValueError, match="unknown evidence"):
        generate_spec(prepared, supplied=path)
    path.write_text(json.dumps(context_for(prepared)))
    assert generate_spec(prepared, supplied=path)["classifiers"] == get_catalog()


def test_dry_run_and_regeneration_guard(prepared):
    assert generate_spec(prepared, dry_run=True)["model_calls"] == 0
    assert not (prepared / "classifier_spec.json").exists()
    fake = FakeCall(json.dumps(context_for(prepared)))
    generate_spec(prepared, call=fake)
    before = file_sha256(prepared / "classifier_spec.json")
    with pytest.raises(ValueError, match="already exists"):
        generate_spec(prepared, call=fake)
    assert len(fake.calls) == 1 and before == file_sha256(prepared / "classifier_spec.json")


def test_api_failure_is_recorded_without_structural_repair(prepared):
    fake = FakeCall(RuntimeError("provider unavailable"))
    with pytest.raises(RuntimeError):
        generate_spec(prepared, call=fake)
    assert len(fake.calls) == 1 and read(prepared / "generation_attempts.json")[0]["kind"] == "api"


@pytest.mark.parametrize("filename", ["profile.json", "evidence.json", "items.jsonl"])
def test_tampered_preparation_rejected_before_generation(prepared, filename):
    path = prepared / filename
    path.write_text(path.read_text() + "\n")
    with pytest.raises(ValueError, match="changed"):
        generate_spec(prepared, call=FakeCall())


def test_supplemental_sources_and_absent_evidence_gaps(source_artifacts):
    assessment, source, directory = source_artifacts
    for name in ("domain_standards.md", "stakeholder_evidence.md"):
        (assessment / name).unlink()
    supplemental = {"standard:exam": {"role": "domain_evidence", "content": "The supplied actual standard text."}}
    (assessment / "source_registry.json").write_text(json.dumps(supplemental))
    prepare(assessment, source, directory)
    evidence = read(directory / "evidence.json")
    assert evidence["registry"]["standard:exam"] == "The supplied actual standard text."
    assert any("stakeholder" in gap for gap in evidence["evidence_gaps"])
    result = generate_spec(directory, call=FakeCall(json.dumps(context_for(directory))))
    assert any("stakeholder" in gap for gap in result["context_by_classifier"]["output_content"]["evidence_gaps"])


def test_generated_output_cannot_supply_code_managed_fields_but_reviewed_import_can(prepared, tmp_path):
    from item_analysis.schema import join_context
    evidence = read(prepared / "evidence.json")
    effective = join_context(context_for(prepared), profile=read(prepared / "profile.json"),
                             source_registry=evidence["registry"], source_roles=evidence["source_roles"])
    fake = FakeCall(json.dumps(effective), json.dumps(effective))
    with pytest.raises(SpecificationValidationError):
        generate_spec(prepared, call=fake)
    assert not (prepared / "classifier_spec.json").exists()
    path = tmp_path / "reviewed.json"
    path.write_text(json.dumps(effective))
    imported = generate_spec(prepared, supplied=path)
    assert imported["classifiers"] == get_catalog()


@pytest.mark.parametrize("root", [[], "text", None])
def test_wrong_json_root_is_repaired_as_validation_failure(prepared, root):
    fake = FakeCall(json.dumps(root), json.dumps(context_for(prepared)))
    assert generate_spec(prepared, call=fake)["classifiers"] == get_catalog()
    assert len(fake.calls) == 2
