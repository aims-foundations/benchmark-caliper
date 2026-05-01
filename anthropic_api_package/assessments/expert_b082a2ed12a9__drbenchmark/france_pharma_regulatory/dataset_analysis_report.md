## Dataset Analysis Report

**Benchmark:** DrBenchmark — A Large Language Understanding Benchmark for the Biomedical French Domain
**Datasets analyzed:** 11 datasets (QUAERO, FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC, E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI)
**Analysis date:** 2025-07-14

---

### Per-Dataset Fit Assessment

#### DrBenchmark/QUAERO

- **Task:** Named Entity Recognition (token-level, IOB2), two configs: `emea` (drug leaflets) and `medline` (biomedical titles)
- **Deployment fit:** **Partial** — The `emea` config is the single strongest genre match in the entire benchmark, containing actual EMEA drug leaflet text (patient information leaflet register) with pharmaceutical composition lists, posology expressions, contraindication blocks, and EMA administrative references. However, the `medline` config (~65% of total examples) contains research-register biomedical titles with off-topic content, and the UMLS-based entity schema collapses all chemical entities into a single CHEM class without INN/excipient/ATC distinction.
- **Key strengths:**
  - `emea` config directly contains EU regulatory drug leaflet text in French (QUAERO-D1, QUAERO-D2, QUAERO-D6, QUAERO-D9)
  - Posology expressions and administration routes annotated (QUAERO-D3, QUAERO-D4)
  - Contraindication blocks with population qualifiers present (QUAERO-D5, QUAERO-D6)
  - Brand name and INN co-occurrence annotated as CHEM (QUAERO-D7, QUAERO-D8)
- **Key concerns:**
  - CHEM tag conflates INNs, excipients, and other chemicals with no sub-class distinction (QUAERO-D10, QUAERO-D11) — MAJOR
  - ATC codes, marketing authorization numbers, and regulatory identifiers receive O tag (QUAERO-D12) — MAJOR
  - `medline` config (majority of examples) contains non-regulatory, non-pharmaceutical content including historical and psychosocial topics (QUAERO-D13, QUAERO-D14, QUAERO-D15) — MAJOR
  - Annotation norms are UMLS Semantic Groups, not EMA/ANSM regulatory entity standards; contraindication conditions are tagged by entity type but not as regulatory constructs (QUAERO-D16, QUAERO-D17) — MAJOR
  - Document splitting artifacts produce corrupted sentence fragments (QUAERO-D19, QUAERO-D20) — MINOR

---

#### DrBenchmark/FrenchMedMCQA

- **Task:** Multiple-Choice Question Answering (MCQA), French pharmacy diploma exam questions, 5 options, single or multiple correct answers
- **Deployment fit:** **Weak** — The task type (closed-set answer selection from exam questions) does not match either NER or STS as required by the deployment. Despite containing relevant pharmaceutical vocabulary, no example presents regulatory prose for entity extraction or pairwise sentence comparison.
- **Key strengths:**
  - Dense pharmaceutical terminology: INNs, drug classes, contraindications, and adverse effects appear as answer options (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D2, FRENCHMEDMCQA-D3)
  - Explicit SmPC reference (RCP) appears at least once (FRENCHMEDMCQA-D7)
  - Pharmaceutical formulation and analytical chemistry content partially overlaps with regulatory CTD Module 3 knowledge domains (FRENCHMEDMCQA-D4, FRENCHMEDMCQA-D5, FRENCHMEDMCQA-D8, FRENCHMEDMCQA-D9)
- **Key concerns:**
  - CRITICAL task type mismatch: MCQA evaluates declarative knowledge retrieval, not NER span extraction or STS pairwise scoring (FRENCHMEDMCQA-D11, FRENCHMEDMCQA-D14)
  - CRITICAL genre mismatch: exam interrogative format vs. declarative regulatory prose (FRENCHMEDMCQA-D12, FRENCHMEDMCQA-D15)
  - Drug names appear as answer options, not as extractable entities in continuous text; ATC codes absent (FRENCHMEDMCQA-D13)
  - Significant fraction of questions covers topics irrelevant to pharmaceutical regulatory work (parasitology, blood group genetics) (FRENCHMEDMCQA-D16, FRENCHMEDMCQA-D17)
  - Ground truth derived from pharmacy exam answer keys, not EMA/ANSM regulatory standards (MINOR OC concern)

---

#### DrBenchmark/DEFT2020

- **Task:** Semantic Textual Similarity (Task 1: 0–5 scored pairs; Task 2: most-similar-sentence MCQA)
- **Deployment fit:** **Partial** — Task 1 directly tests STS in French with genuine drug leaflet content in a meaningful fraction of pairs. However, the scoring calibration reflects general semantic proximity rather than regulatory equivalence, and a large fraction of pairs derives from encyclopedic and non-pharmaceutical content.
- **Key strengths:**
  - Genuine French drug leaflet text in Task 1, including contraindication phrasing, safety warnings, and dose-time threshold language (DEFT2020-D1, DEFT2020-D2, DEFT2020-D3, DEFT2020-D4)
  - Multi-annotator scoring with individual scores available, enabling inter-annotator variance analysis (DEFT2020-D7, DEFT2020-D8)
  - Task 2 tests near-synonym discrimination in drug safety text, structurally analogous to consistency checking (DEFT2020-D12)
  - Regulatory-register French vocabulary appears in drug leaflet pairs (DEFT2020-D9, DEFT2020-D10, DEFT2020-D11)
- **Key concerns:**
  - CRITICAL: Large proportion of pairs from encyclopedic content (beekeeping, sports, history) entirely irrelevant to regulatory deployment (DEFT2020-D13, DEFT2020-D14, DEFT2020-D15)
  - MAJOR: STS scores reflect general semantic proximity; legally critical qualifiers (specific opioid names, "sous stricte surveillance médicale," "potentialisation réciproque") are not penalized at the score level (DEFT2020-D16, DEFT2020-D17, DEFT2020-D18, DEFT2020-D20)
  - MAJOR: No evidence of EMA/ANSM-aligned annotation guidelines; annotators are NLP community members, not regulatory specialists (DEFT2020-D19)
  - MAJOR: Heterogeneous genres (clinical cases, encyclopedia, Cochrane abstracts, drug leaflets) conflated without stratification (DEFT2020-D21, DEFT2020-D22)
  - MINOR: Task 2 distractors include trivially non-medical options, reducing discriminative validity (DEFT2020-D23, DEFT2020-D24)

---

#### DrBenchmark/MORFITT

- **Task:** Multi-label classification of biomedical abstracts into 12 medical specialties
- **Deployment fit:** **Weak** — Abstract-level specialty classification is a different task type from NER and STS, the genre is exclusively PMC research abstracts (not regulatory documents), and a substantial proportion covers veterinary medicine and non-EU geographic contexts.
- **Key strengths:**
  - Pharmacology specialty label present with some drug-adjacent content (MORFITT-D3, MORFITT-D4, MORFITT-D5)
  - Multi-label annotation structure is technically consistent (MORFITT-D6)
- **Key concerns:**
  - CRITICAL task type mismatch: multi-label classification at abstract level vs. NER and STS (MORFITT-D7, MORFITT-D8)
  - CRITICAL genre mismatch: PMC research abstracts only; no regulatory document genre (MORFITT-D9, MORFITT-D10)
  - MAJOR: No regulatory entity annotation whatsoever; drug names appear in text but are unannotated (MORFITT-D11, MORFITT-D12)
  - MAJOR: Substantial non-EU geographic scope (Canada, Japan, Saudi Arabia) diverges from EMA/ANSM deployment (MORFITT-D13, MORFITT-D14, MORFITT-D15, MORFITT-D16)
  - MAJOR: Veterinary content with no human drug regulatory relevance (MORFITT-D17, MORFITT-D18, MORFITT-D19)

---

#### DrBenchmark/CLISTER

- **Task:** Semantic Textual Similarity (STS), 1,000 clinical sentence pairs, 0–5 scale averaged across annotators
- **Deployment fit:** **Partial (with significant OO concern)** — CLISTER directly tests STS in French biomedical language and provides genuine continuous similarity scores with multi-annotator averaging. However, source genre is exclusively clinical case reports (not regulatory documents), and the scoring scheme demonstrates insensitivity to numerically significant differences that would be regulatory-critical mismatches.
- **Key strengths:**
  - French STS with genuine multi-annotator averaged labels (CLISTER-D6, CLISTER-D7)
  - Full 0–5 label range with non-integer values demonstrating continuous distribution (CLISTER-D8, CLISTER-D9)
  - Some pharmaceutical expressions present (drug names, dosage pairs) (CLISTER-D2, CLISTER-D3, CLISTER-D4, CLISTER-D5)
- **Key concerns:**
  - CRITICAL: Source domain exclusively clinical case reports; no SmPC, leaflet, CTD, or EU regulatory document text (CLISTER-D10, CLISTER-D11)
  - CRITICAL: Scoring calibrated for general semantic proximity; quantitative differences of 2×, 14×, and 60× in clinical measurements score 4.0, 3.75, and 3.0 respectively — fundamentally incompatible with regulatory equivalence requirements (CLISTER-D12, CLISTER-D13, CLISTER-D14)
  - MAJOR: Different INNs scored as partially similar (2.0) due to structural template match; regulatory judgment would score 0 (CLISTER-D17, CLISTER-D18)
  - MAJOR: Annotator population not documented; scoring pattern inconsistent with regulatory-standard equivalence norms (CLISTER-D17, CLISTER-D18)
  - MINOR: Tabular data fragments appear as sentence pairs (CLISTER-D19, CLISTER-D20); ceiling dominated by tense-only variations (CLISTER-D21, CLISTER-D22)

---

#### DrBenchmark/MANTRAGSC

- **Task:** Named Entity Recognition (NER, IOB2), multilingual, with French `fr_emea`, `fr_medline`, and `fr_patents` configs
- **Deployment fit:** **Partial** — The `fr_emea` and `fr_patents` configs provide the most direct genre overlap of any NER dataset in the benchmark (actual EMEA drug label text and French patent claims). However, the extremely small size of each French config (test set n=20), the CHEM-conflation problem, and the absence of INN/ATC/excipient-specific schema classes are significant limitations.
- **Key strengths:**
  - `fr_emea` contains genuine EMEA drug label text with posology, contraindications, and INN mentions (MANTRAGSC-D1, MANTRAGSC-D2, MANTRAGSC-D3, MANTRAGSC-D4)
  - INN and salt form co-occurrence present in EMEA examples (MANTRAGSC-D5, MANTRAGSC-D6)
  - `fr_patents` provides French pharmaceutical patent claim language (MANTRAGSC-D7, MANTRAGSC-D8)
  - Adverse event language and SmPC section headers present (MANTRAGSC-D9, MANTRAGSC-D10)
- **Key concerns:**
  - MAJOR: Extremely small French subset (test n=20 per config); no statistically robust NER evaluation possible (MANTRAGSC-D11, MANTRAGSC-D12)
  - MAJOR: CHEM tag conflates INNs, brand names, excipient salt forms — no regulatory entity subclass distinction (MANTRAGSC-D13, MANTRAGSC-D14)
  - MAJOR: `fr_medline` config is non-regulatory research abstract titles (MANTRAGSC-D15, MANTRAGSC-D16)
  - MAJOR: Contraindication and dose-threshold qualifiers not annotated at regulatory granularity; patient population qualifiers tagged LIVB/DISO rather than as contraindication type (MANTRAGSC-D4, MANTRAGSC-D2)
  - MINOR: Patent examples contain highly technical chemical structure notation with sparse annotation (MANTRAGSC-D17)

---

#### DrBenchmark/E3C

- **Task:** Named Entity Recognition (NER), multilingual clinical cases, two annotation layers: clinical (CLINENTITY) and temporal (EVENT/ACTOR/BODYPART/TIMEX3/RML)
- **Deployment fit:** **Weak** — Both annotation schemas capture clinical case entities (pathologies, temporal events, actors) with no pharmaceutical regulatory entity types. Drug names appear in text but are demonstrably unannotated. The genre is exclusively clinical case narrative.
- **Key strengths:**
  - French clinical biomedical language in formal register (E3C-D1, E3C-D3)
  - IOB2 NER format compatible with deployment output format
- **Key concerns:**
  - CRITICAL: Entire dataset is clinical case reports; no regulatory document genre (E3C-D4, E3C-D5)
  - CRITICAL: Neither annotation schema includes any pharmaceutical or regulatory entity type; drug names such as ciclosporine receive O tag (E3C-D2, E3C-D6, E3C-D7)
  - MAJOR: Non-French configs (Basque, English, Spanish, Italian) present in repository and could contaminate evaluation if not filtered (E3C-D8, E3C-D9)
  - MAJOR: Clinical case narrative register fundamentally distinct from regulatory document structure (E3C-D10, E3C-D11)
  - MINOR: High prevalence of all-O examples contributes to annotation sparsity (E3C-D12, E3C-D13)

---

#### DrBenchmark/PxCorpus

- **Task:** Intent classification (4 classes) + NER (38 classes) over transcribed spoken drug prescription utterances
- **Deployment fit:** **Partial (with CRITICAL register caveat)** — PxCorpus has the richest pharmaceutical entity schema in the benchmark (38 NER classes including DRUG, SUBSTANCE, DOSAGE, FREQUENCY, MODE, DURATION) and the `replace` intent class directly captures prescription correction analogous to compliance flagging. However, the entire corpus is transcribed speech with pervasive spoken-language artifacts, making register transfer to formal regulatory documents highly uncertain.
- **Key strengths:**
  - Richest pharmaceutical NER schema in DrBenchmark: 38 classes covering DRUG, SUBSTANCE, DOSAGE, FREQUENCY, MODE, DURATION (PXCORPUS-D1, PXCORPUS-D2, PXCORPUS-D3)
  - INN and brand name co-occurrence with salt form distinctions (PXCORPUS-D8)
  - `replace` intent class captures dosage correction acts directly relevant to compliance flagging (PXCORPUS-D6, PXCORPUS-D7)
  - Dosage unit variety across mg, µg, ml, UI (PXCORPUS-D4)
- **Key concerns:**
  - CRITICAL: Spoken transcription register with ASR artifacts, truncations, code-switching, and informal language entirely absent from regulatory documents (PXCORPUS-D10, PXCORPUS-D11, PXCORPUS-D12, PXCORPUS-D13)
  - CRITICAL: No regulatory document genre present; no SmPC, leaflet, or CTD text (PXCORPUS-D14)
  - MAJOR: NER schema does not capture ATC codes, excipient names, or EMA-templated contraindication qualifiers (PXCORPUS-D15, PXCORPUS-D16)
  - MAJOR: Extreme class imbalance — `replace` class has ~3 examples in 500-item buffer, the most deployment-relevant intent (PXCORPUS-D17, PXCORPUS-D18)
  - MAJOR: No STS task present

---

#### DrBenchmark/DiaMED

- **Task:** Multi-class classification into 22 ICD-10 chapter-level labels, 739 French clinical cases from *The Pan African Medical Journal*
- **Deployment fit:** **Weak** — ICD-10 classification is not NER or STS. The source genre is clinical case narrative, the geographic origin is predominantly Sub-Saharan and North African rather than EU, and no regulatory entity annotation exists. The only distinction from similar datasets is its documented inter-annotator agreement methodology.
- **Key strengths:**
  - Only DrBenchmark dataset with documented inter-annotator agreement (Cohen's Kappa, Gwet's AC1) and one medical expert annotator
  - French clinical prose confirmed across all examples (DIAMED-D1, DIAMED-D8)
  - Drug names and dosages incidentally present in some cases (DIAMED-D1, DIAMED-D2, DIAMED-D12)
- **Key concerns:**
  - CRITICAL: ICD-10 classification task provides no NER or STS signal for the deployment (DIAMED-D6, DIAMED-D9, DIAMED-D13)
  - CRITICAL: Clinical case narrative genre entirely distinct from EU regulatory document prose (DIAMED-D6, DIAMED-D9)
  - CRITICAL: No regulatory entity annotation; drug mentions are incidental and unannotated (DIAMED-D12)
  - MAJOR: Sub-Saharan/North African geographic and clinical context diverges from EMA/ANSM regulatory French (DIAMED-D9, DIAMED-D3, DIAMED-D11)
  - MAJOR: Severely skewed label distribution with near-zero representation for several ICD-10 chapters
  - MINOR: ICD-10 taxonomy only tangentially related to any deployment capability

---

#### DrBenchmark/DEFT2021

- **Task:** Multi-label classification (23 MeSH-C axes) and NER (13 entity types including SUBSTANCE, DOSAGE, MODE, DURATION) over 275 French clinical cases
- **Deployment fit:** **Partial** — The NER config's SUBSTANCE, DOSAGE, and MODE entity types are the closest multi-type clinical NER annotation to the deployment's pharmaceutical entity extraction needs. However, the genre is exclusively clinical case reports, INN/ATC/excipient distinctions are not made, and no regulatory-equivalence STS capability is present.
- **Key strengths:**
  - NER schema includes SUBSTANCE, DOSAGE, MODE, DURATION — partial mapping to deployment's pharmaceutical entity targets (DEFT2021-D3, DEFT2021-D4, DEFT2021-D5)
  - Dense posology expressions with drug names, routes, frequencies in French clinical text (DEFT2021-D1, DEFT2021-D2)
  - Pharmacology and toxicology MeSH specialties present in classification labels (DEFT2021-D6, DEFT2021-D7)
- **Key concerns:**
  - CRITICAL: Genre exclusively clinical case reports; no regulatory document structure (DEFT2021-D8, DEFT2021-D9, DEFT2021-D10)
  - CRITICAL: NER schema dominated by DISO, PROC, ANAT; SUBSTANCE does not distinguish INN from excipient or provide ATC linkage (DEFT2021-D11, DEFT2021-D12, DEFT2021-D13)
  - MAJOR: Annotation norms clinical/biomedical NLP; no EMA/ANSM regulatory standards referenced (DEFT2021-D14, DEFT2021-D15)
  - MAJOR: No STS task present (DEFT2021-D16)
  - MINOR: Small dataset (275 cases) limits generalizability

---

#### DrBenchmark/CAS

- **Task:** Negation/speculation classification and NER (negation/speculation scope), plus POS tagging, over 3,790 French clinical cases
- **Deployment fit:** **Weak** — Negation and speculation scope annotation is linguistically relevant to interpreting safety warnings but does not annotate pharmaceutical entities or regulatory equivalence. Genre is entirely clinical case narrative.
- **Key strengths:**
  - Negation and speculation annotation has indirect relevance to safety-warning interpretation (CAS-D5, CAS-D6)
  - Drug names incidentally present in text (CAS-D2, CAS-D3)
  - Large corpus; French biomedical language confirmed throughout
- **Key concerns:**
  - CRITICAL: Genre exclusively clinical case reports; no regulatory document present (CAS-D8, CAS-D9)
  - CRITICAL: NER schema annotates only negation/speculation scope, not pharmaceutical entities; drug names receive O tag (CAS-D10, CAS-D11)
  - MAJOR: POS annotation is machine-generated (Tagex 3); negation/speculation annotators undocumented; no regulatory expert involvement (CAS-D12)
  - MAJOR: Negation/speculation labels do not distinguish legally critical qualifiers from general clinical hedges
  - MINOR: Severe label imbalance (~70% neutral); negation_speculation rare (CAS-D13)

---

#### DrBenchmark/ESSAI

- **Task:** Negation/speculation classification and NER (negation/speculation scope), plus POS tagging, over 7,247 French clinical trial protocols
- **Deployment fit:** **Weak** — Clinical trial protocol register is closer to regulatory language than clinical case reports, and the drug vocabulary is rich. However, the NER schema annotates linguistic hedging scope rather than pharmaceutical entities, and the genre remains trial protocols rather than EU regulatory submissions.
- **Key strengths:**
  - Rich pharmaceutical vocabulary: INNs and brand names from oncology trials (ESSAI-D1, ESSAI-D2, ESSAI-D14, ESSAI-D15)
  - Dosage and frequency expressions present (ESSAI-D3, ESSAI-D4)
  - Negation/speculation annotation has indirect relevance to safety-warning compliance (ESSAI-D5, ESSAI-D6)
  - Exclusion criteria with organ-function contraindication-like framing (ESSAI-D7, ESSAI-D8)
- **Key concerns:**
  - CRITICAL: Genre is clinical trial protocol summaries; not SmPC, leaflet, CTD, or EU regulatory submission prose (ESSAI-D10, ESSAI-D11)
  - CRITICAL: NER schema annotates hedging scope, not pharmaceutical regulatory entities (ESSAI-D12, ESSAI-D13)
  - MAJOR: No ATC codes, excipient nomenclature, or INN-standardized entries (ESSAI-D14, ESSAI-D15)
  - MAJOR: Negation/speculation labels do not capture regulatory-legal significance of population qualifiers or dose thresholds (ESSAI-D16, ESSAI-D17)
  - MAJOR: POS annotation machine-generated; no regulatory expert involvement documented (ESSAI-D18)
  - MINOR: Oncology domain only; other therapeutic areas absent (ESSAI-D19, ESSAI-D20)

---

### Cross-Cutting Strengths

**1. Consistent French biomedical language across all datasets**
Every dataset in the benchmark delivers French-language text in Latin script with standard diacritics. No modality mismatch, script issue, or dialect problem exists for the deployment's French language requirement. The French biomedical register across QUAERO-D1, MANTRAGSC-D1, DEFT2021-D2, ESSAI-D1, and CLISTER-D1 is consistently professional and technically dense.

**2. Pharmaceutical entity vocabulary is present across multiple datasets**
Drug names (INNs and brand names), dosage expressions, and administration routes appear in text across QUAERO-emea (QUAERO-D3, QUAERO-D7), MANTRAGSC-fr_emea (MANTRAGSC-D2, MANTRAGSC-D3), DEFT2020 (DEFT2020-D4), DEFT2021 (DEFT2021-D1, DEFT2021-D4), PxCorpus (PXCORPUS-D1, PXCORPUS-D8), and ESSAI (ESSAI-D2). This vocabulary coverage provides a foundation for pharmaceutical concept recognition even if not annotated with the regulatory entity distinctions required.

**3. EMEA drug label genre coverage in two NER datasets**
Both QUAERO-emea and MANTRAGSC-fr_emea provide genuine EMEA drug label text — the closest genre match to the deployment's SmPC and patient information leaflet targets. Together they confirm that French regulatory-register pharmaceutical prose does appear in the benchmark (QUAERO-D1, QUAERO-D6, MANTRAGSC-D1, MANTRAGSC-D9, MANTRAGSC-D10). This is the benchmark's most distinctive and deployment-relevant content cluster.

**4. STS task presence in two datasets**
CLISTER and DEFT2020 together provide the only STS capability in the benchmark. DEFT2020 additionally includes drug leaflet sentence pairs (DEFT2020-D1, DEFT2020-D2, DEFT2020-D9) — a subset that meaningfully overlaps with the deployment's safety-warning equivalence task, even if the scoring calibration is insufficient for regulatory purposes.

**5. Negation and speculation annotation across CAS and ESSAI**
Two large corpora (CAS: 3,790 cases; ESSAI: 7,247 protocols) provide negation/speculation scope annotation. While insufficient for regulatory entity NER, this annotation is relevant to the deployment's need to interpret safety warnings that may be negated, hedged, or conditionally qualified. CAS-D5, CAS-D6, ESSAI-D5, ESSAI-D7 demonstrate the coverage.

---

### Cross-Cutting Weaknesses

**CRITICAL — Benchmark-wide absence of EU regulatory document genres (SmPC, CTD, EU-RMP)**
No confirmed instance of SmPC text, CTD module narrative, or EU Risk Management Plan prose appears in any dataset. QUAERO-emea and MANTRAGSC-fr_emea contain patient information leaflet (PIL) text, not SmPC text. The web search findings confirm this explicitly: the QUAERO EMEA subset contains approximately 10 segmented PIL-register documents total across train/dev/test, and no SmPC, CTD, or EU-RMP source is documented anywhere in DrBenchmark. This is the highest-severity validity gap for the deployment: QUAERO-D9, MANTRAGSC-D10 show EMA administrative language, but the formulaic section-structured legal prose of SmPC sections 4.1–4.9 is absent. Every other dataset (MORFITT-D9, MORFITT-D10, E3C-D4, DIAMED-D6, CAS-D8, ESSAI-D10, DEFT2021-D8) confirms clinical case or research abstract genre.

**CRITICAL — Benchmark-wide absence of INN/ATC/excipient-specific NER entity classes**
Across all 11 datasets, no NER schema distinguishes INNs from excipient names, provides ATC code annotation, or captures EMA-templated contraindication qualifiers as a dedicated entity type. The benchmark's best approximations — CHEM in QUAERO and MANTRAGSC — conflate INNs, excipients, and all chemical compounds under one label (QUAERO-D10, QUAERO-D11, MANTRAGSC-D13, MANTRAGSC-D14). DEFT2021's SUBSTANCE tag is the next closest but equally undifferentiated (DEFT2021-D13). The web search findings confirm that ATC code and excipient-specific extraction from real SmPCs remains an unresolved challenge even for state-of-the-art LLMs (Kadi et al. 2025), reinforcing that this is not merely a benchmark gap but a field-level gap that the deployment cannot resolve using this benchmark's evaluation signal.

**CRITICAL — STS scoring calibrated for general semantic proximity, incompatible with regulatory equivalence**
Both STS datasets (CLISTER and DEFT2020) use a 0–5 scale reflecting general semantic similarity. CLISTER-D12 demonstrates a 2× quantitative difference scoring 4.0; CLISTER-D13 shows a 60× difference scoring 3.0; DEFT2020-D16 shows specific opioid names added in a drug safety warning scoring 4.0 without penalization. DEFT2020-D20 shows a mechanism qualifier dropped from an alcohol warning scoring 3.8. The deployment explicitly requires sensitivity to precisely these micro-differences (A3). No published STS rubric calibrated for dose-threshold sensitivity or population-qualifier sensitivity in regulatory text was found in the web search findings — confirming this is a genuine field-level gap.

**CRITICAL — Absence of regulatory affairs annotator expertise across all datasets**
No dataset in DrBenchmark documents involvement of EMA/ANSM regulatory affairs specialists in annotation. The only confirmed medical expert (DiaMED) annotated ICD-10 chapter classification, not NER or STS tasks (DIAMED benchmark YAML Q45). Annotation demographics are undocumented for the majority of corpora. Authors are affiliated with French academic NLP and clinical medicine institutions (benchmark YAML Q8), not regulatory affairs or pharmacovigilance units. This creates a systematic risk: borderline regulatory cases (dose threshold qualifiers, contraindication scope, population modifiers) are expected to yield disagreements between benchmark labels and regulatory-standard judgments (A4), and there is no annotation evidence to calibrate this risk magnitude. CLISTER-D17, CLISTER-D18, DEFT2020-D16, DEFT2020-D17, DEFT2020-D20, MANTRAGSC-D4 all illustrate specific cases where clinical annotation norms diverge from the regulatory equivalence interpretation the deployment requires.

**MAJOR — Regulatory-register French (EMA SmPC/PIL/QRD templates) systematically absent from text content**
Even where pharmaceutical entities appear (DEFT2021-D1, PXCORPUS-D1, ESSAI-D2), the text register is clinical narrative, spoken prescription, or clinical trial protocol. The formulaic, legally constrained register of EMA QRD-template prose ("est contre-indiqué chez les patients présentant…", "la posologie recommandée est de X mg, à administrer par voie…") does not appear in any dataset's content at scale. QUAERO-emea and MANTRAGSC-fr_emea are the only partial exceptions. The web search findings confirm: EMA QRD template v10.4 mandates that "standard statements must be used whenever they are applicable" and deviations require case-by-case EMA justification — phrasing conventions the benchmark does not systematically represent.

**MAJOR — Patent claims language underrepresented and poorly evaluated**
MANTRAGSC-fr_patents is the only French patent NER data in the benchmark. Its test set contains only 20 examples (MANTRAGSC-D12), the NER schema is identical to the EMEA schema (no patent-specific regulatory entity classes), CamemBERT-based models fail to generate non-O labels on this corpus (benchmark YAML Q73), and the patent claim syntax (Markush structures, nested qualifying clauses, "comprising" constructs) is only partially represented (MANTRAGSC-D17). The deployment's patent IP workflow component cannot be adequately evaluated using this subset alone.

**MAJOR — Heterogeneous non-pharmaceutical content dilutes domain signal in two STS datasets**
DEFT2020 mixes drug leaflet pairs with beekeeping, sports, and historical encyclopedic content (DEFT2020-D13, DEFT2020-D14, DEFT2020-D15). MORFITT includes veterinary, Canadian, Japanese, and Saudi Arabian content (MORFITT-D17, MORFITT-D18, MORFITT-D13, MORFITT-D15, MORFITT-D16). This heterogeneity means aggregate benchmark scores conflate performance on deployment-relevant content with performance on entirely off-domain content, reducing the diagnostic value of evaluation metrics.

**MINOR — Document-splitting artifacts from long EMEA text**
Sentence-splitting of long EMEA documents introduces corrupted sentence fragments in QUAERO-emea (QUAERO-D19, QUAERO-D20), potentially affecting annotation quality around document boundaries. This structural limitation applies specifically to the most deployment-relevant content in the benchmark.

**MINOR — Spoken register in PxCorpus incompatible with written regulatory text**
PxCorpus ASR artifacts, code-switching, and informal speech patterns (PXCORPUS-D10, PXCORPUS-D11, PXCORPUS-D12) represent a register entirely absent from regulatory documents. Despite having the richest pharmaceutical NER schema, this dataset's spoken-language origin creates a register transfer gap that is not evaluated by the benchmark.

---

### Content Coverage Summary

**What is well-covered:**
- French biomedical language in standard diacritics and Latin script across all datasets — no IF validity risks
- Clinical NER entity types (pathologies, symptoms, anatomical structures, procedures, events) — robust coverage across E3C, DEFT2021, CAS, QUAERO, MANTRAGSC
- Coarse pharmaceutical substance mentions (CHEM/SUBSTANCE) in EMEA drug label text — QUAERO-emea and MANTRAGSC-fr_emea
- Posology structure (drug + dose + frequency + duration + route) in spoken prescription context — PxCorpus
- STS in French biomedical text — CLISTER and DEFT2020 Task 1
- Negation and speculation scope in clinical and trial text — CAS and ESSAI
- Medical specialty classification — MORFITT and DEFT2021-cls
- ICD-10 disease classification — DiaMED
- Pharmacological knowledge domain (MCQA) — FrenchMedMCQA

**What is absent or insufficiently covered for this deployment:**
- SmPC, CTD module, and EU Risk Management Plan text — not present in any dataset
- INN as a distinct entity class separate from excipients and other CHEM entities — absent from all schemas
- ATC code annotation — absent from all schemas
- Excipient names as a distinct regulatory entity class — absent from all schemas
- EMA-templated contraindication qualifier annotation (population, dose threshold, medical condition) — absent from all schemas
- Safety warning equivalence scoring calibrated for regulatory precision — absent from both STS datasets
- Annotation by regulatory affairs specialists using EMA/ANSM standards — absent from all datasets
- Patent claim language with drug-specific regulatory entity annotation — present only at n=20 test set scale in MANTRAGSC-fr_patents
- EU geographic and institutional context (EMA/ANSM procedural vocabulary) — present only incidentally in QUAERO-D9

The coverage pattern reflects a benchmark designed for clinical NLP evaluation (hospital records, case reports, trial protocols) that partially overlaps with the pharmaceutical regulatory deployment through two EMEA-sourced NER datasets and two STS datasets with drug leaflet subsets. The overlap is real but narrow relative to the full breadth of what the deployment requires.

---

### Limitations

1. **Sample-based analysis**: Per-dataset reports are based on inspected samples, not exhaustive review of all ~50,000+ total examples. The frequency of deployment-relevant content in DEFT2020's drug leaflet subset and QUAERO-emea's full annotation coverage may be higher or lower than the samples suggest.

2. **EMEA document identity**: The specific EMEA drug products represented in QUAERO-emea (natalizumab/Tysabri, lepirudine/Refludan, ziconotide/Prialt) are a small and potentially non-representative sample of the full EMEA drug leaflet universe. Entity vocabulary breadth may be limited (QUAERO-D18).

3. **Inter-annotator agreement unverified for most datasets**: Only DiaMED has documented IAA. For NER and STS datasets where annotation quality directly determines ground-truth validity, agreement estimates are unavailable for CLISTER, QUAERO, MANTRAGSC, DEFT2021-ner, and others.

4. **Regulatory equivalence calibration — field-level gap**: The web search findings confirm that no French or English NLP benchmark with STS annotation calibrated for regulatory equivalence (dose-threshold sensitivity, population-qualifier sensitivity) currently exists. This gap cannot be resolved by adjusting DrBenchmark; it would require creating new resources.

5. **Non-French multilingual configs**: E3C and MANTRAGSC expose non-French configs (Basque, English, Spanish, Italian, German, Dutch) through the same HF repository. Evaluation pipelines that do not filter correctly could incorporate non-French data.

6. **IDMP compliance context**: The EU IDMP mandatory structured data extraction requirement (ISO 11615/11616/11240/11239/11238), which requires extracting approximately 70% of required data attributes from unstructured SmPC/eCTD text, is entirely unaddressed by DrBenchmark. This regulatory obligation is directly in scope for the deployment and has no benchmark analogue.

7. **EMA IRIS platform shift**: Since January 2025, the EMA IRIS platform is mandatory for Article 61(3) SmPC/PIL labeling notifications, potentially altering document formats encountered by the deployment system. Benchmark data predates this change and cannot validate performance on IRIS-formatted submissions.

---

### Cited Evidence

- **QUAERO-D1**: QUAERO/emea | 55 | CHEM/OBJC | "TYSABRI 300 mg solution à diluer pour perfusion natalizumab Chaque flacon de 15 ml de concentré contient 300 mg de natalizumab (20 mg/ml); phosphate de sodium, monobasique, monohydraté; chlorure de sodium; polysorbate 80 (E433) et eau pour préparation injectable." | Pharmaceutical composition list from SmPC-like regulatory text, annotating active substance and excipients | IC, OO
- **QUAERO-D2**: QUAERO/emea | 1 | CHEM | "Phosphate de sodium, monobasique, monohydraté Phosphate de sodium, dibasique, heptahydraté Chlorure de sodium Polysorbate 80 (E433) Eau pour préparation injectable." | Excipient list with E-numbers, as found in SmPC section 6.1 | IC
- **QUAERO-D3**: QUAERO/emea | 32 | PROC/CHEM | "Dans les études cliniques, la dose maximale prévue de ziconotide administré par voie intrarachidienne était de 912 µg/jour après une augmentation posologique sur 7 jours." | Posology expression with dose quantity and administration route annotated | IC, OO
- **QUAERO-D4**: QUAERO/emea | 17 | PROC | "La solution diluée doit être perfusée par voie intraveineuse pendant 1 heure à un débit d'environ 2 ml/minute." | Administration rate and IV route instruction in regulatory text | IC
- **QUAERO-D5**: QUAERO/emea | 23 | CHEM | "Prialt ne doit pas être utilisé chez l'enfant." | Pediatric contraindication in regulatory-register French | IC
- **QUAERO-D6**: QUAERO/emea | 64 | DISO/CHEM | "N'utilisez jamais TYSABRI […] Si vous êtes allergique (hydpersensible) au natalizumab ou à l'un des autres composants contenus dans TYSABRI […] Si vous avez des perturbations graves du système immunitaire (dues à une maladie, telle que leucémie ou infection à VIH…)" | Full contraindication block with population qualifiers, close to EU label format | IC, OO
- **QUAERO-D7**: QUAERO/emea | 51 | CHEM | "EMEA/H/C/122 REFLUDAN… Son principe actif est la lépirudine." | Brand name and INN both tagged CHEM, demonstrates INN extraction capability | IC, OO
- **QUAERO-D8**: QUAERO/emea | 36 | CHEM | "EMEA/H/C/122 Recommandations standard Comme la lépirudine est excrétée et métabolisée en quasi-totalité par le rein" | INN in pharmacokinetic context with EMA document header | IC
- **QUAERO-D9**: QUAERO/emea | 37 | GEOG | "La Commission européenne a délivré une autorisation de mise sur le marché valide dans toute l'Union européenne pour Tysabri à Elan Pharma International Ltd, le 27 juin 2006." | EMA marketing authorization reference in regulatory-genre French | IC, IF
- **QUAERO-D10**: QUAERO/emea | 34 | CHEM | "Contient également: mannitol, hydroxyde de sodium." | Excipients tagged identically to INNs (CHEM), preventing entity sub-class distinction | OO
- **QUAERO-D11**: QUAERO/emea | 50 | CHEM | "Refludan 50 mg en poudre pour solution injectable… le mannitol (E 421) et l'hydroxyde de sodium pour l'ajustement du pH." | Excipient same tag as INN, conflating distinct regulatory entity types | OO
- **QUAERO-D12**: QUAERO/emea | 36 | O | "EMEA/H/C/122" | EMA product number tagged O (no entity), missing key regulatory identifier class | OO, IC
- **QUAERO-D13**: QUAERO/medline | 7 | O | "Le soutien à la parentalité est-il une pierre dans le jardin des parents?" | Psychosocial topic, no regulatory pharmaceutical relevance | IO
- **QUAERO-D14**: QUAERO/medline | 16 | O | "L'apport des inventaires à la connaissance de la démographie parisienne ancienne: le règne de François Ier" | Historical-demographic abstract, outside biomedical regulatory domain | IC, IO
- **QUAERO-D15**: QUAERO/medline | 61 | O | "LÉON GRIMBERT 1860-1931." | Personal name/obituary fragment, no biomedical regulatory content | IC
- **QUAERO-D16**: QUAERO/emea | 43 | LIVB | "Par conséquent, Refludan ne doit pas être administré à la femme enceinte ou qui allaite." | Contraindication clause with pregnancy qualifier — UMLS tags entity type but not regulatory contraindication structure | OC
- **QUAERO-D17**: QUAERO/emea | 2 | DISO | "Une cirrhose du foie peut également affecter l'excrétion rénale de la lépirudine." | Pharmacokinetic safety interaction — DISO tag misses dosing-adjustment regulatory significance | OC
- **QUAERO-D18**: QUAERO/emea | 9 | CHEM | "Vous devez également prévenir votre médecin si jamais vous avez déjà pris du Refludan, une autre hirudine ou un analogue de l'hirudine." | Repeated appearance of same small set of drugs; limited entity vocabulary breadth | IC
- **QUAERO-D19**: QUAERO/emea | 4 | various | "Aucune étude clinique spécifique sur les interactions médicamenteuses n Toutefois, en raison des faibles concentrations plasmatiques du ziconotide…" | Truncated mid-sentence artifact from document splitting | IC, IF
- **QUAERO-D20**: QUAERO/emea | 63 | O | "r." | Single-character fragment, sentence-splitting artifact | IF
- **FRENCHMEDMCQA-D1**: FrenchMedMCQA | 6 | simple | "Parmi les substances suivantes, une seule ne traverse pas la barrière placentaire. Laquelle? Dicoumarine / Glucose / Héparine / Tétracycline / Amplicilline" | Pharmaceutical substance names in safety-relevant context (placental barrier) | IC
- **FRENCHMEDMCQA-D2**: FrenchMedMCQA | 13 | multiple | "Quel est (sont) le(s) diurétique(s) qui provoque(nt) une baisse du potassium sanguin? Chlortalidone / Hydrochlorothiazide / Furosémide / Spironolactone / Amiloride" | INN-style drug names as answer options in pharmacological classification | IC
- **FRENCHMEDMCQA-D3**: FrenchMedMCQA | 44 | multiple | "Peut entraîner des troubles cutanés sévères type syndrome de Lyell... l'association avec le méthotrexate est contre-indiquée" | Adverse effect and drug interaction contraindication language | IC
- **FRENCHMEDMCQA-D4**: FrenchMedMCQA | 100 | multiple | "Parmi les formes solides orales suivantes, indiquer celle(s) qui libère(nt) le principe actif de façon continue : Matrice hydrophile / Comprimé à enrobage par film insoluble..." | Pharmaceutical formulation types relevant to SmPC drug product sections | IC
- **FRENCHMEDMCQA-D5**: FrenchMedMCQA | 50 | multiple | "Parmi les verres suivants, indiquez ceux qui peuvent être utilisés comme conditionnement réutilisable des préparations pour usage parentéral : Verre de type I / Verre de type II..." | Packaging material standards relevant to regulatory CTD Module 3 | IC
- **FRENCHMEDMCQA-D6**: FrenchMedMCQA | 70 | multiple | "Les anti-vitamines K (AVK) sont formellement contre-indiquées avec : Le miconazole (DAKTARIN®) / Les beta-bloquants / Les salicylés à fortes doses..." | Formal contraindication language with brand name — matches regulatory label structure | IC
- **FRENCHMEDMCQA-D7**: FrenchMedMCQA | 105 | simple | "Une utilisation de médicament non conforme aux recommandations du résumé des caractéristiques du produit" | Explicit reference to SmPC (RCP) as regulatory concept — only occurrence across sample | IC, IO
- **FRENCHMEDMCQA-D8**: FrenchMedMCQA | 23 | multiple | "En électrophorèse capillaire haute performance, le sens de migration de l'analyse dépend : De la nature de la charge de l'analyte / Du flux d'électroendosmose..." | Pharmaceutical analytical technique question | IC
- **FRENCHMEDMCQA-D9**: FrenchMedMCQA | 31 | multiple | "La teneur en eau des matières premières est déterminée à l'aide de la méthode de Karl Fisher" | Raw material testing method present in regulatory CTD Module 3 | IC
- **FRENCHMEDMCQA-D10**: FrenchMedMCQA | 72 | multiple | "Parmi les propositions suivantes concernant la ceftriaxone (ROCEPHINE®)... C'est une céphalosporine de 3ème génération / Son importante demi-vie d'élimination est compatible avec une seule administration quotidienne" | INN + brand name + pharmacokinetic reasoning in formal French | IF
- **FRENCHMEDMCQA-D11**: FrenchMedMCQA | 1 | simple | "Au cours de la leucémie lymphoïde chronique, le myélogramme montre:" | MCQA format — tests knowledge retrieval, not NER or STS; task type mismatch | IO, OO
- **FRENCHMEDMCQA-D12**: FrenchMedMCQA | 15 | multiple | "Parmi ces effets indésirables, lesquels résultent du blocage des récepteurs cholinergiques : Sécheresse buccale / Constipation / Dysurie / Troubles de l'accommodation / Trouble de la mémoire" | Interrogative exam format vs. declarative regulatory prose — genre mismatch | IC, IO
- **FRENCHMEDMCQA-D13**: FrenchMedMCQA | 34 | multiple | "Cocher le ou les antibiotique(s) dont l'utilisation est autorisée en fin de grossesse : Ampicilline / Cotrimoxazole / Tétracyclines / Erythromycine / Péfloxacine" | Drug names as answer options — not in NER-extractable continuous text; no ATC codes | IC
- **FRENCHMEDMCQA-D14**: FrenchMedMCQA | 3 | multiple | "Parmi les propriétés suivantes du monoxyde de carbone, indiquer celle(s) qui est (sont) exacte(s)" | Classification of true/false propositions — no STS pairwise similarity signal | OO
- **FRENCHMEDMCQA-D15**: FrenchMedMCQA | 105 | simple | "Une utilisation de médicament non conforme aux recommandations du résumé des caractéristiques du produit" | SmPC reference appears only as a distractor option, not as regulatory prose text | IC, IF
- **FRENCHMEDMCQA-D16**: FrenchMedMCQA | 9 | multiple | "L'oeuf d'Enterobius vermicularis: Est incolore / Est asymétrique / Possède une coque double / Possède une coque lisse / Peut être à l'origine d'une auto-infestation" | Parasitology content with no pharmaceutical regulatory relevance | IC
- **FRENCHMEDMCQA-D17**: FrenchMedMCQA | 19 | multiple | "Parmi les phénotypes suivants, quel(s) est (sont) celui (ceux) que peuvent présenter les enfants issus d'un père AB Rh positif et d'une mère O Rh négatif?" | Blood group genetics with no regulatory relevance | IC
- **DEFT2020-D1**: DEFT2020/task_1 | 18 | moy=4.6 | "En raison de la présence de lactose, ce médicament est contre-indiqué en cas de galactosémie congénitale, de syndrome de malabsorption du glucose et du galactose ou de déficit en lactase." | Contraindication phrasing with excipient (lactose) — directly deployment-relevant regulatory text | IC
- **DEFT2020-D2**: DEFT2020/task_1 | 16 | moy=4.0 | "Ce produit peut provoquer un syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après la dernière prise de stupéfiant." | Drug safety warning with dose-time threshold — deployment-central entity type | IC
- **DEFT2020-D3**: DEFT2020/task_1 | 4 | moy=4.0 | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter pendant la durée du traitement." | Standard SmPC/leaflet precautionary instruction | IC
- **DEFT2020-D4**: DEFT2020/task_1 | 13 | moy=3.6 | "Chez les patients insuffisamment équilibrés par glimepiride arrow à la dose maximale, un traitement par l'insuline peut être associé si nécessaire." | INN (glimepiride) + posology qualifier in drug leaflet register | IC
- **DEFT2020-D5**: DEFT2020/task_2 | Ex.6 | correct_cible=2 | "en cas de traitement concomitant par un autre collyre , attendre 15 minutes entre chaque instillation" | Ophthalmic drug dosing instruction in patient leaflet register | IC
- **DEFT2020-D6**: DEFT2020/task_2 | Ex.22 | correct_cible=0 | "l' utilisation à forte dose d' huile de paraffine expose au risque de suintement anal et parfois d' irritation périanale" | Side-effect with dose qualifier from drug leaflet | IC
- **DEFT2020-D7**: DEFT2020/task_1 | 36 | moy=1.5, scores=[2.0,4.5,0.0,1.0,0.0] | "Après inspection, elles ont toutes été exclues." | High inter-annotator variance on borderline pair — illustrates scoring uncertainty | OO
- **DEFT2020-D8**: DEFT2020/task_1 | 54 | moy=5.0, scores=[5,5,5,5,5] | "Troubles de l'hémostase à type de maladie de Willebrand (se traduisant par un allongement du TCA, du temps de saignement et une diminution des taux du complexe VIIIC/VWF)." | Identical pair, unanimous perfect score — confirms annotator reliability on exact match | OC
- **DEFT2020-D9**: DEFT2020/task_1 | 65 | moy=4.3 | "- Ne pas utiliser chez les personnes présentant des difficultés de déglutition en raison du risque d'inhalation bronchique et de pneumopathie lipoïde." | Contraindication safety warning in EU leaflet formulaic register | IF
- **DEFT2020-D10**: DEFT2020/task_1 | 70 | moy=4.3 | "Prévenir les patients que la voie sublinguale constitue la seule voie efficace et bien tolérée pour l'administration de ce produit." | Administration route instruction in drug leaflet | IC
- **DEFT2020-D11**: DEFT2020/task_2 | Ex.27 | correct_cible=2 | "ce médicament est contre-indiqué dans les cas suivants" | Standard EU patient information leaflet section header | IF
- **DEFT2020-D12**: DEFT2020/task_2 | Ex.46 | correct_cible=0 | "les benzodiazépines et produits apparentés doivent être utilisés avec prudence chez le sujet âgé , en raison du risque de sédation et/ou d' effet myorelaxant qui peuvent favoriser les chutes" | Near-synonym discrimination (sédation vs. somnolence) in drug safety text | OO
- **DEFT2020-D13**: DEFT2020/task_1 | 6,7,9 | moy≈0–0.6 | "Certains apiculteurs sélectionnent leurs reines afin de favoriser au mieux la production." | Beekeeping encyclopedic content — irrelevant to regulatory deployment | IC
- **DEFT2020-D14**: DEFT2020/task_1 | 60 | moy=0.8 | "Les Canadiens de Montréal sont une franchise de hockey sur glace professionnel située à Montréal dans la province de Québec au Canada." | Sports content — zero regulatory relevance | IC
- **DEFT2020-D15**: DEFT2020/task_1 | 3 | moy=2.1 | "Boris Fiodorovitch Godounov, en russe : Бори́с Фёдорович Годуно́в (v.1551–Moscou, 13 avril 1605), gouverne la Russie à partir de 1594…" | Historical encyclopedic content — off-domain for regulatory NLP | IC
- **DEFT2020-D16**: DEFT2020/task_1 | 16 | moy=4.0 | "Ce produit peut provoquer un syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après la dernière prise de stupéfiant." | High similarity score despite addition of specific drug names in target — legally significant detail unmarked | OO
- **DEFT2020-D17**: DEFT2020/task_1 | 13 | moy=3.6 | "Chez les patients insuffisamment équilibrés par glimepiride arrow à la dose maximale, un traitement par l'insuline peut être associé si nécessaire." | "sous stricte surveillance médicale" absent in source; critical qualifier not flagged in score | OO
- **DEFT2020-D18**: DEFT2020/task_1 | 4 | moy=4.0 | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter pendant la durée du traitement." | Precautionary qualifier "par mesure de précaution" not penalized despite regulatory significance | OO
- **DEFT2020-D19**: DEFT2020/task_1 | 54 | moy=5.0 | "Troubles de l'hémostase à type de maladie de Willebrand (se traduisant par un allongement du TCA, du temps de saignement et une diminution des taux du complexe VIIIC/VWF)." | Only exact identity receives 5.0; near-synonyms not systematically distinguished from exact matches | OC
- **DEFT2020-D20**: DEFT2020/task_1 | 30 | moy=3.8 | "L'absorption de boissons alcoolisées est fortement déconseillée pendant le traitement (potentialisation réciproque)." | Mechanism qualifier "(potentialisation réciproque)" dropped in cible; not flagged as regulatory deviation by score | OC
- **DEFT2020-D21**: DEFT2020/task_1 | 26 | moy=3.4 | "Pour la comparaison entre blocs neuraxiaux et anesthésie générale, nous avons évalué la qualité des preuves comme très faible pour la mortalité…" | Cochrane review abstract register — not regulatory document prose | IO
- **DEFT2020-D22**: DEFT2020/task_2 | Ex.15 | correct_cible=2 | "lorsque le traitement ayurvédique…était comparé à la chlorpromazine chez les patients atteints de schizophrénie aiguë, il était équivalent (~10 % d'attrition, n = 36, rr de 0,67, ic entre 0,13 et 3,53)" | Research meta-analysis register with statistics — distinct from regulatory submission language | IO
- **DEFT2020-D23**: DEFT2020/task_2 | Ex.1 | correct_cible=0 | "2008 est une année du calendrier grégorien faisant partie des années 2000 et du XXIe siècle." | Trivially irrelevant distractor — reduces task discriminative validity for regulatory use | OO
- **DEFT2020-D24**: DEFT2020/task_2 | Ex.7 | correct_cible=0 | "Nintendo" | Single-word off-domain distractor — no challenge for regulatory document discrimination | OO
- **MORFITT-D3**: MORFITT | 19 | pharmacology | "Déterminer la stabilité physicochimique et microbiologique de suspensions de sulfadiazine (100 mg/mL)… Les formulations présentaient une concentration en sulfadiazine d'environ 95% au début" | Drug stability abstract with dosage and formulation content — nearest to regulatory pharmaceutical content | IC, IO
- **MORFITT-D4**: MORFITT | 33 | pharmacology, chemistry | "Les eaux thermales sont couramment utilisées comme substances actives dans les formulations cosmétiques… Une eau thermale commerciale a été utilisée comme phase aqueuse dans 5 formulations différentes" | Formulation chemistry abstract; partial overlap with excipient/galenic form vocabulary | IC, IO
- **MORFITT-D5**: MORFITT | 2 | pharmacology | "La morphine intraveineuse a atténué de façon dose-dépendante les réponses nociceptives chez les souris C57BL/6 et CD-1 (DI 50, 0,6 et 2,5 mg·kg−1)" | Drug name, dosage, and route entities present in text but not annotated at token level | IC
- **MORFITT-D6**: MORFITT | 4 | parasitology, genetics | specialities_one_hot [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0] | Multi-label assignment confirmed as genuinely multi-label | OO, OF
- **MORFITT-D7**: MORFITT | 1 | surgery | "La mise en place par cathétérisme d'une valve aortique (TAVI)… Le registre France-TAVI… va inclure plus de 3 000 cas" | Abstract-level classification only; no token-level entity annotations for NER task | IO, OO
- **MORFITT-D8**: MORFITT | 23 | microbiology | "Nous rapportons ici l'histoire d'un patient porteur d'une infection multifocale à Nocardia Farcinica associant des abcès cérébraux, une infection pulmonaire, une endocardite" | Clinical case abstract; no NER ground truth; confirms task type mismatch | IO, OO
- **MORFITT-D9**: MORFITT | 7 | psychology | "Des interventions favorables et ciblées pour les familles sont nécessaires afin d'optimiser l'ajustement parental… Le but de cette revue systématique était de déterminer l'efficacité des interventions" | Systematic review abstract; academic biomedical French; no regulatory register | IO, IC
- **MORFITT-D10**: MORFITT | 34 | surgery | "La vertébroplastie percutanée est utilisée depuis presque 30 ans, ce n'est qu'en 2007 que le premier essai randomisé a été publié" | Clinical trial review; no regulatory document genre present | IO, IC
- **MORFITT-D11**: MORFITT | 29 | veterinary | "Les indications rapportées sont le traitement de la dermatite atopique… Peu d'effets secondaires ont été observés aux doses utilisées" | Drug names and dosage references present in text but unannotated at token level | IC, OO, OC
- **MORFITT-D12**: MORFITT | 19 | pharmacology | "Un test de chromatographie liquide ultra-performante a été développé et validé pour déterminer la stabilité chimique de la sulfadiazine" | Pharmaceutical compound in text; classified only at specialty level, no entity annotation | IC, OO
- **MORFITT-D13**: MORFITT | 8 | microbiology | "La région du Nord-Ouest de l'Ontario présente un taux élevé et documenté d'infections de la peau… causées par une souche de Staphylococcus aureus méthycillinorésistante d'origine communautaire" | Canadian clinical context; jurisdictional mismatch with EMA/ANSM | IC, OC
- **MORFITT-D14**: MORFITT | 13 | genetics | "En 2007 et 2008, 4 423 adultes de Calgary ont répondu à des entrevues au téléphone fixe" | Canadian population study; non-EU context | IC, OC
- **MORFITT-D15**: MORFITT | 32 | microbiology | "Évaluer la charge des maladies d'origine alimentaire au Japon… pour l'année 2011" | Japanese epidemiological study; non-EU regulatory context | IC, OC
- **MORFITT-D16**: MORFITT | 31 | psychology | "La présente étude transversale a étudié les attitudes de médecins internes en Arabie saoudite" | Saudi Arabian medical survey; non-EU jurisdiction | IC, OC
- **MORFITT-D17**: MORFITT | 9 | veterinary | "L'otite externe est une maladie multifactorielle fréquente chez le chien… Décrire le microbiote bactérien auriculaire des chiens avec otite externe" | Canine veterinary content irrelevant to human drug labeling | IO, IC
- **MORFITT-D18**: MORFITT | 26 | veterinary, parasitology, genetics | "Prévalence et caractéristiques morphologiques et moléculaires de Sarcocystis bertrami chez les chevaux en Chine" | Equine parasitology in China; fully outside deployment scope | IO, IC
- **MORFITT-D19**: MORFITT | 10 | genetics | "Le nombre croissant de colonies d'abeilles mellifères et d'apiculteurs au Canada… lutter contre les maladies" | Beekeeping disease management; unrelated to pharmaceutical regulatory deployment | IO, IC
- **CLISTER-D1**: CLISTER | 9 | 0.0 | "Le patient fut donc traité par 1 instillation hebdomadaire intra-vésicale de 81 mg de BCG, pendant 6 semaines." | French clinical prose with dosage and treatment protocol | IC, IF
- **CLISTER-D2**: CLISTER | 41 | 2.0 | "Métoprolol 50 mg deux fois par jour;" / "Metformine 500 mg, 1 comprimé deux fois par jour" | Drug dosage expressions in clinical French notation | IC
- **CLISTER-D3**: CLISTER | 98 | 2.0 | "Acide folinique 15 mg une fois par jour" / "Aspirine 80 mg, 1 comprimé une fois par jour" | Drug-dose pairs structurally similar to posology entries | IC
- **CLISTER-D4**: CLISTER | 116 | 1.0 | "10 à 25 mg une fois par jour" / "Propranolol 40 mg, 1 comprimé deux fois par jour" | Dose-only vs. drug-plus-dose comparison | IC
- **CLISTER-D5**: CLISTER | 168 | 1.0 | "On augmente la dose de phénytoïne à 350 mg par voie intraveineuse une fois par jour." / "La dose maximale de mirtazapine devrait être de 30 mg par jour ou exceptionnellement 45 mg par jour." | Dosage comparison sentence pair | IC
- **CLISTER-D6**: CLISTER | 10 | 5.0 | "Une mastectomie était réalisée avec curage axillaire." / "Une mastectomie avec curage axillaire ont été réalisés." | Near-paraphrase correctly scored maximum | OO
- **CLISTER-D7**: CLISTER | 85 | 4.0 | "Le bilan rénal a objectivé une insuffisance rénale avec une créatininémie à 1440 μmol/l…" / "Le bilan biologique a révélé une insuffisance rénale avec une urée à 2,25g/l…" | Numerically different but semantically related values scored 4.0 | OO
- **CLISTER-D8**: CLISTER | 5 | 2.75 | "Le reste de l'examen échographique ne trouvait aucune autre anomalie." / "Le reste de l'examen somatique était sans anomalie." | Mid-range score for partial semantic overlap | OO
- **CLISTER-D9**: CLISTER | 149 | 0.5 | "Lithium 300 mg x x x x…" / "300 mg IV aux 24 h x x x…" | Near-zero score for tabular entries sharing dose notation | OO
- **CLISTER-D10**: CLISTER | 6 | 0.0 | "La patiente a eu, dans le même temps opératoire, une lithotritie balistique du calcul par voie endoscopique permettant de dénuder le DIU puis de l'extraire par une pince à corps étranger." | Clinical case narrative; not SmPC format | IO, IC
- **CLISTER-D11**: CLISTER | 222 | 0.0 | "CMV : cytomegalovirus; DCI : dénomination commune internationale; HTAP : hypertension artérielle pulmonaire; NR : non renseigné; RGO : reflux gastro-oesophagien" | Abbreviation glossary from clinical case, not regulatory document | IO
- **CLISTER-D12**: CLISTER | 188 | 4.0 | "L'AHG urinaire est à 10 mmol/l." / "L'AHG urinaire est à 20 mmol/l." | 2× quantitative difference scored 4.0 (very similar) | OO, OC
- **CLISTER-D13**: CLISTER | 90 | 3.0 | "Le taux de PSA était de 218 ng/ml (normale ≤ 4ng/ml)." / "Le dosage de PSA était de 13327 ng/ml (normal : < 4 ng/ml)." | 60× magnitude difference scored 3.0 | OO, OC
- **CLISTER-D14**: CLISTER | 123 | 3.75 | "Le taux de PSA était de 4,49 ng/ml." / "Le taux de PSA total était à 66,68 ng/ml." | 14× numeric discrepancy scored near-similar | OO, OC
- **CLISTER-D15**: CLISTER | 4 | 0.0 | "Le testicule gauche est normal." / "Le toucher rectal est normal." | Clinical examination findings; no regulatory entity type | IC, IO
- **CLISTER-D16**: CLISTER | 7 | 4.0 | "La patiente a été opérée et lors de l'exploration on découvrit qu'il s'agissait d'une tumeur de la veine cave inférieure sus-rénale." / "L'examen anatomopathologique de la pièce confirmait qu'il s'agissait d'un léiomyosarcome de la veine cave." | Surgical/pathological reporting; no regulatory relevance | IC
- **CLISTER-D17**: CLISTER | 41 | 2.0 | "Métoprolol 50 mg deux fois par jour;" / "Metformine 500 mg, 1 comprimé deux fois par jour" | Different INNs scored 2.0 due to structural template; regulatory judgment would score near 0 | OC
- **CLISTER-D18**: CLISTER | 164 | 2.0 | "Ésoméprazole 20 mg/jour Hépatique T1/2 = 1,0 – 1,5 h" / "Périndopril 2 mg/jour NR T1/2 = 17 h" | Different INNs and PK profiles scored 2.0; inconsistent with regulatory equivalence | OC
- **CLISTER-D19**: CLISTER | 8 | 1.0 | "Jour 45 - - - - - - - - - 25 μg 0,4 mg" / "Jour 53 15,13 12,0 1,58 - - - - - - 25 μg 0,4 mg" | Table row fragments, not natural-language sentences | IF, OF
- **CLISTER-D20**: CLISTER | 48 | 2.0 | "Jour 91 - - - - - - - - - Fin 0,4 mg" / "Jour 187 1,67 21,2 1,38 - - - - - - - 0,4 mg" | Numeric table rows without natural-language predication | IF, OF
- **CLISTER-D21**: CLISTER | 53 | 5.0 | "Les suites post-opératoires étaient simples." / "Les suites post-opératoires sont simples." | Tense-only variation; negligible linguistic variation | OO
- **CLISTER-D22**: CLISTER | 117 | 5.0 | "Les suites ont été simples." / "Les suites sont simples." | Auxiliary tense variation only; ceiling concentration concern | OO
- **MANTRAGSC-D1**: fr_emea | d335.u292 | CHEM(2) | "Chaque comprimé contient 500 mg de ranolazine." | Drug composition statement with INN annotated CHEM; EMEA register | IC, IO
- **MANTRAGSC-D2**: fr_emea | d16.u650 | CHEM(2), LIVB(7) | "Patients de 4 ans et plus dans l' incapacité d' avaler les capsules: la posologie recommandée d' Agenerase solution buvable est de 17 mg (1,1 ml)/ kg trois fois par jour, sans excéder la dose maximale de 2800 mg par jour" | Full posology expression with patient population qualifier; dose ceiling unannotated | IC, OO
- **MANTRAGSC-D3**: fr_emea | d73.u262 | CHEM(2) | "La dose habituelle de Cholestagel est de 3 comprimés pris deux fois par jour à l' occasion des repas ou de 6 comprimés par jour" | Standard dosage instruction language from EMEA label | IC
- **MANTRAGSC-D4**: fr_emea | d312.u295 | DISO(5) | "Vous ne devez pas prendre Pramipexole Teva si vous allaitez." | Contraindication in patient leaflet register; condition tagged DISO not as contraindication type | OO, OC
- **MANTRAGSC-D5**: fr_emea | d103.u262 | CHEM(2) | "1 ml de solution contient 40 microgrammes de travoprost et 5 mg de timolol (sous forme de maléate de timolol)" | INN and salt excipient form both tagged CHEM; no INN/excipient distinction | OO, IC
- **MANTRAGSC-D6**: fr_emea | d426.u28 | CHEM(2) | "Cette étude a comparé l' efficacité de Tyverb en association avec la capécitabine" | Brand name and INN in same sentence; both CHEM, no proprietary/INN distinction | OO
- **MANTRAGSC-D7**: fr_patents | dEP-1414451-B1.u0019 | CHEM(2) | "Forme posologique orale selon la revendication 1, dans laquelle ledit antagoniste opioïde libérable est la naltrexone et ledit opioïde libérable est la codéine, dans laquelle le rapport de la naltrexone sur la codéine libérable est de 0,005 : 1 à 0,044 : 1." | French patent claim with INNs and dosage ratio; patent claim register confirmed | IC, IO
- **MANTRAGSC-D8**: fr_patents | dEP-1663257-B1.u0006 | CHEM(2) | "L' utilisation selon la revendication 3, où le laxatif osmotique est du glycol de polyéthylène 3350." | Excipient/drug substance in patent claim; CHEM tag does not distinguish excipient from INN | IC, OO
- **MANTRAGSC-D9**: fr_emea | d61.u583 | DISO(5)/PHEN | "Des symptômes potentiellement liés à l' histamine tels que éruption cutanée étendue, gonflement du visage et/ ou des lèvres, démangeaisons, sensation de chaleur ou difficulté à respirer, ont été rapportés." | Adverse reaction listing in SmPC section 4.8 language | IC
- **MANTRAGSC-D10**: fr_emea | d157.u265 | ANAT(1) | "Les effets indésirables, en dehors des cas isolés, sont repris ci-dessous: ils sont classés par organe et par ordre de fréquence" | Standard SmPC adverse effect section header | IC
- **MANTRAGSC-D11**: HF Metadata | fr_emea splits | — | train=70, validation=10, test=20 | Test set of 20 examples is statistically insufficient for robust NER evaluation | IO
- **MANTRAGSC-D12**: HF Metadata | fr_patents splits | — | train=70, validation=10, test=20 | Same size constraint for patent genre evaluation | IO
- **MANTRAGSC-D13**: fr_emea | d103.u262 | CHEM(2) | "travoprost et 5 mg de timolol (sous forme de maléate de timolol)" | INN and salt excipient both tagged CHEM; schema cannot distinguish excipient from active substance | OO
- **MANTRAGSC-D14**: fr_emea | d349.u242 | CHEM(2) | "Renagel 800 mg sevelamer" | Brand name and INN both CHEM; no proprietary/INN label distinction critical for regulatory workflows | OO
- **MANTRAGSC-D15**: fr_medline | d7569194.u1 | DISO(5) | "Luxation antérieure ouverte post-traumatique de la hanche chez l'enfant. A propos d'un cas et revue de la littérature." | Research abstract title; clinical case register; not regulatory prose | IC, IF
- **MANTRAGSC-D16**: fr_medline | d4876372.u1 | PROC(13) | "Le problème de la régulation des naissances: aspects médico-légaux et médico-sociaux." | Non-pharmaceutical medical prose; irrelevant to regulatory NLP | IC
- **MANTRAGSC-D17**: fr_patents | dEP-2137166-B1.u0009 | CHEM(2) | "Composé selon l'une quelconque des revendications 3 à 8, dans lequel R106 est choisi parmi un hydrogène, un alkyle substitué ou insubstitué en C1-C8" | Chemical structure claim; no drug product or INN; sparse annotation on technical nomenclature | IC
- **E3C-D1**: French_clinical | 195 | 1 (CLINENTITY) | "Le bilan biologique montrait une cholestase (bilirubine totale a \`140 mmol/L, bilirubine conjugue à 80 mmol/L, phosphatases alcalines à 700 UI/L)" | Clinical lab results sentence in formal French; `cholestase` annotated as clinical entity | IC
- **E3C-D2**: French_clinical | 111 | all 0 | "Le patient a été mis sous traitement par ciclosporine avec une évolution rapide vers une leucémie aigue myéloblastique." | Drug name `ciclosporine` present but tagged O — pharmaceutical entities not annotated | OO, OC
- **E3C-D3**: French_temporal | 239 | 1 (EVENT) | "Le diagnostic retenu est celui d'une méningo-vascularite bactérienne révélant un adénome hypophysaire à prolactine." | Formal clinical diagnostic statement; shows clinical case register | IC
- **E3C-D4**: French_clinical | 64 | 1 (CLINENTITY) | "La patiente a déjà mené une première grossesse à terme il y a 9 ans, donnant naissance à un petit garçon en bonne santé." | Narrative patient history; typical clinical case format, not regulatory document | IC, IO
- **E3C-D5**: French_clinical | 385 | all 0 | "L'examen ophtalmologique retrouve une semi-mydriase aréflexique gauche avec au fond d'œil montre une occlusion de l'artère centrale de la rétine." | Clinical examination description; narrative register far from regulatory prose | IC
- **E3C-D6**: French_clinical | 54 | 1 (CLINENTITY) | "Cet aspect évoquait une tumeur solide du péritoine." | Pathology annotated as CLINENTITY; no pharmaceutical or regulatory entity layer | OO
- **E3C-D7**: French_clinical | 186 | 1 (CLINENTITY) | "La tomodensitométrie objectivait une formation kystique multicloisonnée, bien limitée de 128x115mm" | Imaging finding annotated; schema contains no drug/dosage/regulatory entity class | OO
- **E3C-D8**: Basque_clinical | 180 | all 0 | "Azken hilabeteetan Ikernek kodeina + ibuprofenoa hartu ditu, baina ez du hobekuntza handirik nabaritu." | Basque text; completely outside French regulatory deployment scope | IF, IC
- **E3C-D9**: English_clinical | 188 | 0 | "A chest radiograph showed right upper lobe consolidation with volume loss, right para-tracheal and left hilar adenopathy" | English clinical text; irrelevant to French deployment | IF
- **E3C-D10**: French_temporal | 107 | 2/7 (ACTOR) | "Il s'agit d'une patiente de 44 ans, sans antécédent médico-chirurgical, qui a présenté depuis un an des céphalées, compliquées 08 mois après de crises d'épilepsies partielles" | Narrative case presentation; temporal entity tagging on clinical events, not regulatory text | IC, OC
- **E3C-D11**: French_temporal | 304 | 1 (EVENT) | "L'examen physique a mis en évidence une volumineuse tuméfaction dorsolombaire gauche ovalaire mesurant 24cm de grand axe et 12cm de petit axe" | Physical examination clinical narrative; structurally absent from regulatory document sections | IC
- **E3C-D12**: Basque_clinical | 6 | 0 | "." | Single punctuation token; degenerate example contributing to sparse annotation | OC
- **E3C-D13**: French_clinical | 89 | all 0 | "Le reste de l'examen est inaccessible." | No entity present; contributes to negative-dominated label distribution | OC
- **PXCORPUS-D1**: PxCorpus | 5 | medical_prescription | "primperan 10 milligrammes comprimés 1 comprimé en cas de nausée toutes les 8 heures pendant 14 jours" | Full prescription structure with drug name, dose, form, frequency, indication, duration | IC, OO
- **PXCORPUS-D2**: PxCorpus | 51 | medical_prescription | "ténofovir 245 milligrammes en comprimés à prendre après les repas 1 comprimé le soir pendant 2 semaines puis stop" | INN drug name with dosage, route instruction, and duration | IC
- **PXCORPUS-D3**: PxCorpus | 97 | medical_prescription | "morphine 10 milligrammes toutes les 4 heures pendant 2 mois" | Controlled substance with frequency interval and duration | IC
- **PXCORPUS-D4**: PxCorpus | 100 | medical_prescription | "oramorph 20 milligrammes par millilitres 5 gouttes en cas de douleur ne pas dépasser 6 gouttes par jour" | Per-unit concentration and maximum-dose ceiling | IC
- **PXCORPUS-D5**: PxCorpus | 38 | none | "la posologie est à 0,0 au lieu de 0,01 25 milligrammes" | Explicit dosage discrepancy reference; relevant to compliance-flagging | IC
- **PXCORPUS-D6**: PxCorpus | 4 | replace | "attention il s'agit de 20 milligrammes et pas 10 milligrammes" | Explicit dosage correction; directly relevant to dose-discrepancy detection | IO, OO
- **PXCORPUS-D7**: PxCorpus | 8 | replace | "remplacer 1 comprimé tous les jours par 1 comprimé en cas d'anxiété" | Frequency/indication substitution captured by replace intent class | IO, OO
- **PXCORPUS-D8**: PxCorpus | 145 | medical_prescription | "lévothyroxine sodique 50 microgrammes 1 comprimé à prendre le matin à jeun pendant 6 semaines" | INN with salt suffix, administration condition, and posology | IC
- **PXCORPUS-D9**: PxCorpus | 119 | medical_prescription | "tropatepine chloridrate 1o milligrammes 1 comprimé le midi" | INN + salt form with minor transcription error ("1o" for "10"), showing ASR noise | IF, IC
- **PXCORPUS-D10**: PxCorpus | 3 | none | "/chet" | Single-token ASR artifact with no lexical content; not regulatory text | IF
- **PXCORPUS-D11**: PxCorpus | 10 | negate | "ne pas tenir compte à midi tous les jours merd/" | Profanity and truncation in spoken transcript; absent from regulatory documents | IF, IC
- **PXCORPUS-D12**: PxCorpus | 88 | none | "i'll agree come on say avec successes merde je vais roulé faut lui faire un et mettre la rame en mode français" | English/French code-switching and informal register unlike regulatory prose | IF, IC
- **PXCORPUS-D13**: PxCorpus | 207 | medical_prescription | "teralithe 250 milligrammes / le serveur de dialogue met beaucoup de temps à comprendre votre énoncé veuillez reformuler différemment" | System dialogue prompt embedded in training example; not a regulatory text pattern | IF, IC
- **PXCORPUS-D14**: PxCorpus | 18 | none | "la partie euh posologie est sur 6 ou 8 semaines là il n'est écrit que 8 semaines par contre le qsp 6 semaines a été rajouté en remarque pharmaceutique" | Closest example to regulatory commentary but spoken, informal, not document-register | IC, IO
- **PXCORPUS-D15**: PxCorpus | 103 | medical_prescription | "trémétadisine trémétasidine à 20 milligrammes à 3 comprimés par jour pendant 3 semaines" | Near-identical drug name variants without ATC linkage or excipient field | OO
- **PXCORPUS-D16**: PxCorpus | 22 | medical_prescription | "sirop de potassium richard 1 cuillerée à soupe matin et soir pendant 1 mois" | "potassium richard" tagged as modifier, not recognized INN or excipient class | OO
- **PXCORPUS-D17**: PxCorpus | 4 | replace | "attention il s'agit de 20 milligrammes et pas 10 milligrammes" | One of only ~3 replace-class examples in 500-example buffer; class severely underrepresented | OC, OO
- **PXCORPUS-D18**: PxCorpus | 12 | replace | "non prendre 150 milligrammes par jour" | Replace class example; rarity limits model reliability for correction-detection task | OC, OO
- **DIAMED-D1**: DiaMED | 1 | A00-B99 | "Le test rapide VIH était positif, confirmé par la sérologie VIH avec un taux de CD4 à 27/mm3." | Confirms dense biomedical vocabulary and clinical register; HIV serology result | IC, IF
- **DIAMED-D2**: DiaMED | 2 | C00-D49 | "4 cures de chimiothérapie palliative selon le protocole LV5 FU2 (5-Fluoro-uracile associé à l'acide folinique)" | Chemotherapy protocol mention with drug name — pharmaceutical entity in clinical narrative | IC
- **DIAMED-D3**: DiaMED | 3 | D50-D89 | "une antibioprophylaxie (association Amoxicilline et acide clavulanique)" | Drug combination mention; keywords include 'Maroc' — non-EU regulatory geographic context | IC, IF
- **DIAMED-D6**: DiaMED | 6 | G00-G99 | "Monsieur Y. O. âgé de 19 ans a été hospitalisé le 03 février 2012 pour une paraplégie évoluant depuis un mois." | Classic clinical case narrative register; entirely distinct from regulatory document genre | IO, IC
- **DIAMED-D8**: DiaMED | 8 | H60-H95 | "une antibiothérapie injectable empirique instaurée à base de céphalosporines de troisième génération et de ciprofloxacine" | Drug class and named drug in clinical treatment narrative; not in EMA SmPC format | IC, IF
- **DIAMED-D9**: DiaMED | 9 | I00-I99 | "Communication interventriculaire ischémique: à propos d'un cas observé dans le service de cardiologie du CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" | Sub-Saharan African hospital setting; non-EU regulatory context | IC, IF
- **DIAMED-D11**: DiaMED | 11 | K00-K95 | "suture de la rupture gastrique par un surjet au polyglactin 910 (vicryl*2/0)" | Trade name usage in surgical narrative; clinical protocol differs from regulatory document conventions | IC, IF
- **DIAMED-D12**: DiaMED | 12 | L00-L99 | "200mg de Phénobarbital à prendre en une prise vespérale... Halopéridol 20 mg et Chlorpromazine 400 mg en deux prises par jour" | Named drugs with dosages — closest to deployment entity types, but unannotated and embedded in clinical narrative | IC, OO
- **DIAMED-D13**: DiaMED | 13 | M00-M99 | "Il s'agit d'un adolescent âgé de 16 ans, sportif (tennis) qui se plaignait depuis plusieurs mois de douleurs mécaniques du coude droit." | Clinical case narrative about orthopedic condition; no pharmaceutical content | IO
- **DEFT2021-D1**: DEFT2021/cls | 3 | [6,14,13,19,4] | "clarithromycine 500 mg deux fois par jour pendant 10 jours... sulfate de quinidine 200 mg trois fois par jour" | Drug names with explicit dosage and frequency — relevant to deployment NER targets | IC
- **DEFT2021-D2**: DEFT2021/cls | 8 | [20,17,22,13,0,4,19] | "rituximab 375 mg/m2 par voie IV, à raison d'une fois par semaine pendant quatre semaines... mofétil mycophénolate (MMF) 500 mg par voie orale, deux fois par jour" | Dense posology expressions with route and frequency | IC
- **DEFT2021-D3**: DEFT2021/ner | 80 | SUBSTANCE/DURATION | "rifampicine – isoniazide – pyrazinamide pendant 6 mois" | Drug names tagged as SUBSTANCE with duration — partial INN coverage | OO
- **DEFT2021-D4**: DEFT2021/ner | 55 | SUBSTANCE/DOSAGE/MODE | "Hydrocortisone 300 mg IV... Hydroxyzine 25 mg par voie orale toutes les 6 heures" | Drug + dose + route + frequency tagged; matches deployment posology targets | OO, IC
- **DEFT2021-D5**: DEFT2021/ner | 7 | SUBSTANCE/DURATION | "cotrimoxazole pour 10 jours" | Drug and duration extraction; treatment annotation | OO
- **DEFT2021-D6**: DEFT2021/cls | 3 | [6,14,13,19,4] | specialities include pharmacology and cardiovascular; text covers CYP3A4, P-gp, IKr/IKs drug interactions | Pharmacology-relevant classification with named drugs | IO
- **DEFT2021-D7**: DEFT2021/cls | 5 | [12,3,20,4,7,5] | "buprénorphine (Subutex)... lévopromazine (Tercian)... paroxétine (Divarius)... prise d'une quantité importante de Codoliprane" | Toxicology specialty; drug names and overdose context | IO
- **DEFT2021-D8**: DEFT2021/cls | 1 | [18,4] | "Femme de 73 ans n'ayant eu qu'un seul enfant par césarienne, mais présentant depuis plusieurs années un prolapsus de stade III" | Patient narrative format — clinical case, not regulatory document | IO, IC
- **DEFT2021-D9**: DEFT2021/cls | 2 | [4,9,18] | "Mme M.J., âgée de 66 ans consultait pour des lombalgies droites lancinantes" | Clinical consultation narrative; no regulatory register | IO, IC
- **DEFT2021-D10**: DEFT2021/cls | 6 | [12,17,4] | "Monsieur B..., âgé de 36 ans, aux antécédents de gastrite" | Clinical case patient history, entirely clinical genre | IO, IC
- **DEFT2021-D11**: DEFT2021/ner | 28 | DISO | "carcinome vésical droit... carcinome urothélial multiple" | Pathology/disease entity annotation — clinical schema dominant | OO
- **DEFT2021-D12**: DEFT2021/ner | 4 | DISO/PROC | "kyste épidermoïde isolé... analyse anatomo-pathologique" | Clinical entity types; no regulatory entity classes | OO
- **DEFT2021-D13**: DEFT2021/ner | 55 | SUBSTANCE | "Hydrocortisone... Hydroxyzine" tagged as SUBSTANCE without INN/ATC specificity | Drug names captured but undifferentiated from other substances; no ATC linkage | OO, IC
- **DEFT2021-D14**: DEFT2021/cls | 3 | [6,14,13,19,4] | Drug interaction case labeled with MeSH pharmacology axes; no regulatory equivalence structure | Annotation captures clinical specialty, not regulatory compliance | OC
- **DEFT2021-D15**: DEFT2021/ner | 3 | SUBSTANCE/PROC | "diphenhydramine et de méthylprednisolone... prémédication" | Clinical semantic annotation; no regulatory labeling hierarchy | OC
- **DEFT2021-D16**: DEFT2021/cls | schema | — | features: id, document_id, text, specialities, specialities_one_hot | No STS pair structure; classification only; cannot evaluate regulatory equivalence scoring | OO, OF
- **CAS-D2**: CAS/cls | cls/train/467 | neutral | "après mise en condition en unité de soins intensifs et administration d' une ampoule de digoxine en intraveineuse , un bilan radiologique a été réalisé ." | Contains drug name (digoxine) and route of administration in clinical narrative | IC
- **CAS-D3**: CAS/cls | cls/train/49 | speculation | "une origine médicamenteuse étant envisagée ( avec éventuellement une imputabilité du paracétamol ) , il était décidé d' arrêter les différents traitements et de remplacer les lavements de pentasa ® par du proctocort ® ( hydrocortisone acétate 90 mg : 1 lavement tous les soirs ) ." | Multiple drug names, dosage and frequency — highest pharmaceutical entity density in sample, but in clinical not regulatory register | IC
- **CAS-D4**: CAS/cls | cls/train/605 | speculation | "puisque le traitement par la warfarine semble plus problématique , un naco est envisagé ." | Drug class mention (NOAC) under speculation marker; shows hedge around drug choice | IC, OO
- **CAS-D5**: CAS/ner_neg | ner_neg/train/75 | IOB2 negation | tokens: ['sans', 'antécédent', 'familial', 'de', 'maladie', 'colique']; ner_tags: [0, 1, 2, 2, 2, 2] | Negation scope spanning clinical history phrase; shows annotation granularity | OO
- **CAS-D6**: CAS/ner_neg | ner_neg/train/637 | IOB2 negation | "ne montrait aucune lésion focale" with negation tags on "montrait" and "lésion focale" | Dual-cue negation encoded; relevant to safety-warning negation detection | OO
- **CAS-D8**: CAS/cls | cls/train/682 | negation_speculation | "Il s'agit d'une patiente âgée de 63 ans , sans antécédents particuliers , ménopausée depuis 14 ans , célibataire , sans enfants , qui a consulté pour algies pelviennes chroniques..." | Prototypical clinical case narrative register, fundamentally different from regulatory document prose | IO, IC
- **CAS-D9**: CAS/cls | cls/train/128 | neutral | "depuis hier soir , je suis essouflé , j' ai des frissons , j' ai mal à la poitrine , là en bas à gauche , surtout quand j' inspire à fond ." | Patient first-person voice — genre entirely absent from EU regulatory submissions | IO, IC
- **CAS-D10**: CAS/ner_neg | ner_neg/train/467 | all-O | "administration d' une ampoule de digoxine en intraveineuse" — all ner_tags = 0 | Drug name "digoxine" not annotated as any entity; confirms no pharmaceutical entity schema | OO, IC
- **CAS-D11**: CAS/ner_spec | ner_spec/train/84 | IOB2 speculation | tokens: ['le', 'diagnostic', "d'", 'ulcère', 'solitaire', 'du', 'rectum', 'était', 'évoqué']; ner_tags: [1, 2, 2, 2, 2, 2, 2, 2, 0] | Speculation span over diagnostic phrase — schema captures linguistic modality, not entity type | OO
- **CAS-D12**: CAS/ner_neg | ner_neg/train/305 | IOB2 negation | tokens: ['les', 'ovaires', 'ne', 'montraient', 'pas', "d'", 'anomalie']; ner_tags: [0, 0, 0, 1, 0, 2, 2] | Negation cue "ne…pas" tagged with B on verb not on "ne"; annotation boundary decisions undocumented | OC
- **CAS-D13**: CAS/cls | cls/train/176 | speculation | "cholstat ® 0.1 ." | Single drug name + dosage fragment labeled speculation with no visible hedge marker; suggests noisy annotation boundary | OO, OC
- **ESSAI-D1**: ESSAI/pos | 226 | neutral | "avec la combinaison gemcitabine + abraxane, chez des patients avec un cancer du pancréas" | Drug INN + brand name co-occurrence in trial text | IC
- **ESSAI-D2**: ESSAI/cls | 1 | negation_speculation | "chimiothérapie à hautes doses avec une combinaison de Busulfan et de Melphalan (BU-MEL) permettra d'obtenir une survie sans événement à 3 ans supérieure à une consolidation par une association de Carboplatine VP16 et Melphalan" | Multi-drug combination with posology context | IC
- **ESSAI-D3**: ESSAI/ner_neg | 2 | O | "Le MEDI9197 est injecté en intra-tumoral tous les 28j (4 semaines)" | Dosing frequency and administration route in trial protocol | IC
- **ESSAI-D4**: ESSAI/ner_spec | 3 | O | "Lorsque la chimiothérapie à base de platine est associée au Caelyx, les perfusions ont lieu tous les quinze jours pendant 6 mois (cycles de 28 jours) puis une maintenance est ensuite instaurée avec le Bevacizumab et l'Atezolizumab ou placebo perfusés toutes les 3 semaines" | Complex multi-drug dosing schedule | IC
- **ESSAI-D5**: ESSAI/cls | 2 | negation | "se sont montrés tout aussi efficace et ne présentent pas plus d'effets secondaires dans différents essais cliniques sur plusieurs milliers de patientes" | Negation of adverse effects — safety-relevant | OO
- **ESSAI-D6**: ESSAI/cls | 4 | speculation | "Dans les formes inopérables et/ou métastatiques, le seul traitement approuvé depuis 2008 est le sorafenib" | Approval claim with temporal boundary | OO
- **ESSAI-D7**: ESSAI/cls | 21 | negation_speculation | "Absence d'insuffisance hépatique ou rénale — Chimiothérapie pré-opératoire de 2ème ligne à base de platine (soit carboplatine-paclitaxel soit carboplatine-caelix)" | Exclusion criteria with organ-function contraindication framing | IC
- **ESSAI-D8**: ESSAI/cls | 9 | negation_speculation | "Ne pas prendre part à un autre projet de recherche sans l'accord de votre médecin, ceci pour vous protéger de tout accident possible pouvant résulter par exemple d'incompatibilités possibles ou d'autres dangers" | Negation in patient safety instruction context | IC
- **ESSAI-D10**: ESSAI/cls | 3 | neutral | "Essai clinique d'immunothérapie évaluant l'association du galunisertib (un facteur de croissance transformant β), avec l'anticorps anti-PD-L1 durvalumab (MEDI4736), dans le cancer du pancréas métastatique" | Trial objective framing — not SmPC regulatory prose | IO
- **ESSAI-D11**: ESSAI/cls | 20 | speculation | "Dans la recherche proposée, nous allons évaluer si l'utilisation de l'oxygène à haut débit humidifié chez les patients immunodéprimés avec un problème respiratoire nécessitant de l'oxygène admis en réanimation est supérieure à la prise en charge habituelle" | Research hypothesis language — absent from SmPC register | IO
- **ESSAI-D12**: ESSAI/ner_spec | 10 | speculation span | "le traitement par un inhibiteur de PARP, le talazoparib, peut être plus efficace et mieux toléré de la chimiothérapie de référence" | Speculation NER marks hedging scope, not INN entity | OO
- **ESSAI-D13**: ESSAI/ner_neg | 11 | negation span | "en l'absence d'atteinte ganglionnaire chez les femmes ménopausées" | Negation NER marks clinical condition under negation, not regulatory entity | OO
- **ESSAI-D14**: ESSAI/ner_neg | 9 | O | "L'acétate d'abiratérone ou l'enzalutamide sont des traitements assez récents et ainsi appelés «hormonothérapies de nouvelle génération»" | Informal INN usage without ATC code mapping | IC
- **ESSAI-D15**: ESSAI/ner_spec | 12 | O | "Les patients seront traités par nivolumab IV en combinaison avec de l'ipilimumab en IT ou en IV" | Route abbreviations in trial shorthand vs. SmPC-standard format | IC
- **ESSAI-D16**: ESSAI/cls | 28 | speculation | "Les agents alkylants sont des chimiothérapies exposant à un risque de troubles de la fertilité avec insuffisance ovarienne précoce chez les femmes" | Population/adverse-event qualifier captured only as speculation, not regulatory entity | OO, OC
- **ESSAI-D17**: ESSAI/cls | 8 | speculation | "Cette étude est destinée à évaluer le nouveau médicament «cobimetinib» chez l'enfant et adolescent porteur d'une tumeur solide en rechute et/ou réfractaire au précédent traitement" | Pediatric population qualifier subsumed in speculation label | OO
- **ESSAI-D18**: ESSAI/YAML | Q43 | — | "ESSAI contains 7,247 clinical trial protocols annotated in 41 POS tags using TreeTagger" | Machine-generated POS; no human regulatory expert annotation documented | OC
- **ESSAI-D19**: ESSAI/cls | 23 | neutral | "Les gliomes de bas grade (grade I ou II) sont les tumeurs cérébrales les plus fréquemment observées chez les enfants, adolescents et jeunes adultes" | Oncology-only scope; non-oncology therapeutic areas absent | IC
- **ESSAI-D20**: ESSAI/ner_spec | 13 | O | "Les effets secondaires attendus sont mineurs de type ballonnement abdominal, diarrhées, spames digestifs le plus souvent et rarement des cailloux dans les voies biliaires" | Adverse effect listing in oncology trial — not SmPC adverse effects section | IC
