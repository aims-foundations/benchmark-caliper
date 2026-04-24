# Stage 2: Running the Pipeline on Expert Answers

After experts submit their elicitation answers via the Stage-2 Google Form,
this guide walks through running the rest of the validity pipeline (steps
2-summary through 8) on those answers.

## Prerequisites

1. **Stage 1 complete** for the expert — `row.json`, assessment slugs,
   `elicitation_questions.json`, and PDFs all present under
   `expert_responses/<csv_stem>/<expert_id>/`.

2. **Stage-2 CSV** downloaded from Google Forms and placed under
   `expert_responses/form_responses/stage_2/`. One CSV per expert
   (or a combined export with multiple rows).

3. **HF links** configured in `benchmarks/hf_links.json` for any benchmarks
   where you want dataset analysis (Step 5b). Benchmarks with null entries
   skip DA gracefully.

4. **API key** set via `.env` or environment variable:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   ```

## CSV format

The Stage-2 CSV is a Google Forms export with this layout:

| Col | Content |
|-----|---------|
| 0 | Timestamp |
| 1 | Email Address |
| 2-6 | Tuple 1: Q1, Q2, Q3, Q4, Feedback |
| 7-11 | Tuple 2: Q1, Q2, Q3, Q4, Feedback |
| 12-16 | Tuple 3: Q1, Q2, Q3, Q4, Feedback |
| 17-21 | Tuple 4: Q1, Q2, Q3, Q4, Feedback |

The script matches the expert by email against stage-1 `row.json` files.

## Quick start: run everything

Process all CSVs in `form_responses/stage_2/`, all experts, all tuples:

```bash
cd anthropic_api_package
python run_expert_stage2.py
```

Or point to a specific CSV:

```bash
python run_expert_stage2.py expert_responses/form_responses/stage_2/fred_philippy.csv
```

### What happens

For each expert matched by email, for each tuple (1-4):

1. Writes `elicitation_answers.json` to the assessment directory
2. Writes `expert_feedback.txt` to the tuple directory (if feedback provided)
3. Runs pipeline steps: `2-summary` → `3a-extract` → `3a-assemble` → `3a-consolidate` →
   `3b-select` → `3b-synthesize` → `3c-verify` → `4a-template` →
   `4b-synthesize` → `5` (web search) → `5b-da` (dataset analysis) →
   `6` (compose) → `7` (Opus scoring) → `8` (report)
4. Copies final artifacts (`scoring_output.json`, `composed_prompt.md`,
   `elicitation_summary.md`, `da_report.md`) back to the tuple directory

Paper-level steps (3a/3b/3c) are idempotent — if tuple 1 and tuple 2
share a benchmark, the second tuple reuses the cached paper summary and
benchmark YAML. DA script outputs and per-dataset summaries are also
cached under `benchmarks/da_cache/`, so multiple tuples sharing a
benchmark only run the deterministic scripts once.

### Expected cost

Per tuple (approximate):
- Steps 2-summary through 4b: ~$0.05-0.10 (Sonnet + Haiku)
- Step 5 web search: ~$0.02-0.05 (Sonnet)
- Step 5b DA interpretation: ~$0.02-0.05 (Sonnet), scripts are free
- Step 7 Opus scoring: ~$0.30-0.50 (the one Opus call)
- **Total per tuple: ~$0.40-0.70**

For 4 tuples: ~$1.50-2.80 total (less if tuples share benchmarks).

## Dry run

Preview what would happen without making API calls:

```bash
python run_expert_stage2.py --dry-run
```

## Parse-only mode

Write answers to disk without running the pipeline — useful for verifying
the CSV was parsed correctly before spending API credits:

```bash
python run_expert_stage2.py --parse-only
```

Then inspect the written answers:

```bash
EXPERT=expert_b082a2ed12a9
BENCH=expert_b082a2ed12a9__ltzglue
SLUG=$(cat assessments/$BENCH/active_slug.txt)
cat assessments/$BENCH/$SLUG/elicitation_answers.json | python3 -m json.tool
```

## Single tuple

Restrict to one tuple (useful for debugging or step-by-step runs):

```bash
python run_expert_stage2.py --tuple 3
```

## Force re-run

By default, tuples with existing `scoring_output.json` are skipped.
Use `--force` to re-run:

```bash
python run_expert_stage2.py --force --tuple 1
```

## Step-by-step: manual run for a single tuple

For debugging or inspecting intermediate outputs, you can run each
pipeline step individually. This example walks through tuple 3
(DrBenchmark / hospital clinician use case) for expert Fred Philippy.

### Setup

```bash
cd anthropic_api_package

# Identify the paper stem and slug
export EXPERT=expert_b082a2ed12a9
export BENCH=drbenchmark
export PAPER_STEM=${EXPERT}__${BENCH}
export PDF=papers/${PAPER_STEM}.pdf
export TUPLE_DIR=expert_responses/stage1_responses_042226/$EXPERT/tuples/tuple_3

# Read the slug from the tuple directory (NOT from active_slug.txt,
# which tracks the last tuple that ran and may belong to a different tuple)
export SLUG=$(cat $TUPLE_DIR/assessment_slug.txt)

# Set active_slug.txt so run_pipeline.py resolves to this tuple's assessment
echo "$SLUG" > assessments/$PAPER_STEM/active_slug.txt
```

### Step 0: Write answers (manual)

First, parse the CSV to write answers without running the pipeline:

```bash
python run_expert_stage2.py --parse-only --tuple 3
```

Verify:
```bash
cat assessments/$PAPER_STEM/$SLUG/elicitation_answers.json | python3 -m json.tool

# Only exists if the expert provided feedback on the generated questions
cat $TUPLE_DIR/expert_feedback.txt 2>/dev/null || echo "(no feedback)"
```

### Step 1: Elicitation summary (Sonnet)

```bash
python run_pipeline.py $PDF --step 2-summary \
  --answers assessments/$PAPER_STEM/$SLUG/elicitation_answers.json
```

Inspect the summary:
```bash
cat assessments/$PAPER_STEM/$SLUG/elicitation_summary.md
```

### Step 2: Paper extraction (if not already cached)

These are paper-level steps — they only run once per benchmark PDF,
shared across all tuples that use the same benchmark.

```bash
# Per-page extraction (Haiku fan-out, ~2-3 min for a 15-page paper)
python run_pipeline.py $PDF --step 3a-extract

# Assemble quote registry (Haiku cross-page merge + mechanical assembly)
python run_pipeline.py $PDF --step 3a-assemble

# Write narrative context (Sonnet, given the assembled registry)
python run_pipeline.py $PDF --step 3a-consolidate

# Pick reference benchmark YAMLs (Haiku)
python run_pipeline.py $PDF --step 3b-select

# Synthesize benchmark YAML (Sonnet)
python run_pipeline.py $PDF --step 3b-synthesize

# Mechanical quote verification
python run_pipeline.py $PDF --step 3c-verify
```

### Step 3: Region YAML (Sonnet)

```bash
python run_pipeline.py $PDF --step 4a-template
python run_pipeline.py $PDF --step 4b-synthesize
```

### Step 4: Web search enrichment (Sonnet)

```bash
python run_pipeline.py $PDF --step 5
```

### Step 5: Dataset analysis (optional)

Only runs if `benchmarks/hf_links.json` has an entry for the benchmark.
For DrBenchmark with `hf_org: "DrBenchmark"`, this profiles all 12
datasets under the org.

```bash
python run_pipeline.py $PDF --step 5b-da --hf-tuple tuple_3
```

This runs:
1. DA scripts on each dataset (cached under `benchmarks/da_cache/`)
2. Per-dataset Sonnet summaries (also cached)
3. Aggregated interpretation weighted by this tuple's deployment context

For the second tuple using the same benchmark (e.g., tuple 4), steps 1-2
hit the cache and only step 3 runs fresh.

Inspect the report:
```bash
cat assessments/$PAPER_STEM/$SLUG/da_report.md
```

### Step 6: Compose evaluation prompt

```bash
python run_pipeline.py $PDF --step 6
```

Review the full prompt that will be sent to Opus:
```bash
cat assessments/$PAPER_STEM/$SLUG/composed_prompt.md
```

### Step 7: Opus scoring (the expensive step)

```bash
python run_pipeline.py $PDF --step 7
```

### Step 8: Format report

```bash
python run_pipeline.py $PDF --step 8
```

### Check costs

```bash
python run_pipeline.py $PDF --show-cost
```

## Output locations

After a complete run, outputs live in two places:

**Assessment directory** (canonical):
```
assessments/<expert>__<benchmark>/<slug>/
  elicitation_answers.json    # expert's answers
  elicitation_summary.md      # Sonnet summary of Q&A
  composed_prompt.md           # full prompt sent to Opus
  da_report.md                 # dataset analysis findings (if HF info available)
  scoring_output.json          # Opus validity scores
  cost_ledger.json             # per-step API costs
  traces/                      # raw API request/response logs
```

**Expert tuple directory** (copies for easy access):
```
expert_responses/<csv_stem>/<expert_id>/tuples/tuple_N/
  elicitation_questions.json   # from stage 1
  elicitation_answers.json     # written by stage 2 (copy)
  assessment_slug.txt          # slug linking to assessment dir
  expert_feedback.txt          # optional feedback on questions
  scoring_output.json          # copy of final scores
  elicitation_summary.md       # copy
  composed_prompt.md           # copy
  da_report.md                 # copy (if available)
```

## Troubleshooting

**"no stage-1 data for <email>"**: The email in the Stage-2 CSV doesn't
match any `row.json` from stage 1. Check for typos or different email
addresses between form submissions.

**"no assessment slug (stage 1 incomplete?)"**: Stage 1 didn't finish
for this tuple. Re-run `run_expert_stage1.py` for this expert.

**"all answers empty for tuple N"**: The expert left all four questions
blank for this tuple in the form. The tuple is skipped.

**Step 5b-da skipped**: No HF info found for this benchmark in
`benchmarks/hf_links.json`. Fill in `hf_dataset_id` or `hf_org` to
enable dataset analysis. The pipeline continues without DA findings.
