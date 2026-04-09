# Two-Prompt Version: Step 1 — Extract Quotes and Structure

Upload your benchmark paper PDF alongside this prompt. This step extracts all
validity-relevant information. You will use the output in Step 2 for scoring.

---

## Prompt (copy everything below this line)

I need you to extract validity-relevant information from the uploaded benchmark paper PDF. This extraction will be used in a follow-up step for regional validity scoring.

### Extraction Categories

Read the **entire paper** carefully. For each category below, extract ALL relevant **verbatim quotes** (exact text, complete sentences, with page numbers). If the paper is SILENT on a category, explicitly note: "NOT DOCUMENTED — paper is silent on [topic]. This absence is a validity-relevant finding."

1. **Task taxonomy / test case categories**: What tasks does the benchmark include? How are they organized? Stated coverage gaps? Task counts per category.
2. **Data sources and collection**: Where does the data come from? How was it collected? Languages/regions represented? Sample counts per language. Data provenance per subset.
3. **Data format and preprocessing**: Input modalities, encoding, normalization pipelines, script/writing system handling.
4. **Label categories and output types**: What output taxonomies are used? How were label sets designed? Justification for regional relevance of categories?
5. **Annotation process**: Who annotated? Demographics of annotators. Recruitment criteria. Inter-annotator agreement statistics. How were disagreements resolved? Were minority perspectives preserved?
6. **Evaluation metrics and output modality**: What metrics? What form do outputs take? Noted metric limitations?
7. **Stated limitations**: Authors' acknowledged gaps, biases, concerns.
8. **Authors and affiliations**: Who built this and where are they based?

**Skip**: Related work surveys, detailed model performance tables, architecture comparisons (unless they reveal benchmark design choices).

### Quote Rules

- Quote **complete sentences** — never truncate mid-sentence with "..."
- If a claim spans multiple sentences, quote all of them
- Include: methodological claims, statistical facts, design decisions, limitations
- Assign each quote an ID (Q1, Q2, ..., QN) and note the page number

### Required Output Format

Produce two sections:

#### Section 1: Narrative Context

For each of the 8 categories, write 2-5 sentences of interpretive summary referencing quote IDs. Example:
> "The benchmark covers 22 task categories [Q1] with a split between industry-relevant and fundamental tasks [Q2]. Coverage is sparse for some language-task pairs [Q5]."

**This section is interpretive — NOT evidence.** It aids readability but the quotes are the authority.

#### Section 2: Quote Registry

A table of ALL extracted quotes:

| ID | Page | Category | Verbatim Quote |
|----|------|----------|----------------|
| Q1 | 1 | task_taxonomy | "Exact quote from paper..." |
| Q2 | 3 | data_sources | "Exact quote from paper..." |
| ... | ... | ... | ... |

**This section is authoritative.** Every entry must be verbatim text from the paper.

After the table, provide a category index:
- **task_taxonomy**: Q1, Q3, Q7, ...
- **data_sources**: Q2, Q4, ...
- **annotation_process**: Q10, Q11, ... (or "NO QUOTES — paper is silent")
- (etc.)

#### Section 3: Benchmark Metadata

```
Name: [benchmark name]
Full Name: [full title]
Year: [publication year]
Domain: [what it evaluates]
Languages: [list of language codes]
Porting Strategy: [ground_up | adapted | mixed | translation | parallel | regional_exams | none]
```

### Important

- **Every page must be read.** Do not skip sections.
- **Missing documentation is a finding.** If annotation demographics, IAA stats, or label validation procedures are absent, say so explicitly.
- **Preserve the two-section structure.** The narrative and quote registry must remain separate. Do not embed quotes inline in the narrative — reference them by ID only.
