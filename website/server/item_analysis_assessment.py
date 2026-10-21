"""Freeze an existing benchmark assessment for its subsequent item analysis.

Only server-resolved assessment artifacts are accepted. Dataset selection never
selects a deployment or a pre-existing classifier specification.
"""

from __future__ import annotations

from copy import deepcopy
import csv
import io
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit

from fastapi import HTTPException
import yaml

from anthropic_api_package_release.item_analysis import data, prepare, report
from anthropic_api_package_release.item_analysis.storage import read_json, write_json
from . import active_runs, db, gallery, logging_gate, pipeline_runner

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_UPLOAD_ITEMS = 50_000


def _text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _step_output(run_id: str, name: str) -> str:
    with db.connect() as conn:
        row = conn.execute(
            "SELECT blob_key FROM steps WHERE run_id = ? AND step_name = ? "
            "AND status = 'success' ORDER BY started_at DESC LIMIT 1", (run_id, name),
        ).fetchone()
    if row and row["blob_key"]:
        try:
            value = read_json(logging_gate.DEFAULT_BLOB_ROOT / row["blob_key"]).get("output_text")
            return value if isinstance(value, str) else ""
        except (OSError, ValueError, TypeError):
            pass
    return ""


def _metadata_document(text: str) -> dict:
    """Read only named metadata fields, never identifiers mentioned in prose."""
    if not isinstance(text, str):
        return {}
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:yaml|yml)?\s*\n", "", text)
        text = re.sub(r"\n```\s*$", "", text)
    try:
        parsed = yaml.safe_load(text)
    except (yaml.YAMLError, ValueError, RecursionError):
        return {}
    if isinstance(parsed, list):
        parsed = {key: value for entry in parsed if isinstance(entry, dict) for key, value in entry.items()}
    return parsed if isinstance(parsed, dict) else {}


def benchmark_identity(scoring: dict, title: str, benchmark_yaml: str = "", metadata: str = "") -> dict:
    """Expose identity evidence separately from the target deployment context."""
    documents = [("benchmark.yaml", _metadata_document(benchmark_yaml)),
                 ("metadata", _metadata_document(metadata))]
    unknown = {"unknown", "not documented", "not specified", "not available", "n/a", "none", "null"}

    def clean(value):
        if not isinstance(value, (str, int)) or isinstance(value, bool):
            return None
        value = str(value).strip()
        return value if value and value.casefold().strip("[]") not in unknown else None

    evidence = {}

    def scalar(field, keys):
        for filename, document in documents:
            for key in keys:
                value = clean(document.get(key))
                if value:
                    evidence[field] = f"{filename}:{key}"
                    return value
        return None

    def values(field, keys, *, urls=False):
        for filename, document in documents:
            found = []
            fields = []
            for key in keys:
                value = document.get(key)
                entries = value if isinstance(value, list) else value.split(",") if isinstance(value, str) else []
                for entry in entries:
                    text = clean(entry)
                    if not text:
                        continue
                    if urls:
                        try:
                            url = urlsplit(text)
                            if url.scheme not in {"http", "https"} or not url.netloc or url.username or url.password:
                                continue
                        except ValueError:
                            continue
                    if text not in found:
                        found.append(text)
                        fields.append(f"{filename}:{key}")
            if found:
                evidence[field] = ", ".join(dict.fromkeys(fields))
                return found
        return []

    name = scalar("name", ("name", "benchmark_name"))
    if not name:
        name = scoring["benchmark"]
        evidence["name"] = "scoring.json:benchmark"
    full_name = scalar("full_name", ("full_name", "fullName"))
    if not full_name and clean(title) and title != name:
        full_name = title
        evidence["full_name"] = "assessment display name"
    aliases = values("aliases", ("aliases", "alternate_names"))
    for alternate in (scoring["benchmark"], title):
        if clean(alternate) and alternate not in {name, full_name} and alternate not in aliases:
            aliases.append(alternate)
            evidence["aliases"] = ", ".join(filter(None, (evidence.get("aliases"), "assessment benchmark name")))
    return {
        "name": name, "full_name": full_name, "aliases": aliases,
        "paper_urls": values("paper_urls", ("paper_url", "paper_urls", "paperURL"), urls=True),
        "source_urls": values("source_urls", ("source_url", "source_urls", "dataset_url", "sourceURL"), urls=True),
        "year": scalar("year", ("year", "publication_year")),
        "languages": values("languages", ("languages", "language")),
        "version": scalar("version", ("version", "benchmark_version", "dataset_version")),
        "evidence": evidence,
    }


def resolve(kind: str, assessment_id: str) -> dict:
    """Resolve by the existing bearer-run-ID or public gallery-ID access model."""
    evidence_documents = {}
    if kind == "gallery":
        original = gallery.get_report(assessment_id)
        if original is None:
            raise HTTPException(404, "This benchmark assessment is not available.")
        # get_report performed the gallery whitelist check before this path is used.
        directory = gallery._slug_dir(gallery._ASSESSMENTS_ROOT / assessment_id)
        scoring = original["scoring"]
        deployment = original["deployment_description"]
        summary = original["elicitation_summary"]
        dataset_report = _text(directory / "dataset_analysis_report.md") if directory else ""
        title = original["benchmark_name"]
        benchmark_yaml = _text(directory / "benchmark.yaml") if directory else ""
        metadata = _text(directory / "metadata.yaml") or _text(directory / "metadata.txt") if directory else ""
    elif kind == "run":
        # Keep arbitrary IDs away from filesystem joins even if a database has
        # been populated manually with an invalid identifier.
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,160}", assessment_id):
            raise HTTPException(404, "This benchmark assessment is not available.")
        with db.connect() as conn:
            exists = conn.execute("SELECT 1 FROM runs WHERE run_id = ?", (assessment_id,)).fetchone()
        if exists is None:
            raise HTTPException(404, "This benchmark assessment is not available.")
        active = active_runs.store.get(assessment_id)
        artifacts = active.artifacts if active else {}
        # Retain actual in-memory source outputs before the upstream run expires.
        # Select evidence fields explicitly; never copy credentials or PDF bytes.
        for field, filename in (("paper_summary", "paper_summary.md"), ("region_yaml", "region.yaml"),
                                ("scaffold_yaml", "region_scaffold.yaml"), ("quote_registry", "quote_registry.md"),
                                ("elicitation_answers", "elicitation_answers.json"), ("elicitation_questions", "elicitation_questions.json")):
            content = artifacts.get(field)
            if content:
                evidence_documents[filename] = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False)
        # Read without creating a directory. Tuple files are the report's
        # session artifacts and do not depend on opt-in trace logging.
        directory = pipeline_runner._WORKSPACE_ROOT / assessment_id
        scoring = artifacts.get("scoring")
        if not scoring:
            try:
                scoring = read_json(directory / "scoring.json")
            except (OSError, ValueError):
                from .app import _parse_scoring_json
                scoring = _parse_scoring_json(_step_output(assessment_id, "7-score"))
        deployment = (active.deployment_description if active else "") or _text(directory / "deployment_description.txt")
        summary = artifacts.get("elicitation_summary") or _text(directory / "elicitation_summary.md")
        summary = summary or _step_output(assessment_id, "2-summary")
        dataset_report = artifacts.get("dataset_analysis_text") or _text(directory / "dataset_analysis_report.md")
        title = scoring.get("benchmark", "") if isinstance(scoring, dict) else ""
        benchmark_yaml = artifacts.get("benchmark_yaml") or _text(directory / "benchmark.yaml") or _step_output(assessment_id, "3b-synthesize")
        metadata = artifacts.get("metadata") or _text(directory / "metadata.yaml") or _text(directory / "metadata.txt") or _step_output(assessment_id, "1-metadata")
    else:
        raise HTTPException(422, "Choose a run or gallery assessment.")
    if (not isinstance(scoring, dict) or not isinstance(scoring.get("dimensions"), dict)
            or not isinstance(scoring.get("benchmark"), str) or not scoring["benchmark"].strip()):
        raise HTTPException(409, "Complete the benchmark assessment before analyzing its items.")
    if any(not isinstance(scoring["dimensions"].get(dimension), dict) for dimension in report.DIMENSIONS):
        raise HTTPException(409, "The benchmark assessment must contain all six dimension assessments before item analysis can start.")
    if not isinstance(deployment, str) or not deployment.strip():
        raise HTTPException(409, "The deployment context for this assessment is no longer available.")
    return deepcopy({
        "kind": kind, "id": assessment_id, "benchmark": scoring["benchmark"],
        "benchmark_name": title, "deployment": deployment, "scoring": scoring,
        "benchmark_identity": benchmark_identity(scoring, title, benchmark_yaml, metadata),
        "elicitation_summary": summary or "Elicitation summary is unavailable for this original assessment.",
        "dataset_analysis_report": dataset_report or "No dataset analysis report was recorded for this original assessment.",
        "evidence_directory": str(directory) if directory else None,
        "missing_evidence": [name for name, value in (("elicitation_summary.md", summary), ("dataset_analysis_report.md", dataset_report)) if not value],
        "evidence_documents": {**evidence_documents, **{name: value for name, value in (("benchmark.yaml", benchmark_yaml), ("metadata.yaml", metadata)) if value}},
    })


def public_assessment(assessment: dict) -> dict:
    return {key: assessment[key] for key in (
        "kind", "id", "benchmark", "benchmark_name", "deployment", "elicitation_summary", "scoring",
        "benchmark_identity", "direct_context", "analysis_basis", "assessment_status",
    ) if key in assessment}


def _name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def dataset_sources(assessment: dict, entries: list[dict]) -> list[dict]:
    """Keep matching datasets once, excluding their old deployment contexts."""
    names = {_name(assessment["benchmark"]), _name(assessment["benchmark_name"])}
    result, seen = [], set()
    for entry in entries:
        benchmark = entry["benchmark"]
        if not names.intersection({_name(benchmark), _name(entry.get("benchmark_title", benchmark))}):
            continue
        identity = (benchmark, entry.get("source_url"), entry.get("source_revision"))
        if identity in seen:
            continue
        seen.add(identity)
        result.append({
            "id": entry["id"], "title": entry.get("benchmark_title", benchmark),
            "benchmark": benchmark, "item_count": entry["item_count"],
            "available": entry["available"], "source_label": entry["source_label"],
            **{key: entry[key] for key in ("source_url", "source_revision", "unavailable_reason") if key in entry},
        })
    return result


def parse_upload(payload: bytes, filename: str) -> list[dict]:
    """Validate bounded uploads before scheduling any paid model request."""
    if not payload or len(payload) > MAX_UPLOAD_BYTES:
        raise HTTPException(400, "Upload a nonempty CSV or JSON file no larger than 10 MiB.")
    suffix = Path(filename).suffix.lower()

    def invalid_constant(_value):
        raise ValueError("Non-finite JSON values are not supported")

    try:
        text = payload.decode("utf-8-sig")
        if suffix == ".json":
            rows = json.loads(text, parse_constant=invalid_constant)
            if not isinstance(rows, list):
                raise ValueError()
        elif suffix == ".csv":
            reader = csv.DictReader(io.StringIO(text))
            if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
                raise ValueError()
            rows = list(reader)
        else:
            raise HTTPException(400, "Upload a .csv file or a .json array of item objects.")
        if not rows or len(rows) > MAX_UPLOAD_ITEMS:
            raise HTTPException(400, f"Upload between 1 and {MAX_UPLOAD_ITEMS:,} items.")
        normalized, seen = [], set()
        evidence_fields = {*data.EVIDENCE_FIELDS, "question", "choices", "options", "answer"}
        for index, row in enumerate(rows, 1):
            if not isinstance(row, dict) or None in row:
                raise ValueError()
            row = dict(row)
            if row.get("item_id") is None or row.get("item_id") == "":
                row["item_id"] = f"uploaded-{index}"
            if "content" not in row:
                raise ValueError()
            item = data._normalize(row, index)
            if item["item_id"] in seen:
                raise HTTPException(400, "Each uploaded item_id must be unique.")
            seen.add(item["item_id"])
            # Uniform JSON-valued columns preserve mixed structured evidence
            # without relying on Arrow's cross-row type inference. Decode CSV
            # JSON cells first so they round-trip as structures, not JSON prose.
            row = {key: data._decode(value) if key in evidence_fields else value for key, value in row.items()}
            normalized.append({key: json.dumps(value, ensure_ascii=False, allow_nan=False)
                               if key not in {"item_id", "benchmark_id"} else str(value) for key, value in row.items()})
        return normalized
    except HTTPException:
        raise
    except (UnicodeError, ValueError, TypeError, csv.Error, RecursionError):
        raise HTTPException(400, "Invalid item file. Each row needs nonempty content; item_id must be unique when supplied. JSON must be an array of objects.") from None


def prepare_upload(directory: Path, assessment: dict, rows: list[dict], payload_sha256: str, suffix: str) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq

    with TemporaryDirectory(prefix="upload-", dir=directory.parent) as temporary:
        path = Path(temporary) / "items.parquet"
        # Explicit union retains fields first encountered in later rows.
        columns = sorted({key for row in rows for key in row})
        pq.write_table(pa.Table.from_pylist(rows, schema=pa.schema([(name, pa.string()) for name in columns])), path)
        dataset = data.prepare_data(path, directory, benchmark=assessment["benchmark"],
                                    source_repo="user-upload", source_table=f"items{suffix}")
    dataset["source"].update({"normalized_sha256": dataset["source"]["sha256"], "sha256": payload_sha256})
    write_json(directory / "dataset.json", dataset)


def attach_assessment(directory: Path, assessment: dict, *, confirmed_source: bool = False) -> None:
    """Replace all preset assessment evidence before generating fresh criteria."""
    dataset = read_json(directory / "dataset.json")
    if not confirmed_source and _name(dataset["benchmark"]) not in {_name(assessment["benchmark"]), _name(assessment["benchmark_name"])}:
        raise ValueError("The prepared snapshot does not match the selected assessment")
    dataset["source_benchmark"] = dataset["benchmark"]
    documents = {
        **assessment.get("evidence_documents", {}),
        "deployment_description.txt": assessment["deployment"],
        "elicitation_summary.md": assessment["elicitation_summary"],
        "dataset_analysis_report.md": assessment["dataset_analysis_report"],
        "framework.yaml": (prepare.PIPELINE_DIR / "framework.yaml").read_text(encoding="utf-8"),
    }
    for missing in assessment.get("missing_evidence", []):
        documents.pop(missing, None)
    registry, roles, gaps = prepare.build_sources(
        directory, documents, scoring=assessment["scoring"],
        assessment_dir=Path(assessment["evidence_directory"]) if assessment.get("evidence_directory") else None,
    )
    gaps.extend(f"The original assessment has no available {name} contents." for name in assessment.get("missing_evidence", []))
    evidence = {
        "benchmark": assessment["benchmark"], "deployment": assessment["deployment"],
        "scoring": assessment["scoring"], "elicitation_summary": assessment["elicitation_summary"],
        "dataset_analysis_report": assessment["dataset_analysis_report"],
        "registry": registry, "source_roles": roles, "evidence_gaps": gaps,
        "assessment": {"kind": assessment["kind"], "id": assessment["id"]},
        "benchmark_identity": assessment.get("benchmark_identity"),
    }
    write_json(directory / "evidence.json", evidence)
    dataset["benchmark"] = assessment["benchmark"]
    dataset["source"].pop("path", None)
    dataset["evidence_sha256"] = data.file_sha256(directory / "evidence.json")
    dataset["assessment"] = evidence["assessment"]
    dataset["benchmark_identity_confirmed"] = True
    write_json(directory / "dataset.json", dataset)
    # A source's historical rules must never become this assessment's rules.
    for name in ("provided_spec.json", "classifier_spec.original.json"):
        (directory / name).unlink(missing_ok=True)
