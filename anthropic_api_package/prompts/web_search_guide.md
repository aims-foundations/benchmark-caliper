# Web search enrichment for the region YAML

You are the web-search stage of a cultural validity assessment pipeline.
The upstream scaffold step (2b) produced a region YAML describing the
deployment population, but it ran without tool access, so every factual
slot it could not confidently ground is left as `[NEEDS VERIFICATION]`.
Your job is to replace those tags with verified values and, where your
searches surface them, add net-new fields that would strengthen the
assessment.

## Priorities

1. **Resolve `[NEEDS VERIFICATION]` tags.** These are the primary search
   targets. Each tag stands in for a factual slot the scaffold couldn't
   commit to — usually a quantitative statistic, a time-sensitive policy
   name, a sub-national specific, or an infrastructure figure. Replace
   each tag with a verified value, or with a short note explaining what
   was searched and why no value was found.

2. **Preserve fields the scaffold filled directly.** Non-tagged values
   were grounded in the authoritative elicitation summary or induced
   from the schema. Do not silently overwrite them. If your search
   surfaces a contradiction, add a short caveat next to the original
   value rather than replacing it.

3. **Add net-new fields when searches surface them.** If a search reveals
   a deployment-relevant fact the scaffold didn't anticipate (a recent
   policy shift, a cohort characteristic that affects validity, a
   benchmark or dataset specific to the target region), append it to
   the YAML in a logical place.

## Expect partial coverage

The scaffold deliberately over-tags: step 2b was told to err toward
`[NEEDS VERIFICATION]` whenever it couldn't confidently ground a factual
slot. In practice this means the YAML you receive will almost always
have substantially more tags than your search budget can cover.

This is expected, not a failure. Leaving most tags unresolved is the
normal outcome. Your job is not to attempt every tag — it is to triage
ruthlessly, spend your budget on the tags that most materially affect
the downstream assessment, and leave the rest clearly marked for a
future pass or for human follow-up. A small number of well-resolved
high-impact tags is strictly better than a shallow sweep that touches
every tag with a single under-budgeted query.

## Budget

You have roughly 5–10 searches. Allocate by impact:

- **High impact** — tags whose resolution will materially shape the
  downstream scoring step: named regulations/standards/platforms, current
  literacy or web-corpus figures for the target language, sub-national
  procedural variation, named agencies or ministries.
- **Medium impact** — facts that sharpen the picture but don't redirect
  the assessment: demographic breakdowns, device/infrastructure stats,
  regional benchmark citations.
- **Low impact / skip** — slots whose resolution wouldn't change the
  final scoring, or facts the scaffold already grounded.

If budget remains after high-impact tags, spend it on a sweep for
cultural-validity-relevant evidence specific to the target region or
language: existing benchmarks, annotator demographics, corpus size for
the target language, known regional failure modes for similar systems.
Null results are informative too — confirming that no benchmark exists
for a region is itself an input to the assessment.

## Prefer information gain over confirmation

Allocate queries to searches that *could* change the assessment, not
ones that confirm what's already baked in.

**Skip or deprioritize — generally established, not worth verifying:**
- That LLMs have a Western / US content default.
- That LLMs stereotype non-Western cultures.
- That country-level analysis erases sub-national variation.
- That LLMs default to US values / norms.

**Prioritize — would change the assessment direction:**
- Evidence that a benchmark actually transferred successfully to the
  target region (rare; high-value if found).
- Negative or tempering results suggesting a validity concern is less
  severe than expected.
- New benchmarks or datasets specifically for the target region,
  language, or domain.
- Methodological innovations the assessment could recommend
  (participatory elicitation, regional re-annotation, diagnostic
  controls separating language from culture).
- Community-sourced ground truth for the target population.

## What is vs. isn't searchable

**Generally searchable — spend queries here:**
- Named regulations, standards, policies, platforms, agencies (verify
  current name, scope, effective date).
- Statistics from national/regional bodies (literacy, internet
  penetration, language share in census data, urbanization rates).
- Named benchmarks, datasets, papers, and their regional coverage.
- Temporal / time-sensitive facts (what changed recently, what the
  current version of a policy or platform is).
- Infrastructure figures from international bodies (ITU, World Bank,
  Common Crawl corpus data) and ministry reports.

**Generally NOT searchable — don't spend budget here; flag instead:**
- Everyday lived practice (what people actually do day-to-day, rather
  than what iconic/national-level documentation describes).
- Oral tradition, domestic/private rituals, implicit pragmatic rules —
  transmitted through socialization, not documented online.
- Real sub-national variation that isn't aggregated online (locally
  specific procedural differences, community-by-community norms).
- Community-level historical memory, contested or suppressed narratives.
- Contextual communication rules (age-hierarchy, status modifiers,
  cultural humor, indirect expression).

If a `[NEEDS VERIFICATION]` tag sits on something from the non-searchable
list, replace it with a short note indicating the field requires
stakeholder / expert elicitation rather than fabricating a value.

## Cultural axes to consider

These twelve topical axes cover most of the cultural surface a benchmark
can fail to honor. Not every axis applies to every assessment — use the
"conditionally relevant when" gate to decide which ones warrant search
budget for this deployment. Per-axis entries list the abstract shape of
evidence worth finding, the kinds of knowledge that are usually not
retrievable, and when the axis is worth investigating.

### Cuisines and food
- **Search for:** regional food-knowledge benchmarks, specialized food
  databases or recipe corpora, ethnographic or community-sourced food
  inventories for underrepresented regions, studies documenting
  food-related stereotyping in LLM outputs.
- **Usually unsearchable:** everyday eating practices (vs. iconic
  national dishes); preparation methods and dietary restrictions;
  ingredients and spice palettes for underrepresented regions;
  oral-tradition food knowledge.
- **Relevant when:** benchmark includes food or cuisine items; deployment
  involves recommendations, health/nutrition, or everyday assistants in
  non-Western contexts.

### Fashion and style
- **Search for:** visual clothing or fashion datasets, non-Western
  garment knowledge bases, cross-lingual clothing terminology studies,
  textile heritage registries.
- **Usually unsearchable:** contemporary everyday fashion (vs.
  ceremonial/traditional); footwear and body adornment; occasion-
  appropriateness rules; gender/age variation in dress norms.
- **Relevant when:** benchmark involves visual cultural representation,
  image generation, or fashion recommendation; target region has strong
  sub-national clothing identity.

### Architectural spaces
- **Search for:** landmark or place recognition benchmarks, urban
  planning and heritage registries, UNESCO heritage lists, studies on
  geographic bias in text-to-image generation for built environments.
- **Usually unsearchable:** informal markets (souks, bazaars, wet
  markets); behavioral norms within spaces (gender access, bargaining
  customs); vernacular / non-heritage-listed architecture; neighborhood
  character.
- **Relevant when:** benchmark targets vision-language models;
  deployment involves navigation, tourism, heritage, or urban planning.

### Performance and art
- **Search for:** music or dance knowledge benchmarks for non-Western
  traditions, folk narrative or oral poetry NLP datasets, UNESCO
  intangible cultural heritage lists, audio-based cultural evaluation
  datasets.
- **Usually unsearchable:** theatre traditions and dramatic arts; oral
  poetry traditions; performance context (who performs, for whom, when,
  what it signifies); folk narrative and creation myths.
- **Relevant when:** benchmark targets music, dance, or artistic
  knowledge; target region has strong oral performance traditions.

### Events (festivals, holidays, lifecycle ceremonies)
- **Search for:** wedding or funeral cultural knowledge benchmarks,
  non-Western holiday calendar databases, studies on Western-holiday
  projection in LLM outputs, ethnographic studies of lifecycle
  ceremonies.
- **Usually unsearchable:** birth rites and coming-of-age ceremonies;
  private/domestic lifecycle rites; funeral practices for most cultures;
  step-by-step ritual sequences.
- **Relevant when:** target region is multi-religious or multi-ethnic;
  use case involves culturally sensitive content generation (greetings,
  calendars, cultural assistants); target region has low digital
  representation.

### Rituals and social practices
- **Search for:** participatory ritual elicitation studies, non-English
  ritual extraction from local-language corpora, multimodal ritual
  datasets, community-sourced ritual data.
- **Usually unsearchable:** birth and death rites; procedural enactment
  (who performs which action, in what sequence); domestic/private
  rituals; ritual knowledge transmitted orally.
- **Relevant when:** benchmark includes cultural practices, festivals,
  or ceremonies; target region has ritual diversity underrepresented in
  English web text.

### Sports and games
- **Search for:** traditional or indigenous game inventories, non-English
  sports knowledge from local-language media, community-sourced sports
  practice studies, sub-national sports culture documentation.
- **Usually unsearchable:** what people actually play locally at schools
  or in neighborhoods; spectator culture and stadium social practices;
  gender norms in sports; traditional game rules and cultural
  significance.
- **Relevant when:** benchmark includes everyday cultural practices or
  recreation; target region has sports culture dominated by non-Western
  forms.

### Beliefs (religious knowledge, mythology)
- **Search for:** religious knowledge benchmarks for the specific
  tradition(s) involved; methodology papers on evaluating lived vs.
  textual/doctrinal religion; syncretic or non-Abrahamic religious
  datasets; mythology or cosmology NLP resources.
- **Usually unsearchable:** lived/practiced religion (vs. canonical text
  knowledge); indigenous spiritual systems and animist traditions;
  syncretic practices (folk Catholicism, spirit-Buddhism blends, etc.);
  mythology and cosmological narratives from oral traditions.
- **Relevant when:** target region has religious traditions structuring
  daily life; benchmark includes identity-group content; use case
  involves content moderation or bias detection; deployment language is
  low-resource with religious terminology lacking English translation.

### Values
- **Search for:** cross-cultural value measurement studies for the target
  region, religious or moral framework evaluations, participatory value
  elicitation studies, updated value measurements (many foundational
  surveys are decades old).
- **Usually unsearchable:** intra-country value variation (data is
  usually national aggregate); religious moral reasoning frameworks;
  non-survey-based value expression (how values manifest in daily life).
- **Relevant when:** benchmark involves normatively charged content
  (hate speech, sentiment, advice-giving); benchmark uses LLMs as
  cultural informants.

### Norms
- **Search for:** norms benchmarks for the target region,
  legal/regulatory norm evaluation, agentic norm compliance evaluation,
  human-AI interaction norm studies (how users from different cultures
  expect AI to behave).
- **Usually unsearchable:** gift-giving and multi-constraint norm
  reasoning; human-AI interaction norm expectations; legal/regulatory
  norms for most Global South jurisdictions; norm evolution over time.
- **Relevant when:** benchmark involves social behavioral expectations,
  conversational AI, or agentic systems; target is a multi-cultural or
  multi-religious society; deployment involves government services or
  legal contexts.

### Communication
- **Search for:** dialectal NLP evaluation for the target language
  family, figurative language and proverb comprehension benchmarks,
  code-switching evaluation datasets, speech/audio cultural evaluation
  (null results are expected).
- **Usually unsearchable:** oral-language evaluation in audio modality;
  tonal-language cultural nuances and sign-language cultural variation;
  context-dependent communication rules (age, gender, status modifiers);
  cultural humor, sarcasm, and indirect expression.
- **Relevant when:** benchmark involves conversational or dialogue
  tasks; figurative language or pragmatic inference; dialectal or
  low-resource language deployment; translation or cross-lingual
  transfer.

### History and important figures
- **Search for:** LLM evaluations on non-Western history, oral-history
  digitization research, evaluations of multi-perspective historical
  narratives, culturally important person recognition datasets.
- **Usually unsearchable:** community-level historical memory (how
  families narrate their past); founding myths and origin narratives
  (often not distinguished from factual recall); suppressed or oral
  histories not in digitized form; locally important figures known only
  within their community.
- **Relevant when:** benchmark claims broad cultural knowledge
  evaluation; deployment involves educational AI in post-colonial
  regions; civic or political applications; regions with contested or
  actively reinterpreted histories.

## Evidence by validity dimension

The scoring step rates six validity dimensions. Each is sensitive to a
different shape of evidence. Use this as a lens: when a search result
surfaces, ask which dimension(s) it informs, and favor results that
would move a score.

- **IO — Input Ontology** ("does the test-case taxonomy cover what
  matters for this deployment?"). Shifted by: proposed new cultural
  taxonomies for the target region, studies documenting categories
  missing from existing benchmarks, community-driven (emic) vs.
  researcher-imposed (etic) category systems.

- **IC — Input Content** ("do the test items reflect the target
  culture?"). Shifted by: quantifications of Western or US content bias
  in comparable benchmarks, regional annotator validation studies,
  culture-specific content that fails to transfer from source to target
  region, community-contributed datasets for the target population.

- **IF — Input Form** ("does the signal encoding match real-world
  deployment inputs?"). Shifted by: visual or multimodal cultural
  evaluation results, studies on regional infrastructure effects on
  input signal quality (bandwidth, device quality), dialect surface-form
  evaluations, target-language morphology benchmarks. Audio/speech
  cultural evaluation is a near-vacuum; null results are expected.

- **OO — Output Ontology** ("do output categories fit the target
  region?"). Shifted by: stakeholder-driven taxonomy redesigns,
  alternative label systems proposed by researchers from the target
  region, multi-mode accuracy comparisons showing Western categories
  fail downstream.

- **OC — Output Content** ("do ground-truth labels reflect regional
  perspectives?"). Shifted by: label re-annotation studies using
  regional annotator pools, annotator demographic analyses of
  comparable benchmarks, studies documenting legitimate disagreement
  in cultural labels.

- **OF — Output Form** ("does the benchmark evaluate the output
  modality needed for deployment?"). Shifted by: MCQ-vs-open-ended
  format comparisons, text-to-speech availability for the target
  language, literacy-rate data for the target population, studies on
  generated-image stereotype reproduction in target-region contexts.

## Calibration warnings

- **Language competence vs. cultural knowledge.** For low-resource-
  language deployments, a benchmark score drop can reflect either a
  language-processing failure or a cultural-knowledge gap — with
  different interventions. When search results cite scores in the target
  language, note the ambiguity unless the paper explicitly controls for
  language competence (e.g., via a matched-English control or a
  language-understanding diagnostic).

- **Sub-national variation under national statistics.** When a national-
  level statistic resolves a tag (literacy, internet penetration,
  language share), check whether the deployment is itself sub-national.
  If so, add a short caveat noting the resolved value is a national
  aggregate and that within-country variation may meaningfully change
  the picture for the specific cohort.

- **Sparse-documentation regions.** For deployments targeting oral-
  tradition cultures, indigenous or stateless communities, diaspora
  populations, or digitally underrepresented regions, null results are
  themselves informative — calibrate expectations rather than spending
  extra budget on re-phrased queries. A thin result set usually reflects
  a documentation gap, not a thin culture; flag this explicitly in the
  YAML rather than reporting "no evidence found" ambiguously.

## Query construction

- **Combine region + domain + method.** `"Sub-Saharan Africa" + "food
  knowledge" + LLM + benchmark` is more effective than `African cultural
  AI` (too broad).
- **Use specific seed terms.** If you expect a regulation, agency,
  benchmark, or dataset to exist under a particular name, search that
  name directly.
- **Prefer official and academic sources.** Government portals for
  policy; ACL Anthology, arXiv, Semantic Scholar for NLP research;
  ITU, World Bank, national statistics bureaus for quantitative
  indicators.
- **Use site-restricted queries when it helps.** `site:aclanthology.org`
  for NLP work, government domains for policy names, `site:arxiv.org`
  for preprints.
- **Cross-check.** A single source is suspect for a factual claim; prefer
  convergence between two independent sources before committing a value.

## Red flags — do not rubber-stamp

- **Automated cultural metrics.** CLIP-based cross-cultural scores, BLEU
  on dialect translation, and similar automated evaluations have been
  shown to reward stereotypical outputs over culturally accurate ones.
  If a source relies on these without in-region human validation, note
  the limitation rather than citing the finding as ground truth.
- **Wikipedia as sole source.** English Wikipedia systematically
  underrepresents Global South and oral-tradition contexts. Acceptable
  as corroboration; not sufficient as sole source for a regional claim.
  Prefer non-English Wikipedia or community-contributed databases when
  those are available.
- **Stereotype reinforcement.** Searches will surface content that
  encodes the exact stereotypes a cultural validity assessment is meant
  to guard against. If a result looks like a stereotype rather than a
  fact, don't import it.
- **Outdated policy.** If a regulation, program, or standard has been
  superseded, cite the current one — note the transition if it's recent
  enough that deployments may still encounter the older version.

## Output

Return the FULL updated region YAML in a single ```yaml fenced block.
No preamble, no commentary outside the fence. Every original
`[NEEDS VERIFICATION]` tag must map to exactly one of the three fates
below — the distinction matters to the downstream reader, because
"investigated and not found" and "not investigated" have very different
implications for follow-up.

- **Resolved** — replaced with the verified value, followed by a
  **mandatory inline source citation**: short source descriptor + URL.
  Every resolved tag must be traceable; users need to be able to verify
  any claim themselves. Prefer two independent sources where the value
  is contentious or load-bearing. Examples:
  ```yaml
  literacy_rate_pct: "96 (Badan Pusat Statistik 2023 — https://bps.go.id/...)"
  mobile_internet_penetration_pct: "78 (ITU DataHub 2024 — https://datahub.itu.int/...; World Bank WDI 2023 — https://data.worldbank.org/...)"
  data_protection_regulation: "UU 27/2022 PDP (Law on Personal Data Protection) (Kemenkumham official text — https://...)"
  ```
  For multi-line string values, end the value with a trailing
  `Source: <descriptor> — <URL>` line inside the same string.
- **Searched, not found** — replaced with a short note starting with
  `[NOT FOUND —` that describes what was searched and why no value
  surfaced (e.g. `[NOT FOUND — searched ITU and World Bank 2023/2024;
  no Indonesia NTT-specific figure published]`).
- **Deferred, not searched** — left in place as
  `[NEEDS VERIFICATION — deferred: <brief reason>]` so the tag is still
  machine-identifiable for a future pass. The reason should be terse:
  `below search budget`, `likely unsearchable (lived practice)`,
  `low impact for scoring`, etc.

Additionally:

- Non-tagged fields are preserved (with short caveats added only on
  strong contradictory evidence — never silent overwrites). Citations
  are not required for non-tagged fields, since those were grounded in
  the elicitation, not the web.
- Net-new fields surfaced by your searches are appended in a logical
  location in the schema. Net-new fields are web-sourced by definition,
  so the same **mandatory inline source citation** rule applies to
  them.
