## Deployment Context

**Use case:** Use case: Reliability of disaster reporting in news at national/local level, finding alignment with effective and verified information (e.g. noisy vs real signals). The evaluation data could report or not disaster damage.
**Target population:** Policy makers and government agencies in Argentina studying trustiness and reliability of disaster communication across different channels are (e.g news, social media post, press). They would be based in Buenos Aires, speakers of Rioplatense Spanish, with an intermediate to advanced level of English, at least a master's degree, and be part of an upper-middle-class household.

# Validity Analysis: crisisbench
**Target context:** Argentina — Buenos Aires Policy Maker Cohort (Disaster Reporting Reliability)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology | 3 | Moderate gaps | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 3 | Moderate gaps | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 3 | Moderate gaps | high |
| **Average** | **2.3** | | |

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

CrisisBench provides a methodologically rigorous, reproducible foundation for crisis-tweet classification with a clean two-task ontology (binary informativeness + multi-class humanitarian type) that aligns at the top level with international ISCRAM/OCHA-derived frameworks Argentine emergency professionals reference. However, three structural misalignments substantially limit its validity for the Buenos Aires policy-maker deployment: (1) Input Content (HIGH priority) is severely misaligned — 94.46% English [Q46], zero Argentine or Rioplatense Spanish content, and a 2010–2017 temporal window that predates the dissolution of Télam (July 2024) and creation of AFE (2025); the only Spanish content in the benchmark is Chilean and Venezuelan, not Rioplatense [DATASET-D2, D3, D6, D7]. (2) Output Ontology (HIGH priority) lacks the source credibility / signal-reliability dimension that is the deployment's core requirement; the user acknowledges this as a downstream construction step but the benchmark provides no learnable credibility signal. (3) Output Content shows annotator-population mismatch and empirically observable annotation noise, with evidence of systematic Spanish-language disaster-content under-recognition [DATASET-D9, D8]. Input Form, Input Ontology, and Output Form present moderate but tractable gaps. The benchmark is best treated as a usable signal-triage foundation for the user's planned downstream credibility-aggregation pipeline, not as a complete evaluation framework for the Argentine deployment.

## Practical Guidance

### What This Benchmark Measures

CrisisBench measures English-language Twitter content's informativeness (binary) and humanitarian type (multi-class) for a fixed set of 2010–2017 disaster events concentrated in North America and globally reported crises. For the Argentine deployment, it provides a usable first-pass signal-triage capability — separating clear noise from clear crisis content at high accuracy on English content (0.866/0.829 F1) — that can serve as Step 1 of the user's planned downstream credibility-scoring pipeline. The strongest dimensions for the deployment are Input Form (text-only modality match) and the foundational utility of the binary informativeness task; the top-level humanitarian categories are recognizable to Argentine policy professionals via international taxonomy alignment.

### Construct Depth

The benchmark probes informativeness and humanitarian type at moderate depth for English North American Twitter content but provides no depth on (a) source credibility, the deployment's core construct, or (b) Spanish-language or Rioplatense register. Cross-dataset F1 degradation of 14.3% [Q87] and ~8% multilingual humanitarian F1 drop [Q99] indicate that even the depth it does provide does not generalize cleanly across event contexts or languages. The dataset analysis reveals annotation noise that further limits the trustworthiness of the F1 numbers as indicators of real-world classification capability, particularly for borderline content where credibility decisions are most consequential.

### What Else You Need

The deployment requires three supplementation streams: (1) Argentine/Rioplatense Spanish disaster content for fine-tuning or evaluation — addressing the Input Content gap; possibilities include collecting and annotating Argentine Twitter/X content using the CrisisBench taxonomy, leveraging the cross-lingual approach in arXiv:2209.02139 [WEB-17], or extending TREC-IS-style protocols [WEB-15] to Argentine events. (2) A credibility-scoring extension — addressing the Output Ontology gap; TREC-IS priority labels (Low/Medium/High/Critical) [WEB-15] are the closest precedent and could anchor downstream construction combining classifier outputs with Argentine source metadata (institutional affiliation, post-Télam press source registry, Buenos Aires Province Resolución 4/2025-compliant metadata). (3) Argentine-annotator label validation on a stratified sample — addressing the Output Content gap; required to quantify expected label disagreement, particularly for Spanish-language content where dataset analysis suggests systematic under-recognition risk.

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The top-level taxonomy (informativeness binary; humanitarian multi-class with categories like affected_individual, infrastructure_and_utilities_damage, requests_or_needs, response_efforts, caution_and_advice) is broadly compatible with the international ISCRAM/OCHA-derived frameworks Argentine emergency professionals use as reference points, and elicitation Q1 confirms users find these categories 'broadly sufficient'. However, the benchmark explicitly defers event-type classification [Q22, Q23], does not include sub-labels for Argentine hazard types (pampero, sudestada, ENSO drought, AMBA urban flash flood) or informal-settlement (villa) impact framing, and the absence of a Latin American taxonomy adaptation is confirmed at the field level [WEB-15]. Some humanitarian classes have very low support (e.g., 17 'terrorism related' tweets [Q52]), and categorical granularity varies significantly across constituent datasets [Q76]. Dataset analysis confirms the schema covers the core triage categories Argentine policy makers need [DATASET-D19, D20, D35, D42] but exposes the 'other_relevant_information' class as a heterogeneous catch-all that limits its utility for borderline credibility cases.

**Strengths:**
- Top-level humanitarian categories (affected_individual, infrastructure_and_utilities_damage, requests_or_needs, response_efforts, caution_and_advice, donation_and_volunteering) align with ISCRAM-derived frameworks recognized by Argentine emergency management professionals, supporting first-pass triage utility
- Binary informativeness layer is structurally compatible with the deployment's first-pass signal-triage step and operationalizes a foundation for downstream credibility scoring

**Checklist:**

- **IO-1**: Required Argentine categories include pampero windstorm, sudestada/Río de la Plata flooding, ENSO-driven drought, urban AMBA flash flood, and villa (informal-settlement) impact framing. Top-level humanitarian categories (infrastructure damage, affected individuals, response efforts) are required and present. — _Sources: Q3, WEB-15_
- **IO-2**: Argentine hazard sub-labels and informal-settlement impact framing are omitted. No Latin American adaptation of ISCRAM/OCHA taxonomies addressing pampero, sudestada, or ENSO-drought sub-types exists in the literature [WEB-15]. Event-type classification is deferred entirely [Q22, Q23]. — _Sources: Q22, WEB-15_
- **IO-3**: Some categories have negligible support (e.g., 'terrorism related' with only 17 tweets [Q52]; 'disease related' only in CrisisNLP [Q53]). The 'other_relevant_information' class is semantically incoherent per dataset analysis (Concern 7), reducing its utility. — _Sources: Q52, Q76, DATASET-D33, DATASET-D31_
- **IO-4**: Documented gaps: (a) no event-type classification implemented; (b) no Argentine hazard sub-types; (c) no informal-settlement impact framing; (d) heterogeneous 'other_relevant_information' catch-all. These constitute construct underrepresentation for the deployment but the user has flagged them as desirable rather than blocking. — _Sources: Q22, Q89, DATASET-D33_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'Typical classification tasks in the community include (i) informativeness ... (ii) humanitarian information types ... and (iii) event types' (p.1)
- [Q22] 'We only focused on two tasks for this study and we aim to address event types task in a future study.' (p.2)
- [Q52] 'Only 17 tweets with the label "terrrorism related" are present in CrisisNLP.' (p.5)
- [Q76] 'CrisisLex and CrisisNLP ... six and eleven class labels, respectively' (p.7)
- [Q89] 'humanitarian task is a multi-class classification problem, which makes it a much more difficult task' (p.8)

*Web sources:*
- [WEB-15] TREC-IS 25-category ontology was developed with North American/European emergency practitioners and does not include Argentine hazard types

*Dataset analysis:*
- DATASET-D19: Calgary flood tweet correctly labelled affected_individual — confirms top-level category functions
- DATASET-D42: Tacloban evacuation centers tweet labelled response_efforts — clear category alignment
- DATASET-D33: Long Island home renovations advertisement placed in other_relevant_information — illustrates catch-all class incoherence
- DATASET-D31: Texas fertilizer explosion casualties labelled other_relevant_information rather than injured_or_dead_people — boundary inconsistency

</details>

**Information gaps:**
- Whether downstream sub-label extension to Argentine hazard types is feasible given absent training data

**Requires expert verification:**
- Whether Argentine emergency management professionals would prioritize villa-impact sub-labels over generic affected_individual labels in operational triage

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Input content is the highest-priority dimension (HIGH per elicitation) and exhibits the most severe alignment failure. English tweets constitute 94.46% of the informativeness set [Q46], with non-English content largely confined to CrisisLex [Q47], and all classification experiments restricted to English [Q59]. The geographic distribution is concentrated in North American and globally reported events: Joplin tornado, Hurricane Sandy [Q27, Q28], 2010/2012 events [Q29], 2017 international disasters [Q31] — with no Argentine or Latin American disaster events documented. Dataset analysis empirically confirms that across 271 sampled examples, zero contain Argentine events, Argentine institutional actors, or Rioplatense Spanish; the only Spanish-language content is Chilean and Venezuelan [DATASET-D2, D3, D4, D6, D7]. The deployment's primary channel — Argentine Twitter/X with Rioplatense voseo, lunfardo, political satire, and references to local actors (SINAGIR, AFE, Buenos Aires province) — is entirely absent from the training distribution. The 2010–2017 temporal window [Q100] predates the dissolution of Télam (July 2024) [WEB-9], creation of AFE (2025) [WEB-10], and post-Musk Twitter/X conventions, meaning the institutional credibility landscape encoded in the data does not match the current Argentine deployment context.

**Strengths:**
- Multi-event, multi-geography training distribution (20+ events spanning floods, earthquakes, hurricanes, typhoons, disease outbreaks, industrial accidents) provides exposure to diverse disaster registers, reducing categorical failure on hazard types absent from any single source [DATASET-D25, D27, D44]
- Some non-English Romance and Asian-language content (Italian, French, Portuguese, Tagalog, Spanish) is present and annotated, demonstrating the label schema has been exposed to multilingual data even though classification experiments are English-only [Q42, Q43, DATASET-D21, D39]

**Checklist:**

- **IC-1**: Yes — Argentine deployment requires Rioplatense Spanish lexical and pragmatic competence (voseo, lunfardo, political satire, local institutional actors). The benchmark contains no Argentine content [DATASET CRITICAL Concern 1]; the only Spanish content is Chilean/Venezuelan [DATASET-D2, D3, D4, D6, D7]. — _Sources: Q46, Q47, Q59, DATASET-D2, DATASET-D3, DATASET-D6_
- **IC-2**: Cultural alignment is poor for social media (the highest-priority channel per elicitation Q2). Argentine political satire of government crisis response, lunfardo register, and references to AMBA institutional actors are absent. Formal press content may align better but is also unrepresented, and the dissolution of Télam materially changes the post-2024 source landscape [WEB-8, WEB-9]. — _Sources: Q31, WEB-8, WEB-9, DATASET-D17, DATASET-D18_
- **IC-3**: Yes — the benchmark embeds North American institutional and cultural framing (US sports commentary, US political discourse, Sandy/Joplin/Maria contexts) [DATASET-D17, D18, D46]. The vernacular register learned as 'noise' is specifically North American social noise, not Argentine. — _Sources: Q27, DATASET-D17, DATASET-D18, DATASET-D46_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotators were involved in constructing CrisisBench. Recruiting Argentine annotators to flag culturally sensitive instances would require a separate validation effort.
- **IC-5**: Documented content issues: (a) zero Argentine/Rioplatense content; (b) only Chilean/Venezuelan Spanish at small scale [WEB-16, WEB-17]; (c) 2010–2017 temporal window predates current Argentine institutional landscape [Q100, WEB-9, WEB-10]; (d) North American event and institutional dominance. These violate content validity for the deployment's primary social media channel. — _Sources: Q46, Q100, WEB-9, WEB-10, WEB-16, WEB-17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q46] 'English tweets appear to be highest in the distribution ... 94.46% of 156,899' (p.5)
- [Q47] 'most of the non-English tweets appear in the CrisisLex dataset' (p.5)
- [Q27] 'Joplin collection ... Sandy collection' (p.3)
- [Q31] 'CrisisMMD ... seven disaster events that happened in 2017' (p.3)
- [Q59] 'we only use tweets in English language in our experiments' (p.6)
- [Q80] 'sub-optimal performance due to the inclusion of heterogeneous data (i.e., a variety of disaster types and occurs in a different part of the world)' (p.7)
- [Q100] 'time-span starting from 2010 to 2017' (p.9)

*Web sources:*
- [WEB-16] CrisisLex Chilean earthquake collection ~2,100 Spanish tweets, 2010, binary relatedness only — not Rioplatense and not used in CrisisBench classification experiments
- [WEB-17] Sánchez et al. 2022 cross-lingual crisis classification paper does not address Rioplatense register
- [WEB-9] Télam dissolved by Decree 548/2024 in July 2024 — material change to Argentine formal press source landscape post-benchmark
- [WEB-10] AFE created by Decree 225/2025 — new federal emergency coordinator absent from benchmark institutional context

*Dataset analysis:*
- DATASET-D2: Chilean earthquake solidarity tweet — Chilean Spanish, not Argentine/Rioplatense
- DATASET-D3: Iquique (Chile) solidarity tweet — confirms Spanish content is exclusively Chilean in sample
- DATASET-D4: Chilean political sentiment about foreign aid labelled not_informative — non-Argentine register
- DATASET-D6: Chilean earthquake tweet — Chilean, not Rioplatense
- DATASET-D7: Venezuelan refinery explosion tweet — Venezuelan Spanish
- DATASET-D17: Joplin tornado personal complaint — North American vernacular register learned as 'personal_update'
- DATASET-D18: Sandy hurricane vernacular tweet — North American slang dominates personal_update class
- DATASET-D46: US political commentary during Hurricane Maria — analogue Argentine political commentary on AFE response would face same out-of-distribution challenge

</details>

**Information gaps:**
- Whether classifiers pre-trained on this benchmark transfer at any usable F1 level to Rioplatense Spanish content
- Whether the small Chilean subset would provide any positive transfer signal for Argentine deployment

**Requires expert verification:**
- Argentine linguist/policy expert validation of which Rioplatense register features (voseo, lunfardo, political satire patterns) most threaten classification accuracy
- Operational assessment by AMBA emergency management staff of how WhatsApp and Telegram channel content (not in benchmark) interacts with the Twitter/X channel monitoring

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Input form is rated LOWER priority by elicitation, and the structural alignment is moderate. The benchmark is text-only Twitter content [Q38] matching the deployment's text-only modality, and Argentine professional cohorts have high digital infrastructure access [WEB-3, WEB-5]. Tokenization, URL/punctuation/user-id removal [Q38], and near-duplicate filtering at 0.75 cosine similarity [Q39, Q40] are reasonable preprocessing choices. However, three concerns remain: (a) the deployment spans Twitter/X, news articles, and press releases, but the benchmark is exclusively tweet-derived with no cross-channel transfer evaluation [WEB-20]; (b) language tagging is done via Google Cloud API [Q44, Q45] but lang_conf is missing for many CrisisMMD/AIDR examples (Concern 9), weakening language-stratified routing for the bilingual deployment; (c) all classification experiments are English-only [Q59] despite multilingual content being present in the consolidated data [Q42, Q43], so the form-level multilingual capability is not validated. The 70/10/20 split [Q60] and aggressive duplicate filtering [Q41, Q97] are methodological strengths.

**Strengths:**
- Text-only Twitter modality matches the deployment's text-only requirement; no signal-distribution mismatch at the modality level
- Rigorous near-duplicate filtering (0.75 cosine threshold, manually validated) reduces overestimated test results [Q39, Q40, Q97]
- Language tags assigned to all tweets via Google Cloud API enable downstream language-stratified analysis [Q44, Q45]

**Checklist:**

- **IF-1**: Twitter text signal distributions match between benchmark and Argentine Twitter/X deployment at the form level. However, Twitter/X platform conventions have evolved post-2022 (post-Musk acquisition); pre-2017 tweet structure may differ in hashtag conventions, link formats, and length. INSUFFICIENT DOCUMENTATION on whether benchmark tokenization handles current X.com URL patterns. — _Sources: Q38_
- **IF-2**: Argentine infrastructure supports text capture: 88.4% national internet penetration [WEB-3]; AMBA professional cohort has full connectivity [WEB-5]. No infrastructure obstacle. — _Sources: WEB-3, WEB-5_
- **IF-3**: Cross-channel form gap: benchmark is tweet-only [Q38]; deployment also covers news articles and press releases. No cross-channel transfer benchmark exists in the literature [WEB-20]. Tweet-length constraints and Twitter-specific preprocessing (user-id removal, URL stripping) do not natively support longer-form institutional content. — _Sources: Q38, WEB-20_
- **IF-4**: Documented form mismatches: (a) tweet-only vs. multi-channel deployment; (b) lang_conf missing for significant CrisisMMD/AIDR subset (Concern 9), reducing language-routing reliability; (c) temporal gap to current X.com platform conventions. These threaten external validity for non-Twitter deployment channels. — _Sources: Q42, Q59, DATASET-D5, DATASET-D10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q38] 'modified version of the Tweet NLP tokenizer ... lowercasing the text and removing URL, punctuation, and user id' (p.4)
- [Q39] 'cosine similarity to compute a similarity score between two tweets and flag them as duplicate if their similarity score is greater than the threshold value of 0.75' (p.4)
- [Q42] 'Some of the existing datasets contain tweets in various languages (i.e., Spanish and Italian) without explicit assignment of a language tag' (p.5)
- [Q44] 'We decided to provide a language tag for each tweet' (p.5)
- [Q45] 'language detection API of Google Cloud Services' (p.5)
- [Q59] 'we only use tweets in English language in our experiments' (p.6)
- [Q60] 'train, dev, and test sets with a proportion of 70%, 10%, and 20%' (p.6)

*Web sources:*
- [WEB-3] 88.4% Argentine national internet penetration as of January 2024
- [WEB-5] AMBA professional cohort fully connected; 71% of fixed-line subscriptions in CABA/Buenos Aires province/Córdoba/Santa Fe/Mendoza
- [WEB-20] TREC CrisisFACTS extends to multi-stream (Twitter, Reddit, Facebook, online news) but provides no tweet-to-news transfer benchmarks

*Dataset analysis:*
- DATASET-D5 (lang_conf NA): CrisisMMD examples have missing language confidence scores, weakening language-stratified routing
- DATASET-D10: AIDR-sourced example with lang_conf NA — same routing weakness in AIDR subset
- DATASET-D39: Tagalog rescue request with phone number — illustrates tweet-form constraint (~140-char/280-char) on structured contact information

</details>

**Information gaps:**
- Whether benchmark-trained classifiers transfer to news article and press release form factors with any usable F1
- Whether lang_conf NA examples disproportionately misclassify by language

**Requires expert verification:**
- Operational assessment of whether Argentine deployment teams can downstream-restrict input to tweets only or must accept news/press content

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Output ontology is HIGH priority per elicitation. The two implemented tasks — binary informativeness and multi-class humanitarian type [Q12] — provide a usable foundation but do not natively include the source credibility, misinformation likelihood, or signal-to-noise reliability dimension that is the deployment's core requirement (elicitation Q3). The user explicitly acknowledges this gap and intends to construct credibility scoring downstream by combining model outputs with external metadata, but the benchmark's data schema (id, event, source, text, lang, lang_conf, class_label) contains no tweet-level credibility metadata to learn from (CRITICAL Concern 2). Dataset analysis empirically confirms the disconnect: a 'DEATH TOLL Now under Investigation for COVER UP!!!' tweet labelled not_informative [DATASET-D45] and a Boston Bombing conspiracy tweet labelled informative [DATASET-D47] illustrate that informativeness ≠ credibility. The label space is also imbalanced even after consolidation (37.40% 'not humanitarian' [Q56]), with low-support classes [Q52, Q53, Q54] and class-mapping discrepancies that produce results reported only for classes the model can classify [Q88]. TREC-IS provides the closest precedent (Low/Medium/High/Critical priority labels) but covers no Argentine events [WEB-15].

**Strengths:**
- Carefully documented label-mapping process across 8 source datasets [Q33, Q106–Q110, Q123–Q125] enables transparent inspection of the consolidated taxonomy
- Top-level humanitarian categories are oriented toward humanitarian aid relevance and align with internationally-normed disaster taxonomies Argentine professionals reference [Q18]
- Binary informativeness layer functions as a deployable first-pass triage filter — operationalizes Step 1 of the user's downstream credibility pipeline [DATASET-D34]

**Checklist:**

- **OO-1**: Top-level humanitarian categories (affected_individual, infrastructure_damage, requests_or_needs, response_efforts, caution_and_advice, displaced_and_evacuations, donation_and_volunteering) are regionally relevant for Argentine emergency triage. The informativeness binary is also relevant. — _Sources: Q12, Q18_
- **OO-2**: Critical missing category: source credibility / signal-reliability dimension absent from output space [DATASET CRITICAL Concern 2]. Argentine hazard sub-labels (pampero, sudestada) and villa-impact framing are absent. TREC-IS priority labels (Low/Medium/High/Critical) are the closest existing precedent but not part of CrisisBench [WEB-15]. — _Sources: DATASET-D45, DATASET-D47, WEB-15_
- **OO-3**: Some categories encode non-regional framing: 'terrorism related' (17 instances [Q52]) and 'disease related' (CrisisNLP only [Q53]) reflect specific source-event distributions. The 'not humanitarian' class at 37.40% [Q56] dominates and may inherit North American assumptions about what counts as humanitarian-relevant. — _Sources: Q52, Q56_
- **OO-4**: Stakeholder-driven taxonomy redesign is warranted given the user-acknowledged credibility-scoring gap. The user's downstream construction approach (combining model outputs with external metadata) is a partial mitigation but not a benchmark-level fix. — _Sources: WEB-15, WEB-21_
- **OO-5**: Documented taxonomy issues: (a) absent credibility/reliability dimension (structural validity violation for the deployment's core construct); (b) absent Argentine sub-labels; (c) heterogeneous 'other_relevant_information' catch-all (Concern 7); (d) imbalanced classes with very low minority support [Q52–Q56]. — _Sources: Q88, DATASET-D33, DATASET-D10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'Informativeness (binary) and Humanitarian type (multi-class) classification' (p.2)
- [Q18] 'we use the class labels that are important for humanitarian aid for disaster response tasks, which are common across the publicly available resources' (p.2)
- [Q33] '"building damaged," originally used in the AIDR system, is mapped to "infrastructure and utilities damage"' (p.3)
- [Q52] 'Only 17 tweets with the label "terrrorism related" are present in CrisisNLP' (p.5)
- [Q56] 'distribution of "not humanitarian" is relatively higher (37.40%) than other class labels' (p.5)
- [Q88] 'we report the results of those classes only for which the model is able to classify' (p.8)

*Web sources:*
- [WEB-15] TREC-IS introduced priority/criticality labels (Low/Medium/High/Critical) as the closest existing benchmark precedent for credibility scoring; covers no Argentine events
- [WEB-21] 2024 NLP credibility survey documents fragmentation in credibility-aggregation literature; no integrated multi-signal benchmark

*Dataset analysis:*
- DATASET-D45: 'DEATH TOLL ... COVER UP!!!' tweet labelled not_informative — illustrates informativeness ≠ credibility
- DATASET-D47: Boston Bombing conspiracy tweet labelled informative — credibility-disjoint output space
- DATASET-D10: Political conflict listing labelled infrastructure_and_utilities_damage — taxonomy boundary misalignment
- DATASET-D33: Long Island home renovations advertisement in other_relevant_information — heterogeneous catch-all

</details>

**Information gaps:**
- Whether downstream credibility-scoring pipelines built on top of this benchmark's outputs achieve operationally useful F1 in Argentine deployment
- Whether external metadata (institutional affiliation, source popularity) the user envisions combining with model outputs is reliably available in Argentine post-Télam press environment

**Requires expert verification:**
- Argentine emergency management expert validation of which output categories are operationally critical vs. nice-to-have
- Whether TREC-IS priority labels would be a useful supplementation target for Argentine deployment

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Annotation provenance is minimally documented: the only directly attested annotation protocol is that AIDR data was labeled by domain experts [Q111]. For the remaining seven source datasets, no annotator demographics, recruitment methods, or inter-annotator agreement statistics are reported in the paper. Web research confirms CrisisNLP used crowdsourced workers with three-annotator agreement [WEB-18], but no Argentine annotators or Argentine-norm calibration is documented anywhere in the provenance chain. Cross-dataset evaluation reveals a 14.3% F1 drop when training on CrisisLex and evaluating on CrisisNLP [Q87], demonstrating that label conventions are not fully portable across event contexts — which raises substantial concern about portability to Argentine discourse. Dataset analysis empirically reveals concrete annotation noise: a Chilean cinema tweet labelled displaced_and_evacuations [DATASET-D1], NGO mission descriptions labelled requests_or_needs [DATASET-D37, D38], substantive typhoon warnings labelled not_informative [DATASET-D28, D30], philosophical text labelled informative [DATASET-D11], and Spanish-language disaster warnings systematically labelled not_informative [DATASET-D9, D8] — suggesting potential systematic under-recognition of Spanish-language disaster signals. Elicitation Q4 indicates Argentine professionals largely accept Global North label conventions, which softens but does not eliminate the concern.

**Strengths:**
- Argentine policy professionals draw on international (Global North) disaster communication standards as reference points (elicitation Q4), reducing expected systematic label disagreement for formal content
- AIDR subset has documented domain-expert annotation [Q111], providing a higher-confidence subset for evaluation

**Checklist:**

- **OC-1**: Partially — international (OCHA/ISCRAM-derived) label conventions used in the benchmark are recognized by Argentine emergency professionals (elicitation Q4), but Argentine institutional and journalistic norms for what constitutes a 'real signal' of disaster impact are not directly represented. Edge cases in political framing and informal-channel content are not aligned. — _Sources: Q111, WEB-18_
- **OC-2**: Likely disagreement at margins: Argentine political satire of government crisis response and lunfardo-inflected commentary may be misclassified. Dataset analysis shows Spanish-language disaster warnings labelled not_informative [DATASET-D9, D8], suggesting systematic Spanish-content under-recognition that would propagate to Argentine deployment. — _Sources: Q87, DATASET-D9, DATASET-D8_
- **OC-3**: Annotator demographics are not reported in the paper for seven of eight source datasets. Only AIDR is documented as domain-expert annotated [Q111]. CrisisNLP used crowdsourcing with three-annotator agreement [WEB-18] but demographics are not published. No Argentine annotators are documented. — _Sources: Q111, WEB-16, WEB-18_
- **OC-4**: Re-annotation by an Argentine annotator pool would be advisable for any deployment-critical evaluation; this is user-acknowledged as a gap (elicitation flag).
- **OC-5**: INSUFFICIENT DOCUMENTATION — paper does not describe aggregation methods or how minority annotator perspectives were handled across the eight constituent datasets.
- **OC-6**: Documented label issues: (a) annotator demographics undocumented for 7/8 sources; (b) 14.3% cross-dataset F1 drop signals non-portable conventions [Q87]; (c) empirically observable annotation noise [DATASET-D1, D37, D38, D28, D33]; (d) Spanish-content label asymmetry [DATASET-D9, D8]. These violate convergent and external validity for Argentine deployment. — _Sources: Q87, Q94, DATASET-D1, DATASET-D28, DATASET-D33, DATASET-D37, DATASET-D38_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q87] '14.3% difference in F1 on CrisisNLP data using the CrisisLex model for the informativeness task' (p.8)
- [Q94] 'Social media data is noisy and it often poses a challenge for labeling and training classifiers.' (p.9)
- [Q111] 'AIDR data has been labeled by domain experts using AIDR system' (p.11)

*Web sources:*
- [WEB-18] CrisisNLP used crowdsourced annotation with three-annotator agreement; demographics not published
- [WEB-16] CrisisLex T6 used crowdsourced workers for relatedness labels; no Argentine annotators documented

*Dataset analysis:*
- DATASET-D1: Chilean cinema tweet labelled displaced_and_evacuations — apparent annotation error
- DATASET-D9: Spanish-language Chilean earthquake aid warning labelled not_informative — systematic Spanish under-recognition risk
- DATASET-D8: Spanish meteorological typhoon warning labelled not_humanitarian — same Spanish-content asymmetry
- DATASET-D28: Quantitative typhoon warning labelled not_informative — boundary inconsistency
- DATASET-D33: Home renovations ad in other_relevant_information — clear annotation error
- DATASET-D37: Capability description labelled requests_or_needs — mislabel
- DATASET-D38: NGO mission statement labelled requests_or_needs — mislabel
- DATASET-D11: Philosophical/religious text labelled informative — boundary anomaly
- DATASET-D45: Sensationalist 'cover up' tweet labelled not_informative — credibility-disjoint label boundary

</details>

**Information gaps:**
- Annotator demographics, education levels, and recruitment for 7 of 8 source datasets
- Inter-annotator agreement statistics across source datasets
- Aggregation methods used to resolve disagreement across multi-annotator labels
- Whether the observed Spanish-language label asymmetry is systematic or sampling artifact

**Requires expert verification:**
- Argentine policy/journalism expert re-annotation of a stratified Spanish-language sample to quantify expected label disagreement
- Validation of whether AIDR's domain-expert subset performs differently on Argentine-relevant content than crowdsourced subsets

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Output form is MODERATE priority per elicitation. The benchmark produces discrete classification labels evaluated via weighted precision/recall/F1 [Q75], with documented model families (CNN [Q63], fastText [Q64], BERT/DistilBERT/RoBERTa [Q66]) achieving 0.866 F1 informativeness and 0.829 F1 humanitarian on consolidated English test set [Q84]. Hyperparameters are fully documented [Q113–Q121] and ten re-runs are performed for stability [Q72]. The output form is clean, reproducible, and suitable for downstream pipeline construction. However, two structural gaps remain: (a) the deployment envisions an aggregated continuous credibility score, which the benchmark does not produce — it requires downstream construction (user-acknowledged); no published pipeline combining CrisisBench outputs with external metadata exists [WEB-21]; (b) multilingual evaluation shows ~8% F1 drop on humanitarian classification using BERT [Q99], indicating that even where multilingual output is attempted, performance degrades substantially. Pre-trained models are mainly trained on non-Twitter text, an acknowledged limitation [Q65]. The discrete-to-continuous transformation is a structural gap but is bounded and tractable.

**Strengths:**
- Standard, reproducible evaluation methodology with weighted F1 chosen explicitly to handle class imbalance [Q75]
- Multiple model families benchmarked (CNN, fastText, transformers) with full hyperparameter documentation [Q113–Q121] and stability via 10 re-runs [Q72]
- Discrete classification labels are easily consumed by downstream credibility-aggregation pipelines, supporting the user's planned architecture

**Checklist:**

- **OF-1**: Partial mismatch: benchmark produces discrete classification labels; deployment envisions an aggregated continuous credibility score combining model outputs with external metadata. The user acknowledges this requires downstream construction. No published end-to-end credibility pipeline applicable to the deployment exists [WEB-21]. — _Sources: Q84, WEB-21_
- **OF-2**: Not applicable — deployment is text-only; no text-to-speech requirement.
- **OF-3**: Target cohort is high-literacy (master's degree+) [WEB-1, WEB-2]; literacy is not a constraint. Output form does not need accessibility adaptations for the analyst cohort. — _Sources: WEB-1_
- **OF-4**: Documented form mismatches: (a) discrete labels vs. envisioned continuous credibility score (user-acknowledged downstream construction step); (b) ~8% F1 drop in multilingual humanitarian classification [Q99] — output reliability degrades for non-English content. These threaten external validity for the operational credibility-scoring use case but are bounded. — _Sources: Q99, Q65_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q65] 'pre-trained models are mainly trained on non-Twitter text' (p.6)
- [Q72] 'we perform ten re-runs for each experiment using different seeds' (p.6)
- [Q75] 'weighted average precision (P), recall (R), and F1-measure (F1) ... takes into account the class imbalance problem' (p.7)
- [Q84] '0.866 (F1) for informativeness and 0.829 for humanitarian' (p.8)
- [Q99] '∼8% drop using BERT model' (p.9)

*Web sources:*
- [WEB-21] 2024 NLP credibility survey: aggregating multiple credibility signals into a unified score remains fragmented and underspecified
- [WEB-1] Argentine national literacy 98.08% (INDEC); target cohort effectively 100%

*Dataset analysis:*
- DATASET-D34: Calgary fire chief media announcement correctly labelled informative — output form usable for institutional-source filtering downstream

</details>

**Information gaps:**
- Whether downstream aggregation of CrisisBench classifier outputs with external Argentine source-metadata produces operationally useful credibility scores
- Whether the ~8% multilingual F1 drop generalizes to or worsens for Rioplatense Spanish

**Requires expert verification:**
- Validation by Argentine policy makers of what continuous credibility score thresholds are operationally meaningful for their decision-making

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Zero Argentine/Rioplatense Spanish content; 2010–2017 temporal window predates current Argentine institutional landscape (post-Télam, post-AFE)

**Recommendation:** Collect and annotate a stratified Argentine Twitter/X sample (covering pampero, sudestada, AMBA flash flood, ENSO drought, and villa-impact events) using the CrisisBench label schema; use this for fine-tuning and as a regional held-out evaluation set. Apply TREC-IS-style protocols [WEB-15] and the cross-lingual transfer approach from arXiv:2209.02139 [WEB-17].

### Output Ontology ⚠

**Gap:** No source credibility / signal-reliability dimension in the output space, which is the deployment's core requirement

**Recommendation:** Construct a downstream credibility-scoring layer combining CrisisBench classifier outputs with Argentine source-metadata streams (post-Télam press source registry, institutional affiliation, AFE/SINAGIR official channels, account history). Use TREC-IS priority labels (Low/Medium/High/Critical) [WEB-15] as the target output schema; align with Buenos Aires Province Resolución 4/2025 [WEB-11] for regulatory compliance.

### Output Content ⚠

**Gap:** Undocumented annotator demographics for 7 of 8 source datasets; observed annotation noise and systematic Spanish-language label asymmetry

**Recommendation:** Conduct re-annotation of a stratified Spanish-language and Argentine-political-satire sample by an Argentine policy/journalism expert pool to quantify expected label disagreement. Restrict deployment-critical evaluation to AIDR domain-expert-annotated subset where possible. Publish a Datasheet documenting Argentine annotator demographics and IAA.

### Input Form

**Gap:** Tweet-only benchmark does not cover deployment's news article and press release channels; lang_conf missing for CrisisMMD/AIDR subsets weakens language routing

**Recommendation:** Conduct cross-channel transfer evaluation by testing CrisisBench-trained classifiers on a held-out Argentine news article and press release corpus. Backfill lang_conf scores for affected examples using a current language-identification model. Consider TREC CrisisFACTS [WEB-20] as a multi-stream framework reference.

### Input Ontology

**Gap:** No sub-labels for Argentine hazard types (pampero, sudestada, ENSO drought, AMBA urban flash flood) or villa-impact framing

**Recommendation:** Extend the humanitarian taxonomy with Argentine hazard sub-labels and informal-settlement (villa) impact framing, validated with AMBA emergency management practitioners. Treat as a regional ontology overlay on top of CrisisBench's top-level categories rather than replacing them.

### Output Form

**Gap:** Discrete labels do not natively yield the aggregated continuous credibility score the deployment envisions; ~8% F1 drop in multilingual setting

**Recommendation:** Design the downstream credibility-aggregation function explicitly: define how classifier confidence scores combine with source-popularity, institutional-affiliation, and corroboration metadata to yield a continuous score. Validate score thresholds with AMBA policy makers and document the transformation pipeline for transparency under Argentine AI governance instruments [WEB-11, WEB-12].

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "We consolidate eight human-annotated datasets and provide 166.1k and 141.5k tweets for informativeness and humanitarian classification tasks, respectively." |
| Q2 | 1 | output_form | "We provide benchmarks for both binary and multiclass classification tasks using several deep learning architectures including, CNN, fastText, and transformers." |
| Q3 | 1 | input_ontology | "Typical classification tasks in the community include (i) informativeness (i.e., informative vs. not-informative messages), (ii) humanitarian information types (e.g., affected individual reports, infrastructure damage reports), and (iii) event types (e.g., flood, earthquake, fire)." |
| Q4 | 1 | output_form | "First, few efforts have been invested to develop standard datasets (specifically, train/dev/test splits) and benchmarks for the community to compare their results, models, and techniques." |
| Q5 | 1 | input_content | "Secondly, most of the published datasets are noisy, e.g., CrisisLex (Olteanu et al. 2014) contains duplicate and near-duplicate content, which produces misleading classification performance." |
| Q6 | 1 | input_form | "Moreover, some datasets (e.g., CrisisLex) consist of tweets from several languages without any explicit language tag, to separate the data of a particular language of interest." |
| Q7 | 1 | input_content | "We consolidate eight publicly available datasets (see Section 3)." |
| Q8 | 1 | output_ontology | "One of the challenges is the inconsistent class labels across various data sources." |
| Q9 | 1 | output_content | "Firoj Alam, Hassan Sajjad, Muhammad Imran, Ferda Ofli, Qatar Computing Research Institute, HBKU, Qatar" |
| Q10 | 2 | input_content | "We consolidate eight publicly available disaster-related datasets by manually mapping semantically similar class labels, which leads to a larger dataset." |
| Q11 | 2 | input_form | "We carefully cleaned various forms of duplicates, and assigned a language tag to each tweet." |
| Q12 | 2 | input_ontology | "We provide benchmark results on English tweets set using state-of-the-art machine learning algorithms such as Convolutional Neural Networks (CNN), fastText (Joulin et al. 2017) and pre-trained transformer models (Devlin et al. 2019) for two classifications tasks, i.e., Informativeness (binary) and Humanitarian type (multi-class) classification." |
| Q13 | 2 | input_form | "For the research community, we aim to release the dataset in multiple forms as, (i) a consolidated class label mapped version, (ii) exact- and near-duplicate filtered version obtained from previous versions, (iii) a subset of the filtered data used for the classification experiments in this study." |
| Q14 | 2 | input_content | "A major limitation of the work by Alam, Muhammad, and Ferda (2019) is that the issue of duplicate and near-duplicate content have not been addressed when combining the different datasets." |
| Q15 | 2 | input_content | "Kersten et al. (2019) focused only on informativeness classification and combined five different datasets. This study has also not focused on exact- and near-duplicate content, which exist in different datasets." |
| Q16 | 2 | output_form | "A fair comparison of the classification experiment is also difficult with previous studies as their train/dev/test splits are not public, except the dataset by Wiegmann et al. (2020)." |
| Q17 | 2 | input_content | "We address such limitations in this study, i.e., we consolidate the datasets, eliminate duplicates, and release standard dataset splits with benchmark results." |
| Q18 | 2 | output_ontology | "In this study, we use the class labels that are important for humanitarian aid for disaster response tasks, which are common across the publicly available resources." |
| Q19 | 2 | output_form | "The study of (Nguyen et al. 2017) and (Neppalli, Caragea, and Caragea 2018) performed comparative experiments between different classical and deep learning algorithms including Support Vector Machines, Logistic Regression, Random Forests, Recurrent Neural Networks, and Convolutional Neural Networks (CNN)." |
| Q20 | 2 | output_form | "Their experimental results suggest that CNN outperforms other algorithms." |
| Q21 | 2 | output_form | "Though in another study, (Burel and Alani 2018) reports that SVM and CNN can provide very competitive results in some cases." |
| Q22 | 2 | input_ontology | "We only focused on two tasks for this study and we aim to address event types task in a future study." |
| Q23 | 3 | input_ontology | "We consolidate eight datasets that were labeled for different disaster response classification tasks and whose labels can be mapped consistently for two tasks: informativeness and humanitarian information type classification." |
| Q24 | 3 | output_ontology | "In doing so, we deal with two major challenges: (i) discrepancies in the class labels used across different datasets, and (ii) exact- and near-duplicate content that exists within as well as across different datasets." |
| Q25 | 3 | input_content | "CrisisLex is one of the largest publicly-available datasets, which consists of two subsets, i.e., CrisisLexT26 and CrisisLexT6 (Olteanu et al. 2014). CrisisLexT26 comprises data from 26 different crisis events that took place in 2012 and 2013 with annotations for informative vs. not-informative as well as humanitarian categories (six classes) classification tasks among others. CrisisLexT6, on the other hand, contains data from six crisis events that occurred between October 2012 and July 2013 with annotations for related vs. not-related binary classification task." |
| Q26 | 3 | input_content | "CrisisNLP is another large-scale dataset collected during 19 different disaster events that happened between 2013 and 2015, and annotated according to different schemes including classes from humanitarian disaster response and some classes related to health emergencies (Imran, Mitra, and Castillo 2016)." |
| Q27 | 3 | input_content | "SWDM2013 dataset consists of data from two events: (i) the Joplin collection contains tweets from the tornado that struck Joplin, Missouri on May 22, 2011; (ii) The Sandy collection contains tweets collected from Hurricane Sandy that hit Northeastern US on Oct 29, 2012 (Imran et al. 2013a)." |
| Q28 | 3 | input_content | "ISCRAM2013 dataset consists of tweets from two different events occurred in 2011 (Joplin 2011) and 2012 (Sandy 2012). Note that this set of tweets are different than SWDM2013 set even though they are collected from same events (Imran et al. 2013b)." |
| Q29 | 3 | input_content | "Disaster Response Data (DRD) consists of tweets collected during various crisis events that took place in 2010 and 2012. This dataset is annotated using 36 classes that include informativeness as well as humanitarian categories." |
| Q30 | 3 | input_content | "Disasters on Social Media (DSM) dataset comprises 10K tweets collected and annotated with labels related vs. not-related to the disasters." |
| Q31 | 3 | input_content | "CrisisMMD is a multimodal dataset consisting of tweets and associated images collected during seven disaster events that happened in 2017 (Alam et al. 2018). The annotations for this dataset is targeted for three classification tasks: (i) informative vs. not-informative, (ii) humanitarian categories (eight classes) and (iii) damage severity assessment." |
| Q32 | 3 | input_content | "AIDR dataset is obtained from the AIDR system (Imran et al. 2014) that has been annotated by domain experts for different events and made available upon requests. We only retained labeled data that are relevant to this study." |
| Q33 | 3 | output_ontology | "The datasets come with different class labels. We create a set of common class labels by manually mapping semantically similar labels into one cluster. For example, the label "building damaged," originally used in the AIDR system, is mapped to "infrastructure and utilities damage" in our final dataset." |
| Q34 | 3 | output_ontology | "Some of the class labels in these datasets are not annotated for humanitarian aid purposes, therefore, we have not included them in the consolidated dataset. For example, we do not select tweets labeled as "animal management" or "not labeled" that appear in CrisisNLP and CrisisLex26." |
| Q35 | 3 | output_ontology | "This causes a drop in the number of tweets for both informativeness and humanitarian tasks as can be seen in Table 1 (Mapping column). The large drop in the CrisisLex dataset for the informativeness task is due to the 3,103 unlabeled tweets (i.e., labeled as "not labeled")." |
| Q36 | 3 | output_ontology | "The other significant drop for the informativeness task is in the DRD dataset. This is because many tweets were annotated with multiple labels," |
| Q37 | 4 | input_form | "To develop a machine learning model, it is important to design non-overlapping train/dev/test splits. A common practice is to randomly split the dataset into train/dev/test sets. This approach does not work with social media data as it generally contains duplicates and near duplicates. Such duplicate content, if present in both train and test sets, often leads to overestimated test results during classification." |
| Q38 | 4 | input_form | "We first tokenize the text before applying any filtering. For tokenization, we used a modified version of the Tweet NLP tokenizer (O'Connor, Krieger, and Ahn 2010). Our modification includes lowercasing the text and removing URL, punctuation, and user id mentioned in the text. We then filter tweets having only one token." |
| Q39 | 4 | input_form | "We then use a similarity-based approach to remove the near-duplicates. To do this, we first convert the tweets into vectors using bag-of-ngram approach as a vector representation. We use uni- and bi-grams with their frequency-based representations. We then use cosine similarity to compute a similarity score between two tweets and flag them as duplicate if their similarity score is greater than the threshold value of 0.75." |
| Q40 | 4 | input_form | "To determine a plausible threshold value, we manually checked the tweets in different threshold bins (i.e., 0.70 to 1.0 with 0.05 interval) as shown in Figure 1, which we selected from consolidated informativeness dataset. By investigating the distribution and manual checking, we concluded that a threshold value of 0.75 is a reasonable choice." |
| Q41 | 4 | input_form | "As indicated in Table 1, there is a drop after filtering, e.g., ∼25% for informativeness and ∼20% for humanitarian tasks. It is important to note that failing to eradicate duplicates from the consolidated dataset would potentially lead to" |
| Q42 | 5 | input_form | "Some of the existing datasets contain tweets in various languages (i.e., Spanish and Italian) without explicit assignment of a language tag." |
| Q43 | 5 | input_form | "In addition, many tweets have codeswitched (i.e., multilingual) content." |
| Q44 | 5 | input_form | "We decided to provide a language tag for each tweet if it is not available with the respective dataset." |
| Q45 | 5 | input_form | "We used the language detection API of Google Cloud Services for this purpose." |
| Q46 | 5 | input_content | "Among different languages of informativeness tweets, English tweets appear to be highest in the distribution compared to any other language, which is 94.46% of 156,899." |
| Q47 | 5 | input_content | "Note that most of the non-English tweets appear in the CrisisLex dataset." |
| Q48 | 5 | output_ontology | "Distribution of class labels is an important factor for developing the classification model." |
| Q49 | 5 | output_ontology | "It is clear that there is an imbalance in class distributions in different datasets and some class labels are not present." |
| Q50 | 5 | output_ontology | "For example, the distribution of "not informative" class is very low in SWDM2013 and ISCRAM2013 datasets." |
| Q51 | 5 | output_ontology | "For the humanitarian task, some class labels are not present in different datasets." |
| Q52 | 5 | output_ontology | "Only 17 tweets with the label "terrrorism related" are present in CrisisNLP." |
| Q53 | 5 | output_ontology | "Similarly, the class "disease related" only appears in CrisisNLP." |
| Q54 | 5 | output_ontology | "The scarcity of the class labels poses a great challenge to design the classification model using individual datasets." |
| Q55 | 5 | output_ontology | "Even after combining the datasets, the imbalance in class distribution seems to persist (last column in Table 4)." |
| Q56 | 5 | output_ontology | "For example, the distribution of "not humanitarian" is relatively higher (37.40%) than other class labels." |
| Q57 | 5 | output_ontology | "In Table 4, we highlighted some class labels, which we dropped in the rest of the classification experiments conducted in this study." |
| Q58 | 5 | output_ontology | "However, tweets with those class labels will be available in the released datasets." |
| Q59 | 6 | input_form | "Although our consolidated dataset contains multilingual tweets, we only use tweets in English language in our experiments." |
| Q60 | 6 | input_form | "We split data into train, dev, and test sets with a proportion of 70%, 10%, and 20%, respectively, also reported in Table 5." |
| Q61 | 6 | input_ontology | "As mentioned earlier we have not selected the tweets with highlighted class labels in Table 4 for the classification experiments." |
| Q62 | 6 | output_form | "For the experiments, we use CNN, fastText, and pre-trained transformer models." |
| Q63 | 6 | output_form | "The current state-of-the-art disaster classification model is based on the CNN architecture." |
| Q64 | 6 | output_form | "For the fastText (Joulin et al. 2017), we used pre-trained embeddings trained on Common Crawl, which is released by fastText for English." |
| Q65 | 6 | input_content | "Though the pre-trained models are mainly trained on non-Twitter text, we hypothesize that their rich contextualized embeddings would be beneficial for the disaster domain." |
| Q66 | 6 | output_form | "In this work, we choose the pre-trained models BERT (Devlin et al. 2019), DistilBERT (Sanh et al. 2019), and RoBERTa (Liu et al. 2019) for the classification tasks." |
| Q67 | 6 | output_form | "We train the CNN models using the Adam optimizer (Kingma and Ba 2014)." |
| Q68 | 6 | output_form | "The batch size is 128 and maximum number of epochs is set to 1000." |
| Q69 | 6 | output_form | "We use a filter size of 300 with both window size and pooling length of 2, 3, and 4, and a dropout rate 0.02." |
| Q70 | 6 | output_form | "We set early stopping criterion based on the accuracy of the development set with a patience of 200." |
| Q71 | 6 | output_form | "For the experiments with fastText, we used default parameters except: (i) the dimension is set to 300, (ii) minimal number of word occurrences is set to 3, and (iii) number of epochs is 50." |
| Q72 | 6 | output_form | "Due to the instability of the pre-trained models as reported in (Devlin et al. 2019), we perform ten re-runs for each experiment using different seeds, and we select the model that performs best on the dev set." |
| Q73 | 6 | output_form | "For transformer-based models, we used a learning rate of 2e − 5, and a batch size of 8." |
| Q74 | 6 | input_form | "Prior to the classification experiment, we preprocess tweets to remove symbols, emoticons, invisi-" |
| Q75 | 7 | output_form | "To measure the performance of each classifier, we use weighted average precision (P), recall (R), and F1-measure (F1). The rationale behind choosing the weighted metric is that it takes into account the class imbalance problem." |
| Q76 | 7 | input_ontology | "The motivation of these experiments is to investigate whether model trained with consolidated dataset generalizes well across different sets. For the individual dataset classification experiments, we selected CrisisLex and CrisisNLP as they are relatively larger in size and have a reasonable number of class labels, i.e., six and eleven class labels, respectively." |
| Q77 | 7 | input_form | "Note that these are subsets of the consolidated dataset reported in Table 5. We selected them from train, dev and test splits of the consolidated dataset to be consistent across different classification experiments." |
| Q78 | 7 | output_form | "To understand the effectiveness of the smaller datasets, we run experiments by training the model using smaller datasets and evaluating using the consolidated test set." |
| Q79 | 7 | input_content | "The availability of annotated data for a disaster event is usually scarce. One of the advantages of our compiled data is to have identical classes across several disaster events. This enables us to combine the annotated data from all previous disasters for the classification." |
| Q80 | 7 | input_content | "Though this increases the size of the training data substantially, the classifier may result in sub-optimal performance due to the inclusion of heterogeneous data (i.e., a variety of disaster types and occurs in a different part of the world)." |
| Q81 | 7 | input_form | "We append a disaster event type as a token to each annotated tweet ti. More concretely, say tweet ti consists of k words {w1, w2, ..., wk}. We append a disaster event type tag di to each tweet so that ti would become {di, w1, w2, ..., wk}. We repeat this step for all disaster event types present in our dataset." |
| Q82 | 7 | input_ontology | "The event-aware training requires the knowledge of the disaster event type at the time of the test. If we do not provide a disaster event type, the classification performance will be suboptimal due to a mismatch between train and test." |
| Q83 | 7 | input_form | "Instead of appending the disaster event type to all tweets of a disaster, we randomly append disaster event type UNK to 5% of the tweets of every disaster. Note that UNK is now distributed across all disaster event types and is a good representation of an unknown event." |
| Q84 | 8 | output_form | "The model trained using the consolidated dataset achieves 0.866 (F1) for informativeness and 0.829 for humanitarian, which is better than the models trained using individual datasets." |
| Q85 | 8 | output_form | "Between CrisisLex and CrisisNLP, the performance is higher on CrisisLex dataset for both informativeness and humanitarian tasks (1st vs. 4th row in Table 6 for the informativeness, and 10th vs. 13th row for the humanitarian task in the same table.)." |
| Q86 | 8 | input_content | "This might be due to the CrisisLex dataset being larger than the CrisisNLP dataset." |
| Q87 | 8 | output_content | "The cross dataset (i.e., train on CrisisLex and evaluate on CrisisNLP) results shows that there is a drop in performance. For example, there is 14.3% difference in F1 on CrisisNLP data using the CrisisLex model for the informativeness task." |
| Q88 | 8 | output_ontology | "In the humanitarian task, for different datasets in Table 6, we have different number of class labels. We report the results of those classes only for which the model is able to classify." |
| Q89 | 8 | input_ontology | "Note that humanitarian task is a multi-class classification problem, which makes it a much more difficult task than the binary informativeness classification." |
| Q90 | 8 | output_form | "The transformer based models achieve higher performance compared to the CNN and fastText. We used three transformer based models, which varies in the parameter sizes. However, in terms of performance, they are quite similar." |
| Q91 | 8 | output_form | "BERT performs better than or on par with CNN across all classes. More importantly, BERT performs substantially better than CNN in the case of minority classes as highlighted in the table." |
| Q92 | 8 | output_form | "The event-aware training improves the classification performance by 1.3 points (F1) using CNN for the humanitarian task compared to the results without using event information (see Table 6). However, no improvement has been observed for the informativeness task." |
| Q93 | 8 | input_ontology | "The training using event information enables the system to use data of all disasters while preserving the disaster-specific distribution." |
| Q94 | 9 | output_content | "Social media data is noisy and it often poses a challenge for labeling and training classifiers." |
| Q95 | 9 | input_form | "Our analysis on publicly available datasets reveals that one should follow a number of steps before preparing and labeling any social media dataset, not just the dataset for crisis computing. Such steps include (i) tokenization to help in the subsequent phase, (ii) remove exact- and near-duplicates, (iii) check for existing data where the same tweet might be annotated for the same task, and then (iv) labeling." |
| Q96 | 9 | output_form | "For designing the classifier, we postulate checking the overlap between training and test splits to avoid any misleading performance." |
| Q97 | 9 | input_form | "It is important to emphasize the fact that the results reported in this study are reliable as they are obtained on a dataset that has been cleaned from duplicate content, which might have led to misleading performance results otherwise." |
| Q98 | 9 | input_content | "Our initial consolidated datasets (i.e., Table 3 and 4) contains multilingual content with more class labels and different types of content (e.g., disease-related), therefore, an interesting future research could be to try different pre-trained multilingual models to classify tweets in different languages." |
| Q99 | 9 | output_form | "We observe that performance dropped significantly for the humanitarian task compared to English-only dataset. For example, ∼8% drop using BERT model." |
| Q100 | 9 | input_content | "The resulting dataset covers a time-span starting from 2010 to 2017, which can be used to study temporal aspects in crisis scenarios." |
| Q101 | 9 | input_form | "We tried to bridge this gap by consolidating existing datasets, filtering exact- and near-duplicates, and providing benchmarks based on state-of-the-art CNN, FastText, and transformer-based models." |
| Q102 | 9 | input_content | "The developed consolidated labeled dataset is curated from different publicly available sources." |
| Q103 | 10 | input_content | "We release the dataset by maintaining the license of existing resources." |
| Q104 | 11 | input_content | "In Table 11, we report the events associated with the respective datasets such as ISCRAM2013, SWDM2013 CrisisLex and CrisisNLP." |
| Q105 | 11 | input_content | "The time-period is from 2011 to 2015, which is a good representative of temporal aspects." |
| Q106 | 11 | output_ontology | "In Table 12, we report class label mapping for ISCRAM2013, SWDM2013, CrisisLex and CrisisNLP datasets." |
| Q107 | 11 | output_ontology | "Note that all humanitarian class labels also mapped to informative, and not humanitarian labels mapped to not-informative in the data preparation step." |
| Q108 | 11 | output_ontology | "In Table 13, we report the class label mapping for informativeness and humanitarian tasks for DRD dataset." |
| Q109 | 11 | output_ontology | "The DSM dataset only contains tweets labeled as relevant vs not-relevant, which we mapped for informativeness task as shown in Table 14." |
| Q110 | 11 | output_ontology | "The CrisisMMD dataset has been annotated for informativeness and humanitarian task, therefore, very minor label mapping was needed as shown in Table in 15." |
| Q111 | 11 | output_content | "The AIDR data has been labeled by domain experts using AIDR system and has been labeled during different events." |
| Q112 | 11 | input_form | "We have chosen a value of > 0.75 to filter duplicate tweets." |
| Q113 | 11 | output_form | "In this section, we report parameters for CNN and BERT model." |
| Q114 | 11 | output_form | "All experimental scripts will be publicly Hyper-parameters include:" |
| Q115 | 11 | output_form | "Batch size: 8" |
| Q116 | 11 | output_form | "Number of epochs: 10" |
| Q117 | 11 | output_form | "Max seq length: 128" |
| Q118 | 11 | output_form | "Learning rate (Adam): 2e-5" |
| Q119 | 11 | output_form | "BERT (bert-base-uncased): L=12, H=768, A=12, total parameters = 110M; where L is number of layers (i.e., Transformer blocks), H is the hidden size, and A is the number of self-attention heads." |
| Q120 | 11 | output_form | "DistilBERT (distilbert-base-uncased): it is a distilled version of the BERT model consists of 6-layer, 768-hidden, 12-heads, 66M parameters." |
| Q121 | 11 | output_form | "RoBERTa (roberta-large): it is using the BERT-large architecture consists of 24-layer, 1024-hidden, 16-heads, 355M parameters." |
| Q122 | 11 | output_form | "In Table 18 and 19, we provide detail results for different datasets (English Tweets) with different models." |
| Q123 | 13 | output_ontology | "Table 12: Class label mapping and grouping for CrisisLex, CrisisNLP, ISCRAM2013, and SWDM2013 datasets. The symbol (✗) indicates we do not map the tweets with that label for this study." |
| Q124 | 14 | output_ontology | "The symbol (✗) indicates we do not map the tweets with that label for this study." |
| Q125 | 15 | output_ontology | "Table 16: Class label mapping for AIDR system." |
| Q126 | 16 | input_form | "Sim. refers to similarity value. Dup. refers to whether we consider them as duplicate and filtered." |
| Q127 | 16 | input_form | "The symbol (✗) indicates a duplicate, which we dropped and the symbol (✓) indicates a not duplicate, which we have included in our dataset." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.perfil.com/noticias/sociedad/el-censo-argentino-arrojo-98-de-alfabetizacion-en-el-pais-pero-no-se-refleja-en-las-aulas.phtml |
| WEB-2 | https://es.theglobaleconomy.com/Argentina/Literacy_rate/ |
| WEB-3 | https://datareportal.com/reports/digital-2024-argentina |
| WEB-4 | https://www.trade.gov/country-commercial-guides/argentina-digital-economy |
| WEB-5 | https://freedomhouse.org/country/argentina/freedom-net/2024 |
| WEB-6 | https://www.unesco.org/en/articles/assessing-internet-development-argentina |
| WEB-7 | https://www.statista.com/topics/6709/internet-usage-in-argentina/ |
| WEB-8 | https://en.wikipedia.org/wiki/T%C3%A9lam |
| WEB-9 | https://www.boletinoficial.gob.ar/detalleAviso/primera/309815/20240701 |
| WEB-10 | https://www.mhewc.org/argentina/ |
| WEB-11 | https://regulations.ai/regulations/argentina-summary |
| WEB-12 | https://digital.nemko.com/regulations/ai-regulation-argentina |
| WEB-13 | https://english.alarabiya.net/News/world/2024/07/02/argentina-government-shuts-state-news-agency-telam |
| WEB-14 | https://www.techandjustice.bsg.ox.ac.uk/research/argentina |
| WEB-15 | https://trecis.github.io/ |
| WEB-16 | https://crisislex.org/data-collections.html |
| WEB-17 | https://arxiv.org/abs/2209.02139 |
| WEB-18 | https://aclanthology.org/L16-1259.pdf |
| WEB-19 | https://www.dcs.gla.ac.uk/~richardm/TREC_IS/2018/Evaluation.html |
| WEB-20 | https://crisisfacts.github.io/ |
| WEB-21 | https://arxiv.org/html/2410.21360v2 |
| WEB-22 | https://www.idea.int/democracytracker/report/argentina/march-2024 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** QCRI/CrisisBench-all-lang (configs: `humanitarian`, `informativeness`)
**Analysis date:** 2025-01-30
**Examples reviewed:** 131 (humanitarian, train split) + 140 (informativeness, train split) = 271 total
**Columns shown:** id, event, source, text, lang, lang_conf, class_label
**Columns skipped (media):** none (text-only dataset)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | humanitarian | Ex. 19 | displaced_and_evacuations | "El trabajo de la mejor Daniela López que conozco en pantalla grande #mataraunhombe #chile #cinema… http://t.co/asAx6KqNvD" | Spanish tweet about Chilean film, labelled displaced/evacuations — apparent annotation error | OC |
| D2 | humanitarian | Ex. 83 | sympathy_and_support | "RT @FlorrGo: #FuerzaChile ,un 2 de abril ... Que vengan los ingleses a ayudarlos ahora ... A la larga o a la corta ,todo vuelve" | Chilean Spanish earthquake solidarity tweet — not Argentine/Rioplatense | IC |
| D3 | humanitarian | Ex. 106 | sympathy_and_support | "Que lindo saber que en mi ciudad bella #Iquique hay gente con un corazón enorme dispuestos a ayudar... Emocionada" | Chilean Spanish (Iquique city) solidarity tweet — Chilean, not Argentine | IC |
| D4 | informativeness | Ex. 88 | not_informative | "#FuerzaChile jaja y piden ayuda jaja que los ayuden los ingleses manga de traidores" | Chilean Spanish tweet expressing contempt for requesting outside help — not Argentine | IC |
| D5 | informativeness | Ex. 89 | informative | "Declaran tres días de luto nacional por accidente de tren en España: Testigos afirman que el tren… http://t.co/pAcRQGdjFv" | Spanish-language tweet about Spain train crash | IC |
| D6 | informativeness | Ex. 37 | informative | "IMPRESIONANTE terremoto Chile camara de seguridad farmacia - NEW VIDEO E...: http://t.co/bkUElKfFUj vía @YouTube" | Chilean Spanish earthquake tweet — Chilean Spanish, not Rioplatense | IC |
| D7 | informativeness | Ex. 127 | informative | "RT @marieli_d: Nuevamente se incendia #Amuay http://t.co/AiWlhgy3" | Venezuelan Spanish tweet about refinery explosion | IC |
| D8 | humanitarian | Ex. 117 | not_humanitarian | "RT @meteomostoles: El tifón #BOPHA,de cat.4 y 947hPa en su centro,va camino de Filipinas.Lleva vientos sostenidos entre 2010 y 249km/h h ..." | Spanish tweet about Philippines typhoon — meteorological content labelled not_humanitarian | OC |
| D9 | informativeness | Ex. 106 | not_informative | "Ojo con el exceso de ayuda por los efectos del #TerremotoenChile porque puede producir mucho más obstáculos de lo que se cree." | Chilean Spanish warning about over-donation — labelled not_informative despite substantive crisis-relevant content | OC |
| D10 | humanitarian | Ex. 102 | infrastructure_and_utilities_damage | "Middle East right now:\nIS about to seize Ramadi\nAl-Qaeda seizes Yemen airport\nSaudi regime executes Indonesian women\nIran exports terrorism" | Political/conflict tweet from AIDR labelled infrastructure damage — apparent mislabel | OC |
| D11 | informativeness | Ex. 1 | informative | "when the ambushes of this century, hold closes even when life puts you in discomfiture, hold closes even that one of condescends your family, so God will facilitate you shortcoming" | Philosophical/religious text labelled informative — no disaster content | OC |
| D12 | informativeness | Ex. 3 | informative | "Sweater weather indeed 🌂 #RubyPH" | Short weather comment during typhoon labelled informative — minimal disaster signal | OC |
| D13 | informativeness | Ex. 7 | informative | "i hope everyone is safe" | Generic safety wish labelled informative | OC |
| D14 | informativeness | Ex. 83 | informative | "This hurricane thingy is looking pretty scary! I'm kinda excited by insane weather..." | Personal reaction labelled informative | OC |
| D15 | informativeness | Ex. 121 | informative | "one of the boston bombing suspects looks a bit like rob kardashian. do I have to wait for the new series to find out" | Celebrity comparison tweet during crisis labelled informative | OC |
| D16 | humanitarian | Ex. 9 | not_humanitarian | "New saying for the day... RG 3 and out - A #Steelers fan at the bar" | Sports commentary during Hurricane Sandy — clear not_humanitarian example | OO |
| D17 | humanitarian | Ex. 26 | personal_update | "Tornado watch until 3am. Of course we just got our new garage door today. *sigh*" | Personal complaint about tornado watch — Joplin 2011, North American event | IC |
| D18 | humanitarian | Ex. 11 | personal_update | "RT @tarnsnastylad: They need to name hurricanes better!.. superstorm Sandy? Seriously??.. Sounds like a FUCKING gay wrestler!" | Crude personal opinion during Sandy — North American vernacular | IC |
| D19 | humanitarian | Ex. 16 | affected_individual | "Floods kill 3, 75,000 forced from Calgary homes http://t.co/c6OPFjFLkA | AP #news" | News headline about Canadian flood — affected individuals, clear label | OO |
| D20 | humanitarian | Ex. 2 | caution_and_advice | "As many as 100,000 people could be forced from their homes by heavy flooding in western Canada. Water levels peak today at noon." | Factual caution about Canadian floods | OO |
| D21 | humanitarian | Ex. 57 | caution_and_advice | "RT @frankowolf1: il comune di Mirandola cerca ing. e arch. contattare Polizia Municipale: 0535/611039, 800/197197 #terremoto" | Italian tweet seeking engineers after earthquake — non-English caution | IC/IF |
| D22 | humanitarian | Ex. 30 | sympathy_and_support | "Mi è piaciuto un video di @YouTube: http://t.co/l5MttNyHPa Alluvione in Sardegna: commenti idioti" | Italian tweet about Sardinia floods — "liked a video about idiotic comments on flooding" | IC |
| D23 | humanitarian | Ex. 44 | sympathy_and_support | "Lac-Mégantic: Éric Forest sur place pour donner son appui http://t.co/wKSAXEtZWm" | French tweet about Canadian train crash — politician on site | IC |
| D24 | humanitarian | Ex. 113 | sympathy_and_support | "RT @portalR7: Tragédia no RS: Dilma chora ao falar sobre vítimas http://t.co/ybxETDmD #R7 #SantaMaria" | Portuguese tweet about Brazil nightclub fire, Dilma crying | IC |
| D25 | humanitarian | Ex. 95 | infrastructure_and_utilities_damage | "After deadly Brazil nightclub fire, safety questions emerge. http://t.co/ah4JK2v2" | Brazil nightclub fire — closest geographic proximity to Argentina | IO |
| D26 | humanitarian | Ex. 6 | infrastructure_and_utilities_damage | "The flood is feared to submerge the bridge roads leading Larkana and Khairpur districts." | Pakistan flood infrastructure — no Argentine geographic relevance | IC |
| D27 | humanitarian | Ex. 49 | infrastructure_and_utilities_damage | "Torrential rains have damaged Kenya's infrastructure, severing road links between Nairobi and Garissa, where the air base of the World Food Programme (WFP) is located." | Africa infrastructure damage — internationally framed | IC |
| D28 | informativeness | Ex. 34 | not_informative | "A tropical cyclone will affect my area. Winds of greater than 100 kph up to 185 kph may be expected in at least 18 hours. #TyphoonHagupit" | Substantive typhoon warning labelled not_informative — clear label inconsistency | OC |
| D29 | informativeness | Ex. 6 | not_informative | "#sobering Helicopter crash into pub in #glasgow! http://t.co/0uYSOocUvu" | Breaking news tweet labelled not_informative | OC |
| D30 | informativeness | Ex. 52 | not_informative | "Bangladesh:palazzo non era per fabbriche: Il progetto del Rana Plaza prevedeva solo 6 piani non 9 o 10 http://t.co/VG9qCqa3xX" | Italian investigative tweet about Rana Plaza building code — labelled not_informative | OC |
| D31 | humanitarian | Ex. 25 | other_relevant_information | "Update on the fertilizer explosion in West, Texas. Estimated 50 to 60 dead, hundreds injured, half of town flattened." | North American industrial explosion — would fit affected_individuals or injured_dead | OO |
| D32 | humanitarian | Ex. 52 | other_relevant_information | "being in a hurricane inside a house with no lights ..." | Personal experience tweet labelled other_relevant_information | OC |
| D33 | humanitarian | Ex. 111 | other_relevant_information | "Check out these award winning Long Island renovations: #longisland #suffolk https://t.co/wLnIbOENK9" | Completely unrelated home renovations tweet in other_relevant_information | OC |
| D34 | informativeness | Ex. 111 | informative | "RT @cityofcalgary: Acting Fire Chief, Ken Uzeloc, will address the media at Ogden Road and 17 Street S.E. at 10 p.m. #yyc #yycflood" | Official municipal announcement — clear informative label, Canadian context | OO |
| D35 | humanitarian | Ex. 28 | requests_or_needs | "I'M ASKING HELP FOR MY FAMILY WHICH IS VICTIM AND WHICH TAKE REFUGE IN PROVINCE." | Direct help request from disaster victim | OO |
| D36 | humanitarian | Ex. 42 | requests_or_needs | "We have water but we need food. Please in Masson Leogane." | Haiti-context needs request — Global South event | IO |
| D37 | humanitarian | Ex. 90 | requests_or_needs | "Equipped with a power generator and air conditioner, the tents can also house an emergency medical center." | Capability description mislabelled as requests_or_needs — annotation inconsistency | OC |
| D38 | humanitarian | Ex. 98 | requests_or_needs | "AmeriCares solicits donations of medicines, medical supplies, and other relief materials from manufacturers, and delivers them quickly and reliably to indigenous health and welfare professionals in 137 countries around the world." | NGO capability description labelled requests_or_needs — mislabel | OC |
| D39 | humanitarian | Ex. 1 | affected_individual | "@lucilledizon: 517 ilang ilang st. bayanihan vilage cainta rizal, David Bautista +63 905 826 5094. Needs rescue @MMDA @govph #rescuePH" | Tagalog rescue request — non-English, Philippine event, clear label | IF |
| D40 | humanitarian | Ex. 79 | infrastructure_and_utilities_damage | "RT @MoralesForLife: Chocolate Hills, napinsala ng Magnitude 7.2 na lindol #PrayForVisayas Pray For Cebu and Bohol also in Mindanao! http://…" | Tagalog tweet about Philippines earthquake damage | IF |
| D41 | informativeness | Ex. 23 | informative | "#Terremoto: secondo Il Foglio &egrave; un Castigo di Dio - foto http://t.co/GuMvqzl0" | Italian earthquake tweet labelled informative | IF |
| D42 | humanitarian | Ex. 14 | response_efforts | "#Tacloban has 49 evacuation centers now sheltering over 30,000 people + @care is helping respond to #typhoonhagupit http://t.co/ePE9MsdpTh" | Clear response effort tweet — CARE NGO involvement | OO |
| D43 | humanitarian | Ex. 3 | disease_related | "Investors Pump Prospects Of Unproven Ebola Treatments: Drugs in development to treat Ebola virus are far from … http://t.co/hv7lcUzha3" | Ebola treatment investor article — disease_related | OO |
| D44 | humanitarian | Ex. 60 | infrastructure_and_utilities_damage | "Colorado floods shut down hundreds of oil and gas wells; recovery will take time: Colorado's oil and... http://t.co/HivwsVtrc8 #Oil #BRK" | North American oil/gas infrastructure damage | IO |
| D45 | informativeness | Ex. 128 | not_informative | "https://t.co/najVJNt4Ip DEATH TOLL Now under Investigation for COVER UP!!! https://t.co/VuGGPYboIv" | Credibility-ambiguous tweet about death toll cover-up labelled not_informative | OO |
| D46 | humanitarian | Ex. 24 | not_humanitarian | "RT @eclecticbrotha: @AlGiordano Damn, I forgot how much of a shitshow Bernie's Puerto Rico operation was." | Political commentary during Hurricane Maria | IC |
| D47 | informativeness | Ex. 31 | informative | "I was told I'm ignorant to think the Boston Bombing wasn't planned by the government to keep our attention away from schemes being planned." | Conspiracy tweet labelled informative | OC |
| D48 | humanitarian | Ex. 33 | disease_related | "Scientists find MERS virus antibodies that may lead to treatments http://t.co/0YAMcmulxD" | MERS treatment research tweet | OO |

---

### Deployment-Relevant Strengths

#### Strength 1: Broad disaster type coverage across humanitarian labels
- **Dimension(s):** IO, OO
- **Observation:** The 15-class humanitarian label schema covers categories directly relevant to Argentine disaster response triage: `affected_individual`, `infrastructure_and_utilities_damage`, `injured_or_dead_people`, `displaced_and_evacuations`, `requests_or_needs`, `response_efforts`, `caution_and_advice`, and `donation_and_volunteering`. These top-level categories map onto the functional needs of Buenos Aires policy makers assessing disaster communication quality regardless of event geography.
- **Deployment relevance:** Argentine emergency management agencies (SINAGIR, AFE) operate within ISCRAM-derived frameworks that recognise these same broad categories. The label schema is thus sufficiently compatible with the international standards Argentine professionals treat as reference points.
- **Datapoint citations:**
  - [D19] Example 16 (humanitarian, train, affected_individual): "Floods kill 3, 75,000 forced from Calgary homes http://t.co/c6OPFjFLkA | AP #news" — straightforward affected-individuals label, clear annotation.
  - [D20] Example 2 (humanitarian, train, caution_and_advice): "As many as 100,000 people could be forced from their homes by heavy flooding in western Canada. Water levels peak today at noon." — clear actionable caution label.
  - [D35] Example 28 (humanitarian, train, requests_or_needs): "I'M ASKING HELP FOR MY FAMILY WHICH IS VICTIM AND WHICH TAKE REFUGE IN PROVINCE." — unambiguous needs signal.
  - [D42] Example 14 (humanitarian, train, response_efforts): "#Tacloban has 49 evacuation centers now sheltering over 30,000 people + @care is helping respond to #typhoonhagupit http://t.co/ePE9MsdpTh" — clear response-efforts label.
  - [D43] Example 3 (humanitarian, train, disease_related): "Investors Pump Prospects Of Unproven Ebola Treatments: Drugs in development to treat Ebola virus are far from … http://t.co/hv7lcUzha3" — disease-related label functions.

#### Strength 2: Binary informativeness task provides a usable signal-triage foundation
- **Dimension(s):** OO, OF
- **Observation:** The informativeness config cleanly separates clearly off-topic social chatter from disaster-relevant content across a wide range of events. The not_informative examples in the sample include sports commentary, celebrity gossip, spam, and personal chitchat, while informative examples range from official municipal announcements to direct eyewitness reports.
- **Deployment relevance:** For Buenos Aires policy makers whose first-pass task is filtering noisy signals from informative crisis content, the binary informativeness layer provides a deployable triage function. Although it does not natively score credibility, it operationalises the first step in the downstream credibility pipeline the user envisions.
- **Datapoint citations:**
  - [D16] Example 9 (humanitarian, train, not_humanitarian): "New saying for the day... RG 3 and out - A #Steelers fan at the bar" — unambiguous noise example.
  - [D34] Example 111 (informativeness, train, informative): "RT @cityofcalgary: Acting Fire Chief, Ken Uzeloc, will address the media at Ogden Road and 17 Street S.E. at 10 p.m. #yyc #yycflood" — official institutional announcement correctly labelled informative.
  - [D36] Example 42 (humanitarian, train, requests_or_needs): "We have water but we need food. Please in Masson Leogane." — clear needs signal from Global South context.

#### Strength 3: Multi-event, multi-geography training distribution
- **Dimension(s):** IC, IO
- **Observation:** The 131 humanitarian examples span at least 20 named events across Asia, North America, South Asia, Europe, the Middle East, and Africa, including floods, earthquakes, hurricanes, disease outbreaks, industrial accidents, and building collapses. This breadth means classifiers trained on this data have exposure to diverse disaster communication registers, not just a single event type.
- **Deployment relevance:** Argentine disaster scenarios span floods, windstorms, earthquakes (low risk), and industrial accidents. A classifier trained on event-diverse data is less likely to fail categorically on event types that were absent from a narrower training set, even if Argentine-specific events are not present.
- **Datapoint citations:**
  - [D25] Example 95 (humanitarian, train, infrastructure_and_utilities_damage): "After deadly Brazil nightclub fire, safety questions emerge." — industrial accident type represented.
  - [D27] Example 49 (humanitarian, train, infrastructure_and_utilities_damage): "Torrential rains have damaged Kenya's infrastructure, severing road links between Nairobi and Garissa…" — African flood infrastructure — broad geographic spread.
  - [D44] Example 60 (humanitarian, train, infrastructure_and_utilities_damage): "Colorado floods shut down hundreds of oil and gas wells; recovery will take time…" — oil/gas infrastructure damage relevant to Argentine Vaca Muerta industrial context.

#### Strength 4: Presence of some non-English and non-North-American content
- **Dimension(s):** IC, IF
- **Observation:** The sampled examples include Italian (Ex. 30, 44, 57, 131 in informativeness), French (Ex. 44 humanitarian), Portuguese (Ex. 113 humanitarian), Tagalog (Ex. 1, 79, 93, 128 humanitarian), and multiple Spanish tweets (Ex. 19, 83, 106 humanitarian; Ex. 37, 67, 88, 89, 106, 127 informativeness). Language tags are present, enabling filtering. The CrisisMMD 2017 events add international disaster diversity.
- **Deployment relevance:** While none of the Spanish content is Argentine or Rioplatense, its presence demonstrates the dataset is not exclusively US/UK English and that non-Latin-alphabet and Romance-language registers have been annotated. For a deployment that must handle multilingual input streams, the label schema has at least been exposed to non-English content at the margins.
- **Datapoint citations:**
  - [D21] Example 57 (humanitarian, train, caution_and_advice): "RT @frankowolf1: il comune di Mirandola cerca ing. e arch. contattare Polizia Municipale: 0535/611039, 800/197197 #terremoto" — Italian caution/advice tweet correctly labelled.
  - [D39] Example 1 (humanitarian, train, affected_individual): "@lucilledizon: 517 ilang ilang st. bayanihan vilage cainta rizal, David Bautista +63 905 826 5094. Needs rescue @MMDA @govph #rescuePH" — Tagalog rescue request correctly labelled affected_individual.
  - [D5] Example 89 (informativeness, train, informative): "Declaran tres días de luto nacional por accidente de tren en España: Testigos afirman que el tren… http://t.co/pAcRQGdjFv" — Spanish-language disaster tweet labelled informative.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Complete absence of Argentine or Rioplatense Spanish content
- **Dimension(s):** IC, IF
- **Observation:** All 271 sampled examples contain zero instances of Argentine events, Argentine institutional actors, or Rioplatense Spanish. The Spanish-language tweets in the sample are Chilean (events: `2014_chile_earthquake`, `2014_chile_earthquake_esp`), Venezuelan (`2012_venezuela_refinery-explosion`), and Spanish (`2013_spain_train-crash_en-mixed`). No lunfardo register, no Argentine agency names (SINAGIR, AFE, SENAPRED), no Buenos Aires Metropolitan Area geography, no Rioplatense voseo constructions, and no Argentine political framing appear anywhere in the sample.
- **Deployment relevance:** The deployment's core channel — Argentine Twitter/X — features Rioplatense Spanish with distinctive lexical, syntactic, and pragmatic features (voseo, lunfardo, political satire, institutional irony) that are entirely absent from the training distribution. A classifier trained on this benchmark will encounter an out-of-distribution linguistic register on every Spanish-language Argentine social media post it processes. This is the single most consequential alignment gap for the deployment.
- **Datapoint citations:**
  - [D2] Example 83 (humanitarian, sympathy_and_support): "RT @FlorrGo: #FuerzaChile ,un 2 de abril ... Que vengan los ingleses a ayudarlos ahora ... A la larga o a la corta ,todo vuelve" — Chilean Spanish, not Argentine; no Rioplatense register.
  - [D3] Example 106 (humanitarian, sympathy_and_support): "Que lindo saber que en mi ciudad bella #Iquique hay gente con un corazón enorme dispuestos a ayudar... Emocionada" — Iquique is in Chile; no Argentine content.
  - [D6] Example 37 (informativeness, informative): "IMPRESIONANTE terremoto Chile camara de seguridad farmacia - NEW VIDEO E...: http://t.co/bkUElKfFUj vía @YouTube" — Chilean earthquake, Chilean Spanish.
  - [D7] Example 127 (informativeness, informative): "RT @marieli_d: Nuevamente se incendia #Amuay http://t.co/AiWlhgy3" — Venezuelan refinery explosion; Venezuelan Spanish.

#### Concern 2: No credibility, misinformation, or source reliability dimension in the output schema
- **Dimension(s):** OO, OF
- **Observation:** Neither the humanitarian nor informativeness config contains any label, score, or metadata field relating to source credibility, institutional authority, misinformation likelihood, or signal reliability. The schema fields are: id, event, source, text, lang, lang_conf, class_label. The `source` field records dataset provenance (e.g., `crisismmd`, `crisisnlp-cf`), not tweet author credibility. No tweet-level credibility metadata is present.
- **Deployment relevance:** The primary output requirement for the Buenos Aires policy-maker cohort is a trustworthiness or reliability score. The benchmark produces only binary informativeness and multi-class humanitarian type labels. This gap is user-acknowledged as requiring downstream construction, but the data itself provides no foundation for learning source credibility signals. Notably, Example D45 (a "DEATH TOLL Now under Investigation for COVER UP!!!" tweet labelled not_informative) and D47 (a conspiracy tweet labelled informative) illustrate that the existing labels do not align with a credibility axis — credible and non-credible content appear on both sides of the informativeness divide.
- **Datapoint citations:**
  - [D45] Example 128 (informativeness, not_informative): "https://t.co/najVJNt4Ip DEATH TOLL Now under Investigation for COVER UP!!! https://t.co/VuGGPYboIv" — credibility-ambiguous sensationalist content labelled not_informative; offers no credibility signal.
  - [D47] Example 31 (informativeness, informative): "I was told I'm ignorant to think the Boston Bombing wasn't planned by the government to keep our attention away from schemes being planned." — conspiracy content labelled informative, illustrating that informativeness ≠ credibility.
  - [D10] Example 102 (humanitarian, infrastructure_and_utilities_damage): "Middle East right now:\nIS about to seize Ramadi\nAl-Qaeda seizes Yemen airport\nSaudi regime executes Indonesian women\nIran exports terrorism" — political conflict content labelled infrastructure damage; no credibility dimension.

---

#### MAJOR

#### Concern 3: Substantial annotation noise and label inconsistency observable in sample
- **Dimension(s):** OC
- **Observation:** Multiple examples in both configs exhibit annotation patterns that would be inconsistent or incorrect by any reasonable standard, suggesting the label quality the deployment would be training/evaluating against is uneven. Specific problems observed: (a) a Chilean Spanish tweet about a cinema film labelled `displaced_and_evacuations`; (b) an NGO capability description labelled `requests_or_needs`; (c) a tent/generator infrastructure description labelled `requests_or_needs`; (d) a substantive typhoon warning labelled `not_informative`; (e) a Long Island home renovations advertisement in `other_relevant_information`; (f) a political conflict tweet labelled `infrastructure_and_utilities_damage`.
- **Deployment relevance:** For a deployment where policy makers need reliable classification outputs to feed a credibility scoring pipeline, noisy ground-truth labels reduce the trustworthiness of any model trained or evaluated on this benchmark. Cross-dataset F1 degradation (14.3%, noted in the YAML) is at least partially explained by these label inconsistencies. Argentine stakeholders calibrating against this benchmark may encounter a noisy signal floor that undermines the pipeline's practical utility.
- **Datapoint citations:**
  - [D1] Example 19 (humanitarian, displaced_and_evacuations): "El trabajo de la mejor Daniela López que conozco en pantalla grande #mataraunhombe #chile #cinema…" — Chilean film discussion labelled displaced_and_evacuations; likely annotation error.
  - [D37] Example 90 (humanitarian, requests_or_needs): "Equipped with a power generator and air conditioner, the tents can also house an emergency medical center." — capability description, not a request; mislabelled.
  - [D38] Example 98 (humanitarian, requests_or_needs): "AmeriCares solicits donations of medicines, medical supplies, and other relief materials from manufacturers, and delivers them quickly and reliably to indigenous health and welfare professionals in 137 countries around the world." — NGO mission statement labelled requests_or_needs; more accurately donation_and_volunteering or response_efforts.
  - [D28] Example 34 (informativeness, not_informative): "A tropical cyclone will affect my area. Winds of greater than 100 kph up to 185 kph may be expected in at least 18 hours. #TyphoonHagupit" — specific quantitative typhoon warning labelled not_informative.
  - [D33] Example 111 (humanitarian, other_relevant_information): "Check out these award winning Long Island renovations: #longisland #suffolk https://t.co/wLnIbOENK9" — entirely unrelated home renovation content in other_relevant_information.
  - [D10] Example 102 (humanitarian, infrastructure_and_utilities_damage): "Middle East right now:\nIS about to seize Ramadi\nAl-Qaeda seizes Yemen airport…\nIran exports terrorism" — political/conflict listing labelled infrastructure damage.

#### Concern 4: Informativeness label boundaries are culturally unstable for Argentine social media
- **Dimension(s):** OC, IC
- **Observation:** Several examples labelled `informative` in the sample carry minimal disaster-relevant content by any standard, while content with substantive disaster information is sometimes labelled `not_informative`. The observed boundary appears to conflate "crisis-adjacent" with "informative," accepting sympathetic sentiment tweets, celebrity references, and personal reactions as informative. Argentine Twitter/X discourse is characterised by political satire and institutional irony — content that superficially resembles the `not_informative` patterns in the benchmark but may carry genuine crisis signals.
- **Deployment relevance:** If the Argentine deployment system inherits these ambiguous label boundaries, it risks classifying Argentine political commentary on government crisis response as not_informative (missing real signals) or misclassifying satirical content as informative. This is particularly acute given the noted Argentine norm of political framing in crisis coverage and the dissolution of Télam, which has dispersed official crisis communication signals across a more fragmented landscape.
- **Datapoint citations:**
  - [D11] Example 1 (informativeness, informative): "when the ambushes of this century, hold closes even when life puts you in discomfiture, hold closes even that one of condescends your family, so God will facilitate you shortcoming" — philosophical/religious text with no disaster content, labelled informative.
  - [D12] Example 3 (informativeness, informative): "Sweater weather indeed 🌂 #RubyPH" — weather comment during typhoon labelled informative; near-zero disaster signal.
  - [D13] Example 7 (informativeness, informative): "i hope everyone is safe" — generic sentiment, labelled informative.
  - [D14] Example 83 (informativeness, informative): "This hurricane thingy is looking pretty scary! I'm kinda excited by insane weather..." — personal reaction, labelled informative.
  - [D29] Example 6 (informativeness, not_informative): "#sobering Helicopter crash into pub in #glasgow! http://t.co/0uYSOocUvu" — breaking news tweet labelled not_informative despite containing disaster event reference.
  - [D30] Example 52 (informativeness, not_informative): "Bangladesh:palazzo non era per fabbriche: Il progetto del Rana Plaza prevedeva solo 6 piani non 9 o 10 http://t.co/VG9qCqa3xX" — Italian investigative report on building code violation labelled not_informative.

#### Concern 5: North American and North Atlantic event dominance distorts register and cultural framing
- **Dimension(s):** IC
- **Observation:** The personal_update and not_humanitarian categories are dominated by North American vernacular English: American sports references, US political discourse, and North American cultural referents. Personal_update examples include Sandy-era tweets referencing Joplin tornado and North American colloquial register. The social chatter that the benchmark trains models to recognise as "noise" is specifically North American social noise, not Argentine social noise.
- **Deployment relevance:** Argentine social media "noise" differs structurally from US social media noise: it includes political satire of the Milei government's handling of floods, lunfardo-inflected commentary, references to local institutional actors (AMBA prefectura, Buenos Aires province civil defense), and WhatsApp-style forwarded messages. A classifier trained to recognise US sports commentary as not_informative may misclassify Argentine political satire about disaster response — which could carry real signals about institutional credibility — in either direction.
- **Datapoint citations:**
  - [D17] Example 26 (humanitarian, personal_update): "Tornado watch until 3am. Of course we just got our new garage door today. *sigh*" — North American personal complaint about Joplin tornado watch; this is the register the classifier learns as "personal_update."
  - [D18] Example 11 (humanitarian, personal_update): "RT @tarnsnastylad: They need to name hurricanes better!.. superstorm Sandy? Seriously??.. Sounds like a FUCKING gay wrestler!" — North American vernacular during Sandy.
  - [D46] Example 24 (humanitarian, not_humanitarian): "RT @eclecticbrotha: @AlGiordano Damn, I forgot how much of a shitshow Bernie's Puerto Rico operation was." — US political commentary during Hurricane Maria labelled not_humanitarian; analogue Argentine political commentary on AFE crisis response would face the same classification challenge.

#### Concern 6: Spanish-language examples present carry Chilean/Venezuelan register, not Rioplatense, and show annotation inconsistency
- **Dimension(s):** IC, OC
- **Observation:** The Spanish-language examples in the sample are all from Chilean or Venezuelan events and use standard Chilean/Venezuelan register. One Chilean Spanish tweet (Ex. 88, informativeness: "#FuerzaChile jaja y piden ayuda jaja que los ayuden los ingleses manga de traidores") reflects Chilean political sentiment about foreign aid and is labelled not_informative. Another substantive Spanish tweet with disaster hashtags (Ex. 106, informativeness: "Ojo con el exceso de ayuda por los efectos del #TerremotoenChile porque puede producir mucho más obstáculos de lo que se cree.") is also labelled not_informative despite containing a crisis-relevant public warning about aid logistics. This suggests the annotation schema may systematically under-recognise disaster-relevance in Spanish-language content.
- **Deployment relevance:** If Spanish-language disaster warnings are being labelled not_informative in the benchmark, any model trained on this data will be systematically biased against recognising Spanish-language disaster signals — directly undermining the Argentine deployment's core function of triage across Spanish-language social media content.
- **Datapoint citations:**
  - [D9] Example 106 (informativeness, not_informative): "Ojo con el exceso de ayuda por los efectos del #TerremotoenChile porque puede producir mucho más obstáculos de lo que se cree." — crisis-relevant Spanish warning about aid logistics labelled not_informative.
  - [D4] Example 88 (informativeness, not_informative): "#FuerzaChile jaja y piden ayuda jaja que los ayuden los ingleses manga de traidores" — Chilean political sentiment during earthquake, not_informative.
  - [D8] Example 117 (humanitarian, not_humanitarian): "RT @meteomostoles: El tifón #BOPHA,de cat.4 y 947hPa en su centro,va camino de Filipinas.Lleva vientos sostenidos entre 2010 y 249km/h h ..." — Spanish-language meteorological warning about a typhoon labelled not_humanitarian, despite containing specific wind-speed and track data.

---

#### MINOR

#### Concern 7: `other_relevant_information` class is a heterogeneous catch-all with low semantic coherence
- **Dimension(s):** OO, OC
- **Observation:** The `other_relevant_information` class in the humanitarian config functions as a residual bucket containing content ranging from clear factual updates ("PAGASA says typhoon has further weakened") to personal experience tweets ("being in a hurricane inside a house with no lights") to a benefit concert announcement to a completely unrelated home renovations advertisement. This class's semantic incoherence limits its usefulness as a training or evaluation signal.
- **Deployment relevance:** For a deployment trying to classify Argentine crisis communication quality, a 13% catch-all class (166/500 buffer examples are other_relevant_information) that conflates substantive updates with noise will produce unreliable outputs for borderline content — precisely the category most relevant to a credibility scoring task where the interesting cases are not clearly informative or clearly noise.
- **Datapoint citations:**
  - [D32] Example 52 (humanitarian, other_relevant_information): "being in a hurricane inside a house with no lights ..." — personal experience, arguably not crisis-informative.
  - [D31] Example 25 (humanitarian, other_relevant_information): "Update on the fertilizer explosion in West, Texas. Estimated 50 to 60 dead, hundreds injured, half of town flattened." — this appears to be injured_or_dead_people or affected_individual rather than other_relevant_information.
  - [D33] Example 111 (humanitarian, other_relevant_information): "Check out these award winning Long Island renovations: #longisland #suffolk https://t.co/wLnIbOENK9" — entirely unrelated content; should be not_humanitarian.

#### Concern 8: Temporal gap — all events 2010–2017; Argentine institutional landscape has changed materially since 2017
- **Dimension(s):** IC
- **Observation:** All events in the sample span 2010–2017 (oldest: 2011 Joplin tornado; newest: 2017 Hurricane Maria/Irma/Harvey). The Argentine institutional context relevant to the deployment has changed substantially since 2017: Télam was dissolved in July 2024, AFE was created in 2025, and the current political environment (Milei administration) has altered the credibility landscape for official disaster communications.
- **Deployment relevance:** Social media conventions, platform norms (Twitter/X after Musk acquisition), and Argentine institutional credibility signals have all shifted since 2017. A classifier trained on 2010–2017 tweet patterns may misclassify post-2022 content that uses different hashtagging conventions, link formats, and institutional citation patterns.
- **Datapoint citations:**
  - [D17] Example 26 (humanitarian, personal_update): "Tornado watch until 3am." (2011 Joplin) — oldest event; Twitter conventions of 2011 differ from 2024.
  - [D46] Example 24 (humanitarian, not_humanitarian): "RT @eclecticbrotha: @AlGiordano Damn, I forgot how much of a shitshow Bernie's Puerto Rico operation was. https://t.co/DgZMF2qnNl" — 2017 Hurricane Maria, pre-Musk Twitter, pre-Télam dissolution.

#### Concern 9: `lang_conf` field is missing (NA) for many CrisisMMD and AIDR examples, complicating language-stratified filtering
- **Dimension(s):** IF
- **Observation:** A large number of examples from `crisismmd` and `aidr_system` sources have `lang_conf: NA` rather than a numeric confidence score. This means the language detection confidence is unavailable for these examples, making it impossible to filter by language detection reliability. Given that the deployment needs to handle Spanish-language content differently from English content, the absence of confidence scores for a significant subset of examples weakens the language-stratification capability of the dataset.
- **Deployment relevance:** For the Argentine deployment, reliable language identification is prerequisite to routing content to appropriate classifiers (English vs. Spanish models). The NA confidence values in the CrisisMMD and AIDR subsets — which include 2017 events most temporally proximate to the deployment window — reduce confidence in automated language-based routing decisions built on this benchmark's language metadata.
- **Datapoint citations:**
  - [D5] Example 5 (humanitarian, donation_and_volunteering): "#Fox914 encourages you to unite and give to those who are affected... #FloodSL #srilanka #colombo #kandy #lka https://t.co/iLgsSCJ06b" — `lang_conf: NA` from crisismmd source.
  - [D42] Example 14 (humanitarian, response_efforts): "#Tacloban has 49 evacuation centers now sheltering over 30,000 people + @care is helping respond to #typhoonhagupit http://t.co/ePE9MsdpTh" — `lang_conf: NA` from crisisnlp-volunteers source.
  - [D10] Example 102 (humanitarian, infrastructure_and_utilities_damage): "Middle East right now:\nIS about to seize Ramadi…" — `lang_conf: NA` from aidr_system source.

---

### Content Coverage Summary

The 271 sampled examples reveal a dataset that is predominantly English-language (~88% of sampled examples), drawn from North American and global events spanning 2010–2017, with a strong concentration in US hurricanes (Sandy, Harvey, Irma, Maria), Philippines typhoons, Nepal earthquake, Pakistan floods, and Joplin tornado. The humanitarian config represents 15 classes with notable imbalance: `not_humanitarian` and `other_relevant_information` together account for the majority of buffer-sampled examples (366/500), consistent with the documented 37.4% not_humanitarian rate. Non-English content is present but sparse: Italian (3–4 examples), French (1), Portuguese (1), Tagalog (4–5), and Spanish (6–8 examples), all from non-Argentine events. The Spanish content is exclusively Chilean and Venezuelan.

Register is predominantly short-form social media (Twitter), ranging from professional news retweets to personal social chatter, with some longer structured text from the DRD (Figure Eight) dataset representing more formal humanitarian situation reports. The DRD examples are notably different in register from tweets — they read as structured field reports or aid request forms — introducing within-benchmark register heterogeneity. The `other_relevant_information` class functions as a heterogeneous residual category. Label quality is uneven, with observable annotation errors in both configs that reduce confidence in benchmark scores as indicators of real-world classification capability.

No Argentine, Rioplatense Spanish, Buenos Aires-specific, or Pampa/Patagonia/Río de la Plata content appears in the sample. The hazard types represented (North Atlantic hurricanes, South Asian floods, Philippines typhoons, North American tornadoes) do not include pampero windstorms, sudestada events, ENSO-driven droughts, or urban flash floods in dense Latin American metropolitan settings.

---

### Limitations

1. **Sample size per class:** The stratified buffer over 15 humanitarian classes produces small per-class samples (2–25 examples for rare classes like `displaced_and_evacuations`, `missing_and_found_people`, `personal_update`). Annotation quality and label consistency observations for these rare classes are based on 2–4 examples and should be treated as directional, not definitive.

2. **Train split only:** All examples are from the train split. Test and dev split distributions, label quality, and language composition are not directly inspected and may differ.

3. **No access to raw tweet metadata:** The dataset provides text, event, source, lang, and class_label, but not tweet author metadata (account type, follower count, verified status), timestamps, or geolocation — all relevant to the deployment's credibility scoring aspiration. The absence of these fields from the schema is a structural limitation of the dataset, not a sampling artefact.

4. **Language detection accuracy unverified:** The `lang` field relies on Google Cloud Language Detection API. Misdetections (e.g., short tweets, code-switched content) cannot be verified from the text alone for non-Latin-script or mixed-language examples.

5. **CrisisMMD multimodal data:** CrisisMMD was originally a multimodal dataset (tweets + images). The HF dataset appears to contain only the text component. Image-based disaster signals from CrisisMMD are not inspectable or evaluated here.

6. **Informativeness label semantics vary by source dataset:** The informativeness label maps from different original schemas (relevant/not-relevant in DSM; informative/not-informative in CrisisLex). The observed label inconsistencies in the informativeness config may partly reflect this multi-source mapping rather than annotation error within any single source.

