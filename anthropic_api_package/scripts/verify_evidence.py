#!/usr/bin/env python3
"""Post-hoc verification of evidence citations in scoring.json files.

Two-level verification per evidence type:
  Quotes:   L1 scoring.json vs benchmark YAML  |  L2 YAML vs PDF page text
  Web:      L1 scoring.json vs region.yaml      |  L2 HTTP liveness
  Dataset:  L1 scoring.json vs DA report         |  L2 re-sample HF with same seed

Usage:
    python scripts/verify_evidence.py assessments/expert_.../slug/
    python scripts/verify_evidence.py --all
    python scripts/verify_evidence.py --all --skip-web --skip-hf
"""

import argparse
import json
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

import yaml
from tqdm import tqdm

# === Compose-prompt import (pure function, no side effects) ===
sys.path.insert(0, str(Path(__file__).parent))
from compose_prompt import extract_web_source_registry

ROOT = Path(__file__).resolve().parent.parent
BENCHMARKS = ROOT / "benchmarks"
ASSESSMENTS = ROOT / "assessments"
PAPERS = ROOT / "papers"
DA_CACHE = BENCHMARKS / "da_cache"

DIMENSIONS = [
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
]

QUOTE_SIM_THRESHOLD = 0.6
PDF_SUBSTRING_THRESHOLD = 0.5
WEB_TIMEOUT = 10

# === Regex patterns ===
RE_QUOTE_ID = re.compile(r"\[Q(\d+)\]")
RE_QUOTE_TEXT = re.compile(r"['‘“\"](.*?)['’”\"]", re.DOTALL)
RE_QUOTE_PAGE = re.compile(r"\(p\.(\d+)\)")
RE_WEB_ID = re.compile(r"^\[WEB-(\d+)\]")
RE_DATASET_DID_PREFIXED = re.compile(r"DATASET-(D\d+|(?:CRITICAL|MAJOR|MINOR)\d+)")
RE_DATASET_DID_ORG = re.compile(r"([A-Z][A-Z0-9_]*-D\d+)")
RE_REPORT_DID = re.compile(r"\b(D\d+|(?:CRITICAL|MAJOR|MINOR)\d+)\b")
RE_CROSSCUTTING = re.compile(r"(?:Cross-cutting\s+)?([CM])(\d+)")


# =========================================================================
#  Assessment discovery
# =========================================================================

def discover_assessments() -> list[Path]:
    results = []
    for scoring_path in sorted(ASSESSMENTS.rglob("scoring.json")):
        scoring = json.loads(scoring_path.read_text())
        first_dim = next(iter(scoring.get("dimensions", {}).values()), {})
        if "evidence_map" in first_dim:
            results.append(scoring_path.parent)
    return results


def resolve_benchmark_yaml(assessment_dir: Path) -> Path | None:
    name = assessment_dir.parent.name
    p = BENCHMARKS / f"{name}.yaml"
    return p if p.exists() else None


def resolve_pdf_path(assessment_dir: Path) -> Path | None:
    name = assessment_dir.parent.name
    # expert_b082a2ed12a9__ltzglue -> ltzglue
    stem = name.split("__", 1)[1] if "__" in name else name
    p = PAPERS / f"{stem}.pdf"
    return p if p.exists() else None


# =========================================================================
#  Structural checks
# =========================================================================

def _normalize_crosscutting_id(raw: str) -> str | None:
    m = RE_CROSSCUTTING.search(raw)
    return f"{m.group(1)}{m.group(2)}" if m else None


def _extract_ids_from_evidence(dim_data: dict) -> dict[str, set]:
    """Build sets of evidence IDs present in each evidence array."""
    ids = {"quote": set(), "web": set(), "dataset": set()}
    for q in dim_data.get("evidence_quotes", []):
        for m in RE_QUOTE_ID.finditer(q):
            ids["quote"].add(f"Q{m.group(1)}")
    for w in dim_data.get("evidence_web_sources", []):
        m = RE_WEB_ID.match(w)
        if m:
            ids["web"].add(f"WEB-{m.group(1)}")
    for d in dim_data.get("evidence_dataset", []):
        for m in RE_DATASET_DID_PREFIXED.finditer(d):
            ids["dataset"].add(m.group(1))
        for m in RE_DATASET_DID_ORG.finditer(d):
            if not m.group(0).startswith("DATASET-"):
                ids["dataset"].add(m.group(1))
        norm = _normalize_crosscutting_id(d)
        if norm:
            ids["dataset"].add(norm)
    return ids


def check_structural(scoring: dict) -> list[dict]:
    results = []

    for dim_key in DIMENSIONS:
        dim = scoring.get("dimensions", {}).get(dim_key, {})
        if not dim:
            continue

        # === Citation format validation ===
        for i, q in enumerate(dim.get("evidence_quotes", [])):
            if not RE_QUOTE_ID.search(q):
                results.append({"check": "quote_format", "status": "FAIL",
                                "detail": f"{dim_key}[{i}]: missing [QN]: {q[:80]}"})

        for i, w in enumerate(dim.get("evidence_web_sources", [])):
            if not RE_WEB_ID.match(w):
                results.append({"check": "web_format", "status": "FAIL",
                                "detail": f"{dim_key}[{i}]: missing [WEB-N]: {w[:80]}"})

        # === Evidence map consistency ===
        ids = _extract_ids_from_evidence(dim)
        emap = dim.get("evidence_map", {})
        for checklist_id, refs in emap.items():
            for ref in refs:
                found = False
                if ref.startswith("Q") and ref in ids["quote"]:
                    found = True
                elif ref.startswith("WEB-") and ref in ids["web"]:
                    found = True
                elif ref in ids["dataset"] or any(
                    m.group(1) in ids["dataset"]
                    for m in RE_DATASET_DID_PREFIXED.finditer(ref)):
                    found = True
                else:
                    norm = _normalize_crosscutting_id(ref)
                    if norm and norm in ids["dataset"]:
                        found = True
                if not found:
                    results.append({
                        "check": "map_consistency", "status": "FAIL",
                        "detail": f"{dim_key} map[{checklist_id}] -> {ref} not in arrays"
                    })

        # === Orphan evidence (warnings) ===
        all_refs = set()
        for refs in emap.values():
            for r in refs:
                all_refs.add(r)
                norm = _normalize_crosscutting_id(r)
                if norm:
                    all_refs.add(norm)

        for qid in ids["quote"]:
            if qid not in all_refs:
                results.append({"check": "orphan", "status": "WARN",
                                "detail": f"{dim_key}: {qid} in quotes but not in map"})
        for wid in ids["web"]:
            if wid not in all_refs:
                results.append({"check": "orphan", "status": "WARN",
                                "detail": f"{dim_key}: {wid} in web but not in map"})

    return results


# =========================================================================
#  Quote verification — Level 1 (scoring vs YAML)
# =========================================================================

def _parse_scored_quote(raw: str) -> dict | None:
    qid_m = RE_QUOTE_ID.search(raw)
    if not qid_m:
        return None
    text_m = RE_QUOTE_TEXT.search(raw)
    page_m = RE_QUOTE_PAGE.search(raw)
    return {
        "qid": f"Q{qid_m.group(1)}",
        "qnum": int(qid_m.group(1)),
        "text": text_m.group(1).strip() if text_m else "",
        "page": int(page_m.group(1)) if page_m else None,
    }


def _build_quote_index(bm_yaml: dict) -> dict[str, dict]:
    idx = {}
    for q in bm_yaml.get("verbatim_quotes", []):
        qid = str(q.get("id", ""))
        idx[qid] = {"text": q.get("text", ""), "page": q.get("page"),
                     "dimension": q.get("dimension", "")}
    return idx


def _fuzzy_match(scored_text: str, yaml_text: str) -> float:
    a = scored_text.rstrip(".").replace("…", "").replace("...", "").strip().lower()
    b = yaml_text.strip().lower()
    if not a or not b:
        return 0.0
    ratio = SequenceMatcher(None, a, b).ratio()
    if a in b:
        ratio = max(ratio, 0.85)
    return ratio


def verify_quotes_l1(scoring: dict, bm_yaml: dict) -> list[dict]:
    """Level 1: scoring.json evidence_quotes vs benchmark YAML verbatim_quotes."""
    index = _build_quote_index(bm_yaml)
    results = []
    seen = set()

    for dim_key in DIMENSIONS:
        dim = scoring.get("dimensions", {}).get(dim_key, {})
        for raw in dim.get("evidence_quotes", []):
            parsed = _parse_scored_quote(raw)
            if not parsed or parsed["qid"] in seen:
                continue
            seen.add(parsed["qid"])

            r = {"qid": parsed["qid"], "exists": False,
                 "page_match": None, "text_similarity": 0.0, "status": "FAIL"}

            if parsed["qid"] not in index:
                r["detail"] = "Q-ID not in YAML"
                results.append(r)
                continue

            r["exists"] = True
            entry = index[parsed["qid"]]

            if parsed["page"] is not None and entry["page"] is not None:
                r["page_match"] = parsed["page"] == entry["page"]

            r["text_similarity"] = round(
                _fuzzy_match(parsed["text"], entry["text"]), 3)

            text_ok = r["text_similarity"] >= QUOTE_SIM_THRESHOLD
            page_ok = r["page_match"] is None or r["page_match"]

            if text_ok and page_ok:
                r["status"] = "PASS"
            elif text_ok:
                r["status"] = "WARN"
                r["detail"] = (f"page mismatch: cited p.{parsed['page']}, "
                               f"YAML p.{entry['page']}")
            else:
                r["status"] = "FAIL"
                r["detail"] = f"low similarity ({r['text_similarity']})"

            results.append(r)

    return results


# =========================================================================
#  Quote verification — Level 2 (YAML vs PDF)
# =========================================================================

def _extract_pdf_pages(pdf_path: Path) -> dict[int, str]:
    """Extract text from each page using PyMuPDF. Returns {page_num: text}."""
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    doc = fitz.open(str(pdf_path))
    pages = {}
    for i, page in enumerate(doc, start=1):
        pages[i] = page.get_text()
    doc.close()
    return pages


def _normalize_pdf_text(text: str) -> str:
    """Rejoin hyphenated line breaks and collapse whitespace."""
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _find_in_page(quote_text: str, page_text: str) -> tuple[float, str]:
    """Fuzzy substring search: best SequenceMatcher ratio of the quote
    against sliding windows of the page text. Returns (similarity, best_chunk)."""
    qt = _normalize_pdf_text(quote_text).lower()
    pt = _normalize_pdf_text(page_text).lower()
    if not qt or not pt:
        return 0.0, ""
    # Exact substring
    if qt in pt:
        idx = pt.index(qt)
        return 1.0, pt[idx:idx + len(qt)]
    # Sliding window: check ratio against windows roughly the size of the quote
    window = len(qt)
    best = 0.0
    best_chunk = ""
    step = max(1, window // 5)
    for start in range(0, len(pt) - window + 1, step):
        chunk_end = start + window + window // 2
        chunk = pt[start:chunk_end]
        ratio = SequenceMatcher(None, qt, chunk).ratio()
        if ratio > best:
            best = ratio
            best_chunk = chunk
        if best >= 0.9:
            break

    # Re-score pass: trim best chunk to quote length and re-evaluate.
    # Catches cases where the correct text is present but trailing context
    # in the oversized window dilutes the ratio below threshold.
    if 0.35 <= best < PDF_SUBSTRING_THRESHOLD and best_chunk:
        trimmed = best_chunk[:len(qt)]
        ratio = SequenceMatcher(None, qt, trimmed).ratio()
        if ratio > best:
            best = ratio
            best_chunk = trimmed

    return best, best_chunk


def _find_in_page_fragments(quote_text: str, page_text: str,
                            threshold: float = PDF_SUBSTRING_THRESHOLD,
                            ) -> tuple[float, str]:
    """Ellipsis-aware matching: split quote on '...' and match each fragment
    independently. Returns (min_fragment_similarity, best_chunk_of_weakest).
    Only called as a fallback when the full-quote match fails."""
    fragments = [f.strip() for f in quote_text.split("...") if f.strip()]
    if len(fragments) < 2:
        return 0.0, ""
    worst_sim = 1.0
    worst_chunk = ""
    for frag in fragments:
        if len(frag) < 15:
            continue
        sim, chunk = _find_in_page(frag, page_text)
        if sim < worst_sim:
            worst_sim = sim
            worst_chunk = chunk
    return worst_sim, worst_chunk


def verify_quotes_l2(bm_yaml: dict, pdf_path: Path) -> list[dict]:
    """Level 2: benchmark YAML verbatim_quotes vs actual PDF page text."""
    pages = _extract_pdf_pages(pdf_path)
    results = []

    for q in bm_yaml.get("verbatim_quotes", []):
        qid = str(q.get("id", ""))
        text = q.get("text", "")
        cited_page = q.get("page")

        r = {"qid": qid, "cited_page": cited_page,
             "found_on_page": None, "similarity": 0.0, "status": "FAIL",
             "quote_text": text}

        if not text or cited_page is None:
            r["detail"] = "missing text or page in YAML"
            results.append(r)
            continue

        # Try cited page first, then ±1 as fallback
        candidates = [cited_page]
        if cited_page - 1 in pages:
            candidates.append(cited_page - 1)
        if cited_page + 1 in pages:
            candidates.append(cited_page + 1)

        best_sim = 0.0
        best_page = None
        best_segment = ""
        for pg in candidates:
            if pg not in pages:
                continue
            sim, segment = _find_in_page(text, pages[pg])
            if sim > best_sim:
                best_sim = sim
                best_page = pg
                best_segment = segment

        # Cross-page fallback: try concatenating adjacent pages
        if best_sim < PDF_SUBSTRING_THRESHOLD and cited_page in pages:
            next_pg = cited_page + 1
            if next_pg in pages:
                joined = pages[cited_page] + "\n" + pages[next_pg]
                sim, segment = _find_in_page(text, joined)
                if sim > best_sim:
                    best_sim = sim
                    best_page = f"{cited_page}+{next_pg}"
                    best_segment = segment

        # Ellipsis-aware fallback: match fragments independently
        if best_sim < PDF_SUBSTRING_THRESHOLD and "..." in text:
            for pg in candidates:
                if pg not in pages:
                    continue
                sim, segment = _find_in_page_fragments(text, pages[pg])
                if sim > best_sim:
                    best_sim = sim
                    best_page = pg
                    best_segment = segment

        r["similarity"] = round(best_sim, 3)
        r["found_on_page"] = best_page
        r["matched_segment"] = best_segment

        if best_sim >= PDF_SUBSTRING_THRESHOLD and best_page == cited_page:
            r["status"] = "PASS"
        elif best_sim >= PDF_SUBSTRING_THRESHOLD:
            r["status"] = "WARN"
            r["detail"] = f"found on page {best_page}, not cited page {cited_page}"
        else:
            r["status"] = "FAIL"
            r["detail"] = f"best similarity {best_sim} below threshold"

        results.append(r)

    return results


def verify_quotes_scoring_vs_pdf(scoring: dict, pdf_path: Path) -> list[dict]:
    """Scoring.json quote text checked directly against PDF page text."""
    pages = _extract_pdf_pages(pdf_path)
    results = []
    seen = set()

    for dim_key in DIMENSIONS:
        dim = scoring.get("dimensions", {}).get(dim_key, {})
        for raw in dim.get("evidence_quotes", []):
            parsed = _parse_scored_quote(raw)
            if not parsed or parsed["qid"] in seen:
                continue
            seen.add(parsed["qid"])

            text = parsed["text"]
            cited_page = parsed["page"]
            r = {"qid": parsed["qid"], "cited_page": cited_page,
                 "found_on_page": None, "similarity": 0.0, "status": "FAIL",
                 "scored_text": text}

            if not text:
                r["detail"] = "no quote text extracted from scoring"
                results.append(r)
                continue

            # Search cited page first, then ±1, then all pages as last resort
            candidates = []
            if cited_page and cited_page in pages:
                candidates.append(cited_page)
                if cited_page - 1 in pages:
                    candidates.append(cited_page - 1)
                if cited_page + 1 in pages:
                    candidates.append(cited_page + 1)
            remaining = [p for p in sorted(pages) if p not in candidates]
            candidates.extend(remaining)

            best_sim = 0.0
            best_page = None
            best_segment = ""
            for pg in candidates:
                sim, segment = _find_in_page(text, pages[pg])
                if sim > best_sim:
                    best_sim = sim
                    best_page = pg
                    best_segment = segment
                if best_sim >= 0.9:
                    break

            # Cross-page fallback: try concatenating adjacent pages
            if best_sim < PDF_SUBSTRING_THRESHOLD and cited_page and cited_page in pages:
                next_pg = cited_page + 1
                if next_pg in pages:
                    joined = pages[cited_page] + "\n" + pages[next_pg]
                    sim, segment = _find_in_page(text, joined)
                    if sim > best_sim:
                        best_sim = sim
                        best_page = f"{cited_page}+{next_pg}"
                        best_segment = segment

            # Ellipsis-aware fallback: match fragments independently
            if best_sim < PDF_SUBSTRING_THRESHOLD and "..." in text:
                for pg in candidates:
                    sim, segment = _find_in_page_fragments(text, pages[pg])
                    if sim > best_sim:
                        best_sim = sim
                        best_page = pg
                        best_segment = segment
                    if best_sim >= 0.9:
                        break

            r["similarity"] = round(best_sim, 3)
            r["found_on_page"] = best_page
            r["matched_segment"] = best_segment

            if best_sim >= PDF_SUBSTRING_THRESHOLD:
                r["status"] = "PASS"
            else:
                r["detail"] = f"best similarity {best_sim} on page {best_page}"

            results.append(r)

    return results


# =========================================================================
#  Web source verification — Level 1 (scoring vs registry)
# =========================================================================

def verify_web_l1(scoring: dict, region_yaml_path: Path) -> list[dict]:
    """Level 1: WEB-N IDs in scoring.json exist in region.yaml registry."""
    with open(region_yaml_path) as f:
        region_data = yaml.safe_load(f)
    registry = extract_web_source_registry(region_data)
    registry_by_id = {e["id"]: e["url"] for e in registry}

    cited = set()
    for dim_key in DIMENSIONS:
        dim = scoring.get("dimensions", {}).get(dim_key, {})
        for w in dim.get("evidence_web_sources", []):
            m = RE_WEB_ID.match(w)
            if m:
                cited.add(f"WEB-{m.group(1)}")

    results = []
    for wid in sorted(cited):
        exists = wid in registry_by_id
        url = registry_by_id.get(wid, "")
        results.append({
            "web_id": wid, "exists": exists, "url": url,
            "status": "PASS" if exists else "FAIL",
            **({"detail": "not in region.yaml registry"} if not exists else {})
        })
    return results


# =========================================================================
#  Web source verification — Level 2 (HTTP liveness)
# =========================================================================

def verify_web_l2(l1_results: list[dict]) -> list[dict]:
    """Level 2: HTTP HEAD each URL from the L1 results."""
    import requests
    results = []
    urls = [(r["web_id"], r["url"]) for r in l1_results if r.get("url")]
    for wid, url in tqdm(urls, desc="  HTTP checks", leave=False):
        r = {"web_id": wid, "url": url}
        try:
            resp = requests.head(url, timeout=WEB_TIMEOUT, allow_redirects=True)
            r["http_code"] = resp.status_code
            # Any HTTP response means the URL is real — even 403 (paywall),
            # 401 (auth-required), or 451 (geo-blocked). Sonnet accesses
            # content via web_search snippets, not direct fetches.
            r["status"] = "alive"
        except requests.exceptions.Timeout:
            r["http_code"] = None
            r["status"] = "timeout"
        except requests.exceptions.ConnectionError:
            r["http_code"] = None
            r["status"] = "dns_error"
        except Exception as e:
            r["http_code"] = None
            r["status"] = "error"
            r["detail"] = str(e)[:200]
        results.append(r)
    return results


# =========================================================================
#  Dataset evidence — Level 1 (scoring vs report)
# =========================================================================

def _extract_cited_evidence_section(report_text: str) -> str:
    for heading in ("### Cited Evidence", "### Datapoint Citations Registry"):
        m = re.search(re.escape(heading) + r"\n(.*)", report_text, re.DOTALL)
        if m:
            return m.group(1)
    return ""


def verify_dataset_l1(scoring: dict, report_path: Path | None) -> list[dict]:
    """Level 1: D-IDs and cross-cutting IDs in scoring.json exist in DA report."""
    # Collect all cited IDs — two formats:
    #   single-dataset mode: "DATASET-D23", "DATASET-MAJOR5"  → bare ID "D23", "MAJOR5"
    #   org mode:            "QUAERO-D3", "CAS-D15"           → kept as-is
    all_dids = set()
    all_cc = set()
    for dim_key in DIMENSIONS:
        dim = scoring.get("dimensions", {}).get(dim_key, {})
        for entry in dim.get("evidence_dataset", []):
            for m in RE_DATASET_DID_PREFIXED.finditer(entry):
                all_dids.add(m.group(1))
            for m in RE_DATASET_DID_ORG.finditer(entry):
                if not m.group(0).startswith("DATASET-"):
                    all_dids.add(m.group(1))
            norm = _normalize_crosscutting_id(entry)
            if norm:
                all_cc.add(norm)

    if not all_dids and not all_cc:
        return []

    report_exists = report_path is not None and report_path.exists()
    report_dids = set()
    report_cc = set()

    if report_exists:
        text = report_path.read_text(encoding="utf-8")
        for m in RE_REPORT_DID.finditer(text):
            report_dids.add(m.group(1))
        for m in RE_DATASET_DID_ORG.finditer(text):
            report_dids.add(m.group(1))
        # Cross-cutting IDs appear in the full report body
        for m in RE_CROSSCUTTING.finditer(text):
            report_cc.add(f"{m.group(1)}{m.group(2)}")

    results = []
    for did in sorted(all_dids):
        in_report = did in report_dids
        results.append({
            "did": did, "type": "datapoint",
            "in_report": in_report, "report_exists": report_exists,
            "status": "PASS" if in_report else ("FAIL" if report_exists else "WARN"),
        })
    for cc in sorted(all_cc):
        in_report = cc in report_cc
        results.append({
            "did": cc, "type": "cross-cutting",
            "in_report": in_report, "report_exists": report_exists,
            "status": "PASS" if in_report else ("FAIL" if report_exists else "WARN"),
        })
    return results


# =========================================================================
#  Dataset evidence — Level 2 (re-sample HF, verify examples)
# =========================================================================

def _resolve_hf_datasets(assessment_dir: Path) -> list[dict]:
    """Resolve HF dataset IDs for this assessment's benchmark.

    Returns list of {repo_id, config} dicts.
    """
    hf_links_path = BENCHMARKS / "hf_links.json"
    if not hf_links_path.exists():
        return []

    with open(hf_links_path) as f:
        hf_links = json.load(f)

    scoring = json.loads((assessment_dir / "scoring.json").read_text())
    bm_name = scoring.get("benchmark", "").lower()

    entry = hf_links.get(bm_name)
    if not entry:
        for v in hf_links.values():
            if v.get("benchmark_name", "").lower() == bm_name:
                entry = v
                break
    if not entry:
        return []
    hf_org = entry.get("hf_org")
    hf_id = entry.get("hf_dataset_id")
    hf_config = entry.get("hf_config")

    if hf_org:
        # Multi-dataset: resolve org datasets from cache directory names
        datasets = []
        for cache_dir in sorted(DA_CACHE.iterdir()):
            if not cache_dir.is_dir():
                continue
            # Cache dir format: OrgName__DatasetName or OrgName__DatasetName__config
            parts = cache_dir.name.split("__")
            if len(parts) >= 2 and parts[0] == hf_org:
                repo_id = f"{parts[0]}/{parts[1]}"
                config = parts[2] if len(parts) > 2 else None
                datasets.append({"repo_id": repo_id, "config": config})
        return datasets
    elif hf_id:
        return [{"repo_id": hf_id, "config": hf_config}]
    return []


def _parse_content_sample_markdown(md: str) -> dict[int, str]:
    """Parse content_sample markdown into {example_num: full_example_text}."""
    examples = {}
    current_num = None
    current_lines = []

    for line in md.split("\n"):
        m = re.match(r"^### Example (\d+)", line)
        if m:
            if current_num is not None:
                examples[current_num] = "\n".join(current_lines)
            current_num = int(m.group(1))
            current_lines = [line]
        elif current_num is not None:
            current_lines.append(line)

    if current_num is not None:
        examples[current_num] = "\n".join(current_lines)

    return examples


def _resolve_best_split(repo_id: str, config: str | None) -> str:
    """Pick the best split to sample from, using cached metadata if available."""
    cache_key = repo_id.replace("/", "__")
    if config:
        cache_key += f"__{config}"
    cache_path = DA_CACHE / cache_key / "script_outputs.json"
    if cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text())
            meta = json.loads(cached.get("hf_metadata", "{}"))
            splits_by_config = meta.get("splits_info", {}).get("splits_by_config", {})
            available = splits_by_config.get(config, next(iter(splits_by_config.values()), []))
            if available:
                return "train" if "train" in available else available[0]
        except (json.JSONDecodeError, KeyError):
            pass
    return "train"


def _run_content_sample(repo_id: str, config: str | None) -> str | None:
    """Re-run content_sample.py with seed 42. Returns markdown or None."""
    script = ROOT / "scripts" / "dataset_analysis" / "content_sample.py"
    split = _resolve_best_split(repo_id, config)
    cmd = [sys.executable, str(script), "--repo_id", repo_id,
           "--split", split, "--seed", "42"]
    if config:
        cmd += ["--config", config]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            return None
        out = json.loads(result.stdout)
        return out.get("markdown", "")
    except Exception:
        return None


def _parse_did_examples_org(report_text: str) -> dict:
    """Parse org-mode cited evidence: **QUAERO-D3**: Example 95: ..."""
    did_examples = {}
    for line in report_text.split("\n"):
        did_m = re.match(r"^-\s+\*\*([A-Z][A-Z0-9_]*-D\d+)\*\*:\s+Example\s+(\d+)", line)
        if did_m:
            did = did_m.group(1)
            example_num = int(did_m.group(2))
            rest = line[did_m.end():]
            did_examples[did] = {"example_num": example_num, "context": rest.strip(": ")}
    return did_examples


def _parse_did_examples_single(report_text: str) -> dict:
    """Parse single-dataset citation table: | D2 | MILU/Hindi | Ex.69 | ... |"""
    did_examples = {}
    for line in report_text.split("\n"):
        m = re.match(r"^\|\s*(D\d+)\s*\|([^|]*)\|\s*Ex\.\s*(\d+)\s*\|([^|]*)\|([^|]*)\|", line)
        if m:
            did = m.group(1)
            example_num = int(m.group(3))
            excerpt = m.group(5).strip()
            did_examples[did] = {
                "example_num": example_num,
                "context": excerpt,
                "prefix": "_SINGLE",
            }
    return did_examples


def verify_dataset_l2(
    scoring: dict,
    report_path: Path | None,
    assessment_dir: Path,
) -> list[dict]:
    """Level 2: re-sample HF datasets, verify D-ID example references."""
    report_text = ""
    if report_path and report_path.exists():
        report_text = report_path.read_text(encoding="utf-8")

    cited_section = _extract_cited_evidence_section(report_text)

    # Try both formats — org mode (bullet list) and single-dataset (pipe table)
    did_examples = _parse_did_examples_org(cited_section)
    is_single = False
    if not did_examples:
        did_examples = _parse_did_examples_single(report_text)
        is_single = True

    if not did_examples:
        return []

    # Re-run content_sample for each dataset and build example indexes
    hf_datasets = _resolve_hf_datasets(assessment_dir)
    dataset_examples = {}  # prefix -> {example_num: text}

    for ds in tqdm(hf_datasets, desc="  HF re-sample", leave=False):
        repo_id = ds["repo_id"]
        prefix = repo_id.split("/")[-1].upper()  # e.g., "QUAERO"

        md = _run_content_sample(repo_id, ds.get("config"))
        if md is not None:
            dataset_examples[prefix] = _parse_content_sample_markdown(md)
        else:
            dataset_examples[prefix] = None

    # Single-dataset mode: map the sole HF dataset to the "_SINGLE" prefix
    if is_single and len(hf_datasets) == 1:
        real_prefix = hf_datasets[0]["repo_id"].split("/")[-1].upper()
        dataset_examples["_SINGLE"] = dataset_examples.get(real_prefix)

    # Verify each D-ID
    results = []
    for did, info in sorted(did_examples.items()):
        if is_single:
            prefix = "_SINGLE"
        else:
            prefix = did.rsplit("-D", 1)[0]
        example_num = info["example_num"]
        context_keywords = info["context"]

        r = {"did": did, "example_num": example_num,
             "example_exists": False, "terms_found": None, "status": "FAIL",
             "context": context_keywords}

        if prefix not in dataset_examples:
            r["detail"] = f"no HF dataset resolved for prefix {prefix}"
            results.append(r)
            continue

        if dataset_examples[prefix] is None:
            r["detail"] = "content_sample.py failed"
            r["status"] = "WARN"
            results.append(r)
            continue

        examples = dataset_examples[prefix]
        if example_num not in examples:
            r["detail"] = f"Example {example_num} not in re-sampled output"
            results.append(r)
            continue

        r["example_exists"] = True
        r["example_excerpt"] = examples[example_num][:300]
        example_text = examples[example_num].lower()

        # Extract key terms: prefer non-ASCII data content (Hindi, French
        # accented, etc.) over English commentary which is just the report
        # author's description and won't appear in non-English datasets.
        data_terms = re.findall(r"[^\x00-\x7F\s|`]{3,}", context_keywords)
        latin_terms = re.findall(r"[a-zA-ZÀ-ɏ]{4,}", context_keywords)
        # Only use Latin terms if no data-language terms were found and the
        # example text itself is predominantly ASCII (i.e. English dataset)
        ascii_ratio = sum(1 for c in example_text if c.isascii()) / max(len(example_text), 1)
        if data_terms:
            words = data_terms
        elif ascii_ratio > 0.9:
            words = latin_terms
        else:
            words = []

        if words:
            matched_terms = [w for w in words if w.lower() in example_text]
            missed_terms = [w for w in words if w.lower() not in example_text]
            r["terms_found"] = len(matched_terms) > 0
            r["terms_matched"] = f"{len(matched_terms)}/{len(words)}"
            r["matched_terms"] = matched_terms
            r["missed_terms"] = missed_terms
        else:
            r["terms_found"] = True
            r["detail"] = r.get("detail", "terms check skipped (language mismatch)")

        if r["example_exists"] and r["terms_found"]:
            r["status"] = "PASS"
        elif r["example_exists"]:
            r["status"] = "WARN"
            r["detail"] = f"example exists but key terms not found ({r.get('terms_matched', '')})"

        results.append(r)

    return results


# =========================================================================
#  Diagnostic output: matched / unmatched fuzzy-matching examples
# =========================================================================

def _print_fuzzy_examples(label: str, items: list[dict], n: int = 3):
    """Print n matched and n unmatched fuzzy-matching pairs to stdout."""
    passed = [i for i in items if i.get("status") in ("PASS", "WARN")]
    failed = [i for i in items if i.get("status") == "FAIL"]

    passed.sort(key=lambda x: x.get("similarity", 0), reverse=True)
    failed.sort(key=lambda x: x.get("similarity", 0), reverse=True)

    def _quote(item):
        text = item.get("scored_text") or item.get("quote_text") or ""
        return text[:120] if text else "(no text)"

    def _segment(item):
        return (item.get("matched_segment") or "")[:120] or "(no segment)"

    if passed or failed:
        print(f"\n  [{label}] Fuzzy-matching examples:")

    if passed:
        print(f"    MATCHED ({len(passed)} total):")
        for item in passed[:n]:
            sim = item.get("similarity", 0)
            pg = item.get("found_on_page", "?")
            print(f"      sim={sim:.3f}  page={pg}")
            print(f"        quote: \"{_quote(item)}\"")
            print(f"        pdf:   \"{_segment(item)}\"")

    if failed:
        print(f"    UNMATCHED ({len(failed)} total):")
        for item in failed[:n]:
            sim = item.get("similarity", 0)
            pg = item.get("found_on_page", "?")
            print(f"      sim={sim:.3f}  best page={pg}")
            print(f"        quote: \"{_quote(item)}\"")
            print(f"        pdf:   \"{_segment(item)}\"")


# =========================================================================
#  Diagnostic dump: matched / unmatched pairs for external analysis
# =========================================================================

def _dump_fuzzy_pairs(result: dict, assessment_dir: Path, n: int = 10):
    all_items = []
    for item in result["quotes"].get("level2_vs_pdf", []):
        all_items.append({
            "source": "Q-L2",
            "similarity": item.get("similarity", 0),
            "cited_page": item.get("cited_page"),
            "found_on_page": item.get("found_on_page"),
            "quote_text": item.get("quote_text", ""),
            "matched_segment": item.get("matched_segment", ""),
            "status": item.get("status", ""),
        })
    for item in result["quotes"].get("scoring_vs_pdf", []):
        all_items.append({
            "source": "S-PDF",
            "similarity": item.get("similarity", 0),
            "cited_page": item.get("cited_page"),
            "found_on_page": item.get("found_on_page"),
            "quote_text": item.get("scored_text", ""),
            "matched_segment": item.get("matched_segment", ""),
            "status": item.get("status", ""),
        })

    matched = sorted(
        [i for i in all_items if i["status"] in ("PASS", "WARN")],
        key=lambda x: x["similarity"], reverse=True,
    )[:n]
    unmatched = sorted(
        [i for i in all_items if i["status"] == "FAIL"],
        key=lambda x: x["similarity"], reverse=True,
    )[:n]

    out = {"matched": matched, "unmatched": unmatched}
    (assessment_dir / "fuzzy_match_pairs.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))


def _dump_dataset_pairs(result: dict, assessment_dir: Path, n: int = 10):
    items = result["dataset"].get("level2_vs_hf", [])
    if not items:
        return

    def _entry(item):
        return {
            "did": item.get("did"),
            "example_num": item.get("example_num"),
            "status": item.get("status"),
            "example_exists": item.get("example_exists"),
            "terms_matched": item.get("terms_matched"),
            "matched_terms": item.get("matched_terms", []),
            "missed_terms": item.get("missed_terms", []),
            "context": item.get("context", ""),
            "example_excerpt": item.get("example_excerpt", ""),
            "detail": item.get("detail", ""),
        }

    matched = [_entry(i) for i in items if i["status"] == "PASS"][:n]
    unmatched = [_entry(i) for i in items if i["status"] in ("FAIL", "WARN")][:n]

    out = {"matched": matched, "unmatched": unmatched}
    (assessment_dir / "dataset_match_pairs.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))


# =========================================================================
#  Summary computation
# =========================================================================

def _pct(items: list[dict], pass_statuses: tuple = ("PASS",)) -> float | None:
    if not items:
        return None
    return round(100 * sum(1 for i in items if i.get("status") in pass_statuses) / len(items), 1)


def compute_summary(result: dict) -> dict:
    structural = result["structural"]
    return {
        "structural_total": len(structural),
        "structural_fails": sum(1 for i in structural if i["status"] == "FAIL"),
        "structural_warns": sum(1 for i in structural if i["status"] == "WARN"),

        "quote_l1_total": len(result["quotes"]["level1_vs_yaml"]),
        "quote_l1_pct": _pct(result["quotes"]["level1_vs_yaml"]),
        "quote_l2_total": len(result["quotes"]["level2_vs_pdf"]),
        "quote_l2_pct": _pct(result["quotes"]["level2_vs_pdf"], ("PASS", "WARN")),
        "quote_scoring_pdf_total": len(result["quotes"]["scoring_vs_pdf"]),
        "quote_scoring_pdf_pct": _pct(result["quotes"]["scoring_vs_pdf"]),

        "web_l1_total": len(result["web_sources"]["level1_vs_registry"]),
        "web_l1_pct": _pct(result["web_sources"]["level1_vs_registry"]),
        "web_l2_total": len(result["web_sources"]["level2_liveness"]),
        "web_l2_alive_pct": _pct(result["web_sources"]["level2_liveness"],
                                  ("alive",)),

        "dataset_l1_total": len(result["dataset"]["level1_vs_report"]),
        "dataset_l1_pct": _pct(result["dataset"]["level1_vs_report"]),
        "dataset_l2_total": len(result["dataset"]["level2_vs_hf"]),
        "dataset_l2_exists_pct": _pct(result["dataset"]["level2_vs_hf"],
                                       ("PASS", "WARN")),
        "dataset_l2_terms_pct": _pct(result["dataset"]["level2_vs_hf"]),
    }


# =========================================================================
#  Output formatting
# =========================================================================

def print_summary_table(all_results: list[dict]):
    print(f"\n{'=' * 100}")
    print("  EVIDENCE VERIFICATION SUMMARY")
    print(f"{'=' * 100}")
    print(f"  {'Assessment':<48} {'Q-L1':>6} {'Q-L2':>6} {'S→PDF':>6} "
          f"{'W-L1':>6} {'W-L2':>6} {'D-L1':>6} {'D-ex':>6} {'D-tm':>6} {'Struct':>6}")
    print(f"  {'-' * 48} {'-' * 6} {'-' * 6} {'-' * 6} "
          f"{'-' * 6} {'-' * 6} {'-' * 6} {'-' * 6} {'-' * 6} {'-' * 6}")

    def _f(val):
        return f"{val:5.1f}%" if val is not None else "  N/A"

    for r in all_results:
        s = r["summary"]
        name = r["assessment"]
        if len(name) > 47:
            name = "..." + name[-44:]

        sf = f"{s['structural_fails']}F" if s["structural_fails"] else "  OK"

        print(f"  {name:<48} {_f(s['quote_l1_pct']):>6} {_f(s['quote_l2_pct']):>6} "
              f"{_f(s.get('quote_scoring_pdf_pct')):>6} "
              f"{_f(s['web_l1_pct']):>6} {_f(s['web_l2_alive_pct']):>6} "
              f"{_f(s['dataset_l1_pct']):>6} {_f(s.get('dataset_l2_exists_pct')):>6} "
              f"{_f(s.get('dataset_l2_terms_pct')):>6} "
              f"{sf:>6}")

    print(f"{'=' * 100}\n")

    # Legend
    print("  Q-L1: quotes vs YAML   |  Q-L2: quotes vs PDF   |  S→PDF: scoring quotes vs PDF")
    print("  W-L1: web vs registry  |  W-L2: URL liveness   |  D-L1: data vs report")
    print("  D-ex: example exists in HF resample            |  D-tm: example + term match\n")


# =========================================================================
#  Per-assessment orchestrator
# =========================================================================

def verify_assessment(
    assessment_dir: Path,
    skip_web: bool = False,
    skip_hf: bool = False,
) -> dict:
    assessment_dir = Path(assessment_dir).resolve()
    scoring = json.loads((assessment_dir / "scoring.json").read_text())
    benchmark_name = scoring.get("benchmark", "unknown")

    bm_yaml_path = resolve_benchmark_yaml(assessment_dir)
    pdf_path = resolve_pdf_path(assessment_dir)
    region_yaml_path = assessment_dir / "region.yaml"
    report_path = assessment_dir / "dataset_analysis_report.md"

    bm_yaml = {}
    if bm_yaml_path:
        with open(bm_yaml_path) as f:
            bm_yaml = yaml.safe_load(f) or {}

    rel_path = str(assessment_dir.relative_to(ROOT))
    result = {
        "assessment": rel_path,
        "benchmark": benchmark_name,
        "structural": [],
        "quotes": {"level1_vs_yaml": [], "level2_vs_pdf": [], "scoring_vs_pdf": []},
        "web_sources": {"level1_vs_registry": [], "level2_liveness": []},
        "dataset": {"level1_vs_report": [], "level2_vs_hf": []},
        "summary": {},
    }

    # === Structural checks ===
    result["structural"] = check_structural(scoring)

    # === Quote L1: scoring vs YAML ===
    if bm_yaml:
        result["quotes"]["level1_vs_yaml"] = verify_quotes_l1(scoring, bm_yaml)

    # === Quote L2: YAML vs PDF ===
    if bm_yaml and pdf_path:
        result["quotes"]["level2_vs_pdf"] = verify_quotes_l2(bm_yaml, pdf_path)
        _print_fuzzy_examples("Q-L2", result["quotes"]["level2_vs_pdf"])

    # === Web L1: scoring vs registry ===
    if region_yaml_path.exists():
        result["web_sources"]["level1_vs_registry"] = verify_web_l1(
            scoring, region_yaml_path)

    # === Web L2: HTTP liveness ===
    if not skip_web and result["web_sources"]["level1_vs_registry"]:
        result["web_sources"]["level2_liveness"] = verify_web_l2(
            result["web_sources"]["level1_vs_registry"])

    # === Quote L3: scoring.json quotes vs PDF ===
    if pdf_path:
        result["quotes"]["scoring_vs_pdf"] = verify_quotes_scoring_vs_pdf(
            scoring, pdf_path)
        _print_fuzzy_examples("S→PDF", result["quotes"]["scoring_vs_pdf"])

    # === Dataset L1: scoring vs report ===
    result["dataset"]["level1_vs_report"] = verify_dataset_l1(
        scoring, report_path if report_path.exists() else None)

    # === Dataset L2: HF re-sampling ===
    if not skip_hf and result["dataset"]["level1_vs_report"]:
        result["dataset"]["level2_vs_hf"] = verify_dataset_l2(
            scoring, report_path if report_path.exists() else None,
            assessment_dir)

    result["summary"] = compute_summary(result)
    _dump_fuzzy_pairs(result, assessment_dir)
    _dump_dataset_pairs(result, assessment_dir)
    return result


# =========================================================================
#  CLI
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Verify evidence citations in scoring.json against original sources")
    parser.add_argument("assessment_dir", nargs="?", default=None,
                        help="Path to assessment directory (must contain scoring.json)")
    parser.add_argument("--all", action="store_true",
                        help="Auto-discover all v2 assessments")
    parser.add_argument("--skip-web", action="store_true",
                        help="Skip HTTP liveness checks")
    parser.add_argument("--skip-hf", action="store_true",
                        help="Skip HuggingFace re-sampling")
    parser.add_argument("--json-output", type=str, default=None,
                        help="Write combined results JSON")
    args = parser.parse_args()

    if args.all:
        dirs = discover_assessments()
        if not dirs:
            print("No v2 assessments found.", file=sys.stderr)
            sys.exit(1)
        print(f"Found {len(dirs)} v2 assessments")
    elif args.assessment_dir:
        dirs = [Path(args.assessment_dir).resolve()]
    else:
        parser.error("Provide an assessment directory or use --all")

    all_results = []
    for adir in tqdm(dirs, desc="Assessments"):
        try:
            result = verify_assessment(adir, skip_web=args.skip_web,
                                       skip_hf=args.skip_hf)
            all_results.append(result)
            # Write per-assessment JSON
            out = adir / "evidence_verification.json"
            out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"\nERROR on {adir}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()

    print_summary_table(all_results)

    if args.json_output:
        Path(args.json_output).write_text(
            json.dumps(all_results, indent=2, ensure_ascii=False))
        print(f"Combined results: {args.json_output}")


if __name__ == "__main__":
    main()
