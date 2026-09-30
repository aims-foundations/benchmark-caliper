"""Small file helpers shared by the experiment's commands."""

from contextlib import contextmanager
import fcntl
import hashlib
import json
from pathlib import Path


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_response(text: str):
    """Accept plain JSON or a single fenced JSON block, never guess missing data."""
    text = text.strip()
    if text.startswith("```"):
        # splitlines() also splits Unicode separators inside valid JSON strings.
        lines = text.split("\n")
        if lines[0].strip() not in {"```", "```json"} or lines[-1].strip() != "```":
            raise ValueError("Expected JSON or one complete JSON code block")
        text = "\n".join(lines[1:-1])
    return json.loads(text)


@contextmanager
def run_lock(directory: Path):
    """Reject concurrent writers to one run, including generation and reporting."""
    with (directory / ".lock").open("a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError("Another process is using this run directory") from exc
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def check_prepared(directory: Path) -> dict:
    from .data import file_sha256

    dataset = read_json(directory / "dataset.json")
    for filename, key in (("items.jsonl", "items_sha256"), ("profile.json", "profile_sha256")):
        if file_sha256(directory / filename) != dataset[key]:
            raise ValueError(f"Prepared {filename} changed; prepare a new run directory")
    evidence = read_json(directory / "evidence.json")
    if file_sha256(directory / "evidence.json") != dataset["evidence_sha256"]:
        raise ValueError("Assessment evidence changed; prepare a new run directory")
    if evidence["benchmark"] != dataset["benchmark"]:
        raise ValueError("Assessment and dataset benchmark differ")
    return dataset


def check_specification(directory: Path) -> dict:
    """Keep saved labels tied to the exact criteria and dataset they measured."""
    from .data import file_sha256

    metadata = read_json(directory / "specification.json")
    current_spec = file_sha256(directory / "classifier_spec.json")
    current_dataset = file_sha256(directory / "dataset.json")
    if metadata.get("spec_sha256") != current_spec:
        raise ValueError("Classifier specification changed; prepare a new run directory")
    if metadata.get("dataset_sha256") != current_dataset:
        raise ValueError("Dataset manifest changed after specification creation")
    if (directory / "run.json").exists():
        run = read_json(directory / "run.json")
        if run.get("spec_sha256") != current_spec or run.get("dataset_sha256") != current_dataset:
            raise ValueError("Saved run and current specification or dataset differ")
    return metadata
