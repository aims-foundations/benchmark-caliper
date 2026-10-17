"""CLI: retrieve a bounded shortlist, then run the six-dimension judge."""

import argparse
import json
import os
from pathlib import Path
import sys

from .data import BRANCHES, discover_inventory, iter_items
from .judge import DEFAULT_MAX_OUTPUT_TOKENS, DEFAULT_MODEL, DEFAULT_REASONING_EFFORT, Judge, PROMPT_PATH
from .runner import run, write_json


def retrieve_candidates(inventory, query, *, retrieve_k, limit_per_table=None, cache_dir=None):
    """Keep question retrieval separate from unchanged validity judging."""
    from .retrieval import ItemIndex, RETRIEVAL_POLICY

    index = ItemIndex(iter_items(inventory, limit_per_table), cache_dir=cache_dir)
    selected = index.search(query, top_k=retrieve_k)
    # The resumable judge consumes one row per source, while retrieval deduplicates
    # evidence. Re-expand provenance so the existing duplicate log remains intact.
    candidates = [
        {"evidence_hash": item["evidence_hash"], "evidence": item["evidence"], "source": source,
         "retrieval_rank": item["retrieval_rank"], "retrieval_score": item["retrieval_score"],
         "exact_match": item["exact_match"]}
        for item in selected for source in item["sources"]
    ]
    metadata = {
        "policy": RETRIEVAL_POLICY, "query": query, "requested_k": retrieve_k,
        "corpus_items": index.total, "indexed_items": index.indexed_items,
        "indexed_source_rows": index.source_rows_seen,
        "contentless_items": index.contentless_items,
        "full_inventory_indexed": limit_per_table is None and not inventory["missing_item_tables"],
    }
    return candidates, metadata


def main() -> int:
    parser = argparse.ArgumentParser(description="Retrieve questions locally, then assess a shortlist for deployment compatibility.")
    commands = parser.add_subparsers(dest="command", required=True)
    inventory = commands.add_parser("inventory", help="Discover item tables from pinned Hugging Face branches")
    inventory.add_argument("--branches", nargs="+", default=list(BRANCHES))
    inventory.add_argument("--benchmarks", nargs="+", help="Optional benchmark directory filter")
    inventory.add_argument("--output", type=Path, required=True)
    scoring = commands.add_parser("run", help="Retrieve a shortlist and score it on six validity dimensions")
    scoring.add_argument("--inventory", type=Path, required=True)
    scoring.add_argument("--deployment", type=Path, required=True)
    scoring.add_argument("--output-dir", type=Path, required=True)
    scoring.add_argument("--model", default=DEFAULT_MODEL)
    scoring.add_argument("--reasoning-effort", choices=["none", "low", "medium", "high"],
                         default=DEFAULT_REASONING_EFFORT, help="Default: high")
    scoring.add_argument("--max-output-tokens", type=int, default=DEFAULT_MAX_OUTPUT_TOKENS,
                         help="Includes reasoning tokens; default: 25000")
    scoring.add_argument("--top-k", type=int, default=10)
    scoring.add_argument("--retrieve-k", type=int, default=20,
                         help="Maximum distinct items to judge after local retrieval; default: 20")
    scoring.add_argument("--retrieval-query", type=Path,
                         help="Optional reference-question text file; otherwise retrieve using the deployment description")
    scoring.add_argument("--embedding-cache-dir", type=Path,
                         help="Private cache for local question embeddings; queries are not cached")
    scoring.add_argument("--limit-per-table", type=int, help="Development limit on source rows from each table")
    scoring.add_argument("--dry-run", action="store_true", help="Retrieve locally and preview the shortlist without calling OpenAI")
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
        query = args.retrieval_query.read_text(encoding="utf-8") if args.retrieval_query else deployment
        if not deployment or not query.strip():
            raise ValueError("Deployment description and retrieval query must not be empty")
        if args.retrieve_k <= 0 or args.top_k <= 0 or args.max_output_tokens <= 0 or (
                args.limit_per_table is not None and args.limit_per_table <= 0):
            raise ValueError("retrieve_k, top_k, max_output_tokens, and limit_per_table must be positive")
        if not args.dry_run and not os.getenv("OPENAI_API_KEY"):
            raise ValueError("Set OPENAI_API_KEY for scoring, or use --dry-run to inspect inputs")
        inventory_data = json.loads(args.inventory.read_text(encoding="utf-8"))
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
        if args.resume:
            from .retrieval import RETRIEVAL_POLICY

            config_path = args.output_dir / "run.json"
            if not config_path.exists():
                raise ValueError("Cannot resume: run.json does not exist")
            saved = json.loads(config_path.read_text(encoding="utf-8"))
            retrieval = saved.get("retrieval")
            if not retrieval or retrieval.get("policy") != RETRIEVAL_POLICY or (
                    retrieval.get("query") != query or retrieval.get("requested_k") != args.retrieve_k):
                raise ValueError("Retrieval settings changed; use a new output directory")
            candidates = saved.get("retrieved_candidates")
            if not isinstance(candidates, list):
                raise ValueError("Saved retrieval candidates are missing; use a new output directory")
            # Reuse the frozen shortlist, avoiding both re-embedding and ranking
            # drift across hardware. run() validates all remaining run settings.
        else:
            candidates, retrieval = retrieve_candidates(
                inventory_data, query, retrieve_k=args.retrieve_k,
                limit_per_table=args.limit_per_table, cache_dir=args.embedding_cache_dir,
            )
        options = dict(
            model=args.model, reasoning_effort=args.reasoning_effort,
            max_output_tokens=args.max_output_tokens, top_k=args.top_k,
            limit_per_table=args.limit_per_table, dry_run=args.dry_run, resume=args.resume,
            candidate_items=candidates, retrieval=retrieval,
        )
        if args.dry_run:
            summary = run(inventory_data, deployment, prompt, args.output_dir, **options)
        else:
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
