## Deployment Context

**Use case:** Assist high school (G10-12) Arabic teachers in Arab countries (teaching students who are native in Arabic) in grading Arabic essays (dataset was collected in Qatar but the writing is in modern standard Arabic which is standard across all Arab countries, although the standards for grading may differ from country to country).
**Target population:** Arabic teachers in Arab countries teaching high school students (G10-12)

# Validity Analysis: laila
**Target context:** Arab-Country G10–12 Arabic Teachers: AI Essay Grading Assistance
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ✓ | 3 | Moderate gaps | medium |
| Output Form ⚠ | 1 | Serious concern | high |
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

LAILA is a methodologically rigorous, well-documented Arabic AES benchmark that establishes the largest publicly available trait-annotated Arabic essay dataset to date [Q1, Q2]. For the target deployment — pan-Arab G10–12 Arabic teachers using AI for essay grading assistance — its validity is mixed. Input Form is well aligned (text-only MSA, matching modality). Output Content has strong annotation procedures but unresolved questions about annotator nationality diversity. The remaining four dimensions show significant deployment mismatches that map directly onto the HIGH-priority gaps flagged in elicitation: Input Ontology (Egypt's holistic grading [WEB-5] and missing genres [Q89]), Input Content (Qatari-only prompts [Q88] with no cross-national degradation testing), Output Ontology (no confidence or rationale categories), and Output Form (discrete labels only, with the benchmark explicitly prohibiting high-stakes operational use without independent validation [Q104, Q105]). The benchmark is best understood as a strong research resource that requires substantial supplementation — both empirical (cross-national validation) and methodological (rationale and uncertainty layers) — before responsible teacher-facing deployment.

## Practical Guidance

### What This Benchmark Measures

LAILA measures how well models can predict CAST-rubric trait scores and a derived holistic score on explanatory and persuasive MSA essays produced by G10–12 Qatari students under timed digital conditions [Q14, Q34, Q38]. Its strongest dimensions for the target context are Input Form (text-only MSA matches deployment) and Output Content (rigorous annotation with substantial IAA [Q44]), making it useful for benchmarking baseline scoring agreement between models and qualified Arabic-educator judgment.

### Construct Depth

The benchmark probes the construct of Arabic essay quality with substantial depth on the analytic-rubric dimension — fine-grained seven-trait scoring, double annotation, rigorous adjudication, and extensive baseline experiments across feature-based, encoder-based, and LLM models in both prompt-specific and cross-prompt setups [Q48, Q83]. However, depth is concentrated within a Qatari-curriculum, two-genre, discrete-label paradigm. It does not probe construct depth on dimensions central to the deployment: cross-national rubric portability (Egypt's holistic grading, Levantine and Maghrebi conventions), narrative/descriptive genre coverage, uncertainty calibration, or rationale quality.

### What Else You Need

For valid teacher-facing deployment beyond Qatar, supplementation is required across four dimensions: (IO) cross-national rubric mapping plus a holistic-only evaluation track for Egyptian-style use; (IC) cross-national prompt validation testing model scoring stability on Egyptian, Levantine, and Maghrebi locally-grounded prompts; (OO+OF) integration of an Arabic-language adaptation of rationale-generation frameworks such as RaDME or RMTS [WEB-13, WEB-12] plus calibrated uncertainty estimates evaluated against teacher disagreement; (OC) a cross-country annotator validation study — re-annotating a stratified sample of LAILA essays with Egyptian, Saudi, Jordanian, Lebanese, and Moroccan Arabic-language educators to quantify cross-country labeling drift on Style, Development, and Organization. The benchmark's own ethics requirements [Q105, Q106] effectively mandate this supplementation before operational deployment.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
LAILA's task taxonomy is explicitly limited to two genres (explanatory and persuasive) [Q89] and operationalizes essay scoring through the QUTC CAST seven-trait rubric [Q33, Q34], a Qatari-curriculum artifact. For a pan-Arab teacher-facing deployment, this presents two HIGH-priority IO problems flagged in the elicitation: (1) Egypt's secondary Arabic assessment is holistic and rubric-free with no documented multi-trait analogue [WEB-5]; the seven-trait structure does not map onto Egyptian classroom practice. (2) Narrative and descriptive genres, which are present in many Arab national curricula, are absent from the benchmark and are explicitly noted as a limitation by the authors [Q89]. The benchmark also frames AES purely as score prediction (regression / sequential generation of trait labels) [Q147, Q181] and does not include any task category for confidence estimation or rationale generation, both of which the deployment requires. The two evaluation setups (prompt-specific and cross-prompt) [Q14] are methodologically appropriate but do not address cross-national generalization. No public rubric documentation was found for Saudi Arabia, Jordan, Lebanon, or Morocco that would allow the seven-trait mapping to be confirmed [WEB-7, WEB-10]. The strengths are real (multi-trait coverage, two evaluation setups), but the omissions are central to deployment validity.

**Strengths:**
- Provides fine-grained seven-trait coverage (REL, ORG, VOC, STY, DEV, MEC, GRA) supporting analytic rather than only holistic scoring [Q34, Q115]
- Includes both prompt-specific and cross-prompt evaluation setups, with cross-prompt being the more deployment-realistic case [Q14, Q72]
- Evaluates a diverse model taxonomy (feature-based, encoder-based, Arabic-centric LLMs in zero/few-shot) [Q48, Q51], giving teachers a meaningful baseline landscape

**Checklist:**

- **IO-1**: Required deployment categories include: (a) trait-based analytic scoring for Gulf-style rubric users, (b) holistic-only scoring suited to Egyptian practice, (c) narrative and descriptive genre scoring, and (d) confidence/rationale outputs. LAILA covers (a) explicitly [Q34] but does not cover (b), (c), or (d). — _Sources: Q34, WEB-5_
- **IO-2**: Yes. The taxonomy omits narrative and descriptive genres [Q89], omits a holistic-only scoring mode aligned with Egyptian practice [WEB-5], and omits confidence/rationale categories that the deployment requires (elicitation Q3). No mapping to Tawjihi (Jordan) or Qiyas (Saudi Arabia) frameworks is documented [WEB-7, WEB-10]. — _Sources: Q89, WEB-5, WEB-7, WEB-10_
- **IO-3**: No clearly irrelevant categories were identified — all seven CAST traits are plausibly meaningful for MSA writing, even if not all are weighted equivalently across national curricula. The pan-Arab MSA standards assumption from elicitation supports surface relevance of the trait set. — _Sources: Q34_
- **IO-4**: Documented gaps that harm content validity: (1) genre ontology restricted to explanatory/persuasive [Q89]; (2) no holistic-only or rubric-free evaluation mode for Egyptian-style use [WEB-5]; (3) no task category for uncertainty or rationale generation [Q181, Q182]; (4) no cross-national rubric mapping between CAST traits and Saudi/Jordanian/Lebanese/Moroccan frameworks [WEB-7, WEB-10]. — _Sources: Q89, Q181, WEB-5, WEB-7, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q14] 'We establish baseline AES results for Arabic under two evaluation setups: prompt-specific and cross-prompt.' (p.2)
- [Q34] 'The rubric covers 7 writing traits [D4]: Relevance (REL), Organization (ORG), Vocabulary (VOC), Style (STY), Development (DEV), Mechanics (MEC), and Grammar (GRA).' (p.5)
- [Q89] 'Second, LAILA includes only explanatory and persuasive writing prompts, limiting genre diversity and potentially affecting model robustness across other styles, such as narrative or descriptive writing.' (p.10)
- [Q181] 'In the zero-shot setting, the LLM is tasked with generating trait scores in JSON format, given the prompt text, essay, and trait rubrics.' (p.18)

*Web sources:*
- [WEB-5] Egypt's Thanaweya Amma Arabic exam uses subject-level percentage scoring without a documented multi-trait essay rubric
- [WEB-7] Saudi Qiyas focuses on higher-education entry testing rather than G10–12 classroom multi-trait essay rubrics
- [WEB-10] Jordan's Tawjihi Arabic exam emphasizes literary comprehension and grammar rather than free-composition trait scoring

</details>

**Information gaps:**
- Genre distribution (narrative/descriptive/argumentative/explanatory) in G10–12 Arabic curricula across Egypt, Saudi Arabia, Jordan, Lebanon, Morocco
- Whether national curricula in target countries use any analytic trait dimensions that would map onto CAST

**Requires expert verification:**
- Mapping of CAST traits to Lebanese CRDP and Moroccan national Arabic writing criteria
- Whether Saudi MOE classroom Arabic assessment uses any internal trait-based rubric beyond Qiyas

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
All 7,859 essays were collected from 4,372 students at 24 schools in Qatar [Q3, Q27], in response to 8 prompts designed for the Qatari educational context. The authors themselves flag that this 'may limit its generalizability to other Arabic-speaking populations due to diverse educational systems' [Q88], offering only partial mitigation through Qatar's expatriate population. Prompts were designed for cultural relevance to the Arabic-speaking context broadly [Q22, Q99], but no prompts grounded in Egyptian history, Levantine literary traditions, or North African social topics are documented. The elicitation flags IC as HIGH priority because models trained on LAILA may misjudge Relevance and Development for locally grounded non-Qatari content (Q4 elicitation), and web searches found no published study testing LAILA-trained models on non-Qatari prompt content (gap_id 2). Comparison datasets cited (ASAP, PERSUADE, MERLIN, TOEFL11) [Q17, Q112, Q113] situate LAILA internationally but not within a cross-Arab-country framework. The content is authentically classroom-produced [Q21] and gender-balanced [Q23, Q100], which are real strengths for L2/L1 MSA-writer representation, but the geographic single-country scope is the dominant validity concern.

**Strengths:**
- Authentic classroom-produced writing under realistic timed conditions [Q21, Q25]
- Intentional gender balance and diversity-by-design principles [Q23, Q100]
- Substantial scale (7,859 essays, 4,372 students, 24 schools, 8 prompts) [Q2, Q27, Q38]
- Qatar's Arab expatriate population provides some dialectal and cultural diversity in student-writer backgrounds [Q88]

**Checklist:**

- **IC-1**: Yes. Prompts are grounded in the Qatari educational context [Q88] and would require region-specific cultural framing for relevance/development scoring of essays from other Arab countries (elicitation Q4). No Egyptian-history, Levantine-literary, or North-African-social prompts are documented. — _Sources: Q88_
- **IC-2**: Partially. Prompts were designed to be 'culturally relevant to the Arabic-speaking context' and free of sensitive topics [Q22, Q99], which provides broad pan-Arab cultural compatibility. However, alignment is to a Qatari-designed conception of pan-Arab cultural relevance, not to nationally specific curricula. — _Sources: Q22, Q99_
- **IC-3**: No Western-specific knowledge is required; the content is Arabic-language and Arab-context throughout [Q22]. The risk is intra-region (Qatar-centric within Arab context) rather than Western-bias. — _Sources: Q22_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the paper does not document any regional annotator panel from non-Qatari Arab countries reviewing prompts for cross-national cultural representativeness; would need an Egyptian/Levantine/Maghrebi expert review of the eight prompts.
- **IC-5**: Documented content issues: (1) single-country source [Q88]; (2) eight prompts may not span the cultural and topical breadth of seven-plus deployment countries; (3) no published cross-national degradation test exists [gap_id 2]. The HIGH-priority IC mismatch flagged in elicitation is corroborated by both the authors' own limitations statement and the absence of compensating evidence. — _Sources: Q88, WEB-6, WEB-26_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'we visited 24 high schools in Qatar and collected essays directly from 4,372 students in authentic classroom settings.' (p.1)
- [Q22] 'Prompts were intentionally varied across genres, ensuring cultural relevance and age appropriateness, thereby promoting model generalization and reducing bias.' (p.3)
- [Q88] 'LAILA was collected from students in a single country, Qatar, and specific grade levels, grades 10 to 12, which may limit its generalizability to other Arabic-speaking populations due to diverse educational systems.' (p.9)
- [Q99] 'Essay prompts were carefully designed to be developmentally appropriate for the target age groups, culturally relevant to the Arabic-speaking context, and free of sensitive topics or potentially harmful content.' (p.10)

*Web sources:*
- [WEB-6] AR-AES dataset uses undergraduate essays from diverse courses, not Arab-secondary curriculum content
- [WEB-26] TAQEEM 2025 introduced 1,265-essay Arabic AES dataset with same seven traits; non-Qatar origin not explicitly documented in available abstracts

</details>

**Information gaps:**
- Empirical performance of LAILA-trained models on non-Qatari prompts (gap_id 2: no study found)
- Whether TAQEEM 2025's dataset extends LAILA's geographic coverage [WEB-26]
- Dialectal-interference patterns in MSA produced by Moroccan, Egyptian, Lebanese students (gap_id 6)

**Requires expert verification:**
- Cultural equivalence of the 8 LAILA prompts when assigned to Egyptian, Lebanese, or Moroccan G10–12 classrooms
- Whether Qatari prompts would be assignable as-is in non-Qatari curricula

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
The benchmark's input form is text-only Modern Standard Arabic submitted digitally via Microsoft Forms with a 65-minute time limit [Q26], producing essays averaging 171 words with most between 90 and 210 words [Q39, Q134, Q135]. PII was systematically removed and pre-generated anonymous IDs assigned [Q97]. This matches the deployment scenario directly: the elicitation marks IF as LOWER priority because deployment is text-only MSA. No script, modality, or capture-device mismatch exists. The main residual concerns are: (1) the short essay length (171-word average) is acknowledged as limiting assessment of long-form writing [Q92], and many national high-school assessments may produce longer compositions; (2) the digital-submission collection mode may not match handwritten or paper-based classroom workflows still common in some target countries — Saudi Arabia has Madrasati [WEB-17] and UAE has high digital adoption [WEB-1], but Egypt, Jordan, Lebanon, Morocco have no comparable national K-12 LMS documented in searches. The form is broadly compatible but biased toward shorter essays and digital-native workflows.

**Strengths:**
- Text-only MSA matches deployment modality and Arabic script requirements [Q26]
- Authentic timed writing conditions emulate high-stakes testing [Q25]
- Systematic anonymization and PII removal supports privacy compliance [Q97]
- Comparison table situates LAILA against other AES datasets on length and annotation depth [Q12]

**Checklist:**

- **IF-1**: No script or signal-distribution mismatch — both source and target are MSA text in Arabic script [Q26]. Length distribution skews short (171-word mean, peak 150–180 [Q134, Q135]); deployment essays may be longer in some curricula, which is a partial distribution mismatch. — _Sources: Q26, Q134, Q135_
- **IF-2**: Digital-submission infrastructure exists in Gulf states (Madrasati in Saudi Arabia, high UAE adoption) [WEB-17, WEB-1] but is less documented for Egypt, Jordan, Lebanon, Morocco; teachers in those countries may still receive handwritten essays requiring transcription before AI scoring. — _Sources: WEB-1, WEB-17_
- **IF-3**: The CAST rubric is provided in Arabic for annotation [Q114] with English translation [Q116]; AraBERT encodes essay+prompt jointly [Q157] and AraT5 receives instruction+essay [Q148]; LLM context limit of 4,096 tokens with iterative example removal [Q184, Q185] is a relevant deployment-time form constraint. — _Sources: Q114, Q148, Q157, Q184_
- **IF-4**: Documented form considerations: (1) average essay length is short (171 words) and may not represent longer compositions found in some curricula [Q92]; (2) no audio/handwriting modality despite handwritten classroom workflows being plausible in non-Gulf countries; (3) the digital Microsoft Forms collection [Q26] may not match all deployment workflows. — _Sources: Q92, Q26_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q26] 'we configured a Microsoft Form for digital essay submission, set with a 65-minute time limit to enforce a time-restricted setup' (p.5)
- [Q39] 'the number of essays per prompt ranges from 500 to 1,181. Essay lengths demonstrate consistency across prompts, with an average of 171 words and a maximum of 706 words.' (p.6)
- [Q92] 'with an average essay length of only 171 words, the dataset lacks extended writing samples, restricting the assessment of models on long-form academic tasks' (p.10)
- [Q97] 'all submissions were assigned pre-generated anonymous identifiers, and personally identifiable information was systematically removed during data cleaning.' (p.10)

*Web sources:*
- [WEB-1] UAE teachers ~75% AI tool adoption per OECD TALIS 2024
- [WEB-17] Saudi Arabia's Madrasati LMS deployed to all public K-12 schools, 92% student attendance

</details>

**Information gaps:**
- Whether handwritten-essay workflows remain dominant in non-Gulf target countries
- Length distribution of typical G10–12 essays in Egyptian, Jordanian, Lebanese, Moroccan curricula

**Requires expert verification:**
- Country-by-country prevalence of digital vs. paper essay submission in G10–12 Arabic classrooms

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The output ontology consists of seven trait scores plus a holistic sum [Q34, Q35], with six traits on a 0–5 scale and REL on a 0–2 scale [Q36], grounded in the QUTC CAST rubric [Q33]. Three concerns drive the low score, two of which are flagged HIGH priority in elicitation. (1) The trait taxonomy is Qatari-curriculum-derived; no mapping is documented to Egyptian holistic grading [WEB-5], Tawjihi [WEB-10], Qiyas [WEB-7], CRDP, or Moroccan frameworks. Egypt's holistic-only practice means the analytic seven-trait label space may not be the construct teachers actually evaluate (elicitation Q2, Q4). (2) The output is exclusively discrete point-score labels [Q181, Q182]; the deployment requires confidence and rationale outputs (elicitation Q3), which are entirely absent from the output ontology. (3) The narrow REL 0–2 scale is acknowledged by the authors as limiting QWK granularity [Q91]. Strengths: the trait set is internally coherent, the REL=0 cascade rule [Q37] is explicit, and the rubric is documented in both Arabic [Q114] and English [Q116, Q118]. But for teacher-facing deployment across multi-country contexts, the output ontology is structurally misaligned on two of the highest-priority elicitation dimensions.

**Strengths:**
- Seven-trait analytic schema aligns with rubric-based grading practice in Gulf countries (Qatar, UAE, Saudi Arabia) [Q34, WEB-7]
- Explicit rubric documentation (Arabic original + English translation) supports interpretability [Q114, Q116, Q118]
- Clear scoring scale and decision rules including REL=0 cascade [Q36, Q37]
- Score distributions reported per trait per prompt give deployment users a sense of label calibration [Q40, Q119]

**Checklist:**

- **OO-1**: Categories are regionally relevant for analytic-rubric users (Gulf, UAE) but not for holistic-grading users (Egypt) [WEB-5]; cross-national rubric mapping is not documented [WEB-7, WEB-10]. — _Sources: Q34, WEB-5, WEB-7, WEB-10_
- **OO-2**: Missing categories for the deployment: (1) no holistic-only output mode for Egyptian-style grading; (2) no confidence/uncertainty category despite elicitation Q3 requiring it; (3) no rationale/justification category despite elicitation Q3 requiring it; (4) no narrative/descriptive trait specifications since those genres are excluded [Q89]. — _Sources: Q89, Q181, Q182_
- **OO-3**: The CAST rubric is QUTC-derived and may encode Gulf-curriculum stylistic and developmental norms in Style, Development, and Organization scoring; the elicitation flags this as warranting verification (Q1, OC priority) rather than dismissal. No web evidence documents how CAST descriptors compare with Maghrebi or Levantine rhetorical traditions. — _Sources: Q33_
- **OO-4**: Stakeholder-driven taxonomy redesign is recommended but not undertaken in LAILA; the dataset's own ethics statement requires fairness auditing and stakeholder consultation before real-world application [Q106]. — _Sources: Q106, WEB-13_
- **OO-5**: Documented taxonomy issues harming structural and content validity: (1) discrete-label-only output form omitting confidence and rationale [Q181, Q182]; (2) narrow REL scale [Q91]; (3) no cross-national rubric mapping [WEB-5, WEB-7, WEB-10]; (4) no holistic-only mode [WEB-5]. — _Sources: Q91, Q181, WEB-5, WEB-7, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q34] 'The rubric covers 7 writing traits [D4]: Relevance (REL), Organization (ORG), Vocabulary (VOC), Style (STY), Development (DEV), Mechanics (MEC), and Grammar (GRA).' (p.5)
- [Q36] 'Six traits (all but REL) were rated on a 6-point scale (0 = lowest, 5 = highest), while REL was rated on a 3-point scale' (p.5)
- [Q91] 'the relevance trait is scored on a narrow scale from 0 to 2, which limits the granularity of evaluation and may cause QWK to underrepresent subtle differences in model predictions.' (p.10)
- [Q182] 'The holistic score was computed as the sum of the individual trait scores.' (p.18)
- [Q106] 'We recommend that any system developed using LAILA undergo fairness auditing and stakeholder consultation before real-world application.' (p.10)

*Web sources:*
- [WEB-5] Egypt's Thanaweya Amma Arabic uses holistic percentage scoring with no documented multi-trait essay rubric
- [WEB-7] Saudi Qiyas focuses on higher-education entry testing rather than secondary multi-trait classroom rubrics
- [WEB-10] Jordan's Tawjihi Arabic exam emphasizes literary comprehension and grammar over trait-scored free composition
- [WEB-13] RaDME framework generates trait scores with co-produced rationales — actionable methodological path but not yet applied to Arabic

</details>

**Information gaps:**
- Whether CAST trait descriptors carry Gulf-specific stylistic norms detectable in score distributions
- Whether any Arab country's national rubric maps onto a subset of the seven traits

**Requires expert verification:**
- Whether Egyptian, Lebanese, or Moroccan teachers would re-weight or re-define Style and Development categories given their professional norms

---

### Output Content — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Annotation procedures are well-documented and rigorous: 6 annotators and 3 supervisors, all Arabic language teachers/lecturers with five holding MSc/PhD in Arabic [Q30, Q31]; structured training [Q102]; comprehensive guidebook with exemplars [Q41]; annotator blinding to student identity [Q42]; double scoring with mean-rounded-down aggregation and supervisor escalation at HOL ≥ 6 [Q43]; QWK IAA of 0.66–0.75 classified as substantial [Q44]; fair compensation [Q101]. These are real strengths. The validity concern is that all annotators appear to be Qatar-based and trained on QUTC CAST [Q30, Q33], with no documentation of nationality diversity (gap_id 5: no documentation found). The elicitation marks OC as MODERATE because the user judges pan-Arab MSA standards uniform for surface linguistic quality (Q1), which lowers — but does not eliminate — the risk that evaluative judgments on Style, Development, and Organization carry implicit Gulf-curriculum norms. The aggregation method (mean-rounded-down) [Q43] could erase minority interpretations on borderline cases. P5 had a 23.3% third-annotator escalation rate [Q45], suggesting some prompts produced systematic annotator disagreement. Overall, methodologically strong but with an unresolved annotator-pool diversity question that matters for cross-country deployment.

**Strengths:**
- Annotators are qualified Arabic-language educators, five with advanced degrees [Q30, Q31]
- Structured training, annotation guidebook, and moderation sessions [Q41, Q102]
- Double annotation with explicit adjudication procedure for disagreements ≥ 6 HOL points [Q43]
- Substantial inter-annotator agreement (QWK 0.66–0.75) [Q44]
- Annotator blinding to student identity reduces demographic bias [Q42, Q98]
- Fair compensation at or above local professional rates [Q101]
- IRB approval and informed consent documented [Q9, Q95]

**Checklist:**

- **OC-1**: Partially. Ground-truth labels reflect qualified Arabic-educator judgment [Q30] but specifically Qatar-based educators trained on QUTC CAST [Q33]; whether they reflect Egyptian, Levantine, or Maghrebi educator perspectives is undocumented. — _Sources: Q30, Q33_
- **OC-2**: Potential disagreement is plausible on Style, Development, and Organization given different national rhetorical traditions; the elicitation flags this as warranting verification (Q1). The pan-Arab MSA assumption should hold for surface mechanics/grammar but is less certain for evaluative traits. — _Sources: Q33, WEB-5_
- **OC-3**: Annotator demographics are partially documented — qualifications and degree level [Q30, Q31] are reported, but nationality, dialect background, and curricular training origin beyond CAST are not. No Datasheet or Data Statement section specifies these. — _Sources: Q30, Q31_
- **OC-4**: INSUFFICIENT DOCUMENTATION — no re-annotation by representative non-Qatari Arab annotators is reported; the LAILA paper does not include any cross-country annotator validation study.
- **OC-5**: Aggregation is mean-of-two-scores rounded down to nearest integer [Q43], with supervisor adjudication only when HOL discrepancy ≥ 6 points. This may erase legitimate minority perspectives on borderline cases (e.g., a 3 vs. 4 disagreement is averaged and rounded down to 3 without further review). — _Sources: Q43_
- **OC-6**: Documented label-correctness considerations: (1) annotator pool nationality undocumented [gap_id 5]; (2) substantial but not perfect IAA, with P5 showing 23.3% escalation [Q45]; (3) round-down aggregation may bias scores slightly downward on disagreement cases [Q43]. — _Sources: Q43, Q45_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q30] 'The hired annotation team consisted of 6 annotators and 3 supervisors, all of whom were Arabic language teachers or lecturers with educational backgrounds.' (p.5)
- [Q31] 'Five members of the team hold advanced degrees (MSc or PhD) in the Arabic language.' (p.5)
- [Q33] 'All essays in LAILA dataset were scored using the Core Academic Skills Test (CAST) rubric [D7], developed by the Qatar University Testing Center (QUTC).' (p.5)
- [Q43] 'If the difference in HOL scores between the two annotators was less than 6 points, the mean of the two scores was computed and then rounded down to the nearest integer; this rounded value was adopted as the final score for each trait.' (p.6)
- [Q44] 'IAA was substantial across prompts, with an average QWK ranging from 0.66 (P5) to 0.75 (P1)' (p.6)
- [Q45] 'P5 showed the lowest average agreement, noting that it has the highest percentage of essays that require a third annotator (A3: 23.3%)' (p.6)
- [Q101] 'All annotators were qualified Arabic language educators who received fair compensation at or above local professional rates.' (p.10)

*Web sources:*
- [WEB-5] Egypt's holistic grading culture suggests Egyptian teachers may apply different evaluative standards than Qatar-based annotators

</details>

**Information gaps:**
- Annotator nationality and dialectal background distribution (gap_id 5: no documentation found)
- Whether the round-down aggregation introduces systematic downward bias on borderline scores
- What proportion of supervisor adjudications involved trait-specific (vs. holistic) disagreements

**Requires expert verification:**
- Whether non-Qatari Arab Arabic-language educators would assign systematically different Style, Development, or Organization scores on the same essays
- Inquiry to LAILA authors regarding annotator nationality composition

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
This is the dimension with the most direct deployment mismatch and is flagged HIGH priority in elicitation. LAILA's evaluation produces only discrete point-score labels [Q181, Q182] evaluated by Quadratic Weighted Kappa [Q58]. The benchmark does not evaluate confidence calibration, uncertainty quantification, score-range prediction, or rationale generation. The deployment use case explicitly requires confidence signals and explanatory justification (elicitation Q3) so teachers can intervene meaningfully on borderline essays. There is no overlap between the benchmark's evaluated output form and the deployment's required output form for these features. Web research confirms this is a structural gap in the field: rationale-generation frameworks (RMTS, RaDME, QwenScore+) exist for English but no Arabic adaptation has been documented [WEB-12, WEB-13, WEB-14], and TAQEEM 2025 used Chain-of-Thought prompting but focused on accuracy, not rationale [WEB-15]. The benchmark's own ethics statement explicitly prohibits use 'for high-stakes educational decisions affecting individual students' [Q104] and warns against 'deployment in operational assessment contexts without independent validation' [Q105]. Combined with the elicitation marking both OO and OF as HIGH priority for this exact reason, the score is 1 — fundamental misalignment.

**Strengths:**
- QWK as the evaluation metric matches the metric used for IAA, providing internal coherence between human and model agreement [Q44, Q58]
- Three-seed repetition for LLM experiments supports reporting variability [Q189]
- Structured JSON output enforced via outlines library [Q190] could be extended to include rationale fields

**Checklist:**

- **OF-1**: No. Benchmark output is discrete trait scores plus holistic sum [Q181, Q182]; deployment requires per-trait scores plus confidence signal plus rationale text. The benchmark does not evaluate the latter two. — _Sources: Q181, Q182_
- **OF-2**: Not applicable — neither benchmark nor deployment requires speech output. Output is text only on both sides.
- **OF-3**: INSUFFICIENT DOCUMENTATION on this specific point in the LAILA paper, but the deployment population is qualified teachers; literacy/accessibility considerations apply more to student-facing outputs than to the teacher-facing scoring interface evaluated here.
- **OF-4**: Documented form mismatches harming external validity: (1) no confidence/uncertainty output evaluated [Q181]; (2) no rationale output evaluated [Q181, Q182]; (3) no in-domain Arabic precedent for rationale-generation evaluation [WEB-12, WEB-13, WEB-15]; (4) benchmark explicitly prohibits high-stakes operational use without independent validation [Q104, Q105]. — _Sources: Q104, Q105, WEB-13, WEB-15_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q58] 'We evaluate model performance using QWK to measure agreement between human and model scores.' (p.8)
- [Q104] 'We explicitly prohibit its use for high-stakes educational decisions affecting individual students.' (p.10)
- [Q105] 'Users must commit to: (1) preventing re-identification attempts, (2) avoiding demographic profiling or inference, and (3) refraining from deployment in operational assessment contexts without independent validation.' (p.10)
- [Q181] 'In the zero-shot setting, the LLM is tasked with generating trait scores in JSON format, given the prompt text, essay, and trait rubrics.' (p.18)
- [Q182] 'The holistic score was computed as the sum of the individual trait scores.' (p.18)

*Web sources:*
- [WEB-12] BERT-based Arabic AES system documented but without rationale generation
- [WEB-13] RaDME generates trait scores with co-produced rationales using knowledge distillation — English only, no Arabic adaptation documented
- [WEB-14] QwenScore+ uses rubric-aware Chain-of-Thought prompting with RLHF — English only
- [WEB-15] TAQEEM 2025 used CoT prompting on Arabic essays but focused on scoring accuracy, not rationale output

</details>

**Information gaps:**
- Whether any Arabic-language AES system has been validated with teacher-facing rationale output (gap_id 3: not found)
- Whether Arabic teachers would accept LLM-generated rationales as professionally credible

**Requires expert verification:**
- Acceptance of AI-generated trait scores and rationales by Arab-country secondary Arabic teachers across the deployment range

---

## Remediation Suggestions

### Output Form ⚠

**Gap:** Benchmark evaluates only discrete point-score outputs via QWK; deployment requires uncertainty signals and rationale text [Q58, Q181]

**Recommendation:** Define and report new metrics alongside QWK: (1) calibration metrics for confidence outputs (e.g., expected calibration error against teacher disagreement); (2) rationale quality metrics evaluated by qualified Arab teachers across multiple countries. Treat current QWK results as necessary but not sufficient evidence.

### Output Ontology ⚠

**Gap:** No category for confidence/uncertainty or rationale outputs, despite both being HIGH-priority deployment requirements (elicitation Q3)

**Recommendation:** Extend the output ontology with two new categories: (1) per-trait confidence/uncertainty signal, and (2) rationale text. Adapt an English rationale-generation framework (RaDME [WEB-13] or RMTS [WEB-12]) to Arabic with teacher-facing evaluation.

### Input Ontology ⚠

**Gap:** Seven-trait CAST taxonomy does not map onto Egyptian holistic grading practice and lacks narrative/descriptive genre coverage

**Recommendation:** Add a holistic-only evaluation track suitable for Egyptian-style assessment, and either commission a narrative/descriptive prompt extension or document explicitly that the system is restricted to explanatory/persuasive genres in deployment guidelines.

### Input Ontology ⚠

**Gap:** Cross-prompt generalization performance is substantially weaker than prompt-specific performance [Q71], yet cross-prompt is the realistic deployment setting [Q72]

**Recommendation:** Anchor deployment evaluation primarily on cross-prompt results rather than prompt-specific results, and communicate this performance ceiling clearly to teacher users so they understand the system's reliability limits on novel prompts.

### Input Content ⚠

**Gap:** All prompts originate in a single country (Qatar); cross-national prompt-content generalization is untested [Q88, gap_id 2]

**Recommendation:** Run a cross-national content validation study by collecting a small held-out set of essays responding to nationally-grounded prompts (Egyptian history, Levantine literature, Maghrebi social topics) and measure scoring stability of LAILA-trained models versus local teacher ground truth.

### Output Content

**Gap:** Annotator nationality diversity within the Qatar-based pool is undocumented [gap_id 5]; cross-country annotator agreement is unknown

**Recommendation:** Direct inquiry to LAILA authors for annotator nationality composition; commission a small cross-country re-annotation study (~500 essays) with Egyptian, Saudi, Lebanese, and Moroccan Arabic-language educators to quantify QWK drift on Style, Development, and Organization.

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
| Q9 | 1 | input_content | "IRB Number: QU-IRB 159/2024-EA" |
| Q10 | 1 | input_ontology | "Arabic AES research faces a significant data scarcity problem, as publicly available annotated datasets remain limited." |
| Q11 | 1 | input_ontology | "Existing Arabic resources are often small in scale such as QAES (Bashendy et al., 2024), lack trait-specific annotations as in ZAEBAC (Habash and Palfreyman, 2022), or consist solely of unannotated essays such as ALC." |
| Q12 | 2 | input_form | "Table 2: Comparison of LAILA with existing essay datasets. "Len" is average essay length in words; "HOL" indicates holistic scoring; "Eur" covers German, Italian, and Czech; "L1/L2" denotes native or second-language learners; "Public" here means freely available." |
| Q13 | 2 | output_ontology | "tailed trait-specific annotations that capture multiple dimensions of writing proficiency." |
| Q14 | 2 | input_ontology | "We establish baseline AES results for Arabic under two evaluation setups: prompt-specific and cross-prompt." |
| Q15 | 2 | output_form | "We publicly release LAILA, including essays with holistic and trait-specific annotations. We also release the benchmarking code to support replication and future research." |
| Q16 | 2 | input_ontology | "Section 2 reviews related work and existing AES datasets. Section 3 outlines the data collection design principles, while Section 4 describes the dataset construction process, including school and prompt selection, essay collection, and annotations." |
| Q17 | 2 | input_content | "Research on AES has advanced considerably in English, supported by large-scale, publicly available datasets such as ASAP/ASAP++ (Mathias and Bhattacharyya, 2018), TOEFL11 (Blanchard et al., 2013), ELLIPSE (Crossley et al., 2023a), and PERSUADE (Crossley et al., 2023b)." |
| Q18 | 2 | input_ontology | "In contrast, other languages have far fewer resources. Some smaller datasets exist, including ACEA (Chinese; annotated but not public) (He et al., 2022), TCFLE-8 (French; public but with only holistic scores) (Wilkens et al., 2023), and MERLIN (German, Italian, and Czech; public but limited to holistic annotations) (Boyd et al., 2014). While useful for AES studies, their limited scale and annotation depth restrict their utility." |
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
| Q38 | 6 | input_content | "LAILA comprises 7,859 essays collected across 8 distinct prompts: 3 explanatory and 5 persuasive (3,446 and 4,413 essays, respectively)." |
| Q39 | 6 | input_form | "Table 3 shows that the number of essays per prompt ranges from 500 to 1,181. Essay lengths demonstrate consistency across prompts, with an average of 171 words and a maximum of 706 words." |
| Q40 | 6 | output_ontology | "Most traits follow a near-normal pattern on the 6-point scale, indicating overall positive essay quality. The REL scores show that 86% of the essays agree strongly with the prompt. In contrast, GRA and VOC show the highest percentage of score 1 at 16%, followed by MEC at 13%, highlighting that these traits pose the greatest challenges." |
| Q41 | 6 | output_content | "To ensure consistency, 2 supervisors developed an annotation guidebook with detailed terminology, exemplars, and annotated practices for each prompt type. Annotators were required to review these materials and complete training sessions before formal annotation. Moderation sessions followed, where discrepancies were discussed and interpretations of the rubric were harmonized." |
| Q42 | 6 | output_content | "The scoring process was conducted using the Assessment Gourmet Platform, which supports large-scale, anonymized essay scoring. The platform ensured that annotators were blinded to student identity [D6], while only supervisors had access to annotator metadata for monitoring purposes." |
| Q43 | 6 | output_content | "The essays were randomly distributed among the annotators to minimize systematic bias, and the scoring sessions were capped to prevent annotators' fatigue. Each essay was independently scored by two annotators across all traits. If the difference in HOL scores between the two annotators was less than 6 points, the mean of the two scores was computed and then rounded down to the nearest integer; this rounded value was adopted as the final score for each trait. However, essays with large discrepancies between annotators (≥ 6 points difference in the HOL score) were flagged and escalated to a supervisor (a third annotator in this case), who provided the final adjudicated score and offered feedback to the annotators to improve alignment and consistency in subsequent batches of essays." |
| Q44 | 6 | output_content | "We compute IAA using Quadratic Weighted Kappa (QWK) (Williamson et al., 2012) to assess agreement between the two main annotators (A1 and A2), prior to adjudication. Table 4 reports QWK per trait and prompt, with agreement strength following Landis and Koch (1977). Overall, IAA was substantial across prompts, with an average QWK ranging from 0.66 (P5) to 0.75 (P1), showing strong consistency." |
| Q45 | 6 | output_content | "However, variability emerges by prompt and trait. In particular, P5 showed the lowest average agreement, noting that it has the highest percentage of essays that require a third annotator (A3: 23.3%; Table 3). This suggests greater initial disagreement" |
| Q46 | 7 | input_ontology | "For each setup, we investigate two research questions in the context of Arabic AES: (RQ1) how do different categories of models compare in overall performance?, and (RQ2) which models achieve the best results across individual traits?." |
| Q47 | 7 | input_ontology | "Model Selection We selected a diverse set of models with varying architectures to establish strong baselines for LAILA. The selection criteria included code availability, ease of implementation, and coverage of SOTA Arabic and English models." |
| Q48 | 7 | input_ontology | "The models fall into three categories: feature-based (FB), encoder-based, and large language models (LLMs). LLMs were evaluated in zero-shot and few-shot settings, and all models followed a multitask setup predicting holistic and trait scores jointly." |
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
| Q77 | 9 | output_form | "Overall, the findings of the benchmarking experiments above highlight the need to prioritize future research on cross-prompt AES, which is practically closer to the real world, while best models are still far from human performance." |
| Q78 | 9 | input_content | "While research on automated scoring of English essays began more than 55 years ago, Arabic essay scoring is hindered by the lack of data resources." |
| Q79 | 9 | input_content | "To bridge this gap, this paper introduced LAILA, the first large-scale publicly available dataset for Arabic AES." |
| Q80 | 9 | input_content | "The dataset comprises 7,859 essays written on 8 different prompts by 4,372 high school students, and provides annotations for 7 writing traits as well as a holistic score with substantial inter-annotator agreement." |
| Q81 | 9 | input_content | "This makes it a comprehensive and reliable resource for training models and evaluating writing quality of Arabic essays." |
| Q82 | 9 | output_content | "For reproducibility, we detailed the data collection and annotation process." |
| Q83 | 9 | output_form | "We also benchmarked LAILA using SOTA Arabic and English AES models in both prompt-specific and cross-prompt settings, showing strong baselines for future research." |
| Q84 | 9 | output_content | "We heartily thank our dedicated annotators for their contributions and express our gratitude to Qatar University Testing Center, the Ministry of Education and Higher Education in Qatar (the Arabic Section of the Department Of Educational Supervision in particular), participating schools, and students for making this work possible." |
| Q85 | 9 | output_content | "We also acknowledge the support of Advanced Group for Information Technology (AGI) for providing access to the platform, Assessment Gourmet, which was used to manage and administer the annotation process." |
| Q86 | 9 | input_content | "This work was made possible by NPRP grant NPRP14S-0402-210127 from the Qatar Research Development and Innovation (QRDI) Council." |
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
| Q116 | 12 | input_form | "An English-translated version of the CAST rubric is presented in Table 6." |
| Q117 | 13 | output_ontology | "Note: A score of 0 is assigned if the student does not attempt the task, provides a response that falls below the performance level described for score 1, or submits content that is not relevant to the topic of the given prompt." |
| Q118 | 13 | output_ontology | "Table 6: CAST Persuasive/Argumentative Writing Rubric - English Translation (Bashendy et al., 2024)." |
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
| Q147 | 16 | input_ontology | "The AES task is formulated as a text generation problem, where the model predicts the trait scores sequentially." |
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
| Q163 | 17 | output_form | "These configurations were considered better suited to the dataset, mitigating training instabilities." |
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
| Q181 | 18 | input_ontology | "In the zero-shot setting, the LLM is tasked with generating trait scores in JSON format, given the prompt text, essay, and trait rubrics." |
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
| WEB-1 | https://www.agbi.com/education/2025/10/uae-teachers-lead-world-in-classroom-ai-adoption/ |
| WEB-2 | https://www.kenresearch.com/saudi-arabia-ai-k12-education-market |
| WEB-3 | https://journal.qubahan.com/index.php/qaj/article/view/2111 |
| WEB-4 | https://edu2-egypt.com/curriculum-frameworks |
| WEB-5 | https://grokipedia.com/page/academic_grading_in_egypt |
| WEB-6 | https://arxiv.org/abs/2407.11212 |
| WEB-7 | https://etec.gov.sa/en/centers/qiyas |
| WEB-8 | https://saudipedia.com/en/article/571/government-and-politics/centers/the-national-center-for-assessment-qiyas |
| WEB-9 | https://en.wikipedia.org/wiki/National_Center_for_Assessment_in_Higher_Education |
| WEB-10 | https://en.wikipedia.org/wiki/Tawjihi |
| WEB-11 | https://acei-global.org/5-things-to-know-about-jordans-tawjihi-examination-a-gateway-to-higher-education/ |
| WEB-12 | https://www.researchgate.net/publication/382302599_Automated_essay_scoring_in_Arabic_a_dataset_and_analysis_of_a_BERT-based_system |
| WEB-13 | https://arxiv.org/html/2502.20748v1 |
| WEB-14 | https://www.preprints.org/manuscript/202504.2338 |
| WEB-15 | https://aclanthology.org/2025.arabicnlp-sharedtasks.135.pdf |
| WEB-16 | https://link.springer.com/article/10.1007/s40593-024-00433-x |
| WEB-17 | https://www.rowad-alkhaleej.edu.sa/en/online-learning-in-saudi-arabia/ |
| WEB-18 | https://olc-wordpress-assets.s3.amazonaws.com/uploads/2021/05/NELC-Phase-2-K-12-Report-Final-1.pdf |
| WEB-19 | https://www.researchgate.net/publication/356918598_Madrasati_e-learning_platform |
| WEB-20 | https://www.education-saudi.com/madrasati-saudi-digital-education-platform-vision-2030/ |
| WEB-21 | https://securiti.ai/qatar-personal-data-protection-law/ |
| WEB-22 | https://www.dlapiperdataprotection.com/countries/qatar/law.html |
| WEB-23 | https://www.almeezan.qa/EnglishLaws//132016.pdf |
| WEB-24 | https://courier.unesco.org/en/articles/ai-goes-school-united-arab-emirates |
| WEB-25 | https://www.onlineeducation.com/features/saudi-arabia-ai-and-online-learning |
| WEB-26 | https://aclanthology.org/2025.arabicnlp-sharedtasks.134/ |
| WEB-27 | https://www.ijiet.org/vol15/IJIET-V15N8-2367.pdf |

---

