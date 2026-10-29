#!/usr/bin/env python3
"""Publish a saved construction export without rerunning any pipeline stage.

Accepts the original ZIP or a folder containing report.html, selected_items.csv,
and results.json. The complete JSON remains inside the archived ZIP. The public
page uses a compact snapshot and one gzip file per screened item.
"""

from __future__ import annotations

import argparse
from contextlib import ExitStack
import csv
import gzip
import hashlib
from io import TextIOWrapper
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
from types import SimpleNamespace
from zipfile import BadZipFile, ZipFile, ZIP_DEFLATED

from bayesian_auditing.benchmark_data import row_fingerprint
from bayesian_auditing.requirements import Requirements
from bayesian_auditing.screening import GATED_DIMENSIONS, ScreeningAssessment, gate_for
from website.server import construction_gallery as gallery
from website.server.adaptive_review import validate_collection
from website.server import construction_composition, result_package, streaming_json


FILES = ("report.html", "selected_items.csv", "results.json")


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Export:
    """Open known source members without extracting paths or reading whole files."""

    def __init__(self, source):
        self.source = Path(source)
        self.stack = ExitStack()
        self.archive = None
        self.members = {name: name for name in FILES}

    def __enter__(self):
        require(not self.source.is_symlink(), "The source export cannot be a symlink")
        try:
            if self.source.is_dir():
                paths = list(self.source.iterdir())
                require({path.name for path in paths} == set(FILES), "The export folder must contain exactly the three original result files")
                require(all(path.is_file() and not path.is_symlink() for path in paths), "Export artifacts must be regular files")
            else:
                self.archive = self.stack.enter_context(ZipFile(self.source))
                entries = [info for info in self.archive.infolist() if not info.is_dir()]
                names = [info.filename for info in entries]
                require(len(names) == len(set(names)), "The archive contains duplicate member names")
                require(all(not PurePosixPath(name).is_absolute() and "\\" not in name
                            and all(part not in {"", ".", ".."} for part in name.split("/")) for name in names), "The archive contains an unsafe path")
                require(not any(stat.S_ISLNK(info.external_attr >> 16) for info in entries), "The archive contains a symlink")
                results = [name for name in names if name == "results.json" or name.endswith("/results.json")]
                require(len(results) == 1, "Expected one original results.json")
                prefix = results[0][:-len("results.json")]
                self.members = {name: prefix + name for name in FILES}
                require(set(names) == set(self.members.values()), "The archive must contain exactly the three original result files")
            return self
        except BaseException:
            self.stack.close()
            raise

    def __exit__(self, *args):
        return self.stack.__exit__(*args)

    def open(self, name):
        return self.archive.open(self.members[name]) if self.archive is not None else (self.source / name).open("rb")


def checksum(stream, destination=None):
    digest, size = hashlib.sha256(), 0
    while chunk := stream.read(64 * 1024):
        digest.update(chunk)
        size += len(chunk)
        if destination is not None:
            destination.write(chunk)
    return {"bytes": size, "sha256": digest.hexdigest()}


def write_json(path, value):
    with path.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
        stream.write("\n")


def read_item(directory, item_id):
    with gzip.open(directory / "items" / gallery.item_filename(item_id), "rt", encoding="utf-8") as stream:
        return json.load(stream)


def derive_snapshot(stream, directory):
    summaries = []
    seen = set()
    (directory / "items").mkdir()

    def transform(path, record):
        if (len(path) == 5 and path[:2] == ("retrieval", "rankings")
                and path[3] == "candidates" and isinstance(path[2], int) and isinstance(path[4], int)):
            return {}
        if len(path) != 3 or path[:2] != ("screening", "items") or not isinstance(path[2], int):
            return record
        item_id = record.get("item_id")
        require(isinstance(item_id, str) and item_id and item_id not in seen, "Screened item IDs must be unique and nonempty")
        seen.add(item_id)
        row = (record.get("evidence") or {}).get("item")
        require(isinstance(row, dict) and row_fingerprint(row) == item_id == record.get("evidence_hash"), "A screened item does not retain its original row identity")
        require(record.get("status") in {"complete", "error"}, "A screened item has an invalid saved status")
        assessment = None
        if record["status"] == "complete":
            assessment = ScreeningAssessment.model_validate(record.get("assessment"))
            require((record.get("gate") or {}).get("status") == gate_for(assessment)["status"], "A saved screening gate differs from its ratings")
        with gzip.open(directory / "items" / gallery.item_filename(item_id), "wt", encoding="utf-8") as output:
            json.dump(record, output, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
        text = record.get("question_text") or record.get("search_text") or json.dumps(row, ensure_ascii=False)
        scores = [getattr(assessment.ratings, name).score for name in GATED_DIMENSIONS] if assessment else []
        summaries.append({
            "item_id": item_id, "index": path[2], "question_preview": " ".join(text.split())[:300],
            "status": record["status"], "gate": (record.get("gate") or {}).get("status"),
            "matched_facet_ids": assessment.task.matched_facet_ids if assessment else [],
            "sources": list(dict.fromkeys(source["benchmark"] for source in record.get("sources", []) if source.get("benchmark"))),
            "quality_score": sum(scores) / 4 if scores and all(score is not None for score in scores) else None,
        })
        return {}

    review = streaming_json.load(stream, transform=transform)
    require(isinstance(review, dict), "The export must contain a result object")
    require(not {"run_secret", "owner_hash", "api_key", "access_token"}.intersection(review), "The source includes private run credentials")
    require(review.get("mode") in {"screening", "selection", "adaptive"}, "The export must include screened construction items")
    require(isinstance(review.get("run_id"), str) and review["run_id"], "The source run ID is missing")
    requirements = Requirements.model_validate(review.get("requirements"))
    selection = review.get("selection") or {}
    selected_ids = selection.get("selected_item_ids", [])
    require(isinstance(selected_ids, list) and all(isinstance(key, str) for key in selected_ids), "Selected item IDs must be a list")
    require(len(selected_ids) == len(set(selected_ids)) and set(selected_ids) <= seen, "Selected items must uniquely reference saved screening records")
    require(selection.get("selected_count", 0) == len(selected_ids), "The selected item count differs from the saved records")
    selected_rows = selection.get("items", [])
    require(len(selected_rows) == len(selected_ids) and {row.get("item_id") for row in selected_rows} == set(selected_ids), "The saved selection summaries differ from the selected IDs")
    initial_ids = {item["item_id"] for item in review["screening"]["allocation"]["items"]}
    selected = []
    for summary in summaries:
        item = read_item(directory, summary["item_id"])
        if item["status"] == "complete":
            ScreeningAssessment.model_validate(item["assessment"]).validate_context(requirements)
        summary.update(selected=summary["item_id"] in selected_ids, initial=summary["item_id"] in initial_ids)
        if summary["selected"]:
            require(summary["status"] == "complete" and summary["gate"] == "pass", "Selected items must have complete passing assessments")
            selected.append(item)
    count = sum(item["status"] == "complete" for item in summaries)
    if "selection_input" in review:
        require(review["selection_input"]["screened"] == count, "The saved screening count differs from the assessed items")
        require(review["selection_input"]["errors"] == len(summaries) - count, "The saved error count differs from the item records")
    if review.get("adaptive"):
        require(review["adaptive"]["screened_count"] == count, "The adaptive screening count differs from the item records")
    if selection:
        validate_collection(SimpleNamespace(selection=selection, screening={"items": selected}, requirements=review["requirements"]))
    # The complete original retrieval and all assessments remain in the ZIP.
    # Only selected items are embedded in the page's initial response.
    review["screening"]["items"] = selected
    if review.get("retrieval"):
        rankings = review["retrieval"].pop("rankings", [])
        counts = {ranking["facet_id"]: len(ranking["candidates"]) for ranking in rankings}
        for query in review["retrieval"].get("queries", []):
            if query.get("facet_id") in counts:
                query.setdefault("candidate_count", counts[query["facet_id"]])
        for queue in review["retrieval"].get("queues", []):
            if "item_ids" in queue:
                queue["item_count"] = len(queue.pop("item_ids"))
    return {"review": review, "items": summaries}


def validate_csv(stream, snapshot):
    rows = list(csv.DictReader(TextIOWrapper(stream, encoding="utf-8-sig", newline="")))
    selection = snapshot["review"].get("selection") or {}
    require([row.get("item_id") for row in rows] == selection.get("selected_item_ids", []), "The CSV selected IDs differ from the saved collection")
    items = {item["item_id"]: item for item in snapshot["review"]["screening"]["items"]}
    for row in rows:
        item = items[row["item_id"]]
        require(row.get("screening_gate") == item["gate"]["status"], "A CSV screening gate differs from the saved assessment")
        for name, finding in item["assessment"]["ratings"].items():
            require(row.get(name) == ("" if finding["score"] is None else str(finding["score"])), "A CSV rating differs from the saved assessment")


def add_composition(directory, snapshot, *, title, annotations=None):
    """Add a derived summary and report while retaining the original exports."""
    snapshot["composition"] = construction_composition.summarize(snapshot["review"], annotations)
    if annotations is not None:
        write_json(directory / "composition_annotations.json", annotations)
    selected = {item["item_id"]: item for item in snapshot["review"]["screening"]["items"]}
    # Report history counts every saved assessment. Only selected rows need full
    # evidence; summaries retain the status of every other screened candidate.
    report_items = [selected.get(item["item_id"], {"item_id": item["item_id"], "status": item["status"]})
                    for item in snapshot["items"]]
    review = {**snapshot["review"], "screening": {
        **snapshot["review"]["screening"], "items": report_items,
    }, "metadata": {
        **(snapshot["review"].get("metadata") or {}), "run_name": title,
    }}
    path = directory / "report-with-composition.html"
    with path.open("w", encoding="utf-8") as output:
        for part in result_package._report(review, composition_annotations=annotations):
            output.write(part)
    with path.open("rb") as stream:
        return {"filename": path.name, **checksum(stream)}


def import_example(source: Path, entry_id: str, *, title: str, description: str,
                   output_dir: Path | None = None, overwrite=False,
                   composition_annotations: Path | None = None):
    require(isinstance(entry_id, str) and gallery.ENTRY_ID.fullmatch(entry_id), "Use a lowercase example ID with words separated by hyphens")
    require(title.strip() and description.strip(), "A title and description are required")
    annotations = (json.loads(Path(composition_annotations).read_text(encoding="utf-8"))
                   if composition_annotations is not None else None)
    root = Path(output_dir) if output_dir is not None else gallery.ROOT
    require(not root.is_symlink(), "The publication root cannot be a symlink")
    destination = root / entry_id
    require(not destination.is_symlink(), "The publication destination cannot be a symlink")
    require(not destination.exists() or overwrite, "This example already exists; use --overwrite to replace it")
    catalog_path = root / "index.json"
    require(not catalog_path.is_symlink(), "The publication catalog cannot be a symlink")
    catalog = json.loads(catalog_path.read_text()) if catalog_path.exists() else {"schema_version": 1, "examples": []}
    require(catalog.get("schema_version") == 1 and isinstance(catalog.get("examples"), list), "The publication catalog is invalid")
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".construction-import-", dir=root) as temporary:
        stage = Path(temporary) / entry_id
        stage.mkdir()
        with Export(source) as export:
            artifacts = {}
            for key, filename in (("report", "report.html"), ("items", "selected_items.csv"), ("results", "results.json")):
                with export.open(filename) as stream:
                    if key == "results":
                        info = checksum(stream)
                    else:
                        with (stage / filename).open("wb") as output:
                            info = checksum(stream, output)
                artifacts[key] = {"filename": filename, **info}
            with export.open("results.json") as stream:
                snapshot = derive_snapshot(stream, stage)
            with export.open("selected_items.csv") as stream:
                validate_csv(stream, snapshot)
            artifacts["summary_report"] = add_composition(stage, snapshot, title=title.strip(), annotations=annotations)
            archive_path = stage / "complete-results.zip"
            if export.archive is not None:
                shutil.copyfile(source, archive_path)
            else:
                with ZipFile(archive_path, "w", compression=ZIP_DEFLATED, compresslevel=6) as archive:
                    for name in FILES:
                        with export.open(name) as stream, archive.open(name, "w", force_zip64=True) as output:
                            shutil.copyfileobj(stream, output, length=64 * 1024)
            write_json(stage / "archive.json", {"results": export.members["results.json"]})
        with archive_path.open("rb") as stream:
            package = checksum(stream)
        artifacts["package"] = {"filename": "complete-results.zip", **package,
                                "package_id": package["sha256"], "chunk_bytes": gallery.CHUNK_BYTES}
        review = snapshot["review"]
        entry = {
            "id": entry_id, "title": title.strip(), "description": description.strip(),
            "run_id": review["run_id"], "result_state": review.get("metadata", {}).get("result_state", "partial"),
            "assessed_count": sum(item["status"] == "complete" for item in snapshot["items"]),
            "selected_count": len(review["screening"]["items"]),
            "coverage_complete": (review.get("selection") or {}).get("fully_satisfied") is True,
            "artifacts": artifacts,
        }
        write_json(stage / "snapshot.json", snapshot)
        updated = [value for value in catalog["examples"] if value["id"] != entry_id] + [entry]
        write_json(Path(temporary) / "index.json", {"schema_version": 1, "examples": sorted(updated, key=lambda item: item["title"])})
        backup = Path(temporary) / "previous"
        if destination.exists():
            destination.rename(backup)
        published = False
        try:
            stage.rename(destination)
            published = True
            (Path(temporary) / "index.json").replace(catalog_path)
        except OSError:
            if published:
                shutil.rmtree(destination)
            if backup.exists():
                backup.rename(destination)
            raise
    return entry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--id", required=True, dest="entry_id")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--composition-annotations", type=Path,
                        help="Optional reviewed format descriptions tied to selected item IDs")
    args = parser.parse_args()
    try:
        entry = import_example(**vars(args))
    except (OSError, BadZipFile, ValueError, TypeError, KeyError) as error:
        parser.exit(1, f"Import refused: {error}\n")
    print(json.dumps(entry, indent=2))


if __name__ == "__main__":
    main()
