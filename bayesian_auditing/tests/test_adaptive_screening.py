"""Adaptive decisions checked against concrete yield and coverage examples."""

from collections import Counter
from copy import deepcopy
import random

import pytest

from bayesian_auditing import adaptive_screening as adaptive
from bayesian_auditing.benchmark_data import row_fingerprint
from bayesian_auditing.requirements import Requirements
from bayesian_auditing.scoring import DIMENSIONS


def requirements(facets=("diagnosis", "investigation", "management"), quotas=()):
    def supported(text):
        return {"text": text, "evidence": [{"answer_id": "success", "quote": text}]}

    return Requirements.model_validate({
        **{key: supported("Answer questions.") for key in
           ("workflow", "primary_user", "input_types", "output_types", "authority")},
        "task_facets": [{"facet_id": facet, "task": supported(facet),
                         "required_input_evidence": supported("A question."),
                         "required_output_behavior": supported("An answer."), "essential": True}
                        for facet in facets],
        "coverage_requirements": [{"facet_ids": scope, "minimum_items": minimum,
                                   "requirement": supported(f"Requirement {index}.")}
                                  for index, (scope, minimum) in enumerate(quotas)],
        "unresolved_details": [],
    })


def queue(facet, ids, source=None, queue_id=None):
    return {"queue_id": queue_id or f"{facet}:{source or 'all'}", "facet_id": facet,
            "source": source, "item_ids": list(ids)}


def selection(req, tasks=None, quotas=None):
    tasks = tasks or {}
    quotas = quotas or {}
    return {"task_coverage": [{"facet_id": facet.facet_id,
                               "selected_count": tasks.get(facet.facet_id, 0)}
                              for facet in req.task_facets],
            "quota_coverage": [{"requirement_index": index, "selected_count": quotas.get(index, 0)}
                               for index in range(len(req.coverage_requirements))]}


def outcome(item_id, facet="diagnosis", retained=True, sources=()):
    return {"item_id": item_id, "facet_id": facet, "retained": retained, "source_names": list(sources)}


def choose(req, queues, *, selected=None, outcomes=(), seen=(), seed=1, decision_index=0, limit=160):
    return adaptive.choose_batch(req, queues, selected or selection(req), list(outcomes), set(seen),
                                 seed=seed, decision_index=decision_index, limit=limit)


def screened(number=0, *, sources=("benchmark-a",), score=4):
    text = "Choose the requested treatment."
    row = {"id": number, "content": text, "answer": "The appropriate treatment."}
    key = row_fingerprint(row)
    return {"item_id": key, "evidence_hash": key, "evidence": {"item": row},
            "sources": [{"benchmark": name, "row": number} for name in sources],
            "status": "complete", "assessment": {
                "task": {"status": "matched", "matched_facet_ids": ["management"],
                         "decision": "Choose treatment.", "evidence": [text],
                         "justification": "Treatment is requested.", "information_gaps": []},
                "ratings": {dimension: {"score": score, "evidence": [text],
                                         "justification": "The question supplies the evidence.",
                                         "information_gaps": []} for dimension in DIMENSIONS},
                "coverage": [],
            }}


def test_two_of_eight_retained_produces_beta_three_seven_and_accumulates():
    ids = [f"item-{number}" for number in range(12)]
    queues = [queue("diagnosis", ids)]
    first = [outcome(key, retained=index < 2) for index, key in enumerate(ids[:8])]
    stats = adaptive.queue_statistics(queues, first)[0]
    assert (stats["successes"], stats["failures"], stats["alpha"], stats["beta"]) == (2, 6, 3, 7)
    assert stats["estimated_yield"] == 0.3
    second = first + [outcome(key, retained=index < 3) for index, key in enumerate(ids[8:])]
    stats = adaptive.queue_statistics(queues, second)[0]
    assert (stats["alpha"], stats["beta"], stats["estimated_yield"]) == (6, 8, 6 / 14)
    assert adaptive.queue_statistics(queues, [])[0]["estimated_yield"] == 0.5


def test_shared_source_row_credits_each_acquisition_queue_once_and_no_other_task():
    queues = [queue(task, ["shared", "later"], source)
              for task in ("diagnosis", "management") for source in (None, "a", "b")]
    rows = adaptive.queue_statistics(queues, [outcome("shared", sources=("a", "b"))])
    assert [(row["successes"], row["failures"]) for row in rows if row["facet_id"] == "diagnosis"] == [(1, 0)] * 3
    assert [(row["successes"], row["failures"]) for row in rows if row["facet_id"] == "management"] == [(0, 0)] * 3


def test_coverage_bonus_can_outweigh_better_yield():
    req = requirements()
    queues, history, seen = [], [], set()
    for facet, successes, failures in [("diagnosis", 1, 7), ("investigation", 6, 12), ("management", 2, 6)]:
        observed = [f"{facet}-{index}" for index in range(successes + failures)]
        queues.append(queue(facet, [*observed, f"{facet}-next"]))
        history += [outcome(key, facet, index < successes) for index, key in enumerate(observed)]
        seen.update(observed)
    result = choose(req, queues, selected=selection(req, {"investigation": 1, "management": 1}),
                    outcomes=history, seen=seen)
    assert result["exploration"] is False
    assert result["facet_id"] == "diagnosis"
    assert [(row["estimated_yield"], row["coverage_weight"], row["priority"])
            for row in result["priorities"]] == [(0.2, 2, 0.4), (0.35, 1, 0.35), (0.3, 1, 0.3)]
    assert result["item_ids"] == ["diagnosis-next"]


def test_conditional_quota_uses_qualifying_count_not_total_task_count():
    req = requirements(quotas=[(["management"], 3)])
    queues = [queue(facet.facet_id, [facet.facet_id]) for facet in req.task_facets]
    result = choose(req, queues, selected=selection(req, {"diagnosis": 1, "investigation": 1,
                                                       "management": 20}, {0: 1}))
    weights = {row["facet_id"]: row["coverage_weight"] for row in result["priorities"]}
    assert weights == {"diagnosis": 1, "investigation": 1, "management": pytest.approx(5 / 3)}
    assert result["facet_id"] == "management"


def test_largest_deficit_including_global_quotas_applies_without_adding_bonuses():
    req = requirements(quotas=[([], 4), (["management"], 10), (["management"], None),
                              (["diagnosis", "investigation"], 2)])
    queues = [queue(facet.facet_id, [facet.facet_id]) for facet in req.task_facets]
    result = choose(req, queues, selected=selection(req, {"diagnosis": 1, "investigation": 1,
                                                        "management": 1}, {0: 3, 1: 6, 2: 0, 3: 1}))
    assert {row["facet_id"]: row["coverage_weight"] for row in result["priorities"]} == {
        "diagnosis": 1.5, "investigation": 1.5, "management": 1.4}


def test_uncovered_task_has_full_bonus_and_met_quotas_have_no_negative_bonus():
    req = requirements(("diagnosis", "management"), quotas=[([], 1)])
    queues = [queue("diagnosis", ["a"]), queue("management", ["b"])]
    result = choose(req, queues, selected=selection(req, {"management": 5}, {0: 9}))
    assert [row["coverage_weight"] for row in result["priorities"]] == [2, 1]


def test_batch_is_eight_from_saved_ranking_and_skips_all_globally_seen_items():
    req = requirements(("diagnosis", "management"))
    ranked = [f"item-{index}" for index in range(16)]
    queues = [queue("diagnosis", ranked), queue("management", ranked[::2], "a"),
              queue("management", ranked[::2])]
    seen = {"item-0", "item-1", "item-3", "item-10"}
    before = deepcopy((queues, seen))
    result = choose(req, queues, seen=seen)
    assert result["item_ids"] == ["item-2", "item-4", "item-5", "item-6", "item-7", "item-8", "item-9", "item-11"]
    assert result["priorities"][0]["remaining"] == 12
    assert (queues, seen) == before


@pytest.mark.parametrize("limit, expected_sizes", [(160, [8] * 14), (159, [8] * 13 + [7])])
def test_total_budget_includes_initial_48_and_final_batch_can_be_short(limit, expected_sizes):
    req = requirements(("diagnosis",))
    queues = [queue("diagnosis", [f"item-{index}" for index in range(200)])]
    seen = {f"item-{index}" for index in range(48)}
    sizes = []
    for decision in range(20):
        batch = choose(req, queues, seen=seen, decision_index=decision, limit=limit)
        if batch is None:
            break
        assert not seen.intersection(batch["item_ids"])
        seen.update(batch["item_ids"])
        sizes.append(len(batch["item_ids"]))
    assert sizes == expected_sizes
    assert len(seen) == limit


def test_exhausted_queues_do_not_receive_exploration_probability():
    req = requirements(("diagnosis", "management"))
    queues = [queue("diagnosis", ["seen"]), queue("management", ["new"])]
    result = choose(req, queues, seen={"seen"}, seed=0)
    assert result["exploration"] is True
    assert result["facet_id"] == "management"
    assert len(result["priorities"]) == 1
    assert choose(req, queues, seen={"seen", "new"}) is None


def test_current_priority_report_includes_exhausted_queues_without_making_them_available():
    req = requirements(("diagnosis", "management"))
    queues = [queue("diagnosis", ["seen"]), queue("management", ["new"])]
    history = [outcome("seen")]
    rows = adaptive.queue_priorities(req, queues, selection(req), history, {"seen"})
    assert [row["remaining"] for row in rows] == [0, 1]
    assert [row["priority"] for row in rows] == [pytest.approx(4 / 3), 1]
    decision = choose(req, queues, outcomes=history, seen={"seen"})
    assert decision["facet_id"] == "management"
    assert decision["priorities"] == [rows[1]]


def test_current_priorities_recompute_coverage_after_collection_changes():
    req = requirements(("diagnosis", "management"), quotas=[(["management"], 3)])
    queues = [queue("diagnosis", ["a"]), queue("management", ["b"])]
    first = adaptive.queue_priorities(req, queues, selection(req), [], set())
    current = adaptive.queue_priorities(req, queues,
                                        selection(req, {"diagnosis": 1, "management": 3}, {0: 2}), [], set())
    assert [row["coverage_weight"] for row in first] == [2, 2]
    assert [row["coverage_weight"] for row in current] == [1, pytest.approx(4 / 3)]
    assert [row["estimated_yield"] for row in first] == [row["estimated_yield"] for row in current]


def test_empty_tasks_have_no_batch():
    req = requirements(())
    assert choose(req, []) is None


def test_greedy_tie_is_queue_id_order_and_exploration_is_uniform():
    req = requirements(("diagnosis", "investigation", "management"))
    queues = [queue(facet.facet_id, [facet.facet_id], queue_id=f"queue-{index}")
              for index, facet in enumerate(req.task_facets)]
    decisions = [choose(req, queues, decision_index=index) for index in range(3000)]
    greedy = [row for row in decisions if not row["exploration"]]
    exploring = [row for row in decisions if row["exploration"]]
    assert all(row["queue_id"] == "queue-0" for row in greedy)
    assert 540 < len(exploring) < 660  # Seeded empirical probability near 20%.
    counts = Counter(row["queue_id"] for row in exploring)
    assert set(counts) == {"queue-0", "queue-1", "queue-2"}
    assert all(150 < count < 250 for count in counts.values())


def test_saved_seed_index_reproduce_choice_across_resume_and_queue_reordering():
    req = requirements()
    queues = [queue(facet.facet_id, [facet.facet_id]) for facet in req.task_facets]
    original = deepcopy((req, queues))
    random.seed(99)
    global_state = random.getstate()
    first = choose(req, queues, seed=97, decision_index=12)
    choose(req, queues, seed=97, decision_index=13)
    assert choose(req, list(reversed(queues)), seed=97, decision_index=12) == first
    assert random.getstate() == global_state
    assert (req, queues) == original


def test_outcomes_use_retention_instead_of_gate_pass_and_keep_original_history():
    records = [screened(index) for index in range(3)]
    acquired = [{"item_id": row["item_id"], "facet_id": "diagnosis"} for row in records]
    first = adaptive.make_outcomes(acquired[:2], records, [records[0]["item_id"]])
    assert [row["retained"] for row in first] == [True, False]
    assert all(row["facet_id"] == "diagnosis" for row in first)  # Matched facet was management.
    second = adaptive.make_outcomes(acquired[2:], records, [records[2]["item_id"]])
    assert first[0]["retained"] is True  # A later replacement does not rewrite history.
    queues = [queue("diagnosis", [row["item_id"] for row in records], source)
              for source in (None, "benchmark-a")]
    stats = adaptive.queue_statistics(queues, first + second)
    assert all((row["successes"], row["failures"]) == (2, 1) for row in stats)


def test_physical_source_duplicates_collapse_to_names_and_inputs_remain_unchanged():
    record = screened(sources=("b", "a", "b", "a"))
    acquired = [{"item_id": record["item_id"], "facet_id": "management"}]
    before = deepcopy((record, acquired))
    result = adaptive.make_outcomes(acquired, [record], [record["item_id"]])
    assert result[0]["source_names"] == ["a", "b"]
    assert (record, acquired) == before
    result[0]["source_names"].append("modified")
    assert (record, acquired) == before


@pytest.mark.parametrize("status", ["error", "pending", None])
def test_invalid_or_incomplete_responses_are_not_recorded_as_failures(status):
    record = screened()
    record["status"] = status
    with pytest.raises(ValueError, match="complete assessment"):
        adaptive.make_outcomes([{"item_id": record["item_id"], "facet_id": "diagnosis"}], [record], [])


def test_missing_response_prevents_partial_batch_commit():
    record = screened()
    with pytest.raises(ValueError, match="complete assessment"):
        adaptive.make_outcomes([{"item_id": record["item_id"], "facet_id": "diagnosis"},
                                {"item_id": "missing", "facet_id": "diagnosis"}], [record], [])


@pytest.mark.parametrize("mutation", [
    lambda row: row["evidence"]["item"].update(content="A modified row."),
    lambda row: row.update(evidence_hash="wrong"),
    lambda row: row.update(assessment={}),
    lambda row: row.update(sources=[{"benchmark": ""}]),
    lambda row: row.update(sources="not a list"),
])
def test_corrupt_outcome_inputs_are_rejected(mutation):
    record = screened()
    mutation(record)
    with pytest.raises(ValueError):
        adaptive.make_outcomes([{"item_id": record["item_id"], "facet_id": "diagnosis"}], [record], [])


def test_gate_failure_can_be_a_failure_but_never_a_retention_success():
    record = screened(score=2)
    acquired = [{"item_id": record["item_id"], "facet_id": "diagnosis"}]
    assert adaptive.make_outcomes(acquired, [record], [])[0]["retained"] is False
    with pytest.raises(ValueError, match="eligibility gate"):
        adaptive.make_outcomes(acquired, [record], [record["item_id"]])


@pytest.mark.parametrize("duplicate", ["acquisitions", "records", "selected"])
def test_duplicate_inputs_cannot_commit_multiple_outcomes(duplicate):
    record = screened()
    acquired = [{"item_id": record["item_id"], "facet_id": "diagnosis"}]
    records, selected = [record], [record["item_id"]]
    if duplicate == "acquisitions":
        acquired *= 2
    elif duplicate == "records":
        records *= 2
    else:
        selected *= 2
    with pytest.raises(ValueError):
        adaptive.make_outcomes(acquired, records, selected)


@pytest.mark.parametrize("history", [
    [outcome("item"), outcome("item")],
    [outcome("item", retained=1)],
    [outcome("item", facet="unknown")],
    [outcome("item", sources=("wrong",))],
    [outcome("item", sources=("a", "a"))],
    [outcome("unknown")], [None], None,
])
def test_invalid_history_cannot_change_posteriors(history):
    with pytest.raises(ValueError):
        adaptive.queue_statistics([queue("diagnosis", ["item"])], history)


@pytest.mark.parametrize("kwargs", [{"seed": -1}, {"seed": True}, {"seed": 2**32},
                                    {"decision_index": -1}, {"decision_index": 1.5},
                                    {"limit": 161}, {"limit": 0}, {"limit": True}])
def test_invalid_policy_parameters_are_rejected(kwargs):
    req = requirements(("diagnosis",))
    with pytest.raises(ValueError):
        choose(req, [queue("diagnosis", ["item"])], **kwargs)


def test_history_requires_seen_ids_and_unknown_facets_are_rejected():
    req = requirements(("diagnosis",))
    with pytest.raises(ValueError, match="already be counted as seen"):
        choose(req, [queue("diagnosis", ["item", "next"])], outcomes=[outcome("item")])
    with pytest.raises(ValueError, match="exactly the extracted"):
        choose(req, [queue("management", ["item"])])


@pytest.mark.parametrize("bad_selection", [
    {}, {"task_coverage": [], "quota_coverage": []},
    {"task_coverage": [{"facet_id": "diagnosis", "selected_count": -1}], "quota_coverage": []},
    {"task_coverage": [{"facet_id": "diagnosis", "selected_count": True}], "quota_coverage": []},
    {"task_coverage": [{"facet_id": [], "selected_count": 1}], "quota_coverage": []},
])
def test_missing_or_malformed_coverage_cannot_silently_change_priority(bad_selection):
    req = requirements(("diagnosis",))
    with pytest.raises(ValueError):
        adaptive.choose_batch(req, [queue("diagnosis", ["item"])], bad_selection, [], set(),
                              seed=1, decision_index=0)


@pytest.mark.parametrize("queues", [
    None, [None], [queue("diagnosis", ["item"], "a")],
    [queue("diagnosis", ["item"]), queue("diagnosis", ["different"], "a")],
    [queue("diagnosis", ["item"]), queue("diagnosis", ["item"], queue_id="other")],
    [queue("diagnosis", ["item", "item"])], [queue("", ["item"])],
])
def test_malformed_queue_membership_is_rejected(queues):
    with pytest.raises(ValueError):
        adaptive.queue_statistics(queues, [])
