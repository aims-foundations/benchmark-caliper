"""CLI for the post-stage-7 item classification experiment."""

import argparse
from functools import partial
import json
import os
from pathlib import Path
import sys

from .classify import run
from .generate import generate_spec
from .prepare import prepare
from .report import compare_review, generate_report
from .storage import check_prepared, read_json, run_lock


def _api(directory: Path):
    # Loading the shared client also loads a local .env when python-dotenv is
    # installed. Read-only commands and dry runs do not import the API SDK.
    from .. import client

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("Set ANTHROPIC_API_KEY for live calls; --dry-run previews inputs without calls")
    client.set_trace_dir(directory / "traces")
    client.set_stream_default(False)
    client.load_ledger(directory / "usage_ledger.json")
    return client


def _call_and_save(client, directory: Path, **request):
    # Invoked only while the generation/classification command holds its lock.
    # Persist after every call so interruption and continuation retain usage.
    try:
        return client.call(**request)
    finally:
        client.save_ledger(directory / "usage_ledger.json")
        client.dump_cost_ledger(directory / "usage.json")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Quantify Caliper validity findings over benchmark items.")
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare", help="Snapshot one dataset and its existing stage-7 assessment")
    prep.add_argument("--assessment-dir", type=Path, required=True)
    prep.add_argument("--items", type=Path, required=True, help="Local measurement-db items.parquet")
    prep.add_argument("--output-dir", type=Path, required=True)
    prep.add_argument("--benchmark", help="Optional check against scoring.json's benchmark")
    prep.add_argument("--seed", type=int, default=42)
    prep.add_argument("--source-repo", default="aims-foundations/measurement-db")
    prep.add_argument("--source-revision", help="Pinned source revision; inferred from an HF cache path when available")
    prep.add_argument("--source-table", help="Source table path in the dataset repository")
    generate = commands.add_parser("generate-spec", help="Generate with Sonnet, or import a supplied classifier JSON")
    generate.add_argument("--run-dir", type=Path, required=True)
    generate_mode = generate.add_mutually_exclusive_group()
    generate_mode.add_argument("--spec", type=Path, help="Use an existing specification instead of calling Sonnet")
    generate_mode.add_argument("--dry-run", action="store_true", help="Save the exact Sonnet request only")
    generate.add_argument("--max-output-tokens", type=int, default=12000)
    classify = commands.add_parser("classify", help="Classify the first 100 random items, or continue to all items")
    classify.add_argument("--run-dir", type=Path, required=True)
    scope = classify.add_mutually_exclusive_group()
    scope.add_argument("--limit", type=int, default=100, help="Prefix size of the saved random order; default: 100")
    scope.add_argument("--all", action="store_true", help="Traverse every prepared item")
    classify.add_argument("--resume", action="store_true", help="Reuse completed results; retry errors and continue")
    classify.add_argument("--dry-run", action="store_true", help="Save requests without making calls or assigning labels")
    classify.add_argument("--max-output-tokens", type=int, default=4096)
    report = commands.add_parser("report", help="Build HTML, item CSV, and a blind review worksheet")
    report.add_argument("--run-dir", type=Path, required=True)
    review = commands.add_parser("validate", help="Compare independently entered review labels with model labels")
    review.add_argument("--run-dir", type=Path, required=True)
    review.add_argument("--review", type=Path, required=True)
    args = parser.parse_args(argv)
    client = None
    try:
        if args.command == "prepare":
            result = prepare(args.assessment_dir, args.items, args.output_dir, benchmark=args.benchmark,
                             seed=args.seed, source_repo=args.source_repo, source_revision=args.source_revision,
                             source_table=args.source_table)
        elif args.command == "generate-spec":
            if not args.spec and not args.dry_run:
                client = _api(args.run_dir)
            spec = generate_spec(args.run_dir, supplied=args.spec, dry_run=args.dry_run,
                                 max_tokens=args.max_output_tokens,
                                 call=partial(_call_and_save, client, args.run_dir) if client else None,
                                 model_id=client.MODELS["sonnet"] if client else "sonnet")
            result = spec if args.dry_run else {
                "benchmark": spec["benchmark"],
                "applicable_classifiers": sum(c["applicable"] for c in spec["classifiers"]),
                "specification": str(args.run_dir / "classifier_spec.json"),
                "review_note": read_json(args.run_dir / "specification.json")["note"],
            }
        elif args.command == "classify":
            if not args.dry_run:
                client = _api(args.run_dir)
            result = run(args.run_dir, limit=None if args.all else args.limit, resume=args.resume,
                         dry_run=args.dry_run, max_tokens=args.max_output_tokens,
                         call=partial(_call_and_save, client, args.run_dir) if client else None,
                         model_id=client.MODELS["haiku"] if client else "haiku")
            if not args.dry_run:
                with run_lock(args.run_dir):
                    generate_report(args.run_dir)
        else:
            with run_lock(args.run_dir):
                check_prepared(args.run_dir)
                result = (generate_report(args.run_dir) if args.command == "report"
                          else compare_review(args.run_dir, args.review))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if result.get("fatal_error") or result.get("errors", 0) else 0
    except KeyboardInterrupt:
        print("Interrupted. Continue classification with --resume and unchanged settings.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
