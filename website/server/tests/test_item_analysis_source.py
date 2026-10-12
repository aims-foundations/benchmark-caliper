"""Pinned remote-source preparation, without network access or model requests."""

import json
from pathlib import Path
import re
from types import SimpleNamespace

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from anthropic_api_package_release.item_analysis.generate import generate_spec
from anthropic_api_package_release.item_analysis.data import read_items
from anthropic_api_package_release.item_analysis.prepare import REQUIRED_ASSESSMENT_FILES
from anthropic_api_package_release.item_analysis.storage import check_prepared
from website.server import db, item_analysis_source as source

TOKEN = "hf_test_only_server_credential"


@pytest.fixture
def remote(tmp_path, monkeypatch, request):
    definition = source.source_definition(getattr(request, "param", "mmlu"))
    rows = {
        "mmlu": [
            {"item_id": f"item-{i}", "benchmark_id": "mmlu", "content": f"Question {i}\nA. yes\nB. no",
             "reference_answer": "A", "item_features": "task=arithmetic"}
            for i in range(3)
        ],
        "toxigen": [
            {"item_id": "toxigen-classification", "benchmark_id": "toxigen",
             "content": json.dumps([{"role": "system", "content": "Classify the statement."},
                                    {"role": "user", "content": "A neutral example statement."}]),
             "grading_criterion": json.dumps({"reference_answer": "0", "response_scale": {"kind": "discrete", "values": [0, 1]}, "rule": "Classify the statement."}),
             "verifier": None, "item_features": "task=classification;split=test"},
            {"item_id": "toxigen-generation", "benchmark_id": "toxigen", "content": "Complete this neutral sentence.",
             "grading_criterion": json.dumps({"reference_answer": None, "response_scale": {"kind": "discrete", "values": [1, 2, 3, 4, 5]}, "rule": "Rate the continuation."}),
             "verifier": None, "item_features": "task=continuation_generation;split=train"},
        ],
        "gsm8k": [
            {"question": "How many apples are 2 plus 3 apples?", "answer": "2 + 3 = <<2+3=5>>5.\n#### 5"},
            {"question": "How many pears are 4 plus 2 pears?", "answer": "4 + 2 = <<4+2=6>>6.\n#### 6"},
        ],
        "humaneval": [
            {"task_id": "HumanEval/0", "prompt": "def double(x):\n    \"\"\"Return twice x.\"\"\"\n",
             "canonical_solution": "    return 2 * x\n", "test": "def check(candidate):\n    assert candidate(2) == 4\n",
             "entry_point": "double"},
            {"task_id": "HumanEval/1", "prompt": "def triple(x):\n    \"\"\"Return three times x.\"\"\"\n",
             "canonical_solution": "    return 3 * x\n", "test": "def check(candidate):\n    assert candidate(2) == 6\n",
             "entry_point": "triple"},
        ],
    }[definition["benchmark"]]
    # Retain the actual cache layout so shared preparation checks provenance.
    table = (tmp_path / f"datasets--{definition['repo'].replace('/', '--')}"
             / "snapshots" / definition["revision"] / definition["table_path"])
    table.parent.mkdir(parents=True)
    pq.write_table(pa.Table.from_pylist(rows), table)
    definition.update(item_count=len(rows), sha256=source.file_sha256(table))
    monkeypatch.setattr(source, "sources", lambda: [definition])
    monkeypatch.setattr(source, "get_token", lambda: TOKEN)
    monkeypatch.setattr(db, "DEFAULT_DB_PATH", tmp_path / "data/runs.db")
    calls = []

    def download(**kwargs):
        calls.append(kwargs)
        return str(table)

    monkeypatch.setattr(source, "hf_hub_download", download)
    return table, calls, definition


def test_catalog_uses_actual_snapshot_metadata_and_never_downloads(monkeypatch):
    monkeypatch.setattr(source, "get_token", lambda: TOKEN)
    monkeypatch.setattr(source, "hf_hub_download", lambda **kwargs: pytest.fail("Catalog must not download"))
    entry = source.source_entry()
    assert entry["id"] == "mmlu" and entry["item_count"] == 14015
    assert entry["available"] and entry["supplied_spec_available"]
    assert source.source_definition("mmlu")["revision"] in entry["source_url"]
    assert "measurement-db-pp" in entry["source_url"]
    assert TOKEN not in json.dumps(entry)


def test_download_is_pinned_and_prepared_inputs_are_real_and_key_free(tmp_path, remote):
    table, calls, definition = remote
    directory = tmp_path / "run"
    supplied = source.prepare_source(directory)
    assert calls == [{"repo_id": definition["repo"], "filename": definition["table_path"],
                      "repo_type": "dataset", "revision": definition["revision"], "token": TOKEN,
                      "cache_dir": tmp_path / "data/item-analysis-sources", "etag_timeout": 20}]
    dataset = check_prepared(directory)
    assert dataset["item_count"] == 3
    assert dataset["source"]["repo"] == "aims-foundations/measurement-db-pp"
    assert dataset["source"]["revision"] == definition["revision"]
    assert dataset["source"]["sha256"] == source.file_sha256(table)
    assert (tmp_path / "data/item-analysis-sources").stat().st_mode & 0o777 == 0o700
    assert supplied.read_bytes() == Path(source.__file__).with_name(definition["supplied_spec"]).read_bytes()
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
    _, _, definition = remote
    if mismatch == "checksum":
        definition["sha256"] = "0" * 64
    else:
        definition["item_count"] = 4
    with pytest.raises(source.DatasetPreparationError, match="failed validation"):
        source.prepare_source(tmp_path / "run")
    assert not (tmp_path / "run/items.jsonl").exists()


def test_cancelled_preparation_never_downloads(tmp_path, remote):
    _, calls, _ = remote
    with pytest.raises(InterruptedError):
        source.prepare_source(tmp_path / "run", stopped=lambda: True)
    assert not calls


def test_stop_after_download_leaves_cached_data_without_starting_preparation(tmp_path, remote):
    table, calls, _ = remote
    with pytest.raises(InterruptedError):
        source.prepare_source(tmp_path / "run", stopped=lambda: bool(calls))
    assert table.is_file() and not (tmp_path / "run").exists()


def test_registry_pins_match_complete_original_assessments():
    definitions = source.sources()
    assert {entry["id"] for entry in definitions} == {"mmlu", "toxigen", "toxigen-south-asia", "gsm8k", "humaneval"}
    assert len({entry["id"] for entry in definitions}) == len(definitions)
    for definition in definitions:
        assert re.fullmatch(r"[a-f0-9]{40}", definition["revision"])
        assert re.fullmatch(r"[a-f0-9]{64}", definition["sha256"])
        assert definition["item_count"] > 0
        assert definition["table_path"].endswith(".parquet")
        assert source.source_definition(definition["id"]) == definition
        assessment = source.ASSESSMENTS_DIR / definition["assessment_dir"]
        for filename in REQUIRED_ASSESSMENT_FILES:
            assert (assessment / filename).read_text(encoding="utf-8").strip()
        scoring = json.loads((assessment / "scoring.json").read_text())
        assert scoring["benchmark"] == definition["benchmark"]
        assert isinstance(scoring["dimensions"], dict) and scoring["dimensions"]
        if definition.get("supplied_spec"):
            spec = json.loads(Path(source.__file__).with_name(definition["supplied_spec"]).read_text())
            assert spec["benchmark"] == definition["benchmark"]
            assert spec["classifiers"]
            # The historical criteria belong only to this original assessment.
            assert definition["assessment_dir"] == "expert_1a429e941728__mmlu/india_hindi_competitive_exam_prep"
        else:
            assert definition["id"] != "mmlu"


def test_public_catalog_sources_are_available_without_hugging_face_credentials(monkeypatch):
    monkeypatch.setattr(source, "get_token", lambda: None)
    monkeypatch.setattr(source, "hf_hub_download", lambda **kwargs: pytest.fail("Catalog must not download"))
    entries = {entry["id"]: entry for entry in source.source_entries()}
    assert not entries["mmlu"]["available"]
    for identifier in ("toxigen", "toxigen-south-asia"):
        assert not entries[identifier]["available"]
        assert "HF_TOKEN" in entries[identifier]["unavailable_reason"]
    for identifier, count in (("gsm8k", 1319), ("humaneval", 164)):
        entry = entries[identifier]
        assert entry["available"] and entry["unavailable_reason"] is None
        assert not entry["supplied_spec_available"]
        assert entry["item_count"] == count
        assert entry["benchmark"] == identifier
        assert entry["deployment"] and entry["assessment_title"]
        assert "openai/" in entry["source_url"]


def test_toxigen_contexts_share_pinned_source_and_keep_distinct_assessments(monkeypatch):
    monkeypatch.setattr(source, "get_token", lambda: TOKEN)
    monkeypatch.setattr(source, "hf_hub_download", lambda **kwargs: pytest.fail("Catalog must not download"))
    clinical = source.source_entry("toxigen")
    academic = source.source_entry("toxigen-south-asia")
    assert clinical["benchmark"] == academic["benchmark"] == "toxigen"
    assert clinical["source_url"] == academic["source_url"]
    assert clinical["item_count"] == academic["item_count"] == 39011
    assert clinical["assessment_title"] != academic["assessment_title"]
    assert clinical["deployment"] != academic["deployment"]
    for entry in (clinical, academic):
        assert entry["available"] and not entry["supplied_spec_available"]
        assert "classification and continuation generation" in entry["description"]
        assert "toxigen/items.parquet" in entry["source_url"]


@pytest.mark.parametrize("remote", ["toxigen", "toxigen-south-asia"], indirect=True)
def test_toxigen_uses_selected_assessment_and_preserves_mixed_grading_rules(tmp_path, remote):
    table, calls, definition = remote
    directory = tmp_path / "run"
    supplied = source.prepare_source(directory, example_id=definition["id"])
    assert not supplied.exists()
    assert calls[0]["repo_id"] == "aims-foundations/measurement-db-pp"
    assert calls[0]["filename"] == "toxigen/items.parquet"
    assert calls[0]["revision"] == definition["revision"]
    assert calls[0]["token"] == TOKEN
    dataset = check_prepared(directory)
    assert dataset["benchmark"] == "toxigen" and dataset["item_count"] == 2
    assert dataset["source"]["sha256"] == source.file_sha256(table)
    assert "normalization" not in dataset["source"]
    evidence = json.loads((directory / "evidence.json").read_text())
    assessment = source.ASSESSMENTS_DIR / definition["assessment_dir"]
    assert evidence["deployment"] == (assessment / "deployment_description.txt").read_text()
    assert evidence["scoring"] == json.loads((assessment / "scoring.json").read_text())
    items = {item["item_id"]: item for item in read_items(directory / "items.jsonl")}
    assert items["toxigen-classification"]["content"] == [
        {"role": "system", "content": "Classify the statement."},
        {"role": "user", "content": "A neutral example statement."},
    ]
    assert items["toxigen-classification"]["reference_answer"] == "0"
    assert items["toxigen-generation"]["reference_answer"] is None
    assert items["toxigen-classification"]["grading_criterion"]["response_scale"]["values"] == [0, 1]
    assert items["toxigen-generation"]["grading_criterion"]["response_scale"]["values"] == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("remote", ["gsm8k", "humaneval"], indirect=True)
def test_public_source_prepares_matching_assessment_with_raw_and_normalized_provenance(tmp_path, monkeypatch, remote):
    table, calls, definition = remote
    monkeypatch.setattr(source, "get_token", lambda: pytest.fail("Public sources must not read the private token"))
    normalized = tmp_path / "expected-normalized.parquet"
    source.normalize_source(definition, table, normalized)
    directory = tmp_path / "run"
    supplied = source.prepare_source(directory, example_id=definition["id"])

    assert calls == [{
        "repo_id": definition["repo"], "filename": definition["table_path"],
        "repo_type": "dataset", "revision": definition["revision"], "token": False,
        "cache_dir": tmp_path / "data/item-analysis-sources", "etag_timeout": 20,
    }]
    assert not supplied.exists()
    assert not (directory / "provided_spec.json").exists()
    dataset = check_prepared(directory)
    assert dataset["benchmark"] == definition["benchmark"]
    assert dataset["item_count"] == definition["item_count"]
    assert dataset["source"] == {
        "repo": definition["repo"], "revision": definition["revision"],
        "table": definition["table_path"], "path": str(table),
        "sha256": source.file_sha256(table), "revision_origin": "provided",
        "normalization": f"{definition['adapter']}-v1",
        "normalized_sha256": source.file_sha256(normalized),
    }
    assert dataset["source"]["sha256"] != dataset["source"]["normalized_sha256"]
    evidence = json.loads((directory / "evidence.json").read_text())
    assessment = source.ASSESSMENTS_DIR / definition["assessment_dir"]
    assert evidence["assessment_dir"] == str(assessment.resolve())
    assert evidence["deployment"] == (assessment / "deployment_description.txt").read_text()
    assert evidence["benchmark"] == definition["benchmark"]
    originals = pq.read_table(table).to_pylist()
    items = sorted(read_items(directory / "items.jsonl"), key=lambda item: item["item_id"])
    for item, original in zip(items, originals):
        assert all(item["additional_fields"][key] == value for key, value in original.items())
        if definition["id"] == "gsm8k":
            assert item["reference_answer"] == original["answer"]
        else:
            assert item["reference_answer"] == original["canonical_solution"]
            assert item["verifier"] == {"test": original["test"], "entry_point": original["entry_point"]}
    assert not list((tmp_path / "data/item-analysis-sources").glob("normalize-*"))
    for path in directory.iterdir():
        assert TOKEN not in path.read_text()


@pytest.mark.parametrize("remote", ["gsm8k", "humaneval"], indirect=True)
def test_public_sources_reject_invalid_schema_before_creating_run(tmp_path, remote):
    table, _, definition = remote
    pq.write_table(pa.Table.from_pylist([{"wrong_column": "value"}]), table)
    definition.update(sha256=source.file_sha256(table), item_count=1)
    with pytest.raises(source.DatasetPreparationError, match="failed validation"):
        source.prepare_source(tmp_path / "run", example_id=definition["id"])
    assert not (tmp_path / "run").exists()


@pytest.mark.parametrize("identifier", ["unknown", "../../gsm8k", "https://huggingface.co/datasets/other/repo"])
def test_unknown_sources_are_rejected_without_downloading(tmp_path, monkeypatch, identifier):
    monkeypatch.setattr(source, "get_token", lambda: pytest.fail("Unknown source must not read credentials"))
    monkeypatch.setattr(source, "hf_hub_download", lambda **kwargs: pytest.fail("Unknown source must not download"))
    with pytest.raises(ValueError, match="not configured"):
        source.source_entry(identifier)
    with pytest.raises(ValueError, match="not configured"):
        source.prepare_source(tmp_path / "run", example_id=identifier)
    assert not (tmp_path / "run").exists()
