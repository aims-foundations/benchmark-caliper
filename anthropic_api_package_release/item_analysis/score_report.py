"""Offline reporting for six independent ordinal assessments of each item.

This reader is intentionally separate from historical categorical reports. Scores
describe individual items; neither their distribution nor completion creates a
replacement benchmark assessment.
"""

from __future__ import annotations

import csv
from collections import Counter
from contextlib import contextmanager
from itertools import islice
from pathlib import Path
from tempfile import NamedTemporaryFile

from . import storage
from .classify import read_results
from .report import (
    _ItemPopulation, _agreement, _comparison_inputs, _csv_text, _escape,
    _read_json, _render_fields, _text, _write_json,
)
from .scoring import DIMENSIONS, validate_score_spec


def _load(directory: Path):
    dataset = _read_json(directory / "dataset.json", {})
    if all(key in dataset for key in ("items_sha256", "profile_sha256", "evidence_sha256")):
        storage.check_prepared(directory)
    if (directory / "specification.json").exists():
        storage.check_specification(directory)
    spec = validate_score_spec(_read_json(directory / "classifier_spec.json"),
                               benchmark=dataset.get("benchmark"))
    items = _ItemPopulation(directory / "items.jsonl")
    results = read_results(directory / "results.jsonl")
    if set(results) - items.item_ids:
        raise ValueError("Results contain items outside the prepared dataset")
    if any(result.get("schema_version") != "caliper_item_result_v4" for result in results.values()):
        raise ValueError("Six-score reports require six-score result records")
    return spec, dataset, items, results


def _selected_items(items, selected_ids: set[str]):
    """Yield selected evidence in saved order without retaining its contents."""
    remaining = set(selected_ids)
    if not remaining:
        return
    for item in items:
        if item["item_id"] in remaining:
            yield item
            remaining.remove(item["item_id"])
            if not remaining:
                break


def _selection_ids(directory: Path, items, results: dict) -> list[str]:
    execution = _read_json(directory / "execution.json", {})
    if "selected_item_ids" in execution:
        selected = execution["selected_item_ids"]
        if (not isinstance(selected, list) or any(not isinstance(value, str) for value in selected)
                or len(selected) != len(set(selected)) or set(selected) - items.item_ids):
            raise ValueError("Execution selection must contain unique prepared item IDs")
        return [item["item_id"] for item in _selected_items(items, set(selected))]
    if "target_items" in execution:
        target = execution["target_items"]
        if type(target) is not int or target < 0:
            raise ValueError("Execution target_items must be a nonnegative integer")
        return [item["item_id"] for item in islice(items, target)]
    return [item["item_id"] for item in _selected_items(items, set(results))]


@contextmanager
def _atomic_text(path: Path):
    """Publish a finished artifact while retaining its previous copy on failure."""
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", newline="", dir=path.parent,
                                prefix=f".{path.name}-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            yield stream
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _dimension_summary(definition: dict, results: dict, total: int) -> dict:
    scores = Counter(result["dimensions"][definition["id"]]["score"]
                     for result in results.values() if result["status"] == "complete")
    completed = sum(scores.values())
    known = completed - scores[None]
    errors = sum(result["status"] == "error" for result in results.values())
    return {
        **definition, "name": definition["id"].replace("_", " ").title(),
        "counts": {str(score): scores[score] for score in range(1, 6)},
        "known": known, "unknown": scores[None],
        "mean_score": sum(score * scores[score] for score in range(1, 6)) / known if known else None,
        "valid_judgments": completed, "errors": errors,
        "pending": total - completed - errors, "invalid": 0,
        "denominator": "counts describe selected items; mean_score uses only numeric scores from completed selected items; Unknown, operational errors, and pending items are excluded from the mean",
    }


def summarize_dimensions(definitions: list[dict], results: dict, total: int) -> list[dict]:
    """Summarize validated results for the selected population without writing files."""
    return [_dimension_summary(definition, results, total) for definition in definitions]


def _write_csv(directory: Path, items, results: dict, selected_ids: set[str]) -> None:
    columns = ["item_id", "selected", "status", "content", "reference_answer", "grading_criterion", "item_evidence", "error"]
    for dimension in DIMENSIONS:
        columns.extend(f"{dimension}.{field}" for field in
                       ("score", "status", "justification", "evidence", "information_gaps"))
    columns += ["analysis_type", "rubric_version"]
    with _atomic_text(directory / "items.csv") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for item in items:
            result = results.get(item["item_id"], {})
            state = result.get("status", "pending")
            row = {key: item.get(key) for key in ("item_id", "content", "reference_answer", "grading_criterion")}
            row.update(selected=item["item_id"] in selected_ids, status=state, item_evidence=item,
                       error=result.get("error", ""), analysis_type="six_scores",
                       rubric_version="caliper_item_rubric_v1")
            for dimension in DIMENSIONS:
                judgment = result.get("dimensions", {}).get(dimension, {})
                row[f"{dimension}.status"] = state
                if state == "complete":
                    score = judgment["score"]
                    row[f"{dimension}.score"] = "unknown" if score is None else score
                    row[f"{dimension}.status"] = "unknown" if score is None else "complete"
                    for field in ("justification", "evidence", "information_gaps"):
                        row[f"{dimension}.{field}"] = judgment[field]
            writer.writerow({key: _csv_text(value) for key, value in row.items()})


def review_columns() -> list[str]:
    columns = ["item_id", "content", "reference_answer", "grading_criterion", "item_evidence"]
    for dimension in DIMENSIONS:
        columns += [dimension, f"{dimension}.justification", f"{dimension}.evidence", f"{dimension}.information_gaps"]
    return [*columns, "review_notes"]


def write_blank_review(items, stream) -> None:
    """Write item evidence and empty human fields without reading predictions."""
    writer = csv.DictWriter(stream, fieldnames=review_columns())
    writer.writeheader()
    for item in items:
        row = {key: item.get(key) for key in ("item_id", "content", "reference_answer", "grading_criterion")}
        row["item_evidence"] = item
        writer.writerow({key: _csv_text(value) for key, value in row.items()})


def _review(directory: Path, items, selected: list[str], *, export_artifacts: bool) -> dict:
    if (directory / "review.csv").exists():
        return _read_json(directory / "review_selection.json", {"method": "existing worksheet preserved"})
    selection = {
        "schema_version": "caliper_item_review_v3", "analysis_type": "six_scores",
        "item_ids": selected,
        "method": "all selected items in saved dataset order" if selected else "awaiting experiment selection",
        "purpose": "independent human review; model scores are omitted",
        "instructions": (
            "Enter 1–5 or unknown for each dimension, plus justification and evidence. "
            "Use information_gaps to record missing evidence; unknown requires a gap. "
            "Blank scores mean unreviewed. Consult the fixed rubric and shared context in classifier_spec.json. "
            "Keep each reviewer's copy separate."
        ),
    }
    if selected:
        if export_artifacts:
            with _atomic_text(directory / "review.csv") as stream:
                write_blank_review(_selected_items(items, set(selected)), stream)
        storage.write_json(directory / "review_selection.json", selection)
    return selection


def generate_score_report(directory: Path, *, run_metadata: dict | None = None,
                          export_artifacts: bool = True) -> dict:
    """Save the summary; materialize portable reports only when requested."""
    spec, dataset, items, results = _load(directory)
    evidence = _read_json(directory / "evidence.json", {})
    selected = _selection_ids(directory, items, results)
    selected_ids = set(selected)
    selected_results = {key: value for key, value in results.items() if key in selected_ids}
    dimensions = summarize_dimensions(spec["classifiers"], selected_results, len(selected))
    completed = sum(value["status"] == "complete" for value in results.values())
    errors = sum(value["status"] == "error" for value in results.values())
    selected_completed = sum(value["status"] == "complete" for value in selected_results.values())
    selected_errors = sum(value["status"] == "error" for value in selected_results.values())
    config = _read_json(directory / "run.json", {})
    original = evidence.get("scoring")
    original_dimensions = original.get("dimensions", original) if isinstance(original, dict) else None
    summary = {
        "schema_version": spec["schema_version"], "report_schema_version": "caliper_item_report_v3",
        "analysis_type": "six_scores", "rubric_version": spec["rubric_version"],
        "benchmark": spec.get("benchmark", dataset.get("benchmark")),
        "deployment": spec.get("deployment_description", spec.get("deployment")),
        "original_deployment": evidence.get("deployment"),
        "specification": _read_json(directory / "specification.json", {}),
        "classification": {key: config.get(key) for key in
                           ("provider", "model_id", "reasoning_effort", "max_tokens", "request_mode", "prompt_sha256")} if config else None,
        "dataset": dataset, "total_items": len(items), "completed_items": completed,
        "error_items": errors, "pending_items": len(items) - completed - errors, "partial_items": 0,
        "complete_snapshot": bool(items) and completed == len(items),
        "scope": "all items in the prepared snapshot" if items and completed == len(items) else "incomplete run over the prepared snapshot",
        "interpretation": (
            "Each item receives six independent 1–5 alignment judgments against the shared deployment requirements. "
            "Unknown means insufficient evidence, not a low score or a processing failure. Counts describe selected items. "
            "Each dimension's average is the arithmetic mean of its numeric scores from completed selected items; "
            "Unknown, operational errors, and pending items are excluded. These six averages can be compared "
            "with the original benchmark dimensions, whose scores remain unchanged. "
            "Scores are not combined into an item rank or an overall benchmark score. "
            "An item's task relevance does not establish benchmark-wide coverage."
        ),
        "original_assessment": {key: original_dimensions.get(key) for key in DIMENSIONS} if original_dimensions else None,
        "original_report_available": (directory / "original_benchmark_report.pdf").is_file(),
        "dimensions": dimensions, "classifiers": dimensions,
        "experiment": {
            "classifier_count": 6, "dimension_count": 6, "benchmark_classifier_combinations": 6,
            "selected_items": len(selected), "selected_completed_items": selected_completed,
            "selected_error_items": selected_errors, "selected_partial_items": 0,
            "selected_pending_items": len(selected) - selected_completed - selected_errors,
            "expected_item_classifier_judgments": len(selected) * 6,
            "completed_item_classifier_judgments": selected_completed * 6,
            "error_item_classifier_judgments": selected_errors * 6,
            "invalid_item_classifier_judgments": 0,
            "pending_item_classifier_judgments": (len(selected) - selected_completed - selected_errors) * 6,
            "expected_primary_requests": len(selected),
            "request_policy": "one primary request per item returns all six dimensions; repairs and retries add calls",
            # v4 records retain cumulative attempt history across failed retries.
            "recorded_api_calls": sum(len(record.get("attempts", [])) for record in results.values()),
        },
    }
    if evidence.get("analysis_basis") == "deployment_requirements":
        summary.update(analysis_basis="deployment_requirements", analysis_scope="item_only", assessment_status="not_run",
                       requirements=evidence.get("requirements", {}), direct_context=evidence.get("direct_context"))
    if run_metadata:
        summary["run"] = {key: run_metadata[key] for key in
                          ("run_id", "status", "scope", "created_at", "updated_at", "exported_at")
                          if run_metadata.get(key) is not None}
    if export_artifacts:
        _write_csv(directory, items, results, selected_ids)
    summary["review_selection"] = _review(directory, items, selected, export_artifacts=export_artifacts)
    comparison = _read_json(directory / "review_comparison.json")
    if comparison:
        current_inputs = _comparison_inputs(directory, Path(comparison.get("review_path", "")))
        current = bool(current_inputs["review_sha256"]) and current_inputs == comparison.get("input_hashes")
        summary["review_comparison_status"] = {
            "current": current,
            "note": "Comparison matches saved results, context, and human review." if current else
                    "Saved comparison is stale; results, context, or human review changed. Rerun validate.",
        }
        if current:
            summary["review_comparison"] = comparison
    storage.write_json(directory / "summary.json", summary)
    if export_artifacts:
        _write_html(directory / "report.html", summary, items, results, selected_ids)
    return summary


def _html_parts(summary: dict, items, results: dict, selected_ids: set[str]):
    experiment = summary["experiment"]
    if summary.get("run", {}).get("status") in {"cancelled", "failed"}:
        readiness = "Stopped — saved results retained"
    elif not experiment["selected_items"]:
        readiness = "Context prepared — scoring not started"
    elif summary["complete_snapshot"]:
        readiness = "Prepared snapshot complete"
    elif experiment["selected_completed_items"] == experiment["selected_items"]:
        readiness = "Selected sample complete"
    else:
        readiness = "Scoring in progress — partial results"
    yield from ("<!doctype html><html lang='en'><head><meta charset='utf-8'>",
             "<meta name='viewport' content='width=device-width, initial-scale=1'>",
             "<meta http-equiv='Content-Security-Policy' content=\"default-src 'none'; style-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'\">",
             "<title>Caliper — six scores per item</title><style>",
             "body{font:16px/1.5 system-ui,sans-serif;color:#172b35;background:#f7f9fa;margin:0 auto;max-width:1250px;padding:28px}"
             "section{background:white;padding:24px;margin:20px 0;border:1px solid #d9e2e7;border-radius:12px}"
             "h1,h2,h3{line-height:1.25}table{border-collapse:collapse;width:100%}th,td{padding:12px;border-bottom:1px solid #d9e2e7;text-align:left;vertical-align:top}"
             "th{white-space:nowrap}.table-scroll{overflow:auto}summary{cursor:pointer}details{margin:8px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}"
             "a{color:#075f77}small{color:#526873}.score{font-weight:bold;font-size:1.1em}.unknown{color:#7c6017}",
             "</style></head><body><h1>Six scores per item</h1>",
             f"<p>{_escape(summary['benchmark'])} · {_escape(summary['deployment'])}</p>",
             f"<section id='item-statistics'><h2>{readiness}</h2>",
             f"<p>{experiment['selected_completed_items']} / {experiment['selected_items']} selected items scored; "
             f"{experiment['selected_error_items']} errors; {experiment['selected_pending_items']} pending. "
             f"Prepared dataset: {summary['total_items']} items.</p>",
             f"<p>{_escape(summary['interpretation'])}</p>",
             "<p><a href='items.csv'>All item scores (CSV)</a> · <a href='summary.json'>Summary JSON</a> · "
             "<a href='classifier_spec.json'>Shared context and fixed rubric</a></p>",
             "<p>1 = fundamental mismatch; 2 = substantial mismatch; 3 = partial alignment; "
             "4 = strong alignment with minor limitations; 5 = strong alignment supported by evidence.</p>",
             "</section><section id='dimension-averages'><h2>Average scores across evaluated items</h2>",
             f"<p>Based on {experiment['selected_completed_items']} completed items out of "
             f"{experiment['selected_items']} selected items in the prepared dataset. Each dimension uses its own "
             "numeric item count. Unknown scores, errors, and pending items are excluded from averages; "
             "Unknown counts are shown separately. Averages are descriptive item summaries and do not establish "
             "benchmark-wide coverage.</p>",
             "<table><tr><th>Dimension</th><th>Item average</th><th>Numeric items</th><th>Unknown</th>"
             "<th>Original benchmark score</th></tr>")
    original = summary.get("original_assessment") or {}
    for dimension in summary["dimensions"]:
        mean = dimension["mean_score"]
        mean_label = f"{mean:.2f} / 5" if mean is not None else "No numeric scores"
        assessment = original.get(dimension["id"])
        original_score = assessment.get("score") if isinstance(assessment, dict) else assessment
        if type(original_score) in (int, float):
            original_label = f"{original_score:.2f} / 5"
        elif original_score is not None:
            original_label = _escape(original_score)
        elif isinstance(assessment, dict) and "score" in assessment:
            original_label = "Unknown"
        else:
            original_label = "Not supplied"
        yield (f"<tr><th>{_escape(dimension['name'])}</th><td class='score'>{mean_label}</td>"
                     f"<td>{dimension['known']}</td><td>{dimension['unknown']}</td><td>{original_label}</td></tr>")
    yield ("</table></section><section id='dimension-distributions'><h2>Score distributions</h2>"
                 "<table><tr><th>Dimension</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>"
                 "<th>Unknown</th><th>Error</th><th>Pending</th></tr>")
    for dimension in summary["dimensions"]:
        yield (f"<tr><th>{_escape(dimension['name'])}</th>" +
                     "".join(f"<td>{dimension['counts'][str(score)]}</td>" for score in range(1, 6)) +
                     f"<td>{dimension['unknown']}</td><td>{dimension['errors']}</td><td>{dimension['pending']}</td></tr>")
    yield ("</table></section><section id='items'><h2>Items and supporting evidence</h2>"
                 "<p>Open a score to see its explanation, evidence, and information gaps. "
                 "Unselected prepared items remain visible as pending.</p><table><tr><th>Item</th><th>Status</th>" +
                 "".join(f"<th>{_escape(value.replace('_', ' ').title())}</th>" for value in DIMENSIONS) + "</tr>")
    for item in items:
        result = results.get(item["item_id"], {})
        state = result.get("status", "pending")
        yield (f"<tr><td><strong>{_escape(item['item_id'])}</strong><br>"
                     f"{_escape(_text(item.get('content'))[:160])}"
                     f"<details><summary>Complete item evidence</summary>{_render_fields(item)}</details></td>"
                     f"<td>{_escape(state.title())}{'' if item['item_id'] in selected_ids else ' (not selected)'}"
                     f"{('<p>' + _escape(result.get('error', '')) + '</p>') if state == 'error' else ''}</td>")
        for dimension in DIMENSIONS:
            if state != "complete":
                yield (f"<td>{_escape(state.title())}</td>")
                continue
            judgment = result["dimensions"][dimension]
            score = judgment["score"]
            label = "Unknown" if score is None else f"{score}/5"
            yield (f"<td><details><summary class='score{' unknown' if score is None else ''}'>{label}</summary>"
                         f"<p>{_escape(judgment['justification'])}</p><strong>Evidence</strong>"
                         f"{_render_fields(judgment['evidence'])}<strong>Information gaps</strong>"
                         f"{_render_fields(judgment['information_gaps'])}</details></td>")
        yield ("</tr>")
    yield ("</table></section><section id='original-assessment'><h2>Original benchmark assessment</h2>"
                 "<p>The benchmark assessment remains separate. Item scores do not overwrite it.</p>")
    if summary["original_assessment"]:
        yield (_render_fields(summary["original_assessment"]))
    else:
        yield ("<p>No benchmark assessment was supplied for this item analysis.</p>")
    if summary["original_report_available"]:
        yield ("<p><a href='original_benchmark_report.pdf'>Original benchmark report (PDF)</a></p>")
    yield ("</section><section id='human-review'><h2>Independent human review</h2>" +
                 f"<p>{_escape(summary['review_selection'].get('instructions', 'Existing worksheet preserved.'))}</p>")
    if summary["review_selection"].get("item_ids"):
        yield ("<p><a href='review.csv'>Review worksheet</a> (may contain existing human annotations). "
                     "A full results package includes a separate fresh blank worksheet.</p>")
    if summary.get("review_comparison_status"):
        yield (f"<p>{_escape(summary['review_comparison_status']['note'])}</p>")
    if summary.get("review_comparison"):
        yield (_render_fields(summary["review_comparison"]["classifiers"]))
    yield ("</section><section id='audit'><h2>Methods and provenance</h2>" +
                 f"<p>{_escape(experiment['request_policy'])}. "
                 f"Rubric: {_escape(summary['rubric_version'])}.</p>")
    for title, value in (("Run", summary.get("run")), ("Model", summary["classification"]),
                         ("Context preparation", summary["specification"]), ("Dataset", summary["dataset"])):
        if value:
            yield (f"<details><summary>{title}</summary>{_render_fields(value)}</details>")
    yield ("<p>This report works offline. Keep companion JSON and CSV files together.</p></section></body></html>")


def _write_html(path: Path, summary: dict, items, results: dict, selected_ids: set[str]) -> None:
    with _atomic_text(path) as stream:
        separator = ""
        for part in _html_parts(summary, items, results, selected_ids):
            # Wrap each complete table tag as it arrives, without copying the
            # full document. User-provided evidence is already escaped.
            part = part.replace("<table>", "<div class='table-scroll' role='region' aria-label='Scrollable data table' tabindex='0'><table>")
            part = part.replace("</table>", "</table></div>")
            stream.write(separator)
            stream.write(part)
            separator = "\n"


def compare_score_review(directory: Path, review_path: Path) -> dict:
    _, _, items, results = _load(directory)
    with review_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"item_id", *DIMENSIONS}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Review CSV is missing columns: {sorted(required - set(reader.fieldnames or []))}")
        rows = list(reader)
    seen = set()
    for row in rows:
        item_id = row["item_id"]
        if item_id not in items.item_ids or item_id in seen:
            raise ValueError(f"Unknown or duplicate review item ID: {item_id!r}")
        seen.add(item_id)
    comparison = {
        "analysis_type": "six_scores", "review_schema_version": "caliper_item_review_v3",
        "review_path": str(review_path), "reviewed_rows": len(rows),
        "input_hashes": _comparison_inputs(directory, review_path), "classifiers": {},
    }
    for dimension in DIMENSIONS:
        pairs, distances = [], []
        counts = Counter()
        for row in rows:
            raw = (row.get(dimension) or "").strip().lower()
            if not raw:
                counts["unreviewed"] += 1
                continue
            if raw not in {"1", "2", "3", "4", "5", "unknown"}:
                raise ValueError(f"Invalid human score {raw!r} for {dimension}; expected 1–5 or unknown")
            fields = ["justification", "information_gaps" if raw == "unknown" else "evidence"]
            for field in fields:
                value = (row.get(f"{dimension}.{field}") or "").strip()
                if value in {"", "[]", "null"}:
                    raise ValueError(f"Review {row['item_id']}: {dimension} requires {field}")
            result = results.get(row["item_id"], {})
            if result.get("status") != "complete":
                counts["model_unavailable"] += 1
                counts["model_errors" if result.get("status") == "error" else "model_pending"] += 1
                continue
            score = result["dimensions"][dimension]["score"]
            model = "unknown" if score is None else str(score)
            counts["human_unknown"] += raw == "unknown"
            counts["model_unknown"] += score is None
            pairs.append((raw, model))
            if raw != "unknown" and score is not None:
                distances.append(abs(int(raw) - score))
        comparison["classifiers"][dimension] = {
            **_agreement(pairs),
            **{key: counts[key] for key in ("unreviewed", "model_unavailable", "model_errors", "model_pending", "human_unknown", "model_unknown")},
            "numeric_pairs": len(distances), "mean_absolute_error": sum(distances) / len(distances) if distances else None,
            "denominator": "reviewed dimensions with completed model judgments; Unknown participates in exact agreement; numeric error excludes Unknown",
        }
    _write_json(directory / "review_comparison.json", comparison)
    generate_score_report(directory)
    return comparison
