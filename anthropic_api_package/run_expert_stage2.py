#!/usr/bin/env python3
"""Stage-2 wrapper for expert-validation experiments.

Parses the CSV export from the Stage-2 Google Form (expert answers to
elicitation questions), writes `elicitation_answers.json` for each tuple
into the corresponding assessment directory, then drives `run_pipeline.py`
through the remaining steps (2-summary through 8) for each tuple.

Prerequisites:
  - Stage 1 must have been run for the expert (row.json, assessment slugs,
    elicitation_questions.json, PDFs all present).
  - The Stage-2 CSV must live under expert_responses/form_responses/stage_2/.

CSV layout (positional — Google Forms export):
  Col 0: Timestamp
  Col 1: Email Address
  Cols 2-6:   Tuple 1 (Q1, Q2, Q3, Q4, Feedback)
  Cols 7-11:  Tuple 2 (Q1, Q2, Q3, Q4, Feedback)
  Cols 12-16: Tuple 3 (Q1, Q2, Q3, Q4, Feedback)
  Cols 17-21: Tuple 4 (Q1, Q2, Q3, Q4, Feedback)

Idempotent: rerunning skips any tuple whose scoring output already exists.
Use --force to re-run, --parse-only to write answers without running the
pipeline, --tuple to restrict to a single tuple, --dry-run to preview
pipeline calls without hitting the API.
"""

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

import client

# run_pipeline.py exit codes for the 5b-da step
_EXIT_NO_HF_INFO = 1    # no HF entry — genuinely optional, safe to skip
_EXIT_HF_SCRIPT_FAILED = 2  # HF entry exists but sampling failed — must abort

# === Path Constants ===
# All paths are resolved relative to this script's location so the package
# remains portable regardless of the working directory at invocation time.
PACKAGE_ROOT = Path(__file__).resolve().parent
EXPERT_RESPONSES = PACKAGE_ROOT / "expert_responses"
FORM_RESPONSES_S2 = EXPERT_RESPONSES / "form_responses" / "stage_2"
ASSESSMENTS_DIR = PACKAGE_ROOT / "assessments"
RUN_PIPELINE = PACKAGE_ROOT / "run_pipeline.py"

# === CSV Layout Constants ===
# Google Forms exports columns in a fixed positional order. These constants
# encode that layout so positional math elsewhere stays readable and easy
# to update if the form schema changes.
COL_TIMESTAMP = 0
COL_EMAIL = 1
TUPLE_BLOCK_START = 2         # first column belonging to tuple data
QUESTIONS_PER_TUPLE = 4       # Q1–Q4 (excludes the trailing feedback column)
COLS_PER_TUPLE = 5            # Q1, Q2, Q3, Q4, Feedback
NUM_TUPLES = 4
EXPECTED_COLUMNS = TUPLE_BLOCK_START + NUM_TUPLES * COLS_PER_TUPLE  # 22


# Build the canonical assessment stem that links an expert to a benchmark.
# This stem is used as a subdirectory name under assessments/ and as the
# PDF filename, so it must be stable and derived the same way everywhere.
def _paper_stem(expert_id: str, bench_slug: str) -> str:
    return f"{expert_id}__{bench_slug}"


# Enumerate all expert directories that have a completed Stage-1 run.
# Stage-1 completion is proxied by the presence of row.json — if that file
# is missing the directory is treated as if it doesn't exist.
def _find_expert_dirs() -> list[Path]:
    """Return all stage-1 expert directories (those containing row.json)."""
    dirs = []
    for stage_dir in sorted(EXPERT_RESPONSES.iterdir()):
        # Skip the form_responses/ sibling directory — it holds CSVs, not
        # per-expert stage data.
        if not stage_dir.is_dir() or stage_dir.name == "form_responses":
            continue
        for expert_dir in sorted(stage_dir.iterdir()):
            if (expert_dir / "row.json").exists():
                dirs.append(expert_dir)
    return dirs


# Map a Google Forms submission back to its stage-1 expert directory using
# the respondent email as the join key. Case and whitespace are normalized
# before comparison to guard against form-entry inconsistencies.
def _match_expert_by_email(email: str, expert_dirs: list[Path]) -> Path | None:
    """Return the expert directory whose row.json email matches; None if not found."""
    email_norm = email.strip().lower()
    for d in expert_dirs:
        row = json.loads((d / "row.json").read_text())
        if row.get("email", "").strip().lower() == email_norm:
            return d
    return None


# Parse a single CSV data row into a structured per-tuple answer dict.
# The positional column layout (TUPLE_BLOCK_START, COLS_PER_TUPLE) drives
# the extraction — no header names are used, intentionally, because Google
# Forms column headers are long and unstable across form versions.
def parse_answers_from_row(raw: list) -> dict[int, dict]:
    """Extract per-tuple answer dicts from a positional CSV row.

    Returns {tuple_index (1-based): {"Q1": ..., "Q2": ..., "Q3": ..., "Q4": ..., "feedback": ...}}
    """
    # Pad with empty strings so downstream indexing never raises IndexError,
    # e.g. when a respondent left the last columns blank and the CSV was
    # exported without trailing delimiters.
    if len(raw) < EXPECTED_COLUMNS:
        raw = list(raw) + [""] * (EXPECTED_COLUMNS - len(raw))

    tuples = {}
    for t_idx in range(NUM_TUPLES):
        # Compute the starting column for this tuple's block in the row.
        offset = TUPLE_BLOCK_START + t_idx * COLS_PER_TUPLE
        answers = {}
        for q in range(QUESTIONS_PER_TUPLE):
            answers[f"Q{q + 1}"] = raw[offset + q].strip()
        # Feedback occupies the slot immediately after Q4 in each block.
        answers["feedback"] = raw[offset + QUESTIONS_PER_TUPLE].strip()
        # Use 1-based tuple index throughout to match the row.json manifest.
        tuples[t_idx + 1] = answers
    return tuples


# Write only the Q1–Q4 answers (not feedback) to the canonical location that
# run_pipeline.py's step 2-summary reads. Feedback is intentionally excluded
# here because it is metadata about the questions, not an answer to them.
def write_answers(answers: dict, assessment_dir: Path) -> Path:
    """Write elicitation_answers.json (Q1-Q4 only, no feedback) to assessment_dir.

    Returns the path of the written file.
    """
    qa = {k: v for k, v in answers.items() if k.startswith("Q")}
    out = assessment_dir / "elicitation_answers.json"
    out.write_text(json.dumps(qa, indent=2) + "\n")
    return out


# Store expert free-text feedback as a plain text file alongside the tuple
# directory. This is kept separate from elicitation_answers.json so that
# pipeline steps that consume answers are not affected by whether feedback
# was provided or not.
def write_feedback(feedback: str, tuple_dir: Path) -> Path | None:
    """Write expert question-feedback to expert_feedback.txt; returns None if empty."""
    if not feedback:
        return None
    out = tuple_dir / "expert_feedback.txt"
    out.write_text(feedback + "\n")
    return out


# Drive run_pipeline.py through every post-elicitation step for a single
# (expert, tuple) pair. Steps are listed in execution order; any step
# marked optional=True may fail without aborting the remaining steps —
# this covers steps like 5b-da which require HuggingFace metadata that
# not all benchmarks provide.
def run_pipeline_remaining(paper_stem: str, slug: str, answers_path: Path,
                           hf_tuple: str | None = None,
                           dry_run: bool = False) -> None:
    """Invoke run_pipeline.py for steps 2-summary through 8 for one tuple.

    Raises RuntimeError if a non-optional step exits non-zero.
    Raises FileNotFoundError if the paper PDF is missing.
    """
    # PDF is keyed by paper_stem and must have been placed here during Stage 1.
    pdf = PACKAGE_ROOT / "papers" / f"{paper_stem}.pdf"
    if not pdf.exists() and not pdf.is_symlink():
        raise FileNotFoundError(f"PDF not found: {pdf}")

    # Each tuple is: (step_name, extra_cli_args, is_optional).
    # Steps are invoked sequentially; a failure in a required step is fatal
    # for the whole tuple.
    steps = [
        ("2-summary", ["--answers", str(answers_path)], False),
        ("3a-extract", [], False),
        ("3a-assemble", [], False),
        ("3a-consolidate", [], False),
        ("3b-select", [], False),
        ("3b-synthesize", [], False),
        ("3c-verify", [], False),
        ("4a-template", [], False),
        ("4b-synthesize", [], False),
        ("5", [], False),
        ("5b-da", [], False),
        ("6", [], False),
        ("7", [], False),
        ("8", [], False),
    ]

    for step, extra_args, optional in steps:
        cmd = [sys.executable, str(RUN_PIPELINE), str(pdf),
               "--step", step, *extra_args]
        # Propagate HF tuple and dry-run flags when present; run_pipeline.py
        # uses --hf-tuple to scope dataset-analysis steps to the right split.
        if hf_tuple:
            cmd += ["--hf-tuple", hf_tuple]
        if dry_run:
            cmd += ["--dry-run"]
        print(f"\n{'=' * 60}")
        print(f"[stage2] --step {step} ({paper_stem}, slug={slug})")
        print(f"{'=' * 60}")
        r = subprocess.run(cmd, cwd=PACKAGE_ROOT)
        if r.returncode != 0:
            # 5b-da: skip when no HF entry exists (exit 1), but halt the
            # entire script when HF data is available and sampling failed
            # (exit 2) — we need real dataset examples whenever available.
            if step == "5b-da" and r.returncode == _EXIT_NO_HF_INFO:
                print(f"  [stage2] --step {step} skipped (no HF info for this benchmark)")
                continue
            if step == "5b-da" and r.returncode == _EXIT_HF_SCRIPT_FAILED:
                print(f"\nFATAL: HF dataset scripts failed for {paper_stem}. "
                      f"Fix hf_links.json or HF access, then re-run.",
                      file=sys.stderr)
                sys.exit(1)
            if optional:
                print(f"  [stage2] --step {step} skipped (optional step failed)")
                continue
            raise RuntimeError(
                f"run_pipeline.py --step {step} failed "
                f"(exit {r.returncode}) for {paper_stem}"
            )


# Orchestrate the full stage-2 lifecycle for a single (expert_row, tuple_idx)
# pair: validate prerequisites, write answer artifacts, optionally run the
# pipeline, and mirror outputs back to the tuple directory for easy access.
def process_tuple(row: dict, tuple_idx: int, answers: dict,
                  expert_dir: Path, *,
                  force: bool = False,
                  parse_only: bool = False,
                  dry_run: bool = False) -> str:
    """Run stage 2 for one tuple. Returns a status string:
    'done' | 'skipped' | 'answers-written' | 'failed: <reason>'
    """
    # === Resolve tuple metadata ===
    # Look up this tuple in the row manifest so we have benchmark_slug
    # for constructing the paper stem and assessment directory path.
    t = next((t for t in row["tuples"] if t["index"] == tuple_idx), None)
    if t is None:
        return f"failed: tuple {tuple_idx} not in row manifest"

    tuple_dir = expert_dir / "tuples" / f"tuple_{tuple_idx}"
    # assessment_slug.txt is written by Stage 1 when it creates the assessment
    # directory; its absence means Stage 1 did not complete for this tuple.
    slug_file = tuple_dir / "assessment_slug.txt"
    if not slug_file.exists():
        return f"failed: no assessment slug (stage 1 incomplete?)"

    slug = slug_file.read_text().strip()
    paper_stem = _paper_stem(row["expert_id"], t["benchmark_slug"])
    assessment_dir = ASSESSMENTS_DIR / paper_stem / slug

    # === Idempotency check ===
    # report.md is the final output of step 8; if it exists, the pipeline
    # already ran to completion for this tuple. Skip unless --force is set.
    report_out = assessment_dir / "report.md"
    if report_out.exists() and not force:
        print(f"[skip tuple {tuple_idx}] report already exists")
        return "skipped"

    # Check that elicitation questions exist (stage 1 prerequisite)
    # These were generated in Stage 1 and are needed by step 2-summary.
    q_path = assessment_dir / "elicitation_questions.json"
    if not q_path.exists():
        return f"failed: {q_path} missing (stage 1 incomplete?)"

    # Check answers are non-empty
    # Guard against rows where a respondent submitted without filling in
    # any answers for this tuple (all Q-values are empty strings).
    qa_answers = {k: v for k, v in answers.items() if k.startswith("Q")}
    if not any(qa_answers.values()):
        return f"failed: all answers empty for tuple {tuple_idx}"

    # === Write answer artifacts ===
    assessment_dir.mkdir(parents=True, exist_ok=True)
    answers_path = write_answers(answers, assessment_dir)
    print(f"  answers -> {answers_path.relative_to(PACKAGE_ROOT)}")

    # Feedback goes to the tuple directory, not the assessment directory,
    # because it is commentary on the elicitation questions rather than
    # input to the downstream pipeline steps.
    write_feedback(answers.get("feedback", ""), tuple_dir)

    if parse_only:
        # Caller requested answers-only mode; skip pipeline execution.
        return "answers-written"

    # === Activate slug and run pipeline ===
    # run_pipeline.py resolves the active assessment directory by reading
    # active_slug.txt; we write it here to point at this tuple's slug
    # before dispatching each step.
    active_slug = ASSESSMENTS_DIR / paper_stem / "active_slug.txt"
    active_slug.write_text(slug + "\n")

    try:
        hf_tuple = f"tuple_{tuple_idx}"
        run_pipeline_remaining(paper_stem, slug, answers_path,
                               hf_tuple=hf_tuple, dry_run=dry_run)
    except (RuntimeError, FileNotFoundError) as e:
        return f"failed: {e}"

    # === Mirror outputs to expert tuple directory ===
    # Copy key pipeline artifacts back alongside the tuple's other Stage-1
    # files so that the per-expert directory is a self-contained record of
    # both stages without needing to navigate the assessments/ tree.
    for artifact in ("scoring.json", "report.md", "composed_prompt.md",
                     "elicitation_summary.md", "da_report.md"):
        src = assessment_dir / artifact
        if src.exists():
            dst = tuple_dir / artifact
            dst.write_bytes(src.read_bytes())

    return "done"


def main() -> None:
    # === CLI argument parsing ===
    p = argparse.ArgumentParser(
        description=(
            "Stage-2 wrapper: parse expert answer CSVs, write "
            "elicitation_answers.json, and run the validity pipeline "
            "from step 2-summary through step 8 for each tuple."
        ),
    )
    p.add_argument(
        "csv_path", nargs="?",
        help="Path to a specific Stage-2 CSV. If omitted, processes all "
             "CSVs under expert_responses/form_responses/stage_2/.",
    )
    p.add_argument("--tuple", type=int, dest="tuple_idx",
                   choices=[1, 2, 3, 4],
                   help="Only process the given tuple index.")
    p.add_argument("--force", action="store_true",
                   help="Re-run tuples whose report already exists.")
    p.add_argument("--parse-only", action="store_true",
                   help="Write answers JSON only; skip pipeline execution.")
    p.add_argument("--dry-run", action="store_true",
                   help="Pass --dry-run to run_pipeline.py (no API calls).")
    args = p.parse_args()

    # Propagate dry-run flag into the client module so any direct API calls
    # made by imported helpers also respect it (not just subprocess children).
    if args.dry_run:
        client.DRY_RUN = True

    # === Resolve CSVs to process ===
    # If a specific CSV is given, use it directly; otherwise scan the canonical
    # Stage-2 form responses directory and process all files found there.
    if args.csv_path:
        csv_paths = [Path(args.csv_path).expanduser().resolve()]
    else:
        if not FORM_RESPONSES_S2.exists():
            print(f"ERROR: {FORM_RESPONSES_S2} not found", file=sys.stderr)
            sys.exit(1)
        csv_paths = sorted(FORM_RESPONSES_S2.glob("*.csv"))
        if not csv_paths:
            print(f"ERROR: no CSVs in {FORM_RESPONSES_S2}", file=sys.stderr)
            sys.exit(1)

    # Build the lookup table of stage-1 expert directories once; used for
    # email matching on every row across all CSV files.
    expert_dirs = _find_expert_dirs()
    if not expert_dirs:
        print("ERROR: no stage-1 expert directories found", file=sys.stderr)
        sys.exit(1)

    results = []

    # === Main processing loop: CSV -> expert -> tuple ===
    for csv_path in csv_paths:
        print(f"\n{'=' * 60}")
        print(f"Processing {csv_path.name}")
        print(f"{'=' * 60}")

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            # Consume (and discard) the header row — columns are addressed
            # positionally, not by name, so we only need to skip it.
            header = next(reader, None)
            if header is None:
                print(f"  WARN: {csv_path.name} is empty, skipping")
                continue

            for row_i, raw in enumerate(reader, start=1):
                # Skip blank rows that sometimes appear at the end of exports.
                if not any(c.strip() for c in raw):
                    continue

                email = raw[COL_EMAIL].strip() if len(raw) > COL_EMAIL else ""
                if not email:
                    print(f"  WARN: row {row_i} has no email, skipping")
                    continue

                # Join CSV row to its stage-1 expert directory via email.
                expert_dir = _match_expert_by_email(email, expert_dirs)
                if expert_dir is None:
                    print(f"  WARN: no stage-1 data for {email}, skipping")
                    continue

                row = json.loads((expert_dir / "row.json").read_text())
                print(f"\n  Expert: {row['name']} ({row['expert_id']})")

                # Parse all four tuples from this CSV row up front so each
                # process_tuple call can index into the result by tuple index.
                all_answers = parse_answers_from_row(raw)

                for tuple_idx in range(1, NUM_TUPLES + 1):
                    # Honor --tuple filter: skip tuples that were not requested.
                    if args.tuple_idx and tuple_idx != args.tuple_idx:
                        continue

                    # Pull benchmark name for display; fall back to "?" if the
                    # tuple is absent from the manifest (shouldn't happen in
                    # normal use, but possible with malformed row.json).
                    t = next((t for t in row["tuples"]
                              if t["index"] == tuple_idx), None)
                    bench_name = t["benchmark_name"] if t else "?"
                    print(f"\n  --- Tuple {tuple_idx} ({bench_name}) ---")

                    status = process_tuple(
                        row, tuple_idx, all_answers[tuple_idx],
                        expert_dir,
                        force=args.force,
                        parse_only=args.parse_only,
                        dry_run=args.dry_run,
                    )
                    print(f"  -> {status}")
                    results.append((row["expert_id"], tuple_idx,
                                    bench_name, status))

    # === Summary table ===
    print(f"\n{'=' * 60}")
    print("Stage-2 Summary")
    print(f"{'=' * 60}")
    for expert_id, t_idx, bench, status in results:
        print(f"  {expert_id} tuple {t_idx} ({bench}): {status}")

    # === Aggregate cost reporting ===
    # Re-scan the CSVs to find unique expert directories and emit per-expert
    # API cost totals. Skipped in parse-only or dry-run modes because no
    # API calls were made and write_costs would produce misleading zeros.
    if not args.parse_only and not args.dry_run:
        # write_costs lives in stage1 and reads the client usage ledger;
        # imported here (not at module top) to keep stage2 standalone for
        # parse-only and dry-run use.
        from run_expert_stage1 import write_costs
        seen_experts = set()
        for csv_path in csv_paths:
            with csv_path.open(newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header
                for raw in reader:
                    email = raw[COL_EMAIL].strip() if len(raw) > COL_EMAIL else ""
                    if not email:
                        continue
                    expert_dir = _match_expert_by_email(email, expert_dirs)
                    # Deduplicate by directory path in case the same expert
                    # appears in multiple CSV files (e.g., re-exports).
                    if expert_dir and expert_dir not in seen_experts:
                        seen_experts.add(expert_dir)
                        row = json.loads((expert_dir / "row.json").read_text())
                        cost_path = write_costs(row)
                        if cost_path:
                            costs = json.loads(cost_path.read_text())
                            print(f"\n  {row['name']}: ${costs['total_usd']:.4f} total")


if __name__ == "__main__":
    main()
