#!/usr/bin/env python3
"""Publish a completed item-analysis export in the repository's curated gallery.

Run from the repository root:
  .venv/bin/python -m website.scripts.import_gallery_item_analysis EXPORT --assessment gsm8k

EXPORT can be an extracted export directory or its original ZIP. Validation is
completed before writing; replacing an existing publication requires --overwrite.
No model calls, database writes, or deployment operations occur here.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from zipfile import BadZipFile, ZipFile, ZIP_DEFLATED

from anthropic_api_package_release.item_analysis.scoring import (
    DIMENSIONS, validate_dimensions, validate_score_spec,
)
from website.server import gallery, gallery_item_analysis


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and not any(
        part in {"", ".", ".."} for part in name.split("/")) and "\\" not in name


def read_export(source: Path) -> dict[str, bytes]:
    """Read without extracting ZIP paths or following filesystem symlinks."""
    require(not source.is_symlink(), "Export cannot be a symlink")
    if source.is_dir():
        paths = sorted(source.rglob("*"))
        require(not any(path.is_symlink() for path in paths), "Export contains a symlink")
        files = {path.relative_to(source).as_posix(): path.read_bytes()
                 for path in paths if path.is_file()}
    else:
        with ZipFile(source) as archive:
            members = [info for info in archive.infolist() if not info.is_dir()]
            require(all(safe_member(info.filename) for info in members), "Unsafe ZIP member path")
            require(len({info.filename for info in members}) == len(members), "Duplicate ZIP member")
            manifests = [info.filename for info in members
                         if info.filename == "manifest.json" or info.filename.endswith("/manifest.json")]
            require(len(manifests) == 1, "Expected exactly one export manifest")
            prefix = manifests[0][:-len("manifest.json")]
            require(all(info.filename.startswith(prefix) for info in members), "Files outside export folder")
            files = {info.filename[len(prefix):]: archive.read(info) for info in members}
    require(all(safe_member(name) for name in files), "Unsafe export artifact path")
    return files


def load_json(files: dict[str, bytes], name: str):
    try:
        return json.loads(files[name], parse_constant=lambda value: require(False, f"Invalid JSON number in {name}"))
    except (KeyError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Missing or invalid JSON artifact: {name}") from exc


def load_rows(files: dict[str, bytes], name: str) -> list[dict]:
    try:
        rows = [json.loads(line) for line in files[name].splitlines() if line.strip()]
        require(all(isinstance(row, dict) for row in rows), f"Invalid records in {name}")
        ids = [row.get("item_id") for row in rows]
        require(all(isinstance(item_id, str) and item_id for item_id in ids), f"Invalid item ID in {name}")
        require(len(ids) == len(set(ids)), f"Duplicate item ID in {name}")
        return rows
    except (KeyError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Missing or invalid JSONL artifact: {name}") from exc


_CREDENTIAL_PATTERN = re.compile(
    rb"(?:\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}|"
    rb'"(?:api_key|access_token|refresh_token|run_token|run_secret|access_secret|owner_token|authorization|x-anthropic-key|x-openai-key)"\s*:\s*"[^"\s]+")',
    re.IGNORECASE,
)


def validate_export(files: dict[str, bytes], assessment_id: str) -> tuple[dict, dict, bytes]:
    report = gallery.get_report(assessment_id)
    require(report is not None, "Unknown gallery assessment")
    manifest = load_json(files, "manifest.json")
    require(isinstance(manifest, dict), "Invalid manifest")
    artifacts = manifest.get("artifacts", [])
    require(isinstance(artifacts, list) and bool(artifacts) and
            all(isinstance(artifact, dict) for artifact in artifacts), "Manifest has no valid artifact checksums")
    listed = [artifact.get("path") for artifact in artifacts]
    require(all(isinstance(name, str) and safe_member(name) for name in listed), "Unsafe manifest path")
    require(len(listed) == len(set(listed)), "Duplicate manifest artifact")
    require(set(files) == set(listed) | {"manifest.json"}, "Export files differ from manifest inventory")
    for artifact in artifacts:
        content = files[artifact["path"]]
        require(len(content) == artifact.get("bytes") and
                hashlib.sha256(content).hexdigest() == artifact.get("sha256"),
                f"Artifact integrity check failed: {artifact['path']}")
    for name, content in files.items():
        require(_CREDENTIAL_PATTERN.search(content) is None,
                f"Possible credential in {name}; remove it from the source export before publication")

    spec = load_json(files, "classifier_spec.json")
    summary = load_json(files, "summary.json")
    original = load_json(files, "original_assessment.json")
    dataset = load_json(files, "audit/dataset.json")
    require(all(isinstance(value, dict) for value in (spec, summary, original, dataset)), "Invalid analysis artifact object")
    validate_score_spec(spec)
    require(dataset.get("assessment") == {"kind": "gallery", "id": assessment_id},
            "Export belongs to a different gallery assessment")
    require(dataset.get("benchmark_identity_confirmed") is True, "Benchmark identity is not confirmed")
    require(original.get("scoring") == report["scoring"], "Original benchmark assessment does not match gallery scores")
    for label, value in (("manifest", manifest), ("summary", summary), ("context", spec), ("original assessment", original)):
        require(value.get("deployment") == report["deployment_description"], f"{label} deployment differs from gallery")
        require(value.get("benchmark") == dataset.get("benchmark"), f"{label} benchmark differs from dataset")
    require(summary.get("original_assessment") == original["scoring"].get("dimensions"),
            "Summary benchmark scores differ from original assessment")
    require(manifest.get("dataset") == dataset == summary.get("dataset"), "Dataset provenance differs across artifacts")
    require(manifest.get("analysis_type") == summary.get("analysis_type") == "six_scores", "Expected a six-score analysis")
    require(manifest.get("run_id") == summary.get("run", {}).get("run_id"), "Run identity differs across artifacts")
    require(manifest.get("rubric_version") == summary.get("rubric_version") == spec.get("rubric_version"), "Rubric differs across artifacts")

    source_items = load_rows(files, "audit/items.jsonl")
    results = load_rows(files, "audit/results.jsonl")
    source_by_id = {item["item_id"]: item for item in source_items}
    results_by_id = {result["item_id"]: result for result in results}
    selected = manifest.get("selected_item_ids")
    require(isinstance(selected, list) and selected and all(isinstance(item_id, str) for item_id in selected), "No selected item IDs")
    require(len(selected) == len(set(selected)), "Duplicate selected item ID")
    require(set(selected) <= source_by_id.keys(), "Selected item missing from prepared snapshot")
    require(set(selected) == results_by_id.keys(), "Saved results do not match selected items")
    require(dataset.get("item_count") == len(source_items) == summary.get("total_items"), "Prepared item counts differ")
    require(dataset.get("items_sha256") == hashlib.sha256(files["audit/items.jsonl"]).hexdigest(), "Prepared items checksum differs")
    items = []
    for item_id in selected:
        result = results_by_id[item_id]
        require(result.get("status") == "complete", "Selected sample is not complete")
        validate_dimensions({"dimensions": result.get("dimensions")})
        # Attempt traces are preserved in the archive, not duplicated in the UI.
        items.append({**source_by_id[item_id], "status": "complete", "dimensions": result["dimensions"]})

    count = len(items)
    require(summary.get("completed_items") == count and summary.get("error_items") == 0
            and summary.get("pending_items") == len(source_items) - count, "Summary completion counts differ")
    expected_counts = {"selected_items": count, "selected_completed_items": count,
                       "selected_error_items": 0, "selected_partial_items": 0, "selected_pending_items": 0,
                       "dimension_count": 6, "expected_item_classifier_judgments": count * 6,
                       "completed_item_classifier_judgments": count * 6,
                       "error_item_classifier_judgments": 0, "invalid_item_classifier_judgments": 0,
                       "pending_item_classifier_judgments": 0}
    for source in (manifest.get("counts", {}), summary.get("experiment", {})):
        require(all(source.get(key) == expected for key, expected in expected_counts.items()), "Manifest or summary selected counts differ")
    require(manifest["counts"].get("prepared_items") == len(source_items), "Manifest prepared count differs")
    dimensions = summary.get("dimensions", [])
    require(isinstance(dimensions, list) and len(dimensions) == 6 and
            all(isinstance(dimension, dict) for dimension in dimensions) and
            {dimension.get("id") for dimension in dimensions} == set(DIMENSIONS), "Summary dimensions differ")
    require(summary.get("classifiers") == dimensions, "Summary classifier dimensions differ")
    for dimension in dimensions:
        scores = [item["dimensions"][dimension["id"]]["score"] for item in items]
        numeric = [score for score in scores if score is not None]
        mean = sum(numeric) / len(numeric) if numeric else None
        saved_mean = dimension.get("mean_score")
        require((mean is None and saved_mean is None) or
                (type(saved_mean) in (int, float) and mean is not None
                 and math.isclose(mean, saved_mean, rel_tol=0, abs_tol=1e-10)), "Dimension average differs from evaluated items")
        counts = Counter(numeric)
        require(dimension.get("counts") == {str(score): counts[score] for score in range(1, 6)}
                and dimension.get("known") == len(numeric) and dimension.get("unknown") == count - len(numeric)
                and all(dimension.get(field) == 0 for field in ("errors", "pending", "invalid")),
                "Dimension distribution differs from evaluated items")

    csv_reader = csv.DictReader(io.StringIO(files["items.csv"].decode("utf-8"), newline=""))
    columns = csv_reader.fieldnames
    csv_rows = list(csv_reader)
    require(len(csv_rows) == len({row.get("item_id") for row in csv_rows}), "Duplicate CSV item ID")
    evaluated = {row["item_id"]: row for row in csv_rows if row.get("item_id") in selected}
    require(set(evaluated) == set(selected), "CSV is missing selected items")
    for item in items:
        row = evaluated[item["item_id"]]
        require(row.get("status") == "complete", "CSV item is incomplete")
        for dimension in DIMENSIONS:
            score = item["dimensions"][dimension]["score"]
            require(row.get(f"{dimension}.score") == ("unknown" if score is None else str(score)), "CSV score differs from saved result")
    csv_output = io.StringIO(newline="")
    writer = csv.DictWriter(csv_output, fieldnames=columns)
    writer.writeheader()
    writer.writerows(evaluated[item_id] for item_id in selected)

    model = manifest.get("model", {})
    model_name = (model.get("model_id") or model.get("model")) if isinstance(model, dict) else model
    require(isinstance(model_name, str) and bool(model_name), "Missing analysis model")
    metadata = {
        "schema_version": 1, "assessment_id": assessment_id,
        "assessment_fingerprint": gallery_item_analysis.assessment_fingerprint(report),
        "run_id": manifest["run_id"], "item_count": count, "total_items": len(source_items),
        "completed_at": manifest["updated_at"], "model": model_name,
    }
    snapshot = {"items": items, "spec": spec, "summary": summary, "manifest": manifest,
                "originalAssessment": original, "dataset": dataset}
    return snapshot, metadata, csv_output.getvalue().encode("utf-8")


def import_snapshot(source: Path, assessment_id: str, *, overwrite: bool = False, output_root: Path | None = None) -> dict:
    require(assessment_id in gallery._entry_ids(), "Unknown gallery assessment")
    output_root = output_root or gallery_item_analysis.SNAPSHOT_ROOT
    destination = output_root / assessment_id
    require(not destination.is_symlink(), "Publication destination cannot be a symlink")
    require(not destination.exists() or overwrite, "Publication already exists; use --overwrite to replace it")
    files = read_export(source)
    snapshot, metadata, evaluated_csv = validate_export(files, assessment_id)
    # Everything above is read-only. Stage a complete publication before swapping
    # it into place; keep the previous publication if staging fails.
    output_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".gallery-import-", dir=output_root) as stage_name:
        stage = Path(stage_name) / assessment_id
        stage.mkdir()
        for name, value in (("snapshot.json", snapshot), ("metadata.json", metadata)):
            (stage / name).write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        (stage / "evaluated-items.csv").write_bytes(evaluated_csv)
        archive_path = stage / "complete-results.zip"
        if source.is_file():
            shutil.copyfile(source, archive_path)
        else:
            with ZipFile(archive_path, "w", compression=ZIP_DEFLATED, compresslevel=6) as archive:
                for name, content in sorted(files.items()):
                    archive.writestr(name, content)
        with ZipFile(archive_path) as archive:
            require(archive.testzip() is None, "Export archive CRC validation failed")
        backup = Path(stage_name) / "previous"
        if destination.exists():
            destination.rename(backup)
        try:
            stage.rename(destination)
        except OSError:
            if backup.exists():
                backup.rename(destination)
            raise
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Extracted complete export or original ZIP")
    parser.add_argument("--assessment", required=True, help="Existing curated gallery assessment ID")
    parser.add_argument("--overwrite", action="store_true", help="Explicitly replace this assessment's saved item analysis")
    args = parser.parse_args()
    try:
        metadata = import_snapshot(args.source, args.assessment, overwrite=args.overwrite)
    except (OSError, BadZipFile, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Import refused: {exc}\n")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
