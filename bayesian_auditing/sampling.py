"""Reproducible, branch-aware sampling of distinct evidence within a benchmark.

Scan once into a temporary index of hashes and source locations, keeping only
the requested number of best candidates in memory. Duplicate rows get one lottery
entry. The private cache contains dataset evidence only; selection never depends
on a user's deployment.
"""

from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
from tempfile import NamedTemporaryFile, TemporaryDirectory

from .data import DATA_VERSION, fingerprint, iter_items

SAMPLE_SIZE = 50
SAMPLE_SEED = 20260925
SAMPLING_VERSION = 1


def sampling_policy():
    return {"version": SAMPLING_VERSION, "method": "seeded_hash_with_branch_coverage",
            "seed": SAMPLE_SEED, "items_per_benchmark": SAMPLE_SIZE}


def sample_upper_bound(inventory):
    counts = {}
    for table in inventory["tables"]:
        name = table["benchmark"]
        counts[name] = counts.get(name, 0) + table["row_count"]
    return sum(min(SAMPLE_SIZE, count) for count in counts.values())


def _priority(seed, benchmark, evidence_hash):
    return hashlib.sha256(f"{seed}:{benchmark}:{evidence_hash}".encode()).hexdigest()


def select_benchmark(inventory, *, token=None, streaming=True, size=SAMPLE_SIZE,
                     seed=SAMPLE_SEED, progress=None, cancelled=None):
    """Return at most `size` items, including all source references for each.

    Reserve one randomly chosen branch-exclusive item per branch when available;
    otherwise reserve one shared item from that branch. Fill remaining places by
    seeded hash priority across the combined distinct pool. This ensures branch
    coverage but is intentionally not a uniform sample of the entire catalog.
    """
    benchmarks = {t["benchmark"] for t in inventory["tables"]}
    branches = sorted({t["branch"] for t in inventory["tables"]})
    if len(benchmarks) != 1 or size < len(branches):
        raise ValueError("Sample one benchmark at a time, with room for each branch")
    benchmark = next(iter(benchmarks))

    def check_cancelled():
        if cancelled and cancelled.is_set():
            raise InterruptedError("Sample preparation cancelled")

    with TemporaryDirectory(prefix="item-sample-index-") as directory, closing(
        sqlite3.connect(str(Path(directory) / "index.sqlite"))
    ) as index:
        index.executescript("""
            CREATE TABLE items (hash TEXT PRIMARY KEY, priority TEXT NOT NULL);
            CREATE TABLE sources (hash TEXT, branch TEXT, path TEXT, row INTEGER, source TEXT);
        """)
        count = 0
        candidates, worst = {}, None
        with closing(iter_items(inventory, token=token, streaming=streaming)) as rows:
            for item in rows:
                check_cancelled()
                key, source = item["evidence_hash"], item["source"]
                priority = _priority(seed, benchmark, key)
                index.execute("INSERT OR IGNORE INTO items VALUES (?, ?)",
                              (key, priority))
                index.execute("INSERT INTO sources VALUES (?, ?, ?, ?, ?)",
                              (key, source["branch"], source["items_path"], source["row"], json.dumps(source)))
                # Keep only the lowest priorities. Once evicted, a duplicate
                # cannot re-enter: the threshold only decreases during the scan.
                if key not in candidates and (len(candidates) < size or (priority, key) < worst):
                    if len(candidates) == size:
                        del candidates[worst[1]]
                    candidates[key] = (priority, item["evidence"])
                    worst = max((entry[0], candidate) for candidate, entry in candidates.items())
                count += 1
                if count % 1000 == 0:
                    index.commit()
                    if progress:
                        progress(count)
        index.commit()
        if progress:
            progress(count)
        check_cancelled()
        index.executescript("""
            CREATE INDEX priority ON items(priority, hash);
            CREATE INDEX provenance ON sources(hash, branch);
            CREATE TEMP TABLE membership AS
                SELECT hash, COUNT(DISTINCT branch) AS branches FROM sources GROUP BY hash;
            CREATE INDEX membership_hash ON membership(hash);
        """)
        selected = []
        for branch in branches:
            winner = index.execute("""
                SELECT items.hash FROM items JOIN membership USING(hash)
                WHERE EXISTS (SELECT 1 FROM sources WHERE sources.hash = items.hash AND branch = ?)
                ORDER BY membership.branches = 1 DESC, priority, items.hash LIMIT 1
            """, (branch,)).fetchone()
            if winner and winner[0] not in selected:
                selected.append(winner[0])
        for (key,) in index.execute("SELECT hash FROM items ORDER BY priority, hash LIMIT ?", (size,)):
            if len(selected) == size:
                break
            if key not in selected:
                selected.append(key)

        sources, locations = {}, {}
        evidence = {key: candidates[key][1] for key in selected if key in candidates}
        for key in selected:
            provenance = index.execute(
                "SELECT branch, path, row, source FROM sources WHERE hash = ? ORDER BY branch, path, row", (key,)
            ).fetchall()
            sources[key] = [json.loads(row[3]) for row in provenance]
            if key not in evidence:
                # Only a reserved branch representative can lie outside the
                # candidates retained in the first pass.
                branch, path, row, _ = provenance[0]
                locations.setdefault((branch, path), []).append(row)
        with closing(iter_items(inventory, token=token, streaming=streaming, selected_rows=locations)) as rows:
            for item in rows:
                check_cancelled()
                evidence[item["evidence_hash"]] = item["evidence"]
        if set(evidence) != set(selected):
            raise ValueError("Selected evidence did not match its pinned source")
        return {"benchmark": benchmark, "source_rows": count,
                "distinct_items": index.execute("SELECT COUNT(*) FROM items").fetchone()[0],
                "items": [{"evidence_hash": key, "evidence": evidence[key], "sources": sources[key]}
                          for key in selected]}


def prepare_samples(inventory, cache_directory, *, token=None, progress=None, cancelled=None):
    """Prepare every benchmark before paid calls; publish cache files atomically.

    Returns cache paths and the exact number of distinct selected inputs. The
    cache key includes pinned tables, seed, sample size, and loader/policy versions.
    """
    directory = Path(cache_directory)
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    directory.chmod(0o700)
    paths, hashes, rows_done = [], set(), 0
    for number, benchmark in enumerate(sorted({t["benchmark"] for t in inventory["tables"]})):
        if cancelled and cancelled.is_set():
            raise InterruptedError("Sample preparation cancelled")
        subset = {**inventory, "tables": sorted(
            [t for t in inventory["tables"] if t["benchmark"] == benchmark],
            key=lambda t: (t["branch"], t["items_path"]))}
        cache_key = fingerprint({"inventory": subset, "data_version": DATA_VERSION, "sampling": sampling_policy()})
        path = directory / f"{cache_key}.json"
        if progress:
            progress(benchmark, number, rows_done)
        if path.exists():
            sample = json.loads(path.read_text())
        else:
            sample = select_benchmark(subset, token=token, cancelled=cancelled, size=SAMPLE_SIZE, seed=SAMPLE_SEED,
                progress=lambda count: progress(benchmark, number, rows_done + count) if progress else None)
            with NamedTemporaryFile(mode="w", dir=directory, suffix=".tmp", delete=False) as output:
                temporary = Path(output.name)
                try:
                    json.dump(sample, output, ensure_ascii=False)
                    output.close()
                    temporary.replace(path)
                finally:
                    temporary.unlink(missing_ok=True)
        if (sample["benchmark"] != benchmark or len(sample["items"]) > SAMPLE_SIZE
                or len({item["evidence_hash"] for item in sample["items"]}) != len(sample["items"])):
            raise ValueError("Invalid cached benchmark sample")
        paths.append(path)
        hashes.update(item["evidence_hash"] for item in sample["items"])
        rows_done += sample["source_rows"]
        if progress:
            progress(benchmark, number + 1, rows_done)
    return paths, len(hashes)


def iter_sample_items(paths):
    for path in paths:
        yield from json.loads(Path(path).read_text())["items"]
