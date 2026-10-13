"""CLI: inspect the corpus with inventory, then run the six-dimension judge."""

import argparse
import json
import os
from pathlib import Path
import sys

from .data import BRANCHES, discover_inventory
from .judge import DEFAULT_MAX_OUTPUT_TOKENS, DEFAULT_MODEL, DEFAULT_REASONING_EFFORT, Judge, PROMPT_PATH
from .runner import run, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank evaluation items by deployment compatibility.")
    commands = parser.add_subparsers(dest="command", required=True)
    inventory = commands.add_parser("inventory", help="Discover item tables from pinned Hugging Face branches")
    inventory.add_argument("--branches", nargs="+", default=list(BRANCHES))
    inventory.add_argument("--benchmarks", nargs="+", help="Optional benchmark directory filter")
    inventory.add_argument("--output", type=Path, required=True)
    scoring = commands.add_parser("run", help="Score every item in the saved inventory")
    scoring.add_argument("--inventory", type=Path, required=True)
    scoring.add_argument("--deployment", type=Path, required=True)
    scoring.add_argument("--output-dir", type=Path, required=True)
    scoring.add_argument("--model", default=DEFAULT_MODEL)
    scoring.add_argument("--reasoning-effort", choices=["none", "low", "medium", "high"],
                         default=DEFAULT_REASONING_EFFORT, help="Default: high")
    scoring.add_argument("--max-output-tokens", type=int, default=DEFAULT_MAX_OUTPUT_TOKENS,
                         help="Includes reasoning tokens; default: 25000")
    scoring.add_argument("--top-k", type=int, default=10)
    scoring.add_argument("--limit-per-table", type=int, help="Development limit on source rows from each table")
    scoring.add_argument("--dry-run", action="store_true", help="Save actual input previews without calling OpenAI")
    scoring.add_argument("--resume", action="store_true", help="Skip saved assessments and retry errors")
    args = parser.parse_args()
    try:
        if args.command == "inventory":
            output = discover_inventory(args.branches, args.benchmarks)
            write_json(args.output, output)
            print(f"Saved {len(output['tables'])} item tables from {len(output['branches'])} branches to {args.output}")
            if output["missing_item_tables"]:
                print(f"Warning: {len(output['missing_item_tables'])} directories have no item table; see inventory.", file=sys.stderr)
            return 0
        deployment = args.deployment.read_text(encoding="utf-8").strip()
        inventory_data = json.loads(args.inventory.read_text(encoding="utf-8"))
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
        options = dict(
            model=args.model, reasoning_effort=args.reasoning_effort,
            max_output_tokens=args.max_output_tokens, top_k=args.top_k,
            limit_per_table=args.limit_per_table, dry_run=args.dry_run, resume=args.resume,
        )
        if args.dry_run:
            summary = run(inventory_data, deployment, prompt, args.output_dir, **options)
        else:
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("Set OPENAI_API_KEY for scoring, or use --dry-run to inspect inputs")
            from openai import OpenAI

            # Allow longer reasoning requests time to finish before retrying.
            with OpenAI(max_retries=2, timeout=600) as client:
                judge = Judge(client, deployment, prompt, model=args.model,
                              reasoning_effort=args.reasoning_effort, max_output_tokens=args.max_output_tokens)
                summary = run(inventory_data, deployment, prompt, args.output_dir, judge=judge, **options)
        print(json.dumps(summary, indent=2))
        return 1 if summary["errors"] else 0
    except KeyboardInterrupt:
        print("Interrupted; use --resume with the same run settings.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
