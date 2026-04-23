#!/usr/bin/env python3
"""Stage-1 wrapper for expert-validation experiments.

Parses the CSV export from the Google Form of expert benchmark proposals,
writes per-row manifests + per-tuple deployment descriptions under
`expert_responses/`, then drives `run_pipeline.py` through --step 0,
--step 1 (metadata), and --step 2-questions for each of the four tuples
per row. The generated `elicitation_questions.json` for each tuple is
copied back into `expert_responses/<csv>/<expert>/tuples/tuple_N/` for
handoff to the expert via the Stage-2 Google Form. Paper-level steps
(3a/3b/3c) are deferred to stage 2, where they can incorporate the
elicitation summary from expert answers.

Idempotent: rerunning skips any tuple that already has
`elicitation_questions.json`. Use `--force` to re-run anyway,
`--parse-only` to stop at manifests without touching the pipeline, and
`--row` / `--tuple` to restrict the batch for debugging.
"""

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import client

PACKAGE_ROOT = Path(__file__).resolve().parent
EXPERT_RESPONSES = PACKAGE_ROOT / "expert_responses"
FORM_RESPONSES = EXPERT_RESPONSES / "form_responses" / "stage_1"

# Core pipeline directories — the wrapper inspects these to decide what
# paper-level steps to skip, and symlinks curated PDFs into PAPERS_DIR.
PAPERS_DIR = PACKAGE_ROOT / "papers"
PAGE_CACHES_DIR = PACKAGE_ROOT / "page_caches"
BENCHMARKS_DIR = PACKAGE_ROOT / "benchmarks"
ASSESSMENTS_DIR = PACKAGE_ROOT / "assessments"
RUN_PIPELINE = PACKAGE_ROOT / "run_pipeline.py"

# Column layout emitted by the Google Form. Update if the form schema changes.
COL_TIMESTAMP = 0
COL_EMAIL_AUTH = 1        # "Email Address" — auto-collected from Google auth
COL_NAME = 2
COL_EMAIL_QUESTION = 3    # Explicit "Email" free-text question (may duplicate col 1)
COL_REGIONS = 4
COL_REGIONAL_CONTEXT = 5
COL_BENCH_A_NAME = 6
COL_BENCH_A_LINK = 7
COL_BENCH_A_EXTRA = 8
COL_TUPLE_1_USE = 9
COL_TUPLE_1_POP = 10
COL_TUPLE_2_USE = 11
COL_TUPLE_2_POP = 12
COL_BENCH_B_NAME = 13
COL_BENCH_B_LINK = 14
COL_BENCH_B_EXTRA = 15
COL_TUPLE_3_USE = 16
COL_TUPLE_3_POP = 17
COL_TUPLE_4_USE = 18
COL_TUPLE_4_POP = 19
EXPECTED_COLUMNS = 20

# Only the use case + target population are pipeline inputs. Regional context
# stays in the manifest for later analysis, not in this file.
DEPLOYMENT_TEMPLATE = (
    "Use case and domain: {use_case}\n"
    "Target population: {target_population}\n"
)


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "unknown"


def _find_paper_pdf(slug: str) -> Path | None:
    """Find a PDF in papers/ whose slugified stem matches the benchmark slug."""
    for pdf in PAPERS_DIR.glob("*.pdf"):
        if slugify(pdf.stem) == slug:
            return pdf
    return None


def expert_id_from_email(email: str) -> str:
    """Deterministic, non-reversible ID from email.

    Uses a truncated SHA-256 so raw emails never appear in repo-tracked
    paths. A local mapping file (.secrets/expert_map.json, gitignored)
    preserves the email ↔ ID link for de-anonymization."""
    normalized = email.strip().lower()
    expert_id = "expert_" + hashlib.sha256(normalized.encode()).hexdigest()[:12]
    _record_expert_mapping(normalized, expert_id)
    return expert_id


def _record_expert_mapping(email: str, expert_id: str) -> None:
    """Append to the local (gitignored) email ↔ ID mapping."""
    map_path = PACKAGE_ROOT / ".secrets" / "expert_map.json"
    map_path.parent.mkdir(parents=True, exist_ok=True)
    mapping = {}
    if map_path.exists():
        mapping = json.loads(map_path.read_text())
    if mapping.get(expert_id) == email:
        return
    mapping[expert_id] = email
    map_path.write_text(json.dumps(mapping, indent=2) + "\n")


def stage_csv(source: Path) -> Path:
    """Ensure the CSV lives under expert_responses/form_responses/stage_1/.
    Copies it there if it doesn't already. Returns the staged path."""
    FORM_RESPONSES.mkdir(parents=True, exist_ok=True)
    target = FORM_RESPONSES / source.name
    if source.resolve() == target.resolve():
        return target
    if target.exists():
        print(
            f"[stage] CSV already present at {target.relative_to(PACKAGE_ROOT)} "
            f"— using existing copy (not overwriting from {source})",
            file=sys.stderr,
        )
        return target
    shutil.copy2(source, target)
    print(f"[stage] copied {source} -> {target.relative_to(PACKAGE_ROOT)}")
    return target


def _benchmark(raw, i_name, i_link, i_extra, expert_id, csv_stem) -> dict:
    name = raw[i_name].strip()
    slug = slugify(name)
    pdf_rel = f"expert_responses/{csv_stem}/{expert_id}/pdfs/{slug}.pdf"
    return {
        "slug": slug,
        "name": name,
        "paper_link": raw[i_link].strip(),
        "additional_doc_link": raw[i_extra].strip(),
        "pdf_path": pdf_rel,
        "pdf_present": (PACKAGE_ROOT / pdf_rel).exists(),
    }


def _tuple(idx, bench, use_case, target_pop, expert_id, csv_stem) -> dict:
    dep_rel = (
        f"expert_responses/{csv_stem}/{expert_id}/tuples/"
        f"tuple_{idx}/deployment_description.txt"
    )
    return {
        "index": idx,
        "benchmark_slug": bench["slug"],
        "benchmark_name": bench["name"],
        "use_case": use_case.strip(),
        "target_population": target_pop.strip(),
        "deployment_description_path": dep_rel,
    }


def parse_row(raw: list, row_index: int, source_csv: str) -> dict:
    if len(raw) < EXPECTED_COLUMNS:
        raw = list(raw) + [""] * (EXPECTED_COLUMNS - len(raw))

    # Prefer the auth-collected email; fall back to the free-text question.
    email = raw[COL_EMAIL_AUTH].strip() or raw[COL_EMAIL_QUESTION].strip()
    if not email:
        print(
            f"WARN: row {row_index} has no email — expert_id will be 'unknown' "
            f"and collide with other empty-email rows.",
            file=sys.stderr,
        )
    expert_id = expert_id_from_email(email)
    csv_stem = Path(source_csv).stem

    bench_a = _benchmark(
        raw, COL_BENCH_A_NAME, COL_BENCH_A_LINK, COL_BENCH_A_EXTRA,
        expert_id, csv_stem,
    )
    bench_b = _benchmark(
        raw, COL_BENCH_B_NAME, COL_BENCH_B_LINK, COL_BENCH_B_EXTRA,
        expert_id, csv_stem,
    )

    tuples = [
        _tuple(1, bench_a, raw[COL_TUPLE_1_USE], raw[COL_TUPLE_1_POP],
               expert_id, csv_stem),
        _tuple(2, bench_a, raw[COL_TUPLE_2_USE], raw[COL_TUPLE_2_POP],
               expert_id, csv_stem),
        _tuple(3, bench_b, raw[COL_TUPLE_3_USE], raw[COL_TUPLE_3_POP],
               expert_id, csv_stem),
        _tuple(4, bench_b, raw[COL_TUPLE_4_USE], raw[COL_TUPLE_4_POP],
               expert_id, csv_stem),
    ]

    return {
        "source_csv": Path(source_csv).name,
        "source_row": row_index,
        "timestamp": raw[COL_TIMESTAMP].strip(),
        "name": raw[COL_NAME].strip(),
        "email": email,
        "expert_id": expert_id,
        "regions_of_expertise": raw[COL_REGIONS].strip(),
        "regional_context": raw[COL_REGIONAL_CONTEXT].strip(),
        "benchmarks": [bench_a, bench_b],
        "tuples": tuples,
    }


def read_rows(csv_path: Path) -> list:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            raise ValueError(f"CSV {csv_path} is empty.")
        if len(header) < EXPECTED_COLUMNS:
            raise ValueError(
                f"CSV {csv_path} has {len(header)} header cols; expected at "
                f"least {EXPECTED_COLUMNS}. Has the form schema changed?"
            )
        return [
            parse_row(row, i, csv_path.name)
            for i, row in enumerate(reader, start=1)
            if any(c.strip() for c in row)
        ]


def write_manifest(row: dict) -> Path:
    csv_stem = Path(row["source_csv"]).stem
    path = EXPERT_RESPONSES / csv_stem / row["expert_id"] / "row.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(row, indent=2) + "\n")
    return path


def write_deployment_description(t: dict) -> Path:
    path = PACKAGE_ROOT / t["deployment_description_path"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(DEPLOYMENT_TEMPLATE.format(
        use_case=t["use_case"],
        target_population=t["target_population"],
    ))
    return path


def _paper_stem(expert_id: str, bench_slug: str) -> str:
    # Double-underscore keeps the split unambiguous even when expert_id
    # itself contains single underscores (e.g., rcorona_berkeley_edu).
    return f"{expert_id}__{bench_slug}"


def stage_pdf(bench: dict, expert_id: str) -> str:
    """Symlink the expert-curated PDF into papers/<expert_id>__<slug>.pdf.
    Returns the paper stem (filename without .pdf)."""
    source = PACKAGE_ROOT / bench["pdf_path"]
    if not source.exists():
        raise FileNotFoundError(
            f"curated PDF missing: {source.relative_to(PACKAGE_ROOT)}"
        )
    stem = _paper_stem(expert_id, bench["slug"])
    dest = PAPERS_DIR / f"{stem}.pdf"
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink() or dest.exists():
        try:
            if dest.resolve() == source.resolve():
                return stem
        except (FileNotFoundError, OSError):
            pass   # broken symlink — replace below
        dest.unlink()
    dest.symlink_to(source)
    print(f"[stage-pdf] {dest.relative_to(PACKAGE_ROOT)} -> "
          f"{source.relative_to(PACKAGE_ROOT)}")
    return stem


def collect_costs(row: dict) -> dict | None:
    """Read each completed tuple's cost ledger and aggregate into a summary."""
    csv_stem = Path(row["source_csv"]).stem
    expert_id = row["expert_id"]
    expert_dir = EXPERT_RESPONSES / csv_stem / expert_id

    tuples_costs = {}
    grand_total = 0.0

    for t in row["tuples"]:
        tuple_dir = expert_dir / "tuples" / f"tuple_{t['index']}"
        slug_file = tuple_dir / "assessment_slug.txt"
        if not slug_file.exists():
            continue

        slug = slug_file.read_text().strip()
        paper_stem = _paper_stem(expert_id, t["benchmark_slug"])
        ledger_path = ASSESSMENTS_DIR / paper_stem / slug / "cost_ledger.json"

        if not ledger_path.exists():
            continue

        client.reset_ledger()
        client.load_ledger(ledger_path)
        report = client.cost_report()

        tuples_costs[str(t["index"])] = {
            "benchmark": t["benchmark_name"],
            "slug": slug,
            "steps": report["steps"],
            "total_usd": report["total_usd"],
        }
        grand_total += report["total_usd"]

    if not tuples_costs:
        return None

    return {
        "expert_id": expert_id,
        "expert_name": row["name"],
        "tuples": tuples_costs,
        "total_usd": round(grand_total, 6),
    }


def write_costs(row: dict) -> Path | None:
    """Collect per-tuple costs and write summary to the expert directory."""
    costs = collect_costs(row)
    if costs is None:
        return None
    csv_stem = Path(row["source_csv"]).stem
    expert_dir = EXPERT_RESPONSES / csv_stem / row["expert_id"]
    path = expert_dir / "costs.json"
    path.write_text(json.dumps(costs, indent=2) + "\n")
    return path


def run_pipeline_step(paper_stem: str, step: str, *,
                      use_case: Path = None) -> None:
    """Invoke run_pipeline.py with a single --step. Raises RuntimeError
    on non-zero exit so the caller can mark the tuple as failed."""
    pdf = PAPERS_DIR / f"{paper_stem}.pdf"
    cmd = [sys.executable, str(RUN_PIPELINE), str(pdf), "--step", step]
    if use_case is not None:
        cmd += ["--use-case", str(use_case)]
    print(f"[run] --step {step} ({paper_stem})")
    r = subprocess.run(cmd, cwd=PACKAGE_ROOT)
    if r.returncode != 0:
        raise RuntimeError(
            f"run_pipeline.py --step {step} failed "
            f"(exit {r.returncode}) for {paper_stem}"
        )


def prepare_paper(paper_stem: str) -> None:
    """Run paper-level steps (3a/3b/3c), skipping any whose output is
    already on disk. 3c-verify is mechanical (no API cost) so it always
    runs — catches any benchmark-YAML formatting issue before elicitation."""
    page_cache = PAGE_CACHES_DIR / paper_stem
    summary = PAPERS_DIR / paper_stem / "paper_summary.md"
    bench_refs = PAPERS_DIR / paper_stem / "benchmark_refs.json"
    bench_yaml = BENCHMARKS_DIR / f"{paper_stem}.yaml"

    if page_cache.exists() and any(page_cache.glob("page_*.txt")):
        print(f"[skip] 3a-extract ({paper_stem}: page cache populated)")
    else:
        run_pipeline_step(paper_stem, "3a-extract")

    if summary.exists():
        print(f"[skip] 3a-consolidate ({paper_stem}: summary exists)")
    else:
        run_pipeline_step(paper_stem, "3a-consolidate")

    if bench_refs.exists():
        print(f"[skip] 3b-select ({paper_stem}: refs exist)")
    else:
        run_pipeline_step(paper_stem, "3b-select")

    if bench_yaml.exists():
        print(f"[skip] 3b-synthesize ({paper_stem}: YAML exists)")
    else:
        run_pipeline_step(paper_stem, "3b-synthesize")

    run_pipeline_step(paper_stem, "3c-verify")


def process_tuple(row: dict, t: dict, *, force: bool = False) -> str:
    """Run one (row, tuple) through the pipeline up to 2-questions.
    Returns 'done' | 'skipped' | 'failed: <reason>'."""
    csv_stem = Path(row["source_csv"]).stem
    expert_id = row["expert_id"]
    tuple_dir = (EXPERT_RESPONSES / csv_stem / expert_id
                 / "tuples" / f"tuple_{t['index']}")
    questions_out = tuple_dir / "elicitation_questions.json"

    if questions_out.exists() and not force:
        print(f"[skip tuple {t['index']}] already done "
              f"({questions_out.relative_to(PACKAGE_ROOT)})")
        return "skipped"

    bench = next((b for b in row["benchmarks"]
                  if b["slug"] == t["benchmark_slug"]), None)
    if bench is None:
        return f"failed: benchmark {t['benchmark_slug']} not in row manifest"

    dep_path = PACKAGE_ROOT / t["deployment_description_path"]
    if not dep_path.exists():
        return f"failed: deployment description missing ({dep_path})"

    try:
        paper_stem = stage_pdf(bench, expert_id)
    except FileNotFoundError as e:
        return f"failed: {e}"

    # --step 0 short-circuits if active_slug.txt already exists (it's
    # meant to be derived once per assessment). For our per-tuple loop
    # we delete it so --step 0 re-derives a slug from *this* tuple's
    # deployment description.
    active = ASSESSMENTS_DIR / paper_stem / "active_slug.txt"
    if active.exists():
        active.unlink()

    try:
        run_pipeline_step(paper_stem, "0", use_case=dep_path)
        run_pipeline_step(paper_stem, "1")
        run_pipeline_step(paper_stem, "2-questions", use_case=dep_path)
    except RuntimeError as e:
        return f"failed: {e}"

    slug = active.read_text().strip()
    q_src = ASSESSMENTS_DIR / paper_stem / slug / "elicitation_questions.json"
    if not q_src.exists():
        return (f"failed: expected {q_src.relative_to(PACKAGE_ROOT)} "
                f"but it was not written")
    tuple_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(q_src, questions_out)
    (tuple_dir / "assessment_slug.txt").write_text(slug + "\n")
    print(f"[done tuple {t['index']}] -> "
          f"{questions_out.relative_to(PACKAGE_ROOT)} (slug: {slug})")
    return "done"


def main() -> None:
    p = argparse.ArgumentParser(
        description=(
            "Stage-1 wrapper: parse the expert-proposal CSV, stage PDFs, "
            "and run the validity pipeline up through --step 2-questions "
            "for each (row, tuple). Writes elicitation_questions.json "
            "under expert_responses/<csv>/<expert>/tuples/tuple_N/ for "
            "handoff to the expert via the Stage-2 Google Form."
        ),
    )
    p.add_argument("csv_path", help="Path to the CSV export from the Google Form.")
    p.add_argument("--row", type=int,
                   help="Only process the given 1-indexed data row.")
    p.add_argument("--tuple", type=int, dest="tuple_idx",
                   choices=[1, 2, 3, 4],
                   help="Only process the given tuple index (1-4) within each row.")
    p.add_argument("--force", action="store_true",
                   help="Re-run tuples whose elicitation_questions.json already exists.")
    p.add_argument("--parse-only", action="store_true",
                   help="Only parse the CSV and write manifests + deployment "
                        "descriptions; skip PDF staging and pipeline invocation.")
    args = p.parse_args()

    src = Path(args.csv_path).expanduser().resolve()
    if not src.exists():
        print(f"ERROR: CSV not found: {src}", file=sys.stderr)
        sys.exit(1)

    staged = stage_csv(src)
    rows = read_rows(staged)

    if args.row is not None:
        rows = [r for r in rows if r["source_row"] == args.row]
        if not rows:
            print(f"ERROR: row {args.row} not found in CSV", file=sys.stderr)
            sys.exit(1)

    # Always-on: dirs, deployment descriptions, PDF linking, manifest
    # (cheap, idempotent). Manifest is written last so pdf_present reflects
    # any auto-linked PDFs.
    for row in rows:
        print(f"[row {row['source_row']}] {row['email']}")
        for t in row["tuples"]:
            d = write_deployment_description(t)
            print(f"  tuple {t['index']} ({t['benchmark_slug']}): "
                  f"{d.relative_to(PACKAGE_ROOT)}")
        for b in row["benchmarks"]:
            pdf_target = PACKAGE_ROOT / b["pdf_path"]
            pdf_target.parent.mkdir(parents=True, exist_ok=True)
            if not pdf_target.exists():
                source = _find_paper_pdf(b["slug"])
                if source:
                    pdf_target.symlink_to(source.resolve())
                    b["pdf_present"] = True
                    print(f"  pdf [link] {b['slug']}: "
                          f"{source.name} -> {b['pdf_path']}")
                else:
                    print(f"  pdf [MISS] {b['slug']}: {b['pdf_path']}\n"
                          f"           Place the PDF in papers/ with a name "
                          f"that matches the benchmark slug \"{b['slug']}\".\n"
                          f"           Any of these would work: "
                          f"{b['slug']}.pdf, "
                          f"{b['slug'].replace('_', '-')}.pdf, "
                          f"{b['name']}.pdf")
            else:
                print(f"  pdf [ok  ] {b['slug']}: {b['pdf_path']}")
        # Create papers/<expert_id>__<slug>.pdf symlinks so manual
        # --step invocations use the namespaced paper stem.
        for b in row["benchmarks"]:
            if b["pdf_present"]:
                try:
                    stem = stage_pdf(b, row["expert_id"])
                    print(f"  papers [link] {stem}.pdf")
                except FileNotFoundError:
                    pass  # already warned above
        m = write_manifest(row)
        print(f"  manifest: {m.relative_to(PACKAGE_ROOT)}")

    if args.parse_only:
        print(f"\nDone (parse-only): wrote {len(rows)} manifest(s).")
        return

    # Pipeline orchestration — one tuple at a time, continue-on-failure.
    totals = {"done": 0, "skipped": 0, "failed": 0}
    failures = []
    for row in rows:
        tuples = row["tuples"]
        if args.tuple_idx is not None:
            tuples = [t for t in tuples if t["index"] == args.tuple_idx]
        for t in tuples:
            print(f"\n=== row {row['source_row']} / tuple {t['index']} "
                  f"({row['expert_id']} / {t['benchmark_slug']}) ===")
            status = process_tuple(row, t, force=args.force)
            if status == "done":
                totals["done"] += 1
            elif status == "skipped":
                totals["skipped"] += 1
            else:
                totals["failed"] += 1
                failures.append((row["source_row"], t["index"],
                                 row["expert_id"], t["benchmark_slug"],
                                 status))

    print("\n=== Summary ===")
    print(f"  done:    {totals['done']}")
    print(f"  skipped: {totals['skipped']}")
    print(f"  failed:  {totals['failed']}")

    # Cost aggregation — reads each tuple's cost ledger (including
    # previously completed tuples) and writes per-expert costs.json.
    print("\n=== Costs ===")
    for row in rows:
        path = write_costs(row)
        if path:
            costs = json.loads(path.read_text())
            print(f"\n  {row['expert_id']}:")
            for tidx, tc in sorted(costs["tuples"].items()):
                print(f"    tuple {tidx} ({tc['benchmark']}): "
                      f"${tc['total_usd']:.4f}")
            print(f"    TOTAL: ${costs['total_usd']:.4f}")
            print(f"    -> {path.relative_to(PACKAGE_ROOT)}")
        else:
            print(f"\n  {row['expert_id']}: no cost data yet")

    if failures:
        print("\nFailures:")
        for row_i, tup_i, eid, bslug, reason in failures:
            print(f"  row {row_i} tuple {tup_i} ({eid}/{bslug}): {reason}")
        sys.exit(1)


if __name__ == "__main__":
    main()
