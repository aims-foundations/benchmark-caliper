# Single-Prompt Validity Analysis

Upload your benchmark paper PDF alongside this prompt.

Replace {REGION} with your target region (e.g., "Iberian Peninsula and Ibero-America",
"Southeast Asia", "Sub-Saharan Africa"). Optionally, paste regional context below
where indicated.

---

## Prompt (copy everything below this line)

I need you to perform a validity analysis of the AI benchmark described in the uploaded PDF, evaluating it for the target region: **{REGION}**.

### Your Task

You will:
1. Read the entire PDF carefully
2. Extract verbatim quotes relevant to validity analysis
3. Score the benchmark across 6 validity dimensions
4. Output a structured JSON result

### Step 1: Read and Extract

Read the full benchmark paper. For each of these 8 categories, extract ALL relevant **verbatim quotes** (exact text from the paper, with page numbers):

1. **Task taxonomy**: What tasks does the benchmark cover? How are they organized? Gaps?
2. **Data sources**: Where does the data come from? Languages/regions represented? Sample counts?
3. **Data format**: Input modalities, encoding, normalization, preprocessing
4. **Label categories**: Output taxonomies, how label sets were designed
5. **Annotation process**: Who annotated? Demographics? Agreement statistics? Disagreement resolution?
6. **Evaluation metrics**: What metrics? Output modality? Metric limitations?
7. **Stated limitations**: Authors' acknowledged gaps, biases, concerns
8. **Authors/affiliations**: Who built this and where are they based?

For each quote, note:
- The **exact text** (complete sentences, never truncate)
- The **page number**
- The **category** it belongs to

If the paper is SILENT on a category (especially annotation demographics, inter-annotator agreement), note: "NOT DOCUMENTED — paper is silent on [topic]."

### Step 2: Analyze for Regional Validity

Using your extracted quotes as evidence, evaluate the benchmark against each of these 6 dimensions:

**Dimension 1: Input Ontology** — Does the task taxonomy cover categories relevant to regional deployment?
- [IO-1] Identify test case categories required for regional deployment.
- [IO-2] Check if the taxonomy omits regionally-relevant categories.
- [IO-3] Check if any categories are irrelevant to the regional context.
- [IO-4] Document category gaps that would harm content validity.

**Dimension 2: Input Content** — Is the data culturally grounded and representative of the target region?
- [IC-1] Do input queries require region-specific cultural, geographic, or dialectal knowledge?
- [IC-2] Does culturally sensitive content align with the target culture?
- [IC-3] Flag inputs requiring Western-specific knowledge that may not transfer.
- [IC-4] Were regional annotators involved in content validation?
- [IC-5] Document content issues that would harm content validity.

**Dimension 3: Input Form** — Is the signal encoding appropriate for regional infrastructure?
- [IF-1] Compare signal distributions between source and target contexts.
- [IF-2] Check if regional infrastructure supports the data capture specifications.
- [IF-3] Identify domain-specific form differences relevant to the region.
- [IF-4] Document form mismatches that would harm external validity.

**Dimension 4: Output Ontology** — Are label categories appropriate for the regional context?
- [OO-1] Review output label categories for regional relevance.
- [OO-2] Identify missing categories specific to the regional context.
- [OO-3] Flag categories that encode non-regional values or assumptions.
- [OO-4] Consider if stakeholder-driven taxonomy redesign is warranted.
- [OO-5] Document taxonomy issues that would harm structural and content validity.

**Dimension 5: Output Content** — Do ground-truth labels represent regional perspectives?
- [OC-1] Do ground truth labels reflect regional stakeholder perspectives?
- [OC-2] Assess potential disagreement between original annotators and regional population.
- [OC-3] Review annotator demographics in benchmark documentation.
- [OC-4] Has label re-annotation by a representative regional pool been conducted?
- [OC-5] Were minority annotator perspectives preserved or majority-voted away?
- [OC-6] Document label issues that would harm convergent and external validity.

**Dimension 6: Output Form** — Does the output modality match regional deployment needs?
- [OF-1] Check if expected output modality matches regional deployment needs.
- [OF-2] Assess text-to-speech or speech availability if relevant.
- [OF-3] Consider literacy rates and accessibility requirements.
- [OF-4] Document form mismatches that would harm external validity.

### Scoring Rubric (1-5)

- **1**: Major validity violations; fundamentally misaligned with target context.
- **2**: Significant concerns; multiple concrete violations or gaps.
- **3**: Partially addressed; mixed evidence; some alignment, some gaps.
- **4**: Well addressed; minor concerns; documentation shows awareness.
- **5**: No concerns; explicit validity-preserving practices demonstrated.

### Critical Rules

- **Document-grounded only**: Base analysis ONLY on evidence in the paper and factual regional context. Do NOT role-play as a member of the target culture.
- **Cite evidence**: For each finding, reference specific quotes from the paper.
- **Flag gaps**: When documentation is silent, say "INSUFFICIENT DOCUMENTATION."
- **Conservative scoring**: When ambiguous, score lower rather than higher.

### Regional Context (Optional)

{REGIONAL_CONTEXT — Paste content from a regions/*.yaml file here for richer context.
If omitted, use your general knowledge of the target region, but note that this
is less reliable for Global South regions. Mark uncertain regional claims as
"[BASED ON GENERAL KNOWLEDGE]".}

### Required Output

First, list your extracted quotes in a table:

| # | Page | Category | Verbatim Quote |
|---|------|----------|----------------|
| Q1 | ... | ... | "..." |

Then output a single JSON object:

```json
{
  "benchmark": "<name>",
  "region": "<region>",
  "dimensions": {
    "input_ontology": {
      "score": <1-5>,
      "justification": "...",
      "checklist_responses": { "IO-1": "...", "IO-2": "...", "IO-3": "...", "IO-4": "..." },
      "evidence_quotes": ["[Q1] 'quote text' (p.X)", ...],
      "confidence": "<high|medium|low>",
      "information_gaps": ["..."],
      "requires_expert_verification": ["..."]
    },
    "input_content": { ... },
    "input_form": { ... },
    "output_ontology": { ... },
    "output_content": { ... },
    "output_form": { ... }
  },
  "overall_summary": "...",
  "risk_assessment": "<high|medium|low>",
  "remediation_suggestions": "...",
  "highest_concern_dimensions": ["..."],
  "strongest_dimensions": ["..."]
}
```
