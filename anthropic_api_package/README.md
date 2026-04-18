# Validity Analyzer (API Pipeline)

A framework for assessing whether AI benchmarks developed in one cultural context can be validly applied to another. Based on the paper *"Validity Analysis when Porting Benchmarks Across Cultures and Regions"* (Corona, Truong, Trager, 2025).

The tool evaluates benchmarks across **6 validity dimensions** (Input/Output × Ontology/Content/Form) and produces scored JSON reports via a cost-routed pipeline of direct Anthropic API calls (Haiku / Sonnet / Opus + deterministic scripts).

This package is a standalone alternative to `cli_package/`, which runs the same pipeline under the Claude Code CLI. Both use identical prompts, schemas, and model routing; only the orchestration layer differs.

## Repository Structure

```
anthropic_api_package/
├── README.md                   # This file
├── ARCHITECTURE.md             # Pipeline flow + cost breakdown
├── framework.yaml              # 6 validity dimensions, checklists, scoring rubric
├── prompt_template.md          # Evaluation prompt template
├── requirements.txt            # Python dependencies
├── .env.example                # ANTHROPIC_API_KEY=
│
├── run_pipeline.py             # CLI entry point (orchestrator)
├── client.py                   # Anthropic SDK wrapper (call / call_parallel)
├── prompts.py                  # Thin loader for prompts/*.md
├── personas.py                 # 6 test personas (helm-a/b, sea-a/b, iber-a/b)
│
├── prompts/                    # All LLM prompts as .md files
│   ├── pdf_extract_page.md
│   ├── pdf_extract_consolidate.md
│   ├── benchmark_example_selection.md
│   ├── benchmark_synthesis.md
│   ├── elicitation_questions.md
│   ├── elicitation_summary.md
│   ├── slug_from_description.md
│   ├── region_template_selection.md
│   ├── region_synthesis.md
│   ├── web_search_guide.md
│   ├── persona_system.md
│   └── opus_scoring_framing.md
│
├── scripts/                    # Deterministic helpers (re-runnable from CLI)
│   ├── split_pdf.sh
│   ├── verify_quotes.py
│   ├── compose_prompt.py
│   ├── format_results.py
│   ├── parse_llm_output.py                # fence-strip + JSON/YAML parse
│   ├── parse_elicitation_questions.py     # validate structured question array
│   └── assemble_elicitation_answers.py    # merge Q + A into summary prompt
│
├── benchmarks/
│   ├── examples/               # 32 curated benchmark YAMLs (read-only ICL references)
│   └── <name>.yaml             # Per-paper generated YAMLs (pipeline output, gitignored)
├── regions/base/               # 7 curated region templates (read-only ICL seeds)
├── papers/<name>/              # Paper-scoped artifacts: paper_summary.md, benchmark_refs.json (gitignored)
├── page_caches/<name>/         # Per-page Haiku extraction cache (gitignored)
└── assessments/<name>/         # Per-paper assessment tree (gitignored)
    ├── active_slug.txt         # Pointer to the current deployment slug
    └── <slug>/                 # One directory per deployment — all deployment-scoped artifacts live here
        ├── deployment_description.txt
        ├── elicitation_questions.json
        ├── elicitation_answers.json
        ├── persona_prompt.md
        ├── elicitation_summary.md
        ├── region_templates.json
        ├── region.yaml
        ├── composed_prompt.md
        ├── scoring.json
        ├── cost_ledger.json
        └── traces/             # Per-step JSONL traces (one file per step)
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Provide your Anthropic API key

Copy `.env.example` to `.env` and paste your key:

```bash
cp .env.example .env
# edit .env:
# ANTHROPIC_API_KEY=sk-ant-...
```

`client.py` reads the key at import time via `python-dotenv`; the shell environment works too.

### 3. (Optional) Install PDF tooling

`scripts/split_pdf.sh` uses `pdftk` or `qpdf` to split PDFs into per-page files for the Haiku fan-out in Step 1a.

```bash
brew install pdftk-java        # macOS, or
brew install qpdf
```

## Running the Pipeline

Drop a benchmark paper PDF into `papers/` and run:

```bash
python run_pipeline.py papers/<name>.pdf
```

### Flags

| Flag | Purpose |
|------|---------|
| `--persona PID` | Auto-answer elicitation using a test persona (PID is one of `helm-a`, `helm-b`, `sea-a`, `sea-b`, `iber-a`, `iber-b`). The persona's `initial_description` is used as the deployment context, and answers are simulated by a Sonnet call in-character. |
| `--use-case PATH` | Read the deployment description from a file. Overrides the persona's `initial_description` (persona still used for answers). |
| `--no-web-search` | Skip Step 3 (web search enrichment). |

If neither `--persona` nor `--use-case` is set, the pipeline prompts for a deployment description on stdin (Ctrl-D to end), then collects each elicitation answer interactively.

### What the pipeline does

| Step | Who | Output |
|------|-----|--------|
| 0 — Slug | Haiku (one-shot) | `assessments/<name>/active_slug.txt` + `<slug>/deployment_description.txt` |
| 1a — PDF extraction | Haiku per-page (parallel) + Sonnet consolidation | `papers/<name>/paper_summary.md` |
| 1b — Benchmark YAML | Haiku example-select + Sonnet synthesis (ICL from `benchmarks/examples/`) | `benchmarks/<name>.yaml` |
| 1c — Quote verification | `scripts/verify_quotes.py` + Sonnet text spot-check | Mechanical + LLM check |
| 1d — Elicitation | Sonnet (questions → persona/stdin answers → summary) | `assessments/<name>/<slug>/elicitation_summary.md` |
| 2 — Region YAML | Haiku template-select + Sonnet synthesis (ICL from `regions/base/`) | `assessments/<name>/<slug>/region.yaml` |
| 3 — Web search | Sonnet + Anthropic's `web_search_20250305` server tool | Enriched region YAML (overwritten in place) |
| 4 — Prompt assembly | `scripts/compose_prompt.py` | `assessments/<name>/<slug>/composed_prompt.md` |
| 5 — Scoring | Opus (the single Opus call) | `assessments/<name>/<slug>/scoring.json` |
| 6 — Report | `scripts/format_results.py` | stdout |

Every API call is its own `--step` key (e.g. `1a-extract`, `1a-consolidate`,
`1b-select`, `1b-synthesize`, `2a-template`, `2b-synthesize`) so you can
dry-run / inspect / pay for each one independently. See
`api_test_instructions.md` for the full list and `ARCHITECTURE.md` for the
cost breakdown.

## Example Run: SEA-HELM → Indonesian administrative chatbot

A complete end-to-end run is bundled in the repo (committed via `git add -f`,
since the pipeline's output directories are otherwise gitignored) so
collaborators can inspect every intermediate artifact without having to run
the pipeline themselves. The deployment under assessment is a hypothetical
Indonesian central-government chatbot answering citizen queries about KTP
applications, Coretax tax filing, OSS-RBA business registration, and
Imigrasi permits. Elicitation was driven by the `sea-b` persona.

### Suggested reading order

Each row below is a separate artifact from the same run. Read top-to-bottom
to follow the pipeline from deployment scenario through to final scoring:

| # | Path | What to look at |
|---|------|-----------------|
| 1 | `assessments/sea-helm/indonesia_bahasa_administrative_citizen/deployment_description.txt` | The deployment scenario the persona provided |
| 2 | `assessments/sea-helm/indonesia_bahasa_administrative_citizen/elicitation_questions.json` + `elicitation_answers.json` + `elicitation_summary.md` | Sonnet-generated elicitation Qs, persona-in-character answers, and the synthesized summary with dimension priority weights + flagged gaps |
| 3 | `papers/sea-helm.pdf` → `papers/sea-helm/paper_summary.md` | Source paper + Haiku/Sonnet consolidated summary (Step 1a output) |
| 4 | `benchmarks/sea-helm.yaml` | Synthesized benchmark YAML with per-dimension characterization and the verbatim quote registry (Step 1b output) |
| 5 | `assessments/sea-helm/indonesia_bahasa_administrative_citizen/region.yaml` | Regional context — regulatory environment (UU 27/2022 PDP Law, Coretax PMK 81/2024), population, NLP ecosystem, benchmark-validity assessment — enriched with URL-cited web-search findings (Steps 2 + 3) |
| 6 | `assessments/sea-helm/indonesia_bahasa_administrative_citizen/composed_prompt.md` | The exact ~80 KB prompt Opus receives — useful for seeing how the framework, benchmark docs, quote registry, regional context, and elicitation summary come together (Step 4 output) |
| 7 | `assessments/sea-helm/indonesia_bahasa_administrative_citizen/scoring.json` | **The main artifact.** Opus's final output: 6 dimension scores with checklist responses, paper-quote evidence, region-source URL citations, confidence, information gaps, and remediation suggestions (Step 5 output) |
| 8 | `assessments/sea-helm/indonesia_bahasa_administrative_citizen/traces/*.jsonl` | Raw LLM request/response bodies per pipeline step (one JSONL per step — `5_score.jsonl` is Opus, others are Haiku/Sonnet) |
| 9 | `assessments/sea-helm/indonesia_bahasa_administrative_citizen/cost_ledger.json` | Token counts and call counts per step per model for the full run |
| 10 | `page_caches/sea-helm/page_001.txt` … `page_029.txt` | Raw per-page Haiku extractions from Step 1a, before Sonnet consolidation (useful if you want to audit the PDF-ingest stage) |

### Generate the formatted report

To render `scoring.json` as a human-readable markdown summary:

```bash
python scripts/format_results.py assessments/sea-helm/indonesia_bahasa_administrative_citizen/scoring.json
```

This produces a dimension-score table, risk assessment, evidence highlights,
and remediation list.

### Note on this bundled run

This is a single reference run, force-committed as a sample. Future pipeline
runs remain gitignored by default (`assessments/`, `papers/<name>/`,
`benchmarks/<name>.yaml`, `page_caches/`, `results/`) so the repo doesn't
accumulate run artifacts. If you want to share another run, force-add its
paths explicitly.

## Personas

Six test personas are defined in `personas.py`. They pair one "reasonable fit" (A) persona with one "poor fit" (B) persona per target benchmark, so the pipeline's ability to discriminate deployment-context mismatches can be measured:

| ID | Benchmark | Deployment |
|----|-----------|------------|
| `helm-a` | HELM | US edtech, undergraduate essay feedback |
| `helm-b` | HELM | Kenyan public-health NGO, community health workers |
| `sea-a` | SEA-HELM | Indonesian ministry, public-service chatbot |
| `sea-b` | SEA-HELM | Malaysian legal aid, Rohingya refugee support |
| `iber-a` | IberBench | Barcelona media, Catalan content moderation |
| `iber-b` | IberBench | SEP Oaxaca, Zapotec-Spanish bilingual assessment |

## Scoring Rubric

Each dimension is scored 1–5:

| Score | Meaning |
|-------|---------|
| 1 | Major validity violations; fundamentally misaligned with target context |
| 2 | Significant concerns; multiple concrete violations or gaps |
| 3 | Partially addressed; mixed evidence |
| 4 | Well addressed; minor concerns; documentation shows awareness |
| 5 | No concerns; explicit validity-preserving practices demonstrated |

## Validity Dimensions

| Dimension | Category | What It Assesses |
|-----------|----------|------------------|
| Input Ontology | Input × Ontology | Test case categories cover regional deployment needs |
| Input Content | Input × Content | Datapoint instances are culturally appropriate |
| Input Form | Input × Form | Signal encoding matches regional infrastructure |
| Output Ontology | Output × Ontology | Label categories reflect regional values |
| Output Content | Output × Content | Ground-truth labels align with regional perspectives |
| Output Form | Output × Form | Output modality matches regional usage patterns |

## Manual Benchmark / Region YAMLs

The pipeline synthesizes both benchmark and region YAMLs automatically. If you want to evaluate with a hand-authored YAML instead, see `benchmarks/examples/*.yaml` and `regions/base/*.yaml` for reference shapes, then drop your file into `benchmarks/<name>.yaml` or `assessments/<name>/<slug>/region.yaml` and start the pipeline from a later step via `--step`.

## Why both `cli_package/` and `anthropic_api_package/`?

- **`cli_package/`** — runs via Claude Code with slash commands, subagents, and skills. Best for interactive terminal use with CC installed.
- **`anthropic_api_package/`** — a standalone Python CLI that calls the Anthropic API directly. Best for CI, web-app backends, headless servers, or any environment without CC.

Both produce equivalent outputs for the same inputs.
