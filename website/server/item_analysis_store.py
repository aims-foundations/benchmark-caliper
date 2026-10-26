"""Private durable metadata and credential-free usage for website item analyses."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import time

from anthropic_api_package_release.item_analysis.storage import read_json, write_json

METADATA = "_website_run.json"
COUNTERS = ("input_tokens", "output_tokens", "cached_input_tokens", "reasoning_tokens")


def timestamp(value: float) -> str:
    return datetime.fromtimestamp(value, timezone.utc).isoformat()


def token_digest(secret: str) -> str:
    return hashlib.sha256(secret.encode()).hexdigest()


def retention_seconds() -> int:
    """Only an explicitly configured positive duration enables automatic expiry."""
    value = os.environ.get("ITEM_ANALYSIS_RETENTION_SECONDS", "0")
    try:
        return max(0, int(value))
    except ValueError:
        return 0


def directory_for(root: Path, run_id: str) -> Path | None:
    if not re.fullmatch(r"[0-9a-f]{32}", run_id):
        return None
    directory = root / run_id
    if directory.is_symlink():
        return None
    return directory


def load_metadata(directory: Path) -> dict:
    data = read_json(directory / METADATA)
    if (not isinstance(data, dict) or data.get("version") != 1
            or data.get("run_id") != directory.name
            or not re.fullmatch(r"[0-9a-f]{64}", data.get("secret_digest", ""))):
        raise ValueError("Invalid saved item analysis")
    return data


def save_metadata(directory: Path, metadata: dict) -> None:
    write_json(directory / METADATA, {"version": 1, **metadata})
    (directory / METADATA).chmod(0o600)


def record_call(directory: Path, entry: dict, totals: dict) -> None:
    """Append each completed call durably before returning its response to the runner."""
    append_jsonl(directory / "usage_ledger.jsonl", entry)
    for key in COUNTERS:
        totals[key] += entry.get(key, 0)
    previous = read_json(directory / "usage.json") if (directory / "usage.json").exists() else {}
    write_usage(directory, totals, entry,
                calls=previous.get("calls", 0) + 1,
                known=previous.get("calls_with_usage", 0) + int(entry["usage_known"]))


def write_usage(directory: Path, totals: dict, entry: dict, *, calls: int, known: int) -> None:
    write_json(directory / "usage.json", {
        **totals, "provider": "openai", "model": entry["model"], "calls": calls,
        "calls_with_usage": known, "calls_without_usage": calls - known,
        "reasoning_effort": entry["reasoning_effort"],
        "note": "Token totals cover only calls with provider usage. Cached input and reasoning tokens are subsets of input and output totals. An interrupted request may not have been sent; missing usage is not proof of no charge.",
    })


def append_jsonl(path: Path, entry: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, allow_nan=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    path.chmod(0o600)


def saved_records(path: Path):
    """Stream durable records, trimming only an unfinished final JSON append."""
    if not path.exists():
        return
    # An interrupted final append is discarded; complete malformed records fail.
    with path.open("r+b") as handle:
        while line := handle.readline():
            end = handle.tell()
            try:
                entry = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                if not line.endswith(b"\n"):
                    handle.truncate(end - len(line))
                    handle.flush()
                    os.fsync(handle.fileno())
                    break
                raise ValueError("Invalid saved call audit") from None
            if not isinstance(entry, dict) or not isinstance(entry.get("sequence"), int) or entry["sequence"] < 1:
                raise ValueError("Invalid saved call audit")
            if not line.endswith(b"\n"):
                # A complete JSON write may survive while its newline does not.
                # Preserve the record and repair its separator before any append.
                handle.write(b"\n")
                handle.flush()
                os.fsync(handle.fileno())
            yield entry


def load_usage(directory: Path) -> tuple[dict, int]:
    """Restore known totals and mark calls interrupted before a completion was saved."""
    totals = dict.fromkeys(COUNTERS, 0)
    seen = set()
    known = 0
    last = None
    for entry in saved_records(directory / "usage_ledger.jsonl"):
        if entry["sequence"] in seen:
            raise ValueError("Duplicate usage record")
        seen.add(entry["sequence"])
        for key in COUNTERS:
            totals[key] += entry.get(key, 0)
        known += int(entry["usage_known"])
        last = entry
    # A process can stop after writing the exact request but before saving any
    # response/usage. Preserve that uncertainty instead of treating it as free.
    for request in saved_records(directory / "requests.jsonl"):
        if request["sequence"] in seen:
            continue
        last = {
            **{key: request[key] for key in ("sequence", "step", "model", "reasoning_effort", "max_tokens", "started_at")},
            "provider": "openai", "finished_at": None, "recovered_at": timestamp(time.time()),
            "status": "interrupted", "error_code": "completion_unavailable", "usage_known": False,
        }
        append_jsonl(directory / "usage_ledger.jsonl", last)
        seen.add(last["sequence"])
    if last is not None:
        write_usage(directory, totals, last, calls=len(seen), known=known)
    return totals, max(seen, default=0)
