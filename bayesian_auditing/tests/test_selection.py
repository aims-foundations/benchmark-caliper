"""Exact collection selection checked against an independent exhaustive oracle."""

from copy import deepcopy
from itertools import combinations
import random
from types import SimpleNamespace

import pytest

from bayesian_auditing.benchmark_data import row_fingerprint
from bayesian_auditing.requirements import Requirements
from bayesian_auditing.scoring import DIMENSIONS
from bayesian_auditing.screening import GATED_DIMENSIONS, gate_for, ScreeningAssessment
from bayesian_auditing import selection


QUOTE = "Choose the action requested by this complete question."


def requirements(tasks=3, quotas=()):
    def supported(text):
        return {"text": text, "evidence": [{"answer_id": "success", "quote": text}]}

    return Requirements.model_validate({
        **{key: supported("Educational question answering.") for key in
           ("workflow", "primary_user", "input_types", "output_types", "authority")},
        "task_facets": [{
            "facet_id": f"task-{number}", "task": supported(f"Task {number}."),
            "required_input_evidence": supported("A complete question."),
            "required_output_behavior": supported("The requested answer."),
            "essential": (True, False, None)[number % 3],
        } for number in range(tasks)],
        "coverage_requirements": [{
            "facet_ids": [], "minimum_items": minimum,
            "requirement": supported(f"Feature requirement {number}."),
        } for number, minimum in enumerate(quotas)],
        "unresolved_details": [],
    })


def candidate(number, tasks=(0,), scores=(4, 4, 4, 4), coverage=()):
    row = {"item_id": f"original-{number}", "content": QUOTE,
           "grading_criterion": "Accept the requested answer.",
           "original_extra_field": [None, "  Preserve whitespace.\n"]}
    item_id = row_fingerprint(row)
    score_map = dict(zip(GATED_DIMENSIONS, scores))
    assessment = {
        "task": {"status": "matched", "decision": "Choose the requested action.",
                 "matched_facet_ids": [f"task-{task}" for task in tasks],
                 "evidence": [QUOTE], "justification": "The question requests this decision.",
                 "information_gaps": []},
        "ratings": {name: {
            "score": score_map.get(name), "evidence": [QUOTE],
            "justification": "The item supplies evidence for this finding.",
            "information_gaps": [] if score_map.get(name) is not None else ["Not established."],
        } for name in DIMENSIONS},
        "coverage": [{
            "requirement_index": index, "satisfied": value, "evidence": [QUOTE],
            "justification": "The original question supplies the relevant condition.",
            "information_gaps": ["The condition is unclear."] if value is None else [],
        } for index, value in enumerate(coverage)],
    }
    return {"item_id": item_id, "evidence_hash": item_id, "evidence": {"item": row},
            "sources": [{"benchmark": "fixture", "row": number}],
            "status": "complete", "assessment": assessment,
            "gate": gate_for(ScreeningAssessment.model_validate(assessment))}


def brute_force(requirements, items, limit, previous=()):
    """Enumerate subsets; no solver helpers or production score helpers used."""
    tasks = {facet.facet_id for facet in requirements.task_facets}
    quotas = [(index, value.minimum_items) for index, value in
              enumerate(requirements.coverage_requirements) if value.minimum_items is not None]

    def counts(subset):
        represented = set().union(*(set(item["assessment"]["task"]["matched_facet_ids"])
                                    for item in subset)) if subset else set()
        features = {index: sum(item["assessment"]["coverage"][index]["satisfied"] is True
                               for item in subset) for index, _ in quotas}
        return represented, features

    retained = [item for item in items if item["item_id"] in previous]
    old_tasks, old_features = counts(retained)
    best_key, best_ids = None, None
    for size in range(min(limit, len(items)) + 1):
        for subset in combinations(items, size):
            covered, features = counts(subset)
            if not old_tasks.issubset(covered):
                continue
            if any(features[index] < min(target, old_features[index]) for index, target in quotas):
                continue
            deficit = sum(max(0, target - features[index]) for index, target in quotas)
            quality = sum(item["assessment"]["ratings"][name]["score"]
                          for item in subset for name in GATED_DIMENSIONS)
            key = (len(tasks & covered), -deficit, quality)
            identifiers = sorted(item["item_id"] for item in subset)
            if best_key is None or key > best_key or (key == best_key and identifiers < best_ids):
                best_key, best_ids = key, identifiers
    return best_ids


@pytest.mark.parametrize("seed", range(25))
def test_small_random_pools_match_exhaustive_optimum(seed):
    rng = random.Random(seed)
    task_count = rng.randint(1, 5)
    quotas = [rng.randint(1, 3) for _ in range(rng.randint(0, 3))]
    req = requirements(task_count, quotas)
    items = [candidate(number,
                       tasks=rng.sample(range(task_count), rng.randint(1, task_count)),
                       scores=tuple(rng.randint(3, 5) for _ in range(4)),
                       coverage=[rng.choice((True, False, None)) for _ in quotas])
             for number in range(rng.randint(2, 8))]
    limit = rng.randint(1, min(4, len(items)))
    previous = [item["item_id"] for item in rng.sample(items, rng.randint(0, limit))]
    expected = brute_force(req, items, limit, previous)
    original = deepcopy(items)
    actual = selection.select_collection(req, items, limit=limit, previous_selected_ids=previous)
    assert sorted(actual["selected_item_ids"]) == expected
    assert items == original


def test_overlap_requires_joint_optimization_not_best_item_per_task():
    req = requirements(3, (1,))
    items = [candidate("best-a", (0,), (5, 5, 5, 5), (False,)),
             candidate("best-b", (1,), (5, 5, 5, 5), (False,)),
             candidate("best-c", (2,), (5, 5, 5, 5), (False,)),
             candidate("ab", (0, 1), (4, 4, 4, 4), (True,)),
             candidate("bc", (1, 2), (3, 3, 3, 3), (True,))]
    result = selection.select_collection(req, items, limit=2)
    assert set(result["selected_item_ids"]) == {items[2]["item_id"], items[3]["item_id"]}


def test_thirty_is_total_capacity_and_quality_beats_equal_task_counts():
    req = requirements()
    items = [candidate(number, (0,), (5, 5, 5, 5)) for number in range(48)]
    items += [candidate(48, (1,), (3, 3, 3, 3)), candidate(49, (2,), (3, 3, 3, 3))]
    result = selection.select_collection(req, items)
    chosen = set(result["selected_item_ids"])
    assert len(chosen) == 30
    assert {items[-2]["item_id"], items[-1]["item_id"]} <= chosen
    assert sum(item["item_id"] in chosen for item in items[:48]) == 28
    assert result["constraints_feasible"] is True and result["fully_satisfied"] is True
    assert [entry["selected_count"] for entry in result["task_coverage"]] == [28, 1, 1]
    assert result["total_quality"] == 28 * 5 + 2 * 3


@pytest.mark.parametrize("count", [0, 1, 7, 29])
def test_smaller_pools_are_not_required_to_fill_thirty(count):
    items = [candidate(number) for number in range(count)]
    result = selection.select_collection(requirements(), items)
    assert set(result["selected_item_ids"]) == {item["item_id"] for item in items}
    assert result["eligible_count"] == result["selected_count"] == count
    assert result["constraints_feasible"] is False
    assert [entry["eligible_count"] for entry in result["task_coverage"]] == [count, 0, 0]
    assert result["solver"]["fallback_used"] is True


@pytest.mark.parametrize("dimension", GATED_DIMENSIONS)
@pytest.mark.parametrize("bad_score", [2, None])
def test_recomputes_each_gate_and_does_not_trust_saved_pass(dimension, bad_score):
    good, bad = candidate("good"), candidate("bad")
    bad["assessment"]["ratings"][dimension].update(
        score=bad_score, information_gaps=["Unknown."] if bad_score is None else [])
    bad["gate"] = {"status": "pass", "reasons": ["Untrusted cached flag."]}
    good["gate"] = {"status": "fail", "reasons": ["Untrusted cached flag."]}
    result = selection.select_collection(requirements(1), [bad, good])
    assert result["selected_item_ids"] == [good["item_id"]]


@pytest.mark.parametrize("task_status", ["no_match", "unresolved"])
def test_nonmatching_and_unresolved_tasks_are_ineligible(task_status):
    item = candidate(0)
    item["assessment"]["task"].update(status=task_status, matched_facet_ids=[],
                                      information_gaps=["Unknown task."] if task_status == "unresolved" else [])
    assert selection.select_collection(requirements(1), [item])["selected_item_ids"] == []


def test_output_content_and_form_do_not_affect_selection_quality():
    low, high = candidate("higher-fit", scores=(5, 5, 5, 5)), candidate("lower-fit", scores=(4, 4, 4, 4))
    for dimension in ("output_content", "output_form"):
        low["assessment"]["ratings"][dimension].update(score=1, information_gaps=[])
        high["assessment"]["ratings"][dimension].update(score=5, information_gaps=[])
    result = selection.select_collection(requirements(1), [low, high], limit=1)
    assert result["selected_item_ids"] == [low["item_id"]]


def test_exact_rows_deduplicate_but_different_original_ids_remain_distinct():
    first, second = candidate(1), candidate(2)
    duplicate = deepcopy(first)
    duplicate["sources"] = [{"benchmark": "another", "row": 10}]
    result = selection.select_collection(requirements(1), [first, duplicate, second])
    assert set(result["selected_item_ids"]) == {first["item_id"], second["item_id"]}
    assert result["eligible_count"] == 2 and result["excluded_counts"]["duplicates"] == 1


def test_same_row_with_conflicting_assessments_is_rejected():
    original = candidate(0)
    changed = deepcopy(original)
    changed["assessment"]["ratings"]["input_content"]["score"] = 5
    with pytest.raises(ValueError):
        selection.select_collection(requirements(1), [original, changed])


@pytest.mark.parametrize("corruption", ["item_id", "evidence_hash", "row"])
def test_full_original_row_identity_is_verified(corruption):
    item = candidate(0)
    if corruption == "row":
        item["evidence"]["item"]["original_extra_field"] = "Changed but same question."
    else:
        item[corruption] = "not-the-row-fingerprint"
    with pytest.raises(ValueError):
        selection.select_collection(requirements(1), [item])


def test_only_true_coverage_can_satisfy_an_explicit_minimum():
    items = [candidate("false", scores=(5, 5, 5, 5), coverage=(False,)),
             candidate("unknown", scores=(5, 5, 5, 5), coverage=(None,)),
             candidate("true", scores=(3, 3, 3, 3), coverage=(True,))]
    result = selection.select_collection(requirements(1, (1,)), items, limit=1)
    assert result["selected_item_ids"] == [items[-1]["item_id"]]
    assert result["quota_coverage"] == [{"requirement_index": 0, "minimum_items": 1,
                                        "eligible_count": 1, "selected_count": 1, "shortfall": 0}]


def test_missing_minimum_is_not_invented_as_a_hard_quota():
    items = [candidate("false", scores=(5, 5, 5, 5), coverage=(False,)),
             candidate("true", scores=(3, 3, 3, 3), coverage=(True,))]
    result = selection.select_collection(requirements(1, (None,)), items, limit=1)
    assert result["selected_item_ids"] == [items[0]["item_id"]]
    assert result["constraints_feasible"] is True and result["fully_satisfied"] is False
    assert result["unresolved_requirement_indices"] == [0]
    assert result["quota_coverage"][0]["shortfall"] is None
    assert result["gaps"]


def test_infeasible_fallback_prioritizes_task_count_then_quota_deficit_then_quality():
    req = requirements(4, (2, 1))
    items = [candidate("high-single", (0,), (5, 5, 5, 5), (True, True)),
             candidate("three-no-features", (0, 1, 2), (5, 5, 5, 5), (False, False)),
             candidate("three-one-feature", (0, 1, 2), (4, 4, 4, 4), (True, False)),
             candidate("three-two-features", (0, 1, 2), (3, 3, 3, 3), (True, True))]
    result = selection.select_collection(req, items, limit=1)
    assert result["selected_item_ids"] == [items[3]["item_id"]]
    assert result["constraints_feasible"] is False
    assert [entry["shortfall"] for entry in result["task_coverage"]] == [0, 0, 0, 1]
    assert [entry["shortfall"] for entry in result["quota_coverage"]] == [1, 0]


def test_previous_coverage_survives_replacement_without_locking_old_items():
    req = requirements(3, (2,))
    old = [candidate("old-a", (0,), (3, 3, 3, 3), (True,)),
           candidate("old-b", (1,), (3, 3, 3, 3), (True,))]
    new = [candidate("new-a", (0,), (4, 4, 4, 4), (True,)),
           candidate("new-b", (1,), (4, 4, 4, 4), (True,)),
           candidate("new-c", (2,), (5, 5, 5, 5), (False,))]
    result = selection.select_collection(req, old + new, limit=2,
                                         previous_selected_ids=[item["item_id"] for item in old])
    assert set(result["selected_item_ids"]) == {new[0]["item_id"], new[1]["item_id"]}
    assert result["preserved_coverage"] == {
        "tasks": [{"facet_id": "task-0", "minimum": 1}, {"facet_id": "task-1", "minimum": 1}],
        "quotas": [{"requirement_index": 0, "minimum": 2}],
    }


def test_previous_feature_counts_are_capped_at_the_required_minimum():
    req = requirements(1, (1,))
    old = [candidate(f"old-{number}", coverage=(True,), scores=(3, 3, 3, 3)) for number in range(2)]
    high = candidate("higher", coverage=(False,), scores=(5, 5, 5, 5))
    result = selection.select_collection(req, old + [high], limit=2,
                                         previous_selected_ids=[item["item_id"] for item in old])
    assert high["item_id"] in result["selected_item_ids"]
    assert len(result["selected_item_ids"]) == 2


def test_exact_lexicographic_tie_break_handles_equal_sums_of_id_ranks():
    items = sorted([candidate(number) for number in range(4)], key=lambda item: item["item_id"])
    for item, tasks in zip(items, ((0, 2), (0, 3), (1, 2), (1, 3))):
        item["assessment"]["task"]["matched_facet_ids"] = [f"task-{task}" for task in tasks]
    req = requirements(4)
    expected = [items[0]["item_id"], items[3]["item_id"]]
    assert selection.select_collection(req, items, limit=2)["selected_item_ids"] == expected
    assert selection.select_collection(req, list(reversed(items)), limit=2)["selected_item_ids"] == expected


def test_solver_timeout_is_not_reported_as_proven_infeasibility(monkeypatch):
    monkeypatch.setattr(selection, "milp", lambda *args, **kwargs: SimpleNamespace(
        status=1, success=False, x=None, message="Time limit reached."))
    with pytest.raises(selection.SelectionIncomplete):
        selection.select_collection(requirements(1), [candidate(0)])


def test_timeout_during_tie_break_does_not_publish_earlier_solver_result(monkeypatch):
    real_milp = selection.milp
    calls = []

    def interrupt_later(*args, **kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            return real_milp(*args, **kwargs)
        return SimpleNamespace(status=1, success=False, x=None, message="Tie-break time limit.")

    monkeypatch.setattr(selection, "milp", interrupt_later)
    with pytest.raises(selection.SelectionIncomplete):
        selection.select_collection(requirements(1), [candidate(0), candidate(1)], limit=1)
    assert len(calls) == 2


def test_cancellation_stops_before_returning_a_selection():
    with pytest.raises(InterruptedError):
        selection.select_collection(requirements(1), [candidate(0)], cancelled=lambda: True)


def test_cancellation_during_solver_prevents_accepting_its_result(monkeypatch):
    real_milp = selection.milp
    cancelled = False

    def solve_then_cancel(*args, **kwargs):
        nonlocal cancelled
        result = real_milp(*args, **kwargs)
        cancelled = True
        return result

    monkeypatch.setattr(selection, "milp", solve_then_cancel)
    with pytest.raises(InterruptedError):
        selection.select_collection(requirements(1), [candidate(0)], cancelled=lambda: cancelled)


def test_errors_failures_and_unknowns_have_separate_exclusion_counts():
    failed = candidate("failed", scores=(2, 5, 5, 5))
    unknown = candidate("unknown", scores=(None, 5, 5, 5))
    error = {"item_id": "unscreened-error", "status": "error", "error": "No accepted assessment."}
    good = candidate("good")
    result = selection.select_collection(requirements(1), [failed, unknown, error, good])
    assert result["selected_item_ids"] == [good["item_id"]]
    assert result["excluded_counts"] == {"errors": 1, "gate_fail": 1, "gate_unresolved": 1, "duplicates": 0}


def test_condition_cannot_claim_true_for_an_unmatched_task():
    req = requirements(2, (1,))
    req.coverage_requirements[0].facet_ids = ["task-1"]
    with pytest.raises(ValueError):
        selection.select_collection(req, [candidate(0, tasks=(0,), coverage=(True,))])


def test_tasks_available_but_joint_coverage_exceeds_capacity():
    req = requirements(3)
    items = [candidate(number, tasks=(number,)) for number in range(3)]
    result = selection.select_collection(req, items, limit=2)
    assert len(result["selected_item_ids"]) == 2
    assert [entry["eligible_count"] for entry in result["task_coverage"]] == [1, 1, 1]
    assert sum(entry["shortfall"] for entry in result["task_coverage"]) == 1
    assert result["constraints_feasible"] is False and result["gaps"]


@pytest.mark.parametrize("limit", [True, 0, -1, 31, 1.5, "30"])
def test_invalid_collection_limits_are_rejected(limit):
    with pytest.raises(ValueError):
        selection.select_collection(requirements(1), [candidate(0)], limit=limit)


@pytest.mark.parametrize("time_limit", [True, 0, -1, float("inf"), float("nan"), "30"])
def test_invalid_solver_deadlines_are_rejected(time_limit):
    with pytest.raises(ValueError):
        selection.select_collection(requirements(1), [candidate(0)], time_limit=time_limit)


def test_previous_selection_must_reference_unique_eligible_items():
    item = candidate(0)
    for previous in (["unknown"], [item["item_id"], item["item_id"]]):
        with pytest.raises(ValueError):
            selection.select_collection(requirements(1), [item], previous_selected_ids=previous)
