## Deployment Context

**Use case:** Deployment scenario: A GPT-4 model is implemented in a one-on-one tutoring session, where its responses are augmented with a human tutor’s input. The tutor evaluates the pedagogical quality of the combined response, particularly in terms of how well it provides guidance. The goal is to assess whether the augmented GPT-4 responses are acceptable to the tutor.

Domain: Educational tutoring
Setting: Mobile application / enterprise software
**Target population:** High-end professional teacher teaching grade 1-8 in major metropolitan cities in India, such as Delhi and Mumbai, who is fluent in English.

# Validity Analysis: mrbench
**Target context:** Indian Metropolitan Grade 1–8 Mathematics Teachers (Delhi & Mumbai)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 4 | Minor gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 5 | Strong alignment | high |
| Output Ontology | 3 | Moderate gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form | 4 | Minor gaps | high |
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

MRBench is well-aligned with the deployment on input form (text/English) and input ontology (math mistake remediation, eight dimensions accepted by the user), but has serious validity concerns on input content and output content — both rated HIGH priority by the user. The benchmark's source dialogues reflect Western classroom dynamics with extended student verbalization and Socratic exchanges that the user explicitly identified as mismatched with Indian Grade 1–8 student behavior, and the ground-truth labels were produced by four CS-trained MBZUAI annotators with no required teaching experience and no documented Indian educator background, while the user expects systematic divergence in guidance-quality judgments. Output ontology raises a moderate concern: the eight dimensions are accepted, but DAMR's equal-weight aggregation does not reflect the deployment's prioritization of 'providing guidance,' and that dimension is operationalized in a Socratic-scaffolding frame that may misclassify direct-correction responses Indian teachers consider acceptable. Output form is structurally appropriate for the use case. Field-wide corroboration ([WEB-6], [WEB-10]) confirms these gaps are systemic rather than MRBench-specific.

## Practical Guidance

### What This Benchmark Measures

MRBench measures whether AI tutor responses to student math mistakes satisfy eight pedagogical criteria (active learning, goal adaptation, cognitive load, motivation, mistake identification, answer non-revelation, guidance, actionability, coherence, tone, human-likeness) under a Western-constructivist learning-sciences frame, scored as percentage-of-desired-label across a CS-trained annotator pool. For this deployment, it provides reasonably robust signal on Input Form and Input Ontology (the task is correctly scoped and the dimensions accepted), and useful signal on Output Form structure.

### Construct Depth

Construct depth is high for the scoped task (192 dialogues, 1,596 responses, dual annotation on a subsample, substantial inter-annotator agreement, factual-correctness gate on guidance) but the depth applies to a Western-default operationalization of pedagogical quality. The construct of 'Indian teacher acceptability of guidance quality' is undermeasured: the 'providing guidance' rubric is Socratic-leaning [Q17, Q23, Q24] and the annotator pool is non-Indian and non-teacher [Q31, Q32], so DAMR and AC scores cannot be interpreted as direct proxies for Indian teacher judgments without supplementation.

### What Else You Need

Three concrete supplements are needed: (1) IC — collect or synthesize Indian-classroom-style short-turn, deferential, procedure-heavy student dialogues to extend or replace the MRBench input pool; (2) OC — re-annotate a representative MRBench subsample with Delhi/Mumbai Grade 1–8 mathematics teachers stratified by board (CBSE/ICSE/State Board/IB) to quantify divergence and produce India-aligned gold labels; (3) OO — design a re-weighted DAMR that elevates 'providing guidance' (with a within-dimension direct-correction vs. Socratic-scaffolding distinction) to reflect the deployment's acceptability priority.

## Dimension Details

### Input Ontology — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
The benchmark scopes the input ontology tightly to student mistake remediation in mathematics across elementary and middle school content [Q1, Q117, Q144], and the elicitation confirmed that curriculum-agnostic math errors are sufficient and that the eight pedagogical dimensions are necessary and sufficient. The user explicitly accepted the benchmark's task scoping and dimension set, reducing concerns about category-level misalignment. Minor concerns remain because the taxonomy was derived iteratively in a Western-default learning sciences frame [Q15, Q16] with no documented Indian pedagogical input, but the user's acceptance of the dimensions makes this a low-priority gap for IO specifically.

**Strengths:**
- Task is tightly scoped to mistake remediation in mathematics, which directly matches the deployment's one-on-one math tutoring use case [Q1, Q111, Q117]
- Coverage spans both elementary (Bridge) and middle-school (MathDial) math, aligning with the Grade 1–8 deployment band [Q144, Q143]
- Eight pedagogical dimensions were validated as necessary and sufficient by the pilot study [Q132], and the user confirmed they are sufficient for this deployment

**Checklist:**

- **IO-1**: Required categories for the deployment are mistake-remediation tutor turns in Grade 1–8 mathematics, which the benchmark covers [Q1, Q144]. The user confirmed curriculum-agnostic math errors are sufficient, so NCERT/CBSE-specific categories are not strictly required. — _Sources: Q1, Q144_
- **IO-2**: No regionally-relevant categories are identified as missing by the user; the eight dimensions were accepted as necessary and sufficient. The taxonomy explicitly excluded grammaticality and empathy [Q131], which is consistent with the deployment's stated priorities. — _Sources: Q132, Q131_
- **IO-3**: No categories are flagged as irrelevant. All eight dimensions [Q17–Q29] map to deployment-relevant constructs, though 'encouraging active learning' and 'answer non-revelation' are weighted equally with 'providing guidance' despite the user identifying guidance as uniquely critical (an OO weighting concern, not an IO category-relevance concern). — _Sources: Q17, Q24_
- **IO-4**: No content-validity-harming category gaps identified at the ontology level for this deployment, given the user's explicit acceptance of the eight-dimension framework. — _Sources: Q132_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we propose a unified evaluation taxonomy with eight pedagogical dimensions based on key learning sciences principles, which is designed to assess the pedagogical value of LLM-powered AI tutor responses grounded in student mistakes or confusions in the mathematical domain.' (p.1)
- [Q117] 'The proposed taxonomy primarily focuses on the task of the student mistake remediation in the domain of mathematics.' (p.9)
- [Q132] 'our validation pilot study (see Section 4.2) confirmed that the selected eight dimensions are both necessary and sufficient for evaluating tutor response quality in dialogues aimed at mistake remediation.' (p.12)
- [Q144] 'The problems covered in the Bridge dataset are at the elementary school level, whereas those in MathDial are at the middle school level.' (p.14)

</details>

**Information gaps:**
- Whether Indian-specific misconception categories (e.g., lakh/crore place-value errors, L1-interference errors) constitute distinct ontological categories rather than instances of existing categories — though user accepted curriculum-agnostic framing

**Requires expert verification:**
- Whether the user's acceptance of the eight dimensions generalizes across all CBSE/ICSE/State Board/IB sub-populations within Delhi and Mumbai

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Input content is the highest-priority concern alongside OC. Both source datasets reflect Western classroom dynamics: Bridge involves real Western tutor-student dialogues at elementary level [Q44], and MathDial uses an LLM acting as the student [Q48], further removing the data from authentic student behavior. The user explicitly confirmed that Indian Grade 1–8 students are briefer, more deferential, less likely to verbalize reasoning, and more procedurally focused than the Western-sourced conversations. Manual quality inspection [Q51] addressed quality but not cultural representativeness, and no documentation indicates Indian misconception types or interaction styles were considered. The corroborating WEIRD-population concern in the broader ITS literature [WEB-6] confirms this is a field-wide structural gap.

**Strengths:**
- Mathematical content itself is broadly familiar and curriculum-agnostic enough that the user accepted it as sufficient for deployment-relevant error scenarios [Q42, Q45, Q49]
- Manual inspection ensured data quality, even if not cultural representativeness [Q51]
- Both elementary and middle-school content provide range across the Grade 1–8 band [Q144]

**Checklist:**

- **IC-1**: Input dialogues are English-language and the deployment is English-medium, so no language transfer is required. However, the conversational register, turn length, and student verbalization patterns reflect Western classroom dynamics that the user identified as meaningfully mismatched with Indian metro classroom dynamics. — _Sources: Q41, Q48_
- **IC-2**: Culturally sensitive content (interaction style, deference patterns, exam-orientation) does NOT align with the target deployment culture. The user confirmed Indian students are 'more brief and deferential and less likely to verbalize reasoning.' MathDial's LLM-as-student [Q48] further distances it from authentic Indian student behavior. — _Sources: Q48, WEB-6_
- **IC-3**: Western-specific knowledge embedded in interaction style: extended Socratic exchanges, lengthy student verbalizations, and the constructivist exploration register characteristic of MathDial conversations [Q48, Q95] are not representative of typical Indian Grade 1–8 student behavior per user elicitation. — _Sources: Q48, Q95, WEB-10_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no documentation of regional annotator recruitment for content review. Would need stakeholder elicitation with Delhi/Mumbai teachers to identify specific culturally mismatched instances within the 192 dialogues.
- **IC-5**: Documented content issues: (a) student communication register mismatch (Western-verbose vs. Indian-brief); (b) LLM-as-student in MathDial removes authentic student variability [Q48]; (c) absence of L1-interference and rote-procedural error patterns common in Indian classrooms; (d) absence of exam-oriented misconception framings. — _Sources: Q48, Q51, WEB-6_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q41] 'We have compiled mistake remediation benchmark, MRBench, from the Bridge (Wang et al., 2024a) and MathDial (Macina et al., 2023) datasets.' (p.5)
- [Q44] 'The Bridge dataset (Wang et al., 2024a) comprises partial dialogue interactions between real human tutors and students at the elementary level' (p.5)
- [Q48] 'The dialogues in the MathDial dataset (Macina et al., 2023) consist of complete multi-turn conversations between a real human tutor and an LLM acting as a student' (p.5)
- [Q95] 'In contrast, for MathDial, the contexts are longer, the mistakes are grounded in reasoning, and the responses are more structured.' (p.8)
- [Q51] 'we manually inspected the data in order to retain only high-quality examples, which resulted in 132 instances for MRBench.' (p.6)

*Web sources:*
- [WEB-6] Comprehensive 2025 ITS evaluation review notes existing studies are 'conducted on small, homogeneous populations, primarily from WEIRD countries' — confirming the structural gap
- [WEB-10] MathTutorBench (EMNLP 2025) is also grounded in Western-default datasets with Socratic scaffolding norms, confirming no India-adapted alternative exists

</details>

**Information gaps:**
- No documented inventory of misconception types in the 192 dialogues, making it impossible to confirm whether Indian-relevant procedural error types appear
- No published taxonomy of common Indian Grade 1–8 mathematics misconceptions to compare against

**Requires expert verification:**
- Indian teacher review of sample MRBench dialogues to confirm extent of perceived realism mismatch
- Whether L1-interference error patterns common in Hindi/Marathi-medium contexts can be approximated by any subset of MRBench dialogues

---

### Input Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
The benchmark and deployment are both text-based, English-language, and use multi-turn dialogue inputs of varying length [Q133, Q141, Q147]. The deployment is mobile-first text interface in English, and the target population is English-fluent. No script, modality, or signal-distribution mismatch exists.

**Strengths:**
- Text-only English format directly matches the deployment's text-based mobile interface
- Multi-turn dialogue history representation [Q13, Q133] matches the deployment's conversational tutoring use case
- No multimodal or non-Latin script handling required

**Checklist:**

- **IF-1**: Signal distributions match: both source and deployment use text-encoded English multi-turn dialogue. Length is measured in characters with varying turn counts [Q141, Q147], compatible with mobile text interfaces. — _Sources: Q133, Q141, Q147_
- **IF-2**: Regional infrastructure supports text-based interaction; urban metro smartphone penetration is high and the user's target population uses English professionally. AI access disparity favors urban private metro schools [WEB-7]. — _Sources: WEB-7_
- **IF-3**: No domain-specific form differences identified. Both contexts use text dialogue inputs without requiring math-specific notation rendering beyond what is captured in source data. — _Sources: Q133_
- **IF-4**: No external-validity-harming form mismatches identified for this deployment. — _Sources: Q133_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q133] 'The prompt template used to generate responses from the seven considered LLMs for both the Bridge and MathDial datasets is shown in Figure 2.' (p.12)
- [Q141] 'It can be observed that the conversation history and response lengths from different LLMs and humans are generally shorter in the Bridge dataset compared to the MathDial dataset.' (p.14)
- [Q147] 'In all cases, length is estimated using the number of characters.' (p.14)

*Web sources:*
- [WEB-7] Urban Tier-1 city schools (Delhi/Mumbai) show approximately 62% higher AI resource access than rural schools, supporting infrastructure adequacy

</details>

---

### Output Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The eight-dimension ontology with three-tier labels [Q58, Q59] was accepted by the user as necessary and sufficient, which is a substantive endorsement. However, two structural concerns remain: (1) DAMR aggregates dimensions with equal analytical weight [Q64, Q65], which the user flagged as misaligned with their prioritization of 'providing guidance' as the dominant acceptability criterion; (2) the 'providing guidance' rubric is operationalized through Socratic scaffolding norms (hints, supporting questions, not revealing the answer immediately) [Q23, Q24], implicitly favoring Western constructivist tutoring. The user explicitly stated Indian teachers value direct correction and exam-readiness, raising the question of whether the 'providing guidance' label decisions encode the right decision rules. The factual-correctness gate for guidance [Q84] partially addresses the latter but not the Socratic vs. direct-correction distinction. The ontology also explicitly excludes downstream learning gains [Q119–Q121].

**Strengths:**
- Eight dimensions accepted by the user as necessary and sufficient
- Three-tier labeling system [Q58, Q59] gives more nuance than binary judgments
- Factual-correctness gate ensures only factually correct guidance counts toward DAMR [Q84], a deployment-relevant safeguard
- Independence-instructed annotation [Q30] preserves dimension-level signal that can be re-weighted post-hoc

**Checklist:**

- **OO-1**: Output label categories are pedagogically coherent and accepted by the user as relevant. The three-tier 'yes / to some extent / no' scheme [Q59] is reasonable for binary acceptability re-mapping. — _Sources: Q58, Q59_
- **OO-2**: No missing categories per user elicitation, but the ontology lacks a within-dimension distinction between Socratic-scaffolding guidance and direct-correction guidance. Both could receive 'yes' on 'providing guidance' [Q24] but be judged categorically different by Indian teachers. — _Sources: Q24_
- **OO-3**: The 'providing guidance' definition [Q24] and the 'encouraging active learning' definition emphasizing answer non-revelation and scaffolding [Q17] encode constructivist Western pedagogical values. The user identified this as a guidance-operationalization mismatch. Confirmed field-wide via [WEB-10]. — _Sources: Q17, Q23, Q24, WEB-10_
- **OO-4**: Stakeholder-driven taxonomy redesign is not strictly required (user accepted the dimensions) but dimension re-weighting and a within-dimension direct-vs-Socratic distinction would be high-value additions. — _Sources: Q64_
- **OO-5**: Documented issues: (a) equal-weight DAMR [Q64, Q67] does not reflect deployment priority on 'providing guidance'; (b) Socratic-default guidance operationalization [Q17, Q23, Q24] may not align with Indian direct-correction norms; (c) ontology excludes downstream learning gains [Q120, Q121], limiting outcome validity. — _Sources: Q64, Q120, Q121, WEB-6_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q24] 'In addition to not revealing the answer immediately, a good tutor response should provide the student with relevant and helpful guidance, such as a hint, an explanation, or a supporting question.' (p.4)
- [Q23] 'a good tutor strategy is not to reveal the answer to the student immediately but rather provide helpful guidance.' (p.4)
- [Q58] 'Each dimension was annotated using a three-tier labeling system' (p.6)
- [Q64] 'Desired Annotation Match Rate (DAMR): This metric quantifies the percentage of responses from each human or LLM-based tutor that received the desired annotation labels.' (p.6)
- [Q84] 'we consider only factually correct guidance as useful' (p.8)
- [Q120] 'However, one of the limitations is that it does not consider the tutoring dialogues' impact on the overall student learning.' (p.9)

*Web sources:*
- [WEB-10] MathTutorBench (EMNLP 2025) similarly defines tutoring quality around withholding answers and Socratic questioning, confirming Western-constructivist default is field-wide
- [WEB-6] WEIRD-population bias in ITS literature corroborates that ontologies in this space encode non-regional pedagogical assumptions

</details>

**Information gaps:**
- Whether the 'providing guidance' rubric, as operationalized in annotator guidelines (Table 4 referenced via Q128), explicitly rewards Socratic forms over direct-correction forms — paper text suggests yes via Q17/Q23/Q24 but full rubric language not in registry

**Requires expert verification:**
- Whether Indian teachers, given the same three-tier labels, would assign the same 'desired' label to a direct-correction response that does NOT scaffold via questioning

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
OC is the joint highest-priority concern. The annotation team comprised four CS post-graduates at MBZUAI in Abu Dhabi [Q6, Q31] with no required teaching experience [Q32], no documented South Asian educational expertise, and no documented familiarity with CBSE/NCERT pedagogy or exam-oriented correction norms. The user explicitly expects systematic differences between Indian teachers' guidance-quality judgments and the MBZUAI annotator pool's. While inter-annotator agreement was substantial within the team (Fleiss kappa 0.65, Cohen kappa 0.71) [Q39, Q61], this is internal homogeneity, not cross-cultural validity. LLM critics performed unreliably [Q107], so they cannot substitute for re-annotation. The WEIRD-population bias in ITS literature [WEB-6] corroborates that no India-specific educator annotation of AI tutor quality exists. Aggregation methods (DAMR) average across the four annotators, potentially erasing minority pedagogical perspectives even within the existing team.

**Strengths:**
- Rigorous training protocol with two-phase pilot, interactive documents, oral instructions, and structured quiz [Q34, Q35, Q135–Q137]
- In-house annotation avoiding crowdsourcing, supporting consistency [Q33]
- Substantial inter-annotator agreement within the team [Q39, Q61]
- Annotators proficient in English [Q31], matching the deployment evaluation language

**Checklist:**

- **OC-1**: Ground truth labels do NOT reflect Indian regional stakeholder perspectives. Annotators are CS-trained, MBZUAI-affiliated [Q6, Q31] with no documented Indian educator background; the user expects systematic divergence on guidance quality, exam-orientation, and direct-correction norms. — _Sources: Q6, Q31, Q32, WEB-6_
- **OC-2**: Significant disagreement is expected between original annotators and the Indian teacher target population. The user explicitly stated Indian teachers value 'more direct correction, exam-readiness framing, and teacher-directed pedagogy over Socratic probing,' which directly conflicts with the constructivist priors implicit in the original labels [Q17, Q23]. — _Sources: Q31, Q32, WEB-6_
- **OC-3**: Documented annotator demographics: four CS post-graduates, two male and two female, English-proficient, MBZUAI-affiliated [Q6, Q31]. Notably absent: teaching experience [Q32 explicitly waives this], regional/cultural background, board familiarity. No formal Datasheet/Data Statement is documented. — _Sources: Q6, Q31, Q32_
- **OC-4**: Re-annotation by representative Indian Grade 1–8 mathematics teachers is strongly recommended for deployment validity. No such re-annotation has been performed in published literature [WEB-6]. — _Sources: WEB-6, WEB-10_
- **OC-5**: Aggregation: DAMR is computed as percentage receiving desired label across annotators [Q64]; with 40 of 192 instances dual-annotated [Q57], minority perspectives among the four homogeneous annotators are likely already smoothed. For Indian-teacher re-annotation, aggregation choices would need to handle potential within-Indian-teacher heterogeneity (CBSE vs. ICSE vs. State Board vs. IB). — _Sources: Q57, Q64_
- **OC-6**: Documented label issues: (a) annotator pool culturally homogeneous and non-Indian; (b) no teaching experience required, so labels reflect 'user' rather than 'teacher' perspectives [Q32]; (c) LLM critics unreliable as substitutes [Q107–Q109]; (d) systematic divergence on guidance quality is expected per user elicitation. — _Sources: Q32, Q107, Q108, Q109_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q6] 'Mohamed bin Zayed University of Artificial Intelligence, Abu Dhabi, UAE.' (p.1)
- [Q31] 'The annotation team consisted of two male and two female annotators, with all four annotators holding at least a post-graduate degree in Computer Science and being proficient in English.' (p.5)
- [Q32] 'we do not require annotators to have direct teaching experience, as understanding of the mathematical tasks at the middle school level and being able to judge the responses from the perspective of a potential user of such AI tutors (or a student), rather than specifically a teacher, is sufficient.' (p.5)
- [Q39] 'we computed Fleiss' kappa value, which for this annotation experiment equals 0.65, indicating substantial agreement.' (p.5)
- [Q61] 'The annotators reached an average Cohen's kappa score of 0.71' (p.6)
- [Q107] 'most of the correlation scores are negative (except for the human-likeness dimension), indicating that the annotations from the LLMs are unreliable for the challenging pedagogical dimensions.' (p.8)
- [Q68] 'We consider human-based evaluations as gold standard.' (p.7)

*Web sources:*
- [WEB-6] 2025 ITS evaluation review confirms existing studies use 'small, homogeneous populations, primarily from WEIRD countries' — corroborating the annotator representativeness gap
- [WEB-10] MathTutorBench also relies on Western-default annotation; no India-adapted educator annotation exists in the field

</details>

**Information gaps:**
- Magnitude of expected Indian-teacher vs. MBZUAI-annotator disagreement is not empirically measured; only directionally indicated by user elicitation
- Whether dimension-level disagreement concentrates on 'providing guidance' as predicted, or also affects mistake identification, actionability, and tone

**Requires expert verification:**
- Indian Grade 1–8 math teacher re-annotation of a representative MRBench subsample to quantify divergence
- Within-Indian-teacher agreement across CBSE/ICSE/Maharashtra State Board/IB sub-populations

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output form is categorical three-tier labels per dimension aggregated into DAMR percentages and AC correlation scores [Q64, Q65, Q66, Q138], well-suited to the deployment's binary acceptability judgments. The form itself is appropriate; the only concern is structural — the equal-weight DAMR aggregate [Q67, Q149, Q150] does not surface the user's prioritization of 'providing guidance,' so the headline score cannot be used directly as a deployment validity proxy without re-weighting. This is an aggregation/reporting concern more than a modality mismatch.

**Strengths:**
- Categorical labels and percentage scores match the deployment's binary acceptability use case
- Per-dimension reporting [Q67, Q149, Q150] preserves signal for downstream re-weighting
- Separate DAMR scores for Bridge and MathDial subsets [Q149, Q150] support stratified analysis by complexity
- Rejection of NLG metrics [Q4, Q7, Q8, Q9, Q10] reflects appropriate concern with pedagogical-construct validity

**Checklist:**

- **OF-1**: Expected output modality (categorical labels and aggregate percentages) matches regional deployment needs for teacher acceptability judgments. The deployment is text-based and the output form is scoring-based, with no modality mismatch. — _Sources: Q64, Q67_
- **OF-2**: Not applicable — no speech-based output is required by the deployment. — _Sources: Q64_
- **OF-3**: Target population is English-fluent and professionally literate [user elicitation]; no accessibility concerns affecting output form. — _Sources: Q64_
- **OF-4**: No external-validity-harming form mismatches identified at the modality level. The structural concern is that equal-weight DAMR [Q64] does not surface deployment-relevant dimension prioritization, making direct use of the headline score for Indian-teacher acceptability prediction unreliable. — _Sources: Q64, Q67_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q64] 'Desired Annotation Match Rate (DAMR): This metric quantifies the percentage of responses from each human or LLM-based tutor that received the desired annotation labels.' (p.6)
- [Q66] 'Annotation Correlation (AC): This metric is based on Pearson's correlation' (p.6)
- [Q67] 'Table 3 shows DAMR scores for each LLM across all eight dimensions.' (p.7)
- [Q149] 'Pedagogical ability assessment of different LLMs using the DAMR scores (in %) across eight evaluation dimensions with human evaluation on the Bridge data.' (p.16)
- [Q4] 'General domain-agnostic natural language generation (NLG) metrics... are not well-suited for this context, as most of them fail to account for pedagogical values' (p.1)

</details>

**Information gaps:**
- Whether per-dimension DAMR scores are released at instance level (not just aggregate), enabling user-side re-weighting

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Source dialogues reflect Western classroom dynamics (extended student verbalization, Socratic exchanges, LLM-as-student in MathDial) that misrepresent Indian Grade 1–8 student behavior

**Recommendation:** Augment MRBench with a supplementary set of short-turn, deferential, procedure-focused student-tutor dialogues collected from Delhi/Mumbai classrooms or simulated under Indian-pedagogy guidelines, and report deployment metrics separately on this Indian subset

### Output Content ⚠

**Gap:** Ground-truth labels reflect four CS-trained MBZUAI annotators with no required teaching experience and no Indian educator representation; systematic divergence from Indian teachers is expected on guidance quality

**Recommendation:** Recruit a panel of 4–8 Delhi/Mumbai Grade 1–8 mathematics teachers (stratified across CBSE, ICSE, Maharashtra State Board, IB) to re-annotate at least the 192-instance benchmark on the eight dimensions, compute Indian-vs-original kappa, and use Indian-annotator labels as the deployment-validity gold standard

### Output Content ⚠

**Gap:** LLM critics (Prometheus2, Llama-3.1-8B) showed mostly negative correlation with human annotations [Q107] and cannot substitute for re-annotation

**Recommendation:** Do not rely on LLM-as-judge for deployment scoring; budget for human-in-the-loop annotation by Indian teachers and explicitly report DAMR/AC stratified by annotator cohort

### Input Ontology

**Gap:** While the user accepted the eight dimensions, the iteratively derived taxonomy [Q15, Q129] received no documented Indian pedagogical input, leaving residual risk that board-specific or exam-oriented sub-criteria are subsumed implicitly

**Recommendation:** Conduct a brief verification pilot with 2–3 Indian teachers from each board context (CBSE/ICSE/State/IB) to confirm dimension sufficiency at the sub-population level before scaling deployment

### Output Ontology

**Gap:** Equal-weight DAMR does not reflect the user's prioritization of 'providing guidance' as the dominant acceptability criterion, and the guidance rubric is operationalized in a Socratic-scaffolding frame

**Recommendation:** Define a deployment-specific weighted-DAMR in which 'providing guidance' carries dominant weight, and split the guidance dimension into two sub-labels — Socratic-scaffolding-guidance and direct-correction-guidance — both eligible for the desired label, calibrated against Indian teacher annotations

### Output Ontology

**Gap:** Ontology excludes downstream learning gains [Q120, Q121] and treats dimensions as orthogonal despite acknowledged interdependencies [Q30, Q116]

**Recommendation:** Pair MRBench-style turn-level scoring with a longitudinal learning-outcome evaluation (e.g., student post-conversation problem-solving) for deployment-relevant outcome validity, and report dimension-correlation diagnostics alongside DAMR

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "we propose a unified evaluation taxonomy with eight pedagogical dimensions based on key learning sciences principles, which is designed to assess the pedagogical value of LLM-powered AI tutor responses grounded in student mistakes or confusions in the mathematical domain." |
| Q2 | 1 | input_content | "We release MRBench – a new evaluation benchmark containing 192 conversations and 1,596 responses from seven state-of-the-art LLM-based and human tutors, providing gold annotations for eight pedagogical dimensions." |
| Q3 | 1 | output_form | "We assess reliability of the popular Prometheus2 and Llama-3.1-8B LLMs as evaluators and analyze each tutor's pedagogical abilities, highlighting which LLMs are good tutors and which ones are more suitable as question-answering systems." |
| Q4 | 1 | output_form | "General domain-agnostic natural language generation (NLG) metrics (Lin, 2004; Popovic´, 2017; Post, 2018; Gao et al., 2020; Liu et al., 2023) are not well-suited for this context, as most of them fail to account for pedagogical values and require gold references, which are often not available, especially in online interactions." |
| Q5 | 1 | input_ontology | "Specifically, for the student mistake remediation task, we need to assess complex pedagogical aspects and abilities of such systems, ensuring that they provide students with sufficient, helpful, and factually correct guidance and do not simply reveal answers when a student makes a mistake." |
| Q6 | 1 | output_content | "Kaushal Kumar Maurya, KV Aditya Srivatsa, Kseniia Petukhova and Ekaterina Kochmar. Mohamed bin Zayed University of Artificial Intelligence, Abu Dhabi, UAE." |
| Q7 | 2 | output_form | "General domain-agnostic natural language generation (NLG) metrics like BLEU (Papineni et al., 2002), BERTScore (Lin, 2004), DialogRPT (Gao et al., 2020), and so on have been used as proxies to measure the coherence and human-likeness of AI tutor responses." |
| Q8 | 2 | output_form | "However, these metrics do not account for pedagogical values (Jurenka et al., 2024; Liu et al., 2024) and often require a ground truth answer to evaluate matching responses." |
| Q9 | 2 | output_form | "For a given input dialogue, there can be multiple valid, pedagogically correct ground truth responses, making detection of the optimal answer non-deterministic (Tack and Piech, 2022; Al-Hossami et al., 2024)." |
| Q10 | 2 | output_form | "Additionally, these metrics can be easily manipulated; for instance, simple responses like "Hello" or "teacher:" (Baladón et al., 2023; Jurenka et al., 2024) can inflate scores." |
| Q11 | 2 | input_ontology | "In this section, we first briefly overview and discuss the limitations of the existing general-purpose NLG metrics and then turn to pedagogically-oriented approaches to evaluation." |
| Q12 | 3 | input_content | "In this work, we focus on educational dialogues between a student and a tutor in the mathematical domain. Specifically, the conversations are grounded in students' mistakes or confusions, and the AI tutor aims to respond in order to remediate such mistakes or confusions." |
| Q13 | 3 | input_ontology | "Formally, let's define the conversation history between a tutor and a student as H = {(T1, S1),(T2, S2), . . . ,(Tt, St)}, where Ti represents the i-th response from the tutor, and Si represents the i-th response from the student. Let Sk denote the student's most recent k utterances, where k ∈ [1, ..., t], containing a mistake or confusion. Then the objective of the tutor is to provide the most appropriate response Tt+1 to address this mistake or confusion." |
| Q14 | 3 | input_ontology | "The evaluation taxonomy detailed in Section 4 assesses the appropriateness of the Tt+1 response across eight key pedagogical dimensions." |
| Q15 | 3 | input_ontology | "In this section, we first present our approach, narrowing the evaluation taxonomy down to eight measurable dimensions aligned with key pedagogical strategies (Jurenka et al., 2024; Hennessy et al., 2016). These dimensions are most suitable for the student mistake remediation task and are based on the learning sciences principles." |
| Q16 | 3 | input_ontology | "We then dive into the details of each dimension and its relationship to previous research. An overview of the taxonomy is presented in Table 2." |
| Q17 | 3 | input_ontology | "Encourage active learning (Chi and Wylie, 2014; Oakley and Sejnowski, 2021): The tutor should encourage students to actively participate in the discussion and practice rather than passively receive information. The tutor can achieve this by not revealing the answer immediately and scaffolding guidance." |
| Q18 | 3 | input_ontology | "Adapt to students' goals and needs (King and South, 2017): The tutor should respond coherently by adapting to the current state and goals of the student's learning rather than following a pre-defined learning path. In the context of student mistake remediation, this happens when the tutor identifies the mistake, pinpoints its location, and responds coherently." |
| Q19 | 3 | input_ontology | "Manage cognitive load and enhance metacognitive skills (Mayer, 2002; Dehaene, 2020; Cohen et al., 2021): The tutor should present the information in a structured manner, with elaboration and examples in manageably small chunks that enable the student to generalize their learning skills beyond the current problem. For the task at hand, this can be achieved by providing appropriate guidance." |
| Q20 | 3 | input_ontology | "Foster motivation and stimulate curiosity (Keller, 1987; Patall et al., 2008): The tutor" |
| Q21 | 4 | input_ontology | "Since all dialogues in the dataset contain a mistake made by the student, a good-quality response from the tutor should include the relevant mistake identification." |
| Q22 | 4 | input_ontology | "A good tutor response should not only notify the student of the committed error but also point to its location in the answer and outline what the error is to help the student remediate it in their subsequent response." |
| Q23 | 4 | input_ontology | "Since most dialogues are relatively short and present contexts for the mistakes made early in the student's solution, a good tutor strategy is not to reveal the answer to the student immediately but rather provide helpful guidance." |
| Q24 | 4 | input_ontology | "In addition to not revealing the answer immediately, a good tutor response should provide the student with relevant and helpful guidance, such as a hint, an explanation, or a supporting question." |
| Q25 | 4 | input_ontology | "Once the guidance is provided to a student, it should be clear from a good tutor response what the student should do next; in other words, the tutor response should not be vague, unclear, or a conversation stopper." |
| Q26 | 4 | input_ontology | "We postulate that a high-quality tutor's response should be logically consistent with the student's previous responses." |
| Q27 | 4 | input_ontology | "In addition to addressing student mistakes, a good tutor should encourage them and avoid using toxic language, which is aligned with the care dimension in the evaluation schema of Wang et al. (2024a)." |
| Q28 | 4 | output_content | "This dimension is particularly critical for LLM-based AI tutors, as they often exhibit unpredictable behavior." |
| Q29 | 4 | input_ontology | "Effective tutoring requires that students feel a connection with the tutor, which is more likely when the tutor's responses appear human-like rather than robotic." |
| Q30 | 4 | output_ontology | "Although there are inherent interdependencies among the proposed dimensions of the taxonomy (e.g., a response that reveals the answer is less likely to be actionable, and vice versa), we explicitly instructed all annotators to treat each dimension as independent and orthogonal to minimize confounding factors and potential biases during the annotation process." |
| Q31 | 5 | output_content | "The annotation team consisted of two male and two female annotators, with all four annotators holding at least a post-graduate degree in Computer Science and being proficient in English." |
| Q32 | 5 | output_content | "We note that for this study, we do not require annotators to have direct teaching experience, as understanding of the mathematical tasks at the middle school level and being able to judge the responses from the perspective of a potential user of such AI tutors (or a student), rather than specifically a teacher, is sufficient." |
| Q33 | 5 | output_content | "To control the annotation workflow and ensure quality, we opted not to use public annotation outsourcing platforms such as Prolific or MTurk, which allowed us to implement rigorous training protocols and a robust validation mechanism for the annotations." |
| Q34 | 5 | output_content | "First, we provided all annotators with comprehensive training, including an interactive training document (see Section C for more details) and oral instructions." |
| Q35 | 5 | output_content | "Following this, we conducted validation pilot study to evaluate the annotation quality and the annotators' understanding of the instructions before rolling out the large-scale human evaluation detailed in Section 5.2." |
| Q36 | 5 | output_content | "In this validation pilot study, all four annotators iteratively reviewed the annotation scheme and guidelines." |
| Q37 | 5 | output_content | "Each annotator also independently labeled the same eight randomly sampled dialogues – four from each of the two datasets (Bridge and MathDial) – across the eight dimensions of the evaluation taxonomy." |
| Q38 | 5 | output_content | "Given that each dialogue contained multiple responses from both LLMs and humans, and each response was annotated across eight evaluation dimensions, this resulted in a total of 544 annotations per annotator." |
| Q39 | 5 | output_content | "To measure inter-annotator agreement, we computed Fleiss' kappa value, which for this annotation experiment equals 0.65, indicating substantial agreement." |
| Q40 | 5 | input_ontology | "None of the annotators identified any additional or redundant dimensions necessary for student mistake remediation." |
| Q41 | 5 | input_content | "We have compiled mistake remediation benchmark, MRBench, from the Bridge (Wang et al., 2024a) and MathDial (Macina et al., 2023) datasets." |
| Q42 | 5 | input_content | "Each instance in both datasets comprises educational dialogue interactions between students and tutors within the mathematical domain." |
| Q43 | 5 | input_content | "These interactions are specifically anchored in the students' errors or misconceptions, accompanied by the subsequent human tutor response, which aims to remediate the mistake or confusion." |
| Q44 | 5 | input_content | "The Bridge dataset (Wang et al., 2024a) comprises partial dialogue interactions between real human tutors and students at the elementary level, featuring two distinct human tutor responses (novice and expert)." |
| Q45 | 5 | input_content | "The dialogue context is typically short (few turns) and predominantly focused on fundamental mathematical concepts, including operations such as multiplication, addition, and so on." |
| Q46 | 5 | input_content | "The original dataset consists of a total of 700 dialogues; we filtered 60 high-quality instances for MRBench." |
| Q47 | 5 | input_content | "Among the various criteria for selecting high-quality dialogues, the key one was that the student's last utterance (or last few utterances) should exhibit an error or confusion." |
| Q48 | 5 | input_content | "The dialogues in the MathDial dataset (Macina et al., 2023) consist of complete multi-turn conversations between a real human tutor and an LLM acting as a student, where the tutor aims to remediate the student's mistakes." |
| Q49 | 5 | input_content | "Specifically, these conversations are grounded in middle school-level mathematical reasoning questions." |
| Q50 | 5 | input_form | "To match the format of Bridge (partial conversations with the last few student's utterances exhibiting a mistake or confusion), we prepared the dataset by terminating a conversation where the student makes a mistake and considering the next tutor response as the expert tutor response (there are no associated novice" |
| Q51 | 6 | input_content | "To further ensure the reliability of our benchmark, we manually inspected the data in order to retain only high-quality examples, which resulted in 132 instances for MRBench." |
| Q52 | 6 | input_content | "Next, for the 192 instances in MRBench (60 from Bridge and 132 from MathDial), we generated appropriate subsequent responses based on the conversation history and the last utterance, which contained confusions or mistakes, using seven state-of-the-art LLMs." |
| Q53 | 6 | input_ontology | "We consider state-of-the-art LLMs of various sizes and capabilities, including: GPT-4 (Achiam et al., 2023), Gemini (Reid et al., 2024), Sonnet (Anthropic, 2024), Mistral (Jiang et al., 2023), Llama-3.1-8B and Llama-3.1-405B (Dubey et al., 2024), and Phi3 (Abdin et al., 2024)." |
| Q54 | 6 | input_form | "Furthermore, each LLM has associated responses for 192 dialogues, resulting in a benchmark of 192 × 7 (7 LLM responses) + 192 × 1 (expert responses) + 60 × 1 (novice responses) = 1,596 responses, which makes the evaluation benchmark reasonably large while still manageable for human annotation described in Section 5.2." |
| Q55 | 6 | output_content | "Four trained annotators (see Section 4.2) annotated MRBench using the validated taxonomy." |
| Q56 | 6 | output_content | "Each annotator was asked to annotate human and LLM-based tutor responses across 8 dimensions of the taxonomy in the context of 48 dialogues." |
| Q57 | 6 | output_content | "A total of 192 instances were annotated, with 40 of those annotated independently by two annotators (10 instances from Bridge and 30 from MathDial) allowing us to calculate pairwise inter-annotator agreement." |
| Q58 | 6 | output_ontology | "Each dimension was annotated using a three-tier labeling system (see Figure 1 and Table 4)." |
| Q59 | 6 | output_ontology | "For instance, the 'mistake identification' dimension employed the following labels: (i) yes, (ii) to some extent, and (iii) no." |
| Q60 | 6 | output_content | "Annotators were instructed to assign 'yes' if the tutor accurately identified the mistake, 'no' if the mistake was missed, and 'to some extent' when there was ambiguity or uncertainty in the mistake identification." |
| Q61 | 6 | output_content | "The annotators reached an average Cohen's kappa score of 0.71, which indicates substantial inter-annotator agreement (McHugh, 2012)." |
| Q62 | 6 | output_form | "We used Prometheus2 (Kim et al., 2024) because: (i) it was specifically trained as an evaluator using reinforcement learning with human feedback (RLHF), (ii) it has a high correlation with human annotations and GPT-4, and (iii) it does not belong to any of the LLM families considered as AI tutors in our framework." |
| Q63 | 6 | output_form | "In addition, we also used Llama-3.1-8B as a lightweight LLM to assess the reliability of smaller models that were not fine-tuned for evaluation objectives as a critic." |
| Q64 | 6 | output_form | "We utilize two key metrics to quantitatively assess the pedagogical effectiveness of LLMs and for comparative analysis: (1) Desired Annotation Match Rate (DAMR): This metric quantifies the percentage of responses from each human or LLM-based tutor that received the desired annotation labels." |
| Q65 | 6 | output_form | "The desired labels for each dimension are detailed in Table 2." |
| Q66 | 6 | output_form | "(2) Annotation Correlation (AC): This metric is based on Pearson's correlation (Sedgwick, 2012), and it estimates the correlation between LLM-generated and human annotations (Kim et al., 2024), allowing us to assess the reliability of LLMs as evaluators in the context of student mistake remediation." |
| Q67 | 7 | output_form | "Table 3 shows DAMR scores for each LLM across all eight dimensions." |
| Q68 | 7 | output_content | "We consider human-based evaluations as gold standard." |
| Q69 | 7 | output_form | "Both these LLMs perform well in identifying students' mistakes and their exact location, with Llama-3.1-405B having a slight edge as GPT-4 reveals the answer approximately 47% of the time, making its responses less actionable and impacting student's learning experience." |
| Q70 | 7 | output_ontology | "This shows that GPT-4 is a good question-answering system but a relatively poor tutor." |
| Q71 | 7 | output_form | "Among these three LLMs, Gemini performs the worst as its responses are often incoherent, while also achieving low scores for mistake identification and exact location." |
| Q72 | 7 | output_form | "Phi3 is the worst-performing LLM model in this context, with the lowest score for coherence, suggesting that the responses from Phi3 are often irrelevant to the conversation context, as well as overall low scores in other dimensions." |
| Q73 | 7 | output_content | "This underscores the model's inadequate capacity for contextual understanding and semantic alignment in educational dialogues considered in this study." |
| Q74 | 7 | output_form | "In the few cases where Phi3 demonstrates some competence, it frequently reveals the answer, reflecting more of a question-answer system than a pedagogical tutor behavior." |
| Q75 | 7 | output_form | "Moreover, its outputs tend to be robotic, template-based and lack the nuance expected in human responses." |
| Q76 | 7 | output_form | "In contrast, despite having fewer parameters, Llama-3.1-8B demonstrates reasonable performance, albeit still below that of larger LLMs." |
| Q77 | 7 | output_form | "Specifically, its responses are coherent, strategically avoid immediate answer revelation, robustly identify and rectify mistakes, and exhibit human-like behavior, as evidenced by the DAMR scores." |
| Q78 | 7 | output_form | "We also investigated the pedagogical value of human responses for both Novice and Expert." |
| Q79 | 7 | output_form | "It can be observed that Novice responses do not have a high score for guidance and are poor in terms of actionability (DAMR score of 1.67)." |
| Q80 | 7 | output_form | "Furthermore, the responses are generally short and ambiguous, such as "this is a good try," which leads to lower scores for mistake identification and location." |
| Q81 | 7 | output_form | "At the same time, they often do not reveal the answer." |
| Q82 | 7 | input_content | "*For the Novice, we have considered only 60 dialogues from the Bridge dataset." |
| Q83 | 7 | output_form | "The DAMR scores for Novice are reported on these 60 instances, while for Expert and all LLMs, all 192 instances were considered." |
| Q84 | 8 | output_ontology | "Can a tutor achieve a higher DAMR score for actionability while receiving a lower score for providing guidance? This is possible since we consider only factually correct guidance as useful (see Table 4)." |
| Q85 | 8 | output_ontology | "At the same time, even incorrect or incomplete guidance can lead to certain actions on the part of the student and can foster their curiosity, thus providing them with learning opportunities." |
| Q86 | 8 | output_ontology | "This further demonstrates the need to treat the dimensions as independent." |
| Q87 | 8 | output_content | "In terms of the other qualities of the Expert responses, they do not normally reveal the answer and tend to include scaffolding; however, there are a small number of instances where they failed to identify the mistake or its location." |
| Q88 | 8 | output_content | "Overall, we conclude that human responses from Expert are significantly better than Novice." |
| Q89 | 8 | output_form | "Our findings on the Tutor Tone align with those of Wang et al. (2024a) – in task-oriented conversations, AI tutors tend to be more Neutral than Encouraging." |
| Q90 | 8 | output_ontology | "When we combine these two labels into "Non-offensive", the DAMR score reaches 100% as we observe no offensive responses from any LLMs or humans." |
| Q91 | 8 | output_form | "We observe high scores for most of the LLMs on human-likeness, which demonstrates their capability to generate human-like output with minimal or no grammatical and fluency mistakes, showing the timely nature of our study, which focuses more on in-depth semantic and pedagogical aspects of tutor responses rather than only on superficial attributes like grammaticality and fluency." |
| Q92 | 8 | input_content | "As discussed in Section 5.1, the conversational contexts in the Bridge dataset are typically very short (see Table 7) and the dialogues are grounded in elementary math operations, so most models are able to identify the mistakes and their locations." |
| Q93 | 8 | input_content | "However, they struggle to provide appropriate guidance without revealing the answer because the mistakes are generally related to quite basic operations like addition or multiplication, often in a one-step type of mathematical problems." |
| Q94 | 8 | output_form | "Still, models like GPT-4 and Llama-3.1-405B are able to offer some reasonable guidance." |
| Q95 | 8 | input_content | "In contrast, for MathDial, the contexts are longer, the mistakes are grounded in reasoning, and the responses are more structured." |
| Q96 | 8 | output_content | "Yet, many LLMs do not meet the expectations for each dimension of the taxonomy, as discussed earlier." |
| Q97 | 8 | input_content | "Combining both types of data in MRBench makes it both challenging and comprehensive." |
| Q98 | 8 | output_content | "In summary, all LLMs and even human tutors lack some pedagogical abilities required for effective tutoring." |
| Q99 | 8 | output_form | "While Llama-3.1-405B is the most effective, followed by Mistral and other state-of-the-art models, GPT-4 reveals the answer too quickly." |
| Q100 | 8 | output_form | "Gemini is less coherent and accurate, and Sonnet focuses on human-likeness and encouraging tone but is less effective in other dimensions." |
| Q101 | 8 | output_form | "Phi3 is the worst-performing model according to our analysis, as it fails to understand the context, while Llama-3.1-8B, despite being smaller, performs reasonably well." |
| Q102 | 8 | output_content | "Human responses are also not perfect – Novice responses are ambiguous and short, whereas Expert responses are more focused on actionability and less on other dimensions." |
| Q103 | 8 | input_ontology | "Overall, the proposed taxonomy precisely categorizes performance across 8 dimensions, reflecting the current state-of-the-art in AI tutors." |
| Q104 | 8 | output_content | "Our study demonstrates that there is a considerable room for improvement in the pedagogical abilities of AI tutors." |
| Q105 | 8 | output_content | "We also performed annotations using Prometheus2 and Llama-3.1-8B as critic LLMs." |
| Q106 | 8 | output_form | "The correlation scores with human annotations are presented in Appendix Tables 5 and 6, respectively." |
| Q107 | 8 | output_content | "Across both LLMs, it can be observed that most of the correlation scores are negative (except for the human-likeness dimension), indicating that the annotations from the LLMs are unreliable for the challenging pedagogical dimensions." |
| Q108 | 8 | output_content | "Prometheus2 is not trained on our taxonomy dimensions, except for the general human-likeness dimension, where the model shows slightly better correlations with positive scores." |
| Q109 | 8 | output_content | "We believe both LLMs have a limited understanding of rich pedagogical concepts, as they were not specifically trained on pedagogically rich datasets." |
| Q110 | 8 | output_content | "At the same time, we acknowledge that the experiments presented in this work are preliminary" |
| Q111 | 9 | input_ontology | "This paper presents the first effort to unify AI tutor evaluation for the student mistake remediation task in the mathematics domain." |
| Q112 | 9 | input_ontology | "Specifically, we propose an evaluation taxonomy with eight pedagogical dimensions based on the key learning sciences principles." |
| Q113 | 9 | output_content | "We also release the MRBench benchmark with seven state-of-the-art LLM-as-tutors responses, along with gold human annotations." |
| Q114 | 9 | output_form | "We also assess the feasibility of LLMs as evaluators in this context by correlating their judgements with human annotations, indicating that they are often unreliable." |
| Q115 | 9 | output_ontology | "This study evaluates tutor response quality across the proposed eight dimensions independently." |
| Q116 | 9 | output_ontology | "However, in practice, these dimensions may be inherently interrelated and may influence one another." |
| Q117 | 9 | input_ontology | "The proposed taxonomy primarily focuses on the task of the student mistake remediation in the domain of mathematics." |
| Q118 | 9 | input_ontology | "We acknowledge that the proposed taxonomy will need to be verified on and likely adapted if applied to other tasks such as concept learning, and to subjects other than mathematics." |
| Q119 | 9 | output_ontology | "The current taxonomy and annotation scheme focus on the appropriateness of the tutor responses." |
| Q120 | 9 | output_ontology | "However, one of the limitations is that it does not consider the tutoring dialogues' impact on the overall student learning." |
| Q121 | 9 | output_ontology | "Specifically, the annotation pertains to the individual tutor turns within educational dialogues, which restricts our understanding of broader implications on student learning processes and learning gains, typically observed after a conversation concludes." |
| Q122 | 9 | output_form | "In this study, we limit the LLM-based evaluation to two LLMs as critics, using the evaluation prompt presented in Figure 6." |
| Q123 | 9 | output_form | "The results obtained with these LLMs are not encouraging, as detailed in Section 6." |
| Q124 | 9 | output_content | "Although we do not foresee any ethical risks, we acknowledge that this work relies on the outputs from LLMs, and there are certain risks associated with such outputs in general since these models may generate responses that, although plausible, can be factually incorrect, nonsensical, or even offensive." |
| Q125 | 9 | output_content | "Of particular importance for the educational domain is the fact that hallucinations can misguide students and propagate biases." |
| Q126 | 10 | output_content | "This research is partially supported by Google through the Google Academic Research Award (GARA) 2024. We are grateful for their support. We also extend our gratitude to the campus supercomputing center at MBZUAI." |
| Q127 | 10 | input_ontology | "strongly believe that this study will help shed light on the current capabilities of LLMs in the context of educational dialogues, and the insights gained from this study may help mitigate issues related to the use of LLMs in the educational domain in the future." |
| Q128 | 12 | output_ontology | "The definitions, associated labels, and the desired labels for each dimension of the proposed taxonomy are provided in Table 4." |
| Q129 | 12 | input_ontology | "Through an iterative analysis of the taxonomy, we identify eight dimensions that comprehensively assess tutor response quality in the context of mistake remediation." |
| Q130 | 12 | input_ontology | "However, other educational settings, particularly those involving tutorial dialogues beyond mistake remediation, may require modifications, as discussed in the limitations section." |
| Q131 | 12 | input_ontology | "To establish a robust framework, we initially considered additional dimensions such as grammaticality and empathy, among others." |
| Q132 | 12 | output_content | "However, our validation pilot study (see Section 4.2) confirmed that the selected eight dimensions are both necessary and sufficient for evaluating tutor response quality in dialogues aimed at mistake remediation." |
| Q133 | 12 | input_form | "The prompt template used to generate responses from the seven considered LLMs for both the Bridge and MathDial datasets is shown in Figure 2." |
| Q134 | 12 | input_form | "The template is adapted from Wang et al. (2024a)." |
| Q135 | 13 | output_content | "As discussed in Section 5.2, prior to commencing large-scale human annotation, we implemented a two-phase interactive training and evaluation protocol and asked each annotator to undertake training." |
| Q136 | 13 | output_content | "Subsequently, we assessed annotators' understanding through a structured quiz, as is shown in a screenshot presented in Figure 5." |
| Q137 | 13 | output_content | "Additionally, we developed a comprehensive set of annotation guidelines, serving as a reference for annotators during the large-scale annotation process." |
| Q138 | 13 | output_form | "The correlation scores are calculated using Pearson's correlation (Sedgwick, 2012)." |
| Q139 | 13 | input_content | "*Only 60 dialogues were considered for Novice, whereas all 192 dialogues were considered for Expert and other tutors." |
| Q140 | 14 | input_content | "Table 7 shows the statistics for the Bridge, MathDial, and MRBench datasets." |
| Q141 | 14 | input_form | "It can be observed that the conversation history and response lengths from different LLMs and humans are generally shorter in the Bridge dataset compared to the MathDial dataset." |
| Q142 | 14 | input_form | "Additionally, the number of turns differs between them." |
| Q143 | 14 | input_ontology | "These aspects highlight that including both datasets in MRBench ensures diversity and provides for a good mix of easy and difficult mathematical problems, making the benchmark both comprehensive and challenging." |
| Q144 | 14 | input_ontology | "The problems covered in the Bridge dataset are at the elementary school level, whereas those in MathDial are at the middle school level." |
| Q145 | 14 | input_form | "The conversation topic is not provided in MathDial." |
| Q146 | 14 | output_content | "* indicates that the annotations are considered for 8 evaluation dimensions of the taxonomy." |
| Q147 | 14 | input_form | "In all cases, length is estimated using the number of characters." |
| Q148 | 15 | output_content | "The template is based on the insights drawn from the Prometheus2 model's official guidelines." |
| Q149 | 16 | output_form | "Pedagogical ability assessment of different LLMs using the DAMR scores (in %) across eight evaluation dimensions with human evaluation on the Bridge data." |
| Q150 | 16 | output_form | "Pedagogical ability assessment of different LLMs using the DAMR scores (in %) across eight evaluation dimensions with human evaluation on the MathDial data." |
| Q151 | 16 | input_content | "'-' indicates that DAMR scores for Novice are not available for MathDial data." |
| Q152 | 17 | output_content | "Figure 4: An example from the annotator training phase for the Mistake Identification dimension." |
| Q153 | 17 | output_content | "Figure 5: An example from the annotator testing phase for the Revealing of the Answer dimension." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.cbse.gov.in/cbsenew/teacher_qual_num.html |
| WEB-2 | https://www.superprof.co.in/blog/maths-tutoring-jobs-certificates/ |
| WEB-3 | https://testbook.com/dsssb-teacher/eligibility-criteria |
| WEB-4 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2234853 |
| WEB-5 | https://www.tiwariacademy.com/ncert-solutions/class-8/maths/ |
| WEB-6 | https://arxiv.org/html/2510.22581 |
| WEB-7 | https://educationforallinindia.com/ai-tutors-and-human-teachers-in-indian-education-implementation-framework-under-samagra-shiksha-abhiyan/ |
| WEB-8 | https://www.education.gov.in/sites/upload_files/mhrd/files/NEP_Final_English_0.pdf |
| WEB-9 | https://edunovations.com/currentaffairs/national/cbse-ai-curriculum-for-classes/ |
| WEB-10 | https://arxiv.org/abs/2502.18940 |
| WEB-11 | https://aclanthology.org/2025.emnlp-main.11/ |

---

