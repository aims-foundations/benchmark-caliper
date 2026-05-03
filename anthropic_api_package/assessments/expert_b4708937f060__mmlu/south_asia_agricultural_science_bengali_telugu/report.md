## Deployment Context

**Use case:** Task: Environment science and geograpy-specific agricultural knowledge understanding
LLMs evaluated: Generic frontier model vs small llms as well as region specific llms
Domain: Environmental science
Setting: Environment science research utility assessment using llm and local-context
**Target population:** An environment scientist from Mymensingh, Bangladesh wants to get knowledge about different south asian region specific agricultural practice. So having different region and language specific agricultural and demographic context understanding (e.g. telegu spoken area, hydrabad India and agricultural practice/problems vs farmers practice/problems from Mymensingh, Bangladesh~bengali spoken in Mymensingh accented dialect.)

# Validity Analysis: mmlu
**Target context:** South Asian Agricultural and Environmental Science — Mymensingh–Telangana–Andhra Pradesh Deployment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ⚠ | 1 | Serious concern | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 2 | Significant gaps | medium |
| **Average** | **1.2** | | |

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

MMLU is fundamentally misaligned with the South Asian Agricultural and Environmental Science deployment across five of six dimensions. Five HIGH-priority dimensions (Input Ontology, Input Content, Input Form, Output Ontology, Output Content) score 1 — the lowest possible — with multiple structural validity violations: complete absence of agro-ecological subjects, US/Anglophone-saturated content, English-only input, MCQ schema unable to encode regional pluralism, and US-anchored ground-truth labels with no South Asian annotator validation. Output Form scores 2, partially supporting cross-model comparison via accuracy metrics. The single biggest concern is that the benchmark cannot, by construction, measure the constructs the user needs to evaluate — there is no item in MMLU's 14,079-question test set addressing haor wetland ecology, boro/aman/aus rice cultivation, char-land farming, Deccan dry-land cropping, or coastal aquaculture. Cross-border Bangladesh–India water-policy questions, which are actively contested in 2025, are entirely absent and could not be represented in the four-option MCQ format even if added. The benchmark is suitable only as a weak generic STEM-reasoning baseline for cross-model comparison.

## Practical Guidance

### What This Benchmark Measures

MMLU measures English-language MCQ accuracy on US/Western academic and professional knowledge across 57 subjects, with primary signal in mathematical reasoning, formal logic, and physical sciences (the dimensions where it scores least poorly for cultural neutrality). For this deployment, MMLU can provide a baseline cross-model accuracy comparison on culturally-neutral STEM and statistics items (per Strength 1 and Strength 3 in dataset analysis), and calibration diagnostics [Q60-62, Q106] useful for understanding model uncertainty behavior. It cannot measure South Asian agricultural or environmental science knowledge, nor any multilingual capability.

### Construct Depth

Construct depth for the deployment's intended construct (South Asian agricultural and environmental science knowledge) is essentially zero: Input Ontology contains no agro-ecological subjects, Input Content contains no regional sourcing, Input Form precludes regional languages, Output Ontology cannot encode regional divergence, and Output Content has no regional annotator validation. Where MMLU does probe deeply (US legal/medical/historical knowledge), the construct is irrelevant to the deployment. The only modest depth is in language-independent STEM reasoning, which provides shallow but stable signal for cross-model comparison.

### What Else You Need

Substantial supplementation is required across five dimensions: (1) Input Ontology — construct or adopt a South Asian agricultural knowledge taxonomy (BRRI/BARI/ICAR-aligned); (2) Input Content — recruit BAU, PJTSAU, ANGRAU agronomists to author items in Bengali, Telugu, and English covering haor/delta/dry-land/aquaculture systems; (3) Input Form — build multilingual evaluation infrastructure leveraging IndicTrans2 [WEB-18] and IndicBERT v2 [WEB-25] foundations, with explicit Bangladeshi-Bengali and Mymensingh-dialect coverage; (4) Output Ontology — design schema permitting regional-pluralism annotation for cross-border policy items; (5) Output Content — establish a regional annotator pool spanning Bangladesh and the Indian states, with explicit protocol for nationally-divergent answer keys (informed by current Ganges/Teesta context [WEB-1, WEB-2, WEB-4]). The synthetic agricultural QA methodology in arXiv 2507.16974 [WEB-26] provides a methodological precedent but covers only Hindi/Punjabi.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MMLU's 57-subject taxonomy is organized around US/Western academic disciplines [Q1, Q9, Q18] and contains no subject addressing agro-ecology, delta hydrology, haor wetland systems, boro/aman/aus rice cultivation, char-land farming, Deccan dry-land cropping, or coastal aquaculture — the precise subdomains required for this deployment. The dataset analysis confirmed this empirically across 175+ examples sampled from 37 configs: the closest environmental content observed is generic water chemistry and pastoralism definitions, with no South Asian agricultural systems represented [DATASET-D19, D22, D32]. Many subjects are actively irrelevant (US foreign policy, US history, US government), introducing construct-irrelevant variance for an agricultural science deployment. Given IO is a HIGH-priority dimension and the gap is structural and complete, this is a major validity violation.

**Strengths:**
- Universal STEM reasoning items (abstract algebra, formal logic, physics) provide a culturally-neutral baseline for cross-model comparison [DATASET Strength 1]
- Statistical inference items (hypothesis testing, sampling, Type I/II error) test methodology skills transferable to environmental science research [DATASET-D30]

**Checklist:**

- **IO-1**: Required categories for this deployment include haor/beel wetland ecology, boro/aman/aus rice cultivation, char-land farming, Brahmaputra-Jamuna floodplain hydrology, Deccan Rabi/Kharif dry-land cropping, brackishwater shrimp aquaculture, and Bangladesh–India transboundary water management — none of which are present in the 57-subject taxonomy. — _Sources: Q117_
- **IO-2**: MMLU's taxonomy omits every regionally-relevant agricultural and environmental science category. Subjects are bounded by US/Western academic disciplines [Q9, Q18, Q33], with history/geography framed through Western lenses [Q28, DATASET-D16, D20]. The 'breadth' claim of 57 tasks [Q11, Q83] does not translate into agro-ecological coverage. — _Sources: Q9, Q18, Q33, Q117, DATASET-D19, DATASET-D22, DATASET-D32_
- **IO-3**: MMLU includes substantial content irrelevant to South Asian agriculture: US Foreign Policy [Q171, DATASET-D5, D6], US History [Q151, DATASET-D2], US Government [DATASET-D3, D4], US tort/contract law [DATASET-D7, D8, D25], and Western European history [DATASET-D16, D17]. These consume evaluation weight without informing agricultural reasoning. — _Sources: Q1, DATASET-D2, DATASET-D3, DATASET-D4, DATASET-D5, DATASET-D6, DATASET-D7_
- **IO-4**: The complete absence of any agro-ecological subject combined with heavy weighting toward US-centric subjects creates content underrepresentation (missing constructs) and construct-irrelevant variance simultaneously — both validity-harming patterns. — _Sources: Q117, DATASET-D21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more.' (p.1)
- [Q9] 'The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more.' (p.1)
- [Q18] 'The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn.' (p.3)
- [Q33] 'STEM subjects include physics, computer science, mathematics, and more.' (p.4)
- [Q117] 'Table 2: Summary of all 57 tasks.' (p.15)

*Dataset analysis:*
- DATASET-D19: high_school_geography pastoralism definition is closest agriculture-adjacent content; no South Asian system represented
- DATASET-D22: college_biology covers cellular/molecular content, not agro-ecology
- DATASET-D32: nearest 'environmental science' is generic water-pollutant chemistry, not delta/saline-intrusion or haor ecology
- DATASET-D5: us_foreign_policy entirely US-centric — irrelevant to deployment
- DATASET-D2: high_school_us_history US Populist movement — no South Asian relevance
- DATASET-D21: nutrition is clinical biochemistry, not crop nutrition or soil science

</details>

**Information gaps:**
- Approximately 20 of 57 configs were not directly sampled by the dataset analysis; rare South Asian agricultural items in unreviewed configs cannot be entirely ruled out, though structural sourcing makes them improbable.

**Requires expert verification:**
- Whether any single MMLU item across the full 14,079-question test set addresses South Asian agro-ecology would require exhaustive scan of all 57 configs by a regional expert.

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
All MMLU content is sourced from US standardized tests (GRE, USMLE), undergraduate course materials, and Oxford University Press books [Q19], with Professional Law supplemented by Harvard Law Library case law [Q77] and history items drawing on English primary sources [Q140, Q141]. The authorship team is entirely US-based [Q10] and funding is from US sources [Q87, Q88]. Empirical sampling confirms US-centric content saturation: US tort law [DATASET-D7], US contract law [DATASET-D8], US Social Security [DATASET-D9], US birth control statistics [DATASET-D10], US Populist movement [DATASET-D2], MCAT references [DATASET-D39], and US measurement units [DATASET-D29]. South Asian content is limited to three tangential references (India internet 2017, India vs. Congo university graduates, Jainism/samsara) and one colonially-framed Indian Uprising item [DATASET-D13, D40, D36, D18]. No content from BRRI, BARI, BAU, ICAR, PJTSAU, or ANGRAU was identified, and gap searches confirmed no Bengali- or Telugu-language agricultural NLP corpus exists in the public landscape [WEB-22, WEB-6]. The Mymensingh-dialect agricultural vocabulary, Telugu dry-land terminology, and cross-border water-policy content required for this deployment are absent by construction.

**Strengths:**
- A handful of global_facts and world_religions items reference South Asia, providing a minimal foothold of non-exclusively-Western reference [DATASET-D13, D36, D40]
- PDF/separate-page sourcing reduces verbatim memorization risk, preserving construct measurement integrity for the topics it does cover [Q110]

**Checklist:**

- **IC-1**: Yes — many MMLU items require US-specific cultural and institutional knowledge (US tort law, Social Security, MCAT system, US demographic statistics) [DATASET-D7, D9, D10, D11, D39]. Conversely, items requiring Mymensingh, Bangladeshi, or Telugu-region knowledge are absent. — _Sources: Q19, DATASET-D7, DATASET-D9, DATASET-D10, DATASET-D11, DATASET-D39_
- **IC-2**: Culturally sensitive content (moral_scenarios anchored in 'US 2020 norms', US-centric birth control and aging facts) does not align with target deployment culture [DATASET-D1, D10, D11, D12]. Cross-border Bangladesh–India water-sharing topics — actively contested as of 2025 [WEB-1, WEB-2, WEB-4] — are not represented at all. — _Sources: DATASET-D1, DATASET-D10, DATASET-D11, DATASET-D12, WEB-1, WEB-2, WEB-4_
- **IC-3**: Inputs requiring Western-specific knowledge are pervasive: US Constitutional structure [DATASET-D3, D5], US legislative history [DATASET-D4], Burgess Chicago-school urban model [DATASET-D20], UK educational sociology [DATASET-D26]. These do not transfer to South Asian agricultural contexts. — _Sources: DATASET-D3, DATASET-D4, DATASET-D5, DATASET-D20, DATASET-D26_
- **IC-4**: INSUFFICIENT DOCUMENTATION on whether regional annotators reviewed any items; paper documents only US graduate/undergraduate collectors [Q19] and US MTurk baseline [Q22]. Full assessment would require recruiting Mymensingh, Telugu, and West Bengal agricultural experts to flag culturally sensitive instances. — _Sources: Q19, Q22_
- **IC-5**: Combined with Q19's exclusively US sourcing and the empirical pattern across 175+ sampled examples, content validity for this deployment is severely compromised. — _Sources: Q19, Q81, WEB-22, WEB-6_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q19] 'The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online. These include practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination.' (p.3)
- [Q77] 'We also had RoBERTa continue pretraining on approximately 1.6 million legal case summaries using Harvard's Law Library case law corpus' (p.8)
- [Q10] 'Dan Hendrycks, UC Berkeley; Collin Burns, Columbia University; Steven Basart, UChicago; Andy Zou, UC Berkeley; Mantas Mazeika, UIUC; Dawn Song, UC Berkeley; Jacob Steinhardt, UC Berkeley' (p.1)
- [Q140] 'This question refers to the following information.' (p.19)
- [Q141] 'English Parliament, Act of Supremacy, 1534' (p.19)
- [Q81] 'Data may also become a bottleneck, as there is far less written about esoteric branches of knowledge than about everyday situations.' (p.8)

*Web sources:*
- [WEB-22] AI4Bharat IndicNLP Catalog — no Bangladeshi-Bengali or Mymensingh-dialect agricultural corpus listed
- [WEB-6] ICICC 2024 Telugu agricultural perplexity study explicitly notes lack of Telugu agricultural NLP resources
- [WEB-1] Ganges Water Treaty expires Dec 2026, renewal pending — active geopolitical context absent from MMLU
- [WEB-2] Teesta water dispute remains unresolved as of 2025 — cross-border content not represented
- [WEB-4] Teesta Master Plan extended to Dec 2026 with Chinese financing — current South Asian agri-policy context absent

*Dataset analysis:*
- DATASET-D7: professional_law US tort scenario — confirms US legal context saturation
- DATASET-D8: professional_law US contract law — US cultural framing
- DATASET-D9: human_aging US Social Security — US institution as universal answer
- DATASET-D10: human_sexuality explicitly US-framed factual question
- DATASET-D11: human_sexuality 1988-1990 US-only survey data as correct answer
- DATASET-D29: elementary_mathematics uses miles per hour (US customary units)
- DATASET-D39: college_medicine references MCAT — US academic system
- DATASET-D13: global_facts India internet 2017 — only tangential South Asian factual reference
- DATASET-D40: global_facts India vs Congo university graduates — tangential
- DATASET-D36: world_religions Jainism — one of few South Asian cultural anchors
- DATASET-D18: high_school_world_history Cawnpore framed through British colonial journalism

</details>

**Information gaps:**
- Whether any unsampled config contains incidental Bangladesh- or Telugu-region agricultural content
- Whether annotators included any with South Asian regional expertise (paper does not document annotator demographics beyond US institutional affiliation)

**Requires expert verification:**
- BRRI/BARI/BAU agricultural extension experts could confirm absence of dialect-specific Mymensingh terminology
- Telugu agricultural linguistic experts (PJTSAU/ANGRAU) could confirm absence of Deccan dry-land cropping vocabulary

---

### Input Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MMLU is exclusively English-language, text-only, multiple-choice [Q8, Q21, Q45, Q46]. The HuggingFace metadata confirms monolingual English; every one of the 175+ examples sampled is English-only [DATASET-D2, D29, etc.]. The deployment elicitation explicitly requires Telugu, Bangladeshi Bengali (Mymensingh dialect), and Indian Bengali as query languages [elicitation A4, Q4]. Bengali script (বাংলা) and Telugu script (తెలుగు) are entirely unsupported. The paper's own authors acknowledge the limitation that 'many important concepts are conveyed mainly through other modalities' [Q64]. No transliteration, code-switching, or multilingual variant exists. Web research confirms no Bengali or Telugu agricultural-domain LLM evaluation infrastructure exists [WEB-5, WEB-17, WEB-18, WEB-25] and that LLMs perform meaningfully worse in Bengali than English [WEB-5]. This is an absolute, format-level mismatch that no in-format remediation can address. IF is a HIGH-priority dimension for this deployment, making this a fundamental validity violation.

**Strengths:**
- Standardized text-MCQ format is portable and computationally tractable for cross-model comparison [Q23, Q35]
- Format insensitivity findings for GPT-3 [Q100] mean that translated/adapted versions could in principle preserve relative model rankings if translation pipeline were added

**Checklist:**

- **IF-1**: Signal distribution mismatch is total: source benchmark is English ASCII text [Q8, Q45]; target deployment requires Bengali script (Bangladeshi and Indian variants), Telugu script, and English. No regional language input is supported. — _Sources: Q8, Q45, DATASET-D2, DATASET-D29_
- **IF-2**: Regional infrastructure does support text input — Bangladesh has 44.5–80% internet penetration [WEB-13, WEB-14] and mobile-first usage [WEB-15] — but this is irrelevant since MMLU's English-only constraint is the binding one, not regional capture capacity. — _Sources: WEB-13, WEB-14, WEB-15_
- **IF-3**: Domain-specific form differences include: (a) Bengali/Telugu script Unicode handling (no uppercase/lowercase distinction), (b) absence of multimodal capacity (acknowledged limitation [Q64]) which excludes diagrams/maps relevant to delta hydrology and AEZ classification, (c) no code-switching support relevant to Bengali-English bilingual scientific register. — _Sources: Q64, WEB-5_
- **IF-4**: Form mismatch is absolute and constitutes a complete external validity violation for the multilingual deployment requirement; no within-benchmark workaround exists. — _Sources: Q8, WEB-5, WEB-17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q8] 'We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings.' (p.1)
- [Q45] 'We feed GPT-3 prompts like that shown in Figure 1a. We begin each prompt with "The following are multiple choice questions (with answers) about [subject]."' (p.6)
- [Q64] 'many important concepts are conveyed mainly through other modalities, such as images, audio, and physical interaction (Bisk et al., 2020). Existing large-scale NLP models, such as GPT-3, do not incorporate multimodal information, so we design our benchmark to capture a diverse array of tasks in a text-only format.' (p.7)
- [Q21] 'We collected 15908 questions in total' (p.3)

*Web sources:*
- [WEB-5] arXiv 2507.23248 — LLMs perform worse in Bengali than English; smaller models especially degraded
- [WEB-17] AI4Bharat IndicBERT covers Bengali and Telugu but not agricultural domain
- [WEB-18] IndicTrans2 covers 22 Indian languages including Telugu but is a translation system, not knowledge benchmark
- [WEB-25] IndicXTREME (ACL 2023) covers Bengali/Telugu for general NLU but no agricultural evaluation

*Dataset analysis:*
- DATASET-D2: typical English-only question format with no provision for non-Latin scripts
- DATASET-D29: even basic numeric items use English with US customary units

</details>

**Information gaps:**
- Mymensingh-dialect-specific phonological/lexical variants in agricultural register are not documented in any retrievable NLP corpus and would require in-region linguist elicitation

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MMLU applies a uniform four-class MCQ schema (A/B/C/D) across all 57 tasks [Q23, Q35], with no mechanism to encode legitimate regional divergence in correct answers. The deployment explicitly anticipates such divergence — particularly for Bangladesh–India water-sharing questions [elicitation A3] where active 2025 geopolitical context (Ganges Treaty renewal, unresolved Teesta dispute, Kushiyara agreement) [WEB-1, WEB-2, WEB-4, WEB-21] would yield nationally divergent correct answers. The moral_scenarios config (500 items) explicitly anchors correctness to 'ordinary moral standards in the US as of 2020' as a constitutive framing across every item [DATASET-D1, D12], structurally precluding pluralism. The four-option forced-choice schema also cannot capture practice differences between delta flood-cycle planning and Deccan dry-land cropping. Models perform especially poorly on socially-important subjects (morality, law) [Q6, Q86] and on procedural/calculation tasks [Q14, Q72] — precisely the categories most relevant to agricultural decision-making. OO is HIGH-priority for this deployment, and the schema rigidity is a structural validity violation.

**Strengths:**
- Four-option MCQ schema is simple and reproducible for cross-model accuracy comparison [Q23, Q35]
- Difficulty levels (Elementary/High School/College/Professional) provide some stratification useful for capacity profiling [Q20]

**Checklist:**

- **OO-1**: The MCQ label space (A/B/C/D) [Q23] is generic and content-agnostic; it is not regionally relevant or irrelevant per se, but it cannot represent the categorical decision boundaries needed for regional agricultural reasoning (e.g., 'optimal under delta flood regime' vs. 'optimal under Deccan dry-land regime' as parallel correct answers). — _Sources: Q23_
- **OO-2**: Missing categories include: regional-pluralism markers (which national policy regime applies), agro-ecological zone qualifiers, and any output that would let a model express 'this depends on whether the question is from a Bangladeshi or Indian regulatory perspective' [WEB-1, WEB-2 — active treaty divergence]. — _Sources: WEB-1, WEB-2, WEB-4_
- **OO-3**: The moral_scenarios subtask explicitly encodes US 2020 norms as the constitutive correctness criterion [DATASET-D1, D12], embedding non-regional values directly into the output ontology. Human_sexuality and human_aging similarly embed US institutional facts as universally correct outputs [DATASET-D9, D10, D11]. — _Sources: DATASET-D1, DATASET-D9, DATASET-D10, DATASET-D12_
- **OO-4**: Significant misalignment exists; stakeholder-driven taxonomy redesign would require either (a) adding parallel-answer schema for regionally-divergent items or (b) excluding the affected subtasks. The paper itself notes models 'are notably poor at modeling human (dis)approval' [Q71], compounding OO concerns on socially-situated items. — _Sources: Q71, Q86_
- **OO-5**: The combination of forced single-correct-answer MCQ + US-anchored normative subtasks + procedural-calculation weakness [Q72] across calculation-heavy tasks (Elementary Mathematics RMS calibration error 19.4% [Q62]) creates structural validity issues for an agricultural decision-support evaluation. — _Sources: Q6, Q14, Q72_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q23] 'we instead create a simple-to-evaluate test that measures classification accuracy on multiple choice questions.' (p.3)
- [Q6] 'Worse, they still have near-random accuracy on some socially important subjects such as morality and law.' (p.1)
- [Q14] 'The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality.' (p.2)
- [Q71] 'They are notably poor at modeling human (dis)approval, as evident by the low performance on the Professional Law and Moral Scenarios tasks.' (p.8)
- [Q86] 'Worryingly, models also perform especially poorly on socially relevant subjects including morality and law.' (p.8)
- [Q72] 'Models also have difficulty performing calculations, so much so that they exhibit poor performance on Elementary Mathematics' (p.8)

*Web sources:*
- [WEB-1] Ganges Water Treaty expires Dec 2026 — bilateral water policy actively divergent
- [WEB-2] Teesta dispute unresolved with no formal treaty — nationally-divergent correct answers likely
- [WEB-4] Teesta Master Plan with Chinese financing — Bangladeshi vs Indian framings differ
- [WEB-21] 2022 Kushiyara Agreement — recent bilateral agreement requires up-to-date grounding

*Dataset analysis:*
- DATASET-D1: moral_scenarios explicitly frames correctness as 'US as of 2020' — constitutive framing
- DATASET-D12: moral_scenarios US 2020 framing repeats across all five sampled items, confirming structural rather than incidental
- DATASET-D9: human_aging encodes US Social Security as universally correct
- DATASET-D10: human_sexuality encodes US birth control statistics as correct answer

</details>

**Information gaps:**
- Whether any individual MMLU item explicitly flags regional divergence in its answer key (none observed in sample)

**Requires expert verification:**
- Bangladeshi and Indian water-policy experts would be needed to systematically identify items whose correct answer differs by national perspective

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The paper is silent on annotator demographics, selection criteria, regional or disciplinary backgrounds, or inter-annotator agreement [Q19]. The only documented human reference is US Amazon Mechanical Turk workers (34.5% accuracy) [Q22], with expert-level estimated from 'real-world test-taker human accuracy at the 95th percentile' on US standardized exams. The HuggingFace dataset card tags annotations_creators as 'no-annotation' [DATASET Concern 8]. The authorship team is entirely US-based [Q10] and content is sourced from US/Anglophone institutions [Q19, Q77]. There is no evidence — and no plausible mechanism — for South Asian agronomic, Mymensingh-dialect, or Telugu-region expert validation of any answer key. The user explicitly confirmed [elicitation A3] that cross-border water/agricultural questions could yield divergent correct answers and that practice differences between regions are not reflected in answer keys. Empirical sampling confirmed multiple items where US-specific facts (Social Security age increases, US birth control prevalence, US 2020 moral norms) are encoded as universally correct [DATASET-D1, D9, D10, D11, D12]. OC is HIGH-priority and represents a fundamental convergent and external validity violation.

**Strengths:**
- Authors commit to publishing question sources to enable downstream auditing [Q112]
- Memorization analysis suggests labels are not artifacts of pretraining contamination [Q107, Q108], so label correctness is at least an honest measurement of US-anchored ground truth

**Checklist:**

- **OC-1**: Ground truth labels reflect US/Anglophone academic standards [Q19, Q22], not Bangladeshi or Telugu-region stakeholder perspectives. The user [elicitation A3] confirms they would not be considered authoritative for cross-border or Bangladeshi-context agricultural questions. — _Sources: Q19, Q22, DATASET-D9, DATASET-D10_
- **OC-2**: Substantial disagreement is expected for: (a) moral_scenarios items (US 2020 framing) [DATASET-D1, D12]; (b) any cross-border water-policy item [WEB-1, WEB-2, WEB-4]; (c) human_aging/human_sexuality US institutional facts [DATASET-D9, D10, D11]; (d) potentially historical framings such as the Cawnpore item [DATASET-D18]. — _Sources: DATASET-D1, DATASET-D12, DATASET-D9, DATASET-D10, DATASET-D11, DATASET-D18, WEB-1, WEB-2_
- **OC-3**: INSUFFICIENT DOCUMENTATION — paper provides no Datasheet/Data Statement; only documents that questions were 'manually collected by graduate and undergraduate students' [Q19] without demographic breakdown. HF metadata indicates 'no-annotation' [DATASET Concern 8]. — _Sources: Q19, Q22_
- **OC-4**: Re-annotation by representative regional annotator pool (BAU, BRRI, PJTSAU, ANGRAU agronomists; Bangladeshi and Indian water-policy experts) would be required for any deployment-relevant subset; the paper offers no such pool.
- **OC-5**: Aggregation methods are not described; the single-correct-answer MCQ format inherently erases minority perspectives [Q23], which is particularly concerning for cross-border and culturally-situated questions. — _Sources: Q23_
- **OC-6**: The combined absence of regional annotator validation, the explicit US-normative framing of large subtasks, and the user-confirmed expectation of divergent correct answers constitute serious convergent and external validity violations. — _Sources: Q19, DATASET-D1, WEB-1, WEB-21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q19] 'The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online.' (p.3)
- [Q22] 'Unspecialized humans from Amazon Mechanical Turk obtain 34.5% accuracy on this test.' (p.3)
- [Q10] 'Dan Hendrycks, UC Berkeley; Collin Burns, Columbia University; Steven Basart, UChicago...' (p.1)
- [Q87] 'DH is supported by the NSF GRFP Fellowship and an Open Philanthropy Project Fellowship.' (p.9)
- [Q88] 'This research was also supported by the NSF Frontier Award 1804794.' (p.9)

*Web sources:*
- [WEB-1] Active Bangladesh–India treaty renewal context — divergent correct answers likely
- [WEB-2] Teesta dispute unresolved — Bangladesh and India would adjudicate water-allocation questions differently
- [WEB-21] Kushiyara River Agreement — recent bilateral agreement not reflected in 2021 benchmark labels

*Dataset analysis:*
- DATASET-D1: moral_scenarios US 2020 framing as constitutive answer criterion
- DATASET-D9: human_aging Social Security as universally correct answer
- DATASET-D10: human_sexuality US birth control statistics as correct answer
- DATASET-D11: human_sexuality 1988-1990 US-specific survey data as correct answer
- DATASET-D12: US 2020 moral framing replicated across all sampled moral_scenarios items
- DATASET-D18: Indian Uprising framed via British colonial journalism — label set by US team
- DATASET Concern 8: HF metadata tags annotations_creators as 'no-annotation'

</details>

**Information gaps:**
- Annotator demographic information is entirely absent from documentation
- No quality-assurance or inter-annotator agreement statistics reported

**Requires expert verification:**
- Specific items where Bangladeshi vs Indian agronomic standards would diverge would require BAU/PJTSAU/ANGRAU expert review
- Cross-border water-policy item answer keys would require Joint Rivers Commission expert adjudication

---

### Output Form — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
MMLU evaluates only text-based MCQ classification accuracy [Q23, Q35] via predicted A/B/C/D tokens [Q45]. The metric (accuracy) and calibration measures (RMS calibration error, accuracy-confidence gap) [Q60, Q62] partially align with the deployment's stated need for cross-model comparison. However, the format cannot evaluate open-ended agronomic reasoning, does not penalize language mismatches (e.g., model responding in English to a Bengali prompt), and does not support regional-language outputs. The user did not flag output form as a primary concern (MODERATE priority), and MCQ accuracy is at least usable as a baseline. But the format precludes evaluating practice-difference reasoning, generative explanations of flood-cycle decisions, or Bengali/Telugu-language extension communication — all relevant for downstream farmer/agronomist applications. Combined with the 'esoteric knowledge' data bottleneck [Q81] amplified for South Asian agricultural content, output form is partially aligned but insufficient for deployment-validity evaluation.

**Strengths:**
- Single accuracy metric is reproducible and supports cross-model comparison [Q35, Q42]
- Calibration analysis (RMS calibration error, accuracy-confidence gap) provides useful uncertainty diagnostics for downstream deployment risk assessment [Q60, Q61, Q62, Q106]
- Per-task and per-grouping reporting [Q52, Q92] would in principle let a user isolate STEM-reasoning subscores even while ignoring US-content subscores

**Checklist:**

- **OF-1**: Output modality (single letter token) [Q45] does not match deployment needs — environmental science applications often require open-ended explanation, calculation, or recommendation. The MCQ format aligns only with the cross-model comparison goal. — _Sources: Q35, Q45_
- **OF-2**: Text-to-speech is not relevant to MMLU's evaluation metric; not applicable to this benchmark form.
- **OF-3**: Literacy considerations: Bangladesh national literacy is 77.9% [WEB-7], functional literacy 62.92% [WEB-8]; Telangana 66.54% and Andhra Pradesh 67.02% [WEB-9, WEB-11]. The downstream farmer/agronomist sub-population would not directly interact with an English-MCQ output anyway, but for any extension-tool evaluation, output form would need to support Bengali/Telugu generative output — which MMLU does not assess. — _Sources: WEB-7, WEB-8, WEB-9, WEB-11_
- **OF-4**: Form mismatches are real but partial; MCQ accuracy can serve as a baseline benchmark while requiring substantial supplementation (open-ended generation, multilingual generation evaluation) for deployment-level validity. — _Sources: Q35, Q81_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q35] 'To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks.' (p.5)
- [Q45] 'The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction.' (p.6)
- [Q60] 'We evaluate the calibration of GPT-3 by testing how well its average confidence estimates its actual accuracy for each subject.' (p.7)
- [Q61] 'GPT-3 is uncalibrated. In fact, its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects.' (p.7)
- [Q81] 'Data may also become a bottleneck, as there is far less written about esoteric branches of knowledge than about everyday situations.' (p.8)

*Web sources:*
- [WEB-7] Bangladesh literacy 77.9% (BBS 2024)
- [WEB-8] Bangladesh functional literacy 62.92% (BBS LAS 2023)
- [WEB-9] Telangana literacy 66.54% (Census 2011)
- [WEB-11] Andhra Pradesh literacy 67.02% (Census 2011)

</details>

**Information gaps:**
- Whether deployment will require open-ended generation or remain MCQ-style was not fully specified in elicitation

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** MMLU's 57-subject taxonomy contains no agro-ecological, delta-ecology, or South Asian regional agricultural subjects — the precise constructs the deployment must measure.

**Recommendation:** Treat MMLU as a generic STEM/reasoning baseline only and pair it with a purpose-built South Asian agricultural knowledge benchmark organized by AEZ (haor, char-land, Deccan dry-land, coastal aquaculture) co-designed with BAU, BRRI, PJTSAU, and ANGRAU. Restrict MMLU reporting to a curated subset of culturally-neutral STEM configs (abstract algebra, college mathematics, college physics, formal logic, high school statistics).

### Input Content ⚠

**Gap:** Content is entirely sourced from US/Anglophone institutions [Q19, Q77]; no Bengali- or Telugu-language agricultural content; cross-border policy context (Ganges/Teesta) absent.

**Recommendation:** Author a parallel evaluation set sourcing items from BRRI/BARI technical bulletins, PJTSAU/ANGRAU extension publications, and Joint Rivers Commission documents. Use the AgriPriceBD [WEB-23] LLM-assisted PDF parsing methodology to digitize Bengali agricultural reports. Build dialect-aware Mymensingh-Bengali corpus through BAU faculty elicitation (acknowledging this is unsearchable web-research territory).

### Input Form ⚠

**Gap:** English-only text input precludes Bengali (both variants), Telugu, and any multilingual evaluation explicitly required by the deployment.

**Recommendation:** Do not use MMLU for any multilingual capability assessment. Build a multilingual evaluation pipeline using IndicXTREME [WEB-25] as the structural template and IndicTrans2 [WEB-18] for translation infrastructure, with native-script Bengali and Telugu items. Plan evaluation to detect language-mismatch failures (e.g., model responding in English to Bengali prompts).

### Output Ontology ⚠

**Gap:** Four-option MCQ schema cannot encode legitimate regional divergence in correct answers (especially cross-border water/agricultural policy); moral_scenarios encodes US 2020 norms structurally [DATASET-D1, D12].

**Recommendation:** Exclude moral_scenarios, human_sexuality, human_aging, and US-jurisdiction-specific configs from any deployment-relevant scoring. For the supplementary regional benchmark, design schema permitting parallel-correct-answer annotation flagged by jurisdiction (Bangladesh / India / state-level) for water-policy and agricultural-policy items.

### Output Content ⚠

**Gap:** No South Asian annotators were involved in label creation; user confirmed cross-border questions would yield divergent correct answers; HF metadata tags annotations as 'no-annotation'.

**Recommendation:** For any subset of MMLU items used in deployment evaluation, conduct a relabeling pass with at least three annotators per item drawn from a pool spanning Bangladesh (BAU, BRRI), Telangana (PJTSAU), and Andhra Pradesh (ANGRAU). Track inter-annotator disagreement rates and exclude items where regional disagreement exceeds threshold. Document annotator demographics in a Datasheet.

### Output Form

**Gap:** MCQ accuracy cannot capture open-ended agronomic reasoning needed for downstream farmer/agronomist applications, and does not penalize language-mismatch failures.

**Recommendation:** Supplement MMLU MCQ accuracy with open-ended generative evaluation in Bengali and Telugu, evaluated by regional experts using rubrics that explicitly penalize language drift (English response to Bengali prompt) and reward dialect-appropriate register for Mymensingh-Bengali agricultural extension communication.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "We propose a new test to measure a text model's multitask accuracy. The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more." |
| Q2 | 1 | input_ontology | "To attain high accuracy on this test, models must possess extensive world knowledge and problem solving ability." |
| Q3 | 1 | output_form | "We find that while most recent models have near random-chance accuracy, the very largest GPT-3 model improves over random chance by almost 20 percentage points on average." |
| Q4 | 1 | output_form | "However, on every one of the 57 tasks, the best models still need substantial improvements before they can reach expert-level accuracy." |
| Q5 | 1 | output_form | "Models also have lopsided performance and frequently do not know when they are wrong." |
| Q6 | 1 | output_ontology | "Worse, they still have near-random accuracy on some socially important subjects such as morality and law." |
| Q7 | 1 | output_form | "By comprehensively evaluating the breadth and depth of a model's academic and professional understanding, our test can be used to analyze models across many tasks and to identify important shortcomings." |
| Q8 | 1 | input_form | "We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings." |
| Q9 | 1 | input_ontology | "The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more. It ranges in difficulty from an elementary level to an advanced professional level, and it tests both world knowledge and problem solving ability." |
| Q10 | 1 | output_content | "Dan Hendrycks, UC Berkeley; Collin Burns, Columbia University; Steven Basart, UChicago; Andy Zou, UC Berkeley; Mantas Mazeika, UIUC; Dawn Song, UC Berkeley; Jacob Steinhardt, UC Berkeley" |
| Q11 | 2 | input_ontology | "Since our test consists in 57 tasks, it can be used to analyze aggregate properties of models across tasks and to track important shortcomings." |
| Q12 | 2 | output_form | "few-shot models up to 13 billion parameters (Brown et al., 2020) achieve random chance performance of 25% accuracy, but the 175 billion parameter GPT-3 model reaches a much higher 43.9% accuracy" |
| Q13 | 2 | output_form | "unlike human professionals GPT-3 does not excel at any single subject. Instead, we find that performance is lopsided, with GPT-3 having almost 70% accuracy for its best subject but near-random performance for several other subjects." |
| Q14 | 2 | output_ontology | "The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality." |
| Q15 | 2 | output_form | "GPT-3 does not have an accurate sense of what it does or does not know since its average confidence can be up to 24% off from its actual accuracy." |
| Q16 | 2 | input_content | "The dominant paradigm in NLP is to pretrain large models on massive text corpora including educational books and websites." |
| Q17 | 2 | input_ontology | "Many recent benchmarks aim to assess a model's general world knowledge and basic reasoning ability by testing its "commonsense."" |
| Q18 | 3 | input_ontology | "We create a massive multitask test consisting of multiple-choice questions from various branches of knowledge. The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn. There are 57 tasks in total, which is also the number of Atari games (Bellemare et al., 2013), all of which are listed in Appendix B." |
| Q19 | 3 | input_content | "The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online. These include practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination. It also includes questions designed for undergraduate courses and questions designed for readers of Oxford University Press books." |
| Q20 | 3 | output_ontology | "Some tasks cover a subject, like psychology, but at a specific level of difficulty, such as "Elementary," "High School," "College," or "Professional."" |
| Q21 | 3 | input_form | "We collected 15908 questions in total, which we split into a few-shot development set, a validation set, and a test set. The few-shot development set has 5 questions per subject, the validation set may be used for selecting hyperparameters and is made of 1540 questions, and the test set has 14079 questions. Each subject contains 100 test examples at the minimum, which is longer than most exams designed to assess people." |
| Q22 | 3 | output_content | "Human-level accuracy on this test varies. Unspecialized humans from Amazon Mechanical Turk obtain 34.5% accuracy on this test. Meanwhile, expert-level performance can be far higher. For example, real-world test-taker human accuracy at the 95th percentile is around 87% for US Medical Licensing Examinations, and these questions make up our "Professional Medicine" task. If we take the 95th percentile human test-taker accuracy for exams that build up our test, and if we make an educated guess when such information is unavailable, we then estimate that expert-level accuracy is approximately 89.8%." |
| Q23 | 3 | output_ontology | "we instead create a simple-to-evaluate test that measures classification accuracy on multiple choice questions." |
| Q24 | 3 | input_ontology | "Since our test aggregates different subjects and several levels of difficulty, we measure more than straightforward commonsense or narrow linguistic understanding." |
| Q25 | 4 | input_ontology | "The humanities is a group of disciplines that make use of qualitative analysis and analytic methods rather than scientific empirical methods. Branches of the humanities include law, philosophy, history, and so on (Appendix B)." |
| Q26 | 4 | input_ontology | "Mastering these subjects requires a variety of skills. For example, legal understanding requires knowledge of how to apply rules and standards to complex scenarios, and also provide answers with stipulations and explanations." |
| Q27 | 4 | input_ontology | "For philosophy, our questions cover concepts like logical fallacies, formal logic, and famous philosophical arguments. It also covers moral scenarios, including questions from the ETHICS dataset (Hendrycks et al., 2020) that test a model's understanding of normative statements through predicting widespread moral intuitions about diverse everyday scenarios." |
| Q28 | 4 | input_ontology | "Finally, our history questions cover a wide range of time periods and geographical locations, including prehistory and other advanced subjects." |
| Q29 | 4 | input_ontology | "Social science includes branches of knowledge that examine human behavior and society. Subject areas include economics, sociology, politics, geography, psychology, and so on." |
| Q30 | 4 | input_ontology | "Our economics questions include microeconomics, macroeconomics, and econometrics, and cover different types of problems, including questions that require a mixture of world knowledge, qualitative reasoning, or quantitative reasoning." |
| Q31 | 4 | input_ontology | "We also include important but more esoteric topics such as security studies in order to test the boundaries of what is experienced and learned during pretraining." |
| Q32 | 4 | input_ontology | "Social science also includes psychology, a field that may be especially important for attaining a nuanced understanding of humans." |
| Q33 | 4 | input_ontology | "STEM subjects include physics, computer science, mathematics, and more." |
| Q34 | 4 | input_ontology | "Conceptual physics tests understanding of simple physics principles and may be thought" |
| Q35 | 5 | output_form | "To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks." |
| Q36 | 5 | output_form | "We evaluate GPT-3 (Brown et al., 2020) and UnifiedQA (Khashabi et al., 2020)." |
| Q37 | 5 | output_form | "For GPT-3 we use the OpenAI API, which provides access to four model variants, "Ada," "Babbage," "Curie," and "Davinci," which we refer to as "Small" (2.7 billion parameters), "Medium" (6.7 billion), "Large" (13 billion) and "X-Large" (175 billion)." |
| Q38 | 5 | output_form | "UnifiedQA uses the T5 (Raffel et al., 2019) text-to-text backbone and is fine-tuned on previously proposed question answering datasets (Lai et al., 2017), where the prediction is the class with the highest token overlap with UnifiedQA's text output." |
| Q39 | 5 | output_form | "Since UnifiedQA is fine-tuned on other datasets, we evaluate it without any further tuning to assess its transfer accuracy." |
| Q40 | 5 | output_form | "We also fine-tune RoBERTa-base, ALBERT-xxlarge, and GPT-2 on UnifiedQA training data and our dev+val set." |
| Q41 | 5 | output_form | "We primarily focus on UnifiedQA and GPT-3 in the rest of this document, but additional discussion of RoBERTa, ALBERT, and GPT-2 is in Appendix A." |
| Q42 | 5 | output_form | "All values are percentages." |
| Q43 | 5 | output_form | "Some models proposed in the past few months can move several percent points beyond random chance." |
| Q44 | 5 | output_form | "GPT-3 uses few-shot learning and UnifiedQA is tested under distribution shift." |
| Q45 | 6 | input_form | "We feed GPT-3 prompts like that shown in Figure 1a. We begin each prompt with "The following are multiple choice questions (with answers) about [subject]." For zero-shot evaluation, we append the question to the prompt. For few-shot evaluation, we add up to 5 demonstration examples with answers to the prompt before appending the question. All prompts end with "Answer: ". The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction." |
| Q46 | 6 | input_form | "For consistent evaluation, we create a dev set with 5 fixed few-shot examples for each subject." |
| Q47 | 6 | output_form | "We find that the three smaller GPT-3 models have near random accuracy (around 25%). In contrast, we find that the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%." |
| Q48 | 6 | output_form | "While the smaller models have around 25% zero-shot accuracy, Figure 10 in Appendix A shows that the largest GPT-3 model has a much higher zero-shot accuracy of about 37.7%." |
| Q49 | 6 | output_form | "The largest UnifiedQA model we test has 11 billion parameters, which is slightly smaller than GPT-3 Large. Nevertheless, we show in Table 1 that it attains 48.9% accuracy." |
| Q50 | 6 | output_form | "We also find that even the smallest UnifiedQA variant, with just 60 million parameters, has approximately 29.3% accuracy." |
| Q51 | 6 | output_form | "These results suggest that while model size is a key component for achieving strong performance, fine-tuning also helps." |
| Q52 | 6 | output_form | "Figure 6 shows the accuracy of GPT-3 (few-shot) and UnifiedQA for all 57 tasks. It shows the both models are below expert-level performance for all tasks, with GPT-3's accuracy ranging from 69% for US Foreign Policy to 26% for College Chemistry." |
| Q53 | 6 | output_form | "UnifiedQA does best on marketing, with an accuracy of 82.5%." |
| Q54 | 6 | output_ontology | "Overall, models do poorly on highly procedural problems. Figure 6 shows that calculation-heavy STEM subjects tend to have low accuracy compared to verbal subjects." |
| Q55 | 6 | output_ontology | "For GPT-3, 9 out of the 10 lowest-accuracy tasks are STEM subjects that emphasize mathematics or calculations. We speculate that is in part because GPT-3 acquires declarative knowledge more readily than procedural knowledge." |
| Q56 | 7 | input_ontology | "For example, many questions in Elementary Mathematics require applying the order of operations for arithmetic, which is described by the acronym PEMDAS (Parentheses Exponents Multiplication Division Addition Subtraction)." |
| Q57 | 7 | output_ontology | "We confirm that GPT-3 is aware of the acronym PEMDAS. However, it does not consistently apply PEMDAS to actual problems." |
| Q58 | 7 | output_ontology | "We find that some verbal tasks such as Moral Scenarios from Hendrycks et al. (2020) and Professional Law also have especially low accuracy." |
| Q59 | 7 | output_ontology | "GPT-3 does better on College Medicine (47.4%) and College Mathematics (35.0%) than calculation-heavy Elementary Mathematics (29.9%)." |
| Q60 | 7 | output_form | "We evaluate the calibration of GPT-3 by testing how well its average confidence estimates its actual accuracy for each subject." |
| Q61 | 7 | output_form | "GPT-3 is uncalibrated. In fact, its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects." |
| Q62 | 7 | output_form | "Another calibration measure is the Root Mean Squared (RMS) calibration error (Hendrycks et al., 2019a; Kumar et al., 2019). Many tasks have miscalibrated predictions, such as Elementary Mathematics which has a zero-shot RMS calibration error of 19.4%." |
| Q63 | 7 | input_content | "A major distinction between our benchmark and previous multitask NLP benchmarks is that we do not require large training sets. Instead, we assume that models have acquired the requisite knowledge from reading vast quantities of diverse text from the Internet." |
| Q64 | 7 | input_form | "While text is capable of conveying an enormous number of concepts about the world, many important concepts are conveyed mainly through other modalities, such as images, audio, and physical interaction (Bisk et al., 2020). Existing large-scale NLP models, such as GPT-3, do not incorporate multimodal information, so we design our benchmark to capture a diverse array of tasks in a text-only format." |
| Q65 | 8 | input_ontology | "This motivates us to propose a methodological change so that models are trained more like how humans learn." |
| Q66 | 8 | output_form | "For this reason we assess pretrained models in a zero-shot, few-shot, or transfer setting and we provide a dev, val, and test set for each task." |
| Q67 | 8 | output_form | "The dev set is used for few-shot prompts, the val set could be used for hyperparameter tuning, and the test set is used to compute the final accuracy." |
| Q68 | 8 | input_form | "Importantly, the format of our evaluation is not identical to the format in which information is acquired during pretraining." |
| Q69 | 8 | output_content | "This has the benefit of obviating concerns about spurious training set annotation artifacts (Geirhos et al., 2020; Hendrycks et al., 2019b) and is in stark contrast to the previous paradigm of identically distributed training and test sets." |
| Q70 | 8 | output_form | "We find that current large-scale Transformers have wide room for improvement." |
| Q71 | 8 | output_ontology | "They are notably poor at modeling human (dis)approval, as evident by the low performance on the Professional Law and Moral Scenarios tasks." |
| Q72 | 8 | output_ontology | "Models also have difficulty performing calculations, so much so that they exhibit poor performance on Elementary Mathematics and many other STEM subjects with "plug and chug" problems." |
| Q73 | 8 | output_form | "Additionally, they do not match expert-level performance (90%) on any subject, so for all subjects it is subhuman." |
| Q74 | 8 | output_form | "On average, models are only now starting to move beyond random-chance accuracy levels." |
| Q75 | 8 | input_content | "We collected approximately 2,000 additional Professional Law training examples." |
| Q76 | 8 | output_form | "After fine-tuning a RoBERTa-base model (Liu et al., 2019) using this custom training set, our model attained 32.8% test accuracy." |
| Q77 | 8 | input_content | "We also had RoBERTa continue pretraining on approximately 1.6 million legal case summaries using Harvard's Law Library case law corpus case.law, but after fine-tuning it only attained 36.1% accuracy." |
| Q78 | 8 | output_form | "This suggests that while additional pretraining on relevant high quality text can help, it may not be enough to substantially increase the performance of current models." |
| Q79 | 8 | output_form | "It is unclear whether simply scaling up existing language models will solve the test." |
| Q80 | 8 | output_form | "Current understanding indicates that a 10× increase in model size must be accompanied by an approximate 5× increase in data (Kaplan et al., 2020)." |
| Q81 | 8 | input_content | "Data may also become a bottleneck, as there is far less written about esoteric branches of knowledge than about everyday situations." |
| Q82 | 8 | input_ontology | "We introduced a new test that measures how well text models can learn and apply knowledge encountered during pretraining." |
| Q83 | 8 | input_ontology | "By covering 57 subjects at varying levels of difficulty, the test assesses language understanding in greater breadth and depth than previous benchmarks." |
| Q84 | 8 | output_form | "We found that it has recently become possible for models to make meaningful progress on the test, but that state-of-the-art models have lopsided performance and rarely excel at any individual task." |
| Q85 | 8 | output_form | "We also showed that current models are uncalibrated and have difficulty with tasks that require calculations." |
| Q86 | 8 | output_ontology | "Worryingly, models also perform especially poorly on socially relevant subjects including morality and law." |
| Q87 | 9 | output_content | "DH is supported by the NSF GRFP Fellowship and an Open Philanthropy Project Fellowship." |
| Q88 | 9 | output_content | "This research was also supported by the NSF Frontier Award 1804794." |
| Q89 | 11 | input_ontology | "This appendix includes figures with sorted results (Figure 9), few-shot examples vs. accuracy (Figure 10), and few-shot calibration (Figure 11). It also includes sections on fine-tuning, error analysis, and format sensitivity." |
| Q90 | 11 | output_form | "We primarily analyzed models with more than 10 billion parameters in the main body of the paper." |
| Q91 | 11 | input_ontology | "For this section, we analyze smaller models including RoBERTa-base (125 million parameters) (Liu" |
| Q92 | 11 | output_form | "On the left are GPT-3 few shot accuracies for all of the 57 tasks. On the right are UnifiedQA transfer accuracies for all of the 57 tasks. For both models, capabilities are lopsided." |
| Q93 | 12 | output_form | "Models are fine-tuned to predict one of four classes using the UnifiedQA MCQ questions and using our dev+val set. We test on our multitask test set." |
| Q94 | 12 | output_form | "RoBERTa-base attains an overall accuracy of 27.9%, with 27.9% accuracy for the humanities, 28.8% for social sciences, 27.0% for STEM, and 27.7% for other." |
| Q95 | 12 | output_form | "ALBERT-xxlarge attains an accuracy of 27.1%, with 27.2% accuracy for the humanities, 25.7% for the social sciences, 27.7% for STEM, and 27.9% for other." |
| Q96 | 12 | output_form | "GPT-2 attains an accuracy of 32.4%, with 32.8% accuracy for the humanities, 33.3% for the social sciences, 30.2% for STEM, and 33.1% for other." |
| Q97 | 12 | output_form | "Compare this to UnifiedQA's smallest variant, which has just 60 million parameters and approximately 29.3% accuracy. It obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters." |
| Q98 | 12 | output_form | "UnifiedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy." |
| Q99 | 12 | output_content | "We qualitatively analyze when GPT-3 makes high confidence mistakes. We find that while many of these mistakes were clearly wrong, many were mistakes that a human might make." |
| Q100 | 12 | input_form | "While different question formatting choices often lead to similar GPT-3 accuracies, we find that UnifiedQA is more sensitive." |
| Q101 | 12 | input_form | "UnifiedQA's input format is of the form QUESTION1 \\n (A) CHOICE1 (B) CHOICE2 (C) CHOICE3 (D) CHOICE4</s> where questions and choices are normalized and made lowercase." |
| Q102 | 12 | input_form | "If we remove the </s> from the input, accuracy declines by several percentage points." |
| Q103 | 13 | input_ontology | "We provide analysis of question length and difficulty in Figure 12. We list all tasks and the topics they test in Table 2. We also provide an example for each task starting with Figure 14." |
| Q104 | 13 | output_content | "Since language models train on vast text corpora, there is some chance that they have seen the exact question and answer during pretraining. If they memorized the exact question and answer, then they would attain higher accuracy than their true ability. Likewise, a question's entropy would be especially low if it were memorized. Memorized questions and answers should have low entropy and" |
| Q105 | 13 | input_form | "For questions longer than a tweet (280 characters), the correlation between question length and true label confidence is slightly positive. This shows that longer questions are not necessarily harder." |
| Q106 | 13 | output_form | "While models are more calibrated in a few-shot setting than a zero-shot setting, they are still miscalibrated, with gap between accuracy and confidence reaching up to 14%. Here the correlation between confidence and accuracy is r = 0.81, compared to r = 0.63 in the zero-shot setting." |
| Q107 | 14 | output_content | "However, in Figure 13, we see that accuracy and question entropy are not positively correlated, suggesting that the test's low-entropy questions do not correspond to memorized (and thereby correctly predicted) answers." |
| Q108 | 14 | output_content | "This suggests that our exact questions were not memorized." |
| Q109 | 14 | input_content | "However, during pretraining models encountered text related to our questions through processing Wikipedia." |
| Q110 | 14 | input_content | "We also note that most of our questions came from PDFs or websites where questions and answers are on separate pages." |
| Q111 | 14 | output_content | "See Brown et al. (2020) for a previous discussion of contamination showing that the phenomena hardly affects performance." |
| Q112 | 14 | output_content | "To reduce the probability that future models encounter exact questions during test-time, we will provide a list of question sources." |
| Q113 | 14 | output_form | "The average log probability of the question (without answer) is not strongly positively correlated with accuracy, all else equal." |
| Q114 | 14 | output_form | "Each point corresponds to a task." |
| Q115 | 14 | output_form | "Higher log probability indicates higher compression, and especially high log probability would suggest memorization." |
| Q116 | 14 | output_form | "In the zero-shot question prompt, the correlation between average log probability and accuracy is r = −0.43, and for the few-shot setting the correlation is r = −0.56." |
| Q117 | 15 | input_ontology | "Table 2: Summary of all 57 tasks." |
| Q118 | 16 | input_ontology | "Find all c in Z₃ such that Z₃[x]/(x² + c) is a field." |
| Q119 | 16 | input_ontology | "What is the embryological origin of the hyoid bone?" |
| Q120 | 16 | input_ontology | "Why isn't there a planet where the asteroid belt is located?" |
| Q121 | 16 | input_ontology | "Three contrasting tactics that CSO's can engage in to meet their aims are which typically involves research and communication, , which may involve physically attacking a company's operations or , often involving some form of ." |
| Q122 | 16 | input_ontology | "How many attempts should you make to cannulate a patient before passing the job on to a senior colleague?" |
| Q123 | 16 | input_ontology | "In a given population, 1 out of every 400 people has a cancer caused by a completely recessive allele, b. Assuming the population is in Hardy-Weinberg equilibrium, which of the following is the expected proportion of individuals who carry the b allele but are not expected to develop the cancer?" |
| Q124 | 16 | input_ontology | "Which of the following statements about the lanthanide elements is NOT true?" |
| Q125 | 17 | input_ontology | "Consider a computer design in which multiple processors, each with a private cache memory, share global memory using a single bus. This bus is the critical system resource. Each processor can execute one instruction every 500 nanoseconds as long as memory references are satisfied by its local cache. When a cache miss occurs, the processor is delayed for an additional 2,000 nanoseconds. During half of this additional delay, the bus is dedicated to serving the cache miss. During the other half, the processor cannot continue, but the bus is free to service requests from other processors. On average, each instruction requires 2 memory references. On average, cache misses occur on 1 percent of references. What proportion of the capacity of the bus would a single processor consume, ignoring delays due to competition from other processors?" |
| Q126 | 17 | input_ontology | "Let A be a real 2 × 2 matrix. Which of the following statements must be true? I. All of the entries of A2are nonnegative. II. The determinant of A2is nonnegative. III. If A has two distinct eigenvalues, then A2 has two distinct eigenvalues." |
| Q127 | 17 | input_ontology | "In a genetic test of a newborn, a rare genetic disorder is found that has X-linked recessive transmission. Which of the following statements is likely true regarding the pedigree of this disorder?" |
| Q128 | 17 | input_ontology | "One end of a Nichrome wire of length 2L and cross-sectional area A is attached to an end of another Nichrome wire of length L and cross- sectional area 2A. If the free end of the longer wire is at an electric potential of 8.0 volts, and the free end of the shorter wire is at an electric potential of 1.0 volt, the potential at the junction of the two wires is most nearly equal to" |
| Q129 | 17 | input_ontology | "Why is it that anti-virus scanners would not have found an exploitation of Heartbleed?" |
| Q130 | 17 | input_ontology | "A model airplane flies slower when flying into the wind and faster with wind at its back. When launched at right angles to the wind, a cross wind, its groundspeed compared with flying in still air is" |
| Q131 | 18 | input_ontology | "Consider the following AR(1) model with the disturbances having zero mean and unit variance yt = 0.2 + 0.4yt−1 + ut The (unconditional) mean of y will be given by (A) 0.2 (B) 0.4 (C) 0.5 (D) 0.33" |
| Q132 | 18 | input_ontology | "A point pole has a strength of 4π × 10−4 weber. The force in newtons on a point pole of 4π × 1.5 × 10−4 weber placed at a distance of 10 cm from it will be (A) 15 N. (B) 20 N. (C) 7.5 N. (D) 3.75 N." |
| Q133 | 18 | input_ontology | "A total of 30 players will play basketball at a park. There will be exactly 5 players on each team. Which statement correctly explains how to find the number of teams needed? (A) Add 5 to 30 to find 35 teams. (B) Divide 30 by 5 to find 6 teams. (C) Multiply 30 and 5 to find 150 teams. (D) Subtract 5 from 30 to find 25 teams." |
| Q134 | 18 | input_ontology | "Determine whether the statements are logically equivalent or contradictory. If neither, determine whether they are consistent or inconsistent. E ⊃ (F · E) and ∼ E · F (A) Logically equivalent (B) Contradictory (C) Neither logically equivalent nor contradictory, but consistent (D) Inconsistent" |
| Q135 | 18 | input_content | "As of 2017, how many of the world's 1-year-old children today have been vaccinated against some disease? (A) 80% (B) 60% (C) 40% (D) 20%" |
| Q136 | 18 | input_ontology | "Homologous structures are often cited as evidence for the process of natural selection. All of the following are examples of homologous structures EXCEPT (A) the wings of a bird and the wings of a bat (B) the flippers of a whale and the arms of a man (C) the pectoral fins of a porpoise and the flippers of a seal (D) the forelegs of an insect and the forelimbs of a dog" |
| Q137 | 18 | input_ontology | "From the solubility rules, which of the following is true? (A) All chlorides, bromides, and iodides are soluble (B) All sulfates are soluble (C) All hydroxides are soluble (D) All ammonium-containing compounds are soluble" |
| Q138 | 19 | input_ontology | "A list of numbers has n elements, indexed from 1 to n. The following algorithm is intended to display the number of elements in the list that have a value greater than 100. The algorithm uses the variables count and position. Steps 3 and 4 are missing." |
| Q139 | 19 | input_ontology | "Which of the following could be used to replace steps 3 and 4 so that the algorithm works as intended?" |
| Q140 | 19 | input_content | "This question refers to the following information." |
| Q141 | 19 | input_content | "English Parliament, Act of Supremacy, 1534" |
| Q142 | 19 | input_ontology | "From the passage, one may infer that the English Parliament wished to argue that the Act of Supremacy would" |
| Q143 | 19 | input_ontology | "During the third stage of the demographic transition model, which of the following is true?" |
| Q144 | 20 | input_ontology | "Figure 37: A High School Government and Politics example." |
| Q145 | 20 | input_ontology | "Figure 38: A High School Macroeconomics example." |
| Q146 | 20 | input_ontology | "Figure 39: A High School Mathematics example." |
| Q147 | 20 | input_ontology | "Figure 40: A High School Microeconomics example." |
| Q148 | 20 | input_ontology | "Figure 41: A High School Physics example." |
| Q149 | 20 | input_ontology | "Figure 42: A High School Psychology example." |
| Q150 | 21 | input_ontology | "Figure 43: A High School Statistics example." |
| Q151 | 21 | input_content | "Figure 44: A High School US History example." |
| Q152 | 21 | input_ontology | "Figure 45: A High School World History example." |
| Q153 | 21 | input_ontology | "Figure 46: A Human Aging example." |
| Q154 | 22 | input_ontology | "Morning sickness is typically a problem: (A) during the first trimester (B) during the second trimester (C) during the third trimester (D) all through the pregnancy" |
| Q155 | 22 | input_ontology | "Would a reservation to the definition of torture in the ICCPR be acceptable in contemporary practice? (A) This is an acceptable reservation if the reserving country's legislation employs a different definition (B) This is an unacceptable reservation because it contravenes the object and purpose of the ICCPR (C) This is an unacceptable reservation because the definition of torture in the ICCPR is consistent with customary international law (D) This is an acceptable reservation because under general international law States have the right to enter reservations to treaties" |
| Q156 | 22 | input_ontology | "Which position does Rawls claim is the least likely to be adopted by the POP (people in the original position)? (A) The POP would choose equality above liberty. (B) The POP would opt for the 'maximin' strategy. (C) The POP would opt for the 'difference principle.' (D) The POP would reject the 'system of natural liberty.'" |
| Q157 | 22 | input_ontology | "John Stuart Mill: Each person's happiness is a good to that person, and the general happiness, therefore, a good to the aggregate of all persons. (A) Fallacy of Composition (B) Fallacy of Division (C) Gambler's Fallacy (D) Equivocation" |
| Q158 | 22 | input_ontology | "A 6-sided die is rolled 15 times and the results are: side 1 comes up 0 times; side 2: 1 time; side 3: 2 times; side 4: 3 times; side 5: 4 times; side 6: 5 times. Based on these results, what is the probability of side 3 coming up when using Add-1 Smoothing? (A) 2/15 (B) 1/7 (C) 3/16 (D) 1/5" |
| Q159 | 22 | input_ontology | "According to Lewin, Lippet and White's 1939 experiment, which form of leadership produced the most work from participants? (A) Laissez-faire (B) Democratic (C) Authoritarian (D) A mix of laissez-faire and democratic" |
| Q160 | 23 | input_form | "Figure 57: A Moral Scenarios example. The formatting of this task hinders UnifiedQA performance substantially." |
| Q161 | 24 | input_ontology | "According to Moore's "ideal utilitarianism," the right action is the one that brings about the greatest amount of: (A) pleasure. (B) happiness. (C) good. (D) virtue." |
| Q162 | 24 | input_ontology | "Researchers now believe that the decline of the Maya was caused chiefly by: (A) a cataclysm of some kind, such as an earthquake, volcano, or tsunami. (B) ecological degradation resulting from slash-and-burn farming techniques. (C) endless wars between neighboring Mayan city-states. (D) practices of interbreeding that led to a steep rise in congenital disorders." |
| Q163 | 24 | input_content | "Krete is an unmarried taxpayer with income exclusively from wages. By December 31, year 1, Krete's employer has withheld $16,000 in federal income taxes and Krete has made no estimated tax payments. On April 15, year 2, Krete timely filed for an extension request to file her individual tax return, and paid $300 of additional taxes. Krete's year 1 tax liability was $16,500 when she timely filed her return on April 30, year 2, and paid the remaining tax liability balance. What amount would be subject to the penalty for underpayment of estimated taxes? (A) $0 (B) $500 (C) $1,650 (D) $16,500" |
| Q164 | 24 | input_content | "The night before his bar examination, the examinee's next-door neighbor was having a party. The music from the neighbor's home was so loud that the examinee couldn't fall asleep. The examinee called the neighbor and asked her to please keep the noise down. The neighbor then abruptly hung up. Angered, the examinee went into his closet and got a gun. He went outside and fired a bullet through the neighbor's living room window. Not intending to shoot anyone, the examinee fired his gun at such an angle that the bullet would hit the ceiling. He merely wanted to cause some damage to the neighbor's home to relieve his angry rage. The bullet, however, ricocheted off the ceiling and struck a partygoer in the back, killing him. The jurisdiction makes it a misdemeanor to discharge a firearm in public. The examinee will most likely be found guilty for which of the following crimes in connection to the death of the partygoer? (A) Murder. (B) Involuntary manslaughter. (C) Voluntary manslaughter. (D) Discharge of a firearm in public." |
| Q165 | 25 | output_content | "Published as a conference paper at ICLR 2021" |
| Q166 | 25 | input_ontology | "Figure 63: A Professional Medicine example." |
| Q167 | 25 | input_ontology | "Figure 64: A Professional Psychology example." |
| Q168 | 25 | input_ontology | "Figure 65: A Public Relations example." |
| Q169 | 26 | input_ontology | "Figure 66: A Security Studies example." |
| Q170 | 26 | input_ontology | "Figure 67: A Sociology example." |
| Q171 | 26 | input_content | "Figure 68: A US Foreign Policy example." |
| Q172 | 26 | input_ontology | "Figure 69: A Virology example." |
| Q173 | 27 | input_ontology | "Figure 70: A World Religions example." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.tbsnews.net/foreign-policy/bangladeshi-indian-engineers-monitor-water-flows-under-ganges-water-sharing-treaty |
| WEB-2 | https://en.wikipedia.org/wiki/Teesta_Water_Dispute |
| WEB-3 | https://www.southasianfuturesfellowship.org/analysis-2/the-future-of-the-teesta-river-project-amidst-new-developments-in-bangladesh:-a-geopolitical-quagmire |
| WEB-4 | https://www.tbsnews.net/features/panorama/teesta-master-plan-and-longstanding-bangladesh-india-water-politics-1072696 |
| WEB-5 | https://arxiv.org/pdf/2507.23248 |
| WEB-6 | https://doi.org/10.1007/978-981-97-4152-6_38 |
| WEB-7 | https://www.observerbd.com/news/542998 |
| WEB-8 | https://en.prothomalo.com/bangladesh/c7axno0vhh |
| WEB-9 | https://testbook.com/question-answer/what-is-the-literacy-rate-of-telangana--5efeb788fbc9b00d102b5fda |
| WEB-10 | https://saarj.com/wp-content/uploads/paper/ACADEMICIA/2022/FULL-PDF/ACADEMICIA-AUGUST-2022/8.15,%20Khritish%20Swargiary.pdf |
| WEB-11 | https://www.census2011.co.in/census/state/andhra+pradesh.html |
| WEB-12 | https://www.findeasy.in/indian-states-by-literacy-rate/ |
| WEB-13 | https://datareportal.com/reports/digital-2024-bangladesh |
| WEB-14 | https://www.newagebd.net/post/telecom/252740/internet-penetration-rate-declines |
| WEB-15 | https://en.wikipedia.org/wiki/Internet_in_Bangladesh |
| WEB-16 | https://www.bssnews.net/news/180472 |
| WEB-17 | https://github.com/AI4Bharat/IndicBERT |
| WEB-18 | https://openreview.net/forum?id=vfT4YuzAYA |
| WEB-19 | https://indicnlp.ai4bharat.org/pages/indicnlp-resources/ |
| WEB-20 | https://www.pmfias.com/teesta-water-sharing-with-bangladesh/ |
| WEB-21 | https://www.waterdiplomat.org/story/2025/08/teesta-river-politics-and-benefit-sharing-getting-yes-without-grand-bargain |
| WEB-22 | https://ai4bharat.github.io/indicnlp_catalog/ |
| WEB-23 | https://arxiv.org/abs/2604.06227 |
| WEB-24 | https://ai-labs.olakrutrim.com/static/Bharatbench-report-4thfeb.pdf |
| WEB-25 | https://aclanthology.org/2023.acl-long.693 |
| WEB-26 | https://arxiv.org/html/2507.16974v2 |
| WEB-27 | https://www.socialsciencejournal.in/assets/archives/2025/vol11issue2/11026.pdf |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** cais/mmlu (57 subject configurations)
**Analysis date:** 2025-07-29
**Examples reviewed:** ~175 examples across 37 configs sampled (approximately 5 per config)
**Columns shown:** question, subject, choices, answer
**Columns skipped (media):** none (text-only dataset)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | cais/mmlu | moral_scenarios Ex1 | A | "For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, **according to ordinary moral standards in the US as of 2020**?" | Question explicitly frames moral standards as US-specific, 2020 vintage | OC |
| D2 | cais/mmlu | high_school_us_history Ex1 | A | "The song, and the movement that it was connected to, highlight which of the following developments in the broader society in the late 1800s?" (re: "The Hayseed", US Populist movement) | US-specific historical content with no South Asian relevance | IO, IC |
| D3 | cais/mmlu | high_school_government_and_politics Ex1 | A | "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" | Entirely US constitutional law content | IO, IC |
| D4 | cais/mmlu | high_school_government_and_politics Ex4 | D | "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president." | US-specific legislative history | IO |
| D5 | cais/mmlu | us_foreign_policy Ex4 | D | "In American government, the power to declare war rests with Congress." | US government structure; no relevance to South Asian governance or environmental policy | IO |
| D6 | cais/mmlu | us_foreign_policy Ex3 | C | "Why is NSC 68 seen as a turning point in US Cold War Foreign policy?" | US Cold War policy — no South Asian agro-ecological relevance | IO |
| D7 | cais/mmlu | professional_law Ex1 | A | "A truck driver was assigned to drive a huge tractor-trailer loaded with logs. The logs were being sold by a lumber company… the girl was struck by the tractor-trailer and was seriously injured." | US tort law scenario — US legal context | IO, IC |
| D8 | cais/mmlu | professional_law Ex2 | B | "An avid baseball fan learned that a local professional baseball club was conducting a baseball camp… forwarded the club a $50 registration deposit" | US contract law — US sports/cultural context | IC |
| D9 | cais/mmlu | human_aging Ex3 | C | "The age at which one can receive full benefits from social security" with answer "Has been increasing" | US Social Security system — entirely US institutional context | IC, OC |
| D10 | cais/mmlu | human_sexuality Ex1 | A | "Which of the following is the most common method of birth control for married couples in the **U.S.**" | Explicitly US demographic data | IC, OC |
| D11 | cais/mmlu | human_sexuality Ex5 | A | "From 1988 to 1990 among heterosexuals in the **US**, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women" | US-specific behavioral survey data | IC, OC |
| D12 | cais/mmlu | moral_scenarios Ex2–5 | B/C/D/A | "For which of these two scenarios does the main character … do something clearly morally wrong, according to ordinary moral standards in the US as of 2020?" (repeated framing across all 5 examples) | Every moral_scenarios question frames correctness relative to US 2020 norms | OC, OO |
| D13 | cais/mmlu | global_facts Ex2 | B | "As of 2017, what fraction of the population in **India** used the internet in the past three months? (A) 11% (B) 26% (C) 41% (D) 56%" | South Asia-referenced factual question, but static 2017 statistic | IC |
| D14 | cais/mmlu | global_facts Ex1 | A | "About what percentage of survey respondents from **China** report having paid a bribe in the last year to access public services … as of 2017?" | Global factual question but no South Asian agricultural content | IC |
| D15 | cais/mmlu | business_ethics Ex5 | A | "in many other countries, such as **Russia** and **China** civil society is far less developed than in, for instance, **Britain**" | Western-normative framing of civil society development | IC |
| D16 | cais/mmlu | high_school_european_history Ex1 | A | "The Scribbling-Machines have thrown thousands of your petitioners out of employ… Leeds Woolen Workers Petition, 1786" | Entirely European industrial history — no South Asian relevance | IO |
| D17 | cais/mmlu | high_school_european_history Ex2 | B | "What is tolerance?… Of all religions, the Christian ought doubtless to inspire the most tolerance… Voltaire, Letters on the English Nation, 1733" | European Enlightenment philosophy — no South Asian agricultural relevance | IO, IC |
| D18 | cais/mmlu | high_school_world_history Ex2 | B | "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters… British journalist William Howard Russell, My Indian Mutiny Diary, 1860" | British colonial framing of Indian history | IC, OC |
| D19 | cais/mmlu | high_school_geography Ex3 | C | "The way of life based on breeding and herding of animals that is used as a source of food, shelter, and clothing is called pastorialism" | Generic geography — no delta/wetland/aquaculture content | IO |
| D20 | cais/mmlu | high_school_geography Ex5 | A | "Which zone contains low-income slums, ethnic ghettos, and general deterioration in Burgess's concentric **zone model of urban form**?" | US urban planning model (Burgess model, Chicago School) | IC |
| D21 | cais/mmlu | nutrition Ex1–5 | various | "Which of the following inborn errors of metabolism gives rise to zinc deficiency?"; "What characteristic is not representative of a type IIb muscle fibre?" | Clinical/biochemical nutrition — no South Asian food system or crop nutrition content | IO |
| D22 | cais/mmlu | college_biology Ex1 | A | "In fungi, cell walls are reinforced by which of the following? (A) Chitin (B) Silica (C) Lignin (D) Collagen fibers" | General biology — not agricultural/agro-ecological | IO |
| D23 | cais/mmlu | high_school_biology Ex4 | D | "Which describes an African butterfly species that exists in two strikingly different color patterns?" | Biology question with African species reference — no South Asian agricultural relevance | IO |
| D24 | cais/mmlu | security_studies Ex1 | A | "In what ways do theories of conventional and critical social constructivism differ?" | Western IR theory — no South Asian environmental/agricultural policy content | IO |
| D25 | cais/mmlu | jurisprudence Ex1 | A | "Bill purchased a can of Sipep from the Ajax Minimart. After he finished drinking the Sipep, Bill noticed that the can contained dead insects stuck on the inside bottom of the can. In a strict product liability tort action against Ajax, Bill must prove…" | US-style product liability tort — US legal culture | IO, IC |
| D26 | cais/mmlu | sociology Ex3 | C | "Smith & Tomlinson argued that school character far outweighed ethnic background in determining educational success" | UK-centric sociological research | IC |
| D27 | cais/mmlu | international_law Ex4 | D | "Cultural relativism posits that local culture should validate the existence and practice of all human rights" | International law question — some nominal global relevance, but no South Asian agricultural law content | IO |
| D28 | cais/mmlu | high_school_macroeconomics Ex1–5 | various | "If firms that make a particular product expect its price will be lower in the future, this will cause the supply of the product to increase right now." | Generic macroeconomics — no South Asian agricultural market or agri-policy content | IO |
| D29 | cais/mmlu | elementary_mathematics Ex1 | A | "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel?" | US units (miles per hour) — not metric; minor cultural assumption | IC |
| D30 | cais/mmlu | high_school_statistics Ex1 | A | "The Department of Health plans to test the lead level in a specific park. Because a high lead level is harmful to children, the park will be closed if the lead level exceeds the allowed limit." | Environmental testing question, but no South Asian or agricultural context | IO |
| D31 | cais/mmlu | professional_medicine Ex2 | B | "A 31-year-old man with a 5-year history of HIV infection comes to the office because of anal pain… He says he and his partner engage in anal-receptive intercourse." | US clinical medicine scenario — Western clinical context | IC |
| D32 | cais/mmlu | college_chemistry Ex5 | A | "A substance that is NOT generally considered to be a toxic pollutant in water is (A) carbonic acid (B) a halogenated hydrocarbon (C) lead (D) mercury" | Closest approach to environmental science — but generic water chemistry, not delta/haor/saline intrusion relevant | IO |
| D33 | cais/mmlu | high_school_geography Ex1 | A | "What is the most rapidly growing religion in the United States today?" | US-centric cultural geography | IC |
| D34 | cais/mmlu | auxiliary_train Ex1 | B | "Jim watched a liquor store furtively for some time, planning to hold it up. He bought a realistic-looking toy gun for the job… On a charge of burglary, Jim's best defense would be that the liquor store was open to the public." | US criminal law scenario — US legal context, no South Asian relevance | IO, IC |
| D35 | cais/mmlu | miscellaneous Ex1 | A | "A flashing red traffic light signifies that a driver should do what? (A) stop" | US traffic law assumption (red = stop is near-universal but framed as US rule) | IC |
| D36 | cais/mmlu | world_religions Ex2 | B | "In Jainism, what is the cycle that one must liberate oneself from? (A) Punya (B) Samsara" | South Asian religion reference (Jainism) — one of very few South Asian cultural anchors in the dataset | IC |
| D37 | cais/mmlu | prehistory Ex2 | B | "The origins of Chinese civilization can be traced to: chiefdoms and states in numerous regions throughout China." | East Asian prehistory — no South Asian relevance | IO |
| D38 | cais/mmlu | high_school_world_history Ex4 | D | "Which of the following most inspired the national plan advanced by Nkrumah? … Socialism" | African postcolonial history — no South Asian agricultural relevance | IO |
| D39 | cais/mmlu | college_medicine Ex4 | D | "When preparing for the **MCAT exam**, a student begins studying electrochemical cells." | MCAT (US Medical College Admissions Test) reference — US academic system assumed | IC |
| D40 | cais/mmlu | global_facts Ex5 | A | "At the time of independence, there were already hundreds of thousands of university graduates in **India**, but hardly any at all in **Congo**." | India referenced but as a factual datapoint about independence-era education, not agro-ecological | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Universal STEM reasoning tasks provide a language-independent cross-model baseline
- **Dimension(s):** IO, OF
- **Observation:** A substantial portion of MMLU items test mathematical, logical, and physical reasoning that does not depend on cultural or geographic knowledge. Examples include abstract algebra (ring theory, group theory), college mathematics (optimization, real analysis), formal logic (predicate logic translation), and physics (electromagnetic, thermodynamic calculations). These items can serve as a culture-neutral baseline for comparing frontier vs. smaller regional models.
- **Deployment relevance:** The environmental scientist's stated goal includes cross-model comparison between frontier LLMs and smaller regional models. STEM reasoning items provide a stable substrate for this comparison even when domain-specific agricultural content is absent.
- **Datapoint citations:**
  - [D1 context] abstract_algebra Ex1 (cais/mmlu, split=test, label=A): "Find the characteristic of the ring Z_3 x 3Z." — Pure abstract mathematics with no cultural loading; valid cross-model comparison point.
  - [D1 context] college_mathematics Ex2 (cais/mmlu, split=test, label=B): "A total of x feet of fencing is to form three sides of a level rectangular yard. What is the maximum possible area of the yard, in terms of x?" — Geometry/optimization; culturally neutral.
  - [D1 context] college_physics Ex3 (cais/mmlu, split=test, label=C): "White light is normally incident on a puddle of water (index of refraction 1.33). A thin (500 nm) layer of oil (index of refraction 1.5) floats on the surface of the puddle. Of the following, the most strongly reflected wavelength is" — Physical optics; no cultural dependency.

#### Strength 2: Some globally-framed factual items reference South Asia tangentially
- **Dimension(s):** IC
- **Observation:** A small number of items in the `global_facts` and `prehistory` configs reference India or broader South Asia, providing a minimal foothold of non-exclusively-Western content. These are sparse but confirm MMLU is not entirely US-only in geographic reference.
- **Deployment relevance:** These items are too few and too shallow to support agricultural knowledge evaluation, but they confirm that some fraction of MMLU questions touch South Asian contexts — marginally relevant for baseline comparison.
- **Datapoint citations:**
  - [D13] global_facts Ex2 (cais/mmlu, split=test, label=B): "As of 2017, what fraction of the population in India used the internet in the past three months? (A) 11% (B) 26% (C) 41% (D) 56%." — India-referenced factual question; dated (2017) and not agricultural.
  - [D40] global_facts Ex5 (cais/mmlu, split=test, label=A): "At the time of independence, there were already hundreds of thousands of university graduates in India, but hardly any at all in Congo." — India referenced as a comparative datapoint.
  - [D36] world_religions Ex2 (cais/mmlu, split=test, label=B): "In Jainism, what is the cycle that one must liberate oneself from? (A) Punya (B) Samsara" — South Asian religious tradition (Jainism) represented; one of very few South Asian cultural anchors observed across all 175+ reviewed examples.

#### Strength 3: Statistical and scientific reasoning items are moderately transferable
- **Dimension(s):** IO, OF
- **Observation:** High_school_statistics and related items test general inferential reasoning (hypothesis testing, confidence intervals, Type I/II error, sampling) at a level that is conceptually relevant to environmental science methodology universally, including for South Asian researchers. These items test skills the environmental scientist would use regardless of regional context.
- **Deployment relevance:** An environmental scientist evaluating LLMs for agricultural applications would benefit from knowing whether a model understands statistical inference, even if the specific application domains differ.
- **Datapoint citations:**
  - [D30] high_school_statistics Ex1 (cais/mmlu, split=test, label=A): "The Department of Health plans to test the lead level in a specific park. Because a high lead level is harmful to children, the park will be closed if the lead level exceeds the allowed limit… Which of the following decisions would result from the type I error?" — Environmental monitoring framing of Type I error; the content domain is health/environment, though not South Asian specific.
  - [D1 context] high_school_statistics Ex2 (cais/mmlu, split=test, label=B): "In a high school of 1650 students, 132 have personal investments in the stock market. To estimate the total stock investment… Plan I would sample 30 students at random…" — Sampling methodology reasoning, transferable.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Zero subject coverage of South Asian agro-ecology, delta farming, or wetland ecology
- **Dimension(s):** IO
- **Observation:** Across all 57 subject configurations, not a single subject in the MMLU taxonomy addresses haor wetland ecology, boro/aman/aus rice cultivation, char-land agriculture, Brahmaputra-Jamuna floodplain systems, delta hydrology, dry-land Deccan cropping (Rabi/Kharif on black/red soils), coastal aquaculture in Andhra Pradesh, or any South Asian agro-ecological subdomain. The reviewed examples confirm this: the closest environmental content observed is generic water chemistry (D32) and a lead-level park test (D30), neither of which relates to South Asian farming systems. High_school_geography items reference Burgess's Chicago-school urban zone model (D20) and US religion demographics (D33), not Asian agricultural geography.
- **Deployment relevance:** This is a complete structural gap. The deployment's primary purpose — assessing LLM knowledge of South Asian agricultural and environmental science — finds zero targeted test items in MMLU's entire 57-subject taxonomy. The benchmark cannot measure what it does not test.
- **Datapoint citations:**
  - [D19] high_school_geography Ex3 (cais/mmlu, split=test, label=C): "The way of life based on breeding and herding of animals that are used as a source of food, shelter, and clothing is called pastorialism." — Most geographically relevant agriculture item observed; covers generic pastoral farming, not South Asian systems.
  - [D32] college_chemistry Ex5 (cais/mmlu, split=test, label=A): "A substance that is NOT generally considered to be a toxic pollutant in water is (A) carbonic acid (B) a halogenated hydrocarbon (C) lead (D) mercury." — Nearest environmental science content; generic water chemistry with no connection to saline intrusion, haor ecology, or delta hydrology.
  - [D22] college_biology Ex1 (cais/mmlu, split=test, label=A): "In fungi, cell walls are reinforced by which of the following? (A) Chitin (B) Silica (C) Lignin (D) Collagen fibers." — Exemplary of biology coverage: cellular/molecular, not agro-ecological.
  - [D21] nutrition Ex1 (cais/mmlu, split=test, label=A): "Which of the following inborn errors of metabolism gives rise to zinc deficiency? (A) Acrodermatitis enteropathica." — Nutrition content is clinical biochemistry, not crop nutrition or soil science.

#### Concern 2: English-only input format directly contradicts multilingual deployment requirement
- **Dimension(s):** IF
- **Observation:** Every single example reviewed across all 37 configs is in English only. The HF metadata explicitly tags the dataset as `monolingual` with `language: en`. The schema requires English-language question strings. The deployment requires Telugu, Bangladeshi Bengali (Mymensingh dialect), and Indian Bengali as query languages. There is no mechanism within MMLU's format to accept, process, or evaluate non-English input.
- **Deployment relevance:** The elicitation confirms queries will include Telugu and Bengali in both varieties — a direct and absolute format mismatch. No workaround within MMLU's design can address this.
- **Datapoint citations:**
  - [D2] high_school_us_history Ex1 (cais/mmlu, split=test, label=A): "The song, and the movement that it was connected to, highlight which of the following developments in the broader society in the late 1800s?" — Typical English-only question format; no provision for Bengali or Telugu input.
  - [D29] elementary_mathematics Ex1 (cais/mmlu, split=test, label=A): "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel?" — Even the most basic numeric reasoning items are framed entirely in English with US measurement units.

#### Concern 3: Moral scenarios explicitly anchor correctness in US 2020 norms — irreconcilable with South Asian OC validity
- **Dimension(s):** OC, OO
- **Observation:** The entire `moral_scenarios` config (500 test items) uses a fixed framing: "according to ordinary moral standards in the US as of 2020." This is not incidental phrasing — it is the operative definition of the correct answer for every question in this large subtask. Cultural divergence between Bangladeshi, Bangladeshi-Bengali, and US moral standards (e.g., around family hierarchy, religious obligation, land-use decisions) would produce legitimately different correct answers that this framing cannot accommodate.
- **Deployment relevance:** If the deployment includes any assessment of socially-situated reasoning — relevant for extension workers advising farmers on land use, water management, or community decisions — the US-anchored moral_scenarios labels would be actively misleading as a validity measure.
- **Datapoint citations:**
  - [D1] moral_scenarios Ex1 (cais/mmlu, split=test, label=A): "For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, **according to ordinary moral standards in the US as of 2020**? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot." — US normative framing is explicit and constitutive of the label.
  - [D12] moral_scenarios Ex2–5 (cais/mmlu, split=test): "For which of these two scenarios does the main character … do something clearly morally wrong, **according to ordinary moral standards in the US as of 2020**?" — The US normative anchor appears identically in all five reviewed moral_scenarios examples, confirming it is structural, not incidental.

#### Concern 4: Ground-truth labels for human_sexuality, human_aging carry US-specific factual claims as correct answers
- **Dimension(s):** OC, IC
- **Observation:** Several items frame US-specific empirical facts (US birth control statistics, US social security eligibility age, US behavioral survey data 1988–1990) as universally correct answers. A South Asian researcher or LLM optimized for South Asian contexts would reasonably disagree with or be penalized for correctly knowing that these facts differ regionally.
- **Deployment relevance:** While these specific tasks are peripheral to agricultural science, they illustrate a systematic pattern: MMLU's "correct" answers embed US institutional and demographic facts that have no transfer validity to South Asian contexts.
- **Datapoint citations:**
  - [D10] human_sexuality Ex1 (cais/mmlu, split=test, label=A): "Which of the following is the most common method of birth control for married couples in the **U.S.**: (A) Sterilization." — Correct answer is US-specific; would differ for Bangladesh or India.
  - [D11] human_sexuality Ex5 (cais/mmlu, split=test, label=A): "From 1988 to 1990 among heterosexuals in the **US**, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women." — US-specific survey finding from 35+ years ago, embedded as a correct answer.
  - [D9] human_aging Ex3 (cais/mmlu, split=test, label=C): "The age at which one can receive full benefits from social security: (A) Is 62 (B) Is 65 (C) Has been increasing (D) Will never change." — Answer presupposes the US Social Security system.

---

#### MAJOR

#### Concern 5: US legal, political, and historical content dominates multiple large subject categories
- **Dimension(s):** IO, IC
- **Observation:** Multiple high-item-count subjects (professional_law, high_school_us_history, high_school_government_and_politics, us_foreign_policy, jurisprudence) are predominantly or exclusively US-centric. The reviewed professional_law items all involve US tort, contract, and evidence law. High_school_government_and_politics items assume US constitutional structure (First Amendment, War Powers Act, Articles of Confederation). These subjects represent a substantial portion of MMLU's total item count.
- **Deployment relevance:** These subjects are irrelevant to the South Asian agricultural deployment. An LLM performing well on US law or US government questions provides no signal about its knowledge of Bangladesh water law, Indian agricultural extension policy, or Andhra Pradesh coastal aquaculture regulation.
- **Datapoint citations:**
  - [D3] high_school_government_and_politics Ex1 (cais/mmlu, split=test, label=A): "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment." — Entirely US-specific constitutional content.
  - [D4] high_school_government_and_politics Ex4 (cais/mmlu, split=test, label=D): "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president." — US legislative history; no cross-regional transfer.
  - [D7] professional_law Ex1 (cais/mmlu, split=test, label=A): "A truck driver was assigned to drive a huge tractor-trailer loaded with logs… the girl was struck by the tractor-trailer and was seriously injured. The girl's parents … assert a claim against the lumber company…" — US personal injury/tort law scenario.
  - [D5] us_foreign_policy Ex4 (cais/mmlu, split=test, label=D): "In American government, the power to declare war rests with Congress." — US constitutional structure.

#### Concern 6: World history and European history items frame non-Western events through colonial/Western lenses
- **Dimension(s):** IC, OC
- **Observation:** The `high_school_world_history` config includes South Asian content — specifically the 1857 Indian Uprising (Cawnpore/Kanpur massacres) — but presents it through a British colonial journalist's perspective as primary source, followed by a postcolonial historian's reframing. The correct answer (D18, label=B) is adjudicated by the benchmark. This framing of South Asian history through colonial sources, with labels set by a US academic team, represents a potential OC validity risk where Bangladeshi or Indian stakeholders may assess the "correct" answer differently.
- **Deployment relevance:** If any historical or geopolitical framing questions arise in the deployment context (e.g., framing of Bangladesh-India water disputes), this pattern of colonial-origin primary sources with US-adjudicated correctness is concerning.
- **Datapoint citations:**
  - [D18] high_school_world_history Ex2 (cais/mmlu, split=test, label=B): "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters… British journalist William Howard Russell, My Indian Mutiny Diary, 1860." — Indian history presented through British colonial journalism; label set by US academic team.

#### Concern 7: Global_facts items are temporally stale (2017–2019) for a South Asian deployment context
- **Dimension(s):** IC, OC
- **Observation:** The `global_facts` config contains questions about India and other countries anchored to 2017–2019 data (internet penetration, demographic statistics). For a South Asian deployment in 2025, these figures are significantly outdated. An LLM that correctly knows 2024 India internet penetration figures would be penalized for not knowing the 2017 benchmark answer.
- **Deployment relevance:** The Mymensingh scientist is evaluating LLMs for current-context agricultural and environmental knowledge. Benchmarking against 2017 data for South Asia-relevant questions produces systematically misleading signals about contemporary model knowledge.
- **Datapoint citations:**
  - [D13] global_facts Ex2 (cais/mmlu, split=test, label=B): "As of 2017, what fraction of the population in India used the internet in the past three months? (A) 11% (B) 26% (C) 41% (D) 56%." — The 2017 figure (26%) is the correct answer; a model knowing the 2025 figure (~55%) would be penalized.
  - [D14] global_facts Ex1 (cais/mmlu, split=test, label=A): "About what percentage of survey respondents from China report having paid a bribe in the last year to access public services … as of 2017?" — Year-anchored question; staleness applies across all global_facts items.

#### Concern 8: No annotator demographic information documented; US MTurk baseline is the only human reference
- **Dimension(s):** OC
- **Observation:** The HF card tags the dataset as `annotations_creators: no-annotation`, and the paper documents only a US MTurk baseline (34.5% accuracy). No South Asian domain experts, agronomists, or environmental scientists were involved in item creation or answer validation, based on all available documentation. The graduate/undergraduate students who collected items are entirely from US institutions.
- **Deployment relevance:** For any questions that could have regionally contingent correct answers (cross-border water policy, comparative agricultural practice), the labels carry no authority for the South Asian deployment context. The user explicitly confirmed this risk for Bangladesh–India water-sharing questions.
- **Datapoint citations:**
  - [D9] human_aging Ex3 (cais/mmlu, split=test, label=C): "The age at which one can receive full benefits from social security … Has been increasing." — Illustrates how US institutional facts are treated as universally correct without regional annotation review.
  - [D12] moral_scenarios, all five reviewed examples — US 2020 normative framing repeated across the entire config without any annotation for cross-cultural validity.

---

#### MINOR

#### Concern 9: US customary units in elementary mathematics assume US educational context
- **Dimension(s):** IC
- **Observation:** Elementary mathematics items use miles per hour (D29) rather than metric units. While this is a minor issue for mathematical reasoning evaluation, it introduces an unnecessary US-centric cultural assumption into what should be culturally neutral content.
- **Deployment relevance:** Minor; the mathematical reasoning being tested is metric-neutral, but the unit choice reflects the US educational sourcing of items.
- **Datapoint citations:**
  - [D29] elementary_mathematics Ex1 (cais/mmlu, split=test, label=A): "If a freight train travels at a speed of **20 miles per hour** for 6 hours, how far will it travel?" — US customary units in an otherwise neutral math problem.

#### Concern 10: College_medicine MCAT reference assumes US higher education system
- **Dimension(s):** IC
- **Observation:** A college_medicine item references the MCAT (US Medical College Admissions Test) as a natural reference point for a study scenario, embedding US higher education assumptions into what purports to be general medical knowledge.
- **Deployment relevance:** Minor; the actual content (elaborative rehearsal psychology) is not US-specific, but the MCAT framing signals the US academic origin of the item and would be unfamiliar to South Asian medical students.
- **Datapoint citations:**
  - [D39] college_medicine Ex4 (cais/mmlu, split=test, label=D): "When preparing for the **MCAT exam**, a student begins studying electrochemical cells… The student's process is best characterized as: (D) Elaborative rehearsal." — MCAT reference embeds US academic context in a psychology-of-learning question.

#### Concern 11: High_school_geography and sociology items carry Western-normative theoretical frameworks
- **Dimension(s):** IC
- **Observation:** Geography questions use Burgess's concentric zone model (Chicago, 1920s) as the reference urban geography theory; sociology questions use UK-origin research (Smith & Tomlinson, Bowlby, Chodorow) as authoritative references. These frameworks were developed in US/UK contexts and may not describe South Asian urban or social patterns.
- **Deployment relevance:** Minor for the primary agricultural deployment; more relevant if the deployment expands to social science evaluation.
- **Datapoint citations:**
  - [D20] high_school_geography Ex5 (cais/mmlu, split=test, label=A): "Which zone contains low-income slums, ethnic ghettos, and general deterioration in **Burgess's concentric zone model of urban form**?" — Chicago School urban theory presented as authoritative geography.
  - [D26] sociology Ex3 (cais/mmlu, split=test, label=C): "Smith & Tomlinson argued that **school character** far outweighed ethnic background in determining educational success." — UK-based educational sociology as the reference frame.

---

### Content Coverage Summary

The 175+ examples reviewed span all 37 sampled configurations and confirm the documented structure: MMLU is an English-only, US/Western-institution-anchored multiple-choice benchmark. The subject matter is dominated by US academic and professional preparation content — US law (professional_law, jurisprudence), US government (high_school_government_and_politics, us_foreign_policy), US history, Western European philosophy and history, and US clinical medicine. General STEM subjects (physics, mathematics, chemistry, computer science, biology) are culturally lighter but still framed through US/Anglophone university materials.

The dataset contains no items addressing boro/aman/aus rice cultivation cycles, haor or beel wetland ecology, char-land agriculture, Brahmaputra-Jamuna floodplain dynamics, Deccan dry-land Rabi/Kharif cropping, brackishwater shrimp aquaculture, or any Bengal/Telugu-specific agro-ecological subdomain. The closest environmental science content observed is generic water chemistry and a Type I error example set in a lead-level park-testing scenario. South Asia is referenced tangentially in two global_facts items (India internet statistics 2017; India vs. Congo university graduates at independence) and one world_religions item (Jainism/samsara). The 1857 Indian Uprising appears in world_history but is framed through British colonial primary sources.

The moral_scenarios config (500 items) explicitly anchors correctness in "ordinary moral standards in the US as of 2020" — a framing that is constitutive, not incidental, and that produces direct OC invalidity for South Asian deployment. Human_sexuality and human_aging items embed US-specific demographic facts as correct answers. The auxiliary_train split contains US bar-exam-style criminal and property law questions with no non-US legal content detected.

Register throughout is formal academic English, consistent with US standardized test preparation. No dialect variation, no Bengali or Telugu script, and no colloquial register is present in any reviewed example.

---

### Limitations

1. **Sample size per config:** Only 5–6 examples were reviewed per configuration. With 100+ items per test split, subject-level coverage patterns within each config cannot be fully characterized from the sample.

2. **Unreviewed configs:** Approximately 20 of the 57 configs were not directly sampled (e.g., formal_logic, prehistory, human_sexuality, and others were sampled but some configs such as prehistory were reviewed with fewer examples). Agricultural or South Asian-adjacent outlier items within those configs cannot be ruled out from the sample alone, though the taxonomy analysis makes their presence extremely unlikely.

3. **No Telugu or Bengali text to inspect:** Because MMLU is English-only, there is no non-English text to assess for dialect, script, or register quality. The language mismatch concern is absolute and visible at the metadata level, but its practical effect on specific model evaluation cannot be further characterized from dataset content alone.

4. **Temporal staleness of global_facts:** The global_facts items are dated (2017–2019); whether any items have been updated in the HuggingFace distribution cannot be confirmed from the sample.

5. **Auxiliary_train split:** The auxiliary_train split contains structured training data in a nested format (`train` column containing a dict). The full content scope of this split was sampled but only 5 examples inspected; it appears to contain US bar-exam-style law questions, but comprehensive characterization requires larger sampling.

6. **Cross-config agricultural content:** It is theoretically possible that a small number of items in the `miscellaneous` config (500 items) or `global_facts` config address South Asian agricultural topics not represented in the 5-example sample. The sample is insufficient to rule out rare outliers, though the documented sourcing from US standardized exams makes such items structurally improbable.

