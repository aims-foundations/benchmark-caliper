"""Private, durable candidate evidence with small explicit in-memory references.

Rankings and assessments retain their ordinary metadata. The three potentially
large evidence fields live in immutable compressed files and are read only when
a caller needs one full candidate. No candidate field is dropped or rewritten.
"""

from __future__ import annotations

from contextlib import suppress
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import zlib

from bayesian_auditing.benchmark_data import row_fingerprint


REFERENCE_KEY = "_candidate_ref"
EVIDENCE_FIELDS = ("evidence", "search_text", "question_text")
_REFERENCE = re.compile(r"[a-f0-9]{64}")


class CandidateStoreError(Exception):
    """A safe storage error that never includes evidence or filesystem paths."""


def has_ref(record: dict) -> bool:
    """Recognize references, including malformed ones that must be rejected."""
    return isinstance(record, dict) and REFERENCE_KEY in record


def _encoded(payload: dict):
    encoder = json.JSONEncoder(ensure_ascii=False, sort_keys=True,
                               separators=(",", ":"), allow_nan=False)
    for chunk in encoder.iterencode(payload):
        yield chunk.encode("utf-8")


def _reference(record: dict) -> str:
    reference = record[REFERENCE_KEY]
    if (not isinstance(reference, str) or _REFERENCE.fullmatch(reference) is None
            or any(key in record for key in EVIDENCE_FIELDS)):
        raise ValueError("Invalid candidate reference")
    return reference


def _validate_identity(record: dict, payload: dict) -> None:
    if (not isinstance(payload, dict) or "evidence" not in payload
            or any(key not in EVIDENCE_FIELDS for key in payload)):
        raise ValueError("Invalid candidate evidence")
    evidence = payload["evidence"]
    if not isinstance(evidence, dict) or not isinstance(evidence.get("item"), dict):
        raise ValueError("Invalid original row")
    identity = row_fingerprint(evidence["item"])
    if record.get("item_id") != identity or record.get("evidence_hash") != identity:
        raise ValueError("Candidate identity differs from its original row")


class CandidateStore:
    def __init__(self, directory: Path):
        # The owner supplies its private review-runs/candidates directory. No
        # record or caller-provided reference can choose a filesystem location.
        self.directory = Path(directory)

    def compact(self, record: dict) -> dict:
        """Persist full evidence and return metadata plus its immutable hash.

        This also accepts screened candidates: assessment and acquisition fields
        stay in the returned record. Reusing an existing reference is cheap.
        """
        temporary = None
        try:
            if not isinstance(record, dict):
                raise ValueError("Invalid candidate")
            if has_ref(record):
                _reference(record)
                return dict(record)
            payload = {key: record[key] for key in EVIDENCE_FIELDS if key in record}
            _validate_identity(record, payload)
            self.directory.mkdir(mode=0o700, parents=True, exist_ok=True)
            self.directory.chmod(0o700)
            digest = hashlib.sha256()
            with tempfile.NamedTemporaryFile(dir=self.directory, prefix=".saving-", delete=False) as stream:
                temporary = Path(stream.name)
                with gzip.GzipFile(fileobj=stream, mode="wb", compresslevel=1, mtime=0) as compressed:
                    pending = bytearray()
                    for chunk in _encoded(payload):
                        digest.update(chunk)
                        pending.extend(chunk)
                        if len(pending) >= 64 * 1024:
                            compressed.write(pending)
                            pending.clear()
                    compressed.write(pending)
                stream.flush()
                os.fsync(stream.fileno())
            reference = digest.hexdigest()
            os.replace(temporary, self.directory / f"{reference}.json.gz")
            directory_fd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
            return {**{key: value for key, value in record.items() if key not in EVIDENCE_FIELDS},
                    REFERENCE_KEY: reference}
        except (OSError, ValueError, TypeError, KeyError, OverflowError):
            raise CandidateStoreError("Could not save candidate evidence.") from None
        finally:
            if temporary is not None:
                with suppress(OSError):
                    temporary.unlink(missing_ok=True)

    def expand(self, record: dict) -> dict:
        """Read one candidate without retaining a cache of its large fields.

        Legacy full records are returned unchanged. References must resolve to
        the exact original payload and row identity before evidence is exposed.
        """
        if not has_ref(record):
            return record
        try:
            reference = _reference(record)
            with gzip.open(self.directory / f"{reference}.json.gz", "rt", encoding="utf-8") as stream:
                payload = json.load(stream)
            digest = hashlib.sha256()
            for chunk in _encoded(payload):
                digest.update(chunk)
            if digest.hexdigest() != reference:
                raise ValueError("Candidate evidence checksum differs")
            _validate_identity(record, payload)
            return {**{key: value for key, value in record.items() if key != REFERENCE_KEY}, **payload}
        except (OSError, ValueError, TypeError, KeyError, OverflowError, EOFError, zlib.error):
            raise CandidateStoreError("Could not read candidate evidence.") from None

    put = compact
    resolve = expand
