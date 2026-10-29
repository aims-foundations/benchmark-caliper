"""Composition describes the selected rows without reclassifying their evidence."""

from copy import deepcopy
from html.parser import HTMLParser

import pytest

from website.server.construction_composition import render_html, summarize


@pytest.fixture
def snapshot():
    return {
        "requirements": {
            "task_facets": [{"facet_id": key, "task": {"text": label}} for key, label in (
                ("diagnosis", "Choose a diagnosis"), ("management", "Choose initial management"),
                ("investigation", "Choose an investigation"))],
            "coverage_requirements": [{"requirement": {"text": "Include medication constraints"}}],
        },
        "selection": {
            "selected_item_ids": ["a", "b", "c", "missing"],
            "items": [{"item_id": "a", "matched_facet_ids": ["diagnosis", "management", "management"]},
                      {"item_id": "missing", "matched_facet_ids": []}],
            "quota_coverage": [{"requirement_index": 0, "minimum_items": 3, "selected_count": 0, "shortfall": 3}],
        },
        "screening": {"items": [
            {"item_id": "not-selected", "question_text": "Question one? A", "sources": [{"benchmark": "excluded"}],
             "assessment": {"task": {"matched_facet_ids": ["investigation"]}}},
            {"item_id": "b", "question_text": "Question one?   A", "sources": [{"benchmark": "source_x"}],
             "assessment": {"task": {"matched_facet_ids": ["diagnosis"]}}},
            {"item_id": "a", "question_text": "  Question  one?\n A ", "sources": [
                {"benchmark": "source_x", "row": 1}, {"benchmark": "source_x", "row": 2}, {"benchmark": "source_y"}],
             "assessment": {"task": {"matched_facet_ids": ["investigation"]}}},
            {"item_id": "c", "question_text": "question one? A", "sources": [{"benchmark": "source_z"}],
             "assessment": {"task": {"matched_facet_ids": ["management"]}}},
        ]},
    }


def test_selected_counts_deduplicate_provenance_and_preserve_overlapping_task_matches(snapshot):
    before = deepcopy(snapshot)
    composition = summarize(snapshot)
    assert composition["selected_count"] == 4
    assert composition["sources"] == [
        {"name": "source_x", "count": 2, "percentage": 50},
        {"name": "source_y", "count": 1, "percentage": 25},
        {"name": "source_z", "count": 1, "percentage": 25},
    ]
    assert composition["unknown_source_count"] == 1
    assert composition["tasks"] == [
        {"facet_id": "diagnosis", "label": "Choose a diagnosis", "count": 2},
        {"facet_id": "management", "label": "Choose initial management", "count": 2},
        {"facet_id": "investigation", "label": "Choose an investigation", "count": 0},
    ]
    assert composition["coverage"] == [{"requirement_index": 0, "label": "Include medication constraints",
                                       "minimum_items": 3, "selected_count": 0, "shortfall": 3}]
    assert snapshot == before


def test_overlap_normalizes_only_whitespace_and_excludes_missing_and_unselected_questions(snapshot):
    assert summarize(snapshot)["question_text"] == {
        "available_count": 3, "distinct_count": 2, "missing_count": 1,
        "overlaps": [{"item_ids": ["a", "b"]}],
    }
    snapshot["screening"]["items"].append({"item_id": "missing", "question_text": " \t\n ",
                                             "search_text": "Question one? A", "evidence": {"item": {"question": "Question one? A"}}})
    assert summarize(snapshot)["question_text"]["missing_count"] == 1


def test_reviewed_formats_are_explicit_and_can_cover_only_part_of_the_selection(snapshot):
    annotations = {"version": 1, "formats": [{"label": "Text multiple choice", "item_ids": ["a", "b", "c"]}],
                   "basis": "Description based on inspection of the saved question text."}
    before = deepcopy(annotations)
    assert summarize(snapshot)["formats"] == {"counts": [], "unknown_count": 4, "basis": None}
    assert summarize(snapshot, annotations)["formats"] == {
        "counts": [{"label": "Text multiple choice", "count": 3}], "unknown_count": 1, "basis": annotations["basis"]}
    assert annotations == before


@pytest.mark.parametrize("annotations", [
    {}, {"version": True, "formats": [], "basis": "Review"},
    {"version": 2, "formats": [], "basis": "Review"},
    {"version": 1, "formats": [], "basis": " "},
    {"version": 1, "formats": [{"label": " ", "item_ids": ["a"]}], "basis": "Review"},
    {"version": 1, "formats": [{"label": "Text", "item_ids": "a"}], "basis": "Review"},
    {"version": 1, "formats": [{"label": "Text", "item_ids": ["not-selected"]}], "basis": "Review"},
    {"version": 1, "formats": [{"label": "Text", "item_ids": ["a", "a"]}], "basis": "Review"},
    {"version": 1, "formats": [{"label": "Text", "item_ids": ["a"]}, {"label": "Other", "item_ids": ["a"]}], "basis": "Review"},
])
def test_invalid_format_annotations_are_rejected(snapshot, annotations):
    with pytest.raises(ValueError):
        summarize(snapshot, annotations)


def test_unknown_sources_and_unresolved_quotas_are_visible(snapshot):
    snapshot["screening"]["items"] = []
    snapshot["selection"]["quota_coverage"].append({"requirement_index": 1, "minimum_items": None,
                                                   "selected_count": 0, "shortfall": None})
    composition = summarize(snapshot)
    html = render_html(composition)
    assert "Source information is unavailable for 4 selected items." in html
    assert "Question text is unavailable for 4 selected items" in html
    assert "Coverage requirement 2" in html and "Unresolved" in html
    assert "Question format has not been reviewed for 4 selected items." in html


def test_empty_or_early_stage_has_no_misleading_composition():
    composition = summarize({})
    assert composition["selected_count"] == 0
    assert composition["sources"] == []
    assert composition["question_text"] == {"available_count": 0, "distinct_count": 0, "missing_count": 0, "overlaps": []}
    assert "No selected items are available" in render_html(composition)


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def test_html_escapes_data_and_provides_only_local_item_links(snapshot):
    attack = '<img src=x onerror="alert(1)">'
    snapshot["requirements"]["task_facets"][0]["task"]["text"] = attack
    snapshot["requirements"]["coverage_requirements"][0]["requirement"]["text"] = attack
    snapshot["screening"]["items"][1]["sources"][0]["benchmark"] = attack
    composition = summarize(snapshot, {"version": 1, "formats": [{"label": attack, "item_ids": ["a"]}], "basis": attack})
    html = render_html(composition)
    tags = Tags()
    tags.feed(html)
    assert not {tag for tag, _ in tags.tags} & {"script", "img", "iframe", "form"}
    assert all(not attr.startswith("on") for _, attrs in tags.tags for attr in attrs)
    assert [attrs["href"] for tag, attrs in tags.tags if tag == "a"] == ["#selected-item-a", "#selected-item-b"]
    assert "&lt;img" in html
    assert "shares can add up to more than 100%" in html
    assert "They remain separate under the existing whole row identity rule." in html
    assert "·" not in html and "—" not in html
