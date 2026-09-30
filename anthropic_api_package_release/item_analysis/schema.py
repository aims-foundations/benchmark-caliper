"""Contracts for the fixed classifier roster and its item-level labels.

Validation never changes an input artifact. Dataset gates and the explicit
model-based execution policy are applied separately and return an audit trail.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from jsonschema import Draft202012Validator


ROSTER = {
    "IO.task_category": {
        "component": "input_ontology", "operation": "assignment",
        "aggregate": "coverage_vs_required",
    },
    "OO.output_category": {
        "component": "output_ontology", "operation": "assignment",
        "aggregate": "category_distribution",
    },
    "OO.value_encoding": {
        "component": "output_ontology", "operation": "flag",
        "aggregate": "prevalence",
    },
    "IC.region_fit": {
        "component": "input_content", "operation": "ordinal",
        "aggregate": "category_distribution",
    },
    "OC.label_contestability": {
        "component": "output_content", "operation": "flag",
        "aggregate": "prevalence",
    },
}

_TEXT = {"type": "string", "minLength": 1, "pattern": r"\S"}
_TEXT_LIST = {"type": "array", "items": _TEXT}
_COMMON_FIELDS = {
    "id": {"enum": list(ROSTER)},
    "component": {"type": "string"},
    "operation": {"enum": ["assignment", "flag", "ordinal"]},
    "applicable": {"type": "boolean"},
    "na_reason": {"type": "string"},
    "criterion": {"type": "string"},
    "label_source": {
        "type": "string",
        # Accept the original pilot's provider-specific labels on import.
        "pattern": r"^(model|data_then_model|haiku|data_then_haiku|data_column:[^\s:]+)$",
    },
    "grounded_in": {**_TEXT_LIST, "uniqueItems": True},
    "example_items": _TEXT_LIST,
    "aggregate": {"type": "string"},
}


def _slot_schema(slot_id: str, definition: dict) -> dict:
    fields = deepcopy(_COMMON_FIELDS)
    fields.update({name: {"const": value} for name, value in definition.items()})
    fields["id"] = {"const": slot_id}
    operation = definition["operation"]
    if operation == "assignment":
        operation_field = "category_set"
        fields[operation_field] = {
            **_TEXT_LIST, "uniqueItems": True,
        }
        operation_requirement = {"minItems": 1}
        if slot_id == "IO.task_category":
            operation_requirement.update({
                "minItems": 2, "contains": {"const": "irrelevant_other"},
            })
    elif operation == "ordinal":
        operation_field = "ordinal_anchors"
        fields[operation_field] = {
            "type": "object", "properties": {str(i): _TEXT for i in (1, 2, 3)},
            "additionalProperties": False,
        }
        operation_requirement = {"required": ["1", "2", "3"]}
    else:
        operation_field = "positive_class"
        fields[operation_field] = {"type": "string"}
        operation_requirement = _TEXT
    return {
        "type": "object", "properties": fields,
        "required": list(_COMMON_FIELDS), "additionalProperties": False,
        "if": {"properties": {"applicable": {"const": True}}},
        "then": {
            "required": [operation_field],
            "properties": {
                "criterion": _TEXT, "na_reason": {"const": ""},
                "grounded_in": {"minItems": 1},
                operation_field: operation_requirement,
            },
        },
        "else": {"properties": {"na_reason": _TEXT}},
    }


SPEC_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "benchmark": _TEXT,
        "deployment": _TEXT,
        # The profile can contain the complete deterministic counts/dtypes or
        # the older pilot's summary. Runtime gates use the actual profile.
        "dataset_profile": {"type": "object"},
        "classifiers": {
            "type": "array", "minItems": len(ROSTER), "maxItems": len(ROSTER),
            "items": {"oneOf": [_slot_schema(i, d) for i, d in ROSTER.items()]},
        },
    },
    "required": ["benchmark", "deployment", "dataset_profile", "classifiers"],
    "additionalProperties": False,
}


def _validate_json(value: Any, schema: dict, description: str) -> None:
    errors = list(Draft202012Validator(schema).iter_errors(value))
    if errors:
        error = errors[0]
        path = ".".join(map(str, error.absolute_path)) or "<root>"
        # oneOf failures otherwise echo an entire long classifier prompt. Pick
        # errors from the matching slot so repair feedback remains readable.
        if error.validator == "oneOf" and isinstance(error.instance, dict):
            slot_id = error.instance.get("id")
            if isinstance(slot_id, str) and slot_id in ROSTER:
                slot_errors = list(Draft202012Validator(
                    _slot_schema(slot_id, ROSTER[slot_id])
                ).iter_errors(error.instance))
                if slot_errors:
                    error = slot_errors[0]
                    suffix = ".".join(map(str, error.absolute_path))
                    path += f".{suffix}" if suffix else ""
        raise ValueError(f"Invalid {description} at {path}: {error.message}")


def _profile_columns(profile: dict) -> set[str]:
    columns = {
        column if isinstance(column, str) else column.get("name")
        for column in profile.get("columns", [])
        if isinstance(column, (str, dict))
    }
    columns.update(profile.get("available_fields", {}))
    return {name for name in columns if isinstance(name, str)}


def validate_spec(
    spec: dict, *, profile: dict | None = None,
    evidence: Mapping[str, Any] | None = None, benchmark: str | None = None,
) -> dict:
    """Validate a spec and return a detached copy in roster order.

    ``evidence`` is an optional registry of exact source identifiers. Supply it
    for generated specifications. Omit it when importing the pilot artifact:
    its historical free-text citations are preserved, not claimed verified.
    ``profile`` validates explicit data-column references against real fields.
    """
    _validate_json(spec, SPEC_SCHEMA, "classifier specification")
    by_id = {classifier["id"]: classifier for classifier in spec["classifiers"]}
    if set(by_id) != set(ROSTER):
        missing = sorted(set(ROSTER) - set(by_id))
        raise ValueError(f"Each classifier must appear exactly once; missing: {missing}")
    if benchmark is not None and spec["benchmark"] != benchmark:
        raise ValueError(
            f"Specification benchmark {spec['benchmark']!r} does not match {benchmark!r}"
        )
    columns = _profile_columns(profile) if profile is not None else None
    reference_errors = []
    for classifier in spec["classifiers"]:
        slot_id = classifier["id"]
        source = classifier["label_source"]
        if source.startswith("data_column:") and columns is not None:
            column = source.split(":", 1)[1]
            if column not in columns:
                raise ValueError(f"{slot_id}: label_source references absent column {column!r}")
        if evidence is not None:
            missing_refs = sorted(set(classifier["grounded_in"]) - set(evidence))
            if missing_refs:
                reference_errors.append(f"{slot_id}: unknown evidence identifiers: {missing_refs}")
    if reference_errors:
        # One structural repair must see every invalid reference, not just the
        # first slot; all references remain subject to the same exact-key check.
        raise ValueError("\n".join(reference_errors))
    result = deepcopy(spec)
    result["classifiers"] = [deepcopy(by_id[slot_id]) for slot_id in ROSTER]
    return result


def apply_profile_gates(spec: dict, profile: dict) -> tuple[dict, list[dict]]:
    """Apply observable gates and return explicit changes alongside a copy.

    MCQs have a uniform answer representation, so output-category assignment is
    N/A under SPEC.md. This release runs every applicable slot through the model;
    source-column suggestions in older artifacts are recorded before conversion.
    Mixed/media items retain their slots: missing evidence becomes an item-level
    unknown, not a benchmark-wide claim that the construct is inapplicable.
    """
    result = deepcopy(spec)
    adjustments = []
    if not isinstance(result, dict) or not isinstance(result.get("classifiers"), list):
        return result, adjustments
    is_mcq = profile.get("output_format", {}).get("is_multiple_choice", profile.get("is_mcq")) is True
    for classifier in result["classifiers"]:
        if not isinstance(classifier, dict):
            continue
        slot_id = classifier.get("id")
        if slot_id == "OO.output_category" and is_mcq:
            reason = (
                "Fixed-choice items have a uniform answer representation; "
                "SPEC.md keeps output-category assignment at benchmark level."
            )
            for field, value in (("applicable", False), ("na_reason", reason)):
                if classifier.get(field) != value:
                    adjustments.append({
                        "id": slot_id, "field": field, "before": classifier.get(field),
                        "after": value, "reason": "MCQ output-uniformity gate",
                    })
                    classifier[field] = value
        source = classifier.get("label_source")
        known_column = (
            isinstance(source, str) and source.startswith("data_column:")
            and source.split(":", 1)[1] in _profile_columns(profile)
        )
        if source in ("haiku", "data_then_haiku", "data_then_model") or known_column:
            adjustments.append({
                "id": slot_id, "field": "label_source", "before": source, "after": "model",
                "reason": "This implementation evaluates every applicable classifier with the configured model.",
            })
            classifier["label_source"] = "model"
    return result, adjustments


def allowed_labels(classifier: dict) -> list[str | int]:
    """Return substantive labels; ``None`` is always the separate unknown state."""
    operation = classifier["operation"]
    if operation == "assignment":
        return list(classifier["category_set"])
    return [0, 1] if operation == "flag" else [1, 2, 3]


def labels_schema(spec: dict) -> dict:
    """Build the per-item response schema from the frozen specification."""
    slots = {}
    for classifier in spec["classifiers"]:
        if not classifier["applicable"]:
            continue
        slots[classifier["id"]] = {
            "type": "object",
            "properties": {
                "label": {"enum": [*allowed_labels(classifier), None]},
                "evidence": _TEXT_LIST,
                "justification": _TEXT,
            },
            "required": ["label", "evidence", "justification"],
            "additionalProperties": False,
            "if": {"properties": {"label": {"type": "null"}}},
            "else": {"properties": {"evidence": {"minItems": 1}}},
        }
    return {
        "type": "object", "properties": {
            "labels": {
                "type": "object", "properties": slots, "required": list(slots),
                "additionalProperties": False,
            },
        }, "required": ["labels"], "additionalProperties": False,
    }


def validate_labels(payload: dict, spec: dict) -> dict:
    """Validate all and only applicable labels, returning a detached label map."""
    _validate_json(payload, labels_schema(spec), "item labels")
    # JSON Schema's enum implementation rejects booleans; retain an explicit
    # guard as Python considers True == 1 and downstream tallies must not.
    for slot_id, value in payload["labels"].items():
        if isinstance(value["label"], bool):
            raise ValueError(f"{slot_id}: label must not be boolean")
        if isinstance(value["label"], float):
            raise ValueError(f"{slot_id}: numeric label must be an integer")
    return deepcopy(payload["labels"])
