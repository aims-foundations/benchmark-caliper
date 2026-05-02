## Deployment Context

**Use case:** Support foreigners visiting Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, or KSA in answering their general questions
**Target population:** Non-Arab tourists or expats visiting Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, or KSA and have general questions about the Arabic language, history or geography of these countries

# Validity Analysis: mmlu
**Target context:** Non-Arab Tourists and Expats in Eight Arab Countries
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 3 | Moderate gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 2 | Significant gaps | high |
| **Average** | **1.5** | | |

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

MMLU is fundamentally misaligned with this deployment across the four HIGH-priority dimensions (IO, IC, OO, OC). Documentation, web evidence, and dataset analysis converge on a clear finding: MMLU's 57 subjects are anchored in US academic curricula with no dedicated Arab-region content; ground-truth labels reflect US-academic and (in moral_scenarios) explicitly US-2020 framings; and the single-answer MCQ schema is structurally incapable of representing the multi-perspective output behavior required for contested Arab historical and political topics. The two MODERATE-priority dimensions (IF, OF) match deployment modality at the surface (English text) but cannot evaluate the Arabic-learning sub-cohort or open-ended explanatory output. Universal STEM and formal-reasoning content remains usable as a transferable competence baseline, but the core deployment domain — Arab history, regional geography, Arabic language basics, and Islamic religious knowledge — is essentially uncovered.

## Practical Guidance

### What This Benchmark Measures

MMLU can usefully measure transferable academic competence in subjects with no cultural dependence — STEM, formal logic, mathematics — and can serve as a baseline for English-language reading comprehension and MCQ reasoning. It cannot measure the deployment's core constructs: Arab history knowledge, Middle Eastern geography, Arabic language basics, Islamic religious knowledge, or the ability to acknowledge multiple perspectives on contested topics.

### Construct Depth

Construct depth is shallow for the deployment's purpose. The benchmark probes broad academic recall via MCQ but cannot surface (a) regional factual accuracy on Arab content, (b) framing perspective on contested events, (c) calibrated hedging on politically sensitive topics, or (d) Arabic-language competence. Even the calibration evaluation [Q64–Q67], while informative about confidence-accuracy gaps, cannot diagnose region-specific overconfidence patterns documented in CAMeL and MENAValues research [WEB-11, WEB-15].

### What Else You Need

Substantial supplementation is required. For IO and IC: ArabicMMLU [WEB-2] (40 tasks, 8 countries, 14,575 MSA questions) and ILMAAM [WEB-5] (culturally refined with 11-expert annotation). For dialect/IF coverage of the Arabic-learning cohort: DialectalArabicMMLU [WEB-1] (Moroccan, Egyptian, Emirati, Saudi). For OC value alignment across all eight countries: MENAValues [WEB-11]. For Islamic-cultural content: PalmX 2025 [WEB-13] and IslamicMMLU [WEB-14]. None of these supplements solve the OO contested-topic schema gap, which is a confirmed ecosystem-wide gap (FV5) and would require new evaluation methodology (multi-perspective scoring, expert adjudication of contested labels).

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MMLU's 57-subject taxonomy is anchored in US academic curricula with no dedicated Arab history, Middle Eastern geography, Arabic language, or Islamic jurisprudence subjects. Dataset analysis confirms that even subjects nominally relevant to the deployment (high_school_world_history, high_school_geography, global_facts, world_religions) contain little to no Arab-region content in sampled examples. Given IO is rated HIGH priority and the deployment's core domain is precisely what MMLU omits, this is a fundamental construct underrepresentation.

**Strengths:**
- Universal STEM and formal reasoning subjects (mathematics, physics, chemistry, formal logic, computer science) test culturally neutral content valid for any region, including Arab contexts (Strength 1; D1–D43 passim)
- World religions subject nominally covers multiple faith traditions, providing at least a structural slot where Islamic content could appear [Q171]
- History subject claims to span 'a wide range of time periods and geographical locations' [Q41], even if dataset evidence shows minimal Arab-region instantiation

**Checklist:**

- **IO-1**: Required categories per the deployment YAML and elicitation include Arab history (Islamic Golden Age, Ottoman period, modern state formation), regional geography of eight countries, Arabic language basics, Islamic religious knowledge, and pan-Arab cultural background. — _Sources: WEB-2, WEB-5_
- **IO-2**: Yes — MMLU has no dedicated subject for any of these categories. The 57 subjects include high_school_us_history, high_school_european_history, us_foreign_policy, professional_law (US bar exam), but no Arab/MENA equivalents [Q1, Q4, Q37, Q43]; dataset confirms exhaustively (D1, D3, D4, D9–D11). — _Sources: Q1, Q37, Q43, Q169, DATASET-D1, DATASET-D9, DATASET-D22, DATASET-D27_
- **IO-3**: Yes — multiple subjects (high_school_us_history, high_school_government_and_politics, us_foreign_policy, professional_law, human_aging, human_sexuality) are US-institution-specific and contribute construct-irrelevant variance for an Arab-region deployment (D1–D11, D32–D35). — _Sources: DATASET-D1, DATASET-D3, DATASET-D9, DATASET-D11, DATASET-D32, DATASET-D34_
- **IO-4**: Confirmed structural gap: zero dedicated Arab-region subjects out of 57; nominally relevant subjects (global_facts, world_religions, high_school_geography) contain little or no Arab-region content in 5–6 sampled examples each (D22–D28). ArabicMMLU and ILMAAM exist as supplements but are not part of MMLU [WEB-2, WEB-5]. — _Sources: DATASET-D16, DATASET-D17, DATASET-D22, DATASET-D36, WEB-2, WEB-12_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more.' (p.1)
- [Q17] 'We comprehensively evaluate the breadth and depth of a model's text understanding by covering numerous topics that humans are incentivized to learn.' (p.2)
- [Q37] 'Branches of the humanities include law, philosophy, history, and so on (Appendix B).' (p.4)
- [Q43] 'Subject areas include economics, sociology, politics, geography, psychology, and so on.' (p.4)
- [Q169] 'Figure 68: A US Foreign Policy example.' (p.26)

*Web sources:*
- [WEB-2] ArabicMMLU (ACL 2024) provides 14,575 native MSA questions across 40 tasks from Arab school exams — confirming the Arab-region taxonomy MMLU omits
- [WEB-5] ILMAAM (2025) found 'significant cultural misalignments and biases, particularly in sensitive areas like religion and morality' in MMLU-derived Arabic content
- [WEB-12] Survey of Arabic benchmarks notes gaps in coverage of North Africa, Levant, Iraq even within the Arabic NLP ecosystem

*Dataset analysis:*
- DATASET-D1: high_school_government_and_politics is exclusively US constitutional law (First Amendment) — no Arab governance content
- DATASET-D9: us_foreign_policy framed entirely from US perspective (NSC 68 Cold War containment)
- DATASET-D22–D26: global_facts sample contains China, India, Mexico, Congo references but zero Arab countries across five sampled examples
- DATASET-D17–D21: world_religions sample contains Christianity, Jainism, Judaism but no Islamic content in six sampled examples
- DATASET-D27–D28: high_school_geography frames around US religious demographics and Burgess US urban model
- DATASET-D16: only Middle East reference in sampled world_history is a pre-Islamic Sasanian Persian inscription
- DATASET-D36: prehistory mentions Middle East only as cattle domestication origin

</details>

**Information gaps:**
- No published quantitative audit of original English MMLU for Arab-region content proportion across all 15,908 items (FV1)
- Whether the full world_religions set (171 questions) contains Islamic content beyond the sample

**Requires expert verification:**
- Full-set count of Arab-region or Islamic-content questions across world_history, world_religions, global_facts, and miscellaneous subjects

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
All identified MMLU source materials are Anglophone Western institutions (GRE, USMLE, US undergraduate courses, Oxford University Press, Harvard Law Library) [Q23–Q25, Q83, Q85]. No Arab educational systems, regional universities, or Arabic-language curricula are represented. Dataset analysis confirms the moral_scenarios subject explicitly anchors ground truth to 'ordinary moral standards in the US as of 2020' (D12–D14) — a direct cultural-frame conflict for a deployment serving users in Arab countries. Web evidence (CAMeL, MENAValues) empirically confirms LLMs trained on such data exhibit Western/Anglocentric bias in Arab contexts.

**Strengths:**
- Source materials are documented (GRE, USMLE, Oxford Press) [Q24, Q25], enabling provenance audit
- Some non-Western primary sources do appear in world_history (Nkrumah, Sasanian inscription) showing the subject is not exclusively Western European (D16, D37)
- Contamination-mitigation steps documented (questions/answers on separate pages) [Q112] reduce one form of construct-irrelevant variance

**Checklist:**

- **IC-1**: Yes — the deployment requires Arab cultural, geographic, and (for the Arabic-learning sub-cohort) dialectal knowledge. MMLU inputs require almost exclusively US/Western cultural and institutional knowledge (D1–D11, D32–D35). — _Sources: DATASET-D1, DATASET-D6, DATASET-D32_
- **IC-2**: Culturally sensitive content (moral_scenarios) is misaligned: explicitly labeled by 'US standards as of 2020' (D12), conflicting with Arab regional norms on alcohol, gender, and family across all eight deployment countries. — _Sources: DATASET-D12, DATASET-D13, DATASET-D14, WEB-15_
- **IC-3**: Multiple inputs require Western-specific knowledge that does not transfer: US tort/contract law (D6, D8), US Social Security (D32), US ethnic demographics (D33), Burgess concentric zone urban model (D28), US contraceptive statistics (D34). — _Sources: Q24, Q25, Q164, DATASET-D6, DATASET-D28, DATASET-D34_
- **IC-4**: INSUFFICIENT DOCUMENTATION — MMLU paper does not document any regional annotator review. ArabicMMLU and ILMAAM provide separate Arab-annotated supplements [WEB-2, WEB-5] but are external to MMLU.
- **IC-5**: Documented: no Arab educational sources [Q24, Q25]; no Arabic-language content; explicit US moral framing in moral_scenarios [D12]; cross-lingual value shifts empirically demonstrated for Arabic vs. English prompts [WEB-11]. — _Sources: Q23, Q24, Q85, DATASET-D12, WEB-11_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q23] 'The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online.' (p.3)
- [Q24] 'These include practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination.' (p.3)
- [Q25] 'It also includes questions designed for undergraduate courses and questions designed for readers of Oxford University Press books.' (p.3)
- [Q85] 'We also had RoBERTa continue pretraining on approximately 1.6 million legal case summaries using Harvard's Law Library case law corpus case.law' (p.8)
- [Q164] 'Krete is an unmarried taxpayer with income exclusively from wages...' (p.24)

*Web sources:*
- [WEB-15] Naous et al. 2024 (CAMeL) demonstrate multilingual and Arabic monolingual LLMs exhibit bias toward Western entities even when prompted in Arabic
- [WEB-11] MENAValues benchmark documents Cross-Lingual Value Shifts where LLMs respond differently in Arabic vs. English on value-based questions
- [WEB-2] ArabicMMLU draws content from Arab school exams across Jordan, Egypt, Lebanon, UAE, KSA — the source-institution coverage MMLU lacks

*Dataset analysis:*
- DATASET-D12: moral_scenarios explicitly anchors ground truth to 'ordinary moral standards in the US as of 2020'
- DATASET-D6, D8: professional_law content is exclusively US tort/contract law scenarios
- DATASET-D32, D33: human_aging encodes US Social Security and US ethnic demographic categories as ground truth
- DATASET-D34, D35: human_sexuality cites US-specific contraceptive and partner-count statistics as correct answers
- DATASET-D31: business_ethics question on civil society lists Russia, China, Britain — Arab world entirely absent from options

</details>

**Information gaps:**
- Inter-annotator agreement and annotator demographics for MMLU are not documented in the paper
- Specific framing of any 1948 war / Palestinian / Levantine history questions, if present anywhere in MMLU (FV3)

**Requires expert verification:**
- Arab regional expert review of any world_religions Islamic content for framing perspective
- Arab expert review of any Middle East / Ottoman / 20th-century Arab references in world_history

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
MMLU's text-only English MCQ format [Q3, Q56, Q71] matches the deployment's primary interaction modality (English text), which the elicitation rates MODERATE priority. However, the Arabic-learning secondary cohort cannot be evaluated by MMLU at all, and MENAValues research [WEB-11] documents cross-lingual value shifts indicating that English MMLU performance does not predict Arabic-prompt behavior. Format brittleness (e.g., separator-token sensitivity [Q105]) adds modest external-validity concern but is not region-specific.

**Strengths:**
- English text-only MCQ format aligns with the primary user cohort's interaction modality (Strength 2; D6, D7)
- Zero-shot/few-shot evaluation paradigm [Q3] matches the open-domain generalization required for tourist/expat queries (Strength 4)
- Formal English register is appropriate for educated adult tourist/expat users [Q56]

**Checklist:**

- **IF-1**: MMLU is exclusively English text [Q71]; primary deployment interaction is English text — match. Arabic-script and dialect inputs from the secondary cohort are unsupported by MMLU and require separate benchmarking [WEB-1, WEB-2]. — _Sources: Q71, WEB-1, WEB-2_
- **IF-2**: Regional infrastructure not a concern — tourists/expats use standard text-based devices; deployment YAML notes this is not a connectivity gap context.
- **IF-3**: DialectalArabicMMLU [WEB-1] covers Moroccan, Egyptian, Emirati, Saudi dialects (4 of 8 countries) but not Kuwaiti, Jordanian, Palestinian, or Lebanese dialects; format-level dialect sensitivity is unaddressed in MMLU. — _Sources: WEB-1_
- **IF-4**: Form mismatch is moderate: English MCQ matches primary cohort; Arabic-language input form is entirely unevaluated by MMLU. Cross-lingual value shifts [WEB-11] mean MMLU scores cannot be assumed to transfer to Arabic prompts. — _Sources: Q71, WEB-11, DATASET-D6_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings.' (p.1)
- [Q71] 'Existing large-scale NLP models, such as GPT-3, do not incorporate multimodal information, so we design our benchmark to capture a diverse array of tasks in a text-only format.' (p.7)
- [Q56] 'We feed GPT-3 prompts like that shown in Figure 1a... All prompts end with "Answer: ". The model then produces probabilities for the tokens "A," "B," "C," and "D,"' (p.6)
- [Q105] 'If we remove the </s> from the input, accuracy declines by several percentage points.' (p.12)

*Web sources:*
- [WEB-1] DialectalArabicMMLU covers five Arabic dialects (Syrian, Egyptian, Emirati, Saudi, Moroccan) with substantial cross-dialect performance variation
- [WEB-2] ArabicMMLU is the closest available substitute for the Arabic-language secondary cohort (14,575 MSA questions)
- [WEB-11] MENAValues documents Cross-Lingual Value Shifts — same model gives drastically different responses in Arabic vs. English

*Dataset analysis:*
- DATASET-D6, D7: clear, formal English register confirms format match for the primary English-speaking cohort

</details>

**Information gaps:**
- Tourist/expat device interface preferences (mobile vs. desktop) not searchable at required precision (FV10)
- Whether Arabic-learning users predominantly prompt in MSA vs. dialect

**Requires expert verification:**
- Empirical sizing of the Arabic-prompting sub-cohort relative to the English primary cohort

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MMLU's single-answer four-option MCQ schema [Q49, Q56] is structurally incompatible with the deployment's required output behavior — acknowledging multiple perspectives on contested topics (1948 war/Nakba, Western Sahara, Lebanese Civil War, Palestinian statehood, Jerusalem status), per elicitation Q3 and the contested-topics YAML section. Every sampled MMLU example has exactly one labeled correct answer with no mechanism for multi-perspective or uncertainty-flagging responses. The authors note near-random model accuracy on 'morality and law' [Q8, Q14] but do not address the structural taxonomy issue. No identified Arab-focused benchmark uses multi-perspective scoring (FV5). Given OO is HIGH priority, this is a fundamental structural-validity violation.

**Strengths:**
- Difficulty stratification (Elementary/High School/College/Professional) [Q26] does provide useful granularity within the MCQ schema
- Aggregation across four broad clusters (humanities, social sciences, STEM, other) [Q99–Q101] supports diagnostic interpretation

**Checklist:**

- **OO-1**: MCQ A/B/C/D label categories are regionally neutral in form but cannot encode multi-perspective or contested-topic acknowledgment, which the deployment explicitly requires per elicitation Q3. — _Sources: Q49, Q56_
- **OO-2**: Missing categories: no schema slot for 'this is contested,' 'depends on country,' or 'multiple perspectives apply' — required for Palestinian narrative, Western Sahara, Lebanese Civil War, etc. [contested_topics YAML section]. — _Sources: DATASET-D12, DATASET-D9, WEB-11_
- **OO-3**: moral_scenarios schema explicitly encodes 'US standards as of 2020' as the decision rule (D12), a non-regional value framing. — _Sources: DATASET-D12, DATASET-D14_
- **OO-4**: Stakeholder-driven redesign would require moving beyond MCQ entirely; no Arab-focused benchmark using multi-label or open-ended contested-history scoring has been identified (FV5).
- **OO-5**: Documented structural-validity violation: the construct (multi-perspective handling of contested Arab regional topics) cannot be represented in the MMLU output schema; MMLU paper itself flags weak performance on 'human values such as law and morality' [Q14, Q15] without addressing the schema issue. — _Sources: Q8, Q14, Q15, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q49] 'To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks.' (p.5)
- [Q56] 'The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction.' (p.6)
- [Q8] 'Worse, they still have near-random accuracy on some socially important subjects such as morality and law.' (p.1)
- [Q14] 'The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality.' (p.2)
- [Q15] 'This second weakness is particularly concerning because it will be important for future models to have a strong understanding of what is legal and what is ethical.' (p.2)

*Web sources:*
- [WEB-5] ILMAAM identified 'significant cultural misalignments and biases, particularly in sensitive areas like religion and morality' in MMLU-derived content
- [WEB-11] MENAValues uses population-level survey distributions rather than single-answer ground truth — illustrating an alternative ontology MMLU lacks

*Dataset analysis:*
- DATASET-D12, D13, D14: moral_scenarios encodes 'US standards as of 2020' as the decision rule, with no slot for cultural variation
- DATASET-D9: us_foreign_policy resolves Cold War historiography to a single labeled answer
- DATASET-D15: colonial-era framing (Indian revolt) resolved to single answer with no multi-perspective accommodation

</details>

**Information gaps:**
- Whether any planned MMLU successor or supplement supports multi-perspective scoring (none identified per FV5)

**Requires expert verification:**
- Region-stakeholder design of an output schema that accommodates contested-topic acknowledgment

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MMLU annotator population is graduate/undergraduate students from US institutions [Q23] with Mechanical Turk and US 95th-percentile test-taker baselines [Q31, Q33, Q34] — no Arab regional stakeholders. Ground-truth labels reflect Western academic framing, with moral_scenarios explicitly encoding 'US standards as of 2020' (D12). Inter-annotator agreement is not documented. Empirical evidence (CAMeL, ILMAAM) confirms Western framing of Arab content in LLM evaluation systematically diverges from Arab stakeholder judgments [WEB-5, WEB-15]. With OC rated HIGH and the deployment serving eight Arab countries with contested historical narratives, this is a major convergent- and external-validity violation.

**Strengths:**
- Annotator source institutions are documented [Q23, Q24, Q25], enabling diagnosis even though the demographics themselves are problematic
- Domain-expert performance is benchmarked against US 95th-percentile test-takers [Q33], providing a calibrated US-centric ceiling — useful as a baseline even if not regionally valid

**Checklist:**

- **OC-1**: Ground-truth labels do not reflect Arab regional stakeholder perspectives. moral_scenarios labels are explicitly US-2020-anchored (D12); professional_law labels reflect US common law (D6–D8); us_foreign_policy labels reflect US institutional framing (D9–D11). — _Sources: DATASET-D12, DATASET-D6, DATASET-D9_
- **OC-2**: High disagreement expected on contested topics (Palestinian narrative, Western Sahara, Jerusalem) where Arab stakeholder judgments diverge from US-academic-sourced labels [contested_topics YAML, WEB-5]. — _Sources: WEB-5, WEB-15_
- **OC-3**: MMLU paper does not document annotator demographics beyond 'graduate and undergraduate students' [Q23] — INSUFFICIENT DOCUMENTATION on country, ethnicity, or expertise composition. — _Sources: Q23_
- **OC-4**: Re-annotation is what ArabicMMLU [WEB-2, WEB-6] and ILMAAM [WEB-5] effectively do — but for separate Arabic-content benchmarks, not for MMLU itself. — _Sources: WEB-2, WEB-5_
- **OC-5**: INSUFFICIENT DOCUMENTATION — MMLU paper does not describe label aggregation methods or treatment of annotator disagreement; whether minority perspectives are erased cannot be assessed from the paper.
- **OC-6**: Confirmed convergent- and external-validity violations: US-centric annotation [Q23, Q31, Q33], explicit US-2020 moral framing (D12), no Arab expert review documented; CAMeL evidence of LLM Western bias [WEB-15] confirms practical impact. — _Sources: Q23, Q31, Q33, Q79, DATASET-D12, WEB-15_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q23] 'The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online.' (p.3)
- [Q31] 'Unspecialized humans from Amazon Mechanical Turk obtain 34.5% accuracy on this test.' (p.3)
- [Q33] 'For example, real-world test-taker human accuracy at the 95th percentile is around 87% for US Medical Licensing Examinations' (p.3)
- [Q34] 'If we take the 95th percentile human test-taker accuracy for exams that build up our test... we then estimate that expert-level accuracy is approximately 89.8%.' (p.3)
- [Q79] 'They are notably poor at modeling human (dis)approval, as evident by the low performance on the Professional Law and Moral Scenarios tasks.' (p.8)

*Web sources:*
- [WEB-5] ILMAAM (2025) identified significant cultural misalignments in religion and morality content; 11 expert annotators reviewed for cultural appropriateness, bias, religious sensitivity
- [WEB-15] Naous et al. 2024 (CAMeL) empirically demonstrate LLM Western cultural bias in Arabic prompts
- [WEB-6] ArabicMMLU annotated by 10 Arab native speakers from Jordan, Egypt, Lebanon, UAE, KSA — illustrating the regional annotation MMLU lacks

*Dataset analysis:*
- DATASET-D12: moral_scenarios labels explicitly encode 'ordinary moral standards in the US as of 2020' as the ground-truth criterion
- DATASET-D6, D7, D8: professional_law ground-truth labels reflect US tort, contract, and federal court procedural rules
- DATASET-D9: us_foreign_policy ground-truth answer encodes US institutional perspective on NSC 68

</details>

**Information gaps:**
- Annotator country/ethnicity composition beyond 'students'
- Inter-annotator agreement statistics (not reported in MMLU paper)
- Aggregation methodology for any items where annotators disagreed (not reported)

**Requires expert verification:**
- Arab regional expert relabeling of any Arab-region or Islamic-content questions in MMLU (e.g., world_religions Islamic items, world_history Middle East items)

---

### Output Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Both MMLU and the deployment use text output, satisfying basic modality match. However, MMLU's classification-accuracy metric over A/B/C/D tokens [Q49, Q56] cannot evaluate the open-ended, multi-perspective explanatory responses the deployment's tourist/expat assistant produces. Calibration evaluation [Q64–Q67] is a useful auxiliary signal — GPT-3's 24% confidence-accuracy gap [Q66] is informative — but does not address the form mismatch. With OF rated MODERATE, this is a real but partial concern: MMLU can score factual recall in MCQ form but not the explanatory output form the deployment expects.

**Strengths:**
- Text output modality matches deployment text interface
- Calibration metrics (RMS calibration error, confidence-accuracy correlation) [Q65, Q67] provide useful auxiliary signals on whether models 'know what they don't know' [Q16] — directly relevant to a tourist/expat assistant that should hedge on contested topics
- Zero-shot/few-shot evaluation regime [Q3] aligns with deployment's open-domain generalization requirement (Strength 4)

**Checklist:**

- **OF-1**: Modality matches (text), but output granularity mismatches: MCQ token probability [Q56] vs. open-ended explanation expected by deployment users. — _Sources: Q49, Q56_
- **OF-2**: Not applicable — text-based deployment, no TTS requirement documented.
- **OF-3**: Tourist/expat target population is literate adult readers; literacy not a concern. INSUFFICIENT DOCUMENTATION on accessibility-specific output requirements.
- **OF-4**: Form mismatch documented: MCQ scoring [Q49] cannot credit appropriately-hedged multi-perspective open-ended responses; the authors note their evaluation format 'is not identical to the format in which information is acquired during pretraining' [Q76]. — _Sources: Q49, Q76, DATASET-D12, WEB-11_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q49] 'To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks.' (p.5)
- [Q56] 'The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction.' (p.6)
- [Q66] 'Its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects.' (p.7)
- [Q76] 'Importantly, the format of our evaluation is not identical to the format in which information is acquired during pretraining.' (p.8)
- [Q16] 'GPT-3 does not have an accurate sense of what it does or does not know since its average confidence can be up to 24% off from its actual accuracy.' (p.2)

*Web sources:*
- [WEB-11] MENAValues evaluates LLMs across neutral, personalized, and observer framings — illustrating richer output-form evaluation that MMLU's MCQ accuracy cannot match

*Dataset analysis:*
- DATASET-D12, D13, D14: every sampled item resolves to a single A/B/C/D label, with no mechanism for partial credit on multi-perspective or hedged responses

</details>

**Information gaps:**
- Whether the deployed system generates free-form text or also offers MCQ-style confirmations (interface design not specified in YAML)

**Requires expert verification:**
- Whether deployment evaluation will supplement MMLU MCQ accuracy with open-ended generation metrics (e.g., MENAValues-style prompting)

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** No dedicated Arab history, Middle Eastern geography, Arabic language, or Islamic content subjects in MMLU's 57-subject taxonomy.

**Recommendation:** Replace MMLU as the primary Arab-region knowledge evaluation with ArabicMMLU [WEB-2] (40 tasks across 8 Arab countries) and PalmX 2025 [WEB-13] (Arabic and Islamic culture). Retain MMLU only for transferable STEM/formal-reasoning subjects.

### Input Content ⚠

**Gap:** All MMLU source materials are Anglophone Western institutions; moral_scenarios explicitly encodes US-2020 standards as ground truth.

**Recommendation:** Supplement with ILMAAM [WEB-5] for culturally aligned content and explicitly exclude moral_scenarios from the deployment evaluation suite. Document the Western-source provenance of any MMLU subjects retained.

### Output Ontology ⚠

**Gap:** Single-answer MCQ schema cannot represent multi-perspective handling of contested topics (1948 war, Western Sahara, Lebanese Civil War, Palestinian statehood, Jerusalem) — the deployment's explicitly required output behavior per elicitation Q3.

**Recommendation:** Develop a custom evaluation harness for contested topics using multi-perspective rubrics with Arab regional expert adjudication; do not rely on MMLU MCQ accuracy for these topics. MENAValues [WEB-11] cross-lingual framing methodology is the closest published model.

### Output Content ⚠

**Gap:** Ground-truth labels were determined by US graduate/undergraduate annotators with no documented Arab regional stakeholder review.

**Recommendation:** For any MMLU items retained that touch Arab or Islamic content (world_religions Islamic items, world_history Middle East items, geography items), commission Arab regional expert relabeling. Use ILMAAM's 11-expert annotation methodology [WEB-5] as a template.

### Input Form

**Gap:** English-only format does not evaluate the Arabic-learning sub-cohort.

**Recommendation:** Add DialectalArabicMMLU [WEB-1] for Moroccan/Egyptian/Emirati/Saudi dialect coverage and ArabicMMLU [WEB-2] for MSA. Note that Kuwaiti, Jordanian, Palestinian, and Lebanese dialects remain unbenchmarked — flag as residual gap.

### Output Form

**Gap:** MCQ accuracy metric cannot evaluate open-ended explanatory or perspective-acknowledging responses that the deployed assistant produces.

**Recommendation:** Add open-ended generation evaluation with rubric-based scoring (cultural appropriateness, multi-perspective acknowledgment, calibrated hedging on contested topics). Re-evaluate every 6–12 months given rapid Arabic-benchmark ecosystem growth [WEB-12].

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "We propose a new test to measure a text model's multitask accuracy. The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more." |
| Q2 | 1 | input_ontology | "To attain high accuracy on this test, models must possess extensive world knowledge and problem solving ability." |
| Q3 | 1 | input_form | "We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings." |
| Q4 | 1 | input_ontology | "The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more. It ranges in difficulty from an elementary level to an advanced professional level, and it tests both world knowledge and problem solving ability." |
| Q5 | 1 | output_form | "We find that while most recent models have near random-chance accuracy, the very largest GPT-3 model improves over random chance by almost 20 percentage points on average." |
| Q6 | 1 | output_form | "However, on every one of the 57 tasks, the best models still need substantial improvements before they can reach expert-level accuracy." |
| Q7 | 1 | output_ontology | "Models also have lopsided performance and frequently do not know when they are wrong." |
| Q8 | 1 | output_ontology | "Worse, they still have near-random accuracy on some socially important subjects such as morality and law." |
| Q9 | 1 | output_form | "By comprehensively evaluating the breadth and depth of a model's academic and professional understanding, our test can be used to analyze models across many tasks and to identify important shortcomings." |
| Q10 | 1 | input_content | "Dan Hendrycks, UC Berkeley; Collin Burns, Columbia University; Steven Basart, UChicago; Andy Zou, UC Berkeley; Mantas Mazeika, UIUC; Dawn Song, UC Berkeley; Jacob Steinhardt, UC Berkeley" |
| Q11 | 2 | input_ontology | "Since our test consists in 57 tasks, it can be used to analyze aggregate properties of models across tasks and to track important shortcomings." |
| Q12 | 2 | output_form | "We find that meaningful progress on our benchmark has only become possible in recent months. In particular, few-shot models up to 13 billion parameters (Brown et al., 2020) achieve random chance performance of 25% accuracy, but the 175 billion parameter GPT-3 model reaches a much higher 43.9% accuracy (see Figure 1b)." |
| Q13 | 2 | output_form | "On the other hand, unlike human professionals GPT-3 does not excel at any single subject. Instead, we find that performance is lopsided, with GPT-3 having almost 70% accuracy for its best subject but near-random performance for several other subjects." |
| Q14 | 2 | output_ontology | "Our results indicate that while recent advances have been impressive, state-of-the-art models still struggle at learning and applying knowledge from pretraining. The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality." |
| Q15 | 2 | output_ontology | "This second weakness is particularly concerning because it will be important for future models to have a strong understanding of what is legal and what is ethical." |
| Q16 | 2 | output_form | "Worryingly, we also find that GPT-3 does not have an accurate sense of what it does or does not know since its average confidence can be up to 24% off from its actual accuracy." |
| Q17 | 2 | input_ontology | "We comprehensively evaluate the breadth and depth of a model's text understanding by covering numerous topics that humans are incentivized to learn." |
| Q18 | 2 | input_content | "The dominant paradigm in NLP is to pretrain large models on massive text corpora including educational books and websites." |
| Q19 | 2 | input_ontology | "Many recent benchmarks aim to assess a model's general world knowledge and basic reasoning ability by testing its "commonsense."" |
| Q20 | 3 | input_ontology | "We create a massive multitask test consisting of multiple-choice questions from various branches of knowledge." |
| Q21 | 3 | input_ontology | "The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn." |
| Q22 | 3 | input_ontology | "There are 57 tasks in total, which is also the number of Atari games (Bellemare et al., 2013), all of which are listed in Appendix B." |
| Q23 | 3 | input_content | "The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online." |
| Q24 | 3 | input_content | "These include practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination." |
| Q25 | 3 | input_content | "It also includes questions designed for undergraduate courses and questions designed for readers of Oxford University Press books." |
| Q26 | 3 | output_ontology | "Some tasks cover a subject, like psychology, but at a specific level of difficulty, such as "Elementary," "High School," "College," or "Professional."" |
| Q27 | 3 | input_form | "We collected 15908 questions in total, which we split into a few-shot development set, a validation set, and a test set." |
| Q28 | 3 | input_form | "The few-shot development set has 5 questions per subject, the validation set may be used for selecting hyperparameters and is made of 1540 questions, and the test set has 14079 questions." |
| Q29 | 3 | input_form | "Each subject contains 100 test examples at the minimum, which is longer than most exams designed to assess people." |
| Q30 | 3 | output_content | "Human-level accuracy on this test varies." |
| Q31 | 3 | output_content | "Unspecialized humans from Amazon Mechanical Turk obtain 34.5% accuracy on this test." |
| Q32 | 3 | output_content | "Meanwhile, expert-level performance can be far higher." |
| Q33 | 3 | output_content | "For example, real-world test-taker human accuracy at the 95th percentile is around 87% for US Medical Licensing Examinations, and these questions make up our "Professional Medicine" task." |
| Q34 | 3 | output_content | "If we take the 95th percentile human test-taker accuracy for exams that build up our test, and if we make an educated guess when such information is unavailable, we then estimate that expert-level accuracy is approximately 89.8%." |
| Q35 | 3 | input_ontology | "Since our test aggregates different subjects and several levels of difficulty, we measure more than straightforward commonsense or narrow linguistic understanding." |
| Q36 | 4 | input_ontology | "The humanities is a group of disciplines that make use of qualitative analysis and analytic methods rather than scientific empirical methods." |
| Q37 | 4 | input_ontology | "Branches of the humanities include law, philosophy, history, and so on (Appendix B)." |
| Q38 | 4 | input_ontology | "For example, legal understanding requires knowledge of how to apply rules and standards to complex scenarios, and also provide answers with stipulations and explanations." |
| Q39 | 4 | input_ontology | "For philosophy, our questions cover concepts like logical fallacies, formal logic, and famous philosophical arguments." |
| Q40 | 4 | input_ontology | "It also covers moral scenarios, including questions from the ETHICS dataset (Hendrycks et al., 2020) that test a model's understanding of normative statements through predicting widespread moral intuitions about diverse everyday scenarios." |
| Q41 | 4 | input_ontology | "Finally, our history questions cover a wide range of time periods and geographical locations, including prehistory and other advanced subjects." |
| Q42 | 4 | input_ontology | "Social science includes branches of knowledge that examine human behavior and society." |
| Q43 | 4 | input_ontology | "Subject areas include economics, sociology, politics, geography, psychology, and so on." |
| Q44 | 4 | input_ontology | "Our economics questions include microeconomics, macroeconomics, and econometrics, and cover different types of problems, including questions that require a mixture of world knowledge, qualitative reasoning, or quantitative reasoning." |
| Q45 | 4 | input_ontology | "We also include important but more esoteric topics such as security studies in order to test the boundaries of what is experienced and learned during pretraining." |
| Q46 | 4 | input_ontology | "Social science also includes psychology, a field that may be especially important for attaining a nuanced understanding of humans." |
| Q47 | 4 | input_ontology | "STEM subjects include physics, computer science, mathematics, and more." |
| Q48 | 4 | input_ontology | "Conceptual physics tests understanding of simple physics principles and may be thought" |
| Q49 | 5 | output_form | "To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks." |
| Q50 | 5 | output_form | "We evaluate GPT-3 (Brown et al., 2020) and UnifiedQA (Khashabi et al., 2020)." |
| Q51 | 5 | output_form | "For GPT-3 we use the OpenAI API, which provides access to four model variants, "Ada," "Babbage," "Curie," and "Davinci," which we refer to as "Small" (2.7 billion parameters), "Medium" (6.7 billion), "Large" (13 billion) and "X-Large" (175 billion)." |
| Q52 | 5 | output_form | "UnifiedQA uses the T5 (Raffel et al., 2019) text-to-text backbone and is fine-tuned on previously proposed question answering datasets (Lai et al., 2017), where the prediction is the class with the highest token overlap with UnifiedQA's text output." |
| Q53 | 5 | output_form | "Since UnifiedQA is fine-tuned on other datasets, we evaluate it without any further tuning to assess its transfer accuracy." |
| Q54 | 5 | output_form | "We also fine-tune RoBERTa-base, ALBERT-xxlarge, and GPT-2 on UnifiedQA training data and our dev+val set." |
| Q55 | 5 | output_form | "We primarily focus on UnifiedQA and GPT-3 in the rest of this document, but additional discussion of RoBERTa, ALBERT, and GPT-2 is in Appendix A." |
| Q56 | 6 | input_form | "We feed GPT-3 prompts like that shown in Figure 1a. We begin each prompt with "The following are multiple choice questions (with answers) about [subject]." For zero-shot evaluation, we append the question to the prompt. For few-shot evaluation, we add up to 5 demonstration examples with answers to the prompt before appending the question. All prompts end with "Answer: ". The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction. For consistent evaluation, we create a dev set with 5 fixed few-shot examples for each subject." |
| Q57 | 6 | output_form | "We compare the few-shot accuracy of each GPT-3 size in Table 1. We find that the three smaller GPT-3 models have near random accuracy (around 25%). In contrast, we find that the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%." |
| Q58 | 6 | output_form | "We also find qualitatively similar results in the zero-shot setting. While the smaller models have around 25% zero-shot accuracy, Figure 10 in Appendix A shows that the largest GPT-3 model has a much higher zero-shot accuracy of about 37.7%." |
| Q59 | 6 | output_form | "The largest UnifiedQA model we test has 11 billion parameters, which is slightly smaller than GPT-3 Large. Nevertheless, we show in Table 1 that it attains 48.9% accuracy. This performs better than the few-shot GPT-3 X-Large model, despite UnifiedQA have an order of magnitude fewer parameters." |
| Q60 | 6 | output_form | "We also find that even the smallest UnifiedQA variant, with just 60 million parameters, has approximately 29.3% accuracy." |
| Q61 | 6 | output_form | "These results suggest that while model size is a key component for achieving strong performance, fine-tuning also helps." |
| Q62 | 6 | output_form | "Using our test, we discover that GPT-3 and UnifiedQA have lopsided performance and several substantial knowledge gaps. Figure 6 shows the accuracy of GPT-3 (few-shot) and UnifiedQA for all 57 tasks. It shows the both models are below expert-level performance for all tasks, with GPT-3's accuracy ranging from 69% for US Foreign Policy to 26% for College Chemistry. UnifiedQA does best on marketing, with an accuracy of 82.5%." |
| Q63 | 6 | output_ontology | "Overall, models do poorly on highly procedural problems. Figure 6 shows that calculation-heavy STEM subjects tend to have low accuracy compared to verbal subjects. For GPT-3, 9 out of the 10" |
| Q64 | 7 | output_form | "We should not trust a model's prediction unless the model is calibrated, meaning that its confidence is a good estimate of the actual probability the prediction is correct." |
| Q65 | 7 | output_form | "We evaluate the calibration of GPT-3 by testing how well its average confidence estimates its actual accuracy for each subject." |
| Q66 | 7 | output_form | "Its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects." |
| Q67 | 7 | output_form | "Another calibration measure is the Root Mean Squared (RMS) calibration error (Hendrycks et al., 2019a; Kumar et al., 2019)." |
| Q68 | 7 | output_form | "Elementary Mathematics which has a zero-shot RMS calibration error of 19.4%." |
| Q69 | 7 | output_form | "Models are only somewhat more calibrated in the few-shot setting, as shown in Appendix A." |
| Q70 | 7 | input_form | "While text is capable of conveying an enormous number of concepts about the world, many important concepts are conveyed mainly through other modalities, such as images, audio, and physical interaction (Bisk et al., 2020)." |
| Q71 | 7 | input_form | "Existing large-scale NLP models, such as GPT-3, do not incorporate multimodal information, so we design our benchmark to capture a diverse array of tasks in a text-only format." |
| Q72 | 7 | input_content | "A major distinction between our benchmark and previous multitask NLP benchmarks is that we do not require large training sets." |
| Q73 | 7 | input_content | "Instead, we assume that models have acquired the requisite knowledge from reading vast quantities of diverse text from the Internet." |
| Q74 | 8 | output_form | "For this reason we assess pretrained models in a zero-shot, few-shot, or transfer setting and we provide a dev, val, and test set for each task." |
| Q75 | 8 | output_form | "The dev set is used for few-shot prompts, the val set could be used for hyperparameter tuning, and the test set is used to compute the final accuracy." |
| Q76 | 8 | input_form | "Importantly, the format of our evaluation is not identical to the format in which information is acquired during pretraining." |
| Q77 | 8 | input_form | "This has the benefit of obviating concerns about spurious training set annotation artifacts (Geirhos et al., 2020; Hendrycks et al., 2019b) and is in stark contrast to the previous paradigm of identically distributed training and test sets." |
| Q78 | 8 | output_form | "We find that current large-scale Transformers have wide room for improvement." |
| Q79 | 8 | output_ontology | "They are notably poor at modeling human (dis)approval, as evident by the low performance on the Professional Law and Moral Scenarios tasks." |
| Q80 | 8 | output_ontology | "Models also have difficulty performing calculations, so much so that they exhibit poor performance on Elementary Mathematics and many other STEM subjects with "plug and chug" problems." |
| Q81 | 8 | output_form | "Additionally, they do not match expert-level performance (90%) on any subject, so for all subjects it is subhuman." |
| Q82 | 8 | output_form | "On average, models are only now starting to move beyond random-chance accuracy levels." |
| Q83 | 8 | input_content | "We collected approximately 2,000 additional Professional Law training examples." |
| Q84 | 8 | output_form | "After fine-tuning a RoBERTa-base model (Liu et al., 2019) using this custom training set, our model attained 32.8% test accuracy." |
| Q85 | 8 | input_content | "We also had RoBERTa continue pretraining on approximately 1.6 million legal case summaries using Harvard's Law Library case law corpus case.law, but after fine-tuning it only attained 36.1% accuracy." |
| Q86 | 8 | output_form | "This suggests that while additional pretraining on relevant high quality text can help, it may not be enough to substantially increase the performance of current models." |
| Q87 | 8 | output_form | "It is unclear whether simply scaling up existing language models will solve the test." |
| Q88 | 8 | output_form | "Current understanding indicates that a 10× increase in model size must be accompanied by an approximate 5× increase in data (Kaplan et al., 2020)." |
| Q89 | 8 | input_ontology | "We introduced a new test that measures how well text models can learn and apply knowledge encountered during pretraining." |
| Q90 | 8 | input_ontology | "By covering 57 subjects at varying levels of difficulty, the test assesses language understanding in greater breadth and depth than previous benchmarks." |
| Q91 | 9 | input_content | "We would like to thank the following for their helpful comments: Oyvind Tafjord, Jan Leike, David Krueger, Alex Tamkin, Girish Sastry, and Henry Zhu." |
| Q92 | 9 | input_content | "DH is supported by the NSF GRFP Fellowship and an Open Philanthropy Project Fellowship." |
| Q93 | 9 | input_content | "This research was also supported by the NSF Frontier Award 1804794." |
| Q94 | 11 | input_ontology | "This appendix includes figures with sorted results (Figure 9), few-shot examples vs. accuracy (Figure 10), and few-shot calibration (Figure 11). It also includes sections on fine-tuning, error analysis, and format sensitivity." |
| Q95 | 11 | output_form | "We primarily analyzed models with more than 10 billion parameters in the main body of the paper. For this section, we analyze smaller models including RoBERTa-base (125 million parameters) (Liu" |
| Q96 | 11 | output_form | "On the left are GPT-3 few shot accuracies for all of the 57 tasks. On the right are UnifiedQA transfer accuracies for all of the 57 tasks. For both models, capabilities are lopsided." |
| Q97 | 12 | input_form | "Models are fine-tuned to predict one of four classes using the UnifiedQA MCQ questions and using our dev+val set." |
| Q98 | 12 | output_form | "We test on our multitask test set." |
| Q99 | 12 | output_form | "RoBERTa-base attains an overall accuracy of 27.9%, with 27.9% accuracy for the humanities, 28.8% for social sciences, 27.0% for STEM, and 27.7% for other." |
| Q100 | 12 | output_form | "ALBERT-xxlarge attains an accuracy of 27.1%, with 27.2% accuracy for the humanities, 25.7% for the social sciences, 27.7% for STEM, and 27.9% for other." |
| Q101 | 12 | output_form | "GPT-2 attains an accuracy of 32.4%, with 32.8% accuracy for the humanities, 33.3% for the social sciences, 30.2% for STEM, and 33.1% for other." |
| Q102 | 12 | output_form | "We qualitatively analyze when GPT-3 makes high confidence mistakes." |
| Q103 | 12 | input_form | "While different question formatting choices often lead to similar GPT-3 accuracies, we find that UnifiedQA is more sensitive." |
| Q104 | 12 | input_form | "UnifiedQA's input format is of the form QUESTION1 \\n (A) CHOICE1 (B) CHOICE2 (C) CHOICE3 (D) CHOICE4</s> where questions and choices are normalized and made lowercase." |
| Q105 | 12 | input_form | "If we remove the </s> from the input, accuracy declines by several percentage points." |
| Q106 | 13 | input_ontology | "We provide analysis of question length and difficulty in Figure 12. We list all tasks and the topics they test in Table 2. We also provide an example for each task starting with Figure 14." |
| Q107 | 13 | input_content | "Since language models train on vast text corpora, there is some chance that they have seen the exact question and answer during pretraining. If they memorized the exact question and answer, then they would attain higher accuracy than their true ability. Likewise, a question's entropy would be especially low if it were memorized. Memorized questions and answers should have low entropy and" |
| Q108 | 13 | input_form | "For questions longer than a tweet (280 characters), the correlation between question length and true label confidence is slightly positive. This shows that longer questions are not necessarily harder." |
| Q109 | 14 | input_content | "However, in Figure 13, we see that accuracy and question entropy are not positively correlated, suggesting that the test's low-entropy questions do not correspond to memorized (and thereby correctly predicted) answers." |
| Q110 | 14 | input_content | "This suggests that our exact questions were not memorized." |
| Q111 | 14 | input_content | "However, during pretraining models encountered text related to our questions through processing Wikipedia." |
| Q112 | 14 | input_content | "We also note that most of our questions came from PDFs or websites where questions and answers are on separate pages." |
| Q113 | 14 | input_content | "See Brown et al. (2020) for a previous discussion of contamination showing that the phenomena hardly affects performance." |
| Q114 | 14 | input_content | "To reduce the probability that future models encounter exact questions during test-time, we will provide a list of question sources." |
| Q115 | 14 | output_form | "The average log probability of the question (without answer) is not strongly positively correlated with accuracy, all else equal." |
| Q116 | 14 | output_form | "Each point corresponds to a task." |
| Q117 | 14 | output_form | "Higher log probability indicates higher compression, and especially high log probability would suggest memorization." |
| Q118 | 14 | output_form | "In the zero-shot question prompt, the correlation between average log probability and accuracy is r = −0.43, and for the few-shot setting the correlation is r = −0.56." |
| Q119 | 15 | input_ontology | "Table 2: Summary of all 57 tasks." |
| Q120 | 16 | input_ontology | "Find all c in Z₃ such that Z₃[x]/(x² + c) is a field." |
| Q121 | 16 | input_ontology | "What is the embryological origin of the hyoid bone?" |
| Q122 | 16 | input_ontology | "Why isn't there a planet where the asteroid belt is located?" |
| Q123 | 16 | input_ontology | "Three contrasting tactics that CSO's can engage in to meet their aims are ___ which typically involves research and communication, ___, which may involve physically attacking a company's operations or ___, often involving some form of ___." |
| Q124 | 16 | input_ontology | "How many attempts should you make to cannulate a patient before passing the job on to a senior colleague?" |
| Q125 | 16 | input_ontology | "In a given population, 1 out of every 400 people has a cancer caused by a completely recessive allele, b. Assuming the population is in Hardy-Weinberg equilibrium, which of the following is the expected proportion of individuals who carry the b allele but are not expected to develop the cancer?" |
| Q126 | 16 | input_ontology | "Which of the following statements about the lanthanide elements is NOT true?" |
| Q127 | 17 | input_ontology | "Consider a computer design in which multiple processors, each with a private cache memory, share global memory using a single bus." |
| Q128 | 17 | input_ontology | "Let A be a real 2 × 2 matrix. Which of the following statements must be true?" |
| Q129 | 17 | input_ontology | "In a genetic test of a newborn, a rare genetic disorder is found that has X-linked recessive transmission." |
| Q130 | 17 | input_ontology | "One end of a Nichrome wire of length 2L and cross-sectional area A is attached to an end of another Nichrome wire of length L and cross- sectional area 2A." |
| Q131 | 17 | input_ontology | "Why is it that anti-virus scanners would not have found an exploitation of Heartbleed?" |
| Q132 | 17 | input_ontology | "A model airplane flies slower when flying into the wind and faster with wind at its back." |
| Q133 | 18 | input_ontology | "Consider the following AR(1) model with the disturbances having zero mean and unit variance yt = 0.2 + 0.4yt−1 + ut The (unconditional) mean of y will be given by (A) 0.2 (B) 0.4 (C) 0.5 (D) 0.33" |
| Q134 | 18 | input_ontology | "A point pole has a strength of 4π × 10−4 weber. The force in newtons on a point pole of 4π × 1.5 × 10−4 weber placed at a distance of 10 cm from it will be (A) 15 N. (B) 20 N. (C) 7.5 N. (D) 3.75 N." |
| Q135 | 18 | input_ontology | "A total of 30 players will play basketball at a park. There will be exactly 5 players on each team. Which statement correctly explains how to find the number of teams needed? (A) Add 5 to 30 to find 35 teams. (B) Divide 30 by 5 to find 6 teams. (C) Multiply 30 and 5 to find 150 teams. (D) Subtract 5 from 30 to find 25 teams." |
| Q136 | 18 | input_ontology | "Determine whether the statements are logically equivalent or contradictory. If neither, determine whether they are consistent or inconsistent. E ⊃ (F · E) and ∼ E · F (A) Logically equivalent (B) Contradictory (C) Neither logically equivalent nor contradictory, but consistent (D) Inconsistent" |
| Q137 | 18 | input_content | "As of 2017, how many of the world's 1-year-old children today have been vaccinated against some disease? (A) 80% (B) 60% (C) 40% (D) 20%" |
| Q138 | 18 | input_ontology | "Homologous structures are often cited as evidence for the process of natural selection. All of the following are examples of homologous structures EXCEPT (A) the wings of a bird and the wings of a bat (B) the flippers of a whale and the arms of a man (C) the pectoral fins of a porpoise and the flippers of a seal (D) the forelegs of an insect and the forelimbs of a dog" |
| Q139 | 18 | input_ontology | "From the solubility rules, which of the following is true? (A) All chlorides, bromides, and iodides are soluble (B) All sulfates are soluble (C) All hydroxides are soluble (D) All ammonium-containing compounds are soluble" |
| Q140 | 19 | input_ontology | "A list of numbers has n elements, indexed from 1 to n. The following algorithm is intended to display the number of elements in the list that have a value greater than 100. The algorithm uses the variables count and position. Steps 3 and 4 are missing." |
| Q141 | 19 | input_ontology | "Which of the following could be used to replace steps 3 and 4 so that the algorithm works as intended?" |
| Q142 | 19 | input_content | "This question refers to the following information." |
| Q143 | 19 | input_content | "From the passage, one may infer that the English Parliament wished to argue that the Act of Supremacy would" |
| Q144 | 19 | input_ontology | "During the third stage of the demographic transition model, which of the following is true?" |
| Q145 | 20 | input_ontology | "Figure 37: A High School Government and Politics example." |
| Q146 | 20 | input_ontology | "Figure 38: A High School Macroeconomics example." |
| Q147 | 20 | input_ontology | "Figure 39: A High School Mathematics example." |
| Q148 | 20 | input_ontology | "Figure 40: A High School Microeconomics example." |
| Q149 | 20 | input_ontology | "Figure 41: A High School Physics example." |
| Q150 | 20 | input_ontology | "Figure 42: A High School Psychology example." |
| Q151 | 21 | input_ontology | "Figure 43: A High School Statistics example." |
| Q152 | 21 | input_content | "Figure 44: A High School US History example." |
| Q153 | 21 | input_content | "Figure 45: A High School World History example." |
| Q154 | 21 | input_ontology | "Figure 46: A Human Aging example." |
| Q155 | 22 | input_content | "Morning sickness is typically a problem: (A) during the first trimester (B) during the second trimester (C) during the third trimester (D) all through the pregnancy" |
| Q156 | 22 | input_content | "Would a reservation to the definition of torture in the ICCPR be acceptable in contemporary practice? (A) This is an acceptable reservation if the reserving country's legislation employs a different definition (B) This is an unacceptable reservation because it contravenes the object and purpose of the ICCPR (C) This is an unacceptable reservation because the definition of torture in the ICCPR is consistent with customary international law (D) This is an acceptable reservation because under general international law States have the right to enter reservations to treaties" |
| Q157 | 22 | input_content | "Which position does Rawls claim is the least likely to be adopted by the POP (people in the original position)? (A) The POP would choose equality above liberty. (B) The POP would opt for the 'maximin' strategy. (C) The POP would opt for the 'difference principle.' (D) The POP would reject the 'system of natural liberty.'" |
| Q158 | 22 | input_content | "John Stuart Mill: Each person's happiness is a good to that person, and the general happiness, therefore, a good to the aggregate of all persons. (A) Fallacy of Composition (B) Fallacy of Division (C) Gambler's Fallacy (D) Equivocation" |
| Q159 | 22 | input_ontology | "A 6-sided die is rolled 15 times and the results are: side 1 comes up 0 times; side 2: 1 time; side 3: 2 times; side 4: 3 times; side 5: 4 times; side 6: 5 times. Based on these results, what is the probability of side 3 coming up when using Add-1 Smoothing? (A) 2/15 (B) 1/7 (C) 3/16 (D) 1/5" |
| Q160 | 22 | input_content | "According to Lewin, Lippet and White's 1939 experiment, which form of leadership produced the most work from participants? (A) Laissez-faire (B) Democratic (C) Authoritarian (D) A mix of laissez-faire and democratic" |
| Q161 | 23 | output_form | "Figure 57: A Moral Scenarios example. The formatting of this task hinders UnifiedQA performance substantially." |
| Q162 | 24 | input_content | "According to Moore's "ideal utilitarianism," the right action is the one that brings about the greatest amount of: (A) pleasure. (B) happiness. (C) good. (D) virtue." |
| Q163 | 24 | input_content | "Researchers now believe that the decline of the Maya was caused chiefly by: (A) a cataclysm of some kind, such as an earthquake, volcano, or tsunami. (B) ecological degradation resulting from slash-and-burn farming techniques. (C) endless wars between neighboring Mayan city-states. (D) practices of interbreeding that led to a steep rise in congenital disorders." |
| Q164 | 24 | input_content | "Krete is an unmarried taxpayer with income exclusively from wages. By December 31, year 1, Krete's employer has withheld $16,000 in federal income taxes and Krete has made no estimated tax payments. On April 15, year 2, Krete timely filed for an extension request to file her individual tax return, and paid $300 of additional taxes. Krete's year 1 tax liability was $16,500 when she timely filed her return on April 30, year 2, and paid the remaining tax liability balance. What amount would be subject to the penalty for underpayment of estimated taxes? (A) $0 (B) $500 (C) $1,650 (D) $16,500" |
| Q165 | 24 | input_content | "The night before his bar examination, the examinee's next-door neighbor was having a party. The music from the neighbor's home was so loud that the examinee couldn't fall asleep. The examinee called the neighbor and asked her to please keep the noise down. The neighbor then abruptly hung up. Angered, the examinee went into his closet and got a gun. He went outside and fired a bullet through the neighbor's living room window. Not intending to shoot anyone, the examinee fired his gun at such an angle that the bullet would hit the ceiling. He merely wanted to cause some damage to the neighbor's home to relieve his angry rage. The bullet, however, ricocheted off the ceiling and struck a partygoer in the back, killing him. The jurisdiction makes it a misdemeanor to discharge a firearm in public. The examinee will most likely be found guilty for which of the following crimes in connection to the death of the partygoer? (A) Murder. (B) Involuntary manslaughter. (C) Voluntary manslaughter. (D) Discharge of a firearm in public." |
| Q166 | 25 | input_content | "Published as a conference paper at ICLR 2021" |
| Q167 | 26 | input_ontology | "Figure 66: A Security Studies example." |
| Q168 | 26 | input_ontology | "Figure 67: A Sociology example." |
| Q169 | 26 | input_ontology | "Figure 68: A US Foreign Policy example." |
| Q170 | 26 | input_ontology | "Figure 69: A Virology example." |
| Q171 | 27 | input_ontology | "Figure 70: A World Religions example." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/abs/2510.27543 |
| WEB-2 | https://aclanthology.org/2024.findings-acl.334/ |
| WEB-3 | https://en.wikipedia.org/wiki/Standard_Moroccan_Amazigh |
| WEB-4 | https://www.constituteproject.org/constitution/Morocco_2011 |
| WEB-5 | https://aclanthology.org/2025.loreslm-1.29/ |
| WEB-6 | https://github.com/mbzuai-nlp/ArabicMMLU |
| WEB-7 | https://huggingface.co/datasets/FreedomIntelligence/ACVA-Arabic-Cultural-Value-Alignment |
| WEB-8 | https://www.atlanticcouncil.org/blogs/menasource/vision-2030-women-economy-saudi-arabia/ |
| WEB-9 | https://www.ohchr.org/en/meeting-summaries/2024/10/experts-committee-elimination-discrimination-against-women |
| WEB-10 | https://arxiv.org/abs/2402.12840 |
| WEB-11 | https://arxiv.org/html/2510.13154 |
| WEB-12 | https://arxiv.org/html/2510.13430v1 |
| WEB-13 | https://arxiv.org/html/2509.02550 |
| WEB-14 | https://arxiv.org/html/2603.23750 |
| WEB-15 | https://venturebeat.com/ai/large-language-models-exhibit-significant-western-cultural-bias-study-finds |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** cais/mmlu (57 subject configurations)
**Analysis date:** 2025-01-31
**Examples reviewed:** ~290 examples across 57 subject configs (5–6 per config)
**Columns shown:** question, subject, choices, answer
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | mmlu | high_school_government_and_politics, test, Ex1 | A | "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" | US constitutional law — exclusively US institutional framing | IO, IC |
| D2 | mmlu | high_school_government_and_politics, test, Ex2 | B | "In the majority of cases, federal programs are implemented by state and local governments, by means of federal funding" | US federal governance structure | IO, IC |
| D3 | mmlu | high_school_government_and_politics, test, Ex4 | D | "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" | US-specific legislative history | IO, IC |
| D4 | mmlu | high_school_us_history, test, Ex2 | B | "John C. Calhoun, 'South Carolina Exposition and Protest,' 1828" | US political history — no Arab-region analog | IO, IC |
| D5 | mmlu | high_school_us_history, test, Ex5 | A | "Tonight, the daughter of an immigrant from Italy has been chosen to run for (vice) president… Geraldine Ferraro, Vice Presidential Nomination Acceptance Address, July 19, 1984" | US domestic politics 1984 | IO, IC |
| D6 | mmlu | professional_law, test, Ex1 | A | "A truck driver was assigned to drive a huge tractor-trailer loaded with logs… the girl was struck by the tractor-trailer and was seriously injured" | US tort law scenario | IO, IC, OC |
| D7 | mmlu | professional_law, test, Ex3 | C | "A patient filed a medical malpractice action against a hospital in federal court" | US federal court procedure | IO, IC, OC |
| D8 | mmlu | professional_law, test, Ex5 | A | "A buyer filed a lawsuit against a seller based on a written contract allegedly executed at the time of the sale of the seller's hot dog stand" | US contract law | IO, IC, OC |
| D9 | mmlu | us_foreign_policy, test, Ex3 | C | "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" | US Cold War policy — framed entirely from US perspective | IO, IC, OC |
| D10 | mmlu | us_foreign_policy, test, Ex4 | D | "In American government, the power to declare war rests with Congress." | US constitutional structure | IO |
| D11 | mmlu | us_foreign_policy, test, Ex5 | A | "Revelations that the NSA was monitoring the communications of American citizens without obtaining warrants" | US domestic surveillance scandal | IO, IC |
| D12 | mmlu | moral_scenarios, test, Ex1 | A | "For which of these two scenarios does the main character do something clearly morally wrong, according to ordinary moral standards in the US as of 2020?" | Explicitly frames moral judgment via US 2020 standards | OC, OO |
| D13 | mmlu | moral_scenarios, test, Ex2 | B | "according to ordinary moral standards in the US as of 2020? Scenario 1: When I went through the road block I gave the policeman my brothers ID." | US-anchored moral framing | OC, OO |
| D14 | mmlu | moral_scenarios, test, Ex3 | C | "according to ordinary moral standards in the US as of 2020? Scenario 2: I was due to start work soon, so I went to a baseball game." | US cultural reference (baseball) embedded in moral reasoning | OC, OO, IC |
| D15 | mmlu | high_school_world_history, test, Ex2 | B | "British journalist William Howard Russell, My Indian Mutiny Diary, 1860… 'the deed was done by a subject race — by black men who dared to shed the blood of their masters'" | Colonial-era British framing of Indian revolt | IC, OC |
| D16 | mmlu | high_school_world_history, test, Ex5 | A | "Excerpt from the inscription of Kerdir at Naqsh-e-Rustam, Persia, late third century C.E. … Jews, Buddhists, Hindus, Nasoreans, Christians, Maktak, and Manichaeans in the empire were smitten" | Near Eastern (Persian) source — the only example touching the broader Middle East region | IO, IC |
| D17 | mmlu | world_religions, test, Ex1 | A | "Rome claimed that their bishop (pope) was the direct successor of which leader? … Peter" | Christian ecclesiastical history — no Islamic content in sampled examples | IO, IC |
| D18 | mmlu | world_religions, test, Ex2 | B | "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" | Jainism content | IO |
| D19 | mmlu | world_religions, test, Ex3 | C | "Which are the synoptic Gospels? … Matthew, Mark, Luke" | Christian Biblical content | IO |
| D20 | mmlu | world_religions, test, Ex4 | D | "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" | Jainism content — no Islamic content in sample | IO |
| D21 | mmlu | world_religions, test, Ex5 | A | "What is the most important prayer in Judaism? … The Shema" | Jewish religious content | IO |
| D22 | mmlu | global_facts, test, Ex1 | A | "About what percentage of survey respondents from China report having paid a bribe in the last year to access public services … as of 2017?" | China-focused global facts | IO, IC |
| D23 | mmlu | global_facts, test, Ex2 | B | "As of 2017, what fraction of the population in India used the internet in the past three months? … 26%" | India-focused global facts | IO, IC |
| D24 | mmlu | global_facts, test, Ex3 | C | "As of 2019, which of the following had the lowest life expectancy? … Mexico" | Global health — Latin American and Asian countries featured; no Arab countries | IO, IC |
| D25 | mmlu | global_facts, test, Ex4 | D | "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … makes it a better place to live?" | India-focused survey data | IO, IC |
| D26 | mmlu | global_facts, test, Ex5 | A | "At the time of independence, there were already hundreds of thousands of university graduates in ____, but hardly any at all in ____. … India, Congo" | Development economics — Africa/Asia framing, no Arab countries | IO, IC |
| D27 | mmlu | high_school_geography, test, Ex1 | A | "What is the most rapidly growing religion in the United States today? … Islam" | US-context geography question; Islam mentioned but in US demographic context | IO, IC |
| D28 | mmlu | high_school_geography, test, Ex5 | A | "Which zone contains low-income slums, ethnic ghettos, and general deterioration in Burgess's concentric zone model of urban form?" | US urban sociology model (Burgess) | IO, IC |
| D29 | mmlu | high_school_european_history, test, Ex1 | A | "Leeds Woolen Workers Petition, 1786 … The sentiments expressed by the Leeds woolen workers illustrate which of the following historical trends?" | British industrial history | IO, IC |
| D30 | mmlu | high_school_european_history, test, Ex2 | B | "Voltaire, Letters on the English Nation, 1733 … of all religions, the Christian ought doubtless to inspire the most tolerance" | European Enlightenment philosophy | IO, IC |
| D31 | mmlu | business_ethics, test, Ex5 | A | "civil society is far less developed than in, for instance, _______ … Russia, China, Britain" | Western-centric civil society framing; Arab world absent from options | IC |
| D32 | mmlu | human_aging, test, Ex3 | C | "The age at which one can receive full benefits from social security … Has been increasing" | US social security system | IC |
| D33 | mmlu | human_aging, test, Ex4 | D | "Which of the following groups of Americans have the lowest rate of alcohol abuse? … Asian-American" | US demographic framing | IC |
| D34 | mmlu | human_sexuality, test, Ex1 | A | "Which of the following is the most common method of birth control for married couples in the U.S. … Sterilization" | US-specific reproductive health statistics | IC |
| D35 | mmlu | human_sexuality, test, Ex5 | A | "From 1988 to 1990 among heterosexuals in the US, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women" | US sexual behavior survey data | IC |
| D36 | mmlu | prehistory, test, Ex4 | D | "Archaeological evidence indicates that cattle were first domesticated where and how long ago? … in the Middle East, about 10,500 years ago" | Middle East referenced as origin of cattle domestication — one of very few regional mentions | IO, IC |
| D37 | mmlu | high_school_world_history, test, Ex4 | D | "Kwame Nkrumah, Neo-Colonialism, 1965 … 'A State in the grip of neo-colonialism is not master of its own destiny.'" | African post-colonial context — non-Western source, though not Arab | IC |
| D38 | mmlu | jurisprudence, test, Ex4 | D | "Which of the following statements best describes the postmodernist project? … It rejects the Kantian concern with individual rights, equality, and justice." | Western jurisprudential theory; no Islamic jurisprudence | IO |
| D39 | mmlu | international_law, test, Ex4 | D | "What is the meaning of cultural relativism? … Cultural relativism posits that local culture should validate the existence and practice of all human rights" | International law — potentially relevant to Arab regional norms | IO |
| D40 | mmlu | auxiliary_train, train, Ex1 | B | "Jim watched a liquor store furtively for some time, planning to hold it up … On a charge of burglary, Jim's best defense would be that the liquor store was open to the public." | US criminal law scenario | IO, IC, OC |
| D41 | mmlu | high_school_statistics, test, Ex5 | A | "As reported on CNN, in a May 1999 national poll 43% of high school students expressed fear about going to school" | US-sourced statistics example | IC |
| D42 | mmlu | security_studies, test, Ex2 | B | "Best described as intensification of worldwide social relations and increasing interdependence, globalization is the result of the compression of space and time" | Abstract IR theory — not regionally specific | IO |
| D43 | mmlu | professional_psychology, test, Ex2 | B | "With regard to minority and nonminority clients, psychotherapy is … equally effective" | US psychology research context | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Universal STEM and Formal Reasoning Content
- **Dimension(s):** IO, IC, IF
- **Observation:** A large proportion of MMLU subjects — abstract algebra, anatomy, astronomy, college chemistry, college physics, computer science, electrical engineering, formal logic, elementary mathematics, machine learning — contain questions with no cultural or geographic specificity. These questions test universal scientific and mathematical knowledge equally valid for Arab-region users and non-Arab users alike.
- **Deployment relevance:** The deployment covers school-level general educational knowledge. STEM content that tourists and expats ask about (basic science, geography concepts, math) can be evaluated fairly through MMLU even in an Arab-region deployment. A model scoring well on these subjects demonstrates transferable academic competence.
- **Datapoint citations:**
  - [D1–D43 passim] Abstract algebra (Ex 1–5), anatomy (Ex 1–5), astronomy (Ex 1–5), college chemistry (Ex 1–5), formal logic (Ex 1–5) — all contain culturally neutral mathematical or biological content. For example, abstract algebra Ex3: "Find all zeros in the indicated finite field of the given polynomial with coefficients in that field. x^3 + 2x + 2 in Z_7" — no cultural grounding required.

#### Strength 2: English-Language Text-Only Format Matches Primary Interaction Mode
- **Dimension(s):** IF
- **Observation:** MMLU is exclusively text-based, English-only, and multiple-choice. The deployment's primary user cohort (non-Arab tourists and expats) interacts in English. MMLU's format matches the primary interaction modality.
- **Deployment relevance:** For the majority English-language user cohort, MMLU's format creates no signal-distribution mismatch. Questions are well-formed, unambiguous in structure, and test reading comprehension at an appropriate register for educated adult users.
- **Datapoint citations:**
  - [D6] professional_law, Ex1: "A truck driver was assigned to drive a huge tractor-trailer loaded with logs…" — demonstrates the clear, formal English register used throughout.
  - [D7] professional_law, Ex3: "A patient filed a medical malpractice action against a hospital in federal court" — standard formal English with no dialect or register barriers for educated English speakers.

#### Strength 3: International Law and Human Rights Coverage with Some Global Applicability
- **Dimension(s):** IO, IC
- **Observation:** The `international_law` subject contains questions about treaty-based human rights mechanisms, cultural relativism, and the distinction between public and private acts under international law. These topics have global applicability and touch on norms relevant to all eight deployment countries.
- **Deployment relevance:** Tourists and expats may have general curiosity about human rights frameworks that apply to the Arab world. International law questions are framed abstractly enough to not be exclusively US-anchored.
- **Datapoint citations:**
  - [D39] international_law, Ex4: "What is the meaning of cultural relativism? … Cultural relativism posits that local culture should validate the existence and practice of all human rights" — this question is abstractly framed and relevant to discussions of human rights in Arab-region contexts.
  - [D39] international_law, Ex3: "Is the unlawful homicide committed by Minister of country X abroad an act jure imperii or jure gestionis?" — abstractly framed, not anchored to any specific legal system.

#### Strength 4: Zero-Shot/Few-Shot Evaluation Design Appropriate for Generalization Testing
- **Dimension(s):** OF
- **Observation:** MMLU is designed for zero-shot and few-shot evaluation, probing knowledge acquired during pretraining. For a deployed system that must generalize to novel queries, this evaluation paradigm (rather than fine-tuned task-specific scoring) is more aligned with deployment behavior.
- **Deployment relevance:** Tourists and expats ask unpredictable general knowledge questions. A model evaluated under zero-shot/few-shot conditions demonstrates the same generalization property required for open-domain question answering about Arab history, geography, and language.
- **Datapoint citations:** All sampled examples are zero-shot MCQ without task-specific training — consistent with the deployment's need to evaluate generalization rather than narrow fine-tuned performance.

#### Strength 5: World Religions Subject Nominally Covers Multiple Faith Traditions
- **Dimension(s):** IO
- **Observation:** The `world_religions` subject includes questions on Jainism, Judaism, and Christianity across the six sampled examples. The subject label indicates coverage of multiple world religions, which nominally includes Islam — the dominant religion across all eight deployment countries.
- **Deployment relevance:** Tourists and expats frequently have questions about Islamic practices, the Islamic calendar, and Islamic history, which are core deployment topics. The world_religions subject is the closest available MMLU proxy for this content area.
- **Datapoint citations:**
  - [D17] world_religions, Ex1: "Rome claimed that their bishop (pope) was the direct successor of which leader? … Peter" — Christian content.
  - [D18] world_religions, Ex2: "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" — Jainism content.
  - [D21] world_religions, Ex5: "What is the most important prayer in Judaism? … The Shema" — Jewish content. No Islamic content appeared in the six sampled world_religions examples, but the subject label does not preclude its presence in the full 171-question set.

#### Strength 6: High School World History Includes Some Non-Western Primary Sources
- **Dimension(s):** IC
- **Observation:** The `high_school_world_history` subject includes non-Western and non-European primary sources. Among the five sampled examples, one is drawn from an ancient Persian inscription (Kerdir at Naqsh-e-Rustam), one from an African anti-colonial theorist (Kwame Nkrumah), and one from a British account of Indian colonialism. This demonstrates that the subject does not exclusively cover Western European history.
- **Deployment relevance:** The deployment requires school-level world history knowledge including pre-Islamic Middle Eastern history. The Persian inscription example shows the subject can include content from the broader Middle East/Central Asia region.
- **Datapoint citations:**
  - [D16] high_school_world_history, Ex5: "Excerpt from the inscription of Kerdir at Naqsh-e-Rustam, Persia, late third century C.E. … Jews, Buddhists, Hindus, Nasoreans, Christians, Maktak, and Manichaeans in the empire were smitten" — Near Eastern content, though pre-Islamic and Persian rather than Arab.
  - [D37] high_school_world_history, Ex4: "Kwame Nkrumah, Neo-Colonialism, 1965 … 'A State in the grip of neo-colonialism is not master of its own destiny.'" — African post-colonial perspective, showing non-Western framing is possible.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: No Arab-Region Subject Categories in the 57-Subject Taxonomy
- **Dimension(s):** IO
- **Observation:** Across all 57 MMLU subject configurations, not one is dedicated to Arab history, Middle Eastern geography, Arabic language, Islamic jurisprudence, or any sub-regional Arab topic. The subject list is exhaustively confirmed from the HF metadata: subjects include `high_school_us_history`, `high_school_european_history`, `high_school_government_and_politics` (US-framed), and `us_foreign_policy` — but no Arab history, no MENA geography, no Islamic law or culture.
- **Deployment relevance:** The deployment is specifically designed to answer questions about Arab history, regional geography, and Arabic language across eight Arab countries. The complete absence of dedicated Arab-region subjects means MMLU cannot evaluate whether a model knows anything useful for the core deployment domain. This is a structural gap, not a sampling artifact.
- **Datapoint citations:**
  - [D1] high_school_government_and_politics, Ex1: "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" — one of five government/politics examples, all US-institutional.
  - [D10] us_foreign_policy, Ex4: "In American government, the power to declare war rests with Congress." — The "Foreign Policy" subject is entirely framed from a US perspective with no Arab-country policy questions in the sample.
  - [D3] high_school_government_and_politics, Ex4: "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" — US-specific legislation.

#### CRITICAL Concern 2: Global Facts Subject Excludes Arab Countries in Sampled Questions
- **Dimension(s):** IO, IC
- **Observation:** `global_facts` is the subject most likely to contain Arab-region statistical questions. All five sampled examples reference China (2), India (3), Mexico (1), and an Africa/Korea comparison (1). No Arab country appears in any of the five sampled global_facts questions.
- **Deployment relevance:** The deployment covers general school-level knowledge about the Arab world, including geography and demography. If `global_facts` — the subject most suited to cross-regional factual knowledge — contains no Arab-country questions even in a sample of five, this signals extremely low Arab-region density.
- **Datapoint citations:**
  - [D22] global_facts, Ex1: "About what percentage of survey respondents from China report having paid a bribe…" — China-focused.
  - [D23] global_facts, Ex2: "As of 2017, what fraction of the population in India used the internet…" — India-focused.
  - [D24] global_facts, Ex3: "As of 2019, which of the following had the lowest life expectancy? … Mexico" — Latin American comparison.
  - [D25] global_facts, Ex4: "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … makes it a better place to live?" — India-focused.
  - [D26] global_facts, Ex5: "At the time of independence, there were already hundreds of thousands of university graduates in India, but hardly any at all in Congo" — Africa/Asia comparison.

#### CRITICAL Concern 3: Moral Scenarios Explicitly Anchored to "US Standards as of 2020"
- **Dimension(s):** OC, OO
- **Observation:** Every sampled `moral_scenarios` example contains the explicit phrase "according to ordinary moral standards in the US as of 2020." This is not merely an implicit cultural bias — it is a stated label constraint encoding US moral standards as the ground truth. For users asking about moral or social norms in Arab countries, this labeling scheme encodes a directly contradictory cultural standard.
- **Deployment relevance:** The deployment system serves users in eight Arab countries where moral norms around alcohol, gender relations, family honor, public behavior, and religious observance diverge significantly from "US standards as of 2020." For any Arab-region moral or social knowledge domain, MMLU's moral_scenarios ground-truth labels are categorically misaligned with local stakeholder judgments.
- **Datapoint citations:**
  - [D12] moral_scenarios, Ex1: "For which of these two scenarios does the main character do something clearly morally wrong, according to ordinary moral standards in the US as of 2020? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot." — US moral framing as explicit label criterion.
  - [D13] moral_scenarios, Ex2: "according to ordinary moral standards in the US as of 2020? Scenario 1 | When I went through the road block I gave the policeman my brothers ID." — identity document fraud scenario judged by US standards.
  - [D14] moral_scenarios, Ex3: "according to ordinary moral standards in the US as of 2020? Scenario 2 | I was due to start work soon, so I went to a baseball game." — baseball as a culturally embedded reference in a moral reasoning task.

#### CRITICAL Concern 4: World History Arab-Region Absence; Middle East Appears Only as Ancient Persia and Agricultural Origin
- **Dimension(s):** IO, IC
- **Observation:** Across five sampled `high_school_world_history` examples, the Middle East/Arab region appears exactly once — in a Sasanian Persian inscription from the 3rd century CE (pre-Islamic, non-Arab). No Arab nationalist history, no Ottoman period, no Islamic civilization, no 20th-century Arab state formation, no Palestinian history, and no Levantine, Egyptian, or Gulf-specific content appears. The prehistory subject mentions the Middle East only as the origin of cattle domestication (~10,500 years ago).
- **Deployment relevance:** The deployment's core subject matter includes Arab history from the Islamic Golden Age through modern state formation. The near-complete absence of Islamic and Arab-period history in the world history and prehistory subjects means MMLU cannot assess a model's knowledge of the content tourists and expats most frequently ask about.
- **Datapoint citations:**
  - [D16] high_school_world_history, Ex5: "Excerpt from the inscription of Kerdir at Naqsh-e-Rustam, Persia, late third century C.E." — only Middle East reference in the five world history examples; pre-Islamic, Persian, not Arab.
  - [D36] prehistory, Ex4: "Archaeological evidence indicates that cattle were first domesticated where and how long ago? … in the Middle East, about 10,500 years ago" — Middle East mentioned only as an ancient agricultural origin, no cultural content.
  - [D29] high_school_european_history, Ex1: "Leeds Woolen Workers Petition, 1786" — European industrial history.
  - [D30] high_school_european_history, Ex2: "Voltaire, Letters on the English Nation, 1733" — European Enlightenment.

#### CRITICAL Concern 5: US Foreign Policy Subject Framed Entirely from US Perspective
- **Dimension(s):** IO, IC, OC
- **Observation:** All five sampled `us_foreign_policy` examples are framed from within US institutional and policy perspectives — NSC 68, War Powers Act, NSA surveillance, "Philadelphian System" exceptionalism. For a deployment covering Arab countries where US foreign policy is a contested and politically sensitive topic (Gulf War, Arab-Israeli conflict, Iraq War), the US-centric framing encodes one perspective as the correct answer.
- **Deployment relevance:** Users asking about US foreign policy in the Arab world — a frequent tourist/expat query about why certain regional conditions exist — will receive answers framed from a US perspective that may contradict the perspectives of host-country citizens in Jordan, Palestine, Lebanon, and Egypt.
- **Datapoint citations:**
  - [D9] us_foreign_policy, Ex3: "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" — entirely US institutional framing.
  - [D11] us_foreign_policy, Ex5: "Revelations that the NSA was monitoring the communications of American citizens without obtaining warrants" — US domestic civil liberties framing of surveillance.

---

#### MAJOR

#### MAJOR Concern 1: Professional Law, Jurisprudence, and Human Aging Encode US Institutional Specifics
- **Dimension(s):** IO, IC, OC
- **Observation:** The `professional_law` subject (500 test examples, the largest in MMLU) consists entirely of US common law scenarios — tort law, contract law, evidence rules, DUI statutes, federal court procedure. `human_aging` references US Social Security age thresholds and alcohol abuse rates among "Americans." These questions have no validity for an Arab-region deployment where legal systems are based on civil law (Morocco, Egypt), Islamic law (Saudi Arabia, Kuwait), or mixed systems (Lebanon, Jordan).
- **Deployment relevance:** Tourists and expats may ask general legal questions (e.g., "What are my rights?" or "How does property law work here?"). A model evaluated on MMLU professional law has been tested only on US common law knowledge, which may actively mislead users about Arab legal systems.
- **Datapoint citations:**
  - [D6] professional_law, Ex1: "A truck driver was assigned to drive a huge tractor-trailer loaded with logs…" — US tort law.
  - [D8] professional_law, Ex5: "A buyer filed a lawsuit against a seller based on a written contract allegedly executed at the time of the sale of the seller's hot dog stand" — US contract law.
  - [D32] human_aging, Ex3: "The age at which one can receive full benefits from social security … Has been increasing" — US social security specifics.
  - [D33] human_aging, Ex4: "Which of the following groups of Americans have the lowest rate of alcohol abuse? … Asian-American" — US demographic categories.

#### MAJOR Concern 2: High School Government and Politics Is Exclusively US Government
- **Dimension(s):** IO, IC
- **Observation:** All five sampled `high_school_government_and_politics` questions concern US constitutional structure — First Amendment, federal-state relations, Articles of Confederation, War Powers Act, Congressional representation. There is no comparative government content, no coverage of Arab governance structures (monarchies, tribal councils, military governments), and no non-US political systems.
- **Deployment relevance:** Tourists and expats visiting Arab countries frequently ask about governance structures, political history, and civic life. MMLU's government subject cannot evaluate a model's knowledge of Hashemite monarchy, Gulf tribal governance, Lebanese confessionalism, or Egyptian political history.
- **Datapoint citations:**
  - [D1] high_school_government_and_politics, Ex1: "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" — US constitutional law.
  - [D2] high_school_government_and_politics, Ex2: "In the majority of cases, federal programs are implemented by state and local governments, by means of federal funding" — US federal structure.
  - [D3] high_school_government_and_politics, Ex4: "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" — US-specific legislation.

#### MAJOR Concern 3: World Religions Sample Shows No Islamic Content; Coverage Depth Unknown
- **Dimension(s):** IO, IC
- **Observation:** Six sampled `world_religions` examples include content on Christian ecclesiastical succession, Jainism (2 questions), Jewish prayer, Daoist text, and Christian Gospels. Zero of the six sampled examples cover Islam. While the full 171-question set may include Islamic content, the absence from the sample raises concerns about proportion and framing.
- **Deployment relevance:** Islam is the dominant religion across all eight deployment countries and a primary topic of tourist/expat curiosity (Islamic calendar, Ramadan, prayer practices, mosque etiquette as general knowledge). A model evaluated only on Christian, Jain, and Jewish content will not have been tested on the religious knowledge most relevant to the deployment.
- **Datapoint citations:**
  - [D17] world_religions, Ex1: "Rome claimed that their bishop (pope) was the direct successor of which leader? … Peter" — Christianity.
  - [D18] world_religions, Ex2: "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" — Jainism.
  - [D19] world_religions, Ex3: "Which are the synoptic Gospels? … Matthew, Mark, Luke" — Christian Biblical content.
  - [D20] world_religions, Ex4: "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" — Jainism.
  - [D21] world_religions, Ex5: "What is the most important prayer in Judaism? … The Shema" — Judaism.

#### MAJOR Concern 4: Single-Answer MCQ Label Schema Cannot Accommodate Multi-Perspective Contested Topics
- **Dimension(s):** OO, OC
- **Observation:** MMLU's output schema enforces exactly one correct answer per question (A, B, C, or D). The deployment requirement — to acknowledge multiple perspectives on contested historical/political topics and flag political sensitivity — is structurally incompatible with this scoring paradigm. Across all 290+ sampled examples, every question has exactly one labeled correct answer with no mechanism for flagging contestedness.
- **Deployment relevance:** Key deployment topics — the 1948 war/Nakba framing, Western Sahara status, Lebanese Civil War causes, Palestinian statehood, Ottoman legacy — require multi-perspective responses. MMLU cannot score a model that says "this topic is contested; here are two perspectives" — such a response would score 0% on MMLU regardless of its accuracy for deployment purposes.
- **Datapoint citations:**
  - [D12] moral_scenarios, Ex1 through [D14] moral_scenarios, Ex3: all examples have a single binary label; no partial credit or multi-perspective acknowledgment is possible.
  - [D9] us_foreign_policy, Ex3: "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" — one correct answer asserted; no acknowledgment of contested Cold War historiography.
  - [D15] high_school_world_history, Ex2: "According to the second passage, the Cawnpore Massacre … can be viewed as a reaction to the systemic brute force with which the British governed India" — colonial framing resolved to single answer from secondary source.

#### MAJOR Concern 5: High School Geography Framed Around US Urban Models and US Religious Demographics
- **Dimension(s):** IO, IC
- **Observation:** Five sampled `high_school_geography` questions include: Islam as the "most rapidly growing religion in the United States" (US-contextual framing), a globe/map projection question, pastoralism definition, core-periphery development model, and Burgess's concentric zone model of US urban form. None concern Arab-world physical geography, political geography, or spatial concepts relevant to Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, or KSA.
- **Deployment relevance:** The deployment covers regional geography of eight Arab countries. MMLU's high school geography content evaluates US-anchored urban sociology models and US religious demographics rather than physical or political geography of the Arab world.
- **Datapoint citations:**
  - [D27] high_school_geography, Ex1: "What is the most rapidly growing religion in the United States today? … Islam" — Islam mentioned only in US demographic context.
  - [D28] high_school_geography, Ex5: "Which zone contains low-income slums, ethnic ghettos, and general deterioration in Burgess's concentric zone model of urban form?" — US urban sociology model.

#### MAJOR Concern 6: Human Sexuality and Human Aging Encode US-Specific Survey Data as Ground Truth
- **Dimension(s):** IC, OC
- **Observation:** `human_sexuality` questions cite US statistics (most common US contraceptive method, US heterosexual partner counts 1988–1990), and `human_aging` references US Social Security and US ethnic group alcohol abuse rates. These ground-truth labels reflect US-population norms that diverge substantially from Arab-region norms around sexuality, family planning, gender relations, and social welfare.
- **Deployment relevance:** Tourists and expats may ask general questions about social norms, health practices, and demographics. A model evaluated on US-population ground truths for these topics will have been reinforced with knowledge claims that contradict Arab-region realities (e.g., contraceptive prevalence, attitudes toward sexuality, alcohol norms).
- **Datapoint citations:**
  - [D34] human_sexuality, Ex1: "Which of the following is the most common method of birth control for married couples in the U.S. … Sterilization" — US-specific reproductive health statistic as ground truth.
  - [D35] human_sexuality, Ex5: "From 1988 to 1990 among heterosexuals in the US, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women" — US behavioral survey data.
  - [D33] human_aging, Ex4: "Which of the following groups of Americans have the lowest rate of alcohol abuse? … Asian-American" — alcohol abuse among American ethnic groups.

---

#### MINOR

#### MINOR Concern 1: High School European History Dominates Non-US History Slot
- **Dimension(s):** IO
- **Observation:** MMLU has a dedicated `high_school_european_history` subject but no equivalent for world history outside Europe and the US. The five sampled European history examples cover British industrialization, Voltaire, Pico della Mirandola, Medici-era Neoplatonism, and the Royal Society. This dedicated European history slot confirms that non-European, non-US histories are subordinated to the catch-all `high_school_world_history` subject.
- **Deployment relevance:** Arab history from the Islamic Golden Age, the Ottoman period, or modern state formation has no dedicated subject and must compete with all other non-European world history for representation in a single 237-question subject.
- **Datapoint citations:**
  - [D29] high_school_european_history, Ex1: "Leeds Woolen Workers Petition, 1786 … The sentiments expressed by the Leeds woolen workers illustrate which of the following historical trends?" — British industrial history.
  - [D30] high_school_european_history, Ex2: "Voltaire, Letters on the English Nation, 1733" — French Enlightenment.

#### MINOR Concern 2: Business Ethics Civil Society Question Omits Arab World from Options
- **Dimension(s):** IC
- **Observation:** A `business_ethics` question asks about countries with less developed civil society compared to a more developed example. The correct answer is "Russia, China, Britain" — the Arab world is not even presented as an option in this question about global civil society development.
- **Deployment relevance:** This is a minor individual instance, but it illustrates how MMLU's question design treats Arab countries as outside the scope of even comparative global analysis.
- **Datapoint citations:**
  - [D31] business_ethics, Ex5: "Although the benefit and contribution of civil society in encouraging sustainability … in many other countries, such as _____ and ______ civil society is far less developed than in, for instance, _______. … Russia, China, Britain" — Arab world entirely absent from the answer options for a global civil society comparison question.

#### MINOR Concern 3: Prehistory and Archaeology Show Selective Middle East Coverage
- **Dimension(s):** IC
- **Observation:** The `prehistory` subject contains a question correctly identifying the Middle East as the origin of cattle domestication ~10,500 years ago. However, this represents the region only as a prehistoric agricultural site, not as a culturally meaningful historical location. Other prehistory questions cover Stonehenge, Machu Picchu, Chinese civilization origins, and African butterfly species.
- **Deployment relevance:** For users curious about the deep history of the Arab region, the prehistory subject does contain one relevant data point. However, coverage is incidental rather than systematic, and the framing is archaeological rather than cultural.
- **Datapoint citations:**
  - [D36] prehistory, Ex4: "Archaeological evidence indicates that cattle were first domesticated where and how long ago? … in the Middle East, about 10,500 years ago" — region mentioned as agricultural origin only.

#### MINOR Concern 4: Professional Psychology US-Centric Research Norms
- **Dimension(s):** IC
- **Observation:** `professional_psychology` references US mental health norms (PKU treatment, minority/nonminority client effectiveness, crisis therapy frameworks). These norms reflect US clinical psychology literature and may not transfer to Arab-region mental health contexts or cultural attitudes toward therapy.
- **Deployment relevance:** Minor for this deployment, which focuses on history, geography, and language rather than psychology. However, to the extent users ask general knowledge questions about psychology or mental health, the US-clinical framing introduces cultural mismatch.
- **Datapoint citations:**
  - [D43] professional_psychology, Ex2: "With regard to minority and nonminority clients, psychotherapy is … equally effective" — US racial/ethnic minority framing of clinical effectiveness research.

---

### Content Coverage Summary

The 290+ sampled MMLU examples across 57 subjects confirm the following characterization:

**Dominant content register:** US academic curriculum (high school through professional level), drawing on US standardized tests, US undergraduate course materials, and Western European academic publications. The register is formal, English-only, and assumes familiarity with US institutional structures (federal government, common law, social security, US ethnic demographics).

**Subject concentration relevant to deployment:** Nominally relevant subjects (`high_school_world_history`, `high_school_geography`, `world_religions`, `global_facts`, `international_law`, `security_studies`) contain either no sampled Arab-region content (`global_facts`, `world_religions`, `high_school_geography`) or incidental references to the broader Middle East (`prehistory`: one question; `high_school_world_history`: one Sasanian Persian inscription).

**Subjects with zero Arab-region relevance:** `high_school_us_history`, `high_school_government_and_politics`, `us_foreign_policy`, `professional_law`, `human_sexuality`, `human_aging` — together comprising several hundred questions — are anchored in US-specific institutional, legal, and demographic contexts that transfer nothing meaningful to the Arab-region deployment.

**Moral and social content:** The `moral_scenarios` subject explicitly labels correct answers as "ordinary moral standards in the US as of 2020," creating a direct conflict with Arab-region moral frameworks on topics including alcohol, gender relations, family structures, and religious observance.

**Language:** Entirely English. No Arabic-script content, no dialect questions, no Arabic language instruction questions. The secondary Arabic-learning user cohort is unservable by this benchmark.

**Non-Western content that does appear:** The world history subject contains non-Western sources (Nkrumah, Kerdir inscription), and prehistory touches the Middle East as an agricultural origin point. These are the strongest evidence against total Western monoculture, but they are scattered and do not constitute systematic Arab-region coverage.

---

### Limitations

1. **Sample size per subject:** 5–6 examples per subject from the test split. For subjects with 237 questions (`high_school_world_history`) or 500 questions (`professional_law`, `moral_scenarios`, `professional_psychology`), the sample cannot confirm or rule out rare Arab-region content. It is possible that a small number of world history questions cover Islamic or Arab-period history not captured in the sample.

2. **World religions Islam content:** Six sampled world_religions examples showed no Islamic content. The full 171-question set may contain Islamic questions (possibly covering the Five Pillars, hadith, early Islamic history), but the framing perspective (Western academic vs. Islamic scholarly) cannot be determined from the sample.

3. **Security studies depth:** The security studies subject (245 questions) was sampled at 5 examples, all covering abstract IR theory. This subject might contain questions touching on Middle East security dynamics, but none appeared in the sample.

4. **Miscellaneous subject:** The `miscellaneous` subject (500+ questions) is a catch-all that could contain Arab-region factual questions. The five sampled examples (traffic lights, labor force, geometry, proletariat, material resistance) show no Arab-region content, but coverage uncertainty is high for this heterogeneous category.

5. **Auxiliary train split:** The auxiliary_train examples sampled are all US law scenarios, but this split was not systematically sampled across subjects — it represents only a subset of the training data.

6. **No access to question-level metadata on source:** The dataset does not expose which specific source documents each question came from, preventing confirmation of which questions originated from GRE, USMLE, Oxford Press, etc., vs. other sources that might include non-US content.

7. **Full quantitative coverage audit impossible from sample:** A definitive count of Arab-region questions across all 15,908 MMLU items would require inspecting every question — beyond what a sample-based analysis can provide. The web search finding that no published quantitative audit exists for original English MMLU Arab-region content proportion remains unresolved.

