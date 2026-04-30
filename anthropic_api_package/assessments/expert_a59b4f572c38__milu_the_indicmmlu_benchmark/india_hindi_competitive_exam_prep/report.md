## Deployment Context

**Use case:** Deployment scenario: A Hindi-speaking student in India is testing his/her preparation for competitive job-related examinations, with an AI system providing feedback on their responses. The goal is to evaluate the applicability of the benchmark and the quality of the LLM’s feedback.

Domain: Educational assessment
Setting: Mobile application / enterprise software

Note: The deployment hypothesis should be tested using Hindi-language sentences from the benchmark, as I am familiar with the language and can provide evaluation in a subsequent stage.
**Target population:** A graduate student in North India interacting in the Hindi language. The student has completed their education primarily in Hindi, with limited exposure to English.

# Validity Analysis: milu
**Target context:** Hindi-Medium Competitive Exam Aspirants — North India (Central Exams)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 3 | Moderate gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content | 2 | Significant gaps | medium |
| Output Form ⚠ | 1 | Serious concern | high |
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

MILU is a serious, India-grounded benchmark whose taxonomy and content provide partial coverage of the priority subjects (Polity, History, Economy, Hindi grammar, even UPSC-style Ethics) for North-India Hindi-medium central-exam aspirants, with empirical confirmation of meaningful regional content (UP, Rajasthan items) in the actual Hindi data. However, for THIS deployment its validity is severely constrained by three structural issues: (1) MILU evaluates only MCQ label accuracy [Q55, Q85] while the deployment requires a Hindi-language explanatory rationale [elicitation Q3] — a fundamental output-ontology and output-form mismatch confirmed by the absence of any rationale field in the dataset; (2) the observed Hindi validation sample is 100% machine-translated [Limitation #1] and contains English-vocabulary items mislabeled as Hindi content [DATASET-D40–D42], inflating construct-irrelevant variance for Hindi-medium students; (3) Current Affairs items are dated 2018–2022 [DATASET-D19–D22], making MILU stale on a heavily-weighted UPSC topic. Strengths in input ontology and partial regional content do not compensate for the output-side gaps. MILU can serve as a partial diagnostic for MCQ knowledge in History/Polity/Economy in Hindi, but cannot validate the deployment's primary product (Hindi rationale quality) at all.

## Practical Guidance

### What This Benchmark Measures

MILU provides domain- and subject-level MCQ accuracy scores in Hindi that meaningfully probe Indian Polity/Constitution, Indian History (ancient/medieval/modern), Indian Economy, Hindi grammar, and a sampling of UPSC-style ethics scenarios — all priority areas for the deployment. Logical Reasoning and Quantitative Aptitude are partially captured under Science and Business Studies domains. Strongest dimensions are input form (text-only Hindi MCQs match the deployment modality) and input ontology (Indian-exam-grounded taxonomy with confirmed empirical coverage of priority subjects).

### Construct Depth

The construct depth is shallow for the deployment's actual task. MILU measures a model's ability to select the correct MCQ option in Hindi, but provides zero evidence on whether the model can produce factually accurate, fluent, or pedagogically appropriate Hindi explanations — which is what the deployed app actually delivers. Within the MCQ scope, depth is also limited: no separation of central-exam vs. state-PSC items, no Current Affairs currency mechanism, mixed translation-induced register risk, and weakest model performance reported precisely in the deployment's priority cultural domains [Q6, Q71].

### What Else You Need

(1) Build or commission a Hindi rationale-quality evaluation rubric covering factual accuracy, fluency in Manak Hindi, pedagogical clarity, and code-mixing ceiling — directly addressing the OO/OF gaps [WEB-14 confirms no off-the-shelf option]. (2) Construct a current-affairs evaluation harness with rolling 12-month Indian GK content to address the staleness gap [DATASET-D19–D22]. (3) Filter the MILU Hindi subset to remove specialist Engineering/programming items, English-vocabulary items, and South India-specific items not in central-exam scope [DATASET-D31–D42] before computing deployment-relevant accuracy. (4) Recruit Hindi-medium central-exam coaching experts to spot-validate at least 200 items and to produce a small gold-standard rationale set.

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
MILU's 8-domain, 41-subject taxonomy was designed around Indian competitive exam content [Q22, Q42] and meaningfully overlaps with the deployment's priority subjects: Polity (Law & Governance), History (Social Sciences/Arts & Humanities), Economy (Business Studies), and GK. Dataset analysis empirically confirms strong representation of UPSC-relevant Polity, History, Economy, Hindi grammar, and even UPSC-style Ethics scenarios. However, MILU's macro-domain taxonomy does not separately enumerate Mathematics/Quantitative Aptitude, Logical Reasoning, or Current Affairs as named categories — three of the deployment's HIGH-priority subject areas for SSC/banking and UPSC CSAT. Dataset analysis partially mitigates this concern (reasoning items appear under Science domain, arithmetic under Business Studies), but pooling across MILU's 40+ exam types [Q27] means central-exam vs. state-PSC items are not separable, and the sample also reveals significant construct-irrelevant content (specialist Engineering/FORTRAN, South India–specific items) that is irrelevant to UPSC/SSC/banking syllabi.

**Strengths:**
- Indian-exam-grounded taxonomy with explicit cultural subjects (local history, arts, festivals, laws) [Q12, Q42]
- Empirical coverage of Polity, History, Economy, Hindi grammar, and UPSC-style ethics confirmed in the Hindi validation split [DATASET-D1, D2, D9, D56]
- Reasoning and quantitative content present in actual data despite not being named macro-domains [DATASET-D13, D15, D17, D18]

**Checklist:**

- **IO-1**: Required categories per elicitation Q1: GK, Current Affairs, History, Mathematics/Reasoning, Polity, Hindi proficiency. MILU's taxonomy [Q42] explicitly covers History/Polity/GK domains; Mathematics/Reasoning and Current Affairs are not named macro-domains but appear empirically in data [DATASET-D13–D18, D19–D22]. — _Sources: Q42, WEB-9, WEB-10, WEB-15_
- **IO-2**: Mathematics/Quantitative Aptitude, Logical Reasoning, and Current Affairs are not enumerated in the 8-domain taxonomy [Q42]; this is a documented partial gap, mitigated by empirical presence of reasoning/arithmetic items in the Hindi split [DATASET-D13, D15, D16, D17, D18]. — _Sources: Q42, DATASET-D13, DATASET-D15, DATASET-D16, DATASET-D17_
- **IO-3**: Sample contains significant Engineering & Technology specialist content (DC motors, FORTRAN, AM/FM modulation, rectifiers) outside UPSC/SSC/banking syllabi [DATASET-D35, D36, D37, D38]; this is construct-irrelevant variance for the deployment. — _Sources: DATASET-D35, DATASET-D36, DATASET-D37, DATASET-D38, DATASET-D31, DATASET-D32_
- **IO-4**: Pooling of 40+ exam types [Q27] across national and state levels [Q92] without published per-tier breakdown means central-exam items cannot be isolated; this harms content validity for a central-exam-only deployment. — _Sources: Q27, Q92_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge.' (p.3)
- [Q27] 'Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years.' (p.3)
- [Q42] 'we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies.' (p.4)

*Web sources:*
- [WEB-9] UPSC Prelims subject weightage analysis (Current Affairs, History, Polity, Geography, Economy, Environment each 10–25 questions)
- [WEB-10] SSC CGL Tier 1 covers General Intelligence/Reasoning, General Awareness, Quantitative Aptitude, English Comprehension
- [WEB-15] UPSC CSAT Paper 2 covers Quantitative Aptitude and Logical Reasoning

*Dataset analysis:*
- DATASET-D1, D2, D3, D5, D6: Strong Polity/Constitution coverage (Mandamus, 44th Amendment, voting age, Panchayati Raj)
- DATASET-D9, D10, D11, D50, D52: Medieval and modern Indian history items aligned with UPSC syllabus
- DATASET-D13, D14, D17, D18: Logical reasoning items (series, syllogism, seating) present in data despite no named taxonomy category
- DATASET-D15, D16: Quantitative aptitude (interest, averages) present under Business Studies domain
- DATASET-D35, D36, D37, D38: Specialist engineering/programming content irrelevant to UPSC/SSC/banking
- DATASET-D31, D32, D33, D34: South India–specific items (Pandya, Tamil cartoons, Telangana) of low priority for North India central-exam focus

</details>

**Information gaps:**
- Proportion of MILU Hindi items sourced from central exams (UPSC/SSC/banking) vs. state PSCs is not published
- Item-level breakdown of Current Affairs vs. timeless GK is unavailable

**Requires expert verification:**
- Whether the empirical density of reasoning and quantitative items in the full Hindi test split is sufficient for SSC/banking evaluation

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Input content is the HIGH-priority dimension per elicitation. MILU's documented sourcing from real Indian exam papers [Q24, Q25] and explicit India-first design [Q11] provide a strong foundation, and the dataset analysis confirms genuine North India regional content (UP minerals, Chikankari, Rajasthan literacy/geography, Kota painting) [DATASET-D23, D25, D27, D28, D29]. However, the dataset analysis surfaces several CRITICAL/MAJOR content-validity violations specific to this Hindi-medium central-exam deployment: (a) 100% of the 245 Hindi validation samples are flagged is_translated=True [Limitation #1], far exceeding the documented ~25% overall translation rate [Q47] and creating high risk of unnatural Hindi register from GPT-4O translation [Q44, Q45]; (b) English-vocabulary questions ('grim', 'didactic', 'Evangelize') are mislabeled as Hindi Language Studies content [DATASET-D40, D41, D42], directly violating the elicitation's 10% code-mixing ceiling for English-medium conventions; (c) Current Affairs items are dated 2018–2022 [DATASET-D19, D20, D21, D22], creating staleness for 2025–2026 aspirants — a documented benchmark limitation since MILU has no currency mechanism; (d) significant South India–specific content (Telangana, Tamil) and specialist engineering items appear in the Hindi pool, diluting deployment relevance.

**Strengths:**
- Source provenance from actual competitive exam papers via online portals [Q24, Q25, Q26]
- Explicit India-first design with culturally relevant subjects [Q11, Q12]
- Empirical North India regional content present (UP, Rajasthan items) [DATASET-D23, D25, D27, D28, D29]
- UPSC-style Ethics scenario question type captured [DATASET-D56]

**Checklist:**

- **IC-1**: Yes — central exams require both pan-India GK and North India sub-regional knowledge per elicitation Q2; dataset confirms partial regional coverage [DATASET-D23, D28] but Chhath Puja, zamindari, and key North Indian freedom fighters were not observed in the sample. — _Sources: Q11, Q12, DATASET-D23, DATASET-D28, DATASET-D29_
- **IC-2**: Generally aligned for Indian content [Q12], but cultural-fit issues exist: South Indian items (Tamil/Telangana) [DATASET-D31, D32, D33, D34] are pan-India GK at the periphery, and English-vocabulary items embedded in Hindi [DATASET-D40, D41, D42] mismatch the Hindi-medium register. — _Sources: Q12, DATASET-D31, DATASET-D32, DATASET-D40_
- **IC-3**: Western-specific knowledge is not a dominant concern, but English-medium textbook conventions surface via translation: dataset shows 100% translation rate in the validation sample [Limitation #1] and English vocabulary tests in Hindi-labeled content [DATASET-D40, D41, D42]; this exceeds the deployment's ~10% code-mixing ceiling [elicitation Q4]. — _Sources: Q44, Q47, DATASET-D40, DATASET-D41, DATASET-D42_
- **IC-4**: INSUFFICIENT DOCUMENTATION — paper does not report annotator demographics for the Hindi subset; would need to know whether reviewers were Hindi-medium graduates familiar with central-exam idiom.
- **IC-5**: Documented violations: (a) heavy translation rate in observed Hindi split [Limitation #1, Q47]; (b) Current Affairs staleness [DATASET-D19, D20, D21, D22]; (c) English-vocabulary items in Hindi pool [DATASET-D40–D42]; (d) South India–specific content density [DATASET-D31–D34]. Each harms content validity for North-India Hindi-medium central-exam deployment. — _Sources: Q47, DATASET-D19, DATASET-D20, DATASET-D40, DATASET-D31_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q11] 'We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams.' (p.2)
- [Q24] 'collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams' (p.3)
- [Q44] 'For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O.' (p.4)
- [Q47] 'Of the total 79K questions, only 25% of questions are translated from English' (p.4)

*Web sources:*
- [WEB-9] UPSC Current Affairs ranges 0–27 questions per year — high weight, currency-sensitive

*Dataset analysis:*
- DATASET-D23, D25, D27, D28, D29: North India regional content (UP minerals, Chikankari, Rajasthan, Kota painting) confirmed
- DATASET-D19, D20, D21, D22: Current Affairs items dated 2018–2022, stale for 2025–2026 aspirants
- DATASET-D40, D41, D42: English vocabulary questions (grim, didactic, Evangelize) labeled as Hindi Language Studies — violates Hindi-medium register
- DATASET-D31, D32, D33, D34: Telangana/Tamil-specific items reduce deployment relevance for North India central-exam focus
- Limitation #1: 100% (245/245) of reviewed Hindi validation examples are is_translated=True, far above documented ~25% rate
- DATASET-D53, D37: Engineering/FORTRAN content translated into Hindi inflates technical specialist proportion

</details>

**Information gaps:**
- Code-mixing rate per Hindi item not quantified
- Whether the validation split's 100% translation rate generalizes to the test split is unverified [Limitation #1]
- Annotator demographics for Hindi audits not reported [Q87]
- Density of Chhath Puja, zamindari, North Indian freedom-fighter content in the full Hindi test split not assessed

**Requires expert verification:**
- Whether GPT-4O Hindi translations preserve Manak Hindi register expected by Hindi-medium aspirants
- Whether the test split (vs. validation split) has substantially different translation rate and subject distribution

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form is LOWER priority per elicitation: deployment is text-only Hindi in Devanagari, matching MILU's text-based MCQ format [Q33, Q29]. Reading-comprehension, image-based, and >4-option items are explicitly excluded [Q33], language correctness is enforced via INDICLID + Unicode filtering [Q34], and duplicates are removed [Q35]. No signal-distribution mismatch concerns arise. The only form-level concern surfaced in dataset analysis is structural: a non-trivial fraction of items in the sample have answer options that reference statements/items absent from the question text [DATASET-D43, D44, D45, D46, D47, D48], indicating data-collection truncation artifacts that introduce construct-irrelevant variance.

**Strengths:**
- Text-only MCQ format matches the deployment's mobile-app input modality [Q33]
- Devanagari Unicode handling and language-identification filtering are explicitly applied [Q34]
- Multiple cleaning passes including manual sampling [Q31, Q32, Q36]

**Checklist:**

- **IF-1**: Signal distributions align: Hindi text in Devanagari is the deployment's input form and matches MILU's encoding [Q29, Q34]. — _Sources: Q29, Q34_
- **IF-2**: Regional infrastructure (Android smartphones, Devanagari rendering) supports text-MCQ input; mature NLP tokenization for Hindi noted in regional context. — _Sources: Q34_
- **IF-3**: Truncation artifacts in some items [DATASET-D43–D48] are a form-level concern: option text references absent question content, harming usability. — _Sources: DATASET-D43, DATASET-D44, DATASET-D45, DATASET-D46, DATASET-D47, DATASET-D48_
- **IF-4**: Documented form mismatches: structurally truncated items [DATASET-D43–D48]; minor code-mixing via transliterated English letters in reasoning items [DATASET-D57]. — _Sources: DATASET-D43, DATASET-D57_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q29] 'we collected more than 150K questions across 11 Indian Languages- Bengali (bn), Gujarati (gu), Hindi (hi)... spanning 41 diverse subjects.' (p.3)
- [Q33] 'we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q34] 'To remove incorrect language entries, we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering' (p.4)

*Dataset analysis:*
- DATASET-D43, D44, D45, D46, D47, D48: Items with answer options referencing absent statements/lists — structural truncation
- DATASET-D57: Transliterated English letters (एमएनक्यू) in reasoning items — minor code-mixing

</details>

**Information gaps:**
- Frequency of structurally truncated items in the full test split is unquantified

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Output ontology is HIGH-priority per elicitation Q3, which specifies that the deployment requires both a correct/incorrect verdict AND a substantive Hindi-language explanatory rationale. MILU's output ontology is a closed-form MCQ label space [Q33, Q55] — a single correct option index. The dataset analysis confirms empirically: every one of 245 reviewed examples has only question/option1–4/target fields with no rationale, explanation, or scoring dimension for free-text output [CRITICAL Concern 1]. Furthermore, MILU's documented pattern that models perform worst precisely in the deployment's priority domains — Arts & Humanities, Social Sciences, Law & Governance [Q6, Q20, Q62, Q71, Q77] — means the benchmark's accuracy ontology, even within its scope, gives weakest signal in the areas the deployment cares about most. This is a fundamental structural-validity violation.

**Strengths:**
- 41-subject hierarchical taxonomy enables domain-level performance analysis aligned with Indian exam structure [Q42]
- MCQ label correctness from real exam keys provides a credible objective floor [Q26]

**Checklist:**

- **OO-1**: Output label categories are MCQ option indices only [Q33, Q55] — they do not include rationale-quality categories required by deployment. — _Sources: Q33, Q55, CRITICAL Concern 1_
- **OO-2**: Missing categories: rationale correctness, rationale fluency in Hindi, pedagogical clarity, and explanation appropriateness — all required by elicitation Q3 but absent from MILU [CRITICAL Concern 1]. — _Sources: CRITICAL Concern 1, WEB-14_
- **OO-3**: Within MCQ scope, no Western-value-encoded categories observed; primary issue is omission, not encoding bias.
- **OO-4**: Stakeholder-driven taxonomy redesign is required: a rationale-quality rubric in Hindi must be added to evaluate the deployment's actual output. — _Sources: WEB-14_
- **OO-5**: Documented harm: MILU's output ontology omits the entire rationale-quality dimension, violating structural validity for this deployment. Additionally, weakest performance in culturally relevant domains [Q6, Q71, Q77] further limits utility for History/Polity/GK signal. — _Sources: Q6, Q71, Q77, CRITICAL Concern 1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q55] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability' (p.5)
- [Q6] 'Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM.' (p.1)
- [Q71] 'open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields.' (p.7)

*Web sources:*
- [WEB-14] 2025 Hindi LLM benchmarking preprint notes Hindi instruction-following/conversational benchmarks are 'largely unavailable publicly'

*Dataset analysis:*
- CRITICAL Concern 1: All 245 reviewed examples have schema (question, option1-4, target, is_translated, language, domain, subject) — no rationale field exists
- DATASET-D1, D15, D56: Even canonical Polity/Math/Ethics items have only target labels with no worked solutions or reasoning chains

</details>

**Requires expert verification:**
- Design of a Hindi rationale-quality rubric requires regional pedagogical expert input

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
Output content priority is MODERATE. For MCQ correctness, MILU has a credible label-provenance chain: questions and answers come from online exam portals where subject experts ensure answer accuracy [Q26], with internal AI4Bharat manual audits [Q87]. However, several issues lower the score: (a) annotator demographics, IAA, and formal QA protocol are not reported — paper does not say whether auditors were Hindi-medium graduates or central-exam experts; (b) the deployment's PRIMARY output (Hindi-language explanatory rationale) has no ground-truth labels at all in MILU [CRITICAL Concern 1]; (c) dataset analysis surfaces at least one suspicious 'none of these' answer for a specific constitutional article query [DATASET-D49] suggesting some scraping data-quality issues; (d) for the ~5+ structurally truncated items observed [DATASET-D43–D48], the labeled answer cannot be validated without source content. Convergent validity for the rationale construct is undefined because the construct itself is not annotated.

**Strengths:**
- MCQ answer keys inherited from established exam-portal QA processes [Q26]
- Internal manual audits by AI4Bharat volunteers [Q87]
- Manual review of topic-tag clusters before assigning subject labels [Q41]

**Checklist:**

- **OC-1**: Ground truth MCQ labels reflect Indian exam-portal expert judgments [Q26], but no rationale labels exist for the deployment's primary output [CRITICAL Concern 1]. — _Sources: Q26, CRITICAL Concern 1_
- **OC-2**: MCQ answer disagreement risk is low for canonical items; rationale-level disagreement cannot be assessed because no rationale annotations exist. — _Sources: Q26_
- **OC-3**: INSUFFICIENT DOCUMENTATION — paper acknowledges AI4Bharat volunteer audits [Q87] but does not report demographics, Hindi-medium status, or domain expertise of annotators. — _Sources: Q87_
- **OC-4**: Re-annotation needed for: (a) any items with 'none of these' answers [DATASET-D49]; (b) all structurally truncated items [DATASET-D43–D48]; (c) full rationale-quality annotation by Hindi-medium central-exam experts. — _Sources: DATASET-D49, DATASET-D43, CRITICAL Concern 1_
- **OC-5**: INSUFFICIENT DOCUMENTATION — paper does not describe aggregation methods or how disagreements between portal answers and audits were resolved.
- **OC-6**: Documented harms: rationale-quality construct entirely unannotated [CRITICAL Concern 1]; data-quality issues in specific items [DATASET-D49, D43–D48]; annotator demographic opacity limits convergent-validity assessment. — _Sources: CRITICAL Concern 1, DATASET-D49, DATASET-D43_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q26] 'These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers.' (p.3)
- [Q87] 'We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits.' (p.9)
- [Q41] 'We manually review these clusters and assign appropriate subject labels.' (p.4)

*Dataset analysis:*
- DATASET-D49: 'None of these' as correct answer for a specific constitutional article query — possible data quality issue
- DATASET-D43, D44, D45, D46, D47, D48: Truncated items where label correctness cannot be independently verified
- CRITICAL Concern 1: No rationale annotation exists for any item

</details>

**Information gaps:**
- Annotator demographics, IAA, and formal QA protocol not documented
- Frequency of data-quality issues like 'none of these' answers and truncated items in the full test split

**Requires expert verification:**
- Whether MCQ keys for North-India-relevant Polity/History items align with how Hindi-medium central-exam coaching answers them
- Establishment of a regional Hindi-medium expert panel to spot-check labels and produce rationale ground truth

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Output form is HIGH-priority per elicitation. The deployment requires open-ended Hindi explanatory text alongside a verdict label. MILU evaluates models exclusively via MCQ label accuracy: log-likelihood option selection for non-API models [Q52, Q53, Q54, Q55] and JSON-structured single-answer generation for API models [Q56, Q57]. The benchmark authors themselves explicitly flag this as a limitation: 'our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought prompting' [Q85]. The dataset analysis confirms this empirically — no rationale or explanation field exists in any of 245 reviewed examples [CRITICAL Concern 1]. Web research confirms no Hindi-language exam-rationale evaluation benchmark currently exists [WEB-14, WEB-13]. MILU's output form fundamentally cannot validate the deployment's core output: fluency, factual accuracy, or pedagogical quality of Hindi-language rationales.

**Strengths:**
- Reproducible MCQ scoring via LM Evaluation Harness [Q52]
- 0-shot, 1-shot, 5-shot evaluation protocols for sensitivity analysis [Q50]

**Checklist:**

- **OF-1**: Mismatch — deployment requires Hindi free-text explanation alongside verdict [elicitation Q3]; MILU produces only MCQ accuracy [Q55, CRITICAL Concern 1]. — _Sources: Q55, CRITICAL Concern 1_
- **OF-2**: Not applicable — deployment is text-only; no TTS requirement.
- **OF-3**: Target population is graduate-level and near-universally literate in Hindi; literacy is not the gating concern. The gating concern is Hindi NLG quality, which MILU does not evaluate. — _Sources: WEB-13_
- **OF-4**: Documented harms: MCQ-only scoring [Q55, Q85] cannot validate Hindi rationale fluency, coherence, or pedagogical fit; no Hindi exam-rationale benchmark exists [WEB-14] to supplement. — _Sources: Q55, Q85, WEB-14, CRITICAL Concern 1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q53] 'We use the log-likelihood method, where the probability of a given output string is computed by conditioning it on some provided input' (p.5)
- [Q55] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability' (p.5)
- [Q57] 'We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing.' (p.5)
- [Q85] 'our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting.' (p.9)

*Web sources:*
- [WEB-13] IndicGenBench (ACL 2024) covers Hindi generation but not exam rationale quality
- [WEB-14] 2025 Hindi LLM benchmarking preprint notes Hindi instruction-following/conversational benchmarks are 'largely unavailable publicly'

*Dataset analysis:*
- CRITICAL Concern 1: No rationale/explanation field in any of 245 reviewed examples — schema is question/option1-4/target/is_translated/language/domain/subject only

</details>

**Requires expert verification:**
- Design and validation of a Hindi rationale-quality rubric (factual accuracy, fluency, pedagogical clarity, register) requires Hindi-medium pedagogy experts

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** No rationale-quality construct in MILU's output ontology, while deployment requires Hindi explanatory feedback [Q33, CRITICAL Concern 1, elicitation Q3]

**Recommendation:** Commission a rationale-evaluation rubric with Hindi-medium pedagogy experts covering factual accuracy, Manak Hindi fluency, pedagogical clarity, and code-mixing ceiling; use as a complementary evaluation alongside MILU's MCQ accuracy.

### Output Form ⚠

**Gap:** MCQ-only scoring (log-likelihood / JSON option selection) cannot validate Hindi free-text rationale [Q55, Q85]

**Recommendation:** Add a generation-based Hindi rationale evaluation using LLM-as-judge with the rubric above, plus periodic human evaluation; consider adapting IFEval-Hi/MT-Bench-Hi protocols [WEB-14] to exam-specific prompts.

### Input Content ⚠

**Gap:** 100% translation rate observed in Hindi validation split [Limitation #1] plus English-vocabulary items mislabeled as Hindi content [DATASET-D40–D42] threaten the 10% code-mixing ceiling

**Recommendation:** Filter MILU Hindi to natively-sourced (is_translated=False) items where possible and exclude English-vocabulary Language-Studies items; sample remaining items for Manak Hindi register quality with a Hindi-medium reviewer.

### Input Content ⚠

**Gap:** Current Affairs items dated 2018–2022 [DATASET-D19–D22] are stale for 2025–2026 aspirants; MILU has no currency mechanism

**Recommendation:** Build a parallel rolling Current Affairs MCQ set (last 12 months of pan-India GK and North-India events) and evaluate the model on it monthly; do not rely on MILU for Current Affairs signal.

### Input Ontology

**Gap:** Pooled 40+ exam types [Q27] and presence of specialist Engineering/South India content [DATASET-D35–D38, D31–D34] dilute central-exam relevance

**Recommendation:** Create a deployment-specific subset by filtering MILU items to Polity/Law&Governance, Social Sciences, Business Studies arithmetic, Science reasoning items, and Hindi grammar; explicitly drop Engineering & Technology specialist items not in UPSC/SSC/banking syllabi.

### Output Content

**Gap:** Annotator demographics not reported [Q87]; some items appear truncated or have suspicious answers [DATASET-D43–D49]

**Recommendation:** Recruit a small Hindi-medium central-exam expert panel to audit a stratified 200-item sample for label correctness, register, and structural completeness; remove confirmed broken items from the deployment-evaluation subset.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge." |
| Q2 | 1 | input_content | "With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science." |
| Q3 | 1 | output_form | "We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q4 | 1 | output_form | "Open multilingual models outperform language-specific fine-tuned models, which perform only slightly better than random baselines." |
| Q5 | 1 | input_ontology | "Models also perform better in high-resource languages as compared to low-resource ones." |
| Q6 | 1 | output_ontology | "Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM." |
| Q7 | 1 | input_ontology | "To the best of our knowledge, MILU is the first of its kind benchmark focused on Indic languages, serving as a crucial step towards comprehensive cultural evaluation." |
| Q8 | 1 | input_content | "All code, benchmarks, and artifacts will be made publicly available to foster open research." |
| Q9 | 1 | output_content | "Sshubam Verma, Mohammed Safi Ur Rahman Khan, Vishwajeet Kumar, Rudra Murthy, Jaydeep Sen" |
| Q10 | 1 | output_content | "Nilekani Centre at AI4Bharat, Indian Institute of Technology, Madras, IBM Research, India" |
| Q11 | 2 | input_content | "We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams." |
| Q12 | 2 | output_ontology | "These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science." |
| Q13 | 2 | input_content | "Following previous efforts (Hendrycks et al., 2021; Zhong et al., 2023), we create this benchmark by collecting questions from over 1500 competitive exams from India." |
| Q14 | 2 | input_content | "We focus on region-specific exams to authentically capture local knowledge in the respective language." |
| Q15 | 2 | output_form | "We evaluate 45 different LLMs - a mix of closed proprietary, open-source, and language-specific models- on MILU." |
| Q16 | 2 | output_form | "Our findings suggest that models struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q17 | 2 | output_form | "Interestingly, open multilingual models outperform language-specific models, which only achieve slightly better than random scores." |
| Q18 | 2 | output_form | "Our analysis of in-context learning reveals that adding more examples improves performance in base models, but the effect on instruct models remains inconclusive." |
| Q19 | 2 | output_form | "We also explore how performance scales with the number of parameters, finding significant improvements as model size increases." |
| Q20 | 2 | output_ontology | "Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM." |
| Q21 | 2 | input_content | "All the artifacts will be released publicly." |
| Q22 | 3 | input_ontology | "MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge." |
| Q23 | 3 | input_ontology | "This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others." |
| Q24 | 3 | input_content | "These questions were sourced following an approach similar to AGIEVAL (Zhong et al., 2023), collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams, among others." |
| Q25 | 3 | input_content | "We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages." |
| Q26 | 3 | output_content | "These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers." |
| Q27 | 3 | input_ontology | "Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years." |
| Q28 | 3 | input_content | "Regional state exams are particularly valuable as they cover various state-level topics and emphasize the official language of each state." |
| Q29 | 3 | input_form | "In total, we collected more than 150K questions across 11 Indian Languages- Bengali (bn), Gujarati (gu), Hindi (hi), Kannada (kn), Malayalam (ml), Marathi (mr), Odia (or), Punjabi (pn), Tamil (ta), Telugu (te), and English (en)-spanning 41 diverse subjects." |
| Q30 | 3 | input_content | "English questions are also included as these often address Indian culture-specific content, which is notably missing from existing popular benchmarks." |
| Q31 | 4 | input_form | "Despite our best efforts to maintain the quality of questions collected, some amount of noise or errors may still be present. To address potential noise in the questions, we employ multiple layers of manual and automated cleaning filters." |
| Q32 | 4 | input_form | "Initially, we manually review a large sample of questions to detect and eliminate potential sources of noise." |
| Q33 | 4 | input_form | "During the collection process, we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency." |
| Q34 | 4 | input_form | "To remove incorrect language entries, we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering (Khan et al., 2024), ensuring that the questions are in the correct language." |
| Q35 | 4 | input_form | "To further refine the dataset, we remove any duplicate questions to retain only the unique ones." |
| Q36 | 4 | input_form | "As a final step, we manually verify a sample of questions from each language to ensure accuracy and correct any remaining errors." |
| Q37 | 4 | input_content | "Upon examination, we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information." |
| Q38 | 4 | input_content | "To address this issue, we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question." |
| Q39 | 4 | output_ontology | "Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap." |
| Q40 | 4 | output_ontology | "To organize them, we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters." |
| Q41 | 4 | output_content | "We manually review these clusters and assign appropriate subject labels." |
| Q42 | 4 | output_ontology | "Following the manual merging of related clusters, we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies." |
| Q43 | 4 | input_content | "Finally, we observed that some topics in certain languages had less than 100 questions. To ensure thorough evaluation across all subjects and languages, we aimed to have at least 100 questions per subject in each language." |
| Q44 | 4 | input_content | "For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O." |
| Q45 | 4 | input_content | "We chose GPT-4O over specialized translation models for their ability to remain task-aware during translation (Ahuja et al., 2024), ensuring the translated content aligns with the intent of the question." |
| Q46 | 4 | input_ontology | "In total, we release around 79K questions across 41 subjects across 8 domains in 11 languages, capping each subject-language pair at 500 questions for feasible evaluations." |
| Q47 | 4 | input_content | "Table 2 shows the overall statistics of MILU. Of the total 79K questions, only 25% of questions are translated from English, with the remainder" |
| Q48 | 5 | output_form | "We evaluate 42 different models on MILU, including large proprietary models, open-source multilingual models, and popular fine-tuned models specific to Indic languages." |
| Q49 | 5 | output_form | "Both the base versions and instruction fine-tuned variants of these models, wherever applicable, are evaluated to measure the improvements gained from fine-tuning." |
| Q50 | 5 | output_form | "All models, except for proprietary models and LLAMA-3.1-405B, are tested under 0-shot, 1-shot, and 5-shot setups." |
| Q51 | 5 | input_content | "We maintain a separate validation set of approximately 9,000 questions to serve as examples for few-shot evaluations." |
| Q52 | 5 | output_form | "For non-API-based models, we use the LM-EVALUATION-HARNESS (Gao et al., 2024; Biderman et al., 2024) to ensure clean and reproducible evaluations." |
| Q53 | 5 | output_form | "We use the log-likelihood method, where the probability of a given output string is computed by conditioning it on some provided input (Brown et al., 2020)." |
| Q54 | 5 | output_form | "Specifically, the log-likelihood of an answer (a) given the question (x), i.e., logP(a\|x), is calculated by concatenating the answer (a) with question (x), and then summing up the log probabilities, of each target token." |
| Q55 | 5 | output_form | "For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability, i.e., argmax(logP(a1\|x), ..., logP(ak\|x))." |
| Q56 | 5 | output_form | "The API-based models are evaluated using the generative approach due to the lack of support for prompt log probabilities." |
| Q57 | 5 | output_form | "We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing." |
| Q58 | 5 | output_form | "Due to the high costs involved, these models are evaluated only in the zero-shot setup." |
| Q59 | 6 | output_form | "We report 5-shot accuracies for all open models (except for LLAMA-3.1-70B-INSTRUCT & LLAMA-3.1-405B for which we report 0-shot accuracy) with the accuracy averaged across all the domains per language." |
| Q60 | 6 | input_ontology | "We evaluate around 16 Indic language LLMs on MILU. These models are primarily built by adapting English LLMs, such as LLAMA-2-7B, by first continually pretraining on small amount Indic language data, followed by optionally instruction finetuning them." |
| Q61 | 6 | output_form | "As seen from Table 4, across languages, the models exhibit average performance comparable to random baselines, with minimal variations among them." |
| Q62 | 6 | output_ontology | "When analyzed across domains, the models generally perform worse in Arts, Humanities, and Social Sciences than in STEM subjects." |
| Q63 | 6 | output_form | "We compare the performance of different Base and Instruct models across zero, one, and five-shot setups." |
| Q64 | 6 | output_form | "As shown in Figure 3, the performance of base models consistently improves with an increasing number of in-context examples, with the 5-shot setup yielding the best results." |
| Q65 | 6 | output_form | "In contrast, Instruct models exhibit more varied behavior, where models either stagnate or even degrade in performance." |
| Q66 | 6 | output_form | "This also aligns with expectations, as Instruct models are specifically fine-tuned as conversation assistants and may not respond well to the few-shot in-context examples format." |
| Q67 | 7 | output_form | "Table 4: Evaluation results of all the language-specific fine-tuned models on MILU. We report domain level 5-shot accuracies for all the models on the language supported by the model. Higher values indicate better model performance for the given domain." |
| Q68 | 7 | output_form | "Figure 3: Comparison of Base and Instruct models averaged across all languages for varying number of in-context examples. We plot the average accuracies of the GEMMA and LLAMA series of models, highlighting the performance trend as the number of in-context examples increases." |
| Q69 | 7 | output_form | "We evaluate the LLAMA and GEMMA family of models, ranging from 1B to 405B parameters, to analyze how performance scales with model size." |
| Q70 | 7 | output_form | "Figure 5 shows that the model performance improves significantly with increasing scale. Notably, instruction-tuned models in the LLAMA family show more substantial improvements as compared to those in the GEMMA family." |
| Q71 | 7 | output_ontology | "We analyze the performance of various base and instruct models across multiple domains and languages. Similar trends to those in Section (§5.2) are observed where the open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields." |
| Q72 | 7 | input_content | "This suggests that the training corpora for these models lack sufficient culturally specific data. Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages." |
| Q73 | 7 | output_form | "As most Indic LLMs are built on English base models like LLAMA-2-7B, we assess the impact of language adaptation on their performance. Table 5 compares language-specific models with the original LLAMA-2-7B, and instruction-tuned models with LLAMA-2-7B-CHAT. Our findings show minimal gains, with some models even underperforming post-adaptation." |
| Q74 | 8 | input_ontology | "In this paper, we introduced MILU—Multilingual Indic Language Understanding Benchmark-a comprehensive benchmark specifically designed to evaluate LLMs across 11 Indic languages, spanning diverse domains and culturally relevant subjects." |
| Q75 | 8 | output_form | "We evaluate 45 different LLMs and find that the majority of LLMs struggle on MILU, with GPT4o achieving the highest average accuracy." |
| Q76 | 8 | input_ontology | "The analysis also shows that models perform significantly better in high-resource languages than low-resource ones, highlighting the need for more robust multilingual strategies." |
| Q77 | 8 | output_ontology | "Additionally, the domain-specific analysis indicates that models perform better in general fields such as STEM while facing challenges in culturally relevant subjects like Arts, Humanities, and Law, highlighting the lack of this knowledge in the current models and datasets." |
| Q78 | 8 | output_form | "We conjecture that limited performance gains may result from small language-specific datasets and reliance on parameter-efficient methods like LoRA (Hu et al., 2022)." |
| Q79 | 8 | output_form | "Another contributing factor could be the lack of diversity in instruction fine-tuning datasets." |
| Q80 | 8 | output_form | "Models like AIRAVATA, which utilize more diverse data (Gala et al., 2024), exhibit noticeably better performance." |
| Q81 | 8 | output_form | "Further investigation is required to fully understand the limitations and opportunities in this area." |
| Q82 | 9 | input_ontology | "First, we restricted our study to the top 11 languages due to the lack of readily available questions in low-resource languages, which we aim to address in future work." |
| Q83 | 9 | output_form | "Second, limited computational resources prevented a thorough evaluation of larger models, such as LLAMA-3.1-70B-INSTRUCT and LLAMA-3.1-405B." |
| Q84 | 9 | input_content | "Third, the scarcity of questions necessitated translating a portion of the dataset." |
| Q85 | 9 | output_form | "Finally, our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting." |
| Q86 | 9 | output_content | "We would like to thank EkStep Foundation and Nilekani Philanthropies for their generous grant towards building datasets, models, tools and other resources for Indian languages." |
| Q87 | 9 | output_content | "We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits." |
| Q88 | 9 | input_content | "All data described in this work was scraped from publicly available resources." |
| Q89 | 9 | input_content | "The datasets used in this paper will be made available under permissible licenses." |
| Q90 | 9 | input_content | "Additionally, the code used for our evaluations will be made publicly available under the MIT License." |
| Q91 | 10 | input_content | "Sumanth Doddapaneni, Rahul Aralikatte, Gowtham Ramesh, Shreya Goyal, Mitesh M. Khapra, Anoop Kunchukuttan, and Pratyush Kumar. 2023. Towards leaving no Indic language behind: Building monolingual corpora, benchmark and models for Indic languages. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 12402–12426, Toronto, Canada. Association for Computational Linguistics." |
| Q92 | 17 | input_content | "We collected our questions from over 40 exam types ranging from various National and state level civil service examinations to examinations conducted by various government and private organizations." |
| Q93 | 17 | input_form | "Detailed analysis of topic and language distribution across languages can be found in Table 9 and Figure 6" |
| Q94 | 17 | output_form | "Model details about the different models evaluated in this work is present in Table 10." |
| Q95 | 18 | input_content | "Table 6: Overview of various national-level exams and the corresponding years of coverage considered in MILU." |
| Q96 | 18 | input_content | "Table 7: Overview of various government and private organization exams and the corresponding years of coverage considered in MILU." |
| Q97 | 18 | input_content | "Table 8: Overview of various State-level civil services exams and the corresponding years of coverage considered in MILU." |
| Q98 | 20 | input_ontology | "Table 9: Detailed subject level statistics of MILU across different languages." |
| Q99 | 22 | output_form | "Table 11: Detailed subject-wise evaluation for ABHINAND/TAMIL-LLAMA-7B-INSTRUCT-V0.2 on MILU across different languages." |
| Q100 | 22 | output_form | "The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q101 | 23 | output_form | "Table 12: Detailed subject-wise evaluation for AI4BHARAT/AIRAVATA on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q102 | 24 | output_form | "Table 13: Detailed subject-wise evaluation for BHABHAAI/GAJENDRA-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q103 | 25 | output_form | "Table 14: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-BASE-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q104 | 26 | output_form | "Table 15: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q105 | 27 | output_form | "Table 16: Detailed subject-wise evaluation for GENVRADMIN/ARYABHATTA-GEMMAGENZ-VIKAS-MERGED on MILU across different languages." |
| Q106 | 28 | output_form | "Table 17: Detailed subject-wise evaluation for MANISHIITG/OPEN-ADITI-V6-LLAMA3 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q107 | 29 | output_form | "Table 18: Detailed subject-wise evaluation for NICKMALHOTRA/PROJECTINDUS on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q108 | 30 | output_form | "Table 19: Detailed subject-wise evaluation for SARVAMAI/OPENHATHI-7B-HI-V0.1-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q109 | 31 | output_form | "Table 20: Detailed subject-wise evaluation for TENSOIC/KAN-LLAMA-7B-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q110 | 32 | output_form | "Table 21: Detailed subject-wise evaluation for ABHINAND/MALAYALAM-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages." |
| Q111 | 33 | output_form | "Table 22: Detailed subject-wise evaluation for ABHINAND/TELUGU-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q112 | 34 | output_form | "Table 23: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q113 | 35 | output_form | "Table 24: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-BASE-V0.1 on MILU across different languages." |
| Q114 | 36 | output_form | "Table 25: Detailed subject-wise evaluation for TELUGU-LLM-LABS/TELUGU-LLAMA2-7B-V0-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q115 | 37 | output_form | "Table 26: Detailed subject-wise evaluation for GPT-4o on MILU across different languages. The results reported are for 0-shot experiments." |
| Q116 | 38 | output_form | "Table 27: Detailed subject-wise evaluation for GPT-4O-MINI on MILU across different languages. The results reported are for 0-shot experiments." |
| Q117 | 39 | output_form | "Table 28: Detailed subject-wise evaluation for GEMINI-1.5-PRO on MILU across different languages. The results reported are for 0-shot experiments." |
| Q118 | 40 | output_form | "Table 29: Detailed subject-wise evaluation for GEMINI-1.5-FLASH on MILU across different languages. The results reported are for 0-shot experiments." |
| Q119 | 41 | output_form | "Table 30: Detailed subject-wise evaluation for KRUTRIM-SPECTRE-V2 on MILU across different languages. The results reported are for 0-shot experiments." |
| Q120 | 42 | output_form | "Table 31: Detailed subject-wise evaluation for SARVAMAI/SARVAM-1 on MILU across different languages. The results reported are for 5-shot experiments." |
| Q121 | 43 | output_form | "Table 32: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.2-1B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q122 | 43 | output_form | "Table 33: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.2-1B-INSTRUCT on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q123 | 44 | output_form | "Table 34: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q124 | 44 | output_form | "Table 35: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B-IT on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q125 | 46 | output_form | "Table 38: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.2-3B-INSTRUCT on MILU across different languages." |
| Q126 | 47 | output_form | "Table 39: Detailed subject-wise evaluation for NVIDIA/NEMOTRON-4-MINI-HINDI-4B-BASE on MILU across different languages. The results reported are for 5-shot experiments." |
| Q127 | 49 | output_form | "Table 42: Detailed subject-wise evaluation for NEULAB/PANGEA-7B on MILU across different languages. The results reported are for 5-shot experiments." |
| Q128 | 52 | output_form | "Table 47: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-9B-IT on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q129 | 52 | output_form | "Table 48: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-27B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q130 | 55 | output_form | "Table 52: 0-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q131 | 56 | output_form | "Table 53: 1-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q132 | 57 | output_form | "Table 54: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.1-405B on MILU across different languages. The results reported are for 0-shot experiments." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2186639 |
| WEB-2 | https://news.careers360.com/womens-share-in-civil-services-up-from-24-35-pc-in-5-years-engineers-over-50-percent-government-data-upsc-ias-ips |
| WEB-3 | https://theprint.in/india/family-support-safety-study-material-a-click-away-whats-driving-more-women-to-take-upsc-exam/1922660/ |
| WEB-4 | https://scroll.in/article/825780/bihar-uttar-pradesh-rajasthan-and-madhya-pradesh-have-worst-literacy-rates-school-outcomes |
| WEB-5 | https://en.wikipedia.org/wiki/Literacy_in_India |
| WEB-6 | https://trai.gov.in/sites/default/files/2024-11/Cons_P_14092023.pdf |
| WEB-7 | https://en.wikipedia.org/wiki/Internet_in_India |
| WEB-8 | https://www.iamai.in/sites/default/files/research/Kantar_%20IAMAI%20report_2024_.pdf |
| WEB-9 | https://testbook.com/ias-preparation/upsc-prelims-subject-wise-weightage |
| WEB-10 | https://www.pw.live/ssc/exams/ssc-cgl-syllabus |
| WEB-11 | https://upsc.gov.in/examinations/active-examinations/civil-services-examination |
| WEB-12 | https://sleepyclasses.com/discover-how-many-candidates-are-selected-in-upsc-each-year/ |
| WEB-13 | https://aclanthology.org/2024.acl-long.595/ |
| WEB-14 | https://arxiv.org/html/2508.19831v1 |
| WEB-15 | https://vajiramandravi.com/upsc-exam/csat-syllabus/ |
| WEB-16 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-17 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-18 | https://prsindia.org/billtrack/digital-personal-data-protection-bill-2023 |
| WEB-19 | https://www.saikrishnaassociates.com/decoding-the-india-ai-governance-guidelines/ |
| WEB-20 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2234853&reg=3&lang=1 |
| WEB-21 | https://github.com/google-research-datasets/indic-gen-bench |
| WEB-22 | https://captaincompliance.com/education/dpdpa-india-the-complete-guide-to-indias-digital-personal-data-protection-act-2023/ |
| WEB-23 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2123422 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Hindi config)
**Analysis date:** 2025-01-31
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | MILU/Hindi | 33 | option1 | "______ एक अदालत का आदेश है जो एक अधीनस्थ अदालत या सार्वजनिक प्राधिकरण को एक आधिकारिक कर्तव्य को सही ढंग से निभाने का निर्देश देता है।" | Mandamus writ definition question — Indian constitutional law | IO, IC |
| D2 | MILU/Hindi | 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" | Constitutional amendment adding 'armed rebellion' — Indian Polity | IO, IC |
| D3 | MILU/Hindi | 39 | option3 | "भारत में किस संवैधानिक संशोधन विधेयक द्वारा मतदान की आयु 21 वर्ष से घटाकर 18 वर्ष की गई थी?" | Constitutional amendment lowering voting age — Indian Polity | IO, IC |
| D4 | MILU/Hindi | 42 | option3 | "निम्नलिखित में से कौन मसौदा समिति का सदस्य नहीं था?" | Drafting committee membership — Indian Constitution | IO, IC |
| D5 | MILU/Hindi | 93 | option2 | "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है?" | Three-tier Panchayati Raj middle unit — Indian Governance | IO, IC |
| D6 | MILU/Hindi | 136 | option4 | "भारत के संविधान के अनुसार, संसद का कौन सा सदन संविधान संशोधन विधेयक पारित करता है?" | Which house passes constitutional amendment bill | IO, IC |
| D7 | MILU/Hindi | 50 | option3 | "1882 में भारत में स्थानीय स्वशासन की शुरुआत किसने की?" | Who introduced local self-government in India 1882 | IO, IC |
| D8 | MILU/Hindi | 199 | option4 | "1907 के कांग्रेस सत्र में उदारवादियों और उग्रवादियों के बीच मुख्य अंतर किस विषय पर था?" | 1907 Congress session — moderate vs extremist split | IO, IC |
| D9 | MILU/Hindi | 32 | option4 | "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया।" | Who completed Qutub Minar — Medieval Indian history | IO, IC |
| D10 | MILU/Hindi | 96 | option2 | "कौन सा अधिनियम प्रांतों में द्वैध शासन प्रणाली स्थापित करता है?" | Which act established dyarchy in provinces — Modern India history | IO, IC |
| D11 | MILU/Hindi | 158 | option3 | "'देवानांप्रिय' और 'प्रियदर्शी' वे उपाधियाँ थीं जिन्हें राजा ______ ने अपनाया था।" | Titles 'Devanampiya' and 'Priyadarshi' — Ashoka/Ancient India | IO, IC |
| D12 | MILU/Hindi | 237 | option3 | "मोहनजोदड़ो और हड़प्पा के खंडहर दिखाते हैं कि ये शानदार और अच्छी तरह से योजनाबद्ध ________ थे।" | Harappan civilization characterized as merchant cities | IO, IC |
| D13 | MILU/Hindi | 36 | option3 | "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है। TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______." | Letter series completion — Logical Reasoning | IO |
| D14 | MILU/Hindi | 44 | option2 | "दिए गए अक्षर श्रृंखला के रिक्त स्थानों में क्रमिक रूप से रखे जाने पर श्रृंखला को पूरा करने वाले अक्षरों के संयोजन का चयन करें। _q p p_p p_p p q_" | Letter pattern completion — Logical Reasoning | IO |
| D15 | MILU/Hindi | 84 | option3 | "सूरज ने अजय से एक निश्चित दर पर साधारण ब्याज पर दो वर्षों के लिए एक राशि उधार ली और उसे विनय को उसी दर पर वार्षिक चक्रवृद्धि ब्याज पर दो वर्षों के लिए उधार दिया।" | Simple vs. compound interest calculation — Quantitative Aptitude/Mathematics | IO |
| D16 | MILU/Hindi | 120 | option4 | "किसी कंपनी में सभी कर्मचारियों का औसत वेतन रु. 10500 है। सभी पुरुष कर्मचारियों का औसत वेतन रु. 15000 है।" | Average salary mixture problem — Quantitative Aptitude | IO |
| D17 | MILU/Hindi | 111 | option3 | "आठ लोग दो समानांतर पंक्तियों में बैठे हैं... A के ठीक विपरीत कौन बैठता है?" | Seating arrangement reasoning problem | IO |
| D18 | MILU/Hindi | 208 | option4 | "कथन: I. कुछ पेन कप हैं। II. सभी कप प्लेट हैं। निष्कर्ष: I. सभी पेन प्लेट हैं।" | Syllogism — formal logical reasoning | IO |
| D19 | MILU/Hindi | 74 | option4 | "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी?" | India GDP growth rate Q2 2018-19 — Current Affairs (dated) | IO, IC |
| D20 | MILU/Hindi | 132 | option4 | "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं?" | WCD Ministry head as of 2018 — Current Affairs (dated) | IO, IC |
| D21 | MILU/Hindi | 88 | option1 | "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान एक क्षुद्रग्रह पर उतरा। उस क्षुद्रग्रह का नाम है:" | JAXA asteroid landing 2019 — Current Affairs (dated) | IO, IC |
| D22 | MILU/Hindi | 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" | Archery Asia Cup 2022 India gold medals — Sports Current Affairs (dated) | IO, IC |
| D23 | MILU/Hindi | 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" | Mineral not found in Uttar Pradesh — North India–specific geography | IC |
| D24 | MILU/Hindi | 68 | option2 | "निम्नलिखित में से राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है?" | 'Bajju' reserve forest in Rajasthan — state-specific geography | IC |
| D25 | MILU/Hindi | 156 | option1 | "2011 की जनगणना के अनुसार राजस्थान की कुल साक्षरता का लगभग प्रतिशत कितना है?" | Rajasthan literacy rate 2011 — state-specific GK | IC |
| D26 | MILU/Hindi | 190 | option2 | "राजस्थान का आकार है-" | Shape of Rajasthan state — state-specific geography | IC |
| D27 | MILU/Hindi | 182 | option1 | "निम्नलिखित में से किस राज्य ने 2011-12 में सबसे अधिक दूध उत्पादन दर्ज किया?" | Highest milk production state 2011-12 — UP-specific GK | IC |
| D28 | MILU/Hindi | 242 | option4 | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है, जिसमें शिफॉन, मलमल, ऑर्गेंजा, ऑर्गेंडी और रेशम जैसे कपड़ों पर नाजुक पारंपरिक हाथ कढ़ाई की जाती है।" | Chikankari — UP traditional embroidery craft | IC |
| D29 | MILU/Hindi | 193 | option3 | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" | Kota painting school — Rajasthan art history | IC |
| D30 | MILU/Hindi | 198 | option2 | "छत्तीसगढ़ के निम्नलिखित विद्रोहों में से किसे 'बस्तर का स्वतंत्रता संग्राम' भी कहा जाता है?" | Chhattisgarh tribal rebellion — Central India history (outside North India core states) | IC |
| D31 | MILU/Hindi | 52 | option2 | "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था, वह था" | Pandya kingdom expansion — South Indian history, less relevant to UPSC North India focus | IC |
| D32 | MILU/Hindi | 108 | option3 | "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" | First cartoons in Tamil magazine — Tamil literary history | IC |
| D33 | MILU/Hindi | 126 | option3 | "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" | Telangana literary work — Telangana-specific cultural question | IC |
| D34 | MILU/Hindi | 41 | option1 | "टी-हब तेलंगाना राज्य सरकार की एक पहल है" | T-Hub Telangana tech incubator — state-specific non-central content | IC |
| D35 | MILU/Hindi | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" | DC series motor behavior — Engineering, not UPSC/SSC priority | IO |
| D36 | MILU/Hindi | 3 | option2 | "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" | Half-wave rectifier output — Electrical engineering technical content | IO |
| D37 | MILU/Hindi | 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" | FORTRAN 77 fixed format — specialist programming, not UPSC/SSC priority | IO |
| D38 | MILU/Hindi | 104 | option4 | "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" | Intermediate frequency for AM receivers — electronics engineering specialist content | IO |
| D39 | MILU/Hindi | 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं।" | William Wordsworth's nationality — English literature, minimal India relevance | IC |
| D40 | MILU/Hindi | 76 | option2 | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" | English vocabulary question: 'didactic' meaning — Language Studies, English vocabulary in Hindi context | IC, IF |
| D41 | MILU/Hindi | 90 | option3 | "शब्द 'grim' का पर्यायवाची लिखें।" | Synonym of English word 'grim' — English vocabulary tested in Hindi-labeled context | IC, IF |
| D42 | MILU/Hindi | 105 | option4 | "निर्देश: निम्नलिखित प्रश्न में, चार विकल्पों में से उस शब्द का चयन करें जो दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है। Evangelize" | English word 'Evangelize' meaning — English vocabulary question in Hindi dataset | IC, IF |
| D43 | MILU/Hindi | 56 | option2 | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें और दिए गए विकल्पों में से सही उत्तर चुनें: (1) और (3) केवल" | Ethanol statements question — options reference numbered statements absent from the question | IF |
| D44 | MILU/Hindi | 86 | option2 | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" | Multidimensional poverty states — options reference A/B/C/D/E labels with no list in question | IF |
| D45 | MILU/Hindi | 94 | option4 | "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? (केवल a, d) / (केवल b, c)" | Redox reactions question — options reference a/b/c/d labels absent from question text | IF |
| D46 | MILU/Hindi | 69 | option2 | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (b), (c) और (d)" | Pure substance — options reference items (a)/(b)/(c)/(d) absent from question | IF |
| D47 | MILU/Hindi | 95 | option1 | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं। AEDBCF" | Sentence ordering — sentences B/C/D/E absent from question text | IF |
| D48 | MILU/Hindi | 106 | option2 | "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" | Chronological ordering of substances — substance list absent from question | IF |
| D49 | MILU/Hindi | 109 | option4 | "छत्तीसगढ़ में नगरपालिकाओं के सभी चुनावों के संचालन के लिए पर्यवेक्षण, दिशा और नियंत्रण का प्रावधान किस अनुच्छेद में है? इनमें से कोई नहीं" | Article on municipality elections in Chhattisgarh — answer is 'none of these' suggesting data quality issue | OC |
| D50 | MILU/Hindi | 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" | Author of Mughal text Maasir-i-Alamgiri — Mughal history relevant to UPSC | IC |
| D51 | MILU/Hindi | 64 | option3 | "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है?" | 'Iron Man of India' — Sardar Patel, standard UPSC GK | IC |
| D52 | MILU/Hindi | 100 | option2 | "मध्यकालीन काल की सरकार एक मिश्रित संरचना थी। यह किन तत्वों का समामेलन था? फारसी-अरबी, तुर्को-मंगोल - भारतीय तत्व" | Medieval Indian governance structure — UPSC History topic | IC |
| D53 | MILU/Hindi | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" | is_translated=True — electrical engineering question translated from English | IC |
| D54 | MILU/Hindi | 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" | Indirect speech conversion — Hindi language grammar question | IC, IO |
| D55 | MILU/Hindi | 51 | option2 | "दिए गए वाक्य का सही सक्रिय रूप चुनें। सभी को उसके शानदार नृत्य प्रदर्शन ने मोहित कर दिया।" | Active voice conversion — Hindi grammar | IC, IO |
| D56 | MILU/Hindi | 83 | option1 | "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है... आदिवासी लोग जर्जर झोपड़ियों में रह रहे थे" | Ethics/governance scenario for senior civil officer — UPSC GS Paper IV Ethics | IO, IC |
| D57 | MILU/Hindi | 145 | option2 | "कौन सा अक्षर समूह प्रश्न चिह्न (?) को बदलकर दी गई श्रृंखला को पूरा करेगा? एमएनक्यू / एमओक्यू" | Letter series in Hindi transliteration of English letters — code-mixing in reasoning | IC, IF |
| D58 | MILU/Hindi | 18 | option3 | "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था?" | 1991 economic crisis trigger — Indian Economy/Current Affairs (historical) | IO, IC |
| D59 | MILU/Hindi | 119 | option2 | "आरबीआई के नोट जारी करने वाले विभाग के पास हमेशा न्यूनतम कितने मूल्य का सोना होना चाहिए?" | RBI minimum gold reserve requirement — Indian Economy | IO, IC |
| D60 | MILU/Hindi | 28 | option2 | "निम्नलिखित में से कौन खेरवार आंदोलन के नेता थे? भागीरथ मांझी" | Kherwar movement leader — tribal history in Jharkhand/Bihar context | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Strong Indian Polity and Governance Coverage
- **Dimension(s):** IO, IC
- **Observation:** The sample contains numerous questions directly aligned with UPSC/SSC priority topic of Indian Polity and Constitution — covering constitutional amendments (44th, 42nd), parliamentary procedures, Panchayati Raj, writs, and governance acts.
- **Deployment relevance:** Polity is one of the highest-weight subjects for UPSC GS Paper II and SSC General Awareness; these questions directly serve the deployment's primary subject requirements.
- **Datapoint citations:**
  - [D1] Example 33 (MILU/Hindi, validation, option1): "______ एक अदालत का आदेश है जो एक अधीनस्थ अदालत या सार्वजनिक प्राधिकरण को एक आधिकारिक कर्तव्य को सही ढंग से निभाने का निर्देश देता है।" — Mandamus writ definition, UPSC standard question type
  - [D2] Example 6 (MILU/Hindi, validation, option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — 44th Amendment question, core UPSC Polity
  - [D3] Example 39 (MILU/Hindi, validation, option3): "भारत में किस संवैधानिक संशोधन विधेयक द्वारा मतदान की आयु 21 वर्ष से घटाकर 18 वर्ष की गई थी?" — 61st Amendment, standard Polity question
  - [D5] Example 93 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है?" — Panchayati Raj, UPSC/SSC staple
  - [D6] Example 136 (MILU/Hindi, validation, option4): "भारत के संविधान के अनुसार, संसद का कौन सा सदन संविधान संशोधन विधेयक पारित करता है?" — Constitutional amendment procedure

#### Strength 2: Meaningful Indian History Coverage Including Medieval and Modern Periods
- **Dimension(s):** IO, IC
- **Observation:** The sample includes questions on Mughal history, ancient Indian civilization, modern independence movement, and colonial-era governance acts — all core UPSC History syllabus areas.
- **Deployment relevance:** History is a top-priority subject for central exams; these questions represent standard UPSC Prelims question types.
- **Datapoint citations:**
  - [D9] Example 32 (MILU/Hindi, validation, option4): "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया।" — Medieval Delhi Sultanate history
  - [D10] Example 96 (MILU/Hindi, validation, option2): "कौन सा अधिनियम प्रांतों में द्वैध शासन प्रणाली स्थापित करता है?" — Government of India Act 1919, standard modern history
  - [D11] Example 158 (MILU/Hindi, validation, option3): "'देवानांप्रिय' और 'प्रियदर्शी' वे उपाधियाँ थीं जिन्हें राजा ______ ने अपनाया था।" — Ashoka, Ancient Indian History
  - [D50] Example 25 (MILU/Hindi, validation, option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" — Mughal history, North India–relevant
  - [D52] Example 100 (MILU/Hindi, validation, option2): "मध्यकालीन काल की सरकार एक मिश्रित संरचना थी। यह किन तत्वों का समामेलन था?" — Medieval governance structure
  - [D8] Example 199 (MILU/Hindi, validation, option4): "1907 के कांग्रेस सत्र में उदारवादियों और उग्रवादियों के बीच मुख्य अंतर किस विषय पर था?" — Surat Split, modern Indian history

#### Strength 3: Logical Reasoning Representation in the Dataset
- **Dimension(s):** IO
- **Observation:** The sample contains a meaningful number of logical reasoning question types including seating arrangements, syllogisms, blood relations, letter/number series, and coding-decoding — which together constitute a significant share of SSC CGL and banking exam papers.
- **Deployment relevance:** Mathematics/Reasoning is flagged as a top-priority gap in MILU's documented taxonomy, but the actual data confirms Logical Reasoning is represented as a subject under the Science domain, partially addressing the gap for SSC/banking exam prep.
- **Datapoint citations:**
  - [D13] Example 36 (MILU/Hindi, validation, option3): "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है। TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______." — Letter series completion
  - [D17] Example 111 (MILU/Hindi, validation, option3): "आठ लोग दो समानांतर पंक्तियों में बैठे हैं...A के ठीक विपरीत कौन बैठता है?" — Seating arrangement
  - [D18] Example 208 (MILU/Hindi, validation, option4): "कथन: I. कुछ पेन कप हैं। II. सभी कप प्लेट हैं। निष्कर्ष: I. सभी पेन प्लेट हैं।" — Syllogism reasoning
  - [D14] Example 44 (MILU/Hindi, validation, option2): "दिए गए अक्षर श्रृंखला के रिक्त स्थानों में क्रमिक रूप से रखे जाने पर श्रृंखला को पूरा करने वाले अक्षरों के संयोजन का चयन करें। _q p p_p p_p p q_" — Letter pattern

#### Strength 4: Quantitative Aptitude Content Present
- **Dimension(s):** IO
- **Observation:** Several questions involve arithmetic calculations (simple/compound interest, averages, mixture problems) that are representative of the Quantitative Aptitude sections in SSC and banking exams. While labeled under Business Studies/Economics, these are functional math questions.
- **Deployment relevance:** Mathematics/Reasoning is the most critical undocumented gap in MILU's taxonomy; finding actual arithmetic content in the data partially mitigates this concern for SSC/banking preparation.
- **Datapoint citations:**
  - [D15] Example 84 (MILU/Hindi, validation, option3): "सूरज ने अजय से एक निश्चित दर पर साधारण ब्याज पर दो वर्षों के लिए एक राशि उधार ली...दो वर्षों के अंत में उसे 1230 रुपये का चक्रवृद्धि ब्याज प्राप्त हुआ।" — Simple vs. compound interest problem
  - [D16] Example 120 (MILU/Hindi, validation, option4): "किसी कंपनी में सभी कर्मचारियों का औसत वेतन रु. 10500 है...कंपनी में कुल कर्मचारियों की संख्या कितनी है?" — Mixture/average problem

#### Strength 5: North India–Specific Regional Content Present
- **Dimension(s):** IC
- **Observation:** Several questions address knowledge specifically relevant to North Indian states (UP, Rajasthan) — covering state-specific geography (minerals in UP), traditional crafts (Chikankari embroidery), literacy statistics (Rajasthan Census 2011), Rajasthan geography, and agricultural data (milk production leader UP).
- **Deployment relevance:** The deployment requires the AI to handle both pan-India GK and North India sub-regional content. These examples confirm that some such content is present, partially addressing the documented partial gap.
- **Datapoint citations:**
  - [D23] Example 26 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — UP-specific mineral geography
  - [D28] Example 242 (MILU/Hindi, validation, option4): "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है, जिसमें शिफॉन, मलमल, ऑर्गेंजा, ऑर्गेंडी और रेशम जैसे कपड़ों पर नाजुक पारंपरिक हाथ कढ़ाई की जाती है।" — Chikankari (UP embroidery)
  - [D25] Example 156 (MILU/Hindi, validation, option1): "2011 की जनगणना के अनुसार राजस्थान की कुल साक्षरता का लगभग प्रतिशत कितना है?" — Rajasthan state-specific statistics
  - [D27] Example 182 (MILU/Hindi, validation, option1): "निम्नलिखित में से किस राज्य ने 2011-12 में सबसे अधिक दूध उत्पादन दर्ज किया? उत्तर प्रदेश" — UP agricultural data
  - [D29] Example 193 (MILU/Hindi, validation, option3): "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" — Kota painting school (Rajasthan art)

#### Strength 6: Hindi Grammar and Language Proficiency Questions
- **Dimension(s):** IO, IC
- **Observation:** The dataset contains Hindi language grammar questions (active/passive voice, indirect speech, sentence structure) that align with the Hindi Language Proficiency component of central exams (UPSC Mains Hindi compulsory paper, SSC Hindi sections).
- **Deployment relevance:** Hindi language proficiency is listed as a priority subject area; these questions are in pure Hindi and reflect standard Hindi grammar exercises appropriate for the target student.
- **Datapoint citations:**
  - [D54] Example 9 (MILU/Hindi, validation, option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — Indirect speech conversion
  - [D55] Example 51 (MILU/Hindi, validation, option2): "दिए गए वाक्य का सही सक्रिय रूप चुनें। सभी को उसके शानदार नृत्य प्रदर्शन ने मोहित कर दिया।" — Active voice question

#### Strength 7: Ethics and Governance Scenarios (UPSC-Style)
- **Dimension(s):** IO, IC
- **Observation:** Example 83 presents a complex ethical scenario for a civil officer — a format directly mirroring UPSC GS Paper IV (Ethics, Integrity, Aptitude) case studies.
- **Deployment relevance:** UPSC aspirants must prepare for ethics-based scenario questions; this confirms MILU captures this question type, which is otherwise rare in competitive exam benchmarks.
- **Datapoint citations:**
  - [D56] Example 83 (MILU/Hindi, validation, option1): "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है...आदिवासी लोग जर्जर झोपड़ियों में रह रहे थे।" — UPSC-style ethics scenario

#### Strength 8: Indian Economy and Finance Coverage
- **Dimension(s):** IO, IC
- **Observation:** Questions on the 1991 economic crisis, RBI operations, MSP (Minimum Support Price), Five-Year Plans, PMMY (Pradhan Mantri Mudra Yojana), and banking sector are present — all standard Economics/GK topics in central exams.
- **Deployment relevance:** Indian economy is a consistently tested area in UPSC GS Paper III and SSC/banking exams.
- **Datapoint citations:**
  - [D58] Example 18 (MILU/Hindi, validation, option3): "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था?" — 1991 crisis
  - [D59] Example 119 (MILU/Hindi, validation, option2): "आरबीआई के नोट जारी करने वाले विभाग के पास हमेशा न्यूनतम कितने मूल्य का सोना होना चाहिए?" — RBI operations

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete Output Format Mismatch — No Explanatory Rationale Infrastructure
- **Dimension(s):** OO, OF
- **Observation:** Every example in the sample is structured as a 4-option MCQ with a single correct label (`target`). There are no rationale fields, explanation columns, or any annotation supporting the deployment's core output requirement: a substantive Hindi-language explanation of why an answer is correct or incorrect.
- **Deployment relevance:** The deployment explicitly requires "both a correct/incorrect label and a substantive explanation of why the answer is right or wrong, delivered in Hindi" (Elicitation Q3). MILU's schema (question, option1–4, target, is_translated, language, domain, subject) contains no field for rationale. This is a total mismatch with the deployed task; benchmark accuracy scores cannot validate whether a model produces accurate or coherent Hindi explanations. This is confirmed by the benchmark paper itself (Q85) and by the absence of any explanation field across all 245 reviewed examples.
- **Datapoint citations:**
  - [D1] Example 33 (MILU/Hindi, validation, option1): "______ एक अदालत का आदेश है जो एक अधीनस्थ अदालत..." — Correct answer is option1, but no explanation of why mandamus fits the definition is provided
  - [D15] Example 84 (MILU/Hindi, validation, option3): "सूरज ने अजय से एक निश्चित दर पर साधारण ब्याज पर दो वर्षों के लिए एक राशि उधार ली..." — Math problem with answer only; no worked solution or rationale
  - [D56] Example 83 (MILU/Hindi, validation, option1): "एक वरिष्ठ सिविल अधिकारी के रूप में..." — Ethics scenario answer marked option1 with no reasoning explaining why option1 is preferred over other plausible options

---

#### MAJOR

#### MAJOR Concern 1: Truncated/Self-Referential Questions — Construct-Irrelevant Variance
- **Dimension(s):** IF, OC
- **Observation:** A substantial number of questions (at minimum 5 identified in the 245-sample) have answer options that reference items, statements, or sentences that are absent from the question text itself. Options contain labels like "(a), (b), (c), (d)" or "1 2 3 4" or "AEDBCF" without the corresponding items being present in the question field. These appear to be reading-comprehension or list-based questions from which the source material was stripped during data collection, leaving the MCQ shell without the necessary context.
- **Deployment relevance:** A student interacting with these questions cannot evaluate the answer options without the missing content. Any model evaluated on these items is effectively guessing. For the deployment, presenting such incomplete questions would actively harm the student's learning experience, and benchmark accuracy on these items does not measure genuine knowledge.
- **Datapoint citations:**
  - [D43] Example 56 (MILU/Hindi, validation, option2): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें...विकल्प (1) और (3) केवल" — Options reference statements (1)(2)(3)(4) that are absent from question
  - [D44] Example 86 (MILU/Hindi, validation, option2): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" — Options reference states A/B/C/D/E with no list provided
  - [D45] Example 94 (MILU/Hindi, validation, option4): "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? केवल a, d" — Options reference reactions a/b/c/d absent from question
  - [D46] Example 69 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (b), (c) और (d)" — Options reference items (a)–(d) absent
  - [D48] Example 106 (MILU/Hindi, validation, option2): "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" — Substances to be ordered are absent from question
  - [D47] Example 95 (MILU/Hindi, validation, option1): "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं। AEDBCF" — Sentences B/C/D/E absent from question

#### MAJOR Concern 2: 100% Translation Rate in Observed Sample — Unknown Effect on Hindi Register
- **Dimension(s):** IC, IF
- **Observation:** Every single example in the 245-sample (all 245) has `is_translated=True`. This is the entire validation split reviewed. While the overall dataset is documented to have ~25% translated items, the validation split may have a substantially higher translation rate, or there may be a systematic sampling issue. All translated items were produced by GPT-4O, and the Hindi phrasing varies in naturalness.
- **Deployment relevance:** The deployment specifies a ~10% English code-mixing ceiling for Hindi-medium students. Machine-translated questions may use unnatural Hindi phrasing, Sanskritized vocabulary, or carry over English-medium structural conventions. For example, engineering and computer science questions (DC motor, FORTRAN, rectifier) that are entirely technical/specialist in nature appear translated into Hindi with mixed terminology. This inflates the engineering/technical content proportion and may introduce phrasing patterns foreign to Hindi-medium exam-style content.
- **Datapoint citations:**
  - [D53] Example 1 (MILU/Hindi, validation, is_translated=True): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" — Engineering question translated from English; typical Hindi-medium UPSC/SSC exam aspirants would not encounter DC motor questions
  - [D37] Example 8 (MILU/Hindi, validation, is_translated=True): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" — FORTRAN programming language question, translated; not in UPSC/SSC scope

#### MAJOR Concern 3: English-Language Questions Classified as Hindi Content
- **Dimension(s):** IC, IF
- **Observation:** Multiple questions in the Hindi-labeled dataset are substantively about English vocabulary — testing the meaning of English words ('grim', 'didactic', 'Evangelize') or converting English sentences — rather than being Hindi-medium content questions. These are labeled `language=Hindi` and `subject=Language Studies` but require knowledge of English vocabulary, not Hindi.
- **Deployment relevance:** The target student population has limited English exposure; a ~10% code-mixing ceiling applies. English vocabulary synonym questions embedded in the Hindi benchmark are a direct mismatch. A Hindi-medium student who cannot identify the synonym of 'grim' in English is not being tested on any UPSC/SSC competency — these exams do not test English vocabulary for Hindi-medium candidates. Benchmark performance on these items does not reflect the target student's actual exam competency.
- **Datapoint citations:**
  - [D41] Example 90 (MILU/Hindi, validation, option3): "शब्द 'grim' का पर्यायवाची लिखें।" — Asks for a synonym of the English word 'grim'; answer options are in Hindi, but the knowledge tested is English vocabulary
  - [D40] Example 76 (MILU/Hindi, validation, option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" — English vocabulary meaning question
  - [D42] Example 105 (MILU/Hindi, validation, option4): "निर्देश: निम्नलिखित प्रश्न में, चार विकल्पों में से उस शब्द का चयन करें जो दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है। Evangelize" — English word meaning question; options in Hindi but knowledge is English vocabulary

#### MAJOR Concern 4: Substantial Over-Representation of Engineering/Technical Content Irrelevant to Deployment
- **Dimension(s):** IO
- **Observation:** The sample contains a high density of specialist engineering and computer science questions (electrical engineering, FORTRAN programming, AM/FM modulation, DC motors, TDM frame rates, transfer machines, chopper circuits) that fall outside the scope of UPSC/SSC/banking central exam syllabi. These items appear predominantly translated from English and constitute a significant fraction of the sample.
- **Deployment relevance:** UPSC, SSC CGL, and banking exams do not test specialist engineering knowledge at this level. Benchmark accuracy on these items measures specialized engineering knowledge, not the GK/History/Polity/Reasoning competencies that the deployment targets. High model performance on engineering items inflates overall benchmark scores without corresponding validity for the deployment context.
- **Datapoint citations:**
  - [D35] Example 1 (MILU/Hindi, validation): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" — DC series motor behavior (Engineering)
  - [D36] Example 3 (MILU/Hindi, validation): "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" — Half-wave rectifier (Engineering)
  - [D37] Example 8 (MILU/Hindi, validation): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" — FORTRAN programming (Engineering/Computer Science)
  - [D38] Example 104 (MILU/Hindi, validation): "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" — Intermediate frequency for AM receivers (Engineering)

#### MAJOR Concern 5: Current Affairs Questions Are Significantly Dated
- **Dimension(s):** IC, IO
- **Observation:** Current Affairs is one of the most heavily weighted and dynamic UPSC GS areas. The sample contains multiple Current Affairs questions tied to specific dates in 2018–2022, including GDP growth rates for Q2 2018-19, cabinet minister assignments as of 2018, international events in 2019–2022. These questions would have stale or incorrect answers for students preparing for 2024-2026 exams.
- **Deployment relevance:** UPSC Current Affairs directly covers the preceding year; questions about 2018-2022 events are outdated for students currently preparing. A model evaluated highly on these items may still fail on current 2024-2025 affairs questions, and the benchmark cannot capture this currency dimension at all.
- **Datapoint citations:**
  - [D19] Example 74 (MILU/Hindi, validation, option4): "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी?" — GDP figure from 2018-19; outdated for current exam prep
  - [D20] Example 132 (MILU/Hindi, validation, option4): "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं?" — Ministry head as of 2018; politically outdated
  - [D21] Example 88 (MILU/Hindi, validation, option1): "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान एक क्षुद्रग्रह पर उतरा।" — 2019 space event Current Affairs
  - [D22] Example 2 (MILU/Hindi, validation, option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — 2022 sports event, dated

#### MAJOR Concern 6: Significant South India–Specific Content in Hindi Dataset
- **Dimension(s):** IC
- **Observation:** Several questions in the Hindi-labeled sample test knowledge that is specific to South Indian states (Telangana, Andhra Pradesh, Tamil Nadu) or South Indian literary/cultural heritage — including T-Hub Telangana, Tamil classical texts (Silappathikaram), Telangana book ('Telangana Rastrodayamalu'), Tamil cartoons, and Pandya kingdom history. While pan-India GK may include some of this, the density of Telangana/Tamil-specific items in a Hindi deployment is unexpected.
- **Deployment relevance:** Central exam syllabi do cover pan-India GK, but North India–based Hindi-medium students would not encounter these as high-priority preparation topics. Moreover, the benchmark documents that regional state exam questions are pooled across language partitions via translation — these may originate from Telugu/Tamil state exam questions translated into Hindi, representing a category mismatch for central-exam preparation.
- **Datapoint citations:**
  - [D33] Example 126 (MILU/Hindi, validation, option3): "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" — Telangana-specific literary question
  - [D34] Example 41 (MILU/Hindi, validation, option1): "टी-हब तेलंगाना राज्य सरकार की एक पहल है" — Telangana state government policy
  - [D32] Example 108 (MILU/Hindi, validation, option3): "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" — Tamil literary history question
  - [D31] Example 52 (MILU/Hindi, validation, option2): "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था" — Pandya kingdom (South Indian history)

---

#### MINOR

#### MINOR Concern 1: Reasoning Questions Use Transliterated English Letters, Introducing Mild Code-Mixing
- **Dimension(s):** IC, IF
- **Observation:** Some logical reasoning questions use transliterated English letter names in Hindi script (e.g., "एमएनक्यू", "एमओक्यू" for MNQ, MOQ) rather than Hindi-medium equivalent notation. While this is a minor form of code-mixing, it may create unnatural reading for students accustomed to Hindi-medium reasoning materials.
- **Deployment relevance:** The ~10% code-mixing ceiling is set for content, not isolated letter labels in pattern sequences; this is likely acceptable. However, the transliteration may be less natural than using the Latin letters directly (which Hindi-medium exam books do routinely).
- **Datapoint citations:**
  - [D57] Example 145 (MILU/Hindi, validation, option2): "कौन सा अक्षर समूह प्रश्न चिह्न (?) को बदलकर दी गई श्रृंखला को पूरा करेगा? एमएनक्यू / एमओक्यू" — Transliterated letter group names

#### MINOR Concern 2: Potential Answer Quality Issue — 'None of These' as Correct Answer for Factual Question
- **Dimension(s):** OC
- **Observation:** Example 109 asks about the constitutional article governing municipal election supervision in Chhattisgarh and the correct answer is "इनमें से कोई नहीं" (none of these). The provided options include Articles 243(ख), 243(क), and 241(ग). 'None of these' as the correct answer for a specific constitutional article question raises a potential data quality concern — either the correct article number was not included in the options, or the source portal recorded an ambiguous answer.
- **Deployment relevance:** Questions where 'none of these' is the correct answer are inherently difficult to explain in a rationale-based deployment, and may reflect data quality issues from the scraping pipeline (correct option not included in the option set).
- **Datapoint citations:**
  - [D49] Example 109 (MILU/Hindi, validation, option4): "छत्तीसगढ़ में नगरपालिकाओं के सभी चुनावों के संचालन के लिए पर्यवेक्षण, दिशा और नियंत्रण का प्रावधान किस अनुच्छेद में है? इनमें से कोई नहीं" — 'None of these' as answer to specific constitutional article query

#### MINOR Concern 3: Non-India–Specific Literary Questions with Low Deployment Relevance
- **Dimension(s):** IC
- **Observation:** A small number of questions test knowledge about non-Indian subjects that are tangentially connected to India's GK scope — such as the nationality of William Wordsworth or the 2019 Man Booker Prize winner (Bernadine Evaristo). These may appear in some competitive exam general awareness sections but are at the periphery of UPSC/SSC core content.
- **Deployment relevance:** These items represent minor dilution of deployment-relevant content. Their presence is not harmful but adds noise for the target student population.
- **Datapoint citations:**
  - [D39] Example 7 (MILU/Hindi, validation, option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं।" — Wordsworth's nationality, borderline relevance to central exam GK

---

### Content Coverage Summary

The 245-sample Hindi validation set covers a broad range of subjects with meaningful representation of Indian Polity/Constitution, Indian History (ancient, medieval, and modern), Indian Economy, Environmental Science/Geography, and Health/Medicine. Logical Reasoning (seating arrangements, syllogisms, blood relations, coding-decoding, series completion) is present as a subject under the Science domain, partially addressing the documented taxonomy gap. Quantitative arithmetic questions (simple/compound interest, averages) appear within Business Studies/Economics.

North India–specific content is present but not dominant: examples covering UP minerals, Chikankari (UP embroidery), Rajasthan geography and literacy, Kota painting, and Bihar/UP agricultural data confirm some sub-regional coverage. However, the sample does not include Chhath Puja, zamindari/land-revenue history, or North Indian freedom movement figures beyond Sardar Patel and general mentions.

A notable characteristic is that 100% of the 245 reviewed examples have `is_translated=True`, which may reflect the composition of the validation split specifically. The translated items include heavy representation of specialist Engineering & Technology and Computer Science content (DC motors, FORTRAN, AM/FM modulation, rectifiers) that falls outside UPSC/SSC/banking central exam syllabi. Several questions are structurally incomplete — answer options reference lists, statements, or sentences absent from the question text, likely artifacts of the source portal scraping process.

Current Affairs content is present but dated to 2018–2022, creating a staleness concern for students preparing for 2025–2026 central exams. English vocabulary questions (synonym/meaning of 'grim', 'didactic', 'Evangelize') are labeled as Hindi Language Studies content but test English word knowledge, which is misaligned with Hindi-medium students' target exam requirements.

The benchmark has no rationale or explanation fields — every item is a bare MCQ with a correct label only.

---

### Limitations

1. **Translation rate in validation split**: All 245 reviewed examples have `is_translated=True`. It is unclear whether this reflects the full validation split composition or a systematic ordering in the parquet file. The test split (14,831 examples) likely has a substantially different translation rate and subject distribution; findings about over-representation of engineering content and translation artifacts may not fully generalize.

2. **Sample size relative to total dataset**: 245 examples from a 14,831-example test set and 812-example validation set; topic distribution within the full dataset may differ from the sample. Rare subjects (Chhath Puja, land-revenue systems, specific North Indian historical figures) may be present in the full test set but absent from this sample.

3. **No inspection of test split**: The test set (14,831 examples) was not reviewed. Domain/subject distribution, translation rates, and data quality issues (truncated questions) in the test split are unconfirmed.

4. **Code-mixing cannot be quantified**: While specific English terms (RMS, AM, PCM, RBI, GDP, FORTRAN) appear in questions, a systematic quantitative estimate of English term density per question is not possible from manual review of 245 examples.

5. **Answer correctness not independently verifiable**: The target labels are inherited from exam portal answer keys. For the ~5 structurally truncated questions (where option lists are absent), the correctness of the labeled answer cannot be assessed without the original source.

6. **North India sub-regional coverage**: The sample confirms some UP/Rajasthan content but cannot establish whether Chhath Puja, zamindari abolition, specific North Indian freedom fighters, or Bihar-specific history appear in the test set at deployable density.

7. **Validation split composition uncertainty**: The fact that all 245 validation examples are translated may indicate the validation split was specifically constructed from translated items, or may be a coincidence of sampling order. This cannot be resolved without examining the full split statistics.

