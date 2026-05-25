# Culture-Agnostic Validity Gradation Experiment

Demonstrates that the validity pipeline detects validity gradations in domains
people consider "culture-neutral" -- math, code, and formal logic -- where
misalignment stems from construct mismatch, format mismatch, and scoring
criteria divergence rather than cultural transfer.

## Design

- **3 benchmarks:** GSM8K (math), HumanEval (code), FOLIO (logic)
- **2 triplets per benchmark**, each with 3 deployment descriptions
  (great / ok / terrible fit)
- **18 total assessments**
- **Population held constant:** US, English-speaking -- validity variation
  is driven entirely by use-case alignment

Each triplet tests a specific type of validity gradient:

| Benchmark | Triplet 1         | Triplet 2          |
|-----------|-------------------|--------------------|
| GSM8K     | Construct depth   | Task format        |
| HumanEval | Construct scope   | Output evaluation  |
| FOLIO     | Reasoning type    | Task structure     |

## Pipeline Execution

Three stages per assessment:

1. **Stage A (Steps 0-2a):** Run the pipeline through elicitation question
   generation. Paper-level outputs (metadata, page extraction) are shared
   across all 6 assessments of the same benchmark.

2. **Stage B (Step 2a-sim):** An Opus subagent simulates the user answering
   elicitation questions, parameterized by
   `(deployment_description, persona_context)` from `assessments.yaml`.

3. **Stage C (Steps 2b-9):** Run the remainder of the pipeline with the
   simulated answers: elicitation summary, paper extraction, benchmark YAML
   synthesis, region YAML, dataset analysis, prompt composition, Opus scoring,
   and report generation.

## Prerequisites

- `ANTHROPIC_API_KEY` set in the environment or in
  `anthropic_api_package_release/.env`
- Python dependencies from `requirements.txt` (parent directory)
- Internet access for ArXiv PDF downloads and HuggingFace dataset streaming

## Running the Experiment

All commands are run from the `anthropic_api_package_release/` directory.

### Full run (~$72, all 18 assessments)

```bash
python culture_agnostic/run_experiment.py
```

### One benchmark at a time (~$24 each)

```bash
python culture_agnostic/run_experiment.py --benchmark gsm8k
python culture_agnostic/run_experiment.py --benchmark humaneval
python culture_agnostic/run_experiment.py --benchmark folio
```

### Stage by stage

Run Stage A for all assessments first (generates elicitation questions),
then inspect the questions if desired, then Stage B (simulate answers),
then Stage C (full pipeline):

```bash
python culture_agnostic/run_experiment.py --stage A
# optionally inspect: assessments/<benchmark>/<slug>/elicitation_questions.json
python culture_agnostic/run_experiment.py --stage B
python culture_agnostic/run_experiment.py --stage C
```

### Single assessment (for debugging)

```bash
python culture_agnostic/run_experiment.py --assessment gsm8k_depth_great
```

### Dry run (no API calls)

```bash
python culture_agnostic/run_experiment.py --dry-run
```

### Check progress

```bash
python culture_agnostic/run_experiment.py --list
```

## Analyzing Results

After all 18 assessments complete:

```bash
# Print to stdout
python culture_agnostic/analyze_results.py

# Write to file
python culture_agnostic/analyze_results.py -o culture_agnostic/results.md
```

The analysis produces:
- Per-dimension score tables for each benchmark/triplet
- Monotonicity checks (great >= ok >= terrible) per dimension
- Sensitivity analysis (which dimensions discriminate most)
- Aggregate summary across all triplets

## Failure Handling

The runner is fail-fast: any failure halts immediately with a diagnostic.
This includes:

- Corrupt or incomplete PDF downloads (validated via magic bytes + size)
- Non-zero exit from any pipeline step
- Malformed or incomplete simulated-user answers
- Missing required outputs after a stage claims success (including the
  dataset analysis report -- a silently-skipped DA is caught)

Completed steps are cached, so re-running after a fix resumes where it
stopped. Use `--force` to re-run assessments that already have scoring.

## File Layout

```
culture_agnostic/
  assessments.yaml              # all 18 assessment definitions
  prompts/
    simulated_user.md           # Opus subagent prompt template
  run_experiment.py             # orchestrator (fail-fast)
  analyze_results.py            # post-hoc analysis
  deployment_descriptions/      # generated at runtime (--use-case files)
  README.md                     # this file
```

Assessment outputs land in the standard pipeline directories:

```
papers/<benchmark>/             # paper-scoped (metadata, quotes, summary)
page_caches/<benchmark>/        # per-page Haiku extraction cache
assessments/<benchmark>/<slug>/ # per-assessment outputs
```

## Cost Estimate

18 assessments x ~$4 per assessment = ~$72 USD.

Stage B (simulated user) adds one Opus call per assessment (~$0.50 each,
~$9 total) on top of the standard pipeline cost.

## Assessment Naming Convention

Slugs follow `{benchmark}_{triplet}_{fit}`:

```
gsm8k_depth_great       gsm8k_format_great
gsm8k_depth_ok          gsm8k_format_ok
gsm8k_depth_terrible    gsm8k_format_terrible
humaneval_scope_great    humaneval_output_eval_great
humaneval_scope_ok       humaneval_output_eval_ok
humaneval_scope_terrible humaneval_output_eval_terrible
folio_reasoning_great    folio_structure_great
folio_reasoning_ok       folio_structure_ok
folio_reasoning_terrible folio_structure_terrible
```

Note: pipeline slugs are derived by Haiku from the deployment description,
so the actual directory names under `assessments/` may differ from these
labels. The runner matches assessments by deployment description text, not
by slug name.
