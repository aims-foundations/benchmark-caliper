## Deployment Context

**Use case:** Deployment scenario: A Hindi-speaking teacher in India uses an LLM to evaluate student responses in an examination setting, assign scores with the support of an AI system, and provide feedback.

Domain: Educational assessment
Setting: Mobile application / enterprise software

Note: The deployment hypothesis should be tested using Hindi-language sentences from the benchmark, as I am familiar with the language and can provide evaluation at a subsequent stage.
**Target population:** A postgraduate- or PhD-qualified teacher with 0–20+ years of teaching experience in Hindi, based in North India and interacting in the Hindi language.

# Validity Analysis: milu
**Target context:** North Indian Hindi-Medium Postgraduate Teacher — MCQ Evaluation Deployment
**Overall risk:** MEDIUM

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology | 3 | Moderate gaps | medium |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ✓ | 4 | Minor gaps | high |
| Output Content ⚠ | 2 | Significant gaps | medium |
| Output Form ✓ | 5 | Strong alignment | high |
| **Average** | **3.3** | | |

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

MILU presents a structurally compatible MCQ benchmark for the North Indian Hindi-medium teacher deployment — the format, output schema, scoring metric, and Devanagari script all match the deployment exactly, and Hindi is the highest-resource Indic language in MILU's scope. However, the HIGH-priority Input Content dimension reveals a critical empirical concern: 100% of sampled Hindi validation items are machine-translated from English (is_translated=True), far exceeding the dataset-wide 25% translation figure cited in the paper. Translated items use English transliterations for technical vocabulary that may not align with state-board Hindi conventions, the only sampled Literature item is about Wordsworth (not canonical Hindi authors), and only one item explicitly references North Indian state content. Combined with absent annotator demographics and no published per-state Hindi-source distribution, the benchmark provides weaker evidence than its India-first framing suggests for the specific construct of evaluating Hindi-medium board-aligned MCQ comprehension. Output ontology, output form, and input form are well-aligned; input ontology is partially aligned with notable gaps in school-literature framing and state civics; input content and output content are the dimensions where validity is most attenuated.

## Practical Guidance

### What This Benchmark Measures

MILU validly measures an LLM's ability to answer single-correct-answer Hindi MCQs sourced from (or translated to look like) Indian competitive-exam content across 8 broad domains, with reliable binary-scored output that matches the deployment's positive/negative marking schema. The strongest dimensions — Output Form (5), Output Ontology (4), and Input Form (4) — confirm that the benchmark's scoring infrastructure and Hindi/Devanagari modality are a direct fit for this deployment.

### Construct Depth

Construct depth is shallow-to-moderate for the deployment's actual target construct (Hindi-medium board-aligned MCQ evaluation). The benchmark probes pan-India competitive-exam-style knowledge in formal Khari Boli, but the dataset analysis reveals that the Hindi validation split is dominated by GPT-4O translations from English source items, which means MILU primarily tests translated-English knowledge rendered in Hindi rather than natively-sourced Hindi-medium curricular knowledge. Coverage of canonical Hindi-board literature (Tulsidas, Premchand), state-specific civics (UP/MP/Rajasthan/Bihar Panchayati Raj), and school-register content (vs. competitive-GK register) is empirically weak in the sampled data.

### What Else You Need

To complete the assessment for this deployment, supplement MILU with: (1) a curated Hindi-board test set using items from UP/MP/Rajasthan/Bihar/CBSE Hindi-medium board exams (addresses Input Content and Input Ontology gaps); (2) a Hindi literature MCQ set covering canonical authors in school-literature register (addresses the Wordsworth-vs-Tulsidas Arts & Humanities gap); (3) a state civics and Panchayati Raj MCQ set (addresses Input Ontology under-representation); (4) Hindi-medium teacher annotator validation of a sample of translated MILU items to estimate translation-induced answer-key error rate (addresses Output Content and Input Content concerns); (5) verification that production inference mode matches the evaluation method used (log-likelihood vs. generative) per [Q85].

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
MILU's taxonomy of 8 domains and 41 subjects spans the breadth needed for a multi-subject teacher-evaluation deployment, and the format is exclusively single-correct-answer MCQ, which is a direct structural match for the deployment's binary positive/negative marking requirement. However, the taxonomy is derived from competitive exam content (UPSC/SSC/state PSC) rather than school-board syllabi, and the dataset sample shows a heavy skew toward Engineering & Tech (23% of Hindi validation items) with under-representation of Civics/Political Science and Panchayati Raj content that is central to UP/MP/Rajasthan/Bihar state-board curricula. Per-subject statistics for Hindi specifically are not publicly available, making it impossible to verify whether the categories adequately cover state-board curricular framing.

**Strengths:**
- Exclusive single-answer MCQ format directly matches the deployment's binary scoring requirement [Q22, Q33, DATASET-D1]
- All 8 declared domains appear in the Hindi validation sample, providing nominal multi-domain breadth [DATASET-D1, D2, D4, D9, D20]
- Indic LLM sub-taxonomy is treated separately, indicating awareness of system heterogeneity [Q60]

**Checklist:**

- **IO-1**: Required categories for the deployment include Hindi Literature (canonical board authors), History (regional medieval and freedom movement), Civics/Political Science with Panchayati Raj and state administration, Geography of North India, Science/Maths in Hindi, Economics, and General Knowledge. MILU declares all 8 domains and 41 subjects [Q42] which nominally cover this breadth, with subject-level statistics in supplementary Table 9 [Q98]. — _Sources: Q42, Q98_
- **IO-2**: MILU's taxonomy is derived from competitive exam content [Q23, Q24, Q27] rather than school/university board syllabi. State-specific civics (Panchayati Raj, state legislatures) is not visible as a dedicated category in the sample [DATASET-D4 is the only Law & Governance item, and concerns the 44th constitutional amendment, not state-level civics]. The single dedicated Hindi-board literature register (close reading of Tulsidas/Premchand/Kabir) appears absent from the sample [DATASET-D5 — the only Literature item is about Wordsworth]. — _Sources: Q23, Q24, DATASET-D4, DATASET-D5_
- **IO-3**: Engineering & Tech dominates the Hindi validation sample (6 of 26 items) including DC motors, transformers, rectifiers, and FORTRAN [DATASET-D1, D13, D14, D23], which are characteristic of polytechnic/engineering entrance content rather than secondary or degree-college teacher domains. This represents construct-irrelevant variance for a general Hindi-medium teacher deployment. — _Sources: DATASET-D1, DATASET-D13, DATASET-D14, DATASET-D23_
- **IO-4**: Identified gaps: (a) school-literature framing for Hindi canonical authors absent; (b) state-specific civics/Panchayati Raj under-represented; (c) over-representation of engineering content; (d) per-language per-subject distributions not published [NOT FOUND per regional YAML state_wise_exam_source_distribution_for_hindi]. — _Sources: WEB-9, WEB-12_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge.' (p.3)
- [Q42] 'we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies.' (p.4)
- [Q23] 'This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others.' (p.3)
- [Q24] 'These questions were sourced following an approach similar to AGIEVAL... collecting the questions from various public exams... such as qualification tests and national and state-level civil services exams' (p.3)
- [Q98] 'Table 9: Detailed subject level statistics of MILU across different languages.' (p.20)

*Web sources:*
- [WEB-12] GitHub subject list includes 'Literature and Linguistics' and 'Arts and Culture' as nominal categories
- [WEB-9] HuggingFace dataset is gated, limiting independent verification of per-subject Hindi distributions

*Dataset analysis:*
- DATASET-D1, D13, D14, D23: Engineering & Tech items (DC motors, rectifiers, transformers, FORTRAN) over-represented in Hindi validation sample
- DATASET-D4: only Law & Governance item is constitutional amendment, not state-level civics or Panchayati Raj
- DATASET-D5: only Literature & Linguistics item in Hindi sample concerns Wordsworth (English poet), not Hindi-board canonical literature

</details>

**Information gaps:**
- Per-language per-subject item counts for Hindi not published in accessible form (Table 9 in gated PDF)
- Whether the test split's domain distribution matches the sampled validation distribution
- Whether MILU includes any items framed in school-literature register vs. competitive-exam GK

**Requires expert verification:**
- Whether the 41-subject taxonomy maps cleanly onto UP/MP/Rajasthan/Bihar board syllabi at the subject level
- Whether the missing categories (state civics, Hindi literary close reading) are material to teacher use cases or marginal

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Input content is the highest-priority dimension per elicitation (HIGH), and dataset analysis reveals a critical concern: all 26 sampled Hindi validation examples are flagged is_translated=True, suggesting the Hindi validation split is dominated by GPT-4O-translated English-source items rather than natively-sourced Hindi competitive-exam questions. While MILU's documentation claims an India-first design [Q11] and includes regionally relevant subjects [Q12, Q14], the actual Hindi content sampled shows: (a) literary content focused on Wordsworth rather than Tulsidas/Premchand/Kabir [DATASET-D5]; (b) translated technical terminology using transliterations (शेल, नाइट्रेट, जंप लेबल) that may not align with state-board Hindi textbook conventions [DATASET-D14, D15, D23]; (c) only one item with explicit North Indian state-specific content (UP minerals) [DATASET-D2]; (d) parallel translated items appearing across all 11 language configs [DATASET-D11, D18, D19, D24]. The paper's dataset-level 25% translation figure [Q47] underestimates the apparent Hindi-validation-split translation rate.

**Strengths:**
- Documented India-first design intent with stated coverage of local history, arts, festivals, and laws [Q2, Q11, Q12]
- Region-specific exams are explicitly emphasized for capturing local knowledge [Q14, Q28]
- Some India-centric Hindi items present (UP minerals, Mughal history, Amrita Shergil, Radcliffe Line) [DATASET-D2, D3, D8, D25]
- Cross-language answer-key consistency demonstrated for translated parallel items [DATASET-D18, D19]

**Checklist:**

- **IC-1**: The deployment requires region-specific knowledge: North Indian state geography, Hindi-board canonical literature, Panchayati Raj civics, state freedom-movement figures. The Hindi sample contains some India-centric items [DATASET-D2, D3, D25] but a majority of items are translated [DATASET-D28] and may not reflect native Hindi competitive-exam content. — _Sources: Q11, Q14, DATASET-D2, DATASET-D3, DATASET-D25, DATASET-D28_
- **IC-2**: Cultural alignment is partially present (Mughal history, Indian arts, partition geography are reasonable matches [DATASET-D3, D8, D25]), but the Hindi-literature register [DATASET-D5 — Wordsworth as the only literature item] does not match Hindi-medium school-board norms. Canonical Hindi literary figures (Tulsidas, Premchand, Kabir, Mahadevi Varma) are not present in the sampled items. — _Sources: Q12, DATASET-D3, DATASET-D5, DATASET-D8_
- **IC-3**: Translated items retain English technical transliterations (शेल, नाइट्रेट, पल्सेटिंग डीसी, जंप लेबल) [DATASET-D14, D15, D23] that may diverge from Vaigyaanik evam Takniki Shabdavali Aayog or state-board conventions. The Wordsworth literature item [DATASET-D5] introduces non-regional content. Translated items effectively test translated-English knowledge rather than native Hindi-register knowledge. — _Sources: DATASET-D5, DATASET-D14, DATASET-D15, DATASET-D23_
- **IC-4**: INSUFFICIENT DOCUMENTATION — MILU does not document recruitment of Hindi-medium North Indian annotators specifically [NOT FOUND per regional YAML annotator_demographics]; institutional base is IIT Madras + IBM Research India, which does not guarantee North Indian Hindi-medium representation.
- **IC-5**: Documented content issues: (a) ~100% translation rate observed in Hindi validation sample vs. ~25% claimed dataset-wide [Q47, DATASET-D28]; (b) absence of canonical Hindi-board literary content; (c) under-representation of UP/Bihar/Rajasthan/MP state-specific civics; (d) translation terminology not validated against state-board Hindi norms [NOT FOUND per regional YAML hindi_register_standardisation]. — _Sources: Q47, Q84, DATASET-D28, WEB-19_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q11] 'We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams.' (p.2)
- [Q14] 'We focus on region-specific exams to authentically capture local knowledge in the respective language.' (p.2)
- [Q44] 'For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O.' (p.4)
- [Q45] 'We chose GPT-4O over specialized translation models for their ability to remain task-aware during translation' (p.4)
- [Q47] 'Of the total 79K questions, only 25% of questions are translated from English' (p.4)
- [Q72] 'This suggests that the training corpora for these models lack sufficient culturally specific data.' (p.7)
- [Q84] 'Third, the scarcity of questions necessitated translating a portion of the dataset.' (p.9)

*Web sources:*
- [WEB-19] Bihar's majority population speaks Bhojpuri (24.86%), Maithili (12.55%), Magahi (10.87%) — Khari Boli register may amplify mismatch for this sub-population
- [WEB-12] GitHub subject categories include 'Literature and Linguistics' and 'Arts and Culture' but no item-level framing detail published

*Dataset analysis:*
- DATASET-D28: All 26 Hindi validation examples flagged is_translated=True — apparent translation rate far higher than the 25% dataset-wide figure
- DATASET-D5: Only Literature & Linguistics item in Hindi sample is about Wordsworth, not Hindi-board canonical literature
- DATASET-D14, D15, D23: Translated items use English transliterations (शेल, नाइट्रेट, जंप लेबल) of unvalidated alignment with state-board Hindi conventions
- DATASET-D2: Only one item with explicit North Indian state content (UP minerals) in 26-item sample
- DATASET-D11, D18, D19, D24: Same source questions appear translated word-for-word across multiple language configs

</details>

**Information gaps:**
- Whether the test split is also predominantly is_translated=True (only validation split sampled)
- Hindi-specific translation proportion in MILU (paper reports only dataset-wide 25%)
- State-wise distribution of Hindi exam sources (UP/MP/Rajasthan/Bihar shares)
- Whether Hindi literature items in the un-sampled portion include canonical board authors

**Requires expert verification:**
- Whether GPT-4O Hindi translations preserve subject-specific terminology in line with UP/MP/Rajasthan/Bihar state-board textbooks
- Whether Khari Boli register mismatches with Bhojpuri/Maithili-speaking Bihar teachers materially affect comprehension
- Whether 'शेल', 'नाइट्रेट', 'जंप लेबल' style transliterations are acceptable in state-board Hindi technical texts

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form is well-aligned with the deployment context. MILU is exclusively text-based MCQ in Devanagari script for Hindi [DATASET-D6, D7], which matches the deployment's Hindi/Devanagari text-only modality. Hindi is high-resource within MILU's 11-language scope [Q5, Q76], questions with images, reading comprehension, and >4 options were excluded for uniformity [Q33], and language verification used INDICLID and Unicode filtering [Q34]. Manual review steps [Q32, Q36] add quality assurance. The minor concerns are: (a) one truncated English item observed [DATASET-D30] indicates residual data quality noise; (b) translation-induced register mismatch in technical vocabulary may affect surface form for translated items [DATASET-D14, D15, D23], though this is more accurately a content concern. No script, modality, or signal-distribution mismatch with the deployment.

**Strengths:**
- Clean Devanagari script throughout the Hindi sample with formal Khari Boli register [DATASET-D6, D7]
- Image-based, reading-comprehension, and >4-option items explicitly excluded for uniformity [Q33]
- Language verification via INDICLID and Unicode filtering ensures script correctness [Q34]
- Hindi is high-resource within MILU's scope, favouring this deployment [Q5, Q76]

**Checklist:**

- **IF-1**: Signal distribution alignment is strong: both benchmark and deployment are text-only Hindi/Devanagari MCQ [Q22, Q33, DATASET-D6]. No modality, resolution, or sensor mismatch. — _Sources: Q22, Q33, DATASET-D6_
- **IF-2**: Regional infrastructure can support text-only Hindi MCQ — Devanagari IME and mobile rendering are mature. Connectivity is the main constraint (Bihar 43%, UP 46% general-population internet penetration [WEB-4]; rural school internet at 18% [WEB-5]) but does not affect input-form fidelity per se. — _Sources: WEB-4, WEB-5_
- **IF-3**: MCQ four-option format with single correct answer matches deployment requirement exactly [Q33, DATASET-D1]. Translation-induced terminology choices [DATASET-D14, D15, D23] are a register concern but are scored under input content rather than form. — _Sources: Q33, DATASET-D1_
- **IF-4**: Minor form-level issue: one truncated English item observed [DATASET-D30], suggesting residual noise despite filtering. No systemic form mismatch. — _Sources: DATASET-D30, Q32, Q36_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs)' (p.3)
- [Q33] 'we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q34] 'we utilize a combination of INDICLID... and Unicode-based filtering, ensuring that the questions are in the correct language.' (p.4)
- [Q5] 'Models also perform better in high-resource languages as compared to low-resource ones.' (p.1)
- [Q32] 'Initially, we manually review a large sample of questions to detect and eliminate potential sources of noise.' (p.4)
- [Q36] 'As a final step, we manually verify a sample of questions from each language to ensure accuracy' (p.4)

*Web sources:*
- [WEB-4] Bihar internet penetration ~43%, UP ~46% (IAMAI/Kantar 2024) — relevant to deployment but not benchmark form
- [WEB-5] Rural school internet access ~18% — affects deployment delivery, not benchmark input form

*Dataset analysis:*
- DATASET-D6: Formal Khari Boli Hindi grammar item in clean Devanagari
- DATASET-D7: Hindi GK question in standard written Hindi/Devanagari
- DATASET-D30: One truncated English question stem indicates residual data quality noise

</details>

**Information gaps:**
- Frequency of truncated/incomplete items across the full dataset (only one observed in sample)

---

### Output Ontology — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output ontology is well-aligned with the deployment. Ground-truth labels are single correct answers per MCQ drawn from exam answer keys [Q12], which exactly matches the deployment's binary correct/incorrect requirement with positive/negative marking. The label schema is binary at inference time, and the elicitation explicitly confirmed that 'evaluation schemas across boards and states are described as broadly similar' [A4], so competitive-exam keyed answers are considered compatible. The 41-subject 8-domain organisation [Q42] supports per-subject reporting useful for diagnostic analysis. Domain-level analysis surfaces a known weakness of LLMs in culturally specific areas [Q20, Q71, Q77], which the deployment user should be aware of. The taxonomy was derived bottom-up from ~20K fine-grained tags clustered and manually merged [Q39, Q40, Q41], which is sound methodology, although whether the resulting categories carry any culturally variable correct-answer norms is not analysed.

**Strengths:**
- Single-correct-answer ground truth from exam answer keys directly matches binary scoring requirement [Q12]
- 41-subject 8-domain organisation supports diagnostic per-subject reporting [Q42]
- Cross-language answer-key consistency for parallel items [DATASET-D18, D19] confirms reliable label application
- Elicitation confirms competitive-exam keys are broadly compatible with North Indian board norms [A4]

**Checklist:**

- **OO-1**: Output labels are MCQ option indices (option1–option4) with a single target [Q12, DATASET-D1]. This is regionally relevant — Indian competitive and board MCQs use the same single-correct format with positive/negative marking [WEB-1, WEB-2]. — _Sources: Q12, DATASET-D1, WEB-1_
- **OO-2**: No regionally specific output categories appear missing for a binary MCQ deployment. The deployment does not require partial-credit, rubric, or multi-label output [A1, A2]. — _Sources: Q42_
- **OO-3**: No categories visibly encode non-regional values. The user confirmed evaluation schemas are broadly consistent across North Indian boards and competitive exams [A4], reducing the risk that competitive-exam answer keys diverge from board norms. — _Sources: Q12_
- **OO-4**: Stakeholder-driven taxonomy redesign is not required — the deployment uses the same single-answer MCQ taxonomy as the benchmark.
- **OO-5**: No major taxonomy issues identified. Minor caveat: domain-level categorisation may aggregate over heterogeneous content (e.g., Arts & Humanities mixing competitive-GK and literature) [Q20, Q77], which could affect interpretation of domain-level scores. — _Sources: Q20, Q77_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science.' (p.2)
- [Q42] 'we determine 41 distinct subject names, which fall into eight main domains' (p.4)
- [Q39] 'in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap.' (p.4)
- [Q41] 'We manually review these clusters and assign appropriate subject labels.' (p.4)
- [Q20] 'Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM.' (p.2)
- [Q77] 'the domain-specific analysis indicates that models perform better in general fields such as STEM while facing challenges in culturally relevant subjects' (p.8)

*Web sources:*
- [WEB-1] Indian competitive exams use single-correct MCQ with positive/negative marking — taxonomically aligned with MILU output schema
- [WEB-2] UPSC and similar exams confirm single-answer MCQ output convention

*Dataset analysis:*
- DATASET-D1: option2 single-target labelling consistent across the sample
- DATASET-D18, D19: Same correct option (option3) across English and Hindi parallel items confirms answer-key consistency

</details>

**Information gaps:**
- Whether domain-level aggregation hides subject-level mismatches relevant to the teacher deployment

**Requires expert verification:**
- Whether competitive-exam answer keys for items in Hindi Literature and Civics agree with state-board mark-scheme conventions in detail

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
Output content (label correctness for individual datapoints) carries moderate validity risk because MILU does not document annotator demographics or inter-annotator agreement. Annotation relied primarily on subject experts at online exam portals [Q26] with manual audit by AI4Bharat volunteers [Q87]; institutional base is IIT Madras + IBM Research India [Q10], which does not guarantee Hindi-medium North Indian educational representation. The regional YAML notes 'no published MILU source provides annotator demographic details or inter-annotator agreement statistics'. The elicitation does mitigate this concern: the user confirmed evaluation schemas are 'broadly consistent across boards and competitive-exam settings' [A4], and dataset analysis shows cross-language answer-key consistency for parallel items [DATASET-D18, D19]. However, with ~all sampled Hindi validation items machine-translated [DATASET-D28], the original answer keys derive from English-source items and were applied to GPT-4O translations without documented Hindi-medium subject-expert audit of the translation-key alignment.

**Strengths:**
- Subject experts at online exam portals provided initial answer accuracy [Q26]
- AI4Bharat volunteer team performed manual audits [Q87]
- Cross-language answer-key consistency observed for parallel items [DATASET-D18, D19]
- Elicitation confirms low expected divergence between competitive-exam keys and North Indian board norms [A4]

**Checklist:**

- **OC-1**: Ground-truth labels derive from exam answer keys [Q12, Q26]; the elicitation confirms these are broadly compatible with North Indian teacher norms [A4]. However, no Hindi-medium North Indian stakeholder validation is documented. — _Sources: Q12, Q26_
- **OC-2**: Disagreement risk is moderate: most items (factual GK, science, history) are unlikely to have culturally variable answers, but translated items where GPT-4O may have introduced subtle translation errors [DATASET-D14, D15, D23] could yield Hindi-translation answer-key errors not caught by audit. — _Sources: DATASET-D14, DATASET-D15, DATASET-D23_
- **OC-3**: INSUFFICIENT DOCUMENTATION — MILU does not provide annotator demographic breakdowns (regional background, Hindi-medium vs. English-medium education, subject expertise) [NOT FOUND per regional YAML annotator_demographics]; no inter-annotator agreement statistics are reported.
- **OC-4**: Re-annotation by Hindi-medium North Indian teacher pool would address the documented gap, particularly for translated items and Arts & Humanities content where register matters most. — _Sources: Q87_
- **OC-5**: INSUFFICIENT DOCUMENTATION — aggregation methods for the cluster-to-subject manual merging [Q41] do not report how disagreements among annotators were resolved, leaving minority-perspective handling opaque.
- **OC-6**: Documented label issues: (a) annotator demographics opaque; (b) no inter-annotator agreement; (c) translated items inherit English-source keys without documented Hindi-medium subject-expert validation. — _Sources: Q26, Q87, WEB-10, DATASET-D28_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q26] 'These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers.' (p.3)
- [Q87] 'We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits.' (p.9)
- [Q10] 'Nilekani Centre at AI4Bharat, Indian Institute of Technology, Madras, IBM Research, India' (p.1)
- [Q41] 'We manually review these clusters and assign appropriate subject labels.' (p.4)
- [Q12] 'These questions include culturally relevant subjects such as local history, arts, festivals, and laws' (p.2)

*Web sources:*
- [WEB-10] NAACL 2025 paper does not publish annotator demographic details or inter-annotator agreement

*Dataset analysis:*
- DATASET-D18, D19: Cross-language parallel items maintain answer-key consistency
- DATASET-D28: All sampled Hindi validation items are translations — keys are inherited from English sources without documented Hindi-medium audit

</details>

**Information gaps:**
- Annotator demographics (region, language background, subject expertise)
- Inter-annotator agreement statistics
- Whether translated Hindi items underwent Hindi-medium subject-expert key validation
- Disagreement-resolution protocols in cluster-to-subject manual merging

**Requires expert verification:**
- Spot-check a sample of translated Hindi answer keys against North Indian teacher judgment
- Verify that competitive-exam keys for Hindi literature, civics, and regional history items align with state-board mark schemes

---

### Output Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
Output form is fully aligned. MILU evaluates models using accuracy as the primary metric [Q3, Q15, Q16, Q75], with log-likelihood scoring for non-API models [Q52–Q55] and structured JSON generative output for API-based models [Q56, Q57]. The output form is a single label/answer index, which directly matches the deployment's binary correct/incorrect MCQ scoring requirement. Per-subject, per-language, per-shot result tables [Q99–Q132] provide granular evidence for Hindi-specific performance. The author-acknowledged caveat that log-likelihood evaluation may yield different results than generation-based or chain-of-thought evaluation [Q85] is relevant if the deployment's runtime inference is generative — the user should verify that production inference matches the evaluation method used to characterise the chosen model.

**Strengths:**
- Accuracy metric directly matches binary MCQ correct/incorrect scoring [Q3, Q16]
- Both log-likelihood [Q52–Q55] and structured JSON generative [Q56, Q57] evaluation modes available
- Granular per-subject per-language reporting at 0/1/5-shot [Q99–Q132] enables Hindi-specific performance lookup
- Authors document the log-likelihood vs. generation caveat explicitly [Q85]

**Checklist:**

- **OF-1**: Output modality is a single discrete answer choice, matching deployment requirement exactly [Q3, Q53–Q55]. No mismatch. — _Sources: Q3, Q53, Q55, DATASET-D1_
- **OF-2**: Text-to-speech is not required for this deployment (text-only Hindi MCQ); no concern.
- **OF-3**: Target population is postgraduate-qualified Hindi-medium teachers — high literacy assumed; no accessibility-driven output-form constraint identified.
- **OF-4**: Documented caveat: log-likelihood evaluation may diverge from generation-based or CoT performance [Q85]. If deployment uses generative inference, model selection should be informed by API-mode evaluation rather than non-API log-likelihood numbers. — _Sources: Q85_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%.' (p.1)
- [Q52] 'For non-API-based models, we use the LM-EVALUATION-HARNESS... to ensure clean and reproducible evaluations.' (p.5)
- [Q55] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability' (p.5)
- [Q57] 'We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing.' (p.5)
- [Q85] 'our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting.' (p.9)

*Dataset analysis:*
- DATASET-D1: Single 'target' field (e.g., option2) confirms the output form is a single-answer label

</details>

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** 100% of sampled Hindi validation items are machine-translated; translated technical terminology uses English transliterations of unvalidated alignment with state-board Hindi norms; canonical Hindi-board literary content absent from sample

**Recommendation:** Stratify any deployment-relevant evaluation by is_translated flag and report performance separately for natively-sourced vs. translated Hindi items; supplement with a curated set of native Hindi-board MCQs covering Hindi literature canonical authors and verified state-board terminology

### Input Content ⚠

**Gap:** No published state-wise breakdown of Hindi exam sources for UP/MP/Rajasthan/Bihar

**Recommendation:** Request access to the gated HuggingFace dataset metadata (or supplementary Table 8) and audit the Hindi item provenance by source-exam state; if Hindi-belt state-PSC sourcing is thin, supplement with state-PSC items directly

### Output Content ⚠

**Gap:** No annotator demographics or inter-annotator agreement published; translated Hindi items inherit English-source keys without documented Hindi-medium subject-expert audit

**Recommendation:** Conduct a focused re-annotation audit by Hindi-medium North Indian teachers on a stratified sample (~200 items) of MILU Hindi items, prioritising Arts & Humanities, Law & Governance, and translated science items to estimate label-correctness rates

### Input Form

**Gap:** Residual data quality noise observed (one truncated English item)

**Recommendation:** Run a lightweight pre-deployment quality filter on Hindi items (minimum stem length, option completeness checks) to surface any analogous cases before relying on MILU scores for model selection

### Input Ontology

**Gap:** Heavy skew toward Engineering & Tech (23% of Hindi sample) and under-representation of Civics/Political Science, Panchayati Raj, and state-board literature framings

**Recommendation:** Use MILU domain-level results as a coarse signal only; build a deployment-specific subject inventory that mirrors UP/MP/Rajasthan/Bihar board syllabi, and weight or filter MILU subjects to align with actual teacher use cases

### Output Form

**Gap:** Log-likelihood evaluation may diverge from generative inference (acknowledged by authors)

**Recommendation:** If production deployment uses generative inference, base model selection on the API-mode (generative) MILU results rather than log-likelihood numbers, or run an internal generative re-evaluation on the candidate model

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge." |
| Q2 | 1 | input_content | "With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science." |
| Q3 | 1 | output_form | "We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q4 | 1 | output_form | "Open multilingual models outperform language-specific fine-tuned models, which perform only slightly better than random baselines." |
| Q5 | 1 | input_ontology | "Models also perform better in high-resource languages as compared to low-resource ones." |
| Q6 | 1 | input_ontology | "Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM." |
| Q7 | 1 | input_ontology | "To the best of our knowledge, MILU is the first of its kind benchmark focused on Indic languages, serving as a crucial step towards comprehensive cultural evaluation." |
| Q8 | 1 | output_form | "All code, benchmarks, and artifacts will be made publicly available to foster open research." |
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
| Q21 | 2 | output_form | "All the artifacts will be released publicly." |
| Q22 | 3 | input_ontology | "MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge." |
| Q23 | 3 | input_ontology | "This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others." |
| Q24 | 3 | input_content | "These questions were sourced following an approach similar to AGIEVAL (Zhong et al., 2023), collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams, among others." |
| Q25 | 3 | input_content | "We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages." |
| Q26 | 3 | output_content | "These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers." |
| Q27 | 3 | input_content | "Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years." |
| Q28 | 3 | input_content | "Regional state exams are particularly valuable as they cover various state-level topics and emphasize the official language of each state." |
| Q29 | 3 | input_content | "In total, we collected more than 150K questions across 11 Indian Languages- Bengali (bn), Gujarati (gu), Hindi (hi), Kannada (kn), Malayalam (ml), Marathi (mr), Odia (or), Punjabi (pn), Tamil (ta), Telugu (te), and English (en)-spanning 41 diverse subjects." |
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
| Q46 | 4 | input_content | "In total, we release around 79K questions across 41 subjects across 8 domains in 11 languages, capping each subject-language pair at 500 questions for feasible evaluations." |
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
| Q81 | 8 | output_ontology | "Further investigation is required to fully understand the limitations and opportunities in this area." |
| Q82 | 9 | input_ontology | "First, we restricted our study to the top 11 languages due to the lack of readily available questions in low-resource languages, which we aim to address in future work." |
| Q83 | 9 | output_form | "Second, limited computational resources prevented a thorough evaluation of larger models, such as LLAMA-3.1-70B-INSTRUCT and LLAMA-3.1-405B." |
| Q84 | 9 | input_content | "Third, the scarcity of questions necessitated translating a portion of the dataset." |
| Q85 | 9 | output_form | "Finally, our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting." |
| Q86 | 9 | output_content | "We would like to thank EkStep Foundation and Nilekani Philanthropies for their generous grant towards building datasets, models, tools and other resources for Indian languages." |
| Q87 | 9 | output_content | "We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits." |
| Q88 | 9 | input_content | "All data described in this work was scraped from publicly available resources." |
| Q89 | 9 | input_content | "The datasets used in this paper will be made available under permissible licenses." |
| Q90 | 9 | input_content | "Additionally, the code used for our evaluations will be made publicly available under the MIT License." |
| Q91 | 10 | output_content | "Sumanth Doddapaneni, Rahul Aralikatte, Gowtham Ramesh, Shreya Goyal, Mitesh M. Khapra, Anoop Kunchukuttan, and Pratyush Kumar. 2023. Towards leaving no Indic language behind: Building monolingual corpora, benchmark and models for Indic languages. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 12402–12426, Toronto, Canada. Association for Computational Linguistics." |
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
| WEB-1 | https://negativemarkingcalculator.in/ |
| WEB-2 | https://testbook.com/upsc-civil-services/negative-marking-in-upsc |
| WEB-3 | https://pwonlyias.com/negative-marking-in-upsc-exam/ |
| WEB-4 | https://www.iamai.in/sites/default/files/research/Kantar_%20IAMAI%20report_2024_.pdf |
| WEB-5 | https://www.amulyacharan.com/2024/12/17/the-digital-divide-in-education-bridging-the-urban-rural-gap/ |
| WEB-6 | https://www.roombr.com/blog/digital-classroom-govt-initiatives-india |
| WEB-7 | https://www.orfonline.org/expert-speak/five-years-of-nep-2020-and-the-promise-of-edtech |
| WEB-8 | https://www.grabon.in/indulge/tech/internet-users-statistics/ |
| WEB-9 | https://huggingface.co/datasets/ai4bharat/MILU |
| WEB-10 | https://aclanthology.org/2025.naacl-long.507/ |
| WEB-11 | https://arxiv.org/abs/2411.02538 |
| WEB-12 | https://github.com/AI4Bharat/MILU |
| WEB-13 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-14 | https://www.hoganlovells.com/en/publications/indias-digital-personal-data-protection-act-2023-brought-into-force- |
| WEB-15 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-16 | https://fpf.org/blog/five-ways-in-which-the-dpdpa-could-shape-the-development-of-ai-in-india/ |
| WEB-17 | https://www.education.gov.in/en/nep/coe-ai-education |
| WEB-18 | https://educationforallinindia.com/artificial-intelligence-in-indian-school-education-use-misuse-and-preventive-measures/ |
| WEB-19 | https://en.wikipedia.org/wiki/Bihar |
| WEB-20 | https://www.researchgate.net/publication/392504733_MILU_A_Multi-task_Indic_Language_Understanding_Benchmark |
| WEB-21 | https://aidigitalnews.com/ai/ai4bharat-and-ibm-research-india-release-new-indic-language-llm-benchmark/ |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU
**Analysis date:** 2025-01-31
**Examples reviewed:** 215 total across 11 language configs (Bengali: 21, English: 20, Gujarati: 24, Hindi: 26, Kannada: 17, Malayalam: 16, Marathi: 21, Odia: 21, Punjabi: 25, Tamil: 19, Telugu: 25); primary focus on Hindi config (26 examples)
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Hindi, validation | Ex. 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: ... मोटर की गति बहुत अधिक होती है" | Engineering question about DC series motor — translated from English | IC, IF |
| D2 | Hindi, validation | Ex. 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? ... अभ्रक" | North Indian state-specific geography: UP minerals question | IC, IO |
| D3 | Hindi, validation | Ex. 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" | Mughal history — competitive-exam GK register | IC |
| D4 | Hindi, validation | Ex. 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? 44वें संविधान संशोधन अधिनियम द्वारा" | Constitutional law MCQ — Law & Governance domain | IO |
| D5 | Hindi, validation | Ex. 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" | Literature question about English poet Wordsworth — not Hindi-board canonical literature | IC |
| D6 | Hindi, validation | Ex. 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा कि उसे अगले महीने बोनस मिलेगा।" | Hindi grammar (indirect speech) — formal Khari Boli register | IF, IC |
| D7 | Hindi, validation | Ex. 13 | option1 | "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? अरबी भाषा" | Hindi-language item about etymology of 'monsoon' — GK-style | IC |
| D8 | Hindi, validation | Ex. 22 | option4 | "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? अमृता शेरगिल" | Indian arts & culture — Amrita Shergil, India-centric | IC |
| D9 | Hindi, validation | Ex. 17 | option4 | "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? संपत्ति कर" | Economics/taxation MCQ — pan-India competitive exam register | IO |
| D10 | Hindi, validation | Ex. 15 | option3 | "1950 में स्थापित, भारतीय रेलवे द्वारा स्वामित्व वाली औद्योगिक इकाइयों में से एक का नाम भारतीय स्वतंत्रता सेनानी के नाम पर रखा गया है: चित्तरंजन दास" | Indian history — Chittaranjan Das/railways — competitive GK | IC |
| D11 | English, validation | Ex. 3 | option4 | "What was the first capital of the Bahamani Kingdom? ... Gulbarga" | Medieval Indian history — source question in English | IC |
| D12 | English, validation | Ex. 9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct? Estimate Committee: All members of this committee are from Assembly only." | Maharashtra state-specific governance question | IC, IO |
| D13 | Hindi, validation | Ex. 3 | option2 | "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" | Electrical engineering MCQ — translated from English | IC |
| D14 | Hindi, validation | Ex. 4 | option2 | "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। शेल" | Engineering transformer question — translated item with 'शेल' (shell) transliteration | IC, IF |
| D15 | Hindi, validation | Ex. 10 | option4 | "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" | Health science MCQ — translated, with 'नाइट्रेट' transliteration retained | IC |
| D16 | Gujarati, validation | Ex. 24 | option3 | "સિંધિ કવિ અને લેખક વસદેવ મોહીનું 2019 માટેના સરસ્વતી સન્માન માટે પસંદગી ... કેકે બિરલા ફાઉન્ડેશન" | Saraswati Samman award question — India-centric literary award | IC |
| D17 | Marathi, validation | Ex. 16 | option3 | "हलषष्ठी सण का साजरा केला जातो? मुलाच्या दीर्घायुष्यासाठी" | Regional Indian festival (Halsashti) — local cultural knowledge | IC |
| D18 | English, validation | Ex. 1 | option3 | "What was the immediate cause for loss of foreign reserves triggering the financial crisis in 1991? Sharp rise in value of imports of oil & petroleum products" | 1991 India economic crisis — same question as Bengali D1 | IC |
| D19 | Hindi, validation | Ex. 18 | option3 | "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था? तेल और पेट्रोलियम उत्पादों के आयात के मूल्य में तीव्र वृद्धि" | Hindi translation of English Ex. 1 — translation quality check | IC |
| D20 | Hindi, validation | Ex. 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते? आठ" | Sports GK — India-centric, recent current affairs | IC |
| D21 | Bengali, validation | Ex. 12 | option4 | ""মঙ্গল ভারত" কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল: আচার্য বিনোবা ভাবে" | Literature: 'Mangal Bharat' work attributed to Vinoba Bhave | IC |
| D22 | Telugu, validation | Ex. 25 | option1 | "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? మొరెనా" | Madhya Pradesh state-specific geography — sub-national knowledge | IC |
| D23 | Hindi, validation | Ex. 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है? एक जंप लेबल या फॉर्मेट लेबल" | Computer science MCQ — translated, technical vocabulary | IC |
| D24 | Hindi, validation | Ex. 5 | option1 | "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं: ... उत्तरी अमेरिका का अटलांटिक तट" | Mediterranean climate geography — translated, no North India content | IC |
| D25 | Hindi, validation | Ex. 19 | option3 | "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? पाकिस्तान" | Partition history — India-centric GK | IC |
| D26 | English, validation | Ex. 17 | option3 | "What is the title of Yashpal Committee Report (1993)? Learning without burden" | India education policy — relevant to teacher deployment | IO |
| D27 | Marathi, validation | Ex. 15 | option1 | "वर्ष 2020 मध्ये, भारत सरकारने राष्ट्रीय शिक्षण धोरण सादर केले. आतापर्यंत किती राष्ट्रीय शिक्षण धोरणे सादर करण्यात आली आहेत? 3" | NEP question — Indian education policy | IO |
| D28 | Hindi, validation | Ex. 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: ... is_translated: True" | is_translated=True flag on all 26 Hindi validation examples reviewed | IC |
| D29 | Gujarati, validation | Ex. 16 | option2 | "છત્તીસગઢના નીચેના કયા બળવાઓને 'બસ્તરનો સ્વાતંત્ર્ય સંઘર્ષ' પણ કહેવામાં આવે છે? લિંગગિરી બળવો" | Chhattisgarh regional history — cross-state cultural knowledge | IC |
| D30 | English, validation | Ex. 11 | option2 | "The owner of the textile shop brought a ... Calculator" | Truncated/incomplete question — possible data quality issue | IF |
| D31 | Punjabi, validation | Ex. 21 | option3 | "ਰਾਸ਼ਟਰੀ ਸਰੋਂ ਖੋਜ ਕੇਂਦਰ ਕਿੱਥੇ ਸਥਿਤ ਹੈ - ਸੇਵਰ" | National Mustard Research Centre location — Rajasthan-specific | IC |
| D32 | Hindi, validation | Ex. 24 | option4 | "तंगस्टन तत्व का प्रतीक क्या है? W" | Chemistry: symbol for tungsten — straightforward science MCQ | IC |
| D33 | Malayalam, validation | Ex. 15 | option2 | "സർക്കസുകളിൽ തൊഴിൽ നിരോധിക്കണമെന്ന് ... ബച്ച്പൻ ബചാവോ ആന്ദോളൻ വേഴ്സസ് യൂണിയൻ ഓഫ് ഇന്ത്യ" | Child labour / constitutional law — Bachpan Bachao Andolan case | IO |
| D34 | Hindi, validation | Ex. 12 | option3 | "आमतौर पर लकड़ी के रेशों की लंबाई के साथ सूजन कितनी होती है: 0.1 से 0.8%" | Materials science MCQ — translated engineering content | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Strict MCQ format with single correct answer — structural alignment with deployment
- **Dimension(s):** IO, OO
- **Observation:** All sampled examples across all 11 language configs are uniformly formatted as single-correct-answer MCQs with exactly four options and a single target label. No reading-comprehension, multi-select, or open-ended items are present in the sample.
- **Deployment relevance:** The deployment requires strict MCQ evaluation with positive/negative marking where one answer is correct. MILU's format is a direct structural match to this requirement.
- **Datapoint citations:**
  - [D1] Hindi Ex. 1 (Hindi, split=validation, label=option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है:" — four options, single target, binary scoring ready.
  - [D6] Hindi Ex. 9 (Hindi, split=validation, label=option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें।" — grammar MCQ, same format, one correct answer.

#### Strength 2: Hindi Devanagari script — correct script and register
- **Dimension(s):** IF
- **Observation:** All Hindi-config items appear in fluent Devanagari script. The language register is formal standard Hindi (Khari Boli), with grammatically complete sentences and standard academic vocabulary. No script mixing or Roman transliteration is observed in the question stems (only in proper nouns and some technical terms).
- **Deployment relevance:** The deployment is text-only, Hindi-medium, Devanagari script. Script alignment is complete.
- **Datapoint citations:**
  - [D6] Hindi Ex. 9 (Hindi, split=validation, label=option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — formal academic Hindi grammar question in clean Devanagari.
  - [D7] Hindi Ex. 13 (Hindi, split=validation, label=option1): "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? अरबी भाषा" — Hindi GK question in standard written Hindi.

#### Strength 3: India-centric general knowledge content with some North Indian regional specificity
- **Dimension(s):** IC
- **Observation:** The Hindi sample includes questions with clear India-specific and North-India-specific content: a UP-minerals geography question, a Mughal history question, a constitutional law question, and an Indian freedom-fighter question. These reflect content broadly familiar to North Indian teachers from competitive-exam contexts.
- **Deployment relevance:** Teachers deploying the system in UP, MP, Rajasthan, and Bihar will encounter questions about subjects directly relevant to their syllabi and general knowledge background.
- **Datapoint citations:**
  - [D2] Hindi Ex. 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? अभ्रक" — UP-specific geographic knowledge directly relevant to North Indian state-board curriculum.
  - [D3] Hindi Ex. 25 (Hindi, split=validation, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" — Mughal history item aligning with North Indian history syllabus.
  - [D25] Hindi Ex. 19 (Hindi, split=validation, label=option3): "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? पाकिस्तान" — partition history, standard North Indian school and competitive-exam content.

#### Strength 4: Multiple subject domains present in Hindi sample — partial curricular breadth
- **Dimension(s):** IO
- **Observation:** The 26 Hindi validation examples span Engineering & Tech (6 items), Environmental Sciences (3), Arts & Humanities (4 — History, Literature, Language Studies, Arts & Culture), Law & Governance (1), Health & Medicine (1), Business Studies (3), and Science (4). This covers all 8 declared domains, providing evidence that domain breadth is not illusory for Hindi.
- **Deployment relevance:** The deployment requires coverage across all Hindi state and central board syllabi; MILU's multi-domain structure at least nominally addresses this, though the depth within each domain varies.
- **Datapoint citations:**
  - [D4] Hindi Ex. 6 (Hindi, split=validation, label=option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — Law & Governance domain present.
  - [D9] Hindi Ex. 17 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? संपत्ति कर" — Business Studies / Economics domain.
  - [D20] Hindi Ex. 2 (Hindi, split=validation, label=option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — Sports & Recreation / Social Sciences domain present.

#### Strength 5: Cross-language answer-key consistency visible in the data
- **Dimension(s):** OC
- **Observation:** A structurally identical question appears in both English (Ex. 1) and Hindi (Ex. 18) with the same correct answer (option3 in both), confirming consistent answer-key application across translations. The deployment user confirmed that competitive-exam answer keys are broadly compatible with North Indian teacher norms.
- **Deployment relevance:** Reduces concern about answer-key divergence between competitive-exam-sourced labels and North Indian board norms.
- **Datapoint citations:**
  - [D18] English Ex. 1 (English, split=validation, label=option3): "What was the immediate cause for loss of foreign reserves triggering the financial crisis in 1991? Sharp rise in value of imports of oil & petroleum products"
  - [D19] Hindi Ex. 18 (Hindi, split=validation, label=option3): "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था? तेल और पेट्रोलियम उत्पादों के आयात के मूल्य में तीव्र वृद्धि" — same item, same answer, consistent key.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: All reviewed Hindi validation examples are machine-translated (is_translated=True)
- **Dimension(s):** IC, IF
- **Observation:** Every single one of the 26 Hindi validation examples in the sample has `is_translated: True`. This is consistent across all items — no natively sourced Hindi item appears in the validation split sample. The benchmark paper states that only ~25% of total questions are translated, but this sample suggests that the validation split for Hindi may disproportionately (or entirely) consist of translated items. If true for the test split as well, the Hindi-language content would not reflect questions drawn from Hindi-language competitive exams but rather English-sourced content machine-translated by GPT-4O.
- **Deployment relevance:** This is critical because: (1) translated items may not reflect the register, phrasing conventions, and topic selection of actual Hindi-medium competitive-exam questions; (2) North Indian Hindi-medium teachers are being assessed on a model that was evaluated on items translated from English rather than native Hindi exam content; (3) subject-specific terminology choices in the translations may not align with state-board conventions.
- **Datapoint citations:**
  - [D28] Hindi Ex. 1 (Hindi, split=validation, label=option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" — is_translated=True; this is an engineering question where the Hindi text is a translation of an English-language technical question.
  - [D14] Hindi Ex. 4 (Hindi, split=validation, label=option2): "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। शेल" — is_translated=True; the answer option 'शेल' is a transliteration of 'shell' rather than a standard Hindi technical term.
  - [D15] Hindi Ex. 10 (Hindi, split=validation, label=option4): "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" — is_translated=True; 'नाइट्रेट' is a transliteration choice that may differ from Vaigyaanik evam Takniki Shabdavali Aayog standardized Hindi science terminology.

---

#### MAJOR

#### MAJOR Concern 1: No canonical Hindi-board literary content visible — competitive-exam GK register dominates Arts & Humanities
- **Dimension(s):** IC, IO
- **Observation:** The Arts & Humanities items in the Hindi sample do not include any questions about canonical Hindi-board literary figures (Tulsidas, Premchand, Kabir, Mahadevi Varma, etc.) or school-syllabus Hindi literature. The one Literature & Linguistics item is about William Wordsworth (an English poet). The History items are about Mughal texts and administrative history — consistent with a UPSC/SSC competitive-exam GK register rather than a school-literature register. No Hindi-medium literature, no doha analysis, no textual comprehension of Ramcharitmanas passages is observed.
- **Deployment relevance:** North Indian Hindi-medium teachers — and the students they evaluate — work with a school-board literature curriculum that foregrounds Hindi authors in a literary register (close reading, aesthetic appreciation) rather than a general-knowledge administrative register. MILU's competitive-exam sourcing produces a different kind of Arts & Humanities content than what a UP Board or CBSE Hindi teacher would encounter in their daily work.
- **Datapoint citations:**
  - [D5] Hindi Ex. 7 (Hindi, split=validation, label=option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" — Literature & Linguistics item asks about an English Romantic poet, not Hindi-board canonical literature.
  - [D3] Hindi Ex. 25 (Hindi, split=validation, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" — History item is administrative/courtly Mughal text authorship — UPSC GK register, not school-syllabus framing.
  - [D8] Hindi Ex. 22 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? अमृता शेरगिल" — Arts & Culture item is factual identification of artist, GK-style.

#### MAJOR Concern 2: Subject coverage in Hindi validation sample skews heavily toward Engineering & Tech, under-representing Civics/Political Science and Social Sciences
- **Dimension(s):** IO
- **Observation:** Of 26 Hindi validation examples, 6 are Engineering & Tech (23%), with only 1 Law & Governance item and no standalone Civics/Political Science or dedicated Social Sciences item (beyond 2 Sports items). Hindi-board curricula in UP, MP, Rajasthan, and Bihar place substantial emphasis on Civics, Panchayati Raj, and Social Sciences — subjects directly assessed in state board exams. The Engineering & Tech items (DC motors, transformers, rectifiers) are more characteristic of polytechnic or engineering entrance exams than school-board or general teacher deployment.
- **Deployment relevance:** If this imbalance persists in the test split, the benchmark may not adequately differentiate LLM performance on the civics and social science domains most relevant to the deployment's North Indian teacher population.
- **Datapoint citations:**
  - [D1] Hindi Ex. 1 (Hindi, split=validation, label=option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" — electrical engineering, likely not in UP Board secondary teacher's core domain.
  - [D13] Hindi Ex. 3 (Hindi, split=validation, label=option2): "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" — second engineering item in sample; both translated.
  - [D4] Hindi Ex. 6 (Hindi, split=validation, label=option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — only Law & Governance item; pertains to constitutional amendment, not Panchayati Raj or state-level civics.

#### MAJOR Concern 3: No sub-national state-board granularity verifiable from item content — potential under-representation of UP/Bihar/Rajasthan state-specific content
- **Dimension(s):** IC, IO
- **Observation:** Only one of the 26 Hindi examples explicitly names a North Indian state in its question (Ex. 26: UP minerals). No items about UP Panchayati Raj structure, Bihar Board history, Rajasthan state administrative geography, or MP-specific civics are visible. Items with state-specific content appear in other language configs (Telugu Ex. 25 mentions Madhya Pradesh; English Ex. 9 mentions Maharashtra), but the Hindi sample shows limited sub-national specificity for the primary Hindi-belt states.
- **Deployment relevance:** The deployment must serve teachers whose students are evaluated on state-board syllabi from UP, MP, Rajasthan, and Bihar specifically. If MILU's Hindi items are drawn primarily from pan-India competitive exams rather than state-level civil service exams, North Indian state-specific curricular content may be structurally absent.
- **Datapoint citations:**
  - [D2] Hindi Ex. 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — the only state-specific Hindi item in the sample, and it is a mineral geography question rather than civics or governance.
  - [D22] Telugu Ex. 25 (Telugu, split=validation, label=option1): "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? మొరెనా" — MP industrial geography appears in Telugu config, not in Hindi.
  - [D12] English Ex. 9 (English, split=validation, label=option2): "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" — state-specific governance in English config (Maharashtra), not Hindi-belt states.

#### MAJOR Concern 4: Translated Hindi items exhibit register and terminology choices not validated for state-board Hindi norms
- **Dimension(s):** IC, IF
- **Observation:** Translated Hindi items retain English technical terms as transliterations rather than using standardized Hindi or Vaigyaanik evam Takniki Shabdavali Aayog equivalents. Examples: 'शेल' (shell type transformer), 'नाइट्रेट' (nitrate), 'पल्सेटिंग डीसी' (pulsating DC), 'जंप लेबल' (jump label), 'स्ट्राइकथ्रू' (strikethrough), 'सुपरस्क्रिप्ट' (superscript). State board science textbooks in Hindi (particularly UP Board and CBSE Hindi medium) often use different terminological conventions — either fully Sanskritized or anglicized in different proportions. This creates a potential register mismatch between MILU's translated vocabulary and what North Indian teachers and students encounter in board textbooks.
- **Deployment relevance:** A teacher evaluating student answers in a Hindi-medium school context will have been trained on a specific terminological register. MILU's translated items may use vocabulary choices that diverge from that register, reducing the ecological validity of benchmark performance as a predictor of deployment performance.
- **Datapoint citations:**
  - [D14] Hindi Ex. 4 (Hindi, split=validation, label=option2): "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। शेल" — 'शेल' is a direct transliteration of 'shell'; standard Hindi technical texts might use 'कोश' or retain 'शेल' differently spelled.
  - [D23] Hindi Ex. 8 (Hindi, split=validation, label=option1): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है? एक जंप लेबल या फॉर्मेट लेबल" — 'जंप लेबल' and 'फॉर्मेट लेबल' are transliterations; CS items in Hindi textbooks vary in how they render these terms.
  - [D15] Hindi Ex. 10 (Hindi, split=validation, label=option4): "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" — 'नाइट्रेट' is transliterated; UP Board biology texts may use 'नाइट्रेट' or 'नत्रज लवण' depending on edition.

---

#### MINOR

#### MINOR Concern 1: One English-config item appears truncated or incomplete
- **Dimension(s):** IF
- **Observation:** English Ex. 11 reads: "The owner of the textile shop brought a" with options Calculator, Computer, Pencil, Fountain pen — the question stem appears incomplete, missing the context that would identify what the shop owner brought. The correct answer (Calculator) is unverifiable from the stem alone.
- **Deployment relevance:** An individual data quality issue; not indicative of a systemic problem given the documented filtering steps, but suggests noise remains in the dataset.
- **Datapoint citations:**
  - [D30] English Ex. 11 (English, split=validation, label=option2): "The owner of the textile shop brought a ... Calculator" — question stem appears to be cut off or missing context, making the correct answer unverifiable from the question alone.

#### MINOR Concern 2: Some items require very recent current-affairs knowledge (2022 sports results, 2020 awards) that may have finite shelf life
- **Dimension(s):** IC
- **Observation:** Several Hindi and non-Hindi items reference very recent events: India's 2022 Archery Asia Cup medals (Hindi Ex. 2), AAP forming government in Punjab in Feb-March 2022 (Bengali Ex. 5, Punjabi Ex. 5), 65th Filmfare Awards 2020 (Bengali Ex. 17, Kannada Ex. 17, Tamil Ex. 17). These items have definite correct answers but become increasingly anomalous as time passes.
- **Deployment relevance:** For a teacher using the system to evaluate students in 2025+, current-affairs items from 2022 may appear dated, and models trained on more recent data may give different performance profiles on these items than at benchmark creation time.
- **Datapoint citations:**
  - [D20] Hindi Ex. 2 (Hindi, split=validation, label=option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते? आठ" — 2022 sports result.
  - [D8] Hindi Ex. 22 (Hindi, split=validation, label=option4): "65वें फिल्मफेयर पुरस्कारों, 2020 में..." — referenced across multiple language configs as a parallel translated item.

#### MINOR Concern 3: Some items across language configs appear to be exact translations of the same English source, suggesting limited native-language diversity
- **Dimension(s):** IC
- **Observation:** The same questions (Bahamani Kingdom capital, Mediterranean climate characteristics, Qutub Minar, Fortran 77, cross-assembler, 1991 financial crisis) appear word-for-word translated across Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, and Telugu. This parallel structure confirms that a significant fraction of the benchmark is a multilingual translation of a shared English-language item pool, not independently sourced native-language questions.
- **Deployment relevance:** For Hindi specifically, this means items that appear to be Hindi-language MCQs may in fact test the model's ability to process translated English content rather than culturally and linguistically native Hindi knowledge — a moderate concern for a deployment aimed at Hindi-medium North Indian teachers whose students encounter native Hindi-register content.
- **Datapoint citations:**
  - [D11] English Ex. 3 (English, split=validation, label=option4): "What was the first capital of the Bahamani Kingdom? Gulbarga" — same question visible in Bengali Ex. 3, Gujarati Ex. 3, Hindi (implicitly), Malayalam Ex. 3, Punjabi Ex. 3.
  - [D24] Hindi Ex. 5 (Hindi, split=validation, label=option1): "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं: ... उत्तरी अमेरिका का अटलांटिक तट" — Mediterranean climate question appears translated across all 11 configs with identical structure.

---

### Content Coverage Summary

The Hindi-config validation sample (26 items) is entirely machine-translated (is_translated=True for all items reviewed), which is the most significant single observation from the data. Subject coverage spans all 8 declared domains, with a clear skew toward Engineering & Tech (23% of sample) and away from Civics/Political Science. The register is formal standard Hindi (Khari Boli) throughout, but technical vocabulary in translated items uses transliteration conventions (शेल, नाइट्रेट, जंप लेबल) that may not align with state-board Hindi textbook norms. Arts & Humanities items in the Hindi sample are in a competitive-exam GK register (factual identification, administrative history) rather than a school-literature register; no canonical Hindi literary figures (Tulsidas, Premchand, Kabir) appear in the sample. One UP-specific geography item provides the only sub-national Hindi-belt state-specific content visible.

Non-Hindi language configs (Bengali, Gujarati, Kannada, Marathi, etc.) also show nearly universal is_translated=True flags in the validation split, and many identical questions appear across all 11 languages, confirming that the validation split is heavily drawn from the translated English item pool. The English config contains genuinely India-centric questions including Maharashtra governance, Indian education policy (Yashpal Committee), and Indian railways history, all non-translated and well-formed. The Marathi config shows regionally specific Indian cultural content (Halsashti festival). Some items have a data quality issue (English Ex. 11 truncated question stem). Current-affairs items from 2020–2022 are present across multiple configs.

---

### Limitations

1. **Sample size per config:** Only 16–26 examples per language config were reviewed; subject-level coverage within each domain cannot be reliably assessed from this sample size. The test split may have a different is_translated distribution than the validation split.

2. **Validation-split translation bias:** The observation that all 26 Hindi validation items are translated may reflect deliberate design (translated items used for few-shot/validation purposes) or a split-level artifact. The test split — which is the primary evaluation set — may contain a higher proportion of natively sourced Hindi items. This cannot be determined from the available sample.

3. **Full subject-level statistics unavailable:** Supplementary Table 9 of the MILU paper (per-language, per-subject item counts) is not publicly accessible without the full PDF; the proportion of Hindi items by subject and whether specific Hindi-board subjects (Hindi Literature, UP History, Rajasthan Polity) are well-represented cannot be assessed from the sample.

4. **No test-split examples reviewed:** All examples are from the validation split. The test split (which would be the deployment evaluation set) was not sampled; its domain, subject, and is_translated distributions may differ.

5. **Annotation quality not directly assessable:** Whether individual answer keys are correct cannot be verified from the data alone without independent subject-matter expertise; the truncated English item (D30) is the only clear quality signal visible.

6. **Register variation within Hindi not assessable from script alone:** Whether MILU's formal Khari Boli register matches UP Board, MP Board, or CBSE Hindi-medium textbook norms requires comparison with those textbooks, which was not possible from the dataset sample.

