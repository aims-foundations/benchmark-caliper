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
    Step 3a-consolidate Sonnet merges per-page extractions (guided by elicitation priorities)
    Step 3b-select      Haiku picks 1-2 reference benchmark YAMLs
    Step 3b-synthesize  Sonnet writes the benchmark YAML (+ coverage_gap_analysis)
    Step 3c-verify      verify_quotes.py (script, no API)
    Step 4a-template    Haiku picks 1-2 base region templates
    Step 4b-synthesize  Sonnet writes the assessment-specific region YAML
    Step 5              Sonnet + web_search_20250305 server tool -> region enrichment
    Step 6              compose_prompt.py (script)
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
    def tqdm(iterable, **kwargs):
        return iterable

import client
import prompts
from personas import PERSONAS


ROOT = Path(__file__).parent
SCRIPTS = ROOT / "scripts"
FRAMEWORK = ROOT / "framework.yaml"

PAPERS = ROOT / "papers"
PAGE_CACHES = ROOT / "page_caches"
BENCHMARKS = ROOT / "benchmarks"
BENCHMARK_EXAMPLES = BENCHMARKS / "examples"
REGIONS_BASE = ROOT / "regions" / "base"
ASSESSMENTS = ROOT / "assessments"


# ===================================================================
# Helpers
# ===================================================================

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


def _parse_fenced(raw: str, fmt: str) -> Any:
    """Strip fences + parse. Goes through scripts/parse_llm_output.py for consistency."""
    cleaned = _run_script("parse_llm_output.py", "--format", fmt, "-", stdin=raw)
    return json.loads(cleaned) if fmt == "json" else yaml.safe_load(cleaned)


def _example_manifest() -> str:
    """Build a one-line-per-file manifest of benchmarks/examples/ for Haiku selection."""
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


def _list_base_templates() -> list[str]:
    return sorted(p.name for p in REGIONS_BASE.glob("*.yaml"))


def _read_yaml_file(filename: str, subdir: Path) -> str:
    return (subdir / filename).read_text()


# ===================================================================
# Path helpers — two scopes:
#   - PAPER-scoped  (papers/<name>/*):        inputs + paper-derived artifacts
#   - ASSESSMENT-scoped (assessments/<name>/<slug>/*): everything deployment-specific
# Re-deriving a slug (new persona) creates a fresh assessment dir alongside
# the old one; the `active_slug.txt` pointer names the "current" assessment.
# ===================================================================

def _paper_dir(name: str) -> Path:
    return PAPERS / name


def _metadata_path(name: str) -> Path:
    return _paper_dir(name) / "metadata.md"


def _paper_summary_path(name: str) -> Path:
    return _paper_dir(name) / "paper_summary.md"


def _benchmark_refs_path(name: str) -> Path:
    return _paper_dir(name) / "benchmark_refs.json"


def _assessments_root(name: str) -> Path:
    return ASSESSMENTS / name


def _active_slug_path(name: str) -> Path:
    return _assessments_root(name) / "active_slug.txt"


def _assessment_dir(name: str, slug: str) -> Path:
    return _assessments_root(name) / slug


def _deployment_desc_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "deployment_description.txt"


def _questions_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "elicitation_questions.json"


def _answers_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "elicitation_answers.json"


def _persona_prompt_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "persona_prompt.md"


def _elicitation_summary_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "elicitation_summary.md"


def _region_templates_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "region_templates.json"


def _region_yaml_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "region.yaml"


def _composed_prompt_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "composed_prompt.md"


def _scoring_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "scoring.json"


def _cost_ledger_path(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "cost_ledger.json"


def _trace_dir(name: str, slug: str) -> Path:
    return _assessment_dir(name, slug) / "traces"


def _read_slug(name: str) -> str | None:
    p = _active_slug_path(name)
    return p.read_text().strip() if p.exists() else None


# ===================================================================
# Step 0 — Derive the assessment slug from the deployment description
# ===================================================================
# Run once per assessment at pipeline init. A short Haiku call turns the
# deployment description into a human-readable slug like
# `kenya_chw_swahili_dholuo`, which scopes every downstream artifact. The
# slug is persisted to `assessments/<name>/active_slug.txt` so subsequent
# --step invocations don't re-derive it.

def step_0_derive_slug(initial_description: str, name: str) -> str:
    existing = _read_slug(name)
    if existing:
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
# Fast, lightweight step that reads only the first 1-2 pages of the PDF
# to extract basic benchmark metadata (name, domain, languages, region,
# porting strategy, source culture). This gives the elicitation step
# (Step 2) enough context to generate targeted questions without waiting
# for the full extraction pipeline.

def step_1_metadata(pdf_path: Path, name: str) -> Path:
    """Haiku reads pages 1-2 of the PDF and returns lightweight metadata."""
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
        # If only page 1 exists (single-page paper), just use that.
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
    """Merge a small set of single-page PDFs into one file."""
    args = [str(p) for p in page_paths]
    # Try pdftk first, then qpdf, then pypdf
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


def _which(cmd: str) -> bool:
    from shutil import which
    return which(cmd) is not None


# ===================================================================
# Step 3a — PDF extraction: per-page Haiku (3a-extract) + Sonnet (3a-consolidate)
# ===================================================================

def step_1a_extract(pdf_path: Path, name: str, max_workers: int = 1) -> Path:
    """Per-page Haiku extraction with on-disk caching.

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

        # === Work out what still needs a Haiku call ===
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
            # Fresh fan-out: drop any stale 1a_extract ledger + trace entries
            # so the cost of this run's pages replaces whatever was there.
            client.clear_steps("3a_extract")
            client.clear_trace_steps("3a_extract")
            print(f"[3a-extract] Split into {total} pages; extracting via Haiku "
                  f"(max_workers={max_workers})...")

        # === Fan-out with on-success cache writes ===
        def _process(page_num: int, page_pdf: Path, cache_file: Path) -> None:
            text = client.call(
                model="haiku",
                system=prompts.render("pdf_extract_page", page_num=page_num),
                user=f"Extract validity-relevant content from page {page_num}.",
                pdf_path=str(page_pdf),
                max_tokens=8192,
                step="3a_extract",
            )
            # Persist immediately so the next re-run skips this page even if
            # a later page crashes the whole step. Skip in dry-run — writing
            # the placeholder would poison the cache for real runs.
            if not client.DRY_RUN:
                cache_file.write_text(text)

        if todo:
            with ThreadPoolExecutor(max_workers=max_workers) as ex:
                futures = [ex.submit(_process, i, pp, cf) for i, pp, cf in todo]
                for fut in tqdm(as_completed(futures), total=len(futures), desc="Haiku pages"):
                    fut.result()  # surface exceptions from worker threads

    print(f"[3a-extract] Page cache at {cache_dir}")
    return cache_dir


def step_3a_consolidate(name: str, elicitation_summary: str = "") -> Path:
    """Sonnet merges per-page JSON into the two-section markdown summary.

    When an elicitation summary is provided, it guides narrative depth:
    HIGH-priority dimensions get more detailed narrative, LOWER-priority
    dimensions get briefer coverage. Quote extraction is always exhaustive.
    """
    _paper_dir(name).mkdir(parents=True, exist_ok=True)
    cache_dir = PAGE_CACHES / name
    summary_path = _paper_summary_path(name)

    page_files = sorted(cache_dir.glob("page_*.txt"))
    if not page_files:
        print(
            f"ERROR: no page cache found at {cache_dir}. Run --step 3a-extract "
            f"first.",
            file=sys.stderr,
        )
        sys.exit(1)
    page_outputs = [p.read_text() for p in page_files]
    combined = "\n\n".join(
        f"### Page {i+1} extraction\n\n{out}" for i, out in enumerate(page_outputs)
    )

    # === Append elicitation priorities if available ===
    user_msg = combined
    if elicitation_summary:
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
            f"be treated as minor details.\n\n"
            f"IMPORTANT: Priority guidance affects narrative depth only. "
            f"Quote extraction must remain exhaustive — every relevant quote "
            f"is included in the registry regardless of priority level."
        )

    print(f"[3a-consolidate] Consolidating {len(page_outputs)} per-page extractions via Sonnet...")
    summary = client.call(
        model="sonnet",
        system=prompts.load("pdf_extract_consolidate"),
        user=user_msg,
        max_tokens=32768,
        step="3a_consolidate",
    )
    summary_path.write_text(summary)
    print(f"[3a-consolidate] Paper summary written to {summary_path}")
    return summary_path


# ===================================================================
# Step 3b — Benchmark YAML: Haiku selection (3b-select) + Sonnet synthesis (3b-synthesize)
# ===================================================================

def step_3b_select(paper_summary: str, name: str) -> list[str]:
    """Haiku picks 1-2 reference benchmark YAMLs; persisted for 3b-synthesize."""
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
) -> Path:
    """Sonnet writes the benchmark YAML from selected references + elicitation context.

    When an elicitation summary is provided, the YAML includes a
    coverage_gap_analysis section cross-referencing user priorities against
    benchmark documentation.
    """
    BENCHMARKS.mkdir(exist_ok=True)
    refs_path = _benchmark_refs_path(name)
    if not refs_path.exists() and not client.DRY_RUN:
        print(
            f"ERROR: {refs_path} not found — run --step 3b-select first.",
            file=sys.stderr,
        )
        sys.exit(1)
    selected_files: list[str] = json.loads(refs_path.read_text()) if refs_path.exists() else []
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
            f"above when writing the coverage_gap_analysis section. For each "
            f"HIGH-priority dimension and each cultural topic priority, assess "
            f"whether the benchmark documents relevant content."
        )

    print("[3b-synthesize] Sonnet synthesizing benchmark YAML...")
    synthesis_raw = client.call(
        model="sonnet",
        system=prompts.load("benchmark_synthesis"),
        user=user_msg,
        max_tokens=32768,
        step="3b_synthesize",
    )
    out_path = BENCHMARKS / f"{name}.yaml"
    if client.DRY_RUN:
        return out_path
    cleaned = _run_script("parse_llm_output.py", "--format", "yaml", "-", stdin=synthesis_raw)
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
    """Interactive stdin path: prompt each question, write answers JSON."""
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
    """Merge Q+A into the Sonnet summary prompt; produce the elicitation summary."""
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

    desc_path = _deployment_desc_path(name, slug)
    initial_description = desc_path.read_text() if desc_path.exists() else ""

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
    summary_path = _elicitation_summary_path(name, slug)
    summary_path.write_text(summary)
    print(f"[2-summary] Elicitation summary written to {summary_path}")
    return summary_path


# ===================================================================
# Step 4 — Region YAML: Haiku template selection (4a-template) + Sonnet synthesis (4b-synthesize)
# ===================================================================

def step_4a_template(elicitation_summary: str, name: str, slug: str) -> list[str]:
    """Haiku picks 1-2 base region templates; persisted for 4b-synthesize."""
    out_path = _region_templates_path(name, slug)
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
    paper_summary: str,
    name: str,
    slug: str,
) -> Path:
    """Sonnet writes the assessment-specific region YAML from selected templates."""
    out_path = _region_yaml_path(name, slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    refs_path = _region_templates_path(name, slug)
    if not refs_path.exists() and not client.DRY_RUN:
        print(
            f"ERROR: {refs_path} not found — run --step 4a-template first.",
            file=sys.stderr,
        )
        sys.exit(1)
    selected: list[str] = json.loads(refs_path.read_text()) if refs_path.exists() else []
    templates_text = "\n\n".join(
        f"### Template: {fn}\n\n```yaml\n{_read_yaml_file(fn, REGIONS_BASE)}\n```"
        for fn in selected
    )
    print("[4b-synthesize] Sonnet synthesizing region YAML...")
    region_raw = client.call(
        model="sonnet",
        system=prompts.load("region_synthesis"),
        user=(
            f"Base templates:\n\n{templates_text}\n\n"
            f"Elicitation summary:\n\n{elicitation_summary}\n\n"
            f"Benchmark YAML:\n\n```yaml\n{benchmark_yaml_text}\n```\n\n"
            f"Paper summary excerpts:\n\n{paper_summary[:4000]}"
        ),
        max_tokens=16384,
        step="4b_synthesize",
    )
    if client.DRY_RUN:
        return out_path
    cleaned = _run_script("parse_llm_output.py", "--format", "yaml", "-", stdin=region_raw)
    out_path.write_text(cleaned)
    print(f"[4b-synthesize] Region YAML written to {out_path}")
    return out_path


# ===================================================================
# Step 5 — Web search enrichment (Sonnet + web_search_20250305)
# ===================================================================

def step_5_web_search(region_path: Path, benchmark_yaml_text: str, elicitation_summary: str) -> None:
    print("[5] Sonnet enriching region YAML via web_search (this may take a minute)...")
    current = region_path.read_text()
    user_msg = (
        f"Current region YAML (assessment-specific — enrich this):\n\n"
        f"```yaml\n{current}\n```\n\n"
        f"Benchmark YAML:\n\n```yaml\n{benchmark_yaml_text}\n```\n\n"
        f"Elicitation summary:\n\n{elicitation_summary}\n\n"
        f"**Start with the benchmark YAML's `coverage_gap_analysis` section.** "
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
        f"region YAML in a single ```yaml fence."
    )
    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}]
    updated_raw = client.call(
        model="sonnet",
        system=prompts.load("web_search_guide"),
        user=user_msg,
        tools=tools,
        max_tokens=16384,
        step="5_web_search",
    )
    if client.DRY_RUN:
        return
    cleaned = _run_script("parse_llm_output.py", "--format", "yaml", "-", stdin=updated_raw)
    region_path.write_text(cleaned)
    print(f"[5] Region YAML updated at {region_path}")


# ===================================================================
# Step 6 — Compose evaluation prompt (script)
# ===================================================================

def step_6_compose(
    benchmark_path: Path,
    region_path: Path,
    elicitation_path: Path,
    name: str,
    slug: str,
) -> Path:
    out_path = _composed_prompt_path(name, slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print("[6] Composing evaluation prompt via compose_prompt.py...")
    _run_script(
        "compose_prompt.py",
        "--benchmark", str(benchmark_path),
        "--region", str(region_path),
        "--framework", str(FRAMEWORK),
        "--elicitation", str(elicitation_path),
        "--region-name", slug,
        "--output", str(out_path),
    )
    return out_path


# ===================================================================
# Step 7 — Opus scoring (the one Opus call)
# ===================================================================

def step_7_score(composed_path: Path, name: str, slug: str) -> Path:
    out_path = _scoring_path(name, slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print("[7] Opus scoring (the one Opus call in the pipeline)...")
    raw = client.call(
        model="opus",
        system=prompts.load("opus_scoring_framing"),
        user=composed_path.read_text(),
        max_tokens=16384,
        step="7_score",
    )
    if client.DRY_RUN:
        return out_path
    cleaned = _run_script("parse_llm_output.py", "--format", "json", "-", stdin=raw)
    out_path.write_text(cleaned)
    print(f"[7] Results written to {out_path}")
    return out_path


# ===================================================================
# Step 8 — Report (script)
# ===================================================================

def step_8_report(results_path: Path) -> None:
    print("\n" + "=" * 60)
    print(_run_script("format_results.py", str(results_path)))


# ===================================================================
# CLI
# ===================================================================

# ===================================================================
# Persistent cost ledger — per-paper file under results/
# ===================================================================
# Each step loads this file, clears its own step labels (so a re-run of a
# single step overwrites that step's cost rather than accumulating), records
# new usage during the call, and saves. After any run the file reflects the
# "final" cost of each step executed so far — a running total of one full
# pipeline run's expected cost even if reached via many re-tries.

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
    "3a-consolidate": ["3a_consolidate"],
    "3b-select":      ["3b_select"],
    "3b-synthesize":  ["3b_synthesize"],
    "3c-verify":      [],   # script only, no API call
    "4a-template":    ["4a_template"],
    "4b-synthesize":  ["4b_synthesize"],
    "5":              ["5_web_search"],
    "6":              [],
    "7":              ["7_score"],
    "8":              [],
}


def _ledger_begin(name: str, *step_keys: str) -> None:
    """Load persistent ledger, then drop this step's prior entries."""
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
        client.clear_steps(*labels)
        # Keep the trace log in sync with the ledger: drop prior entries for
        # these step labels so the JSONL always matches a clean final-run view.
        client.clear_trace_steps(*labels)


def _ledger_end(name: str) -> None:
    """Persist the updated ledger."""
    if client.DRY_RUN:
        return
    slug = _read_slug(name)
    if not slug:
        return
    path = client.save_ledger(_cost_ledger_path(name, slug))
    print(f"[cost] Ledger updated: {path}")


def _init_assessment_paths(name: str) -> None:
    """After a slug is known, point trace + ledger at the assessment dir.

    Safe to call repeatedly. The 0_slug Haiku call lands in the in-memory
    ledger before the slug exists on disk; this function persists it once
    the slug is known and wires subsequent calls into the trace file.
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
    return p.parse_args()


def _resolve_initial_description(args: argparse.Namespace, name: str) -> str:
    """Priority: --use-case file > persona default > cached active-slug description > stdin prompt."""
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
    report = client.format_cost_report()
    if report == "(no API calls recorded)":
        return
    print("\n=== API Cost Report ===")
    print(report)


def _require_paths(name: str) -> None:
    """Paths that must exist before later steps can run in isolation."""
    pass  # Per-step checks live inside each step_* function.


def main() -> None:
    args = parse_args()

    if not args.pdf_path:
        print("ERROR: pdf_path is required", file=sys.stderr)
        sys.exit(2)
    name = Path(args.pdf_path).stem  # un-resolved: preserves expert-namespaced stems
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
    print(f"Running validity pipeline on {pdf_path.name}")
    print(f"  Persona:       {args.persona or '(stdin mode)'}")
    print(f"  Use case file: {args.use_case or '(n/a)'}")
    print(f"  Web search:    {'off' if args.no_web_search else 'on'}\n")

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

        # === Step 3a: paper -> per-page extractions -> consolidated summary ===
        _ledger_begin(name, "3a-extract")
        step_1a_extract(pdf_path, name)
        _ledger_end(name)

        _ledger_begin(name, "3a-consolidate")
        summary_path = step_3a_consolidate(name, elicitation_summary)
        paper_summary = summary_path.read_text()
        _ledger_end(name)

        # === Step 3b: paper summary -> benchmark YAML ===
        _ledger_begin(name, "3b-select")
        step_3b_select(paper_summary, name)
        _ledger_end(name)

        _ledger_begin(name, "3b-synthesize")
        benchmark_path = step_3b_synthesize(paper_summary, name, elicitation_summary)
        benchmark_yaml_text = benchmark_path.read_text()
        _ledger_end(name)

        # === Step 3c: quote provenance verification ===
        step_3c_verify(benchmark_path, summary_path, strict=args.strict_verify)

        # === Step 4: region YAML ===
        _ledger_begin(name, "4a-template")
        step_4a_template(elicitation_summary, name, slug)
        _ledger_end(name)

        _ledger_begin(name, "4b-synthesize")
        region_path = step_4b_synthesize(
            elicitation_summary, benchmark_yaml_text, paper_summary, name, slug
        )
        _ledger_end(name)

        # === Step 5: web search enrichment ===
        if not args.no_web_search:
            _ledger_begin(name, "5")
            step_5_web_search(region_path, benchmark_yaml_text, elicitation_summary)
            _ledger_end(name)

        # === Step 6-8: compose prompt, score (Opus), format report ===
        composed_path = step_6_compose(
            benchmark_path, region_path, elicitation_path, name, slug
        )

        _ledger_begin(name, "7")
        results_path = step_7_score(composed_path, name, slug)
        _ledger_end(name)

        step_8_report(results_path)
    finally:
        _print_cost_report()


def _run_single_step(args: argparse.Namespace, pdf_path: Path, name: str) -> None:
    """Execute exactly one step in isolation, reusing on-disk outputs."""
    benchmark_path = BENCHMARKS / f"{name}.yaml"
    summary_path = _paper_summary_path(name)
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
            step_1a_extract(pdf_path, name)
        elif args.step == "3a-consolidate":
            cache_dir = PAGE_CACHES / name
            if not any(cache_dir.glob("page_*.txt")) and not client.DRY_RUN:
                print(
                    f"ERROR: run --step 3a-extract first ({cache_dir} empty)",
                    file=sys.stderr,
                )
                sys.exit(1)
            elicitation_path = _elicitation_summary_path(name, slug)
            elicitation_summary = elicitation_path.read_text() if elicitation_path.exists() else ""
            _ledger_begin(name, "3a-consolidate")
            step_3a_consolidate(name, elicitation_summary)
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
            step_3b_synthesize(paper_summary, name, elicitation_summary)
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
                summary_path.read_text() if summary_path.exists() else "",
                name, slug,
            )
        elif args.step == "5":
            region_path = _region_yaml_path(name, slug)
            if not region_path.exists():
                print(
                    f"ERROR: run --step 4b-synthesize first ({region_path} missing)",
                    file=sys.stderr,
                )
                sys.exit(1)
            elicitation_path = _elicitation_summary_path(name, slug)
            _ledger_begin(name, "5")
            step_5_web_search(
                region_path, benchmark_path.read_text(), elicitation_path.read_text()
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
            step_6_compose(benchmark_path, region_path, elicitation_path, name, slug)
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
