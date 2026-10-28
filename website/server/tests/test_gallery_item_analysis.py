"""Publication validates saved evidence; public reads never resume private runs."""

from copy import deepcopy
import csv
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import pytest
from fastapi.testclient import TestClient

from anthropic_api_package_release.item_analysis import scoring
from website.scripts.import_gallery_item_analysis import import_snapshot, read_export, validate_export
from website.server import app as app_module, gallery, gallery_item_analysis


def encode(value):
    return json.dumps(value).encode()


def refresh_manifest(files):
    manifest = json.loads(files["manifest.json"])
    manifest["artifacts"] = [
        {"path": name, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
        for name, content in sorted(files.items()) if name != "manifest.json"
    ]
    files["manifest.json"] = encode(manifest)


@pytest.fixture
def export(tmp_path, monkeypatch):
    assessments = tmp_path / "assessments"
    deployment = "Test deployment with expert statistical users."
    benchmark_scores = {"dimensions": {key: {"score": 2} for key in scoring.DIMENSIONS}}
    for entry_id in ("gsm8k", "other"):
        directory = assessments / entry_id / "test-deployment"
        directory.mkdir(parents=True)
        (directory / "scoring.json").write_bytes(encode(benchmark_scores))
        (directory / "deployment_description.txt").write_text(deployment)
    monkeypatch.setattr(gallery, "_ASSESSMENTS_ROOT", assessments)
    monkeypatch.setattr(gallery_item_analysis, "SNAPSHOT_ROOT", tmp_path / "publications")
    gallery.list_entries.cache_clear()
    spec = {
        "schema_version": scoring.CONTEXT_SCHEMA_VERSION, "analysis_type": "six_scores",
        "rubric_version": scoring.RUBRIC_VERSION, "benchmark": "gsm8k",
        "deployment": deployment, "deployment_description": deployment,
        "analysis_basis": "benchmark_assessment", "assessment_status": "complete",
        "dataset_profile": {}, "source_registry": {}, "source_roles": {},
        "classifiers": scoring.dimension_descriptors(),
    }
    source_items = [{"item_id": str(index), "content": f"Question {index}", "reference_answer": "4"}
                    for index in range(3)]
    results = [{"item_id": str(index), "status": "complete", "dimensions": {
        key: {"score": None if index == 1 else 4, "justification": "Saved evidence assessment.",
              "evidence": ["item.content"] if index == 0 else [],
              "information_gaps": [] if index == 0 else ["Reference interpretation is unavailable."]}
        for key in scoring.DIMENSIONS
    }} for index in range(2)]
    items_jsonl = b"\n".join(encode(item) for item in source_items) + b"\n"
    dataset = {"benchmark": "gsm8k", "item_count": 3, "assessment": {"kind": "gallery", "id": "gsm8k"},
               "benchmark_identity_confirmed": True, "source": {"revision": "frozen-revision"},
               "items_sha256": hashlib.sha256(items_jsonl).hexdigest()}
    counts = {
        "selected_items": 2, "selected_completed_items": 2, "selected_error_items": 0,
        "selected_partial_items": 0, "selected_pending_items": 0, "dimension_count": 6,
        "expected_item_classifier_judgments": 12, "completed_item_classifier_judgments": 12,
        "error_item_classifier_judgments": 0, "invalid_item_classifier_judgments": 0,
        "pending_item_classifier_judgments": 0,
    }
    dimensions = [{"id": key, "known": 1, "unknown": 1, "mean_score": 4.0,
                   "counts": {str(score): int(score == 4) for score in range(1, 6)},
                   "errors": 0, "pending": 0, "invalid": 0} for key in scoring.DIMENSIONS]
    shared = {"benchmark": "gsm8k", "deployment": deployment, "analysis_type": "six_scores",
              "rubric_version": scoring.RUBRIC_VERSION, "dataset": dataset}
    summary = {**shared, "original_assessment": benchmark_scores["dimensions"], "total_items": 3,
               "completed_items": 2, "error_items": 0, "pending_items": 1, "dimensions": dimensions,
               "classifiers": dimensions, "experiment": counts, "run": {"run_id": "saved-run"}}
    manifest = {**shared, "run_id": "saved-run", "selected_item_ids": ["0", "1"],
                "counts": {**counts, "prepared_items": 3}, "updated_at": "2026-10-28T20:00:00+00:00",
                "model": {"model_id": "offline-model"}, "artifacts": []}
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=["item_id", "status", *(key + ".score" for key in scoring.DIMENSIONS)])
    writer.writeheader()
    for index in range(3):
        writer.writerow({"item_id": str(index), "status": "complete" if index < 2 else "pending",
                         **{key + ".score": "4" if index == 0 else "unknown" if index == 1 else ""
                            for key in scoring.DIMENSIONS}})
    files = {
        "manifest.json": encode(manifest), "classifier_spec.json": encode(spec),
        "summary.json": encode(summary), "audit/dataset.json": encode(dataset),
        "original_assessment.json": encode({"benchmark": "gsm8k", "deployment": deployment, "scoring": benchmark_scores}),
        "audit/items.jsonl": items_jsonl, "audit/results.jsonl": b"\n".join(encode(row) for row in results),
        "items.csv": stream.getvalue().encode(), "report.html": b"<html><body>Saved export</body></html>",
    }
    refresh_manifest(files)
    yield files, tmp_path
    gallery.list_entries.cache_clear()


def write_export(files, destination):
    for name, content in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return destination


def test_publish_completed_sample_unknown_and_public_artifacts(export, monkeypatch):
    files, tmp_path = export
    source = write_export(files, tmp_path / "export")
    metadata = import_snapshot(source, "gsm8k")
    assert metadata["item_count"] == 2 and metadata["total_items"] == 3
    assert metadata["model"] == "offline-model"
    # A public page cannot call or resume the private run machinery.
    monkeypatch.setattr(app_module.item_analysis, "authorize", lambda *args, **kwargs: pytest.fail("private run accessed"))
    monkeypatch.setattr(app_module.item_analysis, "model_bridge", lambda *args, **kwargs: pytest.fail("model accessed"))
    client = TestClient(app_module.app)
    report = client.get("/api/gallery/gsm8k")
    assert report.status_code == 200 and report.json()["item_analysis"]["item_count"] == 2
    response = client.get("/api/gallery/gsm8k/item-analysis")
    assert response.status_code == 200
    data = response.json()
    assert [item["item_id"] for item in data["items"]] == ["0", "1"]
    assert data["items"][1]["dimensions"]["input_form"]["score"] is None
    assert data["summary"]["dimensions"][0]["mean_score"] == 4
    assert data["dataset"]["source"]["revision"] == "frozen-revision"
    assert response.headers["Content-Security-Policy"] == app_module.SECURITY_HEADERS["Content-Security-Policy"]
    for artifact in gallery_item_analysis.ARTIFACTS:
        download = client.get(f"/api/gallery/gsm8k/item-analysis/artifacts/{artifact}")
        assert download.status_code == 200
        assert download.headers["X-Content-Type-Options"] == "nosniff"
        if artifact == "items":
            rows = list(csv.DictReader(io.StringIO(download.text)))
            assert [row["item_id"] for row in rows] == ["0", "1"]
        elif artifact == "report":
            assert download.content == files["report.html"]
            assert download.headers["Content-Security-Policy"].startswith("sandbox;")
            assert "default-src 'none'" in download.headers["Content-Security-Policy"]
        elif artifact == "package":
            with ZipFile(io.BytesIO(download.content)) as archive:
                assert {name: archive.read(name) for name in archive.namelist()} == files
    assert "item_analysis" not in client.get("/api/gallery/other").json()
    for path in (
        "/api/gallery/other/item-analysis", "/api/gallery/unknown/item-analysis",
        "/api/gallery/unknown/item-analysis/artifacts/package",
        "/api/gallery/gsm8k/item-analysis/artifacts/manifest",
        "/api/gallery/gsm8k/item-analysis/artifacts/..%2F..%2Fmetadata.json",
        "/api/gallery/..%2F..%2Fetc%2Fpasswd/item-analysis",
    ):
        assert client.get(path).status_code == 404


@pytest.mark.parametrize("change, message", [
    ("checksum", "integrity"), ("assessment", "different gallery"),
    ("deployment", "deployment differs"), ("scores", "gallery scores"),
    ("mean", "average differs"), ("duplicate", "Duplicate selected"),
    ("incomplete", "not complete"), ("credential", "Possible credential"),
    ("run_secret", "Possible credential"), ("malformed_inventory", "valid artifact checksums"),
    ("inventory", "inventory"), ("csv", "CSV score differs"),
])
def test_import_refuses_corrupt_or_mismatched_export_before_writing(export, change, message):
    files, tmp_path = export
    files = dict(files)
    if change == "checksum":
        files["report.html"] += b"altered"
    elif change == "inventory":
        files["unexpected.txt"] = b"unexpected"
    elif change == "malformed_inventory":
        value = json.loads(files["manifest.json"])
        value["artifacts"] = ["summary.json"]
        files["manifest.json"] = encode(value)
    else:
        artifact = {
            "assessment": "audit/dataset.json", "deployment": "manifest.json",
            "scores": "original_assessment.json", "mean": "summary.json",
            "duplicate": "manifest.json", "incomplete": "audit/results.jsonl",
            "credential": "manifest.json", "run_secret": "manifest.json", "csv": "items.csv",
        }[change]
        if change == "incomplete":
            rows = [json.loads(line) for line in files[artifact].splitlines()]
            rows[0]["status"] = "error"
            files[artifact] = b"\n".join(encode(row) for row in rows)
        elif change == "csv":
            files[artifact] = files[artifact].replace(b"0,complete,4", b"0,complete,3")
        else:
            value = json.loads(files[artifact])
            if change == "assessment": value["assessment"]["id"] = "other"
            elif change == "deployment": value["deployment"] = "Different users."
            elif change == "scores": value["scoring"]["dimensions"]["input_form"]["score"] = 1
            elif change == "mean":
                value["dimensions"][0]["mean_score"] = 2
                value["classifiers"] = deepcopy(value["dimensions"])
            elif change == "duplicate": value["selected_item_ids"] = ["0", "0"]
            elif change == "credential": value["api_key"] = "private-test-value"
            elif change == "run_secret": value["run_secret"] = "private-browser-access-value"
            files[artifact] = encode(value)
        refresh_manifest(files)
    source = write_export(files, tmp_path / "bad-export")
    with pytest.raises(ValueError, match=message):
        import_snapshot(source, "gsm8k")
    assert not gallery_item_analysis.SNAPSHOT_ROOT.exists()


def test_original_zip_preserved_and_replacement_is_explicit(export):
    files, tmp_path = export
    source = tmp_path / "export.zip"
    with ZipFile(source, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr("download/" + name, content)
    import_snapshot(source, "gsm8k")
    target = gallery_item_analysis.SNAPSHOT_ROOT / "gsm8k"
    assert (target / "complete-results.zip").read_bytes() == source.read_bytes()
    with pytest.raises(ValueError, match="overwrite"):
        import_snapshot(source, "gsm8k")
    import_snapshot(source, "gsm8k", overwrite=True)
    assert gallery_item_analysis.get_artifact("gsm8k", "summary")[0] == files["summary.json"]
    # Updating the benchmark invalidates its old attachment instead of silently
    # comparing saved items with a different deployment/benchmark assessment.
    deployment = gallery._ASSESSMENTS_ROOT / "gsm8k/test-deployment/deployment_description.txt"
    deployment.write_text("New deployment")
    gallery.list_entries.cache_clear()
    assert gallery_item_analysis.get_snapshot("gsm8k") is None


def test_zip_and_filesystem_paths_cannot_escape(export):
    files, tmp_path = export
    source = tmp_path / "unsafe.zip"
    with ZipFile(source, "w") as archive:
        archive.writestr("../manifest.json", files["manifest.json"])
    with pytest.raises(ValueError, match="Unsafe ZIP"):
        import_snapshot(source, "gsm8k")
    source = write_export(files, tmp_path / "symlink-export")
    (source / "private").symlink_to(tmp_path)
    with pytest.raises(ValueError, match="symlink"):
        import_snapshot(source, "gsm8k")
    with pytest.raises(ValueError, match="Unknown gallery"):
        import_snapshot(source, "../outside")


def test_published_gsm8k_snapshot_matches_the_original_export():
    root = Path(__file__).resolve().parents[2] / "gallery_item_analyses/gsm8k"
    files = read_export(root / "complete-results.zip")
    snapshot, metadata, evaluated_csv = validate_export(files, "gsm8k")
    assert metadata["item_count"] == 100 and metadata["total_items"] == 1319
    assert snapshot == json.loads((root / "snapshot.json").read_text())
    assert evaluated_csv == (root / "evaluated-items.csv").read_bytes()
    assert [dimension["mean_score"] for dimension in snapshot["summary"]["dimensions"]] == [1.94, 1.42, 2.97, 1.84, 2.83, 2.57]
