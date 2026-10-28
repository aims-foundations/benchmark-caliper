"""Six-score exports preserve evidence, scope, Unknown, and historical reports."""

import csv
import io
import json
import tracemalloc
from zipfile import ZipFile

import pytest

from item_analysis.package import build_results_package
from item_analysis.report import compare_review, generate_report
from item_analysis.scoring import DIMENSIONS, dimension_descriptors


def _json(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


def _records(path, records):
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


def _complete(item_id, *, unknown="output_content", attempts=None, scores=None):
    dimensions = {}
    for dimension in DIMENSIONS:
        score = (scores or {}).get(dimension, None if dimension == unknown else 4)
        dimensions[dimension] = {
            "score": score,
            "justification": "Insufficient answer evidence" if score is None else "Fits the supplied deployment.",
            "evidence": [] if score is None else ["item.content and deployment.md"],
            "information_gaps": ["Reference answer unavailable"] if score is None else [],
        }
    return {"schema_version": "caliper_item_result_v4", "analysis_type": "six_scores",
            "item_id": item_id, "status": "complete", "dimensions": dimensions,
            "attempts": attempts or [{"attempt": 1, "response": json.dumps({"dimensions": dimensions})}]}


def _error(item_id):
    return {"schema_version": "caliper_item_result_v4", "analysis_type": "six_scores",
            "item_id": item_id, "status": "error", "dimensions": {}, "error": "Provider unavailable",
            "attempts": [{"attempt": 1, "kind": "api", "error": "Provider unavailable"}]}


@pytest.fixture
def score_run(tmp_path):
    _json(tmp_path / "classifier_spec.json", {
        "schema_version": "caliper_item_context_v1", "analysis_type": "six_scores",
        "rubric_version": "caliper_item_rubric_v1", "benchmark": "test",
        "deployment": "Math tutoring", "deployment_description": "Math tutoring",
        "analysis_basis": "benchmark_assessment", "assessment_status": "complete",
        "dataset_profile": {}, "source_registry": {"deployment.md": "Math tutoring"},
        "source_roles": {"deployment.md": "deployment_requirement"}, "classifiers": dimension_descriptors(),
    })
    _json(tmp_path / "dataset.json", {"benchmark": "test", "item_count": 4})
    _json(tmp_path / "evidence.json", {"scoring": {"dimensions": {"input_form": {"score": 2}}}})
    _records(tmp_path / "items.jsonl", [
        {"item_id": f"item-{index}", "content": "<img src=x onerror=alert(1)>",
         "reference_answer": "=SUM(1,2)", "metadata": {"media": "unavailable.png"}}
        for index in range(4)
    ])
    return tmp_path


def test_scores_unknown_errors_and_pending_are_distinct_and_selection_is_explicit(score_run):
    _json(score_run / "execution.json", {"selected_item_ids": ["item-0", "item-1", "item-2"]})
    _records(score_run / "results.jsonl", [_complete("item-0"), _error("item-1")])
    summary = generate_report(score_run)
    assert summary["analysis_type"] == "six_scores"
    assert summary["total_items"] == 4
    assert summary["completed_items"] == summary["error_items"] == 1
    assert summary["pending_items"] == 2
    assert summary["experiment"]["selected_pending_items"] == 1
    assert summary["experiment"]["completed_item_classifier_judgments"] == 6
    assert summary["experiment"]["expected_primary_requests"] == 3
    assert summary["dimensions"] == summary["classifiers"]
    by_id = {dimension["id"]: dimension for dimension in summary["dimensions"]}
    assert by_id["input_form"]["counts"] == {"1": 0, "2": 0, "3": 0, "4": 1, "5": 0}
    assert by_id["input_form"]["mean_score"] == 4
    assert by_id["input_form"]["known"] == 1
    assert by_id["output_content"]["unknown"] == 1
    assert by_id["output_content"]["mean_score"] is None
    assert by_id["output_content"]["errors"] == by_id["output_content"]["pending"] == 1
    assert summary["original_assessment"]["input_form"]["score"] == 2
    assert not summary["complete_snapshot"]
    with (score_run / "items.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 4
    assert rows[0]["input_form.score"] == "4"
    assert rows[0]["output_content.score"] == "unknown"
    assert rows[1]["output_content.score"] == ""
    assert rows[1]["output_content.status"] == "error"
    assert rows[2]["output_content.status"] == "pending"
    assert rows[3]["selected"] == "false"
    assert rows[0]["reference_answer"] == "'=SUM(1,2)"
    assert "unavailable.png" in rows[0]["item_evidence"]
    report = (score_run / "report.html").read_text()
    assert "Unknown" in report and "Information gaps" in report
    assert "<img src=x" not in report and "&lt;img src=x" in report
    assert "Content-Security-Policy" in report and "<script" not in report
    assert "Based on 1 completed items out of 3 selected items" in report
    assert "<th>Input Form</th><td class='score'>4.00 / 5</td><td>1</td><td>0</td><td>2.00 / 5</td>" in report
    assert "<th>Output Content</th><td class='score'>No numeric scores</td><td>0</td><td>1</td><td>Not supplied</td>" in report
    assert report.index("id='dimension-averages'") < report.index("id='items'")
    assert report.index("id='items'") < report.index("id='original-assessment'")


def test_means_use_each_dimensions_numeric_selected_scores_and_keep_exact_precision(score_run):
    _json(score_run / "execution.json", {"selected_item_ids": ["item-0", "item-1", "item-2"]})
    _records(score_run / "results.jsonl", [
        _complete("item-0", scores={"input_form": 1, "input_ontology": 1, "output_content": 1}),
        _complete("item-1", scores={"input_form": 2, "input_ontology": None, "output_content": 5}),
        _complete("item-2", scores={"input_form": 2, "input_ontology": 5}),
        _complete("item-3", unknown=None, scores={dimension: 5 for dimension in DIMENSIONS}),
    ])
    summary = generate_report(score_run)
    by_id = {dimension["id"]: dimension for dimension in summary["dimensions"]}
    assert len(by_id) == 6
    assert by_id["input_form"]["mean_score"] == 5 / 3
    assert by_id["input_form"]["known"] == 3
    assert by_id["input_ontology"]["mean_score"] == 3
    assert by_id["input_ontology"]["known"] == 2
    assert by_id["input_ontology"]["unknown"] == 1
    assert by_id["output_content"]["mean_score"] == 3
    assert by_id["output_content"]["known"] == 2
    assert by_id["output_content"]["unknown"] == 1
    assert by_id["output_form"]["mean_score"] == 4
    assert summary["experiment"]["selected_completed_items"] == 3
    assert summary["completed_items"] == 4
    assert summary["original_assessment"]["input_form"]["score"] == 2
    persisted = json.loads((score_run / "summary.json").read_text())
    assert persisted["dimensions"] == summary["dimensions"] == persisted["classifiers"]
    assert "1.67 / 5" in (score_run / "report.html").read_text()


def test_all_unknown_scores_have_no_numeric_average(score_run):
    _records(score_run / "results.jsonl", [
        _complete("item-0", scores={dimension: None for dimension in DIMENSIONS}),
    ])
    summary = generate_report(score_run)
    assert all(dimension["mean_score"] is None for dimension in summary["dimensions"])
    assert all(dimension["known"] == 0 and dimension["unknown"] == 1 for dimension in summary["dimensions"])
    assert (score_run / "report.html").read_text().count("No numeric scores") == 6


def test_retry_calls_are_counted_once_from_cumulative_attempts(score_run):
    failed = _error("item-0")
    completed = _complete("item-0", attempts=[*failed["attempts"], {"attempt": 2, "response": "Valid response"}])
    _records(score_run / "results.jsonl", [failed, completed])
    summary = generate_report(score_run)
    assert summary["experiment"]["recorded_api_calls"] == 2
    assert summary["experiment"]["selected_completed_items"] == 1
    assert summary["error_items"] == 0


def test_worksheet_is_blind_preserves_annotations_and_comparison_tracks_unknown(score_run):
    _records(score_run / "results.jsonl", [_complete("item-0")])
    generate_report(score_run)
    with (score_run / "review.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    assert all(rows[0][dimension] == "" for dimension in DIMENSIONS)
    assert "Fits the supplied deployment" not in (score_run / "review.csv").read_text()
    row = rows[0]
    row.update(input_form="3", output_content="unknown")
    row["input_form.justification"] = "Form needs a change"
    row["input_form.evidence"] = "Input field"
    row["output_content.justification"] = "Cannot judge answer"
    row["output_content.information_gaps"] = "No answer"
    with (score_run / "review.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row))
        writer.writeheader()
        writer.writerows(rows)
    saved = (score_run / "review.csv").read_bytes()
    comparison = compare_review(score_run, score_run / "review.csv")
    assert comparison["classifiers"]["input_form"]["mean_absolute_error"] == 1
    assert comparison["classifiers"]["output_content"]["accuracy"] == 1
    assert comparison["classifiers"]["output_content"]["numeric_pairs"] == 0
    assert comparison["classifiers"]["input_content"]["unreviewed"] == 1
    assert (score_run / "review.csv").read_bytes() == saved
    assert generate_report(score_run)["review_comparison_status"]["current"]
    with (score_run / "review.csv").open("a") as stream:
        stream.write("\n")
    assert not generate_report(score_run)["review_comparison_status"]["current"]


def test_six_score_package_contains_actual_prompts_raw_results_and_separate_review(score_run):
    _records(score_run / "results.jsonl", [_complete("item-0")])
    _json(score_run / "run.json", {"request_mode": "per_item", "prompts": {"assess_item": "Frozen item rubric"}})
    (score_run / "requests.jsonl").write_text('{"system":"Frozen item rubric"}\n')
    (score_run / "original_benchmark_report.pdf").write_bytes(b"%PDF-1.4 saved report")
    for name in (".env", "_website_run.json", "access.json"):
        (score_run / name).write_text("PRIVATE_SECRET")
    package = build_results_package(score_run, run_id="score-test", status="checkpoint", scope="pilot",
                                    model={"provider": "test", "api_key": "PRIVATE_SECRET"})
    with ZipFile(package) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        assert manifest["analysis_type"] == "six_scores"
        assert manifest["snapshot_status"] == "pilot-complete"
        assert not manifest["complete_snapshot"]
        assert manifest["selected_item_ids"] == ["item-0"]
        assert archive.read("audit/prompts/assess_item.md") == b"Frozen item rubric"
        assert archive.read("audit/results.jsonl") == (score_run / "results.jsonl").read_bytes()
        assert archive.read("original_benchmark_report.pdf") == b"%PDF-1.4 saved report"
        blank = list(csv.DictReader(io.StringIO(archive.read("review/blank_review.csv").decode())))
        assert blank[0]["input_form"] == blank[0]["output_form.information_gaps"] == ""
        assert "six 1–5" in archive.read("README.txt").decode()
        assert "four classifier" not in archive.read("README.txt").decode()
        assert not any("PRIVATE_SECRET" in archive.read(name).decode(errors="replace") for name in archive.namelist())


def test_context_only_report_defers_selection_and_worksheet(score_run):
    summary = generate_report(score_run)
    assert all(dimension["mean_score"] is None for dimension in summary["dimensions"])
    assert all(dimension["known"] == 0 for dimension in summary["dimensions"])
    assert summary["experiment"]["selected_items"] == 0
    assert summary["experiment"]["expected_primary_requests"] == 0
    assert not (score_run / "review.csv").exists()
    package = build_results_package(score_run, run_id="context-only", status="ready")
    with ZipFile(package) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        assert manifest["selected_item_ids"] == []
        assert "review/blank_review.csv" not in archive.namelist()
        assert "href='review.csv'" not in archive.read("report.html").decode()


def test_report_rejects_invalid_saved_score_instead_of_treating_it_as_unknown(score_run):
    invalid = _complete("item-0")
    invalid["dimensions"]["input_form"]["score"] = True
    _records(score_run / "results.jsonl", [invalid])
    with pytest.raises(ValueError, match="integer"):
        generate_report(score_run)


def test_unknown_human_judgment_requires_gap(score_run):
    _records(score_run / "results.jsonl", [_complete("item-0")])
    generate_report(score_run)
    with (score_run / "review.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    rows[0]["input_content"] = "unknown"
    rows[0]["input_content.justification"] = "Not enough evidence"
    with (score_run / "review.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="information_gaps"):
        compare_review(score_run, score_run / "review.csv")


@pytest.mark.parametrize("execution", [
    {"selected_item_ids": ["item-2", "item-0", "item-1"]},
    {"target_items": 3},
    None,
])
def test_summary_only_defers_exports_without_changing_scores_or_review_selection(score_run, execution):
    if execution is not None:
        _json(score_run / "execution.json", execution)
    _records(score_run / "results.jsonl", [_complete("item-0"), _error("item-1")])
    metadata = {"run_id": "saved-run", "status": "failed", "scope": "pilot"}
    summary = generate_report(score_run, run_metadata=metadata, export_artifacts=False)
    assert summary == json.loads((score_run / "summary.json").read_text())
    assert summary["dimensions"][0]["mean_score"] == 4
    assert summary["review_selection"]["item_ids"] == (
        ["item-0", "item-1", "item-2"] if execution is not None else ["item-0", "item-1"])
    assert json.loads((score_run / "review_selection.json").read_text()) == summary["review_selection"]
    assert not any((score_run / name).exists() for name in ("items.csv", "report.html", "review.csv"))

    exported = generate_report(score_run, run_metadata=metadata)
    assert exported == summary
    assert all((score_run / name).is_file() for name in ("items.csv", "report.html", "review.csv"))
    with (score_run / "review.csv").open() as stream:
        assert [row["item_id"] for row in csv.DictReader(stream)] == summary["review_selection"]["item_ids"]


def test_summary_refresh_preserves_existing_exports_and_human_annotations(score_run):
    _records(score_run / "results.jsonl", [_complete("item-0")])
    generate_report(score_run)
    with (score_run / "review.csv").open("a") as stream:
        stream.write("\nHuman annotation retained\n")
    saved = {name: (score_run / name).read_bytes()
             for name in ("report.html", "items.csv", "review.csv", "review_selection.json")}
    _records(score_run / "results.jsonl", [_complete("item-0"), _complete("item-1", unknown=None)])

    summary = generate_report(score_run, export_artifacts=False)
    assert summary["completed_items"] == 2
    assert summary["review_selection"]["item_ids"] == ["item-0"]
    assert all((score_run / name).read_bytes() == content for name, content in saved.items())


def test_full_export_memory_does_not_grow_with_selected_item_contents(score_run):
    # A multilingual population previously accumulated every selected item and
    # several complete copies of the HTML document in memory. This smaller
    # population exercises the same failure without exhausting the test runner.
    count = 600
    content = "<b>&𐐀" + "a" * 8192
    with (score_run / "items.jsonl").open("w") as stream:
        for index in range(count):
            stream.write(json.dumps({"item_id": f"item-{index}", "content": content}) + "\n")
    _json(score_run / "dataset.json", {"benchmark": "test", "item_count": count})
    _json(score_run / "execution.json", {"selected_item_ids": [f"item-{index}" for index in range(count)]})
    tracemalloc.start()
    try:
        summary = generate_report(score_run)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert peak < 12 * 1024 * 1024, f"Report generation retained {peak / 1024**2:.1f} MiB"
    assert summary["experiment"]["selected_items"] == count
    with (score_run / "items.csv").open() as stream:
        assert sum(1 for _ in csv.DictReader(stream)) == count
    with (score_run / "review.csv").open() as stream:
        assert sum(1 for _ in csv.DictReader(stream)) == count
    report = (score_run / "report.html").read_text()
    assert report.count("Complete item evidence") == count
    assert "item-599" in report and "&lt;b&gt;&amp;𐐀" in report
    assert report.count("<table>") == report.count("</table></div>") == 3
    assert report.endswith("</body></html>")


def test_interrupted_streamed_export_keeps_previous_report(score_run, monkeypatch):
    from item_analysis import score_report

    _records(score_run / "results.jsonl", [_complete("item-0")])
    generate_report(score_run)
    saved = (score_run / "report.html").read_bytes()

    def interrupted(*args):
        yield "New report started"
        raise OSError("Simulated interrupted write")

    monkeypatch.setattr(score_report, "_html_parts", interrupted)
    with pytest.raises(OSError, match="interrupted write"):
        generate_report(score_run)
    assert (score_run / "report.html").read_bytes() == saved
    assert not list(score_run.glob(".report.html-*.tmp"))
