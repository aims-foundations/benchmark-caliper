## Deployment Context

**Use case:** Deployment scenario: A Hindi-speaking student in India is testing his/her preparation for competitive job-related examinations, with an AI system providing feedback on their responses. The goal is to evaluate the applicability of the benchmark and the quality of the LLM’s feedback.

Domain: Educational assessment
Setting: Mobile application / enterprise software

Note: The deployment hypothesis should be tested using Hindi-language sentences from the benchmark, as I am familiar with the language and can provide evaluation in a subsequent stage.
**Target population:** A graduate student in North India interacting in the Hindi language. The student has completed their education primarily in Hindi, with limited exposure to English.

# Validity Analysis: mmlu
**Target context:** North India Competitive Exam Aspirants (Hindi-Medium)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ⚠ | 1 | Serious concern | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 2 | Significant gaps | high |
| **Average** | **1.2** | | |

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

MMLU is a near-total mismatch for the North India Hindi-medium competitive exam deployment across five of six validity dimensions. Subject coverage is anchored in US/Western academic curriculum with zero Indian Polity, Indian History, Indian Geography, Current Affairs, or Hindi-language content (the high-priority domains identified in elicitation). Individual items are culturally embedded in US institutional, legal, demographic, and moral contexts; where India does appear, it is filtered through colonial or Western-pollster framing incompatible with the NCERT/Bipin Chandra-aligned exam-prep tradition. The benchmark is entirely English with no Devanagari content, conflicting with the deployment's Hindi-dominant input requirement. Output is label-only with no rationale evaluation, while the deployment requires substantive Hindi explanatory feedback. Annotator pool is undocumented but US-anchored; moral_scenarios labels are explicitly framed in US 2020 norms. Output form is the only dimension with a partial structural match (MCQ format), but even that is undermined by calibration failures and absence of generative-quality measurement. Indian-grounded alternatives (MILU, ParamBench, IndicEval, IndicMMLU-Pro) exist and should be primary; MMLU at best provides weak proxy signal on STEM/reasoning subdomains.

## Practical Guidance

### What This Benchmark Measures

MMLU measures broad English-language multitask classification accuracy on a US/Western academic curriculum, with strongest signal on culturally-neutral STEM (mathematics, physics, computer science) and weakest on humanities, law, and morality. For the NI-CEA deployment, MMLU can provide only weak proxy evidence for the Mathematics & Reasoning domain (one of several high-priority areas) and provides no signal at all on Indian Polity, Indian History, Indian Geography, Current Affairs, Hindi proficiency, or Hindi explanatory feedback quality.

### Construct Depth

MMLU probes breadth across 57 subjects but at modest depth (5-shot prompts, label-only scoring [Q34, Q44]). For the deployment's core constructs — India-grounded factual knowledge, Hindi-medium comprehension, and Hindi pedagogical explanation — MMLU's depth is effectively zero. The English-vs-Hindi performance gap documented in IndicEval [WEB-16] confirms that MMLU's English-medium scores do not predict Hindi-medium ability even on overlapping content.

### What Else You Need

Substantial supplementation is required. (1) For Input Ontology / Input Content, use MILU [WEB-13, WEB-14] and ParamBench [WEB-15] as primary benchmarks; they cover UPSC/SSC-relevant Indian curriculum content in Hindi. (2) For Input Form, use IndicEval [WEB-16] or IndicMMLU-Pro [WEB-18] to measure Hindi-medium degradation. (3) For Output Ontology / Output Form (Hindi explanatory feedback), commission a custom rubric — no existing benchmark covers this gap [WEB-21]. (4) For Output Content, conduct Indian-SME annotation review on any MMLU items used. (5) For Current Affairs, build a continuously-updated PIB/Yojana-sourced evaluation set, since static benchmarks cannot cover this domain.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MMLU's 57-subject taxonomy is anchored in a US/Western academic curriculum [Q1, Q8, Q16] with subjects calibrated to US bar-exam, USMLE, and US-foreign-policy concerns [Q17, Q49]. None of the high-priority Indian competitive exam domains identified in the elicitation (Indian Polity & Constitution, Indian History, Current Affairs, Indian Geography, Hindi language proficiency) is represented. Dataset analysis confirms across ~200 sampled items zero coverage of Indian Polity, Indian History, or Indian Geography; the only South Asian content is two Jainism items in world_religions and one colonial-framed 1857 item. Partial overlap exists for STEM/mathematics and reasoning, which are universally applicable, but this is a small fraction of the deployment's high-priority surface.

**Strengths:**
- Mathematics, abstract algebra, computer science, and conceptual physics items are culturally neutral and provide partial proxy signal for SSC quantitative aptitude / UPSC CSAT reasoning [DATASET-D27, D29, D30, D40].
- NCERT-overlapping science content (biology, virology, evolution) gives weak-but-positive signal for Indian GK science sections [DATASET-D41, D42].

**Checklist:**

- **IO-1**: Required categories per elicitation: General Knowledge (India-centric), Current Affairs, Indian History (ancient/medieval/modern), Indian Polity & Constitution, Mathematics & Reasoning, Hindi language proficiency, with supplementary Indian Geography and Indian Economy. — _Sources: WEB-5, WEB-6_
- **IO-2**: MMLU omits all India-centric categories. The history component claims wide geographic scope [Q27] but sampled items show European and US history exclusively [DATASET-D4, D5, D12, D13, D14]. No Hindi proficiency, no Indian Polity, no Current Affairs subject [Q104]. — _Sources: Q27, Q104, DATASET-D4, DATASET-D5, DATASET-D12_
- **IO-3**: MMLU includes US-jurisdiction-specific categories (professional_law calibrated to US bar exam [Q17], professional_accounting on US CPA standards [DATASET-D32], us_foreign_policy [DATASET-D7, D8, D9], moral_scenarios anchored to US 2020 norms [DATASET-D18, D19]) that are construct-irrelevant for the deployment. — _Sources: Q17, DATASET-D7, DATASET-D8, DATASET-D18, DATASET-D32_
- **IO-4**: Content validity is severely harmed: the benchmark's subject taxonomy [Q104] does not map onto the UPSC/SSC syllabus published at upsc.gov.in [WEB-5] or ssc.gov.in [WEB-6]. Indian-curriculum-grounded benchmarks (MILU, ParamBench, IndicEval) demonstrate that this gap is addressable but absent from MMLU itself. — _Sources: Q104, WEB-5, WEB-13, WEB-15_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more.' (p.1)
- [Q8] 'The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more.' (p.1)
- [Q17] 'practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination' (p.3)
- [Q104] 'Table 2: Summary of all 57 tasks.' (p.15)

*Web sources:*
- [WEB-5] UPSC official syllabus published at upsc.gov.in
- [WEB-6] SSC CGL/CHSL syllabus at ssc.gov.in
- [WEB-13] MILU benchmark covers 8 domains and 41 subjects from Indian competitive exams in 11 Indic languages
- [WEB-15] ParamBench: 17K+ Hindi-language UGC-NET/UPSC questions across 21 Indic subjects

*Dataset analysis:*
- DATASET-D1, D2, D3: high_school_government_and_politics covers exclusively US constitutional content
- DATASET-D4, D5, D6: high_school_us_history items use US primary sources
- DATASET-D12, D13, D14: high_school_european_history dominated by Western European content
- DATASET-D35, D36: only two Jainism items represent South Asian religious content across ~200 samples

</details>

**Information gaps:**
- Whether any subset of MMLU's miscellaneous or global_facts items can be systematically mapped to UPSC GS general-awareness sub-topics.

**Requires expert verification:**
- Mapping of MMLU mathematics items to specific UPSC CSAT / SSC CGL quantitative aptitude topics by an Indian exam-prep subject-matter expert.

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Individual MMLU items are culturally anchored in US/Western contexts: US Congress and constitutional history [DATASET-D1, D2, D3], US bar-exam tort scenarios [DATASET-D10, D11], Western philosophical canon [DATASET-D16, D17], US Social Security and birth-control demographics [DATASET-D20, D21], US measurement units in mathematics [DATASET-D25, D28], and CPA/MCAT institutional referents [DATASET-D32, D48]. The benchmark assumes models acquired requisite knowledge from 'vast quantities of diverse Internet text' [Q60], which is overwhelmingly English-Western. The deployment requires both pan-India and North India–specific factual content (Chhath Puja, Panchayati Raj, tehsils, NCERT-aligned narratives) per elicitation Q2, none of which appears in the sampled items. Where India is referenced, it is via Pew Research statistics [DATASET-D23, D24] or colonial-British framing of the 1857 uprising [DATASET-D15] — both incompatible with NCERT/Bipin Chandra-aligned exam preparation.

**Strengths:**
- Pure-mathematics items (abstract algebra, probability) are content-culturally neutral and transfer cleanly [DATASET-D27, D30].
- Some basic NCERT-overlapping science facts (smallpox eradication, evolution) are factually correct in an Indian curriculum context [DATASET-D41, D42].

**Checklist:**

- **IC-1**: Yes — the deployment requires India-centric cultural and administrative knowledge (festivals like Chhath Puja, tehsils, mandals, North Indian historical figures, NCERT-aligned narratives) per elicitation Q2; MMLU items do not address these. — _Sources: Q60, DATASET-D23_
- **IC-2**: No — culturally sensitive content in MMLU (moral_scenarios explicitly framed as 'US 2020 moral standards' [DATASET-D18, D19]; jurisprudence using US product liability [DATASET-D33]) does not align with Indian deployment culture. — _Sources: DATASET-D18, DATASET-D19, DATASET-D33_
- **IC-3**: Yes — extensive Western-specific knowledge requirements: US tax law [Q152], US bar-exam scenarios [Q153], US CPA standards [DATASET-D32], MCAT framing [DATASET-D48], US traffic conventions [DATASET-D45], and US customary measurement units in arithmetic [DATASET-D25, D28]. — _Sources: Q152, Q153, DATASET-D32, DATASET-D45, DATASET-D25_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the paper does not document any review of items by Indian regional annotators; would need a systematic Indian SME audit to identify all culturally sensitive instances.
- **IC-5**: Content validity is severely harmed: when India does appear (D15, D47), the framing privileges colonial historiography over the nationalist NCERT/Bipin Chandra narrative central to UPSC preparation, creating direct misalignment for exam-prep use. — _Sources: DATASET-D15, DATASET-D47, WEB-20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q17] 'manually collected by graduate and undergraduate students from freely available sources online... Graduate Record Examination and the United States Medical Licensing Examination' (p.3)
- [Q60] 'we assume that models have acquired the requisite knowledge from reading vast quantities of diverse text from the Internet' (p.7)
- [Q152] 'Krete is an unmarried taxpayer with income exclusively from wages... federal income taxes' (p.24)
- [Q153] 'The night before his bar examination... discharge a firearm in public.' (p.24)

*Web sources:*
- [WEB-20] Translated MMLU variants suffer cultural mismatch because content (US History, Law) remains Western-specific even in Hindi

*Dataset analysis:*
- DATASET-D10, D11, D33: US tort/contract law scenarios
- DATASET-D15, D47: 1857 uprising rendered through colonial British journalist's lens
- DATASET-D18, D19: moral_scenarios explicitly grounded in 'US 2020 moral standards'
- DATASET-D25, D28: US customary units (miles, feet) in arithmetic
- DATASET-D23, D24: India-referencing items source Pew Research statistics rather than UPSC GK conventions
- DATASET-D37: Indian name 'Jyoti' inserted in Western rock-concert context — surface-level rather than substantive

</details>

**Information gaps:**
- Full enumeration of India-relevant items beyond the ~200 sampled would require complete corpus review of all 14,079 test items.
- Annotator-side cultural assumptions are not documented in the paper.

**Requires expert verification:**
- Indian SME review of moral_scenarios and jurisprudence items to determine extent of label flips under Indian normative frameworks.
- Audit of how 1857 / colonial history items would be scored against NCERT-aligned answer expectations.

---

### Input Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MMLU is entirely English-language, text-only, with a standardised English preamble for prompts [Q44] and English-only normalised input format for UnifiedQA [Q91]. Dataset metadata confirms 'languages: [en]' and monolingual content; no Devanagari script or Hindi vocabulary appears in any of the ~200 sampled items. The deployment requires Hindi-dominant interaction in Devanagari script with at most ~10% English code-mixing per elicitation Q4. The MCQ structural format (4 options A/B/C/D) is a partial structural match to UPSC/SSC exam formats, but this is overridden by total language and script mismatch. IndicEval [WEB-16] empirically demonstrates a large Hindi-vs-English performance gap (LLaMA 39.53% on UPSC Hindi Zero-Shot vs. ~84.88% Gemini on UPSC English CoT), confirming that English-medium MMLU scores cannot predict Hindi-medium performance.

**Strengths:**
- Four-option MCQ structure (A/B/C/D) [Q44, Q83] is a structural match to UPSC Prelims, SSC CGL, and banking exam formats [DATASET strength 1].
- Text-only modality is appropriate for the deployment's text-based MCQ context (per elicitation deployment description, mobile/enterprise application is text-driven).

**Checklist:**

- **IF-1**: Severe mismatch — MMLU input distribution is 100% English text [Q44, Q91]; deployment input distribution is Hindi (Devanagari) with up to ~10% English code-mixing. — _Sources: Q44, Q91, WEB-16_
- **IF-2**: Regional infrastructure does support Devanagari rendering (Gboard, SwiftKey Hindi available) but the benchmark provides no Devanagari content to evaluate; Hindi tokenization quality is a documented live deployment risk [WEB-1]. — _Sources: WEB-1_
- **IF-3**: Form-relevant differences: MMLU uses no Devanagari script, no Hindi morphology, no code-mixed Hinglish; mathematics items use US customary units (miles, feet) rather than SI units used in Indian exams [DATASET-D25, D28]. — _Sources: Q59, DATASET-D25, DATASET-D28_
- **IF-4**: External validity is severely harmed: MMLU accuracy on English inputs provides no evidence about model performance on Hindi-medium inputs; IndicEval [WEB-16] documents catastrophic multilingual degradation. — _Sources: WEB-16_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q7] 'evaluating models exclusively in zero-shot and few-shot settings' (p.1)
- [Q44] 'We begin each prompt with "The following are multiple choice questions (with answers) about [subject]"... up to 5 demonstration examples... All prompts end with "Answer: "' (p.6)
- [Q59] 'we design our benchmark to capture a diverse array of tasks in a text-only format' (p.7)
- [Q91] 'questions and choices are normalized and made lowercase' (p.12)

*Web sources:*
- [WEB-1] Devanagari tokenization quality is a live deployment risk; even models trained on 20B Hindi tokens hallucinate or mix in English
- [WEB-16] IndicEval documents marked accuracy drops in Hindi vs. English (LLaMA 39.53% UPSC Hindi Zero-Shot)
- [WEB-17] OpenAI MMMLU provides Hindi translation but does not change underlying Western content

*Dataset analysis:*
- DATASET strength 1: every sampled item is four-option MCQ — structural format match
- DATASET concern 2: every question, option, and label is English; HF metadata confirms 'languages: [en]'
- DATASET-D25, D28: US customary units (miles, feet) in math items

</details>

**Information gaps:**
- Quality of community Hindi MMLU translations (OpenAI MMMLU, IndicMMLU-Pro) is documented in web sources but not directly assessed here.

**Requires expert verification:**
- Hindi linguistic review of any translated MMLU variant for register appropriateness (Manak Hindi vs. literal translation) for exam-prep context.

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MMLU's output ontology is a four-class A/B/C/D classification [Q83, Q44] with classification accuracy as the sole performance criterion [Q34, Q23]. Dataset analysis confirms a single ClassLabel field (0–3) with no rationale field. The deployment requires a fundamentally richer output taxonomy: a verdict (sahi/galat) plus a substantive Hindi-language explanation in standard Manak Hindi [elicitation Q3]. MMLU's design provides zero signal on the model's capacity to produce explanatory rationale, let alone in Hindi. The benchmark's stated rationale for the simple format ('a simple-to-evaluate test that measures classification accuracy' [Q23]) is internally coherent but structurally incompatible with the deployment's pedagogical-feedback requirement.

**Strengths:**
- Verdict component (correct vs. incorrect) is a partial match — the A/B/C/D classification can be reduced to a binary correct/incorrect signal that does align with one component of the deployment output (the sahi/galat label) [Q83, DATASET concern 3].

**Checklist:**

- **OO-1**: Output labels (A/B/C/D) [Q83] partially match the deployment's required correctness verdict but entirely omit the explanation component. Deployment requires Hindi explanatory feedback per elicitation Q3. — _Sources: Q83, Q44_
- **OO-2**: Missing categories: free-form Hindi explanation, distractor analysis (why each wrong option is wrong), and reference to canonical Indian sources (NCERT, Laxmikant). None are represented in MMLU's output schema. — _Sources: Q23, Q34_
- **OO-3**: Output categories themselves are content-neutral (letter labels), but the underlying scoring rule treats US-anchored answer keys (e.g., moral_scenarios under US 2020 norms [DATASET-D18, D19]) as correctness ground truth, encoding non-regional values. — _Sources: DATASET-D18, DATASET-D19_
- **OO-4**: A stakeholder-driven output taxonomy redesign is required: minimum {verdict_label, hindi_explanation_text, optional_distractor_analysis} with a separate rubric for explanation quality. No existing benchmark covers this — the rubric gap is documented as unresolved [WEB-21]. — _Sources: WEB-21, WEB-13, WEB-15_
- **OO-5**: Structural and content validity are severely harmed: MMLU's output structure measures only one of two required output components and applies decision rules anchored in US norms. — _Sources: Q23, Q62_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q23] 'we instead create a simple-to-evaluate test that measures classification accuracy on multiple choice questions.' (p.3)
- [Q34] 'we compute the classification accuracy across all examples and tasks.' (p.5)
- [Q83] 'Models are fine-tuned to predict one of four classes' (p.12)
- [Q62] 'the format of our evaluation is not identical to the format in which information is acquired during pretraining.' (p.8)

*Web sources:*
- [WEB-21] No benchmark evaluating Hindi explanatory rationale quality for competitive exam contexts was found — genuine gap
- [WEB-13] MILU evaluates MCQ label accuracy only, not free-form Hindi explanations
- [WEB-15] ParamBench evaluates MCQ accuracy only

*Dataset analysis:*
- DATASET concern 3: every MMLU example has a single scalar `answer` field (ClassLabel 0–3); no rationale field exists
- DATASET-D18, D19: scoring rule explicitly anchored to 'US 2020 moral standards'

</details>

**Information gaps:**
- No published rubric for Hindi exam-prep explanation quality [WEB-21] — cannot quantify the magnitude of the output-ontology gap.

**Requires expert verification:**
- Indian exam-prep pedagogues need to define an explanation-quality rubric (factual accuracy, distractor analysis, Manak Hindi register, NCERT alignment) for the deployment.

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The paper is silent on annotator demographics, qualifications, IAA protocols, and label-validation procedures — Output Content concerns are explicitly NOT DOCUMENTED in the benchmark write-up. Questions were assembled by US graduate/undergraduate students [Q17] and validated against US-standard answer keys. No Indian SMEs, UPSC/SSC specialists, or Hindi-medium educators participated. For India-relevant items that do appear (DATASET-D15 1857 uprising), the answer keys privilege colonial historiography over NCERT/Bipin Chandra nationalist framing, directly conflicting with what Indian exam stakeholders would judge correct. moral_scenarios labels are explicitly anchored to 'ordinary moral standards in the US as of 2020' [DATASET-D18, D19], producing systematic OC misalignment for the target population. Even the strongest Indian-grounded benchmarks (ParamBench, MILU) only partially document Indian-SME involvement [WEB-15, WEB-13]; MMLU documents none.

**Strengths:**
- For purely-cultural-neutral STEM items (abstract algebra, conceptual physics), label correctness is unlikely to depend on annotator culture — these labels probably transfer to Indian stakeholders [DATASET-D27, D30, D40].
- Memorization analysis suggests low risk that exact questions were leaked into pretraining [Q98, Q99], so labels are not artifacts of test contamination.

**Checklist:**

- **OC-1**: No — labels reflect US-educated annotator perspectives [Q17]; for India-centric content, Indian stakeholder perspectives are unrepresented. — _Sources: Q17_
- **OC-2**: Significant disagreement is plausible for moral_scenarios (US 2020 norms vs. Indian norms) [DATASET-D18, D19], for high_school_world_history items framed via colonial sources [DATASET-D15, D47], and for any Indian-content item validated against non-Indian answer keys. — _Sources: DATASET-D18, DATASET-D19, DATASET-D15_
- **OC-3**: INSUFFICIENT DOCUMENTATION — paper does not include a Datasheet or Data Statement section addressing annotator demographics; only [Q17] notes 'graduate and undergraduate students' without further detail.
- **OC-4**: Re-annotation by representative Indian annotator pool is necessary for any India-deployment use; ParamBench [WEB-15] provides a partial template but does not cover MMLU items. — _Sources: WEB-15_
- **OC-5**: INSUFFICIENT DOCUMENTATION — aggregation methods for label disagreements are not described; cannot assess minority-perspective erasure.
- **OC-6**: Convergent and external validity are severely harmed: MMLU labels do not correlate with Indian-stakeholder judgments on culturally embedded items, and US-norm-anchored labels do not generalize to Indian deployment context. — _Sources: DATASET-D18, DATASET-D15, WEB-13_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q17] 'manually collected by graduate and undergraduate students from freely available sources online' (p.3)
- [Q98] 'accuracy and question entropy are not positively correlated' (p.14)
- [Q99] 'This suggests that our exact questions were not memorized.' (p.14)
- [Q100] 'during pretraining models encountered text related to our questions through processing Wikipedia.' (p.14)

*Web sources:*
- [WEB-15] ParamBench uses two-tier annotation team with Indian-context expert review — contrast model for what MMLU lacks
- [WEB-13] MILU derives labels from official Indian competitive exams — implicit Indian-stakeholder validity that MMLU lacks

*Dataset analysis:*
- DATASET-D18, D19: moral_scenarios explicitly invokes 'US 2020 moral standards' as scoring ground truth
- DATASET-D15, D47: 1857 item label privileges colonial framing over NCERT nationalist narrative — direct OC misalignment for Indian deployment

</details>

**Information gaps:**
- Annotator demographics, IAA protocols, label-disagreement aggregation — none documented in paper.
- Whether any cross-cultural annotation comparison has been performed for MMLU labels.

**Requires expert verification:**
- Indian SME re-annotation of moral_scenarios, jurisprudence, and any Indian-content items to quantify label-flip rate.
- Comparison of MMLU answer keys against UPSC/SSC official answer keys for any overlapping content.

---

### Output Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Output form is the dimension with the strongest partial match — both MMLU and the deployment use text-based MCQ as the interaction vehicle, and the binary correct/incorrect verdict can in principle be derived from MMLU's A/B/C/D output [Q83]. However, MMLU evaluates only single-letter classification accuracy [Q34, Q41]; it does not evaluate any natural-language rationale, Hindi fluency, or pedagogical appropriateness. Calibration failures further reduce the value of MMLU's confidence outputs as deployment signal: GPT-3 confidence deviates from accuracy by up to 24% zero-shot [Q57] and 14% few-shot [Q96], with Elementary Mathematics RMS error of 19.4% [Q58]. Given the deployment's negative-marking exam context where confidence calibration matters, this is a real concern. The MODERATE priority weight from elicitation reflects this partial match — score is 2 rather than 1 because the structural MCQ alignment provides some external validity.

**Strengths:**
- Text-based MCQ output form is a partial match to deployment interaction vehicle [Q44, DATASET strength 1].
- Balanced label distribution across A/B/C/D classes prevents position-bias artifacts [DATASET strength 3].
- Confidence/calibration measurement framework [Q56, Q58] is methodologically transferable, even if the specific MMLU calibration findings are not directly applicable.

**Checklist:**

- **OF-1**: Partial match — MCQ text output is appropriate, but the deployment also requires generative Hindi explanatory text which MMLU does not evaluate. — _Sources: Q34, DATASET strength 1_
- **OF-2**: Not applicable — deployment is text-based, not speech-based; TTS availability is not a primary requirement per elicitation.
- **OF-3**: Literacy is not a barrier for the deployment population (graduate-level aspirants per region YAML); however, mobile-first low-bandwidth constraints apply [WEB-10] and rural shared-device usage is documented [WEB-12]. — _Sources: WEB-10_
- **OF-4**: External validity is partially harmed: a model's MMLU label-accuracy and calibration scores do not predict its capacity to produce coherent Hindi explanatory output, and calibration failures up to 24% [Q57] mean confidence signals do not transfer reliably. — _Sources: Q57, Q96, WEB-21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q34] 'we compute the classification accuracy across all examples and tasks.' (p.5)
- [Q41] 'All values are percentages.' (p.5)
- [Q57] 'its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects.' (p.7)
- [Q96] 'gap between accuracy and confidence reaching up to 14%' (p.13)

*Web sources:*
- [WEB-10] IAMAI/Kantar 2024: Bihar 43%, UP 46% internet penetration — relevant for mobile-first deployment constraints
- [WEB-21] No Hindi exam-prep explanation-quality rubric exists

*Dataset analysis:*
- DATASET strength 1: four-option MCQ format structurally matches Indian competitive exam format
- DATASET strength 3: balanced A/B/C/D label distribution
- DATASET concern 3: label-only output structure with no rationale field

</details>

**Information gaps:**
- How well MMLU's calibration framework translates to a Hindi-output context is not empirically tested.

**Requires expert verification:**
- Mobile-device performance of any MMLU-evaluated model on the deployment hardware profile (mid-range Android, intermittent connectivity).

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Zero coverage of Indian Polity, Indian History, Indian Geography, Current Affairs, Hindi proficiency — the core UPSC/SSC syllabus.

**Recommendation:** Replace MMLU as primary evaluation with MILU [WEB-13] and ParamBench [WEB-15], which cover UPSC/UGC-NET-relevant Indian content. Use MMLU at most as a STEM-subset proxy after filtering to abstract_algebra, college/high_school_mathematics, conceptual_physics, college_computer_science.

### Input Content ⚠

**Gap:** US measurement units (miles, feet) in mathematics; US institutional referents (CPA, MCAT, Social Security) introduce construct-irrelevant variance.

**Recommendation:** If MMLU mathematics items are reused, locally adapt unit conventions to SI/metric and replace US-institution-specific framings; alternatively, source quantitative-aptitude items directly from SSC CGL / UPSC CSAT past papers.

### Input Form ⚠

**Gap:** 100% English input with no Devanagari script; deployment requires Hindi-dominant input.

**Recommendation:** Adopt IndicEval [WEB-16] for direct UPSC-Hindi performance measurement and IndicMMLU-Pro [WEB-18] for broader Hindi-translation assessment. Treat any English-MMLU score as upper-bound only; expect substantial Hindi-medium degradation.

### Output Ontology ⚠

**Gap:** Label-only A/B/C/D output cannot evaluate the required Hindi explanatory feedback.

**Recommendation:** Commission a Hindi exam-prep explanation-quality rubric (factual accuracy, distractor analysis, Manak Hindi register, NCERT alignment) with Indian SME panel — this is a documented gap in current literature [WEB-21] and must be built bespoke for the deployment.

### Output Content ⚠

**Gap:** US-anchored annotator pool and US-norm scoring (especially moral_scenarios, jurisprudence, world_history); zero documented Indian SME review.

**Recommendation:** Conduct Indian-SME re-annotation of any MMLU items retained for STEM proxy use; for India-relevant content, rely on benchmarks with documented Indian annotation chains (ParamBench [WEB-15], MILU [WEB-13]).

### Output Form

**Gap:** Calibration failures (up to 24% off [Q57]) reduce reliability of confidence signals in a negative-marking exam context.

**Recommendation:** Add explicit calibration measurement on Hindi-medium UPSC/SSC items (e.g., RMS calibration error per subject) using the methodology from MMLU [Q58] but applied to Indian-curriculum benchmarks; require model abstention support for negative-marking scenarios.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "We propose a new test to measure a text model's multitask accuracy. The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more." |
| Q2 | 1 | input_content | "To attain high accuracy on this test, models must possess extensive world knowledge and problem solving ability." |
| Q3 | 1 | output_form | "We find that while most recent models have near random-chance accuracy, the very largest GPT-3 model improves over random chance by almost 20 percentage points on average." |
| Q4 | 1 | output_ontology | "However, on every one of the 57 tasks, the best models still need substantial improvements before they can reach expert-level accuracy." |
| Q5 | 1 | output_ontology | "Models also have lopsided performance and frequently do not know when they are wrong." |
| Q6 | 1 | output_ontology | "Worse, they still have near-random accuracy on some socially important subjects such as morality and law." |
| Q7 | 1 | input_form | "We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings." |
| Q8 | 1 | input_ontology | "The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more. It ranges in difficulty from an elementary level to an advanced professional level, and it tests both world knowledge and problem solving ability." |
| Q9 | 1 | input_content | "Dan Hendrycks UC Berkeley, Collin Burns Columbia University, Steven Basart UChicago, Andy Zou UC Berkeley, Mantas Mazeika UIUC, Dawn Song UC Berkeley, Jacob Steinhardt UC Berkeley" |
| Q10 | 2 | input_ontology | "Since our test consists in 57 tasks, it can be used to analyze aggregate properties of models across tasks and to track important shortcomings." |
| Q11 | 2 | output_form | "We find that meaningful progress on our benchmark has only become possible in recent months. In particular, few-shot models up to 13 billion parameters (Brown et al., 2020) achieve random chance performance of 25% accuracy, but the 175 billion parameter GPT-3 model reaches a much higher 43.9% accuracy (see Figure 1b)." |
| Q12 | 2 | output_form | "On the other hand, unlike human professionals GPT-3 does not excel at any single subject. Instead, we find that performance is lopsided, with GPT-3 having almost 70% accuracy for its best subject but near-random performance for several other subjects." |
| Q13 | 2 | output_ontology | "Our results indicate that while recent advances have been impressive, state-of-the-art models still struggle at learning and applying knowledge from pretraining. The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality." |
| Q14 | 2 | output_form | "Worryingly, we also find that GPT-3 does not have an accurate sense of what it does or does not know since its average confidence can be up to 24% off from its actual accuracy." |
| Q15 | 2 | input_ontology | "We comprehensively evaluate the breadth and depth of a model's text understanding by covering numerous topics that humans are incentivized to learn." |
| Q16 | 3 | input_ontology | "We create a massive multitask test consisting of multiple-choice questions from various branches of knowledge. The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn. There are 57 tasks in total, which is also the number of Atari games (Bellemare et al., 2013), all of which are listed in Appendix B." |
| Q17 | 3 | input_content | "The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online. These include practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination. It also includes questions designed for undergraduate courses and questions designed for readers of Oxford University Press books." |
| Q18 | 3 | input_ontology | "Some tasks cover a subject, like psychology, but at a specific level of difficulty, such as "Elementary," "High School," "College," or "Professional." For example, the "Professional Psychology" task draws on questions from freely available practice questions for the Examination for Professional Practice in Psychology, while the "High School Psychology" task has questions like those from Advanced Placement Psychology examinations." |
| Q19 | 3 | input_form | "We collected 15908 questions in total, which we split into a few-shot development set, a validation set, and a test set. The few-shot development set has 5 questions per subject, the validation set may be used for selecting hyperparameters and is made of 1540 questions, and the test set has 14079 questions." |
| Q20 | 3 | input_form | "Each subject contains 100 test examples at the minimum, which is longer than most exams designed to assess people." |
| Q21 | 3 | output_form | "Human-level accuracy on this test varies. Unspecialized humans from Amazon Mechanical Turk obtain 34.5% accuracy on this test. Meanwhile, expert-level performance can be far higher. For example, real-world test-taker human accuracy at the 95th percentile is around 87% for US Medical Licensing Examinations, and these questions make up our "Professional Medicine" task. If we take the 95th percentile human test-taker accuracy for exams that build up our test, and if we make an educated guess when such information is unavailable, we then estimate that expert-level accuracy is approximately 89.8%." |
| Q22 | 3 | output_ontology | "Since our test aggregates different subjects and several levels of difficulty, we measure more than straightforward commonsense or narrow linguistic understanding. Instead, we measure arbitrary" |
| Q23 | 3 | output_ontology | "Consequently, we instead create a simple-to-evaluate test that measures classification accuracy on multiple choice questions." |
| Q24 | 4 | input_ontology | "The humanities is a group of disciplines that make use of qualitative analysis and analytic methods rather than scientific empirical methods. Branches of the humanities include law, philosophy, history, and so on (Appendix B)." |
| Q25 | 4 | input_ontology | "Mastering these subjects requires a variety of skills. For example, legal understanding requires knowledge of how to apply rules and standards to complex scenarios, and also provide answers with stipulations and explanations." |
| Q26 | 4 | input_content | "For philosophy, our questions cover concepts like logical fallacies, formal logic, and famous philosophical arguments. It also covers moral scenarios, including questions from the ETHICS dataset (Hendrycks et al., 2020) that test a model's understanding of normative statements through predicting widespread moral intuitions about diverse everyday scenarios." |
| Q27 | 4 | input_ontology | "Finally, our history questions cover a wide range of time periods and geographical locations, including prehistory and other advanced subjects." |
| Q28 | 4 | input_ontology | "Social science includes branches of knowledge that examine human behavior and society. Subject areas include economics, sociology, politics, geography, psychology, and so on." |
| Q29 | 4 | input_ontology | "Our economics questions include microeconomics, macroeconomics, and econometrics, and cover different types of problems, including questions that require a mixture of world knowledge, qualitative reasoning, or quantitative reasoning." |
| Q30 | 4 | input_ontology | "We also include important but more esoteric topics such as security studies in order to test the boundaries of what is experienced and learned during pretraining." |
| Q31 | 4 | input_ontology | "Social science also includes psychology, a field that may be especially important for attaining a nuanced understanding of humans." |
| Q32 | 4 | input_ontology | "STEM subjects include physics, computer science, mathematics, and more." |
| Q33 | 4 | input_ontology | "Conceptual physics tests understanding of simple physics principles and may be thought" |
| Q34 | 5 | output_form | "To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks." |
| Q35 | 5 | output_form | "We evaluate GPT-3 (Brown et al., 2020) and UnifiedQA (Khashabi et al., 2020)." |
| Q36 | 5 | output_form | "For GPT-3 we use the OpenAI API, which provides access to four model variants, "Ada," "Babbage," "Curie," and "Davinci," which we refer to as "Small" (2.7 billion parameters), "Medium" (6.7 billion), "Large" (13 billion) and "X-Large" (175 billion)." |
| Q37 | 5 | output_form | "UnifiedQA uses the T5 (Raffel et al., 2019) text-to-text backbone and is fine-tuned on previously proposed question answering datasets (Lai et al., 2017), where the prediction is the class with the highest token overlap with UnifiedQA's text output." |
| Q38 | 5 | output_form | "Since UnifiedQA is fine-tuned on other datasets, we evaluate it without any further tuning to assess its transfer accuracy." |
| Q39 | 5 | output_form | "We also fine-tune RoBERTa-base, ALBERT-xxlarge, and GPT-2 on UnifiedQA training data and our dev+val set." |
| Q40 | 5 | output_form | "We primarily focus on UnifiedQA and GPT-3 in the rest of this document, but additional discussion of RoBERTa, ALBERT, and GPT-2 is in Appendix A." |
| Q41 | 5 | output_form | "All values are percentages." |
| Q42 | 5 | output_form | "Some models proposed in the past few months can move several percent points beyond random chance." |
| Q43 | 5 | output_form | "GPT-3 uses few-shot learning and UnifiedQA is tested under distribution shift." |
| Q44 | 6 | input_form | "We feed GPT-3 prompts like that shown in Figure 1a. We begin each prompt with "The following are multiple choice questions (with answers) about [subject]." For zero-shot evaluation, we append the question to the prompt. For few-shot evaluation, we add up to 5 demonstration examples with answers to the prompt before appending the question. All prompts end with "Answer: ". The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction. For consistent evaluation, we create a dev set with 5 fixed few-shot examples for each subject." |
| Q45 | 6 | output_form | "We compare the few-shot accuracy of each GPT-3 size in Table 1. We find that the three smaller GPT-3 models have near random accuracy (around 25%). In contrast, we find that the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%." |
| Q46 | 6 | output_form | "While the smaller models have around 25% zero-shot accuracy, Figure 10 in Appendix A shows that the largest GPT-3 model has a much higher zero-shot accuracy of about 37.7%." |
| Q47 | 6 | output_form | "The largest UnifiedQA model we test has 11 billion parameters, which is slightly smaller than GPT-3 Large. Nevertheless, we show in Table 1 that it attains 48.9% accuracy. This performs better than the few-shot GPT-3 X-Large model, despite UnifiedQA have an order of magnitude fewer parameters." |
| Q48 | 6 | output_form | "We also find that even the smallest UnifiedQA variant, with just 60 million parameters, has approximately 29.3% accuracy. These results suggest that while model size is a key component for achieving strong performance, fine-tuning also helps." |
| Q49 | 6 | input_ontology | "Figure 6 shows the accuracy of GPT-3 (few-shot) and UnifiedQA for all 57 tasks. It shows the both models are below expert-level performance for all tasks, with GPT-3's accuracy ranging from 69% for US Foreign Policy to 26% for College Chemistry. UnifiedQA does best on marketing, with an accuracy of 82.5%." |
| Q50 | 6 | output_ontology | "Overall, models do poorly on highly procedural problems. Figure 6 shows that calculation-heavy STEM subjects tend to have low accuracy compared to verbal subjects. The lowest-accuracy tasks are STEM subjects that emphasize mathematics or calculations. We speculate that is in part because GPT-3 acquires declarative knowledge more readily than procedural knowledge." |
| Q51 | 7 | input_content | "For example, many questions in Elementary Mathematics require applying the order of operations for arithmetic, which is described by the acronym PEMDAS (Parentheses Exponents Multiplication Division Addition Subtraction)." |
| Q52 | 7 | output_ontology | "GPT-3 is aware of the acronym PEMDAS. However, it does not consistently apply PEMDAS to actual problems." |
| Q53 | 7 | output_ontology | "GPT-3 learns about topics in a pedagogically unusual order. GPT-3 does better on College Medicine (47.4%) and College Mathematics (35.0%) than calculation-heavy Elementary Mathematics (29.9%)." |
| Q54 | 7 | output_ontology | "GPT-3 demonstrates unusual breadth, but it does not master a single subject. Meanwhile we suspect humans have mastery in several subjects but not as much breadth. In this way, our test shows that GPT-3 has many knowledge blindspots and has capabilities that are lopsided." |
| Q55 | 7 | output_form | "We should not trust a model's prediction unless the model is calibrated, meaning that its confidence is a good estimate of the actual probability the prediction is correct." |
| Q56 | 7 | output_form | "We evaluate the calibration of GPT-3 by testing how well its average confidence estimates its actual accuracy for each subject." |
| Q57 | 7 | output_form | "GPT-3 is uncalibrated. In fact, its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects." |
| Q58 | 7 | output_form | "Another calibration measure is the Root Mean Squared (RMS) calibration error (Hendrycks et al., 2019a; Kumar et al., 2019). Many tasks have miscalibrated predictions, such as Elementary Mathematics which has a zero-shot RMS calibration error of 19.4%." |
| Q59 | 7 | input_form | "While text is capable of conveying an enormous number of concepts about the world, many important concepts are conveyed mainly through other modalities, such as images, audio, and physical interaction (Bisk et al., 2020). Existing large-scale NLP models, such as GPT-3, do not incorporate multimodal information, so we design our benchmark to capture a diverse array of tasks in a text-only format." |
| Q60 | 7 | input_content | "A major distinction between our benchmark and previous multitask NLP benchmarks is that we do not require large training sets. Instead, we assume that models have acquired the requisite knowledge from reading vast quantities of diverse text from the Internet. For this reason we assess pretrained models in a zero-shot, few-shot, or transfer setting and we provide a dev, val, and test set for each task." |
| Q61 | 8 | output_form | "The dev set is used for few-shot prompts, the val set could be used for hyperparameter tuning, and the test set is used to compute the final accuracy." |
| Q62 | 8 | output_form | "Importantly, the format of our evaluation is not identical to the format in which information is acquired during pretraining." |
| Q63 | 8 | output_content | "This has the benefit of obviating concerns about spurious training set annotation artifacts (Geirhos et al., 2020; Hendrycks et al., 2019b) and is in stark contrast to the previous paradigm of identically distributed training and test sets." |
| Q64 | 8 | output_ontology | "We find that current large-scale Transformers have wide room for improvement." |
| Q65 | 8 | output_ontology | "They are notably poor at modeling human (dis)approval, as evident by the low performance on the Professional Law and Moral Scenarios tasks." |
| Q66 | 8 | output_ontology | "Models also have difficulty performing calculations, so much so that they exhibit poor performance on Elementary Mathematics and many other STEM subjects with "plug and chug" problems." |
| Q67 | 8 | output_form | "Additionally, they do not match expert-level performance (90%) on any subject, so for all subjects it is subhuman." |
| Q68 | 8 | output_form | "On average, models are only now starting to move beyond random-chance accuracy levels." |
| Q69 | 8 | input_content | "We collected approximately 2,000 additional Professional Law training examples." |
| Q70 | 8 | output_form | "After fine-tuning a RoBERTa-base model (Liu et al., 2019) using this custom training set, our model attained 32.8% test accuracy." |
| Q71 | 8 | input_content | "We also had RoBERTa continue pretraining on approximately 1.6 million legal case summaries using Harvard's Law Library case law corpus case.law, but after fine-tuning it only attained 36.1% accuracy." |
| Q72 | 8 | output_form | "This suggests that while additional pretraining on relevant high quality text can help, it may not be enough to substantially increase the performance of current models." |
| Q73 | 8 | output_form | "It is unclear whether simply scaling up existing language models will solve the test." |
| Q74 | 8 | output_form | "Current understanding indicates that a 10× increase in model size must be accompanied by an approximate 5× increase in data (Kaplan et al., 2020)." |
| Q75 | 8 | input_ontology | "We introduced a new test that measures how well text models can learn and apply knowledge encountered during pretraining." |
| Q76 | 8 | input_ontology | "By covering 57 subjects at varying levels of difficulty, the test assesses language understanding in greater breadth and depth than previous benchmarks." |
| Q77 | 9 | output_content | "We would like to thank the following for their helpful comments: Oyvind Tafjord, Jan Leike, David Krueger, Alex Tamkin, Girish Sastry, and Henry Zhu." |
| Q78 | 9 | output_content | "DH is supported by the NSF GRFP Fellowship and an Open Philanthropy Project Fellowship." |
| Q79 | 9 | output_content | "This research was also supported by the NSF Frontier Award 1804794." |
| Q80 | 11 | input_ontology | "This appendix includes figures with sorted results (Figure 9), few-shot examples vs. accuracy (Figure 10), and few-shot calibration (Figure 11). It also includes sections on fine-tuning, error analysis, and format sensitivity." |
| Q81 | 11 | output_form | "We primarily analyzed models with more than 10 billion parameters in the main body of the paper. For this section, we analyze smaller models including RoBERTa-base (125 million parameters) (Liu" |
| Q82 | 11 | output_form | "On the left are GPT-3 few shot accuracies for all of the 57 tasks. On the right are UnifiedQA transfer accuracies for all of the 57 tasks. For both models, capabilities are lopsided." |
| Q83 | 12 | output_ontology | "Models are fine-tuned to predict one of four classes using the UnifiedQA MCQ questions and using our dev+val set. We test on our multitask test set." |
| Q84 | 12 | output_form | "RoBERTa-base attains an overall accuracy of 27.9%, with 27.9% accuracy for the humanities, 28.8% for social sciences, 27.0% for STEM, and 27.7% for other." |
| Q85 | 12 | output_form | "ALBERT-xxlarge attains an accuracy of 27.1%, with 27.2% accuracy for the humanities, 25.7% for the social sciences, 27.7% for STEM, and 27.9% for other." |
| Q86 | 12 | output_form | "GPT-2 attains an accuracy of 32.4%, with 32.8% accuracy for the humanities, 33.3% for the social sciences, 30.2% for STEM, and 33.1% for other." |
| Q87 | 12 | output_form | "UnifiedQA's smallest variant, which has just 60 million parameters and approximately 29.3% accuracy. It obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters. This suggests that its larger pretraining dataset enables higher accuracy." |
| Q88 | 12 | output_form | "UnifiedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy. This again suggests that T5's larger pretraining dataset size (and therefore UnifiedQA's pretraining dataset size) can increase accuracy." |
| Q89 | 12 | output_content | "We qualitatively analyze when GPT-3 makes high confidence mistakes. We find that while many of these mistakes were clearly wrong, many were mistakes that a human might make." |
| Q90 | 12 | input_form | "While different question formatting choices often lead to similar GPT-3 accuracies, we find that UnifiedQA is more sensitive." |
| Q91 | 12 | input_form | "UnifiedQA's input format is of the form QUESTION1 \n (A) CHOICE1 (B) CHOICE2 (C) CHOICE3 (D) CHOICE4</s> where questions and choices are normalized and made lowercase." |
| Q92 | 12 | input_form | "If we remove the </s> from the input, accuracy declines by several percentage points." |
| Q93 | 13 | input_ontology | "We provide analysis of question length and difficulty in Figure 12. We list all tasks and the topics they test in Table 2. We also provide an example for each task starting with Figure 14." |
| Q94 | 13 | input_form | "For questions longer than a tweet (280 characters), the correlation between question length and true label confidence is slightly positive. This shows that longer questions are not necessarily harder." |
| Q95 | 13 | output_content | "Since language models train on vast text corpora, there is some chance that they have seen the exact question and answer during pretraining. If they memorized the exact question and answer, then they would attain higher accuracy than their true ability. Likewise, a question's entropy would be especially low if it were memorized. Memorized questions and answers should have low entropy and" |
| Q96 | 13 | output_form | "While models are more calibrated in a few-shot setting than a zero-shot setting, they are still miscalibrated, with gap between accuracy and confidence reaching up to 14%. Here the correlation between confidence and accuracy is r = 0.81, compared to r = 0.63 in the zero-shot setting." |
| Q97 | 13 | output_form | "As the number of few-shot instruction examples increases, the accuracy monotonically increases. Notably, zero-shot performance is only somewhat lower than 5-shot accuracy." |
| Q98 | 14 | output_content | "However, in Figure 13, we see that accuracy and question entropy are not positively correlated, suggesting that the test's low-entropy questions do not correspond to memorized (and thereby correctly predicted) answers." |
| Q99 | 14 | output_content | "This suggests that our exact questions were not memorized." |
| Q100 | 14 | output_content | "However, during pretraining models encountered text related to our questions through processing Wikipedia." |
| Q101 | 14 | input_content | "We also note that most of our questions came from PDFs or websites where questions and answers are on separate pages." |
| Q102 | 14 | output_content | "To reduce the probability that future models encounter exact questions during test-time, we will provide a list of question sources." |
| Q103 | 14 | output_form | "In the zero-shot question prompt, the correlation between average log probability and accuracy is r = −0.43, and for the few-shot setting the correlation is r = −0.56." |
| Q104 | 15 | input_ontology | "Table 2: Summary of all 57 tasks." |
| Q105 | 16 | input_content | "Find all c in Z₃ such that Z₃[x]/(x² + c) is a field." |
| Q106 | 16 | input_content | "What is the embryological origin of the hyoid bone?" |
| Q107 | 16 | input_content | "Why isn't there a planet where the asteroid belt is located?" |
| Q108 | 16 | input_content | "Three contrasting tactics that CSO's can engage in to meet their aims are which typically involves research and communication, , which may involve physically attacking a company's operations or , often involving some form of ." |
| Q109 | 16 | input_content | "How many attempts should you make to cannulate a patient before passing the job on to a senior colleague?" |
| Q110 | 16 | input_content | "In a given population, 1 out of every 400 people has a cancer caused by a completely recessive allele, b. Assuming the population is in Hardy-Weinberg equilibrium, which of the following is the expected proportion of individuals who carry the b allele but are not expected to develop the cancer?" |
| Q111 | 16 | input_content | "Which of the following statements about the lanthanide elements is NOT true?" |
| Q112 | 17 | input_content | "Consider a computer design in which multiple processors, each with a private cache memory, share global memory using a single bus." |
| Q113 | 17 | input_content | "Let A be a real 2 × 2 matrix. Which of the following statements must be true?" |
| Q114 | 17 | input_content | "In a genetic test of a newborn, a rare genetic disorder is found that has X-linked recessive transmission." |
| Q115 | 17 | input_content | "One end of a Nichrome wire of length 2L and cross-sectional area A is attached to an end of another Nichrome wire of length L and cross- sectional area 2A." |
| Q116 | 17 | input_content | "Why is it that anti-virus scanners would not have found an exploitation of Heartbleed?" |
| Q117 | 17 | input_content | "A model airplane flies slower when flying into the wind and faster with wind at its back." |
| Q118 | 18 | input_content | "Consider the following AR(1) model with the disturbances having zero mean and unit variance yt = 0.2 + 0.4yt−1 + ut The (unconditional) mean of y will be given by (A) 0.2 (B) 0.4 (C) 0.5 (D) 0.33" |
| Q119 | 18 | input_content | "A point pole has a strength of 4π × 10−4 weber. The force in newtons on a point pole of 4π × 1.5 × 10−4 weber placed at a distance of 10 cm from it will be (A) 15 N. (B) 20 N. (C) 7.5 N. (D) 3.75 N." |
| Q120 | 18 | input_content | "A total of 30 players will play basketball at a park. There will be exactly 5 players on each team. Which statement correctly explains how to find the number of teams needed? (A) Add 5 to 30 to find 35 teams. (B) Divide 30 by 5 to find 6 teams. (C) Multiply 30 and 5 to find 150 teams. (D) Subtract 5 from 30 to find 25 teams." |
| Q121 | 18 | input_content | "Determine whether the statements are logically equivalent or contradictory. If neither, determine whether they are consistent or inconsistent. E ⊃ (F · E) and ∼ E · F (A) Logically equivalent (B) Contradictory (C) Neither logically equivalent nor contradictory, but consistent (D) Inconsistent" |
| Q122 | 18 | input_content | "As of 2017, how many of the world's 1-year-old children today have been vaccinated against some disease? (A) 80% (B) 60% (C) 40% (D) 20%" |
| Q123 | 18 | input_content | "Homologous structures are often cited as evidence for the process of natural selection. All of the following are examples of homologous structures EXCEPT (A) the wings of a bird and the wings of a bat (B) the flippers of a whale and the arms of a man (C) the pectoral fins of a porpoise and the flippers of a seal (D) the forelegs of an insect and the forelimbs of a dog" |
| Q124 | 18 | input_content | "From the solubility rules, which of the following is true? (A) All chlorides, bromides, and iodides are soluble (B) All sulfates are soluble (C) All hydroxides are soluble (D) All ammonium-containing compounds are soluble" |
| Q125 | 19 | input_content | "A list of numbers has n elements, indexed from 1 to n. The following algorithm is intended to display the number of elements in the list that have a value greater than 100. The algorithm uses the variables count and position. Steps 3 and 4 are missing." |
| Q126 | 19 | input_content | "Which of the following could be used to replace steps 3 and 4 so that the algorithm works as intended?" |
| Q127 | 19 | input_content | "Figure 34: A High School Computer Science example." |
| Q128 | 19 | input_content | "This question refers to the following information." |
| Q129 | 19 | input_content | "From the passage, one may infer that the English Parliament wished to argue that the Act of Supremacy would" |
| Q130 | 19 | input_content | "Figure 35: A High School European History example." |
| Q131 | 19 | input_content | "During the third stage of the demographic transition model, which of the following is true?" |
| Q132 | 19 | input_content | "Figure 36: A High School Geography example." |
| Q133 | 20 | input_content | "Figure 37: A High School Government and Politics example." |
| Q134 | 20 | input_content | "Figure 38: A High School Macroeconomics example." |
| Q135 | 20 | input_content | "Figure 39: A High School Mathematics example." |
| Q136 | 20 | input_content | "Figure 40: A High School Microeconomics example." |
| Q137 | 20 | input_content | "Figure 41: A High School Physics example." |
| Q138 | 20 | input_content | "Figure 42: A High School Psychology example." |
| Q139 | 21 | input_content | "Figure 43: A High School Statistics example." |
| Q140 | 21 | input_content | "Figure 44: A High School US History example." |
| Q141 | 21 | input_content | "Figure 45: A High School World History example." |
| Q142 | 21 | input_content | "Figure 46: A Human Aging example." |
| Q143 | 22 | input_content | "Morning sickness is typically a problem: (A) during the first trimester (B) during the second trimester (C) during the third trimester (D) all through the pregnancy" |
| Q144 | 22 | input_content | "Would a reservation to the definition of torture in the ICCPR be acceptable in contemporary practice? (A) This is an acceptable reservation if the reserving country's legislation employs a different definition (B) This is an unacceptable reservation because it contravenes the object and purpose of the ICCPR (C) This is an unacceptable reservation because the definition of torture in the ICCPR is consistent with customary international law (D) This is an acceptable reservation because under general international law States have the right to enter reservations to treaties" |
| Q145 | 22 | input_content | "Which position does Rawls claim is the least likely to be adopted by the POP (people in the original position)? (A) The POP would choose equality above liberty. (B) The POP would opt for the 'maximin' strategy. (C) The POP would opt for the 'difference principle.' (D) The POP would reject the 'system of natural liberty.'" |
| Q146 | 22 | input_content | "John Stuart Mill: Each person's happiness is a good to that person, and the general happiness, therefore, a good to the aggregate of all persons. (A) Fallacy of Composition (B) Fallacy of Division (C) Gambler's Fallacy (D) Equivocation" |
| Q147 | 22 | input_content | "A 6-sided die is rolled 15 times and the results are: side 1 comes up 0 times; side 2: 1 time; side 3: 2 times; side 4: 3 times; side 5: 4 times; side 6: 5 times. Based on these results, what is the probability of side 3 coming up when using Add-1 Smoothing? (A) 2/15 (B) 1/7 (C) 3/16 (D) 1/5" |
| Q148 | 22 | input_content | "According to Lewin, Lippet and White's 1939 experiment, which form of leadership produced the most work from participants? (A) Laissez-faire (B) Democratic (C) Authoritarian (D) A mix of laissez-faire and democratic" |
| Q149 | 23 | input_form | "The formatting of this task hinders UnifiedQA performance substantially." |
| Q150 | 24 | input_content | "According to Moore's "ideal utilitarianism," the right action is the one that brings about the greatest amount of: (A) pleasure. (B) happiness. (C) good. (D) virtue." |
| Q151 | 24 | input_content | "Researchers now believe that the decline of the Maya was caused chiefly by: (A) a cataclysm of some kind, such as an earthquake, volcano, or tsunami. (B) ecological degradation resulting from slash-and-burn farming techniques. (C) endless wars between neighboring Mayan city-states. (D) practices of interbreeding that led to a steep rise in congenital disorders." |
| Q152 | 24 | input_content | "Krete is an unmarried taxpayer with income exclusively from wages. By December 31, year 1, Krete's employer has withheld $16,000 in federal income taxes and Krete has made no estimated tax payments. On April 15, year 2, Krete timely filed for an extension request to file her individual tax return, and paid $300 of additional taxes. Krete's year 1 tax liability was $16,500 when she timely filed her return on April 30, year 2, and paid the remaining tax liability balance. What amount would be subject to the penalty for underpayment of estimated taxes? (A) $0 (B) $500 (C) $1,650 (D) $16,500" |
| Q153 | 24 | input_content | "The night before his bar examination, the examinee's next-door neighbor was having a party. The music from the neighbor's home was so loud that the examinee couldn't fall asleep. The examinee called the neighbor and asked her to please keep the noise down. The neighbor then abruptly hung up. Angered, the examinee went into his closet and got a gun. He went outside and fired a bullet through the neighbor's living room window. Not intending to shoot anyone, the examinee fired his gun at such an angle that the bullet would hit the ceiling. He merely wanted to cause some damage to the neighbor's home to relieve his angry rage. The bullet, however, ricocheted off the ceiling and struck a partygoer in the back, killing him. The jurisdiction makes it a misdemeanor to discharge a firearm in public. The examinee will most likely be found guilty for which of the following crimes in connection to the death of the partygoer? (A) Murder. (B) Involuntary manslaughter. (C) Voluntary manslaughter. (D) Discharge of a firearm in public." |
| Q154 | 25 | input_content | "A 63-year-old man is brought to the emergency department because of a 4-day history of increasingly severe left leg pain and swelling of his left calf. He also has a 1-month history of increasingly severe upper midthoracic back pain. During this time, he has had a 9-kg (20-lb) weight loss despite no change in appetite. He has no history of major medical illness. His only medications is ibuprofen. He is 180 cm (5 ft 11 in) tall and weighs 82 kg (180 lb); BMI is 25 kg/m2. His vital signs are within normal limits. On examination, lower extremity pulses are palpable bilaterally. The remainder of the physical examination shows no abnormalities. An x-ray of the thoracic spine shows no abnormalities. A CT scan of the abdomen shows a 3-cm mass in the body of the pancreas; there are liver metastases and encasement of the superior mesenteric artery. Ultrasonography of the left lower extremity shows a femoropopliteal venous clot. Which of the following is the most likely cause of this patient's symptoms?" |
| Q155 | 25 | input_content | "The technique that is most likely to produce an immediate improvement in the behavior of a child who hits others and rips up schoolbooks is" |
| Q156 | 25 | input_content | "You work for a utility company that is building a biomass plant in the community. Your employer asks you to give a series of community talks about the plant and future operations. You visit the plant several hours before you are due to give a speech that has been prepared by your immediate supervisor. During the tour of the plant, you discover several claims in the speech are not true. What do you do?" |
| Q157 | 26 | input_content | "Which of the following statements most closely corresponds with differential association theory?" |
| Q158 | 26 | input_content | "Why did Congress oppose Wilson's proposal for the League of Nations?" |
| Q159 | 26 | input_content | "An observational study in diabetics assesses the role of an increased plasma fibrinogen level on the risk of cardiac events. 130 diabetic patients are followed for 5 years to assess the development of acute coronary syndrome. In the group of 60 patients with a normal baseline plasma fibrinogen level, 20 develop acute coronary syndrome and 40 do not. In the group of 70 patients with a high baseline plasma fibrinogen level, 40 develop acute coronary syndrome and 30 do not. Which of the following is the best estimate of relative risk in patients with a high baseline plasma fibrinogen level compared to patients with a normal baseline plasma fibrinogen level?" |
| Q160 | 27 | input_content | "Figure 70: A World Religions example." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/abs/2410.14815 |
| WEB-2 | https://en.wikipedia.org/wiki/Literacy_in_India |
| WEB-3 | https://dhsprogram.com/pubs/pdf/FR375/FR375.pdf |
| WEB-4 | https://indiadatamap.com/2025/08/26/indias-literacy-rate-insights-for-2025/ |
| WEB-5 | https://upsc.gov.in/examinations/active-examination |
| WEB-6 | https://ssc.gov.in/ |
| WEB-7 | https://sleepyclasses.com/discover-how-many-candidates-are-selected-in-upsc-each-year/ |
| WEB-8 | https://www.legacyias.com/upsc-success-rate-2024-best-age-attempt-optional-subject-to-crack-ias/ |
| WEB-9 | https://theprint.in/india/family-support-safety-study-material-a-click-away-whats-driving-more-women-to-take-upsc-exam/1922660/ |
| WEB-10 | https://www.iamai.in/sites/default/files/research/Kantar_%20IAMAI%20report_2024_.pdf |
| WEB-11 | https://en.wikipedia.org/wiki/Internet_in_India |
| WEB-12 | https://www.business-standard.com/industry/news/india-to-exceed-900mn-internet-users-by-2025-125011600669_1.html |
| WEB-13 | https://aclanthology.org/2025.naacl-long.507/ |
| WEB-14 | https://huggingface.co/datasets/ai4bharat/MILU |
| WEB-15 | https://arxiv.org/abs/2508.16185 |
| WEB-16 | https://arxiv.org/abs/2602.16467 |
| WEB-17 | https://llm-stats.com/benchmarks/mmmlu |
| WEB-18 | https://arxiv.org/abs/2501.15747 |
| WEB-19 | https://arxiv.org/abs/2503.10497 |
| WEB-20 | https://arxiv.org/abs/2509.11570 |
| WEB-21 | https://arxiv.org/abs/2508.19831 |
| WEB-22 | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf |
| WEB-23 | https://www.india-briefing.com/news/dpdp-rules-2025-india-data-protection-law-compliance-40769.html/ |
| WEB-24 | https://www.ey.com/en_in/insights/cybersecurity/decoding-the-digital-personal-data-protection-act-2023 |
| WEB-25 | https://iapp.org/news/a/notes-from-the-asia-pacific-region-india-releases-dpdpa-rules-ai-governance-guidelines |
| WEB-26 | https://truyo.com/governing-the-ai-surge-how-india-is-writing-the-rulebook-for-responsible-ai/ |
| WEB-27 | https://blog.lukmaanias.com/2026/04/28/the-digital-personal-data-protection-dpdp-rules-2025/ |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** cais/mmlu
**Analysis date:** 2025-01-30
**Examples reviewed:** ~200 examples across 57 subject configs (5–6 examples per config)
**Columns shown:** question, subject, choices, answer
**Columns skipped (media):** none (text-only dataset)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | high_school_government_and_politics | Ex.1 | A | "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" | US constitutional law question — irrelevant to Indian Polity | IO, IC |
| D2 | high_school_government_and_politics | Ex.4 | D | "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" | US Congress-specific legislation — not Indian constitutional content | IO, IC |
| D3 | high_school_government_and_politics | Ex.5 | A | "What power was granted to the states by the Articles of Confederation but not by the Constitution?" | US Articles of Confederation — no Indian Polity equivalent | IO, IC |
| D4 | high_school_us_history | Ex.2 | B | "John C. Calhoun, 'South Carolina Exposition and Protest,' 1828 … The language of 'protest' that Calhoun used … was similar to the language of which of the following political positions?" | US history question with primary source passage — entirely irrelevant to Indian History | IO, IC |
| D5 | high_school_us_history | Ex.4 | D | "Between 1820 and 1854, the greatest number of immigrants to the United States came from … Ireland" | US immigration history — no relevance to Indian competitive exams | IO, IC |
| D6 | high_school_us_history | Ex.5 | A | "Tonight, the daughter of an immigrant from Italy has been chosen to run for (vice) president … — Geraldine Ferraro, Vice Presidential Nomination Acceptance Address, July 19, 1984" | US political history primary source — alien to UPSC/SSC syllabus | IO, IC |
| D7 | us_foreign_policy | Ex.2 | B | "Why might the 'Philadelphian System' be linked to the idea of American exceptionalism?" | US foreign policy / exceptionalism — irrelevant to Indian deployment | IO, IC |
| D8 | us_foreign_policy | Ex.3 | C | "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" | US Cold War policy — no analogue in UPSC/SSC syllabus | IO, IC |
| D9 | us_foreign_policy | Ex.4 | D | "In American government, the power to declare war rests with … Congress" | US government structure question — not Indian Polity | IO, IC |
| D10 | professional_law | Ex.1 | A | "A truck driver was assigned to drive a huge tractor-trailer loaded with logs … the girl's parents … assert a claim against the lumber company" | US tort law scenario — calibrated against US bar exam, not Indian law | IO, IC |
| D11 | professional_law | Ex.2 | B | "An avid baseball fan … forwarded the club a $50 registration deposit … In a restitutionary action, can the executor of the fan's estate … recover … the $2,500 paid to the club?" | US contract law with baseball cultural context — no Indian law equivalent | IO, IC |
| D12 | high_school_european_history | Ex.1 | A | "The Scribbling-Machines have thrown thousands of your petitioners out of employ … Leeds Woolen Workers Petition, 1786" | British Industrial Revolution primary source — European history with no South Asian content | IO, IC |
| D13 | high_school_european_history | Ex.2 | B | "What is tolerance? … Of all religions, the Christian ought doubtless to inspire the most tolerance … Voltaire, Letters on the English Nation, 1733" | Enlightenment Western philosophy — Western canon, irrelevant to Indian History syllabus | IO, IC |
| D14 | high_school_european_history | Ex.4 | D | "The substitution of Plato for the scholastic Aristotle … Cosimo and Lorenzo de Medici … the Florentine Academy … Neoplatonism" | Italian Renaissance intellectual history — no Indian History coverage | IO, IC |
| D15 | high_school_world_history | Ex.2 | B | "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters … William Howard Russell, My Indian Mutiny Diary, 1860" | 1857 Indian Mutiny from British colonial perspective — if Indian History content appears, it is filtered through colonial framing | IO, IC, OC |
| D16 | philosophy | Ex.1 | A | "According to Parfit, the obligation to give priority to the welfare of one's children is: agent-relative." | Western analytic philosophy (Parfit) — not covered in UPSC/SSC philosophy or ethics sections | IO, IC |
| D17 | philosophy | Ex.2 | B | "Anscombe claims that on Sidgwick's view, the badness of an action must be estimated in light of: its expected consequences." | Western analytic moral philosophy (Sidgwick, Anscombe) — entirely Western canonical tradition | IO, IC |
| D18 | moral_scenarios | Ex.1 | A | "according to ordinary moral standards in the US as of 2020? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot." | Explicitly US-framed moral norms — normative grounding is US-specific | OC, IC |
| D19 | moral_scenarios | Ex.2 | B | "according to ordinary moral standards in the US as of 2020? Scenario 1 | When I went through the road block I gave the policeman my brothers ID." | Again explicitly references US 2020 moral standards — non-transferable to Indian cultural context | OC, IC |
| D20 | human_aging | Ex.3 | C | "The age at which one can receive full benefits from social security … Has been increasing" | US Social Security system — irrelevant to Indian context | IC |
| D21 | human_sexuality | Ex.1 | A | "Which of the following is the most common method of birth control for married couples in the U.S." | Explicitly US-specific demographic question | IC |
| D22 | high_school_geography | Ex.1 | A | "What is the most rapidly growing religion in the United States today? … Islam" | US religion demographics — not Indian Geography content | IO, IC |
| D23 | global_facts | Ex.2 | B | "As of 2017, what fraction of the population in India used the internet in the past three months? … 26%" | One of very few India-referencing questions — but tests dated Western-sourced statistical trivia, not Indian GK curriculum | IC |
| D24 | global_facts | Ex.4 | D | "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … in their country makes it a better place to live … 68%" | India-referencing global survey question — but sourced from Pew/Western pollsters, not Indian exam curriculum | IC |
| D25 | elementary_mathematics | Ex.1 | A | "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel? … 120 miles" | Uses miles (US customary unit) — Indian exams use km; creates construct-irrelevant variance | IC, IF |
| D26 | elementary_mathematics | Ex.5 | A | "A zoo has 15 toucans and 60 parrots. What is the ratio of the number of toucans to the number of parrots at the zoo? … 1:04" | Basic arithmetic ratio — language-neutral content applicable across curricula | IO |
| D27 | high_school_mathematics | Ex.1 | A | "Juan rolls a fair regular octahedral die … What is the probability that the product of the two rolls is a multiple of 3?" | Probability question — content universally applicable regardless of cultural context | IO |
| D28 | college_mathematics | Ex.2 | B | "A total of x feet of fencing is to form three sides of a level rectangular yard. What is the maximum possible area of the yard, in terms of x?" | Uses feet (US customary unit) — minor but consistent US measurement convention | IC |
| D29 | college_computer_science | Ex.2 | B | "Let G = (V, E) be a connected, undirected graph … P_1 can be solved in polynomial time but P_2 is not known to be solvable in polynomial time." | Algorithm complexity theory — culturally neutral STEM content | IO |
| D30 | abstract_algebra | Ex.1 | A | "Find the characteristic of the ring Z_3 x 3Z." | Abstract mathematics — entirely culture-independent | IO |
| D31 | high_school_statistics | Ex.4 | D | "The Hardcore Construction Company has two offices, one in Atlanta and one in New Orleans … Is the 2-sample t-test an appropriate inferential technique?" | Statistical reasoning with US city names as context — content sound but culturally anchored | IC |
| D32 | professional_accounting | Ex.1 | A | "Which of the following procedures does a CPA usually perform when reviewing the financial statements of a nonissuer?" | US CPA (Certified Public Accountant) professional standards — not relevant to Indian accounting exams | IO, IC |
| D33 | jurisprudence | Ex.1 | A | "Bill purchased a can of Sipep from the Ajax Minimart … In a strict product liability tort action against Ajax, Bill must prove …" | US-style product liability tort — uses American legal framework | IC |
| D34 | high_school_world_history | Ex.4 | D | "Kwame Nkrumah, Neo-Colonialism, 1965 … Which of the following most inspired the national plan advanced by Nkrumah in the second paragraph? … Socialism" | Global post-colonial history — partial relevance to Indian modern history via decolonisation themes | IO |
| D35 | world_religions | Ex.2 | B | "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" | Jainism question — one of very few South Asian religious/cultural references in the entire sample | IO, IC |
| D36 | world_religions | Ex.4 | D | "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" | Jainism sect distinction — rare South Asian content, but not an Indian competitive exam priority topic | IO, IC |
| D37 | high_school_psychology | Ex.1 | A | "Jyoti notes the behavior of people as they wait in line for tickets to rock concerts." | Uses Indian name 'Jyoti' but the context is rock concerts (Western cultural setting) — surface-level name inclusion without substantive cultural relevance | IC |
| D38 | auxiliary_train | Ex.1 | A | "Jim watched a liquor store furtively … On a charge of burglary, Jim's best defense would be that … the liquor store was open to the public." | US criminal law (burglary statute) — entirely US legal framework | IO, IC |
| D39 | high_school_macroeconomics | Ex.2 | B | "A nation that must consistently borrow to cover annual budget deficits risks … a decline in net exports as the nation's goods become more expensive to foreign consumers." | General macroeconomic principle — applicable cross-culturally | IO |
| D40 | conceptual_physics | Ex.4 | D | "A wave transfers … energy" | Basic physics principle — universally applicable | IO |
| D41 | high_school_biology | Ex.2 | B | "The sequence of amino acids in hemoglobin molecules of humans is more similar to the hemoglobin of chimpanzees than it is to the hemoglobin of dogs." | Biology/evolution — curriculum-neutral STEM content | IO |
| D42 | virology | Ex.1 | A | "Viruses have encouraged us to change our world, as we have now: Eradicated smallpox" | General science fact — applicable to Indian science GK | IO |
| D43 | international_law | Ex.1 | A | "Which of the following is a treaty-based human rights mechanism? … The UN Human Rights Committee" | International law — partially relevant to UPSC GS II but framed from Western international law perspective | IO |
| D44 | prehistory | Ex.2 | B | "The origins of Chinese civilization can be traced to: chiefdoms and states in numerous regions throughout China." | World history/prehistory — no South Asian prehistoric content visible | IO |
| D45 | miscellaneous | Ex.1 | A | "A flashing red traffic light signifies that a driver should do what? … stop" | US traffic law convention — minor but US-specific | IC |
| D46 | business_ethics | Ex.5 | A | "civil society … in many other countries, such as Russia and China … far less developed than in, for instance, Britain" | Western-centric framing of civil society — India not mentioned as reference | IC |
| D47 | high_school_world_history | Ex.2 | B | "the deed was done by a subject race — by black men who dared to shed the blood of their masters … British journalist William Howard Russell" | 1857 mutiny through British colonial journalist's lens — if Indian content appears at all in MMLU, it is through a colonial/Western perspective | OC, IC |
| D48 | college_medicine | Ex.4 | D | "When preparing for the MCAT exam, a student begins studying electrochemical cells." | References MCAT (US Medical College Admission Test) — US-specific academic context | IC |
| D49 | high_school_statistics | Ex.5 | A | "As reported on CNN, in a May 1999 national poll 43% of high school students expressed fear about going to school." | CNN/US-specific polling context — not Indian curriculum content | IC |
| D50 | security_studies | Ex.1 | A | "In what ways do theories of conventional and critical social constructivism differ?" | IR theory — Western academic framing; partial relevance to UPSC GS II international relations | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Four-option MCQ format structurally matches competitive exam format
- **Dimension(s):** IF
- **Observation:** Every question in MMLU uses a four-option multiple-choice structure (A/B/C/D) with one correct answer and three distractors, which is the identical format used in UPSC Prelims, SSC CGL, and banking exams. The `choices` field consistently contains exactly four options across all 57 subjects sampled.
- **Deployment relevance:** The MCQ format is a genuine structural match, meaning that any component of MMLU used in a format-compatibility test would not introduce format-induced performance variance from input encoding differences.
- **Datapoint citations:**
  - [D26] Example 5 (elementary_mathematics, split=test, label=A): "A zoo has 15 toucans and 60 parrots. What is the ratio of the number of toucans to the number of parrots at the zoo? (A) 1:04 (B) 1:05 (C) 4:01 (D) 4:05" — standard four-option MCQ format identical to Indian competitive exam structure.
  - [D40] Example 4 (conceptual_physics, split=test, label=D): "A wave transfers (A) amplitude (B) wavelength (C) frequency (D) energy" — clean four-option format applicable regardless of deployment context.

#### Strength 2: Culturally neutral STEM content (mathematics, physics, computer science) provides partial proxy signal
- **Dimension(s):** IO
- **Observation:** A substantial fraction of MMLU's items — particularly abstract algebra, college/high school mathematics, conceptual physics, college computer science, and formal logic — contain questions whose correctness is independent of cultural or geographic framing. These items test skills (arithmetic, reasoning, algorithm analysis, probability) that overlap with the quantitative aptitude and reasoning sections of SSC CGL and UPSC Prelims CSAT.
- **Deployment relevance:** For the deployment's Mathematics/Reasoning priority domain, these items constitute a weak but non-zero signal about model competence. UPSC CSAT Paper II and SSC CGL quantitative aptitude share conceptual overlap with MMLU's elementary and college mathematics items.
- **Datapoint citations:**
  - [D27] Example 1 (high_school_mathematics, split=test, label=A): "Juan rolls a fair regular octahedral die marked with the numbers 1 through 8. Then Amal rolls a fair six-sided die. What is the probability that the product of the two rolls is a multiple of 3?" — probability question applicable cross-culturally.
  - [D30] Example 1 (abstract_algebra, split=test, label=A): "Find the characteristic of the ring Z_3 x 3Z." — pure mathematics, culturally neutral.
  - [D29] Example 2 (college_computer_science, split=test, label=B): "P_1 can be solved in polynomial time but P_2 is not known to be solvable in polynomial time." — algorithm complexity, universally applicable.

#### Strength 3: Broad label balance across answer classes
- **Dimension(s):** OF
- **Observation:** Across sampled configs, the distribution of correct answers (A/B/C/D) is reasonably balanced. Buffer counts show roughly 22–31% per class in most subjects, with no systematic bias toward any single letter. This prevents position-bias artifacts from contaminating aggregate accuracy scores.
- **Deployment relevance:** For any comparative evaluation of models on the subset of MMLU items with partial relevance (STEM), balanced answer distribution reduces the risk that accuracy gains reflect position-bias rather than genuine knowledge.
- **Datapoint citations:**
  - [D26] elementary_mathematics buffer: A=79, B=97, C=101, D=101 (n=378) — reasonable balance across four classes.
  - [D27] high_school_mathematics buffer: A=57, B=71, C=71, D=71 (n=270) — no dominant label class.

#### Strength 4: Science and biology content overlaps with Indian GK science sections
- **Dimension(s):** IO
- **Observation:** MMLU's high school biology, college biology, virology, medical genetics, and conceptual physics items cover topics (genetics, evolution, cell biology, basic physics principles) that partially overlap with Indian Class 10–12 NCERT science content tested in UPSC/SSC GK sections. These are not India-specific but are curriculum-neutral science facts.
- **Deployment relevance:** UPSC Prelims General Studies Paper I and SSC CGL GK sections include NCERT-level science questions. MMLU's science content provides weak-but-positive signal in this subdomain.
- **Datapoint citations:**
  - [D41] Example 2 (high_school_biology, split=test, label=B): "The sequence of amino acids in hemoglobin molecules of humans is more similar to the hemoglobin of chimpanzees than it is to the hemoglobin of dogs. This similarity suggests that humans and chimpanzees are more closely related than humans and dogs" — evolution content appearing in NCERT Biology Class 12.
  - [D42] Example 1 (virology, split=test, label=A): "Viruses have encouraged us to change our world, as we have now: Eradicated smallpox" — general science fact tested in Indian GK sections.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Complete absence of Indian Polity, Indian History, and Indian Geography — the core UPSC/SSC subject domains
- **Dimension(s):** IO
- **Observation:** Across all 57 MMLU subject configs and the full sample of ~200 examples, not a single question addresses Indian constitutional law, Panchayati Raj, Indian administrative structures, Indian ancient/medieval/modern history, or Indian physical/political geography. The government and politics config covers exclusively US government. The history configs cover European and US history. No config maps to any of the five priority subject domains in the Indian competitive exam syllabus.
- **Deployment relevance:** Indian Polity and Constitution, Indian History, and Indian Geography are high-priority domains for UPSC Prelims GS Paper I and SSC GK. MMLU provides zero items for these domains. A model achieving high MMLU accuracy could score near-random on UPSC/SSC Indian Polity questions, and MMLU accuracy would provide no predictive information about this.
- **Datapoint citations:**
  - [D1] Example 1 (high_school_government_and_politics, split=test, label=A): "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" — US First Amendment, not Indian constitutional rights.
  - [D3] Example 5 (high_school_government_and_politics, split=test, label=A): "What power was granted to the states by the Articles of Confederation but not by the Constitution?" — US Articles of Confederation, no Indian Polity equivalent.
  - [D4] Example 2 (high_school_us_history, split=test, label=B): "John C. Calhoun, 'South Carolina Exposition and Protest,' 1828 … was similar to the language of which of the following political positions?" — US antebellum history, irrelevant to Indian History syllabus.
  - [D12] Example 1 (high_school_european_history, split=test, label=A): "The Scribbling-Machines have thrown thousands of your petitioners out of employ … Leeds Woolen Workers Petition, 1786" — British Industrial Revolution, no South Asian historical content.

#### Concern 2: All benchmark inputs are in English — zero Hindi or Devanagari content
- **Dimension(s):** IF
- **Observation:** Every single question, answer option, and subject label in the sampled data is in English. The HF metadata confirms `languages: [en]` and `multilinguality: monolingual`. There is no Devanagari script, no Hindi vocabulary, no code-mixed text, and no variant closer to the deployment's required input register (Hindi-dominant with ≤10% English).
- **Deployment relevance:** The deployment requires Hindi-medium interaction. A model's MMLU accuracy measured on English-medium questions provides no evidence whatsoever about its capacity to comprehend Hindi-dominant or Devanagari-script inputs. IndicEval (arXiv:2602.16467) demonstrates a catastrophic Hindi-medium performance penalty: LLaMA achieves only 39.53% on UPSC Hindi Zero-Shot vs. ~84.88% for Gemini on UPSC English CoT. MMLU scores cannot predict this gap.
- **Datapoint citations:**
  - [D10] Example 1 (professional_law, split=test, label=A): "A truck driver was assigned to drive a huge tractor-trailer loaded with logs…" — English-medium, no Hindi content.
  - [D25] Example 1 (elementary_mathematics, split=test, label=A): "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel?" — English-only phrasing, uses US customary units.
  - [D30] Example 1 (abstract_algebra, split=test, label=A): "Find the characteristic of the ring Z_3 x 3Z." — English-only mathematical notation.

#### Concern 3: Output structure is label-only (A/B/C/D) — no Hindi explanatory feedback evaluated
- **Dimension(s):** OO, OF
- **Observation:** Every MMLU example in the dataset has a single scalar `answer` field (ClassLabel 0–3 corresponding to A–D). The benchmark evaluates only whether a model selects the correct letter. There is no field for rationale, explanation, or free-form text output. The benchmark structure makes it architecturally impossible to assess a model's capacity to generate Hindi-language explanatory feedback.
- **Deployment relevance:** The deployment's core output requirement is a substantive Hindi-language explanation of why an answer is correct or incorrect, delivered in standard Manak Hindi register. MMLU accuracy scores provide zero signal on this output dimension. A model could achieve 90% MMLU accuracy while generating incoherent or factually wrong Hindi explanations — or no Hindi output at all.
- **Datapoint citations:**
  - [D1] Schema (all configs): `answer: ClassLabel(4 classes)` with label_names `["A", "B", "C", "D"]` — confirms label-only output structure with no rationale field.
  - [D18] Example 1 (moral_scenarios, split=test, label=A): "Wrong, Wrong" — a two-word answer label; the benchmark evaluates this binary classification with no mechanism for explanatory text.
  - [D26] Example 5 (elementary_mathematics, split=test, label=A): answer=0 (A) — single integer label, no explanation field present.

#### Concern 4: Ground-truth labels reflect US moral and legal norms — not Indian stakeholder perspectives
- **Dimension(s):** OC
- **Observation:** The `moral_scenarios` config explicitly frames every question as measuring "ordinary moral standards in the US as of 2020." The `professional_law` and `high_school_government_and_politics` configs test US legal standards. All labels were validated against US-standard answer keys by US university students. No Indian subject-matter experts, UPSC/SSC exam specialists, or Hindi-medium educators participated in any documented annotation process.
- **Deployment relevance:** For any India-centric GK, Polity, or History question, the US-annotator validation chain is entirely non-representative. More immediately, the moral_scenarios items could produce systematically different correct answers under Indian cultural norms vs. US norms, undermining OC validity for the target population.
- **Datapoint citations:**
  - [D18] Example 1 (moral_scenarios, split=test, label=A): "according to ordinary moral standards in the US as of 2020? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot. Scenario 2 | I popped the ball…" — the explicit US 2020 moral framing makes these labels non-transferable to Indian cultural context.
  - [D19] Example 2 (moral_scenarios, split=test, label=B): "according to ordinary moral standards in the US as of 2020? Scenario 1 | When I went through the road block I gave the policeman my brothers ID." — US legal/moral norm (impersonation at a roadblock) may be evaluated differently under Indian law and social norms.
  - [D15] Example 2 (high_school_world_history, split=test, label=B): "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters … William Howard Russell" — the single instance of 1857 Indian content appears through a colonial British journalist's framing; the correct answer label privileges a colonial historiographic perspective that conflicts with the Indian NCERT/Bipin Chandra narrative taught in Indian competitive exam preparation.

#### MAJOR

#### Concern 5: US-specific cultural assumptions embedded throughout non-STEM items
- **Dimension(s):** IC
- **Observation:** Items across business ethics, human sexuality, human aging, high school geography, marketing, and miscellaneous configs embed US-specific institutional assumptions, demographic statistics, legal conventions, and cultural referents. This is not limited to history or law — it pervades even ostensibly "general" subjects.
- **Deployment relevance:** For a Hindi-medium aspirant from North India, these culturally embedded assumptions constitute construct-irrelevant variance that would depress performance on items even where the underlying conceptual knowledge might be present. More critically, correct answers rely on US-specific factual knowledge that is not part of any Indian competitive exam syllabus.
- **Datapoint citations:**
  - [D20] Example 3 (human_aging, split=test, label=C): "The age at which one can receive full benefits from social security … Has been increasing" — requires knowledge of US Social Security policy; irrelevant to Indian GK.
  - [D21] Example 1 (human_sexuality, split=test, label=A): "Which of the following is the most common method of birth control for married couples in the U.S." — US-specific demographic question; not part of any Indian exam syllabus.
  - [D22] Example 1 (high_school_geography, split=test, label=A): "What is the most rapidly growing religion in the United States today? … Islam" — US religion demographics; Indian Geography covers entirely different content.
  - [D45] Example 1 (miscellaneous, split=test, label=A): "A flashing red traffic light signifies that a driver should do what? … stop" — US traffic law convention; Indian traffic law uses different conventions.
  - [D48] Example 4 (college_medicine, split=test, label=D): "When preparing for the MCAT exam, a student begins studying electrochemical cells." — MCAT is a US-specific standardized test, adding irrelevant institutional framing.

#### Concern 6: Indian content appears only through colonial/Western framing — not from Indian standpoint
- **Dimension(s):** IC, OC
- **Observation:** In the entire sample, the only substantive reference to Indian history occurs in a high_school_world_history example quoting British journalist William Howard Russell's description of the 1857 Sepoy Mutiny/First War of Independence using derogatory racialized colonial language ("a subject race," "black men who dared to shed the blood of their masters"). This colonial framing is antithetical to the Indian nationalist historiography (Bipin Chandra, NCERT textbooks) that UPSC/SSC aspirants study.
- **Deployment relevance:** If this item were used to evaluate a model for the Indian deployment, a model producing an explanation aligned with NCERT's framing of 1857 as the First War of Independence would likely score lower against MMLU's label (which privileges the passage's colonial interpretation). This creates direct OC misalignment for the target population.
- **Datapoint citations:**
  - [D15] Example 2 (high_school_world_history, split=test, label=B): "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters, and that of poor helpless ladies and children … British journalist William Howard Russell, My Indian Mutlny Diary, 1860" — colonial framing of 1857 event; the correct answer ("can be viewed as a reaction to the systemic brute force with which the British governed India") is framed through a second passage by Indian historian Mukherjee, but the question architecture and answer validation remain within a Western academic framework.
  - [D47] Same datapoint — "Violence, it must be emphasized, was an essential component of the British presence in India … Rudrangshu Mukherjee, 'The Kanpur [Cawnpore] Massacres in India in the Revolt of 1857,' 1990" — even the Indian historiographic passage is filtered through a comparative literature framework rather than UPSC's standard national history framing.

#### Concern 7: US customary measurement units appear in mathematics items — potential construct-irrelevant variance
- **Dimension(s):** IC
- **Observation:** Several mathematics and physics items use US customary units (miles, feet, pounds) rather than SI/metric units used in India. Indian competitive exam mathematics uses exclusively metric/SI units and Indian-context word problems.
- **Deployment relevance:** While the mathematical reasoning tested is identical, the appearance of "miles per hour" or "feet of fencing" introduces culturally unfamiliar unit terminology that could create construct-irrelevant difficulty for Hindi-medium aspirants less familiar with US measurement conventions.
- **Datapoint citations:**
  - [D25] Example 1 (elementary_mathematics, split=test, label=A): "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel? … 120 miles" — uses miles; Indian exam arithmetic problems use km/h.
  - [D28] Example 2 (college_mathematics, split=test, label=B): "A total of x feet of fencing is to form three sides of a level rectangular yard. What is the maximum possible area of the yard, in terms of x?" — uses feet; Indian exams use metres.

#### Concern 8: Professional law and accounting items test US-jurisdiction-specific professional standards
- **Dimension(s):** IO, IC
- **Observation:** The `professional_law`, `professional_accounting`, and `jurisprudence` configs contain items that require knowledge of US bar exam standards, US CPA professional conduct rules, and US tort/contract law doctrine. These are inapplicable to Indian competitive exams, which test Indian constitutional law, Indian Evidence Act, Indian Contract Act, and Indian administrative law.
- **Deployment relevance:** These configs constitute dead weight for the deployment — not only do they test irrelevant content, but a model optimized for MMLU professional law performance would be specifically tuned to US legal concepts that directly conflict with Indian legal doctrine (e.g., US "strict product liability" vs. Indian Consumer Protection Act standards).
- **Datapoint citations:**
  - [D10] Example 1 (professional_law, split=test, label=A): "A truck driver was assigned to drive a huge tractor-trailer loaded with logs … the girl's parents … assert a claim against the lumber company" — US tort scenario.
  - [D32] Example 1 (professional_accounting, split=test, label=A): "Which of the following procedures does a CPA usually perform when reviewing the financial statements of a nonissuer?" — US CPA standards, not ICAI (Indian CA) standards.
  - [D33] Example 1 (jurisprudence, split=test, label=A): "Bill purchased a can of Sipep from the Ajax Minimart … In a strict product liability tort action against Ajax, Bill must prove … Ajax is a merchant selling Sipep." — US product liability doctrine.

#### MINOR

#### Concern 9: Surface-level Indian name inclusion without substantive Indian cultural relevance
- **Dimension(s):** IC
- **Observation:** One high_school_psychology example uses the Indian name "Jyoti" in an otherwise Western cultural context (waiting in line for rock concert tickets). This is cosmetic name inclusion that does not constitute genuine India-relevant content.
- **Deployment relevance:** Superficial name substitution without cultural grounding could create a misleading appearance of Indian-context coverage. It does not address any of the actual cultural or content gaps.
- **Datapoint citations:**
  - [D37] Example 1 (high_school_psychology, split=test, label=A): "Jyoti notes the behavior of people as they wait in line for tickets to rock concerts. Which of the following research methods is she using?" — Indian name in a rock concert queue context that is culturally foreign to North Indian aspirants.

#### Concern 10: Rare South Asian religious content (Jainism) present but not aligned with Indian competitive exam priorities
- **Dimension(s):** IO
- **Observation:** Two world_religions items address Jainism specifically — a South Asian religion. This constitutes the clearest South Asian content in the entire sample. However, Jainism represents a minor sub-topic in UPSC/SSC world religions coverage, and the framing is from an academic world religions perspective rather than the NCERT/competitive exam curriculum perspective.
- **Deployment relevance:** While these items demonstrate that MMLU is not entirely devoid of South Asian religious content, their presence does not constitute meaningful coverage of the Indian religions (Hinduism, Buddhism, Jainism, Sikhism) as taught in UPSC GS Paper I Indian Culture section, where the emphasis is on philosophical schools, texts, and historical development within the Indian context.
- **Datapoint citations:**
  - [D35] Example 2 (world_religions, split=test, label=B): "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" — Jainism content, but framed as generic world religions trivia rather than Indian cultural history.
  - [D36] Example 4 (world_religions, split=test, label=D): "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" — Jain sect distinction, minor sub-topic in Indian competitive exam coverage.

#### Concern 11: Global Facts config contains India-referencing items but tests Western-sourced statistical trivia rather than Indian GK curriculum
- **Dimension(s):** IC
- **Observation:** Two global_facts examples reference India — one on internet usage (2017 data) and one on attitudes toward diversity (2018 Pew data). These are not items drawn from Indian GK curriculum sources (PIB, Economic Survey, Census of India) but from international polling organizations using Western survey methodologies.
- **Deployment relevance:** The content format differs from UPSC/SSC GK questions, which draw on official Indian government sources. A model tuned on MMLU global facts would learn to cite Pew/Gallup statistics rather than National Sample Survey Office (NSSO) or Census of India data that appears in competitive exam questions.
- **Datapoint citations:**
  - [D23] Example 2 (global_facts, split=test, label=B): "As of 2017, what fraction of the population in India used the internet in the past three months? … 26%" — Pew Research sourced India statistic; UPSC GK uses TRAI/IAMAI data.
  - [D24] Example 4 (global_facts, split=test, label=D): "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … in their country makes it a better place to live … 68%" — Pew global attitudes survey; not a standard UPSC/SSC GK source format.

---

### Content Coverage Summary

The sampled data confirms MMLU as a coherent, well-structured benchmark anchored entirely in an English-language, US/Western academic tradition. Subject coverage across 57 configs is internally consistent: mathematics and STEM items are culturally neutral; humanities and social science items are systematically US- or Western-centric; professional items (law, accounting, medicine) are calibrated to US professional licensing standards. The benchmark spans genuine breadth in its intended domain but has no subject track — and produces no individual item in the sample — that addresses Indian Polity, Indian History, Indian Geography, Hindi language proficiency, or Current Affairs relevant to India.

The most striking finding from direct content examination is the near-total absence of South Asian content: two Jainism questions in world_religions, one colonial-framed 1857 Mutiny question in world_history, and two Pew-data India-statistic questions in global_facts constitute the entirety of India-referencing content across approximately 200 sampled items. Where India does appear (D15, D47), it is filtered through a Western/colonial academic lens incompatible with the NCERT-aligned nationalist historiography that Indian competitive exam aspirants study.

The language register throughout is formal academic English. Questions range from terse (conceptual_physics, elementary_mathematics) to lengthy multi-paragraph primary-source readings (high_school_european_history, high_school_us_history, high_school_world_history). None of the inputs contains any Devanagari script, Hindi vocabulary, or code-mixed phrasing. The output structure is universally a single integer (0–3) representing the correct answer letter, with no rationale field.

---

### Limitations

1. **Sample size per config:** With 5–6 examples per config, coverage within each subject is limited. Rare India-relevant items within a config (if any exist) may not have appeared in the sample. The absence of South Asian content in the sample is consistent with but not a mathematical proof of complete absence across all 14,079 test items.

2. **Auxiliary train split not fully analyzed:** The auxiliary_train config (professional law focus) was sampled with only 5 examples and confirms US legal content, but its full 1.6M+ legal case summary content was not inspectable.

3. **Hindi translation variants not in scope:** This analysis covers only the original English cais/mmlu dataset. Community-translated Hindi MMLU variants (OpenAI MMMLU, IndicMMLU-Pro) were not sampled and their quality cannot be assessed from this data.

4. **Output quality unverifiable from dataset alone:** The label-only output structure means that any assessment of Hindi explanatory feedback quality must come from external model evaluation, not from the benchmark data itself.

5. **Moral scenarios cultural equivalence unverifiable at scale:** The moral_scenarios config explicitly invokes US 2020 moral standards. Whether the correct answers would align with Indian stakeholder judgments requires systematic cross-cultural annotation that cannot be inferred from reading examples alone.

6. **World religions coverage of Hinduism/Buddhism:** Only 6 world_religions items were sampled. The config may contain more South Asian religious content not captured in the sample, though the subject taxonomy and scoring would still reflect academic comparative religion rather than UPSC Indian Culture curriculum framing.

