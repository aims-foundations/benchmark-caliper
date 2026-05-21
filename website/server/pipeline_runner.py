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
import os
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


def _load_release_module(qualname: str, rel_path: str):
    """Load a module from the release package by exact file path.

    The repo root has a legacy `scripts/` directory that shadows the release
    package's `scripts/` because both are namespace packages (no `__init__.py`).
    `from scripts.X import Y` is therefore ambiguous: whichever ends up in
    `sys.modules` first wins, and in pytest the wrong (legacy) version usually
    wins because pytest's rootdir is on sys.path earlier. The legacy
    `format_results.py` lacks the `assessment_dir` arg, so `build_report`
    crashes with TypeError when the wrong one loads.

    importlib.util.spec_from_file_location bypasses the namespace lookup
    entirely and loads the module from an exact filesystem path, then caches
    it in `sys.modules` under the canonical name so subsequent ordinary
    imports (e.g. inside `verify_evidence.py`, which does
    `from compose_prompt import ...`) resolve to release-package siblings.
    """
    import importlib.util

    if qualname in sys.modules and getattr(sys.modules[qualname], "__file__", "") \
            and str(_PACKAGE_ROOT) in sys.modules[qualname].__file__:
        return sys.modules[qualname]
    sys.modules.pop(qualname, None)

    full = _PACKAGE_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(qualname, full)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load {qualname} from {full}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[qualname] = mod
    spec.loader.exec_module(mod)
    return mod


_DEFAULT_DATA_DIR = Path(__file__).resolve().parent / "data"
_DATA_DIR = Path(os.environ.get("WEBSITE_DATA_DIR", str(_DEFAULT_DATA_DIR)))
_WORKSPACE_ROOT = _DATA_DIR / "tuples"

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
    benchmark_yaml: str | None = None,
    region_yaml: str | None = None,
    dataset_analysis_text: str | None = None,
    pdf_bytes: bytes | None = None,
) -> Path:
    """Persist the inputs Step 8, Step 9, and the verify endpoint read from disk.

    The optional YAML/text artifacts are the same strings the user already
    submitted in the Step 7 request body — they are not new data, just split
    out of the composed prompt so post-hoc verifiers can read them directly.

    `pdf_bytes`, if supplied, is written as `paper.pdf` so the verifier can run
    the PDF-dependent quote checks (L2: YAML vs PDF, and scoring vs PDF). The
    PDF lives only inside this run's workspace and is removed by `reset()` /
    `delete_run` exactly like every other artifact here — "session-scoped",
    in the same sense as scoring.json itself.
    """
    d = workspace_dir(run_id)
    (d / "scoring.json").write_text(
        json.dumps(scoring, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (d / "composed_prompt.md").write_text(composed_prompt, encoding="utf-8")
    (d / "deployment_description.txt").write_text(
        deployment_description, encoding="utf-8"
    )
    if benchmark_yaml:
        (d / "benchmark.yaml").write_text(benchmark_yaml, encoding="utf-8")
    if region_yaml:
        (d / "region.yaml").write_text(region_yaml, encoding="utf-8")
    if dataset_analysis_text:
        (d / "dataset_analysis_report.md").write_text(
            dataset_analysis_text, encoding="utf-8"
        )
    if pdf_bytes:
        (d / "paper.pdf").write_bytes(pdf_bytes)
    return d


def build_report(run_id: str, scoring: dict) -> str:
    """Step 8: render scoring.json as a markdown report.

    Returns the report text and writes it to `<workspace>/report.md` so
    Step 9 can parse limitations and citation registries from it.
    """
    fmt = _load_release_module(
        "scripts.format_results", "scripts/format_results.py"
    )

    d = workspace_dir(run_id)
    report = fmt.format_report(scoring, assessment_dir=d)
    (d / "report.md").write_text(report, encoding="utf-8")
    return report


def build_review_pdf(run_id: str) -> Path:
    """Step 9: assemble the seven dimension PDFs and merge into review.pdf.

    Caller must have already written scoring.json, composed_prompt.md,
    report.md, and deployment_description.txt via the helpers above.
    """
    pdfgen = _load_release_module(
        "scripts.stage3.generate_expert_pdfs",
        "scripts/stage3/generate_expert_pdfs.py",
    )
    _register_fonts = pdfgen._register_fonts
    _build_styles = pdfgen._build_styles
    process_tuple = pdfgen.process_tuple
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


def verify_evidence(
    run_id: str,
    *,
    skip_web: bool = False,
    skip_hf: bool = False,
) -> dict:
    """Run the release package's evidence verifier against this run's workspace.

    The upstream `verify_assessment` resolves benchmark YAML and PDF paths via
    the CLI's `assessments/<expert>/<slug>/` layout, which doesn't apply to the
    website (per-run UUID dirs, no PDF retained). This wrapper calls the
    underlying per-check verifiers directly using whatever artifacts the
    workspace actually has.

    Returns the same shape as `verify_assessment` so callers can rely on the
    documented JSON contract (structural / quotes / web_sources / dataset /
    summary). PDF-dependent checks (quote L2 / scoring-vs-PDF) are always
    skipped because the website does not store the source PDF after extraction.
    """
    import yaml
    ve = _load_release_module(
        "scripts.verify_evidence", "scripts/verify_evidence.py"
    )
    check_structural = ve.check_structural
    compute_summary = ve.compute_summary
    verify_dataset_l1 = ve.verify_dataset_l1
    verify_dataset_l2 = ve.verify_dataset_l2
    verify_quotes_l1 = ve.verify_quotes_l1
    verify_quotes_l2 = ve.verify_quotes_l2
    verify_quotes_scoring_vs_pdf = ve.verify_quotes_scoring_vs_pdf
    verify_web_l1 = ve.verify_web_l1
    verify_web_l2 = ve.verify_web_l2

    d = workspace_dir(run_id)
    scoring_path = d / "scoring.json"
    if not scoring_path.exists():
        raise FileNotFoundError(
            f"scoring.json not found in workspace for run {run_id}"
        )
    scoring = json.loads(scoring_path.read_text())

    bm_yaml_path = d / "benchmark.yaml"
    region_yaml_path = d / "region.yaml"
    report_path = d / "dataset_analysis_report.md"
    pdf_path = d / "paper.pdf"

    bm_yaml: dict = {}
    if bm_yaml_path.exists():
        bm_yaml = yaml.safe_load(bm_yaml_path.read_text()) or {}

    result: dict = {
        "assessment": f"tuples/{run_id}",
        "benchmark": scoring.get("benchmark", "unknown"),
        "structural": [],
        "quotes": {
            "level1_vs_yaml": [],
            "level2_vs_pdf": [],
            "scoring_vs_pdf": [],
        },
        "web_sources": {"level1_vs_registry": [], "level2_liveness": []},
        "dataset": {"level1_vs_report": [], "level2_vs_hf": []},
        "summary": {},
    }

    result["structural"] = check_structural(scoring)

    if bm_yaml:
        result["quotes"]["level1_vs_yaml"] = verify_quotes_l1(scoring, bm_yaml)
        if pdf_path.exists():
            result["quotes"]["level2_vs_pdf"] = verify_quotes_l2(
                bm_yaml, pdf_path
            )

    if pdf_path.exists():
        result["quotes"]["scoring_vs_pdf"] = verify_quotes_scoring_vs_pdf(
            scoring, pdf_path
        )

    if region_yaml_path.exists():
        result["web_sources"]["level1_vs_registry"] = verify_web_l1(
            scoring, region_yaml_path
        )
        if not skip_web and result["web_sources"]["level1_vs_registry"]:
            result["web_sources"]["level2_liveness"] = verify_web_l2(
                result["web_sources"]["level1_vs_registry"]
            )

    result["dataset"]["level1_vs_report"] = verify_dataset_l1(
        scoring, report_path if report_path.exists() else None
    )
    if not skip_hf and result["dataset"]["level1_vs_report"]:
        result["dataset"]["level2_vs_hf"] = verify_dataset_l2(
            scoring,
            report_path if report_path.exists() else None,
            d,
        )

    result["summary"] = compute_summary(result)
    return result


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
