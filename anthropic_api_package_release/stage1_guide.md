# Stage 1 Test: SEA-HELM + IberBench

Test CSV with 1 row (4 tuples) using personas:
- Tuple 1: sea-a (Indonesian ministry chatbot) — SEA-HELM
- Tuple 2: sea-b (KL refugee legal aid) — SEA-HELM
- Tuple 3: iber-a (Barcelona Catalan moderation) — IberBench
- Tuple 4: iber-b (Oaxaca Zapotec education) — IberBench

## Environment setup

```bash
# API key — either .env file or export
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
# or: export ANTHROPIC_API_KEY=sk-ant-...

cd anthropic_api_package
```

## Phase 0: Parse CSV + auto-link PDFs

Expects `papers/sea-helm.pdf` and `papers/iberbench.pdf` to exist.

```bash
python run_expert_stage1.py expert_responses/form_responses/stage_1/test_expert_proposals.csv --parse-only
```

This creates:
- `expert_responses/test_expert_proposals/rud721_gmail_com/` — dir structure, row.json
- `expert_responses/.../pdfs/sea_helm.pdf` and `iberbench.pdf` — symlinks to papers/
- `papers/rud721_gmail_com__sea_helm.pdf` and `rud721_gmail_com__iberbench.pdf` — namespaced symlinks
- `expert_responses/.../tuples/tuple_N/deployment_description.txt` — one per tuple

Verify:
```bash
ls -la expert_responses/test_expert_proposals/rud721_gmail_com/pdfs/
ls -la papers/rud721_gmail_com__*.pdf
```

## Phase 1: Step-by-step on tuple 1

Walk through each pipeline step manually for the SEA-HELM / Indonesian
ministry deployment. Use the namespaced papers/ symlink so the pipeline
sees `rud721_gmail_com__sea_helm` as the paper name (not the original
`sea-helm` from any prior runs).

```bash
export PDF=papers/rud721_gmail_com__sea_helm.pdf
export NAME=rud721_gmail_com__sea_helm
export USE_CASE=expert_responses/test_expert_proposals/rud721_gmail_com/tuples/tuple_1/deployment_description.txt
```

### Step 0 — derive assessment slug

```bash
python run_pipeline.py $PDF --step 0 --use-case $USE_CASE
```

### Step 1 — lightweight metadata (Haiku, pages 1-2)

```bash
python run_pipeline.py $PDF --step 1
```

### Step 2 — elicitation questions (Sonnet)

```bash
python run_pipeline.py $PDF --step 2-questions --use-case $USE_CASE
```

Pause and inspect:
```bash
SLUG=$(cat assessments/$NAME/active_slug.txt)
cat assessments/$NAME/$SLUG/elicitation_questions.json | python3 -m json.tool
```

### Step 3a — per-page PDF extraction (Haiku fan-out, ~2-3 min)

```bash
python run_pipeline.py $PDF --step 3a-extract
python run_pipeline.py $PDF --show-cost
```

### Step 3a — consolidate into paper summary (Sonnet)

```bash
python run_pipeline.py $PDF --step 3a-consolidate
```

### Step 3b — pick reference benchmark YAMLs (Haiku)

```bash
python run_pipeline.py $PDF --step 3b-select
```

### Step 3b — synthesize benchmark YAML (Sonnet)

```bash
python run_pipeline.py $PDF --step 3b-synthesize
```

### Step 3c — mechanical quote verification (script)

```bash
python run_pipeline.py $PDF --step 3c-verify
```

### Check cost so far

```bash
python run_pipeline.py $PDF --show-cost
```

At this point tuple 1's `elicitation_questions.json` is written (from step 2),
and the paper-level artifacts (`paper_summary.md`,
`benchmarks/rud721_gmail_com__sea_helm.yaml`, page cache) are all on disk and
will be reused by tuple 2 (which shares the same benchmark).

## Phase 2: Batched mode for tuples 2-4

Run the full stage-1 wrapper. Expected behavior:
- **Tuple 1**: skipped (already has `elicitation_questions.json`)
- **Tuple 2**: runs steps 0, 1, 2-questions; skips sea_helm paper-level steps (cached from tuple 1)
- **Tuple 3**: runs steps 0, 1, 2-questions + full iberbench paper-level extraction (first time)
- **Tuple 4**: runs steps 0, 1, 2-questions; skips iberbench paper-level steps (cached from tuple 3)

```bash
python run_expert_stage1.py expert_responses/form_responses/stage_1/test_expert_proposals.csv
```

Summary should show: 3 done, 1 skipped, 0 failed.

## Phase 3: Generate the Google Form

After all 4 tuples have `elicitation_questions.json`:

```bash
# Preview form structure
python generate_expert_forms.py expert_responses/form_responses/stage_1/test_expert_proposals.csv --dry-run

# Create the real form
python generate_expert_forms.py expert_responses/form_responses/stage_1/test_expert_proposals.csv
```

Creates the form and writes `stage2_form.json` with the URL and question
mapping to `expert_responses/test_expert_proposals/rud721_gmail_com/`.
