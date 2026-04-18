You will consolidate per-page JSON extractions from a benchmark paper into a
final two-section markdown summary. The per-page extractions are attached in the
user message as N markdown-headed sections — one per page, each introduced by a
`### Page N extraction` heading and followed by the JSON object produced for
that page.

Parse each JSON object independently. If a page's block is malformed (missing
brace, stray fence, unescaped quote, etc.) **do not discard it** — fall back to
reading the block as prose and recover every visibly-complete quote and any
other category / continuity signals you can identify. Malformed structure does
not imply malformed content.

If a page's block is genuinely unrecoverable (empty, truncated to a fragment,
unintelligible), **omit that page entirely from the Quote Registry** and add a
line to the Metadata block like:

`- Pages with unrecoverable extractions: [14, 22]`

Do not create placeholder rows in the Registry — every Registry row must be a
real verbatim quote with a valid `Q<n>` ID, a page number, a category tag, and
quoted text. The count and ID continuity of the Registry are enforced by a
downstream mechanical check.

## Extraction categories

Each per-page quote carries one of eight category tags. The same eight categories
structure the Narrative Context section below:

1. **task_taxonomy** — test-case categories, task types, subtask breakdown.
2. **data_sources** — where datapoints come from (crowdsourced, scraped, expert-written, etc.).
3. **data_format** — input modality, encoding, preprocessing, length/shape constraints.
4. **label_categories** — output label set, ontology, ground-truth schema.
5. **annotation_process** — who annotated, their demographics, inter-annotator agreement, QA.
6. **evaluation_metrics** — scoring metrics, output modality, what counts as a correct answer.
7. **stated_limitations** — limitations or cultural/regional scope restrictions the authors themselves call out.
8. **authors_affiliations** — author names and institutional affiliations (signals deployment-context origin).

## Step 1 — Merge and deduplicate quotes

1. Collect all quotes from every per-page extraction.
2. Handle cross-page sentences: if `continues_from_previous` or `continues_to_next`
   is true, check adjacent pages for overlapping text and merge split sentences.
3. Deduplicate exact or near-exact duplicates (same text on overlapping page
   boundaries). Keep the most complete version.
4. Assign sequential IDs Q1, Q2, ..., QN in page order.
5. Preserve each quote's extraction `category` tag as-is.

## Step 2 — Write narrative context

For each of the 8 extraction categories, write 2-5 sentences of interpretive
context that references quote IDs, e.g.:

> "The benchmark covers 22 task categories [Q1] split between industry-relevant
> and fundamental tasks [Q2]."

When a category has no quotes, say so explicitly:

> "NOT DOCUMENTED: the paper is silent on annotator demographics. This absence is
> itself a validity-relevant finding."

For categories that plausibly span both input and output (`task_taxonomy`,
`data_sources`, `data_format`, `stated_limitations`), explicitly cover each side
where the paper supports it — don't let one side dominate the narrative for
that category.

## Step 3 — Verify coverage

For each category: count its quotes; if zero, add a "NOT DOCUMENTED" note.

## Step 4 — Verify narrative references

Every factual claim in the narrative must reference at least one quote ID. If a
claim has no backing quote, either find the quote or flag it as inference.

## Output format

Produce a single markdown document with this exact structure:

```markdown
# Validity Extraction: {Full Paper Title}
<!-- Model routing: Haiku (per-page extraction) → Sonnet (consolidation) -->

## Metadata
- **Title**: ...
- **Authors**: ...
- **Venue/Year**: ...
- **Total Pages**: ...
- **Quotes Extracted**: N
- **Pages with unrecoverable extractions**: [<page numbers>] (omit the line if none)

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim
references quote IDs from the registry below. **This section is non-authoritative
— it provides readability but is not evidence. Only the Quote Registry below
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

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | ... | ... | "..." |
| ... | ... | ... | ... |

### Category Index
- **task_taxonomy**: Q1, Q2, ...
- **data_sources**: ...
- **data_format**: ...
- **label_categories**: ...
- **annotation_process**: ... (or "NO QUOTES — paper is silent")
- **evaluation_metrics**: ...
- **stated_limitations**: ...
- **authors_affiliations**: ...
```

Output ONLY the markdown document, with no surrounding prose.
