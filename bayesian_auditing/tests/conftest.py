"""Small local Parquet tables matching both Hugging Face branch layouts."""

import json
from pathlib import Path
from types import SimpleNamespace

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from bayesian_auditing import data


@pytest.fixture
def corpus(tmp_path, monkeypatch):
    branches = {"main": "a" * 40, data.BRANCHES[1]: "b" * 40}
    first = {
        "item_id": "one", "benchmark_id": "math", "content": "Compute 1 + 1.",
        "grading_criterion": json.dumps({"reference_answer": "2", "rule": "exact match"}),
        "verifier": "exact_match", "item_features": "language=en", "asset_manifest": None,
    }
    rows = {
        "main": [first, {**first, "item_id": "two", "content": "Explain your reasoning.", "grading_criterion": None}],
        data.BRANCHES[1]: [
            {**first, "item_id": "copy"},
            {**first, "item_id": "different_grade", "grading_criterion": json.dumps({"reference_answer": "3", "rule": "exact match"})},
        ],
    }
    trees = {}
    for branch, commit in branches.items():
        root = tmp_path / commit
        parent = "math" if branch == "main" else "math/formatted_tables"
        (root / parent).mkdir(parents=True)
        pq.write_table(pa.Table.from_pylist(rows[branch]), root / parent / "items.parquet")
        pq.write_table(pa.Table.from_pylist([{
            "benchmark_id": "math", "name": "Mathematics", "modality": ["text"],
            "description": "Simple arithmetic", "coverage": 0.95,
        }]), root / parent / "benchmarks.parquet")
        (root / "math/metadata.yaml").write_text("benchmark:\n  description: Simple arithmetic\nbuild:\n  command: ignored\n")
        directory = lambda path: SimpleNamespace(path=path)
        file = lambda path: SimpleNamespace(path=path, size=100)
        trees[commit, None] = [directory("math"), file("README.md")]
        tables = [file(parent + "/items.parquet"), file(parent + "/benchmarks.parquet")]
        trees[commit, "math"] = [directory("math/raw"), file("math/metadata.yaml")]
        if parent == "math":
            trees[commit, "math"] += tables
        else:
            trees[commit, "math"].append(directory(parent))
            trees[commit, parent] = tables

    class FakeApi:
        def list_repo_refs(self, *args, **kwargs):
            return SimpleNamespace(branches=[SimpleNamespace(name=b, target_commit=c) for b, c in branches.items()])

        def list_repo_tree(self, repo, *, repo_type, revision, path_in_repo=None):
            assert "raw" not in (path_in_repo or "")
            return trees[revision, path_in_repo]

    def download(repo, filename, *, repo_type, revision):
        assert repo == data.REPO
        return str(tmp_path / revision / filename)

    monkeypatch.setattr(data, "hf_hub_download", download)
    return data.discover_inventory(api=FakeApi()), FakeApi(), tmp_path


@pytest.fixture
def assessment_dict():
    from bayesian_auditing.scoring import DIMENSIONS

    return {name: {
        "score": score, "justification": "This dimension aligns with the described setting.",
        "confidence": "high", "confidence_rationale": "The supplied text directly establishes this match.",
        "evidence": ["item.content and deployment: text mathematics"], "information_gaps": [],
    } for name, score in zip(DIMENSIONS, [5, 4, 5, 4, 4, 3])}
