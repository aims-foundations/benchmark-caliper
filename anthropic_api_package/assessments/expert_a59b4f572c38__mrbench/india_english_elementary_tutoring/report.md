## Deployment Context

**Use case:** Deployment scenario: A GPT-4 model is implemented in a one-on-one tutoring session, where its responses are augmented with a human tutor’s input. We need to assesd whather Are the student stisfied with this newly GPT4 responses?

Domain: Educational tutoring
Setting: Mobile application / enterprise software
**Target population:** A student from a metropolitan city in India, in grades 1–8, who is fluent in English.

# Validity Analysis: mrbench
**Target context:** Metropolitan India – Grade 1–8 Mathematics Tutoring (English-medium)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 3 | Moderate gaps | high |
| **Average** | **2.3** | | |

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

MRBench is a well-constructed benchmark for Western/general-context English-language math mistake remediation, but it has serious validity gaps for deployment as an evaluation instrument for NCERT-aligned, English-medium tutoring of Grade 1–8 students in metropolitan India. The four HIGH/MODERATE-priority dimensions (Input Ontology, Input Content, Output Ontology, Output Content) all exhibit material misalignment: source data is Western [Q41, Q44, Q49] with no NCERT topics, Indian numerals, or rupee contexts; annotators are CS-educated MBZUAI affiliates [Q6, Q31] with no Indian educational expertise; the eight-dimension taxonomy collapses warmth register into a non-discriminative Non-offensive label [Q90] and is silent on cultural appropriateness — a deployment-required satisfaction condition (A4); and equal-weight DAMR [Q67] does not surface guidance/cultural-appropriateness prioritization. Input Form is a clean fit, and Output Form is moderately fit. Construct-irrelevant variance, content underrepresentation, and convergent-validity threats are all present and concrete.

## Practical Guidance

### What This Benchmark Measures

MRBench measures whether an AI tutor's English-language responses to mathematical mistake-remediation prompts satisfy eight pedagogical dimensions [Q15, Q16] as judged by a small group of CS-trained, non-Indian annotators on Western-sourced dialogues [Q41]. For the target deployment, the strongest signals it can provide are dimension-level evidence on factual mistake identification [Q21, Q22], answer non-revelation [Q23], factually correct guidance [Q84], coherence [Q26], and human-likeness [Q29] — properties largely transferable across cultural contexts. Input Form alignment is excellent (text + English + Latin script).

### Construct Depth

The benchmark probes pedagogical correctness at the level of single tutor turns [Q119], with author-acknowledged exclusion of downstream learning gains [Q120, Q121] and downplaying of dimension interdependencies [Q30, Q116]. The Tone dimension is non-discriminative by construction [Q90], so warmth-register evidence is essentially absent. Cultural appropriateness, NCERT-curriculum alignment, exam-step-marking acceptability, and Indian student-satisfaction proxies are not measured at all. Construct depth on Output Ontology and Output Content is therefore shallow relative to deployment needs.

### What Else You Need

A complete assessment requires: (1) re-annotation of MRBench, or a successor benchmark, by Indian K-8 math educators to surface convergent-validity gaps (Output Content); (2) authoring or sourcing NCERT-aligned, Indian-context dialogue instances with Indian student error patterns (Input Content + Input Ontology); (3) extending the taxonomy with cultural-appropriateness, warmth-tier, and Socratic-vs-direct-correction dimensions (Output Ontology); (4) a satisfaction-validation study linking benchmark scores to Indian student-satisfaction signals, since no such study exists [WEB-21]; (5) compliance review against DPDPA 2023 child-data provisions before any in-deployment data collection [WEB-15, WEB-17, WEB-18].

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
MRBench's input ontology is scoped to the well-defined task of student mistake remediation in mathematics [Q1, Q111, Q117], with elementary [Q44, Q144] and middle-school [Q49, Q144] coverage that nominally maps to the K-8 grade band. However, the taxonomy is derived from Western learning-sciences literature and Western source datasets [Q15, Q41], with no NCERT-aligned topic categories, no Indian numeral conventions (lakhs/crores), and no rupee-denominated problem categories — all explicitly required by the deployment (A1). The authors themselves caveat that the taxonomy 'will need to be verified on and likely adapted if applied to other tasks…and to subjects other than mathematics' [Q118]; while mathematics is in scope, the regional specialization to NCERT pedagogy is an analogous gap. No India-specific math tutoring benchmark exists in the public literature [WEB-20], confirming the gap is structural rather than addressable by porting.

**Strengths:**
- Task scope (mistake remediation in math) directly matches the deployment's primary use case [Q1, Q12]
- Grade band coverage (elementary + middle-school) [Q144] aligns with the Grade 1–8 target
- Eight-dimension pedagogical taxonomy iteratively validated [Q129, Q132] provides a principled construct space

**Checklist:**

- **IO-1**: Required categories include NCERT-aligned Grade 1–8 topics (place value with Indian grouping, lakhs/crores, rupee-denominated word problems, Indian-context applications such as cricket statistics, school fees, train timetables) and procedural-error subcategories arising from rote-learning artifacts. Confirmed by elicitation A1 and curriculum_and_pedagogy section citing [WEB-9, WEB-11]. — _Sources: WEB-9, WEB-11_
- **IO-2**: The benchmark omits NCERT topic categories, Indian numeral-naming conventions, rupee-context word problems, and rote-procedural error subtypes [Q41, Q44, Q49]. No India-specific math tutoring benchmark currently exists [WEB-20]. — _Sources: Q41, Q44, Q49, WEB-20_
- **IO-3**: The taxonomy itself (eight pedagogical dimensions [Q15, Q16]) is not regionally irrelevant in principle, but the implicit Socratic-scaffolding orientation [Q17, Q23] may encode pedagogical assumptions less salient in Indian exam-oriented, direct-correction tradition [WEB-11, WEB-12]. This is a partial concern rather than full irrelevance. — _Sources: Q17, Q23, WEB-11, WEB-12_
- **IO-4**: Content validity is harmed by under-representation of NCERT topic categories, Indian numeral conventions, and rote-procedural misconception types — all HIGH-priority for this deployment per IO weight. — _Sources: Q118, WEB-11, WEB-20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we propose a unified evaluation taxonomy with eight pedagogical dimensions based on key learning sciences principles, which is designed to assess the pedagogical value of LLM-powered AI tutor responses grounded in student mistakes or confusions in the mathematical domain.' (p.1)
- [Q41] 'We have compiled mistake remediation benchmark, MRBench, from the Bridge (Wang et al., 2024a) and MathDial (Macina et al., 2023) datasets.' (p.5)
- [Q118] 'We acknowledge that the proposed taxonomy will need to be verified on and likely adapted if applied to other tasks such as concept learning, and to subjects other than mathematics.' (p.9)
- [Q144] 'The problems covered in the Bridge dataset are at the elementary school level, whereas those in MathDial are at the middle school level.' (p.14)

*Web sources:*
- [WEB-9] NCERT curriculum defines the Grade 1–8 topic taxonomy required by the deployment
- [WEB-11] NCF 2023 explicitly identifies rote memorisation as a systemic challenge producing distinctive procedural-error typologies
- [WEB-20] VIRAASAT confirms no Indian-culture-specific math tutoring benchmark exists in published literature

</details>

**Information gaps:**
- No empirical mapping between MRBench's eight-dimension taxonomy and NCERT-aligned topic coverage
- No documented enumeration of rote-procedural misconception subcategories that would need to be added

**Requires expert verification:**
- Whether Indian primary-school math educators would identify additional taxonomy dimensions (e.g., exam-step-marking alignment) absent from the eight-dimension scheme
- Whether the Socratic-scaffolding orientation is treated as categorically distinct from direct-correction guidance by Indian teachers

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MRBench's input content is drawn entirely from two Western-sourced datasets: Bridge (real human tutors with elementary-level US students) [Q44, Q45] and MathDial (human tutor + LLM-as-student on middle-school reasoning) [Q48, Q49]. The deployment explicitly requires Indian everyday contexts (cricket, rupees, local markets, school fees) and prohibits culture-distant Western examples (A2). No documentation indicates any Indian-context word problems, Indian numeral conventions, or India-specific student error patterns in the source data. Additionally, MathDial replaces the student with an LLM [Q48], further distancing the conversation register from authentic Indian student behavior. This is a fundamental construct-irrelevant variance problem for the target deployment and the highest-priority dimension by elicitation weight.

**Strengths:**
- Manual quality inspection was applied during selection [Q51], so within-distribution quality is reasonable
- 192 instances spanning two difficulty levels [Q52, Q97] provides a non-trivial sample size for statistical analysis

**Checklist:**

- **IC-1**: Yes — deployment requires Indian-context word problems (cricket, rupees, local markets, NCERT-style scenarios) confirmed by A2 and curriculum_and_pedagogy section. The benchmark's source material does not provide this [Q41, Q44, Q49]. — _Sources: Q41, WEB-9_
- **IC-2**: Culturally sensitive content alignment is poor. Bridge and MathDial originate from Western educational contexts [Q41]; no India-relevant cultural framing is documented in either source. — _Sources: Q41, Q44, Q49_
- **IC-3**: Inputs likely embed Western-specific knowledge (US school scenarios, dollar-denominated problems, US arithmetic conventions). No India-specific instances are documented [Q44, Q49]. — _Sources: Q44, Q49_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotators reviewed the benchmark instances. To resolve, recruit Indian K-8 math educators to label each of the 192 instances for cultural-context appropriateness and NCERT-curriculum alignment.
- **IC-5**: Content validity is severely harmed: the test instances do not sample from the input distribution that the deployed system will encounter, since deployment-side problems will be NCERT-aligned and Indian-context-grounded. — _Sources: Q41, WEB-11_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q41] 'We have compiled mistake remediation benchmark, MRBench, from the Bridge (Wang et al., 2024a) and MathDial (Macina et al., 2023) datasets.' (p.5)
- [Q44] 'The Bridge dataset (Wang et al., 2024a) comprises partial dialogue interactions between real human tutors and students at the elementary level, featuring two distinct human tutor responses (novice and expert).' (p.5)
- [Q48] 'The dialogues in the MathDial dataset (Macina et al., 2023) consist of complete multi-turn conversations between a real human tutor and an LLM acting as a student, where the tutor aims to remediate the student's mistakes.' (p.5)
- [Q49] 'Specifically, these conversations are grounded in middle school-level mathematical reasoning questions.' (p.5)

*Web sources:*
- [WEB-9] NCERT curriculum defines the topic and word-problem context space required by the deployment
- [WEB-11] NCF 2023 documents rote-learning-driven error typologies absent from Western source data

</details>

**Information gaps:**
- No instance-level audit of Bridge/MathDial content for India-specific or India-incompatible cultural framings
- No documented L1-interference or Indian-numeral-convention error patterns in source datasets

**Requires expert verification:**
- Whether any subset of the 192 instances contains culturally neutral problem framings that could be retained without remediation
- Magnitude of communication-register mismatch between Bridge/MathDial student turns and authentic Indian Grade 1–8 student turns

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form is the strongest dimension for this deployment. The benchmark is text-based, English-only, multi-turn dialogue [Q133, Q134, Q141, Q142, Q147], which matches the deployment's English-medium, text-based mobile/enterprise-software channel. No script mismatch (Latin script throughout), no modality mismatch (no speech, image, or multilingual requirement), and English fluency is confirmed for the target population. The IF priority weight is LOWER, consistent with this assessment. A minor structural limitation is the absence of conversation topic metadata in MathDial [Q145], but this does not constitute a form mismatch.

**Strengths:**
- Text-only English format directly matches deployment channel and language
- Latin script alignment — no transliteration or non-Latin numeral handling required
- Multi-turn dialogue structure [Q141, Q142] is appropriate for tutoring-app interaction

**Checklist:**

- **IF-1**: Signal distributions match: text input in English in both benchmark [Q133, Q147] and deployment. Mobile-internet bandwidth in Indian metros is high (92.3% of mobile connections are 3G/4G/5G [WEB-8]; 97.6% urban mobile usage [WEB-6]). — _Sources: Q133, Q147, WEB-6, WEB-8_
- **IF-2**: Regional infrastructure supports the data form trivially — text-based dialogue requires no specialized capture; metro device penetration is high [WEB-6, WEB-7]. — _Sources: WEB-6, WEB-7_
- **IF-3**: Conversation length and turn-count distributions [Q141, Q142] may differ from authentic Indian-student dialogues (typically briefer per cultural_norms_notes), but this is a content/register concern rather than a form concern. — _Sources: Q141, Q142_
- **IF-4**: No material form mismatch threatens external validity. Minor limitation: no topic metadata in MathDial [Q145]. — _Sources: Q145_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q133] 'The prompt template used to generate responses from the seven considered LLMs for both the Bridge and MathDial datasets is shown in Figure 2.' (p.12)
- [Q141] 'It can be observed that the conversation history and response lengths from different LLMs and humans are generally shorter in the Bridge dataset compared to the MathDial dataset.' (p.14)
- [Q145] 'The conversation topic is not provided in MathDial.' (p.14)
- [Q147] 'In all cases, length is estimated using the number of characters.' (p.14)

*Web sources:*
- [WEB-6] Urban mobile usage 97.6% supports text-based mobile-app deployment
- [WEB-8] 92.3% of mobile connections are broadband-grade in India

</details>

**Information gaps:**
- Authentic turn-length distribution for Indian Grade 1–8 students in tutoring contexts is not empirically documented

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
MRBench's output ontology — eight pedagogical dimensions each with a three-tier label [Q58, Q59, Q128] — has structural validity gaps relative to the deployment's success criterion of student satisfaction conditional on cultural appropriateness (A4). The Tutor Tone dimension collapses Neutral and Encouraging into 'Non-offensive' [Q90], yielding 100% DAMR by construction — providing no discriminative signal on the warmth register the deployment treats as a necessary satisfaction condition. The taxonomy explicitly excludes downstream learning-gain measurement [Q119, Q120, Q121]. The factual-correctness gate on guidance [Q84] is preserved, which is useful, but the ontology encodes no distinction between Socratic scaffolding and direct-correction guidance — a categorical distinction Indian teachers would recognize given exam-step-marking culture [WEB-11, WEB-12]. Equal-weight DAMR [Q67, Q83] does not surface dimension-level prioritization. This is a HIGH-priority dimension by elicitation.

**Strengths:**
- Eight-dimension structure provides multi-faceted scoring rather than a single scalar [Q15, Q16]
- Factual-correctness gating on guidance [Q84] preserves a hard requirement aligned with Indian exam-step-marking expectations
- Three-tier labeling [Q58, Q59] permits 'to some extent' nuance rather than binary judgments

**Checklist:**

- **OO-1**: Eight pedagogical dimensions [Q15, Q16] partially overlap with regional acceptability criteria (mistake identification, guidance, actionability are clearly relevant). However, cultural appropriateness and warmth register are absent as discriminating categories — the Tone dimension collapses Neutral/Encouraging into Non-offensive [Q90], achieving 100% DAMR by construction. — _Sources: Q15, Q16, Q90_
- **OO-2**: Missing categories: (a) cultural appropriateness of framing; (b) exam-step-marking alignment / procedural step explicitness; (c) warmth register discriminator separating Encouraging from Neutral; (d) distinction between Socratic scaffolding and direct-correction guidance styles [WEB-11, WEB-12]. — _Sources: Q90, WEB-11, WEB-12_
- **OO-3**: The implicit privileging of non-revelation [Q23] and active-learning scaffolding [Q17] encodes a Socratic pedagogical preference that may not align with Indian direct-correction norms [WEB-11]. Equal-weight reporting [Q67] also assumes dimension parity not endorsed by the deployment (which prioritizes guidance and cultural appropriateness per A4). — _Sources: Q17, Q23, Q67, WEB-11_
- **OO-4**: Stakeholder-driven taxonomy redesign is warranted: at minimum, splitting the Tone dimension into discriminating warmth tiers and adding a cultural-appropriateness dimension would address core gaps. — _Sources: Q90_
- **OO-5**: Structural and content validity are both harmed: (a) Tone dimension is non-discriminative by construction [Q90]; (b) cultural appropriateness is unrepresented; (c) post-conversation outcomes are out of scope by author acknowledgment [Q119, Q120, Q121]. — _Sources: Q90, Q119, Q120, Q121_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q58] 'Each dimension was annotated using a three-tier labeling system (see Figure 1 and Table 4).' (p.6)
- [Q84] 'Can a tutor achieve a higher DAMR score for actionability while receiving a lower score for providing guidance? This is possible since we consider only factually correct guidance as useful (see Table 4).' (p.8)
- [Q90] 'When we combine these two labels into "Non-offensive", the DAMR score reaches 100% as we observe no offensive responses from any LLMs or humans.' (p.8)
- [Q119] 'The current taxonomy and annotation scheme focus on the appropriateness of the tutor responses.' (p.9)
- [Q120] 'However, one of the limitations is that it does not consider the tutoring dialogues' impact on the overall student learning.' (p.9)

*Web sources:*
- [WEB-11] NCF 2023 frames rote-learning culture in which direct correction is normalized — implying Socratic-non-revelation may be culturally non-default
- [WEB-12] NAS 2021 score trajectory grounds the procedural-error context in which step-marking is salient

</details>

**Information gaps:**
- No published study validates that the eight MRBench dimensions are necessary and sufficient for Indian-cohort student satisfaction
- No empirical weighting study for dimension importance under Indian exam-oriented pedagogy

**Requires expert verification:**
- Whether Indian teachers would split the Tone dimension into warmth tiers and how those tiers map to student satisfaction
- Whether direct correction is explicitly preferred or merely tolerated by Indian Grade 1–8 educators

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Ground-truth labels were produced by four annotators — two male, two female, all with at least a postgraduate CS degree, English-proficient [Q31] — affiliated with MBZUAI in Abu Dhabi [Q6]. The authors explicitly state teaching experience was not required [Q32], and there is no documented South Asian educational expertise, NCERT/CBSE familiarity, or Indian-educator participation. While inter-annotator agreement is substantial (Fleiss κ=0.65 in pilot [Q39]; Cohen κ=0.71 main [Q61]), this measures internal consistency among a culturally homogeneous group, not convergent validity with Indian stakeholder judgments. The deployment's success criterion is student satisfaction, with human tutors and student engagement as judges (A3, A4) — for whom cultural appropriateness is a necessary condition not represented in the annotator pool. LLM critics (Prometheus2, Llama-3.1-8B) showed mostly negative correlation with human annotators on pedagogical dimensions [Q107, Q108, Q109], so they do not provide a fallback. OC priority is MODERATE per elicitation, but combined with the absence of Indian raters, convergent and external validity are materially threatened.

**Strengths:**
- Transparent annotator demographics and qualifications documented [Q31]
- Two-phase pilot training with structured quiz [Q34, Q35, Q135, Q136, Q137] supports internal label consistency
- Substantial inter-annotator agreement (Cohen κ=0.71) [Q61] indicates the labeling scheme is operationalizable
- In-house annotation rather than crowdsourcing [Q33] supports quality control

**Checklist:**

- **OC-1**: Ground-truth labels do not reflect Indian regional stakeholder perspectives. Annotators are CS-educated MBZUAI affiliates [Q6, Q31] with no documented Indian educational expertise. — _Sources: Q6, Q31, Q32_
- **OC-2**: Disagreement on tone, warmth register, and cultural appropriateness is expected per A3 (partial alignment) and A4 (cultural appropriateness is a necessary satisfaction condition). Pedagogical-correctness dimensions (mistake identification, factual correctness) likely show smaller divergence. — _Sources: Q31, Q32_
- **OC-3**: Annotator demographics are documented at a basic level — gender, education, language proficiency [Q31] — but not nationality, cultural background, NCERT/CBSE familiarity, or teaching experience (which is explicitly stated to be not required [Q32]). — _Sources: Q31, Q32_
- **OC-4**: Re-annotation by representative Indian K-8 educators is strongly recommended; the joint inter-annotator agreement on the existing scheme would also need to be re-measured with Indian raters. — _Sources: WEB-20_
- **OC-5**: Aggregation methods are not documented in detail; only 40/192 instances were doubly annotated [Q57], so for the remaining 152 instances each label rests on a single annotator's judgment, providing limited resilience to individual annotator priors. — _Sources: Q57_
- **OC-6**: Convergent validity (vs. Indian stakeholder judgments) and external validity (generalization to Indian deployment) are both threatened. The labels reflect non-Indian pedagogical priors as a systematic source of variance. — _Sources: Q6, Q31, Q107_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q6] 'Kaushal Kumar Maurya, KV Aditya Srivatsa, Kseniia Petukhova and Ekaterina Kochmar. Mohamed bin Zayed University of Artificial Intelligence, Abu Dhabi, UAE.' (p.1)
- [Q31] 'The annotation team consisted of two male and two female annotators, with all four annotators holding at least a post-graduate degree in Computer Science and being proficient in English.' (p.5)
- [Q32] 'We note that for this study, we do not require annotators to have direct teaching experience…' (p.5)
- [Q61] 'The annotators reached an average Cohen's kappa score of 0.71, which indicates substantial inter-annotator agreement (McHugh, 2012).' (p.6)
- [Q107] 'Across both LLMs, it can be observed that most of the correlation scores are negative (except for the human-likeness dimension), indicating that the annotations from the LLMs are unreliable for the challenging pedagogical dimensions.' (p.8)

*Web sources:*
- [WEB-20] VIRAASAT confirms Indian cultural reasoning tasks require expert-curated Indian annotation; MRBench has no equivalent

</details>

**Information gaps:**
- Magnitude of annotation divergence between MBZUAI annotators and Indian K-8 math educators on the same instances
- Whether the 40 doubly-annotated instances are representative of the full 192

**Requires expert verification:**
- Re-annotation pilot by Indian K-8 math teachers on a sample of MRBench instances to quantify divergence
- Stakeholder identification of which of the eight dimensions exhibit greatest cross-cultural divergence

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The benchmark output form — categorical three-tier labels per dimension aggregated into DAMR percentages [Q64, Q65] and Pearson-based AC scores [Q66, Q138] — is well-suited to text-output evaluation and matches the deployment's text-based interaction. There is no modality mismatch. The primary structural concern is that equal-weight DAMR reporting [Q67, Q83] does not directly surface the deployment-relevant prioritization (guidance + cultural appropriateness as dominant) and is not designed as a proxy for student satisfaction. Author rejection of generic NLG metrics in favor of pedagogically-aware scoring [Q4, Q7, Q8, Q9] is methodologically appropriate. OF priority is LOWER per elicitation, consistent with this dimension being a moderate rather than primary risk.

**Strengths:**
- Categorical labels and aggregate percentages [Q64] are interpretable for human-tutor co-author quality control
- Per-tutor reporting [Q67, Q83] supports model selection decisions
- Bridge/MathDial subset reporting [Q149, Q150] enables grade-band-specific analysis
- Explicit rejection of generic NLG metrics as inadequate for pedagogical evaluation [Q4, Q7, Q8, Q9] aligns with deployment-relevant scoring

**Checklist:**

- **OF-1**: Output modality (categorical labels + aggregate percentages) matches deployment evaluation needs; deployment-side tutor output is free-form text but the benchmark's role is intermediate quality scoring, not output generation. — _Sources: Q64, Q66_
- **OF-2**: Not applicable — no speech-based output is required by deployment (text-only mobile/enterprise app).
- **OF-3**: Target population is English-fluent and literate per elicitation; no accessibility-driven form constraint violated.
- **OF-4**: Minor mismatch: equal-weight DAMR aggregation [Q67] does not encode dimension prioritization (guidance + cultural appropriateness as dominant per A4), making the headline score a weak proxy for deployment-relevant acceptability. Also, AC scores rely on LLM-critic correlations that proved unreliable [Q107, Q114], so LLM-as-critic deployment is not yet supported. — _Sources: Q67, Q107, Q114_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q4] 'General domain-agnostic natural language generation (NLG) metrics … are not well-suited for this context, as most of them fail to account for pedagogical values…' (p.1)
- [Q64] 'Desired Annotation Match Rate (DAMR): This metric quantifies the percentage of responses from each human or LLM-based tutor that received the desired annotation labels.' (p.6)
- [Q66] 'Annotation Correlation (AC): This metric is based on Pearson's correlation … allowing us to assess the reliability of LLMs as evaluators in the context of student mistake remediation.' (p.6)
- [Q114] 'We also assess the feasibility of LLMs as evaluators … indicating that they are often unreliable.' (p.9)

</details>

**Information gaps:**
- No documented re-weighting scheme for DAMR aggregation under deployment-specific dimension priorities

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** All 192 source instances [Q52] are drawn from Western datasets with no Indian context, NCERT topics, Indian numeral conventions, or rupee-denominated problems.

**Recommendation:** Author a parallel India-specific instance set of comparable size (≈190 dialogues) drawn from NCERT Grade 1–8 topics with cricket/rupee/local-market contexts; pilot-validate against actual Indian student-tutor transcripts where possible.

### Input Ontology ⚠

**Gap:** Taxonomy lacks NCERT topic categories, Indian numeral-naming subcategories, and rote-procedural error-type categories [Q41, WEB-11, WEB-20].

**Recommendation:** Extend the input ontology with NCERT-aligned topic tags and an Indian-specific misconception subtype taxonomy (formula-recall failures on rephrased problems, lakhs/crores grouping errors, L1-interference patterns), validated with Indian K-8 teachers.

### Output Ontology ⚠

**Gap:** Tutor Tone dimension collapses Neutral and Encouraging into Non-offensive yielding 100% DAMR by construction [Q90]; cultural appropriateness is unrepresented; equal-weight DAMR [Q67] does not encode deployment priorities.

**Recommendation:** Split the Tone dimension into discriminating warmth tiers, add a cultural-appropriateness dimension, and introduce a deployment-weighted composite score that prioritizes guidance and cultural appropriateness consistent with elicitation A4.

### Output Ontology ⚠

**Gap:** The taxonomy implicitly favors Socratic non-revelation [Q17, Q23] over direct correction, which may misalign with Indian exam-oriented pedagogy [WEB-11, WEB-12].

**Recommendation:** Pilot a stakeholder-elicitation study with Indian teachers to determine whether direct-correction guidance should be a recognized acceptable category, and adjust the desired-label mapping for Guidance and Active Learning accordingly.

### Output Content ⚠

**Gap:** Annotators are four CS-educated MBZUAI affiliates [Q6, Q31] with explicitly no required teaching experience [Q32] and no documented Indian educational expertise; only 40/192 instances were doubly annotated [Q57].

**Recommendation:** Re-annotate at minimum a stratified sample (e.g., 60 instances spanning Bridge and MathDial) with 3+ Indian K-8 math educators, compute Indian-rater Cohen's kappa, and quantify dimension-level divergence from the original labels.

### Output Content ⚠

**Gap:** No satisfaction-validation study links MRBench-style pedagogical scores to Indian student satisfaction (the deployment success metric per A4) [WEB-21].

**Recommendation:** Run an in-deployment validation study correlating benchmark dimension scores with student engagement signals and tutor-co-author acceptability ratings; use this to derive deployment-specific dimension weights.

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
| WEB-1 | https://www.mypunepulse.com/which-indian-city-actually-leads-in-cbse-schools-a-closer-look-at-the-facts/ |
| WEB-2 | https://ddhehamirpur.in/which-state-has-the-most-cbse-schools-in-india |
| WEB-3 | https://en.wikipedia.org/wiki/Central_Board_of_Secondary_Education |
| WEB-4 | https://veclakhanpur.in/top-popular-schools-in-india-understanding-the-cbse-system |
| WEB-5 | https://modelpapers2021.in/how-many-students-are-there-in-cbse-board-in-india |
| WEB-6 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2132330&reg=3&lang=2 |
| WEB-7 | https://www.dataforindia.com/comm-tech/ |
| WEB-8 | https://datareportal.com/reports/digital-2025-india |
| WEB-9 | https://www.vedantu.com/ncert-solutions |
| WEB-10 | https://ai4education.in/ai-for-ncert%2Fcbse |
| WEB-11 | https://www.cbseguess.com/article/detail/why-most-students-struggle-with-cbse-mathematics-and-how-to-fix-it-33 |
| WEB-12 | https://www.drishtiias.com/daily-news-analysis/national-achievement-survey-nas-2021 |
| WEB-13 | https://nas.gov.in/about-nas |
| WEB-14 | https://www.mathnasium.com/math-centers/hydepark/news/common-math-misconceptions-k-8 |
| WEB-15 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-16 | https://prsindia.org/billtrack/digital-personal-data-protection-bill-2023 |
| WEB-17 | https://ksandk.com/data-protection-and-data-privacy/childrens-data-protection-under-indias-dpdp-rules/ |
| WEB-18 | https://www.dpdpa.com/dpdpa2023/chapter-2/section9.html |
| WEB-19 | https://ksandk.com/data-protection-and-data-privacy/dpdp-compliance-for-schools-and-edtech/ |
| WEB-20 | https://arxiv.org/html/2602.18429 |
| WEB-21 | https://aicompetence.org/ai-socratic-tutors/ |

---

