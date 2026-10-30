"""Public read-only construction examples, explicitly curated by a local importer."""

import gzip
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from zipfile import BadZipFile, ZipFile
import zlib

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, Response, StreamingResponse

from .review_exports import CHUNK_BYTES
from . import construction_retrieval


ROOT = Path(__file__).resolve().parents[1] / "construction_examples"
ENTRY_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
ARTIFACTS = {
    "report": ("report.html", "text/html"),
    "summary_report": ("report-with-composition.html", "text/html"),
    "items": ("selected_items.csv", "text/csv"),
    "results": ("results.json", "application/json"),
    "package": ("complete-results.zip", "application/zip"),
}
router = APIRouter(prefix="/api/item-review/examples", tags=["Construction examples"])


def item_filename(item_id: str) -> str:
    return hashlib.sha256(item_id.encode("utf-8")).hexdigest() + ".json.gz"


def entries() -> list[dict]:
    try:
        path = ROOT / "index.json"
        if path.is_symlink():
            raise ValueError("Invalid catalog")
        catalog = json.loads(path.read_text(encoding="utf-8"))
        values = catalog["examples"]
        if (catalog["schema_version"] != 1 or not isinstance(values, list)
                or any(not isinstance(entry, dict) or not ENTRY_ID.fullmatch(entry.get("id", "")) for entry in values)
                or len({entry["id"] for entry in values}) != len(values)):
            raise ValueError("Invalid catalog")
        return values
    except FileNotFoundError:
        return []
    except (OSError, ValueError, TypeError, KeyError):
        raise HTTPException(503, "The example catalog could not be read.") from None


def published(entry_id: str) -> tuple[dict, Path]:
    entry = next((entry for entry in entries() if entry["id"] == entry_id), None)
    if entry is None:
        raise HTTPException(404, "Construction example not found.")
    directory = ROOT / entry_id
    if directory.is_symlink() or not directory.is_dir() or directory.resolve().parent != ROOT.resolve():
        raise HTTPException(404, "Construction example not found.")
    return entry, directory


def local_file(directory: Path, relative: str) -> Path:
    path = directory / relative
    if (path.is_symlink() or not path.is_file()
            or not path.resolve().is_relative_to(directory.resolve())):
        raise HTTPException(404, "Saved example artifact not found.")
    return path


def snapshot(directory: Path) -> dict:
    try:
        return json.loads(local_file(directory, "snapshot.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise HTTPException(503, "The saved example could not be read.") from None


@router.get("")
def list_examples():
    return {"examples": entries()}


@router.get("/{entry_id}")
def get_example(entry_id: str):
    entry, directory = published(entry_id)
    return {"entry": entry, **snapshot(directory)}


@router.get("/{entry_id}/items/{item_id}")
def get_item(entry_id: str, item_id: str):
    _, directory = published(entry_id)
    if not any(item["item_id"] == item_id for item in snapshot(directory)["items"]):
        raise HTTPException(404, "Saved example item not found.")
    try:
        with gzip.open(local_file(directory, "items/" + item_filename(item_id)), "rt", encoding="utf-8") as stream:
            return json.load(stream)
    except (OSError, ValueError, EOFError, zlib.error):
        raise HTTPException(503, "The saved example item could not be read.") from None


def _retrieval_view(entry_id, read):
    _, directory = published(entry_id)
    path = local_file(directory, construction_retrieval.FILENAME)
    try:
        return read(path)
    except construction_retrieval.RetrievalNotFound as error:
        raise HTTPException(404, str(error)) from None
    except (OSError, ValueError, KeyError, IndexError, TypeError, sqlite3.Error, EOFError, zlib.error):
        raise HTTPException(503, "The saved retrieval records could not be read.") from None


@router.get("/{entry_id}/retrieved")
def get_retrieved(entry_id: str, queue_id: str | None = None,
                  page: int = Query(1, ge=1, le=2**31 - 1), page_size: int = Query(10, ge=1, le=50)):
    return _retrieval_view(entry_id, lambda path: construction_retrieval.page(path, queue_id, page, page_size))


@router.get("/{entry_id}/retrieved/{item_id}")
def get_retrieved_item(entry_id: str, item_id: str, queue_id: str | None = None):
    return _retrieval_view(entry_id, lambda path: construction_retrieval.item(path, queue_id, item_id))


@router.get("/{entry_id}/artifacts/{artifact}")
def get_artifact(entry_id: str, artifact: str):
    if artifact not in ARTIFACTS:
        raise HTTPException(404, "Saved example artifact not found.")
    entry, directory = published(entry_id)
    filename, media_type = ARTIFACTS[artifact]
    headers = {"Cache-Control": "no-cache, no-transform"}
    if artifact in {"report", "summary_report"}:
        headers["Content-Security-Policy"] = (
            "sandbox; default-src 'none'; style-src 'unsafe-inline'; img-src data:; "
            "frame-ancestors 'none'; base-uri 'none'; form-action 'none'"
        )
        return FileResponse(local_file(directory, filename), media_type=media_type,
                            filename=filename, content_disposition_type="inline", headers=headers)
    if artifact != "results":
        return FileResponse(local_file(directory, filename), media_type=media_type, filename=filename, headers=headers)

    archive_path = local_file(directory, "complete-results.zip")
    try:
        members = json.loads(local_file(directory, "archive.json").read_text(encoding="utf-8"))
        member = members["results"]
        with ZipFile(archive_path) as archive:
            size = archive.getinfo(member).file_size
    except (OSError, ValueError, KeyError, BadZipFile):
        raise HTTPException(503, "The saved example archive could not be read.") from None
    if size != entry["artifacts"]["results"]["bytes"]:
        raise HTTPException(503, "The saved example archive could not be read.")

    def content():
        # StreamingResponse advances this iterator off the event loop. Only one
        # decompressed block is retained; the full JSON stays inside the ZIP.
        with ZipFile(archive_path) as archive, archive.open(member) as source:
            while chunk := source.read(64 * 1024):
                yield chunk

    return StreamingResponse(content(), media_type=media_type, headers={
        **headers, "Content-Length": str(size),
        "Content-Disposition": f'attachment; filename="{filename}"',
    })


@router.get("/{entry_id}/package/chunk")
def get_package_chunk(entry_id: str, package_id: str, offset: str):
    entry, directory = published(entry_id)
    package = entry["artifacts"]["package"]
    if package_id != package["package_id"]:
        raise HTTPException(412, "This example package has changed. Open the example again before downloading.")
    try:
        position = int(offset)
    except ValueError:
        raise HTTPException(416, "The requested package offset is invalid.") from None
    if not 0 <= position < package["bytes"]:
        raise HTTPException(416, "The requested package offset is outside the archive.")
    path = local_file(directory, "complete-results.zip")
    expected = min(CHUNK_BYTES, package["bytes"] - position)
    try:
        with path.open("rb") as source:
            if path.stat().st_size != package["bytes"]:
                raise OSError("Archive size changed")
            source.seek(position)
            data = source.read(expected)
        if len(data) != expected:
            raise OSError("Archive is incomplete")
    except OSError:
        raise HTTPException(503, "The saved example package could not be read.") from None
    return Response(data, media_type="application/zip", headers={
        "Cache-Control": "no-store, no-transform", "Content-Length": str(len(data)),
        "X-Package-Id": package_id, "X-Package-Offset": str(position), "X-Accel-Buffering": "no",
    })
