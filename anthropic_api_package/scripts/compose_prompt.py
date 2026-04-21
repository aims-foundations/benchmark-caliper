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
import yaml
from pathlib import Path


def load_yaml(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


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


def format_documentation_excerpts(excerpts) -> str:
    """Format documentation_excerpts sections as markdown.

    Handles both formats:
    - Dict with dimension keys (from optimized pipeline): {input_ontology: "...", ...}
    - Single text string (from repo's benchmark YAMLs): "full text block"
    """
    if isinstance(excerpts, str):
        return excerpts

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
        content = excerpts.get(key, "No documentation available for this dimension.")
        sections.append(f"#### {label}\n\n{content}")
    return "\n\n".join(sections)


def format_region_context(region: dict) -> str:
    """Format region YAML into readable context sections.

    Handles both formats:
    - Repo format: countries as list or dict with primary/extended, languages as
      dict with major/variants keys
    - Pipeline format: countries as dict with primary/extended, languages as list
      of dicts with name/notes
    """
    parts = []

    # Countries — handle list, dict with primary/extended, or plain list
    countries = region.get("countries", {})
    if countries:
        if isinstance(countries, dict):
            primary = countries.get("primary", [])
            extended = countries.get("extended", [])
            if isinstance(primary, list):
                parts.append(f"**Countries**: {', '.join(primary)}")
            if isinstance(extended, list) and extended:
                parts.append(f"**Extended region**: {', '.join(extended)}")
        elif isinstance(countries, list):
            parts.append(f"**Countries**: {', '.join(countries)}")

    # Languages — handle dict with major/variants, list of dicts, or list of strings
    languages = region.get("languages", [])
    if languages:
        lang_strs = []
        if isinstance(languages, dict):
            # Dict format: {major: [...], variants/varieties: [...], note: "..."}
            for lang in languages.get("major", []):
                if isinstance(lang, dict):
                    name = lang.get("name", lang.get("language", str(lang)))
                    code = lang.get("code", "")
                    notes = lang.get("notes", "")
                    entry = f"- {name}"
                    if code:
                        entry += f" ({code})"
                    if notes:
                        entry += f": {notes}"
                    lang_strs.append(entry)
                else:
                    lang_strs.append(f"- {lang}")
            # Handle both 'variants' (repo) and 'varieties' (pipeline)
            variants = languages.get("variants", languages.get("varieties", []))
            if variants:
                lang_strs.append("\n**Language varieties**:")
                for v in variants:
                    if isinstance(v, dict):
                        name = v.get("variety", v.get("name", str(v)))
                        code = v.get("code", "")
                        notes = v.get("notes", "")
                        entry = f"- {name}"
                        if code:
                            entry += f" ({code})"
                        if notes:
                            entry += f": {notes}"
                        lang_strs.append(entry)
                    else:
                        lang_strs.append(f"- {v}")
            note = languages.get("note", "")
            if note:
                lang_strs.append(f"\n*Note: {note}*")
        elif isinstance(languages, list):
            for lang in languages:
                if isinstance(lang, dict):
                    # Handle both {name: ..., notes: ...} and {language: ..., code: ..., notes: ...}
                    name = lang.get("name", lang.get("language", str(lang)))
                    code = lang.get("code", "")
                    notes = lang.get("notes", "")
                    entry = f"- {name}"
                    if code:
                        entry += f" ({code})"
                    if notes:
                        entry += f": {notes}"
                    lang_strs.append(entry)
                else:
                    lang_strs.append(f"- {lang}")
        parts.append("**Languages**:\n" + "\n".join(lang_strs))

    # Writing systems — handle list of strings or list of dicts with note
    ws = region.get("writing_systems", [])
    if ws:
        if isinstance(ws, list):
            ws_strs = [item if isinstance(item, str) else str(item) for item in ws]
            parts.append(f"**Writing systems**: {', '.join(ws_strs)}")
        ws_note = region.get("writing_systems", {})
        if isinstance(ws_note, dict) and ws_note.get("note"):
            parts.append(f"*Note: {ws_note['note']}*")

    # Literacy rates — handle dict {country: rate}, list of {country, rate} dicts
    literacy = region.get("literacy_rates", {})
    if literacy:
        if isinstance(literacy, list):
            # Pipeline format: [{country: "Spain", rate: "98%"}, ...]
            rates = [f"- {item.get('country', '?')}: {item.get('rate', '?')}"
                     if isinstance(item, dict) else f"- {item}"
                     for item in literacy]
            parts.append("**Literacy rates**:\n" + "\n".join(rates))
        elif isinstance(literacy, dict):
            # Repo format: {Spain: 0.98, Portugal: 0.96, ...}
            rates = [f"- {k}: {v}" for k, v in literacy.items()]
            parts.append("**Literacy rates**:\n" + "\n".join(rates))
        else:
            parts.append(f"**Literacy rates**: {literacy}")

    # Notes sections
    for field, label in [
        ("cultural_norms_notes", "Cultural Norms"),
        ("infrastructure_notes", "Infrastructure"),
        ("domain_specific_notes", "Domain-Specific Notes"),
    ]:
        val = region.get(field, "")
        if val:
            parts.append(f"**{label}**:\n\n{val}")

    # Web search enrichment — handle both formats
    enrichment = region.get("web_search_enrichment", {})
    if enrichment:
        parts.append("**Web Search Enrichment**:")

        # Pipeline format: searches_performed as list of {query, key_findings} dicts
        searches = enrichment.get("searches_performed", [])
        if searches:
            for s in searches:
                if isinstance(s, dict):
                    q = s.get("query", "")
                    f = s.get("key_findings", "")
                    parts.append(f"- **Search**: {q}\n  **Findings**: {f}")
                else:
                    parts.append(f"- {s}")

        # Repo format: queries_performed as list of strings, key_findings as list
        queries = enrichment.get("queries_performed", [])
        if queries and not searches:
            parts.append("Searches performed:\n" + "\n".join(f"- {q}" for q in queries))
        findings = enrichment.get("key_findings", [])
        if findings:
            parts.append("Key findings:\n" + "\n".join(f"- {f}" for f in findings))

        conflicts = enrichment.get("conflicting_information", [])
        if conflicts:
            parts.append("\nConflicting information:\n" + "\n".join(f"- {c}" for c in conflicts))

    # Fallback: if none of the expected flat-schema top-level keys matched
    # (e.g. the synthesis step produced a nested, deployment-specific schema),
    # dump the full YAML so downstream scoring still sees the regional data.
    if not parts:
        dumped = yaml.dump(region, sort_keys=False, allow_unicode=True,
                           default_flow_style=False)
        return f"```yaml\n{dumped}```"

    return "\n\n".join(parts)


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
                if isinstance(item, dict):
                    item_id = item.get("id", "")
                    item_text = item.get("text", str(item))
                    parts.append(f"- [{item_id}] {item_text}")
                else:
                    parts.append(f"- {item}")
        parts.append("")
    return "\n".join(parts)


def load_text(path: str) -> str:
    """Load a text file and return its contents."""
    return Path(path).read_text(encoding="utf-8")


def compose_prompt(benchmark: dict, region: dict, framework: dict,
                   elicitation_text: str = "",
                   region_name_override: str = "") -> str:
    """Compose the full evaluation prompt."""

    # Extract benchmark fields
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

    # Scoring rubric from framework
    rubric = framework.get("scoring_rubric", "")
    if isinstance(rubric, dict):
        rubric_lines = []
        for score, desc in sorted(rubric.items()):
            rubric_lines.append(f"- **{score}**: {desc}")
        rubric = "\n".join(rubric_lines)

    prompt = f"""I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **{bm_full}** is valid for use in **{region_name}**.

Analyze the benchmark documentation and regional context below against each of the 6 validity dimensions. For each dimension, assign a score (1-5), provide justification with evidence quotes, respond to each checklist item, and identify information gaps.

### Critical Constraints

- **Document-grounded only**: Base your analysis ONLY on evidence found in the provided benchmark documentation and the factual regional context given. Do NOT role-play as a member of the target culture or speculate beyond what the documentation supports.
- **Cite evidence**: For each finding, quote or reference specific parts of the benchmark documentation.
- **Flag gaps explicitly**: When information is missing from the documentation, say "INSUFFICIENT DOCUMENTATION" and describe what would be needed.
- **Distinguish documentable vs. expert-needed**: Classify each finding as either (a) determinable from documentation, or (b) requiring regional expert verification.
- **Regional specificity**: Evaluate validity *for the specified target region*, not in general.
- **Conservative scoring**: When evidence is ambiguous or insufficient, score lower rather than higher.

### Scoring Rubric

{rubric}

### Quote Provenance Rules

The benchmark documentation below contains two types of text:

- **Verbatim quotes** from the original paper, listed in the "Verbatim Quote Registry"
  section with IDs (Q1, Q2, ...), page numbers, and exact text. These are
  **authoritative evidence** extracted directly from the PDF.
- **Interpretive context** in the "Benchmark Documentation" section, written by the
  extraction pipeline. This provides useful framing and references quote IDs like
  [Q3], but is NOT evidence from the paper itself.

When populating `evidence_quotes` in your output JSON:
- ONLY include text from the Verbatim Quote Registry
- Format each entry as: `"[QN] 'exact quote text' (p.X)"`
- Do NOT cite interpretive context as if it were from the paper
- If you cannot find a verbatim quote to support a finding, state this explicitly
  rather than citing paraphrased text

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

## Target Region

- **Name**: {region_name}

### Regional Context

{format_region_context(region)}

---

## Deployment Context

{elicitation_text if elicitation_text else "_No deployment context provided. Evaluate the benchmark's general validity for the target region._"}

---

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
      "score": "<1-5>",
      "justification": "...",
      "checklist_responses": {{ "IO-1": "...", "IO-2": "..." }},
      "evidence_quotes": ["[Q1] 'quote text' (p.7)", ...],
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
  "remediation_suggestions": "...",
  "highest_concern_dimensions": ["..."],
  "strongest_dimensions": ["..."]
}}
```
"""
    return prompt


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
    args = parser.parse_args()

    benchmark = load_yaml(args.benchmark)
    region = load_yaml(args.region)
    framework = load_yaml(args.framework)

    elicitation_text = ""
    if args.elicitation:
        elicitation_text = load_text(args.elicitation)

    prompt = compose_prompt(benchmark, region, framework, elicitation_text,
                            region_name_override=args.region_name)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(prompt, encoding="utf-8")

    print(f"Composed prompt written to {args.output}")
    print(f"  Benchmark: {benchmark.get('name', 'unknown')}")
    print(f"  Region:    {region.get('name') or args.region_name or 'unknown'}")
    print(f"  Quotes:    {len(benchmark.get('verbatim_quotes', []))}")
    char_count = len(prompt)
    print(f"  Prompt size: {char_count:,} chars (~{char_count // 4:,} tokens)")


if __name__ == "__main__":
    main()
