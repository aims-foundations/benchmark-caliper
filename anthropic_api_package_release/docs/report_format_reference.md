# Report Format Reference

## Overview

Each `report.md` is a three-tier markdown document produced by a two-step process:
1. **Step 7 (Scoring):** Opus reads a `composed_prompt.md` (assembled from all upstream pipeline stages) and outputs a structured `scoring.json` following the schema in `prompts/opus_scoring_framing.md`.
2. **Step 8 (Formatting):** `scripts/format_results.py` transforms the JSON into the final markdown report, pulling in sibling files (`deployment_description.txt`, `composed_prompt.md`, `dataset_analysis_report.md`) from the assessment directory.

The report evaluates a **specific benchmark** for a **specific deployment context** (target population, use case, region) across **6 validity dimensions**.

---

## Tier 1: Dashboard (Preamble + Summary)

### 1.1 Deployment Context
- **Source:** `deployment_description.txt` (from stage 1 elicitation)
- **Fields:**
  - **Use case:** Free text describing the deployment scenario, domain, and setting
  - **Target population:** Free text describing who will use the system — their qualifications, location, language, experience level

This orients the reader on *what* is being evaluated and *for whom* before any scores appear.

### 1.2 Benchmark Identity Header
- `# Validity Analysis: {benchmark_name}` (H1)
- **Target context:** A short label naming the specific deployment persona/scenario (e.g., "North Indian Hindi-Medium Postgraduate Teacher — MCQ Evaluation Deployment")
- **Overall risk:** `HIGH`, `MEDIUM`, or `LOW` — a holistic risk assessment of using this benchmark for this deployment

### 1.3 Dimension Scores Table
A 6-row table plus average:

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|

- **Dimension:** One of the 6 validity dimensions, with flag symbols:
  - `⚠` = highest concern dimension(s)
  - `✓` = strongest dimension(s)
  - No flag = neutral
- **Score:** Integer 1–5
- **Rating:** Text label mapped from score:
  - 1 = "Serious concern"
  - 2 = "Significant gaps"
  - 3 = "Moderate gaps"
  - 4 = "Minor gaps"
  - 5 = "Strong alignment"
- **Confidence:** `high`, `medium`, or `low` — calibrated by how many evidence streams support the finding (high = 2+ streams; medium = 1 stream or indirect; low = mostly inference)
- **Average:** Arithmetic mean of the 6 scores, displayed as final row

A legend below explains the flag symbols.

### 1.4 Dimension Key Table
Static reference table mapping abbreviations (IO, IC, IF, OO, OC, OF) to full names and one-sentence definitions:

| Abbr. | Dimension | Definition |
|:-----:|-----------|------------|
| IO | Input Ontology | Whether the benchmark's test case categories cover the query types expected in deployment. |
| IC | Input Content | Whether individual datapoint content is culturally and contextually appropriate for the target region. |
| IF | Input Form | Whether the input signal encoding (text, audio, image parameters) matches deployment conditions. |
| OO | Output Ontology | Whether the benchmark's output categories and scoring criteria reflect regionally valid decision boundaries. |
| OC | Output Content | Whether ground-truth labels align with the judgments of regional stakeholders. |
| OF | Output Form | Whether the expected output modality matches regional deployment needs and accessibility. |

### 1.5 Overall Summary
A single free-text paragraph (typically 150–250 words) that:
- Identifies the benchmark's strongest alignment with the deployment
- Names the highest-concern dimensions and their key gaps
- Synthesizes across all 6 dimensions into a coherent narrative
- Links validity concerns to specific deployment constraints
- References evidence (quote IDs, dataset citation IDs) where relevant

### 1.6 Practical Guidance
Three subsections that translate abstract scores into actionable advice:

- **What This Benchmark Measures:** What constructs/abilities the benchmark *can* evaluate for the target context, referencing strongest dimensions. Tells the user what signal they'd actually get.
- **Construct Depth:** How deeply the benchmark probes those constructs — what level of evidence it provides vs. what remains unaddressed. Tells the user how much to trust a score on this benchmark.
- **What Else You Need:** Specific supplementary evaluations, datasets, or expert reviews needed for a complete assessment. Each recommendation is tied to specific dimension-level gaps. Numbered and actionable.

---

## Tier 2: Dimension Details

Six sections, one per dimension, in fixed order: IO → IC → IF → OO → OC → OF. Each section contains:

### 2.1 Section Header
`### {Dimension Label} — {score}/5 ({rating})`

Example: `### Input Content — 2/5 (Significant gaps)`

### 2.2 Confidence
`**Confidence:** {high|medium|low}`

### 2.3 Justification
1–3 paragraph narrative explaining *why* this score was assigned. Key requirements:
- Must reference specific evidence (quote IDs like `[Q22]`, web source IDs like `[WEB-12]`, dataset citation IDs like `[DATASET-D35]`)
- Hedging must be consistent — if a claim is hedged ("may be", "suggests") it stays hedged throughout
- Must explain both what works and what doesn't
- Links findings to the specific deployment context, not abstract validity

### 2.4 Strengths
Bulleted list of what the benchmark captures **well** for this dimension/deployment. Each strength is grounded in at least one evidence source. Required even for low-scoring dimensions — partial coverage is still useful signal.

Example:
```
- Strict 4-option single-answer MCQ taxonomy matches deployment's binary scoring requirement [Q22, Q33].
- Explicit inclusion of Arts & Humanities covers civics/literature areas core to North Indian board syllabi [Q42].
```

### 2.5 Checklist
The core analytical content. Each dimension has **4–6 checklist items** with standardized IDs (IO-1 through IO-4, IC-1 through IC-5, etc.). These items come from the region YAML (generated per-deployment by the pipeline) and represent specific validity questions to assess.

Format:
```
- **{ID}**: {substantive response} — _Sources: {comma-separated evidence IDs}_
```

Key rules:
- Every item must be answered — no skipping
- Every substantive response must cite at least one evidence source (quote, web source, or dataset citation)
- If evidence is insufficient: `INSUFFICIENT DOCUMENTATION — {description of what would resolve it}`
- The `evidence_map` in the JSON explicitly links each checklist item ID to its supporting evidence entries

The checklist items for each dimension are:

**Input Ontology (IO-1 through IO-4):**
- IO-1: Identify test case categories required for regional deployment
- IO-2: Check if taxonomy omits regionally relevant categories
- IO-3: Check if taxonomy includes irrelevant categories
- IO-4: Document category gaps harming content validity

**Input Content (IC-1 through IC-5):**
- IC-1: Do inputs require region-specific cultural/geographic/dialectal knowledge?
- IC-2: Does culturally sensitive content align with target culture?
- IC-3: Flag inputs assuming Western-specific knowledge
- IC-4: Regional annotator recruitment for culturally sensitive instances
- IC-5: Document content issues harming content validity

**Input Form (IF-1 through IF-4):**
- IF-1: Compare signal distributions between source and target
- IF-2: Check if regional infrastructure supports data capture specs
- IF-3: Identify domain-specific form differences
- IF-4: Document form mismatches harming external validity

**Output Ontology (OO-1 through OO-5):**
- OO-1: Review output label categories for regional relevance
- OO-2: Identify missing regionally specific categories
- OO-3: Flag categories encoding non-regional values
- OO-4: Consider stakeholder-driven taxonomy redesign
- OO-5: Document taxonomy issues harming structural/content validity

**Output Content (OC-1 through OC-6):**
- OC-1: Do ground-truth labels reflect regional stakeholder perspectives?
- OC-2: Assess potential annotator–regional population disagreement
- OC-3: Review annotator demographics from documentation
- OC-4: Consider label re-annotation by regional annotators
- OC-5: Review aggregation methods for minority perspective erasure
- OC-6: Document label issues harming convergent/external validity

**Output Form (OF-1 through OF-4):**
- OF-1: Does output modality match regional deployment needs?
- OF-2: Assess text-to-speech availability for speech output
- OF-3: Consider literacy rates and accessibility requirements
- OF-4: Document form mismatches harming external validity

### 2.6 Evidence Cited (Collapsed)
A `<details>/<summary>` block containing all evidence used for this dimension, organized into three subsections:

- **Paper quotes:** Verbatim extracts from the benchmark paper, formatted as `[QN] 'quoted text' (p.X)`. These come from the Verbatim Quote Registry — only actual paper text, not interpretive summaries.
- **Web sources:** Regional/deployment context findings from web search, formatted as `[WEB-N] brief factual claim`. Each maps to a URL in the Web Source Registry.
- **Dataset analysis:** Empirical observations from sampled benchmark data on HuggingFace, formatted as `DATASET-DN: description of observation`. These come from the Dataset Analysis module which inspected actual datapoints.

Any of the three may be absent (empty list in JSON). At least one stream should be populated for scores of 4 or 5.

### 2.7 Information Gaps
Bulleted list of things the scorer **could not assess** due to missing documentation, gated data, or absent metadata. Each gap describes what would be needed to resolve it.

Example:
```
- Hindi-specific translation proportion in test split unknown; requires gated-access verification.
- No published mapping between MILU subjects and UP/MP/Rajasthan/Bihar board syllabus chapters.
```

### 2.8 Requires Expert Verification
Bulleted list of claims that need a **domain or regional expert** to confirm before the score can be fully trusted.

Example:
```
- Hindi-medium board teacher review of a sample of translated items for register fidelity.
- Subject-expert audit of truncated items and items where English vocabulary is tested inside Hindi Language Studies.
```

Each dimension section ends with a horizontal rule (`---`).

---

## Tier 3: Remediation Suggestions

4–6 items, sorted so highest-concern dimensions (flagged `⚠`) appear first. Each item:

### 3.1 Heading
`### {Dimension Label}{⚠ flag if highest concern}`

### 3.2 Gap
`**Gap:** {description}` — What is missing or problematic, referencing specific findings from Tier 2.

### 3.3 Recommendation
`**Recommendation:** {concrete action}` — Actionable remedy. Specific enough to execute (e.g., "Filter MILU Hindi items by `is_translated` flag and prefer natively sourced items" rather than "improve data quality").

---

## Appendix: Evidence Registries

Three optional subsections pulled from `composed_prompt.md` and sibling files:

### A.1 Verbatim Quote Registry
Full table of all paper quotes cited anywhere in the report:

| ID | Page | Dimension | Text |
|----|------|-----------|------|

Typically 80–130+ entries. Each `[QN]` used in Tier 2 traces back to a row here with its page number and verbatim text.

### A.2 Web Source Registry
URL mapping for all `[WEB-N]` citations:

| ID | URL |
|----|-----|

Typically 15–25 entries. Full URLs enabling readers to verify claims.

### A.3 Dataset Analysis
The complete `dataset_analysis_report.md` — the empirical analysis of sampled benchmark data from HuggingFace. This is a substantial sub-document with its own structure:

- **Header:** Dataset name, analysis date, examples reviewed, columns shown/skipped
- **Datapoint Citations Registry:** Table of all `[DN]` citations with verbatim excerpts in the data's own language plus English interpretations

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|

- **Deployment-Relevant Strengths:** Findings with citations, each tagged by dimension
- **Potential Concerns:** Organized by severity (CRITICAL / MAJOR / MINOR), each with citations
- **Content Coverage Summary:** Brief characterization of what the data contains
- **Limitations:** What the sample cannot tell you

---

## Three Evidence Streams — How They Interact

The report draws on three independent evidence streams, each with its own citation namespace:

1. **Paper quotes (`[QN]`):** Verbatim extracts from the benchmark's academic paper. These document what the authors *claim* about the benchmark. ~80–130 quotes extracted by the pipeline.

2. **Web sources (`[WEB-N]`):** Findings from web search research about the deployment region and benchmark. These provide regional context (literacy rates, infrastructure, legal frameworks, etc.) that the paper doesn't cover. ~15–25 sources.

3. **Dataset analysis (`DATASET-DN` or `{dataset_name}-DN`):** Empirical observations from sampling and inspecting actual benchmark data on HuggingFace. These reveal what the data *actually contains* vs. what the paper claims. ~30–50 citations.

The scoring prompt instructs Opus that **empirical evidence (dataset analysis) is more authoritative than documentation** when they conflict. This is how findings like "paper claims 25% translation rate but 100% of sampled items are translated" emerge.

**Evidence map:** The `scoring.json` contains an `evidence_map` per dimension that explicitly links each checklist item ID to its supporting evidence entries. This creates a fully traceable chain: checklist response → evidence IDs → registry entries → original source.

**Confidence calibration** is tied to evidence stream coverage:
- `high` = supported by 2+ evidence streams
- `medium` = supported by 1 stream, or indirect evidence
- `low` = mostly inference, no direct evidence

---

## Key Design Properties

1. **Deployment-conditioned, not abstract.** Every assessment is relative to a specific use case/population. A score of 2 on Input Content doesn't mean "bad data" — it means "significant gaps *for this specific deployment*."

2. **Balanced by design.** The scoring prompt requires strengths for every dimension (even low-scoring ones) and evidence grounding for both strengths and concerns. Scores can go up or down when re-run with better prompts.

3. **Traceable evidence chain.** Every claim traces back to a verifiable source: paper quote, URL, or specific datapoint excerpt in the data's own language. The evidence registries make this auditable.

4. **Explicit uncertainty.** `INSUFFICIENT DOCUMENTATION` markers, `information_gaps`, `requires_expert_verification`, and confidence levels all flag where the automated assessment reaches its limits and human judgment is needed.

5. **Actionable remediation.** Each remediation item pairs a specific gap with a concrete recommendation, sorted by priority.

6. **Fixed dimension framework.** The 6 dimensions and their checklist items provide a consistent structure across all assessments, enabling cross-benchmark comparison while allowing deployment-specific content within each item.
