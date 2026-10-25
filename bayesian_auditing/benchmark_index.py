"""Search all pinned benchmark items without keeping the corpus in memory.

The completed SQLite cache holds original evidence, source references, an FTS5
keyword index, and BGE vectors. Building streams source rows and embeds bounded
batches. Searching scans vectors in batches and retains only the best matches.
"""

from __future__ import annotations

from copy import deepcopy
import heapq
from itertools import chain
import json
from pathlib import Path
import re
import sqlite3
import tempfile
from typing import Iterable

from .benchmark_data import BENCHMARK_DATA_VERSION, row_fingerprint, row_search_text
from .benchmark_encoding import FullRowBGEEncoder
from .data import fingerprint
from .onet import MAX_TOKENS, MODEL_ID, MODEL_REVISION, QUERY_INSTRUCTION, RRF_K
from .retrieval import _unit_vectors, question_text


DEFAULT_CACHE_DIR = Path.home() / ".cache" / "benchmark-caliper" / "benchmark-index"
DEFAULT_DENSE_K = 600
DEFAULT_BM25_K = 600
ENCODING_BATCH_SIZE = 64
SCAN_BATCH_SIZE = 2048
INDEX_VERSION = 2


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
        CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE items (
            item_id TEXT PRIMARY KEY, evidence TEXT NOT NULL,
            search_text TEXT NOT NULL, question_text TEXT NOT NULL
        );
        CREATE TABLE vectors (item_id TEXT PRIMARY KEY, vector BLOB NOT NULL);
        CREATE TABLE sources (
            item_id TEXT NOT NULL, source_hash TEXT NOT NULL, source TEXT NOT NULL,
            PRIMARY KEY (item_id, source_hash)
        );
        CREATE VIRTUAL TABLE search_fts USING fts5(
            search_text, content='items', content_rowid='rowid',
            tokenize='unicode61 remove_diacritics 2'
        );
    """)


def _add_item(connection, item):
    evidence = item["evidence"]
    if not isinstance(evidence, dict) or not isinstance(evidence.get("item"), dict):
        raise ValueError("Benchmark evidence must contain its complete original row")
    row = evidence["item"]
    text = row_search_text(row)
    encoded_evidence = _json({"item": row})
    key = row_fingerprint(row)
    if item.get("evidence_hash") is not None and item["evidence_hash"] != key:
        raise ValueError("Benchmark evidence_hash must match the complete original row")
    existing = connection.execute("SELECT evidence FROM items WHERE item_id = ?", (key,)).fetchone()
    if existing is not None and existing[0] != encoded_evidence:
        raise ValueError(f"Conflicting original rows for evidence_hash {key}")
    sources = list(item.get("sources", []))
    if "source" in item:
        sources.append(item["source"])
    if not sources or any(not isinstance(source, dict) or not isinstance(source.get("benchmark"), str)
                          or not source["benchmark"].strip() for source in sources):
        raise ValueError("Every benchmark item requires source provenance with a benchmark identifier")
    if existing is None:
        # Keep the original row unchanged; source/benchmark context is not part
        # of row identity, searched text, or the canonical evidence payload.
        saved_evidence = {"item": row}
        cursor = connection.execute(
            "INSERT INTO items(item_id, evidence, search_text, question_text) VALUES (?, ?, ?, ?)",
            (key, encoded_evidence, text, question_text(saved_evidence)),
        )
        connection.execute("INSERT INTO search_fts(rowid, search_text) VALUES (?, ?)", (cursor.lastrowid, text))
    connection.executemany(
        "INSERT OR IGNORE INTO sources(item_id, source_hash, source) VALUES (?, ?, ?)",
        ((key, fingerprint(source), _json(source)) for source in sources),
    )


def _build(connection, items, inventory, encoder, policy, cancelled, progress):
    _schema(connection)
    source_rows = 0
    estimated_rows = sum(table.get("row_count", 0) for table in inventory.get("tables", []))
    _report(progress, "loading", 0, estimated_rows)
    for item in items:
        _check_cancelled(cancelled)
        _add_item(connection, item)
        source_rows += 1
        if source_rows % 1024 == 0:
            connection.commit()
            _report(progress, "loading", source_rows, estimated_rows)
    expected_counts = [table.get("row_count") for table in inventory["tables"]]
    if all(type(value) is int and value >= 0 for value in expected_counts):
        if source_rows != sum(expected_counts):
            raise ValueError("Loaded benchmark row count differs from the pinned inventory")
    connection.commit()
    _report(progress, "loading", source_rows, source_rows)
    count = lambda sql: connection.execute(sql).fetchone()[0]
    stats = {
        "source_rows": source_rows,
        "total_items": count("SELECT COUNT(*) FROM items"),
        "indexed_items": count("SELECT COUNT(*) FROM items"),
        "contentless_items": 0,
        "source_references": count("SELECT COUNT(*) FROM sources"),
        "unique_documents": count("SELECT COUNT(*) FROM items"),
        "embedded_documents": 0, "cache_hit": False,
    }
    dimensions = policy["embedding"]["dimensions"]
    _report(progress, "embedding", 0, stats["unique_documents"])
    last_id = 0
    while True:
        _check_cancelled(cancelled)
        batch = connection.execute(
            "SELECT rowid, item_id, search_text FROM items WHERE rowid > ? ORDER BY rowid LIMIT ?",
            (last_id, ENCODING_BATCH_SIZE),
        ).fetchall()
        if not batch:
            break
        vectors = _encode(encoder, [text for _, _, text in batch], dimensions, cancelled)
        dimensions = vectors.shape[1]
        connection.executemany(
            "INSERT INTO vectors(item_id, vector) VALUES (?, ?)",
            ((row[1], vector.astype("<f4").tobytes()) for row, vector in zip(batch, vectors)),
        )
        connection.commit()
        last_id = batch[-1][0]
        stats["embedded_documents"] += len(batch)
        _report(progress, "embedding", stats["embedded_documents"], stats["unique_documents"])
    policy["embedding"]["dimensions"] = dimensions
    _check_cancelled(cancelled)
    connection.execute("INSERT INTO search_fts(search_fts) VALUES ('optimize')")
    connection.commit()
    return stats


class BenchmarkIndex:
    """An opened completed cache, used and closed on its creating thread.

    Each search returns the complete union of its dense and keyword lists.
    Only shortlisted records are decoded into full evidence objects in memory.
    """

    def __init__(self, path, encoder=None, *, cache_hit=True):
        self.path = Path(path)
        self._connection = sqlite3.connect(self.path.resolve().as_uri() + "?mode=ro", uri=True)
        try:
            metadata = dict(self._connection.execute("SELECT key, value FROM metadata"))
            if json.loads(metadata.get("complete", "false")) is not True:
                raise ValueError("Benchmark cache is incomplete")
            self._policy = json.loads(metadata["policy"])
            self._stats = json.loads(metadata["stats"])
            self._cache_key = json.loads(metadata["cache_key"])
        except Exception:
            self._connection.close()
            raise
        self._stats["cache_hit"] = cache_hit
        self._encoder = encoder if encoder is not None else FullRowBGEEncoder()

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
            for rank, candidate in enumerate(ordered, 1):
                _check_cancelled(cancelled)
                key = candidate["item_id"]
                evidence, text, preview = self._connection.execute(
                    "SELECT evidence, search_text, question_text FROM items WHERE item_id = ?", (key,)
                ).fetchone()
                candidate.update(rank=rank, evidence=json.loads(evidence), search_text=text, question_text=preview,
                                 sources=[json.loads(row[0]) for row in self._connection.execute(
                                     "SELECT source FROM sources WHERE item_id = ? ORDER BY source_hash", (key,))])
            self._policy["candidate_limits"] = {"dense_k": dense_k, "bm25_k": bm25_k}
            return ordered
        except sqlite3.OperationalError:
            _check_cancelled(cancelled)
            raise
        finally:
            self._connection.set_progress_handler(None, 0)


def prepare_benchmark_index(items: Iterable[dict], cache_dir=None, inventory=None,
                            encoder=None, cancelled=None, progress=None) -> BenchmarkIndex:
    """Reuse a completed cache or atomically build one from all supplied rows.

    Cache identity includes the pinned inventory, loader version, and complete
    indexing/encoding policy. A cache hit does not consume ``items``. The caller
    retains ownership of the source iterator and must close it when appropriate.
    Cancellation or failure removes the unpublished temporary database.
    """
    if not isinstance(inventory, dict) or not inventory.get("tables"):
        raise ValueError("A pinned benchmark inventory with tables is required")
    if any(not table.get("commit") for table in inventory["tables"]):
        raise ValueError("Every benchmark table must identify its pinned commit")
    _check_cancelled(cancelled)
    policy = _policy(encoder)
    cache_key = fingerprint({"inventory": inventory, "policy": policy})
    directory = Path(cache_dir) if cache_dir is not None else DEFAULT_CACHE_DIR
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    directory.chmod(0o700)
    path = directory / f"{cache_key}.sqlite3"
    if path.exists():
        index = BenchmarkIndex(path, encoder, cache_hit=True)
        if index._cache_key != cache_key:
            index.close()
            raise ValueError("Benchmark cache identity does not match the pinned inventory")
        _report(progress, "cache", index.stats["unique_documents"], index.stats["unique_documents"],
                cache_hits=index.stats["unique_documents"])
        return index
    encoder = encoder if encoder is not None else FullRowBGEEncoder()
    with tempfile.NamedTemporaryFile(prefix="building-", suffix=".sqlite3", dir=directory, delete=False) as handle:
        temporary = Path(handle.name)
    connection = None
    try:
        connection = sqlite3.connect(temporary)
        connection.set_progress_handler(lambda: int(bool(cancelled and cancelled())), 1000)
        stats = _build(connection, items, inventory, encoder, policy, cancelled, progress)
        _check_cancelled(cancelled)
        connection.executemany("INSERT INTO metadata(key, value) VALUES (?, ?)",
                               ((key, _json(value)) for key, value in {
                                   "complete": True, "policy": policy, "stats": stats, "cache_key": cache_key,
                               }.items()))
        connection.commit()
        connection.close()
        connection = None
        _check_cancelled(cancelled)
        temporary.replace(path)
        return BenchmarkIndex(path, encoder, cache_hit=False)
    except sqlite3.OperationalError:
        _check_cancelled(cancelled)
        raise
    finally:
        if connection is not None:
            connection.close()
        temporary.unlink(missing_ok=True)
        Path(str(temporary) + "-journal").unlink(missing_ok=True)
