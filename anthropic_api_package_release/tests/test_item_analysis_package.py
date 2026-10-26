"""Offline exports preserve evidence and clearly identify incomplete work."""

import csv
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile

import pytest

from item_analysis.package import build_results_package
from item_analysis.report import generate_report
from test_item_analysis_report import (
    prepared_run, generic_run, _generic_complete, _split_progress,
    _write_jsonl, _read_review, _save_review,
)


def test_partial_package_has_offline_report_exact_artifacts_and_safe_manifest(generic_run):
    _split_progress(generic_run)
    (generic_run / "run.json").write_text(json.dumps({
        "request_mode": "per_classifier", "model_id": "test-model", "provider": "test",
        "prompts": {"input_ontology": "The frozen ontology prompt."},
    }))
    (generic_run / "requests.jsonl").write_text('{"sequence":1,"system":"The exact sent prompt."}\n')
    (generic_run / "website_provenance.json").write_text(json.dumps({
        "generation_system": "Saved generation system", "generation_user_template": "Saved generation template",
    }))
    (generic_run / "usage_ledger.jsonl").write_text('{"sequence":1,"status":"cancelled","usage_known":false}\n')
    for name in ("_website_run.json", ".env", "access.json"):
        (generic_run / name).write_text("PRIVATE_CREDENTIAL_AND_TOKEN")
    package = build_results_package(
        generic_run, run_id="run-42", status="cancelled", scope="pilot",
        created_at="2026-10-26T10:00:00+00:00", updated_at="2026-10-26T10:04:00+00:00",
        model={"model_id": "test-model", "api_key": "PRIVATE_CREDENTIAL_AND_TOKEN"},
    )
    assert package.parent == generic_run / "generated_exports"
    assert "cancelled-partial" in package.name and "run-42" in package.name
    with ZipFile(package) as archive:
        names = set(archive.namelist())
        assert {"report.html", "items.csv", "summary.json", "classifier_spec.json", "review.csv",
                "manifest.json", "README.txt", "original_assessment.json", "audit/evidence.json",
                "review/blank_review.csv", "audit/requests.jsonl", "audit/usage_ledger.jsonl"}.issubset(names)
        assert {name for name in names if "/" not in name} == {
            "report.html", "items.csv", "summary.json", "classifier_spec.json", "review.csv",
            "manifest.json", "README.txt", "original_assessment.json",
        }
        assert names.isdisjoint({"_website_run.json", ".env", "access.json", ".lock"})
        assert not any("PRIVATE_CREDENTIAL_AND_TOKEN" in archive.read(name).decode("utf-8", errors="replace") for name in names)
        manifest = json.loads(archive.read("manifest.json"))
        assert manifest["status"] == "cancelled"
        assert manifest["scope"] == "pilot"
        assert manifest["snapshot_status"] == "cancelled-partial"
        assert manifest["selected_item_ids"] == [f"item-{index}" for index in range(4)]
        assert manifest["created_at"] == "2026-10-26T10:00:00+00:00"
        assert manifest["counts"]["completed_item_classifier_judgments"] == 7
        assert manifest["counts"]["error_item_classifier_judgments"] == 1
        assert manifest["counts"]["pending_item_classifier_judgments"] == 8
        assert manifest["model"] == {"request_mode": "per_classifier", "model_id": "test-model", "provider": "test"}
        assert manifest["usage"] is None
        for entry in manifest["artifacts"]:
            content = archive.read(entry["path"])
            assert entry["sha256"] == hashlib.sha256(content).hexdigest()
            assert entry["bytes"] == len(content)
        for name in ("results.jsonl", "requests.jsonl", "usage_ledger.jsonl"):
            assert archive.read(f"audit/{name}") == (generic_run / name).read_bytes()
        assert archive.read("audit/prompts/classify_input_ontology.md") == b"The frozen ontology prompt."
        assert archive.read("audit/prompts/generation_user_template.md") == b"Saved generation template"
        original = json.loads(archive.read("original_assessment.json"))
        assert original["scoring"]["dimensions"]["input_form"]["score"] == 2
        report = archive.read("report.html").decode()
        assert "Stopped — saved results retained" in report
        assert report.index("id='item-statistics'") < report.index("id='original-assessment'")
        assert "Original assessment: six benchmark dimensions" in report
        assert "Category match" in report and "<code>match</code>" in report
        assert "href='items.csv'" in report and "href='summary.json'" in report
        assert "<script" not in report and "<link" not in report
        assert "Content-Security-Policy" in report
        assert "<div class='table-scroll'" in report
        assert "<details><summary>Fixed decision rules and sourced context" in report
        assert "<details><summary>Item examples and evidence" in report
        assert "{'decision_rules'" not in report


def test_existing_human_annotations_stay_exact_and_blank_review_is_independent(generic_run):
    _write_jsonl(generic_run / "results.jsonl", [_generic_complete("item-0")])
    generate_report(generic_run)
    rows = _read_review(generic_run)
    rows[0]["input_content"] = "issue_identified"
    rows[0]["input_content.justification"] = "PRIVATE REVIEWER OPINION"
    rows[0]["review_notes"] = "Reviewer's independent note"
    _save_review(generic_run, rows)
    saved = (generic_run / "review.csv").read_bytes()
    package = build_results_package(generic_run, run_id="review-run", status="failed")
    assert (generic_run / "review.csv").read_bytes() == saved
    with ZipFile(package) as archive:
        assert archive.read("review.csv") == saved
        blank = archive.read("review/blank_review.csv").decode()
        assert "PRIVATE REVIEWER OPINION" not in blank
        records = list(csv.DictReader(io.StringIO(blank)))
        assert records[0]["input_content"] == records[0]["review_notes"] == ""
        assert records[0]["content"] == "<img src=x onerror=alert(1)>"
        report = archive.read("report.html").decode()
        assert "<img src=x" not in report and "&lt;img src=x" in report
        assert "separately named copy" in archive.read("README.txt").decode()


def test_specification_only_package_marks_missing_logs_without_inventing_results(generic_run):
    package = build_results_package(generic_run, run_id="spec-only", status="ready")
    with ZipFile(package) as archive:
        names = set(archive.namelist())
        assert "audit/results.jsonl" not in names and "review.csv" not in names
        assert "review/blank_review.csv" not in names
        manifest = json.loads(archive.read("manifest.json"))
        assert manifest["snapshot_status"] == "specification-only"
        assert manifest["selected_item_ids"] == []
        assert manifest["created_at"] is None
        assert manifest["model"] is None and manifest["usage"] is None
        assert "audit/results.jsonl" in {entry["path"] for entry in manifest["missing_artifacts"]}
        assert "Specification prepared — classification not started" in archive.read("report.html").decode()
        assert "href='review.csv'" not in archive.read("report.html").decode()


def test_completed_pilot_is_distinct_from_full_snapshot_completion(generic_run):
    items = [{"item_id": f"item-{index}", "content": "Question"} for index in range(10)]
    _write_jsonl(generic_run / "items.jsonl", items)
    _write_jsonl(generic_run / "results.jsonl", [_generic_complete("item-0"), _generic_complete("item-1")])
    (generic_run / "execution.json").write_text(json.dumps({"selected_item_ids": ["item-0", "item-1"]}))
    package = build_results_package(generic_run, run_id="pilot", status="checkpoint", scope="pilot")
    with ZipFile(package) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        assert manifest["snapshot_status"] == "pilot-complete"
        assert not manifest["complete_snapshot"]
        assert manifest["counts"]["selected_completed_items"] == 2
        assert "Selected sample complete" in archive.read("report.html").decode()


def test_package_rejects_symlink_artifacts_and_external_pdf(generic_run, tmp_path_factory):
    external = tmp_path_factory.mktemp("private") / "secret.json"
    external.write_text("PRIVATE")
    (generic_run / "usage.json").symlink_to(external)
    with pytest.raises(ValueError, match="symlink"):
        build_results_package(generic_run, run_id="unsafe", status="ready")
    (generic_run / "usage.json").unlink()
    with pytest.raises(ValueError, match="frozen"):
        build_results_package(generic_run, run_id="unsafe", status="ready", assessment_pdf=external)
    assert not (generic_run / "generated_exports").exists()


def test_frozen_original_pdf_is_included_as_an_exact_artifact(generic_run):
    pdf = generic_run / "original_benchmark_report.pdf"
    pdf.write_bytes(b"%PDF-1.4\nA saved original assessment PDF")
    package = build_results_package(generic_run, run_id="pdf", status="ready", assessment_pdf=pdf)
    with ZipFile(package) as archive:
        assert archive.read("original_benchmark_report.pdf") == pdf.read_bytes()
        assert "href='original_benchmark_report.pdf'" in archive.read("report.html").decode()


def test_manifest_retains_usage_coverage_when_public_usage_has_only_token_totals(generic_run):
    (generic_run / "usage.json").write_text(json.dumps({
        "input_tokens": 20, "output_tokens": 5, "calls": 2,
        "calls_with_usage": 1, "calls_without_usage": 1,
    }))
    package = build_results_package(generic_run, run_id="usage", status="failed",
                                    usage={"input_tokens": 20, "output_tokens": 5})
    with ZipFile(package) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        assert manifest["usage"]["calls"] == 2
        assert manifest["usage"]["calls_without_usage"] == 1
        assert "unknown provider usage" in manifest["usage_note"]
