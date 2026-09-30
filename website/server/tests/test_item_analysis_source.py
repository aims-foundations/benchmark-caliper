"""Pinned remote-source preparation, without network access or model requests."""

import json
from pathlib import Path
from types import SimpleNamespace

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from anthropic_api_package_release.item_analysis.generate import generate_spec
from anthropic_api_package_release.item_analysis.storage import check_prepared
from website.server import db, item_analysis_source as source

TOKEN = "hf_test_only_server_credential"


@pytest.fixture
def remote(tmp_path, monkeypatch):
    # Use the real new-repository cache layout to exercise provenance checks.
    table = (tmp_path / "datasets--aims-foundations--measurement-db-pp"
             / "snapshots" / source.REVISION / "mmlu/items.parquet")
    table.parent.mkdir(parents=True)
    pq.write_table(pa.Table.from_pylist([
        {"item_id": f"item-{i}", "benchmark_id": "mmlu", "content": f"Question {i}\nA. yes\nB. no",
         "reference_answer": "A", "item_features": "task=arithmetic"}
        for i in range(3)
    ]), table)
    monkeypatch.setattr(source, "ITEM_COUNT", 3)
    monkeypatch.setattr(source, "TABLE_SHA256", source.file_sha256(table))
    monkeypatch.setattr(source, "get_token", lambda: TOKEN)
    monkeypatch.setattr(db, "DEFAULT_DB_PATH", tmp_path / "data/runs.db")
    calls = []

    def download(**kwargs):
        calls.append(kwargs)
        return str(table)

    monkeypatch.setattr(source, "hf_hub_download", download)
    return table, calls


def test_catalog_uses_actual_snapshot_metadata_and_never_downloads(monkeypatch):
    monkeypatch.setattr(source, "get_token", lambda: TOKEN)
    monkeypatch.setattr(source, "hf_hub_download", lambda **kwargs: pytest.fail("Catalog must not download"))
    entry = source.source_entry()
    assert entry["id"] == "mmlu" and entry["item_count"] == 14015
    assert entry["available"] and entry["supplied_spec_available"]
    assert source.REVISION in entry["source_url"]
    assert "measurement-db-pp" in entry["source_url"]
    assert TOKEN not in json.dumps(entry)


def test_download_is_pinned_and_prepared_inputs_are_real_and_key_free(tmp_path, remote):
    table, calls = remote
    directory = tmp_path / "run"
    supplied = source.prepare_source(directory)
    assert calls == [{"repo_id": source.REPO_ID, "filename": source.TABLE_PATH,
                      "repo_type": "dataset", "revision": source.REVISION, "token": TOKEN,
                      "cache_dir": tmp_path / "data/item-analysis-sources", "etag_timeout": 20}]
    dataset = check_prepared(directory)
    assert dataset["item_count"] == 3
    assert dataset["source"]["repo"] == "aims-foundations/measurement-db-pp"
    assert dataset["source"]["revision"] == source.REVISION
    assert dataset["source"]["sha256"] == source.file_sha256(table)
    assert (tmp_path / "data/item-analysis-sources").stat().st_mode & 0o777 == 0o700
    assert supplied.read_bytes() == source.SPEC_PATH.read_bytes()
    spec = generate_spec(directory, supplied=supplied)
    assert sum(slot["applicable"] for slot in spec["classifiers"]) == 4
    for path in directory.iterdir():
        if path.is_file():
            assert TOKEN not in path.read_text()


def test_missing_access_is_actionable_and_never_downloads(tmp_path, monkeypatch):
    monkeypatch.setattr(source, "get_token", lambda: None)
    monkeypatch.setattr(source, "hf_hub_download", lambda **kwargs: pytest.fail("Missing credential"))
    entry = source.source_entry()
    assert not entry["available"] and "HF_TOKEN" in entry["unavailable_reason"]
    with pytest.raises(source.DatasetAccessError, match="server-side Hugging Face access"):
        source.prepare_source(tmp_path / "run")


@pytest.mark.parametrize("status", [401, 403, 404, 500, None])
def test_provider_failures_are_sanitized(tmp_path, monkeypatch, remote, status):
    class ProviderError(RuntimeError):
        response = SimpleNamespace(status_code=status)

    def fail(**kwargs):
        raise ProviderError(f"Sensitive provider body {TOKEN}")

    monkeypatch.setattr(source, "hf_hub_download", fail)
    expected = source.DatasetAccessError if status in {401, 403, 404} else source.DatasetPreparationError
    with pytest.raises(expected) as error:
        source.prepare_source(tmp_path / "run")
    assert TOKEN not in str(error.value) and "Sensitive" not in str(error.value)
    assert not (tmp_path / "run/items.jsonl").exists()


@pytest.mark.parametrize("mismatch", ["checksum", "rows"])
def test_changed_snapshot_is_rejected_before_preparation(tmp_path, monkeypatch, remote, mismatch):
    if mismatch == "checksum":
        monkeypatch.setattr(source, "TABLE_SHA256", "0" * 64)
    else:
        monkeypatch.setattr(source, "ITEM_COUNT", 4)
    with pytest.raises(source.DatasetPreparationError, match="failed validation"):
        source.prepare_source(tmp_path / "run")
    assert not (tmp_path / "run/items.jsonl").exists()


def test_cancelled_preparation_never_downloads(tmp_path, remote):
    _, calls = remote
    with pytest.raises(InterruptedError):
        source.prepare_source(tmp_path / "run", stopped=lambda: True)
    assert not calls


def test_stop_after_download_leaves_cached_data_without_starting_preparation(tmp_path, remote):
    table, calls = remote
    with pytest.raises(InterruptedError):
        source.prepare_source(tmp_path / "run", stopped=lambda: bool(calls))
    assert table.is_file() and not (tmp_path / "run").exists()
