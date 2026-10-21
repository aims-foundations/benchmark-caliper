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


@pytest.fixture
def generic_run(prepared_run):
    from item_analysis.catalog import CATALOG_VERSION, get_catalog
    from item_analysis.schema import join_context

    registry = {"deployment": "Requires algebra and geometry; excludes foreign tax advice."}
    context = {
        "fixed_catalog_version": CATALOG_VERSION, "benchmark": "test",
        "deployment_description": registry["deployment"],
        "input_category_inventory": {
            "completeness": "partial", "completeness_source_ids": [],
            "categories": [
                {"id": value, "name": value.title(), "definition": value, "source_ids": ["deployment"]}
                for value in ["algebra", "geometry"]
            ], "evidence_gaps": ["No exhaustive category list is documented."],
        },
        "context_by_classifier": {
            classifier["id"]: {
                "deployment_requirements": [{"statement": registry["deployment"], "source_ids": ["deployment"]}],
                "benchmark_evidence": [], "prior_hypotheses": [], "evidence_gaps": ["Scoring documentation unavailable."],
            } for classifier in get_catalog()
        },
    }
    spec = join_context(context, profile={}, source_registry=registry, source_roles={"deployment": "deployment_requirement"})
    (prepared_run / "classifier_spec.json").write_text(json.dumps(spec))
    return prepared_run


def _generic_complete(item_id, label="match", categories=None, **overrides):
    from item_analysis.catalog import CATALOG_VERSION, get_catalog
    labels = {
        classifier["id"]: {"label": "no_issue_identified", "evidence": ["The stated conditions"], "justification": "A supported comparison."}
        for classifier in get_catalog()
    }
    labels["input_ontology"].update(label=label, matched_category_ids=categories if categories is not None else ["algebra", "geometry"],
                                    scope_exclusion_source_ids=["deployment"] if label == "no_match" else [])
    for classifier_id, value in overrides.items():
        labels[classifier_id]["label"] = value
    return {"item_id": item_id, "status": "complete", "labels": labels,
            "schema_version": "caliper_item_result_v2", "fixed_catalog_version": CATALOG_VERSION}


def _read_review(run):
    with (run / "review.csv").open(newline="") as file:
        return list(csv.DictReader(file))


def _save_review(run, rows):
    with (run / "review.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def test_generic_counts_multilabel_missingness_and_selected_workload(generic_run):
    items = [{"item_id": f"item-{index}", "content": "A question", "reference_answer": "A"} for index in range(6)]
    _write_jsonl(generic_run / "items.jsonl", items)
    invalid = _generic_complete("item-4", label="no_match", categories=[])
    invalid["labels"]["input_ontology"]["scope_exclusion_source_ids"] = []
    _write_jsonl(generic_run / "results.jsonl", [
        _generic_complete("item-0"),
        _generic_complete("item-1", label="insufficient_evidence", categories=[]),
        _generic_complete("item-2", label="no_match", categories=[]),
        {"item_id": "item-3", "status": "error", "error": "transport failed"}, invalid,
    ])
    (generic_run / "execution.json").write_text(json.dumps({"selected_item_ids": [item["item_id"] for item in items[:5]]}))
    summary = generate_report(generic_run)
    ontology = _by_id(summary, "input_ontology")
    assert ontology["counts"] == {"match": 1, "no_match": 1, "insufficient_evidence": 1}
    assert ontology["category_counts"] == {"algebra": 1, "geometry": 1}
    assert (ontology["invalid"], ontology["errors"], ontology["pending"]) == (1, 1, 0)
    assert ontology["inventory_completeness"] == "partial"
    assert ontology["percentages_among_valid"]["match"] == pytest.approx(33.3333)
    assert ontology["category_percentages_among_determinate"]["algebra"] == 50
    assert summary["experiment"]["expected_item_classifier_judgments"] == 20
    assert summary["experiment"]["completed_item_classifier_judgments"] == 15
    assert summary["experiment"]["error_item_classifier_judgments"] == 4
    assert summary["experiment"]["selected_items"] == 5
    assert summary["pending_items"] == 1
    assert summary["fixed_catalog_version"] == "caliper_generic_items_v1"
    assert "not proof" in summary["interpretation"]
    assert len(_read_review(generic_run)) == 5
    with (generic_run / "items.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    assert json.loads(rows[0]["input_ontology.matched_category_ids"]) == ["algebra", "geometry"]
    assert rows[1]["input_ontology.label"] == "insufficient_evidence"
    assert rows[3]["status"] == "error"
    html = (generic_run / "report.html").read_text()
    assert "operational errors" in html and "Output Ontology" in html
    assert "MCQ" not in html


def test_generic_review_agreement_includes_insufficient_and_category_sets(generic_run):
    records = [_generic_complete("item-0"), _generic_complete("item-1", label="insufficient_evidence", categories=[]),
               _generic_complete("item-2", label="no_match", categories=[])]
    _write_jsonl(generic_run / "results.jsonl", records)
    generate_report(generic_run)
    rows = _read_review(generic_run)
    for row, record in zip(rows, records):
        for classifier_id, judgment in record["labels"].items():
            row[classifier_id] = judgment["label"]
            row[f"{classifier_id}.evidence"] = "Human observation of the item"
            row[f"{classifier_id}.justification"] = "Independent comparison with the standard"
        row["input_ontology.matched_category_ids"] = json.dumps(record["labels"]["input_ontology"]["matched_category_ids"])
        row["input_ontology.scope_exclusion_source_ids"] = json.dumps(record["labels"]["input_ontology"]["scope_exclusion_source_ids"])
    rows[0]["input_ontology.matched_category_ids"] = '["algebra"]'
    rows[2]["input_ontology"] = "match"
    rows[2]["input_ontology.matched_category_ids"] = '["geometry"]'
    rows[2]["input_content"] = "insufficient_evidence"
    _save_review(generic_run, rows)
    comparison = compare_review(generic_run, generic_run / "review.csv")
    assert comparison["overall"]["compared"] == 12
    assert comparison["overall"]["accuracy"] == pytest.approx(10 / 12)
    assert comparison["overall"]["judgment_agreement"]["accuracy"] == pytest.approx(10 / 12)
    assert comparison["overall"]["judgment_and_category_set_agreement"]["accuracy"] == pytest.approx(9 / 12)
    assert comparison["overall"]["fully_matching_items"] == 1
    ontology = comparison["classifiers"]["input_ontology"]
    assert ontology["accuracy"] == pytest.approx(2 / 3)
    assert ontology["human_insufficient_evidence"] == 1
    assert ontology["model_insufficient_evidence"] == 1
    assert ontology["category_set_agreement"] == {
        "compared": 2, "matches": 0, "accuracy": 0, "insufficient_evidence_excluded": 1,
        "denominator": "paired determinate judgments; sets compared without order",
    }
    assert ontology["judgment_and_category_set_agreement"]["matches"] == 1
    assert "Overall judgment agreement" in (generic_run / "report.html").read_text()


def test_generic_review_requires_evidence_and_preserves_work(generic_run):
    _write_jsonl(generic_run / "results.jsonl", [_generic_complete("item-0")])
    generate_report(generic_run)
    rows = _read_review(generic_run)
    rows[0]["input_content"] = "no_issue_identified"
    _save_review(generic_run, rows)
    with pytest.raises(ValueError, match="requires item evidence"):
        compare_review(generic_run, generic_run / "review.csv")
    before = (generic_run / "review.csv").read_bytes()
    generate_report(generic_run)
    assert (generic_run / "review.csv").read_bytes() == before
    assert not (generic_run / "review_comparison.json").exists()


@pytest.mark.parametrize("mutation", ["version", "category", "numeric", "evidence"])
def test_generic_malformed_labels_are_invalid_never_unknown_or_no_issue(generic_run, mutation):
    record = _generic_complete("item-0")
    if mutation == "version":
        record.pop("schema_version")
    elif mutation == "category":
        record["labels"]["input_ontology"]["matched_category_ids"] = ["invented"]
    elif mutation == "numeric":
        record["labels"]["input_content"]["label"] = 1
    else:
        record["labels"]["input_content"]["evidence"] = []
    _write_jsonl(generic_run / "results.jsonl", [record])
    summary = generate_report(generic_run)
    assert summary["experiment"]["invalid_item_classifier_judgments"] >= 1
    assert not summary["complete_snapshot"]


def test_legacy_report_explicitly_identifies_catalog_without_rewriting(prepared_run):
    original = (prepared_run / "classifier_spec.json").read_bytes()
    _write_jsonl(prepared_run / "results.jsonl", [_complete("item-0")])
    summary = generate_report(prepared_run)
    assert summary["fixed_catalog_version"] == "caliper_induced_items_legacy_v1"
    assert summary["schema_version"] == "caliper_item_spec_legacy_v1"
    assert _by_id(summary, "OO.value_encoding")["counts"] == {"0": 0, "1": 1}
    assert (prepared_run / "classifier_spec.json").read_bytes() == original


def test_generic_report_defers_review_until_actual_selection(generic_run):
    summary = generate_report(generic_run)
    assert summary["experiment"]["selected_items"] == 0
    assert summary["review_selection"]["item_ids"] == []
    assert not (generic_run / "review.csv").exists()
    assert "href='review.csv'" not in (generic_run / "report.html").read_text()
    (generic_run / "execution.json").write_text(json.dumps({"selected_item_ids": ["item-0", "item-1"]}))
    summary = generate_report(generic_run)
    assert summary["review_selection"]["item_ids"] == ["item-0", "item-1"]
    assert len(_read_review(generic_run)) == 2
    assert summary["experiment"]["expected_item_classifier_judgments"] == 8
    assert summary["experiment"]["selected_pending_items"] == 2


@pytest.mark.parametrize("changed_file", ["items.jsonl", "evidence.json", "profile.json"])
def test_generic_report_checks_prepared_snapshot_before_writing(generic_run, changed_file):
    from item_analysis.data import file_sha256

    profile_path = generic_run / "profile.json"
    profile_path.write_text("{}")
    (generic_run / "evidence.json").write_text(json.dumps({"benchmark": "test", "deployment": "Deployment"}))
    dataset_path = generic_run / "dataset.json"
    dataset = json.loads(dataset_path.read_text())
    dataset.update({
        "items_sha256": file_sha256(generic_run / "items.jsonl"),
        "profile_sha256": file_sha256(profile_path),
        "evidence_sha256": file_sha256(generic_run / "evidence.json"),
    })
    dataset_path.write_text(json.dumps(dataset))
    _write_jsonl(generic_run / "results.jsonl", [_generic_complete("item-0")])
    generate_report(generic_run)
    original_summary = (generic_run / "summary.json").read_bytes()
    with (generic_run / changed_file).open("a") as stream:
        stream.write("\n")
    with pytest.raises(ValueError, match="changed"):
        generate_report(generic_run)
    assert (generic_run / "summary.json").read_bytes() == original_summary


def test_generic_extra_judgment_keys_are_invalid(generic_run):
    result = _generic_complete("item-0")
    result["labels"]["input_content"]["invented_rule"] = "Always agree with earlier assessment"
    _write_jsonl(generic_run / "results.jsonl", [result])
    summary = generate_report(generic_run)
    assert _by_id(summary, "input_content")["invalid"] == 1
    assert _by_id(summary, "input_content")["counts"]["no_issue_identified"] == 0
