"""Load the website's real MMLU example from a pinned Hugging Face snapshot.

Only source metadata and classification instructions ship with the website.
Dataset contents are downloaded using the server's Hugging Face access and
cached privately on its data disk. HTTP clients cannot choose a repo or revision.
"""

from pathlib import Path
import shutil
from typing import Callable

from huggingface_hub import get_token, hf_hub_download

from anthropic_api_package_release.item_analysis.data import file_sha256
from anthropic_api_package_release.item_analysis.prepare import prepare
from . import db

REPO_ID = "aims-foundations/measurement-db-pp"
REVISION = "cc796d3545a6bd2e78b5513c13e60a6913d01e3f"
TABLE_PATH = "mmlu/items.parquet"
ITEM_COUNT = 14015
TABLE_SHA256 = "b1f8008870e1db4e8a0b9c98ec9be05b2d87715c42439d35b2618f9361bd6bad"
SOURCE_URL = f"https://huggingface.co/datasets/{REPO_ID}/tree/{REVISION}/mmlu"
ASSESSMENT_DIR = (Path(__file__).resolve().parents[2] / "anthropic_api_package_release"
                  / "assessments/expert_1a429e941728__mmlu/india_hindi_competitive_exam_prep")
SPEC_PATH = Path(__file__).with_name("item_analysis_mmlu_spec.json")


class DatasetAccessError(RuntimeError):
    """A credential problem safe to describe without exposing provider details."""


class DatasetPreparationError(RuntimeError):
    """A download or snapshot-validation failure with a safe public message."""


def source_entry() -> dict:
    configured = bool(get_token())
    return {
        "id": "mmlu", "title": "MMLU · Hindi-medium exam preparation",
        "benchmark": "mmlu", "item_count": ITEM_COUNT,
        "deployment": (ASSESSMENT_DIR / "deployment_description.txt").read_text(encoding="utf-8"),
        "description": "Real MMLU items loaded from measurement-db-pp on Hugging Face, paired with the original Caliper assessment. Review 100 items, then continue through the full snapshot.",
        "source_label": f"{REPO_ID} · {TABLE_PATH} · {ITEM_COUNT:,}-item snapshot",
        "source_url": SOURCE_URL, "source_revision": REVISION,
        "available": configured, "supplied_spec_available": True,
        "unavailable_reason": None if configured else (
            "MMLU needs server-side Hugging Face access. The maintainer must configure HF_TOKEN "
            "with read access to aims-foundations/measurement-db-pp."
        ),
    }


def prepare_source(directory: Path, stopped: Callable[[], bool] | None = None) -> Path:
    """Download/cache all source items, then use the shared deterministic preparation.

    Hugging Face locks and atomically publishes downloads in its cache. Each
    analysis still gets its own immutable prepared inputs and saved item order.
    Stop is checked before and after the file download and preparation; no model
    requests occur here, and no credential enters the prepared files.
    """
    def check_stopped():
        if stopped and stopped():
            raise InterruptedError("Dataset preparation stopped.")

    check_stopped()
    token = get_token()
    if not token:
        raise DatasetAccessError(source_entry()["unavailable_reason"])
    cache = db.DEFAULT_DB_PATH.parent / "item-analysis-sources"
    cache.mkdir(parents=True, mode=0o700, exist_ok=True)
    try:
        items = Path(hf_hub_download(
            repo_id=REPO_ID, filename=TABLE_PATH, repo_type="dataset",
            revision=REVISION, token=token, cache_dir=cache, etag_timeout=20,
        ))
    except Exception as exc:
        status = getattr(getattr(exc, "response", None), "status_code", None)
        if status in {401, 403, 404}:
            raise DatasetAccessError(
                "The server's Hugging Face account cannot read the pinned MMLU snapshot. "
                "The maintainer must grant its HF_TOKEN access to aims-foundations/measurement-db-pp."
            ) from None
        raise DatasetPreparationError(
            "MMLU could not be downloaded from Hugging Face. No model calls were made; try again later."
        ) from None
    finally:
        token = None
    check_stopped()
    try:
        import pyarrow.parquet as pq

        if file_sha256(items) != TABLE_SHA256:
            raise ValueError("Snapshot checksum differs")
        with pq.ParquetFile(items) as parquet:
            if parquet.metadata.num_rows != ITEM_COUNT:
                raise ValueError("Snapshot row count differs")
            if not {"item_id", "content", "reference_answer"}.issubset(parquet.schema_arrow.names):
                raise ValueError("Snapshot columns differ")
        prepare(ASSESSMENT_DIR, items, directory, benchmark="mmlu", seed=42,
                source_repo=REPO_ID, source_revision=REVISION, source_table=TABLE_PATH)
        supplied = directory / "provided_spec.json"
        shutil.copyfile(SPEC_PATH, supplied)
    except Exception:
        raise DatasetPreparationError(
            "The MMLU snapshot or its assessment failed validation. No model calls were made; "
            "the maintainer should check the pinned dataset and source cache."
        ) from None
    check_stopped()
    return supplied
