## Deployment Context

**Use case:** In a pharmaceutical setting, a regulatory specialist uses document management software to ensure compliance in French drug labeling and scientific abstracts by applying a model evaluated on semantic textual similarity and fine-grained named-entity recognition. The system identifies over a dozen types of precise entities, such as chemical compounds and dosage modes, while verifying that safety warnings across different leaflets or patents are semantically consistent. These results determine whether pharmacological documentation meets strict professional standards for official submission or requires manual revision to prevent regulatory non-compliance.
**Target population:** Regulatory affairs specialists, pharmacologists, and legal experts at pharmaceutical companies or government health agencies.

# Validity Analysis: drbenchmark
**Target context:** EU Pharmaceutical Regulatory Affairs Professionals (France / EMA-ANSM Zone)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 4 | Minor gaps | high |
| **Average** | **2.5** | | |

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

DrBenchmark is the most comprehensive French biomedical language understanding benchmark available [Q83] and provides solid methodological infrastructure (HuggingFace toolkit, IOB2/SeqEval/Spearman evaluation, reproducibility hygiene) [Q48, Q51, Q52, Q54], but its fitness as a proxy for EU pharmaceutical regulatory NLP evaluation is severely limited. The benchmark is calibrated to clinical and biomedical research French, while the deployment operates on regulatory French — a register characterized by EMA QRD-templated phrasing, INN/ATC/excipient nomenclature, and legally constrained safety-warning formulations ([WEB-3], [WEB-5], [WEB-7]). Empirical sampling confirms three CRITICAL cross-cutting findings: (C1) universal regulatory document genre absence except QUAERO EMEA, a minority subset; (C2) no benchmark label set encodes regulatory-specific entity types (INNs distinct from CHEM, ATC codes, MA numbers — confirmed full gaps); (C3) STS scoring is fundamentally misaligned with regulatory equivalence requirements, with 2× biomarker differences scored 4.0 (CLISTER-D10) and scope extensions scored 3.8 (DEFT2020-D130). The benchmark's strongest dimensions for this deployment are Input Form (text/Latin-script/HuggingFace alignment) and Output Form (IOB2 + Spearman protocol), both LOWER priority in elicitation. Its weakest dimensions — Output Ontology (score 1), Input Ontology, Input Content, and Output Content — are precisely the four HIGH-priority dimensions in elicitation, indicating that the benchmark's diagnostic value is inverse to deployment criticality. Web search confirms no French regulatory NLP benchmark exists ([WEB-10], gap_ids 1–4), so DrBenchmark remains the best available foundational evaluation, but it cannot substitute for regulatory-specific validation.

## Practical Guidance

### What This Benchmark Measures

DrBenchmark measures French biomedical language understanding capabilities — POS tagging, coarse-grained NER over UMLS Semantic Groups [Q103, Q106], clinical entity NER [Q104, Q108], pharmacy-domain MCQA [Q39], and general semantic similarity on clinical case sentence pairs [Q22, Q41]. For the regulatory deployment, it provides a foundational signal for whether a French biomedical model has competent French clinical-register comprehension and can extract drug, anatomy, and procedure entities at coarse UMLS granularity. The strongest dimensions (Input Form, Output Form) confirm interface compatibility, and Output Form's scoring infrastructure [Q51, Q52, Q54] is fully reusable.

### Construct Depth

Construct depth is shallow for the deployment's actual targets. The benchmark probes biomedical entity recognition at the UMLS-Semantic-Group level — sufficient to distinguish CHEM from DISO from PROC, but insufficient to distinguish INNs from excipients from solvents (QUAERO-D1, QUAERO-D55, MANTRAGSC-D5), to identify ATC codes (QUAERO-D95), or to flag contraindication population qualifiers (QUAERO-D64, QUAERO-D86). STS depth is even shallower: scoring captures lexical and structural similarity on clinical narratives but does not detect legally significant micro-differences (CLISTER-D10, CLISTER-D12, DEFT2020-D130). What remains unaddressed: regulatory-genre register (SmPC/PIL/CTD/RMP/patent), regulatory entity granularity, regulatory-equivalence STS rubric, and regulatory-expert annotation norms.

### What Else You Need

Three supplementation streams are required: (1) Input Ontology + Input Content — construct or curate a regulatory-genre evaluation set drawing primary instances from SmPCs (per EMA QRD v10.4 [WEB-5, WEB-6]), PILs, CTD modules, RMPs, and pharmaceutical patents, ideally with French national additions (ANSM 'Feuille de style', blue-box content [WEB-7, WEB-8]); (2) Output Ontology — define a regulatory entity schema covering INN/ATC code/excipient-with-known-effect/MA number/contraindication qualifier/special warning, and develop a regulatory-equivalence STS rubric calibrated to EMA SmPC guideline standards (no published equivalent exists [WEB-10], gap_id 3); (3) Output Content — recruit EMA/ANSM-trained regulatory affairs specialists and legal experts to (re-)annotate a calibration set, measuring divergence from clinical NLP annotation patterns on borderline cases (anticipated per elicitation A4 and confirmed by C2/C3). The deployment's documented 'supplementary template layer' for CTD modules (A1) and human-review-gate design (A3) appropriately mitigate but do not eliminate the validity gap.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
DrBenchmark's task taxonomy spans 20 tasks across POS, NER, MCQA, MCC, MLC, and STS [Q1, Q18, Q81], which superficially overlaps with the deployment's NER and STS needs. However, no task in the inventory is drawn from EU regulatory document genres — SmPCs, PILs, CTD modules, RMPs, and patent claims are absent or only marginally represented. The closest analog to regulatory pharmacology knowledge is FrenchMedMCQA, derived from French pharmacy diploma exams [Q39], but this is a closed-set MCQA task whose output ontology (answer-index selection) bears no relation to the deployment's NER spans or STS scores (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D2). Authors themselves acknowledge that general benchmarks may not adequately evaluate in-domain performance [Q10]. Web search confirms no published French biomedical NLP benchmark covers regulatory genres (gap_id 1, [WEB-10]). For a HIGH-priority dimension in elicitation, this represents substantial construct underrepresentation.

**Strengths:**
- Includes both NER and STS as task types, which are the two task categories the deployment requires [Q1, Q18]
- Pharmacy diploma MCQA [Q39] provides a partial proxy for pharmaceutical domain knowledge, though task-type mismatched

**Checklist:**

- **IO-1**: Required deployment categories are NER over regulatory documents (SmPCs, PILs, CTD modules, RMPs, patents) and STS calibrated for regulatory equivalence on safety warnings. The benchmark covers NER and STS as task types [Q1, Q18] but not on these document genres. — _Sources: Q1, Q18_
- **IO-2**: Yes — task taxonomy omits regulatory document genres entirely. C1 confirms universal regulatory document genre absence across all datasets except QUAERO EMEA, with no SmPC, PIL, CTD, RMP, or patent text contributing primary instances. Independent evaluation [WEB-10] corroborates clinical-only scope. — _Sources: C1, WEB-10_
- **IO-3**: MCQA task on pharmacy diploma exams [Q39], MORFITT specialty classification, and DiaMED ICD-10 chapter classification are construct-irrelevant for the deployment, which requires only NER and STS outputs (FRENCHMEDMCQA-D1, MORFITT-D17, DIAMED-D1). Veterinary content (MORFITT-D12, MORFITT-D13, MORFITT-D14) is also irrelevant. — _Sources: Q39, FRENCHMEDMCQA-D1, MORFITT-D17, DIAMED-D1_
- **IO-4**: Major content validity gap: the benchmark's task taxonomy does not include any regulatory-genre NER task or any regulatory-equivalence STS task. Deployment-critical genres (SmPC, PIL, CTD, RMP, patent claims) are not represented as primary task sources, with QUAERO EMEA being the only marginal exception. — _Sources: Q10, C1, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'It encompasses 20 diversified tasks, including named-entity recognition, part-of-speech tagging, question-answering, semantic textual similarity, and classification.' (p.1)
- [Q10] 'In the case of specialized domains, general benchmarks may not adequately evaluate the performance of in-domain models.' (p.2)
- [Q18] 'A variety of tasks with different requirements and objectives: Part-of-Speech (POS) tagging, Multi-class, Multi-label and Intent classification, Named-Entity Recognition (NER), Multiple-Choice Question-Answering (MCQA), and Semantic Textual Similarity (STS).' (p.2)
- [Q39] 'FrenchMedMCQA ... contains 3,105 questions coming from real exams of the French medical specialization diploma in pharmacy' (p.4)
- [Q81] 'Table 8 summarizes the results obtained on average by the considered MLMs when aggregating the tasks into one of the five designated categories: POS, NER, MCQA, MCC ... MLC ... or STS tasks.' (p.8)

*Web sources:*
- [WEB-10] Independent 2024 evaluation (Bannour et al., arXiv:2403.19726) confirms all evaluated French biomedical NER corpora are clinical; no regulatory genre included

*Dataset analysis:*
- C1 (cross-cutting): Universal regulatory document genre absence across all datasets except QUAERO EMEA; no SmPC, PIL, CTD, RMP, or patent claims as primary source text
- FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D2: MCQA output is closed-set answer index, not NER spans or STS scores — categorical task-type mismatch
- MORFITT-D17: 12 specialty classes have no mapping to EMA entity categories
- DIAMED-D1: ICD-10 chapter classification has no structural relationship to NER or STS deployment requirements

</details>

**Information gaps:**
- No quantitative measure of how much QUAERO EMEA content within DrBenchmark's task instances corresponds to SmPC vs. PIL sub-genres

**Requires expert verification:**
- Whether MCQA pharmacy diploma content has any indirect diagnostic value for assessing model regulatory knowledge despite task-type mismatch

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Input content sources span clinical literature, clinical cases, trials, and speech transcripts [Q19], with QUAERO EMEA drug labels [Q34] and Mantra-GSC EMEA/patent subsets [Q40] being the only direct regulatory-genre content. Empirical sampling confirms QUAERO EMEA (QUAERO-D37, QUAERO-D51) is authentic EU regulatory document text but a minority subset, while every other dataset is clinical narrative, research abstracts, or transcribed speech with no regulatory register (C1). Furthermore, multiple datasets exhibit non-EU geographic origin (DIAMED Pan African Medical Journal — DIAMED-D2, DIAMED-D9; MORFITT Saudi Arabia/Jordan — MORFITT-D10, MORFITT-D11; E3C/DEFT2021 African contexts — E3C-D9, DEFT2021-D108) introducing register variation inconsistent with EMA/ANSM French. ESSAI's drug mentions are dominated by investigational compound codes (MEDI9197, BMS-986179) absent from marketed labeling (ESSAI-D7, ESSAI-D8). DEFT2020 is contaminated with ~30–40% non-biomedical content (DEFT2020-D1, DEFT2020-D3, DEFT2020-D6). The patent subset, a named deployment genre, is an effective blind spot where CamemBERT models fail entirely [Q73]. For a HIGH-priority dimension, this is a major content validity violation.

**Strengths:**
- QUAERO EMEA is authentic EU drug label text (QUAERO-D37, QUAERO-D51), providing one minority subset of regulatory-register content
- Mantra-GSC nominally includes EMEA and patent subsets [Q40], the named deployment document types

**Checklist:**

- **IC-1**: Yes — deployment requires EU-specific regulatory French (EMA QRD-templated phrasing, ANSM-prescribed contraindication formulations, INN/ATC/excipient nomenclature). Most benchmark content is clinical case narrative without these conventions; multiple datasets have non-EU origin (DIAMED-D2, DIAMED-D9; MORFITT-D10, MORFITT-D11; E3C-D9, E3C-D10). Drug mentions appear in informal clinical posology (CAS-D22, CAS-D29, CLISTER-D6 brand-name use) rather than EMA-templated form. — _Sources: Q19, DIAMED-D2, MORFITT-D10, E3C-D9, CAS-D22_
- **IC-2**: Mostly aligned at the level of language (French) and domain (biomedical) but misaligned at the level of register: regulatory French is template-driven and legally constrained, while benchmark content is predominantly clinical narrative or research abstract prose [Q19]. Investigational compound codes in ESSAI (ESSAI-D7, ESSAI-D8, ESSAI-D9) do not appear in marketed labeling. — _Sources: Q19, ESSAI-D7, CLISTER-D6_
- **IC-3**: Construct-irrelevant content includes: ~30–40% non-biomedical text in DEFT2020 (DEFT2020-D1, DEFT2020-D3, DEFT2020-D5, DEFT2020-D6); veterinary and animal-disease content in MORFITT and MANTRAGSC (MORFITT-D12, MORFITT-D13, MORFITT-D14, MANTRAGSC-D13); ASR artifacts and profanity in PxCorpus (PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D8); educational vignettes in CAS (CAS-D47). — _Sources: DEFT2020-D1, MORFITT-D12, PXCORPUS-D4, CAS-D47_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotator recruitment is documented in DrBenchmark; web search confirms no French regulatory NLP benchmark uses regulatory affairs annotators (gap_id 4). Would need pilot re-annotation by EMA/ANSM-trained regulatory specialists.
- **IC-5**: Confirmed content gaps: ATC codes appear in source text but are unannotated (QUAERO-D95); INNs are conflated with excipients and other chemicals under broad CHEM (QUAERO-D1, QUAERO-D55, MANTRAGSC-D5); patent register is effectively unrepresented [Q73]; non-EU clinical contexts pervade DiaMED, MORFITT, E3C, DEFT2021, and MANTRAGSC. — _Sources: Q73, Q16, QUAERO-D95, QUAERO-D1, WEB-10, WEB-14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q19] 'A diverse range of data origins: Scientific literature, clinical trials, clinical cases, speech transcriptions, and more' (p.2)
- [Q34] 'The dataset covers two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE.' (p.3)
- [Q40] 'Mantra-GSC ... 3 sources ... biomedical abstracts/titles, drug labels and patents' (p.4)
- [Q73] 'all the models based on CamemBERT face difficulties in corpora with limited amount of data, such as MantraGSC Patents, where they fail to generate labels other than O' (p.7)
- [Q16] 'aside the multilingual benchmark BigBIO ... which includes only 4 corpora for French ... no large benchmark specialized in the French biomedical field exists.' (p.2)

*Web sources:*
- [WEB-10] Bannour et al. (2024) confirms all evaluated French biomedical NER corpora are clinical; no regulatory genre
- [WEB-14] arXiv:2504.20598 (2025) confirms pharmaceutical patent text has distinct NLP challenges that biomedical NER models do not address

*Dataset analysis:*
- QUAERO-D37, QUAERO-D51: confirmed authentic EU regulatory document text — the unique regulatory-genre asset
- C1: Universal regulatory genre absence except QUAERO EMEA minority subset
- DEFT2020-D1, D3, D5, D6: ~30–40% non-biomedical content (railway, history, beekeeping, geography) in STS training distribution
- DIAMED-D2, DIAMED-D9: All sources from Pan African Medical Journal — non-EU clinical context
- MORFITT-D10, MORFITT-D11: Saudi Arabia, Jordan abstracts — non-EU register
- E3C-D9, E3C-D10: African and Moroccan clinical contexts
- ESSAI-D7, ESSAI-D8, ESSAI-D9: Investigational compound codes (MEDI9197, BMS-986179, CMAK683X2101) dominate, absent from marketed labeling
- PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D8: ASR artifacts, dysfluencies, profanity in spoken transcripts
- CAS-D22, CAS-D29: Drug mentions in informal clinical posology, not EMA-templated

</details>

**Information gaps:**
- Quantitative breakdown of QUAERO EMEA content into SmPC sections vs. PIL sections vs. other label material
- Whether DEFT2020 task_2 (sentence selection, not sampled) shows different content distribution

**Requires expert verification:**
- Whether non-EU francophone clinical register (Maghreb, sub-Saharan Africa) introduces terminology differences material to regulatory NER

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form is the strongest dimension for the deployment. The benchmark operates exclusively on French text with Latin script and standard French diacritics [Q31], matching the deployment exactly with no script or modality mismatch. Distribution via HuggingFace Datasets with normalized loading schemes [Q48] is fully compatible. Tokenization is acknowledged as varying across models (FlauBERT 1.43, DrBERT-CP 1.90 sub-tokens/word) [Q78], but reported to play a minor role overall [Q80]. Sequence-length handling (sentence splitting for long EMEA documents) [Q37] is compatible with deployment needs. Two concerns prevent a 5: (1) PxCorpus introduces a transcribed-speech modality with ASR artifacts (PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D8) not present in deployment input; (2) tokenization fragmentation impact on highly technical regulatory nomenclature (INNs, ATC codes, excipient IUPAC names) is unverified [Q80]. This dimension is LOWER priority in elicitation, consistent with a non-critical assessment.

**Strengths:**
- Exclusively French text [Q31] with Latin script — perfect language and script match
- HuggingFace toolkit with normalized loading schemes [Q48] — fully compatible with deployment infrastructure
- Standard methodological hygiene (predefined splits, 70/10/20 partitioning) [Q32, Q42]
- Tokenization variation acknowledged and partially analyzed [Q78, Q80]

**Checklist:**

- **IF-1**: Signal distributions are aligned at the level of French text on Latin script [Q31]. Tokenization fragmentation varies across models (1.43–1.90 average sub-tokens/word) [Q78]; impact on technical regulatory nomenclature (INN stems, ATC codes) is unverified [Q80]. — _Sources: Q31, Q78, Q80_
- **IF-2**: Deployment is text-based document processing (per regional YAML); HuggingFace Datasets toolkit is compatible. No infrastructure mismatch is documented [Q48]. — _Sources: Q48_
- **IF-3**: Two domain-specific form differences: (a) PxCorpus is transcribed speech with ASR artifacts (PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D8), incompatible with formal written regulatory prose; (b) sequence length handling for QUAERO EMEA documents that exceed model max length used sentence splitting [Q37], potentially fragmenting cross-sentence regulatory entity references. — _Sources: Q37, PXCORPUS-D4, PXCORPUS-D5_
- **IF-4**: Minor mismatches: PxCorpus speech modality contributes a register that does not exist in deployment; tokenization fragmentation behavior on highly technical nomenclature is not directly evaluated. — _Sources: Q80, PXCORPUS-D4, E3C-D13_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'While the dataset covers 5 languages, only the French portion is retained for the benchmark.' (p.3)
- [Q37] 'considering that some documents from EMEA exceed the maximum input sequence length that most current language models can handle, we decided to split these documents into sentences.' (p.3)
- [Q48] 'We developed a practical toolkit based on the HuggingFace Datasets library ... with data loaders that adhere to normalized schemes and predefined data splits.' (p.5)
- [Q78] 'FlauBERT is the model with the least word segmentation (1.43 in average), while DrBERT-CP tends to have the highest average segmentation (1.90 in average).' (p.8)
- [Q80] 'tokenization, as it is currently done in MLMs, seems to play a minor role in the performance of systems.' (p.8)

*Dataset analysis:*
- Confirmed property #1: French language throughout, Latin script across all 11 datasets
- PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D8: ASR artifacts, dysfluencies, system dialogue prompts in transcribed speech
- E3C-D13: Backslash-n tokenization artifact

</details>

**Information gaps:**
- No direct measurement of tokenization fragmentation behavior on INN stems, ATC alphanumeric codes, or excipient IUPAC names

**Requires expert verification:**
- Whether sentence-splitting [Q37] of long EMEA documents breaks cross-sentence references important to regulatory entity resolution

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The output ontology represents the most severe validity violation for this deployment. NER label sets across all datasets use broad UMLS Semantic Groups (QUAERO: GEOG, PHEN, DISO, ANAT, OBJC, PHYS, PROC, DEVI, CHEM, LIVB [Q103]; Mantra-GSC analogous [Q106]) or coarse clinical entity types (E3C: CLINENTITY, EVENT, ACTOR, BODYPART, TIMEX3, RML [Q104]; PxCorpus prescription entities [Q108]). None of these encodes the regulatory-specific entity types the deployment requires: (a) INNs are conflated with excipients and other chemicals under CHEM (QUAERO-D1, QUAERO-D55, MANTRAGSC-D5, MANTRAGSC-D6); (b) ATC codes appear in source text but receive no entity label (QUAERO-D95) — confirmed full gap; (c) MA numbers are absent from all label sets — confirmed full gap; (d) contraindication population qualifiers are largely untagged (QUAERO-D64, QUAERO-D86); (e) excipient-specific Ph.Eur./INCI distinction is absent. STS scoring is calibrated for general semantic proximity on a 0–5 scale [Q22, Q41] with Spearman/EDRM evaluation [Q54]. Empirical sampling confirms this calibration is fundamentally misaligned: a 2× quantitative biomarker difference scored 4.0 (CLISTER-D10), positive vs. negative lab results scored 3.0 (CLISTER-D12), scope extension to alcohol-sedative interaction scored 3.8 (DEFT2020-D130). The deployment elicitation explicitly states regulatory equivalence requires treating minor lexical differences as critical mismatches (A3) — a fundamentally different decision rule. Web search confirms no French regulatory STS benchmark exists (gap_id 3). For a HIGH-priority dimension, this is a structural validity violation.

**Strengths:**
- STS task type is present [Q22, Q41] and uses standard metrics (Spearman, EDRM) [Q54] — the task interface matches deployment
- PxCorpus NER includes prescription-relevant categories (DOSAGE, DURATION, FREQUENCY, MODE, SUBSTANCE) [Q108], conceptually adjacent to regulatory posology entities
- DEFT2021 NER and DiaMED labels demonstrate fine-grained label inventories exist in principle [Q28, Q45]

**Checklist:**

- **OO-1**: Output labels are calibrated to clinical and biomedical research norms. NER uses UMLS Semantic Groups [Q103, Q106] and clinical/temporal entities [Q104]; STS uses 0–5 general similarity [Q22, Q41]. None calibrated for regulatory norms. — _Sources: Q22, Q41, Q103, Q104, Q106, Q108_
- **OO-2**: Missing categories specific to regional/regulatory contexts: no INN-specific label (subsumed under CHEM — QUAERO-D1, QUAERO-D55); no ATC code label (confirmed full gap — QUAERO-D95); no MA number label (confirmed full gap); no excipient-with-known-effect distinct label; no EMA-templated contraindication qualifier label (QUAERO-D64, QUAERO-D86). STS lacks any regulatory-equivalence rubric (gap_id 3, [WEB-10]). — _Sources: QUAERO-D1, QUAERO-D95, QUAERO-D64, QUAERO-D86, MANTRAGSC-D5_
- **OO-3**: STS scoring encodes a general semantic proximity decision rule [Q22, Q41, Q54] inconsistent with the deployment's regulatory-equivalence rule (A3). Empirical patterns (CLISTER-D10: 2× biomarker difference scored 4.0; CLISTER-D12: positive vs. negative result scored 3.0; DEFT2020-D130: scope extension scored 3.8) systematically under-penalize legally significant micro-differences. — _Sources: Q54, CLISTER-D10, CLISTER-D12, DEFT2020-D130, DEFT2020-D16_
- **OO-4**: Stakeholder-driven taxonomy redesign is required: the deployment system applies regulatory-specific templates as a supplementary layer (A1), but the foundational benchmark provides no INN/ATC/excipient/MA-number granularity. STS would need re-scoring under regulatory equivalence rubric. — _Sources: C2, C3_
- **OO-5**: Severe structural and content validity violation: benchmark scoring functions and label taxonomies do not represent the deployment's decision space. NER lacks fine-grained regulatory categories; STS encodes a different decision rule. C2 and C3 confirm these as cross-cutting CRITICAL findings. — _Sources: C2, C3, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'The first task aims at identifying the degree of similarity within pairs of sentences, from 0 (the less similar) to 5 (the most similar).' (p.3)
- [Q41] 'CLISTER ... 1,000 sentence pairs manually annotated by several annotators, who assigned similarity scores ranging from 0 to 5 ... averaged together to obtain a floating-point number representing the overall similarity.' (p.4)
- [Q54] 'For STS tasks, the models' performance was assessed using two metrics: (1) the Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM)' (p.6)
- [Q103] 'O, GEOG, PHEN, DISO, ANAT, OBJC, PHYS, PROC, DEVI, CHEM and LIVB' (p.14)
- [Q104] 'Clinical: O, and CLINENTITY. Temporal: O, EVENT, ACTOR, BODYPART, TIMEX3 and RML' (p.14)
- [Q106] 'Medline: ANAT, PROC, CHEM, PHYS, GEOG, DEVI, LIVB, OBJC, DISO, PHEN and O. EMEA and Patents: ANAT, PROC, CHEM, PHYS, DEVI, LIVB, OBJC, DISO, PHEN and O.' (p.14)
- [Q108] 'Named-entity recognition: O, ANATOMY, DATE, DOSAGE, DURATION, MEDICAL EXAM, FREQUENCY, MODE, MOMENT, PATHOLOGY, SOSY, SUBSTANCE, TREATMENT and VALUE' (p.14)

*Web sources:*
- [WEB-10] Bannour et al. (2024) confirms nested entity flattening in QUAERO across prior evaluations including DrBenchmark — affecting fine-grained boundary precision

*Dataset analysis:*
- C2 (CRITICAL): No benchmark label set encodes regulatory-specific entity types (INNs distinct from CHEM, ATC codes, excipient nomenclature, MA numbers, contraindication qualifiers)
- C3 (CRITICAL): STS scoring fundamentally misaligned with regulatory equivalence requirements across CLISTER and DEFT2020
- QUAERO-D1, QUAERO-D55: CHEM label conflates INNs, excipients, solvents, antibodies
- QUAERO-D95: ATC codes referenced but unannotated — confirmed full gap
- QUAERO-D64, QUAERO-D86: Contraindication population qualifiers untagged
- MANTRAGSC-D5, MANTRAGSC-D6: CHEM conflates pharmaceuticals with gases and hormones
- CLISTER-D10: 2× quantitative biomarker difference scored 4.0
- CLISTER-D12: Positive vs. negative lab results scored 3.0
- DEFT2020-D130: Sedative+alcohol scope extension scored 3.8
- DEFT2020-D16: Safety warning specificity difference scored 4.0

</details>

**Information gaps:**
- Whether DrBenchmark NER models can be re-purposed via post-hoc filtering to extract INN-specific entities from CHEM-tagged spans

**Requires expert verification:**
- How a regulatory-equivalence STS rubric would be operationalized for EMA SmPC safety-warning paraphrase detection in French

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Annotation documentation is uneven across DrBenchmark's 20 source datasets. Where documented, annotators are biomedical/clinical NLP specialists or automatic taggers: DEFT-2021 was manually annotated for MLC and NER [Q25]; CLISTER STS used multiple annotators averaging 0–5 scores [Q41]; DiaMED used 4 annotators including 'one of which is a medical expert' applying ICD-10 chapter labels [Q45] with documented Cohen's Kappa and Gwet's AC1 IAA [Q46]; CAS POS used Tagex 3 automatic annotation validated at 98% precision [Q42]. No dataset documents regulatory affairs specialists, EMA/ANSM-trained pharmacologists, or legal experts as annotators (M2, gap_id 4 confirmed). The deployment elicitation explicitly anticipates 'systematic disagreements ... on borderline cases — biomedical NLP annotators tend to prioritize clinical relevance over the rigid legal constraints that govern regulatory interpretation' (A4). QUAERO nested entity simplification caused 6.06% (EMEA) and 8.90% (MEDLINE) annotation loss [Q37], with disproportionate impact on fine-grained regulatory boundaries plausible but unverified. CLISTER's STS empirical patterns (CLISTER-D10, CLISTER-D12) and DEFT2020's (DEFT2020-D16, DEFT2020-D130) confirm ground-truth labels diverge from regulatory equivalence judgments. For a HIGH-priority dimension, this is a major convergent validity violation.

**Strengths:**
- DiaMED documents inter-annotator agreement using both Cohen's Kappa and Gwet's AC1 across two sessions [Q45, Q46] — strong methodological hygiene
- DiaMED includes 'one medical expert' in the annotator pool [Q45] — closest available approximation to domain expertise
- CAS POS validated at 98% precision against manual annotations [Q42]
- CLISTER uses multi-annotator averaging [Q41] reducing individual annotator bias on STS scores

**Checklist:**

- **OC-1**: No — ground-truth labels reflect biomedical/clinical NLP annotation conventions. The deployment ground-truth authority is EMA SmPC guidelines, ANSM circulars, and regulatory affairs expert judgment (regional YAML); no benchmark dataset uses this annotation authority. — _Sources: Q41, Q45, M2_
- **OC-2**: Substantial disagreement is expected on borderline cases per elicitation A4 and confirmed empirically: CLISTER-D10 (2× biomarker = 4.0), CLISTER-D12 (positive vs. negative = 3.0), DEFT2020-D130 (scope extension = 3.8), DEFT2020-D16 (specificity difference = 4.0) all show clinical-proximity scoring inconsistent with regulatory equivalence. DEFT2020-D46, DEFT2020-D102 also show high inter-annotator disagreement on borderline pairs. — _Sources: CLISTER-D10, CLISTER-D12, DEFT2020-D16, DEFT2020-D130, DEFT2020-D46_
- **OC-3**: Annotator demographics are partially documented. Documented: DEFT-2021 manually annotated [Q25]; CLISTER multiple annotators [Q41]; DiaMED 4 annotators including one medical expert (ICD-10 expertise) [Q45]; CAS automatic + manual [Q42]. Not documented: regulatory affairs expertise, EMA/ANSM training, or legal expert involvement in any dataset (M2). — _Sources: Q25, Q41, Q42, Q45, M2_
- **OC-4**: Re-annotation by EMA/ANSM-trained regulatory specialists would be required. Web search confirms no published French regulatory NLP benchmark uses regulatory annotation norms (gap_id 4).
- **OC-5**: CLISTER averages multiple annotators to a floating-point reference [Q41] — minority perspectives could be erased. DEFT2020 examples show high variance (DEFT2020-D46 scores span 0–5; DEFT2020-D102 bimodal). DiaMED reports IAA but not how disagreements were resolved [Q46]. — _Sources: Q41, Q46, DEFT2020-D46, DEFT2020-D102_
- **OC-6**: Major convergent validity violation: ground-truth labels are unlikely to correlate with regulatory affairs specialist judgments on borderline entity boundaries or equivalence cases. Nested entity loss (6.06% EMEA, 8.90% MEDLINE) [Q37] further degrades boundary precision for fine-grained regulatory entities — corroborated by independent evaluation [WEB-10]. — _Sources: Q37, WEB-10, M2_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'This dataset is manually annotated in two tasks: (i) multi-label classification and (ii) NER.' (p.3)
- [Q37] 'we simplified the evaluation process by retaining only annotations at the higher granularity level ... which translates into an average loss of 6.06% of the annotations on EMEA and 8.90% on MEDLINE.' (p.3)
- [Q41] 'CLISTER ... 1,000 sentence pairs manually annotated by several annotators, who assigned similarity scores ranging from 0 to 5 ... averaged together to obtain a floating-point number representing the overall similarity.' (p.4)
- [Q42] 'CAS ... annotated for POS tagging with 31 classes using automatic annotations through Tagex 3, with an evaluation conducted by comparing the automatic outputs against manual annotations. This evaluation yielded 98% precision.' (p.4)
- [Q45] 'DiaMed ... manually annotated by several annotators, one of which is a medical expert, into 22 chapters of the International Classification of Diseases, 10th Revision (ICD-10)' (p.4)
- [Q46] 'Table 4: Inter-annotator agreement statistics. κ is referring to Kappa Cohen and G to Gwet's AC1.' (p.4)

*Web sources:*
- [WEB-10] Bannour et al. (2024) corroborates nested entity flattening in QUAERO and confirms no regulatory genre coverage in existing French biomedical NLP benchmarks

*Dataset analysis:*
- M2: No dataset in DrBenchmark documents regulatory affairs specialists; closest is one medical expert with ICD-10 clinical coding expertise (DiaMED)
- Confirmed property #4: No annotator population with documented regulatory affairs expertise across all 11 datasets
- CLISTER-D10, CLISTER-D11, CLISTER-D12: STS labels reflect clinical proximity, not regulatory equivalence
- DEFT2020-D16, DEFT2020-D130: STS labels under-penalize regulatory-relevant scope and specificity differences
- DEFT2020-D46, DEFT2020-D102: High inter-annotator disagreement on borderline pairs
- QUAERO-D64, QUAERO-D86: Contraindication qualifiers untagged in annotations

</details>

**Information gaps:**
- Whether the medical expert in DiaMED has any regulatory training, or only clinical/ICD-10 expertise
- Specific entity types lost in the 6.06% / 8.90% nested-entity simplification on QUAERO

**Requires expert verification:**
- Magnitude of expected divergence between clinical NLP annotators and EMA/ANSM regulatory specialists on a calibration set of borderline regulatory-equivalence STS pairs

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output form is well-aligned with the deployment. Sequence labeling uses SeqEval with IOB2 format predicting on the first token of each word for tokenizer-agnostic evaluation [Q52, Q53]; STS uses Spearman correlation and EDRM [Q54]; classification uses majority-class baselines [Q56]; all models fine-tuned with consistent hyperparameters across four runs with t-test statistical significance [Q51, Q99]. The deployment system consumes label and score outputs in formats matching this protocol (regional YAML infrastructure_notes). Hyperparameter and reproducibility documentation is in the appendix [Q49]. No modality mismatch — the deployment is text-based document processing requiring tag/score outputs, not speech or image modality. This dimension is LOWER priority in elicitation, consistent with no critical concerns.

**Strengths:**
- IOB2 + SeqEval evaluation [Q52, Q53] is the standard format consumed by typical NER pipelines
- Spearman + EDRM for STS [Q54] are standard score outputs
- Tokenizer-agnostic evaluation explicitly ensured [Q53] — first-token-only label prediction
- Reproducibility infrastructure (4 runs averaged, t-test significance, hyperparameters in appendix) [Q51, Q49]
- Fully open-sourced toolkit under MIT license [Q95]

**Checklist:**

- **OF-1**: Yes — output modalities are token-level IOB2 tags for NER and continuous similarity scores for STS [Q52, Q54], directly matching deployment consumption format (text-based document processing per regional YAML). — _Sources: Q52, Q54_
- **OF-2**: Not applicable — deployment is text-based document processing, not speech-based output. PxCorpus is the only spoken-input dataset and its outputs are still text labels [Q44]. — _Sources: Q44_
- **OF-3**: Not applicable to the target population — EU regulatory affairs professionals are highly literate specialists; no accessibility concerns about literacy.
- **OF-4**: No form mismatches identified between benchmark output protocol (IOB2 tags, Spearman/EDRM scores, classification labels) and deployment consumption format. — _Sources: Q52, Q54, Q56_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q49] 'we have integrated all the training details, including hyperparameters, in Appendix A. This information will help users to reproduce and customize the experiments' (p.5)
- [Q51] 'All the models are fine-tuned regarding a strict protocol using the same hyperparameters for each downstream task. The reported results are obtained by averaging the scores from four separate runs ... statistical significance computed using Student's t-test.' (p.5)
- [Q52] 'we chose the SeqEval ... metric in conjunction with the IOB2 format and the training of all the models to predict only the label on the first token of each word' (p.6)
- [Q53] 'It provides a tokenizer-agnostic evaluation and mitigates any correlation between models' performances and the tokenization process.' (p.6)
- [Q54] 'For STS tasks, the models' performance was assessed using two metrics: (1) the Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM)' (p.6)
- [Q56] 'The results of the 8 models are reported in Table 6 and compared to a baseline obtained by considering the majority class for all predictions.' (p.6)

</details>

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** NER labels conflate INNs/excipients/solvents under CHEM and lack ATC code and MA number categories (confirmed full gaps); STS uses general semantic proximity scoring rather than regulatory equivalence (CLISTER-D10, DEFT2020-D130).

**Recommendation:** Define a regulatory NER schema with explicit INN, ATC code, excipient-with-known-effect (per EMA excipients guideline annex), contraindication qualifier (population/dose/condition), special warning, and MA number categories. Develop a regulatory-equivalence STS rubric that treats quantitative differences (dose thresholds, age cutoffs, biomarker values) and scope extensions as critical mismatches per the deployment's decision rule (A3).

### Output Ontology ⚠

**Gap:** Patent subset (Mantra-GSC fr_patents) — a named deployment genre — is an effective blind spot where CamemBERT models generate only 'O' labels [Q73].

**Recommendation:** Treat patent NER as out-of-scope for the foundational benchmark and develop a separate evaluation track using the deployment's regulatory-specific template layer (A1). Track external work on pharmaceutical patent NLP ([WEB-14]) as it matures.

### Input Ontology ⚠

**Gap:** Task taxonomy contains no regulatory-genre NER or regulatory-equivalence STS task; document genres central to deployment (SmPC, PIL, CTD, RMP, patent) are absent or marginal.

**Recommendation:** Construct a supplementary evaluation suite with NER and STS tasks drawn from EU regulatory documents — at minimum SmPC Section 4 (clinical particulars), PIL safety information, and a representative patent claim sample. Use QUAERO EMEA (QUAERO-D37, QUAERO-D51) as the seed and expand with ANSM-published label corpora and EMA EPAR documents.

### Input Content ⚠

**Gap:** Predominantly clinical-narrative content with non-EU contexts (DiaMED Pan African; MORFITT Saudi/Jordan; E3C/DEFT2021 African) and ESSAI investigational compound codes; ~30–40% of DEFT2020 is non-biomedical.

**Recommendation:** Filter DEFT2020 to remove non-biomedical pairs; weight or stratify evaluations by EU vs. non-EU origin; substitute or supplement with a French SmPC/PIL corpus extracted from ANSM and EMA public databases under the appropriate ANSM Feuille de style template ([WEB-8]).

### Output Content ⚠

**Gap:** No dataset documents regulatory affairs specialist annotators; closest is one ICD-10 medical expert in DiaMED [Q45]. Systematic disagreements anticipated on borderline cases (A4).

**Recommendation:** Recruit a small panel of EMA/ANSM-trained regulatory affairs specialists or legal experts to re-annotate (a) a calibration sample of QUAERO EMEA NER spans with the regulatory schema above, and (b) ~100 STS pairs designed to probe regulatory micro-differences. Measure inter-annotator agreement against existing clinical annotations using Cohen's Kappa and Gwet's AC1 (following DiaMED methodology [Q46]).

### Input Form

**Gap:** Tokenization fragmentation behavior on highly technical regulatory nomenclature (INN stems, ATC alphanumeric codes, excipient IUPAC names) is unverified [Q80]; QUAERO sentence-splitting [Q37] may break cross-sentence regulatory entity references.

**Recommendation:** Run a tokenization audit on a held-out set of regulatory nomenclature strings (INN list from WHO, ATC code samples, excipient names from EMA annex) measuring sub-token-per-word ratios across DrBERT-FS, DrBERT-CP, and CamemBERT-bio. Replace sentence splitting with longer-context handling (sliding window or long-context model) for SmPC sections that span legal cross-references.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "It encompasses 20 diversified tasks, including named-entity recognition, part-of-speech tagging, question-answering, semantic textual similarity, and classification." |
| Q2 | 1 | output_form | "We evaluate 8 state-of-the-art pre-trained masked language models (MLMs) on general and biomedical-specific data, as well as English specific MLMs to assess their cross-lingual capabilities." |
| Q3 | 1 | output_form | "Our experiments reveal that no single model excels across all tasks, while generalist models are sometimes still competitive." |
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
| Q16 | 2 | input_content | "To our knowledge, aside the multilingual benchmark BigBIO (Fries et al., 2022) which includes only 4 corpora for French and is initially intended for generative text completion under zero-shot scenario, no large benchmark specialized in the French biomedical field exists." |
| Q17 | 2 | input_ontology | "Our proposed benchmark comprises 20 French biomedical language understanding tasks, one of which is specifically created for this benchmark." |
| Q18 | 2 | input_ontology | "A variety of tasks with different requirements and objectives: Part-of-Speech (POS) tagging, Multi-class, Multi-label and Intent classification, Named-Entity Recognition (NER), Multiple-Choice Question-Answering (MCQA), and Semantic Textual Similarity (STS)." |
| Q19 | 2 | input_content | "A diverse range of data origins: Scientific literature, clinical trials, clinical cases, speech transcriptions, and more as described in Table 2." |
| Q20 | 2 | input_ontology | "Please note that within DrBenchmark, we include classical tasks like NER and POS tagging, as well as more specific and challenging tasks like MCQA and multi-label classification." |
| Q21 | 3 | input_content | "DEFT-2020 (Cardon et al., 2020) contains clinical cases, encyclopedia and drug labels introduced in the 2020 edition of an annual French Text Mining Challenge, called DEFT, and annotated for two tasks: (i) textual similarity and (ii) multi-class classification." |
| Q22 | 3 | output_ontology | "The first task aims at identifying the degree of similarity within pairs of sentences, from 0 (the less similar) to 5 (the most similar)." |
| Q23 | 3 | output_ontology | "The second task consists in identifying, for a given sentence, the most similar sentence among three sentences provided." |
| Q24 | 3 | input_content | "DEFT-2021 (Grouin et al., 2021) is a subset of 275 clinical cases taken from the 2019 edition of DEFT." |
| Q25 | 3 | output_content | "This dataset is manually annotated in two tasks: (i) multi-label classification and (ii) NER." |
| Q26 | 3 | output_ontology | "The multi-label classification task focuses on identifying the patient's clinical profile based on the diseases, signs, or symptoms mentioned in the clinical cases." |
| Q27 | 3 | output_ontology | "The dataset is annotated with 23 axes from Chapter C of the Medical Subject Headings (MeSH)." |
| Q28 | 3 | output_ontology | "The second task involves fine-grained information extraction for 13 types of entities (more detail in Appendix B.7)." |
| Q29 | 3 | input_content | "E3C (Magnini et al., 2020) is a multilingual dataset of clinical cases annotated for the NER task." |
| Q30 | 3 | output_ontology | "It consists of two types of annotations (more detail in Appendix B.4): (i) clinical entities (e.g., pathologies), (ii) temporal information and factuality (e.g., events)." |
| Q31 | 3 | input_form | "While the dataset covers 5 languages, only the French portion is retained for the benchmark." |
| Q32 | 3 | input_form | "Since the dataset does not come with pre-defined subsets, we performed a 70 / 10 / 20 random split, as described in Table 3." |
| Q33 | 3 | input_content | "The QUAERO French Medical Corpus (Névéol et al., 2014), simply referred to as QUAERO in this paper, contains annotated entities and concepts for NER tasks." |
| Q34 | 3 | input_content | "The dataset covers two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE." |
| Q35 | 3 | output_ontology | "10 entity categories corresponding to the UMLS Semantic Groups (Lindberg et al., 1993) were annotated (more detail in Appendix B.3)." |
| Q36 | 3 | output_content | "In total, 26,409 entity annotations were mapped to 5,797 unique UMLS concepts." |
| Q37 | 3 | output_content | "Due to the presence of nested entities in annotations, we simplified the evaluation process by retaining only annotations at the higher granularity level from the BigBio (Fries et al., 2022) implementation, following the approach described in Touchent et al. (2023), which translates into an average loss of 6.06% of the annotations on EMEA and 8.90% on MEDLINE. Additionally, considering that some documents from EMEA exceed the maximum input sequence length that most current language models can handle, we decided to split these documents into sentences." |
| Q38 | 4 | input_content | "MorFITT (Labrak et al., 2023) is a multi-label dataset annotated with medical specialties. It contains 3,624 biomedical abstracts from PMC Open Access. It has been annotated across 12 medical specialties (more detail in Appendix B.5), for a total of 5,116 annotations." |
| Q39 | 4 | input_ontology | "FrenchMedMCQA (Labrak et al., 2022) is a Multiple-Choice Question-Answering (MCQA) dataset for biomedical domain. It contains 3,105 questions coming from real exams of the French medical specialization diploma in pharmacy, integrating single and multiple answers. The first task consists of automatically identifying the set of correct answers among the 5 proposed for a given question. The second task consists of identifying the number of answers (between 1 and 5) supposedly correct for a given question." |
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
| Q54 | 6 | output_ontology | "For STS tasks, the models' performance was assessed using two metrics: (1) the Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM), as defined by the original authors of the DEFT-2020 dataset (Cardon et al., 2020)." |
| Q55 | 6 | input_ontology | "In Section 5.1, we compare the results obtained by each model within DrBenchmark, which permits to position a wide range of state-of-the-art models in the biomedical field across various NLP tasks." |
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
| Q73 | 7 | input_content | "However, all the models based on CamemBERT face difficulties in corpora with limited amount of data, such as MantraGSC Patents, where they fail to generate labels other than 'O'." |
| Q74 | 7 | output_form | "On the other hand, in the same low-resource scenarios, CamemBERTa models exhibit greater robustness and achieve superior performance." |
| Q75 | 8 | input_form | "Tokenizers play a crucial role in MLMs by utilizing size-limited vocabularies to split texts into sub-units, aiming to handle out-of-vocabulary (OOV) words." |
| Q76 | 8 | input_content | "Due to variations in the training data, vocabularies differ across different models, as illustrated in Figure 2." |
| Q77 | 8 | input_form | "So far, there has been a prevailing notion in the community that excessive segmentation of words in tokenization leads to a loss of morphological form and semantic meaning, introducing noise and adversely affecting performance (Church, 2020; Hofmann et al., 2021; Bostrom and Durrett, 2020)." |
| Q78 | 8 | input_form | "However, our experiments, as shown in Table 7, reveal that FlauBERT is the model with the least word segmentation (1.43 in average), while DrBERT-CP tends to have the highest average segmentation (1.90 in average)." |
| Q79 | 8 | input_form | "Surprisingly, when comparing the performance of these two models on the benchmark tasks, we observe that DrBERT-CP outperforms FlauBERT on 16 out of the 20 tasks, thus contradicting previous conclusions drawn by the community." |
| Q80 | 8 | input_form | "Yet, tokenization, as it is currently done in MLMs, seems to play a minor role in the performance of systems." |
| Q81 | 8 | input_ontology | "Table 8 summarizes the results obtained on average by the considered MLMs when aggregating the tasks into one of the five designated categories: POS, NER, MCQA, MCC (Multi-class classification), MLC (Multi-label classification), or STS tasks." |
| Q82 | 8 | output_form | "Upon analyzing the average performance by task category, it becomes evident that the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS." |
| Q83 | 9 | input_ontology | "In this paper, we introduced DrBenchmark, the first large language understanding benchmark tailored for the French biomedical domain." |
| Q84 | 9 | input_ontology | "We conducted a qualitative evaluation of 8 state-of-the-art masked language models (MLMs) on this comprehensive benchmark, encompassing 20 diverse downstream tasks." |
| Q85 | 9 | output_form | "Our findings illuminate the limitations of generalist models in tackling complex biomedical tasks, emphasizing the importance of employing domain-specific models to achieve peak performance." |
| Q86 | 9 | output_form | "We have observed that several biomedical tasks in DrBenchmark exhibit relatively poor performance, even when utilizing specialized biomedical models." |
| Q87 | 9 | output_ontology | "We postulate that the models examined in this study, here state-of-the-art MLMs, may not be the most effective choices for specific tasks such as question-answering or multi-label classification." |
| Q88 | 9 | output_form | "The quantitative study we conducted on the PLMs requires further in-depth analysis to comprehend the impact of different parameters." |
| Q89 | 9 | input_form | "Firstly, we investigated the influence of tokenizers based on the average number of sub-tokens they produce per word." |
| Q90 | 9 | input_form | "Various tokenization algorithms are employed, depending on the model under examination." |
| Q91 | 9 | input_content | "The size of the data has not been thoroughly investigated, particularly the significance of the pre-training data size, especially specialized data in the biomedical field." |
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
| WEB-1 | https://www.ema.europa.eu/en/about-us/what-we-do/reform-eu-pharmaceutical-legislation |
| WEB-2 | https://www.europarl.europa.eu/legislative-train/theme-a-new-plan-for-europe-s-sustainable-prosperity-and-competitiveness/file-revision-of-the-pharmaceutical-legislation |
| WEB-3 | https://ec.europa.eu/health/system/files/2016-11/smpc_guideline_rev2_en_0.pdf |
| WEB-4 | https://www.ema.europa.eu/en/committees/working-parties-other-groups/chmp/smpc-advisory-group |
| WEB-5 | https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/product-information-requirements/product-information-qrd-templates-human |
| WEB-6 | https://www.ema.europa.eu/en/documents/template-form/qrd-product-information-template-version-104-highlighted_en.pdf |
| WEB-7 | https://www.pharmalex.com/thought-leadership/blogs/the-complex-landscape-of-french-regulatory-affairs/ |
| WEB-8 | https://ansm.sante.fr/uploads/2022/07/01/20220701-amm-pdtaut-doc004a-v01-recommandations-nationales-trad-amm-eng.pdf |
| WEB-9 | https://www.hma.eu/fileadmin/dateien/Human_Medicines/CMD_h_/procedural_guidance/Application_for_MA/CMDh_258_2012_Rev25_2023_05_clean_-_BlueBox_requirements.pdf |
| WEB-10 | https://arxiv.org/abs/2403.19726 |
| WEB-11 | https://incountry.com/blog/french-health-data-compliance-and-how-to-achieve-it/ |
| WEB-12 | https://secureprivacy.ai/blog/data-residency-requirements-eu-vs-us-explained |
| WEB-13 | https://www.hma.eu/human-medicines/cmdh/templates/qrd.html |
| WEB-14 | https://arxiv.org/pdf/2504.20598 |

---

### Dataset Analysis

## Dataset Analysis Report

**Benchmark:** DrBenchmark — A Large Language Understanding Benchmark for the Biomedical French Language
**Datasets analyzed:** 11 datasets — QUAERO (EMEA config), FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC (fr_medline config), E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI
**Analysis date:** 2025-07-10

---

### Per-Dataset Fit Assessment

#### DrBenchmark/QUAERO (EMEA config)
- **Task:** NER (token classification, IOB2, 10 UMLS Semantic Group classes)
- **Deployment fit:** Partial — The EMEA configuration is the single dataset in DrBenchmark drawn directly from EU drug approval documents (patient information leaflets and SmPC-style texts), making it the closest available proxy for the deployment genre. Authentic regulatory source text is confirmed by QUAERO-D37 and QUAERO-D51. However, the label schema conflates INNs, excipients, and other chemicals under a single CHEM class (QUAERO-D1, QUAERO-D55), no ATC code entity type exists (QUAERO-D95), and contraindication population qualifiers are largely untagged (QUAERO-D64, QUAERO-D86).
- **Key concerns:**
  - CHEM label conflates INNs, excipients, solvents, and antibodies; downstream INN-vs-excipient distinction required by the deployment is impossible without post-processing (QUAERO-D1, QUAERO-D55)
  - ATC codes referenced in source text but not annotated as entities (QUAERO-D95)
  - Contraindication qualifiers (age thresholds, population conditions) receive no entity label, preventing regulatory-equivalence NER evaluation (QUAERO-D64, QUAERO-D86)
  - Nested entity simplification resulted in 6.06% annotation loss on EMEA subset, likely disproportionately affecting fine-grained regulatory entity boundaries
  - Some examples are uninformative administrative fragments (QUAERO-D15, QUAERO-D41, QUAERO-D84)

#### DrBenchmark/FrenchMedMCQA
- **Task:** Multiple-Choice Question Answering (MCQA) — pharmacy diploma exam questions
- **Deployment fit:** Weak — The deployment requires NER and STS; MCQA is a categorically different task type producing answer-index outputs rather than entity spans or similarity scores. Drug INNs appear only as answer choices in exam format (FRENCHMEDMCQA-D13, FRENCHMEDMCQA-D74), not as extraction targets in regulatory prose.
- **Key concerns:**
  - Fundamental task-type mismatch: output ontology is closed-set answer selection, bearing no relation to IOB2 NER labels or STS scores (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D2)
  - All content is academic clinical pharmacology exam prose, not legally constrained regulatory document text (FRENCHMEDMCQA-D105)
  - SmPC referenced in one answer option as a definitional item, not as source text (FRENCHMEDMCQA-D105)
  - Potential temporal validity concern for policy-adjacent questions (FRENCHMEDMCQA-D94)

#### DrBenchmark/DEFT2020
- **Task:** STS (sentence similarity scoring, 0–5 scale) and sentence selection
- **Deployment fit:** Partial — The STS task type is directly relevant. Some sentence pairs contain drug-label register text with excipient-based contraindications and safety warnings (DEFT2020-D18, DEFT2020-D16, DEFT2020-D52). However, approximately 30–40% of examples are entirely non-biomedical (DEFT2020-D1, DEFT2020-D3, DEFT2020-D5, DEFT2020-D6), and the scoring calibration does not distinguish legally significant micro-differences from general semantic proximity (DEFT2020-D16, DEFT2020-D130).
- **Key concerns:**
  - Large non-biomedical content fraction (beekeeping, railway infrastructure, history, geography) that will skew STS model representations away from regulatory register (DEFT2020-D1, DEFT2020-D3, DEFT2020-D5, DEFT2020-D6)
  - STS scores treat regulatory-relevant scope extensions (additional substance classes, alcohol interactions) as high-similarity rather than flagging them as potential mismatches (DEFT2020-D16, DEFT2020-D130)
  - Obligation modality differences (precautionary framing vs. direct instruction) scored identically under general proximity (DEFT2020-D4)
  - High inter-annotator disagreement on borderline pairs (DEFT2020-D46, DEFT2020-D102), with no regulatory-expert annotation to resolve them

#### DrBenchmark/MORFITT
- **Task:** Multi-label classification of biomedical abstracts by medical specialty (12 classes)
- **Deployment fit:** Weak — Document-level specialty classification is not a deployment task. No regulatory document genres present; all content is PMC Open Access research abstracts. Multiple examples originate from non-EU clinical contexts (MORFITT-D10, MORFITT-D11) and significant veterinary content is present (MORFITT-D12, MORFITT-D13, MORFITT-D14).
- **Key concerns:**
  - Task-type mismatch: document-level specialty classification produces no NER or STS outputs relevant to the deployment (MORFITT-D17)
  - No regulatory entity types present; label taxonomy (12 specialty classes) has no mapping to EMA entity categories (MORFITT-D17)
  - Non-EU geographic origin of multiple abstracts (Saudi Arabia, Jordan, Canada) introduces register and terminology variation inconsistent with EMA/ANSM French (MORFITT-D10, MORFITT-D11)
  - Veterinary content (animal disease, equine parasitology, canine otitis) has no deployment relevance (MORFITT-D12, MORFITT-D13, MORFITT-D14)
  - Translated abstracts from English may not reflect native French regulatory register (MORFITT-D8, MORFITT-D9)

#### DrBenchmark/CLISTER
- **Task:** STS (sentence similarity, 0–5 continuous scale) on clinical case sentence pairs
- **Deployment fit:** Partial — STS task type is relevant. Some pairs contain drug mentions (CLISTER-D2, CLISTER-D3, CLISTER-D4) adjacent to posology expressions. However, all text derives exclusively from clinical case narratives, and the scoring calibration produces critical failures for regulatory equivalence: a 2× quantitative difference in a biomarker value receives a score of 4.0 (CLISTER-D10), and positive vs. negative lab results receive 3.0 (CLISTER-D12).
- **Key concerns:**
  - Exclusively clinical case register; no regulatory document text present (CLISTER-D1 through CLISTER-D8)
  - STS scores are calibrated for clinical narrative proximity, not regulatory equivalence; quantitative differences (2× biomarker, route of administration) are systematically under-penalized (CLISTER-D10, CLISTER-D11, CLISTER-D12)
  - Brand names used alongside INNs in clinical prose, inconsistent with EMA INN-only convention (CLISTER-D6)
  - Some examples contain tabular pharmacokinetic rows or English prescription abbreviations (CLISTER-D15, CLISTER-D16), reducing ecological validity
  - No annotator documentation confirms regulatory expertise

#### DrBenchmark/MANTRAGSC (fr_medline config sampled)
- **Task:** Biomedical NER (IOB2, UMLS Semantic Group classes) across EMEA, MEDLINE, and patent subsets
- **Deployment fit:** Weak for the MEDLINE config sampled; the EMEA and patent configs are more relevant but were not the primary sample. The sampled MEDLINE content is exclusively historical French academic titles with no regulatory genre content (MANTRAGSC-D1, MANTRAGSC-D4). The patent config is a named deployment document type but CamemBERT-based models fail entirely on it. The dataset is critically small (~100 French MEDLINE examples).
- **Key concerns:**
  - Sampled config (fr_medline) contains only historical biomedical MEDLINE titles, not EMEA or patent text (MANTRAGSC-D1, MANTRAGSC-D4)
  - CHEM label conflates pharmaceutical substances with gases, hormones, and other chemicals — no INN-specific granularity (MANTRAGSC-D5, MANTRAGSC-D6)
  - No dosage, route, mode, or posology sub-entity labels (MANTRAGSC-D7, MANTRAGSC-D8)
  - Extremely small dataset size (~100 French MEDLINE training examples) limits statistical reliability (MANTRAGSC-D9, MANTRAGSC-D10)
  - Some content reflects sub-Saharan African epidemiology and veterinary contexts, non-EU register (MANTRAGSC-D11, MANTRAGSC-D12, MANTRAGSC-D13)
  - Patent subset is an effective blind spot: CamemBERT models generate only 'O' labels on MantraGSC Patents

#### DrBenchmark/E3C
- **Task:** Clinical NER — French_clinical (CLINENTITY only) and French_temporal (EVENT, ACTOR, BODYPART, TIMEX3, RML)
- **Deployment fit:** Weak — The NER task type is relevant, but the label schema captures only clinical entities (pathologies, temporal expressions) and explicitly excludes all drug-regulatory entity types. Drug names and dosages appearing in the source text receive O tags throughout (E3C-D3, E3C-D4, E3C-D8), representing the inverse of what the deployment requires.
- **Key concerns:**
  - CLINENTITY schema labels pathologies and symptoms; all drug names, INNs, dosages, and routes present in text receive O tags (E3C-D3, E3C-D4, E3C-D8, E3C-D11)
  - No label corresponds to any deployment-required regulatory entity type (E3C-D6, E3C-D7)
  - Some clinical cases originate from non-EU African settings, introducing geographic and register mismatch (E3C-D9, E3C-D10)
  - Tokenization artifacts (backslash-n tokens) visible in some examples (E3C-D13)

#### DrBenchmark/PxCorpus
- **Task:** Intent classification (4 classes) and NER (38 classes covering prescription entities) on transcribed spoken prescriptions
- **Deployment fit:** Weak — The NER entity types (SUBSTANCE, DOSAGE, MODE, FREQUENCY, DURATION) are conceptually the closest to deployment targets across DrBenchmark's spoken-language datasets. However, the input modality is transcribed speech, introducing pervasive ASR artifacts, dysfluencies, and informal register that are fundamentally incompatible with the formal written regulatory prose of SmPCs, patient leaflets, and CTD modules (PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D6, PXCORPUS-D8).
- **Key concerns:**
  - Critical modality mismatch: all utterances are transcribed spoken language with filler words, truncation artifacts, profanity, and system dialogue prompts embedded (PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D6, PXCORPUS-D8)
  - No ATC codes, excipient nomenclature, EMA-standard contraindication qualifiers, or INN-vs-brand distinction in label schema (PXCORPUS-D12, PXCORPUS-D13)
  - Severe class imbalance: `replace` (most relevant to inconsistency detection) has only 3 examples in the sample (PXCORPUS-D10, PXCORPUS-D11)
  - `none` class contaminated by meta-commentary and simulation artifacts (PXCORPUS-D14, PXCORPUS-D15, PXCORPUS-D16)
  - ASR transcription errors produce non-canonical drug name forms (PXCORPUS-D20, PXCORPUS-D21, PXCORPUS-D22)

#### DrBenchmark/DiaMED
- **Task:** Multi-class classification (ICD-10 chapter-level assignment)
- **Deployment fit:** Weak — ICD-10 chapter classification is a clinical coding task with no structural relationship to the deployment's NER or STS requirements. All source material originates from the Pan African Medical Journal (sub-Saharan African clinical cases), introducing both genre mismatch and geographic register mismatch with EU regulatory French (DIAMED-D2, DIAMED-D9).
- **Key concerns:**
  - Task-type mismatch: ICD-10 chapter classification produces no NER or STS output relevant to the deployment
  - Exclusive geographic origin from Pan African Medical Journal introduces non-EU clinical context and potential terminology inconsistency with EMA/ANSM French register (DIAMED-D2, DIAMED-D9, DIAMED-D12)
  - Drug mentions are informal narrative abbreviations (e.g., "D4T", "3TC"), not INN-formatted regulatory text (DIAMED-D1)
  - Severe class imbalance (Neoplasms: 165 examples; R00-R99: 1 example)
  - Annotation by 4 annotators with ICD-10 clinical coding expertise has no relationship to regulatory annotation standards

#### DrBenchmark/DEFT2021
- **Task:** NER (13 clinical entity types) and multi-label classification on clinical case reports
- **Deployment fit:** Weak — NER task type is relevant, but the schema covers clinical entity types (anatomy, pathology, treatment, temporal) rather than regulatory entity types. Drug names appear throughout the text and receive treatment/substance tags, but without INN-specific granularity, ATC codes, excipient distinction, or regulatory posology structure (DEFT2021-D55, DEFT2021-D158).
- **Key concerns:**
  - Clinical entity schema does not include INN, ATC code, excipient, or contraindication qualifier categories (DEFT2021-D55, DEFT2021-D158)
  - Drug names tagged as generic clinical substance entities identical to other treatment terms, precluding regulatory-grade INN extraction (DEFT2021-D80, DEFT2021-D99)
  - Some case reports originate from non-EU African settings (DEFT2021-D108, DEFT2021-D166)
  - Annotation by DEFT challenge participants with clinical/biomedical NLP expertise; no regulatory affairs specialist involvement documented
  - Sentence-boundary artifacts (punctuation-only tokens) present in sample (DEFT2021-D26, DEFT2021-D31, DEFT2021-D42)

#### DrBenchmark/CAS
- **Task:** POS tagging (31 classes), negation/speculation NER, and negation/speculation classification on clinical cases
- **Deployment fit:** Weak — POS tagging and negation/speculation classification are proxy tasks at best. All content is clinical case narrative. Drug mentions appear incidentally (CAS-D22, CAS-D33) but in informal clinical prose without regulatory structure. No label in any CAS configuration represents a regulatory entity or compliance-relevant category.
- **Key concerns:**
  - Label space (negation/speculation classes, POS tags) captures linguistic properties irrelevant to regulatory entity extraction or compliance verification (CAS task schema)
  - Clinical case genre entirely absent from regulatory document types; no SmPC, leaflet, or CTD content (CAS-D5, CAS-D15)
  - Drug mentions in informal narrative posology format, not EMA-templated expressions (CAS-D22, CAS-D29, CAS-D63)
  - POS annotations produced by automatic tagger (Tagex 3); no regulatory expertise required or applied

#### DrBenchmark/ESSAI
- **Task:** POS tagging (36 classes), negation/speculation NER, and negation/speculation classification on clinical trial protocols
- **Deployment fit:** Weak — Clinical trial protocol text is a distinct genre from regulatory submission documents. Dosage and frequency expressions appear in narrative form (ESSAI-D10, ESSAI-D11) and investigational compound codes (MEDI9197, BMS-986179, CMAK683X2101) dominate drug mentions (ESSAI-D7, ESSAI-D8, ESSAI-D9), which are absent from marketed drug labeling. Patient-addressed informal register appears in some examples (ESSAI-D13, ESSAI-D14).
- **Key concerns:**
  - Investigational compound codes, not INNs, are the dominant drug identifiers; these do not appear in SmPCs or patient leaflets (ESSAI-D7, ESSAI-D8, ESSAI-D9)
  - Clinical trial protocol genre differs structurally from regulatory submission documents; informed-consent second-person register is absent from SmPCs and CTDs (ESSAI-D13, ESSAI-D14)
  - Negation/speculation label taxonomy unrelated to regulatory compliance categories (ESSAI-D12)
  - No patent language, excipient lists, contraindication sections, or SmPC section headers observed across 75 sampled examples

---

### Cross-Cutting Findings

#### CRITICAL

**C1 — Universal regulatory document genre absence across all datasets except QUAERO EMEA**
Every dataset except QUAERO's EMEA configuration is drawn exclusively from clinical case narratives, academic research abstracts, clinical trial protocols, or transcribed spoken prescriptions. No dataset contributes SmPC sections, patient information leaflets, CTD modules, EU Risk Management Plans, or pharmaceutical patent claims as primary source text. This pattern is confirmed across CLISTER-D1 through CLISTER-D8, E3C-D3, DEFT2021-D3, CAS-D5, ESSAI-D1, DIAMED-D2, MORFITT-D4, and MANTRAGSC-D1. The benchmark's single partial coverage point (QUAERO EMEA) itself represents only a minority subset within that dataset, and even there the label schema is insufficient for the deployment's regulatory entity types.

**C2 — Systematic output ontology gap: no benchmark label set encodes regulatory-specific entity types**
Across all NER-bearing datasets (QUAERO, E3C, MANTRAGSC, DEFT2021, PxCorpus), no label explicitly represents INNs as distinct from other chemical entities, ATC codes, excipient nomenclature with Ph.Eur./INCI standards, EMA-templated contraindication qualifiers, or marketing authorization numbers. Drug entities are captured under broad UMLS CHEM/SUBSTANCE categories (QUAERO-D1, QUAERO-D55, MANTRAGSC-D5, MANTRAGSC-D6) or generic treatment/substance clinical tags (DEFT2021-D55, E3C-D3, E3C-D4), none of which enable the regulatory-grade entity discrimination the deployment requires. ATC codes are confirmed as a full gap with no analog in any dataset label set (QUAERO-D95).

**C3 — STS scoring calibration is fundamentally misaligned with regulatory equivalence requirements across both STS datasets**
Both CLISTER and DEFT2020 use a 0–5 general semantic proximity scale annotated by clinical/research annotators without any regulatory equivalence rubric. CLISTER-D10 shows a 2× quantitative biomarker difference scored 4.0 (high similarity); CLISTER-D12 shows positive vs. negative lab results scored 3.0; DEFT2020-D16 shows a safety warning where added substance class specificity is absorbed into a 4.0 score; DEFT2020-D130 shows a scope extension (adding alcohol to sedative interaction warning) scored 3.8. These patterns directly instantiate the benchmark YAML's confirmed "full gap" for STS scoring calibration, meaning models trained or evaluated on these datasets will not learn to treat regulatory micro-differences as critical mismatches.

#### MAJOR

**M1 — Non-biomedical content contamination in DEFT2020 STS training distribution**
Approximately 30–40% of DEFT2020 examples are non-biomedical (DEFT2020-D1, DEFT2020-D3, DEFT2020-D5, DEFT2020-D6). Models trained on this distribution will develop STS representations partly calibrated to general encyclopedic French similarity rather than biomedical or regulatory language, reducing the benchmark's diagnostic validity for the deployment's regulatory equivalence task.

**M2 — Annotator population mismatch across all datasets**
No dataset in DrBenchmark documents regulatory affairs specialists, EMA/ANSM-trained pharmacologists, or legal experts as annotators. The closest documented expertise is one medical expert with ICD-10 clinical coding knowledge (DiaMED) and automated annotation validated by clinical NLP researchers (CAS). This confirmed benchmark-wide gap means that ground-truth labels on borderline entity boundary and equivalence cases systematically reflect clinical biomedical conventions rather than the rigid legal constraints governing regulatory annotation, as anticipated by the elicitation response on OC.

**M3 — Spoken/transcribed modality introduces irreducible register mismatch for PxCorpus**
PxCorpus is the dataset with entity types (SUBSTANCE, DOSAGE, MODE, FREQUENCY, DURATION) most conceptually adjacent to the deployment's NER targets, yet its input modality is transcribed speech with pervasive ASR artifacts, profanity, system dialogue prompts, and dysfluencies (PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D6, PXCORPUS-D8). Models evaluated on PxCorpus performance are being assessed on a fundamentally different input distribution from the formal written regulatory French the system will encounter.

**M4 — Non-EU geographic origin of clinical case content across multiple datasets**
DiaMED (exclusively Pan African Medical Journal; DIAMED-D2, DIAMED-D9), MORFITT (Saudi Arabia, Jordan, Canada; MORFITT-D10, MORFITT-D11), MANTRAGSC (Dakar, Cameroon; MANTRAGSC-D11, MANTRAGSC-D12), DEFT2021 (Africa, Morocco; DEFT2021-D108, DEFT2021-D166), and E3C (Morocco, Africa; E3C-D9, E3C-D10) all contain cases with non-EU clinical contexts. These may introduce terminology conventions, abbreviation norms, or institutional registers inconsistent with EMA/ANSM French regulatory prose, compounding the domain register mismatch.

**M5 — Patent subset remains an effective blind spot despite nominal coverage in MANTRAGSC**
The MantraGSC fr_patents config is the only benchmark asset touching patent language — a named deployment document type — yet CamemBERT-based models generate only 'O' labels on this subset. The fr_medline config was sampled rather than the patent config, confirming the patent genre was not directly inspected. An independent 2025 arXiv study (arXiv:2504.20598) corroborates that pharmaceutical patent text has distinct NLP challenges that biomedical NER models do not address.

**M6 — Investigational compound codes dominate drug mentions in ESSAI, absent from regulatory labeling**
ESSAI contains numerous experimental compound identifiers (MEDI9197, BMS-986179, CMAK683X2101, LY3200882; ESSAI-D7, ESSAI-D8, ESSAI-D9) that do not appear in any marketed drug labeling document. A model evaluated on ESSAI NER performance is being assessed on entities that have no analog in the SmPCs, patient leaflets, or CTD modules the deployment system processes.

#### MINOR

**m1 — Noisy and uninformative examples dilute benchmark quality across multiple datasets**
Administrative fragments (QUAERO-D15, QUAERO-D41, QUAERO-D84), punctuation-only token artifacts (DEFT2021-D26, DEFT2021-D31, DEFT2021-D42), truncated ASR utterances (PXCORPUS-D4, PXCORPUS-D17, PXCORPUS-D18), and all-O entity-free MANTRAGSC examples (MANTRAGSC-D9, MANTRAGSC-D10) are present across datasets. These reduce benchmark signal density without affecting the core validity concerns.

**m2 — Tokenization artifacts visible in E3C and PxCorpus**
Backslash-n escape sequences appear as separate tokens in E3C (E3C-D13), and embedded system dialogue prompts appear in PxCorpus (PXCORPUS-D8). These artifacts are unlikely to affect aggregate performance substantially but could affect IOB2 boundary detection in affected examples.

---

### Confirmed Properties

The following properties are confirmed across datasets by content inspection:

1. **French language throughout, Latin script**: All datasets confirmed as French-language text with standard diacritics. No script mismatch or non-French content. CLISTER-D16 (English abbreviations) is an isolated exception.
2. **Clinical case narrative dominance**: The overwhelming majority of DrBenchmark content across all datasets is clinical case report prose — a register confirmed to be distinct from regulatory French.
3. **UMLS Semantic Groups as the NER ceiling for pharmacological entities**: The most granular drug-entity annotation available across QUAERO, MANTRAGSC, and related datasets is the CHEM Semantic Group, which conflates all pharmaceutical, chemical, and biological entities without regulatory-grade subtyping.
4. **No annotator population with documented regulatory affairs expertise**: Confirmed across all 11 datasets; the closest approximation is one medical expert with ICD-10 expertise (DiaMED) and clinical pharmacology exam authority (FrenchMedMCQA).
5. **QUAERO EMEA as the only direct regulatory genre source**: Content inspection confirms QUAERO EMEA-D37 and QUAERO-D51 as authentic EU regulatory document text; this is the unique regulatory-genre asset within the benchmark.
6. **STS calibration for clinical proximity, not regulatory equivalence**: Confirmed across CLISTER and DEFT2020 by examples showing that quantitative differences, route-of-administration distinctions, and scope extensions in safety language receive high similarity scores inconsistent with regulatory equivalence requirements.

---

### Content Coverage Summary

**What is represented:** DrBenchmark collectively covers French clinical case narratives (CLISTER, CAS, E3C, DiaMED, DEFT2021), biomedical research abstracts (MORFITT), clinical trial protocols (ESSAI), transcribed prescription dialogues (PxCorpus), pharmacy diploma exam questions (FrenchMedMCQA), biomedical MEDLINE titles (MANTRAGSC fr_medline), and a small subset of EU drug label text (QUAERO EMEA). Drug-related content is present in multiple datasets but consistently in clinical or research register rather than regulatory register.

**What is absent relative to deployment needs:**
- **SmPC sections** as primary NER or STS source text: absent except in the QUAERO EMEA minority subset
- **Patient information leaflets** as a distinct, representative corpus: partially present in QUAERO EMEA but uncharacterized as a separate sub-genre
- **CTD module language**: entirely absent
- **EU Risk Management Plans**: entirely absent
- **Pharmaceutical patent claim language**: nominally present in MANTRAGSC fr_patents config but constituting an effective model blind spot
- **ATC codes** as annotated entities: confirmed full gap across all datasets
- **INN-specific NER labels** (distinct from other CHEM entities): confirmed full gap
- **Excipient nomenclature** with Ph.Eur./INCI distinction: confirmed full gap
- **STS pairs annotated for regulatory equivalence**: confirmed full gap; no published benchmark exists
- **Regulatory affairs specialist annotators**: confirmed full gap; no dataset documents this annotator profile

---

### Limitations

1. **Patent config not directly sampled**: MANTRAGSC fr_patents was not the sampled configuration; the confirmed CamemBERT failure and patent-as-blind-spot finding derives from benchmark paper documentation rather than direct content inspection of patent examples.
2. **QUAERO MEDLINE config not sampled**: Only the EMEA configuration was analyzed. The MEDLINE config (biomedical titles) would likely show weaker regulatory fit, but this was not directly verified.
3. **DEFT2020 task_2 not sampled**: Only task_1 (sentence scoring) was analyzed; task_2 (sentence selection) may have a different content distribution.
4. **DEFT2021 classification config not sampled**: Only the NER configuration was analyzed; the multi-label classification config may have different content properties.
5. **CAS configs beyond POS not sampled**: The ner_neg, ner_spec, and cls configs were not directly inspected; the finding that label space is irrelevant to the deployment is confirmed structurally from schema, not from sampled examples of those configs.
6. **Sample-based analysis**: All per-dataset analyses are based on sampled examples (34–234 examples per dataset); rare regulatory-relevant content may be present but unobserved in the samples.
7. **No inspection of QUAERO EMEA proportions**: The fraction of patient information leaflet vs. SmPC-style text within the EMEA config could not be quantified from the sample.
8. **Nested entity loss impact unverifiable**: The 6.06% annotation loss in QUAERO EMEA from nested entity simplification is documented but the specific entity types lost cannot be determined from current sample.

---

### Cited Evidence

- **QUAERO-D1**: 1 | IC, OO | Excipient list from SmPC; CHEM tags conflate with active substance tags
- **QUAERO-D2**: 2 | IC | INN (lépirudine) in drug label context
- **QUAERO-D15**: 15 | IC | Fragmented multilingual address text
- **QUAERO-D34**: 34 | IC, OO | Multi-component excipient; nested entity simplification risk
- **QUAERO-D37**: 37 | IC | EU marketing authorization language confirming regulatory genre
- **QUAERO-D41**: 41 | IC | Near-empty example (tokens=['o', '.'])
- **QUAERO-D51**: 51 | IC, IF | EMEA document header confirming authentic source
- **QUAERO-D55**: 55 | IC, OO | INN and excipients conflated under CHEM
- **QUAERO-D64**: 64 | OO, OC | Contraindication content; population qualifiers largely untagged
- **QUAERO-D84**: 84 | IC | Bare document reference fragment
- **QUAERO-D86**: 86 | OO | Age-based contraindication; qualifier tokens untagged
- **QUAERO-D95**: 95 | IC, OO | ATC code referenced in text but value absent/unlabeled
- **FRENCHMEDMCQA-D1**: 1 | 1 correct | IO/OO | MCQA clinical recall — no NER/STS relevance
- **FRENCHMEDMCQA-D2**: 2 | 2 correct | OO | Output = index selection, not entity spans or scores
- **FRENCHMEDMCQA-D13**: 13 | 3 correct | IC | Drug INNs appear only as answer choices
- **FRENCHMEDMCQA-D50**: 50 | 2 correct | IC | Pharmaceutical manufacturing content, exam format
- **FRENCHMEDMCQA-D70**: 70 | 2 correct | IC | INN+brand in answer options, not regulatory prose
- **FRENCHMEDMCQA-D72**: 72 | 4 correct | IC | Drug-specific pharmacology, exam knowledge recall
- **FRENCHMEDMCQA-D74**: 74 | 2 correct | IC | INN+brand names as classified choices
- **FRENCHMEDMCQA-D94**: 94 | 2 correct | IC | Vaccination policy — potential temporal validity concern
- **FRENCHMEDMCQA-D105**: 105 | 1 correct | IC | SmPC referenced in answer option, not source text
- **DEFT2020-D1**: Example 1 (moy=0.5): Electric railway caténaire content — non-biomedical domain
- **DEFT2020-D3**: Example 3 (moy=2.1): Boris Godunov historical content — non-biomedical domain
- **DEFT2020-D4**: Example 4 (moy=4.0): Breastfeeding contraindication — drug label register, obligation modality difference
- **DEFT2020-D5**: Example 5 (moy=4.2): Caudry municipality — geographic/encyclopedic content
- **DEFT2020-D6**: Example 6 (moy=0.4): Beekeeping/queen selection — non-biomedical content
- **DEFT2020-D16**: Example 16 (moy=4.0): Opioid withdrawal warning — safety timing and substance class specificity difference scored as high similarity
- **DEFT2020-D18**: Example 18 (moy=4.6): Lactose excipient contraindication — SmPC section 4.3-style language
- **DEFT2020-D26**: Example 26 (moy=3.4): Cochrane comparative effectiveness statement — research prose register
- **DEFT2020-D27**: Example 27 (moy=4.4): Methodological quality assessment — research prose register
- **DEFT2020-D46**: Example 46 (moy=2.2, vote=5.0): High annotator disagreement (scores span 0–5)
- **DEFT2020-D52**: Example 52 (moy=4.4): Pharmaceutical tablet description — dosage form SmPC language
- **DEFT2020-D54**: Example 54 (moy=5.0): Von Willebrand hemostasis — identical source/target pair, adverse-event language
- **DEFT2020-D102**: Example 102 (moy=3.2, vote=1.0): Bimodal annotator disagreement on dental prosthetics pair
- **DEFT2020-D130**: Example 130 (moy=3.8): Sedative drug warning — scope extension (alcohol addition) scored as near-equivalent
- **MORFITT-D1**: Ex. 1 | 9 | Cardiology abstract; academic register confirmed
- **MORFITT-D2**: Ex. 19 | 7 | Pharmaceutical stability study; closest to regulatory content
- **MORFITT-D3**: Ex. 33 | 10,7 | Cosmetic/galenic formulation; academic not regulatory
- **MORFITT-D4**: Ex. 2 | 10 | Preclinical analgesic study; academic register
- **MORFITT-D5**: Ex. 21 | 1,3,4 | COVID immunology; no regulatory framing
- **MORFITT-D6**: Ex. 29 | 8 | Cyclosporine in veterinary; no INN/ATC conventions
- **MORFITT-D7**: Ex. 19 | 7 | Sulfadiazine dosage in research context
- **MORFITT-D8**: Ex. 10 | 3 | French translation from English; non-EMA register
- **MORFITT-D9**: Ex. 28 | 3,8 | Translated abstract; veterinary/Canadian context
- **MORFITT-D10**: Ex. 31 | 11 | Saudi Arabia medical intern survey
- **MORFITT-D11**: Ex. 20 | 1 | Jordanian cancer fatigue study
- **MORFITT-D12**: Ex. 4 | 8,4 | Foot-and-mouth disease in livestock
- **MORFITT-D13**: Ex. 9 | 6,0,8 | Canine otitis microbiome
- **MORFITT-D14**: Ex. 26 | 6,8,5 | Equine Sarcocystis parasitology
- **MORFITT-D15**: Ex. 12 | 11 | Psychosocial predictors of depression; non-regulatory
- **MORFITT-D16**: Ex. 22 | 11 | Arabic food addiction scale validation
- **MORFITT-D17**: Ex. 3 | 1 | "Etiology" label; no mapping to regulatory entity taxonomy
- **MORFITT-D18**: Ex. 6 | 6,8,2 | Multi-label PRRSV study; unrelated to regulatory norms
- **CLISTER-D1**: 9 | 0.0 | Clinical treatment narrative, not regulatory posology
- **CLISTER-D2**: 78 | 4.0 | Drug mention in anesthesia context, not SmPC format
- **CLISTER-D3**: 41 | 2.0 | Prescription-style text in clinical case context
- **CLISTER-D4**: 98 | 2.0 | Clinical dosage notation, informal register
- **CLISTER-D5**: 164 | 2.0 | Tabular pharmacokinetic data from clinical case
- **CLISTER-D6**: 146 | 0.0 | Brand name used, not INN-only regulatory convention
- **CLISTER-D7**: 75 | 1.25 | INN in oncology narrative, not regulatory format
- **CLISTER-D8**: 88 | 0.0 | Toxicology context, not contraindication section language
- **CLISTER-D9**: 3 | 3.0 | Adverse reaction scoring under general proximity vs. regulatory equivalence
- **CLISTER-D10**: 188 | 4.0 | 2× quantitative biomarker difference scored 4.0 (high similarity)
- **CLISTER-D11**: 149 | 0.5 | Route of administration difference (oral vs. IV) flagged via general scoring
- **CLISTER-D12**: 36 | 3.0 | Positive vs. negative test result scored 3.0
- **CLISTER-D13**: 10 | 5.0 | Minor grammatical variation correctly scored 5.0
- **CLISTER-D14**: 37 | 5.0 | Synonymous lexical expressions scored 5.0
- **CLISTER-D15**: 8 | 1.0 | Tabular pharmacokinetic rows; fragmented text
- **CLISTER-D16**: 191 | 2.0 | English prescription abbreviations in French corpus
- **MANTRAGSC-D1**: Ex. 1 | DISO | MEDLINE case report title; academic register
- **MANTRAGSC-D2**: Ex. 36 | CHEM (Cefotaxime) | Drug in clinical context, not regulatory format
- **MANTRAGSC-D3**: Ex. 45 | CHEM (testostérone) | Research-register hormone entity
- **MANTRAGSC-D4**: Ex. 41 | GEOG/epidemic | Sub-Saharan epidemiology; non-EU regulatory context
- **MANTRAGSC-D5**: Ex. 36 | CHEM | No INN-specific label granularity
- **MANTRAGSC-D6**: Ex. 53 | CHEM | Gases and drugs share same label as pharmaceutical INNs
- **MANTRAGSC-D7**: Ex. 18 | DEVI | No dosage/route/mode entity layer
- **MANTRAGSC-D8**: Ex. 17 | PROC | Treatment terms without posology sub-entities
- **MANTRAGSC-D9**: Ex. 57 | all-O | Administrative noise in tiny dataset
- **MANTRAGSC-D10**: Ex. 47 | all-O | Anthropological content; no entities
- **MANTRAGSC-D11**: Ex. 43 | DISO | Dakar clinical case; non-EU register
- **MANTRAGSC-D12**: Ex. 41 | GEOG | Central African epidemiology
- **MANTRAGSC-D13**: Ex. 22 | LIVB | Veterinary/avian content
- **E3C-D1**: Ex. 1 | all-O | "cholestase (bilirubine totale à 140 mmol/L...)" | IC, IF
- **E3C-D2**: Ex. 59 | all-O | "thrombolyse intraveineuse par ténectéplase 50 mg" | IO, IC
- **E3C-D3**: Ex. 62 | all-O | "amoxicilline-acide clavulanique à 3g/j, moxifloxacine à 400 mg/j" | IO, IC, OO
- **E3C-D4**: Ex. 79 | all-O | "Isoniazide 5mg/kg, Rifampicine 10 mg/kg, Ethambutol 25 mg/kg" | OO, OC
- **E3C-D5**: Ex. 39 | mixed | "ciclosporine, d'evérolimus et de corticoïdes, une insuffisance rénale" | OO
- **E3C-D6**: Ex. 3 | 0,0,0,0,1,2,0,0,0 | "tumeur solide du péritoine" | OO
- **E3C-D7**: Ex. 53 | ...1,2,2,0 | "état de choc septique" | OO
- **E3C-D8**: Ex. 103 | all-O | "fentanyl (3µg/kg) et de l'étomidate (0,2mg/kg)" | OO, OC
- **E3C-D9**: Ex. 90 | all-O | "rapportée en Afrique noire" | IC
- **E3C-D10**: Ex. 70 | ...1,...,0 | "originaire du Maroc" | IC
- **E3C-D11**: Ex. 112 | all-O | "Le traitement de cotrimoxazole était arrêté" | OC
- **E3C-D12**: Ex. 44 | all-O | "contraception orale au oestro-progestatifs" | OC
- **E3C-D13**: Ex. 5 | ...1,2,... | tokens=['\\','n','La',...] | IF
- **PXCORPUS-D1**: 41 | medical_prescription | IC, IO
- **PXCORPUS-D2**: 47 | medical_prescription | IC, IO
- **PXCORPUS-D3**: 166 | medical_prescription | IC
- **PXCORPUS-D4**: 3 | none | IF, IC
- **PXCORPUS-D5**: 10 | negate | IF, IC
- **PXCORPUS-D6**: 88 | none | IF, IC
- **PXCORPUS-D7**: 75 | medical_prescription | IF
- **PXCORPUS-D8**: 207 | medical_prescription | IF, IC
- **PXCORPUS-D9**: 169 | medical_prescription | IF
- **PXCORPUS-D10**: 4 | replace | IO, OO
- **PXCORPUS-D11**: 8 | replace | IO, OO
- **PXCORPUS-D12**: 9 | medical_prescription | OO
- **PXCORPUS-D13**: 99 | medical_prescription | OO
- **PXCORPUS-D14**: 18 | none | IC, OO
- **PXCORPUS-D15**: 76 | none | IC, OO
- **PXCORPUS-D16**: 64 | none | IC, OO
- **PXCORPUS-D17**: 34 | medical_prescription | IC
- **PXCORPUS-D18**: 59 | medical_prescription | IC
- **PXCORPUS-D19**: 81 | medical_prescription | IC
- **PXCORPUS-D20**: 13 | medical_prescription | IC, IF
- **PXCORPUS-D21**: 119 | medical_prescription | IC, IF
- **PXCORPUS-D22**: 103 | medical_prescription | IC, IF
- **DIAMED-D1**: Example 1 (label=A00-B99): "Le traitement était basé sur les antirétroviraux (Stavudine (D4T), Lamuvidine (3TC), Efavirenz (EFV))..." — Drug names in clinical narrative, not regulatory INN format; Pan African Medical Journal source.
- **DIAMED-D2**: Example 2 (label=C00-D49): Source URL `panafrican-med-journal.com`, published Nov 2015 — confirms non-EU geographic provenance.
- **DIAMED-D3**: Example 3 (label=D50-D89): Keywords include "Maroc" — North African setting.
- **DIAMED-D4**: Example 4 (label=E00-E89): Pan African Medical Journal source — consistent sub-Saharan/African geographic pattern.
- **DIAMED-D5**: Example 5 (label=F01-F99): "Halopéridol 20 mg et Chlorpromazine 400 mg...Phénobarbital" — clinical-narrative drug dosage mentions without regulatory structure.
- **DIAMED-D6**: Example 6 (label=G00-G99): Pan African Medical Journal source — African clinical setting confirmed.
- **DIAMED-D7**: Example 7 (label=H00-H59): Pan African Medical Journal source — no regulatory content.
- **DIAMED-D8**: Example 8 (label=H60-H95): "amphotéricine B par voie intraveineuse...itraconazole par voie orale" — drug names in narrative, no ATC codes or SmPC-style posology.
- **DIAMED-D9**: Example 9 (label=I00-I99): "service de cardiologie du CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" — explicitly West African clinical setting.
- **DIAMED-D10**: Example 10 (label=J00-J99): Pan African Medical Journal source — African clinical setting.
- **DIAMED-D11**: Example 11 (label=K00-K95): "polyglactin 910 (vicryl*2/0)" — trade name mention in surgical narrative, not regulatory INN context.
- **DIAMED-D12**: Example 12 (label=L00-L99): Keywords include "Niamey"; drugs listed as "Phénobarbital 200mg", "Halopéridol 20mg" in narrative — African setting, clinical dosage mentions not in regulatory format.
- **DIAMED-D13**: Example 13 (label=M00-M99): Pan African Medical Journal source — African clinical setting, no drug regulatory content.
- **DIAMED-D14**: Example 14 (label=N00-N99): Pan African Medical Journal source — African clinical setting, no regulatory content.
- **DEFT2021-D3**: Ex. 3 | Clinical narrative drug administration — no regulatory genre
- **DEFT2021-D15**: Ex. 15 | Broad span annotation for macroscopic findings
- **DEFT2021-D26**: Ex. 26 | Single punctuation token artifact
- **DEFT2021-D31**: Ex. 31 | Single initial token artifact
- **DEFT2021-D42**: Ex. 42 | Single initial token artifact
- **DEFT2021-D55**: Ex. 55 | Drug/dose/route annotated as clinical entities, not regulatory INN
- **DEFT2021-D80**: Ex. 80 | Informal clinical drug naming (no ATC/INN)
- **DEFT2021-D81**: Ex. 81 | Detailed chemotherapy in clinical narrative prose
- **DEFT2021-D99**: Ex. 99 | Drug name casually used, no regulatory formatting
- **DEFT2021-D108**: Ex. 108 | Non-EU geographic context in patient history
- **DEFT2021-D158**: Ex. 158 | Excipient/drug mixture annotated as generic substance
- **DEFT2021-D166**: Ex. 166 | Non-EU geographic reference (Madagascar)
- **CAS-D1**: Example 1: "l'examen clinique montre un état général conservé" — Clinical examination report; formal French clinical register
- **CAS-D5**: Example 5: "un homme de 48 ans...rectorragies dues à des polypes du rectum traités par électrocoagulation" — Clinical case presentation format
- **CAS-D13**: Example 13: "depuis hier soir, je suis essouflé...j'ai des frissons" — Patient direct speech; informal register
- **CAS-D15**: Example 15: "Il s'agit d'une patiente âgée de 54 ans...transmissions virales hépatiques" — Clinical case narrative; possible non-metropolitan context
- **CAS-D22**: Example 22: "administration d'une ampoule de digoxine en intraveineuse" — Drug mention in clinical narrative, informal posology
- **CAS-D29**: Example 29: "887,5 mg (12,5 mg/kg/h) administrée sur quatre heures" — Clinical dosage expression, not regulatory format
- **CAS-D33**: Example 33: "cyclophosphamide, vincristine et prednisone...rituximab" — Chemotherapy drugs listed in clinical protocol narrative
- **CAS-D34**: Example 34: "le Betnésol® lavement était progressivement arrêté" — Trade name with dosage form in clinical narrative
- **CAS-D47**: Example 47: "vous êtes appelés au secours d'une infirmière de nuit..." — Educational vignette register
- **CAS-D49**: Example 49: "la malade a été traitée à la norfloxacine" — Drug in casual clinical syntax
- **CAS-D54**: Example 54: "la valeur limite d'exposition autorisée était de 450 ppm soit 2 500 mg/m3" — Occupational exposure context
- **CAS-D63**: Example 63: "Pentasa®...Proctocort® (hydrocortisone acétate 90 mg: 1 lavement tous les soirs)" — Closest to posology expression; embedded in narrative
- **CAS-D80**: Example 80: "Cholstat® 0.1" — Branded drug fragment
- **CAS-D103**: Example 103: Dense lab table (AST, ALT, bilirubine, RNI, créatinine) — Structured numerical data; POS-tagged only
- **ESSAI-D1**: Ex. 3 | pos | "Un tirage au sort…répartira les patientes dans les deux bras de l'étude" | IC, IO
- **ESSAI-D2**: Ex. 6 | pos | "administré toutes les deux semaines sous forme de perfusion d'une heure" | IC
- **ESSAI-D3**: Ex. 37 | pos | "un anticorps anti-CTLA-4 (ipilimumab) et un anticorps anti-PD-1 (nivolumab)" | IC, IO
- **ESSAI-D4**: Ex. 71 | pos | "Ce traitement bénéficie d'une autorisation de mise sur le marché" | IC
- **ESSAI-D5**: Ex. 1 | pos | "la combinaison gemcitabine + abraxane, chez des patients avec un cancer du pancréas" | IC, OO
- **ESSAI-D6**: Ex. 36 | pos | "pemetrexed et cisplatine ou carboplatine, jusqu'à 6 cycles" | IC
- **ESSAI-D7**: Ex. 2 | pos | "Le MEDI9197 est injecté en intra-tumoral tous les 28j" | IC
- **ESSAI-D8**: Ex. 42 | pos | "Le BMS-986179 sera administré par voie veineuse toutes les semaines" | IC
- **ESSAI-D9**: Ex. 16 | pos | "évaluer la tolérance et l'efficacité du CMAK683X2101 (inhibiteur d'EED)" | IC
- **ESSAI-D10**: Ex. 25 | pos | "après 8 jours…toutes les 2 semaines pendant 6 semaines" | IC
- **ESSAI-D11**: Ex. 47 | pos | "donné par voie orale 2 fois par jour, pour une durée de 48 semaines" | IC
- **ESSAI-D12**: HF schema | cls labels | `["negation_speculation","negation","neutral","speculation"]` | OO
- **ESSAI-D13**: Ex. 26 | pos | "Vous serez vus en consultation régulièrement pour évaluer la tolérance" | IC, IF
- **ESSAI-D14**: Ex. 20 | pos | "Le choix de ton traitement est guidé par les anomalies des gènes de ta maladie" | IC, IF
