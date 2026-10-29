"""Select a fixed-size collection by coverage, then four-dimension quality.

Only validated, gate-passing screened items enter the integer program. Retrieval
ranks and output-content/output-form ratings do not affect collection membership.
No model requests are made here.
"""

from copy import deepcopy
from collections.abc import Iterable, Mapping
import math
import time

import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp

from .benchmark_data import row_fingerprint
from .requirements import Requirements
from .screening import GATED_DIMENSIONS, ScreeningAssessment, gate_for


DEFAULT_COLLECTION_LIMIT = 30
SELECTION_VERSION = 1
SELECTION_POLICY = {
    "version": SELECTION_VERSION,
    "collection_limit": DEFAULT_COLLECTION_LIMIT,
    "eligibility": "Validated task match and each of the four gated ratings at least 3",
    "quality_dimensions": list(GATED_DIMENSIONS),
    "quality_formula": "Mean of the four gated ratings; optimize their integer sum",
    "task_minimum": "One selected item per extracted facet, regardless of essential status",
    "explicit_quotas": "Enforce numeric minimum_items using only satisfied=true findings",
    "unknown_coverage": "Does not count toward quotas; does not exclude an otherwise eligible item",
    "unknown_minimum": "Report unresolved; do not invent a numeric constraint",
    "size": "min(collection limit, number of distinct eligible items)",
    "preservation": "Preserve achieved task coverage and quota counts capped at their targets, not item identities",
    "fallback_priority": ["Preserve achieved coverage", "Maximize distinct tasks covered",
                          "Minimize total explicit quota shortfall", "Maximize total quality"],
    "tie_break": "Lexicographically smallest sorted list of canonical item identifiers",
    "solver": "scipy.optimize.milp (HiGHS), zero relative optimality gap",
}


class SelectionError(RuntimeError):
    """A selection could not be safely established."""


class SelectionIncomplete(SelectionError):
    """The solver stopped before proving the required optimum or tie-break."""


def _check_cancelled(cancelled):
    if cancelled is not None and cancelled():
        raise InterruptedError("Collection selection was cancelled.")


def _eligible_items(requirements, screened_items, cancelled):
    excluded = {"errors": 0, "gate_fail": 0, "gate_unresolved": 0, "duplicates": 0}
    seen, eligible = {}, {}
    for record in screened_items:
        _check_cancelled(cancelled)
        if not isinstance(record, dict):
            raise ValueError("Every screened item must be an object.")
        if record.get("status") == "error":
            excluded["errors"] += 1
            continue
        if record.get("status") != "complete":
            raise ValueError("Selection requires completed screening results or explicit response errors.")
        evidence = record.get("evidence")
        if not isinstance(evidence, dict) or not isinstance(evidence.get("item"), dict):
            raise ValueError("A screened item must retain its complete original row.")
        key = row_fingerprint(evidence["item"])
        if record.get("item_id") != key or ("evidence_hash" in record and record["evidence_hash"] != key):
            raise ValueError("Screened item identifiers must match their complete original rows.")
        assessment = ScreeningAssessment.model_validate(record.get("assessment"))
        assessment.validate_context(requirements)
        snapshot = assessment.model_dump()
        if key in seen:
            if seen[key] != snapshot:
                raise ValueError("Duplicate item identifiers have conflicting screening assessments.")
            excluded["duplicates"] += 1
            continue
        seen[key] = snapshot
        gate = gate_for(assessment)["status"]
        if gate != "pass":
            excluded[f"gate_{gate}"] += 1
            continue
        rating_sum = sum(getattr(assessment.ratings, name).score for name in GATED_DIMENSIONS)
        eligible[key] = {
            "item_id": key, "quality_score": rating_sum / 4, "rating_sum": rating_sum,
            "matched_facet_ids": sorted(assessment.task.matched_facet_ids),
            "coverage_requirement_indices": sorted(finding.requirement_index for finding in assessment.coverage
                                                    if finding.satisfied is True),
        }
    return [eligible[key] for key in sorted(eligible)], excluded


class _Solver:
    """Keep a single deadline and verify every returned integer solution."""

    def __init__(self, deadline, cancelled):
        self.deadline, self.cancelled = deadline, cancelled
        self.calls = 0

    def check(self):
        _check_cancelled(self.cancelled)
        if time.monotonic() >= self.deadline:
            raise SelectionIncomplete("Collection selection exceeded its time limit. No new selection was accepted.")

    def solve(self, objective, rows, lower, upper, bounds):
        self.check()
        matrix = np.asarray(rows, dtype=float)
        low, high = np.asarray(lower, dtype=float), np.asarray(upper, dtype=float)
        self.check()
        self.calls += 1
        try:
            result = milp(
                c=np.asarray(objective, dtype=float), integrality=np.ones(len(objective), dtype=int),
                bounds=Bounds(np.zeros(len(objective)), bounds),
                constraints=LinearConstraint(matrix, low, high),
                options={"mip_rel_gap": 0.0, "time_limit": min(5.0, self.deadline - time.monotonic()),
                         "presolve": True},
            )
        except Exception as exc:
            _check_cancelled(self.cancelled)
            raise SelectionError("The collection solver could not complete. No new selection was accepted.") from exc
        self.check()
        if result.status == 2:
            return None
        if result.status == 1:
            raise SelectionIncomplete("The collection solver stopped before proving the optimum. No new selection was accepted.")
        if result.status != 0 or result.x is None:
            raise SelectionError("The collection solver did not return a proven optimum. No new selection was accepted.")
        values = np.asarray(result.x, dtype=float)
        if values.shape != (len(objective),) or not np.isfinite(values).all():
            raise SelectionError("The collection solver returned an invalid solution.")
        rounded = np.rint(values)
        if (not np.allclose(values, rounded, rtol=0, atol=1e-6)
                or (rounded < 0).any() or (rounded > bounds).any()):
            raise SelectionError("The collection solver returned a nonintegral or out-of-bounds solution.")
        totals = matrix @ rounded
        if (totals < low).any() or (totals > high).any():
            raise SelectionError("The collection solver returned a solution that violates its constraints.")
        return rounded.astype(int)


def _add_constraint(rows, lower, upper, coefficients, minimum, maximum=np.inf):
    rows.append(np.asarray(coefficients, dtype=float))
    lower.append(minimum)
    upper.append(maximum)


def _fix_optimum(solver, objective, rows, lower, upper, bounds):
    values = solver.solve(-objective, rows, lower, upper, bounds)
    if values is None:
        raise SelectionError("Previously achieved coverage cannot be preserved within the collection limit.")
    optimum = int(objective @ values)
    _add_constraint(rows, lower, upper, objective, optimum, optimum)
    return values


def _lexicographic_selection(solver, count, size, rows, lower, upper, bounds):
    """Prefer the first available identifier while preserving every optimum."""
    selected = []
    for index in range(count):
        solver.check()
        if len(selected) == size:
            break
        indicator = np.zeros(len(bounds))
        indicator[index] = 1
        # Feasibility with this ID included is the exact lexicographic test.
        values = solver.solve(np.zeros(len(bounds)), [*rows, indicator], [*lower, 1], [*upper, 1], bounds)
        chosen = values is not None
        _add_constraint(rows, lower, upper, indicator, int(chosen), int(chosen))
        if chosen:
            selected.append(index)
    if len(selected) != size:
        raise SelectionError("The solver did not establish the complete identifier tie-break.")
    return selected


def _choose(items, task_matrix, quota_matrix, targets, size, task_floors, quota_floors, solver):
    count = len(items)
    ratings = np.asarray([item["rating_sum"] for item in items], dtype=float)
    rows, lower, upper = [], [], []
    _add_constraint(rows, lower, upper, np.ones(count), size, size)
    for coefficients, floor in zip(task_matrix, task_floors):
        if floor:
            _add_constraint(rows, lower, upper, coefficients, floor)
    for coefficients, floor in zip(quota_matrix, quota_floors):
        if floor:
            _add_constraint(rows, lower, upper, coefficients, floor)
    full_rows, full_lower, full_upper = list(rows), list(lower), list(upper)
    possible = all(sum(row) >= 1 for row in task_matrix)
    possible = possible and all(target <= min(size, sum(row)) for target, row in zip(targets, quota_matrix))
    if possible:
        for coefficients in task_matrix:
            _add_constraint(full_rows, full_lower, full_upper, coefficients, 1)
        for coefficients, target in zip(quota_matrix, targets):
            _add_constraint(full_rows, full_lower, full_upper, coefficients, target)
        optimum = solver.solve(-ratings, full_rows, full_lower, full_upper, np.ones(count))
    else:
        optimum = None  # Avoid passing impossible, potentially huge quotas to the solver.
    if optimum is not None:
        total = int(ratings @ optimum)
        _add_constraint(full_rows, full_lower, full_upper, ratings, total, total)
        return _lexicographic_selection(solver, count, size, full_rows, full_lower, full_upper, np.ones(count)), True

    # Indicators represent covered tasks; integer credits represent quota units
    # achieved up to each target. This keeps priority stages separate and clear.
    task_count, quota_count = len(task_matrix), len(quota_matrix)
    width = count + task_count + quota_count
    rows = [np.pad(row, (0, width - count)) for row in rows]
    bounds = np.asarray([1] * (count + task_count)
                        + [min(target, size, int(sum(row))) for target, row in zip(targets, quota_matrix)], dtype=float)
    for position, coefficients in enumerate([*task_matrix, *quota_matrix]):
        row = np.zeros(width)
        row[:count] = coefficients
        row[count + position] = -1
        _add_constraint(rows, lower, upper, row, 0)
    for start, stop in ((count, count + task_count), (count + task_count, width)):
        if start != stop:
            objective = np.zeros(width)
            objective[start:stop] = 1
            _fix_optimum(solver, objective, rows, lower, upper, bounds)
    objective = np.zeros(width)
    objective[:count] = ratings
    _fix_optimum(solver, objective, rows, lower, upper, bounds)
    return _lexicographic_selection(solver, count, size, rows, lower, upper, bounds), False


def select_collection(requirements: Requirements, screened_items: Iterable[dict], *,
                      limit: int = DEFAULT_COLLECTION_LIMIT, previous_selected_ids: list[str] | None = None,
                      cancelled=None, time_limit: float = 30.0) -> dict:
    """Return a proven selection, or raise without publishing an approximation.

    The default is thirty items total. If complete numeric coverage is impossible,
    preserve earlier achieved coverage, maximize distinct covered tasks, minimize
    numeric quota deficits, then maximize quality. Equal optima use exact ID order.
    """
    if (not isinstance(requirements, Requirements) or not isinstance(screened_items, Iterable)
            or isinstance(screened_items, (str, bytes, Mapping))):
        raise ValueError("Selection requires validated requirements and an iterable of screened items.")
    if type(limit) is not int or not 1 <= limit <= DEFAULT_COLLECTION_LIMIT:
        raise ValueError("The collection limit must be a positive integer no greater than 30.")
    if type(time_limit) not in {int, float} or not math.isfinite(time_limit) or time_limit <= 0:
        raise ValueError("The selection time limit must be finite and positive.")
    previous = [] if previous_selected_ids is None else previous_selected_ids
    if (not isinstance(previous, list) or any(not isinstance(key, str) or not key for key in previous)
            or len(set(previous)) != len(previous)):
        raise ValueError("Previous selected identifiers must be a list of distinct item identifiers.")
    started = time.monotonic()
    solver = _Solver(started + time_limit, cancelled)
    solver.check()
    items, excluded = _eligible_items(requirements, screened_items, cancelled)
    keys = {item["item_id"] for item in items}
    if not set(previous).issubset(keys):
        raise ValueError("Every previous selected identifier must remain in the current eligible pool.")
    size = min(limit, len(items))
    facets = [facet.facet_id for facet in requirements.task_facets]
    quotas = requirements.coverage_requirements
    numeric = [index for index, quota in enumerate(quotas) if quota.minimum_items is not None]
    unresolved = [index for index, quota in enumerate(quotas) if quota.minimum_items is None]
    task_matrix = [[int(facet in item["matched_facet_ids"]) for item in items] for facet in facets]
    all_quota_matrix = [[int(index in item["coverage_requirement_indices"]) for item in items] for index in range(len(quotas))]
    quota_matrix = [all_quota_matrix[index] for index in numeric]
    targets = [quotas[index].minimum_items for index in numeric]
    prior_indices = [index for index, item in enumerate(items) if item["item_id"] in set(previous)]
    task_floors = [int(any(row[index] for index in prior_indices)) for row in task_matrix]
    quota_floors = [min(target, sum(row[index] for index in prior_indices)) for target, row in zip(targets, quota_matrix)]
    solver.check()
    if items:
        selected_indices, feasible = _choose(items, task_matrix, quota_matrix, targets, size, task_floors, quota_floors, solver)
    else:
        selected_indices, feasible = [], not facets and not numeric
    selected = [items[index] for index in selected_indices]
    task_coverage = [{"facet_id": facet, "minimum": 1, "eligible_count": sum(row),
                      "selected_count": sum(row[index] for index in selected_indices),
                      "shortfall": max(0, 1 - sum(row[index] for index in selected_indices))}
                     for facet, row in zip(facets, task_matrix)]
    quota_coverage = []
    for index, (quota, row) in enumerate(zip(quotas, all_quota_matrix)):
        total = sum(row[position] for position in selected_indices)
        quota_coverage.append({"requirement_index": index, "minimum_items": quota.minimum_items,
                               "eligible_count": sum(row), "selected_count": total,
                               "shortfall": None if quota.minimum_items is None else max(0, quota.minimum_items - total)})
    # Recheck the actual selected IDs, independently of auxiliary solver variables.
    if any(entry["selected_count"] < floor for entry, floor in zip(task_coverage, task_floors)):
        raise SelectionError("The selected collection did not preserve achieved task coverage.")
    if any(quota_coverage[index]["selected_count"] < floor for index, floor in zip(numeric, quota_floors)):
        raise SelectionError("The selected collection did not preserve achieved quota coverage.")
    actual_feasible = not any(entry["shortfall"] for entry in task_coverage)
    actual_feasible = actual_feasible and not any(quota_coverage[index]["shortfall"] for index in numeric)
    if feasible != actual_feasible:
        raise SelectionError("The selected collection does not agree with the solver's coverage result.")
    gaps = []
    if (not feasible and all(entry["eligible_count"] >= 1 for entry in task_coverage)
            and all(quota_coverage[index]["eligible_count"] >= quotas[index].minimum_items for index in numeric)):
        gaps.append(f"Coverage requirements cannot all fit within the {limit}-item total collection limit.")
    gaps.extend(f"Task '{entry['facet_id']}' has no selected item." for entry in task_coverage if entry["shortfall"])
    gaps.extend(f"Coverage requirement {entry['requirement_index']} is short by {entry['shortfall']} item(s)."
                for entry in quota_coverage if entry["shortfall"] is not None and entry["shortfall"] > 0)
    gaps.extend(f"Coverage requirement {index} has no numeric minimum and remains unresolved." for index in unresolved)
    policy = deepcopy(SELECTION_POLICY)
    policy["collection_limit"] = limit
    result = {
        "policy": policy, "limit": limit, "eligible_count": len(items), "selected_count": len(selected),
        "selected_item_ids": [item["item_id"] for item in selected], "items": selected,
        "total_quality": sum(item["rating_sum"] for item in selected) / 4,
        "task_coverage": task_coverage, "quota_coverage": quota_coverage,
        "constraints_feasible": feasible, "fully_satisfied": feasible and not unresolved,
        "gaps": gaps, "unresolved_requirement_indices": unresolved, "excluded_counts": excluded,
        "previous_selected_item_ids": sorted(previous),
        "preserved_coverage": {
            "tasks": [{"facet_id": facet, "minimum": floor} for facet, floor in zip(facets, task_floors) if floor],
            "quotas": [{"requirement_index": index, "minimum": floor} for index, floor in zip(numeric, quota_floors) if floor],
        },
        "solver": {"status": "optimal", "implementation": "scipy.optimize.milp (HiGHS)",
                   "scipy_version": scipy.__version__, "calls": solver.calls, "mip_rel_gap": 0.0,
                   "fallback_used": not feasible, "time_limit_seconds": time_limit,
                   "elapsed_seconds": time.monotonic() - started},
    }
    solver.check()
    return result
