## Deployment Context

**Use case:** Timeline generation for coordination and evaluation of response efforts across time published in social media. The data would be tweets from natural disaster domain generated in Ecuadorian Spanish.
**Target population:** Latin American data and social analysts working at NGO and international organizations (e.g. Red Cross, UN OCHA) who seek to find how affected populations' needs evolve across time. They would be fluent in American English and Spanish, potentially speakers of different accents of Latin American Spanish.

# Validity Analysis: crisisltlsum
**Target context:** Ecuador — Humanitarian Crisis Social Media Analysts
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ⚠ | 1 | Serious concern | high |
| Output Ontology | 2 | Significant gaps | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 3 | Moderate gaps | medium |
| **Average** | **1.5** | | |

> ⚠ = highest concern &nbsp; ✓ = strongest dimension

### Dimension Key

| Abbr. | Dimension | Definition |
|:-----:|-----------|------------|
| IO | Input Ontology | Whether the benchmark's test case categories cover the query types expected in deployment. |
| IC | Input Content | Whether individual datapoint content is culturally and contextually appropriate for the target region. |
| IF | Input Form | Whether the input signal encoding (text, audio, image parameters) matches deployment conditions. |
| OO | Output Ontology | Whether the benchmark's output categories and scoring criteria reflect regionally valid decision boundaries. |
| OC | Output Content | Whether ground-truth labels align with the judgments of regional stakeholders. |
| OF | Output Form | Whether the expected output modality matches regional deployment needs and accessibility. |

## Overall Summary

CrisisLTLSum is a well-documented but tightly scoped English-language benchmark built on US/Australian Twitter data covering four crisis domains (wildfire, local fire, traffic, storm). For the Ecuador humanitarian crisis social media analyst deployment, it presents fundamental misalignments across nearly every validity dimension: the crisis taxonomy excludes the deployment's priority categories (volcanic, seismic, displacement, complex emergencies); the input content is geographically and institutionally US/Australian; the preprocessing pipeline is English-only with the authors themselves acknowledging language dependency; the output relevance criteria embed US-journalism assumptions that conflict with humanitarian needs-signal interpretation; and the labels were produced by English-native MTurk workers rather than by the inter-operational humanitarian teams the deployment requires. Only the surface output modality (text summaries and binary classifications) and the methodological scaffolding (cluster-then-refine procedure, multi-reference ROUGE, four-axis summarization rubric) offer any reusable value.

## Practical Guidance

### What This Benchmark Measures

CrisisLTLSum measures English-language, US/Australian-context timeline extraction and abstractive summarization quality for short-duration local crisis events in four narrow domains (wildfire, local fire, traffic, storm), evaluated against US English-native MTurk worker judgments. For the Ecuador deployment it can serve at most as a methodological exemplar — not as a measurement of the constructs (Spanish humanitarian operational relevance, multi-phase geophysical event tracking, SITREP-quality summarization) the deployment requires.

### Construct Depth

The benchmark probes its in-scope constructs reasonably deeply — it provides 1,000 timelines, transparent QC procedures, multi-reference summaries, and both automatic (ROUGE) and human (four-axis) evaluation. However, that depth is entirely conditional on the English/US/Australian/four-domain frame; outside that frame, none of the depth transfers. Input Ontology, Input Content, Input Form, and Output Content all score 1; Output Ontology scores 2; only Output Form (modality match) reaches 3.

### What Else You Need

Substantial supplementation is required: (1) a Spanish-language Ecuadorian crisis dataset with timeline structure (UrbangEnCy [WEB-17] is a binary-classification starting point but does not provide timelines); (2) re-annotation by Ecuadorian humanitarian inter-operational teams to define and label operational relevance; (3) replacement of the English NLP preprocessing stack (NER, OSM-anchoring, tokenization) with Spanish/Kichwa-aware components; (4) extension of the crisis taxonomy to volcanic, seismic, landslide, displacement, and complex humanitarian categories; (5) genre-aware evaluation against UN OCHA SITREP and Cruz Roja reporting conventions in both Spanish and English.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark's taxonomy is restricted to four crisis domains — wildfire, local fire, traffic, and storm [Q1, Q122] — and its scope is explicitly limited to 'local' events bound to a specific building, street, or county of short duration [Q12]. The Ecuador deployment prioritizes large-scale humanitarian and geophysical events (volcanic eruptions, lahares, earthquake sequences, mass displacement, complex humanitarian emergencies) that are entirely absent from this taxonomy, as confirmed by elicitation A1 and the regional crisis typology where 'benchmark_coverage: absent' is recorded for nearly every priority crisis type. Independent Ecuadorian crisis NLP work has identified volcanic and telluric (seismic) categories as operationally distinct [WEB-18]. Only 'storm' has even partial overlap, and that overlap is shallow because the benchmark's storm cases come from US/Australian meteorological contexts. The construct underrepresentation is severe and structural.

**Strengths:**
- The benchmark does cover traffic incidents and local urban fires, which may have some narrow applicability to urban Ecuadorian cantonal emergencies (e.g., Quito, Guayaquil) that municipal Cuerpo de Bomberos handle [Q122]; and it formalizes a granular 'local event' notion (e.g., 'fire in building A') [Q40] that conceptually maps onto parroquia-level incident tracking.

**Checklist:**

- **IO-1**: Required categories for Ecuador humanitarian deployment include volcanic eruption sequences (Cotopaxi, Tungurahua, Sangay), lahares, earthquake/aftershock sequences, landslides (movimiento en masa), riverine and coastal flooding (desbordamiento, inundación), mass displacement, and complex humanitarian emergencies [WEB-18]; elicitation A1 confirms these are the priority categories. — _Sources: WEB-18_
- **IO-2**: The benchmark omits all of the above categories. Q122 confirms the search is limited to 'wildfire, local fire, traffic, and storm,' and Q12 restricts scope to short-duration local events, structurally excluding multi-phase volcanic and displacement crises. — _Sources: Q122, Q12_
- **IO-3**: Wildfire and US-style traffic incidents are not 'irrelevant' per se but are low-priority for Ecuadorian humanitarian coordinators; páramo fires are noted in the region YAML as a Sierra concern but the benchmark's wildfire framing is calibrated to California/NSW/Victoria contexts [Q124], introducing construct-irrelevant variance. — _Sources: Q124_
- **IO-4**: Content validity is severely harmed: the benchmark cannot evaluate timeline extraction or summarization for the disaster types that constitute the deployment's primary operational use case. Q22's claim of '1,000 timelines' applies only within the four-domain frame and provides no coverage for Andean or Amazonian disaster typologies. — _Sources: Q1, Q22_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'CrisisLTLSum contains 1,000 crisis event timelines across four domains: wildfires, local fires, traffic, and storms.' (p.1)
- [Q12] 'The term "local" indicates that an event is bound to an exact location, such as a building, a street, or a county, and usually lasts for a short period.' (p.2)
- [Q122] 'We build CrisisLTLSum by limiting the search to four crisis domains: wildfire, local fire, traffic, and storm.' (p.12)
- [Q40] 'the clustering objective is to group tweets related to the same local event, such as a "fire in building A" or a "wildfire in a specific area".' (p.4)

*Web sources:*
- [WEB-18] Ecuadorian researchers built a Twitter monitoring system around four locally-relevant categories: volcanic, telluric (seismic), fires, and climatological — confirming Ecuador's distinct crisis taxonomy.
- [WEB-21] HumVI 2024 review confirms English-dominance and the absence of multilingual humanitarian timeline benchmarks.

</details>

**Information gaps:**
- Whether any narrow urban-fire or traffic sub-use-case in Quito/Guayaquil could meaningfully reuse the benchmark's taxonomy without retraining.

**Requires expert verification:**
- Whether IGEPN/SNGR alert escalation workflows could be modeled as 'timelines' compatible with the benchmark's seed-tweet formulation.

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
All source data was collected from seven US states and two Australian states during 2020–2021 [Q123], and geographic areas were selected for their fit to the four-domain taxonomy [Q124]. Tweet filtering depends on US/Australian city, town, and 'famous neighborhoods' lists [Q30] and on English-curated keyword lists [Q126]. The 1,000 clusters were hand-selected by the authors [Q52]. Ecuadorian crisis tweets reference parroquias, cantones, SNGR (formerly SGR) [WEB-11], IGEPN, INAMHI, Cruz Roja Ecuatoriana, volcano names (Cotopaxi, Tungurahua, Sangay), Kichwa toponyms, and operationally critical terms like 'damnificados' and 'albergues' — none of which are represented in the dataset. Elicitation A2 confirms analysts require precise anchoring to Ecuador-specific entities and that US-default references would be operationally meaningless. The Ecuador-specific UrbangEnCy dataset [WEB-17] exists but covers only binary classification, not timelines.

**Strengths:**
- The benchmark provides a methodological template (semi-automated cluster-then-refine, seed-tweet specification) [Q27, Q52] that could in principle be re-applied to Ecuadorian Spanish content; the authors transparently document content-collection limitations [Q117] and explicitly acknowledge that replication for other languages/locations is hard [Q119].

**Checklist:**

- **IC-1**: Yes — Ecuador queries require Spanish-language dialectal knowledge, Ecuadorian administrative geography (24 provinces, ~221+ cantones, 1,500+ parroquias) [WEB-6, WEB-8], Kichwa/Shuar toponym recognition [WEB-1], institutional acronyms (SNGR/SGR, IGEPN, INAMHI, MSP), and crisis-specific Spanish vocabulary ('damnificado', 'albergue', 'lahares', 'desbordamiento'). None of this is present in the benchmark. — _Sources: WEB-6, WEB-8, WEB-11, WEB-1_
- **IC-2**: Cultural sensitivity is misaligned: the dataset reflects US/Australian crisis-response cultural norms (FEMA-style agencies, US journalistic conventions). Ecuadorian humanitarian context emphasizes inter-agency coordination, indigenous community signals, and the 'damnificado' legal-operational concept absent from the benchmark. — _Sources: Q123, Q124_
- **IC-3**: Western-specific knowledge is pervasive: location candidate lists [Q30], OSM-based place anchoring [Q36], and keyword curation from US/Australian news [Q126] all encode US/Australian assumptions that will not transfer. — _Sources: Q30, Q36, Q126_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the benchmark itself documents no regional annotators; for Ecuador deployment, expert annotators from Cruz Roja Ecuatoriana, UN OCHA Ecuador, and indigenous federations (CONAIE, ECUARUNARI) would be required.
- **IC-5**: Content validity is fundamentally violated: the entire instance pool reflects US/Australian crisis content [Q123, Q69], with no Spanish, Latin American, or humanitarian-organizational content represented. — _Sources: Q123, Q69_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q123] 'We collect CrisisLTLSum across seven states in the USA and two states of Australia during 2020 and 2021.' (p.12)
- [Q124] 'These states are selected as they are some of the areas subject to the most events falling into our crisis domains of interest.' (p.13)
- [Q30] 'The location filtering relies on a list of location candidates created by gathering cities, towns, and famous neighborhoods in a big area of interest.' (p.3)
- [Q52] 'We, authors of this work, manually selected 1,000 clusters... while specifying the "seed tweet"... of each timeline.' (p.5)
- [Q126] 'We carefully curate a keyword list for each of our categories of interest by employing expert knowledge gathered through over-viewing crisis stories in news, social media, and related big disaster events of the past.' (p.13)
- [Q119] 'replicating the same process for other language or based on other locations may be hard because of such dependencies.' (p.10)

*Web sources:*
- [WEB-6] Ecuador has 24 provinces with distinct administrative hierarchy.
- [WEB-8] Ecuador has approximately 221 cantones and over 1,500 parroquias — administrative units absent from benchmark geography.
- [WEB-11] SNGR was formally renamed from SGR in 2024; both acronyms appear in tweets.
- [WEB-17] UrbangEnCy provides 25,500+ Ecuadorian Spanish emergency tweets but only binary labels.
- [WEB-1] Kichwa and Shuar are official intercultural languages; toponyms appear in Sierra/Oriente content.

</details>

**Information gaps:**
- OpenStreetMap coverage quality for rural Ecuadorian parroquias and Kichwa community names is unverified.

**Requires expert verification:**
- Specific institutional Twitter/X handles for SNGR, IGEPN, INAMHI, and Cruz Roja Ecuatoriana for entity-linking.

---

### Input Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark's preprocessing pipeline is English-specific throughout: AllenNLP NER trained on CoNLL03 [Q33], BERT-based NER fine-tuned on English Twitter [Q35], lemmatization and lowercasing of English keywords [Q129], OpenStreetMap matching of English place names [Q36], and BERT/BART models with 512-token English-tokenizer constraints [Q86, Q141, Q143]. The authors themselves flag that 'replicating the same process for other language or based on other locations may be hard' [Q119]. The Ecuador deployment processes Ecuadorian Spanish in informal/semi-formal registers with Kichwa-Spanish code-switching and crisis-specific vocabulary (elicitation A4); no Kichwa NLP resources are publicly available [WEB-1, WEB-13]. The signal-distribution mismatch is total at the language level and severe at the register/script level — the benchmark cannot process Spanish input at all without reconstruction, and Kichwa toponyms within Spanish tweets would not be recognized by any component of the pipeline.

**Strengths:**
- The benchmark is text-only and Twitter-native, matching the surface modality of the Ecuadorian deployment's primary data source; UrbangEnCy [WEB-17] confirms Twitter is also used for Ecuadorian emergency NLP, so the platform-level signal type is shared.

**Checklist:**

- **IF-1**: Signal distribution mismatch is severe: the benchmark operates on English Twitter; the deployment requires Ecuadorian Spanish with code-switching, indigenous toponyms, and informal orthography [WEB-1]. Tokenizers, NER, lemmatization [Q129], and place-name matching [Q36] would all need replacement. — _Sources: Q33, Q35, Q129, WEB-1_
- **IF-2**: Regional infrastructure supports Twitter capture (95.8% mobile broadband [WEB-15]; UrbangEnCy demonstrates feasibility [WEB-17]), but Amazonian rural areas have severely limited connectivity, biasing the available signal away from indigenous communities most exposed to environmental crises. — _Sources: WEB-15, WEB-17_
- **IF-3**: Domain-specific form differences include Kichwa orthographic variation (the 2008 unified alphabet remains contested [WEB-1]), Spanish accent marks, and crisis vocabulary like 'damnificados', 'lahares' that no English-trained tokenizer or NER will handle correctly. — _Sources: WEB-1_
- **IF-4**: External validity is fundamentally violated: the entire preprocessing pipeline [Q28–Q37] is English/US/Australia-calibrated and the authors explicitly acknowledge the language dependency [Q119]. — _Sources: Q119, Q36_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'we use a pre-trained neural model from AllenNLP... trained on CoNLL03... to extract entities with types of people, location, and organization.' (p.3)
- [Q35] 'we further developed a BERT-based NER model tuned on Twitter data to detect location mentions.' (p.4)
- [Q36] 'We use OpenStreetMap API to map location mentions to physical addresses.' (p.4)
- [Q119] 'replicating the same process for other language or based on other locations may be hard because of such dependencies.' (p.10)
- [Q129] 'we maintain both a lower-cased and a lemittized version of the keywords and the tweet's text.' (p.13)

*Web sources:*
- [WEB-1] Kichwa orthography is contested with continued spelling variation; written use of indigenous languages outside schools is minimal.
- [WEB-13] First Ecuadorian Spanish NLP corpus exists but does not cover Kichwa.
- [WEB-15] Ecuador has 95.8% mobile broadband connections, supporting Twitter use.
- [WEB-17] UrbangEnCy demonstrates feasibility of Spanish Ecuadorian Twitter capture but is binary-classification only.

</details>

**Information gaps:**
- OSM coverage quality for Ecuadorian rural geography; smartphone vs. feature-phone distribution in Oriente.

**Requires expert verification:**
- Frequency and patterns of Kichwa-Spanish code-switching in real-time crisis tweets from indigenous federation accounts.

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The output ontology consists of (a) a binary relevance label conditioned on three conjunctive criteria — relevant, informative (facts vs. 'personal points of view'), and not repetitive [Q58] — and (b) a four-axis summary rubric (Coherence, Accuracy, Coverage, Overall) scored 1–5 [Q106, Q151–Q160]. The Coherence rubric explicitly references English grammar and English-language understandability [Q153]. For humanitarian coordinators, relevance criteria differ structurally: road/bridge access status to affected communities, informal community broadcasts, displacement movement indicators, alert level changes, and 'damnificados' counts at parroquia/cantón level are operationally salient (region YAML; elicitation A3), and arguably some 'personal points of view' from affected communities are highly informative for needs assessment — directly conflicting with the benchmark's exclusion of personal views [Q58]. The four-axis summary rubric is partially transferable in abstract structure but its operational definitions are anchored to English [Q153] and contain no notion of humanitarian reporting conventions (UN OCHA SITREP format, numbered findings, agency acronym usage).

**Strengths:**
- The four-axis rubric (Coherence, Accuracy, Coverage, Overall) is a generic and well-structured summarization evaluation framework [Q106, Q151] that could plausibly be adapted to Spanish reference summaries with rewritten anchors; the Accuracy axis [Q155] aligns with humanitarian concerns about avoiding hallucinated content.

**Checklist:**

- **OO-1**: The binary 'part of timeline / not' label is too coarse for humanitarian use; the rubric axes are reusable in form but their English-anchored definitions [Q153] need redesign. — _Sources: Q58, Q153_
- **OO-2**: Missing categories include: humanitarian-relevance sub-types (logistics access, needs signals, coordination signals, displacement), source-type tagging (official agency vs. community vs. media), and alert-escalation states (critical for IGEPN/SNGR volcanic monitoring) — none are represented [Q58, Q151]. — _Sources: Q58, Q151, WEB-21_
- **OO-3**: The 'informative = facts not personal points of view' criterion [Q58] encodes a US-journalism stance that excludes precisely the affected-community first-person testimony often most operationally salient in humanitarian monitoring. — _Sources: Q58_
- **OO-4**: Stakeholder-driven taxonomy redesign is required, involving Cruz Roja Ecuatoriana and UN OCHA Ecuador analysts, to define a multi-label relevance schema and SITREP-aligned summary criteria.
- **OO-5**: Structural and content validity are violated: the output space does not represent the constructs ('humanitarian operational relevance', 'situation report quality') the deployment cares about. — _Sources: Q153, Q157_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q58] 'A tweet is labeled as part of the timeline only if it satisfies all the following three conditions: relevant... informative: provides facts about the event but not only contains personal points of view, not repetitive...' (p.5)
- [Q106] 'Each summary was evaluated by five different workers on a scale from 1 to 5 across four axes: Coherence, Accuracy, Coverage, and Overall quality...' (p.8)
- [Q153] 'A summary is coherent if when read by itself, it's easy to understand and free of English errors.' (p.21)
- [Q155] 'Does the factual information in the summary accurately match the information in the timeline?' (p.21)
- [Q157] '"How well does the summary cover the important information in the timeline?"' (p.21)

*Web sources:*
- [WEB-21] HumVI confirms humanitarian NLP requires bespoke relevance taxonomies not covered by general crisis benchmarks.

</details>

**Information gaps:**
- Whether Cruz Roja/UN OCHA have published formal relevance schemas adaptable as a target ontology.

**Requires expert verification:**
- Operational definition of 'important information' in Ecuadorian humanitarian SITREP conventions vs. benchmark's 'Coverage' axis.

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Ground-truth labels were produced by MTurk workers explicitly restricted to 'countries where native English speakers are most likely to be found' [Q61], with majority vote across three workers per timeline [Q70] and reference summaries selected from the two highest-agreeing workers [Q88]. Summary quality ratings used five MTurk workers under the same location restriction [Q105, Q106]. The deployment requires labels produced by an inter-operational team of Ecuadorian field coordinators, social analysts, and domain experts (elicitation A3) — a fundamentally different and unavailable annotator population. There is no Spanish-speaking, Latin American, indigenous-language-fluent, or humanitarian-practitioner annotator in the entire benchmark pipeline. The high inter-annotator agreement (90.06% [Q77]) demonstrates only internal consistency among US-context workers, not validity for the Ecuadorian humanitarian construct.

**Strengths:**
- The benchmark documents annotation procedures transparently — multiple QC gates [Q60–Q66], qualification testing [Q62], expert review [Q64], and reported agreement statistics [Q77, Q79] — providing a methodological template that could be adapted (with different annotators) for Ecuadorian re-annotation.

**Checklist:**

- **OC-1**: No — labels reflect English-native MTurk worker judgments [Q61, Q70], not Ecuadorian humanitarian coordinator perspectives. — _Sources: Q61, Q70_
- **OC-2**: Disagreement is highly likely on the 'informative' criterion [Q58] (excluding personal views vs. needs-signal interpretation), on what constitutes 'important information' for Coverage [Q157], and on event boundaries (US local-fire model vs. multi-phase volcanic crisis). — _Sources: Q58, Q157_
- **OC-3**: Demographic documentation is partial: only the location restriction [Q61], MTurk recruitment, qualification process [Q62–Q66], and pay rate [Q67–Q68] are documented. No information on language background beyond English-native, professional background, or humanitarian experience. — _Sources: Q61, Q62, Q67_
- **OC-4**: Re-annotation by an Ecuadorian inter-operational team (per A3) is essential — but the existing labels themselves are not reusable as a starting point for humanitarian relevance.
- **OC-5**: Aggregation is majority vote of three workers [Q70], which can erase a single dissenting humanitarian-aware perspective — particularly risky for low-frequency but high-importance signals (community needs, indigenous voices). — _Sources: Q70, WEB-22_
- **OC-6**: Convergent validity and external validity are both violated: there is no evidence the labels correlate with Ecuadorian humanitarian judgments, and the annotator population is operationally unrepresentative. — _Sources: Q61, Q105_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q61] 'we use location restriction (QC1) to limit the pool of workers to countries where native English speakers are most likely to be found.' (p.5)
- [Q70] 'we take the majority label among the three workers.' (p.6)
- [Q77] 'The average timeline-level agreement between those two workers is 90.06%.' (p.6)
- [Q88] 'we pick the two summaries written by the two workers who agree the most...' (p.7)
- [Q105] 'we recruit a group of workers from MTurk with the same Location restriction (QC1)...' (p.8)

*Web sources:*
- [WEB-22] HumAID 2016 Ecuador Earthquake subset shows severe class imbalance (e.g., 3 tweets in 'displaced people and evacuations'), illustrating that even Ecuador-event data annotated under generic schemas underweights humanitarian categories.
- [WEB-27] MDPI study confirms HumAID Ecuador subset class imbalance limits training utility.

</details>

**Information gaps:**
- Specific country-level distribution of the MTurk worker pool (US-only? US/UK/AU?).

**Requires expert verification:**
- Whether any Cruz Roja Ecuatoriana or UN OCHA Ecuador annotation guidelines could anchor a re-annotation effort.

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
At the surface modality level, the benchmark and deployment match: both produce text outputs (binary classification labels, abstractive text summaries) [Q91, Q98]. ROUGE [Q98–Q100] and the human rubric [Q106] are evaluation metrics that can in principle be adapted to Spanish reference summaries with appropriate tokenization. However, the benchmark provides no documentation of multilingual evaluation, and the human-written reference summaries [Q87] are English. UN OCHA situation reports follow specific genre conventions (numbered bullets, standardized headers, percentages) that differ from the abstractive narrative style elicited in the benchmark. The deployment also requires bilingual reporting (Spanish for national counterparts, English for global reporting), which the benchmark does not address. So the modality matches but the formatting/genre/language alignment does not.

**Strengths:**
- Text-based abstractive summarization is the right surface form for humanitarian SITREP production [Q98]; the multi-reference ROUGE setup [Q100] is a reasonable template that extends to Spanish references with multilingual tokenization; the human evaluation protocol design [Q103–Q108] is methodologically sound and could be re-instantiated with bilingual evaluators.

**Checklist:**

- **OF-1**: Text-output modality matches deployment needs (analyst-consumable text summaries and binary relevance flags) [Q91, Q98]. — _Sources: Q91, Q98_
- **OF-2**: Text-to-speech is not a primary requirement — analysts are literate professionals (region YAML literacy_and_education.analyst_population). Not applicable.
- **OF-3**: Analyst literacy is high in Spanish and English [region YAML]; no accessibility barrier at the consumer side. Affected populations have ~94–96% national literacy [WEB-2, WEB-3] but with rural and indigenous gaps [WEB-5] — relevant if outputs were redirected to community use, but not for the primary analyst use case. — _Sources: WEB-2, WEB-3, WEB-5_
- **OF-4**: External validity is partially preserved at the modality level but compromised by language (English-only references [Q87], English-anchored Coherence [Q153]) and genre (no SITREP conventions). ROUGE applied to English references against Spanish outputs would be invalid. — _Sources: Q87, Q153_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q91] 'For evaluation, we use the average timeline-level accuracy.' (p.7)
- [Q98] 'We evaluate all timeline summarization models with ROUGE...' (p.8)
- [Q100] 'We use SacreROUGE... to compute multi-reference ROUGE scores.' (p.8)
- [Q87] 'each timeline in our dataset is annotated by three workers... it includes three summaries.' (p.7)
- [Q108] 'the human-written summaries are significantly better than the ones generated by models, in terms of overall quality with an average rating of 4.12.' (p.8)

*Web sources:*
- [WEB-2] Ecuador adult literacy ~94% (2022).
- [WEB-3] Ecuador adult literacy ~96.3% (2022).
- [WEB-5] Indigenous communities have lower literacy rates than national average.

</details>

**Information gaps:**
- Whether multilingual ROUGE/BERTScore implementations adopted by humanitarian NLP practitioners are validated for Spanish SITREP-style text.

**Requires expert verification:**
- Specific UN OCHA / Cruz Roja SITREP genre conventions to anchor evaluation rubric adaptation.

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Four-domain US taxonomy excludes Ecuador's priority crisis types (volcanic, seismic, landslide, displacement, complex humanitarian emergencies).

**Recommendation:** Co-design a deployment-specific crisis taxonomy with Cruz Roja Ecuatoriana, UN OCHA Ecuador, IGEPN, and SNGR; include multi-phase event states (alert escalation, lahar advisory, exclusion-zone declaration, return phase) explicitly modeled as timeline structure.

### Input Content ⚠

**Gap:** All instances are US/Australian English Twitter; no Ecuadorian geographic, institutional, or linguistic content.

**Recommendation:** Build an Ecuador-specific timeline corpus using UrbangEnCy [WEB-17] as a Spanish-tweet seed pool, extended with parroquia-level location candidates, SNGR/IGEPN/INAMHI keyword lists, and Kichwa toponym dictionaries curated with CONAIE/ECUARUNARI input.

### Input Form ⚠

**Gap:** English-only preprocessing pipeline (NER, lemmatization, OSM, tokenizers) cannot process Spanish or Kichwa.

**Recommendation:** Replace AllenNLP/CoNLL03 NER with Spanish NER fine-tuned on Ecuadorian tweets (extending the Mexico earthquake template [WEB-20]); validate OpenStreetMap coverage for Ecuadorian rural geography and supplement with a Kichwa-toponym gazetteer; handle the SGR/SNGR acronym alias [WEB-11] explicitly.

### Output Content ⚠

**Gap:** Labels and reference summaries produced by English-native MTurk workers, not by the Ecuadorian inter-operational team that will use the system.

**Recommendation:** Conduct re-annotation with field coordinators, social analysts, and domain experts from Cruz Roja Ecuatoriana and UN OCHA Ecuador; use deliberative consensus rather than majority-vote aggregation to preserve minority humanitarian signals; document annotator demographics in a Datasheet.

### Output Form

**Gap:** ROUGE and the human rubric assume English references; no Spanish or bilingual evaluation; no SITREP genre conventions.

**Recommendation:** Use multilingual semantic-similarity metrics (e.g., multilingual BERTScore) against Spanish reference summaries; develop a parallel English/Spanish evaluation track aligned with UN OCHA SITREP and Cruz Roja appeal genre conventions.

### Output Ontology

**Gap:** Binary 'part of timeline' criterion and four-axis rubric are anchored to English/US-journalism norms; humanitarian relevance categories (logistics access, community needs, displacement signals, alert escalation) are unrepresented.

**Recommendation:** Redesign the relevance schema as multi-label humanitarian-operational tagging (logistics, needs, displacement, coordination, casualties, infrastructure, alert-state) and rewrite the summary rubric to include SITREP genre conformance, bilingual coherence, and source-type provenance.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "CrisisLTLSum contains 1,000 crisis event timelines across four domains: wildfires, local fires, traffic, and storms." |
| Q2 | 1 | input_content | "We built CrisisLTLSum using a semi-automated cluster-then-refine approach to collect data from the public Twitter stream." |
| Q3 | 1 | output_ontology | "A timeline is a chronologically sorted set of posts, where each brings in new information or updates about an ongoing event (such as a fire, storm, or traffic incident)." |
| Q4 | 1 | input_ontology | "CrisisLTLSum supports two complex downstream tasks: timeline extraction and timeline summarization." |
| Q5 | 1 | input_ontology | "The timeline extraction task is formalized as: given a seed tweet as the initial mention of a crisis event, extract relevant tweets with updates on the same event from the incoming noisy tweet stream." |
| Q6 | 1 | input_ontology | "The timeline summarization task aims to generate abstractive summaries of evolving events by aggregating important details from temporal and incremental information." |
| Q7 | 1 | output_form | "Our initial experiments indicate a significant gap between the performance of strong baselines compared to the human performance on both tasks." |
| Q8 | 1 | input_content | "Our dataset, code, and models are publicly available." |
| Q9 | 1 | input_content | "Hossein Rajaby Faghihi, Bashar Alhafni, Ke Zhang, Shihao Ran, Joel Tetreault, Alejandro Jaimes" |
| Q10 | 1 | input_content | "Michigan State University, New York University Abu Dhabi, Dataminr, Inc." |
| Q11 | 2 | input_ontology | "To the best of our knowledge, this is the first annotated dataset for such an extraction task, while this problem has been tackled before in unsupervised settings (Zhang et al., 2018)." |
| Q12 | 2 | input_ontology | "Moreover, we focus on the extraction of local crisis events. The term "local" indicates that an event is bound to an exact location, such as a building, a street, or a county, and usually lasts for a short period." |
| Q13 | 2 | input_content | "Building a corpus of local crisis events is particularly useful for first responders but also challenging because the timelines of these events are often not captured in existing knowledge sources." |
| Q14 | 2 | input_content | "This means one has to design mechanisms for automatically detecting and tracking events directly from the Twitter stream, which is especially hard for existing clustering methods (Guille and Favre, 2015; Asgari-Chenaghlu et al., 2021) given the low number of available tweets for each local event." |
| Q15 | 2 | input_form | "First, the process of identifying and extracting relevant updates for a specific event has to contend with the large volume of noise (Alam et al., 2021a) and informal tone (Rudra et al., 2018) compared to other domains such as news." |
| Q16 | 2 | input_ontology | "Additionally, summarizing an on-going event helps toward a quick and better understanding of its progress. This requires a good level of abstraction with important details covered and properly presented (e.g., the temporal order of event evolution)." |
| Q17 | 2 | output_form | "CrisisLTLSum is the first dataset to provide human-written timeline summaries to support research in this direction." |
| Q18 | 2 | input_content | "CrisisLTLSum is developed through a two-step semi-automated process to create 1,000 local crisis timelines from the public Twitter stream." |
| Q19 | 2 | input_ontology | "To our best knowledge, this is the first timeline dataset focusing on "local" crisis events with the largest number of unique events." |
| Q20 | 2 | input_ontology | "We propose CrisisLTLSum, which is the largest dataset over local crisis event timelines. Notably, this is the first benchmark for abstractive timeline summarization in the crisis domain or on Twitter." |
| Q21 | 2 | output_form | "We develop strong baselines for both tasks, and our experiments show a considerable gap between these models and human performance, indicating the importance of this dataset for enabling future research on extracting timelines of crisis event updates and summarizing them." |
| Q22 | 2 | input_ontology | "While existing datasets on crisis event timelines (Binh Tran et al., 2013; Tran et al., 2015; Pasquali et al., 2021) are limited to a small set of large-scale events, CrisisLTLSum covers a thousand timelines compared to only tens of events covered by each of the existing datasets." |
| Q23 | 2 | input_ontology | "Additionally, we further go beyond the simple tweet categorization by enabling the extraction of information that include updates over the events' progress." |
| Q24 | 2 | input_ontology | "Timeline summarization (TLS) was firstly proposed in Allan et al. (2001), which extracts a single sentence from the news stream of an event topic." |
| Q25 | 2 | input_ontology | "In general, the TLS task aims to summarize the target's evolution (e.g., a topic or an entity) in a timeline (Martschat and Markert, 2018; Ghalandari and Ifrim, 2020)." |
| Q26 | 2 | input_ontology | "Existing approaches of TLS are mainly based on extractive methods, which are often grouped into several categories." |
| Q27 | 3 | input_content | "This section presents our semi-automated approach to collect CrisisLTLSum. We first extract clusters of tweets as noisy timelines and then refine them via human annotation to get clean timelines that only include non-redundant, informative, and relevant tweets." |
| Q28 | 3 | input_form | "Figure 2 shows the process for generating a set of noisy timelines starting from the Twitter stream and followed by pre-processing and knowledge enhancement steps, the online clustering method, and post-processing & cleaning steps." |
| Q29 | 3 | input_content | "We limit the incoming tweets to specific geographical areas, periods, and domains of interest." |
| Q30 | 3 | input_form | "The location filtering relies on a list of location candidates created by gathering cities, towns, and famous neighborhoods in a big area of interest. A tweet is considered relevant to our area of interest if 1) the text mentions one of the candidates, 2) the geo-tag matches the area of interest, or 3) the user location matches the area of interest." |
| Q31 | 3 | input_content | "To limit the tweets to a specified crisis domain, we curate domain-specific keywords and only select tweets with phrases matching one of the keywords. This approach is not comprehensive or exhaustive but somewhat representative of each crisis domain." |
| Q32 | 3 | input_content | "The combinations of (area a, domain d, time t) are manually selected so that the events of type d at location a are more frequent during time period t." |
| Q33 | 3 | input_form | "We use three different modules. First, we use a pre-trained neural model from AllenNLP (Gardner et al., 2018), trained on CoNLL03 (Tjong Kim Sang and De Meulder, 2003), to extract entities with types of people, location, and organization." |
| Q34 | 3 | input_form | "Although this module extracts some important entities in the text, it fails to extract uncommon entities or special mentions" |
| Q35 | 4 | input_form | "Since location mentions are crucial in extracting local events and existing models have low performance detecting them from noisy tweets text, we further developed a BERT-based NER model tuned on Twitter data to detect location mentions." |
| Q36 | 4 | input_form | "Location Augmentation We use OpenStreetMap API to map location mentions to physical addresses." |
| Q37 | 4 | input_form | "This step provides complementary information about each location while reducing the noise introduced by the entity extraction module through removing location mentions that are wrongly detected or are not located in the area of interest." |
| Q38 | 4 | input_ontology | "Online Clustering This step aims to mimic the real-life scenario where tweets are sequentially fed into a clustering algorithm (Wang et al., 2015)." |
| Q39 | 4 | input_ontology | "We further choose this method since this is a lot faster than the retro-spective (all data available at the same time) clustering methods for a large pool of input data." |
| Q40 | 4 | input_ontology | "Here, the clustering objective is to group tweets related to the same local event, such as a "fire in building A" or a "wildfire in a specific area"." |
| Q41 | 4 | output_form | "The online clustering method utilizes a custom similarity metric that combines the similarity of the entities, the closeness of locations in the real world, and the existence of shared hashtags." |
| Q42 | 4 | output_form | "The mindist, maxdist, shashtag, and sdist are hyper-parameters of the clustering algorithm." |
| Q43 | 4 | output_form | "We have only used heuristics and a small set of executions to tune these hyper-parameters." |
| Q44 | 4 | input_ontology | "The new tweet is added to the highest matching-score cluster where the similarity score is higher than simthreshold and the time elapsed between the new tweet and the last update of the cluster is less than timethreshold." |
| Q45 | 4 | input_ontology | "If the previous criteria are met for none of the clusters, a new cluster is created based on the new tweet." |
| Q46 | 4 | input_ontology | "During this process, we remove inactive clusters whose last update was at least expirationthreshold minutes ago and have less than tweetthreshold number of tweets available." |
| Q47 | 4 | input_ontology | "A cluster head is always the tweet with the most entity mentions; In case of a tie, the more recent tweet becomes the head of the cluster." |
| Q48 | 4 | input_ontology | "The hyper-parameters of this method is noted in Appendix A." |
| Q49 | 4 | input_form | "Cluster Post-Processing We apply three post-processing steps to improve the quality of the generated clusters." |
| Q50 | 4 | input_form | "First, we manually merge pairs of clusters with a cluster head similarity higher than a threshold headmin." |
| Q51 | 4 | input_form | "This step compensates for some of the errors from missing entities in the pre-processing step, which affects the intermediate similarity scores in the clustering algorithm." |
| Q52 | 5 | input_content | "We, authors of this work, manually selected 1,000 clusters that contain enough tweets describing how a crisis event evolves, while specifying the "seed tweet" (i.e. the first observed post that describes the ongoing event) of each timeline." |
| Q53 | 5 | input_ontology | "The selected clusters cover events mainly from four crisis domains, including wildfire, local fire, storm, and traffic." |
| Q54 | 5 | output_content | "We use the Amazon Mechanical Turk (MTurk) platform to label and refine the noisy clusters to generate a clean timeline and collect the summaries." |
| Q55 | 5 | output_content | "We split the annotation into multiple batches of Human Intelligence Tasks (HITs), where each batch contains timelines from the same domain." |
| Q56 | 5 | output_content | "Each HIT contains three noisy timelines, and we collect annotations from 3 different workers on each." |
| Q57 | 5 | output_content | "The workers are given the seed tweet and the subsequent tweets sorted by time, and they were asked to read the tweet one by one and answer i) whether the tweet should be part of the timeline, and ii) what is the reason if not." |
| Q58 | 5 | output_ontology | "A tweet is labeled as part of the timeline only if it satisfies all the following three conditions: relevant: talks about the same event indicated in the seed tweet, informative: provides facts about the event but not only contains personal points of view, not repetitive: brings in new information." |
| Q59 | 5 | output_content | "After reviewing all the tweets, the worker is finally asked to write a concise summary to describe how the event progresses over time." |
| Q60 | 5 | output_content | "Following prior quality control practices (Briakou et al., 2021), we use multiple quality control (QC) steps to ensure the recruitment of high-quality annotators." |
| Q61 | 5 | output_content | "First, we use location restriction (QC1) to limit the pool of workers to countries where native English speakers are most likely to be found." |
| Q62 | 5 | output_content | "Next, we recruit annotators who pass our qualification test (QC2), where we ask them to annotate 3 timelines." |
| Q63 | 5 | output_content | "We run several small pilot tasks, each with a replication factor of nine." |
| Q64 | 5 | output_content | "We check annotators' performance on timeline extraction task against experts' labels and have experts manually review (QC3) annotators' summary quality." |
| Q65 | 5 | output_content | "Only workers passing all the quality control steps contribute to the final task." |
| Q66 | 5 | output_content | "During the final task, we perform regular quality checks (QC4), and only use workers who consistently perform well." |
| Q67 | 5 | output_content | "We compensate the workers at a rate of $3 per HIT for the task." |
| Q68 | 5 | output_content | "Each batch of tasks is followed by a one-time bonus that makes the final rate over $10 per hour." |
| Q69 | 5 | input_content | "Out of these 1,000 annotated timelines (10,610 tweets) in CrisisLTLSum, 423 (42%) are about" |
| Q70 | 6 | output_content | "To make the ground-truth on whether each tweet is part of the timeline or not, we take the majority label among the three workers." |
| Q71 | 6 | output_ontology | "4,303 (41%) tweets are labeled as part of the timeline, whereas 6,307 (59%) are not." |
| Q72 | 6 | input_form | "Out of all timelines, 110 (11%) only include tweets that are part of the timeline, whereas 68 (7%) did not include any." |
| Q73 | 6 | input_form | "The majority of the timelines (447 or 45%) have five tweets or less." |
| Q74 | 6 | input_form | "Our dataset includes long timelines of 26 or more tweets, constituting 9% (94 timelines) across all domains." |
| Q75 | 6 | input_form | "We notice an interesting trend across the domains: the longer the timeline, the lower the average percentage of tweets to be part of the timeline." |
| Q76 | 6 | output_content | "To measure the agreement rate between workers on the timeline extraction task, we consider the annotations of two out of three workers who agree most per timeline." |
| Q77 | 6 | output_content | "The average timeline-level agreement between those two workers is 90.06%." |
| Q78 | 6 | output_content | "We also explore a more profound analysis by comparing the workers' annotations on 20% of the timelines against the annotations of experts." |
| Q79 | 6 | output_content | "The average timeline-level agreement rate of this analysis is 91.77%." |
| Q80 | 6 | input_form | "To aid reproducibility when using our dataset for various research experiments, we divided our dataset into: training (TRAIN: 70% or 706 timelines), development (DEV 10% or 86 timelines), and testing (TEST 20% or 208 timelines) splits." |
| Q81 | 6 | input_form | "The splits are created via stratified sampling based on the event crisis domains and the length of timelines (i.e., number of tweets) as shown in Table 2." |
| Q82 | 6 | input_ontology | "Given a crisis event timeline consisting of n tweets T = [t0, t1, ..., tn], where t0 is the seed tweet, i.e. the first observed post that describes the ongoing event, we define two tasks: Timeline Extraction and Timeline Summarization." |
| Q83 | 6 | input_ontology | "Given an initial seed tweet t0, and following chronologically sorted tweets ti, i = 1, ..., n, the goal of the timeline extraction task is to determine whether tweet ti is part of the timeline, i.e., related to the same event and adding new information compared to all prior tweets [t0, ..., ti−1]." |
| Q84 | 7 | input_ontology | "Timeline Summarization: Similar to previous work by Chen et al. (2019), this task aims to generate a summary Ŷ = {ŵ1, ..., ŵk} with sequence of words ŵi to concisely describe the crisis event and its evolution given the output from the timeline extraction task Textracted." |
| Q85 | 7 | input_form | "We construct a list of tweet sequences S by concatenating all the tweets that are part of the timeline from t1 to ti: S = [t1, t1 + t2, ..., t1 + ... + tn]." |
| Q86 | 7 | input_form | "For our first sentence-level classification model, we fine-tune BERT (Devlin et al., 2019) on the tweet sequences where every training example would have the form of "t0 [SEP] si"; where si ∈ S." |
| Q87 | 7 | output_content | "Since each timeline in our dataset is annotated by three workers (§3.2), it includes three summaries." |
| Q88 | 7 | output_content | "To adapt the timeline summarization task to this setting, we pick the two summaries written by the two workers who agree the most based on the timeline extraction labels they assign to the tweets in each timeline." |
| Q89 | 7 | output_content | "This reduces the variance between the summaries regarding their coverage of the crisis event described in the tweets that are part of the timeline." |
| Q90 | 7 | input_form | "During fine-tuning, we double the examples in TRAIN by repeating each timeline twice, once for each summary." |
| Q91 | 7 | output_form | "For evaluation, we use the average timeline-level accuracy." |
| Q92 | 7 | input_form | "Although the BERT-based sequence classification model has a limitation when extracting long timelines due to its limited size of 512 positional embeddings, it performs better than the BERT-GRU sequence labeling model." |
| Q93 | 7 | input_form | "We attribute this to: 1) the careful preprocessing we did when constructing the sequences used to train the BERT-based sequence classification model, and 2) the limited data size, which might not enable the BERT-GRU model to fully capture the sequential relation-" |
| Q94 | 8 | output_form | "For timeline extraction results on the TEST set, we compare both the human-level performance and the best model's performance against experts' annotations." |
| Q95 | 8 | output_content | "To get the human-level performance on the TEST set, we average the performance of the two workers who agree most across all timelines in TEST." |
| Q96 | 8 | output_form | "The best timeline extraction model achieves 73.51 average timeline accuracy, whereas the human-level performance is 88.98." |
| Q97 | 8 | output_form | "This highlights the difficulty of the timeline extraction task and indicates that more involved models are needed to close the gap between model performance and human-level performance." |
| Q98 | 8 | output_form | "We evaluate all timeline summarization models with ROUGE (Lin and Och, 2004)." |
| Q99 | 8 | output_form | "The summarization output of each model is evaluated in a multi-reference setting against the two summaries written by the two workers who agree the most based on the timeline extraction labels." |
| Q100 | 8 | output_form | "We use SacreROUGE (Deutsch and Roth, 2020) to compute multi-reference ROUGE scores." |
| Q101 | 8 | output_form | "For the Seq2Seq pretrained models, we present results in two settings: 1) using the oracle timeline; and 2) using the extracted timeline from the best timeline extraction model." |
| Q102 | 8 | output_form | "In the oracle setting, we use the gold labels in the DEV set to identify tweets that are part of each timeline to the summarization models." |
| Q103 | 8 | output_form | "We further conducted a human evaluation to better assess the quality of the summaries." |
| Q104 | 8 | output_form | "We take the whole TEST set and we evaluate eight summaries per timeline: 1) the three human-written summaries; 2) three model-generated summaries using the three models we develop for timeline summarization in the oracle setting; 3) two summaries from random systems: a random tweet that is part of the timeline, and a summary from a randomly selected timeline that belongs to a different crisis domain." |
| Q105 | 8 | output_content | "Following a similar process in 3.2, we recruit a group of workers from MTurk with the same Location restriction (QC1), who can pass our pilot study as a qualification test." |
| Q106 | 8 | output_content | "Each summary was evaluated by five different workers on a scale from 1 to 5 across four axes: Coherence, Accuracy, Coverage, and Overall quality, as was done by Lai et al. (2022)." |
| Q107 | 8 | output_content | "Detailed instructions and annotation workflows are presented as Figures 15–21 in Appendix E." |
| Q108 | 8 | output_form | "Looking at the results over all the timelines, the human-written summaries are significantly better than the ones generated by models, in terms of overall quality with an average rating of 4.12." |
| Q109 | 9 | input_content | "We presented CrisisLTLSum, the first dataset on local crisis timelines extracted from Twitter and the first to provide human-written summaries on information extracted from Twitter." |
| Q110 | 9 | input_ontology | "We showed that CrisisLTLSum supports two downstream tasks: Timeline Extraction and Timeline Summarization." |
| Q111 | 9 | output_form | "Our experiments with SOTA baselines indicate that both of these tasks are challenging and encourage future research." |
| Q112 | 9 | input_ontology | "Our dataset further provides a resource for developing methods on utilizing microblogs toward aiding first-responders in evaluating ongoing crisis events." |
| Q113 | 9 | output_form | "For timeline extraction, 66 timelines (77%) have at least one error, in which 272 out of 958 tweets (28%) are wrong." |
| Q114 | 9 | output_form | "We observe that the model performance decreases with increasing timeline length for both timeline extraction and summarization tasks, with significant drops in accuracy and ROUGE scores when timelines get longer." |
| Q115 | 9 | output_form | "Most of the summarization errors were due to hallucinations or to copying specific sentences that are present in the timeline without covering all the important event details described in the timeline." |
| Q116 | 10 | input_content | "We thank Aoife Cahill for providing detailed feedback on this paper, Alison Smith-Renner and Wenjuan Zhang for helpful discussions on MTurk annotations, our colleagues at Dataminr, and the EMNLP reviewers for their helpful and constructive comments." |
| Q117 | 10 | input_content | "This study has some limitations on the dataset generation workflow. First, our noisy timeline collection process is not a comprehensive and exhaustive extraction to find all available information about a local crisis event. Here, our focus is to provide a representative dataset rather performing a comprehensive set containing all the local crisis events and their updates." |
| Q118 | 10 | input_form | "Second, the proposed noisy timeline collection pipeline is highly dependent to the performance of the entity extraction modules, especially for the location extraction, and the accuracy of the OpenStreetMap API to find the correct physical address of each location mention." |
| Q119 | 10 | input_form | "Accordingly, replicating the same process for other language or based on other locations may be hard because of such dependencies." |
| Q120 | 10 | output_form | "Furthermore, the online clustering method used in this paper has a set of hyperparameters which are tuned heuristically from a small set of experiments. More comprehensive and large scale experiments on tuning those parameters could potentially impact the quality of the generated timelines." |
| Q121 | 10 | input_content | "Generating similar results by following our noisy timeline collection process is in general limited by the users' access to the public Twitter stream and the changes in the available posts (they may become restricted or deleted)." |
| Q122 | 12 | input_ontology | "We build CrisisLTLSum by limiting the search to four crisis domains: wildfire, local fire, traffic, and storm." |
| Q123 | 12 | input_content | "We collect CrisisLTLSum across seven states in the USA and two states of Australia during 2020 and 2021. The selected states in the USA are New York, Illinois, Massachusetts, California, Texas, and Florida. From Australia, we have selected the states of New South Wales and Victoria." |
| Q124 | 13 | input_content | "These states are selected as they are some of the areas subject to the most events falling into our crisis domains of interest. California, Victoria, and New South Wales are mainly selected due to the abundance of wildfires in hot seasons. Texas and Florida have been selected as they are both subject to wildfires and storm events during different months. Massachusetts and Illinois are selected first because those areas are frequently subjected to bad weather, and second as they contain big cities subject to traffic and local fire events alongside New York." |
| Q125 | 13 | input_form | "This step selects the subset of filtered tweets related to a specific crisis category of interest. Ideally, this task can be performed by a neural model trained on a large set of tweets with labeled data indicating the categories. However, as such a large amount of labeled data is unavailable, we rely on a common approach of designing keywords." |
| Q126 | 13 | input_content | "We carefully curate a keyword list for each of our categories of interest by employing expert knowledge gathered through over-viewing crisis stories in news, social media, and related big disaster events of the past." |
| Q127 | 13 | input_content | "Please note that these lists are generic for each category and not specific to unique events. For instance, instead of defining keywords specific to an event called "Hurricane Ida", our keywords list includes phrases such as "fallen tree", "building collapse", or "storm"." |
| Q128 | 13 | input_form | "The quality of the keywords list is crucial to the final quality of the generated timelines, and we polish this list multiple times based on small sets of experiments before using them for the final task." |
| Q129 | 13 | input_form | "To avoid making a long list of keywords and ensure that different lexical formats of the same word are still considered in the keyword matching process, we maintain both a lower-cased and a lemittized version of the keywords and the tweet's text." |
| Q130 | 13 | input_form | "If any of the keywords exist in the text and in any of these formats, then the tweet is considered related to the category." |
| Q131 | 13 | input_form | "The multi-word keywords are not considered n-grams but as an indication that all the words in the keyword should exist in the text, even if not as a sequence." |
| Q132 | 13 | input_content | "This approach will not be comprehensive or exhaustive but rather representative of each crisis domain. Improving this method to be more encompassing is an area for future research." |
| Q133 | 13 | input_form | "We use the following parameters shared among all different domains: shashtag is set to 0.2 and sdist is 0.3. The simthreshold and timethreshold are set to 0.7 and 15 hours respectively. The timethreshold is reduced to 3 hours to avoid merging various accidents at different times but in the same location. The mindist and maxdist are set to 0.4 kilometer and 4 kilometer for fire and traffic events while having the larger range of 0.4 and 10 kilometers for the wildfire and storm extraction. The expirationthreshold is set to 15 hours and tweetthreshold is 4." |
| Q134 | 13 | input_content | "The online clustering approach may fail to properly relate some tweets due to missing entities, clustering method hyper-parameters, or the difference in the description of various angles of the same story." |
| Q135 | 13 | output_content | "To address this, we merge clusters by comparing all cluster heads with each other and combining those with a higher similarity score than a threshold shead. Additionally, we use human feedback to merge clusters where their similarity score is below shead but higher than a second hyper parameter s min head." |
| Q136 | 13 | input_form | "Here, the goal is to remove tweets from the same cluster with identical or similar text. The duplicate removal relies on a fuzzy string sequence-matching technique to compute the similarity between a pair of tweets. We simply go over each tweet sorted in chronological order and remove the ones that match any of the previous tweets in the same cluster with a matching score higher than dmatch." |
| Q137 | 13 | input_form | "Although the keyword filtering step would reduce the number of tweets unrelated to the category of interest, this step aims to further remove the unrelated clusters generated from the pipeline." |
| Q138 | 14 | input_content | "Our goal is to select 1000 clusters that contain enough tweets describing an evolving crisis event." |
| Q139 | 14 | input_form | "In particular, we first identify a "seed tweet" as the first observed post mentioning a local crisis event, then roughly check whether the following tweets in the cluster contain updates about the same event." |
| Q140 | 14 | input_ontology | "We select clusters across four crisis domains, including wildfire, fire, storm, and traffic, depending on how frequently each type of event happens in extracted noisy clusters." |
| Q141 | 14 | input_form | "We fine-tune BERT base uncased on a single GPU for 10 epochs with a learning rate of 5e-5, batch size of 32, a seed of 42, and a maximum sequence length of 512." |
| Q142 | 14 | input_form | "The GRU has one layer with a hidden size of 128. The model was trained for 50 epochs with early stopping after five epochs if the performance did not improve on the DEV set. We use a learning rate of 5e-5, a batch size of 16, and a seed of 42." |
| Q143 | 14 | input_form | "We fine-tune BART based on a single GPU for ten epochs with a learning rate of 5e-5, batch size of 16, a seed of 42, and a maximum target sequence length of 512." |
| Q144 | 14 | input_form | "During inference, we use beam search with a beam size of 4." |
| Q145 | 14 | output_content | "To ensure the workers have a good understanding of the QE dimensions listed in the rubrics, as shown in Figure 18, the workers are asked to pass a screening test before they can access the quality rating part of the task interface." |
| Q146 | 15 | input_content | "Table 8: Aggregated data statistics based on crisis domains and timeline lengths of the TRAIN, DEV, and TEST splits." |
| Q147 | 15 | output_content | "Once they answer the test question with the correct answer, the rating interface will show up, as shown in Figure 19." |
| Q148 | 15 | output_content | "In this page, we display the original tweet timeline on the left hand side of the rating interface." |
| Q149 | 15 | output_content | "Before displaying all the summaries and the rating options, to make sure the workers go over the timeline carefully, we ask them to use the length of the timeline to answer the last screening question before conducting the rating task." |
| Q150 | 15 | output_content | "The rating part of the interface is shown in Figures 20 and 21." |
| Q151 | 21 | output_ontology | "During this task, you will be reading a timeline that consists of a sequence of tweets describing an event and eight different summaries for the event in the timeline. You will rate the quality of each of the eight summaries by four axes: coherence, accuracy, coverage, and overall quality." |
| Q152 | 21 | output_content | "The rubrics below give specific guidance on how each axis should be rated. Please read the rubrics carefully before continuing to the task." |
| Q153 | 21 | output_ontology | "For each summary, answer the question "how coherent is the summary on its own?" on a scale 1 to 5. A summary is coherent if when read by itself, it's easy to understand and free of English errors. A summary is not coherent if it's difficult to understand what the summary is trying to say. Generally, it's more important that the summary is understandable than it being free of grammar errors." |
| Q154 | 21 | output_ontology | "Score of 1: The summary is impossible to understand. Score of 2: The summary has many mistakes or confusing phrasing. Score of 3: The summary has some mistakes or confusing phrasing that made it hard to understand. Score of 4: The summary is mostly clear with only a few minor mistakes or confusing phrasing. Score of 5: The summary is perfectly clear." |
| Q155 | 21 | output_ontology | "For each summary, answer the question "Does the factual information in the summary accurately match the information in the timeline?" on a scale of 1 to 5. A summary is accurate if it doesn't say things that aren't in the timeline, it doesn't mix up information, and generally is not misleading." |
| Q156 | 21 | output_ontology | "Score of 1: The summary is completely wrong, made up, or exactly contradicts what is written in the timeline. Score of 2: The summary says many things not mentioned in or contradicting the timeline. Score of 3: The summary says at least one crucial piece of information that is not in the timeline, or it contradicts something in the timeline. Score of 4: The summary says anything at all that is not mentioned in the timeline or contradicts something in the timeline. Score of 5: The summary has no incorrect statements or misleading implications." |
| Q157 | 21 | output_ontology | "For each summary, answer the question "How well does the summary cover the important information in the timeline?" on a scale of 1 to 5. A good summary has good coverage if it mentions the main information from the timeline that's important to understand the event. A summary has poor coverage if someone reading only the summary would be missing several important pieces of information about the event in the timeline." |
| Q158 | 21 | output_ontology | "Score of 1: The summary contains no information relevant to the timeline. Score of 2: The summary is missing many important pieces of information required to understand the timeline. Score of 3: The summary is missing at least one crucial piece of information required to understand the timeline. Score of 4: The summary is missing some important information from the timeline. Score of 5: The summary covers all of the important information required to understand the timeline." |
| Q159 | 21 | output_ontology | "For each summary, answer the question "How good is the summary overall at representing the timeline?" on a scale of 1 to 5. This encompasses all of the above axes, as well as the information included in the summary and if it has helped you understand the event. If it's hard to find ways to make the summary better, give the summary a high score. If there are lots of different ways the summary could be better, give the summary a low score." |
| Q160 | 21 | output_ontology | "Score of 1: The summary is terrible. Score of 2: The summary is a pretty bad representation of the timeline and needs significant improvement. Score of 3: The summary is an okay representation of the timeline, but could be significantly improved. Score of 4: The summary is a pretty good representation of the timeline, but it's not perfect. Score of 5: The summary is an excellent representation of the timeline." |
| Q161 | 21 | output_content | "Now you will review an example timeline and two associated summaries." |
| Q162 | 21 | output_content | "For each of the summaries, we have provided ratings on the four axes: coherence, accuracy, coverage, and overall quality with explanations for why these ratings were chosen." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://books.openbookpublishers.com/10.11647/obp.0032/chapter11.html |
| WEB-2 | https://www.theglobaleconomy.com/Ecuador/literacy_rate/ |
| WEB-3 | https://www.worldviewdata.com/countries/ecuador/literacy-rate |
| WEB-4 | http://www.mannaproject.org/ecuador |
| WEB-5 | https://iwgia.org/en/ecuador/5087-iw-2023-ecuador.html |
| WEB-6 | https://en.wikipedia.org/wiki/Provinces_of_Ecuador |
| WEB-7 | https://www.researchgate.net/figure/Geographic-map-of-Ecuador-Administratively-Ecuador-is-divided-in-24-provinces-containing_fig1_360575372 |
| WEB-8 | https://storyteller.travel/map-provinces-ecuador/ |
| WEB-9 | https://en.wikipedia.org/wiki/Cantons_of_Ecuador |
| WEB-10 | https://www.gestionderiesgos.gob.ec/ |
| WEB-11 | https://www.gestionderiesgos.gob.ec/wp-content/uploads/downloads/2024/05/Resol.SNGR-102-2024.pdf |
| WEB-12 | https://en.wikipedia.org/wiki/Demographics_of_Ecuador |
| WEB-13 | https://ieeexplore.ieee.org/document/7889589 |
| WEB-14 | https://tradingeconomics.com/ecuador/individuals-using-the-internet-percent-of-population-wb-data.html |
| WEB-15 | https://datareportal.com/reports/digital-2026-ecuador |
| WEB-16 | https://www.worlddata.info/america/ecuador/telecommunication.php |
| WEB-17 | https://www.sciencedirect.com/science/article/pii/S2352340920315729 |
| WEB-18 | https://www.researchgate.net/publication/312485537_System_for_monitoring_natural_disasters_using_natural_language_processing_in_the_social_network_Twitter |
| WEB-19 | https://doi.org/10.17632/4x37zz82k8 |
| WEB-20 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6484392/ |
| WEB-21 | https://arxiv.org/html/2410.06370 |
| WEB-22 | https://www.researchgate.net/publication/350720422_HumAID_Human-Annotated_Disaster_Incidents_Data_from_Twitter |
| WEB-23 | https://crisisnlp.qcri.org/ |
| WEB-24 | https://disasterlaw.ifrc.org/dmi/dmi_country/49 |
| WEB-25 | https://www.uil.unesco.org/en/litbase/basic-education-young-people-and-adults-ecuador |
| WEB-26 | https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/A7NVF7 |
| WEB-27 | https://www.mdpi.com/2076-3417/15/8/4330 |

---

