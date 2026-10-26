"""Allocate the initial screening budget across existing task rankings."""

from .benchmark_queries import ScreeningQueues


INITIAL_SCREENING_BUDGET = 48


def allocate_initial_screening(queues: list[dict], budget: int = INITIAL_SCREENING_BUDGET) -> dict:
    """Take distinct items fairly from all-source queues without changing them.

    Each pass takes one next unseen item per task, in the supplied queue order.
    A task with no remaining unseen items drops out, allowing the others to use
    its share. Targets describe the initial even split; actual counts record the
    allocation after overlaps and exhausted queues have been handled.
    """
    if type(budget) is not int or budget < 0:
        raise ValueError("The screening budget must be a nonnegative integer.")
    if not isinstance(queues, list):
        raise ValueError("Screening allocation requires a list of queues.")
    all_source, facets = [], set()
    for queue in queues:
        if not isinstance(queue, dict) or "source" not in queue:
            raise ValueError("Each screening queue must identify its source scope.")
        if queue["source"] is not None:
            continue
        facet_id = queue.get("facet_id")
        if not isinstance(facet_id, str) or not facet_id.strip():
            raise ValueError("An all-source queue requires a nonempty task facet identifier.")
        if facet_id in facets:
            raise ValueError("Each task facet may have only one all-source queue.")
        facets.add(facet_id)
        all_source.append(queue)
    reader = ScreeningQueues(all_source)
    each, remainder = divmod(budget, len(all_source)) if all_source else (0, 0)
    allocations = [{"queue_id": queue["queue_id"], "facet_id": queue["facet_id"],
                    "target": each + (number < remainder), "allocated": 0}
                   for number, queue in enumerate(all_source)]
    items, seen = [], set()
    active = list(range(len(all_source)))
    while len(items) < budget and active:
        remaining = []
        for number in active:
            allocation = allocations[number]
            selected = reader.take(allocation["queue_id"], 1, seen)
            if not selected:
                continue
            item_id = selected[0]
            seen.add(item_id)
            allocation["allocated"] += 1
            items.append({"item_id": item_id, "queue_id": allocation["queue_id"],
                          "facet_id": allocation["facet_id"]})
            remaining.append(number)
            if len(items) == budget:
                break
        active = remaining
    return {"budget": budget, "allocated": len(items), "shortfall": budget - len(items),
            "allocations": allocations, "items": items}
