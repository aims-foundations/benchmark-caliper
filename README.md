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
