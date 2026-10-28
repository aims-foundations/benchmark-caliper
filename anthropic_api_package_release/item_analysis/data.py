"""Prepare a reproducible population from a local measurement-db Parquet snapshot.

No retrieval, verifier execution, deduplication, or evidence truncation occurs here.
The saved order is a seeded shuffle: a pilot is a prefix of the full population.
"""

from __future__ import annotations

import base64
from array import array
from collections import Counter, defaultdict
from datetime import date, datetime
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import random
import re
from tempfile import TemporaryFile
from typing import Iterable, Iterator

PREPARATION_BATCH_ROWS = 1024

EVIDENCE_FIELDS = (
    "content", "reference_answer", "grading_criterion", "verifier",
    "item_features", "asset_manifest",
)
TEXT_FEATURES = {
    "question", "prompt", "content", "text", "passage", "answer",
    "reference_answer", "rationale", "explanation", "solution",
}
MEDIA_KEYS = {
    "image": {"image", "images", "image_url", "image_path", "image_file"},
    "audio": {"audio", "audio_url", "audio_path", "audio_file"},
    "video": {"video", "video_url", "video_path", "video_file"},
}


def file_sha256(path: Path) -> str:
    """Hash the file's bytes, including when the input is a cache symlink."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_items(path: Path) -> Iterator[dict]:
    with Path(path).open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                raise ValueError(f"Empty item line {line_number} in {path}")
            yield json.loads(line)


def _decode(value):
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
            # Python accepts NaN/Infinity although JSON does not. Leave those
            # strings as evidence instead of manufacturing non-JSON numbers.
            if not any(isinstance(entry, float) and not math.isfinite(entry)
                       for entry in _walk(decoded)):
                return decoded
        except json.JSONDecodeError:
            pass
    return value


def _present(value) -> bool:
    return value is not None and value != "" and value != [] and value != {} and (
        not isinstance(value, str) or bool(value.strip())
    )


def _json_default(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, bytes):
        return {"encoding": "base64", "data": base64.b64encode(value).decode("ascii")}
    raise TypeError(f"Cannot preserve Parquet value of type {type(value).__name__}")


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False,
                      default=_json_default)


def _normalize(row: dict, row_number: int) -> dict:
    original_id = row.get("item_id")
    if not _present(original_id) or isinstance(original_id, (dict, list, bool)):
        raise ValueError(f"Missing or invalid item_id at source row {row_number}")
    item = {field: _decode(row.get(field)) for field in EVIDENCE_FIELDS}
    if not _present(item["content"]) and _present(row.get("question")):
        item["content"] = {"question": _decode(row["question"])}
    choices = _decode(row.get("choices", row.get("options")))
    if _present(choices):
        item["content"] = {"prompt": item["content"], "choices": choices}
    if not _present(item["content"]) or (
        isinstance(item["content"], dict) and "prompt" in item["content"]
        and not _present(item["content"]["prompt"])
    ):
        raise ValueError(f"Missing content at source row {row_number}")
    if item["reference_answer"] is None:
        if row.get("answer") is not None:
            item["reference_answer"] = _decode(row["answer"])
        elif isinstance(item["grading_criterion"], dict):
            item["reference_answer"] = item["grading_criterion"].get("reference_answer")
    item["item_id"] = str(original_id)
    item["source"] = {"row": row_number, "item_id": original_id}
    additional = {key: value for key, value in row.items()
                  if key not in EVIDENCE_FIELDS and key != "item_id"}
    if additional:
        item["additional_fields"] = additional
    return item


def _feature_map(value) -> dict:
    if isinstance(value, dict):
        return value
    # Historical measurement-db tables use e.g. task=hendrycksTest-anatomy.
    if isinstance(value, str) and "=" in value:
        pairs = [part.strip().split("=", 1) for part in value.split(";")]
        if all(len(pair) == 2 and pair[0] for pair in pairs):
            return dict(pairs)
    return {}


def _walk(value):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _choice_evidence(content) -> tuple[bool, bool]:
    explicit = False
    choice_lines = False
    for value in _walk(content):
        if isinstance(value, dict):
            for name in ("choices", "options", "answer_choices"):
                choices = value.get(name)
                if isinstance(choices, (dict, list)) and len(choices) >= 2:
                    explicit = True
        elif isinstance(value, str):
            labels = re.findall(r"^\s*([A-Z])[.)]\s+\S", value, re.MULTILINE)
            if "A" in labels and "B" in labels:
                choice_lines = True
    return explicit, choice_lines


def _benchmark_identity(observed: set[str], benchmark: str) -> dict:
    """Check named benchmark IDs without treating opaque hashes as names.

    The supported MMLU snapshot identifies every row with the name ``mmlu``.
    Other tables may use hashes, UUIDs, or numeric IDs. Those need an external
    ID-to-name mapping and are explicitly recorded as unverified here.
    """
    values = sorted(observed)
    opaque = re.compile(r"(?:[a-fA-F0-9]{16,64}|[a-fA-F0-9]{8}(?:-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}|[0-9]+)")
    mismatched = [value for value in values
                  if value != benchmark and not opaque.fullmatch(value)]
    if mismatched:
        raise ValueError(
            f"Source benchmark_id values {mismatched!r} do not match requested benchmark {benchmark!r}; "
            "named benchmark IDs must match exactly"
        )
    status = "matched" if values == [benchmark] else "unverified_opaque_ids" if values else "not_available"
    return {
        "requested": benchmark, "observed_ids": values, "status": status,
        "note": "Named IDs are checked exactly. Missing or opaque IDs do not establish benchmark identity; verify source provenance.",
    }


def _profile(items: Iterable[dict], schema) -> dict:
    """Count every item incrementally; retain all observed scalar categories."""
    counts = defaultdict(Counter)
    skipped = set()
    media_counts = Counter()
    media_fields = set()
    available = Counter()
    explicit_count = line_count = mcq_count = assets_count = row_count = 0
    for item in items:
        row_count += 1
        for name in EVIDENCE_FIELDS:
            if _present(item[name]):
                available[name] += 1
        for name, value in _feature_map(item["item_features"]).items():
            if name.lower() in TEXT_FEATURES or name.lower().endswith("_text"):
                skipped.add(name)
                continue
            values = value if isinstance(value, list) else [value]
            if any(isinstance(entry, (dict, list)) for entry in values):
                skipped.add(name)
                continue
            # A list-valued feature counts presence once per item per category.
            counts[name].update({_json(entry) for entry in values if entry is not None})
        explicit, lines = _choice_evidence(item["content"])
        explicit_count += explicit
        line_count += lines
        mcq_count += explicit or lines
        assets_count += _present(item["asset_manifest"])
        item_media = set()
        for value in _walk([item, _feature_map(item["item_features"])]):
            if not isinstance(value, dict):
                continue
            for name, entry in value.items():
                if not _present(entry):
                    continue
                for kind, keys in MEDIA_KEYS.items():
                    if name.lower() in keys:
                        item_media.add(kind)
                        media_fields.add(name)
                if name.lower() in {"type", "modality", "mime_type", "mimetype"} and isinstance(entry, str):
                    for kind in MEDIA_KEYS:
                        if entry.lower() == kind or entry.lower().startswith(kind + "/"):
                            item_media.add(kind)
                            media_fields.add(name)
        media_counts.update(item_media)
    all_mcq = bool(row_count) and mcq_count == row_count
    return {
        "row_count": row_count,
        "columns": [{"name": field.name, "dtype": str(field.type)} for field in schema],
        "available_fields": {name: available[name] for name in EVIDENCE_FIELDS},
        "item_feature_value_counts": {
            name: [{"value": json.loads(value), "count": count}
                   for value, count in sorted(values.items())]
            for name, values in sorted(counts.items())
        },
        "item_features_excluded_from_counts": sorted(skipped),
        "item_feature_counting": "Counts items per scalar category; excludes prose fields and nested objects. All observed categories are retained.",
        "is_mcq": all_mcq,
        "output_format": {
            "is_multiple_choice": all_mcq,
            "status": "all" if all_mcq else "some" if mcq_count else "not_established",
            "item_count": row_count,
            "items_with_explicit_choices": explicit_count,
            "items_with_choice_lines": line_count,
            "items_with_either_choice_evidence": mcq_count,
            "basis": "Observed choices/options collections or lines labeled A and B followed by a period or closing parenthesis. Reference-answer letters alone are insufficient.",
        },
        "has_media": bool(media_counts or assets_count),
        "media_fields": sorted(media_fields),
        "media_assets_loaded": False,
        "modality": {
            "items_with_asset_manifest": assets_count,
            "items_with_media_markers": {kind: media_counts[kind] for kind in MEDIA_KEYS},
            "note": "Counts observable populated media fields or type metadata. Assets were not opened; absent markers do not establish absence of media.",
        },
    }


def prepare_data(items_path: Path, output_dir: Path, *, benchmark: str, seed: int = 42,
                 source_repo: str = "aims-foundations/measurement-db",
                 source_revision: str | None = None,
                 source_table: str | None = None) -> dict:
    """Validate, profile, and save all items without changing the source table.

    A local file is pinned by its checksum even if its repository revision is
    unknown. Snapshot-path provenance records historical cache availability;
    this function makes no claim that the revision can still be downloaded.
    Existing prepared artifacts are never overwritten. Parquet content is read
    in batches and spooled to disk; only byte offsets, identity sets and complete
    profile counts remain in memory. Shuffling offsets produces the same order
    as shuffling the full item list with the same seed.
    Populated named benchmark IDs must match ``benchmark`` exactly; opaque
    IDs are retained with an explicit unverified-identity status in the profile.
    """
    import pyarrow.parquet as pq

    items_path = Path(items_path).expanduser().absolute()
    output_dir = Path(output_dir)
    destinations = [output_dir / name for name in ("items.jsonl", "profile.json", "dataset.json")]
    if any(path.exists() for path in destinations):
        raise FileExistsError(f"Prepared dataset files already exist in {output_dir}")
    if not benchmark.strip():
        raise ValueError("benchmark must not be empty")
    inferred = re.search(r"/snapshots/([^/]+)/(.+)$", str(items_path))
    if inferred and source_revision is not None and source_revision != inferred.group(1):
        raise ValueError("Provided source_revision contradicts the local cache snapshot path")
    if inferred and source_table is not None and source_table != inferred.group(2):
        raise ValueError("Provided source_table contradicts the local cache snapshot path")
    source_hash = file_sha256(items_path)
    offsets = array("Q")
    seen = set()
    observed_benchmarks = set()
    # Keep source-order records on disk until every row, source identity, and
    # serialized value passes validation. No prepared outputs exist on failure.
    with TemporaryFile(mode="w+b") as spool:
        with pq.ParquetFile(items_path) as parquet:
            if "item_id" not in parquet.schema_arrow.names:
                raise ValueError("Source table must have an item_id column")

            def normalized_items():
                row_number = 0
                # Decode one batch at a time without parallel column buffers;
                # large multilingual tables must fit the website's memory budget.
                for batch in parquet.iter_batches(batch_size=PREPARATION_BATCH_ROWS, use_threads=False):
                    for row in batch.to_pylist():
                        row_number += 1
                        if _present(row.get("benchmark_id")):
                            observed_benchmarks.add(str(row["benchmark_id"]))
                        item = _normalize(row, row_number)
                        if item["item_id"] in seen:
                            raise ValueError(f"Duplicate item_id {item['item_id']!r}; source population must have unique IDs")
                        seen.add(item["item_id"])
                        serialized = (_json(item) + "\n").encode("utf-8")
                        offsets.append(spool.tell())
                        spool.write(serialized)
                        yield item

            profile = _profile(normalized_items(), parquet.schema_arrow)
        if not offsets:
            raise ValueError("Source table contains no items")
        profile["benchmark_identity"] = _benchmark_identity(observed_benchmarks, benchmark)
        if file_sha256(items_path) != source_hash:
            raise ValueError("Source table changed while preparing data")
        # Fisher–Yates uses only positions, so shuffling offsets exactly preserves
        # the former seeded permutation while retaining all rows and evidence.
        random.Random(seed).shuffle(offsets)
        profile_text = json.dumps(profile, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        revision_origin = "provided" if source_revision else "cache_path" if inferred else "unknown"
        source_revision = source_revision or (inferred.group(1) if inferred else None)
        source_table = source_table or (inferred.group(2) if inferred else items_path.name)
        output_dir.mkdir(parents=True, exist_ok=True)
        with destinations[0].open("xb") as stream:
            for offset in offsets:
                spool.seek(offset)
                stream.write(spool.readline())
        with destinations[1].open("x", encoding="utf-8") as stream:
            stream.write(profile_text + "\n")
    manifest = {
        "version": 1, "benchmark": benchmark, "item_count": len(offsets), "seed": seed,
        "source": {
            "repo": source_repo, "revision": source_revision, "table": source_table,
            "path": str(items_path), "sha256": source_hash,
            "revision_origin": revision_origin,
        },
        "items_sha256": file_sha256(destinations[0]),
        "profile_sha256": file_sha256(destinations[1]),
    }
    with destinations[2].open("x", encoding="utf-8") as stream:
        json.dump(manifest, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")
    return manifest
