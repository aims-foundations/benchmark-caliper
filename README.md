# Benchmark Caliper

A framework for assessing whether AI benchmarks developed in one cultural context can be validly applied to another. 

Benchmark Caliper evaluates a benchmark across **6 validity dimensions** (Input/Output × Ontology/Content/Form) and produces a scored, evidence-backed report for a specific deployment context.

## How it works

You provide a benchmark paper (PDF) and a description of where and how the benchmark would be deployed. Benchmark Caliper then:

1. Extracts the benchmark's metadata and methodology from the paper.
2. Asks a few targeted questions about your deployment context and synthesizes your answers.
3. Builds a structured profile of the benchmark and the target region.
4. Scores all 6 validity dimensions and produces a report with per-dimension scores, reasoning, and supporting evidence.

The analysis runs on the Anthropic API with cost-routed model selection — lighter models for extraction and synthesis, the strongest model for the final scoring step.

## Components

| Component | Description |
|-----------|-------------|
| [`anthropic_api_package_release/`](anthropic_api_package_release/) | The validity-analysis pipeline. Run it from the command line to inspect the assessments from the paper, reproduce one, or analyze your own benchmark. See its [README](anthropic_api_package_release/README.md). |
| [`website/`](website/) | A web interface to the pipeline: upload a paper, describe a deployment, and receive a validity report. See its [README](website/README.md). |

## Repository structure

```
benchmark-caliper/
├── anthropic_api_package_release/   # Validity-analysis pipeline
│   ├── run_pipeline.py              # CLI entry point and orchestrator
│   ├── run_expert_stage1.py         # Batch runner for expert assessments
│   ├── run_comparative.py           # Comparative (regional vs. reference) runs
│   ├── client.py                    # Anthropic API wrapper with cost routing
│   ├── framework.yaml               # Validity dimensions, checklists, scoring rubric
│   ├── prompt_template.md           # Evaluation prompt template
│   ├── prompts/                     # LLM prompt per pipeline step
│   ├── scripts/                     # Deterministic helpers (PDF, parsing, reports)
│   ├── benchmarks/                  # Benchmark example YAMLs (ICL references)
│   ├── regions/                     # Region template YAMLs (ICL references)
│   ├── templates/                   # Input templates for new assessments
│   ├── assessments/                 # Pipeline outputs for the paper's assessments
│   ├── papers/                      # Benchmark papers and extracted summaries
│   ├── tests/                       # Pipeline test suite
│   └── README.md                    # Pipeline setup and usage
├── website/                         # Web interface to the pipeline
│   ├── server/                      # FastAPI backend
│   ├── client/                      # Vite + React + TypeScript frontend
│   ├── DESIGN.md                    # Architecture and security posture
│   ├── DEPLOYMENT.md                # Hosted setup
│   └── README.md                    # Local setup and usage
├── Dockerfile                       # Builds the website + pipeline image
├── render.yaml                      # Render deployment blueprint
└── entrypoint.sh                    # Container entrypoint
```

## Getting started

- **To analyze a benchmark through the web interface:** see [`website/README.md`](website/README.md).
- **To run the pipeline from the command line** — inspect the assessments from the paper, reproduce one, or analyze your own benchmark — see [`anthropic_api_package_release/README.md`](anthropic_api_package_release/README.md).

## Deployment

The website (with the pipeline bundled) deploys as a single Docker service.
`Dockerfile` and `render.yaml` define the build; see
[`website/DEPLOYMENT.md`](website/DEPLOYMENT.md) for the hosted setup.

## Validity dimensions

| Dimension | Category | What it assesses |
|-----------|----------|------------------|
| Input Ontology | Input × Ontology | Test case categories cover regional deployment needs |
| Input Content | Input × Content | Datapoint instances are culturally appropriate |
| Input Form | Input × Form | Signal encoding matches regional infrastructure |
| Output Ontology | Output × Ontology | Label categories reflect regional values |
| Output Content | Output × Content | Ground-truth labels align with regional perspectives |
| Output Form | Output × Form | Output modality matches regional usage patterns |

Each dimension is scored 1–5:

| Score | Meaning |
|-------|---------|
| 1 | Major validity violations; fundamentally misaligned with target context |
| 2 | Significant concerns; multiple concrete violations or gaps |
| 3 | Partially addressed; mixed evidence |
| 4 | Well addressed; minor concerns; documentation shows awareness |
| 5 | No concerns; explicit validity-preserving practices demonstrated |

## Ground-truth validation

Three benchmark–region pairs from the paper were scored by domain experts and serve as ground truth for validating the framework's scores. Mean absolute error (MAE) is measured against the expert average:

| Benchmark | Region | Expert avg | MAE |
|-----------|--------|-----------|-----|
| HELM | Southeast Asia | 1.7 | 0.00 |
| SEA-HELM | Southeast Asia | 4.3 | 0.67 |
| IberBench | Iberian | 3.7 | 0.00 |
