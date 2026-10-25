"""Extraction contracts with mocked Responses; these do not measure LLM quality."""

import asyncio
from copy import deepcopy
import json
from pathlib import Path

import httpx
from openai import AsyncOpenAI, OpenAI
from pydantic import ValidationError
import pytest

from bayesian_auditing.requirements import (
    AsyncRequirementExtractor, DEFAULT_MODEL, PROMPT_PATH,
    RequirementExtractor, Requirements,
)


def supported(text, answer_id, quote):
    return {"text": text, "evidence": [{"answer_id": answer_id, "quote": quote}]}


@pytest.fixture
def answers():
    path = Path(__file__).parents[1] / "examples" / "medical_study_goal.json"
    return json.loads(path.read_text())


@pytest.fixture
def requirements(answers):
    """A human-authored extraction of §2.2, including the separate collection quota."""
    tasks = [
        ("diagnosis", "Identify the likely diagnosis"),
        ("investigation", "choose the appropriate investigation"),
        ("initial_management", "choose the indicated initial management"),
    ]
    quota = answers["success"].split(". ")[1]
    facets = [{
        "facet_id": facet_id,
        "task": supported(task, "success", task),
        "required_input_evidence": supported(answers["inputs"], "inputs", answers["inputs"]),
        "required_output_behavior": {
            "text": "Provide a source-referenced answer in the question's requested format: a supplied option identifier or concise short answer.",
            "evidence": [
                {"answer_id": "outputs", "quote": answers["outputs"]},
                {"answer_id": "constraints", "quote": "one supplied option identifier or a concise short answer"},
            ],
        },
        "essential": True,
    } for facet_id, task in tasks]
    facets[2]["required_input_evidence"]["text"] += (
        " Include the stated allergy, medication, or contraindication when it materially constrains management."
    )
    facets[2]["required_input_evidence"]["evidence"].append({
        "answer_id": "success", "quote": "a stated allergy, medication, or contraindication materially constrains the management choice",
    })
    return {
        "workflow": supported(answers["task"], "task", answers["task"]),
        "primary_user": supported(answers["users"], "users", answers["users"]),
        "input_types": supported(answers["inputs"], "inputs", answers["inputs"]),
        "output_types": supported(answers["outputs"], "outputs", answers["outputs"]),
        "authority": supported("Educational practice only; not treatment instructions for real patients.",
                               "constraints", "This is an educational workflow; it does not provide treatment instructions for real patients."),
        "task_facets": facets,
        "coverage_requirements": [{
            "facet_ids": ["initial_management"], "minimum_items": 3,
            "requirement": supported(quota, "success", quota),
        }],
        "unresolved_details": [],
    }


def response_body(requirements, mode="complete"):
    content = [{"type": "output_text", "text": json.dumps(requirements), "annotations": []}]
    if mode in {"refusal", "mixed_refusal"}:
        refusal = {"type": "refusal", "refusal": "private-provider-diagnostic"}
        content = [refusal] if mode == "refusal" else [*content, refusal]
    if mode == "malformed":
        content[0]["text"] = "private-provider-diagnostic: not json"
    return {
        "id": "resp_extract", "object": "response", "created_at": 1, "model": DEFAULT_MODEL,
        "status": "incomplete" if mode == "incomplete" else "completed",
        "incomplete_details": {"reason": "max_output_tokens"} if mode == "incomplete" else None,
        "output": [{"type": "message", "id": "msg_extract", "status": "completed", "role": "assistant", "content": content}],
        "usage": {"input_tokens": 100, "output_tokens": 90, "total_tokens": 190,
                  "input_tokens_details": {"cached_tokens": 10}, "output_tokens_details": {"reasoning_tokens": 30}},
    }


@pytest.mark.parametrize("async_mode", [False, True])
@pytest.mark.parametrize("mode", ["complete", "unknown", "fabricated_quote", "bad_answer_id", "bad_facet_ref",
                                 "malformed", "incomplete", "refusal", "mixed_refusal"])
def test_real_sdk_request_and_response_contract(answers, requirements, async_mode, mode):
    if mode == "unknown":
        answers["constraints"] = ""
        requirements["authority"] = {"text": None, "evidence": []}
        requirements["unresolved_details"] = ["Authority is unspecified."]
        for facet in requirements["task_facets"]:
            facet["required_output_behavior"]["evidence"] = [
                {"answer_id": "outputs", "quote": answers["outputs"]},
            ]
    if mode == "fabricated_quote":
        requirements["task_facets"][0]["task"]["evidence"][0]["quote"] = "private-provider-diagnostic"
    if mode == "bad_answer_id":
        requirements["workflow"]["evidence"][0]["answer_id"] = "private-provider-diagnostic"
    if mode == "bad_facet_ref":
        requirements["coverage_requirements"][0]["facet_ids"] = ["private-provider-diagnostic"]
    captured = []
    original_answers = deepcopy(answers)

    def respond(request):
        captured.append(json.loads(request.content))
        return httpx.Response(200, json=response_body(requirements, mode))

    if async_mode:
        async def extract():
            async with AsyncOpenAI(api_key="unit-test-placeholder", http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))) as client:
                return await AsyncRequirementExtractor(client)(answers)
        result = asyncio.run(extract())
    else:
        with OpenAI(api_key="unit-test-placeholder", http_client=httpx.Client(transport=httpx.MockTransport(respond))) as client:
            result = RequirementExtractor(client)(answers)

    assert len(captured) == 1  # Invalid outputs do not cause another paid extraction.
    request = captured[0]
    assert request["model"] == "gpt-6-luna"
    assert request["reasoning"] == {"effort": "high"}
    assert request["max_output_tokens"] == 25_000
    assert request["store"] is False
    assert request["instructions"] == PROMPT_PATH.read_text()
    assert json.loads(request["input"])["answers"] == original_answers == answers
    assert request["text"]["format"]["strict"] is True
    schema = request["text"]["format"]["schema"]
    for model in [schema, *schema["$defs"].values()]:
        assert model["additionalProperties"] is False
        assert set(model["required"]) == set(model["properties"])
    assert result["response_id"] == "resp_extract"
    assert result["response_model"] == DEFAULT_MODEL
    assert result["usage"]["output_tokens_details"]["reasoning_tokens"] == 30
    assert "raw_output" not in result
    if mode in {"complete", "unknown"}:
        assert result["status"] == "complete"
        assert result["requirements"] == requirements
        assert "error" not in result
    else:
        assert result["status"] == "error"
        assert "requirements" not in result
        assert result["error"]
        assert "private-provider-diagnostic" not in json.dumps(result)


def test_paper_worked_example_preserves_distinct_tasks_and_conditional_quota(answers, requirements):
    result = Requirements.model_validate(requirements)
    result.validate_evidence(answers)
    assert [facet.facet_id for facet in result.task_facets] == ["diagnosis", "investigation", "initial_management"]
    assert all(facet.essential for facet in result.task_facets)
    quota, = result.coverage_requirements
    assert quota.minimum_items == 3 and quota.facet_ids == ["initial_management"]
    assert "materially constrains" in quota.requirement.text
    management = result.task_facets[2]
    assert "at least three" not in management.required_output_behavior.text
    assert {e.answer_id for e in management.required_output_behavior.evidence} == {"outputs", "constraints"}


@pytest.mark.parametrize("location", [
    ("workflow",), ("primary_user",), ("input_types",), ("output_types",), ("authority",),
    ("task_facets", 0, "task"), ("task_facets", 1, "required_input_evidence"),
    ("task_facets", 2, "required_output_behavior"), ("coverage_requirements", 0, "requirement"),
])
def test_checks_quotations_in_every_supported_field(answers, requirements, location):
    target = requirements
    for key in location:
        target = target[key]
    target["evidence"][0]["quote"] = "not in any source answer"
    with pytest.raises(ValueError, match="does not occur exactly"):
        Requirements.model_validate(requirements).validate_evidence(answers)


def test_quotations_preserve_whitespace_case_unicode_and_source(answers, requirements):
    answers["task"] = "  Répondre\n aux QUESTIONS.  "
    requirements["workflow"] = supported("Answer questions", "task", "Répondre\n aux QUESTIONS")
    Requirements.model_validate(requirements).validate_evidence(answers)
    requirements["workflow"]["evidence"][0]["quote"] = "Répondre aux QUESTIONS"
    with pytest.raises(ValueError, match="does not occur exactly"):
        Requirements.model_validate(requirements).validate_evidence(answers)
    requirements["workflow"]["evidence"][0] = {"answer_id": "users", "quote": answers["task"]}
    with pytest.raises(ValueError, match="'users' answer"):
        Requirements.model_validate(requirements).validate_evidence(answers)


@pytest.mark.parametrize("case", ["duplicate_facets", "unknown_facet", "unknown_task", "unknown_quota", "empty_facet_id",
                                 "unsupported_text", "blank_text", "unknown_with_evidence", "empty_quote", "extra_field"])
def test_rejects_inconsistent_structured_requirements(requirements, case):
    if case == "duplicate_facets":
        requirements["task_facets"].append(deepcopy(requirements["task_facets"][0]))
    elif case == "unknown_facet":
        requirements["coverage_requirements"][0]["facet_ids"] = ["not_extracted"]
    elif case == "unknown_task":
        requirements["task_facets"][0]["task"] = {"text": None, "evidence": []}
    elif case == "unknown_quota":
        requirements["coverage_requirements"][0]["requirement"] = {"text": None, "evidence": []}
    elif case == "empty_facet_id":
        requirements["task_facets"][0]["facet_id"] = " "
    elif case == "unsupported_text":
        requirements["workflow"]["evidence"] = []
    elif case == "blank_text":
        requirements["workflow"]["text"] = " "
    elif case == "unknown_with_evidence":
        requirements["workflow"]["text"] = None
    elif case == "empty_quote":
        requirements["workflow"]["evidence"][0]["quote"] = "\n "
    elif case == "extra_field":
        requirements["task_facets"][0]["assumed_authority"] = "Autonomous"
    with pytest.raises(ValidationError):
        Requirements.model_validate(requirements)


@pytest.mark.parametrize("minimum", [0, -1, 3.5, "3", True])
def test_minimum_is_a_positive_integer_without_type_coercion(requirements, minimum):
    requirements["coverage_requirements"][0]["minimum_items"] = minimum
    with pytest.raises(ValidationError):
        Requirements.model_validate(requirements)


def test_unsupported_quota_forms_are_preserved_without_reinterpreting_as_minimum(answers, requirements):
    answers["success"] += " Exactly 40% of cases must involve children."
    requirements["coverage_requirements"] = [{
        "facet_ids": [], "minimum_items": None,
        "requirement": supported("Exactly 40% of cases must involve children.", "success", "Exactly 40% of cases must involve children."),
    }]
    requirements["unresolved_details"] = ["The percentage target requires a separate enforcement rule; it is not an item minimum."]
    parsed = Requirements.model_validate(requirements)
    parsed.validate_evidence(answers)
    assert parsed.coverage_requirements[0].minimum_items is None


def test_unknowns_and_absent_tasks_remain_explicit(answers, requirements):
    answers["constraints"] = ""
    requirements["authority"] = {"text": None, "evidence": []}
    requirements["task_facets"] = []
    requirements["coverage_requirements"] = []
    requirements["unresolved_details"] = ["Authority and the required decisions are unclear."]
    parsed = Requirements.model_validate(requirements)
    parsed.validate_evidence(answers)
    assert parsed.authority.text is None
    assert parsed.task_facets == []


def test_other_domains_do_not_require_medical_facets(answers, requirements):
    answers["success"] = "Optionally translate the supplied text into French."
    requirements["task_facets"] = [{
        "facet_id": "translation",
        "task": supported(answers["success"], "success", answers["success"]),
        "required_input_evidence": {"text": None, "evidence": []},
        "required_output_behavior": {"text": None, "evidence": []},
        "essential": False,
    }]
    requirements["coverage_requirements"] = []
    parsed = Requirements.model_validate(requirements)
    parsed.validate_evidence(answers)
    assert parsed.task_facets[0].facet_id == "translation"
    assert parsed.task_facets[0].essential is False
    requirements["task_facets"][0]["essential"] = None
    assert Requirements.model_validate(requirements).task_facets[0].essential is None
