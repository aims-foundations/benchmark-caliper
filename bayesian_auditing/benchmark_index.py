"""Search all pinned benchmark items without keeping the corpus in memory.

The SQLite cache holds row fingerprints, source references, contentless FTS5
postings, and BGE vectors. Original rows are streamed through bounded embedding
batches and fetched again only for the final dense/BM25 candidate union.
"""

from __future__ import annotations

from copy import deepcopy
from contextlib import contextmanager
import fcntl
import hashlib
import heapq
from itertools import chain, islice
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import tempfile
import time
from typing import Callable, Iterable

from .benchmark_data import BENCHMARK_DATA_VERSION, row_fingerprint, row_search_text, row_text
from .benchmark_encoding import FullRowBGEEncoder
from .data import fingerprint
from .onet import MAX_TOKENS, MODEL_ID, MODEL_REVISION, QUERY_INSTRUCTION, RRF_K
from .retrieval import _unit_vectors, question_text


DEFAULT_CACHE_DIR = Path.home() / ".cache" / "benchmark-caliper" / "benchmark-index"
DEFAULT_DENSE_K = 600
DEFAULT_BM25_K = 600
ENCODING_BATCH_SIZE = 64
SCAN_BATCH_SIZE = 2048
INDEX_VERSION = 3
DEFAULT_MINIMUM_FREE_BYTES = 15_000_000_000


def _check_cancelled(cancelled):
    if cancelled is not None and cancelled():
        raise InterruptedError("Benchmark retrieval was cancelled")


def _json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def _policy(encoder) -> dict:
    custom = encoder is not None and not isinstance(encoder, FullRowBGEEncoder)
    return {
        "version": INDEX_VERSION,
        "loader_version": BENCHMARK_DATA_VERSION,
        "method": "bge_bm25_rrf",
        "corpus": "All rows in the selected pinned inventory; no sampling",
        "deduplication": "Exact complete original row; source provenance is outside identity",
        "storage": {
            "original_rows": "Fetched from pinned source tables only for the final candidate union",
            "collision_check": "Independent SHA-512 of the complete canonical original row",
            "keyword_index": "Contentless FTS5 with default full detail and column-size statistics",
        },
        "embedding": {
            "model": "custom" if custom else MODEL_ID,
            "revision": None if custom else MODEL_REVISION,
            "encoder_namespace": getattr(encoder, "cache_namespace", f"{type(encoder).__module__}.{type(encoder).__qualname__}") if custom else None,
            "dimensions": getattr(encoder, "dimensions", None) if custom else FullRowBGEEncoder.dimensions,
            "max_tokens_per_chunk": MAX_TOKENS,
            "chunking": "Nonoverlapping token chunks; reserve tokenizer special-token positions",
            "pooling": "L2-normalized CLS per chunk, equal mean of every chunk, final L2 normalization",
            "normalization": "l2", "truncation": "none", "similarity": "dot_product",
            "query_instruction": QUERY_INSTRUCTION, "document_instruction": None,
            "indexed_content": "All original row fields in sorted, labelled text; string values retain their literal whitespace",
        },
        "bm25": {
            "implementation": "SQLite FTS5 bm25", "k1": 1.2, "b": 0.75,
            "indexed_content": "The same complete original row text used for dense retrieval",
            "tokenization": "FTS5 unicode61, remove_diacritics=2; no stemming or stopword removal",
            "query": "OR of quoted Unicode word tokens; operators are treated literally",
            "unmatched_records": "Excluded from keyword ranking",
            "scores": "Negated SQLite BM25 scores; larger is better",
        },
        "fusion": {"method": "reciprocal_rank_fusion", "k": RRF_K,
                   "ranks_start_at": 1, "tie_break": "evidence_hash ascending",
                   "output": "Complete union of dense and BM25 lists; no post-fusion truncation"},
        "candidate_limits": {"dense_k": DEFAULT_DENSE_K, "bm25_k": DEFAULT_BM25_K},
    }


def _encode(encoder, texts, dimensions, cancelled):
    _check_cancelled(cancelled)
    values = (encoder.encode(texts, cancelled=cancelled) if isinstance(encoder, FullRowBGEEncoder)
              else encoder.encode(texts))
    _check_cancelled(cancelled)
    return _unit_vectors(values, rows=len(texts), dimensions=dimensions)


def _report(progress, stage, completed, total, *, cache_hits=0):
    if progress is not None:
        progress({"stage": stage, "completed": completed, "total": total, "cache_hits": cache_hits})


def _schema(connection):
    connection.executescript("""
        BEGIN;
        CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE items (
            item_id TEXT PRIMARY KEY, row_digest BLOB NOT NULL
        );
        CREATE TABLE vectors (item_id TEXT PRIMARY KEY, vector BLOB NOT NULL);
        CREATE TABLE sources (
            item_id TEXT NOT NULL, source_hash TEXT NOT NULL, source TEXT NOT NULL,
            PRIMARY KEY (item_id, source_hash)
        );
        CREATE VIRTUAL TABLE search_fts USING fts5(
            search_text, content='',
            tokenize='unicode61 remove_diacritics 2'
        );
    """)


def _row_digest(row):
    return hashlib.sha512(row_text(row).encode("utf-8")).digest()


def _add_item(connection, item):
    """Add hashes, postings and provenance within the current batch transaction.

    Return new searchable text only until its vector is computed; raw row text
    is never stored in the database or its rollback journal.
    """
    evidence = item["evidence"]
    if not isinstance(evidence, dict) or not isinstance(evidence.get("item"), dict):
        raise ValueError("Benchmark evidence must contain its complete original row")
    row = evidence["item"]
    key = row_fingerprint(row)
    digest = _row_digest(row)
    if item.get("evidence_hash") is not None and item["evidence_hash"] != key:
        raise ValueError("Benchmark evidence_hash must match the complete original row")
    existing = connection.execute("SELECT row_digest FROM items WHERE item_id = ?", (key,)).fetchone()
    if existing is not None and existing[0] != digest:
        raise ValueError(f"Conflicting original rows for evidence_hash {key}")
    sources = list(item.get("sources", []))
    if "source" in item:
        sources.append(item["source"])
    if not sources or any(not isinstance(source, dict) or not isinstance(source.get("benchmark"), str)
                          or not source["benchmark"].strip() for source in sources):
        raise ValueError("Every benchmark item requires source provenance with a benchmark identifier")
    text = None
    if existing is None:
        text = row_search_text(row)
        cursor = connection.execute(
            "INSERT INTO items(item_id, row_digest) VALUES (?, ?)", (key, digest),
        )
        connection.execute("INSERT INTO search_fts(rowid, search_text) VALUES (?, ?)", (cursor.lastrowid, text))
    inserted = connection.executemany(
        "INSERT OR IGNORE INTO sources(item_id, source_hash, source) VALUES (?, ?, ?)",
        ((key, fingerprint(source), _json(source)) for source in sources),
    )
    return key, text, inserted.rowcount


def _checkpoint(connection, state):
    # Source offset, identities, postings, provenance and vectors commit
    # together. An interrupted batch is retried without losing any raw rows.
    connection.execute("INSERT OR REPLACE INTO metadata(key, value) VALUES ('build_state', ?)",
                       (_json(state),))
    connection.commit()


def _build(connection, items, inventory, encoder, policy, cancelled, progress):
    saved = connection.execute("SELECT value FROM metadata WHERE key = 'build_state'").fetchone()
    state = json.loads(saved[0]) if saved else {
        "source_rows": 0, "dimensions": policy["embedding"]["dimensions"],
        "stats": {"source_rows": 0, "total_items": 0, "indexed_items": 0,
                  "contentless_items": 0, "source_references": 0, "unique_documents": 0,
                  "embedded_documents": 0, "cache_hit": False},
    }
    stats, source_rows = state["stats"], state["source_rows"]
    estimated_rows = sum(table.get("row_count", 0) for table in inventory.get("tables", []))
    _report(progress, "indexing", source_rows, estimated_rows)
    pending = []

    def flush():
        _check_cancelled(cancelled)
        if pending:
            vectors = _encode(encoder, [text for _, text in pending], state["dimensions"], cancelled)
            state["dimensions"] = vectors.shape[1]
            connection.executemany(
                "INSERT INTO vectors(item_id, vector) VALUES (?, ?)",
                ((row[0], vector.astype("<f4").tobytes()) for row, vector in zip(pending, vectors)),
            )
            stats["embedded_documents"] += len(pending)
        state["source_rows"] = stats["source_rows"] = source_rows
        _check_cancelled(cancelled)
        _checkpoint(connection, state)
        pending.clear()
        _report(progress, "indexing", source_rows, estimated_rows)

    # Factories can skip committed tables/row groups without fetching them.
    remaining = items(source_rows) if callable(items) else islice(items, source_rows, None)
    try:
        for item in remaining:
            _check_cancelled(cancelled)
            key, text, references = _add_item(connection, item)
            source_rows += 1
            stats["source_references"] += references
            if text is not None:
                pending.append((key, text))
                for field in ("total_items", "indexed_items", "unique_documents"):
                    stats[field] += 1
            if len(pending) == ENCODING_BATCH_SIZE or source_rows % 1024 == 0:
                flush()
        expected_counts = [table.get("row_count") for table in inventory["tables"]]
        if all(type(value) is int and value >= 0 for value in expected_counts):
            if source_rows != sum(expected_counts):
                raise ValueError("Loaded benchmark row count differs from the pinned inventory")
        estimated_rows = source_rows
        flush()
    finally:
        if callable(items) and hasattr(remaining, "close"):
            remaining.close()
    policy["embedding"]["dimensions"] = state["dimensions"]
    _check_cancelled(cancelled)
    connection.execute("INSERT INTO search_fts(search_fts) VALUES ('optimize')")
    connection.commit()
    return stats


class BenchmarkIndex:
    """An opened completed cache, used and closed on its creating thread.

    Each search returns the complete union of its dense and keyword lists.
    Only shortlisted records are decoded into full evidence objects in memory.
    """

    def __init__(self, path, encoder=None, *, cache_hit=True, row_loader=None):
        self.path = Path(path)
        self._connection = sqlite3.connect(self.path.resolve().as_uri() + "?mode=ro", uri=True)
        try:
            metadata = dict(self._connection.execute("SELECT key, value FROM metadata"))
            if json.loads(metadata.get("complete", "false")) is not True:
                raise ValueError("Benchmark cache is incomplete")
            self._policy = json.loads(metadata["policy"])
            if self._policy["version"] != INDEX_VERSION:
                raise ValueError("Benchmark cache storage version differs; prepare a new index")
            self._stats = json.loads(metadata["stats"])
            self._cache_key = json.loads(metadata["cache_key"])
            self._inventory = json.loads(metadata["inventory"])
        except Exception:
            self._connection.close()
            raise
        self._stats["cache_hit"] = cache_hit
        self._encoder = encoder if encoder is not None else FullRowBGEEncoder()
        self._row_loader = row_loader if row_loader is not None else self._fetch_rows

    def _fetch_rows(self, requests, *, cancelled=None):
        from .benchmark_rows import fetch_benchmark_rows

        return fetch_benchmark_rows(self._inventory, requests, cancelled=cancelled)

    @property
    def policy(self):
        return deepcopy(self._policy)

    @property
    def stats(self):
        return deepcopy(self._stats)

    def close(self):
        self._connection.close()

    def _dense(self, query, limit, cancelled):
        import numpy as np

        if not limit or not self._stats["indexed_items"]:
            return []
        dimensions = self._policy["embedding"]["dimensions"]
        query_vector = _encode(self._encoder, [QUERY_INSTRUCTION + query], dimensions, cancelled)[0]
        cursor = self._connection.execute(
            "SELECT item_id, vector FROM vectors"
        )
        best = []
        while True:
            _check_cancelled(cancelled)
            batch = cursor.fetchmany(SCAN_BATCH_SIZE)
            if not batch:
                break
            vectors = np.stack([np.frombuffer(row[1], dtype="<f4") for row in batch])
            if vectors.shape[1] != dimensions or not np.isfinite(vectors).all():
                raise ValueError("Cached benchmark vectors are invalid")
            scores = np.clip(vectors @ query_vector, -1.0, 1.0)
            # Negative scores make smaller tuples better; IDs break score ties.
            best = heapq.nsmallest(limit, chain(best, ((-float(score), row[0]) for row, score in zip(batch, scores))))
        return [(key, -score) for score, key in best]

    def _keyword(self, query, limit):
        tokens = list(dict.fromkeys(re.findall(r"\b\w+\b", query)))
        if not limit or not tokens:
            return []
        expression = " OR ".join('"' + token + '"' for token in tokens)
        return [(key, -score) for key, score in self._connection.execute(
            "SELECT i.item_id, bm25(search_fts) AS score FROM search_fts "
            "JOIN items i ON i.rowid = search_fts.rowid WHERE search_fts MATCH ? "
            "ORDER BY score ASC, i.item_id ASC LIMIT ?", (expression, limit),
        )]

    def search(self, query, *, dense_k=DEFAULT_DENSE_K, bm25_k=DEFAULT_BM25_K,
               cancelled=None) -> list[dict]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Benchmark query must be nonempty text")
        for name, value in (("dense_k", dense_k), ("bm25_k", bm25_k)):
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer")
        if not dense_k and not bm25_k:
            raise ValueError("At least one benchmark retrieval method must be enabled")
        _check_cancelled(cancelled)
        self._connection.set_progress_handler(lambda: int(bool(cancelled and cancelled())), 1000)
        try:
            dense = self._dense(query, dense_k, cancelled)
            keyword = self._keyword(query, bm25_k)
            _check_cancelled(cancelled)
            candidates = {}
            for method, matches in (("dense", dense), ("bm25", keyword)):
                for rank, (key, score) in enumerate(matches, 1):
                    candidate = candidates.setdefault(key, {
                        "item_id": key, "evidence_hash": key, "dense_rank": None, "bm25_rank": None,
                        "dense_score": None, "bm25_score": None, "rrf_score": 0.0,
                    })
                    candidate[f"{method}_rank"] = rank
                    candidate[f"{method}_score"] = score
                    candidate["rrf_score"] += 1.0 / (RRF_K + rank)
            ordered = sorted(candidates.values(), key=lambda row: (-row["rrf_score"], row["item_id"]))
            requests, digests = [], {}
            for rank, candidate in enumerate(ordered, 1):
                _check_cancelled(cancelled)
                key = candidate["item_id"]
                digests[key] = self._connection.execute(
                    "SELECT row_digest FROM items WHERE item_id = ?", (key,),
                ).fetchone()[0]
                sources = [json.loads(row[0]) for row in self._connection.execute(
                    "SELECT source FROM sources WHERE item_id = ? ORDER BY source_hash", (key,),
                )]
                candidate.update(rank=rank, sources=sources)
                requests.append({"item_id": key, "sources": deepcopy(sources)})
            if requests:
                rows = self._row_loader(requests, cancelled=cancelled)
                _check_cancelled(cancelled)
                if not isinstance(rows, dict) or set(rows) != set(candidates):
                    raise ValueError("Fetched benchmark rows must exactly match the shortlisted item IDs")
                for candidate in ordered:
                    _check_cancelled(cancelled)
                    key = candidate["item_id"]
                    row = rows[key]
                    if row_fingerprint(row) != key or _row_digest(row) != digests[key]:
                        raise ValueError(f"Fetched benchmark row does not match its indexed identity: {key}")
                    evidence = {"item": deepcopy(row)}
                    candidate.update(evidence=evidence, search_text=row_search_text(row),
                                     question_text=question_text(evidence))
            self._policy["candidate_limits"] = {"dense_k": dense_k, "bm25_k": bm25_k}
            return ordered
        except sqlite3.OperationalError:
            _check_cancelled(cancelled)
            raise
        finally:
            self._connection.set_progress_handler(None, 0)


@contextmanager
def _build_lock(directory, cancelled):
    """Serialize builders across website and preparation processes.

    Locking the directory inode avoids stale lock files and unlink races. The
    kernel releases the lock if a worker exits, including an abrupt termination.
    """
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        while True:
            _check_cancelled(cancelled)
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                time.sleep(0.1)
        yield
    finally:
        os.close(descriptor)


def prepare_benchmark_index(items: Iterable[dict] | Callable[[int], Iterable[dict]],
                            cache_dir=None, inventory=None, encoder=None,
                            cancelled=None, progress=None, *, resume=False,
                            minimum_free_bytes=0, row_loader=None) -> BenchmarkIndex:
    """Reuse a completed cache or atomically build one from all supplied rows.

    Cache identity includes the pinned inventory, loader version, and complete
    indexing/encoding policy. A cache hit does not consume ``items``. The caller
    retains ownership of a supplied iterator. Alternatively, ``items`` can be a
    factory taking the committed source-row offset; its iterator is closed here.
    With ``resume=True``, committed rows and embeddings survive interruption in
    an unpublished checkpoint. The same pinned inventory and policy must be
    supplied on retry. Incomplete checkpoints are never opened for search.
    ``row_loader(requests, *, cancelled=None)`` may supply shortlisted original
    rows for offline use; the default fetches them from the pinned inventory.
    """
    if not isinstance(inventory, dict) or not inventory.get("tables"):
        raise ValueError("A pinned benchmark inventory with tables is required")
    if any(not table.get("commit") for table in inventory["tables"]):
        raise ValueError("Every benchmark table must identify its pinned commit")
    if type(minimum_free_bytes) is not int or minimum_free_bytes < 0:
        raise ValueError("Minimum free disk bytes must be a nonnegative integer")
    _check_cancelled(cancelled)
    policy = _policy(encoder)
    cache_key = fingerprint({"inventory": inventory, "policy": policy})
    directory = Path(cache_dir) if cache_dir is not None else DEFAULT_CACHE_DIR
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    directory.chmod(0o700)

    def guarded_progress(state):
        if state["stage"] != "cache" and shutil.disk_usage(directory).free < minimum_free_bytes:
            raise OSError(f"Free disk space is below the {minimum_free_bytes / 1e9:g} GB reserve")
        if progress is not None:
            progress(state)

    with _build_lock(directory, cancelled):
        return _prepare_locked(items, directory, inventory, encoder, cancelled,
                               guarded_progress, resume, policy, cache_key, row_loader)


def _prepare_locked(items, directory, inventory, encoder, cancelled, progress,
                    resume, policy, cache_key, row_loader):
    path = directory / f"{cache_key}.sqlite3"
    if path.exists():
        index = BenchmarkIndex(path, encoder, cache_hit=True, row_loader=row_loader)
        if index._cache_key != cache_key:
            index.close()
            raise ValueError("Benchmark cache identity does not match the pinned inventory")
        _report(progress, "cache", index.stats["unique_documents"], index.stats["unique_documents"],
                cache_hits=index.stats["unique_documents"])
        return index
    encoder = encoder if encoder is not None else FullRowBGEEncoder()
    if resume:
        temporary = directory / f"{cache_key}.building.sqlite3"
        temporary.touch(mode=0o600, exist_ok=True)
    else:
        with tempfile.NamedTemporaryFile(prefix="building-", suffix=".sqlite3", dir=directory, delete=False) as handle:
            temporary = Path(handle.name)
    connection = None
    try:
        connection = sqlite3.connect(temporary)
        connection.execute("PRAGMA cache_size = -262144")  # Bound build page cache to 256 MiB.
        connection.set_progress_handler(lambda: int(bool(cancelled and cancelled())), 1000)
        if not connection.execute("SELECT name FROM sqlite_master WHERE name = 'metadata'").fetchone():
            _schema(connection)
            connection.execute("INSERT INTO metadata(key, value) VALUES ('cache_key', ?)", (_json(cache_key),))
            connection.commit()
        else:
            saved = connection.execute("SELECT value FROM metadata WHERE key = 'cache_key'").fetchone()
            if saved is None or json.loads(saved[0]) != cache_key:
                raise ValueError("Benchmark checkpoint identity does not match the pinned inventory")
            complete = connection.execute("SELECT value FROM metadata WHERE key = 'complete'").fetchone()
            if complete and json.loads(complete[0]) is True:
                # Recover a termination between final commit and publication.
                connection.close()
                connection = None
                _check_cancelled(cancelled)
                temporary.replace(path)
                return BenchmarkIndex(path, encoder, cache_hit=False, row_loader=row_loader)
        stats = _build(connection, items, inventory, encoder, policy, cancelled, progress)
        _check_cancelled(cancelled)
        connection.execute("DELETE FROM metadata WHERE key = 'build_state'")
        connection.executemany("INSERT OR REPLACE INTO metadata(key, value) VALUES (?, ?)",
                               ((key, _json(value)) for key, value in {
                                   "complete": True, "policy": policy, "stats": stats,
                                   "cache_key": cache_key, "inventory": inventory,
                               }.items()))
        connection.commit()
        connection.close()
        connection = None
        _check_cancelled(cancelled)
        temporary.replace(path)
        return BenchmarkIndex(path, encoder, cache_hit=False, row_loader=row_loader)
    except sqlite3.OperationalError:
        _check_cancelled(cancelled)
        raise
    finally:
        if connection is not None:
            connection.close()
        if not resume:
            temporary.unlink(missing_ok=True)
            Path(str(temporary) + "-journal").unlink(missing_ok=True)
