"""Generate a classifier specification once, or import a reviewed specification."""

from itertools import islice
import json
from pathlib import Path

from .data import file_sha256, read_items
from .model_client import MODEL_ID, PROVIDER, REASONING_EFFORT
from .schema import SPEC_SCHEMA, apply_profile_gates, validate_spec
from .storage import check_prepared, parse_response, read_json, run_lock, write_json

PROMPT_PATH = Path(__file__).parent / "prompts" / "generate_spec.md"


def generation_request(directory: Path, max_tokens=12000, *, model_id=MODEL_ID,
                       reasoning_effort=REASONING_EFFORT) -> dict:
    dataset = check_prepared(directory)
    evidence = read_json(directory / "evidence.json")
    payload = {
        "benchmark": dataset["benchmark"], "deployment": evidence["deployment"],
        "dataset_profile": read_json(directory / "profile.json"),
        "evidence_registry": evidence["registry"],
        "example_items": list(islice(read_items(directory / "items.jsonl"), 8)),
        "output_schema": SPEC_SCHEMA,
    }
    return {
        "model": model_id, "reasoning_effort": reasoning_effort,
        "system": PROMPT_PATH.read_text(encoding="utf-8"),
        "user": json.dumps(payload, ensure_ascii=False, allow_nan=False),
        "max_tokens": max_tokens, "step": "item_specification",
    }


def _save_spec(directory, raw_spec, *, source, validate_references):
    dataset = check_prepared(directory)
    profile = read_json(directory / "profile.json")
    evidence = read_json(directory / "evidence.json")
    canonical, adjustments = apply_profile_gates(raw_spec, profile)
    canonical = validate_spec(
        canonical, profile=profile, benchmark=dataset["benchmark"],
        evidence=evidence["registry"] if validate_references else None,
    )
    deployment_matches = canonical["deployment"].strip() == evidence["deployment"].strip()
    if validate_references and not deployment_matches:
        raise ValueError("Generated deployment must copy the supplied deployment text exactly; contextual details belong in classifier criteria")
    # The factual profile comes from code, even when importing a historical pilot.
    # Keep the original JSON alongside it so the replacement is visible.
    if canonical.get("dataset_profile") != profile:
        adjustments.append({"field": "dataset_profile", "reason": "Use the prepared full-table profile; preserve original in classifier_spec.original.json"})
    canonical["dataset_profile"] = profile
    write_json(directory / "classifier_spec.original.json", raw_spec)
    write_json(directory / "classifier_spec.json", canonical)
    metadata = {
        "source": source, "adjustments": adjustments,
        "evidence_references_checked": validate_references,
        "deployment_text_matches": deployment_matches,
        "note": ("Structure and source IDs checked; semantic correctness still needs review."
                 if validate_references else
                 "Imported references and deployment alignment are not automatically verified. Compare the original and specification deployments and review the criteria before interpreting results."),
        "spec_sha256": file_sha256(directory / "classifier_spec.json"),
        "dataset_sha256": file_sha256(directory / "dataset.json"),
    }
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
            }, validate_references=False)
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
                }, validate_references=True)
            except ValueError as exc:
                entry["error"] = str(exc)
                attempts.append(entry)
                write_json(directory / "generation_attempts.json", attempts)
                if attempt:
                    raise ValueError("Specification failed validation after one repair; inspect generation_attempts.json") from exc
            else:
                attempts.append(entry)
                write_json(directory / "generation_attempts.json", attempts)
                return result
    raise AssertionError("Unreachable specification generation state")
