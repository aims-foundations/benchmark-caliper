# Two-Prompt Version: Step 2 — Validity Scoring

Use this prompt AFTER completing Step 1. The extracted quotes and benchmark summary
from Step 1 should already be in the conversation context.

Replace {REGION} with your target region. Optionally paste regional context where indicated.

---

## Prompt (copy everything below this line)

Using the benchmark information and quote registry you just extracted, perform a validity analysis for the target region: **{REGION}**.

### Quote Provenance Rules

The benchmark information from Step 1 contains two types of text:

- **Verbatim quotes** in the Quote Registry (Q1, Q2, ...) — these are **authoritative evidence** from the PDF.
- **Narrative context** — interpretive summaries. These provide useful framing but are NOT evidence.

When populating `evidence_quotes` in your output:
- ONLY cite text from the Quote Registry
- Format: `"[QN] 'exact quote text' (p.X)"`
- Do NOT cite narrative text as evidence
- If no quote supports a finding, say so explicitly

### Scoring Rubric (1-5)

- **1**: Major validity violations; fundamentally misaligned with target context.
- **2**: Significant concerns; multiple concrete violations or gaps.
- **3**: Partially addressed; mixed evidence; some alignment, some gaps.
- **4**: Well addressed; minor concerns; documentation shows awareness.
- **5**: No concerns; explicit validity-preserving practices demonstrated.

### Critical Rules

- **Document-grounded only**: Base analysis ONLY on evidence from the quote registry and factual regional context. Do NOT role-play as a member of the target culture.
- **Cite evidence**: Every score must be backed by specific quotes.
- **Flag gaps**: When documentation is silent, say "INSUFFICIENT DOCUMENTATION."
- **Conservative scoring**: When ambiguous, score lower.

### Regional Context

{REGIONAL_CONTEXT — Paste content from a regions/*.yaml file here for richer analysis.
If omitted, use your general knowledge, but mark uncertain claims as
"[BASED ON GENERAL KNOWLEDGE]".}

### Dimensions to Evaluate

For each dimension, answer every checklist item, then provide a score with justification.

**1. Input Ontology** — Task taxonomy coverage for regional deployment
- [IO-1] Identify test case categories required for regional deployment.
- [IO-2] Check if taxonomy omits regionally-relevant categories.
- [IO-3] Check if any categories are irrelevant to the regional context.
- [IO-4] Document category gaps that would harm content validity.

**2. Input Content** — Cultural grounding and representativeness
- [IC-1] Do inputs require region-specific cultural/geographic/dialectal knowledge?
- [IC-2] Does culturally sensitive content align with the target culture?
- [IC-3] Flag inputs requiring Western-specific knowledge.
- [IC-4] Were regional annotators involved in content validation?
- [IC-5] Document content issues that would harm content validity.

**3. Input Form** — Signal encoding and infrastructure compatibility
- [IF-1] Compare signal distributions between source and target contexts.
- [IF-2] Check if regional infrastructure supports the data specifications.
- [IF-3] Identify domain-specific form differences.
- [IF-4] Document form mismatches that would harm external validity.

**4. Output Ontology** — Label taxonomy appropriateness
- [OO-1] Review label categories for regional relevance.
- [OO-2] Identify missing categories specific to the region.
- [OO-3] Flag categories encoding non-regional values.
- [OO-4] Consider if stakeholder-driven redesign is warranted.
- [OO-5] Document taxonomy issues harming structural/content validity.

**5. Output Content** — Label correctness and annotator representativeness
- [OC-1] Do labels reflect regional stakeholder perspectives?
- [OC-2] Potential disagreement between original and regional annotators?
- [OC-3] Review annotator demographics documentation.
- [OC-4] Has representative regional re-annotation been done?
- [OC-5] Were minority perspectives preserved or majority-voted away?
- [OC-6] Document label issues harming convergent/external validity.

**6. Output Form** — Output modality and metric appropriateness
- [OF-1] Does output modality match regional deployment needs?
- [OF-2] Speech/TTS availability if relevant?
- [OF-3] Literacy and accessibility requirements?
- [OF-4] Document form mismatches harming external validity.

### Required Output

Output a single valid JSON object:

```json
{
  "benchmark": "<name from Step 1 metadata>",
  "region": "{REGION}",
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
  "overall_summary": "3-5 sentence summary",
  "risk_assessment": "<high|medium|low>",
  "remediation_suggestions": "prioritized actions",
  "highest_concern_dimensions": ["dimension names with lowest scores"],
  "strongest_dimensions": ["dimension names with highest scores"]
}
```
