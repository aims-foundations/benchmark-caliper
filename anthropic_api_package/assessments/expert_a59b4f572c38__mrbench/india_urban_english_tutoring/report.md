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
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology | 3 | Moderate gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 4 | Minor gaps | high |
| **Average** | **3.2** | | |

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

MRBench is a well-constructed, narrowly-scoped benchmark for evaluating AI tutor responses to mathematics mistakes, with strengths in taxonomy validation, annotator training, and metric design. For the Delhi/Mumbai Grade 1–8 mathematics teacher deployment, validity is strongly preserved on dimensions involving curricular ontology (IO), input form (IF), and output form (OF), all of which align with the user's accepted text-only English, curriculum-agnostic deployment. However, two HIGH-priority dimensions show significant validity concerns: (a) Input Content — Bridge and MathDial were sourced from Western academic settings and depict student communication dynamics (extended verbalization, structured Socratic exchanges) that the user explicitly identified as mismatched with Indian classroom realities; (b) Output Content — gold-standard labels were produced by four MBZUAI CS post-graduates without required teaching experience and without documented South Asian pedagogical expertise, while the user expects systematic divergence on the most-critical 'providing guidance' dimension between this pool and Indian professional teachers. A MODERATE-priority concern attaches to Output Ontology: equal-weight DAMR does not reflect the user's prioritization of 'providing guidance,' and that dimension's rubric implicitly favors Socratic scaffolding over the direct-correction norms valued by Indian teachers. Field-level evidence (MathTutorBench, Shiksha Copilot study, 2025 ITS survey) confirms these are not local artifacts but field-wide gaps in pedagogically- and cross-culturally-grounded benchmarking.

## Practical Guidance

### What This Benchmark Measures

MRBench can support evaluation of (i) whether AI tutor responses identify mathematical mistakes and avoid revealing answers immediately, (ii) whether responses are coherent and human-like, and (iii) the relative pedagogical performance of different LLMs on a Western-default rubric. For the Indian metro deployment, IO/IF/OF dimensions are well-aligned, so the benchmark is structurally usable as a screening tool for ruling out clearly poor tutors (e.g., Phi3, GPT-4's answer-revealing tendency) before deployment-specific validation.

### Construct Depth

The benchmark probes pedagogical quality at the level of individual tutor turns [Q119–Q121] across eight learning-science-grounded dimensions, with substantial within-pool annotator agreement (κ=0.71) [Q61]. However, depth is limited in three ways: (1) it does not assess cumulative learning impact [Q120, Q121]; (2) the most-critical dimension for this deployment ('providing guidance') is operationalized through a Socratic lens that may not match Indian acceptability criteria; (3) ground-truth labels reflect a homogeneous, non-Indian, non-teacher annotator pool, so the labels' convergent validity with Indian professional teachers' judgments is unestablished.

### What Else You Need

To use MRBench validly for this deployment, supplement with: (a) re-annotation of at least the 'providing guidance' dimension by Delhi/Mumbai Grade 1–8 teachers (addresses OC); (b) a small-N expansion of dialogues sampled from authentic Indian metropolitan classrooms or a pilot adaptation of Bridge/MathDial dialogues vetted by Indian teachers for realism (addresses IC); (c) a deployment-specific weighted DAMR with 'providing guidance' as dominant weight (addresses OO); (d) qualitative review of the guidance rubric's desired-label definition to determine whether direct-correction responses are appropriately rewarded (addresses OO/OC). MathTutorBench [WEB-16] is not a substitute — it shares the same Western pedagogical default.

## Dimension Details

### Input Ontology — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
The user explicitly accepted curriculum-agnostic math errors as sufficient and confirmed the eight pedagogical dimensions are necessary and sufficient (elicitation Q1, Q3), reducing concern at the taxonomy level. The benchmark covers two difficulty levels (elementary and middle-school) [Q143, Q144], aligning with Grade 1–8 scope. The taxonomy is curriculum-agnostic by construction [Q117, Q118] and was validated against learning-science principles with a pilot confirming necessity and sufficiency [Q129, Q131, Q132]. Minor concerns: the taxonomy reflects a Socratic/answer-withholding pedagogical model [Q17, Q23] that the deployment context flags as partially conflicting with Indian direct-correction norms, but this is more an output-rubric concern (handled in OO/OC) than an input-category gap. No Indian curriculum-specific subcategories (e.g., NCERT topics, lakh/crore conventions) are present, but the user explicitly stated these are not required.

**Strengths:**
- Eight-dimension taxonomy was iteratively validated and confirmed necessary and sufficient by pilot annotators [Q129, Q131, Q132]
- Curriculum-agnostic design [Q117] aligns with the user's explicit acceptance criterion
- Coverage of both elementary and middle-school difficulty levels matches Grade 1–8 scope [Q143, Q144]
- Task is narrowly and clearly defined (mistake remediation in math) [Q12, Q13], reducing construct-irrelevant variance

**Checklist:**

- **IO-1**: Test case categories required for the deployment are mistake-remediation dialogues at Grade 1–8 math difficulty; the user accepted curriculum-agnostic errors as sufficient (elicitation Q1). The benchmark covers elementary [Q44, Q45] and middle-school [Q48, Q49] difficulty levels. — _Sources: Q12, Q44, Q48_
- **IO-2**: No regionally-relevant categories are documented as omitted at the taxonomy level; the user confirmed the eight dimensions are necessary and sufficient (elicitation Q3). NCERT-specific topics and Indian conventions (e.g., lakhs/crores) are absent but explicitly deemed unnecessary by the user. — _Sources: Q132_
- **IO-3**: No taxonomy categories are flagged as irrelevant; all eight dimensions [Q1, Q15] are accepted as applicable to the deployment. — _Sources: Q1, Q15_
- **IO-4**: No category-level gaps that would harm content validity are identified given the user's curriculum-agnostic acceptance criterion. Sub-national board variation (CBSE/ICSE/State Board/IB) is a flagged gap but operates at content level rather than taxonomy level. — _Sources: Q117_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q117] 'The proposed taxonomy primarily focuses on the task of the student mistake remediation in the domain of mathematics.' (p.9)
- [Q129] 'Through an iterative analysis of the taxonomy, we identify eight dimensions that comprehensively assess tutor response quality in the context of mistake remediation.' (p.12)
- [Q132] 'our validation pilot study (see Section 4.2) confirmed that the selected eight dimensions are both necessary and sufficient for evaluating tutor response quality in dialogues aimed at mistake remediation.' (p.12)
- [Q143] 'including both datasets in MRBench ensures diversity and provides for a good mix of easy and difficult mathematical problems' (p.14)
- [Q144] 'The problems covered in the Bridge dataset are at the elementary school level, whereas those in MathDial are at the middle school level.' (p.14)

</details>

**Information gaps:**
- Whether sub-national curriculum variation (CBSE vs. ICSE vs. Maharashtra State Board vs. IB) affects category-level coverage of mistake types relevant to specific teacher subgroups

**Requires expert verification:**
- Confirmation from a broader Indian teacher pool (beyond the elicited user) that no additional pedagogical dimensions specific to Indian classrooms (e.g., exam-readiness framing as a distinct dimension) are needed

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
This is a HIGH-priority dimension per elicitation. The benchmark content is drawn from Bridge [Q44–Q47] and MathDial [Q48, Q49], both Western-academic English-language datasets. The user explicitly confirmed (elicitation Q2) meaningful mismatches in student communication style: Indian Grade 1–8 students are briefer, more deferential, and procedure-focused, while MathDial features extended multi-turn structured dialogues [Q95]. The Bridge selection criterion centers on student last-utterance error [Q47] but does not document misconception types relevant to Indian rote-procedural traditions, L1-interference errors, or NCERT-specific algorithmic conventions. No documentation acknowledges cultural provenance as a limitation. MathDial's student is an LLM, not a real student [Q48], introducing an additional layer of cultural distance from authentic Indian student behavior. Field-level evidence confirms this is not a local artifact: no Indian-classroom-grounded math tutoring benchmark exists [WEB-16, WEB-19].

**Strengths:**
- Mathematical content is broadly familiar across cultures (user confirmed math content feels recognizable; elicitation Q2)
- Both datasets are grounded in real student errors [Q41, Q42, Q43], providing authentic mistake-remediation contexts
- Manual quality inspection [Q51] and selection criteria [Q47] ensure each instance contains a genuine mistake/confusion

**Checklist:**

- **IC-1**: Inputs do not require region-specific cultural or geographic knowledge — math content is curriculum-agnostic [Q41–Q43]. However, recognizing realistic student communication patterns (brevity, deference, procedural focus) is regionally specific, and Indian teachers may find the depicted dialogue dynamics unrepresentative of their classrooms (elicitation Q2). — _Sources: Q41, Q42, Q43_
- **IC-2**: Cultural alignment is partial. Math content aligns; conversational dynamics do not. The user identified meaningful mismatch in interaction norms (elicitation Q2). The paper does not acknowledge cultural provenance [no quote addresses this]. — _Sources: Q44, Q48, Q95, WEB-15_
- **IC-3**: Inputs implicitly require familiarity with Western-style extended student verbalization [Q95] and Socratic dialogue framing. While teachers can read these dialogues fluently in English, judging realism may be affected. INSUFFICIENT DOCUMENTATION on whether specific dialogue exemplars contain culturally Western references; would require dataset-level inspection. — _Sources: Q95_
- **IC-4**: No regional annotators were recruited; the annotation team was MBZUAI-based [Q31, Q6] with no documented Indian or South Asian educational expertise. — _Sources: Q31_
- **IC-5**: Documented content issues harming content validity: (a) Western-sourced student communication dynamics [Q44, Q48, Q95] mismatched with Indian classroom norms (elicitation Q2); (b) absence of L1-interference and rote-procedural error types in selection criteria [Q47]; (c) MathDial uses LLM-as-student [Q48] rather than real students. Field-wide gap confirmed by [WEB-16] (MathTutorBench shares same Western provenance) and [WEB-19] (no India-specific ITS benchmark exists). — _Sources: Q44, Q48, Q95, WEB-16, WEB-19_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q44] 'The Bridge dataset (Wang et al., 2024a) comprises partial dialogue interactions between real human tutors and students at the elementary level' (p.5)
- [Q48] 'The dialogues in the MathDial dataset (Macina et al., 2023) consist of complete multi-turn conversations between a real human tutor and an LLM acting as a student' (p.5)
- [Q95] 'In contrast, for MathDial, the contexts are longer, the mistakes are grounded in reasoning, and the responses are more structured.' (p.8)
- [Q47] 'the key one was that the student's last utterance (or last few utterances) should exhibit an error or confusion.' (p.5)
- [Q97] 'Combining both types of data in MRBench makes it both challenging and comprehensive.' (p.8)

*Web sources:*
- [WEB-16] MathTutorBench (EMNLP 2025) is also Western-sourced and operationalizes good tutoring as Socratic withholding, confirming field-wide cultural provenance gap
- [WEB-19] 2025 ITS evaluation survey identifies absence of pedagogy-driven, cross-cultural evaluation frameworks; no India-specific ITS benchmark cited
- [WEB-15] Indian teacher-AI collaboration study (Shiksha Copilot) confirms Indian teachers face structural misalignment with Western-default AI outputs

</details>

**Information gaps:**
- No empirical inspection of whether specific Bridge/MathDial dialogues contain culturally Western references (e.g., names, contexts, units beyond math)
- No documentation of misconception type distribution and whether it covers Indian-prevalent error patterns
- Whether L1-interference errors common in Indian Grade 1–8 students appear in either dataset

**Requires expert verification:**
- Indian teacher review of a sample of Bridge and MathDial dialogues for realism of student communication style
- Comparison of MRBench misconception types with NCERT-published error analysis [WEB-13]

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
The benchmark is text-only English [Q133, Q134, Q147], matching the deployment's text-based English mobile/enterprise application interface. The target population is fluent in English professionally. No script mismatch, no multimodal mismatch, and adequate infrastructure (urban Tier-1 internet penetration ~80–88%, smartphone access near-universal for professional teachers) [WEB-5, WEB-6, WEB-7] support text-based English signal delivery. Minor concern: no multimodal capture of handwritten student work, which is common in actual Indian classrooms, but the evaluator-role deployment (teachers judging text dialogues) does not require this. The user weighted IF as LOWER priority.

**Strengths:**
- Text-only English [Q133, Q134] matches deployment interface exactly
- No script or modality mismatch — both benchmark and deployment are Latin-script English
- Target population has fluent English and reliable mobile infrastructure [WEB-5, WEB-7]
- Length and turn metadata documented per dataset [Q141, Q142, Q147]

**Checklist:**

- **IF-1**: Signal distributions match: text-based English dialogues [Q133, Q134] correspond to deployment's text-based English interface. No image, audio, or specialized capture parameters required. — _Sources: Q133, Q134_
- **IF-2**: Regional infrastructure supports the format: urban Indian metro internet penetration is high (~80–88%) and smartphone access is near-universal for professional teachers [WEB-5, WEB-6]. — _Sources: WEB-5, WEB-6, WEB-7_
- **IF-3**: Domain-specific form differences are minimal. The benchmark does not include images of handwritten work [no quote], which is common in Indian classrooms; however, the evaluator-role deployment (teachers judging text-based AI+human responses) does not require multimodal input. — _Sources: Q141_
- **IF-4**: No form mismatches significantly harm external validity for this deployment. Conversation length differences between Bridge and MathDial [Q141, Q142] are documented and do not introduce mismatch with the deployment. — _Sources: Q141, Q142_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q133] 'The prompt template used to generate responses from the seven considered LLMs for both the Bridge and MathDial datasets is shown in Figure 2.' (p.12)
- [Q141] 'It can be observed that the conversation history and response lengths from different LLMs and humans are generally shorter in the Bridge dataset compared to the MathDial dataset.' (p.14)
- [Q147] 'In all cases, length is estimated using the number of characters.' (p.14)

*Web sources:*
- [WEB-5] Urban Tier-1 internet penetration ~88%, broadband >50% in urban households
- [WEB-6] India had 660 million smartphone users as of 2024–2025
- [WEB-7] National mobile data median speed 94.62 Mbps in early 2024

</details>

---

### Output Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
MODERATE priority per elicitation. The eight dimensions and three-tier labeling [Q58, Q59] are accepted by the user as necessary and sufficient (elicitation Q3). However, two structural concerns affect deployment validity. First, DAMR weights all eight dimensions equally [Q64], whereas the user identified 'providing guidance' as the single most critical dimension; using DAMR directly as an acceptability proxy would dilute the signal Indian teachers care most about. Second, the 'providing guidance' rubric operationalizes guidance via Socratic scaffolding (hints, supporting questions, not revealing answers) [Q23, Q24], which the user (elicitation Q4) and field evidence [WEB-15, WEB-16] indicate may not match Indian direct-correction expectations — a structural validity concern about how the construct itself is operationalized. The decision rule for the most-critical dimension may encode a non-regional pedagogical value. Treating dimensions as orthogonal [Q30] is acknowledged as a simplification [Q116, Q120, Q121]. Tone label collapse to 'Non-offensive' [Q90] reaches 100% compliance, providing little discriminative signal.

**Strengths:**
- Eight dimensions accepted as necessary and sufficient by the user (elicitation Q3) and pilot validation [Q132]
- Per-dimension DAMR scores reported separately [Q67], enabling manual re-weighting toward 'providing guidance' [WEB-19 confirms re-weighting feasible]
- Three-tier labeling [Q58, Q59] supports nuanced acceptability judgments rather than binary
- Desired labels are explicitly documented [Q65, Q128], making the decision rule auditable

**Checklist:**

- **OO-1**: Output label categories are dimensionally relevant to the deployment — all eight are accepted by the user (elicitation Q3). However, the decision rule for 'providing guidance' favors Socratic scaffolding [Q23, Q24], which may not align with Indian direct-correction norms (elicitation Q4, [WEB-15]). — _Sources: Q58, Q59, Q23_
- **OO-2**: No dimensions are flagged as missing per user elicitation (Q3). However, exam-readiness framing — culturally salient for Indian teachers per cultural notes — is not a separate dimension; it is implicitly subsumed under guidance/actionability without dedicated operationalization. — _Sources: Q132_
- **OO-3**: The 'providing guidance' dimension's desired label encodes a Socratic/answer-withholding value [Q23 'a good tutor strategy is not to reveal the answer to the student immediately but rather provide helpful guidance']. This is a non-regional pedagogical assumption per elicitation Q4 and field evidence [WEB-15, WEB-16]. — _Sources: Q23, Q24, WEB-15, WEB-16_
- **OO-4**: Stakeholder-driven taxonomy redesign is not required (user accepts dimensions) but rubric recalibration of the 'providing guidance' dimension and DAMR re-weighting are recommended. — _Sources: Q64_
- **OO-5**: Structural validity concern: equal-weight DAMR [Q64] does not match the user's prioritization of 'providing guidance' as dominant. Content validity concern: the guidance dimension's decision rule may encode a Western pedagogical default [Q23, Q24] that diverges from Indian acceptability criteria. Both are documented limitations enabling targeted remediation. — _Sources: Q64, Q23, Q90, Q120_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q58] 'Each dimension was annotated using a three-tier labeling system' (p.6)
- [Q64] 'Desired Annotation Match Rate (DAMR): This metric quantifies the percentage of responses from each human or LLM-based tutor that received the desired annotation labels.' (p.6)
- [Q23] 'a good tutor strategy is not to reveal the answer to the student immediately but rather provide helpful guidance.' (p.4)
- [Q24] 'a good tutor response should provide the student with relevant and helpful guidance, such as a hint, an explanation, or a supporting question.' (p.4)
- [Q30] 'we explicitly instructed all annotators to treat each dimension as independent and orthogonal to minimize confounding factors' (p.4)
- [Q90] 'When we combine these two labels into "Non-offensive", the DAMR score reaches 100% as we observe no offensive responses from any LLMs or humans.' (p.8)
- [Q120] 'one of the limitations is that it does not consider the tutoring dialogues' impact on the overall student learning.' (p.9)

*Web sources:*
- [WEB-15] Indian teachers value direct, curriculum-aligned outputs over Socratic scaffolding; misalignment with Western-default AI outputs documented
- [WEB-16] MathTutorBench reward model also operationalizes good tutoring as Socratic withholding, confirming field-wide rubric default
- [WEB-19] 2025 ITS survey notes no published weighted DAMR variants; per-dimension re-weighting remains an open methodological gap

</details>

**Information gaps:**
- Whether the 'providing guidance' rubric, when applied with Indian-specific definitions of acceptable guidance, would yield substantially different desired labels — requires Indian teacher rubric review
- No published weighted DAMR methodology calibrated to specific evaluator populations [WEB-19]

**Requires expert verification:**
- Indian teacher review of the 'providing guidance' rubric definition [Q24] to determine whether direct-correction responses would be appropriately rewarded under current desired labels

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
HIGH priority per elicitation. The annotation pool is four MBZUAI CS post-graduates [Q31] explicitly without required teaching experience [Q32], with no documented South Asian educational expertise. The user expects systematic divergence (elicitation Q4) between Indian teachers' guidance-quality judgments and this annotator pool's, particularly on direct correction vs. Socratic probing, exam-readiness framing, and teacher-directed pedagogy. Field evidence corroborates: Indian teachers structurally value direct, curriculum-aligned outputs over Western-default Socratic scaffolding [WEB-15]. Inter-annotator agreement (Cohen's κ=0.71, Fleiss' κ=0.65) [Q39, Q61] demonstrates internal consistency within the MBZUAI pool but provides no evidence of convergent validity with Indian teachers — the gold standard [Q68] reflects MBZUAI annotators' implicit pedagogical model. LLM-critic correlations were predominantly negative [Q107], confirming pedagogical judgments are not easily automatable. The most-critical dimension's labels were calibrated by annotators whose pedagogical priors likely diverge from Indian professional teachers'. No India-specific annotation study exists [WEB-19].

**Strengths:**
- Rigorous in-house training and validation protocols [Q33, Q34, Q35, Q36, Q135, Q136, Q137]
- Substantial inter-annotator agreement within the MBZUAI pool (Cohen's κ=0.71) [Q61]
- Annotator demographics are transparently documented [Q31, Q6, Q32], enabling regional gap analysis
- Limitations on LLM-as-evaluator are explicitly reported [Q107, Q114]

**Checklist:**

- **OC-1**: Ground truth labels do not reflect Indian regional stakeholder perspectives. Annotators are MBZUAI CS post-graduates [Q31] with no required teaching experience [Q32] and no documented South Asian pedagogical expertise. — _Sources: Q31, Q32, Q6_
- **OC-2**: Systematic disagreement is expected per user elicitation (Q4) and field evidence [WEB-15]. Indian teachers prioritize direct correction, exam-readiness, and teacher-directed pedagogy; MBZUAI annotators were instructed to judge from a 'student or potential AI tutor user' perspective [Q32], not a teacher's. — _Sources: Q32, WEB-15_
- **OC-3**: Annotator demographics are documented [Q31, Q6]: four annotators, two male / two female, all post-graduate CS, MBZUAI Abu Dhabi. No teaching experience required [Q32]. No information on cultural/national background beyond institutional affiliation. — _Sources: Q31, Q6, Q32_
- **OC-4**: Re-annotation by representative Indian Grade 1–8 teachers is strongly recommended for this deployment, particularly on the 'providing guidance' dimension. No such re-annotation exists [WEB-19]. — _Sources: WEB-19_
- **OC-5**: Aggregation uses pairwise inter-annotator agreement on overlapping subset (40 of 192 instances) [Q57]; the remaining 152 instances are single-annotated. With a homogeneous annotator pool [Q31], minority pedagogical perspectives (e.g., direct-correction-favoring) cannot be detected. — _Sources: Q57, Q31_
- **OC-6**: Convergent validity concern: gold labels [Q68] correlate with MBZUAI annotators' Western/generic-academic pedagogical priors, not Indian teachers' judgments. External validity concern: original judgments are unlikely to generalize to the Indian metro teacher target context (elicitation Q4, [WEB-15]). — _Sources: Q68, Q32, WEB-15_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'The annotation team consisted of two male and two female annotators, with all four annotators holding at least a post-graduate degree in Computer Science and being proficient in English.' (p.5)
- [Q32] 'we do not require annotators to have direct teaching experience, as understanding of the mathematical tasks at the middle school level and being able to judge the responses from the perspective of a potential user of such AI tutors (or a student), rather than specifically a teacher, is sufficient.' (p.5)
- [Q6] 'Mohamed bin Zayed University of Artificial Intelligence, Abu Dhabi, UAE.' (p.1)
- [Q61] 'The annotators reached an average Cohen's kappa score of 0.71, which indicates substantial inter-annotator agreement' (p.6)
- [Q68] 'We consider human-based evaluations as gold standard.' (p.7)
- [Q107] 'Across both LLMs, it can be observed that most of the correlation scores are negative (except for the human-likeness dimension), indicating that the annotations from the LLMs are unreliable for the challenging pedagogical dimensions.' (p.8)

*Web sources:*
- [WEB-15] Indian teachers face structural misalignment with Western-default AI outputs; value curriculum-aligned, direct guidance
- [WEB-19] No India-specific or cross-cultural ITS evaluation framework cited in 2025 survey
- [WEB-16] MathTutorBench (related Western-default benchmark) shares same annotator-cultural-provenance pattern

</details>

**Information gaps:**
- No measurement of inter-annotator agreement among Indian professional teachers on the same MRBench instances
- No published cross-cultural comparison of pedagogical-quality judgments on AI tutor responses
- No information on the annotators' national/cultural backgrounds beyond institutional affiliation

**Requires expert verification:**
- Pilot re-annotation of a MRBench subset by Delhi/Mumbai Grade 1–8 mathematics teachers, with κ comparison to original labels
- Targeted review of the 'providing guidance' dimension's desired labels by CBSE/NCERT-experienced educators

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
LOWER priority per elicitation. Output form (categorical labels [Q58, Q59], DAMR percentages, and Pearson correlations [Q64, Q66]) is appropriate for the deployment scenario where teachers render acceptability judgments on AI+human-augmented responses. The benchmark explicitly avoids unreliable NLG metrics like BLEU/BERTScore [Q4, Q7, Q8] in favor of pedagogically meaningful categorical scores. No mismatch with deployment output needs is identified. Minor concern: the benchmark reports per-dimension DAMR but no aggregate acceptability score weighted by deployment priorities; teams would need to compute their own weighted aggregate to map to a binary acceptable/unacceptable judgment, but this is straightforward.

**Strengths:**
- Categorical and percentage outputs map cleanly onto teachers' acceptability judgments
- Per-dimension reporting [Q67] supports custom re-weighting toward 'providing guidance'
- Explicit rejection of unreliable surface-level NLG metrics [Q4, Q7, Q8]
- Both DAMR (per-tutor performance) and AC (LLM-evaluator reliability) metrics provided [Q64, Q66]

**Checklist:**

- **OF-1**: Output modality (categorical labels and percentages) matches the deployment, where teachers judge acceptability of text responses [Q58, Q64]. No mismatch. — _Sources: Q58, Q64_
- **OF-2**: Text-to-speech is not relevant — both benchmark and deployment are text-only. — _Sources: Q133_
- **OF-3**: Target population is fluent in English with high literacy and professional qualifications [WEB-1, WEB-2]; accessibility is not a concern for the evaluator role. — _Sources: WEB-1, WEB-2_
- **OF-4**: No form mismatches harming external validity. Categorical/percentage outputs are appropriate. Aggregating per-dimension DAMR into a deployment-relevant acceptability score requires user-side weighting but is methodologically simple. — _Sources: Q64, Q66_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q58] 'Each dimension was annotated using a three-tier labeling system' (p.6)
- [Q64] 'Desired Annotation Match Rate (DAMR): This metric quantifies the percentage of responses from each human or LLM-based tutor that received the desired annotation labels.' (p.6)
- [Q66] 'Annotation Correlation (AC): This metric is based on Pearson's correlation' (p.6)
- [Q4] 'General domain-agnostic natural language generation (NLG) metrics ... are not well-suited for this context, as most of them fail to account for pedagogical values' (p.1)

*Web sources:*
- [WEB-1] Indian Grade 1–8 teachers in CBSE schools require B.Ed/D.El.Ed and pass CTET — high literacy and professional qualification
- [WEB-2] CTET eligibility confirms English literacy among target population

</details>

---

## Remediation Suggestions

### Output Content ⚠

**Gap:** Gold-standard labels were produced by MBZUAI CS post-graduates without required teaching experience [Q31, Q32] and no documented South Asian pedagogical expertise; user expects systematic divergence on guidance-quality judgments (elicitation Q4).

**Recommendation:** Conduct re-annotation of a representative MRBench subset (e.g., 40–60 instances spanning Bridge and MathDial) by 3–4 Delhi/Mumbai Grade 1–8 mathematics teachers with CBSE/ICSE/State Board representation. Compute Cohen's κ between Indian teachers and original MBZUAI labels per dimension; treat per-dimension divergence (especially on 'providing guidance') as the deployment-relevant validity adjustment.

### Output Content ⚠

**Gap:** 152 of 192 MRBench instances are single-annotated [Q57], so minority pedagogical perspectives within an already-homogeneous annotator pool [Q31] cannot be detected.

**Recommendation:** When recruiting Indian teacher re-annotators, ensure full overlap on the re-annotated subset (every instance labeled by ≥2 teachers) and report per-instance disagreement, not just aggregate κ. This surfaces minority-perspective patterns relevant to the diverse Indian metro teaching workforce.

### Input Content ⚠

**Gap:** Bridge and MathDial conversations reflect Western academic settings with extended student verbalization [Q44, Q48, Q95]; Indian Grade 1–8 students are briefer, more deferential, and procedure-focused (elicitation Q2). L1-interference and rote-procedural error types absent from selection criteria [Q47].

**Recommendation:** Pilot a small India-grounded supplement (~30–60 dialogues) collected from Delhi/Mumbai classrooms or simulated by Indian teachers, with student error types informed by NCERT error-analysis literature [WEB-13] and CBSE-EI competency-based items [WEB-14]. Use this supplement to test whether tutor performance rankings change relative to MRBench.

### Input Content ⚠

**Gap:** Sub-national board variation (CBSE, ICSE, Maharashtra State Board, IB) is unresolved; pedagogical expectations differ across boards.

**Recommendation:** Stratify Indian teacher annotators by board affiliation when conducting OC re-annotation. Report per-board DAMR alignment to detect whether deployment validity differs by school type, and use this to guide deployment scoping (e.g., initial rollout in CBSE schools where dominant pedagogical norm is best characterized).

### Output Ontology

**Gap:** DAMR weights all eight dimensions equally [Q64], but 'providing guidance' is the user-identified dominant acceptability criterion, and the guidance rubric encodes Socratic-scaffolding values [Q23, Q24] that may not match Indian direct-correction norms.

**Recommendation:** Implement deployment-specific weighted DAMR with 'providing guidance' as dominant weight. Additionally, recalibrate the 'providing guidance' desired labels through expert review: define what constitutes acceptable direct-correction guidance for Indian teachers and add this as an alternative acceptable response pattern, rather than treating answer revelation as monolithically negative.

### Output Ontology

**Gap:** The benchmark does not aggregate to a binary acceptability decision and does not consider cumulative learning impact [Q120, Q121].

**Recommendation:** Define a deployment-specific decision rule that maps weighted DAMR (or per-dimension thresholds) to a binary 'acceptable / not acceptable' label aligned with the deployment's evaluator-role requirement. Document the threshold transparently and audit against Indian teacher binary judgments on a held-out set.

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
| Q9 | 2 | output_content | "For a given input dialogue, there can be multiple valid, pedagogically correct ground truth responses, making detection of the optimal answer non-deterministic (Tack and Piech, 2022; Al-Hossami et al., 2024)." |
| Q10 | 2 | output_form | "Additionally, these metrics can be easily manipulated; for instance, simple responses like "Hello" or "teacher:" (Baladón et al., 2023; Jurenka et al., 2024) can inflate scores." |
| Q11 | 2 | output_form | "In this section, we first briefly overview and discuss the limitations of the existing general-purpose NLG metrics and then turn to pedagogically-oriented approaches to evaluation." |
| Q12 | 3 | input_ontology | "In this work, we focus on educational dialogues between a student and a tutor in the mathematical domain. Specifically, the conversations are grounded in students' mistakes or confusions, and the AI tutor aims to respond in order to remediate such mistakes or confusions." |
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
| Q39 | 5 | output_form | "To measure inter-annotator agreement, we computed Fleiss' kappa value, which for this annotation experiment equals 0.65, indicating substantial agreement." |
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
| Q53 | 6 | input_content | "We consider state-of-the-art LLMs of various sizes and capabilities, including: GPT-4 (Achiam et al., 2023), Gemini (Reid et al., 2024), Sonnet (Anthropic, 2024), Mistral (Jiang et al., 2023), Llama-3.1-8B and Llama-3.1-405B (Dubey et al., 2024), and Phi3 (Abdin et al., 2024)." |
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
| Q85 | 8 | output_content | "At the same time, even incorrect or incomplete guidance can lead to certain actions on the part of the student and can foster their curiosity, thus providing them with learning opportunities." |
| Q86 | 8 | output_ontology | "This further demonstrates the need to treat the dimensions as independent." |
| Q87 | 8 | output_content | "In terms of the other qualities of the Expert responses, they do not normally reveal the answer and tend to include scaffolding; however, there are a small number of instances where they failed to identify the mistake or its location." |
| Q88 | 8 | output_content | "Overall, we conclude that human responses from Expert are significantly better than Novice." |
| Q89 | 8 | output_form | "Our findings on the Tutor Tone align with those of Wang et al. (2024a) – in task-oriented conversations, AI tutors tend to be more Neutral than Encouraging." |
| Q90 | 8 | output_ontology | "When we combine these two labels into "Non-offensive", the DAMR score reaches 100% as we observe no offensive responses from any LLMs or humans." |
| Q91 | 8 | input_ontology | "We observe high scores for most of the LLMs on human-likeness, which demonstrates their capability to generate human-like output with minimal or no grammatical and fluency mistakes, showing the timely nature of our study, which focuses more on in-depth semantic and pedagogical aspects of tutor responses rather than only on superficial attributes like grammaticality and fluency." |
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
| Q126 | 10 | output_content | "This research is partially supported by Google through the Google Academic Research Award (GARA) 2024. We are grateful for their support. We also extend our gratitude to the campus supercomputing center at MBZUAI." |
| Q127 | 10 | output_content | "strongly believe that this study will help shed light on the current capabilities of LLMs in the context of educational dialogues, and the insights gained from this study may help mitigate issues related to the use of LLMs in the educational domain in the future." |
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
| WEB-1 | https://www.asiancollegeofteachers.com/blogs/1524-Teaching-License-In-India-What-It-Is-And-How-Do-You-Renew-It-blog.php |
| WEB-2 | https://testbook.com/ctet/eligibility-criteria |
| WEB-3 | https://en.wikipedia.org/wiki/Central_Board_of_Secondary_Education |
| WEB-4 | https://candidschools.com/icse-schools-in-india-a-state-wise-list/ |
| WEB-5 | https://muftinternet.com/blog/usage-statistics-internet-and-mobile-users-in-india-2025/ |
| WEB-6 | https://www.storyboard18.com/digital/660-million-smartphone-users-16-17-billion-monthly-upi-transactions-power-digital-bharat-report-89731.htm |
| WEB-7 | https://datareportal.com/reports/digital-2024-india |
| WEB-8 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2234853&reg=3&lang=1 |
| WEB-9 | https://educationforallinindia.com/artificial-intelligence-in-indian-school-education-use-misuse-and-preventive-measures/ |
| WEB-10 | https://www.myidcm.com/blog/artificial-intelligence-course-in-india |
| WEB-11 | https://edurev.in/courses/118419_Mathematics-Ganita-Prakash-Class-8-New-NCERT |
| WEB-12 | https://ciet.ncert.gov.in/activity/eaie |
| WEB-13 | https://ejournals.ncert.gov.in/index.php/tpt/article/download/1323/1261 |
| WEB-14 | https://www.scribd.com/document/628027385/CFPQ-Maths10 |
| WEB-15 | https://arxiv.org/html/2507.00456v1 |
| WEB-16 | https://arxiv.org/abs/2502.18940 |
| WEB-17 | https://aclanthology.org/2025.emnlp-main.11/ |
| WEB-18 | https://github.com/eth-lre/mathtutorbench |
| WEB-19 | https://arxiv.org/html/2510.22581v1 |

---

