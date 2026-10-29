"""Ephemeral prepared ZIPs; saved pipeline results remain the durable source."""

import asyncio
from dataclasses import dataclass, field
import hashlib
from threading import Lock
import time
from typing import BinaryIO
from uuid import uuid4

from . import streaming_json


# Different visitors must not compress large archives at the same time.
_build_lock = Lock()
CHUNK_BYTES = 1024 * 1024
DOWNLOAD_IDLE_SECONDS = 300


def build(snapshot, *, builder, expand):
    with _build_lock:
        return builder(snapshot, expand=expand)


def snapshot_key(snapshot) -> str:
    digest = hashlib.sha256()
    for chunk in streaming_json.iterencode(snapshot, sort_keys=True):
        digest.update(chunk.encode("utf-8"))
    return digest.hexdigest()


@dataclass
class PreparedPackage:
    key: str = ""
    task: asyncio.Task | None = field(default=None, repr=False)
    file: BinaryIO | None = field(default=None, repr=False)
    filename: str = ""
    size: int = 0
    error: dict | None = None
    transferring: bool = False
    package_id: str = field(default_factory=lambda: str(uuid4()))
    lease_until: float = 0
    read_task: asyncio.Task | None = field(default=None, repr=False)

    def refresh_lease(self):
        self.lease_until = time.monotonic() + DOWNLOAD_IDLE_SECONDS

    def pinned(self) -> bool:
        return self.file is not None and self.lease_until > time.monotonic()

    def close(self):
        self.lease_until = 0
        if self.file is not None:
            self.file.close()
            self.file = None

    def public(self):
        if self.task is not None and not self.task.done():
            return {"status": "preparing", "message": "Preparing the results package."}
        if self.file is not None:
            return {"status": "ready", "message": "The results package is ready.",
                    "filename": self.filename, "bytes": self.size,
                    "package_id": self.package_id, "chunk_bytes": CHUNK_BYTES}
        if self.error:
            return {"status": "failed", **self.error}
        return {"status": "not_started", "message": "Prepare the package to download the saved results."}
