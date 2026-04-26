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
