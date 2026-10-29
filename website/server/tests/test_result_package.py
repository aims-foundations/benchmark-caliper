"""Review exports preserve evidence and stay usable without the running app."""

from copy import deepcopy
import csv
from html import unescape
from html.parser import HTMLParser
from io import StringIO
import json
import re
from zipfile import ZipFile

import pytest

from bayesian_auditing.benchmark_data import row_fingerprint
from website.server.candidate_store import CandidateStore, has_ref
from website.server import result_package


def supported(text):
    return {"text": text, "evidence": [{"answer_id": "task", "quote": "Help triage patients"}]}


def finding(score=None):
    result = {"justification": "This question requires the supplied patient evidence.",
              "evidence": ["Chest pain for three hours"], "information_gaps": []}
    if score is not None:
        result["score"] = score
    return result


@pytest.fixture
def snapshot():
    original = {"question": "Chest pain for three hours: what is the next action?", "answer": "Urgent assessment",
                "metadata": {"tags": ["emergency", None], "weight": 1.25}, "enabled": False,
                "json_cell": '{ "preserve": "spacing" }'}
    item = {"item_id": "item-b", "status": "complete", "question_text": original["question"],
            "search_text": "Full search row", "evidence": {"item": original}, "evidence_hash": "item-b",
            "sources": [{"repo": "aims-foundations/measurement-db", "benchmark": "triage",
                         "commit": "abc123", "path": "triage/items.parquet", "row": 17}],
            "gate": {"status": "pass", "reasons": ["All four gated dimensions pass."]},
            "assessment": {"task": {**finding(), "status": "matched", "decision": "Choose the next action",
                                     "matched_facet_ids": ["triage"]},
                           "ratings": {key: finding(index % 5 + 1) for index, (key, _) in enumerate(result_package.DIMENSIONS)},
                           "coverage": [{**finding(), "requirement_index": 0, "satisfied": True}]}}
    other = deepcopy(item)
    other.update(item_id="not-selected", question_text="UNSELECTED SENTINEL", evidence={"item": {"question": "UNSELECTED SENTINEL"}})
    return {
        "run_id": "final-run-123", "source_run_id": "source-run", "selection_run_id": "final-run-123",
        "mode": "adaptive", "status": "completed", "message": "Collection frozen with coverage gaps.",
        "model": "gpt-6-luna", "reasoning_effort": "medium",
        "metadata": {"export_version": 1, "run_name": "Chest pain triage", "created_at": "2026-10-26T12:00:00Z",
                     "finished_at": "2026-10-26T12:04:00Z", "exported_at": "2026-10-26T12:05:00Z",
                     "result_state": "frozen", "usage_scope": "current_run"},
        "deployment": {key: f"Original answer {index}: Help triage patients" for index, (key, _) in enumerate(result_package.ANSWERS)},
        "requirements": {**{key: supported(key) for key in ("workflow", "primary_user", "input_types", "output_types", "authority")},
                         "task_facets": [{"facet_id": key, "task": supported(description), "essential": True,
                                          "required_input_evidence": supported("Patient symptoms"),
                                          "required_output_behavior": supported("Next action")}
                                         for key, description in (("triage", "Triage urgency"), ("followup", "Plan follow-up"))],
                         "coverage_requirements": [{"requirement": supported("Include at least two emergency cases"),
                                                    "minimum_items": 2, "facet_ids": ["triage"]},
                                                   {"requirement": supported("Include age diversity"),
                                                    "minimum_items": None, "facet_ids": []}],
                         "unresolved_details": ["Age range is unspecified."]},
        "extraction": {"prompt": "Original extraction prompt", "output_schema": {"type": "object"}},
        "grounding": {"adopted": [{"record_id": "onet-1", "passage": "Assess patient symptoms", "applicability": "direct"}]},
        "retrieval": {"scope": {"commit": "abc123"}, "queries": [{"query": "triage"}], "policy": {"version": 3},
                      "rankings": [{"facet_id": "triage", "candidates": [other, item]}],
                      "queues": [{"item_ids": ["not-selected", "item-b"]}]},
        "screening": {"allocation": {"budget": 48, "allocated": 2, "items": [{"item_id": "item-b"}]},
                      "items": [other, item], "model": {"prompt": "Original screening prompt"}, "policy": {"version": 1}},
        "selection": {"selected_item_ids": ["item-b"], "items": [{"item_id": "item-b", "quality_score": 4.25,
                                                                  "matched_facet_ids": ["triage"]}],
                      "selected_count": 1, "eligible_count": 2, "limit": 30, "fully_satisfied": False, "total_quality": 4.25,
                      "gaps": ["Task followup has no selected item."], "unresolved_requirement_indices": [1],
                      "task_coverage": [{"facet_id": "triage", "minimum": 1, "eligible_count": 2, "selected_count": 1, "shortfall": 0},
                                        {"facet_id": "followup", "minimum": 1, "eligible_count": 0, "selected_count": 0, "shortfall": 1}],
                      "quota_coverage": [{"requirement_index": 0, "minimum_items": 2, "eligible_count": 2, "selected_count": 1, "shortfall": 1},
                                         {"requirement_index": 1, "minimum_items": None, "eligible_count": 0, "selected_count": 0, "shortfall": None}]},
        "adaptive": {"frozen": True, "stop_reason": "queues_exhausted", "settings": {"candidate_limit": 160},
                     "batches": [{"number": 0, "kind": "initial", "status": "committed", "item_ids": ["item-b"],
                                  "selected_item_ids": ["item-b"], "outcomes": [{"item_id": "item-b", "retained": True}]},
                                 {"number": 1, "kind": "adaptive", "status": "committed", "facet_id": "followup",
                                  "item_ids": ["item-a"], "outcomes": [], "selected_item_ids": ["item-b"], "unresolved_item_ids": ["item-a"]}],
                     "queue_statistics": [{"facet_id": "triage", "yield": 0.5}], "attempts": [],
                     "cost": {"spent_usd": 0.01, "reserved_usd": 0, "unknown_attempts": 1}},
        "usage": {"input_tokens": 10, "output_tokens": 2, "total_tokens": 12},
        "stage_usage": [{"run_id": "first-stage", "mode": "requirements", "status": "completed",
                         "usage": {"input_tokens": 100, "output_tokens": 10, "total_tokens": 110}},
                        {"run_id": "final-run-123", "mode": "adaptive", "status": "completed",
                         "usage": {"input_tokens": 10, "output_tokens": 2, "total_tokens": 12}}],
    }


def read_package(snapshot, *, expand=None):
    with result_package.build_results_package(snapshot, expand=expand) as file:
        assert file.tell() == 0
        assert file.seekable()
        with ZipFile(file) as archive:
            assert archive.namelist() == ["report.html", "selected_items.csv", "results.json"]
            assert archive.testzip() is None
            html = archive.read("report.html").decode("utf-8")
            csv_text = archive.read("selected_items.csv").decode("utf-8-sig")
            original = json.loads(archive.read("results.json"))
    return html, list(csv.DictReader(StringIO(csv_text))), original


def test_frozen_collection_has_descriptive_gaps_evidence_and_history(snapshot):
    html, rows, original = read_package(snapshot)
    assert "Collection frozen" in html
    assert "Coverage remains incomplete." in html
    assert "Plan follow-up" in html
    assert "Include at least two emergency cases" in html
    assert "Include age diversity" in html and "Unresolved" in html
    assert "Task followup has no selected item." in html
    assert "No unseen candidates remain" in html
    assert "1 newly screened items retained" in html
    assert "Adaptive batch 1" in html
    assert "1 acquired candidates lack valid assessments" in html
    assert "Step 7 calls and retries only" in html
    assert "Top-level token usage covers the current run only" in html
    assert "first-stage" in html and "Complete recorded stage usage" in html
    for index in range(6):
        assert f"Original answer {index}" in html
    for _, label in result_package.DIMENSIONS:
        assert label in html
    assert "This question requires the supplied patient evidence." in html
    assert "Chest pain for three hours" in html and "abc123" in html and "triage/items.parquet" in html
    assert rows[0]["matched_tasks"] == "Triage urgency"
    assert original == snapshot


def test_join_selected_ids_preserves_order_and_all_raw_json_without_mutation(snapshot):
    snapshot["selection"]["selected_item_ids"] = ["item-b", "not-selected"]
    snapshot["selection"]["items"].insert(0, {"item_id": "not-selected", "quality_score": 3})
    before = deepcopy(snapshot)
    html, rows, original = read_package(snapshot)
    assert [row["item_id"] for row in rows] == ["item-b", "not-selected"]
    assert rows[0]["question_preview"].startswith("Chest pain")
    assert rows[1]["question_preview"] == "UNSELECTED SENTINEL"
    assert rows[0]["quality_score"] == "4.25"
    assert [rows[0][key] for key, _ in result_package.DIMENSIONS] == ["1", "2", "3", "4", "5", "1"]
    assert "Complete original item row" in html
    assert "preserve" in html
    assert snapshot == before == original


def test_screening_support_is_labeled_as_model_provided_and_preserved_as_safe_text(snapshot):
    item = snapshot["screening"]["items"][1]
    passage = '<img src=x onerror=alert(1)>\nTwo  spaces and altered wording.'
    for finding in (item["assessment"]["task"], item["assessment"]["ratings"]["input_content"],
                    item["assessment"]["coverage"][0]):
        finding["evidence"] = [passage]
    before = deepcopy(snapshot)

    html, rows, original = read_package(snapshot)

    assert html.count("<h5>Model-provided item evidence</h5>") == 8
    assert '<li class="preserve">&lt;img src=x onerror=alert(1)&gt;\nTwo  spaces and altered wording.</li>' in html
    assert "<img" not in html
    assert "<blockquote>&lt;img" not in html
    assert "<blockquote>Help triage patients" in html  # Step 2 still cites literal answer excerpts.
    assert rows[0]["screening_gate"] == "pass"
    assert rows[0]["input_content"] == str(item["assessment"]["ratings"]["input_content"]["score"])
    assert original == before == snapshot


def test_unselected_rows_stay_in_json_but_not_selected_report_or_csv(snapshot):
    html, rows, original = read_package(snapshot)
    assert "UNSELECTED SENTINEL" not in html
    assert len(rows) == 1
    assert original["retrieval"]["rankings"][0]["candidates"][0]["question_text"] == "UNSELECTED SENTINEL"


def test_stored_candidates_export_complete_original_fields_and_per_occurrence_metadata(snapshot, tmp_path):
    snapshot["screening"]["items"][1]["evidence"]["item"]["_candidate_ref"] = "original source column"
    # Assign the real row identities required by the evidence store, including
    # every selection/queue reference to these fixture candidates.
    identifiers = {item["item_id"]: row_fingerprint(item["evidence"]["item"])
                   for item in snapshot["screening"]["items"]}

    def identify(value):
        if isinstance(value, dict):
            result = {key: identify(nested) for key, nested in value.items()}
            if "evidence" in result and "item_id" in result:
                result["evidence_hash"] = result["item_id"]
            return result
        if isinstance(value, list):
            return [identify(nested) for nested in value]
        return identifiers.get(value, value) if isinstance(value, str) else value

    original = identify(snapshot)
    retrieved = original["retrieval"]["rankings"][0]["candidates"][1]
    retrieved["rank"] = 3
    second_query = {**deepcopy(retrieved), "rank": 7, "scores": {"dense": 0.8, "keyword": 1.3}}
    original["retrieval"]["rankings"].append({"facet_id": "followup", "candidates": [second_query]})
    screened = original["screening"]["items"][1]
    screened.update(rank=19, screened_run_id="screen-run", acquisition={"queue_id": "triage-all", "facet_id": "triage"})
    expected_html, expected_csv, _ = read_package(original)

    store = CandidateStore(tmp_path / "private-review-runs" / "candidates")
    compact = deepcopy(original)
    for ranking in compact["retrieval"]["rankings"]:
        ranking["candidates"] = [store.compact(item) for item in ranking["candidates"]]
    compact["screening"]["items"] = [store.compact(item) for item in compact["screening"]["items"]]
    before = deepcopy(compact)
    expanded_ids = []

    def expand(record):
        if has_ref(record):
            expanded_ids.append(record["item_id"])
        return store.expand(record)

    html, rows, exported = read_package(compact, expand=expand)
    assert exported == original
    # The store's canonical JSON changes object-key order, which has no effect
    # on the contents of the original row shown in the report's evidence view.
    def normalize_json_views(report):
        return re.sub(r"<pre>(.*?)</pre>", lambda match: json.dumps(json.loads(unescape(match[1])), sort_keys=True),
                      report, flags=re.S)

    assert normalize_json_views(html) == normalize_json_views(expected_html)
    assert rows == expected_csv
    assert compact == before
    # HTML and CSV read only the selected record. Full JSON subsequently reads
    # each ranking/screening occurrence, preserving its distinct rank metadata.
    assert expanded_ids[:2] == [screened["item_id"], screened["item_id"]]
    assert len(expanded_ids) == 7
    assert [ranking["candidates"][-1]["rank"] for ranking in exported["retrieval"]["rankings"]] == [3, 7]
    assert exported["screening"]["items"][1]["rank"] == 19
    serialized = html + json.dumps(rows) + json.dumps(exported)
    assert exported["screening"]["items"][1]["evidence"]["item"]["_candidate_ref"] == "original source column"
    assert compact["screening"]["items"][1]["_candidate_ref"] not in serialized
    assert "private-review-runs" not in serialized
    assert "UNSELECTED SENTINEL" not in html


@pytest.mark.parametrize("mode", ["requirements", "grounding", "retrieval", "screening", "selection", "adaptive"])
def test_early_or_interrupted_stage_exports_are_explicitly_partial(snapshot, mode):
    minimal = {key: snapshot[key] for key in ("run_id", "deployment", "metadata", "usage")}
    minimal.update(mode=mode, status="running", requirements=None, selection=None)
    minimal["metadata"]["result_state"] = "partial"
    html, rows, original = read_package(minimal)
    assert "Partial result — the current stage is unfinished." in html
    assert "No benchmark collection has been selected" in html
    assert "No validated requirements are available" in html
    assert len(rows) == 0
    assert original == minimal
    assert result_package.package_filename(minimal).endswith("-partial.zip")


def test_stage_completion_does_not_claim_frozen_or_validated_benchmark(snapshot):
    snapshot.update(mode="selection", adaptive=None)
    snapshot["metadata"]["result_state"] = "stage_complete"
    html, _, _ = read_package(snapshot)
    assert "This stage is complete." in html
    assert "has not produced a frozen collection" in html
    assert "Target-system performance and separate human validation are not included." in html
    assert not result_package.package_filename(snapshot).endswith("-partial.zip")


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def test_html_escapes_all_untrusted_fields_and_never_loads_external_assets(snapshot):
    attack = '</pre><script src="https://bad.invalid/a.js">alert(1)</script><img src=x onerror=alert(2)>'

    def poison(value):
        if isinstance(value, dict):
            return {key: poison(item) if key not in {"item_id", "facet_id", "result_state", "mode"} else item for key, item in value.items()}
        if isinstance(value, list):
            return [poison(item) for item in value]
        return value + attack if isinstance(value, str) else value

    malicious = poison(snapshot)
    html, _, original = read_package(malicious)
    parser = Tags()
    parser.feed(html)
    assert not {tag for tag, _ in parser.tags} & {"script", "img", "iframe", "object", "link", "form", "base"}
    assert all(not name.startswith("on") and name not in {"src", "href"} for _, attrs in parser.tags for name in attrs)
    assert "&lt;script" in html
    assert "Content-Security-Policy" in html
    assert "@media print" in html
    assert original == malicious


@pytest.mark.parametrize("value", ["=1+2", "+SUM(1,2)", "-1+2", "@SUM(A1)", "  =1+2", "\tplain", "\rplain", "\nplain"])
def test_csv_formula_guard_does_not_change_evidence(snapshot, value):
    item = snapshot["screening"]["items"][1]
    item["question_text"] = value
    item["evidence"]["item"]["question"] = value
    snapshot["requirements"]["task_facets"][0]["task"]["text"] = value
    _, rows, original = read_package(snapshot)
    assert rows[0]["question_preview"] == "'" + value
    assert rows[0]["matched_tasks"] == "'" + value
    assert original["screening"]["items"][1]["evidence"]["item"]["question"] == value


def test_csv_unicode_quoting_preview_and_unknown_scores_preserve_full_source(snapshot):
    value = '症状, "chest pain"\n' + "x" * 1100
    item = snapshot["screening"]["items"][1]
    item["question_text"] = value
    item["assessment"]["ratings"]["output_form"]["score"] = None
    html, rows, original = read_package(snapshot)
    assert rows[0]["question_preview"] == value[:1000] + "…"
    assert rows[0]["output_form"] == ""
    assert rows[0]["reviewer_notes"] == ""
    assert "症状" in html
    assert original["screening"]["items"][1]["question_text"] == value


def test_filename_is_safe_bounded_descriptive_and_distinguishes_runs(snapshot):
    assert result_package.package_filename(snapshot) == "chest-pain-triage_2026-10-26_final-run-12.zip"
    snapshot["metadata"]["run_name"] = '../../CON\r\nInjected: "héllo" ' * 100
    snapshot["run_id"] = "../../../dangerous\r\nvalue"
    filename = result_package.package_filename(snapshot)
    assert re.fullmatch(r"[a-z0-9_-]+\.zip", filename)
    assert len(filename) < 110
    assert "2026-10-26" in filename
    snapshot["metadata"]["run_name"] = "全中文"
    assert result_package.package_filename(snapshot).startswith("benchmark-results_")


def test_missing_selected_evidence_is_reported_instead_of_using_a_different_row(snapshot):
    snapshot["screening"]["items"].pop()
    html, rows, _ = read_package(snapshot)
    assert "saved screening evidence for this item is unavailable" in html
    assert rows[0]["item_id"] == "item-b"
    assert rows[0]["question_preview"] == "No item text is recorded."
    assert "UNSELECTED SENTINEL" not in html


def test_failure_closes_temporary_file_and_never_returns_partial_package(snapshot, monkeypatch):
    opened = []
    factory = result_package.SpooledTemporaryFile

    def remember(**kwargs):
        file = factory(**kwargs)
        opened.append(file)
        return file

    monkeypatch.setattr(result_package, "SpooledTemporaryFile", remember)
    snapshot["unserializable"] = object()
    with pytest.raises(TypeError):
        result_package.build_results_package(snapshot)
    assert len(opened) == 1 and opened[0].closed
