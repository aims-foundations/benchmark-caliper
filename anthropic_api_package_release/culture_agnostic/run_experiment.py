#!/usr/bin/env python3
"""Orchestrate the culture-agnostic validity gradation experiment.

Runs all 18 assessments (3 benchmarks × 2 triplets × 3 fit levels) through:

  Stage A:  Steps 0–2a — pipeline through elicitation question generation
  Stage B:  Step 2a-sim — Opus subagent simulates the user answering
  Stage C:  Steps 2b–7  — remainder of the pipeline with simulated answers

Paper PDFs are downloaded from ArXiv on first run. Paper-level pipeline
outputs (metadata, page caches, quote registry, benchmark YAML) are shared
across all 6 assessments of the same benchmark. Assessment-level outputs
(elicitation, region YAML, scoring) are per-slug.

FAIL-FAST: Every failure is fatal. If a PDF download is corrupt, a pipeline
step fails, the simulated-user call returns malformed answers, or a required
output is missing after a step claims success, the script exits immediately.
Fix the problem before re-running — idempotent caching means completed steps
won't re-execute.

Usage:
    python culture_agnostic/run_experiment.py
    python culture_agnostic/run_experiment.py --assessment gsm8k_depth_great
    python culture_agnostic/run_experiment.py --stage A
    python culture_agnostic/run_experiment.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

EXPERIMENT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = EXPERIMENT_DIR.parent
RUN_PIPELINE = PACKAGE_ROOT / "run_pipeline.py"
PAPERS_DIR = PACKAGE_ROOT / "papers"
ASSESSMENTS_DIR = PACKAGE_ROOT / "assessments"

# Short labels for pipeline step markers parsed from stdout.
# The pipeline prints "[step_label] description..." for each step.
STEP_SHORT = {
    "0": "slug", "1": "metadata", "2-questions": "questions",
    "2-stdin": "answers", "2-summary": "elicit-summary",
    "3a-extract": "pdf-extract", "3a-merge": "quote-registry",
    "3a-assemble": "quote-registry", "3a-consolidate": "paper-summary",
    "3b-select": "benchmark-refs", "3b-synthesize": "benchmark-yaml",
    "3c-verify": "quote-verify", "3c": "quote-verify",
    "4a-template": "region-template", "4a": "region-template",
    "4b-synthesize": "region-yaml", "4b": "region-yaml",
    "5": "web-search", "5b": "dataset-analysis",
    "6": "compose-prompt", "7": "opus-scoring",
    "8": "format-report", "9": "review-pdf",
}

STEP_RE = re.compile(r"^\[([^\]]+)\]")

sys.path.insert(0, str(PACKAGE_ROOT))
import client  # noqa: E402

SIMULATED_USER_PROMPT = (EXPERIMENT_DIR / "prompts" / "simulated_user.md").read_text()

ARXIV_PDF_URL = "https://arxiv.org/pdf/{arxiv_id}.pdf"

PDF_MAGIC = b"%PDF"
MIN_PDF_BYTES = 50_000  # real papers are at least ~100 KB


def fatal(msg: str) -> None:
    """Print an error and exit immediately."""
    print(f"\nFATAL: {msg}", file=sys.stderr)
    sys.exit(1)


# ===================================================================
# Resource loading and validation
# ===================================================================

def load_assessments() -> tuple[dict, list[dict]]:
    """Load benchmark metadata and assessment definitions from assessments.yaml."""
    yaml_path = EXPERIMENT_DIR / "assessments.yaml"
    if not yaml_path.exists():
        fatal(f"assessments.yaml not found at {yaml_path}")
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    if not data or "benchmarks" not in data or "assessments" not in data:
        fatal("assessments.yaml is malformed — missing 'benchmarks' or 'assessments' key")
    for i, a in enumerate(data["assessments"]):
        for field in ("slug", "benchmark", "triplet", "fit",
                      "deployment_description", "persona_context"):
            if field not in a or not a[field].strip():
                fatal(f"Assessment #{i} missing or empty field: {field}")
        if a["benchmark"] not in data["benchmarks"]:
            fatal(f"Assessment '{a['slug']}' references unknown benchmark '{a['benchmark']}'")
    return data["benchmarks"], data["assessments"]


def validate_pdf(pdf_path: Path, label: str) -> None:
    """Verify a file is a valid PDF (magic bytes + minimum size)."""
    if not pdf_path.exists():
        fatal(f"{label}: file does not exist at {pdf_path}")
    size = pdf_path.stat().st_size
    if size < MIN_PDF_BYTES:
        fatal(f"{label}: file is only {size} bytes (minimum {MIN_PDF_BYTES}). "
              f"Likely a failed download or HTML error page. Delete {pdf_path} and retry.")
    with open(pdf_path, "rb") as f:
        header = f.read(4)
    if header != PDF_MAGIC:
        fatal(f"{label}: file does not start with %PDF magic bytes "
              f"(got {header!r}). Likely an HTML error page from ArXiv. "
              f"Delete {pdf_path} and retry.")


def ensure_paper_pdf(benchmark_key: str, arxiv_id: str) -> Path:
    """Download the benchmark paper from ArXiv if not already present."""
    pdf_path = PAPERS_DIR / f"{benchmark_key}.pdf"
    if pdf_path.exists():
        validate_pdf(pdf_path, f"{benchmark_key} paper")
        return pdf_path
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    url = ARXIV_PDF_URL.format(arxiv_id=arxiv_id)
    print(f"  Downloading {benchmark_key} paper from {url}...")
    try:
        urllib.request.urlretrieve(url, pdf_path)
    except Exception as e:
        if pdf_path.exists():
            pdf_path.unlink()
        fatal(f"Failed to download {benchmark_key} paper from {url}: {e}")
    validate_pdf(pdf_path, f"{benchmark_key} paper (just downloaded)")
    print(f"  Saved to {pdf_path} ({pdf_path.stat().st_size:,} bytes)")
    return pdf_path


def write_deployment_desc(assessment: dict) -> Path:
    """Write the deployment description file for --use-case."""
    desc_dir = EXPERIMENT_DIR / "deployment_descriptions"
    desc_dir.mkdir(exist_ok=True)
    desc_path = desc_dir / f"{assessment['slug']}.txt"
    desc_path.write_text(assessment["deployment_description"].strip())
    return desc_path


# ===================================================================
# Pipeline subprocess helpers — all fail hard on non-zero exit
# ===================================================================

def run_pipeline_step(pdf_path: Path, step: str, use_case: Path | None = None,
                      extra_args: list[str] | None = None,
                      dry_run: bool = False, slug: str = "") -> None:
    """Run a single pipeline step via subprocess. Fatal on failure."""
    cmd = ["python3", str(RUN_PIPELINE), str(pdf_path), "--step", step]
    if use_case:
        cmd.extend(["--use-case", str(use_case)])
    if dry_run:
        cmd.append("--dry-run")
    if extra_args:
        cmd.extend(extra_args)
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PACKAGE_ROOT))
    if r.returncode != 0:
        stderr = r.stderr.strip() if r.stderr else "(no stderr)"
        stdout_tail = "\n".join(r.stdout.strip().split("\n")[-10:]) if r.stdout else ""
        fatal(f"Pipeline step {step} failed for {slug} (exit {r.returncode}).\n"
              f"  stderr: {stderr}\n"
              f"  stdout (last 10 lines): {stdout_tail}")


def run_pipeline_full(pdf_path: Path, use_case: Path, hf_dataset: str,
                      dry_run: bool = False, slug: str = "") -> None:
    """Run the full pipeline with live per-step progress. Fatal on failure.

    Streams stdout line-by-line via Popen, parses [step] markers, and
    prints a progress line for each new pipeline step encountered.
    stderr passes through to the terminal so streaming tokens are visible.
    """
    cmd = ["python3", str(RUN_PIPELINE), str(pdf_path),
           "--use-case", str(use_case),
           "--hf-dataset", hf_dataset,
           "--streaming"]
    if dry_run:
        cmd.append("--dry-run")

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=None,
        text=True, cwd=str(PACKAGE_ROOT),
    )

    seen_steps: list[str] = []
    all_stdout: list[str] = []

    for line in proc.stdout:
        line = line.rstrip("\n")
        all_stdout.append(line)

        m = STEP_RE.match(line)
        if not m:
            continue
        step_key = m.group(1)
        if step_key in seen_steps:
            continue

        seen_steps.append(step_key)
        label = STEP_SHORT.get(step_key, step_key)
        n = len(seen_steps)

        cached = any(w in line.lower()
                     for w in ("cached", "already exists", "already on disk"))
        skipped = "skip" in line.lower()

        if skipped:
            tag = "(skip)"
        elif cached:
            tag = "(cached)"
        else:
            tag = ""

        print(f"    [C] {n:>2}. {label} {tag}".rstrip())

    proc.wait()

    if proc.returncode != 0:
        stdout_tail = "\n".join(all_stdout[-15:])
        fatal(f"Full pipeline failed for {slug} (exit {proc.returncode}).\n"
              f"  stdout (last 15 lines):\n{stdout_tail}")


# ===================================================================
# Assessment directory lookup — match by deployment description text
# ===================================================================

def find_slug_dir(benchmark_key: str, assessment: dict) -> Path | None:
    """Find the slug directory whose deployment_description.txt matches."""
    root = ASSESSMENTS_DIR / benchmark_key
    if not root.exists():
        return None
    for slug_dir in root.iterdir():
        if not slug_dir.is_dir():
            continue
        desc_file = slug_dir / "deployment_description.txt"
        if desc_file.exists():
            if desc_file.read_text().strip() == assessment["deployment_description"].strip():
                return slug_dir
    return None


def require_slug_dir(benchmark_key: str, assessment: dict, context: str) -> Path:
    """Like find_slug_dir but fatal if not found."""
    d = find_slug_dir(benchmark_key, assessment)
    if d is None:
        fatal(f"{context}: no assessment directory found for {assessment['slug']}. "
              f"Run Stage A first.")
    return d


def has_file(benchmark_key: str, assessment: dict, filename: str) -> tuple[bool, Path | None]:
    """Check if a specific file exists in this assessment's slug dir."""
    slug_dir = find_slug_dir(benchmark_key, assessment)
    if slug_dir is None:
        return False, None
    return (slug_dir / filename).exists(), slug_dir


# ===================================================================
# Simulated user (Stage B)
# ===================================================================

def simulate_user(assessment: dict, questions_json: str) -> dict:
    """Call Opus to simulate the user answering elicitation questions.

    Returns answers as a dict: {"Q1": "...", "Q2": "...", ...}.
    Fatal on parse failure or missing answers.
    """
    prompt = SIMULATED_USER_PROMPT.format(
        deployment_description=assessment["deployment_description"].strip(),
        persona_context=assessment["persona_context"].strip(),
        questions_json=questions_json,
    )

    raw = client.call(
        model="opus",
        system="You are simulating a practitioner answering follow-up questions "
               "about their deployment context for a benchmark validity analysis tool.",
        user=prompt,
        max_tokens=4096,
        step="2a_sim",
    )

    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```\s*$", "", cleaned)

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        fatal(f"Simulated user response is not valid JSON for {assessment['slug']}.\n"
              f"  Parse error: {e}\n"
              f"  Raw response (first 500 chars): {raw[:500]}")

    # Normalize to dict format: always produce {"Q1": "...", "Q2": "...", ...}
    questions = json.loads(questions_json)
    expected_ids = [q["id"] for q in questions]

    if isinstance(parsed, list):
        raw_answers = []
        for item in parsed:
            if "id" not in item or "answer" not in item:
                fatal(f"Simulated user returned malformed array element: {item}")
            raw_answers.append((item["id"], item["answer"]))
    elif isinstance(parsed, dict):
        raw_answers = list(parsed.items())
    else:
        fatal(f"Simulated user returned unexpected type {type(parsed).__name__}")

    if len(raw_answers) != len(expected_ids):
        fatal(f"Simulated user returned {len(raw_answers)} answers but "
              f"{len(expected_ids)} questions exist for {assessment['slug']}.\n"
              f"  Expected IDs: {expected_ids}\n"
              f"  Got keys: {[k for k, _ in raw_answers]}")

    # Check if the returned keys match expected IDs exactly
    returned_keys = {k for k, _ in raw_answers}
    expected_set = set(expected_ids)

    if returned_keys == expected_set:
        answers = dict(raw_answers)
    else:
        # Opus sometimes uses dimension codes (e.g. "OO") instead of question
        # IDs (e.g. "Q3"). If the count matches, map answers by position.
        bad_keys = returned_keys - expected_set
        print(f"    [B] WARNING: Opus used wrong keys {sorted(bad_keys)}, "
              f"re-mapping by position to {expected_ids}")
        answers = {}
        for i, (_, answer_text) in enumerate(raw_answers):
            answers[expected_ids[i]] = answer_text

    for qid, answer in answers.items():
        if not isinstance(answer, str) or not answer.strip():
            fatal(f"Simulated user returned empty answer for {qid} in {assessment['slug']}")

    return answers


# ===================================================================
# Post-stage validation
# ===================================================================

def validate_stage_a_outputs(benchmark_key: str, assessment: dict) -> None:
    """Verify Stage A produced all expected outputs."""
    slug_dir = require_slug_dir(benchmark_key, assessment, "Stage A validation")

    required = ["deployment_description.txt", "elicitation_questions.json"]
    for fname in required:
        fpath = slug_dir / fname
        if not fpath.exists():
            fatal(f"Stage A completed but {fname} is missing at {fpath}")
        if fpath.stat().st_size == 0:
            fatal(f"Stage A completed but {fname} is empty at {fpath}")

    # Validate questions structure
    q_path = slug_dir / "elicitation_questions.json"
    try:
        questions = json.loads(q_path.read_text())
    except json.JSONDecodeError as e:
        fatal(f"elicitation_questions.json is not valid JSON: {e}")
    if not isinstance(questions, list) or len(questions) == 0:
        fatal(f"elicitation_questions.json is empty or not a list")
    for q in questions:
        if "id" not in q or "question" not in q:
            fatal(f"Malformed question entry (missing id or question): {q}")

    # Validate paper-level outputs
    paper_dir = PAPERS_DIR / benchmark_key
    metadata = paper_dir / "metadata.md"
    if not metadata.exists():
        fatal(f"Paper metadata missing at {metadata}")


def validate_stage_b_outputs(benchmark_key: str, assessment: dict) -> None:
    """Verify Stage B produced valid answers matching all questions."""
    slug_dir = require_slug_dir(benchmark_key, assessment, "Stage B validation")

    a_path = slug_dir / "elicitation_answers.json"
    if not a_path.exists():
        fatal(f"Stage B completed but elicitation_answers.json is missing at {a_path}")

    q_path = slug_dir / "elicitation_questions.json"
    questions = json.loads(q_path.read_text())
    answers = json.loads(a_path.read_text())

    expected_ids = {q["id"] for q in questions}
    missing = expected_ids - set(answers.keys())
    if missing:
        fatal(f"Answers file is incomplete — missing IDs: {sorted(missing)}")


def validate_stage_c_outputs(benchmark_key: str, assessment: dict,
                             dry_run: bool = False) -> None:
    """Verify Stage C produced all required outputs including DA report."""
    if dry_run:
        return
    slug_dir = require_slug_dir(benchmark_key, assessment, "Stage C validation")

    required = [
        "elicitation_summary.md",
        "paper_summary.md",
        "benchmark.yaml",
        "region.yaml",
        "composed_prompt.md",
        "scoring.json",
        "dataset_analysis_report.md",
    ]
    for fname in required:
        fpath = slug_dir / fname
        if not fpath.exists():
            fatal(f"Stage C completed but {fname} is missing at {fpath}.\n"
                  f"  This means a pipeline step silently skipped or failed.\n"
                  f"  Assessment dir: {slug_dir}")
        if fpath.stat().st_size == 0:
            fatal(f"Stage C completed but {fname} is empty at {fpath}")

    # Validate scoring structure
    scoring_path = slug_dir / "scoring.json"
    try:
        scoring = json.loads(scoring_path.read_text())
    except json.JSONDecodeError as e:
        fatal(f"scoring.json is not valid JSON: {e}")

    if not isinstance(scoring, dict):
        fatal(f"scoring.json is not a dict (got {type(scoring).__name__})")


# ===================================================================
# Stage runners
# ===================================================================

def run_stage_a(pdf_path: Path, assessment: dict, desc_path: Path,
                benchmark_key: str, dry_run: bool = False) -> None:
    """Stage A: Steps 0–2a. Fatal on any failure."""
    has_q, _ = has_file(benchmark_key, assessment, "elicitation_questions.json")
    if has_q:
        print(f"    [A] cached (questions already on disk)")
        return

    print(f"    [A] 1/3 slug")
    run_pipeline_step(pdf_path, "0", use_case=desc_path, dry_run=dry_run,
                      slug=assessment["slug"])

    print(f"    [A] 2/3 metadata")
    run_pipeline_step(pdf_path, "1", dry_run=dry_run, slug=assessment["slug"])

    print(f"    [A] 3/3 questions")
    run_pipeline_step(pdf_path, "2-questions", use_case=desc_path, dry_run=dry_run,
                      slug=assessment["slug"])

    if not dry_run:
        validate_stage_a_outputs(benchmark_key, assessment)
    print(f"    [A] done")


def run_stage_b(assessment: dict, benchmark_key: str,
                dry_run: bool = False) -> None:
    """Stage B: Opus simulates the user. Fatal on any failure."""
    has_a, _ = has_file(benchmark_key, assessment, "elicitation_answers.json")
    if has_a:
        print(f"    [B] cached (answers already on disk)")
        return

    slug_dir = require_slug_dir(benchmark_key, assessment, "Stage B")
    q_path = slug_dir / "elicitation_questions.json"
    if not q_path.exists():
        fatal(f"Stage B: elicitation_questions.json not found at {q_path}. "
              f"Run Stage A first.")

    questions_json = q_path.read_text()
    n_questions = len(json.loads(questions_json))

    if dry_run:
        print(f"    [B] (dry-run) would simulate {n_questions} answers")
        questions = json.loads(questions_json)
        placeholder = {q["id"]: "(dry-run placeholder)" for q in questions}
        (slug_dir / "elicitation_answers.json").write_text(
            json.dumps(placeholder, indent=2))
        return

    print(f"    [B] simulating user ({n_questions} questions)...")
    client.reset_ledger()
    answers = simulate_user(assessment, questions_json)

    a_path = slug_dir / "elicitation_answers.json"
    a_path.write_text(json.dumps(answers, indent=2))

    ledger_path = slug_dir / "cost_ledger.json"
    client.save_ledger(ledger_path)

    validate_stage_b_outputs(benchmark_key, assessment)
    print(f"    [B] done ({len(answers)} answers)")


def run_stage_c(pdf_path: Path, assessment: dict, desc_path: Path,
                benchmark_key: str, hf_dataset: str,
                dry_run: bool = False) -> None:
    """Stage C: Steps 2-summary through 9. Fatal on any failure."""
    has_scoring, _ = has_file(benchmark_key, assessment, "scoring.json")
    if has_scoring:
        print(f"    [C] cached (scoring already on disk)")
        return

    run_pipeline_full(pdf_path, desc_path, hf_dataset, dry_run=dry_run,
                      slug=assessment["slug"])

    validate_stage_c_outputs(benchmark_key, assessment, dry_run=dry_run)
    print(f"    [C] done")


# ===================================================================
# Pre-flight checks
# ===================================================================

def preflight(benchmarks: dict, assessments: list[dict],
              benchmark_filter: str | None) -> dict[str, Path]:
    """Verify all resources are available before starting any assessments.

    Downloads and validates paper PDFs. Returns {benchmark_key: pdf_path}.
    """
    print("Pre-flight checks")
    print("-" * 40)

    # Verify prompt template loads
    prompt_path = EXPERIMENT_DIR / "prompts" / "simulated_user.md"
    if not prompt_path.exists():
        fatal(f"Simulated user prompt missing at {prompt_path}")
    try:
        template = prompt_path.read_text()
        template.format(
            deployment_description="test",
            persona_context="test",
            questions_json="test",
        )
    except KeyError as e:
        fatal(f"Simulated user prompt has unrecognized placeholder: {e}")
    print(f"  Prompt template: OK")

    # Verify pipeline script exists
    if not RUN_PIPELINE.exists():
        fatal(f"Pipeline script missing at {RUN_PIPELINE}")
    print(f"  Pipeline script: OK")

    # Verify framework.yaml
    framework = PACKAGE_ROOT / "framework.yaml"
    if not framework.exists():
        fatal(f"framework.yaml missing at {framework}")
    print(f"  Framework YAML:  OK")

    # Verify API key is set
    import os
    if not os.environ.get("ANTHROPIC_API_KEY"):
        try:
            from dotenv import dotenv_values
            env = dotenv_values(PACKAGE_ROOT / ".env")
            if not env.get("ANTHROPIC_API_KEY"):
                fatal("ANTHROPIC_API_KEY not set in environment or .env")
        except ImportError:
            fatal("ANTHROPIC_API_KEY not set and python-dotenv not installed")
    print(f"  API key:         OK")

    # Download and validate all paper PDFs
    pdf_paths: dict[str, Path] = {}
    needed = {a["benchmark"] for a in assessments}
    for bkey, binfo in benchmarks.items():
        if benchmark_filter and bkey != benchmark_filter:
            continue
        if bkey not in needed:
            continue
        pdf_paths[bkey] = ensure_paper_pdf(bkey, binfo["paper_arxiv"])
        print(f"  Paper PDF ({bkey}): OK ({pdf_paths[bkey].stat().st_size:,} bytes)")

    # Validate all assessment slugs are unique
    slugs = [a["slug"] for a in assessments]
    dupes = [s for s in slugs if slugs.count(s) > 1]
    if dupes:
        fatal(f"Duplicate assessment slugs: {set(dupes)}")

    print(f"  Assessments:     {len(assessments)} defined, all valid")
    print()
    return pdf_paths


# ===================================================================
# Main
# ===================================================================

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run the culture-agnostic validity gradation experiment."
    )
    p.add_argument(
        "--assessment",
        help="Run only this assessment slug (e.g., gsm8k_depth_great).",
    )
    p.add_argument(
        "--benchmark",
        choices=["gsm8k", "humaneval", "folio"],
        help="Run only assessments for this benchmark.",
    )
    p.add_argument(
        "--stage",
        choices=["A", "B", "C"],
        help="Run only this stage (A=questions, B=simulate, C=pipeline).",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Re-run even if outputs already exist.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without making API calls.",
    )
    p.add_argument(
        "--list",
        action="store_true",
        dest="list_assessments",
        help="List all assessment slugs with status and exit.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    benchmarks, assessments = load_assessments()

    if args.list_assessments:
        for a in assessments:
            has_scoring, _ = has_file(a["benchmark"], a, "scoring.json")
            has_answers, _ = has_file(a["benchmark"], a, "elicitation_answers.json")
            has_questions, _ = has_file(a["benchmark"], a, "elicitation_questions.json")
            if has_scoring:
                status = "done"
            elif has_answers:
                status = "answers (needs Stage C)"
            elif has_questions:
                status = "questions (needs Stage B)"
            else:
                status = "pending"
            print(f"  {a['slug']:<35s} [{status}]")
        return

    # Filter assessments
    if args.assessment:
        assessments = [a for a in assessments if a["slug"] == args.assessment]
        if not assessments:
            all_slugs = [a["slug"] for a in load_assessments()[1]]
            fatal(f"Unknown assessment slug '{args.assessment}'. "
                  f"Valid slugs: {', '.join(all_slugs)}")
    if args.benchmark:
        assessments = [a for a in assessments if a["benchmark"] == args.benchmark]

    # Pre-flight: validate all resources before any API calls
    pdf_paths = preflight(benchmarks, assessments, args.benchmark)

    total = len(assessments)
    stage_label = f" (stage {args.stage} only)" if args.stage else ""
    print(f"Running {total} assessments{stage_label}\n")

    completed = 0
    for idx, assessment in enumerate(assessments, 1):
        slug = assessment["slug"]
        bkey = assessment["benchmark"]
        binfo = benchmarks[bkey]
        pdf_path = pdf_paths[bkey]
        hf_dataset = binfo["hf_dataset"]

        print(f"\n[{idx}/{total}] {slug}  ({bkey} / {assessment['triplet']} / {assessment['fit']})")
        print(f"{'─'*60}")

        if not args.force:
            has_scoring, _ = has_file(bkey, assessment, "scoring.json")
            if has_scoring:
                print(f"  Already complete (use --force to re-run)")
                completed += 1
                continue

        desc_path = write_deployment_desc(assessment)

        # --- Stage A ---
        if not args.stage or args.stage == "A":
            run_stage_a(pdf_path, assessment, desc_path, bkey,
                        dry_run=args.dry_run)
        if args.stage == "A":
            completed += 1
            continue

        # --- Stage B ---
        if not args.stage or args.stage == "B":
            run_stage_b(assessment, bkey, dry_run=args.dry_run)
        if args.stage == "B":
            completed += 1
            continue

        # --- Stage C ---
        if not args.stage or args.stage == "C":
            run_stage_c(pdf_path, assessment, desc_path, bkey, hf_dataset,
                        dry_run=args.dry_run)

        completed += 1

    print(f"\n{'='*60}")
    print(f"All {completed}/{len(assessments)} assessments processed successfully.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
