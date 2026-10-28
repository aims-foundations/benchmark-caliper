"""Run Step 7 in batches, publishing outcomes only after selection succeeds.

The initial allocation stays unchanged. Adaptive acquisitions and request
attempts have their own history, which survives cancellation and continuation.
Snapshots are checkpointed with their request reservations before paid work.
"""

import asyncio
from contextlib import AsyncExitStack
from copy import deepcopy
from threading import Event

from bayesian_auditing.adaptive_screening import (
    ADAPTIVE_VERSION, ADAPTIVE_POLICY, ADAPTIVE_CANDIDATE_LIMIT, ADAPTIVE_BATCH_SIZE,
    EXPLORATION_PROBABILITY, choose_batch, make_outcomes, queue_priorities,
)
from bayesian_auditing.benchmark_queries import ScreeningQueues
from bayesian_auditing.requirements import Requirements
from bayesian_auditing.screening import ItemScreener, ScreeningAssessment, GATED_DIMENSIONS, gate_for
from bayesian_auditing.screening_budget import (
    COST_POLICY, AdaptiveSettings, can_afford, cost_summary, request_reservation, usage_cost,
)


def settings_record(settings: AdaptiveSettings) -> dict:
    return {**settings.model_dump(), "candidate_limit": ADAPTIVE_CANDIDATE_LIMIT,
            "batch_size": ADAPTIVE_BATCH_SIZE, "exploration_rate": EXPLORATION_PROBABILITY}


def all_outcomes(state: dict) -> list[dict]:
    return [outcome for batch in state["batches"] for outcome in batch["outcomes"]]


def acquisitions(screening: dict, state: dict | None) -> list[dict]:
    initial = list(screening["allocation"]["items"])
    if state is None:
        return initial
    return initial + [dict(item_id=item_id, facet_id=batch["facet_id"], queue_id=batch["queue_id"])
                      for batch in state["batches"][1:] for item_id in batch["item_ids"]]


def validate_collection(job) -> None:
    """Check accepted membership and the counts used by the acquisition policy."""
    selection = job.selection
    ids = selection["selected_item_ids"]
    records = {item["item_id"]: item for item in job.screening["items"]}
    if (not isinstance(ids, list) or len(set(ids)) != len(ids)
            or not set(ids).issubset(records) or len(ids) > 30
            or selection["limit"] != 30 or selection["selected_count"] != len(ids)
            or [item["item_id"] for item in selection["items"]] != ids):
        raise ValueError("The selected collection does not match saved candidates.")
    assessments = []
    for key in ids:
        item = records[key]
        assessment = ScreeningAssessment.model_validate(item["assessment"])
        if item["status"] != "complete" or gate_for(assessment)["status"] != "pass":
            raise ValueError("Selected candidates must have valid passing assessments.")
        assessments.append(assessment)
    requirements = Requirements.model_validate(job.requirements)
    tasks = [{"facet_id": facet.facet_id,
              "selected_count": sum(facet.facet_id in item.task.matched_facet_ids for item in assessments)}
             for facet in requirements.task_facets]
    quotas = [{"requirement_index": index,
               "selected_count": sum(any(f.requirement_index == index and f.satisfied is True for f in item.coverage)
                                     for item in assessments)}
              for index in range(len(requirements.coverage_requirements))]
    for expected, name, key in ((tasks, "task_coverage", "facet_id"), (quotas, "quota_coverage", "requirement_index")):
        actual = [{key: row[key], "selected_count": row["selected_count"]} for row in selection[name]]
        if actual != expected:
            raise ValueError("Selected coverage counts do not match the actual assessments.")
    quality = sum(sum(getattr(item.ratings, name).score for name in GATED_DIMENSIONS) / 4 for item in assessments)
    if selection["total_quality"] != quality:
        raise ValueError("Selected quality does not match the saved ratings.")


def initialize(job, settings: AdaptiveSettings) -> dict:
    from . import item_review as service

    validate_collection(job)
    allocation = job.screening["allocation"]["items"]
    items = job.screening["items"]
    if len(items) != len(allocation) or any(item["status"] != "complete" for item in items):
        raise ValueError("Finish valid initial screening before adaptive screening.")
    outcomes = make_outcomes(allocation, items, job.selection["selected_item_ids"],
                             resolve=service.expand_candidate)
    state = {
        "version": ADAPTIVE_VERSION, "policy": deepcopy(ADAPTIVE_POLICY),
        "settings": settings_record(settings),
        # Keep Step 6 separate from the collection rebuilt during Step 7.
        "initial_selection": deepcopy(job.selection),
        "initial_selection_run_id": job.selection_run_id,
        "batches": [{"number": 0, "kind": "initial", "status": "committed",
                     "queue_id": None, "facet_id": None, "source": None, "exploration": None,
                     "item_ids": [entry["item_id"] for entry in allocation], "outcomes": outcomes,
                     "selected_item_ids": list(job.selection["selected_item_ids"])}],
        "attempts": [], "frozen": False, "stop_reason": None,
    }
    state["queue_statistics"] = current_priorities(job, state)
    state["cost"] = cost_summary([], state["settings"])
    state["screened_count"] = state["acquired_count"] = len(items)
    return state


def validate_history(job) -> None:
    """Validate saved decisions and once-only outcomes without repeating a solve."""
    from . import item_review as service

    state = job.adaptive
    validate_collection(job)
    if state["version"] != ADAPTIVE_VERSION or state["policy"] != ADAPTIVE_POLICY:
        raise ValueError("The saved adaptive policy has changed.")
    if state["cost"].get("policy") != COST_POLICY:
        raise ValueError("The saved cost accounting policy has changed. Start a new adaptive run from the selection.")
    fields = AdaptiveSettings.model_fields
    settings = AdaptiveSettings.model_validate({key: value for key, value in state["settings"].items() if key in fields})
    if state["settings"] != settings_record(settings):
        raise ValueError("The saved adaptive settings have changed.")
    queues = job.benchmark_retrieval["queues"]
    reader = ScreeningQueues(queues)
    queue_by_id = {queue["queue_id"]: queue for queue in queues}
    items = {item["item_id"]: item for item in job.screening["items"]}
    initial = job.screening["allocation"]["items"]
    seen, last_selected = set(), None
    batches = state["batches"]
    if not batches:
        raise ValueError("The initial selection outcomes are missing.")
    initial_selection = state.get("initial_selection")
    if initial_selection is not None and initial_selection["selected_item_ids"] != batches[0]["selected_item_ids"]:
        raise ValueError("The saved initial collection does not match the initial selection outcomes.")
    for number, batch in enumerate(batches):
        if batch["number"] != number or batch["kind"] != ("initial" if number == 0 else "adaptive"):
            raise ValueError("Adaptive batches must retain their original order.")
        if number == 0:
            acquired = initial
            if batch["item_ids"] != [entry["item_id"] for entry in initial] or batch["status"] != "committed":
                raise ValueError("The initial acquisition outcomes have changed.")
        else:
            queue = queue_by_id[batch["queue_id"]]
            if batch["facet_id"] != queue["facet_id"] or batch["source"] != queue["source"]:
                raise ValueError("An adaptive batch has the wrong queue attribution.")
            if not 1 <= len(batch["item_ids"]) <= ADAPTIVE_BATCH_SIZE:
                raise ValueError("An adaptive batch must contain one to eight candidates.")
            if batch["item_ids"] != reader.take(batch["queue_id"], len(batch["item_ids"]), seen):
                raise ValueError("An adaptive batch must take the next unseen ranked candidates.")
            acquired = [dict(item_id=key, facet_id=batch["facet_id"]) for key in batch["item_ids"]]
        if len(set(batch["item_ids"])) != len(batch["item_ids"]) or seen.intersection(batch["item_ids"]):
            raise ValueError("An item may be acquired only once.")
        seen.update(batch["item_ids"])
        if batch["status"] == "committed":
            complete = [entry for entry in acquired if items.get(entry["item_id"], {}).get("status") == "complete"]
            if len(complete) != len(acquired) and not (state["frozen"] and state["stop_reason"] == "cost_limit" and number == len(batches) - 1):
                raise ValueError("Only a cost-limited final batch can be committed partially.")
            if not set(batch["selected_item_ids"]).issubset(seen):
                raise ValueError("A batch selection contains an unseen candidate.")
            expected = make_outcomes(complete, list(items.values()), batch["selected_item_ids"],
                                     resolve=service.expand_candidate)
            if batch["outcomes"] != expected:
                raise ValueError("Saved selection outcomes cannot be relabeled.")
            last_selected = batch["selected_item_ids"]
        elif batch["status"] != "pending" or number != len(batches) - 1 or batch["outcomes"]:
            raise ValueError("Only the last batch can be pending, without outcomes.")
    if len(seen) > ADAPTIVE_CANDIDATE_LIMIT or last_selected != job.selection["selected_item_ids"]:
        raise ValueError("Adaptive history does not match the accepted collection.")
    if state["queue_statistics"] != current_priorities(job, state):
        raise ValueError("Queue counts do not match their saved outcomes.")
    model = job.screening["model"]
    screener = ItemScreener(None, prompt=model["prompt"], model=model["model"],
                           reasoning_effort=model["reasoning_effort"], max_output_tokens=model["max_output_tokens"])
    candidates = {(ranking["facet_id"], item["item_id"]): item
                  for ranking in job.benchmark_retrieval["rankings"] for item in ranking["candidates"]}
    for attempt in state["attempts"]:
        number = attempt["batch_number"]
        if (type(number) is not int or not 1 <= number < len(batches)
                or attempt["item_id"] not in batches[number]["item_ids"]
                or attempt["status"] not in {"pending", "unknown", "complete", "error"}):
            raise ValueError("A screening attempt has no valid adaptive acquisition.")
        batch = batches[number]
        row = service.expand_candidate(candidates[batch["facet_id"], attempt["item_id"]])["evidence"]["item"]
        request = screener.request_options(job.request.deployment.model_dump(), Requirements.model_validate(job.requirements), row)
        if (attempt["cost_usd"] != usage_cost(attempt["usage"], state["settings"])
                or attempt["reserved_usd"] != request_reservation(request, state["settings"])):
            raise ValueError("Saved attempt costs do not match their requests and reported usage.")
    if state["cost"] != cost_summary(state["attempts"], state["settings"]):
        raise ValueError("Cost totals do not match the attempt history.")


def current_priorities(job, state: dict) -> list[dict]:
    seen = {entry["item_id"] for entry in acquisitions(job.screening, state)}
    return queue_priorities(Requirements.model_validate(job.requirements), job.benchmark_retrieval["queues"],
                            job.selection, all_outcomes(state), seen)


def publish(job, state: dict) -> None:
    """Replace snapshots so a concurrent export never observes later mutation."""
    from . import item_review as service

    state["cost"] = cost_summary(state["attempts"], state["settings"])
    state["acquired_count"] = sum(len(batch["item_ids"]) for batch in state["batches"])
    state["screened_count"] = sum(item["status"] == "complete" for item in job.screening["items"])
    state["queue_statistics"] = current_priorities(job, state)
    job.adaptive = deepcopy(state)
    service.checkpoint(job)


async def commit_batch(job, state: dict, requirements, *, partial: bool = False) -> None:
    from . import item_review as service

    batch = state["batches"][-1]
    items = {item["item_id"]: item for item in job.screening["items"]}
    complete = [key for key in batch["item_ids"] if items.get(key, {}).get("status") == "complete"]
    if not partial and len(complete) != len(batch["item_ids"]):
        raise ValueError("A batch is not ready for selection.")
    cancelled = Event()
    job.message = f"Rebuilding the collection after adaptive batch {batch['number']}."
    work = asyncio.create_task(asyncio.to_thread(
        service.select_collection, requirements, service.screened_records(job),
        previous_selected_ids=job.selection["selected_item_ids"], cancelled=cancelled.is_set,
    ))
    try:
        selection = await asyncio.shield(work)
    except asyncio.CancelledError:
        cancelled.set()
        await service.finish_worker(work)
        raise
    acquired = [dict(item_id=key, facet_id=batch["facet_id"]) for key in complete]
    outcomes = make_outcomes(acquired, job.screening["items"], selection["selected_item_ids"],
                             resolve=service.expand_candidate)
    # Nothing is published until optimization and all outcome checks succeed.
    batch.update(status="committed", outcomes=outcomes,
                 selected_item_ids=list(selection["selected_item_ids"]))
    if partial:
        batch["unresolved_item_ids"] = [key for key in batch["item_ids"] if key not in complete]
        # A partially committed batch is valid only as the final cost-limited
        # collection. Persist that decision together with the batch, including
        # if a restart happens before freeze() publishes its final message.
        state.update(frozen=True, stop_reason="cost_limit")
    job.selection, job.selection_run_id = selection, job.run_id
    publish(job, state)


def freeze(job, state: dict, reason: str) -> None:
    state.update(frozen=True, stop_reason=reason)
    publish(job, state)
    labels = {"candidate_limit": "the 160-candidate total limit was reached",
              "queues_exhausted": "no unseen retrieved candidates remain",
              "cost_limit": "the additional screening cost budget cannot fund another request"}
    job.status = "completed"
    job.message = f"Collection frozen: {labels[reason]}. Review the selected items and any remaining coverage gaps."


async def adapt_benchmarks(job, api_key: str) -> None:
    from . import item_review as service

    requirements = service.validate_selection_source(job)
    validate_history(job)
    state = deepcopy(job.adaptive)
    settings = state["settings"]
    queues = job.benchmark_retrieval["queues"]
    candidates = service.screening_candidates(job.benchmark_retrieval, requirements)
    answers = job.request.deployment.model_dump()
    model = job.screening["model"]
    job.status, job.message = "running", "Choosing the next screening queue from selection yield and coverage gaps."

    # Each request attempt is recorded explicitly. Hidden SDK retries would make
    # budget accounting and unknown charges impossible to inspect reliably.
    async with AsyncExitStack() as stack:
        screener = service.AsyncItemScreener(None, prompt=model["prompt"], model=model["model"],
                                           reasoning_effort=model["reasoning_effort"],
                                           max_output_tokens=model["max_output_tokens"])
        while True:
            batch = state["batches"][-1]
            if batch["status"] == "committed":
                seen = {entry["item_id"] for entry in acquisitions(job.screening, state)}
                if len(seen) >= ADAPTIVE_CANDIDATE_LIMIT:
                    freeze(job, state, "candidate_limit")
                    return
                decision = choose_batch(requirements, queues, job.selection, all_outcomes(state), seen,
                                        seed=settings["seed"], decision_index=len(state["batches"]) - 1)
                if decision is None:
                    freeze(job, state, "queues_exhausted")
                    return
                # Admit a prefix of the chosen queue that fits the reservation.
                affordable, reservation = [], 0.0
                for key in decision["item_ids"]:
                    row = service.expand_candidate(candidates[decision["facet_id"], key])["evidence"]["item"]
                    estimate = request_reservation(screener.request_options(answers, requirements, row), settings)
                    reservation += estimate or 0
                    if not can_afford(reservation, state["attempts"], settings):
                        break
                    affordable.append(key)
                if not affordable:
                    freeze(job, state, "cost_limit")
                    return
                batch = {**decision, "number": len(state["batches"]), "kind": "adaptive",
                         "status": "pending", "item_ids": affordable, "outcomes": [],
                         "selected_item_ids": [], "budget_limited": len(affordable) < len(decision["item_ids"])}
                state["batches"].append(batch)
                publish(job, state)

            for key in batch["item_ids"]:
                existing = next((item for item in job.screening["items"] if item["item_id"] == key), None)
                if existing and existing["status"] == "complete":
                    continue
                candidate = service.expand_candidate(candidates[batch["facet_id"], key])
                reservation = request_reservation(screener.request_options(answers, requirements, candidate["evidence"]["item"]), settings)
                if not can_afford(reservation, state["attempts"], settings):
                    await commit_batch(job, state, requirements, partial=True)
                    freeze(job, state, "cost_limit")
                    return
                attempt = {"item_id": key, "batch_number": batch["number"], "run_id": job.run_id,
                           "status": "pending", "usage": None, "cost_usd": None, "reserved_usd": reservation}
                state["attempts"].append(attempt)
                publish(job, state)
                job.message = f"Screening adaptive batch {batch['number']}: {state['screened_count']} of 160 total candidates assessed."
                try:
                    if screener.client is None:
                        screener.client = await stack.enter_async_context(service.AsyncOpenAI(
                            api_key=api_key, base_url="https://api.openai.com/v1", max_retries=0, timeout=600))
                    result = await screener(answers, requirements, candidate["evidence"]["item"])
                except BaseException:
                    attempt["status"] = "unknown"
                    publish(job, state)
                    raise
                attempt.update(status=result["status"], usage=result.get("usage"),
                               cost_usd=usage_cost(result.get("usage"), settings))
                service.record_usage(job, result.get("usage"))
                saved = {**service.candidate_store().compact(candidate),
                         "acquisition": {"queue_id": batch["queue_id"], "facet_id": batch["facet_id"]},
                         "screened_run_id": job.run_id,
                         **{name: result[name] for name in ("status", "assessment", "gate", "response_id", "response_model", "usage", "error") if name in result}}
                records = {item["item_id"]: item for item in job.screening["items"]}
                records[key] = saved
                order = acquisitions(job.screening, state)
                job.screening = {**job.screening, "items": [records[entry["item_id"]] for entry in order if entry["item_id"] in records]}
                publish(job, state)
                if result["status"] != "complete":
                    job.status = "failed"
                    job.message = "An adaptive screening response was invalid. The batch remains pending and the previous collection is retained; resume to retry unfinished items."
                    return
            await commit_batch(job, state, requirements)
