"""Build an offline, allowlisted snapshot of a Caliper item-analysis run."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

from .catalog import is_generic_spec
from .report import generate_report
from .scoring import is_score_spec
from .storage import run_lock


ARTIFACTS = (
    "report.html", "items.csv", "summary.json", "classifier_spec.json", "review.csv",
    "dataset.json", "profile.json", "evidence.json", "items.jsonl", "direct_context.json",
    "specification.json", "classifier_spec.original.json", "run.json", "execution.json",
    "results.jsonl", "generation_request.json", "generation_attempts.json",
    "requests.jsonl", "classification_requests.jsonl", "preview_requests.jsonl",
    "usage.json", "usage_ledger.json", "usage_ledger.jsonl", "website_provenance.json",
    "review_selection.json", "review_comparison.json", "original_benchmark_report.pdf",
)
MODEL_FIELDS = {"provider", "model", "model_id", "reasoning_effort", "max_tokens", "request_mode"}
USAGE_FIELDS = {"input_tokens", "output_tokens", "cached_input_tokens", "reasoning_tokens", "latency_ms",
                "model_calls", "calls", "calls_with_usage", "calls_without_usage", "cost_usd"}
ROOT_ARTIFACTS = {"report.html", "items.csv", "summary.json", "classifier_spec.json", "review.csv", "original_benchmark_report.pdf"}


def _archive_name(name: str) -> str:
    return name if name in ROOT_ARTIFACTS else f"audit/{name}"


def _json(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def _safe_file(directory: Path, name: str) -> Path | None:
    path = directory / name
    # A known filename must still not be a symlink into private runtime storage.
    if path.is_symlink():
        raise ValueError(f"Cannot export a symlink as {name}")
    if not path.exists():
        return None
    if not path.is_file() or path.resolve().parent != directory:
        raise ValueError(f"Export artifact is not a regular run file: {name}")
    return path


def _read(directory: Path, name: str, default=None):
    path = _safe_file(directory, name)
    return json.loads(path.read_text(encoding="utf-8")) if path else default


def _records(path: Path):
    if path.exists():
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                if line.strip():
                    yield json.loads(line)


def _slug(value, length: int = 45) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")[:length].strip("-") or "unspecified"


def _snapshot_status(summary: dict, status: str, scope: str | None) -> str:
    selected = summary["experiment"]
    if status in {"cancelled", "failed"}:
        return f"{status}-partial"
    if not selected["selected_items"]:
        return "specification-only"
    if summary["complete_snapshot"]:
        return "snapshot-complete"
    if (selected["selected_completed_items"] == selected["selected_items"]
            and not selected["invalid_item_classifier_judgments"]):
        return "pilot-complete" if scope == "pilot" else "selected-sample-complete"
    return "partial-results"


def _selected_ids(directory: Path, summary: dict, spec: dict) -> list[str]:
    execution = _read(directory, "execution.json", {})
    if "selected_item_ids" in execution:
        return execution["selected_item_ids"]
    items = _records(directory / "items.jsonl")
    if "target_items" in execution:
        from itertools import islice
        return [item["item_id"] for item in islice(items, execution["target_items"])]
    if not is_generic_spec(spec) and not is_score_spec(spec):
        return [item["item_id"] for item in items]
    result_ids = {record["item_id"] for record in _records(directory / "results.jsonl")}
    return [item["item_id"] for item in items if item["item_id"] in result_ids]


def _blank_review(directory: Path, spec: dict, selected_ids: list[str], stream) -> None:
    """Create a fresh worksheet from inputs, never from existing human responses."""
    if is_score_spec(spec):
        from .score_report import write_blank_review
        selected = set(selected_ids)
        write_blank_review((item for item in _records(directory / "items.jsonl") if item["item_id"] in selected), stream)
        return
    columns = ["item_id", "content", "reference_answer", "grading_criterion"]
    classifiers = [c for c in spec["classifiers"] if c.get("applicable", True)]
    for classifier in classifiers:
        cid = classifier["id"]
        columns.append(cid)
        if is_generic_spec(spec):
            if cid == "input_ontology":
                columns += [f"{cid}.matched_category_ids", f"{cid}.scope_exclusion_source_ids"]
            columns += [f"{cid}.evidence", f"{cid}.justification"]
    columns.append("review_notes")
    writer = csv.DictWriter(stream, fieldnames=columns)
    writer.writeheader()
    selected = set(selected_ids)
    for item in _records(directory / "items.jsonl"):
        if item["item_id"] in selected:
            row = {}
            for key in columns[:4]:
                value = item.get(key)
                text = "" if value is None else value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
                row[key] = "'" + text if text.lstrip().startswith(("=", "+", "-", "@")) else text
            writer.writerow(row)


def build_results_package(run_dir: Path, *, run_id: str, status: str,
                          scope: str | None = None, created_at: str | None = None,
                          updated_at: str | None = None, usage: dict | None = None,
                          model: dict | None = None, assessment_pdf: Path | None = None) -> Path:
    """Return a descriptive ZIP path under ``run_dir/generated_exports``.

    Only explicit artifact names and public metadata are included. The caller
    must finish the current phase first; the run lock rejects concurrent writers.
    Missing historical artifacts are listed, never reconstructed as exact logs.
    """
    directory = Path(run_dir).resolve()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with run_lock(directory):
        # Check every input before report generation can follow a replaced link.
        for name in ARTIFACTS:
            _safe_file(directory, name)
        if assessment_pdf is not None:
            supplied = Path(assessment_pdf)
            if supplied.resolve() != directory / "original_benchmark_report.pdf" or supplied.is_symlink():
                raise ValueError("The original PDF must be the frozen original_benchmark_report.pdf inside the run")
            if _safe_file(directory, "original_benchmark_report.pdf") is None:
                raise ValueError("The frozen original benchmark PDF is unavailable")
        metadata = {"run_id": run_id, "status": status, "scope": scope,
                    "created_at": created_at, "updated_at": updated_at, "exported_at": now}
        summary = generate_report(directory, run_metadata=metadata)
        spec = _read(directory, "classifier_spec.json")
        evidence = _read(directory, "evidence.json", {})
        config = _read(directory, "run.json", {})
        selected_ids = _selected_ids(directory, summary, spec)
        snapshot_status = _snapshot_status(summary, status, scope)
        export_dir = directory / "generated_exports"
        if export_dir.is_symlink():
            raise ValueError("Export directory must not be a symlink")
        export_dir.mkdir(exist_ok=True)
        filename = "-".join((_slug(summary["benchmark"]), _slug(summary["deployment"], 30),
                             now[:10], _slug(run_id, 20), snapshot_status)) + ".zip"
        output = export_dir / filename
        entries, missing = [], []
        handle = tempfile.NamedTemporaryFile(prefix=".package-", suffix=".tmp", dir=export_dir, delete=False)
        temporary = Path(handle.name)
        handle.close()
        try:
            with ZipFile(temporary, "w", compression=ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
                def write_member(name: str, source, kind: str) -> None:
                    digest, size = hashlib.sha256(), 0
                    with archive.open(name, "w", force_zip64=True) as destination:
                        while chunk := source.read(1024 * 1024):
                            destination.write(chunk)
                            digest.update(chunk)
                            size += len(chunk)
                    entries.append({"path": name, "sha256": digest.hexdigest(), "bytes": size, "kind": kind})

                def virtual(name: str, data: bytes, kind: str = "export_metadata") -> None:
                    write_member(name, io.BytesIO(data), kind)

                for name in ARTIFACTS:
                    path = _safe_file(directory, name)
                    if path:
                        with path.open("rb") as source:
                            write_member(_archive_name(name), source, "saved_artifact")
                    else:
                        missing.append({"path": _archive_name(name), "reason": "Not present in the saved run"})
                scoring = evidence.get("scoring")
                virtual("original_assessment.json", _json({
                    "benchmark": evidence.get("benchmark", summary["benchmark"]),
                    "deployment": evidence.get("deployment"),
                    "assessment_status": "available" if scoring is not None else evidence.get("assessment_status", "not_supplied"),
                    "scoring": scoring, "context_artifact": "audit/evidence.json",
                }))
                for cid, prompt in config.get("prompts", {}).items():
                    if is_score_spec(spec) and cid == "assess_item" and isinstance(prompt, str):
                        virtual("audit/prompts/assess_item.md", prompt.encode("utf-8"), "frozen_prompt")
                        continue
                    if cid in {c["id"] for c in spec["classifiers"]} and isinstance(prompt, str):
                        virtual(f"audit/prompts/classify_{_slug(cid).replace('-', '_')}.md", prompt.encode("utf-8"), "frozen_prompt")
                if not is_score_spec(spec):
                    generation = _read(directory, "generation_request.json", {})
                    provenance = _read(directory, "website_provenance.json", {})
                    generation_system = generation.get("system", provenance.get("generation_system"))
                    if isinstance(generation_system, str):
                        virtual("audit/prompts/generation_system.md", generation_system.encode("utf-8"), "frozen_prompt")
                    else:
                        missing.append({"path": "audit/prompts/generation_system.md", "reason": "No saved generation request with a system prompt"})
                    if isinstance(provenance.get("generation_user_template"), str):
                        virtual("audit/prompts/generation_user_template.md", provenance["generation_user_template"].encode("utf-8"), "frozen_prompt")
                    else:
                        missing.append({"path": "audit/prompts/generation_user_template.md", "reason": "No frozen generation user-template snapshot"})
                if not config.get("prompts"):
                    missing.append({"path": "audit/prompts/assess_item.md" if is_score_spec(spec) else "audit/prompts/classify_*.md",
                                    "reason": "No frozen scoring prompt snapshots in run.json"})
                if selected_ids:
                    with tempfile.TemporaryFile(mode="w+", encoding="utf-8", newline="", dir=export_dir) as worksheet:
                        _blank_review(directory, spec, selected_ids, worksheet)
                        worksheet.flush()
                        worksheet.seek(0)
                        # TextIOWrapper is avoided here so large worksheets stay streamed.
                        class EncodedReader:
                            def read(self, size):
                                return worksheet.read(size).encode("utf-8")
                        write_member("review/blank_review.csv", EncodedReader(), "fresh_blind_worksheet")
                else:
                    missing.append({"path": "review/blank_review.csv", "reason": "No classification selection has been recorded"})
                virtual("README.txt", _readme(snapshot_status, six_scores=is_score_spec(spec)).encode("utf-8"))
                public_model = {key: value for key, value in {**config, **(model or {})}.items() if key in MODEL_FIELDS}
                saved_usage = _read(directory, "usage.json", {})
                public_usage = {key: value for key, value in {**saved_usage, **(usage or {})}.items() if key in USAGE_FIELDS}
                manifest = {
                    "schema_version": "caliper_item_package_v1", **metadata,
                    "snapshot_status": snapshot_status, "benchmark": summary["benchmark"],
                    "deployment": summary["deployment"], "model": public_model or None,
                    "usage": public_usage or None, "dataset": summary["dataset"],
                    "usage_note": "Totals describe recorded usage only. Failed or cancelled requests may have unknown provider usage; inspect audit/usage_ledger.jsonl or audit/usage_ledger.json. Missing usage is not evidence of zero billable calls.",
                    "selected_item_ids": selected_ids,
                    "counts": {"prepared_items": summary["total_items"], **summary["experiment"]},
                    "complete_snapshot": summary["complete_snapshot"],
                    "artifacts": entries, "missing_artifacts": missing,
                    "checksum_note": "SHA-256 values cover each archived member's exact uncompressed bytes. manifest.json is excluded from its own checksum list.",
                }
                if is_score_spec(spec):
                    manifest.update(analysis_type="six_scores", rubric_version=spec["rubric_version"])
                archive.writestr("manifest.json", _json(manifest))
            temporary.replace(output)
        finally:
            temporary.unlink(missing_ok=True)
        return output


def _readme(snapshot_status: str, *, six_scores: bool = False) -> str:
    if six_scores:
        return f"""CALIPER SIX-SCORE ITEM ANALYSIS — OFFLINE RESULTS PACKAGE

Snapshot: {snapshot_status}

Extract the whole ZIP and open report.html in a browser. It needs no server or
internet connection. Keep companion file names so relative links still work.
The report shows one row per item and six 1–5 deployment-alignment scores:
Input Ontology, Input Content, Input Form, Output Ontology, Output Content,
and Output Form. Open each score to inspect its explanation, evidence, and gaps.
Unknown means insufficient evidence. Operational errors and pending items are
separate states. An item can be complete while some scores remain Unknown.

items.csv contains all prepared items, selection flags, scores, explanations,
evidence, and information gaps. summary.json records the selected-item score
distributions, selected progress, and full prepared-population counts. No item
rank or combined benchmark score is computed. A completed pilot does not imply
completion of the full prepared snapshot or establish benchmark-wide coverage.

classifier_spec.json contains the fixed six-dimension rubric, shared deployment
requirements, benchmark documentation, and their source references. Context is
assembled once from saved evidence; one primary model call returns all six
judgments for an item. Repairs and retries add calls. Original benchmark scores
are not used as item-scoring evidence and are never overwritten by item scores.
audit/evidence.json retains the original evidence; original_assessment.json
contains benchmark scoring when supplied. original_benchmark_report.pdf is
included only when a saved original PDF exists. Missing assessments are explicit.

INDEPENDENT HUMAN REVIEW
Make a separately named copy of review/blank_review.csv for each reviewer.
Share that blank copy with classifier_spec.json and the relevant evidence,
without model predictions or other reviewers' annotations. Enter 1–5 or unknown
for each dimension, a justification, evidence, and information gaps. Unknown
requires an explanation of the missing information; blank scores mean unreviewed.
Keep reviewers' files separate. Root review.csv is preserved exactly and may
already contain human annotations. It is not necessarily a blank template.
audit/review_comparison.json, when present, records agreement and per-dimension
numeric error; report.html states whether the comparison matches saved inputs.

AUDIT AND REPRODUCIBILITY
manifest.json identifies the run, timestamps, scope, status, selected IDs, model,
available usage, member sizes, SHA-256 checksums, and missing artifacts. The
audit/ folder contains saved input items, context provenance, frozen scoring
prompts, exact requests, raw responses, results, configuration, and usage logs.
Some artifacts appear only after scoring starts. Context assembly does not
require a context-generation model request. Missing logs mean unavailable,
not zero calls. Usage totals can omit unknown usage from failed or cancelled
provider calls and are not guaranteed billing totals. Previews are not execution.
No historical request is reconstructed as an exact log. Future model calls
may produce different judgments. Credentials and private website access files
are outside the artifact allowlist and are not included.
"""
    return f"""CALIPER ITEM ANALYSIS — OFFLINE RESULTS PACKAGE

Snapshot: {snapshot_status}

Extract the whole ZIP and open report.html in a browser. It needs no server or
internet connection. Keep the relative file names so report links still work.
The report starts with selected-item counts and four classifier statistics.
The separate original assessment retains the six benchmark-level dimensions.
Item judgments do not change those original scores.

items.csv includes all prepared items with per-classifier status and evidence.
summary.json stores counts and explicit percentage denominators. Pending,
operational errors, invalid responses, and insufficient evidence are different.
An incomplete package still includes every saved successful judgment. A finished
pilot is a completed selection, not completion of the full prepared snapshot.

audit/evidence.json retains original assessment context; original_assessment.json
contains its scoring object when supplied. original_benchmark_report.pdf is
included only when a saved original PDF exists. No missing assessment is inferred.

INDEPENDENT HUMAN REVIEW
Make a separately named copy of review/blank_review.csv for each reviewer.
Share that blank copy with classifier_spec.json and the relevant evidence, without
model predictions or other reviewers' annotations. Enter raw judgment IDs, item
evidence, and a justification. For Input Ontology, also enter category IDs.
Keep reviewers' files separate. The package's root review.csv is preserved exactly
and may already contain human annotations; it is not necessarily a blank template.
audit/review_comparison.json, when present, records a saved comparison; report.html
identifies whether that comparison still matches the saved inputs.

AUDIT AND REPRODUCIBILITY
manifest.json identifies this run, timestamps, scope, status, selection, model,
available usage, member sizes, SHA-256 checksums, and missing artifacts. Missing
timestamps or logs mean unavailable, not zero calls or successful completion.
The audit/ folder contains saved frozen prompts, requests, responses, input items,
configuration, and usage logs. Recorded usage totals can omit unknown usage for
failed or cancelled provider calls; they are not guaranteed billing totals.
Preview requests are previews, not proof of execution.
No historical request is reconstructed and presented as an exact request log.
This package can support audit or a new experiment, but cannot guarantee that a
future model call reproduces the same labels. Credentials and website access
metadata are outside the artifact allowlist and are not included.
"""
