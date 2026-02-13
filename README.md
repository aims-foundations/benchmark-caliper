# Validity Analyzer

A framework for assessing whether AI benchmarks developed in one cultural context can be validly applied to another. Based on the paper *"Validity Analysis when Porting Benchmarks Across Cultures and Regions"* (Corona, Truong, Trager, 2025).

The tool evaluates benchmarks across **6 validity dimensions** (Input/Output × Ontology/Content/Form) and produces scored reports, radar charts, and heatmap visualizations.

## Repository Structure

```
validity-analyzer/
├── framework.yaml          # Core validity framework: dimensions, checklists, scoring rubric, ground truth
├── prompt_template.md      # LLM prompt template for running evaluations
├── benchmarks/             # Benchmark description YAMLs (one per benchmark)
│   ├── helm.yaml
│   ├── seahelm.yaml
│   ├── afrimedqa.yaml
│   └── ...                 # 34 benchmarks total
├── regions/                # Regional context YAMLs (one per region)
│   ├── southeast_asia.yaml
│   ├── sub_saharan_africa.yaml
│   ├── east_asia.yaml
│   ├── mena.yaml
│   ├── iberian.yaml
│   ├── latin_america_indigenous.yaml
│   └── iran_persian.yaml
├── papers/                 # Source papers/data for reference
├── generate_report.py      # Generate markdown reports + radar charts from results
├── generate_heatmap.py     # Generate heatmap visualization across all results
├── validate.py             # Compare LLM scores against ground-truth expert scores
├── analysis.md             # Summary of all 32 evaluations and key findings
├── reproduce.sh            # One-command reproduction script
└── results/                # Output directory (generated, not checked in)
    ├── *.json              # Raw evaluation results
    ├── *_report.md         # Per-benchmark markdown reports
    ├── all_radar.png       # Combined radar chart
    ├── validity_heatmap.png/.pdf  # Heatmap visualization
    └── summary.csv         # Spreadsheet for human review
```

## Setup

```bash
pip install pyyaml numpy matplotlib
```

## Reproducing Existing Results

The evaluation pipeline has two stages: (1) LLM-based scoring, and (2) report generation.

### Quick Start

```bash
# Run the full pipeline (see reproduce.sh for details)
bash reproduce.sh
```

### Step-by-Step

**Stage 1: Run LLM evaluations.** Each evaluation feeds a benchmark YAML, a region YAML, and the framework into an LLM (Claude) using the prompt template. The LLM returns a structured JSON with scores for all 6 dimensions.

For a single benchmark-region pair:

1. Open `prompt_template.md` and fill in the template with content from:
   - The benchmark file (e.g., `benchmarks/helm.yaml`)
   - The target region file (e.g., `regions/southeast_asia.yaml`)
   - The framework (`framework.yaml`)
2. Provide the filled prompt to Claude (or another capable LLM).
3. Save the JSON output to `results/<benchmark>_<region>.json`.

The expected JSON format (see `results/helm_sea.json` for a complete example):

```json
{
  "benchmark": "helm",
  "region": "southeast_asia",
  "dimensions": {
    "input_ontology": {
      "score": 2,
      "justification": "...",
      "checklist_responses": { "IO-1": "...", "IO-2": "..." },
      "evidence_quotes": ["..."],
      "confidence": "high",
      "information_gaps": ["..."],
      "requires_expert_verification": ["..."]
    }
  },
  "overall_summary": "...",
  "risk_assessment": "high|medium|low",
  "remediation_suggestions": "...",
  "highest_concern_dimensions": ["input_content"],
  "strongest_dimensions": ["input_ontology"]
}
```

**Stage 2: Generate reports and visualizations.**

```bash
# Generate markdown reports and radar charts for all results
python generate_report.py

# Generate a single report
python generate_report.py --result helm_sea

# Compare specific benchmarks side-by-side
python generate_report.py --compare helm_sea seahelm_sea

# Generate the heatmap across all results
python generate_heatmap.py

# Validate LLM scores against ground-truth (3 case studies from the paper)
python validate.py

# Export a CSV for human review
python validate.py --csv
```

## Analyzing a New Benchmark

To evaluate a benchmark not yet in the repository:

### 1. Create a benchmark YAML

Create `benchmarks/<name>.yaml` following this structure (see existing files for examples):

```yaml
name: "MyBenchmark"
full_name: "Full Benchmark Name"
paper_url: "https://arxiv.org/abs/..."
year: 2024
domain: "General LLM evaluation"
porting_strategy: "translation"  # one of: ground_up, adapted, mixed, translation, parallel, regional_exams, none
languages: ["en", "fr", "sw"]
primary_region: "Sub-Saharan Africa"

description: |
  One-paragraph description of what the benchmark evaluates.

documentation_excerpts: |
  Paste relevant excerpts from the benchmark's paper, README, or datasheet.
  Include: data collection methodology, annotation process, task descriptions,
  language coverage, stated limitations. The more detail here, the better
  the LLM evaluation will be.
```

The `porting_strategy` field determines how the benchmark appears in the heatmap. Options:
- `ground_up` — Built from scratch for the target region
- `adapted` — Substantially modified for the target region
- `mixed` — Combination of original and new content
- `regional_exams` — Based on existing local exams
- `parallel` — Parallel construction in multiple languages
- `translation` — Translated from a source benchmark
- `none` — No porting (Western/Global North baseline)

### 2. Create a region YAML (if needed)

If your target region isn't already in `regions/`, create `regions/<name>.yaml`:

```yaml
name: "Region Name"
abbreviation: "RGN"

countries:
  - Country1
  - Country2

languages:
  major:
    - Language1
    - Language2

writing_systems:
  - Latin
  - Other Script

literacy_rates:
  Country1: 0.95
  Country2: 0.85

cultural_norms_notes: |
  Key cultural concepts and norms relevant to AI evaluation.

infrastructure_notes: |
  Internet penetration, device usage, data infrastructure.

domain_specific_notes: |
  Healthcare, legal, education system specifics.
```

### 3. Run the evaluation

Fill in `prompt_template.md` with your benchmark and region content, then provide it to Claude. Save the JSON output to `results/<benchmark>_<region>.json`.

### 4. Generate reports

```bash
python generate_report.py --result <benchmark>_<region>
python generate_heatmap.py  # regenerates heatmap with the new entry
```

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
|-----------|----------|-----------------|
| Input Ontology | Input × Ontology | Test case categories cover regional deployment needs |
| Input Content | Input × Content | Datapoint instances are culturally appropriate |
| Input Form | Input × Form | Signal encoding matches regional infrastructure |
| Output Ontology | Output × Ontology | Label categories reflect regional values |
| Output Content | Output × Content | Ground-truth labels align with regional perspectives |
| Output Form | Output × Form | Output modality matches regional usage patterns |

## Ground-Truth Validation

Three benchmark-region pairs from the paper serve as ground truth for validating LLM-based scores:

| Benchmark | Region | Expert Avg | LLM MAE |
|-----------|--------|-----------|---------|
| HELM | Southeast Asia | 1.7 | 0.00 |
| SEA-HELM | Southeast Asia | 4.3 | 0.67 |
| IberBench | Iberian | 3.7 | 0.00 |

Run `python validate.py` to reproduce this comparison.
