"""Load server-configured benchmarks and their matching Caliper assessments.

Only source metadata and MMLU's example criteria ship with the website. Tables
are pinned by revision and checksum and cached privately. HTTP clients select
catalog IDs; they cannot choose repositories, revisions, or filesystem paths.
"""

from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from typing import Callable

from huggingface_hub import get_token, hf_hub_download

from anthropic_api_package_release.item_analysis.data import file_sha256
from anthropic_api_package_release.item_analysis.prepare import prepare
from anthropic_api_package_release.item_analysis.storage import read_json, write_json
from . import db
from .item_analysis_adapters import normalize_source

SOURCES_PATH = Path(__file__).with_name("item_analysis_sources.json")
ASSESSMENTS_DIR = (Path(__file__).resolve().parents[2] / "anthropic_api_package_release" / "assessments")


class DatasetAccessError(RuntimeError):
    """A credential problem safe to describe without exposing provider details."""


class DatasetPreparationError(RuntimeError):
    """A download or snapshot-validation failure with a safe public message."""


def sources() -> list[dict]:
    return read_json(SOURCES_PATH)


def source_definition(example_id: str) -> dict:
    for source in sources():
        if source["id"] == example_id:
            return source
    raise ValueError("This benchmark is not configured on the server.")


def source_entry(example_id: str = "mmlu") -> dict:
    source = source_definition(example_id)
    available = not source["requires_token"] or bool(get_token())
    label = source["benchmark_title"]
    return {
        "id": source["id"], "title": f"{label} · {source['assessment_title']}",
        "benchmark": source["benchmark"], "benchmark_title": label,
        "assessment_title": source["assessment_title"], "item_count": source["item_count"],
        "deployment": (ASSESSMENTS_DIR / source["assessment_dir"] / "deployment_description.txt").read_text(encoding="utf-8"),
        "description": source.get("description") or f"{label} items paired with the original Caliper assessment for this use case. Review 100 items, then continue through the full snapshot.",
        "source_label": f"{source['repo']} · {source['table_path']} · {source['item_count']:,}-item snapshot",
        "source_url": f"https://huggingface.co/datasets/{source['repo']}/blob/{source['revision']}/{source['table_path']}",
        "source_revision": source["revision"],
        "available": available, "supplied_spec_available": bool(source.get("supplied_spec")),
        "unavailable_reason": None if available else (
            f"{label} needs server-side Hugging Face access. The maintainer must configure HF_TOKEN "
            f"with read access to {source['repo']}."
        ),
    }


def source_entries() -> list[dict]:
    return [source_entry(source["id"]) for source in sources()]


def prepare_source(directory: Path, stopped: Callable[[], bool] | None = None,
                   *, example_id: str = "mmlu") -> Path:
    """Verify the original table, normalize its fields, and freeze run inputs.

    Hugging Face downloads are atomic and cached. Normalization preserves the
    source evidence and never executes code from benchmark items. Every run
    records both the downloaded checksum and, when needed, the normalized one.
    """
    source = source_definition(example_id)
    label = source["benchmark_title"]

    def check_stopped():
        if stopped and stopped():
            raise InterruptedError("Dataset preparation stopped.")

    check_stopped()
    token = get_token() if source["requires_token"] else False
    if source["requires_token"] and not token:
        raise DatasetAccessError(source_entry(example_id)["unavailable_reason"])
    cache = db.DEFAULT_DB_PATH.parent / "item-analysis-sources"
    cache.mkdir(parents=True, mode=0o700, exist_ok=True)
    try:
        items = Path(hf_hub_download(
            repo_id=source["repo"], filename=source["table_path"], repo_type="dataset",
            revision=source["revision"], token=token, cache_dir=cache, etag_timeout=20,
        ))
    except Exception as exc:
        status = getattr(getattr(exc, "response", None), "status_code", None)
        if status in {401, 403, 404}:
            raise DatasetAccessError(
                f"The server cannot read the pinned {label} snapshot. "
                f"The maintainer should check dataset access and the configured source in {source['repo']}."
            ) from None
        raise DatasetPreparationError(
            f"{label} could not be downloaded from Hugging Face. No model calls were made; try again later."
        ) from None
    finally:
        token = None
    check_stopped()
    try:
        import pyarrow.parquet as pq

        if file_sha256(items) != source["sha256"]:
            raise ValueError("Snapshot checksum differs")
        with pq.ParquetFile(items) as parquet:
            if parquet.metadata.num_rows != source["item_count"]:
                raise ValueError("Snapshot row count differs")
            if source["adapter"] == "measurement-db" and not {"item_id", "content"}.issubset(parquet.schema_arrow.names):
                raise ValueError("Snapshot columns differ")
        assessment = ASSESSMENTS_DIR / source["assessment_dir"]
        with TemporaryDirectory(prefix="normalize-", dir=cache) as temporary:
            prepared_items = items
            if source["adapter"] != "measurement-db":
                prepared_items = Path(temporary) / "items.parquet"
                normalize_source(source, items, prepared_items)
            dataset = prepare(assessment, prepared_items, directory, benchmark=source["benchmark"], seed=42,
                              source_repo=source["repo"], source_revision=source["revision"],
                              source_table=source["table_path"])
            if prepared_items != items:
                dataset["source"].update({
                    "normalization": f"{source['adapter']}-v1",
                    "normalized_sha256": dataset["source"]["sha256"],
                    "sha256": source["sha256"], "path": str(items),
                })
                write_json(directory / "dataset.json", dataset)
        supplied = directory / "provided_spec.json"
        if source.get("supplied_spec"):
            shutil.copyfile(Path(__file__).with_name(source["supplied_spec"]), supplied)
    except Exception:
        raise DatasetPreparationError(
            f"The {label} snapshot or its assessment failed validation. No model calls were made; "
            "the maintainer should check the pinned dataset and source cache."
        ) from None
    check_stopped()
    return supplied
