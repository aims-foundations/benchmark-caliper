"""One six-dimension assessment per item, using shared, frozen source context."""

from copy import deepcopy
from itertools import islice
import json
import os
from pathlib import Path

from .data import file_sha256, read_items
from .model_client import MODEL_ID, PROVIDER, REASONING_EFFORT
from .storage import check_prepared, check_specification, parse_response, read_json, run_lock, text_hash, write_json

CONTEXT_SCHEMA_VERSION = "caliper_item_context_v1"
RUBRIC_VERSION = "caliper_item_rubric_v1"
RESULT_SCHEMA_VERSION = "caliper_item_result_v4"
REQUEST_SCHEMA_VERSION = "caliper_item_scoring_request_v1"
PROMPT_PATH = Path(__file__).parent / "prompts" / "assess_item.md"
DIMENSIONS = (
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
)
SOURCE_ROLES = frozenset({
    "deployment_requirement", "benchmark_evidence", "domain_evidence", "stakeholder_evidence",
    "elicitation_question",
})
ANCHORS = {
    "1": "Fundamental mismatch with the deployment requirement.",
    "2": "Substantial mismatch that requires major changes.",
    "3": "Partial alignment with material limitations.",
    "4": "Strong alignment with minor limitations.",
    "5": "Strong alignment supported by explicit evidence.",
}
QUESTIONS = (
    "Does this item test a task or capability relevant to the deployment?",
    "Does this item's concrete question or scenario fit the deployment's users, language, and domain?",
    "Does this item's input modality and representation match deployment inputs?",
    "Do this item's expected decisions and grading criteria capture success in the deployment?",
    "Is this item's reference answer or expected judgment appropriate for the deployment?",
    "Does this item's expected response format or modality match deployment needs?",
)


def dimension_descriptors() -> list[dict]:
    """Return detached, fixed descriptors for the existing website transport."""
    return [{"id": cid, "component": cid.replace("_", " ").title(),
             "operation": "ordinal", "applicable": True, "question": question,
             "ordinal_anchors": deepcopy(ANCHORS)}
            for cid, question in zip(DIMENSIONS, QUESTIONS)]


_JUDGMENT_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["score", "justification", "evidence", "information_gaps"],
    "properties": {
        "score": {"type": ["integer", "null"], "minimum": 1, "maximum": 5},
        "justification": {"type": "string", "minLength": 1},
        "evidence": {"type": "array", "items": {"type": "string", "minLength": 1}},
        "information_gaps": {"type": "array", "items": {"type": "string", "minLength": 1}},
    },
    "allOf": [{"if": {"properties": {"score": {"type": "null"}}},
               "then": {"properties": {"information_gaps": {"minItems": 1}}},
               "else": {"properties": {"evidence": {"minItems": 1}}}}],
}
OUTPUT_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["dimensions"],
    "properties": {"dimensions": {
        "type": "object", "additionalProperties": False, "required": list(DIMENSIONS),
        "properties": {cid: deepcopy(_JUDGMENT_SCHEMA) for cid in DIMENSIONS},
    }},
}


def is_score_spec(spec) -> bool:
    return isinstance(spec, dict) and spec.get("analysis_type") == "six_scores"


def validate_score_spec(spec, *, profile=None, benchmark=None) -> dict:
    if (not is_score_spec(spec) or spec.get("schema_version") != CONTEXT_SCHEMA_VERSION
            or spec.get("rubric_version") != RUBRIC_VERSION):
        raise ValueError("Invalid six-score context or rubric version")
    if spec.get("classifiers") != dimension_descriptors():
        raise ValueError("The fixed six-dimension rubric cannot change within a run")
    for field in ("benchmark", "deployment", "deployment_description"):
        if not isinstance(spec.get(field), str) or not spec[field].strip():
            raise ValueError(f"Six-score context requires nonempty {field}")
    if spec["deployment"] != spec["deployment_description"]:
        raise ValueError("Six-score deployment text must be preserved exactly")
    if benchmark is not None and spec["benchmark"] != benchmark:
        raise ValueError("Six-score context benchmark differs from prepared data")
    if not isinstance(spec.get("dataset_profile"), dict):
        raise ValueError("Six-score context requires the prepared dataset profile")
    if profile is not None and spec["dataset_profile"] != profile:
        raise ValueError("Six-score context dataset profile changed")
    registry, roles = spec.get("source_registry"), spec.get("source_roles")
    if not isinstance(registry, dict) or not isinstance(roles, dict) or registry.keys() != roles.keys():
        raise ValueError("Six-score context requires matching source registry and roles")
    if any(role not in SOURCE_ROLES or key.startswith("scoring.json") for key, role in roles.items()):
        raise ValueError("Prior assessments and hypotheses cannot ground item scores")
    provenance = (spec.get("analysis_basis"), spec.get("assessment_status"))
    if provenance not in {("deployment_requirements", "not_run"), ("benchmark_assessment", "complete")}:
        raise ValueError("Invalid six-score context provenance")
    return spec


def prepare_context(directory: Path, *, dry_run=False) -> dict:
    """Assemble shared evidence without a model call or generated classifiers."""
    directory = Path(directory)
    with run_lock(directory):
        dataset = check_prepared(directory)
        if (directory / "classifier_spec.json").exists() or (directory / "run.json").exists():
            raise ValueError("A context already exists; prepare a new directory for changed criteria")
        evidence = read_json(directory / "evidence.json")
        registry = evidence.get("registry", {})
        from .prepare import source_role
        roles = evidence.get("source_roles") or {key: source_role(key) for key in registry}
        # Exclude benchmark scores and model-written hypotheses, the original
        # benchmark-wide rubric, and example items belonging to other records.
        retained = {key: deepcopy(value) for key, value in registry.items()
                    if roles.get(key) in SOURCE_ROLES and not key.startswith("scoring.json")}
        direct = evidence.get("analysis_basis") == "deployment_requirements"
        spec = {
            "schema_version": CONTEXT_SCHEMA_VERSION, "analysis_type": "six_scores",
            "rubric_version": RUBRIC_VERSION, "benchmark": dataset["benchmark"],
            "deployment": evidence["deployment"], "deployment_description": evidence["deployment"],
            "analysis_basis": "deployment_requirements" if direct else "benchmark_assessment",
            "assessment_status": "not_run" if direct else "complete",
            "source_registry": retained, "source_roles": {key: roles[key] for key in retained},
            "dataset_profile": read_json(directory / "profile.json"),
            "evidence_gaps": deepcopy(evidence.get("evidence_gaps", [])),
            "classifiers": dimension_descriptors(),
        }
        validate_score_spec(spec)
        if not dry_run:
            write_json(directory / "classifier_spec.json", spec)
            write_json(directory / "specification.json", {
                "schema_version": CONTEXT_SCHEMA_VERSION, "analysis_type": "six_scores",
                "rubric_version": RUBRIC_VERSION, "source": {"kind": "deterministic"},
                "analysis_basis": spec["analysis_basis"], "assessment_status": spec["assessment_status"],
                "evidence_references_checked": True, "deployment_text_matches": True,
                "semantic_validation": "unreviewed", "adjustments": [],
                "note": "Shared source context assembled without a model call. Item scores require human review for semantic grounding.",
                "excluded_source_ids": [key for key in registry if key not in retained],
                "spec_sha256": file_sha256(directory / "classifier_spec.json"),
                "dataset_sha256": file_sha256(directory / "dataset.json"),
            })
        return spec


def validate_dimensions(payload) -> dict:
    """Reject incomplete/malformed judgments; missing evidence is not a low score."""
    if not isinstance(payload, dict) or set(payload) != {"dimensions"}:
        raise ValueError("Response must contain only dimensions")
    dimensions = payload["dimensions"]
    if not isinstance(dimensions, dict) or set(dimensions) != set(DIMENSIONS):
        raise ValueError("Response must assess all six dimensions exactly once")
    for cid, judgment in dimensions.items():
        if not isinstance(judgment, dict) or set(judgment) != {"score", "justification", "evidence", "information_gaps"}:
            raise ValueError(f"{cid}: expected score, justification, evidence and information_gaps")
        score = judgment["score"]
        if score is not None and (type(score) is not int or not 1 <= score <= 5):
            raise ValueError(f"{cid}: score must be an integer 1–5 or null")
        if not isinstance(judgment["justification"], str) or not judgment["justification"].strip():
            raise ValueError(f"{cid}: justification must be nonempty text")
        for field in ("evidence", "information_gaps"):
            values = judgment[field]
            if not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values):
                raise ValueError(f"{cid}: {field} must be an array of nonempty strings")
        if score is not None and not judgment["evidence"]:
            raise ValueError(f"{cid}: a numerical score requires supporting evidence")
        if score is None and not judgment["information_gaps"]:
            raise ValueError(f"{cid}: an unknown score requires information gaps")
    return dimensions


def scoring_request(item, spec, deployment=None, *, prompt=None, max_tokens=4096,
                    model_id=MODEL_ID, reasoning_effort=REASONING_EFFORT) -> dict:
    validate_score_spec(spec)
    if deployment is not None and deployment != spec["deployment"]:
        raise ValueError("Scoring deployment differs from the prepared shared context")
    payload = {
        **{key: value for key, value in spec.items() if key != "deployment"},
        "request_schema_version": REQUEST_SCHEMA_VERSION,
        "item": item, "output_schema": OUTPUT_SCHEMA,
    }
    return {"model": model_id, "reasoning_effort": reasoning_effort,
            "system": prompt if prompt is not None else PROMPT_PATH.read_text(encoding="utf-8"),
            "user": json.dumps(payload, ensure_ascii=False, allow_nan=False),
            "max_tokens": max_tokens, "step": "item_scoring"}


def check_result_progress(record: dict, previous: dict | None = None) -> None:
    """Validate saved whole-item checkpoints, including cumulative retry history."""
    if (record.get("schema_version") != RESULT_SCHEMA_VERSION
            or record.get("analysis_type") != "six_scores"):
        raise ValueError("Saved result schema changed; prepare a new run directory")
    attempts = record.get("attempts")
    if (not isinstance(attempts, list) or not attempts
            or any(not isinstance(entry, dict) or type(entry.get("attempt")) is not int
                   or entry["attempt"] != index + 1 for index, entry in enumerate(attempts))):
        raise ValueError("Invalid saved scoring attempts")
    for entry in attempts:
        if (not isinstance(entry.get("response"), str)
                and not (entry.get("kind") == "api" and isinstance(entry.get("error"), str))):
            raise ValueError("Invalid saved scoring attempt response")
    if record.get("status") == "complete":
        validate_dimensions({"dimensions": record.get("dimensions")})
        if "error" in record:
            raise ValueError("Completed scores cannot also be an operational error")
    elif record.get("status") == "error":
        if record.get("dimensions") != {} or not isinstance(record.get("error"), str) or not record["error"].strip():
            raise ValueError("A failed scoring request requires an error and no dimension judgments")
    else:
        raise ValueError("Invalid six-score item status")
    if previous:
        if previous.get("schema_version") != RESULT_SCHEMA_VERSION:
            raise ValueError("Result versions cannot change within an item")
        if previous.get("status") == "complete":
            raise ValueError(f"Duplicate completed result for {record['item_id']}")
        history = previous["attempts"]
        if attempts[:len(history)] != history or len(attempts) <= len(history):
            raise ValueError("Saved scoring attempts cannot change or disappear")


def run(directory: Path, *, limit=100, resume=False, dry_run=False, max_tokens=4096,
        call=None, model_id=MODEL_ID, provider=PROVIDER, reasoning_effort=REASONING_EFFORT,
        on_result=None, should_stop=None) -> dict:
    """Score once per selected item, repairing structure at most once per attempt.

    Completed items are immutable. Resume retries failed items and may grow the
    selection; all scoring inputs, prompts, and model settings remain frozen.
    """
    from .classify import read_results

    directory = Path(directory)
    if (limit is not None and (type(limit) is not int or limit <= 0)) or type(max_tokens) is not int or max_tokens <= 0:
        raise ValueError("limit and max_tokens must be positive integers")
    with run_lock(directory):
        dataset = check_prepared(directory)
        metadata = check_specification(directory)
        spec = validate_score_spec(read_json(directory / "classifier_spec.json"),
                                   profile=read_json(directory / "profile.json"), benchmark=dataset["benchmark"])
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
        target = dataset["item_count"] if limit is None else min(limit, dataset["item_count"])
        selected = lambda: islice(read_items(directory / "items.jsonl"), target)
        selected_ids = [item["item_id"] for item in selected()]
        if dry_run:
            if resume:
                raise ValueError("A dry run is an input preview, not a resumable scoring run")
            path = directory / "preview_requests.jsonl"
            with path.open("w", encoding="utf-8") as stream:
                for item in selected():
                    request = scoring_request(item, spec, prompt=prompt, max_tokens=max_tokens,
                                              model_id=model_id, reasoning_effort=reasoning_effort)
                    stream.write(json.dumps({"item_id": item["item_id"], "request": request}, ensure_ascii=False) + "\n")
            return {"status": "preview", "analysis_type": "six_scores", "items": target,
                    "model_calls": 0, "classifier_count": len(DIMENSIONS), "request_mode": "per_item",
                    "primary_requests": target, "target_item_classifier_judgments": target * len(DIMENSIONS),
                    "path": str(path)}
        if call is None:
            raise ValueError("Scoring requires an API client; use --dry-run to inspect inputs")
        config = {
            "version": 5, "schema_version": RESULT_SCHEMA_VERSION, "analysis_type": "six_scores",
            "request_mode": "per_item", "request_schema_version": REQUEST_SCHEMA_VERSION,
            "spec_schema_version": CONTEXT_SCHEMA_VERSION, "rubric_version": RUBRIC_VERSION,
            "dataset_sha256": file_sha256(directory / "dataset.json"),
            "evidence_sha256": file_sha256(directory / "evidence.json"),
            "spec_sha256": metadata["spec_sha256"], "provider": provider,
            "model": model_id, "model_id": model_id, "reasoning_effort": reasoning_effort,
            "prompts": {"assess_item": prompt}, "prompt_sha256": {"assess_item": text_hash(prompt)},
            "output_schema": OUTPUT_SCHEMA, "max_tokens": max_tokens,
        }
        config_path, results_path = directory / "run.json", directory / "results.jsonl"
        if config_path.exists():
            if not resume:
                raise ValueError("Scoring already started; use --resume to continue")
            if read_json(config_path) != config:
                raise ValueError("Scoring inputs or settings changed; prepare a new run directory")
            if (directory / "execution.json").exists() and target < read_json(directory / "execution.json").get("target_items", 0):
                raise ValueError("Resume may only grow the selected item count")
        else:
            if resume or results_path.exists():
                raise ValueError("Cannot resume without a matching run.json")
            write_json(config_path, config)
        completed = read_results(results_path, repair_tail=resume)
        known_ids = {item["item_id"] for item in read_items(directory / "items.jsonl")}
        if completed.keys() - known_ids:
            raise ValueError("Results contain item IDs outside the prepared dataset")
        for record in completed.values():
            check_result_progress(record)
        attempted, request_calls, cancelled, fatal_error = 0, 0, False, None

        def save_state():
            complete = sum(completed.get(key, {}).get("status") == "complete" for key in selected_ids)
            state = {
                "schema_version": RESULT_SCHEMA_VERSION, "analysis_type": "six_scores",
                "rubric_version": RUBRIC_VERSION, "request_mode": "per_item",
                "target_items": target, "dataset_items": dataset["item_count"],
                "selected_item_ids": selected_ids, "classifier_count": len(DIMENSIONS),
                "primary_requests": target, "target_item_classifier_judgments": target * len(DIMENSIONS),
                "completed_item_classifier_judgments": complete * len(DIMENSIONS),
                "complete": complete, "attempted_this_invocation": attempted,
                "request_calls_this_invocation": request_calls,
                "errors": sum(completed.get(key, {}).get("status") == "error" for key in selected_ids),
                "partial": 0, "pending": sum(key not in completed for key in selected_ids),
                "full_dataset_complete": target == dataset["item_count"] and complete == target,
                "fatal_error": fatal_error, "cancelled": cancelled or bool(should_stop and should_stop()),
            }
            write_json(directory / "execution.json", state)
            return state

        save_state()
        with results_path.open("a", encoding="utf-8") as stream, (directory / "classification_requests.jsonl").open("a", encoding="utf-8") as requests:
            def persist(record):
                check_result_progress(record, completed.get(record["item_id"]))
                stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
                completed[record["item_id"]] = deepcopy(record)
                save_state()
                if on_result:
                    on_result(deepcopy(record))

            for item in selected():
                if should_stop and should_stop():
                    cancelled = True
                    break
                previous = completed.get(item["item_id"])
                if previous and previous["status"] == "complete":
                    continue
                record = deepcopy(previous) if previous else {
                    "schema_version": RESULT_SCHEMA_VERSION, "analysis_type": "six_scores",
                    "item_id": item["item_id"], "status": "error", "dimensions": {}, "attempts": [],
                }
                request = scoring_request(item, spec, prompt=prompt, max_tokens=max_tokens,
                                          model_id=model_id, reasoning_effort=reasoning_effort)
                for repair in range(2):
                    if should_stop and should_stop():
                        cancelled = True
                        break
                    current = dict(request)
                    if repair:
                        previous_attempt = record["attempts"][-1]
                        current["user"] += "\n\nPrevious response:\n" + previous_attempt["response"]
                        current["user"] += "\n\nCorrect only these structural errors and return the full six-dimension JSON:\n" + previous_attempt["error"]
                        current["step"] = "item_scoring_repair"
                    entry = {"attempt": len(record["attempts"]) + 1}
                    requests.write(json.dumps({"item_id": item["item_id"], "attempt": entry["attempt"], "request": current}, ensure_ascii=False) + "\n")
                    requests.flush()
                    if not repair:
                        attempted += 1
                    request_calls += 1
                    try:
                        raw = call(**current)
                    except Exception as exc:
                        fatal_error = f"{type(exc).__name__}: {exc}"
                        entry.update(error=fatal_error, kind="api")
                        record.update(status="error", error=fatal_error)
                    else:
                        entry["response"] = raw if isinstance(raw, str) else repr(raw)
                        try:
                            if not isinstance(raw, str):
                                raise ValueError("Scoring client must return JSON text")
                            dimensions = validate_dimensions(parse_response(raw))
                        except ValueError as exc:
                            entry.update(error=str(exc), kind="structure")
                            record.update(status="error", error=str(exc))
                        else:
                            record.update(status="complete", dimensions=dimensions)
                            record.pop("error", None)
                    record["attempts"].append(entry)
                    # Persist returned judgments even when cancellation arrived
                    # during the request. Only the next call is suppressed.
                    persist(record)
                    if record["status"] == "complete" or fatal_error:
                        break
                if fatal_error or cancelled:
                    break
        return save_state()
