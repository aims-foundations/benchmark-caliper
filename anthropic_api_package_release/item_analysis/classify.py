"""One model request per item, all applicable classifiers, with safe continuation."""

from itertools import islice
import json
from pathlib import Path

from .data import file_sha256, read_items
from .schema import labels_schema, validate_labels, validate_spec
from .storage import check_prepared, check_specification, parse_response, read_json, run_lock, text_hash, write_json

PROMPT_PATH = Path(__file__).parent / "prompts" / "classify_item.md"


def classification_request(item, spec, deployment, prompt, *, max_tokens=4096):
    fields = ("id", "component", "operation", "criterion", "category_set", "ordinal_anchors",
              "positive_class", "example_items")
    classifiers = [{key: c[key] for key in fields if key in c}
                   for c in spec["classifiers"] if c["applicable"]]
    payload = {
        "deployment": deployment, "contextualized_deployment": spec["deployment"],
        "classifiers": classifiers, "item": item, "output_schema": labels_schema(spec),
    }
    return {"model": "haiku", "system": prompt,
            "user": json.dumps(payload, ensure_ascii=False, allow_nan=False),
            "max_tokens": max_tokens, "step": "item_classification", "stream": False}


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
        call=None, model_id="haiku", on_result=None, should_stop=None) -> dict:
    """limit is a prefix of a saved random permutation, and can grow on resume.

    All other inputs are frozen. A changed rubric, specification, dataset,
    deployment, actual model ID, or token setting requires a fresh directory.
    Optional website hooks report flushed records and stop before the next call.
    A response already received is saved before stopping, so it can be resumed.
    """
    if (limit is not None and limit <= 0) or max_tokens <= 0:
        raise ValueError("limit and max_tokens must be positive")
    with run_lock(directory):
        dataset = check_prepared(directory)
        metadata = check_specification(directory)
        spec = validate_spec(read_json(directory / "classifier_spec.json"),
                             profile=read_json(directory / "profile.json"), benchmark=dataset["benchmark"])
        deployment = read_json(directory / "evidence.json")["deployment"]
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
        target = dataset["item_count"] if limit is None else min(limit, dataset["item_count"])
        selected = lambda: islice(read_items(directory / "items.jsonl"), target)
        if dry_run:
            if resume:
                raise ValueError("A dry run is an input preview, not a resumable scoring run")
            preview_path = directory / "preview_requests.jsonl"
            with preview_path.open("w", encoding="utf-8") as stream:
                for item in selected():
                    request = classification_request(item, spec, deployment, prompt, max_tokens=max_tokens)
                    stream.write(json.dumps({"item_id": item["item_id"], "request": request}, ensure_ascii=False) + "\n")
            return {"status": "preview", "items": target, "model_calls": 0, "path": str(preview_path)}
        if call is None:
            raise ValueError("Classification requires an API client; use --dry-run to inspect inputs")
        config = {
            "version": 1, "dataset_sha256": file_sha256(directory / "dataset.json"),
            "spec_sha256": metadata["spec_sha256"], "model": "haiku", "model_id": model_id,
            "prompt": prompt, "prompt_sha256": text_hash(prompt), "output_schema": labels_schema(spec),
            "max_tokens": max_tokens,
        }
        config_path = directory / "run.json"
        results_path = directory / "results.jsonl"
        if config_path.exists():
            if not resume:
                raise ValueError("Scoring already started; use --resume to continue")
            if read_json(config_path) != config:
                raise ValueError("Scoring inputs or settings changed; prepare a new run directory")
        else:
            if resume or results_path.exists():
                raise ValueError("Cannot resume without a matching run.json")
            write_json(config_path, config)
        completed = read_results(results_path, repair_tail=resume)
        known_ids = {item["item_id"] for item in read_items(directory / "items.jsonl")}
        if completed.keys() - known_ids:
            raise ValueError("Results contain item IDs outside the prepared dataset")
        for record in completed.values():
            if record["status"] == "complete":
                validate_labels({"labels": record["labels"]}, spec)
        attempted = 0
        fatal_error = None
        cancelled = False
        with results_path.open("a", encoding="utf-8") as stream:
            for item in selected():
                if should_stop and should_stop():
                    cancelled = True
                    break
                previous = completed.get(item["item_id"])
                if previous and previous["status"] == "complete":
                    continue
                request = classification_request(item, spec, deployment, prompt, max_tokens=max_tokens)
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
                stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
                stream.flush()
                completed[item["item_id"]] = record
                attempted += 1
                if on_result:
                    on_result(record)
                if attempted == 1 or attempted % 10 == 0:
                    print(f"Classified {attempted} new items; current item {item['item_id']}: {record['status']}", flush=True)
                if fatal_error or cancelled:
                    break  # Do not spend further calls after an authentication/quota/API failure.
        selected_ids = {item["item_id"] for item in selected()}
        complete = sum(completed.get(key, {}).get("status") == "complete" for key in selected_ids)
        state = {"target_items": target, "dataset_items": dataset["item_count"],
                 "complete": complete, "attempted_this_invocation": attempted,
                 "errors": sum(completed.get(key, {}).get("status") == "error" for key in selected_ids),
                 "pending": sum(key not in completed for key in selected_ids),
                 "full_dataset_complete": target == dataset["item_count"] and complete == target,
                 "fatal_error": fatal_error,
                 "cancelled": cancelled or bool(should_stop and should_stop())}
        write_json(directory / "execution.json", state)
        return state
