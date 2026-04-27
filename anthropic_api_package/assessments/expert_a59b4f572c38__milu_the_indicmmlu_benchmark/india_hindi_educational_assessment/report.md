## Deployment Context

**Use case:** Deployment scenario: A Hindi-speaking teacher in India uses an LLM to evaluate student responses in an examination setting, assign scores with the support of an AI system, and provide feedback.

Domain: Educational assessment
Setting: Mobile application / enterprise software

Note: The deployment hypothesis should be tested using Hindi-language sentences from the benchmark, as I am familiar with the language and can provide evaluation at a subsequent stage.
**Target population:** A postgraduate- or PhD-qualified teacher with 0–20+ years of teaching experience in Hindi, based in North India and interacting in the Hindi language.

# Validity Analysis: MILU
**Target context:** North India Hindi-Medium Postgraduate Teacher — MCQ Assessment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology | 3 | Moderate gaps | medium |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form | 3 | Moderate gaps | high |
| Output Ontology ✓ | 3 | Moderate gaps | medium |
| Output Content ⚠ | 2 | Significant gaps | medium |
| Output Form ✓ | 5 | Strong alignment | high |
| **Average** | **2.8** | | |

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

MILU is structurally well-suited to the deployment's MCQ format, scoring scheme, and Devanagari script-language pairing — Output Form, Output Ontology, and Input Form macro-alignment are strong. However, Input Content shows severe, multi-stream validity violations for the North Indian Hindi-medium teacher deployment: dataset analysis reveals that the sampled Hindi validation split is 100% translated (vs. the paper's claimed 25%), ~6%+ of items have truncated stems making them functionally unanswerable, canonical North Indian Hindi-board literary figures (Tulsidas, Premchand, Kabir, Mahadevi Verma) are absent while Tamil/Telugu/Kashmiri content predominates, English-vocabulary items appear within the Hindi benchmark, and competitive-exam framing (UPSC-Mains-style ethics scenarios) crowds out school-board pedagogical framing. The paper itself acknowledges that models perform worst in Arts & Humanities and Social Sciences — precisely the domains where Hindi-belt teachers most need reliable evaluation. With Input Content rated HIGH priority by elicitation, these findings translate into substantial deployment risk that the paper's documentation alone would not surface.

## Practical Guidance

### What This Benchmark Measures

MILU can help evaluate an LLM's ability to answer Indian competitive-exam-style MCQs in Hindi with binary correct/incorrect scoring — specifically its handling of Devanagari script, India-centric general-knowledge content, and STEM domains where it performs comparatively well. The strongest dimensions for the deployment are Output Form (perfect alignment with binary scoring), Output Ontology (matched MCQ taxonomy), and macro-level Input Form (text-only Devanagari).

### Construct Depth

MILU probes broad-but-shallow Indian competitive-exam knowledge across 41 subjects, with per-language and per-subject accuracy tables enabling Hindi-specific isolation. However, depth is limited where the deployment most needs it: Hindi-board canonical literature, regional Hindi-belt history/civics, and school-board pedagogical framings are under-represented or absent in the sampled data. The benchmark does not probe whether a model can score student responses in alignment with state-board teacher answer keys; it only probes whether a model can answer competitive-exam keys in Hindi.

### What Else You Need

For a complete deployment assessment, supplementation is required in three areas: (1) a Hindi-board curricular MCQ evaluation set drawn from UP/MP/RBSE/BSEB/CBSE Class 9–12 papers and aligned to NEP 2020/NCERT 2024 revisions [WEB-5, WEB-12] — addressing the Input Content gap; (2) Hindi-belt teacher annotator review of a stratified item sample for cultural/curricular framing concordance — addressing the Output Content gap; (3) item-level filtering or audit for the ~6%+ truncated-stem items [DATASET-MAJOR1] before reporting accuracy figures. IndicMMLU-Pro [WEB-11] and the 2025 Hindi instruction-following suite [WEB-13] are noted but neither addresses the school-board curricular gap.

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
MILU's MCQ-based, India-centric taxonomy of 8 domains and 41 subjects [Q1, Q42] partially aligns with the deployment's MCQ assessment needs across Hindi-belt boards, and the inclusion of culturally relevant subjects [Q12, Q74] is consistent with the user's school-board scope. However, the taxonomy is derived from competitive-exam sources [Q24, Q92] rather than school or university board syllabi, and the coarse aggregation of ~20K fine-grained tags into 41 subjects [Q39, Q42] obscures whether canonical Hindi-board topics (Hindi literature, regional medieval history) are adequately represented. Dataset evidence shows Literature and Linguistics items in the Hindi sample skewing to non-Hindi-belt content (Tamil, Telugu, Kashmiri, English Romantic poets) with no Tulsidas/Premchand/Kabir/Mahadevi Verma items observed [DATASET-MAJOR2]. The taxonomy thus omits or under-resolves regionally relevant categories central to the deployment.

**Strengths:**
- MCQ-only format with single-correct-answer structure [Q22, Q33] directly matches the deployment's binary-scoring MCQ assessment requirement.
- Explicit India-first design that values regional/state-level exams for capturing local knowledge [Q14, Q28] makes the taxonomy more deployment-relevant than English-origin alternatives like MMLU.
- Eight domains span the breadth of school-board subject areas (Arts & Humanities, Social Sciences, Science, Law and Governance, Business Studies) [Q42], covering the deployment's listed subject domains at a coarse level.

**Checklist:**

- **IO-1**: Required categories for the deployment include Hindi literature (canonical figures Tulsidas, Premchand, Kabir, Mahadevi Verma, Prasad, Nirala, Dinkar), regional history (UP, MP, Rajasthan, Bihar), civics/Constitution, geography of Hindi-belt states, and Hindi-medium science/maths. MILU declares 8 domains and 41 subjects [Q1, Q42] including Arts and Humanities, Social Sciences, Science and Law and Governance — covering the deployment's domains at the macro level, but with school-board-specific sub-categories not separately delineated. — _Sources: Q1, Q42_
- **IO-2**: MILU's taxonomy was built bottom-up from ~20K competitive-exam tags clustered into 41 subjects [Q39, Q40, Q42], not from school-board syllabi. The paper does not list a 'Hindi literature' or 'Hindi-board regional history' subject; such content appears subsumed within broader 'Arts and Humanities' labels. Dataset analysis shows the Hindi Literature and Linguistics subject contains Tamil, Telugu, Kashmiri, and English-vocabulary items rather than canonical Hindi-board literary content [DATASET-MAJOR2, DATASET-MAJOR3], suggesting taxonomic granularity insufficient for the deployment. — _Sources: Q39, Q42, DATASET-MAJOR2, DATASET-MAJOR3_
- **IO-3**: The taxonomy includes Engineering and Technology and (per elicitation) lower-priority Health and Medicine [Q42], which are largely irrelevant to school-board MCQ teacher assessment. MAJOR4 finding documents UPSC-Mains-style ethics scenarios appearing in Social Sciences/Sociology [DATASET-MAJOR4] — a category of construct-irrelevant variance for school-board MCQ contexts. — _Sources: Q42, DATASET-MAJOR4_
- **IO-4**: Documented gaps: (a) absence of explicit Hindi-board literature, regional-history, and state-civics sub-categories; (b) coarse 41-subject aggregation hides whether canonical Hindi-board topics are present at all; (c) inclusion of UPSC-Mains-style civil-services reasoning items as construct-irrelevant variance for the school-board deployment. — _Sources: Q39, DATASET-MAJOR2, DATASET-MAJOR4, WEB-9_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge.' (p.1)
- [Q22] 'MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge.' (p.3)
- [Q24] 'These questions were sourced following an approach similar to AGIEVAL ... collecting the questions from various public exams ... such as qualification tests and national and state-level civil services exams' (p.3)
- [Q39] 'Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap.' (p.4)
- [Q42] 'we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies.' (p.4)

*Web sources:*
- [WEB-9] MILU paper provides subject-language granularity but no per-state source breakdown for Hindi-belt states.
- [WEB-8] MILU GitHub now reports ~85K questions vs. ~79K in paper, indicating dataset is being updated.

*Dataset analysis:*
- DATASET-MAJOR2: Sampled Hindi Literature and Linguistics items reference Tamil, Telugu, Kashmiri, and English-Romantic content, with no canonical Hindi-board literary figures observed in 245 sampled items.
- DATASET-MAJOR4: Social Sciences subject contains UPSC-Mains-style civil-servant ethics scenario (Ex. 83) — competitive-exam framing not aligned with school-board MCQ taxonomy.

</details>

**Information gaps:**
- Whether 'Hindi literature' is a discrete subject within MILU's 41-subject scheme or subsumed under 'Literature and Linguistics' is not explicit in the paper.
- Whether school-board syllabus topics (vs. competitive-exam topics) are systematically represented within the 41-subject taxonomy is not documented.

**Requires expert verification:**
- Hindi-board curriculum specialist review of which MILU subjects map to which board syllabus topics.
- Subject-matter expert audit to confirm absence of Tulsidas/Premchand/Kabir items beyond the 245-item sample.

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Input Content is the highest-priority dimension per elicitation and shows the most severe validity violations. Dataset analysis reveals: (1) all 245 sampled Hindi validation items are flagged is_translated=True [DATASET-CRITICAL1], sharply at odds with the paper's 25% translated figure [Q47] and indicating the few-shot/validation calibration corpus may be wholly translated rather than organically Indic-sourced; (2) ~6% of sampled items have truncated/incomplete question stems where referenced statements/options are absent [DATASET-MAJOR1]; (3) the canonical North Indian Hindi literary figures listed as high-priority for the deployment (Tulsidas, Premchand, Kabir, Mahadevi Verma) are absent from the sample, while Tamil, Telugu, Kashmiri literary content predominates [DATASET-MAJOR2, DATASET-MAJOR5]; (4) English-vocabulary items (didactic, grim, evangelize) appear within the Hindi-language benchmark as construct-irrelevant content [DATASET-MAJOR3]; (5) social science items skew to UPSC-Mains-style ethics scenarios rather than school-board civics MCQs [DATASET-MAJOR4]. The flagged-gaps summary further confirms no per-state breakdown of Hindi-belt exam contributions is documented [WEB-9, WEB-8]. These are concrete, multi-stream violations of content validity for the deployment.

**Strengths:**
- Explicit India-first sourcing methodology incorporating regional and state-level exams [Q2, Q11, Q14] is a content-design strength relative to translated-from-English alternatives.
- English questions with India-specific content are deliberately included [Q30], addressing a gap in popular benchmarks.
- Some Hindi-belt regional content does appear (UP minerals Ex. 26, Rajasthan Bajju area Ex. 68, UP chikankari Ex. 242) [DATASET-D26, DATASET-D28, DATASET-D29, DATASET-D30].

**Checklist:**

- **IC-1**: The deployment requires region-specific Hindi-belt knowledge (UP/MP/Rajasthan/Bihar history, geography, governance) and canonical Hindi-board literary content. MILU explicitly targets India-centric content [Q2, Q11], but dataset analysis shows under-representation of Hindi-belt regional content with disproportionate South Indian/Eastern/Kashmiri content in Arts & Humanities [DATASET-MAJOR5, DATASET-MAJOR2]. — _Sources: Q2, Q11, DATASET-MAJOR5, DATASET-MAJOR2_
- **IC-2**: Cultural alignment is partially achieved at the national India-centric level [Q12, Q30] but fails at the Hindi-belt sub-national level. Canonical Hindi-board literature is absent from the sample [DATASET-MAJOR2]; competitive-exam framing dominates over school-board pedagogical framing [DATASET-MAJOR4]. — _Sources: Q12, DATASET-MAJOR2, DATASET-MAJOR4_
- **IC-3**: MILU contains content not aligned to the deployment context: English vocabulary tested via Hindi translation [DATASET-MAJOR3], UPSC-Mains-style civil-servant ethics scenarios [DATASET-MAJOR4], and time-stamped current-affairs items (e.g., Ex. 40 GDP Q3 2018, Ex. 41 May 2022 archery cup, Ex. 42 2018 cabinet minister) [DATASET-D40, DATASET-D41, DATASET-D42] that suit civil-services prep but not school-board curricular assessment. — _Sources: DATASET-MAJOR3, DATASET-MAJOR4, DATASET-D40, DATASET-D41, DATASET-D42_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the paper documents AI4Bharat manual audits [Q87] but no regional Hindi-belt annotator review of content cultural alignment. Documentation does not specify whether annotators familiar with UP/MP/Bihar/Rajasthan board syllabi audited the Hindi item set.
- **IC-5**: Documented content issues: (a) validation split appears 100% translated despite paper's 25% figure [DATASET-CRITICAL1, Q47]; (b) ~6%+ items are functionally unanswerable due to truncated stems [DATASET-MAJOR1]; (c) canonical Hindi-board literary content absent [DATASET-MAJOR2]; (d) English-vocabulary items as construct-irrelevant variance [DATASET-MAJOR3]; (e) competitive-exam framing dominates [DATASET-MAJOR4]; (f) South Indian/non-Hindi-belt regional content over-represented [DATASET-MAJOR5]; (g) no per-state Hindi-belt source breakdown [WEB-9]; (h) potential syllabus-currency mismatch with NEP 2020/NCERT 2024 revisions [WEB-5, WEB-12]. — _Sources: Q47, DATASET-CRITICAL1, DATASET-MAJOR1, DATASET-MAJOR2, DATASET-MAJOR3, DATASET-MAJOR4, DATASET-MAJOR5, WEB-9, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science.' (p.1)
- [Q11] 'We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams.' (p.2)
- [Q24] 'collecting the questions from various public exams ... such as qualification tests and national and state-level civil services exams' (p.3)
- [Q44] 'For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O.' (p.4)
- [Q47] 'Of the total 79K questions, only 25% of questions are translated from English' (p.4)

*Web sources:*
- [WEB-9] MILU paper provides no per-state breakdown of Hindi-language item counts for UPPSC, MPPSC, RPSC, or BPSC.
- [WEB-8] MILU GitHub repo does not document per-state Hindi-belt source distribution.
- [WEB-5] NCERT released revised textbooks for Classes 3 and 6 in 2024 under NEP 2020; Classes 4, 5, 7, 8 planned 2025–26 — creates syllabus-currency risk for items sourced from older exam papers.
- [WEB-12] NEP 2020 implementation is ongoing across states with autonomous timelines.

*Dataset analysis:*
- DATASET-CRITICAL1: All 245 sampled Hindi validation examples flagged is_translated=True, contradicting the paper's 25% translated figure and suggesting validation/few-shot calibration is entirely from translated origin.
- DATASET-MAJOR1: Pervasive truncated question stems — at least 14/245 sampled items reference statements/options/underlined text not present in the question field, making items functionally unanswerable.
- DATASET-MAJOR2: Hindi Literature and Linguistics items reference Tamil/Telugu/Kashmiri/English-Romantic literature; no Tulsidas/Premchand/Kabir/Mahadevi Verma items found in 245-item sample.
- DATASET-MAJOR3: Hindi-language benchmark contains English-vocabulary items (didactic, grim, evangelize) testing English proficiency through Hindi translation — construct-irrelevant variance.
- DATASET-MAJOR4: Social Sciences contains UPSC-Mains-style ethics scenarios and PCS-style argument-strength items unsuited to school-board MCQ assessment.
- DATASET-MAJOR5: South Indian, Kashmiri, Eastern Indian regional content over-represented in Arts & Humanities and Geography; UP/MP/Bihar/Rajasthan content sparse.

</details>

**Information gaps:**
- Whether the test split (vs. validation split) has the same is_translated distribution as the sampled validation split.
- What fraction of the full Hindi item set is functionally truncated beyond the 245-item sample.
- Per-state distribution of Hindi-language items by source exam (UPPSC, MPPSC, RPSC, BPSC).
- Whether translated Hindi register matches the formal Khari Boli expected in state-board contexts.

**Requires expert verification:**
- Hindi-board subject-matter experts to audit a larger sample for Hindi-board curricular coverage.
- Linguistic review of GPT-4O-translated items for North Indian academic register conformity.
- Item-level review of canonical literary content framing (literary-critical vs. competitive-exam GK).

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
At the gross signal-distribution level, input form is well-aligned: text-only Devanagari MCQ items match the deployment's text-only Devanagari Hindi-medium use case; INDICLID and Unicode-based filtering are documented [Q34]; up-to-four-option uniformity is enforced [Q33]; reading comprehension and image-based items are excluded [Q33]. However, dataset analysis surfaces concrete form-level defects: ~14/245 sampled items have truncated stems where referenced content (numbered statements, lettered options, underlined text, idioms) is absent from the question field [DATASET-MAJOR1] — this is a form/encoding defect (the structured fields do not contain the full question signal) that will systematically depress measured accuracy unrelated to language competence. The English-vocabulary-in-Hindi-wrapping issue [DATASET-MAJOR3] is also partly a form issue (the input mixes scripts/languages in unintended ways). These form defects undermine external validity of measured scores even though the script/modality alignment itself is strong.

**Strengths:**
- Text-only Devanagari script-language pairing matches deployment exactly [Q34].
- Multiple cleaning layers (INDICLID, Unicode filtering, deduplication, manual sampling) are documented [Q31, Q32, Q34, Q35, Q36].
- MCQ uniformity (≤4 options, no images, no reading comprehension) [Q33] aligns with deployment's MCQ-only constraint.
- Low-bandwidth-friendly form suits Hindi-belt infrastructure where rural connectivity is variable [WEB-3, WEB-4].

**Checklist:**

- **IF-1**: Signal distributions align: text-only Devanagari in both source and target contexts; MILU enforces script correctness via INDICLID and Unicode filtering [Q34]. — _Sources: Q34_
- **IF-2**: Regional infrastructure (Android smartphones, 4G in urban Hindi-belt with variable rural coverage) supports text-only MCQ delivery; no capture-side mismatch [WEB-3, WEB-4]. — _Sources: WEB-3, WEB-4_
- **IF-3**: Domain-specific form difference: dataset analysis shows a non-trivial fraction of items have structurally incomplete question stems where referenced content is missing from the question field [DATASET-MAJOR1, DATASET-D10, DATASET-D11, DATASET-D12, DATASET-D13, DATASET-D14, DATASET-D15, DATASET-D16, DATASET-D17, DATASET-D18, DATASET-D19]. English-vocabulary items embedded in Hindi wrappers [DATASET-MAJOR3] are a secondary form-level mismatch. — _Sources: DATASET-MAJOR1, DATASET-MAJOR3_
- **IF-4**: Documented form mismatches: (a) truncated/incomplete question stems making items functionally unanswerable [DATASET-MAJOR1]; (b) the 25% GPT-4O-translated subset's register fidelity to formal Khari Boli is undocumented (paper applies INDICLID for script but no register check) [Q34, Q44]; (c) Unicode normalization (NFC/NFD/nukta) consistency across the Hindi item set is not documented in the paper. — _Sources: DATASET-MAJOR1, Q34, Q44_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q34] 'we utilize a combination of INDICLID ... and Unicode-based filtering ... ensuring that the questions are in the correct language.' (p.4)
- [Q44] 'we sampled questions from the English set from that subject and translated them into the required language using GPT-4O.' (p.4)

*Web sources:*
- [WEB-3] Hindi-belt internet penetration variable (Bihar ~25%, UP ~30%) but text-only modality is low-bandwidth tolerant.
- [WEB-4] UP/Bihar have large absolute internet subscriber bases supporting text MCQ delivery.

*Dataset analysis:*
- DATASET-MAJOR1: At least 14/245 sampled items have structurally incomplete question stems where referenced statements/options/underlined text is absent from the question field.
- DATASET-MAJOR3: English-vocabulary items embedded in Hindi-wrapper form mix script/language in ways that conflate construct measurement.

</details>

**Information gaps:**
- Unicode normalization consistency across MILU's Hindi item set is not documented.
- Fraction of truncated-stem items in the test split (as opposed to the sampled validation split) is unknown.

**Requires expert verification:**
- Hindi linguist review of GPT-4O-translated items for register and orthographic fidelity to formal Khari Boli.

---

### Output Ontology — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
MILU's output space — single correct answer from up to four options with binary correct/incorrect scoring [Q22, Q33, Q55] — directly matches the deployment's binary-scoring requirement and is a strong alignment per elicitation Q1/Q2 (LOWER priority dimension). However, the paper itself acknowledges that models perform poorly in culturally relevant domains (Arts & Humanities, Social Sciences, Law & Governance) compared to STEM [Q6, Q20, Q62, Q71], and attributes this to training-corpora gaps [Q72] — directly relevant since these are the deployment's high-priority domains. The 41-subject coarse aggregation [Q39, Q42] subsumes Hindi-board-specific cultural sub-categories under broader labels, limiting structural validity at the sub-category level. Thus the output taxonomy is structurally aligned at the macro level (binary MCQ, India-centric subjects) but mismatched at the granular level where the deployment's highest-priority assessment lives.

**Strengths:**
- Single-correct-answer MCQ output with binary scoring [Q22, Q55] exactly matches the deployment's positive/negative-marking binary scheme.
- Culturally relevant subject areas are explicitly part of the output taxonomy [Q12, Q42].
- Per-language, per-subject, per-shot accuracy tables (Tables 11–54) [Q99–Q132] enable Hindi-specific isolation, supporting deployment-relevant analysis.
- Paper transparently flags the cultural-knowledge weakness as a limitation [Q6, Q77].

**Checklist:**

- **OO-1**: Output label categories are binary correct/incorrect over 4-option MCQs [Q22, Q55] — directly relevant and matched to the deployment's evaluation scheme per elicitation Q2. — _Sources: Q22, Q55_
- **OO-2**: Missing fine-grained categories: Hindi-board sub-subjects (Hindi literature canonical authors, regional medieval history, state civics) are not separately resolved within the 41-subject scheme [Q39, Q42], limiting the deployment's ability to isolate performance on its highest-priority topic clusters. — _Sources: Q39, Q42_
- **OO-3**: The output taxonomy itself does not encode non-regional values; however, the inclusion of Engineering/Health subjects [Q42] and competitive-exam-framed Sociology/Ethics items [DATASET-MAJOR4] introduces categories that inflate breadth without serving the deployment. — _Sources: Q42, DATASET-MAJOR4_
- **OO-4**: INSUFFICIENT DOCUMENTATION on stakeholder involvement in taxonomy design — paper documents AI4Bharat team manual review of K-means clusters [Q41] but no Hindi-belt teacher or board-curriculum stakeholder consultation. A stakeholder-driven taxonomy redesign for school-board granularity would be warranted.
- **OO-5**: Documented taxonomy issues: (a) coarse 41-subject scheme hides Hindi-board sub-categories [Q39]; (b) STEM-vs-cultural performance gap concentrated in deployment's highest-priority domains [Q6, Q20, Q71, Q72]; (c) lack of school-board-aligned sub-categories prevents content-validity verification at the level the deployment cares about. — _Sources: Q6, Q20, Q71, Q72, Q39_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs)' (p.3)
- [Q55] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability' (p.5)
- [Q6] 'models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM.' (p.1)
- [Q20] 'models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM.' (p.2)
- [Q71] 'open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields.' (p.7)
- [Q72] 'the training corpora for these models lack sufficient culturally specific data.' (p.7)
- [Q42] 'we determine 41 distinct subject names, which fall into eight main domains' (p.4)

*Dataset analysis:*
- DATASET-MAJOR4: Sociology subject contains UPSC-Mains-style ethics scenarios — a category whose taxonomic placement does not match school-board civics teacher-assessment ontology.

</details>

**Information gaps:**
- Whether MILU's 41-subject scheme can be re-mapped post-hoc to school-board topic taxonomy.

**Requires expert verification:**
- Hindi-board curriculum specialist mapping of MILU subjects to UP/MP/RBSE/BSEB/CBSE syllabus topics.

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
Although the elicitation marks OC as LOWER priority because evaluation schemas are claimed to be broadly consistent across boards [Q4 elicitation], multiple concrete label-provenance concerns remain: (1) the validation split is empirically 100% translated [DATASET-CRITICAL1], meaning few-shot calibration uses GPT-4O-translated answer keys whose correctness in formal Hindi-board register is unverified; (2) annotation is delegated to original exam portals [Q26] with no published demographic breakdown, and the AI4Bharat team is institutionally based at IIT Madras (Chennai) — geographically distant from the Hindi belt; (3) ~6%+ of items are functionally unanswerable yet still carry a 'correct' target label [DATASET-MAJOR1], meaning ground-truth correctness cannot be construct-validly verified for those items; (4) one law item (Ex. 127) tests the year the IPC took effect (target=1862) [DATASET-D43] — a factual answer-key whose correctness is uncontroversial, but the broader label-reliability of competitive-exam-sourced keys for school-board contexts is not externally validated. Although OC is lower priority, multiple concrete issues make a score of 2 appropriate.

**Strengths:**
- Original exam portals tag questions and subject experts verify answer accuracy [Q26], providing a baseline label-quality mechanism.
- AI4Bharat team conducted manual audits [Q87], adding a second review layer.
- User confirms evaluation schemas are broadly consistent across North Indian boards [elicitation Q4], reducing mismatch severity.
- MILU was built by an India-based team (AI4Bharat / IIT Madras / IBM Research India) [Q10], better than out-of-region annotation.

**Checklist:**

- **OC-1**: The user states evaluation schemas are broadly consistent across North Indian boards and competitive-exam settings [elicitation Q4], suggesting moderate alignment of ground-truth labels with regional stakeholder perspectives. However, no Hindi-belt teacher annotator pool is documented [Q26, Q87]. — _Sources: Q26_
- **OC-2**: Potential disagreement risk is moderate: competitive-exam answer keys may diverge from school-board pedagogical framings of canonical literary content (e.g., Tulsidas treated as GK fact vs. literary-critical object) — the regional context flags this explicitly though no item-level evidence is published. The is_translated=True dominance in validation [DATASET-CRITICAL1] introduces an additional translation-quality risk to ground-truth labels. — _Sources: DATASET-CRITICAL1_
- **OC-3**: The paper provides no annotator demographic breakdown — no information on regional backgrounds, Hindi proficiency, or familiarity with Hindi state-board curricula. AI4Bharat institutional base is IIT Madras (Chennai, South India) [Q10]. INSUFFICIENT DOCUMENTATION for full assessment. — _Sources: Q10, Q26, Q87_
- **OC-4**: Re-annotation by representative North Indian Hindi-belt teacher pool would address translation-derived label uncertainty and competitive-vs-school-board framing differences; not currently documented.
- **OC-5**: INSUFFICIENT DOCUMENTATION on aggregation methods — paper does not describe how multiple annotator judgments are reconciled; primary trust is delegated to source-portal subject experts [Q26]. — _Sources: Q26_
- **OC-6**: Documented label issues: (a) no annotator demographic breakdown [Q26, Q87]; (b) institutional geographic asymmetry (IIT Madras base vs. North Indian deployment) [Q10]; (c) 25% paper-reported and apparently 100% in-validation translated content [Q47, DATASET-CRITICAL1] introduces translation-derived label provenance risk; (d) functionally unanswerable items with ostensibly correct targets [DATASET-MAJOR1]. — _Sources: Q26, Q87, Q10, Q47, DATASET-CRITICAL1, DATASET-MAJOR1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q26] 'These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers.' (p.3)
- [Q87] 'We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits.' (p.9)
- [Q10] 'Nilekani Centre at AI4Bharat, Indian Institute of Technology, Madras, IBM Research, India' (p.1)
- [Q47] 'Of the total 79K questions, only 25% of questions are translated from English' (p.4)

*Dataset analysis:*
- DATASET-CRITICAL1: All 245 sampled validation items flagged is_translated=True — the calibration corpus's ground-truth labels are GPT-4O-translation-derived rather than organically Hindi-sourced.
- DATASET-MAJOR1: ~14/245 items have correct targets but stems are functionally incomplete, making target-correctness unverifiable from the item content alone.
- DATASET-D43: Example 127 IPC effective year — competitive-exam factual key (target=1862) — a representative case of competitive-exam answer-key style.

</details>

**Information gaps:**
- Annotator demographic breakdown (regional background, Hindi proficiency, board-curriculum familiarity).
- Whether translated items' answer keys were re-verified by Hindi-proficient annotators after GPT-4O translation.
- Aggregation method when multiple annotators disagree.

**Requires expert verification:**
- Hindi-belt board-curriculum teacher review of a sample of MILU answer keys for regional concordance.
- Independent Hindi linguist verification of translated items' answer-key fidelity.

---

### Output Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
Output form is fully aligned with the deployment's binary correct/incorrect scoring requirement. MILU evaluates via accuracy on closed-set MCQ outputs [Q22, Q55] using log-likelihood selection for non-API models [Q52, Q53, Q54, Q55] and structured JSON for API models [Q57]. The deployment requires identical binary correct/incorrect signal per elicitation Q2; no modality, representation, or scoring-form mismatch exists. The deployment is text-only Devanagari with no TTS or speech-output requirements, and the postgraduate-teacher cohort is fully literate. The paper acknowledges log-likelihood vs. generation-based methods may differ [Q85], a minor methodological caveat but not a form mismatch.

**Strengths:**
- Binary correct/incorrect output scoring matches deployment exactly [Q22, Q55, elicitation Q2].
- Closed-set 4-option label space requires no free-form interpretation [Q33].
- Per-language, per-subject accuracy reporting [Q99–Q132] enables Hindi-specific deployment evaluation.
- Text-only output suits Devanagari Hindi-medium teacher use case [Q34, elicitation Q1].
- Postgraduate-teacher cohort is effectively 100% literate, removing accessibility constraints [WEB-1, WEB-2].

**Checklist:**

- **OF-1**: Expected output modality (binary correct/incorrect MCQ accuracy) matches deployment exactly [Q22, Q55, elicitation Q2]. — _Sources: Q22, Q55_
- **OF-2**: Not applicable — no speech output is required for this deployment (text-only Devanagari MCQ assessment).
- **OF-3**: Postgraduate-teacher cohort is by definition fully literate in Hindi [WEB-1, WEB-2 contextual]; no accessibility gap for text-output form. — _Sources: WEB-1, WEB-2_
- **OF-4**: No form mismatch documented. Minor caveat: paper acknowledges log-likelihood evaluation may yield different results from generation/CoT [Q85] — relevant for deployment if the deployed LLM uses generation-based answering, but not a fundamental form mismatch. — _Sources: Q85_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs)' (p.3)
- [Q52] 'For non-API-based models, we use the LM-EVALUATION-HARNESS' (p.5)
- [Q55] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability' (p.5)
- [Q57] 'We explicitly prompt these models to generate the correct response in a structured JSON format' (p.5)
- [Q85] 'our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods' (p.9)

*Web sources:*
- [WEB-1] 2011 census general literacy figures contextualize cohort literacy assumptions; postgraduate teacher cohort effectively 100% literate.
- [WEB-2] NSO PLFS 2023-24 literacy improvements support the literacy assumption.

</details>

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Validation split appears to be 100% translated rather than the paper-reported 25%; canonical Hindi-board literary figures absent from sampled items; ~6%+ items have truncated, functionally unanswerable stems.

**Recommendation:** Before deployment use, audit MILU's full Hindi item set for is_translated distribution, filter or repair truncated-stem items, and supplement with a Hindi-board-aligned MCQ set covering Tulsidas, Premchand, Kabir, Mahadevi Verma, Prasad, Nirala, and Dinkar. Engage a Hindi-board curriculum specialist to score this supplementation.

### Input Content ⚠

**Gap:** No per-state breakdown of Hindi-belt exam contributions (UPPSC, MPPSC, RPSC, BPSC) is published; Hindi-belt regional content is sparse relative to South Indian/Eastern content in sampled items.

**Recommendation:** Request per-state metadata from the MILU authors or directly partition the dataset by source-exam tags if available. Re-balance evaluation by stratifying or up-sampling Hindi-belt-specific items for deployment-relevant accuracy reporting.

### Output Content ⚠

**Gap:** No annotator demographic breakdown; institutional base is in South India; translated items' answer keys are GPT-4O-derived without documented Hindi-proficient human re-verification.

**Recommendation:** Recruit a North Indian Hindi-belt teacher annotator pool to re-verify ground-truth labels on a stratified sample (especially translated items and items touching canonical literature); document inter-annotator agreement with the original keys before relying on MILU accuracy figures.

### Input Form

**Gap:** Pervasive truncated/incomplete question stems (≥6% in sampled validation split) systematically depress measured accuracy in ways unrelated to language or cultural competence.

**Recommendation:** Run an automated audit detecting items where answer options reference numbered/lettered content not present in the question stem; either repair these items by recovering the missing content or exclude them from the deployment-relevant evaluation set.

### Input Ontology

**Gap:** The 41-subject taxonomy was derived from competitive-exam tags and does not separately resolve school-board sub-categories (Hindi literature, regional history, state civics).

**Recommendation:** Construct a post-hoc mapping from MILU's 41 subjects to UP/MP/RBSE/BSEB/CBSE syllabus topics with a Hindi-board curriculum specialist; report deployment-relevant accuracy on this re-mapped taxonomy rather than MILU's native one.

### Input Ontology

**Gap:** Inclusion of UPSC-Mains-style ethics scenarios, English-vocabulary items in Hindi wrappers, and Engineering/Health subjects introduces construct-irrelevant variance for school-board MCQ teacher assessment.

**Recommendation:** Filter out construct-irrelevant subject categories and item types (English-vocabulary wrappers, civil-servant ethics scenarios, time-stamped current-affairs items) when computing deployment-relevant accuracy; report deployment-filtered scores alongside native MILU scores.

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
| WEB-1 | https://scroll.in/article/825780/bihar-uttar-pradesh-rajasthan-and-madhya-pradesh-have-worst-literacy-rates-school-outcomes |
| WEB-2 | https://www.findeasy.in/indian-states-by-literacy-rate/ |
| WEB-3 | https://muftinternet.com/blog/usage-statistics-internet-and-mobile-users-in-india-2025/ |
| WEB-4 | https://en.wikipedia.org/wiki/Internet_in_India |
| WEB-5 | https://www.idreameducation.org/blog/post-nep-ncert-changes/ |
| WEB-6 | https://www.drishtiias.com/state-pcs/mppsc-exam-pattern |
| WEB-7 | https://arxiv.org/html/2501.13912v1 |
| WEB-8 | https://github.com/AI4Bharat/MILU |
| WEB-9 | https://arxiv.org/abs/2411.02538 |
| WEB-10 | https://www.sanskritiias.com/bpsc/syllabus/bpsc-exam-pattern-and-syllabus |
| WEB-11 | https://arxiv.org/abs/2501.15747 |
| WEB-12 | https://en.wikipedia.org/wiki/National_Education_Policy_2020 |
| WEB-13 | https://arxiv.org/html/2508.19831v1 |
| WEB-14 | https://huggingface.co/datasets/ai4bharat/MILU |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Hindi configuration)
**Analysis date:** 2025-08-04
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Dimension |
|----|---------|-----------|-------|---------|-----------|
| D1 | MILU/Hindi | All 245 | is_translated=True | Every sampled example has `is_translated: True` | IC |
| D2 | MILU/Hindi | Ex. 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं।" (Arts & Humanities / Literature and Linguistics) | IC |
| D3 | MILU/Hindi | Ex. 76 | option2 | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" (Arts & Humanities / Language Studies) | IC |
| D4 | MILU/Hindi | Ex. 90 | option3 | "शब्द 'grim' का पर्यायवाची लिखें।" (Arts & Humanities / Language Studies) | IC |
| D5 | MILU/Hindi | Ex. 105 | option4 | "निर्देश: निम्नलिखित प्रश्न में...दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है... Evangelize" (Arts & Humanities / Language Studies) | IC |
| D6 | MILU/Hindi | Ex. 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" (Arts & Humanities / Language Studies) | IC, OO |
| D7 | MILU/Hindi | Ex. 51 | option2 | "दिए गए वाक्य का सही सक्रिय रूप चुनें। सभी को उसके शानदार नृत्य प्रदर्शन ने मोहित कर दिया।" (Arts & Humanities / Language Studies) | IC |
| D8 | MILU/Hindi | Ex. 97 | option3 | "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है।" (postposition grammar; Language Studies) | IC |
| D9 | MILU/Hindi | Ex. 195 | option4 | "निर्देश: उस खंड की पहचान करें जिसमें व्याकरण संबंधी त्रुटि है... 'के शासन द्वारा'" | IC |
| D10 | MILU/Hindi | Ex. 118 | option2 | "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें." [question text for the idiom is absent] | IC, IF |
| D11 | MILU/Hindi | Ex. 152 | option1 | "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए सबसे उपयुक्त विकल्प चुनें." [underlined segment missing] | IC, IF |
| D12 | MILU/Hindi | Ex. 56 | option2 | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें..." [statements 1-4 not present in question text] | IC, IF |
| D13 | MILU/Hindi | Ex. 69 | option2 | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल, (b) केवल, (c) केवल" [referents a,b,c,d absent] | IC, IF |
| D14 | MILU/Hindi | Ex. 86 | option2 | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक...राज्यों A,B,C,D,E..." [states not named] | IC, IF |
| D15 | MILU/Hindi | Ex. 94 | option4 | "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? (a), (b), (c), (d)" [reactions not listed] | IC, IF |
| D16 | MILU/Hindi | Ex. 106 | option2 | "निम्नलिखित पदार्थों को...कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4" [substances not named] | IC, IF |
| D17 | MILU/Hindi | Ex. 143 | option4 | "निम्नलिखित शब्दों को तार्किक और अर्थपूर्ण क्रम में व्यवस्थित करने के लिए सही विकल्प चुनें." [words absent] | IC, IF |
| D18 | MILU/Hindi | Ex. 95 | option1 | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है. वाक्य A और F स्थिर हैं." [sentences not present] | IC, IF |
| D19 | MILU/Hindi | Ex. 151 | option1 | "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं...कौन सा तर्क मजबूत है?" [statement/arguments absent] | IC, IF |
| D20 | MILU/Hindi | Ex. 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" (Arts & Humanities / History — Mughal historiography) | IC |
| D21 | MILU/Hindi | Ex. 52 | option2 | "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था" (Arts & Humanities / History — South Indian history) | IC |
| D22 | MILU/Hindi | Ex. 48 | option3 | "भांड पाथेर थिएटर मुख्य रूप से भारत के निम्नलिखित में से किस राज्य/केंद्र शासित प्रदेश की परंपरा है?" (Arts & Humanities / Arts and Culture — Jammu & Kashmir) | IC |
| D23 | MILU/Hindi | Ex. 108 | option3 | "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" (Arts & Humanities / Literature and Linguistics — Tamil-specific) | IC |
| D24 | MILU/Hindi | Ex. 232 | option2 | "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है?" (Arts & Humanities / Literature and Linguistics — Tamil classic) | IC |
| D25 | MILU/Hindi | Ex. 126 | option3 | "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" (Arts & Humanities / Literature and Linguistics — Telugu/Telangana-specific) | IC |
| D26 | MILU/Hindi | Ex. 193 | option3 | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" (Arts & Humanities / Arts and Culture — Rajasthan-specific) | IC |
| D27 | MILU/Hindi | Ex. 198 | option2 | "'बस्तर का स्वतंत्रता संग्राम' भी कहा जाता है?" (Arts & Humanities / History — Chhattisgarh-specific) | IC |
| D28 | MILU/Hindi | Ex. 68 | option2 | "राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है?" (Geography — Rajasthan-specific) | IC |
| D29 | MILU/Hindi | Ex. 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" (Geography — UP-specific) | IC |
| D30 | MILU/Hindi | Ex. 242 | option4 | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है...चिकनकारी" (Arts & Humanities / Arts and Culture — UP-specific) | IC |
| D31 | MILU/Hindi | Ex. 115 | option4 | "किस लेखक ने...किस्सा किस्सा लखनऊवा-लखनऊ के आवामी किस्से के लिए साहित्य अकादमी युवा पुरस्कार 2021 जीता?" (Literature — recent award) | IC |
| D32 | MILU/Hindi | Ex. 64 | option3 | "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है?" (History — national patriotic figure) | IC |
| D33 | MILU/Hindi | Ex. 83 | option1 | "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम..." (Sociology — ethics scenario) | IC, OO |
| D34 | MILU/Hindi | Ex. 142 | option1 | "क्या तेलंगाना सरकार को सभी को मुफ्त शिक्षा प्रदान करनी चाहिए?" (Education — argumentation item) | IC |
| D35 | MILU/Hindi | Ex. 188 | option3 | "नई शिक्षा नीति 2020 में देखा गया है..." [problems (a)(b) not stated] | IC, IF |
| D36 | MILU/Hindi | Ex. 122 | option4 | "प्रधानमंत्री मुद्रा योजना (PMMY) के बारे में निम्नलिखित में से कौन सा कथन सही है? न तो 1 और न ही 2 / दोनों 1 और 2..." [statements 1 and 2 absent] | IC, IF |
| D37 | MILU/Hindi | Ex. 157 | option4 | "पद्म पुरस्कार 2021 के संदर्भ में निम्नलिखित कथनों पर विचार करें. 1...2...3..." (multi-statement item — complete in question) | IC |
| D38 | MILU/Hindi | Ex. 201 | option4 | "BIOS के संदर्भ में निम्नलिखित में से कौन सा कथन सही है? केवल I और II / केवल I और III..." [statements I, II, III absent] | IC, IF |
| D39 | MILU/Hindi | Ex. 222 | option2 | "2022 में फॉर्च्यून 500 सूची में भारतीय कंपनियों के संबंध में निम्नलिखित पर विचार करें: A, B, C, D, E केवल..." [items A-E absent] | IC, IF |
| D40 | MILU/Hindi | Ex. 74 | option4 | "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी?" (Economics — time-stamped current affairs) | IC |
| D41 | MILU/Hindi | Ex. 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022..." (Sports and Recreation — time-stamped current affairs) | IC |
| D42 | MILU/Hindi | Ex. 132 | option4 | "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं?" (Politics — time-stamped) | IC |
| D43 | MILU/Hindi | Ex. 127 | option2 | "भारतीय दंड संहिता किस वर्ष प्रभावी हुई? (target: option2 = 1862)" (Law and Ethics — factual) | OC |

---

### Findings

#### CRITICAL

#### Finding CRITICAL1: All 245 sampled validation examples are marked `is_translated: True` — the translated proportion appears to dominate or constitute the entire validation split

- **Dimension(s):** IC, IF
- **Observation:** Every single one of the 245 sampled examples carries `is_translated: True`. The published paper reports that only ~25% of the released 79K questions are translated from English [Q47], which would predict a minority of translated items in any representative sample. Yet no item in this 245-item sample has `is_translated: False`. This may indicate that the validation split was specifically constructed from translated items (as opposed to the test split which may contain the organically sourced majority), or that the `is_translated` flag has a different semantics than expected.
- **Potential concern for deployment:** If the validation split consists entirely of translated items, few-shot examples drawn from this split (as MILU intends [Q51]) will always be translated-origin content. For the Hindi-medium teacher deployment, this means that in-context examples used to calibrate LLM performance will never reflect organically sourced Hindi-exam register. Translated items may carry GPT-4O translation artifacts — formal but potentially non-idiomatic Khari Boli — and may not match the register of school-board or state-exam question papers. The entire few-shot calibration corpus would then be drawn from a systematically different distribution than the test corpus.
- **Datapoint citations:**
  - [D1] All 245 examples (MILU/Hindi, split=validation): `is_translated: True` on every row — if this is representative of the split, the validation set is 100% translated-origin, sharply at odds with the paper's reported 25% translated figure for the full dataset.

---

#### MAJOR

#### Finding MAJOR1: Pervasive truncated/incomplete question stems — answer options refer to absent content

- **Dimension(s):** IC, IF
- **Observation:** A substantial number of questions in the sample are self-evidently incomplete: the question stem references numbered statements, lettered items, underlined text, or a list of substances/reactions that are not present in the `question` field. Affected examples include at minimum: Ex. 56 (four statements about ethanol not provided), Ex. 69 (substances (a)–(d) absent), Ex. 86 (states A–E not named), Ex. 94 (reactions (a)–(d) not listed), Ex. 95 (sentences B–E absent), Ex. 106 (substances 1–4 not listed), Ex. 118 (idiom text missing), Ex. 122 (statements 1 and 2 absent), Ex. 143 (words to be arranged absent), Ex. 151 (statement and arguments absent), Ex. 152 (underlined segment missing), Ex. 188 (NEP problems (a)(b) absent), Ex. 201 (BIOS statements I–III absent), Ex. 222 (Fortune 500 items A–E absent).
- **Potential concern for deployment:** These items cannot be answered from the `question` field alone. If an LLM is evaluated on these items using only the structured fields provided, it must guess among four options without the necessary referent content — systematically degrading accuracy scores for no construct-valid reason. For the North Indian teacher deployment, where MILU is being assessed as a benchmark for Hindi-medium MCQ evaluation, this data quality issue means a non-trivial fraction of Hindi items are functionally unanswerable and will depress measured accuracy in ways unrelated to language or cultural competence. The fraction of affected items in the validation split appears substantial (at least 14/245 = ~6% confirmed from the sample, likely higher).
- **Datapoint citations:**
  - [D12] Example 56 (MILU/Hindi, split=validation, label=option2): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें और दिए गए विकल्पों में से सही उत्तर चुनें:" — answer options reference statements 1–4 that are not present in the question field.
  - [D13] Example 69 (MILU/Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल, (b) केवल, (c) केवल" — substances (a)–(d) not provided.
  - [D14] Example 86 (MILU/Hindi, split=validation, label=option2): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, C..." — states A–E not identified.
  - [D15] Example 94 (MILU/Hindi, split=validation, label=option4): "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं?" — reactions (a)–(d) absent.
  - [D16] Example 106 (MILU/Hindi, split=validation, label=option2): "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4" — substances 1–4 not named.
  - [D10] Example 118 (MILU/Hindi, split=validation, label=option2): "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें." — the idiom itself is absent.
  - [D11] Example 152 (MILU/Hindi, split=validation, label=option1): "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए सबसे उपयुक्त विकल्प चुनें." — underlined segment not present.
  - [D18] Example 95 (MILU/Hindi, split=validation, label=option1): "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है. वाक्य A और F स्थिर हैं." — sentences not provided.
  - [D19] Example 151 (MILU/Hindi, split=validation, label=option1): "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं...कौन सा तर्क मजबूत है?" — statement and arguments I/II absent.
  - [D35] Example 188 (MILU/Hindi, split=validation, label=option3): "नई शिक्षा नीति 2020 में देखा गया है कि भारत में उच्च शिक्षा प्रणाली निम्नलिखित में से किन समस्याओं का सामना कर रही है? केवल (a) / केवल (b)..." — problems (a)/(b) not stated.
  - [D36] Example 122 (MILU/Hindi, split=validation, label=option4): "प्रधानमंत्री मुद्रा योजना (PMMY) के बारे में निम्नलिखित में से कौन सा कथन सही है? न तो 1 और न ही 2..." — statements 1 and 2 absent.
  - [D38] Example 201 (MILU/Hindi, split=validation, label=option4): "BIOS के संदर्भ में निम्नलिखित में से कौन सा कथन सही है? केवल I और II..." — statements I, II, III absent.
  - [D39] Example 222 (MILU/Hindi, split=validation, label=option2): "2022 में फॉर्च्यून 500 सूची में भारतीय कंपनियों के संबंध में निम्नलिखित पर विचार करें: A, B, C, D, E केवल..." — companies A–E not named.

---

#### Finding MAJOR2: Hindi Arts & Humanities items do not include canonical North Indian literary content (Tulsidas, Premchand, Kabir, Mahadevi Verma)

- **Dimension(s):** IC, IO
- **Observation:** Across 245 sampled Hindi validation items, Arts & Humanities / Literature and Linguistics questions reference Kashmiri poets (Ex. 98: "कश्मीर का जॉन कीट्स"), Tamil classics (Ex. 108: Subramanya Bharati; Ex. 232: Silappatikaram/Ilango Adigal), Telugu literary works (Ex. 126: Telangana Rastrodayamalu), Sindhi writers (Ex. 179: Sahitya Akademi), and William Wordsworth (Ex. 7). No sampled item references Tulsidas, Premchand, Kabir, Mahadevi Verma, Jaishankar Prasad, Nirala, or Dinkar — the canonical Hindi-board literary figures listed as high-priority for the deployment. The History items reference Mughal historiography (Ex. 25: Masir-e-Alamgiri), Pandya kings (Ex. 52), Indus Valley (Ex. 237), and Asoka (Ex. 158), but not figures specifically canonical to North Indian state-board Hindi literature curricula.
- **Potential concern for deployment:** The deployment requires assessment of student responses to MCQs covering canonical Hindi literature as taught in UP, MP, Bihar, and Rajasthan boards. If Hindi Literature and Linguistics items are drawn from competitive-exam general-knowledge framings featuring South Indian, Kashmiri, or international literary figures rather than the canonical Hindi-board authors, the benchmark will not measure what North Indian teachers actually test their students on. This directly instantiates the highest-priority IC gap identified in the coverage gap analysis.
- **Datapoint citations:**
  - [D2] Example 7 (Arts & Humanities / Literature and Linguistics, label=option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं।" — a UK Romantic poet, not part of Hindi board syllabus; no equivalent item found for Tulsidas or Premchand.
  - [D23] Example 108 (Arts & Humanities / Literature and Linguistics, label=option3): "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" — Tamil literary history, not North Indian board Hindi literature.
  - [D24] Example 232 (Arts & Humanities / Literature and Linguistics, label=option2): "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है?" — Tamil classic literature.
  - [D25] Example 126 (Arts & Humanities / Literature and Linguistics, label=option3): "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" — Telugu/Telangana literary topic.
  - [D20] Example 25 (Arts & Humanities / History, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" — Mughal court historiography, competitive-exam framing rather than school-board Hindi literature perspective.

---

#### Finding MAJOR3: English-vocabulary Language Studies items in a Hindi-language benchmark

- **Dimension(s):** IC, IF
- **Observation:** Multiple Language Studies items in the Hindi benchmark ask about English vocabulary or English grammar in a Hindi-translated wrapping: Ex. 76 asks the meaning of 'didactic' in English; Ex. 90 asks for the synonym of 'grim'; Ex. 105 asks the Hindi meaning of 'Evangelize'; Ex. 3 (implicitly) tests English grammar concepts (active/passive voice in Hindi phrasing). These items appear to be translated from English-language verbal-ability competitive-exam questions (SSC, banking exams) where the original task was English vocabulary proficiency, not Hindi language competence.
- **Potential concern for deployment:** North Indian Hindi-medium teachers assess students on Hindi grammar, Hindi literature, and sometimes Sanskrit-origin vocabulary — not on English synonym/antonym or English word definition tasks. Items that test knowledge of English vocabulary words (grim, didactic, evangelize) within the Hindi benchmark do not align with Hindi-medium state-board curricula. A model performing well on these items would be demonstrating English vocabulary knowledge accessed through Hindi translation, not Hindi-medium linguistic competence. This conflation may inflate or distort benchmark scores in ways irrelevant to the deployment context.
- **Datapoint citations:**
  - [D3] Example 76 (Arts & Humanities / Language Studies, label=option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" — Hindi item asking meaning of the English word 'didactic.'
  - [D4] Example 90 (Arts & Humanities / Language Studies, label=option3): "शब्द 'grim' का पर्यायवाची लिखें." — Hindi item asking for synonym of the English word 'grim.'
  - [D5] Example 105 (Arts & Humanities / Language Studies, label=option4): "निर्देश:...दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है और उसके अनुरूप बटन पर क्लिक करें। Evangelize" — Hindi item asking Hindi translation of English 'Evangelize.'

---

#### Finding MAJOR4: Competitive-exam IAS/civil-services framing dominates Social Sciences and Ethics items; school-board register absent

- **Dimension(s):** IC
- **Observation:** The one Ethics/Governance scenario item in the sample (Ex. 83) presents a complex multi-paragraph real-world dilemma cast explicitly from the perspective of "एक वरिष्ठ सिविल अधिकारी" (a senior civil servant) deciding how to respond to tribal displacement by an old-age home. This is textbook UPSC Mains Ethics, Paper IV framing — far from any school-board MCQ context. Similarly, Ex. 142 asks students to evaluate arguments about whether the Telangana government should provide free education to all, a policy-reasoning format typical of state PCS exams but foreign to UP Board Class 10–12 MCQ contexts.
- **Potential concern for deployment:** State-board teachers at the secondary level assess students on factual civics, basic constitutional law, and social science MCQs — not on complex IAS-style ethical reasoning scenarios or multi-paragraph argument evaluation. The presence of such items in the Hindi benchmark means a deployed LLM calibrated on MILU may be optimized for competitive-exam reasoning patterns that teachers in the deployment context never need to evaluate.
- **Datapoint citations:**
  - [D33] Example 83 (Social Sciences / Sociology, label=option1): "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है..." — 4-option scenario question in UPSC Ethics Paper IV register.
  - [D34] Example 142 (Arts & Humanities / Education, label=option1): "क्या तेलंगाना सरकार को सभी को मुफ्त शिक्षा प्रदान करनी चाहिए? तर्क: A: हाँ... B: नहीं..." — argument-strength evaluation item typical of state PCS prelims, not school-board MCQs.

---

#### Finding MAJOR5: Strong South India / non-Hindi-belt regional content bias in Arts & Humanities and Geography

- **Dimension(s):** IC, IO
- **Observation:** A disproportionate share of regionally specific content in the sample is drawn from South India, Eastern India, or states outside the Hindi belt. Arts & Culture items reference: Bhānd Pather theatre (Jammu & Kashmir, Ex. 48), Kota painting school (Rajasthan, Ex. 193 — one of the few Hindi-belt items), Tamil magazine cartoons (Ex. 108), Silappatikaram (Tamil, Ex. 232), Telangana literature (Ex. 126). History items feature Pandya kingdom (Ex. 52), Bastar rebellion/Chhattisgarh (Ex. 198). Geography features Manipur's Imphal Basin (Ex. 186), Jharkhand river origins (Ex. 107). UP/MP/Bihar/Rajasthan-specific content is rare: only Ex. 26 (UP minerals), Ex. 68 (Rajasthan reserved area), Ex. 242 (UP chikankari embroidery) are clearly Hindi-belt specific in this sample.
- **Potential concern for deployment:** The deployment targets North Indian Hindi-belt teachers whose students are assessed on UP/MP/Bihar/Rajasthan regional history, geography, and culture. The apparent under-representation of Hindi-belt regional content and over-representation

