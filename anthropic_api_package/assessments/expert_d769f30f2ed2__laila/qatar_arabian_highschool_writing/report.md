## Deployment Context

**Use case:** Support high school students (G10-12) in editing and revising their Arabic essay drafts before submitting them for grading.
**Target population:** high school students (G10-12) in Arab countries (especially Qatar)

# Validity Analysis: laila
**Target context:** Arab High-School Arabic Essay Feedback (Qatar Primary)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ✓ | 3 | Moderate gaps | high |
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

LAILA is a high-quality Arabic AES dataset that establishes substantial within-Qatar validity for numeric trait scoring on persuasive and explanatory essays, but it is structurally misaligned with the proposed deployment along three of the four dimensions marked HIGH priority. (1) Output Form (1/5) and Output Ontology (1/5) are direct mismatches: the benchmark validates QWK agreement on ordinal scores while the deployment requires open-ended natural-language revision suggestions — an output category absent from the benchmark, and a field-wide gap in Arabic AES. (2) Input Ontology (2/5) covers only 2 of 5–7 deployment-required genres; literary analysis, religious/Quranic commentary, and cultural commentary are entirely absent and the CAST rubric is explicitly persuasive/argumentative. (3) Input Content (2/5) is single-country (Qatar) with explicit author acknowledgement of limited generalizability; cross-national rubric and curriculum alignment with Egypt, Saudi Arabia, Jordan, and Lebanon is empirically unstudied. Output Content (3/5) is strong within Qatar (qualified annotators, substantial IAA) but unvalidated cross-nationally. Input Form (4/5) aligns well as both contexts are digital Arabic text. The authors themselves prohibit operational deployment without independent validation [Q104, Q106].

## Practical Guidance

### What This Benchmark Measures

LAILA can validate model fidelity in producing numeric ordinal trait scores (REL, ORG, VOC, STY, DEV, MEC, GRA) and a holistic score on Qatari G10–12 explanatory and persuasive essays, against teacher-annotator judgments anchored in the CAST rubric. It is most informative for Output Content and Input Form within Qatar's persuasive/argumentative scope, where the benchmark's annotation rigor and digital-text alignment with deployment are genuine strengths.

### Construct Depth

The benchmark probes scoring agreement at the trait level with substantial QWK (avg 0.66–0.75), but it does not probe whether those scores can be translated into actionable feedback, whether they generalize across Arab national curricula, or whether they extend to genres beyond persuasive/explanatory. Construct depth is therefore moderate within scope and shallow outside it. The narrow REL scale (0–2) further compresses granularity on relevance judgments [Q91].

### What Else You Need

For deployment, supplementary evaluations are required for: (a) Output Form — a feedback-generation evaluation harness with rubrics for actionability, MSA register-appropriateness, and comprehensibility, evaluated by Arab teachers and students; (b) Input Ontology — datasets and rubrics covering literary analysis, religious/Quranic commentary, and cultural commentary; (c) Input Content & Output Content — cross-national annotation studies in Egypt, Saudi Arabia, Jordan, and Lebanon to estimate scoring-norm divergence from Qatari CAST conventions; (d) within-Qatar — school-type representativeness audit covering government, Arabic private, international, and community schools.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark's task taxonomy is restricted to 8 prompts spanning only two genres — explanatory and persuasive [Q38] — with the CAST rubric explicitly designed for persuasive/argumentative writing [Q118]. The deployment requires coverage of literary analysis, religious/Quranic commentary, and cultural commentary genres common in Arab high-school curricula, which the authors explicitly acknowledge as out of scope: 'limiting genre diversity and potentially affecting model robustness across other styles, such as narrative or descriptive writing' [Q89]. Web research confirms this is a field-wide gap: TAQEEM 2025 and ZaQQ 2025 maintain the same explanatory/persuasive restriction [WEB-10, WEB-11]. The benchmark also organizes its evaluation around prompt-specific and cross-prompt scoring setups [Q14, Q46], with the entire model output taxonomy restricted to numeric trait scoring [Q48, Q181] — no benchmarked task category corresponds to natural-language revision suggestion generation that the deployment requires. Given IO is HIGH priority in elicitation and multiple genre categories are missing, this represents significant taxonomic underrepresentation.

**Strengths:**
- Within its persuasive/argumentative scope, the taxonomy is well-articulated with two complementary evaluation setups (prompt-specific and cross-prompt) that probe different generalization regimes [Q14, Q46]
- The benchmark explicitly recognizes cross-prompt evaluation as more realistic and prioritizes it for future research [Q72, Q77], aligning with deployment-style use

**Checklist:**

- **IO-1**: Deployment requires explanatory, persuasive, literary analysis, religious/Quranic commentary, cultural commentary, and possibly narrative/descriptive genres, plus a feedback-generation task category alongside scoring [elicitation A4; regional YAML genre_coverage]. — _Sources: Q89_
- **IO-2**: Yes — benchmark covers only explanatory and persuasive genres [Q38, Q89]; literary analysis, religious text commentary, and cultural commentary are entirely absent. The output task taxonomy is also limited to numeric scoring [Q48], omitting the natural-language feedback generation category that the deployment requires. — _Sources: Q38, Q89, Q48, WEB-10, WEB-11_
- **IO-3**: No clear evidence that benchmark categories are irrelevant to the regional context — the persuasive and explanatory genres are themselves part of Arab curricula; the issue is omission, not inclusion of foreign categories.
- **IO-4**: Documented gaps: (a) genre coverage missing literary, religious, cultural commentary [Q89]; (b) absence of feedback-generation task type [Q48, Q181]; (c) explanatory prompts P1 and P5 themselves showed interpretive instability with higher REL=0 frequencies [Q124, Q125], suggesting even within-scope coverage has weaknesses. — _Sources: Q89, Q124, Q125, Q48_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q38] 'LAILA comprises 7,859 essays collected across 8 distinct prompts: 3 explanatory and 5 persuasive (3,446 and 4,413 essays, respectively).' (p.6)
- [Q89] 'LAILA includes only explanatory and persuasive writing prompts, limiting genre diversity and potentially affecting model robustness across other styles, such as narrative or descriptive writing.' (p.10)
- [Q118] 'CAST Persuasive/Argumentative Writing Rubric - English Translation' (p.13)
- [Q48] 'all models followed a multitask setup predicting holistic and trait scores jointly.' (p.7)
- [Q125] 'both P1 and P5 are explanatory prompts, which often allow greater flexibility in structure and content.' (p.14)

*Web sources:*
- [WEB-10] TAQEEM 2025 shared task continues the explanatory/persuasive genre restriction
- [WEB-11] ZaQQ 2025 dataset also confined to standard essay genres; no Arabic AES resource for religious/literary genres

</details>

**Information gaps:**
- Whether the deployment's specific genre mix (e.g., proportion of religious vs. literary essays) can be quantified for each target country's curriculum
- Whether explanatory prompts in LAILA approximate any deployment genre adequately enough to provide partial signal

**Requires expert verification:**
- Qatari and other Arab MoE curriculum specialists should confirm the genre breakdown actually assigned at G10–12 across school types

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Content was collected from 24 Qatari high schools with 4,372 students under exam-style supervision [Q3, Q27], with prompts deliberately designed to be 'developmentally appropriate for the target age groups, culturally relevant to the Arabic-speaking context, and free of sensitive topics' [Q99] and gender balance pursued [Q23, Q100]. However, the deployment targets Egypt, Saudi Arabia, Jordan, Lebanon and other Arab countries [elicitation A1], and the authors themselves acknowledge that single-country sampling 'may limit its generalizability to other Arabic-speaking populations due to diverse educational systems' [Q88]. The Qatar expatriate mitigation is partial only [Q88]. Web research confirms that secondary-curriculum Arabic writing rubrics in Egypt, Saudi Arabia, Jordan, and Lebanon are unverified against CAST [WEB-5, WEB-6, WEB-7], that Lebanese students show documented MSA-register avoidance [WEB-9], and that within Qatar itself ~60% of secondary students attend private schools across 23 curricula [WEB-1, WEB-3, WEB-4] with no documented school-type breakdown of the LAILA sample. Two prompts (P3, P4) are also under-represented [Q90], and average length is only 171 words [Q92], restricting extended-writing assessment. Given IC is HIGH priority, multiple substantive content gaps weigh heavily.

**Strengths:**
- Authentic classroom-produced writing under exam-style supervised conditions with IRB approval [Q21, Q3, Q95]
- Deliberate cultural relevance and age-appropriateness in prompt design [Q99]
- Explicit gender balance principle [Q23, Q100]
- Largest publicly available Arabic AES dataset [Q1, Q79]

**Checklist:**

- **IC-1**: Yes — Arabic high-school essays inherently require cultural, dialectal, and curricular knowledge. LAILA's content is anchored in Qatari institutional norms (QUTC, Qatar MoE) [Q33, Q84], and the regional YAML notes that Levantine-, Egyptian-, and French-contact-influenced MSA may diverge from Qatar's Gulf MSA conventions [WEB-9, gap_id 4]. — _Sources: Q33, Q84, WEB-9_
- **IC-2**: Partially — Qatar-targeted prompts are culturally appropriate for Qatar [Q99] but unvalidated for Egypt, Saudi Arabia, Jordan, or Lebanon, where curriculum bodies and rubrics differ [WEB-5, WEB-6, WEB-7] and no cross-national rubric comparison has been published (gap_id 1). — _Sources: Q99, Q88, WEB-5, WEB-6, WEB-7_
- **IC-3**: No clear Western-specific content was identified; LLM selection used the Open Arabic LLM Leaderboard [Q178], and prompts are Arabic. The risk is Qatar-centric rather than Western-centric content. — _Sources: Q178_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the LAILA paper does not document recruitment of non-Qatari Arab annotators; the regional YAML explicitly flags this as a gap requiring expert elicitation in each target country (gap_id 1).
- **IC-5**: Documented content issues: single-country sourcing [Q88], unverified cross-national applicability, prompt-count imbalance for P3/P4 [Q90], short average length restricting long-form assessment [Q92], and undocumented Qatari school-type representation [WEB-1, WEB-4]. — _Sources: Q88, Q90, Q92, WEB-1, WEB-4_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'we visited 24 high schools in Qatar and collected essays directly from 4,372 students in authentic classroom settings.' (p.1)
- [Q88] 'LAILA was collected from students in a single country, Qatar, and specific grade levels, grades 10 to 12, which may limit its generalizability to other Arabic-speaking populations due to diverse educational systems.' (p.9)
- [Q99] 'Essay prompts were carefully designed to be developmentally appropriate for the target age groups, culturally relevant to the Arabic-speaking context, and free of sensitive topics or potentially harmful content.' (p.10)
- [Q90] 'two of the prompts (Prompts 3 and 4) have fewer essays than the rest, which could introduce imbalance' (p.10)
- [Q92] 'with an average essay length of only 171 words, the dataset lacks extended writing samples, restricting the assessment of models on long-form academic tasks' (p.10)

*Web sources:*
- [WEB-1] Qatar 2024–2025: 278 government schools (~137,048 students), 351 private schools (~228,488 students); ~60% of secondary students in private schools
- [WEB-4] 23 distinct curricula operate in Qatar; British curriculum leads at 45.8% of K-12 schools
- [WEB-9] Lebanese students documented to resist formal MSA literary register
- [WEB-5] Egypt's curriculum reform ongoing since 2018; writing assessment norms in transition
- [WEB-6] Saudi Arabia uses centrally produced rating tools managed by supervisors

</details>

**Information gaps:**
- School-type breakdown of LAILA's 24-school sample (government vs. Arabic private vs. international vs. community)
- Whether and how non-Qatari Arab dialectal influence on MSA is treated by annotators
- Cross-national curriculum rubric divergence for STY/DEV

**Requires expert verification:**
- Curriculum specialists in Egypt, Saudi Arabia, Jordan, Lebanon to confirm whether Qatari prompts and topic conventions transfer
- LAILA authors regarding within-Qatar school-type sampling

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
The input form is digital Arabic text submitted via Microsoft Forms under a 65-minute timed condition [Q25, Q26], aligning well with the deployment's text-based formative-feedback interface. The script is native Arabic (RTL), eliminating Latin-script mismatch concerns. Length distribution is unimodal around 171 words [Q134, Q135] with a smaller cluster of short essays (11–60 words, 1,061 essays) [Q136], and very few essays exceed 500 words [Q138] — a meaningful but minor mismatch with deployment, where formative drafts may vary more in length and grade-level. Model-specific input formats (AraBERT pooling + 816 features [Q156, Q157], AraT5 instruction+text [Q148], LLMs with 4096-token context [Q184]) are reasonable for Arabic NLP. Internet penetration in Qatar is 99% [WEB-14], supporting digital deployment. IF was marked LOWER priority, and the form alignment is genuinely strong; the main residual concern is that benchmark essays are exam-style timed productions while deployment drafts are pre-submission and may differ in length/polish.

**Strengths:**
- Native Arabic script, RTL-appropriate, no script-encoding mismatch [Q25, Q26]
- Digital text submission matches deployment modality
- Diverse handcrafted feature set covering surface, readability, lexical, semantic, syntactic aspects [Q54]
- Qatar internet penetration ~99% supports web-based deployment [WEB-14]

**Checklist:**

- **IF-1**: Signal distributions match — both benchmark and deployment use digital Arabic text. Length distribution differs slightly: benchmark concentrates at 150–180 words [Q135] with few long essays [Q138], whereas deployment drafts may span a wider range. — _Sources: Q25, Q134, Q135_
- **IF-2**: Yes — digital infrastructure is available; Qatar reports 99% internet penetration [WEB-14]. Secondary-geography figures are not verified [regional YAML internet_connectivity_secondary_geographies]. — _Sources: WEB-14_
- **IF-3**: Domain-specific differences: timed exam-style production [Q25] vs. formative untimed draft; benchmark lacks long-form samples (>500 words) [Q138, Q92], which limits validation for extended writing assignments. — _Sources: Q25, Q92, Q138_
- **IF-4**: Minor form mismatches: length-distribution skew toward short essays and absence of long-form coverage [Q92, Q138]; timed vs. untimed production conditions. — _Sources: Q92, Q138_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'LAILA was designed to collect essays written under timed conditions using a digital submission platform.' (p.3)
- [Q26] 'we configured a Microsoft Form for digital essay submission, set with a 65-minute time limit' (p.5)
- [Q134] 'unimodal pattern centered around an average essay length of 171 words, with the majority of essays concentrated between 90 and 210 words.' (p.15)
- [Q92] 'with an average essay length of only 171 words, the dataset lacks extended writing samples' (p.10)
- [Q138] 'Beyond 420 words, the frequency drops sharply, with only a few essays exceeding 500 words' (p.15)

*Web sources:*
- [WEB-14] 99% internet penetration in Qatar as of 2024

</details>

**Information gaps:**
- Length and polish distribution of typical formative drafts in deployment
- Internet/device infrastructure in non-Qatar target geographies

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
This is the most severe misalignment. LAILA's output ontology is exclusively numeric ordinal trait scoring on the CAST rubric: 6 traits at 0–5 plus REL at 0–2 [Q34, Q36], with holistic computed as the sum [Q35, Q182]. All benchmarked models 'followed a multitask setup predicting holistic and trait scores jointly' [Q48]; LLMs produce trait scores in JSON format [Q181]; AraT5 formulates AES as text generation of trait names plus scores [Q147]. The deployment requires actionable natural-language revision suggestions explaining why points were lost [elicitation A3, regional YAML output_function], a qualitatively different output category that is entirely absent from the benchmark's output schema. Web research confirms this gap is field-wide: 'crucial aspects of writing evaluation, such as providing feedback, have often been overlooked' even in English [WEB-12], and no Arabic rubric-to-natural-language feedback system exists [WEB-13, WEB-23]. The CAST rubric is also explicitly genre-scoped to persuasive/argumentative writing [Q118], compounding the misalignment with deployment genres. The narrow REL scale (0–2) further limits granularity [Q91]. OO is HIGH priority and the mismatch is direct, structural, and acknowledged by the authors who 'explicitly prohibit its use for high-stakes educational decisions' [Q104].

**Strengths:**
- Trait-decomposed scoring offers a principled construct decomposition (REL, ORG, VOC, STY, DEV, MEC, GRA) that could anchor downstream feedback generation [Q34]
- CAST rubric is institutionally grounded in QUTC and provided in Arabic [Q33, Q114]
- Zero-rule for irrelevant essays (REL=0 → all traits 0) reflects pedagogical logic [Q37, Q117]

**Checklist:**

- **OO-1**: The 7-trait label space is broadly relevant to Arab high-school writing assessment, but the rubric is explicitly designed for persuasive/argumentative writing [Q118], limiting regional relevance for literary, religious, or cultural-commentary genres. — _Sources: Q34, Q118_
- **OO-2**: Missing categories: (a) natural-language feedback / revision-suggestion outputs that the deployment requires [elicitation A3, WEB-12]; (b) trait categories or rubric dimensions specific to genres absent from the benchmark (e.g., textual fidelity for Quranic commentary, literary device recognition). — _Sources: Q48, Q181, WEB-12_
- **OO-3**: INSUFFICIENT DOCUMENTATION on whether CAST trait definitions encode Qatar-specific stylistic norms versus pan-Arab conventions; the regional YAML flags this as gap_id 1.
- **OO-4**: Stakeholder-driven taxonomy redesign would be needed to (i) add a feedback-generation output category and (ii) extend or replace the rubric for non-persuasive genres. — _Sources: Q118, WEB-12_
- **OO-5**: Documented taxonomy issues: numeric-only output schema [Q48, Q181, Q147]; CAST genre-specificity [Q118]; narrow REL scale limits granularity [Q91]; no validated mapping from trait scores to actionable feedback. — _Sources: Q48, Q181, Q147, Q118, Q91_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q34] 'The rubric covers 7 writing traits [D4]: Relevance (REL), Organization (ORG), Vocabulary (VOC), Style (STY), Development (DEV), Mechanics (MEC), and Grammar (GRA).' (p.5)
- [Q48] 'all models followed a multitask setup predicting holistic and trait scores jointly.' (p.7)
- [Q181] 'the LLM is tasked with generating trait scores in JSON format, given the prompt text, essay, and trait rubrics.' (p.18)
- [Q118] 'CAST Persuasive/Argumentative Writing Rubric - English Translation' (p.13)
- [Q91] 'the relevance trait is scored on a narrow scale from 0 to 2, which limits the granularity of evaluation and may cause QWK to underrepresent subtle differences in model predictions.' (p.10)
- [Q104] 'We explicitly prohibit its use for high-stakes educational decisions affecting individual students.' (p.10)

*Web sources:*
- [WEB-12] 2024 Springer survey: feedback generation explicitly identified as overlooked in AES literature
- [WEB-13] AAEE Saudi system generates corrected essay versions but not trait-grounded revision suggestions
- [WEB-10] TAQEEM 2025 — first Arabic AES shared task — also limited to scoring outputs

</details>

**Information gaps:**
- Whether trait-score outputs can be reliably converted to feedback through downstream generation models
- Whether CAST trait definitions encode Qatar-specific norms

**Requires expert verification:**
- Pedagogical experts on whether the CAST trait decomposition supports formative feedback at all

---

### Output Content — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Annotation quality within Qatar is a relative strength: 6 annotators + 3 supervisors, all Arabic-language teachers/lecturers with 5 holding advanced degrees [Q30, Q31], with detailed guidelines, training, moderation, and adjudication procedures [Q41, Q42, Q43]. Inter-annotator agreement is substantial, averaging QWK 0.66 (P5) to 0.75 (P1) [Q44]. However, P5 required third-annotator adjudication on 23.3% of essays [Q45], indicating interpretive instability on explanatory prompts. The decisive concern is institutional homogeneity: rubric, annotators, schools, and funding are all Qatar-anchored (QUTC, QRDI, Qatar MoE) [Q33, Q84, Q86], with no documented non-Qatari annotators and no cross-national norm validation (gap_id 1, gap_id 6). For deployment in Egypt, Saudi Arabia, Jordan, and Lebanon, it is unknown whether STY and DEV labels reflect pan-Arab teacher consensus or Qatar-specific institutional convention [WEB-5, WEB-6, WEB-7]. OC was rated MODERATE priority, and the in-region (Qatar) signal is genuinely positive — but the cross-national transferability is unsubstantiated. A score of 3 reflects strong within-Qatar content validity tempered by unvalidated transferability.

**Strengths:**
- All annotators qualified Arabic-language educators, 5 with MSc/PhD [Q30, Q31]
- Substantial inter-annotator QWK agreement averaging 0.66–0.75 [Q44]
- Comprehensive guidelines with terminology, exemplars, training, moderation [Q41, Q102]
- Annotator-blind scoring with anonymization [Q42, Q98]
- Adjudication procedure for high-discrepancy essays [Q43]
- Fair compensation for annotators at or above local professional rates [Q101]

**Checklist:**

- **OC-1**: Labels reflect Qatari Arabic-language-teacher perspectives [Q30, Q31, Q33, Q84]. Whether they reflect Egyptian, Saudi, Jordanian, or Lebanese stakeholder perspectives is undocumented [gap_id 1]. — _Sources: Q30, Q31, Q33, Q84_
- **OC-2**: Potential disagreement is plausible for subjective traits (STY, DEV) but unmeasured. Lebanese student MSA-register avoidance [WEB-9] suggests a different teacher community may judge stylistic features differently. — _Sources: WEB-9, WEB-5_
- **OC-3**: Annotator demographics partially documented: 6+3 team, Arabic-language educators, 5 with advanced degrees [Q30, Q31]; nationality and per-trait IAA breakdown not in published paper [gap_id 6]. — _Sources: Q30, Q31_
- **OC-4**: Re-annotation by a representative cross-national pool would be needed before deploying outside Qatar. — _Sources: WEB-5, WEB-6, WEB-7, WEB-9_
- **OC-5**: Aggregation rule (mean rounded down, supervisor adjudication if HOL diff ≥ 6) [Q43] could erase minority annotator perspectives, though escalation provides a safety valve. Within-Qatar perspectives may also collapse to a single institutional norm. — _Sources: Q43_
- **OC-6**: Documented label issues: single-institution annotator pool [Q84], unmeasured cross-national norm transferability, P5 elevated adjudication rate [Q45]. — _Sources: Q84, Q45_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q30] 'The hired annotation team consisted of 6 annotators and 3 supervisors, all of whom were Arabic language teachers or lecturers with educational backgrounds.' (p.5)
- [Q31] 'Five members of the team hold advanced degrees (MSc or PhD) in the Arabic language.' (p.5)
- [Q44] 'IAA was substantial across prompts, with an average QWK ranging from 0.66 (P5) to 0.75 (P1)' (p.6)
- [Q45] 'P5 showed the lowest average agreement, noting that it has the highest percentage of essays that require a third annotator (A3: 23.3%)' (p.6)
- [Q84] 'we heartily thank our dedicated annotators ... Qatar University Testing Center, the Ministry of Education and Higher Education in Qatar' (p.9)
- [Q43] 'essays with large discrepancies between annotators (≥ 6 points difference in the HOL score) were flagged and escalated to a supervisor' (p.6)

*Web sources:*
- [WEB-5] Egypt's curriculum reform suggests evolving writing-assessment norms not aligned with CAST
- [WEB-6] Saudi Arabia uses centrally produced rating tools managed by supervisors
- [WEB-9] Lebanese student MSA-register avoidance suggests differing teacher norms
- [WEB-7] Lebanon's CRDP authoritative but Arabic writing rubrics not in searchable form

</details>

**Information gaps:**
- Per-trait IAA breakdown (especially STY, DEV)
- Annotator nationality / non-Qatari Arab participation
- Cross-national teacher-judgment correlation studies

**Requires expert verification:**
- Sample re-annotation by Egyptian, Saudi, Jordanian, Lebanese teachers to estimate cross-national QWK

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The output-form mismatch is the most direct and explicitly documented gap. LAILA evaluates models using QWK between human and model numeric scores [Q58] with hyperparameter optimization on average QWK [Q59, Q60, Q61]; LLMs are constrained to JSON-formatted scores via the outlines library [Q190]. The deployment requires open-ended natural-language revision suggestions in MSA accessible to G10–12 students [elicitation A3, regional YAML output_function]. QWK on numeric scores cannot capture pedagogical usefulness, actionability, or comprehensibility of generated feedback. The authors themselves recognize this limit by prohibiting high-stakes use [Q104] and recommending 'fairness auditing and stakeholder consultation before real-world application' [Q106]. Web research confirms no Arabic rubric-to-natural-language feedback evaluation framework exists [WEB-12, WEB-13, WEB-23]. OF was marked HIGH priority. Even basic infrastructure for evaluating feedback quality (rubrics for actionability, register-appropriateness, MSA fluency) is absent from the benchmark.

**Strengths:**
- QWK is the established gold-standard metric for ordinal scoring agreement [Q58]
- JSON output enforcement and three-seed averaging for LLM experiments improve numeric-output reproducibility [Q189, Q190]
- Authors transparently flag the limits of the current evaluation [Q104, Q106]

**Checklist:**

- **OF-1**: No — benchmark output modality is structured numeric/JSON scores [Q58, Q181, Q190]; deployment requires open-ended natural-language MSA feedback. Direct mismatch. — _Sources: Q58, Q181, Q190_
- **OF-2**: Not applicable — deployment is text-based; TTS not required.
- **OF-3**: Literacy is high in target population (G10–12 students); MSA register-appropriateness for adolescents is the key accessibility consideration, on which the benchmark provides no signal.
- **OF-4**: Documented form mismatch: QWK [Q58] cannot capture pedagogical usefulness, comprehensibility, or actionability of generated revision suggestions; benchmark explicitly prohibits operational deployment without independent validation [Q104, Q105]. — _Sources: Q58, Q104, Q105, WEB-12, WEB-13_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q58] 'We evaluate model performance using QWK to measure agreement between human and model scores.' (p.8)
- [Q190] 'For all the LLM experiments, we used vLLM for inference with the outlines library to enforce the JSON output format.' (p.18)
- [Q181] 'In the zero-shot setting, the LLM is tasked with generating trait scores in JSON format' (p.18)
- [Q104] 'We explicitly prohibit its use for high-stakes educational decisions affecting individual students.' (p.10)
- [Q106] 'We recommend that any system developed using LAILA undergo fairness auditing and stakeholder consultation before real-world application.' (p.10)

*Web sources:*
- [WEB-12] AES literature explicitly identifies feedback generation as an overlooked area
- [WEB-13] AAEE Saudi system provides corrected essays but not trait-grounded revision suggestions
- [WEB-23] No Arabic system bridges trait scores to actionable natural-language feedback for secondary students

</details>

**Information gaps:**
- Whether any supplementary Arabic feedback-generation evaluation rubric is in development
- Whether downstream LLM-generated feedback can be calibrated against LAILA scores

**Requires expert verification:**
- Pedagogical experts and Arabic-language teachers on what 'good' formative feedback looks like in MSA for G10–12

---

## Remediation Suggestions

### Output Form ⚠

**Gap:** Benchmark evaluates only numeric/JSON score agreement (QWK), providing no signal on natural-language feedback quality, actionability, or MSA register-appropriateness.

**Recommendation:** Construct a supplementary feedback-generation evaluation: pair each LAILA essay with teacher-authored model revision feedback, then evaluate generated feedback on a multi-axis rubric (faithfulness to trait scores, actionability, MSA register, student comprehensibility). Pilot with Arab high-school teachers and G10–12 students before any deployment.

### Output Ontology ⚠

**Gap:** Output schema is restricted to numeric trait scoring with no feedback-generation category; CAST rubric is genre-specific to persuasive/argumentative writing.

**Recommendation:** Redesign the output ontology to include a feedback-generation task and extend or replace CAST with rubrics validated for literary analysis, religious commentary, and cultural commentary genres. Engage Qatari and other Arab curriculum specialists to define rubric categories.

### Input Ontology ⚠

**Gap:** Only explanatory and persuasive prompts are covered; literary analysis, religious/Quranic commentary, and cultural commentary genres are absent — and confirmed missing from TAQEEM 2025 and ZaQQ as well.

**Recommendation:** Collect a complementary Arabic essay corpus covering the missing genres at G10–12, with prompts validated against multiple national curricula, and develop genre-appropriate annotation guidelines.

### Input Content ⚠

**Gap:** All essays are from Qatari students; cross-national generalizability is acknowledged as limited and within-Qatar school-type breakdown is undocumented.

**Recommendation:** Conduct cross-national essay collection in Egypt, Saudi Arabia, Jordan, and Lebanon at G10–12, and audit the Qatar sample's school-type distribution against MoEHE statistics (government, Arabic private, international, community).

### Input Form

**Gap:** Benchmark concentrates on short timed exam essays (~171 words) with very few long-form samples; deployment drafts may differ in length and polish.

**Recommendation:** Augment evaluation with longer-form essay samples (>500 words) and untimed draft conditions to test model robustness for formative pre-submission contexts.

### Output Content

**Gap:** All annotators are Qatar-affiliated; cross-national norm transferability for subjective traits (STY, DEV) is empirically unstudied.

**Recommendation:** Recruit a representative pool of Egyptian, Saudi, Jordanian, and Lebanese Arabic-language teachers to re-annotate a stratified subsample of LAILA essays; report cross-national QWK per trait to quantify norm divergence before deploying outside Qatar.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "LAILA, the largest publicly available Arabic AES dataset to date, comprising 7,859 essays annotated with holistic and trait-specific scores on seven dimensions: relevance, organization, vocabulary, style, development, mechanics, and grammar." |
| Q2 | 1 | input_content | "The dataset comprises 7,859 essays across 8 distinct prompts making it the most extensive publicly available Arabic resource of its kind." |
| Q3 | 1 | input_content | "Under Institutional Review Board (IRB) approval, we visited 24 high schools in Qatar and collected essays directly from 4,372 students in authentic classroom settings." |
| Q4 | 1 | output_ontology | "Table 1: Brief description of the traits in LAILA." |
| Q5 | 1 | output_content | "Trait-Specific Annotations: We provide de-" |
| Q6 | 1 | output_content | "Annotation Guidelines: We develop and share comprehensive guidelines for data annotation to ensure transparency and reproducibility." |
| Q7 | 1 | output_content | "May Bashendy, Walid Massoud, Sohaila Eltanbouly, Salam Albatarni, Marwan Sayed, Abrar Abir, Houda Bouamor, Tamer Elsayed." |
| Q8 | 1 | output_content | "Computer Science and Engineering Department, Qatar University and Carnegie Mellon University in Qatar." |
| Q9 | 1 | output_content | "IRB Number: QU-IRB 159/2024-EA" |
| Q10 | 1 | input_content | "Arabic AES research faces a significant data scarcity problem, as publicly available annotated datasets remain limited." |
| Q11 | 1 | input_content | "Existing Arabic resources are often small in scale such as QAES (Bashendy et al., 2024), lack trait-specific annotations as in ZAEBAC (Habash and Palfreyman, 2022), or consist solely of unannotated essays such as ALC." |
| Q12 | 2 | input_form | "Table 2: Comparison of LAILA with existing essay datasets. "Len" is average essay length in words; "HOL" indicates holistic scoring; "Eur" covers German, Italian, and Czech; "L1/L2" denotes native or second-language learners; "Public" here means freely available." |
| Q13 | 2 | output_ontology | "tailed trait-specific annotations that capture multiple dimensions of writing proficiency." |
| Q14 | 2 | input_ontology | "We establish baseline AES results for Arabic under two evaluation setups: prompt-specific and cross-prompt." |
| Q15 | 2 | output_form | "We publicly release LAILA, including essays with holistic and trait-specific annotations. We also release the benchmarking code to support replication and future research." |
| Q16 | 2 | input_content | "Section 2 reviews related work and existing AES datasets. Section 3 outlines the data collection design principles, while Section 4 describes the dataset construction process, including school and prompt selection, essay collection, and annotations." |
| Q17 | 2 | input_content | "Research on AES has advanced considerably in English, supported by large-scale, publicly available datasets such as ASAP/ASAP++ (Mathias and Bhattacharyya, 2018), TOEFL11 (Blanchard et al., 2013), ELLIPSE (Crossley et al., 2023a), and PERSUADE (Crossley et al., 2023b)." |
| Q18 | 2 | input_content | "In contrast, other languages have far fewer resources. Some smaller datasets exist, including ACEA (Chinese; annotated but not public) (He et al., 2022), TCFLE-8 (French; public but with only holistic scores) (Wilkens et al., 2023), and MERLIN (German, Italian, and Czech; public but limited to holistic annotations) (Boyd et al., 2014). While useful for AES studies, their limited scale and annotation depth restrict their utility." |
| Q19 | 2 | input_content | "Compared with English and other languages, Arabic AES lacks robust datasets. Few datasets have been developed, both public and proprietary, yet all face limitations in scale, annotation depth, or accessibility." |
| Q20 | 3 | input_ontology | "The development of LAILA was guided by nine core design principles [D1–D9], each reflecting deliberate choices to ensure a high-quality, representative, and ethically sound resource for Arabic AES." |
| Q21 | 3 | input_content | "[D1] Ensuring Data Integrity: We designed LAILA to capture authentic, classroom-produced writing created without external assistance. This design choice preserves genuine linguistic variation, learner errors, and authentic complexities essential for real-world AES applications." |
| Q22 | 3 | input_content | "[D2] Maximizing Diversity: To reflect the breadth of Arabic writing proficiency, LAILA was planned to collect essays from multiple educational institutions and student populations with diverse academic and demographic backgrounds. Prompts were intentionally varied across genres, ensuring cultural relevance and age appropriateness, thereby promoting model generalization and reducing bias." |
| Q23 | 3 | input_content | "[D3] Achieving Gender Balance: We intentionally aimed to balance the number of essays from male and female students to promote fairness, reduce gender-based bias, support inclusive evaluation, and enhance model generalization." |
| Q24 | 3 | output_ontology | "[D4] Supporting Full Trait Coverage: LAILA was built to capture multiple dimensions of writing quality through annotations of relevance, organization, vocabulary, style, development, mechanics, and grammar. This design supports fine-grained assessment and meaningful feedback." |
| Q25 | 3 | input_form | "[D5] Ensuring Authentic Writing Conditions: To emulate real academic or high-stakes testing scenarios, LAILA was designed to collect essays written under timed conditions using a digital submission platform. This setup ensures consis" |
| Q26 | 5 | input_form | "taining one persuasive and one explanatory prompt, along with a unique, pre-generated ID to maintain students' anonymity while enabling metadata tracking [D6]. We also configured a Microsoft Form for digital essay submission, set with a 65-minute time limit to enforce a time-restricted setup [D5]." |
| Q27 | 5 | input_content | "Data collection spanned one academic year through 27 school visits (24 initial, three follow-ups), by nine team members, to meet the target student count." |
| Q28 | 5 | input_content | "Each visit, which lasted around six hours, was supported by at least two team members, an IT teacher, and proctoring teachers." |
| Q29 | 5 | input_form | "The collected essays then underwent a cleaning process to ensure data quality before the annotation phase. First, we resolved duplicate and misidentified submissions, by correcting ID mismatches through manual verification and name cross-referencing. Next, a manual review eliminated submissions lacking meaningful content, e.g., irrelevant personal content. Lastly, essays with 10 or fewer words were excluded for being insufficient for AES analysis." |
| Q30 | 5 | output_content | "The hired annotation team consisted of 6 annotators and 3 supervisors, all of whom were Arabic language teachers or lecturers with educational backgrounds." |
| Q31 | 5 | output_content | "Five members of the team hold advanced degrees (MSc or PhD) in the Arabic language." |
| Q32 | 5 | output_content | "The supervisors oversaw training, quality assurance, and dispute resolution, while the annotators performed the primary scoring tasks." |
| Q33 | 5 | output_ontology | "All essays in LAILA dataset were scored using the Core Academic Skills Test (CAST) rubric [D7], developed by the Qatar University Testing Center (QUTC)." |
| Q34 | 5 | output_ontology | "The rubric covers 7 writing traits [D4]: Relevance (REL), Organization (ORG), Vocabulary (VOC), Style (STY), Development (DEV), Mechanics (MEC), and Grammar (GRA)." |
| Q35 | 5 | output_ontology | "Additionally, a Holistic score (HOL) was computed as the sum of the 7 trait scores." |
| Q36 | 5 | output_ontology | "Six traits (all but REL) were rated on a 6-point scale (0 = lowest, 5 = highest), while REL was rated on a 3-point scale (0 = not relevant, 1 = partially relevant, and 2 = fully relevant)." |
| Q37 | 5 | output_ontology | "Furthermore, if an essay received a REL score of 0, all other trait scores were set to 0, as irrelevant responses are not subject to further evaluation." |
| Q38 | 6 | input_ontology | "LAILA comprises 7,859 essays collected across 8 distinct prompts: 3 explanatory and 5 persuasive (3,446 and 4,413 essays, respectively)." |
| Q39 | 6 | input_form | "Table 3 shows that the number of essays per prompt ranges from 500 to 1,181. Essay lengths demonstrate consistency across prompts, with an average of 171 words and a maximum of 706 words." |
| Q40 | 6 | output_ontology | "Most traits follow a near-normal pattern on the 6-point scale, indicating overall positive essay quality. The REL scores show that 86% of the essays agree strongly with the prompt. In contrast, GRA and VOC show the highest percentage of score 1 at 16%, followed by MEC at 13%, highlighting that these traits pose the greatest challenges." |
| Q41 | 6 | output_content | "To ensure consistency, 2 supervisors developed an annotation guidebook with detailed terminology, exemplars, and annotated practices for each prompt type. Annotators were required to review these materials and complete training sessions before formal annotation. Moderation sessions followed, where discrepancies were discussed and interpretations of the rubric were harmonized." |
| Q42 | 6 | output_content | "The scoring process was conducted using the Assessment Gourmet Platform, which supports large-scale, anonymized essay scoring. The platform ensured that annotators were blinded to student identity [D6], while only supervisors had access to annotator metadata for monitoring purposes." |
| Q43 | 6 | output_content | "The essays were randomly distributed among the annotators to minimize systematic bias, and the scoring sessions were capped to prevent annotators' fatigue. Each essay was independently scored by two annotators across all traits. If the difference in HOL scores between the two annotators was less than 6 points, the mean of the two scores was computed and then rounded down to the nearest integer; this rounded value was adopted as the final score for each trait. However, essays with large discrepancies between annotators (≥ 6 points difference in the HOL score) were flagged and escalated to a supervisor (a third annotator in this case), who provided the final adjudicated score and offered feedback to the annotators to improve alignment and consistency in subsequent batches of essays." |
| Q44 | 6 | output_content | "We compute IAA using Quadratic Weighted Kappa (QWK) (Williamson et al., 2012) to assess agreement between the two main annotators (A1 and A2), prior to adjudication. Table 4 reports QWK per trait and prompt, with agreement strength following Landis and Koch (1977). Overall, IAA was substantial across prompts, with an average QWK ranging from 0.66 (P5) to 0.75 (P1), showing strong consistency." |
| Q45 | 6 | output_content | "However, variability emerges by prompt and trait. In particular, P5 showed the lowest average agreement, noting that it has the highest percentage of essays that require a third annotator (A3: 23.3%; Table 3). This suggests greater initial disagreement" |
| Q46 | 7 | input_ontology | "For each setup, we investigate two research questions in the context of Arabic AES: (RQ1) how do different categories of models compare in overall performance?, and (RQ2) which models achieve the best results across individual traits?." |
| Q47 | 7 | input_ontology | "Model Selection We selected a diverse set of models with varying architectures to establish strong baselines for LAILA. The selection criteria included code availability, ease of implementation, and coverage of SOTA Arabic and English models." |
| Q48 | 7 | output_ontology | "The models fall into three categories: feature-based (FB), encoder-based, and large language models (LLMs). LLMs were evaluated in zero-shot and few-shot settings, and all models followed a multitask setup predicting holistic and trait scores jointly." |
| Q49 | 7 | input_ontology | "We selected 4 FB models: Linear Regression (LR), Random Forest (RF), Extreme Gradient Boosting (XGB), and a feedforward Neural Network (NN)." |
| Q50 | 7 | input_ontology | "For encoder-based models, we fine-tuned two pre-trained SOTA systems: AraBERT (Antoun et al., 2020), combined with handcrafted features (Sayed et al., 2025), and AraT5 (Nagoudi et al., 2022), inspired by the strong performance of T5 in English AES (Do et al., 2024)." |
| Q51 | 7 | input_ontology | "For LLMs, we evaluated three Arabic-centric models: ALLaM (Bari et al., 2025), Command-R7B-Arabic (R7B) (Alnumay et al., 2025), and Fanar (Team et al., 2025), under zero-shot and few-shot (5-shot) settings." |
| Q52 | 7 | output_form | "For the prompt-specific experiments, we used 5-fold cross-validation using the predefined 5 splits. In each cross-validation iteration, one fold (20%) was used as the test set, and the remaining four folds were further split into training (70%) and development (10%) sets, with stratification applied to maintain consistent prompt distributions and ensure consistent evaluation across models." |
| Q53 | 7 | input_ontology | "For encoder-based models, we employ the same AraBERT-based architecture, which performed strongly in Arabic AES (Sayed et al., 2025), along with two SOTA English AES models, ProTACT (Do et al., 2023) and MOOSE (Chen et al., 2025)." |
| Q54 | 8 | input_form | "We implemented the 816 handcrafted features introduced by Sayed et al. (2025) for Arabic AES, encompassing surface, readability, lexical, semantic, and syntactic aspects." |
| Q55 | 8 | input_form | "These features were applied to the FB models, ProTACT, MOOSE, and AraBERT." |
| Q56 | 8 | input_form | "To mitigate noise, we performed feature selection based on Pearson and Spearman correlations (Li and Ng, 2024), retaining features whose absolute correlation with any trait exceeded a predefined threshold for either metric." |
| Q57 | 8 | input_form | "For MOOSE, however, we did not apply this explicit feature selection step." |
| Q58 | 8 | output_form | "We evaluate model performance using QWK to measure agreement between human and model scores." |
| Q59 | 8 | output_form | "Hyperparameters are tuned via Bayesian optimization with the Tree-structured Parzen Estimator algorithm (Bergstra et al., 2011), implemented using Optuna's TPESampler." |
| Q60 | 8 | output_form | "We ran 20 trials with 5 startup trials and a fixed random seed of 11." |
| Q61 | 8 | output_form | "The best configuration, selected based on average QWK on the development set, was used for final evaluation on the test data." |
| Q62 | 9 | output_form | "FB models showed comparable performance, with only a 2-point difference between the top performer (XGB) and the lowest (NN), highlighting consistency of these feature-based approaches." |
| Q63 | 9 | output_form | "Among encoder-based models, ProTACT exhibited the lowest performance overall, suggesting limited transferability from its English architecture, while AraBERT trailed XGB by 4.4 points." |
| Q64 | 9 | output_form | "Notably, MOOSE achieved the highest performance among all evaluated cross-prompt models." |
| Q65 | 9 | output_form | "For LLMs, few-shot prompting improved Fanar and R7B (+19 and +11.6 points), whereas ALLaM dropped by 7 points, indicating high sensitivity to prompt design." |
| Q66 | 9 | output_form | "No single model consistently outperformed the others across individual traits." |
| Q67 | 9 | output_form | "MOOSE performed best in REL, STY, and GRA traits." |
| Q68 | 9 | output_form | "For the remaining traits, RF led in VOC and HOL, XGB in ORG, and Fanar (5) in DEV and MEC." |
| Q69 | 9 | output_form | "Encoder-based models excel in prompt-specific tasks, approaching the IAA (Table 4), which indicates a close reach to the human performance." |
| Q70 | 9 | output_form | "AraBERT exhibits the best performance overall in the prompt-specific setup with an average QWK performance of 0.74." |
| Q71 | 9 | output_form | "However, its cross-prompt performance drops significantly (average QWK: 0.549), underscoring its ability to capture prompt-dependent patterns rather than generalizable features." |
| Q72 | 9 | input_ontology | "We note that the applicability of the prompt-specific setup is relatively limited due to reliance on target prompt essays that are labeled, which is often unavailable in practice." |
| Q73 | 9 | output_form | "In the cross-prompt setup, while MOOSE achieves the highest average performance (average QWK: 0.597), we observe that classical FB models (XGB) remain remarkably competitive." |
| Q74 | 9 | output_form | "This confirms that handcrafted features capture prompt-independent linguistic properties that generalize better in the more challenging and realistic cross-prompt setup than some standard encoders." |
| Q75 | 9 | output_form | "LLMs, specifically Fanar and R7B with few shots, exhibit consistent performance across both setups, indicating they capture general scoring criteria." |
| Q76 | 9 | output_form | "Their relative underperformance in prompt-specific tasks reflects their limited ability to exploit prompt-dependent patterns without fine-tuning." |
| Q77 | 9 | input_ontology | "Overall, the findings of the benchmarking experiments above highlight the need to prioritize future research on cross-prompt AES, which is practically closer to the real world, while best models are still far from human performance." |
| Q78 | 9 | input_content | "While research on automated scoring of English essays began more than 55 years ago, Arabic essay scoring is hindered by the lack of data resources." |
| Q79 | 9 | input_content | "To bridge this gap, this paper introduced LAILA, the first large-scale publicly available dataset for Arabic AES." |
| Q80 | 9 | input_content | "The dataset comprises 7,859 essays written on 8 different prompts by 4,372 high school students, and provides annotations for 7 writing traits as well as a holistic score with substantial inter-annotator agreement." |
| Q81 | 9 | input_content | "This makes it a comprehensive and reliable resource for training models and evaluating writing quality of Arabic essays." |
| Q82 | 9 | output_content | "For reproducibility, we detailed the data collection and annotation process." |
| Q83 | 9 | output_form | "We also benchmarked LAILA using SOTA Arabic and English AES models in both prompt-specific and cross-prompt settings, showing strong baselines for future research." |
| Q84 | 9 | output_content | "We heartily thank our dedicated annotators for their contributions and express our gratitude to Qatar University Testing Center, the Ministry of Education and Higher Education in Qatar (the Arabic Section of the Department Of Educational Supervision in particular), participating schools, and students for making this work possible." |
| Q85 | 9 | output_content | "We also acknowledge the support of Advanced Group for Information Technology (AGI) for providing access to the platform, Assessment Gourmet, which was used to manage and administer the annotation process." |
| Q86 | 9 | output_content | "This work was made possible by NPRP grant NPRP14S-0402-210127 from the Qatar Research Development and Innovation (QRDI) Council." |
| Q87 | 9 | input_content | "While LAILA represents a significant step forward for Arabic AES, it has notable limitations." |
| Q88 | 9 | input_content | "First, LAILA was collected from students in a single country, Qatar, and specific grade levels, grades 10 to 12, which may limit its generalizability to other Arabic-speaking populations due to diverse educational systems. However, this concern is partially mitigated by Qatar's large population of Arab expatriates, resulting in student participants representing a wide variety of Arabic dialects and backgrounds." |
| Q89 | 10 | input_ontology | "Second, LAILA includes only explanatory and persuasive writing prompts, limiting genre diversity and potentially affecting model robustness across other styles, such as narrative or descriptive writing." |
| Q90 | 10 | input_content | "Third, two of the prompts (Prompts 3 and 4) have fewer essays than the rest, which could introduce imbalance and lead to skewed performance in prompt-specific evaluations." |
| Q91 | 10 | output_ontology | "Fourth, the relevance trait is scored on a narrow scale from 0 to 2, which limits the granularity of evaluation and may cause QWK to underrepresent subtle differences in model predictions." |
| Q92 | 10 | input_form | "Fifth, with an average essay length of only 171 words, the dataset lacks extended writing samples, restricting the assessment of models on long-form academic tasks requiring more complex, extended compositions." |
| Q93 | 10 | output_form | "Finally, we acknowledge that the experimental results reported in Table 5 do not aim to exhaustively benchmark state-of-the-art AES models; rather, they serve as baseline performance for LAILA." |
| Q94 | 10 | input_content | "We emphasize that the primary contribution of this work lies in the construction and public release of a large-scale Arabic AES dataset, rather than in proposing novel AES model architectures." |
| Q95 | 10 | output_content | "The collection of LAILA received approval from an Institutional Review Board (IRB Number: QU-IRB 159/2024-EA) and was conducted with informed consent from both students and their legal guardians." |
| Q96 | 10 | input_content | "Essays were written under exam-style supervised conditions, with participation entirely voluntary and independent of students' academic evaluations or grades." |
| Q97 | 10 | input_form | "To protect participant privacy, all submissions were assigned pre-generated anonymous identifiers, and personally identifiable information was systematically removed during data cleaning." |
| Q98 | 10 | output_content | "Annotation was conducted on a platform that prevented annotators from accessing student identities or demographic information." |
| Q99 | 10 | input_content | "Essay prompts were carefully designed to be developmentally appropriate for the target age groups, culturally relevant to the Arabic-speaking context, and free of sensitive topics or potentially harmful content." |
| Q100 | 10 | input_content | "The dataset includes balanced gender representation and covers grades 10-12." |
| Q101 | 10 | output_content | "All annotators were qualified Arabic language educators who received fair compensation at or above local professional rates." |
| Q102 | 10 | output_content | "They completed structured training on annotation guidelines, and inter-annotator disagreements were resolved through systematic adjudication procedures." |
| Q103 | 10 | output_form | "The dataset will be released exclusively for research and educational purposes in Arabic automated essay scoring." |
| Q104 | 10 | output_form | "We explicitly prohibit its use for high-stakes educational decisions affecting individual students." |
| Q105 | 10 | output_form | "Users must commit to: (1) preventing re-identification attempts, (2) avoiding demographic profiling or inference, and (3) refraining from deployment in operational assessment contexts without independent validation." |
| Q106 | 10 | output_form | "We recommend that any system developed using LAILA undergo fairness auditing and stakeholder consultation before real-world application." |
| Q107 | 11 | input_ontology | "TAQEEM 2025: Overview of the first shared task for Arabic quality evaluation of essays in multi-dimensions." |
| Q108 | 11 | output_ontology | "QAES: First publicly-available trait-specific annotations for automated scoring of Arabic essays." |
| Q109 | 11 | input_content | "ZaQQ: A new Arabic dataset for automatic essay scoring via a novel human–ai collaborative framework." |
| Q110 | 11 | input_content | "The English language learner insight, proficiency and skills evaluation (ELLIPSE) corpus." |
| Q111 | 11 | input_content | "A large-scale corpus for assessing written argumentation: PERSUADE 2.0." |
| Q112 | 11 | input_content | "The MERLIN corpus: Learner language and the CEFR." |
| Q113 | 11 | input_content | "TOEFL11: A corpus of non-native English." |
| Q114 | 12 | output_content | "For annotating LAILA, we adopted the rubric from the Core Academic Skills Test (CAST), which is provided in Arabic, developed by the Qatar University Testing Center (QUTC)." |
| Q115 | 12 | output_ontology | "This rubric guided scoring across 7 writing traits: relevance (REL), organization (ORG), vocabulary (VOC), style (STY), development (DEV), mechanics (MEC), and grammar (GRA)." |
| Q116 | 12 | output_ontology | "An English-translated version of the CAST rubric is presented in Table 6." |
| Q117 | 13 | output_ontology | "Note: A score of 0 is assigned if the student does not attempt the task, provides a response that falls below the performance level described for score 1, or submits content that is not relevant to the topic of the given prompt." |
| Q118 | 13 | input_ontology | "Table 6: CAST Persuasive/Argumentative Writing Rubric - English Translation (Bashendy et al., 2024)." |
| Q119 | 14 | output_ontology | "Figure 4 presents the score distributions in LAILA across 8 distinct prompts (P1–P8) and 7 writing traits, including Relevance (REL), Organization (ORG), Vocabulary (VOC), Style (STY), Development (DEV), Mechanics (MEC), and Grammar (GRA), alongside a Holistic (HOL) score representing the sum of all individual traits." |
| Q120 | 14 | output_ontology | "All traits are rated on a scale of 0–5, except REL, which ranges from 0–2." |
| Q121 | 14 | output_form | "Overall, most traits approximate a normal distribution with comparable patterns across prompts, suggesting that essays' quality remains relatively stable regardless of the prompt topic." |
| Q122 | 14 | output_content | "However, variations emerge by prompt and trait." |
| Q123 | 14 | output_ontology | "For REL, distributions are consistently skewed toward score 2 (the highest) across all prompts, indicating that most students successfully addressed the assigned task and produced strongly relevant essays." |
| Q124 | 14 | input_content | "However, P1 and P5 display relatively higher frequencies at score 0, compared to other prompts, suggesting potential ambiguity in prompt wording that may have limited clear interpretation." |
| Q125 | 14 | input_ontology | "Notably, both P1 and P5 are explanatory prompts, which often allow greater flexibility in structure and content." |
| Q126 | 14 | input_content | "This openness may have led to varied interpretations among students and inconsistencies in alignment with the intended prompt focus." |
| Q127 | 14 | output_form | "The distribution of ORG scores varies across prompts but consistently peaks at score 3." |
| Q128 | 14 | output_form | "P2 exhibits a pronounced peak at 3, whereas P3 and P4 show a wider spread toward lower scores, suggesting a weaker organizational structure in these essays." |
| Q129 | 14 | output_form | "P5 and P6 display nearly identical, perfectly bell-shaped distributions, while P7 and P8 are skewed toward higher scores, reflecting stronger organization." |
| Q130 | 14 | output_form | "Similarly, the VOC and STY traits generally follow comparable patterns, clustering around scores 2–3 with a common peak at 3, indicating that these dimensions present moderate challenges for most students." |
| Q131 | 14 | output_form | "The DEV, MEC, and GRA traits exhibit broadly comparable distributions across all prompts, though with subtle variations." |
| Q132 | 14 | output_form | "The DEV trait shows distinct peaks at scores 2, 3, and 4, suggesting that" |
| Q133 | 15 | input_form | "Figure 5 presents the distribution of essay lengths (in words) across all prompts in LAILA dataset, which contains a total of 7,859 essays." |
| Q134 | 15 | input_form | "The data exhibits a unimodal pattern centered around an average essay length of 171 words, with the majority of essays concentrated between 90 and 210 words." |
| Q135 | 15 | input_form | "A pronounced peak occurs in the 150 to 180 word range, where the count reaches its highest at 1,065 essays." |
| Q136 | 15 | input_form | "Shorter essays are also represented, with 1,061 essays falling between 11 and 60 words." |
| Q137 | 15 | input_form | "Notably, the minimum observed length is 11 words, which results from the data cleaning step that excluded essays containing 10 words or fewer." |
| Q138 | 15 | input_form | "Beyond 420 words, the frequency drops sharply, with only a few essays exceeding 500 words, suggesting that longer essays are less common in the dataset." |
| Q139 | 15 | output_form | "In this section, we provide all the details of implementation and hyperparameter tuning for all the models used in the benchmarking experiments." |
| Q140 | 15 | output_form | "All experiments were conducted on two machines: one equipped with an NVIDIA RTX A6000 GPU, and another with two NVIDIA A10 GPUs." |
| Q141 | 15 | output_form | "For the feature-based (FB) models, the architectures and hyperparameter configurations were kept consistent across both the prompt-specific and cross-prompt setups." |
| Q142 | 15 | output_form | "We used the sklearn library for Linear Regression (LR) and Random Forest (RF) models, and the XGBoost library for the Extreme Gradient Boosting (XGB) model." |
| Q143 | 15 | output_form | "The Neural Network (NN) model followed the architecture described by Li and Ng (2024), consisting of two hidden layers with ReLU activations and a sigmoid output layer, implemented in PyTorch." |
| Q144 | 15 | output_form | "For the NN, the number of epochs was fixed at 50 with early stopping, setting patience to 7, and checkpointing the best epoch during hyperparameter tuning for final model training." |
| Q145 | 15 | output_form | "For all the FB models, feature selection was performed on the training set during hyperparameter tuning, with threshold values of [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], where 0 corresponds to using all features." |
| Q146 | 16 | input_ontology | "Motivated by the strong performance of the T5 model in prompt-specific English AES, we finetuned the AraT5 model using a similar setup to the ArTS model (Do et al., 2024)." |
| Q147 | 16 | output_ontology | "The AES task is formulated as a text generation problem, where the model predicts the trait scores sequentially." |
| Q148 | 16 | input_form | "The input to the model consisted of an instruction to score the essay along with the essay text, and the model was fine-tuned to generate the trait names followed by their corresponding scores." |
| Q149 | 16 | input_form | "The prediction order of the traits was aligned with the rubric to reflect the scoring order followed by human annotators." |
| Q150 | 16 | input_form | "Our setup differs from ArTS in data splitting: while their training and testing data included essays from all prompts (with a single model trained on all prompts), we adopted the conventional prompt-specific setup, training a separate model for each prompt using our predefined dataset splits." |
| Q151 | 16 | output_form | "For training, we used Seq2SeqTrainer from the transformers library." |
| Q152 | 16 | output_form | "For hyperparameter tuning, we explored the learning rates in the range [5e-5, 1e-4, 2e-4]." |
| Q153 | 16 | output_form | "Other hyperparameters followed the configuration of (Do et al., 2024), with a batch size of 4 and a maximum of 15 epochs." |
| Q154 | 16 | output_form | "Early stopping was applied based on the average QWK score on the development set." |
| Q155 | 16 | input_ontology | "AraBERT is used as a baseline for the prompt-specific and cross-prompt setups using the same architecture and hyperparameter search space." |
| Q156 | 16 | input_form | "The model is fine-tuned with a custom regression head and combined with handcrafted features for trait scoring." |
| Q157 | 16 | input_form | "The essay and prompt were provided as input to the encoder, with the max-pooled token representation concatenated with the handcrafted features." |
| Q158 | 16 | input_form | "The resulting vector was then fed into eight parallel regression heads, each corresponding" |
| Q159 | 17 | output_form | "Sigmoid activation is used at the output layer to produce values in the range [0, 1], which were subsequently rescaled to the appropriate range for each trait." |
| Q160 | 17 | output_form | "For hyperparameter tuning, the learning rates for the encoder layers and the regression head are tuned separately to better accommodate the larger dataset, with a weight decay of 0.01." |
| Q161 | 17 | output_form | "In addition, we tuned the number of trainable layers, with values of [2, 4, 8, all], where 'all' corresponds to training all encoder layers." |
| Q162 | 17 | output_form | "For the feature selection threshold, we used the same search space as that used with the FB models." |
| Q163 | 17 | input_form | "These configurations were considered better suited to the dataset, mitigating training instabilities." |
| Q164 | 17 | input_ontology | "For ProTACT, we used the official implementation released by the authors." |
| Q165 | 17 | input_form | "Essay representations were constructed using CNNs and LSTMs over Part-of-speech (POS) embeddings, while prompt representations combined POS and pre-trained GloVe embeddings." |
| Q166 | 17 | input_form | "A multi-head attention mechanism was applied to obtain prompt-aware essay representations, which were then concatenated with handcrafted features and passed through a linear layer for scoring." |
| Q167 | 17 | input_form | "The architecture was adapted for Arabic by replacing GloVe with AraVec embeddings (Mohammad et al., 2017)." |
| Q168 | 17 | input_form | "POS embeddings were extracted using Camel Tools." |
| Q169 | 17 | output_form | "For hyperparameter tuning, we adopted the same search spaces for learning rate and feature selection threshold as in the NN model, while additionally tuning the trait similarity loss threshold." |
| Q170 | 17 | output_form | "All other parameters were kept consistent with those reported in the original study, including embedding dimension, maximum essay length, maximum prompt length, LSTM units, self-attention heads, CNN filters, and kernel size." |
| Q171 | 17 | input_ontology | "For MOOSE, we used the official implementation released by the authors." |
| Q172 | 17 | input_form | "The architecture was adapted for Arabic by replacing BERT with AraBERT (Antoun et al., 2020)." |
| Q173 | 17 | input_form | "Specifically, in the preprocessing stage, AraBERTv02 was used only for tokenization and input encoding, while the finetuned model for the scoring task used AraBERTv01." |
| Q174 | 17 | output_form | "This design choice was guided by empirical validation: we experimented with using AraBERTv01 and AraBERTv02 consistently for both preprocessing and modeling, as well as with mixed configurations, and found that using AraBERTv02 for tokenization and input encoding while finetuning AraBERTv01 for scoring yielded the best performance on the development set, thus it was adopted." |
| Q175 | 17 | input_form | "For the incorporated features, We implemented the handcrafted features introduced by Sayed et al. (2025) for Arabic AES, without applying any feature selection step." |
| Q176 | 17 | output_form | "For hyperparameter tuning, the learning rate was tuned over the values 1e-4 and 2e-5, while all other parameters were kept consistent with those reported in the original study." |
| Q177 | 17 | output_form | "Training was performed with a batch size of 8 for a maximum of 14 epochs, and no early stopping was applied." |
| Q178 | 17 | input_content | "The selection of the LLMs was based on the Open Arabic LLM Leaderboard, where we selected" |
| Q179 | 18 | input_ontology | "The selected models are: Fanar, Command R7B Arabic, and ALLaM." |
| Q180 | 18 | input_ontology | "We evaluated the models under zero-shot and few-shot prompting." |
| Q181 | 18 | output_ontology | "In the zero-shot setting, the LLM is tasked with generating trait scores in JSON format, given the prompt text, essay, and trait rubrics." |
| Q182 | 18 | output_ontology | "The holistic score was computed as the sum of the individual trait scores." |
| Q183 | 18 | input_ontology | "In the few-shot setting, the rubric was omitted, as the meaning of the scores could be inferred from the examples." |
| Q184 | 18 | input_form | "The number of examples was fixed to 5, balancing scoring context with the context length limit (4096 tokens)." |
| Q185 | 18 | input_form | "When a prompt exceeded this limit, we iteratively removed examples until it fit." |
| Q186 | 18 | input_form | "Although Command-R7B supports a larger context length, we fixed the number of examples to 5 to ensure fair comparison across LLMs." |
| Q187 | 18 | input_ontology | "In the prompt-specific setup, few-shot examples are selected from the same prompt." |
| Q188 | 18 | input_ontology | "In the cross-prompt setup, examples are selected from different source prompts, ensuring that each comes from a distinct training prompt to expose the model to varied contexts." |
| Q189 | 18 | output_form | "To account for variability in example selection, each experiment was repeated three times with random seeds 1, 11, and 42, and we report the average performance across runs." |
| Q190 | 18 | output_form | "For all the LLM experiments, we used vLLM for inference with the outlines library to enforce the JSON output format." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://grokipedia.com/page/List_of_schools_in_Qatar |
| WEB-2 | https://link.springer.com/chapter/10.1007/978-981-97-9667-0_11 |
| WEB-3 | https://www.tutorchase.com/blog/the-education-system-in-qatar-explained |
| WEB-4 | https://consulting-haus.com/wp-content/uploads/2023/09/CH_Education_Sector-Overview_September-2023.pdf |
| WEB-5 | https://www.impact-se.org/middle-eastern-curriculum-reform-a-window-into-national-values/ |
| WEB-6 | https://www.moe.gov.sa/ar/education/studies/Documents/Education%20in%20Saudi%20Arabia.pdf |
| WEB-7 | https://wenr.wes.org/2017/05/education-in-lebanon |
| WEB-8 | https://en.wikipedia.org/wiki/Education_in_Lebanon |
| WEB-9 | https://www.researchgate.net/publication/267714826_Foreign_Language_Education_in_Lebanon_A_Context_of_Cultural_and_Curricular_Complexities |
| WEB-10 | https://aclanthology.org/2025.arabicnlp-sharedtasks.134/ |
| WEB-11 | https://www.mdpi.com/2306-5729/10/9/148 |
| WEB-12 | https://link.springer.com/article/10.1007/s10462-024-11017-5 |
| WEB-13 | https://www.researchgate.net/publication/343796441_Automated_students_arabic_essay_scoring_using_trained_neural_network_by_e-jaya_optimization_to_support_personalized_system_of_instruction |
| WEB-14 | https://www.researchgate.net/figure/Total-Number-of-Schools-in-Qatar-Primary-Intermediate-Secondary_fig1_369912994 |
| WEB-15 | https://play.google.com/store/apps/details?id=app.qeducation.edu.gov.qa |
| WEB-16 | https://www.mordorintelligence.com/industry-reports/qatar-e-learning-management-system-market |
| WEB-17 | https://www.tandfonline.com/doi/full/10.1080/2331186X.2024.2430865 |
| WEB-18 | https://awej.org/saudi-efl-learners-perceptions-of-using-artificial-intelligence-and-its-impact-on-their-writing-skills/ |
| WEB-19 | https://unesdoc.unesco.org/ark:/48223/pf0000386162 |
| WEB-20 | https://assurance.ncsa.gov.qa/en/privacy/law |
| WEB-21 | https://securiti.ai/qatar-personal-data-protection-law/ |
| WEB-22 | https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/qatar |
| WEB-23 | https://www.sciencedirect.com/science/article/abs/pii/S0306457319304935 |
| WEB-24 | https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1614673/full |
| WEB-25 | https://journals.sagepub.com/doi/10.1177/21582440251378375 |
| WEB-26 | https://arxiv.org/html/2503.17739v2 |

---

