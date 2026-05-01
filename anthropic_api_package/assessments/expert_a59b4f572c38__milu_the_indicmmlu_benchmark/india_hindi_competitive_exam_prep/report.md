## Deployment Context

**Use case:** Deployment scenario: A Hindi-speaking student in India is testing his/her preparation for competitive job-related examinations, with an AI system providing feedback on their responses. The goal is to evaluate the applicability of the benchmark and the quality of the LLM’s feedback.

Domain: Educational assessment
Setting: Mobile application / enterprise software

Note: The deployment hypothesis should be tested using Hindi-language sentences from the benchmark, as I am familiar with the language and can provide evaluation in a subsequent stage.
**Target population:** A graduate student in North India interacting in the Hindi language. The student has completed their education primarily in Hindi, with limited exposure to English.

# Validity Analysis: milu
**Target context:** Hindi-Medium Competitive Exam Aspirants — North India (Central Exams)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 3 | Moderate gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content | 2 | Significant gaps | medium |
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

MILU is the most relevant publicly available benchmark for Indic-language knowledge evaluation and provides genuine value for a portion of this deployment's needs — particularly for measuring MCQ-level accuracy on Indian Polity, History, Geography, and Economics in Hindi. Its India-first design [Q11], real-exam sourcing [Q24, Q25], and 41-subject taxonomy [Q42] are well-suited to a central-exam preparation context in principle. However, two structural issues sharply limit its validity for THIS deployment: (1) Output form/ontology mismatch (Output Ontology=1, Output Form=1) — MILU evaluates only MCQ option selection, while the deployment requires open-ended Hindi explanatory rationales; this is a fundamental scope gap acknowledged by the paper itself [Q85] and confirmed by data inspection (DATASET-D1, D9). (2) Hindi partition content concerns (Input Content=2) — dataset analysis found 100% is_translated=True in the 26-item Hindi validation sample (DATASET-D13), heavy Engineering/Tech skew misaligned with UPSC/SSC syllabi (DATASET-D5/D6/D7/D16/D36), Current Affairs staleness (DATASET-D4/D25/D33), and pervasive cross-language item duplication. Input form (4) is the strongest dimension; output ontology and output form are the weakest. The benchmark can serve as a partial accuracy probe for a subset of priority subjects but cannot validate the deployment's core output.

## Practical Guidance

### What This Benchmark Measures

MILU measures MCQ-label accuracy on Hindi-language Indian-domain knowledge across 8 macro-domains and 41 subjects. For this deployment, it provides moderate evidence for a model's ability to produce correct verdicts on UPSC/SSC-style Polity, History, Geography, and Economics MCQs in Hindi (Input Ontology partial coverage, Input Form strong, Input Content partial). It offers no evidence on the deployment's core output: the Hindi explanatory rationale (Output Ontology and Output Form both score 1).

### Construct Depth

Construct depth is shallow for this deployment. MILU probes whether a model can rank the correct option among up to four — a necessary but far-from-sufficient signal for exam-feedback quality. It does not probe pedagogical clarity, factual rationale accuracy, fluency, register appropriateness, or robustness to authentic Hindi-medium exam phrasing. Combined with cross-language duplication, possible high translation rate in Hindi, and Current Affairs staleness, even the verdict-accuracy signal is partially construct-irrelevant for 2025–26 central-exam readiness.

### What Else You Need

Three supplementations are essential: (1) A custom Hindi-language rationale-quality evaluation framework with rubric covering factual accuracy, fluency, pedagogical clarity, and register — no public resource exists [WEB-13, WEB-14]. (2) A central-exam-specific subset of MILU filtered to UPSC/SSC/banking items with explicit Mathematics/Reasoning and Current Affairs categories, ideally drawing on natively authored Hindi items rather than translated content. (3) A current-affairs evaluation set refreshed annually with 2024–2026 events to address staleness.

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
MILU's 8 macro-domain / 41-subject taxonomy [Q42] aligns partially with central-exam priority subjects: Social Sciences and Law & Governance map to History/Polity, while Arts & Humanities covers cultural GK. However, the taxonomy does not separately enumerate Mathematics/Reasoning or Current Affairs as named categories — both heavily weighted in UPSC CSAT and SSC CGL Tier 1 [WEB-9, WEB-10, WEB-15]. Dataset analysis confirms reasoning and quantitative items exist (in the English partition: D8, D9), but the Hindi sample shows a heavy skew toward translated Engineering & Tech items (DC motor, half-wave rectifier, transformer, AM bandwidth, Fortran 77) that are peripheral to UPSC GS / SSC GA syllabi. State-level and central-level items are pooled without metadata distinguishing them [Q27], making it impossible to filter for central-exam scope (D24, D27).

**Strengths:**
- Explicit India-first design covering Science, Social Sciences, Humanities, Arts, Business Studies, Law [Q23, Q74] aligns with multi-domain GK breadth required for UPSC/SSC.
- Hierarchical 8-domain × 41-subject structure [Q42] supports per-subject performance analysis relevant to syllabus mapping.
- Reasoning and quantitative aptitude content is present in MILU's taxonomy, confirmed empirically in the English partition (DATASET-D8, D9).

**Checklist:**

- **IO-1**: For central-exam aspirants (UPSC/SSC/banking), priority categories are GK, Current Affairs, History, Polity, Mathematics/Reasoning, Hindi proficiency, Geography, Economics (elicitation Q1; [WEB-9, WEB-10, WEB-15]). — _Sources: WEB-9, WEB-10, WEB-15_
- **IO-2**: Mathematics/Reasoning and Current Affairs are not named as MILU macro-domains [Q42]; they may be subsumed under other domains but lack explicit enumeration. Dataset findings confirm reasoning/quant items exist in the English partition (DATASET-D8, D9) but not whether the Hindi partition has comparable representation. State-level vs. central-exam labeling is absent (DATASET-D24, D27). — _Sources: Q42, DATASET-D8, DATASET-D9, DATASET-D24, DATASET-D27_
- **IO-3**: MILU pools state-PSC and central-exam items [Q27, Q92] and the observed Hindi sample contains low-priority Engineering/Tech and niche CS items (Fortran 77, AM bandwidth) that are construct-irrelevant for UPSC/SSC GS (DATASET-D5, D6, D7, D16, D36). — _Sources: Q27, DATASET-D5, DATASET-D6, DATASET-D7, DATASET-D16, DATASET-D36_
- **IO-4**: Two notable gaps: (a) absence of explicit Current Affairs and Mathematics/Reasoning macro-domains hampers syllabus-aligned scoring; (b) inability to separate central-exam from state-PSC items at the metadata level injects construct-irrelevant variance for this deployment. — _Sources: Q42, Q27, DATASET-D24_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q42] 'Following the manual merging of related clusters, we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies.' (p.4)
- [Q23] 'This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others.' (p.3)
- [Q27] 'Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years.' (p.3)
- [Q74] 'we introduced MILU—Multilingual Indic Language Understanding Benchmark-a comprehensive benchmark specifically designed to evaluate LLMs across 11 Indic languages, spanning diverse domains and culturally relevant subjects.' (p.8)

*Web sources:*
- [WEB-9] UPSC Prelims subject weightage — Current Affairs, Economy, History, Geography, Polity, Environment each 10–25 questions/year
- [WEB-10] SSC CGL Tier 1 covers Reasoning, General Awareness, Quantitative Aptitude, English Comprehension
- [WEB-15] UPSC CSAT Paper 2 covers Quantitative Aptitude and Logical Reasoning (qualifying)

*Dataset analysis:*
- DATASET-D8: Logical Reasoning analogy item present in English partition — confirms reasoning subject exists in MILU taxonomy
- DATASET-D9: Quantitative aptitude (compound interest) in English partition — confirms math subject coverage
- DATASET-D5/D6/D7/D16/D36: Hindi sample contains Engineering and niche CS items (Fortran 77, AM bandwidth) — peripheral to UPSC/SSC GS
- DATASET-D24: Maharashtra Legislative Committee question — state-level governance content not in central-exam scope
- DATASET-D27: MP industrial geography question — state-level content commingled with central-exam items

</details>

**Information gaps:**
- Proportion of MILU Hindi items aligned to UPSC/SSC/banking vs. state PSC is not published.
- Whether Mathematics/Reasoning and Current Affairs are present in the Hindi partition at central-exam syllabus weight is not quantifiable from the small validation sample.

**Requires expert verification:**
- A subject-matter expert in UPSC/SSC syllabus design should map MILU's 41 subjects to central-exam syllabus weights and quantify representation in the Hindi partition's test split.

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
MILU's stated design priorities — India-first sourcing, regional cultural content, sourcing from real exam papers [Q11, Q12, Q24, Q25] — are well aligned with the deployment's content needs. However, dataset analysis reveals two critical issues for the Hindi partition: (1) all 26 Hindi validation examples carry is_translated=True (DATASET-D13), suggesting the Hindi partition may contain a much higher translated proportion than the documented overall ~25% [Q47]; (2) cross-language item duplication is pervasive (DATASET-D14/D15/D29), reducing effective Hindi-specific content. North India sub-regional content is sparse in the observed Hindi sample (only DATASET-D3 on UP minerals). Current Affairs items are time-bounded to 2014–2022 events (DATASET-D4, D25, D33), creating staleness risk for 2025–26 exam cycles. While translated items use fluent Devanagari with low code-mixing (DATASET-D12, D21), the linguistic register may not match authentic Hindi-medium exam papers.

**Strengths:**
- Source content is real Indian competitive exam papers [Q24, Q25], grounding the input in authentic exam ecosystems.
- India-first design explicitly includes culturally relevant subjects — local history, arts, festivals, laws [Q12, Q2].
- Constitutional law, Mughal/medieval North Indian history, and Indian GK are present in Hindi (DATASET-D1, D2, D3, D11, D18) — directly relevant to UPSC/SSC content.
- Observed Hindi items use clean Devanagari with minimal English code-mixing (DATASET-D12, D21), respecting the deployment's ~10% ceiling.

**Checklist:**

- **IC-1**: Yes, deployment requires both pan-India GK and North India sub-regional knowledge (elicitation Q2). MILU partially addresses this — pan-India GK is well represented (DATASET-D1, D11, D18, D22), but North India sub-regional content (Chhath Puja, zamindari, North Indian freedom fighters) is sparse in observed Hindi sample (only DATASET-D3). — _Sources: Q11, Q12, DATASET-D1, DATASET-D2, DATASET-D3, DATASET-D11_
- **IC-2**: Cultural alignment is partially achieved through India-first sourcing [Q11, Q24], but the dominant translation path for the Hindi partition (DATASET-D13: 100% is_translated in sample) means linguistic-cultural register may not match Hindi-medium exam conventions. — _Sources: Q11, Q24, DATASET-D13_
- **IC-3**: No Western-specific content was observed; the benchmark is India-centric. However, translated engineering items (DATASET-D5, D6, D7, D36) inject construct-irrelevant content that mismatches central-exam syllabus. — _Sources: DATASET-D5, DATASET-D6, DATASET-D7, DATASET-D36_
- **IC-4**: INSUFFICIENT DOCUMENTATION — paper does not report whether annotators or reviewers were Hindi-medium graduates or domain experts familiar with central-exam content [Q87 mentions only 'AI4Bharat volunteers'].
- **IC-5**: Critical content issues: (a) probable over-representation of translated items in Hindi partition; (b) Current Affairs staleness (events 2014–2022 in a benchmark to be used for 2025–26 prep); (c) cross-language duplication (DATASET-D14/D15/D29) reducing genuine Hindi-source diversity; (d) sparse North India sub-regional items observed. — _Sources: Q44, Q47, DATASET-D13, DATASET-D14, DATASET-D15, DATASET-D29, DATASET-D4, DATASET-D25, WEB-9_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q11] 'We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams.' (p.2)
- [Q24] 'collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams' (p.3)
- [Q25] 'We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages.' (p.3)
- [Q44] 'For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O.' (p.4)
- [Q47] 'Of the total 79K questions, only 25% of questions are translated from English, with the remainder' (p.4)
- [Q12] 'These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science.' (p.2)

*Web sources:*
- [WEB-9] Current Affairs is heavily and variably weighted in UPSC GS Paper 1, raising staleness concerns for older exam scrapes

*Dataset analysis:*
- DATASET-D13: All 26 Hindi validation examples carry is_translated=True — sample suggests Hindi partition translation rate substantially exceeds the documented 25% overall average
- DATASET-D14/D15: Identical 1991 financial crisis question appears in English original and Hindi translation — confirms cross-language translation pipeline
- DATASET-D29: 44th Constitutional Amendment question appears identically across Hindi, Tamil, Malayalam — cross-language item duplication reduces Hindi-specific diversity
- DATASET-D3: UP minerals question — only observed North India sub-regional item in Hindi sample (1 of 26)
- DATASET-D4/D25/D33: Current Affairs items reference 2022 events — stale for 2025–26 exam cycles
- DATASET-D12/D21: Hindi items use clean Devanagari with minimal English intrusion — code-mixing within deployment ceiling
- DATASET-D1/D2/D11/D18: Substantive Polity, Mughal history, Geography, Arts GK content present in Hindi

</details>

**Information gaps:**
- True translation rate in the Hindi test split (vs. observed 100% in 26-item validation sample) is unknown.
- Proportion of MILU Hindi items aligned with central exams vs. state PSCs is undocumented.
- Item-level North India sub-regional content breakdown is not published.
- Annotator demographics — whether reviewers were Hindi-medium graduates familiar with the target student linguistic register — not reported.

**Requires expert verification:**
- A Hindi-medium UPSC/SSC subject-matter expert should review a stratified sample of MILU Hindi test items for: (a) authenticity of register vs. authentic Hindi-medium exam papers, (b) translation artifact rate, (c) syllabus alignment with central exams, (d) North India sub-regional content presence.

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
MILU is text-only with explicit exclusion of reading-comprehension passages, image-based items, and >4-option items [Q33], plus INDICLID + Unicode-based language filtering [Q34], duplicate removal [Q35], and multi-stage manual cleaning [Q31, Q32, Q36]. This matches the deployment's text-only mobile interface and standard Devanagari script with no RTL/capitalization concerns. Observed Hindi items render in standard Devanagari with minimal Roman intrusion (DATASET-D12, D21). One residual concern: dataset analysis observed at least two malformed items with truncated stems across language partitions (DATASET-D34, D35), suggesting filtering imperfections.

**Strengths:**
- Text-only MCQ format directly matches deployment input modality.
- Devanagari script handling is well-supported [Q34], no signal-distribution mismatch for Hindi.
- Multi-layer cleaning pipeline [Q31, Q32, Q36] reduces noise.
- Observed code-mixing in Hindi items remains below the ~10% ceiling (DATASET-D12, D21).

**Checklist:**

- **IF-1**: Signal distribution matches: text-only Devanagari [Q33, Q34] aligns with the deployment's mobile text interface. No image/audio modality mismatch. — _Sources: Q33, Q34, DATASET-D12, DATASET-D21_
- **IF-2**: Regional infrastructure (Android-dominant smartphones, Devanagari Unicode standard) supports text-only MCQ ingestion. Bandwidth-sensitive but format-compatible [WEB-6]. — _Sources: Q34, WEB-6_
- **IF-3**: Domain-specific form: MCQ-with-4-options matches central-exam Prelims pattern (UPSC, SSC, banking are MCQ-based). Reading-comprehension exclusion [Q33] removes one common exam format but is acceptable for the deployment's objective-prep scope. — _Sources: Q33_
- **IF-4**: Minor form mismatches: (a) some items have truncated stems suggesting reading-comprehension remnants (DATASET-D34, D35); (b) reading-comprehension exclusion means RC-style UPSC CSAT questions are not represented. — _Sources: Q33, DATASET-D34, DATASET-D35_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'During the collection process, we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q34] 'To remove incorrect language entries, we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering (Khan et al., 2024), ensuring that the questions are in the correct language.' (p.4)
- [Q31] 'we employ multiple layers of manual and automated cleaning filters.' (p.4)
- [Q35] 'we remove any duplicate questions to retain only the unique ones.' (p.4)

*Web sources:*
- [WEB-6] TRAI data shows internet penetration patchy in Bihar — relevant to deployment connectivity assumptions

*Dataset analysis:*
- DATASET-D12: Pure Devanagari Hindi item, no English code-mixing
- DATASET-D21: Hindi item with appropriate transliteration of loanwords (ओक/oak)
- DATASET-D34: English item with truncated stem ('The owner of the textile shop brought a') — filtering imperfection
- DATASET-D35: Malayalam item with truncated 'Directions:' stem — pattern repeats across languages

</details>

**Information gaps:**
- Frequency of malformed/truncated items in the full Hindi test split is unknown.

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
This is a fundamental mismatch. MILU's output ontology is a single MCQ label — one of up to four options [Q33, Q55] — and the dataset schema confirms only a 'target' field with no rationale or explanation field (DATASET-D1, D9). The deployment requires a correct/incorrect verdict PLUS a substantive Hindi-language explanatory rationale (elicitation Q3). MILU has no rubric, no label set, and no scoring function for rationale quality. The 41-subject taxonomy [Q42] supports per-subject accuracy reporting but cannot validate explanation quality. Compounding this, the benchmark itself reports models perform worst in Arts & Humanities, Social Sciences, and Law & Governance [Q6, Q20, Q62, Q71, Q77] — precisely the deployment's priority subjects (History, Polity, GK).

**Strengths:**
- 41-subject × 8-domain hierarchical taxonomy [Q42] supports per-subject diagnostic accuracy reporting, useful for identifying weak areas.
- Closed-form MCQ accuracy is unambiguous for the verdict portion of the deployment's required output.

**Checklist:**

- **OO-1**: MCQ option labels are regionally relevant only insofar as the questions are India-sourced [Q26]. The output category space is, however, structurally incomplete for this deployment. — _Sources: Q55_
- **OO-2**: Critical missing categories: rationale-quality dimensions (factual accuracy, fluency, pedagogical clarity, register appropriateness — listed in elicitation pedagogical_context). MILU has none of these. — _Sources: Q33, DATASET-D1, DATASET-D9, WEB-14_
- **OO-3**: MCQ-only ontology does not encode non-regional values per se, but encodes an evaluation philosophy (option-selection only) that is misaligned with pedagogical-feedback deployments. — _Sources: Q55_
- **OO-4**: Significant taxonomy redesign is required: a separate rationale-quality rubric must be developed, as MILU provides no foundation. The 2025 Hindi LLM benchmarking preprint [WEB-14] confirms no such Hindi rubric exists publicly. — _Sources: WEB-13, WEB-14_
- **OO-5**: MILU's MCQ-only output ontology violates structural validity for this deployment (the construct of pedagogical feedback has internal structure — verdict + rationale — that MILU cannot represent) and content validity (rationale-quality categories are entirely absent). — _Sources: Q33, Q42, Q6, Q71, DATASET-D1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q55] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability' (p.5)
- [Q42] 'we determine 41 distinct subject names, which fall into eight main domains' (p.4)
- [Q6] 'Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM.' (p.1)
- [Q71] 'open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields.' (p.7)

*Web sources:*
- [WEB-14] arXiv:2508.19831 — Hindi instruction-following / conversational evaluation benchmarks 'largely unavailable publicly'; confirms no Hindi pedagogical rationale rubric exists
- [WEB-13] IndicGenBench covers Hindi generation but not exam rationale quality

*Dataset analysis:*
- DATASET-D1: target='option1' is the only output label; no rationale field exists in schema
- DATASET-D9: Compound interest answer is just 'option2' with no worked solution — confirms no explanation field

</details>

**Requires expert verification:**
- A pedagogical-NLP expert should design a Hindi exam rationale rubric covering factual accuracy, fluency, and pedagogical clarity — this is wholly outside MILU's scope.

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
For the MCQ-label correctness narrowly, MILU has reasonable provenance: answers are inherited from online exam portals where 'subject experts ensure the accuracy of the answers' [Q26], with AI4Bharat volunteer manual audits [Q87] and researcher review of subject-tag clusters [Q41]. However, the paper reports no annotator demographics, no inter-annotator agreement statistics, and no formal QA protocol beyond manual sampling. Critically, the deployment's core output (Hindi rationale) has no ground-truth labels in MILU at all. Dataset analysis surfaces additional concerns: cross-language item duplication (DATASET-D14/D15/D29) and malformed items with truncated stems (DATASET-D34, D35) suggest QA imperfections at the item level. ~55% of subject labels were assigned via machine translation + GPT-4O-MINI [Q37, Q38], an automated process that may not preserve Hindi-specific terminology fidelity.

**Strengths:**
- Answer keys derive from established Indian competitive-exam ecosystems where subject experts validate correctness at source [Q26].
- Multi-stage manual review applied to subject-tag clusters [Q41] and a manual audit pass [Q87].
- Constitutional, historical, and GK answer labels in the observed Hindi sample appear factually correct (DATASET-D1, D2, D22).

**Checklist:**

- **OC-1**: MCQ answer labels reflect Indian exam-portal subject-expert consensus [Q26], which is reasonable for central-exam content. However, regional stakeholder perspectives on rationale quality have no representation since rationale labels do not exist. — _Sources: Q26_
- **OC-2**: INSUFFICIENT DOCUMENTATION on annotator-population disagreement risk for MCQ labels; annotator demographics are not reported beyond 'AI4Bharat volunteers' [Q87].
- **OC-3**: Paper does not provide a Datasheet or Data Statement with annotator demographics — gap for assessing convergent validity.
- **OC-4**: Re-annotation by Hindi-medium subject experts would be needed to (a) validate translation quality on the ~25%+ translated Hindi subset, (b) flag items where the answer is region-sensitive, (c) generate ground-truth Hindi rationales. — _Sources: Q38_
- **OC-5**: INSUFFICIENT DOCUMENTATION on aggregation methods; the paper describes manual cluster review [Q41] but not how disagreements were resolved.
- **OC-6**: Label issues: (a) no IAA statistics; (b) ~55% of topic labels assigned by automated MT+GPT pipeline [Q37, Q38]; (c) cross-language duplicates introduce identical labels across translated copies (DATASET-D14/D15); (d) malformed items have labels whose validity is questionable (DATASET-D34, D35); (e) rationale ground-truth wholly absent. — _Sources: Q37, Q38, DATASET-D14, DATASET-D15, DATASET-D29, DATASET-D34, DATASET-D35_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q26] 'These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers.' (p.3)
- [Q87] 'We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits.' (p.9)
- [Q41] 'We manually review these clusters and assign appropriate subject labels.' (p.4)
- [Q37] 'we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information.' (p.4)
- [Q38] 'we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question.' (p.4)

*Dataset analysis:*
- DATASET-D14/D15: Identical 1991 crisis question across English and translated Hindi — labels are correct but duplicated
- DATASET-D29: 44th Amendment question identical across Hindi/Tamil/Malayalam — confirms label propagation via translation
- DATASET-D34: Truncated English stem with assigned label='option2' — label validity questionable for malformed item
- DATASET-D35: Truncated Malayalam 'Directions:' stem with label assignment — same QA gap

</details>

**Information gaps:**
- Annotator demographics, IAA statistics, and disagreement-resolution protocols are not reported.
- Translation-quality verification for the Hindi partition is not documented.
- No Hindi rationale ground truth exists in the benchmark.

**Requires expert verification:**
- A Hindi-medium subject-matter expert should audit a representative Hindi sample for label correctness, especially for translated items and items with stems that may have been corrupted by RC-passage stripping.

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The output form mismatch is fundamental and acknowledged by the paper itself. MILU evaluates via log-likelihood option selection [Q52, Q53, Q54, Q55] or zero-shot JSON-formatted option choice for API models [Q56, Q57]. The authors note explicitly that this 'may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting' [Q85]. The deployment requires open-ended Hindi-language explanatory generation — a fundamentally different output form. Dataset analysis confirms the schema contains only a 'target' MCQ label field (DATASET-D1, D9) with no infrastructure for evaluating fluency, correctness, or pedagogical quality of free-text Hindi output. External evidence confirms no comparable Hindi-language NLG benchmark for exam rationale exists [WEB-13, WEB-14].

**Strengths:**
- MCQ accuracy can validate the verdict-correctness portion of the deployment's output.
- Per-language, per-subject accuracy reporting [Q59, Q67] supports diagnostic identification of weak areas.
- Multiple shot configurations (0/1/5-shot) [Q50] provide robustness checks on the verdict accuracy.

**Checklist:**

- **OF-1**: Major mismatch: MILU outputs MCQ option labels [Q55, Q57]; deployment requires open-ended Hindi rationale plus verdict (elicitation Q3). The verdict portion is partially covered; the rationale portion is wholly uncovered. — _Sources: Q55, Q57, DATASET-D1, DATASET-D9_
- **OF-2**: Not applicable — deployment is text-only, no TTS requirement.
- **OF-3**: Target population is graduate-level (high literacy within cohort), so accessibility is not the bottleneck — the bottleneck is rationale quality, which MILU cannot evaluate.
- **OF-4**: Form mismatches: (a) MCQ vs. open-ended generation; (b) log-likelihood scoring [Q53] vs. free-text Hindi generation quality; (c) no fluency/coherence/pedagogical metrics. The paper itself flags this limitation [Q85]. — _Sources: Q53, Q85, WEB-13, WEB-14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q52] 'For non-API-based models, we use the LM-EVALUATION-HARNESS' (p.5)
- [Q53] 'We use the log-likelihood method, where the probability of a given output string is computed by conditioning it on some provided input' (p.5)
- [Q55] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability' (p.5)
- [Q56] 'The API-based models are evaluated using the generative approach due to the lack of support for prompt log probabilities.' (p.5)
- [Q57] 'We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing.' (p.5)
- [Q85] 'our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting.' (p.9)

*Web sources:*
- [WEB-13] IndicGenBench (ACL 2024) covers Hindi generation but not exam rationale quality
- [WEB-14] arXiv:2508.19831 confirms Hindi instruction-following / conversational benchmarks 'largely unavailable publicly'

*Dataset analysis:*
- DATASET-D1: Schema contains only 'target' field with MCQ option label — no rationale field
- DATASET-D9: Quantitative answer is just option label, no worked solution — confirms output form is option-selection only

</details>

**Requires expert verification:**
- A Hindi-language NLG evaluation specialist should design a custom rationale-quality rubric (factual accuracy, fluency, pedagogical clarity, register) since no off-the-shelf Hindi resource exists [WEB-13, WEB-14].

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** No taxonomy or label set for rationale quality dimensions exists in MILU.

**Recommendation:** Adopt or develop a multi-axis rationale-quality taxonomy (e.g., 4-axis: factuality, fluency, pedagogical helpfulness, Manak Hindi register), informed by Hindi-medium coaching pedagogy conventions. Expert verification by Hindi-medium UPSC/SSC educators is required.

### Output Form ⚠

**Gap:** MILU evaluates only MCQ option selection; deployment requires open-ended Hindi rationale generation.

**Recommendation:** Design and operationalize a separate Hindi rationale-quality benchmark with (a) human-rated rubric (factual accuracy, fluency, pedagogical clarity, register), (b) ~500–1000 expert-authored gold rationales for a stratified sample of MILU Hindi items, (c) automated metrics (BLEURT/COMET-style for Hindi, plus LLM-as-judge calibrated against expert ratings).

### Input Content ⚠

**Gap:** Hindi partition appears to contain a high proportion of translated items (DATASET-D13: 100% in observed sample), pervasive cross-language duplication, and stale Current Affairs.

**Recommendation:** Curate a deployment-specific Hindi subset: (a) prefer items with is_translated=False where they exist; (b) deduplicate across languages; (c) replace pre-2023 Current Affairs items with a fresh annual current-affairs probe; (d) ensure North India sub-regional items (Chhath Puja, zamindari, North Indian freedom fighters) are sufficiently represented via custom item authoring.

### Input Content ⚠

**Gap:** North India sub-regional content (Chhath Puja, zamindari, regional freedom fighters) is sparsely observed in the Hindi sample (1 of 26 items).

**Recommendation:** Author or source ~200–500 additional Hindi items specifically covering North India sub-regional content within central-exam framing, drawing from authentic UPSC/SSC previous-year papers.

### Input Ontology

**Gap:** Mathematics/Reasoning and Current Affairs are not separately enumerated in MILU's 8 macro-domains; central-exam vs. state-PSC items are commingled without metadata.

**Recommendation:** Add metadata layer mapping each MILU item to (a) UPSC/SSC/banking syllabus category (including explicit Math/Reasoning, Current Affairs), (b) central-exam vs. state-PSC scope. This enables filtered evaluation aligned to syllabus weights [WEB-9, WEB-10, WEB-15].

### Output Content

**Gap:** No annotator demographics, IAA statistics, or formal QA protocol reported; ~55% of topic labels assigned by automated GPT-4O-MINI [Q37, Q38]; malformed items observed (DATASET-D34, D35).

**Recommendation:** Conduct a Hindi-medium expert audit on a stratified sample of the Hindi test split: verify answer correctness, translation-register quality, item completeness, and subject-tag accuracy. Report IAA. Filter or repair malformed items prior to deployment-grade evaluation.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge." |
| Q2 | 1 | input_content | "With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science." |
| Q3 | 1 | output_form | "We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q4 | 1 | output_form | "Open multilingual models outperform language-specific fine-tuned models, which perform only slightly better than random baselines." |
| Q5 | 1 | input_ontology | "Models also perform better in high-resource languages as compared to low-resource ones." |
| Q6 | 1 | output_ontology | "Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM." |
| Q7 | 1 | input_ontology | "To the best of our knowledge, MILU is the first of its kind benchmark focused on Indic languages, serving as a crucial step towards comprehensive cultural evaluation." |
| Q8 | 1 | input_content | "All code, benchmarks, and artifacts will be made publicly available to foster open research." |
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
| Q21 | 2 | input_content | "All the artifacts will be released publicly." |
| Q22 | 3 | input_ontology | "MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge." |
| Q23 | 3 | input_ontology | "This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others." |
| Q24 | 3 | input_content | "These questions were sourced following an approach similar to AGIEVAL (Zhong et al., 2023), collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams, among others." |
| Q25 | 3 | input_content | "We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages." |
| Q26 | 3 | output_content | "These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers." |
| Q27 | 3 | input_ontology | "Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years." |
| Q28 | 3 | input_content | "Regional state exams are particularly valuable as they cover various state-level topics and emphasize the official language of each state." |
| Q29 | 3 | input_form | "In total, we collected more than 150K questions across 11 Indian Languages- Bengali (bn), Gujarati (gu), Hindi (hi), Kannada (kn), Malayalam (ml), Marathi (mr), Odia (or), Punjabi (pn), Tamil (ta), Telugu (te), and English (en)-spanning 41 diverse subjects." |
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
| Q46 | 4 | input_ontology | "In total, we release around 79K questions across 41 subjects across 8 domains in 11 languages, capping each subject-language pair at 500 questions for feasible evaluations." |
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
| Q91 | 10 | input_content | "Sumanth Doddapaneni, Rahul Aralikatte, Gowtham Ramesh, Shreya Goyal, Mitesh M. Khapra, Anoop Kunchukuttan, and Pratyush Kumar. 2023. Towards leaving no Indic language behind: Building monolingual corpora, benchmark and models for Indic languages. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 12402–12426, Toronto, Canada. Association for Computational Linguistics." |
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
| WEB-1 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2186639 |
| WEB-2 | https://news.careers360.com/womens-share-in-civil-services-up-from-24-35-pc-in-5-years-engineers-over-50-percent-government-data-upsc-ias-ips |
| WEB-3 | https://theprint.in/india/family-support-safety-study-material-a-click-away-whats-driving-more-women-to-take-upsc-exam/1922660/ |
| WEB-4 | https://scroll.in/article/825780/bihar-uttar-pradesh-rajasthan-and-madhya-pradesh-have-worst-literacy-rates-school-outcomes |
| WEB-5 | https://en.wikipedia.org/wiki/Literacy_in_India |
| WEB-6 | https://trai.gov.in/sites/default/files/2024-11/Cons_P_14092023.pdf |
| WEB-7 | https://en.wikipedia.org/wiki/Internet_in_India |
| WEB-8 | https://www.iamai.in/sites/default/files/research/Kantar_%20IAMAI%20report_2024_.pdf |
| WEB-9 | https://testbook.com/ias-preparation/upsc-prelims-subject-wise-weightage |
| WEB-10 | https://www.pw.live/ssc/exams/ssc-cgl-syllabus |
| WEB-11 | https://upsc.gov.in/examinations/active-examinations/civil-services-examination |
| WEB-12 | https://sleepyclasses.com/discover-how-many-candidates-are-selected-in-upsc-each-year/ |
| WEB-13 | https://aclanthology.org/2024.acl-long.595/ |
| WEB-14 | https://arxiv.org/html/2508.19831v1 |
| WEB-15 | https://vajiramandravi.com/upsc-exam/csat-syllabus/ |
| WEB-16 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-17 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-18 | https://prsindia.org/billtrack/digital-personal-data-protection-bill-2023 |
| WEB-19 | https://www.saikrishnaassociates.com/decoding-the-india-ai-governance-guidelines/ |
| WEB-20 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2234853&reg=3&lang=1 |
| WEB-21 | https://github.com/google-research-datasets/indic-gen-bench |
| WEB-22 | https://captaincompliance.com/education/dpdpa-india-the-complete-guide-to-indias-digital-personal-data-protection-act-2023/ |
| WEB-23 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2123422 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (configs: Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu)
**Analysis date:** 2025-08-01
**Examples reviewed:** 215 total (21 Bengali, 20 English, 24 Gujarati, 26 Hindi, 17 Kannada, 16 Malayalam, 21 Marathi, 21 Odia, 25 Punjabi, 19 Tamil, 25 Telugu) — all from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Hindi, validation | 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? … 44वें संविधान संशोधन अधिनियम द्वारा" | Polity/Constitution question in Hindi, about 44th Constitutional Amendment — UPSC core topic | IC, IO |
| D2 | Hindi, validation | 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? … साकी मुस्तईद खान" | Mughal-period history question in Hindi — directly relevant to North India medieval history | IC, IO |
| D3 | Hindi, validation | 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? … अभ्रक" | State-specific GK question about Uttar Pradesh minerals — North India sub-regional content | IC, IO |
| D4 | Hindi, validation | 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते? … आठ" | Current Affairs question (2022) about archery medal count — time-bounded, may be stale | IC, IO |
| D5 | Hindi, validation | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: … मोटर की गति बहुत अधिक होती है" | Engineering/Physics question in Hindi, `is_translated: True` — not in UPSC/SSC core syllabus | IC, IO |
| D6 | Hindi, validation | 3 | option2 | "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: … पल्सेटिंग डीसी" | Technical engineering question in Hindi, `is_translated: True` — domain not central to UPSC/SSC GS | IC, IO |
| D7 | Hindi, validation | 4 | option2 | "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। … शेल" | Electrical engineering, translated — technical domain not prioritized for Hindi-medium UPSC prep | IO |
| D8 | English, validation | 6 | option3 | "Fill in the gap below with suitable word. Fruit ∶ Reap∶∶ Flower ∶ _____… Bloom" | Logical Reasoning/analogy question in English — confirms presence of reasoning subject | IO |
| D9 | English, validation | 7 | option2 | "If Rs. 4000 becomes Rs. 5760 in 2 years at compound interest … what is the annual rate of interest? … 20 percent" | Mathematics/Quantitative Aptitude question (compound interest) — confirms presence in English partition | IO |
| D10 | Hindi, validation | 17 | option4 | "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? … संपत्ति कर" | Economics/direct tax question in Hindi — Economics is relevant to GK syllabus | IC |
| D11 | Hindi, validation | 13 | option1 | "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? … अरबी भाषा" | General Knowledge question in Hindi (monsoon etymology) — accessible, pan-India GK | IC |
| D12 | Hindi, validation | 19 | option3 | "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? … पाकिस्तान" | Geography GK question in Hindi — relevant to UPSC/SSC syllabus, Devanagari script, no English terms | IC, IF |
| D13 | Hindi (all examples) | all 26 | — | All 26 Hindi examples: is_translated = True | Every Hindi validation example in the sample is machine-translated from English | IC |
| D14 | English, validation | 1 | option3 | "What was the immediate cause for loss of foreign reserves triggering the financial crisis in 1991? … Sharp rise in value of imports of oil & petroleum products" | English original; same question appears in Hindi (D15) and Bengali — confirms translation pipeline | IC |
| D15 | Hindi, validation | 18 | option3 | "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था? … तेल और पेट्रोलियम उत्पादों के आयात के मूल्य में तीव्र वृद्धि" | Hindi translation of D14 — fluent Hindi, but `is_translated: True`, confirms translation pipeline | IC |
| D16 | Hindi, validation | 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है? … एक जंप लेबल या फॉर्मेट लेबल" | Computer Science / Fortran programming question in Hindi — very niche for UPSC/SSC aspirants | IO |
| D17 | Hindi, validation | 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा। … प्रबंधक ने अपने सहायक से कहा कि उसे अगले महीने बोनस मिलेगा।" | Hindi Language Studies question (indirect speech) — tests Hindi grammar directly | IC, IF |
| D18 | Hindi, validation | 22 | option4 | "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? … अमृता शेरगिल" | Arts & Culture GK in Hindi — pan-India Indian art figure | IC |
| D19 | Marathi, validation | 16 | option3 | "हलषष्ठी सण का साजरा केला जातो? … मुलाच्या दीर्घायुष्यासाठी" | Regional festival question in Marathi — culturally specific, regional content (not Hindi/North India) | IC |
| D20 | Gujarati, validation | 16 | option2 | "છત્તીસગઢના નીચેના કયા બળવાઓને 'બસ્તરનો સ્વાતંત્ર્ય સંઘર્ષ' પણ કહેવામાં આવે છે? … લિંગગિરી બળવો" | Chhattisgarh tribal revolt question — regional Indian history, culturally grounded | IC |
| D21 | Hindi, validation | 5 | option1 | "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं … सदाबहार ओक के पेड़ … भूमध्यसागरीय" | Geography question (Mediterranean climate) — translated, pan-India geography, no English code-mixing | IC, IF |
| D22 | English, validation | 3 | option4 | "What was the first capital of the Bahamani Kingdom? … Gulbarga" | India-specific historical knowledge (Deccan Sultanate) — same question appears across all languages | OC |
| D23 | Hindi, validation | 15 | option3 | "1950 में स्थापित, भारतीय रेलवे द्वारा स्वामित्व वाली औद्योगिक इकाइयों में से एक का नाम भारतीय स्वतंत्रता सेनानी के नाम पर रखा गया है: … चित्तरंजन दास" | Indian history/GK — freedom fighter named railway unit; is_translated: True | IC |
| D24 | English, validation | 9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct? … Estimate Committee: All members of this committee are from Assembly only." | State-level (Maharashtra) governance question in English partition — not central exam scope | IO |
| D25 | Punjabi, validation | 5 | option4 | "ਫਰਵਰੀ - ਮਾਰਚ 2022 ਵਿੱਚ ਹੋਈ ਰਾਜ ਵਿਧਾਨਸਭਾ ਚੋਣਾਂ ਵਿੱਚ, ਆਮ ਆਦਮੀ ਪਾਰਟੀ (AAP) ਨੇ … ਪੰਜਾਬ" | Current Affairs (2022 state elections) in Punjabi — politically specific, time-bounded | IC |
| D26 | Hindi, validation | 20 | option3 | "नेत्रगोलक लगभग गोलाकार होता है जिसकी व्यास लगभग कितनी होती है? … 2.3 सेमी" | Biology/Science question in Hindi — `is_translated: True`, basic science fact | IO |
| D27 | Telugu, validation | 25 | option1 | "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? … మొరెనా" | State-level GK (Madhya Pradesh industrial geography) in Telugu — regional, not central exam | IO |
| D28 | Hindi, validation | 24 | option4 | "तंगस्टन तत्व का प्रतीक क्या है? … W" | Chemistry/Science fact question in Hindi, `is_translated: True` — basic science, not UPSC priority | IO |
| D29 | Malayalam, validation | 6 | option1 | "ദേശീയ അടിയന്തരാവസ്ഥ പ്രഖ്യാപിക്കാൻ 'സായുധ കലാപം' എന്ന പദം ഭരണഘടനയിൽ ചേർത്തത് എപ്പോൾ? … 44-ാമത് ഭരണഘടനാ ഭേദഗതി നിയമം വഴി" | Same Constitutional Amendment question appears in Hindi (D1), Tamil, and Malayalam — cross-language duplication | IC, OC |
| D30 | Marathi, validation | 13 | option2 | "प्रांतांमध्ये द्वैधशासन प्रणाली कोणत्या कायद्याने स्थापन केली? … भारत सरकार अधिनियम 1919" | Indian constitutional history question (dyarchy) — India-specific, historically grounded | IC |
| D31 | English, validation | 15 | option3 | "Founded in 1950, one of the industrial units owned by Indian Railways is named after the Indian freedom fighter: … Chittaranjan Das" | India-specific GK, English original — Chittaranjan Das is a pan-India figure relevant to GK | IC |
| D32 | Hindi, validation | 11 | option2 | "संदीप माइकल निम्नलिखित में से किस खेल से जुड़े थे? … हॉकी" | Sports GK in Hindi — niche figure, is_translated: True | IC |
| D33 | Bengali, validation | 5 | option4 | "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) … পাঞ্জাব" | 2022 state elections Current Affairs — AAP, UP, Goa all named; time-bounded content | IC |
| D34 | English, validation | 11 | option2 | "The owner of the textile shop brought a … Calculator" | Incomplete stem — "brought a" with no further context; question appears malformed | IC, OC |
| D35 | Malayalam, validation | 14 | option4 | "ദിശകൾ: മാർബിൾ ഉപയോഗിക്കാവുന്നത് … ശിൽപ്പം" | Incomplete stem ("Directions: marble can be used") — same truncated structure appears across languages | IC, OC |
| D36 | Hindi, validation | 16 | — | "एएम की बैंडविड्थ _________ है। … 1110 kHz" | AM bandwidth engineering question — highly technical, `is_translated: True`; unlikely in UPSC GS | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Core UPSC/SSC Polity and Constitutional Law Coverage in Hindi
- **Dimension(s):** IO, IC
- **Observation:** The Hindi partition includes substantive questions on Indian constitutional law — specifically the 44th Constitutional Amendment (adding 'armed rebellion' for national emergency declaration) and other governance questions. These directly address the high-priority UPSC/SSC subject of Indian Polity & Constitution.
- **Deployment relevance:** For central exam aspirants, constitutional amendment questions are among the most tested areas in UPSC GS Paper 2 and SSC General Awareness. The Hindi rendering is clear and uses correct Devanagari terminology without excessive code-mixing.
- **Datapoint citations:**
  - [D1] Example 6 (Hindi, split=validation, label=option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? … 44वें संविधान संशोधन अधिनियम द्वारा" — UPSC-relevant Polity question in fluent Devanagari, no significant English intrusion.

#### Strength 2: Mughal and North Indian Medieval History Coverage
- **Dimension(s):** IO, IC
- **Observation:** The Hindi partition contains Mughal-period history questions (e.g., the authorship of 'Masir-e-Alamgiri') and pan-India medieval history questions (e.g., who completed the Qutb Minar). These are directly in scope for UPSC GS Paper 1 Indian history, with emphasis on the Delhi Sultanate and Mughal era that is especially prominent in North Indian exam preparation.
- **Deployment relevance:** Mughal administrative history and North Indian medieval landmarks are high-frequency topics in both UPSC and SSC GK sections. The Qutb Minar question also appears consistently across all language partitions, confirming it as a pan-India GK anchor.
- **Datapoint citations:**
  - [D2] Example 25 (Hindi, split=validation, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? … साकी मुस्तईद खान" — Mughal literary history, directly relevant to UPSC GS1.
  - [D22] Example 3 (English, split=validation, label=option4): "What was the first capital of the Bahamani Kingdom? … Gulbarga" — pan-India medieval history, same question appearing in all language partitions.

#### Strength 3: North India–Specific Regional GK Present in Hindi Partition
- **Dimension(s):** IC, IO
- **Observation:** The Hindi sample contains at least one question specifically about Uttar Pradesh's mineral resources, addressing sub-regional content within a central-exam framing. This is the type of India-within-India regional knowledge that the deployment requires the AI to handle.
- **Deployment relevance:** Central exams (UPSC, SSC) occasionally test state-specific geography and resource questions. The presence of a UP-specific item in the Hindi partition confirms that MILU does include some North India sub-regional content, partially addressing the documented gap.
- **Datapoint citations:**
  - [D3] Example 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? … अभ्रक" — UP state GK question in Hindi; directly serves the North India sub-regional layer.

#### Strength 4: Hindi Script Fidelity and Low Code-Mixing in Observed Examples
- **Dimension(s):** IF, IC
- **Observation:** Across all 26 Hindi examples examined, the questions and answer options are written in standard Devanagari. Technical terms are rendered in Hindi transliterations (e.g., "पल्सेटिंग डीसी" for "pulsating DC," "ट्रांसफार्मर" for transformer) or Hindi equivalents. Roman script or English-medium phrasing is minimal — the observed Hindi items do not appear to exceed the deployment's ~10% code-mixing ceiling.
- **Deployment relevance:** The target student population can read standard Devanagari Hindi; the absence of heavy Roman-script intrusion in the observed sample is a positive signal for accessibility.
- **Datapoint citations:**
  - [D12] Example 19 (Hindi, split=validation, label=option3): "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? … पाकिस्तान" — Pure Devanagari, no English terms.
  - [D21] Example 5 (Hindi, split=validation, label=option1): "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं … सदाबहार ओक के पेड़ … भूमध्यसागरीय" — "ओक" (oak) is retained as a transliterated loanword; "भूमध्यसागरीय" (Mediterranean) is a full Sanskrit-Hindi rendering — appropriate register.

#### Strength 5: Breadth of India-Centric General Knowledge Subjects
- **Dimension(s):** IO, IC
- **Observation:** Across the Hindi and English partitions, the sample contains questions spanning Economics (direct tax, 1991 financial crisis), Geography (Radcliffe Line, Mediterranean climate), Biology (eyeball diameter, Blue Baby Syndrome), Arts & Culture (Amrita Shergil), and History — consistent with the multi-domain pan-India GK coverage required for UPSC and SSC.
- **Deployment relevance:** The multi-domain spread matches the general awareness section tested across all central exams, confirming that the benchmark does not over-index on a single domain.
- **Datapoint citations:**
  - [D10] Example 17 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? … संपत्ति कर" — Economics GK in Hindi, UPSC/SSC relevant.
  - [D11] Example 13 (Hindi, split=validation, label=option1): "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? … अरबी भाषा" — GK in Hindi, accessible register.
  - [D18] Example 22 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? … अमृता शेरगिल" — Indian arts culture GK.

#### Strength 6: Presence of Logical Reasoning and Quantitative Questions (in English Partition)
- **Dimension(s):** IO
- **Observation:** The English partition includes both Logical Reasoning (analogy questions, coding-decoding in Telugu) and Quantitative Aptitude (compound interest calculation). These subjects correspond to UPSC CSAT Paper 2 and SSC CGL Tier 1, which are priority areas the deployment must cover.
- **Deployment relevance:** While these appear in the English partition specifically, their presence confirms that MILU's taxonomy does encompass the Reasoning and Mathematics domains that were flagged as potentially absent. The English partition is described as covering Indian-culture-specific content; the presence of reasoning questions here suggests the Hindi partition likely also has them.
- **Datapoint citations:**
  - [D8] Example 6 (English, split=validation, label=option3): "Fill in the gap below with suitable word. Fruit ∶ Reap∶∶ Flower ∶ _____ … Bloom" — Analogy reasoning question confirming domain presence.
  - [D9] Example 7 (English, split=validation, label=option2): "If Rs. 4000 becomes Rs. 5760 in 2 years at compound interest (compounded annually), then what is the annual rate of interest? … 20 percent" — Quantitative aptitude/compound interest.

#### Strength 7: Hindi Grammar and Language Proficiency Questions Present
- **Dimension(s):** IO, IC
- **Observation:** The Hindi partition includes a Hindi Language Studies question testing indirect speech transformation (reported speech) — a topic directly tested in UPSC Hindi language paper and SSC Hindi proficiency sections.
- **Deployment relevance:** Hindi language proficiency is explicitly listed as a priority subject for this deployment, and the benchmark contains at least some questions testing grammatical competence in Hindi.
- **Datapoint citations:**
  - [D17] Example 9 (Hindi, split=validation, label=option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा। … प्रबंधक ने अपने सहायक से कहा कि उसे अगले महीने बोनस मिलेगा।" — Hindi indirect speech transformation, tests Hindi grammatical knowledge.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: 100% Translation Rate in Hindi Validation Sample — No Natively Authored Hindi Questions Observed
- **Dimension(s):** IC
- **Observation:** All 26 Hindi validation examples in the sample carry `is_translated: True`. Not a single natively authored Hindi question appears in this sample. This means every Hindi question observed was originally written in English and translated via GPT-4O. The benchmark documentation states that only ~25% of the total dataset is translated; however, this sample suggests the Hindi validation partition may have a much higher translated proportion than the overall dataset average.
- **Deployment relevance:** This is critical for the deployment. Translated questions may not reflect the vocabulary conventions, sentence structures, or idiomatic phrasing of Hindi-medium competitive exam papers (which have their own established register). Questions authored in Hindi for exams like UPSC Hindi medium, UPPSC, or Hindi SSC papers have characteristic patterns that differ from back-translated English. If the Hindi partition predominantly consists of translated items, the benchmark may poorly represent the linguistic environment of the target student — and models fine-tuned or evaluated on translated Hindi may perform differently on authentically authored Hindi exam content.
- **Datapoint citations:**
  - [D13] All 26 examples (Hindi, split=validation): is_translated = True for all — "जब एक डीसी सीरीज मोटर बिना लोड के चलती है…", "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है…", "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह'…" — every item carries the translated flag.
  - [D15] Example 18 (Hindi, split=validation, label=option3): "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था?" — direct translation of D14 (English: "What was the immediate cause for loss of foreign reserves…"), confirming the translation pipeline.

#### CRITICAL Concern 2: Output Ontology Mismatch — MCQ Labels Only, No Explanatory Rationale Infrastructure
- **Dimension(s):** OO, OF
- **Observation:** Every datapoint in the dataset provides only a `target` field (one of option1–option4) as the ground-truth output. There is no rationale field, explanation field, or any annotation supporting the deployment's required output: a substantive Hindi-language explanation of why an answer is right or wrong.
- **Deployment relevance:** The deployment's core output is a correct/incorrect label **plus** a Hindi-language explanatory rationale (elicitation Q3). MILU benchmark scores measure only whether a model selects the correct MCQ option — they cannot validate whether the model's Hindi explanations are factually accurate, fluent, or pedagogically appropriate. This is a fundamental scope mismatch confirmed by direct inspection of the data schema. The paper's own limitation section acknowledges the log-likelihood evaluation may differ from generation-based approaches (Q85), but even generation-based scoring in MILU only assesses option selection.
- **Datapoint citations:**
  - [D1] Example 6 (Hindi, split=validation, label=option1): target = "option1" — the only output label is the MCQ choice; no rationale, no explanation field exists in the schema.
  - [D9] Example 7 (English, split=validation, label=option2): target = "option2" — compound interest answer with no worked solution or explanation provided; the schema has no field for this.

#### MAJOR

#### MAJOR Concern 1: Heavy Engineering/Technology Domain Skew in Hindi Sample — Misalignment with Central Exam Priority
- **Dimension(s):** IO
- **Observation:** Of the 26 Hindi validation examples, at least 7 are from Engineering & Tech (DC motor behavior, half-wave rectifier, constant current transformer, AM bandwidth, Fortran 77 column labels, wood swelling in timber, Materials Science) and 3 more are from Science (Computer Science, Biology). Together these constitute approximately 38% of the Hindi sample. By contrast, only 1 question is from Law & Governance (the 44th Amendment, D1) and only 2 are from Arts & Humanities with historical content (D2, D23).
- **Deployment relevance:** For UPSC/SSC/banking central exam preparation, Engineering & Tech and advanced Computer Science questions (e.g., Fortran 77 syntax, D16) are low-priority relative to History, Polity, Geography, and Economics. The observed sample distribution suggests the Hindi partition may over-represent technical domains (possibly because English engineering exam content was translated to fill gaps), which does not reflect the actual subject distribution of UPSC GS or SSC General Awareness syllabi.
- **Datapoint citations:**
  - [D5] Example 1 (Hindi, split=validation): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" — Engineering question, is_translated: True.
  - [D6] Example 3 (Hindi, split=validation): "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है" — Engineering question, is_translated: True.
  - [D7] Example 4 (Hindi, split=validation): "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है" — Engineering question, is_translated: True.
  - [D16] Example 8 (Hindi, split=validation): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है" — Niche Computer Science, is_translated: True; not in UPSC/SSC General Studies syllabus.
  - [D36] Example 16 (Hindi, split=validation): "एएम की बैंडविड्थ _________ है। … 1110 kHz" — Electrical engineering bandwidth, is_translated: True.

#### MAJOR Concern 2: Current Affairs Questions Are Time-Bounded and May Be Stale
- **Dimension(s):** IC, IO
- **Observation:** Multiple examples contain Current Affairs questions tied to specific years (2022 state elections, May 2022 archery tournament, 2020 Filmfare Awards, 2021 Padma Awards, Hillary Clinton's June 2014 book). MILU was published in 2024, and these questions reference events from 2014–2022 — meaning a significant portion of "Current Affairs" content is already dated and may not represent the current affairs knowledge tested in 2025–2026 exam cycles.
- **Deployment relevance:** Current Affairs is one of the most heavily weighted and variably tested areas of UPSC GS Paper 1 (confirmed in the web search context). For a deployment serving students preparing for 2025–2026 exam cycles, a benchmark sourced from exams up to ~2023 will have stale current affairs content. Model performance on MILU's Current Affairs items does not predict readiness for current exam cycles.
- **Datapoint citations:**
  - [D4] Example 2 (Hindi, split=validation): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — 2022 sports event; stale for 2025–26 exam prep.
  - [D25] Example 5 (Punjabi, split=validation): "ਫਰਵਰੀ - ਮਾਰਚ 2022 ਵਿੱਚ ਹੋਈ ਰਾਜ ਵਿਧਾਨਸਭਾ ਚੋਣਾਂ ਵਿੱਚ, ਆਮ ਆਦਮੀ ਪਾਰਟੀ (AAP) ਨੇ … ਪੰਜਾਬ" — 2022 election results; dated.

#### MAJOR Concern 3: Cross-Language Item Duplication Reduces Effective Question Pool Size
- **Dimension(s):** OC, IC
- **Observation:** The same factual questions appear identically translated across multiple language partitions. Examples include: the 1991 financial crisis question (Bengali Ex.1, English Ex.1, Hindi Ex.18, Malayalam Ex.1); the Bahamani Kingdom capital (Bengali Ex.3, English Ex.3, Gujarati Ex.3, Malayalam Ex.3, Punjabi Ex.3); the Qutb Minar completion (Bengali Ex.18, English Ex.18, Gujarati Ex.18, Hindi, Kannada Ex.15, Punjabi Ex.18, Tamil Ex.18); the Mediterranean climate question (English Ex.5, Gujarati Ex.5, Hindi Ex.5, Kannada Ex.5, Malayalam Ex.5, Marathi Ex.5, Punjabi, Tamil Ex.5, Telugu Ex.5). This pattern strongly suggests that a significant fraction of MILU consists of the same items translated, not independently sourced questions for each language.
- **Deployment relevance:** If the same items are used across language partitions via translation, the "79,000 questions" figure conflates distinct items with translated copies. For the Hindi partition specifically, the effective number of unique factual scenarios tested may be substantially smaller than the headline count suggests. Additionally, cross-language translation introduces a risk that questions originally designed for one language/exam context (e.g., SSC English) are not genuinely representative of the Hindi-medium exam ecosystem.
- **Datapoint citations:**
  - [D29] Example 6 (Malayalam, split=validation, label=option1): "ദേശീയ അടിയന്തരാവസ്ഥ പ്രഖ്യാപിക്കാൻ 'സായുധ കലാപം' എന്ന പദം ഭരണഘടനയിൽ ചേർത്തത് എപ്പോൾ?" — same 44th Amendment question as D1 (Hindi), D6 (Tamil), confirmed duplicate across Malayalam.
  - [D14] Example 1 (English, split=validation) and [D15] Example 18 (Hindi, split=validation): "What was the immediate cause for loss of foreign reserves…" / "1991 में वित्तीय संकट को ट्रिगर करने वाले…" — literal translation confirmed by is_translated field.

#### MAJOR Concern 4: Incomplete / Truncated Question Stems Observed
- **Dimension(s):** OC, IC
- **Observation:** At least two distinct examples contain severely truncated or incomplete question stems that do not provide enough context for meaningful answering. English Example 11 reads only "The owner of the textile shop brought a" with options including Computer, Calculator, Pencil, and Fountain pen — with no coherent question preceding this stem fragment. The marble/sculpture directions question appears similarly across Malayalam (Ex.14), Marathi (Ex.14), Telugu (Ex.14), Tamil (Ex.14) as "Directions: marble can be used" or equivalent, with options for painting, music, stones, and sculpture. These appear to be reading-comprehension remnants where the passage was stripped but the question fragment survived.
- **Deployment relevance:** Malformed or incomplete items undermine the validity of the benchmark. A model that encounters such items cannot answer based on the question content — any response is essentially random. If such items appear in the test split, they will add noise to accuracy scores in a way that is not informative about model quality. For a deployment context where the AI must explain the reasoning behind an answer, such items are particularly problematic.
- **Datapoint citations:**
  - [D34] Example 11 (English, split=validation, label=option2): "The owner of the textile shop brought a … Calculator" — No coherent question is present; the stem is a sentence fragment.
  - [D35] Example 14 (Malayalam, split=validation, label=option4): "ദിശകൾ: മാർബിൾ ഉപയോഗിക്കാവുന്നത് … ശിൽപ്പം" — Truncated "Directions:" stem without the relevant passage; same pattern in Marathi Ex.14, Telugu Ex.14, Tamil Ex.14.

#### MINOR

#### MINOR Concern 1: State-Level Content Mixed with Central Exam Content Without Labeling
- **Dimension(s):** IO
- **Observation:** Some items clearly pertain to state-level governance rather than central exams — for example, the Maharashtra Legislative Committee question (English Ex.9) and the Madhya Pradesh Banmore industrial area question (Telugu Ex.25). These are not labeled in the metadata as "state-PSC" versus "central exam" items, making it impossible to filter the benchmark for central-exam-only use without manual review.
- **Deployment relevance:** The deployment is explicitly scoped to central-level examinations (UPSC, SSC, banking), not state PSCs. Items about Maharashtra's legislative committee procedures or MP's industrial geography add noise if used for evaluating central-exam readiness but are not identifiable from the `domain` or `subject` metadata.
- **Datapoint citations:**
  - [D24] Example 9 (English, split=validation, label=option2): "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" — state-level governance question, not central exam scope.
  - [D27] Example 25 (Telugu, split=validation, label=option1): "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? … మొరెనా" — State-level (MP) geography question.

#### MINOR Concern 2: North India–Specific Sub-Regional Content Sparse in Observed Hindi Sample
- **Dimension(s):** IC
- **Observation:** Only one question in the Hindi sample (D3, UP minerals) could be classified as specifically North India sub-regional. No questions about Chhath Puja, Bhojpuri culture, zamindari systems, North Indian freedom movement figures (Chandrashekhar Azad, Ram Prasad Bismil), or UP/Bihar/Rajasthan administrative specifics were observed. The Mughal history question (D2) is pan-India/pan-subcontinental rather than specifically North Indian.
- **Deployment relevance:** The deployment must handle both pan-India GK and North India–specific content for central exams. The scarcity of observed North India sub-regional items (1 of 26) suggests this layer may be thinly represented in the Hindi partition, though a 26-item sample is insufficient to make a strong claim.
- **Datapoint citations:**
  - [D3] Example 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — the only observed North India–specific item in the Hindi sample.

#### MINOR Concern 3: Regional/State-Specific Cultural Content Appears Only in Non-Hindi Partitions
- **Dimension(s):** IC
- **Observation:** Culturally specific regional content (the Halashashthi festival in Marathi Ex.16, Lokranjan Mahotsav in Marathi/Gujarati, Chhattisgarh Bastar revolt in Gujarati/Kannada/Punjabi/Telugu, Sindhi poet Vasdev Mohi in Gujarati, Telangana literature in Kannada) appears in non-Hindi partitions. In the Hindi partition, no comparably region-specific Hindi-belt cultural content (festivals, literary traditions specific to Hindi-speaking North India) was observed.
- **Deployment relevance:** This creates a mild concern that MILU's culturally grounded content — which is a stated design strength — may be distributed toward South Indian and West Indian language partitions, where regional state exams provide richer locally sourced material. The Hindi partition, which is most important for this deployment, may rely more heavily on translated pan-India content than on natively sourced culturally specific Hindi exam content.
- **Datapoint citations:**
  - [D19] Example 16 (Marathi, split=validation, label=option3): "हलषष्ठी सण का साजरा केला जातो? … मुलाच्या दीर्घायुष्यासाठी" — Maharashtra-specific festival question; no equivalent Hindi-belt festival question observed.
  - [D20] Example 16 (Gujarati, split=validation, label=option2): "છત્તીસગઢના નીચેના કયા બળવાઓને 'બસ્તરનો સ્વાતંત્ર્ય સંઘર્ષ' … લિંગગિરી બળવો" — Chhattisgarh tribal revolt; this question also appears in Kannada, Punjabi, Telugu but not observed in Hindi.

---

### Content Coverage Summary

The MILU dataset, as observed across 215 examples from the validation split, is a large-scale MCQ benchmark with broad subject coverage across 11 Indic languages. The Hindi partition (26 examples) demonstrates adequate rendering in standard Devanagari with low observed code-mixing, and contains substantive content relevant to UPSC/SSC central exam topics including Indian constitutional law, Mughal history, and general knowledge in Economics and Geography.

However, two structural features substantially limit the benchmark's fit for this deployment. First, the entire Hindi validation sample is machine-translated (`is_translated: True` for all 26 items), raising questions about linguistic authenticity for the target population of Hindi-medium exam aspirants. Second, the observed domain distribution in the Hindi sample is skewed toward Engineering & Technology (DC motors, transformers, AM bandwidth, Fortran 77) — subjects that are peripheral to UPSC GS and SSC General Awareness. This skew likely results from the translation gap-filling strategy (translating English engineering exam questions to meet minimum thresholds) documented in the benchmark paper.

The English partition shows broader subject coverage, including Logical Reasoning and Mathematics questions, confirming these domains exist within MILU's taxonomy — but their representation in the Hindi partition specifically remains unverified from this sample.

Cross-language item duplication is pervasive: the same factual questions (Bahamani Kingdom capital, Qutb Minar, 1991 financial crisis, Mediterranean climate) appear identically translated across all 11 language partitions in the validation split. This is structurally expected for a translated benchmark but means the effective number of unique factual scenarios is smaller than the total item count implies.

Two malformed items with truncated stems were observed across multiple language partitions, suggesting imperfect filtering of reading-comprehension remnants from the scraping process.

The benchmark's output schema (MCQ `target` field only) provides no infrastructure for evaluating the Hindi-language explanatory rationale that constitutes the deployment's core output — a fundamental mismatch that cannot be remedied by data inspection alone.

---

### Limitations

1. **Sample size and representativeness:** Only validation split examples were examined (26 Hindi, 20–25 per other language). The test split contains approximately 6,600–10,000 examples per language config; the observed 100% translation rate in the Hindi validation sample cannot be generalized to the full test split without examining a larger sample. The actual distribution of natively authored vs. translated Hindi items in the test set requires direct inspection.

2. **Subject distribution cannot be quantified from this sample:** The 26 Hindi examples are insufficient to estimate the true proportion of Engineering/Tech vs. History/Polity/GK/Reasoning items in the Hindi test partition. The observed skew may be an artifact of the small validation sample.

3. **No test split content inspected:** All examples are from the validation split, which is used for few-shot examples in the benchmark's evaluation protocol. The test split (which is the actual evaluation set) was not sampled, and subject distributions may differ.

4. **Translation quality unassessable from inspection alone:** While observed Hindi items are fluent Devanagari, the quality of GPT-4O translations for technical domains (especially Electrical Engineering, Computer Science) relative to authentic Hindi exam register cannot be assessed through casual reading — it would require review by a Hindi-medium domain expert.

5. **No audio or image modality:** These are excluded by MILU's design; no inspectability concern applies.

6. **Rationale quality entirely outside data scope:** The deployment's core output (Hindi explanatory rationale) is wholly absent from the dataset schema. No amount of data inspection can assess this dimension; it requires a separate evaluation framework.

