"""Query provenance and fixed screening order, without model or dataset calls."""

from copy import deepcopy

import pytest

from bayesian_auditing.benchmark_queries import (
    ScreeningQueues, build_benchmark_queries, build_screening_queues,
)
from bayesian_auditing.requirements import Requirements


def supported(text, answer_id, quote=None):
    return {"text": text, "evidence": [{"answer_id": answer_id, "quote": text if quote is None else quote}]}


@pytest.fixture
def context():
    answers = {
        "task": "Answer practice clinical questions.",
        "users": "Medical students in an educational setting.",
        "inputs": "A text case with labeled options.",
        "outputs": "One supplied option identifier.",
        "success": "Choose initial management. Identify the diagnosis. Consider stated allergies. Include at least three constrained management cases.",
        "constraints": "Educational practice only; no instructions for real patients.",
    }
    requirements = Requirements.model_validate({
        "workflow": supported(answers["task"], "task"),
        "primary_user": supported(answers["users"], "users"),
        "input_types": supported(answers["inputs"], "inputs"),
        "output_types": supported(answers["outputs"], "outputs"),
        "authority": supported(answers["constraints"], "constraints"),
        "task_facets": [{
            "facet_id": facet_id, "task": supported(task, "success"),
            "required_input_evidence": supported("text case with labeled options", "inputs"),
            "required_output_behavior": supported("supplied option identifier", "outputs"),
            "essential": True,
        } for facet_id, task in [("management", "Choose initial management"), ("diagnosis", "Identify the diagnosis")]],
        "coverage_requirements": [{
            "facet_ids": ["management"], "minimum_items": 3,
            "requirement": supported("Include at least three constrained management cases.", "success"),
        }],
        "unresolved_details": [],
    })
    mapping = {
        "facet_id": "management",
        "records": [{
            "record_id": "onet-management",
            "supporting_passage": "Assess risks and benefits of treatment options.",
            "applicability": "partially_applicable",
            "rationale": "Only treatment vocabulary applies to these practice questions.",
            "search_terms": ["risks and benefits", "treatment options"],
        }, {
            "record_id": "onet-rejected",
            "supporting_passage": "Dispense prescriptions to patients.",
            "applicability": "not_applicable",
            "rationale": "Dispensing prescriptions is outside this educational task.",
            "search_terms": [],
        }],
        "refinements": [supported("Consider stated allergies.", "success")],
        "unresolved_details": [],
    }
    grounding = {"facets": [{
        "facet_id": "management", "status": "complete", "mapping": mapping,
        "candidates": [{
            "doc_id": record["record_id"], "text": record["supporting_passage"],
            "name": "This unused candidate name must not enter a benchmark query.",
        } for record in mapping["records"]],
    }, {
        "facet_id": "diagnosis", "status": "complete", "candidates": [],
        "mapping": {"facet_id": "diagnosis", "records": [], "refinements": [],
                    "unresolved_details": ["No related descriptions were retrieved."]},
    }]}
    return answers, requirements, grounding


def test_queries_preserve_requirements_and_only_adopt_supported_vocabulary(context):
    answers, requirements, grounding = context
    before = deepcopy((answers, requirements.model_dump(), grounding))
    management, diagnosis = build_benchmark_queries(*context)
    assert management == {
        "facet_id": "management",
        "query": "\n".join([
            "Task: Choose initial management",
            "Required input evidence: text case with labeled options",
            "Required output behavior: supplied option identifier",
            "Workflow: Answer practice clinical questions.",
            "Users and context: Medical students in an educational setting.",
            "Input types: A text case with labeled options.",
            "Output types: One supplied option identifier.",
            "Authority and constraints: Educational practice only; no instructions for real patients.",
            "O*NET search vocabulary: risks and benefits; treatment options",
            "Goal-grounded refinement: Consider stated allergies.",
        ]),
        "onet_record_ids": ["onet-management"],
        "search_terms": ["risks and benefits", "treatment options"],
        "refinements": grounding["facets"][0]["mapping"]["refinements"],
    }
    assert "Task: Identify the diagnosis" in diagnosis["query"]
    assert "risks and benefits" not in diagnosis["query"]
    assert diagnosis["search_terms"] == diagnosis["onet_record_ids"] == []
    for result in (management, diagnosis):
        assert "Dispense prescriptions" not in result["query"]
        assert "unused candidate name" not in result["query"]
        assert "three constrained" not in result["query"]  # A collection quota is not an item instruction.
    assert (answers, requirements.model_dump(), grounding) == before
    # Neither returned refinements nor query text are views into earlier artifacts.
    management["refinements"][0]["text"] = "changed downstream"
    assert (answers, requirements.model_dump(), grounding) == before


def test_queries_follow_requirement_order_and_deduplicate_supported_terms(context):
    answers, requirements, grounding = context
    grounding["facets"].reverse()
    management = grounding["facets"][1]
    additional = deepcopy(management["mapping"]["records"][0])
    additional["record_id"] = "second-support"
    additional["applicability"] = "applicable"
    management["mapping"]["records"].append(additional)
    management["candidates"].append({"doc_id": "second-support", "text": additional["supporting_passage"]})
    queries = build_benchmark_queries(*context)
    assert [query["facet_id"] for query in queries] == ["management", "diagnosis"]
    assert queries[0]["search_terms"] == ["risks and benefits", "treatment options"]
    assert queries[0]["onet_record_ids"] == ["onet-management", "second-support"]


def test_unknown_requirement_fields_are_omitted_without_inference(context):
    answers, requirements, grounding = context
    payload = requirements.model_dump()
    payload["authority"] = {"text": None, "evidence": []}
    payload["task_facets"][0]["required_input_evidence"] = {"text": None, "evidence": []}
    query = build_benchmark_queries(answers, Requirements.model_validate(payload), grounding)[0]["query"]
    assert "Authority and constraints:" not in query
    assert "Required input evidence:" not in query
    assert "Input types: A text case with labeled options." in query


@pytest.mark.parametrize("problem", [
    "missing_facet", "duplicate_facet", "unknown_facet", "failed_facet", "pending_facet",
    "wrong_mapping_facet", "missing_candidates", "unknown_record", "bad_passage",
    "bad_search_term", "bad_refinement_evidence", "bad_requirement_evidence",
    "invalid_rejected_record", "malformed_candidate", "missing_mapping", "unexplained_empty_mapping",
])
def test_invalid_upstream_artifacts_cannot_produce_queries(context, problem):
    answers, requirements, grounding = context
    entry = grounding["facets"][0]
    mapping = entry["mapping"]
    if problem == "missing_facet":
        grounding["facets"].pop()
    elif problem == "duplicate_facet":
        grounding["facets"].append(deepcopy(entry))
    elif problem == "unknown_facet":
        entry["facet_id"] = "new occupational duty"
    elif problem == "failed_facet":
        entry["status"] = "error"
    elif problem == "pending_facet":
        entry["status"] = "running"
    elif problem == "wrong_mapping_facet":
        mapping["facet_id"] = "diagnosis"
    elif problem == "missing_candidates":
        entry.pop("candidates")
    elif problem == "unknown_record":
        mapping["records"][0]["record_id"] = "not retrieved"
    elif problem == "bad_passage":
        mapping["records"][0]["supporting_passage"] += " Invented extension."
    elif problem == "bad_search_term":
        mapping["records"][0]["search_terms"].append("not in passage")
    elif problem == "bad_refinement_evidence":
        mapping["refinements"][0]["evidence"][0]["quote"] = "not in answers"
    elif problem == "bad_requirement_evidence":
        requirements.workflow.evidence[0].quote = "not in answers"
    elif problem == "invalid_rejected_record":
        mapping["records"][1]["supporting_passage"] = "unverified rejected record"
    elif problem == "malformed_candidate":
        entry["candidates"].append(None)
    elif problem == "missing_mapping":
        entry.pop("mapping")
    elif problem == "unexplained_empty_mapping":
        grounding["facets"][1]["mapping"]["unresolved_details"] = []
    with pytest.raises(ValueError):
        build_benchmark_queries(*context)


def candidate(item_id, *sources):
    return {"item_id": item_id, "sources": [{"benchmark": source} for source in sources]}


@pytest.fixture
def rankings():
    return [{"facet_id": "management", "query": "management query", "candidates": [
        candidate("shared", "alpha", "beta", "alpha"),
        candidate("alpha-only", "alpha"),
        candidate("beta-only", "beta"),
        candidate("no-source"),
    ]}, {"facet_id": "diagnosis", "query": "diagnosis query", "candidates": [
        candidate("beta-only", "beta"), candidate("shared", "alpha", "beta"),
        candidate("diagnosis-only", "alpha"),
    ]}]


def test_static_queues_keep_ranks_and_source_membership(rankings):
    before = deepcopy(rankings)
    queues = build_screening_queues(rankings)
    assert [(queue["facet_id"], queue["source"], queue["item_ids"]) for queue in queues] == [
        ("management", None, ["shared", "alpha-only", "beta-only", "no-source"]),
        ("management", "alpha", ["shared", "alpha-only"]),
        ("management", "beta", ["shared", "beta-only"]),
        ("diagnosis", None, ["beta-only", "shared", "diagnosis-only"]),
        ("diagnosis", "beta", ["beta-only", "shared"]),
        ("diagnosis", "alpha", ["shared", "diagnosis-only"]),
    ]
    assert rankings == before


def test_duplicate_evidence_is_once_per_queue_without_losing_sources():
    queues = build_screening_queues([{"facet_id": "task", "candidates": [
        candidate("same", "alpha"), candidate("other", "beta"), candidate("same", "beta"),
    ]}])
    assert [queue["item_ids"] for queue in queues] == [["same", "other"], ["same"], ["other", "same"]]


def test_queue_identifiers_distinguish_arbitrary_facets_sources_and_global_queue():
    rankings = [{"facet_id": facet_id, "candidates": [candidate("one", *sources)]}
                for facet_id, sources in [("task|source", ["all", "null", "任務"]), ("task", ["source|all", '["x",null]'])]]
    queues = build_screening_queues(rankings)
    assert len({queue["queue_id"] for queue in queues}) == 7
    assert build_screening_queues(deepcopy(rankings)) == queues


def test_global_screened_set_skips_overlapping_tasks_and_sources(rankings):
    queues = build_screening_queues(rankings)
    reader = ScreeningQueues(queues)
    screened = set()
    management_all, management_alpha, management_beta, diagnosis_all = [queue["queue_id"] for queue in queues[:4]]
    attempted = reader.take(management_all, 2, screened)
    assert attempted == ["shared", "alpha-only"]
    assert screened == set()
    assert reader.take(management_all, 2, screened) == attempted  # Cancellation does not consume a batch.
    screened.update(attempted)
    assert reader.take(management_alpha, 8, screened) == []
    assert reader.take(management_beta, 8, screened) == ["beta-only"]
    assert reader.take(diagnosis_all, 8, screened) == ["beta-only", "diagnosis-only"]
    screened.add("beta-only")
    assert reader.take(management_all, 8, screened) == ["no-source"]
    assert reader.take(diagnosis_all, 8, screened) == ["diagnosis-only"]


def test_empty_queues_and_batch_limits():
    queues = build_screening_queues([{"facet_id": "empty", "candidates": []}])
    assert len(queues) == 1
    reader = ScreeningQueues(queues)
    queue_id = queues[0]["queue_id"]
    assert reader.take(queue_id, 8, set()) == []
    assert reader.take(queue_id, 0, set()) == []
    with pytest.raises(KeyError):
        reader.take("unknown", 1, set())
    for invalid_limit in (-1, True, 1.5):
        with pytest.raises(ValueError):
            reader.take(queue_id, invalid_limit, set())


def test_queue_snapshot_cannot_be_changed_by_mutating_export(rankings):
    queues = build_screening_queues(rankings)
    reader = ScreeningQueues(queues)
    queue_id = queues[0]["queue_id"]
    queues[0]["item_ids"].clear()
    assert reader.take(queue_id, 1, set()) == ["shared"]


@pytest.mark.parametrize("problem", ["duplicate_facet", "empty_item_id", "bad_source", "duplicate_queue", "repeated_item"])
def test_invalid_rankings_and_queues_fail_clearly(rankings, problem):
    if problem == "duplicate_facet":
        rankings.append(deepcopy(rankings[0]))
    elif problem == "empty_item_id":
        rankings[0]["candidates"][0]["item_id"] = " "
    elif problem == "bad_source":
        rankings[0]["candidates"][0]["sources"] = [{"benchmark": None}]
    if problem in {"duplicate_facet", "empty_item_id", "bad_source"}:
        with pytest.raises(ValueError):
            build_screening_queues(rankings)
        return
    queues = build_screening_queues(rankings)
    if problem == "duplicate_queue":
        queues.append(deepcopy(queues[0]))
    elif problem == "repeated_item":
        queues[0]["item_ids"].append("shared")
    with pytest.raises(ValueError):
        ScreeningQueues(queues)
