"""Step 8 (report.md) and Step 9 (review.pdf) — deterministic, no API calls.

These steps are pure-Python script invocations on the upstream artifacts
produced by Step 7. We import directly from the release package so the
website produces byte-identical output to the CLI pipeline.

Step 9 expects a per-run "tuple directory" on disk containing:
  - scoring.json            (Step 7 output)
  - composed_prompt.md      (Step 6 output, used for quote-registry parsing)
  - report.md               (Step 8 output, used for limitations parsing)
  - deployment_description.txt (user input)

We materialise that directory under `data/tuples/<run_id>/` and pass it to
`scripts.stage3.generate_expert_pdfs.process_tuple()` to produce the seven
per-dimension PDFs, then merge them with pypdf into review.pdf.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

# Make the release package importable for `scripts.format_results` and
# `scripts.stage3.generate_expert_pdfs`. The package ships without a
# setup.py — putting its root on sys.path is the minimum needed.
_PACKAGE_ROOT = (
    Path(__file__).resolve().parent.parent.parent / "anthropic_api_package_release"
)
if str(_PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(_PACKAGE_ROOT))


_WORKSPACE_ROOT = Path(__file__).resolve().parent / "data" / "tuples"

# Matches anthropic_api_package_release/run_pipeline.py:REVIEW_DIMENSION_ORDER
REVIEW_DIMENSION_ORDER = ["summary", "io", "ic", "if", "oo", "oc", "of"]


def workspace_dir(run_id: str) -> Path:
    d = _WORKSPACE_ROOT / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_tuple_inputs(
    run_id: str,
    *,
    scoring: dict,
    composed_prompt: str,
    deployment_description: str,
) -> Path:
    """Persist the inputs Step 8 and Step 9 read from disk."""
    d = workspace_dir(run_id)
    (d / "scoring.json").write_text(
        json.dumps(scoring, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (d / "composed_prompt.md").write_text(composed_prompt, encoding="utf-8")
    (d / "deployment_description.txt").write_text(
        deployment_description, encoding="utf-8"
    )
    return d


def build_report(run_id: str, scoring: dict) -> str:
    """Step 8: render scoring.json as a markdown report.

    Returns the report text and writes it to `<workspace>/report.md` so
    Step 9 can parse limitations and citation registries from it.
    """
    from scripts.format_results import format_report

    d = workspace_dir(run_id)
    report = format_report(scoring, assessment_dir=d)
    (d / "report.md").write_text(report, encoding="utf-8")
    return report


def build_review_pdf(run_id: str) -> Path:
    """Step 9: assemble the seven dimension PDFs and merge into review.pdf.

    Caller must have already written scoring.json, composed_prompt.md,
    report.md, and deployment_description.txt via the helpers above.
    """
    from scripts.stage3.generate_expert_pdfs import (
        _register_fonts,
        _build_styles,
        process_tuple,
    )
    from pypdf import PdfReader, PdfWriter

    tuple_dir = workspace_dir(run_id)
    review_path = tuple_dir / "pdfs" / "review.pdf"
    if review_path.exists():
        return review_path

    _register_fonts()
    styles = _build_styles()
    process_tuple(tuple_dir, styles)

    writer = PdfWriter()
    pdf_dir = tuple_dir / "pdfs"
    for name in REVIEW_DIMENSION_ORDER:
        pdf_file = pdf_dir / f"{name}.pdf"
        if pdf_file.exists():
            for page in PdfReader(pdf_file).pages:
                writer.add_page(page)

    pdf_dir.mkdir(parents=True, exist_ok=True)
    with open(review_path, "wb") as f:
        writer.write(f)

    # Match the CLI pipeline's behaviour: drop intermediate section PDFs
    # after the merged review.pdf is written.
    for name in REVIEW_DIMENSION_ORDER:
        section_pdf = pdf_dir / f"{name}.pdf"
        if section_pdf.exists():
            section_pdf.unlink()
    return review_path


def report_path(run_id: str) -> Path:
    return workspace_dir(run_id) / "report.md"


def review_pdf_path(run_id: str) -> Path:
    return workspace_dir(run_id) / "pdfs" / "review.pdf"


def reset(run_id: str, *, scoring_only: bool) -> None:
    """Wipe workspace artifacts to support `--rerun-*` semantics.

    scoring_only=True  → matches `--rerun-scoring`: drops scoring.json,
                         report.md, and pdfs/, keeps composed_prompt.md
                         and deployment_description.txt.
    scoring_only=False → matches `--rerun-all`: removes the workspace dir
                         entirely.
    """
    d = _WORKSPACE_ROOT / run_id
    if not d.exists():
        return
    if not scoring_only:
        shutil.rmtree(d, ignore_errors=True)
        return
    for name in ("scoring.json", "report.md"):
        f = d / name
        if f.exists():
            f.unlink()
    pdfs = d / "pdfs"
    if pdfs.exists():
        shutil.rmtree(pdfs, ignore_errors=True)
