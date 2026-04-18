# Validity Analysis Prompt Template

Use this template when asking Claude Code to evaluate a benchmark against a target region using the validity framework.

---

## Instructions for Claude Code

You are an expert in AI benchmark validity analysis. You will be given:
1. A **benchmark description** (metadata, documentation excerpts, design details)
2. A **target region/culture** (with factual context about the region)
3. The **validity framework** (6 dimensions with checklists)

Your task is to analyze the benchmark's documentation and assess potential validity violations when the benchmark is applied to the specified regional/cultural context.

### Critical Constraints

- **Document-grounded only**: Base your analysis ONLY on evidence found in the provided benchmark documentation and the factual regional context given. Do NOT role-play as a member of the target culture or speculate beyond what the documentation supports.
- **Cite evidence**: For each finding, quote or reference specific parts of the benchmark documentation.
- **Flag gaps explicitly**: When information is missing from the documentation, say "INSUFFICIENT DOCUMENTATION" and describe what would be needed.
- **Distinguish documentable vs. expert-needed**: Classify each finding as either (a) determinable from documentation, or (b) requiring regional expert verification.

### Scoring Rubric (1-5 scale)

- **1** = Major validity violations; benchmark component fundamentally misaligned with target context based on documented evidence.
- **2** = Significant concerns; multiple concrete violations or gaps identified in documentation.
- **3** = Partially addressed; mixed evidence; some alignment, some gaps.
- **4** = Well addressed; minor concerns or gaps; documentation shows awareness of regional needs.
- **5** = Fully addressed; no concerns identified; documentation demonstrates explicit validity-preserving practices for target context.

---

## Prompt Template

Copy and fill in the sections below, then provide the filled template to Claude Code.

```
I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Benchmark Information

**Name**: {BENCHMARK_NAME}
**Domain**: {DOMAIN}
**Languages**: {LANGUAGES}
**Porting Strategy**: {translation | parallel_construction | ground_up | mixed}
**Year**: {YEAR}

### Benchmark Documentation
{Paste key excerpts from the benchmark's paper, README, datasheet, or other documentation.
Include: abstract, data collection methodology, annotation process, task descriptions,
language coverage, any stated limitations.}

## Target Region

**Region**: {REGION_NAME}
**Countries**: {COUNTRIES}
**Languages**: {LANGUAGES}
**Writing Systems**: {WRITING_SYSTEMS}

### Regional Context
{Paste the regional context from the region YAML file, including literacy rates,
cultural norms, infrastructure notes, etc.}

## Framework Dimensions to Evaluate

For each of the 6 dimensions below, answer every checklist question, then provide an
overall score (1-5) with justification.

### Dimension 1: Input Ontology
Definition: The input data ontology consists of the set of test case categories represented
by the benchmark, which should cover the query types that evaluated systems are expected to
encounter during deployment (e.g., factual questions, creative writing help, or restaurant
recommendations for NLP dialogue systems; pick-and-place tasks, point navigation, or planning
for robotics).

Theoretical Importance: A misalignment in this taxonomy — whether through the omission of
necessary categories (construct underrepresentation) or the inclusion of irrelevant ones
(construct-irrelevant variance) — harms the content validity of the benchmark.

Checklist:
- [IO-1] Identify test case categories required for regional deployment.
- [IO-2] Check if source benchmark's taxonomy omits regionally-relevant categories.
- [IO-3] Check if source benchmark includes categories irrelevant to regional context.
- [IO-4] Document category gaps that would harm content validity.

### Dimension 2: Input Content
Definition: Whereas the ontology defines the types of input queries, the content of dataset
inputs refers to the explicit instances specified by individual datapoints — an LLM prompt,
an image, a database entry, etc.

Theoretical Importance: Even when the test case taxonomy provides good coverage,
implementation-level details of individual datapoints can introduce construct-irrelevant
variance, violating content validity.

Checklist:
- [IC-1] Determine if input queries require region-specific cultural, geographic, or dialectal knowledge.
- [IC-2] Assess whether culturally sensitive content aligns with target deployment culture.
- [IC-3] Flag inputs requiring Western-specific knowledge that may not transfer.
- [IC-4] Recruit regional annotators to identify culturally sensitive instances if resources permit.
- [IC-5] Document content issues that would harm content validity.

### Dimension 3: Input Form
Definition: The form of dataset inputs determines the encoding of the input signal — e.g.,
text vs. audio for natural language, or camera parameters such as focal length and resolution
for visual data.

Theoretical Importance: Since machine learning systems are sensitive to signal distributions,
a mismatch between the benchmark's input representation and the real-world signals that
deployed models would encounter violates the external validity of the evaluation.

Checklist:
- [IF-1] Compare signal distributions between source and target contexts.
- [IF-2] Check if regional infrastructure supports the same data capture specifications.
- [IF-3] Identify domain-specific form differences relevant to the intended use case.
- [IF-4] Document form mismatches that would harm external validity.

### Dimension 4: Output Ontology
Definition: A benchmark's output ontology determines the space of outputs an AI system is
expected to produce and the decision rules by which those outputs are organized and scored
— i.e., the benchmark's criteria. For categorical outputs, the mapping is direct (e.g.,
safe/unsafe, or object class labels). For free-form outputs, the scoring function must
first interpret what the output means before mapping it to a score — and this interpretive
step is where validity violations most readily arise, since decision rules can differ across
cultural contexts. For instance, an LLM recommending "red wine" for a dinner party may
score highly for helpfulness in a Western context but poorly where alcohol consumption is
prohibited.

Theoretical Importance: A misaligned output taxonomy thus violates structural validity
(the construct's structure is misrepresented), content validity (through missing or
irrelevant categories), and risks violating external validity (benchmark performance is
less likely to generalize to regional settings).

Checklist:
- [OO-1] Review output label categories for regional relevance.
- [OO-2] Identify missing categories specific to regional contexts.
- [OO-3] Flag categories that encode non-regional values or assumptions.
- [OO-4] Consider stakeholder-driven taxonomy redesign if significant misalignment exists.
- [OO-5] Document taxonomy issues that would harm structural validity and content validity.

### Dimension 5: Output Content
Definition: Whereas taxonomic alignment addresses whether abstract decision boundaries
reflect regional values, label correctness concerns whether the labels for particular
datapoints correlate with the judgments of regional stakeholders.

Theoretical Importance: Disagreement between regional and original annotators violates
both convergent validity (the labels fail to correlate with regional perspectives on the
construct) and external validity (the original judgments do not generalize to the target
context).

Checklist:
- [OC-1] Determine if ground truth labels reflect regional stakeholder perspectives.
- [OC-2] Assess potential disagreement between original annotators and regional population.
- [OC-3] Review annotator demographics in benchmark documentation (Datasheets, Data Statements).
- [OC-4] Consider label re-annotation by representative regional annotator pool.
- [OC-5] Review aggregation methods for potential erasure of minority perspectives.
- [OC-6] Document label issues that would harm convergent validity and external validity.

### Dimension 6: Output Form
Definition: The form of dataset outputs pertains to the representation of output signals
models are expected to produce.

Theoretical Importance: If a benchmark does not evaluate models on the output forms
encountered during real-world deployment, this violates the external validity of the
evaluation.

Checklist:
- [OF-1] Check if expected output modality matches regional deployment needs.
- [OF-2] Assess text-to-speech availability for speech-based output requirements.
- [OF-3] Consider literacy rates and accessibility requirements in target population.
- [OF-4] Document form mismatches that would harm external validity.

## Required Output Format

For each dimension, respond with:

```json
{
  "dimension": "<dimension_name>",
  "score": <1-5>,
  "justification": "<2-4 sentence summary of overall assessment>",
  "checklist_responses": {
    "<checklist_id>": "<your assessment for this item>"
  },
  "evidence_quotes": ["<relevant quote from benchmark docs>"],
  "confidence": "<high|medium|low>",
  "information_gaps": ["<what info was missing>"],
  "requires_expert_verification": ["<findings that need regional expert input>"]
}
```

After all 6 dimensions, provide:

```json
{
  "overall_summary": "<3-5 sentence summary of the benchmark's validity for this region>",
  "risk_assessment": "<high|medium|low risk of validity violations>",
  "remediation_suggestions": "<key actions to improve validity>",
  "highest_concern_dimensions": ["<dimensions with lowest scores>"],
  "strongest_dimensions": ["<dimensions with highest scores>"]
}
```
```

---

## Prompt Variants (for robustness testing)

To check for prompt sensitivity, re-run each benchmark with these variant framings:

### Variant A: Neutral (default above)
Use the template as-is.

### Variant B: Problem-focused
Add to the instructions: "Focus on identifying concrete validity violations and gaps.
For each dimension, lead with the most significant problems you find before noting
any strengths."

### Variant C: Strength-focused
Add to the instructions: "Focus on identifying what the benchmark does well for this
regional context. For each dimension, lead with strengths and alignment before noting
any remaining gaps."

If scores differ by more than 2 points across variants for any dimension, flag that
dimension for mandatory human review.
