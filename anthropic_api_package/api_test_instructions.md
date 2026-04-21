# API Test Instructions

Step-by-step plan for running the validity pipeline against the live Anthropic
API, one API call at a time, so you can verify each output before committing
to the next call. Every Haiku / Sonnet / Opus call is its own `--step` key —
any step that used to bundle multiple calls (e.g. `1a` = N Haiku + 1 Sonnet)
has been split so each call is its own debugging unit.

## 1. API key setup

`client.py` reads `ANTHROPIC_API_KEY` from the environment and (via
`python-dotenv`) from a `.env` file in `api_package/`.

```bash
cp api_package/.env.example api_package/.env
# then edit .env and set:
#   ANTHROPIC_API_KEY=sk-ant-...
```

Either `.env` or an exported shell env var works — whichever you prefer.
`.env` is gitignored.

## 2. Incremental test plan

Place a real paper PDF at `api_package/papers/<name>.pdf` (e.g.
`papers/helm.pdf`), then run steps one at a time. After each step, inspect
the output file before continuing. `--show-cost` prints the running ledger.

**Tip — inspect the prompt before paying.** Append `--dry-run` to any
`--step X` command to print the exact system + user prompt that step would
send, skip the API call, and leave the cost ledger untouched. Pipe it
through `less` for long prompts:

```bash
python run_pipeline.py $PDF --step 3b-synthesize --dry-run | less
```

Dry-run uses whatever real outputs are on disk from prior steps, so
`--step 3b-synthesize --dry-run` after a real `--step 3a-consolidate` shows
you the exact Sonnet prompt built from the real paper summary.

```bash
cd api_package
PDF=papers/helm.pdf                # change to your paper
NAME=helm                          # must match PDF stem
PERSONA=helm-b                     # or helm-a / sea-a / sea-b / iber-a / iber-b
```

### Step 0 — Derive the assessment slug
1 Haiku; **< $0.001**

The slug is a short, human-readable identifier for this deployment (e.g.
`kenya_chw_swahili_dholuo`). It scopes every deployment-specific output
under `assessments/${NAME}/<slug>/`. Derived once from the persona's
`initial_description` (or `--use-case` file), then persisted as
`assessments/${NAME}/active_slug.txt`.

```bash
python run_pipeline.py $PDF --step 0 --persona $PERSONA
# inspect: assessments/${NAME}/active_slug.txt
#          assessments/${NAME}/<slug>/deployment_description.txt
```

Delete `assessments/${NAME}/active_slug.txt` to force re-derivation (e.g.
after swapping personas). Old slug dirs stick around — comparing two
personas on the same paper just means two sibling `<slug>/` dirs.

### Step 1 — Metadata extraction (Haiku, pages 1-2)
1 Haiku; **< $0.001**

Reads only the first 1-2 pages of the PDF and extracts lightweight metadata
(name, domain, languages, region, porting strategy). This runs fast (~5s) so
elicitation questions can be presented within ~30 seconds of pipeline start.

```bash
python run_pipeline.py $PDF --step 1
# inspect: papers/${NAME}/metadata.md
```

### Step 2-questions — elicitation questions + persona handoff
1 Sonnet; **~$0.01**

Uses lightweight metadata (not the full benchmark YAML) to generate targeted
deployment-context questions.

```bash
SLUG=$(cat assessments/${NAME}/active_slug.txt)
python run_pipeline.py $PDF --step 2-questions --persona $PERSONA
# inspect: assessments/${NAME}/${SLUG}/elicitation_questions.json
#          assessments/${NAME}/${SLUG}/persona_prompt.md   ← hand to a CC Opus subagent
```

### CC Opus subagent handoff
**No API cost** — In a Claude Code session, dispatch an Opus subagent with the
system prompt + user message from
`assessments/${NAME}/${SLUG}/persona_prompt.md`. Save its JSON reply to
`assessments/${NAME}/${SLUG}/elicitation_answers.json`.

### Step 2-summary — elicitation summary
1 Sonnet; **~$0.02**

```bash
python run_pipeline.py $PDF --step 2-summary \
    --answers assessments/${NAME}/${SLUG}/elicitation_answers.json
# inspect: assessments/${NAME}/${SLUG}/elicitation_summary.md
```

### Step 3a-extract — PDF extraction (per-page Haiku fan-out)
~30 Haiku calls serially (1 worker); **~$0.04–0.12**; ~2–3 min wall-clock

The Haiku fan-out is single-threaded by default to stay under common
per-minute TPM caps (50k TPM at tier 1 is enough for ~15 calls/min; one
worker paces naturally at ~12 calls/min). If you're on a higher tier,
edit `max_workers` in `step_1a_extract` to speed things up.

```bash
python run_pipeline.py $PDF --step 3a-extract
# inspect: page_caches/${NAME}/page_NNN.txt
python run_pipeline.py $PDF --show-cost
```

**Resumable.** Each page's Haiku output is written to
`page_caches/${NAME}/page_NNN.txt` as soon as the call returns. If the step
crashes partway (e.g. a 429 rate-limit error that outruns the SDK's retry
budget), just re-run `--step 3a-extract` — cached pages are skipped and
only the missing ones are re-dispatched. The cost ledger accumulates across
retries so the final `--show-cost` total reflects the real cost of all
pages, not just the last retry's.

If you want a truly fresh re-run (new prompts, updated PDF, etc.), delete
the cache dir first:
```bash
rm -rf page_caches/${NAME}
```

### Step 3a-consolidate — paper summary (Sonnet merge)
1 Sonnet; **~$0.02–0.05**

Reads every `page_caches/${NAME}/page_NNN.txt` and folds them into a single
paper summary. When an elicitation summary exists, uses dimension priority
weights to allocate narrative depth (HIGH: 4-6 sentences, MODERATE: 2-4,
LOWER: 1-2). Quote extraction remains exhaustive regardless of priorities.

```bash
python run_pipeline.py $PDF --step 3a-consolidate
# inspect: papers/${NAME}/paper_summary.md
```

### Step 3b-select — pick reference benchmark YAMLs
1 Haiku; **~$0.001**

Picks 1–2 YAMLs from `benchmarks/examples/` to use as ICL context for the
synthesis step. Selection is persisted so the synthesis step can be
re-run / dry-run without re-asking Haiku.

```bash
python run_pipeline.py $PDF --step 3b-select
# inspect: papers/${NAME}/benchmark_refs.json
```

### Step 3b-synthesize — benchmark YAML synthesis
1 Sonnet; **~$0.03–0.10**. Upper bound applies when the paper is long and
the quote registry is dense (the output can run 10k+ tokens before the new
32k `max_tokens` ceiling). When an elicitation summary is available, includes
a `coverage_gap_analysis` section cross-referencing user priorities against
benchmark documentation.

```bash
python run_pipeline.py $PDF --step 3b-synthesize
# inspect: benchmarks/${NAME}.yaml
```

### Step 3c-verify — mechanical quote verification
Script only, **no API cost**.

```bash
python run_pipeline.py $PDF --step 3c-verify
# inspect console output; fails loud if YAML quotes don't match the summary
```

### Step 4a-template — pick base region templates
1 Haiku; **~$0.001**

Picks 1–2 templates from `regions/base/` to seed the region YAML. Selection
is persisted so the synthesis step can be re-run / dry-run without re-asking
Haiku.

```bash
python run_pipeline.py $PDF --step 4a-template
# inspect: assessments/${NAME}/${SLUG}/region_templates.json
```

### Step 4b-synthesize — region YAML synthesis
1 Sonnet; **~$0.03–0.05**

```bash
python run_pipeline.py $PDF --step 4b-synthesize
# inspect: assessments/${NAME}/${SLUG}/region.yaml
```

### Step 5 — web-search enrichment (optional)
1 Sonnet + up to 10 web searches; **~$0.20–0.50**. Skip if you want to save
budget — step 6 will use whatever region YAML is on disk. Prioritizes
`coverage_gap_analysis` from the benchmark YAML when available.

```bash
python run_pipeline.py $PDF --step 5
# inspect: assessments/${NAME}/${SLUG}/region.yaml (overwritten in place)
```

### Step 6 — compose evaluation prompt
Script, **no API cost**.

```bash
python run_pipeline.py $PDF --step 6
# inspect: assessments/${NAME}/${SLUG}/composed_prompt.md
```

### Step 7 — Opus scoring
1 Opus; **~$0.50–1.50**. Biggest line item.

```bash
python run_pipeline.py $PDF --step 7
# inspect: assessments/${NAME}/${SLUG}/scoring.json
```

### Step 8 — format report
Script, no API cost.

```bash
python run_pipeline.py $PDF --step 8
# final human-readable report prints to stdout
```

### Final cost audit

```bash
python run_pipeline.py $PDF --show-cost
# per-step In$ / Out$ / Tools$ / Total$
# raw JSON also at assessments/${NAME}/${SLUG}/cost_ledger.json
```

The ledger + traces are **assessment-scoped**
(`assessments/${NAME}/${SLUG}/`), so a single paper can hold multiple
assessments (one per deployment slug) side by side without clobbering each
other.

### Per-call trace (inputs, outputs, duration, cost)

Every real (non-dry-run) API call appends a JSON line to
`assessments/${NAME}/${SLUG}/traces/<step_label>.jsonl` — one JSONL file per
step label, so the 3a-extract fan-out lands in
`traces/3a_extract.jsonl` (N lines, one per page), while single-call steps
like `3a_consolidate`, `3b_select`, etc. each get a one-line file. Each
record carries: `timestamp, step, model, max_tokens, pdf_path, tools,
duration_seconds, system, user, output, tool_trace, usage, cost_usd`.
Overwrite-on-rerun stays in sync with the cost ledger — re-running a step
wipes that step's trace file before writing the new run.

`tool_trace` is an ordered list of any `server_tool_use` (the query the
model issued) and `web_search_tool_result` (title / url / page_age for
each result the model got back) blocks from the response. Empty for
calls that didn't use tools. Makes step 3 post-hoc auditable — you can
see every query Sonnet ran and every URL it retrieved, which is how
you'd diagnose citation quality or tighten the web-search prompt in a
future iteration.

Step-label names (underscore-form) match what appears in `--show-cost`:
`0_slug`, `1a_extract`, `1a_consolidate`, `1b_select`, `1b_synthesize`,
`1d_questions`, `1d_summary`, `2a_template`, `2b_synthesize`,
`3_web_search`, `5_score`.

```bash
SLUG=$(cat assessments/${NAME}/active_slug.txt)
TRACES=assessments/${NAME}/${SLUG}/traces
```

Useful queries:

```bash
# Top 5 most expensive calls across all steps
cat $TRACES/*.jsonl \
    | jq -c '{step, model, cost_usd, dur: .duration_seconds}' \
    | sort -t: -k4 -gr | head -5

# Longest calls
cat $TRACES/*.jsonl \
    | jq -c '{step, model, dur: .duration_seconds, cost_usd}' \
    | sort -t: -k3 -gr | head -5

# Full prompt for a specific step (one file per step now)
jq '.system, .user' $TRACES/1b_synthesize.jsonl

# Every web-search query the step 3 run issued
jq -r '.tool_trace[] | select(.type=="server_tool_use") | .input.query' \
    $TRACES/3_web_search.jsonl

# Every URL returned across those searches
jq -r '.tool_trace[] | select(.type=="web_search_tool_result") | .results[].url' \
    $TRACES/3_web_search.jsonl
```

## 3. Expected total

- **With web search:** ~$1–2.50
- **Without web search:** ~$0.70–1.50

## 4. Re-running a step

If any single step's output looks wrong, just re-run that step. The cost
ledger overwrites that step's row rather than accumulating, and the step's
trace file is wiped at the start of the re-run — so after any number of
retries `--show-cost` and `traces/<step>.jsonl` both reflect the "final
run" view, a clean point estimate of what a successful end-to-end pipeline
execution costs.
