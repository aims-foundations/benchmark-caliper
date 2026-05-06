## Deployment Context

**Use case:** Deployment scenario: A GPT-4 model is implemented in a one-on-one tutoring session, where its responses are augmented with a human tutor’s input. We need to assesd whather Are the student stisfied with this newly GPT4 responses?

Domain: Educational tutoring
Setting: Mobile application / enterprise software
**Target population:** A student from a metropolitan city in India, in grades 1–8, who is fluent in English.

# Validity Analysis: mrbench
**Target context:** Metropolitan India — Grades 1–8 Mathematics Tutoring (Student Population)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 3 | Moderate gaps | medium |
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

MRBench provides a methodologically rigorous, learning-sciences-grounded evaluation framework for LLM tutoring on mathematics mistake remediation, but it is materially misaligned with the Metropolitan India Grade 1–8 deployment on the dimensions the user has flagged as HIGH priority. The taxonomy (input ontology) lacks any category for NCERT alignment, Indian numeral conventions, or cultural register; the instance pool (input content) is drawn from Western-framed Bridge and MathDial datasets with no documented Indian content, against a deployment requirement (A1, A2) for NCERT-aligned, India-grounded problems; the output ontology has no dimension for cultural appropriateness or student satisfaction, with the Tutor Tone dimension trivially collapsing to non-offensiveness [Q90] precisely on the axis where Indian classroom warmth norms (A4) would matter; and ground-truth labels (output content) come from four Computer Science post-graduates with undisclosed nationality and no teaching experience [Q31, Q32], with no Indian rater validation in either MRBench or the BEA 2025 Shared Task [WEB-17, WEB-18]. Input form and output form are well-matched as text-only English-medium evaluation, partially mitigating overall risk. The benchmark is useful as a partial diagnostic — particularly for per-LLM behaviors like answer revelation rate — but it cannot substitute for a culturally and curricularly validated evaluation of the deployment's primary success criterion.

## Practical Guidance

### What This Benchmark Measures

MRBench measures whether LLM tutor responses to student mathematical mistakes exhibit eight specific pedagogical behaviors: mistake identification, mistake-location, guidance, actionability, coherence, tone (operationalized as non-offensiveness), human-likeness, and not-revealing-the-answer. For the Indian deployment, the strongest signals come from input form (text-based English dialogue, fully matched to deployment) and output form (per-dimension DAMR diagnostics that directly support QA review by human tutor co-authors), particularly the answer-revelation rate which is a meaningful production-relevant signal.

### Construct Depth

The benchmark probes pedagogical behaviors at the level of individual tutor turns, not learning outcomes or student satisfaction — limitations explicitly acknowledged by the authors [Q119, Q120, Q121]. It provides no evidence on cultural appropriateness, NCERT alignment, or Indian-context word problem handling, and the Tutor Tone dimension collapses trivially [Q90] on the very axis where Indian register differences would surface. DAMR's per-dimension granularity is useful but does not operationalize the deployment's primary success criterion (student satisfaction).

### What Else You Need

Substantial supplementation is required: (1) NCERT-aligned content evaluation set (input_ontology, input_content) since no existing benchmark fills this [WEB-6, WEB-7]; (2) Indian-context word problem evaluation extending GSM8K-style robustness testing [WEB-8] to MRBench dialogues; (3) cultural-appropriateness output dimension with Indian-rater-validated desired labels (output_ontology, output_content); (4) student-satisfaction validation linking DAMR to actual engagement signals from the deployed system; (5) Indian rater pool (educators and metropolitan Grade 1–8 students/parents) to re-annotate a sample for tone, human-likeness, and any added cultural dimension. DPDP Act 2025 [WEB-23, WEB-24] imposes verifiable parental consent and bans on profiling that constrain how this supplementation can be done.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
MRBench's eight-dimension pedagogical taxonomy is rigorously derived from learning-sciences principles [Q1, Q15, Q129] and covers core mistake-remediation behaviors (mistake identification, guidance, not revealing the answer, tone, human-likeness) that are relevant to any tutoring deployment. However, for the Indian metropolitan Grade 1–8 deployment — explicitly flagged HIGH priority and confirmed in elicitation A1 to require NCERT-aligned curriculum coverage — the taxonomy contains no category for curriculum alignment, Indian numeral conventions (lakhs/crores), rupee-denominated content, or culturally appropriate register. The authors themselves acknowledge the taxonomy 'will need to be verified on and likely adapted if applied to other tasks ... and to subjects other than mathematics' [Q118] but do not extend this to non-Western educational settings. Web search confirms no NCERT Grade 1–8 tutoring dialogue benchmark exists [WEB-6, WEB-7], so the gap is not addressable by alternative resources. The taxonomy provides partial but inadequate coverage of the categories required for this deployment.

**Strengths:**
- Pedagogically grounded eight-dimension taxonomy derived through iterative validation [Q15, Q129, Q132]
- Explicit focus on mistake remediation in mathematics matches the deployment's task scope [Q12, Q117]
- Covers two curriculum levels (elementary/Bridge and middle school/MathDial) corresponding to Grades 1–8 banding [Q143, Q144]

**Checklist:**

- **IO-1**: Required regional categories include NCERT-aligned topic coverage (place value with lakhs, fractions, integers, linear equations, mensuration), Indian numeral conventions, rupee-denominated word problems, and culturally appropriate register. Confirmed via elicitation A1 and NCERT syllabus sources [WEB-2, WEB-4, WEB-5]. — _Sources: WEB-2, WEB-4, WEB-5_
- **IO-2**: Yes. The benchmark's taxonomy omits curriculum alignment, Indian numeral conventions, and cultural-register categories. The authors acknowledge adaptation would be required for other educational settings [Q118, Q130], and no NCERT-aligned tutoring dialogue benchmark currently fills this gap [WEB-6, WEB-7]. — _Sources: Q117, Q118, Q130, WEB-6, WEB-7_
- **IO-3**: The taxonomy's pedagogical dimensions (mistake identification, guidance, actionability, coherence, tone, human-likeness, etc.) are broadly relevant; no included category is clearly irrelevant to the Indian deployment, though the operationalization of Tutor Tone trivially collapses to non-offensiveness [Q90]. — _Sources: Q1, Q15_
- **IO-4**: Documented gaps: (a) no NCERT curriculum-alignment dimension; (b) no Indian numeral/currency convention dimension; (c) no cultural-appropriateness/register dimension. These omissions harm content validity for the target deployment because A4 confirms cultural appropriateness is a necessary condition for satisfaction. — _Sources: Q118, Q130, Q143, Q144_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we propose a unified evaluation taxonomy with eight pedagogical dimensions based on key learning sciences principles' (p.1)
- [Q15] 'narrowing the evaluation taxonomy down to eight measurable dimensions aligned with key pedagogical strategies' (p.3)
- [Q117] 'The proposed taxonomy primarily focuses on the task of the student mistake remediation in the domain of mathematics.' (p.9)
- [Q118] 'We acknowledge that the proposed taxonomy will need to be verified on and likely adapted if applied to other tasks ... and to subjects other than mathematics.' (p.9)
- [Q129] 'Through an iterative analysis of the taxonomy, we identify eight dimensions that comprehensively assess tutor response quality in the context of mistake remediation.' (p.12)
- [Q130] 'other educational settings, particularly those involving tutorial dialogues beyond mistake remediation, may require modifications' (p.12)
- [Q143] 'including both datasets in MRBench ensures diversity and provides for a good mix of easy and difficult mathematical problems' (p.14)
- [Q144] 'The problems covered in the Bridge dataset are at the elementary school level, whereas those in MathDial are at the middle school level.' (p.14)

*Web sources:*
- [WEB-2] NCERT Grade 1–5 mathematics syllabus (place value with lakhs, spiral sequencing)
- [WEB-4] NCERT upper-primary syllabus emphasizing abstraction, fractions, integers, algebra
- [WEB-5] NCERT Class 8 chapter list (Rational Numbers, Linear Equations, Mensuration)
- [WEB-6] MathQuest covers NCERT but only Grades 11–12 and is problem-solving, not tutoring dialogue
- [WEB-7] HAWP Hindi arithmetic word problems — only Indian-language math dataset, not tutoring dialogue

</details>

**Information gaps:**
- No documentation of whether MRBench's source datasets contain any NCERT-aligned content
- No empirical study comparing pedagogical taxonomy coverage across Indian vs. Western tutoring contexts

**Requires expert verification:**
- Whether additional pedagogical dimensions (e.g., respect/hierarchy register, scaffolding to NCERT learning outcomes) are required for the Indian metropolitan cohort

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Input content is a HIGH-priority dimension per elicitation, and the deployment requires Indian everyday contexts (cricket, rupees, local markets, school fees) with explicit rejection of Western contexts (A2). MRBench's 192 instances are drawn entirely from Bridge and MathDial [Q41, Q52], neither of which is documented as containing Indian curriculum content, Indian numeral conventions, or India-specific scenarios. The paper notes that Bridge problems are 'fundamental mathematical concepts, including operations such as multiplication, addition' [Q45] in short Western-style framings, and MathDial is 'middle school-level mathematical reasoning' [Q49] without regional grounding. Web search confirms no Indian-context tutoring dialogue dataset exists [WEB-6, WEB-7], and GSM8K robustness research (Tomar et al. 2025) directly demonstrates measurable LLM performance drops when Western contexts are replaced with Indian ones [WEB-8] — establishing that this is not cosmetic but a measurable validity threat. There is no evidence of any India-relevant content in MRBench's instance pool.

**Strengths:**
- Instance pool is rigorously filtered for high quality, with a clear criterion that the student's last utterance contains a mistake [Q46, Q47, Q51]
- Combines elementary and middle-school-level dialogues providing some grade-banding diversity within math [Q97, Q143, Q144]
- Fundamental mathematical operations covered (addition, multiplication) overlap with NCERT primary content even if framing differs [Q45]

**Checklist:**

- **IC-1**: Yes — the deployment requires Indian cultural, geographic, and curricular grounding (NCERT topics, rupees, cricket, local markets, train timetables, school fees, festival contexts). Confirmed via elicitation A1, A2 and NCERT syllabus sources [WEB-2, WEB-4]. — _Sources: WEB-2, WEB-4_
- **IC-2**: No — there is no evidence that MRBench's source datasets contain any India-aligned cultural content. Bridge and MathDial are sourced from Western/general-context tutoring corpora [Q41, Q44, Q48] with no documentation of Indian inclusion. — _Sources: Q41, Q44, Q48_
- **IC-3**: Likely yes. The paper notes Bridge dialogues focus on 'fundamental operations' [Q45] in short Western-framed contexts, and MathDial's middle-school reasoning problems [Q49] are not documented as having Indian grounding. GSM8K robustness research directly demonstrates that Western-to-Indian context substitution degrades LLM performance [WEB-8], so Western framings in MRBench's instances do not transfer cleanly. — _Sources: Q45, Q49, Q93, WEB-8_
- **IC-4**: Not performed by the benchmark authors. INSUFFICIENT DOCUMENTATION on whether any regional annotators reviewed instance content for cultural fit; the four annotators' nationalities are undisclosed [Q31]. — _Sources: Q31_
- **IC-5**: Documented harms to content validity: (a) no rupee-denominated problems; (b) no Indian numeral conventions in problem statements; (c) no Indian everyday scenarios; (d) Western framings that empirically degrade LLM performance when transposed [WEB-8]. The deployment's HIGH-priority requirement for Indian-context word problems is entirely unmet. — _Sources: Q41, WEB-6, WEB-8_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q41] 'We have compiled mistake remediation benchmark, MRBench, from the Bridge (Wang et al., 2024a) and MathDial (Macina et al., 2023) datasets.' (p.5)
- [Q44] 'The Bridge dataset comprises partial dialogue interactions between real human tutors and students at the elementary level' (p.5)
- [Q45] 'The dialogue context is typically short (few turns) and predominantly focused on fundamental mathematical concepts, including operations such as multiplication, addition' (p.5)
- [Q48] 'The dialogues in the MathDial dataset consist of complete multi-turn conversations between a real human tutor and an LLM acting as a student' (p.5)
- [Q49] 'these conversations are grounded in middle school-level mathematical reasoning questions' (p.5)
- [Q52] 'for the 192 instances in MRBench (60 from Bridge and 132 from MathDial)' (p.6)
- [Q93] 'they struggle to provide appropriate guidance without revealing the answer because the mistakes are generally related to quite basic operations like addition or multiplication' (p.8)

*Web sources:*
- [WEB-6] No NCERT-aligned Grade 1–8 English-medium tutoring dialogue benchmark exists
- [WEB-7] HAWP is Hindi arithmetic word problems only, not tutoring dialogue
- [WEB-8] GSM8K robustness research shows Indian-context substitution causes measurable LLM performance drops

</details>

**Information gaps:**
- No instance-level content audit of Bridge/MathDial for cultural framings is published
- No data on whether any of the 192 instances incidentally contain India-applicable framings

**Requires expert verification:**
- Sample-level review by Indian educators to confirm degree of cultural distance in actual instance content
- Empirical measurement of LLM performance drop on MRBench instances when transposed to Indian context

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form is a LOWER-priority dimension. MRBench is text-based English dialogue [Q13, Q133], encoded as conversation history with tutor/student turns and lengths measured in characters [Q147]. The deployment is also text-only English-medium via mobile or enterprise software and explicitly targets fluent English speakers; no modality, script, or language mismatch exists. Mobile internet penetration in metropolitan India is high (75%+ of children aged 5–14 use mobile phones, with metro rates higher) [WEB-10, WEB-12], and Android dominates with 92.4% market share [WEB-13], so text-based delivery on mobile is well-supported. The minor concerns are that conversation lengths and turn structures differ between Bridge and MathDial [Q141, Q142] — but this represents internal diversity rather than a target-context mismatch.

**Strengths:**
- Text-only English format perfectly matches the deployment's text-based English-medium delivery [Q13]
- Conversation-history input format directly matches a mobile-app tutoring dialogue use case [Q13, Q133]
- Internal diversity in conversation length across Bridge and MathDial provides some signal-distribution variation [Q141, Q142]

**Checklist:**

- **IF-1**: Signal distributions are aligned: both benchmark and deployment are English-medium text dialogues with conversation history and turn structure [Q13, Q133]. No script or language mismatch. — _Sources: Q13, Q133_
- **IF-2**: Regional infrastructure supports the format. India has approximately 750M+ mobile internet users with strong metropolitan 5G coverage [WEB-10, WEB-11], and Android dominates at 92.4% market share [WEB-13]. — _Sources: WEB-10, WEB-11, WEB-13_
- **IF-3**: Domain-specific form is well-matched: tutor/student dialogue turns over text are the deployment's actual use case. No multimodal (audio, image, handwriting) requirement is specified. — _Sources: Q13, Q133_
- **IF-4**: Minor gap: MathDial does not provide conversation topic labels [Q145], which could complicate routing/curriculum-tagging in deployment. Otherwise no form mismatch identified. — _Sources: Q145_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q13] 'Formally, let's define the conversation history between a tutor and a student as H = {(T1, S1),(T2, S2), ...}' (p.3)
- [Q133] 'The prompt template used to generate responses from the seven considered LLMs for both the Bridge and MathDial datasets is shown in Figure 2.' (p.12)
- [Q141] 'conversation history and response lengths from different LLMs and humans are generally shorter in the Bridge dataset compared to the MathDial dataset' (p.14)
- [Q145] 'The conversation topic is not provided in MathDial.' (p.14)
- [Q147] 'In all cases, length is estimated using the number of characters.' (p.14)

*Web sources:*
- [WEB-10] 751.5M Indian internet users, 52.4% penetration as of 2024
- [WEB-11] Mobile broadband dominates Indian internet access; 5G rollout in metros since 2022
- [WEB-12] ~65% of Indian children aged 5–14 used mobile phones in 2023
- [WEB-13] Android dominates Indian smartphone OS market at 92.4% in 2025

</details>

**Information gaps:**
- No data on actual deployment device distribution for Grade 1–8 metropolitan students specifically (smartphone vs. tablet vs. laptop share)

**Requires expert verification:**
- Whether deployment intends to support voice/audio modalities later, which would require benchmark extension

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Output ontology is a HIGH-priority dimension per elicitation. MRBench scores responses across eight pedagogical dimensions using a three-tier label system [Q58, Q59] aggregated into DAMR [Q64]. Critically, the deployment's primary success criterion is student satisfaction, and elicitation A4 explicitly confirms that a pedagogically correct but culturally distant response would NOT count as satisfying — yet MRBench has no output category for cultural appropriateness, NCERT curriculum correctness, or Indian classroom register. The Tutor Tone dimension trivially collapses to a non-offensiveness boundary (DAMR reaches 100% when neutral and encouraging are merged into 'Non-offensive') [Q90], failing to operationalize the warmth/encouragement register required by the deployment. The authors explicitly acknowledge the taxonomy 'does not consider the tutoring dialogues' impact on overall student learning' [Q120, Q121] and treats dimensions as orthogonal/independent [Q30, Q86] despite real interdependencies [Q116]. A response could therefore receive a high DAMR score while being culturally unsuitable for metropolitan Indian students, with no flag in the output schema. Web search confirms no validation study links MRBench scores to Indian student satisfaction [WEB-9, WEB-17, WEB-18].

**Strengths:**
- Eight orthogonal pedagogical dimensions provide fine-grained per-behavior signal that supports targeted diagnosis (e.g., GPT-4 reveals answer 47% of time) [Q69]
- Three-tier labeling system [Q58, Q59] captures partial credit for ambiguous cases
- Explicit 'desired label' for each dimension makes the decision rule transparent and auditable [Q65, Q128]
- Domain-agnostic NLG metrics (BLEU, BERTScore) are explicitly rejected for being inappropriate to pedagogical evaluation [Q4, Q7, Q8, Q10] — a defensible methodological choice

**Checklist:**

- **OO-1**: The eight output categories (mistake identification, mistake location, guidance, actionability, coherence, tone, human-likeness, revealing the answer) are pedagogically relevant for any tutoring context but are insufficient for the Indian deployment, which additionally requires cultural appropriateness and curriculum alignment categories (A4, A1). — _Sources: Q14, Q64_
- **OO-2**: Missing categories: (a) cultural-register/warmth specific to Indian classroom norms; (b) NCERT curriculum correctness; (c) Indian numeral convention compliance; (d) student satisfaction proxy. Tutor Tone is operationalized as non-offensiveness [Q90], which does not capture warmth required by elicitation A4. — _Sources: Q90, Q119, Q120_
- **OO-3**: Tutor Tone's collapse to 'Non-offensive' achieving 100% DAMR [Q90] encodes a Western default of register adequacy that does not match Indian classroom warmth norms (per A4). The 'human-likeness' dimension is similarly under-specified for cultural register. — _Sources: Q89, Q90_
- **OO-4**: Stakeholder-driven taxonomy redesign is needed: at minimum, adding a cultural-appropriateness dimension and a curriculum-alignment dimension, with desired labels validated against Indian educators and students. — _Sources: Q116, Q118_
- **OO-5**: Documented harms: structural validity is harmed because the deployment's success construct (student satisfaction including cultural fit) has structure not captured by the eight dimensions; content validity is harmed by missing categories; external validity is harmed because high DAMR scores cannot be assumed to predict deployment-context satisfaction. Authors themselves acknowledge taxonomy does not address overall learning impact [Q120, Q121]. — _Sources: Q120, Q121, WEB-9, WEB-17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q14] 'The evaluation taxonomy detailed in Section 4 assesses the appropriateness of the Tt+1 response across eight key pedagogical dimensions.' (p.3)
- [Q30] 'we explicitly instructed all annotators to treat each dimension as independent and orthogonal' (p.4)
- [Q58] 'Each dimension was annotated using a three-tier labeling system' (p.6)
- [Q64] 'Desired Annotation Match Rate (DAMR): This metric quantifies the percentage of responses ... that received the desired annotation labels.' (p.6)
- [Q86] 'This further demonstrates the need to treat the dimensions as independent.' (p.8)
- [Q89] 'in task-oriented conversations, AI tutors tend to be more Neutral than Encouraging.' (p.8)
- [Q90] 'When we combine these two labels into "Non-offensive", the DAMR score reaches 100% as we observe no offensive responses from any LLMs or humans.' (p.8)
- [Q116] 'in practice, these dimensions may be inherently interrelated and may influence one another.' (p.9)
- [Q119] 'The current taxonomy and annotation scheme focus on the appropriateness of the tutor responses.' (p.9)
- [Q120] 'one of the limitations is that it does not consider the tutoring dialogues' impact on the overall student learning.' (p.9)
- [Q121] 'the annotation pertains to the individual tutor turns within educational dialogues, which restricts our understanding of broader implications on student learning processes' (p.9)

*Web sources:*
- [WEB-9] LLM-in-education meta-analysis documents motivational effects but not for Indian school-age math
- [WEB-17] BEA 2025 Shared Task extended MRBench without Indian curriculum or rater adaptation
- [WEB-18] NAACL 2025 BEA proceedings: no participating system addressed regional adaptation

</details>

**Information gaps:**
- No published correlation between DAMR scores and student satisfaction for any population
- No empirical specification of what Indian-classroom 'warmth register' looks like at the response level

**Requires expert verification:**
- Definition and operationalization of a cultural-appropriateness output dimension by Indian educators and students
- Calibration of desired labels for Tutor Tone against Indian metropolitan student preferences

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Output content is MODERATE-priority per elicitation, with A3 indicating partial alignment expected between Indian student satisfaction and benchmark annotators but anticipating divergence on tone, warmth, and cultural fit. MRBench's annotators are four post-graduate Computer Science students proficient in English [Q31] with no disclosed nationality, cultural background, or teaching experience [Q32]; teaching experience was explicitly NOT required [Q32]. Inter-annotator agreement is substantial (Fleiss' kappa 0.65 pilot, Cohen's kappa 0.71 full-scale) [Q39, Q61], indicating internal label reliability — but reliability does not address whether labels reflect Indian stakeholder perspectives. No Indian educators, parents, or students contributed to ground-truth labels, and no cross-cultural validation has been performed; the BEA 2025 Shared Task extended MRBench without addressing this [WEB-17, WEB-18]. The deployment's actual judges (human tutor co-authors and student engagement signals per A3) are structurally different from the benchmark's annotator pool. LLM-as-judge alternatives are explicitly unreliable [Q107, Q109, Q114], a finding corroborated by 2024–2025 literature [WEB-19, WEB-20], so they cannot substitute for human re-annotation.

**Strengths:**
- Strong inter-annotator agreement (Fleiss' kappa 0.65, Cohen's kappa 0.71) demonstrates internal label reliability [Q39, Q61]
- In-house annotation with comprehensive training and validation pilot avoids crowdsourcing quality issues [Q33, Q34, Q35]
- Expert and Novice human responses included as comparison baselines, with Expert treated as gold standard [Q68, Q78]
- Authors explicitly assess and report the unreliability of LLM critics [Q107, Q109, Q114] — providing honest evidence that automated re-annotation is not a substitute

**Checklist:**

- **OC-1**: No — labels reflect the perspectives of four Computer Science post-graduates [Q31] with undisclosed nationality and no teaching experience [Q32]. There is no documented Indian stakeholder representation in the annotator pool. — _Sources: Q31, Q32_
- **OC-2**: Disagreement is anticipated, particularly on Tutor Tone and human-likeness dimensions where cultural register expectations differ. A3 indicates partial alignment expected; A4 confirms divergence on cultural appropriateness. The paper itself notes Tutor Tone's neutral/encouraging distinction collapses trivially [Q90], suggesting the dimension lacks discriminative power on the very axis where Indian register differences would matter. — _Sources: Q90, Q107_
- **OC-3**: Annotator demographics partially disclosed: gender (2 male, 2 female), education (post-graduate Computer Science), and English proficiency [Q31]. Nationality, cultural background, and teaching experience are NOT disclosed; teaching experience explicitly not required [Q32]. This is below the level of detail recommended in Datasheets/Data Statements for cross-cultural validity assessment. — _Sources: Q31, Q32_
- **OC-4**: Re-annotation by representative regional annotators (Indian educators, Indian metropolitan students or parents) is needed for the deployment, particularly on tone, human-likeness, and any added cultural-appropriateness dimension. No such re-annotation exists [WEB-17]. — _Sources: WEB-17, WEB-18_
- **OC-5**: Aggregation method (majority across four annotators with Cohen's kappa reported [Q57, Q61]) is reasonable for internal reliability but provides no mechanism to detect minority cultural perspectives; with all four annotators from a single demographic profile, minority perspectives are structurally absent. — _Sources: Q39, Q61_
- **OC-6**: Documented harms to convergent validity (labels not validated against Indian raters) and external validity (judgments may not generalize to Indian metropolitan student satisfaction). The deployment's reliance on human tutor co-authorship partially mitigates this for the deployed system, but the benchmark itself cannot be relied on as a satisfaction proxy. — _Sources: Q31, Q32, WEB-19, WEB-20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'The annotation team consisted of two male and two female annotators, with all four annotators holding at least a post-graduate degree in Computer Science and being proficient in English.' (p.5)
- [Q32] 'we do not require annotators to have direct teaching experience ... being able to judge the responses from the perspective of a potential user of such AI tutors (or a student), rather than specifically a teacher, is sufficient.' (p.5)
- [Q33] 'we opted not to use public annotation outsourcing platforms such as Prolific or MTurk' (p.5)
- [Q39] 'we computed Fleiss' kappa value, which for this annotation experiment equals 0.65, indicating substantial agreement.' (p.5)
- [Q61] 'The annotators reached an average Cohen's kappa score of 0.71' (p.6)
- [Q68] 'We consider human-based evaluations as gold standard.' (p.7)
- [Q107] 'most of the correlation scores are negative ... indicating that the annotations from the LLMs are unreliable for the challenging pedagogical dimensions.' (p.8)
- [Q109] 'both LLMs have a limited understanding of rich pedagogical concepts' (p.8)
- [Q114] 'we also assess the feasibility of LLMs as evaluators in this context ... indicating that they are often unreliable.' (p.9)

*Web sources:*
- [WEB-17] BEA 2025 Shared Task extended MRBench without Indian rater validation
- [WEB-18] NAACL 2025 BEA proceedings: no participating system documented Indian adaptation
- [WEB-19] 2025 MDPI study: LLM evaluators show inconsistency across models for educational evaluation
- [WEB-20] 2025 essay-evaluation study: LLM scores and human judgements share little common signal

</details>

**Information gaps:**
- Annotator nationality and cultural background not disclosed in the paper
- No cross-cultural validation study with Indian raters has been published
- No published comparison of MRBench labels to Indian human-tutor co-author judgments

**Requires expert verification:**
- Re-annotation of a sample of MRBench instances by Indian educators and metropolitan Grade 1–8 students to quantify divergence on tone and human-likeness
- Calibration of the deployment's human tutor co-author judgments against MRBench gold labels

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Output form is a LOWER-priority dimension. MRBench's evaluation outputs are categorical labels per dimension and aggregate DAMR/AC scores [Q64, Q66], not free-form text — providing actionable per-dimension diagnostics (e.g., GPT-4 reveals answer 47% of the time [Q69]) that map cleanly to deployment QA tasks. The deployment's actual product output is free-form English tutor text, which the benchmark does not directly score for free-form quality but indirectly assesses via the categorical taxonomy. Domain-agnostic NLG metrics (BLEU, BERTScore) are explicitly rejected as inappropriate [Q4, Q7, Q8, Q10] — a defensible methodological choice. The chief weakness is that DAMR does not operationalize student satisfaction or engagement, and the LLM-critic alternative is unreliable [Q107, Q109, Q114] — confirmed by 2024–2025 literature [WEB-19, WEB-20] — meaning automated re-evaluation of the deployed system using MRBench-style critics is not a valid substitute for human judgment. Partial mitigation comes from the deployment's human tutor co-authorship layer.

**Strengths:**
- DAMR provides interpretable per-dimension percentages directly usable for model comparison and deployment QA [Q64, Q67]
- Per-dataset (Bridge vs. MathDial) reporting [Q149, Q150] enables grade-band-specific diagnostics roughly aligned with primary vs. upper-primary
- Explicit, well-reasoned rejection of NLG metrics that would be inappropriate for tutoring evaluation [Q4, Q7, Q8, Q10]
- Honest reporting of LLM-critic unreliability [Q107, Q109, Q114] prevents users from over-relying on automated re-evaluation

**Checklist:**

- **OF-1**: Output modality (categorical label scoring + aggregate metrics) is not the deployment's product output (free-form tutor text), but it serves as an evaluation signal that maps onto the deployment's per-dimension QA needs. The match is indirect but adequate as evaluation signal. — _Sources: Q64, Q67_
- **OF-2**: Not applicable — neither benchmark nor deployment requires text-to-speech. INSUFFICIENT DOCUMENTATION on whether deployment plans audio extension; assumed text-only per regional context.
- **OF-3**: Target population is described as fluent English speakers in metropolitan India [regional context]. Mobile internet penetration is high [WEB-10, WEB-12], so accessibility constraints around text output are minimal. INSUFFICIENT DOCUMENTATION on accessibility for students with disabilities in the deployment's target population. — _Sources: WEB-10, WEB-12_
- **OF-4**: Documented form mismatch: DAMR does not operationalize student satisfaction or engagement, which is the deployment's primary success criterion. Automated LLM critics are unreliable [Q107, Q114] and cannot substitute for human judgment in production. External validity is partially harmed: benchmark scores will not transparently predict deployment satisfaction outcomes. — _Sources: Q107, Q114, WEB-19, WEB-20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q4] 'General domain-agnostic natural language generation (NLG) metrics ... are not well-suited for this context, as most of them fail to account for pedagogical values' (p.1)
- [Q64] 'Desired Annotation Match Rate (DAMR): This metric quantifies the percentage of responses from each human or LLM-based tutor that received the desired annotation labels.' (p.6)
- [Q66] 'Annotation Correlation (AC): This metric is based on Pearson's correlation' (p.6)
- [Q67] 'Table 3 shows DAMR scores for each LLM across all eight dimensions.' (p.7)
- [Q69] 'GPT-4 reveals the answer approximately 47% of the time, making its responses less actionable' (p.7)
- [Q107] 'most of the correlation scores are negative ... indicating that the annotations from the LLMs are unreliable' (p.8)
- [Q114] 'we also assess the feasibility of LLMs as evaluators in this context ... indicating that they are often unreliable.' (p.9)
- [Q149] 'DAMR scores ... with human evaluation on the Bridge data.' (p.16)
- [Q150] 'DAMR scores ... with human evaluation on the MathDial data.' (p.16)

*Web sources:*
- [WEB-10] Mobile internet broadly available in Indian metros for text delivery
- [WEB-12] ~65% of Indian children aged 5–14 used mobile phones in 2023
- [WEB-19] 2025 MDPI: LLM evaluator inconsistency confirmed for educational evaluation
- [WEB-20] 2025 study: LLM and human evaluator scores share little common signal

</details>

**Information gaps:**
- No documented mapping between DAMR scores and student satisfaction outcomes
- No published deployment study using MRBench scores as a production QA signal

**Requires expert verification:**
- Whether the deployment's human tutor co-authors can effectively use DAMR-style per-dimension reports for QA review
- Whether deployment satisfaction signals can be calibrated to MRBench dimensions via instrumentation

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** All 192 instances are drawn from Western-context Bridge and MathDial datasets with no documented Indian content; GSM8K research shows context substitution causes measurable LLM performance drops.

**Recommendation:** Construct a parallel evaluation set of NCERT-aligned dialogues with Indian everyday contexts (cricket, rupees, local markets, school fees, train timetables) authored or reviewed by Indian primary/middle-school teachers, and re-evaluate the seven LLMs on this set to quantify the regional performance gap.

### Input Content ⚠

**Gap:** DPDP Act 2023 / Rules 2025 impose verifiable parental consent and ban profiling/tracking of under-18 users [WEB-23, WEB-24], constraining how Indian student data can be collected for any supplementation effort.

**Recommendation:** Design any Indian content-collection or re-annotation effort under DPDP-compliant verifiable parental consent workflows; avoid behavioural-monitoring data collection for under-18 users and document data fiduciary obligations before deployment.

### Output Ontology ⚠

**Gap:** Tutor Tone dimension collapses to non-offensiveness [Q90]; no output category captures cultural appropriateness or student satisfaction, both confirmed essential by elicitation A4.

**Recommendation:** Replace or supplement the Tutor Tone dimension with a multi-level cultural-register dimension calibrated to Indian classroom warmth norms; add a proxy output dimension for predicted student satisfaction validated against in-deployment engagement signals.

### Input Ontology ⚠

**Gap:** Taxonomy omits NCERT curriculum alignment, Indian numeral convention compliance, and cultural-register categories required by the deployment.

**Recommendation:** Extend the eight-dimension taxonomy with at least three additional categories (curriculum-alignment, numeral/currency-convention compliance, cultural-register/warmth) and validate them with Indian educators before any deployment QA decisions are made on benchmark scores.

### Output Content ⚠

**Gap:** Ground-truth labels reflect four Computer Science post-graduates with undisclosed nationality and no teaching experience; no Indian rater validation in MRBench or BEA 2025 Shared Task.

**Recommendation:** Recruit a panel of Indian educators (NCERT-familiar primary and middle-school math teachers) and a smaller panel of metropolitan Grade 1–8 students or parents to re-annotate at least the 40 double-annotated instances [Q57] across all dimensions, then quantify divergence from MRBench gold labels and report dimension-specific recalibration.

### Output Form

**Gap:** DAMR does not operationalize student satisfaction; LLM critics are unreliable [Q107, Q114] and cannot substitute for human judgment, confirmed by 2024–2025 literature [WEB-19, WEB-20].

**Recommendation:** Treat MRBench scores as one input among several to a deployment QA dashboard that also incorporates human tutor co-author ratings and student engagement signals, rather than as a sufficient indicator of deployment readiness; do not use Prometheus2/Llama-3.1-8B critics for production re-evaluation.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "we propose a unified evaluation taxonomy with eight pedagogical dimensions based on key learning sciences principles, which is designed to assess the pedagogical value of LLM-powered AI tutor responses grounded in student mistakes or confusions in the mathematical domain." |
| Q2 | 1 | input_content | "We release MRBench – a new evaluation benchmark containing 192 conversations and 1,596 responses from seven state-of-the-art LLM-based and human tutors, providing gold annotations for eight pedagogical dimensions." |
| Q3 | 1 | output_form | "We assess reliability of the popular Prometheus2 and Llama-3.1-8B LLMs as evaluators and analyze each tutor's pedagogical abilities, highlighting which LLMs are good tutors and which ones are more suitable as question-answering systems." |
| Q4 | 1 | output_form | "General domain-agnostic natural language generation (NLG) metrics (Lin, 2004; Popovic´, 2017; Post, 2018; Gao et al., 2020; Liu et al., 2023) are not well-suited for this context, as most of them fail to account for pedagogical values and require gold references, which are often not available, especially in online interactions." |
| Q5 | 1 | input_ontology | "Specifically, for the student mistake remediation task, we need to assess complex pedagogical aspects and abilities of such systems, ensuring that they provide students with sufficient, helpful, and factually correct guidance and do not simply reveal answers when a student makes a mistake." |
| Q6 | 1 | input_content | "Kaushal Kumar Maurya, KV Aditya Srivatsa, Kseniia Petukhova and Ekaterina Kochmar. Mohamed bin Zayed University of Artificial Intelligence, Abu Dhabi, UAE." |
| Q7 | 2 | output_form | "General domain-agnostic natural language generation (NLG) metrics like BLEU (Papineni et al., 2002), BERTScore (Lin, 2004), DialogRPT (Gao et al., 2020), and so on have been used as proxies to measure the coherence and human-likeness of AI tutor responses." |
| Q8 | 2 | output_form | "However, these metrics do not account for pedagogical values (Jurenka et al., 2024; Liu et al., 2024) and often require a ground truth answer to evaluate matching responses." |
| Q9 | 2 | output_form | "For a given input dialogue, there can be multiple valid, pedagogically correct ground truth responses, making detection of the optimal answer non-deterministic (Tack and Piech, 2022; Al-Hossami et al., 2024)." |
| Q10 | 2 | output_form | "Additionally, these metrics can be easily manipulated; for instance, simple responses like "Hello" or "teacher:" (Baladón et al., 2023; Jurenka et al., 2024) can inflate scores." |
| Q11 | 2 | input_ontology | "In this section, we first briefly overview and discuss the limitations of the existing general-purpose NLG metrics and then turn to pedagogically-oriented approaches to evaluation." |
| Q12 | 3 | input_ontology | "In this work, we focus on educational dialogues between a student and a tutor in the mathematical domain. Specifically, the conversations are grounded in students' mistakes or confusions, and the AI tutor aims to respond in order to remediate such mistakes or confusions." |
| Q13 | 3 | input_form | "Formally, let's define the conversation history between a tutor and a student as H = {(T1, S1),(T2, S2), . . . ,(Tt, St)}, where Ti represents the i-th response from the tutor, and Si represents the i-th response from the student. Let Sk denote the student's most recent k utterances, where k ∈ [1, ..., t], containing a mistake or confusion. Then the objective of the tutor is to provide the most appropriate response Tt+1 to address this mistake or confusion." |
| Q14 | 3 | output_ontology | "The evaluation taxonomy detailed in Section 4 assesses the appropriateness of the Tt+1 response across eight key pedagogical dimensions." |
| Q15 | 3 | input_ontology | "In this section, we first present our approach, narrowing the evaluation taxonomy down to eight measurable dimensions aligned with key pedagogical strategies (Jurenka et al., 2024; Hennessy et al., 2016). These dimensions are most suitable for the student mistake remediation task and are based on the learning sciences principles." |
| Q16 | 3 | input_ontology | "We then dive into the details of each dimension and its relationship to previous research. An overview of the taxonomy is presented in Table 2." |
| Q17 | 3 | input_ontology | "Encourage active learning (Chi and Wylie, 2014; Oakley and Sejnowski, 2021): The tutor should encourage students to actively participate in the discussion and practice rather than passively receive information. The tutor can achieve this by not revealing the answer immediately and scaffolding guidance." |
| Q18 | 3 | input_ontology | "Adapt to students' goals and needs (King and South, 2017): The tutor should respond coherently by adapting to the current state and goals of the student's learning rather than following a pre-defined learning path. In the context of student mistake remediation, this happens when the tutor identifies the mistake, pinpoints its location, and responds coherently." |
| Q19 | 3 | input_ontology | "Manage cognitive load and enhance metacognitive skills (Mayer, 2002; Dehaene, 2020; Cohen et al., 2021): The tutor should present the information in a structured manner, with elaboration and examples in manageably small chunks that enable the student to generalize their learning skills beyond the current problem. For the task at hand, this can be achieved by providing appropriate guidance." |
| Q20 | 3 | input_ontology | "Foster motivation and stimulate curiosity (Keller, 1987; Patall et al., 2008): The tutor" |
| Q21 | 4 | input_ontology | "Since all dialogues in the dataset contain a mistake made by the student, a good-quality response from the tutor should include the relevant mistake identification." |
| Q22 | 4 | input_ontology | "A good tutor response should not only notify the student of the committed error but also point to its location in the answer and outline what the error is to help the student remediate it in their subsequent response." |
| Q23 | 4 | output_ontology | "Since most dialogues are relatively short and present contexts for the mistakes made early in the student's solution, a good tutor strategy is not to reveal the answer to the student immediately but rather provide helpful guidance." |
| Q24 | 4 | output_ontology | "In addition to not revealing the answer immediately, a good tutor response should provide the student with relevant and helpful guidance, such as a hint, an explanation, or a supporting question." |
| Q25 | 4 | output_ontology | "Once the guidance is provided to a student, it should be clear from a good tutor response what the student should do next; in other words, the tutor response should not be vague, unclear, or a conversation stopper." |
| Q26 | 4 | output_ontology | "We postulate that a high-quality tutor's response should be logically consistent with the student's previous responses." |
| Q27 | 4 | output_ontology | "In addition to addressing student mistakes, a good tutor should encourage them and avoid using toxic language, which is aligned with the care dimension in the evaluation schema of Wang et al. (2024a)." |
| Q28 | 4 | output_ontology | "This dimension is particularly critical for LLM-based AI tutors, as they often exhibit unpredictable behavior." |
| Q29 | 4 | output_ontology | "Effective tutoring requires that students feel a connection with the tutor, which is more likely when the tutor's responses appear human-like rather than robotic." |
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
| Q65 | 6 | output_ontology | "The desired labels for each dimension are detailed in Table 2." |
| Q66 | 6 | output_form | "(2) Annotation Correlation (AC): This metric is based on Pearson's correlation (Sedgwick, 2012), and it estimates the correlation between LLM-generated and human annotations (Kim et al., 2024), allowing us to assess the reliability of LLMs as evaluators in the context of student mistake remediation." |
| Q67 | 7 | output_form | "Table 3 shows DAMR scores for each LLM across all eight dimensions." |
| Q68 | 7 | output_content | "We consider human-based evaluations as gold standard." |
| Q69 | 7 | output_form | "Both these LLMs perform well in identifying students' mistakes and their exact location, with Llama-3.1-405B having a slight edge as GPT-4 reveals the answer approximately 47% of the time, making its responses less actionable and impacting student's learning experience." |
| Q70 | 7 | output_ontology | "This shows that GPT-4 is a good question-answering system but a relatively poor tutor." |
| Q71 | 7 | output_form | "Among these three LLMs, Gemini performs the worst as its responses are often incoherent, while also achieving low scores for mistake identification and exact location." |
| Q72 | 7 | output_form | "Phi3 is the worst-performing LLM model in this context, with the lowest score for coherence, suggesting that the responses from Phi3 are often irrelevant to the conversation context, as well as overall low scores in other dimensions." |
| Q73 | 7 | output_form | "This underscores the model's inadequate capacity for contextual understanding and semantic alignment in educational dialogues considered in this study." |
| Q74 | 7 | output_ontology | "In the few cases where Phi3 demonstrates some competence, it frequently reveals the answer, reflecting more of a question-answer system than a pedagogical tutor behavior." |
| Q75 | 7 | output_form | "Moreover, its outputs tend to be robotic, template-based and lack the nuance expected in human responses." |
| Q76 | 7 | output_form | "In contrast, despite having fewer parameters, Llama-3.1-8B demonstrates reasonable performance, albeit still below that of larger LLMs." |
| Q77 | 7 | output_form | "Specifically, its responses are coherent, strategically avoid immediate answer revelation, robustly identify and rectify mistakes, and exhibit human-like behavior, as evidenced by the DAMR scores." |
| Q78 | 7 | output_content | "We also investigated the pedagogical value of human responses for both Novice and Expert." |
| Q79 | 7 | output_content | "It can be observed that Novice responses do not have a high score for guidance and are poor in terms of actionability (DAMR score of 1.67)." |
| Q80 | 7 | output_content | "Furthermore, the responses are generally short and ambiguous, such as "this is a good try," which leads to lower scores for mistake identification and location." |
| Q81 | 7 | output_content | "At the same time, they often do not reveal the answer." |
| Q82 | 7 | input_content | "*For the Novice, we have considered only 60 dialogues from the Bridge dataset." |
| Q83 | 7 | output_form | "The DAMR scores for Novice are reported on these 60 instances, while for Expert and all LLMs, all 192 instances were considered." |
| Q84 | 8 | output_ontology | "Can a tutor achieve a higher DAMR score for actionability while receiving a lower score for providing guidance? This is possible since we consider only factually correct guidance as useful (see Table 4)." |
| Q85 | 8 | output_ontology | "At the same time, even incorrect or incomplete guidance can lead to certain actions on the part of the student and can foster their curiosity, thus providing them with learning opportunities." |
| Q86 | 8 | output_ontology | "This further demonstrates the need to treat the dimensions as independent." |
| Q87 | 8 | output_content | "In terms of the other qualities of the Expert responses, they do not normally reveal the answer and tend to include scaffolding; however, there are a small number of instances where they failed to identify the mistake or its location." |
| Q88 | 8 | output_content | "Overall, we conclude that human responses from Expert are significantly better than Novice." |
| Q89 | 8 | output_ontology | "Our findings on the Tutor Tone align with those of Wang et al. (2024a) – in task-oriented conversations, AI tutors tend to be more Neutral than Encouraging." |
| Q90 | 8 | output_ontology | "When we combine these two labels into "Non-offensive", the DAMR score reaches 100% as we observe no offensive responses from any LLMs or humans." |
| Q91 | 8 | output_form | "We observe high scores for most of the LLMs on human-likeness, which demonstrates their capability to generate human-like output with minimal or no grammatical and fluency mistakes, showing the timely nature of our study, which focuses more on in-depth semantic and pedagogical aspects of tutor responses rather than only on superficial attributes like grammaticality and fluency." |
| Q92 | 8 | input_content | "As discussed in Section 5.1, the conversational contexts in the Bridge dataset are typically very short (see Table 7) and the dialogues are grounded in elementary math operations, so most models are able to identify the mistakes and their locations." |
| Q93 | 8 | input_content | "However, they struggle to provide appropriate guidance without revealing the answer because the mistakes are generally related to quite basic operations like addition or multiplication, often in a one-step type of mathematical problems." |
| Q94 | 8 | output_form | "Still, models like GPT-4 and Llama-3.1-405B are able to offer some reasonable guidance." |
| Q95 | 8 | input_content | "In contrast, for MathDial, the contexts are longer, the mistakes are grounded in reasoning, and the responses are more structured." |
| Q96 | 8 | output_ontology | "Yet, many LLMs do not meet the expectations for each dimension of the taxonomy, as discussed earlier." |
| Q97 | 8 | input_content | "Combining both types of data in MRBench makes it both challenging and comprehensive." |
| Q98 | 8 | output_ontology | "In summary, all LLMs and even human tutors lack some pedagogical abilities required for effective tutoring." |
| Q99 | 8 | output_form | "While Llama-3.1-405B is the most effective, followed by Mistral and other state-of-the-art models, GPT-4 reveals the answer too quickly." |
| Q100 | 8 | output_form | "Gemini is less coherent and accurate, and Sonnet focuses on human-likeness and encouraging tone but is less effective in other dimensions." |
| Q101 | 8 | output_form | "Phi3 is the worst-performing model according to our analysis, as it fails to understand the context, while Llama-3.1-8B, despite being smaller, performs reasonably well." |
| Q102 | 8 | output_content | "Human responses are also not perfect – Novice responses are ambiguous and short, whereas Expert responses are more focused on actionability and less on other dimensions." |
| Q103 | 8 | input_ontology | "Overall, the proposed taxonomy precisely categorizes performance across 8 dimensions, reflecting the current state-of-the-art in AI tutors." |
| Q104 | 8 | output_ontology | "Our study demonstrates that there is a considerable room for improvement in the pedagogical abilities of AI tutors." |
| Q105 | 8 | output_content | "We also performed annotations using Prometheus2 and Llama-3.1-8B as critic LLMs." |
| Q106 | 8 | output_form | "The correlation scores with human annotations are presented in Appendix Tables 5 and 6, respectively." |
| Q107 | 8 | output_content | "Across both LLMs, it can be observed that most of the correlation scores are negative (except for the human-likeness dimension), indicating that the annotations from the LLMs are unreliable for the challenging pedagogical dimensions." |
| Q108 | 8 | output_form | "Prometheus2 is not trained on our taxonomy dimensions, except for the general human-likeness dimension, where the model shows slightly better correlations with positive scores." |
| Q109 | 8 | output_content | "We believe both LLMs have a limited understanding of rich pedagogical concepts, as they were not specifically trained on pedagogically rich datasets." |
| Q110 | 8 | output_form | "At the same time, we acknowledge that the experiments presented in this work are preliminary" |
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
| Q126 | 10 | input_content | "This research is partially supported by Google through the Google Academic Research Award (GARA) 2024. We are grateful for their support. We also extend our gratitude to the campus supercomputing center at MBZUAI." |
| Q127 | 10 | output_ontology | "strongly believe that this study will help shed light on the current capabilities of LLMs in the context of educational dialogues, and the insights gained from this study may help mitigate issues related to the use of LLMs in the educational domain in the future." |
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
| Q148 | 15 | output_form | "The template is based on the insights drawn from the Prometheus2 model's official guidelines." |
| Q149 | 16 | output_form | "Pedagogical ability assessment of different LLMs using the DAMR scores (in %) across eight evaluation dimensions with human evaluation on the Bridge data." |
| Q150 | 16 | output_form | "Pedagogical ability assessment of different LLMs using the DAMR scores (in %) across eight evaluation dimensions with human evaluation on the MathDial data." |
| Q151 | 16 | input_content | "'-' indicates that DAMR scores for Novice are not available for MathDial data." |
| Q152 | 17 | output_content | "Figure 4: An example from the annotator training phase for the Mistake Identification dimension." |
| Q153 | 17 | output_content | "Figure 5: An example from the annotator testing phase for the Revealing of the Answer dimension." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://ftp.bills.com.au/lunar-tips/icse-student-count-in-india-2023-overview-1767648175 |
| WEB-2 | https://ncert.nic.in/pdf/syllabus/06Math%20(I-V).pdf |
| WEB-3 | https://cbseportal.com/NCERT/syllabus/maths-primary-class |
| WEB-4 | https://cbseportal.com/NCERT/syllabus/maths-secondary |
| WEB-5 | https://www.tiwariacademy.com/ncert-solutions/class-8/maths/ |
| WEB-6 | https://arxiv.org/html/2404.13099v1 |
| WEB-7 | https://aclanthology.org/2022.lrec-1.373.pdf |
| WEB-8 | https://www.emergentmind.com/topics/gsm8k |
| WEB-9 | https://arxiv.org/html/2507.02180v1 |
| WEB-10 | https://datareportal.com/reports/digital-2024-india |
| WEB-11 | https://muftinternet.com/blog/usage-statistics-internet-and-mobile-users-in-india-2025/ |
| WEB-12 | https://www.dataforindia.com/comm-tech/ |
| WEB-13 | https://www.imarcgroup.com/india-smartphone-market |
| WEB-14 | https://factly.in/data-more-than-90-students-appearing-in-secondary-higher-secondary-exams-are-from-state-regional-boards/ |
| WEB-15 | https://cissikar.com/blog/how-many-cbse-schools-in-india |
| WEB-16 | https://en.wikipedia.org/wiki/Council_for_the_Indian_School_Certificate_Examinations |
| WEB-17 | https://arxiv.org/html/2507.10579v1 |
| WEB-18 | https://aclanthology.org/2025.naacl-long.57.pdf |
| WEB-19 | https://www.mdpi.com/2076-3417/15/2/671 |
| WEB-20 | https://arxiv.org/pdf/2508.02442 |
| WEB-21 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-22 | https://www.cookieyes.com/blog/india-digital-personal-data-protection-act-dpdpa/ |
| WEB-23 | https://ksandk.com/data-protection-and-data-privacy/child-data-protection-under-dpdp-act-parental-consent-rules/ |
| WEB-24 | https://www.dpdpa.com/dpdpa2023/chapter-2/section9.html |
| WEB-25 | https://law.asia/childrens-data-protection-dpdp-act/ |
| WEB-26 | https://www.orfonline.org/expert-speak/dpdp-rules-and-the-future-of-child-data-safety |
| WEB-27 | https://www.careerlauncher.com/cbse-ncert/class-8/maths/ |
| WEB-28 | https://en.wikipedia.org/wiki/Central_Board_of_Secondary_Education |

---

