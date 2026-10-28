"""Private durable checkpoints for the goal-conditioned construction pipeline.

The small run record and immutable retrieval evidence are separate compressed
JSON files. Multiple stages can reference the same evidence without copying it
on disk or rewriting it after every screening response. API keys are never
accepted by this store; access tokens are saved only as SHA-256 digests.
"""

from __future__ import annotations

from contextlib import contextmanager
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import tempfile
import zlib

from .candidate_store import CandidateStore, CandidateStoreError, has_ref
from .streaming_json import load


VERSION = 2


class CheckpointError(Exception):
    """Saving or reading a checkpoint failed; never include private data."""


class AccessDenied(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


def token_hash(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


class Checkpoints:
    def __init__(self, directory: Path):
        self.directory = directory

    def run_path(self, run_id: str) -> Path:
        # Never interpret a supplied run ID as part of a filesystem path.
        return self.directory / f"{token_hash(run_id)}.json.gz"

    @contextmanager
    def _temporary(self):
        self.directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.directory.chmod(0o700)
        with tempfile.NamedTemporaryFile(dir=self.directory, prefix=".saving-", delete=False) as stream:
            path = Path(stream.name)
            try:
                yield stream, path
            finally:
                path.unlink(missing_ok=True)

    def _write(self, payload: dict, destination: Path | None = None) -> str:
        """Commit one complete JSON document; failures leave the old file intact."""
        digest = hashlib.sha256()
        encoder = json.JSONEncoder(ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":"), allow_nan=False)
        with self._temporary() as (stream, temporary):
            with gzip.GzipFile(fileobj=stream, mode="wb", compresslevel=1, mtime=0) as compressed:
                pending = bytearray()
                for chunk in encoder.iterencode(payload):
                    pending.extend(chunk.encode("utf-8"))
                    if len(pending) >= 64 * 1024:
                        digest.update(pending)
                        compressed.write(pending)
                        pending.clear()
                digest.update(pending)
                compressed.write(pending)
            stream.flush()
            os.fsync(stream.fileno())
            reference = digest.hexdigest()
            target = destination or self.directory / f"evidence-{reference}.json.gz"
            if destination is not None or not target.exists():
                os.replace(temporary, target)
                directory_fd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
        return reference

    def save(self, run_id: str, secret: str, state: dict, *, retrieval: dict | None,
             retrieval_ref: str | None = None) -> str | None:
        try:
            if retrieval is None:
                retrieval_ref = None
            elif retrieval_ref is None:
                retrieval_ref = self._write(retrieval)
            self._write({"version": VERSION, "token_hash": token_hash(secret),
                         "run": state, "retrieval_ref": retrieval_ref}, self.run_path(run_id))
            return retrieval_ref
        except (OSError, ValueError, TypeError, CandidateStoreError) as exc:
            raise CheckpointError("Could not save the review checkpoint.") from exc

    def load(self, run_id: str, secret: str) -> tuple[dict, str | None]:
        """Authenticate first, then restore old or new evidence one row at a time.

        Older run files embed complete screened rows. The first pass discards
        those rows without writing anything; only an authenticated second pass
        migrates them to the candidate store. Both passes use the same open file
        so an atomic checkpoint update cannot change the authenticated snapshot.
        """
        candidates = CandidateStore(self.directory / "candidates")
        validated = set()

        def compact(record):
            reference = candidates.compact(record)
            if has_ref(record):
                identity = (reference["_candidate_ref"], reference.get("item_id"),
                            reference.get("evidence_hash"))
                if identity not in validated:
                    candidates.expand(reference)
                    validated.add(identity)
            return reference

        def screening_path(path):
            return (len(path) == 4 and path[:3] == ("run", "screening", "items")
                    and type(path[3]) is int)

        def restore_screening(path, record):
            return compact(record) if screening_path(path) else record

        def restore_retrieval(path, record):
            if (len(path) == 4 and path[0] == "rankings" and type(path[1]) is int
                    and path[2] == "candidates" and type(path[3]) is int):
                return compact(record)
            return record

        discarded_screening = False

        def authentication_pass(path, record):
            nonlocal discarded_screening
            if screening_path(path):
                discarded_screening = True
                return {}
            return record

        try:
            with self.run_path(run_id).open("rb") as source:
                with gzip.GzipFile(fileobj=source, mode="rb") as stream:
                    record = load(stream, transform=authentication_pass)
                if not secrets.compare_digest(record["token_hash"], token_hash(secret)):
                    raise AccessDenied("invalid_token")
                if (type(record["version"]) is not int or record["version"] not in {1, VERSION}
                        or record["run"]["run_id"] != run_id):
                    raise ValueError("Unsupported checkpoint")
                if discarded_screening:
                    source.seek(0)
                    with gzip.GzipFile(fileobj=source, mode="rb") as stream:
                        record = load(stream, transform=restore_screening)
        except FileNotFoundError:
            raise AccessDenied("missing_run") from None
        except (OSError, ValueError, TypeError, KeyError, EOFError, zlib.error, CandidateStoreError) as exc:
            raise CheckpointError("Could not read the review checkpoint.") from exc
        try:
            state, reference = record["run"], record["retrieval_ref"]
            retrieval = None
            if reference is not None:
                if not isinstance(reference, str) or not re.fullmatch(r"[a-f0-9]{64}", reference):
                    raise ValueError("Invalid evidence reference")
                with gzip.open(self.directory / f"evidence-{reference}.json.gz", "rb") as stream:
                    retrieval = load(stream, transform=restore_retrieval)
                if not isinstance(retrieval, dict):
                    raise ValueError("Invalid retrieval evidence")
            return {**state, "benchmark_retrieval": retrieval}, reference
        except (OSError, ValueError, TypeError, KeyError, EOFError, zlib.error, CandidateStoreError) as exc:
            raise CheckpointError("Could not read the review checkpoint.") from exc
