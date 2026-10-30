"""Small, read-only views of the original retrieval records in public examples.

The importer writes one SQLite file incrementally. Large evidence fields shared
by task rankings are stored once, while each occurrence keeps its own metadata.
Requests read one page of summaries or one exact saved candidate.
"""

from contextlib import closing
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3

from .construction_item_preview import item_preview


FILENAME = "retrieval.sqlite3"
EVIDENCE_FIELDS = ("evidence", "question_text", "search_text")
RANK_FIELDS = ("item_id", "rank", "dense_rank", "bm25_rank", "dense_score", "bm25_score", "rrf_score")
SCHEMA = """
CREATE TABLE metadata (key TEXT PRIMARY KEY, value INTEGER NOT NULL);
CREATE TABLE payloads (digest TEXT PRIMARY KEY, data BLOB NOT NULL);
CREATE TABLE rankings (position INTEGER PRIMARY KEY, facet_id TEXT NOT NULL UNIQUE);
CREATE TABLE candidates (
    ranking INTEGER NOT NULL, item_id TEXT NOT NULL, position INTEGER NOT NULL,
    payload_digest TEXT NOT NULL, metadata TEXT NOT NULL, summary TEXT NOT NULL,
    PRIMARY KEY (ranking, item_id), UNIQUE (ranking, position)
);
CREATE TABLE queues (
    queue_id TEXT PRIMARY KEY, position INTEGER NOT NULL UNIQUE,
    ranking INTEGER NOT NULL, facet_id TEXT NOT NULL, source TEXT, item_count INTEGER NOT NULL
);
CREATE TABLE queue_items (
    queue_id TEXT NOT NULL, position INTEGER NOT NULL, item_id TEXT NOT NULL,
    PRIMARY KEY (queue_id, position), UNIQUE (queue_id, item_id)
);
"""


class RetrievalNotFound(LookupError):
    """The requested queue or membership is absent from a saved example."""


def _json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False)


def _require(condition, message):
    if not condition:
        raise ValueError(message)


class Builder:
    """Keep one candidate in memory as the streaming importer visits its row."""

    def __init__(self, path: Path):
        _require(not path.exists(), "Derived retrieval data already exists")
        self.database = sqlite3.connect(path)
        self.database.executescript(SCHEMA)

    def close(self):
        self.database.close()

    def add(self, ranking: int, position: int, record: dict):
        # Importing source-table dependencies is only needed during publication.
        from bayesian_auditing.benchmark_data import row_fingerprint

        item_id = record.get("item_id")
        row = (record.get("evidence") or {}).get("item")
        _require(isinstance(item_id, str) and item_id and isinstance(row, dict)
                 and row_fingerprint(row) == item_id == record.get("evidence_hash"),
                 "A retrieved item does not retain its original row identity")
        payload = _json({key: record[key] for key in EVIDENCE_FIELDS if key in record}).encode("utf-8")
        digest = hashlib.sha256(payload).hexdigest()
        self.database.execute("INSERT OR IGNORE INTO payloads VALUES (?, ?)",
                              (digest, gzip.compress(payload, mtime=0)))
        summary = {**{key: record.get(key) for key in RANK_FIELDS}, **item_preview(record),
                   "sources": sorted({source["benchmark"] for source in record.get("sources", [])
                                      if source.get("benchmark")})}
        metadata = {key: value for key, value in record.items() if key not in EVIDENCE_FIELDS}
        try:
            self.database.execute("INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?)",
                                  (ranking, item_id, position, digest, _json(metadata), _json(summary)))
        except sqlite3.IntegrityError:
            raise ValueError("Retrieved item IDs and positions must be unique within each task ranking") from None

    def finish(self, retrieval: dict | None):
        retrieval = retrieval or {}
        facets = {}
        try:
            for position, ranking in enumerate(retrieval.get("rankings", [])):
                facet_id = ranking.get("facet_id")
                _require(isinstance(facet_id, str) and facet_id and facet_id not in facets,
                         "Retrieval task rankings must have unique nonempty facet IDs")
                facets[facet_id] = position
                self.database.execute("INSERT INTO rankings VALUES (?, ?)", (position, facet_id))
                count = self.database.execute("SELECT count(*) FROM candidates WHERE ranking = ?", (position,)).fetchone()[0]
                _require(count == len(ranking["candidates"]), "A retrieval ranking differs from its saved candidates")
            seen_queues = set()
            for position, queue in enumerate(retrieval.get("queues", [])):
                queue_id, facet_id, source = queue.get("queue_id"), queue.get("facet_id"), queue.get("source")
                identifiers = queue.get("item_ids")
                _require(isinstance(queue_id, str) and queue_id and queue_id not in seen_queues,
                         "Retrieval queues must have unique nonempty IDs")
                seen_queues.add(queue_id)
                _require(facet_id in facets and (source is None or isinstance(source, str)), "A retrieval queue has an invalid task or source")
                _require(isinstance(identifiers, list) and all(isinstance(key, str) for key in identifiers)
                         and len(set(identifiers)) == len(identifiers), "Retrieval queue item IDs must be unique")
                ranking = facets[facet_id]
                self.database.execute("INSERT INTO queues VALUES (?, ?, ?, ?, ?, ?)",
                                      (queue_id, position, ranking, facet_id, source, len(identifiers)))
                for index, item_id in enumerate(identifiers, 1):
                    candidate = self.database.execute("SELECT summary FROM candidates WHERE ranking = ? AND item_id = ?",
                                                      (ranking, item_id)).fetchone()
                    _require(candidate is not None, "A retrieval queue references an item outside its task ranking")
                    _require(source is None or source in json.loads(candidate[0])["sources"],
                             "A retrieval queue source differs from its item provenance")
                    self.database.execute("INSERT INTO queue_items VALUES (?, ?, ?)", (queue_id, index, item_id))
                if source is None:
                    ranked = [row[0] for row in self.database.execute(
                        "SELECT item_id FROM candidates WHERE ranking = ? ORDER BY position", (ranking,))]
                    _require(identifiers == ranked, "A task queue differs from its saved ranking order")
            unique = self.database.execute("SELECT count(DISTINCT item_id) FROM candidates").fetchone()[0]
            self.database.executemany("INSERT INTO metadata VALUES (?, ?)", [("schema_version", 1), ("unique_candidate_count", unique)])
            self.database.commit()
        except sqlite3.IntegrityError:
            raise ValueError("The saved retrieval data is inconsistent") from None


def _open(path):
    database = sqlite3.connect(path.resolve().as_uri() + "?mode=ro&immutable=1", uri=True)
    try:
        database.row_factory = sqlite3.Row
        database.execute("PRAGMA cache_size = -1024")
        database.execute("PRAGMA query_only = ON")
        version = database.execute("SELECT value FROM metadata WHERE key = 'schema_version'").fetchone()
        _require(version is not None and version[0] == 1, "Unsupported retrieval view version")
    except BaseException:
        database.close()
        raise
    return database


def _queue(database, queue_id):
    row = (database.execute("SELECT * FROM queues ORDER BY position LIMIT 1").fetchone() if queue_id is None else
           database.execute("SELECT * FROM queues WHERE queue_id = ?", (queue_id,)).fetchone())
    if row is None:
        raise RetrievalNotFound("Saved retrieval queue not found.")
    return row


def page(path: Path, queue_id: str | None, number: int, size: int) -> dict:
    with closing(_open(path)) as database:
        queue = _queue(database, queue_id)
        rows = database.execute("""
            SELECT candidate.summary, membership.position
            FROM queue_items AS membership
            JOIN candidates AS candidate ON candidate.item_id = membership.item_id AND candidate.ranking = ?
            WHERE membership.queue_id = ? ORDER BY membership.position LIMIT ? OFFSET ?
        """, (queue["ranking"], queue["queue_id"], size, (number - 1) * size)).fetchall()
        unique = database.execute("SELECT value FROM metadata WHERE key = 'unique_candidate_count'").fetchone()[0]
        return {"queue_id": queue["queue_id"], "facet_id": queue["facet_id"], "source": queue["source"],
                "page": number, "page_size": size, "total": queue["item_count"],
                "total_pages": max(1, (queue["item_count"] + size - 1) // size), "unique_candidate_count": unique,
                "items": [{**json.loads(row["summary"]), "queue_rank": row["position"]} for row in rows]}


def item(path: Path, queue_id: str | None, item_id: str) -> dict:
    with closing(_open(path)) as database:
        queue = _queue(database, queue_id)
        row = database.execute("""
            SELECT candidate.metadata, payload.data
            FROM queue_items AS membership
            JOIN candidates AS candidate ON candidate.item_id = membership.item_id AND candidate.ranking = ?
            JOIN payloads AS payload ON payload.digest = candidate.payload_digest
            WHERE membership.queue_id = ? AND membership.item_id = ?
        """, (queue["ranking"], queue["queue_id"], item_id)).fetchone()
        if row is None:
            raise RetrievalNotFound("Saved retrieval item not found in this queue.")
        return {**json.loads(row["metadata"]), **json.loads(gzip.decompress(row["data"]))}
