"""Screening contracts with mocked model responses, not live quality evaluation."""

import asyncio
from copy import deepcopy
import json

import httpx
from openai import AsyncOpenAI, OpenAI
from pydantic import ValidationError
import pytest

from bayesian_auditing.requirements import Requirements
from bayesian_auditing.screening import (
    AsyncItemScreener, GATED_DIMENSIONS, ItemScreener, PROMPT_PATH,
    SCREENING_VERSION, ScreeningAssessment, gate_for,
)
from bayesian_auditing.scoring import DIMENSIONS


QUESTION = "Which initial management is indicated?"
CONSTRAINT = "Drug A is contraindicated because of the stated allergy."
SCORER = "Accept B or Drug B after trimming whitespace."


def supported(text, answer):
    return {"text": text, "evidence": [{"answer_id": answer, "quote": text}]}


@pytest.fixture
def answers():
    return {
        "task": "  Answer educational clinical questions.\n",
        "users": "English-speaking students.",
        "inputs": "Self-contained English text cases with visible options.",
        "outputs": "One supplied option identifier or a concise answer.",
        "success": "Choose management, diagnosis, or investigation. Include three management cases where an allergy changes the choice. Include one English case.",
        "constraints": "Educational practice only.",
    }


@pytest.fixture
def requirements(answers):
    return Requirements.model_validate({
        "workflow": supported(answers["task"], "task"),
        "primary_user": supported(answers["users"], "users"),
        "input_types": supported(answers["inputs"], "inputs"),
        "output_types": supported(answers["outputs"], "outputs"),
        "authority": supported(answers["constraints"], "constraints"),
        "task_facets": [{
            "facet_id": identifier, "task": supported(task, "success"),
            "required_input_evidence": supported(answers["inputs"], "inputs"),
            "required_output_behavior": supported(answers["outputs"], "outputs"),
            "essential": essential,
        } for identifier, task, essential in (("initial_management", "management", True),
                                              ("diagnosis", "diagnosis", False),
                                              ("investigation", "investigation", None))],
        "coverage_requirements": [
            {"facet_ids": ["initial_management"], "minimum_items": 3,
             "requirement": supported("Include three management cases where an allergy changes the choice.", "success")},
            {"facet_ids": [], "minimum_items": 1,
             "requirement": supported("Include one English case.", "success")},
        ],
        "unresolved_details": [],
    })


@pytest.fixture
def item_row():
    return {
        "item_id": "original-question-17", "benchmark_id": "synthetic-review-example",
        "content": {"case": CONSTRAINT, "question": QUESTION, "options": ["A. Drug A", "B. Drug B"]},
        "reference_answer": "B", "grading_criterion": {"rule": SCORER},
        "verifier": None, "arbitrary_column": "Preserve every original field.",
    }


def rating(score=4, quote=QUESTION):
    return {"score": score, "evidence": [quote] if quote else [],
            "justification": "The supplied evidence supports the stated finding.",
            "information_gaps": ["The needed evidence is unavailable."] if score is None else []}


@pytest.fixture
def assessment():
    return {
        "task": {"status": "matched", "decision": "Choose the indicated initial management.",
                 "matched_facet_ids": ["initial_management"], "evidence": [QUESTION],
                 "justification": "The question directly requests a management decision.", "information_gaps": []},
        "ratings": {name: rating(None if name == "output_content" else 4,
                                 SCORER if name in {"output_ontology", "output_form"} else QUESTION)
                    for name in DIMENSIONS},
        "coverage": [
            {"requirement_index": 0, "satisfied": True, "evidence": [CONSTRAINT],
             "justification": "The stated contraindication changes the available management choice.", "information_gaps": []},
            {"requirement_index": 1, "satisfied": True, "evidence": [QUESTION],
             "justification": "The question is supplied in English.", "information_gaps": []},
        ],
    }


def response_body(assessment, mode="complete"):
    content = [{"type": "output_text", "text": json.dumps(assessment), "annotations": []}]
    if mode in {"refusal", "mixed_refusal"}:
        refusal = {"type": "refusal", "refusal": "private-provider-diagnostic"}
        content = [refusal] if mode == "refusal" else [*content, refusal]
    elif mode == "malformed":
        content[0]["text"] = "private-provider-diagnostic: not JSON"
    return {"id": "resp_screen", "object": "response", "created_at": 1, "model": "gpt-6-luna",
            "status": "incomplete" if mode == "incomplete" else "completed",
            "incomplete_details": {"reason": "max_output_tokens"} if mode == "incomplete" else None,
            "output": [{"type": "message", "id": "msg_screen", "status": "completed", "role": "assistant", "content": content}],
            "usage": {"input_tokens": 100, "output_tokens": 90, "total_tokens": 190,
                      "input_tokens_details": {"cached_tokens": 10}, "output_tokens_details": {"reasoning_tokens": 30}}}


@pytest.mark.parametrize("async_mode", [False, True])
@pytest.mark.parametrize("mode", ["complete", "fabricated_quote", "unknown_facet", "missing_coverage",
                                 "malformed", "incomplete", "refusal", "mixed_refusal"])
def test_real_sdk_contract_preserves_input_and_sanitizes_errors(answers, requirements, item_row, assessment, async_mode, mode):
    if mode == "fabricated_quote":
        assessment["ratings"]["input_form"]["evidence"] = ["private-provider-diagnostic"]
    elif mode == "unknown_facet":
        assessment["task"]["matched_facet_ids"] = ["private-provider-diagnostic"]
    elif mode == "missing_coverage":
        assessment["coverage"].pop()
    captured = []
    original = deepcopy((answers, requirements.model_dump(), item_row))

    def respond(request):
        captured.append(json.loads(request.content))
        return httpx.Response(200, json=response_body(assessment, mode))

    if async_mode:
        async def screen():
            async with AsyncOpenAI(api_key="unit-test-placeholder", http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))) as client:
                return await AsyncItemScreener(client)(answers, requirements, item_row)
        result = asyncio.run(screen())
    else:
        with OpenAI(api_key="unit-test-placeholder", http_client=httpx.Client(transport=httpx.MockTransport(respond))) as client:
            result = ItemScreener(client)(answers, requirements, item_row)
    assert len(captured) == 1
    request = captured[0]
    assert request["model"] == "gpt-6-luna"
    assert request["reasoning"] == {"effort": "high"} and request["max_output_tokens"] == 25000
    assert request["store"] is False and "tools" not in request
    assert request["instructions"] == PROMPT_PATH.read_text()
    assert json.loads(request["input"]) == {"answers": answers, "requirements": requirements.model_dump(), "item": item_row}
    assert original == (answers, requirements.model_dump(), item_row)
    schema = request["text"]["format"]["schema"]
    assert request["text"]["format"]["strict"] is True
    for model in [schema, *schema["$defs"].values()]:
        assert model["additionalProperties"] is False
        assert set(model["required"]) == set(model["properties"])
    assert result["response_id"] == "resp_screen" and result["response_model"] == "gpt-6-luna"
    assert result["usage"]["output_tokens_details"]["reasoning_tokens"] == 30
    assert "raw_output" not in result and "overall_score" not in result
    if mode == "complete":
        assert result["status"] == "complete" and result["assessment"] == assessment
        assert result["gate"]["status"] == "pass"
    else:
        assert result["status"] == "error" and "assessment" not in result and "gate" not in result
        if mode == "fabricated_quote":
            # Parsed evidence is saved for diagnosis, not accepted as an assessment.
            assert 'Assessment field: ratings.input_form.evidence[0]' in result["error"]
            assert 'Returned quotation: "private-provider-diagnostic"' in result["error"]
        else:
            assert "private-provider-diagnostic" not in json.dumps(result)


@pytest.mark.parametrize("dimension", GATED_DIMENSIONS)
@pytest.mark.parametrize("score,expected", [(1, "fail"), (2, "fail"), (3, "pass"), (5, "pass"), (None, "unresolved")])
def test_each_gated_dimension_has_independent_threshold(assessment, dimension, score, expected):
    assessment["ratings"][dimension] = rating(score)
    result = gate_for(ScreeningAssessment.model_validate(assessment))
    assert result["status"] == expected
    assert result["reasons"]


@pytest.mark.parametrize("dimension", ["output_content", "output_form"])
@pytest.mark.parametrize("score", [1, None])
def test_other_two_ratings_never_change_gate(assessment, dimension, score):
    assessment["ratings"][dimension] = rating(score)
    assert gate_for(ScreeningAssessment.model_validate(assessment))["status"] == "pass"


def test_no_match_and_known_low_scores_dominate_other_uncertainty(assessment):
    assessment["task"].update(status="no_match", matched_facet_ids=[])
    assessment["ratings"]["input_form"] = rating(None)
    assert gate_for(ScreeningAssessment.model_validate(assessment))["status"] == "fail"
    assessment["task"].update(status="unresolved", decision=None, evidence=[], information_gaps=["Question is incomplete."])
    assert gate_for(ScreeningAssessment.model_validate(assessment))["status"] == "unresolved"
    assessment["ratings"]["input_ontology"] = rating(2)
    assert gate_for(ScreeningAssessment.model_validate(assessment))["status"] == "fail"


@pytest.mark.parametrize("facet", ["diagnosis", "investigation"])
def test_nonessential_and_unknown_essential_facets_can_match(requirements, item_row, assessment, facet):
    assessment["task"]["matched_facet_ids"] = [facet]
    assessment["coverage"][0]["satisfied"] = False
    value = ScreeningAssessment.model_validate(assessment)
    value.validate_context(requirements, item_row)
    assert gate_for(value)["status"] == "pass"


def test_multiple_requested_decisions_can_match_but_ids_must_be_unique(requirements, item_row, assessment):
    assessment["task"]["matched_facet_ids"] = ["initial_management", "diagnosis"]
    ScreeningAssessment.model_validate(assessment).validate_context(requirements, item_row)
    assessment["task"]["matched_facet_ids"].append("diagnosis")
    with pytest.raises(ValidationError, match="must not repeat"):
        ScreeningAssessment.model_validate(assessment)


@pytest.mark.parametrize("status,ids,decision,evidence,gaps", [
    ("matched", [], "decision", [QUESTION], []),
    ("no_match", ["diagnosis"], "decision", [QUESTION], []),
    ("unresolved", ["diagnosis"], None, [], ["gap"]),
    ("matched", ["diagnosis"], None, [QUESTION], []),
    ("no_match", [], None, [QUESTION], []),
    ("no_match", [], "decision", [], []),
    ("unresolved", [], None, [], []),
    ("unresolved", [], "tentative decision", [], ["gap"]),
])
def test_inconsistent_task_states_are_rejected(assessment, status, ids, decision, evidence, gaps):
    assessment["task"].update(status=status, matched_facet_ids=ids, decision=decision,
                              evidence=evidence, information_gaps=gaps)
    with pytest.raises(ValidationError):
        ScreeningAssessment.model_validate(assessment)


@pytest.mark.parametrize("change", ["missing", "duplicate", "unknown", "other_task", "no_match", "unresolved"])
def test_coverage_references_and_positive_task_scope_are_checked(requirements, item_row, assessment, change):
    if change == "missing":
        assessment["coverage"].pop()
    elif change == "duplicate":
        assessment["coverage"][1]["requirement_index"] = 0
    elif change == "unknown":
        assessment["coverage"][1]["requirement_index"] = 999
    elif change == "other_task":
        assessment["task"]["matched_facet_ids"] = ["diagnosis"]
    else:
        assessment["task"].update(status=change, matched_facet_ids=[], information_gaps=["The task is uncertain."])
    with pytest.raises(ValueError):
        ScreeningAssessment.model_validate(assessment).validate_context(requirements, item_row)


def test_coverage_unknown_or_unsatisfied_does_not_gate_and_zero_requirements_need_empty_list(requirements, item_row, assessment):
    assessment["coverage"][0].update(satisfied=None, information_gaps=["The allergy's effect is unclear."])
    assessment["coverage"][1]["satisfied"] = False
    value = ScreeningAssessment.model_validate(assessment)
    value.validate_context(requirements, item_row)
    assert gate_for(value)["status"] == "pass"
    requirements.coverage_requirements.clear()
    assessment["coverage"] = []
    ScreeningAssessment.model_validate(assessment).validate_context(requirements, item_row)


@pytest.mark.parametrize("location", ["task", *DIMENSIONS, "coverage"])
def test_all_findings_require_literal_item_evidence(requirements, item_row, assessment, location):
    finding = assessment["task"] if location == "task" else (
        assessment["coverage"][0] if location == "coverage" else assessment["ratings"][location])
    finding["evidence"] = ["A fabricated source excerpt."]
    with pytest.raises(ValueError, match="quotation"):
        ScreeningAssessment.model_validate(assessment).validate_context(requirements, item_row)


@pytest.mark.parametrize("quote", ["content", "English-speaking students.", QUESTION + CONSTRAINT, "Which  initial management is indicated?"])
def test_keys_goal_only_quotes_joined_values_and_rewritten_whitespace_are_not_evidence(requirements, item_row, assessment, quote):
    assessment["ratings"]["input_content"]["evidence"] = [quote]
    with pytest.raises(ValueError, match="quotation"):
        ScreeningAssessment.model_validate(assessment).validate_context(requirements, item_row)


def test_quote_errors_identify_every_rejected_excerpt_without_changing_it(requirements, item_row, assessment):
    task_quote = 'Changed task wording with "quotes", a newline\nthen literal \\n.'
    rating_quote = 'A fabricated source excerpt: <img src=x onerror=alert(1)>.'
    coverage_quote = 'Unverified coverage \u2014 preserve punctuation.'
    assessment["task"]["evidence"] = [QUESTION, task_quote]
    assessment["ratings"]["input_content"]["evidence"] = [rating_quote]
    assessment["coverage"][1]["evidence"] = [coverage_quote]
    original = deepcopy((assessment, item_row))
    with pytest.raises(ValueError) as caught:
        ScreeningAssessment.model_validate(assessment).validate_context(requirements, item_row)
    message = str(caught.value)
    assert message.startswith("A screening evidence quotation does not occur exactly in the original item.")
    for path, quote in (
        ("task.evidence[1]", task_quote),
        ("ratings.input_content.evidence[0]", rating_quote),
        ("coverage[1].evidence[0]", coverage_quote),
    ):
        assert f"Assessment field: {path}\nReturned quotation: {json.dumps(quote, ensure_ascii=False)}" in message
    assert message.count("Returned quotation:") == 3
    assert "Assessment field: task.evidence[0]" not in message
    assert (assessment, item_row) == original


def test_nested_and_raw_json_cell_excerpts_preserve_original_values(requirements, item_row, assessment):
    item_row["new_field"] = [{"note": "Multiline\noriginal evidence."}]
    item_row["json_cell"] = '{ "rule": "keep original spacing" }'
    assessment["ratings"]["input_form"]["evidence"] = ["Multiline\noriginal evidence."]
    assessment["ratings"]["output_form"]["evidence"] = ['"rule": "keep original spacing"']
    ScreeningAssessment.model_validate(assessment).validate_context(requirements, item_row)
    assessment["ratings"]["output_form"]["evidence"] = ['{"rule":"keep original spacing"}']
    with pytest.raises(ValueError, match="quotation"):
        ScreeningAssessment.model_validate(assessment).validate_context(requirements, item_row)


@pytest.mark.parametrize("mutation", ["known_no_evidence", "unknown_no_gap", "blank_evidence", "blank_reason", "bool_score", "too_high", "extra_confidence"])
def test_rating_validation_is_strict_without_forcing_unknowns(assessment, mutation):
    value = assessment["ratings"]["input_content"]
    if mutation == "known_no_evidence": value["evidence"] = []
    elif mutation == "unknown_no_gap": value["score"] = None
    elif mutation == "blank_evidence": value["evidence"] = [" "]
    elif mutation == "blank_reason": value["justification"] = " "
    elif mutation == "bool_score": value["score"] = True
    elif mutation == "too_high": value["score"] = 6
    else: value["confidence"] = 0.9
    with pytest.raises(ValidationError):
        ScreeningAssessment.model_validate(assessment)


def test_missing_media_and_opaque_scorer_can_leave_only_affected_dimensions_unknown(requirements, item_row, assessment):
    item_row["asset_manifest"] = {"url": "https://unfetched.invalid/image.png"}
    item_row["grading_criterion"] = None
    assessment["ratings"]["input_form"] = rating(None, "https://unfetched.invalid/image.png")
    assessment["ratings"]["input_form"]["information_gaps"] = ["The required image is not included in the row."]
    assessment["ratings"]["output_ontology"] = rating(None, QUESTION)
    assessment["ratings"]["output_ontology"]["information_gaps"] = ["Source scoring behavior is absent."]
    assessment["ratings"]["output_form"] = rating(None, QUESTION)
    value = ScreeningAssessment.model_validate(assessment)
    value.validate_context(requirements, item_row)
    assert value.ratings.input_ontology.score == 4
    assert gate_for(value)["status"] == "unresolved"
    assert value.ratings.output_content.score is None


def test_input_validation_happens_before_any_model_call(answers, requirements, item_row):
    screener = ItemScreener(None)
    broken_answers = {**answers, "task": "changed after extraction"}
    with pytest.raises(ValueError, match="quotation"):
        screener.request_options(broken_answers, requirements, item_row)
    with pytest.raises(ValueError, match="complete original item row"):
        screener.request_options(answers, requirements, [])
    custom = ItemScreener(None, prompt="Custom instructions", model="custom", reasoning_effort="low", max_output_tokens=200)
    options = custom.request_options(answers, requirements, item_row)
    assert options["instructions"] == "Custom instructions" and options["model"] == "custom"
    assert options["reasoning"] == {"effort": "low"} and options["max_output_tokens"] == 200
    assert SCREENING_VERSION == 1
