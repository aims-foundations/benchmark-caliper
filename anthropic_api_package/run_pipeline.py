#!/usr/bin/env python3
"""Orchestrate the full validity analysis pipeline on a benchmark paper PDF.

Usage:
    python run_pipeline.py <pdf_path> [--persona PID] [--use-case PATH] [--no-web-search]

Pipeline stages (costs kept in line with cli_package by routing each step to the
cheapest sufficient model). Elicitation runs EARLY (Steps 1-2) so the user
provides deployment context within ~30 seconds, then heavy processing follows.

    Step 0              Haiku derives the assessment slug from the deployment description
    Step 1              Haiku extracts lightweight metadata from pages 1-2
    Step 2-questions    Sonnet generates elicitation questions (uses metadata, not full YAML)
    Step 2-summary      Sonnet summarizes the answered questions
    Step 3a-extract     split PDF -> Haiku per-page (parallel, cached)
    Step 3a-assemble    Haiku cross-page merge + script assembles Quote Registry
    Step 3a-consolidate Sonnet writes Narrative Context given registry
    Step 3b-select      Haiku picks 1-2 reference benchmark YAMLs
    Step 3b-synthesize  Sonnet writes the benchmark YAML (+ coverage_gap_analysis)
    Step 3c-verify      verify_quotes.py (script, no API)
    Step 4a-template    Haiku picks 1-2 base region templates
    Step 4b-synthesize  Sonnet writes the assessment-specific region YAML
    Step 5              Sonnet + web_search_20250305 server tool -> region enrichment
    Step 5b             Dataset analysis scripts + Sonnet interpretation (conditional)
    Step 6              compose_prompt.py (script, embeds DA findings if present)
    Step 7              Opus scoring (the one Opus call in the pipeline)
    Step 8              format_results.py (script)

All deployment-scoped outputs land under `assessments/<name>/<slug>/`
(elicitation artifacts, region YAML, composed prompt, scoring, cost ledger,
traces). Paper-scoped outputs live under `papers/<name>/`. The slug is
derived once up front from the deployment description; remove
`assessments/<name>/active_slug.txt` to force a new assessment identity
(prior slug dirs stick around for comparison).

Exactly one Opus call. Sonnet for synthesis/judgment-heavy steps. Haiku for
extraction/selection. All prompts live in prompts/*.md; see prompts.py.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import yaml

try:
    from tqdm import tqdm
except ImportError:
    # Graceful no-op so the file runs on envs that didn't install tqdm
    def tqdm(iterable, **kwargs):
        return iterable

import client
import prompts
from personas import PERSONAS


ROOT = Path(__file__).parent
SCRIPTS = ROOT / "scripts"
FRAMEWORK = ROOT / "framework.yaml"   # validity dimension definitions, read by compose_prompt.py

# === Directory layout ===
# papers/<name>/              — paper-scoped, stable across assessment re-runs
# page_caches/<name>/         — per-page Haiku extraction cache (skipped on crash-resume)
# benchmarks/                 — synthesized benchmark YAML + reference examples
# regions/base/               — canonical regional context templates
# assessments/<name>/<slug>/  — deployment-scoped artifacts (one dir per persona/use-case)
PAPERS = ROOT / "papers"
PAGE_CACHES = ROOT / "page_caches"
BENCHMARKS = ROOT / "benchmarks"
BENCHMARK_EXAMPLES = BENCHMARKS / "examples"
REGIONS_BASE = ROOT / "regions" / "base"
ASSESSMENTS = ROOT / "assessments"


# ===================================================================
# Helpers
# ===================================================================

# Runs any script under scripts/ as a subprocess and returns its stdout;
# hard-exits on non-zero so callers don't need to propagate return codes.
def _run_script(script: str, *args: str, stdin: str | None = None) -> str:
    """Run a script from scripts/ and return stdout; fail loud on non-zero exit."""
    path = SCRIPTS / script
    if script.endswith(".py"):
        cmd = ["python3", str(path), *args]
    elif script.endswith(".sh"):
        cmd = ["bash", str(path), *args]
    else:
        cmd = [str(path), *args]
    result = subprocess.run(cmd, input=stdin, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {script} failed (exit {result.returncode})", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout


# Parse an LLM response that may have markdown fences; returns a Python object.
# Delegates to parse_llm_output.py rather than inlining the fence-stripping logic
# so all callers handle edge cases (nested fences, leading prose) identically.
def _parse_fenced(raw: str, fmt: str) -> Any:
    """Strip markdown fences and parse; fmt is 'json' or 'yaml'. Returns a Python object."""
    cleaned = _run_script("parse_llm_output.py", "--format", fmt, "-", stdin=raw)
    return json.loads(cleaned) if fmt == "json" else yaml.safe_load(cleaned)


def _example_manifest() -> str:
    """Build a one-line-per-file manifest of benchmarks/examples/ for Haiku selection.

    Produces a compact, token-efficient listing so Haiku can pick analogous
    examples by domain/strategy/region without reading full YAML files.
    """
    lines = []
    for path in sorted(BENCHMARK_EXAMPLES.glob("*.yaml")):
        data = yaml.safe_load(path.read_text()) or {}
        domain = data.get("domain", "?")
        strategy = data.get("porting_strategy", "?")
        region = data.get("primary_region", "?")
        lines.append(
            f"{path.name} | domain: {domain} | porting_strategy: {strategy} | primary_region: {region}"
        )
    return "\n".join(lines)


# Returns sorted filenames only — Haiku sees the list and picks by name;
# the actual YAML content is loaded later in 4b-synthesize.
def _list_base_templates() -> list[str]:
    """Return sorted filenames of all base region templates (names only, not content)."""
    return sorted(p.name for p in REGIONS_BASE.glob("*.yaml"))


def _read_yaml_file(filename: str, subdir: Path) -> str:
    """Read a YAML file from subdir and return raw text (not parsed)."""
    return (subdir / filename).read_text()


# ===================================================================
# Path helpers — two scopes:
#   - PAPER-scoped  (papers/<name>/*):        inputs + paper-derived artifacts
#   - ASSESSMENT-scoped (assessments/<name>/<slug>/*): everything deployment-specific
# Re-deriving a slug (new persona) creates a fresh assessment dir alongside
# the old one; the `active_slug.txt` pointer names the "current" assessment.
# ===================================================================

# --- Paper-scoped paths (shared across all assessments of the same paper) ---

def _paper_dir(name: str) -> Path:
    """Root directory for all paper-scoped artifacts (papers/<name>/)."""
    return PAPERS / name


# Lightweight benchmark metadata (title, domain, languages, region) written by Step 1
def _metadata_path(name: str) -> Path:
    return _paper_dir(name) / "metadata.md"


# Full paper summary: Sonnet narrative + appended Quote Registry
# Tuple-scoped: each deployment context gets its own summary (elicitation
# guides narrative depth), stored in the assessment directory.
def _paper_summary_path(name: str, slug: str = "") -> Path:
    if slug:
        return _assessment_dir(name, slug) / "paper_summary.md"
    return _paper_dir(name) / "paper_summary.md"


# Mechanically-assembled verbatim quote table — authoritative source for 3b quote backfill
def _quote_registry_path(name: str) -> Path:
    return _paper_dir(name) / "quote_registry.md"


# JSON list of selected benchmark example filenames, written by 3b-select
def _benchmark_refs_path(name: str) -> Path:
    return _paper_dir(name) / "benchmark_refs.json"


# --- Assessment-scoped paths (unique per deployment persona / use-case) ---

def _assessments_root(name: str) -> Path:
    """Parent of all slug-specific assessment dirs for a given paper."""
    return ASSESSMENTS / name


# Pointer to the current active assessment slug; removing this forces a new slug on next run
def _active_slug_path(name: str) -> Path:
    return _assessments_root(name) / "active_slug.txt"


def _assessment_dir(name: str, slug: str) -> Path:
    """Root directory for a single deployment assessment (assessments/<name>/<slug>/)."""
    return _assessments_root(name) / slug


# Free-text description of the deployment context, persisted so re-runs don't re-prompt
def _deployment_desc_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "deployment_description.txt"


# Structured JSON array of elicitation questions written by Step 2-questions
def _questions_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "elicitation_questions.json"


# Q&A responses: either typed interactively (stdin) or produced by CC Opus subagent
def _answers_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "elicitation_answers.json"


# Handoff document for the CC Opus subagent in persona mode (not used in stdin mode)
def _persona_prompt_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "persona_prompt.md"


# Sonnet-synthesized summary of the Q&A — priority weights, cultural topics, etc.
def _elicitation_summary_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "elicitation_summary.md"


# JSON list of selected base region template filenames, written by 4a-template
def _region_templates_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "region_templates.json"


# Initial region YAML from 4b (unverified slots marked [NEEDS VERIFICATION])
def _region_scaffold_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "region_scaffold.yaml"


# Final region YAML after web-search enrichment (Step 5 overwrites this from scaffold)
def _region_yaml_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "region.yaml"


# Sonnet interpretation of HuggingFace dataset content, written by Step 5b
def _da_report_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "dataset_analysis_report.md"


# Assembled evaluation prompt: benchmark YAML + region YAML + framework + elicitation context
def _composed_prompt_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "composed_prompt.md"


# Opus scoring output: structured JSON with per-dimension scores and rationale
def _scoring_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "scoring.json"


# Running cost ledger: accumulates per-step API usage, survives between re-runs
def _cost_ledger_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "cost_ledger.json"


# Per-step API call traces (JSONL), used for crash-resume and cost accounting
def _trace_dir(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "traces"


def _read_slug(name: str) -> str | None:
    """Return the active assessment slug from disk, or None if not yet derived."""
    p = _active_slug_path(name)
    return p.read_text().strip() if p.exists() else None


def _parse_quote_registry(name: str) -> dict[str, str]:
    """Parse the Quote Registry markdown table into {Q_id: text}.

    Registry rows look like: | Q1 | 20 | task_taxonomy | "verbatim text" |

    Used to backfill quote text into the benchmark YAML after Sonnet synthesis —
    Sonnet only emits (id, page, dimension) to avoid transcription errors and
    reduce output tokens; the authoritative text comes from this mechanical table.
    """
    registry_path = _quote_registry_path(name)
    if not registry_path.exists():
        return {}
    id_to_text: dict[str, str] = {}
    for line in registry_path.read_text().splitlines():
        # Match the strict pipe-delimited table format: | Q{n} | {page} | {category} | "{text}" |
        m = re.match(
            r'^\|\s*(Q\d+)\s*\|\s*\d+\s*\|\s*\w+\s*\|\s*"(.+)"\s*\|$',
            line,
        )
        if m:
            # Unescape pipe characters that were escaped to avoid breaking the table format
            id_to_text[m.group(1)] = m.group(2).replace("\\|", "|")
    return id_to_text


# ===================================================================
# Step 0 — Derive the assessment slug from the deployment description
# ===================================================================

def step_0_derive_slug(initial_description: str, name: str) -> str:
    """Haiku derives a short, filesystem-safe slug from the deployment description.

    Idempotent: if active_slug.txt already exists on disk for this paper, the
    cached slug is returned immediately without a new API call. Returns the slug
    string that scopes all downstream assessment-dir paths.
    """
    existing = _read_slug(name)
    if existing:
        # Slug already exists on disk — idempotent, so subsequent --step invocations
        # always land in the same assessment directory.
        print(f"[0] Using cached slug: {existing}")
        return existing

    print("[0] Haiku deriving assessment slug from deployment description...")
    slug_raw = client.call(
        model="haiku",
        system=prompts.load("slug_from_description"),
        user=initial_description,
        max_tokens=64,
        step="0_slug",
    ).strip()
    # Sanitize to lowercase alphanumerics + underscores; truncate to keep paths sane.
    # The `or "unknown"` guard handles the pathological case where Haiku returns
    # only punctuation that gets stripped to empty string.
    slug = re.sub(
        r"[^a-z0-9_]", "",
        slug_raw.lower().replace(" ", "_").replace("-", "_"),
    )[:60] or "unknown"
    # Dry-run: don't persist the placeholder as a real slug — it would poison
    # active_slug.txt and short-circuit every subsequent real --step 0.
    if client.DRY_RUN:
        print(f"[0] (dry-run) would write slug: {slug}")
        return slug
    # Create the assessment dir and persist both the description (now
    # assessment-scoped so multiple deployments per paper don't clobber) and
    # the active_slug pointer that subsequent --step invocations read.
    assess = _assessment_dir(name, slug)
    assess.mkdir(parents=True, exist_ok=True)
    _deployment_desc_path(name, slug).write_text(initial_description)
    _active_slug_path(name).write_text(slug)
    print(f"[0] Slug: {slug}")
    return slug


# ===================================================================
# Step 1 — Quick metadata extraction (Haiku, pages 1-2 only)
# ===================================================================
# Runs early so Step 2 (elicitation) can generate targeted questions
# from lightweight metadata without waiting for the full PDF extraction.

def step_1_metadata(pdf_path: Path, name: str) -> Path:
    """Haiku reads pages 1-2 of the PDF and returns lightweight metadata.

    Caches to papers/<name>/metadata.md so subsequent re-runs are instant.
    Returns the metadata file path.
    """
    _paper_dir(name).mkdir(parents=True, exist_ok=True)
    out_path = _metadata_path(name)

    if out_path.exists():
        print(f"[1] Using cached metadata: {out_path}")
        return out_path

    # === Extract pages 1-2 into a temp PDF ===
    with tempfile.TemporaryDirectory() as tmp:
        pages_dir = Path(tmp) / "pages"
        pages_dir.mkdir()
        _run_script("split_pdf.sh", str(pdf_path), str(pages_dir))
        front_pages: list[Path] = []
        for i in (1, 2):
            p = pages_dir / f"page_{i:03d}.pdf"
            if p.exists():
                front_pages.append(p)

        if not front_pages:
            print("ERROR: split_pdf.sh produced no page files", file=sys.stderr)
            sys.exit(1)

        # Merge pages 1-2 back into a single small PDF for the API call.
        # Single-page papers (cover-only PDFs) produce only one file — skip merge.
        if len(front_pages) == 1:
            front_pdf = front_pages[0]
        else:
            front_pdf = Path(tmp) / "front.pdf"
            _merge_pages(front_pages, front_pdf)

        print("[1] Haiku extracting metadata from pages 1-2...")
        metadata = client.call(
            model="haiku",
            system=prompts.load("metadata_extract"),
            user="Extract metadata from the attached benchmark paper (pages 1-2).",
            pdf_path=str(front_pdf),
            max_tokens=1024,
            step="1_metadata",
        )

    if client.DRY_RUN:
        return out_path
    out_path.write_text(metadata)
    print(f"[1] Metadata written to {out_path}")
    return out_path


def _merge_pages(page_paths: list[Path], out_path: Path) -> None:
    """Merge a small set of single-page PDFs into one file.

    Falls back through three tools (pdftk -> qpdf -> pypdf) to handle
    environments where only a subset is installed.
    """
    args = [str(p) for p in page_paths]
    # Try pdftk first (fastest), then qpdf (widely available on Linux), then pypdf
    if _which("pdftk"):
        subprocess.run(["pdftk", *args, "cat", "output", str(out_path)],
                        check=True, capture_output=True)
    elif _which("qpdf"):
        subprocess.run(["qpdf", "--empty", "--pages", *args, "--",
                        str(out_path)], check=True, capture_output=True)
    else:
        # pypdf fallback
        subprocess.run(
            ["python3", "-c",
             f"from pypdf import PdfReader,PdfWriter; "
             f"w=PdfWriter(); "
             f"[w.add_page(p) for f in {[str(p) for p in page_paths]} for p in PdfReader(f).pages]; "
             f"w.write('{out_path}')"],
            check=True, capture_output=True,
        )


# Thin wrapper so callers don't need to import shutil inline
def _which(cmd: str) -> bool:
    """Return True if cmd is available on PATH."""
    from shutil import which
    return which(cmd) is not None


# ===================================================================
# Step 3a — PDF extraction: Haiku per-page (3a-extract) + Haiku merge + script
#           registry (3a-assemble) + Sonnet narrative (3a-consolidate)
# ===================================================================

def step_1a_extract(pdf_path: Path, name: str, max_workers: int = 1) -> Path:
    """Per-page Haiku extraction with on-disk caching (implements step 3a-extract).

    NOTE: Named step_1a_extract for legacy reasons; this is step 3a-extract in the
    pipeline numbering. The name predates the step renumbering that moved elicitation
    earlier.

    Each successful page extraction is written to
    `page_caches/<name>/page_NNN.txt` immediately. On re-run (e.g. after a
    rate-limit crash), cached pages are skipped — only the missing ones are
    dispatched. Returns the cache directory.

    `max_workers=1` by default: at ~3-5k input tokens per page and ~5s per
    Haiku call, serial dispatch yields ~12 calls/min ≈ 40k TPM, which stays
    under the lowest common personal-tier cap (50k TPM for Haiku). Bump it
    if you have a higher tier — total wall-clock for 30 pages at 1 worker
    is ~2-3 minutes.
    """
    _paper_dir(name).mkdir(parents=True, exist_ok=True)
    cache_dir = PAGE_CACHES / name
    cache_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        pages_dir = Path(tmp) / "pages"
        pages_dir.mkdir()
        _run_script("split_pdf.sh", str(pdf_path), str(pages_dir))
        page_files = sorted(pages_dir.glob("page_*.pdf"))
        if not page_files:
            print("ERROR: split_pdf.sh produced no page files", file=sys.stderr)
            sys.exit(1)

        # === Determine which pages still need extraction ===
        # Page files that already have a cached .txt are skipped — this makes
        # the step safe to retry after rate-limit crashes without re-paying for
        # already-extracted pages.
        total = len(page_files)
        todo: list[tuple[int, Path, Path]] = []
        for i, page_pdf in enumerate(page_files, start=1):
            cache_file = cache_dir / f"page_{i:03d}.txt"
            if not cache_file.exists():
                todo.append((i, page_pdf, cache_file))
        cached = total - len(todo)
        if cached:
            print(f"[3a-extract] {cached}/{total} pages cached from prior run; "
                  f"re-dispatching {len(todo)}.")
        else:
            # Fresh fan-out: drop any stale 3a_extract ledger + trace entries
            # so the cost of this run's pages replaces whatever was there.
            client.clear_steps("3a_extract")
            client.clear_trace_steps("3a_extract")
            print(f"[3a-extract] Split into {total} pages; extracting via Haiku "
                  f"(max_workers={max_workers})...")

        # === Fan-out: dispatch remaining pages to Haiku in parallel ===
        def _process(page_num: int, page_pdf: Path, cache_file: Path) -> None:
            text = client.call(
                model="haiku",
                system=prompts.render("pdf_extract_page", page_num=page_num),
                user=f"Extract validity-relevant content from page {page_num}.",
                pdf_path=str(page_pdf),
                max_tokens=8192,
                step="3a_extract",
            )
            # Write cache immediately on success — if a later page crashes, the
            # next re-run skips this page. Skipped in dry-run to avoid poisoning
            # the cache with placeholder text.
            if not client.DRY_RUN:
                cache_file.write_text(text)

        if todo:
            with ThreadPoolExecutor(max_workers=max_workers) as ex:
                futures = [ex.submit(_process, i, pp, cf) for i, pp, cf in todo]
                for fut in tqdm(as_completed(futures), total=len(futures), desc="Haiku pages"):
                    fut.result()  # re-raise any exception from the worker thread

    print(f"[3a-extract] Page cache at {cache_dir}")
    return cache_dir


def _parse_page_json(raw_text: str) -> dict:
    """Best-effort parse of a per-page Haiku extraction response (may have markdown fences).

    Returns a safe empty skeleton if parsing fails — a bad page is dropped
    rather than crashing the whole assemble step.
    """
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]  # drop opening fence line (e.g. ```json)
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Haiku occasionally returns a short explanation instead of JSON;
        # return a safe skeleton so assemble continues without crashing.
        return {"quotes": [], "page_summary": "", "continues_from_previous": False,
                "continues_to_next": False}


def step_3a_assemble(name: str) -> Path:
    """Merge cross-page quotes (Haiku), then mechanically assemble the Quote Registry.

    1. Read per-page JSONs from the page cache
    2. Identify cross-page sentence boundaries
    3. Call Haiku once per boundary to merge split sentences
    4. Collect all quotes, apply merges, deduplicate
    5. Assign sequential Q1..QN IDs in page order
    6. Write Quote Registry + Category Index markdown

    Returns the path to the written quote_registry.md.
    """
    cache_dir = PAGE_CACHES / name
    registry_path = _quote_registry_path(name)
    if registry_path.exists():
        print(f"[3a-assemble] Quote registry already exists: {registry_path}")
        return registry_path
    _paper_dir(name).mkdir(parents=True, exist_ok=True)

    page_files = sorted(cache_dir.glob("page_*.txt"))
    if not page_files:
        print(f"ERROR: no page cache at {cache_dir}. Run --step 3a-extract first.",
              file=sys.stderr)
        sys.exit(1)

    pages = [(int(p.stem.split("_")[1]), _parse_page_json(p.read_text()))
             for p in page_files]
    pages.sort(key=lambda x: x[0])

    # === Phase 1: Identify and merge cross-page sentence splits ===
    # Haiku flags each page with continues_to_next / continues_from_previous.
    # When both sides agree a boundary exists, Haiku merges the last quote of
    # page A with the first quote of page B. The merge prompt returns either
    # the joined text or the word "SEPARATE" if the fragments are unrelated.
    merge_results = {}  # (page_a, page_b) -> merged_text or None
    merge_pairs = []
    for i in range(len(pages) - 1):
        page_a_num, page_a = pages[i]
        page_b_num, page_b = pages[i + 1]
        if page_a.get("continues_to_next") and page_b.get("continues_from_previous"):
            quotes_a = page_a.get("quotes", [])
            quotes_b = page_b.get("quotes", [])
            if quotes_a and quotes_b:
                merge_pairs.append((page_a_num, page_b_num,
                                    quotes_a[-1], quotes_b[0]))

    if merge_pairs:
        print(f"[3a-assemble] {len(merge_pairs)} cross-page boundaries to merge (Haiku)...")
        merge_prompt = prompts.load("cross_page_merge")
        for page_a_num, page_b_num, frag_a, frag_b in tqdm(merge_pairs, desc="Merging"):
            result = client.call(
                model="haiku",
                system=merge_prompt,
                user=(
                    f"Fragment A (end of page {page_a_num}):\n"
                    f"\"{frag_a['text']}\"\n\n"
                    f"Fragment B (start of page {page_b_num}):\n"
                    f"\"{frag_b['text']}\""
                ),
                max_tokens=512,
                step="3a_merge",
            )
            if client.DRY_RUN:
                continue
            stripped = result.strip()
            # Haiku responds with "SEPARATE" when the two fragments don't belong
            # together (e.g. a sentence ends naturally at the page break).
            if stripped.upper().startswith("SEPARATE"):
                merge_results[(page_a_num, page_b_num)] = None
            else:
                # Strip outer quotes that Haiku sometimes wraps the merged text in
                merge_results[(page_a_num, page_b_num)] = stripped.strip('"')
                print(f"    pages {page_a_num}-{page_b_num}: merged")
    else:
        print("[3a-assemble] No cross-page boundaries found.")

    # === Phase 2: collect all quotes, apply merges, deduplicate ===
    # Walk pages in order, substituting merged text where applicable and
    # dropping the "consumed" first quote of any page whose boundary was merged.
    all_quotes = []
    # Track which pages had their first quote absorbed into the prior page's last quote
    skip_next_first = set()  # page numbers whose first quote was merged into prior page

    for page_a_num, page_b_num, _, _ in merge_pairs:
        merged = merge_results.get((page_a_num, page_b_num))
        if merged is not None:
            skip_next_first.add(page_b_num)

    for page_num, page_data in pages:
        for qi, q in enumerate(page_data.get("quotes", [])):
            # This quote was consumed by a successful cross-page merge — skip it
            if qi == 0 and page_num in skip_next_first:
                continue

            text = q.get("text", "").strip()
            if not text:
                continue

            # If this is the last quote on a page and its boundary was merged,
            # replace it with the merged text so the full sentence is preserved.
            is_last = (qi == len(page_data.get("quotes", [])) - 1)
            merged_into = None
            if is_last:
                for pa, pb, _, _ in merge_pairs:
                    if pa == page_num:
                        merged_into = merge_results.get((pa, pb))
                        break

            if merged_into is not None:
                all_quotes.append({
                    "text": merged_into,
                    "page": page_num,
                    "category": q.get("category", ""),
                })
            else:
                all_quotes.append({
                    "text": text,
                    "page": page_num,
                    "category": q.get("category", ""),
                })

    # Deduplicate by normalized text — Haiku sometimes emits the same sentence
    # from adjacent pages when a quote appears in both a figure and the body text.
    seen_texts = set()
    deduped = []
    for q in all_quotes:
        normalized = q["text"].strip().lower()
        if normalized not in seen_texts:
            seen_texts.add(normalized)
            deduped.append(q)
    removed = len(all_quotes) - len(deduped)
    if removed:
        print(f"[3a-assemble] Removed {removed} duplicate quotes.")
    all_quotes = deduped

    # === Phase 3: assign IDs and build registry markdown ===
    # The Category Index at the end lets Sonnet (3b-synthesize) quickly find all
    # quotes for a given validity dimension without scanning the full table.
    categories = [
        "task_taxonomy", "data_sources", "data_format", "label_categories",
        "annotation_process", "evaluation_metrics", "stated_limitations",
        "authors_affiliations",
    ]
    cat_index: dict[str, list[str]] = {c: [] for c in categories}

    lines = [
        "---",
        "",
        "## Quote Registry",
        "",
        "**This section is authoritative.** Every entry is verbatim text from the paper.",
        "",
        "| ID | Page | Category | Text |",
        "|----|------|----------|------|",
    ]
    for i, q in enumerate(all_quotes, 1):
        qid = f"Q{i}"
        cat = q["category"]
        # Escape pipes inside quote text to avoid breaking the markdown table
        text_escaped = q["text"].replace("|", "\\|").replace("\n", " ")
        lines.append(f'| {qid} | {q["page"]} | {cat} | "{text_escaped}" |')
        if cat in cat_index:
            cat_index[cat].append(qid)

    lines.append("")
    lines.append("### Category Index")
    for cat in categories:
        ids = cat_index[cat]
        if ids:
            lines.append(f"- **{cat}**: {', '.join(ids)}")
        else:
            # Explicit "NO QUOTES" entry makes coverage gaps visible in the registry
            lines.append(f'- **{cat}**: NO QUOTES — paper is silent')

    registry_text = "\n".join(lines) + "\n"

    if not client.DRY_RUN:
        registry_path.write_text(registry_text)
    print(f"[3a-assemble] {len(all_quotes)} quotes in registry "
          f"({len(merge_pairs)} merges, {removed} deduped) -> {registry_path}")
    return registry_path


def step_3a_consolidate(name: str, elicitation_summary: str = "",
                        slug: str = "") -> Path:
    """Sonnet writes Narrative Context given the pre-assembled Quote Registry.

    The registry (from step_3a_assemble) is provided as input. Sonnet writes
    only the Metadata + Narrative Context sections. The final paper_summary.md
    is produced by concatenating Sonnet's output with the registry.

    When an elicitation summary is provided, it guides narrative depth:
    HIGH-priority dimensions get more detailed narrative.

    Returns path to the written paper_summary.md.
    """
    _paper_dir(name).mkdir(parents=True, exist_ok=True)
    summary_path = _paper_summary_path(name, slug)
    if summary_path.exists():
        print(f"[3a-consolidate] Paper summary already exists: {summary_path}")
        return summary_path
    registry_path = _quote_registry_path(name)

    if not registry_path.exists():
        print(f"ERROR: {registry_path} not found. Run --step 3a-assemble first.",
              file=sys.stderr)
        sys.exit(1)

    registry_text = registry_path.read_text()

    user_msg = f"## Pre-Assembled Quote Registry\n\n{registry_text}"
    if elicitation_summary:
        # Inject priority weights so Sonnet allocates narrative depth proportionally
        # to what the deployment cares about rather than treating all dimensions equally.
        user_msg += (
            f"\n\n---\n\n"
            f"## Elicitation Summary (for narrative depth guidance)\n\n"
            f"{elicitation_summary}\n\n"
            f"Use the Dimension Priority Weights above to guide narrative depth:\n"
            f"- HIGH-priority dimensions: 4-6 sentences of narrative context\n"
            f"- MODERATE-priority dimensions: 2-4 sentences\n"
            f"- LOWER-priority dimensions: 1-2 sentences\n\n"
            f"Cultural topic priorities from the summary should receive extra "
            f"attention — call out related quotes even if they would otherwise "
            f"be treated as minor details."
        )

    print(f"[3a-consolidate] Sonnet writing narrative context...")
    narrative = client.call(
        model="sonnet",
        system=prompts.load("pdf_extract_consolidate"),
        user=user_msg,
        max_tokens=16384,
        step="3a_consolidate",
    )

    # Concatenate Sonnet's narrative + mechanical registry
    full_summary = narrative.rstrip() + "\n\n" + registry_text
    summary_path.write_text(full_summary)
    print(f"[3a-consolidate] Paper summary written to {summary_path}")
    return summary_path


# ===================================================================
# Step 3b — Benchmark YAML: Haiku selection (3b-select) + Sonnet synthesis (3b-synthesize)
# ===================================================================

def step_3b_select(paper_summary: str, name: str) -> list[str]:
    """Haiku picks 1-2 reference benchmark YAMLs from benchmarks/examples/; persisted for 3b-synthesize.

    Returns the list of selected example filenames (e.g. ['afrisenti.yaml']).
    """
    refs_path = _benchmark_refs_path(name)
    if refs_path.exists():
        selected = json.loads(refs_path.read_text())
        print(f"[3b-select] Benchmark refs already exist: {selected}")
        return selected
    _paper_dir(name).mkdir(parents=True, exist_ok=True)
    print("[3b-select] Haiku selecting reference benchmark examples...")
    selection_raw = client.call(
        model="haiku",
        system=prompts.load("benchmark_example_selection"),
        user=(
            f"Benchmark example manifest:\n\n{_example_manifest()}\n\n"
            f"Paper summary:\n\n{paper_summary}"
        ),
        max_tokens=512,
        step="3b_select",
    )
    if client.DRY_RUN:
        return []
    selected_files = _parse_fenced(selection_raw, "json")
    _benchmark_refs_path(name).write_text(json.dumps(selected_files))
    print(f"[3b-select] Selected references: {selected_files}")
    return selected_files


def step_3b_synthesize(
    paper_summary: str,
    name: str,
    elicitation_summary: str = "",
    slug: str = "",
) -> Path:
    """Sonnet writes the benchmark YAML from selected references + elicitation context.

    When an elicitation summary is provided, the YAML includes
    coverage_strengths and coverage_gap_analysis sections cross-referencing
    user priorities against benchmark documentation. Quote text is backfilled
    from the mechanical registry after synthesis to avoid LLM transcription
    errors.

    Tuple-scoped: each deployment context gets its own YAML (coverage
    analysis depends on elicitation priorities). Stored in the assessment
    directory when slug is provided.
    """
    if slug:
        out_path = _assessment_dir(name, slug) / "benchmark.yaml"
    else:
        out_path = BENCHMARKS / f"{name}.yaml"
    if out_path.exists():
        print(f"[3b-synthesize] Benchmark YAML already exists: {out_path}")
        return out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    refs_path = _benchmark_refs_path(name)
    if not refs_path.exists() and not client.DRY_RUN:
        print(
            f"ERROR: {refs_path} not found — run --step 3b-select first.",
            file=sys.stderr,
        )
        sys.exit(1)
    selected_files: list[str] = json.loads(refs_path.read_text()) if refs_path.exists() else []
    # Embed full YAML of each selected example so Sonnet can mimic the schema
    examples_text = "\n\n".join(
        f"### Example: {fn}\n\n```yaml\n{_read_yaml_file(fn, BENCHMARK_EXAMPLES)}\n```"
        for fn in selected_files
    )

    user_msg = f"Reference examples:\n\n{examples_text}\n\nPaper summary:\n\n{paper_summary}"
    if elicitation_summary:
        user_msg += (
            f"\n\n---\n\n"
            f"## Elicitation Summary\n\n{elicitation_summary}\n\n"
            f"Use the dimension priority weights and cultural topic priorities "
            f"above when writing the coverage_strengths and "
            f"coverage_gap_analysis sections. For each HIGH-priority dimension "
            f"and each cultural topic priority, assess whether the benchmark "
            f"documents relevant content — noting both where coverage aligns "
            f"well and where it diverges."
        )

    print("[3b-synthesize] Sonnet synthesizing benchmark YAML...")
    synthesis_raw = client.call(
        model="sonnet",
        system=prompts.load("benchmark_synthesis"),
        user=user_msg,
        max_tokens=32768,
        step="3b_synthesize",
    )
    if client.DRY_RUN:
        return out_path
    cleaned = _run_script("parse_llm_output.py", "--format", "yaml", "-", stdin=synthesis_raw)

    # === Backfill verbatim_quotes text from the mechanically-assembled registry ===
    # Sonnet only emits id/page/dimension; the text is filled in here to avoid
    # LLM copying errors and reduce output tokens.
    id_to_text = _parse_quote_registry(name)
    if id_to_text:
        data = yaml.safe_load(cleaned)
        missing_ids = []
        for q in data.get("verbatim_quotes", []):
            qid = q.get("id", "")
            if qid in id_to_text:
                q["text"] = id_to_text[qid]
            else:
                missing_ids.append(qid)
        if missing_ids:
            print(f"  WARN: {len(missing_ids)} quote IDs not found in registry: "
                  f"{', '.join(missing_ids[:5])}", file=sys.stderr)
        cleaned = yaml.dump(data, sort_keys=False, allow_unicode=True,
                            default_flow_style=False, width=120)

    out_path.write_text(cleaned)
    print(f"[3b-synthesize] Benchmark YAML written to {out_path}")
    return out_path


# ===================================================================
# Step 3c — Quote provenance: mechanical verify (3c-verify)
# ===================================================================

def step_3c_verify(
    benchmark_path: Path,
    summary_path: Path,
    strict: bool = False,
) -> bool:
    """Mechanical check: counts, IDs, dimension coverage. No API call.

    Returns True if all checks passed. On failure:
      - strict=True:  halt the pipeline (sys.exit with the script's exit code).
      - strict=False: print the failure report and return False, so the caller
                      can decide what to do. Default for user-facing runs — a
                      single Sonnet formatting slip shouldn't burn the whole run.
    """
    print("[3c-verify] Running mechanical verification (verify_quotes.py)...")
    cmd = ["python3", str(SCRIPTS / "verify_quotes.py"),
           str(benchmark_path), str(summary_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode == 0:
        return True
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if strict:
        print(f"ERROR: verify_quotes.py failed (exit {result.returncode}). "
              f"Re-run without --strict-verify to continue past this gate.",
              file=sys.stderr)
        sys.exit(result.returncode)
    print("[3c-verify] WARNING: mechanical check failed but --strict-verify is "
          "off; continuing. Inspect the report above and consider re-running "
          "3a-consolidate / 3b-synthesize if the issues look substantive.",
          file=sys.stderr)
    return False


# ===================================================================
# Step 2 — Elicitation (questions + answers + summary)
# ===================================================================
# Runs EARLY — right after metadata extraction, before heavy PDF
# processing. The user provides deployment context within the first
# minute, then can walk away while the pipeline runs.
#
# The persona branch no longer makes an API call. Instead, step_2_questions
# emits an `assessments/<name>/<slug>/persona_prompt.md` that the user hands
# to a Claude Code Opus subagent. The subagent's JSON reply is saved to
# `assessments/<name>/<slug>/elicitation_answers.json`, and step_2_summary
# consumes it.
# The stdin (no-persona) path collects answers inline and continues.

def step_2_questions(
    metadata_text: str,
    initial_description: str,
    persona_id: str | None,
    name: str,
    slug: str,
) -> tuple[Path, Path | None]:
    """Generate the elicitation question array and (for personas) the CC handoff prompt.

    Receives lightweight metadata (from Step 1), not the full benchmark YAML.

    Returns (questions_path, persona_prompt_path or None). The persona prompt
    is what the caller hands to a Claude Code Opus subagent; the subagent's
    JSON reply should be saved to `_answers_path(name, slug)` before running
    the summary step.
    """
    _assessment_dir(name, slug).mkdir(parents=True, exist_ok=True)

    # === Generate the structured JSON question array (Sonnet) ===
    print("[2-questions] Sonnet generating elicitation questions...")
    questions_raw = client.call(
        model="sonnet",
        system=prompts.load("elicitation_questions"),
        user=(
            f"Benchmark metadata:\n\n{metadata_text}\n\n"
            f"Deployment description:\n\n{initial_description}"
        ),
        max_tokens=4096,
        step="2_questions",
    )
    q_path = _questions_path(name, slug)
    if client.DRY_RUN:
        return q_path, None
    questions_json = _run_script("parse_elicitation_questions.py", "-", stdin=questions_raw)
    questions = json.loads(questions_json)

    q_path.write_text(questions_json)
    _deployment_desc_path(name, slug).write_text(initial_description)
    print(f"[2-questions] {len(questions)} questions written to {q_path}")

    persona_prompt_path: Path | None = None
    if persona_id:
        # === Build handoff prompt for CC Opus subagent (persona mode) ===
        # Rather than calling the API here, we emit a self-contained markdown doc
        # the user drops into a CC Opus subagent. This keeps orchestration costs
        # low and allows the persona simulation to run asynchronously.
        persona = PERSONAS[persona_id]
        system_rendered = prompts.render(
            "persona_system", persona_block=persona["persona_block"]
        )
        answers_target = _answers_path(name, slug)
        persona_prompt_path = _persona_prompt_path(name, slug)
        persona_prompt_path.write_text(
            f"# Persona elicitation — hand this to a Claude Code Opus subagent\n\n"
            f"Persona: `{persona_id}`\n\n"
            f"Dispatch a Claude Code Opus subagent with the system prompt and user "
            f"message below. Save the subagent's JSON reply to:\n\n"
            f"    {answers_target}\n\n"
            f"Then resume the pipeline:\n\n"
            f"    python run_pipeline.py {name}.pdf --step 2-summary "
            f"--answers {answers_target}\n\n"
            f"---\n\n"
            f"## System prompt\n\n{system_rendered}\n\n"
            f"---\n\n"
            f"## User message\n\n"
            f"Questions:\n\n```json\n{json.dumps(questions, indent=2)}\n```\n"
        )
        print(f"[2-questions] Persona handoff prompt written to {persona_prompt_path}")

    return q_path, persona_prompt_path


def step_2_collect_stdin(name: str, slug: str) -> Path:
    """Interactive stdin path: prompt each elicitation question and write answers JSON.

    Used when running in non-persona mode. The user is prompted for each question
    in sequence; answers are persisted so step_2_summary can consume them.
    Returns the path to the written answers JSON.
    """
    q_path = _questions_path(name, slug)
    if not q_path.exists():
        print(f"ERROR: {q_path} not found — run step 2-questions first", file=sys.stderr)
        sys.exit(1)
    questions = json.loads(q_path.read_text())
    print("[2-stdin] Collecting answers interactively...")
    answers = {}
    for q in questions:
        print(f"\n{q['id']} [{q['dimension']}]: {q['question']}")
        answers[q["id"]] = input("> ").strip()
    a_path = _answers_path(name, slug)
    a_path.write_text(json.dumps(answers, indent=2))
    print(f"[2-stdin] Answers written to {a_path}")
    return a_path


def step_2_summary(
    name: str,
    slug: str,
    metadata_text: str,
    answers_path: Path | None = None,
) -> Path:
    """Sonnet synthesizes the Q&A into a structured elicitation summary.

    Reads questions + answers (from disk or the provided path), assembles a
    Q+A block via script, and has Sonnet produce dimension priority weights,
    cultural topic priorities, and deployment context notes. These feed into
    3a-consolidate, 3b-synthesize, 4a/4b, 5, and 5b as a shared context document.

    Returns path to the written elicitation_summary.md.
    """
    q_path = _questions_path(name, slug)
    if not q_path.exists():
        print(f"ERROR: {q_path} not found — run step 2-questions first", file=sys.stderr)
        sys.exit(1)
    a_path = Path(answers_path) if answers_path else _answers_path(name, slug)
    if not a_path.exists():
        print(
            f"ERROR: answers file {a_path} not found. For a persona run, dispatch "
            f"the CC Opus subagent using {_persona_prompt_path(name, slug)} and save "
            f"its JSON reply there. For interactive mode, run without --step first.",
            file=sys.stderr,
        )
        sys.exit(1)

    summary_path = _elicitation_summary_path(name, slug)
    if summary_path.exists():
        print(f"[2-summary] Elicitation summary already exists: {summary_path}")
        return summary_path

    desc_path = _deployment_desc_path(name, slug)
    initial_description = desc_path.read_text() if desc_path.exists() else ""

    # Assemble the formatted Q+A block for Sonnet's input
    qa_block = _run_script(
        "assemble_elicitation_answers.py",
        "--questions", str(q_path),
        "--answers", str(a_path),
    )

    print("[2-summary] Sonnet producing elicitation summary...")
    summary = client.call(
        model="sonnet",
        system=prompts.load("elicitation_summary"),
        user=(
            f"Deployment description:\n\n{initial_description}\n\n"
            f"Benchmark metadata:\n\n{metadata_text}\n\n"
            f"Questions & answers:\n\n{qa_block}"
        ),
        max_tokens=8192,
        step="2_summary",
    )
    summary_path.write_text(summary)
    print(f"[2-summary] Elicitation summary written to {summary_path}")
    return summary_path


# ===================================================================
# Step 4 — Region YAML: Haiku template selection (4a-template) + Sonnet synthesis (4b-synthesize)
# ===================================================================

def step_4a_template(elicitation_summary: str, name: str, slug: str) -> list[str]:
    """Haiku picks 1-2 base region templates from regions/base/; persisted for 4b-synthesize.

    The selection is based on the deployment context from the elicitation summary
    (geography, language community, cultural context). Returns selected filenames.
    """
    out_path = _region_templates_path(name, slug)
    if out_path.exists():
        selected = json.loads(out_path.read_text())
        print(f"[4a-template] Region templates already exist: {selected}")
        return selected
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print("[4a-template] Haiku selecting base region template(s)...")
    selection_raw = client.call(
        model="haiku",
        system=prompts.load("region_template_selection"),
        user=(
            f"Base template files:\n{chr(10).join(_list_base_templates())}\n\n"
            f"Elicitation summary:\n\n{elicitation_summary}"
        ),
        max_tokens=256,
        step="4a_template",
    )
    if client.DRY_RUN:
        return []
    selected = _parse_fenced(selection_raw, "json")
    out_path.write_text(json.dumps(selected))
    print(f"[4a-template] Selected templates: {selected}")
    return selected


def step_4b_synthesize(
    elicitation_summary: str,
    benchmark_yaml_text: str,
    name: str,
    slug: str,
) -> Path:
    """Sonnet writes the assessment-specific region YAML scaffold from selected templates.

    The scaffold uses [NEEDS VERIFICATION] placeholders for factual slots that
    Sonnet cannot confidently fill without tool access — Step 5 (web search)
    resolves these. Outputs to assessments/<name>/<slug>/region_scaffold.yaml.

    Returns path to the written scaffold.
    """
    out_path = _region_scaffold_path(name, slug)
    if out_path.exists():
        print(f"[4b-synthesize] Region scaffold already exists: {out_path}")
        return out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    refs_path = _region_templates_path(name, slug)
    if not refs_path.exists() and not client.DRY_RUN:
        print(
            f"ERROR: {refs_path} not found — run --step 4a-template first.",
            file=sys.stderr,
        )
        sys.exit(1)
    selected: list[str] = json.loads(refs_path.read_text()) if refs_path.exists() else []

    def _yaml_to_json_str(yaml_text: str) -> str:
        # Convert YAML to JSON for the prompt — models handle JSON more reliably
        # as structured data than YAML (fewer ambiguous indent-level interpretations).
        try:
            parsed = yaml.safe_load(yaml_text)
            return json.dumps(parsed, indent=2, ensure_ascii=False)
        except yaml.YAMLError as e:
            print(f"WARNING: YAML parse failed, inserting raw text: {e}",
                  file=sys.stderr)
            return yaml_text

    templates_text = "\n\n".join(
        f"### Template: {fn}\n\n```json\n{_yaml_to_json_str(_read_yaml_file(fn, REGIONS_BASE))}\n```"
        for fn in selected
    )
    benchmark_json = _yaml_to_json_str(benchmark_yaml_text)
    print("[4b-synthesize] Sonnet synthesizing region scaffold...")
    region_raw = client.call(
        model="sonnet",
        system=prompts.load("region_synthesis"),
        user=(
            f"Base templates:\n\n{templates_text}\n\n"
            f"Elicitation summary:\n\n{elicitation_summary}\n\n"
            f"Benchmark:\n\n```json\n{benchmark_json}\n```"
        ),
        max_tokens=16384,
        step="4b_synthesize",
    )
    if client.DRY_RUN:
        return out_path
    # Parse JSON output then re-serialize as YAML for the canonical on-disk format
    cleaned_json = _run_script("parse_llm_output.py", "--format", "json", "-", stdin=region_raw)
    parsed = json.loads(cleaned_json)
    as_yaml = yaml.dump(parsed, sort_keys=False, allow_unicode=True,
                        default_flow_style=False)
    out_path.write_text(as_yaml)
    print(f"[4b-synthesize] Region scaffold written to {out_path}")
    return out_path


# ===================================================================
# Step 5 — Web search enrichment (Sonnet + web_search_20250305)
# ===================================================================

def step_5_web_search(scaffold_path: Path, region_path: Path,
                      benchmark_yaml_text: str, elicitation_summary: str) -> None:
    """Sonnet enriches the region scaffold using the web_search_20250305 server tool.

    Resolves [NEEDS VERIFICATION] placeholders in the scaffold and adds net-new
    fields surfaced by searches. The search budget (max 10 queries) is allocated
    first to coverage_gap_analysis entries from the benchmark YAML, then to
    residual [NEEDS VERIFICATION] slots. Overwrites region_path with the enriched
    YAML on success.
    """
    if region_path.exists():
        print(f"[5] Region YAML already exists: {region_path}")
        return
    print("[5] Sonnet enriching region document via web_search (this may take a minute)...")
    current_yaml = scaffold_path.read_text()
    current_parsed = yaml.safe_load(current_yaml)
    current_json = json.dumps(current_parsed, indent=2, ensure_ascii=False)
    benchmark_parsed = yaml.safe_load(benchmark_yaml_text)
    benchmark_json = json.dumps(benchmark_parsed, indent=2, ensure_ascii=False)
    user_msg = (
        f"Current region document (assessment-specific — enrich this):\n\n"
        f"```json\n{current_json}\n```\n\n"
        f"Benchmark:\n\n```json\n{benchmark_json}\n```\n\n"
        f"Elicitation summary:\n\n{elicitation_summary}\n\n"
        f"**Start with the benchmark's `coverage_gap_analysis` section.** "
        f"This is your primary search targeting input — it lists exactly where "
        f"the user's priorities and the benchmark's coverage diverge, with gap "
        f"types (`full`/`partial`) and suggested search queries. Allocate the "
        f"majority of your search budget to `full` and `partial` gaps before "
        f"applying the guide's general heuristics.\n\n"
        f"The upstream step (4b) produced a scaffold without tool access, so "
        f"every factual slot it could not confidently ground was left as "
        f"`[NEEDS VERIFICATION]`. These tags are secondary search targets — "
        f"resolve as many as your search budget allows, replacing each tag with "
        f"a verified value (or, if the value genuinely cannot be found, a short "
        f"note explaining why and citing what was searched). You may also add "
        f"net-new fields surfaced by your searches; do not drop or silently "
        f"overwrite fields that were filled directly by 4b.\n\n"
        f"Execute your web search plan per the guide, then return the FULL updated "
        f"region document as a single JSON object in a ```json fence. Do NOT output "
        f"any preamble, analysis, or commentary — only the fenced JSON block."
    )
    # Cap web searches at 10 per run to keep costs predictable across all benchmarks
    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}]
    updated_raw = client.call(
        model="sonnet",
        system=prompts.load("web_search_guide"),
        user=user_msg,
        tools=tools,
        max_tokens=32768,
        step="5_web_search",
    )
    if client.DRY_RUN:
        return
    cleaned_json = _run_script("parse_llm_output.py", "--format", "json", "-",
                               stdin=updated_raw)
    parsed = json.loads(cleaned_json)
    as_yaml = yaml.dump(parsed, sort_keys=False, allow_unicode=True,
                        default_flow_style=False)
    region_path.write_text(as_yaml)
    print(f"[5] Region YAML written to {region_path}")


# ===================================================================
# Step 5b — Dataset analysis (deterministic scripts + Sonnet interpretation)
# ===================================================================

HF_LINKS_FILE = ROOT / "benchmarks" / "hf_links.json"
DA_SCRIPTS = ROOT / "scripts" / "dataset_analysis"
DA_CACHE = ROOT / "benchmarks" / "da_cache"
_DEFAULT_CHAR_BUDGET = 50_000


def _da_script_cache_path(hf_dataset: str, hf_config: str | list[str] | None = None) -> Path:
    """Filesystem path for caching deterministic script outputs for one HF dataset."""
    key = hf_dataset.replace("/", "__")
    if hf_config:
        if isinstance(hf_config, list):
            key += "__" + "_".join(sorted(hf_config))
        else:
            key += f"__{hf_config}"
    return DA_CACHE / key / "script_outputs.json"


def _da_summary_cache_path(hf_dataset: str) -> Path:
    """Filesystem path for caching a Sonnet per-dataset summary (org mode)."""
    return DA_CACHE / hf_dataset.replace("/", "__") / "summary.md"


def _requires_remote_code(hf_dataset_id: str) -> bool:
    """Check whether a HF dataset uses a custom loading script.

    Datasets with loading scripts are incompatible with datasets 4.x and
    produce unreliable results even on 3.x (schema casting failures,
    config discovery issues). We skip DA for these datasets entirely.
    """
    import requests as _req
    try:
        resp = _req.get(
            f"https://huggingface.co/api/datasets/{hf_dataset_id}",
            params={"full": "true"}, timeout=15,
        )
        if resp.status_code != 200:
            return False
        siblings = resp.json().get("siblings", [])
        repo_name = hf_dataset_id.split("/")[-1]
        for s in siblings:
            fname = s.get("rfilename", "")
            if fname.endswith(".py") and not fname.startswith("_"):
                if fname == f"{repo_name}.py" or fname == "__init__.py":
                    return True
        return False
    except Exception:
        return False


def _resolve_hf_info(args: argparse.Namespace, name: str) -> dict | None:
    """Resolve dataset analysis target from CLI args or hf_links.json.

    Returns a dict with either:
      {"mode": "single", "hf_dataset_id": "...", "hf_config": "..."}
      {"mode": "org",    "hf_org": "DrBenchmark"}
    or None if no HF info is available or the dataset requires remote code.
    """
    if args.hf_dataset:
        if _requires_remote_code(args.hf_dataset):
            print(f"[5b] skipping DA: {args.hf_dataset} uses a custom loading "
                  f"script (incompatible with datasets 4.x)")
            return None
        return {"mode": "single",
                "hf_dataset_id": args.hf_dataset,
                "hf_config": args.hf_config}

    if HF_LINKS_FILE.exists():
        links = json.loads(HF_LINKS_FILE.read_text())
        tuple_key = getattr(args, "hf_tuple", None)
        # Try both the full name and the part after "__" (handles expert-namespaced stems)
        for key in [name, name.split("__", 1)[-1]]:
            entry = links.get(key, {})
            if not entry:
                continue
            # Per-tuple override (always single-dataset)
            if tuple_key:
                per_tuple = entry.get("per_tuple", {}).get(tuple_key, {})
                if per_tuple.get("hf_dataset_id"):
                    ds_id = per_tuple["hf_dataset_id"]
                    if _requires_remote_code(ds_id):
                        print(f"[5b] skipping DA: {ds_id} uses a custom loading "
                              f"script (incompatible with datasets 4.x)")
                        return None
                    return {"mode": "single",
                            "hf_dataset_id": ds_id,
                            "hf_config": per_tuple.get("hf_config")}
            # Org-level resolution
            if entry.get("hf_org"):
                return {"mode": "org", "hf_org": entry["hf_org"]}
            # Single dataset
            if entry.get("hf_dataset_id"):
                ds_id = entry["hf_dataset_id"]
                if _requires_remote_code(ds_id):
                    print(f"[5b] skipping DA: {ds_id} uses a custom loading "
                          f"script (incompatible with datasets 4.x)")
                    return None
                return {"mode": "single",
                        "hf_dataset_id": ds_id,
                        "hf_config": entry.get("hf_config")}

    return None


def _resolve_org_datasets(hf_org: str) -> list[str]:
    """List all dataset IDs under a HuggingFace organization via the HF API."""
    import requests
    url = f"https://huggingface.co/api/datasets?author={hf_org}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return [d["id"] for d in resp.json()]


def _run_da_script(script_name: str, *extra_args: str) -> str:
    """Run a dataset analysis script and return its JSON stdout.

    Returns a JSON error object on timeout or non-zero exit so callers can
    surface warnings without crashing the whole analysis step.
    """
    script = DA_SCRIPTS / script_name
    cmd = [sys.executable, str(script), *extra_args]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        print(f"  WARN: {script_name} timed out after 300s")
        return json.dumps({"script": script_name, "error": "timed out after 300s"})
    if result.returncode != 0:
        print(f"  WARN: {script_name} failed:\n{result.stderr.rstrip()}")
        return json.dumps({"script": script_name, "error": result.stderr[:500]})
    return result.stdout


def _profile_single_dataset(hf_dataset: str, hf_config: str | list[str] | None) -> dict:
    """Run DA scripts on one dataset and return {script_name: json_str}.

    Runs hf_metadata unconditionally; adds content_sample and audio_stats
    when the modality/schema warrants. Stops early if metadata returns errors
    (e.g. private/non-existent dataset).

    Config resolution:
      - hf_config is a list  → sample from those configs
      - hf_config is a string → sample from that single config
      - hf_config is None    → auto-discover all configs via metadata and
                                sample uniformly across them
    """
    script_outputs = {}

    # Metadata: always run without --config to get the full config map
    meta_args = ["--repo_id", hf_dataset]
    print(f"    hf_metadata...")
    meta_json = _run_da_script("hf_metadata.py", *meta_args)
    script_outputs["hf_metadata"] = meta_json

    meta = json.loads(meta_json)
    if meta.get("errors"):
        print(f"    WARN: metadata errors: {meta['errors']}")
        return script_outputs

    splits_by_config = meta.get("splits_info", {}).get("splits_by_config", {})

    # Resolve configs: explicit list/string > auto-discover from metadata
    if isinstance(hf_config, list):
        configs = hf_config
        resolve_mode = "explicit"
    elif hf_config:
        configs = [hf_config]
        resolve_mode = "explicit"
    elif splits_by_config:
        configs = sorted(splits_by_config.keys())
        resolve_mode = "auto"
    else:
        configs = [None]
        resolve_mode = "auto"

    if len(configs) > 1:
        print(f"    {'Auto-discovered' if resolve_mode == 'auto' else 'Explicit'} "
              f"{len(configs)} configs: {', '.join(str(c) for c in configs)}")

    # Content sampling: fan out across configs, splitting char budget evenly
    per_config_budget = _DEFAULT_CHAR_BUDGET // max(len(configs), 1)
    if len(configs) > 1:
        print(f"    Char budget: {_DEFAULT_CHAR_BUDGET} total, "
              f"~{per_config_budget} per config")
    merged_md_parts = []
    merged_n_exported = 0
    merged_total_chars = 0

    for cfg in configs:
        cfg_splits = splits_by_config.get(cfg, next(iter(splits_by_config.values()), []))
        split = "train" if "train" in cfg_splits else (cfg_splits[0] if cfg_splits else "train")
        sample_args = ["--repo_id", hf_dataset, "--split", split,
                        "--char_budget", str(per_config_budget)]
        if cfg:
            sample_args += ["--config", cfg]
        label = f"config={cfg}, " if cfg else ""
        print(f"    content_sample ({label}split={split}, budget={per_config_budget})...")
        raw_json = _run_da_script("content_sample.py", *sample_args)
        try:
            parsed = json.loads(raw_json)
        except (json.JSONDecodeError, TypeError):
            parsed = {"markdown": raw_json}

        md = parsed.get("markdown", "")
        if cfg and md:
            md = f"## Config: `{cfg}`\n\n{md}"
        merged_md_parts.append(md)
        merged_n_exported += parsed.get("n_exported", 0)
        merged_total_chars += parsed.get("total_chars", 0)

    merged_result = {
        "script": "content_sample",
        "repo_id": hf_dataset,
        "config": hf_config,
        "n_exported": merged_n_exported,
        "total_chars": merged_total_chars,
        "char_budget": _DEFAULT_CHAR_BUDGET,
        "markdown": "\n\n---\n\n".join(merged_md_parts),
    }
    script_outputs["content_sample"] = json.dumps(merged_result, indent=2)

    modalities = meta.get("modality", [])
    features = meta.get("schema", {}).get("features", {})

    if "audio" in modalities:
        audio_cols = [col for col, dtype in features.items() if "Audio" in str(dtype)]
        if audio_cols:
            # Audio stats: run on first config only (schema is typically uniform)
            first_cfg = configs[0]
            first_splits = splits_by_config.get(first_cfg, next(iter(splits_by_config.values()), []))
            a_split = "train" if "train" in first_splits else (first_splits[0] if first_splits else "train")
            audio_args = ["--repo_id", hf_dataset, "--split", a_split,
                          "--column", audio_cols[0], "--sample_size", "50"]
            if first_cfg:
                audio_args += ["--config", first_cfg]
            print(f"    audio_stats on '{audio_cols[0]}'...")
            script_outputs["audio_stats"] = _run_da_script(
                "audio_stats.py", *audio_args)

    return script_outputs


def _sonnet_per_dataset_summary(
    hf_dataset: str,
    script_outputs: dict,
    benchmark_yaml_text: str,
    elicitation_summary: str,
) -> str:
    """Stage 1 (org mode): Sonnet analyzes one dataset with deployment context.

    Used in a loop over all org datasets before the Stage 2 aggregation call.
    Returns the raw Sonnet markdown string (not written to disk here).
    """
    data_sections = []
    data_sections.append(
        f"### HF Metadata\n```json\n{script_outputs.get('hf_metadata', '{}')}\n```")
    content_json = script_outputs.get("content_sample", "{}")
    try:
        # content_sample.py returns {"markdown": "...", ...} — extract the human-readable part
        content_md = json.loads(content_json).get("markdown", content_json)
    except (json.JSONDecodeError, AttributeError):
        content_md = content_json
    data_sections.append(f"### Sampled Examples\n\n{content_md}")
    if "audio_stats" in script_outputs:
        data_sections.append(
            f"### Audio Stats\n```json\n{script_outputs['audio_stats']}\n```")
    data_block = "\n\n".join(data_sections)

    return client.call(
        model="sonnet",
        system=prompts.load("da_per_dataset"),
        user=(
            f"## Dataset: {hf_dataset}\n\n"
            f"## Benchmark YAML\n\n```yaml\n{benchmark_yaml_text}\n```\n\n"
            f"## Deployment Context (Elicitation Summary)\n\n{elicitation_summary}\n\n"
            f"## Dataset Content\n\n{data_block}"
        ),
        max_tokens=8192,
        step="5b_da_per_dataset",
    )


def _find_citation_excerpt(report_text: str, d_num: int) -> str | None:
    """Find citation [D{d_num}] in the citations registry of a per-dataset report.

    Searches the Citations Registry section for a matching row in either
    bracketed or pipe-delimited table format. Returns the cell content or None
    if the citation ID is not found.
    """
    registry_text = report_text
    # Narrow search to the citations section so we don't false-match body text
    for heading in ("Datapoint Citations Registry", "Citations Registry",
                    "Datapoint citations"):
        idx = report_text.find(heading)
        if idx != -1:
            registry_text = report_text[idx:]
            break

    bracketed = f"[D{d_num}]"
    table_pat = re.compile(rf"\|\s*D{d_num}\s*\|")

    for line in registry_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("|-") or stripped.startswith("| --"):
            continue

        if bracketed in stripped:
            # Inline [D{n}] format: strip the ID prefix and surrounding decoration
            content = stripped.lstrip("-|").strip()
            content = content.replace(bracketed, "", 1).strip()
            content = content.strip("|").strip()
            return content

        if table_pat.search(stripped):
            # Pipe-table format: collect non-ID cells and join them
            cells = [c.strip() for c in stripped.split("|")]
            cells = [c for c in cells if c and c.strip() != f"D{d_num}"]
            return " | ".join(cells)

    return None


def _resolve_cited_evidence(
    report: str,
    per_dataset_summaries: dict[str, str],
) -> str:
    """Replace bare citation IDs in Cited Evidence with full excerpts from per-dataset reports.

    Org (multi-dataset) mode only. The aggregation Sonnet call produces a
    Cited Evidence section containing a JSON array of "DATASET-D{n}" IDs.
    This function replaces each ID with the actual datapoint text extracted
    from that dataset's per-dataset report, so the final report is self-contained.
    """
    marker = "### Cited Evidence"
    idx = report.find(marker)
    if idx == -1:
        return report

    before = report[:idx]
    rest = report[idx + len(marker):]

    next_heading = re.search(r"\n### ", rest)
    if next_heading:
        section_body = rest[:next_heading.start()]
        after = rest[next_heading.start():]
    else:
        section_body = rest
        after = ""

    # Extract the JSON array from a ```json ... ``` fenced block
    json_match = re.search(
        r"```json\s*\n(\[.*?\])\s*\n```", section_body, re.DOTALL)
    if not json_match:
        print("  [5b] Warning: no JSON array found in Cited Evidence section")
        return report
    try:
        cited_ids: list[str] = json.loads(json_match.group(1))
    except json.JSONDecodeError as exc:
        print(f"  [5b] Warning: malformed JSON in Cited Evidence: {exc}")
        return report

    # Parse each "DATASET_SHORT-D{n}" string into (short_name, datapoint_number)
    id_pat = re.compile(r"^(.+)-D(\d+)$")
    parsed = []
    for cid in cited_ids:
        m = id_pat.match(cid.strip())
        if m:
            parsed.append((m.group(1), int(m.group(2)), cid.strip()))

    if not parsed:
        return report

    # Build a short-name -> full HF ID map (e.g. "AFRISENTI" -> "masakhane/afrisenti")
    short_to_full: dict[str, str] = {}
    for full_id in per_dataset_summaries:
        short = full_id.split("/")[-1].upper()
        short_to_full[short] = full_id

    resolved = []
    found = 0
    for ds_short, d_num, prefixed in parsed:
        full_id = short_to_full.get(ds_short.upper())
        if not full_id:
            resolved.append(f"- **{prefixed}**: _[source dataset not found]_")
            continue

        excerpt = _find_citation_excerpt(per_dataset_summaries[full_id], d_num)
        if excerpt:
            resolved.append(f"- **{prefixed}**: {excerpt}")
            found += 1
        else:
            resolved.append(
                f"- **{prefixed}**: _[citation not found in report]_")

    total = len(parsed)
    print(f"  [5b] Resolved {found}/{total} cited evidence entries")

    return before + f"{marker}\n\n" + "\n".join(resolved) + "\n" + after


EXIT_HF_SCRIPT_FAILED = 2


def _validate_content_sample(
    script_outputs: dict, hf_dataset: str, cache_path: Path,
) -> None:
    """Abort with exit code 2 if content_sample returned an error or no examples.

    Removes the stale cache entry so a re-run with corrected config will
    re-profile from scratch rather than replaying the cached failure.
    """
    raw = script_outputs.get("content_sample", "{}")
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        parsed = {}

    error = parsed.get("error")
    if error:
        if cache_path.exists():
            cache_path.unlink()
        print(f"FATAL [5b]: content_sample failed for {hf_dataset}: {error}",
              file=sys.stderr)
        sys.exit(EXIT_HF_SCRIPT_FAILED)

    n_examples = parsed.get("examples_exported", 0)
    if n_examples == 0 and "markdown" not in parsed:
        if cache_path.exists():
            cache_path.unlink()
        print(f"FATAL [5b]: content_sample returned 0 examples for {hf_dataset} "
              f"(check hf_config in hf_links.json)", file=sys.stderr)
        sys.exit(EXIT_HF_SCRIPT_FAILED)


def step_5b_dataset_analysis(
    hf_info: dict,
    benchmark_yaml_text: str,
    elicitation_summary: str,
    web_search_text: str,
    name: str,
    slug: str,
) -> Path | None:
    """Run dataset analysis scripts and have Sonnet interpret findings.

    Supports two modes:
      single — one dataset, single-pass interpretation
      org    — all datasets under an HF org, two-stage interpretation
               (per-dataset summaries -> aggregated report)

    Script outputs are cached (dataset-intrinsic, reused across assessments).
    Sonnet analyses use trace-based resume so a crash mid-org run can continue
    from where it left off. Returns path to the written dataset_analysis_report.md
    or None in dry-run mode.
    """
    out_path = _da_report_path(name, slug)
    if out_path.exists():
        print(f"[5b] DA report already exists: {out_path}")
        return out_path

    if hf_info["mode"] == "org":
        hf_org = hf_info["hf_org"]
        print(f"[5b] Resolving datasets under HF org '{hf_org}'...")
        dataset_ids = _resolve_org_datasets(hf_org)
        print(f"[5b] Found {len(dataset_ids)} datasets: "
              f"{', '.join(d.split('/')[-1] for d in dataset_ids)}")

        # === Stage 1: profile each dataset + per-dataset Sonnet analysis ===
        # Script outputs are cached (dataset-intrinsic). Per-dataset Sonnet
        # analyses use trace-based resume: completed analyses are recovered
        # from 5b_da_per_dataset.jsonl so a crash mid-way can resume.
        # Traces are only cleared on a fully fresh run (no prior results).
        trace_file = _trace_dir(name, slug) / "5b_da_per_dataset.jsonl"
        completed_analyses: dict[str, str] = {}
        if trace_file.exists():
            # Recover completed per-dataset analyses from the trace JSONL by
            # matching the dataset ID in the user message of each entry
            for line in trace_file.read_text().splitlines():
                try:
                    entry = json.loads(line)
                    user_msg = entry.get("user", "")
                    for ds_id in dataset_ids:
                        if ds_id in user_msg and ds_id not in completed_analyses:
                            completed_analyses[ds_id] = entry["output"]
                            break
                except (json.JSONDecodeError, KeyError):
                    continue

        if completed_analyses:
            print(f"[5b] Resuming: {len(completed_analyses)}/{len(dataset_ids)} "
                  f"per-dataset analyses cached from prior run")
        else:
            client.clear_trace_steps("5b_da_per_dataset")

        per_dataset_summaries = {}
        for i, ds_id in enumerate(dataset_ids, 1):
            ds_short = ds_id.split("/")[-1]

            script_cache = _da_script_cache_path(ds_id)

            if script_cache.exists():
                print(f"\n  [{i}/{len(dataset_ids)}] {ds_id} (script cache hit)")
                outputs = json.loads(script_cache.read_text())
            else:
                print(f"\n  [{i}/{len(dataset_ids)}] Profiling {ds_id}...")
                outputs = _profile_single_dataset(ds_id, hf_config=None)
                script_cache.parent.mkdir(parents=True, exist_ok=True)
                script_cache.write_text(json.dumps(outputs, indent=2))

            if ds_id in completed_analyses and not client.DRY_RUN:
                print(f"    {ds_short} analysis (trace hit)")
                per_dataset_summaries[ds_id] = completed_analyses[ds_id]
                continue

            print(f"    Sonnet analyzing {ds_short}...")
            summary = _sonnet_per_dataset_summary(
                ds_id, outputs, benchmark_yaml_text, elicitation_summary)
            per_dataset_summaries[ds_id] = summary

        # === Stage 2: aggregation across all datasets ===
        # All per-dataset summaries are concatenated and sent to Sonnet for a
        # cross-dataset interpretation informed by the benchmark and deployment context.
        summaries_block = "\n\n".join(
            f"### {ds_id}\n\n{summary}"
            for ds_id, summary in per_dataset_summaries.items()
        )
        print(f"\n  [5b] Sonnet aggregating {len(dataset_ids)} dataset analyses...")
        report = client.call(
            model="sonnet",
            system=prompts.load("da_aggregate"),
            user=(
                f"## Benchmark YAML\n\n```yaml\n{benchmark_yaml_text}\n```\n\n"
                f"## Deployment Context (Elicitation Summary)\n\n{elicitation_summary}\n\n"
                f"## Web Search Findings\n\n{web_search_text}\n\n"
                f"## Per-Dataset Analysis Reports\n\n{summaries_block}"
            ),
            max_tokens=16384,
            step="5b_da_interpret",
        )

        if not client.DRY_RUN:
            # Replace citation IDs (e.g. AFRISENTI-D3) with inline excerpts
            # so the final report is self-contained and readable without cross-referencing
            report = _resolve_cited_evidence(report, per_dataset_summaries)

    else:
        # Single-dataset mode — direct interpretation, no intermediate summary
        hf_dataset = hf_info["hf_dataset_id"]
        hf_config = hf_info.get("hf_config")

        if isinstance(hf_config, list):
            cfg_label = f" | configs: {hf_config}"
        elif hf_config:
            cfg_label = f" | config: {hf_config}"
        else:
            cfg_label = " | configs: auto-discover"

        script_cache = _da_script_cache_path(hf_dataset, hf_config)
        if script_cache.exists():
            print(f"[5b] {hf_dataset}{cfg_label} (script cache hit)")
            script_outputs = json.loads(script_cache.read_text())
        else:
            print(f"[5b] Running dataset analysis on {hf_dataset}{cfg_label}...")
            script_outputs = _profile_single_dataset(hf_dataset, hf_config)
            script_cache.parent.mkdir(parents=True, exist_ok=True)
            script_cache.write_text(json.dumps(script_outputs, indent=2))

        # Validate that content_sample produced actual examples — a silent
        # fallback to paper-only analysis defeats the purpose of the DA step
        _validate_content_sample(script_outputs, hf_dataset, script_cache)

        data_sections = []
        data_sections.append(
            f"### HF Metadata\n```json\n{script_outputs.get('hf_metadata', '{}')}\n```")
        content_json = script_outputs.get("content_sample", "{}")
        try:
            content_md = json.loads(content_json).get("markdown", content_json)
        except (json.JSONDecodeError, AttributeError):
            content_md = content_json
        data_sections.append(f"### Sampled Examples\n\n{content_md}")
        if "audio_stats" in script_outputs:
            data_sections.append(
                f"### Audio Stats\n```json\n{script_outputs['audio_stats']}\n```")
        data_block = "\n\n".join(data_sections)

        print("  [5b] Sonnet interpreting dataset content...")
        report = client.call(
            model="sonnet",
            system=prompts.load("da_interpret"),
            user=(
                f"## Benchmark YAML\n\n```yaml\n{benchmark_yaml_text}\n```\n\n"
                f"## Deployment Context (Elicitation Summary)\n\n{elicitation_summary}\n\n"
                f"## Web Search Findings\n\n{web_search_text}\n\n"
                f"## Dataset Content\n\n{data_block}"
            ),
            max_tokens=16384,
            step="5b_da_interpret",
        )

    if client.DRY_RUN:
        return out_path

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report)
    print(f"[5b] DA report written to {out_path}")
    return out_path


# ===================================================================
# Step 6 — Compose evaluation prompt (script)
# ===================================================================

def step_6_compose(
    benchmark_path: Path,
    region_path: Path,
    elicitation_path: Path,
    name: str,
    slug: str,
    da_report_path: Path | None = None,
) -> Path:
    """Assemble the final evaluation prompt by invoking compose_prompt.py.

    Concatenates benchmark YAML, region YAML, framework dimensions, elicitation
    summary, and (optionally) the dataset analysis report into a single prompt
    document that Step 7 (Opus scoring) reads. No API call — pure script.
    Returns path to the composed_prompt.md.
    """
    out_path = _composed_prompt_path(name, slug)
    if out_path.exists():
        print(f"[6] Composed prompt already exists: {out_path}")
        return out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print("[6] Composing evaluation prompt via compose_prompt.py...")
    compose_args = [
        "--benchmark", str(benchmark_path),
        "--region", str(region_path),
        "--framework", str(FRAMEWORK),
        "--elicitation", str(elicitation_path),
        "--region-name", slug,
        "--output", str(out_path),
    ]
    if da_report_path and da_report_path.exists():
        compose_args += ["--dataset-analysis", str(da_report_path)]
    _run_script("compose_prompt.py", *compose_args)
    return out_path


# ===================================================================
# Step 7 — Opus scoring (the one Opus call)
# ===================================================================

def step_7_score(composed_path: Path, name: str, slug: str) -> Path:
    """Opus reads the composed evaluation prompt and returns structured validity scores.

    This is the single Opus call in the pipeline. All prior steps build up the
    prompt; Opus performs the final holistic judgment across validity dimensions.
    Returns path to the written scoring.json.
    """
    out_path = _scoring_path(name, slug)
    if out_path.exists():
        print(f"[7] Scoring output already exists: {out_path}")
        return out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print("[7] Opus scoring (the one Opus call in the pipeline)...")
    raw = client.call(
        model="opus",
        system=prompts.load("opus_scoring_framing"),
        user=composed_path.read_text(),
        max_tokens=32768,
        step="7_score",
    )
    if client.DRY_RUN:
        return out_path
    cleaned = _run_script("parse_llm_output.py", "--format", "json", "-", stdin=raw)
    cleaned = _run_script("repair_scoring_json.py", "-", stdin=cleaned)
    out_path.write_text(cleaned)
    print(f"[7] Results written to {out_path}")
    return out_path


# ===================================================================
# Step 8 — Report (script)
# ===================================================================

def step_8_report(results_path: Path) -> None:
    """Format the Opus scoring JSON into a human-readable markdown report.

    Invokes format_results.py (no API call). Writes report.md next to
    scoring.json and also prints it to stdout for immediate review.
    """
    report_path = results_path.parent / "report.md"
    if report_path.exists():
        print(f"[8] Report already exists: {report_path}")
        return
    report = _run_script("format_results.py", str(results_path))
    report_path.write_text(report, encoding="utf-8")
    print(f"[8] Report written to {report_path}")
    print("\n" + "=" * 60)
    print(report)


# ===================================================================
# Persistent cost ledger — per-paper file under assessments/
# ===================================================================
# Each step loads this file, clears its own step labels (so a re-run of a
# single step overwrites that step's cost rather than accumulating), records
# new usage during the call, and saves. After any run the file reflects the
# "final" cost of each step executed so far — a running total of one full
# pipeline run's expected cost even if reached via many re-tries.

# Entries cleared by _ledger_begin but not repopulated by new API calls
# (i.e. the step's output was already cached and it skipped). _ledger_end
# restores these so a no-op re-run doesn't erase historical cost data.
_cleared_but_unused: dict = {}

# Mapping from public step identifiers (used with --step) to the ledger step
# labels that the step's API calls emit. Re-running a step clears its labels.
# Every API call has its own --step so you can dry-run / inspect / pay for
# each one independently.
STEP_LABELS: dict[str, list[str]] = {
    "0": ["0_slug"],
    "1":              ["1_metadata"],
    "2-questions":    ["2_questions"],
    "2-summary":      ["2_summary"],
    # Note: "3a_extract" is NOT cleared by _ledger_begin, because the per-page
    # cache lets a retry skip pages that already succeeded. Clearing it here
    # would erase the cost of those successful pages and under-count the true
    # expected cost. Instead, step_1a_extract (the extraction function) clears
    # this label itself when it detects a fresh (no-cache) run.
    "3a-extract":     [],
    "3a-assemble":    ["3a_merge"],
    "3a-consolidate": ["3a_consolidate"],
    "3b-select":      ["3b_select"],
    "3b-synthesize":  ["3b_synthesize"],
    "3c-verify":      [],   # script only, no API call
    "4a-template":    ["4a_template"],
    "4b-synthesize":  ["4b_synthesize"],
    "5":              ["5_web_search"],
    # 5b_da_per_dataset is NOT auto-cleared: per-dataset analyses use
    # trace-based resume (like 3a_extract). Only the aggregation re-runs.
    "5b-da":          ["5b_da_interpret"],
    "6":              [],
    "7":              ["7_score"],
    "8":              [],
}


def _ledger_begin(name: str, *step_keys: str) -> None:
    """Load persistent ledger then drop prior entries for the given step(s).

    Called at the start of each step so a re-run replaces rather than
    accumulates. No-ops in dry-run mode to leave the real ledger untouched.

    Snapshots cleared entries into _cleared_but_unused so _ledger_end can
    restore them if the step turns out to be a cache-hit (no new API calls).
    """
    global _cleared_but_unused
    _cleared_but_unused = {}
    if client.DRY_RUN:
        return  # don't touch the real ledger in dry-run mode
    slug = _read_slug(name)
    if not slug:
        # No slug yet (e.g. step 0 firing) — ledger writes are deferred until
        # the slug lands. See _init_assessment_paths.
        return
    _assessment_dir(name, slug).mkdir(parents=True, exist_ok=True)
    client.reset_ledger()
    client.load_ledger(_cost_ledger_path(name, slug))
    labels: list[str] = []
    for k in step_keys:
        labels.extend(STEP_LABELS.get(k, []))
    if labels:
        # Snapshot entries we're about to clear so they can be restored if the
        # step skips (cached output exists) — prevents no-op re-runs from
        # erasing historical cost data.
        snap = client.ledger_snapshot()
        _cleared_but_unused = {l: snap[l] for l in labels if l in snap}
        client.clear_steps(*labels)
        # Keep the trace log in sync with the ledger: drop prior entries for
        # these step labels so the JSONL always matches a clean final-run view.
        client.clear_trace_steps(*labels)


def _ledger_end(name: str) -> None:
    """Persist the in-memory ledger to disk after a step completes.

    If _ledger_begin cleared entries that were never replaced by new API
    calls (step was a cache-hit), restore them before saving so historical
    cost data is preserved.
    """
    global _cleared_but_unused
    if client.DRY_RUN:
        _cleared_but_unused = {}
        return
    slug = _read_slug(name)
    if not slug:
        _cleared_but_unused = {}
        return
    # Restore entries that were cleared but never replaced by new API calls.
    if _cleared_but_unused:
        snap = client.ledger_snapshot()
        to_restore = {l: v for l, v in _cleared_but_unused.items() if l not in snap}
        if to_restore:
            client.graft_snapshot(to_restore)
        _cleared_but_unused = {}
    path = client.save_ledger(_cost_ledger_path(name, slug))
    print(f"[cost] Ledger updated: {path}")


def _init_assessment_paths(name: str) -> None:
    """After a slug is known, point trace + ledger at the assessment dir.

    Safe to call repeatedly. The 0_slug Haiku call lands in the in-memory
    ledger before the slug exists on disk; this function persists it once
    the slug is known and wires subsequent calls into the trace file.

    Reconciles the in-memory ledger (typically just 0_slug) with the disk
    ledger so other steps' historical costs survive without being double-counted.
    """
    if client.DRY_RUN:
        return
    slug = _read_slug(name)
    if not slug:
        return
    _assessment_dir(name, slug).mkdir(parents=True, exist_ok=True)
    client.set_trace_dir(_trace_dir(name, slug))

    # Reconcile this run's in-memory ledger (typically just 0_slug from step
    # 0) with the disk ledger (which may already hold costs from prior runs
    # of this assessment). Goal: disk state for OTHER steps survives; any
    # step this run touched is replaced, not doubled.
    ledger_path = _cost_ledger_path(name, slug)
    in_mem = client.ledger_snapshot()
    client.reset_ledger()
    client.load_ledger(ledger_path)      # pull prior disk state
    for step in in_mem:
        client.clear_steps(step)          # drop any stale copy of this run's steps
    client.graft_snapshot(in_mem)         # re-plant this run's fresh entries
    client.save_ledger(ledger_path)


def parse_args() -> argparse.Namespace:
    """Define and parse all CLI arguments; returns the populated Namespace."""
    p = argparse.ArgumentParser(description="Validity analysis pipeline.")
    p.add_argument("pdf_path", nargs="?", help="Path to the benchmark paper PDF")
    p.add_argument(
        "--persona",
        help=f"Persona ID for CC Opus subagent elicitation (one of {sorted(PERSONAS)})",
    )
    p.add_argument(
        "--use-case",
        help="Path to a file containing the deployment description "
        "(overrides the persona's initial_description)",
    )
    p.add_argument(
        "--no-web-search",
        action="store_true",
        help="Skip Step 5 (web search enrichment)",
    )
    p.add_argument(
        "--step",
        choices=sorted(STEP_LABELS),
        help="Run a single pipeline step (default: run all steps end-to-end).",
    )
    p.add_argument(
        "--answers",
        help="Path to an answers JSON file (used with --step 2-summary after "
        "running a CC Opus subagent on the persona prompt).",
    )
    p.add_argument(
        "--show-cost",
        action="store_true",
        help="Print the persistent cost ledger for <pdf>.stem and exit.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print each step's system/user prompt to stdout instead of "
        "calling the API. Downstream calls receive a placeholder; use with "
        "--step to inspect one step at a time.",
    )
    p.add_argument(
        "--streaming",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Force-enable (--streaming) or disable (--no-streaming) token "
        "streaming to stderr for ALL API calls. Default (omitted): stream "
        "Sonnet/Opus only, since the Haiku fan-out is usually parallel. "
        "Handy with --step 3a-extract (1 worker) to watch page extractions.",
    )
    p.add_argument(
        "--strict-verify",
        action="store_true",
        help="Halt the pipeline if the 3c-verify mechanical check fails. "
        "Default is soft: print the failure report and continue, so a single "
        "Sonnet formatting slip doesn't waste a full-run's cost. Use --strict-verify "
        "in CI / dev to enforce the gate.",
    )
    p.add_argument(
        "--hf-dataset",
        help="HuggingFace dataset ID (e.g. masakhane/afrisenti). "
        "Enables Step 5b dataset analysis. Also checks benchmarks/hf_links.json.",
    )
    p.add_argument(
        "--hf-config",
        help="HuggingFace dataset config/subset (e.g. pcm). Used with --hf-dataset.",
    )
    p.add_argument(
        "--hf-tuple",
        help="Tuple key for per-tuple HF link override in hf_links.json "
        "(e.g. tuple_3). Used by expert experiment scripts.",
    )
    p.add_argument(
        "--no-dataset-analysis",
        action="store_true",
        help="Skip Step 5b even if an HF dataset ID is available.",
    )
    p.add_argument(
        "--tpm-limit",
        type=int,
        default=30_000,
        help="Input tokens-per-minute rate limit. Default: 30000 "
        "(personal-tier Sonnet limit). Set to 0 to disable.",
    )
    p.add_argument(
        "--otpm-limit",
        type=int,
        default=8_000,
        help="Output tokens-per-minute rate limit. Default: 8000 "
        "(personal-tier Sonnet limit). Set to 0 to disable.",
    )
    return p.parse_args()


def _resolve_initial_description(args: argparse.Namespace, name: str) -> str:
    """Resolve the deployment description from CLI args or interactive input.

    Priority: --use-case file > persona default > cached active-slug description > stdin prompt.
    """
    if args.use_case:
        return Path(args.use_case).read_text().strip()
    if args.persona:
        return PERSONAS[args.persona]["initial_description"]
    active = _read_slug(name)
    if active:
        cached = _deployment_desc_path(name, active)
        if cached.exists():
            return cached.read_text().strip()
    print("Enter your deployment description (end with Ctrl-D):")
    return sys.stdin.read().strip()


def _print_cost_report() -> None:
    """Print the current in-memory cost report if any API calls were made."""
    report = client.format_cost_report()
    if report == "(no API calls recorded)":
        return
    print("\n=== API Cost Report ===")
    print(report)


def _require_paths(name: str) -> None:
    """Paths that must exist before later steps can run in isolation."""
    pass  # Per-step checks live inside each step_* function.


def main() -> None:
    """Entry point: parse args, validate preconditions, then run full pipeline or single step."""
    args = parse_args()

    if not args.pdf_path:
        print("ERROR: pdf_path is required", file=sys.stderr)
        sys.exit(2)
    # Use the PDF stem as the paper name; deliberately un-resolved to preserve
    # expert-experiment-namespaced stems (e.g. "expert_b082a2ed12a9__ltzglue").
    name = Path(args.pdf_path).stem
    pdf_path = Path(args.pdf_path).resolve()

    # --show-cost: read-only, no step execution.
    if args.show_cost:
        slug = _read_slug(name)
        if not slug:
            print(
                f"ERROR: no slug on disk for {name}. Run --step 0 (or a full "
                f"pipeline) first to derive the assessment slug.",
                file=sys.stderr,
            )
            sys.exit(1)
        client.reset_ledger()
        client.load_ledger(_cost_ledger_path(name, slug))
        report = client.format_cost_report()
        print(report)
        return

    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        client.set_dry_run(True)
        print("[dry-run mode] API calls are skipped; prompts printed to stdout.\n")
    if args.streaming is not None:
        client.set_stream_default(args.streaming)
    if args.tpm_limit or args.otpm_limit:
        client.set_tpm_limit(args.tpm_limit, args.otpm_limit)
    if args.persona:
        args.persona = args.persona.lower()
        if args.persona not in PERSONAS:
            print(
                f"ERROR: unknown persona '{args.persona}'. Known: {sorted(PERSONAS)}",
                file=sys.stderr,
            )
            sys.exit(1)
    if not FRAMEWORK.exists():
        print(f"ERROR: framework.yaml not found at {FRAMEWORK}", file=sys.stderr)
        sys.exit(1)

    # === Single-step mode ===
    if args.step:
        _run_single_step(args, pdf_path, name)
        return

    # === Sequential mode ===
    hf_info = _resolve_hf_info(args, name)
    print(f"Running validity pipeline on {pdf_path.name}")
    print(f"  Persona:       {args.persona or '(stdin mode)'}")
    print(f"  Use case file: {args.use_case or '(n/a)'}")
    print(f"  Web search:    {'off' if args.no_web_search else 'on'}")
    if args.no_dataset_analysis:
        da_status = "off"
    elif hf_info is None:
        da_status = "no HF link"
    elif hf_info["mode"] == "org":
        da_status = f"org: {hf_info['hf_org']}"
    else:
        da_status = hf_info["hf_dataset_id"]
    print(f"  Dataset analysis: {da_status}\n")

    try:
        # === Step 0: derive the assessment slug ===
        initial_description = _resolve_initial_description(args, name)
        slug = step_0_derive_slug(initial_description, name)
        _init_assessment_paths(name)

        # === Step 1: quick metadata extraction (Haiku, pages 1-2) ===
        _ledger_begin(name, "1")
        metadata_path = step_1_metadata(pdf_path, name)
        metadata_text = metadata_path.read_text() if metadata_path.exists() else ""
        _ledger_end(name)

        # === Step 2: elicit deployment context (early — before heavy PDF processing) ===
        _ledger_begin(name, "2-questions")
        q_path, persona_prompt_path = step_2_questions(
            metadata_text, initial_description, args.persona, name, slug
        )
        _ledger_end(name)

        if args.persona:
            # Persona mode requires an async CC Opus subagent loop — pause here
            # and print instructions. The user resumes with --step 2-summary.
            answers_target = _answers_path(name, slug)
            print(
                f"\n[pause] Persona elicitation requires a Claude Code Opus subagent.\n"
                f"        1. Open {persona_prompt_path}\n"
                f"        2. Dispatch a CC Opus subagent with the system prompt + user message\n"
                f"        3. Save the subagent's JSON reply to {answers_target}\n"
                f"        4. Resume: python run_pipeline.py {pdf_path.name} "
                f"--step 2-summary --answers {answers_target}\n"
            )
            return

        step_2_collect_stdin(name, slug)

        _ledger_begin(name, "2-summary")
        elicitation_path = step_2_summary(name, slug, metadata_text)
        elicitation_summary = elicitation_path.read_text()
        _ledger_end(name)

        # === Step 3a: paper -> per-page extractions -> assemble registry -> narrative ===
        _ledger_begin(name, "3a-extract")
        step_1a_extract(pdf_path, name)
        _ledger_end(name)

        _ledger_begin(name, "3a-assemble")
        step_3a_assemble(name)
        _ledger_end(name)

        _ledger_begin(name, "3a-consolidate")
        summary_path = step_3a_consolidate(name, elicitation_summary, slug)
        paper_summary = summary_path.read_text()
        _ledger_end(name)

        # === Step 3b: paper summary -> benchmark YAML ===
        _ledger_begin(name, "3b-select")
        step_3b_select(paper_summary, name)
        _ledger_end(name)

        _ledger_begin(name, "3b-synthesize")
        benchmark_path = step_3b_synthesize(paper_summary, name, elicitation_summary, slug)
        benchmark_yaml_text = benchmark_path.read_text()
        _ledger_end(name)

        # === Step 3c: quote provenance verification ===
        step_3c_verify(benchmark_path, summary_path, strict=args.strict_verify)

        # === Step 4: region YAML ===
        _ledger_begin(name, "4a-template")
        step_4a_template(elicitation_summary, name, slug)
        _ledger_end(name)

        _ledger_begin(name, "4b-synthesize")
        scaffold_path = step_4b_synthesize(
            elicitation_summary, benchmark_yaml_text, name, slug
        )
        _ledger_end(name)

        region_path = _region_yaml_path(name, slug)

        # === Step 5: web search enrichment ===
        web_search_text = ""
        if not args.no_web_search:
            _ledger_begin(name, "5")
            step_5_web_search(scaffold_path, region_path,
                              benchmark_yaml_text, elicitation_summary)
            _ledger_end(name)
            # Read back the enriched YAML to pass as context to Step 5b
            web_search_text = region_path.read_text()

        # === Step 5b: dataset analysis (conditional on HF link) ===
        da_report_path = None
        if not args.no_dataset_analysis and hf_info:
            _ledger_begin(name, "5b-da")
            da_report_path = step_5b_dataset_analysis(
                hf_info,
                benchmark_yaml_text, elicitation_summary, web_search_text,
                name, slug,
            )
            _ledger_end(name)

        # === Step 6-8: compose prompt, score (Opus), format report ===
        composed_path = step_6_compose(
            benchmark_path, region_path, elicitation_path, name, slug,
            da_report_path=da_report_path,
        )

        _ledger_begin(name, "7")
        results_path = step_7_score(composed_path, name, slug)
        _ledger_end(name)

        step_8_report(results_path)
    finally:
        # Always print cost report on exit, even if a step raised an exception
        _print_cost_report()


def _run_single_step(args: argparse.Namespace, pdf_path: Path, name: str) -> None:
    """Execute exactly one pipeline step in isolation, reusing on-disk outputs for inputs.

    Each branch validates that required upstream files exist, then calls the
    appropriate step_* function. Cost ledger is loaded/saved via _ledger_begin
    / _ledger_end in the try/finally.
    """
    metadata_path = _metadata_path(name)

    if args.step == "0":
        initial_description = _resolve_initial_description(args, name)
        step_0_derive_slug(initial_description, name)
        _init_assessment_paths(name)
        _print_cost_report()
        return

    slug = _read_slug(name)
    if not slug and not client.DRY_RUN:
        print(
            f"ERROR: no slug on disk for {name}. Run --step 0 first to derive "
            f"the assessment slug (provide --persona or --use-case).",
            file=sys.stderr,
        )
        sys.exit(1)
    if slug:
        _init_assessment_paths(name)

    summary_path = _paper_summary_path(name, slug or "")
    benchmark_path = _assessment_dir(name, slug) / "benchmark.yaml" if slug else BENCHMARKS / f"{name}.yaml"

    try:
        if args.step == "1":
            _ledger_begin(name, "1")
            step_1_metadata(pdf_path, name)
        elif args.step == "2-questions":
            if not metadata_path.exists() and not client.DRY_RUN:
                print(f"ERROR: run --step 1 first ({metadata_path} missing)",
                      file=sys.stderr)
                sys.exit(1)
            metadata_text = metadata_path.read_text() if metadata_path.exists() else ""
            initial_description = _resolve_initial_description(args, name)
            _ledger_begin(name, "2-questions")
            _, persona_prompt_path = step_2_questions(
                metadata_text, initial_description, args.persona,
                name, slug,
            )
            if persona_prompt_path:
                answers_target = _answers_path(name, slug)
                print(
                    f"\n[next] Hand {persona_prompt_path} to a CC Opus subagent, "
                    f"save its JSON to {answers_target}, then:\n"
                    f"       python run_pipeline.py {pdf_path.name} "
                    f"--step 2-summary --answers {answers_target}\n"
                )
        elif args.step == "2-summary":
            if not metadata_path.exists() and not client.DRY_RUN:
                print(f"ERROR: run --step 1 first ({metadata_path} missing)",
                      file=sys.stderr)
                sys.exit(1)
            metadata_text = metadata_path.read_text() if metadata_path.exists() else ""
            _ledger_begin(name, "2-summary")
            step_2_summary(
                name,
                slug,
                metadata_text,
                answers_path=Path(args.answers) if args.answers else None,
            )
        elif args.step == "3a-extract":
            _ledger_begin(name, "3a-extract")
            step_1a_extract(pdf_path, name)  # legacy name; see docstring
        elif args.step == "3a-assemble":
            cache_dir = PAGE_CACHES / name
            if not any(cache_dir.glob("page_*.txt")) and not client.DRY_RUN:
                print(
                    f"ERROR: run --step 3a-extract first ({cache_dir} empty)",
                    file=sys.stderr,
                )
                sys.exit(1)
            _ledger_begin(name, "3a-assemble")
            step_3a_assemble(name)
        elif args.step == "3a-consolidate":
            registry_path = _quote_registry_path(name)
            if not registry_path.exists() and not client.DRY_RUN:
                print(
                    f"ERROR: run --step 3a-assemble first ({registry_path} missing)",
                    file=sys.stderr,
                )
                sys.exit(1)
            elicitation_path = _elicitation_summary_path(name, slug)
            elicitation_summary = elicitation_path.read_text() if elicitation_path.exists() else ""
            _ledger_begin(name, "3a-consolidate")
            step_3a_consolidate(name, elicitation_summary, slug or "")
        elif args.step == "3b-select":
            if not summary_path.exists() and not client.DRY_RUN:
                print(f"ERROR: run --step 3a-consolidate first ({summary_path} missing)",
                      file=sys.stderr)
                sys.exit(1)
            paper_summary = summary_path.read_text() if summary_path.exists() else ""
            _ledger_begin(name, "3b-select")
            step_3b_select(paper_summary, name)
        elif args.step == "3b-synthesize":
            if not summary_path.exists() and not client.DRY_RUN:
                print(f"ERROR: run --step 3a-consolidate first ({summary_path} missing)",
                      file=sys.stderr)
                sys.exit(1)
            paper_summary = summary_path.read_text() if summary_path.exists() else ""
            elicitation_path = _elicitation_summary_path(name, slug)
            elicitation_summary = elicitation_path.read_text() if elicitation_path.exists() else ""
            _ledger_begin(name, "3b-synthesize")
            step_3b_synthesize(paper_summary, name, elicitation_summary, slug or "")
        elif args.step == "3c-verify":
            if not benchmark_path.exists() or not summary_path.exists():
                print("ERROR: run --step 3a-consolidate + 3b-synthesize first",
                      file=sys.stderr)
                sys.exit(1)
            step_3c_verify(benchmark_path, summary_path, strict=args.strict_verify)
        elif args.step == "4a-template":
            elicitation_path = _elicitation_summary_path(name, slug)
            if not elicitation_path.exists() and not client.DRY_RUN:
                print("ERROR: run --step 2-summary first", file=sys.stderr)
                sys.exit(1)
            _ledger_begin(name, "4a-template")
            step_4a_template(
                elicitation_path.read_text() if elicitation_path.exists() else "",
                name, slug,
            )
        elif args.step == "4b-synthesize":
            elicitation_path = _elicitation_summary_path(name, slug)
            if (not elicitation_path.exists() or not benchmark_path.exists()) \
                    and not client.DRY_RUN:
                print("ERROR: run --step 3b-synthesize + 2-summary first",
                      file=sys.stderr)
                sys.exit(1)
            _ledger_begin(name, "4b-synthesize")
            step_4b_synthesize(
                elicitation_path.read_text() if elicitation_path.exists() else "",
                benchmark_path.read_text() if benchmark_path.exists() else "",
                name, slug,
            )
        elif args.step == "5":
            scaffold_path = _region_scaffold_path(name, slug)
            if not scaffold_path.exists():
                print(
                    f"ERROR: run --step 4b-synthesize first ({scaffold_path} missing)",
                    file=sys.stderr,
                )
                sys.exit(1)
            region_path = _region_yaml_path(name, slug)
            elicitation_path = _elicitation_summary_path(name, slug)
            _ledger_begin(name, "5")
            step_5_web_search(
                scaffold_path, region_path,
                benchmark_path.read_text(), elicitation_path.read_text()
            )
        elif args.step == "5b-da":
            hf_info = _resolve_hf_info(args, name)
            if not hf_info:
                print("ERROR: no HF info. Pass --hf-dataset or add "
                      f"'{name}' to benchmarks/hf_links.json", file=sys.stderr)
                sys.exit(1)
            elicitation_path = _elicitation_summary_path(name, slug)
            region_path = _region_yaml_path(name, slug)
            _ledger_begin(name, "5b-da")
            step_5b_dataset_analysis(
                hf_info,
                benchmark_path.read_text() if benchmark_path.exists() else "",
                elicitation_path.read_text() if elicitation_path.exists() else "",
                region_path.read_text() if region_path.exists() else "",
                name, slug,
            )
        elif args.step == "6":
            region_path = _region_yaml_path(name, slug)
            if not region_path.exists():
                print(
                    f"ERROR: run --step 4b-synthesize first ({region_path} missing)",
                    file=sys.stderr,
                )
                sys.exit(1)
            elicitation_path = _elicitation_summary_path(name, slug)
            da_path = _da_report_path(name, slug)
            step_6_compose(benchmark_path, region_path, elicitation_path, name, slug,
                           da_report_path=da_path if da_path.exists() else None)
        elif args.step == "7":
            composed_path = _composed_prompt_path(name, slug)
            if not composed_path.exists():
                print(f"ERROR: run step 6 first ({composed_path} missing)", file=sys.stderr)
                sys.exit(1)
            _ledger_begin(name, "7")
            step_7_score(composed_path, name, slug)
        elif args.step == "8":
            results_path = _scoring_path(name, slug)
            if not results_path.exists():
                print(f"ERROR: run step 7 first ({results_path} missing)", file=sys.stderr)
                sys.exit(1)
            step_8_report(results_path)
        else:
            print(f"ERROR: unknown --step {args.step}", file=sys.stderr)
            sys.exit(2)
    finally:
        if args.step in STEP_LABELS:
            _ledger_end(name)
        _print_cost_report()


if __name__ == "__main__":
    main()
