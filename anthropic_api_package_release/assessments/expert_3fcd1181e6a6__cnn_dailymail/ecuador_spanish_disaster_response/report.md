## Deployment Context

**Use case:** Timeline generation for coordination and evaluation of response efforts across time published in social media. The data would be tweets from natural disaster domain generated in Ecuadorian Spanish.
**Target population:** Latin American data and social analysts working at NGO and international organizations (e.g. Red Cross, UN OCHA) who seek to find how affected populations' needs evolve across time. They would be fluent in American English and Spanish, potentially speakers of different accents of Latin American Spanish.

# Validity Analysis: cnn_dailymail_rc
**Target context:** Ecuador Humanitarian Crisis Tweet Analysis — NGO/IO Analyst Deployment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ⚠ | 1 | Serious concern | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ⚠ | 1 | Serious concern | high |
| **Average** | **1.0** | | |

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

The CNN/Daily Mail Reading Comprehension benchmark is categorically misaligned with the Ecuador Humanitarian Crisis Tweet Analysis deployment across all six validity dimensions, all rated HIGH priority in the elicitation. The benchmark defines a single Cloze-style entity-fill-in task on formal English news articles averaging 763 tokens, with algorithmically-generated labels reflecting anglophone editorial conventions of two Western news outlets. The deployment requires temporally ordered narrative timeline generation from informal Ecuadorian Spanish tweets (with Kichwa entity tokens) anchored to parroquia/cantón/provincia administrative levels, validated by inter-operational humanitarian teams. Empirical sampling of the HuggingFace dataset confirms zero Spanish content, zero Latin American geographic coverage, zero humanitarian crisis content, and no human annotation. Every dimension scored 1. No partial reuse pathway is supported by the evidence — the benchmark and deployment share essentially no structural, content, or task overlap.

## Practical Guidance

### What This Benchmark Measures

The benchmark measures a narrow, well-defined construct: a model's ability to resolve entity references within a single English news document via Cloze-style fill-in [Q10, Q11, Q17, Q20]. It does not measure humanitarian crisis classification, multilingual processing, social-media register handling, geographic anchoring at sub-national administrative levels, temporal timeline generation, or operational-relevance judgment — the constructs the Ecuador deployment requires.

### Construct Depth

The benchmark probes its own narrow construct (document-internal entity reference resolution) at substantial depth, with ~1M datapoints [Q14], multiple model architectures (Deep LSTM, Attentive, Impatient Readers [Q39, Q44, Q54]), multiple baselines [Q22, Q32], length-sensitivity analysis [Q78], and qualitative attention-map error analysis [Q79–Q88]. However, it provides essentially zero evidence about any of the deployment's required constructs (humanitarian taxonomy, multilingual register handling, timeline coherence, institutional attribution, needs-evolution tracking).

### What Else You Need

Complete supplementation is required across all six dimensions. Specifically: (1) humanitarian crisis taxonomy benchmark with compound and socio-political crisis coverage (closest English-only analog: TREC-IS/CrisisBench [WEB-29]); (2) Ecuadorian Spanish crisis-tweet corpus with informal register and Kichwa-tokens (no existing benchmark per gap-7 search); (3) Ecuador-specific NER/geolocation evaluation grounded in HDX COD-AB P-codes [WEB-17]; (4) timeline-generation benchmark for Spanish disaster tweets (closest analog: CrisisFACTS [WEB-19], English-only); (5) inter-operational team annotation protocols across field coordinators, social analysts, and domain experts (no existing benchmark per gap-6 search); (6) LOPDP-compliant data governance framework [WEB-26] for processing tweet data from Ecuadorian residents.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark defines a single unified task — Cloze-style entity fill-in over a context document estimating p(a|c,q) [Q10] — and explicitly scopes itself to single-document linguistic relationship detection while excluding world knowledge and co-occurrence statistics [Q11, Q17]. There is no humanitarian crisis taxonomy, no disaster-type subdivision, no socio-political emergency category, and no compound-crisis structure. Empirical sampling confirms zero humanitarian content across 14 datapoints (US crime, UK culture, military affairs, celebrity features) [DATASET-D4, D5, D6, D8, D13]. The Ecuador deployment requires coverage of compound and socio-political crises scored by population impact and response-gap severity per the elicitation. This is a categorical mismatch on a HIGH-priority dimension.

**Strengths:**
- The task is well-scoped and internally coherent: the authors define a single, focused construct (document-internal entity reference resolution) [Q10, Q11, Q17, Q20], which provides clean evaluation signal for that narrow construct even if it does not transfer to humanitarian crisis taxonomy.

**Checklist:**

- **IO-1**: Required categories include disaster-type classification (volcanic, seismic, flooding/landslide), socio-political crises, and compound cascading events, prioritized by population impact and response-gap severity per the elicitation A1. — _Sources: WEB-1_
- **IO-2**: Yes — the source benchmark has no humanitarian crisis taxonomy at all. Q10 defines the task as p(a|c,q) entity fill-in; no disaster, emergency, or humanitarian-needs categories exist. Empirical sampling confirms zero crisis-domain content [DATASET-D4, D5, D6, D8, D13]. — _Sources: Q10, Q17, DATASET-D4, DATASET-D5, DATASET-D6, DATASET-D8, DATASET-D13_
- **IO-3**: Yes — the entire CNN/Daily Mail topic distribution (US crime, UK monarchy, celebrity features, Western military affairs) is irrelevant to the Ecuadorian humanitarian deployment context [DATASET-D4, D6, D11, D13]. — _Sources: DATASET-D4, DATASET-D6, DATASET-D11, DATASET-D13_
- **IO-4**: Documented gaps: no volcanic/seismic/flooding/landslide categories, no socio-political crisis categories, no compound-crisis structure, no needs-evolution dimension. These omissions constitute severe construct underrepresentation for the target deployment. — _Sources: Q10, Q17, WEB-1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q10] 'we seek to estimate the conditional probability p(a|c, q), where c is a context document, q a query relating to that document, and a the answer to that query.' (p.2)
- [Q11] 'we wish to be able to exclude additional information, such as world knowledge gained from co-occurrence statistics, in order to test a model's core capability to detect and understand the linguistic relationships between entities in the context document.' (p.2)
- [Q17] 'the focus of this paper is to provide a corpus for evaluating a model's ability to read and comprehend a single document, not world knowledge or co-occurrence.' (p.2)

*Web sources:*
- [WEB-1] SGR open event data 2010–2023 confirms Ecuador disaster types span volcanic, seismic, flooding, and landslide hazards across all sub-national levels
- [WEB-19] CrisisFACTS identified as closest crisis-timeline benchmark — but English-only and non-Ecuadorian

*Dataset analysis:*
- DATASET-D4: British graphic artist feature — no crisis relevance
- DATASET-D6: Frank Lloyd Wright/Salvador Dalí personality piece — entirely orthogonal to humanitarian taxonomy
- DATASET-D8: US criminal home invasion case — no disaster content
- DATASET-D13: US mass shooting — no humanitarian crisis category
- DATASET-D5: Chinese toy recall — consumer safety, not humanitarian crisis

</details>

**Information gaps:**
- Whether other CNN/Daily Mail subsets contain any disaster-relevant articles — not material since coverage would still be anglophone Western and English-only

**Requires expert verification:**
- Detailed humanitarian crisis taxonomy structure (e.g., compound-crisis sub-types) used by Red Cross Ecuador and OCHA in operational practice

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Content is exclusively drawn from CNN (~93k) and Daily Mail (~220k) English news articles 2007–2015 [Q4, Q9, Q14], with all geographic and institutional references rooted in US/UK contexts [DATASET-D1, D2, D11, D16]. Empirical sampling shows references to Philadelphia, Miami, Alaska, London, Heathrow, Andersen AFB, the US CPSC, and UK monarchy — with zero Ecuadorian content. The deployment requires precise anchoring to Ecuador-specific entities at parroquia/cantón/provincia level (1,499 parroquias, 221+ cantones, 24 provincias [WEB-3, WEB-5, WEB-6]) and recognition of agencies like SGR, COE, Cuerpo de Bomberos, GAD, MSP, IGEPN [WEB-15, WEB-1]. Kichwa-origin place names appear in tweets but no NLP resources exist for Kichwa [WEB-8, WEB-9]. This is a categorical, HIGH-priority content mismatch.

**Strengths:**
- The corpus is large-scale (~1M datapoints [Q14, Q16]) and drawn from real natural language — the authors explicitly contrast this with synthetic data approaches that fail to capture 'the complexity, richness, and noise of natural language' [Q6]. This scale and naturalism is a methodological strength, even though the specific content does not transfer.

**Checklist:**

- **IC-1**: Yes — the deployment requires Ecuador-specific cultural, geographic, and dialectal knowledge: parroquia/cantón/provincia disambiguation [WEB-3, WEB-5, WEB-6], recognition of SGR/COE/GAD/Cuerpo de Bomberos institutional handles [WEB-15], Kichwa-origin place names [WEB-8], and informal Ecuadorian Spanish register per elicitation A4. — _Sources: WEB-3, WEB-5, WEB-6, WEB-15, WEB-8_
- **IC-2**: No — content is anglophone Western news with anglophone editorial framing of even non-Western events [DATASET-D3, D12, D19]. There is no alignment with Ecuadorian or Latin American cultural context. — _Sources: DATASET-D3, DATASET-D12, DATASET-D19_
- **IC-3**: Yes — every sampled datapoint requires Western-specific knowledge: US police institutions [DATASET-D1], US Air Force bases [DATASET-D2, D10], UK monarchy and infrastructure [DATASET-D11], Western private military contractors [DATASET-D7, D18], US Consumer Product Safety Commission [DATASET-D16]. — _Sources: DATASET-D1, DATASET-D2, DATASET-D10, DATASET-D11, DATASET-D7, DATASET-D16_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotators were involved in benchmark construction; the benchmark's automated pipeline [Q3, Q16] precludes any regional input. Recruitment of Ecuadorian humanitarian analysts would be needed for any port.
- **IC-5**: Documented issues: zero Ecuadorian geographic coverage (24 provincias, 221+ cantones, ~1,499 parroquias absent [WEB-3, WEB-5, WEB-6]); zero Ecuadorian institutional coverage (SGR, COE, IGEPN, Cuerpo de Bomberos, GAD, MSP, Cruz Roja Ecuatoriana absent [WEB-15, WEB-16]); no Kichwa-origin entity tokens [WEB-8, WEB-10]. These constitute fundamental construct-irrelevant variance for the deployment. — _Sources: WEB-3, WEB-5, WEB-6, WEB-15, WEB-16, WEB-8, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q4] 'two new corpora of roughly a million news stories with associated queries from the CNN and Daily Mail websites.' (p.1)
- [Q9] 'Articles were collected starting in April 2007 for CNN and June 2010 for the Daily Mail, both until the end of April 2015.' (p.2)
- [Q14] 'We have collected 93k articles from the CNN and 220k articles from the Daily Mail websites.' (p.2)

*Web sources:*
- [WEB-3] Ecuador has 24 provincias requiring disambiguation
- [WEB-5] Ecuador has 221–222 cantones requiring sub-provincial anchoring
- [WEB-6] ~1,499 parroquias per INEC 2022 census
- [WEB-15] SGR is the primary Ecuadorian emergency management authority issuing COE resolutions
- [WEB-1] SGR open event data covers events 2010–2023 at province/cantón/parroquia level
- [WEB-8] Kichwa is extremely low-resource; first NLP dataset (Killkan) only released 2024
- [WEB-17] HDX Ecuador COD-AB provides authoritative P-code gazetteer absent from benchmark

*Dataset analysis:*
- DATASET-D1: Philadelphia/Miami police shooting — US institutional and geographic anchoring
- DATASET-D2: US Air Force F-15s and Russian bombers — US/Russian military, no Latin America
- DATASET-D11: Queen Elizabeth opens Heathrow Terminal 5 — UK monarchy and infrastructure
- DATASET-D16: US Consumer Product Safety Commission as institutional source — no SGR/COE analog
- DATASET-D17: BUPA UK healthcare; Spain mentioned only in European corporate context, not Latin America

</details>

**Information gaps:**
- Detailed informal Ecuadorian crisis abbreviation lexicon — partially documented in YAML (SGR, COE, EDAN, GAD, MSP, ARCOTEL) but population-level abbreviations require field elicitation

**Requires expert verification:**
- Specific Kichwa place-name tokens commonly appearing in crisis-time tweets in highland and Amazon provinces
- Costeño vs Serrano dialect distribution in tweet corpus during specific events

---

### Input Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Inputs are formal English news articles averaging 763 tokens with 27 entities per document [Q76], processed via tokenization into Deep LSTM encoders [Q40, Q42, Q43] with entity anonymization [Q18] that suppresses lexical surface form. Empirical sampling confirms uniformly formal journalistic English register with complete sentences and standard punctuation [DATASET-D14, D15, D18]. The deployment requires processing informal-to-semi-formal Ecuadorian Spanish tweets averaging ~280 characters, with non-standard orthography, missing diacritics, crisis abbreviations, and Kichwa entity tokens (per elicitation A4 and YAML). The HF metadata explicitly tags the dataset as `language:en` and `multilinguality:monolingual` (DATASET concern 1), confirming structural absence of Spanish content. The anonymization procedure [Q18] would explicitly suppress the dialect-specific entity signals critical for Ecuadorian anchoring. This is a categorical HIGH-priority form mismatch on language, register, length, and signal type.

**Strengths:**
- The benchmark documents its sensitivity to document length and entity density [Q76, Q78], providing methodological transparency about input characteristics — useful as a contrastive anchor when evaluating tweet-length systems.

**Checklist:**

- **IF-1**: Severe mismatch — source is formal English news prose at ~763 tokens [Q76]; target is informal Ecuadorian Spanish tweets at ~40–60 tokens with non-standard orthography, missing diacritics, and crisis abbreviations [WEB-12, elicitation A4]. — _Sources: Q76, DATASET-D14, DATASET-D15_
- **IF-2**: Regional infrastructure (Twitter/X access, ~78.2% internet penetration [WEB-12], ~57% smartphone penetration [WEB-14]) supports tweet capture, but the benchmark's signal specification (formal long-form English news) is not what regional infrastructure produces during crises. — _Sources: WEB-12, WEB-14_
- **IF-3**: Domain-specific differences: (a) language mismatch (English vs Spanish/Kichwa-influenced); (b) register mismatch (formal news vs informal crisis-time social media); (c) length mismatch (763 tokens vs ~50 tokens); (d) entity-anonymization procedure [Q18] would suppress diagnostic dialect-specific signals; (e) crisis-time connectivity disruptions create survivorship bias [WEB-12] absent from news data. — _Sources: Q18, Q56, WEB-8, WEB-10, WEB-12_
- **IF-4**: All four form mismatches (language, register, length, anonymization-induced signal suppression) constitute severe external validity violations for the deployment. — _Sources: Q18, Q76, DATASET-D14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q18] 'we anonymise and randomise our corpora with the following procedure, a) use a coreference system to establish coreferents… b) replace all entities with abstract entity markers according to coreference; c) randomly permute these entity markers' (p.3)
- [Q76] 'the average CNN validation document contained 763 tokens and 27 entities' (p.8)
- [Q56] 'The entity anonymisation and permutation aspect of the task… may end up levelling the playing field… favouring models capable of dealing with syntax rather than just semantics.' (p.6)

*Web sources:*
- [WEB-8] No NLP resources existed for Kichwa before 2024 Killkan ASR dataset
- [WEB-10] Kichwa agglutinative morphology creates context-dependent forms that compound NLP challenges
- [WEB-12] Internet penetration 78.2%, with crisis-time power outages disrupting telecom
- [WEB-14] Smartphone penetration ~57% nationally

*Dataset analysis:*
- DATASET-D14: Multi-clause formal English with institutional attribution (~30+ words per sentence)
- DATASET-D15: Formal attributed quotation in journalistic prose
- DATASET-D18: US English direct quotation, no register variation
- DATASET concern 1: HF metadata `language:en`, `multilinguality:monolingual` — structural absence of Spanish content

</details>

**Information gaps:**
- Specific orthographic-degradation patterns in Ecuadorian crisis-time tweets (deferred per YAML)

**Requires expert verification:**
- Field-analyst confirmation of Kichwa-Spanish code-switching patterns observed in actual SGR-tracked event tweet streams

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The output ontology is a closed entity-classification schema: select the correct anonymized entity token from candidates appearing in the context [Q34], scored by accuracy [Q22, Q52]. No structured label taxonomy, no humanitarian category hierarchy, and no temporal/needs-evolution structure exists. The authors themselves flag that the model cannot scale to multi-sentence inference [Q66, Q67] or world knowledge [Q74], and that 'many queries requiring complex inference and long range reference resolution' remain unsolved [Q75]. The deployment requires temporally ordered narrative timelines with phase transitions, geographic anchoring at parroquia level, institutional attribution, and humanitarian needs taxonomy across access/health/WASH/shelter/food/protection/telecoms/SAR dimensions (YAML output_task_requirements). DATASET concern 4 confirms no temporal sequencing or needs-evolution structure in any output field. This is a categorical HIGH-priority structural mismatch.

**Strengths:**
- The output space is well-defined and scoring is unambiguous (closed-vocabulary classification accuracy [Q22, Q52]) — a methodological strength for the benchmark's own narrow construct, but with no transferability to the deployment's open-ended timeline output.

**Checklist:**

- **OO-1**: Output labels are anonymized entity tokens drawn from individual documents [Q34] — no relevance to humanitarian timeline categories. — _Sources: Q34_
- **OO-2**: Missing categories include all needs-dimension labels (access, health, WASH, shelter, food, protection, telecoms, SAR per YAML), all phase-transition labels, all geographic-anchoring outputs at parroquia/cantón level [WEB-17], and all institutional-attribution labels [WEB-15]. — _Sources: WEB-17, WEB-15_
- **OO-3**: The token-level entity-prediction structure encodes anglophone editorial assumptions about what constitutes a 'salient' entity [DATASET-D19, D12] — selection of US foreign-policy actors over affected-population access/needs is a non-regional value embedded in the implicit ontology. — _Sources: DATASET-D12, DATASET-D19_
- **OO-4**: Stakeholder-driven taxonomy redesign would be required: an inter-operational team of field coordinators, social analysts, and domain experts (per elicitation A3) would need to define a humanitarian output taxonomy from scratch, since no benchmark category corresponds to deployment requirements.
- **OO-5**: The structural validity violation is total: the benchmark's output construct (single-token entity selection) and the deployment's output construct (multi-entity, temporally ordered, needs-typed narrative timeline) share no structural correspondence. — _Sources: Q34, Q66, Q74, Q75_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q34] 'p(a|d, q) ∝ exp (W(a)g(d, q)), s.t. a ∈ V, where V is the vocabulary' (p.4)
- [Q66] 'the frame-semantic approach does not trivially scale to situations where several sentences, and thus frames, are required to answer a query.' (p.7)
- [Q74] 'the incorporation of world knowledge and multi-document queries will also require the development of attention and embedding mechanisms whose complexity to query does not scale linearly' (p.8)
- [Q75] 'There are still many queries requiring complex inference and long range reference resolution that our models are not yet able to answer.' (p.8)

*Web sources:*
- [WEB-17] HDX Ecuador COD-AB provides admin-level 0–3 P-code structure absent from benchmark output ontology
- [WEB-19] CrisisFACTS is closest timeline benchmark but English-only — confirms timeline-generation taxonomy has no Spanish/Ecuador analog

*Dataset analysis:*
- DATASET concern 4: Output is Cloze entity fill-in or unordered bullet summaries — no temporal sequencing, no needs-evolution tracking, no operational relevance ranking
- DATASET concern 9: All highlights fields are unordered bullet lists with no phase structure

</details>

**Information gaps:**
- Detailed needs-evolution category schema used in Red Cross/OCHA Ecuador operational practice

**Requires expert verification:**
- Specific phase-transition labels (e.g., search-and-rescue → shelter → WASH) used by Ecuadorian inter-operational teams

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Ground-truth labels are generated entirely algorithmically by replacing entities in machine-extracted bullet summaries [Q3, Q16]; HF metadata explicitly tags `annotations_creators:no-annotation` (DATASET concern 5). No human annotation, no inter-annotator agreement, no demographic information, no humanitarian validation. The authors themselves acknowledge ambiguous queries that fail even under human evaluation [Q81, Q82, Q83, Q84], including geographic ambiguities like distinguishing administrative levels [Q82] — an acknowledged failure mode that maps directly to the Ecuador deployment's need for parroquia/cantón/provincia disambiguation. The deployment's authoritative quality standard is inter-operational team consensus across field coordinators, social analysts, and domain experts (elicitation A3, YAML). These two quality structures are categorically incompatible. HIGH-priority dimension.

**Strengths:**
- The benchmark documents specific failure modes including geographic ambiguity at multiple administrative levels [Q81, Q82] — providing a useful diagnostic frame even if the labels themselves do not transfer.

**Checklist:**

- **OC-1**: No — labels reflect anglophone editorial bullet-point conventions [Q3, Q16] generated by automated extraction with no human curation; they have no relationship to Ecuadorian humanitarian stakeholder perspectives. — _Sources: Q3, Q16, DATASET-D12, DATASET-D19_
- **OC-2**: Severe disagreement expected: anglophone editorial framing foregrounds political actors and Western institutional voices [DATASET-D12, D19], whereas humanitarian operational judgment foregrounds affected-population access, needs, and response gaps (per elicitation A3 and YAML output_task_requirements). — _Sources: DATASET-D12, DATASET-D19_
- **OC-3**: INSUFFICIENT DOCUMENTATION — the paper contains no human annotator pool [Q3, Q16]; HF metadata `annotations_creators:no-annotation` (DATASET concern 5) confirms structural absence of annotator demographics.
- **OC-4**: Re-annotation by the deployment's inter-operational team (field coordinators + social analysts + domain experts per elicitation A3) would be required, but no annotator infrastructure is documented — labels would need to be created from scratch on Spanish-language Ecuadorian content. — _Sources: WEB-21_
- **OC-5**: INSUFFICIENT DOCUMENTATION on aggregation — labels are not aggregated from multiple annotators because there is only the algorithmic extraction pipeline [Q16]. This precludes minority-perspective representation entirely.
- **OC-6**: Convergent validity is not assessable (no human labels to correlate); external validity is severely violated since algorithmic labels reflect editorial conventions of two Western news organizations only. — _Sources: Q16, Q81, Q82_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'summary and paraphrase sentences, with their associated documents, can be readily converted to context–query–answer triples using simple entity detection and anonymisation algorithms.' (p.1)
- [Q16] 'We construct a corpus of document–query–answer triples by turning these bullet points into Cloze [12] style questions by replacing one entity at a time with a placeholder.' (p.2)
- [Q81] 'ambiguous queries, where—at least following the anonymisation process—multiple entities are plausible answers even when evaluated manually.' (p.11)
- [Q82] 'the query searches for an entity marker that describes a geographic location… Here it is unclear whether the placeholder refers to a part of town, town, region or country.' (p.11)

*Web sources:*
- [WEB-15] SGR is the authoritative Ecuadorian emergency-management voice; analyst attribution requires distinguishing official from citizen sources
- [WEB-21] HumAID used Mechanical Turk crowd annotation, not humanitarian field experts — confirming gap in multi-role validation across all comparable benchmarks

*Dataset analysis:*
- DATASET concern 5: HF metadata `annotations_creators:no-annotation` confirms zero human annotation
- DATASET-D12: Highlight foregrounds Laura Bush political statement — illustrates anglophone editorial selection that humanitarian operational judgment would not endorse
- DATASET-D19: 'Laura Bush -- in a rare foray into foreign policy' — Wall Street Journal commentary framing

</details>

**Information gaps:**
- Whether any aggregated quality-control passes were performed on the bullet-point extraction — paper does not document any

**Requires expert verification:**
- Specific operational-relevance calibration patterns of Red Cross Ecuador and UN OCHA inter-operational teams for low-visibility high-value signals (e.g., rural road access reports)

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Output form is single-token classification accuracy on a closed entity vocabulary [Q34, Q52], with hyperparameter tuning on validation [Q58, Q60, Q61] and attention heat-map interpretability [Q79, Q85, Q86, Q87, Q88]. The deployment requires temporally ordered, multi-sentence narrative timeline summaries with geographic-anchoring precision, institutional-attribution accuracy, temporal coherence, operational-relevance calibration, and bilingual-workflow support per YAML output_task_requirements. The HF dataset's summarization variant produces unordered abstractive bullet lists [DATASET-D1, D5] — also not a temporal timeline. Even at the closest structural overlap (abstractive summarization), the form is misaligned: no temporal sequencing, no phase transitions, no needs-typed multi-sentence narrative output. Memory constraints prevented architectural depth experiments [Q69], and the authors flag the fixed-width hidden vector as an information bottleneck [Q45]. HIGH-priority dimension.

**Strengths:**
- Multiple evaluation strategies are defined (majority baselines [Q22], word-distance alignment [Q32, Q33], frame-semantic heuristics [Q29], attention models [Q49, Q50, Q51]), and length-sensitivity analysis is reported [Q78] — providing methodological scaffolding that could in principle be adapted, though not the output form itself.

**Checklist:**

- **OF-1**: No — expected output modality is single-token classification [Q34, Q52]; deployment requires multi-sentence temporally ordered narrative timeline (YAML output_task_requirements). — _Sources: Q34, Q52, DATASET concern 4_
- **OF-2**: Not applicable — deployment is text-based; analysts work in office/coordination-hub environments with no speech-output requirement (YAML device_and_connectivity_context_for_analysts).
- **OF-3**: Analyst literacy is high (professional NGO/IO data analysts) per YAML analyst_digital_literacy; not a constraint on output form. However, affected populations (tweet authors) include lower-literacy rural and indigenous communities (~5.4% national illiteracy, higher in rural areas [WEB-11]) — but this is an input concern, not output. — _Sources: WEB-11_
- **OF-4**: The categorical mismatch between single-token classification (or unordered bullet summarization) and temporally ordered narrative timelines violates external validity for the deployment use case. — _Sources: Q34, DATASET concern 4, WEB-19_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q34] 'p(a|d, q) ∝ exp (W(a)g(d, q)), s.t. a ∈ V, where V is the vocabulary' (p.4)
- [Q52] 'we next evaluate these models on our reading comprehension corpora.' (p.6)
- [Q45] 'The fixed width hidden vector forms a bottleneck for this information flow' (p.5)
- [Q69] 'Memory constraints prevented us from experimenting with deeper Attentive Readers.' (p.7)

*Web sources:*
- [WEB-19] CrisisFACTS represents the closest existing timeline benchmark — but English-only with no Latin American coverage
- [WEB-11] National illiteracy 5.4% (analyst-side literacy not a constraint)

*Dataset analysis:*
- DATASET concern 4: Cloze entity fill-in / abstractive bullets — neither is temporally ordered narrative timeline
- DATASET concern 9: Highlights are unordered bullet lists with no temporal sequencing or phase-transition labels
- DATASET-D1: Four-bullet US crime summary — no temporal evolution
- DATASET-D3: Pakistan martial law four-bullet summary — flat list of facts despite dynamic political crisis

</details>

**Information gaps:**
- Whether any extension of the benchmark task to multi-sentence generation has been published — the original paper does not include such an extension

**Requires expert verification:**
- Specific timeline-output format expectations of Red Cross Ecuador and OCHA situation-report consumers

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** No humanitarian crisis taxonomy; no Latin American disaster categories; no compound or socio-political crisis structure

**Recommendation:** Construct an Ecuador-specific crisis taxonomy in collaboration with Red Cross Ecuador and UN OCHA, drawing on SGR open event data 2010–2023 [WEB-1] and SGR hazard-guide structure [WEB-2], with explicit categories for compound and socio-political crises prioritized by population impact and response-gap severity per elicitation A1.

### Input Content ⚠

**Gap:** Zero Ecuadorian geographic, institutional, or dialectal content; no Kichwa-origin entity coverage

**Recommendation:** Build a Spanish-language Ecuadorian crisis-tweet corpus anchored to HDX COD-AB P-codes [WEB-17] covering all 24 provincias / 221+ cantones / ~1,499 parroquias [WEB-3, WEB-5, WEB-6], including SGR/COE/GAD/IGEPN/Cuerpo de Bomberos institutional handles [WEB-15, WEB-16] and Kichwa-origin place-name tokens with field-analyst validation given the Kichwa NLP resource gap [WEB-8, WEB-10].

### Input Form ⚠

**Gap:** Formal English news at ~763 tokens with entity anonymization; no Spanish, no informal register, no tweet-length inputs

**Recommendation:** Replace the input form entirely with informal Ecuadorian Spanish tweets at native length distribution, preserving non-standard orthography, missing diacritics, crisis abbreviations (SGR, COE, EDAN, GAD, MSP), and Kichwa-Spanish lexical mixing; do not apply entity anonymization, since dialect-specific surface forms are diagnostically critical.

### Output Ontology ⚠

**Gap:** Cloze entity fill-in has no correspondence to humanitarian timeline output structure

**Recommendation:** Design a structured output ontology with temporally ordered timeline entries typed by humanitarian needs dimensions (access, health, WASH, shelter, food, protection, telecoms, SAR), institutional attribution, and parroquia-level geographic anchoring; consult CrisisFACTS [WEB-19] as a methodological starting point while extending to Spanish/Ecuadorian context.

### Output Content ⚠

**Gap:** Algorithmic label generation with no human annotation and no humanitarian validation

**Recommendation:** Establish an inter-operational annotation protocol with field coordinators, social analysts, and domain experts (per elicitation A3) producing consensus labels on relevance, geographic anchoring, institutional attribution, and needs-evolution; document annotator demographics and inter-annotator agreement; comply with Ecuador LOPDP [WEB-26, WEB-27] for processing tweet data.

### Output Form ⚠

**Gap:** Single-token classification or unordered bullet summarization mismatched with temporally ordered narrative timelines

**Recommendation:** Adopt a multi-sentence temporally ordered narrative output form with phase-transition labels and bilingual (Spanish/English) presentation to support UN OCHA inter-agency reporting workflows; evaluate using timeline-coherence metrics adapted from CrisisFACTS [WEB-19] augmented with operational-relevance judgments from the inter-operational team.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "Machine reading systems can be tested on their ability to answer questions posed on the contents of documents that they have seen, but until now large scale training and test datasets have been missing for this type of evaluation." |
| Q2 | 1 | input_ontology | "In this work we define a new methodology that resolves this bottleneck and provides large scale supervised reading comprehension data." |
| Q3 | 1 | input_content | "We observe that summary and paraphrase sentences, with their associated documents, can be readily converted to context–query–answer triples using simple entity detection and anonymisation algorithms." |
| Q4 | 1 | input_content | "Using this approach we have collected two new corpora of roughly a million news stories with associated queries from the CNN and Daily Mail websites." |
| Q5 | 1 | input_content | "While obtaining supervised natural language reading comprehension data has proved difficult, some researchers have explored generating synthetic narratives and queries [3, 4]." |
| Q6 | 1 | input_content | "Historically, however, many similar approaches in Computational Linguistics have failed to manage the transition from synthetic data to real environments, as such closed worlds inevitably fail to capture the complexity, richness, and noise of natural language [5]." |
| Q7 | 1 | output_form | "These models draw on recent developments for incorporating attention mechanisms into recurrent neural network architectures [6, 7, 8, 4]." |
| Q8 | 1 | output_content | "Karl Moritz Hermann, Tomáš Kočiský, Edward Grefenstette, Lasse Espeholt, Will Kay, Mustafa Suleyman, Phil Blunsom are from Google DeepMind and University of Oxford." |
| Q9 | 2 | input_content | "Articles were collected starting in April 2007 for CNN and June 2010 for the Daily Mail, both until the end of April 2015. Validation data is from March, test data from April 2015. Articles of over 2000 tokens and queries whose answer entity did not appear in the context were filtered out." |
| Q10 | 2 | input_ontology | "The reading comprehension task naturally lends itself to a formulation as a supervised learning problem. Specifically we seek to estimate the conditional probability p(a\|c, q), where c is a context document, q a query relating to that document, and a the answer to that query." |
| Q11 | 2 | input_ontology | "For a focused evaluation we wish to be able to exclude additional information, such as world knowledge gained from co-occurrence statistics, in order to test a model's core capability to detect and understand the linguistic relationships between entities in the context document." |
| Q12 | 2 | input_content | "Such an approach requires a large training corpus of document–query–answer triples and until now such corpora have been limited to hundreds of examples and thus mostly of use only for testing [9]." |
| Q13 | 2 | input_content | "This limitation has meant that most work in this area has taken the form of unsupervised approaches which use templates or syntactic/semantic analysers to extract relation tuples from the document to form a knowledge graph that can be queried." |
| Q14 | 2 | input_content | "We have collected 93k articles from the CNN and 220k articles from the Daily Mail websites. Both news providers supplement their articles with a number of bullet points, summarising aspects of the information contained in the article." |
| Q15 | 2 | input_form | "Of key importance is that these summary points are abstractive and do not simply copy sentences from the documents." |
| Q16 | 2 | output_content | "We construct a corpus of document–query–answer triples by turning these bullet points into Cloze [12] style questions by replacing one entity at a time with a placeholder. This results in a combined corpus of roughly 1M data points (Table 1)." |
| Q17 | 2 | input_ontology | "Note that the focus of this paper is to provide a corpus for evaluating a model's ability to read and comprehend a single document, not world knowledge or co-occurrence." |
| Q18 | 3 | input_form | "To prevent such degenerate solutions and create a focused task we anonymise and randomise our corpora with the following procedure, a) use a coreference system to establish coreferents in each data point; b) replace all entities with abstract entity markers according to coreference; c) randomly permute these entity markers whenever a data point is loaded." |
| Q19 | 3 | input_form | "Clearly a human reader can answer both queries correctly. However in the anonymised setup the context document is required for answering the query, whereas the original version could also be answered by someone with the requisite background knowledge." |
| Q20 | 3 | input_ontology | "Therefore, following this procedure, the only remaining strategy for answering questions is to do so by exploiting the context presented with each question. Thus performance on our two corpora truly measures reading comprehension capability." |
| Q21 | 3 | output_ontology | "Table 2 gives an indication of the difficulty of the task, showing how frequent the correct answer is contained in the top N entity markers in a given document. Note that our models don't distinguish between entity markers and regular words. This makes the task harder and the models more general." |
| Q22 | 3 | output_form | "We define two simple baselines, the majority baseline (maximum frequency) picks the entity most frequently observed in the context document, whereas the exclusive majority (exclusive frequency) chooses the entity most frequently observed in the context but not observed in the query." |
| Q23 | 3 | input_ontology | "Traditionally, a pipeline of NLP models has been used for attempting question answering, that is models that make heavy use of linguistic annotation, structured world knowledge and semantic parsing and similar NLP pipeline outputs." |
| Q24 | 3 | input_ontology | "Frame-semantic parsing attempts to identify predicates and their arguments, allowing models access to information about "who did what to whom"." |
| Q25 | 4 | input_form | "makes use of frame-semantic annotations which we obtained by parsing our model with a state-of-the-art frame-semantic parser [13, 14]." |
| Q26 | 4 | input_form | "As the parser makes extensive use of linguistic information we run these benchmarks on the unanonymised version of our corpora." |
| Q27 | 4 | output_content | "There is no significant advantage in this as the frame-semantic approach used here does not possess the capability to generalise through a language model beyond exploiting one during the parsing phase." |
| Q28 | 4 | input_form | "Extracting entity-predicate triples—denoted as (e1, V, e2)—from both the query q and context document d, we attempt to resolve queries using a number of rules with an increasing recall/precision trade-off as follows (Table 4)." |
| Q29 | 4 | output_content | "Strategies are ordered by precedence and answers determined accordingly. This heuristic algorithm was iteratively tuned on the validation data set." |
| Q30 | 4 | input_form | "For reasons of clarity, we pretend that all PropBank triples are of the form (e1, V, e2). In practice, we take the argument numberings of the parser into account and only compare like with like, except in cases such as the permuted frame rule, where ordering is relaxed." |
| Q31 | 4 | output_form | "In the case of multiple possible answers from a single rule, we randomly choose one." |
| Q32 | 4 | output_form | "We consider another baseline that relies on word distance measurements. Here, we align the placeholder of the Cloze form question with each possible entity in the context document and calculate a distance measure between the question and the context around the aligned entity." |
| Q33 | 4 | output_form | "We tune the maximum penalty per word (m = 8) on the validation data." |
| Q34 | 4 | output_ontology | "We propose three neural models for estimating the probability of word type a from document d answering query q: p(a\|d, q) ∝ exp (W(a)g(d, q)), s.t. a ∈ V, where V is the vocabulary, and W(a) indexes row a of weight matrix W and through a slight abuse of notation word types double as indexes." |
| Q35 | 4 | input_ontology | "Note that we do not privilege entities or variables, the model must learn to differentiate these in the input sequence." |
| Q36 | 4 | input_form | "The function g(d, q) returns a vector embedding of a document and query pair." |
| Q37 | 4 | input_ontology | "Long short-term memory (LSTM, [18]) networks have recently seen considerable success in tasks such as machine translation and language modelling [17]." |
| Q38 | 4 | input_ontology | "When used for translation, Deep LSTMs [19] have shown a remarkable ability to embed long sequences into a vector representation which contains enough information to generate a full translation in another language." |
| Q39 | 4 | input_ontology | "Our first neural model for reading comprehension tests the ability of Deep LSTM encoders to handle significantly longer sequences." |
| Q40 | 4 | input_form | "We feed our documents one word at a time into a Deep LSTM encoder, after a delimiter we then also feed the query into the encoder. Alternatively we also experiment with processing the query then the document." |
| Q41 | 4 | input_ontology | "The result is that this model processes each document query pair as a single long sequence. Given the embedded document and query the network predicts which token in the document answers the query." |
| Q42 | 5 | input_form | "We employ a Deep LSTM cell with skip connections from each input x(t) to every hidden layer, and from every hidden layer to the output y(t):" |
| Q43 | 5 | input_form | "Thus our Deep LSTM Reader is defined by g^LSTM(d, q) = y(\|d\|+\|q\|) with input x(t) the concatenation of d and q separated by the delimiter \|\|\|." |
| Q44 | 5 | input_ontology | "The Deep LSTM Reader must propagate dependencies over long distances in order to connect queries to their answers." |
| Q45 | 5 | input_form | "The fixed width hidden vector forms a bottleneck for this information flow that we propose to circumvent using an attention mechanism inspired by recent results in translation and image recognition [6, 7]." |
| Q46 | 5 | input_form | "This attention model first encodes the document and the query using separate bidirectional single layer LSTMs [19]." |
| Q47 | 5 | input_form | "The encoding u of a query of length \|q\| is formed by the concatenation of the final forward and backward outputs, u = −→yq (\|q\|) \|\| ←−yq (1)." |
| Q48 | 5 | input_form | "For the document the composite output for each token at position t is, yd(t) = −→yd(t) \|\| ←−yd(t)." |
| Q49 | 5 | output_form | "The representation r of the document d is formed by a weighted sum of these output vectors." |
| Q50 | 5 | output_form | "These weights are interpreted as the degree to which the network attends to a particular token in the document when answering the query:" |
| Q51 | 5 | output_form | "The variable s(t) is the normalised attention at token t." |
| Q52 | 6 | output_form | "Having described a number of models in the previous section, we next evaluate these models on our reading comprehension corpora." |
| Q53 | 6 | input_ontology | "Our hypothesis is that neural models should in principle be well suited for this task." |
| Q54 | 6 | input_ontology | "We expect that the attention-based models would therefore outperform the pure LSTM-based approaches." |
| Q55 | 6 | input_ontology | "Considering the second dimension of our investigation, the comparison of traditional versus neural approaches to NLP, we do not have a strong prior favouring one approach over the other." |
| Q56 | 6 | input_form | "The entity anonymisation and permutation aspect of the task presented here may end up levelling the playing field in that regard, favouring models capable of dealing with syntax rather than just semantics." |
| Q57 | 6 | output_form | "With these considerations in mind, the experimental part of this paper is designed with a threefold aim. First, we want to establish the difficulty of our machine reading task by applying a wide range of models to it. Second, we compare the performance of parse-based methods versus that of neural models. Third, within the group of neural models examined, we want to determine what each component contributes to the end performance; that is, we want to analyse the extent to which an LSTM can solve this task, and to what extent various attention mechanisms impact performance." |
| Q58 | 6 | output_form | "All model hyperparameters were tuned on the respective validation sets of the two corpora." |
| Q59 | 6 | output_form | "Our experimental results are in Table 5, with the Attentive and Impatient Readers performing best across both datasets." |
| Q60 | 6 | output_form | "For the Deep LSTM Reader, we consider hidden layer sizes [64, 128, 256], depths [1, 2, 4], initial learning rates [1E−3, 5E−4, 1E−4, 5E−5], batch sizes [16, 32] and dropout [0.0, 0.1, 0.2]. We evaluate two types of feeds. In the cqa setup we feed first the context document and subsequently the question into the encoder, while the qca model starts by feeding in the question followed by the context document. We report results on the best model (underlined hyperparameters, qca setup)." |
| Q61 | 6 | output_form | "For the attention models we consider hidden layer sizes [64, 128, 256], single layer, initial learning rates [1E−4, 5E−5, 2.5E−5, 1E−5], batch sizes [8, 16, 32] and dropout [0, 0.1, 0.2, 0.5]." |
| Q62 | 6 | output_form | "For all models we used asynchronous RmsProp [20] with a momentum of 0.9 and a decay of 0.95." |
| Q63 | 7 | output_ontology | "While the one frame-semantic model proposed in this paper is clearly a simplification of what could be achieved with annotations from an NLP pipeline, it does highlight the difficulty of the task when approached from a symbolic NLP perspective." |
| Q64 | 7 | output_ontology | "First, the frame-semantic pipeline has a poor degree of coverage with many relations not being picked up by our PropBank parser as they do not adhere to the default predicate-argument structure." |
| Q65 | 7 | input_content | "This effect is exacerbated by the type of language used in the highlights that form the basis of our datasets." |
| Q66 | 7 | output_ontology | "The second issue is that the frame-semantic approach does not trivially scale to situations where several sentences, and thus frames, are required to answer a query." |
| Q67 | 7 | output_ontology | "This was true for the majority of queries in the dataset." |
| Q68 | 7 | output_ontology | "We expect that on other types of machine reading data where questions rather than Cloze queries are used this particular model would perform significantly worse." |
| Q69 | 7 | output_form | "Memory constraints prevented us from experimenting with deeper Attentive Readers." |
| Q70 | 8 | input_ontology | "The supervised paradigm for training machine reading and comprehension models provides a promising avenue for making progress on the path to building full natural language understanding systems." |
| Q71 | 8 | input_ontology | "We have demonstrated a methodology for obtaining a large number of document-query-answer triples and shown that recurrent and attention based neural networks provide an effective modelling framework for this task." |
| Q72 | 8 | output_form | "Our analysis indicates that the Attentive and Impatient Readers are able to propagate and integrate semantic information over long distances." |
| Q73 | 8 | output_form | "In particular we believe that the incorporation of an attention mechanism is the key contributor to these results." |
| Q74 | 8 | output_ontology | "However, the incorporation of world knowledge and multi-document queries will also require the development of attention and embedding mechanisms whose complexity to query does not scale linearly with the data set size." |
| Q75 | 8 | output_ontology | "There are still many queries requiring complex inference and long range reference resolution that our models are not yet able to answer." |
| Q76 | 8 | input_form | "Note that these examples were chosen as they were short, the average CNN validation document contained 763 tokens and 27 entities, thus most instances were significantly harder to answer than these examples." |
| Q77 | 10 | output_form | "The precise hyperparameters used for the various attentive models are as in Table 6. All models were trained using asynchronous RmsProp [20] with a momentum of 0.9 and a decay of 0.95." |
| Q78 | 10 | output_form | "To understand how the model performance depends on the size of the context, we plot performance versus document lengths in Figures 4 and 5. The first figure (Fig. 4) plots a sliding window of performance across document length, showing that performance of the attentive models degrades slightly as documents increase in length. The second figure (Fig. 5) shows the cumulative performance with documents up to length N, showing that while the length does impact the models' performance, that effect becomes negligible after reaching a length of ~500 tokens." |
| Q79 | 10 | output_form | "We expand on the analysis of the attention mechanism presented in the paper by including visualisations for additional queries from the CNN validation dataset below. We consider examples from the Attentive Reader as well as the Impatient Reader in this appendix." |
| Q80 | 10 | input_ontology | "Figure 6 shows two positive examples from the CNN validation set that require reasonable levels of lexical generalisation and co-reference in order to be answered. The first query in Figure 7 contains strong lexical cues through the quote, but requires identifying the entity" |
| Q81 | 11 | output_content | "Figures 8 and 9 show examples of queries where the Attentive Reader fails to select the correct answer. The two examples in Figure 8 highlight a fairly common phenomenon in the data, namely ambiguous queries, where—at least following the anonymisation process—multiple entities are plausible answers even when evaluated manually." |
| Q82 | 11 | output_content | "Note that in both cases the query searches for an entity marker that describes a geographic location, preceded by the word "in". Here it is unclear whether the placeholder refers to a part of town, town, region or country." |
| Q83 | 11 | output_content | "Figure 9 contains two additional negative cases. The first failure is caused by the co-reference entity selection process. The correct entity, ent15, and the predicted one, ent81, both refer to the same person, but not being clustered together. Arguably this is a difficult clustering as one entity refers to "Kate Middleton" and the other to "The Duchess of Cambridge"." |
| Q84 | 11 | output_content | "The right example shows a situation in which the model fails as it perhaps gets too little information from the short query and then selects the wrong cue with the term "claims" near the wrongly identified entity ent1 (correct: ent74)." |
| Q85 | 11 | output_form | "To give a better intuition for the behaviour of the Impatient Reader, we use a similar visualisation technique as before. However, this time around we highlight the attention at every time step as the model updates its focus while moving through a given query. Figures 10–13 shows how the attention of the Impatient Reader changes and becomes increasingly more accurate as the model" |
| Q86 | 12 | output_form | "Figure 7: Two more correctly answered validation set queries. The left example (entity ent315) requires correctly attributing the quote, which does not appear trivial with a number of other candidate entities in the vicinity. The right hand side shows our model is not afraid of Chuck Norris (ent164)." |
| Q87 | 12 | output_form | "Figure 8: Attention heat maps from the Attentive Reader for two wrongly answered validation set queries. In the left case the model returns ent85 (correct: ent67), in the right example it gives ent24 (correct: ent64). In both cases the query is unanswerable due to its ambiguous nature and the model selects a plausible answer." |
| Q88 | 12 | output_form | "Note how the attention is distributed fairly arbitraty at first, slowly focussing on the correct entity ent5 only once the question has sufficiently been parsed." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://datosabiertos.gob.ec/organization/sgr |
| WEB-2 | https://www.gestionderiesgos.gob.ec/biblioteca/ |
| WEB-3 | https://en.wikipedia.org/wiki/Provinces_of_Ecuador |
| WEB-4 | https://www.geopostcodes.com/country/ecuador/administrative-divisions/ |
| WEB-5 | https://en.wikipedia.org/wiki/Cantons_of_Ecuador |
| WEB-6 | https://grokipedia.com/page/List_of_cities_in_Ecuador |
| WEB-7 | https://storyteller.travel/map-provinces-ecuador/ |
| WEB-8 | https://arxiv.org/abs/2404.15501 |
| WEB-9 | https://ieeexplore.ieee.org/document/9532603/ |
| WEB-10 | https://cdt.org/wp-content/uploads/2025/06/2025-06-25-Quechua-Report-English-final.pdf |
| WEB-11 | https://www.statista.com/statistics/1322285/digital-illiteracy-ecuador/ |
| WEB-12 | https://freedomhouse.org/country/ecuador/freedom-net/2024 |
| WEB-13 | https://datareportal.com/reports/digital-2024-ecuador |
| WEB-14 | https://www.statista.com/statistics/1081753/smartphone-owners-ecuador/ |
| WEB-15 | https://www.gestionderiesgos.gob.ec/ |
| WEB-16 | https://www.gestionderiesgos.gob.ec/category/sgr/ |
| WEB-17 | https://data.humdata.org/dataset/cod-ab-ecu |
| WEB-18 | http://datosabiertos-gestionriesgosec.opendata.arcgis.com |
| WEB-19 | https://aclanthology.org/2025.acl-long.783.pdf |
| WEB-20 | https://crisisnlp.qcri.org/ |
| WEB-21 | https://crisisnlp.qcri.org/humaid_dataset |
| WEB-22 | https://huggingface.co/datasets/QCRI/CrisisBench-all-lang |
| WEB-23 | https://reliefweb.int/country/ecu |
| WEB-24 | https://www.unocha.org/latin-america-and-caribbean |
| WEB-25 | https://www.dlapiperdataprotection.com/index.html?t=law&c=EC |
| WEB-26 | https://www.clym.io/regulations/organic-law-on-the-protection-of-personal-data-lopdp-ecuador |
| WEB-27 | https://www.cosede.gob.ec/wp-content/uploads/2023/12/REGLAMENTO-GENERAL-A-LA-LEY-ORG%C3%81NICA-DE-PROTECCION-DE-DATOS-PERSONALES_compressed-1.pdf |
| WEB-28 | https://developer.twitter.com/en/developer-terms/policy |
| WEB-29 | https://github.com/firojalam/crisis_datasets_benchmarks |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** abisee/cnn_dailymail (config 3.0.0)
**Analysis date:** 2025-07-14
**Examples reviewed:** 14 from `train` split
**Columns shown:** article, highlights, id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | cnn_dailymail | 1 | highlights | "A man named as a suspect in the fatal shooting of a Philadelphia, Pennsylvania, police officer last week was captured at a shelter in Miami, Florida" | US domestic crime reporting anchored to US cities and police institutions | IC |
| D2 | cnn_dailymail | 2 | highlights | "Two U.S. Air Force F-15s escorted two Russian Bear long-range bombers out of an air exclusion zone off the coast of Alaska" | US/Russian military content; US geographic and institutional references only | IC |
| D3 | cnn_dailymail | 3 | highlights | "Pakistani President Pervez Musharraf orders troops to take a television station's equipment… Pakistani opposition leader Imran Khan says he's under house arrest" | South Asian political crisis coverage; anglophone editorial framing of non-Western event | IC, OC |
| D4 | cnn_dailymail | 4 | highlights | "British graphic artist's identity remains a mystery despite huge popularity. Feted by the art world and Hollywood celebrities count among his collectors." | UK arts/culture story; no crisis relevance | IO |
| D5 | cnn_dailymail | 5 | highlights | "State-run news agency: China orders an investigation by quality control agencies. Children who swallow the beads can become comatose or have seizures." | Consumer safety story; no humanitarian crisis taxonomy | IO |
| D6 | cnn_dailymail | 6 | highlights | "Frank Lloyd Wright wanted store magnate to sleep on porch. Salvador Dalí's stated ambitions were bigger than Napoleon's." | Personality/celebrity feature; entirely irrelevant to humanitarian deployment | IO |
| D7 | cnn_dailymail | 7 | highlights | "Erik Prince: 'There was definitely incoming small arms fire from insurgents'… Iraqi government says Blackwater guards killed 17, fired without provocation." | Iraq war contracting dispute; Western institutional actors, no Latin American context | IC |
| D8 | cnn_dailymail | 8 | highlights | "NEW: The 17-year-old suspect allegedly fired the fatal shot… Taylor died after being shot in home invasion last week." | US criminal case; no disaster/humanitarian content | IO |
| D9 | cnn_dailymail | 9 | highlights | "BUPA was founded in 1947 in response to plans to establish the NHS. The company's biggest base is in the UK but has customers in three continents." | UK/European healthcare company profile | IC |
| D10 | cnn_dailymail | 11 | highlights | "Air Force says 2 pilots in good condition after ejecting from plane. Emergency responders on scene of crash at Andersen Air Force Base." | US military aviation accident; Guam/US institutional context | IC |
| D11 | cnn_dailymail | 12 | highlights | "Queen Elizabeth opens Heathrow Airport's $8.6 billion new Terminal 5. The new building took more than 15 years to complete following protests." | UK infrastructure story; no crisis or Latin American relevance | IC |
| D12 | cnn_dailymail | 13 | highlights | "Laura Bush calls on Myanmar junta to 'step aside,' allow for a democracy. Military leaders must give up the 'terror campaigns' against its people." | US foreign policy commentary on Myanmar; anglophone editorial framing of political crisis | IC, OC |
| D13 | cnn_dailymail | 14 | highlights | "Police confiscate computers, examine information on Web sites. Gunman may have frequented the Westroads Mall, police say." | US mass shooting in Nebraska; no relevance to Ecuadorian crisis context | IO |
| D14 | cnn_dailymail | 3 | article | "The country is at a critical and dangerous juncture -- threatened by rising tensions and spreading terrorism, Musharraf said in a televised address to the nation after declaring martial law." | Political crisis description in formal English news register — contrasts with informal Ecuadorian Spanish tweet register | IF |
| D15 | cnn_dailymail | 1 | article | "Miami Police Officer Gil Gonzalez said Lewis 'had a Bible and was praying when we went to get him. He had a look of guilt, a look of shock.'" | Formal English journalistic prose; illustrates register mismatch with informal crisis tweets | IF |
| D16 | cnn_dailymail | 5 | article | "Scientists have found the highly popular holiday toy contains a chemical that, once metabolized, converts into the toxic 'date rape' drug GHB (gamma-hydroxy butyrate), Scott Wolfson, a spokesman with the U.S. Consumer Product Safety Commission (CPSC), told CNN." | Western institutional actor reference (CPSC); no analog to Ecuadorian emergency institutions (SGR, COE) | IC |
| D17 | cnn_dailymail | 9 | article | "BUPA is a leading healthcare company in the UK, Spain, Australia, Ireland, Hong Kong, Thailand, Malta and Saudi Arabia." | UK-centric healthcare company geography; Spain mentioned but in European commercial context, not Latin American crisis context | IC |
| D18 | cnn_dailymail | 7 | article | "There was no 'deliberate violence,' committed by Blackwater employees, he added. Still, when asked whether it is possible someone with Blackwater 'screwed up' in the incident, Prince replied, 'Certainly it's possible.'" | Direct quotation in US English journalism; illustrates that all content is English formal register | IF |
| D19 | cnn_dailymail | 13 | article | "U.S. first lady Laura Bush -- in a rare foray into foreign policy -- called on Myanmar's military junta to 'step aside'… in a commentary published in Wednesday's Wall Street Journal." | US foreign policy voiced through US media outlet; anglophone editorial framing of humanitarian crisis | OC |
| D20 | cnn_dailymail | 14 | article | "Hawkins fired more than 30 rounds, the police chief said. The shootings sent panicked holiday shoppers fleeing for cover." | US mass violence event; content type entirely absent from humanitarian timeline task requirements | IO |

---

### Deployment-Relevant Strengths

Given the categorical misalignment documented throughout the YAML and confirmed by every sampled example, the data shows essentially no deployment-relevant strengths for the Ecuador humanitarian tweet analysis use case. The one partial technical observation below is noted for completeness, but the evidentiary record does not support characterizing it as a meaningful asset.

#### Strength 1: Abstractive highlight-article pairing structure is formally analogous to summarization
- **Dimension(s):** OF
- **Observation:** The dataset encodes article–highlights pairs where highlights are abstractive summaries (not sentence extracts), which is structurally analogous to a summarization or timeline-entry generation task. The article and highlights fields are cleanly separated, making the format technically straightforward for evaluating whether a model can compress a document into key facts.
- **Deployment relevance:** This is the weakest possible form of structural relevance: the format is recognizable as a summarization benchmark, but the content, language, domain, output structure, and annotation methodology are all misaligned with the deployment. It provides no evidence that the benchmark would serve the timeline-generation use case.
- **Datapoint citations:**
  - [D1] Example 1 (cnn_dailymail, split=train): "Tip leads police to John Lewis at homeless shelter in Miami. Lewis is suspected in fatal shooting of Philadelphia Ofc. Charles Cassidy." — Highlights are abstractive and non-extractive, confirming the format, but the content is a US crime story with zero relevance to Ecuadorian crisis timelines.
  - [D5] Example 5 (cnn_dailymail, split=train): "State-run news agency: China orders an investigation by quality control agencies. Children who swallow the beads can become comatose or have seizures." — Highlights condense a multi-source news story into bullet facts, structurally similar to timeline entries, but the domain (Chinese toy safety recall) is entirely irrelevant.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete language mismatch — English only, no Spanish, no Kichwa
- **Dimension(s):** IF
- **Observation:** Every article and every highlight in all 14 sampled examples is monolingual English in formal journalistic register. The dataset HF metadata explicitly tags the dataset as `language:en` and `multilinguality:monolingual`. No Spanish-language content, no Ecuadorian dialect variation, no informal register, no crisis-time abbreviations, no Kichwa-origin entity tokens appear anywhere in the sample.
- **Deployment relevance:** The deployment processes Ecuadorian Spanish tweets in a mixed informal-to-semi-formal register, with Kichwa terms appearing in place and entity names. A benchmark with zero Spanish content cannot measure a system's ability to process the target input signal. This is a categorical, not marginal, misalignment.
- **Datapoint citations:**
  - [D14] Example 3 (cnn_dailymail, split=train): "The country is at a critical and dangerous juncture -- threatened by rising tensions and spreading terrorism, Musharraf said in a televised address to the nation after declaring martial law." — Formal English journalistic prose; no register overlap with informal Ecuadorian Spanish crisis tweets.
  - [D15] Example 1 (cnn_dailymail, split=train): "Miami Police Officer Gil Gonzalez said Lewis 'had a Bible and was praying when we went to get him. He had a look of guilt, a look of shock.'" — US English direct quotation in news article; no analog to informal tweet register.
  - [D18] Example 7 (cnn_dailymail, split=train): "There was no 'deliberate violence,' committed by Blackwater employees, he added." — US English formal prose; no Spanish, no dialect variation, no non-standard orthography.

#### CRITICAL Concern 2: No humanitarian crisis content — taxonomy entirely absent
- **Dimension(s):** IO
- **Observation:** Across all 14 examples, zero articles concern natural disasters, floods, volcanic eruptions, earthquakes, landslides, or humanitarian emergencies. Topics include a US police shooting (Ex. 1), a US-Russia military incident (Ex. 2), a Pakistani political crisis (Ex. 3), a British street artist (Ex. 4), a Chinese toy recall (Ex. 5), an egotists feature (Ex. 6), an Iraq contractor shooting (Ex. 7), two US criminal cases (Ex. 8, 10), a UK healthcare company (Ex. 9), a US military crash (Ex. 11), a Heathrow terminal opening (Ex. 12), a US foreign policy commentary (Ex. 13), and a US mall shooting (Ex. 14). Not a single example falls within the humanitarian crisis domain.
- **Deployment relevance:** The deployment requires a system that can identify, classify, and track humanitarian needs across disaster types prioritized by population impact and response-gap severity. No benchmark category exists for volcanic eruptions, seismic events, flooding, landslides, compound crises, or socio-political emergencies. The benchmark provides no signal for this task.
- **Datapoint citations:**
  - [D4] Example 4 (cnn_dailymail, split=train, label="British graphic artist's identity remains a mystery despite huge popularity"): — Arts/culture content with no crisis relevance whatsoever.
  - [D6] Example 6 (cnn_dailymail, split=train, label="Frank Lloyd Wright wanted store magnate to sleep on porch. Salvador Dalí's stated ambitions were bigger than Napoleon's."): — Personality feature; exemplifies the breadth of topic coverage that is entirely orthogonal to humanitarian crisis taxonomy.
  - [D8] Example 8 (cnn_dailymail, split=train, label="NEW: The 17-year-old suspect allegedly fired the fatal shot… Taylor died after being shot in home invasion last week."): — US criminal case; no disaster, no humanitarian needs, no geographic or institutional anchoring to Ecuador.
  - [D13] Example 14 (cnn_dailymail, split=train, label="Police confiscate computers, examine information on Web sites. Gunman may have frequented the Westroads Mall, police say."): — US mass shooting; no crisis taxonomy overlap.

#### CRITICAL Concern 3: No Ecuador-specific geographic or institutional entity coverage
- **Dimension(s):** IC
- **Observation:** All geographic references across all 14 examples are US, UK, or Western institutional locations (Philadelphia, Miami, Alaska, London, Heathrow, Omaha, Guam, Washington DC) or non-Latin American international locations (Pakistan, Iraq, Myanmar, China). No Ecuadorian province, cantón, parroquia, or community appears. No Ecuadorian emergency management institution (SGR, SNGRE, Cuerpo de Bomberos, COE, GAD) is referenced. No Latin American humanitarian organization branch (Cruz Roja Ecuatoriana, OCHA ROLAC) appears.
- **Deployment relevance:** Analysts require precise anchoring to Ecuador-specific administrative units and institutional actors. A system trained and evaluated on this benchmark has no exposure to the entity space it must handle in deployment. The gap extends to all sub-national administrative levels required for field coordination decisions (parroquia, cantón, provincia).
- **Datapoint citations:**
  - [D1] Example 1 (cnn_dailymail, split=train): "A man named as a suspect in the fatal shooting of a Philadelphia, Pennsylvania, police officer last week was captured at a shelter in Miami, Florida." — US city and police department references; no Latin American geography.
  - [D16] Example 5 (cnn_dailymail, split=train): "Scientists have found the highly popular holiday toy contains a chemical… Scott Wolfson, a spokesman with the U.S. Consumer Product Safety Commission (CPSC), told CNN." — US regulatory agency (CPSC); no analog to SGR, Cuerpo de Bomberos, or COE.
  - [D9] Example 9 (cnn_dailymail, split=train): "BUPA is a leading healthcare company in the UK, Spain, Australia, Ireland, Hong Kong, Thailand, Malta and Saudi Arabia." — Spain mentioned only in a European corporate context; no Ecuadorian health or emergency institutions.
  - [D11] Example 12 (cnn_dailymail, split=train): "Queen Elizabeth opens Heathrow Airport's $8.6 billion new Terminal 5." — UK infrastructure; no relevance to Ecuador's sub-national emergency management geography.

#### CRITICAL Concern 4: Output task is extractive entity fill-in, not temporal narrative timeline generation
- **Dimension(s):** OO, OF
- **Observation:** The benchmark's output structure (for the reading comprehension task described in the YAML) is Cloze-style entity token prediction — selecting a single anonymized entity from a closed candidate set. The HuggingFace dataset as hosted is structured for summarization (article → highlights), but neither the Cloze entity fill-in nor the abstractive highlight format corresponds to temporally ordered, multi-sentence narrative timeline generation. No temporal sequencing, no needs-evolution tracking, no operational relevance ranking, and no humanitarian category labeling is present in any output field.
- **Deployment relevance:** The deployment requires temporally ordered narrative timelines suited to NGO coordination workflows — a fundamentally different output structure. The benchmark provides no evaluation signal for timeline coherence, geographic anchoring precision, institutional attribution accuracy, or humanitarian needs taxonomy coverage. Even if the summarization format were adopted, the summaries are of US/UK news stories without any temporal disaster-event sequencing.
- **Datapoint citations:**
  - [D1] Example 1 (cnn_dailymail, split=train, highlights="Tip leads police to John Lewis at homeless shelter in Miami."): — Four-bullet summary of a US crime story; no temporal ordering of evolving needs, no humanitarian phase transitions.
  - [D5] Example 5 (cnn_dailymail, split=train, highlights="State-run news agency: China orders an investigation by quality control agencies."): — Four-bullet summary of a product recall; no timeline structure, no population needs tracking.
  - [D3] Example 3 (cnn_dailymail, split=train, highlights="NEW: President Musharraf orders troops to take a television station's equipment."): — Political crisis highlights in English; no temporal evolution of humanitarian needs, no geographic anchoring to operational units.

#### CRITICAL Concern 5: Ground-truth labels algorithmically generated with no humanitarian validation
- **Dimension(s):** OC
- **Observation:** The HF metadata confirms `annotations_creators:no-annotation` — highlights are machine-extracted from CNN/Daily Mail bullet points with no human annotation. No field coordinator, social analyst, domain expert, or humanitarian professional was involved in any label generation. The authoritative quality standard is entirely determined by anglophone editorial conventions of two Western news organizations.
- **Deployment relevance:** The deployment's authoritative quality standard is inter-operational team consensus across field coordinators, social analysts, and domain experts collectively judging relevance and summary quality for Ecuadorian crisis content. The benchmark's automated label generation provides no approximation of this multi-role humanitarian validation structure. The two quality standards are not merely different in degree — they are structurally incompatible.
- **Datapoint citations:**
  - [D19] Example 13 (cnn_dailymail, split=train): "U.S. first lady Laura Bush -- in a rare foray into foreign policy -- called on Myanmar's military junta to 'step aside'… in a commentary published in Wednesday's Wall Street Journal." — Highlight generated from US media editorial framing of a political crisis; operational relevance judgment by Ecuadorian field coordinators would produce categorically different outputs for analogous content.
  - [D12] Example 13 (cnn_dailymail, split=train, highlights="Laura Bush calls on Myanmar junta to 'step aside,' allow for a democracy."): — The highlight reflects US foreign policy editorial priority; an inter-operational humanitarian team would foreground civilian casualty data, displacement figures, and access constraints rather than a US official's political statement.
  - [D3] Example 3 (cnn_dailymail, split=train): "Pakistani opposition leader Imran Khan says he's under house arrest." — Anglophone editorial judgment selects political actors as salient; humanitarian operational relevance would foreground affected population access and needs over political actors' statements.

---

#### MAJOR

#### MAJOR Concern 6: Western institutional and cultural knowledge assumed throughout
- **Dimension(s):** IC
- **Observation:** Articles consistently assume familiarity with US and UK institutions, geographic conventions, and cultural references: the NFL (Ex. 8, 10), US Air Force base names (Elmendorf, Andersen, Eglin — Ex. 2, 11), US political figures (Laura Bush, Condoleezza Rice — Ex. 13), British cultural figures (Banksy, Queen Elizabeth — Ex. 4, 12), and Western legal and media institutions. No Latin American institutional context appears.
- **Deployment relevance:** A system benchmarked on this dataset will have learned entity and context associations rooted entirely in US/UK institutional knowledge. When applied to Ecuadorian crisis tweets referencing SGR, SNGRE, COE, GAD municipales, IGEPN, or Cruz Roja Ecuatoriana, the system's learned representations will have no grounding in these entities.
- **Datapoint citations:**
  - [D2] Example 2 (cnn_dailymail, split=train): "Two U.S. Air Force F-15s escorted two Russian Bear long-range bombers out of an air exclusion zone off the coast of Alaska, U.S. military officials said Wednesday." — US military institutional framing; no analog to Ecuadorian emergency management chain.
  - [D7] Example 7 (cnn_dailymail, split=train): "Blackwater CEO Erik Prince said Sunday that guards 'definitely' faced insurgent fire September 16." — US private military contractor context; no Latin American institutional analog.
  - [D11] Example 12 (cnn_dailymail, split=train): "Queen Elizabeth helped launch Heathrow's $8.6 billion new Terminal 5 on Friday." — UK monarchy and infrastructure; no relevance to Ecuadorian deployment context.

#### MAJOR Concern 7: Formal written English register categorically mismatched with informal Ecuadorian Spanish tweet stream
- **Dimension(s):** IF
- **Observation:** All 14 articles are written in formal journalistic English prose with complete sentences, standard punctuation, institutional attribution, and no orthographic variation. This is the maximum possible register distance from informal crisis-time Ecuadorian Spanish tweets, which feature truncated sentences, phonetic spelling, missing diacritics, crisis-specific abbreviations (SGR, COE, EDAN, GAD), and Kichwa-origin place name tokens.
- **Deployment relevance:** A system calibrated on this benchmark's register would likely treat informal tweet-style inputs as out-of-distribution noise, potentially filtering out the high-value low-visibility signals (road access reports, community water shortages in informal register) that the deployment specifically requires to surface.
- **Datapoint citations:**
  - [D14] Example 3 (cnn_dailymail, split=train): "The country is at a critical and dangerous juncture -- threatened by rising tensions and spreading terrorism, Musharraf said in a televised address to the nation after declaring martial law." — 30-word formal clause with institutional attribution; contrast with a hypothetical tweet: "sgr activa alerta roja en Portoviejo #Manabí inundaciones sectorElVerano sin agua."
  - [D15] Example 1 (cnn_dailymail, split=train): "Miami Police Officer Gil Gonzalez said Lewis 'had a Bible and was praying when we went to get him. He had a look of guilt, a look of shock.'" — Formal attributed quotation; no register overlap with crisis tweet shorthand.

---

#### MINOR

#### MINOR Concern 8: Article length (averaging hundreds of tokens) is architecturally mismatched with tweet-length inputs
- **Dimension(s):** IF
- **Observation:** Sampled articles are long-form news texts ranging from approximately 200 to over 1,000 words. Example 3 (Pakistan martial law) runs to several thousand characters. The benchmark is explicitly designed for documents averaging 763 tokens. Tweet inputs average 280 characters (approximately 40–60 tokens).
- **Deployment relevance:** A model architecture benchmarked on 763-token documents and optimized for that length distribution will not generalize directly to tweet-length inputs without architectural adaptation. The YAML documentation notes that the benchmark's own performance analysis shows sensitivity to document length (Q78), but the relevant regime for tweets is far shorter than anything in this dataset.
- **Datapoint citations:**
  - [D14] Example 3 (cnn_dailymail, split=train): "Hours after declaring a state of emergency Saturday, Pakistani President Pervez Musharraf ordered troops to take a television station's equipment and put a popular opposition leader under house arrest…" — Multi-paragraph article of approximately 1,200+ words; no architectural overlap with sub-100-token tweet processing.

#### MINOR Concern 9: No temporal sequencing or event-phase structure in any output
- **Dimension(s):** OO
- **Observation:** The highlights fields across all 14 examples are unordered bullet-point summaries with no timestamp, no event-phase label, no before/after sequencing, and no indication of evolving states. Even in the Pakistan martial law example (Ex. 3), which covers a dynamic political crisis, the highlights are a flat list of discrete facts without temporal ordering.
- **Deployment relevance:** The deployment requires not just summarization but temporal ordering of how affected populations' needs evolve — identifying phase transitions (e.g., from search-and-rescue to shelter to WASH needs). The complete absence of temporal structure in any benchmark output means this dimension of the deployment task has no analog in the benchmark at all.
- **Datapoint citations:**
  - [D3] Example 3 (cnn_dailymail, split=train, highlights="NEW: President Musharraf orders troops to take a television station's equipment. Pakistani opposition leader Imran Khan says he's under house arrest. President Musharraf says his actions are for the good of the country. White House calls Musharraf's emergency declaration 'disappointing'."): — Four unordered facts; no temporal sequencing, no phase-transition labels, no needs-evolution tracking structure.

---

### Content Coverage Summary

All 14 sampled examples are drawn from CNN and Daily Mail news articles covering US domestic crime and law enforcement (Examples 1, 8, 10, 14), US and allied military affairs (Examples 2, 11), non-Western political crises reported through US/UK editorial lens (Examples 3, 13), UK and European culture and business (Examples 4, 9, 12), US-adjacent international consumer safety (Example 5), Western celebrity/arts features (Example 6), and the Iraq War as covered by US media (Example 7). Every article is monolingual formal English. Geographic references are exclusively US, UK, and Western-allied institutional locations. No Latin American, Ecuadorian, or Spanish-language content appears in any form. No humanitarian disaster, natural hazard, emergency response, or crisis taxonomy content appears. Ground-truth highlights are algorithmically derived from editorial bullet points with no human annotation. The output structure is flat, unordered bullet summaries with no temporal sequencing. The content is entirely consistent with what the YAML documentation describes — and entirely misaligned with every priority dimension of the Ecuador humanitarian tweet analysis deployment.

---

### Limitations

- **Sample size:** 14 examples from a 287,113-example training split. While every sampled example is categorically misaligned with the deployment, the sample cannot confirm the precise distribution of topic categories across the full dataset. However, given the documented source constraint (CNN and Daily Mail articles, 2007–2015, English-only), there is no plausible mechanism by which Ecuador-specific, Spanish-language, or humanitarian crisis content could appear in any portion of the dataset.
- **Config version:** Only config `3.0.0` (summarization format) was sampled. Configs `1.0.0` and `2.0.0` may differ in preprocessing but share the same underlying article corpus and therefore the same language, geographic, and domain coverage constraints.
- **Cloze task not directly observable:** The HuggingFace dataset as hosted presents the summarization version (article + highlights), not the original Cloze entity fill-in version described in the benchmark paper. The entity anonymization procedure (replacing named entities with abstract markers like `ent5`, `ent85`) is not visible in the sampled data. This does not affect the validity assessment — both the summarization and Cloze versions share the same fundamental misalignments — but the specific anonymization artifacts described in the YAML cannot be directly observed in this sample.
- **Temporal range not confirmed in sample:** The YAML documents articles from April 2007 to April 2015. The sample does not include date metadata, so the temporal distribution of the 14 examples cannot be confirmed. This is not material to the validity assessment.
- **No Spanish-language content possible:** The confirmed monolingual English constraint (HF metadata `language:en`, `multilinguality:monolingual`) means no amount of additional sampling would surface Spanish-language content. The absence is structural, not a sampling artifact.

