"""Summarize saved classifications and export a blind human-review worksheet.

Generic percentages describe valid model judgments, including insufficient evidence.
Operational failures and pending items are separate. Legacy numeric labels retain
their historical meanings and denominators.
"""

from __future__ import annotations

import csv
import html
import json
from collections import Counter
from collections.abc import Iterable, Iterator
from itertools import islice
from pathlib import Path
from typing import Any

from . import storage
from .data import file_sha256
from .catalog import CATALOG_VERSION, SPEC_SCHEMA_VERSION, LEGACY_SCHEMA_VERSION, LEGACY_CATALOG_VERSION, is_generic_spec
from .classify import check_result_progress
from .schema import allowed_labels, validate_spec


GENERIC_IDS = {"input_ontology", "input_content", "output_ontology", "output_content"}
SPLIT_RESULT_SCHEMA = "caliper_item_result_v3"


def _generic(classifier: dict) -> bool:
    return classifier.get("id") in GENERIC_IDS


def _versions(spec: dict) -> dict:
    generic = is_generic_spec(spec)
    return {
        "schema_version": spec.get("schema_version", SPEC_SCHEMA_VERSION if generic else LEGACY_SCHEMA_VERSION),
        "fixed_catalog_version": spec.get("fixed_catalog_version", LEGACY_CATALOG_VERSION),
    }


DIMENSIONS = (
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
)


def _read_json(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _iter_jsonl(path: Path) -> Iterator[dict]:
    if not path.exists():
        return
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
            yield record


def _read_jsonl(path: Path) -> list[dict]:
    return list(_iter_jsonl(path))


class _ItemPopulation:
    """Validated, repeatable on-disk population; retain IDs, not all item content."""

    def __init__(self, path: Path):
        self.path = path
        self.item_ids: set[str] = set()
        for item in self:
            item_id = item["item_id"]
            if item_id in self.item_ids:
                raise ValueError("Duplicate item IDs in items.jsonl")
            self.item_ids.add(item_id)

    def __iter__(self) -> Iterator[dict]:
        return _iter_jsonl(self.path)

    def __len__(self) -> int:
        return len(self.item_ids)


def _items_with_ids(items: Iterable[dict], item_ids: set[str]) -> list[dict]:
    """Keep the saved order and stop reading once every requested item is found."""
    remaining = set(item_ids)
    selected = []
    if not remaining:
        return selected
    for item in items:
        if item["item_id"] in remaining:
            selected.append(item)
            remaining.remove(item["item_id"])
            if not remaining:
                break
    return selected


def _load_run(run_dir: Path) -> tuple[dict, _ItemPopulation, dict[str, dict]]:
    dataset = _read_json(run_dir / "dataset.json", {})
    if dataset.get("analysis_basis") == "deployment_requirements":
        storage.check_prepared(run_dir)
    if (run_dir / "specification.json").exists():
        storage.check_specification(run_dir)
    spec = _read_json(run_dir / "classifier_spec.json")
    if not isinstance(spec, dict) or not isinstance(spec.get("classifiers"), list):
        raise ValueError("classifier_spec.json must contain classifiers")
    if "fixed_catalog_version" in spec:
        # Reject unsupported versions and mutated rules; historical specs remain untouched.
        validate_spec(spec)
        if all(key in dataset for key in ("items_sha256", "profile_sha256", "evidence_sha256")):
            storage.check_prepared(run_dir)
    items = _ItemPopulation(run_dir / "items.jsonl")
    results: dict[str, dict] = {}
    for result in _iter_jsonl(run_dir / "results.jsonl"):
        item_id = result.get("item_id")
        if item_id not in items.item_ids:
            raise ValueError(f"Result contains an item outside the prepared dataset: {item_id!r}")
        statuses = {"complete", "error", "partial"} if result.get("schema_version") == SPLIT_RESULT_SCHEMA else {"complete", "error"}
        if result.get("status") not in statuses:
            raise ValueError(f"Unrecognized result status for {item_id}")
        previous = results.get(item_id)
        if result.get("schema_version") == SPLIT_RESULT_SCHEMA:
            check_result_progress(result, previous)
        elif previous and previous.get("schema_version") == SPLIT_RESULT_SCHEMA:
            raise ValueError("Result versions cannot change within an item")
        # Retries do not duplicate observations. A later failed retry never erases
        # an already completed historical classification. Split snapshots must
        # preserve their cumulative labels and attempts, checked above.
        if results.get(item_id, {}).get("status") != "complete":
            results[item_id] = result
    return spec, items, results


def _valid_model_label(label: Any, classifier: dict) -> bool:
    return any(type(label) is type(option) and label == option for option in allowed_labels(classifier))


def _classifier_state(result: dict, classifier: dict) -> str:
    """Describe this classifier's progress independently of sibling requests."""
    if _generic(classifier) and result.get("schema_version") == SPLIT_RESULT_SCHEMA:
        labels = result.get("labels", {})
        if isinstance(labels, dict) and classifier["id"] in labels:
            return "complete"
        errors = result.get("classifier_errors", {})
        if isinstance(errors, dict) and classifier["id"] in errors:
            return "error"
        # A claimed complete record with a missing label is invalid, not pending.
        return "complete" if result.get("status") == "complete" else "pending"
    return result.get("status", "pending")


def _classifier_error(result: dict, classifier: dict) -> str:
    if result.get("schema_version") == SPLIT_RESULT_SCHEMA:
        return result.get("classifier_errors", {}).get(classifier["id"], "")
    return result.get("error", "") if result.get("status") == "error" else ""


def _judgment(result: dict, classifier: dict) -> tuple[Any, dict, bool]:
    if _generic(classifier) and (
        result.get("schema_version") not in {"caliper_item_result_v2", SPLIT_RESULT_SCHEMA}
        or result.get("fixed_catalog_version") != CATALOG_VERSION
    ):
        return None, {}, True
    labels = result.get("labels")
    if not isinstance(labels, dict):
        return None, {}, True
    if _generic(classifier) and (
        set(labels) - GENERIC_IDS
        or (result.get("schema_version") == "caliper_item_result_v2" and set(labels) != GENERIC_IDS)
    ):
        return None, {}, True
    judgment = labels.get(classifier["id"])
    if not isinstance(judgment, dict) or "label" not in judgment:
        return None, {}, True
    if _generic(classifier):
        fields = {"label", "evidence", "justification"}
        if classifier["id"] == "input_ontology":
            fields |= {"matched_category_ids", "scope_exclusion_source_ids"}
        if set(judgment) != fields:
            return None, judgment, True
    label = judgment["label"]
    if (label is None and _generic(classifier)) or (label is not None and not _valid_model_label(label, classifier)):
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
    if classifier["id"] == "input_ontology":
        matched = judgment.get("matched_category_ids")
        if (not isinstance(matched, list) or any(not isinstance(value, str) for value in matched)
                or len(matched) != len(set(matched)) or bool(matched) != (label == "match")):
            return None, judgment, True
        exclusions = judgment.get("scope_exclusion_source_ids")
        if (not isinstance(exclusions, list) or any(not isinstance(value, str) for value in exclusions)
                or len(exclusions) != len(set(exclusions))):
            return None, judgment, True
        if any(classifier.get("source_roles", {}).get(ref) != "deployment_requirement" for ref in exclusions):
            return None, judgment, True
        inventory = classifier.get("input_category_inventory", {})
        if inventory:
            allowed = {category["id"] for category in inventory.get("categories", [])}
            if set(matched) - allowed:
                return None, judgment, True
            if label == "no_match" and inventory.get("completeness") != "complete":
                exclusions = judgment.get("scope_exclusion_source_ids", [])
                if (not exclusions or not set(exclusions).issubset(classifier.get("source_registry", {}))
                        or any(classifier.get("source_roles", {}).get(ref) != "deployment_requirement" for ref in exclusions)):
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


def _write_items_csv(run_dir: Path, items: Iterable[dict], results: dict, classifiers: list[dict],
                     provenance: dict | None = None) -> None:
    provenance = provenance or {}
    columns = ["item_id", "status", "content", "reference_answer", "grading_criterion", "error"]
    for classifier in classifiers:
        suffixes = ["status", "error", "label", "evidence", "justification"]
        if classifier["id"] == "input_ontology":
            suffixes += ["matched_category_ids", "scope_exclusion_source_ids"]
        columns.extend(f"{classifier['id']}.{suffix}" for suffix in suffixes)
    columns.extend(provenance)
    with (run_dir / "items.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for item in items:
            result = results.get(item["item_id"], {})
            row = {key: item.get(key, "") for key in columns[:5]}
            row.update(status=result.get("status", "pending"), error=result.get("error", ""))
            row.update(provenance)
            for classifier in classifiers:
                prefix = classifier["id"]
                if not classifier["applicable"]:
                    row[f"{prefix}.label"] = "N/A"
                    row[f"{prefix}.status"] = "not_applicable"
                    continue
                state = _classifier_state(result, classifier)
                row[f"{prefix}.status"] = state
                row[f"{prefix}.error"] = _classifier_error(result, classifier)
                if state == "complete":
                    label, judgment, invalid = _judgment(result, classifier)
                    if invalid:
                        row[f"{prefix}.status"] = "invalid"
                    row[f"{prefix}.label"] = "invalid" if invalid else "unknown" if label is None else label
                    row[f"{prefix}.evidence"] = judgment.get("evidence", [])
                    row[f"{prefix}.justification"] = judgment.get("justification", "")
                    if prefix == "input_ontology":
                        row[f"{prefix}.matched_category_ids"] = judgment.get("matched_category_ids", [])
                        row[f"{prefix}.scope_exclusion_source_ids"] = judgment.get("scope_exclusion_source_ids", [])
            writer.writerow({key: _csv_text(value) for key, value in row.items()})


def _export_review(run_dir: Path, items: list[dict] | _ItemPopulation, classifiers: list[dict],
                   provenance: dict | None = None) -> dict:
    provenance = provenance or {}
    path = run_dir / "review.csv"
    selection_path = run_dir / "review_selection.json"
    if path.exists():
        return _read_json(selection_path, {"method": "existing worksheet preserved"})
    generic = any(_generic(classifier) for classifier in classifiers)
    if generic and not items:
        return {
            "schema_version": "caliper_item_review_v2", "fixed_catalog_version": provenance.get("fixed_catalog_version"),
            "method": "awaiting experiment selection", "purpose": "review worksheet deferred until items are selected",
            "item_ids": [], "instructions": "Run classification to record the selected items before exporting the review worksheet.",
        }
    if generic:
        selection = {
            "schema_version": "caliper_item_review_v2",
            "fixed_catalog_version": provenance.get("fixed_catalog_version"),
            "method": "all selected items in the saved shuffled order",
            "purpose": "independent human review of the selected experiment items; not a tuning holdout",
            "item_ids": [item["item_id"] for item in items],
            "instructions": (
                "Enter a fixed judgment label for each classifier, including insufficient_evidence when warranted. "
                "Blank means unreviewed. For Input Ontology also enter a JSON array of matched category IDs "
                "([] for no_match or insufficient_evidence). Consult the fixed rules and sourced context in "
                "classifier_spec.json. Predictions are intentionally omitted."
            ),
        }
        columns = ["item_id", "content", "reference_answer", "grading_criterion"]
        for classifier in classifiers:
            columns.append(classifier["id"])
            if classifier["id"] == "input_ontology":
                columns.extend(["input_ontology.matched_category_ids", "input_ontology.scope_exclusion_source_ids"])
            columns.extend([f"{classifier['id']}.evidence", f"{classifier['id']}.justification"])
        columns.extend(["review_notes", *provenance])
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            for item in items:
                row = {key: item.get(key, "") for key in columns[:4]}
                writer.writerow({key: _csv_text(value) for key, value in {**row, **provenance}.items()})
        _write_json(selection_path, selection)
        return selection
    # Items are already seed-shuffled by preparation. Reserve these IDs even if
    # the pilot has not classified them yet, to avoid reviewing pilot examples.
    holdout = len(items) > 100
    selected = list(islice(items, 100, 150)) if holdout else list(islice(items, 50))
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
    columns.extend(provenance)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for item in selected:
            row = {key: item.get(key, "") for key in columns[:4]}
            writer.writerow({key: _csv_text(value) for key, value in {**row, **provenance}.items()})
    _write_json(selection_path, selection)
    return selection


def _summarize_classifier(classifier: dict, results: dict, total: int) -> dict:
    if _generic(classifier):
        return _summarize_generic(classifier, results, total)
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
        state = _classifier_state(result, classifier)
        if state == "error":
            errors += 1
            continue
        if state != "complete":
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



def _summarize_generic(classifier: dict, results: dict, total: int) -> dict:
    summary = dict(classifier)
    summary["criterion"] = classifier["question"]
    counts = {label: 0 for label in allowed_labels(classifier)}
    invalid = errors = completed = 0
    inventory = classifier.get("input_category_inventory", {})
    category_counts = {category["id"]: 0 for category in inventory.get("categories", [])}
    for result in results.values():
        state = _classifier_state(result, classifier)
        if state == "error":
            errors += 1
            continue
        if state != "complete":
            continue
        completed += 1
        label, judgment, bad = _judgment(result, classifier)
        if bad:
            invalid += 1
            continue
        counts[label] += 1
        for category_id in judgment.get("matched_category_ids", []):
            category_counts[category_id] += 1
    valid = sum(counts.values())
    insufficient = counts["insufficient_evidence"]
    determinate = valid - insufficient
    summary.update(
        counts=counts, valid_judgments=valid, determinate_judgments=determinate,
        insufficient_evidence=insufficient, invalid=invalid, errors=errors,
        pending=total - completed - errors, completed=completed,
        percentages_among_valid={label: _percent(count, valid) for label, count in counts.items()},
        percentage_denominator="all valid judgments, including insufficient_evidence",
        not_observed_labels=[label for label, count in counts.items() if count == 0],
    )
    if classifier["id"] == "input_ontology":
        summary.update(
            category_counts=category_counts,
            category_percentages_among_determinate={key: _percent(count, determinate) for key, count in category_counts.items()},
            category_percentage_denominator="match and no_match judgments; category assignments may overlap",
            required_categories_not_observed=[key for key, count in category_counts.items() if not count],
            inventory_completeness=inventory.get("completeness", "unknown"),
            completeness_source_ids=inventory.get("completeness_source_ids", []),
            coverage_interpretation=(
                "Counts record supported matches to the supplied category inventory. Categories may overlap. "
                "A category not observed in these items is not established absent from the benchmark. "
                "Partial or unknown inventories do not establish complete deployment coverage."
            ),
        )
    else:
        summary["issue_percent_among_determinate"] = _percent(counts["issue_identified"], determinate)
        summary["determinate_percentage_denominator"] = "issue_identified and no_issue_identified judgments"
    return summary

def generate_report(run_dir: Path, *, run_metadata: dict | None = None) -> dict:
    """Write summary.json, items.csv, blind review.csv, and standalone report.html."""
    run_dir = Path(run_dir)
    spec, items, results = _load_run(run_dir)
    dataset = _read_json(run_dir / "dataset.json", {})
    evidence = _read_json(run_dir / "evidence.json", {})
    direct = evidence.get("analysis_basis") == "deployment_requirements"
    original = evidence.get("scoring", {})
    original_dimensions = original.get("dimensions", original) if isinstance(original, dict) else {}
    completed = sum(result["status"] == "complete" for result in results.values())
    errors = sum(result["status"] == "error" for result in results.values())
    partial = sum(result["status"] == "partial" for result in results.values())
    generic = is_generic_spec(spec)
    execution = _read_json(run_dir / "execution.json", {})
    if generic and "selected_item_ids" in execution:
        selected_ids = set(execution["selected_item_ids"])
        if selected_ids - items.item_ids:
            raise ValueError("Execution selection contains items outside the prepared dataset")
        selected_items = _items_with_ids(items, selected_ids)
    elif generic and "target_items" in execution:
        selected_items = list(islice(items, execution["target_items"]))
    elif generic and results:
        selected_items = _items_with_ids(items, set(results))
    else:
        selected_items = [] if generic else items
    selected_ids = {item["item_id"] for item in selected_items}
    selected_results = {item_id: result for item_id, result in results.items() if item_id in selected_ids}
    definitions = []
    for classifier in spec["classifiers"]:
        definition = dict(classifier)
        if generic:
            definition["context"] = spec["context_by_classifier"][classifier["id"]]
            if classifier["id"] == "input_ontology":
                definition["input_category_inventory"] = spec["input_category_inventory"]
                definition["source_registry"] = spec["source_registry"]
                definition["source_roles"] = spec["source_roles"]
        definitions.append(definition)
    reporting_results = selected_results if generic else results
    reporting_total = len(selected_items) if generic else len(items)
    classifiers = [_summarize_classifier(classifier, reporting_results, reporting_total) for classifier in definitions]
    complete_snapshot = (
        bool(items) and completed == len(items)
        and not any(classifier.get("invalid", 0) for classifier in classifiers)
        and (not generic or all(not _judgment(result, classifier)[2]
                                for result in results.values() for classifier in definitions))
    )
    run_config = _read_json(run_dir / "run.json", {})
    split_requests = (
        run_config.get("request_mode") == "per_classifier"
        or execution.get("request_mode") == "per_classifier"
        or any(result.get("schema_version") == SPLIT_RESULT_SCHEMA for result in results.values())
    )
    request_policy = (
        "one primary request per item-classifier pair; repairs and retries add calls"
        if split_requests else
        "one primary request per item covers every configured classifier; repairs and retries add calls"
    )
    summary = {
        **_versions(spec),
        "report_schema_version": "caliper_item_report_v2" if generic else "legacy_item_report_v1",
        "benchmark": spec.get("benchmark", dataset.get("benchmark")),
        "deployment": spec.get("deployment_description", spec.get("deployment")),
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
        "partial_items": partial,
        "pending_items": len(items) - completed - errors - partial,
        "complete_snapshot": complete_snapshot,
        "scope": "all items in the prepared snapshot" if complete_snapshot else "incomplete run over the prepared snapshot",
        "interpretation": (
            "Counts describe classifier judgments, not verified prevalence. "
            "Percentages exclude unknown, invalid, failed, and pending judgments. "
            "No item statistics are converted into 1–5 scores."
        ),
        "original_assessment": None if direct else {dimension: original_dimensions.get(dimension) for dimension in DIMENSIONS},
        "original_report_available": (run_dir / "original_benchmark_report.pdf").is_file(),
        "classifiers": classifiers,
    }
    if run_metadata:
        summary["run"] = {key: run_metadata[key] for key in
                          ("run_id", "status", "scope", "created_at", "updated_at", "exported_at")
                          if key in run_metadata and run_metadata[key] is not None}
    if split_requests and summary["classification"] is not None:
        summary["classification"].update(
            request_mode="per_classifier",
            request_schema_version=run_config.get("request_schema_version"),
            prompt_sha256=run_config.get("prompt_sha256"),
        )
    active_count = sum(classifier["applicable"] for classifier in definitions)
    selected_completed = sum(result["status"] == "complete" for result in selected_results.values())
    summary["experiment"] = {
        "classifier_count": active_count,
        "benchmark_classifier_combinations": active_count,
        "selected_items": len(selected_items),
        "selected_completed_items": selected_completed,
        "selected_error_items": sum(result["status"] == "error" for result in selected_results.values()),
        "selected_partial_items": sum(result["status"] == "partial" for result in selected_results.values()),
        "selected_pending_items": len(selected_items) - len(selected_results),
        "expected_item_classifier_judgments": len(selected_items) * active_count,
        "completed_item_classifier_judgments": sum(classifier.get("valid_judgments", classifier.get("known", 0) + classifier.get("unknown", 0)) for classifier in classifiers),
        "error_item_classifier_judgments": sum(classifier.get("errors", 0) for classifier in classifiers),
        "invalid_item_classifier_judgments": sum(classifier.get("invalid", 0) for classifier in classifiers),
        "pending_item_classifier_judgments": sum(classifier.get("pending", 0) for classifier in classifiers),
        "request_policy": request_policy,
        # Split-request snapshots retain cumulative attempts. Historical records
        # contain only the attempts made for that append.
        "recorded_api_calls": (
            sum(len(record.get("attempts", [])) for record in results.values()
                if record.get("schema_version") == SPLIT_RESULT_SCHEMA)
            + sum(len(record.get("attempts", [])) for record in _iter_jsonl(run_dir / "results.jsonl")
                  if record.get("schema_version") != SPLIT_RESULT_SCHEMA)
        ),
    }
    if generic:
        summary["interpretation"] = (
            "Counts describe model judgments, not verified prevalence. Judgment percentages include insufficient_evidence; "
            "any determinate-only percentage states its denominator. Invalid responses, operational errors, and pending "
            "items remain separate. No issue identified is a bounded finding for the examined aspect and available "
            "evidence, not proof of alignment, stakeholder agreement, or benchmark validity. No item statistics are "
            "converted into 1–5 scores."
        )
    provenance = _versions(spec)
    if direct:
        provenance.update({
            "analysis_basis": "deployment_requirements", "assessment_status": "not_run",
            "unassessed_dimensions": ["input_form", "output_form"],
            "direct_context_sha256": dataset.get("direct_context_sha256"),
        })
        summary.update(**provenance, analysis_scope="item_only",
                       requirements=evidence.get("requirements", {}), direct_context=evidence.get("direct_context"))
        summary["interpretation"] += (
            " This is item-only analysis based on explicit deployment requirements. "
            "No benchmark assessment was run; Input Form and Output Form are not assessed. "
            "Completion refers only to classifying this item snapshot, not to a complete benchmark validity assessment."
        )
    _write_items_csv(run_dir, items, results, definitions, provenance)
    summary["review_selection"] = _export_review(run_dir, selected_items if generic else items, definitions, provenance)
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
    (run_dir / "report.html").write_text(_render_html(summary, items, reporting_results), encoding="utf-8")
    return summary


def _escape(value: Any) -> str:
    return html.escape(_text(value), quote=True)


def _display_percent(value: float | None) -> str:
    return "—" if value is None else f"{value:.1f}%"


def _friendly(value: Any) -> str:
    names = {
        "match": "Category match", "no_match": "No category match",
        "issue_identified": "Issue identified", "no_issue_identified": "No issue identified",
        "insufficient_evidence": "Insufficient evidence", "invalid": "Invalid response",
    }
    return names.get(str(value), str(value).replace("_", " ").capitalize())


def _render_fields(value: Any) -> str:
    """Render nested evidence as readable text with all original values escaped."""
    if isinstance(value, dict):
        return "<dl>" + "".join(
            f"<dt>{_escape(str(key).replace('_', ' ').capitalize())}</dt><dd>{_render_fields(entry)}</dd>"
            for key, entry in value.items()
        ) + "</dl>" if value else "<p>Not supplied.</p>"
    if isinstance(value, list):
        return "<ul>" + "".join(f"<li>{_render_fields(entry)}</li>" for entry in value) + "</ul>" if value else "<p>None recorded.</p>"
    return f"<p class='text'>{_escape(value) if value is not None else 'Not supplied'}</p>"


def _run_readiness(summary: dict) -> str:
    state = summary.get("run", {}).get("status")
    experiment = summary["experiment"]
    if state in {"cancelled", "failed"}:
        return "Stopped — saved results retained" if state == "cancelled" else "Run failed — saved results retained"
    if summary["complete_snapshot"]:
        return "Prepared snapshot complete"
    if not experiment["selected_items"]:
        return "Specification prepared — classification not started"
    if (experiment["selected_completed_items"] == experiment["selected_items"]
            and not experiment["invalid_item_classifier_judgments"]):
        return "Selected sample complete — remaining prepared items not classified"
    return "Partial results — classification incomplete"


def _render_html(summary: dict, items: Iterable[dict], results: dict) -> str:
    parts = ["""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Caliper item analysis</title><style>
body{font:16px/1.6 system-ui,sans-serif;max-width:1100px;margin:auto;padding:2rem;color:#17212f;background:#fafbfc}
h1,h2,h3{line-height:1.25}section{background:white;padding:1.5rem;margin:1.5rem 0;border:1px solid #dce2e8;border-radius:8px}
table{border-collapse:collapse;width:100%;margin:1rem 0}th,td{text-align:left;padding:.5rem;border-bottom:1px solid #dce2e8;vertical-align:top}
.table-scroll{max-width:100%;overflow-x:auto}
pre,.text{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}small{color:#465368}a{color:#175c9e}.notice{background:#edf3fa;padding:1rem}
details{margin:.8rem 0}summary{cursor:pointer;font-weight:600}dt{font-weight:600;margin-top:.6rem}dd{margin-left:1rem}dd p,li p{margin:.25rem 0}.metrics{display:flex;flex-wrap:wrap;gap:1.5rem}.metric strong{display:block;font-size:1.8rem}.status{font-weight:600;color:#254b70}code{overflow-wrap:anywhere}nav{display:flex;gap:1rem;flex-wrap:wrap}@media(max-width:650px){body{padding:1rem}section{padding:1rem}table{font-size:.85rem}}@media print{body{max-width:none;background:white}section{break-inside:avoid}nav{display:none}}
</style><body><h1>Caliper item analysis</h1>"""]
    experiment = summary["experiment"]
    parts.append(
        f"<p><strong>{_escape(summary['benchmark'])}</strong></p>"
        f"<p><strong>Classifier deployment:</strong> {_escape(summary['deployment'])}</p>"
        f"<p class='status'>{_escape(_run_readiness(summary))}</p>"
        "<nav aria-label='Report sections'><a href='#item-statistics'>Item statistics</a>"
        "<a href='#original-assessment'>Original assessment</a><a href='#human-review'>Human review</a>"
        "<a href='#audit'>Methods and provenance</a></nav>"
        "<section id='item-statistics'><h2>Item statistics</h2>"
        f"<p>{experiment['classifier_count']} item dimensions summarize the selected sample. These judgments do not revise the original six-dimension benchmark assessment.</p>"
        "<div class='metrics'>"
    )
    for label, key in (("Selected items", "selected_items"), ("Complete", "selected_completed_items"),
                       ("With errors", "selected_error_items"), ("Partially completed", "selected_partial_items"),
                       ("Pending", "selected_pending_items")):
        parts.append(f"<div class='metric'><strong>{experiment[key]}</strong>{label}</div>")
    parts.append(
        "</div>"
        "<p>These item counts are mutually exclusive. A partially completed item has saved judgments and pending dimensions; "
        "an item with errors may also contain saved judgments. Pending items have no saved item record.</p>"
        f"<p>{experiment['selected_items']} selected items × {experiment['classifier_count']} classifiers = "
        f"{experiment['expected_item_classifier_judgments']} expected judgments; "
        f"{experiment['completed_item_classifier_judgments']} valid judgments saved. "
        f"{experiment['error_item_classifier_judgments']} failed, {experiment['invalid_item_classifier_judgments']} invalid, "
        f"and {experiment['pending_item_classifier_judgments']} pending judgments.</p>"
    )
    if any(_generic(c) for c in summary["classifiers"]):
        parts.append("<table><tr><th>Item dimension</th><th>Category matches / issues</th><th>Valid judgments</th><th>Insufficient evidence</th><th>Failed / pending</th></tr>")
        for classifier in summary["classifiers"]:
            key = "match" if classifier["id"] == "input_ontology" else "issue_identified"
            parts.append(f"<tr><td><a href='#{_escape(classifier['id'])}'>{_escape(classifier['id'].replace('_', ' ').title())}</a></td>"
                         f"<td>{classifier['counts'][key]} ({_display_percent(classifier['percentages_among_valid'][key])})</td>"
                         f"<td>{classifier['valid_judgments']}</td><td>{classifier['insufficient_evidence']}</td>"
                         f"<td>{classifier['errors']} / {classifier['pending']}</td></tr>")
        parts.append("</table><p><small>Percentages use each dimension's valid judgments, including insufficient evidence. "
                     "A dash means there is no valid denominator. A category match and an issue are different judgments; compare their definitions below.</small></p>")
    parts.append(
        f"<details><summary>Prepared snapshot: {summary['total_items']} items</summary>"
        f"<p>{summary['completed_items']} completed / {summary['total_items']} prepared items; "
        f"{summary['error_items']} with errors; {summary['partial_items']} partially completed; "
        f"{summary['pending_items']} pending. {summary['total_items'] - experiment['selected_items']} prepared items "
        "are outside the current selection.</p></details>"
    )
    parts.append(
        f"<p class='notice'>{_escape(summary['interpretation'])} "
        "A category not observed in a partial run is not demonstrated absent from the benchmark.</p></section>"
    )
    parts.append(
        "<p><a href='items.csv'>All items and predictions (CSV)</a> · " +
        ("<a href='review.csv'>Review worksheet</a> · " if summary["review_selection"].get("item_ids") else "") +
        "<a href='classifier_spec.json'>Classifier specification</a> · "
        "<a href='summary.json'>Summary JSON</a></p>"
        "<p><small>These links need the companion files beside this report. "
        "On the website, download and extract the complete results package to open them.</small></p>"
    )
    if summary.get("assessment_status") == "not_run":
        parts.append(
            "<section id='original-assessment'><h2>Benchmark assessment not run</h2>"
            "<p>This item-only analysis uses explicit deployment requirements. "
            "There are no benchmark-level validity scores. Input Form and Output Form are not assessed.</p>"
            f"<details><summary>Supplied requirements</summary>{_render_fields(summary.get('requirements'))}</details></section>"
        )
    else:
        parts.append(
            "<section id='original-assessment'><h2>Original assessment: six benchmark dimensions</h2><p>These benchmark-level scores are retained unchanged. "
            "Input Form and Output Form remain at benchmark level. They are separate from the four item classifiers above.</p>"
            "<table><tr><th>Dimension</th><th>Original score</th><th>Original finding</th></tr>"
        )
        for dimension, assessment in summary["original_assessment"].items():
            score = assessment.get("score", "Not supplied") if isinstance(assessment, dict) else "Not supplied"
            parts.append(f"<tr><td>{_escape(dimension.replace('_', ' ').title())}</td><td>{_escape(score)}</td>"
                         f"<td><details><summary>Original finding</summary>{_render_fields(assessment or 'Not supplied')}</details></td></tr>")
        parts.append("</table></section>")
    if summary.get("original_report_available"):
        parts.append("<p><a href='original_benchmark_report.pdf'>Original benchmark report (PDF)</a></p>")
    # The HTML shows one example per observed judgment. Keep only those records,
    # even when exporting a large population or a fully classified run.
    example_ids = set()
    for classifier in summary["classifiers"]:
        if not classifier.get("applicable", True):
            continue
        seen = set()
        for item_id, result in results.items():
            if _classifier_state(result, classifier) != "complete":
                continue
            label, _, invalid = _judgment(result, classifier)
            key = "invalid" if invalid else label
            if key not in seen:
                seen.add(key)
                example_ids.add(item_id)
    item_by_id = {item["item_id"]: item for item in _items_with_ids(items, example_ids)}
    for classifier in summary["classifiers"]:
        if _generic(classifier):
            parts.append(_render_generic_classifier(classifier, item_by_id, results))
            continue
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
        grounding = "Grounding in explicit deployment requirements" if summary.get("assessment_status") == "not_run" else "Grounding in the original assessment"
        parts.append(f"<details><summary>{grounding}</summary><pre>{_escape(classifier.get('grounded_in'))}</pre></details>")
        parts.append("<h3>Examples</h3><p><small>First example of each observed label, including unknown. Inspect the CSV for all items.</small></p>")
        seen: set[str] = set()
        for item_id, result in results.items():
            if _classifier_state(result, classifier) != "complete":
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
        "<section id='human-review'><h2>Human review</h2>"
        f"<p>{_escape(selection.get('purpose', 'Existing review worksheet'))}. "
        f"{_escape(selection.get('instructions', ''))}</p>"
    )
    if "review_comparison" in summary:
        overall = summary["review_comparison"].get("overall", {})
        if overall:
            parts.append(
                f"<p>Overall judgment agreement: {_display_percent(overall['accuracy'] * 100 if overall['accuracy'] is not None else None)} "
                f"over {overall['compared']} item-classifier pairs. "
                "Insufficient evidence is an explicit judgment and participates in agreement. "
                "Operational errors are excluded and reported separately.</p>"
            )
        joint = overall.get("judgment_and_category_set_agreement")
        if joint:
            parts.append(
                f"<p>Overall agreement including Input Ontology category sets: "
                f"{_display_percent(joint['accuracy'] * 100 if joint['accuracy'] is not None else None)} "
                f"over {joint['compared']} item-classifier pairs.</p>"
            )
        parts.append(
            "<p>Agreement with independently supplied human labels.</p>"
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
        parts.append("</table>")
        ontology = summary["review_comparison"]["classifiers"].get("input_ontology", {}).get("category_set_agreement")
        if ontology:
            parts.append(
                f"<p>Input Ontology exact category-set agreement: "
                f"{_display_percent(ontology['accuracy'] * 100 if ontology['accuracy'] is not None else None)} "
                f"over {ontology['compared']} paired determinate judgments; "
                f"{ontology['insufficient_evidence_excluded']} pairs with insufficient evidence excluded.</p>"
            )
        parts.append("<p><a href='summary.json'>Comparison details and confusion counts in the summary JSON</a></p>")
    else:
        note = summary.get("review_comparison_status", {}).get(
            "note", "No human-label comparison has been supplied yet."
        )
        parts.append(f"<p>{_escape(note)} Full item coverage does not establish classification accuracy.</p>")
    parts.append("</section><section id='audit'><h2>Methods and provenance</h2>"
                 f"<p>{_escape(experiment['request_policy'].capitalize())}.</p>"
                 f"<p><strong>Schema:</strong> <code>{_escape(summary['schema_version'])}</code>; "
                 f"<strong>catalog:</strong> <code>{_escape(summary['fixed_catalog_version'])}</code>.</p>")
    for title, data in (("Run and export details", summary.get("run")),
                        ("Classification model", summary.get("classification")),
                        ("Specification provenance", summary.get("specification")),
                        ("Dataset provenance", summary.get("dataset")),
                        ("Original deployment requirements", summary.get("original_deployment"))):
        if data:
            parts.append(f"<details><summary>{title}</summary>{_render_fields(data)}</details>")
    parts.append("<p>This report works offline. Detailed data are in the accompanying relative-linked JSON and CSV files. "
                 "In a full results package, README.txt explains the audit files and separate reviewer worksheets.</p>")
    document = "\n".join([*parts, "</section></body></html>"])
    return document.replace("<table>", "<div class='table-scroll' role='region' aria-label='Scrollable data table' tabindex='0'><table>").replace("</table>", "</table></div>")



def _render_generic_classifier(classifier: dict, item_by_id: dict, results: dict) -> str:
    parts = [f"<section id='{_escape(classifier['id'])}'><h2>{_escape(classifier['id'].replace('_', ' ').title())}</h2>",
             f"<p>{_escape(classifier['question'])}</p>",
             f"<p>{classifier['determinate_judgments']} determinate judgments; "
             f"{classifier['insufficient_evidence']} insufficient evidence; {classifier['invalid']} invalid; "
             f"{classifier['errors']} operational errors; {classifier['pending']} pending.</p>",
             "<table><tr><th>Judgment</th><th>Count</th><th>Percent of valid judgments</th></tr>"]
    for label, count in classifier["counts"].items():
        parts.append(f"<tr><td>{_escape(_friendly(label))} <small>(<code>{_escape(label)}</code>)</small></td><td>{count}</td>"
                     f"<td>{_display_percent(classifier['percentages_among_valid'][label])}</td></tr>")
    parts.append("</table>")
    if classifier["id"] == "input_ontology":
        parts.append(f"<p><strong>Required-category inventory:</strong> {_escape(classifier['inventory_completeness'])}. "
                     f"{_escape(classifier['coverage_interpretation'])}</p>")
        parts.append("<table><tr><th>Category ID</th><th>Name</th><th>Matched items</th></tr>")
        for category in classifier["input_category_inventory"]["categories"]:
            parts.append(f"<tr><td>{_escape(category['id'])}</td><td>{_escape(category['name'])}</td>"
                         f"<td>{classifier['category_counts'][category['id']]}</td></tr>")
        parts.append("</table>")
        missing = classifier["required_categories_not_observed"]
        parts.append(f"<p>Required categories not observed: {_escape(', '.join(missing) if missing else 'None')}.</p>")
        parts.append("<details><summary>Required-category definitions, sources, and inventory gaps</summary>"
                     f"{_render_fields(classifier['input_category_inventory'])}</details>")
    parts.append("<details><summary>Fixed decision rules and sourced context</summary>"
                 f"{_render_fields({'decision_rules': classifier.get('decision_rules'), 'context': classifier.get('context')})}</details>")
    parts.append("<details><summary>Item examples and evidence</summary><p><small>First item for each observed judgment; inspect the CSV for all items.</small></p>")
    seen = set()
    for item_id, result in results.items():
        if _classifier_state(result, classifier) != "complete":
            continue
        label, judgment, invalid = _judgment(result, classifier)
        key = "invalid" if invalid else label
        if key in seen:
            continue
        seen.add(key)
        item = item_by_id[item_id]
        parts.append(f"<details><summary>{_escape(_friendly(key))} <small>{_escape(key)} · {_escape(item_id)}</small></summary>"
                     f"<pre>{_escape(_text(item.get('content'))[:2000])}</pre>"
                     f"<p><strong>Reference:</strong> {_escape(item.get('reference_answer'))}</p>"
                     f"<p><strong>Matched category IDs:</strong> {_escape(', '.join(judgment.get('matched_category_ids', [])) or 'None')}</p>"
                     f"<strong>Item evidence:</strong>{_render_fields(judgment.get('evidence'))}"
                     f"<p>{_escape(judgment.get('justification'))}</p></details>")
    return "\n".join([*parts, "</details></section>"])

def _parse_human_label(raw: str, classifier: dict) -> Any:
    if raw == "unknown" and not _generic(classifier):
        return None
    for option in allowed_labels(classifier):
        if raw == str(option):
            return option
    suffix = "" if _generic(classifier) else " or 'unknown'"
    raise ValueError(f"Invalid human label {raw!r} for {classifier['id']}; expected {allowed_labels(classifier)}{suffix}")


def compare_review(run_dir: Path, review_path: Path) -> dict:
    """Validate a filled blind-review CSV, save agreement, and refresh the report."""
    run_dir, review_path = Path(run_dir), Path(review_path).resolve()
    spec, items, results = _load_run(run_dir)
    classifiers = [classifier for classifier in spec["classifiers"] if classifier["applicable"]]
    item_ids = items.item_ids
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
    if is_generic_spec(spec):
        comparison = _compare_generic_review(spec, rows, results)
        comparison.update(review_path=str(review_path), reviewed_rows=len(rows),
                          input_hashes=_comparison_inputs(run_dir, review_path))
        _write_json(run_dir / "review_comparison.json", comparison)
        generate_report(run_dir)
        return comparison
    comparison = {
        **_versions(spec),
        "review_schema_version": "legacy_item_review_v1",
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
            if _classifier_state(result, classifier) != "complete":
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


def _agreement(pairs: list[tuple[str, str]]) -> dict:
    total = len(pairs)
    matches = sum(human == model for human, model in pairs)
    accuracy = matches / total if total else None
    human_counts = Counter(human for human, _ in pairs)
    model_counts = Counter(model for _, model in pairs)
    expected = sum(human_counts[label] * model_counts[label] for label in human_counts) / total**2 if total else 0
    return {
        "compared": total, "matches": matches, "accuracy": accuracy,
        "cohen_kappa": (accuracy - expected) / (1 - expected) if total and expected < 1 else None,
        "confusion": [{"human": human, "model": model, "count": count}
                      for (human, model), count in sorted(Counter(pairs).items())],
    }


def _human_ids(row: dict, field: str) -> list[str]:
    try:
        value = json.loads(row.get(field) or "[]")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Review {row['item_id']}: {field} must be a JSON array of IDs") from exc
    if (not isinstance(value, list) or any(not isinstance(entry, str) for entry in value)
            or len(value) != len(set(value))):
        raise ValueError(f"Review {row['item_id']}: {field} must contain unique string IDs")
    return value


def _compare_generic_review(spec: dict, rows: list[dict], results: dict) -> dict:
    comparison = {**_versions(spec), "review_schema_version": "caliper_item_review_v2", "classifiers": {}}
    inventory = spec["input_category_inventory"]
    category_ids = {category["id"] for category in inventory["categories"]}
    item_agreement = {row["item_id"]: [] for row in rows}
    for original in spec["classifiers"]:
        classifier = dict(original)
        classifier.update(input_category_inventory=inventory, source_registry=spec["source_registry"], source_roles=spec["source_roles"])
        classifier_id = classifier["id"]
        pairs = []
        counts = Counter()
        category_pairs = []
        joint_matches = 0
        for row in rows:
            raw = (row.get(classifier_id) or "").strip()
            if not raw:
                counts["unreviewed"] += 1
                continue
            human = _parse_human_label(raw, classifier)
            for field in ("evidence", "justification"):
                if not (row.get(f"{classifier_id}.{field}") or "").strip():
                    raise ValueError(f"Review {row['item_id']}: {classifier_id} requires item evidence and justification")
            human_categories = []
            if classifier_id == "input_ontology":
                field = "input_ontology.matched_category_ids"
                if not (row.get(field) or "").strip():
                    raise ValueError(f"Review {row['item_id']}: enter a JSON array in {field}, including [] when empty")
                human_categories = _human_ids(row, field)
                if set(human_categories) - category_ids or bool(human_categories) != (human == "match"):
                    raise ValueError(f"Review {row['item_id']}: category IDs must be in the inventory and nonempty only for match")
                if human == "no_match" and inventory["completeness"] != "complete":
                    exclusions = _human_ids(row, "input_ontology.scope_exclusion_source_ids")
                    if (not exclusions or set(exclusions) - set(spec["source_registry"])
                            or any(spec["source_roles"].get(ref) != "deployment_requirement" for ref in exclusions)):
                        raise ValueError(f"Review {row['item_id']}: partial/unknown inventory no_match needs scope exclusion source IDs")
            counts["human_insufficient_evidence"] += human == "insufficient_evidence"
            result = results.get(row["item_id"], {})
            state = _classifier_state(result, classifier)
            if state != "complete":
                counts["model_unavailable"] += 1
                counts["model_errors" if state == "error" else "model_pending"] += 1
                continue
            model, judgment, invalid = _judgment(result, classifier)
            if invalid:
                counts["invalid_model_labels"] += 1
                continue
            counts["model_insufficient_evidence"] += model == "insufficient_evidence"
            pairs.append((human, model))
            equal = human == model
            if classifier_id == "input_ontology":
                same_categories = set(human_categories) == set(judgment["matched_category_ids"])
                if "insufficient_evidence" in (human, model):
                    counts["category_insufficient_evidence_excluded"] += 1
                else:
                    category_pairs.append(same_categories)
                equal = equal and same_categories
                joint_matches += equal
            item_agreement[row["item_id"]].append(equal)
        result = _agreement(pairs)
        for name in ("unreviewed", "model_unavailable", "model_errors", "model_pending", "invalid_model_labels",
                     "human_insufficient_evidence", "model_insufficient_evidence"):
            result[name] = counts[name]
        if classifier_id == "input_ontology":
            total = len(category_pairs)
            result["category_set_agreement"] = {
                "compared": total, "matches": sum(category_pairs),
                "accuracy": sum(category_pairs) / total if total else None,
                "insufficient_evidence_excluded": counts["category_insufficient_evidence_excluded"],
                "denominator": "paired determinate judgments; sets compared without order",
            }
            result["judgment_and_category_set_agreement"] = {
                "compared": len(pairs), "matches": joint_matches,
                "accuracy": joint_matches / len(pairs) if pairs else None,
            }
        comparison["classifiers"][classifier_id] = result
    by_classifier = list(comparison["classifiers"].values())
    compared = sum(result["compared"] for result in by_classifier)
    matches = sum(result["matches"] for result in by_classifier)
    accuracies = [result["accuracy"] for result in by_classifier if result["accuracy"] is not None]
    item_pairs = [all(labels) for labels in item_agreement.values() if len(labels) == len(spec["classifiers"])]
    joint_matches = sum(result.get("judgment_and_category_set_agreement", result)["matches"] for result in by_classifier)
    comparison["overall"] = {
        "judgment_agreement": {"compared": compared, "matches": matches, "accuracy": matches / compared if compared else None},
        "judgment_and_category_set_agreement": {
            "compared": compared, "matches": joint_matches, "accuracy": joint_matches / compared if compared else None,
            "definition": "pooled item-classifier agreement; Input Ontology requires both judgment and category-set agreement",
        },
        "compared": compared, "matches": matches, "accuracy": matches / compared if compared else None,
        "macro_classifier_accuracy": sum(accuracies) / len(accuracies) if accuracies else None,
        "denominator": "judgment labels on reviewed item-classifier pairs with valid model results, including insufficient_evidence",
        "fully_compared_items": len(item_pairs), "fully_matching_items": sum(item_pairs),
        "item_exact_agreement": sum(item_pairs) / len(item_pairs) if item_pairs else None,
        "item_exact_agreement_definition": "all classifier judgments and the Input Ontology category set agree",
        **{name: sum(result[name] for result in by_classifier)
           for name in ("model_errors", "model_pending", "invalid_model_labels", "unreviewed")},
    }
    return comparison
