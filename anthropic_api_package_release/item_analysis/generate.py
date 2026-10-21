"""Prepare sourced context once, then join it to the immutable classifier catalog."""

from itertools import islice
import json
from pathlib import Path

from .data import file_sha256, read_items
from .model_client import MODEL_ID, PROVIDER, REASONING_EFFORT
from .schema import (CONTEXT_SCHEMA, CATALOG_VERSION, SPEC_SCHEMA_VERSION, is_generic_spec,
                     join_context, validate_context, validate_spec)
from .storage import check_prepared, parse_response, read_json, run_lock, write_json

PROMPT_PATH = Path(__file__).parent / "prompts" / "generate_spec.md"
USER_PROMPT_PATH = PROMPT_PATH.with_name("generate_user.md")


_VALIDATION_MESSAGES = {
    "invalid_json": "The model returned invalid JSON after one repair. No items were classified; start a new analysis to prepare the context again.",
    "schema": "The model returned context that still failed the required format after one repair. No items were classified; start a new analysis.",
    "evidence": "The generated contextual specification cited evidence outside the supplied context after one repair. No items were classified; start a new analysis.",
    "deployment": "The generated contextual specification changed the supplied deployment text after one repair. No items were classified; start a new analysis.",
    "provenance": "The generated contextual specification misstated whether a benchmark assessment was run after one repair. No items were classified; start a new analysis.",
    "task_grounding": "The generated task categories did not cite your task requirements after one repair. No items were classified; start a new analysis.",
}


class SpecificationValidationError(ValueError):
    """Exhausted structural repair with a fixed, context-free public diagnostic."""

    def __init__(self, *, code="schema"):
        self.code = code if isinstance(code, str) and code in _VALIDATION_MESSAGES else "schema"
        self.public_message = _VALIDATION_MESSAGES[self.code]
        super().__init__("Specification failed validation after one repair; inspect generation_attempts.json")


def _validation_code(error: ValueError) -> str:
    """Classify validator-owned prefixes without exposing arbitrary model text."""
    message = str(error)
    if isinstance(error, json.JSONDecodeError) or message == "Expected JSON or one complete JSON code block":
        return "invalid_json"
    if message.startswith("Generated deployment must copy"):
        return "deployment"
    if message.startswith(("Invalid context specification at ", "Invalid classifier specification at ")):
        return "schema"
    if "unknown evidence identifiers:" in message:
        return "evidence"
    if "source role cannot ground this claim" in message:
        return "task_grounding"
    return "schema"


def generation_request(directory: Path, max_tokens=12000, *, model_id=MODEL_ID,
                       reasoning_effort=REASONING_EFFORT) -> dict:
    dataset = check_prepared(directory)
    evidence = read_json(directory / "evidence.json")
    registry = evidence["registry"]
    roles = evidence.get("source_roles")
    if not roles:
        raise ValueError("Prepared evidence predates generic sourced context; prepare a new run directory")
    values = {
        "benchmark": dataset["benchmark"], "deployment_description": evidence["deployment"],
        "original_rubric": registry["framework.yaml"],
        "source_registry_json": json.dumps({key: {"role": roles[key], "content": content} for key, content in registry.items()}, ensure_ascii=False, allow_nan=False),
        "dataset_profile_json": json.dumps(read_json(directory / "profile.json"), ensure_ascii=False, allow_nan=False),
        "example_items_json": json.dumps(list(islice(read_items(directory / "items.jsonl"), 8)), ensure_ascii=False, allow_nan=False),
    }
    # One substitution pass: supplied documents cannot inject template tokens.
    import re
    user = re.sub(r"{{([a-z_]+)}}", lambda match: values[match.group(1)], USER_PROMPT_PATH.read_text(encoding="utf-8"))
    return {
        "model": model_id, "reasoning_effort": reasoning_effort,
        "system": PROMPT_PATH.read_text(encoding="utf-8"), "user": user,
        "max_tokens": max_tokens, "step": "item_specification",
    }


def _save_spec(directory, raw_spec, *, source):
    dataset = check_prepared(directory)
    profile = read_json(directory / "profile.json")
    evidence = read_json(directory / "evidence.json")
    direct = evidence.get("analysis_basis") == "deployment_requirements"
    if not is_generic_spec(raw_spec):
        raise ValueError("New runs require caliper_generic_items_v1 contextual specifications; historical specifications are readable only")
    if "schema_version" in raw_spec and source.get("kind") == "provided":
        # A supplied effective spec is accepted only when its full catalog,
        # profile, deployment and registered sources match this prepared run.
        checked = validate_spec(raw_spec, profile=profile, evidence=evidence["registry"], benchmark=dataset["benchmark"])
        context = {key: checked[key] for key in CONTEXT_SCHEMA["properties"]}
        if checked["source_roles"] != evidence["source_roles"]:
            raise ValueError("Imported source roles differ from prepared evidence")
    else:
        context = raw_spec
    context = validate_context(context, source_registry=evidence["registry"], source_roles=evidence["source_roles"],
                               benchmark=dataset["benchmark"], deployment_description=evidence["deployment"])
    adjustments = []
    # Deterministic availability gaps cannot disappear in generated prose.
    for cid, content in context["context_by_classifier"].items():
        for gap in evidence.get("evidence_gaps", []):
            if gap not in content["evidence_gaps"]:
                content["evidence_gaps"].append(gap)
                adjustments.append({"classifier": cid, "field": "evidence_gaps", "added": gap,
                                    "reason": "Preserve deterministic source availability gap"})
    canonical = join_context(context, profile=profile, source_registry=evidence["registry"], source_roles=evidence["source_roles"],
                             analysis_basis="deployment_requirements" if direct else "benchmark_assessment",
                             assessment_status="not_run" if direct else "complete")
    write_json(directory / "classifier_spec.original.json", raw_spec)
    write_json(directory / "classifier_spec.json", canonical)
    metadata = {
        "schema_version": SPEC_SCHEMA_VERSION, "fixed_catalog_version": CATALOG_VERSION,
        "source": source, "adjustments": adjustments, "evidence_references_checked": True,
        "deployment_text_matches": True, "semantic_validation": "unreviewed",
        "note": "Structure, immutable catalog, source IDs and source roles checked; semantic grounding remains unreviewed and requires human review.",
        "spec_sha256": file_sha256(directory / "classifier_spec.json"),
        "dataset_sha256": file_sha256(directory / "dataset.json"),
    }
    if direct:
        metadata.update(analysis_basis="deployment_requirements", assessment_status="not_run",
                        unassessed_dimensions=["input_form", "output_form"])
        metadata["note"] += " No benchmark assessment was run; Input Form and Output Form are not assessed."
    write_json(directory / "specification.json", metadata)
    return canonical


def generate_spec(directory: Path, *, supplied: Path | None = None, dry_run=False,
                  max_tokens=12000, call=None, model_id=MODEL_ID, provider=PROVIDER,
                  reasoning_effort=REASONING_EFFORT) -> dict:
    """At most one repair call for structural failures; never repair cultural judgments."""
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    with run_lock(directory):
        check_prepared(directory)
        if (directory / "classifier_spec.json").exists() or (directory / "run.json").exists():
            raise ValueError("A specification already exists; prepare a new directory for changed criteria")
        if supplied is not None:
            if dry_run:
                raise ValueError("Use --dry-run to preview specification generation, or --spec to import; choose one")
            return _save_spec(directory, read_json(supplied), source={
                "kind": "provided", "path": str(supplied.resolve()), "sha256": file_sha256(supplied),
            })
        request = generation_request(directory, max_tokens, model_id=model_id,
                                     reasoning_effort=reasoning_effort)
        write_json(directory / "generation_request.json", request)
        if dry_run:
            return {"status": "preview", "request": "generation_request.json", "model_calls": 0}
        if call is None:
            raise ValueError("Specification generation requires an API client; use --dry-run to inspect the request")
        attempts = []
        for attempt in range(2):
            current = dict(request)
            if attempt:
                current["user"] += "\n\nYour previous response:\n" + attempts[-1]["response"]
                current["user"] += "\n\nCorrect these structural errors and return the full JSON:\n" + attempts[-1]["error"]
                current["step"] = "item_specification_repair"
            try:
                raw = call(**current)
            except Exception as exc:
                attempts.append({"attempt": attempt + 1, "error": f"{type(exc).__name__}: {exc}", "kind": "api"})
                write_json(directory / "generation_attempts.json", attempts)
                raise
            entry = {"attempt": attempt + 1, "response": raw}
            try:
                result = _save_spec(directory, parse_response(raw), source={
                    "kind": "generated", "provider": provider, "model": model_id,
                    "model_id": model_id, "reasoning_effort": reasoning_effort,
                    "max_tokens": max_tokens,
                })
            except ValueError as exc:
                entry["error"] = str(exc)
                attempts.append(entry)
                write_json(directory / "generation_attempts.json", attempts)
                if attempt:
                    raise SpecificationValidationError(code=_validation_code(exc)) from exc
            else:
                attempts.append(entry)
                write_json(directory / "generation_attempts.json", attempts)
                return result
    raise AssertionError("Unreachable specification generation state")
