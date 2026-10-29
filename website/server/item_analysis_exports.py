"""Reuse private ZIP exports while the saved run and its artifacts are unchanged."""

import hashlib
import json
from pathlib import Path
from threading import Lock

from anthropic_api_package_release.item_analysis import package
from anthropic_api_package_release.item_analysis.data import file_sha256
from anthropic_api_package_release.item_analysis.storage import read_json, write_json
from . import item_analysis_store as store


CACHE_VERSION = 1
CACHE_NAME = "_package_cache.json"
# Bound compression memory and CPU when different visitors export together.
_build_lock = Lock()


def fingerprint(job) -> str:
    files = {}
    for name in package.ARTIFACTS:
        path = job.directory / name
        if path.is_symlink():
            raise ValueError("Export input must not be a symlink")
        if path.exists():
            info = path.stat()
            if not path.is_file():
                raise ValueError("Export input must be a regular file")
            # Usage is reconstructed during restoration, even if its contents
            # are unchanged. Hash this small file to preserve cache reuse.
            files[name] = file_sha256(path) if name == "usage.json" else [info.st_size, info.st_mtime_ns]
    state = {"version": CACHE_VERSION, "files": files, "run_id": job.run_id,
             "status": job.status, "scope": job.scope, "created_at": job.created_at,
             "updated_at": job.updated_at, "usage": job.usage, "model": job.model}
    return hashlib.sha256(json.dumps(state, sort_keys=True, allow_nan=False).encode()).hexdigest()


def cached_package(job) -> Path | None:
    directory = job.directory / "generated_exports"
    try:
        if directory.is_symlink():
            return None
        metadata = directory / CACHE_NAME
        if metadata.is_symlink():
            return None
        cached = read_json(metadata)
        filename = cached["filename"]
        if (cached["version"] != CACHE_VERSION or not isinstance(filename, str)
                or Path(filename).name != filename or not filename.endswith(".zip")):
            return None
        path = directory / filename
        if path.is_symlink() or not path.is_file():
            return None
        info = path.stat()
        if ([info.st_size, info.st_mtime_ns] != cached["file_state"]
                or fingerprint(job) != cached["fingerprint"]):
            return None
        return path
    except (OSError, ValueError, KeyError, TypeError):
        return None


def build_package(job) -> Path:
    with _build_lock:
        cached = cached_package(job)
        if cached is not None:
            return cached
        path = package.build_results_package(
            job.directory, run_id=job.run_id, status=job.status, scope=job.scope,
            created_at=store.timestamp(job.created_at), updated_at=store.timestamp(job.updated_at),
            usage=job.usage, model=job.model)
        info = path.stat()
        write_json(path.parent / CACHE_NAME, {
            "version": CACHE_VERSION, "fingerprint": fingerprint(job),
            "filename": path.name, "file_state": [info.st_size, info.st_mtime_ns],
        })
        return path
