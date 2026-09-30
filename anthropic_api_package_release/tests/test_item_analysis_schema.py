"""Contract checks for specifications, provenance gates, and model labels."""

from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from item_analysis.schema import (  # noqa: E402
    ROSTER, SPEC_SCHEMA, allowed_labels, apply_profile_gates, labels_schema,
    validate_labels, validate_spec,
)


@pytest.fixture
def spec():
    # Checked-in copy of the peer pilot preserves its legacy source references,
    # data_then_haiku policy, and MCQ gate conflict as import-compatibility cases.
    return json.loads((Path(__file__).parent / "fixtures" / "item_analysis_spec.json").read_text())


@pytest.fixture
def profile():
    return {
        "columns": [{"name": "question", "dtype": "string"}, {"name": "subject", "dtype": "string"}],
        "available_fields": {"question": 2, "choices": 2, "answer": 2},
        "output_format": {"is_multiple_choice": True},
    }


def prediction(spec):
    return {"labels": {
        classifier["id"]: {
            "label": allowed_labels(classifier)[0],
            "evidence": ["Question asks for the probability of an event."],
            "justification": "The supplied task category covers probability calculations.",
        }
        for classifier in spec["classifiers"] if classifier["applicable"]
    }}


def test_peer_spec_import_is_lossless_and_independent(spec):
    result = validate_spec(spec, benchmark="mmlu")
    assert result == spec
    result["classifiers"][0]["category_set"].append("new")
    assert "new" not in spec["classifiers"][0]["category_set"]
    Draft202012Validator.check_schema(SPEC_SCHEMA)


@pytest.mark.parametrize("mutation", [
    lambda s: s["classifiers"].pop(),
    lambda s: s["classifiers"].__setitem__(1, deepcopy(s["classifiers"][0])),
    lambda s: s["classifiers"][0].__setitem__("id", "IO.invented"),
    lambda s: s["classifiers"][0].__setitem__("id", ["IO.task_category"]),
    lambda s: s["classifiers"][0].__setitem__("operation", "flag"),
    lambda s: s["classifiers"][0].__setitem__("aggregate", "prevalence"),
    lambda s: s["classifiers"][0].__setitem__("extra_field", "unsupported"),
    lambda s: s["classifiers"][0].__setitem__("criterion", "  "),
    lambda s: s["classifiers"][0].__setitem__("na_reason", "Not applicable despite applicable=true"),
    lambda s: s["classifiers"][0].__setitem__("category_set", ["required_without_residual"]),
    lambda s: s["classifiers"][0].__setitem__("category_set", ["math", "math", "irrelevant_other"]),
    lambda s: s["classifiers"][3].__setitem__("ordinal_anchors", {"1": "Relevant", "2": "Neutral", "4": "Wrong"}),
])
def test_invalid_specification_is_rejected(spec, mutation):
    mutation(spec)
    with pytest.raises(ValueError):
        validate_spec(spec)


def test_na_requires_reason_but_can_omit_operation_details(spec):
    classifier = spec["classifiers"][1]
    classifier.update(applicable=False, criterion="", na_reason="")
    classifier.pop("category_set")
    with pytest.raises(ValueError, match="na_reason"):
        validate_spec(spec)
    classifier["na_reason"] = "Uniform MCQ answer representation."
    validate_spec(spec)
    classifier["category_set"] = []
    validate_spec(spec)


def test_generated_sources_are_checked_against_exact_registry(spec):
    registry = {"deployment_description.txt": "Required syllabus"}
    with pytest.raises(ValueError, match="unknown evidence identifiers"):
        validate_spec(spec, evidence=registry)
    for classifier in spec["classifiers"]:
        classifier["grounded_in"] = ["deployment_description.txt"]
    validate_spec(spec, evidence=registry)


def test_benchmark_and_source_column_mismatch_fail(spec, profile):
    with pytest.raises(ValueError, match="does not match"):
        validate_spec(spec, benchmark="another-benchmark")
    spec["classifiers"][0]["label_source"] = "data_column:invented_field"
    with pytest.raises(ValueError, match="absent column"):
        validate_spec(spec, profile=profile)
    # A bad column must not disappear through source normalization.
    gated, _ = apply_profile_gates(spec, profile)
    with pytest.raises(ValueError, match="absent column"):
        validate_spec(gated, profile=profile)
    spec["classifiers"][0]["label_source"] = "data_column:subject"
    validate_spec(spec, profile=profile)


def test_mcq_gate_and_execution_adjustments_are_explicit(spec, profile):
    original = deepcopy(spec)
    result, adjustments = apply_profile_gates(spec, profile)
    assert spec == original
    assert result["classifiers"][1]["applicable"] is False
    assert result["classifiers"][1]["na_reason"]
    assert all(c["label_source"] == "haiku" for c in result["classifiers"])
    assert any(a["field"] == "applicable" and a["before"] is True and a["after"] is False for a in adjustments)
    assert any(a["field"] == "label_source" and a["before"] == "data_then_haiku" for a in adjustments)
    validate_spec(result, profile=profile)
    twice, second_adjustments = apply_profile_gates(result, profile)
    assert twice == result
    assert second_adjustments == []


def test_mixed_output_or_missing_media_does_not_disable_constructs(spec):
    result, _ = apply_profile_gates(spec, {
        "output_format": {"is_multiple_choice": False, "status": "some"},
        "has_media": True, "media_assets_loaded": False,
    })
    assert all(classifier["applicable"] for classifier in result["classifiers"])


def test_labels_require_exact_applicable_slots(spec, profile):
    spec, _ = apply_profile_gates(spec, profile)
    payload = prediction(spec)
    assert set(validate_labels(payload, spec)) == set(ROSTER) - {"OO.output_category"}
    Draft202012Validator.check_schema(labels_schema(spec))
    payload["labels"]["OO.output_category"] = {
        "label": "anything", "evidence": ["text"], "justification": "text",
    }
    with pytest.raises(ValueError):
        validate_labels(payload, spec)
    payload = prediction(spec)
    payload["labels"].pop("IC.region_fit")
    with pytest.raises(ValueError):
        validate_labels(payload, spec)


@pytest.mark.parametrize("slot,label", [
    ("IO.task_category", "invented_category"),
    ("IC.region_fit", 0),
    ("IC.region_fit", "3"),
    ("OO.value_encoding", True),
    ("OO.value_encoding", 1.0),
    ("OC.label_contestability", 2),
])
def test_invalid_label_rejected(spec, slot, label):
    payload = prediction(spec)
    payload["labels"][slot]["label"] = label
    with pytest.raises(ValueError):
        validate_labels(payload, spec)


def test_unknown_requires_explanation_and_known_requires_evidence(spec):
    payload = prediction(spec)
    value = payload["labels"]["OC.label_contestability"]
    value.update(label=None, evidence=[], justification="Reference answer is unavailable.")
    assert validate_labels(payload, spec)["OC.label_contestability"]["label"] is None
    value["justification"] = "  "
    with pytest.raises(ValueError):
        validate_labels(payload, spec)
    value.update(label=0, justification="No supported dispute.")
    with pytest.raises(ValueError):
        validate_labels(payload, spec)
