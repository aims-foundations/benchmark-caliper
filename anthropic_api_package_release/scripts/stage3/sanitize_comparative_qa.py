#!/usr/bin/env python3
"""sanitize_comparative_qa.py -- Clean elicitation Q&A for comparative assessment.

Abstracts regional-benchmark-specific properties from elicitation questions so
that step 2-summary can regenerate an uncontaminated elicitation summary when
run against a comparator benchmark. Uses a single Opus API call per tuple.

The system prompt (prompts/sanitize_comparative_qa.md) contains fixed
instructions parameterized only by benchmark names. The user message contains
the comparator's step-1 metadata (for grounding) followed by the Q&A block.
This two-part structure makes the procedure fully reproducible and reportable
as a single LLM call with a known prompt.

Usage:
    python3 scripts/stage3/sanitize_comparative_qa.py \
        --source assessments/expert_xxx__milu/slug \
        --pdf papers/mmlu.pdf \
        --comparator-name mmlu \
        --comparator-full-name "Measuring Massive Multitask Language Understanding"

    python3 scripts/stage3/sanitize_comparative_qa.py \
        --source assessments/expert_xxx__drbenchmark/slug \
        --pdf papers/blurb.pdf \
        --comparator-name blurb \
        --dry-run
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PACKAGE_ROOT))

import client

# === Path Constants ===
ASSESSMENTS_DIR = PACKAGE_ROOT / "assessments"
PAPERS_DIR = PACKAGE_ROOT / "papers"
RUN_PIPELINE = PACKAGE_ROOT / "run_pipeline.py"
PROMPT_PATH = PACKAGE_ROOT / "prompts" / "sanitize_comparative_qa.md"


# === Q&A Assembly ===

def assemble_qa_block(questions: list[dict], answers: dict) -> str:
    """Format Q&A pairs into the text block consumed by the prompt."""
    blocks = []
    for q in questions:
        qid = q["id"]
        n = qid.lstrip("Q")
        blocks.append(f"{qid} [{q['dimension']}]: {q['question']}\nA{n}: {answers[qid]}")
    return "\n\n".join(blocks)


def parse_cleaned_qa(text: str, original_questions: list[dict],
                     original_answers: dict) -> tuple[list[dict], dict]:
    """Parse Opus output back into questions and answers structures.

    Falls back to originals if a Q/A-line can't be parsed, so that
    a partial model response never silently drops a pair.
    """
    cleaned_q = []
    cleaned_a = {}
    for orig in original_questions:
        qid = orig["id"]
        n = qid.lstrip("Q")
        q_pattern = rf'{qid}\s*\[(\w+)\]:\s*(.+?)(?=\nA{n}:)'
        q_match = re.search(q_pattern, text, re.DOTALL)
        if q_match:
            cleaned_q.append({
                "id": qid,
                "dimension": q_match.group(1),
                "question": q_match.group(2).strip(),
            })
        else:
            print(f"  WARN: could not parse cleaned {qid}, keeping original",
                  file=sys.stderr)
            cleaned_q.append(orig)

        a_pattern = rf'A{n}:\s*(.+?)(?=\n\nQ\d|\Z)'
        a_match = re.search(a_pattern, text, re.DOTALL)
        if a_match:
            cleaned_a[qid] = a_match.group(1).strip()
        else:
            print(f"  WARN: could not parse cleaned A{n}, keeping original",
                  file=sys.stderr)
            cleaned_a[qid] = original_answers.get(qid, "")

    return cleaned_q, cleaned_a


def _scrub_regional_names(text: str, regional_name: str,
                          regional_full_name: str) -> tuple[str, int]:
    """Last-resort regex pass: replace any remaining regional benchmark name references."""
    replacement = "the benchmark under assessment"
    variants = {regional_name, regional_full_name}
    if ":" in regional_full_name:
        variants.add(regional_full_name.split(":")[0].strip())
    variants.add(regional_name.replace("_", " "))
    variants.discard("")
    total_subs = 0
    for v in sorted(variants, key=len, reverse=True):
        pattern = re.compile(r'\b' + re.escape(v) + r'\b', re.IGNORECASE)
        text, n = pattern.subn(replacement, text)
        total_subs += n
    return text, total_subs


# === Benchmark Identity ===

def read_regional_benchmark(source_dir: Path) -> tuple[str, str]:
    """Read regional benchmark name and full_name from benchmark.yaml."""
    yaml_path = source_dir / "benchmark.yaml"
    if not yaml_path.exists():
        print(f"ERROR: {yaml_path} not found", file=sys.stderr)
        sys.exit(1)
    name = full_name = ""
    for line in yaml_path.read_text().splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip("'\"")
        elif line.startswith("full_name:"):
            full_name = line.split(":", 1)[1].strip().strip("'\"")
    if not name:
        print(f"ERROR: no 'name' field in {yaml_path}", file=sys.stderr)
        sys.exit(1)
    return name, full_name or name


def expert_id_from_stem(paper_stem: str) -> str:
    """Extract expert_id from a paper stem like 'expert_xxx__benchmark'."""
    if "__" not in paper_stem:
        print(f"ERROR: paper stem {paper_stem!r} not in "
              f"'<expert_id>__<benchmark>' form", file=sys.stderr)
        sys.exit(1)
    return paper_stem.split("__", 1)[0]


# === Comparator Metadata ===

def ensure_comparator_metadata(paper_stem: str, pdf_path: Path) -> str:
    """Run step 1 (metadata extraction) if needed, return metadata text.

    Step 1 is a single Haiku call on pages 1-2 of the comparator PDF.
    It caches to papers/<paper_stem>/metadata.md, so repeated calls are free.
    """
    metadata_path = PAPERS_DIR / paper_stem / "metadata.md"
    if metadata_path.exists():
        print(f"[metadata] using cached: {metadata_path}")
        return metadata_path.read_text()

    print("[metadata] running step 1 (Haiku metadata extraction)...")
    dst_pdf = PAPERS_DIR / f"{paper_stem}.pdf"
    r = subprocess.run(
        [sys.executable, str(RUN_PIPELINE), str(dst_pdf), "--step", "1"],
        cwd=PACKAGE_ROOT,
    )
    if r.returncode != 0:
        print("ERROR: step 1 metadata extraction failed", file=sys.stderr)
        sys.exit(1)

    if not metadata_path.exists():
        print(f"ERROR: step 1 did not produce {metadata_path}", file=sys.stderr)
        sys.exit(1)

    return metadata_path.read_text()


# === Target Directory Setup ===

def setup_target_dir(source_dir: Path, paper_stem: str, slug: str,
                     pdf_path: Path) -> Path:
    """Create the comparative assessment dir and copy source artifacts."""
    target_dir = ASSESSMENTS_DIR / paper_stem / slug
    target_dir.mkdir(parents=True, exist_ok=True)

    for fname in ("deployment_description.txt",
                  "elicitation_questions.json",
                  "elicitation_answers.json"):
        dst = target_dir / fname
        if dst.exists():
            continue
        src = source_dir / fname
        if not src.exists():
            print(f"ERROR: {src} not found — is stage 2 complete?",
                  file=sys.stderr)
            sys.exit(1)
        dst.write_bytes(src.read_bytes())

    active_slug = ASSESSMENTS_DIR / paper_stem / "active_slug.txt"
    active_slug.write_text(slug + "\n")

    dst_pdf = PAPERS_DIR / f"{paper_stem}.pdf"
    if not dst_pdf.exists() and not dst_pdf.is_symlink():
        dst_pdf.parent.mkdir(parents=True, exist_ok=True)
        try:
            dst_pdf.symlink_to(pdf_path.resolve())
        except OSError:
            shutil.copy2(pdf_path, dst_pdf)

    return target_dir


# === Main ===

def main() -> None:
    p = argparse.ArgumentParser(
        description="Clean elicitation Q&A for comparative assessment via Opus.",
    )
    p.add_argument("--source", required=True,
                   help="Path to the regional tuple's assessment directory.")
    p.add_argument("--pdf", required=True,
                   help="Path to the comparator benchmark PDF.")
    p.add_argument("--comparator-name", default=None,
                   help="Comparator benchmark slug (default: PDF stem).")
    p.add_argument("--comparator-full-name", default=None,
                   help="Comparator benchmark full name "
                        "(default: same as --comparator-name).")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the prompt without calling the API.")
    p.add_argument("--force", action="store_true",
                   help="Re-clean even if cleaned questions already exist.")
    args = p.parse_args()

    if args.dry_run:
        client.DRY_RUN = True

    # === Resolve source ===
    source_dir = Path(args.source).expanduser().resolve()
    if not source_dir.is_dir():
        print(f"ERROR: source dir {source_dir} not found", file=sys.stderr)
        sys.exit(1)

    slug = source_dir.name
    source_paper_stem = source_dir.parent.name
    expert_id = expert_id_from_stem(source_paper_stem)

    # === Resolve comparator ===
    pdf_path = Path(args.pdf).expanduser().resolve()
    if not pdf_path.exists():
        print(f"ERROR: comparator PDF {pdf_path} not found", file=sys.stderr)
        sys.exit(1)

    comp_name = args.comparator_name or pdf_path.stem
    comp_full_name = args.comparator_full_name or comp_name
    paper_stem = f"{expert_id}__{comp_name}"

    # === Read regional benchmark identity ===
    regional_name, regional_full_name = read_regional_benchmark(source_dir)

    print(f"[setup] regional: {regional_name} ({regional_full_name})")
    print(f"[setup] comparator: {comp_name} ({comp_full_name})")
    print(f"[setup] paper stem: {paper_stem}")
    print(f"[setup] slug: {slug}")

    # === Set up target directory ===
    target_dir = setup_target_dir(source_dir, paper_stem, slug, pdf_path)
    print(f"[setup] target dir: {target_dir}")

    # === Idempotency check ===
    cleaned_marker = target_dir / ".qa_cleaned"
    if cleaned_marker.exists() and not args.force:
        print(f"[skip] Q&A already cleaned (marker: {cleaned_marker})")
        print(f"\nReady to run:")
        print(f"  python3 run_comparative.py --source {args.source} "
              f"--pdf {args.pdf} --name {comp_name}")
        return

    # === Extract comparator metadata (step 1) ===
    metadata_text = ensure_comparator_metadata(paper_stem, pdf_path)

    # === Load deployment description and Q&A from source ===
    deploy_path = source_dir / "deployment_description.txt"
    if not deploy_path.exists():
        print(f"ERROR: {deploy_path} not found", file=sys.stderr)
        sys.exit(1)
    deployment_text = deploy_path.read_text().strip()

    questions = json.loads((source_dir / "elicitation_questions.json").read_text())
    answers = json.loads((source_dir / "elicitation_answers.json").read_text())
    qa_block = assemble_qa_block(questions, answers)

    # === Build prompt ===
    # System prompt: fixed instructions parameterized by benchmark names
    # User message: comparator metadata + deployment description + Q&A block
    system_template = PROMPT_PATH.read_text()
    system_prompt = (system_template
                     .replace("{{REGIONAL_NAME}}", regional_name)
                     .replace("{{REGIONAL_FULL_NAME}}", regional_full_name)
                     .replace("{{COMPARATOR_NAME}}", comp_name)
                     .replace("{{COMPARATOR_FULL_NAME}}", comp_full_name))

    user_message = (
        f"## Comparator Benchmark Metadata\n\n"
        f"{metadata_text}\n\n"
        f"## Deployment Description\n\n"
        f"{deployment_text}\n\n"
        f"## Original Q&A Pairs\n\n"
        f"{qa_block}"
    )

    # === Call Opus ===
    print(f"[clean] calling Opus to sanitize {len(questions)} Q&A pairs...")
    result = client.call(
        model="opus",
        system=system_prompt,
        user=user_message,
        max_tokens=4096,
        step="sanitize_qa",
    )

    if args.dry_run:
        return

    # === Parse and write cleaned Q&A ===
    cleaned_questions, cleaned_answers = parse_cleaned_qa(result, questions, answers)

    if len(cleaned_questions) != len(questions):
        print(f"ERROR: parsed {len(cleaned_questions)} questions, "
              f"expected {len(questions)}", file=sys.stderr)
        sys.exit(1)

    out_q_path = target_dir / "elicitation_questions.json"
    out_q_path.write_text(json.dumps(cleaned_questions, indent=2) + "\n")
    print(f"[clean] wrote cleaned questions to {out_q_path}")

    out_a_path = target_dir / "elicitation_answers.json"
    out_a_path.write_text(json.dumps(cleaned_answers, indent=2) + "\n")
    print(f"[clean] wrote cleaned answers to {out_a_path}")

    # === Final scrub: remove any remaining regional benchmark name references ===
    total_scrubbed = 0
    for path in (out_q_path, out_a_path):
        raw = path.read_text()
        scrubbed, n = _scrub_regional_names(raw, regional_name, regional_full_name)
        if n:
            path.write_text(scrubbed)
            total_scrubbed += n
    deploy_dst = target_dir / "deployment_description.txt"
    deploy_text = deploy_dst.read_text()
    deploy_text, n = _scrub_regional_names(deploy_text, regional_name, regional_full_name)
    deploy_dst.write_text(deploy_text)
    total_scrubbed += n
    if total_scrubbed:
        print(f"[scrub] post-hoc regex removed {total_scrubbed} residual name reference(s)")
    else:
        print(f"[scrub] no residual name references found")

    # === Write trace for reproducibility ===
    trace_path = target_dir / "traces" / "sanitize_qa.jsonl"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    trace = {
        "step": "sanitize_qa",
        "model": client.MODELS["opus"],
        "temperature": "API default",
        "system_prompt_path": str(PROMPT_PATH.relative_to(PACKAGE_ROOT)),
        "regional_benchmark": {"name": regional_name, "full_name": regional_full_name},
        "comparator_benchmark": {"name": comp_name, "full_name": comp_full_name},
        "comparator_metadata": metadata_text,
        "deployment_description": deployment_text,
        "input_qa_block": qa_block,
        "raw_output": result,
        "cleaned_questions": cleaned_questions,
        "cleaned_answers": cleaned_answers,
    }
    trace_path.write_text(json.dumps(trace, indent=2) + "\n")
    print(f"[clean] wrote trace to {trace_path}")

    # === Mark as cleaned ===
    cleaned_marker.write_text(f"cleaned by sanitize_comparative_qa.py\n"
                              f"model: {client.MODELS['opus']}\n"
                              f"regional: {regional_name}\n"
                              f"comparator: {comp_name}\n")

    # === Cost report ===
    print(f"\n{client.format_cost_report()}")
    ledger_path = target_dir / "cost_ledger_sanitize.json"
    client.dump_cost_ledger(ledger_path)
    print(f"[clean] cost ledger written to {ledger_path}")

    # === Report ===
    print(f"\nReady to run:")
    print(f"  python3 run_comparative.py --source {args.source} "
          f"--pdf {args.pdf} --name {comp_name}")


if __name__ == "__main__":
    main()
