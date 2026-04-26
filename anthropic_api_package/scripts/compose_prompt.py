#!/usr/bin/env python3
"""compose_prompt.py — Assemble the evaluation prompt from YAML artifacts.

Replaces the LLM-based Step 4 with deterministic template filling.
Reads benchmark YAML, region YAML, and framework YAML, then composes the
self-contained evaluation prompt that gets sent to the scoring model.

Usage:
    python3 scripts/compose_prompt.py \\
        --benchmark benchmarks/<name>.yaml \\
        --region regions/<name>.yaml \\
        --framework framework.yaml \\
        --template prompt_template.md \\
        --output .claude/prompts/<name>/variant_a_neutral.md

All quote provenance rules are baked into the template — no LLM judgment needed.
"""

import argparse
import re
import yaml
from pathlib import Path


# Load a YAML file and return its contents as a dict
def load_yaml(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# Render the verbatim_quotes list from a benchmark YAML as a markdown table.
# Pipe characters in quote text are escaped so they don't break the table.
def format_quote_table(quotes: list[dict]) -> str:
    """Format verbatim_quotes as a markdown table."""
    rows = ["| ID | Page | Dimension | Text |", "|----|------|-----------|------|"]
    for q in quotes:
        qid = q.get("id", "")
        page = q.get("page", "")
        dim = q.get("dimension", "")
        text = q.get("text", "").replace("|", "\\|")
        rows.append(f'| {qid} | {page} | {dim} | "{text}" |')
    return "\n".join(rows)


# Render benchmark documentation excerpts as readable markdown.
# Handles two schemas that coexist in the repo: a per-dimension dict (produced
# by the optimized pipeline) and a legacy single text block (from hand-curated YAMLs).
def format_documentation_excerpts(excerpts) -> str:
    """Format documentation_excerpts sections as markdown.

    Handles both formats:
    - Dict with dimension keys (from optimized pipeline): {input_ontology: "...", ...}
    - Single text string (from repo's benchmark YAMLs): "full text block"
    """
    # Legacy format: the entire documentation block is already a formatted string
    if isinstance(excerpts, str):
        return excerpts

    # Canonical display names for the 6 validity dimensions
    dim_labels = {
        "input_ontology": "Input Ontology",
        "input_content": "Input Content",
        "input_form": "Input Form",
        "output_ontology": "Output Ontology",
        "output_content": "Output Content",
        "output_form": "Output Form",
    }
    sections = []
    for key, label in dim_labels.items():
        # Fall back to a neutral placeholder so the section still appears in the
        # composed prompt — an empty section would confuse the scoring model.
        content = excerpts.get(key, "No documentation available for this dimension.")
        sections.append(f"#### {label}\n\n{content}")
    return "\n\n".join(sections)


# Serialize the region dict as a fenced YAML block, replacing raw URLs with
# compact WEB-N citation IDs so the scoring model sees tidy references.
def format_region_yaml(region: dict, registry: list[dict]) -> str:
    """Dump region dict as fenced YAML, replacing [|url|] with [WEB-N] IDs."""
    dumped = yaml.dump(region, sort_keys=False, allow_unicode=True,
                       default_flow_style=False)
    if registry:
        dumped = inject_web_ids(dumped, registry)
    return f"```yaml\n{dumped}```"


# Regex to match the [|url|] delimiter used by the research pipeline to embed
# web source URLs inline within region YAML string values.
_URL_DELIM_RE = re.compile(r"\[\|([^|]+)\|\]")


# Walk the entire region dict recursively and collect all [|url|] sources into
# a deduplicated registry with stable WEB-N IDs. Order reflects first appearance
# in the YAML (depth-first dict traversal), which is deterministic.
def extract_web_source_registry(region: dict) -> list[dict]:
    """Walk the region dict and extract all [|url|] delimited sources.

    Returns a list of {id: "WEB-1", url: "https://..."} dicts, deduplicated
    by URL in order of first appearance.
    """
    seen_urls: dict[str, int] = {}
    registry: list[dict] = []

    def _walk(obj):
        if isinstance(obj, str):
            for m in _URL_DELIM_RE.finditer(obj):
                url = m.group(1).strip()
                # First occurrence wins; subsequent duplicates reuse the same ID
                if url not in seen_urls:
                    idx = len(registry) + 1
                    seen_urls[url] = idx
                    registry.append({"id": f"WEB-{idx}", "url": url})
        elif isinstance(obj, dict):
            for v in obj.values():
                _walk(v)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item)

    _walk(region)
    return registry


# Swap every [|url|] occurrence in a YAML string for its assigned WEB-N label.
# If a URL somehow isn't in the registry (shouldn't happen), leave the original
# match unchanged to avoid silently dropping information.
def inject_web_ids(yaml_text: str, registry: list[dict]) -> str:
    """Replace [|url|] with [WEB-N] in the YAML text for the composed prompt."""
    url_to_id = {entry["url"]: entry["id"] for entry in registry}

    def _replace(m):
        url = m.group(1).strip()
        # Fall back to the original token if the URL wasn't registered
        wid = url_to_id.get(url, m.group(0))
        return f"[{wid}]"

    return _URL_DELIM_RE.sub(_replace, yaml_text)


# Render the web source registry as a two-column markdown table mapping
# WEB-N IDs back to their full URLs — gives the scoring model a lookup table.
def format_web_source_registry(registry: list[dict]) -> str:
    """Format web source registry as a markdown table."""
    if not registry:
        return "_No web sources cited._"
    rows = ["| ID | URL |", "|----|-----|"]
    for entry in registry:
        rows.append(f"| {entry['id']} | {entry['url']} |")
    return "\n".join(rows)


# Strip redundant sections from the elicitation summary so the composed prompt
# doesn't repeat information already present in the region YAML (Use Case,
# Target Population, Flagged Gaps). Only the scored responses and priority
# weights are novel signal for the scoring model.
def filter_elicitation(text: str) -> str:
    """Keep only Elicitation Responses and Dimension Priority Weights.

    Use Case, Target Population, and Flagged Gaps are already captured in
    the region YAML and would be redundant in the composed prompt.
    """
    keep = {"Elicitation Responses", "Dimension Priority Weights"}
    result = []
    current_heading = None
    current_lines: list[str] = []

    # State-machine pass over H2 sections: accumulate lines per heading,
    # flush to result only when the heading is in the keep-list.
    for line in text.splitlines():
        if line.startswith("## "):
            if current_heading in keep:
                result.extend(current_lines)
            current_heading = line[3:].strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    # Flush the final section, which has no following H2 to trigger the flush
    if current_heading in keep:
        result.extend(current_lines)

    # If nothing matched (unexpected elicitation format), return the full text
    # rather than an empty string to avoid silently dropping content.
    return "\n".join(result).strip() if result else text


# Render the framework's dimension definitions and checklists as markdown.
# The checklist items may be plain strings or {id, text} dicts depending on
# which version of framework.yaml is in use.
def format_framework_dimensions(framework: dict) -> str:
    """Format framework dimensions and checklists.

    Matches prompt_template.md structure: definition + theoretical importance + checklist.
    Uses 'definition' field from framework.yaml (not 'description').
    """
    dims = framework.get("dimensions", {})
    parts = []
    for dim_key, dim_data in dims.items():
        name = dim_data.get("name", dim_key)
        # framework.yaml uses 'definition', not 'description'
        definition = dim_data.get("definition", dim_data.get("description", ""))
        theoretical = dim_data.get("theoretical_importance", "")

        parts.append(f"### {name}")
        parts.append(f"\n**Definition**: {definition.strip()}")
        if theoretical:
            parts.append(f"\n**Theoretical Importance**: {theoretical.strip()}")

        checklist = dim_data.get("checklist", [])
        if checklist:
            parts.append("\n**Checklist:**")
            for item in checklist:
                # Newer framework versions use structured {id, text} dicts;
                # older versions store plain strings directly.
                if isinstance(item, dict):
                    item_id = item.get("id", "")
                    item_text = item.get("text", str(item))
                    parts.append(f"- [{item_id}] {item_text}")
                else:
                    parts.append(f"- {item}")
        parts.append("")
    return "\n".join(parts)


# Read a plain text or markdown file; thin wrapper kept for callsite clarity.
def load_text(path: str) -> str:
    """Load a text file and return its contents."""
    return Path(path).read_text(encoding="utf-8")


# Central assembly function: merges all artifact data into a single markdown
# prompt string that the scoring model (Opus) receives verbatim.
# Returns the fully composed prompt as a string (caller writes it to disk).
def compose_prompt(benchmark: dict, region: dict, framework: dict,
                   elicitation_text: str = "",
                   region_name_override: str = "",
                   dataset_analysis_text: str = "") -> str:
    """Compose the full evaluation prompt."""

    # === Extract benchmark metadata ===
    bm_name = benchmark.get("name", "unknown")
    bm_full = benchmark.get("full_name", bm_name)
    bm_domain = benchmark.get("domain", "")
    bm_langs = ", ".join(benchmark.get("languages", []))
    bm_porting = benchmark.get("porting_strategy", "")
    bm_year = benchmark.get("year", "")

    excerpts = benchmark.get("documentation_excerpts", {})
    quotes = benchmark.get("verbatim_quotes", [])

    # Prefer top-level YAML `name`, then CLI override (deployment slug),
    # then the literal "unknown" as a last resort.
    region_name = region.get("name") or region_name_override or "unknown"

    # === Format scoring rubric ===
    # Rubric may be either a plain string (copy-paste from framework doc) or a
    # dict keyed by integer score — both are normalised to a bullet list.
    rubric = framework.get("scoring_rubric", "")
    if isinstance(rubric, dict):
        rubric_lines = []
        for score, desc in sorted(rubric.items()):
            rubric_lines.append(f"- **{score}**: {desc}")
        rubric = "\n".join(rubric_lines)

    # === Build web source registry ===
    # URLs are extracted from the region dict once here and reused for both
    # the YAML block (inline [WEB-N] injection) and the separate registry table.
    web_registry = extract_web_source_registry(region)

    # === Assemble the static header and evidence sections ===
    # This block is always present regardless of optional inputs.
    prompt = f"""I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **{bm_full}** is valid for use in **{region_name}**.

Analyze the evidence sources below against each of the 6 validity dimensions. For each dimension, assign a score (1-5), provide justification with cited evidence, respond to each checklist item, and identify information gaps.

### Critical Constraints

- **Evidence-grounded only**: Base your analysis ONLY on the three evidence sources provided: (1) benchmark documentation with verbatim quotes, (2) regional context with web-sourced findings, and (3) dataset analysis findings with datapoint citations (if present). Do NOT role-play as a member of the target culture or speculate beyond what these sources support.
- **Cite evidence**: For each finding, cite at least one source — a verbatim quote `[QN]`, a web source `[WEB-N]`, or a dataset citation `DATASET-D{{n}}`.
- **Flag gaps explicitly**: When none of the three evidence sources addresses a checklist item, say "INSUFFICIENT DOCUMENTATION" and describe what would be needed.
- **Distinguish documentable vs. expert-needed**: Classify each finding as either (a) determinable from documentation, or (b) requiring regional expert verification.
- **Regional specificity**: Evaluate validity *for the specified target region*, not in general.
- **Conservative scoring**: When evidence is ambiguous or insufficient, score lower rather than higher.

### Scoring Rubric

{rubric}

### Evidence Sources

The prompt below contains three evidence sources:

1. **Benchmark Documentation** + **Verbatim Quote Registry** — paper content, with authoritative quotes labeled `[QN]`
2. **Regional Context** (YAML) + **Web Source Registry** — deployment context with web research findings cited as `[WEB-N]`
3. **Dataset Analysis Findings** (if present) — empirical observations from the benchmark's HuggingFace data, cited as `DATASET-D{{n}}`

Citation rules for each source are in your system instructions.

---

## Benchmark Information

- **Name**: {bm_name}
- **Full Name**: {bm_full}
- **Domain**: {bm_domain}
- **Languages**: {bm_langs}
- **Porting Strategy**: {bm_porting}
- **Year**: {bm_year}

### Benchmark Documentation

{format_documentation_excerpts(excerpts)}

### Verbatim Quote Registry

{format_quote_table(quotes)}

---

## Regional Context

{format_region_yaml(region, web_registry)}

### Web Source Registry

{format_web_source_registry(web_registry)}

---

## Expert Elicitation

{filter_elicitation(elicitation_text) if elicitation_text else "_No elicitation responses provided. Evaluate the benchmark's general validity for the target region._"}

---
"""

    # === Append dataset analysis section (optional) ===
    # Only included when a dataset analysis report was generated (Step 5b).
    # The DATASET-D{n} citation format is explained here so the scoring model
    # knows how to reference specific datapoints.
    if dataset_analysis_text:
        prompt += f"""
## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{{n}}` IDs (e.g., QUAERO-D3). Findings tagged CRITICAL
should be treated as strong evidence for lower scores on the affected dimensions.

{dataset_analysis_text}

---
"""

    # === Append framework dimensions and required JSON output schema ===
    # The output schema is hardcoded here (not in a template file) because it
    # mirrors the exact fields that downstream report generation expects.
    prompt += f"""
## Framework Dimensions to Evaluate

{format_framework_dimensions(framework)}

---

## Required Output Format

Output a single valid JSON object with this structure:

```json
{{
  "benchmark": "{bm_name}",
  "region": "{region_name}",
  "dimensions": {{
    "input_ontology": {{
      "score": "<integer 1-5>",
      "justification": "...",
      "strengths": ["what this dimension captures well for the target context"],
      "checklist_responses": {{ "IO-1": "...", "IO-2": "..." }},
      "evidence_quotes": ["[Q1] 'quote text' (p.7)", ...],
      "evidence_web_sources": ["[WEB-1] literacy rate 96%", ...],
      "evidence_dataset": ["DATASET-D1: observation", ...],
      "evidence_map": {{ "IO-1": ["Q1", "WEB-3"], "IO-2": ["DATASET-D1"] }},
      "confidence": "<high|medium|low>",
      "information_gaps": ["..."],
      "requires_expert_verification": ["..."]
    }},
    "input_content": {{ "..." }},
    "input_form": {{ "..." }},
    "output_ontology": {{ "..." }},
    "output_content": {{ "..." }},
    "output_form": {{ "..." }}
  }},
  "overall_summary": "...",
  "risk_assessment": "<high|medium|low>",
  "practical_guidance": {{
    "what_this_benchmark_measures": "...",
    "construct_depth": "...",
    "supplementation_needed": "..."
  }},
  "remediation_suggestions": [
    {{ "dimension": "...", "gap": "...", "recommendation": "..." }}
  ],
  "highest_concern_dimensions": ["..."],
  "strongest_dimensions": ["..."]
}}
```
"""
    return prompt


# CLI entry point: parse arguments, load artifacts, compose and write the prompt.
def main():
    parser = argparse.ArgumentParser(description="Compose evaluation prompt from YAML artifacts")
    parser.add_argument("--benchmark", required=True, help="Path to benchmark YAML")
    parser.add_argument("--region", required=True, help="Path to region YAML")
    parser.add_argument("--framework", required=True, help="Path to framework YAML")
    parser.add_argument("--output", required=True, help="Output path for composed prompt")
    # --template is accepted but not used (template is built into this script)
    parser.add_argument("--template", required=False, help="(unused, template is built-in)")
    parser.add_argument("--elicitation", required=False,
                        help="Path to elicitation summary markdown (from Step 2)")
    parser.add_argument("--region-name", required=False, default="",
                        help="Human-readable region name to use when the region "
                             "YAML has no top-level `name` field (e.g. the "
                             "deployment slug).")
    parser.add_argument("--dataset-analysis", required=False,
                        help="Path to dataset analysis report markdown (from Step 5b)")
    args = parser.parse_args()

    # === Load YAML artifacts ===
    benchmark = load_yaml(args.benchmark)
    region = load_yaml(args.region)
    framework = load_yaml(args.framework)

    # === Load optional text inputs ===
    elicitation_text = ""
    if args.elicitation:
        elicitation_text = load_text(args.elicitation)

    dataset_analysis_text = ""
    if args.dataset_analysis:
        dataset_analysis_text = load_text(args.dataset_analysis)

    # === Compose prompt and write to disk ===
    prompt = compose_prompt(benchmark, region, framework, elicitation_text,
                            region_name_override=args.region_name,
                            dataset_analysis_text=dataset_analysis_text)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(prompt, encoding="utf-8")

    # === Print summary for quick sanity-check at the terminal ===
    print(f"Composed prompt written to {args.output}")
    print(f"  Benchmark: {benchmark.get('name', 'unknown')}")
    print(f"  Region:    {region.get('name') or args.region_name or 'unknown'}")
    print(f"  Quotes:    {len(benchmark.get('verbatim_quotes', []))}")
    # Re-extract the registry here only for the count — the registry used inside
    # compose_prompt was already built from the same region dict.
    web_sources = len(extract_web_source_registry(region))
    print(f"  Web srcs:  {web_sources}")
    print(f"  DA report: {'included' if dataset_analysis_text else 'not included'}")
    char_count = len(prompt)
    print(f"  Prompt size: {char_count:,} chars (~{char_count // 4:,} tokens)")


if __name__ == "__main__":
    main()
