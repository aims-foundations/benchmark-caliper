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
RE_DATASET_DID = re.compile(r"([A-Z][A-Z0-9_]*-D\d+)")
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
        for m in RE_DATASET_DID.finditer(d):
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
                elif RE_DATASET_DID.match(ref) and ref in ids["dataset"]:
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
    import fitz
    doc = fitz.open(str(pdf_path))
    pages = {}
    for i, page in enumerate(doc, start=1):
        pages[i] = page.get_text()
    doc.close()
    return pages


def _find_in_page(quote_text: str, page_text: str) -> float:
    """Fuzzy substring search: best SequenceMatcher ratio of the quote
    against sliding windows of the page text."""
    qt = quote_text.strip().lower()
    pt = page_text.lower()
    if not qt or not pt:
        return 0.0
    # Exact substring
    if qt in pt:
        return 1.0
    # Sliding window: check ratio against windows roughly the size of the quote
    window = len(qt)
    best = 0.0
    # Step through the page text in increments; full character-by-character
    # would be too slow for long pages, so step by ~20% of the quote length
    step = max(1, window // 5)
    for start in range(0, len(pt) - window + 1, step):
        chunk = pt[start:start + window + window // 2]
        ratio = SequenceMatcher(None, qt, chunk).ratio()
        best = max(best, ratio)
        if best >= 0.9:
            break
    return best


def verify_quotes_l2(bm_yaml: dict, pdf_path: Path) -> list[dict]:
    """Level 2: benchmark YAML verbatim_quotes vs actual PDF page text."""
    pages = _extract_pdf_pages(pdf_path)
    results = []

    for q in bm_yaml.get("verbatim_quotes", []):
        qid = str(q.get("id", ""))
        text = q.get("text", "")
        cited_page = q.get("page")

        r = {"qid": qid, "cited_page": cited_page,
             "found_on_page": None, "similarity": 0.0, "status": "FAIL"}

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
        for pg in candidates:
            if pg not in pages:
                continue
            sim = _find_in_page(text, pages[pg])
            if sim > best_sim:
                best_sim = sim
                best_page = pg

        r["similarity"] = round(best_sim, 3)
        r["found_on_page"] = best_page

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
            if 200 <= resp.status_code < 300:
                r["status"] = "alive"
            elif 300 <= resp.status_code < 400:
                r["status"] = "redirect"
            else:
                r["status"] = "dead"
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
    m = re.search(r"### Cited Evidence\n(.*)", report_text, re.DOTALL)
    return m.group(1) if m else ""


def verify_dataset_l1(scoring: dict, report_path: Path | None) -> list[dict]:
    """Level 1: D-IDs and cross-cutting IDs in scoring.json exist in DA report."""
    # Collect all cited IDs
    all_dids = set()
    all_cc = set()
    for dim_key in DIMENSIONS:
        dim = scoring.get("dimensions", {}).get(dim_key, {})
        for entry in dim.get("evidence_dataset", []):
            for m in RE_DATASET_DID.finditer(entry):
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
        cited_section = _extract_cited_evidence_section(text)
        for m in RE_DATASET_DID.finditer(cited_section):
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
    if bm_name not in hf_links:
        return []

    entry = hf_links[bm_name]
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


def _run_content_sample(repo_id: str, config: str | None) -> str | None:
    """Re-run content_sample.py with seed 42. Returns markdown or None."""
    script = ROOT / "scripts" / "dataset_analysis" / "content_sample.py"
    cmd = [sys.executable, str(script), "--repo_id", repo_id,
           "--split", "train", "--seed", "42"]
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


def verify_dataset_l2(
    scoring: dict,
    report_path: Path | None,
    assessment_dir: Path,
) -> list[dict]:
    """Level 2: re-sample HF datasets, verify D-ID example references."""
    # Collect D-IDs that reference specific examples (e.g., "QUAERO-D3: Example 95: ...")
    report_text = ""
    if report_path and report_path.exists():
        report_text = _extract_cited_evidence_section(
            report_path.read_text(encoding="utf-8"))

    # Parse the cited evidence section to find example-number references per D-ID
    # Format: **QUAERO-D3**: Example 95: "code ATC" in text
    did_examples = {}
    for line in report_text.split("\n"):
        did_m = re.match(r"^-\s+\*\*([A-Z][A-Z0-9_]*-D\d+)\*\*:\s+Example\s+(\d+)", line)
        if did_m:
            did = did_m.group(1)
            example_num = int(did_m.group(2))
            rest = line[did_m.end():]
            did_examples[did] = {"example_num": example_num, "context": rest.strip(": ")}

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

    # Verify each D-ID
    results = []
    for did, info in sorted(did_examples.items()):
        prefix = did.rsplit("-D", 1)[0]
        example_num = info["example_num"]
        context_keywords = info["context"]

        r = {"did": did, "example_num": example_num,
             "example_exists": False, "terms_found": None, "status": "FAIL"}

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
        example_text = examples[example_num].lower()

        # Extract key terms from the context and check presence in example
        # Use significant words (4+ chars, not common filler)
        words = re.findall(r"[a-zA-ZÀ-ɏ]{4,}", context_keywords)
        if words:
            found = sum(1 for w in words if w.lower() in example_text)
            r["terms_found"] = found > 0 or len(words) == 0
            r["terms_matched"] = f"{found}/{len(words)}"
        else:
            r["terms_found"] = True  # no terms to check

        if r["example_exists"] and r["terms_found"]:
            r["status"] = "PASS"
        elif r["example_exists"]:
            r["status"] = "WARN"
            r["detail"] = f"example exists but key terms not found ({r.get('terms_matched', '')})"

        results.append(r)

    return results


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

        "web_l1_total": len(result["web_sources"]["level1_vs_registry"]),
        "web_l1_pct": _pct(result["web_sources"]["level1_vs_registry"]),
        "web_l2_total": len(result["web_sources"]["level2_liveness"]),
        "web_l2_alive_pct": _pct(result["web_sources"]["level2_liveness"],
                                  ("alive", "redirect")),

        "dataset_l1_total": len(result["dataset"]["level1_vs_report"]),
        "dataset_l1_pct": _pct(result["dataset"]["level1_vs_report"]),
        "dataset_l2_total": len(result["dataset"]["level2_vs_hf"]),
        "dataset_l2_pct": _pct(result["dataset"]["level2_vs_hf"]),
    }


# =========================================================================
#  Output formatting
# =========================================================================

def print_summary_table(all_results: list[dict]):
    print(f"\n{'=' * 100}")
    print("  EVIDENCE VERIFICATION SUMMARY")
    print(f"{'=' * 100}")
    print(f"  {'Assessment':<48} {'Q-L1':>6} {'Q-L2':>6} "
          f"{'W-L1':>6} {'W-L2':>6} {'D-L1':>6} {'D-L2':>6} {'Struct':>6}")
    print(f"  {'-' * 48} {'-' * 6} {'-' * 6} "
          f"{'-' * 6} {'-' * 6} {'-' * 6} {'-' * 6} {'-' * 6}")

    def _f(val):
        return f"{val:5.1f}%" if val is not None else "  N/A"

    for r in all_results:
        s = r["summary"]
        name = r["assessment"]
        if len(name) > 47:
            name = "..." + name[-44:]

        sf = f"{s['structural_fails']}F" if s["structural_fails"] else "  OK"

        print(f"  {name:<48} {_f(s['quote_l1_pct']):>6} {_f(s['quote_l2_pct']):>6} "
              f"{_f(s['web_l1_pct']):>6} {_f(s['web_l2_alive_pct']):>6} "
              f"{_f(s['dataset_l1_pct']):>6} {_f(s['dataset_l2_pct']):>6} "
              f"{sf:>6}")

    print(f"{'=' * 100}\n")

    # Legend
    print("  Q-L1: quotes vs YAML  |  Q-L2: quotes vs PDF  |  W-L1: web vs registry")
    print("  W-L2: URL liveness    |  D-L1: data vs report  |  D-L2: data vs HF resample\n")


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
        "quotes": {"level1_vs_yaml": [], "level2_vs_pdf": []},
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

    # === Web L1: scoring vs registry ===
    if region_yaml_path.exists():
        result["web_sources"]["level1_vs_registry"] = verify_web_l1(
            scoring, region_yaml_path)

    # === Web L2: HTTP liveness ===
    if not skip_web and result["web_sources"]["level1_vs_registry"]:
        result["web_sources"]["level2_liveness"] = verify_web_l2(
            result["web_sources"]["level1_vs_registry"])

    # === Dataset L1: scoring vs report ===
    result["dataset"]["level1_vs_report"] = verify_dataset_l1(
        scoring, report_path if report_path.exists() else None)

    # === Dataset L2: HF re-sampling ===
    if not skip_hf and result["dataset"]["level1_vs_report"]:
        result["dataset"]["level2_vs_hf"] = verify_dataset_l2(
            scoring, report_path if report_path.exists() else None,
            assessment_dir)

    result["summary"] = compute_summary(result)
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
