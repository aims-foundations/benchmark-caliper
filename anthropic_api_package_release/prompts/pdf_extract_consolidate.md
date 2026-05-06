You will write the Metadata and Narrative Context sections for a benchmark paper
extraction. A pre-assembled Quote Registry (with sequential Q IDs, page numbers,
categories, and verbatim text) is provided as input — do NOT regenerate it.

Your job is to read the registry and write interpretive narrative that references
quote IDs, making the extraction human-readable.

## Purpose: validity assessment

This extraction feeds a downstream validity assessment. The goal is to determine
whether an AI benchmark appropriately measures what matters for a specific
deployment context — considering cultural, linguistic, and regional factors.

Validity is evaluated across six dimensions organized as a 2x3 grid of
(Input / Output) x (Ontology / Content / Form):

| Code | Dimension | What it captures |
|------|-----------|-----------------|
| IO | Input Ontology | Do the benchmark's test-case categories cover what the deployment needs? |
| IC | Input Content | Do the actual datapoints reflect the target population's language, culture, domain? |
| IF | Input Form | Does the signal encoding (text vs. audio, resolution, script) match deployment conditions? |
| OO | Output Ontology | Do the output labels and scoring rules reflect regional values and decision boundaries? |
| OC | Output Content | Do ground-truth labels agree with what regional stakeholders would judge correct? |
| OF | Output Form | Does the output modality match what the deployment actually produces? |

The eight extraction categories below were chosen because they supply evidence
for these dimensions. When writing narrative, highlight information that bears on
validity — both where the benchmark's design aligns with potential
deployment contexts and where it may diverge from them.

## Extraction categories

The registry uses eight category tags. Write one narrative subsection per category:

1. **task_taxonomy** — test-case categories, task types, subtask breakdown.
2. **data_sources** — where datapoints come from (crowdsourced, scraped, expert-written, etc.).
3. **data_format** — input modality, encoding, preprocessing, length/shape constraints.
4. **label_categories** — output label set, ontology, ground-truth schema.
5. **annotation_process** — who annotated, their demographics, inter-annotator agreement, QA.
6. **evaluation_metrics** — scoring metrics, output modality, what counts as a correct answer.
7. **stated_limitations** — limitations or cultural/regional scope restrictions the authors themselves call out.
8. **authors_affiliations** — author names and institutional affiliations (signals deployment-context origin).

## Writing the narrative

For each of the 8 categories, write 2-5 sentences of interpretive context that
references quote IDs, e.g.:

> "The benchmark covers 22 task categories [Q1] split between industry-relevant
> and fundamental tasks [Q2]."

When a category has no quotes in the registry, say so explicitly:

> "NOT DOCUMENTED: the paper is silent on annotator demographics. This absence is
> itself a validity-relevant finding."

For categories that plausibly span both input and output (`task_taxonomy`,
`data_sources`, `data_format`, `stated_limitations`), explicitly cover each side
where the paper supports it — don't let one side dominate the narrative.

Every factual claim must reference at least one quote ID from the registry.
If a claim has no backing quote, either find the quote or flag it as inference.

## Elicitation summary (deployment context)

An **Elicitation Summary** may be provided alongside the registry. This summary
captures the specific deployment scenario under which the benchmark will be
evaluated — who will use the system, in what domain, and what matters most for
validity in that context. It includes **Dimension Priority Weights** (HIGH,
MODERATE, LOWER) that reflect which validity dimensions are most important for
this deployment.

Use these priorities to calibrate narrative depth:
- **HIGH-priority dimensions**: 4-6 sentences — expand on nuances, note
  where the paper's design aligns with or diverges from what the deployment
  requires
- **MODERATE-priority dimensions**: 2-4 sentences
- **LOWER-priority dimensions**: 1-2 sentences

Cultural or domain-specific topics flagged in the summary deserve extra attention
— call out related quotes even if they would otherwise be treated as minor details.

Priority guidance affects **narrative depth only**. Every quote in the registry
must still be referenced regardless of priority level. Do not drop or skip quotes
from low-priority categories.

If no elicitation summary is provided, write all categories at uniform depth
(2-5 sentences each).

## Output format

Produce ONLY the following markdown sections — no surrounding prose, no registry:

```markdown
# Validity Extraction: {Full Paper Title}
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: ...
- **Authors**: ...
- **Venue/Year**: ...
- **Total Pages**: {from the registry page numbers}
- **Quotes Extracted**: {count of quotes in the registry}

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim
references quote IDs from the registry. **This section is non-authoritative
— it provides readability but is not evidence. Only the Quote Registry
contains verbatim text from the paper.**

### 1. Task Taxonomy / Test Case Categories
...

### 2. Data Sources and Collection
...

### 3. Data Format and Preprocessing
...

### 4. Label Categories and Output Types
...

### 5. Annotation Process
...

### 6. Evaluation Metrics and Output Modality
...

### 7. Stated Limitations
...

### 8. Authors and Affiliations
...
```

Output ONLY the markdown above. The Quote Registry will be appended mechanically.
