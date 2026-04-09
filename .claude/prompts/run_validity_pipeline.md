# End-to-End Validity Analysis Pipeline (Optimized)

Given a benchmark paper PDF, run the full pipeline: extract structured YAMLs, enrich
regional context via web search, compose the evaluation prompt, run scoring via subagent,
and save all artifacts.

## Usage

Provide the path to a benchmark paper PDF as the argument to this prompt:

```
/run_validity_pipeline papers/some_benchmark.pdf
```

For automated testing with a simulated persona (skips human elicitation and uses a test persona to answer elicitation questions in character):

```
/run_validity_pipeline papers/some_benchmark.pdf --persona <PERSONA_ID>
```

Persona IDs are defined in `.claude/prompts/personas.md`. Each pairs a benchmark with a simulated practitioner. "A" personas represent reasonable-fit deployments; "B" personas represent poor-fit deployments. The pipeline should produce discriminably different scores between A and B for the same benchmark.

---

## Cost Optimization Architecture

This pipeline uses **model routing** and **scripts** to minimize cost:

| Component | Model/Tool | Rationale |
|-----------|-----------|-----------|
| PDF page count & split | **Bash script** | No LLM needed |
| Per-page quote extraction | **Haiku subagents** | Simple extraction, 1-page context |
| Quote consolidation | **Sonnet subagent** | Dedup/renumber, moderate reasoning |
| YAML structuring | **Sonnet subagent** | Template-filling, not deep reasoning |
| Quote verification (counts) | **Python script** | Mechanical comparison |
| Quote spot-check (text) | **Sonnet subagent** | Text comparison |
| Elicitation (questions + summary) | **Sonnet subagent(s)** | Question selection, context structuring |
| Persona simulation (test mode) | **Sonnet subagent** | In-character answer generation |
| Region YAML creation | **Sonnet subagent** | Factual/structural |
| Web search enrichment | **Sonnet subagent** | Search + synthesis (guided by elicitation) |
| Prompt composition | **Python script** | Deterministic template fill |
| Validity scoring | **Opus subagent** | Only step needing deep reasoning |
| Report formatting | **Python script** | JSON → table |

**Opus is used for exactly 1 call** (validity scoring). Everything else uses Haiku,Sonnet, or scripts. Elicitation adds 2-3 Sonnet calls (or 3-4 in persona test mode).

---

## Pipeline Steps

Follow each step sequentially — do NOT skip steps or combine them.

### Step 0: Read project context

Read the following files to understand the project structure, YAML formats, and
evaluation framework:

- `README.md` — project overview and expected file formats
- `framework.yaml` — the 6 validity dimensions, checklists, and scoring rubric
- `prompt_template.md` — the template used to compose evaluation prompts

Also list existing files in `benchmarks/` and `regions/` so you know what already exists.

### Step 1: Extract benchmark information from the PDF

This step has three substeps: extract quotes via per-page Haiku subagents, consolidate via Sonnet, then verify the provenance chain.

#### Step 1a: Extract quotes via `/validity-pdf-extract`

Use the project-specific `/validity-pdf-extract` skill to process the paper.
The skill now uses **per-page Haiku extraction** with **Sonnet consolidation**:

```
/validity-pdf-extract <path-to-pdf>
```

The skill produces a markdown file with:
1. **Narrative Context** — Interpretive prose organized by 8 validity-relevant
   categories, with `[QN]` references into the quote registry. Non-authoritative.
2. **Quote Registry** — Indexed table of verbatim quotes. **Authoritative.**

Save the output to `papers/<benchmark_name>_paper_summary.md`.

#### Step 1b: Structure the summary into a benchmark YAML

Spawn a **Sonnet subagent** (use `model: sonnet` in the Agent tool) to structure
the paper summary into the benchmark YAML.

The subagent prompt should include:
- The full paper summary from Step 1a
- 1-2 existing benchmark YAMLs from `benchmarks/` as format examples
- Instructions for required fields and structure (below)

**Required fields:**
- `name` — short identifier (lowercase, no spaces)
- `full_name` — full benchmark title from the paper
- `year` — publication year
- `domain` — what the benchmark evaluates
- `porting_strategy` — one of: `ground_up`, `adapted`, `mixed`, `translation`, `parallel`, `regional_exams`, `none`
- `languages` — list of language codes covered
- `primary_region` — the geographic/cultural region the benchmark targets

**Required section: `documentation_excerpts`**

Interpretive narrative organized by the 6 validity dimensions, referencing quotes
by registry IDs (e.g., `[Q3]`, `[Q14]`). Structure with these headers:
1. **Input Ontology** — Task taxonomy, test case categories, coverage, stated gaps
2. **Input Content** — Data sources, collection methodology, cultural grounding
3. **Input Form** — Signal encoding, data formats, preprocessing
4. **Output Ontology** — Label categories, output types, taxonomy design
5. **Output Content** — Annotation process, annotator demographics, IAA
6. **Output Form** — Output modality, evaluation metrics, scoring methodology

Propagate "NOT DOCUMENTED" notes from the paper summary.

**Required section: `verbatim_quotes`**

Copy ALL Quote Registry entries into a structured YAML list:

```yaml
verbatim_quotes:
  - id: Q1
    text: "exact quote text"
    page: 20
    dimension: input_ontology
```

Rules:
- Propagate ALL quotes — do not drop any.
- Copy quote text exactly as it appears in the registry.
- Tag each quote with the most relevant validity dimension.

Save to `benchmarks/<name>.yaml`.

#### Step 1c: Verify quote provenance chain

Run the **mechanical verification script** first:

```bash
python3 scripts/verify_quotes.py benchmarks/<name>.yaml papers/<name>_paper_summary.md
```

This checks: count match, ID continuity, and dimension coverage.

Then, spawn a **Sonnet subagent** for the **text spot-check**: read 3 quotes'
original PDF pages and confirm character-for-character match. The subagent
receives ONLY the 3 quotes + their page numbers + the PDF path — minimal context.

Subagent prompt:
```
Spot-check 3 verbatim quotes against the original PDF.

For each quote below, read the specified page of the PDF using the Read tool
with the pages parameter, then confirm the quote text matches exactly.

Quote 1: [id, text, page]
Quote 2: [id, text, page]
Quote 3: [id, text, page]

PDF path: <path>

For each quote, report:
- MATCH: text matches the PDF exactly
- MISMATCH: text differs (show the difference)
- NOT FOUND: quote text not found on the specified page
```

If mismatches are found, correct them in both the paper summary and YAML.

Report verification results before proceeding.

### Step 1d: Elicit deployment context from the user

This step gathers the user's deployment context — who will use the system, where,and what cultural concerns matter — so that downstream steps (region inference, web search, scoring) can be conditioned on the actual use case rather than operating generically.

**Guide file:** `.claude/prompts/elicitation_guide.md` — this file contains the full elicitation logic (question selection heuristics, weighting rules, output format). The subagent reads it as its operational guide. If the guide is updated in the future, this step requires no changes.

#### Interactive mode (default)

Spawn a **Sonnet subagent** with the following inputs:

1. The full text of `.claude/prompts/elicitation_guide.md`
2. The benchmark YAML from Step 1b (so the subagent knows what the benchmark covers)
3. The user's initial description of their use case and target population

The subagent will:
1. Read the elicitation guide and benchmark metadata
2. Select 3-5 targeted questions using the guide's weighting heuristics
3. Return the questions to the orchestrator

The orchestrator then presents the questions to the user (via `AskUserQuestion`)
and collects their answers.

Then spawn the **same or a new Sonnet subagent** with:
1. The elicitation guide
2. The original use-case description
3. The user's answers

The subagent produces a structured **elicitation summary** following the output
format defined in the guide (use case, target population, elicitation responses,
dimension priority weights, cultural topic priorities, flagged gaps).

Save the summary to `papers/<benchmark_name>_elicitation_summary.md`.

#### Automated testing mode (persona-driven)

When the pipeline is invoked with a `--persona` argument (e.g.,
`/run_validity_pipeline papers/helm.pdf --persona HELM-B`), skip the human interaction and use the test personas defined in `.claude/prompts/personas.md`.

The orchestrator mediates a cross-subagent exchange:

1. **Elicitation subagent** (Sonnet) — receives the elicitation guide + the persona's `initial_description` field (as if the user typed it). Returns 3-5 elicitation questions.

2. **Persona subagent** (Sonnet) — receives the persona block from `personas.md` (wrapped in the persona system prompt pattern defined in that file) + the elicitation questions. Returns in-character answers.

3. **Elicitation subagent** (Sonnet) — receives the persona answers. Produces the structured elicitation summary.

Save the summary to `papers/<benchmark_name>_elicitation_summary.md` as usual.
The rest of the pipeline proceeds identically — downstream steps consume the summary without knowing whether it came from a human or a persona.

### Step 2: Infer target region and resolve region YAML

From the benchmark paper **and the elicitation summary**, infer the primary target region. The elicitation summary from Step 1d provides the user's actual deployment context, which may differ from the benchmark's stated target. Consider:

- What region/culture does the benchmark claim to serve?
- Where were the data and annotations sourced from?
- **What is the user's intended deployment region and population?** (from elicitation summary)
- If there is a mismatch between the benchmark's source region and the user'starget region, the region YAML should reflect the **user's target region** — the validity analysis evaluates fit-for-purpose, not the benchmark in isolation.

Check if an existing region YAML in `regions/` matches the user's target region.

**If a match exists:** Use the existing region YAML. Proceed to Step 3.

**If no match exists:** Spawn a **Sonnet subagent** to create a new region YAML at `regions/<name>.yaml`. The subagent receives:
- The benchmark name and target region
- The paper summary's relevant sections
- The elicitation summary (for population details, languages, cultural concerns)
- Instructions for required fields (countries, languages, writing systems,
  literacy rates, cultural norms, infrastructure, domain-specific notes)
- Instruction to mark uncertain items with [NEEDS VERIFICATION]

### Step 3: Web search to enrich regional context

This step is critical for addressing recall limitations. Spawn a **Sonnet subagent**
to perform targeted web searches and update the region YAML.

**Guide file:** `.claude/prompts/web_search_guide.md` — this file contains the full search strategy (budget allocation heuristics, per-topic query templates,source priorities, unsearchable-knowledge flags). The subagent reads it as its
operational guide. If the guide is updated in the future, this step requires no changes.

The subagent receives:

1. The full text of `.claude/prompts/web_search_guide.md`
2. The current region YAML
3. The benchmark YAML (task categories, languages, domain)
4. The elicitation summary from Step 1.5 (deployment context, dimension priority weights, cultural topic priorities, flagged gaps)

The subagent will:

1. Read the web search guide to understand search strategy and budget allocation
2. Use the elicitation summary's **dimension priority weights** and **cultural topic priorities** to focus its search budget on the highest-impact areas
3. Use the elicitation summary's **flagged gaps** as initial search targets — these are areas where the evidence base is thin and web search is most valuable
4. Execute 5-10 targeted web searches following the guide's heuristics
5. Update the region YAML's notes sections with findings, adding a `web_search_enrichment` field documenting searches, findings, and conflicts
6. Write the updated YAML to `regions/<name>.yaml`

### Step 4: Compose the evaluation prompt (SCRIPT)

Run the **prompt composition script** — no LLM needed:

```bash
python3 scripts/compose_prompt.py \
    --benchmark benchmarks/<name>.yaml \
    --region regions/<name>.yaml \
    --framework framework.yaml \
    --elicitation papers/<benchmark_name>_elicitation_summary.md \
    --output .claude/prompts/<name>/variant_a_neutral.md
```

This deterministically assembles the evaluation prompt from YAML artifacts,including all quote provenance rules, the full quote registry, regional context, deployment context from elicitation, and framework dimensions.

The `--elicitation` flag injects the elicitation summary into the composed prompt as a "Deployment Context" section, so the Opus scorer can see the user's use case, target population, dimension priority weights, and flagged gaps.

Verify the output file was created and report its size.

### Step 5: Run the validity analysis via Opus subagent

This is the **only Opus call** in the pipeline. Spawn an **Opus subagent**
(use `model: opus` in the Agent tool) with the composed prompt.

In the subagent prompt:

1. Include the full text of the composed prompt from Step 4. (This now includes a "Deployment Context" section with the elicitation summary — the scorer sees the user's use case, target population, dimension priority weights, and flagged gaps as part of the prompt.)

2. Instruct the subagent to write its output as a single valid JSON file.

3. Remind the subagent of two key context rules:

   > **Deployment context conditions the analysis.** The "Deployment Context" section
   > contains the user's specific use case, target population, and dimension priority
   > weights from elicitation. Your validity analysis must evaluate the benchmark's
   > fitness for THIS specific deployment — not in the abstract. Dimensions marked
   > HIGH priority in the elicitation should receive the most thorough analysis.
   > Flagged gaps from elicitation should be explicitly addressed in your assessment.

4. Remind the subagent of the quote provenance rules:

   > **Quote provenance is critical.** The benchmark documentation in this prompt
   > contains two clearly separated sections: "Benchmark Documentation" (interpretive
   > context with [QN] references) and "Verbatim Quote Registry" (authoritative
   > evidence from the original paper). When you populate `evidence_quotes` in your
   > JSON output, you MUST only include text from the Verbatim Quote Registry, formatted
   > as `"[QN] 'exact quote text' (p.X)"`. Do NOT cite the interpretive context as
   > evidence. If no verbatim quote supports a finding, say so explicitly.

5. The JSON must follow the project's result format (see README.md):

```json
{
  "benchmark": "<benchmark_name>",
  "region": "<region_name>",
  "dimensions": {
    "input_ontology": {
      "score": "<1-5>",
      "justification": "...",
      "checklist_responses": { "IO-1": "...", ... },
      "evidence_quotes": ["[Q1] 'quote text' (p.7)", ...],
      "confidence": "<high|medium|low>",
      "information_gaps": ["..."],
      "requires_expert_verification": ["..."]
    },
    "input_content": { "..." },
    "input_form": { "..." },
    "output_ontology": { "..." },
    "output_content": { "..." },
    "output_form": { "..." }
  },
  "overall_summary": "...",
  "risk_assessment": "<high|medium|low>",
  "remediation_suggestions": "...",
  "highest_concern_dimensions": ["..."],
  "strongest_dimensions": ["..."]
}
```

6. The output file should be saved to `results/<benchmark_name>_<region_name>.json`.

### Step 6: Report results (SCRIPT)

Run the **report formatting script** — no LLM needed:

```bash
python3 scripts/format_results.py results/<benchmark_name>_<region_name>.json
```

This prints:
- Score summary table (dimension → score → confidence)
- Overall risk assessment
- Top concerns and strongest dimensions
- Remediation suggestions
- File paths for all artifacts

---

## Important Notes

- **Thoroughness over speed for extraction.** Step 1 is the most important step.
  The `/validity-pdf-extract` skill uses per-page Haiku extraction to ensure every
  page is read without truncation — this is more thorough than the old chunked approach.
- **Quote provenance is structural, not aspirational.** The two-section output format
  (narrative + quote registry) prevents "evidence laundering." The `verbatim_quotes`
  YAML field and the Verbatim Quote Registry in the composed prompt are the
  authoritative evidence chain.
- **Step 1c verification is not optional.** The script handles mechanical checks;
  the Sonnet subagent handles text spot-checks. Both must pass.
- **Elicitation conditions everything downstream.** Step 1d gathers the user's deployment context. Steps 2, 3, and 5 all consume the elicitation summary. Without it, the pipeline evaluates the benchmark generically rather than for a specific use case.
- **The elicitation guide and web search guide are referenced by file path.** Updating those files changes pipeline behavior without modifying this prompt.
- **Web search is not optional.** Step 3 addresses recall failures — the primary
  risk in LLM-based validity analysis.
- **Result format matters.** The JSON output must match the project's schema exactly.
- **Model routing is intentional.** Do not upgrade Haiku/Sonnet steps to Opus.
  The routing is designed to use each model where its capability level suffices.

## Prerequisites

- `/validity-pdf-extract` skill at `.claude/skills/validity-pdf-extract/`
- Python 3 with PyYAML (`pip install pyyaml`)
- pdftk or qpdf for PDF splitting (optional — falls back to Read tool)
- `framework.yaml`, `README.md`, and `prompt_template.md` in project root

## Cost Comparison

| Component | Old (all-Opus) | New (routed) |
|-----------|---------------|--------------|
| PDF extraction | Opus × N chunks | Haiku × N pages + Sonnet × 1 |
| YAML structuring | Opus × 1 | Sonnet × 1 |
| Verification | Opus × 1 | Script + Sonnet × 1 |
| Elicitation | — (new components) | Sonnet × 2-3 (+ 1 more in test mode) |
| Region creation | Opus × 1 | Sonnet × 1 |
| Web enrichment | Opus × 1 | Sonnet × 1 (guided by elicitation) |
| Prompt composition | Opus × 1 | Script (free) |
| Scoring | Opus × 1 | Opus × 1 |
| Reporting | Opus × 1 | Script (free) |
| **Total Opus calls** | **~6-8** | **1** |
