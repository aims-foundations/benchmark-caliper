## Deployment Context

**Use case:** Task: Environment science and geograpy-specific agricultural knowledge understanding
LLMs evaluated: Generic frontier model vs small llms as well as region specific llms
Domain: Environmental science
Setting: Environment science research utility assessment using llm and local-context
**Target population:** An environment scientist from Mymensingh, Bangladesh wants to get knowledge about different south asian region specific agricultural practice. So having different region and language specific agricultural and demographic context understanding (e.g. telegu spoken area, hydrabad India and agricultural practice/problems vs farmers practice/problems from Mymensingh, Bangladesh~bengali spoken in Mymensingh accented dialect.)

# Validity Analysis: milu
**Target context:** Mymensingh Environmental Scientist — Cross-Regional South Asian Agricultural Knowledge
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 3 | Moderate gaps | high |
| Output Ontology | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 3 | Moderate gaps | high |
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

MILU is fundamentally misaligned with the Mymensingh environmental-scientist deployment context. The benchmark is by design India-centric across all six validity dimensions: its 41-subject taxonomy lacks Bangladesh-specific agro-ecological subdomains; its content originates exclusively from Indian competitive exams with no Bangladeshi farming, dialect, or trans-border hydrology representation; its Bengali corpus reflects West Bengal exam register and is heavily machine-translated (100% of the sampled validation Bengali split); its annotation pool excluded Bangladeshi subject-matter experts; and its single-correct-answer MCQ format cannot accommodate the cross-border knowledge pluralism that trans-border water-policy questions demand. Dataset analysis empirically confirms these structural gaps: Bangladesh appears in 215 sampled examples only as a wrong-answer distractor, Agriculture-labeled questions concern Indian schemes and corporate trivia rather than agronomy, and Telangana/AP agro-ecological content is absent. MILU's strengths — broad Indic-script coverage, consistent MCQ structure, broad domain diagnostic breadth — make it useful as a generic Indic-LLM screening tool, but it provides essentially no discriminative signal for Bangladeshi agricultural and environmental science knowledge.

## Practical Guidance

### What This Benchmark Measures

MILU measures Indian competitive-exam general knowledge across 11 Indic languages and 8 broad domains. For the Mymensingh deployment, it can usefully measure (a) whether candidate LLMs render Bengali and Telugu scripts correctly (input_form strength) and (b) whether they have basic STEM and general-knowledge capability across Indic languages (output_form strength enables cross-model comparison). It cannot measure agricultural science depth, Bangladeshi agro-ecological knowledge, trans-border policy reasoning, or Bangladeshi Bengali register competence — the core constructs the deployment cares about.

### Construct Depth

Construct depth is shallow for the target deployment. Even within the relevant Environmental Sciences domain, sampled content is geography trivia and Indian-policy-scheme recall, not agronomic, soil-science, or wetland-ecology reasoning (input_ontology score 2, input_content score 1). The Agriculture subject label exists but maps to institutional and corporate trivia. MILU provides surface-level breadth without the technical depth a professional environmental scientist would need to assess LLM reliability for their query workload.

### What Else You Need

Significant supplementation is required: (a) a Bangladesh-specific agricultural knowledge benchmark covering haor/beel/char-land systems and boro/aman cycles (none currently exists per GAP-1, GAP-8); (b) BEnQA [WEB-6] as a Bangladeshi Bengali register baseline to disentangle language-competence from cultural-knowledge gaps; (c) a trans-border policy benchmark with pluralistic ground-truth structure to address output_ontology and output_content gaps; (d) Telangana/AP sub-regional agro-ecological items if cross-reference zones are core to the use case; and (e) generation-mode and CoT evaluation to address [Q85] log-likelihood limitations for reasoning-heavy queries.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
MILU's 41-subject taxonomy includes an Environmental Sciences domain and an Agriculture subject, but both are surface-level and India-scoped by design [Q19, Q38]. The taxonomy lacks any Bangladesh-specific agro-ecological subdomains — no haor/beel wetland category, no char-land farming, no boro/aman rice cycle subject, and no trans-border water management category. Dataset analysis confirms this empirically: across 215 sampled examples, Environmental Sciences is populated almost entirely with geography trivia (DATASET-D6, D9, D16, D18) rather than agro-ecological science, and the few Agriculture-labeled questions concern Indian schemes/institutions (DATASET-D10, D13, D14). The authors themselves note poor model performance in 'culturally relevant areas' [Q6, Q68] which the deployment population would consider their core expertise. For a HIGH-priority deployment requiring agro-ecological depth across Bangladeshi delta and Indian cross-reference zones, the taxonomy is materially underrepresentative.

**Strengths:**
- MILU's taxonomy does include an Environmental Sciences domain and an Agriculture subject label that appears across multiple Indic languages, providing at least minimal coverage of the relevant domain category [Q38, DATASET-D10, DATASET-D13]
- The 8-domain × 41-subject structure offers broad coverage breadth that enables comparative diagnosis of model capabilities across general knowledge areas, useful as a baseline screening tool [Q1, Q18]

**Checklist:**

- **IO-1**: Required categories for the deployment include: haor/beel wetland ecology, char-land floodplain agriculture, boro/aman/aus rice cultivation systems, trans-border river hydrology (GBM system), Telangana dry-land cropping (cotton/sorghum/pigeonpea on Deccan red/black soils), Andhra Pradesh coastal aquaculture (L. vannamei/P. monodon under CAA/MPEDA frameworks), and integrated crop-fish farming. None of these appear as named subjects in MILU's 41-subject taxonomy [Q38]. — _Sources: Q38_
- **IO-2**: Yes — the taxonomy omits all Bangladesh-specific agro-ecological categories. The deployment YAML confirms this is structurally absent (GAP-1 resolution: 'CONFIRMED STRUCTURALLY ABSENT' [WEB-17]), and dataset analysis confirms no haor/beel/char/boro/aman content appears in 215 sampled examples (CRITICAL Concern 1: DATASET-D10, D13, D14, D15). — _Sources: WEB-17, DATASET-D10, DATASET-D13, DATASET-D14, DATASET-D15_
- **IO-3**: Many MILU subjects are India-centric civic/cultural categories (Indian constitutional law, Indian state polity, medieval Indian history) that introduce construct-irrelevant variance for an environmental-science deployment. Dataset evidence: DATASET-D2 (1991 Indian fiscal crisis), D5 (Indian Election Commissioner removal), D19 (Bahmani Kingdom), D27 (Radcliffe Line), D28 (44th Constitutional Amendment) — none relevant to agricultural/environmental science. — _Sources: DATASET-D2, DATASET-D5, DATASET-D19, DATASET-D27, DATASET-D28_
- **IO-4**: The category gap encompasses (a) absent wetland/floodplain ecology subdomains, (b) absent trans-border hydrology subdomain, (c) absent technical agronomy depth (soil science, crop physiology, irrigation) — only policy/institutional trivia appears under 'Agriculture' (CRITICAL Concern 1, MAJOR Concern 5). This constitutes substantial construct underrepresentation for the deployment. — _Sources: Q6, Q19, DATASET-D10, DATASET-D13, DATASET-D18_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q19] 'MILU is designed as a culturally relevant benchmark to assess general problem-solving abilities and India-specific knowledge.' (p.3)
- [Q38] 'we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies.' (p.4)
- [Q6] 'Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM.' (p.1)
- [Q82] 'First, we restricted our study to the top 11 languages due to the lack of readily available questions in low-resource languages, which we aim to address in future work.' (p.9)

*Web sources:*
- [WEB-17] AI4Bharat/MILU GitHub confirms 8 domains × 41 subjects with India-centric design
- [WEB-18] NAACL paper confirms India-only sourcing and taxonomy

*Dataset analysis:*
- DATASET-D10: Only Bengali Agriculture-labeled question concerns India's National Food Security Mission, not Bangladeshi farming
- DATASET-D13: Marathi Agriculture question asks location of National Mustard Research Centre (Sever, Rajasthan) — institutional trivia not agronomy
- DATASET-D14: Odia Agriculture question asks which Indian company makes farm equipment — corporate trivia
- DATASET-D18: Environmental Sciences domain populated with Mediterranean climate trivia, not agro-ecology
- DATASET-D9: Environmental Sciences/Geography subject contains Telangana welfare-pension question — taxonomy applied loosely

</details>

**Information gaps:**
- Exact subject-level question counts in Environmental Sciences for Bengali and Telugu test split (Table 9 not directly accessible)
- Whether any Telugu test questions include Telangana/AP sub-regional agro-ecological content (sample of 25 validation examples cannot rule in/out)

**Requires expert verification:**
- A Bangladeshi agronomist's assessment of which specific subdomains would be required at minimum for a baseline professional-knowledge benchmark

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Every datapoint in MILU originates from Indian competitive exams [Q9, Q11, Q20, Q24, Q93]. The deployment YAML and web search confirm structural absence of Bangladeshi content (GAP-1, GAP-6 [WEB-17, WEB-18]). Dataset analysis confirms this empirically: across 215 sampled examples, Bangladesh appears only as a wrong-answer distractor in two questions about Indian Pharmacopoeia (DATASET-D21, D25), and no Bangladeshi institution, ecological system, or trans-border policy appears anywhere in the sample (CRITICAL Concern 1). Bengali content is West Bengal exam-derived, with the entire validation Bengali sample being machine-translated from English (DATASET-D3, all 21 examples). Telugu content shows no Telangana/AP agro-ecological specificity (MAJOR Concern 6). For a HIGH-priority dimension targeting Bangladeshi farming context, Mymensingh dialect terminology, haor wetlands, and trans-border hydrology, the content is essentially zero — a fundamental misalignment.

**Strengths:**
- MILU does include English questions specifically chosen to address South Asian culture-specific content [Q26], offering some pan-South-Asian general knowledge value
- West Bengal-derived Bengali content shares deltaic ecology context with Mymensingh and may carry partial transferable agronomic relevance for the West Bengal cross-reference zone (though depth is unconfirmed)

**Checklist:**

- **IC-1**: Yes — the deployment requires Bangladeshi agro-ecological knowledge (haor, beel, char-land, boro/aman cycles), Mymensingh dialect agricultural terminology, and cross-border GBM hydrology. None of this is present in the sampled MILU content (CRITICAL Concern 1) and the YAML confirms structural absence ([WEB-17] AI4Bharat/MILU GitHub). — _Sources: Q9, Q11, WEB-17, DATASET-D1_
- **IC-2**: Cultural alignment is poor: MILU's Bengali corpus reflects West Bengal exam register conventions, not Bangladeshi register. The expert elicitation (A2) noted 'potentially slight implicit Indian Bengali stylistic bias' and confirmed dialect-specific Bangladeshi agricultural terminology is absent. Dataset analysis: 100% of sampled Bengali validation items are machine-translated (DATASET-D3), compounding register mismatch. — _Sources: Q24, DATASET-D3_
- **IC-3**: Many inputs require Indian-specific knowledge that does not transfer: Indian constitutional procedure (DATASET-D5, D28), Indian state assembly elections (DATASET-D4), Indian medieval/colonial history (DATASET-D19, D38), Indian corporate brands (DATASET-D14, D33). These contribute construct-irrelevant variance for an environmental-science evaluation. — _Sources: DATASET-D5, DATASET-D28, DATASET-D4, DATASET-D19, DATASET-D14_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no Bangladeshi annotators participated in MILU construction (GAP-6 resolution: 'CONFIRMED ABSENT' [WEB-17, WEB-18]). For the deployment, Bangladeshi agronomist review of any MILU-relevant subset would be required to flag culturally sensitive instances. — _Sources: WEB-17, WEB-18_
- **IC-5**: Documented content issues: (a) zero Bangladesh-specific datapoints, (b) Bengali content sourced from West Bengal exams [Q24], (c) ~25% machine-translated overall [Q43] with the validation Bengali split observed at 100% translated (DATASET-D3), (d) Bangladesh appears only as distractor (DATASET-D21, D25). These cumulatively violate content validity for the target deployment. — _Sources: Q24, Q43, DATASET-D3, DATASET-D21, DATASET-D25_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams.' (p.2)
- [Q11] 'We create this benchmark by collecting questions from over 1500 competitive exams from India.' (p.2)
- [Q24] 'Regional state exams are particularly valuable as they cover various state-level topics and emphasize the official language of each state.' (p.3)
- [Q43] 'Of the total 79K questions, only 25% of questions are translated from English' (p.4)
- [Q93] 'We collected our questions from over 40 exam types ranging from various National and state level civil service examinations to examinations conducted by various government and private organizations.' (p.17)

*Web sources:*
- [WEB-17] AI4Bharat/MILU GitHub confirms exclusively India-centric exam sourcing
- [WEB-18] NAACL paper confirms no Bangladeshi exam corpus
- [WEB-6] BEnQA exists as a separate Bangladeshi Bengali science benchmark, but is not integrated into MILU

*Dataset analysis:*
- DATASET-D1: National Food Security Mission Bengali question — Indian scheme, no Bangladesh context
- DATASET-D2: India's 1991 foreign reserve crisis — Indian economic history
- DATASET-D4: AAP wins Punjab assembly elections — Indian state polity
- DATASET-D21: Bangladesh appears only as wrong-answer distractor (Indian Pharmacopoeia question)
- DATASET-D25: Same Pharmacopoeia question in Telugu, Bangladesh again only as distractor
- DATASET-D33: Telangana T-Hub tech incubator — Telangana surfaces in non-agricultural context only

</details>

**Information gaps:**
- Whether the test split (vs validation) contains a higher proportion of original (non-translated) Bengali questions (DATASET limitation 1)
- Quantitative subject-level question counts for Agriculture/Environmental Science in Bengali and Telugu test splits (GAP-4 not resolved [WEB-18])

**Requires expert verification:**
- A Bangladeshi linguist's assessment of register/terminology drift in MILU's machine-translated Bengali items

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
MILU's text-based MCQ format is technically compatible with the deployment's text-only modality, and Bengali and Telugu scripts are reliably rendered (DATASET strengths 1, 4). However, two concerns reduce alignment: (a) the exam-register MCQ phrasing differs from naturalistic professional-query style (elicitation A4), and (b) approximately 25% of questions are machine-translated [Q43], with the sampled Bengali validation split observed at 100% translated (DATASET-D3, CRITICAL Concern 2), introducing register artifacts and occasional pipeline quality issues including incomplete question stems (DATASET-D34, D35, D36 — MINOR Concern 8). For a MODERATE-priority dimension where script support is the floor requirement, MILU clears that bar but does not match the naturalistic register a Mymensingh domain expert would use.

**Strengths:**
- Bengali and Telugu scripts are fully populated in 215 sampled examples (DATASET Strength 1: D3, D31), confirming script-level encoding compatibility for the deployment's primary languages
- Multiple cleaning layers were applied — INDICLID language ID, Unicode filtering, deduplication, manual spot-checks [Q30, Q31, Q32] — providing baseline data hygiene
- Consistent 4-option MCQ structure across all 11 languages enables reproducible cross-language and cross-model comparison (DATASET Strength 4: D6, D11)

**Checklist:**

- **IF-1**: The text-based signal modality matches deployment needs (both are text). However, register distribution differs: MILU is exam-register MCQ, deployment is naturalistic professional query (elicitation Q4/A4). Script encoding in Bengali and Telugu is verified functional (DATASET-D3, D31). — _Sources: Q29, DATASET-D3, DATASET-D31_
- **IF-2**: Mymensingh has connectivity adequate for text-based LLM access — Bangladesh has ~47% internet penetration with ~100% 4G coverage as of 2025 [WEB-20, WEB-21], and Mymensingh hosts BAU and is a divisional capital [WEB-7]. Text MCQ infrastructure is supported. — _Sources: WEB-20, WEB-21, WEB-7_
- **IF-3**: Domain-specific form differences: (a) machine-translated content carries register artifacts — the YAML notes 'translated questions likely carry Indian Bengali register conventions rather than Bangladeshi Bengali norms', and (b) some translated items have incomplete stems (DATASET-D34, D35) suggesting pipeline degradation. MCQ format also excludes reading-comprehension and image-based queries [Q29], though this is non-binding for the deployment. — _Sources: Q29, Q43, DATASET-D34, DATASET-D35_
- **IF-4**: Form mismatches are moderate: register artifacts from machine translation [Q43, Q84] (DATASET-D3 — 100% translation in Bengali validation), occasional truncated question stems (DATASET-D34, D35, D36), and exam-register vs. naturalistic-query phrasing divergence. None block use, but they reduce ecological validity. — _Sources: Q43, Q84, DATASET-D3, DATASET-D34, DATASET-D36_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q29] 'we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q30] 'we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering (Khan et al., 2024), ensuring that the questions are in the correct language.' (p.4)
- [Q40] 'For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O.' (p.4)
- [Q43] 'Of the total 79K questions, only 25% of questions are translated from English' (p.4)
- [Q84] 'Third, the scarcity of questions necessitated translating a portion of the dataset.' (p.9)

*Web sources:*
- [WEB-20] Bangladesh internet penetration ~47% (2025), 4G coverage ~100% — text modality supported
- [WEB-21] Mobile-dominant connectivity in Bangladesh

*Dataset analysis:*
- DATASET-D3: 100% of 21 sampled Bengali validation items are is_translated=True
- DATASET-D31: Engineering content rendered correctly in Bengali script though machine-translated
- DATASET-D34: Bengali antonym question with target word missing — translation pipeline quality issue
- DATASET-D35: Bengali argument-evaluation question missing argument content — pipeline quality issue
- DATASET-D36: English question with truncated stem

</details>

**Information gaps:**
- Whether the test split (vs validation) has a lower machine-translation rate for Bengali
- Mymensingh-specific connectivity statistics (national aggregates only [WEB-20])

**Requires expert verification:**
- A Bangladeshi Bengali linguist's review of GPT-4O-translated MILU items for register naturalness vs. Indian Bengali bias

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
MILU's output ontology is single-correct-answer MCQ over 41 India-derived subject labels and 8 domains [Q35, Q36, Q37, Q38]. The structural single-correct-label format cannot accommodate cross-border knowledge pluralism on contested topics like trans-border water policy — the deployment YAML identifies this as a HIGH-priority concern (transboundary_policy_context, GAP-3 [WEB-11, WEB-14]). Even if such questions existed, the format would force a single nationally-partial answer key (MAJOR Concern 7: DATASET-D5, D28). The 41-subject labels themselves were derived by clustering ~20K Indian-exam tags [Q35, Q36] and validated against Indian standards. Domain-wise model performance is poor in culturally relevant areas [Q16, Q68], and the authors note a need for 'more inclusive data distribution' [Q70]. For a MODERATE-priority dimension, the structural rigidity plus India-derived label space creates meaningful misalignment, though the basic MCQ correctness structure is functional for non-contested factual content.

**Strengths:**
- The 41-subject taxonomy was derived through systematic clustering and manual review of ~20K fine-grained tags [Q35, Q36, Q37], reflecting principled construction rather than ad-hoc category assignment
- Domain-wise reporting allows users to disaggregate model performance by domain, enabling targeted diagnosis of weak areas like Arts & Humanities and Law & Governance [Q16, Q68]
- Cross-language structural consistency in label space supports comparative evaluation (DATASET Strength 4: D11)

**Checklist:**

- **OO-1**: Output labels are India-validated and India-derived [Q35, Q38]. Regional relevance for Bangladesh is partial: factual STEM labels generally transfer, but governance/law/policy labels reflect Indian constitutional and administrative categories not applicable to Bangladesh (DATASET-D5, D8, D28). — _Sources: Q35, Q38, DATASET-D5_
- **OO-2**: Missing categories: no Bangladesh-specific agro-ecological label space (haor, beel, char-land), no trans-border hydrology label, no cross-border policy category that could accommodate plural answer keys. Confirmed absent [WEB-17, WEB-18]. — _Sources: WEB-17, WEB-18_
- **OO-3**: Indian state polity labels (Maharashtra Legislative Committee, Indian Election Commissioner removal) encode Indian-specific governance assumptions (DATASET-D5, D8, D17). For environmental policy, Indian exam answers would encode India's official water-sharing positions, which differ from Bangladeshi authoritative positions on the Ganges and Teesta [WEB-11, WEB-14]. — _Sources: DATASET-D5, DATASET-D8, DATASET-D17, WEB-11, WEB-14_
- **OO-4**: Stakeholder-driven taxonomy redesign would be required to add (a) wetland ecology subdomains, (b) cross-border policy category supporting plural ground truths, and (c) technical agronomy depth subdomains (soil science, crop physiology, irrigation engineering). — _Sources: Q70_
- **OO-5**: Documented taxonomy issues: India-derived label space [Q35, Q38], single-correct-answer structural rigidity (MAJOR Concern 7), and absence of regional categories. These violate structural validity (taxonomy doesn't fit cross-border pluralism) and content validity (missing categories) for the deployment. — _Sources: Q35, Q38, Q16_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q35] 'Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap.' (p.4)
- [Q36] 'we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters.' (p.4)
- [Q38] 'we determine 41 distinct subject names, which fall into eight main domains' (p.4)
- [Q16] 'Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM.' (p.2)
- [Q70] 'Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages.' (p.7)

*Web sources:*
- [WEB-11] Ganges treaty expires Dec 2026; renewal contested — bilateral ground-truth volatility
- [WEB-14] No Teesta formal treaty exists — categorically contested ground truth
- [WEB-17] AI4Bharat/MILU GitHub confirms India-only taxonomy

*Dataset analysis:*
- DATASET-D5: Indian Election Commissioner removal — Indian constitutional answer encoded as single correct response
- DATASET-D8: Maharashtra Legislative Committee — India-state-specific label
- DATASET-D28: 44th Constitutional Amendment as definitive answer — Indian-specific legal fact
- DATASET-D9: Welfare-pension question classified under Environmental Sciences/Geography — taxonomy applied loosely

</details>

**Information gaps:**
- Exact granularity of subject labels within Environmental Sciences (Agriculture, Geography, Earth Sciences, Environmental Science as separate sub-subjects?) — not directly observable beyond DATASET-D6, D7, D10

**Requires expert verification:**
- A Bangladeshi policy expert's identification of which Indian exam answer keys would be considered authoritative vs. nationally partial for environmental governance questions

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Ground-truth labels originate exclusively from Indian exam portals where 'subject experts ensure the accuracy of the answers' [Q22] and AI4Bharat volunteers conducted manual audits [Q87]. No Bangladeshi annotators, agronomists, or environmental scientists are documented in the annotation pool (GAP-6 resolution: 'CONFIRMED ABSENT' [WEB-17, WEB-18]). Approximately 45% of questions arrived pre-tagged from source portals, with the remainder receiving GPT-4O-MINI-generated topic assignments [Q33, Q34]. There is no documentation of inter-annotator agreement metrics or annotator demographics beyond AI4Bharat affiliation. The expert elicitation (A3) noted Indian exam answers are 'generally considered authoritative' for Bangladeshi environmental scientists, with notable exceptions around trans-border water agreements where Indian answers encode nationally partial perspectives — and the YAML documents that bilateral volatility (Ganges 2026 expiry, Teesta unresolved) makes this gap more acute [WEB-11, WEB-14]. Dataset analysis confirms Bangladesh appears only as wrong-answer distractor (DATASET-D21, D25) — Bangladeshi perspectives are structurally excluded. For a HIGH-priority dimension, this is a substantial convergent-validity concern.

**Strengths:**
- Indian exam-portal source provides documented subject-expert validation pathway for ~45% of pre-tagged questions [Q22, Q33], offering some baseline authority for non-contested STEM facts
- Manual cluster review for subject label assignment [Q37] and AI4Bharat volunteer audits [Q87] provide a layer of human oversight
- For non-contested scientific facts (basic chemistry, biology, physics), expert elicitation (A3) confirms Indian exam answers are generally accepted as authoritative by Bangladeshi environmental scientists

**Checklist:**

- **OC-1**: Ground truth labels reflect Indian exam-portal subject experts and AI4Bharat volunteers [Q22, Q87]. For non-contested STEM facts, this is broadly acceptable to Bangladeshi scientists (elicitation A3). For trans-border policy, governance, and Bangladesh-specific agricultural practice, Indian answers encode partial perspectives [WEB-11, WEB-14]. — _Sources: Q22, Q87, WEB-11, WEB-14_
- **OC-2**: Likely disagreement zones: (a) trans-border river-flow allocation answers, (b) agricultural-policy authority questions where Indian and Bangladeshi national positions differ, (c) Bangladesh-specific cropping-calendar questions (none currently exist in MILU). Elicitation A3 explicitly identified this. Currently, no such questions are present in sampled data, so the disagreement is latent rather than active. — _Sources: WEB-11, WEB-14, DATASET-D5, DATASET-D28_
- **OC-3**: Annotator demographics documented are: Indian exam-portal subject experts [Q22], AI4Bharat team volunteers [Q87], and GPT-4O-MINI for topic-tag assignment [Q34]. No Bangladeshi annotators documented [WEB-17, WEB-18]. No inter-annotator agreement metrics, no demographic breakdown beyond institutional affiliation. INSUFFICIENT DOCUMENTATION on annotator country/region distribution. — _Sources: Q22, Q34, Q87, WEB-17_
- **OC-4**: Re-annotation by a Bangladeshi annotator pool would be required for any deployment-relevant subset, particularly for environmental policy and trans-border water questions. The deployment YAML notes BAU and BARI as candidate institutional sources [WEB-7, WEB-8]. — _Sources: WEB-7, WEB-8_
- **OC-5**: Aggregation method is single-correct-answer MCQ, which by construction erases minority perspectives — a Bangladeshi alternative answer to a contested water-policy question would be marked wrong. Authors do not discuss aggregation alternatives or pluralistic labeling. — _Sources: DATASET-D21, DATASET-D25_
- **OC-6**: Documented label issues: (a) no Bangladeshi annotator participation [WEB-17], (b) no IAA reported, (c) GPT-4O-MINI used for ~55% of topic tagging [Q34] without human verification documented per item, (d) Bangladesh appears only as distractor (DATASET-D21, D25). These violate convergent validity (labels don't correlate with regional perspectives where they would diverge) and external validity for the deployment. — _Sources: Q34, WEB-17, DATASET-D21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers.' (p.3)
- [Q33] 'approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information.' (p.4)
- [Q34] 'we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question.' (p.4)
- [Q37] 'We manually review these clusters and assign appropriate subject labels.' (p.4)
- [Q87] 'We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits.' (p.9)
- [Q70] 'Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages.' (p.7)

*Web sources:*
- [WEB-11] Ganges treaty in renegotiation 2024–2026 — Indian and Bangladeshi positions diverge
- [WEB-14] No formal Teesta treaty; positions categorically differ
- [WEB-17] AI4Bharat/MILU GitHub: no Bangladeshi annotator participation
- [WEB-18] NAACL paper: annotation by AI4Bharat volunteers and Indian exam-portal experts only
- [WEB-7] BAU Mymensingh exists as candidate Bangladeshi institutional annotator source

*Dataset analysis:*
- DATASET-D5: Indian constitutional procedure encoded as definitive correct answer for governance question
- DATASET-D8: Maharashtra state law as single correct answer
- DATASET-D21: Bangladesh appears only as wrong-answer distractor in Pharmacopoeia question
- DATASET-D25: Same Pharmacopoeia question in Telugu — Bangladesh as distractor across languages
- DATASET-D28: 44th Constitutional Amendment Indian law as definitive answer

</details>

**Information gaps:**
- No inter-annotator agreement metrics reported anywhere in MILU documentation
- No demographic breakdown of AI4Bharat volunteer auditors (gender, regional origin, professional discipline)
- Per-item verification rate for GPT-4O-MINI-generated topic tags [Q34]

**Requires expert verification:**
- Bangladeshi environmental scientist re-annotation of any cross-border water or Bangladesh-specific agricultural items, were such items added
- Identification by a Bangladeshi policy expert of specific MILU items where Indian exam answers would be considered nationally partial vs. universally authoritative

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
MILU evaluates via accuracy on MCQ tasks using log-likelihood scoring for non-API models [Q48–Q51] and structured-JSON generative scoring for API models [Q53]. Both deployment and benchmark are text-based, satisfying the basic modality match. The MCQ output format does not require speech, vision, or other modalities that would create infrastructural barriers in Mymensingh (high text-only connectivity [WEB-20]). Two limitations reduce the score: (a) the authors acknowledge log-likelihood may yield different results than generation-based or CoT methods [Q85], which matters for the deployment's reasoning-heavy queries; and (b) MCQ output cannot capture the multi-step open-ended agricultural reasoning the deployment scenario requires (CRITICAL Concern 3, MAJOR Concern 7). For a LOWER-priority dimension where text modality is the main requirement, MILU is functionally adequate but suppresses richer output forms relevant to professional knowledge work.

**Strengths:**
- Text-based output modality is fully aligned with the deployment's text-only LLM access pattern [Q48, Q53]
- Reproducible evaluation via LM-EVALUATION-HARNESS [Q48] and structured JSON parsing for API models [Q53] enables consistent benchmarking across the frontier and regional Indic LLMs the user deploys
- 0/1/5-shot evaluation across base and instruct variants [Q45, Q46] provides multiple data points on model behavior, including the documented warning that instruct models may degrade with few-shot examples [Q62, Q63] — useful diagnostic signal for the deployment
- Consistent MCQ structure supports cross-language and cross-model comparability (DATASET Strength 4)

**Checklist:**

- **OF-1**: Output modality (text MCQ answer-key selection) matches the deployment's text-based LLM access [Q48, Q53]. Modality match is good; format-richness match is partial — deployment expects open-ended reasoning, MCQ provides only label selection. — _Sources: Q48, Q53_
- **OF-2**: Text-to-speech is not required by the deployment (text-based access only per YAML llm_access_modality). Not applicable.
- **OF-3**: Target population is professional environmental scientists; literacy and accessibility are not constraints. Bangladesh national connectivity supports text modality [WEB-20, WEB-21]. Mymensingh hosts BAU, suggesting above-average professional digital infrastructure [WEB-7]. — _Sources: WEB-20, WEB-21, WEB-7_
- **OF-4**: Form mismatch is mild: log-likelihood vs. generative evaluation differences acknowledged by authors [Q85] mean MILU scores may not predict generation-mode deployment performance. MCQ format suppresses open-ended agricultural reasoning the deployment requires (MAJOR Concern 7). External validity for generation-mode deployment is partial. — _Sources: Q85_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q48] 'For non-API-based models, we use the LM-EVALUATION-HARNESS (Gao et al., 2024; Biderman et al., 2024) to ensure clean and reproducible evaluations.' (p.5)
- [Q49] 'We use the log-likelihood method, where the probability of a given output string is computed by conditioning it on some provided input' (p.5)
- [Q53] 'We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing.' (p.5)
- [Q62] 'Instruct models exhibit more varied behavior, where models either stagnate or even degrade in performance.' (p.6)
- [Q85] 'our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting.' (p.9)

*Web sources:*
- [WEB-20] Bangladesh internet/mobile coverage adequate for text modality
- [WEB-7] BAU as professional institutional context — text infrastructure supported

*Dataset analysis:*
- DATASET Strength 4: Consistent 4-option MCQ structure across all 215 sampled examples enables reproducible cross-language evaluation

</details>

**Information gaps:**
- Whether deployment workflow requires explicit chain-of-thought or generation-mode evaluation that would diverge from MILU's log-likelihood scoring [Q85]

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Zero Bangladeshi datapoints; Bengali corpus is West Bengal-derived; sampled Bengali validation is 100% machine-translated

**Recommendation:** Source new Bengali items from Bangladeshi institutional question banks (BAU, BARI, BRRI, BWDB) authored in Bangladeshi register; integrate BEnQA [WEB-6] as a complementary Bangladeshi Bengali baseline; explicitly flag and quarantine machine-translated items in any deployment screening report.

### Input Ontology ⚠

**Gap:** 41-subject taxonomy lacks Bangladesh-specific agro-ecological subdomains (haor wetland ecology, char-land agriculture, boro/aman rice systems, trans-border hydrology)

**Recommendation:** Collaborate with BAU Mymensingh and BARI/BRRI to define a Bangladesh-extended subject taxonomy with named subdomains for floodplain ecology, wetland farming, and cross-border river systems; construct an extension benchmark covering those subdomains.

### Output Content ⚠

**Gap:** No Bangladeshi annotators; no inter-annotator agreement metrics; ~55% of topic tags assigned by GPT-4O-MINI without per-item human verification

**Recommendation:** Recruit a Bangladeshi annotator panel including BAU agronomists and an environmental-policy expert to re-annotate any items relevant to Bangladesh, trans-border water, or wetland systems; report inter-annotator agreement at minimum for the Bangladesh-relevant subset.

### Input Form

**Gap:** Exam-register MCQ phrasing diverges from naturalistic professional-query register; some translated items have truncated stems

**Recommendation:** Augment evaluation with naturalistic-register Bangladeshi Bengali agricultural query items elicited from BAU/BARI scientists; filter out items with incomplete stems (DATASET-D34, D35, D36) before reporting scores.

### Output Form

**Gap:** Log-likelihood MCQ scoring suppresses open-ended agricultural reasoning relevant to the deployment use case [Q85]

**Recommendation:** Add a generation-mode evaluation track with rubric-based scoring for a sub-sample of agriculturally relevant items, and include CoT prompts to align with the deployment's reasoning-heavy query workload.

### Output Ontology

**Gap:** Single-correct-answer MCQ structure cannot encode legitimate Indian–Bangladeshi pluralism on contested trans-border policy questions

**Recommendation:** For policy and trans-border items, adopt a multi-reference scoring schema where both Indian and Bangladeshi authoritative answers are accepted, or construct a separate pluralistic-ground-truth track using Bangladesh policy documents and the GBM bilateral context [WEB-11, WEB-14].

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge." |
| Q2 | 1 | input_content | "With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science." |
| Q3 | 1 | output_form | "We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q4 | 1 | output_form | "Open multilingual models outperform language-specific fine-tuned models, which perform only slightly better than random baselines." |
| Q5 | 1 | output_content | "Models also perform better in high-resource languages as compared to low-resource ones." |
| Q6 | 1 | input_ontology | "Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM." |
| Q7 | 1 | input_ontology | "To the best of our knowledge, MILU is the first of its kind benchmark focused on Indic languages, serving as a crucial step towards comprehensive cultural evaluation." |
| Q8 | 1 | output_content | "Sshubam Verma1 Mohammed Safi Ur Rahman Khan1,2 Vishwajeet Kumar3 Rudra Murthy3 Jaydeep Sen3 1Nilekani Centre at AI4Bharat 2Indian Institute of Technology, Madras 3IBM Research, India" |
| Q9 | 2 | input_content | "We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams." |
| Q10 | 2 | output_ontology | "These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science." |
| Q11 | 2 | input_content | "We create this benchmark by collecting questions from over 1500 competitive exams from India." |
| Q12 | 2 | input_content | "We focus on region-specific exams to authentically capture local knowledge in the respective language." |
| Q13 | 2 | output_form | "We evaluate 45 different LLMs - a mix of closed proprietary, open-source, and language-specific models- on MILU." |
| Q14 | 2 | output_form | "Our findings suggest that models struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q15 | 2 | output_form | "Our analysis of in-context learning reveals that adding more examples improves performance in base models, but the effect on instruct models remains inconclusive." |
| Q16 | 2 | output_ontology | "Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM." |
| Q17 | 3 | input_ontology | "MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge." |
| Q18 | 3 | input_ontology | "This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others." |
| Q19 | 3 | input_ontology | "MILU is designed as a culturally relevant benchmark to assess general problem-solving abilities and India-specific knowledge." |
| Q20 | 3 | input_content | "These questions were sourced following an approach similar to AGIEVAL (Zhong et al., 2023), collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams, among others." |
| Q21 | 3 | input_content | "We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages." |
| Q22 | 3 | output_content | "These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers." |
| Q23 | 3 | input_content | "Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years." |
| Q24 | 3 | input_content | "Regional state exams are particularly valuable as they cover various state-level topics and emphasize the official language of each state." |
| Q25 | 3 | input_content | "In total, we collected more than 150K questions across 11 Indian Languages- Bengali (bn), Gujarati (gu), Hindi (hi), Kannada (kn), Malayalam (ml), Marathi (mr), Odia (or), Punjabi (pn), Tamil (ta), Telugu (te), and English (en)-spanning 41 diverse subjects." |
| Q26 | 3 | input_content | "English questions are also included as these often address Indian culture-specific content, which is notably missing from existing popular benchmarks." |
| Q27 | 4 | input_form | "Despite our best efforts to maintain the quality of questions collected, some amount of noise or errors may still be present. To address potential noise in the questions, we employ multiple layers of manual and automated cleaning filters." |
| Q28 | 4 | input_form | "Initially, we manually review a large sample of questions to detect and eliminate potential sources of noise." |
| Q29 | 4 | input_form | "During the collection process, we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency." |
| Q30 | 4 | input_form | "To remove incorrect language entries, we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering (Khan et al., 2024), ensuring that the questions are in the correct language." |
| Q31 | 4 | input_form | "To further refine the dataset, we remove any duplicate questions to retain only the unique ones." |
| Q32 | 4 | input_form | "As a final step, we manually verify a sample of questions from each language to ensure accuracy and correct any remaining errors." |
| Q33 | 4 | output_ontology | "Upon examination, we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information." |
| Q34 | 4 | input_form | "To address this issue, we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question." |
| Q35 | 4 | output_ontology | "Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap." |
| Q36 | 4 | output_ontology | "To organize them, we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters." |
| Q37 | 4 | output_content | "We manually review these clusters and assign appropriate subject labels." |
| Q38 | 4 | output_ontology | "Following the manual merging of related clusters, we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies." |
| Q39 | 4 | input_form | "Finally, we observed that some topics in certain languages had less than 100 questions. To ensure thorough evaluation across all subjects and languages, we aimed to have at least 100 questions per subject in each language." |
| Q40 | 4 | input_form | "For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O." |
| Q41 | 4 | input_form | "We chose GPT-4O over specialized translation models for their ability to remain task-aware during translation (Ahuja et al., 2024), ensuring the translated content aligns with the intent of the question." |
| Q42 | 4 | input_content | "In total, we release around 79K questions across 41 subjects across 8 domains in 11 languages, capping each subject-language pair at 500 questions for feasible evaluations." |
| Q43 | 4 | input_content | "Table 2 shows the overall statistics of MILU. Of the total 79K questions, only 25% of questions are translated from English, with the remainder" |
| Q44 | 5 | output_form | "We evaluate 42 different models on MILU, including large proprietary models, open-source multilingual models, and popular fine-tuned models specific to Indic languages." |
| Q45 | 5 | output_form | "Both the base versions and instruction fine-tuned variants of these models, wherever applicable, are evaluated to measure the improvements gained from fine-tuning." |
| Q46 | 5 | output_form | "All models, except for proprietary models and LLAMA-3.1-405B, are tested under 0-shot, 1-shot, and 5-shot setups." |
| Q47 | 5 | input_content | "We maintain a separate validation set of approximately 9,000 questions to serve as examples for few-shot evaluations." |
| Q48 | 5 | output_form | "For non-API-based models, we use the LM-EVALUATION-HARNESS (Gao et al., 2024; Biderman et al., 2024) to ensure clean and reproducible evaluations." |
| Q49 | 5 | output_form | "We use the log-likelihood method, where the probability of a given output string is computed by conditioning it on some provided input (Brown et al., 2020)." |
| Q50 | 5 | output_form | "Specifically, the log-likelihood of an answer (a) given the question (x), i.e., logP(a\|x), is calculated by concatenating the answer (a) with question (x), and then summing up the log probabilities, of each target token." |
| Q51 | 5 | output_form | "For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability, i.e., argmax(logP(a1\|x), ..., logP(ak\|x))." |
| Q52 | 5 | output_form | "The API-based models are evaluated using the generative approach due to the lack of support for prompt log probabilities." |
| Q53 | 5 | output_form | "We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing." |
| Q54 | 5 | output_form | "Due to the high costs involved, these models are evaluated only in the zero-shot setup." |
| Q55 | 6 | output_form | "We report 5-shot accuracies for all open models (except for LLAMA-3.1-70B-INSTRUCT & LLAMA-3.1-405B for which we report 0-shot accuracy) with the accuracy averaged across all the domains per language." |
| Q56 | 6 | input_content | "We evaluate around 16 Indic language LLMs on MILU." |
| Q57 | 6 | input_ontology | "These models are primarily built by adapting English LLMs, such as LLAMA-2-7B, by first continually pretraining on small amount Indic language data, followed by optionally instruction finetuning them." |
| Q58 | 6 | output_form | "As seen from Table 4, across languages, the models exhibit average performance comparable to random baselines, with minimal variations among them." |
| Q59 | 6 | output_ontology | "When analyzed across domains, the models generally perform worse in Arts, Humanities, and Social Sciences than in STEM subjects." |
| Q60 | 6 | output_form | "We compare the performance of different Base and Instruct models across zero, one, and five-shot setups." |
| Q61 | 6 | output_form | "As shown in Figure 3, the performance of base models consistently improves with an increasing number of in-context examples, with the 5-shot setup yielding the best results." |
| Q62 | 6 | output_form | "In contrast, Instruct models exhibit more varied behavior, where models either stagnate or even degrade in performance." |
| Q63 | 6 | output_form | "This also aligns with expectations, as Instruct models are specifically fine-tuned as conversation assistants and may not respond well to the few-shot in-context examples format." |
| Q64 | 7 | output_form | "We evaluate the LLAMA and GEMMA family of models, ranging from 1B to 405B parameters, to analyze how performance scales with model size." |
| Q65 | 7 | output_form | "Figure 5 shows that the model performance improves significantly with increasing scale." |
| Q66 | 7 | output_form | "Notably, instruction-tuned models in the LLAMA family show more substantial improvements as compared to those in the GEMMA family." |
| Q67 | 7 | output_form | "We analyze the performance of various base and instruct models across multiple domains and languages." |
| Q68 | 7 | output_ontology | "Similar trends to those in Section (§5.2) are observed where the open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields." |
| Q69 | 7 | output_content | "This suggests that the training corpora for these models lack sufficient culturally specific data." |
| Q70 | 7 | output_content | "Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages." |
| Q71 | 7 | output_form | "As most Indic LLMs are built on English base models like LLAMA-2-7B, we assess the impact of language adaptation on their performance." |
| Q72 | 7 | output_form | "Table 5 compares language-specific models with the original LLAMA-2-7B, and instruction-tuned models with LLAMA-2-7B-CHAT." |
| Q73 | 7 | output_form | "Our findings show minimal gains, with some models even underperforming post-adaptation." |
| Q74 | 8 | input_ontology | "In this paper, we introduced MILU—Multilingual Indic Language Understanding Benchmark-a comprehensive benchmark specifically designed to evaluate LLMs across 11 Indic languages, spanning diverse domains and culturally relevant subjects." |
| Q75 | 8 | output_form | "We evaluate 45 different LLMs and find that the majority of LLMs struggle on MILU, with GPT4o achieving the highest average accuracy." |
| Q76 | 8 | input_form | "The analysis also shows that models perform significantly better in high-resource languages than low-resource ones, highlighting the need for more robust multilingual strategies." |
| Q77 | 8 | output_ontology | "Additionally, the domain-specific analysis indicates that models perform better in general fields such as STEM while facing challenges in culturally relevant subjects like Arts, Humanities, and Law, highlighting the lack of this knowledge in the current models and datasets." |
| Q78 | 8 | output_form | "We conjecture that limited performance gains may result from small language-specific datasets and reliance on parameter-efficient methods like LoRA (Hu et al., 2022)." |
| Q79 | 8 | output_content | "Another contributing factor could be the lack of diversity in instruction fine-tuning datasets." |
| Q80 | 8 | output_content | "Models like AIRAVATA, which utilize more diverse data (Gala et al., 2024), exhibit noticeably better performance." |
| Q81 | 8 | output_form | "Further investigation is required to fully understand the limitations and opportunities in this area." |
| Q82 | 9 | input_ontology | "First, we restricted our study to the top 11 languages due to the lack of readily available questions in low-resource languages, which we aim to address in future work." |
| Q83 | 9 | output_form | "Second, limited computational resources prevented a thorough evaluation of larger models, such as LLAMA-3.1-70B-INSTRUCT and LLAMA-3.1-405B." |
| Q84 | 9 | input_form | "Third, the scarcity of questions necessitated translating a portion of the dataset." |
| Q85 | 9 | output_form | "Finally, our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting." |
| Q86 | 9 | output_content | "We would like to thank EkStep Foundation and Nilekani Philanthropies for their generous grant towards building datasets, models, tools and other resources for Indian languages." |
| Q87 | 9 | output_content | "We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits." |
| Q88 | 9 | input_content | "All data described in this work was scraped from publicly available resources." |
| Q89 | 9 | input_content | "The datasets used in this paper will be made available under permissible licenses." |
| Q90 | 9 | output_form | "Additionally, the code used for our evaluations will be made publicly available under the MIT License." |
| Q91 | 9 | output_content | "We only used ChatGPT for assistance purely with the language of the paper, e.g., paraphrasing, spell-checking, or polishing the author's original content, without suggesting new content." |
| Q92 | 10 | input_content | "Sumanth Doddapaneni, Rahul Aralikatte, Gowtham Ramesh, Shreya Goyal, Mitesh M. Khapra, Anoop Kunchukuttan, and Pratyush Kumar. 2023. Towards leaving no Indic language behind: Building monolingual corpora, benchmark and models for Indic languages. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 12402–12426, Toronto, Canada. Association for Computational Linguistics." |
| Q93 | 17 | input_content | "We collected our questions from over 40 exam types ranging from various National and state level civil service examinations to examinations conducted by various government and private organizations." |
| Q94 | 17 | input_form | "Detailed analysis of topic and language distribution across languages can be found in Table 9 and Figure 6" |
| Q95 | 17 | output_form | "Model details about the different models evaluated in this work is present in Table 10." |
| Q96 | 18 | input_content | "Table 6: Overview of various national-level exams and the corresponding years of coverage considered in MILU." |
| Q97 | 18 | input_content | "Table 7: Overview of various government and private organization exams and the corresponding years of coverage considered in MILU." |
| Q98 | 18 | input_content | "Table 8: Overview of various State-level civil services exams and the corresponding years of coverage considered in MILU." |
| Q99 | 20 | input_ontology | "Table 9: Detailed subject level statistics of MILU across different languages." |
| Q100 | 22 | output_form | "Table 11: Detailed subject-wise evaluation for ABHINAND/TAMIL-LLAMA-7B-INSTRUCT-V0.2 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q101 | 23 | output_form | "Table 12: Detailed subject-wise evaluation for AI4BHARAT/AIRAVATA on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q102 | 24 | output_form | "Table 13: Detailed subject-wise evaluation for BHABHAAI/GAJENDRA-V0.1 on MILU across different languages." |
| Q103 | 24 | output_form | "The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q104 | 25 | output_form | "Table 14: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-BASE-V0.1 on MILU across different languages." |
| Q105 | 26 | output_form | "Table 15: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q106 | 27 | output_form | "Table 16: Detailed subject-wise evaluation for GENVRADMIN/ARYABHATTA-GEMMAGENZ-VIKAS-MERGED on MILU across different languages." |
| Q107 | 28 | output_form | "Table 17: Detailed subject-wise evaluation for MANISHIITG/OPEN-ADITI-V6-LLAMA3 on MILU across different languages." |
| Q108 | 29 | output_form | "Table 18: Detailed subject-wise evaluation for NICKMALHOTRA/PROJECTINDUS on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q109 | 30 | output_form | "Table 19: Detailed subject-wise evaluation for SARVAMAI/OPENHATHI-7B-HI-V0.1-BASE on MILU across different languages." |
| Q110 | 31 | output_form | "Table 20: Detailed subject-wise evaluation for TENSOIC/KAN-LLAMA-7B-BASE on MILU across different languages." |
| Q111 | 32 | output_form | "Table 21: Detailed subject-wise evaluation for ABHINAND/MALAYALAM-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q112 | 33 | output_form | "Table 22: Detailed subject-wise evaluation for ABHINAND/TELUGU-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q113 | 34 | output_form | "Table 23: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-INSTRUCT-V0.1 on MILU across different languages." |
| Q114 | 35 | output_form | "Table 24: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-BASE-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q115 | 36 | output_form | "Table 25: Detailed subject-wise evaluation for TELUGU-LLM-LABS/TELUGU-LLAMA2-7B-V0-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q116 | 37 | output_form | "Table 26: Detailed subject-wise evaluation for GPT-4o on MILU across different languages. The results reported are for 0-shot experiments." |
| Q117 | 38 | output_form | "Table 27: Detailed subject-wise evaluation for GPT-4O-MINI on MILU across different languages. The results reported are for 0-shot experiments." |
| Q118 | 39 | output_form | "Table 28: Detailed subject-wise evaluation for GEMINI-1.5-PRO on MILU across different languages. The results reported are for 0-shot experiments." |
| Q119 | 40 | output_form | "Table 29: Detailed subject-wise evaluation for GEMINI-1.5-FLASH on MILU across different languages. The results reported are for 0-shot experiments." |
| Q120 | 41 | output_form | "The results reported are for 0-shot experiments." |
| Q121 | 42 | output_form | "Table 31: Detailed subject-wise evaluation for SARVAMAI/SARVAM-1 on MILU across different languages. The results reported are for 5-shot experiments." |
| Q122 | 44 | output_form | "Table 34: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B on MILU across different languages." |
| Q123 | 44 | output_form | "Table 35: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B-IT on MILU across different languages." |
| Q124 | 47 | output_form | "Table 39: Detailed subject-wise evaluation for NVIDIA/NEMOTRON-4-MINI-HINDI-4B-BASE on MILU across different languages. The results reported are for 5-shot experiments." |
| Q125 | 48 | output_form | "Table 40: Detailed subject-wise evaluation for META-LLAMA/LLAMA-2-7B-HF on MILU across different languages." |
| Q126 | 48 | output_form | "Table 41: Detailed subject-wise evaluation for META-LLAMA/LLAMA-2-7B-CHAT-HF on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q127 | 49 | output_form | "Table 42: Detailed subject-wise evaluation for NEULAB/PANGEA-7B on MILU across different languages. The results reported are for 5-shot experiments." |
| Q128 | 52 | input_ontology | "Table 47: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-9B-IT on MILU across different languages." |
| Q129 | 52 | output_form | "Table 48: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-27B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q130 | 55 | output_form | "Table 52: 0-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q131 | 56 | output_form | "1-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q132 | 57 | output_form | "Table 54: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.1-405B on MILU across different languages. The results reported are for 0-shot experiments." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://pjtsau.edu.in/crop.html |
| WEB-2 | https://telanganaslbc.com/StateProfile.aspx |
| WEB-3 | https://caa.gov.in/ |
| WEB-4 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2078575 |
| WEB-5 | https://mpeda.gov.in/?page_id=651 |
| WEB-6 | https://arxiv.org/abs/2403.10900 |
| WEB-7 | https://bau.edu.bd/ |
| WEB-8 | https://en.wikipedia.org/wiki/Bangladesh_Agricultural_University |
| WEB-9 | https://en.banglapedia.org/index.php/Bangladesh_Agricultural_University |
| WEB-10 | https://lotusarise.com/agro-ecological-regions-of-india-upsc/ |
| WEB-11 | https://thediplomat.com/2026/04/why-the-india-bangladesh-ganges-treaty-renewal-must-deliver-real-security/ |
| WEB-12 | https://www.thegeostrata.com/post/the-ganga-countdown-time-is-running-out-and-so-is-the-water |
| WEB-13 | https://www.gktoday.in/india-bangladesh-ganga-water-sharing-treaty-renewal-talks-begin/ |
| WEB-14 | https://en.wikipedia.org/wiki/Teesta_Water_Dispute |
| WEB-15 | https://www.waterdiplomat.org/story/2025/08/teesta-river-politics-and-benefit-sharing-getting-yes-without-grand-bargain |
| WEB-16 | https://www.tbsnews.net/features/panorama/teesta-master-plan-and-longstanding-bangladesh-india-water-politics-1072696 |
| WEB-17 | https://github.com/AI4Bharat/MILU |
| WEB-18 | https://aclanthology.org/2025.naacl-long.507/ |
| WEB-19 | https://mowr.nic.in/core/WebsiteUpload/2023/2023011877.pdf |
| WEB-20 | https://datareportal.com/reports/digital-2024-bangladesh |
| WEB-21 | https://en.wikipedia.org/wiki/Internet_in_Bangladesh |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (configs: Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu)
**Analysis date:** 2025-01-31
**Examples reviewed:** 215 total (Bengali: 21, English: 20, Gujarati: 24, Hindi: 26, Kannada: 17, Malayalam: 16, Marathi: 21, Odia: 21, Punjabi: 25, Tamil: 19, Telugu: 25) — all from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Bengali | Ex.7 | option4 | "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... জাতীয় খাদ্য সুরক্ষা মিশন মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" | National Food Security Mission: crop development scheme, soil health restoration — Indian scheme, no Bangladesh context | IO, IC |
| D2 | Bengali | Ex.1 | option3 | "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল?" | India's 1991 foreign reserve crisis — Indian economic history, irrelevant to Bangladesh agricultural deployment | IC |
| D3 | Bengali | Ex.1 | option3 | **is_translated:** True | All 21 Bengali validation examples are machine-translated from English | IF |
| D4 | Bengali | Ex.5 | option4 | "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP)... পাঞ্জাব" | Indian state assembly election — Indian polity, no Bangladesh relevance | IC |
| D5 | Bengali | Ex.9 | option3 | "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে... প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" | Removal of Indian Election Commissioner — Indian constitutional law only | OC |
| D6 | English | Ex.5 | option1 | "A geographic region has the following distinct characteristics: 1. Warm and dry climate 2. Mild and wet winter 3. Evergreen oak trees" | Mediterranean climate region identification — generic geography | IO |
| D7 | English | Ex.10 | option4 | "Which of the following are claimed as advantageous in respect of aerobic sludge digestion as compared to anaerobic sludge digestion?" | Wastewater engineering/environmental science — technically relevant but not agro-ecological | IO |
| D8 | English | Ex.9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" | Maharashtra state governance — India-specific law, not relevant to Bangladesh | IC, OC |
| D9 | English | Ex.13 | option4 | "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? ... Telangana" | Telangana state welfare policy — classified under Geography, reflects generic Indian current affairs | IC, OO |
| D10 | Bengali | Ex.7 | option4 | domain: Environmental Sciences, subject: Agriculture | Agriculture-labeled question about India's National Food Security Mission — only MILU "Agriculture" example in Bengali sample | IO, IC |
| D11 | Kannada | Ex.7 | option4 | "ರಾಷ್ಟ್ರೀಯ ಆಹಾರ ಭದ್ರತಾ ಮಿಷನ್ ಒಂದು ಬೆಳೆ ಅಭಿವೃದ್ಧಿ ಯೋಜನೆ... ಮಣ್ಣಿನ ಆರೋಗ್ಯವನ್ನು ಪುನಃಸ್ಥಾಪಿಸಲು" | National Food Security Mission crop scheme in Kannada — same Indian policy content replicated across languages | IC, IO |
| D12 | Marathi | Ex.7 | option4 | "राष्ट्रीय अन्न सुरक्षा मिशन हे एक पीक विकास योजना आहे... मातीचे आरोग्य पुनर्संचयित करणे" | National Food Security Mission in Marathi — same question across languages confirms India-only policy content | IC |
| D13 | Marathi | Ex.21 | option3 | "राष्ट्रीय मोहरी संशोधन केंद्र कुठे स्थित आहे... सेवर" | Location of National Mustard Research Centre in India — India-specific agricultural institution | IC, IO |
| D14 | Odia | Ex.21 | option4 | "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" | Which Indian company produces agricultural equipment rapidly (Kirloskar) — India-specific corporate knowledge | IC, IO |
| D15 | Punjabi | Ex.7 | option4 | "ਰਾਸ਼ਟਰੀ ਖਾਦ ਸੁਰੱਖਿਆ ਮਿਸ਼ਨ ਇੱਕ ਫਸਲ ਵਿਕਾਸ ਯੋਜਨਾ ਹੈ... ਮਿੱਟੀ ਦੀ ਸਿਹਤ ਨੂੰ ਬਹਾਲ ਕਰਨਾ" | National Food Security Mission in Punjabi — same cross-language India-scoped agriculture question | IC |
| D16 | Telugu | Ex.25 | option1 | "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది?... మొరెనా" | Location of Banmore Industrial Development Centre in Madhya Pradesh — Indian geography | IC |
| D17 | Telugu | Ex.9 | option2 | "క్రింది వాటిలో మహారాష్ట్ర శాసనసభ కమిటీ వ్యవస్థ గురించి ఏ ప్రకటన సరైనది కాదు?" | Maharashtra Legislative Committee system in Telugu — state-specific Indian governance | IC, OC |
| D18 | English | Ex.5 | option1 | domain: Environmental Sciences, subject: Geography | Mediterranean climate question under Environmental Sciences — geographic reasoning, not agro-ecological depth | IO |
| D19 | Bengali | Ex.3 | option4 | "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল?... গুলবার্গা" | First capital of Bahmani Kingdom — medieval Indian history, no agriculture/environment relevance | IC |
| D20 | Bengali | Ex.12 | option4 | "'মঙ্গল ভারত' কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল" | "Mangal Bharat" literary work by Vinoba Bhave — Indian literary/national leader trivia | IC |
| D21 | Odia | Ex.2 | option4 | "ଡିସେମ୍ବର 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆକୁ ପ୍ରଥମେ ଜଣା ଦେଇଥିବା ଦେଶ କେଉଁଟି?... ଆଫଗାନିସ୍ତାନ; option2: ବାଙ୍ଗ୍ଲାଦେଶ" | Which country first reported Indian Pharmacopoeia (Afghanistan) — Bangladesh appears as wrong answer option | IC, OC |
| D22 | Hindi | Ex.10 | option4 | "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है?... नाइट्रेट" | Blue Baby Syndrome caused by excess nitrate in blood — generic health/environmental science | IO |
| D23 | English | Ex.10 | option4 | "Lower BOD concentration in supernatant liquor... Production of a sludge with excellent dewatering propensity... aerobic sludge digestion" | Aerobic vs. anaerobic sludge digestion advantages — environmental engineering question | IO |
| D24 | Bengali | Ex.8 | option4 | "নিম্নলিখিত কোনগুলি অক্সিডেশন-রিডাকশন বিক্রিয়া?" | Oxidation-reduction reactions — basic chemistry | IO |
| D25 | Telugu | Ex.2 | option4 | "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది?... ఆఫ్ఘనిస్తాన్; option2: బంగ్లాదేశ్" | Same Indian Pharmacopoeia question in Telugu — Bangladesh again used only as distractor | IC, OC |
| D26 | Bengali | Ex.2 | option3 | "একটি ক্রিকেট প্রশিক্ষণ শিবিরে ১২০০ জন শিশু... নির্বাচিত না হওয়া শিশুদের সংখ্যা এবং মোট শিশুদের সংখ্যার অনুপাত" | Ratio problem about cricket training camp — numeracy/reasoning, irrelevant to agricultural science | IO |
| D27 | Gujarati | Ex.8 | option3 | "રેડક્લિફ રેખા નીચેના પૈકી કયા દેશ સાથે ભારતની સરહદોને અલગ કરે છે?... પાકિસ્તાન" | Radcliffe Line divides India from Pakistan — Indian partition geography | IC |
| D28 | Hindi | Ex.6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?... 44वें संविधान संशोधन अधिनियम द्वारा" | Indian constitutional amendment for 'armed rebellion' clause — Indian law and governance | IC, OC |
| D29 | Marathi | Ex.16 | option3 | "हलषष्ठी सण का साजरा केला जातो?... मुलाच्या दीर्घायुष्यासाठी" | Halashashthi festival purpose (for son's longevity) — Indian/Hindu cultural practice, Agriculture-labeled but not agricultural | IO |
| D30 | Punjabi | Ex.21 | option3 | "ਰਾਸ਼ਟਰੀ ਸਰੋਂ ਖੋਜ ਕੇਂਦਰ ਕਿੱਥੇ ਸਥਿਤ ਹੈ... ਸੇਵਰ" | Location of National Mustard Research Centre — Indian agricultural institution trivia | IC, IO |
| D31 | Bengali | Ex.4 | option2 | "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। ... শেল" (is_translated: True) | Shell-type constant current transformer — engineering question, machine-translated from English | IF |
| D32 | English | Ex.20 | option2 | "Flower colours of red, pink, blue and purple come mainly from pigments called... Anthocyanins" | Plant pigment biology question — generic botany | IO |
| D33 | Odia | Ex.17 | option1 | "T - Hub ଏକ ତେଲେଙ୍ଗାନା ରାଜ୍ୟ ସରକାରର ପ୍ରୟାସ... ଉଦ୍ୟମିତାକୁ ପ୍ରୋତ୍ସାହନ ଦେବାକୁ ଏକ ପ୍ରଯୁକ୍ତି ଉତ୍ପ୍ରେରଣ କେନ୍ଦ୍ର" | T-Hub Telangana state entrepreneurship tech incubator — Telangana-specific but non-agricultural | IC |
| D34 | Bengali | Ex.6 | option2 | "নিচের প্রশ্নে... সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে" (question body missing the target word) | Antonym question — incomplete stem, illustrates quality issues in translated questions | IF |
| D35 | Bengali | Ex.19 | option1 | "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে" (arguments not shown in question field) | Argument evaluation question — missing argument content, shows data quality gap in translated items | IF |
| D36 | English | Ex.11 | option2 | "The owner of the textile shop brought a... Calculator" | Incomplete question stem — no meaningful question context present | IF |
| D37 | Hindi | Ex.13 | option1 | "'মানসून' শব্দের উৎপত্তি কোন ভাষা থেকে?... আরবি ভাষা" (Hindi): "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है?... अरबी भाषा" | Origin of word 'monsoon' from Arabic — climate vocabulary trivia, tangentially relevant to agricultural climate | IO |
| D38 | Marathi | Ex.13 | option2 | "प्रांतांमध्ये द्वैधशासन प्रणाली कोणत्या कायद्याने स्थापन केली?... भारत सरकार अधिनियम 1919" | Government of India Act 1919 establishing dyarchy — Indian colonial law | IC, OC |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-script Indic language coverage including Bengali
- **Dimension(s):** IF
- **Observation:** The benchmark successfully delivers text-based MCQ content in Bengali script across all 21 sampled Bengali validation examples, as well as Telugu (25 examples), Hindi, and 8 other Indic scripts. The deployment's primary modality — text-based Indic script queries — is technically supported.
- **Deployment relevance:** The environmental scientist's queries in Bengali and Telugu scripts are at least modality-compatible with the benchmark format. Script-level compatibility ensures that model performance scores on MILU reflect at minimum the correct input encoding for the target scripts.
- **Datapoint citations:**
  - [D3] Bengali Ex.1 (Bengali, validation, option3): `is_translated: True` — Confirms Bengali script is fully populated across all sampled examples, though all are machine-translated.
  - [D31] Bengali Ex.4 (Bengali, validation, option2): "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। ... শেল" — Technical content in Bengali script, confirming script rendering is functional even for translated engineering content.

#### Strength 2: Environmental Sciences and Agriculture subject labels present in multiple languages
- **Dimension(s):** IO
- **Observation:** The "Agriculture" subject appears in the Environmental Sciences domain across at least Bengali (Ex.7), Kannada (Ex.7), Marathi (Ex.7, Ex.21), Punjabi (Ex.7, Ex.21), and Odia (Ex.21). A single Agriculture-labeled question also appears in Bengali. The Environmental Sciences domain contributes Geography, Earth Sciences, and Environmental Science sub-subjects as well.
- **Deployment relevance:** The presence of Agriculture-labeled questions across languages demonstrates that the subject taxonomy does include agricultural content, even if surface-level. For an initial screening of whether a model has any agricultural knowledge, these items provide at least minimal signal.
- **Datapoint citations:**
  - [D10] Bengali Ex.7 (Bengali, validation, option4, subject=Agriculture): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" — Only Bengali Agriculture question in sample; concerns soil health but in the context of an Indian national scheme.
  - [D13] Marathi Ex.21 (Marathi, validation, option3, subject=Agriculture): "राष्ट्रीय मोहरी संशोधन केंद्र कुठे स्थित आहे... सेवर" — Agriculture question about location of National Mustard Research Centre.
  - [D14] Odia Ex.21 (Odia, validation, option4, subject=Agriculture): "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" — Agricultural equipment manufacturer in India.

#### Strength 3: Broad domain coverage enabling baseline comparisons across general knowledge areas
- **Dimension(s):** IO, OF
- **Observation:** Across 215 sampled examples, MILU covers Engineering, Science (Physics, Chemistry, Biology, Computer Science, Logical Reasoning), Social Sciences, Arts & Humanities, Law & Governance, Health & Medicine, Business Studies, and Environmental Sciences. This allows a broad model capability baseline.
- **Deployment relevance:** For the scientist's use of both frontier LLMs (GPT-4o, Gemini) and regional small LLMs, MILU's breadth enables diagnosis of whether regional LLMs fail specifically in science/environment or broadly across all domains — a useful comparative signal even if the agricultural domain content is inadequate.
- **Datapoint citations:**
  - [D7] English Ex.10 (English, validation, option4, subject=Environmental Science): "Which of the following are claimed as advantageous in respect of aerobic sludge digestion as compared to anaerobic sludge digestion? (1) Lower BOD concentration in supernatant liquor..." — Technical environmental engineering question, at least adjacent to environmental science professional knowledge.
  - [D22] Hindi Ex.10 (Hindi, validation, option4, subject=Health and Medicine): "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है?... नाइट्रेट" — Nitrate-related health question, tangentially relevant to agro-environmental context (nitrate contamination in agricultural water).

#### Strength 4: Consistent MCQ structure enables cross-language and cross-model comparison
- **Dimension(s):** OF
- **Observation:** All sampled examples follow identical 4-option MCQ structure with `target` field, `is_translated` flag, and domain/subject labels. This structural consistency enables controlled comparison across 11 languages and across model families.
- **Deployment relevance:** If the goal includes benchmarking multiple LLMs (frontier + regional) across Bengali and Telugu, MILU's consistent format allows reproducible, comparable evaluation — a practical strength for the meta-analytic purpose of assessing whether regional Indic LLMs perform adequately on science content before deployment in the agricultural query context.
- **Datapoint citations:**
  - [D6] English Ex.5 (English, validation, option1, subject=Geography): "A geographic region has the following distinct characteristics: 1. Warm and dry climate 2. Mild and wet winter 3. Evergreen oak trees" — Illustrates clean MCQ structure with unambiguous single-correct answer.
  - [D11] Kannada Ex.7 (Kannada, validation, option4, subject=Agriculture): "ರಾಷ್ಟ್ರೀಯ ಆಹಾರ ಭದ್ರತಾ ಮಿಷನ್ ಒಂದು ಬೆಳೆ ಅಭಿವೃದ್ಧಿ ಯೋಜನೆ" — Same question appears in Bengali, Kannada, Marathi, Malayalam, Punjabi, confirming reliable cross-language structural alignment for identical underlying content.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete absence of Bangladesh-specific agricultural content
- **Dimension(s):** IO, IC
- **Observation:** Across all 215 sampled examples, zero questions address Bangladeshi agro-ecological systems. The Agriculture-labeled items that do appear concern Indian national schemes: the National Food Security Mission (NFSM) and the National Mustard Research Centre, and an Indian agricultural equipment company (Kirloskar). No question in the sample touches haor wetlands, beel fisheries, boro or aman rice cultivation, char-land farming, Brahmaputra-Jamuna floodplain management, or any Bangladeshi agricultural institution. This is consistent with the confirmed structural absence documented in the YAML and web search, and is directly observable in the data.
- **Deployment relevance:** The environmental scientist's primary knowledge domain — Bangladeshi delta agro-ecology — is entirely unrepresented. A model that scores well on MILU Agriculture questions has demonstrated knowledge of Indian food policy schemes, not Bangladeshi farming systems. The benchmark provides no discriminative power for the agricultural science retrieval use case as described.
- **Datapoint citations:**
  - [D10] Bengali Ex.7 (Bengali, validation, option4, domain=Environmental Sciences, subject=Agriculture): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" — The only Bengali Agriculture example in the validation sample concerns India's NFSM, not Bangladesh farming.
  - [D13] Marathi Ex.21 (Marathi, validation, option3, subject=Agriculture): "राष्ट्रीय मोहरी संशोधन केंद्र कुठे स्थित आहे... सेवर" — Agriculture question asking for location of Indian Mustard Research Centre in Rajasthan; no agronomic depth, no cross-border relevance.
  - [D14] Odia Ex.21 (Odia, validation, option4, subject=Agriculture): "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" — Agricultural equipment company trivia (Kirloskar); no agro-ecological science content.
  - [D15] Punjabi Ex.7 (Punjabi, validation, option4, subject=Agriculture): "ਰਾਸ਼ਟਰੀ ਖਾਦ ਸੁਰੱਖਿਆ ਮਿਸ਼ਨ ਇੱਕ ਫਸਲ ਵਿਕਾਸ ਯੋਜਨਾ ਹੈ... ਮਿੱਟੀ ਦੀ ਸਿਹਤ ਨੂੰ ਬਹਾਲ ਕਰਨਾ" — Same NFSM policy question replicated in Punjabi; Indian scheme only.

#### CRITICAL Concern 2: Bengali validation sample is 100% machine-translated; no original Bengali-authored questions visible
- **Dimension(s):** IF, IC
- **Observation:** Every one of the 21 Bengali validation examples has `is_translated: True`. This means the Bengali validation set in this sample consists entirely of questions translated from English (presumably Indian English exam content) via GPT-4O. This is consistent with the 25% overall translation rate documented in the paper, but the validation split sampled here shows complete translation saturation. The translated questions adopt standard Bengali script but carry formal translated register, not the naturalistic Bangladeshi Bengali or West Bengal exam register.
- **Deployment relevance:** Bangladeshi Bengali-register competence is a core requirement for the deployment. A benchmark where Bengali performance is assessed entirely on machine-translated questions conflates translation quality with language knowledge. For Mymensingh-dialect users, the register mismatch is compounded: the translation pipeline renders Indian English into what is likely to be a generic, somewhat stilted written Bengali, not the natural phrasing of a Bangladeshi agricultural scientist.
- **Datapoint citations:**
  - [D3] Bengali Ex.1 (Bengali, validation): `is_translated: True` — Confirmed for all 21 sampled Bengali validation examples; no `is_translated: False` observation in this split.
  - [D31] Bengali Ex.4 (Bengali, validation, option2): "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। ... শেল" — Engineering transformer question translated into Bengali; the phrasing is formally correct but exam-register, not naturalistic professional Bengali.
  - [D34] Bengali Ex.6 (Bengali, validation): "নিচের প্রশ্নে... সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে" — Antonym question with the target word missing from the question field entirely; the translated question is incomplete, suggesting translation pipeline quality issues.
  - [D35] Bengali Ex.19 (Bengali, validation): "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে" — Argument evaluation question where Arguments I and II are absent from the question field; answer cannot be verified from the question stem alone.

#### CRITICAL Concern 3: Environmental Sciences domain is surface-level general knowledge, not agro-ecological science
- **Dimension(s):** IO, IC
- **Observation:** The Environmental Sciences examples sampled across languages consistently classify geography questions (Mediterranean climate, Radcliffe Line, state populations) and generic earth science questions under this domain, not agro-ecological or soil science content. Agriculture-labeled questions (when they appear) concern Indian policy schemes or corporate trivia, not technical crop science. Across 215 examples, no question addresses: soil types and crop suitability, water management, wetland ecology, irrigation science, delta morphology, or climate change impacts on agriculture.
- **Deployment relevance:** The user explicitly confirmed that MILU's agricultural content is "surface-level." The data confirms this: the Environmental Sciences and Agriculture subject labels in MILU do not map to the technical depth required by a professional environmental scientist. MILU cannot assess whether a model can answer questions about floodplain hydrology, alluvial soil classification, or wetland rice agronomy — the core knowledge domains in the deployment context.
- **Datapoint citations:**
  - [D18] English Ex.5 (English, validation, option1, domain=Environmental Sciences, subject=Geography): "A geographic region has the following distinct characteristics: 1. Warm and dry climate 2. Mild and wet winter 3. Evergreen oak trees" — Mediterranean climate identification; classified as Environmental Sciences but has no agro-ecological depth.
  - [D6] English Ex.5 (same as D18) — Further confirms that "Environmental Sciences" domain encodes geography trivia, not environmental science.
  - [D29] Marathi Ex.16 (Marathi, validation, option3, domain=Arts & Humanities, subject=Arts and Culture): "हलषष्ठी सण का साजरा केला जातो?... मुलाच्या दीर्घायुष्यासाठी" — A festival question classified under Arts & Culture that in a different taxonomy could be agriculture-adjacent (harvest festivals), but demonstrates how culturally specific Indian content dominates even "Environmental Sciences"-adjacent categories.
  - [D9] English Ex.13 (English, validation, option4, domain=Environmental Sciences, subject=Geography): "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? ... Telangana" — Welfare policy question classified under Environmental Sciences/Geography; illustrates how the domain-subject taxonomy is applied loosely, and that "Telangana" appears in the sample only in a non-agricultural governance context.

---

#### MAJOR

#### MAJOR Concern 4: Indian-centric ground-truth labels for all governance, law, and policy questions; Bangladesh structurally excluded from answer keys
- **Dimension(s):** OC, OO
- **Observation:** Every governance and law question sampled encodes exclusively Indian constitutional, electoral, and policy knowledge as the ground truth. These include Indian Election Commissioner removal procedure (Bengali Ex.9), the 44th Constitutional Amendment (Hindi Ex.6, Malayalam Ex.6, Tamil Ex.6), Maharashtra state legislature committee rules (English Ex.9, Telugu Ex.9), and Indian state election results (Bengali Ex.5, Punjabi Ex.5). Bangladesh appears in two sampled examples solely as a wrong-answer distractor option (Odia Ex.2, Telugu Ex.2), never as the basis for a correct answer.
- **Deployment relevance:** While the user confirmed that Indian exam answer keys are "generally considered authoritative" for environmental science facts, the governance domain is categorically different. For trans-border agricultural policy questions (river-water allocation, bilateral treaty terms), Indian exam answers encode nationally partial perspectives. The current bilateral volatility (Ganges treaty nearing expiry December 2026, Teesta unresolved) makes this more acute. No such questions exist in the sampled data — confirming the structural absence documented in the YAML.
- **Datapoint citations:**
  - [D5] Bengali Ex.9 (Bengali, validation, option3, domain=Law & Governance, subject=Politics and Governance): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে... প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — Answer concerns Indian constitutional procedure; Bangladeshi constitutional norms are categorically different.
  - [D8] English Ex.9 (English, validation, option2, domain=Law & Governance): "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" — Maharashtra-specific state law; no cross-border relevance.
  - [D21] Odia Ex.2 (Odia, validation, option4, domain=Health & Medicine): "ଡିସେମ୍ବର 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆକୁ ପ୍ରଥମେ ଜଣା ଦେଇଥିବା ଦେଶ କେଉଁଟି?... ଆଫଗାନିସ୍ତାନ; option2: ବାଙ୍ଗ୍ଲାଦେଶ" — Bangladesh listed as a wrong answer; correct answer is Afghanistan. Illustrates Bangladesh's role in this benchmark: a distractor, not a knowledge frame.
  - [D25] Telugu Ex.2 (Telugu, validation, option4): "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది?... option2: బంగ్లాదేశ్" — Bangladesh again used as wrong-answer distractor across languages.

#### MAJOR Concern 5: Agriculture-labeled questions are policy trivia and institutional facts, not agronomic science
- **Dimension(s):** IO, OO
- **Observation:** Every Agriculture-subject question identified in the sample falls into one of three categories: (a) Indian government scheme facts (NFSM launch date, objectives), (b) Indian institutional locations (National Mustard Research Centre at Sever, Rajasthan), or (c) Indian corporate knowledge (Kirloskar as agricultural equipment manufacturer). None address agronomic principles, soil science, crop physiology, pest management, irrigation design, or ecosystem dynamics.
- **Deployment relevance:** An environmental scientist using LLMs to retrieve and reason over agricultural and environmental science knowledge requires models that can demonstrate technical depth — understanding soil types and water retention, rice growth stages and water requirements, integrated crop-fish system management. MILU Agriculture questions test Indian bureaucratic and corporate general-knowledge facts, not agronomic science. A model scoring well on these items provides no assurance about agricultural science competence.
- **Datapoint citations:**
  - [D1] Bengali Ex.7 (Bengali, validation, option4, subject=Agriculture): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" — Factual recall about Indian scheme objectives; no agronomy.
  - [D30] Punjabi Ex.21 (Punjabi, validation, option3, subject=Agriculture): "ਰਾਸ਼ਟਰੀ ਸਰੋਂ ਖੋਜ ਕੇਂਦਰ ਕਿੱਥੇ ਸਥਿਤ ਹੈ... ਸੇਵਰ" — Asks the location of India's mustard research centre; pure institutional geography.
  - [D14] Odia Ex.21 (Odia, validation, option4, subject=Agriculture): "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" — Corporate brand identification; not agricultural science.

#### MAJOR Concern 6: Telugu sample shows no Telangana/Andhra agro-ecological content; only general Indian exam material
- **Dimension(s):** IO, IC
- **Observation:** The 25 Telugu examples contain no questions about Telangana dry-land cropping, Andhra coastal aquaculture, or sub-regional agro-ecological specifics. Telangana appears once in the sampled data (English Ex.13 and Gujarati Ex.13) only in a social welfare policy context (pension for single women). The Telugu sample covers engineering, health, history, computer science, geography (generic), economics, and materials science — no regionally specific agricultural content is present.
- **Deployment relevance:** The deployment context explicitly targets Telangana dry-land cropping (cotton, sorghum, pigeonpea, red Deccan soils) and Andhra coastal aquaculture (L. vannamei shrimp farming, MPEDA/CAA regulatory framework) as cross-reference agro-ecological zones. MILU Telugu does not assess model knowledge of these sub-regional systems.
- **Datapoint citations:**
  - [D33] Odia Ex.17 (Odia, validation, option1, subject=Business and Management): "T - Hub ଏକ ତେଲେଙ୍ଗାନା ରାଜ୍ୟ ସରକାରର ପ୍ରୟାସ... ଉଦ୍ୟମିତାକୁ ପ୍ରୋତ୍ସାହନ ଦେବାକୁ ଏକ ପ୍ରଯୁକ୍ତି ଉତ୍ପ୍ରେରଣ କେନ୍ଦ୍ର" — T-Hub Telangana tech incubator; Telangana context appears only in tech entrepreneurship, not agriculture.
  - [D9] English Ex.13 (English, validation, option4, domain=Environmental Sciences): "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? ... Telangana" — Telangana surfaces as a welfare policy answer; no agricultural content.
  - [D16] Telugu Ex.25 (Telugu, validation, option1, domain=Environmental Sciences, subject=Geography): "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది?... మొరెనా" — Madhya Pradesh industrial centre location; Environmental Sciences domain again populated with geography trivia, not ecological content.

#### MAJOR Concern 7: MCQ format with single correct answer cannot accommodate cross-border knowledge pluralism on contested environmental/policy topics
- **Dimension(s):** OO, OF
- **Observation:** MILU enforces a single-correct-answer MCQ format with a definitive `target` field. The deployment includes scenarios — trans-border river management, water-sharing agreement terms, upstream dam impacts on Bangladeshi agriculture — where the "correct" answer is nationally contested and legitimately differs between Indian and Bangladeshi perspectives. No such questions exist in the current corpus, but the format structurally precludes them.
- **Deployment relevance:** Even if MILU were augmented with trans-border content, the MCQ format would force selection of a single answer key (likely Indian-exam-derived) for questions where Bangladeshi scientists hold different scientifically and politically valid positions. This is a structural output ontology constraint, not merely a coverage gap.
- **Datapoint citations:**
  - [D5] Bengali Ex.9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে... প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — Illustrates how Indian constitutional answers are encoded as the single correct response; a parallel Bengali question about Bangladesh's election commission removal would have a categorically different correct answer.
  - [D28] Hindi Ex.6 (Hindi, validation, option1, domain=Law & Governance): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?... 44वें संविधान संशोधन अधिनियम द्वारा" — Indian constitutional amendment as definitive answer; demonstrates how the MCQ single-correct format encodes nationally specific legal facts.

---

#### MINOR

#### MINOR Concern 8: Incomplete question stems visible in translated examples, indicating pipeline quality issues
- **Dimension(s):** IF
- **Observation:** At least two Bengali validation examples have incomplete or truncated question stems: Ex.6 asks for an antonym but the target word is absent; Ex.19 references "Arguments I and II" that are not present in the question field. English Ex.11 ("The owner of the textile shop brought a...") also presents an incomplete sentence with no meaningful context for answering. These truncation artifacts are present in the publicly released dataset.
- **Deployment relevance:** While these are minor quality issues that do not affect the dominant validity concerns, they indicate that the machine-translation and cleaning pipeline introduced some data quality degradation, particularly in Bengali. This slightly undermines confidence in translated Bengali content quality overall.
- **Datapoint citations:**
  - [D34] Bengali Ex.6 (Bengali, validation): "নিচের প্রশ্নে... সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে" — The antonym target word is absent from the question text.
  - [D35] Bengali Ex.19 (Bengali, validation): "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে" — Arguments I and II are referenced but not present in the question field.
  - [D36] English Ex.11 (English, validation, option2): "The owner of the textile shop brought a... Calculator" — Incomplete sentence with no meaningful question context.

#### MINOR Concern 9: Cross-language duplication of identical questions provides inflated coverage illusion
- **Dimension(s):** IO
- **Observation:** The same underlying questions appear across all 11 languages. The National Food Security Mission question (Ex.7 in Bengali, Kannada, Malayalam, Marathi, Punjabi), the cross-assembler definition (Ex.14 across Bengali, English, Kannada, Punjabi, Tamil, Telugu), the Bahmani Kingdom capital (Ex.3 across Bengali, English, Gujarati, Hindi, Malayalam, Punjabi, Tamil), and the Mediterranean climate question appear verbatim across most language configs. These represent translated duplicates of single source items, not independent language-specific questions.
- **Deployment relevance:** The apparent 79,000-question scale of MILU overstates content diversity; the underlying distinct-question count is substantially smaller, and for agricultural content specifically, the number of distinct agronomic questions is very low. A naive count of "Agriculture subject questions" across 11 languages would inflate the perceived agricultural coverage by a factor of up to 11×.
- **Datapoint citations:**
  - [D11] Kannada Ex.7 / [D12] Marathi Ex.7 / [D1] Bengali Ex.7 / [D15] Punjabi Ex.7 — All ask identical NFSM questions in different Indic scripts; same question content replicated across languages.
  - [D19] Bengali Ex.3 / [D27] (implicit in Gujarati, Hindi, Malayalam, Punjabi, Tamil samples) — Bahmani Kingdom capital question identical across multiple language configs.

---

### Content Coverage Summary

The 215 sampled examples span 11 Indic language configs and show a consistent pattern across all of them. Domain distribution in the sample favors Engineering & Technology (frequent), Arts & Humanities (history, language studies, arts/culture), and Business Studies (economics, finance), with Science (physics, chemistry, computer science, logical reasoning) and Social Sciences (sports, sociology) also well-represented. Environmental Sciences appears but is populated almost entirely with geography trivia (climate regions, political boundaries, state-level facts) rather than environmental or agro-ecological science.

The topical content is dominated by Indian competitive exam material: Indian constitutional law, Indian civil service facts, Indian national schemes and institutions, Indian history (medieval and colonial), Indian electoral politics, and Indian corporate/industrial knowledge. All Bengali examples in the validation split are machine-translated from English. South Asian content that appears to be cross-regional (e.g., geographic climate questions, basic physics/engineering) is generic and could have originated from any English-language exam.

Bangladesh appears in the sampled data exclusively as a wrong-answer distractor in two questions (Odia Ex.2, Telugu Ex.2) about Indian Pharmacopoeia recognition. No Bangladeshi agricultural institution, ecological system, land tenure concept, or trans-border water policy appears anywhere in the sample. Telangana and Andhra Pradesh appear only in non-agricultural contexts (tech incubator, welfare pension). The agricultural science vocabulary of the deployment context — haor, beel, boro, aman, char, Farakka, Teesta — has zero representation in the sampled content.

---

### Limitations

1. **Sample is from validation split only.** All 215 examples are drawn from the validation split (~9,000 total questions used for few-shot examples). The test split (~79,000 questions) may have different subject and domain distributions, including potentially more original (non-translated) Bengali questions and more Agriculture/Environmental Sciences content. The 100% translation rate observed in Bengali validation may not hold for the test split.

2. **Sample size per language is small (16–26 examples).** With 16–26 examples per language config, rare subjects (e.g., specific agro-ecological content, if any exists in the test split) would likely not appear in this sample even if present. The absence of Bangladesh-specific content and technical agricultural science in this sample is consistent with structural gaps documented in the YAML, but the sample cannot confirm the exact count of such questions in the full dataset.

3. **Subject distribution within Environmental Sciences is not fully observable.** Table 9 of the MILU paper contains per-subject per-language question counts but was not accessible in this analysis. The sampled data confirms surface-level coverage in Environmental Sciences, but the exact proportion of Agriculture, Environmental Science, Geography, and Earth Sciences sub-subjects in Bengali and Telugu test splits cannot be determined from this sample alone.

4. **Telugu agricultural sub-regional specificity requires corpus-level inspection.** Whether any Telugu test questions address Telangana dry-land cropping or Andhra coastal aquaculture cannot be confirmed or excluded from 25 validation examples. Direct inspection of the Telugu test split subject distribution would be needed.

5. **Machine translation register effects are not directly assessable from this data.** The extent to which GPT-4O translation introduces Indian Bengali register conventions (vs. generic translated register) cannot be assessed from reading translated MCQs alone, as the content of these questions is domain-neutral (engineering, computing, history). Register effects would be most visible in culturally-loaded or dialect-sensitive agricultural terminology, which is absent from the sample.

