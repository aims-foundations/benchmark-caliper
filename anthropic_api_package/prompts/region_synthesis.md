Produce an assessment-specific region YAML scoped to the target population
described in the elicitation summary.

The user message contains:
- 1-2 selected base template YAMLs (structural and stylistic examples).
- The full elicitation summary (authoritative source for scoping).
- The benchmark YAML (domain, languages, task categories).
- Relevant excerpts from the paper summary.

## Granularity: narrower than the base templates

The base templates in `regions/base/` are **broad regional sketches**
(continent- or language-family-scale, e.g. `east_asia`, `mena`,
`sub_saharan_africa`). The output YAML you produce is **not** another
broad-region template. It describes the specific deployment population
named in the elicitation summary — typically much narrower (one country, a
sub-national cohort, a specific ministry or NGO, a defined occupational
group).

Treat the base templates as structural references, not scope references.
Your output should look like a zoomed-in version of a template: same kind
of fields, but every value narrowed to the deployment population. If the
elicitation scopes to "rural community health workers in western Kenya,"
the output is about them specifically — not about Sub-Saharan Africa in
general. Fields that only make sense at the broader scale (pan-regional
trade blocs, continent-wide literacy averages) get dropped or replaced
with narrower equivalents.

In rare cases the deployment is itself broad (e.g. "any Spanish-speaking
user" with no further scoping). Match the scope the elicitation actually
specifies; don't invent narrowness that isn't there.

## Pipeline context: you are producing a scaffold, not a finished document

A downstream step (step 3) runs another Sonnet call with web search access
that will fill in factual content. **You have no web search and no tools.**
Everything factual you emit comes from parametric knowledge, which is stale
by construction (training-cutoff + sub-national populations + shifting
policy), so even facts you feel confident about are not reliable enough to
ship without verification.

Your job here is to build the best possible scaffold:
- Lay out the right schema for this population (including new fields the
  base templates don't cover).
- Populate the fields that can be grounded in the elicitation summary or
  schema induction directly.
- Leave tagged placeholders for every factual slot a web-search step should
  resolve.

## Core rules

**The provided base template(s) define the schema by example.** Use them as
guides for structure, field depth, and tone — do NOT copy their content
verbatim. Induce the schema from the examples rather than from an explicit
field list. If the elicitation surfaces population characteristics the base
templates do not accommodate (sub-national identity, occupation cohort, age
band, clinical setting, specific regulatory regime, etc.), **add new fields**
rather than dropping the information.

**Fill directly when grounded.** Fields derivable from the elicitation
summary or from obvious structural induction can be written as normal:
- Qualitative framing of the population (who they are, what they do, what
  they care about) — the elicitation summary is authoritative here.
- Field names, nesting, and organization induced from the base template
  schema plus use-case-salient additions.
- Top-level high-confidence categorical facts (primary language, country,
  benchmark domain) where the elicitation has already pinned them down.

**Tag `[NEEDS VERIFICATION]` for everything factual and specific.** Any
value that a future reader should not trust without an external check gets
the tag — not as a value, but as a placeholder in place of the value:

- Quantitative statistics (literacy rates, internet penetration, device
  share, language-share percentages, urbanization %, demographic
  breakdowns).
- Named policies, regulations, standards, platforms (PP 71/2019, specific
  ministerial circulars, platform names, API endpoints, legal thresholds).
- Time-sensitive facts (current-year figures, active programs, recent
  reforms, "as of" claims).
- Sub-national specifics (province-level variation, locally-specific
  procedures, regional office structures) even if the general pattern is
  known.
- Infrastructure specifics (bandwidth figures, mobile-network coverage,
  device model distributions).

Examples:
```yaml
# GOOD — grounded qualitative field, fill directly:
population_description: >
  Indonesian citizens seeking guidance on federal administrative
  procedures (KTP, tax filing, business registration), contacting the
  service primarily via mobile.

# GOOD — factual slot, tag instead of guessing:
literacy_rate: "[NEEDS VERIFICATION]"
mobile_internet_penetration_pct: "[NEEDS VERIFICATION]"
applicable_data_protection_regulation: "[NEEDS VERIFICATION]"

# GOOD — list structure induced from schema, individual facts tagged:
regional_procedural_variation:
  - region: DKI Jakarta
    notes: "[NEEDS VERIFICATION]"
  - region: "[NEEDS VERIFICATION — surface other salient kabupaten/provinces]"
    notes: "[NEEDS VERIFICATION]"

# BAD — parametric-memory number shipped as fact:
literacy_rate: 96
# BAD — confident-sounding but potentially stale regulation name:
applicable_data_protection_regulation: "PP 71/2019"
```

**When in doubt, tag.** Over-tagging at most wastes a web search; under-
tagging ships stale facts into the final assessment. Err toward the former.

**Do not tag fields that don't belong in this assessment.** If a base
template has a field that's irrelevant to the scoped population (e.g. a
`traditional_medicine_practices` field for a deployment about tax filing),
drop it — don't tag it.

**Read-only invariant:** `regions/base/` is never modified. Your output is
a new YAML for `assessments/<benchmark>/<slug>/region.yaml`.

## Output

Output ONLY the YAML document, wrapped in a ```yaml fenced block so it can
be extracted cleanly. No preamble.
