"""Preparation preserves the full population and auditable item evidence."""

import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from item_analysis.data import file_sha256, prepare_data, read_items


def write_table(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), path)
    return path


def test_full_population_seeded_prefix_and_complete_category_counts(tmp_path):
    source = write_table(tmp_path / "items.parquet", [
        {"item_id": f"item-{number}", "content": "Same content\nA. yes\nB. no",
         "reference_answer": "A", "item_features": f"task=category-{number}"}
        for number in range(150)
    ])
    before = file_sha256(source)
    manifests = [prepare_data(source, tmp_path / name, benchmark="fixture", seed=seed)
                 for name, seed in [("one", 17), ("two", 17), ("three", 18)]]
    first = list(read_items(tmp_path / "one/items.jsonl"))
    second = list(read_items(tmp_path / "two/items.jsonl"))
    third = list(read_items(tmp_path / "three/items.jsonl"))
    assert first == second
    assert first != third
    assert len(first) == 150  # Identical content with distinct IDs is not deduplicated.
    assert {item["item_id"] for item in first} == {f"item-{n}" for n in range(150)}
    assert {item["source"]["row"] for item in first[:100]} != set(range(1, 101))
    assert all(item["source"]["row"] == int(item["item_id"].split("-")[1]) + 1 for item in first)
    assert file_sha256(source) == before
    assert manifests[0]["items_sha256"] == manifests[1]["items_sha256"]
    profile = json.loads((tmp_path / "one/profile.json").read_text())
    assert len(profile["item_feature_value_counts"]["task"]) == 150
    assert sum(entry["count"] for entry in profile["item_feature_value_counts"]["task"]) == 150
    assert profile["is_mcq"] is True
    assert profile["output_format"]["items_with_choice_lines"] == 150


def test_preserves_long_evidence_and_reference_types_without_executing_verifier(tmp_path):
    long_text = "Evidence stays intact. " * 2000
    source = write_table(tmp_path / "items.parquet", [
        {"item_id": "zero", "content": json.dumps({"question": long_text, "choices": ["a", "b"]}),
         "reference_answer": "0", "grading_criterion": json.dumps({"reference_answer": "other", "rubric": long_text}),
         "verifier": json.dumps({"code": "raise RuntimeError('must not execute')"}),
         "item_features": json.dumps({"subject": "science", "question": long_text}),
         "asset_manifest": json.dumps([{"type": "image", "path": "missing.png"}])},
        {"item_id": "nested", "content": "Question", "reference_answer": None,
         "grading_criterion": json.dumps({"reference_answer": ["first", "second"]}),
         "verifier": None, "item_features": None, "asset_manifest": None},
        {"item_id": "missing", "content": "Question", "reference_answer": None,
         "grading_criterion": "Use expert judgment", "verifier": None,
         "item_features": None, "asset_manifest": None},
    ])
    prepare_data(source, tmp_path / "run", benchmark="fixture")
    items = {item["item_id"]: item for item in read_items(tmp_path / "run/items.jsonl")}
    assert items["zero"]["content"]["question"] == long_text
    assert items["zero"]["reference_answer"] == 0
    assert items["zero"]["grading_criterion"]["rubric"] == long_text
    assert items["zero"]["asset_manifest"][0]["path"] == "missing.png"
    assert items["nested"]["reference_answer"] == ["first", "second"]
    assert items["missing"]["reference_answer"] is None
    profile = json.loads((tmp_path / "run/profile.json").read_text())
    assert "question" not in profile["item_feature_value_counts"]
    assert profile["has_media"] is True
    assert profile["media_assets_loaded"] is False
    assert profile["modality"]["items_with_media_markers"]["image"] == 1
    assert profile["is_mcq"] is False  # Other rows have no choice evidence.


def test_legacy_choices_and_explicit_answer_are_preserved(tmp_path):
    source = write_table(tmp_path / "items.parquet", [
        {"item_id": "first", "question": "Which?", "choices": ["one", "two"],
         "answer": 0, "subject": "example", "content_hash": "5e432382"},
        {"item_id": "second", "question": "Which again?", "choices": ["one", "two"],
         "answer": None, "subject": "example"},
    ])
    prepare_data(source, tmp_path / "run", benchmark="fixture")
    items = {item["item_id"]: item for item in read_items(tmp_path / "run/items.jsonl")}
    assert items["first"]["content"]["choices"] == ["one", "two"]
    assert items["first"]["reference_answer"] == 0  # No guessed conversion to choice text.
    assert items["second"]["reference_answer"] is None
    assert items["first"]["additional_fields"]["subject"] == "example"
    assert items["first"]["additional_fields"]["content_hash"] == "5e432382"
    assert json.loads((tmp_path / "run/profile.json").read_text())["is_mcq"] is True


def test_letters_alone_do_not_establish_mcq_and_unused_media_columns_do_not_establish_media(tmp_path):
    source = write_table(tmp_path / "items.parquet", [
        {"item_id": "one", "content": "Give a letter.", "reference_answer": "A", "image": None},
    ])
    prepare_data(source, tmp_path / "run", benchmark="fixture")
    profile = json.loads((tmp_path / "run/profile.json").read_text())
    assert profile["is_mcq"] is False
    assert profile["output_format"]["status"] == "not_established"
    assert profile["has_media"] is False
    assert profile["media_fields"] == []


@pytest.mark.parametrize("rows, message", [
    ([{"item_id": "same", "content": "a"}, {"item_id": "same", "content": "b"}], "Duplicate item_id"),
    ([{"item_id": None, "content": "a"}], "item_id"),
    ([{"item_id": " ", "content": "a"}], "item_id"),
    ([{"item_id": "one", "content": "  "}], "Missing content"),
    ([{"item_id": "one", "question": None, "choices": ["a", "b"]}], "Missing content"),
])
def test_invalid_population_fails_before_writing(tmp_path, rows, message):
    source = write_table(tmp_path / "items.parquet", rows)
    with pytest.raises(ValueError, match=message):
        prepare_data(source, tmp_path / "run", benchmark="fixture")
    assert not (tmp_path / "run/items.jsonl").exists()


def test_cache_provenance_and_existing_artifacts_are_protected(tmp_path):
    revision = "a" * 40
    source = write_table(tmp_path / "snapshots" / revision / "mmlu/items.parquet", [
        {"item_id": "one", "content": "Question"},
    ])
    manifest = prepare_data(source, tmp_path / "run", benchmark="mmlu")
    assert manifest["source"]["revision"] == revision
    assert manifest["source"]["table"] == "mmlu/items.parquet"
    assert manifest["source"]["revision_origin"] == "cache_path"
    assert manifest["source"]["sha256"] == file_sha256(source)
    assert manifest["items_sha256"] == file_sha256(tmp_path / "run/items.jsonl")
    assert manifest["profile_sha256"] == file_sha256(tmp_path / "run/profile.json")
    saved = (tmp_path / "run/dataset.json").read_bytes()
    with pytest.raises(FileExistsError):
        prepare_data(source, tmp_path / "run", benchmark="mmlu", seed=999)
    assert (tmp_path / "run/dataset.json").read_bytes() == saved


def test_named_benchmark_mismatch_cannot_silently_relabel_dataset(tmp_path):
    source = write_table(tmp_path / "items.parquet", [
        {"item_id": "one", "benchmark_id": "afrimedqa", "content": "Question"},
    ])
    with pytest.raises(ValueError, match="do not match requested benchmark"):
        prepare_data(source, tmp_path / "run", benchmark="mmlu")
    assert not (tmp_path / "run/items.jsonl").exists()
    prepare_data(source, tmp_path / "matching", benchmark="afrimedqa")
    profile = json.loads((tmp_path / "matching/profile.json").read_text())
    assert profile["benchmark_identity"]["status"] == "matched"
    assert profile["benchmark_identity"]["observed_ids"] == ["afrimedqa"]


def test_opaque_benchmark_ids_are_retained_as_unverified_identity(tmp_path):
    source = write_table(tmp_path / "items.parquet", [
        {"item_id": "one", "benchmark_id": "83d93a48fa4b4ba2", "content": "Question"},
    ])
    prepare_data(source, tmp_path / "run", benchmark="mmlu")
    profile = json.loads((tmp_path / "run/profile.json").read_text())
    assert profile["benchmark_identity"]["status"] == "unverified_opaque_ids"
    assert profile["benchmark_identity"]["observed_ids"] == ["83d93a48fa4b4ba2"]


@pytest.mark.parametrize("claim", [
    {"source_revision": "b" * 40},
    {"source_table": "afrimedqa/items.parquet"},
])
def test_explicit_provenance_cannot_contradict_cache_path(tmp_path, claim):
    revision = "a" * 40
    source = write_table(tmp_path / "snapshots" / revision / "mmlu/items.parquet", [
        {"item_id": "one", "benchmark_id": "mmlu", "content": "Question"},
    ])
    with pytest.raises(ValueError, match="contradicts the local cache snapshot path"):
        prepare_data(source, tmp_path / "run", benchmark="mmlu", **claim)
    assert not (tmp_path / "run/items.jsonl").exists()
