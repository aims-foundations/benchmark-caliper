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
