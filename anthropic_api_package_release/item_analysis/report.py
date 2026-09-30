"""Summarize saved classifications and export a blind human-review worksheet.

Percentages describe model labels among known classifications. Unknown judgments,
failed calls, and pending items are separate; none count as negative labels.
"""

from __future__ import annotations

import csv
import html
import json
from collections import Counter
from pathlib import Path
from typing import Any

from . import storage
from .data import file_sha256
from .schema import allowed_labels


DIMENSIONS = (
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
)


def _read_json(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    # File iteration splits physical newlines only. str.splitlines() would also
    # split Unicode separators that legitimately occur inside JSON item text.
    with path.open(encoding="utf-8") as file:
        for number, line in enumerate(file, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in {path.name} line {number}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"Expected an object in {path.name} line {number}")
            records.append(record)
    return records


def _load_run(run_dir: Path) -> tuple[dict, list[dict], dict[str, dict]]:
    if (run_dir / "specification.json").exists():
        storage.check_specification(run_dir)
    spec = _read_json(run_dir / "classifier_spec.json")
    if not isinstance(spec, dict) or not isinstance(spec.get("classifiers"), list):
        raise ValueError("classifier_spec.json must contain classifiers")
    items = _read_jsonl(run_dir / "items.jsonl")
    item_ids = {item["item_id"] for item in items}
    if len(item_ids) != len(items):
        raise ValueError("Duplicate item IDs in items.jsonl")
    results: dict[str, dict] = {}
    for result in _read_jsonl(run_dir / "results.jsonl"):
        item_id = result.get("item_id")
        if item_id not in item_ids:
            raise ValueError(f"Result contains an item outside the prepared dataset: {item_id!r}")
        if result.get("status") not in {"complete", "error"}:
            raise ValueError(f"Unrecognized result status for {item_id}")
        # Retries do not duplicate observations. A later failed retry never erases
        # an already completed classification.
        if results.get(item_id, {}).get("status") != "complete":
            results[item_id] = result
    return spec, items, results


def _valid_model_label(label: Any, classifier: dict) -> bool:
    return any(type(label) is type(option) and label == option for option in allowed_labels(classifier))


def _judgment(result: dict, classifier: dict) -> tuple[Any, dict, bool]:
    judgment = result.get("labels", {}).get(classifier["id"])
    if not isinstance(judgment, dict) or "label" not in judgment:
        return None, {}, True
    label = judgment["label"]
    if label is not None and not _valid_model_label(label, classifier):
        return None, judgment, True
    evidence = judgment.get("evidence")
    justification = judgment.get("justification")
    valid_evidence = (
        isinstance(evidence, list)
        and all(isinstance(text, str) and text.strip() for text in evidence)
        and (label is None or bool(evidence))
    )
    if not valid_evidence or not isinstance(justification, str) or not justification.strip():
        return None, judgment, True
    return label, judgment, False


def _percent(numerator: int, denominator: int) -> float | None:
    return round(100 * numerator / denominator, 4) if denominator else None


def _comparison_inputs(run_dir: Path, review_path: Path) -> dict:
    paths = {
        "results_sha256": run_dir / "results.jsonl",
        "spec_sha256": run_dir / "classifier_spec.json",
        "review_sha256": review_path,
    }
    return {key: file_sha256(path) if path.is_file() else None for key, path in paths.items()}


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _csv_text(value: Any) -> str:
    # Keep spreadsheet applications from interpreting item text as a formula.
    text = _text(value)
    return "'" + text if text.lstrip().startswith(("=", "+", "-", "@")) else text


def _write_items_csv(run_dir: Path, items: list[dict], results: dict, classifiers: list[dict]) -> None:
    columns = ["item_id", "status", "content", "reference_answer", "grading_criterion", "error"]
    for classifier in classifiers:
        columns.extend(f"{classifier['id']}.{suffix}" for suffix in ("label", "evidence", "justification"))
    with (run_dir / "items.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for item in items:
            result = results.get(item["item_id"], {})
            row = {key: item.get(key, "") for key in columns[:5]}
            row.update(status=result.get("status", "pending"), error=result.get("error", ""))
            for classifier in classifiers:
                prefix = classifier["id"]
                if not classifier["applicable"]:
                    row[f"{prefix}.label"] = "N/A"
                elif result.get("status") == "complete":
                    label, judgment, invalid = _judgment(result, classifier)
                    row[f"{prefix}.label"] = "invalid" if invalid else "unknown" if label is None else label
                    row[f"{prefix}.evidence"] = judgment.get("evidence", [])
                    row[f"{prefix}.justification"] = judgment.get("justification", "")
            writer.writerow({key: _csv_text(value) for key, value in row.items()})


def _export_review(run_dir: Path, items: list[dict], classifiers: list[dict]) -> dict:
    path = run_dir / "review.csv"
    selection_path = run_dir / "review_selection.json"
    if path.exists():
        return _read_json(selection_path, {"method": "existing worksheet preserved"})
    # Items are already seed-shuffled by preparation. Reserve these IDs even if
    # the pilot has not classified them yet, to avoid reviewing pilot examples.
    holdout = len(items) > 100
    selected = items[100:150] if holdout else items[:50]
    selection = {
        "method": "prepared shuffled items 101–150" if holdout else "first up to 50 prepared shuffled items",
        "purpose": "holdout after the 100-item pilot" if holdout else "pilot debugging; not an independent holdout",
        "item_ids": [item["item_id"] for item in selected],
        "instructions": (
            "Fill applicable classifier columns with an allowed label, or 'unknown'. "
            "Blank means unreviewed. Consult classifier_spec.json; predictions are intentionally omitted."
        ),
    }
    applicable = [classifier["id"] for classifier in classifiers if classifier["applicable"]]
    columns = ["item_id", "content", "reference_answer", "grading_criterion", *applicable, "review_notes"]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for item in selected:
            writer.writerow({key: _csv_text(item.get(key, "")) for key in columns[:4]})
    _write_json(selection_path, selection)
    return selection


def _summarize_classifier(classifier: dict, results: dict, total: int) -> dict:
    definition_fields = (
        "id", "component", "operation", "applicable", "na_reason", "criterion", "aggregate", "grounded_in",
    )
    summary = {key: classifier.get(key) for key in definition_fields}
    if not classifier["applicable"]:
        return {**summary, "na_count": total}
    if classifier["operation"] == "assignment":
        summary["category_set"] = classifier["category_set"]
    counts = {str(option): 0 for option in allowed_labels(classifier)}
    unknown = invalid = completed = errors = 0
    for result in results.values():
        if result["status"] == "error":
            errors += 1
            continue
        completed += 1
        label, _, is_invalid = _judgment(result, classifier)
        if is_invalid:
            invalid += 1
        elif label is None:
            unknown += 1
        else:
            counts[str(label)] += 1
    known = sum(counts.values())
    summary.update(
        counts=counts,
        known=known,
        unknown=unknown,
        invalid=invalid,
        errors=errors,
        pending=total - completed - errors,
        completed=completed,
        percentages_among_known={label: _percent(count, known) for label, count in counts.items()},
        unknown_percent_among_completed=_percent(unknown, completed),
        percentage_denominator="known valid labels only",
        not_observed_labels=[label for label, count in counts.items() if count == 0],
    )
    if classifier["operation"] == "flag":
        summary["positive_percent_among_known"] = _percent(counts["1"], known)
        summary["positive_class"] = classifier.get("positive_class")
    if classifier["operation"] == "ordinal":
        summary["ordinal_anchors"] = classifier["ordinal_anchors"]
    if classifier["id"] == "IO.task_category":
        summary["required_categories_not_observed"] = [
            label for label in summary["not_observed_labels"] if label != "irrelevant_other"
        ]
    return summary


def generate_report(run_dir: Path) -> dict:
    """Write summary.json, items.csv, blind review.csv, and standalone report.html."""
    run_dir = Path(run_dir)
    spec, items, results = _load_run(run_dir)
    dataset = _read_json(run_dir / "dataset.json", {})
    evidence = _read_json(run_dir / "evidence.json", {})
    original = evidence.get("scoring", {})
    original_dimensions = original.get("dimensions", original) if isinstance(original, dict) else {}
    completed = sum(result["status"] == "complete" for result in results.values())
    errors = sum(result["status"] == "error" for result in results.values())
    classifiers = [_summarize_classifier(classifier, results, len(items)) for classifier in spec["classifiers"]]
    complete_snapshot = (
        bool(items) and completed == len(items)
        and not any(classifier.get("invalid", 0) for classifier in classifiers)
    )
    run_config = _read_json(run_dir / "run.json", {})
    summary = {
        "benchmark": spec.get("benchmark", dataset.get("benchmark")),
        "deployment": spec.get("deployment"),
        "original_deployment": evidence.get("deployment"),
        "specification": _read_json(run_dir / "specification.json", {}),
        "classification": {
            key: run_config.get(key)
            for key in ("provider", "model_id", "reasoning_effort", "max_tokens")
        } if run_config else None,
        "dataset": dataset,
        "total_items": len(items),
        "completed_items": completed,
        "error_items": errors,
        "pending_items": len(items) - completed - errors,
        "complete_snapshot": complete_snapshot,
        "scope": "all items in the prepared snapshot" if complete_snapshot else "incomplete run over the prepared snapshot",
        "interpretation": (
            "Counts describe classifier judgments, not verified prevalence. "
            "Percentages exclude unknown, invalid, failed, and pending judgments. "
            "No item statistics are converted into 1–5 scores."
        ),
        "original_assessment": {dimension: original_dimensions.get(dimension) for dimension in DIMENSIONS},
        "classifiers": classifiers,
    }
    _write_items_csv(run_dir, items, results, spec["classifiers"])
    summary["review_selection"] = _export_review(run_dir, items, spec["classifiers"])
    comparison = _read_json(run_dir / "review_comparison.json")
    if comparison:
        review_path = Path(comparison.get("review_path", ""))
        current_inputs = _comparison_inputs(run_dir, review_path)
        current = bool(current_inputs["review_sha256"]) and comparison.get("input_hashes") == current_inputs
        summary["review_comparison_status"] = {
            "current": current,
            "note": (
                "Comparison matches the saved predictions, specification, and human labels."
                if current else
                "Saved human-review comparison is stale: its predictions, specification, "
                "or review file changed or are unavailable. Rerun validate to refresh agreement."
            ),
        }
        if current:
            summary["review_comparison"] = comparison
    _write_json(run_dir / "summary.json", summary)
    (run_dir / "report.html").write_text(_render_html(summary, items, results), encoding="utf-8")
    return summary


def _escape(value: Any) -> str:
    return html.escape(_text(value), quote=True)


def _display_percent(value: float | None) -> str:
    return "—" if value is None else f"{value:.1f}%"


def _render_html(summary: dict, items: list[dict], results: dict) -> str:
    parts = ["""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Caliper item analysis</title><style>
body{font:16px/1.6 system-ui,sans-serif;max-width:1100px;margin:auto;padding:2rem;color:#17212f;background:#fafbfc}
h1,h2,h3{line-height:1.25}section{background:white;padding:1.5rem;margin:1.5rem 0;border:1px solid #dce2e8;border-radius:8px}
table{border-collapse:collapse;width:100%;margin:1rem 0}th,td{text-align:left;padding:.5rem;border-bottom:1px solid #dce2e8;vertical-align:top}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}small{color:#465368}a{color:#175c9e}.notice{background:#edf3fa;padding:1rem}
</style><body><h1>Caliper item analysis</h1>"""]
    parts.append(
        f"<p><strong>{_escape(summary['benchmark'])}</strong> · {_escape(summary['scope'])}</p>"
        f"<p><strong>Classifier deployment:</strong> {_escape(summary['deployment'])}</p>"
        "<details><summary>Original deployment requirements</summary>"
        f"<pre>{_escape(summary['original_deployment'] or 'Not supplied')}</pre></details>"
    )
    metadata = summary["specification"]
    if summary.get("classification"):
        parts.append(
            "<details><summary>Classification model</summary>"
            f"<pre>{_escape(summary['classification'])}</pre></details>"
        )
    if metadata:
        parts.append(
            "<section><h2>Specification provenance</h2>"
            f"<p>{_escape(metadata.get('note'))}</p>"
            f"<p><strong>Source:</strong> {_escape(metadata.get('source'))}</p>"
            f"<p><strong>Evidence references checked:</strong> {_escape(metadata.get('evidence_references_checked'))}</p>"
        )
        if metadata.get("adjustments"):
            parts.append("<h3>Explicit adjustments</h3><ul>")
            for adjustment in metadata["adjustments"]:
                parts.append(f"<li><pre>{_escape(json.dumps(adjustment, ensure_ascii=False, indent=2))}</pre></li>")
            parts.append("</ul>")
        parts.append("</section>")
    parts.append(
        f"<p>{summary['completed_items']} completed / {summary['total_items']} prepared items; "
        f"{summary['error_items']} failed; {summary['pending_items']} pending.</p>"
    )
    parts.append(
        f"<p class='notice'>{_escape(summary['interpretation'])} "
        "A category not observed in a partial run is not demonstrated absent from the benchmark.</p>"
    )
    parts.append(
        "<p><a href='items.csv'>All items and predictions (CSV)</a> · "
        "<a href='review.csv'>Blind review worksheet</a> · "
        "<a href='classifier_spec.json'>Classifier specification</a> · "
        "<a href='summary.json'>Summary JSON</a></p>"
    )
    parts.append(f"<details><summary>Dataset provenance</summary><pre>{_escape(summary['dataset'])}</pre></details>")
    parts.append(
        "<section><h2>Original assessment</h2><p>These benchmark-level scores are retained unchanged. "
        "Input Form and Output Form remain at benchmark level.</p>"
        "<table><tr><th>Dimension</th><th>Original score</th><th>Original finding</th></tr>"
    )
    for dimension, assessment in summary["original_assessment"].items():
        score = assessment.get("score", "Not supplied") if isinstance(assessment, dict) else "Not supplied"
        finding = assessment.get("justification", "") if isinstance(assessment, dict) else ""
        parts.append(f"<tr><td>{_escape(dimension.replace('_', ' ').title())}</td><td>{_escape(score)}</td><td>{_escape(finding)}</td></tr>")
    parts.append("</table></section>")
    item_by_id = {item["item_id"]: item for item in items}
    for classifier in summary["classifiers"]:
        parts.append(f"<section><h2>{_escape(classifier['id'])}</h2>")
        if not classifier["applicable"]:
            parts.append(f"<p>Not applicable to {classifier['na_count']} prepared items: {_escape(classifier['na_reason'])}</p></section>")
            continue
        parts.append(f"<p>{_escape(classifier['criterion'])}</p>")
        parts.append(
            f"<p>{classifier['known']} known labels; {classifier['unknown']} unknown "
            f"({_display_percent(classifier['unknown_percent_among_completed'])} of completed); "
            f"{classifier['invalid']} invalid; {classifier['errors']} failed; {classifier['pending']} pending.</p>"
        )
        parts.append("<table><tr><th>Label</th><th>Meaning</th><th>Count</th><th>Percent of known labels</th></tr>")
        for label, count in classifier["counts"].items():
            meaning = classifier.get("ordinal_anchors", {}).get(label, "")
            if classifier["operation"] == "flag":
                meaning = classifier.get("positive_class", "Positive") if label == "1" else "Criterion not met"
            percentage = classifier["percentages_among_known"][label]
            parts.append(f"<tr><td>{_escape(label)}</td><td>{_escape(meaning)}</td><td>{count}</td><td>{_display_percent(percentage)}</td></tr>")
        parts.append("</table>")
        if classifier["not_observed_labels"]:
            parts.append(f"<p><small>Not observed among classified items: {_escape(', '.join(classifier['not_observed_labels']))}.</small></p>")
        if classifier.get("required_categories_not_observed"):
            categories = ", ".join(classifier["required_categories_not_observed"])
            parts.append(f"<p>Required categories not observed among classified items: {_escape(categories)}.</p>")
        parts.append(f"<details><summary>Grounding in the original assessment</summary><pre>{_escape(classifier.get('grounded_in'))}</pre></details>")
        parts.append("<h3>Examples</h3><p><small>First example of each observed label, including unknown. Inspect the CSV for all items.</small></p>")
        seen: set[str] = set()
        for item_id, result in results.items():
            if result["status"] != "complete":
                continue
            label, judgment, invalid = _judgment(result, classifier)
            key = "invalid" if invalid else "unknown" if label is None else str(label)
            if key in seen:
                continue
            seen.add(key)
            item = item_by_id[item_id]
            parts.append(
                f"<details><summary>{_escape(key)} · {_escape(item_id)}</summary>"
                f"<pre>{_escape(_text(item.get('content'))[:2000])}</pre>"
                f"<p><strong>Reference answer:</strong> {_escape(item.get('reference_answer'))}</p>"
                f"<p><strong>Evidence:</strong> {_escape(judgment.get('evidence'))}</p>"
                f"<p>{_escape(judgment.get('justification'))}</p></details>"
            )
        parts.append("</section>")
    selection = summary["review_selection"]
    parts.append(
        "<section><h2>Human review</h2>"
        f"<p>{_escape(selection.get('purpose', 'Existing review worksheet'))}. "
        f"{_escape(selection.get('instructions', ''))}</p>"
    )
    if "review_comparison" in summary:
        parts.append(
            "<p>Agreement with the supplied human labels. "
            "Model unknowns count as disagreements with a known human label.</p>"
            "<table><tr><th>Classifier</th><th>Compared</th><th>Agreement</th><th>Cohen’s κ</th></tr>"
        )
        for classifier_id, comparison in summary["review_comparison"]["classifiers"].items():
            accuracy = comparison["accuracy"]
            kappa = comparison["cohen_kappa"]
            agreement = _display_percent(accuracy * 100 if accuracy is not None else None)
            kappa_display = f"{kappa:.3f}" if kappa is not None else "—"
            parts.append(
                f"<tr><td>{_escape(classifier_id)}</td><td>{comparison['compared']}</td>"
                f"<td>{agreement}</td><td>{kappa_display}</td></tr>"
            )
        parts.append("</table><p><a href='review_comparison.json'>Comparison details and confusion counts</a></p>")
    else:
        note = summary.get("review_comparison_status", {}).get(
            "note", "No human-label comparison has been supplied yet."
        )
        parts.append(f"<p>{_escape(note)} Full item coverage does not establish classification accuracy.</p>")
    return "\n".join([*parts, "</section></body></html>"])


def _parse_human_label(raw: str, classifier: dict) -> Any:
    if raw == "unknown":
        return None
    for option in allowed_labels(classifier):
        if raw == str(option):
            return option
    raise ValueError(f"Invalid human label {raw!r} for {classifier['id']}; expected {allowed_labels(classifier)} or 'unknown'")


def compare_review(run_dir: Path, review_path: Path) -> dict:
    """Validate a filled blind-review CSV, save agreement, and refresh the report."""
    run_dir, review_path = Path(run_dir), Path(review_path).resolve()
    spec, items, results = _load_run(run_dir)
    classifiers = [classifier for classifier in spec["classifiers"] if classifier["applicable"]]
    item_ids = {item["item_id"] for item in items}
    with review_path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {"item_id", *(classifier["id"] for classifier in classifiers)}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Review CSV is missing columns: {sorted(required - set(reader.fieldnames or []))}")
        rows = list(reader)
    seen: set[str] = set()
    for row in rows:
        item_id = row["item_id"]
        if item_id not in item_ids:
            raise ValueError(f"Unknown review item ID: {item_id!r}")
        if item_id in seen:
            raise ValueError(f"Duplicate review item ID: {item_id!r}")
        seen.add(item_id)
    comparison = {
        "review_path": str(review_path), "reviewed_rows": len(rows),
        "input_hashes": _comparison_inputs(run_dir, review_path), "classifiers": {},
    }
    for classifier in classifiers:
        pairs: list[tuple[str, str]] = []
        unreviewed = unavailable = human_unknown = model_unknown = invalid = 0
        for row in rows:
            raw = (row.get(classifier["id"]) or "").strip()
            if not raw:
                unreviewed += 1
                continue
            human = _parse_human_label(raw, classifier)
            result = results.get(row["item_id"], {})
            if result.get("status") != "complete":
                unavailable += 1
                continue
            predicted, _, is_invalid = _judgment(result, classifier)
            if is_invalid:
                invalid += 1
                continue
            if human is None:
                human_unknown += 1
                continue
            if predicted is None:
                model_unknown += 1
            pairs.append((str(human), "unknown" if predicted is None else str(predicted)))
        total = len(pairs)
        matches = sum(human == predicted for human, predicted in pairs)
        accuracy = matches / total if total else None
        gold_counts = Counter(human for human, _ in pairs)
        model_counts = Counter(predicted for _, predicted in pairs)
        expected = sum(gold_counts[label] * model_counts[label] for label in gold_counts) / total**2 if total else 0
        kappa = (accuracy - expected) / (1 - expected) if total and expected < 1 else None
        confusion = Counter(pairs)
        comparison["classifiers"][classifier["id"]] = {
            "compared": total, "matches": matches, "accuracy": accuracy, "cohen_kappa": kappa,
            "human_unknown_excluded": human_unknown, "model_unknown_included_as_disagreement": model_unknown,
            "unreviewed": unreviewed, "model_unavailable": unavailable, "invalid_model_labels": invalid,
            "confusion": [{"human": human, "model": model, "count": count} for (human, model), count in sorted(confusion.items())],
        }
    _write_json(run_dir / "review_comparison.json", comparison)
    generate_report(run_dir)
    return comparison
