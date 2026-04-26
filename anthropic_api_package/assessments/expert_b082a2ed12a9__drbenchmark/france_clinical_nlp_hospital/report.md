## Deployment Context

**Use case:** In a hospital setting, a clinician uses software to manage unstructured French clinical cases by applying a model evaluated on part-of-speech tagging, named-entity recognition, and multi-label classification. The system identifies specific clinical and temporal entities while mapping pathologies to standardized medical classification chapters and axes to automatically generate a patient’s clinical profile. These outputs directly help the clinician summarize complex medical histories and prioritize care based on the severity of identified symptoms, ensuring that life-critical decisions are supported by accurately synthesized data.
**Target population:** French-speaking medical professionals, including clinicians, hospital physicians, and nursing staff in French-speaking health systems.

# Validity Analysis: drbenchmark
**Target context:** French Pharmaceutical Regulatory NLP — DrBenchmark Assessment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
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

DrBenchmark is a well-engineered, methodologically rigorous benchmark for French biomedical NLP across 20 tasks, 6 task categories, and 8 pre-trained masked language models — but it is not a regulatory NLP benchmark. For the target deployment (compliance verification of French pharmaceutical regulatory documents using NER and STS), three of six dimensions (Output Ontology, Output Content, Input Ontology) score at the bottom of the rubric, and a fourth (Input Content) scores 2. The benchmark's input genres are clinical case reports, research abstracts, clinical trial protocols, exam questions, and transcribed prescriptions — empirically confirmed across all 12 datasets. Not a single task derives from current EMA QRD-formatted SmPCs, current PIL templates, CTD modules, or ANSM-format submissions; the closest analogous regulatory NLP corpus is Italian DART (2024) [WEB-15] with no French equivalent. NER label sets use UMLS Semantic Groups, MeSH, and ICD-10 — INNs, ATC codes, excipient nomenclature, MedDRA, and contraindication qualifiers are absent. STS calibration failures are empirically demonstrated on legally significant differences (DEFT2020-D10, CLISTER-D8, D9). Annotator workforces include no regulatory affairs or legal specialists. Input Form is the lowest-concern dimension (text-only, Latin script, mature French NLP infrastructure), and Output Form is moderately compatible but lacks workflow-calibration metrics tied to regulatory adjudication. The benchmark can supply useful baseline evidence on French biomedical language understanding capabilities of candidate models, but it cannot serve as the validity basis for a regulatory compliance system.

## Practical Guidance

### What This Benchmark Measures

DrBenchmark measures generalist and specialized French biomedical language model performance on clinical-research NLP tasks: clinical case POS tagging and NER, biomedical literature classification, pharmacy-domain MCQA, clinical-case STS, and ICD-10 chapter classification. For the target deployment it provides indirect evidence — primarily on Input Form (text-only French Latin-script handling), basic NER capability on clinical entity types (DEFT-2021 DOSAGE/SUBSTANCE/TREATMENT, PxCorpus drug/dose/mode), and general-purpose STS scoring behavior. The strongest dimensions for the deployment are Input Form and Output Form (structural compatibility with the pipeline).

### Construct Depth

The benchmark probes French biomedical language understanding deeply across 20 tasks with rigorous reproducibility (4-run averaging, t-tests, documented hyperparameters [Q51]) but does not probe regulatory document NLP at all. For Output Ontology and Output Content — the dimensions most central to compliance-checking — the benchmark provides essentially no construct-relevant evidence: regulatory entity classes are absent from label sets and regulatory expertise is absent from annotation workflows. STS scoring, while well-instrumented, is empirically shown to be insensitive to legally significant small differences (DEFT2020-D10, CLISTER-D9), so it does not measure the construct the deployment requires.

### What Else You Need

A regulatory-domain French benchmark must be built or sourced before this system is deployed. Specific supplementation: (1) for Input Ontology and Input Content — assemble a French SmPC/PIL/CTD corpus modeled on Italian DART [WEB-15] with current QRD v10.4 [WEB-7] and ANSM 'Feuille de style' [WEB-5] coverage; (2) for Output Ontology — define a regulatory NER schema with INN, ATC, excipient, MedDRA, contraindication-qualifier, and SmPC-section classes, and design a regulatory-equivalence STS rubric; (3) for Output Content — recruit a regulatory affairs / pharmacovigilance / legal annotator pool and document IAA on borderline safety-warning pairs; (4) for Output Form — add workflow-calibration metrics (precision-at-threshold, false-flag rate, calibration curves) aligned with EU AI Act high-risk obligations [WEB-13, WEB-14]; (5) for DROM coverage — collect tropical-pathology vocabulary content from French overseas territories. Additionally evaluate net-new models (CamemBERT 2.0 [WEB-28], DrLongformer-CP [WEB-16], AliBERT) not covered in DrBenchmark.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
DrBenchmark covers 20 tasks across POS, NER, MCQA, MCC, MLC, and STS [Q1, Q17, Q18, Q81], representing genuine breadth for French biomedical NLP. However, for the deployment's HIGH-priority requirement of regulatory document compliance NLP, the task taxonomy is structurally misaligned. No task derives from current EMA QRD-formatted SmPCs, current PIL templates, CTD modules, or ANSM-format submissions; QUAERO EMEA leaflets [Q34] and DEFT-2020 drug labels [Q21] are pre-existing research corpora predating QRD v10.4 [WEB-7]. Empirical inspection confirms universal genre mismatch: every dataset is clinical case prose, research abstract, trial protocol, exam question, or transcribed speech (DATASET cross-cutting C1). MCQA (FrenchMedMCQA), POS tagging (CAS, ESSAI), and clinical-case ICD-10 classification (DiaMed [Q45]) contribute task types of limited deployment relevance. The closest analogous regulatory NLP benchmark is Italian DART (2024), with no French equivalent [WEB-15].

**Strengths:**
- Genuinely broad task-type coverage across 6 categories including STS and NER which match deployment task families [Q1, Q18]
- QUAERO and Mantra-GSC do include EMEA drug-label genre as the closest available approximation to regulatory text (QUAERO-D1, QUAERO-D2)
- PxCorpus contributes posology-style NER schema (drug, dose, mode) that has surface overlap with regulatory entity needs [Q44]

**Checklist:**

- **IO-1**: Required deployment task categories are NER over regulatory entity types (INNs, ATC codes, excipients, posology, contraindication qualifiers, MedDRA terms) and STS calibrated for regulatory equivalence on SmPCs/PILs/CTD modules [WEB-6, WEB-7, WEB-15]. — _Sources: WEB-6, WEB-7, WEB-15_
- **IO-2**: Yes — taxonomy omits regulatory-document NER and regulatory-equivalence STS. No DrBenchmark task derives from QRD-formatted SmPCs, current PIL templates, CTD modules, ANSM 'Feuille de style' submissions, or PSURs [Q34, Q44, Q45; DATASET C1; WEB-5, WEB-15]. — _Sources: Q34, Q44, Q45, WEB-5, WEB-15_
- **IO-3**: MCQA from pharmacy licensing exams (FrenchMedMCQA [Q39]), veterinary content in MORFITT (MORFITT-D11, D12, D13, D14), and POS tagging on clinical case narratives (CAS [Q42], ESSAI [Q43]) are largely irrelevant to a regulatory compliance NLP pipeline. — _Sources: Q39, Q42, Q43_
- **IO-4**: Category gaps documented: no SmPC-section-structured tasks; no regulatory-equivalence STS; no pharmacovigilance signal detection; no MedDRA-coded adverse effect classification. Confirmed gap with Italian DART as the only structurally similar benchmark in any language [WEB-15]. — _Sources: WEB-15_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'It encompasses 20 diversified tasks, including named-entity recognition, part-of-speech tagging, question-answering, semantic textual similarity, and classification.' (p.1)
- [Q17] 'Our proposed benchmark comprises 20 French biomedical language understanding tasks, one of which is specifically created for this benchmark.' (p.2)
- [Q34] 'The dataset covers two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE.' (p.3)
- [Q44] 'PxCorpus...is a spoken language understanding dataset in the domain of medical drug prescription transcripts.' (p.4)
- [Q45] 'DiaMed is an original dataset...comprises 739 new French clinical cases collected from an open source journal (The Pan African Medical Journal).' (p.4)

*Web sources:*
- [WEB-7] EMA QRD product information template v10.4 defines current SmPC structure (sections 4.1–4.9)
- [WEB-15] DART (2024) Italian SmPC NER/RE corpus is the closest analogous regulatory NLP resource; no French equivalent identified
- [WEB-5] France adds national 'blue-box' and 'Feuille de style' regulatory layer not in QUAERO EMEA

*Dataset analysis:*
- Cross-cutting C1: Universal genre mismatch — every dataset is clinical/research/exam/transcribed-speech, not regulatory submission text
- QUAERO-D7, QUAERO-D8: EMEA documents sentence-split, header fragments isolated — document-level regulatory structure destroyed
- MORFITT-D11–D14: Veterinary content irrelevant to human pharmaceutical regulation
- ESSAI-D8, ESSAI-D9: Experimental drug codes (BMS-986179, MEDI9197) rather than approved product labeling vocabulary
- PXCORPUS-D9, D10: No regulatory submission text in PxCorpus despite drug-prescription domain

</details>

**Information gaps:**
- No published crosswalk between EMA/ANSM regulatory annotation guidelines and DrBenchmark task categories
- Whether ANSM circulars define NLP-relevant document subgenres beyond SmPC/PIL is not documented in retrievable form

**Requires expert verification:**
- Specific ANSM-mandated document genres beyond SmPC/PIL/CTD that may need their own task categories
- Whether overseas-territory regulatory texts (DROM-specific adaptations) constitute a distinct task-category requirement

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Source diversity is genuine — scientific literature, clinical trials, clinical cases, speech transcriptions, drug leaflets [Q19, Q33, Q34, Q38, Q39, Q43, Q44]. However, for the HIGH-priority deployment requirement of regulatory entity vocabulary (INNs, ATC codes, excipient nomenclature, posology templates, contraindication qualifiers, MedDRA), benchmark content provides only incidental coverage. ATC codes appear in QUAERO text but are unlabeled (QUAERO-D3, QUAERO-D4); INNs and excipients are conflated under a single CHEM tag (QUAERO-D5, QUAERO-D6, MANTRAGSC-D8). Substantial benchmark content is irrelevant to regulatory compliance: encyclopedic non-medical content in DEFT-2020 (apiculture, sports, WWII, railways — DEFT2020-D6 through D9), Pan African clinical cases in DiaMed [Q45] (DIAMED-D9), African and other non-metropolitan provenance in E3C and DEFT-2021 (E3C-D8, E3C-D9, DEFT2021-D3, DEFT2021-D12), and experimental drug codes in ESSAI (ESSAI-D8, D9). No data from French overseas territories is identified, despite secondary deployment scope; tropical pathology vocabulary (dengue, chikungunya, paludisme) is absent from all label sets.

**Strengths:**
- QUAERO EMEA includes excipient lists, posology, and contraindication content as raw text even if not labeled distinctly (QUAERO-D1, QUAERO-D2, QUAERO-D15)
- DEFT-2020 contains real drug-label sentence pairs covering breastfeeding contraindications, excipient warnings, and pharmaceutical form (DEFT2020-D1, D2, D4)
- Diverse data origins from authoritative biomedical sources — MEDLINE, EMEA, PMC OA, real pharmacy exam questions, clinical trial protocols [Q19, Q34, Q38, Q39, Q43]

**Checklist:**

- **IC-1**: Yes — deployment requires metropolitan French regulatory vocabulary (INN, ATC, EMA-template phrasing) [WEB-5, WEB-7] and secondarily DROM-specific tropical pathology vocabulary [WEB-19, WEB-20]. Neither is well covered. — _Sources: WEB-5, WEB-7, WEB-19, WEB-20_
- **IC-2**: Mixed — biomedical content is genre-appropriate but a non-trivial fraction reflects non-metropolitan-French settings (Pan African clinical cases in DiaMed [Q45], DIAMED-D3, D9, D12; African references in E3C-D8, E3C-D9; international provenance in MORFITT-D4 through D10) introducing construct-irrelevant variance. — _Sources: Q45, DIAMED-D3, DIAMED-D9, E3C-D8, E3C-D9, MORFITT-D4_
- **IC-3**: Yes — substantial encyclopedic non-medical content in DEFT-2020 (DEFT2020-D6, D7, D8, D9), veterinary content in MORFITT (MORFITT-D11–D14), and experimental compound codes in ESSAI (ESSAI-D8, D9) are largely irrelevant to French pharmaceutical regulatory compliance. — _Sources: DEFT2020-D6, DEFT2020-D7, MORFITT-D11, ESSAI-D8_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotator review by French regulatory affairs specialists is documented for any constituent dataset. Recruitment of ANSM/LEEM-affiliated reviewers would resolve.
- **IC-5**: Documented content issues: ATC codes textually present but unlabeled (QUAERO-D3, D4); INN/excipient conflation under CHEM (QUAERO-D5, D6, MANTRAGSC-D8); no MedDRA-coded content; no France-specific blue-box/CIP code/Feuille de style content [WEB-5]; no DROM data; uneven geographic provenance dilutes metropolitan-France representativeness. — _Sources: QUAERO-D3, QUAERO-D5, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q19] 'A diverse range of data origins: Scientific literature, clinical trials, clinical cases, speech transcriptions...' (p.2)
- [Q34] 'The dataset covers two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE.' (p.3)
- [Q45] 'DiaMed...comprises 739 new French clinical cases collected from an open source journal (The Pan African Medical Journal).' (p.4)
- [Q39] 'FrenchMedMCQA...contains 3,105 questions coming from real exams of the French medical specialization diploma in pharmacy' (p.4)

*Web sources:*
- [WEB-5] France-specific blue-box, CIP codes, Feuille de style, and List I/II classification add a national regulatory layer not in QUAERO EMEA
- [WEB-7] EMA QRD v10.4 SmPC sections 4.1–4.9 define regulatory phrasing not modeled in benchmark
- [WEB-19], [WEB-20] DROM (Martinique, Guadeloupe, French Guiana, Réunion, Mayotte) under Article 73 — distinct disease prevalence not covered

*Dataset analysis:*
- QUAERO-D3, D4: ATC codes textually present but not annotated as entities
- QUAERO-D5, D6: INN/excipient conflated under CHEM with no sub-typing
- DEFT2020-D6, D7, D8, D9: Encyclopedic non-medical content (apiculture, sports, WWII, railways) is construct-irrelevant
- DIAMED-D3, D9, D12: Sub-Saharan African institutional provenance (Burkina Faso, Niger, Morocco) throughout DiaMed
- MORFITT-D4 through D10: International provenance (Canada, Jordan, Egypt, Saudi Arabia, Japan, China)
- ESSAI-D8, D9: Experimental compound codes (BMS-986179, MEDI9197) rather than approved product vocabulary
- MORFITT-D15: One Chikungunya abstract is the only DROM-relevant tropical pathology content found

</details>

**Information gaps:**
- No documented ATC code, MedDRA, or excipient nomenclature crosswalk for benchmark content
- No DROM-specific tropical pathology corpus identified
- Whether France-specific blue-box/CIP code/Feuille de style content appears in any benchmark dataset is unknown

**Requires expert verification:**
- Whether vocabulary patterns for DROM regulatory adaptations differ materially from metropolitan French regulatory text — requires ARS/ANSM regional officer elicitation

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Both benchmark and deployment are text-only French in Latin script with diacritics; no script, modality, or infrastructure mismatch. The benchmark provides a HuggingFace-based normalized toolkit [Q47, Q48] compatible with standard institutional ML infrastructure. PxCorpus is the only modality outlier — transcribed speech with disfluencies, code-switching, system error messages, and truncations (PXCORPUS-D2, D3, D16, D17, D18) — but this is a single dataset and its transcriptions are already text-form when ingested [Q44]. QUAERO EMEA preprocessing introduces systematic measurement error: sentence-splitting destroys document structure (QUAERO-D7, D8, D9, D10) and 6.06–8.90% of nested annotations are lost [Q37], directly relevant to regulatory text where nested entity structures may carry compliance significance. Tokenization is studied as a variable [Q75, Q89, Q90] and shown to play a minor role [Q80]. Random 70/10/20 splits where datasets lacked predefined ones [Q32, Q42] is a methodological choice users should note. Overall this is the lowest-concern dimension as documented.

**Strengths:**
- Pure text French Latin-script alignment with deployment — no script, dialect, or modality mismatch
- Standardized HuggingFace + PyTorch toolkit with normalized loaders supports institutional ML infrastructure [Q47, Q48]
- Tokenization studied as a variable across 8 models with sub-token rates reported [Q75, Q89, Q90]
- Empirical confirmation that all non-PxCorpus datasets are well-formed standard French in Latin script (Confirmed Property 1)

**Checklist:**

- **IF-1**: Signal distributions match — both benchmark and deployment are written French text in Latin script with standard diacritics. No image/audio/cross-script considerations [Q31, Q44]. — _Sources: Q31, Q44, Confirmed Property 1_
- **IF-2**: Yes — HuggingFace Datasets/Transformers + PyTorch infrastructure [Q48] is fully supported in French enterprise pharma IT environments [WEB-12]. HDS certification is a hosting compliance requirement [WEB-11, WEB-12], not an infrastructure incompatibility. — _Sources: Q48, WEB-11, WEB-12_
- **IF-3**: Domain-specific form differences exist: QUAERO EMEA preprocessing loses 6.06–8.90% of nested annotations and sentence-splits long documents [Q37], confirmed empirically (QUAERO-D7, D8, D9, D10) — relevant for full SmPC processing where document-level structure matters. PxCorpus transcribed-speech artifacts (PXCORPUS-D16, D17, D18) would not transfer well to written regulatory text. — _Sources: Q37, QUAERO-D7, PXCORPUS-D16_
- **IF-4**: Form mismatches harming external validity: (1) QUAERO EMEA document fragmentation distorts the closest-to-regulatory dataset; (2) PxCorpus spoken-form artifacts limit transfer; (3) some non-French tokens in QUAERO (QUAERO-D11, D12) and OCR/copy-paste artifacts in E3C (E3C-D10, D11). Long-document handling for full SmPCs (>512 tokens) is not benchmarked — DrLongformer-CP exists but was not included [WEB-16]. — _Sources: Q37, QUAERO-D11, E3C-D10, WEB-16_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'While the dataset covers 5 languages, only the French portion is retained for the benchmark.' (p.3)
- [Q37] 'an average loss of 6.06% of the annotations on EMEA and 8.90% on MEDLINE...we decided to split these documents into sentences.' (p.3)
- [Q44] 'The recordings were manually transcribed and semantically annotated.' (p.4)
- [Q48] 'We developed a practical toolkit based on the HuggingFace Datasets library...adhere to normalized schemes and predefined data splits.' (p.5)
- [Q80] 'tokenization, as it is currently done in MLMs, seems to play a minor role in the performance of systems.' (p.8)

*Web sources:*
- [WEB-11] French HDS certification required for hosting health data — compliance constraint, not infrastructure incompatibility
- [WEB-12] French enterprise pharma IT infrastructure mature; no infrastructure bottleneck expected
- [WEB-16] DrLongformer-CP (2024) extends beyond 512 tokens — not in DrBenchmark

*Dataset analysis:*
- Confirmed Property 1: All datasets except PxCorpus are well-formed standard French Latin script — IF lowest concern
- QUAERO-D7, D8, D9, D10: Document fragmentation artifacts confirmed empirically — preprocessing destroys regulatory structure
- PXCORPUS-D16, D17, D18 (CRITICAL): Spoken-language transcription artifacts make PxCorpus unrepresentative of written regulatory text
- E3C-D10, D11: Tokenization artifacts from OCR/copy-paste
- QUAERO-D11, D12: Non-French tokens (Czech, German/English) in EMEA data

</details>

**Information gaps:**
- Long-document (>512 token) handling for full SmPCs not benchmarked

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
This dimension represents one of the most severe validity violations. NER label taxonomies use UMLS Semantic Groups [Q35, Q103], MeSH chapters [Q27, Q107], ICD-10 chapters [Q45], or clinical entity types [Q108] — none of which distinguish regulatory entity classes required by the deployment. INNs, ATC codes, excipient nomenclature, EMA SmPC section identifiers, and contraindication qualifiers are absent from every label set. Empirical inspection confirms ATC codes appear in QUAERO text but are unlabeled (QUAERO-D3, D4); INNs and excipients are conflated under CHEM (QUAERO-D5, D6, MANTRAGSC-D8); MedDRA terminology required for SmPC section 4.8 is absent from all benchmark label sets [WEB-7]. The STS scale 0–5 [Q22, Q41] is calibrated for general semantic proximity, not regulatory equivalence — empirically demonstrated by DEFT2020 scoring omission of 'sous stricte surveillance médicale' at 3.6 (DEFT2020-D10), CLISTER scoring a 15-fold PSA difference at 3.75 (CLISTER-D9), and a 2-fold biological value difference at 4.0 (CLISTER-D8). DrBERT-FS does not excel on MLC or STS [Q82], the two task families most central to deployment compliance-checking. No published EMA/ANSM regulatory-equivalence scoring rubric exists [WEB-10].

**Strengths:**
- DEFT-2021 NER includes DOSAGE, SUBSTANCE, TREATMENT, FREQUENCY, MODE entity types [Q108] which provide partial overlap with posology entity needs
- PxCorpus NER schema distinguishes drug, dose, mode (38 classes [Q44]) including INN/brand distinction in some tags (PXCORPUS-D6, D7)
- Label taxonomies are richly documented in appendices for all NER tasks [Q103–Q108]

**Checklist:**

- **OO-1**: Output label categories reflect biomedical-research and clinical ontologies (UMLS, MeSH, ICD-10) [Q35, Q27, Q45]; partial regulatory relevance only via DEFT-2021 DOSAGE/SUBSTANCE/TREATMENT [Q108] and PxCorpus drug/dose/mode [Q44]. — _Sources: Q35, Q27, Q45, Q108_
- **OO-2**: Missing regional regulatory categories: INNs as a distinct class, ATC codes, excipient nomenclature (EPC/INCI), EMA SmPC section structural markers, MedDRA-coded adverse effects, contraindication qualifiers, pharmacovigilance signal terms, France-specific blue-box elements [WEB-5, WEB-7]. Empirically: ATC codes textually present but unlabeled (QUAERO-D3, D4); INN/excipient conflated (QUAERO-D5, D6). — _Sources: QUAERO-D3, QUAERO-D5, WEB-5, WEB-7_
- **OO-3**: STS 0–5 Likert scale [Q22, Q41] encodes general semantic-proximity assumptions, not regulatory equivalence. DEFT2020 and CLISTER empirically demonstrate calibration failure on legally significant differences (DEFT2020-D10, D11, D12; CLISTER-D8, D9, D10). The `moy`/`vote` divergence in DEFT2020 (DEFT2020-D18, D19, D20) further obscures ground-truth scoring semantics. — _Sources: Q22, Q41, DEFT2020-D10, CLISTER-D8, CLISTER-D9, DEFT2020-D18_
- **OO-4**: Stakeholder-driven taxonomy redesign is required: an EMA/ANSM-aligned regulatory NER schema (modeled e.g. on Italian DART [WEB-15]) and a regulatory-equivalence STS rubric calibrated to safety-warning legal significance. — _Sources: WEB-15_
- **OO-5**: Documented harms: structural validity violation (UMLS/MeSH/ICD-10 do not represent regulatory entity structure); content validity violation (entire entity classes missing); convergent validity threat (STS scoring does not correlate with regulatory equivalence judgment). — _Sources: Q82, Cross-cutting C2_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'identifying the degree of similarity within pairs of sentences, from 0 (the less similar) to 5 (the most similar).' (p.3)
- [Q35] '10 entity categories corresponding to the UMLS Semantic Groups...were annotated' (p.3)
- [Q41] 'CLISTER...similarity scores ranging from 0 to 5...averaged together' (p.4)
- [Q82] 'the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS.' (p.8)
- [Q103] 'O, GEOG, PHEN, DISO, ANAT, OBJC, PHYS, PROC, DEVI, CHEM and LIVB' (p.14)
- [Q108] 'Named-entity recognition: O, ANATOMY, DATE, DOSAGE, DURATION, MEDICAL EXAM, FREQUENCY, MODE, MOMENT, PATHOLOGY, SOSY, SUBSTANCE, TREATMENT and VALUE' (p.14)

*Web sources:*
- [WEB-7] EMA QRD v10.4 mandates SmPC section 4.8 use MedDRA terminology — absent from all benchmark label sets
- [WEB-10] No published EMA/ANSM regulatory-equivalence scoring rubric for NLP found
- [WEB-15] DART (Italian) demonstrates a regulatory-aligned NER schema with active substance, route of administration, contraindication, ADR, drug-drug interaction classes — no French equivalent

*Dataset analysis:*
- Cross-cutting C2: Universal NER label taxonomy misalignment with regulatory entity types
- QUAERO-D3, D4: ATC codes textually present but entirely unlabeled — direct entity-class gap
- QUAERO-D5, D6, MANTRAGSC-D8: INN/excipient conflated under CHEM with no sub-typing
- DEFT2020-D10: Omission of 'sous stricte surveillance médicale' scored 3.6/5 — STS calibration failure
- CLISTER-D8: 2-fold biological value difference scored 4.0; CLISTER-D9: 15-fold PSA difference scored 3.75
- DEFT2020-D18, D19, D20: moy/vote divergence (up to 2.8 points) — ambiguous ground truth for threshold setting

</details>

**Information gaps:**
- No published EMA/ANSM regulatory-equivalence scoring rubric to use as a reference standard
- No published crosswalk between EMA/ANSM annotation guidelines and DrBenchmark NER schemas

**Requires expert verification:**
- Specific entity-class hierarchy a French regulatory NER schema should adopt — requires regulatory affairs expert elicitation
- Threshold values for STS scores that should constitute 'regulatory equivalent' vs. 'requires manual review'

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Annotation workforce alignment is severely deficient for the deployment. Benchmark annotators are described as clinical case reviewers, medical experts, or NLP researchers [Q25, Q41, Q42, Q45]; no constituent dataset documents involvement of regulatory affairs specialists, pharmacovigilance officers, or legal experts applying EMA SmPC guidelines or ANSM circulars. DiaMed's narrow IAA validation base (15 cases per session, 4 annotators [Q45, Q46]) and CAS's silver-standard automatic annotation at 98% precision [Q42] further weaken ground-truth authority. DEFT-2021 reports no IAA. Empirical inspection confirms high annotator disagreement on drug-label STS pairs — DEFT2020 5-annotator score ranges of 3+ points (DEFT2020-D14, D15, D16, D17), and `moy`/`vote` divergence up to 2.8 points (DEFT2020-D18, D19, D20). Independent 2024 evaluation [WEB-18] confirms cross-task IAA is unreliable due to methodological heterogeneity. For a deployment where authoritative ground truth rests with regulatory-legal professionals applying EMA QRD templates [WEB-7] and ANSM circulars [WEB-5], the divergence is categorical and unmitigated.

**Strengths:**
- DiaMed inter-annotator agreement reported using both Cohen's Kappa and Gwet's AC1 over two sessions, providing methodological transparency [Q45, Q46]
- CLISTER averages multiple annotators' scores to produce ground truth [Q41]
- Authorship is from credible French biomedical NLP institutions including CHU Nantes and INSERM [Q7, Q8]
- DEFT-2021 manual annotation workflow documented [Q25]

**Checklist:**

- **OC-1**: No — ground truth labels reflect clinical/research-NLP expert perspectives, not regulatory affairs / pharmacovigilance / legal-expert perspectives that authoritatively apply EMA SmPC guidelines and ANSM circulars [WEB-5, WEB-7]. Deployment elicitation Q4 confirms human-in-the-loop adjudication design but did not resolve annotator-norm alignment. — _Sources: Q25, Q41, Q42, Q45, WEB-5, WEB-7_
- **OC-2**: Disagreement is highly likely on borderline regulatory cases. DEFT2020 already shows 5-annotator score spreads of 3+ points on drug-label pairs (DEFT2020-D14, D15) and moy/vote divergence (DEFT2020-D18, D19, D20). Regulatory affairs reviewers would apply distinct EMA/ANSM normative criteria. — _Sources: DEFT2020-D14, DEFT2020-D18_
- **OC-3**: Annotator demographics are partially documented — DiaMed has 4 annotators including 1 medical expert [Q45]; CLISTER had multiple annotators (count unspecified [Q41]); CAS used Tagex 3 automatic annotation [Q42]; DEFT-2021 was manually annotated with no demographics reported [Q25]. No dataset reports regulatory affairs or legal expertise in annotators. — _Sources: Q25, Q41, Q42, Q45_
- **OC-4**: Recommended — re-annotation by a regulatory affairs / pharmacovigilance pool applying EMA QRD v10.4 and ANSM 'Feuille de style' criteria [WEB-7, WEB-5] would be required for ground-truth alignment. No such re-annotation is documented for any dataset. — _Sources: WEB-7, WEB-5_
- **OC-5**: Aggregation methods risk erasing minority perspectives: CLISTER averages annotator scores [Q41] without surfacing variance; DEFT2020 reports both `moy` and `vote` but they diverge substantially (DEFT2020-D18, D19, D20). For regulatory boundary decisions where minority dissent could indicate compliance risk, averaging is methodologically inadequate. — _Sources: Q41, DEFT2020-D18, DEFT2020-D19_
- **OC-6**: Documented harms: convergent validity violation (no regulatory expertise in annotation); external validity violation (judgments will not generalize to ANSM/EMA review contexts); IAA inadequate or absent for several tasks [Q25, Q45, WEB-18]. — _Sources: Q45, WEB-18, Cross-cutting M2_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'This dataset is manually annotated in two tasks: (i) multi-label classification and (ii) NER.' (p.3)
- [Q41] 'CLISTER...manually annotated by several annotators, who assigned similarity scores ranging from 0 to 5 to each pair. The scores were then averaged together' (p.4)
- [Q42] 'CAS...annotated for POS tagging with 31 classes using automatic annotations through Tagex 3...This evaluation yielded 98% precision.' (p.4)
- [Q45] 'manually annotated by several annotators, one of which is a medical expert...The inter-annotator agreement between the 4 annotators has been computed for two annotation sessions...with 15 different clinical cases assessed per session.' (p.4)
- [Q46] 'Table 4: Inter-annotator agreement statistics. κ is referring to Kappa Cohen and G to Gwet's AC1.' (p.4)

*Web sources:*
- [WEB-5] ANSM 'Feuille de style' and France-specific blue-box requirements define normative regulatory annotation criteria
- [WEB-7] EMA QRD v10.4 defines the standard regulatory annotation reference for SmPC sections
- [WEB-18] HAL 04523267 (2024) confirms cross-dataset IAA in French clinical NLP is unreliable due to methodological heterogeneity

*Dataset analysis:*
- Cross-cutting M2: No regulatory affairs expertise across all benchmark annotation workflows
- DEFT2020-D14, D15, D16, D17: 5-annotator score ranges of 3+ points on drug-label STS pairs
- DEFT2020-D18, D19, D20: moy/vote divergence up to 2.8 points creates ground-truth ambiguity
- CLISTER-D12, D13: Annotators are clinical/research professionals, not regulatory specialists
- DIAMED-D5: IAA on 30 total cases is a narrow validation base for a 739-example corpus
- FRENCHMEDMCQA-D7, D8: Potentially dated regulatory/clinical thresholds in exam-derived ground truth

</details>

**Information gaps:**
- No documented IAA for QUAERO, MORFITT, ESSAI, DEFT-2021 NER specifically
- Demographics of CLISTER annotator pool unspecified
- No published regulatory-affairs annotator pool benchmark for French SmPCs/PILs

**Requires expert verification:**
- Magnitude of likely disagreement between current annotators and regulatory affairs reviewers on borderline drug-label pairs — requires LEEM/ANSM annotator pilot
- Whether ICD-10 chapter labels in DiaMed align or diverge from French hospital coding (PMSI) and ANSM regulatory ICD-10 usage

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Output forms — text labels for classification/NER and continuous scores for STS [Q52, Q54] — are structurally compatible with the deployment's multi-candidate confidence-score and human-review flagging design. Strict reproducibility protocol with 4-run averaging, Student's t-test significance, and documented hyperparameters [Q49, Q51, Q99, Q100] is a real strength, and the SeqEval/IOB2 first-token evaluation [Q52, Q53] provides tokenizer-agnostic measurement. Low-resource sensitivity is probed by varying training data proportions [Q68, Q69, Q70]. However, several gaps are deployment-relevant: (1) the granularity of confidence scoring for triggering mandatory human review is not benchmarked — a parameter the EU AI Act high-risk classification [WEB-13, WEB-14] makes externally consequential; (2) QUAERO sentence-splitting and 6.06–8.90% nested annotation loss [Q37] systematically distorts the most regulation-adjacent dataset (QUAERO-D7, D8, D9, D10); (3) workflow-calibration metrics tied to regulatory human-in-the-loop adjudication design are absent; (4) no model excels uniformly [Q3, Q57, Q58], and DrBERT-FS underperforms specifically on MLC and STS [Q82] — the two output forms most central to deployment.

**Strengths:**
- Standardized evaluation protocol with 4-run averaging, t-test significance, documented hyperparameters [Q49, Q51, Q99, Q100]
- Tokenizer-agnostic SeqEval/IOB2 NER evaluation predicting first token of each word [Q52, Q53]
- Spearman + EDRM dual-metric STS evaluation [Q54]
- Majority-class baseline reported for classification [Q56]
- Low-resource sensitivity probed across 25/50/75/100% training data slices [Q68, Q69]
- Continuous-score output form structurally aligned with deployment's confidence-flagging design

**Checklist:**

- **OF-1**: Output modality (text labels + continuous scores) matches deployment text-only document-processing pipeline. No audio/image/cross-modality requirement [Q44 transcribed before inclusion]. — _Sources: Q52, Q54_
- **OF-2**: Not applicable — deployment is written-document processing; speech output not required.
- **OF-3**: Not applicable — deployment users are domain expert professionals (regulatory affairs, pharmacovigilance) with high literacy; accessibility is not a core concern.
- **OF-4**: Form mismatches harming external validity: (1) no benchmarking of confidence-score granularity for mandatory-review thresholds — relevant under EU AI Act high-risk obligations [WEB-13, WEB-14]; (2) QUAERO preprocessing artifacts (sentence-splitting + 6.06–8.90% nested annotation loss [Q37]; QUAERO-D7, D8, D9, D10) degrade the most regulation-adjacent measurement; (3) no workflow-level metric (e.g., precision at threshold, calibration, false-flag rate) tied to the regulatory adjudication loop; (4) ESSAI/CAS use silver-standard POS via TreeTagger/Tagex [Q42, Q43] introducing systematic noise. — _Sources: Q37, Q82, QUAERO-D7, WEB-13, WEB-14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q37] '6.06% of the annotations on EMEA and 8.90% on MEDLINE...we decided to split these documents into sentences.' (p.3)
- [Q49] 'we have integrated all the training details, including hyperparameters, in Appendix A.' (p.5)
- [Q51] 'All the models are fine-tuned regarding a strict protocol...averaging the scores from four separate runs...statistical significance computed using Student's t-test.' (p.5)
- [Q52] 'we chose the SeqEval...metric in conjunction with the IOB2 format and the training of all the models to predict only the label on the first token of each word' (p.6)
- [Q54] 'For STS tasks, the models' performance was assessed using two metrics: (1) the Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM)' (p.6)
- [Q57] 'no single model outperforms the rest in all application scenarios.' (p.6)
- [Q82] 'the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS.' (p.8)

*Web sources:*
- [WEB-13] ANSM and CNIL jointly enforce digital health AI compliance in France
- [WEB-14] EU AI Act classifies medical-purpose AI as high-risk (Annex III) with transparency, oversight, accountability obligations

*Dataset analysis:*
- Cross-cutting M7: QUAERO EMEA preprocessing artifacts destroy regulatory document structure (QUAERO-D7, D8, D9, D10)
- PXCORPUS-D14, D15: Full NER tag ontology not surfaced in HF metadata — output form documentation gap
- DEFT2020-D18, D19, D20: moy/vote divergence creates ambiguity about which output score anchors threshold decisions

</details>

**Information gaps:**
- Mandatory-review confidence threshold not benchmarked
- No calibration / reliability-diagram analysis reported for STS scores
- EU AI Act-aligned auditability and transparency metrics not part of evaluation protocol

**Requires expert verification:**
- What confidence-score threshold and false-flag rate would satisfy ANSM/CNIL human-oversight obligations under the EU AI Act high-risk classification

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** NER label taxonomies (UMLS, MeSH, ICD-10) lack regulatory entity classes; STS 0–5 Likert scale [Q22, Q41] empirically fails to distinguish legally significant differences (DEFT2020-D10, CLISTER-D8, D9)

**Recommendation:** Design a regulatory NER schema with INN, ATC, excipient, MedDRA, contraindication qualifier, posology element, and SmPC-section classes (using DART [WEB-15] as model). Develop a regulatory-equivalence STS rubric calibrated to legal significance — e.g., binary 'regulatorily equivalent / not equivalent' with required justification labels — with thresholds elicited from regulatory affairs experts.

### Output Content ⚠

**Gap:** No constituent dataset documents regulatory affairs, pharmacovigilance, or legal expertise in annotation; DiaMed IAA covers only 30 cases; CAS uses silver-standard automatic annotation; DEFT-2021 reports no IAA

**Recommendation:** Re-annotate a representative sample of QUAERO EMEA, DEFT-2020 drug-label pairs, and DEFT-2021 NER with a regulatory affairs / pharmacovigilance / legal expert panel applying EMA QRD v10.4 [WEB-7] and ANSM normative criteria [WEB-5]. Compute IAA and surface annotator-level variance rather than averaging (addressing CLISTER and DEFT2020 aggregation concerns).

### Input Ontology ⚠

**Gap:** No tasks derived from current-format EMA SmPCs, PILs, CTD modules, ANSM 'Feuille de style' submissions, or PSURs; closest analogue is Italian DART with no French equivalent

**Recommendation:** Construct a French regulatory NLP evaluation set modeled on Italian DART [WEB-15] using publicly available SmPCs and PILs from the EMA product information register and ANSM publications, structured according to QRD v10.4 [WEB-7] sections 4.1–4.9. Include task types: section-typed NER, regulatory-equivalence STS, contraindication detection, and SmPC structural parsing.

### Input Content

**Gap:** Regulatory entity vocabulary (INNs, ATC codes, excipients, MedDRA, contraindication qualifiers) is incidentally present (e.g., QUAERO-D3) but not consistently annotated, and substantial irrelevant content (encyclopedic, veterinary, sub-Saharan African) dilutes representativeness

**Recommendation:** Curate a metropolitan-French regulatory text corpus covering INN/ATC/excipient/MedDRA vocabulary with explicit annotations; add a DROM tropical-pathology subset (dengue, chikungunya, paludisme) for secondary deployment scope; filter out construct-irrelevant content (e.g., DEFT2020 non-medical pairs, MORFITT veterinary content) when using DrBenchmark for screening.

### Input Form

**Gap:** Long SmPC documents exceed 512-token limits of standard MLMs; PxCorpus spoken-language transcription artifacts (PXCORPUS-D16, D17, D18) are unrepresentative of written regulatory text

**Recommendation:** Evaluate net-new long-document models (DrLongformer-CP [WEB-16]) and updated encoders (CamemBERT 2.0 [WEB-28], AliBERT) on the regulatory NLP supplementary set; deprioritize PxCorpus as an evaluation signal for the deployment.

### Output Form

**Gap:** Confidence-score granularity and mandatory-review thresholds are not benchmarked; QUAERO sentence-splitting and 6.06–8.90% nested annotation loss [Q37] systematically distorts the most regulation-adjacent dataset

**Recommendation:** Add workflow-calibration metrics — calibration curves, precision-at-threshold, false-flag rate — aligned with EU AI Act high-risk auditability obligations [WEB-13, WEB-14]. Re-process QUAERO EMEA without sentence-splitting using a long-document model such as DrLongformer-CP [WEB-16] to preserve nested entity structure relevant to regulatory compliance.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "It encompasses 20 diversified tasks, including named-entity recognition, part-of-speech tagging, question-answering, semantic textual similarity, and classification." |
| Q2 | 1 | output_form | "We evaluate 8 state-of-the-art pre-trained masked language models (MLMs) on general and biomedical-specific data, as well as English specific MLMs to assess their cross-lingual capabilities." |
| Q3 | 1 | output_ontology | "Our experiments reveal that no single model excels across all tasks, while generalist models are sometimes still competitive." |
| Q4 | 1 | input_ontology | "These tasks encompass part-of-speech (POS) tagging, named-entity recognition (NER), classification, question-answering (QA), and semantic textual similarity (STS)." |
| Q5 | 1 | input_ontology | "Although the French language is generally considered as well-endowed, it is notably lacking in evaluation resources within the biomedical field." |
| Q6 | 1 | output_form | "We also perform a quantitative study of 8 pre-trained state-of-the-art masked language models" |
| Q7 | 1 | output_content | "Yanis Labrak, Adrien Bazoge, Oumaima El Khettari, Mickael Rouvier, Pacôme Constant dit Beaufils, Natalia Grabar, Béatrice Daille, Solen Quiniou, Emmanuel Morin, Pierre-Antoine Gourraud and Richard Dufour" |
| Q8 | 1 | output_content | "LIA, Avignon Université, Zenidoc, Nantes Université, CHU Nantes, Clinique des données, INSERM, CIC 1413, École Centrale Nantes, CNRS, LS2N, UMR 6004, Service de Neuroradiologie diagnostique et interventionnelle, l'institut du thorax, UMR 8163 – STL CNRS, Université de Lille" |
| Q9 | 1 | input_ontology | "The biomedical field remains an area with relatively few proposed benchmarks, mainly for English and Chinese, facilitating the availability of many biomedical models in these two languages." |
| Q10 | 2 | input_ontology | "In the case of specialized domains, general benchmarks may not adequately evaluate the performance of in-domain models." |
| Q11 | 2 | input_ontology | "Specifically, within the biomedical domain, only few benchmarks have been proposed, and they primarily focus on few languages." |
| Q12 | 2 | input_content | "For instance, platforms like BLURB (Gu et al., 2021) and BLUE (Peng et al., 2019) predominantly offer benchmarks for English, while CBLUE (Zhang et al., 2022a) caters to the Chinese language." |
| Q13 | 2 | input_ontology | "BLURB integrates 13 tasks, including NER, information and relation extraction, sentence similarity, text classification, and QA." |
| Q14 | 2 | input_ontology | "BLUE encompasses 10 tasks, such as NER, sentence similarity, relation extraction, text classification, and inference." |
| Q15 | 2 | input_ontology | "CBLUE covers 8 tasks, including NER, information extraction, text and intent classification, sentence similarity, and query relevance." |
| Q16 | 2 | input_ontology | "To our knowledge, aside the multilingual benchmark BigBIO (Fries et al., 2022) which includes only 4 corpora for French and is initially intended for generative text completion under zero-shot scenario, no large benchmark specialized in the French biomedical field exists." |
| Q17 | 2 | input_ontology | "Our proposed benchmark comprises 20 French biomedical language understanding tasks, one of which is specifically created for this benchmark." |
| Q18 | 2 | input_ontology | "A variety of tasks with different requirements and objectives: Part-of-Speech (POS) tagging, Multi-class, Multi-label and Intent classification, Named-Entity Recognition (NER), Multiple-Choice Question-Answering (MCQA), and Semantic Textual Similarity (STS)." |
| Q19 | 2 | input_content | "A diverse range of data origins: Scientific literature, clinical trials, clinical cases, speech transcriptions, and more as described in Table 2." |
| Q20 | 2 | input_ontology | "Please note that within DrBenchmark, we include classical tasks like NER and POS tagging, as well as more specific and challenging tasks like MCQA and multi-label classification." |
| Q21 | 3 | input_content | "DEFT-2020 (Cardon et al., 2020) contains clinical cases, encyclopedia and drug labels introduced in the 2020 edition of an annual French Text Mining Challenge, called DEFT, and annotated for two tasks: (i) textual similarity and (ii) multi-class classification." |
| Q22 | 3 | output_ontology | "The first task aims at identifying the degree of similarity within pairs of sentences, from 0 (the less similar) to 5 (the most similar)." |
| Q23 | 3 | input_ontology | "The second task consists in identifying, for a given sentence, the most similar sentence among three sentences provided." |
| Q24 | 3 | input_content | "DEFT-2021 (Grouin et al., 2021) is a subset of 275 clinical cases taken from the 2019 edition of DEFT." |
| Q25 | 3 | output_content | "This dataset is manually annotated in two tasks: (i) multi-label classification and (ii) NER." |
| Q26 | 3 | input_ontology | "The multi-label classification task focuses on identifying the patient's clinical profile based on the diseases, signs, or symptoms mentioned in the clinical cases." |
| Q27 | 3 | output_ontology | "The dataset is annotated with 23 axes from Chapter C of the Medical Subject Headings (MeSH)." |
| Q28 | 3 | output_ontology | "The second task involves fine-grained information extraction for 13 types of entities (more detail in Appendix B.7)." |
| Q29 | 3 | input_content | "E3C (Magnini et al., 2020) is a multilingual dataset of clinical cases annotated for the NER task." |
| Q30 | 3 | output_ontology | "It consists of two types of annotations (more detail in Appendix B.4): (i) clinical entities (e.g., pathologies), (ii) temporal information and factuality (e.g., events)." |
| Q31 | 3 | input_form | "While the dataset covers 5 languages, only the French portion is retained for the benchmark." |
| Q32 | 3 | input_form | "Since the dataset does not come with pre-defined subsets, we performed a 70 / 10 / 20 random split, as described in Table 3." |
| Q33 | 3 | input_content | "The QUAERO French Medical Corpus (Névéol et al., 2014), simply referred to as QUAERO in this paper, contains annotated entities and concepts for NER tasks." |
| Q34 | 3 | input_content | "The dataset covers two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE." |
| Q35 | 3 | output_ontology | "10 entity categories corresponding to the UMLS Semantic Groups (Lindberg et al., 1993) were annotated (more detail in Appendix B.3)." |
| Q36 | 3 | input_content | "In total, 26,409 entity annotations were mapped to 5,797 unique UMLS concepts." |
| Q37 | 3 | output_form | "Due to the presence of nested entities in annotations, we simplified the evaluation process by retaining only annotations at the higher granularity level from the BigBio (Fries et al., 2022) implementation, following the approach described in Touchent et al. (2023), which translates into an average loss of 6.06% of the annotations on EMEA and 8.90% on MEDLINE. Additionally, considering that some documents from EMEA exceed the maximum input sequence length that most current language models can handle, we decided to split these documents into sentences." |
| Q38 | 4 | input_content | "MorFITT (Labrak et al., 2023) is a multi-label dataset annotated with medical specialties. It contains 3,624 biomedical abstracts from PMC Open Access. It has been annotated across 12 medical specialties (more detail in Appendix B.5), for a total of 5,116 annotations." |
| Q39 | 4 | input_content | "FrenchMedMCQA (Labrak et al., 2022) is a Multiple-Choice Question-Answering (MCQA) dataset for biomedical domain. It contains 3,105 questions coming from real exams of the French medical specialization diploma in pharmacy, integrating single and multiple answers. The first task consists of automatically identifying the set of correct answers among the 5 proposed for a given question. The second task consists of identifying the number of answers (between 1 and 5) supposedly correct for a given question." |
| Q40 | 4 | input_content | "Mantra-GSC (Kors et al., 2015) is a multilingual dataset annotated for biomedical NER. From the 5 languages covered, we included only the French subset in this benchmark. The dataset is obtained from 3 sources which have been partitioned to be evaluated separately by 2 annotation schemes (more detail in Appendix B.6): Medline (11 classes), and EMEA and Patents (10 classes). The sources cover different types of documents (biomedical abstracts/titles, drug labels and patents). To ensure evaluation consistency, we randomly split the dataset into 3 subsets: 70% for training, 10% for validation, and 20% for testing." |
| Q41 | 4 | output_content | "CLISTER (Hiebel et al., 2022) is a French clinical cases Semantic textual similarity (STS) dataset of 1,000 sentence pairs manually annotated by several annotators, who assigned similarity scores ranging from 0 to 5 to each pair. The scores were then averaged together to obtain a floating-point number representing the overall similarity. The objective of this dataset is to develop models that can automatically predict a similarity score that closely aligns with the reference score based solely on the two sentences provided." |
| Q42 | 4 | output_content | "CAS (Grabar et al., 2018) comprises 3,790 clinical cases that have been annotated for POS tagging with 31 classes using automatic annotations through Tagex 3, with an evaluation conducted by comparing the automatic outputs against manual annotations. This evaluation yielded 98% precision. Since the dataset does not come with predefined subsets, we made the decision to randomly split it into 3 subsets of 70%, 10% and 20% of the total data for training, validation and test respectively." |
| Q43 | 4 | input_content | "ESSAI (Dalloux et al., 2021) contains 7,247 clinical trial protocols annotated in 41 POS tags using TreeTagger (Schmid, 1994). As the dataset was not originally divided into 3 subsets, we applied the same procedure as on the CAS corpus." |
| Q44 | 4 | input_ontology | "PxCorpus (Kocabiyikoglu et al., 2022) is a spoken language understanding dataset in the domain of medical drug prescription transcripts. It includes 4 hours (1,981 recordings) of transcribed and annotated dialogues focused on drug prescriptions. The recordings were manually transcribed and semantically annotated. The first task involves classifying the textual utterances into one of the 4 intent classes (prescribe, replace, negate, none). The second task is a NER task where each word in a sequence is classified into one of 38 classes, such as drug, dose, or mode (more detail in Appendix B.9)." |
| Q45 | 4 | output_content | "DiaMed is an original dataset created specifically for DrBenchmark. It comprises 739 new French clinical cases collected from an open source journal (The Pan African Medical Journal). The cases have been manually annotated by several annotators, one of which is a medical expert, into 22 chapters of the International Classification of Diseases, 10th Revision (ICD-10) (Wor, 2019). These chapters provide a general description of the type of injury or disease. To ease the annotation process, only label at the chapter level were used (more detail in Appendix B.8). The inter-annotator agreement between the 4 annotators has been computed for two annotation sessions (see Table 4), with 15 different clinical cases assessed per session." |
| Q46 | 4 | output_content | "Table 4: Inter-annotator agreement statistics. κ is referring to Kappa Cohen and G to Gwet's AC1." |
| Q47 | 4 | input_form | "To facilitate the adoption of DrBenchmark and ensure consistency in implementations, we have de-" |
| Q48 | 5 | input_form | "We developed a practical toolkit based on the HuggingFace Datasets library (Lhoest et al., 2021). This toolkit includes data loaders that adhere to normalized schemes and predefined data splits. It also provides pre-training and evaluation scripts for each of the tasks, utilizing the HuggingFace Transformers (Wolf et al., 2020) and PyTorch (Paszke et al., 2019) libraries." |
| Q49 | 5 | output_form | "For further guidance, we have integrated all the training details, including hyperparameters, in Appendix A. This information will help users to reproduce and customize the experiments conducted with DrBenchmark." |
| Q50 | 5 | output_form | "To guarantee fair comparison, we focus exclusively on pre-trained masked language models (MLMs) in this study. These MLMs are based on BERT-like architectures (Devlin et al., 2019)." |
| Q51 | 5 | output_form | "All the models are fine-tuned regarding a strict protocol using the same hyperparameters for each downstream task. The reported results are obtained by averaging the scores from four separate runs, thus ensuring robustness and reliability. We also report statistical significance computed using Student's t-test." |
| Q52 | 6 | output_form | "To ensure a fair and consistent comparison among systems for sequence-to-sequence tasks such as POS tagging and NER, we chose the SeqEval (Nakayama, 2018) metric in conjunction with the IOB2 format and the training of all the models to predict only the label on the first token of each word as mentioned by Touchent et al. (2023)." |
| Q53 | 6 | output_form | "It provides a tokenizer-agnostic evaluation and mitigates any correlation between models' performances and the tokenization process." |
| Q54 | 6 | output_form | "For STS tasks, the models' performance was assessed using two metrics: (1) the Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM), as defined by the original authors of the DEFT-2020 dataset (Cardon et al., 2020)." |
| Q55 | 6 | output_form | "In Section 5.1, we compare the results obtained by each model within DrBenchmark, which permits to position a wide range of state-of-the-art models in the biomedical field across various NLP tasks." |
| Q56 | 6 | output_form | "The results of the 8 models are reported in Table 6 and compared to a baseline obtained by considering the majority class for all predictions." |
| Q57 | 6 | output_ontology | "Overall, although we might anticipate certain models to excel in all tasks, we discovered that no single model outperforms the rest in all application scenarios." |
| Q58 | 6 | output_form | "Interestingly, most of the models examined manage to secure the top position in at least one of the French biomedical downstream tasks studied." |
| Q59 | 6 | output_form | "The only exception pertains to the cross-lingual generalist model (XLM-RoBERTa), which manages to reach the second-best position on several tasks." |
| Q60 | 6 | output_form | "French biomedical language models (DrBERT-FS, DrBERT-CP, CamemBERT-bio), presumed to be the most aligned with the nature of the data of the benchmark, exhibit indeed superior performance across many tasks." |
| Q61 | 6 | output_form | "More precisely, DrBERT-FS achieves the highest performance in 8 tasks, DrBERT-CP in 5 tasks, and CamemBERT-bio in 2 tasks." |
| Q62 | 6 | output_form | "This indicates that domain and language-specialized models achieve the best performance in up to 75% of the DrBenchmark downstream tasks." |
| Q63 | 6 | output_form | "Generalist models (CamemBERT, CamemBERTa, FlauBERT and XLM-RoBERTa) are more suitable for tasks that require extensive linguistic knowledge but may not perform as well as specialized models nor even reach their level of performance." |
| Q64 | 6 | output_form | "We observe that all generalist models obtain better performance only on 4 out of the 20 tasks, but still remain competitive on most tasks." |
| Q65 | 6 | output_form | "Furthermore, our experiments with DrBERT-FS indicate that biomedical models may require less pre-training data compared to generalist ones." |
| Q66 | 6 | output_form | "However, it is important to note that this observation requires further confirmation." |
| Q67 | 6 | output_form | "In some tasks, biomedical models that undergo continual pre-training from a generalist model, such as CamemBERT-bio, can prove to be the most effective, underscoring the value of pre-training on generalist data." |
| Q68 | 7 | input_form | "For this purpose, we conducted experiments by varying the amount of training data during the fine-tuning process by randomly choosing four percentages of the training data: 25%, 50%, 75% and 100%." |
| Q69 | 7 | output_form | "To make the experiment as fair as possible, we did four runs for each percentage, model and dataset combination." |
| Q70 | 7 | output_form | "The validation and test sets have not been changed for the sake of comparison." |
| Q71 | 7 | output_form | "We observe that on certain datasets, some models capture information more quickly than others, like in Figures 1b, 1f and 1a." |
| Q72 | 7 | output_form | "Unsurprisingly, in almost all scenarios, having the complete training set yields better results than having only 25% of it." |
| Q73 | 7 | output_form | "However, all the models based on CamemBERT face difficulties in corpora with limited amount of data, such as MantraGSC Patents, where they fail to generate labels other than 'O'." |
| Q74 | 7 | output_form | "On the other hand, in the same low-resource scenarios, CamemBERTa models exhibit greater robustness and achieve superior performance." |
| Q75 | 8 | input_form | "Tokenizers play a crucial role in MLMs by utilizing size-limited vocabularies to split texts into sub-units, aiming to handle out-of-vocabulary (OOV) words." |
| Q76 | 8 | input_content | "Due to variations in the training data, vocabularies differ across different models, as illustrated in Figure 2." |
| Q77 | 8 | input_form | "So far, there has been a prevailing notion in the community that excessive segmentation of words in tokenization leads to a loss of morphological form and semantic meaning, introducing noise and adversely affecting performance (Church, 2020; Hofmann et al., 2021; Bostrom and Durrett, 2020)." |
| Q78 | 8 | output_form | "However, our experiments, as shown in Table 7, reveal that FlauBERT is the model with the least word segmentation (1.43 in average), while DrBERT-CP tends to have the highest average segmentation (1.90 in average)." |
| Q79 | 8 | output_form | "Surprisingly, when comparing the performance of these two models on the benchmark tasks, we observe that DrBERT-CP outperforms FlauBERT on 16 out of the 20 tasks, thus contradicting previous conclusions drawn by the community." |
| Q80 | 8 | input_form | "Yet, tokenization, as it is currently done in MLMs, seems to play a minor role in the performance of systems." |
| Q81 | 8 | input_ontology | "Table 8 summarizes the results obtained on average by the considered MLMs when aggregating the tasks into one of the five designated categories: POS, NER, MCQA, MCC (Multi-class classification), MLC (Multi-label classification), or STS tasks." |
| Q82 | 8 | output_ontology | "Upon analyzing the average performance by task category, it becomes evident that the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS." |
| Q83 | 9 | input_ontology | "In this paper, we introduced DrBenchmark, the first large language understanding benchmark tailored for the French biomedical domain." |
| Q84 | 9 | input_ontology | "We conducted a qualitative evaluation of 8 state-of-the-art masked language models (MLMs) on this comprehensive benchmark, encompassing 20 diverse downstream tasks." |
| Q85 | 9 | output_form | "Our findings illuminate the limitations of generalist models in tackling complex biomedical tasks, emphasizing the importance of employing domain-specific models to achieve peak performance." |
| Q86 | 9 | output_form | "We have observed that several biomedical tasks in DrBenchmark exhibit relatively poor performance, even when utilizing specialized biomedical models." |
| Q87 | 9 | output_ontology | "We postulate that the models examined in this study, here state-of-the-art MLMs, may not be the most effective choices for specific tasks such as question-answering or multi-label classification." |
| Q88 | 9 | output_form | "The quantitative study we conducted on the PLMs requires further in-depth analysis to comprehend the impact of different parameters." |
| Q89 | 9 | input_form | "Firstly, we investigated the influence of tokenizers based on the average number of sub-tokens they produce per word." |
| Q90 | 9 | input_form | "Various tokenization algorithms are employed, depending on the model under examination." |
| Q91 | 9 | output_form | "The size of the data has not been thoroughly investigated, particularly the significance of the pre-training data size, especially specialized data in the biomedical field." |
| Q92 | 9 | output_form | "Although the benchmark is easily reproducible and customizable, it required a substantial amount of computational power to execute all runs." |
| Q93 | 9 | output_form | "We utilized approximately 2,500 hours on V100 GPUs from the Jean-Zay supercomputer to complete the quantitative study." |
| Q94 | 9 | output_form | "According to the Jean Zay supercomputer documentation, the total environmental cost is estimated to be equivalent to 647,500 Wh or 36.9 kgCO2eq/kWh, based on the carbon intensity of the energy grid mentioned in the BLOOM environmental cost study conducted on Jean Zay (Luccioni et al., 2022)." |
| Q95 | 9 | output_content | "All code for DrBenchmark is released under the MIT License." |
| Q96 | 9 | input_content | "The licensing for all datasets remains unchanged from the original sources, and DrBenchmark has no intention of redistributing these datasets." |
| Q97 | 9 | output_content | "This work was performed using HPC resources from GENCI-IDRIS (Grant 2022-AD011013061R1 and 2022-AD011013715) and from CCIPL (Centre de Calcul Intensif des Pays de la Loire)." |
| Q98 | 9 | output_content | "This work was financially supported by ANR MALADES (ANR-23-IAS1-0005), ANR AIBy4 (ANR-20-THIA-0011) and Zenidoc." |
| Q99 | 13 | output_form | "For the experiments, we utilize the following hyperparameters that yield optimal performance from the models." |
| Q100 | 13 | output_form | "To mitigate overfitting, we locally save the best model based on its validation metric." |
| Q101 | 14 | output_ontology | "INT, PRO:DEM, VER:impf, VER:ppre, PRP:det, KON, VER:pper, PRP, PRO:IND, VER:simp, VER:con, SENT, VER:futu, PRO:PER, VER:infi, ADJ, NAM, NUM, PUN:cit, PRO:REL, VER:subi, ABR, NOM, VER:pres, DET:ART, VER:cond, VER:subp, DET:POS, ADV, SYM and PUN." |
| Q102 | 14 | output_ontology | "INT, PRO:POS, PRP, SENT, PRO, ABR, VER:pres, KON, SYM, DET:POS, VER:, PRO:IND, NAM, ADV, PRO:DEM, NN, PRO:PER, VER:pper, VER:ppre, PUN, VER:simp, PREF, NUM, VER:futu, NOM, VER:impf, VER:subp, VER:infi, DET:ART, PUN:cit, ADJ, PRP:det, PRO:REL, VER:cond and VER:subi." |
| Q103 | 14 | output_ontology | "O, GEOG, PHEN, DISO, ANAT, OBJC, PHYS, PROC, DEVI, CHEM and LIVB" |
| Q104 | 14 | output_ontology | "Clinical: O, and CLINENTITY. Temporal: O, EVENT, ACTOR, BODYPART, TIMEX3 and RML" |
| Q105 | 14 | output_ontology | "microbiology, etiology, virology, physiology, immunology, parasitology, genetics, chemistry, veterinary, surgery, pharmacology and psychology" |
| Q106 | 14 | output_ontology | "Medline: ANAT, PROC, CHEM, PHYS, GEOG, DEVI, LIVB, OBJC, DISO, PHEN and O. EMEA and Patents: ANAT, PROC, CHEM, PHYS, DEVI, LIVB, OBJC, DISO, PHEN and O." |
| Q107 | 14 | output_ontology | "Multi-label Classification: immunitaire (immunology), endocriniennes (endocrinology), blessures (injury), chimiques (chemicals), etatsosy (signs and symptoms), nutritionnelles (nutrition), infections (infections), virales (virology), parasitaires (parasitology), tumeur (oncology), osteomusculaires (osteomuscular disorders), stomatognathique (stomatology), digestif (digestive system disorders), respiratoire (respiratory system disorders), ORL (otorhinolaryngologic diseases), nerveux (nervous system disorders), oeil (eye diseases), homme (male genital diseases), femme (female genital diseases), cardiovasculaires (cardiology), hemopathies (hemic and lymphatic diseases), genetique (genertic disorders) and peau (dermatology)." |
| Q108 | 14 | output_ontology | "Named-entity recognition: O, ANATOMY, DATE, DOSAGE, DURATION, MEDICAL EXAM, FREQUENCY, MODE, MOMENT, PATHOLOGY, SOSY, SUBSTANCE, TREATMENT and VALUE" |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://iaocr.com/en/blog/french-regulatory-authority-for-clinical-trials |
| WEB-2 | https://pharma-blue.com/glossary/ansm/ |
| WEB-3 | https://www.glassdoor.com/Job/france-regulatory-affairs-jobs-SRCH_IL.0,6_IN86_KO7,25.htm |
| WEB-4 | https://www.lexology.com/library/detail.aspx?g=9eb5298b-3d96-448a-b563-7135317d423c |
| WEB-5 | https://www.pharmalex.com/thought-leadership/blogs/the-complex-landscape-of-french-regulatory-affairs/ |
| WEB-6 | https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/product-information-requirements/product-information-qrd-templates-human |
| WEB-7 | https://www.ema.europa.eu/en/documents/template-form/qrd-product-information-template-version-104-highlighted_en.pdf |
| WEB-8 | https://www.hma.eu/human-medicines/cmdh/templates/qrd.html |
| WEB-9 | https://pharmacores.com/smpc-summary-of-product-characteristics/ |
| WEB-10 | https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/product-information-requirements/product-information-reference-documents-guidelines-0 |
| WEB-11 | https://cms.law/en/int/expert-guides/cms-expert-guide-to-digital-health-apps-and-telemedicine/france |
| WEB-12 | https://intuitionlabs.ai/articles/compliance-frameworks-pharmaceutical-it-comparative-analysis |
| WEB-13 | https://iclg.com/practice-areas/digital-health-laws-and-regulations/france |
| WEB-14 | https://www.europeanpharmaceuticalreview.com/article/264445/ai-act-data-governance-and-compliance-strategy-implications-in-pharma/ |
| WEB-15 | https://arxiv.org/abs/2510.18475 |
| WEB-16 | https://arxiv.org/html/2402.16689v1 |
| WEB-17 | https://arxiv.org/html/2402.13432 |
| WEB-18 | https://hal.science/hal-04523267 |
| WEB-19 | https://www.statista.com/topics/10409/overseas-france/ |
| WEB-20 | https://en.wikipedia.org/wiki/Overseas_departments_and_regions_of_France |
| WEB-21 | https://www.worldatlas.com/geography/french-overseas-territories.html |
| WEB-22 | https://www.lcanews.com/en/frances-overseas-territories-explained/ |
| WEB-23 | https://www.statista.com/statistics/1320629/population-french-overseas-regions/ |
| WEB-24 | https://www.twobirds.com/en/insights/2026/france/ai-liability-in-light-of-the-new-2024-pld-expanded-liability-challenging-defences-and-new-evidentiar |
| WEB-25 | https://practiceguides.chambers.com/practice-guides/digital-healthcare-2025/france/trends-and-developments |
| WEB-26 | https://arxiv.org/abs/2306.15550 |
| WEB-27 | https://arxiv.org/pdf/2304.00958 |
| WEB-28 | https://arxiv.org/html/2411.08868v1 |

---

### Dataset Analysis

## Dataset Analysis Report

**Benchmark:** DrBenchmark — A Large Language Understanding Benchmark for French Biomedical NLP
**Datasets analyzed:** 11 datasets (QUAERO, FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC, E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI)
**Analysis date:** 2025-07-11

---

### Per-Dataset Fit Assessment

#### DrBenchmark/QUAERO (EMEA config)
- **Task:** NER (token classification) on EMEA drug leaflets and MEDLINE biomedical titles
- **Deployment fit:** Partial — QUAERO is the closest any dataset comes to the deployment's primary document genre (regulatory drug product information). EMEA drug leaflet content is present with characteristic posology, contraindication, excipient list, and ATC code language (QUAERO-D1, QUAERO-D2, QUAERO-D3). However, critical gaps prevent strong fit.
- **Key concerns:**
  - **CRITICAL (IO, OO):** UMLS Semantic Group taxonomy (CHEM, DISO, PROC, etc.) conflates INNs, excipients, ATC codes, and chemical reagents under a single label; no regulatory sub-type distinction exists (QUAERO-D4, QUAERO-D5, QUAERO-D6). ATC codes are textually present but entirely unlabeled.
  - **MAJOR (IF, OF):** Sentence-splitting of long EMEA documents produces null sentences, isolated header fragments, and mixed-content token sequences — systematic preprocessing artifacts that corrupt regulatory document structure (QUAERO-D7, QUAERO-D8, QUAERO-D9, QUAERO-D10). 6.06% of nested annotations are lost per benchmark documentation.
  - **MAJOR (OC, OO):** Safety warnings and contraindications are present (QUAERO-D15, QUAERO-D16) but contraindication relationships and population qualifiers are not captured as distinct entity types; annotations reflect biomedical NLP researcher judgment, not regulatory affairs expertise.
  - **MINOR (IF):** Non-French tokens present from multi-country regulatory leaflet appendices (QUAERO-D11, QUAERO-D12).
  - **MINOR (IC):** Vocabulary coverage is limited to a small set of brand products (Refludan, TYSABRI, Prialt); broader regulatory deployment requires coverage across hundreds of active substances.

#### DrBenchmark/FrenchMedMCQA
- **Task:** Multiple-choice QA from French pharmacy specialization diploma exams
- **Deployment fit:** Weak — the dataset is exclusively MCQA format; it contributes neither NER nor STS task types central to the deployment. Regulatory entity vocabulary (INNs, ATC codes, posology templates, EMA phrasing) does not appear as labeled structured content.
- **Key concerns:**
  - **MAJOR (IO):** MCQA format is irrelevant to the deployment's NER and STS pipeline; no task-type alignment exists.
  - **MAJOR (IC):** Drug names appear only as answer options in pharmacological knowledge questions, not as labeled regulatory entities (FRENCHMEDMCQA-D5, FRENCHMEDMCQA-D6). Single instance of SmPC-adjacent terminology ("résumé des caractéristiques du produit") is definitional only (FRENCHMEDMCQA-D1).
  - **MAJOR (OC):** Ground truth reflects pharmacy licensing exam keys — authoritative for academic pharmacological facts but disconnected from EMA/ANSM compliance judgment (FRENCHMEDMCQA-D9).
  - **MINOR (OC):** Some questions may reflect dated regulatory status (hepatitis B vaccination obligations, WHO hypertension thresholds) (FRENCHMEDMCQA-D7, FRENCHMEDMCQA-D8).

#### DrBenchmark/DEFT2020
- **Task:** Semantic textual similarity (Task 1, 0–5 scale) and multi-class classification (Task 2)
- **Deployment fit:** Partial — DEFT2020 is the most relevant STS dataset for the deployment context because it includes drug labeling text pairs (contraindications, posology warnings, excipient instructions) from the DEFT 2020 challenge. However, the multi-genre design introduces substantial irrelevant content, and the scoring calibration is not suitable for regulatory equivalence.
- **Key concerns:**
  - **MAJOR (IO, IC):** Large fraction of non-medical encyclopedic content (beekeeping, sports, WWII history, railway infrastructure) has zero regulatory relevance (DEFT2020-D6, DEFT2020-D7, DEFT2020-D8, DEFT2020-D9). Drug-label pairs are real and deployment-relevant (DEFT2020-D1, DEFT2020-D2, DEFT2020-D3) but cannot be isolated without filtering.
  - **MAJOR (OO, OC):** The scoring rubric does not distinguish legally significant small differences from surface paraphrases. Omission of "sous stricte surveillance médicale" scores 3.6/5 (DEFT2020-D10); removal of a mechanistic qualifier scores 3.8 (DEFT2020-D11). These represent direct calibration failures for regulatory equivalence scoring.
  - **MAJOR (OC):** High annotator disagreement (>3 point range across 5 annotators) on drug-label pairs is documented (DEFT2020-D14, DEFT2020-D15); annotators are general rather than regulatory specialists.
  - **MAJOR (OO):** The `moy` and `vote` fields diverge substantially on multiple examples (up to 2.8-point gap), creating ambiguity about which score represents ground truth for model training and threshold-setting (DEFT2020-D18, DEFT2020-D19, DEFT2020-D20).

#### DrBenchmark/MORFITT
- **Task:** Multi-label medical specialty classification of biomedical research abstracts (12 specialty classes)
- **Deployment fit:** Weak — the dataset is exclusively scientific research abstracts classified by medical specialty. Neither genre nor label taxonomy aligns with the deployment's NER/STS regulatory compliance tasks.
- **Key concerns:**
  - **CRITICAL (IO, IC):** All content is research literature; no regulatory document genre present (MORFITT-D1, MORFITT-D2, MORFITT-D3).
  - **MAJOR (IC):** Significant international geographic provenance (Canada, Jordan, Egypt, Saudi Arabia, Japan, China) unrepresentative of metropolitan French regulatory text (MORFITT-D4 through MORFITT-D10).
  - **MAJOR (IO):** Veterinary medicine content included (MORFITT-D11, MORFITT-D12, MORFITT-D13, MORFITT-D14); irrelevant to human pharmaceutical regulatory compliance.
  - **MAJOR (OO):** 12-class specialty taxonomy has no alignment with EMA/ANSM regulatory entity types.
  - **MINOR (IF):** Some abstracts are translations from English, introducing register differences from native regulatory French (MORFITT-D16, MORFITT-D17).
  - **INFO:** One Chikungunya abstract relevant to overseas territories is present (MORFITT-D15) but as research content, not regulatory documentation.

#### DrBenchmark/CLISTER
- **Task:** STS on French clinical case sentence pairs (0–5 scale)
- **Deployment fit:** Weak — while CLISTER is an STS task, all content derives from clinical case reports. No regulatory document pairs exist, and the scoring calibration is insensitive to the numeric and lexical differences that carry legal consequence in EMA/ANSM labeling.
- **Key concerns:**
  - **CRITICAL (IO, IC):** All sentence pairs are clinical case prose; zero examples from SmPCs, patient leaflets, or regulatory submissions (CLISTER-D1, CLISTER-D2, CLISTER-D3).
  - **MAJOR (OO):** Scoring scale is insensitive to factually meaningful numeric differences: a twofold difference in a biological value scores 4.0 (CLISTER-D8); a 15-fold PSA difference scores 3.75 (CLISTER-D9); a 2 vs. 4.5 year follow-up difference scores 4.0 (CLISTER-D10). This calibration failure directly undermines regulatory equivalence checking.
  - **MAJOR (OC):** Annotators are clinical/research professionals; no regulatory affairs expertise confirmed. Ground truth does not reflect EMA/ANSM equivalence standards (CLISTER-D12, CLISTER-D13).
  - **MINOR (IC, OF):** Truncated sentences and table fragments introduce noise (CLISTER-D14, CLISTER-D15, CLISTER-D16).

#### DrBenchmark/MANTRAGSC
- **Task:** Biomedical NER (UMLS Semantic Groups, IOB2) across multiple language-source configurations
- **Deployment fit:** Weak — the sampled examples appear exclusively from the `fr_medline` configuration (research titles), not the `fr_emea` configuration (drug labels) that would be more deployment-relevant. NER label taxonomy replicates the same UMLS Semantic Group limitations as QUAERO.
- **Key concerns:**
  - **MAJOR (IO, IC):** Sampled content is entirely MEDLINE-style short clinical/research titles (MANTRAGSC-D1, MANTRAGSC-D2); `fr_emea` configuration — most relevant to deployment — was not represented in the analyzed sample. This is a structural sampling gap affecting interpretation.
  - **MAJOR (OO):** INN/excipient conflated under CHEM label with no sub-typing; no posology, ATC, or contraindication qualifier tags exist (MANTRAGSC-D8, MANTRAGSC-D9, MANTRAGSC-D10).
  - **MINOR (IC):** Non-metropolitan French geographic provenance in several titles (MANTRAGSC-D11, MANTRAGSC-D12); veterinary pathology present (MANTRAGSC-D13).
  - **MAJOR (OC):** Annotation by biomedical NLP researchers; no regulatory affairs expertise in annotation workflow.

#### DrBenchmark/E3C
- **Task:** NER for clinical entities (CLINENTITY) and temporal/factuality entities on French clinical case reports
- **Deployment fit:** Weak — all content is clinical case narrative; drug names and dosages appear extensively but are systematically unlabeled (O-tagged), confirming the label ontology targets pathology/symptom recognition exclusively.
- **Key concerns:**
  - **CRITICAL (IO, IC):** All examples are clinical case reports; no regulatory document genre present (E3C-D1, E3C-D2, E3C-D3).
  - **MAJOR (IO, OO):** Drug names (ciclosporine, vancomycine, fentanyl, metronidazole, isoniazide) appear frequently but are systematically tagged O (E3C-D4, E3C-D5, E3C-D6, E3C-D7). The label set captures pathologies/symptoms, not pharmacological or regulatory entity types.
  - **MAJOR (IC):** Multiple examples reference North African and sub-Saharan African clinical settings (E3C-D8, E3C-D9), not metropolitan French regulatory contexts.
  - **MINOR (IC, IF):** Tokenization artifacts from OCR/copy-paste provenance (E3C-D10, E3C-D11).

#### DrBenchmark/PxCorpus
- **Task:** Intent classification (4 classes) and NER (38 classes) on transcribed spoken drug prescription dictations
- **Deployment fit:** Weak — the spoken-language transcription register is fundamentally misaligned with the written regulatory document genre the deployment targets, despite partial NER label overlap with posology entity types.
- **Key concerns:**
  - **CRITICAL (IF):** All content is transcribed spoken dictation with pervasive spoken-language artifacts: disfluencies ("euh"), code-switching English/French (PXCORPUS-D2), automated system error messages embedded in utterances (PXCORPUS-D3), truncated words (PXCORPUS-D17, PXCORPUS-D18). NER models trained on this corpus are unlikely to transfer to written regulatory text.
  - **MAJOR (IO, IC):** No regulatory submission text, SmPC sections, or EMA-style safety warning language present (PXCORPUS-D9, PXCORPUS-D10). Spoken compliance-checking meta-commentary (PXCORPUS-D11) superficially resembles the deployment task but is a qualitatively different genre.
  - **MINOR (OO):** Severe class imbalance — `replace` class at ~0.6% of sample (PXCORPUS-D12, PXCORPUS-D13); full NER tag ontology (38 classes) not surfaced in HF metadata (PXCORPUS-D14, PXCORPUS-D15).
  - **INFO (IC):** INN/brand name distinction exists in NER label set (tag 10 vs. tag 22) (PXCORPUS-D6, PXCORPUS-D7); this partial overlap with deployment vocabulary does not compensate for the form mismatch.

#### DrBenchmark/DiaMED
- **Task:** Multi-class ICD-10 chapter classification of clinical case reports (22 chapters)
- **Deployment fit:** Weak — DiaMED is the only dataset with a named original contribution to DrBenchmark, but its geographic provenance (exclusively Pan African Medical Journal), its task type (ICD-10 chapter classification), and its annotation base make it poorly aligned with the deployment context.
- **Key concerns:**
  - **CRITICAL (IO, IC):** All examples are clinical case reports from sub-Saharan African clinical settings; no regulatory document genre present (DIAMED-D1, DIAMED-D2). All 14 sampled examples show African institutional provenance (DIAMED-D9, DIAMED-D3, DIAMED-D12).
  - **MAJOR (IC):** Geographic setting is uniformly non-metropolitan France; ICD-10 chapter classification reflects sub-Saharan African disease profiles, not the metropolitan French regulatory population (DIAMED-D9).
  - **MAJOR (OC):** IAA validated on only 30 total cases across 2 sessions (15 per session); narrow validation base for a 739-example corpus. Multi-system boundary cases (DIAMED-D5) may be inconsistently labeled without detection.
  - **MAJOR (OO):** ICD-10 chapter-level labels reflect diagnostic classification, not regulatory compliance; annotators are clinical experts, not regulatory affairs specialists.
  - **MINOR (IF):** Images present in schema but excluded from the NLP task; modality inflation in HF metadata.

#### DrBenchmark/DEFT2021
- **Task:** NER (14-class clinical entity types) and multi-label classification (23 MeSH Chapter C axes) on clinical case reports
- **Deployment fit:** Weak — DEFT2021's NER label set (DOSAGE, SUBSTANCE, TREATMENT) has the closest surface alignment to regulatory entity vocabulary within the benchmark, but the deployment-critical token types are annotated in clinical narrative context, not regulatory labeling structure.
- **Key concerns:**
  - **CRITICAL (IO, IC):** All examples are clinical case reports; no regulatory document genre present (DEFT2021-D4). Drug names and doses appear in clinical narratives (DEFT2021-D2, DEFT2021-D5, DEFT2021-D6) rather than in EMA SmPC-structured posology or contraindication sections.
  - **MAJOR (IC):** DOSAGE and SUBSTANCE/TREATMENT annotations are calibrated for clinical case-report annotation norms, not EMA/ANSM regulatory labeling annotation norms (DEFT2021-D10, DEFT2021-D11). No ATC codes, excipient names, or contraindication qualifiers observed.
  - **MAJOR (IO):** Strong urology/oncology sub-domain bias in sampled cases (DEFT2021-D8) may not represent the breadth of disease categories in regulatory labeling documents.
  - **MAJOR (OC):** No IAA statistics reported in benchmark paper for DEFT2021 NER; no regulatory affairs expertise in annotation workflow.
  - **MINOR (OF):** Some IOB2 annotation inconsistencies visible at entity boundaries (DEFT2021-D13, DEFT2021-D14).

#### DrBenchmark/CAS
- **Task:** POS tagging (31 classes, silver-standard), negation/speculation classification, and NER for negation/speculation on French clinical case reports
- **Deployment fit:** Weak — POS tagging has no direct relevance to the deployment's NER/STS pipeline; negation/speculation classification is a tangentially useful sub-component but is calibrated on clinical case negation patterns, not regulatory safety-warning negation.
- **Key concerns:**
  - **MAJOR (IO, IC):** Exclusively clinical case narrative genre; no regulatory document content present (CAS-D1, CAS-D5). Drug/dose mentions are narrative-embedded, not in regulatory labeling format (CAS-D22, CAS-D63).
  - **MAJOR (OO):** Sampled config is POS tagging — not aligned to NER or STS deployment tasks (CAS-D2).
  - **MAJOR (OC):** Silver-standard annotation at 98% precision introduces systematic noise; annotation by NLP researchers and automated tools, no regulatory expertise.
  - **MINOR (IC):** Possible non-metropolitan French clinical cases in sample (CAS-D15, CAS-D44).

#### DrBenchmark/ESSAI
- **Task:** POS tagging (36-class ESSAI-specific scheme), negation/speculation NER and classification on French clinical trial protocols
- **Deployment fit:** Weak — clinical trial protocol genre is meaningfully distinct from regulatory labeling documents; vocabulary is dominated by experimental drug codes and trial-procedure language rather than approved product labeling vocabulary.
- **Key concerns:**
  - **MAJOR (IO, IC):** Genre is clinical trial protocols (partially patient-facing informed consent documents), not SmPCs or patient leaflets (ESSAI-D4, ESSAI-D5, ESSAI-D6). Regulatory term "autorisation de mise sur le marché" appears only incidentally (ESSAI-D7).
  - **MAJOR (IC):** Drug vocabulary consists primarily of experimental compound codes (BMS-986179, MEDI9197, LY3200882) not representative of approved product labeling (ESSAI-D8, ESSAI-D9). Approved drugs appear in trial arm context only (ESSAI-D10).
  - **MINOR (IC, OO):** Negation/contraindication language present but structurally different from SmPC safety-warning negation (ESSAI-D3, ESSAI-D11); trial-context negation (eligibility criteria) ≠ labeling-context negation.
  - **MINOR (OF):** ESSAI-specific 36-class POS scheme not directly portable to regulatory document tokenization (ESSAI-D14); possible transcription artifact detected (ESSAI-D15).
  - **MAJOR (OC):** Silver-standard TreeTagger annotations; no regulatory affairs expertise in annotation workflow.

---

### Cross-Cutting Findings

#### CRITICAL

**C1 — Universal genre mismatch: clinical/research prose vs. regulatory submission text (IO, IC)**
Every dataset in the benchmark derives from clinical case reports, research abstracts, scientific literature, clinical trial protocols, exam questions, or transcribed speech. Not a single dataset contains examples drawn from current-format EMA SmPCs (QRD template v10.4), patient information leaflets conforming to current PIL templates, CTD modules, or ANSM-format national authorization dossiers. QUAERO EMEA is the closest approximation but its source documents predate the current QRD revision cycle and have been preprocessed in ways that destroy document structure. This gap is confirmed across QUAERO-D7, QUAERO-D8, CLISTER-D1, E3C-D1, DEFT2021-D4, DIAMED-D1, CAS-D1, ESSAI-D4, PxCorpus-D9, MORFITT-D1, MANTRAGSC-D1, DEFT2020-D6.

**C2 — Universal NER label taxonomy misalignment with regulatory entity types (OO)**
Across all NER datasets (QUAERO, MANTRAGSC, E3C, DEFT2021, PxCorpus), the label ontologies use UMLS Semantic Groups (CHEM, DISO, PROC), clinical entity types (CLINENTITY, PATHOLOGY, SOSY), or spoken-prescription categories (drug, dose, mode). No label set distinguishes INNs from excipients from chemical reagents (QUAERO-D4, QUAERO-D5, QUAERO-D6, MANTRAGSC-D8). ATC codes are textually present in QUAERO (QUAERO-D3) but unlabeled. MedDRA terminology (required for SmPC section 4.8) is absent from all label sets. Contraindication qualifiers and EMA SmPC section structural markers are absent from every dataset.

#### MAJOR

**M1 — STS scoring calibration failure for regulatory equivalence (OO)**
Both STS datasets (DEFT2020, CLISTER) use 0–5 Likert averaged similarity scales that are insensitive to legally significant small differences. DEFT2020 scores the omission of "sous stricte surveillance médicale" at 3.6/5 (DEFT2020-D10); omission of a mechanistic qualifier at 3.8 (DEFT2020-D11); addition of an alcohol warning at 3.8 (DEFT2020-D12). CLISTER scores a twofold biological value difference at 4.0 (CLISTER-D8) and a 15-fold PSA difference at 3.75 (CLISTER-D9). This pattern is consistent across both datasets and directly undermines the deployment's requirement for regulatory-equivalence scoring. No published regulatory-equivalence scoring rubric for EMA/ANSM NLP exists to substitute.

**M2 — Annotation workforce has no regulatory affairs expertise across all datasets (OC)**
Every dataset in the benchmark was annotated by clinical case reviewers, NLP researchers, automated tools (CAS/ESSAI — silver standard), or domain-subject-matter experts (one medical expert in DiaMED). No dataset documentation mentions regulatory affairs specialists, pharmacovigilance officers, or legal experts applying EMA SmPC guidelines or ANSM circulars. This is confirmed across QUAERO, DEFT2021 (DEFT2021-D4), CLISTER (CLISTER-D12), DiaMED (DIAMED-D5), CAS, ESSAI. For a deployment where authoritative ground truth rests with regulatory-legal professionals, this is a direct and unmitigated convergent validity threat.

**M3 — High annotator disagreement on drug-label pairs in both STS datasets (OC)**
DEFT2020 shows 5-annotator score ranges of 3+ points on drug-label pairs (DEFT2020-D14, DEFT2020-D15, DEFT2020-D16, DEFT2020-D17). CLISTER uses averaged scores without surfacing individual annotator variance. The DEFT2020 `moy`/`vote` divergence (DEFT2020-D18, DEFT2020-D19, DEFT2020-D20) creates ambiguity about which score should anchor threshold-setting for mandatory regulatory review. Neither dataset provides a definitive, adjudicated ground truth appropriate for regulatory compliance boundary decisions.

**M4 — Silver-standard and narrow IAA across classification/NER tasks (OC)**
CAS POS annotations are auto-generated at 98% precision (CAS-D2, consistent with benchmark documentation). ESSAI uses TreeTagger automatic annotation at 98% precision. DiaMED IAA is validated on only 30 total cases (DIAMED-D5). DEFT2021 reports no IAA statistics. This pattern of uneven and often narrow annotation quality assessment is consistent across tasks. Cross-task IAA comparison is unreliable due to methodological heterogeneity (confirmed by independent 2024 HAL evaluation study).

**M5 — Sub-Saharan African geographic provenance in multiple datasets (IC)**
Several datasets contain examples from African clinical settings that may introduce vocabulary and disease profile distributions unrepresentative of metropolitan French regulatory documents: DiaMED (entirely Pan African Medical Journal: DIAMED-D9), E3C (E3C-D8, E3C-D9), DEFT2021 (DEFT2021-D3, DEFT2021-D12), MANTRAGSC (MANTRAGSC-D11, MANTRAGSC-D12). This is distinct from and does not address the French overseas territory gap.

**M6 — PxCorpus input form fundamentally misaligned with written regulatory text (IF)**
PxCorpus is the only dataset where the IF concern rises to MAJOR/CRITICAL level. Spoken-language transcription artifacts (disfluencies, code-switching, system error messages, truncation) pervade the data (PXCORPUS-D1, PXCORPUS-D2, PXCORPUS-D3, PXCORPUS-D16, PXCORPUS-D17, PXCORPUS-D18) in ways that would impede transfer to written regulatory text NER. This is an isolated finding for this single dataset but represents the most severe IF concern in the benchmark.

**M7 — QUAERO EMEA preprocessing artifacts destroy regulatory document structure (IF, OF)**
The sentence-splitting and nested annotation loss documented in benchmark YAML [Q37] is confirmed in the data: null token/tag sequences (QUAERO-D9), isolated header fragments (QUAERO-D8), excessively long mixed-content sequences (QUAERO-D10). For regulatory compliance NER where nested entity structures may carry compliance significance (e.g., a CHEM entity nested within a PROC entity for a specific route of administration), this 6.06–8.90% annotation loss and document fragmentation is a systematic measurement error affecting the most deployment-relevant dataset.

#### MINOR

**m1 — Non-French tokens in QUAERO EMEA leaflets (IF)**
Czech and German/English organizational names appear in QUAERO examples (QUAERO-D11, QUAERO-D12), reflecting multi-country regulatory leaflet appendices. This is a minor isolated issue but indicates QUAERO is not a clean French-only regulatory corpus.

**m2 — Potentially dated regulatory and clinical standards in FrenchMedMCQA (OC)**
Vaccination obligation rules (FRENCHMEDMCQA-D8) and hypertension thresholds (FRENCHMEDMCQA-D7) may reflect superseded French regulatory status. Temporal validity of exam-derived ground truth warrants review.

**m3 — DEFT2021 NER domain bias toward urology/oncology (IC)**
The sampled DEFT2021 examples cluster in urological and oncological clinical cases (DEFT2021-D8), potentially under-representing the breadth of disease categories appearing in regulatory labeling contraindications and safety warnings.

**m4 — MORFITT includes veterinary medicine content (IO)**
Several MORFITT abstracts cover canine, equine, and avian pathology (MORFITT-D11, MORFITT-D12, MORFITT-D13, MORFITT-D14) under the `veterinary` specialty label — a domain entirely outside human pharmaceutical regulatory compliance.

---

### Confirmed Properties

1. **French text-only, Latin script throughout**: All datasets except PxCorpus (transcribed speech) are written standard French in Latin script with diacritics. No cross-modality, cross-script, or dialect variation relevant to metropolitan France deployment was observed. Input Form is the lowest-concern validity dimension as documented.

2. **Genre taxonomy is clinical/research NLP, not regulatory NLP**: Content inspection across all 12 datasets confirms the benchmark YAML's characterization — clinical cases, research abstracts, clinical trial protocols, exam questions, and transcribed prescriptions are the actual genres represented. QUAERO EMEA and DEFT2020 drug-label subsets are the only partial exceptions.

3. **Drug entities appear in clinical narrative context, not regulatory labeling structure**: Drug names, dosages, and routes of administration appear in multiple datasets (QUAERO, DEFT2021, E3C, CAS, CLISTER, ESSAI, PxCorpus) but consistently in clinical or trial narrative context, not in the formulaic, section-structured format of EMA SmPCs or patient information leaflets.

4. **No French overseas territory content confirmed**: Zero examples from Martinique, Guadeloupe, French Guiana, Réunion, or Mayotte were identified across any dataset. DiaMED's Pan African Journal sourcing does not address this gap. Tropical pathology vocabulary (dengue, chikungunya, paludisme) is absent from all label sets.

5. **No regulatory affairs expertise in any annotation workflow**: Content inspection confirms benchmark YAML documentation — annotators across all datasets are clinical case reviewers, NLP researchers, medical experts, or automated systems. No dataset documentation indicates regulatory affairs specialists or pharmacovigilance officers were involved in annotation.

6. **Best deployment-relevant NER label subset**: DEFT2021's DOSAGE, SUBSTANCE, TREATMENT, FREQUENCY, MODE classes and PxCorpus's drug/dose/mode NER scheme are the closest available approximations to regulatory posology entity typing, but both are calibrated to clinical narrative and spoken prescription contexts respectively — not to EMA SmPC section-structured posology templates.

---

### Content Coverage Summary

**What is collectively represented:** The benchmark assembles strong coverage of French clinical case NLP (CAS, DEFT2021, E3C, DiaMED, CLISTER), research literature NER (QUAERO MEDLINE, MANTRAGSC Medline, MORFITT), clinical trial protocol processing (ESSAI), pharmacy-domain QA (FrenchMedMCQA), drug-prescription spoken NLU (PxCorpus), and mixed-genre STS (DEFT2020). Task type diversity across POS, NER, STS, classification, and MCQA is genuine and broad.

**What gaps remain relative to the deployment:** The benchmark has no tasks or datasets derived from: (1) current-format EMA SmPCs/RCPs (QRD v10.4); (2) patient information leaflets formatted to EMA PIL template; (3) CTD modules or ANSM-format national authorization dossiers; (4) pharmacovigilance periodic safety update reports (PSURs); (5) France-specific packaging regulatory requirements (blue-box, CIP codes, Feuille de style); (6) MedDRA-coded adverse effect terminology (required for SmPC section 4.8); (7) regulatory entity types: INNs as a distinct class, ATC codes, excipient nomenclature by EPC/INCI standards, contraindication qualifiers, EMA SmPC section structural markers. The closest existing comparable resource is the Italian DART corpus (2024) — no French-language regulatory SmPC NLP corpus was identified in the literature.

The benchmark is, in sum, well-suited for evaluating French biomedical language understanding in clinical and research NLP — which is its stated purpose — but the deployment context requires regulatory document NLP, a meaningfully distinct sub-domain for which DrBenchmark provides only incidental and partial coverage through QUAERO EMEA and DEFT2020 drug-label subsets.

---

### Limitations

1. **MANTRAGSC `fr_emea` configuration not inspected**: The analyzed MANTRAGSC sample appears to be entirely `fr_medline`. The `fr_emea` configuration (EMEA drug labels) may be more deployment-relevant but was not represented in the analyzed examples — its fit assessment here is therefore incomplete and warrants separate inspection.

2. **FrenchMedMCQA Task 2 not analyzed**: The count-of-correct-answers sub-task was not separately examined for any additional deployment-relevant content patterns.

3. **DEFT2021 classification config not sampled**: Only the NER config of DEFT2021 was inspected; the 23 MeSH Chapter C multi-label classification config was not directly sampled, limiting assessment of that task's alignment.

4. **CAS negation/speculation NER configs not sampled**: Only the `pos` config was inspected; the `ner_neg`, `ner_spec`, and `cls` configs — which may be more deployment-relevant — were not represented in the analyzed examples.

5. **Exam answer key provenance for FrenchMedMCQA**: The temporal provenance of exam questions is unknown; questions may span multiple exam years, and the currency of ground-truth answers for regulatory/clinical standards that have changed since question creation cannot be assessed without access to exam metadata.

6. **Annotation quality for inherited datasets**: IAA statistics for QUAERO, MANTRAGSC, E3C, and MORFITT are inherited from original source papers with varying methodologies; they were not re-assessed for DrBenchmark. Cross-dataset IAA comparison is unreliable per independent 2024 evaluation (HAL 04523267).

7. **QUAERO MEDLINE config not sampled**: Only the EMEA config was analyzed; the MEDLINE config (biomedical article titles) was not inspected and would likely show even weaker deployment fit.

8. **No access to ANSM-specific circular documentation**: Whether France-specific national requirements (blue-box, Feuille de style, List I/II classification) introduce vocabulary patterns that would appear in any benchmark dataset cannot be assessed from public corpus inspection alone.

---

### Cited Evidence

- **QUAERO-D1**: Example 1 (CHEM): Excipient list in SmPC section 6 format — confirms regulatory genre alignment.
- **QUAERO-D2**: Example 55: Natalizumab concentration/dose disclosure — posology content present.
- **QUAERO-D3**: Example 95: "code ATC" in text — ATC codes textually present but not annotated as entities.
- **QUAERO-D4**: Example 95: ATC code unlabeled — regulatory entity taxonomy gap.
- **QUAERO-D5**: Example 34: Excipients tagged as CHEM — no INN/excipient distinction.
- **QUAERO-D6**: Example 50: INN and excipients share same CHEM label — regulatory sub-type gap.
- **QUAERO-D7**: Example 36: Header fragment in sentence — splitting artifact.
- **QUAERO-D8**: Example 84: Isolated "EMEA/H/C/122 4." — null-content splitting artifact.
- **QUAERO-D9**: Example 98: Empty tokens/tags — null sentence from splitting.
- **QUAERO-D10**: Example 107: Excessively long mixed-content token sequence — inconsistent splitting.
- **QUAERO-D11**: Example 15: Czech-language tokens in dataset — non-French content.
- **QUAERO-D12**: Example 121: German/English organization names — minor language mixing.
- **QUAERO-D13**: Example 129: Posology sentence — relevant content present.
- **QUAERO-D14**: Example 78: Dose threshold sentence — relevant but unannotated as posology entity.
- **QUAERO-D15**: Example 64: Long contraindication passage — contraindication qualifier entities absent from scheme.
- **QUAERO-D16**: Example 23: Pediatric exclusion sentence — population qualifier not captured as distinct entity type.
- **FRENCHMEDMCQA-D1**: Example 105 | simple/1 | IC, IO | Only instance of SmPC-adjacent regulatory terminology ("résumé des caractéristiques du produit")
- **FRENCHMEDMCQA-D2**: Example 70 | multiple/1 | IC | Brand name (DAKTARIN®) in answer option; clinical register, not regulatory normative prose
- **FRENCHMEDMCQA-D5**: Example 6 | simple/1 | IC | Drug names as exam answer options, not as labeled regulatory entities
- **FRENCHMEDMCQA-D6**: Example 50 | multiple/1 | IC | Pharmaceutical container classification as exam knowledge, not regulatory artifact
- **FRENCHMEDMCQA-D7**: Example 20 | multiple/4 | OC | Potentially dated WHO hypertension thresholds — temporal validity concern
- **FRENCHMEDMCQA-D8**: Example 94 | multiple/1 | OC | Hepatitis B vaccination obligation — may reflect superseded French regulatory status
- **FRENCHMEDMCQA-D9**: Example 105 | simple/1 | OC | Definitional exam question about regulatory concept; ground truth is licensure fact, not compliance judgment
- **DEFT2020-D1**: 4 | IC, IO | Breastfeeding contraindication drug label
- **DEFT2020-D2**: 18 | IC, IO | Excipient contraindication drug label
- **DEFT2020-D3**: 16 | OO, OC | Safety warning with time-threshold
- **DEFT2020-D4**: 52 | IC | Pharmaceutical form description
- **DEFT2020-D5**: 121 | IC | Storage instruction
- **DEFT2020-D6**: 6 | IO, IC | Apiculture content, irrelevant genre
- **DEFT2020-D7**: 60 | IO, IC | Sports content
- **DEFT2020-D8**: 76 | IO, IC | WWII military content
- **DEFT2020-D9**: 1 | IO, IC | Railway infrastructure content
- **DEFT2020-D10**: 13 | OO, OC | Missing "stricte surveillance médicale" scored 3.6
- **DEFT2020-D11**: 30 | OO, OC | Missing mechanistic qualifier scored 3.8
- **DEFT2020-D12**: 130 | OO, OC | Alcohol qualifier added, scored 3.8
- **DEFT2020-D13**: 127 | OO | Contradictory sterilization statements scored 0.4
- **DEFT2020-D14**: 4 | OC | Annotator spread [5,2,4,4,5] on breastfeeding pair
- **DEFT2020-D15**: 16 | OC | Annotator spread [5,2,4,4,5] on drug safety pair
- **DEFT2020-D16**: 46 | OC | Annotator spread [5,2,0,3,1] on historical pair
- **DEFT2020-D17**: 109 | OC | Annotator spread [5,4,0,3,0] on clinical pair
- **DEFT2020-D18**: 46 | OO | moy=2.2 vs vote=5.0 discrepancy
- **DEFT2020-D19**: 109 | OO | moy=2.4 vs vote=0.0 discrepancy
- **DEFT2020-D20**: 82 | OO | moy=2.7 vs vote=4.0 discrepancy
- **DEFT2020-D21**: 45 | IC | Health education research, not regulatory
- **DEFT2020-D22**: 26 | IC | Anaesthesia trial abstract
- **MORFITT-D1**: Ex. 1 | 9 | Scientific literature genre, not regulatory
- **MORFITT-D2**: Ex. 19 | 7 | Closest regulatory-adjacent but still research abstract
- **MORFITT-D3**: Ex. 33 | 10,7 | Cosmetic formulation research, not patient leaflet
- **MORFITT-D4**: Ex. 8 | 0 | Canadian geographic provenance
- **MORFITT-D5**: Ex. 10 | 3 | Quebec, Canada provenance
- **MORFITT-D6**: Ex. 20 | 1 | Jordanian patient population
- **MORFITT-D7**: Ex. 22 | 11 | Egyptian student population
- **MORFITT-D8**: Ex. 31 | 11 | Saudi Arabian internship context
- **MORFITT-D9**: Ex. 32 | 0 | Japanese epidemiology data
- **MORFITT-D10**: Ex. 26 | 6,8,5 | Chinese parasitology
- **MORFITT-D11**: Ex. 9 | 6,0,8 | Canine otitis/veterinary
- **MORFITT-D12**: Ex. 28 | 3,8 | Veterinary EEG study
- **MORFITT-D13**: Ex. 29 | 8 | Small animal dermatology
- **MORFITT-D14**: Ex. 5 | 6,8 | Equine pulmonary physiology
- **MORFITT-D15**: Ex. 17 | 2 | Chikungunya/overseas territory relevance
- **MORFITT-D16**: Ex. 6 | 6,8,2 | Translated content, register concern
- **MORFITT-D17**: Ex. 5 | 6,8 | Translated content, register concern
- **CLISTER-D1**: 1 | 0.0 | IO, IC
- **CLISTER-D2**: 6 | 0.0 | IO, IC
- **CLISTER-D3**: 222 | 0.0 | IO, IC
- **CLISTER-D4**: 41 | 2.0 | IC
- **CLISTER-D5**: 116 | 1.0 | IC
- **CLISTER-D6**: 98 | 2.0 | IC
- **CLISTER-D7**: 164 | 2.0 | IC
- **CLISTER-D8**: 188 | 4.0 | OO
- **CLISTER-D9**: 123 | 3.75 | OO
- **CLISTER-D10**: 125 | 4.0 | OO
- **CLISTER-D11**: 8 | 1.0 | OO
- **CLISTER-D12**: 8 + 123 | 1.0/3.75 | OC
- **CLISTER-D13**: 163 | 5.0 | OC
- **CLISTER-D14**: 61 | 0.0 | IC, OF
- **CLISTER-D15**: 131 | 4.0 | IC, OF
- **CLISTER-D16**: 8 | 1.0 | IC, OF
- **MANTRAGSC-D1**: Ex. 1 | DISO | MEDLINE case-report title; not regulatory prose
- **MANTRAGSC-D2**: Ex. 36 | CHEM/DISO | Drug name in clinical title, no posology context
- **MANTRAGSC-D3**: Ex. 41 | GEOG/DISO | Sub-Saharan African context, non-regulatory
- **MANTRAGSC-D4**: Ex. 43 | DISO | Senegalese case series, non-metropolitan
- **MANTRAGSC-D5**: Ex. 7 | O | 3-token title, no NER value
- **MANTRAGSC-D6**: Ex. 34 | O | 2-token title
- **MANTRAGSC-D7**: Ex. 57 | O | Administrative title, no regulatory content
- **MANTRAGSC-D8**: Ex. 36 | CHEM | INN labeled coarsely as chemical
- **MANTRAGSC-D9**: Ex. 45 | CHEM/PHYS | Hormones labeled without posology context
- **MANTRAGSC-D10**: Ex. 18 | DEVI | Medical device, no excipient/regulatory context
- **MANTRAGSC-D11**: Ex. 43 | DISO | Dakar case series
- **MANTRAGSC-D12**: Ex. 41 | GEOG | Cameroonian epidemic
- **MANTRAGSC-D13**: Ex. 22 | DISO | Veterinary pathology
- **MANTRAGSC-D14**: Ex. 50 | CHEM | Vague pharmaceutical reference, ambiguous regulatory status
- **E3C-D1**: Ex. 1 | French clinical prose, well-formed, text-only
- **E3C-D2**: Ex. 59 | Drug in clinical narrative, not regulatory template
- **E3C-D3**: Ex. 62 | Medication dosage in clinical context
- **E3C-D4**: Ex. 79 | Drug names/doses systematically unlabeled
- **E3C-D5**: Ex. 53 | Antibiotics tagged O
- **E3C-D6**: Ex. 103 | Anesthetic agents with doses tagged O
- **E3C-D7**: Ex. 39 | Immunosuppressants tagged O
- **E3C-D8**: Ex. 70 | Patient from Morocco
- **E3C-D9**: Ex. 90 | Explicit sub-Saharan Africa reference
- **E3C-D10**: Ex. 5 | Tokenization artifact (escaped newline)
- **E3C-D11**: Ex. 1 | Backtick artifact from preprocessing
- **E3C-D12**: Ex. 20 | Pathology-focused CLINENTITY labels confirmed
- **E3C-D13**: Ex. 95 | Morphological finding labeling pattern
- **E3C-D14**: Ex. 53 | Multi-token entity boundary labeling
- **PXCORPUS-D1**: Ex. 75 | medical_prescription | IF, IC | INFO
- **PXCORPUS-D2**: Ex. 88 | none | IF, IC | MAJOR
- **PXCORPUS-D3**: Ex. 207 | medical_prescription | IF, IC | MAJOR
- **PXCORPUS-D4**: Ex. 10 | negate | IF | MINOR
- **PXCORPUS-D5**: Ex. 3 | none | IF | MINOR
- **PXCORPUS-D6**: Ex. 5 | medical_prescription | IC, OO | INFO
- **PXCORPUS-D7**: Ex. 41 | medical_prescription | IC | INFO
- **PXCORPUS-D8**: Ex. 166 | medical_prescription | IC | INFO
- **PXCORPUS-D9**: Ex. 21 | none | IO, IC | MAJOR
- **PXCORPUS-D10**: Ex. 18 | none | IO, IC | MAJOR
- **PXCORPUS-D11**: Ex. 76 | none | IO, IC | MAJOR
- **PXCORPUS-D12**: Ex. 4 | replace | OO | MINOR
- **PXCORPUS-D13**: Ex. 12 | replace | OO | MINOR
- **PXCORPUS-D14**: Ex. 103 | medical_prescription | OO | MINOR
- **PXCORPUS-D15**: Ex. 22 | medical_prescription | OO | MINOR
- **PXCORPUS-D16**: Ex. 169 | medical_prescription | IF | CRITICAL
- **PXCORPUS-D17**: Ex. 197 | medical_prescription | IF | CRITICAL
- **PXCORPUS-D18**: Ex. 84 | none | IF | CRITICAL
- **DIAMED-D1**: Example 1 (label=A00-B99): "Maladie de Kaposi à localisation broncho-pulmonaire révélant une infection VIH" — clinical narrative genre; drug mentions as prose; sub-Saharan African disease profile.
- **DIAMED-D2**: Example 8 (label=H60-H95): "amphotéricine B par voie intraveineuse...relais par l'itraconazole" — posology as clinical prose, not regulatory labeling format.
- **DIAMED-D3**: Example 3 (label=D50-D89): keyword "Maroc" — Morocco-based clinical case; non-metropolitan-France provenance.
- **DIAMED-D4**: Example 4 (label=E00-E89): Piebaldisme case — rare pigmentary anomaly; no regulatory labeling content.
- **DIAMED-D5**: Example 5 (label=F01-F99): Pathomimie case with psychiatric and dermatological features — multi-system ambiguity for ICD-10 chapter assignment.
- **DIAMED-D6**: Example 6 (label=G00-G99): Spinal compression case from unspecified African setting — clinical narrative genre confirmed.
- **DIAMED-D7**: Example 7 (label=H00-H59): Adie pupil case — brief clinical report; no regulatory content.
- **DIAMED-D8**: Example 8 (label=H60-H95): Otitis externa maligne — Candida albicans — clinical case with treatment narrative.
- **DIAMED-D9**: Example 9 (label=I00-I99): "CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" — explicit sub-Saharan African institutional origin.
- **DIAMED-D10**: Example 10 (label=J00-J99): Abducens nerve palsy/pansinusitis — clinical case; respiratory/ENT context.
- **DIAMED-D11**: Example 11 (label=K00-K95): Acute gastric dilatation — two cases including one occurring during Ramadan fast; cultural/geographic context outside metropolitan France.
- **DIAMED-D12**: Example 12 (label=L00-L99): keyword "Niamey"; drug toxidermie case — Niger clinical setting; drug names (Phénobarbital, Halopéridol) in narrative prose.
- **DIAMED-D13**: Example 13 (label=M00-M99): Osteochondritis dissecans in adolescent — musculoskeletal clinical case; no regulatory content.
- **DIAMED-D14**: Example 14 (label=N00-N99): Breast fibromatosis labeled N00-N99 — potential ICD-10 boundary ambiguity between genitourinary and neoplasm chapters.
- **DEFT2021-D1**: id=946 | Clinical case surgical narrative; no regulatory genre
- **DEFT2021-D2**: id=140 | Dense chemotherapy dosage annotation; clinical, not regulatory
- **DEFT2021-D3**: id=1450 | Madagascar travel reference; geographic scope note
- **DEFT2021-D4**: id=179 | Drug/dose entities in clinical observation note, not SmPC
- **DEFT2021-D5**: id=546 | Antibiotic drugs as TREATMENT; clinical, not INN/ATC
- **DEFT2021-D6**: id=146 | Topical drug with concentration; clinical prescription, not SmPC
- **DEFT2021-D7**: id=2708 | Vaccination as TREATMENT; non-regulatory
- **DEFT2021-D8**: id=1087 | Detailed urothelial carcinoma; urology bias
- **DEFT2021-D9**: id=1127 | Scleroderma case; rare non-urology example
- **DEFT2021-D10**: id=22 | Morphine dosage in clinical error narrative
- **DEFT2021-D11**: id=20 | Morphine injection dose; clinical protocol, not regulatory
- **DEFT2021-D12**: id=2577 | Africa residence in patient history
- **DEFT2021-D13**: id=1766 | Single-token SOSY annotation
- **DEFT2021-D14**: id=2931 | Punctuation-only sentence fragment
- **CAS-D1**: Example 1: "l'examen clinique montre un état général conservé" — canonical clinical examination prose confirming genre.
- **CAS-D2**: Example 2: pos_tags = [3, 8, 23, 9, ...] — POS integer labels only, no entity/similarity labels.
- **CAS-D5**: Example 5: "un homme de 48 ans…rectorragies dues à des polypes du rectum traités par électrocoagulation" — clinical case narrative structure.
- **CAS-D15**: Example 15: "soins dentaire informels et de points de feux" — possible non-metropolitan context.
- **CAS-D22**: Example 22: "administration d'une ampoule de digoxine en intraveineuse" — drug in narrative, not regulatory format.
- **CAS-D33**: Example 33: "cyclophosphamide, vincristine et prednisone" — chemotherapy listed in case narrative protocol.
- **CAS-D34**: Example 34: "le Betnésol® lavement était progressivement arrêté" — branded drug with trademark, no regulatory structure.
- **CAS-D44**: Example 44: "exposition à l'eau de la rivière" — environmental exposure scenario.
- **CAS-D63**: Example 63: "Proctocort® (hydrocortisone acétate 90 mg : 1 lavement tous les soirs)" — closest instance to posology expression, still narrative-embedded.
- **CAS-D103**: Example 103: Dense AST/ALT/bilirubine lab table — complex clinical notation tokenized as POS sequence.
- **ESSAI-D1**: Ex. 1 | Oncology clinical trial domain confirmed
- **ESSAI-D2**: Ex. 3 | Randomization/trial arm language
- **ESSAI-D3**: Ex. 40 | "contre-indication" in eligibility criterion, not labeling
- **ESSAI-D4**: Ex. 25 | Patient-directed register, not SmPC/leaflet
- **ESSAI-D5**: Ex. 26 | Patient follow-up language
- **ESSAI-D6**: Ex. 33 | Institution-specific (Gustave Roussy)
- **ESSAI-D7**: Ex. 71 | "autorisation de mise sur le marché" incidental mention
- **ESSAI-D8**: Ex. 2 | Experimental drug code (MEDI9197)
- **ESSAI-D9**: Ex. 42 | Alphanumeric drug code (BMS-986179)
- **ESSAI-D10**: Ex. 37 | Approved drugs in trial arm context
- **ESSAI-D11**: Ex. 40 | Negation of contraindication as eligibility criterion
- **ESSAI-D12**: Ex. 5 | Dose optimization objective (trial context)
- **ESSAI-D13**: Ex. 48 | Posology in trial schedule
- **ESSAI-D14**: Ex. 46 | Integer POS tags, 36-class ESSAI-specific scheme
- **ESSAI-D15**: Ex. 75 | Possible transcription artifact ("set" for "est")
