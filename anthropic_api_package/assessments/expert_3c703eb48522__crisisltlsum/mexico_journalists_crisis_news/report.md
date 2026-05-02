## Deployment Context

**Use case:** Summarization of quick messages (e.g. tweets) for event reporting in the crisis domain for news writing in American English and Mexican Spanish mostly
**Target population:** Journalists and media workers who monitor social media to cover breaking news from Mexico City. They would speak Mexican Spanish natively (possible neutral/standard regional variety), and English fluently. They would be expected to use the model in English and Spanish to cover news of disasters happening not only in Mexico, but also south of the United States and also Central America.

# Validity Analysis: crisisltlsum
**Target context:** Mexico City and Central America Bilingual Crisis Journalism
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 3 | Moderate gaps | medium |
| Output Ontology | 2 | Significant gaps | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ⚠ | 1 | Serious concern | high |
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

CrisisLTLSum is a fundamentally English-language, US/Australian-anchored crisis-tweet benchmark whose four-domain ontology (wildfire/local fire/traffic/storm) [Q1, Q122], English-keyword-filtered content [Q126], English NER + OpenStreetMap pipeline [Q35, Q36], Anglophone MTurk annotators [Q61], English-anchored coherence rubric [Q153], and English-only ROUGE evaluation [Q99, Q100] together create severe validity gaps for the target deployment of bilingual crisis journalism in Mexico City and Central America. The structurally important crisis types for the deployment area — earthquakes, volcanic activity (Popocatépetl), tropical-system flooding, civil unrest, and CDMX transportation infrastructure failures — are entirely absent from the benchmark [WEB-7, WEB-20, WEB-23]. The Spanish-language output requirement (one of two deployment languages) receives zero coverage from the benchmark's evaluation framework. Of the six dimensions, five are scored 1–2 (high concern) and only Input Form scores 3 due to modality match. The authors themselves acknowledge non-portability to other languages and regions [Q119].

## Practical Guidance

### What This Benchmark Measures

CrisisLTLSum measures, for English-language US/Australian tweets in four crisis domains (wildfire, local fire, traffic, storm), how well systems can (a) extract relevant non-redundant updates from a noisy tweet stream given a seed tweet [Q5, Q83] and (b) produce abstractive summaries scored against multi-reference human summaries [Q98, Q99]. Within that English/US scope, it provides defensible signal: 90%+ inter-annotator agreement [Q77] and a 73.51% vs. 88.98% model-vs-human gap [Q96] indicate the tasks are non-trivial and well-instrumented. For the target deployment, the benchmark's English-output evaluation framework can serve as a starting point for the English half of the bilingual requirement.

### Construct Depth

Construct depth is shallow for the target deployment. The benchmark probes timeline extraction and summarization only on English tweets in four event types with no Spanish content, no journalist annotators, no editorial-style axes, no semáforo or SASMEX vocabulary, and no register-appropriateness metric. Even where the benchmark provides defensible signal (English summarization quality on fire/traffic/storm events), it does not address whether systems handle Mexican Spanish, voseo, code-switching, alcaldía/colonia toponymy, CENAPRED/SSN attribution, the #Verificado19S verification-tweet genre, or AP Español register conformance. The Coherence rubric [Q153] is structurally inapplicable to Spanish output. Strongest dimension is Input Form (modality match); weakest are Input Ontology, Input Content, Output Content, and Output Form — all of which would need substantial supplementation.

### What Else You Need

A complete assessment requires: (1) construction of a Spanish-language crisis tweet corpus anchored to Mexican/Central American events covering earthquakes, volcanic activity, tropical flooding, and civil unrest (no such corpus currently exists per [WEB-3, WEB-4]); (2) re-annotation by Mexican journalist annotators using an extended relevance/informativeness rubric that accounts for verification posts [WEB-23] and community solidarity posts; (3) a Spanish coherence rubric and AP Español–aligned register/attribution axes to replace [Q153]; (4) a bilingual summarization evaluation protocol using BERTScore-multilingual and LLM-as-judge alongside ROUGE [WEB-17, WEB-18]; (5) Spanish gazetteer integration for alcaldía/colonia/municipio resolution to replace the OSM-English pipeline [Q36]; and (6) explicit handling of SASMEX/CENAPRED hashtag and semáforo vocabulary as seed-tweet types [WEB-7, WEB-20].

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark's input ontology is restricted to four crisis domains — wildfire, local fire, traffic, and storm [Q1, Q53, Q122] — explicitly chosen because they are the most frequent in the selected US and Australian states [Q124]. For the target deployment, the elicitation and regional research identify earthquakes, volcanic activity, tropical-system flooding, civil unrest, and CDMX-specific transportation infrastructure failures as structurally important crisis types. Earthquakes are central to CDMX coverage given the 1985, 2017, and 2022 events, and Popocatépetl produces near-continuous low-level activity that yields a constant tweet stream rather than discrete spike events [WEB-7, WEB-20, WEB-26]. Even nominally overlapping categories (storms) carry different regional profiles: Mexican/Central American tropical systems use distinct alert vocabularies (semáforo phases, SMN/CONRED naming) that are not represented [WEB-19]. The 'local' definition (building/street/county, short-lived) [Q12] also conflicts with persistent volcanic phenomena and multi-day tropical systems. The taxonomy is therefore both under-representative (missing required categories) and structurally mismatched on the categories it does include.

**Strengths:**
- Three of the four covered domains (local fire, traffic, storms) have at least nominal applicability to CDMX urban crisis coverage [Q53, Q122], so timeline/summarization patterns learned on those event types may partially transfer for those specific event types in urban contexts.

**Checklist:**

- **IO-1**: Required categories for the target region include earthquakes, volcanic activity (with semáforo phase vocabulary), tropical-system flooding, civil unrest/protests, organized-crime-related public-safety events, and CDMX transportation infrastructure failures, in addition to fire/traffic/storm [WEB-7, WEB-20, elicitation A1]. — _Sources: WEB-7, WEB-20_
- **IO-2**: Yes — earthquakes, volcanic activity, tropical-system flooding, and civil unrest are entirely absent from the benchmark's four-domain ontology [Q1, Q53, Q122]. The Popocatépetl semáforo vocabulary and SASMEX seed-tweet conventions have no analog in the benchmark [WEB-7, WEB-20]. — _Sources: Q1, Q53, Q122, WEB-7, WEB-20_
- **IO-3**: No category in the benchmark is wholly irrelevant to the target region — wildfires, local fires, traffic, and storms all have regional analogs [Q122] — but the 'storm' category as operationalized via US keyword lists [Q126, Q127] carries US-specific damage profiles that may not transfer. — _Sources: Q122, Q124_
- **IO-4**: Construct underrepresentation is severe: four of the highest-priority crisis types in the deployment area (earthquake, volcanic, tropical flooding, civil unrest) are missing. The 'local' scope definition [Q12] also excludes persistent volcanic activity, which is structurally central to CDMX coverage [WEB-26]. — _Sources: Q1, Q12, WEB-26_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'CrisisLTLSum contains 1,000 crisis event timelines across four domains: wildfires, local fires, traffic, and storms.' (p.1)
- [Q12] 'The term "local" indicates that an event is bound to an exact location, such as a building, a street, or a county, and usually lasts for a short period.' (p.2)
- [Q53] 'The selected clusters cover events mainly from four crisis domains, including wildfire, local fire, storm, and traffic.' (p.5)
- [Q122] 'We build CrisisLTLSum by limiting the search to four crisis domains: wildfire, local fire, traffic, and storm.' (p.12)
- [Q124] 'These states are selected as they are some of the areas subject to the most events falling into our crisis domains of interest.' (p.13)

*Web sources:*
- [WEB-7] SASMEX disseminates earthquake alerts via standardized hashtags (#TenemosSismo, #AlertaSismica) reaching ~25M people — a structurally distinct seed-tweet ecosystem absent from the benchmark
- [WEB-20] CENAPRED's Popocatépetl semáforo system uses a seven-phase color-coded volcanic alert vocabulary not represented in benchmark categories
- [WEB-26] Popocatépetl is at Amarillo Fase 2 with ongoing daily exhalations (167 on April 28, 2026), indicating persistent rather than spike-event tweet streams

</details>

**Information gaps:**
- Frequency of cartel/organized-crime crisis events in tweet streams is undocumented in indexed sources
- Relative weighting of missing categories vs. the four covered ones in actual journalist workflow not quantified

**Requires expert verification:**
- Whether outlet-specific editorial priorities further alter category importance ranking

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
All input content was collected from seven US states and two Australian states during 2020–2021 [Q123], using English-language keyword lists curated from English news and social media [Q126, Q127], English Twitter NER models [Q35], and OpenStreetMap location augmentation anchored to US/Australian gazetteers [Q30, Q36]. The authors themselves note that replication for other languages or regions would be difficult [Q119]. For the target deployment, no Mexican or Central American content is present; Mexican administrative geography (16 alcaldías, colonias, 32 estados, municipios) and Central American departamentos/municipios are entirely absent. The web research confirms that no Spanish-language crisis tweet corpus anchored to Mexican or Central American events exists [WEB-3, WEB-4, WEB-6]. Mexican Spanish Twitter conventions (diacritic dropping, regional vocabulary like 'temblor'/'sismo'/'edomex', SASMEX hashtags #TenemosSismo, voseo in Central America, code-switching at the border) are entirely unrepresented in the benchmark's content [WEB-7, WEB-8]. The keyword-filtering pipeline is also acknowledged as not comprehensive [Q132], and its effectiveness depends on English-curated lists [Q128].

**Strengths:**
- The general principle of geographic and temporal focus (specific area × domain × time period) [Q29, Q32] is methodologically transferable, even though the specific filters used are US-anchored.
- The benchmark explicitly acknowledges its non-replicability for other languages/regions [Q119], providing transparency that supports informed adaptation decisions.

**Checklist:**

- **IC-1**: Yes — target inputs require Mexican Spanish dialectal knowledge, alcaldía/colonia/municipio toponymy, Central American voseo, indigenous-language place names (Nahuatl, Zapotec, Maya, Mam, K'iche'), and SASMEX/CENAPRED hashtag conventions, none of which are present in benchmark content [Q123, WEB-4, WEB-7]. — _Sources: Q123, WEB-4, WEB-7_
- **IC-2**: No — the benchmark's English-language US/Australian content does not align culturally or linguistically with bilingual Mexican/Central American crisis journalism [Q123, Q126]. — _Sources: Q123, Q126_
- **IC-3**: Yes — input content is filtered through English-language keyword lists [Q126, Q127] and US/Australian location lists [Q30] that would not transfer to Spanish-language Mexican crisis tweets. The OpenStreetMap-based location augmentation [Q36] requires Spanish-language gazetteer adaptation not provided. — _Sources: Q30, Q36, Q126, Q127_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no Spanish-speaking annotators or regional reviewers were involved in content selection [Q52, Q61]. Recruitment of Mexican/Central American journalists or linguists would be required to identify culturally sensitive instances. — _Sources: Q52_
- **IC-5**: Content validity is severely compromised: the benchmark contains zero Spanish-language content, zero Mexican/Central American geographic anchors, and uses an English-only NER + OSM pipeline that the authors explicitly note is not portable [Q119]. — _Sources: Q119, Q132, WEB-3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q30] 'The location filtering relies on a list of location candidates created by gathering cities, towns, and famous neighborhoods in a big area of interest.' (p.3)
- [Q35] 'we further developed a BERT-based NER model tuned on Twitter data to detect location mentions.' (p.4)
- [Q36] 'We use OpenStreetMap API to map location mentions to physical addresses.' (p.4)
- [Q119] 'replicating the same process for other language or based on other locations may be hard because of such dependencies.' (p.10)
- [Q123] 'We collect CrisisLTLSum across seven states in the USA and two states of Australia during 2020 and 2021.' (p.12)
- [Q126] 'We carefully curate a keyword list for each of our categories of interest by employing expert knowledge gathered through over-viewing crisis stories in news, social media, and related big disaster events of the past.' (p.13)
- [Q132] 'This approach will not be comprehensive or exhaustive but rather representative of each crisis domain.' (p.13)

*Web sources:*
- [WEB-3] HumAID is English-only despite including a 2017 Mexico earthquake subset — confirming the gap in Spanish-language Mexican crisis tweet content
- [WEB-4] Curiel et al. (PMC 2019) is the only known Mexican-Spanish crisis NER/geolocation resource and is not a timeline/summarization dataset
- [WEB-7] SASMEX hashtag conventions (#TenemosSismo, #AlertaSismica) are the standard CDMX seed-tweet vocabulary absent from benchmark
- [WEB-8] @SASMEX X account provides structured earthquake seed tweets with no analog in benchmark content

</details>

**Information gaps:**
- Frequency of indigenous-language place names in crisis tweets unknown
- Voseo penetration in Central American crisis tweets unquantified

**Requires expert verification:**
- Mexican/Central American journalist review of which colonia/municipio/landmark references are most frequent in crisis tweet streams
- Linguist review of code-switching patterns at US-Mexico border

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
The modality match is good: both the benchmark and target deployment operate on text-only tweets [Q2, Q18], and the elicitation explicitly marks this dimension as LOWER priority because no modality mismatch exists. However, the linguistic form of inputs is exclusively English [Q35, Q86], with preprocessing (lemmatization, lowercasing, fuzzy duplicate matching) implemented for English [Q129, Q136], and a 512-token BERT ceiling [Q92]. For a Spanish-language deployment, tokenization, lemmatization, and morphological handling must accommodate Spanish diacritics, accented-character variants, and informal diacritic-dropping in tweets — none of which is documented as supported. The 512-token sequence ceiling and tweet-text format are technically appropriate for the target. Per the elicitation, the linguistic-form mismatch is captured under IC and OF rather than IF; the modality dimension itself is well-aligned.

**Strengths:**
- Text-only tweet modality matches the target deployment exactly [Q2, Q18, elicitation IF-priority=LOWER].
- Standard tweet preprocessing pipeline (lemmatization, deduplication) [Q129, Q136] is methodologically applicable, even if its specific implementation is English-only.
- BERT-style 512-token sequence handling [Q86, Q92] is compatible with multilingual transformer backbones used for Spanish.

**Checklist:**

- **IF-1**: Signal distribution match is acceptable at the modality level (text tweets) [Q2, Q18]. Within-modality differences (English vs. Spanish character set, diacritic handling, tweet-register orthography) require Spanish-specific preprocessing not documented in the benchmark [Q129]. — _Sources: Q2, Q18, Q129_
- **IF-2**: Yes — Mexican mobile/Twitter infrastructure supports the same text-tweet capture format. Mexico has ~152M mobile connections (1.2 phones/person) [WEB-14], indicating high source-tweet generation capacity. Central America country-level data was not retrieved [WEB-15]. — _Sources: WEB-14_
- **IF-3**: Domain-specific differences include: SASMEX-formatted seed tweets have a structured machine-readable form [WEB-7, WEB-8] that the benchmark's pipeline does not specifically handle; Spanish accented-character handling is required but undocumented; tweet-register diacritic-dropping is a known phenomenon requiring graceful handling. — _Sources: WEB-7, WEB-8_
- **IF-4**: Form mismatches at the modality level are minor. The substantive linguistic-form mismatches (English-only preprocessing, English NER) materially affect IC and OF rather than IF per the elicitation framing. — _Sources: Q86, Q92_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'we built CrisisLTLSum using a semi-automated cluster-then-refine approach to collect data from the public Twitter stream.' (p.1)
- [Q18] 'CrisisLTLSum is developed through a two-step semi-automated process to create 1,000 local crisis timelines from the public Twitter stream.' (p.2)
- [Q86] 'we fine-tune BERT (Devlin et al., 2019) on the tweet sequences where every training example would have the form of "t0 [SEP] si"' (p.7)
- [Q92] 'the BERT-based sequence classification model has a limitation when extracting long timelines due to its limited size of 512 positional embeddings' (p.7)
- [Q129] 'we maintain both a lower-cased and a lemittized version of the keywords and the tweet's text.' (p.13)

*Web sources:*
- [WEB-14] Mexico mobile-phone penetration ~1.2 phones/person supports tweet-stream input form expectations
- [WEB-7] SASMEX standardized seed-tweet format introduces a structured input subtype absent from benchmark

</details>

**Information gaps:**
- Country-specific Central America mobile/internet penetration figures not retrieved
- Spanish tweet diacritic-dropping rates in crisis contexts not quantified

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The output ontology consists of (a) a binary timeline-membership label governed by three conditions — relevant, informative, non-repetitive [Q58] — and (b) a four-axis summary quality rubric (Coherence, Accuracy, Coverage, Overall Quality) rated 1–5 [Q106, Q151]. The three relevance conditions are conceptually generalizable, but were validated only on US English tweets by Anglophone annotators [Q61], and cross-lingual transfer validity to Mexican Spanish tweets covering different event types is unestablished. Critically, the Coherence rubric is explicitly anchored to English: 'A summary is coherent if when read by itself, it's easy to understand and free of English errors' [Q153, Q154]. This makes the coherence axis structurally invalid for Spanish-language output. Additionally, the informativeness criterion encodes US-centric judgments about what constitutes a meaningful crisis update; the Mexican context includes documented genres (community solidarity posts, citizen verification posts like #Verificado19S) that have distinct informativeness profiles [WEB-23, WEB-24]. No category captures editorial dimensions (source attribution to CENAPRED/SSN/SASMEX, casualty framing, AP Español alignment) that are central to the target deployment.

**Strengths:**
- The three-criterion relevance/informativeness/non-redundancy schema [Q58] is conceptually portable and provides a transferable starting point for Spanish-language label adaptation.
- The four-axis summary rubric (Coherence, Accuracy, Coverage, Overall) [Q106] decomposes summary quality in a way that supports targeted adaptation — Accuracy and Coverage axes [Q155, Q157] are linguistically more neutral than Coherence.

**Checklist:**

- **OO-1**: The binary timeline-membership label and four-axis quality rubric are partially relevant, but the Coherence axis is explicitly English-anchored [Q153] and the relevance/informativeness conditions [Q58] were validated only on US tweets. — _Sources: Q58, Q106, Q153_
- **OO-2**: Missing categories include: source-attribution quality (whether CENAPRED/SSN/CNPC are cited correctly), AP Español register conformance, verification-tweet detection (a specific genre in #19S contexts) [WEB-23], and seismic/volcanic alert-vocabulary correctness (semáforo phases, SASMEX hashtag usage) [WEB-7, WEB-20]. — _Sources: WEB-23, WEB-7, WEB-20_
- **OO-3**: The Coherence axis encodes 'free of English errors' [Q153] as the criterion, which directly encodes Anglophone language norms. The informativeness criterion [Q58] implicitly encodes US news-reading conventions about what counts as a 'fact' versus 'personal point of view,' and was validated only by Anglophone annotators [Q61]. — _Sources: Q58, Q153, Q154_
- **OO-4**: Significant misalignment exists. Stakeholder-driven taxonomy redesign is warranted: a Spanish-language coherence rubric, a register/style axis aligned with AP Español, and addition of source-attribution and verification-correctness axes are needed. — _Sources: Q151, Q153_
- **OO-5**: Structural validity is compromised by the English-anchored coherence rubric; content validity is compromised by missing axes for register, attribution, and verification quality. External validity transfer is therefore not supported. — _Sources: Q153, Q155, Q157_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q58] 'A tweet is labeled as part of the timeline only if it satisfies all the following three conditions: relevant: talks about the same event indicated in the seed tweet, informative: provides facts about the event but not only contains personal points of view, not repetitive: brings in new information.' (p.5)
- [Q106] 'Each summary was evaluated by five different workers on a scale from 1 to 5 across four axes: Coherence, Accuracy, Coverage, and Overall quality' (p.8)
- [Q151] 'You will rate the quality of each of the eight summaries by four axes: coherence, accuracy, coverage, and overall quality.' (p.21)
- [Q153] 'A summary is coherent if when read by itself, it's easy to understand and free of English errors.' (p.21)
- [Q155] 'Does the factual information in the summary accurately match the information in the timeline?' (p.21)
- [Q157] 'How well does the summary cover the important information in the timeline?' (p.21)

*Web sources:*
- [WEB-23] Flores-Saviaga & Savage document #Verificado19S verification-tweet genre that has no analog in the benchmark's informativeness ontology
- [WEB-7] SASMEX vocabulary defines a specific seed-tweet/follow-up structure not addressed by benchmark output categories
- [WEB-20] CENAPRED semáforo phase vocabulary is essential output-ontology content for volcanic crises

</details>

**Information gaps:**
- AP Español operationalizable criteria not openly accessible — flagged for expert elicitation
- Whether Mexican journalists' relevance judgments diverge systematically from the benchmark's three-criterion definition is empirically unverified

**Requires expert verification:**
- Mexican journalist review of relevance/informativeness boundaries on Spanish crisis tweets
- AP Español editor input on register and source-attribution rubric

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Ground-truth labels were determined by majority vote among three MTurk workers [Q70] recruited under QC1, which restricted workers to 'countries where native English speakers are most likely to be found' [Q61, Q105]. Reference summaries were written by the two workers who agreed most on extraction labels [Q87, Q88]. While inter-annotator agreement was high (90.06% [Q77], 91.77% against experts [Q78, Q79]), no Spanish-speaking annotators, no journalists, and no individuals with Latin American crisis knowledge contributed to ground truth. The elicitation explicitly confirms that journalistic relevance judgments, attribution norms, and summary scope differ from US conventions (Q3/A3). Therefore the labels and reference summaries cannot be assumed to reflect Mexican/Central American journalistic stakeholder perspectives. The aggregation method (majority vote on binary labels [Q70]; selecting the two most-agreeing workers' summaries [Q87, Q88]) further erases minority perspectives — a particular concern when no annotator represents the target population at all. Documented Mexican-context phenomena like #Verificado19S verification posts and community solidarity posts [WEB-23] would likely be judged differently by Mexican journalists than by Anglophone MTurk workers.

**Strengths:**
- Documentation of annotator quality control (QC1–QC4) is detailed [Q60–Q66], providing transparency about who did label and enabling targeted re-annotation planning.
- High inter-annotator agreement (90.06% [Q77]) and expert validation (91.77% [Q79]) demonstrate internal consistency of labels within the Anglophone population.
- Compensation transparency ($3/HIT, >$10/hour effective rate) [Q67, Q68] is documented.

**Checklist:**

- **OC-1**: No — ground-truth labels reflect Anglophone MTurk worker judgments [Q61, Q70], not Mexican/Central American journalist perspectives. The elicitation (A3) confirms divergent relevance and attribution norms. — _Sources: Q61, Q70_
- **OC-2**: Substantial disagreement is likely. Mexican journalists operating under AP Español norms apply distinct attribution standards (CENAPRED/SSN/CNPC) [WEB-1, WEB-12] and may judge community solidarity posts and verification posts [WEB-23] as more informative than US MTurk workers would. — _Sources: WEB-1, WEB-12, WEB-23_
- **OC-3**: Annotator demographics are documented only at the level of 'countries where native English speakers are most likely to be found' [Q61, Q105]. No information on age, gender, occupation, or journalistic background is provided. No Datasheet or Data Statement is referenced. — _Sources: Q61, Q105_
- **OC-4**: Re-annotation by a representative pool — Spanish-speaking journalists familiar with Mexican/Central American crisis contexts — is required for validity in the target deployment [elicitation A3]. — _Sources: Q61_
- **OC-5**: Aggregation by majority vote on binary labels [Q70] and selection of the two most-agreeing workers' summaries [Q87, Q88] erases minority perspectives. When the entire annotator pool is non-representative of the target population, this aggregation compounds rather than mitigates the validity gap. — _Sources: Q70, Q87, Q88_
- **OC-6**: Convergent validity with regional stakeholders is unsupported; external validity to Mexican journalist judgments cannot be assumed. — _Sources: Q61, Q70, WEB-23_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q61] 'we use location restriction (QC1) to limit the pool of workers to countries where native English speakers are most likely to be found.' (p.5)
- [Q70] 'To make the ground-truth on whether each tweet is part of the timeline or not, we take the majority label among the three workers.' (p.6)
- [Q77] 'The average timeline-level agreement between those two workers is 90.06%.' (p.6)
- [Q79] 'The average timeline-level agreement rate of this analysis is 91.77%.' (p.6)
- [Q87] 'Since each timeline in our dataset is annotated by three workers (§3.2), it includes three summaries.' (p.7)
- [Q88] 'we pick the two summaries written by the two workers who agree the most based on the timeline extraction labels they assign to the tweets in each timeline.' (p.7)
- [Q105] 'we recruit a group of workers from MTurk with the same Location restriction (QC1)' (p.8)

*Web sources:*
- [WEB-1] CENAPRED is the authoritative Mexican source for crisis attribution — distinct from US norms
- [WEB-12] Central American national civil-protection agencies (CONRED, COPECO, DGPC, SINAPRED, CNE, SINAPROC) define the local source-attribution ecosystem
- [WEB-23] #Verificado19S citizen-verification genre would be judged differently by Mexican journalists than US MTurk workers

</details>

**Information gaps:**
- Specific MTurk worker demographics beyond country of residence are undocumented
- The magnitude of disagreement between Anglophone MTurk workers and Mexican journalists is empirically unmeasured

**Requires expert verification:**
- Pilot re-annotation study with Mexican journalists to quantify disagreement rates on representative Spanish-language crisis tweets
- AP Español editor review of summary references for register and attribution conformance

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark evaluates only English-language output: timeline-extraction accuracy is measured against expert annotations on English tweets [Q91, Q94, Q96]; timeline summaries are evaluated using SacreROUGE [Q98, Q100] against English-language reference summaries written by Anglophone MTurk workers [Q99]; the human-evaluation rubric is written in English and scores coherence against English-language writing norms [Q106, Q153]. The target deployment requires bilingual output (Mexican Spanish + American English) with the elicitation specifying that English summaries should be more directly publication-ready and Spanish summaries adapted by journalists (A4). The benchmark provides no Spanish-language reference summaries, no Spanish coherence rubric, no bilingual evaluation protocol, no AP Español alignment metric, and no register-appropriateness scoring. The web research further documents that ROUGE correlates poorly with human judgments for Spanish summarization, with BERTScore-precision (multilingual) and LLM-as-judge being current best practice [WEB-17, WEB-18] — none of which the benchmark uses. The mismatch with the deployment's bilingual output requirement is total for Spanish.

**Strengths:**
- The English-language output evaluation [Q98, Q106] is methodologically sound and directly applicable to the deployment's English-output evaluation needs, where English summaries are expected to be higher-quality and more publication-ready (elicitation A4).
- Multi-reference ROUGE [Q99, Q100] and the four-axis human evaluation [Q106] together provide a defensible English evaluation framework that can be reused for the English half of bilingual output.

**Checklist:**

- **OF-1**: Partial match — output modality (free-form text summary) matches deployment requirements, but the language coverage (English-only) misses 50% of the bilingual requirement [Q99, Q106; elicitation A4]. — _Sources: Q99, Q106_
- **OF-2**: Not applicable — deployment does not require text-to-speech output (journalists work with text artifacts).
- **OF-3**: Not applicable — target users are professional journalists with high literacy; no accessibility constraints alter the form requirement.
- **OF-4**: Form mismatch: complete absence of Spanish-language summarization evaluation [Q99, Q106, Q153] directly contradicts the bilingual deployment requirement, severely harming external validity for the Spanish output channel. — _Sources: Q98, Q100, Q153, WEB-17, WEB-18_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q91] 'For evaluation, we use the average timeline-level accuracy.' (p.7)
- [Q96] 'The best timeline extraction model achieves 73.51 average timeline accuracy, whereas the human-level performance is 88.98.' (p.8)
- [Q98] 'We evaluate all timeline summarization models with ROUGE (Lin and Och, 2004).' (p.8)
- [Q99] 'The summarization output of each model is evaluated in a multi-reference setting against the two summaries written by the two workers who agree the most' (p.8)
- [Q100] 'We use SacreROUGE (Deutsch and Roth, 2020) to compute multi-reference ROUGE scores.' (p.8)
- [Q106] 'Each summary was evaluated by five different workers on a scale from 1 to 5 across four axes: Coherence, Accuracy, Coverage, and Overall quality' (p.8)
- [Q153] 'A summary is coherent if when read by itself, it's easy to understand and free of English errors.' (p.21)

*Web sources:*
- [WEB-17] Standard ROUGE variants correlate weakly with human judgments for Spanish summarization; BERTScore-precision with multilingual models is recommended
- [WEB-18] LLM-as-judge approaches show strong correlation with human judgments in multilingual summarization evaluation

</details>

**Information gaps:**
- Operationalizable AP Español rubric criteria not openly accessible
- No Spanish crisis-summarization reference dataset exists to enable bilingual evaluation construction

**Requires expert verification:**
- AP Español editor input to construct a Spanish coherence/register rubric
- Mexican journalist evaluation panel to validate any Spanish-language summarization quality framework

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Earthquake, volcanic activity, tropical-system flooding, civil unrest, and CDMX transportation infrastructure failures are absent from the four-domain taxonomy [Q122]

**Recommendation:** Extend the ontology with these crisis types and curate Spanish-language seed-tweet/keyword lists for each, including SASMEX (#TenemosSismo, #AlertaSismica) [WEB-7] and CENAPRED semáforo vocabulary [WEB-20]. Recognize persistent (e.g., volcanic) vs. spike-event temporal profiles [WEB-26] in the 'local' definition [Q12].

### Input Ontology ⚠

**Gap:** The 'local' scope definition (building/street/county, short period) [Q12] excludes persistent volcanic activity and multi-day tropical systems

**Recommendation:** Generalize the temporal-scope definition to support persistent and multi-phase events, with explicit handling of semáforo phase transitions and tropical-system alert lifecycles.

### Input Content ⚠

**Gap:** Zero Spanish-language Mexican/Central American content; English NER + English-OSM pipeline is non-portable [Q35, Q36, Q119]

**Recommendation:** Build or commission a Spanish-language crisis tweet corpus anchored to Mexican (CDMX alcaldías, key estados) and Central American (departamentos/municipios) events. Adapt the Curiel et al. (PMC 2019) Mexican-Spanish NER pipeline [WEB-4] for georesolution, and integrate a Spanish-language gazetteer that includes colonias, alcaldías, and indigenous-language place names.

### Output Content ⚠

**Gap:** Reference labels and summaries authored entirely by Anglophone MTurk workers under QC1 location restriction [Q61]; no journalist or Mexican stakeholder representation

**Recommendation:** Re-annotate a representative subset using Mexican Spanish-speaking journalists familiar with Mexican/Central American crisis contexts and AP Español. Quantify disagreement against the original labels and report convergent-validity statistics. Avoid majority-vote aggregation that erases minority perspectives when annotator pools are small.

### Output Form ⚠

**Gap:** No Spanish-language summarization evaluation; English-only ROUGE [Q99, Q100] and English coherence rubric [Q153]

**Recommendation:** Implement a bilingual evaluation protocol: BERTScore with multilingual backbone (XLM-R or mBERT) and LLM-as-judge for Spanish summaries [WEB-17, WEB-18], alongside human evaluation by Spanish-speaking journalists. Maintain the existing English ROUGE pipeline for the English output channel where it remains defensible.

### Output Ontology

**Gap:** Coherence rubric is explicitly anchored to English [Q153]; missing axes for source attribution, AP Español register, and verification-tweet detection

**Recommendation:** Construct a Spanish coherence rubric referencing Spanish-language writing norms; add an AP Español–aligned register axis (requires expert elicitation from AP Español editors) and a source-attribution axis covering CENAPRED/SSN/CNPC/SASMEX [WEB-1, WEB-7]; add a verification-quality axis informed by the #Verificado19S model [WEB-23].

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
| Q9 | 1 | output_content | "Hossein Rajaby Faghihi, Bashar Alhafni, Ke Zhang, Shihao Ran, Joel Tetreault, Alejandro Jaimes" |
| Q10 | 1 | output_content | "Michigan State University, New York University Abu Dhabi, Dataminr, Inc." |
| Q11 | 2 | input_ontology | "To the best of our knowledge, this is the first annotated dataset for such an extraction task, while this problem has been tackled before in unsupervised settings (Zhang et al., 2018)." |
| Q12 | 2 | input_ontology | "Moreover, we focus on the extraction of local crisis events. The term "local" indicates that an event is bound to an exact location, such as a building, a street, or a county, and usually lasts for a short period." |
| Q13 | 2 | input_content | "Building a corpus of local crisis events is particularly useful for first responders but also challenging because the timelines of these events are often not captured in existing knowledge sources." |
| Q14 | 2 | input_ontology | "This means one has to design mechanisms for automatically detecting and tracking events directly from the Twitter stream, which is especially hard for existing clustering methods (Guille and Favre, 2015; Asgari-Chenaghlu et al., 2021) given the low number of available tweets for each local event." |
| Q15 | 2 | input_content | "First, the process of identifying and extracting relevant updates for a specific event has to contend with the large volume of noise (Alam et al., 2021a) and informal tone (Rudra et al., 2018) compared to other domains such as news." |
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
| Q30 | 3 | input_content | "The location filtering relies on a list of location candidates created by gathering cities, towns, and famous neighborhoods in a big area of interest. A tweet is considered relevant to our area of interest if 1) the text mentions one of the candidates, 2) the geo-tag matches the area of interest, or 3) the user location matches the area of interest." |
| Q31 | 3 | input_content | "To limit the tweets to a specified crisis domain, we curate domain-specific keywords and only select tweets with phrases matching one of the keywords. This approach is not comprehensive or exhaustive but somewhat representative of each crisis domain." |
| Q32 | 3 | input_content | "The combinations of (area a, domain d, time t) are manually selected so that the events of type d at location a are more frequent during time period t." |
| Q33 | 3 | input_form | "We use three different modules. First, we use a pre-trained neural model from AllenNLP (Gardner et al., 2018), trained on CoNLL03 (Tjong Kim Sang and De Meulder, 2003), to extract entities with types of people, location, and organization." |
| Q34 | 3 | input_content | "Although this module extracts some important entities in the text, it fails to extract uncommon entities or special mentions" |
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
| Q50 | 4 | input_content | "First, we manually merge pairs of clusters with a cluster head similarity higher than a threshold headmin." |
| Q51 | 4 | input_content | "This step compensates for some of the errors from missing entities in the pre-processing step, which affects the intermediate similarity scores in the clustering algorithm." |
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
| Q75 | 6 | output_content | "We notice an interesting trend across the domains: the longer the timeline, the lower the average percentage of tweets to be part of the timeline." |
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
| Q102 | 8 | input_form | "In the oracle setting, we use the gold labels in the DEV set to identify tweets that are part of each timeline to the summarization models." |
| Q103 | 8 | output_form | "We further conducted a human evaluation to better assess the quality of the summaries." |
| Q104 | 8 | output_form | "We take the whole TEST set and we evaluate eight summaries per timeline: 1) the three human-written summaries; 2) three model-generated summaries using the three models we develop for timeline summarization in the oracle setting; 3) two summaries from random systems: a random tweet that is part of the timeline, and a summary from a randomly selected timeline that belongs to a different crisis domain." |
| Q105 | 8 | output_content | "Following a similar process in 3.2, we recruit a group of workers from MTurk with the same Location restriction (QC1), who can pass our pilot study as a qualification test." |
| Q106 | 8 | output_form | "Each summary was evaluated by five different workers on a scale from 1 to 5 across four axes: Coherence, Accuracy, Coverage, and Overall quality, as was done by Lai et al. (2022)." |
| Q107 | 8 | output_content | "Detailed instructions and annotation workflows are presented as Figures 15–21 in Appendix E." |
| Q108 | 8 | output_form | "Looking at the results over all the timelines, the human-written summaries are significantly better than the ones generated by models, in terms of overall quality with an average rating of 4.12." |
| Q109 | 9 | input_content | "We presented CrisisLTLSum, the first dataset on local crisis timelines extracted from Twitter and the first to provide human-written summaries on information extracted from Twitter." |
| Q110 | 9 | input_ontology | "We showed that CrisisLTLSum supports two downstream tasks: Timeline Extraction and Timeline Summarization." |
| Q111 | 9 | output_form | "Our experiments with SOTA baselines indicate that both of these tasks are challenging and encourage future research." |
| Q112 | 9 | input_ontology | "Our dataset further provides a resource for developing methods on utilizing microblogs toward aiding first-responders in evaluating ongoing crisis events." |
| Q113 | 9 | output_content | "For timeline extraction, 66 timelines (77%) have at least one error, in which 272 out of 958 tweets (28%) are wrong." |
| Q114 | 9 | output_form | "We observe that the model performance decreases with increasing timeline length for both timeline extraction and summarization tasks, with significant drops in accuracy and ROUGE scores when timelines get longer." |
| Q115 | 9 | output_form | "Most of the summarization errors were due to hallucinations or to copying specific sentences that are present in the timeline without covering all the important event details described in the timeline." |
| Q116 | 10 | output_content | "We thank Aoife Cahill for providing detailed feedback on this paper, Alison Smith-Renner and Wenjuan Zhang for helpful discussions on MTurk annotations, our colleagues at Dataminr, and the EMNLP reviewers for their helpful and constructive comments." |
| Q117 | 10 | input_content | "This study has some limitations on the dataset generation workflow. First, our noisy timeline collection process is not a comprehensive and exhaustive extraction to find all available information about a local crisis event. Here, our focus is to provide a representative dataset rather performing a comprehensive set containing all the local crisis events and their updates." |
| Q118 | 10 | input_content | "Second, the proposed noisy timeline collection pipeline is highly dependent to the performance of the entity extraction modules, especially for the location extraction, and the accuracy of the OpenStreetMap API to find the correct physical address of each location mention." |
| Q119 | 10 | input_content | "Accordingly, replicating the same process for other language or based on other locations may be hard because of such dependencies." |
| Q120 | 10 | output_form | "Furthermore, the online clustering method used in this paper has a set of hyperparameters which are tuned heuristically from a small set of experiments. More comprehensive and large scale experiments on tuning those parameters could potentially impact the quality of the generated timelines." |
| Q121 | 10 | input_content | "Generating similar results by following our noisy timeline collection process is in general limited by the users' access to the public Twitter stream and the changes in the available posts (they may become restricted or deleted)." |
| Q122 | 12 | input_ontology | "We build CrisisLTLSum by limiting the search to four crisis domains: wildfire, local fire, traffic, and storm." |
| Q123 | 12 | input_content | "We collect CrisisLTLSum across seven states in the USA and two states of Australia during 2020 and 2021. The selected states in the USA are New York, Illinois, Massachusetts, California, Texas, and Florida. From Australia, we have selected the states of New South Wales and Victoria." |
| Q124 | 13 | input_content | "These states are selected as they are some of the areas subject to the most events falling into our crisis domains of interest. California, Victoria, and New South Wales are mainly selected due to the abundance of wildfires in hot seasons. Texas and Florida have been selected as they are both subject to wildfires and storm events during different months. Massachusetts and Illinois are selected first because those areas are frequently subjected to bad weather, and second as they contain big cities subject to traffic and local fire events alongside New York." |
| Q125 | 13 | input_form | "This step selects the subset of filtered tweets related to a specific crisis category of interest. Ideally, this task can be performed by a neural model trained on a large set of tweets with labeled data indicating the categories. However, as such a large amount of labeled data is unavailable, we rely on a common approach of designing keywords." |
| Q126 | 13 | input_content | "We carefully curate a keyword list for each of our categories of interest by employing expert knowledge gathered through over-viewing crisis stories in news, social media, and related big disaster events of the past." |
| Q127 | 13 | input_content | "Please note that these lists are generic for each category and not specific to unique events. For instance, instead of defining keywords specific to an event called "Hurricane Ida", our keywords list includes phrases such as "fallen tree", "building collapse", or "storm"." |
| Q128 | 13 | input_content | "The quality of the keywords list is crucial to the final quality of the generated timelines, and we polish this list multiple times based on small sets of experiments before using them for the final task." |
| Q129 | 13 | input_form | "To avoid making a long list of keywords and ensure that different lexical formats of the same word are still considered in the keyword matching process, we maintain both a lower-cased and a lemittized version of the keywords and the tweet's text." |
| Q130 | 13 | input_form | "If any of the keywords exist in the text and in any of these formats, then the tweet is considered related to the category." |
| Q131 | 13 | input_form | "The multi-word keywords are not considered n-grams but as an indication that all the words in the keyword should exist in the text, even if not as a sequence." |
| Q132 | 13 | input_content | "This approach will not be comprehensive or exhaustive but rather representative of each crisis domain. Improving this method to be more encompassing is an area for future research." |
| Q133 | 13 | input_form | "We use the following parameters shared among all different domains: shashtag is set to 0.2 and sdist is 0.3. The simthreshold and timethreshold are set to 0.7 and 15 hours respectively. The timethreshold is reduced to 3 hours to avoid merging various accidents at different times but in the same location. The mindist and maxdist are set to 0.4 kilometer and 4 kilometer for fire and traffic events while having the larger range of 0.4 and 10 kilometers for the wildfire and storm extraction. The expirationthreshold is set to 15 hours and tweetthreshold is 4." |
| Q134 | 13 | input_content | "The online clustering approach may fail to properly relate some tweets due to missing entities, clustering method hyper-parameters, or the difference in the description of various angles of the same story." |
| Q135 | 13 | output_content | "To address this, we merge clusters by comparing all cluster heads with each other and combining those with a higher similarity score than a threshold shead. Additionally, we use human feedback to merge clusters where their similarity score is below shead but higher than a second hyper parameter s min head." |
| Q136 | 13 | input_form | "Here, the goal is to remove tweets from the same cluster with identical or similar text. The duplicate removal relies on a fuzzy string sequence-matching technique to compute the similarity between a pair of tweets. We simply go over each tweet sorted in chronological order and remove the ones that match any of the previous tweets in the same cluster with a matching score higher than dmatch." |
| Q137 | 13 | input_content | "Although the keyword filtering step would reduce the number of tweets unrelated to the category of interest, this step aims to further remove the unrelated clusters generated from the pipeline." |
| Q138 | 14 | input_content | "Our goal is to select 1000 clusters that contain enough tweets describing an evolving crisis event." |
| Q139 | 14 | input_content | "In particular, we first identify a "seed tweet" as the first observed post mentioning a local crisis event, then roughly check whether the following tweets in the cluster contain updates about the same event." |
| Q140 | 14 | input_ontology | "We select clusters across four crisis domains, including wildfire, fire, storm, and traffic, depending on how frequently each type of event happens in extracted noisy clusters." |
| Q141 | 14 | output_form | "We fine-tune BERT base uncased on a single GPU for 10 epochs with a learning rate of 5e-5, batch size of 32, a seed of 42, and a maximum sequence length of 512." |
| Q142 | 14 | output_form | "The GRU has one layer with a hidden size of 128. The model was trained for 50 epochs with early stopping after five epochs if the performance did not improve on the DEV set. We use a learning rate of 5e-5, a batch size of 16, and a seed of 42." |
| Q143 | 14 | output_form | "We fine-tune BART based on a single GPU for ten epochs with a learning rate of 5e-5, batch size of 16, a seed of 42, and a maximum target sequence length of 512." |
| Q144 | 14 | output_form | "During inference, we use beam search with a beam size of 4." |
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
| WEB-1 | https://en.wikipedia.org/wiki/CENAPRED |
| WEB-2 | https://mx.usembassy.gov/natural-disaster-alert-u-s-embassy-mexico-city/ |
| WEB-3 | https://crisisnlp.qcri.org/humaid_dataset.html |
| WEB-4 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6484392/ |
| WEB-5 | https://www.gob.mx/cenapred |
| WEB-6 | https://github.com/wangcongcong123/crisis_nlp_progress/blob/master/datasets/TREC-IS.md |
| WEB-7 | https://en.wikipedia.org/wiki/Mexican_Seismic_Alert_System |
| WEB-8 | https://x.com/sasmex |
| WEB-9 | https://medium.com/hci-wvu/countering-fake-news-in-natural-disasters-using-bots-and-citizen-crowds-412bbef6b489 |
| WEB-10 | https://x.com/cnpc_mx |
| WEB-11 | https://es.wikipedia.org/wiki/Centro_Nacional_de_Prevenci%C3%B3n_de_Desastres |
| WEB-12 | https://whndn.org/portfolio-item/disaster-response-services-tools/ |
| WEB-13 | http://data.proteccioncivil.cdmx.gob.mx/Monitoreo-popo.html |
| WEB-14 | https://www.worlddata.info/america/mexico/telecommunication.php |
| WEB-15 | https://datahub.itu.int/data/?e=1&i=11624 |
| WEB-16 | https://psmag.com/social-justice/how-mexico-city-residents-used-social-media-to-debunk-fact-from-fiction/ |
| WEB-17 | https://arxiv.org/pdf/2503.17039 |
| WEB-18 | https://aclanthology.org/2024.emnlp-main.1085.pdf |
| WEB-19 | https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2022.827236/full |
| WEB-20 | https://www.cenapred.unam.mx/reportesVolcanesMX/ |
| WEB-21 | https://www.milenio.com/estados/que-es-el-semaforo-de-alerta-volcanica-y-como-funciona |
| WEB-22 | https://cnnespanol.cnn.com/2024/03/15/volcan-popocatepetl-alerta-amarilla-riesgos-orix |
| WEB-23 | https://arxiv.org/abs/2007.05848 |
| WEB-24 | https://link.springer.com/article/10.1007/s00779-020-01411-5 |
| WEB-25 | https://mimran.me/papers/HumAID_Human_Annotated_Disaster_Incidents_Data_from_Twitter_ICWSM21.pdf |
| WEB-26 | https://www.infobae.com/mexico/2026/04/29/popocatepetl-tuvo-167-emisiones-este-28-de-abril/ |

---

