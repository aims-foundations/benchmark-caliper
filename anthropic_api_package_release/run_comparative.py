#!/usr/bin/env python3
"""Comparative-assessment wrapper for expert-validation experiments.

Runs the validity pipeline for a *global comparator* benchmark using a
regional tuple's deployment context. The comparison is per-benchmark:
each expert-proposed regional benchmark is compared to a global counterpart
using the deployment context of the regional benchmark's *second* tuple
(tuples 2 and 4 in the expert's manifest).

Inputs:
  --source <regional_tuple_dir>   e.g. assessments/expert_xxx__milu/india_hindi_competitive_exam_prep
  --pdf    <global_pdf>           PDF of the comparator benchmark (must already exist)
  --name   <comparator_slug>      Used to namespace the new assessment dir; defaults to the PDF stem.
                                  Final paper stem becomes "<expert_id>__<comparator_slug>".
  --hf-dataset <id>               Optional HF dataset id for step 5b-da
  --hf-tuple   <key>              Optional HF subset/split key
  --dry-run                       Pass --dry-run to run_pipeline.py
  --force                         Re-run even if report.md already exists

What it does:
  1. Copies the regional tuple's deployment + elicitation artifacts into
     a new assessment directory keyed by the comparator paper stem, reusing
     the same slug so paths stay parallel.
  2. Sets active_slug.txt and places the comparator PDF at
     papers/<comparator_paper_stem>.pdf (symlinked from the source PDF).
  3. Drives run_pipeline.py through every PDF-dependent step:
       1, 3a-extract, 3a-assemble, 3a-consolidate,
       3b-select, 3b-synthesize, 3c-verify,
       4a-template, 4b-synthesize, 5, 5b-da (optional), 6, 7, 8
  4. Mirrors the final scoring/report/composed-prompt back into the source
     tuple directory under `comparative_<artifact>` so each regional tuple
     directory carries both the regional and comparative outputs side by side.

Idempotent: skips if the comparative report.md already exists; --force overrides.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import client

# Reuse exit-code constants from the stage-2 wrapper. The 5b-da step uses
# distinct exit codes so callers can tell "no HF entry" (skippable) from
# "HF entry exists but the dataset script failed" (fatal).
from run_expert_stage2 import _EXIT_NO_HF_INFO, _EXIT_HF_SCRIPT_FAILED

# === Path Constants ===
PACKAGE_ROOT = Path(__file__).resolve().parent
ASSESSMENTS_DIR = PACKAGE_ROOT / "assessments"
PAPERS_DIR = PACKAGE_ROOT / "papers"
RUN_PIPELINE = PACKAGE_ROOT / "run_pipeline.py"

# Files copied verbatim from the source tuple into the comparative assessment
# dir. These represent the frozen "expert-side" inputs that must be identical
# across the regional and comparative runs so the only changing variable is
# the benchmark PDF itself.
COPY_FILES = (
    "deployment_description.txt",
    "elicitation_questions.json",
    "elicitation_answers.json",
)

# Pipeline steps the comparative run drives, in execution order.
# We deliberately skip:
#   - step 0         : slug is reused from the source tuple (no derivation needed)
#   - step 2-questions: elicitation questions/answers are copied from the source tuple
# Step 2-summary IS run: it regenerates elicitation_summary.md using the comparator's
# metadata + the (cleaned) Q&A, so that Priority Weights and Flagged Gaps are anchored
# to the comparator rather than the regional benchmark.
STEPS = [
    ("1", [], False),
    ("2-summary", [], False),
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

# Artifacts mirrored back into the source tuple directory after a successful
# run. Prefixed with `comparative_` so they sit alongside the regional
# outputs without clobbering them.
MIRROR_ARTIFACTS = (
    "scoring.json",
    "report.md",
    "composed_prompt.md",
    "da_report.md",
)


# Derive the expert id from a regional paper stem.
# Stage-1/2 stems follow the pattern "<expert_id>__<benchmark_slug>"; we
# re-use the expert id as-is to keep the comparative paper stem in the
# same expert namespace.
def _expert_id_from_stem(paper_stem: str) -> str:
    if "__" not in paper_stem:
        raise ValueError(
            f"paper stem {paper_stem!r} is not in '<expert_id>__<benchmark>' form"
        )
    return paper_stem.split("__", 1)[0]


# Build the comparative paper stem from the source expert id and the
# comparator benchmark slug. The two-underscore join mirrors the regional
# convention so both stems sort and parse the same way.
def _comparative_paper_stem(expert_id: str, comparator_slug: str) -> str:
    return f"{expert_id}__{comparator_slug}"


# Place the comparator PDF where run_pipeline.py expects it. Uses a symlink
# when possible (cheap, leaves the source untouched); falls back to a copy
# if symlinks aren't supported on this filesystem.
def _ensure_pdf(src_pdf: Path, dst_pdf: Path) -> None:
    if dst_pdf.exists() or dst_pdf.is_symlink():
        return
    dst_pdf.parent.mkdir(parents=True, exist_ok=True)
    try:
        dst_pdf.symlink_to(src_pdf.resolve())
    except OSError:
        # Some filesystems (notably some network mounts) don't support
        # symlinks; copying gives the same downstream behavior.
        shutil.copy2(src_pdf, dst_pdf)


# Provision the comparative assessment directory by mirroring the source
# tuple's expert-side artifacts and pointing active_slug.txt at the reused
# slug. This is what lets every subsequent --step invocation resolve to
# the same on-disk path.
def _setup_assessment_dir(source_tuple_dir: Path, paper_stem: str,
                          slug: str) -> Path:
    """Copy expert-side files from source tuple into a fresh assessment dir.

    Skips files that already exist in the target — this preserves cleaned
    artifacts (e.g., sanitized elicitation_questions.json) placed by the
    clean-comparative skill before this script runs.
    """
    target_dir = ASSESSMENTS_DIR / paper_stem / slug
    target_dir.mkdir(parents=True, exist_ok=True)

    for fname in COPY_FILES:
        dst = target_dir / fname
        if dst.exists():
            continue
        src = source_tuple_dir / fname
        if not src.exists():
            raise FileNotFoundError(
                f"required source artifact {src} not found — "
                f"is stage 2 complete for this tuple?"
            )
        dst.write_bytes(src.read_bytes())

    # active_slug.txt is what run_pipeline.py reads on every --step invocation
    # to find the current assessment dir. Writing it here lets us skip --step 0.
    active_slug = ASSESSMENTS_DIR / paper_stem / "active_slug.txt"
    active_slug.write_text(slug + "\n")

    return target_dir


# Drive run_pipeline.py through every PDF-dependent step for this comparative
# run. Mirrors run_expert_stage2.run_pipeline_remaining but with the step list
# trimmed to skip elicitation-side steps that are already satisfied by the
# files we copied in.
def _run_pipeline_steps(paper_stem: str, slug: str, *,
                        hf_dataset: str | None = None,
                        hf_tuple: str | None = None,
                        dry_run: bool = False) -> None:
    pdf = PAPERS_DIR / f"{paper_stem}.pdf"
    if not pdf.exists() and not pdf.is_symlink():
        raise FileNotFoundError(f"PDF not found at {pdf}")

    for step, extra_args, optional in STEPS:
        cmd = [sys.executable, str(RUN_PIPELINE), str(pdf),
               "--step", step, *extra_args]
        # --hf-dataset is only meaningful for 5b-da, but run_pipeline.py
        # silently ignores it on other steps so we can pass it through.
        if hf_dataset:
            cmd += ["--hf-dataset", hf_dataset]
        if hf_tuple:
            cmd += ["--hf-tuple", hf_tuple]
        if dry_run:
            cmd += ["--dry-run"]

        print(f"\n{'=' * 60}")
        print(f"[comparative] --step {step} ({paper_stem}, slug={slug})")
        print(f"{'=' * 60}")
        r = subprocess.run(cmd, cwd=PACKAGE_ROOT)
        if r.returncode != 0:
            # 5b-da: "no HF info" is a soft skip (the comparator may not be
            # on HuggingFace); "HF script failed" is fatal because the data
            # is supposed to be there and something is misconfigured.
            if step == "5b-da" and r.returncode == _EXIT_NO_HF_INFO:
                print(f"  [comparative] --step {step} skipped (no HF info)")
                continue
            if step == "5b-da" and r.returncode == _EXIT_HF_SCRIPT_FAILED:
                print(f"\nFATAL: HF dataset script failed for {paper_stem}. "
                      f"Fix hf_links.json or HF access, then re-run.",
                      file=sys.stderr)
                sys.exit(1)
            if optional:
                print(f"  [comparative] --step {step} skipped (optional)")
                continue
            raise RuntimeError(
                f"run_pipeline.py --step {step} failed "
                f"(exit {r.returncode}) for {paper_stem}"
            )


# Copy the comparative run's final artifacts back into the source tuple
# directory under a `comparative_` prefix. This keeps every regional tuple
# directory self-contained: the expert form generator and any downstream
# analysis only need to look in one place to find both runs.
def _mirror_back(comparative_dir: Path, source_tuple_dir: Path) -> None:
    for artifact in MIRROR_ARTIFACTS:
        src = comparative_dir / artifact
        if not src.exists():
            continue
        dst = source_tuple_dir / f"comparative_{artifact}"
        dst.write_bytes(src.read_bytes())


def main() -> None:
    p = argparse.ArgumentParser(
        description=(
            "Run the validity pipeline for a global comparator benchmark "
            "using a regional tuple's deployment context."
        ),
    )
    p.add_argument("--source", required=True,
                   help="Path to the regional tuple's assessment directory "
                        "(e.g. assessments/expert_xxx__milu/india_hindi_competitive_exam_prep).")
    p.add_argument("--pdf", required=True,
                   help="Path to the comparator benchmark PDF.")
    p.add_argument("--name", default=None,
                   help="Comparator slug used in the new paper stem "
                        "(default: PDF stem).")
    p.add_argument("--hf-dataset", default=None,
                   help="HF dataset id for step 5b-da (optional).")
    p.add_argument("--hf-tuple", default=None,
                   help="HF subset/split key for step 5b-da (optional).")
    p.add_argument("--dry-run", action="store_true",
                   help="Pass --dry-run to run_pipeline.py (no API calls).")
    p.add_argument("--force", action="store_true",
                   help="Re-run even if comparative report.md already exists.")
    args = p.parse_args()

    if args.dry_run:
        client.DRY_RUN = True

    # === Resolve source tuple ===
    source_tuple_dir = Path(args.source).expanduser().resolve()
    if not source_tuple_dir.is_dir():
        print(f"ERROR: source dir {source_tuple_dir} not found", file=sys.stderr)
        sys.exit(1)

    # The slug is the leaf directory name; the parent's name is the source
    # paper stem (e.g. "expert_xxx__milu"). We reuse the slug verbatim so
    # the regional and comparative assessments live at parallel paths.
    slug = source_tuple_dir.name
    source_paper_stem = source_tuple_dir.parent.name

    try:
        expert_id = _expert_id_from_stem(source_paper_stem)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # === Resolve comparator name ===
    src_pdf = Path(args.pdf).expanduser().resolve()
    if not src_pdf.exists():
        print(f"ERROR: comparator PDF {src_pdf} not found", file=sys.stderr)
        sys.exit(1)

    comparator_slug = args.name or src_pdf.stem
    paper_stem = _comparative_paper_stem(expert_id, comparator_slug)

    # === Idempotency check ===
    target_dir = ASSESSMENTS_DIR / paper_stem / slug
    report_out = target_dir / "report.md"
    if report_out.exists() and not args.force:
        print(f"[skip] comparative report already exists at {report_out}")
        return

    # === Provision assessment dir & PDF ===
    print(f"[setup] expert_id={expert_id}")
    print(f"[setup] source paper stem: {source_paper_stem}")
    print(f"[setup] comparator paper stem: {paper_stem}")
    print(f"[setup] reused slug: {slug}")

    target_dir = _setup_assessment_dir(source_tuple_dir, paper_stem, slug)
    print(f"[setup] copied {len(COPY_FILES)} expert-side files into {target_dir}")

    dst_pdf = PAPERS_DIR / f"{paper_stem}.pdf"
    _ensure_pdf(src_pdf, dst_pdf)
    print(f"[setup] PDF placed at {dst_pdf}")

    # === Run pipeline ===
    try:
        _run_pipeline_steps(
            paper_stem, slug,
            hf_dataset=args.hf_dataset,
            hf_tuple=args.hf_tuple,
            dry_run=args.dry_run,
        )
    except (RuntimeError, FileNotFoundError) as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # === Mirror artifacts back to source tuple ===
    if not args.dry_run:
        _mirror_back(target_dir, source_tuple_dir)
        print(f"\n[done] comparative artifacts mirrored into {source_tuple_dir}")


if __name__ == "__main__":
    main()
