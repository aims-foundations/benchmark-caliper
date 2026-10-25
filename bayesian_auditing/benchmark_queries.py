"""Build benchmark queries and screening queues from validated earlier steps.

O*NET contributes only the vocabulary adopted for an existing task. Retrieval
determines the order of later screening; it does not select benchmark members.
"""

import json

from .onet_mapping import OnetMapping
from .requirements import Requirements


def build_benchmark_queries(answers: dict[str, str], requirements: Requirements,
                            grounding: dict) -> list[dict]:
    """Return one deterministic query per task without changing its requirements.

    Validate every facet mapping before returning any queries. This includes
    rejected records: an invalid saved mapping must be repaired, not partially
    reused. Unknown requirement fields are omitted from the search text.
    """
    requirements.validate_evidence(answers)
    facets = {facet.facet_id: facet for facet in requirements.task_facets}
    grounded = grounding.get("facets")
    if not isinstance(grounded, list):
        raise ValueError("O*NET grounding must contain a list of facet mappings.")
    mappings = {}
    for entry in grounded:
        if not isinstance(entry, dict):
            raise ValueError("Each O*NET grounding entry must describe a task facet.")
        facet_id = entry.get("facet_id")
        if not isinstance(facet_id, str) or facet_id not in facets:
            raise ValueError("O*NET grounding references an unknown task facet.")
        if facet_id in mappings:
            raise ValueError("O*NET grounding repeats a task facet.")
        if entry.get("status") != "complete":
            raise ValueError("Every O*NET facet mapping must be complete before benchmark retrieval.")
        candidates = entry.get("candidates")
        if not isinstance(candidates, list) or any(not isinstance(row, dict) for row in candidates):
            raise ValueError("An O*NET facet mapping must retain its retrieved candidates.")
        mapping = OnetMapping.model_validate(entry.get("mapping"))
        mapping.validate_context(answers, facets[facet_id], candidates)
        mappings[facet_id] = mapping
    if set(mappings) != set(facets):
        raise ValueError("Every extracted task requires a completed O*NET mapping before benchmark retrieval.")

    queries = []
    for facet in requirements.task_facets:
        mapping = mappings[facet.facet_id]
        adopted = [record for record in mapping.records
                   if record.applicability in {"applicable", "partially_applicable"}]
        # Keep the supplied spelling and order, removing only identical terms.
        terms = list(dict.fromkeys(term for record in adopted for term in record.search_terms))
        fields = [
            ("Task", facet.task),
            ("Required input evidence", facet.required_input_evidence),
            ("Required output behavior", facet.required_output_behavior),
            ("Workflow", requirements.workflow),
            ("Users and context", requirements.primary_user),
            ("Input types", requirements.input_types),
            ("Output types", requirements.output_types),
            ("Authority and constraints", requirements.authority),
        ]
        lines = [f"{label}: {value.text}" for label, value in fields if value.text is not None]
        if terms:
            lines.append("O*NET search vocabulary: " + "; ".join(terms))
        for refinement in mapping.refinements:
            lines.append(f"Goal-grounded refinement: {refinement.text}")
        queries.append({
            "facet_id": facet.facet_id,
            "query": "\n".join(lines),
            "onet_record_ids": [record.record_id for record in adopted],
            "search_terms": terms,
            "refinements": [refinement.model_dump() for refinement in mapping.refinements],
        })
    return queries


def _queue_id(facet_id: str, source: str | None) -> str:
    # A JSON pair distinguishes global queues from literal source names and
    # remains unambiguous even when identifiers contain punctuation or Unicode.
    return json.dumps([facet_id, source], ensure_ascii=False, separators=(",", ":"))


def build_screening_queues(rankings: list[dict]) -> list[dict]:
    """Keep each facet's ranking and its per-benchmark subsequences as queues.

    Input candidate lists are already in retrieval order. Evidence shared across
    benchmarks remains in each relevant queue, once per queue, under the same
    item identifier. Source queues follow their first appearance in the ranking.
    """
    queues, seen_facets = [], set()
    for ranking in rankings:
        facet_id = ranking.get("facet_id")
        if not isinstance(facet_id, str) or not facet_id.strip():
            raise ValueError("A benchmark ranking requires a nonempty task facet identifier.")
        if facet_id in seen_facets:
            raise ValueError("Benchmark rankings must not repeat task facets.")
        seen_facets.add(facet_id)
        candidates = ranking.get("candidates")
        if not isinstance(candidates, list):
            raise ValueError("A benchmark ranking requires a candidate list.")
        all_items, by_source = {}, {}
        for candidate in candidates:
            item_id = candidate.get("item_id")
            if not isinstance(item_id, str) or not item_id.strip():
                raise ValueError("A benchmark candidate requires a nonempty item identifier.")
            all_items.setdefault(item_id, None)
            sources = candidate.get("sources", [])
            if not isinstance(sources, list):
                raise ValueError("Benchmark candidate sources must be a list.")
            for reference in sources:
                source = reference.get("benchmark") if isinstance(reference, dict) else None
                if not isinstance(source, str) or not source.strip():
                    raise ValueError("Each benchmark source requires a nonempty benchmark name.")
                by_source.setdefault(source, {}).setdefault(item_id, None)
        for source, items in [(None, all_items), *by_source.items()]:
            queues.append({"queue_id": _queue_id(facet_id, source), "facet_id": facet_id,
                           "source": source, "item_ids": list(items)})
    return queues


class ScreeningQueues:
    """Select unseen items from fixed rankings without consuming cancelled work.

    The caller owns one global set of successfully screened item IDs and passes
    it to every take(). Update that set only after screening finishes. Selection
    does not reserve or mark items, so cancelled batches can be retried. A future
    concurrent scheduler must also exclude its own pending reservations.
    """

    def __init__(self, queues: list[dict]):
        self._items = {}
        for queue in queues:
            queue_id = queue.get("queue_id")
            if not isinstance(queue_id, str) or not queue_id.strip():
                raise ValueError("A screening queue requires a nonempty identifier.")
            if queue_id in self._items:
                raise ValueError("Screening queue identifiers must be unique.")
            item_ids = queue.get("item_ids")
            if (not isinstance(item_ids, list)
                    or any(not isinstance(item, str) or not item.strip() for item in item_ids)):
                raise ValueError("A screening queue requires a list of nonempty item identifiers.")
            if len(set(item_ids)) != len(item_ids):
                raise ValueError("An item may occur only once within a screening queue.")
            self._items[queue_id] = tuple(item_ids)

    def take(self, queue_id: str, limit: int, screened_ids: set[str]) -> list[str]:
        """Return up to limit next unseen IDs; leave queues and screened_ids intact."""
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
            raise ValueError("The batch limit must be a nonnegative integer.")
        items = self._items[queue_id]
        selected = []
        for item_id in items:
            if len(selected) == limit:
                break
            if item_id not in screened_ids:
                selected.append(item_id)
        return selected
