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

PACKAGE_ROOT = Path(__file__).resolve().parent
EXPERT_RESPONSES = PACKAGE_ROOT / "expert_responses"
FORM_RESPONSES_S2 = EXPERT_RESPONSES / "form_responses" / "stage_2"
ASSESSMENTS_DIR = PACKAGE_ROOT / "assessments"
RUN_PIPELINE = PACKAGE_ROOT / "run_pipeline.py"

COL_TIMESTAMP = 0
COL_EMAIL = 1
TUPLE_BLOCK_START = 2
QUESTIONS_PER_TUPLE = 4
COLS_PER_TUPLE = 5  # Q1, Q2, Q3, Q4, Feedback
NUM_TUPLES = 4
EXPECTED_COLUMNS = TUPLE_BLOCK_START + NUM_TUPLES * COLS_PER_TUPLE  # 22


def _paper_stem(expert_id: str, bench_slug: str) -> str:
    return f"{expert_id}__{bench_slug}"


def _find_expert_dirs() -> list[Path]:
    """Find all stage-1 expert directories (those containing row.json)."""
    dirs = []
    for stage_dir in sorted(EXPERT_RESPONSES.iterdir()):
        if not stage_dir.is_dir() or stage_dir.name == "form_responses":
            continue
        for expert_dir in sorted(stage_dir.iterdir()):
            if (expert_dir / "row.json").exists():
                dirs.append(expert_dir)
    return dirs


def _match_expert_by_email(email: str, expert_dirs: list[Path]) -> Path | None:
    """Find the expert directory whose row.json matches the given email."""
    email_norm = email.strip().lower()
    for d in expert_dirs:
        row = json.loads((d / "row.json").read_text())
        if row.get("email", "").strip().lower() == email_norm:
            return d
    return None


def parse_answers_from_row(raw: list) -> dict[int, dict]:
    """Extract per-tuple answer dicts from a CSV row.

    Returns {tuple_index: {"Q1": "...", ..., "feedback": "..."}}
    """
    if len(raw) < EXPECTED_COLUMNS:
        raw = list(raw) + [""] * (EXPECTED_COLUMNS - len(raw))

    tuples = {}
    for t_idx in range(NUM_TUPLES):
        offset = TUPLE_BLOCK_START + t_idx * COLS_PER_TUPLE
        answers = {}
        for q in range(QUESTIONS_PER_TUPLE):
            answers[f"Q{q + 1}"] = raw[offset + q].strip()
        answers["feedback"] = raw[offset + QUESTIONS_PER_TUPLE].strip()
        tuples[t_idx + 1] = answers
    return tuples


def write_answers(answers: dict, assessment_dir: Path) -> Path:
    """Write elicitation_answers.json (Q1-Q4 only, no feedback) to the
    assessment directory. Feedback is stored separately."""
    qa = {k: v for k, v in answers.items() if k.startswith("Q")}
    out = assessment_dir / "elicitation_answers.json"
    out.write_text(json.dumps(qa, indent=2) + "\n")
    return out


def write_feedback(feedback: str, tuple_dir: Path) -> Path | None:
    """Write expert feedback on generated questions (if any)."""
    if not feedback:
        return None
    out = tuple_dir / "expert_feedback.txt"
    out.write_text(feedback + "\n")
    return out


def run_pipeline_remaining(paper_stem: str, slug: str, answers_path: Path,
                           hf_tuple: str | None = None,
                           dry_run: bool = False) -> None:
    """Run pipeline steps 2-summary through 8 for one tuple."""
    pdf = PACKAGE_ROOT / "papers" / f"{paper_stem}.pdf"
    if not pdf.exists() and not pdf.is_symlink():
        raise FileNotFoundError(f"PDF not found: {pdf}")

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
        ("5b-da", [], True),   # optional — fails gracefully if no HF info
        ("6", [], False),
        ("7", [], False),
        ("8", [], False),
    ]

    for step, extra_args, optional in steps:
        cmd = [sys.executable, str(RUN_PIPELINE), str(pdf),
               "--step", step, *extra_args]
        if hf_tuple:
            cmd += ["--hf-tuple", hf_tuple]
        if dry_run:
            cmd += ["--dry-run"]
        print(f"\n{'=' * 60}")
        print(f"[stage2] --step {step} ({paper_stem}, slug={slug})")
        print(f"{'=' * 60}")
        r = subprocess.run(cmd, cwd=PACKAGE_ROOT)
        if r.returncode != 0:
            if optional:
                print(f"  [stage2] --step {step} skipped (no HF info or not applicable)")
                continue
            raise RuntimeError(
                f"run_pipeline.py --step {step} failed "
                f"(exit {r.returncode}) for {paper_stem}"
            )


def process_tuple(row: dict, tuple_idx: int, answers: dict,
                  expert_dir: Path, *,
                  force: bool = False,
                  parse_only: bool = False,
                  dry_run: bool = False) -> str:
    """Process one tuple through stage 2.
    Returns 'done' | 'skipped' | 'answers-written' | 'failed: <reason>'."""
    t = next((t for t in row["tuples"] if t["index"] == tuple_idx), None)
    if t is None:
        return f"failed: tuple {tuple_idx} not in row manifest"

    tuple_dir = expert_dir / "tuples" / f"tuple_{tuple_idx}"
    slug_file = tuple_dir / "assessment_slug.txt"
    if not slug_file.exists():
        return f"failed: no assessment slug (stage 1 incomplete?)"

    slug = slug_file.read_text().strip()
    paper_stem = _paper_stem(row["expert_id"], t["benchmark_slug"])
    assessment_dir = ASSESSMENTS_DIR / paper_stem / slug

    scoring_out = assessment_dir / "scoring_output.json"
    if scoring_out.exists() and not force:
        print(f"[skip tuple {tuple_idx}] scoring output already exists")
        return "skipped"

    # Check that elicitation questions exist (stage 1 prerequisite)
    q_path = assessment_dir / "elicitation_questions.json"
    if not q_path.exists():
        return f"failed: {q_path} missing (stage 1 incomplete?)"

    # Check answers are non-empty
    qa_answers = {k: v for k, v in answers.items() if k.startswith("Q")}
    if not any(qa_answers.values()):
        return f"failed: all answers empty for tuple {tuple_idx}"

    # Write answers to assessment directory
    assessment_dir.mkdir(parents=True, exist_ok=True)
    answers_path = write_answers(answers, assessment_dir)
    print(f"  answers -> {answers_path.relative_to(PACKAGE_ROOT)}")

    # Write feedback to tuple directory
    write_feedback(answers.get("feedback", ""), tuple_dir)

    if parse_only:
        return "answers-written"

    # Set the active slug so run_pipeline.py resolves it
    active_slug = ASSESSMENTS_DIR / paper_stem / "active_slug.txt"
    active_slug.write_text(slug + "\n")

    try:
        hf_tuple = f"tuple_{tuple_idx}"
        run_pipeline_remaining(paper_stem, slug, answers_path,
                               hf_tuple=hf_tuple, dry_run=dry_run)
    except (RuntimeError, FileNotFoundError) as e:
        return f"failed: {e}"

    # Copy final outputs back to expert tuple dir for easy access
    for artifact in ("scoring_output.json", "composed_prompt.md",
                     "elicitation_summary.md", "da_report.md"):
        src = assessment_dir / artifact
        if src.exists():
            dst = tuple_dir / artifact
            dst.write_bytes(src.read_bytes())

    return "done"


def main() -> None:
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
                   help="Re-run tuples whose scoring output already exists.")
    p.add_argument("--parse-only", action="store_true",
                   help="Write answers JSON only; skip pipeline execution.")
    p.add_argument("--dry-run", action="store_true",
                   help="Pass --dry-run to run_pipeline.py (no API calls).")
    args = p.parse_args()

    if args.dry_run:
        client.DRY_RUN = True

    # Collect CSVs to process
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

    expert_dirs = _find_expert_dirs()
    if not expert_dirs:
        print("ERROR: no stage-1 expert directories found", file=sys.stderr)
        sys.exit(1)

    results = []

    for csv_path in csv_paths:
        print(f"\n{'=' * 60}")
        print(f"Processing {csv_path.name}")
        print(f"{'=' * 60}")

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header is None:
                print(f"  WARN: {csv_path.name} is empty, skipping")
                continue

            for row_i, raw in enumerate(reader, start=1):
                if not any(c.strip() for c in raw):
                    continue

                email = raw[COL_EMAIL].strip() if len(raw) > COL_EMAIL else ""
                if not email:
                    print(f"  WARN: row {row_i} has no email, skipping")
                    continue

                expert_dir = _match_expert_by_email(email, expert_dirs)
                if expert_dir is None:
                    print(f"  WARN: no stage-1 data for {email}, skipping")
                    continue

                row = json.loads((expert_dir / "row.json").read_text())
                print(f"\n  Expert: {row['name']} ({row['expert_id']})")

                all_answers = parse_answers_from_row(raw)

                for tuple_idx in range(1, NUM_TUPLES + 1):
                    if args.tuple_idx and tuple_idx != args.tuple_idx:
                        continue

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

    # Summary
    print(f"\n{'=' * 60}")
    print("Stage-2 Summary")
    print(f"{'=' * 60}")
    for expert_id, t_idx, bench, status in results:
        print(f"  {expert_id} tuple {t_idx} ({bench}): {status}")

    # Aggregate costs for completed experts
    if not args.parse_only and not args.dry_run:
        from run_expert_stage1 import write_costs
        seen_experts = set()
        for csv_path in csv_paths:
            with csv_path.open(newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for raw in reader:
                    email = raw[COL_EMAIL].strip() if len(raw) > COL_EMAIL else ""
                    if not email:
                        continue
                    expert_dir = _match_expert_by_email(email, expert_dirs)
                    if expert_dir and expert_dir not in seen_experts:
                        seen_experts.add(expert_dir)
                        row = json.loads((expert_dir / "row.json").read_text())
                        cost_path = write_costs(row)
                        if cost_path:
                            costs = json.loads(cost_path.read_text())
                            print(f"\n  {row['name']}: ${costs['total_usd']:.4f} total")


if __name__ == "__main__":
    main()
