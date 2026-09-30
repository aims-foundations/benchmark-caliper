"""Exercise the preparation → Sonnet contract with real artifacts and no API."""

from copy import deepcopy
import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from item_analysis.data import file_sha256
from item_analysis.generate import generate_spec
from item_analysis.prepare import prepare


SPEC_FIXTURE = Path(__file__).parent / "fixtures" / "item_analysis_spec.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def peer_spec():
    return read(SPEC_FIXTURE)


@pytest.fixture
def source_artifacts(tmp_path, peer_spec):
    assessment = tmp_path / "assessment"
    assessment.mkdir()
    scoring = {
        "benchmark": "mmlu",
        "dimensions": {
            "input_ontology": {
                "score": 2,
                "checklist_responses": {"IO-1": "Required tasks include Indian history and mathematics."},
                "evidence": {"key/with~escapes": ["A real source excerpt."]},
            },
            "input_form": {"score": 2, "justification": "Questions are English text."},
            "output_form": {"score": 2, "justification": "Labels omit Hindi explanations."},
        },
    }
    documents = {
        "scoring.json": json.dumps(scoring),
        "deployment_description.txt": peer_spec["deployment"],
        "elicitation_summary.md": "Required categories include Indian history and mathematics.",
        "dataset_analysis_report.md": "Items first and second have answer choices. The reference answer is A.",
    }
    for name, content in documents.items():
        (assessment / name).write_text(content, encoding="utf-8")
    source = tmp_path / "items.parquet"
    pq.write_table(pa.Table.from_pylist([
        {"item_id": "first", "content": "What is one plus one?\nA. two\nB. three",
         "reference_answer": "A", "item_features": "task=math"},
        {"item_id": "second", "content": "Which subject studies past events?\nA. history\nB. geometry",
         "reference_answer": "A", "item_features": "task=history"},
    ]), source)
    return assessment, source, tmp_path / "run"


@pytest.fixture
def prepared(source_artifacts):
    assessment, source, directory = source_artifacts
    prepare(assessment, source, directory, benchmark="mmlu", seed=17,
            source_revision="test-revision", source_table="mmlu/items.parquet")
    return directory


def generation_spec(peer_spec, directory):
    result = deepcopy(peer_spec)
    registry = read(directory / "evidence.json")["registry"]
    source = "scoring.json#/dimensions/input_ontology/checklist_responses/IO-1"
    assert source in registry
    for classifier in result["classifiers"]:
        classifier["grounded_in"] = ["deployment_description.txt", source]
        classifier["example_items"] = []
    return result


class FakeCall:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, **request):
        self.calls.append(deepcopy(request))
        if not self.responses:
            raise AssertionError("Unexpected additional model call")
        result = self.responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


def test_prepare_snapshots_evidence_and_pointer_registry(prepared, source_artifacts):
    assessment, _, _ = source_artifacts
    evidence = read(prepared / "evidence.json")
    registry = evidence["registry"]
    assert registry["scoring.json#/dimensions/input_ontology/evidence/key~1with~0escapes/0"] == "A real source excerpt."
    assert "framework.yaml" in registry
    assert registry["dataset_analysis_report.md"] == (assessment / "dataset_analysis_report.md").read_text()
    assert evidence["scoring"]["dimensions"]["input_form"]["score"] == 2
    manifest = read(prepared / "dataset.json")
    assert manifest["evidence_sha256"] == file_sha256(prepared / "evidence.json")
    assert manifest["source"]["revision"] == "test-revision"
    # Editing an upstream file later does not silently alter the prepared snapshot.
    (assessment / "deployment_description.txt").write_text("Changed upstream deployment")
    assert read(prepared / "evidence.json") == evidence


def test_generated_spec_checks_references_and_uses_authoritative_profile(prepared, peer_spec):
    supplied_response = generation_spec(peer_spec, prepared)
    supplied_response["dataset_profile"] = {"row_count": 9999, "columns": ["imaginary_column"]}
    fake = FakeCall(json.dumps(supplied_response))
    result = generate_spec(prepared, call=fake)
    assert len(fake.calls) == 1
    request = fake.calls[0]
    assert request["model"] == "sonnet"
    payload = json.loads(request["user"])
    assert payload["benchmark"] == "mmlu"
    assert payload["dataset_profile"]["row_count"] == 2
    assert len(payload["example_items"]) == 2
    assert {item["item_id"] for item in payload["example_items"]} == {"first", "second"}
    assert all(item["reference_answer"] == "A" for item in payload["example_items"])
    assert set(payload["output_schema"]["required"]) == {"benchmark", "deployment", "dataset_profile", "classifiers"}
    assert "evidence_registry" in payload
    assert result["dataset_profile"] == read(prepared / "profile.json")
    assert read(prepared / "classifier_spec.original.json") == supplied_response
    assert read(prepared / "classifier_spec.json") == result
    metadata = read(prepared / "specification.json")
    assert metadata["evidence_references_checked"] is True
    assert metadata["source"]["kind"] == "generated"
    assert metadata["spec_sha256"] == file_sha256(prepared / "classifier_spec.json")
    assert any(change["field"] == "dataset_profile" for change in metadata["adjustments"])
    assert read(prepared / "generation_request.json")["user"] == request["user"]


def test_generated_deployment_drift_is_repaired_before_classification(prepared, peer_spec):
    valid = generation_spec(peer_spec, prepared)
    wrong = deepcopy(valid)
    wrong["deployment"] = "A different deployment that happens to use MMLU."
    fake = FakeCall(json.dumps(wrong), json.dumps(valid))
    generated = generate_spec(prepared, call=fake)
    assert generated["deployment"] == read(prepared / "evidence.json")["deployment"]
    assert "copy the supplied deployment text exactly" in fake.calls[1]["user"]
    assert len(fake.calls) == 2


def test_malformed_json_receives_one_repair_with_error_context(prepared, peer_spec):
    spec = generation_spec(peer_spec, prepared)
    fake = FakeCall('{"classifiers":', json.dumps(spec))
    generate_spec(prepared, call=fake)
    assert len(fake.calls) == 2
    repair = fake.calls[1]
    assert repair["step"] == "item_specification_repair"
    assert "Your previous response:" in repair["user"]
    assert '{"classifiers":' in repair["user"]
    assert "Correct these structural errors" in repair["user"]
    attempts = read(prepared / "generation_attempts.json")
    assert len(attempts) == 2
    assert "error" in attempts[0]
    assert "error" not in attempts[1]


def test_bad_evidence_references_fail_after_one_repair_and_leave_no_spec(prepared, peer_spec):
    spec = generation_spec(peer_spec, prepared)
    spec["classifiers"][0]["grounded_in"] = ["scoring.json#/invented/path"]
    fake = FakeCall(json.dumps(spec), json.dumps(spec))
    with pytest.raises(ValueError, match="after one repair"):
        generate_spec(prepared, call=fake)
    assert len(fake.calls) == 2
    assert "unknown evidence identifiers" in fake.calls[1]["user"]
    attempts = read(prepared / "generation_attempts.json")
    assert len(attempts) == 2
    assert all("scoring.json#/invented/path" in entry["error"] for entry in attempts)
    assert not (prepared / "classifier_spec.json").exists()
    assert not (prepared / "classifier_spec.original.json").exists()
    assert not (prepared / "specification.json").exists()


def test_peer_import_preserves_original_and_records_gate(prepared, peer_spec, tmp_path):
    supplied = tmp_path / "peer.json"
    supplied.write_text(json.dumps(peer_spec), encoding="utf-8")
    fake = FakeCall()
    result = generate_spec(prepared, supplied=supplied, call=fake)
    assert fake.calls == []
    assert read(prepared / "classifier_spec.original.json") == peer_spec
    assert read(supplied) == peer_spec
    output_slot = next(c for c in result["classifiers"] if c["id"] == "OO.output_category")
    assert output_slot["applicable"] is False
    assert output_slot["na_reason"]
    assert result["dataset_profile"] == read(prepared / "profile.json")
    metadata = read(prepared / "specification.json")
    assert metadata["evidence_references_checked"] is False
    assert metadata["source"]["sha256"] == file_sha256(supplied)
    assert any(change.get("id") == "OO.output_category" and change["field"] == "applicable"
               for change in metadata["adjustments"])
    assert any(change["field"] == "label_source" and change["before"] == "data_then_haiku"
               for change in metadata["adjustments"])


def test_dry_run_writes_request_without_model_call_or_spec(prepared):
    fake = FakeCall()
    result = generate_spec(prepared, dry_run=True, call=fake)
    assert result["model_calls"] == 0
    assert fake.calls == []
    request = read(prepared / "generation_request.json")
    assert json.loads(request["user"])["dataset_profile"]["row_count"] == 2
    assert not (prepared / "classifier_spec.json").exists()
    assert not (prepared / "generation_attempts.json").exists()


def test_spec_regeneration_is_rejected_before_api_call(prepared, peer_spec):
    fake = FakeCall(json.dumps(generation_spec(peer_spec, prepared)))
    generate_spec(prepared, call=fake)
    before = file_sha256(prepared / "classifier_spec.json")
    with pytest.raises(ValueError, match="already exists"):
        generate_spec(prepared, call=fake)
    assert len(fake.calls) == 1
    assert file_sha256(prepared / "classifier_spec.json") == before


def test_api_failure_is_recorded_without_structural_repair(prepared):
    fake = FakeCall(RuntimeError("provider unavailable"))
    with pytest.raises(RuntimeError, match="provider unavailable"):
        generate_spec(prepared, call=fake)
    assert len(fake.calls) == 1
    attempts = read(prepared / "generation_attempts.json")
    assert attempts[0]["kind"] == "api"
    assert not (prepared / "classifier_spec.json").exists()


@pytest.mark.parametrize("filename", ["profile.json", "evidence.json", "items.jsonl"])
def test_tampered_preparation_rejected_before_generation(prepared, filename):
    artifact = prepared / filename
    artifact.write_text(artifact.read_text() + "\n", encoding="utf-8")
    fake = FakeCall()
    with pytest.raises(ValueError, match="changed"):
        generate_spec(prepared, call=fake)
    assert fake.calls == []


def test_missing_assessment_and_benchmark_mismatch_do_not_prepare_partial_run(source_artifacts):
    assessment, source, directory = source_artifacts
    with pytest.raises(ValueError, match="does not match"):
        prepare(assessment, source, directory, benchmark="unrelated")
    assert not directory.exists()
    (assessment / "dataset_analysis_report.md").unlink()
    with pytest.raises(FileNotFoundError):
        prepare(assessment, source, directory)
    assert not directory.exists()
