"""Public retrieval browsing preserves saved queues and reads bounded evidence."""

from contextlib import closing
from copy import deepcopy
import gzip
import json
import sqlite3

import pytest

from bayesian_auditing.benchmark_data import row_fingerprint
from website.server import construction_gallery as gallery, construction_retrieval as retrieval
from website.server.tests.test_construction_gallery import public_client, publish, source_snapshot, write_export


def candidate(question, source, rank):
    row = {"question": question, "answer": "Saved answer", "metadata": {"nullable": None, "enabled": False}}
    item_id = row_fingerprint(row)
    return {"item_id": item_id, "evidence_hash": item_id, "evidence": {"item": row},
            "question_text": question, "search_text": json.dumps(row),
            "sources": [{"benchmark": source, "row": 7}],
            "rank": rank, "dense_rank": None, "bm25_rank": rank, "dense_score": None,
            "bm25_score": 2.25, "rrf_score": .01, "additional_field": {"keep": [False, None, 2.0]}}


@pytest.fixture
def public_data(tmp_path, monkeypatch):
    first = candidate("Which test should be ordered?", "source_a", 3)
    second = candidate("Which treatment should be used?", "source_b", 9)
    shared = {**deepcopy(first), "rank": 17, "dense_score": .9, "additional_field": {"keep": "Other task"}}
    third = candidate("Which diagnosis fits?", "source_a", 21)
    rankings = [{"facet_id": "diagnosis", "candidates": [second, first]},
                {"facet_id": "management", "candidates": [shared, third]}]
    queues = [{"queue_id": "diagnosis-all", "facet_id": "diagnosis", "source": None,
               "item_ids": [second["item_id"], first["item_id"]]},
              {"queue_id": "diagnosis-source-a", "facet_id": "diagnosis", "source": "source_a",
               "item_ids": [first["item_id"]]},
              {"queue_id": "management-all", "facet_id": "management", "source": None,
               "item_ids": [shared["item_id"], third["item_id"]]}]
    root = tmp_path / "public"
    directory = root / "another-example"
    directory.mkdir(parents=True)
    (root / "index.json").write_text(json.dumps({"schema_version": 1, "examples": [{"id": "another-example"}]}))
    path = directory / retrieval.FILENAME
    with closing(retrieval.Builder(path)) as builder:
        for index, ranking in enumerate(rankings):
            for position, item in enumerate(ranking["candidates"]):
                builder.add(index, position, item)
        builder.finish({"rankings": rankings, "queues": queues})
    client = public_client(monkeypatch, root)
    return client, path, rankings, queues


def test_pages_follow_saved_queue_order_and_do_not_load_evidence(public_data, monkeypatch):
    client, path, rankings, queues = public_data
    monkeypatch.setattr(gzip, "decompress", lambda *args: pytest.fail("A page must not decompress candidate evidence"))
    monkeypatch.setattr(gallery, "snapshot", lambda *args: pytest.fail("Retrieval pages must not load the full review snapshot"))
    base = "/api/item-review/examples/another-example/retrieved"
    response = client.get(base, params={"page": 2, "page_size": 1})
    assert response.status_code == 200
    page = response.json()
    assert page["queue_id"] == "diagnosis-all" and page["facet_id"] == "diagnosis" and page["source"] is None
    assert page["total"] == page["total_pages"] == 2 and page["unique_candidate_count"] == 3
    assert page["items"][0]["item_id"] == rankings[0]["candidates"][1]["item_id"]
    assert page["items"][0]["queue_rank"] == 2 and page["items"][0]["rank"] == 3
    assert page["items"][0]["dense_rank"] is None and "evidence" not in page["items"][0]
    assert client.get(base, params={"page": 3, "page_size": 1}).json()["items"] == []
    source_page = client.get(base, params={"queue_id": queues[1]["queue_id"]}).json()
    assert source_page["source"] == "source_a" and source_page["total"] == 1
    assert source_page["items"][0]["queue_rank"] == 1
    for parameters in ({"page": 0}, {"page_size": 51}, {"page_size": 0}, {"page": str(2**100)}):
        assert client.get(base, params=parameters).status_code == 422


def test_exact_records_share_payloads_but_keep_task_specific_metadata(public_data, monkeypatch):
    client, path, rankings, queues = public_data
    with closing(sqlite3.connect(path)) as database:
        assert database.execute("SELECT count(*) FROM candidates").fetchone()[0] == 4
        assert database.execute("SELECT count(*) FROM payloads").fetchone()[0] == 3
    original = gzip.decompress
    calls = []

    def decompress(data):
        calls.append(len(data))
        return original(data)

    monkeypatch.setattr(gzip, "decompress", decompress)
    base = "/api/item-review/examples/another-example/retrieved"
    for ranking, queue in zip(rankings, (queues[0], queues[2])):
        for item in ranking["candidates"]:
            response = client.get(base + "/" + item["item_id"], params={"queue_id": queue["queue_id"]})
            assert response.status_code == 200 and response.json() == item
    assert len(calls) == 4  # Only the requested candidate is decompressed.


def test_membership_publication_and_corrupt_data_have_safe_errors(public_data):
    client, path, rankings, queues = public_data
    base = "/api/item-review/examples/another-example/retrieved"
    wrong_source = rankings[0]["candidates"][0]["item_id"]
    assert client.get(base + "/" + wrong_source, params={"queue_id": queues[1]["queue_id"]}).status_code == 404
    assert client.get(base + "/unknown-item").status_code == 404
    assert client.get(base, params={"queue_id": "' OR 1=1 --"}).status_code == 404
    assert client.get(base.replace("another-example", "not-published")).status_code == 404
    with closing(sqlite3.connect(path)) as database:
        database.execute("UPDATE payloads SET data = ?", (b"invalid compressed content",))
        database.commit()
    failed = client.get(base + "/" + wrong_source)
    assert failed.status_code == 503 and str(path) not in failed.text
    path.write_bytes(b"not a database")
    assert client.get(base).status_code == 503


def test_imported_examples_expose_every_retrieved_candidate_without_changing_exports(tmp_path, monkeypatch, source_snapshot):
    source = write_export(tmp_path / "source", source_snapshot)
    root = tmp_path / "published"
    publish(source, root)
    original = (source / "results.json").read_bytes()
    client = public_client(monkeypatch, root)
    base = "/api/item-review/examples/clinical-exam-study"
    for ranking in source_snapshot["retrieval"]["rankings"]:
        queue = next(queue for queue in source_snapshot["retrieval"]["queues"] if queue["facet_id"] == ranking["facet_id"])
        pages = [client.get(base + "/retrieved", params={"queue_id": queue["queue_id"], "page": number, "page_size": 7}).json()
                 for number in (1, 2, 3)]
        assert [item["item_id"] for page in pages for item in page["items"]] == queue["item_ids"]
        for item in ranking["candidates"]:
            assert client.get(base + "/retrieved/" + item["item_id"], params={"queue_id": queue["queue_id"]}).json() == item
    assert client.get(base + "/artifacts/results").content == original


@pytest.mark.parametrize("fault", ["missing_item", "wrong_source", "reversed_queue", "duplicate_candidate", "changed_row"])
def test_invalid_retrieval_cannot_replace_an_existing_publication(tmp_path, source_snapshot, fault):
    source = write_export(tmp_path / "source", source_snapshot)
    root = tmp_path / "published"
    publish(source, root)
    original_catalog = (root / "index.json").read_bytes()
    database = root / "clinical-exam-study" / retrieval.FILENAME
    original_data = database.read_bytes()
    changed = deepcopy(source_snapshot)
    ranking = changed["retrieval"]["rankings"][0]
    queue = changed["retrieval"]["queues"][0]
    if fault == "missing_item": queue["item_ids"].append("missing")
    elif fault == "wrong_source": queue["source"] = "wrong-source"
    elif fault == "reversed_queue": queue.update(source=None, item_ids=list(reversed(queue["item_ids"])))
    elif fault == "duplicate_candidate": ranking["candidates"].append(deepcopy(ranking["candidates"][0]))
    elif fault == "changed_row": ranking["candidates"][0]["evidence"]["item"]["extra"] = "changed"
    invalid = write_export(tmp_path / "invalid", changed)
    with pytest.raises(ValueError):
        publish(invalid, root, overwrite=True)
    assert (root / "index.json").read_bytes() == original_catalog
    assert database.read_bytes() == original_data
