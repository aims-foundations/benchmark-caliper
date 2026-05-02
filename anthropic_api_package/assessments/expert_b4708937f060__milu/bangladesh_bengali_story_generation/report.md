## Deployment Context

**Use case:** The focus is region-dependent generic llm adaptation.

Task: domain-dependent language and dialect understanding
LLMs evaluated: Generic frontier model vs small llms as well as region specific llms
Domain: General llm capability on region-dependent and context driven task understanding
Setting: Evaluating region-dependent llms to assess their capability on local-context tasks.
**Target population:** A native bengali speaker (a university student doing bsc thesis in story generation) from Dhaka, Bangladesh is using a regional llm to generate local context-driven stories. So it is important to have Bangladesh specific entity presence in the evaluation of the bengali part of the benchmark.

# Validity Analysis: milu
**Target context:** Bangladeshi Bengali University Student — Story Generation Thesis Deployment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ⚠ | 1 | Serious concern | high |
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

MILU is structurally misaligned with the Bangladeshi Bengali story generation deployment along five of six dimensions. Its ontology is India-first by explicit design [Q9, Q19] and excludes Bangladeshi national categories (1971 Liberation War, SSC/HSC, Bangladeshi universities, Ekushe Boi Mela, rural/riverine contexts). Empirical sampling confirms zero Bangladeshi cultural touchstones in 21 Bengali validation items [DATASET-D2-D7], 100% translation rate from English in the sampled Bengali validation split [DATASET-D8] (vs. 25% documented), and Bangladesh appearing only as a distractor option in non-Bengali splits [DATASET-D22, D23]. Ground-truth labels are validated entirely within Indian institutional frameworks [Q8, Q22, Q86] with no Bangladeshi annotators documented. Output form is closed MCQ accuracy [Q51], structurally incompatible with the deployment's open-ended story generation target. The only well-aligned dimension is input form (text in Bangla script [Q29, Q30, DATASET-D24]). High MILU Bengali scores would not predict — and could mislead — the deployment's intended evaluation construct.

## Practical Guidance

### What This Benchmark Measures

MILU measures multiple-choice factual recall on Indian competitive-exam content rendered in Indic scripts, including Bengali. For this deployment, MILU's strongest residual signal is on universal STEM and Bengali grammar/vocabulary items [DATASET-D17-D21, D24-D25] — i.e., baseline academic Bengali competence. It can serve as a screening filter to distinguish models with zero Bengali competence from those with some, but cannot measure Bangladeshi cultural grounding, register fidelity, or story-generation quality.

### Construct Depth

Shallow for the deployment's target construct. MILU probes one cell of a much larger evaluation space (closed-form factual recall on Indian content). The 'culturally relevant' framing in the documentation [Q1, Q19] refers to Indian culture; for Bangladeshi cultural grounding, MILU provides effectively no signal (input_ontology, input_content, output_ontology, output_content all scored 1). The output_form gap (MCQ vs. story generation) further means even strong MILU performance does not validate generative ability.

### What Else You Need

Substantial supplementation is required across input_ontology, input_content, output_ontology, output_content, and output_form. Recommended supplements: (1) BLUCK [WEB-15] and BnMMLU [WEB-18] for Bangladesh-sourced cultural and academic MCQ baselines; (2) BengaliMoralBench [WEB-8] and BanglaSocialBench [WEB-16] for Bangladeshi cultural and sociopragmatic context; (3) the Bengali Dialectal Bias Benchmark [WEB-1] for register/dialect coverage; (4) a purpose-built story-generation rubric authored and validated by native Bangladeshi annotators, modeled on BanglaSocialBench's native-speaker-written methodology, covering 1971 Liberation War, post-1971 political history through the 2024 July Uprising, Bangladeshi universities and exam systems, Bangladeshi geography (Dhaka neighborhoods, Padma/Meghna/Jamuna river systems, Cox's Bazar, Chittagong Hill Tracts), Islamic cultural register, and rural/riverine narrative contexts.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MILU's 8-domain, 41-subject taxonomy is explicitly structured around Indian academic and competitive examination content [Q1, Q17, Q19], with 'local knowledge' operationalized as Indian state-level [Q12]. The deployment requires Bangladesh-specific categories (1971 Liberation War, SSC/HSC exams, Bangladeshi universities, Ekushe Boi Mela, rural/riverine contexts) which have no designated position in the ontology. Empirical sampling confirms zero Bangladeshi cultural touchstones across 21 Bengali validation items [DATASET-D2, D3, D4, D5, D6, D7] and that Bangladesh appears only as a distractor option in non-Bengali splits [DATASET-D22, D23]. The authors themselves note models perform poorly in culturally relevant areas [Q6, Q68], precisely the domains where Bangladeshi knowledge should appear.

**Strengths:**
- Broad multi-domain coverage spans 8 domains including Arts & Humanities, Law & Governance, and STEM [Q1, Q17, DATASET-D2, D4], which means the structural slots exist even if filled with Indian content — a Bangladesh-targeted re-population of those slots is conceivable.
- Subject-level granularity (41 subjects) and language-stratified evaluation tables [Q99, Q128] provide a fine-grained reporting infrastructure that could in principle host Bangladesh-specific subjects.

**Checklist:**

- **IO-1**: Required Bangladesh-specific categories include the 1971 Liberation War, 1952 Language Movement, SSC/HSC exam content, Bangladeshi universities (Dhaka University, BUET, IUT, BRAC), Ekushe Boi Mela and Pohela Boishakh, post-1971 political history including the 2024 July Uprising, rural/riverine contexts, and Bangladeshi literary figures (Humayun Ahmed, Selim Al Deen) [WEB-3, WEB-5, WEB-7]. Story generation also requires categories for narrative settings (rural village life, river delta, Chittagong Hill Tracts, Dhaka neighborhoods) absent from competitive-exam ontology. — _Sources: WEB-3, WEB-5, WEB-7, WEB-15_
- **IO-2**: Yes — the taxonomy is structurally India-first [Q9, Q12, Q19] and excludes Bangladeshi national categories. Empirically confirmed: zero Bangladeshi cultural items in the 21-example Bengali validation sample [DATASET-D2 through D7]. — _Sources: Q9, Q12, Q19, DATASET-D2, DATASET-D6, DATASET-D22_
- **IO-3**: Yes — the taxonomy includes Indian-specific categories (Indian state elections, Indian constitutional law, Filmfare Awards, Indian freedom fighters, Indian state welfare schemes) [DATASET-D2, D3, D5, D9, D10, D11, D12] that are construct-irrelevant or actively misleading for a Bangladeshi cultural-grounding evaluation. — _Sources: DATASET-D2, DATASET-D3, DATASET-D5, DATASET-D9, DATASET-D11_
- **IO-4**: Major content-validity gap: the taxonomy under-represents Bangladeshi national knowledge and over-represents Indian state/national knowledge. Authors acknowledge poor model performance in culturally relevant areas [Q6, Q68] but attribute it to training data, not to the benchmark's own India-first ontology [Q9]. — _Sources: Q6, Q68, Q9_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge.' (p.1)
- [Q9] 'We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams.' (p.2)
- [Q12] 'We focus on region-specific exams to authentically capture local knowledge in the respective language.' (p.2)
- [Q17] 'MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge.' (p.3)
- [Q19] 'MILU is designed as a culturally relevant benchmark to assess general problem-solving abilities and India-specific knowledge.' (p.3)
- [Q68] 'open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance' (p.7)

*Web sources:*
- [WEB-3] SSC and HSC are the primary Bangladeshi national curriculum exams, entirely absent from MILU
- [WEB-5] July 2024 Uprising is a foundational live cultural reference for Bangladeshi students, post-benchmark
- [WEB-15] BLUCK (2025) demonstrates that a Bangladesh-sourced cultural-knowledge ontology is feasible and distinct from MILU

*Dataset analysis:*
- DATASET-D2: AAP Punjab election (2022) — India-specific governance in Bengali split
- DATASET-D5: 65th Filmfare Awards — Indian film industry, no Bangladeshi (Dhallywood) equivalent
- DATASET-D6: Qutub Minar, Delhi — Indian historical monument, no Bangladeshi sites (Lalbagh Fort, Paharpur) appear
- DATASET-D7: Bahamani Kingdom — medieval Indian history fills the History slot in Bengali
- DATASET-D22, D23: Bangladesh appears only as a distractor option in Odia/Telugu splits, never as a subject

</details>

**Information gaps:**
- Whether the larger Bengali test split (6,637 items) contains any organically-sourced Bengali-medium items with Bangladeshi-relevant content (validation sample shows 0%)

**Requires expert verification:**
- Native Bangladeshi review of any candidate Bengali items that survive translation-filter to confirm absence of Bangladeshi cultural anchoring

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
All MILU content was scraped from Indian competitive exam portals [Q11, Q21, Q88], spanning national civil service, government/private organization, and Indian state-level exams [Q93, Q96, Q97, Q98]. No Bangladeshi exam sources are mentioned. Empirical inspection confirms 100% of sampled Bengali validation items are GPT-4O translations from English [DATASET-D8] (vs. documented 25% [Q43]), and every culturally-specific Bengali item references Indian institutions, persons, or geography [DATASET-D1 through D7]. Identical questions appear verbatim across all 11 language splits [DATASET-D7 cross-config], confirming Bengali content is parallel translation of pan-Indian English exam content rather than Bengali-medium regional sourcing. The deployment's required Bangladeshi register (Cholti with Arabic/Persian loanword density) is not represented; the sampled vocabulary uses Tatsama Sanskritic forms characteristic of pan-Indian written Bengali [DATASET-D1, D25].

**Strengths:**
- STEM and universal academic content (chemistry, anatomy, computer science, mathematics) is culturally neutral and transfers validly to a Bangladeshi context [DATASET-D17, D18, D19, D20, D21], providing baseline signal on general academic Bengali competence.
- Bengali-language grammar and vocabulary items (antonyms, active/passive transformations) probe written Bengali competence directly [DATASET-D24, D25], offering some linguistic signal even if register-neutral.

**Checklist:**

- **IC-1**: Yes — the deployment requires Bangladeshi-specific cultural, geographic, and dialectal knowledge (Q1, Q2, Q3 elicitation responses; [WEB-3, WEB-5, WEB-8]). Bangladeshi Cholti register with Arabic/Persian loanwords is required and is distinct from West Bengali norms. — _Sources: WEB-3, WEB-5, WEB-8_
- **IC-2**: No — content reflects Indian national/state cultural framing exclusively [Q9, DATASET-D1 through D7]. The 1991 Indian financial crisis, Indian state elections, Indian constitutional law, Indian film awards, and Indian medieval/colonial monuments all populate the Bengali split. — _Sources: Q9, DATASET-D1, DATASET-D2, DATASET-D3, DATASET-D5, DATASET-D6, DATASET-D7_
- **IC-3**: Yes — items requiring Indian-specific knowledge (Indian Election Commissioner removal procedure, AAP state politics, Indian Pharmacopoeia, India's National Food Security Mission) [DATASET-D3, D2, D14] do not transfer and may produce false negatives for users with Bangladeshi civic knowledge. — _Sources: DATASET-D2, DATASET-D3, DATASET-D14_
- **IC-4**: No Bangladeshi annotators participated [Q8, Q86, Q87]; the documentation discloses only Indian institutional affiliation. The flagged_verification_priorities list confirms no Bangladeshi annotators are documented. — _Sources: Q8, Q86, Q87_
- **IC-5**: Severe content-validity violation: Bengali content is (a) translated from English in 100% of sampled items [DATASET-D8], (b) culturally India-centric [DATASET-D2-D7], (c) lacks any Bangladeshi register markers [DATASET-D1, D25]. Strong scores on this content do not predict performance on Bangladesh-grounded story generation. — _Sources: Q40, Q43, DATASET-D8, DATASET-D25_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams.' (p.2)
- [Q11] 'We create this benchmark by collecting questions from over 1500 competitive exams from India.' (p.2)
- [Q21] 'We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages.' (p.3)
- [Q40] 'For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O.' (p.4)
- [Q43] 'Of the total 79K questions, only 25% of questions are translated from English' (p.4)
- [Q84] 'the scarcity of questions necessitated translating a portion of the dataset.' (p.9)

*Web sources:*
- [WEB-3] SSC/HSC Bangladeshi national curriculum exams are the appropriate Bangladeshi exam-source equivalents, entirely absent from MILU
- [WEB-15] BLUCK demonstrates feasibility of Bangladesh-sourced exam content (BCS, university entrance, bar council)
- [WEB-18] BnMMLU sources directly from Bangladeshi NCTB textbooks — viable alternative content provenance

*Dataset analysis:*
- DATASET-D8: 100% of 21 sampled Bengali validation items are is_translated=True, vs. 25% documented benchmark average
- DATASET-D1: 1991 India balance-of-payments crisis question translated into Bengali — Indian-specific economic history
- DATASET-D2, D3, D5, D6, D7: Indian governance, film, monument, and medieval-history references populate culturally-specific Bengali items
- DATASET-D25: Bengali vocabulary uses Sanskrit-derived Tatsama forms ('নৃত্য পরিবেশনা') with no Bangladeshi Cholti register markers
- DATASET-D7 cross-config: Bahamani Kingdom question appears verbatim in Gujarati, Malayalam, Punjabi splits — confirming parallel translation rather than Bengali-medium sourcing

</details>

**Information gaps:**
- Whether the test split (6,637 Bengali items) has a different translation rate or contains organically-sourced Bengali-medium items with West-Bengali-specific (but not Bangladeshi) cultural content
- Systematic register classification of Bengali items by a Bangladeshi linguist

**Requires expert verification:**
- Native Bangladeshi linguistic audit of register markers across a larger Bengali sample
- Comparison of MILU Bengali content to BLUCK/BnMMLU Bangladeshi-sourced content for cultural-distance measurement

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
MILU is purely text-based MCQ in Indic scripts [Q29] with INDICLID + Unicode filtering for script correctness [Q30] and manual verification per language [Q32]. The deployment is also text-only in Bengali script [WEB-2]. Empirical inspection confirms Bengali items are correctly rendered in Bangla script with no encoding errors [DATASET-D24, D25]. No script-level mismatch exists. The remaining concerns (register/dialect stratification, translation-induced surface form) are content/lexical rather than form properties; the writing-system-level form alignment is strong. One residual concern is that 100% translation rate in the Bengali validation sample [DATASET-D8] may produce translation-flavored surface text that differs subtly from organically Bengali-written prose, but this is at the boundary of form vs. content.

**Strengths:**
- Bengali script (Bangla lipi) rendering is correct and well-formed throughout the sampled split [DATASET-D24, D25]; no script contamination from other Indic scripts observed.
- Documentation explicitly applies INDICLID and Unicode-based filtering to ensure script and language correctness [Q30], plus a final manual sample verification per language [Q32].
- Modality (text) matches the deployment's text-only requirement; no image/audio dependency [Q29].

**Checklist:**

- **IF-1**: Signal modality (written Bengali script) matches deployment [Q29, WEB-2, DATASET-D24]. No resolution/encoding mismatch — both are Unicode Bengali text. — _Sources: Q29, WEB-2, DATASET-D24_
- **IF-2**: Bangladeshi infrastructure supports Bengali text input/output; urban Dhaka university students have adequate connectivity and devices [WEB-9, WEB-10]. No infrastructure barrier to MILU's input form. — _Sources: WEB-9, WEB-10_
- **IF-3**: MILU excludes reading-comprehension and image-based questions for uniformity [Q29], which slightly narrows form coverage relative to general LLM use, but is acceptable for an MCQ knowledge benchmark. — _Sources: Q29_
- **IF-4**: Minor concern: cross-language parallel-translation patterns [DATASET-D7] may produce translationese surface forms in Bengali items, distinct from organically-written Bengali prose; this is a subtle form-quality issue rather than a structural mismatch. — _Sources: DATASET-D8, DATASET-D7_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q29] 'During the collection process, we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q30] 'we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering (Khan et al., 2024), ensuring that the questions are in the correct language.' (p.4)
- [Q32] 'we manually verify a sample of questions from each language to ensure accuracy and correct any remaining errors.' (p.4)

*Web sources:*
- [WEB-2] Bengali alphasyllabary tokenization challenges are documented; Sangraha corpus has ~30B Bengali tokens
- [WEB-9] Urban Dhaka connectivity supports text-based deployment

*Dataset analysis:*
- DATASET-D24: Bengali script correctly rendered in antonym question — no encoding errors
- DATASET-D25: Active/passive Bengali grammar transformation — well-formed Bengali prose
- DATASET-D8: 100% translated items in Bengali validation may produce translationese surface form

</details>

**Information gaps:**
- Whether translation-induced surface patterns systematically differ from organically-written Bangladeshi Bengali prose at a level that affects model evaluation

**Requires expert verification:**
- Native Bangladeshi reader assessment of whether translated Bengali surface form reads naturally

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MILU's output space is a discrete label among up to four MCQ options [Q29, Q51], with the 41-subject taxonomy serving as metadata for analysis [Q38]. The deployment targets open-ended Bengali story generation, where the output space is free-form narrative text — fundamentally incompatible with a closed MCQ label space [DATASET-D5 OF concern]. Furthermore, the correct-answer category encodings reflect Indian national/state factual standards — Indian Election Commissioner removal procedure, Indian state political wins, Indian Pharmacopoeia [DATASET-D2, D3, D14] — which encode non-Bangladeshi values and assumptions in the answer-key structure itself. The MCQ output ontology cannot be re-mapped to evaluate culturally grounded narrative generation, and within-Bengali items the answer correctness is calibrated to Indian rather than Bangladeshi knowledge frameworks. No mechanism distinguishes India-specific from Bangladesh-specific answer correctness.

**Strengths:**
- Structured 4-option categorical output is reproducible and unambiguously scorable [Q51], which provides a clean baseline for measuring factual recall on whatever knowledge frame is encoded — useful as a first-pass screen even if not for the deployment's primary task.

**Checklist:**

- **OO-1**: Output labels are India-calibrated correct answers [DATASET-D3 — Indian CEC removal procedure; DATASET-D2 — Indian state election winner]. For a Bangladeshi user, the 'correct' answer for governance items presupposes Indian constitutional structures, not Bangladeshi ones. — _Sources: Q51, DATASET-D3, DATASET-D2_
- **OO-2**: Missing: any output category encoding Bangladeshi-specific correct answers (e.g., Bangladesh's Election Commission structure, SSC/HSC curriculum standards, Bangladeshi historical events). No story-generation-relevant output categories exist at all. — _Sources: DATASET-D3, DATASET-D14_
- **OO-3**: Yes — categories encode Indian national values/assumptions: Indian-state-level governance correctness [DATASET-D2, D3], Indian historical canon [DATASET-D6, D7], Indian cultural figures [DATASET-D4, D5]. These violate convergent validity for a Bangladeshi-targeted evaluation. — _Sources: DATASET-D2, DATASET-D4, DATASET-D6, DATASET-D7_
- **OO-4**: Stakeholder-driven taxonomy redesign would be required: a story-generation rubric grounded in Bangladeshi cultural touchstones, register, and named entities is needed — MCQ accuracy cannot be re-purposed. BanglaSocialBench's native-speaker-written context-dependent methodology [WEB-16] is the closest existing model. — _Sources: WEB-16, WEB-15_
- **OO-5**: Severe structural and content validity violations: the output taxonomy is doubly misaligned (closed-form MCQ vs. open generation; Indian answer-keys vs. Bangladeshi correctness). — _Sources: Q29, Q38_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q29] 'During the collection process, we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency.' (p.4)
- [Q38] 'we determine 41 distinct subject names, which fall into eight main domains' (p.4)
- [Q51] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability' (p.5)

*Web sources:*
- [WEB-16] BanglaSocialBench native-speaker-written, context-dependent evaluation methodology is the closest precedent for a culturally-grounded output ontology
- [WEB-15] BLUCK uses Bangladesh-sourced MCQ ontology as a category-redesign reference

*Dataset analysis:*
- DATASET-D3: Indian Election Commissioner removal procedure as the 'correct' answer encodes Indian constitutional law as ground truth
- DATASET-D2: AAP Punjab election win as correct answer encodes Indian party-political knowledge
- DATASET-D14: India's National Food Security Mission as correct answer encodes Indian government program knowledge

</details>

**Information gaps:**
- Whether any items in the test split have answer keys that would also be correct under Bangladeshi knowledge frameworks (universal STEM items presumably yes; cultural/governance items presumably no)

**Requires expert verification:**
- Bangladeshi expert review of cultural/governance answer keys to identify items where Indian and Bangladeshi correct answers diverge

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Ground truth labels were validated by Indian exam portal subject experts [Q22] and audited by AI4Bharat volunteers [Q87]. The benchmark team is exclusively affiliated with Indian institutions — Nilekani Centre at AI4Bharat, IIT Madras, IBM Research India [Q8] — and funded by Indian philanthropies [Q86]. No Bangladeshi reviewers or subject-matter experts are mentioned anywhere. The elicitation explicitly designates Indian-only annotator pools (including West Bengali speakers) as 'explicitly insufficient' for this deployment. Empirically, the cultural/governance items in the Bengali split [DATASET-D2, D3, D4, D5, D6] have answer labels reflecting Indian standards, and no Bangladeshi institutional or individual validator is documented. For governance items like Election Commissioner removal [DATASET-D3], a Bangladeshi annotator would correctly identify the framing as Indian-specific. No formal IAA, annotator demographic profiles, or aggregation methodology disclosures are provided.

**Strengths:**
- Source exam portals provided subject-expert answer validation [Q22], establishing baseline label correctness within the Indian-exam knowledge frame.
- Manual cluster review and AI4Bharat volunteer audits [Q37, Q87] add a second pass of human verification, even if not Bangladeshi-grounded.
- Approximately 45% of items arrived with topic tags from source portals [Q33], reducing reliance on automated clustering for those items.

**Checklist:**

- **OC-1**: No — labels reflect Indian stakeholder perspectives only [Q8, Q22]. The elicitation requires native Bangladeshi Bengali speakers as primary ground truth and explicitly designates Indian-only pools as insufficient. — _Sources: Q8, Q22, Q86_
- **OC-2**: Significant disagreement is likely on cultural/governance items where Indian and Bangladeshi correct answers diverge structurally [DATASET-D3 — Indian-specific CEC removal procedure]. Universal STEM items would show low disagreement. — _Sources: DATASET-D3, DATASET-D2_
- **OC-3**: Documentation discloses Indian institutional affiliation (AI4Bharat, IIT Madras, IBM Research India [Q8]) and Indian funding [Q86], but provides no formal Datasheet, demographic breakdown, or inter-annotator agreement statistics. — _Sources: Q8, Q86, Q87_
- **OC-4**: Re-annotation by a representative Bangladeshi annotator pool would be required for any deployment-relevant use; existing labels cannot be assumed valid for Bangladesh-targeted evaluation. — _Sources: WEB-8, WEB-16_
- **OC-5**: No aggregation methodology disclosed; minority-perspective erasure cannot be assessed from documentation. INSUFFICIENT DOCUMENTATION on aggregation procedure.
- **OC-6**: Severe convergent and external validity violations: labels do not correlate with regional Bangladeshi perspectives on cultural and governance items, and Indian judgments will not generalize. — _Sources: Q8, DATASET-D3, DATASET-D14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q8] 'Sshubam Verma1 Mohammed Safi Ur Rahman Khan1,2 Vishwajeet Kumar3 Rudra Murthy3 Jaydeep Sen3 1Nilekani Centre at AI4Bharat 2Indian Institute of Technology, Madras 3IBM Research, India' (p.1)
- [Q22] 'These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers.' (p.3)
- [Q86] 'We would like to thank EkStep Foundation and Nilekani Philanthropies for their generous grant towards building datasets, models, tools and other resources for Indian languages.' (p.9)
- [Q87] 'volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits.' (p.9)

*Web sources:*
- [WEB-8] BengaliMoralBench's native Bangladeshi speaker consensus methodology is a model for the annotation approach this deployment requires
- [WEB-16] BanglaSocialBench's native-speaker-written evaluation methodology demonstrates that Bangladeshi annotator pools are feasible

*Dataset analysis:*
- DATASET-D3: Indian Election Commissioner removal procedure label requires Indian constitutional knowledge — Bangladeshi evaluator would identify framing mismatch
- DATASET-D2: AAP Punjab election label requires Indian party-political knowledge — irrelevant to Bangladeshi civic knowledge
- DATASET-D14: India's National Food Security Mission label — Bangladeshi user has no reason to know this Indian program

</details>

**Information gaps:**
- Inter-annotator agreement statistics (not disclosed)
- Annotator demographic breakdown beyond institutional affiliation (not disclosed)
- Aggregation methodology for resolving disagreements (not disclosed)

**Requires expert verification:**
- Bangladeshi annotator re-review of culturally/politically specific Bengali items to quantify the Indian-vs-Bangladeshi label divergence rate

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MILU evaluates models using accuracy on closed MCQ items via log-likelihood (non-API) or structured JSON parsing (API) [Q48, Q49, Q51, Q52, Q53]. The deployment requires evaluating open-ended Bengali story generation, which demands free-form text output assessed for narrative coherence, register appropriateness, cultural authenticity, and grounding in Bangladeshi named entities. No MILU mechanism produces a score that transfers to story generation evaluation [DATASET-D5 concern]. The authors themselves note log-likelihood may diverge from generation-based and CoT methods [Q85]. The output-form gap is structural: MCQ accuracy measures forced-choice factual recall, not generative cultural grounding. Even if MILU scores were perfectly calibrated to Bangladeshi knowledge (which they are not), they would still not validate story generation quality.

**Strengths:**
- MILU's evaluation infrastructure is well-documented and reproducible across 0/1/5-shot conditions, log-likelihood, and generative-JSON modes [Q46, Q48, Q53], spanning 42–45 models [Q44, Q75]. This breadth means baseline factual-recall comparisons across models are feasible as a screening step.
- Both base and instruct variants are evaluated [Q45], and per-subject/per-language tables are provided [Q99, Q128], enabling fine-grained baseline comparisons within MILU's intended construct.

**Checklist:**

- **OF-1**: No — MILU produces single discrete labels (option1–4) or structured JSON [Q51, Q53]; the deployment requires open-ended free-form Bengali narrative text. Output modalities do not match. — _Sources: Q51, Q53, DATASET-D1_
- **OF-2**: Not applicable — deployment is text-only; no TTS requirement. INSUFFICIENT DOCUMENTATION on whether MILU's evaluation infrastructure could be extended to speech, but this is not a deployment requirement.
- **OF-3**: Target population is highly literate (university students [WEB-3]); literacy is not a barrier for either MILU's or the deployment's text format. — _Sources: WEB-3_
- **OF-4**: Severe external-validity violation: MCQ accuracy on India-centric content does not predict Bangladeshi story-generation quality. The deployment must construct a separate generative evaluation rubric (per BanglaSocialBench precedent [WEB-16]). — _Sources: Q85, WEB-16, DATASET-D1, DATASET-D19_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q48] 'For non-API-based models, we use the LM-EVALUATION-HARNESS (Gao et al., 2024; Biderman et al., 2024) to ensure clean and reproducible evaluations.' (p.5)
- [Q51] 'For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability' (p.5)
- [Q52] 'The API-based models are evaluated using the generative approach due to the lack of support for prompt log probabilities.' (p.5)
- [Q53] 'We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing.' (p.5)
- [Q85] 'our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting.' (p.9)

*Web sources:*
- [WEB-16] BanglaSocialBench's native-speaker-written, context-dependent evaluation methodology is the closest precedent for a story-generation rubric
- [WEB-3] University student literacy supports text-based deployment

*Dataset analysis:*
- DATASET-D1: MCQ correct-answer scoring produces binary pass/fail and yields no information about whether a model can narratively describe economic history in Bangladeshi Bengali
- DATASET-D19: Universal medical MCQ — correct answer does not predict ability to weave medical detail into a culturally authentic Bangladeshi story

</details>

**Information gaps:**
- No story-generation evaluation methodology exists in MILU; supplementation is structural, not incremental

**Requires expert verification:**
- Design and validation of a Bangladeshi story-generation rubric by native-speaker linguists and literary scholars

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Taxonomy lacks Bangladeshi-specific categories (1971 Liberation War, SSC/HSC, Bangladeshi universities, cultural events, rural/riverine contexts, 2024 July Uprising)

**Recommendation:** Supplement with BLUCK (Bangladesh-sourced cultural/historical MCQ across 23 categories [WEB-15]) and BnMMLU (Bangladeshi NCTB-textbook-sourced MMLU [WEB-18]) to populate the missing ontology slots; do not rely on MILU's Bengali split for cultural-knowledge claims.

### Input Content ⚠

**Gap:** 100% of sampled Bengali validation items are GPT-4O translations from English Indian-exam content [DATASET-D8]; no Bangladeshi register markers; no Bangladeshi named entities

**Recommendation:** Source supplementary content from Bangladesh-origin exams (BCS, SSC, HSC, university entrance) per BLUCK/BnMMLU methodology; for the thesis, document explicitly that MILU Bengali scores reflect translated pan-Indian content and report MILU only as a baseline-screening signal alongside Bangladesh-sourced benchmarks.

### Input Content ⚠

**Gap:** Bangladeshi Cholti register (Arabic/Persian loanword density) is absent from the sampled translated Bengali content [DATASET-D1, D25]; West-Bengali/pan-Indian Sanskritic register dominates

**Recommendation:** Supplement with the Bengali Dialectal Bias Benchmark [WEB-1] for explicit dialect coverage (including Barishal, Chittagong, Sylhet, Rangpur, Noakhali); commission a register-stratified sample of story-generation prompts that probes Bangladeshi Cholti vs. West-Bengali outputs.

### Output Ontology ⚠

**Gap:** Closed MCQ output space cannot evaluate open-ended story generation; correct-answer categories encode Indian rather than Bangladeshi knowledge

**Recommendation:** Construct a story-generation rubric with native Bangladeshi linguists and literary scholars, modeled on BanglaSocialBench's native-speaker-written context-dependent methodology [WEB-16], covering cultural authenticity, register fidelity, named-entity grounding, and narrative coherence.

### Output Content ⚠

**Gap:** Ground-truth labels validated only by Indian institutional reviewers [Q8, Q22, Q86]; no Bangladeshi annotators; elicitation declares Indian-only pools 'explicitly insufficient'

**Recommendation:** Recruit a panel of native Bangladeshi Bengali annotators (university-educated, cross-regional including Dhaka, Sylhet, Chittagong, Barisal) to (a) re-validate any MILU Bengali items used in the thesis, and (b) author ground truth for the new story-generation rubric. Disclose annotator demographics and inter-annotator agreement in the thesis.

### Output Form ⚠

**Gap:** MCQ accuracy via log-likelihood [Q51] does not transfer to evaluating open-ended Bengali narrative generation

**Recommendation:** Adopt a generation-based evaluation protocol (per the limitation noted in [Q85]) with multi-criteria human scoring (cultural authenticity, register, named-entity accuracy, narrative coherence) plus optional LLM-as-judge calibration validated against Bangladeshi annotator scores. Treat MILU accuracy purely as an upstream screening signal.

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
| Q8 | 1 | output_content | "Sshubam Verma1 Mohammed Safi Ur Rahman Khan1,2 Vishwajeet Kumar3 Rudra Murthy3 Jaydeep Sen3 1Nilekani Centre at AI4Bharat 2Indian Institute of Technology, Madras 3IBM Research, India" |
| Q9 | 2 | input_content | "We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams." |
| Q10 | 2 | output_ontology | "These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science." |
| Q11 | 2 | input_content | "We create this benchmark by collecting questions from over 1500 competitive exams from India." |
| Q12 | 2 | input_content | "We focus on region-specific exams to authentically capture local knowledge in the respective language." |
| Q13 | 2 | output_form | "We evaluate 45 different LLMs - a mix of closed proprietary, open-source, and language-specific models- on MILU." |
| Q14 | 2 | output_form | "Our findings suggest that models struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q15 | 2 | output_form | "Our analysis of in-context learning reveals that adding more examples improves performance in base models, but the effect on instruct models remains inconclusive." |
| Q16 | 2 | input_ontology | "Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM." |
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
| Q33 | 4 | output_content | "Upon examination, we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information." |
| Q34 | 4 | input_form | "To address this issue, we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question." |
| Q35 | 4 | output_ontology | "Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap." |
| Q36 | 4 | output_ontology | "To organize them, we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters." |
| Q37 | 4 | output_content | "We manually review these clusters and assign appropriate subject labels." |
| Q38 | 4 | output_ontology | "Following the manual merging of related clusters, we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies." |
| Q39 | 4 | input_content | "Finally, we observed that some topics in certain languages had less than 100 questions. To ensure thorough evaluation across all subjects and languages, we aimed to have at least 100 questions per subject in each language." |
| Q40 | 4 | input_content | "For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O." |
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
| Q57 | 6 | input_content | "These models are primarily built by adapting English LLMs, such as LLAMA-2-7B, by first continually pretraining on small amount Indic language data, followed by optionally instruction finetuning them." |
| Q58 | 6 | output_form | "As seen from Table 4, across languages, the models exhibit average performance comparable to random baselines, with minimal variations among them." |
| Q59 | 6 | input_ontology | "When analyzed across domains, the models generally perform worse in Arts, Humanities, and Social Sciences than in STEM subjects." |
| Q60 | 6 | output_form | "We compare the performance of different Base and Instruct models across zero, one, and five-shot setups." |
| Q61 | 6 | output_form | "As shown in Figure 3, the performance of base models consistently improves with an increasing number of in-context examples, with the 5-shot setup yielding the best results." |
| Q62 | 6 | output_form | "In contrast, Instruct models exhibit more varied behavior, where models either stagnate or even degrade in performance." |
| Q63 | 6 | output_form | "This also aligns with expectations, as Instruct models are specifically fine-tuned as conversation assistants and may not respond well to the few-shot in-context examples format." |
| Q64 | 7 | output_form | "We evaluate the LLAMA and GEMMA family of models, ranging from 1B to 405B parameters, to analyze how performance scales with model size." |
| Q65 | 7 | output_form | "Figure 5 shows that the model performance improves significantly with increasing scale." |
| Q66 | 7 | output_form | "Notably, instruction-tuned models in the LLAMA family show more substantial improvements as compared to those in the GEMMA family." |
| Q67 | 7 | output_form | "We analyze the performance of various base and instruct models across multiple domains and languages." |
| Q68 | 7 | input_ontology | "Similar trends to those in Section (§5.2) are observed where the open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields." |
| Q69 | 7 | input_content | "This suggests that the training corpora for these models lack sufficient culturally specific data." |
| Q70 | 7 | input_content | "Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages." |
| Q71 | 7 | output_form | "As most Indic LLMs are built on English base models like LLAMA-2-7B, we assess the impact of language adaptation on their performance." |
| Q72 | 7 | output_form | "Table 5 compares language-specific models with the original LLAMA-2-7B, and instruction-tuned models with LLAMA-2-7B-CHAT." |
| Q73 | 7 | output_form | "Our findings show minimal gains, with some models even underperforming post-adaptation." |
| Q74 | 8 | input_ontology | "In this paper, we introduced MILU—Multilingual Indic Language Understanding Benchmark-a comprehensive benchmark specifically designed to evaluate LLMs across 11 Indic languages, spanning diverse domains and culturally relevant subjects." |
| Q75 | 8 | output_form | "We evaluate 45 different LLMs and find that the majority of LLMs struggle on MILU, with GPT4o achieving the highest average accuracy." |
| Q76 | 8 | input_ontology | "The analysis also shows that models perform significantly better in high-resource languages than low-resource ones, highlighting the need for more robust multilingual strategies." |
| Q77 | 8 | input_ontology | "Additionally, the domain-specific analysis indicates that models perform better in general fields such as STEM while facing challenges in culturally relevant subjects like Arts, Humanities, and Law, highlighting the lack of this knowledge in the current models and datasets." |
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
| WEB-1 | https://arxiv.org/abs/2603.21359 |
| WEB-2 | https://arxiv.org/abs/2507.23248 |
| WEB-3 | https://en.wikipedia.org/wiki/Education_in_Bangladesh |
| WEB-4 | https://www.dhakatribune.com/bangladesh/education/319301/bbs-functional-literacy-rate-7-above-years-in |
| WEB-5 | https://en.wikipedia.org/wiki/July_Revolution_(Bangladesh) |
| WEB-6 | https://www.euaa.europa.eu/news-events/bangladesh-situation-update-one-year-after-students-protests |
| WEB-7 | https://www.chathamhouse.org/2025/11/sheikh-hasina-verdict-and-bangladeshs-upcoming-referendum-signal-transitional-moment-south |
| WEB-8 | https://arxiv.org/abs/2511.03180 |
| WEB-9 | https://datareportal.com/reports/digital-2024-bangladesh |
| WEB-10 | https://www.tbsnews.net/bangladesh/over-50-households-use-internet-bangladesh-bbs-1032411 |
| WEB-11 | https://en.prothomalo.com/bangladesh/7ifddqcbtf |
| WEB-12 | https://www.tbsnews.net/bangladesh/internet-users-bangladesh-reach-131-million-2023-791442 |
| WEB-13 | https://ngital.com/bangladesh-internet-penetration-2025-data-insights/ |
| WEB-14 | https://arxiv.org/abs/2502.11187 |
| WEB-15 | https://arxiv.org/abs/2505.21092 |
| WEB-16 | https://arxiv.org/abs/2603.15949 |
| WEB-17 | https://aclanthology.org/2025.banglalp-1.14/ |
| WEB-18 | https://arxiv.org/abs/2505.18951 |
| WEB-19 | https://arxiv.org/abs/2503.10995 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Bengali config, with cross-config inspection of English, Hindi, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu)
**Analysis date:** 2025-01-31
**Examples reviewed:** 215 total (21 Bengali validation, 20 English validation, 24 Gujarati, 26 Hindi, 17 Kannada, 16 Malayalam, 21 Marathi, 21 Odia, 25 Punjabi, 19 Tamil, 25 Telugu)
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Bengali validation | Ex. 1 | option3 | "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল? … তেল ও পেট্রোলিয়াম পণ্যের আমদানির মূল্যের তীব্র বৃদ্ধি" | India's 1991 balance-of-payments crisis question, translated from English (is_translated=True) | IC, OC |
| D2 | Bengali validation | Ex. 5 | option4 | "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" | Indian state assembly election (AAP in Punjab, 2022) — exclusively India-centric governance content | IC, IO |
| D3 | Bengali validation | Ex. 9 | option3 | "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" | Removal of India's Election Commissioner — refers to Indian constitutional provisions | IC, OC |
| D4 | Bengali validation | Ex. 12 | option4 | "'মঙ্গল ভারত' কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল … আচার্য বিনোবা ভাবে" | "Mangal Bharat" — Indian national leader Vinoba Bhave; India-specific cultural/literary content | IC |
| D5 | Bengali validation | Ex. 17 | option2 | "৬৫তম ফিল্মফেয়ার অ্যাওয়ার্ডস, ২০২০-এ সেরা সিনেমাটোগ্রাফির জন্য পুরস্কারটি কে জিতেছেন? … জয় ওজা" | 65th Filmfare Awards (Indian film industry awards) — not Bangladeshi film industry | IC, IO |
| D6 | Bengali validation | Ex. 18 | option4 | "_______ দিল্লিতে কুতুব মিনারের নির্মাণ সম্পন্ন করেছিলেন … ইলতুতমিশ" | Qutub Minar, Delhi — India-specific historical monument | IC |
| D7 | Bengali validation | Ex. 3 | option4 | "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল? … গুলবার্গা" | Bahamani Kingdom capital — medieval Indian/Deccan history, not Bangladeshi | IC |
| D8 | Bengali validation | all 21 | various | All 21 Bengali examples show is_translated: True | Every Bengali validation example in sample is translated from English | IC, IF |
| D9 | English validation | Ex. 2 | option3 | "Which state has topped the India Innovation Index - 2019 published by Niti Aayog? … Karnataka" | India Innovation Index — Indian national governance content | IC |
| D10 | English validation | Ex. 9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" | Maharashtra state legislature — India-specific governance at state level | IC |
| D11 | English validation | Ex. 13 | option4 | "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? … Telangana" | Telangana state welfare scheme — Indian state government | IC |
| D12 | English validation | Ex. 15 | option3 | "Founded in 1950, one of the industrial units owned by Indian Railways is named after the Indian freedom fighter … Chittaranjan Das" | Indian Railways industrial unit named after Indian independence figure | IC |
| D13 | Bengali validation | Ex. 2 | option3 | "একটি ক্রিকেট প্রশিক্ষণ শিবিরে ১২০০ জন শিশু প্রশিক্ষণ নিচ্ছে যার মধ্যে ৯০০ জন নির্বাচিত হয়েছে। নির্বাচিত না হওয়া শিশুদের সংখ্যা এবং মোট শিশুদের সংখ্যার অনুপাত কত? … ১ : ৪" | Cricket training camp ratio problem — culturally neutral arithmetic, cricket context | IC |
| D14 | Bengali validation | Ex. 7 | option4 | "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প … জাতীয় খাদ্য সুরক্ষা মিশন আগস্ট ২০০৭ সালে চালু হয়েছিল" | India's National Food Security Mission — Indian government program | IC |
| D15 | Hindi validation | Ex. 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? … 44वें संविधान संशोधन अधिनियम द्वारा" | Indian constitutional amendment — India-specific law and governance | IC |
| D16 | Gujarati validation | Ex. 8 | option3 | "રેડક્લિફ રેખા નીચેના પૈકી કયા દેશ સાથે ભારતની સરહદોને અલગ કરે છે? … પાકિસ્તાન" | Radcliffe Line separating India and Pakistan — Indian national geography/history | IC |
| D17 | Bengali validation | Ex. 4 | option2 | "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। … শেল" | Constant current transformer type question — domain-neutral engineering/STEM | IC |
| D18 | Bengali validation | Ex. 8 | option4 | "নিম্নলিখিত কোনগুলি অক্সিডেশন-রিডাকশন বিক্রিয়া? … উপরের সবগুলি" | Oxidation-reduction reactions — universal science content | IC |
| D19 | Bengali validation | Ex. 10 | option4 | "হৃদয়ের পেসমেকার দ্বারা চিহ্নিত হয়, … এসএ নোড" | SA node as cardiac pacemaker — universal medical content | IC |
| D20 | Bengali validation | Ex. 14 | option3 | "একটি অ্যাসেম্বলার যা একটি মেশিনে চলে কিন্তু অন্য মেশিনের জন্য মেশিন কোড তৈরি করে তাকে কি বলা হয়? … ক্রস-অ্যাসেম্বলার" | Cross-assembler definition — universal computer science | IC |
| D21 | Bengali validation | Ex. 16 | option1 | "দুটি পাত্র আছে X এবং Y। X-এ ১০০ মিলি দুধ … m = n" | Milk-water mixture ratio problem — culturally neutral quantitative reasoning | IC |
| D22 | Odia validation | Ex. 2 | option4 | "ডিসেমবর 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆ… ବାଙ୍ଗ୍ଲାଦେଶ" | Indian Pharmacopoeia — Bangladesh mentioned as a distractor option, not as subject matter | IO |
| D23 | Telugu validation | Ex. 2 | option4 | "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది? … ఆఫ్ఘనిస్తాన్" | India Pharmacopoeia question — Bangladesh listed as distractor option2 | IO |
| D24 | Bengali validation | Ex. 6 | option2 | "নিচের প্রশ্নে, দেওয়া চারটি বিকল্পের মধ্যে থেকে সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে। … শীতল" | Antonym question in Bengali — vocabulary test | IF |
| D25 | Bengali validation | Ex. 13 | option2 | "নিচের বাক্যটির সঠিক সক্রিয় রূপ নির্বাচন করুন। সবাই তার চমৎকার নৃত্য পরিবেশনা দ্বারা মুগ্ধ হয়েছিল। … তার চমৎকার নৃত্য পরিবেশনা সবাইকে মুগ্ধ করেছিল।" | Active voice conversion of Bengali sentence — grammar in written Bengali | IF |
| D26 | Marathi validation | Ex. 16 | option3 | "হলষষ্ঠী সণ কা সাজরা কেলা জাতো? … মুলাচ্যা দীর্ঘায়ুষ্যাসাঠী" | Halshashthi festival (Maharashtra/Hindu calendar) — India-specific cultural festival, not Bangladeshi | IC |
| D27 | Bengali validation | Ex. 11 | option3 | "সিদ্ধান্ত গ্রহণের সাথে যুক্ত সমস্যাগুলি হল: … ভয় এবং মিথ্যা আশা" | Decision-making problems — generic management/psychology content | IC |
| D28 | Bengali validation | Ex. 19 | option1 | "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে … শুধুমাত্র যুক্তি I শক্তিশালী" | Logical argument strength question — generic reasoning | IC |
| D29 | Bengali validation | Ex. 20 | option2 | "জে, কে, এল, এম এবং এন পাঁচজন কাজিন … এম" | Age ordering puzzle with letter-named cousins — culturally neutral logic | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Bengali script is correctly used throughout the Bengali split
- **Dimension(s):** IF
- **Observation:** All 21 Bengali validation examples are rendered in Bangla script with correct Unicode rendering. The questions, options, and answers appear well-formed in Bengali script without visible encoding errors or script contamination from other Indic scripts.
- **Deployment relevance:** The target deployment uses Bangladeshi Bengali in Bangla script. No script mismatch exists at the writing-system level, satisfying the most basic input form requirement for a text-only Bengali evaluation.
- **Datapoint citations:**
  - [D24] Example 6 (Bengali, validation, option2): "নিচের প্রশ্নে, দেওয়া চারটি বিকল্পের মধ্যে থেকে সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে। … শীতল" — Bengali script is correctly rendered; antonym question shows standard written Bengali vocabulary
  - [D25] Example 13 (Bengali, validation, option2): "তার চমৎকার নৃত্য পরিবেশনা সবাইকে মুগ্ধ করেছিল।" — Active voice grammar question shows well-formed Bengali prose sentences

#### Strength 2: Multi-domain coverage including Arts & Humanities, Law & Governance, Science, and Business Studies
- **Dimension(s):** IO
- **Observation:** The sampled Bengali examples span Engineering (Ex. 4, 15, 16, 21), Science (Ex. 8), Health & Medicine (Ex. 10), Business Studies (Ex. 1, 11, 19), Arts & Humanities (Ex. 3, 6, 12, 13, 17, 18), Environmental Sciences (Ex. 7), Social Sciences (Ex. 2, 20), and Law & Governance (Ex. 5, 9). The domain coverage is broad across the 8 MILU domains.
- **Deployment relevance:** The deployment's evaluation of LLMs on cultural knowledge benefits from having multiple non-STEM domains present (Arts & Humanities, Law & Governance) even if their content is India-centric. This enables at least baseline measurement of model cultural knowledge capacity in Bengali, distinguishing models that have zero cultural awareness from those with some.
- **Datapoint citations:**
  - [D2] Example 5 (Bengali, validation, option4): "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" — domain=Law & Governance; confirms that political/governance content exists in Bengali, though content is India-specific
  - [D4] Example 12 (Bengali, validation, option4): "'মঙ্গল ভারত' কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল … আচার্য বিনোবা ভাবে" — domain=Arts & Humanities, subject=Literature and Linguistics; confirms literary content present in Bengali, though referencing Indian figures

#### Strength 3: STEM and universal academic content is present and transferable
- **Dimension(s):** IC
- **Observation:** A substantial portion of Bengali items covers domain-universal content — electrical engineering, chemistry, computer science, biology, mathematics — where the factual answer is culturally neutral and not India-specific. Questions about oxidation-reduction reactions, cardiac pacemakers, cross-assemblers, and mixture ratios have identical correct answers regardless of whether the evaluatee is Indian or Bangladeshi.
- **Deployment relevance:** For a deployment evaluating whether an LLM has general academic competence in Bengali, these universal STEM items provide valid signal. A model that cannot answer basic physics or chemistry questions in Bengali is unlikely to generate high-quality Bengali stories involving these topics either. While not the primary gap area, this represents a genuinely transferable subset.
- **Datapoint citations:**
  - [D18] Example 8 (Bengali, validation, option4): "নিম্নলিখিত কোনগুলি অক্সিডেশন-রিডাকশন বিক্রিয়া? … উপরের সবগুলি" — universal chemistry content; answer identical regardless of national context
  - [D19] Example 10 (Bengali, validation, option4): "হৃদয়ের পেসমেকার দ্বারা চিহ্নিত হয়, … এসএ নোড" — universal medical anatomy; no cultural specificity
  - [D20] Example 14 (Bengali, validation, option3): "একটি অ্যাসেম্বলার যা একটি মেশিনে চলে কিন্তু অন্য মেশিনের জন্য মেশিন কোড তৈরি করে তাকে কি বলা হয়? … ক্রস-অ্যাসেম্বলার" — universal computer science definition
  - [D21] Example 16 (Bengali, validation, option1): "দুটি পাত্র আছে X এবং Y। X-এ ১০০ মিলি দুধ … m = n" — culturally neutral quantitative reasoning

#### Strength 4: Bengali language grammar and vocabulary items present
- **Dimension(s):** IF, IC
- **Observation:** Examples 6 and 13 in the Bengali validation split test Bengali language competence directly — an antonym question and an active/passive voice transformation. These items probe written Bengali language knowledge at the lexical and syntactic level.
- **Deployment relevance:** Story generation quality depends partly on grammatical Bengali competence. These items provide at least some signal about whether a model can manipulate Bengali grammatical structures, even if the specific vocabulary tested may reflect written standard Bengali without dialect stratification.
- **Datapoint citations:**
  - [D24] Example 6 (Bengali, validation, option2): "নিচের প্রশ্নে, দেওয়া চারটি বিকল্পের মধ্যে থেকে সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে। … শীতল" — antonym selection tests Bengali vocabulary
  - [D25] Example 13 (Bengali, validation, option2): "নিচের বাক্যটির সঠিক সক্রিয় রূপ নির্বাচন করুন। সবাই তার চমৎকার নৃত্য পরিবেশনা দ্বারা মুগ্ধ হয়েছিল।" — active/passive voice tests Bengali grammatical competence

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Every sampled Bengali item is translated from English (is_translated=True across all 21 examples)
- **Dimension(s):** IC, IF
- **Observation:** All 21 Bengali validation examples in the sample carry `is_translated: True`. Per MILU documentation, ~25% of questions overall are translated using GPT-4O from English. The Bengali validation split in this sample shows 100% translated items. This means the Bengali content in this sample does not originate from Bengali-medium Indian exams at all — it is translated English content. No item in the Bengali validation sample was organically written in or sourced from a Bengali-language exam.
- **Deployment relevance:** The elicitation explicitly requires Bangladeshi Standard Bengali (Cholti register with Arabic/Persian loanword patterns). GPT-4O translation from English produces Bengali text in a standardized written register that almost certainly does not reflect Bangladeshi Cholti orthographic and lexical norms. The translated questions use vocabulary and phrasing patterns derived from English source content processed through a translation model likely trained on mixed Bengali corpora. This is the most direct form evidence of the register gap flagged in the deployment context.
- **Datapoint citations:**
  - [D8] All 21 Bengali validation examples (Bengali, validation): is_translated=True across the full sample — no organically Bengali-language exam content is present in this split's validation examples; all content is GPT-4O translated from English
  - [D1] Example 1 (Bengali, validation, option3): "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল?" — Indian 1991 crisis question translated into Bengali; vocabulary is formal written Bengali without any markers of Bangladeshi Cholti register

#### Concern 2: All cultural/political content in Bengali sample is exclusively India-centric; zero Bangladeshi cultural touchstones identified
- **Dimension(s):** IC, IO, OC
- **Observation:** Across the 21 Bengali validation examples, every culturally or politically specific item references Indian institutions, events, persons, or geography: India's 1991 financial crisis (Ex. 1), AAP's Punjab election win (Ex. 5), India's Election Commissioner removal procedure (Ex. 9), Indian leader Vinoba Bhave's "Mangal Bharat" (Ex. 12), the 65th Filmfare Awards (Ex. 17), and the Qutub Minar in Delhi (Ex. 18). Zero items reference: the 1971 Liberation War, Bangladeshi political history, Bangladeshi universities, Bangladeshi cultural events (Ekushe Boi Mela, Pohela Boishakh), Bangladeshi geography (Dhaka neighborhoods, Bangladeshi rivers), or Bangladeshi literary/cultural figures. This is consistent with documentation but confirmed empirically.
- **Deployment relevance:** The deployment requires that the benchmark evaluate LLMs on Bangladesh-specific cultural knowledge for Bengali story generation. The total absence of Bangladeshi cultural content means MILU Bengali scores measure performance on Indian cultural knowledge rendered in Bengali script — a fundamentally different construct from what is needed. High MILU Bengali accuracy does not predict Bangladeshi cultural grounding in story generation.
- **Datapoint citations:**
  - [D2] Example 5 (Bengali, validation, option4): "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" — India-specific political knowledge (Indian state elections); no Bangladeshi political equivalent present
  - [D3] Example 9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — Indian constitutional law (removal of India's Election Commissioner); Bangladesh's election commission structure is structurally different and absent
  - [D4] Example 12 (Bengali, validation, option4): "'মঙ্গল ভারত' কাজটি … আচার্য বিনোবা ভাবে" — Indian national movement figure; no Bangladeshi literary/cultural figure appears in any sampled item
  - [D5] Example 17 (Bengali, validation, option2): "৬৫তম ফিল্মফেয়ার অ্যাওয়ার্ডস, ২০২০-এ সেরা সিনেমাটোগ্রাফির জন্য পুরস্কারটি কে জিতেছেন? … জয় ওজা" — Filmfare Awards (Indian film industry); Bangladeshi film industry (Dhallywood, BTV drama) entirely absent
  - [D6] Example 18 (Bengali, validation, option4): "_______ দিল্লিতে কুতুব মিনারের নির্মাণ সম্পন্ন করেছিলেন … ইলতুতমিশ" — Delhi monument history; no Bangladeshi historical sites (Lalbagh Fort, Ahsan Manzil, Paharpur, Mainamati) present

#### Concern 3: Bangladesh appears only as a distractor option in non-Bengali language items — confirming structural absence
- **Dimension(s):** IO, IC
- **Observation:** In the Odia and Telugu validation samples, "Bangladesh" (বাংলাদেশ / బంగ్లాదేశ్) appears in option lists as a wrong-answer distractor in a question about which country first recognized the Indian Pharmacopoeia. This is the only appearance of Bangladesh in the entire 215-item cross-language sample. Bangladesh is not the subject of any question in any language split; it appears solely as a foil answer in India-centric questions.
- **Deployment relevance:** This direct observation confirms that Bangladesh is structurally positioned as a peripheral "foreign country" in MILU's knowledge frame, not as the primary geographic and cultural reference point. For a deployment centered on Bangladeshi Bengali cultural grounding, this framing is fundamentally misaligned.
- **Datapoint citations:**
  - [D22] Example 2 (Odia, validation, option4): "ଡିସେମ୍ବର 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆ… ବାଙ୍ଗ୍ଲାଦେଶ" — Bangladesh listed as option2 (wrong answer) in a question about Indian Pharmacopoeia; Bangladesh is a distractor, not a subject
  - [D23] Example 2 (Telugu, validation, option4): "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది? … బంగ్లాదేశ్" — same question in Telugu; Bangladesh again as distractor option

#### Concern 4: No Bangladeshi Bengali annotators — ground truth reflects Indian knowledge frameworks exclusively
- **Dimension(s):** OC
- **Observation:** Every examined item in the Bengali split carries a ground-truth answer label validated by Indian exam portal subject experts (per documentation) and audited by AI4Bharat (IIT Madras, IBM India). The culturally specific items in the Bengali sample [D2, D3, D4, D5, D6] all have correct answers that presuppose Indian constitutional, electoral, and cultural knowledge. No Bangladeshi institutional or individual validator is documented anywhere. For the governance/law questions (e.g., Election Commissioner removal procedure), the answer is verifiably correct for India but would be wrong if applied to Bangladesh's constitutional framework.
- **Deployment relevance:** The deployment requires native Bangladeshi Bengali speakers as primary ground truth. The benchmark's answer labels for cultural/governance content reflect Indian standards; a Bangladeshi evaluator might contest the framing of questions that appear to be generic ("the election commissioner") but actually encode Indian-specific legal structures.
- **Datapoint citations:**
  - [D3] Example 9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — the answer (President removes on CEC's recommendation) is specific to Indian constitutional law; Bangladesh's Election Commission operates under different provisions that a Bangladeshi annotator would recognize as distinct
  - [D2] Example 5 (Bengali, validation, option4): "আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" — requires knowledge of Indian party politics that is irrelevant to Bangladeshi civic knowledge

#### Concern 5: Output form (MCQ accuracy) fundamentally misaligned with deployment target (open-ended Bengali story generation)
- **Dimension(s):** OF, OO
- **Observation:** Every example across all 215 reviewed items is a closed-form 4-option MCQ. The output space is a discrete label (option1–option4). The deployment requires evaluating open-ended Bengali story generation — a generative task where cultural grounding, register appropriateness, narrative coherence, and accuracy of Bangladeshi named entities, historical events, and social context must be assessed. No mechanism in MILU produces a score that transfers to this task.
- **Deployment relevance:** This is a structural incompatibility: MCQ accuracy scores measure factual recall under forced choice, while story generation evaluation requires assessing fluency, cultural authenticity, register appropriateness, and factual grounding in Bangladeshi context. Strong performance on MILU Bengali (even if culturally recalibrated) would not directly validate culturally grounded story generation ability.
- **Datapoint citations:**
  - [D1] Example 1 (Bengali, validation, option3): "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল?" — The correct answer (option3) is binary pass/fail; this produces no information about whether a model can narratively describe economic history in Bangladeshi Bengali
  - [D19] Example 10 (Bengali, validation, option4): "হৃদয়ের পেসমেকার দ্বারা চিহ্নিত হয়, … এসএ নোড" — Medical MCQ; answering correctly does not predict whether the model can weave medical detail into a culturally authentic Bangladeshi story

---

#### MAJOR

#### Concern 6: Absence of 1971 Liberation War, Language Movement, and post-independence Bangladeshi political history
- **Dimension(s):** IO, IC
- **Observation:** None of the 21 Bengali examples, nor any English examples, reference the 1971 Liberation War, the 1952 Language Movement (Bhasha Andolan), Sheikh Mujibur Rahman, the founding of Bangladesh, or any post-1971 Bangladeshi political event. The History subject in Bengali covers the Bahamani Kingdom (Ex. 3) and Qutub Minar (Ex. 18) — medieval Indian history. The Law & Governance domain covers Indian state elections and Indian constitutional procedure.
- **Deployment relevance:** The 1971 Liberation War is described by the elicitation as "the foundational national narrative" for Bangladeshi Bengali speakers. The 2024 July Uprising — highly salient to the target student cohort — is post-benchmark and entirely absent. Any LLM evaluation intended to assess Bangladeshi cultural grounding must be able to test these topics; MILU provides no signal on them.
- **Datapoint citations:**
  - [D7] Example 3 (Bengali, validation, option4): "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল? … গুলবার্গা" — History subject item covers Deccan medieval Indian kingdom; the equivalent Bangladeshi history items (Liberation War, Language Movement) are absent
  - [D6] Example 18 (Bengali, validation, option4): "_______ দিল্লিতে কুতুব মিনারের নির্মাণ সম্পন্ন করেছিলেন … ইলতুতমিশ" — Delhi monument history; no equivalent Bangladeshi historical landmark questions appear

#### Concern 7: No items referencing Bangladeshi geography, institutions, or named entities
- **Dimension(s):** IC, IO
- **Observation:** Across all 21 Bengali items, no Bangladeshi geographic reference appears (no Dhaka, Cox's Bazar, Buriganga, Padma, Jamuna, Meghna, Rangamati, Sundarbans-Bangladesh). No Bangladeshi institution appears (no Dhaka University, BUET, IUT, BRAC University). The only geographic references in the Bengali sample are Indian: Delhi (Qutub Minar), Punjab (AAP election).
- **Deployment relevance:** The deployment explicitly requires LLM familiarity with Bangladeshi neighborhoods, rivers, universities, and tourism sites as reference points for story generation. MILU Bengali provides no data to evaluate this.
- **Datapoint citations:**
  - [D6] Example 18 (Bengali, validation, option4): "দিল্লিতে কুতুব মিনারের নির্মাণ" — Delhi is the only city named in culturally specific Bengali items; no Dhaka or Bangladeshi city appears
  - [D2] Example 5 (Bengali, validation, option4): "পাঞ্জাব" — Punjab (Indian state) is a named geographic reference; no Bangladeshi geographic equivalent present

#### Concern 8: Bengali register appears to be standardized written form, not Bangladeshi Cholti — no Arabic/Persian loanword patterns observed
- **Dimension(s):** IC, IF
- **Observation:** The Bengali vocabulary in the sampled items uses standard written Bengali orthography. Examining available lexical items: "আর্থিক সংকট" (financial crisis), "তাৎক্ষণিক" (immediate), "মুদ্রার রিজার্ভ" (currency reserves), "নির্বাচন কমিশনার" (election commissioner), "রাষ্ট্রপতি" (president). These are primarily Tatsama (Sanskrit-derived) formal vocabulary forms characteristic of the pan-Indian written Bengali register, not the Arabic/Persian loanword patterns that characterize Bangladeshi Standard Bengali Cholti. Terms like "সরকার" (government, from Persian "sarkar") do appear, but the overall lexical profile shows no distinctive Bangladeshi register markers. Given that all items are GPT-4O translations from English, this is expected.
- **Deployment relevance:** The elicitation identifies Bangladeshi Standard Bengali's Arabic/Persian loanword density as a distinguishing feature. A benchmark using Sanskritic-heavy written Bengali vocabulary would underestimate model performance on Bangladeshi-register text if models have been trained on predominantly Bangladeshi Bengali corpora, or overestimate it if models are stronger on the West Bengali register being tested.
- **Datapoint citations:**
  - [D1] Example 1 (Bengali, validation, option3): "বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ … তেল ও পেট্রোলিয়াম পণ্যের আমদানির মূল্যের তীব্র বৃদ্ধি" — vocabulary: "তাৎক্ষণিক" (tātkṣaṇika, Sanskrit-derived), "আমদানি" (Persian/Arabic "āmdāni"); mixed register with no distinctively Bangladeshi Cholti markers
  - [D25] Example 13 (Bengali, validation, option2): "তার চমৎকার নৃত্য পরিবেশনা সবাইকে মুগ্ধ করেছিল।" — "নৃত্য পরিবেশনা" (nṛtya paribeśanā) uses Sanskrit-derived dance vocabulary; standard written Bengali without Bangladeshi-specific register markers

#### Concern 9: India-specific governance and law content in Bengali may produce false negatives for Bangladeshi users
- **Dimension(s):** OC, OO
- **Observation:** Several Bengali governance items test knowledge of Indian constitutional and electoral procedures that are structurally different in Bangladesh. Example 9 tests removal of India's Election Commissioner (answer: President on CEC's recommendation). Example 5 tests which Indian state AAP won in 2022. A Bangladeshi user who correctly knows Bangladesh's electoral commission structure but answers according to that knowledge would be marked wrong. These items produce false negative scores for Bangladeshi cultural knowledge rather than measuring gaps.
- **Deployment relevance:** For a deployment evaluating Bangladeshi cultural grounding, items that penalize Bangladeshi-specific knowledge while rewarding Indian-specific knowledge produce construct-irrelevant variance that would make MILU Bengali scores misleading as a validity measure for this deployment.
- **Datapoint citations:**
  - [D3] Example 9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — correct only for Indian constitutional law; Bangladesh's equivalent procedure differs
  - [D14] Example 7 (Bengali, validation, option4): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প … জাতীয় খাদ্য সুরক্ষা মিশন আগস্ট ২০০৭ সালে চালু হয়েছিল" — India's National Food Security Mission; a Bangladeshi user has no reason to know this Indian government program

---

#### MINOR

#### Concern 10: Bengali validation split has disproportionately high translation rate compared to documented 25% overall
- **Dimension(s):** IC, IF
- **Observation:** MILU documentation states that ~25% of total questions are translated from English. Yet all 21 Bengali validation examples sampled show `is_translated: True` (100%). While the sample size (21) is small and the validation split may differ from the test split, this suggests the Bengali validation split is predominantly or entirely composed of translated items, not organically sourced Bengali exam content.
- **Deployment relevance:** If the test split for Bengali also has a higher-than-average translation rate, then MILU Bengali performance reflects model ability to read translated English content in Bengali script rather than genuine Bengali-medium cultural knowledge. This further compounds the register gap concern.
- **Datapoint citations:**
  - [D8] All 21 Bengali validation examples (Bengali, validation): is_translated=True — 100% translation rate in the sampled Bengali validation split, compared to documented 25% overall benchmark average

#### Concern 11: Cross-language contamination — identical questions appear verbatim across multiple language splits
- **Dimension(s):** IF
- **Observation:** The 1991 India financial crisis question (D1), Bahamani Kingdom capital question (D7), Qutub Minar question (D6), cross-assembler question (D20), and Mediterranean climate question appear verbatim translated across Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, and Telugu splits. This confirms that a large portion of MILU's multilingual content is parallel translations of the same question set rather than language-specific sourcing.
- **Deployment relevance:** For a Bangladeshi Bengali deployment, this means that MILU's Bengali content does not capture any language-specific cultural knowledge that is unique to Bengali-medium contexts — it is a translation of pan-Indian English exam content. The "regional state exam" value proposition claimed in the documentation does not appear to materialize in the Bengali validation sample.
- **Datapoint citations:**
  - [D7] Example 3 (Bengali, validation, option4): "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল? … গুলবার্গা" — same question appears in Gujarati Ex. 3 ("બહમણી રાજ્યની પ્રથમ રાજધાની"), Hindi (not sampled but implied by cross-config parallel), Malayalam Ex. 3 ("ബഹ്മനി സാമ്രാജ്യത്തിന്റെ ആദ്യ തലസ്ഥാനം"), Punjabi Ex. 3 ("ਬਹਮਨੀ ਰਾਜ ਦਾ ਪਹਿਲਾ ਰਾਜਧਾਨੀ"), Tamil Ex. 18, Telugu (not in sample) — identical content across all languages confirms parallel translation, not language-specific sourcing

#### Concern 12: Rural, riverine, and village life contexts — structurally absent in exam format
- **Dimension(s):** IO
- **Observation:** All 215 reviewed examples are competitive examination questions (civil services, engineering entrance, technical knowledge) targeting urban, academically educated populations. No item invokes agricultural life, river ecology, monsoon seasons, boat culture, fishing villages, or rural Bangladesh contexts. This is a structural feature of the exam-sourced data collection methodology, not a sampling artifact.
- **Deployment relevance:** The deployment explicitly requires coverage of rural/village Bangladesh and riverine contexts as narrative settings for story generation. No MILU item provides evaluation signal for LLMs' ability to generate authentic content in these registers.
- **Datapoint citations:**
  - [D13] Example 2 (Bengali, validation, option3): "একটি ক্রিকেট প্রশিক্ষণ শিবিরে ১২০০ জন শিশু" — the most "everyday" context in the Bengali sample is a cricket training camp, still an organized institutional setting; no rural or riverine reference exists in any sampled item
  - [D27] Example 11 (Bengali, validation, option3): "সিদ্ধান্ত গ্রহণের সাথে যুক্ত সমস্যাগুলি হল: … ভয় এবং মিথ্যা আশা" — management psychology question; the register throughout is urban, academic, and professional

---

### Content Coverage Summary

The Bengali validation split of MILU (21 examples reviewed) consists entirely of translated English exam questions (`is_translated=True` in 100% of the sample), covering: electrical engineering and materials science (Exs. 4, 15, 16, 21), general sciences (Exs. 8, 10, 14), India-specific law and governance (Exs. 5, 9), India-specific history (Exs. 3, 7, 18), India-specific culture and arts (Exs. 12, 17), Indian government programs (Ex. 7), quantitative reasoning (Exs. 2, 16, 20), Bengali language grammar (Exs. 6, 13), management/business (Exs. 1, 11, 19), and environmental science (Ex. 7).

The cultural, political, and geographic content is uniformly India-centric. Named entities include: AAP (Indian party), Punjab (Indian state), the Indian President and Chief Election Commissioner, Vinoba Bhave (Indian nationalist leader), Filmfare Awards (Indian film industry), Qutub Minar (Delhi), and the Bahamani Kingdom (Deccan Sultanate). No Bangladeshi named entity, institution, historical event, geographic location, or cultural figure appears in any Bengali example.

Cross-config inspection confirms that the same questions appear in parallel translation across all 11 language splits, confirming that the Bengali content is not sourced from Bengali-medium Indian state exams (which would produce at least some India-regional Bengali content) but rather from pan-Indian English exam questions translated into Bengali.

Register analysis of the Bengali text shows standard formal written Bengali using primarily Tatsama vocabulary. No distinctive Bangladeshi Cholti register markers or Arabic/Persian loanword density patterns are observed.

The English split confirms the India-centric content origin: state-specific Indian governance (Maharashtra legislative committees, Telangana welfare scheme, Indian Railways named after Indian freedom fighter, Niti Aayog India Innovation Index). These are the source documents from which the Bengali translations derive.

---

### Limitations

1. **Sample size:** Only 21 Bengali validation examples were reviewed. The test split (6,637 examples) may contain a different proportion of translated vs. organically sourced items, and may include items from Bengali-medium Indian state exams that do not appear in the validation split. The 100% translation rate observed in the validation sample should not be assumed to apply to the test split without direct verification.

2. **Register analysis limits:** Determining whether Bengali text reflects Bangladeshi Cholti vs. West Bengali orthographic norms requires systematic lexical analysis by a native Bangladeshi Bengali linguist. The present analysis observes vocabulary patterns but cannot definitively classify register with certainty from a 21-item sample.

3. **Test split not sampled:** The full Bengali test split (6,637 examples) was not inspected. It is possible that organically sourced Bengali-medium exam items in the test split contain some Bangladeshi-relevant content, though the documentation strongly suggests this is unlikely given the Indian exam sourcing.

4. **Domain distribution:** The 21-item validation sample may not reflect the domain distribution of the full test split. The high proportion of STEM-adjacent items with `is_translated=True` may be a validation-split artifact.

5. **No audio or image modalities:** MILU is text-only; no audio or image content was present to inspect. This limitation is alignment-confirming (deployment is text-only) rather than a gap in this analysis.

6. **Annotator demographics not directly inspectable:** The demographic composition of annotators cannot be verified from the dataset itself; this analysis relies on documentation disclosures showing exclusively Indian institutional affiliation.

