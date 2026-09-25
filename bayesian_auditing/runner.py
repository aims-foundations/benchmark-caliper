"""A sequential, resumable scoring loop and file-based result reports."""

from collections import Counter
import heapq
import json
from pathlib import Path
import sys

from openai import OpenAIError

from .data import DATA_VERSION, fingerprint, iter_items
from .judge import DEFAULT_MAX_OUTPUT_TOKENS, DEFAULT_REASONING_EFFORT, request_input
from .scoring import Assessment, SCORING_VERSION

DONE = {"complete", "unresolved", "preview"}


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def records(path: Path, *, repair_tail=False):
    """Recover an interrupted final append; never hide corruption in a complete line."""
    if not path.exists():
        return
    with path.open("r+b" if repair_tail else "rb") as stream:
        while True:
            offset = stream.tell()
            line = stream.readline()
            if not line:
                break
            try:
                record = json.loads(line)
            except (ValueError, UnicodeDecodeError) as exc:
                if repair_tail and not line.endswith(b"\n"):
                    stream.truncate(offset)
                    break
                raise ValueError(f"Invalid assessment log at byte {offset}: {path}") from exc
            if repair_tail and not line.endswith(b"\n"):
                stream.write(b"\n")
            yield record


def read_state(path: Path, *, repair_tail=False):
    done, finished_sources, all_sources, statuses = set(), set(), set(), {}
    usage = Counter(input_tokens=0, output_tokens=0, reasoning_tokens=0, cached_input_tokens=0)
    for record in records(path, repair_tail=repair_tail):
        key, status = record["evidence_hash"], record["status"]
        source_key = fingerprint(record["source"])
        all_sources.add(source_key)
        if status != "duplicate":
            statuses[key] = status
        if status in DONE:
            done.add(key)
        if status in DONE or status == "duplicate":
            finished_sources.add(source_key)
        tokens = record.get("usage") or {}
        usage["input_tokens"] += tokens.get("input_tokens", 0)
        usage["output_tokens"] += tokens.get("output_tokens", 0)
        usage["reasoning_tokens"] += (tokens.get("output_tokens_details") or {}).get("reasoning_tokens", 0)
        usage["cached_input_tokens"] += (tokens.get("input_tokens_details") or {}).get("cached_tokens", 0)
    return done, finished_sources, all_sources, statuses, dict(usage)


def ranked_items(path: Path, top_k: int) -> list[dict]:
    # Keep only top-k complete records in memory. Successful judgments are written
    # once per evidence hash; resume never repeats them.
    best = heapq.nlargest(
        top_k, (r for r in records(path) if r["status"] == "complete"),
        key=lambda r: (r["overall_score"], r["evidence_hash"]),
    )
    sources = {r["evidence_hash"]: {} for r in best}
    for record in records(path):
        key = record["evidence_hash"]
        if key in sources:
            sources[key][fingerprint(record["source"])] = record["source"]
    return [{
        "rank": rank, "evidence_hash": r["evidence_hash"],
        "overall_score": r["overall_score"], "assessment": r["assessment"],
        "evidence": r["evidence"], "sources": list(sources[r["evidence_hash"]].values()),
        "response_id": r.get("response_id"), "response_model": r.get("response_model"),
    } for rank, r in enumerate(best, 1)]


def run(inventory, deployment, prompt, output_dir, *, model,
        reasoning_effort=DEFAULT_REASONING_EFFORT,
        max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS, top_k=10, limit_per_table=None, dry_run=False,
        resume=False, judge=None):
    if not deployment.strip():
        raise ValueError("Deployment description must not be empty")
    if top_k <= 0 or max_output_tokens <= 0 or (limit_per_table is not None and limit_per_table <= 0):
        raise ValueError("top_k, max_output_tokens, and limit_per_table must be positive")
    if not dry_run and judge is None:
        raise ValueError("A judge is required for a live run")
    config = {
        "format_version": 1, "data_version": DATA_VERSION, "scoring_version": SCORING_VERSION,
        "inventory": inventory, "deployment": deployment, "model": model,
        "reasoning_effort": reasoning_effort, "max_output_tokens": max_output_tokens,
        "prompt": prompt, "output_schema": Assessment.model_json_schema(),
        "limit_per_table": limit_per_table, "dry_run": dry_run,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = output_dir / "run.json"
    log_path = output_dir / "assessments.jsonl"
    if config_path.exists():
        if not resume:
            raise ValueError("Run already exists; use --resume or a new output directory")
        if json.loads(config_path.read_text(encoding="utf-8")) != config:
            raise ValueError("Run settings or evidence inventory changed; use a new output directory")
    else:
        if resume:
            raise ValueError("Cannot resume: run.json does not exist")
        if any(output_dir.iterdir()):
            raise ValueError("Use an empty output directory for a new run")
        write_json(config_path, config)
    done, finished_sources, _, _, _ = read_state(log_path, repair_tail=resume)
    traversal_complete = False
    fatal_error = None
    processed = 0
    try:
        with log_path.open("a", encoding="utf-8") as log:
            for item in iter_items(inventory, limit_per_table):
                source_key = fingerprint(item["source"])
                if source_key in finished_sources:
                    continue
                key = item["evidence_hash"]
                fatal = None
                if key in done:
                    record = {"source": item["source"], "evidence_hash": key, "status": "duplicate"}
                elif dry_run:
                    record = {**item, "status": "preview", "request_input": request_input(deployment, item["evidence"])}
                else:
                    try:
                        record = {**item, **judge(item["evidence"])}
                    except OpenAIError as exc:
                        # After SDK retries, stop on API failures (including quota,
                        # authentication, and invalid parameters) to avoid a failing
                        # request for every remaining row. Resume retries this item.
                        record = {**item, "status": "error", "error": str(exc)}
                        fatal = exc
                log.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
                log.flush()
                if record["status"] in DONE:
                    done.add(key)
                if record["status"] in DONE or record["status"] == "duplicate":
                    finished_sources.add(source_key)
                processed += 1
                if processed == 1 or processed % 25 == 0 or record["status"] == "error":
                    print(f"Processed {processed} source rows this invocation; latest status: {record['status']}", file=sys.stderr)
                if fatal is not None:
                    raise fatal
        traversal_complete = True
    except BaseException as exc:
        fatal_error = str(exc) or type(exc).__name__
        raise
    finally:
        _, _, sources, statuses, usage = read_state(log_path)
        counts = Counter(statuses.values())
        full_traversal = traversal_complete and limit_per_table is None and not inventory["missing_item_tables"]
        summary = {
            "state": "finished" if traversal_complete else "interrupted",
            "dry_run": dry_run, "tables_in_inventory": len(inventory["tables"]),
            "missing_item_tables": inventory["missing_item_tables"],
            "limit_per_table": limit_per_table, "source_rows_seen": len(sources),
            "unique_scoring_inputs": len(statuses),
            "complete": counts["complete"], "unresolved": counts["unresolved"],
            "errors": counts["error"], "previews": counts["preview"],
            "configured_scope_traversed": traversal_complete,
            "full_inventory_traversed": full_traversal,
            "full_inventory_scored": full_traversal and not dry_run and not counts["error"] and not counts["unresolved"],
            "usage_all_attempts": usage, "fatal_error": fatal_error,
            "ranking_scope": "Complete assessments only; unresolved and failed items are not ranked.",
        }
        write_json(output_dir / "ranked_items.json", ranked_items(log_path, top_k))
        write_json(output_dir / "summary.json", summary)
    return summary
