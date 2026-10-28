"""Public, immutable item-analysis snapshots curated alongside gallery reports.

Publishing is a local author operation (see website/scripts); serving a saved
snapshot never creates a run, reads browser credentials, or calls a model.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from . import gallery

SNAPSHOT_ROOT = Path(__file__).resolve().parents[1] / "gallery_item_analyses"
ARTIFACTS = {
    "spec": ("classifier_spec.json", "application/json"),
    "items": ("evaluated-items.csv", "text/csv"),
    "summary": ("summary.json", "application/json"),
    "report": ("report.html", "text/html"),
    "package": ("complete-results.zip", "application/zip"),
}
_METADATA_FIELDS = ("run_id", "item_count", "total_items", "completed_at", "model")


def assessment_fingerprint(report: dict) -> str:
    """Bind publication to the exact curated deployment and benchmark scores."""
    content = {key: report[key] for key in
               ("id", "slug", "deployment_description", "scoring")}
    return hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def _directory(entry_id: str) -> Path | None:
    if entry_id not in gallery._entry_ids():
        return None
    path = SNAPSHOT_ROOT / entry_id
    if not path.is_dir() or path.is_symlink() or path.resolve().parent != SNAPSHOT_ROOT.resolve():
        return None
    return path


def published_metadata(entry_id: str, report: dict) -> dict | None:
    directory = _directory(entry_id)
    if directory is None:
        return None
    try:
        metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
        if (metadata["schema_version"] != 1 or metadata["assessment_id"] != entry_id
                or metadata["assessment_fingerprint"] != assessment_fingerprint(report)):
            return None
        return {key: metadata[key] for key in _METADATA_FIELDS}
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _published_directory(entry_id: str) -> Path | None:
    report = gallery.get_report(entry_id)
    return _directory(entry_id) if report and report.get("item_analysis") else None


def get_snapshot(entry_id: str) -> dict | None:
    directory = _published_directory(entry_id)
    if directory is None:
        return None
    try:
        return json.loads((directory / "snapshot.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def get_artifact(entry_id: str, artifact: str) -> tuple[bytes, str, str] | None:
    """Serve only known export members; never join user input to an archive path."""
    if artifact not in ARTIFACTS:
        return None
    directory = _published_directory(entry_id)
    if directory is None:
        return None
    filename, media_type = ARTIFACTS[artifact]
    try:
        if artifact in {"items", "package"}:
            content = (directory / filename).read_bytes()
        else:
            with ZipFile(directory / "complete-results.zip") as archive:
                # Import normalizes directory exports to root members and keeps
                # an existing ZIP byte-for-byte, including its optional folder.
                manifests = [name for name in archive.namelist()
                             if name == "manifest.json" or name.endswith("/manifest.json")]
                if len(manifests) != 1:
                    return None
                prefix = manifests[0][:-len("manifest.json")]
                content = archive.read(prefix + filename)
        return content, media_type, filename
    except (OSError, KeyError, BadZipFile):
        return None
