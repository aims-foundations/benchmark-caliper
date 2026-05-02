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
| Output Form ✓ | 2 | Significant gaps | medium |
| **Average** | **1.3** | | |

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

CrisisLTLSum is fundamentally misaligned with the Ecuador humanitarian crisis social-media analyst deployment along five of six validity dimensions. Its taxonomy excludes all of Ecuador's priority crisis types (volcanic, seismic, landslide, flooding, displacement, complex emergencies); its content is entirely US/Australian English Twitter; its preprocessing pipeline is English-locked and the authors themselves flag non-portability [Q119]; its annotators were restricted to English-speaking countries [Q61], not the inter-operational humanitarian teams the deployment requires; and its evaluation rubric is anchored to English coherence [Q153]. The only dimension scoring above 2 is Output Form (surface text-based modality matches), and even there ROUGE and the human rubric require Spanish/genre adaptation. The benchmark's methodology — semi-automated cluster-then-refine, MTurk QC stack, four-axis summary rubric — is auditable and re-implementable as a template, but the artifact itself transfers essentially nothing usable to the deployment context.

## Practical Guidance

### What This Benchmark Measures

CrisisLTLSum measures whether a model can identify relevant, informative, non-redundant English tweets about US/Australian local fire, wildfire, traffic, and storm events given a seed tweet, and can produce abstractive English summaries scored on coherence, accuracy, coverage, and overall quality. Its strongest dimensions are Output Form (text-based binary + summary outputs match deployment modality) and the methodological transparency of its annotation and evaluation protocols.

### Construct Depth

The benchmark probes timeline-membership classification and abstractive event summarization to a moderate depth in its target context: it documents a 15-point model–human gap on extraction (88.98 vs 73.51 [Q96]) and reveals systematic model failure modes (hallucinations, length-related accuracy drops [Q114, Q115]). However, this depth is entirely within the US/Australian English short-duration local-event regime; it provides no evidence on long-running multi-phase events (volcanic alert sequences), Spanish-language signal processing, indigenous-language entity handling, or humanitarian-coordinator relevance criteria.

### What Else You Need

For Ecuador deployment, the benchmark cannot stand alone. Required supplementation: (1) Input Ontology — define a multi-class crisis taxonomy covering volcanic, seismic, landslide, flooding, displacement, and complex-emergency categories aligned with SNGR/IGEPN classifications; (2) Input Content — build a Ecuadorian Spanish crisis tweet corpus (extending UrbangEnCy [WEB-17]) with Kichwa/Shuar toponym annotation; (3) Input Form — replace AllenNLP/CoNLL03 NER with Spanish NER and develop or curate Kichwa entity recognition; (4) Output Ontology — redesign relevance categories around humanitarian operational salience (logistics, needs, displacement, coordination, alerts) elicited from Cruz Roja / OCHA SOPs; (5) Output Content — re-annotate via inter-operational teams of Ecuadorian field coordinators, social analysts, and domain experts; (6) Output Form — adopt Spanish-tokenization-aware ROUGE / multilingual BERTScore and align human rubric to OCHA situation-report and Cruz Roja appeal conventions.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark restricts itself to four crisis domains — wildfire, local fire, traffic, and storm [Q122] — and explicitly defines events as 'local' incidents 'bound to an exact location, such as a building, a street, or a county, and usually lasts for a short period' [Q12]. The Ecuador deployment's priority crisis types are volcanic eruptions, earthquakes, landslides, coastal/riverine flooding, mass displacement, and complex humanitarian emergencies — none of which appear in the benchmark taxonomy. The elicitation explicitly identifies large-scale humanitarian crises that 'exceed local response capacity' as the operational priority, structurally incompatible with the benchmark's local/short-duration framing. Storms have only partial overlap, and even there the benchmark's storm category was selected for North American contexts (Texas/Florida hurricanes, NSW storms) [Q124], not Andean lahares or tropical Pacific precipitation. An independent Ecuadorian Twitter monitoring system identified four distinct categories — volcanic, telluric (seismic), fires, and climatological — confirming that Ecuador's operational taxonomy diverges fundamentally [WEB-18].

**Strengths:**
- The taxonomy does include 'storm' and 'local fire' categories that have partial conceptual overlap with páramo fires and some Costa flooding scenarios in Ecuador [Q122, Q124]; the 'local' event framing [Q12] could apply to canton-level fire events in urban Ecuadorian contexts.

**Checklist:**

- **IO-1**: Required categories for Ecuador humanitarian deployment include volcanic eruptions and lahares (Cotopaxi, Tungurahua, Sangay), earthquake/aftershock sequences (Manabí 2016 type), landslides (movimiento en masa), coastal/riverine flooding (desbordamiento), mass displacement (including Venezuelan migration and volcanic exclusion zones), and complex humanitarian emergencies. The elicitation confirms these prioritized categories and notes they fall outside the benchmark's four-category set. — _Sources: WEB-18_
- **IO-2**: Yes — the benchmark omits all of Ecuador's priority geophysical and humanitarian crisis types. The authors confirm coverage is limited to wildfire, local fire, traffic, and storm [Q122], with no volcanic, seismic, landslide, displacement, or complex-emergency content. — _Sources: Q122, Q12, WEB-18_
- **IO-3**: Traffic incidents and US-style wildfire and storm categories are not operationally irrelevant in Ecuador per se but are tuned to a US/Australian event profile (Texas/Florida storms, California/NSW/Victoria wildfires [Q124]) that does not match Ecuadorian risk geography. — _Sources: Q124_
- **IO-4**: The benchmark structurally cannot evaluate model performance on volcanic eruption timelines, earthquake aftershock sequences, displacement events, or humanitarian emergencies. This is a content-validity violation for the deployment: the construct of 'crisis timeline' the benchmark measures is a strict subset of, and partially disjoint from, the construct relevant to Ecuadorian humanitarian coordinators. — _Sources: Q12, Q122, WEB-21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'Moreover, we focus on the extraction of local crisis events. The term "local" indicates that an event is bound to an exact location, such as a building, a street, or a county, and usually lasts for a short period.' (p.2)
- [Q122] 'We build CrisisLTLSum by limiting the search to four crisis domains: wildfire, local fire, traffic, and storm.' (p.12)
- [Q124] 'These states are selected as they are some of the areas subject to the most events falling into our crisis domains of interest. California, Victoria, and New South Wales are mainly selected due to the abundance of wildfires...' (p.13)

*Web sources:*
- [WEB-18] An Ecuador-specific Twitter monitoring system independently identified four distinct crisis categories — volcanic, telluric (seismic), fires, and climatological — diverging from the benchmark taxonomy
- [WEB-21] HumVI 2024 review confirms multilingual humanitarian disaster NLP datasets are dominated by English and natural disaster timelines in Spanish are a known sector-wide gap

</details>

**Information gaps:**
- Whether storm-category models trained on US/Australian data have any zero-shot transfer to Ecuadorian flooding or páramo storm contexts is empirically unknown.

**Requires expert verification:**
- The exact distribution of crisis types in the Ecuadorian humanitarian tweet stream (proportion volcanic vs. flooding vs. displacement) requires field stakeholder input from Cruz Roja Ecuatoriana / OCHA Ecuador.

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
All 10,610 tweets in the benchmark were collected from seven US states and two Australian states during 2020–2021 [Q123], selected explicitly because their event profiles match the benchmark's four crisis categories [Q124]. Tweet filtering relies on location candidates from US/Australian cities, towns, and 'famous neighborhoods' [Q30] and on English-curated keyword lists [Q126, Q127]. No Spanish-language, Latin American, indigenous-language, or humanitarian-organizational content is documented. The Ecuador deployment requires anchoring to parroquias, cantones, provincias, SNGR/SGR (renamed in 2024 [WEB-11]), Cruz Roja Ecuatoriana, IGEPN, INAMHI, and Kichwa/Shuar toponyms — none of which are present. The elicitation confirms US-default references would be 'operationally meaningless or misleading.' This is an instance-level content-validity violation that cannot be remediated through fine-tuning alone.

**Strengths:**
- The benchmark's clustering and filtering methodology (geographic+keyword+entity-based clustering) is documented in sufficient detail [Q28, Q30, Q31] to be re-implemented for Ecuador, providing a useful methodological template even though no instance content transfers.

**Checklist:**

- **IC-1**: Yes — Ecuador deployment requires Spanish-language content, Ecuadorian administrative geography (24 provinces [WEB-6], ~221–224 cantons [WEB-8, WEB-9], 1,500+ parroquias [WEB-8]), Ecuadorian institutional handles (SNGR/SGR [WEB-11], IGEPN, INAMHI, Cruz Roja Ecuatoriana), and Kichwa/Shuar place names. None are present in the benchmark. — _Sources: Q123, WEB-6, WEB-8, WEB-11_
- **IC-2**: Culturally sensitive content (e.g., 'damnificados', 'albergue', references to indigenous communities, displacement vocabulary) is entirely absent. The benchmark contains no Latin American or humanitarian-organizational instances. — _Sources: Q126, Q127_
- **IC-3**: All instances require US/Australian-specific knowledge: place names from California, Texas, Florida, New York, Illinois, Massachusetts, NSW, Victoria [Q123]; English-language emergency vocabulary; US/Australian agency references implicit in keyword lists [Q126]. — _Sources: Q123, Q30, Q126_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotator review of benchmark instances has been performed; the elicitation confirms an inter-operational team of Ecuadorian field coordinators would need to do this.
- **IC-5**: Documented: 100% of input instances are US/Australian English Twitter content [Q123]; transferability to Ecuadorian Spanish humanitarian context is essentially zero at the instance level. — _Sources: Q123, Q69, WEB-17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q123] 'We collect CrisisLTLSum across seven states in the USA and two states of Australia during 2020 and 2021. The selected states in the USA are New York, Illinois, Massachusetts, California, Texas, and Florida. From Australia, we have selected the states of New South Wales and Victoria.' (p.12)
- [Q30] 'The location filtering relies on a list of location candidates created by gathering cities, towns, and famous neighborhoods in a big area of interest.' (p.3)
- [Q126] 'We carefully curate a keyword list for each of our categories of interest by employing expert knowledge gathered through over-viewing crisis stories in news, social media, and related big disaster events of the past.' (p.13)
- [Q69] 'Out of these 1,000 annotated timelines (10,610 tweets) in CrisisLTLSum...' (p.5)

*Web sources:*
- [WEB-6] Ecuador has 24 provinces (Pichincha, Guayas, Manabí, etc.)
- [WEB-8] Ecuador has approximately 221 cantons and over 1,500 parroquias
- [WEB-11] National disaster authority renamed from SGR to SNGR in 2023–2024
- [WEB-12] Approximately 527,333 Kichwa speakers and 59,894 Shuar speakers per INEC 2010
- [WEB-17] UrbangEnCy is the only Ecuador-specific Spanish crisis tweet dataset, 25,500+ tweets, binary classification only

</details>

**Information gaps:**
- The proportion of operationally critical Ecuador crisis tweets in Kichwa or with Kichwa toponyms is not quantified in available sources.

**Requires expert verification:**
- Authoritative list of Ecuadorian institutional handles and parroquia-level toponyms; should be elicited from CONAIE, ECUARUNARI, SNGR, and Cruz Roja Ecuatoriana.

---

### Input Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark's preprocessing pipeline is English-specific throughout: AllenNLP NER trained on CoNLL03 [Q33], a BERT-based NER fine-tuned on English Twitter [Q35], OpenStreetMap location matching calibrated to US/Australian geography [Q36], English lemmatization and lowercasing [Q129], and English keyword matching [Q130]. The authors explicitly acknowledge: 'replicating the same process for other language or based on other locations may be hard because of such dependencies' [Q119]. The Ecuador deployment requires processing Ecuadorian Spanish with informal register, code-switching with Kichwa, non-standard orthography (the 2008 unified Kichwa alphabet is contested [WEB-1]), and Kichwa/Shuar toponyms for which no NLP resources exist [WEB-1, WEB-12]. No Kichwa pre-trained model or annotated corpus has been identified [domain_specific_notes]. BERT/BART tokenization is English-calibrated [Q86, Q141, Q143]. This is a fundamental external-validity violation: the entire signal-processing chain is built on assumptions that do not hold in the deployment.

**Strengths:**
- The benchmark transparently flags the language-locality dependency [Q119], giving downstream users a clear signal that the pipeline is not portable; and the modular architecture (NER → location augmentation → clustering → classification) [Q28] provides a re-implementable template if components are swapped for Spanish/Kichwa-aware equivalents.

**Checklist:**

- **IF-1**: Signal distributions differ substantially: benchmark is English Twitter with US/Australian place-name density; deployment is Ecuadorian Spanish with informal register, crisis-specific Spanish lexicon ('damnificados', 'albergue', 'desbordamiento', 'lahares'), and Kichwa/Shuar toponyms. — _Sources: Q33, Q129, WEB-13_
- **IF-2**: Ecuador has high mobile broadband (95.8% of mobile connections [WEB-15]) and ~77% national internet penetration [WEB-14], so Twitter/X capture is technically supported, but rural Oriente coverage is severely limited [infrastructure_notes]. The OSM location-augmentation step has unverified coverage quality for rural Ecuadorian parroquias. — _Sources: Q36, WEB-14, WEB-15_
- **IF-3**: Domain-specific form differences: Spanish-tokenization-aware NER is required; Kichwa toponym recognition is not supported by any documented NLP tool; the benchmark's CoNLL03-trained NER [Q33] will systematically miss Spanish entity mentions and Kichwa place names. — _Sources: Q33, Q35, WEB-1_
- **IF-4**: Documented: full pipeline mismatch on language, NER, location resolution, and tokenization. The authors' own limitation statement [Q119] concedes non-portability. — _Sources: Q119_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'we use a pre-trained neural model from AllenNLP (Gardner et al., 2018), trained on CoNLL03 (Tjong Kim Sang and De Meulder, 2003), to extract entities with types of people, location, and organization.' (p.3)
- [Q35] 'we further developed a BERT-based NER model tuned on Twitter data to detect location mentions.' (p.4)
- [Q36] 'We use OpenStreetMap API to map location mentions to physical addresses.' (p.4)
- [Q119] 'replicating the same process for other language or based on other locations may be hard because of such dependencies' (p.10)
- [Q129] 'we maintain both a lower-cased and a lemittized version of the keywords and the tweet's text.' (p.13)

*Web sources:*
- [WEB-1] Ecuadorian indigenous languages have official alphabets but written use outside schools is minimal; 2008 unified Kichwa orthography contested
- [WEB-13] First Ecuadorian Spanish NLP corpus exists (2017) but does not cover Kichwa
- [WEB-14] Ecuador internet penetration ~77.2% (2024)
- [WEB-15] 95.8% of Ecuador mobile connections on 3G/4G/5G as of end 2025
- [WEB-17] UrbangEnCy provides Ecuador-specific Spanish emergency tweets but only binary classification

</details>

**Information gaps:**
- Quality of OpenStreetMap coverage for Ecuadorian rural parroquias and Kichwa community names is not assessed in available sources.

**Requires expert verification:**
- Whether existing Spanish BERT variants combined with UrbangEnCy fine-tuning are operationally adequate for Ecuadorian crisis Twitter, and what resources would be needed to extend to Kichwa toponym recognition.

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The output ontology has two parts: a binary timeline-membership label defined by three conjunctive criteria — relevant, informative, not repetitive [Q58] — and a four-axis summarization rubric (Coherence, Accuracy, Coverage, Overall quality, each 1–5) [Q106, Q151]. The criteria are abstract enough to be conceptually portable, but their operationalization is English- and US-context-specific: 'informative' is defined as facts vs. 'personal points of view' [Q58], an annotation norm reflecting US MTurk-worker intuitions; the Coherence rubric explicitly references 'English errors' and English-language readability [Q153]. The deployment's relevance criteria for humanitarian coordinators (road access status, informal community broadcasts, displacement indicators, IGEPN alert level changes, damnificado counts at parroquia level — see operational_context_notes) are structurally richer than the benchmark's binary fact-vs-opinion split. The elicitation rated OO as HIGH priority precisely because relevance for humanitarian coordinators differs structurally from US annotator norms. Score is 2 rather than 1 because the four-axis summary rubric is conceptually adaptable to Spanish summary evaluation, even though its English anchoring would need to be replaced.

**Strengths:**
- The four-axis summary rubric (Coherence, Accuracy, Coverage, Overall) [Q106, Q151] is a reasonable, decomposable structure that could be re-anchored to Spanish humanitarian reporting norms; the explicit decomposition of relevance into three criteria [Q58] makes the operational definition transparent and auditable.

**Checklist:**

- **OO-1**: The binary relevance label and four-axis summary rubric are conceptually generic but operationally tuned to US English. Categories like 'informative' (facts vs. personal opinion) [Q58] do not capture humanitarian-coordinator distinctions such as 'logistical' vs. 'needs-assessment' vs. 'institutional-coordination' relevance [operational_context_notes]. — _Sources: Q58, Q151_
- **OO-2**: Missing categories for the deployment: road/bridge access status, informal community broadcast signals, displacement movement indicators, institutional coordination signals, casualty/damnificado counts at parroquia/cantón level, infrastructure damage to service delivery, official alert level changes (IGEPN color codes, SNGR declarations) — these are flagged in operational_context_notes as the actual relevance criteria for Ecuadorian humanitarian coordinators. — _Sources: WEB-21_
- **OO-3**: The Coherence rubric explicitly references 'English errors' and English-language comprehensibility [Q153], embedding a non-portable language assumption. The 'fact vs. personal point of view' distinction [Q58] reflects US journalistic norms and may misclassify community broadcasts (often first-person but operationally critical) as non-informative. — _Sources: Q58, Q153_
- **OO-4**: The elicitation indicates stakeholder-driven taxonomy redesign is necessary: an inter-operational team of Ecuadorian field coordinators, social analysts, and domain experts would need to define multi-class relevance categories aligned with humanitarian coordination workflows.
- **OO-5**: Documented: structural-validity concern (binary relevance is too coarse for humanitarian operational salience); content-validity concern (key humanitarian categories missing); external-validity concern (English-anchored coherence does not generalize to Spanish summary evaluation). — _Sources: Q58, Q153, Q106_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q58] 'A tweet is labeled as part of the timeline only if it satisfies all the following three conditions: relevant: talks about the same event indicated in the seed tweet, informative: provides facts about the event but not only contains personal points of view, not repetitive: brings in new information.' (p.5)
- [Q106] 'Each summary was evaluated by five different workers on a scale from 1 to 5 across four axes: Coherence, Accuracy, Coverage, and Overall quality...' (p.8)
- [Q151] '...rate the quality of each of the eight summaries by four axes: coherence, accuracy, coverage, and overall quality.' (p.21)
- [Q153] 'A summary is coherent if when read by itself, it's easy to understand and free of English errors.' (p.21)

*Web sources:*
- [WEB-21] HumVI review notes humanitarian event detection datasets disproportionately English; structural relevance categories for humanitarian work are underrepresented

</details>

**Information gaps:**
- No documented mapping from humanitarian-coordinator relevance categories (logistics, needs, displacement, coordination, casualties) to a multi-class extraction taxonomy exists.

**Requires expert verification:**
- The full set of relevance categories operationally used by Cruz Roja Ecuatoriana / OCHA Ecuador in tweet-stream analysis, and whether they are encoded in any internal SOPs.

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Ground-truth labels were produced by three MTurk workers per timeline [Q56, Q70], explicitly restricted to 'countries where native English speakers are most likely to be found' [Q61]. The two reference summaries used for ROUGE scoring were chosen as those written by the two most-agreeing workers [Q87, Q88]. Summarization quality ratings came from a separate pool of five MTurk workers under the same location restriction [Q105, Q106]. No Spanish-speaking, Latin American, or humanitarian-practitioner annotators participated. The Ecuador deployment requires inter-operational validation by teams of Ecuadorian field coordinators, social analysts, and domain experts — explicitly not a crowd-sourced English-speaker pool (elicitation A3, OC priority HIGH). Inter-annotator agreement of 90.06% [Q77] and 91.77% against experts [Q79] is internally high but provides no evidence about Ecuadorian-stakeholder agreement. This is a direct convergent-validity violation: the labels reflect a different population's judgments than the deployment requires.

**Strengths:**
- The benchmark documents annotator quality control thoroughly (QC1–QC4) [Q60, Q61, Q62, Q64, Q66] and reports both inter-worker and worker-vs-expert agreement [Q77, Q79], making the methodology auditable and providing a clear template that an Ecuador-specific re-annotation effort could replicate using inter-operational teams.

**Checklist:**

- **OC-1**: No — labels reflect English-speaking MTurk worker judgments [Q61], not Ecuadorian humanitarian-coordinator judgments. The elicitation explicitly identifies an inter-operational team as the authoritative judge. — _Sources: Q61, Q70_
- **OC-2**: Disagreement is likely substantial: humanitarian coordinators would weight informal community broadcasts, infrastructure-access signals, and displacement indicators more heavily than US MTurk workers, who applied a generic fact-vs-opinion rule [Q58]. — _Sources: Q58, Q61_
- **OC-3**: The benchmark documents annotator location restriction (English-speaking countries) [Q61], qualification testing [Q62], and quality monitoring [Q66], but provides no demographic breakdown beyond that. There is no Datasheet-level disclosure of country, professional background, or domain expertise. — _Sources: Q61, Q62, Q66_
- **OC-4**: Re-annotation by a representative Ecuadorian inter-operational team is required for deployment; the elicitation flags this as a HIGH priority gap.
- **OC-5**: Aggregation by majority vote across three workers [Q70] could erase minority perspectives; for humanitarian content where a single field-relevant signal in a tweet may be operationally critical, majority voting risks suppressing exactly the rare signals coordinators most need. — _Sources: Q70_
- **OC-6**: Documented: convergent-validity violation (labels do not correlate with deployment-population judgments) and external-validity violation (US-MTurk judgments do not generalize to humanitarian-coordinator context). — _Sources: Q61, Q105_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q56] 'Each HIT contains three noisy timelines, and we collect annotations from 3 different workers on each.' (p.5)
- [Q61] 'we use location restriction (QC1) to limit the pool of workers to countries where native English speakers are most likely to be found.' (p.5)
- [Q70] 'To make the ground-truth on whether each tweet is part of the timeline or not, we take the majority label among the three workers.' (p.6)
- [Q77] 'The average timeline-level agreement between those two workers is 90.06%.' (p.6)
- [Q105] 'we recruit a group of workers from MTurk with the same Location restriction (QC1)...' (p.8)

</details>

**Information gaps:**
- No documented annotator demographics beyond country-of-residence proxy; no comparison of MTurk worker labels against humanitarian-practitioner labels on any subset.

**Requires expert verification:**
- The actual labeling protocol used by Cruz Roja Ecuatoriana and OCHA Ecuador for tweet-relevance and summary-quality decisions, and whether existing inter-agency SOPs can be operationalized as an annotation protocol.

---

### Output Form — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
Output modalities — binary classification labels and abstractive text summaries [Q82, Q84] — match the deployment's text-based requirements at the surface level (elicitation rated OF as MODERATE, the only non-HIGH dimension). However, evaluation is via ROUGE n-gram overlap against English reference summaries [Q98, Q99] and an English-language human rubric [Q153], neither of which transfers cleanly to Spanish humanitarian reporting. Spanish-tokenization-aware ROUGE or multilingual BERTScore would be needed [evaluation_metric_adaptation], and UN OCHA / Red Cross situation reports follow specific genre conventions (numbered bullets, standardized headers, figures and percentages) that diverge from the abstractive summary style elicited in the benchmark [humanitarian_information_management]. Average timeline-level accuracy [Q91] as the extraction metric is generic and portable. The benchmark also does not penalize or evaluate language mismatch between input and output — so a system producing English summaries from Spanish tweets would not be flagged.

**Strengths:**
- Both tasks produce text outputs (binary labels, abstractive summaries) [Q82, Q84] matching deployment surface modality; multi-reference ROUGE setup [Q99, Q100] is methodologically sound and could be replicated against Spanish reference summaries; the four-axis human rubric [Q106] is decomposable and adaptable.

**Checklist:**

- **OF-1**: Surface modality matches: binary classification + abstractive text [Q82, Q84]. However, deployment requires bilingual output (English for OCHA/Red Cross global reporting, Spanish for Ecuadorian government coordination) — the benchmark does not evaluate language-conditioned generation. — _Sources: Q82, Q84_
- **OF-2**: Not applicable — speech-based output is not required; analyst population is high-literacy and produces written reports [literacy_and_education].
- **OF-3**: The analyst user population has high literacy in Spanish and English [literacy_and_education]; this dimension is not a barrier. Tweet-author population literacy is more variable [WEB-2, WEB-3, WEB-5] but affects input rather than output form. — _Sources: WEB-2, WEB-3_
- **OF-4**: Form mismatches: ROUGE is English-anchored [Q98]; human rubric refers to 'English errors' [Q153]; summary style does not match UN OCHA / Red Cross genre conventions; no evaluation of language-mismatch between Spanish input and required Spanish/English output. — _Sources: Q98, Q153_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q82] 'we define two tasks: Timeline Extraction and Timeline Summarization.' (p.6)
- [Q91] 'For evaluation, we use the average timeline-level accuracy.' (p.7)
- [Q98] 'We evaluate all timeline summarization models with ROUGE (Lin and Och, 2004).' (p.8)
- [Q99] 'The summarization output of each model is evaluated in a multi-reference setting against the two summaries written by the two workers who agree the most...' (p.8)
- [Q153] 'A summary is coherent if when read by itself, it's easy to understand and free of English errors.' (p.21)

*Web sources:*
- [WEB-2] Ecuador adult literacy ~94% (2022, World Bank)
- [WEB-3] Ecuador adult literacy ~96.3% (2022)

</details>

**Information gaps:**
- Whether Spanish-tokenization-aware ROUGE or BERTScore variants have been validated for humanitarian summary evaluation; what specific genre-convention checks UN OCHA / Cruz Roja apply to situation-report summaries.

**Requires expert verification:**
- Stylistic conventions and quality criteria for OCHA situation reports and Cruz Roja emergency appeals in Spanish that would need to be encoded in an adapted human evaluation rubric.

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Benchmark covers only wildfire, local fire, traffic, and storm; deployment priorities (volcanic, seismic, landslide, flooding, displacement, complex emergencies) are entirely absent.

**Recommendation:** Define an Ecuador-specific crisis taxonomy aligned with SNGR alert categories and IGEPN volcanic phases; do not use CrisisLTLSum scores as evidence of model capability on Ecuadorian disaster types.

### Input Content ⚠

**Gap:** All instances are US/Australian English Twitter from 2020–2021; no Ecuadorian Spanish, Kichwa toponym, or humanitarian-organization content is present.

**Recommendation:** Build a parallel Ecuadorian Spanish crisis timeline corpus by extending UrbangEnCy [WEB-17] with timeline structure and adding seed clusters for volcanic, seismic, and displacement events; curate parroquia/cantón/Kichwa-toponym lists with CONAIE/ECUARUNARI input.

### Input Form ⚠

**Gap:** Preprocessing pipeline (CoNLL03 NER, English BERT, OSM-on-US-geography, English lemmatization) is English-locked; the authors themselves flag non-portability [Q119].

**Recommendation:** Replace NER with Spanish-tuned models (e.g., Spanish BERT variants); add a Kichwa/Shuar toponym recognizer or gazetteer; validate OSM coverage on rural Ecuadorian parroquias and supplement with INEC administrative-unit databases.

### Output Content ⚠

**Gap:** Ground-truth labels and reference summaries produced by English-speaking-country MTurk workers [Q61] cannot serve as proxies for inter-operational humanitarian-team judgments required by the deployment.

**Recommendation:** Re-annotate a representative subset using inter-operational teams of Ecuadorian field coordinators, social analysts, and domain experts; replicate the documented QC1–QC4 protocol [Q60–Q66] but adapted for humanitarian practitioners; report agreement separately for each role to surface minority operational perspectives that majority voting would erase.

### Output Form

**Gap:** ROUGE and human rubric are English-anchored and do not match UN OCHA situation report or Cruz Roja appeal genre conventions.

**Recommendation:** Adopt Spanish-tokenization-aware ROUGE plus a multilingual semantic similarity metric (e.g., BERTScore-multilingual); add genre-convention checks (numbered bullets, standardized headers, parroquia-level damnificado figures) to the human rubric; evaluate language-fidelity (does Spanish input produce Spanish output) as an explicit axis.

### Output Ontology

**Gap:** Binary fact-vs-opinion relevance and English-anchored coherence rubric do not capture humanitarian-coordinator relevance categories or Spanish-language summary quality.

**Recommendation:** Redesign relevance as a multi-class taxonomy (logistics/access, needs, displacement, coordination, alerts, casualties) elicited from Cruz Roja Ecuatoriana and OCHA Ecuador SOPs; replace 'English errors' coherence anchor with Spanish-language fluency anchored to OCHA/Cruz Roja reporting genre conventions.

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

