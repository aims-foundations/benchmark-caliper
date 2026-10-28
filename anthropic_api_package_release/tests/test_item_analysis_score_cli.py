"""The default CLI path assembles context locally and scores one item per request."""

import json

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from item_analysis import __main__ as cli, scoring
from item_analysis.prepare import prepare
from item_analysis.storage import read_json


@pytest.fixture
def inputs(tmp_path):
    assessment = tmp_path / "assessment"
    assessment.mkdir()
    (assessment / "scoring.json").write_text(json.dumps({"benchmark": "arithmetic", "dimensions": {}}))
    for filename in ("deployment_description.txt", "elicitation_summary.md", "dataset_analysis_report.md"):
        (assessment / filename).write_text("English arithmetic tutoring with worked explanations.")
    items = tmp_path / "items.parquet"
    pq.write_table(pa.Table.from_pylist([
        {"item_id": "a", "content": "What is 2 + 2?", "reference_answer": "4"},
        {"item_id": "b", "content": "What is 3 + 3?", "reference_answer": "6"},
    ]), items)
    return assessment, items, tmp_path / "run"


def test_prepare_cli_automatically_freezes_six_score_context_without_key(inputs, monkeypatch, capsys):
    assessment, items, directory = inputs
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(cli, "_api", lambda *_: pytest.fail("Preparation cannot need a provider client"))
    assert cli.main(["prepare", "--assessment-dir", str(assessment), "--items", str(items), "--output-dir", str(directory)]) == 0
    assert read_json(directory / "classifier_spec.json")["analysis_type"] == "six_scores"
    assert cli.main(["classify", "--run-dir", str(directory), "--dry-run", "--all"]) == 0
    requests = [json.loads(line) for line in (directory / "preview_requests.jsonl").read_text().splitlines()]
    assert len(requests) == 2
    assert all(set(json.loads(entry["request"]["user"])["output_schema"]["properties"]["dimensions"]["properties"]) == set(scoring.DIMENSIONS) for entry in requests)


def test_prepare_context_preview_does_not_write_then_creates_context(inputs, monkeypatch, capsys):
    assessment, items, directory = inputs
    prepare(assessment, items, directory)
    monkeypatch.setattr(cli, "_api", lambda *_: pytest.fail("Context preparation cannot call a model"))
    assert cli.main(["prepare-context", "--run-dir", str(directory), "--dry-run"]) == 0
    assert not (directory / "classifier_spec.json").exists()
    assert json.loads(capsys.readouterr().out)["analysis_type"] == "six_scores"
    assert cli.main(["prepare-context", "--run-dir", str(directory)]) == 0
    assert read_json(directory / "classifier_spec.json")["rubric_version"] == scoring.RUBRIC_VERSION


def test_classify_prepared_inputs_builds_context_and_resume_makes_no_duplicate_calls(inputs, monkeypatch, capsys):
    assessment, items, directory = inputs
    prepare(assessment, items, directory)
    calls = []

    def judge(**request):
        calls.append(request)
        return json.dumps({"dimensions": {dimension: {
            "score": 4, "justification": "Supported by the supplied item and deployment.",
            "evidence": ["item.content: arithmetic question"], "information_gaps": [],
        } for dimension in scoring.DIMENSIONS}})

    monkeypatch.setattr(cli, "_api", lambda *_: judge)
    assert cli.main(["classify", "--run-dir", str(directory), "--limit", "1"]) == 0
    assert len(calls) == 1
    assert cli.main(["classify", "--run-dir", str(directory), "--all", "--resume"]) == 0
    assert len(calls) == 2
    assert read_json(directory / "summary.json")["complete_snapshot"]
    assert (directory / "report.html").is_file()
