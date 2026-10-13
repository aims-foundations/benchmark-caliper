"""Reporting must preserve denominators, review independence, and item identities."""

import csv
import hashlib
import json

import pytest

from item_analysis.report import compare_review, generate_report


@pytest.fixture
def prepared_run(tmp_path):
    classifiers = [
        {
            "id": "IO.task_category", "component": "input_ontology", "operation": "assignment",
            "applicable": True, "criterion": "Which task?", "category_set": ["math", "history", "irrelevant_other"],
            "aggregate": "coverage_vs_required",
        },
        {
            "id": "OO.output_category", "component": "output_ontology", "operation": "assignment",
            "applicable": False, "na_reason": "MCQ answer format is shared", "aggregate": "category_distribution",
        },
        {
            "id": "OO.value_encoding", "component": "output_ontology", "operation": "flag",
            "applicable": True, "criterion": "Check the convention", "positive_class": "convention-dependent",
            "aggregate": "prevalence",
        },
        {
            "id": "IC.region_fit", "component": "input_content", "operation": "ordinal",
            "applicable": True, "criterion": "Regional fit", "ordinal_anchors": {"1": "relevant", "2": "neutral", "3": "misaligned"},
            "aggregate": "category_distribution",
        },
    ]
    spec = {"benchmark": "test", "deployment": "<script>alert('deployment')</script>", "classifiers": classifiers}
    (tmp_path / "classifier_spec.json").write_text(json.dumps(spec))
    (tmp_path / "dataset.json").write_text(json.dumps({"benchmark": "test", "item_count": 4, "seed": 42, "source": "test.jsonl"}))
    (tmp_path / "evidence.json").write_text(json.dumps({"scoring": {"dimensions": {"input_form": {"score": 2, "justification": "Shared format finding"}}}}))
    items = [{"item_id": f"item-{index}", "content": "<img src=x onerror=alert(1)>", "reference_answer": "A"} for index in range(4)]
    _write_jsonl(tmp_path / "items.jsonl", items)
    return tmp_path


def _write_jsonl(path, records):
    path.write_text("".join(json.dumps(record) + "\n" for record in records))


def _complete(item_id, task="math", flag=1, fit=2):
    return {
        "item_id": item_id, "status": "complete",
        "labels": {
            "IO.task_category": {"label": task, "evidence": ["item stem"], "justification": "Example"},
            "OO.value_encoding": {"label": flag, "evidence": ["item answer"], "justification": "Example"},
            "IC.region_fit": {"label": fit, "evidence": ["item scenario"], "justification": "Example"},
        },
    }


def _by_id(summary, classifier_id):
    return next(classifier for classifier in summary["classifiers"] if classifier["id"] == classifier_id)


def test_retry_unknown_error_and_invalid_labels_have_separate_denominators(prepared_run):
    _write_jsonl(prepared_run / "results.jsonl", [
        {"item_id": "item-0", "status": "error", "error": "first attempt"},
        _complete("item-0"),
        {"item_id": "item-0", "status": "error", "error": "late failed retry"},
        _complete("item-1", task=None, flag=None),
        {"item_id": "item-2", "status": "error", "error": "unavailable"},
        _complete("item-3", task="unapproved-label", flag=True),
    ])
    summary = generate_report(prepared_run)
    task = _by_id(summary, "IO.task_category")
    assert task["counts"] == {"math": 1, "history": 0, "irrelevant_other": 0}
    assert (task["known"], task["unknown"], task["invalid"], task["errors"]) == (1, 1, 1, 1)
    assert task["percentages_among_known"]["math"] == 100
    assert task["unknown_percent_among_completed"] == pytest.approx(33.3333)
    assert task["required_categories_not_observed"] == ["history"]
    assert _by_id(summary, "OO.value_encoding")["counts"] == {"0": 0, "1": 1}
    assert _by_id(summary, "OO.output_category")["na_count"] == 4
    assert summary["completed_items"] == 3
    assert summary["error_items"] == 1
    assert not summary["complete_snapshot"]
    assert summary["original_assessment"]["input_form"]["score"] == 2


def test_report_escapes_content_and_exports_all_items(prepared_run):
    _write_jsonl(prepared_run / "results.jsonl", [_complete("item-0")])
    generate_report(prepared_run)
    report = (prepared_run / "report.html").read_text()
    assert "<script>alert" not in report
    assert "<img src=x" not in report
    assert "&lt;script&gt;" in report
    assert "&lt;img src=x" in report
    assert "not demonstrated absent" in report
    assert "Shared format finding" in report
    with (prepared_run / "items.csv").open() as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 4
    assert rows[0]["status"] == "complete"
    assert rows[1]["status"] == "pending"


def test_review_reserves_holdout_before_classification_and_never_overwrites(prepared_run):
    items = [{"item_id": f"item-{index}", "content": "A question", "reference_answer": "A"} for index in range(180)]
    _write_jsonl(prepared_run / "items.jsonl", items)
    summary = generate_report(prepared_run)
    assert summary["review_selection"]["item_ids"] == [f"item-{index}" for index in range(100, 150)]
    with (prepared_run / "review.csv").open() as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 50
    assert rows[0]["IO.task_category"] == ""
    assert "OO.output_category" not in rows[0]
    assert not any("prediction" in column or "justification" in column for column in rows[0])
    (prepared_run / "review.csv").write_text("human editing in progress")
    generate_report(prepared_run)
    assert (prepared_run / "review.csv").read_text() == "human editing in progress"


def test_empty_and_full_runs_report_completeness_honestly(prepared_run):
    summary = generate_report(prepared_run)
    assert summary["pending_items"] == 4
    assert not summary["complete_snapshot"]
    assert _by_id(summary, "IO.task_category")["percentages_among_known"]["math"] is None
    _write_jsonl(prepared_run / "results.jsonl", [_complete(f"item-{index}", task=None) for index in range(4)])
    summary = generate_report(prepared_run)
    assert summary["complete_snapshot"]
    assert _by_id(summary, "IO.task_category")["unknown"] == 4
    assert summary["scope"] == "all items in the prepared snapshot"


def test_review_compares_typed_labels_and_keeps_unknown_disagreements(prepared_run):
    _write_jsonl(prepared_run / "results.jsonl", [
        _complete("item-0", flag=1), _complete("item-1", flag=0),
        _complete("item-2", flag=None), _complete("item-3", flag=1),
    ])
    generate_report(prepared_run)
    with (prepared_run / "review.csv").open() as file:
        rows = list(csv.DictReader(file))
    for row, flag in zip(rows, ["1", "1", "0", "unknown"]):
        row["OO.value_encoding"] = flag
    with (prepared_run / "review.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    comparison = compare_review(prepared_run, prepared_run / "review.csv")
    flag = comparison["classifiers"]["OO.value_encoding"]
    assert flag["compared"] == 3
    assert flag["accuracy"] == pytest.approx(1 / 3)
    assert flag["cohen_kappa"] == pytest.approx(0)
    assert flag["human_unknown_excluded"] == 1
    assert flag["model_unknown_included_as_disagreement"] == 1
    assert comparison["classifiers"]["IO.task_category"]["unreviewed"] == 4
    assert (prepared_run / "review_comparison.json").exists()
    assert "Comparison details" in (prepared_run / "report.html").read_text()


def test_review_rejects_invalid_labels_before_saving_comparison(prepared_run):
    generate_report(prepared_run)
    with (prepared_run / "review.csv").open() as file:
        rows = list(csv.DictReader(file))
    rows[0]["OO.value_encoding"] = "yes"
    with (prepared_run / "review.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="Invalid human label"):
        compare_review(prepared_run, prepared_run / "review.csv")
    assert not (prepared_run / "review_comparison.json").exists()


def test_results_outside_prepared_snapshot_fail_visibly(prepared_run):
    _write_jsonl(prepared_run / "results.jsonl", [_complete("foreign-item")])
    with pytest.raises(ValueError, match="outside the prepared dataset"):
        generate_report(prepared_run)


def test_provenance_is_visible_and_malformed_evidence_prevents_completion(prepared_run):
    (prepared_run / "evidence.json").write_text(json.dumps({"deployment": "Original deployment requirements"}))
    metadata = {
        "source": {"kind": "provided"},
        "evidence_references_checked": False,
        "note": "Imported citations remain unverified.",
        "adjustments": [{"id": "OO.output_category", "after": False, "reason": "MCQ output-uniformity gate"}],
        "spec_sha256": hashlib.sha256((prepared_run / "classifier_spec.json").read_bytes()).hexdigest(),
        "dataset_sha256": hashlib.sha256((prepared_run / "dataset.json").read_bytes()).hexdigest(),
    }
    (prepared_run / "specification.json").write_text(json.dumps(metadata))
    records = [_complete(f"item-{index}") for index in range(4)]
    records[0]["labels"]["IC.region_fit"]["evidence"] = "incorrectly encoded string"
    _write_jsonl(prepared_run / "results.jsonl", records)
    summary = generate_report(prepared_run)
    assert not summary["complete_snapshot"]
    assert _by_id(summary, "IC.region_fit")["invalid"] == 1
    assert summary["original_deployment"] == "Original deployment requirements"
    assert summary["specification"] == metadata
    report = (prepared_run / "report.html").read_text()
    assert "Original deployment requirements" in report
    assert "Imported citations remain unverified" in report
    assert "MCQ output-uniformity gate" in report


def test_jsonl_preserves_unicode_separators_inside_item_and_evidence_text(prepared_run):
    text = "A paragraph\u2028with a line separator\u2029and a paragraph separator\u0085and next-line"
    item = {"item_id": "unicode", "content": text, "reference_answer": "A"}
    result = _complete("unicode")
    result["labels"]["IO.task_category"]["evidence"] = [text]
    for filename, record in (("items.jsonl", item), ("results.jsonl", result)):
        (prepared_run / filename).write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = generate_report(prepared_run)
    assert summary["complete_snapshot"]
    with (prepared_run / "items.csv").open(encoding="utf-8", newline="") as file:
        row = next(csv.DictReader(file))
    assert row["content"] == text
    assert json.loads(row["IO.task_category.evidence"]) == [text]


def test_report_rejects_changed_frozen_specification(prepared_run):
    metadata = {
        "spec_sha256": hashlib.sha256((prepared_run / "classifier_spec.json").read_bytes()).hexdigest(),
        "dataset_sha256": hashlib.sha256((prepared_run / "dataset.json").read_bytes()).hexdigest(),
    }
    (prepared_run / "specification.json").write_text(json.dumps(metadata))
    spec_path = prepared_run / "classifier_spec.json"
    spec = json.loads(spec_path.read_text())
    spec["classifiers"][0]["criterion"] = "A different criterion"
    spec_path.write_text(json.dumps(spec))
    with pytest.raises(ValueError):
        generate_report(prepared_run)


@pytest.mark.parametrize("changed_file", ["review.csv", "results.jsonl"])
def test_changed_review_or_predictions_hide_stale_agreement(prepared_run, changed_file):
    _write_jsonl(prepared_run / "results.jsonl", [_complete("item-0")])
    generate_report(prepared_run)
    compare_review(prepared_run, prepared_run / "review.csv")
    summary = generate_report(prepared_run)
    assert summary["review_comparison_status"]["current"]
    assert "review_comparison" in summary
    with (prepared_run / changed_file).open("a") as file:
        file.write("\n")
    summary = generate_report(prepared_run)
    assert not summary["review_comparison_status"]["current"]
    assert "review_comparison" not in summary
    assert "comparison is stale" in (prepared_run / "report.html").read_text()
