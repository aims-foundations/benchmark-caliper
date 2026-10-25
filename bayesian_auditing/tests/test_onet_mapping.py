"""Grounding contracts with mocked Responses; these do not measure LLM quality."""

import asyncio
from copy import deepcopy
import json
from pathlib import Path

import httpx
from openai import AsyncOpenAI, OpenAI
from pydantic import ValidationError
import pytest

from bayesian_auditing.onet_mapping import (
    AsyncOnetMapper, DEFAULT_MODEL, MAX_REFINEMENTS, OnetMapper, OnetMapping,
    PROMPT_PATH, build_onet_query,
)
from bayesian_auditing.requirements import Requirements


def supported(text, answer_id, quote):
    return {"text": text, "evidence": [{"answer_id": answer_id, "quote": quote}]}


@pytest.fixture
def answers():
    path = Path(__file__).parents[1] / "examples" / "medical_study_goal.json"
    return json.loads(path.read_text())


@pytest.fixture
def requirements(answers):
    """Use one existing facet with the paper's separately retained collection quota."""
    return Requirements.model_validate({
        "workflow": supported(answers["task"], "task", answers["task"]),
        "primary_user": supported(answers["users"], "users", answers["users"]),
        "input_types": supported(answers["inputs"], "inputs", answers["inputs"]),
        "output_types": supported(answers["outputs"], "outputs", answers["outputs"]),
        "authority": supported(answers["constraints"], "constraints", answers["constraints"]),
        "task_facets": [{
            "facet_id": "initial_management",
            "task": supported("Choose the indicated initial management", "success", "choose the indicated initial management"),
            "required_input_evidence": supported(answers["inputs"], "inputs", answers["inputs"]),
            "required_output_behavior": supported(answers["outputs"], "outputs", answers["outputs"]),
            "essential": True,
        }],
        "coverage_requirements": [{
            "facet_ids": ["initial_management"], "minimum_items": 3,
            "requirement": supported(answers["success"].split(". ")[1], "success", answers["success"].split(". ")[1]),
        }],
        "unresolved_details": [],
    })


@pytest.fixture
def candidates():
    # Exact supplied O*NET record, including its hierarchy and occupation link.
    return [{
        "doc_id": "dwa:4.A.2.a.1.f.4::29-1229.01",
        "kind": "activity_edge",
        "name": "Evaluate treatment options to guide medical decisions.",
        "text": "Judging the Qualities of Objects, Services, or People > Evaluate patient or client condition or treatment options. > Evaluate treatment options to guide medical decisions. Assess the risks and benefits of therapies for allergic and immunologic disorders.",
        "occupation_id": "29-1229.01", "dense_rank": 1, "bm25_rank": 3,
        "rrf_score": 0.032,
    }]


@pytest.fixture
def mapping(candidates):
    return {
        "facet_id": "initial_management",
        "records": [{
            "record_id": candidates[0]["doc_id"],
            "supporting_passage": "Assess the risks and benefits of therapies for allergic and immunologic disorders.",
            "applicability": "partially_applicable",
            "rationale": "Therapy risks and benefits provide related vocabulary for management questions. The record's allergy and immunology setting does not limit the educational deployment to that specialty or confer authority to treat patients.",
            "search_terms": ["risks and benefits", "therapies"],
        }],
        "refinements": [supported(
            "Consider stated allergies, medications, or contraindications only when they materially constrain management.",
            "success", "a stated allergy, medication, or contraindication materially constrains the management choice",
        )],
        "unresolved_details": [],
    }


def response_body(mapping, mode="complete"):
    content = [{"type": "output_text", "text": json.dumps(mapping), "annotations": []}]
    if mode in {"refusal", "mixed_refusal"}:
        refusal = {"type": "refusal", "refusal": "private-provider-diagnostic"}
        content = [refusal] if mode == "refusal" else [*content, refusal]
    if mode == "malformed":
        content[0]["text"] = "private-provider-diagnostic: not json"
    return {
        "id": "resp_map", "object": "response", "created_at": 1, "model": DEFAULT_MODEL,
        "status": "incomplete" if mode == "incomplete" else "completed",
        "incomplete_details": {"reason": "max_output_tokens"} if mode == "incomplete" else None,
        "output": [{"type": "message", "id": "msg_map", "status": "completed", "role": "assistant", "content": content}],
        "usage": {"input_tokens": 100, "output_tokens": 90, "total_tokens": 190,
                  "input_tokens_details": {"cached_tokens": 10}, "output_tokens_details": {"reasoning_tokens": 30}},
    }


@pytest.mark.parametrize("async_mode", [False, True])
@pytest.mark.parametrize("mode", [
    "complete", "no_match", "unknown_record", "wrong_facet", "nonliteral_quote",
    "nonliteral_term", "bad_refinement", "bad_answer_id", "malformed",
    "incomplete", "refusal", "mixed_refusal",
])
def test_real_sdk_request_and_response_contract(answers, requirements, candidates, mapping, async_mode, mode):
    facet = requirements.task_facets[0]
    if mode == "no_match":
        mapping["records"] = []
        mapping["refinements"] = []
        mapping["unresolved_details"] = ["No shortlisted record supplies applicable vocabulary."]
    elif mode == "unknown_record":
        mapping["records"][0]["record_id"] = "private-provider-diagnostic"
    elif mode == "wrong_facet":
        mapping["facet_id"] = "private-provider-diagnostic"
    elif mode == "nonliteral_quote":
        mapping["records"][0]["supporting_passage"] = "private-provider-diagnostic: risks and benefits of therapies"
    elif mode == "nonliteral_term":
        mapping["records"][0]["search_terms"] = ["private-provider-diagnostic"]
    elif mode == "bad_refinement":
        mapping["refinements"][0]["evidence"][0]["quote"] = "private-provider-diagnostic"
    elif mode == "bad_answer_id":
        mapping["refinements"][0]["evidence"][0]["answer_id"] = "private-provider-diagnostic"
    captured = []
    original_answers, original_requirements, original_candidates = deepcopy(answers), requirements.model_dump(), deepcopy(candidates)

    def respond(request):
        captured.append(json.loads(request.content))
        return httpx.Response(200, json=response_body(mapping, mode))

    if async_mode:
        async def run():
            async with AsyncOpenAI(api_key="unit-test-placeholder", http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))) as client:
                return await AsyncOnetMapper(client)(answers, requirements, facet, candidates)
        result = asyncio.run(run())
    else:
        with OpenAI(api_key="unit-test-placeholder", http_client=httpx.Client(transport=httpx.MockTransport(respond))) as client:
            result = OnetMapper(client)(answers, requirements, facet, candidates)

    assert len(captured) == 1  # Invalid outputs do not trigger paid repair calls.
    request = captured[0]
    assert request["instructions"] == PROMPT_PATH.read_text()
    assert request["model"] == "gpt-6-luna"
    assert request["reasoning"] == {"effort": "high"}
    assert request["max_output_tokens"] == 25_000
    assert request["store"] is False
    assert json.loads(request["input"]) == {
        "answers": original_answers, "requirements": original_requirements,
        "facet": facet.model_dump(), "candidates": original_candidates,
    }
    assert answers == original_answers and requirements.model_dump() == original_requirements
    assert candidates == original_candidates
    schema = request["text"]["format"]["schema"]
    assert request["text"]["format"]["strict"] is True
    for model in [schema, *schema["$defs"].values()]:
        assert model["additionalProperties"] is False
        assert set(model["required"]) == set(model["properties"])
    assert result["response_id"] == "resp_map"
    assert result["response_model"] == DEFAULT_MODEL
    assert result["usage"]["output_tokens_details"]["reasoning_tokens"] == 30
    assert "raw_output" not in result
    if mode in {"complete", "no_match"}:
        assert result["status"] == "complete" and result["mapping"] == mapping
        assert "error" not in result
    else:
        assert result["status"] == "error" and "mapping" not in result
        assert result["error"]
        assert "private-provider-diagnostic" not in json.dumps(result)


@pytest.mark.parametrize("case", [
    "duplicate_record", "blank_id", "blank_passage", "blank_rationale",
    "adopted_without_terms", "rejected_with_terms", "duplicate_terms", "blank_term",
    "unknown_refinement", "unsupported_refinement", "too_many_refinements",
    "empty_unexplained", "blank_unresolved", "extra_task", "invalid_applicability",
])
def test_rejects_unsupported_or_inconsistent_mapping(mapping, case):
    record = mapping["records"][0]
    if case == "duplicate_record":
        mapping["records"].append(deepcopy(record))
    elif case.startswith("blank_") and case != "blank_unresolved":
        field = {"blank_id": "record_id", "blank_passage": "supporting_passage", "blank_rationale": "rationale"}.get(case)
        if field:
            record[field] = " \n"
        else:
            record["search_terms"] = [" "]
    elif case == "adopted_without_terms":
        record["search_terms"] = []
    elif case == "rejected_with_terms":
        record["applicability"] = "not_applicable"
    elif case == "duplicate_terms":
        record["search_terms"].append(record["search_terms"][0])
    elif case == "unknown_refinement":
        mapping["refinements"] = [{"text": None, "evidence": []}]
    elif case == "unsupported_refinement":
        mapping["refinements"][0]["evidence"] = []
    elif case == "too_many_refinements":
        mapping["refinements"] *= MAX_REFINEMENTS + 1
    elif case == "empty_unexplained":
        mapping["records"] = []
    elif case == "blank_unresolved":
        mapping["unresolved_details"] = [" "]
    elif case == "extra_task":
        mapping["task"] = "Treat real patients."
    elif case == "invalid_applicability":
        record["applicability"] = "maybe"
    with pytest.raises(ValidationError):
        OnetMapping.model_validate(mapping)


def test_rejected_records_and_no_candidates_are_valid_explained_outcomes(answers, requirements, candidates, mapping):
    mapping["records"][0]["applicability"] = "not_applicable"
    mapping["records"][0]["search_terms"] = []
    mapping["records"][0]["rationale"] = "The activity does not apply to this deployment."
    OnetMapping.model_validate(mapping).validate_context(answers, requirements.task_facets[0], candidates)
    mapping["records"] = []
    mapping["unresolved_details"] = ["No matching records were retrieved."]
    OnetMapping.model_validate(mapping).validate_context(answers, requirements.task_facets[0], [])


def test_quote_checks_preserve_unicode_whitespace_and_named_source(answers, requirements, candidates, mapping):
    candidates[0]["text"] = "  Évaluer\n les options.  "
    record = mapping["records"][0]
    record["supporting_passage"] = "Évaluer\n les options."
    record["search_terms"] = ["Évaluer", "options"]
    answers["constraints"] = "  Éducation\n uniquement.  "
    mapping["refinements"] = [supported("Educational context", "constraints", "Éducation\n uniquement.")]
    OnetMapping.model_validate(mapping).validate_context(answers, requirements.task_facets[0], candidates)
    record["supporting_passage"] = "Évaluer les options."
    with pytest.raises(ValueError, match="does not occur exactly"):
        OnetMapping.model_validate(mapping).validate_context(answers, requirements.task_facets[0], candidates)
    record["supporting_passage"] = "Évaluer\n les options."
    mapping["refinements"][0]["evidence"][0]["answer_id"] = "task"
    with pytest.raises(ValueError, match="original answer"):
        OnetMapping.model_validate(mapping).validate_context(answers, requirements.task_facets[0], candidates)


@pytest.mark.parametrize("case", ["unknown_facet", "changed_facet", "bad_goal_quote", "missing_candidate_id", "duplicate_candidate", "blank_candidate"])
def test_invalid_inputs_fail_before_provider_call(answers, requirements, candidates, case):
    mapper = OnetMapper(None)
    facet = requirements.task_facets[0].model_copy(deep=True)
    if case == "unknown_facet":
        facet.facet_id = "unknown"
    elif case == "changed_facet":
        facet.essential = False
    elif case == "bad_goal_quote":
        requirements.workflow.evidence[0].quote = "not in original answer"
    elif case == "missing_candidate_id":
        candidates[0].pop("doc_id")
    elif case == "duplicate_candidate":
        candidates.append(deepcopy(candidates[0]))
    elif case == "blank_candidate":
        candidates[0]["text"] = " "
    with pytest.raises(ValueError):
        mapper(answers, requirements, facet, candidates)


def test_search_queries_distinguish_tasks_without_shared_context_or_quotas(requirements):
    facet = requirements.task_facets[0]
    diagnosis = facet.model_copy(deep=True)
    diagnosis.facet_id = "diagnosis"
    diagnosis.task.text = "Identify the likely diagnosis"
    diagnosis.task.evidence[0].quote = "Identify the likely diagnosis"
    requirements.task_facets.append(diagnosis)
    original = requirements.model_dump()

    query = build_onet_query(requirements, facet)
    diagnosis_query = build_onet_query(requirements, diagnosis)
    assert query == "Choose the indicated initial management"
    assert diagnosis_query == "Identify the likely diagnosis"
    assert query != diagnosis_query
    for context in (facet.required_input_evidence, facet.required_output_behavior,
                    requirements.workflow, requirements.primary_user, requirements.authority):
        assert context.text not in query and context.text not in diagnosis_query
    assert "at least three" not in query
    assert requirements.model_dump() == original

    facet = facet.model_copy(deep=True)
    facet.task.text = "A different task"
    with pytest.raises(ValueError, match="extracted task facet"):
        build_onet_query(requirements, facet)
