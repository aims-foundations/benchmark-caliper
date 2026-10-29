"""Ephemeral prepared ZIPs; saved pipeline results remain the durable source."""

import asyncio
from dataclasses import dataclass, field
import hashlib
from threading import Lock
from typing import BinaryIO

from . import streaming_json


# Different visitors must not compress large archives at the same time.
_build_lock = Lock()


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

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def public(self):
        if self.task is not None and not self.task.done():
            return {"status": "preparing", "message": "Preparing the results package."}
        if self.file is not None:
            return {"status": "ready", "message": "The results package is ready.",
                    "filename": self.filename, "bytes": self.size}
        if self.error:
            return {"status": "failed", **self.error}
        return {"status": "not_started", "message": "Prepare the package to download the saved results."}
