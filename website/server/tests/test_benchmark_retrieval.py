"""Step 4 HTTP continuation with a real local index and an offline encoder."""

from copy import deepcopy
import asyncio
from contextlib import contextmanager
import json
import time
from threading import Event

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from bayesian_auditing import benchmark_data, data as legacy_data
from bayesian_auditing.benchmark_index import prepare_benchmark_index as real_prepare
from bayesian_auditing.benchmark_data import row_fingerprint, row_search_text
from website.server import item_review
from website.server.tests.test_item_review import BODY, KEY, HF_KEY, client, finished
from website.server.tests.test_onet_grounding import CANDIDATE, mapping, seed_requirements


def seed_grounding(*, facets=1):
    access = seed_requirements(facets=facets)
    source = item_review.jobs[access["run_id"]]
    source.request = source.request.model_copy(update={"mode": "grounding"})
    source.grounding = {"retrieval": {"fixture": True}, "mapping": {"prompt": "Original mapping prompt"},
                        "facets": [{"facet_id": f"task-{number}", "status": "complete",
                                    "candidates": [deepcopy(CANDIDATE)], "mapping": mapping(f"task-{number}")}
                                   for number in range(facets)]}
    return access


def start_retrieval(client, source, body=None):
    response = client.post(f"/api/item-review/runs/{source['run_id']}/retrieve",
                           json={} if body is None else body,
                           headers={"X-Review-Token": source["run_secret"]})
    assert response.status_code == 202, response.text
    assert response.headers["cache-control"] == "no-store"
    return response.json()


def export(client, access):
    response = client.get(f"/api/item-review/runs/{access['run_id']}/export",
                          headers={"X-Review-Token": access["run_secret"]})
    assert response.status_code == 200, response.text
    return response


@pytest.fixture
def full_bank(client, monkeypatch, tmp_path):
    """More than 50 rows in one collection, including cross-source duplicates."""
    rows = [{"evidence": {"item": {"item_id": f"math-{number:03d}", "benchmark_id": "matharena",
                                  "content": f"Explain mathematics exercise {number}.",
                                  "grading_criterion": "fixture answer", "raw_item_id": str(number),
                                  "new_column": '{ "original_spacing": true }'}},
             "source": {"benchmark": "matharena", "branch": "main", "row": number}}
            for number in range(55)]
    rows.append({**deepcopy(rows[0]), "source": {"benchmark": "coding", "branch": "main", "row": 0}})
    for name in ("coding", "customer_support"):
        rows.append({"evidence": {"item": {"item_id": name, "content": f"Explain {name}.",
                                            "grading_criterion": "fixture answer", "release": "withheld"}},
                     "source": {"benchmark": name, "branch": "main", "row": 1}})
    for row in rows:
        row["evidence_hash"] = row_fingerprint(row["evidence"]["item"])
    inventory = {"repo": "fixture", "branches": {"main": "fixed-a"},
                 "missing_item_tables": [], "tables": [
                     {"benchmark": name, "branch": branch, "commit": commit,
                      "items_path": f"{name}/items.parquet",
                      "row_count": sum(row["source"]["benchmark"] == name for row in rows)}
                     for name, branch, commit in [("matharena", "main", "fixed-a"),
                                                  ("coding", "main", "fixed-a"),
                                                  ("customer_support", "main", "fixed-a")]]}
    calls, builds = [], []

    def iter_items(selected, *, token, streaming):
        assert token == HF_KEY and streaming is True
        calls.append(deepcopy(selected))
        names = {table["benchmark"] for table in selected["tables"]}
        return (deepcopy(row) for row in rows if row["source"]["benchmark"] in names)

    class Encoder:
        dimensions = 2
        cache_namespace = "website-benchmark-retrieval-tests"

        def encode(self, texts):
            return np.asarray([[1., 0.] for _ in texts], dtype=np.float32)

    def prepare(items, cache_dir=None, inventory=None, encoder=None, cancelled=None, progress=None):
        builds.append(deepcopy(inventory))
        return real_prepare(items, tmp_path / "index", inventory, Encoder(), cancelled, progress)

    def forbidden(*args, **kwargs):
        pytest.fail("Benchmark retrieval must not call a model or seeded sample preparation")

    monkeypatch.setattr(item_review, "inventory", lambda: deepcopy(inventory))
    monkeypatch.setattr(item_review, "iter_benchmark_items", iter_items)
    monkeypatch.setattr(item_review, "prepare_benchmark_index", prepare)
    for name in ("AsyncOpenAI", "AsyncJudge", "AsyncRequirementExtractor", "AsyncOnetMapper",
                 "prepare_samples", "iter_sample_items", "review_items"):
        monkeypatch.setattr(item_review, name, forbidden)
    monkeypatch.setattr(legacy_data, "iter_items", forbidden)
    monkeypatch.setattr(legacy_data, "_context", forbidden)
    return {"calls": calls, "builds": builds, "prepare": prepare, "rows": rows}


def test_continuation_searches_every_collection_and_preserves_full_rows(client, full_bank):
    source = seed_grounding(facets=2)
    original = finished(client, source).json()
    access = start_retrieval(client, source)
    result = finished(client, access).json()
    assert result["status"] == "completed" and result["mode"] == "retrieval"
    assert result["source_run_id"] == source["run_id"] and result["usage"] == {}
    for field in ("deployment", "requirements", "extraction", "grounding"):
        assert result[field] == original[field]
    expected_sources = {"matharena", "coding", "customer_support"}
    expected_rows = full_bank["rows"]
    retrieval = result["retrieval"]
    assert set(retrieval["scope"]["benchmarks"]) == expected_sources
    assert retrieval["scope"]["sample_only"] is False
    assert retrieval["scope"]["release_filter"] is None
    assert retrieval["scope"]["branches"] == {"main": "fixed-a"}
    assert retrieval["stats"]["source_rows"] == len(expected_rows)
    assert retrieval["stats"]["indexed_items"] == len({row["evidence_hash"] for row in expected_rows})
    assert len(retrieval["queries"]) == 2
    assert all("mathematical ideas" in query["query"] for query in retrieval["queries"])
    assert "rankings" not in retrieval
    assert "inventory" not in retrieval
    assert all("item_ids" not in queue and "item_count" in queue for queue in retrieval["queues"])
    assert "ranked_items" not in result and "scoring_policy" not in result
    exported = export(client, access).json()["retrieval"]
    assert exported["inventory"] == full_bank["builds"][0]
    assert {table["benchmark"] for table in exported["inventory"]["tables"]} == expected_sources
    assert sum(table["row_count"] for table in exported["inventory"]["tables"]) == len(expected_rows)
    assert all(table["commit"] and table["items_path"] for table in exported["inventory"]["tables"])
    assert len(exported["rankings"]) == 2
    assert all(len(ranking["candidates"]) == retrieval["stats"]["indexed_items"] for ranking in exported["rankings"])
    assert finished(client, source).json() == original
    shared = next(row for row in exported["rankings"][0]["candidates"]
                  if row["item_id"] == full_bank["rows"][0]["evidence_hash"])
    assert {reference["benchmark"] for reference in shared["sources"]} == {"matharena", "coding"}
    assert shared["evidence"]["item"] == full_bank["rows"][0]["evidence"]["item"]
    assert "original_spacing" in shared["search_text"]
    for candidate in exported["rankings"][0]["candidates"]:
        assert candidate["item_id"] == row_fingerprint(candidate["evidence"]["item"])
        assert "grading_criterion" in candidate["search_text"]


def test_http_pipeline_reads_real_parquet_rows_without_projection_or_release_filter(
        client, full_bank, monkeypatch, tmp_path):
    original = {"item_id": "original-id", "benchmark_id": "original-benchmark",
                "raw_item_id": "source-id", "content_hash": "source-provided-hash",
                "content": "  Explain the mathematical idea.\n",
                "grading_criterion": '{ "answer": "exact spelling" }',
                "new_unknown_column": "Every column must survive."}
    changed_id = {**original, "item_id": "a different identifier"}
    changed_json = {**original, "grading_criterion": '{"answer":"exact spelling"}'}
    without_content = {"input": "This complete row has no conventional content or ID columns.",
                       "release": "withheld", "new_unknown_column": "Keep this row as well."}
    tables = {"first": [original, original, changed_id, changed_json],
              "another_source": [original], "no_content_column": [without_content]}
    inventory = {"repo": "fixture", "branches": {"main": "fixed-main"},
                 "missing_item_tables": [], "tables": []}
    for name, rows in tables.items():
        path = f"{name}/formatted_tables/items.parquet"
        local = tmp_path / path
        local.parent.mkdir(parents=True)
        pq.write_table(pa.Table.from_pylist(rows), local, row_group_size=1)
        inventory["tables"].append({"benchmark": name, "branch": "main", "commit": "fixed-main",
                                     "items_path": path, "row_count": len(rows)})
    opened = []

    @contextmanager
    def open_items(actual_inventory, table, *, token, streaming):
        assert actual_inventory == inventory and token == HF_KEY and streaming is True
        opened.append(table["items_path"])
        with pq.ParquetFile(tmp_path / table["items_path"]) as parquet:
            yield parquet

    monkeypatch.setattr(item_review, "inventory", lambda: deepcopy(inventory))
    monkeypatch.setattr(item_review, "iter_benchmark_items", benchmark_data.iter_benchmark_items)
    monkeypatch.setattr(benchmark_data, "open_item_table", open_items)
    access = start_retrieval(client, seed_grounding())
    result = finished(client, access).json()
    assert result["status"] == "completed"
    assert len(opened) == 3
    assert result["retrieval"]["stats"]["source_rows"] == 6
    assert result["retrieval"]["stats"]["indexed_items"] == 4
    assert result["retrieval"]["scope"]["release_filter"] is None
    exported = export(client, access).json()["retrieval"]
    by_id = {item["item_id"]: item for item in exported["rankings"][0]["candidates"]}
    for row in (original, changed_id, changed_json, without_content):
        candidate = by_id[row_fingerprint(row)]
        assert candidate["evidence"] == {"item": row}
        assert candidate["search_text"] == row_search_text(row)
    references = by_id[row_fingerprint(original)]["sources"]
    assert len(references) == 3
    assert {reference["benchmark"] for reference in references} == {"first", "another_source"}
    assert by_id[row_fingerprint(without_content)]["sources"][0]["item_id"] is None
    queue = next(queue for queue in exported["queues"] if queue["source"] is None)
    page = client.get(f"/api/item-review/runs/{access['run_id']}/candidates",
                      params={"queue_id": queue["queue_id"]},
                      headers={"X-Review-Token": access["run_secret"]}).json()
    assert page["items"] == exported["rankings"][0]["candidates"]


def test_export_keeps_one_retrieval_snapshot_and_releases_interrupted_download(client, full_bank):
    access = start_retrieval(client, seed_grounding())
    assert finished(client, access).json()["status"] == "completed"
    job = item_review.jobs[access["run_id"]]
    original = deepcopy(job.benchmark_retrieval)

    async def check_snapshot():
        response = await item_review.export_review(job.run_id, job.secret)
        newer = deepcopy(original)
        newer["queries"] = []
        newer["queues"] = []
        newer["rankings"] = []
        # Workers publish a replacement dictionary, preserving earlier snapshots.
        job.benchmark_retrieval = newer
        text = "".join([chunk async for chunk in response.body_iterator])
        assert json.loads(text)["retrieval"] == original
        assert job.downloads == 0
        response = await item_review.export_review(job.run_id, job.secret)
        await response.body_iterator.__anext__()
        await response.body_iterator.aclose()
        assert job.downloads == 0

    asyncio.run(check_snapshot())


@pytest.mark.parametrize("body", [
    {"benchmarks": None}, {"benchmarks": ["matharena"]},
    {"benchmarks": []}, {"benchmarks": ["matharena", "matharena"]}, {"benchmarks": ["unknown"]},
    {"benchmarks": [1]}, {"benchmarks": "matharena"}, {"retrieve_k": 20},
])
def test_retrieval_request_rejects_invalid_scope_and_extra_settings(client, full_bank, body):
    source = seed_grounding()
    response = client.post(f"/api/item-review/runs/{source['run_id']}/retrieve", json=body,
                           headers={"X-Review-Token": source["run_secret"]})
    assert response.status_code == 422
    assert not full_bank["calls"] and not full_bank["builds"]


@pytest.mark.parametrize("problem", ["extra_branch", "wrong_table_commit", "wrong_table_branch"])
def test_retrieval_rejects_inventory_that_is_not_one_pinned_main(client, full_bank, monkeypatch, problem):
    source = seed_grounding()
    data = item_review.inventory()
    if problem == "extra_branch":
        data["branches"]["migration"] = "another-commit"
    elif problem == "wrong_table_commit":
        data["tables"][0]["commit"] = "another-commit"
    else:
        data["tables"][0]["branch"] = "migration"
    monkeypatch.setattr(item_review, "inventory", lambda: deepcopy(data))
    response = client.post(f"/api/item-review/runs/{source['run_id']}/retrieve", json={},
                           headers={"X-Review-Token": source["run_secret"]})
    assert response.status_code == 503
    assert not full_bank["calls"] and not full_bank["builds"]


@pytest.mark.parametrize("problem", [
    "not_finished", "failed_grounding", "no_grounding", "incomplete_mapping", "missing_facet",
    "invalid_passage", "bad_requirement_evidence", "no_tasks", "extraction_only",
])
def test_invalid_or_incomplete_parent_cannot_start_retrieval(client, full_bank, problem):
    source = seed_grounding(facets=2)
    job = item_review.jobs[source["run_id"]]
    if problem == "not_finished":
        job.finished_at = None
    elif problem == "failed_grounding":
        job.status = "failed"
    elif problem == "no_grounding":
        job.grounding = None
    elif problem == "incomplete_mapping":
        job.grounding["facets"][1]["status"] = "error"
    elif problem == "missing_facet":
        job.grounding["facets"].pop()
    elif problem == "invalid_passage":
        job.grounding["facets"][1]["mapping"]["records"][0]["supporting_passage"] += " fabricated extension"
    elif problem == "bad_requirement_evidence":
        job.requirements["workflow"]["evidence"][0]["quote"] = "invented evidence"
    elif problem == "no_tasks":
        job.requirements["task_facets"] = []
        job.grounding["facets"] = []
    elif problem == "extraction_only":
        job.request = job.request.model_copy(update={"mode": "requirements"})
    response = client.post(f"/api/item-review/runs/{source['run_id']}/retrieve", json={},
                           headers={"X-Review-Token": source["run_secret"]})
    assert response.status_code == 409
    assert not full_bank["calls"] and not full_bank["builds"]


def test_no_matching_onet_records_still_retrieves_existing_requirements(client, full_bank):
    source = seed_grounding()
    mapped = item_review.jobs[source["run_id"]].grounding["facets"][0]["mapping"]
    mapped["records"] = []
    mapped["unresolved_details"] = ["No occupation record applies to the task."]
    result = finished(client, start_retrieval(client, source)).json()
    assert result["status"] == "completed"
    assert result["retrieval"]["queries"][0]["search_terms"] == []


def test_dataset_access_and_source_token_are_required_but_provider_key_is_not(client, full_bank, monkeypatch):
    source = seed_grounding()
    url = f"/api/item-review/runs/{source['run_id']}/retrieve"
    assert client.post(url, json={}).status_code == 404
    assert client.post(url, json={}, headers={"X-Review-Token": "wrong"}).status_code == 404
    monkeypatch.setattr(item_review, "get_token", lambda: None)
    assert client.post(url, json={}, headers={"X-Review-Token": source["run_secret"]}).status_code == 503
    assert not full_bank["calls"] and not full_bank["builds"]
    monkeypatch.setattr(item_review, "get_token", lambda: HF_KEY)
    assert finished(client, start_retrieval(client, source)).json()["status"] == "completed"
    assert client.post("/api/item-review/runs", json={**BODY, "mode": "retrieval"},
                       headers={"X-OpenAI-Key": KEY}).status_code == 400


def test_candidate_paging_and_full_export_require_run_token(client, full_bank):
    source = seed_grounding()
    access = start_retrieval(client, source)
    result = finished(client, access).json()
    queue = next(queue for queue in result["retrieval"]["queues"] if queue["source"] is None)
    url = f"/api/item-review/runs/{access['run_id']}/candidates"
    headers = {"X-Review-Token": access["run_secret"]}
    params = {"queue_id": queue["queue_id"]}
    assert client.get(url, params=params).status_code == 404
    assert client.get(url, params=params, headers={"X-Review-Token": source["run_secret"]}).status_code == 404
    assert client.get(url, params={"queue_id": "unknown"}, headers=headers).status_code == 404
    assert client.get(url, params={**params, "page": 0}, headers=headers).status_code == 422
    pages = []
    for page in (1, 2, 3):
        response = client.get(url, params={**params, "page": page}, headers=headers)
        assert response.status_code == 200 and response.headers["cache-control"] == "no-store"
        value = response.json()
        assert value["page"] == page and value["total_pages"] == 3 and value["total_items"] == 57
        assert value["page_size"] == 20
        pages.extend(value["items"])
    assert len({row["item_id"] for row in pages}) == 57
    exported = export(client, access)
    assert "benchmark-retrieval-" in exported.headers["content-disposition"]
    assert exported.headers["cache-control"] == "no-store"
    assert exported.json()["retrieval"]["rankings"][0]["candidates"] == pages
    assert len(exported.json()["retrieval"]["queues"][0]["item_ids"]) == 57
    assert client.get(f"/api/item-review/runs/{access['run_id']}/export").status_code == 404
    for secret in (KEY, HF_KEY, source["run_secret"], access["run_secret"]):
        assert secret not in exported.text
    item_review.jobs[access["run_id"]].finished_at = time.monotonic() - item_review.RETENTION_SECONDS - 1
    assert client.get(url, params=params, headers=headers).status_code == 404


def test_worker_failure_is_sanitized_and_failed_retrieval_can_be_retried(client, full_bank, monkeypatch):
    source = seed_grounding()
    original = finished(client, source).json()
    def broken(*args, **kwargs):
        raise ValueError(f"private index failure {KEY} {HF_KEY}")
    monkeypatch.setattr(item_review, "prepare_benchmark_index", broken)
    failed = start_retrieval(client, source)
    failure = finished(client, failed)
    assert failure.json()["status"] == "failed"
    assert KEY not in failure.text and HF_KEY not in failure.text
    monkeypatch.setattr(item_review, "prepare_benchmark_index", full_bank["prepare"])
    retried = start_retrieval(client, failed)
    assert finished(client, retried).json()["status"] == "completed"
    assert finished(client, source).json() == original


def test_worker_cancellation_keeps_completed_facet_and_allows_retry(client, full_bank, monkeypatch):
    source = seed_grounding(facets=2)
    entered, closed = Event(), Event()
    class SlowIndex:
        def __init__(self, index):
            self.index = index
            self.policy, self.stats = index.policy, index.stats
            self.calls = 0

        def search(self, query, *, cancelled):
            self.calls += 1
            if self.calls == 2:
                entered.set()
                deadline = time.monotonic() + 3
                while not cancelled() and time.monotonic() < deadline:
                    time.sleep(.01)
                assert cancelled(), "Cancellation did not reach the benchmark search worker"
                raise InterruptedError("Cancelled")
            return self.index.search(query, cancelled=cancelled)

        def close(self):
            self.index.close()
            closed.set()

    monkeypatch.setattr(item_review, "prepare_benchmark_index",
                        lambda *args, **kwargs: SlowIndex(full_bank["prepare"](*args, **kwargs)))
    access = start_retrieval(client, source)
    assert entered.wait(2)
    duplicate = client.post(f"/api/item-review/runs/{source['run_id']}/retrieve", json={},
                            headers={"X-Review-Token": source["run_secret"]})
    assert duplicate.status_code == 429
    stopped = client.post(f"/api/item-review/runs/{access['run_id']}/cancel",
                          headers={"X-Review-Token": access["run_secret"]})
    assert stopped.status_code == 200 and stopped.json()["status"] == "cancelled"
    assert closed.is_set()
    saved = export(client, access).json()["retrieval"]
    assert len(saved["rankings"]) == 1 and saved["rankings"][0]["facet_id"] == "task-0"
    assert len(saved["rankings"][0]["candidates"]) == 57
    assert saved["queues"] and all(queue["facet_id"] == "task-0" for queue in saved["queues"])
    monkeypatch.setattr(item_review, "prepare_benchmark_index", full_bank["prepare"])
    retried = start_retrieval(client, access)
    result = finished(client, retried).json()
    assert result["status"] == "completed" and result["retrieval"]["stats"]["cache_hit"] is True
    assert len(export(client, retried).json()["retrieval"]["rankings"]) == 2
