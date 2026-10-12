"""Preserve official benchmark evidence in the shared item-analysis schema.

These adapters only read dataset values. HumanEval test and solution code are
retained as text and are never imported or executed.
"""

import json
from pathlib import Path


REQUIRED_COLUMNS = {
    "gsm8k": ("question", "answer"),
    "humaneval": ("task_id", "prompt", "canonical_solution", "test", "entry_point"),
}


def normalize_source(source: dict, items: Path, output: Path) -> None:
    """Write a deterministic, lossless adaptation of an official test split.

    GSM8K has no source item ID, so IDs identify rows in its pinned test table.
    Original columns remain available alongside the normalized evidence fields.
    The caller records and validates the original snapshot's provenance.
    """
    import pyarrow as pa
    import pyarrow.parquet as pq

    adapter = source.get("adapter")
    if adapter not in REQUIRED_COLUMNS:
        raise ValueError("Unsupported item-analysis source adapter")
    benchmark = source.get("benchmark")
    if benchmark != adapter:
        raise ValueError("Source benchmark does not match its adapter")

    table = pq.read_table(items)
    required = REQUIRED_COLUMNS[adapter]
    if not set(required).issubset(table.column_names):
        raise ValueError(f"The {benchmark} source is missing required columns")
    if not table.num_rows:
        raise ValueError(f"The {benchmark} source contains no items")

    normalized = []
    seen_ids = set()
    for index, row in enumerate(table.to_pylist()):
        if any(not isinstance(row[name], str) or not row[name].strip() for name in required):
            raise ValueError(f"The {benchmark} source has invalid evidence at row {index + 1}")
        if adapter == "gsm8k":
            item = {
                **row,
                "item_id": f"{benchmark}/test/{index}",
                "benchmark_id": benchmark,
                "content": row["question"],
                "reference_answer": row["answer"],
                "item_features": json.dumps({"split": "test", "config": "main"}),
            }
        else:
            item = {
                **row,
                "item_id": row["task_id"],
                "benchmark_id": benchmark,
                "content": row["prompt"],
                "reference_answer": row["canonical_solution"],
                "verifier": json.dumps({"test": row["test"], "entry_point": row["entry_point"]}),
                "item_features": json.dumps({"split": "test", "language": "python"}),
            }
        if item["item_id"] in seen_ids:
            raise ValueError(f"The {benchmark} source has duplicate item IDs")
        seen_ids.add(item["item_id"])
        normalized.append(item)

    pq.write_table(pa.Table.from_pylist(normalized), output)
