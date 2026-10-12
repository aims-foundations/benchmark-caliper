"""Official benchmark adapters preserve evidence without executing source code."""

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from anthropic_api_package_release.item_analysis.data import prepare_data, read_items
from website.server.item_analysis_adapters import normalize_source


ROWS = {
    "gsm8k": {
        "question": "How much do three $2 apples cost?",
        "answer": "Three apples cost 3 * 2 = <<3*2=6>>6 dollars.\n#### 6",
    },
    "humaneval": {
        "task_id": "HumanEval/0",
        "prompt": "def double(x):\n    \"\"\"Return twice x.\"\"\"\n",
        "canonical_solution": "    return 2 * x\n",
        "test": "raise RuntimeError('Source code must never execute')\n",
        "entry_point": "double",
    },
}


def adapt(tmp_path, benchmark, rows):
    source, output = tmp_path / "source.parquet", tmp_path / "normalized.parquet"
    pq.write_table(pa.Table.from_pylist(rows), source)
    normalize_source({"adapter": benchmark, "benchmark": benchmark}, source, output)
    return output


@pytest.mark.parametrize("benchmark", ["gsm8k", "humaneval"])
def test_preserves_original_evidence_through_shared_preparation(tmp_path, benchmark):
    original = {**ROWS[benchmark], "source_note": "Additional source metadata stays intact."}
    output = adapt(tmp_path, benchmark, [original])
    normalized = pq.read_table(output).to_pylist()[0]
    assert all(normalized[name] == value for name, value in original.items())
    assert normalized["benchmark_id"] == benchmark

    directory = tmp_path / "prepared"
    prepare_data(output, directory, benchmark=benchmark)
    item = next(read_items(directory / "items.jsonl"))
    assert item["additional_fields"]["source_note"] == original["source_note"]
    if benchmark == "gsm8k":
        assert item["item_id"] == "gsm8k/test/0"
        assert item["content"] == original["question"]
        assert item["reference_answer"] == original["answer"]
        assert item["item_features"] == {"split": "test", "config": "main"}
    else:
        assert item["item_id"] == original["task_id"]
        assert item["content"] == original["prompt"]
        assert item["reference_answer"] == original["canonical_solution"]
        assert item["verifier"] == {"test": original["test"], "entry_point": original["entry_point"]}
        assert item["item_features"] == {"split": "test", "language": "python"}


def test_gsm8k_ids_are_stable_and_preserve_duplicate_questions(tmp_path):
    output = adapt(tmp_path, "gsm8k", [ROWS["gsm8k"], ROWS["gsm8k"]])
    first = pq.read_table(output).to_pylist()
    assert [row["item_id"] for row in first] == ["gsm8k/test/0", "gsm8k/test/1"]
    normalize_source({"adapter": "gsm8k", "benchmark": "gsm8k"}, tmp_path / "source.parquet", output)
    assert pq.read_table(output).to_pylist() == first


@pytest.mark.parametrize("benchmark", ["gsm8k", "humaneval"])
def test_missing_columns_are_rejected_without_output(tmp_path, benchmark):
    with pytest.raises(ValueError, match="missing required columns"):
        adapt(tmp_path, benchmark, [{"unrelated": "value"}])
    assert not (tmp_path / "normalized.parquet").exists()


@pytest.mark.parametrize("benchmark,field", [
    (benchmark, field) for benchmark, row in ROWS.items() for field in row
])
@pytest.mark.parametrize("value", [None, "", "  ", 5])
def test_missing_or_invalid_evidence_is_rejected(tmp_path, benchmark, field, value):
    with pytest.raises(ValueError, match="invalid evidence"):
        adapt(tmp_path, benchmark, [{**ROWS[benchmark], field: value}])
    assert not (tmp_path / "normalized.parquet").exists()


@pytest.mark.parametrize("benchmark", ["gsm8k", "humaneval"])
def test_empty_source_is_rejected(tmp_path, benchmark):
    source, output = tmp_path / "source.parquet", tmp_path / "normalized.parquet"
    pq.write_table(pa.table({name: pa.array([], type=pa.string()) for name in ROWS[benchmark]}), source)
    with pytest.raises(ValueError, match="contains no items"):
        normalize_source({"adapter": benchmark, "benchmark": benchmark}, source, output)
    assert not output.exists()


def test_duplicate_humaneval_ids_are_rejected(tmp_path):
    with pytest.raises(ValueError, match="duplicate item IDs"):
        adapt(tmp_path, "humaneval", [ROWS["humaneval"], ROWS["humaneval"]])
    assert not (tmp_path / "normalized.parquet").exists()


@pytest.mark.parametrize("source", [
    {"adapter": "unsupported", "benchmark": "gsm8k"},
    {"adapter": "gsm8k", "benchmark": "humaneval"},
])
def test_unknown_or_mismatched_adapter_is_rejected(tmp_path, source):
    with pytest.raises(ValueError):
        normalize_source(source, tmp_path / "source.parquet", tmp_path / "normalized.parquet")
