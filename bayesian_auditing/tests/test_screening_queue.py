"""Initial screening allocation is deterministic, fair, and globally distinct."""

from copy import deepcopy

import pytest

from bayesian_auditing.screening_queue import INITIAL_SCREENING_BUDGET, allocate_initial_screening


def queue(facet_id, item_ids, *, source=None, queue_id=None):
    return {"queue_id": queue_id or f"queue-{facet_id}-{source}", "facet_id": facet_id,
            "source": source, "item_ids": item_ids}


def test_fifty_candidates_split_17_17_16_in_existing_task_order():
    queues = [queue(task, [f"{task}-{number}" for number in range(30)])
              for task in ("management", "diagnosis", "investigation")]
    result = allocate_initial_screening(queues)
    assert INITIAL_SCREENING_BUDGET == result["budget"] == result["allocated"] == 50
    assert result["shortfall"] == 0
    assert [row["target"] for row in result["allocations"]] == [17, 17, 16]
    assert [row["allocated"] for row in result["allocations"]] == [17, 17, 16]
    assert [item["item_id"] for item in result["items"][:6]] == [
        "management-0", "diagnosis-0", "investigation-0",
        "management-1", "diagnosis-1", "investigation-1",
    ]
    for original in queues:
        selected = [item["item_id"] for item in result["items"] if item["queue_id"] == original["queue_id"]]
        assert selected == original["item_ids"][:len(selected)]


def test_overlapping_items_are_skipped_globally_without_losing_queue_turns():
    queues = [queue("first", ["shared", "first-only", "shared-later"]),
              queue("second", ["shared", "second-only", "shared-later", "last"])]
    result = allocate_initial_screening(queues, budget=5)
    assert [item["item_id"] for item in result["items"]] == [
        "shared", "second-only", "first-only", "shared-later", "last",
    ]
    assert [item["facet_id"] for item in result["items"]] == ["first", "second", "first", "second", "second"]
    assert [row["target"] for row in result["allocations"]] == [3, 2]
    assert [row["allocated"] for row in result["allocations"]] == [2, 3]
    assert result["allocated"] == 5 and result["shortfall"] == 0


def test_exhausted_queue_share_is_redistributed_to_remaining_tasks():
    queues = [queue("short", ["only"]), queue("second", [f"b-{i}" for i in range(50)]),
              queue("third", [f"c-{i}" for i in range(50)])]
    result = allocate_initial_screening(queues)
    assert [row["target"] for row in result["allocations"]] == [17, 17, 16]
    assert [row["allocated"] for row in result["allocations"]] == [1, 25, 24]
    assert result["allocated"] == 50 and result["shortfall"] == 0


def test_union_smaller_than_budget_reports_shortfall_and_empty_tasks():
    queues = [queue("empty", []), queue("first", ["shared", "one"]),
              queue("second", ["shared", "two"])]
    result = allocate_initial_screening(queues)
    assert result["allocated"] == 3 and result["shortfall"] == 47
    assert [item["item_id"] for item in result["items"]] == ["shared", "two", "one"]
    assert [row["allocated"] for row in result["allocations"]] == [0, 2, 1]


def test_more_tasks_than_budget_preserves_order_and_stops_at_fifty():
    queues = [queue(f"task-{i}", [f"item-{i}"]) for i in range(60)]
    result = allocate_initial_screening(queues)
    assert result["allocated"] == 50
    assert [row["target"] for row in result["allocations"]] == [1] * 50 + [0] * 10
    assert [row["allocated"] for row in result["allocations"]] == [1] * 50 + [0] * 10
    assert [item["item_id"] for item in result["items"]] == [f"item-{i}" for i in range(50)]


def test_source_queues_do_not_change_task_allocations_or_supply_extra_items():
    global_queues = [queue("first", ["one", "two"]), queue("second", ["three"])]
    mixed = [queue("first", ["source-only"], source="benchmark-a"), global_queues[0],
             queue("second", ["other-source-only"], source="benchmark-b"), global_queues[1]]
    assert allocate_initial_screening(mixed) == allocate_initial_screening(global_queues)


def test_allocation_is_deterministic_and_preserves_inputs():
    queues = [queue("first", ["same", "one"]), queue("second", ["same", "two"])]
    before = deepcopy(queues)
    first = allocate_initial_screening(queues)
    assert first == allocate_initial_screening(deepcopy(queues))
    assert queues == before
    first["items"][0]["item_id"] = "changed result"
    first["allocations"][0]["facet_id"] = "changed result"
    assert queues == before


@pytest.mark.parametrize("queues", [[], [queue("source-only", ["one"], source="benchmark")]])
def test_no_all_source_queues_reports_entire_shortfall(queues):
    assert allocate_initial_screening(queues) == {
        "budget": 50, "allocated": 0, "shortfall": 50, "allocations": [], "items": [],
    }


def test_zero_budget_returns_empty_allocation_with_zero_targets():
    result = allocate_initial_screening([queue("task", ["one"])], budget=0)
    assert result["budget"] == result["allocated"] == result["shortfall"] == 0
    assert result["allocations"][0]["target"] == result["allocations"][0]["allocated"] == 0
    assert result["items"] == []


@pytest.mark.parametrize("budget", [-1, 1.5, True, "50", None])
def test_invalid_budgets_fail_clearly(budget):
    with pytest.raises(ValueError, match="budget"):
        allocate_initial_screening([], budget)


@pytest.mark.parametrize("queues", [
    None, [None], [{"facet_id": "task"}],
    [queue("", ["one"])], [queue("task", ["one"], queue_id=" ")],
    [queue("same-facet", ["one"]), queue("same-facet", ["two"], queue_id="different-queue")],
    [queue("first", ["one"], queue_id="same-queue"), queue("second", ["two"], queue_id="same-queue")],
    [queue("task", ["same", "same"])], [queue("task", [""])], [queue("task", [7])],
    [queue("task", "not a list")],
])
def test_malformed_global_queues_fail_instead_of_changing_allocations(queues):
    with pytest.raises(ValueError):
        allocate_initial_screening(queues)
