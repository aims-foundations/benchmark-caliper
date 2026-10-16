"""Metadata-only Data Bank discovery and confirmed, immutable item snapshots.

Search never calls a model or reads item values. The bundled repository
index makes setup immediate; a daemon refreshes metadata from main in the
background. Every match is only a candidate and requires caller confirmation.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timezone
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
from threading import Lock, Thread
import time
import unicodedata
from urllib.parse import unquote, urlsplit

from huggingface_hub import HfApi, HfFileSystem, get_token, hf_hub_download
import pyarrow.parquet as pq
import yaml

from anthropic_api_package_release.item_analysis import data
from anthropic_api_package_release.item_analysis.storage import write_json
from . import db

REPO = "aims-foundations/measurement-db-pp"
# The index now includes every release label. Reject earlier filtered caches
# even when the repository revision has not changed.
CATALOG_VERSION = 2
BUNDLED_CATALOG = Path(__file__).with_name("item_analysis_databank_catalog.json")
REFRESH_SECONDS = 3600
MAX_TABLE_BYTES = 32 * 1024 * 1024
MAX_UNCOMPRESSED_BYTES = 96 * 1024 * 1024
MAX_ITEMS = 50_000
MAX_METADATA_BYTES = 8 * 1024 * 1024
_REVISION = re.compile(r"^[0-9a-f]{40}$")
_SLUG = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,150}$")
_lock = Lock()
_preparation_lock = Lock()
_catalogs: dict[str, dict] = {}
_latest: str | None = None
_last_refresh = 0.0
_refreshing = False
_refresh_failed = False


class DataBankError(ValueError):
    """Only fixed, credential-free messages may leave the discovery adapter."""


def _normal(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower())


def _strings(value) -> list[str]:
    if isinstance(value, str):
        return [value] if value.strip() else []
    return [str(v) for v in value if isinstance(v, (str, int)) and str(v).strip()] if isinstance(value, list) else []


def canonical_identifier(value: str) -> str | None:
    """Canonical paper IDs and source URLs; URL arguments never reach a loader."""
    value = unquote(value.strip()).rstrip(".,;")
    arxiv = re.search(r"(?:arxiv(?:\.org/(?:abs|pdf|html)/|:)\s*)([a-z-]+/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?", value, re.I)
    if arxiv:
        return "arxiv:" + arxiv.group(1).lower()
    doi = re.search(r"(?:doi\.org/|doi:\s*|^)(10\.\d{4,9}/\S+)", value, re.I)
    if doi:
        return "doi:" + doi.group(1).rstrip("/.").lower()
    try:
        parsed = urlsplit(value if "://" in value else "https://" + value)
    except ValueError:
        return None
    host = (parsed.hostname or "").lower().removeprefix("www.")
    parts = [part for part in parsed.path.split("/") if part]
    if host == "github.com" and len(parts) >= 2:
        return "github:" + "/".join(parts[:2]).removesuffix(".git").lower()
    if host == "huggingface.co" and parts and parts[0] == "datasets" and len(parts) >= 3:
        return "hf:" + "/".join(parts[1:3]).lower()
    if "://" in value and host and parts:
        return "url:" + host + "/" + "/".join(parts).rstrip("/").lower()
    return None


def _safe_urls(value) -> list[str]:
    result = []
    for url in _strings(value):
        try:
            parsed = urlsplit(url)
            if parsed.scheme in {"http", "https"} and parsed.hostname and not parsed.username and not parsed.password:
                result.append(url)
        except ValueError:
            pass
    return result


def _languages(value) -> set[str]:
    aliases = {"english": "en", "eng": "en", "hindi": "hi", "hin": "hi", "chinese": "zh", "zho": "zh",
               "mandarin": "zh", "french": "fr", "fra": "fr", "spanish": "es", "spa": "es",
               "german": "de", "deu": "de", "arabic": "ar", "ara": "ar", "korean": "ko", "kor": "ko",
               "japanese": "ja", "jpn": "ja", "portuguese": "pt", "por": "pt"}
    result = set()
    for language in _strings(value):
        language = language.strip().lower()
        canonical = aliases.get(language, language.split("-")[0] if re.fullmatch(r"[a-z]{2}(?:-[a-z0-9]+)?", language) else None)
        if canonical:
            result.add(canonical)
    return result


def _identity(assessment: dict) -> dict:
    identity = assessment.get("benchmark_identity") or {}
    names = _strings(identity.get("name")) + _strings(identity.get("full_name")) + _strings(identity.get("aliases"))
    names += _strings(assessment.get("benchmark")) + _strings(assessment.get("benchmark_name"))
    urls = _strings(identity.get("paper_urls")) + _strings(identity.get("source_urls"))
    return {"names": sorted(set(names)), "identifiers": {v for u in urls if (v := canonical_identifier(u))},
            "version": identity.get("version"), "languages": _strings(identity.get("languages"))}


def _variant(name: str) -> set[str]:
    words = re.findall(r"[a-z]+|\d+", name.lower())
    found = set(words).intersection({"pro", "lite", "mini", "plus", "hard", "easy", "multilingual"})
    found.update(re.findall(r"\bv\d+\b", name.lower()))
    # Common compact names preserve meaningful suffixes (MMLU-Pro vs MMLU).
    compact = _normal(name)
    for marker in ("pro", "lite", "mini", "plus"):
        if len(compact) > len(marker) + 2 and compact.endswith(marker):
            found.add(marker)
    return found


def _rank(entry: dict, identity: dict, query: str | None) -> tuple[float, list[str], list[str], str]:
    names = [entry["benchmark"], entry["title"], *entry.get("aliases", [])]
    normalized = {_normal(n) for n in names if n}
    targets = {_normal(n) for n in identity["names"] if n}
    identifiers = set(entry.get("identifiers", []))
    shared = identifiers.intersection(identity["identifiers"])
    reasons, conflicts, score, kind = [], [], 0.0, "related_name"
    if shared:
        score, kind = 100.0, "identifier"
        reasons.append("Matching paper or source identifier: " + sorted(shared)[0])
    if targets.intersection(normalized):
        score, kind = max(score, 90.0), "identifier" if shared else "exact_name"
        reasons.append("Benchmark name or alias matches the assessment.")
    elif targets:
        similar = max((SequenceMatcher(None, a, b).ratio() for a in targets for b in normalized), default=0)
        if similar >= .72 and any(len(a) >= 4 for a in targets):
            score = max(score, 40 + similar * 20)
            reasons.append("Similar benchmark name; verify that this is the intended benchmark.")
    if score and kind == "related_name":
        conflicts.append("The benchmark name differs; this may be a related variant rather than the assessed benchmark.")
    source_variants = _variant(entry["benchmark"]) | _variant(entry["title"])
    expected_variants = set().union(*(_variant(n) for n in identity["names"])) if identity["names"] else set()
    if source_variants != expected_variants and (score or query):
        conflicts.append("Variant differs: assessment " + (", ".join(sorted(expected_variants)) or "base/unspecified")
                         + "; dataset " + (", ".join(sorted(source_variants)) or "base/unspecified") + ".")
    version = identity.get("version")
    if version and entry.get("version") and _normal(str(version)) != _normal(entry["version"]):
        conflicts.append(f"Release differs: assessment {version}; dataset {entry['version']}.")
    paper_ids = {v for v in identity["identifiers"] if v.startswith(("arxiv:", "doi:"))}
    source_papers = {v for v in identifiers if v.startswith(("arxiv:", "doi:"))}
    # Only compare like identifier schemes: a DOI and arXiv ID may name one paper.
    for scheme in ("arxiv:", "doi:"):
        a, b = {v for v in paper_ids if v.startswith(scheme)}, {v for v in source_papers if v.startswith(scheme)}
        if a and b and a.isdisjoint(b):
            conflicts.append("The documented paper identifier differs from the assessment's paper.")
    requested_languages, source_languages = _languages(identity["languages"]), _languages(entry.get("languages"))
    if requested_languages and source_languages and requested_languages.isdisjoint(source_languages):
        conflicts.append("Documented language differs: assessment " + ", ".join(sorted(requested_languages))
                         + "; dataset " + ", ".join(sorted(source_languages)) + ".")
    if query is not None:
        q = query.strip()[:300]
        qnorm = _normal(q)
        qid = canonical_identifier(q)
        searchable = normalized | {_normal(u) for u in entry.get("paper_urls", []) + entry.get("source_urls", [])}
        exact = qnorm in normalized or (qid and qid in identifiers)
        partial = len(qnorm) >= 2 and any(qnorm in n for n in searchable)
        similar = max((SequenceMatcher(None, qnorm, n).ratio() for n in normalized), default=0)
        if not qnorm or not (exact or partial or (len(qnorm) >= 4 and similar >= .6)):
            return 0, [], [], "search"
        score = (120 if exact else 100 if partial else 70 * similar) + min(score, 100) / 100
        reasons.insert(0, "Matches your Data Bank search." if exact or partial else "Similar to your Data Bank search.")
        kind = "search"
        if not targets.intersection(normalized) and not shared:
            conflicts.append("This search result has not been verified as the benchmark in the assessment.")
    return score, reasons, conflicts, kind


def _cache_dir() -> Path:
    return db.DEFAULT_DB_PATH.parent / "item-analysis-databank"


def _valid_catalog(value: dict) -> bool:
    return (isinstance(value, dict) and value.get("version") == CATALOG_VERSION
            and value.get("repo") == REPO and bool(_REVISION.fullmatch(str(value.get("revision", ""))))
            and isinstance(value.get("entries"), list))


def _load_catalog() -> dict | None:
    global _latest
    with _lock:
        if _latest in _catalogs:
            return _catalogs[_latest]
        for path in (_cache_dir() / "latest.json", BUNDLED_CATALOG):
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
                if _valid_catalog(value):
                    _catalogs[value["revision"]] = value
                    _latest = value["revision"]
                    return value
            except (OSError, ValueError):
                pass
    return None


def _refresh_worker() -> None:
    global _latest, _refreshing, _refresh_failed
    try:
        catalog = refresh_catalog(skip_if_unchanged=True)
        directory = _cache_dir()
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        for name in (catalog["revision"] + ".json", "latest.json"):
            temporary = directory / (name + ".tmp")
            temporary.write_text(json.dumps(catalog, ensure_ascii=False), encoding="utf-8")
            temporary.replace(directory / name)
        with _lock:
            _catalogs[catalog["revision"]] = catalog
            _latest, _refresh_failed = catalog["revision"], False
    except Exception:
        # Never log provider exception bodies, paths, or credentials.
        with _lock:
            _refresh_failed = True
    finally:
        with _lock:
            _refreshing = False


def _schedule_refresh() -> None:
    global _refreshing, _last_refresh
    with _lock:
        if _refreshing or (time.monotonic() - _last_refresh < REFRESH_SECONDS):
            return
        _refreshing, _last_refresh = True, time.monotonic()
    Thread(target=_refresh_worker, daemon=True, name="databank-metadata-refresh").start()


def search_candidates(assessment: dict, query: str | None = None) -> dict:
    """Return explainable candidates promptly; none is selected or confirmed."""
    query = query.strip() if query and query.strip() else None
    catalog = _load_catalog()
    _schedule_refresh()
    if catalog is None:
        return {"candidates": [], "status": "unavailable", "repo": REPO, "revision": None,
                "message": "Data Bank metadata is unavailable. Retry later or upload the benchmark items.",
                "requires_confirmation": True}
    identity = _identity(assessment)
    has_access = bool(get_token())
    found = []
    for entry in catalog["entries"]:
        score, reasons, conflicts, kind = _rank(entry, identity, query)
        if score <= 0:
            continue
        candidate = deepcopy(entry)
        # Schema eligibility never claims a gated table can be read without access.
        if candidate["available"] and not has_access:
            candidate["available"] = False
            candidate["unavailable_reason"] = "Server-side Data Bank access is unavailable. Upload matching items or contact the maintainer."
        candidate.update(match_reasons=reasons, conflicts=conflicts, match_type=kind, requires_confirmation=True)
        found.append((score, candidate))
    found.sort(key=lambda pair: (-pair[0], pair[1]["title"].lower()))
    failed = _refresh_failed
    return {"candidates": [candidate for _, candidate in found[:30]], "status": "cached" if failed else "ready",
            "repo": REPO, "revision": catalog["revision"], "requires_confirmation": True,
            "message": "Using the last verified metadata catalog because refresh was unavailable." if failed else
                       "Review and confirm the benchmark identity, release, and item scope before continuing."}


def resolve_candidate(candidate_id: str) -> dict:
    """Resolve only a candidate from a catalog actually served by this server."""
    match = re.fullmatch(r"databank:([0-9a-f]{40}):([a-zA-Z0-9][a-zA-Z0-9_.-]{0,150})", candidate_id)
    if not match:
        raise DataBankError("This dataset selection is invalid. Search again and confirm a candidate.")
    revision, _ = match.groups()
    _load_catalog()
    catalog = _catalogs.get(revision)
    if catalog is None:
        try:
            value = json.loads((_cache_dir() / f"{revision}.json").read_text(encoding="utf-8"))
            if _valid_catalog(value) and value["revision"] == revision:
                catalog = value
        except (OSError, ValueError):
            pass
    if catalog:
        for entry in catalog["entries"]:
            if entry["id"] == candidate_id:
                return deepcopy(entry)
    raise DataBankError("This dataset selection has expired. Search again and confirm its current revision.")


def _metadata_file(path: str, revision: str, token, *, download=hf_hub_download) -> Path:
    return Path(download(repo_id=REPO, filename=path, repo_type="dataset", revision=revision,
                         token=token, etag_timeout=10))


def _inspect_footer(path: str, revision: str, token) -> dict:
    filesystem = HfFileSystem(token=token)
    with filesystem.open(f"datasets/{REPO}@{revision}/{path}", "rb", block_size=65536, cache_type="readahead") as stream:
        with pq.ParquetFile(stream) as parquet:
            return {"item_count": parquet.metadata.num_rows, "columns": parquet.schema_arrow.names,
                    "uncompressed_bytes": sum(parquet.metadata.row_group(i).total_byte_size
                                              for i in range(parquet.metadata.num_row_groups))}


def _build_entry(slug: str, revision: str, api, token) -> dict | None:
    files = {entry.path: entry for entry in api.list_repo_tree(REPO, repo_type="dataset", revision=revision, path_in_repo=slug)}
    meta_path = f"{slug}/metadata.yaml"
    metadata = {}
    if meta_path in files:
        if getattr(files[meta_path], "size", MAX_METADATA_BYTES + 1) > MAX_METADATA_BYTES:
            return None
        metadata = yaml.safe_load(_metadata_file(meta_path, revision, token).read_text(encoding="utf-8")) or {}
    declared = metadata.get("benchmark", {}) if isinstance(metadata, dict) else {}
    if not isinstance(declared, dict):
        return None
    for directory in (f"{slug}/formatted_tables",):
        if directory in files:
            files.update({entry.path: entry for entry in api.list_repo_tree(REPO, repo_type="dataset", revision=revision, path_in_repo=directory)})
    # The processed bank publishes its current tables directly under each slug.
    # Older collections may still use formatted_tables. Read identity metadata
    # alongside the selected item table; metadata.yaml is optional in this bank.
    table_path = next((p for p in (f"{slug}/items.parquet", f"{slug}/formatted_tables/items.parquet") if p in files), None)
    parent = str(Path(table_path).parent) if table_path else slug
    benchmark_path = f"{parent}/benchmarks.parquet"
    rows = []
    if benchmark_path in files and getattr(files[benchmark_path], "size", MAX_METADATA_BYTES + 1) <= MAX_METADATA_BYTES:
        rows = pq.read_table(_metadata_file(benchmark_path, revision, token)).to_pylist()
    # The release label is descriptive metadata, not a search or access policy.
    # Search the repository regardless of that label; HF enforces file access.
    benchmark = {**(rows[0] if rows else {}), **declared}
    character_path = f"{slug}/characterization.yaml"
    characterization = {}
    if character_path in files and getattr(files[character_path], "size", MAX_METADATA_BYTES + 1) <= MAX_METADATA_BYTES:
        characterization = yaml.safe_load(_metadata_file(character_path, revision, token).read_text(encoding="utf-8")) or {}
    count = characterization.get("tables", {}).get("items", {}).get("rows", 0)
    count = count if isinstance(count, int) and count >= 0 else 0
    table = files.get(table_path)
    size = getattr(table, "size", 0)
    lfs = getattr(table, "lfs", None)
    sha256 = getattr(lfs, "sha256", None) if lfs is not None else None
    aliases = sorted(set(_strings(benchmark.get("aliases")) + [str(row["name"]) for row in rows if row.get("name")]))
    ids = sorted({str(row["benchmark_id"]) for row in rows if row.get("benchmark_id") is not None})
    paper_urls = sorted(set(_safe_urls(benchmark.get("paper_url"))
                            + [url for row in rows for url in _safe_urls(row.get("paper_url"))]))
    source_urls = sorted({url for record in [benchmark, *rows]
                          for key in ("data_source_url", "source_url", "dataset_source")
                          for url in _safe_urls(record.get(key))})
    title = str(benchmark.get("name") or slug)
    version = benchmark.get("version")
    modality = sorted(set(_strings(benchmark.get("modality"))
                          + [value for row in rows for value in _strings(row.get("modality"))]))
    features = benchmark.get("benchmark_features") or {}
    if isinstance(features, str):
        try:
            features = json.loads(features)
        except ValueError:
            features = {}
    languages = _strings(benchmark.get("languages")) + _strings(benchmark.get("language"))
    if isinstance(features, dict):
        languages += _strings(features.get("languages")) + _strings(features.get("language"))
    reasons = []
    granularity = benchmark.get("granularity") or (rows[0].get("granularity") if rows else None)
    if granularity != "item" or any(row.get("granularity", granularity) != "item" for row in rows):
        reasons.append("This release is not verified as individual benchmark items.")
    if not table_path:
        reasons.append("No formatted item table is published for this release.")
    if not ids:
        reasons.append("The benchmark identity mapping is unavailable.")
    opaque = re.compile(r"(?:[a-fA-F0-9]{16,64}|[a-fA-F0-9]{8}(?:-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}|[0-9]+)")
    if any(value != slug and not opaque.fullmatch(value) for value in ids):
        reasons.append("This release uses named configurations requiring a dedicated item adapter.")
    if not sha256 or not re.fullmatch(r"[0-9a-f]{64}", sha256):
        reasons.append("The published item checksum is unavailable.")
    if any(m.lower() not in {"text", "code"} for m in modality) or not modality:
        reasons.append("This item analysis supports text evidence; this release requires other media or has unspecified modality.")
    if size > MAX_TABLE_BYTES:
        reasons.append("The full item table exceeds this service's 32 MiB download limit.")
    if count > MAX_ITEMS:
        reasons.append("The full snapshot exceeds this service's 50,000-item limit.")
    footer = {}
    if table_path and size <= MAX_TABLE_BYTES and count <= MAX_ITEMS:
        footer = _inspect_footer(table_path, revision, token)
        if count and count != footer["item_count"]:
            reasons.append("Published item counts disagree; the snapshot requires maintainer review.")
        count = footer["item_count"]
        if not {"item_id", "benchmark_id", "content"}.issubset(footer["columns"]):
            reasons.append("The formatted item table lacks required identity or content columns.")
        if footer["uncompressed_bytes"] > MAX_UNCOMPRESSED_BYTES:
            reasons.append("The full snapshot exceeds this service's 96 MiB decoded-data limit.")
        if count > MAX_ITEMS:
            reasons.append("The full snapshot exceeds this service's 50,000-item limit.")
    if not count:
        reasons.append("This release has no verified nonempty item population.")
    source_url = f"https://huggingface.co/datasets/{REPO}/blob/{revision}/{table_path or meta_path}"
    return {"id": f"databank:{revision}:{slug}", "benchmark": slug, "title": title, "aliases": aliases,
            "repo": REPO, "revision": revision, "source_revision": revision, "table_path": table_path,
            "sha256": sha256, "table_bytes": size, "item_count": count, "benchmark_ids": ids,
            "columns": footer.get("columns", []), "uncompressed_bytes": footer.get("uncompressed_bytes"),
            "source_url": source_url, "source_label": f"measurement-db-pp · {slug} · {count:,} items",
            "metadata_url": f"https://huggingface.co/datasets/{REPO}/blob/{revision}/{meta_path if meta_path in files else benchmark_path}",
            "version": str(version) if version else None, "split": benchmark.get("split"),
            "testing_scope": str(benchmark.get("testing_condition") or "")[:2400] or None,
            "description": str(benchmark.get("one_line_description") or benchmark.get("description") or "")[:600],
            "paper_urls": paper_urls, "source_urls": source_urls, "modality": modality, "languages": sorted(set(languages)),
            "identifiers": sorted({v for u in paper_urls + source_urls if (v := canonical_identifier(u))}),
            "release": benchmark.get("release"), "granularity": granularity, "available": not reasons,
            "unavailable_reason": " ".join(reasons) + " Upload a supported matching snapshot to continue." if reasons else None,
            "requires_confirmation": True}


def refresh_catalog(revision: str = "main", *, api=None, skip_if_unchanged=False) -> dict:
    """Build an atomic index from repository metadata and footers, never item rows."""
    api = api or HfApi()
    try:
        # dataset_info returns a huge sibling list for this repository. Refs are
        # enough to freeze main and keep hourly checks small on the hosted service.
        resolved = revision if _REVISION.fullmatch(revision) else next(
            ref.target_commit for ref in api.list_repo_refs(REPO, repo_type="dataset").branches if ref.name == "main")
        if not _REVISION.fullmatch(resolved):
            raise ValueError("Invalid revision")
        previous = _load_catalog() if skip_if_unchanged else None
        if previous and previous["revision"] == resolved:
            return deepcopy(previous)
        token = get_token()
        roots = [entry.path for entry in api.list_repo_tree(REPO, repo_type="dataset", revision=resolved)
                 if not hasattr(entry, "size") and _SLUG.fullmatch(entry.path)]
        with ThreadPoolExecutor(max_workers=6) as pool:
            entries = list(pool.map(lambda slug: _build_entry(slug, resolved, api, token), roots))
        entries = sorted((entry for entry in entries if entry), key=lambda entry: entry["benchmark"])
        if not entries:
            raise ValueError("Empty catalog")
        return {"version": CATALOG_VERSION, "repo": REPO, "branch": "main", "revision": resolved,
                "generated_at": datetime.now(timezone.utc).isoformat(), "entries": entries}
    except Exception:
        raise DataBankError("Data Bank metadata could not be refreshed. The previous verified catalog remains available.") from None


def _prepare_candidate(directory: Path, candidate: dict, stopped=None) -> dict:
    """Prepare every item from the confirmed pinned source, without assessment."""
    def check_stopped():
        if stopped and stopped():
            raise InterruptedError("Dataset preparation stopped.")

    check_stopped()
    pinned = resolve_candidate(candidate.get("id", ""))
    if pinned != {key: candidate.get(key) for key in pinned}:
        raise DataBankError("The confirmed dataset metadata changed. Search again and confirm its revision.")
    if not pinned["available"]:
        raise DataBankError(pinned["unavailable_reason"])
    if (pinned["item_count"] > MAX_ITEMS or pinned["table_bytes"] > MAX_TABLE_BYTES
            or (pinned.get("uncompressed_bytes") or 0) > MAX_UNCOMPRESSED_BYTES):
        raise DataBankError("The full confirmed snapshot exceeds this service's preparation limits. Upload a supported matching snapshot.")
    if not get_token():
        raise DataBankError("Server-side Data Bank access is unavailable. Upload the benchmark items or contact the maintainer.")
    try:
        directory = Path(directory)
        path = Path(hf_hub_download(repo_id=REPO, filename=pinned["table_path"], repo_type="dataset",
                                   revision=pinned["revision"], token=get_token(), etag_timeout=10,
                                   cache_dir=_cache_dir() / "sources"))
        check_stopped()
        if path.stat().st_size != pinned["table_bytes"] or data.file_sha256(path) != pinned["sha256"]:
            raise ValueError("Source bytes changed")
        with pq.ParquetFile(path) as parquet:
            actual_bytes = sum(parquet.metadata.row_group(i).total_byte_size for i in range(parquet.metadata.num_row_groups))
            if (parquet.metadata.num_rows != pinned["item_count"] or actual_bytes > MAX_UNCOMPRESSED_BYTES
                    or parquet.schema_arrow.names != pinned["columns"]):
                raise ValueError("Source schema or population changed")
        # Validate the external ID mapping; opaque IDs alone cannot prove identity.
        observed_ids = pq.read_table(path, columns=["benchmark_id"])["benchmark_id"].to_pylist()
        if any(value is None or not str(value).strip() for value in observed_ids):
            raise ValueError("Every item requires a verified benchmark identity")
        ids = {str(value) for value in observed_ids}
        if not ids or not ids.issubset(set(pinned["benchmark_ids"])):
            raise ValueError("Source benchmark identity changed")
        check_stopped()
        dataset = data.prepare_data(path, directory, benchmark=pinned["benchmark"],
                                    source_repo=REPO, source_revision=pinned["revision"], source_table=pinned["table_path"])
        dataset["source"].pop("path", None)
        dataset["source"].update({"candidate_id": pinned["id"], "version": pinned["version"],
                                  "benchmark_ids": pinned["benchmark_ids"], "identity_validation": "repository_metadata_mapping",
                                  "testing_scope": pinned["testing_scope"]})
        write_json(directory / "dataset.json", dataset)
        check_stopped()
        return dataset
    except InterruptedError:
        raise
    except Exception:
        raise DataBankError("The confirmed Data Bank snapshot failed access or validation. No model calls were made; retry or upload matching items.") from None


def prepare_candidate(directory: Path, candidate: dict, stopped=None) -> dict:
    """Serialize full-table preparation to bound memory across concurrent jobs."""
    while not _preparation_lock.acquire(timeout=.1):
        if stopped and stopped():
            raise InterruptedError("Dataset preparation stopped.")
    try:
        return _prepare_candidate(directory, candidate, stopped)
    finally:
        _preparation_lock.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", required=True)
    parser.add_argument("--output", type=Path, default=BUNDLED_CATALOG)
    options = parser.parse_args()
    result = refresh_catalog()
    options.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Indexed {len(result['entries'])} benchmark entries at {result['revision']}; no item rows saved.")
