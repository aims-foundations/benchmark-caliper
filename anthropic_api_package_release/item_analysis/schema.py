"""Fixed generic contracts and explicit read compatibility for historical artifacts.

Structural and source-role validation is not semantic validation of a model's
paraphrases. Specifications retain an unreviewed semantic-grounding status.
"""
from copy import deepcopy
from typing import Any, Mapping

from jsonschema import Draft202012Validator

from . import legacy_schema
from .catalog import (CATALOG_VERSION, SPEC_SCHEMA_VERSION, LEGACY_SCHEMA_VERSION,
                      LEGACY_CATALOG_VERSION, get_catalog, is_generic_spec)

ROSTER = {c["id"]: {k: c[k] for k in ("component", "operation", "aggregate")} for c in get_catalog()}
LEGACY_ROSTER = legacy_schema.ROSTER
_TEXT = {"type": "string", "minLength": 1, "pattern": r"\S"}
_TEXT_LIST = {"type": "array", "items": _TEXT}
_REFS = {**_TEXT_LIST, "uniqueItems": True}
_STATEMENT = {"type": "object", "properties": {"statement": _TEXT, "source_ids": {**_REFS, "minItems": 1}},
              "required": ["statement", "source_ids"], "additionalProperties": False}
_CONTEXT = {"type": "object", "properties": {
    **{k: {"type": "array", "items": _STATEMENT} for k in ("deployment_requirements", "benchmark_evidence", "prior_hypotheses")},
    "evidence_gaps": _TEXT_LIST,
}, "required": ["deployment_requirements", "benchmark_evidence", "prior_hypotheses", "evidence_gaps"], "additionalProperties": False}
_INVENTORY = {"type": "object", "properties": {
    "completeness": {"enum": ["complete", "partial", "unknown"]},
    "completeness_source_ids": _REFS,
    "categories": {"type": "array", "items": {"type": "object", "properties": {
        "id": _TEXT, "name": _TEXT, "definition": _TEXT, "source_ids": {**_REFS, "minItems": 1},
    }, "required": ["id", "name", "definition", "source_ids"], "additionalProperties": False}},
    "evidence_gaps": _TEXT_LIST,
}, "required": ["completeness", "completeness_source_ids", "categories", "evidence_gaps"], "additionalProperties": False,
    "if": {"properties": {"completeness": {"const": "complete"}}},
    "then": {"properties": {"completeness_source_ids": {"minItems": 1}}}}
CONTEXT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object",
    "properties": {
        "fixed_catalog_version": {"const": CATALOG_VERSION}, "benchmark": _TEXT,
        "deployment_description": _TEXT, "input_category_inventory": _INVENTORY,
        "context_by_classifier": {"type": "object", "properties": {key: _CONTEXT for key in ROSTER},
                                  "required": list(ROSTER), "additionalProperties": False},
    }, "required": ["fixed_catalog_version", "benchmark", "deployment_description", "input_category_inventory", "context_by_classifier"],
    "additionalProperties": False,
}
SPEC_SCHEMA = deepcopy(CONTEXT_SCHEMA)
SPEC_SCHEMA["properties"].update({
    "schema_version": {"const": SPEC_SCHEMA_VERSION}, "deployment": _TEXT,
    "dataset_profile": {"type": "object"}, "source_registry": {"type": "object", "minProperties": 1},
    "source_roles": {"type": "object", "additionalProperties": {"enum": ["deployment_requirement", "benchmark_evidence", "domain_evidence", "stakeholder_evidence", "prior_assessment", "rubric", "dataset_profile", "example_item", "elicitation_question", "prior_hypothesis"]}},
    "classifiers": {"const": get_catalog()},
    "semantic_validation": {"const": "unreviewed"},
    "analysis_basis": {"enum": ["benchmark_assessment", "deployment_requirements"]},
    "assessment_status": {"enum": ["complete", "not_run"]},
})
SPEC_SCHEMA["required"] += ["schema_version", "deployment", "dataset_profile", "source_registry", "source_roles", "classifiers", "semantic_validation", "analysis_basis", "assessment_status"]


def _validate_json(value: Any, schema: dict, description: str) -> None:
    errors = list(Draft202012Validator(schema).iter_errors(value))
    if errors:
        error = errors[0]
        path = ".".join(map(str, error.absolute_path)) or "<root>"
        raise ValueError(f"Invalid {description} at {path}: {error.message}")


def _references(refs, registry, roles, path, *, permitted=None):
    missing = set(refs) - set(registry)
    if missing:
        return [f"{path}: unknown evidence identifiers: {sorted(missing)}"]
    if permitted and any(roles.get(ref) not in permitted for ref in refs):
        return [f"{path}: source role cannot ground this claim; required roles: {sorted(permitted)}"]
    return []


def validate_context(context: dict, *, source_registry: Mapping[str, Any], source_roles: Mapping[str, str],
                     benchmark=None, deployment_description=None) -> dict:
    _validate_json(context, CONTEXT_SCHEMA, "context specification")
    if benchmark is not None and context["benchmark"] != benchmark:
        raise ValueError("Specification benchmark does not match prepared benchmark")
    if deployment_description is not None and context["deployment_description"] != deployment_description:
        raise ValueError("Generated deployment must copy the supplied deployment text exactly; contextual details belong in sourced statements")
    inventory = context["input_category_inventory"]
    ids = [category["id"] for category in inventory["categories"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Required category IDs must be unique")
    errors = []
    deployment_roles = {"deployment_requirement"}
    errors += _references(inventory["completeness_source_ids"], source_registry, source_roles, "inventory completeness", permitted=deployment_roles)
    for category in inventory["categories"]:
        errors += _references(category["source_ids"], source_registry, source_roles, f"category {category['id']}", permitted=deployment_roles)
    if inventory["completeness"] != "complete" and not inventory["evidence_gaps"]:
        errors.append("Incomplete or unknown inventory requires an explicit evidence gap")
    for cid, content in context["context_by_classifier"].items():
        if not content["deployment_requirements"] and not content["evidence_gaps"]:
            errors.append(f"{cid}: missing requirements require an explicit evidence gap")
        for field in ("deployment_requirements", "benchmark_evidence", "prior_hypotheses"):
            permitted = deployment_roles if field == "deployment_requirements" else None
            if field == "benchmark_evidence":
                permitted = {"benchmark_evidence", "domain_evidence", "stakeholder_evidence", "dataset_profile", "example_item", "rubric"}
            for statement in content[field]:
                errors += _references(statement["source_ids"], source_registry, source_roles, f"{cid}.{field}", permitted=permitted)
    if errors:
        raise ValueError("\n".join(errors))
    return deepcopy(context)


def join_context(context: dict, *, profile: dict, source_registry: dict, source_roles: dict,
                 analysis_basis="benchmark_assessment", assessment_status="complete") -> dict:
    context = validate_context(context, source_registry=source_registry, source_roles=source_roles)
    result = {**context, "schema_version": SPEC_SCHEMA_VERSION, "deployment": context["deployment_description"],
              "dataset_profile": deepcopy(profile), "source_registry": deepcopy(source_registry),
              "source_roles": deepcopy(source_roles), "classifiers": get_catalog(),
              "semantic_validation": "unreviewed", "analysis_basis": analysis_basis, "assessment_status": assessment_status}
    return validate_spec(result)


def validate_spec(spec: dict, *, profile=None, evidence=None, benchmark=None) -> dict:
    if not isinstance(spec, dict):
        _validate_json(spec, SPEC_SCHEMA, "classifier specification")
    if spec.get("fixed_catalog_version") in (None, LEGACY_CATALOG_VERSION) and spec.get("schema_version") in (None, LEGACY_SCHEMA_VERSION):
        legacy = deepcopy(spec)
        versions = {key: legacy.pop(key) for key in ("schema_version", "fixed_catalog_version") if key in legacy}
        return {**legacy_schema.validate_spec(legacy, profile=profile, evidence=evidence, benchmark=benchmark), **versions}
    _validate_json(spec, SPEC_SCHEMA, "classifier specification")
    if spec["deployment"] != spec["deployment_description"]:
        raise ValueError("Deployment alias differs from deployment_description")
    if (spec["analysis_basis"] == "deployment_requirements") != (spec["assessment_status"] == "not_run"):
        raise ValueError("Specification assessment provenance is inconsistent")
    if profile is not None and profile != spec["dataset_profile"]:
        raise ValueError("Specification dataset profile differs from prepared profile")
    if evidence is not None and dict(evidence) != spec["source_registry"]:
        raise ValueError("Specification source registry differs from prepared evidence")
    if set(spec["source_roles"]) != set(spec["source_registry"]):
        raise ValueError("Every registered source requires an explicit source role")
    context = {key: spec[key] for key in CONTEXT_SCHEMA["properties"]}
    validate_context(context, source_registry=spec["source_registry"], source_roles=spec["source_roles"], benchmark=benchmark)
    return deepcopy(spec)


def apply_profile_gates(spec: dict, profile: dict) -> tuple[dict, list[dict]]:
    if is_generic_spec(spec):
        return deepcopy(spec), []  # MCQ semantic categories/scoring remain relevant.
    return legacy_schema.apply_profile_gates(spec, profile)


def allowed_labels(classifier: dict) -> list[str | int]:
    return list(classifier["labels"]) if classifier["id"] in ROSTER else legacy_schema.allowed_labels(classifier)


def labels_schema(spec: dict) -> dict:
    if not is_generic_spec(spec):
        return legacy_schema.labels_schema(spec)
    category_ids = [c["id"] for c in spec["input_category_inventory"]["categories"]]
    slots = {}
    for classifier in get_catalog():
        props = {"label": {"enum": classifier["labels"]}, "evidence": {**_TEXT_LIST, "minItems": 1}, "justification": _TEXT}
        slot = {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}
        if classifier["id"] == "input_ontology":
            props.update(matched_category_ids={"type": "array", "items": {"enum": category_ids} if category_ids else False, "uniqueItems": True},
                         scope_exclusion_source_ids=_REFS)
            slot["required"] += ["matched_category_ids", "scope_exclusion_source_ids"]
            slot["allOf"] = [{"if": {"properties": {"label": {"const": "match"}}},
                              "then": {"properties": {"matched_category_ids": {"minItems": 1}}},
                              "else": {"properties": {"matched_category_ids": {"maxItems": 0}}}}]
            if spec["input_category_inventory"]["completeness"] != "complete":
                slot["allOf"].append({"if": {"properties": {"label": {"const": "no_match"}}},
                                      "then": {"properties": {"scope_exclusion_source_ids": {"minItems": 1}}}})
        slots[classifier["id"]] = slot
    return {"type": "object", "properties": {"labels": {"type": "object", "properties": slots, "required": list(slots), "additionalProperties": False}},
            "required": ["labels"], "additionalProperties": False}


def validate_labels(payload: dict, spec: dict) -> dict:
    if not is_generic_spec(spec):
        return legacy_schema.validate_labels(payload, spec)
    _validate_json(payload, labels_schema(spec), "item labels")
    _validate_scope_exclusion(payload["labels"], spec)
    return deepcopy(payload["labels"])


def classifier_labels_schema(spec: dict, classifier_id: str) -> dict:
    """Use the same judgment contract, requiring exactly one classifier."""
    if not is_generic_spec(spec) or classifier_id not in ROSTER:
        raise ValueError("A single-classifier request requires a current generic classifier ID")
    schema = labels_schema(spec)
    labels = schema["properties"]["labels"]
    labels["properties"] = {classifier_id: labels["properties"][classifier_id]}
    labels["required"] = [classifier_id]
    return schema


def _validate_scope_exclusion(labels: dict, spec: dict) -> None:
    if "input_ontology" in labels:
        errors = _references(labels["input_ontology"]["scope_exclusion_source_ids"],
                             spec["source_registry"], spec["source_roles"], "scope exclusion",
                             permitted={"deployment_requirement"})
        if errors:
            raise ValueError("\n".join(errors))


def validate_classifier_labels(payload: dict, spec: dict, classifier_id: str) -> dict:
    """Validate one response without requiring or accepting sibling judgments."""
    _validate_json(payload, classifier_labels_schema(spec, classifier_id), "classifier label")
    _validate_scope_exclusion(payload["labels"], spec)
    return deepcopy(payload["labels"])
