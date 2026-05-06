## Deployment Context

**Use case:** In a newsroom setting, journalists and editors use LLM-powered software to manage Luxembourgish news articles by applying a model evaluated on headline acceptability, linguistic acceptability, topic classification, and named entity recognition. The system automatically verifies grammatical standards, classifies the article’s domain, and identifies key entities to enable automatic internal linking between related news stories. These outputs determine whether a headline is logically consistent with its content and if the article can be instantly published or must be flagged for manual editorial revision to maintain professional standards.
**Target population:** Professional journalists, editors, and digital content managers at Luxembourgish media outlets who produce and curate news content in the Luxembourgish language for a local audience.

# Validity Analysis: ltzglue
**Target context:** Luxembourgish Professional Newsroom
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 3 | Moderate gaps | high |
| Input Content ⚠ | 2 | Significant gaps | medium |
| Input Form | 3 | Moderate gaps | medium |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 4 | Minor gaps | high |
| **Average** | **2.7** | | |

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

LTZGLUE is the first GLUE-style benchmark for Luxembourgish and covers all four tasks the newsroom deployment requires (HA, LA, TC, NER), with RTL — the deployment's primary outlet — as principal data source. However, three of the highest-priority deployment dimensions (IC code-switching, OO output ontology, OC annotator population) show substantial misalignment. Code-switching, a HIGH-priority operational requirement, is acknowledged as under-represented [Q112] and only the NER comment subcorpus is documented as covering it [Q41]. The LA Ortho ground truth is derived from Spellchecker.lu encoding the formal ZLS standard [Q31, WEB-11], creating systematic divergence from the deployment's flexible journalistic register [A3]. Annotators are student assistants [Q114] with low documented IAA where measured (Cohen's Kappa 0.45 for SA [Q27]) and AI-assisted labelling for RTE [Q63, Q64] and JUDGEWEL [Q37] — none professional journalists. Output form (OF) is well aligned and partially mitigates these concerns. The benchmark itself explicitly cautions against treating its scores as evidence of cultural or demographic coverage [Q120, Q121].

## Practical Guidance

### What This Benchmark Measures

LTZGLUE provides a credible first-pass evaluation of generic Luxembourgish NLU capability across the deployment's four required tasks, with strongest signal on output-form compatibility (OF), task-coverage breadth (IO, partially), and an authentic RTL-grounded text source for HA, NER, and TC. Strong encoder performance on TC and NER [Q94, Q105] suggests these tasks are reasonably tractable.

### Construct Depth

The benchmark probes surface-level NLU constructs (categorical classification, sequence labelling) but does not probe the deployment's actual ground truth — professional editorial judgment under flexible journalistic register with dense code-switching. LA in particular operationalises formal-orthographic correctness via LOD/Spellchecker [Q30, Q31] rather than journalistic acceptability; HA operationalises TF-IDF structural mismatch [Q22] rather than editorial coherence. Output Content (OC) and Output Ontology (OO) gaps mean high benchmark scores would not directly transfer to editorial-quality judgments.

### What Else You Need

To complete the assessment, the deployer should: (a) commission re-annotation of held-out HA and LA samples by professional Luxembourgish editors to address OC and OO gaps; (b) audit benchmark instances for code-switching density and supplement with a code-switched evaluation set to address the HIGH-priority IC gap; (c) re-evaluate or expand the TC taxonomy against the deploying outlet's actual editorial categories (IO); (d) reinstate GPE/LOC granularity for cross-border NER use cases (OO); (e) calibrate per-task model confidence scores against editorial flagging thresholds in a shadow-deployment phase before live auto-publication.

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The benchmark covers all four tasks the deployment requires (HA, LA, TC, NER) [Q15, Q29, Q46, Q34], and notably introduces headline acceptability as a novel contribution for Luxembourgish [Q69], directly addressing the deployment's headline-vs-body consistency need. The topic taxonomy maps to standard international news categories aligned with the deployment [Q48, A1]. However, three of the eight tasks (SA, ID, RTE) are operationally irrelevant to the newsroom pipeline, and the topic taxonomy includes ANIMALS [Q48] — an unusual inclusion whose newsroom relevance is unjustified — while plausibly missing standard newsroom categories such as POLITICS, HEALTH, and JUSTICE which Luxembourgish media routinely cover (including EU institutions and Grande Région affairs per [WEB-1]). This represents partial alignment: the required task types are present, but taxonomy gaps within TC may cause misclassification in production.

**Strengths:**
- All four deployment-required tasks (HA, LA, TC, NER) are present in the benchmark [Q15, Q29, Q46, Q34]
- Headline acceptability is purpose-built for Luxembourgish rather than ported [Q69], directly serving the deployment's headline-consistency requirement
- Topic taxonomy maps to standard international news categories, matching the deployment's stated taxonomy needs [Q48, A1]

**Checklist:**

- **IO-1**: Deployment requires HA, LA, TC, NER tasks under standard international news categories with code-switching robustness [A1, A2]; all four task types are represented in LTZGLUE [Q15, Q29, Q46, Q34]. — _Sources: Q15, Q29, Q46, Q34_
- **IO-2**: The TC label set (SPORTS, CULTURE, TECHNOLOGY, BUSINESS, ANIMALS) [Q48] omits standard newsroom beats such as POLITICS, HEALTH, JUSTICE, and LOCAL/MUNICIPAL, which are core to Luxembourgish journalism including EU institutional coverage [WEB-1]. No headline-acceptability category gap; HA is present [Q15]. — _Sources: Q48, WEB-1_
- **IO-3**: Three benchmark tasks (Sentiment Analysis [Q23], Intent Detection [Q51, Q154], Recognising Textual Entailment [Q59]) are not part of the deployment use case and would consume evaluation effort without contributing to deployment validity. The ANIMALS topic label [Q48] is an unusual inclusion whose relevance to a professional newsroom taxonomy is not justified in the documentation. — _Sources: Q23, Q51, Q59, Q48_
- **IO-4**: Category gaps within topic classification (missing POLITICS/HEALTH/JUSTICE) and inclusion of ANIMALS create content-validity concerns specifically for the TC task; the HA, LA, and NER task categories themselves are appropriate for the deployment. — _Sources: Q48, WEB-1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q15] 'We formulate headline acceptability (HA) as a binary classification task where the model must decide whether a given headline matches the accompanying article body.' (p.3)
- [Q48] 'From the available categories, we focused on five principal domains: SPORTS, CULTURE, TECHNOLOGY, BUSINESS, and ANIMALS.' (p.4)
- [Q69] 'a substantial proportion of the LTZGLUE tasks are newly created for LTZ rather than direct translations or simple repackaging' (p.5)
- [Q67] 'Together, the eight tasks in LTZGLUE form a broad and balanced evaluation suite, covering four binary and four multi-class settings' (p.5)

*Web sources:*
- [WEB-1] EU institutional politics and Greater Region cross-border affairs are core Luxembourgish news beats not represented in the five-label TC schema

</details>

**Information gaps:**
- No documentation of why ANIMALS was selected as a top-five news category; whether RTL's editorial taxonomy actually contains a comparable label is not addressed
- No documentation of category coverage for POLITICS / EU affairs in the TC training set despite their centrality to Luxembourgish journalism

**Requires expert verification:**
- Whether the deploying outlet's editorial taxonomy actually requires only the five benchmark TC labels or whether additional Luxembourg-specific beats are operationally needed

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
Code-switching is identified as a HIGH-priority deployment requirement [A2] and is a structural feature of Luxembourgish journalism [WEB-6, WEB-10]. The benchmark explicitly acknowledges that 'most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts' [Q112], and that data are concentrated in a limited set of public domains [Q119]. Only the human-annotated RTL news comment NER corpus is documented as covering 'informal and code-mixed writing' [Q41]; systematic quantification of code-switched content across the other tasks (HA, LA, TC) is absent. RTL is the principal source for HA, SA, TC, and NER comments [Q16, Q24, Q40, Q46], which aligns with the deployment's primary outlet [WEB-1], a meaningful strength. However, LA sentences are sourced from the LOD formal dictionary [Q30], RTE is machine-translated then LLM-improved [Q60, Q61], and intent detection uses German MT [Q54] — meaning much of the benchmark content is not authentic Luxembourgish journalistic text. Given code-switching is a HIGH-priority dimension for this deployment and the benchmark itself flags this as a limitation, score is 2.

**Strengths:**
- RTL — the principal Luxembourgish broadcast outlet [WEB-1] — is the dominant source for HA, SA, TC, and NER, providing strong domain alignment for the deployment's primary register [Q16, Q24, Q40, Q46]
- The RTL news comment NER subcorpus explicitly covers informal and code-mixed writing [Q41], partially addressing the deployment's code-switching need for NER
- The benchmark explicitly acknowledges its register and code-switching limitations [Q112, Q119], enabling informed deployment risk management

**Checklist:**

- **IC-1**: Yes — Luxembourgish journalism requires handling French, German, and English code-switching, EU institutional terminology, and Grande Région cross-border entities [A2, WEB-1, WEB-10]. The benchmark partially addresses this through the RTL comment NER subcorpus [Q41] but does not systematically cover code-switching across HA, LA, or TC. — _Sources: Q41, Q112, WEB-10, WEB-6_
- **IC-2**: RTL-derived content (HA, SA, TC, NER comments) [Q16, Q24, Q40, Q46] aligns with mainstream Luxembourgish journalistic culture; LA sentences from LOD [Q30] reflect formal/normative register diverging from the deployment's flexible journalistic standard [A3]. — _Sources: Q16, Q24, Q40, Q46, Q30_
- **IC-3**: Intent detection uses xSID voice-assistant commands [Q51, Q55] — a register entirely irrelevant to newsroom deployment. RTE is sourced from English-origin pairs translated and LLM-improved [Q60, Q61], introducing non-Luxembourgish provenance. — _Sources: Q51, Q55, Q60, Q61_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotator audit of code-switched coverage across the benchmark has been performed; gap_id 1 in the regional YAML remains unresolved [NEEDS VERIFICATION]. Direct dataset inspection by Luxembourgish journalism experts would be needed.
- **IC-5**: Documented content issues: (a) systematic under-representation of code-switching outside the NER comment subcorpus [Q112]; (b) LA grounded in formal LOD register [Q30] rather than journalistic register; (c) 22–28% of RTE filtered post-LLM improvement [Q66] indicating quality variance; (d) JUDGEWEL automatically constructed with minimal human verification [Q37]. — _Sources: Q112, Q30, Q66, Q37_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q41] 'It covers a wider range of text types and registers, including informal and code-mixed writing' (p.4)
- [Q112] 'most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts' (p.9)
- [Q119] 'LTZ is a small language community, and linguistic data often originate from a limited set of public domains' (p.10)
- [Q30] 'The sentences are derived from the Luxembourgish Online Dictionary (LOD) and are manipulated using the tags available in the dataset.' (p.3)
- [Q66] 'The filtering reduced between 22 and 28% of instances in the data' (p.5)
- [Q16] 'To construct this dataset, we use RTL news articles.' (p.3)

*Web sources:*
- [WEB-1] RTL leads Luxembourg's media landscape across television, radio, and web, aligning the benchmark's principal source with the deployment's primary outlet
- [WEB-10] Luxembourgish nationals speak on average 4.3 languages and 9 of 10 residents speak French, confirming code-switching as a structural feature
- [WEB-6] Luxembourg's three-language administrative regime (Law of 24 February 1984) institutionalises French/German/Luxembourgish co-occurrence in journalistic text

</details>

**Information gaps:**
- Quantified rate of French/German/English code-switching in HA, LA, and TC instances (gap_id 1, deferred)
- Whether RTL article corpus reflects only published staff articles or includes user-comment register
- Coverage of EU institutional naming conventions and Grande Région entity mentions in the NER training set

**Requires expert verification:**
- Whether code-switching density in benchmark instances matches operational density in target newsroom copy
- Whether the RTL-sourced subset reflects the same editorial register as the deploying outlet's output

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Modality alignment is good: both benchmark and deployment are text-only [Q17], RTL articles, comments, parliamentary transcripts, and chat rooms provide register diversity in pre-training [Q74], and OpenLID filtering removes non-Luxembourgish content [Q47]. The 40–400 word filter [Q47] is plausibly compatible with newsroom article lengths. However, Luxembourgish has 'ongoing standardisation' and 'vast amounts of variation' [Q7], and the documentation does not describe explicit orthographic normalisation across datasets. The BPE tokenizer (50,368 vocab on 233M tokens) [Q128, Q75] may not adequately represent journalistic orthographic variants or code-switched French/German tokens, particularly given the formal-register skew of the data [Q112]. The deployment explicitly applies the flexible journalistic register [A3], but LA Ortho ground truth is built from Spellchecker.lu data [Q31] encoding the formal ZLS standard [WEB-11, WEB-12], creating a known register mismatch.

**Strengths:**
- Text-only modality matches the deployment's text-only pipeline [Q17]
- Pre-training corpus draws from a broad set of Luxembourgish written sources including RTL news, comments, parliamentary speech, podcasts, chat rooms, and Wikipedia [Q74], providing some register breadth
- Article-length filtering (40–400 words) [Q47] is operationally compatible with newsroom article lengths

**Checklist:**

- **IF-1**: Both benchmark and deployment use plain text [Q17]; signal-distribution mismatch is low at the modality level. Tokenisation (BPE, 50,368 vocab on 233M tokens) [Q128, Q75] may under-represent journalistic orthographic variants and code-switched tokens. — _Sources: Q17, Q128, Q75_
- **IF-2**: Luxembourg has near-universal digital infrastructure (98.8% internet penetration [WEB-17]), so capture infrastructure is not a constraint. — _Sources: WEB-17_
- **IF-3**: The benchmark filters articles to 40–400 words [Q47] and removes non-Luxembourgish content via OpenLID [Q47] — both operationally plausible for newsroom text. However, no explicit orthographic normalisation across datasets is documented despite acknowledged 'vast amounts of variation' [Q7], and the LA Ortho category encodes the ZLS formal standard via Spellchecker.lu [Q31, WEB-11] which diverges from the deployment's flexible journalistic register [A3]. — _Sources: Q47, Q7, Q31, WEB-11, A3_
- **IF-4**: Form-level mismatches that may harm external validity: (a) tokenisation potentially mis-segmenting code-switched and orthographically variant tokens; (b) implicit assumption of formal orthography in LA Ortho ground truth diverging from journalistic practice [A3, Q31]. — _Sources: Q31, Q7_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q17] 'This subset is split equally, with one half serving as the positive class with original headlines, and the other half providing the article bodies for which we assign swapped headlines.' (p.3)
- [Q7] 'the ongoing standardisation of the language (Gilles, 2019), vast amounts of variation (Lutgen et al., 2025), and decentralised resources, make it extremely challenging to evaluate LTZ language understanding' (p.1)
- [Q47] 'we removed articles identified as non-Luxembourgish by OpenLID (Burchell et al., 2023), as well as those containing fewer than 40 words or more than 400 words.' (p.4)
- [Q74] 'A large portion of the data stems from RTL ... transcribed podcasts (Podcasts) ... transcribed political speeches and debates from the Chambre des Députés (Chamber). In addition, we use 1M sentences from the web crawl of the Leipzig Collection ... text crawled from LTZ chat rooms (Webchat), a Wikipedia crawl ...' (p.6)
- [Q128] 'a BPE-based tokenizer, which we train on the entire pre-training set, using a minimum frequency of two and a vocabulary size of 50,368.' (p.12)

*Web sources:*
- [WEB-17] 98.8% internet penetration in Luxembourg confirms enterprise-grade digital infrastructure for newsroom deployment
- [WEB-11] ZLS sets the official orthographic standard (November 2019) and maintains Spellchecker.lu — the LA Ortho category's data source — anchoring it in formal rather than journalistic orthography

</details>

**Information gaps:**
- Whether explicit orthographic normalisation was applied across datasets (gap_id 3, partially resolved — formal-source inputs confirmed but normalisation across datasets undocumented)
- Tokenizer behaviour on code-switched and orthographically variant tokens

**Requires expert verification:**
- Whether the BPE tokenizer adequately segments code-switched newsroom copy

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The output label structure is appropriate for the deployment's per-task classification paradigm [Q84, A4], and headline acceptability binary (True/False) [Q148] and TC's category labels [Q153] map cleanly to editorial use. However, several output-ontology features misalign with deployment needs (HIGH priority): (a) LA Multi exposes formally-derived linguistic error categories (Verb, Adj, Syntax, Ortho) [Q31, Q151] grounded in the LOD/Spellchecker formal standard, while the deployment explicitly applies a flexible journalistic register [A3] — the Ortho category in particular may penalise legitimate journalistic variants; (b) the GPE→LOC merge [Q44] reduces granularity for cross-border journalism that needs to distinguish municipalities, regions, and countries [WEB-1, regional YAML]; (c) the ANIMALS topic label [Q48] encodes a non-newsroom assumption; (d) intent detection's xSID schema [Q154] is operationally irrelevant. The benchmark explicitly cautions against using performance as evidence of cultural/demographic coverage [Q121].

**Strengths:**
- Label-output (not MCQA) paradigm [Q84] mirrors the deployment's per-task classification with valid label sets, matching the deployment's per-task scoring pipeline [A4]
- HA binary True/False [Q148] directly maps to the deployment's headline-flagging logic
- TC label set covers standard international news categories aligned with the deployment's editorial taxonomy [Q153, A1]

**Checklist:**

- **OO-1**: HA [Q148] and TC [Q153] labels align with deployment needs. NER tags (LOC/PER/ORG/MISC/DATE) [Q152] are appropriate categories but the GPE→LOC merge [Q44] is regionally suboptimal. LA Multi categories [Q151] encode formal linguistic error types divergent from the deployment's journalistic register [A3]. — _Sources: Q148, Q153, Q152, Q44, Q151_
- **OO-2**: GPE has been merged into LOC [Q44], removing a category Luxembourgish cross-border journalism plausibly needs to distinguish (municipalities vs. countries vs. geographic regions), per regional YAML and [WEB-1]. No journalist-register acceptability category exists. — _Sources: Q44, WEB-1_
- **OO-3**: The LA Ortho category [Q31, Q151] encodes Spellchecker.lu's formal ZLS standard [WEB-11], which represents non-deployment values (formal orthographic correctness) rather than the editorial register the deployment applies [A3]. The ANIMALS TC label [Q48] reflects an editorial assumption inherited from RTL's category structure rather than universally newsroom-relevant. — _Sources: Q31, Q151, Q48, WEB-11_
- **OO-4**: Stakeholder-driven taxonomy redesign is warranted for LA Multi (to recognise journalistically-acceptable variants) and for TC (to evaluate whether ANIMALS is needed and whether POLITICS / EU coverage labels should be added) given HIGH OO priority weight. — _Sources: Q31, Q48, Q44_
- **OO-5**: Documented taxonomy issues: (a) LA Ortho derived from formal-standard Spellchecker.lu [Q31] vs. flexible journalistic register [A3]; (b) GPE→LOC merge [Q44] vs. cross-border granularity needs; (c) ANIMALS label [Q48] vs. standard newsroom beats; (d) intent detection schema [Q154] irrelevant to deployment. — _Sources: Q31, Q44, Q48, Q154_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'The first class interferes with the subject-verb agreement ... The last class impacts the orthography, which is achieved by using data provided by Spellchecker.lu' (p.3)
- [Q44] 'the tag set is harmonised by merging the GPE and LOC categories into a single location label' (p.4)
- [Q48] 'we focused on five principal domains: SPORTS, CULTURE, TECHNOLOGY, BUSINESS, and ANIMALS.' (p.4)
- [Q84] 'We did not use a Multiple Choice Question Answering (MCQA)-setup, but provided the labels that should be used as output.' (p.6)
- [Q148] 'headline_classification: Decide if the given title/headline fits the text. Output True or False.' (p.15)
- [Q121] 'We therefore caution against using benchmark performance as evidence of cultural or demographic coverage.' (p.10)

*Web sources:*
- [WEB-11] ZLS established by Law of 20 July 2018; maintains Spellchecker.lu encoding the November 2019 formal orthographic standard — the source of LA Ortho ground-truth labels
- [WEB-1] Luxembourgish news routinely covers cross-border (Belgian, French, German) entities, motivating GPE/LOC granularity

</details>

**Information gaps:**
- Whether LA Ortho ground-truth labels would survive review by professional Luxembourgish editors applying journalistic register
- Whether the deploying outlet's NER schema requires the GPE/LOC distinction

**Requires expert verification:**
- Editorial review of a sample of LA Ortho instances against journalistic-register standards
- Editorial confirmation of the operational TC taxonomy

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Annotator-population mismatch is the highest-confidence concern in this analysis. Sentiment analysis annotation achieved Cohen's Kappa of only 0.45 [Q27] — below the 0.60–0.80 range typical for robust NLU annotation — with disagreements resolved by annotators agreeing among themselves [Q28]. Annotators beyond SA are described as 'student assistants' [Q114]; no evidence of professional journalist or editor involvement, despite the deployment explicitly requiring journalistic-register ground truth [A3]. RTE labels are AI-assisted (ChatGPT-5.1 improvement [Q61], ChatGPT-5-MINI quality and label verification [Q63, Q64]), with manual correction only where the LLM altered semantics [Q65]. JUDGEWEL NER uses LLMs as judges with minimal human verification [Q37]. The benchmark itself warns 'models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices' [Q120]. Given OC is a HIGH-priority dimension and the deployment requires journalist-register ground truth, score is 2.

**Strengths:**
- The Lothritz et al. (2022) RTL NER subcorpus is fully human-annotated and high-precision [Q40, Q42]
- RTE labels underwent two-stage AI verification with manual correction where semantics drifted [Q62, Q65], offering some quality control
- The benchmark explicitly cautions deployers against treating performance as cultural/demographic coverage [Q121], enabling informed risk assessment

**Checklist:**

- **OC-1**: Ground-truth labels do not reflect professional Luxembourgish journalist/editor perspectives. The deployment requires the flexible journalistic register [A3], but annotators are described as student assistants [Q114] with no documented journalism background; LA labels derive from formal LOD/Spellchecker sources [Q30, Q31] and RTE labels are AI-assisted [Q63, Q64]. — _Sources: Q114, Q30, Q31, Q63, Q64, WEB-11_
- **OC-2**: Likely substantial disagreement between benchmark annotators and the target population (working journalists/editors), particularly on borderline LA Ortho cases [A3] where the deployment explicitly anticipates formal-vs-journalistic disagreement. — _Sources: Q31, WEB-11_
- **OC-3**: Annotator demographics: SA was annotated by two native Luxembourgish speakers [Q25] with Cohen's Kappa 0.45 [Q27]; intent translation by one native speaker with consultation [Q52]; other tasks by 'student assistants' [Q114]. No professional-journalist annotators documented; no Datasheet-level demographic breakdown provided. — _Sources: Q25, Q27, Q52, Q114_
- **OC-4**: Re-annotation of LA, HA, and a sample of NER by professional Luxembourgish editors applying the deployment's flexible register would be necessary to establish convergent validity for the deployment. — _Sources: Q114, Q31_
- **OC-5**: SA disagreements resolved by annotators agreeing among themselves [Q28] — a consensus aggregation that erases minority annotator perspectives without documented arbitration. Cohen's Kappa 0.45 [Q27] indicates substantial baseline disagreement subsequently flattened. — _Sources: Q27, Q28_
- **OC-6**: Documented label issues likely to harm convergent and external validity: (a) student-annotator pool [Q114] vs. professional-journalist target users [A3]; (b) AI-assisted RTE labels [Q63, Q64]; (c) LLM-as-judge JUDGEWEL [Q37]; (d) low SA IAA [Q27]; (e) explicit benchmark caution against demographic-coverage claims [Q120, Q121]. — _Sources: Q114, Q63, Q64, Q37, Q27, Q120, Q121_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'In total, we extract 4,583 sentences, which are then annotated by two native speakers of LTZ.' (p.3)
- [Q27] 'We calculated Cohen's Kappa at 0.45.' (p.3)
- [Q28] 'For the final set, the annotators agree on a label in cases of label disagreement.' (p.3)
- [Q37] 'The resulting sentences are then evaluated using LLMs acting as judges, with minimal human verification to calibrate quality thresholds.' (p.4)
- [Q63] 'we prompted CHATGPT-5-MINI to judge the texts in the improved data and label their quality as either low, medium, or high' (p.5)
- [Q64] 'we prompted CHATGPT-5-MINI to verify whether the dataset labels remained correct' (p.5)
- [Q114] 'We would like to thank the student assistants for their annotation work.' (p.9)
- [Q120] 'models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices.' (p.10)
- [Q121] 'We therefore caution against using benchmark performance as evidence of cultural or demographic coverage.' (p.10)

*Web sources:*
- [WEB-11] LA Ortho is anchored in Spellchecker.lu which encodes the formal ZLS standard, structurally divorced from the journalistic register the deployment applies

</details>

**Information gaps:**
- Number, demographics, and journalism background of student annotators
- Whether any IAA was computed for tasks other than SA
- Adjudication procedure when SA annotators initially disagreed

**Requires expert verification:**
- Disagreement rate between professional Luxembourgish editors and benchmark labels on a held-out sample, especially for LA Ortho and HA

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output form aligns well with deployment needs (LOWER priority dimension). All tasks produce discrete label outputs evaluated by macro-F1 [Q93, Q96], directly compatible with the deployment's per-task significance-score-and-threshold pipeline [A4]. Encoder results are averaged over three runs with reported standard deviations [Q89, Q96], enabling stability assessment. The label-output (not MCQA) paradigm [Q84] mirrors the deployment's classification framing. Class-imbalanced tasks use class-balanced loss [Q92]. Caveats: LLM outputs failing label format are discarded [Q90], inflating reported scores; LLMs are evaluated only once with macro-F1 only [Q96] — meaning LLM performance is less stable, and the benchmark itself flags this as 'indicative rather than directly comparable' [Q86]. The deployment's threshold-flagging logic [A4] requires confidence scores per task, which encoder fine-tuning supports natively but prompted LLM evaluation may not.

**Strengths:**
- Discrete label outputs evaluated by macro-F1 [Q93, Q96] directly support the deployment's per-task threshold flagging [A4]
- Encoder results averaged over three runs with standard deviations [Q89, Q96] permit stability assessment for production deployment
- Class-balanced loss applied to imbalanced tasks (LA, SA) [Q92] addresses real distributional skew
- Label-output paradigm rather than MCQA [Q84] matches the deployment's classification framing

**Checklist:**

- **OF-1**: Discrete label outputs [Q93, Q148, Q149, Q150, Q151, Q152, Q153] match the deployment's per-task scoring needs [A4]; the deployment's threshold flagging is a downstream wrapper compatible with macro-F1 evaluation. — _Sources: Q93, Q96, Q148, Q152, Q153_
- **OF-2**: Not applicable — deployment is text-only [deployment_modality]; speech output is not required.
- **OF-3**: Target users are professional journalists/editors with high literacy and trilingual proficiency [WEB-14, WEB-15]; no accessibility constraints introduced by the output form. — _Sources: WEB-14, WEB-15_
- **OF-4**: Minor mismatches: (a) prompted LLM scores are single-run macro-F1 [Q96] less directly comparable to encoder runs [Q86]; (b) discarded malformed LLM outputs [Q90] inflate apparent performance — relevant if the deployment uses prompted LLMs rather than fine-tuned encoders. — _Sources: Q90, Q96, Q86_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q84] 'We did not use a Multiple Choice Question Answering (MCQA)-setup, but provided the labels that should be used as output.' (p.6)
- [Q86] 'prompt-based evaluation introduces additional sources of variability ... performance should be interpreted as indicative rather than directly comparable to supervised results.' (p.6)
- [Q89] 'For encoder-based models, results are reported as averages over multiple runs' (p.7)
- [Q90] 'such outputs are discarded prior to evaluation.' (p.7)
- [Q92] 'we use class-balanced loss based on effective size (Cui et al., 2019) with a beta of 0.99.' (p.7)
- [Q96] 'Encoder results are averaged over three runs with standard deviations as subscripts. Prompted LLMs were evaluated once; we report macro-F1 only.' (p.8)

*Web sources:*
- [WEB-14] Luxembourg trilingual education system produces newsroom professionals with high literacy in Luxembourgish/French/German plus English
- [WEB-15] EU Education and Training Monitor confirms strong language education context for target users

</details>

**Information gaps:**
- Whether confidence scores from fine-tuned encoders are well-calibrated for the deployment's threshold-based flagging logic

**Requires expert verification:**
- Calibration of model confidence outputs against editorial flagging thresholds in production

---

## Remediation Suggestions

### Output Content ⚠

**Gap:** Annotators are student assistants [Q114] with no professional journalism background; SA Cohen's Kappa 0.45 [Q27] is below typical thresholds; RTE and JUDGEWEL labels are AI-assisted [Q37, Q63, Q64]

**Recommendation:** Re-annotate held-out HA and LA test sets with at least three professional Luxembourgish editors applying explicit journalistic-register guidelines; report IAA and adjudication procedure

### Input Content ⚠

**Gap:** Code-switching density across HA, LA, and TC tasks is undocumented; only the NER comment subcorpus explicitly covers code-mixed text [Q41, Q112]

**Recommendation:** Sample 200–500 instances per task and label code-switched tokens; commission a code-switched evaluation supplement drawn from RTL articles to quantify performance under realistic French/German/English mixing

### Output Ontology ⚠

**Gap:** LA Ortho ground truth derived from Spellchecker.lu / formal ZLS standard [Q31, WEB-11] diverges from the deployment's flexible journalistic register [A3]

**Recommendation:** Either drop the Ortho subclass for production scoring or remap it against an editorial style guide; involve the deploying outlet's chief sub-editor in defining what counts as an unacceptable orthographic variant

### Output Ontology ⚠

**Gap:** GPE has been merged into LOC [Q44], reducing granularity for Luxembourgish cross-border journalism that needs to distinguish municipalities, regions, countries, and EU institutions [WEB-1]

**Recommendation:** Restore the GPE/LOC distinction in a deployment-specific NER schema and supplement training data with annotated EU institutional and Grande Région entity examples

### Input Form

**Gap:** No explicit orthographic normalisation across datasets despite acknowledged 'vast amounts of variation' [Q7]; tokenizer behaviour on code-switched and orthographically variant tokens is undocumented [Q128]

**Recommendation:** Profile the BPE tokenizer's handling of code-switched French/German tokens and journalistic orthographic variants on a sample of newsroom copy; consider tokenizer extension or fine-tuning if fragmentation rates are high

### Input Ontology

**Gap:** TC label set (SPORTS, CULTURE, TECHNOLOGY, BUSINESS, ANIMALS) [Q48] omits standard newsroom beats (POLITICS, HEALTH, JUSTICE, LOCAL/MUNICIPAL) and includes ANIMALS without operational justification

**Recommendation:** Audit the deploying outlet's actual editorial taxonomy and either retrain TC against that taxonomy or document mappings/exclusions; verify whether ANIMALS aligns with any operational category

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This paper presents LTZGLUE, the first Natural Language Understanding (NLU) benchmark for Luxembourgish (LTZ) based on the popular GLUE benchmark for English." |
| Q2 | 1 | input_ontology | "Our tasks include common natural language processing tasks in binary and multi-class classification settings, including named entity recognition, topic classification, and intent classification." |
| Q3 | 1 | output_form | "We evaluate various pre-trained language models for LTZ to present an overview of the current capabilities of these models on the LTZ language." |
| Q4 | 1 | input_content | "Small and under-researched languages are particularly difficult to evaluate, as is the case with Luxembourgish (LTZ), the national language of Luxembourg, with around 400k speakers." |
| Q5 | 1 | input_content | "LTZ only has a handful of NLU tasks available (Lothritz et al., 2022; Philippy et al., 2024; Plum et al., 2026)." |
| Q6 | 1 | input_content | "As most of these are in the news domain, and the majority of the down-stream tasks comprise less than a thousand instances, model evaluation is not always dependable." |
| Q7 | 1 | input_form | "Additional factors, such as the ongoing standardisation of the language (Gilles, 2019), vast amounts of variation (Lutgen et al., 2025), and decentralised resources, make it extremely challenging to evaluate LTZ language understanding in language models." |
| Q8 | 1 | input_ontology | "Our contributions are: (1) LTZGLUE: the first unified GLUE benchmark for LTZ, with 8 tasks." |
| Q9 | 1 | input_ontology | "(2) LTZ-E1 (mini/base): 2 new encoder language models for LTZ, which achieve competitive performance when fine-tuned on LTZGLUE." |
| Q10 | 1 | input_content | "Alistair Plum1, Felicia Körner2,3, Anne-Marie Lutgen1, Laura Bernardy1, Fred Philippy1, Emilia Milano1, Nils Rehlinger1, Cédric Lothritz4, Tharindu Ranasinghe5, Barbara Plank2,3, Christoph Purschke1 1University of Luxembourg, Luxembourg, 2LMU Munich, Germany 3Munich Center for Machine Learning, Germany 4LIST, Luxembourg, 5Lancaster University, UK" |
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
| Q22 | 3 | input_content | "The resulting negative examples remain topically related but are temporally and structurally mismatched, forcing models to attend to article content rather than surface cues." |
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
| Q35 | 4 | output_ontology | "Using Wikipedia's hyperlink structure, entities are matched to their corresponding Wikidata types and labelled in BIO format." |
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
| Q76 | 6 | output_form | "We evaluate a set of supervised encoder-based models that explicitly support LTZ, either through direct pre-training or multilingual coverage." |
| Q77 | 6 | output_form | "As a representative baseline, we include multilingual BERT (MBERT-base) (Devlin et al., 2019), which still remains widely used for multilingual transfer and low-resource evaluation." |
| Q78 | 6 | output_form | "We additionally evaluate a more recent multilingual BERT (MMBERT-base) variant with updated pre-training data and tokenisation." |
| Q79 | 6 | output_form | "To complement these general-purpose multilingual models, we include LUXEMBERT, a language-specific model trained on LTZ data (Lothritz et al., 2022), which provides a stronger inductive bias for the language's lexical and orthographic properties." |
| Q80 | 6 | output_form | "Finally, we evaluate XLM-RoBERTa (XLM-R-base) (Conneau et al., 2020), a large-scale multilingual model trained on substantially more data and languages than MBERT-base, and commonly used as a strong reference point for multilingual NLU." |
| Q81 | 6 | output_form | "In addition to supervised encoder-based models, we evaluate a set of LLMs in a prompt-based zero-shot setting. This group includes QWEN3-235B, LLAMA-3.3, GEMMA-3-27B, and GPT5-MINI, which represent a range of model sizes, training regimes, and degrees of multilingual coverage." |
| Q82 | 6 | output_content | "None of these models are fine-tuned on LTZGLUE, although some of the text data (RTL, Wikipedia) is very likely to have been processed during training." |
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
| Q115 | 9 | input_content | "This work is supported by the LLMs4EU project, funded by the European Union through the Digital Europe Programme (DIGITAL) under the grant agreement 10119847. FK and BP are supported by the ERC Consolidator Grant DIALECT 101043235." |
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
| WEB-1 | https://media-ownership.eu/2023-edition/findings/countries/luxembourg/ |
| WEB-2 | https://delano.lu/article/paperjam-leads-monthly-luxembo |
| WEB-3 | https://rsf.org/en/country/luxembourg |
| WEB-4 | https://www.press.lu/en/mediatic-landscape-in-luxembourg/editors-in-chief/ |
| WEB-5 | https://www.justarrived.lu/en/medias-telecommunications-luxembourg/medias/ |
| WEB-6 | https://en.wikipedia.org/wiki/Languages_of_Luxembourg |
| WEB-7 | https://en.wikipedia.org/wiki/Luxembourgish |
| WEB-8 | https://en.wikipedia.org/wiki/Demographics_of_Luxembourg |
| WEB-9 | https://statistiques.public.lu/en/recensement/diversite-linguistique.html |
| WEB-10 | https://en.paperjam.lu/article/delano_23-lux-residents-speak-4-or-more-languages |
| WEB-11 | https://data.public.lu/en/organizations/zenter-fir-dletzebuerger-sprooch/ |
| WEB-12 | https://men.public.lu/en/grands-dossiers/systeme-educatif/promotion-langue-luxembourgeoise.html |
| WEB-13 | https://www.cpll.lu/ |
| WEB-14 | https://men.public.lu/en/systeme-educatif/langues-ecole-luxembourgeoise.html |
| WEB-15 | https://op.europa.eu/webpub/eac/education-and-training-monitor/en/country-reports/luxembourg.html |
| WEB-16 | https://en.wikipedia.org/wiki/Education_in_Luxembourg |
| WEB-17 | https://www.theglobaleconomy.com/Luxembourg/Internet_users/ |
| WEB-18 | https://www.statista.com/statistics/377741/household-internet-access-in-luxembourg/ |
| WEB-19 | https://www.press.lu/en/journalists/legal-texts-concerning-the-press-in-luxembourg/ |
| WEB-20 | https://smc.gouvernement.lu/fr/legislation/medias.html |
| WEB-21 | https://www.dlapiper.com/en/insights/publications/2025/10/newsflash-draft-bill-n8625 |
| WEB-22 | https://cnpd.public.lu/fr/actualites/international/2024/07/ai-act.html |
| WEB-23 | https://cms.law/en/int/expert-guides/ai-regulation-scanner/luxembourg |
| WEB-24 | https://www.chd.lu/en/node/3016 |
| WEB-25 | https://www.nortonrosefulbright.com/en-lu/knowledge/publications/a473a1c1/artificial-intelligence-regulation |
| WEB-26 | https://newspapersonline.com/luxembourg-newspapers-online/ |
| WEB-27 | https://luxtoday.lu/en/luxembourg-en/luxembourg-modernises-media-law |

---

