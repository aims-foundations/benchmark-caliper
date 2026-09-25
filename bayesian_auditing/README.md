# Goal-conditioned item review

This first demo implements **Find and review relevant tests**: describe an AI
deployment in a text file, assess evaluation items with **GPT-6 Luna**, and return
the highest-scoring items with six validity scores and supporting evidence.

The [website](../website/README.md) also provides a guided demo at
`/benchmark-caliper/items`, using this module's loader and judge with a small
sample from both branches. This CLI supports the full saved inventory and
disk-based resume.

The item-level rubric adapts Benchmark Caliper's
[six-dimensional framework](../anthropic_api_package_release/framework.yaml).
The implementation uses the OpenAI Responses API with `gpt-6-luna`, high reasoning
effort, and one structured assessment per distinct scoring input. It replaces
the earlier embedding-search prototype. Bayesian experimental design, testing
the deployed system, and audit reporting are future steps.

## Quick start

Run these commands from the repository root:

```bash
python -m pip install -r bayesian_auditing/requirements.txt
```

Access to the gated
[measurement-db dataset](https://huggingface.co/datasets/aims-foundations/measurement-db)
requires an authorized Hugging Face account. The loader uses the existing Hub
login or `HF_TOKEN`. Use `hf auth login` if a login is needed. Live judging also
requires `OPENAI_API_KEY` in the environment and access to `gpt-6-luna`.

Start with two benchmark directories to inspect a small example from both
branches:

```bash
python -m bayesian_auditing inventory \
  --benchmarks matharena afrimedqa \
  --output bayesian_auditing/results/demo_inventory.json

python -m bayesian_auditing run \
  --inventory bayesian_auditing/results/demo_inventory.json \
  --deployment bayesian_auditing/examples/deployment.txt \
  --output-dir bayesian_auditing/results/demo_preview \
  --limit-per-table 2 --dry-run
```

The included deployment is an example text mathematics tutor. Replace it with a
description of your intended users, tasks, input format, expected outputs,
success criteria, and constraints. Unspecified requirements remain unspecified;
the judge is instructed to report information gaps.

`--dry-run` downloads data and saves the actual request inputs without making
OpenAI calls or producing scores. The pinned sample inventory currently contains
three tables: matharena in both branches and afrimedqa in the migration branch.
The limit applies to source rows in **each table**, before duplicate detection.

Once the inputs look appropriate, run a small paid assessment in a new folder:

```bash
python -m bayesian_auditing run \
  --inventory bayesian_auditing/results/demo_inventory.json \
  --deployment bayesian_auditing/examples/deployment.txt \
  --output-dir bayesian_auditing/results/demo_scores \
  --limit-per-table 2 --top-k 5
```

The model defaults to `gpt-6-luna` with `--reasoning-effort high`; `--model` and
`--reasoning-effort` are available for later comparisons. The default
`--max-output-tokens 25000` includes internal reasoning and the final assessment.
This ceiling follows [OpenAI's initial reasoning-token guidance](https://developers.openai.com/api/docs/guides/reasoning#allocating-space-for-reasoning)
and does not force each item to consume that many tokens. High effort may use
more time and tokens; its effect on scoring quality needs human-reviewed
evaluation. The request timeout is 600 seconds to accommodate longer responses.
An incomplete or invalid response is recorded as an error, never as a low
validity score.

## Process and scoring

1. **Discover and pin the data.** `inventory` reads `main` and
   `migration/tabular-builders-20260924`, saving their commit IDs and item-table
   paths. It checks benchmark roots and `formatted_tables/`, avoiding raw data
   and model-response traces. `--branches` can explicitly select other branches.
   Missing item tables are reported in the inventory.
2. **Read each item.** The loader streams Parquet rows and combines the full item
   text, grading criterion/reference answer, verifier description, item features,
   asset references, and available benchmark metadata. Verifiers are never
   executed. Metadata about historical model performance is excluded.
3. **Avoid repeated judgments.** An exact hash of all supplied item evidence and
   benchmark context identifies duplicates, including copies across branches.
   Identical evidence is assessed once per deployment/run; every source remains
   traceable. Different grading criteria or context produce separate assessments.
4. **Assess all six dimensions in one call.** The deployment description and
   evidence are sent with the readable [judging prompt](prompts/assess_item.md).
   Every dimension returns a score (or an explicit unknown), confidence and its
   rationale, a short justification, evidence references, and information gaps.
5. **Validate and rank.** Python validates the structured response and computes
   a confidence-adjusted mean across all six dimensions. Every valid assessment
   enters the ranking, including those with missing evidence. Results retain the
   original scores, confidence, gaps, and source provenance for human review.

| Dimension | Item-level question |
| --- | --- |
| Input ontology | Does this task or capability belong to the deployment workload or test a stated constraint? |
| Input content | Does the particular scenario fit the domain, users, language, and operating conditions? |
| Input form | Does the input modality, representation, and interaction format match? |
| Output ontology | Do the expected decisions and grading criteria measure deployment success? |
| Output content | Is the particular reference answer or expected judgment appropriate and supported? |
| Output form | Does the expected response format, modality, and language match? |

Scores range from **1 (fundamental mismatch)** to **5 (strong, evidence-supported
alignment)**, with dimension-specific anchors in the prompt. Compatibility and
confidence are separate judgments. The judge should make a defensible tentative
estimate when possible, with low confidence and explicit assumptions. When no
estimate is defensible, the score stays `null`, confidence is `insufficient`, and
an information gap is required. A missing dimension no longer discards the item.

Scoring version 2 uses a simple, inspectable policy:

| Confidence | Meaning | Ranking weight |
| --- | --- | --- |
| High | Direct, applicable evidence; no material gap | 1.0 |
| Medium | Relevant evidence with a limited inference or gap | 0.6 |
| Low | Indirect evidence or a major gap could change the estimate | 0.3 |
| Insufficient | No defensible score; stored score is `null` | 0.0 |

For each known dimension, `adjusted = 3 + weight * (score - 3)`. A missing
dimension contributes a neutral baseline of 3 **only to the ranking calculation**.
`overall_score` is the equal-weight mean of all six adjusted contributions.
`compatibility_score` is the unadjusted mean of the available scores;
`scored_dimensions` records coverage. `needs_review` flags any low-confidence or
missing dimension. The same summary is used in the CLI and hosted demo.

For example, a low-confidence 5 contributes 3.6, while a high-confidence 5
contributes 5. Five high-confidence 4s and one unknown yield an overall 3.83,
an unadjusted mean of 4, and coverage of 5/6. Six unknowns yield a baseline of 3
and no unadjusted mean. That baseline is **not evidence of compatibility** and can
rank above a supported mismatch. Review the evidence before selecting tests.

These weights are policy choices, not calibrated probabilities. Confidence is
the judge's evidence-support assessment, not measured reliability. The mean is
a demo ranking heuristic, not a validated validity or deployment-safety measure.
High means can still hide individual mismatches. Ties use evidence hashes for
deterministic ordering. Human-reviewed calibration is a later step.

## Traverse the full inventory

Omit the benchmark filter when discovering tables, and omit the row limit when
scoring:

```bash
python -m bayesian_auditing inventory \
  --output bayesian_auditing/results/inventory.json

python -m bayesian_auditing run \
  --inventory bayesian_auditing/results/inventory.json \
  --deployment bayesian_auditing/examples/deployment.txt \
  --output-dir bayesian_auditing/results/full_run \
  --top-k 50
```

This makes paid requests across the full saved inventory. Processing is
sequential for readability; large inventories can take substantial time. The
first demo does not use Batch API or concurrency. On September 25, 2026, discovery
found 113 item tables (6 on main, 107 on the migration branch); this is a table count,
not an item count, and will change as the dataset develops.

Use the same command with `--resume` after an interruption. Resume requires the
same inventory, deployment, prompt, schema, model, reasoning settings, token
limit, and row limit. Changing `--top-k` is allowed and rebuilds the ranked output
without repeating completed judgments. Changed scoring settings need a new
output folder. A preview cannot be resumed as a live run.

Scoring-version-1 runs cannot be resumed under this schema. Keep their exported
files and use a new output folder for version 2; old results have no recorded
confidence, so it must not be invented or silently backfilled. New judgments
require new API calls.

Completed assessments, including partial-evidence ones, are reused. Failed responses are retried
on resume. After the SDK's two retries, an API exception stops the run and saves
partial results, avoiding repeated requests during an authentication or quota
failure. Dataset read errors also stop the run. A partially written final JSONL
record can be recovered on resume; corruption in a complete line is reported.
An interruption after a request succeeds but before its result is saved can
cause that request to be repeated. Use one process per output directory.

## Output files

| File | Contents |
| --- | --- |
| `run.json` | Deployment, pinned inventory, model settings, rubric, and output-schema snapshot. |
| `assessments.jsonl` | Append-only assessments with confidence, errors, and duplicate source references. Previews include the exact request input. |
| `ranked_items.json` | Up to `--top-k` valid assessments ordered by adjusted score, with coverage, evidence, and all source references. |
| `summary.json` | Counts, traversal status, items needing review, errors, scoring policy, reported token usage across attempts, and any fatal error. |

Check `full_inventory_scored` before describing a result as a full ranking. It is
false for limited previews, interrupted runs, missing tables, or failed responses.
It means all items have a valid assessment, not that all dimensions are known or
confident; inspect `needs_review` and individual gaps. “Full inventory” means the tables in the saved
inventory, which may itself contain a benchmark/branch filter. A partial ranked
list is still saved for review, but omitted items could otherwise have ranked
highly. Reported output tokens already include reasoning tokens; do not add
them again when estimating cost. Usage may be unavailable for failed requests.

The text demo records media references but does not download or inspect images,
audio, or linked documents. Relevant dimensions remain unknown when those assets
are necessary and no defensible inference is possible. No input text is silently truncated. An item that
exceeds API limits will need explicit handling in a later iteration.

## Maintainer guide

| File | Responsibility |
| --- | --- |
| `data.py` | Discover tables, pin revisions, normalize evidence, and preserve provenance. |
| `prompts/assess_item.md` | Six-dimensional rubric and evidence requirements. |
| `scoring.py` | Typed output schema, validation, and aggregate arithmetic. |
| `judge.py` | One structured OpenAI Responses request. |
| `runner.py` | Sequential traversal, duplicate detection, checkpoint log, and ranking. |
| `__main__.py` | CLI arguments and client setup. |

The modules are independent of the existing website and Anthropic pipeline. The
rubric is deliberately an item-level adaptation: a single item cannot establish
the coverage or validity of an entire benchmark. Hashes and source IDs are kept
in memory for resume/deduplication; full item records are streamed, and ranking
retains only the requested top items. Increase `DATA_VERSION` or
`SCORING_VERSION` when changes would make previous runs incompatible.

```bash
python -m pip install -r bayesian_auditing/requirements-dev.txt
python -m pytest bayesian_auditing/tests -q
```

Tests use local Parquet fixtures for both branch layouts and mock HTTP responses
through the real OpenAI SDK. They cover validation, ranking, duplicate handling,
resume, incomplete/refused responses, and failure reporting without paid calls.
They do not establish judge quality. Human review of a small live run is needed
before relying on a full-corpus ranking.

API references: [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)
and [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).
