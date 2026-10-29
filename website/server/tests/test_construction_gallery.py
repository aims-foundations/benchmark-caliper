"""Curated construction pages preserve exports without accessing private runs."""

from copy import deepcopy
import hashlib
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from website.scripts import import_construction_example as importer
from website.server import construction_gallery as gallery, item_review, result_package
from website.server.tests.test_adaptive_screening import seed_selected


@pytest.fixture
def source_snapshot(monkeypatch):
    monkeypatch.setattr(item_review, "jobs", {})
    access = seed_selected(facets=2, per_facet=20)
    job = item_review.jobs[access["run_id"]]
    value = deepcopy(item_review.public_job(job))
    value["retrieval"] = deepcopy(job.benchmark_retrieval)
    return value


def write_export(path, snapshot):
    path.mkdir()
    with result_package.build_results_package(snapshot) as output, ZipFile(output) as archive:
        for name in archive.namelist():
            (path / name).write_bytes(archive.read(name))
    return path


def publish(source, root, **options):
    return importer.import_example(source, "clinical-exam-study", title="Clinical exam study with management constraints",
                                   description="Saved example for review.", output_dir=root, **options)


def public_client(monkeypatch, root):
    monkeypatch.setattr(gallery, "ROOT", root)
    app = FastAPI()
    app.include_router(gallery.router)
    return TestClient(app)


def test_import_preserves_artifacts_and_public_page_loads_only_selected_items(tmp_path, monkeypatch, source_snapshot):
    source = write_export(tmp_path / "source", source_snapshot)
    originals = {name: (source / name).read_bytes() for name in importer.FILES}
    root = tmp_path / "published"
    entry = publish(source, root)
    assert entry["assessed_count"] == 40 and entry["selected_count"] == 30
    assert entry["coverage_complete"] is True
    assert not (root / entry["id"] / "results.json").exists()
    assert len(list((root / entry["id"] / "items").glob("*.json.gz"))) == 40
    for key, filename in (("report", "report.html"), ("items", "selected_items.csv"), ("results", "results.json")):
        assert entry["artifacts"][key]["sha256"] == hashlib.sha256(originals[filename]).hexdigest()
    archive_path = root / entry["id"] / "complete-results.zip"
    with ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        assert {name: archive.read(name) for name in archive.namelist()} == originals

    for name in ("authorize", "AsyncOpenAI", "restore_review", "launch_review"):
        monkeypatch.setattr(item_review, name, lambda *args, **kwargs: pytest.fail("Public gallery cannot use private run machinery"))
    client = public_client(monkeypatch, root)
    base = "/api/item-review/examples"
    assert client.get(base).json() == {"examples": [entry]}
    data = client.get(base + "/" + entry["id"]).json()
    assert data["entry"] == entry and len(data["items"]) == 40
    selected = set(source_snapshot["selection"]["selected_item_ids"])
    assert {item["item_id"] for item in data["review"]["screening"]["items"]} == selected
    assert data["review"]["selection"] == source_snapshot["selection"]
    assert data["review"]["requirements"] == source_snapshot["requirements"]
    assert data["review"]["grounding"] == source_snapshot["grounding"]
    assert "rankings" not in data["review"]["retrieval"]
    assert all("item_ids" not in queue and queue["item_count"] == 20 for queue in data["review"]["retrieval"]["queues"])
    assert [query["candidate_count"] for query in data["review"]["retrieval"]["queries"]] == [20, 20]
    assert [item["index"] for item in data["items"]] == list(range(40))
    assert all(item["initial"] for item in data["items"])
    omitted = next(item for item in source_snapshot["screening"]["items"] if item["item_id"] not in selected)
    summary = next(item for item in data["items"] if item["item_id"] == omitted["item_id"])
    assert summary["sources"] == ["fixture"] and not summary["selected"]
    assert summary["gate"] == "pass" and summary["quality_score"] == 4
    assert client.get(base + f"/{entry['id']}/items/{omitted['item_id']}").json() == omitted

    for key, original in (("report", originals["report.html"]), ("items", originals["selected_items.csv"]),
                          ("results", originals["results.json"]), ("package", archive_path.read_bytes())):
        response = client.get(base + f"/{entry['id']}/artifacts/{key}")
        assert response.status_code == 200 and response.content == original
        if key == "report":
            assert "sandbox" in response.headers["content-security-policy"]
            assert "inline" in response.headers["content-disposition"]


def test_original_zip_is_copied_byte_for_byte_and_chunk_reads_are_bounded(tmp_path, monkeypatch, source_snapshot):
    folder = write_export(tmp_path / "source", source_snapshot)
    source = tmp_path / "original.zip"
    with ZipFile(source, "w", compression=ZIP_DEFLATED) as archive:
        for name in importer.FILES:
            archive.write(folder / name, "original-folder/" + name)
    root = tmp_path / "published"
    entry = publish(source, root)
    assert (root / entry["id"] / "complete-results.zip").read_bytes() == source.read_bytes()
    client = public_client(monkeypatch, root)
    base = "/api/item-review/examples/clinical-exam-study"
    package = entry["artifacts"]["package"]
    assert package["package_id"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert package["chunk_bytes"] == 1048576
    original = source.read_bytes()
    assert client.get(base + "/artifacts/results").content == (folder / "results.json").read_bytes()
    # A smaller test bound exercises several independent offsets and retries.
    monkeypatch.setattr(gallery, "CHUNK_BYTES", 1024)
    parts = []
    for offset in range(0, package["bytes"], 1024):
        response = client.get(base + "/package/chunk", params={"package_id": package["package_id"], "offset": offset})
        assert response.status_code == 200
        assert response.headers["x-package-id"] == package["package_id"]
        assert response.headers["x-package-offset"] == str(offset)
        assert len(response.content) == int(response.headers["content-length"]) == min(1024, package["bytes"] - offset)
        assert response.content == original[offset:offset + 1024]
        parts.append(response.content)
    assert b"".join(parts) == original
    assert client.get(base + "/package/chunk", params={"package_id": "wrong", "offset": 0}).status_code == 412
    for offset in (-1, package["bytes"], "invalid"):
        assert client.get(base + "/package/chunk", params={"package_id": package["package_id"], "offset": offset}).status_code == 416


@pytest.mark.parametrize("change", ["duplicate", "row", "selected_id", "selected_count", "task_count", "quality", "assessed_count", "csv"])
def test_invalid_source_is_rejected_without_replacing_an_existing_publication(tmp_path, source_snapshot, change):
    original_source = write_export(tmp_path / "original", source_snapshot)
    root = tmp_path / "published"
    publish(original_source, root)
    original_index = (root / "index.json").read_bytes()
    original_snapshot = (root / "clinical-exam-study" / "snapshot.json").read_bytes()
    changed = deepcopy(source_snapshot)
    if change == "duplicate": changed["screening"]["items"].append(deepcopy(changed["screening"]["items"][0]))
    elif change == "row": changed["screening"]["items"][0]["evidence"]["item"]["content"] = "Different original content"
    elif change == "selected_id": changed["selection"]["selected_item_ids"][0] = "unknown-item"
    elif change == "selected_count": changed["selection"]["selected_count"] += 1
    elif change == "task_count": changed["selection"]["task_coverage"][0]["selected_count"] += 1
    elif change == "quality": changed["selection"]["total_quality"] += 1
    elif change == "assessed_count": changed["selection_input"]["screened"] += 1
    source = write_export(tmp_path / "changed", changed)
    if change == "csv":
        (source / "selected_items.csv").write_text("item_id\nwrong-id\n")
    with pytest.raises(ValueError):
        publish(source, root, overwrite=True)
    assert (root / "index.json").read_bytes() == original_index
    assert (root / "clinical-exam-study" / "snapshot.json").read_bytes() == original_snapshot
    assert not list(root.glob(".construction-import-*"))


def test_overwrite_is_explicit_and_published_id_is_not_a_path(tmp_path, monkeypatch, source_snapshot):
    source = write_export(tmp_path / "source", source_snapshot)
    root = tmp_path / "published"
    publish(source, root)
    with pytest.raises(ValueError, match="already exists"):
        publish(source, root)
    importer.import_example(source, "clinical-exam-study", title="Updated display title", description="Same saved results.",
                            output_dir=root, overwrite=True)
    client = public_client(monkeypatch, root)
    assert client.get("/api/item-review/examples").json()["examples"][0]["title"] == "Updated display title"
    for path in ("/unknown", "/clinical-exam-study/artifacts/secrets", "/clinical-exam-study/items/not-a-published-id"):
        assert client.get("/api/item-review/examples" + path).status_code == 404
    with pytest.raises(ValueError):
        importer.import_example(source, "../escape", title="Title", description="Description", output_dir=root)
    with pytest.raises(ValueError):
        link = tmp_path / "linked-export"
        link.symlink_to(source, target_is_directory=True)
        publish(link, root, overwrite=True)


def test_unsafe_or_incomplete_archives_cannot_be_published(tmp_path):
    for number, members in enumerate((
        {"../report.html": b"report", "../selected_items.csv": b"csv", "../results.json": b"{}"},
        {"report.html": b"report", "results.json": b"{}"},
    )):
        source = tmp_path / f"source-{number}.zip"
        with ZipFile(source, "w") as archive:
            for name, content in members.items():
                archive.writestr(name, content)
        root = tmp_path / f"published-{number}"
        with pytest.raises(ValueError):
            publish(source, root)
        assert not (root / "index.json").exists()


def test_results_parser_uses_bounded_reads_and_discards_retrieval_payloads(tmp_path, source_snapshot):
    original = deepcopy(source_snapshot)
    original["retrieval"]["rankings"][0]["candidates"][0]["large_original_field"] = "x" * 2_000_000
    raw = json.dumps(original).encode()

    class BoundedReader(BytesIO):
        def read(self, size=-1):
            assert 0 <= size <= streaming_json.CHUNK_BYTES
            return super().read(size)

        def readinto(self, buffer):
            assert len(buffer) <= streaming_json.CHUNK_BYTES
            return super().readinto(buffer)

    from website.server import streaming_json
    snapshot = importer.derive_snapshot(BoundedReader(raw), tmp_path)
    assert "rankings" not in snapshot["review"]["retrieval"]
    assert "large_original_field" not in json.dumps(snapshot)
    assert len(snapshot["items"]) == 40
