# End-to-End Validity Analysis Pipeline (Optimized)

Given a benchmark paper PDF, run the full pipeline: elicit user deployment context early,
extract structured YAMLs guided by that context, enrich regional context via web search,
compose the evaluation prompt, run scoring via subagent, and save all artifacts.

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
| Quick metadata extraction | **Haiku subagent** | Read 1-2 pages, extract basic metadata |
| Elicitation (questions + summary) | **Sonnet subagent(s)** | Runs early — only needs metadata |
| Persona simulation (test mode) | **Sonnet subagent** | In-character answer generation |
| PDF page count & split | **Bash script** | No LLM needed |
| Per-page quote extraction | **Haiku subagents** | Simple extraction, 1-page context (guided by elicitation priorities) |
| Quote consolidation | **Sonnet subagent** | Dedup/renumber, moderate reasoning |
| YAML structuring | **Sonnet subagent** | Template-filling, not deep reasoning |
| Quote verification (counts) | **Python script** | Mechanical comparison |
| Quote spot-check (text) | **Sonnet subagent** | Text comparison |
| Region YAML creation | **Sonnet subagent** | Factual/structural |
| Web search enrichment | **Sonnet subagent** | Search + synthesis (guided by elicitation) |
| Prompt composition | **Python script** | Deterministic template fill |
| Validity scoring | **Opus subagent** | Only step needing deep reasoning |
| Report formatting | **Python script** | JSON → table |

**Opus is used for exactly 1 call** (validity scoring). Everything else uses Haiku, Sonnet, or scripts. Elicitation adds 1 Haiku call + 2-3 Sonnet calls (or 3-4 in persona test mode).

### Why elicitation runs first

The user interaction happens **before** heavy PDF processing. This serves two goals:

1. **User experience**: The user provides their deployment context within the first minute, then can walk away while the pipeline runs. No 5-10 minute wait before being asked questions.
2. **Extraction efficiency**: Knowing the user's dimension priorities and cultural topic priorities lets the extraction and consolidation steps focus on what matters, saving tokens and producing more targeted output.

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

### Step 1: Quick metadata extraction from the PDF

Before beginning, tag the logging module. Run:

```bash
python3 scripts/pipeline_module.py set elicitation
```

This is a **fast, lightweight step** — read only pages 1-2 of the PDF to extract basic benchmark metadata. The goal is to gather just enough context for elicitation, not to perform full extraction.

Spawn a **Haiku subagent** (use `model: haiku` in the Agent tool) with:
- The PDF path and instruction to read pages 1-2 only (abstract, introduction, title page)
- Instructions to extract these fields as a structured summary:

```
- name: short identifier (lowercase, no spaces)
- full_name: full benchmark title
- year: publication year
- domain: what the benchmark evaluates (1-2 sentences)
- languages: list of languages mentioned
- primary_region: the geographic/cultural region the benchmark targets
- porting_strategy: one of ground_up, adapted, mixed, translation, parallel, regional_exams, none
- brief_description: 2-3 sentence summary of what this benchmark does and how it was built
- source_culture: whether the benchmark was designed by/for the target population or transferred from another context
```

Subagent prompt template:
```
Read pages 1-2 of the PDF at "{PDF_PATH}" using the Read tool with pages: "1-2".

Extract the following metadata about this benchmark paper. Only use information
visible on these pages (abstract, introduction, title, authors). If a field
cannot be determined from pages 1-2, write "UNKNOWN".

Output as a structured text block:

- name: [short lowercase identifier]
- full_name: [full title]
- year: [publication year]
- domain: [what it evaluates]
- languages: [languages mentioned]
- primary_region: [target region/culture]
- porting_strategy: [ground_up | adapted | mixed | translation | parallel | regional_exams | none]
- brief_description: [2-3 sentence summary]
- source_culture: [designed by target population | transferred from Western context | mixed | unclear]
```

Save the output as `papers/<benchmark_name>_metadata.md`. This file is consumed by
Step 2 (elicitation) and later superseded by the full benchmark YAML.

**This step should complete in under 30 seconds.**

### Step 2: Elicit deployment context from the user

This step gathers the user's deployment context **early** — before heavy PDF processing — so that:
1. The user isn't waiting 5-10 minutes before being asked questions
2. Downstream extraction can be guided by what the user actually cares about

**Guide file:** `.claude/prompts/elicitation_guide.md` — this file contains the full elicitation logic (question selection heuristics, weighting rules, output format). The subagent reads it as its operational guide. If the guide is updated in the future, this step requires no changes.

#### Interactive mode (default)

Spawn a **Sonnet subagent** with the following inputs:

1. The full text of `.claude/prompts/elicitation_guide.md`
2. The lightweight metadata from Step 1 (so the subagent knows what the benchmark covers at a high level — name, domain, languages, region, porting strategy, source culture)
3. The user's initial description of their use case and target population

The subagent will:
1. Read the elicitation guide and benchmark metadata
2. Select 3-5 targeted questions using the guide's weighting heuristics
3. Return the questions to the orchestrator

**Note:** The elicitation guide's question selection logic is driven primarily by the user's use case and target region, not by detailed benchmark content. The lightweight metadata from Step 1 provides sufficient context (domain, languages, porting strategy, source culture) for the weighting heuristics. Full benchmark documentation is not needed at this stage.

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

1. **Elicitation subagent** (Sonnet) — receives the elicitation guide + the lightweight metadata from Step 1 + the persona's `initial_description` field (as if the user typed it). Returns 3-5 elicitation questions.

2. **Persona subagent** (Sonnet) — receives the persona block from `personas.md` (wrapped in the persona system prompt pattern defined in that file) + the elicitation questions. Returns in-character answers.

3. **Elicitation subagent** (Sonnet) — receives the persona answers. Produces the structured elicitation summary.

Save the summary to `papers/<benchmark_name>_elicitation_summary.md` as usual.
The rest of the pipeline proceeds identically — downstream steps consume the summary without knowing whether it came from a human or a persona.

### Step 3: Extract benchmark information from the PDF

Before beginning, tag the logging module. Run:

```bash
python3 scripts/pipeline_module.py set extraction
```

This step has three substeps: extract quotes via per-page Haiku subagents, consolidate via Sonnet, then verify the provenance chain.

**The elicitation summary from Step 2 is now available.** Use it to guide extraction focus (see notes below).

#### Step 3a: Extract quotes via `/validity-pdf-extract`

Use the project-specific `/validity-pdf-extract` skill to process the paper.
The skill uses **per-page Haiku extraction** with **Sonnet consolidation**:

```
/validity-pdf-extract <path-to-pdf> papers/<benchmark_name>_elicitation_summary.md
```

The second argument passes the elicitation summary from Step 2. The skill uses the summary's **dimension priority weights** and **cultural topic priorities** to:
- During consolidation, write more detailed narrative for HIGH-priority dimensions and briefer narrative for LOWER-priority dimensions
- Call out quotes related to the user's cultural topic priorities even if they would otherwise be treated as minor details

The skill produces a markdown file with:
1. **Narrative Context** — Interpretive prose organized by 8 validity-relevant
   categories, with `[QN]` references into the quote registry. Non-authoritative.
   HIGH-priority dimensions receive more detailed narrative.
2. **Quote Registry** — Indexed table of verbatim quotes. **Authoritative.**
   All quotes are still extracted from all pages — priority guidance affects
   narrative depth, not quote completeness.

Save the output to `papers/<benchmark_name>_paper_summary.md`.

#### Step 3b: Structure the summary into a benchmark YAML

Spawn a **Sonnet subagent** (use `model: sonnet` in the Agent tool) to structure
the paper summary into the benchmark YAML.

The subagent prompt should include:
- The full paper summary from Step 3a
- The elicitation summary from Step 2 (dimension priority weights, cultural topic priorities, flagged gaps)
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

**Required section: `coverage_gap_analysis`**

Cross-reference the elicitation summary against the benchmark documentation to
identify where the user's priorities and the benchmark's actual coverage diverge.
For each HIGH-priority dimension and each cultural topic priority from the
elicitation summary, assess whether the benchmark documents relevant content.

```yaml
coverage_gap_analysis:
  # For each elicitation priority, note what the benchmark covers vs. what's missing
  - user_priority: "sub-national variation in Nigeria"
    benchmark_coverage: "Country-level only — no state or ethnic group breakdown"
    gap_type: "partial"  # full | partial | none (none = benchmark covers it well)
    web_search_target: "Sub-national cultural variation benchmarks Nigeria Yoruba Igbo Hausa"
  - user_priority: "regional cuisines"
    benchmark_coverage: "NOT DOCUMENTED — no food-related tasks"
    gap_type: "full"
    web_search_target: "Nigerian cuisine cultural knowledge AI evaluation"
```

Gap types:
- **full**: The benchmark is silent on this priority. Web search should look for
  supplementary evidence or alternative benchmarks.
- **partial**: The benchmark addresses this but at insufficient depth or the wrong
  granularity for the user's context.
- **none**: The benchmark covers this priority well. No web search needed for this gap.

The `web_search_target` field provides a suggested search query for Step 5.
Only populate for `full` and `partial` gaps.

Save to `benchmarks/<name>.yaml`.

#### Step 3c: Verify quote provenance chain

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

### Step 4: Infer target region and resolve region YAML

Before beginning, tag the logging module. Run:

```bash
python3 scripts/pipeline_module.py set web_search
```

This covers Step 4 (region resolution) and Step 5 (web-search enrichment) as a single logging module.

From the benchmark paper **and the elicitation summary**, infer the primary target region. The elicitation summary from Step 2 provides the user's actual deployment context, which may differ from the benchmark's stated target. Consider:

- What region/culture does the benchmark claim to serve?
- Where were the data and annotations sourced from?
- **What is the user's intended deployment region and population?** (from elicitation summary)
- If there is a mismatch between the benchmark's source region and the user'starget region, the region YAML should reflect the **user's target region** — the validity analysis evaluates fit-for-purpose, not the benchmark in isolation.

Check if an existing region YAML in `regions/` matches the user's target region.

**If a match exists:** Use the existing region YAML. Proceed to Step 5.

**If no match exists:** Spawn a **Sonnet subagent** to create a new region YAML at `regions/<name>.yaml`. The subagent receives:
- The benchmark name and target region
- The paper summary's relevant sections
- The elicitation summary (for population details, languages, cultural concerns)
- Instructions for required fields (countries, languages, writing systems,
  literacy rates, cultural norms, infrastructure, domain-specific notes)
- Instruction to mark uncertain items with [NEEDS VERIFICATION]

### Step 5: Web search to enrich regional context

This step is critical for addressing recall limitations. Spawn a **Sonnet subagent**
to perform targeted web searches and update the region YAML.

**Guide file:** `.claude/prompts/web_search_guide.md` — this file contains the full search strategy (budget allocation heuristics, per-topic query templates,source priorities, unsearchable-knowledge flags). The subagent reads it as its
operational guide. If the guide is updated in the future, this step requires no changes.

The subagent receives:

1. The full text of `.claude/prompts/web_search_guide.md`
2. The current region YAML
3. The benchmark YAML (task categories, languages, domain)
4. The elicitation summary from Step 2 (deployment context, dimension priority weights, cultural topic priorities, flagged gaps)

The subagent will:

1. Read the web search guide to understand search strategy and budget allocation
2. **Read the benchmark YAML's `coverage_gap_analysis` section first.** This is the primary input for search targeting — it lists exactly where the user's priorities and the benchmark's coverage diverge, with gap types (`full`/`partial`) and suggested search queries. Allocate the majority of the search budget to `full` and `partial` gaps before applying the guide's general heuristics.
3. Use the elicitation summary's **dimension priority weights** and **cultural topic priorities** to further focus budget on the highest-impact areas
4. Use the elicitation summary's **flagged gaps** as secondary search targets — these are areas where the evidence base is thin and web search is most valuable
5. Execute 5-10 targeted web searches, prioritizing coverage gaps over general enrichment
6. Update the region YAML's notes sections with findings, adding a `web_search_enrichment` field documenting searches, findings, and conflicts
7. Write the updated YAML to `regions/<name>.yaml`

### Step 6: Compose the evaluation prompt (SCRIPT)

Before beginning, tag the logging module. Run:

```bash
python3 scripts/pipeline_module.py set prompt_composition
```

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

### Step 7: Run the validity analysis via Opus subagent

Before beginning, tag the logging module. Run:

```bash
python3 scripts/pipeline_module.py set validity_scoring
```

This is the **only Opus call** in the pipeline. Spawn an **Opus subagent**
(use `model: opus` in the Agent tool) with the composed prompt.

In the subagent prompt:

1. Include the full text of the composed prompt from Step 6. (This now includes a "Deployment Context" section with the elicitation summary — the scorer sees the user's use case, target population, dimension priority weights, and flagged gaps as part of the prompt.)

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

### Step 8: Report results (SCRIPT)

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

After the report is printed, close out the logging run:

```bash
python3 scripts/pipeline_module.py end
python3 scripts/summarize_run.py logs/claude-trace.jsonl
```

The first command marks the run as finished. The second writes
`logs/<run_id>_summary.json` with per-module token and tool-call totals.

---

## Important Notes

- **Elicitation runs first, extraction follows.** Steps 1-2 (metadata + elicitation) are fast and involve the user. Steps 3+ are heavy processing that runs unattended. This means the user gives input within the first minute, then can walk away.
- **Thoroughness over speed for extraction.** Step 3 is the most important extraction step. The `/validity-pdf-extract` skill uses per-page Haiku extraction to ensure every page is read without truncation — this is more thorough than the old chunked approach.
- **Extraction is guided by elicitation.** Step 3a passes elicitation dimension priorities to the extraction skill. HIGH-priority dimensions get more detailed narrative; all quotes are still extracted regardless of priority.
- **Quote provenance is structural, not aspirational.** The two-section output format (narrative + quote registry) prevents "evidence laundering." The `verbatim_quotes` YAML field and the Verbatim Quote Registry in the composed prompt are the authoritative evidence chain.
- **Step 3c verification is not optional.** The script handles mechanical checks; the Sonnet subagent handles text spot-checks. Both must pass.
- **Elicitation conditions everything downstream.** Step 2 gathers the user's deployment context. Steps 3, 4, 5, and 7 all consume the elicitation summary. Without it, the pipeline evaluates the benchmark generically rather than for a specific use case.
- **The elicitation guide and web search guide are referenced by file path.** Updating those files changes pipeline behavior without modifying this prompt.
- **Web search is not optional.** Step 5 addresses recall failures — the primary risk in LLM-based validity analysis.
- **Result format matters.** The JSON output must match the project's schema exactly.
- **Model routing is intentional.** Do not upgrade Haiku/Sonnet steps to Opus. The routing is designed to use each model where its capability level suffices.

## Prerequisites

- `/validity-pdf-extract` skill at `.claude/skills/validity-pdf-extract/`
- Python 3 with PyYAML (`pip install pyyaml`)
- pdftk or qpdf for PDF splitting (optional — falls back to Read tool)
- `framework.yaml`, `README.md`, and `prompt_template.md` in project root

## Cost Comparison

| Component | Old (all-Opus) | New (routed) |
|-----------|---------------|--------------|
| Quick metadata | — | Haiku × 1 (pages 1-2 only) |
| Elicitation | — (ran late) | Sonnet × 2-3 (runs early, + 1 more in test mode) |
| PDF extraction | Opus × N chunks | Haiku × N pages + Sonnet × 1 (guided by elicitation) |
| YAML structuring | Opus × 1 | Sonnet × 1 |
| Verification | Opus × 1 | Script + Sonnet × 1 |
| Region creation | Opus × 1 | Sonnet × 1 |
| Web enrichment | Opus × 1 | Sonnet × 1 (guided by elicitation) |
| Prompt composition | Opus × 1 | Script (free) |
| Scoring | Opus × 1 | Opus × 1 |
| Reporting | Opus × 1 | Script (free) |
| **Total Opus calls** | **~6-8** | **1** |
| **Time to user interaction** | **~5-10 min** | **~30 sec** |
