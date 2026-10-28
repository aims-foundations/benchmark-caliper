"""Choose the next fixed retrieval queue from retention yield and coverage gaps.

This module makes no model requests and changes no saved state. The controller
commits outcomes only after a complete batch has been screened and selected.
Historical outcomes describe retention at that moment, even if a later batch
replaces an item. A seed and decision index reproduce each queue choice.
"""

import hashlib
import random

from .benchmark_data import row_fingerprint
from .benchmark_queries import ScreeningQueues
from .requirements import Requirements
from .screening import ScreeningAssessment, gate_for


ADAPTIVE_VERSION = 1
ADAPTIVE_CANDIDATE_LIMIT = 160
ADAPTIVE_BATCH_SIZE = 8
EXPLORATION_PROBABILITY = 0.2
ADAPTIVE_POLICY = {
    "version": ADAPTIVE_VERSION,
    "candidate_limit": ADAPTIVE_CANDIDATE_LIMIT,
    "batch_size": ADAPTIVE_BATCH_SIZE,
    "prior": {"alpha": 1, "beta": 1},
    "yield": "(1 + retained) / (2 + retained + not retained)",
    "success": "Newly screened item retained immediately after its complete batch",
    "history": "Record each outcome once; later replacements do not change it",
    "cost_limited_final_batch": "Select from valid completed assessments; unresolved candidates receive no outcome",
    "credit": "Acquisition task's all-source and matching source queues, once per queue",
    "coverage_weight": "1 + largest fractional shortfall among task minimum 1 and applicable numeric quotas",
    "conditional_quota_extension": "Use selected satisfied=true counts; global quotas apply to every task",
    "priority": "Posterior mean selection yield times coverage weight",
    "exploration_probability": EXPLORATION_PROBABILITY,
    "exploration": "Uniform choice among queues with unseen candidates",
    "exploitation": "Highest priority, then lexicographically smallest queue identifier",
    "randomness": "Python Random seeded by SHA256(version:seed:decision_index)",
    "candidates": "Next ranked globally unseen items in the chosen saved queue",
}


def _identifier(value):
    return isinstance(value, str) and bool(value.strip())


def _validate_queues(queues):
    if not isinstance(queues, list) or any(not isinstance(queue, dict) for queue in queues):
        raise ValueError("Adaptive screening requires a list of queue objects.")
    reader = ScreeningQueues(queues)
    scopes = {}
    for queue in queues:
        facet, source = queue.get("facet_id"), queue.get("source")
        if not _identifier(facet) or "source" not in queue or (source is not None and not _identifier(source)):
            raise ValueError("Every queue requires a task facet and a valid source scope.")
        if (facet, source) in scopes:
            raise ValueError("A task may have only one queue for each source scope.")
        scopes[facet, source] = set(queue["item_ids"])
    for (facet, source), items in scopes.items():
        if (facet, None) not in scopes or not items.issubset(scopes[facet, None]):
            raise ValueError("Every source queue must belong to its task's all-source queue.")
    return reader, scopes


def queue_statistics(queues: list[dict], outcomes: list[dict]) -> list[dict]:
    """Rebuild Beta counters from immutable, globally distinct item outcomes.

    The acquisition facet controls credit, not the item's matched task facets.
    Duplicate physical source references have already been collapsed into names
    by make_outcomes, so one item contributes at most once to any queue.
    """
    _, scopes = _validate_queues(queues)
    if not isinstance(outcomes, list):
        raise ValueError("Queue statistics require a list of committed outcomes.")
    counts = {scope: [0, 0] for scope in scopes}
    seen = set()
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            raise ValueError("Every committed outcome must be an object.")
        item_id, facet = outcome.get("item_id"), outcome.get("facet_id")
        names, retained = outcome.get("source_names"), outcome.get("retained")
        if (not _identifier(item_id) or not _identifier(facet) or type(retained) is not bool
                or not isinstance(names, list) or any(not _identifier(name) for name in names)
                or len(set(names)) != len(names)):
            raise ValueError("An outcome requires item/task identifiers, distinct sources, and a boolean retention result.")
        if item_id in seen:
            raise ValueError("An item may have only one committed retention outcome.")
        seen.add(item_id)
        expected_sources = {source for (task, source), items in scopes.items()
                            if task == facet and source is not None and item_id in items}
        if item_id not in scopes.get((facet, None), set()) or set(names) != expected_sources:
            raise ValueError("An outcome must match its acquisition task's saved item and source queues.")
        for source in [None, *names]:
            counts[facet, source][0 if retained else 1] += 1
    result = []
    for queue in sorted(queues, key=lambda value: value["queue_id"]):
        successes, failures = counts[queue["facet_id"], queue["source"]]
        alpha, beta = 1 + successes, 1 + failures
        result.append({"queue_id": queue["queue_id"], "facet_id": queue["facet_id"],
                       "source": queue["source"], "successes": successes, "failures": failures,
                       "alpha": alpha, "beta": beta, "estimated_yield": alpha / (alpha + beta)})
    return result


def _coverage_counts(rows, key, expected):
    if not isinstance(rows, list):
        raise ValueError("Selection must report complete task and quota coverage counts.")
    result = {}
    for row in rows:
        expected_type = str if key == "facet_id" else int
        if (not isinstance(row, dict) or type(row.get(key)) is not expected_type
                or row[key] not in expected or row[key] in result
                or type(row.get("selected_count")) is not int or row["selected_count"] < 0):
            raise ValueError("Selection coverage counts must be distinct, known, nonnegative integers.")
        result[row[key]] = row["selected_count"]
    if set(result) != expected:
        raise ValueError("Selection must report every task and coverage requirement.")
    return result


def queue_priorities(requirements: Requirements, queues: list[dict], selection: dict,
                     outcomes: list[dict], seen_ids) -> list[dict]:
    """Report every queue's current yield, coverage bonus, and unseen count.

    Exhausted queues remain visible for inspection but cannot be chosen. Unknown
    quota minima contribute no numerical bonus. Conditional quotas use their
    qualifying selected count, even if the task itself is already represented.
    """
    if not isinstance(requirements, Requirements) or not isinstance(selection, dict):
        raise ValueError("Adaptive choices require validated requirements and an accepted selection.")
    if not isinstance(seen_ids, (set, frozenset, list, tuple)) or any(not _identifier(key) for key in seen_ids):
        raise ValueError("Seen identifiers must be a collection of nonempty item identifiers.")
    seen = set(seen_ids)
    _, scopes = _validate_queues(queues)
    statistics = queue_statistics(queues, outcomes)
    facets = {facet.facet_id for facet in requirements.task_facets}
    if {facet for facet, _ in scopes} != facets:
        raise ValueError("Saved queues must represent exactly the extracted task facets.")
    if not {outcome["item_id"] for outcome in outcomes}.issubset(seen):
        raise ValueError("Every committed outcome must already be counted as seen.")
    task_counts = _coverage_counts(selection.get("task_coverage"), "facet_id", facets)
    quotas = requirements.coverage_requirements
    quota_counts = _coverage_counts(selection.get("quota_coverage"), "requirement_index", set(range(len(quotas))))
    priorities = []
    for stats in statistics:
        facet = stats["facet_id"]
        remaining = len(scopes[facet, stats["source"]] - seen)
        deficit = float(task_counts[facet] == 0)
        for index, quota in enumerate(quotas):
            target = quota.minimum_items
            if target is not None and (not quota.facet_ids or facet in quota.facet_ids):
                deficit = max(deficit, max(0, target - quota_counts[index]) / target)
        weight = 1 + deficit
        priorities.append({**stats, "coverage_weight": weight,
                           "priority": stats["estimated_yield"] * weight, "remaining": remaining})
    return priorities


def choose_batch(requirements: Requirements, queues: list[dict], selection: dict,
                 outcomes: list[dict], seen_ids, *, seed: int, decision_index: int,
                 limit: int = ADAPTIVE_CANDIDATE_LIMIT) -> dict | None:
    """Plan up to eight unseen items without consuming or reserving anything.

    The limit includes the initial screening allocation. The caller owns seen
    IDs and pending work, and must resume an incomplete batch before asking for
    another decision.
    """
    if type(limit) is not int or not 1 <= limit <= ADAPTIVE_CANDIDATE_LIMIT:
        raise ValueError("The total candidate limit must be an integer between 1 and 160.")
    for name, value in (("seed", seed), ("decision_index", decision_index)):
        if type(value) is not int or not 0 <= value <= 2**32 - 1:
            raise ValueError(f"The {name} must be an integer between 0 and 4294967295.")
    priorities = [row for row in queue_priorities(requirements, queues, selection, outcomes, seen_ids)
                  if row["remaining"] > 0]
    seen = set(seen_ids)
    if len(seen) >= limit or not priorities:
        return None
    digest = hashlib.sha256(f"{ADAPTIVE_VERSION}:{seed}:{decision_index}".encode("ascii")).digest()
    rng = random.Random(int.from_bytes(digest, "big"))
    exploration = rng.random() < EXPLORATION_PROBABILITY
    chosen = rng.choice(priorities) if exploration else min(
        priorities, key=lambda row: (-row["priority"], row["queue_id"]))
    item_ids = ScreeningQueues(queues).take(chosen["queue_id"], min(ADAPTIVE_BATCH_SIZE, limit - len(seen)), seen)
    return {"decision_index": decision_index, "queue_id": chosen["queue_id"],
            "facet_id": chosen["facet_id"], "source": chosen["source"],
            "exploration": exploration, "item_ids": item_ids, "priorities": priorities}


def make_outcomes(acquisitions: list[dict], screened_items: list[dict], selected_ids,
                  *, resolve=None) -> list[dict]:
    """Freeze this batch's retention signal after all its assessments are valid.

    Requirements-specific context validation belongs to the screening/selection
    stages. Here we additionally check row identities, assessment structure, and
    eligibility for retained items. Errors or missing responses are not failures:
    they prevent committing the batch until screening has been completed.
    An optional resolver loads each acquired record's original row as needed.
    """
    if not isinstance(acquisitions, list) or not isinstance(screened_items, list):
        raise ValueError("Outcome construction requires acquisition and screening lists.")
    if (not isinstance(selected_ids, (list, tuple, set, frozenset))
            or any(not _identifier(key) for key in selected_ids) or len(set(selected_ids)) != len(selected_ids)):
        raise ValueError("Selected identifiers must be distinct nonempty strings.")
    selected = set(selected_ids)
    records = {}
    for record in screened_items:
        if not isinstance(record, dict) or not _identifier(record.get("item_id")):
            raise ValueError("Screening records require valid item identifiers.")
        if record["item_id"] in records:
            raise ValueError("Screening records must not repeat an item.")
        records[record["item_id"]] = record
    outcomes, seen = [], set()
    for acquisition in acquisitions:
        if (not isinstance(acquisition, dict) or not _identifier(acquisition.get("item_id"))
                or not _identifier(acquisition.get("facet_id"))):
            raise ValueError("Each acquisition must identify its item and task facet.")
        key = acquisition["item_id"]
        if key in seen:
            raise ValueError("Acquisitions must not repeat an item.")
        seen.add(key)
        record = records.get(key)
        if record is None or record.get("status") != "complete":
            raise ValueError("A batch cannot commit outcomes until every acquired item has a complete assessment.")
        if resolve is not None:
            record = resolve(record)
        evidence = record.get("evidence")
        if not isinstance(evidence, dict) or not isinstance(evidence.get("item"), dict):
            raise ValueError("Screening outcomes require complete original item rows.")
        if key != row_fingerprint(evidence["item"]) or record.get("evidence_hash", key) != key:
            raise ValueError("A screening outcome identifier must match its original row.")
        assessment = ScreeningAssessment.model_validate(record.get("assessment"))
        if key in selected and gate_for(assessment)["status"] != "pass":
            raise ValueError("A retained outcome must pass the screening eligibility gate.")
        sources = record.get("sources")
        if (not isinstance(sources, list) or any(not isinstance(source, dict)
                or not _identifier(source.get("benchmark")) for source in sources)):
            raise ValueError("A screening outcome requires valid benchmark source references.")
        outcomes.append({"item_id": key, "facet_id": acquisition["facet_id"],
                         "source_names": sorted({source["benchmark"] for source in sources}),
                         "retained": key in selected})
    return outcomes
