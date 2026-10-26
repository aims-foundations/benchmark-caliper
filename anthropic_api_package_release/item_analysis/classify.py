"""Independent classifier requests with durable per-dimension continuation."""

from copy import deepcopy
from itertools import islice
import json
from pathlib import Path

from .data import file_sha256, read_items
from .model_client import MODEL_ID, PROVIDER, REASONING_EFFORT
from .schema import (
    CATALOG_VERSION, SPEC_SCHEMA_VERSION, get_catalog, is_generic_spec,
    classifier_labels_schema, validate_classifier_labels, validate_labels, validate_spec,
)
from .storage import check_prepared, check_specification, parse_response, read_json, run_lock, text_hash, write_json

PROMPT_DIR = Path(__file__).parent / "prompts"
RESULT_SCHEMA_VERSION = "caliper_item_result_v3"
REQUEST_SCHEMA_VERSION = "caliper_item_classifier_request_v1"


def classification_request(item, spec, deployment, classifier_id, *, prompt=None,
                           max_tokens=4096, model_id=MODEL_ID,
                           reasoning_effort=REASONING_EFFORT):
    if not is_generic_spec(spec):
        raise ValueError("Historical classifier specifications are read-only; prepare a new generic run")
    output_schema = classifier_labels_schema(spec, classifier_id)
    classifier = next(c for c in spec["classifiers"] if c["id"] == classifier_id)
    context = spec["context_by_classifier"][classifier_id]
    # Keep original evidence for every extracted statement. Deployment sources
    # also supply explicit scope boundaries even when the context is incomplete.
    source_ids = {key for key, role in spec["source_roles"].items()
                  if role == "deployment_requirement"}
    for field in ("deployment_requirements", "benchmark_evidence", "prior_hypotheses"):
        for statement in context[field]:
            source_ids.update(statement["source_ids"])
    if classifier_id == "input_ontology":
        inventory = spec["input_category_inventory"]
        source_ids.update(inventory["completeness_source_ids"])
        for category in inventory["categories"]:
            source_ids.update(category["source_ids"])
    payload = {
        "schema_version": SPEC_SCHEMA_VERSION,
        "request_schema_version": REQUEST_SCHEMA_VERSION,
        "fixed_catalog_version": spec["fixed_catalog_version"],
        "benchmark": spec["benchmark"], "deployment_description": deployment,
        "classifier": classifier, "context": context,
        "source_registry": {key: value for key, value in spec["source_registry"].items()
                            if key in source_ids},
        "source_roles": {key: value for key, value in spec["source_roles"].items()
                         if key in source_ids},
        "dataset_profile": spec["dataset_profile"],
        "item": item, "output_schema": output_schema,
    }
    if classifier_id == "input_ontology":
        payload["input_category_inventory"] = spec["input_category_inventory"]
    if spec.get("analysis_basis") == "deployment_requirements":
        payload.update(analysis_basis="deployment_requirements", assessment_status="not_run")
    if prompt is None:
        prompt = (PROMPT_DIR / f"classify_{classifier_id}.md").read_text(encoding="utf-8")
    return {"model": model_id, "reasoning_effort": reasoning_effort, "system": prompt,
            "user": json.dumps(payload, ensure_ascii=False, allow_nan=False),
            "max_tokens": max_tokens, "step": f"item_classification.{classifier_id}"}


def check_result_progress(record: dict, previous: dict | None = None) -> None:
    """Check cumulative split-request history without interpreting judgments."""
    if record.get("schema_version") != RESULT_SCHEMA_VERSION:
        raise ValueError("Result versions cannot change within an item")
    labels, errors, attempts = record.get("labels"), record.get("classifier_errors"), record.get("attempts")
    if not isinstance(labels, dict) or not isinstance(errors, dict) or not isinstance(attempts, list):
        raise ValueError("Invalid saved classifier progress")
    if set(labels) & set(errors):
        raise ValueError("A saved classifier judgment cannot also be an error")
    if previous:
        if previous.get("schema_version") != RESULT_SCHEMA_VERSION:
            raise ValueError("Result versions cannot change within an item")
        if previous["status"] == "complete":
            raise ValueError(f"Duplicate completed result for {record['item_id']}")
        if any(labels.get(cid) != value for cid, value in previous["labels"].items()):
            raise ValueError("Saved successful classifier judgments cannot change or disappear")
        if attempts[:len(previous["attempts"])] != previous["attempts"]:
            raise ValueError("Saved classifier attempts cannot change or disappear")


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
            if record.get("status") not in {"complete", "error", "partial"}:
                raise ValueError(f"Invalid result status at byte {start}")
            if record["status"] == "complete" and not isinstance(record.get("labels"), dict):
                raise ValueError(f"Missing labels in completed result at byte {start}")
            previous = latest.get(record["item_id"])
            if previous and previous["status"] == "complete":
                raise ValueError(f"Duplicate completed result for {record['item_id']}")
            if (record.get("schema_version") == RESULT_SCHEMA_VERSION
                    or (previous and previous.get("schema_version") == RESULT_SCHEMA_VERSION)):
                check_result_progress(record, previous)
            if repair_tail and not line.endswith(b"\n"):
                stream.write(b"\n")
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
        classifier_ids = [c["id"] for c in spec["classifiers"]]
        prompts = {cid: (PROMPT_DIR / f"classify_{cid}.md").read_text(encoding="utf-8")
                   for cid in classifier_ids}
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
                    for cid in classifier_ids:
                        request = classification_request(item, spec, deployment, cid, prompt=prompts[cid],
                                                         max_tokens=max_tokens, model_id=model_id,
                                                         reasoning_effort=reasoning_effort)
                        stream.write(json.dumps({"item_id": item["item_id"], "classifier_id": cid,
                                                 "request": request}, ensure_ascii=False) + "\n")
            return {"status": "preview", "items": target, "model_calls": 0,
                    "classifier_count": classifier_count, "request_mode": "per_classifier",
                    "primary_requests": target * classifier_count,
                    "target_item_classifier_judgments": target * classifier_count,
                    "path": str(preview_path)}
        if call is None:
            raise ValueError("Classification requires an API client; use --dry-run to inspect inputs")
        config = {
            "version": 4, "schema_version": RESULT_SCHEMA_VERSION,
            "request_mode": "per_classifier", "request_schema_version": REQUEST_SCHEMA_VERSION,
            "spec_schema_version": SPEC_SCHEMA_VERSION,
            "fixed_catalog_version": CATALOG_VERSION,
            "catalog_sha256": text_hash(json.dumps(get_catalog(), sort_keys=True, ensure_ascii=False)),
            "dataset_sha256": file_sha256(directory / "dataset.json"),
            "evidence_sha256": file_sha256(directory / "evidence.json"),
            "spec_sha256": metadata["spec_sha256"], "provider": provider,
            "model": model_id, "model_id": model_id, "reasoning_effort": reasoning_effort,
            "prompts": prompts, "prompt_sha256": {cid: text_hash(p) for cid, p in prompts.items()},
            "output_schemas": {cid: classifier_labels_schema(spec, cid) for cid in classifier_ids},
            "max_tokens": max_tokens,
            "generation_prompt_sha256": text_hash(
                (PROMPT_DIR / "generate_spec.md").read_text(encoding="utf-8")
            ),
            "generation_user_template_sha256": text_hash(
                (PROMPT_DIR / "generate_user.md").read_text(encoding="utf-8")
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
            for cid, label in record["labels"].items():
                validate_classifier_labels({"labels": {cid: label}}, spec, cid)
            errors = record["classifier_errors"]
            if (set(errors) - set(classifier_ids) or set(errors) & set(record["labels"])
                    or any(not isinstance(error, str) or not error.strip() for error in errors.values())):
                raise ValueError("Invalid saved classifier errors")
            expected_status = ("complete" if len(record["labels"]) == classifier_count else
                               "error" if errors else "partial")
            if record["status"] != expected_status:
                raise ValueError("Saved item status disagrees with classifier progress")
            if any(not isinstance(entry, dict) or entry.get("classifier_id") not in classifier_ids
                   for entry in record["attempts"]):
                raise ValueError("Invalid saved classifier attempts")
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
                "request_mode": "per_classifier",
                "target_items": target, "dataset_items": dataset["item_count"],
                "selected_item_ids": selected_ids, "classifier_count": classifier_count,
                "target_item_classifier_judgments": target * classifier_count,
                "completed_item_classifier_judgments": sum(
                    len(completed.get(key, {}).get("labels", {})) for key in selected_ids
                ),
                "complete": complete, "attempted_this_invocation": attempted,
                "request_calls_this_invocation": request_calls,
                "errors": sum(completed.get(key, {}).get("status") == "error" for key in selected_ids),
                "partial": sum(completed.get(key, {}).get("status") == "partial" for key in selected_ids),
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
            def persist(record):
                # Each append is a cumulative checkpoint. A saved judgment is
                # reusable even if the process stops during the next request.
                record["status"] = ("complete" if len(record["labels"]) == classifier_count else
                                    "error" if record["classifier_errors"] else "partial")
                if record["classifier_errors"]:
                    record["error"] = "; ".join(f"{cid}: {error}" for cid, error in record["classifier_errors"].items())
                else:
                    record.pop("error", None)
                stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
                stream.flush()
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
                    "item_id": item["item_id"], "status": "partial", "labels": {},
                    "classifier_errors": {}, "attempts": [],
                    "schema_version": RESULT_SCHEMA_VERSION, "fixed_catalog_version": CATALOG_VERSION,
                }
                item_attempted = False
                for cid in classifier_ids:
                    if cid in record["labels"]:
                        continue
                    request = classification_request(item, spec, deployment, cid, prompt=prompts[cid],
                                                     max_tokens=max_tokens, model_id=model_id,
                                                     reasoning_effort=reasoning_effort)
                    last_attempt = None
                    for attempt in range(2):
                        if should_stop and should_stop():
                            cancelled = True
                            break
                        current = dict(request)
                        if attempt:
                            current["user"] += "\n\nPrevious response:\n" + last_attempt["response"]
                            current["user"] += "\n\nCorrect these structural errors and return the complete JSON for this classifier only:\n" + last_attempt["error"]
                            current["step"] = f"item_classification_repair.{cid}"
                        if not item_attempted:
                            attempted += 1
                            item_attempted = True
                        entry = {"classifier_id": cid, "attempt": attempt + 1}
                        try:
                            request_calls += 1
                            raw = call(**current)
                        except Exception as exc:
                            fatal_error = f"{type(exc).__name__}: {exc}"
                            entry.update(error=fatal_error, kind="api")
                            record["classifier_errors"][cid] = fatal_error
                            record["attempts"].append(entry)
                            persist(record)
                            break
                        entry["response"] = raw
                        try:
                            labels = validate_classifier_labels(parse_response(raw), spec, cid)
                        except ValueError as exc:
                            entry["error"] = str(exc)
                            record["classifier_errors"][cid] = str(exc)
                        else:
                            record["labels"].update(labels)
                            record["classifier_errors"].pop(cid, None)
                        record["attempts"].append(entry)
                        persist(record)
                        last_attempt = entry
                        if cid in record["labels"]:
                            break
                    if fatal_error or cancelled:
                        break
                if item_attempted and (attempted == 1 or attempted % 10 == 0):
                    print(f"Classified {attempted} new items; current item {item['item_id']}: {record['status']}", flush=True)
                if fatal_error or cancelled:
                    break  # Do not spend further calls after an authentication/quota/API failure.
        return save_state()
