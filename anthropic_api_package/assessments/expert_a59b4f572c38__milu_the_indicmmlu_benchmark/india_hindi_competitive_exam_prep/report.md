## Deployment Context

**Use case:** Deployment scenario: A Hindi-speaking student in India is testing his/her preparation for competitive job-related examinations, with an AI system providing feedback on their responses. The goal is to evaluate the applicability of the benchmark and the quality of the LLM’s feedback.

Domain: Educational assessment
Setting: Mobile application / enterprise software

Note: The deployment hypothesis should be tested using Hindi-language sentences from the benchmark, as I am familiar with the language and can provide evaluation in a subsequent stage.
**Target population:** A graduate student in North India interacting in the Hindi language. The student has completed their education primarily in Hindi, with limited exposure to English.

# Validity Analysis: MILU
**Target context:** Hindi-Medium Competitive Exam Aspirants — North India (Central Exams)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 3 | Moderate gaps | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form | 2 | Significant gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content | 2 | Significant gaps | medium |
| Output Form ⚠ | 1 | Serious concern | high |
| **Average** | **1.7** | | |

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

MILU is a thoughtfully designed India-centric MCQ benchmark whose intent broadly aligns with the deployment's exam-aspirant target population, but its empirical fitness for evaluating a Hindi-language competitive-exam feedback system targeting North Indian central-exam aspirants is severely limited. Three categories of validity violation dominate: (1) Output-side mismatch — MILU evaluates only MCQ label accuracy via log-likelihood [Q53–Q55], while the deployment requires open-ended Hindi explanatory rationale; benchmark scores cannot validate the deployment's core output and no proxy exists in the wider ecosystem [WEB-9, WEB-10, WEB-11]. (2) Input content defects empirically confirmed by dataset analysis — ~15–20 of 245 sampled items are unanswerable due to stripped statement lists/passages [DATASET-CRITICAL1], 100% of validation samples are machine-translated (vs. paper's claimed 25%) [DATASET-MAJOR1, Q47], English vocabulary testing exceeds the deployment's 10% code-mixing ceiling [DATASET-MAJOR2], and Current Affairs items are temporally stale [DATASET-MAJOR4]. (3) Subject-distribution skew — overrepresentation of advanced Engineering/Technology and underrepresentation of Quantitative Aptitude [DATASET-MAJOR5] misaligns with central-exam priority subjects. The benchmark's strengths — India-first sourcing, multi-domain coverage, granular per-subject reporting, and acknowledged weakness in culturally-loaded domains — are real but insufficient to overcome the fundamental output-form mismatch and empirically confirmed input-content defects. A North Indian central-exam expert pool and a purpose-built Hindi explanation-quality rubric are required for valid deployment evaluation.

## Practical Guidance

### What This Benchmark Measures

MILU measures a model's accuracy at selecting correct MCQ options on Indian competitive-exam-style questions in 11 Indic languages including Hindi. For this deployment, it provides modest signal on the model's Hindi-language factual knowledge across India-centric subjects (Input Ontology score 3) and confirms documented model weakness in culturally-loaded domains [Q6, Q77] — useful directional evidence for the deployment's Hindi-medium UPSC/SSC/banking context.

### Construct Depth

Construct depth is shallow relative to deployment needs. The benchmark probes only one of two required output components (label correctness) and does so via scalar accuracy with no rationale assessment (Output Ontology and Output Form scores both 1). Empirical defects further limit interpretability: ~6–8% of sampled items are unanswerable [DATASET-CRITICAL1], the validation split is 100% machine-translated [DATASET-MAJOR1], and the subject mix overweights non-priority Engineering content [DATASET-MAJOR5]. High MILU accuracy cannot be assumed to predict deployment-grade Hindi feedback quality.

### What Else You Need

Three categories of supplementation are required: (1) A purpose-built Hindi explanation-quality evaluation protocol — adapt Pariksha's LA + TQ + Hallucination methodology [WEB-10] for the competitive-exam-rationale domain, with native Hindi-medium central-exam expert annotators (addresses OO and OF gaps). (2) A central-exam-syllabus-aligned MCQ subset — filter MILU Hindi to items mapped against UPSC/SSC/banking syllabi, exclude advanced Engineering content, supplement with Quantitative Aptitude items, and refresh Current Affairs with items <12 months old (addresses IO, IC, OC gaps). (3) A data-integrity audit pass to remove items with stripped statements/passages and to validate the actual translation rate in the test split (addresses IC and IF gaps from DATASET-CRITICAL1, CRITICAL2, MAJOR1).

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
MILU's taxonomy is India-centric and explicitly sourced from competitive exams [Q22, Q24], which broadly aligns with the deployment's central-exam priority subjects (GK, History, Polity, Reasoning). However, dataset analysis shows the Hindi validation sample is skewed toward advanced Engineering/Technology content (~18–20% of sampled items per MAJOR5) that is not tested in UPSC Prelims, SSC CGL, or banking exams, while Mathematics/Quantitative Aptitude — a top SSC/banking priority — is sparsely represented. The 41 subjects also coarsely aggregate ~20K fine-grained tags [Q39, Q42], making it hard to verify whether central-exam priority subjects are adequately covered versus state-level or unrelated regional exam content. The taxonomy was derived from competitive-exam scraping rather than UPSC/SSC syllabus mapping, and no published breakdown by exam type for the Hindi subset exists.

**Strengths:**
- Multi-domain India-centric taxonomy explicitly sourced from competitive exams aligned with deployment exam types [Q22, Q24]
- Coverage of culturally relevant subjects including local history, arts, festivals, and laws within the subject taxonomy [Q12, Q42]
- Hindi-specific items observed in dataset that align with central-exam Hindi grammar testing (e.g., indirect speech, active/passive voice) [DATASET-D23, DATASET-D24]

**Checklist:**

- **IO-1**: Deployment requires categories covering GK, Current Affairs, Indian Polity & Constitution, History, Mathematics/Quantitative Aptitude, Logical Reasoning, Hindi language proficiency, Geography, and Economics, scoped to UPSC/SSC/banking central exams [elicitation Q1].
- **IO-2**: MILU's 8-domain / 41-subject taxonomy includes Arts and Humanities, Social Sciences, Law and Governance, Science, etc. [Q42], which broadly maps to deployment priority subjects. However, Mathematics/Quantitative Aptitude as a discrete priority area is not explicitly called out and dataset analysis shows it is sparsely represented (DATASET-MAJOR5). Current Affairs is not a discrete subject category in MILU's taxonomy. — _Sources: Q42, DATASET-MAJOR5_
- **IO-3**: Dataset analysis reveals a notable concentration of advanced Engineering/Technology content (DC motors, half-wave rectifiers, transformers, AM modulation, TDM, choppers) that is not part of central-exam syllabi for UPSC/SSC/banking [DATASET-MAJOR5], introducing construct-irrelevant categories. — _Sources: DATASET-MAJOR5_
- **IO-4**: Critical content-validity gaps: (a) no published breakdown of Hindi item proportions by exam type (UPSC/SSC/banking vs. state PSC), (b) overrepresentation of advanced engineering content irrelevant to deployment, (c) underrepresentation of Quantitative Aptitude despite SSC/banking criticality [Q97, DATASET-MAJOR5]. — _Sources: Q97, DATASET-MAJOR5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge.' (p.3)
- [Q24] 'These questions were sourced following an approach similar to AGIEVAL...such as qualification tests and national and state-level civil services exams, among others.' (p.3)
- [Q42] 'Following the manual merging of related clusters, we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies.' (p.4)
- [Q39] 'Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap.' (p.4)

*Dataset analysis:*
- DATASET-MAJOR5: Sample shows ~18–20% Engineering/Technology items not tested in central exams; Quantitative Aptitude underrepresented
- DATASET-D23: Hindi grammar items relevant to deployment (indirect speech)
- DATASET-D24: Hindi active/passive voice item — aligned with deployment

</details>

**Information gaps:**
- No published breakdown of MILU Hindi item proportions across UPSC/SSC/banking vs. state PSC exam types
- No documentation on whether Current Affairs is treated as a discrete category or distributed across subjects
- Coarse 41-subject aggregation obscures granularity needed to verify central-exam coverage

**Requires expert verification:**
- Whether observed engineering content overrepresentation generalizes beyond the validation split sample to the full Hindi release
- Mapping of MILU subjects to UPSC/SSC syllabus topics by a central-exam subject expert

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Input content is the deployment's HIGH-priority dimension and shows severe, empirically confirmed validity violations. Dataset analysis reveals two critical defects: (1) systematic missing content in translated items — approximately 15–20 of 245 sampled items reference 'the following statements/items/sentences' that are entirely absent from the question text [DATASET-CRITICAL1], rendering them unanswerable from presented content; and (2) 100% of the sampled validation split is machine-translated [DATASET-MAJOR1], contradicting the documented 25% translation rate [Q47] and exposing few-shot evaluation to exclusively translated exemplars. Additional MAJOR concerns include English vocabulary testing (Didactic, grim, Evangelize) within Hindi Language Studies items [DATASET-MAJOR2], which exceeds the deployment's ~10% code-mixing ceiling and introduces construct-irrelevant difficulty for Hindi-medium aspirants. The deployment's North India sub-regional content (Chhath Puja, zamindari, tehsil/mandal) is partially present (e.g., UP chikankari, UP minerals, Rajasthan geography) but unverified at distribution level. These defects collectively make the Hindi item pool unreliable for the deployment's target population.

**Strengths:**
- Some genuine North India sub-regional content present (UP chikankari craft, UP minerals, Rajasthan geography/Kota painting) [DATASET-D28, D29, D30, D31, D32]
- India-first sourcing design with 1,500+ competitive exams and emphasis on regional state exams [Q11, Q13, Q14, Q28]
- Native Hindi grammar items (indirect speech, voice) present and deployment-relevant [DATASET-D23, D24]

**Checklist:**

- **IC-1**: Deployment requires items grounded in pan-India GK plus North India sub-regional content (Chhath Puja, Mughal/medieval North Indian history, zamindari, tehsil/mandal admin units) [elicitation Q2]. Dataset shows partial UP/Rajasthan coverage [DATASET-D28, D29, D30, D31, D32] but also South Indian and Chhattisgarh-specific items [DATASET-D37, D38] whose central-exam relevance is mixed. — _Sources: Q14, DATASET-D28, DATASET-D29, DATASET-D30, DATASET-D31, DATASET-D37, DATASET-D38_
- **IC-2**: Cultural alignment is partial. North India sub-regional examples appear, but the validation sample's 100% translation rate [DATASET-D1, MAJOR1] and English-vocabulary testing within Language Studies [DATASET-D20, D21, D22] indicate substantial deviation from the deployment's Hindi-medium register and ~10% code-mixing ceiling [elicitation Q4]. — _Sources: DATASET-D1, DATASET-D20, DATASET-D21, DATASET-D22_
- **IC-3**: Several items require Western/English-medium knowledge inappropriate for the target Hindi-medium graduate cohort: English literary vocabulary (Didactic, grim, Evangelize) [DATASET-D20, D21, D22], English poet Wordsworth [DATASET-D19], and Roman-alphabet letter sequences in reasoning items [DATASET-D36]. — _Sources: DATASET-D19, DATASET-D20, DATASET-D21, DATASET-D22, DATASET-D36_
- **IC-4**: INSUFFICIENT DOCUMENTATION — annotator demographics are not reported [Q26, Q87]; the paper acknowledges only AI4Bharat volunteer audits, with no breakdown of regional background, Hindi register expertise, or familiarity with North Indian central-exam curricula.
- **IC-5**: Severe content-validity issues documented: (a) systematic missing referents in translated items rendering ~6–8% of sampled items unanswerable [DATASET-CRITICAL1]; (b) 100% machine-translation rate in validation split contradicting paper's 25% claim [DATASET-MAJOR1 vs. Q47]; (c) English vocabulary testing exceeds deployment code-mixing ceiling [DATASET-MAJOR2]; (d) temporally dated Current Affairs items (2018–2022) [DATASET-MAJOR4]. — _Sources: DATASET-CRITICAL1, DATASET-MAJOR1, DATASET-MAJOR2, DATASET-MAJOR4, Q47, WEB-12_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q11] 'We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams.' (p.2)
- [Q14] 'We focus on region-specific exams to authentically capture local knowledge in the respective language.' (p.2)
- [Q44] 'For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O.' (p.4)
- [Q47] 'Of the total 79K questions, only 25% of questions are translated from English, with the remainder' (p.4)

*Web sources:*
- [WEB-12] arXiv 2501.13912 notes most Indic evaluation datasets are translated from English, limiting socio-cultural and domain-specific nuance — consistent with observed translation defects

*Dataset analysis:*
- DATASET-CRITICAL1 (D2–D18): ~15–20 items reference statements/items/sentences absent from question text, rendering items unanswerable
- DATASET-MAJOR1 (D1): 100% of 245 validation samples have is_translated=True, contradicting paper's 25% claim
- DATASET-MAJOR2 (D20, D21, D22, D36): English vocabulary (Didactic, grim, Evangelize) and Roman-alphabet sequences tested in Hindi items
- DATASET-D28, D29, D30, D31, D32: North India sub-regional content present (UP chikankari, UP minerals, Rajasthan geography, Kota painting, Lucknow literature)
- DATASET-D37, D38: South Indian (Pandya dynasty) and Chhattisgarh-specific items of questionable central-exam relevance
- DATASET-MAJOR4: Temporally dated Current Affairs items (2018–2022 GDP, 2019 Ryugu, 2022 sports)

</details>

**Information gaps:**
- Whether the 100% translation rate observed in validation generalizes to the full Hindi release or is split-specific
- Distribution of MILU Hindi items across North Indian states (UP/Bihar/Rajasthan/MP) vs. other regions
- Quantitative rate of English code-mixing across the full Hindi item pool
- Annotator demographic breakdown and Hindi register expertise

**Requires expert verification:**
- North Indian central-exam expert review of Hindi item distribution against UPSC/SSC syllabus and ~10% code-mixing ceiling
- Verification of whether systematic-missing-content defect occurs at the same rate in the test split as in validation

---

### Input Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Input form alignment is partially good but undermined by systematic data-integrity defects. The deployment is text-only Hindi in Devanagari, matching MILU's text-based MCQ format with INDICLID and Unicode filtering [Q33, Q34]. However, dataset analysis reveals two form-level corruption patterns: (1) tables, code blocks, statement enumerations, and source passages were stripped during scraping/processing, leaving questions that reference content not present [DATASET-CRITICAL1]; and (2) at least one item has a meta-instruction ('Select the correct answer using the code given below') as an answer option [DATASET-CRITICAL2], indicating systematic format corruption affecting precisely the UPSC-Prelims-style 'which of the following statements' items most representative of the deployment task. While the documented form (text MCQ, four options, Devanagari) matches deployment needs, the as-shipped form for many items is broken. IF was rated LOWER priority in elicitation, but the empirical defects elevate concern.

**Strengths:**
- Text-only MCQ format with up to four options matches deployment text-only Hindi interface [Q33]
- INDICLID and Unicode-based filtering enforces correct script (Devanagari for Hindi) [Q34]
- Duplicate removal and multiple manual/automated cleaning layers applied [Q31, Q35, Q36]
- Devanagari is a high-resource Unicode-standard script with no RTL/capitalization issues [WEB-3 region context]

**Checklist:**

- **IF-1**: Documented signal distribution (text MCQ in Devanagari, four options) aligns with deployment [Q33, Q34]. However, empirical data shows form corruption: stripped tables, missing statement lists, and meta-instruction options [DATASET-CRITICAL1, CRITICAL2]. — _Sources: Q33, Q34, DATASET-CRITICAL1_
- **IF-2**: Regional infrastructure supports text in Devanagari Unicode; mobile/Android dominant [region context]. No infrastructure mismatch.
- **IF-3**: UPSC Prelims and SSC CGL frequently use 'which of the following statements is correct' with code tables; this exact item type is the most likely to be corrupted by table-stripping in MILU [DATASET-CRITICAL2], creating a domain-specific form risk for the deployment. — _Sources: DATASET-CRITICAL2_
- **IF-4**: Form mismatches: (a) systematic stripping of referenced content during dataset processing renders ~6–8% of sampled items unanswerable [DATASET-CRITICAL1]; (b) format corruption affects competitive-exam-representative item types [DATASET-CRITICAL2]. — _Sources: DATASET-CRITICAL1, DATASET-CRITICAL2_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'During the collection process, we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q34] 'To remove incorrect language entries, we utilize a combination of INDICLID...and Unicode-based filtering...ensuring that the questions are in the correct language.' (p.4)
- [Q31] 'To address potential noise in the questions, we employ multiple layers of manual and automated cleaning filters.' (p.4)

*Dataset analysis:*
- DATASET-CRITICAL1: Systematic stripping of statement lists, code tables, and source passages during data processing
- DATASET-CRITICAL2 (D9): Meta-instruction appearing as answer option indicates table-stripping corruption
- DATASET-D2 through D18: 15+ examples demonstrating form corruption

</details>

**Information gaps:**
- Rate of form-corruption defects in the test split vs. validation split
- Whether MILU's release pipeline included a final human pass for table/statement-list integrity

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
OO is a HIGH-priority dimension and represents a fundamental mismatch. MILU's output ontology is a closed four-option MCQ with a single correct answer scored by accuracy [Q22, Q55]. The deployment requires both a correct/incorrect verdict AND a substantive Hindi-language explanation of why the answer is right or wrong [elicitation Q3]. There is no provision in MILU's output space for explanatory rationale — dataset analysis confirms zero rationale fields across all 245 sampled items [DATASET-MAJOR3]. Additionally, the paper documents that models perform worst in Arts & Humanities, Social Sciences, and Law & Governance [Q20, Q71], which are precisely the culturally-loaded domains central to UPSC GS prep — meaning even the MCQ-label scoring captures the wrong slice of the deployment's quality space. The benchmark's output taxonomy cannot validate the deployment's core output type.

**Strengths:**
- Closed-set MCQ scoring is unambiguous and supports the binary correct/incorrect component of deployment feedback [Q55]
- Granular per-subject, per-language accuracy reporting (Tables 11–54) enables Hindi-domain isolation [Q99–Q132]
- Documentation explicitly acknowledges weakness in culturally-loaded domains as a known limitation [Q6, Q77]

**Checklist:**

- **OO-1**: Output categories are restricted to one of four MCQ options [Q55]. The deployment requires (a) correct/incorrect label PLUS (b) Hindi-language explanatory rationale [elicitation Q3]. The benchmark covers (a) but provides no taxonomy or scoring for (b). — _Sources: Q22, Q55, DATASET-MAJOR3_
- **OO-2**: Critical missing categories: (1) explanatory rationale quality (factual accuracy, fluency, pedagogical clarity, register appropriateness); (2) Hindi register conformity (Manak Hindi vs. Sanskritized vs. heavily code-mixed); (3) deployment-specific feedback dimensions specified in pedagogical_context. — _Sources: DATASET-MAJOR3, WEB-10_
- **OO-3**: MCQ-label-only ontology encodes the assumption that benchmark performance is fully captured by accuracy on closed-set selection — an assumption that does not hold for the deployment's open-ended explanation-generation task. — _Sources: Q55_
- **OO-4**: Substantial taxonomy redesign would be needed: a Hindi explanation-quality rubric (e.g., adapted from Pariksha's LA + TQ + Hallucination dimensions [WEB-10]) does not exist within MILU and must be supplemented externally. — _Sources: WEB-9, WEB-10, WEB-11_
- **OO-5**: Structural validity is violated because the construct (deployment-grade Hindi feedback) has a richer structure than the benchmark's scalar MCQ accuracy can represent. Content validity is violated by missing explanation-quality categories. External validity is violated because high MILU accuracy may not predict high deployment quality. — _Sources: Q6, Q77, DATASET-MAJOR3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs)...' (p.3)
- [Q55] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability...' (p.5)
- [Q6] 'Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM.' (p.1)
- [Q77] '...the domain-specific analysis indicates that models perform better in general fields such as STEM while facing challenges in culturally relevant subjects like Arts, Humanities, and Law...' (p.8)

*Web sources:*
- [WEB-10] Pariksha (arXiv 2406.15053) — Hindi output evaluation methodology (LA + TQ + Hallucination) is closest analog to needed explanation-quality rubric
- [WEB-9] IndicGenBench covers Hindi generation but not exam rationale quality
- [WEB-11] MT-Bench-Hi covers conversational Hindi but not exam explanation

*Dataset analysis:*
- DATASET-MAJOR3: All 245 sampled items have only target field; zero rationale or explanation annotations
- DATASET-D34: Complex UPSC-style ethics scenario has no rationale despite requiring nuanced reasoning

</details>

**Requires expert verification:**
- Construction of a Hindi explanation-quality rubric requires native-speaker pedagogical expertise

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
Ground-truth labels for MCQ correctness derive from original exam portals where subject experts ensure answer accuracy [Q26], which is reasonable label provenance for objective MCQs. However, OC has multiple validity concerns for the target deployment: (1) annotator demographics are entirely unreported [Q26, Q87] — no breakdown by region, Hindi register expertise, or central-exam familiarity; (2) the institutional concentration at IIT Madras (Chennai) creates potential geographic asymmetry relative to North Indian Hindi-belt deployment; (3) 25% of released questions are GPT-4O-translated [Q47] with no human verification of translated label correctness; (4) the validation split shows 100% translation [DATASET-MAJOR1], amplifying label-provenance concerns; (5) Current Affairs items dated 2018–2022 [DATASET-MAJOR4] have stale ground truth for a 2025–2026 exam-prep deployment; (6) MCQ correctness labels do not address the deployment's primary output (Hindi explanation), so OC is silent on the deployment's most important quality construct.

**Strengths:**
- Original exam portals provide subject-expert-verified answer keys, giving objective ground truth for the MCQ label component [Q26]
- Multiple manual audit layers by AI4Bharat volunteers [Q87]
- Manual cluster review for subject labeling [Q41]

**Checklist:**

- **OC-1**: Label correctness for objective MCQs is reasonable since drawn from official exam answer keys [Q26]. However, no Hindi-medium central-exam stakeholder review is documented, and translated items lack any human label verification. — _Sources: Q26_
- **OC-2**: Potential disagreement risk: GPT-4O-translated items [Q44, Q47] may not preserve the precise terminology North Indian Hindi-medium aspirants expect; institutional concentration at IIT Madras is documented [Q10] but regional review is not. — _Sources: Q10, Q44, Q47_
- **OC-3**: INSUFFICIENT DOCUMENTATION — paper provides no annotator demographic breakdown (region, language proficiency, central-exam familiarity); only 'AI4Bharat team volunteers' for manual audits [Q87].
- **OC-4**: Re-annotation by a North Indian Hindi-medium central-exam expert pool is recommended but not currently in scope of MILU.
- **OC-5**: Cluster-level label assignment via K-means + manual review [Q40, Q41] may erase fine-grained subject distinctions important for central-exam preparation; aggregation of 20K tags into 41 subjects [Q39, Q42] obscures Hindi-specific subtopics. — _Sources: Q39, Q40, Q41, Q42_
- **OC-6**: Critical OC issues: (a) 25% translated content lacks human label verification [Q47]; (b) annotator demographics undocumented; (c) Current Affairs labels are temporally stale [DATASET-MAJOR4]; (d) no labels at all for the deployment's open-ended explanation output [DATASET-MAJOR3]. — _Sources: Q47, DATASET-MAJOR4, DATASET-MAJOR3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q26] 'These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers.' (p.3)
- [Q87] 'We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits.' (p.9)
- [Q10] 'Nilekani Centre at AI4Bharat, Indian Institute of Technology, Madras, IBM Research, India' (p.1)
- [Q47] 'Of the total 79K questions, only 25% of questions are translated from English, with the remainder' (p.4)

*Dataset analysis:*
- DATASET-MAJOR4 (D25, D26, D27): Temporally dated Current Affairs labels (2018–2022) stale for 2025–2026 deployment
- DATASET-MAJOR1 (D1): 100% translation in validation split amplifies label-provenance concern
- DATASET-MAJOR3: Zero rationale annotations across sample

</details>

**Information gaps:**
- Annotator regional demographics and Hindi register expertise
- Whether translated items underwent any human verification of label correctness
- Currency policy for Current Affairs items (refresh cadence)

**Requires expert verification:**
- North Indian central-exam expert review of label correctness for a sample of Hindi items, especially translated ones
- Native-Hindi-speaker review for register-appropriate terminology

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
OF is a HIGH-priority dimension with a fundamental mismatch. MILU evaluates models via accuracy under log-likelihood scoring (non-API) or structured JSON generation (API) [Q52–Q57], producing a single scalar accuracy per subject/language/shot configuration [Q100]. The deployment requires open-ended Hindi-language explanatory text generation [elicitation Q3]. Dataset analysis confirms zero infrastructure for evaluating generation quality [DATASET-MAJOR3]. The paper itself acknowledges that log-likelihood scoring 'may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting' [Q85]. No Hindi competitive-exam explanation-quality benchmark exists in the broader ecosystem [WEB-9, WEB-10, WEB-11, WEB-12], confirming this is a genuine evaluation gap. Benchmark scores cannot validate the deployment's core output form.

**Strengths:**
- Reproducible scoring via LM-EVALUATION-HARNESS [Q52]
- Multiple shot configurations (0/1/5-shot) reported per model [Q50, Q100]
- Granular per-model, per-subject, per-language accuracy tables enable detailed Hindi-domain analysis [Q99–Q132]

**Checklist:**

- **OF-1**: Expected output modality (MCQ label) does not match deployment requirement (Hindi explanatory text + label) [elicitation Q3, Q53–Q55]. Fundamental mismatch. — _Sources: Q53, Q55, DATASET-MAJOR3_
- **OF-2**: Not applicable — deployment is text-only; no TTS requirement.
- **OF-3**: Target population is graduate-level (near-universal literacy within cohort) and Hindi-literate in Devanagari; literacy is not a barrier. However, output form must be Manak Hindi text rather than English/Sanskritized register, which MILU does not evaluate.
- **OF-4**: Critical form mismatch: scalar accuracy on closed-set MCQ selection cannot proxy for open-ended Hindi text generation quality [Q85, DATASET-MAJOR3]. The ecosystem lacks any purpose-built Hindi exam-explanation benchmark [WEB-9, WEB-10, WEB-11, WEB-12]. — _Sources: Q85, WEB-9, WEB-10, WEB-11, WEB-12, DATASET-MAJOR3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q52] 'For non-API-based models, we use the LM-EVALUATION-HARNESS to ensure clean and reproducible evaluations.' (p.5)
- [Q53] 'We use the log-likelihood method, where the probability of a given output string is computed by conditioning it on some provided input...' (p.5)
- [Q55] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability...' (p.5)
- [Q85] 'Finally, our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting.' (p.9)

*Web sources:*
- [WEB-9] IndicGenBench covers Hindi generation tasks but not exam-explanation quality
- [WEB-10] Pariksha evaluates Hindi LA + TQ + Hallucination but for health/finance/culture, not exam rationale
- [WEB-11] MT-Bench-Hi covers conversational Hindi instruction-tuning, not exam explanation
- [WEB-12] arXiv 2501.13912 — most Hindi evaluation datasets are translated, lacking domain-specific socio-cultural grounding

*Dataset analysis:*
- DATASET-MAJOR3: Zero rationale or explanation annotations across all 245 sampled items

</details>

**Requires expert verification:**
- Design of a deployment-specific Hindi explanation-quality evaluation protocol (e.g., adapting Pariksha's LA/TQ/Hallucination methodology)

---

## Remediation Suggestions

### Output Form ⚠

**Gap:** MILU evaluates MCQ label accuracy only; deployment requires open-ended Hindi rationale generation, with no proxy in the benchmark.

**Recommendation:** Build a deployment-specific Hindi explanation-quality evaluation harness adapting Pariksha's Linguistic Acceptability + Task Quality + Hallucination dimensions [WEB-10], with native Hindi-medium central-exam expert annotators rating sampled model rationales on factual accuracy, Hindi fluency in Manak Hindi register, pedagogical clarity, and ≤10% English code-mixing.

### Input Content ⚠

**Gap:** Systematic missing referents in ~6–8% of sampled items render them unanswerable [DATASET-CRITICAL1], and 100% of validation samples are machine-translated [DATASET-MAJOR1] vs. paper's 25% claim.

**Recommendation:** Run a data-integrity audit on the full Hindi release to flag and exclude items where 'the following statements/items/sentences' are referenced but absent; report actual translation rate per split; restrict few-shot exemplars to natively sourced Hindi items only.

### Input Content ⚠

**Gap:** English vocabulary testing (Didactic, grim, Evangelize) within Hindi Language Studies items exceeds the deployment's ~10% code-mixing ceiling and creates construct-irrelevant difficulty for Hindi-medium aspirants [DATASET-MAJOR2].

**Recommendation:** Filter Hindi Language Studies items to remove those whose core construct is English vocabulary recognition; retain only items testing Hindi grammar, idiom, comprehension, and vocabulary.

### Input Form

**Gap:** Table/code/statement-list stripping during scraping has corrupted UPSC-Prelims-style items most representative of the deployment task [DATASET-CRITICAL2].

**Recommendation:** Re-scrape or repair items where source content (numbered statements, code tables, source passages) has been stripped; flag and exclude items with meta-instruction options like 'Select the correct answer using the code given below' until repaired.

### Input Ontology

**Gap:** Subject distribution skews toward advanced Engineering/Technology content not tested in central exams while underrepresenting Quantitative Aptitude [DATASET-MAJOR5]; no published breakdown by exam type for the Hindi subset.

**Recommendation:** Construct a central-exam-aligned subset by mapping MILU's 41 subjects against published UPSC/SSC/IBPS syllabi [WEB-8]; exclude advanced engineering items irrelevant to deployment; supplement with externally sourced Quantitative Aptitude items in Hindi.

### Output Content

**Gap:** Current Affairs labels reflect 2018–2022 events [DATASET-MAJOR4], temporally stale for 2025–2026 exam preparation; annotator demographics not documented.

**Recommendation:** Establish a refresh policy for Current Affairs items (rolling 12–18 month window); recruit a North Indian Hindi-medium central-exam expert annotator pool to re-verify a sample of translated items and to document demographic composition.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge." |
| Q2 | 1 | input_content | "With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science." |
| Q3 | 1 | output_form | "We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q4 | 1 | output_form | "Open multilingual models outperform language-specific fine-tuned models, which perform only slightly better than random baselines." |
| Q5 | 1 | output_form | "Models also perform better in high-resource languages as compared to low-resource ones." |
| Q6 | 1 | output_ontology | "Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM." |
| Q7 | 1 | input_ontology | "To the best of our knowledge, MILU is the first of its kind benchmark focused on Indic languages, serving as a crucial step towards comprehensive cultural evaluation." |
| Q8 | 1 | output_content | "All code, benchmarks, and artifacts will be made publicly available to foster open research." |
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
| Q21 | 2 | output_content | "All the artifacts will be released publicly." |
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
| Q37 | 4 | input_form | "Upon examination, we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information." |
| Q38 | 4 | input_form | "To address this issue, we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question." |
| Q39 | 4 | output_ontology | "Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap." |
| Q40 | 4 | input_form | "To organize them, we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters." |
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
| Q72 | 7 | output_ontology | "This suggests that the training corpora for these models lack sufficient culturally specific data. Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages." |
| Q73 | 7 | output_form | "As most Indic LLMs are built on English base models like LLAMA-2-7B, we assess the impact of language adaptation on their performance. Table 5 compares language-specific models with the original LLAMA-2-7B, and instruction-tuned models with LLAMA-2-7B-CHAT. Our findings show minimal gains, with some models even underperforming post-adaptation." |
| Q74 | 8 | input_ontology | "In this paper, we introduced MILU—Multilingual Indic Language Understanding Benchmark-a comprehensive benchmark specifically designed to evaluate LLMs across 11 Indic languages, spanning diverse domains and culturally relevant subjects." |
| Q75 | 8 | output_form | "We evaluate 45 different LLMs and find that the majority of LLMs struggle on MILU, with GPT4o achieving the highest average accuracy." |
| Q76 | 8 | output_form | "The analysis also shows that models perform significantly better in high-resource languages than low-resource ones, highlighting the need for more robust multilingual strategies." |
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
| WEB-1 | https://theprint.in/india/family-support-safety-study-material-a-click-away-whats-driving-more-women-to-take-upsc-exam/1922660/ |
| WEB-2 | https://sleepyclasses.com/discover-how-many-candidates-are-selected-in-upsc-each-year/ |
| WEB-3 | https://en.wikipedia.org/wiki/List_of_Indian_states_and_union_territories_by_literacy_rate |
| WEB-4 | https://www.findeasy.in/indian-states-by-literacy-rate/ |
| WEB-5 | https://www.iamai.in/sites/default/files/research/Kantar_%20IAMAI%20report_2024_.pdf |
| WEB-6 | https://en.wikipedia.org/wiki/Internet_in_India |
| WEB-7 | https://www.pw.live/upsc/exams/how-many-candidates-applied-for-upsc-2024 |
| WEB-8 | https://upsc.gov.in/ |
| WEB-9 | https://arxiv.org/abs/2404.16816 |
| WEB-10 | https://arxiv.org/html/2406.15053v1 |
| WEB-11 | https://arxiv.org/abs/2508.19831 |
| WEB-12 | https://arxiv.org/html/2501.13912v1 |
| WEB-13 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-14 | https://www.ey.com/en_in/insights/cybersecurity/decoding-the-digital-personal-data-protection-act-2023 |
| WEB-15 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-16 | https://www.lexology.com/library/detail.aspx?g=47dda3b5-1111-4b6b-9f87-799ef8066802 |
| WEB-17 | https://negd.gov.in/press_release/meity-unveils-india-ai-governance-guidelines-under-indiaai-mission-to-ensure-safe-inclusive-and-responsible-adoption-of-artificial-intelligence-across-sectors/ |
| WEB-18 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2234853&reg=3&lang=1 |
| WEB-19 | https://www.scconline.com/blog/post/2025/11/06/meity-launches-india-ai-governance-guidelines-under-indiaai-mission-2025/ |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Hindi configuration)
**Analysis date:** 2025-01-31
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Dimension |
|----|---------|-----------|-------|---------|-----------|
| D1 | MILU/Hindi | All 245 | is_translated=True | Every single example in the 245-item sample has `is_translated: True` | IC |
| D2 | MILU/Hindi | Ex.69 | option2 (Chemistry) | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल / (b) केवल / (c) केवल" — options reference unlisted items (a)(b)(c) | IC/IF |
| D3 | MILU/Hindi | Ex.86 | option2 (Sociology) | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, C और E / केवल A, B, D और E" — options reference state list not present in question | IC/IF |
| D4 | MILU/Hindi | Ex.56 | option2 (Chemistry) | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें... (1) और (2) केवल" — numbered statements absent from question text | IC/IF |
| D5 | MILU/Hindi | Ex.94 | option4 (Chemistry) | "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? केवल a, d / केवल b, c" — lettered reactions not shown | IC/IF |
| D6 | MILU/Hindi | Ex.95 | option1 (Sports) | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं" — sentences B-F completely absent | IC/IF |
| D7 | MILU/Hindi | Ex.106 | option2 (Chemistry) | "निम्नलिखित पदार्थों को...कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4 / 4 2 3 1" — numbered substances not named in question | IC/IF |
| D8 | MILU/Hindi | Ex.110 | option4 (Agriculture) | "राष्ट्रीय खाद्य सुरक्षा मिशन... (a) राष्ट्रीय खाद्य सुरक्षा मिशन एक फसल विकास योजना है। (b)..." — this item actually includes statements, appears intact | IF |
| D9 | MILU/Hindi | Ex.135 | option3 (Politics) | Option 4 reads "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें" — option4 is a meta-instruction, not an answer | IF |
| D10 | MILU/Hindi | Ex.137 | option4 (Politics) | "ग्राम सभा क्या है: (ख) और (ग) केवल / (ग) और (घ) केवल" — options reference lettered list absent from question | IC/IF |
| D11 | MILU/Hindi | Ex.118 | option2 (Language) | "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें" — no idiom/मुहावरा is given in the question text | IC/IF |
| D12 | MILU/Hindi | Ex.152 | option1 (Language) | "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए सबसे उपयुक्त विकल्प चुनें" — no sentence or underlined portion present | IC/IF |
| D13 | MILU/Hindi | Ex.151 | option1 (Economics) | "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं... कौन सा तर्क मजबूत है?" — statement and arguments completely missing | IC/IF |
| D14 | MILU/Hindi | Ex.143 | option4 (Logical Reasoning) | "निम्नलिखित शब्दों को तार्किक और अर्थपूर्ण क्रम में व्यवस्थित करें: 3,1,5,2,4 / 5,2,3,1,4" — words to order are absent | IC/IF |
| D15 | MILU/Hindi | Ex.145 | option2 (Logical Reasoning) | "कौन सा अक्षर समूह प्रश्न चिह्न (?) को बदलकर दी गई श्रृंखला को पूरा करेगा?" — no series is provided | IC/IF |
| D16 | MILU/Hindi | Ex.188 | option3 (Education) | "नई शिक्षा नीति 2020 में देखा गया है कि... निम्नलिखित में से किन समस्याओं का सामना कर रही है? केवल (a) / केवल (b) / उपरोक्त सभी" — problems (a)(b) not listed | IC/IF |
| D17 | MILU/Hindi | Ex.201 | option4 (Computer Science) | "निम्नलिखित में से कौन सा कथन BIOS के संदर्भ में सही है? केवल I और II / केवल I और III / सभी कथन सही हैं" — statements I, II, III absent | IC/IF |
| D18 | MILU/Hindi | Ex.222 | option2 (Business) | "2022 में फॉर्च्यून 500 सूची में भारतीय कंपनियों के संबंध में निम्नलिखित पर विचार करें: A, B, C और D केवल" — items A-E not enumerated | IC/IF |
| D19 | MILU/Hindi | Ex.7 | option2 (Literature) | "विलियम वर्ड्सवर्थ _________ के कवि हैं" — tests knowledge of English poet; India-relevance absent | IC |
| D20 | MILU/Hindi | Ex.76 | option2 (Language) | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" — English word 'Didactic' asked in Hindi; tests English vocabulary | IC |
| D21 | MILU/Hindi | Ex.90 | option3 (Language) | "शब्द 'grim' का पर्यायवाची लिखें" — English word 'grim' asked in Hindi question | IC |
| D22 | MILU/Hindi | Ex.105 | option4 (Language) | "निर्देश: निम्नलिखित प्रश्न में... शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है... Evangelize" — English word tested in Hindi | IC |
| D23 | MILU/Hindi | Ex.9 | option3 (Language Studies) | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा..." — tests Hindi grammar (indirect speech) directly relevant to deployment | IC/IO |
| D24 | MILU/Hindi | Ex.51 | option2 (Language Studies) | "दिए गए वाक्य का सही सक्रिय रूप चुनें" — active/passive voice in Hindi | IO |
| D25 | MILU/Hindi | Ex.74 | option4 (Economics) | "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी? 7.1 प्रतिशत" — specific historical data point (2018) | OC |
| D26 | MILU/Hindi | Ex.2 | option2 (Sports) | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" | OC |
| D27 | MILU/Hindi | Ex.88 | option1 (Physics) | "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान एक क्षुद्रग्रह पर उतरा... रयुगु" | OC |
| D28 | MILU/Hindi | Ex.242 | option4 (Arts) | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है... चिकनकारी" — UP-specific cultural craft content | IC |
| D29 | MILU/Hindi | Ex.26 | option2 (Earth Sciences) | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — UP-specific geography content | IC |
| D30 | MILU/Hindi | Ex.68 | option2 (Geography) | "राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है?" — Rajasthan state-level content | IC |
| D31 | MILU/Hindi | Ex.193 | option3 (Arts) | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" — Rajasthan state-level cultural content | IC |
| D32 | MILU/Hindi | Ex.115 | option4 (Literature) | "'किस्सा किस्सा लखनऊवा-लखनऊ के आवामी किस्से' के लिए साहित्य अकादमी युवा पुरस्कार 2021" — UP/Lucknow literary content | IC |
| D33 | MILU/Hindi | Ex.28 | option2 (Sociology) | "खेरवार आंदोलन के नेता — भागीरथ मांझी" — Jharkhand/tribal movement, less central-exam prominent | IC |
| D34 | MILU/Hindi | Ex.83 | option1 (Sociology) | Complex ethics scenario about senior civil officer, tribal displacement, old-age home; very long UPSC-style case | IO |
| D35 | MILU/Hindi | Ex.170 | option2 (Business) | "कपड़ा दुकान के मालिक ने क्या खरीदा? कैलकुलेटर" — decontextualized; passage/context missing | IC/IF |
| D36 | MILU/Hindi | Ex.36 | option3 (Logical Reasoning) | "TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______" — letter series with Roman characters in Hindi question | IC |
| D37 | MILU/Hindi | Ex.52 | option2 (History) | "सुंदर पांड्यन — पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया" — South Indian dynasty, less prominent in UPSC Hindi prep | IC |
| D38 | MILU/Hindi | Ex.109 | option4 (Politics) | "छत्तीसगढ़ में नगरपालिकाओं के सभी चुनावों के संचालन के लिए... अनुच्छेद 243 (ख)..." — state-specific (Chhattisgarh) content | IC |
| D39 | MILU/Hindi | Ex.200 | option4 | Correct answer for "पितृसत्तात्मक परिवार" labels patriarchal family; accepted factual answer | OC |

---

### Findings

#### CRITICAL

#### Finding CRITICAL1: Systematic Missing Content in Translated Items — Questions Reference Absent Lists, Statements, and Passages

- **Dimension(s):** IC, IF
- **Observation:** A substantial minority of the 245 sampled items (approximately 15–20 items identified) contain questions that explicitly instruct the model/student to evaluate "the following statements," "the following items (a, b, c, d)," "the given sentence," or "the given idiom" — but the referenced content is entirely absent from the question field. The answer options reference these missing elements (e.g., "केवल A और B," "केवल 1 और 3," "AEDBCF"). This renders the items unanswerable without the original source material, and a model's correct response would be chance-level or based on residual training knowledge rather than the provided content. This pattern appears across multiple subjects including Chemistry, Sociology, Language Studies, Logical Reasoning, Computer Science, and Economics.
- **Potential concern for deployment:** For a system evaluating Hindi-medium students preparing for central competitive exams, these items represent a fundamental data integrity failure. If a model "correctly" answers these questions, it demonstrates memorization of the answer from training data rather than reasoning from presented content — precisely the behavior this benchmark cannot differentiate. Benchmark accuracy scores on these items are not interpretable, inflating or deflating performance measures for the deployment use case in a non-reproducible way.
- **Datapoint citations:**
  - [D2] Example 69 (MILU/Hindi, split=validation, label=option2, Chemistry): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल / (b) केवल / (c) केवल" — options reference items (a)(b)(c) not present in question.
  - [D3] Example 86 (MILU/Hindi, split=validation, label=option2, Sociology): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, C और E" — states A–E never enumerated.
  - [D4] Example 56 (MILU/Hindi, split=validation, label=option2, Chemistry): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें... (1) और (2) केवल" — four statements entirely absent.
  - [D5] Example 94 (MILU/Hindi, split=validation, label=option4, Chemistry): "कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? केवल a, d" — reactions a–d not shown.
  - [D6] Example 95 (MILU/Hindi, split=validation, label=option1, Sports): "वाक्यों B, C, D और E को तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं" — sentences B–F entirely absent.
  - [D7] Example 106 (MILU/Hindi, split=validation, label=option2, Chemistry): "निम्नलिखित पदार्थों को कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4 / 4 2 3 1" — substances 1–4 unnamed.
  - [D10] Example 137 (MILU/Hindi, split=validation, label=option4, Politics): "ग्राम सभा क्या है: (ख) और (ग) केवल / (ग) और (घ) केवल" — definitions (क)(ख)(ग)(घ) absent.
  - [D11] Example 118 (MILU/Hindi, split=validation, label=option2, Language): "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें" — no idiom appears in question.
  - [D12] Example 152 (MILU/Hindi, split=validation, label=option1, Language): "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए..." — no sentence provided.
  - [D13] Example 151 (MILU/Hindi, split=validation, label=option1, Economics): "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं... कौन सा तर्क मजबूत है?" — statement and arguments not present.
  - [D14] Example 143 (MILU/Hindi, split=validation, label=option4, Logical Reasoning): "निम्नलिखित शब्दों को तार्किक और अर्थपूर्ण क्रम में व्यवस्थित करें" — words to order absent.
  - [D15] Example 145 (MILU/Hindi, split=validation, label=option2, Logical Reasoning): "कौन सा अक्षर समूह...दी गई श्रृंखला को पूरा करेगा?" — series not provided.
  - [D16] Example 188 (MILU/Hindi, split=validation, label=option3, Education): "निम्नलिखित में से किन समस्याओं का सामना कर रही है? केवल (a) / केवल (b)" — problems (a)(b) not listed.
  - [D17] Example 201 (MILU/Hindi, split=validation, label=option4, Computer Science): "BIOS के संदर्भ में सही है? केवल I और II" — statements I, II, III absent.
  - [D18] Example 222 (MILU/Hindi, split=validation, label=option2, Business): "फॉर्च्यून 500 सूची में... A, B, C और D केवल" — items A–E not enumerated.

---

#### Finding CRITICAL2: Option-as-Meta-Instruction Format Corruption

- **Dimension(s):** IF, OC
- **Observation:** At least one item has an answer option that is a meta-instruction rather than a substantive answer choice. Example 135, option4 reads "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें" ("Select the correct answer using the code given below") — this is a formatting artifact from a multi-step MCQ format (common in UPSC Prelims) where the original question provided a numbered code table, but the code table has been stripped during dataset processing. The correct answer is option3, meaning a student must choose from options that include one non-answer.
- **Potential concern for deployment:** This indicates systematic stripping of table/code structures during competitive exam scraping and dataset formatting. For central-exam competitive preparation (UPSC GS Paper I heavily uses "which of the following statements is/are correct?" with code tables), this format corruption is particularly consequential: the exact item types most representative of UPSC Prelims are the ones most likely to be corrupt in this dataset.
- **Datapoint citations:**
  - [D9] Example 135 (MILU/Hindi, split=validation, label=option3, Politics and Governance): Option4 = "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें" — a formatting directive appearing as an answer choice, indicating the code table (1/2 only, 2/3 only, etc.) was stripped.

---

#### MAJOR

#### Finding MAJOR1: 100% of Sampled Validation Items Are Machine-Translated from English

- **Dimension(s):** IC, IF
- **Observation:** Every single one of the 245 sampled validation examples carries `is_translated: True`. The benchmark documentation states that only ~25% of released questions are translated, and the remainder are natively sourced. However, the entire validation split sample reviewed here is 100% translated. This is either a property of the validation split specifically (which may have been populated disproportionately with translated items) or a sampling artifact. Either way, any few-shot evaluation using this validation set as the source of in-context examples will expose models exclusively to translated content as exemplars.
- **Potential concern for deployment:** For Hindi-medium competitive exam students, the register and phrasing of natively sourced Hindi exam questions differs substantially from machine-translated content. If few-shot examples are drawn from this validation split (as documented in Q51), models are being primed with translated Hindi that may not reflect the register of actual competitive exam question language. This is a potential construct-irrelevant variance source for deployment evaluation.
- **Datapoint citations:**
  - [D1] All 245 examples (MILU/Hindi, split=validation): `is_translated: True` — 245/245 items in sample are translated from English; no natively sourced Hindi validation items appear in this sample.

---

#### Finding MAJOR2: English Vocabulary Testing Within Hindi Language Studies Items — Exceeds 10% Code-Mixing Threshold

- **Dimension(s):** IC
- **Observation:** Several Language Studies items in the Hindi configuration test vocabulary knowledge of English words directly, asking Hindi-medium students to define English terms like "Didactic," "grim," and "Evangelize." These are not technical terms with standard Hindi equivalents but English literary/rhetorical vocabulary. Additionally, Logical Reasoning items use Roman-alphabet letter sequences (e.g., "TAB, TTZBB, TTBBB..." in Example 36) embedded in Hindi text. While some code-mixing with English technical terms is acceptable per the deployment specification (~10% ceiling), items that require knowledge of English literary vocabulary as the *core* assessment construct go beyond incidental code-mixing.
- **Potential concern for deployment:** Hindi-medium competitive exam aspirants preparing for UPSC/SSC are assessed on Hindi language proficiency (Hindi grammar, idiom, comprehension) not English vocabulary recognition. Items testing "Didactic," "grim," or "Evangelize" definitions create construct-irrelevant difficulty for this population: failure represents English vocabulary deficit, not Hindi language knowledge deficit. This is a direct IC validity concern for the target student population.
- **Datapoint citations:**
  - [D20] Example 76 (MILU/Hindi, split=validation, label=option2, Language Studies): "'डिडैक्टिक' शब्द का अर्थ क्या है? / नैतिक पाठ पढ़ाना" — English word 'Didactic' is the core test construct.
  - [D21] Example 90 (MILU/Hindi, split=validation, label=option3, Language Studies): "शब्द 'grim' का पर्यायवाची लिखें" — 'grim' is an English word; the question tests English synonym knowledge.
  - [D22] Example 105 (MILU/Hindi, split=validation, label=option4, Language Studies): "शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है... Evangelize / उपदेश देना" — English word tested.
  - [D36] Example 36 (MILU/Hindi, split=validation, label=option3, Logical Reasoning): "TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______" — Roman letter series embedded in Hindi question.

---

#### Finding MAJOR3: Output Ontology Fundamental Mismatch — MCQ Label Scoring Cannot Validate Hindi Explanatory Rationale

- **Dimension(s):** OO, OF
- **Observation:** All 245 sampled items follow the MCQ format with a single correct answer and `target` field specifying one of four options. The benchmark provides no rationale, explanation, or annotation of *why* an answer is correct. The deployment requires the AI system to return both a correct/incorrect label *and* a substantive Hindi-language explanation of why the answer is right or wrong.
- **Potential concern for deployment:** MILU benchmark accuracy scores measure only label selection correctness, not explanation quality. A model that achieves high accuracy on MILU MCQs may generate factually incorrect, incoherent, or pedagogically unhelpful Hindi explanations for the same questions. This is a fundamental output form mismatch: benchmark scores cannot be used to validate the deployment's core output, and no proxy measure for explanation quality exists within the benchmark infrastructure. This was anticipated in documentation but the sampled data confirms there is zero annotation supporting rationale assessment.
- **Datapoint citations:**
  - [D2]–[D18]: All examples — none contain a rationale field, explanation, or annotation of reasoning. The `target` field specifies only which option letter is correct. For instance, Example 83 [D34] presents a complex multi-paragraph civil services ethics scenario whose correct answer (option1) requires nuanced reasoning about tribal rights and official duties, yet no explanation is provided in the dataset.

---

#### Finding MAJOR4: Current Affairs Items Are Temporally Dated — Knowledge Currency Risk for Central Exam Deployment

- **Dimension(s):** OC
- **Observation:** Multiple Current Affairs and GK items reference specific events from 2018–2022 that are time-bound fact questions. Examples include India's GDP growth rate for July–September 2018 (Ex.74), the 2020 Archery Asia Cup gold medals won by India (Ex.2), the 2019 Japanese asteroid mission Ryugu (Ex.88), the 2020 Minister of Women and Child Development (Ex.132 — as of 2018), and the 2022 ASSOCHAM President (Ex.123 — December 2020). For a deployment targeting students preparing for current UPSC/SSC exams (2024–2026), questions testing 2018–2022 Current Affairs have limited validity for the "Current Affairs" domain.
- **Potential concern for deployment:** Current Affairs is a top-priority domain for UPSC/SSC/banking exam preparation. Students preparing for 2025–2026 exams need current knowledge; a benchmark evaluating 2018–2022 events cannot validly measure Current Affairs preparedness for the deployment cohort. Model performance on these items may also be inflated due to training data contamination (these events were well-covered in pre-training corpora).
- **Datapoint citations:**
  - [D25] Example 74 (MILU/Hindi, split=validation, label=option4, Economics): "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी? 7.1 प्रतिशत" — 2018 economic data.
  - [D26] Example 2 (MILU/Hindi, split=validation, label=option2, Sports): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022..." — 2022 sports event.
  - [D27] Example 88 (MILU/Hindi, split=validation, label=option1, Physics): "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान... रयुगु" — 2019 space event.

---

#### Finding MAJOR5: Subject Distribution Skewed Toward Engineering/Technology — Mismatch With Central Exam Priority Subjects

- **Dimension(s):** IO
- **Observation:** Among the 245 sampled validation items, there is a notably high concentration of Engineering & Technology domain items (approximately 45–50 items, roughly 18–20% of the sample). These cover topics like DC motor behavior (Ex.1), Half-Wave Rectifiers (Ex.3), Transformer types (Ex.4), AM modulation bandwidth (Ex.16), TDM frame rates (Ex.47), and chopper circuits (Ex.160). Engineering and technical content of this specificity is not tested in UPSC Prelims, SSC CGL, or banking exams. By contrast, Mathematics/Quantitative Aptitude — a top-priority subject for SSC and banking exams — appears to have very limited representation (only the compound interest problem Ex.84 and the weighted average Ex.120 are clearly quantitative aptitude items).
- **Potential concern for deployment:** The deployment targets UPSC, SSC, and banking exam preparation. For SSC CGL and IBPS PO, Quantitative Aptitude is a major paper; for UPSC, General Science (not advanced engineering) is tested. The overrepresentation of advanced Engineering content and underrepresentation of Mathematics/Quantitative Aptitude in this sample suggests the Hindi MILU subset may not adequately cover the most critical subject areas for the central exam deployment.
- **Datapoint citations:**
  - [D2], [D3] above plus: Example 1 (DC series motor — Engineering), Example 3 (Half-wave rectifier — Engineering), Example 4 (Transformer type — Engineering), Example 16 (AM bandwidth — Technology), Example 38 (Form factor — Engineering), Example 47 (TDM frame rate — Technology), Example 49 (Ampere's law — Physics/Engineering), Example 160 (Chopper circuit — Engineering) — approximately 18–20% of sample is advanced Engineering/Technology content not tested in UPSC/SSC/banking exams.
  - [D34] Example 83 (Sociology — Ethics case): Complex civil services ethics scenario; UPSC-style but appears only once in sample vs. numerous engineering items.

---

#### MINOR

#### Finding MINOR1: South India–Specific Content Present in Hindi-Language Items

- **Dimension(s):** IC
- **Observation:** Several items in the Hindi configuration specifically test knowledge of South Indian states, dynasties, cultural works, or current affairs not typically emphasized in central exam preparation from a North Indian Hindi-medium perspective. Examples include: the Pandya king who extended the empire to the Kaveri (Ex.52), Tamil magazine cartoon history (Ex.108), the classical Tamil epic "Silappatikaram" (Ex.232), Kota painting school period (Ex.193 — Rajasthan, North India-relevant), and Bhanda Pather theater of J&K (Ex.48). While some such items appear in UPSC GS, the framing and depth suggest sourcing from South Indian or regional state-level exams.
- **Potential concern for deployment:** Hindi-medium students from North India preparing for central exams would encounter UPSC-standard questions about South India, but questions with very fine-grained knowledge about South Indian literary/historical figures (Sundar Pandyan, Tamil epic authorship, Tamil magazine cartoons) may reflect South Indian regional exam content rather than central exam scope. This is a moderate concern for content validity.
- **Datapoint citations:**
  - [D37] Example 52 (MILU/Hindi, split=validation, label=option2, History):

