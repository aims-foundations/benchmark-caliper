## Deployment Context

**Use case:** In a newsroom setting, journalists and editors use LLM-powered software to manage Luxembourgish news articles by applying a model evaluated on headline acceptability, linguistic acceptability, topic classification, and named entity recognition. The system automatically verifies grammatical standards, classifies the article’s domain, and identifies key entities to enable automatic internal linking between related news stories. These outputs determine whether a headline is logically consistent with its content and if the article can be instantly published or must be flagged for manual editorial revision to maintain professional standards.
**Target population:** Professional journalists, editors, and digital content managers at Luxembourgish media outlets who produce and curate news content in the Luxembourgish language for a local audience.

# Validity Analysis: ltzglue
**Target context:** Luxembourgish Professional Newsroom — LtzGLUE Assessment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 4 | Minor gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form | 3 | Moderate gaps | medium |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 4 | Minor gaps | high |
| **Average** | **2.8** | | |

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

LTZGLUE provides genuinely useful task coverage for a Luxembourgish professional newsroom — all four required tasks (HA, LA, TC, NER) are present, the modality matches, and reporting practices are mostly sound. However, on the three deployment-priority HIGH dimensions (IC, OO, OC), the benchmark exhibits systematic mismatches with deployment ground truth. Code-switching, the deployment's core operational requirement, is not systematically represented and is actively filtered out of the TC pipeline by OpenLID. The LA label ontology is anchored in formal prescriptive standards (LOD/Spellchecker.lu, aligned with the ZLS 2019 D'Lëtzebuerger Orthografie) rather than the flexible journalistic register the deployment targets. Ground-truth labels for HA and LA show no documented involvement of professional journalists or editors, with HA constructed algorithmically and LA generated from dictionary manipulations. RTL Lëtzebuerg dominates source data, raising single-outlet representativeness concerns. The benchmark's authors are commendably transparent about these limitations [Q110, Q112, Q113, Q117, Q120], but transparency does not resolve the validity gap for this specific deployment.

## Practical Guidance

### What This Benchmark Measures

LTZGLUE measures whether models can perform GLUE-style classification on Luxembourgish text drawn predominantly from RTL Lëtzebuerg and other formal/institutional sources, with labels derived from prescriptive linguistic standards (LA), algorithmic construction (HA), editorial categories (TC), and a mix of human and LLM annotation (NER, RTE, SA, ID). For the four deployment-required tasks, it gives a defensible upper-bound estimate of model capability on monolingual, formal-register Luxembourgish. The strongest dimension for deployment relevance is Input Ontology — the task set genuinely covers the deployment's needs — followed by Output Form, where the F1/threshold-friendly classification paradigm aligns cleanly with the per-task flagging architecture.

### Construct Depth

Construct depth is shallow for the deployment's actual ground truth. Headline acceptability is operationalised as topical/temporal headline-body match rather than editorial acceptability; linguistic acceptability is operationalised as prescriptive correctness rather than journalistic register; NER loses the country/administrative-region distinction needed for cross-border journalism via the GPE/LOC merger. The benchmark probes a related but narrower construct on each of the deployment's three highest-priority dimensions (IC, OO, OC). Topic classification is the exception — the construct probed matches what the deployment needs, and benchmark-deployment alignment is strong there.

### What Else You Need

Three concrete supplements are needed before the benchmark can underwrite deployment thresholds. (1) IC: a code-switching test set drawn from real newsroom copy, with French/German/English embeddings preserved, to evaluate per-task performance under realistic input distributions. (2) OC: a re-annotation pilot for HA and LA on a representative test subset, using working journalists/editors applying the editorial register, to quantify the label-shift rate against the benchmark's prescriptive labels. (3) OO: a NER label-set extension that restores the GPE/country distinction for EU-institution and Greater-Region entities, plus a multi-class LA scheme that distinguishes prescriptive-error from register-acceptable variant. A per-class confusion matrix from the benchmark's existing test sets would also materially help threshold calibration.

## Dimension Details

### Input Ontology — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
All four deployment-required tasks (HA, LA, TC, NER) are explicitly present in LTZGLUE [Q8, Q11, Q15, Q67]. Headline acceptability is formulated as binary headline-body match [Q15], directly matching the deployment's HA need. Topic classification uses a five-label scheme [Q48] that the deployment team accepts as adequate (A1). The benchmark also contains tasks irrelevant to the deployment (intent detection targeting voice-assistant register [Q55], RTE, SA), but these can simply be ignored at deployment time and do not harm IO validity for the four required tasks. The remaining concern is that the benchmark's task formulations — particularly HA constructed by TF-IDF headline swapping [Q16-Q22] — operationalise the construct in a way that may diverge from the editorial 'does this headline actually fit the article in a journalistically acceptable way' question. With dimension priority MODERATE per elicitation, score 4 is appropriate.

**Strengths:**
- Full task coverage: all four deployment-required tasks present in benchmark [Q8, Q11, Q67]
- HA formulated as binary headline-body match, the exact deployment subtask [Q15]
- TC five-label set explicitly accepted as adequate by the deployment team (A1) and the task is the most stable across models [Q99]
- Substantial proportion of tasks newly constructed for LTZ rather than direct translations [Q69, Q70], improving construct fit for the language

**Checklist:**

- **IO-1**: Required categories per deployment elicitation are HA, LA, TC, NER (A1, A4); all four are represented in LTZGLUE [Q8, Q11, Q67]. — _Sources: Q8, Q11, Q15, Q67_
- **IO-2**: No required category is omitted. The narrow TC label set [Q48] omits POLITICS/GOVERNMENT, which is unusual for a newsroom but explicitly accepted by the deployment team (A1). — _Sources: Q48_
- **IO-3**: Intent detection [Q55] and RTE [Q59] are present but irrelevant to the newsroom deployment; ID's voice-assistant register [Q55] is explicitly off-domain. These do not harm IO validity for the four selected tasks because they can be excluded. — _Sources: Q55, Q59_
- **IO-4**: Minor gap: HA construction via algorithmic headline swapping [Q16-Q22] tests headline-body match as a topical/structural alignment problem, which may underspecify the editorial notion of headline acceptability (clickbait, accuracy, tone). Documented but limited. — _Sources: Q15, Q16_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q8] 'LTZGLUE: the first unified GLUE benchmark for LTZ, with 8 tasks.' (p.1)
- [Q11] 'In this section, we introduce the eight tasks for LTZGLUE. The set spans binary and multi-class sentence and token-level classification tasks.' (p.2)
- [Q15] 'We formulate headline acceptability (HA) as a binary classification task where the model must decide whether a given headline matches the accompanying article body.' (p.3)
- [Q48] 'we focused on five principal domains: SPORTS, CULTURE, TECHNOLOGY, BUSINESS, and ANIMALS.' (p.4)
- [Q55] 'The source segments consist of user commands for a voice-controlled AI assistant, representing a specialised spoken register for which there is no equivalent reference corpus in LTZ.' (p.5)
- [Q67] 'Together, the eight tasks in LTZGLUE form a broad and balanced evaluation suite, covering four binary and four multi-class settings...' (p.5)
- [Q99] 'The topic classification task emerges as the easiest overall.' (p.8)

</details>

**Information gaps:**
- Whether the algorithmic HA construction adequately approximates editorial headline acceptability judgements (clickbait, factual fit, tone) cannot be determined from documentation.

**Requires expert verification:**
- Editorial team validation that the binary headline-body-match formulation maps to their internal HA flag criteria.

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Input Content is the deployment's HIGH-priority risk per elicitation, and the evidence supports a low score. Code-switching is a core operational requirement (A2), but the benchmark documentation describes no systematic code-switched content; instead the OpenLID filter in TC preprocessing [Q47] would actively exclude code-switched sentences, and the authors themselves warn that most sources reflect 'formal writing or institutional usage rather than informal or multilingual contexts' [Q112] and that models may 'reproduce dominant norms while under-representing multilingual practices' [Q120]. Data are dominated by RTL [Q12, Q74, Q135] — a single outlet with public service obligations [WEB-2] — limiting representativeness across the Luxembourg media landscape [WEB-5, WEB-6]. The Lothritz et al. NER corpus is noted as covering 'informal and code-mixed writing' [Q41], a partial mitigation, but it is one sub-component. Cross-border/EU institutional entity coverage in NER cannot be confirmed from documentation. Authors flag that ecological validity is limited [Q110] and that resource-constraint biases 'cannot be fully quantified' [Q113].

**Strengths:**
- Authentic institutional/journalistic Luxembourgish text from RTL is the dominant source [Q12, Q74], matching the broad domain of deployment
- NER corpus from Lothritz et al. explicitly includes informal and code-mixed writing [Q41], providing partial code-switching coverage for that one task
- Authors are transparent about register and demographic coverage limitations [Q112, Q119, Q120]
- Multiple data sources (RTL, LOD, Wikipedia, Leipzig, Webchat, Chamber, podcasts) provide some domain breadth in the pre-training corpus [Q74, Q135]

**Checklist:**

- **IC-1**: Yes — newsroom inputs require handling of cross-border entities (EU institutions, Greater Region), code-switched French/German/English lexical items, and journalistic register Luxembourgish (deployment context, A2). The benchmark does not document systematic coverage of these. — _Sources: Q47, Q112, Q120_
- **IC-2**: Most content originates from RTL Lëtzebuerg and other Luxembourg public sources [Q12, Q74, Q135]; cultural alignment is in-region but skewed to one outlet's editorial conventions. — _Sources: Q12, Q74, WEB-2, WEB-5_
- **IC-3**: Intent detection content was translated from English voice-assistant commands [Q51, Q55] and is not natively Luxembourgish in register; this is a Western-AI-product domain artefact unrelated to newsroom needs. — _Sources: Q51, Q55_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotator panel reviewed instances for cultural sensitivity; authors acknowledge biases 'cannot be fully quantified' [Q113]. — _Sources: Q113_
- **IC-5**: Documented content issues: (a) systematic exclusion of code-switched text via OpenLID filter in TC [Q47]; (b) RTL outlet dominance [Q12, Q74] [WEB-2]; (c) under-representation of informal/multilingual contexts [Q112, Q120]; (d) intent detection from translated voice-assistant register [Q55]; (e) resource constraints introducing unquantified biases [Q113]. — _Sources: Q47, Q74, Q110, Q112, Q113, WEB-2, WEB-6_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'Unless stated otherwise, the textual data used across most tasks stems from two main sources' (p.2)
- [Q41] 'It covers a wider range of text types and registers, including informal and code-mixed writing, and focuses on four primary entity categories (PER, ORG, LOC, GPE).' (p.4)
- [Q47] 'we removed articles identified as non-Luxembourgish by OpenLID...' (p.4)
- [Q74] 'A large portion of the data stems from RTL...' (p.6)
- [Q110] 'Several tasks rely on relatively small or domain-specific corpora, which limits the ecological validity of the results...' (p.9)
- [Q112] 'Coverage across domains, registers, and demographic varieties may also be limited. LTZ displays substantial orthographic and sociolinguistic variation, yet most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts.' (p.9)
- [Q113] 'some annotation decisions and class distributions are necessarily influenced by resource constraints. Certain tasks exhibit label imbalance or rely on automatic preprocessing, which may introduce biases that we cannot fully quantify.' (p.9)
- [Q119] 'LTZ is a small language community, and linguistic data often originate from a limited set of public domains.' (p.10)
- [Q120] 'models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices.' (p.10)
- [Q55] 'The source segments consist of user commands for a voice-controlled AI assistant...' (p.5)

*Web sources:*
- [WEB-2] CMPF Media Pluralism Monitor 2024 confirms RTL public service mandate (2024–2030 State convention), reinforcing single-outlet-dominance concern
- [WEB-5] Conseil de Presse editor-in-chief registry confirms a multi-outlet Luxembourg media landscape (Mediahuis, Editpress, Lumédia, Woxx, Reporter.lu, etc.) not represented in benchmark sources
- [WEB-6] Conseil de Presse composition data confirms outlet diversity not reflected in LTZGLUE provenance

</details>

**Information gaps:**
- Quantitative measure of code-switching prevalence in benchmark instances per task
- Whether NER corpora contain sufficient EU institution and Greater Region administrative entity instances
- Whether non-RTL outlet copy is represented anywhere in the benchmark

**Requires expert verification:**
- Direct corpus inspection by an LTZ NLP expert to quantify code-switching frequency in HA, LA, NER, and TC test sets
- Author inquiry on whether non-RTL newsroom copy was included in any task

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Form modality matches: both benchmark and deployment are text-only [Q116, deployment context]. Latin script is shared, eliminating script mismatch. The LTZ-E1 BPE tokeniser was trained on the LTZ pre-training corpus [Q128] which under-represents multilingual content [Q112, Q120], so subword fragmentation of code-switched French/German/English proper nouns is a plausible (but undocumented) risk. The benchmark's normalisation pipeline relies on LOD and OpenLID filtering [Q47], aligning the data toward formal-orthographic standards (ZLS's 2019 D'Lëtzebuerger Orthografie [WEB-3]) that the deployment team explicitly does not target. Authors note 'vast amounts of variation' [Q7] and that data reflect formal writing [Q112]. Maximum sequence length 1024 [Q129] is adequate for headlines and short articles but may truncate longer newsroom copy. With dimension priority MODERATE, score 3 reflects modality match offset by tokenisation/normalisation register concerns.

**Strengths:**
- Text-only modality matches deployment pipeline (deployment context)
- Latin script alignment eliminates script-level risk
- BPE tokeniser explicitly trained on LTZ corpus [Q128] provides better LTZ subword coverage than generic multilingual tokenisers
- Personal-data preprocessing avoids directly identifying information [Q116], easing GDPR posture

**Checklist:**

- **IF-1**: Text-only signal in both contexts. Encoder max sequence length 1024 [Q129] may truncate long-form articles but covers headlines and most news copy. — _Sources: Q116, Q129_
- **IF-2**: Luxembourg has near-universal high-bandwidth internet [WEB-10, WEB-11]; deployment infrastructure supports any text-input form the benchmark uses. — _Sources: WEB-10, WEB-11_
- **IF-3**: Domain-specific form differences: benchmark normalisation is anchored in LOD (ZLS 2019 standard) [Q30, WEB-3] and OpenLID filtering [Q47], whereas newsroom copy uses a flexible journalistic register with extensive orthographic variation [Q7, Q112]. Code-switched proper nouns may be aggressively subword-fragmented by the LTZ-trained BPE tokeniser [Q128]. — _Sources: Q7, Q47, Q112, Q128, WEB-3_
- **IF-4**: Form mismatches: (a) likely BPE subword fragmentation of code-switched tokens [Q128] given training corpus skew [Q112, Q120]; (b) orthographic-normalisation alignment with ZLS prescriptive standards [WEB-3] rather than the journalistic register the deployment targets. — _Sources: Q112, Q120, Q128, WEB-3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q7] 'the ongoing standardisation of the language..., vast amounts of variation..., and decentralised resources, make it extremely challenging to evaluate LTZ language understanding...' (p.1)
- [Q47] 'we removed articles identified as non-Luxembourgish by OpenLID...' (p.4)
- [Q112] 'most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts.' (p.9)
- [Q116] 'all preprocessing avoids the inclusion of directly identifying personal information.' (p.9)
- [Q128] 'a BPE-based tokenizer, which we train on the entire pre-training set, using a minimum frequency of two and a vocabulary size of 50,368.' (p.12)
- [Q129] 'both models have a max sequence length of 1024.' (p.12)

*Web sources:*
- [WEB-3] D'Lëtzebuerger Orthografie (Nov 2019) is the current ZLS-issued normative standard, anchoring LOD-grounded normalisation to formal-prescriptive conventions
- [WEB-10] Luxembourg internet penetration ~98.8%, confirming no infrastructure constraint
- [WEB-11] Eurostat household internet access 99.06% (2023)

</details>

**Information gaps:**
- Empirical analysis of LTZ-E1 BPE tokeniser behaviour on code-switched proper nouns
- Quantification of how much real newsroom orthographic variation diverges from the LOD/ZLS 2019 standard

**Requires expert verification:**
- Tokenisation audit on representative cross-border-entity newsroom snippets
- Editorial review of orthographic-variation tolerance against ZLS prescriptive forms

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Output Ontology is HIGH priority per elicitation and the evidence supports a low score on the deployment-relevant LA and HA tasks while supporting reasonable alignment on TC. The LA error taxonomy is grounded in LOD and Spellchecker.lu [Q31] — both aligned with the ZLS 2019 prescriptive standard [WEB-3] — directly contradicting the deployment's stated need for a flexible journalistic register (A3). The binary collapse [Q33] further obscures whether borderline editorial-vs-prescriptive disagreements exist in the label space. The NER tag set harmonises GPE into LOC [Q44], losing the country/administrative-region distinction that newsroom journalism covering EU institutions and the Greater Region depends on. HA labels are binary headline-body match [Q15, Q148] without an editorial-acceptability dimension. By contrast, TC's five labels [Q48, Q153] are accepted as adequate by the deployment (A1), and binary HA/RTE label conventions [Q147] are clearly documented. Intent detection's voice-assistant label set [Q154] is off-domain but irrelevant to deployment.

**Strengths:**
- TC label set explicitly accepted by the deployment team as adequate [Q48] (A1)
- Label conventions and prompt vocabularies are explicitly documented [Q147–Q155], aiding deployment integration
- NER preserves PER/ORG and adds DATE/MISC [Q44, Q152], covering most journalistic entity categories
- Binary and multi-class LA forms are both available [Q29, Q33], allowing the deployment to choose granularity

**Checklist:**

- **OO-1**: TC labels are regionally adequate (A1). LA error taxonomy [Q31] reflects formal grammatical/orthographic standards rather than editorial-register acceptability — misaligned with deployment per A3. HA labels are binary topical-match only [Q15], not editorial acceptability. — _Sources: Q15, Q31, Q48_
- **OO-2**: Missing: an 'editorially acceptable but prescriptively non-standard' middle category for LA; a GPE/country distinction in NER [Q44] that matters for cross-border journalism; a POLITICS/GOVERNMENT label in TC [Q48] (acknowledged but accepted). — _Sources: Q44, Q48_
- **OO-3**: LA taxonomy [Q31] encodes ZLS prescriptive norms [WEB-3] rather than journalistic-register norms; deployment team explicitly flags this divergence (A3). LA prompt instructs binary correctness 'in Luxembourgish' without register qualification [Q150]. — _Sources: Q31, Q150, WEB-3_
- **OO-4**: Stakeholder-driven taxonomy redesign is recommended for LA in particular: the editorial team and a formal language authority would 'plausibly disagree on borderline cases' (A3), so a multi-class scheme distinguishing prescriptive errors from register-acceptable variants would better fit deployment. — _Sources: Q31, Q33_
- **OO-5**: Documented taxonomy issues: (a) LA prescriptive grounding [Q31] vs. journalistic register (A3); (b) NER GPE/LOC merger [Q44] losing cross-border entity distinction; (c) HA construction omits editorial-acceptability dimension [Q15-Q22]; (d) intent label set targets voice-assistant domain [Q154] (irrelevant but signals porting issues). — _Sources: Q15, Q31, Q44, Q154_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'The first class interferes with the subject-verb agreement... The last class impacts the orthography, which is achieved by using data provided by Spellchecker.lu...' (p.3)
- [Q33] 'The binary dataset distinguishes between correct (1) and incorrect (0)...' (p.4)
- [Q44] 'the tag set is harmonised by merging the GPE and LOC categories into a single location label, while retaining PER, ORG, and MISC unchanged.' (p.4)
- [Q48] 'we focused on five principal domains: SPORTS, CULTURE, TECHNOLOGY, BUSINESS, and ANIMALS.' (p.4)
- [Q147] 'If determined labels are 0 and 1 then 0 is used for False, 1 is used for True.' (p.15)
- [Q150] 'linguistic_acceptability_binary: Decide whether the sentence is linguistically acceptable in Luxembourgish. Output: 0 or 1.' (p.15)
- [Q152] 'ner: ... Allowed Tags: O, B-LOC, I-LOC, B-PER,I-PER, B-DATE, I-DATE,B-ORG, I-ORG, B-MISC, I-MISC.' (p.15)
- [Q154] 'slot_intent_detection: ... Allowed intents: reminder/show_reminders, weather/find...' (p.15)

*Web sources:*
- [WEB-3] ZLS-issued D'Lëtzebuerger Orthografie (Nov 2019) is the prescriptive standard underlying the LOD and thus the LA label ontology

</details>

**Information gaps:**
- Empirical rate at which LA labels would disagree with editorial-register judgements on real newsroom copy
- Frequency of cross-border GPE entities in NER test data that the GPE/LOC merger conflates

**Requires expert verification:**
- Editorial board review of a sample of LA gold labels to estimate prescriptive-vs-editorial disagreement rate
- NER expert audit of LOC tag content for country-vs-physical-location mix

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Output Content is HIGH priority per elicitation. There is no evidence in the benchmark documentation that any HA or LA ground-truth labels were produced by professional journalists or editors; HA is algorithmically constructed via TF-IDF swapping [Q16-Q22] and LA is algorithmically generated from LOD/Spellchecker.lu manipulations [Q30, Q31]. The annotators that are documented are 'two native speakers' for SA with moderate agreement (κ=0.45) [Q25, Q27], a single LTZ native speaker (plus consultees) for ID translation [Q52], and unspecified 'student assistants' [Q114]. JUDGEWEL NER uses LLM judges with minimal human verification [Q37]; RTE relies heavily on ChatGPT-assisted post-editing and verification [Q61, Q63, Q64]. Authors explicitly acknowledge that resource constraints introduce biases that 'cannot be fully quantified' [Q113] and that data reflect institutional/media contexts with associated societal biases [Q117]. For the deployment, which targets a flexible professional-journalistic register (A3), the absence of newsroom-validated labels for HA and LA is a direct convergent-validity violation.

**Strengths:**
- Lothritz et al. NER corpus is fully human-annotated [Q40, Q42], providing one high-precision component
- Authors are transparent about annotation limitations and resource-constraint biases [Q113, Q117, Q120, Q121]
- RTE labels underwent two-stage verification [Q62-Q65], partially mitigating translation-error effects
- SA used two independent annotators with reported κ [Q25-Q28], allowing some agreement assessment

**Checklist:**

- **OC-1**: No — there is no documented evidence that ground-truth labels for HA or LA reflect professional journalist/editor perspectives; HA is algorithmic [Q16-Q22], LA is algorithmic from LOD/Spellchecker.lu [Q30, Q31]. Deployment ground truth is editorial acceptability (A3), which is not the construct labelled. — _Sources: Q16, Q22, Q30, Q31, WEB-3_
- **OC-2**: Likely substantial disagreement on LA: deployment team explicitly says editorial vs. formal-authority disagreement on borderline cases is expected (A3). For HA, the algorithmic construction guarantees only topical/temporal mismatch [Q16-Q22], not editorial unacceptability. — _Sources: Q31_
- **OC-3**: Annotator demographics are minimally documented: 'two native speakers' for SA [Q25], 'one LTZ native speaker' for ID [Q52], 'student assistants' acknowledgment [Q114], no professional-background detail. No journalist or editor involvement documented. — _Sources: Q25, Q52, Q114_
- **OC-4**: Re-annotation of HA and LA test sets by professional editorial staff is strongly recommended to align ground truth with deployment register (A3). — _Sources: Q31_
- **OC-5**: SA uses a tie-breaking aggregation by annotator agreement on disagreed labels [Q28]; with κ=0.45 [Q27] and only two annotators, minority perspectives are likely erased. RTE LLM-based verification [Q63, Q64] removes ~25% and corrects ~10% labels, embedding LLM judgement in the gold standard. — _Sources: Q27, Q28, Q37, Q63, Q64_
- **OC-6**: Documented label issues: (a) algorithmic HA ground truth without editorial validation [Q16-Q22]; (b) prescriptive-source LA ground truth misaligned with journalistic register [Q31]; (c) LLM-judge involvement in JUDGEWEL [Q37] and RTE [Q63, Q64]; (d) moderate SA agreement [Q27]; (e) unquantified resource-constraint biases [Q113]; (f) institutional-media bias acknowledgment [Q117, Q120]. — _Sources: Q22, Q31, Q37, Q63, Q113, Q117, Q120_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q16] 'To construct this dataset, we use RTL news articles. We keep only documents from the twenty most frequent categories...' (p.3)
- [Q22] 'The resulting negative examples remain topically related but are temporally and structurally mismatched, forcing models to attend to article content rather than surface cues.' (p.3)
- [Q25] 'In total, we extract 4,583 sentences, which are then annotated by two native speakers of LTZ.' (p.3)
- [Q27] 'We calculated Cohen's Kappa at 0.45.' (p.3)
- [Q30] 'The sentences are derived from the Luxembourgish Online Dictionary (LOD) and are manipulated using the tags available in the dataset.' (p.3)
- [Q31] '...by using data provided by Spellchecker.lu, a semiautomatic spellchecking website frequently used in Luxembourg.' (p.3)
- [Q37] 'The resulting sentences are then evaluated using LLMs acting as judges, with minimal human verification to calibrate quality thresholds.' (p.4)
- [Q52] 'The translations were performed by an LTZ native speaker. In cases of uncertainty, additional native LTZ speakers were consulted.' (p.4)
- [Q63] 'we prompted CHATGPT-5-MINI to judge the texts ... removing nearly 25% of the entire dataset' (p.5)
- [Q64] '...verify whether the dataset labels remained correct... Nearly 10% of the labels were false.' (p.5)
- [Q113] '...resource constraints. Certain tasks exhibit label imbalance or rely on automatic preprocessing, which may introduce biases that we cannot fully quantify.' (p.9)
- [Q114] 'We would like to thank the student assistants for their annotation work.' (p.9)
- [Q117] 'some tasks draw on data originally produced in institutional or media contexts, which may reflect societal biases in representation.' (p.10)
- [Q120] 'models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices.' (p.10)

*Web sources:*
- [WEB-3] ZLS prescriptive standards (D'Lëtzebuerger Orthografie 2019) anchor the LOD-derived LA labels to formal correctness, not editorial acceptability

</details>

**Information gaps:**
- Quantification of editorial-vs-prescriptive disagreement on real newsroom copy
- Demographic and professional profile of student-assistant annotators
- Whether any LA or HA labels were spot-checked by working journalists

**Requires expert verification:**
- Re-annotation pilot of HA and LA test subsets by professional editors to estimate label-shift rate
- Author inquiry on annotator backgrounds and any newsroom validation steps

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output Form is LOWER priority per elicitation, and the alignment is good. The benchmark evaluates F1/macro-F1 across classification tasks [Q93, Q96], which maps directly onto the deployment's per-task threshold flagging architecture (A4). Encoder results are averaged across three runs with standard deviations [Q89, Q96], providing variance information useful for threshold calibration. Class-balanced loss is applied for imbalanced LA and SA [Q92], partially addressing label imbalance. Limitations: macro-F1-only reporting for LLMs evaluated once [Q96] obscures task-level label imbalance and prompt-sensitivity effects [Q86, Q87] that would matter if the deployment uses LLMs rather than fine-tuned encoders. Malformed LLM outputs are discarded before scoring [Q90, Q91], which inflates apparent LLM performance relative to deployment realities. No per-class confusion matrices appear to be reported in the main tables, limiting threshold tuning. Modality match is strong; reporting depth is the only meaningful gap.

**Strengths:**
- F1-based classification evaluation maps directly to deployment per-task thresholding [Q93, Q96] (A4)
- Encoder results averaged over three runs with standard deviations [Q89, Q96], supporting threshold calibration
- Class-balanced loss applied for imbalanced tasks [Q92], improving label-rare-class evaluation
- Bayesian hyperparameter sweeps with multi-seed evaluation [Q137, Q138] yield reproducible numbers
- Full per-task validation and test scores are tabulated [Q156, Q158, Q159]

**Checklist:**

- **OF-1**: Output modality matches: classification labels in benchmark [Q93, Q146-Q155] and per-task scores with thresholds in deployment (A4) operate in the same paradigm. — _Sources: Q93, Q96_
- **OF-2**: TTS not required — pipeline is text-only (deployment context); no speech output requirement. — _Sources: Q116_
- **OF-3**: Target population is professional journalists with full digital infrastructure access [WEB-10, WEB-11]; literacy and accessibility constraints do not apply to the deployment context. — _Sources: WEB-10, WEB-11_
- **OF-4**: Form mismatches are minor: (a) macro-F1-only LLM reporting [Q96] hides label-imbalance effects relevant to threshold setting; (b) discarded malformed LLM outputs [Q90, Q91] inflate apparent LLM scores; (c) prompt sensitivity makes LLM scores indicative only [Q86, Q87]. — _Sources: Q86, Q90, Q91, Q96_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q86] 'prompt-based evaluation introduces additional sources of variability... performance should be interpreted as indicative rather than directly comparable to supervised results.' (p.6)
- [Q89] 'For encoder-based models, results are reported as averages over multiple runs...' (p.7)
- [Q90] 'Prompted LLMs do not always produce well-formed outputs... such outputs are discarded prior to evaluation.' (p.7)
- [Q92] '...we use class-balanced loss based on effective size... with a beta of 0.99.' (p.7)
- [Q93] 'Table 6 shows F1 scores for all models across all tasks...' (p.7)
- [Q96] 'Encoder results are averaged over three runs with standard deviations as subscripts. Prompted LLMs were evaluated once; we report macro-F1 only.' (p.8)
- [Q156] 'We show full results (validation and test set performance) for each model and task...' (p.15)

*Web sources:*
- [WEB-10] Luxembourg internet penetration ~98.8%, confirming no infrastructure constraint on text-output pipeline
- [WEB-11] Eurostat household internet 99.06% (2023), supporting no accessibility-driven form constraints

</details>

**Information gaps:**
- Per-class precision/recall and confusion matrices that would directly support threshold calibration

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Code-switched French/German/English content is not systematically represented in benchmark instances and is actively excluded from TC by OpenLID filtering.

**Recommendation:** Construct a deployment-side code-switching evaluation set from authentic newsroom copy (≥500 instances per task) preserving embedded French/German/English tokens, and report per-task F1 separately on this set as a complement to LTZGLUE scores.

### Input Content ⚠

**Gap:** RTL Lëtzebuerg dominates benchmark sources, limiting representativeness across the broader Luxembourg media landscape.

**Recommendation:** Before deployment at any non-RTL outlet, run a held-out evaluation on that outlet's own copy (drawn from production archives, with editor-validated labels) and compare per-task F1 to LTZGLUE benchmark scores to detect outlet-specific style drift.

### Output Content ⚠

**Gap:** No documented involvement of professional journalists or editors in HA or LA ground-truth labelling; LA labels reflect prescriptive correctness, not editorial acceptability.

**Recommendation:** Run a re-annotation pilot on a stratified sample (≥300 instances) of the HA and LA test sets using two professional editors per item, measure inter-annotator agreement and disagreement rates with the LTZGLUE labels, and use the re-annotated subset as the calibration anchor for deployment thresholds.

### Output Ontology ⚠

**Gap:** LA label ontology is grounded in prescriptive ZLS/LOD standards rather than the flexible journalistic register the deployment targets; NER GPE/LOC merger loses cross-border distinction.

**Recommendation:** Define a deployment-specific multi-class LA scheme distinguishing prescriptive errors from editorially-acceptable variants, and re-introduce a GPE tag (or a country/EU-institution sub-class) into the NER label set, mapping LTZGLUE NER outputs through a post-processing layer for cross-border entities.

### Input Form

**Gap:** LTZ-E1 BPE tokeniser was trained on a corpus skewed toward formal/institutional Luxembourgish, risking aggressive subword fragmentation of code-switched proper nouns.

**Recommendation:** Audit tokeniser behaviour on a sample of cross-border-entity newsroom snippets (EU institutions, French/German political figures); if fragmentation is heavy, evaluate XLM-R-base or MMBERT-base alongside LTZ-specific encoders, since [Q105] indicates MMBERT-base is the strongest overall on LTZGLUE.

### Output Form

**Gap:** Macro-F1-only reporting for LLMs and absence of per-class confusion matrices limit threshold calibration for the deployment's per-task flagging.

**Recommendation:** Re-run the deployment-targeted models on the LTZGLUE test sets to produce per-class precision/recall and confusion matrices, and use these to set per-task thresholds that explicitly trade off false-positive editorial overhead against false-negative substandard-content publication.

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
| Q41 | 4 | output_ontology | "It covers a wider range of text types and registers, including informal and code-mixed writing, and focuses on four primary entity categories (PER, ORG, LOC, GPE)." |
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
| Q56 | 5 | output_content | "Due to the lack of LTZ references in this register, it was not possible to systematically verify the translated terminology." |
| Q57 | 5 | input_form | "After translating the dataset, we transferred the BIO tags by first using token-level fuzzy matching between the LTZ and the German dataset, followed by manual verification." |
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
| Q76 | 6 | input_ontology | "We evaluate a set of supervised encoder-based models that explicitly support LTZ, either through direct pre-training or multilingual coverage." |
| Q77 | 6 | output_form | "As a representative baseline, we include multilingual BERT (MBERT-base) (Devlin et al., 2019), which still remains widely used for multilingual transfer and low-resource evaluation." |
| Q78 | 6 | output_form | "We additionally evaluate a more recent multilingual BERT (MMBERT-base) variant with updated pre-training data and tokenisation." |
| Q79 | 6 | output_form | "To complement these general-purpose multilingual models, we include LUXEMBERT, a language-specific model trained on LTZ data (Lothritz et al., 2022), which provides a stronger inductive bias for the language's lexical and orthographic properties." |
| Q80 | 6 | output_form | "Finally, we evaluate XLM-RoBERTa (XLM-R-base) (Conneau et al., 2020), a large-scale multilingual model trained on substantially more data and languages than MBERT-base, and commonly used as a strong reference point for multilingual NLU." |
| Q81 | 6 | output_form | "In addition to supervised encoder-based models, we evaluate a set of LLMs in a prompt-based zero-shot setting. This group includes QWEN3-235B, LLAMA-3.3, GEMMA-3-27B, and GPT5-MINI, which represent a range of model sizes, training regimes, and degrees of multilingual coverage." |
| Q82 | 6 | output_form | "None of these models are fine-tuned on LTZGLUE, although some of the text data (RTL, Wikipedia) is very likely to have been processed during training." |
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
| Q122 | 10 | output_content | "Finally, although no sensitive content is intentionally included, automated filtering and preprocessing cannot guarantee the complete removal of harmful or offensive material." |
| Q123 | 10 | output_content | "Researchers using LTZGLUE are encouraged to inspect task-specific subsets and consider downstream implications, especially in public-facing settings." |
| Q124 | 12 | input_ontology | "For demonstration purposes, we present an example for each task in ltzGLUE in Table 7. The examples are intended to illustrate the task formulations and typical model inputs and outputs." |
| Q125 | 12 | input_form | "We follow the Ettin recipe (Weller et al., 2026), based on ModernBERT (Warner et al., 2025), for training hyperpameters and model architecture." |
| Q126 | 12 | input_form | "We train two sizes of LTZ-E1 models, mini and base, with 68M and 110M non-embedding parameters, respectively." |
| Q127 | 12 | input_form | "LTZ-E1-mini has 19 hidden layers, a hidden size of 512, an intermediate size of 768, and 8 attention heads, whereas LTZ-E1-base has 22 hidden layers, a hidden size of 768, an intermediate size of 1152, and 12 attention heads." |
| Q128 | 12 | input_form | "Both models share a GPTNeoXTokenizerFast tokenizer (Black et al., 2022), a BPE-based tokenizer, which we train on the entire pre-training set, using a minimum frequency of two and a vocabulary size of 50,368." |
| Q129 | 12 | input_form | "We use a constant batch size of 1024 packed sequences, where both models have a max sequence length of 1024." |
| Q130 | 12 | input_form | "We follow ModernBERT (Warner et al., 2025) and Ettin (Weller et al., 2026) in using the Warmup-Stable-Decay (WSD) scheduler (Zhai et al., 2022; Hu et al., 2024), though we use a shorter warmup and decay phase of 500 batches each, due to our smaller pre-training dataset size and larger number of epochs (10 vs. one)." |
| Q131 | 12 | input_form | "Again following ModernBERT and Ettin's recipe, we use the StableAdamW optimizer (Wortsman et al., 2023), with a peak learning rate of 3e-3 with a weight decay of 3e-4 for LTZ-E1-mini and 8e-4 with a weight decay of 1e-5 for LTZ-E1-base." |
| Q132 | 12 | input_form | "As our pre-training set is small, we" |
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
| Q143 | 14 | output_ontology | "You are an expert for the Luxembourgish language. I am giving you a sentence in Luxembourgish. You have to judge its quality and improve it while keeping the meaning intact. As output, write only the improved sentence or the original sentence if it is of very high quality." |
| Q144 | 14 | output_ontology | "You are an expert for the Luxembourgish language. I am giving you two texts in Luxembourgish. You have to judge their quality. As output, simply write 'low', 'medium' or 'high' depending on the quality of both sentences, nothing else." |
| Q145 | 14 | output_ontology | "You are an expert for the Luxembourgish language. I am giving you two texts TEXT1 and TEXT2 in Luxembourgish as well as a LABEL where 1 means that TEXT1 logically entails TEXT2 while 0 means the opposite. You have to check if the labels are correct. As output, simply write 'true' if the label is the correct one or 'false' if the label is incorrect." |
| Q146 | 14 | output_form | "You are a classification and text-processing model specialized in NLP tasks for Luxembourgish (lb). Follow ALL rules strictly: 1. Respond ONLY in valid JSON. 2. Do NOT add explanations, comments or text outside of JSON. 3. Use field: "output": <model_answer>. 4. Use field: "task": "<task_name>". 5. Use field: "input": "<input example text>". 6. Predict only the requested outputs and" |
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
| WEB-1 | https://statistiques.public.lu/en/actualites/2024/stn16-population-2024.html |
| WEB-2 | https://cmpf.eui.eu/country/luxembourg/ |
| WEB-3 | https://men.public.lu/en/grands-dossiers/systeme-educatif/promotion-langue-luxembourgeoise.html |
| WEB-4 | https://data.public.lu/en/organizations/zenter-fir-dletzebuerger-sprooch/ |
| WEB-5 | https://www.press.lu/en/mediatic-landscape-in-luxembourg/editors-in-chief/ |
| WEB-6 | https://www.press.lu/en/who-we-are/composition-cdp/ |
| WEB-7 | https://www.press.lu/en/journalists/legal-texts-concerning-the-press-in-luxembourg/ |
| WEB-8 | http://zls.lu/ |
| WEB-9 | https://www.inll.lu/en/ |
| WEB-10 | https://datareportal.com/reports/digital-2026-luxembourg |
| WEB-11 | https://www.statista.com/statistics/377741/household-internet-access-in-luxembourg/ |
| WEB-12 | https://link.springer.com/content/pdf/10.1007/978-3-031-28819-7_26.pdf |
| WEB-13 | https://cms.law/en/int/expert-guides/cms-expert-guide-to-data-protection-and-cyber-security-laws/luxembourg |
| WEB-14 | https://cnpd.public.lu/en/actualites/national/2024/09/rapport-annuel-2023.html |
| WEB-15 | https://cnpd.public.lu/en.html |
| WEB-16 | https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6 |
| WEB-17 | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai |

---
