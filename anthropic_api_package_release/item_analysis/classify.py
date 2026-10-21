"""One model request per item, all applicable classifiers, with safe continuation."""

from itertools import islice
import json
from pathlib import Path

from .data import file_sha256, read_items
from .model_client import MODEL_ID, PROVIDER, REASONING_EFFORT
from .schema import (
    CATALOG_VERSION, SPEC_SCHEMA_VERSION, get_catalog, is_generic_spec,
    labels_schema, validate_labels, validate_spec,
)
from .storage import check_prepared, check_specification, parse_response, read_json, run_lock, text_hash, write_json

PROMPT_PATH = Path(__file__).parent / "prompts" / "classify_item.md"
RESULT_SCHEMA_VERSION = "caliper_item_result_v2"


def classification_request(item, spec, deployment, prompt, *, max_tokens=4096,
                           model_id=MODEL_ID, reasoning_effort=REASONING_EFFORT):
    if not is_generic_spec(spec):
        raise ValueError("Historical classifier specifications are read-only; prepare a new generic run")
    payload = {
        "schema_version": SPEC_SCHEMA_VERSION,
        "fixed_catalog_version": spec["fixed_catalog_version"],
        "benchmark": spec["benchmark"],
        "deployment_description": deployment,
        # The actual fixed questions, rules, meanings and response contracts are
        # supplied on every item request, not reconstructed by the item judge.
        "classifiers": spec["classifiers"],
        "input_category_inventory": spec["input_category_inventory"],
        "context_by_classifier": spec["context_by_classifier"],
        "source_registry": spec["source_registry"],
        "source_roles": spec["source_roles"],
        "dataset_profile": spec["dataset_profile"],
        "item": item, "output_schema": labels_schema(spec),
    }
    if spec.get("analysis_basis") == "deployment_requirements":
        payload.update(analysis_basis="deployment_requirements", assessment_status="not_run")
    return {"model": model_id, "reasoning_effort": reasoning_effort, "system": prompt,
            "user": json.dumps(payload, ensure_ascii=False, allow_nan=False),
            "max_tokens": max_tokens, "step": "item_classification"}


def read_results(path: Path, *, repair_tail=False) -> dict:
    """Recover only an interrupted final append; never silently ignore a corrupt record."""
    if not path.exists():
        return {}
    latest = {}
    with path.open("r+b" if repair_tail else "rb") as stream:
        while True:
            start = stream.tell()
            line = stream.readline()
            if not line:
                break
            try:
                record = json.loads(line)
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                if repair_tail and not line.endswith(b"\n"):
                    stream.truncate(start)
                    break
                raise ValueError(f"Invalid results record at byte {start}") from exc
            if not isinstance(record, dict) or not isinstance(record.get("item_id"), str):
                raise ValueError(f"Missing item_id in results record at byte {start}")
            if record.get("status") not in {"complete", "error"}:
                raise ValueError(f"Invalid result status at byte {start}")
            if record["status"] == "complete" and not isinstance(record.get("labels"), dict):
                raise ValueError(f"Missing labels in completed result at byte {start}")
            if repair_tail and not line.endswith(b"\n"):
                stream.write(b"\n")
            previous = latest.get(record["item_id"])
            if previous and previous["status"] == "complete":
                raise ValueError(f"Duplicate completed result for {record['item_id']}")
            latest[record["item_id"]] = record
    return latest


def run(directory: Path, *, limit=100, resume=False, dry_run=False, max_tokens=4096,
        call=None, model_id=MODEL_ID, provider=PROVIDER, reasoning_effort=REASONING_EFFORT,
        on_result=None, should_stop=None) -> dict:
    """limit is a prefix of a saved random permutation, and can grow on resume.

    All other inputs are frozen. A changed rubric, specification, dataset,
    deployment, provider, actual model ID, reasoning, or token setting requires a fresh directory.
    Optional website hooks report flushed records and stop before the next call.
    A response already received is saved before stopping, so it can be resumed.
    """
    if (limit is not None and limit <= 0) or max_tokens <= 0:
        raise ValueError("limit and max_tokens must be positive")
    with run_lock(directory):
        dataset = check_prepared(directory)
        metadata = check_specification(directory)
        saved_spec = read_json(directory / "classifier_spec.json")
        if not is_generic_spec(saved_spec):
            raise ValueError("Historical classifier specifications are read-only; prepare a new generic run")
        spec = validate_spec(saved_spec,
                             profile=read_json(directory / "profile.json"), benchmark=dataset["benchmark"])
        deployment = read_json(directory / "evidence.json")["deployment"]
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
        target = dataset["item_count"] if limit is None else min(limit, dataset["item_count"])
        selected = lambda: islice(read_items(directory / "items.jsonl"), target)
        selected_ids = [item["item_id"] for item in selected()]
        classifier_count = len(spec["classifiers"])
        if dry_run:
            if resume:
                raise ValueError("A dry run is an input preview, not a resumable scoring run")
            preview_path = directory / "preview_requests.jsonl"
            with preview_path.open("w", encoding="utf-8") as stream:
                for item in selected():
                    request = classification_request(item, spec, deployment, prompt, max_tokens=max_tokens,
                                                     model_id=model_id, reasoning_effort=reasoning_effort)
                    stream.write(json.dumps({"item_id": item["item_id"], "request": request}, ensure_ascii=False) + "\n")
            return {"status": "preview", "items": target, "model_calls": 0,
                    "classifier_count": classifier_count,
                    "target_item_classifier_judgments": target * classifier_count,
                    "path": str(preview_path)}
        if call is None:
            raise ValueError("Classification requires an API client; use --dry-run to inspect inputs")
        config = {
            "version": 3, "schema_version": RESULT_SCHEMA_VERSION,
            "spec_schema_version": SPEC_SCHEMA_VERSION,
            "fixed_catalog_version": CATALOG_VERSION,
            "catalog_sha256": text_hash(json.dumps(get_catalog(), sort_keys=True, ensure_ascii=False)),
            "dataset_sha256": file_sha256(directory / "dataset.json"),
            "evidence_sha256": file_sha256(directory / "evidence.json"),
            "spec_sha256": metadata["spec_sha256"], "provider": provider,
            "model": model_id, "model_id": model_id, "reasoning_effort": reasoning_effort,
            "prompt": prompt, "prompt_sha256": text_hash(prompt), "output_schema": labels_schema(spec),
            "max_tokens": max_tokens,
            "generation_prompt_sha256": text_hash(
                (PROMPT_PATH.parent / "generate_spec.md").read_text(encoding="utf-8")
            ),
            "generation_user_template_sha256": text_hash(
                (PROMPT_PATH.parent / "generate_user.md").read_text(encoding="utf-8")
            ),
            "generation_request_sha256": (
                file_sha256(directory / "generation_request.json")
                if (directory / "generation_request.json").exists() else None
            ),
        }
        config_path = directory / "run.json"
        results_path = directory / "results.jsonl"
        if config_path.exists():
            if not resume:
                raise ValueError("Scoring already started; use --resume to continue")
            if read_json(config_path) != config:
                raise ValueError("Scoring inputs or settings changed; prepare a new run directory")
            if (directory / "execution.json").exists():
                previous_target = read_json(directory / "execution.json").get("target_items", 0)
                if target < previous_target:
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
            if (record.get("schema_version") != RESULT_SCHEMA_VERSION
                    or record.get("fixed_catalog_version") != CATALOG_VERSION):
                raise ValueError("Saved result schema or catalog changed; prepare a new run directory")
            if record["status"] == "complete":
                validate_labels({"labels": record["labels"]}, spec)
        attempted = 0
        request_calls = 0
        fatal_error = None
        cancelled = False

        def save_state():
            complete = sum(completed.get(key, {}).get("status") == "complete" for key in selected_ids)
            state = {
                "schema_version": RESULT_SCHEMA_VERSION, "fixed_catalog_version": CATALOG_VERSION,
                "target_items": target, "dataset_items": dataset["item_count"],
                "selected_item_ids": selected_ids, "classifier_count": classifier_count,
                "target_item_classifier_judgments": target * classifier_count,
                "completed_item_classifier_judgments": sum(
                    len(completed[key]["labels"]) for key in selected_ids
                    if completed.get(key, {}).get("status") == "complete"
                ),
                "complete": complete, "attempted_this_invocation": attempted,
                "request_calls_this_invocation": request_calls,
                "errors": sum(completed.get(key, {}).get("status") == "error" for key in selected_ids),
                "pending": sum(key not in completed for key in selected_ids),
                "full_dataset_complete": target == dataset["item_count"] and complete == target,
                "fatal_error": fatal_error,
                "cancelled": cancelled or bool(should_stop and should_stop()),
            }
            write_json(directory / "execution.json", state)
            return state

        # Persist the selected population before any call so interrupted runs
        # and review exports still have the correct experimental denominator.
        save_state()
        with results_path.open("a", encoding="utf-8") as stream:
            for item in selected():
                if should_stop and should_stop():
                    cancelled = True
                    break
                previous = completed.get(item["item_id"])
                if previous and previous["status"] == "complete":
                    continue
                request = classification_request(item, spec, deployment, prompt, max_tokens=max_tokens,
                                                 model_id=model_id, reasoning_effort=reasoning_effort)
                attempts = []
                record = {"item_id": item["item_id"], "status": "error"}
                for attempt in range(2):
                    if should_stop and should_stop():
                        cancelled = True
                        record["error"] = "Stopped before completing classification."
                        break
                    current = dict(request)
                    if attempt:
                        current["user"] += "\n\nPrevious response:\n" + attempts[-1]["response"]
                        current["user"] += "\n\nCorrect these structural errors and return the full JSON:\n" + attempts[-1]["error"]
                        current["step"] = "item_classification_repair"
                    try:
                        request_calls += 1
                        raw = call(**current)
                    except Exception as exc:
                        fatal_error = f"{type(exc).__name__}: {exc}"
                        attempts.append({"error": fatal_error, "kind": "api"})
                        record["error"] = fatal_error
                        break
                    entry = {"response": raw}
                    try:
                        labels = validate_labels(parse_response(raw), spec)
                    except ValueError as exc:
                        entry["error"] = str(exc)
                        record["error"] = str(exc)
                        attempts.append(entry)
                    else:
                        attempts.append(entry)
                        record = {"item_id": item["item_id"], "status": "complete", "labels": labels}
                        break
                record["attempts"] = attempts
                record["schema_version"] = RESULT_SCHEMA_VERSION
                record["fixed_catalog_version"] = CATALOG_VERSION
                stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
                stream.flush()
                completed[item["item_id"]] = record
                attempted += 1
                save_state()
                if on_result:
                    on_result(record)
                if attempted == 1 or attempted % 10 == 0:
                    print(f"Classified {attempted} new items; current item {item['item_id']}: {record['status']}", flush=True)
                if fatal_error or cancelled:
                    break  # Do not spend further calls after an authentication/quota/API failure.
        return save_state()
