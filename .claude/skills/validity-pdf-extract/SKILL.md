---
name: validity-pdf-extract
description: Extract verbatim quotes and narrative context from a benchmark paper PDF for validity analysis. Uses per-page Haiku extraction for cost efficiency, with Sonnet consolidation. Produces a two-section output separating an indexed quote registry (authoritative) from interpretive narrative context (convenience). Use instead of pdf-summary when running the validity analysis pipeline.
---

# Validity PDF Extract Skill (Optimized)

## Purpose

Extracts validity-relevant information from a benchmark paper PDF, with strict
separation between **verbatim quotes** (authoritative evidence) and **interpretive
context** (convenience narrative).

**Cost optimization**: This skill uses a tiered model approach:
- **Haiku subagents**: Per-page quote extraction (cheap, parallel, small context)
- **Sonnet** (this skill's model): Consolidation, narrative writing, quality control

This replaces the previous all-Opus approach, reducing cost by ~80% for extraction.

## Invocation

```
/validity-pdf-extract <local-pdf-path> <elicitation-summary-path>
```

The second argument is the path to the elicitation summary produced by the pipeline's
Step 2 (e.g., `papers/<benchmark_name>_elicitation_summary.md`). This summary contains
**dimension priority weights** and **cultural topic priorities** that guide extraction
depth.

### Elicitation-guided extraction

The elicitation summary's dimension priorities shape how the skill allocates
narrative depth during consolidation:

- **HIGH-priority dimensions**: Write 4-6 sentences of narrative context, include all
  relevant quotes, and note even minor related claims.
- **MODERATE-priority dimensions**: Write 2-4 sentences of narrative context.
- **LOWER-priority dimensions**: Write 1-2 sentences, covering only key findings.

**Cultural topic priorities** from the elicitation summary further focus the narrative:
when the user has flagged specific topics (e.g., lifecycle events, regional cuisines,
sub-national variation), the narrative should call out quotes and claims related to
those topics even if they would otherwise be treated as minor details.

**Important**: Priority guidance affects narrative depth only. Quote extraction from
the PDF is always exhaustive — every relevant quote is captured regardless of
priority level. This ensures the full evidence base is available for downstream
steps, even if the narrative emphasizes what the user cares about most.

## Extraction Categories

For each category, extract ALL available detail. If the paper is SILENT on a topic,
explicitly note its absence — missing documentation is itself a finding.

1. **Task taxonomy / test case categories**: What tasks does the benchmark include?
   How are they organized? Any stated coverage gaps? Task counts per category.
2. **Data sources and collection**: Where does the data come from? How was it
   collected? What languages/regions are represented? Sample counts per language.
3. **Data format and preprocessing**: Input modalities, encoding, normalization
   pipelines, script/writing system handling.
4. **Label categories and output types**: What output taxonomies are used? How were
   label sets designed? Any justification for regional relevance of categories?
5. **Annotation process**: Who annotated? Demographics of annotators. Recruitment
   criteria. Inter-annotator agreement statistics. How were disagreements resolved?
6. **Evaluation metrics and output modality**: What metrics are used? What form do
   model outputs take? Any noted limitations of the metrics?
7. **Stated limitations**: The authors' own acknowledged gaps, biases, or concerns.
8. **Authors and affiliations**: Who built this and where are they based?

Skip: related work surveys, detailed experimental results/rankings, model
architecture comparisons (unless they reveal something about benchmark design).

## Execution Steps

### Phase 1: Determine Page Count

```bash
# Try pdftk first, fall back to other methods
TOTAL_PAGES=$(pdftk "$PDF_PATH" dump_data 2>/dev/null | grep NumberOfPages | awk '{print $2}')
echo "PDF has $TOTAL_PAGES pages"
```

If pdftk is unavailable, use the Read tool on the PDF with `pages: "1"` and note
the total from the PDF metadata, or use `scripts/split_pdf.sh` which handles
multiple fallbacks.

If the PDF is small (<=12 pages), you may skip the per-page subagent approach
and extract directly in a single pass using Phase 3 (Consolidation) only.

### Phase 2: Per-Page Haiku Extraction

This is the core cost optimization. Instead of feeding large chunks to an expensive
model, we deploy **Haiku subagents** that each process a single page.

#### Subagent Deployment Strategy

Deploy Haiku subagents in parallel batches. Each subagent receives:
- ONE page of the PDF
- The 8 extraction categories (listed above)
- Instructions to output structured JSON

**Launch subagents using the Agent tool with `model: haiku`.**

For each page (or batch of 2-3 pages for very short pages), spawn a Haiku subagent
with this prompt template:

```
You are extracting validity-relevant quotes from page {PAGE_NUM} of a benchmark paper.

Read the PDF at "{PDF_PATH}" using the Read tool with pages: "{PAGE_NUM}".

Extract ALL factual claims relevant to these categories:
1. Task taxonomy / test case categories
2. Data sources and collection
3. Data format and preprocessing
4. Label categories and output types
5. Annotation process (annotators, demographics, agreement)
6. Evaluation metrics and output modality
7. Stated limitations
8. Authors and affiliations

For each relevant claim, output a JSON object:
{
  "quotes": [
    {
      "text": "<EXACT verbatim text from the PDF - complete sentences>",
      "page": {PAGE_NUM},
      "category": "<one of: task_taxonomy, data_sources, data_format, label_categories, annotation_process, evaluation_metrics, stated_limitations, authors_affiliations>"
    }
  ],
  "page_summary": "<1-2 sentence summary of what this page covers>",
  "continues_from_previous": <true/false>,
  "continues_to_next": <true/false>
}

Rules:
- Quote COMPLETE sentences only (never truncate mid-sentence)
- If a sentence spans from the previous page, include the full sentence visible on this page
- If a claim spans multiple sentences, quote all of them together
- Include statistical facts, methodological claims, design decisions, and limitations
- Skip: related work citations, model performance tables, figure captions (unless they contain methodological claims)
- If this page has no relevant content (e.g., references, full-page figures), return {"quotes": [], "page_summary": "...", "continues_from_previous": false, "continues_to_next": false}

Output ONLY the JSON object, nothing else.
```

**Parallelization**: Launch up to 5-8 subagents concurrently to maximize throughput.
Wait for each batch to complete before launching the next. Collect all outputs.

**Error handling**: If a subagent fails on a page (oversized figure, unreadable),
log the page number and continue. Do not retry more than once.

#### Writing Raw Extractions

After all subagents complete, write the collected per-page results to a temporary
file for the consolidation pass:

```
papers/<benchmark_name>_raw_extractions.json
```

This file is intermediate and can be deleted after consolidation.

### Phase 3: Consolidation (Sonnet — this model)

This phase runs in the current Sonnet context. It takes the raw per-page extractions
and the elicitation summary, and produces the final two-section output.

**Before starting consolidation**, read the elicitation summary and note:
1. The **dimension priority weights** (HIGH/MODERATE/LOWER for each of IO/IC/IF/OO/OC/OF)
2. The **cultural topic priorities** (ranked list of 3-5 topics)
3. The **flagged gaps** (areas where evidence is thin)

Use these priorities throughout Steps 3.2 and 3.3 below.

#### Step 3.1: Merge and Deduplicate Quotes

1. Collect all quotes from the per-page extractions
2. **Handle cross-page sentences**: If `continues_from_previous` or `continues_to_next`
   is true, check adjacent pages for overlapping text. Merge split sentences.
3. **Deduplicate**: Remove exact or near-exact duplicates (same text from overlapping
   page boundaries). Keep the version with the most complete text.
4. **Assign sequential IDs**: Number all quotes Q1, Q2, ..., QN in page order.
5. **Tag dimensions**: Map each category tag to the appropriate validity dimension:
   - task_taxonomy → input_ontology
   - data_sources → input_content
   - data_format → input_form
   - label_categories → output_ontology
   - annotation_process → output_content
   - evaluation_metrics → output_form
   - stated_limitations → general (or most relevant dimension)
   - authors_affiliations → general

#### Step 3.2: Write Narrative Context

For each of the 8 extraction categories, write interpretive context that
references quote IDs. **Adjust depth based on elicitation dimension priorities:**

- **HIGH-priority dimensions** (from elicitation): 4-6 sentences. Include all relevant
  quotes, note minor related claims, and call out any quotes touching the user's
  cultural topic priorities.
- **MODERATE-priority dimensions**: 2-4 sentences (default depth).
- **LOWER-priority dimensions**: 1-2 sentences, key findings only.

Map extraction categories to validity dimensions for priority lookup:
- task_taxonomy → Input Ontology (IO)
- data_sources → Input Content (IC)
- data_format → Input Form (IF)
- label_categories → Output Ontology (OO)
- annotation_process → Output Content (OC)
- evaluation_metrics → Output Form (OF)
- stated_limitations, authors_affiliations → use MODERATE depth

Example for a HIGH-priority dimension:
- "The benchmark covers 22 task categories [Q1] with a split between
  industry-relevant and fundamental tasks [Q2]. Regional cuisines, flagged as a
  cultural topic priority by the user, appear in the food-related QA subset [Q8]
  but coverage is limited to national-level dishes [Q9]."

When quotes indicate something is NOT DOCUMENTED, say so explicitly:
- "NOT DOCUMENTED: The paper provides no annotator demographic information.
  This absence is itself a validity-relevant finding."

#### Step 3.3: Verify Coverage

For each extraction category:
- Count quotes tagged to it
- If zero quotes, add: "NOT DOCUMENTED: The paper is silent on [category]."

#### Step 3.4: Verify Narrative References

Every factual claim in narrative sections must reference at least one quote ID.
If a claim has no backing quote, either find the quote or flag as inference.

### Phase 4: Write Output

Save to `papers/<benchmark_name>_paper_summary.md`:

```markdown
# Validity Extraction: {Full Paper Title}
<!-- Generated by validity-pdf-extract (optimized) | Source: {pdf_path} | Pages: {total} -->
<!-- Model routing: Haiku (per-page extraction) → Sonnet (consolidation) -->

## Metadata
- **Title**: {title}
- **Authors**: {authors}
- **Venue/Year**: {venue} {year}
- **Total Pages**: {total_pages}
- **Quotes Extracted**: {N}

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim
references quote IDs from the registry below. **This section is non-authoritative
— it provides readability but is not evidence. Only the Quote Registry below
contains verbatim text from the paper.**

### 1. Task Taxonomy / Test Case Categories
{Prose with [Q1], [Q3] references...}

### 2. Data Sources and Collection
{Prose with [Q5], [Q6] references...}

### 3. Data Format and Preprocessing
{Prose with references...}

### 4. Label Categories and Output Types
{Prose with references...}

### 5. Annotation Process
{Prose with references... or "NOT DOCUMENTED: ..."}

### 6. Evaluation Metrics and Output Modality
{Prose with references...}

### 7. Stated Limitations
{Prose with references...}

### 8. Authors and Affiliations
{Prose with references...}

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.
Downstream pipeline steps must propagate these quotes exactly as written.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 20 | task_taxonomy | "IberBench integrates 101 datasets..." |
| Q2 | 10 | task_taxonomy | "IberBench includes 70 datasets..." |
| ... | ... | ... | ... |
| QN | ... | ... | "..." |

### Category Index
- **task_taxonomy**: Q1, Q2, ...
- **data_sources**: Q3, Q4, ...
- **data_format**: ...
- **label_categories**: ...
- **annotation_process**: ... (or "NO QUOTES — paper is silent")
- **evaluation_metrics**: ...
- **stated_limitations**: ...
- **authors_affiliations**: ...
```

### Phase 5: Cleanup

Delete the intermediate raw extractions file:
```bash
rm -f papers/<benchmark_name>_raw_extractions.json
```

## Exhaustive Coverage Requirement

Every page of the PDF must be processed by a Haiku subagent. Do not skip pages.

### Handling Failures

| Error | Response |
|-------|----------|
| PDF path doesn't exist | Alert user: "PDF not found at {path}" |
| Haiku subagent fails on a page | Log page number, retry once, then skip with note |
| Page has no extractable text | Log "page N: no extractable text (likely figure)" |
| pdftk not available | Use Read tool with pages parameter directly |

### Reporting Skipped Pages

If any pages were skipped, add to the output:

```markdown
## _Processing Notes
- **Pages processed**: 1-24, 26-27, 29-42
- **Pages skipped**: 25 (full-page figure), 28 (failed extraction)
```

## Key Differences from Previous Version

| Aspect | Previous (all-Opus) | Optimized (Haiku+Sonnet) |
|--------|---------------------|--------------------------|
| **Extraction model** | Opus | Haiku (per-page) |
| **Consolidation model** | Opus | Sonnet |
| **Context per extraction call** | 8-12 pages | 1 page |
| **Estimated cost reduction** | Baseline | ~80% cheaper |
| **Parallelism** | Sequential chunks | Parallel pages |
| **Quote quality control** | Single pass | Two-tier (extract → verify) |
