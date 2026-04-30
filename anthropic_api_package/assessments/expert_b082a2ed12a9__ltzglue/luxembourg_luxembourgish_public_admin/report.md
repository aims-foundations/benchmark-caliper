## Deployment Context

**Use case:** In a public administration setting, a civil servant uses LLM-powered software to manage Luxembourgish citizen feedback by applying a model evaluated on topic classification, named entity recognition, intent detection, and sentiment analysis. The system automatically categorizes messages by domain and identifies key entities while classifying user intent and gauging sentiment to help detect frustrated users. These outputs enable the automated routing of requests to specific departments and the immediate prioritization of disgruntled or urgent correspondence, ensuring administrative actions are triggered accurately based on the content and tone of the message.
**Target population:** Civil servants in Luxembourgish government agencies who process digital correspondence and citizen inquiries written in the diverse orthographic styles of the Luxembourgish language.

# Validity Analysis: ltzglue
**Target context:** Luxembourg Public Administration — Civil Servant NLU Deployment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 3 | Moderate gaps | medium |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 3 | Moderate gaps | medium |
| **Average** | **2.2** | | |

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

LTZGLUE is a credible first GLUE-style NLU benchmark for Luxembourgish and a valuable resource for general LTZ NLP capability assessment. However, for the specific deployment of routing citizen correspondence in Luxembourg public administration, validity is materially limited across the four HIGH-priority dimensions (IO, IC, OO, OC). The most severe gap is output ontology: LTZGLUE produces single hard labels across taxonomies (RTL editorial topics, voice-assistant intents, ternary sentiment) that do not encode the administrative routing categories, multi-label structure, confidence scores, urgency scaling, or language-of-input axis the deployment requires. Input content reflects predominantly formal/institutional registers, with the authors themselves warning this does not represent informal and multilingual contexts — precisely the distribution of real citizen correspondence given Luxembourg's ~47% frontalier workforce and entrenched code-switching. Annotation quality is moderate (κ=0.45 on sentiment) and lacks documented administrative-domain expertise. Input form and output form mismatches are moderate: text-to-label alignment is preserved, but length/language filtering and absence of calibration/multi-label metrics weaken external validity. The benchmark's authors explicitly caution against using performance as evidence of cultural or demographic coverage [Q121], and this caution applies directly here.

## Practical Guidance

### What This Benchmark Measures

LTZGLUE measures general Luxembourgish NLU capability of encoder models and prompted LLMs across eight tasks (NER, topic, sentiment, acceptability, intent, RTE, headline acceptability). It is a useful instrument for selecting a base model with strong LTZ representation (e.g., MMBERT-base, LUXEMBERT, LTZ-E1) and for screening basic linguistic competence. Its NER component, in particular, can support entity extraction in citizen correspondence at a foundational level.

### Construct Depth

Depth is shallow for the deployment's specific constructs. The benchmark probes language-level NLU (lexical, syntactic, basic semantic) with reasonable rigor, but it does not probe administrative-domain construct dimensions: routing topic taxonomy, state-vs-communal competency discrimination, frontalier-specific terminology, formal-but-understated frustration detection, multi-label decisions, or language-of-input identification. Sentiment with κ=0.45 [Q27] and voice-assistant intents [Q154] cover only a thin slice of the operational construct space.

### What Else You Need

(1) IO/OO: a Luxembourg-administrative topic taxonomy and multi-label dataset co-designed with civil servants, including state-vs-communal axis and confidence-threshold rules. (2) IC: a held-out evaluation set sampled from real citizen correspondence (anonymized under GDPR/CNPD guidance [WEB-9, WEB-10, WEB-11]) covering code-switched, orthographically variable, and frontalier-specific content. (3) OC: re-annotation by administrative-experienced annotators with reported per-class agreement and a register-aware sentiment/urgency scheme. (4) OF: calibration evaluation (ECE, reliability) and multi-label metrics (micro/macro-F1, hamming loss). (5) Compliance: a DPIA and EU AI Act risk classification analysis [WEB-12, WEB-13] before deployment.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
LTZGLUE provides a GLUE-style suite of eight tasks covering binary and multi-class sentence- and token-level classification [Q11, Q67], which is a credible general-purpose NLU foundation for Luxembourgish. However, for the specific deployment — routing citizen correspondence to government departments — the taxonomies are misaligned. Topic classification covers only five RTL editorial categories (SPORTS, CULTURE, TECHNOLOGY, BUSINESS, ANIMALS) [Q48, Q153] with no administrative categories such as cross-border worker issues, housing, transport, tax, social security, or communal vs. national competency routing — all flagged as required in the elicitation and regional context. Intent detection labels are exclusively voice-assistant commands (alarm, reminder, weather) [Q154], with no administrative intents (complaint, document request, escalation). The benchmark contains no multi-label task formulation [Q67], whereas the deployment requires multi-label outputs [elicitation Q4]. The authors themselves acknowledge no unified benchmark currently exists for LTZ NLU [Q14]. Given IO is HIGH priority and the gaps span both omission (administrative categories) and irrelevance (voice-assistant intents) for this deployment, this constitutes significant taxonomic misalignment.

**Strengths:**
- Provides eight diverse NLU task formulations including NER, topic classification, sentiment, RTE, and acceptability, establishing a baseline construct coverage for Luxembourgish [Q11, Q67]
- A substantial proportion of tasks are newly created for LTZ rather than direct translations, enabling some language-specific phenomena [Q69]
- NER schema includes PER, ORG, LOC, MISC, DATE [Q152] which has partial overlap with entities relevant to administrative correspondence (named persons, organizations, locations)

**Checklist:**

- **IO-1**: The deployment requires categories for cross-border worker / frontalier issues, housing/cost-of-living, transport, tax, social security, EU institutional matters, residency permits, communal services, public health, plus a state-vs-communal routing dimension and multi-label outputs with confidence scores [elicitation Q1, Q4; regional context administrative_domain_notes]. — _Sources: WEB-5, WEB-2_
- **IO-2**: Yes — none of LTZGLUE's topic classes (SPORTS, CULTURE, TECHNOLOGY, BUSINESS, ANIMALS) [Q48, Q153] correspond to administrative routing categories, and intent detection covers only voice-assistant commands [Q154]. No state-vs-communal competency dimension or multi-label formulation exists [Q67]. — _Sources: Q48, Q153, Q154, Q67_
- **IO-3**: Yes — the voice-assistant intent labels (alarm, reminder, weather sub-intents) [Q154] are construct-irrelevant for administrative correspondence routing. The RTE logical-entailment framing [Q59] is unrelated to routing decisions, though it may have ancillary value for general LLM evaluation. — _Sources: Q154, Q59_
- **IO-4**: Major content-validity gap: the benchmark cannot assess routing taxonomy performance for cross-border worker issues, housing, transport, tax, communal vs. national competencies — the categories that drive operational value [regional context benchmark_validity_risks_summary.input_ontology_gap]. The absence of multi-label formulation [Q67] additionally prevents evaluation of the deployment's required output structure. — _Sources: Q67, Q14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q11] 'In this section, we introduce the eight tasks for LTZGLUE. The set spans binary and multi-class sentence and token-level classification tasks.' (p.2)
- [Q14] 'No unified benchmark currently exists to evaluate LTZ language understanding consistently, a gap we aim to fill.' (p.2)
- [Q48] 'From the available categories, we focused on five principal domains: SPORTS, CULTURE, TECHNOLOGY, BUSINESS, and ANIMALS.' (p.4)
- [Q67] 'Together, the eight tasks in LTZGLUE form a broad and balanced evaluation suite, covering four binary and four multi-class settings, sentence- and document-level inputs, as well as a token-level sequence-labelling task.' (p.5)
- [Q153] 'topic_classification: Classify topic of the document by title and text. Allowed category_names: sports, animals, business, culture, technology.' (p.15)
- [Q154] 'slot_intent_detection: Detect the intent for the text given. Allowed intents: reminder/show_reminders, weather/find, reminder/set_reminder...' (p.15)

*Web sources:*
- [WEB-5] ~231,290 cross-border workers in Q1 2024, ~47% of Luxembourg employment — supports salience of frontalier topic category
- [WEB-2] OECD 2025: 50% of frontaliers from France, remainder split between Belgium and Germany — supports differentiated administrative-query profile

</details>

**Information gaps:**
- Whether any LTZ-specific administrative-domain benchmark or taxonomy exists outside LTZGLUE — flagged as not searched in regional context
- Formal enumeration of communal vs. national competencies needed to define a routing taxonomy

**Requires expert verification:**
- Final administrative topic taxonomy and multi-label structure must be co-designed with civil servants and legal/administrative experts

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Benchmark inputs are drawn predominantly from RTL news articles, the Luxembourgish Online Dictionary, Wikipedia/Wikidata, and a translated English voice-assistant corpus [Q12, Q16, Q24, Q30, Q34, Q46, Q51]. The authors explicitly warn that 'most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts' [Q112], and that LTZ data 'often originate from a limited set of public domains' [Q119]. The deployment, however, expects orthographically variable, code-switched (Luxembourgish/French/German) citizen correspondence [elicitation Q2; regional context languages.code_switching_patterns]. Only the human-annotated NER sub-corpus from RTL user comments provides partial coverage of informal and code-mixed writing [Q41]. The intent detection corpus uses a voice-assistant register that has no LTZ reference, so terminology could not be systematically verified [Q55, Q56]. Given that ~47% of Luxembourg's workforce are frontaliers (mostly French-speaking) [WEB-5, WEB-2] and the language law requires the administration to respond in the citizen's chosen language [WEB-14], the benchmark's content distribution is materially narrower than the deployment input distribution. IC is HIGH priority and the documented gaps are substantial.

**Strengths:**
- Lothritz et al. NER sub-corpus from RTL online news comments provides partial informal and code-mixed writing coverage [Q40, Q41]
- Authors transparently document content limitations, register narrowness, and demographic-coverage caveats [Q110, Q112, Q119, Q121]
- Pre-training corpus for LTZ-E1 includes broader registers (user comments, webchat, transcribed podcasts and political speeches) [Q74], which may benefit downstream model representations even if task evaluation is narrower

**Checklist:**

- **IC-1**: Yes — citizen correspondence requires handling of orthographically variable Luxembourgish, French/German code-switching, frontalier-specific terminology, and Luxembourg-specific institutional vocabulary [elicitation Q2; regional context languages.code_switching_patterns, cultural_norms_notes]. The benchmark inputs are dominated by RTL news and dictionary content [Q12, Q16, Q46], which do not encode this distribution. — _Sources: Q12, Q112, WEB-5, WEB-14_
- **IC-2**: Partially. Sources are Luxembourgish in origin so cultural framing is locally grounded, but the institutional/journalistic register diverges from citizen-government correspondence [Q112]. The voice-assistant intent corpus is translated from English without LTZ register reference [Q55, Q56], introducing alien register material. — _Sources: Q112, Q55, Q56_
- **IC-3**: Yes — the xSID-derived intent corpus (alarm/reminder/weather) [Q51, Q55] is Western voice-assistant content with no administrative analogue in Luxembourg; its inputs encode construct-irrelevant register. Authors note pre-training data overlap with LLMs may also inflate performance [Q111]. — _Sources: Q51, Q55, Q111_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no Luxembourg civil-administration domain experts appear to have reviewed task inputs for representativeness; the elicitation flags this as needing real-time civil-servant feedback for progressive alignment [elicitation Q3].
- **IC-5**: Documented content-validity issues: (a) formal/institutional register dominance [Q112], (b) absence of systematic code-switching coverage outside NER [Q41], (c) voice-assistant register import without LTZ reference [Q55, Q56], (d) no representation of frontalier-specific administrative content [WEB-5]. — _Sources: Q112, Q41, Q55, Q56, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'Unless stated otherwise, the textual data used across most tasks stems from two main sources' (p.2)
- [Q41] 'It covers a wider range of text types and registers, including informal and code-mixed writing' (p.4)
- [Q55] 'The source segments consist of user commands for a voice-controlled AI assistant, representing a specialised spoken register for which there is no equivalent reference corpus in LTZ' (p.5)
- [Q56] 'Due to the lack of LTZ references in this register, it was not possible to systematically verify the translated terminology.' (p.5)
- [Q112] 'most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts' (p.9)
- [Q119] 'LTZ is a small language community, and linguistic data often originate from a limited set of public domains.' (p.10)

*Web sources:*
- [WEB-5] ~231,290 frontaliers (~47% of employment) — citizen-input distribution will be heavily multilingual
- [WEB-14] Law of 24 February 1984 Article 4 requires reply in citizen's chosen language — input language detection is legally salient
- [WEB-3] Constitutional anchoring of Luxembourgish since 1 July 2023 — political weight on processing standardized and non-standardized LTZ

</details>

**Information gaps:**
- No quantification of code-switching frequency in any task split
- No measure of orthographic-variation coverage in task inputs
- Whether RTL user-comment NER sub-corpus contains enough French/German switching to represent deployment distribution

**Requires expert verification:**
- Sampling and qualitative review of LTZGLUE task inputs by civil-administration linguists to confirm representativeness for citizen-correspondence content

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Form mismatch is moderate. Both benchmark and deployment are text-only in Latin script, so there is no modality or script-direction violation [regional context infrastructure_notes.deployment_modality; writing_systems]. Tokenization (BPE, vocab 50,368, max sequence 1,024) [Q128, Q129] is suitable for typical citizen-correspondence lengths (40–400 words covers many but not all messages [regional context infrastructure_notes.expected_input_length, Q47]). However, signal-distribution mismatch persists at the form level: task inputs are filtered to remove non-Luxembourgish text via OpenLID and constrained to 40–400 words [Q47], which removes precisely the multilingual and length-extreme inputs the deployment will encounter. The benchmark's text register (formal news, dictionary examples, transcribed political speeches) [Q74, Q16, Q30] differs from informal, orthographically variable citizen messages. IF is MODERATE priority; the form-level alignment is partial because text-text matching is achieved, but distributional filtering and register narrowness reduce external validity.

**Strengths:**
- Text-only modality matches deployment exactly [regional context infrastructure_notes.deployment_modality]
- Latin-script writing system aligns with all three administrative languages [regional context writing_systems]
- BPE tokenizer trained on broad LTZ pre-training corpus including comments, webchat, podcasts may handle orthographic variation reasonably [Q74, Q128]
- Sequence length cap of 1,024 tokens is sufficient for most short-to-medium correspondence

**Checklist:**

- **IF-1**: Both source and target are text. Length filter (40–400 words) [Q47] excludes very short and very long messages that are realistic in administrative correspondence (e.g., one-line inquiries, multi-page complaints). — _Sources: Q47, Q129_
- **IF-2**: Yes — Luxembourg has 99.0% internet penetration [WEB-7] and advanced digital infrastructure [regional context infrastructure_notes.connectivity]; data-capture specifications match. — _Sources: WEB-7_
- **IF-3**: Use-case-specific differences: filtering of non-Luxembourgish text via OpenLID [Q47] removes code-switched inputs that the deployment must actually process. Pre-training data is broader [Q74] but downstream task data is narrower in register. — _Sources: Q47, Q74, Q112_
- **IF-4**: External-validity concerns from (a) length filtering excluding tail of distribution, (b) language-detection filtering removing multilingual inputs, (c) register narrowness in downstream task data [Q47, Q112]. — _Sources: Q47, Q112_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q47] 'we removed articles identified as non-Luxembourgish by OpenLID (Burchell et al., 2023), as well as those containing fewer than 40 words or more than 400 words.' (p.4)
- [Q74] 'A large portion of the data stems from RTL... transcribed radio interviews... user comments... transcribed podcasts... transcribed political speeches and debates' (p.6)
- [Q128] 'a BPE-based tokenizer, which we train on the entire pre-training set, using a minimum frequency of two and a vocabulary size of 50,368.' (p.12)
- [Q129] 'a max sequence length of 1024.' (p.12)
- [Q112] 'most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts' (p.9)

*Web sources:*
- [WEB-7] 99.0% internet penetration in Luxembourg as of January 2024 — confirms text-channel deployment is well-supported

</details>

**Information gaps:**
- Empirical length distribution of expected citizen correspondence
- Empirical proportion of code-switched messages in real digital channels

**Requires expert verification:**
- Sample-level review of incoming citizen messages to validate that benchmark form constraints (length, language-purity filtering) do not exclude operationally important inputs

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Severe structural misalignment between benchmark output ontology and deployment requirements. All eight LTZGLUE tasks produce single hard labels [Q67] across narrow label spaces: binary headline acceptability [Q148], three-class sentiment [Q149], binary/four-class linguistic acceptability [Q33, Q151], BIO-tagged NER over PER/ORG/LOC/MISC/DATE [Q44, Q152], five-class topic [Q48, Q153], nine voice-assistant intents [Q154], and binary entailment [Q155]. The deployment explicitly requires multi-label classification with confidence scores for routing and human-fallback escalation [elicitation Q4], and demands administrative topic categories (cross-border worker, housing, transport, tax, communal vs. national) and urgency/frustration scales — none of which appear in any task. Sentiment's three-class scheme [Q149] cannot encode urgency or formal-but-understated frustration cues that are operationally significant per the elicitation [elicitation Q3] and regional cultural notes. EU AI Act considerations [WEB-12] and the language law's requirement to detect citizen language choice [WEB-14] introduce further required output dimensions (language-of-input, possibly risk flags) absent from the benchmark. OO is HIGH priority. This is the most severe dimension violation.

**Strengths:**
- Standard, well-documented label schemas (BIO for NER, ternary sentiment) that are interoperable with downstream pipelines [Q44, Q149, Q152]
- NER label set (PER, ORG, LOC, MISC, DATE) is partially useful for entity extraction within administrative messages [Q152]

**Checklist:**

- **OO-1**: Output labels are designed for general NLU evaluation, not administrative routing. Topic classes (sports, culture, technology, business, animals) [Q153] have no overlap with required routing categories. — _Sources: Q153, Q154_
- **OO-2**: Missing categories include: cross-border worker / frontalier issues, housing/cost-of-living, transport, tax, social security, EU institutional matters, residency permits, communal services, public health, plus a state-vs-communal routing axis and an urgency/escalation axis [regional context administrative_domain_notes; elicitation Q1, Q4]. — _Sources: WEB-12, WEB-14_
- **OO-3**: The voice-assistant intent labels (alarm/reminder/weather) [Q154] encode a non-administrative, non-Luxembourg-public-sector value framing — they are operational categories from a consumer assistant context, not civic communication. — _Sources: Q154_
- **OO-4**: Stakeholder-driven taxonomy redesign is necessary; the elicitation confirms that routing logic requires multi-label outputs and confidence-based escalation [elicitation Q4], implying co-design with civil servants and legal experts. — _Sources: Q67_
- **OO-5**: Structural validity is violated: the benchmark's single-label space cannot represent the multi-label decision structure [Q67 vs. elicitation Q4]. Content validity is violated through the absence of required administrative categories. External validity is at risk because performance on these tasks does not predict performance on the operational decision structure. — _Sources: Q67, Q149, Q153_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'The binary dataset distinguishes between correct (1) and incorrect (0)' (p.4)
- [Q44] 'the tag set is harmonised by merging the GPE and LOC categories into a single location label, while retaining PER, ORG, and MISC unchanged.' (p.4)
- [Q67] 'Together, the eight tasks in LTZGLUE form a broad and balanced evaluation suite, covering four binary and four multi-class settings' (p.5)
- [Q149] 'sentiment_analysis: Classify sentiment of the text. Allowed labels: positive, neutral, negative.' (p.15)
- [Q152] 'ner: Perform Named Entity Recognition... Allowed Tags: O, B-LOC, I-LOC, B-PER,I-PER, B-DATE, I-DATE,B-ORG, I-ORG, B-MISC, I-MISC.' (p.15)
- [Q153] 'topic_classification: ... Allowed category_names: sports, animals, business, culture, technology.' (p.15)
- [Q154] 'slot_intent_detection: ... Allowed intents: reminder/show_reminders, weather/find, reminder/set_reminder, ...' (p.15)

*Web sources:*
- [WEB-12] EU AI Act Annex III Category 5(a) high-risk classification potentially relevant — implies need for documented decision rules and oversight outputs not in benchmark
- [WEB-14] Language law requires response in citizen's chosen language — implies language-of-input output dimension absent from benchmark

</details>

**Information gaps:**
- Final list of required routing categories and confidence-threshold rules

**Requires expert verification:**
- Co-design of administrative topic taxonomy and multi-label/confidence scheme with civil servants, legal counsel (CNPD), and AI Act compliance officers

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Annotation provenance and quality are mixed and weakly tied to civil-administration norms. Sentiment was annotated by two native LTZ speakers with Cohen's Kappa 0.45 — moderate agreement — and disagreements resolved by consensus [Q25, Q26, Q27, Q28]; no documentation of administrative-register expertise. JUDGEWEL NER relies on LLM-as-judge with 'minimal human verification' [Q37]. RTE used ChatGPT-5-mini to verify labels, finding nearly 10% incorrect labels [Q63, Q64], with manual correction afterwards [Q65]. The intent detection translation lacked LTZ register references and could not be systematically verified [Q56]. Authors explicitly caution against 'using benchmark performance as evidence of cultural or demographic coverage' [Q121] and note 'models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices' [Q120]. For a deployment where sentiment must capture formal-but-understated frustration in civil correspondence [elicitation Q3, regional context cultural_norms_notes], κ=0.45 with consumer-facing news comments as source material is insufficient. OC is HIGH priority.

**Strengths:**
- Native LTZ speakers conducted sentiment annotation [Q25] and intent translation [Q52], grounding labels in language-native judgment
- Lothritz et al. NER sub-corpus is fully human-annotated with 'high-precision' result [Q42]
- RTE underwent multi-stage label verification with manual correction [Q63, Q64, Q65]
- Authors transparently disclose annotation limitations [Q113, Q120, Q121]

**Checklist:**

- **OC-1**: INSUFFICIENT DOCUMENTATION on whether labels reflect civil-administration stakeholder perspectives. Sentiment annotators are described only as native LTZ speakers [Q25]; no administrative or civil-service background is documented. — _Sources: Q25_
- **OC-2**: Likely disagreement risk is high for sentiment/urgency: regional culture features formal, understated expression of frustration [regional context cultural_norms_notes]; news-comment-trained annotators with κ=0.45 [Q27] are unlikely to encode that register reliably. — _Sources: Q27, Q120_
- **OC-3**: Documentation is partial — annotator counts and native-speaker status reported [Q25, Q52], but no demographic, professional, or domain-expertise breakdown provided. No Datasheet/Data Statement is referenced. — _Sources: Q25, Q52_
- **OC-4**: Re-annotation by civil-servant or administration-experienced annotators is recommended; the elicitation already provisions a real-time civil-servant feedback loop [elicitation Q3] but pre-deployment re-annotation would be additionally valuable.
- **OC-5**: Sentiment disagreements were resolved by consensus between two annotators [Q28], which can erase minority perspectives; this is a risk for a population with diverse linguistic backgrounds (frontaliers, non-native LTZ writers). — _Sources: Q28_
- **OC-6**: Convergent validity is at risk because labels may not correlate with civil-servant judgments of administrative correspondence; external validity is at risk because the source distribution (RTL comments, dictionary, voice-assistant) differs from citizen-administration correspondence [Q112, Q119]. — _Sources: Q112, Q119, Q121_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'we extract 4,583 sentences, which are then annotated by two native speakers of LTZ.' (p.3)
- [Q27] 'We calculated Cohen's Kappa at 0.45.' (p.3)
- [Q28] 'For the final set, the annotators agree on a label in cases of label disagreement.' (p.3)
- [Q37] 'The resulting sentences are then evaluated using LLMs acting as judges, with minimal human verification to calibrate quality thresholds.' (p.4)
- [Q52] 'The translations were performed by an LTZ native speaker. In cases of uncertainty, additional native LTZ speakers were consulted.' (p.4)
- [Q56] 'Due to the lack of LTZ references in this register, it was not possible to systematically verify the translated terminology.' (p.5)
- [Q64] 'Nearly 10% of the labels were false.' (p.5)
- [Q120] 'models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices.' (p.10)
- [Q121] 'We therefore caution against using benchmark performance as evidence of cultural or demographic coverage.' (p.10)

</details>

**Information gaps:**
- Annotator demographics, professional background, civil-administration experience
- Whether sentiment label boundaries were validated against civil-correspondence-specific examples
- Granular agreement statistics by class (e.g., neutral vs. negative) to assess understated-frustration handling

**Requires expert verification:**
- Civil-servant review of a held-out sample of sentiment labels for civil-correspondence relevance
- Re-annotation of a small evaluation set by administrative-domain annotators to estimate convergent validity

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Output form is text-classification labels evaluated by macro-F1 with results averaged over three runs and standard deviations reported [Q93, Q96]. This is a standard, well-documented evaluation methodology and matches the deployment's text-to-label format at surface level. However, the deployment requires confidence scores for routing thresholds and multi-label outputs for messages spanning multiple departments [elicitation Q4]. LTZGLUE reports only macro-F1 with no calibration metrics (e.g., ECE, Brier score), no per-class precision/recall thresholds, and no multi-label evaluation methodology. Invalid LLM outputs are simply discarded [Q90, Q91], which masks the operational reality that malformed outputs in deployment must be handled (escalated). OF is MODERATE priority. The form is text-to-text-label as required, but the metric set and label cardinality do not match the deployment's operational form.

**Strengths:**
- Text-output modality matches deployment [Q93]
- Multi-run evaluation with standard deviations reported for encoder models [Q89, Q96] supports meaningful comparison
- Hyperparameter search via Bayesian optimization with early stopping is methodologically sound [Q136, Q138]
- Class-balanced loss for imbalanced tasks [Q92] is a conscientious design choice

**Checklist:**

- **OF-1**: Text output matches deployment, but the deployment additionally requires confidence scores and multi-label outputs [elicitation Q4], which the benchmark's macro-F1 single-label evaluation does not assess. — _Sources: Q93, Q96_
- **OF-2**: Not applicable — deployment is text-only [regional context infrastructure_notes.deployment_modality], and benchmark is text-only [Q93]. — _Sources: Q93_
- **OF-3**: Civil servants are professionally literate [regional context target_population.civil_servant_profile]; literacy is not a constraint. Citizens have 99.0% internet penetration [WEB-7]. No accessibility-driven output modality concerns. — _Sources: WEB-7_
- **OF-4**: External-validity gap: macro-F1 alone cannot validate the calibration and multi-label behaviors required for routing escalation logic; invalid outputs being discarded [Q90, Q91] hides a deployment-relevant failure mode. — _Sources: Q90, Q96_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q90] 'Prompted LLMs do not always produce well-formed outputs and may return an incorrect number of predictions for a given task; such outputs are discarded prior to evaluation.' (p.7)
- [Q93] 'Table 6 shows F1 scores for all models across all tasks' (p.7)
- [Q96] 'Encoder results are averaged over three runs with standard deviations as subscripts. Prompted LLMs were evaluated once; we report macro-F1 only.' (p.8)
- [Q92] 'when fine-tuning on these tasks we use class-balanced loss based on effective size (Cui et al., 2019) with a beta of 0.99.' (p.7)

*Web sources:*
- [WEB-7] 99.0% internet penetration — confirms text-output channel is universally accessible

</details>

**Information gaps:**
- No calibration metrics (ECE, reliability diagrams) reported
- No multi-label evaluation methodology defined
- No analysis of malformed-output rate as an operational signal

**Requires expert verification:**
- Specification of operational confidence thresholds and escalation-rate targets by deployment owners

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** All tasks emit single hard labels with narrow non-administrative taxonomies; no confidence scores, no multi-label outputs, no urgency scale, no language-of-input output

**Recommendation:** Define a deployment-specific output schema with multi-label routing categories, calibrated confidence scores tied to escalation thresholds, an urgency scale validated against civil-servant judgments, and a language-of-input field to satisfy the 1984 language law obligation [WEB-14].

### Input Ontology ⚠

**Gap:** No Luxembourg-administrative topic or intent taxonomy, no state-vs-communal routing axis, no multi-label formulation

**Recommendation:** Co-design an administrative topic taxonomy with national and communal civil servants covering at minimum: cross-border worker matters, housing/cost-of-living, transport, tax, social security, residency, communal services, EU institutional. Include a state-vs-communal routing dimension and a multi-label structure aligned with the deployment's actual case types.

### Input Content ⚠

**Gap:** Benchmark inputs are dominated by formal/institutional registers and filter out non-Luxembourgish text; code-switching and orthographic variation are under-represented

**Recommendation:** Construct an internal evaluation corpus from anonymized real citizen correspondence (with CNPD-compliant DPIA) that explicitly preserves French/German code-switching, frontalier terminology, and orthographic variation. Use it as an out-of-distribution stress test alongside LTZGLUE.

### Output Content ⚠

**Gap:** Sentiment annotators lack documented administrative-register expertise; κ=0.45 is moderate; LLM-assisted labeling introduces uncertainty in RTE and JUDGEWEL

**Recommendation:** Re-annotate a calibration sample of sentiment and any new routing categories with civil servants or administration-experienced annotators; report per-class agreement and disagreement patterns; use the deployment's human-in-the-loop feedback to drive ongoing label refinement.

### Input Form

**Gap:** Length filter (40–400 words) and language-purity filter (OpenLID) exclude tail-distribution inputs the deployment will face

**Recommendation:** Construct a supplementary evaluation slice without length and language-purity filters to characterize model behavior on very short, very long, and multilingual inputs; report performance separately on these slices.

### Output Form

**Gap:** Macro-F1 only; no calibration metrics; invalid outputs are silently discarded; no multi-label evaluation

**Recommendation:** Add calibration metrics (ECE, reliability diagrams), multi-label metrics (micro/macro-F1, hamming loss, subset accuracy), and treat malformed-output rate as an explicit deployment KPI rather than discarding such cases.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This paper presents LTZGLUE, the first Natural Language Understanding (NLU) benchmark for Luxembourgish (LTZ) based on the popular GLUE benchmark for English." |
| Q2 | 1 | input_ontology | "Our tasks include common natural language processing tasks in binary and multi-class classification settings, including named entity recognition, topic classification, and intent classification." |
| Q3 | 1 | output_form | "We evaluate various pre-trained language models for LTZ to present an overview of the current capabilities of these models on the LTZ language." |
| Q4 | 1 | input_ontology | "Small and under-researched languages are particularly difficult to evaluate, as is the case with Luxembourgish (LTZ), the national language of Luxembourg, with around 400k speakers." |
| Q5 | 1 | input_content | "LTZ only has a handful of NLU tasks available (Lothritz et al., 2022; Philippy et al., 2024; Plum et al., 2026)." |
| Q6 | 1 | input_content | "As most of these are in the news domain, and the majority of the down-stream tasks comprise less than a thousand instances, model evaluation is not always dependable." |
| Q7 | 1 | input_form | "Additional factors, such as the ongoing standardisation of the language (Gilles, 2019), vast amounts of variation (Lutgen et al., 2025), and decentralised resources, make it extremely challenging to evaluate LTZ language understanding in language models." |
| Q8 | 1 | input_ontology | "Our contributions are: (1) LTZGLUE: the first unified GLUE benchmark for LTZ, with 8 tasks." |
| Q9 | 1 | input_ontology | "(2) LTZ-E1 (mini/base): 2 new encoder language models for LTZ, which achieve competitive performance when fine-tuned on LTZGLUE." |
| Q10 | 1 | output_content | "Alistair Plum1, Felicia Körner2,3, Anne-Marie Lutgen1, Laura Bernardy1, Fred Philippy1, Emilia Milano1, Nils Rehlinger1, Cédric Lothritz4, Tharindu Ranasinghe5, Barbara Plank2,3, Christoph Purschke1 1University of Luxembourg, Luxembourg, 2LMU Munich, Germany 3Munich Center for Machine Learning, Germany 4LIST, Luxembourg, 5Lancaster University, UK" |
| Q11 | 2 | input_ontology | "In this section, we introduce the eight tasks for LTZGLUE. The set spans binary and multi-class sentence and token-level classification tasks. Together, these tasks cover a broad spectrum of linguistic and semantic phenomena and provide the first unified benchmark for evaluating LTZ NLP models." |
| Q12 | 2 | input_content | "Unless stated otherwise, the textual data used across most tasks stems from two main sources: (i)" |
| Q13 | 2 | input_content | "LTZ, the focus of this benchmark, is regarded as under-researched, and research is ongoing. Joshi et al. (2020) classify Luxembourgish as one of the "scraping-by" languages: although some unlabeled data exists, meaningful progress will require coordinated efforts to raise awareness and collect labeled datasets, as such resources are currently almost nonexistent." |
| Q14 | 2 | input_ontology | "Yet progress remains uneven across tasks, and existing resources vary widely in size, domain, and annotation quality. No unified benchmark currently exists to evaluate LTZ language understanding consistently, a gap we aim to fill." |
| Q15 | 3 | input_ontology | "We formulate headline acceptability (HA) as a binary classification task where the model must decide whether a given headline matches the accompanying article body." |
| Q16 | 3 | input_content | "To construct this dataset, we use RTL news articles. We keep only documents from the twenty most frequent categories. We then filter articles by body length and title length, remove exact duplicate titles, randomly shuffle the remaining instances, and retain a fixed subset of 30k examples." |
| Q17 | 3 | input_form | "This subset is split equally, with one half serving as the positive class with original headlines, and the other half providing the article bodies for which we assign swapped headlines." |
| Q18 | 3 | input_form | "We compute TF–IDF representations of the article texts using unigrams and bigrams, an LTZ stopword list, a minimum document frequency of two, and a large feature cap to preserve topical detail." |
| Q19 | 3 | input_form | "For every article body in the negative half, we search its nearest neighbours to identify a donor headline, with a minimum 30-day distance so that we avoid headlines tied to the same event." |
| Q20 | 3 | input_form | "To prevent trivial matches, we reject candidates whose headlines show high positional similarity, measured as the fraction of identical tokens in aligned positions (threshold 0.25)." |
| Q21 | 3 | input_form | "We store original and swapped titles, reshuffle, and split into train (20k), development (3k), and test (6k) sets." |
| Q22 | 3 | input_form | "The resulting negative examples remain topically related but are temporally and structurally mismatched, forcing models to attend to article content rather than surface cues." |
| Q23 | 3 | input_ontology | "We formulate the sentiment analysis (SA) task as a classification task where the model has to predict positive, negative, and neutral sentiment." |
| Q24 | 3 | input_content | "We use articles from RTL, randomly selected from the commentary and letter to the editor sections." |
| Q25 | 3 | output_content | "In total, we extract 4,583 sentences, which are then annotated by two native speakers of LTZ." |
| Q26 | 3 | output_content | "Annotators are instructed to label each sentence, and to use unsure only when they would otherwise randomly use the other labels." |
| Q27 | 3 | output_content | "We calculated Cohen's Kappa at 0.45." |
| Q28 | 3 | output_content | "For the final set, the annotators agree on a label in cases of label disagreement." |
| Q29 | 3 | input_ontology | "We introduce a linguistic acceptability dataset consisting of four distinct linguistic subtypes, which can either be used as a binary (LA (BINARY)) or multiclass (LA (MULTI)) classification dataset." |
| Q30 | 3 | input_content | "The sentences are derived from the Luxembourgish Online Dictionary (LOD) and are manipulated using the tags available in the dataset." |
| Q31 | 3 | output_ontology | "The first class interferes with the subject-verb agreement by changing the conjugated form of the main verb or auxiliary verb. The second class similarly modifies the declined form of the adjective and therefore violates the agreement in case, number, and gender. For the third class, we manipulate the syntax by deleting 2-3 random words from the sentence, depending on the length. The last class impacts the orthography, which is achieved by using data provided by Spellchecker.lu, a semiautomatic spellchecking website frequently used in Luxembourg. We changed one random word in the sentence by using the least frequent variant in the spellchecker data." |
| Q32 | 4 | input_form | "The multiclass dataset and binary dataset have a 70-10-20 split, and the distribution is shown in Table 2." |
| Q33 | 4 | output_ontology | "The binary dataset distinguishes between correct (1) and incorrect (0), for which the label 0 encompasses the categories Verb, Adj, Syntax and Ortho." |
| Q34 | 4 | input_content | "The JUDGEWEL dataset (Plum et al., 2026) introduces an automatically constructed corpus for named entity recognition (NER) in LTZ, derived from Wikipedia and Wikidata." |
| Q35 | 4 | input_form | "Using Wikipedia's hyperlink structure, entities are matched to their corresponding Wikidata types and labelled in BIO format." |
| Q36 | 4 | input_form | "Candidate sentences are selected to maximise diversity, and a set of quality heuristics filters incomplete or overlapping entities." |
| Q37 | 4 | output_content | "The resulting sentences are then evaluated using LLMs acting as judges, with minimal human verification to calibrate quality thresholds." |
| Q38 | 4 | input_content | "The final dataset contains roughly 27k sentences across five entity types (see Table 3)." |
| Q39 | 4 | output_content | "Models trained on JUDGEWEL achieve performance comparable to human-annotated data, demonstrating that automatically constructed resources can provide effective supervision." |
| Q40 | 4 | input_content | "The NER dataset introduced by Lothritz et al. (2022), by contrast, is a fully human-annotated corpus derived from RTL online news comments." |
| Q41 | 4 | input_content | "It covers a wider range of text types and registers, including informal and code-mixed writing, and focuses on four primary entity categories (PER, ORG, LOC, GPE)." |
| Q42 | 4 | output_content | "Annotation was conducted manually, yielding a smaller but high-precision dataset." |
| Q43 | 4 | input_form | "The two datasets are merged to increase both coverage and domain balance." |
| Q44 | 4 | output_ontology | "To ensure compatibility, the tag set is harmonised by merging the GPE and LOC categories into a single location label, while retaining PER, ORG, and MISC unchanged." |
| Q45 | 4 | input_content | "This unified resource thus aligns the structured reliability of JUDGEWEL with the domain and stylistic breadth of the NER set by (Lothritz et al., 2022), providing a large-scale, multi-domain NER dataset for LTZ." |
| Q46 | 4 | input_content | "To construct the news topic classification (TC) dataset, we collected news articles from RTL, which provides content pre-assigned to editorial categories." |
| Q47 | 4 | input_form | "We applied a series of preprocessing steps to ensure data quality. Specifically, we removed articles identified as non-Luxembourgish by OpenLID (Burchell et al., 2023), as well as those containing fewer than 40 words or more than 400 words." |
| Q48 | 4 | output_ontology | "From the available categories, we focused on five principal domains: SPORTS, CULTURE, TECHNOLOGY, BUSINESS, and ANIMALS." |
| Q49 | 4 | input_form | "Given the substantial over-representation of the SPORTS category, we performed downsampling to mitigate class imbalance." |
| Q50 | 4 | input_form | "The resulting dataset was split into training, development, and test sets (category distribution is summarized in Table 4)." |
| Q51 | 4 | input_content | "We constructed a new LTZ dataset for intent detection (ID) by translating the English xSID test and validation datasets (van der Goot et al., 2021)." |
| Q52 | 4 | output_content | "The translations were performed by an LTZ native speaker. In cases of uncertainty, additional native LTZ speakers were consulted." |
| Q53 | 4 | input_form | "Since LTZ is linguistically closely related to German, the German" |
| Q54 | 5 | input_content | "Since this task is originally intended to be crosslingual, we use the machine translated German training set (van der Goot et al., 2021)." |
| Q55 | 5 | input_content | "The main challenge in translating the English dataset stems from its register. The source segments consist of user commands for a voice-controlled AI assistant, representing a specialised spoken register for which there is no equivalent reference corpus in LTZ. This register is marked by domain-specific terminology and collocations (e.g., set an alarm, set a reminder, add to playlist), as well as non-standard spelling (e.g., all lowercase, missing punctuation)." |
| Q56 | 5 | input_content | "Due to the lack of LTZ references in this register, it was not possible to systematically verify the translated terminology." |
| Q57 | 5 | output_form | "After translating the dataset, we transferred the BIO tags by first using token-level fuzzy matching between the LTZ and the German dataset, followed by manual verification." |
| Q58 | 5 | output_ontology | "Table 5 shows the label distribution and size of each data split." |
| Q59 | 5 | input_ontology | "Recognizing Textual Entailment (RTE) (Haim et al., 2006) is a classic NLU task featured in the original GLUE benchmark. Given a pair of texts A and B, the task consists of determining whether A is a logical premise of B." |
| Q60 | 5 | input_content | "Lothritz et al. (2023) released a machine-translated Luxembourgish version of the dataset using Google Translate. However, due to numerous grammar and vocabulary related mistakes introduced in this process, we set out to improve the quality of the dataset." |
| Q61 | 5 | input_form | "Specifically, we first prompted CHATGPT-5.1 to assess and improve the translated sentence pairs unless they were already of very high quality, while explicitly keeping the original meaning to avoid label conflicts (see Appendix 7.4)." |
| Q62 | 5 | output_content | "In addition, we perform two verification steps to make sure that (a) the quality of the improved texts is high enough and (b) that the labels are correct." |
| Q63 | 5 | output_content | "To achieve (a), we prompted CHATGPT-5-MINI to judge the texts in the improved data and label their quality as either low, medium, or high, keeping only data rated at least medium, removing nearly 25% of the entire dataset (see Appendix 7.5)." |
| Q64 | 5 | output_content | "For (b), we prompted CHATGPT-5-MINI to verify whether the dataset labels remained correct after the first translation and improvement, outputting true or false for each sentence pair (see Appendix 7.6). Nearly 10% of the labels were false." |
| Q65 | 5 | output_content | "We found that the quality improvement step often corrected intentional logical contradictions or factual inaccuracies rather than keeping the original semantics. We therefore adjusted the sentences manually such that they corresponded to the ground truth again, while keeping false positives intact." |
| Q66 | 5 | input_content | "The filtering reduced between 22 and 28% of instances in the data, resulting in a final dataset of 1,876, 197, and 626 sentence pairs for the training, development, and test set, respectively." |
| Q67 | 5 | input_ontology | "Together, the eight tasks in LTZGLUE form a broad and balanced evaluation suite, covering four binary and four multi-class settings, sentence- and document-level inputs, as well as a token-level sequence-labelling task." |
| Q68 | 5 | input_ontology | "Despite the low-research status of LTZ, this places LTZGLUE in the same general range as the original English GLUE benchmark, which comprises nine diverse NLU tasks (Wang et al., 2019b)." |
| Q69 | 5 | input_ontology | "In addition, a substantial proportion of the LTZGLUE tasks are newly created for LTZ rather than direct translations or simple repackaging, allowing the benchmark to reflect phenomena and usage patterns specific to the language." |
| Q70 | 6 | input_ontology | "In this landscape, supporting eight tasks for LTZ, including token-level NER and several newly constructed text-level tasks, is a strong indicator of the maturity and breadth of the emerging LTZ NLP ecosystem." |
| Q71 | 6 | input_ontology | "This design allows us to assess current LTZ NLU performance across fundamentally different modelling paradigms, while maintaining a clear separation between task-specific supervision and general-purpose language understanding." |
| Q72 | 6 | input_form | "We train two encoder language models for LTZ: LTZ-E1-mini with 68M and LTZ-E1-base with 110M non-embedding parameters." |
| Q73 | 6 | input_form | "We closely follow the Ettin recipe (Weller et al., 2026), which is based on MODERNBERT (Warner et al., 2025)." |
| Q74 | 6 | input_content | "The pre-training set is compiled from a variety of sources of LTZ. A large portion of the data stems from RTL (see Section 3), including news articles (News), transcribed radio interviews (Radio), and user comments (Comments). We also include transcribed podcasts (Podcasts) and transcribed political speeches and debates from the Chambre des Députés (Chamber). In addition, we use 1M sentences from the web crawl of the Leipzig Collection (Web, this excludes RTL), text crawled from LTZ chat rooms (Webchat), a Wikipedia crawl from October 2023 (Wikipedia), and finally, example sentences from the LOD retrieved in March 2024." |
| Q75 | 6 | input_form | "We filter out sentences containing fewer than three words (as tokenized by whitespace), totalling 11.7M sentences, which corresponds to roughly 233M tokens using our tokenizer." |
| Q76 | 6 | output_form | "We evaluate a set of supervised encoder-based models that explicitly support LTZ, either through direct pre-training or multilingual coverage." |
| Q77 | 6 | output_form | "As a representative baseline, we include multilingual BERT (MBERT-base) (Devlin et al., 2019), which still remains widely used for multilingual transfer and low-resource evaluation." |
| Q78 | 6 | output_form | "We additionally evaluate a more recent multilingual BERT (MMBERT-base) variant with updated pre-training data and tokenisation." |
| Q79 | 6 | output_form | "To complement these general-purpose multilingual models, we include LUXEMBERT, a language-specific model trained on LTZ data (Lothritz et al., 2022), which provides a stronger inductive bias for the language's lexical and orthographic properties." |
| Q80 | 6 | output_form | "Finally, we evaluate XLM-RoBERTa (XLM-R-base) (Conneau et al., 2020), a large-scale multilingual model trained on substantially more data and languages than MBERT-base, and commonly used as a strong reference point for multilingual NLU." |
| Q81 | 6 | output_form | "In addition to supervised encoder-based models, we evaluate a set of LLMs in a prompt-based zero-shot setting. This group includes QWEN3-235B, LLAMA-3.3, GEMMA-3-27B, and GPT5-MINI, which represent a range of model sizes, training regimes, and degrees of multilingual coverage." |
| Q82 | 6 | input_content | "None of these models are fine-tuned on LTZGLUE, although some of the text data (RTL, Wikipedia) is very likely to have been processed during training." |
| Q83 | 6 | output_form | "The models are evaluated using prompts that describe each task, allowing us to assess their ability to generalise to LTZ without task-specific supervision." |
| Q84 | 6 | output_form | "We did not use a Multiple Choice Question Answering (MCQA)-setup, but provided the labels that should be used as output." |
| Q85 | 6 | output_form | "This evaluation setting reflects the growing use of LLMs as general-purpose language understanding systems, particularly in scenarios where annotated data is scarce or unavailable." |
| Q86 | 6 | output_form | "However, prompt-based evaluation introduces additional sources of variability, including prompt sensitivity and differences in instruction-following behaviour across models. As a result, performance should be interpreted as indicative rather than directly comparable to supervised results." |
| Q87 | 6 | output_form | "Nevertheless, including these models provides a complementary perspective on the current capabilities of large-scale multilingual and instruction-tuned systems for LTZ NLU." |
| Q88 | 7 | output_form | "We evaluate the models described in Section 4 across all tasks in the benchmark." |
| Q89 | 7 | output_form | "For encoder-based models, results are reported as averages over multiple runs (see Appendix 7.2 for more details)." |
| Q90 | 7 | output_form | "Prompted LLMs do not always produce well-formed outputs and may return an incorrect number of predictions for a given task; such outputs are discarded prior to evaluation." |
| Q91 | 7 | output_form | "All reported scores are computed on the remaining valid predictions per model." |
| Q92 | 7 | output_form | "For the supervised models, since the linguistic acceptability and sentiment analysis datasets are highly imbalanced, when fine-tuning on these tasks we use class-balanced loss based on effective size (Cui et al., 2019) with a beta of 0.99." |
| Q93 | 7 | output_form | "Table 6 shows F1 scores for all models across all tasks (see Appendix 7.9 for full results)." |
| Q94 | 7 | output_form | "Encoder-based models perform strongly across most settings, particularly on structurally complex and label-sensitive tasks, confirming findings from prior work on multilingual and low-resource NLU (Wu and Dredze, 2019; Conneau et al., 2020)." |
| Q95 | 7 | output_form | "Prompted large language models, by contrast, show more variable behaviour and perform competitively only on a set of semantically coarse-grained tasks, consistent with recent observations that prompting alone is often insufficient for strong performance on structured NLU tasks (Wei et al., 2022; Liu et al., 2023)." |
| Q96 | 8 | output_form | "Table 6: Test F1 scores across all ltzGLUE tasks. Encoder results are averaged over three runs with standard deviations as subscripts. Prompted LLMs were evaluated once; we report macro-F1 only." |
| Q97 | 8 | output_form | "MMBERT-base achieves the highest score with very low variance, indicating both high accuracy and stability." |
| Q98 | 8 | output_form | "In contrast, prompted LLMs perform substantially worse than all fine-tuned encoders." |
| Q99 | 8 | input_ontology | "The topic classification task emerges as the easiest overall. All encoder models achieve very high F1 scores with extremely low variance, indicating a stable and largely language-agnostic task." |
| Q100 | 8 | output_form | "Prompted LLMs perform competitively in this setting: GPT and QWEN approach encoder-level performance in a single run." |
| Q101 | 8 | output_form | "Results on the intent detection task reveal a clear separation between models. Among the encoders, LUXEMBERT achieves the strongest performance with very low variance, highlighting the benefit of language-specific pre-training." |
| Q102 | 8 | output_form | "Prompted LLMs struggle substantially with this task: all LLMs achieve low F1 scores, with GEMMA performing particularly poorly. This suggests that intent classification in LTZ relies on supervised task-specific training." |
| Q103 | 8 | input_ontology | "The recognising textual entailment task is the most challenging overall, with low F1 scores and high variance across encoder models." |
| Q104 | 8 | output_form | "Prompted LLMs perform relatively well in comparison to most encoders: GPT and QWEN achieve strong single-run F1 scores, exceeding all encoder models except MMBERT-base." |
| Q105 | 8 | output_form | "First, MMBERT-base consistently achieves the strongest or near-strongest performance across almost all tasks, combining high mean F1 scores with comparatively low variance, suggesting that broad multilingual pre-training with sufficient LTZ exposure yields stable and transferable representations." |
| Q106 | 8 | output_form | "Second, LTZ-specific encoders such as LUXEMBERT and LTZ-E1-mini are particularly competitive on lexically grounded or task-specific settings (e.g., intent detection and acceptability), but exhibit greater instability on structurally complex inference tasks such as multi-class acceptability and textual entailment." |
| Q107 | 8 | output_form | "Third, prompted LLMs display substantially more task-dependent behaviour and generally underperform fine-tuned encoders, except on semantically coarse-" |
| Q108 | 9 | input_ontology | "This paper makes two central contributions to LTZ NLU. First, we introduce a new benchmark that provides the first comprehensive GLUE-style evaluation suite for LTZ. Second, we present a systematic evaluation of encoder-based models and prompted large language models across all tasks, offering concrete guidance on model choice in such a low-resource setting." |
| Q109 | 9 | input_content | "The construction of the dataset required a deliberately resource-conscious approach. In the absence of large, task-diverse annotated resources, we combine the reuse of existing datasets with the targeted annotation of new data, carefully aligning annotation schemes across tasks, and using large language models as auxiliary tools." |
| Q110 | 9 | input_content | "While LTZGLUE provides the first systematic benchmark for LTZ NLU, the dataset remains constrained by the availability and scope of existing resources. Several tasks rely on relatively small or domain-specific corpora, which limits the ecological validity of the results and restricts the range of linguistic phenomena covered." |
| Q111 | 9 | input_content | "In addition, some of the data sources used in this benchmark may already be included, in whole or in part, in the pre-training corpora of the large language models evaluated in this work. While the exact composition of proprietary pre-training datasets is typically not fully disclosed, this potential overlap cannot be entirely ruled out and may inflate performance estimates." |
| Q112 | 9 | input_content | "Coverage across domains, registers, and demographic varieties may also be limited. LTZ displays substantial orthographic and sociolinguistic variation, yet most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts." |
| Q113 | 9 | output_content | "Although we draw on established GLUE-style tasks, some annotation decisions and class distributions are necessarily influenced by resource constraints. Certain tasks exhibit label imbalance or rely on automatic preprocessing, which may introduce biases that we cannot fully quantify." |
| Q114 | 9 | output_content | "We would like to thank the student assistants for their annotation work." |
| Q115 | 9 | output_content | "This work is supported by the LLMs4EU project, funded by the European Union through the Digital Europe Programme (DIGITAL) under the grant agreement 10119847. FK and BP are supported by the ERC Consolidator Grant DIALECT 101043235." |
| Q116 | 9 | input_form | "The datasets included in this work are derived from publicly accessible sources that permit research use, and all preprocessing avoids the inclusion of directly identifying personal information." |
| Q117 | 10 | output_content | "However, some tasks draw on data originally produced in institutional or media contexts, which may reflect societal biases in representation." |
| Q118 | 10 | output_content | "These patterns can influence model behaviour and should be considered when deploying systems trained on LTZGLUE." |
| Q119 | 10 | input_content | "LTZ is a small language community, and linguistic data often originate from a limited set of public domains." |
| Q120 | 10 | output_content | "As a result, models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices." |
| Q121 | 10 | output_content | "We therefore caution against using benchmark performance as evidence of cultural or demographic coverage." |
| Q122 | 10 | input_content | "Finally, although no sensitive content is intentionally included, automated filtering and preprocessing cannot guarantee the complete removal of harmful or offensive material." |
| Q123 | 10 | output_content | "Researchers using LTZGLUE are encouraged to inspect task-specific subsets and consider downstream implications, especially in public-facing settings." |
| Q124 | 12 | input_ontology | "For demonstration purposes, we present an example for each task in ltzGLUE in Table 7. The examples are intended to illustrate the task formulations and typical model inputs and outputs." |
| Q125 | 12 | input_form | "We follow the Ettin recipe (Weller et al., 2026), based on ModernBERT (Warner et al., 2025), for training hyperpameters and model architecture." |
| Q126 | 12 | input_form | "We train two sizes of LTZ-E1 models, mini and base, with 68M and 110M non-embedding parameters, respectively." |
| Q127 | 12 | input_form | "LTZ-E1-mini has 19 hidden layers, a hidden size of 512, an intermediate size of 768, and 8 attention heads, whereas LTZ-E1-base has 22 hidden layers, a hidden size of 768, an intermediate size of 1152, and 12 attention heads." |
| Q128 | 12 | input_form | "Both models share a GPTNeoXTokenizerFast tokenizer (Black et al., 2022), a BPE-based tokenizer, which we train on the entire pre-training set, using a minimum frequency of two and a vocabulary size of 50,368." |
| Q129 | 12 | input_form | "We use a constant batch size of 1024 packed sequences, where both models have a max sequence length of 1024." |
| Q130 | 12 | input_form | "We follow ModernBERT (Warner et al., 2025) and Ettin (Weller et al., 2026) in using the Warmup-Stable-Decay (WSD) scheduler (Zhai et al., 2022; Hu et al., 2024), though we use a shorter warmup and decay phase of 500 batches each, due to our smaller pre-training dataset size and larger number of epochs (10 vs. one)." |
| Q131 | 12 | input_form | "Again following ModernBERT and Ettin's recipe, we use the StableAdamW optimizer (Wortsman et al., 2023), with a peak learning rate of 3e-3 with a weight decay of 3e-4 for LTZ-E1-mini and 8e-4 with a weight decay of 1e-5 for LTZ-E1-base." |
| Q132 | 12 | input_content | "As our pre-training set is small, we" |
| Q133 | 13 | output_form | "We use a 20GB MIG partition of an NVIDIA A100-SXM4-80GB to pretrain each model, taking 47 hours for LTZ-E1-mini and 76 hours for LTZ-E1-base." |
| Q134 | 13 | output_form | "However, we note that compute times were negatively impacted by concurrent jobs on the server cluster with suboptimal CPU thread management." |
| Q135 | 13 | input_content | "We show pre-training data token counts per source in Table 9, where sources (described in Section 4.1) are: RTL news articles (News), RTL transcribed radio interviews (Radio), RTL user comments (Comments), transcribed podcasts (Podcasts), transcribed political speeches and debates from the Chambre des Députés (Chamber), 1M sentences from the web crawl of the Leipzig Collection (Web), text from Luxembourgish chat rooms (Webchat), a Wikipedia crawl (Wikipedia), and examples from the Luxembourgish Online Dictionary (LOD)." |
| Q136 | 13 | output_form | "Though we do not aim to optimise performance in our evaluation, we conduct basic hyperparameter sweeps for each model and task combination in order to provide a fairer comparison across models." |
| Q137 | 13 | output_form | "For each model and task combination, we select the best hyperparameters based on the validation set, and use those parameters to finetune two additional models with differing seeds, resulting in three runs." |
| Q138 | 13 | output_form | "In order to reduce the computational demand of the sweeps, we use Bayesian search with early stopping after three iterations, and cap each sweep at 30 runs, for 1,440 total runs across all models and tasks (and an additional 96 to finetune the two additional seeds)." |
| Q139 | 13 | output_form | "However, we note again that these ranges were kept simple to keep sweeps computationally feasible, thus, these values should not be seen as optimal hyperparameters." |
| Q140 | 14 | output_form | "We use several 20GB MIG partitions of NVIDIA A100-SXM4-80GB GPUs to conduct the sweeps. Depending on model and task dataset size, multiple runs were conducted in parallel on each partition, totalling 59 days of compute, which includes fine-tuning the additional seeds, as well as evaluation on the validation and test sets." |
| Q141 | 14 | input_content | "Table 9: Token counts (M) per source for pretraining data of LTZ-E1." |
| Q142 | 14 | output_form | "Table 10: Hyperparameter sweep ranges used for all task and model combinations." |
| Q143 | 14 | output_content | "You are an expert for the Luxembourgish language. I am giving you a sentence in Luxembourgish. You have to judge its quality and improve it while keeping the meaning intact. As output, write only the improved sentence or the original sentence if it is of very high quality." |
| Q144 | 14 | output_content | "You are an expert for the Luxembourgish language. I am giving you two texts in Luxembourgish. You have to judge their quality. As output, simply write 'low', 'medium' or 'high' depending on the quality of both sentences, nothing else." |
| Q145 | 14 | output_content | "You are an expert for the Luxembourgish language. I am giving you two texts TEXT1 and TEXT2 in Luxembourgish as well as a LABEL where 1 means that TEXT1 logically entails TEXT2 while 0 means the opposite. You have to check if the labels are correct. As output, simply write 'true' if the label is the correct one or 'false' if the label is incorrect." |
| Q146 | 14 | output_form | "You are a classification and text-processing model specialized in NLP tasks for Luxembourgish (lb). Follow ALL rules strictly: 1. Respond ONLY in valid JSON. 2. Do NOT add explanations, comments or text outside of JSON. 3. Use field: "output": <model_answer>. 4. Use field: "task": "<task_name>". 5. Use field: "input": "<input example text>". 6. Predict only the requested outputs and" |
| Q147 | 15 | output_ontology | "If determined labels are 0 and 1 then 0 is used for False, 1 is used for True." |
| Q148 | 15 | input_ontology | "headline_classification: Decide if the given title/headline fits the text. Output True or False." |
| Q149 | 15 | output_ontology | "sentiment_analysis: Classify sentiment of the text. Allowed labels: positive, neutral, negative." |
| Q150 | 15 | input_ontology | "linguistic_acceptability_binary: Decide whether the sentence is linguistically acceptable in Luxembourgish. Output: 0 or 1." |
| Q151 | 15 | output_ontology | "linguistic_acceptability_multilabel: Detect if the sentence is correct or if some element is wrong. If the sentence is correct, Output: correct. If it is not, Output the label referencing the wrong element: syntax, verb, ortho or adj." |
| Q152 | 15 | output_ontology | "ner: Perform Named Entity Recognition on the given sequence of sentence tokens. Output tags as lists of ner_tags. Allowed Tags: O, B-LOC, I-LOC, B-PER,I-PER, B-DATE, I-DATE,B-ORG, I-ORG, B-MISC, I-MISC." |
| Q153 | 15 | output_ontology | "topic_classification: Classify topic of the document by title and text. Allowed category_names: sports, animals, business, culture, technology." |
| Q154 | 15 | output_ontology | "slot_intent_detection: Detect the intent for the text given. Allowed intents: reminder/show_reminders, weather/find, reminder/set_reminder, reminder/cancel_reminder, alarm/snooze_alarm, alarm/show_alarms, alarm/set_alarm, nalarm/cancel_alarm, nalarm/time_left_on_alarm." |
| Q155 | 15 | output_ontology | "recognizing_textual_entailment: Determine if the information in the second sentence is entailed in the first one. Output: 0 or 1." |
| Q156 | 15 | output_form | "We show full results (validation and test set performance) for each model and task for HA, SA, LA (BINARY), and LA (MULTI) in Table 12 and for NER, TC, ID, and RTE in Table 13." |
| Q157 | 16 | output_form | "Table 11: Best hyperparameters per model for each task." |
| Q158 | 17 | output_form | "Dev and Test F1 scores for Headline Acceptability (HA), Sentiment Analysis (SA) and Linguistic Acceptability (Binary LAB and Multi LAM. Results are averaged over three runs, with standard deviations as subscripts." |
| Q159 | 17 | output_form | "Dev and Test F1 scores for Named Entity Recognition (NER), Topic Classification (TC), Intent Detection (ID) and Textual Entailment (RTE). Results are averaged over three runs, with standard deviations as subscripts." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://statistiques.public.lu/en/publications/series/regards/2025/regards-01-25.html |
| WEB-2 | https://www.oecd.org/en/publications/2025/04/oecd-economic-surveys-luxembourg-2025_3eb782b5/full-report/reviving-productivity-growth_4509ab88.html |
| WEB-3 | https://gouvernement.lu/fr/actualites/toutes_actualites.gouv2024_mcult+fr+actualites+mes-actualites+2024+fevrier+sproochegesetz-40-joer.html |
| WEB-4 | https://statistiques.public.lu/fr/publications/series/en-chiffres/2024/demographie-lux-en-chiffres-2024.html |
| WEB-5 | https://en.paperjam.lu/article/growth-in-number-of-cross-bord |
| WEB-6 | https://media.alleyesonme.jobs/en/article-titles/le-luxembourg-attire-t-il-toujours-les-frontaliers |
| WEB-7 | https://datareportal.com/reports/digital-2024-luxembourg |
| WEB-8 | https://www.statista.com/statistics/377741/household-internet-access-in-luxembourg/ |
| WEB-9 | https://www.luther-lawfirm.com/fileadmin/user_upload/Luxembourg_-_Data_Protection_Overview___Guidance_Note___DataGuidance.pdf |
| WEB-10 | https://cnpd.public.lu/en.html |
| WEB-11 | https://cnpd.public.lu/en/actualites/national/2024/09/rapport-annuel-2023.html |
| WEB-12 | https://artificialintelligenceact.eu/annex/3/ |
| WEB-13 | https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act |
| WEB-14 | https://data.legilux.public.lu/filestore/eli/etat/leg/loi/1984/02/24/n1/jo/fr/html/eli-etat-leg-loi-1984-02-24-n1-jo-fr-html.html |
| WEB-15 | https://guichet.public.lu/fr/citoyens/justice/voies-recours-reglement-litiges/frais-avocat-justice/langues-tribunaux.html |
| WEB-16 | https://statistiques.public.lu/en/actualites/2025/stn20-25-emploi-salarie.html |

---

