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
| Input Ontology ⚠ | 3 | Moderate gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ✓ | 4 | Minor gaps | high |
| Output Content | 3 | Moderate gaps | medium |
| Output Form ✓ | 4 | Minor gaps | high |
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

MILU is the most relevant publicly available Indic-language MCQ benchmark for evaluating LLM behaviour on Hindi multiple-choice questions, and its strict 4-option/single-answer/binary-scoring schema is a precise structural match for the North Indian Hindi-Medium Postgraduate Teacher deployment. Hindi is high-resource within its scope, formal Khari Boli register is consistent throughout, and there is genuine North Indian state-specific content (UP/Rajasthan/Bihar geography, Panchayati Raj, Chikankari). However, the benchmark has significant content-level concerns for this deployment: empirical analysis of the Hindi validation split shows 100% of items are translated (vs. paper's 25% dataset-wide claim), canonical Hindi-board literary figures (Tulsidas, Premchand, Kabir) are absent from the sample, ~3-4% of items have truncated stems, English vocabulary tests appear inside Hindi Language Studies, and framing is dominated by UPSC/SSC-style competitive-exam GK rather than school-board syllabus content. Annotator demographics for Hindi items are not documented. The user's elicitation confirmed that competitive-exam keys are broadly compatible with board norms, mitigating but not eliminating these concerns. Output ontology and output form align well; input ontology is acceptable in breadth but mis-framed in register; input content is the weakest dimension and matches the elicitation's HIGH priority assignment.

## Practical Guidance

### What This Benchmark Measures

MILU measures LLM ability to answer formal Hindi competitive-exam-style MCQs across 8 domains and 41 subjects, with strong format and scoring alignment to the deployment's binary-correctness use case (output_ontology, output_form). For STEM, India-GK, civics/Panchayati Raj, and constitutional law content, MILU provides reasonable signal for North Indian teacher use cases. The benchmark's Hindi-specific accuracy figures and per-subject tables [Q98-Q132] can serve as a first-pass screen for whether candidate LLMs handle formal Khari Boli MCQ inputs at all.

### Construct Depth

Construct depth is shallow for the school-board deployment construct. The benchmark probes competitive-exam-style factual recall and pan-India GK well, but does not probe school/board syllabus alignment, canonical Hindi literature comprehension (input_content), or state-specific syllabus content with sufficient granularity. A high MILU Hindi score does not warrant strong inference about a model's ability to evaluate Class 9-12 UP/MP/Rajasthan/Bihar board MCQs, particularly in Hindi Sahitya. The 100% translation rate observed in the validation split (input_content) introduces register-fidelity uncertainty that further erodes construct depth for board-aligned use.

### What Else You Need

Supplement with: (1) a North-Indian-board-aligned Hindi Literature MCQ set covering Tulsidas, Premchand, Kabir, Mahadevi Varma, and Harivansh Rai Bachchan to address input_content/input_ontology gaps; (2) a state-board-syllabus-aligned subset for at least UP, MP, Rajasthan, Bihar to address state-wise distribution gaps; (3) Hindi-medium board-teacher review of a stratified item sample for register/translation fidelity (input_content, output_content); (4) data-quality audit to flag truncated/malformed items before deployment use (input_form, output_ontology); and (5) a generative-inference evaluation pass if the deployment uses generative LLMs, since MILU's headline numbers rely on log-likelihood scoring (output_form, [Q85]).

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
MILU's taxonomy of 8 domains and 41 subjects covers all major board-curricular areas relevant to the deployment (Hindi Language, History, Civics, Science, Geography, Arts) and the strict MCQ format aligns precisely with the deployment's positive/negative marking requirement. However, the taxonomy was derived from competitive-exam content (1,500+ exams, predominantly UPSC/SSC/state civil-service style) rather than from school/university board syllabi. Dataset analysis confirms the framing skew: the validation sample is dominated by UPSC-style GK, current affairs, ethics scenarios, and includes highly specialised post-secondary engineering content (FORTRAN 77, AM receiver IF) that exceeds school-board level. Conversely, canonical school-board literary figures (Tulsidas, Premchand, Kabir) were absent from the sample. The 41-subject scheme appears adequate in breadth but the framing register inside subjects diverges from board syllabi.

**Strengths:**
- Strict 4-option single-answer MCQ taxonomy is a precise structural match for the deployment's binary scoring requirement [Q22, Q33].
- Explicit inclusion of Arts & Humanities and Law & Governance as first-class domains covers civics/literature areas core to North Indian board syllabi [Q42].
- Domain-level results are reported with granular per-subject, per-language tables enabling Hindi-specific drill-down [Q98, Q99-Q132].

**Checklist:**

- **IO-1**: Required categories for the deployment span Hindi Language and Literature (canonical authors), History (regional medieval, freedom movement), Civics (Panchayati Raj, state administration), Geography, Science, Mathematics, and General Knowledge — all in formal Hindi MCQ form. MILU's 8-domain/41-subject schema nominally covers these areas [Q42, Q23]. — _Sources: Q42, Q23_
- **IO-2**: The taxonomy omits a school/board-syllabus framing layer. MILU's subjects are derived from competitive-exam tags clustered into 41 subjects [Q39, Q42]; no subject category specifically represents 'Class 9-12 Hindi Sahitya' or state-board syllabus content. Canonical Hindi literary authors expected in board Literature were absent from the sample [DATASET-D3, DATASET-D33]. — _Sources: Q39, Q42, DATASET-D3, DATASET-D33, WEB-12_
- **IO-3**: Several categories include content irrelevant or over-scoped for school-board teacher use: civil-service ethics scenarios [DATASET-D17], specialised post-secondary engineering items (FORTRAN 77, AM receiver IF) [DATASET-D45, DATASET-D46], and time-stamped current-affairs items [DATASET-D47]. These reflect competitive-exam framing acknowledged as the source [Q24, Q92]. — _Sources: Q24, Q92, DATASET-D17, DATASET-D45, DATASET-D46, DATASET-D47_
- **IO-4**: Construct underrepresentation in school-board Hindi Literature framing and construct-irrelevant variance from civil-service GK and advanced engineering content jointly compromise content validity for the deployment, though the 8-domain breadth itself remains acceptable. — _Sources: Q24, DATASET-D17, DATASET-D45_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge.' (p.3)
- [Q23] 'This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others.' (p.3)
- [Q24] 'collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams' (p.3)
- [Q42] '41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies.' (p.4)
- [Q92] 'over 40 exam types ranging from various National and state level civil service examinations to examinations conducted by various government and private organizations.' (p.17)

*Web sources:*
- [WEB-12] GitHub subject list confirms 'Literature and Linguistics' and 'Arts and Culture' as subject categories without item-level framing detail.

*Dataset analysis:*
- DATASET-D17: Example 83 is a UPSC GS Paper II ethics scenario, confirming civil-service framing inside the taxonomy.
- DATASET-D45: Example 8 (FORTRAN 77 fixed-format) — taxonomy includes post-secondary engineering content unlikely in any school-board syllabus.
- DATASET-D46: Example 104 (AM receiver intermediate frequency) — polytechnic/engineering specialisation.
- DATASET-D47: Example 2 (Archery Asia Cup 2022) — current-affairs item not aligned to board syllabi.

</details>

**Information gaps:**
- No published mapping between MILU subjects and UP/MP/Rajasthan/Bihar board syllabus chapters.
- Subject-level item counts for Hindi specifically not publicly accessible (gated dataset).

**Requires expert verification:**
- Whether a Hindi-medium board teacher would judge the 41-subject schema as adequately representing Class 9-12 board curricular structure.

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Input content is the highest-priority dimension per the elicitation (HIGH) and shows the most significant validity concerns. While MILU is India-first and includes some North Indian state-specific content (UP minerals, Rajasthan geography, Chikankari, Panchayati Raj), the dataset analysis reveals a CRITICAL finding: 100% of the 245 sampled Hindi validation items carry is_translated: True, far exceeding the paper's reported dataset-wide 25% translation rate. This raises serious concerns about Hindi-register fidelity for items used as few-shot exemplars. Multiple MAJOR concerns compound this: canonical Hindi literary figures (Tulsidas, Premchand, Kabir, Mahadevi Varma) were entirely absent from the sample; English vocabulary questions ('didactic', 'grim', 'Evangelize') appear inside Hindi Language Studies; ~3-4% of items have truncated stems making them unevaluable; framing is dominated by UPSC/SSC/state-civil-service GK rather than board syllabus content. State-wise exam-source distribution for Hindi items is undocumented. The deployment user did note that competitive-exam answer keys are broadly compatible with North Indian teacher norms, mitigating but not eliminating these concerns.

**Strengths:**
- Genuine North Indian state-specific content present (UP minerals, Rajasthan districts and literacy, Bihar e-cigarette policy, UP Chikankari) [DATASET-D6, DATASET-D15, DATASET-D26, DATASET-D34].
- India-first design with explicit inclusion of regional and state-level exam material [Q11, Q14, Q28].
- Hindi grammar items (indirect speech, postpositions, voice) align with board Language Studies content [DATASET-D4, DATASET-D20].
- Indian constitutional and Panchayati Raj content aligned with civics syllabi [DATASET-D2, DATASET-D19, DATASET-D48].

**Checklist:**

- **IC-1**: Yes — deployment requires Hindi-belt cultural, regional, and dialectal knowledge (canonical Hindi literature, North Indian medieval history, state administrative content). MILU includes some such material [Q2, Q12, DATASET-D6, DATASET-D34] but coverage is uneven. — _Sources: Q2, Q12, DATASET-D6, DATASET-D34, DATASET-D19_
- **IC-2**: Partial alignment. India-centric framing is genuine [Q11, Q30] but the validation sample showed canonical Hindi-board literary figures absent and English-vocabulary items embedded in Hindi Language Studies subject [DATASET-D16, DATASET-D18, DATASET-D22], indicating cultural/curricular misalignment for the target deployment. — _Sources: Q11, Q30, DATASET-D16, DATASET-D18, DATASET-D22, WEB-19_
- **IC-3**: Some Western/non-regional content present: William Wordsworth, Man Booker Prize, English vocabulary items [DATASET-D3, DATASET-D25, DATASET-D16]. Also South Indian regional content (Pandya, Silappatikaram, Tamil Bharati) [DATASET-D10, DATASET-D23, DATASET-D33] — appropriate for pan-India exams but dilutive for North-Indian-board deployment. — _Sources: DATASET-D3, DATASET-D10, DATASET-D16, DATASET-D23, DATASET-D25, DATASET-D33_
- **IC-4**: INSUFFICIENT DOCUMENTATION — MILU does not document recruitment of regional annotators by language; AI4Bharat volunteers and online-portal subject experts are referenced [Q26, Q87] but no Hindi-medium North Indian regional annotator pool is specified. Web search confirmed no public source resolves this (gap_id 6). — _Sources: Q26, Q87_
- **IC-5**: Multiple content issues compromising content validity: (a) 100% translation rate in the sampled validation split [DATASET-D35], (b) absence of canonical Hindi literary canon from sample, (c) truncated/unanswerable items (~3-4%) [DATASET-D37 through D44], (d) competitive-exam framing dominance [Q24, DATASET-D17, DATASET-D47], (e) English vocabulary masquerading as Hindi Language Studies [DATASET-D16, DATASET-D22]. — _Sources: DATASET-D35, DATASET-D37, DATASET-D38, DATASET-D39, DATASET-D40, DATASET-D41, DATASET-D42, DATASET-D43, DATASET-D44, DATASET-D17, DATASET-D47, Q44, Q47_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws' (p.1)
- [Q11] 'We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams.' (p.2)
- [Q14] 'We focus on region-specific exams to authentically capture local knowledge in the respective language.' (p.2)
- [Q44] 'For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O.' (p.4)
- [Q47] 'Of the total 79K questions, only 25% of questions are translated from English' (p.4)
- [Q72] 'This suggests that the training corpora for these models lack sufficient culturally specific data.' (p.7)
- [Q84] 'Third, the scarcity of questions necessitated translating a portion of the dataset.' (p.9)

*Web sources:*
- [WEB-19] Bihar's standard Hindi is native to only ~25.5% of population; Bhojpuri/Maithili/Magahi dominate — register risk for postgraduate Hindi teachers in Bihar.
- [WEB-12] GitHub repository indicates Literature and Linguistics and Arts and Culture as subjects but no published item-level framing detail.
- [WEB-9] Dataset is gated on HuggingFace, limiting independent validation of Hindi-specific translation/source distribution.

*Dataset analysis:*
- DATASET-D35: 100% (245/245) of sampled Hindi validation items marked is_translated: True — CRITICAL finding inconsistent with paper's 25% dataset-wide claim.
- DATASET-D1: Translated DC-series-motor item with potentially anglicised technical Hindi vocabulary.
- DATASET-D3: 'विलियम वर्ड्सवर्थ ... इंग्लैंड' — translated Western literary content rather than Hindi literary canon.
- DATASET-D6: UP minerals question — genuine North Indian regional content present.
- DATASET-D15: Rajasthan district reserved-area question — North-Indian state-specific content.
- DATASET-D16: English word 'didactic' meaning tested inside Hindi Language Studies subject.
- DATASET-D17: UPSC GS Paper II ethics scenario — competitive-exam framing dominant.
- DATASET-D22: 'Evangelize' English-vocabulary item in Hindi Language Studies.
- DATASET-D34: UP Chikankari handicraft — North Indian cultural content directly relevant.
- DATASET-D37 through D44: Multiple items with truncated stems (referenced statements, sub-options, sentences absent from question field) rendering them unanswerable.
- DATASET-D47: Time-stamped current-affairs item (Archery Asia Cup 2022).

</details>

**Information gaps:**
- Hindi-specific translation proportion in test split unknown; whether the 100% translation rate seen in validation extends to test split needs gated-access verification.
- State-wise (UP/MP/Rajasthan/Bihar) exam-source distribution for Hindi items not published.
- No comparison published between MILU Hindi items and UP/MP/Rajasthan/Bihar board syllabi.
- Whether GPT-4O Hindi translations conform to Vaigyaanik evam Takniki Shabdavali Aayog standardised scientific terminology vs. anglicised transliteration.

**Requires expert verification:**
- Hindi-medium board teacher review of a sample of translated items for register fidelity.
- Subject-expert audit of truncated items and items where English vocabulary is tested inside Hindi Language Studies.
- Test-split sampling to confirm whether canonical Hindi literary figures appear with adequate coverage.

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form is well-aligned with the deployment. Both benchmark and deployment are text-only Hindi MCQs in Devanagari script (Unicode U+0900-U+097F), which is a high-resource pairing with mature NLP tooling. MILU enforces format uniformity (4 options, no images, no reading comprehension) [Q33] and applies INDICLID + Unicode filtering for language verification [Q34]. The dataset analysis confirms consistent formal Khari Boli register throughout the sample with no script mismatches or romanisation issues. Two minor form-level concerns reduce the score from 5: (a) ~3-4% of sampled items have truncated/missing question stems where tables or sub-item lists were lost during scraping, breaking item form integrity [DATASET-D37 through D44]; (b) Logical Reasoning items use Latin alphabet sequences inside Hindi wrappers, which is standard for competitive exams but introduces a slight English-literacy dependency [DATASET-D36].

**Strengths:**
- Devanagari Unicode rendering with consistent formal Khari Boli register matches deployment requirement [DATASET-D4, DATASET-D20].
- Format uniformity enforced via explicit exclusion of images, reading-comprehension passages, and >4-option questions [Q33].
- Language verification via INDICLID + Unicode filtering [Q34] and duplicate removal [Q35].
- Hindi is a high-resource language within MILU's scope, favouring inference performance [Q5, Q76].

**Checklist:**

- **IF-1**: Signal distributions match: text-only Devanagari Hindi in both benchmark and deployment. Formal Khari Boli register confirmed consistent across the validation sample [DATASET strength 1]. — _Sources: Q34, Q5_
- **IF-2**: Regional infrastructure supports text-only Hindi MCQ ingestion. Devanagari IME availability on mobile is mature though precise teacher-cohort adoption [NEEDS VERIFICATION]; mobile internet penetration is ~43% Bihar, ~46% UP per IAMAI/Kantar 2024 [WEB-4], implying capacity but with rural connectivity constraints. — _Sources: WEB-4, WEB-5_
- **IF-3**: MCQ form (4 options + single answer) precisely matches deployment requirement [Q33]. No multimedia, no reading-comprehension passages, no >4-option items. — _Sources: Q33_
- **IF-4**: Two minor form mismatches: (a) ~3-4% of items have form-corruption from scraping (truncated stems missing referenced tables/sub-items) [DATASET-D37 through D44]; (b) Latin alphabetic sequences inside Logical Reasoning items [DATASET-D36] — standard for Indian competitive exams but a minor structural artifact. — _Sources: DATASET-D36, DATASET-D37, DATASET-D38, DATASET-D39, DATASET-D40, DATASET-D41, DATASET-D42, DATASET-D43, DATASET-D44_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q34] 'we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering ... ensuring that the questions are in the correct language.' (p.4)
- [Q35] 'we remove any duplicate questions to retain only the unique ones.' (p.4)
- [Q5] 'Models also perform better in high-resource languages as compared to low-resource ones.' (p.1)

*Web sources:*
- [WEB-4] Bihar internet penetration ~43%, UP ~46% (IAMAI/Kantar ICUBE 2024) — adequate for text-only Hindi MCQ but rural constraints exist.
- [WEB-5] Rural school internet access ~18% vs. urban 62% — relevant to enterprise deployment reach.

*Dataset analysis:*
- Strength 1: Consistent Devanagari Unicode and formal Khari Boli register across all 245 sampled items.
- DATASET-D37 through D44: 7-8 items in 245 with truncated stems where referenced tables/sub-items lost in scraping.
- DATASET-D36: Latin letter sequences inside Hindi-wrapper Logical Reasoning items.

</details>

**Information gaps:**
- Hindi Devanagari IME adoption rate among the specific postgraduate teacher cohort.
- Whether truncation defects observed in validation split also affect the test split.

---

### Output Ontology — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output ontology aligns very well with deployment. MILU produces a single correct option per MCQ drawn from exam answer keys [Q12, Q26], scored as binary correct/incorrect — structurally identical to the deployment's positive/negative marking requirement. The user explicitly confirmed (Q4 elicitation) that no rubric-based or graded output is needed. Domain-level reporting is granular [Q42, Q98]. Two concerns reduce the score from 5: (a) a malformed item where an instruction line ('use the code below') appears as an answer option, indicating output-label corruption [DATASET-D49]; (b) culturally variable correct-answer norms are not discussed in the paper, though the user confirmed evaluation schemas are broadly consistent across boards and competitive exams, mitigating this concern.

**Strengths:**
- Single-correct-answer label schema matches deployment's binary scoring schema exactly [Q22, Q42].
- Per-domain, per-language, per-subject evaluation tables enable Hindi-specific analysis [Q98, Q99-Q132].
- Culturally relevant domain categorisation (Arts & Humanities, Law & Governance) explicitly reported [Q20, Q71].

**Checklist:**

- **OO-1**: Output labels (option1-4 with single target) are regionally relevant — they replicate the standard Indian MCQ answer-key format used by all North Indian boards [Q12, Q22]. — _Sources: Q12, Q22_
- **OO-2**: No regionally specific output category is missing for the binary MCQ scoring use case. Rubric-based or graded output not required per deployment elicitation. — _Sources: Q42_
- **OO-3**: INSUFFICIENT DOCUMENTATION on whether any items encode non-regional values; the user noted competitive-exam keys are broadly consistent with North Indian teacher norms (elicitation Q4), but the paper does not analyse culturally variable correct-answer norms.
- **OO-4**: Stakeholder taxonomy redesign not required — schema is a precise structural match. — _Sources: Q42_
- **OO-5**: Minor structural-validity concern from a malformed answer option [DATASET-D49] indicating data-quality erosion of the output schema; the issue is item-level rather than schema-level. — _Sources: DATASET-D49_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science.' (p.2)
- [Q22] 'multiple-choice based questions (MCQs) taken from over 41 subjects' (p.3)
- [Q26] 'subject experts ensure the accuracy of the answers.' (p.3)
- [Q42] '41 distinct subject names, which fall into eight main domains' (p.4)
- [Q20] 'Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM.' (p.2)

*Dataset analysis:*
- Strength 2: All 245 sampled items follow 4-option single-target format — precise structural match to deployment.
- DATASET-D49: Example 135 has formatting instruction 'use the code below' as option4 — malformed item, output-schema corruption.

</details>

**Information gaps:**
- Frequency of malformed-option items beyond the validation sample observed.
- Whether any Hindi items have answer keys that diverge from North Indian teacher norms (no documented IAA).

**Requires expert verification:**
- Spot-check of Hindi answer keys against UP/MP/Rajasthan/Bihar board model-answer expectations.

---

### Output Content — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Annotation relied on subject experts at online exam portals [Q26] plus AI4Bharat volunteer audit [Q87], with manual cluster-to-subject assignment [Q41]. The paper does not provide annotator demographic details (regional background, Hindi-medium vs. English-medium, subject expertise) and does not report inter-annotator agreement. Web search confirmed no published source resolves this gap (gap_id 6). The institutional base (IIT Madras + IBM Research India) does not guarantee Hindi-medium North Indian regional representation. The user's confirmation (elicitation Q4) that competitive-exam keys are broadly consistent with North Indian teacher norms substantially mitigates concern, supported by dataset evidence that answer keys for India-centric items appear standard. However, for items requiring regionally specific judgments (e.g., Hindi literary canon, regional history framing) the absence of annotator-demographic transparency leaves a moderate gap.

**Strengths:**
- Subject experts at exam portals manually tagged questions and ensured answer accuracy [Q26].
- AI4Bharat volunteer audit layer adds quality assurance [Q87].
- Manual cluster-to-subject label assignment rather than fully automated [Q41].
- User confirmation that evaluation schemas are broadly consistent across North Indian boards and competitive exams reduces label-disagreement risk for typical items.

**Checklist:**

- **OC-1**: Partially. Ground-truth labels derive from competitive-exam answer keys [Q26], which the user confirmed are broadly compatible with North Indian teacher norms (elicitation Q4). However, no Hindi-medium North Indian stakeholder-perspective validation is documented. — _Sources: Q26_
- **OC-2**: Disagreement risk is moderate: typical India-GK items show good alignment, but for culturally specific items (canonical Hindi literature framing, regional history interpretations) the absence of annotator-demographic data prevents firm assessment. — _Sources: Q26, Q41_
- **OC-3**: INSUFFICIENT DOCUMENTATION — no Datasheet or Data Statement section provides annotator demographics. Institutional affiliation (IIT Madras, IBM Research India) is documented [Q9, Q10] but does not guarantee Hindi-medium North Indian representation. Web search confirmed this gap remains unresolved (gap_id 6). — _Sources: Q9, Q10, WEB-10_
- **OC-4**: Re-annotation by Hindi-medium North Indian teachers would strengthen convergent validity, particularly for Arts & Humanities, Hindi Literature, and regional history items. Not currently performed.
- **OC-5**: INSUFFICIENT DOCUMENTATION — no inter-annotator agreement statistics are reported, so aggregation/erasure of minority perspectives cannot be assessed.
- **OC-6**: Convergent-validity concern is moderate due to undocumented annotator demographics, partially mitigated by user-confirmed schema consistency. External validity for culturally specific items remains uncertain. — _Sources: Q26, Q87_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q26] 'These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers.' (p.3)
- [Q41] 'We manually review these clusters and assign appropriate subject labels.' (p.4)
- [Q87] 'We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits.' (p.9)
- [Q9] 'Sshubam Verma, Mohammed Safi Ur Rahman Khan, Vishwajeet Kumar, Rudra Murthy, Jaydeep Sen' (p.1)
- [Q10] 'Nilekani Centre at AI4Bharat, Indian Institute of Technology, Madras, IBM Research, India' (p.1)

*Web sources:*
- [WEB-10] NAACL 2025 paper confirms institutional base (IIT Madras + IBM Research India) but does not publish annotator demographics.
- [WEB-19] Bihar's Hindi-as-mother-tongue is only ~25.5% — relevant to whether Bihar Hindi-medium teachers' register expectations match annotator outputs.

</details>

**Information gaps:**
- Annotator demographic profile (regional background, language medium, subject expertise).
- Inter-annotator agreement statistics for Hindi items.
- Whether any Hindi-medium North Indian teachers were involved in audit.

**Requires expert verification:**
- Hindi-medium North Indian teacher review of a sample of culturally specific items (literature, regional history, civics) to assess label consistency with regional norms.

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output form aligns well with the deployment. Accuracy is the primary metric [Q3, Q15], with log-likelihood scoring for non-API models via LM-EVALUATION-HARNESS [Q52-Q55] and structured-JSON generative scoring for API models [Q56, Q57]. Both approaches produce a single answer-label output that maps directly to the deployment's binary correct/incorrect requirement. The deployment requires binary correct/incorrect feedback, which this output form supports natively. Reporting at 0/1/5-shot levels [Q50, Q100] gives operational flexibility. The authors explicitly acknowledge that log-likelihood evaluation may yield different results from generation-based or chain-of-thought approaches [Q85] — a caveat that matters if the deployment uses generative inference. API models are evaluated zero-shot only due to cost [Q58], potentially limiting comparability with few-shot deployment configurations.

**Strengths:**
- Accuracy-based binary scoring directly maps to deployment's positive/negative marking requirement [Q3, Q15, Q16].
- Reproducible evaluation via LM-EVALUATION-HARNESS [Q52].
- Structured JSON generative output for API models matches programmatic-integration needs [Q57].
- 0/1/5-shot reporting enables deployment-config sensitivity analysis [Q50, Q100].

**Checklist:**

- **OF-1**: Output modality (single answer-label) matches deployment's binary correct/incorrect feedback requirement [Q15, Q55, Q57]. — _Sources: Q15, Q55, Q57_
- **OF-2**: TTS not required — deployment is text-only Hindi mobile/desktop application per deployment_modality field.
- **OF-3**: Target population is postgraduate-qualified teachers (high literacy assumed); accessibility considerations beyond Devanagari rendering not flagged in elicitation. INSUFFICIENT DOCUMENTATION on benchmark-side accessibility analysis but not relevant for this deployment.
- **OF-4**: Minor mismatch: log-likelihood scoring [Q53-Q55] differs from generation-based deployment inference; the paper acknowledges this as a limitation [Q85]. API-evaluation zero-shot constraint [Q58] may limit comparability with deployments running few-shot. — _Sources: Q53, Q54, Q55, Q58, Q85_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%.' (p.1)
- [Q15] 'We evaluate 45 different LLMs ... on MILU.' (p.2)
- [Q52] 'For non-API-based models, we use the LM-EVALUATION-HARNESS ... to ensure clean and reproducible evaluations.' (p.5)
- [Q55] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability' (p.5)
- [Q57] 'We explicitly prompt these models to generate the correct response in a structured JSON format' (p.5)
- [Q58] 'Due to the high costs involved, these models are evaluated only in the zero-shot setup.' (p.5)
- [Q85] 'our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting.' (p.9)

</details>

**Information gaps:**
- Whether the deployment will use log-likelihood or generation-based inference; benchmark caveat suggests results may differ across these modes.

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** 100% of sampled Hindi validation items are translated (vs. paper's claimed 25% dataset-wide); canonical Hindi-board literary figures absent from the sample; English vocabulary embedded in Hindi Language Studies.

**Recommendation:** Filter MILU Hindi items by is_translated flag and prefer natively sourced items for evaluation; supplement with a custom Hindi Literature MCQ set covering canonical board authors (Tulsidas, Premchand, Kabir, Mahadevi Varma); reclassify or remove English-vocabulary items mislabelled under Hindi Language Studies.

### Input Ontology ⚠

**Gap:** Taxonomy derived from competitive exams (UPSC/SSC/state civil services) rather than school/board syllabi; no subject category represents Class 9-12 board curricular structure.

**Recommendation:** Define a deployment-specific subject mapping that aligns MILU subjects to UP/MP/Rajasthan/Bihar board syllabus chapters; downweight or exclude post-secondary engineering and ethics-scenario items that exceed school-board scope.

### Input Form

**Gap:** Approximately 3-4% of sampled items have truncated stems where referenced tables, sub-items, or sentences were lost during scraping.

**Recommendation:** Programmatically detect items whose options reference content (numbered statements, lettered sub-items, named sentences) absent from the question stem and exclude them prior to deployment evaluation; report exclusion rate transparently.

### Output Content

**Gap:** No published annotator demographics or inter-annotator agreement; representation of Hindi-medium North Indian educators in annotation/audit unknown.

**Recommendation:** Recruit a small panel of Hindi-medium North Indian board teachers (3-5 per state across UP/MP/Rajasthan/Bihar) to re-annotate a stratified sample of 200-500 culturally specific items (Hindi Literature, regional history, regional civics) and measure label agreement with MILU keys.

### Output Form

**Gap:** Headline accuracy figures are computed via log-likelihood scoring, which the authors note may diverge from generation-based or chain-of-thought evaluation [Q85]; deployment may use generative inference.

**Recommendation:** Re-run MILU Hindi evaluation in the deployment's actual inference mode (generative, with structured JSON output) on at least the candidate model to ensure accuracy estimates reflect deployed behaviour.

### Output Ontology

**Gap:** At least one item observed where a formatting instruction appears as an answer option (DATASET-D49), indicating data-quality erosion of the output label schema.

**Recommendation:** Run a heuristic audit of all Hindi options to detect instruction-like strings (e.g., 'नीचे दिए गए कोड का उपयोग करके') appearing as answer choices and exclude or correct affected items.

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

**Dataset(s):** ai4bharat/MILU (Hindi config)
**Analysis date:** 2025-01-30
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | MILU/Hindi | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" | DC series motor no-load speed — translated Engineering item | IC, IF |
| D2 | MILU/Hindi | 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? 44वें संविधान संशोधन अधिनियम द्वारा" | Constitutional amendment — Law & Governance item | IO, IC |
| D3 | MILU/Hindi | 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" | William Wordsworth's nationality — translated Arts/Literature item, non-Indian literary content | IC |
| D4 | MILU/Hindi | 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" | Hindi indirect speech conversion — Language Studies item | IC, IF |
| D5 | MILU/Hindi | 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" | Mughal text authorship — History item with India-specific content | IO, IC |
| D6 | MILU/Hindi | 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? अभ्रक" | UP-specific minerals question — North Indian regional geography | IC, IO |
| D7 | MILU/Hindi | 28 | option2 | "निम्नलिखित में से कौन खेरवार आंदोलन के नेता थे? भागीरथ मांझी" | Kherwar movement leader — regional tribal history | IC |
| D8 | MILU/Hindi | 32 | option4 | "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया। इल्तुतमिश" | Completion of Qutub Minar — medieval Indian history | IO, IC |
| D9 | MILU/Hindi | 48 | option3 | "भांड पाथेर थिएटर मुख्य रूप से भारत के निम्नलिखित में से किस राज्य/केंद्र शासित प्रदेश की परंपरा है? जम्मू और कश्मीर" | Bhand Pather theatre tradition — regional Indian arts | IC |
| D10 | MILU/Hindi | 52 | option2 | "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था, वह था सुंदर पांड्यन" | Pandya kingdom history — South Indian dynastic history, not North India | IC |
| D11 | MILU/Hindi | 54 | option3 | "भारत की पहली टेक्नीकलर फिल्म कौन सी है? झांसी की रानी" | First Technicolor Indian film — India GK, Rani Lakshmibai connection | IC |
| D12 | MILU/Hindi | 57 | option4 | "किस राज्य सरकार ने राज्य भर में इलेक्ट्रॉनिक सिगरेट के निर्माण और बिक्री-खरीद पर पूर्ण प्रतिबंध लगाया है? बिहार" | Bihar e-cigarette ban — North Indian state-level policy | IC |
| D13 | MILU/Hindi | 64 | option3 | "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है? सरदार वल्लभभाई पटेल" | Iron Man of India — national GK, competitive exam style | IO, IC |
| D14 | MILU/Hindi | 65 | option4 | "झारखंड की उप राजधानी क्या है? दुमका" | Jharkhand sub-capital — regional Indian geography | IC |
| D15 | MILU/Hindi | 68 | option2 | "निम्नलिखित में से राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है? बीकानेर" | Rajasthan reserved area — North Indian state-specific geography | IC |
| D16 | MILU/Hindi | 76 | option2 | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है? नैतिक पाठ पढ़ाना" | Meaning of English word 'didactic' asked in Hindi — English vocabulary test | IC |
| D17 | MILU/Hindi | 83 | option1 | "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है" | Civil officer ethics scenario — UPSC/civil services ethics framing | IO, IC |
| D18 | MILU/Hindi | 90 | option3 | "शब्द 'grim' का पर्यायवाची लिखें। भयानक" | Synonym of English word 'grim' asked in Hindi | IC |
| D19 | MILU/Hindi | 93 | option2 | "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है? पंचायत समिति" | Three-tier Panchayati Raj — civics, relevant to North Indian governance | IC, IO |
| D20 | MILU/Hindi | 97 | option3 | "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है। का" | Hindi postposition fill-in — language/grammar item | IC, IF |
| D21 | MILU/Hindi | 98 | option1 | "किस प्रसिद्ध कश्मीरी कवि को आमतौर पर 'कश्मीर का जॉन कीट्स' कहा जाता है? रसूल मीर" | Kashmiri poet comparison to John Keats — regional literature | IC |
| D22 | MILU/Hindi | 105 | option4 | "निर्देश: निम्नलिखित प्रश्न में...Evangelize [का अर्थ] उपदेश देना" | English vocabulary 'Evangelize' — meaning tested in Hindi | IC |
| D23 | MILU/Hindi | 108 | option3 | "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए? सी. सुब्रह्मण्य भारती" | First cartoons in Tamil magazine — South Indian literary history | IC |
| D24 | MILU/Hindi | 115 | option4 | "निम्नलिखित लेखकों में से किसने लघु कथाओं के संग्रह 'किस्सा किस्सा लखनऊवा' के लिए साहित्य अकादमी युवा पुरस्कार 2021 जीता? हिमांशु वाजपेयी" | Sahitya Akademi award for Lucknow-themed stories — North Indian literary content | IC |
| D25 | MILU/Hindi | 130 | option4 | "2019 का मैन बुकर पुरस्कार फिक्शन के लिए जीतने वाली पहली अश्वेत महिला कौन बनी हैं? बर्नाडिन एवरिस्टो" | Man Booker Prize winner — international literary GK | IC |
| D26 | MILU/Hindi | 156 | option1 | "2011 की जनगणना के अनुसार राजस्थान की कुल साक्षरता का लगभग प्रतिशत कितना है? 66.11%" | Rajasthan literacy rate — North Indian state statistics | IC |
| D27 | MILU/Hindi | 182 | option1 | "निम्नलिखित में से किस राज्य ने 2011 - 12 में सबसे अधिक दूध उत्पादन दर्ज किया? उत्तर प्रदेश" | Milk production by state — UP-relevant agricultural GK | IC |
| D28 | MILU/Hindi | 190 | option2 | "राजस्थान का आकार है- समचतुर्भुज" | Rajasthan's shape — state-specific geography | IC |
| D29 | MILU/Hindi | 193 | option3 | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है? महाराव उम्मेद सिंह I" | Kota painting school — Rajasthan regional arts | IC |
| D30 | MILU/Hindi | 198 | option2 | "छत्तीसगढ़ के निम्नलिखित विद्रोहों में से किसे 'बस्तर का स्वतंत्रता संग्राम' भी कहा जाता है? लिंगागिरी विद्रोह" | Chhattisgarh tribal revolt — Central Indian regional history | IC |
| D31 | MILU/Hindi | 211 | option3 | "राजस्थान सरकार ने मौसमी और गैर-संचारी रोगों की निगरानी के लिए...कौन सा सॉफ्टवेयर लॉन्च किया है? निदान" | Rajasthan state health software — state-level policy GK | IC |
| D32 | MILU/Hindi | 213 | option1 | "राजतरंगिणी के लेखक कौन हैं? कल्हण" | Rajatarangini author — classical Sanskrit text, competitive-exam GK | IC |
| D33 | MILU/Hindi | 232 | option2 | "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है? इलंगो अडिगल" | Tamil epic Silappatikaram — South Indian literary history | IC |
| D34 | MILU/Hindi | 242 | option4 | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है...चिकनकारी" | UP handicraft Chikankari — North Indian craft, directly relevant | IC, IO |
| D35 | MILU/Hindi | All 245 | — | All 245 examples have `is_translated: True` | Every sampled item is marked as translated from English | IC, IF |
| D36 | MILU/Hindi | 36 | option3 | "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है। TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______." | Letter series with English alphabet labels — Logical Reasoning item | IC, IF |
| D37 | MILU/Hindi | 56 | option2 | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें...केवल (1) और (3)" | Reference to numbered statements not present in the question field — truncated/incomplete item | IC, IF |
| D38 | MILU/Hindi | 69 | option2 | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल" | Options reference (a),(b),(c),(d) labels absent from question stem — truncated item | IC, IF |
| D39 | MILU/Hindi | 86 | option2 | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" | Options reference A,B,C,D,E state labels not named in the question — truncated item | IC, IF |
| D40 | MILU/Hindi | 95 | option1 | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। AEDBCF" | Sentence ordering question where actual sentences B,C,D,E are missing | IC, IF |
| D41 | MILU/Hindi | 106 | option2 | "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" | Ordering question where the numbered substances are not listed | IC, IF |
| D42 | MILU/Hindi | 188 | option3 | "नई शिक्षा नीति 2020 में देखा गया है...निम्नलिखित में से किन समस्याओं का सामना कर रही है? उपरोक्त सभी" | Sub-items (a),(b) not listed in question stem — truncated | IC, IF |
| D43 | MILU/Hindi | 118 | option2 | "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें। अपने काम को बेहतर तरीके से व्यवस्थित करना" | Idiom question with no idiom in the stem — missing content | IC, IF |
| D44 | MILU/Hindi | 151 | option1 | "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं। केवल तर्क I मजबूत है" | Statement and arguments not present in question field — truncated item | IC, IF |
| D45 | MILU/Hindi | 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" | FORTRAN 77 programming — highly specialized computing, unlikely in state board | IO |
| D46 | MILU/Hindi | 104 | option4 | "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" | AM receiver intermediate frequency — specialized electronics | IO |
| D47 | MILU/Hindi | 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" | Archery Asia Cup 2022 results — current affairs, time-sensitive | IC |
| D48 | MILU/Hindi | 34 | option1 | "किस कानून के तहत, विधायिका के सदस्य बजट की आलोचना नहीं कर सकते थे? भारतीय परिषद अधिनियम-1892" | Colonial Indian Council Act — constitutional/legal history | IO, IC |
| D49 | MILU/Hindi | 135 | option3 | "पंचायतों के संबंध में निम्नलिखित में से कौन सा/से सही है/हैं?...नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें:" | Option4 of the MCQ is an instruction ("use the code below"), not an answer — malformed item | OO |
| D50 | MILU/Hindi | 10 | option4 | "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" | Blue Baby Syndrome cause — Health/Medicine competitive-exam item | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Devanagari Hindi script with standard formal register throughout
- **Dimension(s):** IF, IC
- **Observation:** All 245 sampled items are rendered in standard Devanagari Unicode Hindi with a formal, pan-India Khari Boli register appropriate for competitive examinations and board-level assessments. Vocabulary is standard Sanskrit-derived academic Hindi (e.g., "संवैधानिक संशोधन", "पंचायती राज प्रणाली", "सहजीवी संबंध"). No script inconsistencies, romanisation, or Perso-Arabic loanword conflicts were observed.
- **Deployment relevance:** The deployment requires Devanagari script text-only interaction. The consistent formal Hindi register matches what North Indian board teachers and students encounter in official examination materials.
- **Datapoint citations:**
  - [D4] Example 9 (MILU/Hindi, validation, option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — Standard formal Hindi grammatical question, consistent with board-level language items.
  - [D20] Example 97 (MILU/Hindi, validation, option3): "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है। का" — Hindi postposition fill-in, academic register.

#### Strength 2: Strong MCQ structural alignment with deployment format
- **Dimension(s):** IO, OO
- **Observation:** All 245 sampled items are 4-option single-correct-answer MCQs with a single `target` field containing the correct option label. The binary correct/incorrect evaluation schema is structurally identical to the deployment's positive/negative marking requirement. No multi-select, open-ended, or partial-credit items appear in the sample.
- **Deployment relevance:** The deployment requires strict MCQ format with single correct answers and binary scoring. MILU's format is a precise match, reducing any format-translation burden.
- **Datapoint citations:**
  - [D2] Example 6 (MILU/Hindi, validation, option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — Classic 4-option MCQ, single correct answer.
  - [D13] Example 64 (MILU/Hindi, validation, option3): "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है?" — Standard GK MCQ format.

#### Strength 3: Meaningful coverage of India-centric Law & Governance and Civics content
- **Dimension(s):** IO, IC
- **Observation:** Multiple items address Indian constitutional law (constitutional amendments, writs, parliamentary procedure), Panchayati Raj (three-tier system, gram sabha), and India-specific legal provisions (SC/ST Prevention of Atrocities Act, Sati Prevention Act). These subjects align directly with the civics and political science portions of North Indian board syllabi.
- **Deployment relevance:** North Indian state board syllabi (UP, MP, Rajasthan, Bihar) prominently include Indian polity and constitutional studies. Items on Panchayati Raj (Example 93), constitutional writs (Example 33), and constitutional amendments (Example 6, 39, 136) are directly deployable against board-level student assessments.
- **Datapoint citations:**
  - [D19] Example 93 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है? पंचायत समिति" — Panchayati Raj content directly relevant to North Indian civics syllabi.
  - [D2] Example 6 (MILU/Hindi, validation, option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? 44वें संविधान संशोधन अधिनियम द्वारा" — Constitutional amendment knowledge.
  - [D48] Example 34 (MILU/Hindi, validation, option1): "किस कानून के तहत, विधायिका के सदस्य बजट की आलोचना नहीं कर सकते थे? भारतीय परिषद अधिनियम-1892" — Indian legislative history.

#### Strength 4: Meaningful presence of North Indian state-specific geographical and cultural content
- **Dimension(s):** IC
- **Observation:** Several items in the sample are directly anchored to North Indian states: UP minerals (Example 26), Rajasthan's district geography (Example 68, 190), Rajasthan literacy statistics (Example 156), UP milk production (Example 182), Rajasthan health policy (Example 211), and UP's Chikankari craft (Example 242). This confirms that MILU's region-specific exam sourcing does include some Hindi-belt state content.
- **Deployment relevance:** The deployment population of North Indian teachers needs to evaluate students on state-board content about their own states. These items demonstrate that MILU is not exclusively pan-India competitive content.
- **Datapoint citations:**
  - [D6] Example 26 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? अभ्रक" — UP-specific geography question.
  - [D15] Example 68 (MILU/Hindi, validation, option2): "निम्नलिखित में से राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है? बीकानेर" — Rajasthan district-level geography.
  - [D34] Example 242 (MILU/Hindi, validation, option4): "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है...चिकनकारी" — UP handicraft, directly North Indian cultural content.
  - [D28] Example 190 (MILU/Hindi, validation, option2): "राजस्थान का आकार है- समचतुर्भुज" — Rajasthan-specific geographic question.

#### Strength 5: Coverage of Indian medieval and modern history in Hindi
- **Dimension(s):** IO, IC
- **Observation:** History items cover Mughal-era texts (Example 25), medieval construction history (Example 32), Indian freedom movement framing (Example 64, 235), ancient Indian history (Example 158, 237), and colonial-era governance (Example 50, 96). These are standard components of North Indian board history syllabi.
- **Deployment relevance:** History is a core subject in all Hindi state board syllabi. Items on Ashoka (Example 158), the Qutub Minar (Example 32), the Iron Man of India (Example 64), and Harappan cities (Example 237) align with topics examined at secondary level in UP, MP, Rajasthan, and Bihar boards.
- **Datapoint citations:**
  - [D8] Example 32 (MILU/Hindi, validation, option4): "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया। इल्तुतमिश" — Medieval Indian history.
  - [D5] Example 25 (MILU/Hindi, validation, option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" — Mughal historiography.

#### Strength 6: Hindi language and grammar items present in Language Studies subject
- **Dimension(s):** IC, IO
- **Observation:** The sample includes Hindi grammatical exercises covering active/passive voice conversion (Example 51, 91), indirect speech (Example 9), postposition usage (Example 97), and fill-in-the-blank sentence completion (Example 152). These are directly aligned with Hindi language instruction at board level.
- **Deployment relevance:** Hindi Language and Literature is a compulsory subject in all North Indian board curricula. Grammar items on voice, indirect speech, and postpositions are standard components of Class 10–12 Hindi papers.
- **Datapoint citations:**
  - [D4] Example 9 (MILU/Hindi, validation, option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — Indirect speech (reported speech) conversion.
  - [D20] Example 97 (MILU/Hindi, validation, option3): "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है। का" — Hindi postposition fill-in.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: 100% of sampled validation items are marked `is_translated: True`
- **Dimension(s):** IC, IF
- **Observation:** All 245 sampled examples from the Hindi validation split carry `is_translated: True`. The benchmark documentation states that only ~25% of total questions across all 11 languages were translated from English; if Hindi's validation split is entirely composed of translated items, this would substantially exceed the reported dataset-wide average. Even if this is an artifact of the validation split (vs. the test split), an evaluator relying on the validation split for few-shot examples would be drawing exclusively from translated content.
- **Deployment relevance:** Translated items may not reflect the natural Hindi academic register used in North Indian board assessments. GPT-4O translations may produce grammatically correct but register-misaligned Hindi — particularly for subject-specific terminology (science, economics, civics) — that diverges from what UP, MP, Rajasthan, or Bihar board students and teachers would encounter. This is the single highest-risk finding in the sample.
- **Datapoint citations:**
  - [D35] All 245 examples: `is_translated: True` on every record — every item in the validation split is a translation.
  - [D1] Example 1 (MILU/Hindi, validation, option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" — Translated engineering item; technical Hindi vocabulary (e.g., "डीसी सीरीज मोटर") may follow English-derived transliteration rather than standardised Hindi scientific terminology.
  - [D3] Example 7 (MILU/Hindi, validation, option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" — Translated item on a British poet, clearly sourced from English.

---

#### MAJOR

#### MAJOR Concern 1: Numerous items with truncated or missing question stems rendering them unevaluable
- **Dimension(s):** IC, IF
- **Observation:** At least 7–8 items in the 245-item sample have options that reference content (numbered statements, lettered sub-items, named sentences) that is absent from the `question` field. This indicates that the original question included a table, passage, or list that was stripped during scraping, leaving the MCQ shell unanswerable without the missing context.
- **Deployment relevance:** If a deployed LLM encounters these items, it cannot evaluate the question correctly — neither can a teacher using the benchmark for reference. These items inflate measurement error and cannot serve their intended evaluative function.
- **Datapoint citations:**
  - [D37] Example 56 (MILU/Hindi, validation, option2): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें...केवल (1) और (3)" — Four statements referenced but absent from question stem.
  - [D38] Example 69 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल" — Options reference (a),(b),(c),(d) items absent from question.
  - [D39] Example 86 (MILU/Hindi, validation, option2): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" — State labels A–E not identified in the question.
  - [D40] Example 95 (MILU/Hindi, validation, option1): "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। AEDBCF" — The actual sentences are missing.
  - [D41] Example 106 (MILU/Hindi, validation, option2): "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" — Numbered substances not listed.
  - [D43] Example 118 (MILU/Hindi, validation, option2): "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें। अपने काम को बेहतर तरीके से व्यवस्थित करना" — The idiom itself is absent from the question field.
  - [D44] Example 151 (MILU/Hindi, validation, option1): "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं। केवल तर्क I मजबूत है" — Statement and arguments missing from stem.
  - [D42] Example 188 (MILU/Hindi, validation, option3): "नई शिक्षा नीति 2020 में देखा गया है...निम्नलिखित में से किन समस्याओं का सामना कर रही है? उपरोक्त सभी" — Sub-items (a),(b) absent.

#### MAJOR Concern 2: Absence of canonical Hindi literary figures (Tulsidas, Premchand, Kabir, Mahadevi Varma) from the sample
- **Dimension(s):** IC, IO
- **Observation:** No item in the 245-item sample tests knowledge of canonical Hindi-board literary figures — Tulsidas, Premchand, Kabir, Mahadevi Varma, Harivansh Rai Bachchan, or Surdas. The Literature and Linguistics items present are either about: (a) English literary figures (William Wordsworth, Example 7; Man Booker Prize winner, Example 130), (b) South Indian authors (C. Subramania Bharati, Example 108; Silappatikaram, Example 232; Telugu author, Example 126), (c) English vocabulary meanings ('didactic', Example 76; 'grim', Example 90; 'Evangelize', Example 105), or (d) regional/marginal Hindi literary awards (Example 115). While the sample is limited to the validation split and may not reflect test split content, this complete absence is notable.
- **Deployment relevance:** Canonical Hindi literature (Ramcharitmanas, Premchand's Godan, Kabir's dohas) is a required component of every Hindi state board syllabus (UP, MP, Rajasthan, Bihar) at Class 9–12. A benchmark used to evaluate MCQ responses from Hindi-board students that lacks these authors cannot validly assess Hindi literature performance in the deployment context.
- **Datapoint citations:**
  - [D3] Example 7 (MILU/Hindi, validation, option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" — British poet identified instead of Hindi literary canon.
  - [D33] Example 232 (MILU/Hindi, validation, option2): "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है? इलंगो अडिगल" — South Indian Tamil epic, not North Indian Hindi literature.
  - [D22] Example 105 (MILU/Hindi, validation, option4): "निर्देश: निम्नलिखित प्रश्न में...Evangelize [का अर्थ] उपदेश देना" — English vocabulary test embedded in Hindi Language Studies subject.
  - [D16] Example 76 (MILU/Hindi, validation, option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है? नैतिक पाठ पढ़ाना" — English word meaning tested in Hindi Language Studies.

#### MAJOR Concern 3: Competitive-exam framing dominates; minimal school-board syllabus framing visible
- **Dimension(s):** IO, IC
- **Observation:** The vast majority of items in the sample are structured as UPSC/SSC/state civil service GK-style questions — current affairs (Examples 2, 11, 35, 88, 131), government schemes and policies (Examples 82, 102, 122, 148, 239), constitutional/legal facts (Examples 6, 33, 34, 39, 42, 46, 136), and administrative GK (Examples 50, 71, 72, 132, 165). Only a small subset of items (Hindi grammar, some art history, a few biology/chemistry items) resembles the classroom-instruction framing typical of board-level syllabi. Ethics scenario items (Example 83) are explicitly UPSC Civil Services Paper II format.
- **Deployment relevance:** North Indian board teachers assess students on syllabus-aligned content, not current-affairs or civil-service GK. A benchmark skewed toward civil-service exam framing will produce validity estimates that do not reflect whether an LLM can evaluate students on UP Board Class 12 Hindi, History, or Science papers.
- **Datapoint citations:**
  - [D17] Example 83 (MILU/Hindi, validation, option1): "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है..." — Clearly UPSC GS Paper II (Ethics, Integrity and Aptitude) format scenario.
  - [D47] Example 2 (MILU/Hindi, validation, option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — Current affairs sports GK, not a board syllabus topic.
  - [D13] Example 64 (MILU/Hindi, validation, option3): "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है? सरदार वल्लभभाई पटेल" — Standard competitive-exam GK format.

#### MAJOR Concern 4: English-vocabulary questions embedded in Hindi Language Studies subject
- **Dimension(s):** IC, IO
- **Observation:** Multiple items in the Language Studies and Literature and Linguistics subjects test the meaning or synonym of English words, presented in a Hindi instructional frame. Examples include: meaning of 'didactic' (Example 76), synonym of 'grim' (Example 90), meaning of 'Evangelize' (Example 105), and active/passive voice for "क्या आवाज़ ने उसे परेशान किया?" (an English-language structure reframed in Hindi, Example 91). These appear to be translated from English-medium competitive exam language papers.
- **Deployment relevance:** Hindi state board Language Studies papers test Hindi grammar and Hindi literature, not English vocabulary. Items testing synonyms of English words, when labelled as Hindi Language Studies, would produce systematically misleading validity estimates for the deployment — a model that succeeds on these items is being tested on English proficiency, not Hindi Language Studies competence.
- **Datapoint citations:**
  - [D16] Example 76 (MILU/Hindi, validation, option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है? नैतिक पाठ पढ़ाना" — Testing English word meaning within Hindi Language Studies subject.
  - [D18] Example 90 (MILU/Hindi, validation, option3): "शब्द 'grim' का पर्यायवाची लिखें। भयानक" — English synonym tested in Hindi.
  - [D22] Example 105 (MILU/Hindi, validation, option4): "निर्देश: निम्नलिखित प्रश्न में...Evangelize [का अर्थ] उपदेश देना" — English religious term meaning in Hindi Language Studies.

#### MAJOR Concern 5: Malformed answer option — an instruction appearing as an answer choice
- **Dimension(s):** OO, IF
- **Observation:** Example 135 (Panchayats/Politics and Governance) has its fourth option read: "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें:" ("Select the correct answer using the code below:") — a formatting instruction from the original question, not an answer choice. The target is `option3`. This is a scraping artifact where the answer-code table was stripped but the instruction line was retained as an option.
- **Deployment relevance:** If a deployed model encounters this item, it may select option4 (the instruction) as an answer. This is a data quality defect that can corrupt both model evaluation scores and teacher trust in the system.
- **Datapoint citations:**
  - [D49] Example 135 (MILU/Hindi, validation, option3): "पंचायतों के संबंध में...नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें:" — An instruction line masquerading as answer option 4.

---

#### MINOR

#### MINOR Concern 1: Non-North-Indian regional content takes substantial share of Arts & Humanities and History
- **Dimension(s):** IC
- **Observation:** Several Arts & Humanities History and Literature items in the sample concern South Indian history and literature: Pandya kingdom (Example 52), Tamil epic Silappatikaram (Example 232), Tamil magazine cartoons (Example 108), Telugu book authorship (Example 126), Kashmiri poet (Example 98), and Kota painting (Rajasthan, Example 193). While pan-Indian content is appropriate for general competitive exams, it dilutes the North Indian board syllabus alignment for this specific deployment.
- **Deployment relevance:** North Indian board history syllabi emphasise Mughal, Rajput, and North Indian medieval history, and North Indian freedom movement figures. South Indian dynastic history (Pandya, Chola) and Tamil literary history are less emphasized. This is a calibration concern rather than a fundamental misalignment.
- **Datapoint citations:**
  - [D10] Example 52 (MILU/Hindi, validation, option2): "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था, वह था सुंदर पांड्यन" — South Indian Pandya dynasty, not a North Indian board syllabus priority.
  - [D23] Example 108 (MILU/Hindi, validation, option3): "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए? सी. सुब्रह्मण्य भारती" — Tamil literary history.

#### MINOR Concern 2: Time-sensitive current-affairs items create staleness risk
- **Dimension(s):** IC, OC
- **Observation:** Multiple items are tied to specific events from 2018–2022 with exact statistics that become outdated (e.g., India's GDP growth rate in July–September 2018, Example 74; ASSOCHAM president December 2020, Example 123; Minister of WCD in 2018, Example 132; India's first UNDP Youth Climate Champion in January 2022, Example 239). These items have objectively correct answers only at a specific point in time.
- **Deployment relevance:** If teachers use MILU items to create new assessment questions, or if the LLM is evaluated on whether it correctly marks student answers to these current-affairs questions, staleness could cause the system to mark correct historical answers as incorrect if the LLM's training data reflects a different time period.
- **Datapoint citations:**
  - [D47] Example 2 (MILU/Hindi, validation, option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — Time-stamped sports result.
  - Example 132 (MILU/Hindi, validation, option4): "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं? मेनेका गांधी" — Cabinet position tied to a specific year.

#### MINOR Concern 3: Highly specialised Engineering and Tech content unlikely to appear in school-board assessments
- **Dimension(s):** IO
- **Observation:** A substantial number of Engineering & Tech items are highly specialised — FORTRAN 77 programming (Example 8), AM/SSB-SC modulation bandwidth (Example 43, 104), TDM frame rate calculations (Example 47), and timber fibre swelling percentages (Example 12). These are appropriate for polytechnic entrance exams or engineering qualification tests but not for school-board level assessments.
- **Deployment relevance:** The deployment covers all board types including secondary level, where Engineering & Tech content would be introductory at most. The presence of advanced technical content within what is labelled as the Hindi MILU benchmark means the benchmark over-represents post-secondary technical exam difficulty for the school-board teacher deployment.
- **Datapoint citations:**
  - [D45] Example 8 (MILU/Hindi, validation, option1): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" — FORTRAN 77 programming — highly specialised computing, unlikely in any board syllabus.
  - [D46] Example 104 (MILU/Hindi, validation, option4): "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" — AM receiver IF — polytechnic/engineering level.

#### MINOR Concern 4: Logical Reasoning items use English alphabetic sequences
- **Dimension(s):** IC, IF
- **Observation:** Logical Reasoning items in the Science domain use sequences of Latin/English letters (TAB, TTZBB, etc. in Example 36; _q p p_ in Example 44; A, C, F, H, ?, M in Example 124) despite being presented in Hindi. The question wrapper is in Hindi but the reasoning object is English alphanumeric.
- **Deployment relevance:** This is a minor structural concern — Hindi board students are familiar with English alphabetic sequences in reasoning tests, which appear in many competitive exams. However, it does confirm the competitive-exam sourcing of Logical Reasoning items and may introduce a slight English-literacy dependency.
- **Datapoint citations:**
  - [D36] Example 36 (MILU/Hindi, validation, option3): "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है...TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______. TTTTXBBBB" — Latin letter series reasoning.

---

### Content Coverage Summary

The Hindi validation split of MILU (245 items sampled) spans eight domains with notable concentration in Engineering & Tech (approx. 25%), Science (approx. 20%), Environmental Sciences including Geography and Agriculture (approx. 15%), and Arts & Humanities (approx. 20%), with smaller contributions from Business Studies, Law & Governance, Social Sciences, and Health & Medicine. All items are in standard formal Devanagari Hindi. The entire validation sample is marked `is_translated: True`, which is inconsistent with the paper's reported 25% dataset-wide translation rate and represents the most significant data-quality finding from the sample.

Content topics reflect a pan-Indian competitive-exam orientation: UPSC/SSC-style general knowledge, constitutional law, Indian polity, India-centric science GK, and current affairs. India-centric content is genuinely present (North Indian state geography, Panchayati Raj, Chikankari, medieval Indian history), but canonical Hindi board literary figures (Tulsidas, Premchand, Kabir) are entirely absent from the sample, and Hindi Literature and Linguistics items instead test English vocabulary meanings.

Data quality concerns are non-trivial: approximately 3–4% of sampled items have truncated stems where tables, passages, or sub-item lists were lost during scraping, rendering the question unanswerable. One item has a formatting instruction appearing as an answer option.

The register throughout is uniform formal Hindi — appropriate for the deployment — but the framing is overwhelmingly competitive-exam (UPSC/SSC/state civil service) rather than school/university board syllabus instruction.

---

### Limitations

1. **Validation split only:** All 245 examples are from the validation split (812 total items). The test split contains 14,831 Hindi items. The `is_translated: True` finding on all validation items may not generalise to the test split, which likely contains a higher proportion of natively sourced Hindi questions. The canonical Hindi literature absence, truncation defects, and competitive-exam framing findings should be verified against a sample of the test split before drawing strong conclusions.

2. **Sample size relative to total:** 245 items out of 15,643 total Hindi items (~1.6%) limits subject-level inferences. Subjects like Hindi Literature specifically may have more board-aligned items in the test split that did not appear in this sample.

3. **Subject distribution not controllable:** The sample was drawn from the validation split as provided; subject distribution within the sample may over- or under-represent specific subjects relative to the full test split.

4. **Translation quality not auditable from text alone:** While register concerns about GPT-4O translations can be flagged, assessing whether specific technical translations (electronics, chemistry, economics) use the correct Hindi-board terminology (Vaigyaanik evam Takniki Shabdavali Aayog standard terms vs. transliterated English) requires domain-expert review beyond what can be determined from reading the items.

5. **Annotator demographics unverifiable:** The demographic backgrounds of item annotators and the exam-source distribution for Hindi items cannot be determined from the dataset content alone, as this metadata is not exposed in the HuggingFace schema.

6. **Test split gating:** The test split is available via gated access on HuggingFace (auto-gated), meaning independent validation of subject distribution and translation rates for the full Hindi test set requires dataset access approval.

