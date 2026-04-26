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
| Output Form ✓ | 2 | Significant gaps | high |
| **Average** | **2.0** | | |

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

LTZGLUE is the first unified LTZ NLU benchmark and a meaningful contribution to a 'scraping-by' language ecosystem [Q13], but its fitness for the Luxembourg civil-servant correspondence-routing deployment is poor across the dimensions weighted HIGH in elicitation (IO, IC, OO, OC). The taxonomy gaps are categorical: zero administrative topic categories, zero state-vs-communal jurisdiction split, zero frontalier-specific classes, no housing or cost-of-living categories, and a generic 3-class sentiment scheme that does not capture the formal-understated urgency profile of Luxembourgish citizen-government correspondence. The output paradigm is single-label hard classification with macro-F1 scoring [Q84, Q93, Q96], structurally incompatible with the deployment's multi-label, confidence-scored routing logic. Input content is biased toward formal/edited registers [Q112], with code-switching and orthographic variation — confirmed features of citizen messages — largely absent. Annotation reliability is moderate (Cohen's Kappa 0.45 [Q27]) with limited annotator provenance documentation [Q114] and notable LLM involvement in RTE and JUDGEWEL labels [Q37, Q63, Q64]. The benchmark is most useful as a generic LTZ encoder-quality signal, not as evidence of administrative-NLU readiness.

## Practical Guidance

### What This Benchmark Measures

LTZGLUE measures generic Luxembourgish NLU capability across eight GLUE-style tasks [Q67] — useful for selecting an underlying LTZ encoder backbone. It provides defensible signal on whether a model can perform PER/ORG/LOC NER, basic sentiment, headline-body coherence, linguistic acceptability, and entailment in Luxembourgish, and identifies MMBERT-base and LUXEMBERT as competitive backbones [Q105, Q106]. The IF dimension (text-only LTZ modality match) and the encoder evaluation methodology (averaged runs with variance [Q89]) are the strongest signals for the deployment.

### Construct Depth

Construct depth is shallow for the target deployment. Performance on LTZGLUE TC, ID, and SA gives no calibrated evidence about administrative-routing accuracy because the label spaces do not overlap with deployment categories [Q48, Q149, Q154]. Sentiment evaluation depth is limited by Cohen's Kappa 0.45 [Q27] and the absence of administrative-register annotators. RTE depth is partly compromised by LLM-mediated label processing [Q61, Q63, Q64]. The benchmark probes only single-label hard classification [Q84]; it provides no evidence on confidence calibration, multi-label decoding, or threshold robustness.

### What Else You Need

To reach deployment readiness, supplement with: (1) a Luxembourg-administrative topic taxonomy co-designed with civil servants and a labeled corpus of citizen messages addressing IO and OO gaps; (2) a code-switched/orthographically-variable citizen-correspondence sample to address IC; (3) civil-servant re-annotation of sentiment and urgency to address OC, leveraging the human-in-the-loop feedback mechanism described in elicitation A3; (4) calibration analysis (ECE/Brier) and multi-label evaluation harness to address OF; and (5) explicit handling of non-LTZ content (Portuguese, French, German, [WEB-10, WEB-11]) outside benchmark scope.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
LTZGLUE provides eight GLUE-style NLU tasks [Q8, Q11, Q67] but its taxonomies are fundamentally misaligned with the deployment's administrative routing needs. Topic classification covers only five RTL editorial categories — SPORTS, CULTURE, TECHNOLOGY, BUSINESS, ANIMALS [Q48] — which share zero overlap with the deployment-critical categories of cross-border worker status, housing, cost-of-living, state-vs-communal competency, EU-institutional matters, and tax/social-security routing identified in elicitation. Intent detection is restricted to voice-assistant reminder/alarm intents [Q154], with no citizen-government communication intents. NER retains only PER/ORG/LOC/MISC after merging GPE into LOC [Q44, Q152], removing the administrative-jurisdiction granularity the routing system needs. The authors themselves caution against inferring cultural/demographic coverage from benchmark performance [Q121]. Given HIGH priority weighting for IO and the existence of ~47% cross-border workforce [WEB-1] and a 100-commune state/communal split [WEB-7], the benchmark's taxonomy substantially under-represents the construct of administrative-routing NLU.

**Strengths:**
- Provides a unified, GLUE-style suite spanning binary, multi-class, sentence-level, document-level, and token-level tasks [Q67, Q70], establishing a baseline of LTZ NLU capability that the deployment can use to gauge generic encoder performance.
- Includes a token-level NER task [Q35, Q152] whose PER/ORG/LOC/MISC categories will partially transfer to entity extraction in citizen messages, even though jurisdiction-level entities are absent.

**Checklist:**

- **IO-1**: Required deployment categories include cross-border worker/frontalier status, housing, cost-of-living, national identity/residency documents, income tax (with frontalier sub-cases including the 34-day DTA threshold), social security/health insurance, urban planning/construction permits at communal level, transport (free public transit policy), EU institutional matters, labor law, education/childcare, and immigration/naturalization, plus a state-vs-communal competency distinction across 100 communes [WEB-1, WEB-7, WEB-18, WEB-20]. — _Sources: WEB-1, WEB-7, WEB-18, WEB-20_
- **IO-2**: Yes — LTZGLUE's TC taxonomy (SPORTS, CULTURE, TECHNOLOGY, BUSINESS, ANIMALS) [Q48, Q153] omits all administrative categories required for deployment routing; intent detection covers only reminder/alarm voice-assistant intents [Q154]; NER omits administrative-jurisdiction and legal-status entity types [Q44, Q152]. — _Sources: Q48, Q153, Q154, Q44, Q152_
- **IO-3**: The ANIMALS category [Q48, Q153] and the entire reminder/alarm intent set [Q154] are largely irrelevant to the citizen-correspondence routing context; the authors acknowledge the ID source register has 'no equivalent reference corpus in LTZ' [Q55]. — _Sources: Q48, Q154, Q55_
- **IO-4**: Documented gaps: zero administrative topic categories, zero state-vs-communal jurisdiction distinction, zero frontalier-specific intents, zero EU-institutional category, zero housing/cost-of-living categories. These are construct-underrepresentation gaps that materially harm content validity for the target use case; authors explicitly flag that 'Coverage across domains, registers, and demographic varieties may also be limited' [Q112]. — _Sources: Q112, Q121_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q48] 'From the available categories, we focused on five principal domains: SPORTS, CULTURE, TECHNOLOGY, BUSINESS, and ANIMALS.' (p.4)
- [Q153] 'topic_classification: Classify topic of the document by title and text. Allowed category_names: sports, animals, business, culture, technology.' (p.15)
- [Q154] 'slot_intent_detection: Detect the intent for the text given. Allowed intents: reminder/show_reminders, weather/find, reminder/set_reminder, ... alarm/set_alarm, ...' (p.15)
- [Q44] 'the tag set is harmonised by merging the GPE and LOC categories into a single location label, while retaining PER, ORG, and MISC unchanged.' (p.4)
- [Q112] 'Coverage across domains, registers, and demographic varieties may also be limited.' (p.9)
- [Q121] 'We therefore caution against using benchmark performance as evidence of cultural or demographic coverage.' (p.10)
- [Q67] 'Together, the eight tasks in LTZGLUE form a broad and balanced evaluation suite, covering four binary and four multi-class settings...' (p.5)

*Web sources:*
- [WEB-1] Cross-border workers constitute ~47% of Luxembourg's workforce — directly motivates a frontalier topic class absent from LTZGLUE
- [WEB-7] Luxembourg comprises exactly 100 communes following 2023 mergers — motivates state-vs-communal routing absent from LTZGLUE
- [WEB-18] OECD Economic Survey notes 34-day remote-work threshold under DTAs is an active frontalier policy concern
- [WEB-20] Free public transport policy in force since 2020 generates a distinct citizen-query class

</details>

**Information gaps:**
- No publicly identified Luxembourgish administrative-domain NLP dataset exists to supplement LTZGLUE topic coverage.

**Requires expert verification:**
- Definitive list of state-vs-communal competency boundary cases (e.g., état civil) requires Luxembourg administrative-law expert review.

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Input content is sourced predominantly from formal/edited registers — RTL news, the LOD dictionary, Wikipedia, transcribed parliamentary speeches, and Leipzig web crawls [Q12, Q74, Q135] — which the authors explicitly acknowledge 'reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts' [Q112]. The deployment's primary input — citizen correspondence with French/German code-switching, loanword alternation (e.g., Administratioun vs. Verwaltung), and orthographic variation — is essentially absent. The Lothritz et al. NER comment corpus [Q40, Q41] is the only documented informal/code-mixed slice. Construct-irrelevant variance is further introduced by ChatGPT-5.1 sentence improvement and ChatGPT-5-Mini filtering on RTE [Q61, Q63, Q66], removing 22–28% of instances. The intent detection register (voice-assistant commands) has 'no equivalent reference corpus in LTZ' [Q55, Q56]. Given IC is a HIGH-priority dimension with explicit user concern about code-switching and orthographic variation, the alignment is poor.

**Strengths:**
- The Lothritz et al. NER corpus drawn from RTL online news comments [Q40, Q41] does cover informal and code-mixed writing, providing a partial bridge to citizen-message register.
- Pre-training data spans diverse LTZ sources including chat rooms (Webchat), comments, and transcribed speech [Q74, Q135], giving the encoder backbones some exposure to informal LTZ even if downstream task data is largely formal.
- A substantial proportion of LTZGLUE tasks are newly created for LTZ rather than direct translations [Q69], reflecting some LTZ-specific phenomena.

**Checklist:**

- **IC-1**: Yes — Luxembourg-specific cultural, geographic, and administrative knowledge is required (commune names, administrative bodies like CNS/CNAP/CCSS/ITM, frontalier-specific concepts, OLO orthographic conventions). LTZGLUE inputs do not systematically encode these [Q12, Q74]. — _Sources: Q12, Q74_
- **IC-2**: Partial — LTZGLUE content is in-region (RTL, parliamentary speeches, LOD) [Q74, Q135] so cultural alignment is broadly Luxembourgish, but it is biased toward formal/edited media culture rather than the citizen-administration interaction context [Q112, Q119]. — _Sources: Q74, Q112, Q119_
- **IC-3**: Some Western/English-source artifacts: xSID intent dataset is translated from English voice-assistant commands [Q51] with non-LTZ register [Q55]; RTE was machine-translated then LLM-improved [Q60, Q61], potentially injecting English-centric phrasing. — _Sources: Q51, Q55, Q60, Q61_
- **IC-4**: INSUFFICIENT DOCUMENTATION — annotators are described only as 'two native speakers of LTZ' for SA [Q25] and 'student assistants' [Q114]; no documentation of demographic, regional, or administrative-domain familiarity. Would need annotator recruitment criteria from authors.
- **IC-5**: Documented content issues: (a) formal-register dominance excludes citizen-correspondence distribution [Q112]; (b) 22–28% of RTE instances filtered after LLM improvement [Q66] — distributional artifact; (c) JUDGEWEL NER labels generated by LLM judges with minimal human verification [Q37]; (d) no orthographic-variation or code-switching coverage in task data [Q7, Q112]. — _Sources: Q112, Q66, Q37, Q7_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'Unless stated otherwise, the textual data used across most tasks stems from two main sources...' (p.2)
- [Q74] 'A large portion of the data stems from RTL... transcribed political speeches and debates from the Chambre des Députés...' (p.6)
- [Q112] 'most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts.' (p.9)
- [Q119] 'LTZ is a small language community, and linguistic data often originate from a limited set of public domains.' (p.10)
- [Q55] 'a specialised spoken register for which there is no equivalent reference corpus in LTZ' (p.5)
- [Q66] 'The filtering reduced between 22 and 28% of instances in the data...' (p.5)
- [Q41] 'It covers a wider range of text types and registers, including informal and code-mixed writing...' (p.4)
- [Q7] 'the ongoing standardisation of the language..., vast amounts of variation..., and decentralised resources, make it extremely challenging to evaluate LTZ language understanding...' (p.1)

*Web sources:*
- [WEB-11] Portuguese is the second-most-spoken primary language in Luxembourg (~15% of residents) — significant share of citizen messages may be outside LTZ entirely
- [WEB-10] CIA World Factbook reports Luxembourgish as first language for only 48.9% of residents — code-switching/multilingual input is the norm

</details>

**Information gaps:**
- Exact proportion of code-switched or informal-register instances within each task split is not reported.
- No documentation of orthographic-variant coverage (OLO compliance vs. legacy spellings) in task data.

**Requires expert verification:**
- Whether sample citizen messages from MyGuichet.lu or other channels match any LTZGLUE input distribution requires inspection of internal deployment data.

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Input form alignment is partial. The benchmark is text-only and targets Luxembourgish [Q1], matching the deployment's text-only digital-correspondence modality and target language. Tokenization uses a BPE tokenizer trained on the full LTZ pre-training set with vocabulary 50,368 and max sequence length 1,024 [Q128, Q129], which is technically appropriate. However, the form profile of benchmark text differs from the deployment input distribution: non-Luxembourgish content was filtered out via OpenLID [Q47] and short sentences (<3 words) were removed [Q75], whereas citizen messages routinely contain French/German embeddings, may be very short, and exhibit non-standard orthography. The authors flag 'ongoing standardisation' and 'vast amounts of variation' [Q7] as evaluation challenges but do not preprocess to address them. The intent-detection source diverges further with all-lowercase, missing-punctuation conventions [Q55]. Given IF is MODERATE priority, partial alignment yields a middle score.

**Strengths:**
- Text-only, Luxembourgish-targeted modality matches the deployment's text-only digital-channel input [Q1].
- Custom LTZ-trained BPE tokenizer with 50,368 vocab and 1,024 max sequence length [Q128, Q129] is appropriate for typical citizen-correspondence lengths.
- Pre-training corpus includes transcribed speech and chat-room text [Q74], expanding signal diversity beyond pure edited prose.

**Checklist:**

- **IF-1**: Signal distribution differs: benchmark text is filtered for LTZ-only [Q47] and ≥3-word sentences [Q75], whereas deployment inputs include code-switched, multilingual, and very short messages. — _Sources: Q47, Q75_
- **IF-2**: Yes — text-only digital infrastructure is well-supported in Luxembourg (~99% household internet [WEB-14]; top-tier digital government [WEB-13]), so no capture-spec mismatch. — _Sources: WEB-14, WEB-13_
- **IF-3**: Domain-specific form differences: non-standard orthography, missing diacritics, French/German code-switching, and OLO-variant spellings are common in citizen messages but not represented systematically in LTZGLUE data [Q7, Q112]; xSID translation flags non-standard spelling difficulty [Q55]. — _Sources: Q7, Q112, Q55_
- **IF-4**: Form mismatches that may harm external validity: (a) language-ID filtering removes the multilingual signal that real citizen messages contain; (b) minimum-length filtering excludes short queries; (c) no orthographic-variation augmentation. These are documentation-confirmed but their magnitude requires empirical assessment. — _Sources: Q47, Q75, Q7_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'This paper presents LTZGLUE, the first Natural Language Understanding (NLU) benchmark for Luxembourgish (LTZ)...' (p.1)
- [Q47] 'we removed articles identified as non-Luxembourgish by OpenLID...' (p.4)
- [Q75] 'We filter out sentences containing fewer than three words...' (p.6)
- [Q128] 'a BPE-based tokenizer, which we train on the entire pre-training set, using a minimum frequency of two and a vocabulary size of 50,368.' (p.12)
- [Q7] 'the ongoing standardisation of the language..., vast amounts of variation...' (p.1)
- [Q55] 'non-standard spelling (e.g., all lowercase, missing punctuation).' (p.5)

*Web sources:*
- [WEB-14] ~99% household internet access in Luxembourg — digital text channel is the dominant deployment modality
- [WEB-13] Luxembourg ranks among top EU member states in e-government maturity

</details>

**Information gaps:**
- Length distribution of LTZGLUE task instances vs. expected citizen-message length is not directly reported.
- Quantitative measure of orthographic variation in LTZGLUE data is not provided.

**Requires expert verification:**
- Whether citizen-correspondence form (length, code-mixing rate, diacritic usage) overlaps measurably with LTZGLUE distributions requires deployment-side text analysis.

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Output ontology presents three converging critical misalignments. First, the benchmark is single-label and hard-classification across all eight tasks [Q84], with explicit binary or fixed multi-class label sets [Q147–Q155], whereas the deployment requires multi-label outputs and calibrated confidence scores for routing [user A4]. Second, none of the label sets contain administrative, jurisdictional, frontalier-specific, housing, cost-of-living, or EU-institutional categories — the topic-classification labels are SPORTS/CULTURE/TECHNOLOGY/BUSINESS/ANIMALS [Q153] and intent labels are reminder/alarm/weather [Q154]. Third, sentiment labels are generic positive/neutral/negative [Q149] with no calibration to the formal-but-understated register of citizen-government correspondence — directly conflicting with the deployment's urgency-prioritization logic. The NER label set merges GPE into LOC [Q44, Q152], reducing administrative granularity. With OO marked HIGH priority and high-stakes routing decisions in scope, this is a fundamental structural-validity violation.

**Strengths:**
- Output label sets are explicitly enumerated with prompts [Q146, Q147–Q155], making the existing label space transparent and easy to map or extend.
- BIO scheme for NER [Q35, Q152] is a standard format that supports re-annotation with extended administrative entity types.

**Checklist:**

- **OO-1**: Output label categories have low regional relevance for routing: TC labels are editorial-news categories [Q153]; ID labels are voice-assistant intents [Q154]; SA labels are generic 3-class sentiment [Q149]; NER tags are PER/ORG/LOC/DATE/MISC [Q152]. — _Sources: Q149, Q152, Q153, Q154_
- **OO-2**: Missing categories specific to Luxembourg administrative routing: cross-border worker status, housing, cost-of-living, identity/residency documents, income-tax (resident vs. frontalier), social security, urban planning, transport, EU-institutional, labor, education, immigration, plus state-vs-communal competency split across 100 communes [WEB-1, WEB-7, WEB-18]. — _Sources: WEB-1, WEB-7, WEB-18, Q48_
- **OO-3**: TC labels reflect RTL editorial categorization [Q48] not administrative jurisdiction; ID labels reflect English voice-assistant ontology [Q51, Q154]; sentiment encodes a generic emotion taxonomy without urgency calibration relevant to formal Luxembourgish administrative communication. — _Sources: Q48, Q51, Q154, Q149_
- **OO-4**: Stakeholder-driven taxonomy redesign is required given the elicitation's HIGH priority on OO and the explicit need for multi-label, confidence-scored outputs [user A4].
- **OO-5**: Documented taxonomy issues harming structural and content validity: (a) single-label-only output paradigm [Q84] structurally incompatible with multi-label routing; (b) absence of all deployment-relevant administrative categories; (c) no probabilistic/ranked output schema; (d) GPE/LOC merge [Q44] erases jurisdictional granularity. — _Sources: Q84, Q44_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q84] 'We did not use a Multiple Choice Question Answering (MCQA)-setup, but provided the labels that should be used as output.' (p.6)
- [Q149] 'sentiment_analysis: Classify sentiment of the text. Allowed labels: positive, neutral, negative.' (p.15)
- [Q152] 'ner: ... Allowed Tags: O, B-LOC, I-LOC, B-PER,I-PER, B-DATE, I-DATE,B-ORG, I-ORG, B-MISC, I-MISC.' (p.15)
- [Q153] 'topic_classification: ... Allowed category_names: sports, animals, business, culture, technology.' (p.15)
- [Q154] 'slot_intent_detection: ... Allowed intents: reminder/show_reminders, weather/find, ...' (p.15)
- [Q44] 'merging the GPE and LOC categories into a single location label, while retaining PER, ORG, and MISC unchanged.' (p.4)

*Web sources:*
- [WEB-1] ~47% cross-border workforce — frontalier label class required
- [WEB-7] 100 communes — state vs. communal label dimension required
- [WEB-18] OECD identifies frontalier 34-day DTA threshold and housing as active citizen concerns

</details>

**Information gaps:**
- Whether LTZGLUE evaluation code exposes per-class probabilities or only argmax labels is not documented in the paper.

**Requires expert verification:**
- Final administrative routing taxonomy should be co-designed with civil servants from national and communal authorities.

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Annotation provenance and reliability are weak for the deployment context. Sentiment labels rest on two native LTZ annotators with Cohen's Kappa 0.45 [Q25, Q27] — moderate agreement at best — with disagreements resolved by consensus [Q28]; no documentation of administrative-domain familiarity or civil-service register competence. Intent translation was performed by a single LTZ native speaker [Q52]. RTE labels were generated through a ChatGPT-5.1 improvement step [Q61] followed by ChatGPT-5-Mini quality and label verification [Q63, Q64], with manual correction of cases where logical contradictions were inadvertently 'fixed' [Q65] — this introduces LLM-induced label artifacts. JUDGEWEL NER relies on LLM judges with minimal human verification [Q37]. The authors explicitly acknowledge 'some annotation decisions and class distributions are necessarily influenced by resource constraints' and that 'automatic preprocessing may introduce biases that we cannot fully quantify' [Q113], and warn 'models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices' [Q120]. Annotator details are limited to a generic acknowledgement of student assistants [Q114]. Given OC HIGH priority and the user's explicit concern about civil-administrative sentiment calibration, convergent and external validity are substantially impaired.

**Strengths:**
- Sentiment annotation used native LTZ speakers [Q25] and the Lothritz et al. NER corpus is fully human-annotated [Q42], providing some grounding in regional linguistic competence.
- RTE label-correctness verification step [Q64, Q65] caught approximately 10% incorrect labels and the authors performed manual correction to preserve logical contradictions [Q65].
- Authors transparently document limitations and caution against over-claiming demographic coverage [Q120, Q121, Q123].

**Checklist:**

- **OC-1**: Ground truth labels do not demonstrably reflect Luxembourg civil-administrative stakeholder perspectives; no documentation indicates annotators were drawn from or consulted with civil-service domain experts [Q25, Q52, Q114]. — _Sources: Q25, Q52, Q114_
- **OC-2**: High potential for disagreement on sentiment: formal/understated citizen-government correspondence likely receives more 'neutral' labels under generic sentiment annotation than civil servants would judge appropriate for prioritization [Q149]; this is a recognized risk in elicitation Q3/A3. — _Sources: Q149_
- **OC-3**: Annotator demographics are minimally documented: 'two native speakers' for SA [Q25], 'student assistants' acknowledged [Q114], single LTZ native speaker plus consultations for ID [Q52]. No Datasheet/Data Statement-level demographic detail. — _Sources: Q25, Q52, Q114_
- **OC-4**: Re-annotation by a representative civil-servant pool is recommended given the HIGH priority and the moderate-only Cohen's Kappa of 0.45 [Q27]; the deployment's human-in-the-loop feedback mechanism (elicitation A3) provides infrastructure for progressive recalibration. — _Sources: Q27_
- **OC-5**: Aggregation method for SA used annotator consensus on disagreements [Q28] — this can erase minority/edge-case judgments relevant to detecting subtle frustration cues. Class-balanced loss [Q92] addresses imbalance but not annotator-perspective minority preservation. — _Sources: Q28, Q92_
- **OC-6**: Documented label issues harming convergent and external validity: (a) Cohen's Kappa 0.45 [Q27]; (b) LLM-mediated RTE labels [Q63, Q64]; (c) LLM-judged JUDGEWEL labels [Q37]; (d) potential pre-training contamination of LLM evaluators with RTL/Wikipedia data [Q111]; (e) absence of administrative-domain annotator expertise. — _Sources: Q27, Q63, Q64, Q37, Q111_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'we extract 4,583 sentences, which are then annotated by two native speakers of LTZ.' (p.3)
- [Q27] 'We calculated Cohen's Kappa at 0.45.' (p.3)
- [Q28] 'For the final set, the annotators agree on a label in cases of label disagreement.' (p.3)
- [Q37] 'evaluated using LLMs acting as judges, with minimal human verification to calibrate quality thresholds.' (p.4)
- [Q52] 'The translations were performed by an LTZ native speaker. In cases of uncertainty, additional native LTZ speakers were consulted.' (p.4)
- [Q63] 'we prompted CHATGPT-5-MINI to judge the texts in the improved data and label their quality...' (p.5)
- [Q64] 'we prompted CHATGPT-5-MINI to verify whether the dataset labels remained correct... Nearly 10% of the labels were false.' (p.5)
- [Q113] 'some annotation decisions and class distributions are necessarily influenced by resource constraints. Certain tasks exhibit label imbalance or rely on automatic preprocessing, which may introduce biases that we cannot fully quantify.' (p.9)
- [Q114] 'We would like to thank the student assistants for their annotation work.' (p.9)
- [Q120] 'models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices.' (p.10)
- [Q117] 'some tasks draw on data originally produced in institutional or media contexts, which may reflect societal biases in representation.' (p.10)

*Web sources:*
- [WEB-1] Cross-border workforce ~47% — annotators drawn from formal-media context unlikely to reflect frontalier-specific concerns

</details>

**Information gaps:**
- Annotator linguistic background, regional origin, and occupation are undocumented.
- Proportion of LLM-annotated vs. human-annotated NER and RTE test instances not separable from public materials.

**Requires expert verification:**
- Calibration of sentiment/urgency labels against civil-servant judgments on representative citizen-message samples.

---

### Output Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
All LTZGLUE tasks are evaluated with macro-F1 over single-label predictions [Q84, Q93, Q96], with malformed LLM outputs discarded prior to scoring [Q90, Q91]. The deployment requires multi-label classification with calibrated confidence scores to drive routing thresholds and human-in-the-loop escalation [user A4] — an output form LTZGLUE never produces or evaluates. Prompted LLMs are evaluated once with macro-F1 [Q96] and the authors note results 'should be interpreted as indicative rather than directly comparable' due to prompt sensitivity [Q86, Q87]. There is no calibration analysis, no probabilistic scoring, no multi-label evaluation, and no per-class confidence reporting. Encoders report averages over three runs with standard deviations [Q89, Q96], which is methodologically sound but still single-label. With OF MODERATE priority and the deployment requiring confidence-aware multi-label outputs, this is a clear functional gap.

**Strengths:**
- Encoder evaluation reports averages over three runs with standard deviations [Q89, Q96], providing variance estimates useful for deployment risk assessment.
- Class-balanced loss is applied to imbalanced tasks [Q92], and Bayesian hyperparameter search with early stopping is used [Q138] — sound methodology for low-resource fine-tuning.
- Output modality (text label) and target literacy/digital channel match the deployment context (text-only digital correspondence; near-universal internet access [WEB-14]).

**Checklist:**

- **OF-1**: Expected output modality is partially aligned: both benchmark and deployment use textual labels, but the deployment additionally requires multi-label outputs and confidence scores [user A4] that LTZGLUE does not produce or evaluate [Q84, Q93]. — _Sources: Q84, Q93_
- **OF-2**: Not applicable — deployment is text-only with no speech-output requirement; civil-servant users are assumed digitally literate with high digital-government maturity [WEB-13]. — _Sources: WEB-13_
- **OF-3**: Civil servants are the direct consumers of classification outputs and are assumed digitally proficient; literacy/accessibility constraints affect citizen authors but not the output modality, which is structured labels delivered to civil servants. INSUFFICIENT DOCUMENTATION on whether benchmark output formatting (e.g., JSON [Q146]) matches deployment integration requirements.
- **OF-4**: Form mismatches harming external validity: (a) single-label F1 evaluation provides no signal about confidence calibration; (b) malformed-output discarding [Q90, Q91] hides robustness failures relevant to production routing; (c) no multi-label scoring; (d) prompt-based LLM evaluation flagged as 'indicative' only [Q86]. — _Sources: Q90, Q91, Q86, Q96_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q84] 'We did not use a Multiple Choice Question Answering (MCQA)-setup, but provided the labels that should be used as output.' (p.6)
- [Q93] 'Table 6 shows F1 scores for all models across all tasks...' (p.7)
- [Q96] 'Encoder results are averaged over three runs with standard deviations as subscripts. Prompted LLMs were evaluated once; we report macro-F1 only.' (p.8)
- [Q90] 'Prompted LLMs do not always produce well-formed outputs and may return an incorrect number of predictions for a given task; such outputs are discarded prior to evaluation.' (p.7)
- [Q86] 'prompt-based evaluation introduces additional sources of variability... performance should be interpreted as indicative rather than directly comparable to supervised results.' (p.6)
- [Q92] 'we use class-balanced loss based on effective size...' (p.7)
- [Q146] 'Respond ONLY in valid JSON. ... Use field: "output": <model_answer>...' (p.14)

*Web sources:*
- [WEB-13] Luxembourg ranks among top EU member states in e-government maturity — civil-servant interface assumed structured-text
- [WEB-14] ~99% household internet access — text-output channel is appropriate

</details>

**Information gaps:**
- No reported calibration metrics (e.g., ECE, Brier score) for any task.
- No multi-label evaluation or threshold-sensitivity analysis.

**Requires expert verification:**
- Whether LTZGLUE evaluation scripts can be extended to expose probabilities for downstream multi-label/threshold use requires inspection of the project repository.

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** All tasks emit single hard labels [Q84]; deployment requires multi-label routing with confidence scores.

**Recommendation:** Define a multi-label output schema with calibrated probabilities; evaluate using ranking metrics (e.g., micro-F1@k, mean average precision) and calibration metrics (ECE, Brier) alongside macro-F1; expose argmax + per-class probabilities from the model.

### Input Ontology ⚠

**Gap:** LTZGLUE TC/ID/NER taxonomies contain zero administrative routing categories and no state-vs-communal jurisdiction split.

**Recommendation:** Co-design a Luxembourg administrative routing taxonomy with national and communal civil servants covering frontalier status, housing, cost-of-living, identity/residency, tax (with frontalier sub-cases), social security, urban planning (per-commune), transport, EU-institutional, labor, education/childcare, and immigration; collect a labeled evaluation set per category.

### Output Content ⚠

**Gap:** Sentiment annotation rests on two annotators with Cohen's Kappa 0.45 [Q27] and undocumented administrative-domain familiarity; LLM-mediated label processing in RTE/JUDGEWEL [Q37, Q63, Q64] introduces uncertainty.

**Recommendation:** Recruit ≥3 annotators with documented Luxembourgish civil-administrative experience; re-annotate a stratified sample of sentiment/urgency on citizen-correspondence data; report inter-annotator agreement with disagreement analysis preserved (avoid consensus-erasure of minority judgments [Q28]); leverage the human-in-the-loop feedback mechanism for progressive recalibration.

### Input Content ⚠

**Gap:** Benchmark content is dominated by formal RTL/parliamentary/Wikipedia/LOD sources [Q112]; citizen-correspondence register with code-switching and orthographic variation is essentially absent.

**Recommendation:** Construct an in-domain evaluation corpus from anonymized citizen messages received via MyGuichet.lu and similar channels, preserving code-switching, French/German loanword alternation (e.g., Administratioun/Verwaltung), and OLO/non-OLO orthographic variants.

### Input Form

**Gap:** OpenLID filtering [Q47] and ≥3-word filtering [Q75] remove signal characteristics common in real citizen messages (multilingual content, short queries).

**Recommendation:** Add a deployment-side preprocessing audit that measures language-mix proportions and message-length distributions, and complement LTZGLUE-trained models with explicit detection of non-LTZ content (Portuguese/French/German [WEB-10, WEB-11]) routed to language-appropriate pipelines.

### Output Form

**Gap:** Single-label macro-F1 evaluation with malformed outputs discarded [Q90, Q91, Q96] provides no calibration or robustness signal for production routing.

**Recommendation:** Add confidence-calibration evaluation (ECE, reliability diagrams), threshold-sweep analyses for routing decisions, and a separate report of malformed-output rates (rather than discarding) to surface production robustness.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This paper presents LTZGLUE, the first Natural Language Understanding (NLU) benchmark for Luxembourgish (LTZ) based on the popular GLUE benchmark for English." |
| Q2 | 1 | input_ontology | "Our tasks include common natural language processing tasks in binary and multi-class classification settings, including named entity recognition, topic classification, and intent classification." |
| Q3 | 1 | output_form | "We evaluate various pre-trained language models for LTZ to present an overview of the current capabilities of these models on the LTZ language." |
| Q4 | 1 | input_ontology | "Small and under-researched languages are particularly difficult to evaluate, as is the case with Luxembourgish (LTZ), the national language of Luxembourg, with around 400k speakers." |
| Q5 | 1 | input_ontology | "LTZ only has a handful of NLU tasks available (Lothritz et al., 2022; Philippy et al., 2024; Plum et al., 2026)." |
| Q6 | 1 | input_content | "As most of these are in the news domain, and the majority of the down-stream tasks comprise less than a thousand instances, model evaluation is not always dependable." |
| Q7 | 1 | input_form | "Additional factors, such as the ongoing standardisation of the language (Gilles, 2019), vast amounts of variation (Lutgen et al., 2025), and decentralised resources, make it extremely challenging to evaluate LTZ language understanding in language models." |
| Q8 | 1 | input_ontology | "Our contributions are: (1) LTZGLUE: the first unified GLUE benchmark for LTZ, with 8 tasks." |
| Q9 | 1 | input_ontology | "(2) LTZ-E1 (mini/base): 2 new encoder language models for LTZ, which achieve competitive performance when fine-tuned on LTZGLUE." |
| Q10 | 1 | output_content | "Alistair Plum1, Felicia Körner2,3, Anne-Marie Lutgen1, Laura Bernardy1, Fred Philippy1, Emilia Milano1, Nils Rehlinger1, Cédric Lothritz4, Tharindu Ranasinghe5, Barbara Plank2,3, Christoph Purschke1 1University of Luxembourg, Luxembourg, 2LMU Munich, Germany 3Munich Center for Machine Learning, Germany 4LIST, Luxembourg, 5Lancaster University, UK" |
| Q11 | 2 | input_ontology | "In this section, we introduce the eight tasks for LTZGLUE. The set spans binary and multi-class sentence and token-level classification tasks. Together, these tasks cover a broad spectrum of linguistic and semantic phenomena and provide the first unified benchmark for evaluating LTZ NLP models." |
| Q12 | 2 | input_content | "Unless stated otherwise, the textual data used across most tasks stems from two main sources: (i)" |
| Q13 | 2 | input_ontology | "LTZ, the focus of this benchmark, is regarded as under-researched, and research is ongoing. Joshi et al. (2020) classify Luxembourgish as one of the "scraping-by" languages: although some unlabeled data exists, meaningful progress will require coordinated efforts to raise awareness and collect labeled datasets, as such resources are currently almost nonexistent." |
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
| Q43 | 4 | input_content | "The two datasets are merged to increase both coverage and domain balance." |
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
| Q57 | 5 | input_form | "After translating the dataset, we transferred the BIO tags by first using token-level fuzzy matching between the LTZ and the German dataset, followed by manual verification." |
| Q58 | 5 | output_ontology | "Table 5 shows the label distribution and size of each data split." |
| Q59 | 5 | input_ontology | "Recognizing Textual Entailment (RTE) (Haim et al., 2006) is a classic NLU task featured in the original GLUE benchmark. Given a pair of texts A and B, the task consists of determining whether A is a logical premise of B." |
| Q60 | 5 | input_content | "Lothritz et al. (2023) released a machine-translated Luxembourgish version of the dataset using Google Translate. However, due to numerous grammar and vocabulary related mistakes introduced in this process, we set out to improve the quality of the dataset." |
| Q61 | 5 | input_content | "Specifically, we first prompted CHATGPT-5.1 to assess and improve the translated sentence pairs unless they were already of very high quality, while explicitly keeping the original meaning to avoid label conflicts (see Appendix 7.4)." |
| Q62 | 5 | output_content | "In addition, we perform two verification steps to make sure that (a) the quality of the improved texts is high enough and (b) that the labels are correct." |
| Q63 | 5 | output_content | "To achieve (a), we prompted CHATGPT-5-MINI to judge the texts in the improved data and label their quality as either low, medium, or high, keeping only data rated at least medium, removing nearly 25% of the entire dataset (see Appendix 7.5)." |
| Q64 | 5 | output_content | "For (b), we prompted CHATGPT-5-MINI to verify whether the dataset labels remained correct after the first translation and improvement, outputting true or false for each sentence pair (see Appendix 7.6). Nearly 10% of the labels were false." |
| Q65 | 5 | output_content | "We found that the quality improvement step often corrected intentional logical contradictions or factual inaccuracies rather than keeping the original semantics. We therefore adjusted the sentences manually such that they corresponded to the ground truth again, while keeping false positives intact." |
| Q66 | 5 | input_content | "The filtering reduced between 22 and 28% of instances in the data, resulting in a final dataset of 1,876, 197, and 626 sentence pairs for the training, development, and test set, respectively." |
| Q67 | 5 | input_ontology | "Together, the eight tasks in LTZGLUE form a broad and balanced evaluation suite, covering four binary and four multi-class settings, sentence- and document-level inputs, as well as a token-level sequence-labelling task." |
| Q68 | 5 | input_ontology | "Despite the low-research status of LTZ, this places LTZGLUE in the same general range as the original English GLUE benchmark, which comprises nine diverse NLU tasks (Wang et al., 2019b)." |
| Q69 | 5 | input_content | "In addition, a substantial proportion of the LTZGLUE tasks are newly created for LTZ rather than direct translations or simple repackaging, allowing the benchmark to reflect phenomena and usage patterns specific to the language." |
| Q70 | 6 | input_ontology | "In this landscape, supporting eight tasks for LTZ, including token-level NER and several newly constructed text-level tasks, is a strong indicator of the maturity and breadth of the emerging LTZ NLP ecosystem." |
| Q71 | 6 | input_ontology | "This design allows us to assess current LTZ NLU performance across fundamentally different modelling paradigms, while maintaining a clear separation between task-specific supervision and general-purpose language understanding." |
| Q72 | 6 | output_form | "We train two encoder language models for LTZ: LTZ-E1-mini with 68M and LTZ-E1-base with 110M non-embedding parameters." |
| Q73 | 6 | output_form | "We closely follow the Ettin recipe (Weller et al., 2026), which is based on MODERNBERT (Warner et al., 2025)." |
| Q74 | 6 | input_content | "The pre-training set is compiled from a variety of sources of LTZ. A large portion of the data stems from RTL (see Section 3), including news articles (News), transcribed radio interviews (Radio), and user comments (Comments). We also include transcribed podcasts (Podcasts) and transcribed political speeches and debates from the Chambre des Députés (Chamber). In addition, we use 1M sentences from the web crawl of the Leipzig Collection (Web, this excludes RTL), text crawled from LTZ chat rooms (Webchat), a Wikipedia crawl from October 2023 (Wikipedia), and finally, example sentences from the LOD retrieved in March 2024." |
| Q75 | 6 | input_form | "We filter out sentences containing fewer than three words (as tokenized by whitespace), totalling 11.7M sentences, which corresponds to roughly 233M tokens using our tokenizer." |
| Q76 | 6 | input_ontology | "We evaluate a set of supervised encoder-based models that explicitly support LTZ, either through direct pre-training or multilingual coverage." |
| Q77 | 6 | output_form | "As a representative baseline, we include multilingual BERT (MBERT-base) (Devlin et al., 2019), which still remains widely used for multilingual transfer and low-resource evaluation." |
| Q78 | 6 | output_form | "We additionally evaluate a more recent multilingual BERT (MMBERT-base) variant with updated pre-training data and tokenisation." |
| Q79 | 6 | output_form | "To complement these general-purpose multilingual models, we include LUXEMBERT, a language-specific model trained on LTZ data (Lothritz et al., 2022), which provides a stronger inductive bias for the language's lexical and orthographic properties." |
| Q80 | 6 | output_form | "Finally, we evaluate XLM-RoBERTa (XLM-R-base) (Conneau et al., 2020), a large-scale multilingual model trained on substantially more data and languages than MBERT-base, and commonly used as a strong reference point for multilingual NLU." |
| Q81 | 6 | output_form | "In addition to supervised encoder-based models, we evaluate a set of LLMs in a prompt-based zero-shot setting. This group includes QWEN3-235B, LLAMA-3.3, GEMMA-3-27B, and GPT5-MINI, which represent a range of model sizes, training regimes, and degrees of multilingual coverage." |
| Q82 | 6 | output_content | "None of these models are fine-tuned on LTZGLUE, although some of the text data (RTL, Wikipedia) is very likely to have been processed during training." |
| Q83 | 6 | output_form | "The models are evaluated using prompts that describe each task, allowing us to assess their ability to generalise to LTZ without task-specific supervision." |
| Q84 | 6 | output_ontology | "We did not use a Multiple Choice Question Answering (MCQA)-setup, but provided the labels that should be used as output." |
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
| Q111 | 9 | output_content | "In addition, some of the data sources used in this benchmark may already be included, in whole or in part, in the pre-training corpora of the large language models evaluated in this work. While the exact composition of proprietary pre-training datasets is typically not fully disclosed, this potential overlap cannot be entirely ruled out and may inflate performance estimates." |
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
| Q126 | 12 | output_form | "We train two sizes of LTZ-E1 models, mini and base, with 68M and 110M non-embedding parameters, respectively." |
| Q127 | 12 | output_form | "LTZ-E1-mini has 19 hidden layers, a hidden size of 512, an intermediate size of 768, and 8 attention heads, whereas LTZ-E1-base has 22 hidden layers, a hidden size of 768, an intermediate size of 1152, and 12 attention heads." |
| Q128 | 12 | input_form | "Both models share a GPTNeoXTokenizerFast tokenizer (Black et al., 2022), a BPE-based tokenizer, which we train on the entire pre-training set, using a minimum frequency of two and a vocabulary size of 50,368." |
| Q129 | 12 | input_form | "We use a constant batch size of 1024 packed sequences, where both models have a max sequence length of 1024." |
| Q130 | 12 | output_form | "We follow ModernBERT (Warner et al., 2025) and Ettin (Weller et al., 2026) in using the Warmup-Stable-Decay (WSD) scheduler (Zhai et al., 2022; Hu et al., 2024), though we use a shorter warmup and decay phase of 500 batches each, due to our smaller pre-training dataset size and larger number of epochs (10 vs. one)." |
| Q131 | 12 | output_form | "Again following ModernBERT and Ettin's recipe, we use the StableAdamW optimizer (Wortsman et al., 2023), with a peak learning rate of 3e-3 with a weight decay of 3e-4 for LTZ-E1-mini and 8e-4 with a weight decay of 1e-5 for LTZ-E1-base." |
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
| Q145 | 14 | output_ontology | "You are an expert for the Luxembourgish language. I am giving you two texts TEXT1 and TEXT2 in Luxembourgish as well as a LABEL where 1 means that TEXT1 logically entails TEXT2 while 0 means the opposite. You have to check if the labels are correct. As output, simply write 'true' if the label is the correct one or 'false' if the label is incorrect." |
| Q146 | 14 | output_ontology | "You are a classification and text-processing model specialized in NLP tasks for Luxembourgish (lb). Follow ALL rules strictly: 1. Respond ONLY in valid JSON. 2. Do NOT add explanations, comments or text outside of JSON. 3. Use field: "output": <model_answer>. 4. Use field: "task": "<task_name>". 5. Use field: "input": "<input example text>". 6. Predict only the requested outputs and" |
| Q147 | 15 | output_ontology | "If determined labels are 0 and 1 then 0 is used for False, 1 is used for True." |
| Q148 | 15 | output_ontology | "headline_classification: Decide if the given title/headline fits the text. Output True or False." |
| Q149 | 15 | output_ontology | "sentiment_analysis: Classify sentiment of the text. Allowed labels: positive, neutral, negative." |
| Q150 | 15 | output_ontology | "linguistic_acceptability_binary: Decide whether the sentence is linguistically acceptable in Luxembourgish. Output: 0 or 1." |
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
| WEB-2 | https://www.chronicle.lu/category/surveys-reports/54808-cross-border-workers-constitute-47-of-luxembourgs-500k-workforce-in-2023 |
| WEB-3 | https://luxembourg.public.lu/en/society-and-culture/population/demographics.html |
| WEB-4 | https://www.alphatrad.co.uk/news/portuguese-in-luxembourg |
| WEB-5 | https://statistiques.public.lu/en/actualites/2025/stn16-population-2025.html |
| WEB-6 | https://statistiques.public.lu/en/actualites/2024/stn16-population-2024.html |
| WEB-7 | https://gouvernement.lu/en/actualites/toutes_actualites/communiques/2023/02-fevrier/10-100-communes.html |
| WEB-8 | https://elections.public.lu/en/fusion-communes.html |
| WEB-9 | https://en.paperjam.lu/article/delano_understanding-cross-border-worker-phenomenon |
| WEB-10 | https://theworldfactbook.org/country/luxembourg.html |
| WEB-11 | https://en.wikipedia.org/wiki/Portuguese_in_Luxembourg |
| WEB-12 | https://www.mdpi.com/1999-5903/17/6/228 |
| WEB-13 | https://digital-strategy.ec.europa.eu/en/policies/desi-luxembourg |
| WEB-14 | https://www.statista.com/statistics/377741/household-internet-access-in-luxembourg/ |
| WEB-15 | https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Urban-rural_Europe_-_digital_society |
| WEB-16 | https://eufordigital.eu/wp-content/uploads/2020/06/DESI2020Thematicchapters-FullEuropeanAnalysis.pdf |
| WEB-17 | https://statistiques.public.lu/en/publications/series/luxembourg-en-chiffres/2024/luxembourg-en-chiffres-2024.html |
| WEB-18 | https://www.oecd.org/en/publications/2025/04/oecd-economic-surveys-luxembourg-2025_3eb782b5/full-report/reviving-productivity-growth_4509ab88.html |
| WEB-19 | https://www.expatica.com/lu/working/employment-basics/cross-border-worker-in-luxembourg-1063529/ |
| WEB-20 | https://transports.public.lu/en/plus/faq/gratuite-transports-publics.html |
| WEB-21 | https://www.mobiliteit.lu/en/tickets-page/fares/ |
| WEB-22 | https://regulations.ai/regulations/luxembourg-summary |
| WEB-23 | https://cms.law/en/int/expert-guides/ai-regulation-scanner/luxembourg |
| WEB-24 | https://www.pinsentmasons.com/out-law/news/luxembourg-law-addresses-eu-ai-act-enforcement |
| WEB-25 | https://www.arendt.com/news-insights/news/new-luxembourg-bill-designates-national-authorities-under-the-ai-act-the-cnpd-takes-centre-stage/ |
| WEB-26 | https://cnpd.public.lu/en/actualites/national/2025/08/ai-act-un-an.html |
| WEB-27 | https://cnpd.public.lu/en/dossiers-thematiques/intelligence-artificielle/regulation-ia/ria-maitrise-ia.html |
| WEB-28 | https://luxembourg.public.lu/en/living/mobility/public-transport.html |
| WEB-29 | https://washington.mae.lu/en/actualites/2020/free-public-transport-nationwide.html |
| WEB-30 | https://www.migrationpolicy.org/country-resource/luxembourg |

---
