#!/usr/bin/env python3
"""Orchestrate the full validity analysis pipeline on a benchmark paper PDF.

Usage:
    python run_pipeline.py <pdf_path> [--persona PID] [--use-case PATH] [--no-web-search]

Pipeline stages (costs kept in line with cli_package by routing each step to the
cheapest sufficient model). Every API call has its own --step key so you can
dry-run, inspect, and pay for each one independently:
    Step 0              Haiku derives the assessment slug from the deployment description
    Step 1a-extract     split PDF -> Haiku per-page (parallel, cached)
    Step 1a-consolidate Sonnet merges per-page extractions into a paper summary
    Step 1b-select      Haiku picks 1-2 reference benchmark YAMLs
    Step 1b-synthesize  Sonnet writes the benchmark YAML
    Step 1c-verify      verify_quotes.py (script, no API)
    Step 1d-questions   Sonnet generates elicitation questions + persona handoff prompt
    Step 1d-summary     Sonnet summarizes the answered questions
    Step 2a-template    Haiku picks 1-2 base region templates
    Step 2b-synthesize  Sonnet writes the assessment-specific region YAML
    Step 3              Sonnet + web_search_20250305 server tool -> region enrichment
    Step 4              compose_prompt.py (script)
    Step 5              Opus scoring (the one Opus call in the pipeline)
    Step 6              format_results.py (script)

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
# Step 1a — PDF extraction: per-page Haiku (1a-extract) + Sonnet (1a-consolidate)
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
            print(f"[1a-extract] {cached}/{total} pages cached from prior run; "
                  f"re-dispatching {len(todo)}.")
        else:
            # Fresh fan-out: drop any stale 1a_extract ledger + trace entries
            # so the cost of this run's pages replaces whatever was there.
            client.clear_steps("1a_extract")
            client.clear_trace_steps("1a_extract")
            print(f"[1a-extract] Split into {total} pages; extracting via Haiku "
                  f"(max_workers={max_workers})...")

        # === Fan-out with on-success cache writes ===
        def _process(page_num: int, page_pdf: Path, cache_file: Path) -> None:
            text = client.call(
                model="haiku",
                system=prompts.render("pdf_extract_page", page_num=page_num),
                user=f"Extract validity-relevant content from page {page_num}.",
                pdf_path=str(page_pdf),
                max_tokens=8192,
                step="1a_extract",
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

    print(f"[1a-extract] Page cache at {cache_dir}")
    return cache_dir


def step_1a_consolidate(name: str) -> Path:
    """Sonnet merges per-page JSON into the two-section markdown summary."""
    _paper_dir(name).mkdir(parents=True, exist_ok=True)
    cache_dir = PAGE_CACHES / name
    summary_path = _paper_summary_path(name)

    page_files = sorted(cache_dir.glob("page_*.txt"))
    if not page_files:
        print(
            f"ERROR: no page cache found at {cache_dir}. Run --step 1a-extract "
            f"first.",
            file=sys.stderr,
        )
        sys.exit(1)
    page_outputs = [p.read_text() for p in page_files]
    combined = "\n\n".join(
        f"### Page {i+1} extraction\n\n{out}" for i, out in enumerate(page_outputs)
    )
    print(f"[1a-consolidate] Consolidating {len(page_outputs)} per-page extractions via Sonnet...")
    summary = client.call(
        model="sonnet",
        system=prompts.load("pdf_extract_consolidate"),
        user=combined,
        max_tokens=32768,
        step="1a_consolidate",
    )
    summary_path.write_text(summary)
    print(f"[1a-consolidate] Paper summary written to {summary_path}")
    return summary_path


# ===================================================================
# Step 1b — Benchmark YAML: Haiku selection (1b-select) + Sonnet synthesis (1b-synthesize)
# ===================================================================

def step_1b_select(paper_summary: str, name: str) -> list[str]:
    """Haiku picks 1-2 reference benchmark YAMLs; persisted for 1b-synthesize."""
    _paper_dir(name).mkdir(parents=True, exist_ok=True)
    print("[1b-select] Haiku selecting reference benchmark examples...")
    selection_raw = client.call(
        model="haiku",
        system=prompts.load("benchmark_example_selection"),
        user=(
            f"Benchmark example manifest:\n\n{_example_manifest()}\n\n"
            f"Paper summary:\n\n{paper_summary}"
        ),
        max_tokens=512,
        step="1b_select",
    )
    if client.DRY_RUN:
        return []
    selected_files = _parse_fenced(selection_raw, "json")
    _benchmark_refs_path(name).write_text(json.dumps(selected_files))
    print(f"[1b-select] Selected references: {selected_files}")
    return selected_files


def step_1b_synthesize(paper_summary: str, name: str) -> Path:
    """Sonnet writes the benchmark YAML from the selected references."""
    BENCHMARKS.mkdir(exist_ok=True)
    refs_path = _benchmark_refs_path(name)
    if not refs_path.exists() and not client.DRY_RUN:
        print(
            f"ERROR: {refs_path} not found — run --step 1b-select first.",
            file=sys.stderr,
        )
        sys.exit(1)
    selected_files: list[str] = json.loads(refs_path.read_text()) if refs_path.exists() else []
    examples_text = "\n\n".join(
        f"### Example: {fn}\n\n```yaml\n{_read_yaml_file(fn, BENCHMARK_EXAMPLES)}\n```"
        for fn in selected_files
    )
    print("[1b-synthesize] Sonnet synthesizing benchmark YAML...")
    synthesis_raw = client.call(
        model="sonnet",
        system=prompts.load("benchmark_synthesis"),
        user=f"Reference examples:\n\n{examples_text}\n\nPaper summary:\n\n{paper_summary}",
        max_tokens=32768,
        step="1b_synthesize",
    )
    out_path = BENCHMARKS / f"{name}.yaml"
    if client.DRY_RUN:
        return out_path
    cleaned = _run_script("parse_llm_output.py", "--format", "yaml", "-", stdin=synthesis_raw)
    out_path.write_text(cleaned)
    print(f"[1b-synthesize] Benchmark YAML written to {out_path}")
    return out_path


# ===================================================================
# Step 1c — Quote provenance: mechanical verify (1c-verify)
# ===================================================================

def step_1c_verify(
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
    print("[1c-verify] Running mechanical verification (verify_quotes.py)...")
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
    print("[1c-verify] WARNING: mechanical check failed but --strict-verify is "
          "off; continuing. Inspect the report above and consider re-running "
          "1a-consolidate / 1b-synthesize if the issues look substantive.",
          file=sys.stderr)
    return False


# ===================================================================
# Step 1d — Elicitation (questions + answers + summary)
# ===================================================================
# The persona branch no longer makes an API call. Instead, step_1d_questions
# emits an `assessments/<name>/<slug>/persona_prompt.md` that the user hands
# to a Claude Code Opus subagent. The subagent's JSON reply is saved to
# `assessments/<name>/<slug>/elicitation_answers.json`, and step_1d_summary
# consumes it.
# The stdin (no-persona) path collects answers inline and continues.

def step_1d_questions(
    benchmark_yaml_text: str,
    initial_description: str,
    persona_id: str | None,
    name: str,
    slug: str,
) -> tuple[Path, Path | None]:
    """Generate the elicitation question array and (for personas) the CC handoff prompt.

    Returns (questions_path, persona_prompt_path or None). The persona prompt
    is what the caller hands to a Claude Code Opus subagent; the subagent's
    JSON reply should be saved to `_answers_path(name, slug)` before running
    the summary step.
    """
    _assessment_dir(name, slug).mkdir(parents=True, exist_ok=True)

    # === Generate the structured JSON question array (Sonnet) ===
    print("[1d-questions] Sonnet generating elicitation questions...")
    questions_raw = client.call(
        model="sonnet",
        system=prompts.load("elicitation_questions"),
        user=(
            f"Benchmark YAML:\n\n```yaml\n{benchmark_yaml_text}\n```\n\n"
            f"Deployment description:\n\n{initial_description}"
        ),
        max_tokens=4096,
        step="1d_questions",
    )
    q_path = _questions_path(name, slug)
    if client.DRY_RUN:
        return q_path, None
    # Validator: fails loud on bad IDs, missing fields, or invalid dimensions.
    questions_json = _run_script("parse_elicitation_questions.py", "-", stdin=questions_raw)
    questions = json.loads(questions_json)

    q_path.write_text(questions_json)
    # Persist the deployment description (idempotent — step 0 already wrote it,
    # but keep this write so 1d-questions stays re-runnable if the user edits
    # the description manually between runs).
    _deployment_desc_path(name, slug).write_text(initial_description)
    print(f"[1d-questions] {len(questions)} questions written to {q_path}")

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
            f"    python run_pipeline.py {name}.pdf --step 1d-summary "
            f"--answers {answers_target}\n\n"
            f"---\n\n"
            f"## System prompt\n\n{system_rendered}\n\n"
            f"---\n\n"
            f"## User message\n\n"
            f"Questions:\n\n```json\n{json.dumps(questions, indent=2)}\n```\n"
        )
        print(f"[1d-questions] Persona handoff prompt written to {persona_prompt_path}")

    return q_path, persona_prompt_path


def step_1d_collect_stdin(name: str, slug: str) -> Path:
    """Interactive stdin path: prompt each question, write answers JSON."""
    q_path = _questions_path(name, slug)
    if not q_path.exists():
        print(f"ERROR: {q_path} not found — run step 1d-questions first", file=sys.stderr)
        sys.exit(1)
    questions = json.loads(q_path.read_text())
    print("[1d-stdin] Collecting answers interactively...")
    answers = {}
    for q in questions:
        print(f"\n{q['id']} [{q['dimension']}]: {q['question']}")
        answers[q["id"]] = input("> ").strip()
    a_path = _answers_path(name, slug)
    a_path.write_text(json.dumps(answers, indent=2))
    print(f"[1d-stdin] Answers written to {a_path}")
    return a_path


def step_1d_summary(
    name: str,
    slug: str,
    benchmark_yaml_text: str,
    answers_path: Path | None = None,
) -> Path:
    """Merge Q+A into the Sonnet summary prompt; produce the elicitation summary."""
    q_path = _questions_path(name, slug)
    if not q_path.exists():
        print(f"ERROR: {q_path} not found — run step 1d-questions first", file=sys.stderr)
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

    print("[1d-summary] Sonnet producing elicitation summary...")
    summary = client.call(
        model="sonnet",
        system=prompts.load("elicitation_summary"),
        user=(
            f"Deployment description:\n\n{initial_description}\n\n"
            f"Benchmark YAML:\n\n```yaml\n{benchmark_yaml_text}\n```\n\n"
            f"Questions & answers:\n\n{qa_block}"
        ),
        max_tokens=8192,
        step="1d_summary",
    )
    summary_path = _elicitation_summary_path(name, slug)
    summary_path.write_text(summary)
    print(f"[1d-summary] Elicitation summary written to {summary_path}")
    return summary_path


# ===================================================================
# Step 2 — Region YAML: Haiku template selection (2a-template) + Sonnet synthesis (2b-synthesize)
# ===================================================================

def step_2a_template(elicitation_summary: str, name: str, slug: str) -> list[str]:
    """Haiku picks 1-2 base region templates; persisted for 2b-synthesize."""
    out_path = _region_templates_path(name, slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print("[2a-template] Haiku selecting base region template(s)...")
    selection_raw = client.call(
        model="haiku",
        system=prompts.load("region_template_selection"),
        user=(
            f"Base template files:\n{chr(10).join(_list_base_templates())}\n\n"
            f"Elicitation summary:\n\n{elicitation_summary}"
        ),
        max_tokens=256,
        step="2a_template",
    )
    if client.DRY_RUN:
        return []
    selected = _parse_fenced(selection_raw, "json")
    out_path.write_text(json.dumps(selected))
    print(f"[2a-template] Selected templates: {selected}")
    return selected


def step_2b_synthesize(
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
            f"ERROR: {refs_path} not found — run --step 2a-template first.",
            file=sys.stderr,
        )
        sys.exit(1)
    selected: list[str] = json.loads(refs_path.read_text()) if refs_path.exists() else []
    templates_text = "\n\n".join(
        f"### Template: {fn}\n\n```yaml\n{_read_yaml_file(fn, REGIONS_BASE)}\n```"
        for fn in selected
    )
    print("[2b-synthesize] Sonnet synthesizing region YAML...")
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
        step="2b_synthesize",
    )
    if client.DRY_RUN:
        return out_path
    cleaned = _run_script("parse_llm_output.py", "--format", "yaml", "-", stdin=region_raw)
    out_path.write_text(cleaned)
    print(f"[2b-synthesize] Region YAML written to {out_path}")
    return out_path


# ===================================================================
# Step 3 — Web search enrichment (Sonnet + web_search_20250305)
# ===================================================================

def step_3_web_search(region_path: Path, benchmark_yaml_text: str, elicitation_summary: str) -> None:
    print("[3] Sonnet enriching region YAML via web_search (this may take a minute)...")
    current = region_path.read_text()
    user_msg = (
        f"Current region YAML (assessment-specific — enrich this):\n\n"
        f"```yaml\n{current}\n```\n\n"
        f"Benchmark YAML:\n\n```yaml\n{benchmark_yaml_text}\n```\n\n"
        f"Elicitation summary:\n\n{elicitation_summary}\n\n"
        f"The upstream step (2b) produced a scaffold without tool access, so "
        f"every factual slot it could not confidently ground was left as "
        f"`[NEEDS VERIFICATION]`. These tags are your primary search targets — "
        f"resolve as many as your search budget allows, replacing each tag with "
        f"a verified value (or, if the value genuinely cannot be found, a short "
        f"note explaining why and citing what was searched). You may also add "
        f"net-new fields surfaced by your searches; do not drop or silently "
        f"overwrite fields that were filled directly by 2b.\n\n"
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
        step="3_web_search",
    )
    if client.DRY_RUN:
        return
    cleaned = _run_script("parse_llm_output.py", "--format", "yaml", "-", stdin=updated_raw)
    region_path.write_text(cleaned)
    print(f"[3] Region YAML updated at {region_path}")


# ===================================================================
# Step 4 — Compose evaluation prompt (script)
# ===================================================================

def step_4_compose(
    benchmark_path: Path,
    region_path: Path,
    elicitation_path: Path,
    name: str,
    slug: str,
) -> Path:
    out_path = _composed_prompt_path(name, slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print("[4] Composing evaluation prompt via compose_prompt.py...")
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
# Step 5 — Opus scoring (the one Opus call)
# ===================================================================

def step_5_score(composed_path: Path, name: str, slug: str) -> Path:
    out_path = _scoring_path(name, slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print("[5] Opus scoring (the one Opus call in the pipeline)...")
    raw = client.call(
        model="opus",
        system=prompts.load("opus_scoring_framing"),
        user=composed_path.read_text(),
        max_tokens=16384,
        step="5_score",
    )
    if client.DRY_RUN:
        return out_path
    cleaned = _run_script("parse_llm_output.py", "--format", "json", "-", stdin=raw)
    out_path.write_text(cleaned)
    print(f"[5] Results written to {out_path}")
    return out_path


# ===================================================================
# Step 6 — Report (script)
# ===================================================================

def step_6_report(results_path: Path) -> None:
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
    # Note: "1a_extract" is NOT cleared by _ledger_begin, because the per-page
    # cache lets a retry skip pages that already succeeded. Clearing it here
    # would erase the cost of those successful pages and under-count the true
    # expected cost. Instead, step_1a_extract clears this label itself when it
    # detects a fresh (no-cache) run.
    "1a-extract":     [],
    "1a-consolidate": ["1a_consolidate"],
    "1b-select":      ["1b_select"],
    "1b-synthesize":  ["1b_synthesize"],
    "1c-verify":      [],   # script only, no API call
    "1d-questions":   ["1d_questions"],
    "1d-summary":     ["1d_summary"],
    "2a-template":    ["2a_template"],
    "2b-synthesize":  ["2b_synthesize"],
    "3":              ["3_web_search"],
    "4":              [],
    "5":              ["5_score"],
    "6":              [],
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
        help="Skip Step 3 (web search enrichment)",
    )
    p.add_argument(
        "--step",
        choices=sorted(STEP_LABELS),
        help="Run a single pipeline step (default: run all steps end-to-end).",
    )
    p.add_argument(
        "--answers",
        help="Path to an answers JSON file (used with --step 1d-summary after "
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
        "Handy with --step 1a-extract (1 worker) to watch page extractions.",
    )
    p.add_argument(
        "--strict-verify",
        action="store_true",
        help="Halt the pipeline if the 1c-verify mechanical check fails. "
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
    pdf_path = Path(args.pdf_path).resolve()
    name = pdf_path.stem

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
        # === Step 0: derive the assessment slug; everything downstream is
        # scoped under <name>/<slug>/. Resolving initial_description up front
        # forces the user to commit to a deployment early so trace+ledger can
        # be slug-scoped from the very first API call. ===
        initial_description = _resolve_initial_description(args, name)
        slug = step_0_derive_slug(initial_description, name)
        _init_assessment_paths(name)

        # === Step 1a: paper -> per-page extractions -> consolidated summary ===
        _ledger_begin(name, "1a-extract")
        step_1a_extract(pdf_path, name)
        _ledger_end(name)

        _ledger_begin(name, "1a-consolidate")
        summary_path = step_1a_consolidate(name)
        paper_summary = summary_path.read_text()
        _ledger_end(name)

        # === Step 1b: paper summary -> benchmark YAML ===
        _ledger_begin(name, "1b-select")
        step_1b_select(paper_summary, name)
        _ledger_end(name)

        _ledger_begin(name, "1b-synthesize")
        benchmark_path = step_1b_synthesize(paper_summary, name)
        benchmark_yaml_text = benchmark_path.read_text()
        _ledger_end(name)

        # === Step 1c: quote provenance verification ===
        step_1c_verify(benchmark_path, summary_path, strict=args.strict_verify)

        # === Step 1d: elicit the deployment context ===
        _ledger_begin(name, "1d-questions")
        q_path, persona_prompt_path = step_1d_questions(
            benchmark_yaml_text, initial_description, args.persona, name, slug
        )
        _ledger_end(name)

        # Persona mode pauses for the CC Opus subagent handoff. The user
        # dispatches the subagent, saves its JSON reply, and re-invokes with
        # --step 1d-summary --answers <path>. Non-persona mode continues with
        # an interactive stdin loop.
        if args.persona:
            answers_target = _answers_path(name, slug)
            print(
                f"\n[pause] Persona elicitation requires a Claude Code Opus subagent.\n"
                f"        1. Open {persona_prompt_path}\n"
                f"        2. Dispatch a CC Opus subagent with the system prompt + user message\n"
                f"        3. Save the subagent's JSON reply to {answers_target}\n"
                f"        4. Resume: python run_pipeline.py {pdf_path.name} "
                f"--step 1d-summary --answers {answers_target}\n"
            )
            return

        step_1d_collect_stdin(name, slug)

        _ledger_begin(name, "1d-summary")
        elicitation_path = step_1d_summary(name, slug, benchmark_yaml_text)
        elicitation_summary = elicitation_path.read_text()
        _ledger_end(name)

        # === Step 2-3: region YAML + optional web-search enrichment ===
        _ledger_begin(name, "2a-template")
        step_2a_template(elicitation_summary, name, slug)
        _ledger_end(name)

        _ledger_begin(name, "2b-synthesize")
        region_path = step_2b_synthesize(
            elicitation_summary, benchmark_yaml_text, paper_summary, name, slug
        )
        _ledger_end(name)

        if not args.no_web_search:
            _ledger_begin(name, "3")
            step_3_web_search(region_path, benchmark_yaml_text, elicitation_summary)
            _ledger_end(name)

        # === Step 4-6: compose prompt, score (Opus), format report ===
        composed_path = step_4_compose(
            benchmark_path, region_path, elicitation_path, name, slug
        )

        _ledger_begin(name, "5")
        results_path = step_5_score(composed_path, name, slug)
        _ledger_end(name)

        step_6_report(results_path)
    finally:
        # Always surface the per-step cost breakdown — even on crash, so a
        # mid-pipeline failure still tells you what you just spent.
        _print_cost_report()


def _run_single_step(args: argparse.Namespace, pdf_path: Path, name: str) -> None:
    """Execute exactly one step in isolation, reusing on-disk outputs."""
    benchmark_path = BENCHMARKS / f"{name}.yaml"
    summary_path = _paper_summary_path(name)

    # Step 0 derives the slug and then wires trace+ledger at the assessment
    # dir. Every other single-step invocation requires the slug to already be
    # on disk (from an earlier `--step 0`) — otherwise we have no idea where
    # to park the trace/ledger for this assessment.
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
        if args.step == "1a-extract":
            _ledger_begin(name, "1a-extract")
            step_1a_extract(pdf_path, name)
        elif args.step == "1a-consolidate":
            cache_dir = PAGE_CACHES / name
            if not any(cache_dir.glob("page_*.txt")) and not client.DRY_RUN:
                print(
                    f"ERROR: run --step 1a-extract first ({cache_dir} empty)",
                    file=sys.stderr,
                )
                sys.exit(1)
            _ledger_begin(name, "1a-consolidate")
            step_1a_consolidate(name)
        elif args.step == "1b-select":
            if not summary_path.exists() and not client.DRY_RUN:
                print(f"ERROR: run --step 1a-consolidate first ({summary_path} missing)",
                      file=sys.stderr)
                sys.exit(1)
            paper_summary = summary_path.read_text() if summary_path.exists() else ""
            _ledger_begin(name, "1b-select")
            step_1b_select(paper_summary, name)
        elif args.step == "1b-synthesize":
            if not summary_path.exists() and not client.DRY_RUN:
                print(f"ERROR: run --step 1a-consolidate first ({summary_path} missing)",
                      file=sys.stderr)
                sys.exit(1)
            paper_summary = summary_path.read_text() if summary_path.exists() else ""
            _ledger_begin(name, "1b-synthesize")
            step_1b_synthesize(paper_summary, name)
        elif args.step == "1c-verify":
            if not benchmark_path.exists() or not summary_path.exists():
                print("ERROR: run --step 1a-consolidate + 1b-synthesize first",
                      file=sys.stderr)
                sys.exit(1)
            step_1c_verify(benchmark_path, summary_path, strict=args.strict_verify)
        elif args.step == "1d-questions":
            if not benchmark_path.exists():
                print("ERROR: run step 1b first", file=sys.stderr)
                sys.exit(1)
            initial_description = _resolve_initial_description(args, name)
            _ledger_begin(name, "1d-questions")
            _, persona_prompt_path = step_1d_questions(
                benchmark_path.read_text(), initial_description, args.persona,
                name, slug,
            )
            if persona_prompt_path:
                answers_target = _answers_path(name, slug)
                print(
                    f"\n[next] Hand {persona_prompt_path} to a CC Opus subagent, "
                    f"save its JSON to {answers_target}, then:\n"
                    f"       python run_pipeline.py {pdf_path.name} "
                    f"--step 1d-summary --answers {answers_target}\n"
                )
        elif args.step == "1d-summary":
            if not benchmark_path.exists():
                print("ERROR: run step 1b first", file=sys.stderr)
                sys.exit(1)
            _ledger_begin(name, "1d-summary")
            step_1d_summary(
                name,
                slug,
                benchmark_path.read_text(),
                answers_path=Path(args.answers) if args.answers else None,
            )
        elif args.step == "2a-template":
            elicitation_path = _elicitation_summary_path(name, slug)
            if not elicitation_path.exists() and not client.DRY_RUN:
                print("ERROR: run --step 1d-summary first", file=sys.stderr)
                sys.exit(1)
            _ledger_begin(name, "2a-template")
            step_2a_template(
                elicitation_path.read_text() if elicitation_path.exists() else "",
                name, slug,
            )
        elif args.step == "2b-synthesize":
            elicitation_path = _elicitation_summary_path(name, slug)
            if (not elicitation_path.exists() or not benchmark_path.exists()) \
                    and not client.DRY_RUN:
                print("ERROR: run --step 1b-synthesize + 1d-summary first",
                      file=sys.stderr)
                sys.exit(1)
            _ledger_begin(name, "2b-synthesize")
            step_2b_synthesize(
                elicitation_path.read_text() if elicitation_path.exists() else "",
                benchmark_path.read_text() if benchmark_path.exists() else "",
                summary_path.read_text() if summary_path.exists() else "",
                name, slug,
            )
        elif args.step == "3":
            region_path = _region_yaml_path(name, slug)
            if not region_path.exists():
                print(
                    f"ERROR: run --step 2b-synthesize first ({region_path} missing)",
                    file=sys.stderr,
                )
                sys.exit(1)
            elicitation_path = _elicitation_summary_path(name, slug)
            _ledger_begin(name, "3")
            step_3_web_search(
                region_path, benchmark_path.read_text(), elicitation_path.read_text()
            )
        elif args.step == "4":
            region_path = _region_yaml_path(name, slug)
            if not region_path.exists():
                print(
                    f"ERROR: run --step 2b-synthesize first ({region_path} missing)",
                    file=sys.stderr,
                )
                sys.exit(1)
            elicitation_path = _elicitation_summary_path(name, slug)
            step_4_compose(benchmark_path, region_path, elicitation_path, name, slug)
        elif args.step == "5":
            composed_path = _composed_prompt_path(name, slug)
            if not composed_path.exists():
                print(f"ERROR: run step 4 first ({composed_path} missing)", file=sys.stderr)
                sys.exit(1)
            _ledger_begin(name, "5")
            step_5_score(composed_path, name, slug)
        elif args.step == "6":
            results_path = _scoring_path(name, slug)
            if not results_path.exists():
                print(f"ERROR: run step 5 first ({results_path} missing)", file=sys.stderr)
                sys.exit(1)
            step_6_report(results_path)
        else:
            print(f"ERROR: unknown --step {args.step}", file=sys.stderr)
            sys.exit(2)
    finally:
        # Persist the ledger for any known step. Empty-label steps still
        # need this: 1a-extract fires API calls but has no pre-declared labels
        # to clear (it clears them internally when a fresh cache is detected).
        # Pure-script steps (1c-verify, 4, 6) are no-op saves — cheap and safe.
        if args.step in STEP_LABELS:
            _ledger_end(name)
        _print_cost_report()


if __name__ == "__main__":
    main()
