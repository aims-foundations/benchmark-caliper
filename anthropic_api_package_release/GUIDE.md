# Reviewer Guide

This package contains the validity analysis pipeline and all experiment artifacts from our study. It supports three modes of engagement:

1. **Inspect experiment results** — Browse the full pipeline outputs from all expert assessments
2. **Reproduce an existing assessment** — Re-run the pipeline on any of our expert tuples
3. **Run your own assessment** — Evaluate a benchmark of your choice against a custom deployment context

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with your Anthropic API key (required for modes 2 and 3):

```bash
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

The pipeline uses `pdftk` or `qpdf` for PDF splitting. Install one of:

```bash
brew install pdftk-java   # macOS
brew install qpdf          # alternative
```

---

## 1. Inspect Experiment Results

All pipeline outputs are included as artifacts. No API key needed.

### Assessment outputs

Each expert assessment lives under `assessments/<expert_id>__<benchmark>/<deployment_slug>/`. A complete assessment contains:

| File | Description |
|------|-------------|
| `deployment_description.txt` | The deployment scenario provided by the expert |
| `elicitation_questions.json` | Pipeline-generated questions tailored to the deployment |
| `elicitation_answers.json` | Expert's answers to those questions |
| `elicitation_summary.md` | Synthesized priority weights and deployment context |
| `paper_summary.md` | Structured extraction from the benchmark paper |
| `benchmark.yaml` | Synthesized benchmark profile |
| `region.yaml` | Region-specific context for the deployment |
| `composed_prompt.md` | The full evaluation prompt sent to Opus |
| `scoring.json` | Opus's structured validity scores across 6 dimensions |
| `report.md` | Human-readable formatted report |
| `pdfs/review.pdf` | Concatenated 7-section PDF (summary + 6 dimensions) |
| `traces/` | Raw API call traces for every pipeline step |

### Suggested reading order for one assessment

1. `deployment_description.txt` — What deployment is being evaluated
2. `elicitation_questions.json` + `elicitation_answers.json` — The expert dialogue
3. `pdfs/review.pdf` — The final validity report (start here for a quick overview)
4. `scoring.json` — Raw scores if you want to inspect dimensions programmatically
5. `composed_prompt.md` — The full prompt sent to Opus (to understand what the model saw)

### Expert validation results (Stage 3)

Expert ratings of the pipeline's outputs are in `stage3_results/`:

- `primary_assessments.json` — Expert Likert ratings for each assessment
- `comparative_assessments.json` — Expert ratings comparing regional vs. reference benchmarks
- `plots/` — Visualizations used in the paper
- `raw/` — Raw Google Form responses

### Directory conventions

- `expert_<hash>__<benchmark>` — A regional benchmark assessment
- `expert_<hash>__<comparator>` — A reference benchmark assessment (e.g., MMLU, GLUE)
- Comparator pairs are listed in `benchmarks/hf_links.json` under `_comment_comparative`

---

## 2. Reproduce an Existing Assessment

Re-run any assessment to verify the pipeline produces structurally similar results. Two modes:

### Re-run scoring only (one Opus call, ~$0.50)

Keeps all upstream outputs cached; only the Opus scoring, report, and review PDF are regenerated:

```bash
python run_pipeline.py papers/<expert_id>__<benchmark>.pdf \
  --use-case assessments/<expert_id>__<benchmark>/<slug>/deployment_description.txt \
  --rerun-scoring
```

### Re-run the full pipeline (~$2-5)

Clears all cached outputs and runs every step from scratch:

```bash
python run_pipeline.py papers/<expert_id>__<benchmark>.pdf \
  --use-case assessments/<expert_id>__<benchmark>/<slug>/deployment_description.txt \
  --rerun-all
```

### Concrete example

```bash
# Re-score the CrisisLTLSum/Ecuador assessment
python run_pipeline.py papers/expert_3fcd1181e6a6__crisisltlsum.pdf \
  --use-case assessments/expert_3fcd1181e6a6__crisisltlsum/ecuador_spanish_disaster_response/deployment_description.txt \
  --rerun-scoring
```

Since LLM outputs are non-deterministic, scores will differ slightly between runs. The pipeline structure, dimensions, and evidence citations should be consistent.

---

## 3. Run Your Own Assessment

Evaluate any benchmark paper against a deployment context you define. This follows a two-step process:

### Step A: Generate tailored questions

1. **Prepare your deployment description.** Copy the template and fill it in:

   ```bash
   cp templates/deployment_description.txt my_deployment.txt
   # Edit my_deployment.txt with your deployment scenario
   ```

   See `templates/example_deployment_description.txt` for a filled-in example.

2. **Run the pipeline through question generation:**

   ```bash
   python run_pipeline.py your_paper.pdf --use-case my_deployment.txt --step 2-questions
   ```

   This produces `assessments/<paper_stem>/<slug>/elicitation_questions.json` — a set of 4 questions tailored to your deployment context, one per validity dimension.

### Step B: Provide answers and generate the report

1. **Answer the questions.** Create a JSON file mapping question IDs to your answers:

   ```json
   {
     "Q1": "Your answer to question 1...",
     "Q2": "Your answer to question 2...",
     "Q3": "Your answer to question 3...",
     "Q4": "Your answer to question 4..."
   }
   ```

   Save it as `assessments/<paper_stem>/<slug>/elicitation_answers.json`. See `templates/example_elicitation_answers.json` for a filled-in example.

2. **Run the full pipeline:**

   ```bash
   python run_pipeline.py your_paper.pdf --use-case my_deployment.txt
   ```

   The pipeline detects your pre-filled answers, skips interactive prompting, and runs all remaining steps. Output: `assessments/<paper_stem>/<slug>/pdfs/review.pdf`.

### Optional: HuggingFace dataset analysis

If the benchmark has a HuggingFace dataset, the pipeline can run automated dataset analysis (schema, label distributions, language profiles):

```bash
python run_pipeline.py your_paper.pdf --use-case my_deployment.txt --hf-dataset org/dataset_name
```

### Cost estimate

A full run on a typical 15-30 page paper costs $2-5 in API calls. The breakdown:
- Steps 1-6 (Haiku + Sonnet): ~$1-3
- Step 7 (Opus scoring): ~$0.50-1.50
- Steps 8-9 (local, no API): $0

---

## Pipeline Architecture

See `ARCHITECTURE.md` for the full pipeline flow and `framework.yaml` for the validity dimension definitions. All LLM prompts are in `prompts/*.md`.
