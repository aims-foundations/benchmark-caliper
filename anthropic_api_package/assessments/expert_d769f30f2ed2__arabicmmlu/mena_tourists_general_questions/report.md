## Deployment Context

**Use case:** Support foreigners visiting Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, or KSA in answering their general questions
**Target population:** Non-Arab tourists or expats visiting Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, or KSA and have general questions about the Arabic language, history or geography of these countries

# Validity Analysis: arabicmmlu
**Target context:** Non-Arab Tourists and Expats in Eight Arabic-Speaking Countries (ArabicMMLU Deployment)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 3 | Moderate gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 3 | Moderate gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ⚠ | 1 | Serious concern | high |
| **Average** | **2.0** | | |

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

ArabicMMLU is a serious ground-up Arabic-language knowledge benchmark whose subject taxonomy and authentic source materials provide reasonable construct validity for evaluating school-curriculum knowledge of Arabic language, history, and geography. For the specific deployment of non-Arab tourists/expats across eight Arabic-speaking countries seeking educational-level knowledge, however, two structural mismatches dominate the assessment: (1) the single-correct-answer MCQ output ontology and form fundamentally cannot evaluate the multi-perspective, explanatory natural-language responses the deployment explicitly requires [Q27, Q88, elicitation A3]; and (2) input content and verification skew heavily Jordanian, with Morocco's school-curriculum content largely absent, Kuwait effectively absent, and no Palestinian annotators despite Palestine being a top-3 source country [Q31, Q89, WEB-3, DATASET-D4, DATASET-D5]. The 96% answer-key verification ceiling [Q43] likely reflects Jordanian/Egyptian consensus rather than pan-regional validity for contested historical and civic content. Strengths include authentic exam sourcing across eight countries, level-appropriate subject coverage, MSA text-only format matching the deployment modality, and confirmed substantial Palestinian STEM/curriculum content.

## Practical Guidance

### What This Benchmark Measures

ArabicMMLU measures a model's ability to select curriculum-designated correct answers on MCQ school-exam questions across 40 subjects spanning STEM, social science, humanities, Arabic language, and other domains, drawn predominantly from Jordan with substantial Egyptian and Palestinian content. The strongest dimension for this deployment is Input Ontology (subject coverage approximately matches the deployment's school-curriculum scope) and Input Form (uniform MSA text matches deployment modality). It can usefully assess whether a system has acquired the factual content of Jordanian-curriculum school knowledge in MSA.

### Construct Depth

The benchmark probes factual recall and basic reasoning at primary, middle, and high school levels (university content only 6% [Q71]), but only at the depth of single-correct-answer MCQ. It does not probe explanatory quality, multi-perspective reasoning, perspective-flagging on contested content, robustness to learner-register Arabic, or appropriate framing for non-Muslim/non-Arab audiences — all of which are central to the deployment requirements. The Output Ontology and Output Form dimensions, scored 1, indicate that even a model achieving the 96% verification ceiling [Q44] would not have been evaluated on the pluralistic, explanatory behaviors the deployment demands.

### What Else You Need

For valid deployment evaluation, substantial supplementation is required: (1) an open-ended Arabic generation evaluation such as AraGen with 3C3H LLM-as-judge [WEB-6] or 'Beyond MCQ' [WEB-5] to address the OO/OF gap; (2) a bespoke contested-content evaluation with Palestinian, Moroccan, and Kuwaiti subject-matter experts to address the OC gap; (3) Moroccan and Kuwaiti school-curriculum item collection to address the IO/IC coverage gaps for those deployment countries; (4) a learner-register Arabic robustness evaluation (none exists [WEB-6, gap_id 5]) to address the IF gap; and (5) explicit perspective-flagging evaluation specific to the eight-country contested-content scope, which no existing benchmark targets.

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The benchmark's taxonomy of 40 tasks across school subjects and education levels [Q25] aligns well with the deployment's school-curriculum knowledge scope (history, geography, Arabic language, civics) [Q72, Q73]. However, several taxonomic issues materially harm content validity for this deployment: (a) the taxonomy includes categories irrelevant to the tourist/expat school-knowledge use case — Driving Test, professional Law (Morocco-only), vocational General Knowledge — that were observed in the sampled data [DATASET-D5, DATASET-D26, DATASET-D27]; (b) university-level content is only 6% of the dataset [Q71]; (c) Civics content as instantiated is overwhelmingly Jordanian-specific rather than pan-Arab [DATASET-D4]; (d) Morocco's school-curriculum (history/geography/civics) is essentially absent from the sample, with Morocco's contribution concentrated in professional law [DATASET-D5]; (e) Kuwait does not appear at all in the sample [Limitations.5]. The future-work acknowledgment of needed extensions — short-answer questions, larger regional coverage, professional-domain content [Q88] — confirms these are recognized gaps.

**Strengths:**
- Authentic school-curriculum framing across primary/middle/high school directly matches the deployment's knowledge scope [Q25, Q28, DATASET-D38, DATASET-D34]
- Subject groups explicitly include Arabic-specific contexts (history, geography, civics, political science) that are deployment-relevant [Q72, Q73]
- Broad multi-subject taxonomy with level-appropriate complexity confirmed in sampled data [DATASET-D38, DATASET-D22, DATASET-D34]

**Checklist:**

- **IO-1**: Required categories for this deployment: Arabic language, Arab history, Arab geography, civics/social science at school-curriculum level [elicitation Q1, A1]; explicitly out of scope are dialectal phrases, tourist etiquette, practical travel, and professional domains. — _Sources: Q25, Q72, Q73_
- **IO-2**: Yes — country-specific school-curriculum coverage is unequal. Morocco's school subjects are largely absent from the sample (only professional law observed) [DATASET-D5]; Kuwait does not appear at all [Limitations.5]; civics is Jordan-only in the sample [DATASET-D4]. The paper acknowledges unequal country representation [Q89, Q90, Q91]. — _Sources: Q89, Q90, Q91, DATASET-D4, DATASET-D5, WEB-3_
- **IO-3**: Yes — Driving Test [DATASET-D26], professional Law [DATASET-D5], vocational General Knowledge (sheet metal screws, hospital names) [DATASET-D27, DATASET-D10], and University Accounting/Management [DATASET-D22, DATASET-D23] are out of scope for the deployment's school-curriculum tourist knowledge use case. — _Sources: DATASET-D5, DATASET-D26, DATASET-D27, DATASET-D22_
- **IO-4**: Documented gaps: (1) absence of Maghrebi school-curriculum content for Morocco; (2) absence of Kuwaiti curriculum; (3) lack of a multi-perspective or contested-content taxonomic dimension despite the subjects most relevant to the deployment being inherently contested [Q72, Q73]; (4) university-level content underrepresented at 6% [Q71]. — _Sources: Q71, Q72, Q88, DATASET-D4_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'ArabicMMLU is an Arabic multiple-choice question-answering dataset comprising 40 tasks spanning a wide range of subjects and education levels.' (p.3)
- [Q71] 'This could be attributed to the relatively small portion (i.e., 6%) of university-level questions in ArabicMMU' (p.7)
- [Q72] 'We present the performance of open-source models on selected subjects that potentially contain Arabic-specific contexts.' (p.7)
- [Q88] 'ArabicMMLU can be extended to include short-answer or essay questions, different modalities, larger region coverage, and more questions in professional settings.' (p.9)
- [Q89] 'ArabicMMLU does not represent all Arabic countries equally.' (p.9)

*Web sources:*
- [WEB-3] Jordan, Egypt, and Palestine confirmed as top-3 source countries; Kuwait not in top tier
- [WEB-2] Morocco-sourced questions present but model performance distinctively lower

*Dataset analysis:*
- DATASET-D4: All 5 sampled Civics MS items are exclusively Jordan-specific — confirms Jordan-skew in the civics taxonomy slot
- DATASET-D5: All 5 Morocco samples are professional law, none from school-curriculum subjects
- DATASET-D26: Driving Test items (UAE, Lebanon, Egypt) — out of scope for school-curriculum deployment
- DATASET-D27: Vocational General Knowledge items (sheet metal screws) — irrelevant to tourist/expat use case
- Kuwait absence: zero Country=Kuwait examples across ~210 sampled examples

</details>

**Information gaps:**
- Exact per-country, per-subject distribution counts not extractable from documentation
- Whether Country=null items are truly pan-Arab or reflect missing metadata

**Requires expert verification:**
- Whether sub-regional curriculum distinctions (Maghrebi, Levantine, Gulf) are meaningfully represented in the full dataset beyond the sampled configs

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Authentic ground-up sourcing from school exams across eight countries [Q1, Q26] is a substantial strength over translation-based prior work [Q5, Q6], and Palestine being a top-3 source country is materially better than the scaffold anticipated [WEB-3, WEB-4]. However, content distribution is severely unequal: Jordan contributes 6,000+ questions while some countries contribute as few as 100 [Q89]; Morocco lacks annotators and Maghrebi school-curriculum coverage [DATASET-D5]; Kuwait is effectively absent [Limitations.5]; and contested historical content is framed through Jordanian curriculum perspective [DATASET-D1, DATASET-D2, DATASET-D3]. OCR corruption in some Egyptian university items [DATASET-D23, DATASET-D24] introduces construct-irrelevant variance. Islamic Studies content is presented prescriptively from an internal Muslim perspective [DATASET-D14, DATASET-D35], misaligned with the non-Muslim tourist target population. Per the elicitation, pan-Arab framing is acceptable [A2], but the system should flag country-specific content — yet the benchmark's ground-truth treats Jordanian framing as the silent default for civic and historical questions [DATASET-D4].

**Strengths:**
- Ground-up data collection from authentic school exams in eight countries, distinct from prior translation-based approaches [Q1, Q5, Q6, Q26]
- Palestine confirmed as top-3 source country with substantive curriculum content across multiple subjects [WEB-3, WEB-4, DATASET-D17, DATASET-D20, DATASET-D21]
- Native-speaker workforce with regional collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia [Q31, Q96]
- GPT-4 performance gap (80% on translated MMLU vs 72.5% on ArabicMMLU) supports construct validity for culturally grounded knowledge [Q64, Q65]

**Checklist:**

- **IC-1**: Yes — many inputs require region-specific knowledge of Arab history, geography, Jordanian/Egyptian/Palestinian curricula, and Islamic religious practice [Q72, Q73, DATASET-D1, DATASET-D14]. — _Sources: Q72, Q73, DATASET-D1, DATASET-D14_
- **IC-2**: Partially — pan-Arab framing is acceptable per elicitation [A2], but contested historical content (e.g., King Abdullah I and Zionism [DATASET-D1], 1948 events) is framed from Jordanian curriculum perspective without flagging this country-specificity, conflicting with the deployment requirement to flag rather than silently generalize country-specific content. — _Sources: DATASET-D1, DATASET-D2, DATASET-D3_
- **IC-3**: Limited Western-specific content concern — some Geography items ask about non-Arab global facts (Kilimanjaro, Shanghai) [MINOR Concern 11], but these are general world knowledge rather than Western-specific cultural content. The more pressing issue is Jordan-specific content presented as default Arab content. — _Sources: DATASET-D4_
- **IC-4**: Verified by 2 native Arabic speakers on 100 sampled questions [Q42], yielding 96% match [Q43] — but no Moroccan, Palestinian, or Kuwaiti annotators participated in collection or verification [Q31, Q96]. Palestinian-sourced contested content was verified by non-Palestinian workers. — _Sources: Q42, Q43, Q31, Q96_
- **IC-5**: Documented content issues: (1) Jordan-skew (~6,000+ questions) vs. ~100 for others [Q89]; (2) Morocco's school-curriculum content largely absent [DATASET-D5]; (3) Kuwait effectively absent [Limitations.5]; (4) OCR corruption in university Egyptian items [DATASET-D23, DATASET-D24]; (5) Islamic Studies presented prescriptively for Muslim students rather than explanatorily for non-Muslim visitors [DATASET-D14, DATASET-D35]; (6) Jordanian-curriculum framing of contested historical events [DATASET-D1, DATASET-D2, DATASET-D3]. — _Sources: Q89, DATASET-D5, DATASET-D23, DATASET-D24, DATASET-D14, DATASET-D35, DATASET-D1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we present ArabicMMLU, the first multi-task language understanding benchmark for the Arabic language, sourced from school exams across diverse educational levels in different countries spanning North Africa, the Levant, and the Gulf regions.' (p.1)
- [Q26] 'The questions are sourced from eight different countries in North Africa (Morocco and Egypt), the Levant (Jordan, Palestine, and Lebanon), and the Gulf (UAE, Kuwait, and KSA).' (p.3)
- [Q89] 'ArabicMMLU does not represent all Arabic countries equally. For example, we have collected over 6K multiple-choice questions from Jordan, while other countries are represented with only 100 questions or, in some cases, not at all.' (p.9)
- [Q96] 'We extend our gratitude to all collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia who participated in the data collection process.' (p.10)
- [Q65] 'our ArabicMMU presents a greater challenge due to its inclusion of a higher proportion of Arabic-specific content.' (p.7)

*Web sources:*
- [WEB-3] Jordan, Egypt, Palestine named as top-3 source countries
- [WEB-4] HuggingFace dataset card confirms Palestine as top-3 contributor
- [WEB-2] BLOOMZ and Jais perform notably worse on Morocco-sourced questions, indicating Morocco content is distinctive but underrepresented

*Dataset analysis:*
- DATASET-D1: Question on King Abdullah I and Zionism — Jordanian curriculum framing of contested Palestinian history
- DATASET-D4: All 5 Civics MS items are Jordan-only, confirming Jordan-skew in civics domain
- DATASET-D5: Morocco's representation concentrated in professional law, absent from school-curriculum subjects
- DATASET-D14: Islamic Studies questions presuppose Muslim reader perspective
- DATASET-D23, DATASET-D24: Severe OCR corruption in Egyptian university items
- DATASET-D35: Arabic Language reading passage frames Islamic ritual prescriptively

</details>

**Information gaps:**
- Exact per-country question counts beyond top-3 not published
- Proportion of OCR-corrupted items in full dataset

**Requires expert verification:**
- Whether ground-truth labels for Palestinian-sourced contested-history questions reflect Palestinian historiography
- Whether Moroccan curriculum perspectives in history/geography are present in the full dataset beyond the sampled configs
- Whether Islamic Studies items would be considered appropriately framed for non-Muslim educational use

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The benchmark is uniformly text-only MSA [Q2, Q92], aligning with the deployment's text-only modality [A4] and MSA target [elicitation]. Multimodal content was discarded [Q37] and contextual passages preserved where needed [Q38]. However, the benchmark's MSA is fluent native-speaker register from school exams, while the deployment's users are non-native learners with basic-to-intermediate MSA proficiency, likely producing grammatically imperfect or code-switched Arabic [elicitation, expected_arabic_proficiency]. This signal-distribution gap is structural and undocumented as a design trade-off in the paper. The benchmark also notes that real-world Arabic LLM exposure includes dialectal Arabic, which is excluded here [Q92]. One minor data-quality issue observed: an Arabic Language Grammar item with English question stem [DATASET-D16] inconsistent with the stated Arabic-only design [Q30].

**Strengths:**
- Text-only MSA format directly aligns with deployment's text-based modality [Q2, Q93, A4]
- Multimodal content systematically excluded; contextual passages preserved for dependent questions [Q37, Q38]
- Prompt language variants (Arabic/English) tested, providing some signal on cross-lingual prompt sensitivity [Q47]
- Uniform MSA register confirmed across all sampled configs [DATASET-D29, DATASET-D15]

**Checklist:**

- **IF-1**: Signal distribution mismatch: benchmark assumes fluent native-speaker MSA from school exams [Q2], while deployment users produce learner-register MSA potentially with grammatical imperfection and code-switching [elicitation expected_arabic_proficiency, languages.user_input_register]. No dedicated benchmark for non-native Arabic robustness identified [WEB-6, gap_id 5]. — _Sources: Q2, Q92, WEB-6_
- **IF-2**: Infrastructure supports text-only Arabic input; RTL rendering requirement noted [writing_systems]. No infrastructure barriers identified for tourists/expats with personal devices [infrastructure_notes]. — _Sources: Q93_
- **IF-3**: Domain-specific form differences: dialectal Arabic excluded from benchmark [Q92] but is common in real-world MENA usage; learner code-switching with Latin script likely [writing_systems] but not represented. — _Sources: Q92_
- **IF-4**: Form mismatch: learner-register input vs. fluent-MSA evaluation creates undocumented signal-distribution gap. One data-quality artifact: English question stem in nominally Arabic-only benchmark [DATASET-D16]. — _Sources: DATASET-D16, Q30_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'Our data comprises 40 tasks and 14,575 multiple-choice questions in Modern Standard Arabic (MSA) and is carefully constructed by collaborating with native speakers in the region.' (p.1)
- [Q30] 'When designing ArabicMMLU, we excluded questions in English and only included questions in Arabic.' (p.3)
- [Q37] 'workers were instructed to include only questions accompanied by an answer key, and to discard questions containing multi-modal information' (p.4)
- [Q92] 'The dataset primarily focuses on Modern Standard Arabic (MSA). However, multilingual and Arabic LLMs are often exposed to both MSA and dialectical Arabic.' (p.9)
- [Q93] 'ArabicMMLU is focused solely on text-based assessment' (p.9)

*Web sources:*
- [WEB-6] Arabic LLM benchmark survey (40+ benchmarks) does not list any learner-register robustness benchmark

*Dataset analysis:*
- DATASET-D29: Clear MSA grammar question, text-only — confirms uniform MSA register
- DATASET-D15: MSA prose passage with comprehension question
- DATASET-D16: English question stem in Arabic-language config — minor inconsistency with stated Arabic-only design

</details>

**Information gaps:**
- No empirical evaluation of model performance on learner-register or code-switched Arabic input

**Requires expert verification:**
- Whether tourist/expat learner Arabic deviates from benchmark MSA in ways that materially affect downstream system behavior

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
This is the most critical structural mismatch for this deployment. The label schema is exclusively single-correct-answer MCQ with 2–5 candidate options [Q27], and every sampled example confirms this format [DATASET-D1, all]. The deployment explicitly requires multi-perspective acknowledgment of contested historical and civic questions [elicitation A3], but the benchmark's output taxonomy structurally cannot represent or score such pluralistic responses. The four prompt-configuration variants tested vary only in prompt language and output script [Q47], not in label structure. Contested questions like King Abdullah I and Zionism [DATASET-D1], GCC founding states [DATASET-D25], and 'elements of a state' with 'occupation' as a distractor option [DATASET-D18] are all reduced to single correct labels reflecting one curriculum's framing. The future-work note proposing short-answer and essay questions [Q88] tacitly acknowledges this limitation. Open-ended Arabic evaluation alternatives exist (AraGen, 'Beyond MCQ' — [WEB-5, WEB-6]) but are not part of ArabicMMLU itself.

**Strengths:**
- MCQ format produces well-defined, reproducible scoring for factual recall tasks [Q27]
- Multiple prompt-configuration variants enable analysis of prompt-language sensitivity [Q47]

**Checklist:**

- **OO-1**: Output label categories are uniform single-correct MCQ [Q27], reviewed against deployment requirement for multi-perspective acknowledgment [elicitation A3] — fundamental misalignment. — _Sources: Q27_
- **OO-2**: Missing categories: multi-perspective/multi-correct labels, perspective-flagging labels, explanatory/short-answer outputs, abstention labels for contested content. None present in benchmark [Q27, Q88]. — _Sources: Q27, Q88_
- **OO-3**: The single-correct-answer assumption encodes a 'one curriculum framing is correct' value that conflicts with the deployment's pluralistic requirement [elicitation A3]; instances like the King Abdullah I question [DATASET-D1] and 'occupation' distractor [DATASET-D18] make this concrete. — _Sources: DATASET-D1, DATASET-D18, DATASET-D25_
- **OO-4**: Stakeholder-driven taxonomy redesign needed for deployment use; supplementary frameworks (AraGen 3C3H, 'Beyond MCQ') identified but not specifically targeted at contested historical content [WEB-5, WEB-6, net_new_findings]. — _Sources: WEB-5, WEB-6_
- **OO-5**: Documented: structural validity violation (construct of multi-perspective knowledge cannot be represented), content validity violation (multi-perspective categories absent), and external validity risk (benchmark performance will not predict pluralistic response quality). — _Sources: Q27, Q88, DATASET-D1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q27] 'Each question has 2–5 candidate answers, with one correct answer.' (p.3)
- [Q47] 'We initially conducted experiments with four settings... vary only in prompt language and output script' (p.5)
- [Q88] 'For future work, ArabicMMLU can be extended to include short-answer or essay questions' (p.9)
- [Q100] 'This is a Natural Science question for primary school in Jordan. Select the correct answer!' (p.14)

*Web sources:*
- [WEB-5] 'Beyond MCQ' Arabic open-ended benchmark identified as supplementary option
- [WEB-6] AraGen with 3C3H LLM-as-judge metric for open-ended Arabic generation

*Dataset analysis:*
- DATASET-D1: Contested Jordanian/Palestinian history reduced to single Jordanian-curriculum correct answer
- DATASET-D18: 'Occupation' (الاحتلال) used as distractor in 'elements of a state' — politically loaded MCQ framing without multi-perspective acknowledgment
- DATASET-D25: GCC founding states reduced to single true/false answer

</details>

**Requires expert verification:**
- Which specific contested questions in the full dataset would require multi-perspective treatment under the deployment's pluralistic framing

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Label-correctness verification process — 96% inter-annotator agreement on 100 sampled questions [Q42, Q43] with native MSA speakers holding Bachelor's degrees and competitive compensation [Q35, Q36, Q39] — establishes a reasonable practical ceiling [Q44]. However, annotator-pool composition undermines convergent validity for the multi-country deployment: 10 annotators are from Jordan (4), Egypt (2), Lebanon (1), UAE (1), KSA (2), with no Moroccan, Kuwaiti, or Palestinian annotators [Q31] despite Palestine being a top-3 source country [WEB-3, WEB-4]. For contested historical questions where 'correct' answers vary across national curricula, the 96% agreement likely reflects Jordanian/Egyptian consensus rather than pan-regional validity. The sampled data shows concrete examples of Jordanian-curriculum framing for shared Arab history [DATASET-D1, DATASET-D2, DATASET-D3, DATASET-D11]. Training data contamination is acknowledged as unverifiable [Q95]. OCR corruption in university Egyptian items [DATASET-D23, DATASET-D24] suggests label quality may degrade in some sub-corpora. No aggregation method considerations for minority perspectives are documented.

**Strengths:**
- 96% answer-key accuracy verification on a 100-question sample provides a documented quality ceiling [Q42, Q43, Q44]
- Native-speaker annotator workforce with at least Bachelor's degrees and competitive pay [Q35, Q36, Q39]
- Pre-collection workshop standardized annotator process [Q40]
- Annotators include workers from 5 of 8 deployment countries (Jordan, Egypt, Lebanon, UAE, KSA) [Q31, Q96]

**Checklist:**

- **OC-1**: Partially — labels reflect curriculum-stated 'correct' answers from source exams, which encode national perspectives. For non-contested STEM content this is acceptable [DATASET-D21, DATASET-D38]; for contested civic/historical content [DATASET-D1, DATASET-D3], labels reflect source-country curriculum perspective without acknowledgment. — _Sources: DATASET-D1, DATASET-D3, DATASET-D21_
- **OC-2**: High potential for disagreement on contested content — Palestinian, Moroccan, and Kuwaiti perspectives are not represented in the verifier pool [Q31] despite Palestine being a major source [WEB-3, WEB-4]. The 96% figure [Q43] likely overstates regional validity for politically sensitive items. — _Sources: Q31, WEB-3, WEB-4_
- **OC-3**: Documented: 6 internal workers (1 Jordanian, 1 Egyptian, 1 Lebanese, 1 UAE, 2 KSA), 4 external workers (3 Jordanian, 1 Egyptian) [Q31]; internal workers are Master's/RA-level CS students, external workers hold Bachelor's [Q35]. Demographics are documented but skew Jordanian/Egyptian. — _Sources: Q31, Q35_
- **OC-4**: Re-annotation by Palestinian, Moroccan, and Kuwaiti annotators recommended for contested-content items, especially history/civics from those source countries. — _Sources: Q31, Q96_
- **OC-5**: No aggregation method for minority/competing perspectives is documented — the benchmark's structure precludes it [Q27]. — _Sources: Q27_
- **OC-6**: Documented: (1) annotator-pool skew toward Jordan/Egypt with absent Moroccan/Palestinian/Kuwaiti perspectives [Q31, Q96]; (2) 96% ceiling does not account for cross-curriculum disagreement on contested content [Q43, Q44]; (3) OCR corruption in some sub-corpora [DATASET-D23, DATASET-D24]; (4) contamination unverifiable [Q95]. — _Sources: Q31, Q43, Q44, Q95, DATASET-D23, DATASET-D24_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'a total of 10 Arabic native speakers from different countries: 6 internal workers (1 Jordanian, 1 Egyptian, 1 Lebanese, 1 from UAE, and 2 from KSA) and 4 external workers (3 Jordanian and 1 Egyptian).' (p.4)
- [Q42] 'we assessed the accuracy of our data collection by having two native Arabic speakers annotate 100 randomly sampled questions' (p.4)
- [Q43] 'We found that 96% of the questions and answer keys match on average' (p.4)
- [Q44] 'This 96% score is considered to represent the maximum score meaningfully achievable for ArabicMMLU.' (p.4)
- [Q95] 'we cannot assert that the model's pretraining data is free from contamination.' (p.10)
- [Q96] 'collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia' (p.10)

*Web sources:*
- [WEB-3] Palestine confirmed top-3 source country — yet no Palestinian annotators in pool
- [WEB-4] HuggingFace dataset card confirms Palestine major contributor

*Dataset analysis:*
- DATASET-D1: Jordanian-framing of King Abdullah I/Zionism question — verified by non-Palestinian workers
- DATASET-D3: Jordanian-British 1928 treaty framing as authoritative
- DATASET-D11: Jordanian royal history as primary social science fact
- DATASET-D23, DATASET-D24: OCR-corrupted Egyptian university items where label correctness becomes ambiguous

</details>

**Information gaps:**
- Whether the 100-question verification sample included contested-content items
- Distribution of OCR corruption across the full dataset

**Requires expert verification:**
- Whether Palestinian, Moroccan, and Kuwaiti subject-matter experts would agree with ground-truth labels on country-sourced contested items

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark measures performance as percentage MCQ accuracy [Q3, Q45] via highest-token-probability scoring for open-source models [Q50, Q79] or first-token regex matching for closed-source models [Q53, Q54]. This output form is fundamentally misaligned with the deployment's requirement for open-ended, explanatory, multi-perspective natural-language responses [elicitation A3]. The benchmark cannot evaluate whether a model produces appropriately nuanced, perspective-flagging answers — it can only score whether the model selects the curriculum-designated correct option. Additional output-form analyses (calibration [Q80], length-confidence correlation [Q82], few-shot trends [Q75, Q76], negation sensitivity [Q83, Q84]) all operate on the same MCQ scoring surface. The text-based MCQ form is appropriate for literacy-capable populations [Q93] in principle, but the form mismatch with the deployment's natural-language explanatory output requirement is structural and not addressable through reweighting or filtering. Supplementary frameworks (AraGen 3C3H, 'Beyond MCQ') exist [WEB-5, WEB-6] but are separate evaluations.

**Strengths:**
- Standardized accuracy metric is reproducible and comparable across 35 evaluated models [Q3, Q45]
- Auxiliary analyses (calibration, length-confidence, negation sensitivity) provide robustness signal beyond raw accuracy [Q80, Q82, Q83]
- Two scoring methods documented for open-source vs closed-source models [Q50, Q53]

**Checklist:**

- **OF-1**: Mismatch — benchmark output is discrete MCQ labels [Q3, Q50, Q53]; deployment requires open-ended natural-language responses with multi-perspective acknowledgment [elicitation A3, output_form_mismatch]. — _Sources: Q3, Q50, Q53_
- **OF-2**: Not applicable — deployment is text-only [A4], so TTS availability is not required. — _Sources: Q93_
- **OF-3**: Target population is literate non-native Arabic learners [target_population_description]; text output is appropriate, but the benchmark's discrete-label form does not assess natural-language fluency, explanatory quality, or perspective-flagging. — _Sources: Q93_
- **OF-4**: Documented: external validity violation — benchmark MCQ accuracy will not predict whether the system produces appropriately explanatory, multi-perspective natural-language responses required by the deployment [elicitation A3, output_form_mismatch.mismatch_severity=HIGH]. — _Sources: Q3, Q94_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'Our comprehensive evaluations of 35 models reveal substantial room for improvement' (p.1)
- [Q45] 'Our experiments focus on zero-shot and few-shot settings across 35 models.' (p.5)
- [Q50] 'for open-source models, we determine the answer based on the highest probability among all possible options.' (p.6)
- [Q53] 'For closed-source models, we determine the answer based on the first token generated in the text using a regular expression.' (p.6)
- [Q93] 'ArabicMMLU is focused solely on text-based assessment, and the exploration of multimodal questions is left for future work.' (p.9)
- [Q94] 'our experimental results do not provide conclusive answers regarding the performance of LLMs in Arabic.' (p.9)

*Web sources:*
- [WEB-5] 'Beyond MCQ' Arabic open-ended benchmark — supplementary alternative for OF
- [WEB-6] AraGen 3C3H LLM-as-judge framework for open-ended Arabic generation

*Dataset analysis:*
- All sampled examples uniformly use single-correct MCQ format with no explanatory or multi-answer outputs

</details>

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** Single-correct-answer MCQ format cannot represent multi-perspective acknowledgment required by deployment [Q27, elicitation A3]

**Recommendation:** Supplement ArabicMMLU with an open-ended Arabic generation evaluation (e.g., AraGen 3C3H [WEB-6] or 'Beyond MCQ' [WEB-5]) and develop a custom rubric that scores perspective-flagging on contested historical/civic items, with explicit credit for acknowledging country-specific framings.

### Output Form ⚠

**Gap:** MCQ accuracy scoring cannot evaluate explanatory natural-language quality required by deployment [Q3, Q50, Q53]

**Recommendation:** Adopt LLM-as-judge or human-rater scoring of free-form responses to a curated subset of ArabicMMLU history/civics/Islamic-studies questions reformulated as open-ended questions, scoring on correctness, completeness, and multi-perspective coverage.

### Input Content ⚠

**Gap:** Morocco's school-curriculum content (history/geography/civics) is largely absent; Kuwait is effectively absent [DATASET-D5, Limitations.5]

**Recommendation:** Commission targeted collection of Moroccan and Kuwaiti primary/middle/high school exam items in history, geography, and civics, with native annotators from each country, to extend country coverage before deployment-relevant evaluation.

### Output Content ⚠

**Gap:** Annotator pool lacks Palestinian, Moroccan, and Kuwaiti members despite Palestine being a top-3 source country [Q31, WEB-3]

**Recommendation:** Re-verify a stratified sample of Palestinian-, Moroccan-, and Egyptian-sourced contested-content items with annotators from those countries; report disagreement rates separately from the 96% pooled figure to expose curriculum-specific disagreement.

### Input Form

**Gap:** Benchmark MSA register does not represent learner-register, code-switched Arabic produced by non-native users [Q92, elicitation expected_arabic_proficiency]

**Recommendation:** Construct a small bespoke evaluation set of learner-register and code-switched Arabic queries paraphrasing ArabicMMLU items, and measure performance degradation; this addresses the documentation gap noted in [WEB-6] where no learner-register Arabic benchmark exists.

### Input Ontology

**Gap:** Out-of-scope categories (Driving Test, professional Law, vocational General Knowledge) inflate aggregate scores irrelevantly [DATASET-D5, DATASET-D26, DATASET-D27]

**Recommendation:** Define a deployment-relevant subset of ArabicMMLU configs (history, geography, civics, Arabic language, social science, Islamic studies at appropriate framing) and report scores only on this subset; exclude driving test, professional law, and vocational items.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we present ArabicMMLU, the first multi-task language understanding benchmark for the Arabic language, sourced from school exams across diverse educational levels in different countries spanning North Africa, the Levant, and the Gulf regions." |
| Q2 | 1 | input_form | "Our data comprises 40 tasks and 14,575 multiple-choice questions in Modern Standard Arabic (MSA) and is carefully constructed by collaborating with native speakers in the region." |
| Q3 | 1 | output_form | "Our comprehensive evaluations of 35 models reveal substantial room for improvement, particularly among the best open-source models." |
| Q4 | 1 | output_form | "Notably, BLOOMZ, mT0, LLaMA2, and Falcon struggle to achieve a score of 50%, while even the top-performing Arabic-centric model only achieves a score of 62.3%." |
| Q5 | 1 | input_content | "Although large language models (LLMs) such as GPT-3.5 (Ouyang et al., 2022), BLOOMZ (Muennighoff et al., 2022), and Jais (Sengupta et al., 2023) have been pretrained with substantial coverage of Modern Standard Arabic (MSA), their reasoning and knowledge assessments are primarily conducted using datasets translated from English to Arabic (Sengupta et al., 2023; Huang et al., 2023), which means there is limited capacity to evaluate content specific to Arabic." |
| Q6 | 1 | input_content | "This reliance on translation systems not only demonstrates an Anglocentric approach (Ramesh et al., 2023; Talat et al., 2022) but also potentially introduces errors and biases." |
| Q7 | 1 | input_content | "Given that Arabic is one of the most widely-spoken languages in the world, with a speaker population of over 400 million people (Shoufan and Alameri, 2015; Diab et al., 2017), it is critically important that datasets be constructed for the language that are regionally- and culturally-localized." |
| Q8 | 1 | output_content | "Fajri Koto, Haonan Li, Sara Shatnawi, Jad Doughman, Abdelrahman Boda Sadallah, Aisha Alraeesi, Khalid Almubarak, Zaid Alyafeai, Neha Sengupta, Shady Shehata, Nizar Habash, Preslav Nakov, Timothy Baldwin" |
| Q9 | 1 | output_content | "Department of Natural Language Processing, MBZUAI; Prince Sattam bin Abdulaziz University; King Fahd University of Petroleum and Minerals; Core42; New York University Abu Dhabi; The University of Melbourne" |
| Q10 | 1 | input_ontology | "The evaluation of language models has increasingly shifted from linguistically-centric tasks, such as part-of-speech (POS) tagging and named entity recognition (NER), towards reasoning and knowledge evaluation." |
| Q11 | 2 | input_content | "Early Arabic pretrained language models typically had less than 2 billion parameters and were primarily monolingual." |
| Q12 | 2 | input_ontology | "These models can be classified into three main categories: encoder-only, decoder-only, and encoder–decoder models." |
| Q13 | 2 | output_content | "The encoder-only models, such as AraBERT (Antoun et al., 2020), CAMeLBERT (Inoue et al., 2021), AraELECTRA (Antoun et al., 2021a), and ARBERT & MARBERT (Abdul-Mageed et al., 2021), are mainly from the BERT family." |
| Q14 | 2 | output_content | "AraGPT2 (Antoun et al., 2021b), on the other hand, is a decoder-only model available in different sizes ranging from 135M to 1.4B parameters." |
| Q15 | 2 | output_content | "Examples of encoder–decoder models include AraT5 (Nagoudi et al., 2022) and AraBART (Kamal Eddine et al., 2022)." |
| Q16 | 2 | output_content | "Jais (Sengupta et al., 2023) and AceGPT (Huang et al., 2023) are two recent Arabic-centric decoder-only models with parameter sizes of up to 30B and 13B, respectively." |
| Q17 | 2 | input_content | "Jais is pretrained on a corpus of 72 billion Arabic tokens, while AceGPT builds upon LLaMA2 and is enhanced with reinforcement learning from AI feedback (Lee et al., 2023) to localize the model to Arabic values and culture." |
| Q18 | 2 | output_content | "Both models are bilingual (English and Arabic), and were fine-tuned on various instruction datasets." |
| Q19 | 2 | input_content | "Arabic is also present in multilingual models." |
| Q20 | 2 | output_form | "This includes earlier models such as mBERT (Devlin et al., 2019) and XLM-R (Conneau et al., 2020), and more recent LLMs such as BLOOMZ (Muennighoff et al., 2022), mT0 (Muennighoff et al., 2022), Falcon (Penedo et al., 2023), GPT-3.5 (Ouyang et al., 2022), and GPT-4 (OpenAI, 2023)." |
| Q21 | 2 | output_form | "In the original papers, only GPT-4 was evaluated in Arabic in terms of its reasoning and knowledge capabilities, using the English–Arabic translated MMLU dataset, reporting an accuracy of 80%." |
| Q22 | 2 | input_content | "Arabic is included in various multilingual benchmarks for natural language understanding and generation, such as XGLUE (Liang et al., 2020), XTREME (Hu et al., 2020), XTREME-R (Ruder et al., 2021) and GEM (Gehrmann et al., 2021)." |
| Q23 | 2 | input_content | "In recent years, several Arabic-centric benchmarks have been released, such as Dolphin (Nagoudi et al., 2023), OCRA (Elmadany et al., 2023), and LAraBench (Abdelali et al., 2024)." |
| Q24 | 2 | input_ontology | "Many tasks in these benchmarks involve classification, such as natural language." |
| Q25 | 3 | input_ontology | "ArabicMMLU is an Arabic multiple-choice question-answering dataset comprising 40 tasks spanning a wide range of subjects and education levels." |
| Q26 | 3 | input_content | "The questions are sourced from eight different countries in North Africa (Morocco and Egypt), the Levant (Jordan, Palestine, and Lebanon), and the Gulf (UAE, Kuwait, and KSA)." |
| Q27 | 3 | output_ontology | "Each question has 2–5 candidate answers, with one correct answer." |
| Q28 | 3 | input_ontology | "The subjects are drawn from different education levels (primary school, middle school, and KSA, prioritize Islamic studies alongside subjects like mathematics, natural science, social science, and geography." |
| Q29 | 3 | input_form | "In public schools, Arabic is commonly used for teaching and assessment, while in international schools, English is the predominant language of instruction for most subjects, following either the UK or USA curriculum." |
| Q30 | 3 | input_form | "When designing ArabicMMLU, we excluded questions in English and only included questions in Arabic." |
| Q31 | 4 | output_content | "The data construction process involved a total of 10 Arabic native speakers from different countries: 6 internal workers (1 Jordanian, 1 Egyptian, 1 Lebanese, 1 from UAE, and 2 from KSA) and 4 external workers (3 Jordanian and 1 Egyptian)." |
| Q32 | 4 | input_content | "During the first stage of data collection, the internal workers were tasked with collecting relevant sources for data collection. These sources were URLs containing the questions, which needed to be publicly available." |
| Q33 | 4 | input_content | "In the second stage, all workers were asked to manually scrape the data within a 2-month period. The task was to collect metadata, including the source (URL of the source document), country, subject, level, question, multiple-choice options, and the correct answer key." |
| Q34 | 4 | input_content | "Each external worker was assigned to gather 2,000 questions, while internal workers were tasked with gathering 1,000–2,000 questions each." |
| Q35 | 4 | output_content | "Our internal workers are Master's students and Research Assistants in Computer Science, while the external workers hold Bachelor's degrees." |
| Q36 | 4 | output_content | "We ensured competitive compensation for the workers, exceeding the monthly average wage in each respective country." |
| Q37 | 4 | input_form | "During manual data scraping, workers were instructed to include only questions accompanied by an answer key, and to discard questions containing multi-modal information (e.g., images, videos, or tables)." |
| Q38 | 4 | input_form | "If a question had additional contextual information (e.g., a passage referenced by several questions), the context was required to be included with each corresponding question." |
| Q39 | 4 | output_content | "While our workers are native speakers of Modern Standard Arabic with at least Bachelor's degrees, we maintain the quality of our dataset construction through meticulous steps." |
| Q40 | 4 | output_content | "Firstly, we conducted a 1-hour workshop before the data collection stage to clarify the process." |
| Q41 | 4 | input_content | "Secondly, we automatically filtered out repetitive questions and those without an answer key, reducing the initial set of over 15,000 questions to 14,575 unique questions." |
| Q42 | 4 | output_content | "Finally, we assessed the accuracy of our data collection by having two native Arabic speakers annotate 100 randomly sampled questions. They were provided with all metadata, including the answer key, and tasked with verifying the correctness of each sample using any available resources (e.g., search engines)." |
| Q43 | 4 | output_content | "We found that 96% of the questions and answer keys match on average, while the remaining could have incorrect answer keys." |
| Q44 | 4 | output_content | "This 96% score is considered to represent the maximum score meaningfully achievable for ArabicMMLU." |
| Q45 | 5 | output_form | "Our experiments focus on zero-shot and few-shot settings across 35 models." |
| Q46 | 5 | output_form | "This includes 22 open-source multilingual models (XGLM (Lin et al., 2022), BLOOMZ (Muennighoff et al., 2022), mT0 (Muennighoff et al., 2022), Falcon (Penedo et al., 2023), and LLaMA2 (Touvron et al., 2023), across various sizes), 11 open-source Arabic-centric models (AraT5 (Nagoudi et al., 2022), AraGPT2 (Antoun et al., 2021b), AceGPT (Huang et al., 2023) and Jais (Sengupta et al., 2023), also across various sizes), and 2 closed-source models (GPT-3.5: gpt-3.5-turbo (Ouyang et al., 2022) and GPT-4: gpt-4-0613 (OpenAI, 2023))." |
| Q47 | 5 | output_form | "We initially conducted experiments with four settings: (1) Arabic prompt and Arabic alphabetic output, (2) Arabic prompt and English (i.e. Latin script) alphabetic output, (3) English prompt and Arabic alphabetic output, and (4) English prompt and English alphabetic output." |
| Q48 | 5 | input_form | "Figure 4 illustrates the Arabic and English prompts." |
| Q49 | 5 | input_form | "The placeholders [SUBJECT], [LEVEL], and [COUNTRY] are replaced with the corresponding Arabic and English words, while the placeholders [INPUT] and [OPTION] are in Arabic." |
| Q50 | 6 | output_form | "Following previous studies (Koto et al., 2023; Li et al., 2023), for open-source models, we determine the answer based on the highest probability among all possible options." |
| Q51 | 6 | output_form | "In the case of English alphabetic output, we measure the probability of the first generated token being A, B, C, D, or E." |
| Q52 | 6 | output_form | "For Arabic, we measure the probability of the first generated token being @, H., h., X, or è." |
| Q53 | 6 | output_form | "For closed-source models, we determine the answer based on the first token generated in the text using a regular expression." |
| Q54 | 6 | output_form | "If there is no match, we assign a random answer." |
| Q55 | 6 | output_form | "To evaluate the influence of prompt language, we initially benchmarked the open-source models using all four prompt settings (Section 4.1), as depicted in Figure 5." |
| Q56 | 6 | output_form | "We observe that the optimal configuration across all models is to use an English prompt and English alphabetic output." |
| Q57 | 6 | output_form | "Predictably, the Arabic-specific LLMs — Jais-chat (30B) and AceGPT-chat (13B) — demonstrate the greatest robustness when employing Arabic alphabetic output." |
| Q58 | 6 | output_form | "For the remaining experiments, we will report based on the setting of English prompt and English alphabetic output." |
| Q59 | 7 | output_form | "As expected, the Arabic-centric model Jais-chat (30B) emerges as the top-performing open-source model, boasting an average score of 62.3%, surpassing GPT-3.5 by 4.6 points." |
| Q60 | 7 | output_form | "Compared to AceGPT-chat (13B), both Jais-chat models (13B and 30B) exhibit substantially higher accuracy in areas including STEM, Social Science, Humanities, and Others." |
| Q61 | 7 | output_form | "For multilingual models such as BLOOMZ (7B) and mT0 (13B), their performance lags behind Jais, with a disparity of more than 14 points." |
| Q62 | 7 | output_form | "XGLM, LLaMA2, and Falcon perform at a level close to random, suggesting their limited proficiency in Arabic." |
| Q63 | 7 | output_form | "GPT-4 achieves the highest accuracy, with a score of 72.5%, surpassing Jais-chat (30B) by 10 points." |
| Q64 | 7 | input_content | "It is noteworthy that in the GPT-4 technical report (OpenAI, 2023), the accuracy of the English-Arabic translated MMLU dataset is reported as 80%, which is 8 points higher than our ArabicMMU results." |
| Q65 | 7 | input_content | "One possible explanation for this difference is that our ArabicMMU presents a greater challenge due to its inclusion of a higher proportion of Arabic-specific content." |
| Q66 | 7 | output_form | "Furthermore, we notice a trend of increasing accuracy with larger models, with the exception of XGLM." |
| Q67 | 7 | output_form | "For example, BLOOMZ (7B) achieves an accuracy 15.9 points higher than BLOOMZ (560M), while mT0 (13B) shows a 13.8-point increase compared to mT0 (300M)." |
| Q68 | 7 | input_ontology | "We observe that ArabicMMU questions are more challenging at the high school level compared to the primary and middle school levels." |
| Q69 | 7 | output_form | "Specifically, for high school questions, GPT-4 achieves a score of only 61.7%, while Jais-chat scores 51.2%." |
| Q70 | 7 | output_form | "Interestingly, we notice that the model accuracy at the university level is higher than for high school." |
| Q71 | 7 | input_ontology | "This could be attributed to the relatively small portion (i.e., 6%) of university-level questions in ArabicMMU, which potentially skews the results." |
| Q72 | 7 | input_ontology | "We present the performance of open-source models on selected subjects that potentially contain Arabic-specific contexts." |
| Q73 | 7 | input_ontology | "These subjects include history, geography, civics, political" |
| Q74 | 8 | output_form | "We focus our more detailed analysis in this section solely on the best open-source models, namely BLOOMZ, AceGPT, and Jais, providing researchers and the community with insights to better understand these models and opportunities for future improvements." |
| Q75 | 8 | output_form | "While all the results in Section 4.2 were based on zero-shot learning, we observe in Figure 7 that when we move to few-shot learning, results for base models improve but those for instruction-tuned models deteriorate." |
| Q76 | 8 | output_form | "Specifically, AceGPT and Jais show an improvement of 2–10 points when using few-shot learning, but the results for BLOOMZ and Jais-chat drop." |
| Q77 | 8 | output_form | "These findings are consistent with prior research over IndoMMIU (Koto et al., 2023) and CMMLU (Li et al., 2023)." |
| Q78 | 8 | output_form | "We analyze whether BLOOMZ, AceGPT, and Jais are well-calibrated in answering ArabicMMLU questions by comparing the probability of the correct answers with the actual accuracy for each task (i.e., subject and level combination)." |
| Q79 | 8 | output_form | "The answer probability is obtained through softmax normalization across the available candidate answers." |
| Q80 | 8 | output_form | "In Figure 8, we observe that the three open-source models are well calibrated with correlation scores r > 0.9." |
| Q81 | 8 | output_form | "Additionally, we investigate the correlation between model confidence and question length in Figure 9." |
| Q82 | 8 | output_form | "We find no correlation between the length of the questions and the model confidence for either Jais or AceGPT." |
| Q83 | 8 | output_ontology | "Despite negation being an absolutely foundational linguistic phenomenon, LLMs have been shown to be worryingly insensitive to its effects in English (Kassner and Schütze, 2020; Hosseini et al., 2021; Truong et al., 2023)." |
| Q84 | 8 | input_ontology | "We thus perform an analysis of LLM performance over questions in ArabicMMLU with and without negation to determine whether this observation ports across to Arabic." |
| Q85 | 8 | input_form | "We utilize specific negation phrases to identify questions containing negations in Arabic." |
| Q86 | 9 | input_ontology | "We introduce ArabicMMLU, the first large-scale multi-task language understanding dataset designed to evaluate real-world knowledge in Arabic." |
| Q87 | 9 | input_content | "Through experiments with over 14K multiple-choice questions spanning various subjects and education levels, we observed that Arabic-centric LLMs outperform multilingual LLMs, albeit with lower accuracy than GPT-4." |
| Q88 | 9 | input_ontology | "For future work, ArabicMMLU can be extended to include short-answer or essay questions, different modalities (i.e., images, audio, video), larger region coverage, and more questions in professional settings." |
| Q89 | 9 | input_content | "ArabicMMLU does not represent all Arabic countries equally. For example, we have collected over 6K multiple-choice questions from Jordan, while other countries are represented with only 100 questions or, in some cases, not at all." |
| Q90 | 9 | input_content | "This is largely due to the availability of publicly-accessible exams in each country; some countries have digitized their exams, but not others." |
| Q91 | 9 | input_content | "Additionally, our search for relevant Arabic content across the internet was not exhaustive." |
| Q92 | 9 | input_form | "The dataset primarily focuses on Modern Standard Arabic (MSA). However, multilingual and Arabic LLMs are often exposed to both MSA and dialectical Arabic." |
| Q93 | 9 | input_form | "ArabicMMLU is focused solely on text-based assessment, and the exploration of multimodal questions is left for future work." |
| Q94 | 9 | output_form | "It is important to emphasize that our experimental results do not provide conclusive answers regarding the performance of LLMs in Arabic." |
| Q95 | 10 | output_content | "to a lack of sufficient information about its training regimen. As such, we cannot assert that the model's pretraining data is free from contamination." |
| Q96 | 10 | input_content | "We extend our gratitude to all collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia who participated in the data collection process." |
| Q97 | 10 | input_content | "We also acknowledge the contributions of Samta Kamboj, Sarah Al Barri, and Onkar Pandit from Core42, who assisted in collecting the Arabic Language question dataset." |
| Q98 | 14 | input_content | "Table 7 presents the distribution of ArabicMMLU data categorized by subject across different education levels." |
| Q99 | 14 | input_form | "Figure 10 illustrates a complete example of prompts used in this study. This example features a Natural Science question with prompts provided in both Arabic and English." |
| Q100 | 14 | output_ontology | "This is a Natural Science question for primary school in Jordan. Select the correct answer!" |
| Q101 | 14 | input_content | "Table 7: The distribution of ArabicMMLU for each subject in different education levels." |
| Q102 | 15 | output_form | "Table 8 presents the detailed zero-shot results across subjects and education levels, while Table 9, Table 10, Table 11 display the results with different prompts and alphabetic outputs (complementing the main result at Table 8)." |
| Q103 | 15 | output_form | "Zero-shot LLM performance (% accuracy) with English prompt and English alphabetic output, for each subject and education level." |
| Q104 | 15 | output_form | "The models are BLOOMZ (7B), AceGPT-chat (13B), Jais-chat (30B), GPT-3.5 (175B), and GPT-4." |
| Q105 | 16 | output_form | "Zero-shot LLM performance (% accuracy) with Arabic prompt and Arabic alphabetic output, combined across subject groups." |
| Q106 | 16 | output_form | ""Average" means the average across all questions in ArabicMMLU." |
| Q107 | 16 | input_ontology | "Table 9 presents results organized by subject groups: STEM, Social Science, Humanities, Arabic Language, and Other." |
| Q108 | 17 | output_form | "Zero-shot LLM performance (% accuracy) with Arabic prompt and English alphabetic output, combined across subject groups." |
| Q109 | 17 | input_ontology | "Table 10: Zero-shot LLM performance (% accuracy) with Arabic prompt and English alphabetic output, combined across subject groups." |
| Q110 | 18 | output_form | "Zero-shot LLM performance (% accuracy) with English prompt and Arabic alphabetic output, combined across subject groups." |
| Q111 | 19 | output_content | "Table 12 lists the sources of pre-trained models used in this study. All models are sourced from Huggingface (Wolf et al., 2020)." |
| Q112 | 19 | output_content | "With the exception of GPT-3.5 and GPT-4, all the models used in this study were sourced from Huggingface (Wolf et al., 2020)." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/abs/2402.12840 |
| WEB-2 | https://arxiv.org/html/2402.12840v1 |
| WEB-3 | https://github.com/mbzuai-nlp/ArabicMMLU |
| WEB-4 | https://huggingface.co/datasets/MBZUAI/ArabicMMLU |
| WEB-5 | https://arxiv.org/abs/2510.24328 |
| WEB-6 | https://arxiv.org/abs/2510.13430 |
| WEB-7 | https://www.pinsentmasons.com/out-law/analysis/gulf-governments-approach-to-ai-regulation |
| WEB-8 | https://blogs.loc.gov/law/2024/12/falqs-ai-regulations-in-the-gulf-cooperation-council-member-states-part-one/ |
| WEB-9 | https://blogs.loc.gov/law/2024/12/falqs-ai-regulations-in-the-gulf-cooperation-council-member-states-part-two/ |
| WEB-10 | https://www.whitecase.com/insight-our-thinking/ai-watch-global-regulatory-tracker-uae |
| WEB-11 | https://www.york.ac.uk/assuring-autonomy/news/blog/ai-regulation-middle-east/ |
| WEB-12 | https://cms.law/en/int/expert-guides/ai-regulation-scanner/kingdom-of-saudi-arabia |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** MBZUAI/ArabicMMLU
**Analysis date:** 2025-01-31
**Examples reviewed:** ~210 examples across 41 configs (5–8 per config)
**Columns shown:** ID, Source, Country, Group, Subject, Level, Question, Context, Answer Key, Option 1–5, is_few_shot
**Columns skipped (media):** None (text-only dataset; Context field is mostly null in sampled examples)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | History (High School) | ID 3049, Jordan | D | "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين: إتمام وحدة الضفتين عام 1950م / رفضه إعطاء اليهود ممراً إلى حائط البراق / دعوة العرب إلى دعم صندوق الأمة الفلسطيني / رفضه معاهدة سايكس بيكو ووعد بلفور رفضاً قاطعاَ" | Jordan HS history question about King Abdullah I's positions on Zionism and Palestine — framed from Jordanian curriculum perspective | IO, IC, OC |
| D2 | Civics (High School) | ID 14526, Jordan | B | "مثّل ______ العرب في مؤتمر الصلح الذي عقده الحلفاء في باريس: ١-الأمير عبدالله بن الحسين / ٢-الأمير فيصل بن الحسين / ٣-الشريف الحُسين بن علي / ٤-الحُسين بن طلال" | Jordan civics HS: who represented Arabs at Paris Peace Conference — Jordanian Hashemite framing | IC, OC |
| D3 | Civics (High School) | ID 14529, Jordan | C | "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨: تحرر البلاد من قيود فك الانتداب" | Jordan civics HS: primary goal of the 1948 Jordanian-British treaty — Jordanian national framing | IC, OC |
| D4 | Civics (Middle School) | IDs 14291–14327 (5 items), Jordan | various | "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952... القوة العربية من تشكيلات الجيش العربي الأردني... عُدل قانون الأحزاب الأردني" | All 5 sampled Civics Middle School items are exclusively about Jordanian political history | IO, IC |
| D5 | Law (Professional) | IDs 4824, 4843, 4880, 4881, 4652, Morocco | B/C/D/E/C | "يبتدئ أجل الاستئناف... من وزير العدل والسلطة الحكومية المكلفة بالدفاع الوطني" | All 5 sampled Law (Professional) items are from Morocco (Moroccan procedural law) | IO, IC |
| D6 | Geography (Middle School) | ID 8055, Jordan | A | "توجد كنيسة سيدة الجبل في ……. عنجرة" | Jordan middle school geography: location of Lady of the Mountain church in Ajloun, Jordan | IC |
| D7 | Geography (High School) | ID 8529, Jordan | D | "محمية طبيعية في الأردن تشرف عليها إدارة مشتركة بين سلطة المنطقة الاقتصادية الخاصة في العقبة ووزارة السياحة والجمعية الملكية لحماية الطبيعة: وادي رم" | Jordan HS geography: Jordan-specific nature reserve question | IC |
| D8 | History (High School) | ID 2819, Jordan | D | "صدر دستور عام 1952 في عهد جلالة الملك: طلال بن عبدالله" | Jordan HS history: which Jordanian king issued 1952 constitution | IC |
| D9 | History (High School) | ID 2716, Jordan | D | "ترمز الكرة الارضية في شعار المملكة الاردنية الهاشمية إلى: انتشار الاسلام" | Jordan HS history: symbolism in the Hashemite Kingdom's emblem | IC |
| D10 | Social Science (Primary School) | ID 5489, Jordan | D | "تشمل الخدمات الطبية الملكية الحكومية العديد من المؤسسات المتخصصة... مستشفى المدينة الطبية" | Jordan primary social science: Jordan Royal Medical Services institutions | IC |
| D11 | Social Science (Primary School) | ID 5481, Jordan | D | "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" | Jordan primary social science: fact about King Talal's reign — Jordan-specific | IC |
| D12 | Economics (High School) | ID 11412, Jordan | C | "ارسال الشكوى عن طريق الموقع الالكتروني للبنك المركزي وهو: www.cbj.gov.jo" | Jordan HS economics: URL of the Central Bank of Jordan — Jordan-institution specific | IC |
| D13 | Economics (High School) | ID 11561, Jordan | B | "نسبة الأردنيين الذين لا يستطيعون الوصول إلى الخدمات المالية الرسمية: 0.67" | Jordan HS economics: Jordan-specific financial inclusion statistic | IC |
| D14 | Islamic Studies (General) | IDs 165, 385, 46, 157, 54 — Country=null | A/D | "من هو النبي الذي علم منطق الطير؟ سليمان عليه السلام / كم مرة اعتمر النبي صلى الله عليه وسلم؟ أربع عمرات" | Pan-Islamic knowledge questions: no country field — factual hadith/Quran questions | IC, IO |
| D15 | Arabic Language (General) | ID 11728, Country=null | B | "يعود تاريخ العرب إلى آلاف السنين... سُمِّيَ العدنانيون بعرب [فراغ]. الشمال" | Pan-Arab ethnolinguistic history reading comprehension — culturally grounded, no country marker | IC |
| D16 | Arabic Language (Grammar) | ID 12626, Country=null | A | "In the following Quranic verse, what is the correct parsing of the word ــكَ" | Grammar question with English question stem — unexpected language mixing in nominally Arabic benchmark | IF |
| D17 | Geography (Middle School) | ID 8136, Palestine | D | "من الجزر المحيطة بقارة أقيانوسيا: نيوزيلندا / تسمانيا / سلمن / جميع ما ذكر" | Palestine middle school geography: world geography (Oceania islands) — no regional specificity | IC |
| D18 | Geography (Middle School) | ID 8064, Palestine | C | "جمع ما يلي من عناصر الدولة عدا: الشعب / الاقليم / الاحتلال / السيادة" | Palestine MS geography: elements of a state — "occupation" appears as a distractors option | OC |
| D19 | History (Middle School) | ID 2641, Palestine | A | "العلم الذي يبحث في حركات ومواقع النجوم والكواكب: الفلك" | Palestine MS history: astronomy definition — not politically sensitive | IC |
| D20 | Computer Science (Primary School) | IDs 7354–7599, Palestine | various | "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" | Palestine primary CS: binary number systems — STEM, no contested content | IC |
| D21 | Biology (High School) | IDs 9699, 9707, 9834, Palestine | B/B/B | "مقدار تكبير العدسة الزيتية في المجهر الضوئي هو: X100 / إحدى العضيات التالية مسئولة عن تصنيع الليبيدات في الخلية: الشبكة الاندوبلازمية الملساء" | Palestine HS biology: standard cellular biology — culturally neutral STEM | IC |
| D22 | Accounting (University) | IDs 7185–7245, Egypt | A/B | "يفترض أسلوب المراجعة حول الحاسب أنه إذا كانت المدخلات سليمة... فإن عملية التشغيل تكون سليمة بالتبعية: صح" | Egypt university accounting — auditing/financial statements questions | IO |
| D23 | Management (University) | IDs 6174–6175, Egypt | B/C | "درجتة تهييتع الدتلطة بتين الألتخاص... تذتير إلى: ال مركز ة" | Severely garbled OCR text making question almost illegible | IC, OC |
| D24 | Political Science (University) | IDs 7008, 7024, Egypt | D | "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ: كل ما سبق" | Egypt university political science with severe OCR corruption — content partially unreadable | IC, OC |
| D25 | Civics (High School) | ID 14546, Jordan | B | "الدول التي سعت الى اقامة مجلس التعاون الخليجي هي (الامارات العربيه المتحده، قطر، عُمان، اليمن، العراق): لا" | Jordan civics HS: false claim about GCC founding states — correct answer is "No" since Yemen and Iraq were not founders | IO, OC |
| D26 | Driving Test | IDs 687, 695, UAE; 1025, Lebanon; 806, 798, Egypt | various | "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر" | Driving test questions from UAE, Lebanon, Egypt — practical/regulatory, not school-curriculum history/geography | IO |
| D27 | General Knowledge (Primary School) | ID 4381, Jordan | B | "برغي سن الصاج هو: مسمار لولبي الشكل مسلوب من نهايته" | Jordan primary GK: sheet metal screw definition — vocational/practical knowledge | IO |
| D28 | General Knowledge (Middle School) | ID 4556, Jordan | A | "الشامل الأكاديمي يمثل: الأدبي" | Jordan middle school GK: Jordanian academic track system — Jordan-specific educational structure | IC |
| D29 | Arabic Language (Grammar) | ID 12655, Country=null | D | "في الآية القرآنية ﴿إنَّ الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحاتِ﴾، ما هو الإعراب الصحيح لكلمة إنَّ: حرف توكيد ونصب" | Arabic grammar parsing using Quranic verse — MSA grammar directly relevant to deployment | IF |
| D30 | History (High School) | ID 2827, Jordan | A | "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة... القيام بشعائر الأديان" | Jordan HS history/civics: Jordanian constitution rights — Jordan-specific legal framing | IC, OC |
| D31 | Islamic Studies (High School) | ID 14064, Jordan | E | "للتفكير آثار إيجابية عدة: جميع ما ذكر" | Jordan HS Islamic studies: positive effects of thinking (Islamic values framing) — presented as school subject | IC |
| D32 | Social Science (Middle School) | ID 5261, Country=null | D | "أنعم الله على بلادنا العربية بثروات كبيرة من النفط والغاز الطبيعي... يرجع السبب في ذلك إلى: توافره بكميات قليلة" | Pan-Arab social science MS: Arab world natural resources | IC |
| D33 | Geography (Primary School) | ID 7848, Jordan | A | "يمتد الوطن العربي في قارتي: آسيا وأفريقيا" | Jordan primary geography: Arab world spans Asia and Africa — broad pan-Arab framing | IC |
| D34 | History (Primary School) | ID 2437, Jordan | D | "يثرب هو الاسم القديم ل: المدينة المنورة" | Jordan primary history: ancient name of Medina — Islamic history, factual | IC |
| D35 | Arabic Language (General) | ID 12069, Country=null | B | "لا يمكن أنْ يصلي المسلم [فراغ]: بدون وضوء" | Arabic language reading with Islamic ritual context — assumes Muslim reader perspective | IC |
| D36 | Computer Science (University) | IDs 7262–7303, KSA | C/A/B/A | "جميع البرامج التالية تعتبر من التطبيقات باستثناء: نظام التشغيل" | KSA university CS: basic computer science concepts — confirmed KSA source | IO |
| D37 | Geography (Middle School) | ID 8058, Jordan | C | "يوجد متحف التاريخ الطبيعي في: نيويورك" | Jordan MS geography: Natural History Museum location — answer is New York, not the primary one | OC |
| D38 | Natural Science (Middle School) | IDs 1902, 1865 — Country=null | C/B | "قام أحمد بحرق كمية من الماغنيسيوم بالمختبر؛ أي المعادلات التالية تصف التفاعل الذي حصل؟ الماغنيسيوم + أكسجين -> أكسيد الماغنيسيوم" | Natural science MS: chemistry reactions — country-neutral STEM | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Authentic school-curriculum framing directly matches deployment knowledge scope
- **Dimension(s):** IO, IC
- **Observation:** The benchmark is genuinely sourced from national school exam materials, not translated from English. Subjects directly relevant to the deployment — history, geography, civics, Arabic language, Islamic studies, and social science — appear across multiple levels and multiple countries. The sampled data confirms subject labels match the deployment's "school-curriculum level" scope.
- **Deployment relevance:** Tourists seeking educational-level knowledge about Arab history, geography, and language will encounter exactly the types of questions the benchmark tests. This supports construct validity for the core knowledge-testing use case.
- **Datapoint citations:**
  - [D1] History (High School), ID 3049, Jordan, label=D: "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" — Modern Arab history question at HS level, directly in-scope for deployment
  - [D15] Arabic Language (General), ID 11728, null, label=B: "يعود تاريخ العرب إلى آلاف السنين... سُمِّيَ العدنانيون بعرب [فراغ]. الشمال" — Reading comprehension about Arab ethnolinguistic history at appropriate level
  - [D33] Geography (Primary School), ID 7848, Jordan, label=A: "يمتد الوطن العربي في قارتي: آسيا وأفريقيا" — Basic Arab world geography, school-level

#### Strength 2: Palestine confirmed as top-3 source country with substantial curriculum content
- **Dimension(s):** IO, IC
- **Observation:** Multiple samples confirm Palestinian-sourced questions exist across subjects: Biology (high school, multiple items), Computer Science (primary, 5+ items), Math (primary), Physics (high school), Geography (middle school), Social Science (primary), Arabic Language (primary school). This is a stronger regional representation than anticipated by the benchmark YAML's uncertainty.
- **Deployment relevance:** Palestine is a deployment country, and its curriculum content is substantively represented. For STEM and language subjects, Palestinian curriculum questions appear consistent with pan-Arab academic content and do not differ from Jordanian content in ways that would cause validity problems.
- **Datapoint citations:**
  - [D21] Biology (High School), IDs 9699/9707/9834, Palestine, label=B/C/B: "مقدار تكبير العدسة الزيتية في المجهر الضوئي هو: X100" — Palestinian HS biology is standard STEM content
  - [D20] Computer Science (Primary School), IDs 7354–7599, Palestine: "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" — Palestinian primary CS questions
  - [D17] Geography (Middle School), ID 8136, Palestine, label=D: "من الجزر المحيطة بقارة أقيانوسيا: جميع ما ذكر" — Palestinian geography content is globally framed, not locally contested

#### Strength 3: Morocco is present with country-specific legal/professional content
- **Dimension(s):** IO, IC
- **Observation:** The Law (Professional) config consists entirely of Morocco-sourced questions in the sample (all 5 examples, Country=Morocco), drawn from Moroccan procedural law. This confirms Morocco has substantive, country-specific representation in at least one subject area. The legal language is distinctly Moroccan in register and references Moroccan legal institutions.
- **Deployment relevance:** Morocco is a flagged coverage gap in the deployment context. Finding authentic Moroccan-sourced content confirms the country is not entirely absent, though its coverage is concentrated in a subject area (professional law) that is out of scope for the tourist/expat school-knowledge use case.
- **Datapoint citations:**
  - [D5] Law (Professional), ID 4824, Morocco, label=E: "يتم استدعاء الشهود بأحد الطرق التالية... الطريقة الإدارية / جميع الأجوبة صحيحة" — Moroccan procedural law question with five options, distinctly Moroccan legal framing
  - [D5] Law (Professional), ID 4652, Morocco, label=C: "من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" — Moroccan "Gendarmerie Royale" ("الدرك الملكي") referenced — culturally distinctive Moroccan institutional name

#### Strength 4: MSA text-only format aligns with deployment's text modality requirement
- **Dimension(s):** IF
- **Observation:** All sampled questions are in Modern Standard Arabic (Arabic script), text-only, with clear question–option structure. There are no images, audio, or multimodal elements in any sampled example. Contextual passages where present (e.g., Arabic Language General config) are also in MSA prose. The format is consistent across all 41 configs.
- **Deployment relevance:** The deployment is text-only and targets MSA-using Arabic learners. The benchmark's uniform MSA text format matches the interaction modality.
- **Datapoint citations:**
  - [D29] Arabic Language (Grammar), ID 12655, null, label=D: "في الآية القرآنية ﴿إنَّ الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحاتِ﴾، ما هو الإعراب الصحيح لكلمة إنَّ: حرف توكيد ونصب" — Clear MSA grammar question, text-only
  - [D15] Arabic Language (General), ID 11728, null, label=B: full passage in MSA prose about Arab history with comprehension question — demonstrates passage-based reading in MSA

#### Strength 5: Broad multi-subject taxonomy across education levels confirmed in data
- **Dimension(s):** IO
- **Observation:** The sampled data confirms 40 distinct tasks are genuinely populated with level-appropriate content: primary school questions are simpler (e.g., basic arithmetic, vocabulary, animal facts), middle school questions involve more abstract concepts, and high school questions involve analytical reasoning. The taxonomy covers STEM, Humanities, Social Science, Language, and Other as labeled.
- **Deployment relevance:** The broad level distribution allows assessment of whether a system can handle the full range of school-curriculum knowledge a tourist might ask about — from basic facts to higher-level concepts.
- **Datapoint citations:**
  - [D38] Natural Science (Middle School), ID 1902, null, label=C: "قام أحمد بحرق كمية من الماغنيسيوم بالمختبر؛ أي المعادلات التالية تصف التفاعل الذي حصل؟" — Level-appropriate chemistry content
  - [D22] Accounting (University), ID 7245, Egypt, label=A: "يفترض أسلوب المراجعة حول الحاسب أنه إذا كانت المدخلات سليمة..." — University-level auditing/IT question
  - [D34] History (Primary School), ID 2437, Jordan, label=D: "يثرب هو الاسم القديم ل: المدينة المنورة" — Primary-level Islamic history fact

#### Strength 6: KSA content confirmed through university-level source URLs
- **Dimension(s):** IO, IC
- **Observation:** The Computer Science (University) config is sourced entirely from KSA (King Saud University: `faculty.ksu.edu.sa`), confirming KSA's presence in at least the STEM university tier. Saudi internal workers are also represented in the annotator pool per the documentation.
- **Deployment relevance:** KSA is a deployment country. The presence of KSA-sourced university STEM questions confirms some Gulf coverage in the benchmark.
- **Datapoint citations:**
  - [D36] Computer Science (University), ID 7280, KSA, label=C: "الكمبيوتر الدقيق هو عبارة عن: جهاز الكمبيوتر المكتبي" — Sourced from `faculty.ksu.edu.sa`, confirming KSA institutional sourcing

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Output form is entirely MCQ — cannot evaluate multi-perspective acknowledgment required by deployment
- **Dimension(s):** OO, OF
- **Observation:** Every single sampled example uses a single-correct-answer MCQ format (options A–E, one labeled correct). Contested historical and civic questions — such as the question about King Abdullah I's positions on Zionism [D1], or the Jordanian-Palestinian political questions [D2, D3] — are all assigned a single "correct" answer from the Jordanian curriculum perspective. The benchmark cannot evaluate whether a system acknowledges competing Palestinian, Egyptian, or pan-Arab framings of the same events.
- **Deployment relevance:** The deployment explicitly requires the system to "acknowledge multiple perspectives and note that different countries hold different positions." This is the most critical structural mismatch: the benchmark scores only factual recall within one curriculum's framing, not pluralistic or explanatory responses.
- **Datapoint citations:**
  - [D1] History (High School), ID 3049, Jordan, label=D: "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" — A question about Jordanian/Palestinian political history has a single Jordanian-curriculum correct answer, with no mechanism to flag that Palestinian perspectives may frame this history differently
  - [D25] Civics (High School), ID 14546, Jordan, label=B: "الدول التي سعت الى اقامة مجلس التعاون الخليجي هي (الامارات العربيه المتحده، قطر، عُمان، اليمن، العراق): لا" — True/false about GCC founding — correct answer is "No" but only one national framing is tested
  - [D18] Geography (Middle School), ID 8064, Palestine, label=C: "جمع ما يلي من عناصر الدولة عدا: الشعب / الاقليم / الاحتلال / السيادة" — "Occupation" (الاحتلال) appears as a distractor for "elements of a state" — a politically loaded framing that receives a single correct answer without any acknowledgment of the contested status of Palestinian statehood

#### CRITICAL Concern 2: Civics content is overwhelmingly Jordan-specific, not pan-Arab or multi-country
- **Dimension(s):** IO, IC
- **Observation:** All 5 sampled Civics (Middle School) items are exclusively about Jordanian political institutions, Jordanian government history, and Jordanian party law. All 5 sampled Civics (High School) items are also Jordan-centric (Jordanian society, Arab Cooperation Council from Jordanian perspective, Jordanian-British treaty). This confirms the Jordan-skew documented in the YAML extends to the civics domain, which is the most sensitive for the multi-perspective deployment requirement.
- **Deployment relevance:** For tourists in any of the other seven deployment countries (Morocco, Egypt, Palestine, Lebanon, UAE, Kuwait, KSA), civics questions about Jordanian government structures, Jordanian army formations, and Jordanian party law have minimal relevance. More critically, a system trained or evaluated on these civics items may produce Jordanian-framed answers to generic Arab civics questions asked by users in other countries.
- **Datapoint citations:**
  - [D4] Civics (Middle School), IDs 14291–14327, Jordan: "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952 وقد عرفت باسم الحكومة: الوطنية" / "القوة العربية من تشكيلات الجيش العربي الأردني في المرحلة: الأولى" / "عُدل قانون الأحزاب الأردني حيث جاء فيه ألا يقل عدد المؤسسين للحزب عن (500) عضو عام: 2007" — All five civics MS items are Jordanian-specific
  - [D2] Civics (High School), ID 14526, Jordan, label=B: "مثّل ______ العرب في مؤتمر الصلح الذي عقده الحلفاء في باريس: الأمير فيصل بن الحسين" — Presents Hashemite framing of pan-Arab representation without acknowledging other national narratives
  - [D3] Civics (High School), ID 14529, Jordan, label=C: "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨" — Highly Jordan-specific political history content

#### MAJOR

#### MAJOR Concern 3: Jordanian-curriculum framing in contested history questions risks annotation bias
- **Dimension(s):** IC, OC
- **Observation:** The history content sampled is heavily Jordanian in framing. The question about King Abdullah I and Zionism [D1] presents the Jordanian narrative as the sole "correct" answer. The question about the 1952 Jordanian constitution [D8] and Hashemite emblem symbolism [D9] treats Jordan-specific historical facts as the authoritative framing. Since no Palestinian annotators verified Palestinian-sourced questions, and the civics sample confirms Jordan-centric framing, the benchmark's ground-truth for contested historical events may reflect Jordanian national consensus rather than pan-Arab or Palestinian perspectives.
- **Deployment relevance:** A system evaluated well on these items might give Jordanian-framed answers to tourists in Palestine, Lebanon, or Morocco who ask about shared historical events. The deployment requires explicit flagging of country-specific perspectives, but the benchmark labels do not encode this requirement.
- **Datapoint citations:**
  - [D1] History (High School), ID 3049, Jordan, label=D: "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين: رفضه معاهدة سايكس بيكو ووعد بلفور رفضاً قاطعاً" — The "correct" answer (he did NOT reject Balfour unequivocally) reflects Jordanian historical consensus that may be contested by Palestinian historiography
  - [D30] History (High School), ID 2827, Jordan, label=A: "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة... القيام بشعائر الأديان" — Jordanian constitutional framing of religious freedom rights
  - [D11] Social Science (Primary School), ID 5481, Jordan, label=D: "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" — Jordanian royal history presented as school-level social science

#### MAJOR Concern 4: Kuwait is effectively absent from the sampled data
- **Dimension(s):** IO, IC
- **Observation:** Across all 41 sampled configs (approximately 210 examples), no single example has Country=Kuwait. The web search findings confirm Kuwait is absent from the country-grouped model performance table in the paper, and no Kuwaiti collaborators are acknowledged. This absence is confirmed in practice by the sampled data.
- **Deployment relevance:** Kuwait is one of the eight deployment countries. Any system evaluated on ArabicMMLU will have essentially no Kuwaiti curriculum exposure in its evaluation, meaning the benchmark cannot assess whether the system handles Kuwait-specific school knowledge appropriately.
- **Datapoint citations:**
  - Zero instances of Country=Kuwait across all 210 sampled examples — absence constitutes the evidence; no positive citations possible

#### MAJOR Concern 5: OCR/digitization quality issues create illegible questions in some university-level items
- **Dimension(s):** IC, OC
- **Observation:** Multiple university-level items from Egyptian sources show severe OCR corruption that renders question text partially or wholly illegible. Characters are scrambled, words are unreadable, and answer options contain garbled text. This affects at least the Management (University) and Political Science (University) configs and potentially others.
- **Deployment relevance:** A system that answers OCR-corrupted questions "correctly" is exploiting noise rather than demonstrating knowledge. Benchmark scores on corrupted items have no validity for the deployment's knowledge-testing purpose. The 96% answer-key accuracy ceiling documented in the YAML may be overestimated for university-level Egyptian content.
- **Datapoint citations:**
  - [D23] Management (University), ID 6175, Egypt, label=C: "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة فتى السشمستة تذتير إلى: ال مركز ة" — Severely corrupted OCR; question is unreadable without reconstruction
  - [D24] Political Science (University), ID 7008, Egypt, label=D: "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ: كل ما سبق" — OCR corruption throughout; answer options also corrupted

#### MAJOR Concern 6: Morocco's curriculum representation is limited to professional law, absent from school-curriculum subjects
- **Dimension(s):** IO, IC
- **Observation:** While Morocco appears in the Law (Professional) config (all 5 sampled items), no Morocco-sourced questions were found in the school-curriculum subjects (History, Geography, Civics, Social Science, Islamic Studies, Arabic Language) across the sampled data. The Moroccan legal questions reference Moroccan legal procedure and institutions, but the deployment requires school-curriculum knowledge (history, geography, Arabic language), which is where Moroccan curriculum distinctiveness (Maghrebi historical framing, French-influenced educational tradition) would matter most.
- **Deployment relevance:** Tourists visiting Morocco and asking about Moroccan history, geography, or civic life will encounter questions where the benchmark provides no Moroccan-curriculum grounding. A system evaluated only on Jordanian and Egyptian history framing may produce non-Moroccan answers to Moroccan historical questions.
- **Datapoint citations:**
  - [D5] Law (Professional), IDs 4824/4843/4880/4881/4652, Morocco: All five Morocco-sourced samples are procedural law items — none are from history, geography, or school-level curricula
  - [D4] Civics (Middle School), IDs 14291–14327, Jordan: All five civics MS items are Jordan-only — confirms Morocco's absence from this high-priority subject category

#### MAJOR Concern 7: Islamic Studies content assumes internal Muslim religious perspective, not external educational framing
- **Dimension(s):** IC, OC
- **Observation:** The Islamic Studies questions (at all levels) are framed as internal religious knowledge questions — asking about the number of Prophet Muhammad's Umrah pilgrimages, which Quranic surah contains specific stories, and prescribed Islamic ritual practice. The Arabic Language (General) config uses a reading passage that frames Islamic purification practices prescriptively ("لا يمكن أنْ يصلي المسلم بدون وضوء"). These are presented as school-curriculum content for Muslim students, not as culturally informative questions for non-Muslim visitors.
- **Deployment relevance:** The deployment's target population are non-native, non-Arab tourists and expats, many of whom may be non-Muslim. A system evaluated on these items is tested for its ability to reproduce internal Islamic religious knowledge, not for its ability to explain Islamic practices to a non-Muslim visitor in an appropriately explanatory, non-prescriptive register. The benchmark cannot evaluate whether the system frames Islamic content accessibly for outsiders.
- **Datapoint citations:**
  - [D14] Islamic Studies (General), ID 46, null, label=A: "كم مرة اعتمر النبي صلى الله عليه وسلم؟ أربع عمرات" — Internal Islamic knowledge question presupposing Muslim reader
  - [D35] Arabic Language (General), ID 12069, null, label=B: "لا يمكن أنْ يصلي المسلم [فراغ]: بدون وضوء" — Reading passage frames Islamic ritual as prescriptive instruction ("the Muslim cannot pray without wudu") rather than descriptive/educational
  - [D31] Islamic Studies (High School), ID 14064, Jordan, label=E: "للتفكير آثار إيجابية عدة: جميع ما ذكر" — Islamic studies HS question framing positive thinking within Islamic value framework

#### MINOR

#### MINOR Concern 8: Driving Test questions are out-of-scope for school-curriculum knowledge deployment
- **Dimension(s):** IO
- **Observation:** The Driving Test config includes questions about traffic rules, road safety, and vehicle operation from Egypt, UAE, and Lebanon. These are practical regulatory knowledge items, not school-curriculum knowledge about Arab history, geography, or language.
- **Deployment relevance:** The deployment explicitly scopes to "school-curriculum-level general knowledge (history, geography, Arabic language)" with practical travel knowledge explicitly out of scope. Driving test performance scores are not informative for the tourist knowledge-assistant use case, and including this config in aggregate scoring could dilute or mislead benchmark-to-deployment mapping.
- **Datapoint citations:**
  - [D26] Driving Test, ID 687, UAE, label=A: "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر من مركبتك" — Practical traffic safety rule, not school-curriculum knowledge
  - [D26] Driving Test, ID 1025, Lebanon, label=C: "يُحَظَّر على سائق المركبة: يجري مناورة عكس الإتجاه (Demi Tour) وسط الطريق العام" — Note "Demi Tour" (French term) embedded in Arabic text — reflects Lebanon's French-influenced regulatory register

#### MINOR Concern 9: Some General Knowledge items cover vocational and institutional knowledge irrelevant to tourist context
- **Dimension(s):** IO
- **Observation:** General Knowledge (Primary) and General Knowledge (Middle School) samples include items about sheet metal screws, metal welding, Jordanian Royal Medical Services hospital names, and road safety. These are Jordanian school curriculum items that have no relevance to a tourist or expat seeking knowledge about Arab history and culture.
- **Deployment relevance:** These items contribute to benchmark scores but do not test the specific knowledge domains (history, geography, Arabic language) the deployment targets. High performance on vocational GK does not predict performance on culturally relevant questions.
- **Datapoint citations:**
  - [D27] General Knowledge (Primary School), ID 4381, Jordan, label=B: "برغي سن الصاج هو: مسمار لولبي الشكل مسلوب من نهايته" — Sheet metal screw definition — vocational, not culturally relevant
  - [D10] Social Science (Primary School), ID 5489, Jordan, label=D: "تشمل الخدمات الطبية الملكية الحكومية... مستشفى المدينة الطبية" — Jordanian Royal Medical Services hospitals — Jordan-institutional, not pan-Arab knowledge

#### MINOR Concern 10: One Arabic Language Grammar question has an English question stem
- **Dimension(s):** IF
- **Observation:** In Arabic Language (Grammar), example ID 12626, the question stem is in English: "In the following Quranic verse, what is the correct parsing of the word ـكَ" — while the answer options are in Arabic. This is an unexpected language mix in a benchmark that claims to be exclusively in MSA Arabic (excluding English questions by design).
- **Deployment relevance:** This is a minor data quality observation. The question is answerable in Arabic, but the English stem creates an inconsistency in the input form distribution. For a system tested on purely Arabic inputs, this question introduces a signal that may not represent the benchmark's intended register.
- **Datapoint citations:**
  - [D16] Arabic Language (Grammar), ID 12626, null, label=A: "In the following Quranic verse, what is the correct parsing of the word ـكَ: مضاف إليه مجرور وعلامة جره الكسرة" — English question stem with Arabic answer options; unexpected language mixing

#### MINOR Concern 11: Some Geography items ask about global (non-Arab) facts, reducing regional specificity
- **Dimension(s):** IC
- **Observation:** Several Geography items ask about non-Arab global knowledge: Mt. Kilimanjaro in Tanzania, Shanghai as an industrial smog city, the height of the snow line in equatorial regions, cold ocean currents (West Australia Current). While legitimate world geography content, these do not test Arabic/Arab-regional knowledge specifically.
- **Deployment relevance:** For the deployment's focus on "Arab history and geography," these items have lower diagnostic relevance. However, they do represent the type of factual geography knowledge a tourist might ask about.
- **Datapoint citations:**
  - [D] Geography (High School), ID 8189, Jordan, label=B: "يبلغ ارتفاع جبل كلمنجارو في تنزانيا: 5800 م" — Kilimanjaro altitude — global geography, not Arab-specific
  - [D] Geography (High School), ID 8216, Jordan, label=A: "من المدن الصناعية التي يتكون فيها الضباب الدخاني: شنغهاي" — Industrial smog cities — Shanghai as answer, global content

---

### Content Coverage Summary

The sampled data reveals a benchmark that is predominantly Jordanian in its civics and history domains (all 10 sampled civics items across middle and high school are Jordan-only), moderately represented by Egypt (university-level accounting, economics, political science, philosophy), and more lightly populated by Palestine (strong STEM presence at primary-high school level but minimal contested-history items in the sample), KSA (university STEM), Morocco (professional law only), and Lebanon (driving test). No Kuwait-sourced items appear in any sampled config.

The register is consistently MSA — formal written Arabic appropriate for school examinations — with occasional OCR-corruption artifacts particularly in Egyptian university-level items. One grammar item has an English question stem. The content divides roughly into: (a) culturally neutral STEM items (biology, physics, chemistry, math, computer science) sourced mainly from Jordan and Palestine; (b) Jordanian-centric civic and historical items; (c) pan-Islamic religious knowledge items (Islamic Studies across all levels, pan-Islamic Arabic Language reading texts); (d) Jordanian vocational and institutional items (driving, school tracking, hospital names); and (e) a small Moroccan professional law cluster.

For the deployment's school-curriculum tourist knowledge use case, the most relevant content is in History, Geography, Islamic Studies, Arabic Language, and Social Science. Of these, History and Civics are heavily Jordanian-framed, Geography includes both Jordan-specific and world-geography content, and Islamic Studies presents religious practice as internal knowledge rather than cultural explanation. The Arabic Language configs are well-suited to testing MSA grammar and vocabulary in an educational register.

---

### Limitations

1. **Sample size per config**: Only 5–8 examples per config were available. Some patterns (e.g., complete absence of Kuwait, Morocco's concentration in Law) may be sample artifacts rather than true distributional properties, though they are corroborated by the web search findings.

2. **Country field reliability**: A meaningful number of examples have Country=null (especially in Islamic Studies (General), Natural Science, Physics, Social Science Middle School, and Arabic Language configs). It is not possible from the sample to determine whether null-country items are truly country-agnostic (pan-Arab) or reflect metadata collection gaps.

3. **Contested content not reliably identifiable from MCQ alone**: The most critical deployment concern — whether contested historical questions have ground-truth labels that reflect one national perspective — cannot be fully verified by reading MCQ text alone. Deeper subject-matter analysis by area experts in Palestinian, Moroccan, and pan-Arab historiography would be needed.

4. **Inter-config quality variation**: OCR quality appears to vary substantially across sources. The university-level Egyptian social science items show severe digitization artifacts not visible in primary and middle school Jordanian items. The proportion of corrupted items across the full 14,575-question dataset cannot be estimated from this sample.

5. **Kuwait absence**: The inference that Kuwait is absent or minimally present is based on zero appearances in ~210 sampled examples and the absence from named country lists in the paper. This cannot be ruled out as a sampling artifact without examining the full dataset metadata.

6. **Islamic Studies register analysis**: Whether the Islamic Studies content is presented in an internal-community vs. external-educational register is a judgment call requiring expert review; the sample provides suggestive evidence but not a definitive audit.

