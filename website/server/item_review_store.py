"""Private temporary results with indexed deduplication and ranking.

Each run owns a SQLite file in a private temporary directory. API keys and
deployment answers are never written here. Expiration and shutdown remove the
store; it does not support durable resume after a server restart.
"""

from collections import Counter
import json
import sqlite3
from tempfile import TemporaryDirectory
from threading import RLock


class ReviewStore:
    def __init__(self):
        self.directory = TemporaryDirectory(prefix="item-review-")
        self.connection = sqlite3.connect(f"{self.directory.name}/results.sqlite", check_same_thread=False)
        self.lock = RLock()
        self.counts = Counter()
        self.needs_review = 0
        self.unranked = 0
        self.connection.executescript("""
            CREATE TABLE items (
                id INTEGER PRIMARY KEY, evidence_hash TEXT UNIQUE NOT NULL,
                status TEXT NOT NULL, score REAL, record TEXT NOT NULL
            );
            CREATE INDEX ranking ON items(status, score DESC, evidence_hash);
            CREATE TABLE sources (evidence_hash TEXT NOT NULL, source TEXT NOT NULL);
            CREATE INDEX source_lookup ON sources(evidence_hash);
        """)

    @property
    def processed(self):
        return sum(self.counts.values())

    @property
    def ranked(self):
        return self.counts["complete"] - self.unranked

    def add_source(self, evidence_hash, source):
        with self.lock, self.connection:
            self.connection.execute("INSERT INTO sources VALUES (?, ?)", (evidence_hash, json.dumps(source)))

    def contains(self, evidence_hash):
        with self.lock:
            return self.connection.execute("SELECT 1 FROM items WHERE evidence_hash = ?", (evidence_hash,)).fetchone() is not None

    def append(self, record):
        record = dict(record)
        for source in record.pop("sources", []):
            self.add_source(record["evidence_hash"], source)
        with self.lock, self.connection:
            self.connection.execute("INSERT INTO items(evidence_hash, status, score, record) VALUES (?, ?, ?, ?)",
                                    (record["evidence_hash"], record["status"], record.get("overall_score"), json.dumps(record)))
            self.counts[record["status"]] += 1
            self.needs_review += bool(record.get("needs_review"))
            self.unranked += record["status"] == "complete" and record.get("overall_score") is None

    def records(self, status, *, offset=0, limit=None, cutoff=None, scored=None):
        """Read a page or stream every result; never load the whole ranking."""
        cutoff = self.processed if cutoff is None else cutoff
        score_filter = "" if scored is None else ("AND score IS NOT NULL " if scored else "AND score IS NULL ")
        with self.lock:
            cursor = self.connection.execute(
                "SELECT evidence_hash, record FROM items WHERE status = ? AND id <= ? "
                + score_filter + "ORDER BY score DESC, evidence_hash LIMIT ? OFFSET ?",
                (status, cutoff, -1 if limit is None else limit, offset),
            )
        try:
            rank = offset
            while True:
                with self.lock:
                    row = cursor.fetchone()
                    if row is None:
                        return
                    sources = self.connection.execute("SELECT source FROM sources WHERE evidence_hash = ? ORDER BY rowid", (row[0],)).fetchall()
                record = json.loads(row[1])
                record["sources"] = [json.loads(source[0]) for source in sources]
                if status == "complete" and record.get("overall_score") is not None:
                    rank += 1
                    record["rank"] = rank
                yield record
        finally:
            with self.lock:
                cursor.close()

    def close(self):
        with self.lock:
            self.connection.close()
            self.directory.cleanup()
