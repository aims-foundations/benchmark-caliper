## Dataset Analysis Report

**Benchmark:** DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Language
**Datasets analyzed:** 11 datasets — QUAERO, FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC, E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI
**Analysis date:** 2025-07-14

---

### Per-Dataset Fit Assessment

#### DrBenchmark/QUAERO

- **Task:** Named Entity Recognition (NER), 10 UMLS Semantic Group classes, two configurations: EMEA drug leaflets (`emea`) and MEDLINE titles (`medline`)
- **Deployment fit:** **Partial** — The `emea` configuration is the single strongest content match in the entire benchmark for this deployment: it draws directly from EMA patient information leaflets and contains authentic regulatory phrasing covering posology, contraindications, adverse events, and excipient lists (QUAERO-D1, QUAERO-D2, QUAERO-D3, QUAERO-D5, QUAERO-D6, QUAERO-D9). However, the UMLS Semantic Group label space collapses INNs, excipients, brand names, and endogenous chemicals under a single CHEM tag (QUAERO-D13, QUAERO-D14), the `medline` configuration contributes substantially off-domain noise (QUAERO-D16, QUAERO-D17, QUAERO-D18), nested entity simplification discards 6.06% of EMEA annotations (QUAERO-D15, QUAERO-D19), and the dataset provides no STS capability.
- **Key strengths:**
  - EMEA drug leaflet content directly represents the primary deployment genre (patient information leaflets, safety warnings, posology)
  - Contraindication, pregnancy/lactation, pediatric restriction phrasing present (QUAERO-D6, QUAERO-D7, QUAERO-D8)
  - Specific dose figures, administration routes, and titration schedules annotated (QUAERO-D9, QUAERO-D10)
  - Incidental tropical disease reference in MEDLINE (QUAERO-D11)
- **Key concerns:**
  - MAJOR [OO]: CHEM label conflates INN, brand name, excipient, and endogenous chemical — no regulatory sub-distinction (QUAERO-D13, QUAERO-D14)
  - MAJOR [OO]: No STS task; regulatory equivalence checking cannot be evaluated
  - MAJOR [IC]: MEDLINE configuration is substantially off-domain (historical, biographical, philosophical titles — QUAERO-D16, QUAERO-D17, QUAERO-D18)
  - MAJOR [OO, OC]: Nested entity simplification loses annotation precision; EMEA authorization codes outside label space (QUAERO-D15)
  - MINOR [IC]: Non-French text fragments and document-splitting artifacts in emea config (QUAERO-D19, QUAERO-D20, QUAERO-D21)
  - MINOR [OC]: No regulatory affairs annotators; UMLS Semantic Group norms may diverge from EMA SmPC annotation guidelines

---

#### DrBenchmark/FrenchMedMCQA

- **Task:** Multiple-Choice Question Answering (MCQA), two subtasks: correct answer identification and answer count prediction; sourced from French pharmacy specialization diploma exams
- **Deployment fit:** **Weak** — Task type (MCQA) is fundamentally misaligned with the deployment's NER and STS requirements. The pharmaceutical vocabulary present in questions (drug names, contraindications, SmPC references) is relevant content but is unannotated as entities and unavailable for NER or STS evaluation. A substantial share of questions covers basic biomedical science irrelevant to compliance workflows.
- **Key strengths:**
  - French pharmaceutical vocabulary present: drug contraindications with brand names (FRENCHMEDMCQA-D2), SmPC/RCP reference (FRENCHMEDMCQA-D3), pregnancy-period antibiotic contraindications (FRENCHMEDMCQA-D10)
  - Formal written French register consistent with regulatory document language (FRENCHMEDMCQA-D6)
  - Drug-specific pharmacokinetic and safety content (FRENCHMEDMCQA-D8, FRENCHMEDMCQA-D9)
- **Key concerns:**
  - CRITICAL [IO, OO, OF]: Task type (MCQA) incompatible with NER and STS evaluation required by deployment (FRENCHMEDMCQA-D11)
  - CRITICAL [IO, IC]: All inputs from pharmacy education exams, not from SmPCs, PILs, or CTD modules (FRENCHMEDMCQA-D12, FRENCHMEDMCQA-D13)
  - MAJOR [OO, IC]: No entity-level annotation; drug names present but unannotated (FRENCHMEDMCQA-D14, FRENCHMEDMCQA-D15)
  - MAJOR [IC]: Majority of questions cover basic science (nuclear physics, spectroscopy, osmolarity) unrelated to compliance workflows (FRENCHMEDMCQA-D17, FRENCHMEDMCQA-D18, FRENCHMEDMCQA-D19)
  - MAJOR [OC]: Exam answer keys as ground truth; may not reflect current ANSM/EMA normative standards (FRENCHMEDMCQA-D20)
  - MINOR [IC]: No French overseas territory or tropical pathology content (FRENCHMEDMCQA-D21)

---

#### DrBenchmark/DEFT2020

- **Task:** Semantic Textual Similarity (STS), two subtasks: scored sentence-pair similarity (0–5 scale, 5 annotators) and 3-way retrieval; drawn from DEFT 2020 challenge including drug leaflets, clinical texts, and encyclopedic content
- **Deployment fit:** **Partial** — This is the benchmark's primary STS dataset and the closest approximation to the deployment's compliance-checking function. A meaningful fraction of sentence pairs originate from drug leaflets and include authentic safety warning, contraindication, and posology phrasing (DEFT2020-D1, DEFT2020-D2, DEFT2020-D3, DEFT2020-D5). The multi-annotator score field enables uncertainty quantification (DEFT2020-D12, DEFT2020-D13). However, a large proportion of pairs are encyclopedic/off-domain (DEFT2020-D14, DEFT2020-D15, DEFT2020-D16, DEFT2020-D17), and the 0–5 scale is not calibrated for regulatory-equivalence judgment (DEFT2020-D18, DEFT2020-D19).
- **Key strengths:**
  - Authentic drug leaflet contraindication and safety warning sentence pairs (DEFT2020-D1, DEFT2020-D2, DEFT2020-D3, DEFT2020-D6)
  - Retained individual annotator scores enabling uncertainty/calibration analysis (DEFT2020-D12, DEFT2020-D13)
  - Pharmacovigilance-adjacent language present (DEFT2020-D11)
  - Pairs that illustrate legally significant paraphrase shifts (DEFT2020-D5: sublingual route addition)
- **Key concerns:**
  - CRITICAL [IO, IC]: ~30–40% of sentence pairs are entirely off-domain (railway infrastructure, biography, beekeeping, video games — DEFT2020-D14, DEFT2020-D15, DEFT2020-D16, DEFT2020-D17)
  - CRITICAL [OO, OC]: 0–5 scale treats precautionary qualifiers and dose-threshold differences as high-similarity (DEFT2020-D18, DEFT2020-D2); not calibrated for regulatory-equivalence judgment
  - MAJOR [IO, IC]: No SmPC or CTD module text; drug-labeling content resembles patient leaflets, not formal regulatory sections (DEFT2020-D22)
  - MAJOR [OC]: Annotator divergence on drug-label pairs suggests heterogeneous interpretive standards; no regulatory expertise documented (DEFT2020-D23)
  - MINOR [IC]: No French overseas territory or tropical disease content
  - MINOR [OF]: License not specified in HF metadata

---

#### DrBenchmark/MORFITT

- **Task:** Multi-label medical specialty classification of biomedical abstracts (12 labels: microbiology, pharmacology, virology, etc.)
- **Deployment fit:** **Weak** — The task (specialty routing of research abstracts) is entirely misaligned with the deployment's NER and STS requirements. The pharmacology label class partially overlaps in subject matter, and one abstract (MORFITT-D17) incidentally covers chikungunya in the Indian Ocean context, relevant to overseas territory priorities. However, regulatory document genres are entirely absent, and veterinary, Canadian, and non-French content dilutes relevance.
- **Key strengths:**
  - One abstract directly covers drug formulation stability (MORFITT-D19)
  - Chikungunya epidemic in Indian Ocean region present (MORFITT-D17) — incidental tropical disease coverage
  - Multi-label one-hot encoding compatible with deployment's multi-candidate output design (MORFITT-D4, MORFITT-D21)
  - Formal French biomedical register consistent with deployment (MORFITT-D1)
- **Key concerns:**
  - CRITICAL [IO, OO]: Task type (specialty classification) incompatible with NER or STS evaluation
  - CRITICAL [IO, IC]: No SmPCs, PILs, CTD modules, or ANSM regulatory content
  - CRITICAL [IO, OC]: 12 specialty labels (domain routing) do not map to regulatory entity vocabulary
  - MAJOR [IC, OC]: Substantial non-French geographic content (Canada, Jordan, Saudi Arabia, Egypt — MORFITT-D8, MORFITT-D13, MORFITT-D20, MORFITT-D31)
  - MAJOR [IC, IO]: Veterinary content irrelevant to human pharmaceutical regulatory compliance (MORFITT-D9, MORFITT-D26, MORFITT-D29)

---

#### DrBenchmark/CLISTER

- **Task:** Semantic Textual Similarity (STS) of French clinical case sentence pairs (1,000 pairs, 0–5 scale, multi-annotator averaged)
- **Deployment fit:** **Partial** — CLISTER is the benchmark's cleanest STS dataset and the closest to the deployment's compliance-checking function in terms of task structure. Multi-annotator averaged scores span the full 0–5 range and demonstrate sensitivity to semantic distinctions (CLISTER-D3, CLISTER-D13, CLISTER-D14). Some drug and dosage content is present (CLISTER-D6, CLISTER-D7, CLISTER-D8, CLISTER-D9). However, all content derives from clinical case reports, not regulatory documents; the scoring rubric assigns high similarity to numerically distinct clinical values in ways that would be inappropriate for regulatory compliance (CLISTER-D17, CLISTER-D18); and the dataset is saturated with repetitive clinical boilerplate (CLISTER-D21).
- **Key strengths:**
  - French clinical language consistent with deployment register (CLISTER-D1, CLISTER-D2)
  - Full 0–5 score range with fractional labels for sensitivity analysis (CLISTER-D3, CLISTER-D4)
  - Drug name and dosing pairs present (CLISTER-D6, CLISTER-D7, CLISTER-D9)
  - Synonym/temporal equivalence correctly handled at score=5 (CLISTER-D10, CLISTER-D11, CLISTER-D12)
  - Mid-range annotation captures clinically meaningful content differences (CLISTER-D13, CLISTER-D14)
- **Key concerns:**
  - CRITICAL [IO, IC]: Exclusively clinical case narratives; no SmPCs, PILs, or regulatory document genres (CLISTER-D15, CLISTER-D16)
  - CRITICAL [OO]: Scoring rubric assigns 4.0 to quantitatively different values (2-year vs. 4.5-year follow-up, 10 vs. 20 mmol/l) — inappropriate for regulatory compliance dose/threshold equivalence (CLISTER-D17, CLISTER-D18)
  - MAJOR [OC]: Clinical annotators, not regulatory affairs specialists; drug dosage comparisons scored by clinical intuition rather than regulatory standards (CLISTER-D19, CLISTER-D20)
  - MAJOR [IC]: High repetition of clinical boilerplate saturating score=5 cluster reduces lexical diversity (CLISTER-D21)
  - MINOR [IC]: Fragmented/truncated items, tabular data, and OCR artifacts present (CLISTER-D22, CLISTER-D23, CLISTER-D24)
  - MINOR [IC]: No French overseas territory or tropical pathology content

---

#### DrBenchmark/MANTRAGSC

- **Task:** Named Entity Recognition (NER), multilingual, French configurations: `fr_emea` (EMEA drug leaflets), `fr_medline` (MEDLINE titles), `fr_patents` (pharmaceutical patents); 10-class UMLS Semantic Group scheme
- **Deployment fit:** **Partial** — The `fr_emea` and `fr_patents` configurations provide authentic regulatory and pharmaceutical text: posology statements with dose thresholds (MANTRAGSC-D2), adverse reaction language from drug labels (MANTRAGSC-D3, MANTRAGSC-D4), and pharmaceutical patent claim text (MANTRAGSC-D5). These represent two of the deployment's priority document genres. However, the French subsets are very small (~100 examples each), the UMLS label scheme does not distinguish INN from excipient or drug class (MANTRAGSC-D11), and `fr_medline` is off-domain (MANTRAGSC-D8, MANTRAGSC-D9, MANTRAGSC-D10).
- **Key strengths:**
  - `fr_emea` contains authentic EMA drug leaflet text with posology, adverse event, and drug composition sentences (MANTRAGSC-D1, MANTRAGSC-D2, MANTRAGSC-D3, MANTRAGSC-D4)
  - `fr_patents` covers pharmaceutical patent claim language — a deployment-adjacent genre (MANTRAGSC-D5, MANTRAGSC-D7)
  - INN identification with salt form present (MANTRAGSC-D6)
  - Standard written French text, no modality or script mismatch
- **Key concerns:**
  - CRITICAL [OO]: UMLS Semantic Groups collapse INN, drug class, excipient, and chemical compound under CHEM — no regulatory sub-distinction (MANTRAGSC-D11, MANTRAGSC-D12)
  - CRITICAL [IC, IO]: `fr_medline` configuration is off-domain (traumatology, social medicine, public health titles — MANTRAGSC-D8, MANTRAGSC-D9, MANTRAGSC-D10)
  - MAJOR [IC]: French configurations are very small (~100 examples each); evaluation representativeness is limited
  - MAJOR [OC]: No regulatory affairs annotators; UMLS annotation norms diverge from EMA SmPC annotation guidelines
  - MINOR [IC]: Multilingual contamination risk from non-French configurations in HF dataset (MANTRAGSC-D13)
  - MINOR [IO, IF]: `fr_patents` uses distinct patent claim register, not directly transferable to patient leaflet language (MANTRAGSC-D14)

---

#### DrBenchmark/E3C

- **Task:** Named Entity Recognition (NER), multilingual clinical cases; French configurations: `French_clinical` (binary: O, CLINENTITY) and `French_temporal` (events, actors, body parts, temporal expressions, factuality markers)
- **Deployment fit:** **Weak** — The French configurations provide clean clinical prose in standard written French, and the temporal/factuality annotation layer is linguistically sophisticated. However, the CLINENTITY label is a single-class scheme capturing pathologies and symptoms, drug names appear in text but are tagged O (E3C-D2, E3C-D12), and the schema provides no regulatory entity types whatsoever. The majority of the dataset is non-French (8 of 10 configurations), and the French training data is small.
- **Key strengths:**
  - Standard written French clinical prose consistent with deployment text modality (E3C-D1, E3C-D3)
  - Temporal/factuality annotation layer provides multi-class structural richness (E3C-D4)
  - IOB2 evaluation protocol consistent with deployment NER infrastructure (E3C-D5)
- **Key concerns:**
  - CRITICAL [IC, IF]: 8 of 10 configurations are non-French (Basque, English, Italian, Spanish — E3C-D6, E3C-D7, E3C-D8); French subsets are small
  - CRITICAL [IO, IC]: All French examples are clinical case narratives; no regulatory document genres (E3C-D9, E3C-D10)
  - CRITICAL [OO, OC]: Drug names present in text but tagged O; schema has no substance, INN, posology, or contraindication entity type (E3C-D2, E3C-D11, E3C-D12)
  - MAJOR [OC]: Clinical NLP annotators; no regulatory affairs expertise; schema orthogonal to regulatory compliance needs (E3C-D13)
  - MAJOR [IC]: French training split is small (~1,400 examples); coarse two-class scheme limits fine-tuning utility (E3C-D14)
  - MAJOR [OO]: No STS component

---

#### DrBenchmark/PxCorpus

- **Task:** Intent classification (4 classes: medical_prescription, negate, none, replace) and NER over prescription entity types; derived from transcribed drug prescription spoken dialogues
- **Deployment fit:** **Partial (narrow)** — PxCorpus is the only dataset containing drug names with posology annotations (dose, form, frequency, duration, route — PXCORPUS-D1, PXCORPUS-D2, PXCORPUS-D3) and the only dataset with a correction/negation intent class directly analogous to compliance flagging (PXCORPUS-D8, PXCORPUS-D9). However, the input genre is spoken-language transcription containing disfluencies, code-switching, and artifacts (PXCORPUS-D12, PXCORPUS-D13, PXCORPUS-D14) radically different from formal regulatory documents, the intent schema does not map to regulatory compliance categories (PXCORPUS-D18), and severe class imbalance limits evaluation of the correction classes (PXCORPUS-D21).
- **Key strengths:**
  - Posology entity coverage: drug names, doses, forms, frequencies, durations, routes across diverse patterns (PXCORPUS-D1 through PXCORPUS-D7)
  - `replace` and `negate` intent classes capture dosage correction and negation speech acts relevant to inconsistency detection (PXCORPUS-D8, PXCORPUS-D9)
  - `none` class includes form inconsistency meta-commentary directly relevant to compliance concepts (PXCORPUS-D10, PXCORPUS-D11)
- **Key concerns:**
  - CRITICAL [IO, IC]: Spoken-language transcription genre with disfluencies, code-switching, and artifacts incompatible with regulatory document processing (PXCORPUS-D12, PXCORPUS-D13, PXCORPUS-D14, PXCORPUS-D15, PXCORPUS-D16)
  - MAJOR [OO]: Intent classes model spoken dialogue speech acts, not regulatory compliance verdicts; no STS component (PXCORPUS-D18)
  - MAJOR [OO, IC]: NER scheme does not include INN/brand distinction, ATC codes, excipient nomenclature, or contraindication qualifiers; some NER tag indices undecoded (PXCORPUS-D19, PXCORPUS-D20)
  - MAJOR [OC, OF]: Severe class imbalance — `replace` class has only 3 examples in 500-example buffer (PXCORPUS-D21)
  - MAJOR [OC]: Annotation norms reflect spoken-language understanding, not regulatory documentation standards (PXCORPUS-D22, PXCORPUS-D23)

---

#### DrBenchmark/DiaMED

- **Task:** Multi-class classification at ICD-10 chapter level (22 classes); 739 French clinical cases from the Pan African Medical Journal
- **Deployment fit:** **Weak** — DiaMED is the only dataset purpose-built for DrBenchmark but is doubly misaligned with the deployment: its task (ICD-10 chapter classification) does not evaluate NER or STS, and its content (clinical cases from Sub-Saharan Africa, Morocco, Niger, Burkina Faso) is geographically mismatched with both metropolitan France (primary) and French overseas territories (secondary). Some drug vocabulary is present in case narratives (DIAMED-D1, DIAMED-D8, DIAMED-D12) but unannotated. Inter-annotator agreement is documented, which is a quality signal strength.
- **Key strengths:**
  - French-language clinical text with ICD-10 chapter-level annotation and documented IAA (Cohen's Kappa, Gwet's AC1)
  - Broad ICD-10 chapter coverage across all 22 classes
  - Drug and treatment mentions present in clinical cases (DIAMED-D8, DIAMED-D12)
- **Key concerns:**
  - CRITICAL [IC, IO]: All cases from Sub-Saharan Africa and North Africa, not metropolitan France or French overseas territories (DIAMED-D3, DIAMED-D9, DIAMED-D11)
  - CRITICAL [IO, OO]: ICD-10 chapter classification does not evaluate NER or STS capability
  - CRITICAL [OO, OC]: 22 ICD-10 chapter labels reflect clinical disease coding, not regulatory entity vocabulary or safety compliance axes (DIAMED-D4)
  - MAJOR [IO, IC]: All inputs are clinical case narratives; no regulatory document genres
  - MAJOR [IC, OC]: Sub-Saharan African disease presentations (HIV/AIDS at CD4=27, Burkina Faso hospital settings) introduce epidemiological patterns mismatched with metropolitan or overseas French regulatory context (DIAMED-D1)
  - MINOR [OO]: Severe class imbalance across ICD-10 chapters

---

#### DrBenchmark/DEFT2021

- **Task:** Two configurations — `cls` (multi-label classification over 23 MeSH Chapter C axes) and `ner` (fine-grained NER with 13 entity types including SUBSTANCE, DOSAGE, MODE, FREQUENCY); 275 clinical cases, manually annotated
- **Deployment fit:** **Partial** — DEFT2021 provides the benchmark's richest NER scheme for drug-adjacent entities (SUBSTANCE, DOSAGE, MODE, FREQUENCY annotated in clinical cases — DEFT2021-D3, DEFT2021-D5, DEFT2021-D6). Drug interaction and pharmacovigilance reasoning is present in some cases (DEFT2021-D1, DEFT2021-D2). However, the entity scheme does not include INN/brand distinction, ATC codes, or excipient categories (DEFT2021-D10); all content is from clinical cases, not regulatory documents; and no STS task is present.
- **Key strengths:**
  - 13-type NER scheme includes SUBSTANCE, DOSAGE, MODE, FREQUENCY — partially overlapping with posology entity types relevant to deployment (DEFT2021-D3, DEFT2021-D5, DEFT2021-D6)
  - Manually annotated (gold standard) for both NER and classification
  - Drug interaction and benefit-risk reasoning cases present (DEFT2021-D1, DEFT2021-D2)
  - Multi-label classification output compatible with deployment's multi-candidate design (DEFT2021-D4)
- **Key concerns:**
  - CRITICAL [OO]: No STS task; compliance-equivalence scoring not evaluable
  - CRITICAL [IO, IC]: All inputs are clinical case reports; no regulatory document genres (DEFT2021-D8, DEFT2021-D9)
  - CRITICAL [OO, IC]: NER SUBSTANCE tag conflates INN, excipient, and chemical entity without regulatory sub-distinction (DEFT2021-D10); MeSH Chapter C axes reflect disease classification, not regulatory safety signal categories (DEFT2021-D14)
  - MAJOR [OC]: Clinical/NLP annotators; no regulatory affairs expertise (DEFT2021-D12, DEFT2021-D13)
  - MINOR [IC]: Some Canadian pharmacy and non-metropolitan-France clinical content present (DEFT2021-D15, DEFT2021-D16)

---

#### DrBenchmark/CAS

- **Task:** Four configurations — `cls` (negation/speculation sentence classification, 4 classes), `ner_neg` (negation scope NER), `ner_spec` (speculation scope NER), `pos` (POS tagging, 31 classes); silver-standard automatic annotation via Tagex 3 with 98% precision validation
- **Deployment fit:** **Weak** — CAS provides negation and speculation detection in clinical French prose, which has marginal relevance to safety claim checking. Some clinical cases contain drug names (CAS-D6, CAS-D7). However, the task labels (negation/speculation/neutral) are categorically misaligned with regulatory entity NER, drug names are untagged in NER configs (CAS-D15), POS labels are silver-standard, class imbalance is severe (CAS-D16), and all content is clinical case narrative.
- **Key strengths:**
  - French clinical prose register consistent with deployment (CAS-D1, CAS-D2)
  - Negation and speculation detection has marginal relevance to flagging uncertain safety claims (CAS-D3, CAS-D4, CAS-D5)
  - Span-level NER for negation/speculation scope (CAS-D8, CAS-D9)
  - Drug names with dosing occasionally present (CAS-D6)
- **Key concerns:**
  - CRITICAL [IO]: All clinical case content; no regulatory document genres (CAS-D10, CAS-D11)
  - CRITICAL [OO]: Negation/speculation task labels entirely misaligned with regulatory entity NER requirements (CAS-D12, CAS-D13)
  - MAJOR [OC]: Silver-standard POS and NER annotation; 2% error floor in labels (CAS-D14)
  - MAJOR [IC]: Drug names present in text but untagged in NER configurations (CAS-D15)
  - MAJOR [OO, OF]: Extreme neutral-class dominance (74%) limits evaluation of safety-critical minority classes (CAS-D16)

---

#### DrBenchmark/ESSAI

- **Task:** Four configurations — `cls` (negation/speculation classification, 4 classes), `ner_neg` (negation scope NER), `ner_spec` (speculation scope NER), `pos` (POS tagging, 41 classes via TreeTagger); drawn from French clinical trial protocol summaries; silver-standard POS annotation
- **Deployment fit:** **Weak** — ESSAI provides formal French biomedical prose from clinical trial protocols and contains numerous pharmaceutical compound names (ESSAI-D1, ESSAI-D3, ESSAI-D4, ESSAI-D5). However, drug names appear only in classification/negation context and are never annotated as drug entities; the NER scope labels cover only negation/speculation spans (ESSAI-D10, ESSAI-D11); trial protocol investigational language is structurally distinct from approved regulatory document sections; POS labels are silver-standard (ESSAI-D12); and neutral class dominance (76.8%) limits evaluation utility.
- **Key strengths:**
  - Formal French biomedical prose consistent with deployment text modality (ESSAI-D1)
  - Drug names and posology expressions present in text (ESSAI-D2, ESSAI-D3, ESSAI-D5)
  - Negation of adverse effect claims has marginal relevance to safety monitoring (ESSAI-D6)
  - Lemmatization provided, supporting drug name normalization
- **Key concerns:**
  - CRITICAL [IO, IC]: Clinical trial protocol genre is structurally distinct from approved regulatory documents (SmPCs, PILs — ESSAI-D8, ESSAI-D9)
  - CRITICAL [OO, IC]: NER tags annotate only negation/speculation scope; drug names never labeled as drug entities (ESSAI-D10, ESSAI-D11)
  - MAJOR [OC, OF]: Silver-standard POS annotation via TreeTagger (ESSAI-D12)
  - MAJOR [OO, OC]: Extreme neutral class dominance (76.8%) limits diagnostic value (no datapoint citation — structural distribution finding)
  - MAJOR [OC]: Annotation norms reflect clinical NLP epistemic modeling, not regulatory legal standards (ESSAI-D13)

---

### Cross-Cutting Strengths

**1. French biomedical text register is consistent across all datasets** [IC, IF]
Every dataset provides standard written French biomedical prose: from clinical case narratives (CLISTER-D1, E3C-D1, CAS-D1, DEFT2021-D7, DIAMED-D1) to drug leaflets (QUAERO-D2, MANTRAGSC-D1) to pharmacy exam questions (FRENCHMEDMCQA-D6) to clinical trial protocols (ESSAI-D1). There are no script mismatches, no RTL concerns, and no cross-modality gaps (PxCorpus provides transcribed text, not audio). This uniformly supports the deployment's text-only, metropolitan-French infrastructure assumption.

**2. Drug and pharmaceutical vocabulary present across multiple datasets** [IC]
Several datasets collectively represent a meaningful range of pharmaceutical vocabulary: EMEA drug leaflet sentences with INNs, dosage forms, and excipient lists (QUAERO-D1, QUAERO-D2, MANTRAGSC-D1, MANTRAGSC-D2); contraindication and adverse event language (QUAERO-D5, QUAERO-D6, MANTRAGSC-D3); drug interaction and benefit-risk reasoning (DEFT2021-D1, DEFT2021-D2); posology expressions across diverse patterns (PXCORPUS-D1 through PXCORPUS-D7); and drug names in clinical context (DEFT2021-D6, CAS-D6, ESSAI-D3). This provides partial NER training signal for pharmaceutical entity detection, even if label granularity is insufficient.

**3. Multi-annotator label uncertainty is documented and partially recoverable** [OC, OF]
DEFT2020 retains all five individual annotator scores per pair (DEFT2020-D12, DEFT2020-D13), enabling downstream uncertainty quantification aligned with the deployment's human-in-the-loop design. CLISTER uses averaged multi-annotator scores with full 0–5 range coverage. DiaMED documents IAA via Cohen's Kappa and Gwet's AC1. These three datasets provide a measurable basis for confidence-score calibration, relevant to the deployment's borderline-case flagging design.

**4. Negation and speculation detection infrastructure present** [IO, OO]
CAS and ESSAI provide sentence-level classification and span-level NER for negation and speculation scope — an analytically useful capability for identifying when safety-relevant findings are negated or uncertain. This partially maps to a compliance-checking sub-task: detecting when a proposed labeling statement negates or qualifies a safety warning (CAS-D3, CAS-D4, CAS-D5, ESSAI-D6). While not calibrated to regulatory norms, this is an underrecognized partial alignment between benchmark and deployment.

**5. The benchmark is the first and most comprehensive French biomedical NLP evaluation framework available** [IO]
For the deployment's French-language context, DrBenchmark represents the most relevant existing benchmark. The absence of a purpose-built French regulatory NLP benchmark (confirmed by web search) means DrBenchmark's 20-task taxonomy — despite its gaps — constitutes the most informative available proxy for French biomedical model selection. This has practical relevance for model shortlisting decisions even where individual task-deployment alignment is imperfect.

---

### Cross-Cutting Weaknesses

#### CRITICAL [IO] — No regulatory document genre is the primary evaluation target in any dataset
Zero of the 11 datasets uses SmPCs, CTD modules, or ANSM submission formats as the primary evaluation genre. QUAERO (`emea`) and MANTRAGSC (`fr_emea`) source from EMA drug leaflets for NER, but neither is used for STS compliance-checking tasks. All other datasets draw from clinical case narratives, research abstracts, pharmacy exam questions, clinical trial protocols, or spoken-language transcriptions. This is the most consequential single gap between benchmark and deployment (confirmed by QUAERO-D16, DEFT2020-D22, CLISTER-D15, E3C-D9, DIAMED-D6, DEFT2021-D8, ESSAI-D8).

#### CRITICAL [OO] — STS scoring is not calibrated for regulatory equivalence anywhere in the benchmark
Both STS datasets (DEFT2020 and CLISTER) use general semantic proximity scales that assign high similarity to sentence pairs differing in legally significant ways: precautionary qualifier removal (DEFT2020-D2, DEFT2020-D18), route-of-administration addition (DEFT2020-D5), twofold numerical difference in clinical measurements (CLISTER-D17, CLISTER-D18), and temporal synonym equivalence (CLISTER-D12). The 0–5 scale provides no mechanism to signal that a dose threshold change or population qualifier modification constitutes a regulatory variation type. This gap is fully confirmed by web search findings documenting that even minor text changes in drug labeling require formal variation submissions (Type IA/IB/II), making sub-Likert-scale differences legally operative.

#### CRITICAL [OO, IC] — NER label spaces across all datasets fail to distinguish regulatory entity types
Across all NER datasets, the label schemes use clinical/research ontologies (UMLS Semantic Groups in QUAERO and MANTRAGSC; CLINENTITY in E3C; SUBSTANCE/DOSAGE in DEFT2021; negation/speculation scope in CAS and ESSAI) that do not capture the regulatory entity types the deployment requires. The CHEM label in QUAERO and MANTRAGSC conflates INN, excipient, brand name, and endogenous chemical (QUAERO-D13, QUAERO-D14, MANTRAGSC-D11). Drug names appear in text but are tagged O in E3C (E3C-D12) and CAS (CAS-D15). No dataset labels ATC codes, excipient names as distinct from active ingredients, or EMA posology template components (population, dose, route, frequency as separately typed fields). This is confirmed by web search establishing that no published crosswalk between DrBenchmark NER schemas and EMA/ANSM regulatory annotation guidelines exists.

#### CRITICAL [OC] — No annotation authority from regulatory affairs expertise across any dataset
Across all 11 datasets, annotators are clinical professionals, NLP researchers, pharmacy educators (exam keys), or spoken-language annotators. No regulatory affairs specialist, pharmacovigilance officer, EMA reviewer, ANSM officer, or pharmaceutical legal expert is identified in any annotation team. CAS and ESSAI POS labels are silver-standard (automatic + validation). Ground-truth labels throughout the benchmark reflect clinical and research annotation norms that may systematically diverge from regulatory-legal compliance standards. This is confirmed for every dataset reviewed (QUAERO-D19 [MINOR OC], DEFT2020-D23, CLISTER-D19, MANTRAGSC [MAJOR OC], E3C-D13, DIAMED-D4, DEFT2021-D12, CAS-D14, ESSAI-D12).

#### MAJOR [IO] — Task type misalignment: classification tasks dominate while NER and STS are underrepresented relative to deployment needs
The deployment requires NER and STS. Of the 11 datasets: MORFITT, DiaMED, and FrenchMedMCQA contribute only classification tasks entirely incompatible with NER or STS evaluation (FRENCHMEDMCQA-D11, MORFITT-D2, DIAMED [all examples]). CAS and ESSAI contribute negation/speculation-scope NER unrelated to regulatory entity NER. PxCorpus contributes intent classification and posology-scope NER from spoken transcription. Only QUAERO, MANTRAGSC, DEFT2021-ner, and E3C contribute token-level NER with partial pharmaceutical relevance; only DEFT2020 and CLISTER contribute STS. This distribution means the benchmark underweights the two highest-priority deployment task types.

#### MAJOR [IC] — Substantial off-domain content across multiple datasets
Off-domain or peripherally relevant content dilutes regulatory signal across several datasets: ~30–40% encyclopedic/general content in DEFT2020 (DEFT2020-D14, DEFT2020-D15, DEFT2020-D16, DEFT2020-D17); MEDLINE titles including historical, biographical, and philosophical content in QUAERO (QUAERO-D16, QUAERO-D17, QUAERO-D18); veterinary and non-French-population content in MORFITT (MORFITT-D9, MORFITT-D26, MORFITT-D29, MORFITT-D8); and Sub-Saharan African clinical cases in DiaMED (DIAMED-D9, DIAMED-D11).

#### MAJOR [IC] — No French overseas territory or tropical disease vocabulary in any dataset
The deployment identifies French overseas territories (Martinique, Guadeloupe, French Guiana, Réunion, Mayotte) as the highest secondary adaptation priority, with distinct tropical disease patterns (dengue, chikungunya, paludisme, Zika, leptospirose). No dataset systematically covers this vocabulary. QUAERO-D11 (drug-resistant malaria in France in a MEDLINE title) and MORFITT-D17 (Chikungunya epidemic in the Indian Ocean) provide incidental references, but neither is a deliberate coverage target. This gap is fully confirmed by web search.

#### MINOR [OC] — Silver-standard annotation in CAS and ESSAI POS tasks propagates label error
Automatic POS tagging via Tagex 3 (CAS) and TreeTagger (ESSAI) with only 98% precision validation means both POS corpora contain a systematic error floor. For deployment fine-tuning on safety-critical tasks, this label quality concern compounds annotation authority concerns (CAS-D14, ESSAI-D12).

---

### Content Coverage Summary

**Well-covered domains:** French biomedical clinical narrative (clinical cases, examination findings, diagnostic reasoning); French clinical trial protocol language; EMEA drug leaflet sentence-level text for NER in limited quantities; French pharmacy specialization knowledge (MCQA format only); drug and posology vocabulary in spoken prescription dialogues; epistemic modality (negation/speculation) in clinical and trial contexts.

**Partially covered domains:** EMA drug leaflet NER (QUAERO-emea, MANTRAGSC-fr_emea) — useful for entity detection but with label granularity gaps; STS over clinical and mixed-domain text pairs (DEFT2020, CLISTER) — structurally relevant but not calibrated for regulatory equivalence; pharmacological and pharmaceutical specialty content (DEFT2021, FrenchMedMCQA, MORFITT) — subject-matter overlap without task-level alignment.

**Gaps relative to deployment needs:**
- SmPC sections (Section 4.3 contraindications, 4.4 special warnings, 4.8 adverse reactions, 5.1 pharmacodynamics): **Not covered**
- Patient information leaflet compliance structure: **Covered incidentally** (QUAERO-emea, DEFT2020 drug pairs) but not as a compliance-checking task
- CTD module text: **Not covered**
- ANSM submission templates (Feuille de style, blue-box elements): **Not covered**
- Regulatory entity vocabulary (INNs distinguished from brand names, ATC codes, excipient nomenclature, MedDRA preferred terms): **Not covered** in any dataset's label space
- STS calibrated for regulatory variation type (IA/IB/II distinctions): **Not covered**
- Annotation by regulatory affairs or legal experts: **Not present** in any dataset
- French overseas territory content (tropical pathology, DOM-specific terminology): **Not covered** as a deliberate target
- Versioned document compliance (detecting unauthorized changes between SmPC versions): **Not covered**

---

### Limitations

1. **Sample-based analysis only:** Each per-dataset analysis was conducted on a sample of examples (typically 100–500 per dataset). Rare entity types, infrequent regulatory phrasings, or edge-case annotation norms may not be visible in the sampled data. QUAERO's full EMEA subset may contain proportionally more high-value regulatory text than the sample indicates.

2. **NER tag decoding incomplete for PxCorpus:** Several NER tag indices in PxCorpus (e.g., tags 46, 49) could not be decoded against a label list in the HF metadata, preventing full assessment of the NER ontology scope (PXCORPUS-D19, PXCORPUS-D20).

3. **DiaMED IAA numerical values not surfaced:** Specific Cohen's Kappa and Gwet's AC1 values from Table 4 of the benchmark paper were not retrievable from indexed web sources. The overall quality signal is positive but the magnitude of agreement is unknown without accessing the full PDF.

4. **DEFT2020 domain mix not precisely quantifiable:** The estimate of ~30–40% off-domain content in DEFT2020 is based on the sampled 74 task_1 examples; the full dataset proportion may differ.

5. **STS compliance calibration not assessable without regulatory ground truth:** Whether the benchmark's STS scoring would misclassify legally significant text changes at the relevant regulatory threshold (IA/IB/II variation types) cannot be determined from the benchmark alone — it would require a purpose-built regulatory equivalence test set with ground truth from regulatory affairs specialists.

6. **Multilingual contamination in MANTRAGSC:** The HF dataset contains 12 configurations; analysis confirmed German-language example presence (MANTRAGSC-D13). Users pulling from the full dataset without configuration-level filtering may inadvertently include non-French examples.

7. **License status unresolved for DEFT2020:** The HF metadata reports "license: not specified," which may create deployment barriers that cannot be resolved from public information alone.

---

### Cited Evidence

- **QUAERO-D1**: QUAERO/emea | 1 | CHEM/O | "Phosphate de sodium , monobasique , monohydraté Phosphate de sodium , dibasique , heptahydraté Chlorure de sodium Polysorbate 80 ( E433 ) Eau pour préparation injectable" | Excipient nomenclature list with E-numbers from drug leaflet | IC, OO
- **QUAERO-D2**: QUAERO/emea | 55 | CHEM/DEVI/PROC | "TYSABRI 300 mg solution à diluer pour perfusion natalizumab Chaque flacon de 15 ml de concentré contient 300 mg de natalizumab ( 20 mg / ml )" | Brand name, INN, dosage, form, concentration co-occurring in regulatory sentence | IC
- **QUAERO-D3**: QUAERO/emea | 51 | CHEM/O | "EMEA / H / C / 122 REFLUDAN ... Son principe actif est la lépirudine ." | EMEA authorization number, brand name, INN in drug leaflet header | IC
- **QUAERO-D4**: QUAERO/emea | 57 | CHEM | "La lépirudine bloque spécifiquement l' une des substances impliquées dans le processus de coagulation , la thrombine ." | INN and endogenous protein tagged CHEM; mechanism-of-action phrasing from SmPC Section 5 | IC, OO
- **QUAERO-D5**: QUAERO/emea | 6 | DISO/CHEM | "Des épisodes de troubles psychiatriques aigus , tels que hallucinations , réactions paranoïdes , hostilité , délire , psychose et réactions maniaques ont été rapportés chez des patients traités par le ziconotide ." | Safety warning listing adverse psychiatric events; drug name tagged CHEM | IC, OC
- **QUAERO-D6**: QUAERO/emea | 43 | CHEM/LIVB | "Par conséquent , Refludan ne doit pas être administré à la femme enceinte ou qui allaite ." | Standard contraindication phrasing for pregnancy/lactation in regulatory text | IC
- **QUAERO-D7**: QUAERO/emea | 23 | CHEM/LIVB | "Prialt ne doit pas être utilisé chez l' enfant ." | Pediatric contraindication standard phrasing | IC
- **QUAERO-D8**: QUAERO/emea | 64 | CHEM/DISO/ANAT | "N' utilisez jamais TYSABRI ... Si vous êtes allergique ( hydpersensible ) au natalizumab ou à l' un des autres composants contenus dans TYSABRI" | Allergy/hypersensitivity contraindication in patient-facing PIL language | IC
- **QUAERO-D9**: QUAERO/emea | 32 | CHEM/PROC | "la dose maximale prévue de ziconotide administré par voie intrarachidienne était de 912 µg / jour après une augmentation posologique sur 7 jours ." | Specific dose, route, titration schedule — core posology regulatory text | IC
- **QUAERO-D10**: QUAERO/emea | 11 | CHEM/PROC/DISO | "La dose peut être augmentée par intervalles de 1 à 2 jours , voire plus , pour obtenir le meilleur équilibre entre le soulagement de la douleur et les effets indésirables éventuels ." | Titration instruction balancing efficacy and adverse events | IC
- **QUAERO-D11**: QUAERO/medline | 98 | DISO/GEOG | "Le paludisme chimiorésistant en France ." | Drug-resistant malaria in France; incidental tropical disease relevance | IC
- **QUAERO-D12**: QUAERO/medline | 132 | PROC/CHEM | "Adaptation posologique des traitements par aminoglycosides ." | Posology adjustment term; drug class (aminoglycosides) tagged CHEM | IC
- **QUAERO-D13**: QUAERO/emea | 50 | CHEM/O | "Refludan 50 mg en poudre pour solution injectable ... Lepirudine Les autres composants sont le mannitol ( E 421 ) et l' hydroxyde de sodium" | Brand name, INN, excipients all share CHEM label — regulatory distinction collapsed | OO
- **QUAERO-D14**: QUAERO/emea | 1 | CHEM/O | "Phosphate de sodium , monobasique ... Polysorbate 80 ( E433 ) ... Eau pour préparation injectable" | Excipients tagged identically to active ingredients under CHEM | OO
- **QUAERO-D15**: QUAERO/emea | 36 | CHEM/PHYS | "EMEA / H / C / 122 Recommandations standard Comme la lépirudine est excrétée et métabolisée en quasi-totalité par le rein" | EMEA authorization code untagged; regulatory administrative entity outside label space | OO, OC
- **QUAERO-D16**: QUAERO/medline | 16 | O | "L' apport des inventaires a la connaissance de la demographie parisienne ancienne : le regne de Francois Ier" | Historical demography article title; entirely off-domain, all O tags | IC, IO
- **QUAERO-D17**: QUAERO/medline | 78 | O | "De la médecine factuelle ( evidence-based medicine ) au ' libre arbitre '." | Philosophical/methodological title; no biomedical entity, all O | IC
- **QUAERO-D18**: QUAERO/medline | 61 | O | "LÉON GRIMBERT 1860 - 1931 ." | Biographical citation; zero regulatory relevance, all O tags | IC
- **QUAERO-D19**: QUAERO/emea | 4 | CHEM/PROC/PHYS | "Aucune étude clinique spécifique sur les interactions médicamenteuses n Toutefois , en raison des faibles concentrations plasmatiques du ziconotide" | Sentence truncated at "n" — document-splitting artifact affecting annotation integrity | OC
- **QUAERO-D20**: QUAERO/emea | 15 | O | "Č eská republika Biogen Idec ( Czech Republic ) s ." | Czech-language text fragment in EMEA distributor section; noise for French-only system | IC
- **QUAERO-D21**: QUAERO/emea | 41 | O | "o ." | Single-character artifact from document splitting | IC
- **FRENCHMEDMCQA-D1**: FrenchMedMCQA | 6 | simple | "Parmi les substances suivantes, une seule ne traverse pas la barrière placentaire. Laquelle? Dicoumarine / Héparine / Tétracycline..." | Drug placental crossing pharmacokinetics question | IC, IO
- **FRENCHMEDMCQA-D2**: FrenchMedMCQA | 70 | multiple | "Les anti-vitamines K (AVK) sont formellement contre-indiquées avec : Le miconazole (DAKTARIN®) / Les salicylés à fortes doses..." | Drug contraindications with brand names, relevant to labeling | IC
- **FRENCHMEDMCQA-D3**: FrenchMedMCQA | 105 | simple | "Le mésusage est défini comme : Une utilisation de médicament non conforme aux recommandations du résumé des caractéristiques du produit" | References SmPC (résumé des caractéristiques du produit) concept | IC, IO
- **FRENCHMEDMCQA-D4**: FrenchMedMCQA | 50 | multiple | "Parmi les verres suivants, indiquez ceux qui peuvent être utilisés comme conditionnement réutilisable des préparations pour usage parentéral" | Pharmaceutical packaging for parenteral preparations | IC
- **FRENCHMEDMCQA-D5**: FrenchMedMCQA | 100 | multiple | "Parmi les formes solides orales suivantes, indiquer celle(s) qui libère(nt) le principe actif de façon continue : Matrice hydrophile / Comprimé à enrobage par film insoluble..." | Dosage form terminology relevant to regulatory submissions | IC
- **FRENCHMEDMCQA-D6**: FrenchMedMCQA | 23 | multiple | "En électrophorèse capillaire haute performance, le sens de migration de l'analyse dépend : De la nature de la charge de l'analyte / Du flux d'électroendosmose..." | Formal technical French, matching regulatory document register | IF
- **FRENCHMEDMCQA-D7**: FrenchMedMCQA | 44 | multiple | "Parmi les propositions concernant le cotrimoxazole, quelle(s) est (sont) celle(s) qui est (sont) exacte(s)? ... Le triméthoprime est un inhibiteur de la dihydrofolate synthétase..." | Multi-answer discrimination over drug properties | IO, OO
- **FRENCHMEDMCQA-D8**: FrenchMedMCQA | 48 | multiple | "La distribution tissulaire des médicaments... Détermine le volume apparent de distribution / Est influencée par la liaison du médicament aux protéines plasmatiques..." | Drug distribution pharmacokinetics | IC
- **FRENCHMEDMCQA-D9**: FrenchMedMCQA | 104 | multiple | "Une intoxication aiguë par les opiacés présente généralement les manifestations cliniques suivantes: Dépression du système nerveux central / Dépression respiratoire / Myosis..." | Drug toxicology and adverse effects | IC
- **FRENCHMEDMCQA-D10**: FrenchMedMCQA | 34 | multiple | "Cocher le ou les antibiotique(s) dont l'utilisation est autorisée en fin de grossesse : Ampicilline / Cotrimoxazole / Tétracyclines / Erythromycine / Péfloxacine..." | Pregnancy contraindication for antibiotics | IC
- **FRENCHMEDMCQA-D11**: FrenchMedMCQA | 1 | simple | "Au cours de la leucémie lymphoïde chronique, le myélogramme montre: Une population de lymphocytes>30%..." | MCQA format; no NER labels or STS scores present | IO, OO, OF
- **FRENCHMEDMCQA-D12**: FrenchMedMCQA | 61 | simple | "La certification des établissements de santé: Ne concerne que les établissements de santé publics... Concerne tous les établissements de santé" | Healthcare administration, not from regulatory submission documents | IO, IC
- **FRENCHMEDMCQA-D13**: FrenchMedMCQA | 43 | multiple | "L'économie médicale est une économie : De service de santé / Régie par la loi de l'offre et de la demande..." | Health economics exam question, absent from regulatory workflows | IO, IC
- **FRENCHMEDMCQA-D14**: FrenchMedMCQA | 72 | multiple | "Parmi les propositions suivantes concernant la ceftriaxone (ROCEPHINE®)..." | Drug INN and brand name appear but are unannotated as NER entities | OO, IC
- **FRENCHMEDMCQA-D15**: FrenchMedMCQA | 112 | multiple | "Parmi les propositions suivantes concernant le ganciclovir (CYMEVAN®)..." | Drug name appears without NER label | OO, IC
- **FRENCHMEDMCQA-D16**: FrenchMedMCQA | 8 | multiple | "La trinitrine: Est le trinitrate d'isosorbide / Est un médicament anti-angoreux..." | Binary correct/incorrect output, no similarity score | OO, OF
- **FRENCHMEDMCQA-D17**: FrenchMedMCQA | 10 | multiple | "Cocher la (les) proposition(s) exacte(s) concernant l'osmolarité et l'osmolalité ? L'osmolarité est le nombre d'osmoles par litre de solution..." | Pure physicochemistry, irrelevant to labeling compliance | IC
- **FRENCHMEDMCQA-D18**: FrenchMedMCQA | 37 | simple | "Les 3 nucléides de l'hydrogène, H(A=1,Z=1), H(A=2,Z=1) et H(A=3,Z=1) sont: Des isotones / Des isotopes..." | Nuclear physics question, irrelevant to deployment | IC
- **FRENCHMEDMCQA-D19**: FrenchMedMCQA | 88 | multiple | "Un spectre de bandes : Peut être un spectre d'émission / Peut être un spectre d'absorption..." | Analytical spectroscopy, not a regulatory topic | IC
- **FRENCHMEDMCQA-D20**: FrenchMedMCQA | 94 | multiple | "La vaccination contre l'hépatite B: Est obligatoire pour tout le personnel de santé / Est recommandée pour tous les sujets à risque..." | Regulatory obligation status; exam ground truth may lag ANSM updates | OC
- **FRENCHMEDMCQA-D21**: FrenchMedMCQA | 67 | multiple | "Quelle est (sont) la (les) parasitose(s) qui présente(nt) un stade hépatique? Giardiase / Paludisme / Fasciolose..." | Paludisme appears as generic exam topic, not overseas-territory terminology | IC
- **DEFT2020-D1**: DEFT2020 task_1 | Ex. 18 | moy=4.6 | "En raison de la présence de lactose, ce médicament est contre-indiqué en cas de galactosémie congénitale, de syndrome de malabsorption du glucose et du galactose ou de déficit en lactase." | Drug leaflet contraindication for lactose-containing medication | IC
- **DEFT2020-D2**: DEFT2020 task_1 | Ex. 4 | moy=4.0 | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter pendant la durée du traitement." | Breastfeeding contraindication with precautionary qualifier; cible drops qualifier | OO
- **DEFT2020-D3**: DEFT2020 task_1 | Ex. 16 | moy=4.0 | "Ce produit peut provoquer un syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après la dernière prise de stupéfiant." | Opioid withdrawal warning with specific time threshold | IC
- **DEFT2020-D4**: DEFT2020 task_1 | Ex. 13 | moy=3.6 | "Chez les patients insuffisamment équilibrés par glimepiride arrow à la dose maximale, un traitement par l'insuline peut être associé si nécessaire." | Drug name + posology language from drug leaflet | IC
- **DEFT2020-D5**: DEFT2020 task_1 | Ex. 52 | moy=4.4 | "Comprimé rond, blanc, biconvexe, gravé 6 sur une face, une flèche étant gravée sur l'autre face." | Pharmaceutical form description; cible adds "sublingual" route — regulatory-significant difference | OO
- **DEFT2020-D6**: DEFT2020 task_1 | Ex. 70 | moy=4.3 | "Prévenir les patients que la voie sublinguale constitue la seule voie efficace et bien tolérée pour l'administration de ce produit." | Route-of-administration patient instruction from drug insert | IC
- **DEFT2020-D7**: DEFT2020 task_1 | Ex. 65 | moy=4.3 | "Ne pas utiliser chez les personnes présentant des difficultés de déglutition en raison du risque d'inhalation bronchique et de pneumopathie lipoïde." | Contraindication paraphrase; cible substitutes synonyms; rated high-similarity | OC
- **DEFT2020-D8**: DEFT2020 task_1 | Ex. 54 | moy=5.0 | "Troubles de l'hémostase à type de maladie de Willebrand (se traduisant par un allongement du TCA, du temps de saignement et une diminution des taux du complexe VIIIC/VWF)." | Identical sentences; upper-anchor calibration point | OO
- **DEFT2020-D9**: DEFT2020 task_2 | Ex. 22 | correct_cible=0 | "l'utilisation à forte dose d'huile de paraffine expose au risque de suintement anal et parfois d'irritation périanale" | Side-effect retrieval task using drug leaflet language | IC
- **DEFT2020-D10**: DEFT2020 task_1 | Ex. 26 | moy=3.4 | "Pour la comparaison entre blocs neuraxiaux et anesthésie générale, nous avons évalué la qualité des preuves comme très faible pour la mortalité..." | Cochrane-style evidence-graded clinical language | IF
- **DEFT2020-D11**: DEFT2020 task_1 | Ex. 38 | moy=4.2 | "Cependant, dans certaines études épidémiologiques cas-témoins, une augmentation de la survenue de fentes labio-palatines a été observée avec les benzodiazépines." | Pharmacovigilance-adjacent drug adverse event language | IC
- **DEFT2020-D12**: DEFT2020 task_1 | Ex. 46 | moy=2.2, vote=5.0 | scores=[5.0, 2.0, 0.0, 3.0, 1.0] | High inter-annotator disagreement; signals annotation uncertainty | OC
- **DEFT2020-D13**: DEFT2020 task_1 | Ex. 36 | moy=1.5 | scores=[2.0, 4.5, 0.0, 1.0, 0.0] | Extreme annotator divergence on low-similarity pair | OC
- **DEFT2020-D14**: DEFT2020 task_1 | Ex. 1 | moy=0.5 | "Entre Perpignan et Villefranche, il subsiste de très nombreux poteaux caténaires datant des premiers essais en 12 KV 16 2/3 Hz..." | Railway infrastructure; entirely off-domain | IO
- **DEFT2020-D15**: DEFT2020 task_1 | Ex. 3 | moy=2.1 | "Boris Fiodorovitch Godounov, en russe : Бори́с Фёдорович Годуно́в (v.1551–Moscou, 13 avril 1605), gouverne la Russie..." | Russian historical biography; off-domain | IO
- **DEFT2020-D16**: DEFT2020 task_1 | Ex. 6 | moy=0.4 | "Certains apiculteurs sélectionnent leurs reines afin de favoriser au mieux la production." | Beekeeping content; off-domain | IO
- **DEFT2020-D17**: DEFT2020 task_2 | Ex. 37 | correct_cible=0 | "Lancement du célèbre MMORPG : World of Warcraft." | Video game; entirely irrelevant to pharmaceutical domain | IO
- **DEFT2020-D18**: DEFT2020 task_1 | Ex. 4 | moy=4.0 | scores=[5.0, 2.0, 4.0, 4.0, 5.0] | Precautionary qualifier dropped in cible; rated 4.0 — legally significant difference not captured | OO
- **DEFT2020-D19**: DEFT2020 task_2 | Ex. 27 | correct_cible=2 | "ce médicament est contre-indiqué dans les cas suivants" vs. "n'utilisez jamais diclofenac eg 1%, gel dans les cas suivants" | General vs. brand-specific prohibition; general STS would conflate | OO
- **DEFT2020-D20**: DEFT2020 task_1 | Ex. 17 | moy=1.3 | "Les personnes infectées par le virus de l'immunodéficience humaine présentent un risque augmenté de développer une tuberculose (TB) active." | HIV/TB risk statement vs. treatment statement; scored 1.3 by general proximity | OO
- **DEFT2020-D21**: DEFT2020 task_1 | Ex. 13 | moy=3.6 | "glimepiride arrow" appears unannotated in "Chez les patients insuffisamment équilibrés par glimepiride arrow à la dose maximale..." | INN+brand and posology expression present as free text, no NER labels | IC
- **DEFT2020-D22**: DEFT2020 task_1 | Ex. 19 | moy=1.3 | "Ketoderm 2%, gel en récipient unidose peut donc être utilisé au cours de la grossesse." / "Qu'est-ce que ketoderm 2%, gel en récipient unidose et dans quel cas est-il utilisé." | Patient leaflet format, not SmPC Section 4.6 format | IO
- **DEFT2020-D23**: DEFT2020 task_1 | Ex. 4 | moy=4.0 | scores=[5.0, 2.0, 4.0, 4.0, 5.0] | Annotator scoring 2.0 may reflect regulatory-aware reading of precautionary qualifier; others score 4–5 | OC
- **MORFITT-D1**: MORFITT | 1 | 9 (surgery) | "La mise en place par cathétérisme d'une valve aortique (TAVI) destinée à traiter les malades ayant un rétrécissement aortique a été une des plus importantes innovations médicales de notre siècle." | TAVI cardiac innovation abstract — formal biomedical French register | IC, IF
- **MORFITT-D2**: MORFITT | 2 | 10 (pharmacology) | "Nous avons récemment publié les conclusions d'un nouveau test préclinique portant sur le dépistage analgésique rapide basé sur l'injection intraplantaire (i.pl.) d'une solution saline hypertonique à 10 % (HS) chez des souris femelles croisées (CD-1)." | Preclinical analgesic screening — pharmacology label but no NER/STS annotation | IO, OO
- **MORFITT-D4**: MORFITT | 4 | 8, 4 (veterinary, parasitology) | "Les échanges internationaux sont responsables de la résurgence de nombreuses maladies affectant le bétail." | Livestock disease / international trade — multi-label veterinary context | OO
- **MORFITT-D8**: MORFITT | 8 | 0 (microbiology) | "La région du Nord-Ouest de l'Ontario présente un taux élevé et documenté d'infections de la peau et des tissus mous causées par une souche de Staphylococcus aureus méthycillinorésistante d'origine communautaire (SARM-C)." | Canadian setting — geographic mismatch with metropolitan France regulatory context | IC, OC
- **MORFITT-D9**: MORFITT | 9 | 6, 0, 8 | "L'otite externe est une maladie multifactorielle fréquente chez le chien." | Canine ear disease — veterinary content irrelevant to human regulatory compliance | IC, IO
- **MORFITT-D13**: MORFITT | 13 | 3 | "En 2007 et 2008, 4 423 adultes de Calgary ont répondu à des entrevues au téléphone fixe portant sur l'activité physique" | Calgary-based physical activity study — non-French, non-pharmaceutical content | IC
- **MORFITT-D17**: MORFITT | 17 | 2 (virology) | "l'étude de l'épidémie de Chikungunya, un alphavirus transmis par Aedes aegypti et Aedes albopictus, survenue dans l'océan Indien en 2004-2007." | Chikungunya epidemic in Indian Ocean — relevant to overseas territory disease vocabulary | IC
- **MORFITT-D19**: MORFITT | 19 | 7 (pharmacology) | "Déterminer la stabilité physicochimique et microbiologique de suspensions de sulfadiazine (100 mg/mL) dans des formulations de sirop simple (A) et de sorbitol (B) préparées à partir de comprimés disponibles dans le commerce." | Drug formulation stability study — closest to pharmaceutical regulatory content; drug name present but unannotated as INN | IC, OC
- **MORFITT-D20**: MORFITT | 20 | 1 | "79 patients au total ont été recrutés à Amman (Jordanie) en 2015." | Jordanian oncology study — non-French geographic context | IC
- **MORFITT-D21**: MORFITT | 21 | 1, 3, 4 | "Bloquer le complément, notamment l'axe C5a-C5aR1, par des thérapies spécifiques représente un espoir thérapeutique dans les formes les plus sévères de la maladie." | COVID-19 complement pathway — three-label multi-label assignment | OO, OF
- **MORFITT-D26**: MORFITT | 26 | 6, 8, 5 | "74 % (34/46) des échantillons de tissus examinés provenant de chevaux contenaient des sarcocystes" | Equine parasitology study — veterinary, not human pharmaceutical | IC, IO
- **MORFITT-D29**: MORFITT | 29 | 8 (veterinary) | "La cyclosporine est de plus en plus utilisée en dermatologie des petits animaux." | Veterinary dermatology — cyclosporine in small animal context; not human regulatory use | IC
- **MORFITT-D31**: MORFITT | 31 | 11 | "des médecins internes en formation en Arabie saoudite" | Saudi Arabian medical intern study — non-metropolitan France context | IC
- **MORFITT-D34**: MORFITT | 34 | 9 (surgery) | "Bien que la vertébroplastie percutanée soit utilisée depuis presque 30 ans, ce n'est qu'en 2007 que le premier essai randomisé a été publié." | Vertebroplasty RCT review — clinical research abstract, not regulatory document | IO
- **CLISTER-D1**: CLISTER | 10 | 5.0 | "Une mastectomie était réalisée avec curage axillaire." / "Une mastectomie avec curage axillaire ont été réalisés." | Near-paraphrase in standard French clinical language | IC, IF
- **CLISTER-D2**: CLISTER | 11 | 4.0 | "La tomodensitométrie abdominale montre des images gazeuses dans la paroi abdominale postérieure, dans l'espace périnéphrétique droit, et dans le rein droit (Figure 1)." / "La tomodensitométrie abdominale avait montré des images gazeuses dans la paroi abdominale postérieure, dans l'espace péri néphrétique droit et au sein du parenchyme." | Clinical imaging paraphrase with minor lexical variation | IC
- **CLISTER-D3**: CLISTER | 5 | 2.75 | "Le reste de l'examen échographique ne trouvait aucune autre anomalie." / "Le reste de l'examen somatique était sans anomalie." | Mid-range score for partial clinical exam overlap | OO
- **CLISTER-D4**: CLISTER | 54 | 3.75 | "B.A., âgé de 20 ans a été admis au service d'accueil des urgences pour anurie associée à des lombalgies gauches." / "B.O., 35 ans a été admis au service d'urologie pour des lombalgies gauches avec une insuffisance rénale à 510 mol/l de créatininémie" | Fractional label for partial scenario overlap | OO
- **CLISTER-D5**: CLISTER | 149 | 0.5 | "Lithium 300 mg x x x x x x x x x x x x x x x x" / "300 mg IV aux 24 h x x x x x x x x x x x x x x x x" | Near-zero score for minimally similar dosing notations | OO
- **CLISTER-D6**: CLISTER | 41 | 2.0 | "Métoprolol 50 mg deux fois par jour;" / "Metformine 500 mg, 1 comprimé deux fois par jour" | Dosage format comparison between named drugs | IC
- **CLISTER-D7**: CLISTER | 98 | 2.0 | "Acide folinique 15 mg une fois par jour" / "Aspirine 80 mg, 1 comprimé une fois par jour" | Drug-dose formatting STS comparison | IC
- **CLISTER-D8**: CLISTER | 116 | 1.0 | "10 à 25 mg une fois par jour" / "Propranolol 40 mg, 1 comprimé deux fois par jour" | Posology expression comparison | IC
- **CLISTER-D9**: CLISTER | 78 | 4.0 | "2 Maintien : épidurale (bupivicaïne, fentanyl, épimorphine), rémifentanyl et sévoflurane" / "3 Épidurale : bupivicaïne, fentanyl et épimorphine" | Drug-list overlap in clinical anesthesia context | IC
- **CLISTER-D10**: CLISTER | 21 | 5.0 | "Les limites d'exérèse étaient saines." / "Les limites de l'exérèse étaient saines." | Near-identical sentence with article difference; score=5 | OC
- **CLISTER-D11**: CLISTER | 37 | 5.0 | "Les limites d'exérèse étaient saines." / "Les marges chirurgicales étaient saines." | Synonym-based paraphrase correctly scored maximum | OC
- **CLISTER-D12**: CLISTER | 112 | 5.0 | "L'évolution était favorable avec un recul d'une année." / "L'évolution était favorable avec un recul de 12 mois." | Temporal synonym ("un an" vs "12 mois") correctly assessed as equivalent | OC
- **CLISTER-D13**: CLISTER | 36 | 3.0 | "L'examen cytobactériologique des urines a permis d'isoler un colibacille." / "L'examen cytobactériologique des urines était négatif." | Same exam, opposite findings; mid-range score | OO
- **CLISTER-D14**: CLISTER | 90 | 3.0 | "Le taux de PSA était de 218 ng/ml (normale ≤ 4ng/ml)." / "Le dosage de PSA était de 13327 ng/ml (normal : < 4 ng/ml)." | Same test, dramatically different values; scored 3.0 | OO
- **CLISTER-D15**: CLISTER | 7 | 4.0 | "La patiente a été opérée et lors de l'exploration on découvrit qu'il s'agissait d'une tumeur de la veine cave inférieure sus-rénale." | Surgical case narrative, not regulatory document genre | IO, IC
- **CLISTER-D16**: CLISTER | 6 | 0.0 | "Dans le cadre de la Matériovigilance et d'éventuelles investigations supplémentaires concernant le matériel impliqué, ce cas a été notifié aux autorités sanitaires concernées." | Only incidental regulatory-adjacent language (materiovigilance) in entire sample | IO
- **CLISTER-D17**: CLISTER | 125 | 4.0 | "Le recul est de 2 ans." / "Le suivie est de 4 ans et demi." | Different follow-up durations scored 4.0; same rubric would conflate regulatory dose differences | OO
- **CLISTER-D18**: CLISTER | 188 | 4.0 | "L'AHG urinaire est à 10 mmol/l." / "L'AHG urinaire est à 20 mmol/l." | Twofold quantitative difference scored 4.0; regulatory dose doubling requires near-0 | OO
- **CLISTER-D19**: CLISTER | 146 | 0.0 | "Cette patiente, suivie en psychiatrie pour des troubles de l'humeur bipolaires, avait arrêté son traitement au lithium (Teralithe LP® 400 mg, deux comprimés par jour) un mois avant cette ingestion massive." | Named drug with dose in clinical case; regulatory annotator might weight differently | OC
- **CLISTER-D20**: CLISTER | 69 | 1.0 | "Hépatique (P) T1/2 = 96 h (P) –" / "Hépatique, rénal T1/2 = 15 – 40 jours" | Pharmacokinetic comparison; score reflects clinical rather than regulatory judgment | OC
- **CLISTER-D21**: CLISTER | 12 | 5.0 | "Les suites postopératoires furent simples." / "Les suites postopératoires étaient simple." | Highly repeated clinical boilerplate formula saturating score=5 cluster | IC
- **CLISTER-D22**: CLISTER | 8 | 1.0 | "Jour 45 - - - - - - - - - 25 μg 0,4 mg" / "Jour 53 15,13 12,0 1,58 - - - - - - 25 μg 0,4 mg" | Tabular medication tracking data; non-standard sentence structure | IC
- **CLISTER-D23**: CLISTER | 191 | 2.0 | "5 mg PO Q 4H PRN X" / "10 mg PO Q 4H PRN X X" | Abbreviation-heavy clinical shorthand; non-standard register | IC
- **CLISTER-D24**: CLISTER | 163 | 5.0 | "Sheldon).\n\nLe patient subissait une chi miothérapie par Méthotrexate - Vinblastine - Endoxan -Cisplatine par voie" | Fragment with apparent OCR word break ("chi miothérapie"); source document processing artifact | IC
- **MANTRAGSC-D1**: fr_emea | 5 | CHEM | `"Chaque comprimé contient 500 mg de ranolazine."` | Standard drug labeling INN+dosage sentence | IC
- **MANTRAGSC-D2**: fr_emea | 7 | CHEM | `"la posologie recommandée d' Agenerase solution buvable est de 17 mg (1,1 ml)/ kg trois fois par jour, sans excéder la dose maximale de 2800 mg par jour"` | Posology statement with dose thresholds from drug leaflet | IC, IO
- **MANTRAGSC-D3**: fr_emea | 6 | DISO | `"Des symptômes potentiellement liés à l' histamine tels que éruption cutanée étendue, gonflement du visage et/ ou des lèvres, démangeaisons, sensation de chaleur ou difficulté à respirer, ont été rapportés."` | Adverse reaction / safety warning from drug label | IC
- **MANTRAGSC-D4**: fr_emea | 11 | DISO | `"Les effets indésirables, en dehors des cas isolés, sont repris ci-dessous: ils sont classés par organe et par ordre de fréquence"` | SmPC/leaflet adverse effects section header | IC, IO
- **MANTRAGSC-D5**: fr_patents | 5 | CHEM | `"Forme posologique orale selon la revendication 1, dans laquelle ledit antagoniste opioïde libérable est la naltrexone et ledit opioïde libérable est la codéine, dans laquelle le rapport de la naltrexone sur la codéine libérable est de 0,005 : 1 à 0,044 : 1."` | Pharmaceutical patent claim with drug ratio | IC, IO
- **MANTRAGSC-D6**: fr_emea | 9 | CHEM | `"1 ml de solution contient 40 microgrammes de travoprost et 5 mg de timolol (sous forme de maléate de timolol)"` | INN with salt form in drug composition statement | OO
- **MANTRAGSC-D7**: fr_patents | 3 | CHEM | `"le laxatif osmotique est du glycol de polyéthylène 3350"` | Excipient-level chemical naming annotated as CHEM | IC, OO
- **MANTRAGSC-D8**: fr_medline | 1 | DISO | `"Luxation antérieure ouverte post-traumatique de la hanche chez l'enfant."` | Traumatology research title; not regulatory text | IC, IO
- **MANTRAGSC-D9**: fr_medline | 3 | DISO | `"Paraparésie fébrile chez une Tunisienne: spondylite à cryptocoque avec atteinte médullaire."` | Clinical case title with non-Metropolitan geographic context | IC
- **MANTRAGSC-D10**: fr_medline | 10 | PROC | `"Le problème de la régulation des naissances: aspects médico-légaux et médico-sociaux."` | Public health/social medicine framing; outside regulatory domain | IO
- **MANTRAGSC-D11**: fr_emea | 7 | CHEM | `"antirétroviraux"` (tag=2, CHEM) | Drug class labeled same as INN; no regulatory sub-distinction | OO
- **MANTRAGSC-D12**: fr_patents | 2 | CHEM | `"Composition pharmaceutique selon la revendication 9, dans laquelle la mort cellulaire induite est la mort cellulaire d' une cellule B ou d' une cellule T."` | Pharmaceutical composition claim; no regulatory claim-structure annotation | OO
- **MANTRAGSC-D13**: de_emea | 7 | CHEM | `"Die empfohlene Dosis für Agenerase Lösung beträgt 17 mg... Amprenavir/kg Körpergewicht"` | German-language example; not relevant to French deployment | IC
- **MANTRAGSC-D14**: fr_patents | 1 | CHEM | `"Composé selon l'une quelconque des revendications 3 à 8, dans lequel R106 est choisi parmi un hydrogène, un alkyle substitué ou insubstitué en C1-C8 linéaire ou ramifié"` | Chemical patent claim language; distinct from patient leaflet register | IO, IF
- **E3C-D1**: French_clinical | 195 | 0 | "Le bilan biologique montrait une cholestase (bilirubine totale a ` 140 mmol/L, bilirubine conjugue à 80 mmol/L, phosphatases alcalines à 700 UI/L) et une cytolyse" | Formal clinical French with lab value reporting; register-aligned but not regulatory genre | IC, IF
- **E3C-D2**: French_clinical | 478 | 0 | "Le patient a été mis sous traitement par ciclosporine avec une évolution rapide vers une leucémie aigue myéloblastique" | Drug name present (ciclosporine) but tagged O; schema cannot capture INN entities | IC, OO
- **E3C-D3**: French_temporal | 107 | mixed | "Il s'agit d'une patiente de 44 ans, sans antécédent médico-chirurgical, qui a présenté depuis un an des céphalées, compliquées 08 mois après de crises d'épilepsies partielles" | Complex clinical narrative with temporal markers; demonstrates French clinical genre | IC, IF
- **E3C-D4**: French_temporal | 304 | mixed | "L'examen physique a mis en évidence une volumineuse tuméfaction dorsolombaire gauche ovalaire mesurant 24cm de grand axe et 12cm de petit axe" | Multi-class temporal/factuality annotation; BODYPART and measurement spans tagged | OO
- **E3C-D5**: French_clinical | 54 | 1,2 | "Cet aspect évoquait une tumeur solide du péritoine" | B-I IOB2 entity span for CLINENTITY; confirms IOB2 encoding format | OF
- **E3C-D6**: Basque_clinical | 180 | 0 | "Azken hilabeteetan Ikernek kodeina + ibuprofenoa hartu ditu, baina ez du hobekuntza handirik nabaritu" | Basque text; irrelevant to French deployment | IC, IF
- **E3C-D7**: English_clinical | 188 | 0 | "A chest radiograph showed right upper lobe consolidation with volume loss, right para-tracheal and left hilar adenopathy" | English clinical text; irrelevant to French regulatory deployment | IC, IF
- **E3C-D8**: Italian_clinical | 446 | mixed | "Trattata con nutrizione parenterale(NP), volume iniziale di 240 ml/die(166 kcal)" | Italian clinical text; irrelevant to French regulatory deployment | IC, IF
- **E3C-D9**: French_clinical | 439 | 0 | "La culture a isolé le germe Nocardia asteroides" | Bacteriological clinical finding; clinical case genre, not regulatory document | IO, IC
- **E3C-D10**: French_clinical | 253 | 0 | "La fonction hépatique s'est améliorée avec un TP à 82% à l'arrêt du traitement" | Clinical outcome reporting; typical case genre, not regulatory submission text | IO, IC
- **E3C-D11**: French_clinical | 195 | 0 | "une cholestase (bilirubine totale a ` 140 mmol/L...phosphatases alcalines à 700 UI/L)" | Lab measurement tagged O; no dosage/substance/reference-value entity class available | OO
- **E3C-D12**: French_clinical | 478 | 0 | "mis sous traitement par ciclosporine" | Drug name tagged O; schema lacks INN/substance entity type required for regulatory NER | OO, OC
- **E3C-D13**: French_clinical | 64 | 1,2 | "La patiente a déjà mené une première grossesse à terme" | "Première grossesse" tagged CLINENTITY; obstetric clinical annotation norm, not regulatory contraindication logic | OC
- **E3C-D14**: French_clinical | 91 | 0 | "Un prélèvement systématique a été réalisé" | Short decontextualized sentence; illustrates limited training data depth | IC
- **PXCORPUS-D1**: PxCorpus | 5 | medical_prescription | "primperan 10 milligrammes comprimés 1 comprimé en cas de nausée toutes les 8 heures pendant 14 jours" | Brand drug with dose, form, indication, frequency, duration — deployment-relevant posology structure | IC
- **PXCORPUS-D2**: PxCorpus | 166 | medical_prescription | "alprazolam 0,25 milligrammes 1 comprimé en cas d'anxiété pendant 1 mois" | INN drug with dose, conditional indication, duration | IC
- **PXCORPUS-D3**: PxCorpus | 212 | medical_prescription | "triclabendazole comprimés à 250 milligrammes 10 milligrammes par kilogrammes en prise unique pendant 1 mois" | Weight-based dosing expression | IC
- **PXCORPUS-D4**: PxCorpus | 121 | medical_prescription | "cordarone 100 milligrammes 1 comprimé 1 jour sur 2 pendant 1 mois" | Alternating-day schedule — posology variety | IC
- **PXCORPUS-D5**: PxCorpus | 146 | medical_prescription | "toviaz 4 milligrammes comprimés à libération prolongée 1 comprimé le matin quantité suffisante pour 1 mois à renouveler pendant 2 fois" | Modified-release form with renewal instruction | IC
- **PXCORPUS-D6**: PxCorpus | 71 | medical_prescription | "orgazuline injectable 1 injection sous-cutanée matin et soir pendant 7 jours" | Subcutaneous injection route | IC
- **PXCORPUS-D7**: PxCorpus | 150 | medical_prescription | "discotrine 10 milligrammes patch 1 patch le matin au réveil retirer le patch le soir pendant 1 mois" | Transdermal patch with timed application/removal | IC
- **PXCORPUS-D8**: PxCorpus | 4 | replace | "attention il s'agit de 20 milligrammes et pas 10 milligrammes" | Explicit dosage correction speech act | IO, OC
- **PXCORPUS-D9**: PxCorpus | 8 | replace | "remplacer 1 comprimé tous les jours par 1 comprimé en cas d'anxiété" | Regimen replacement: daily → conditional | IO, OC
- **PXCORPUS-D10**: PxCorpus | 76 | none | "euh la spécialité est incohérente avec la posologie car la spécialité est en gélules et la posologie en comprimés…" | Form inconsistency meta-commentary | OC
- **PXCORPUS-D11**: PxCorpus | 92 | none | "ajouter un commentaire pour aciclovir comprimés et ne propose pas les différentes formes galéniques du produit…" | Galenic form selection failure description | OC
- **PXCORPUS-D12**: PxCorpus | 3 | none | "/chet" | Single-token transcription artifact; no pharmaceutical content | IO, IC
- **PXCORPUS-D13**: PxCorpus | 88 | none | "i'll agree come on say avec successes merde je vais roulé faut lui faire un et mettre la rame en mode français…" | Code-switched colloquial fragment from dialogue session | IO, IC, IF
- **PXCORPUS-D14**: PxCorpus | 10 | negate | "ne pas tenir compte à midi tous les jours merd/" | Spoken correction with truncation artifact | IC, IF
- **PXCORPUS-D15**: PxCorpus | 75 | medical_prescription | "euh 2 le matin 2 le midi et 2 le soir" | Spoken filler with no drug name; no regulatory document parallel | IC, IF
- **PXCORPUS-D16**: PxCorpus | 169 | medical_prescription | "lamotrigine 25 milligrammes euh p/ combien" | Incomplete, disfluent, truncated utterance | IC, IF
- **PXCORPUS-D17**: PxCorpus | 207 | medical_prescription | "teralithe 250 milligrammes / le serveur de dialogue met beaucoup de temps à comprendre votre énoncé veuillez reformuler différemment…" | System error message embedded in prescription utterance | IC, IF
- **PXCORPUS-D18**: PxCorpus | schema | — | `["medical_prescription", "negate", "none", "replace"]` | Intent classes model spoken dialogue, not regulatory compliance verdicts | OO
- **PXCORPUS-D19**: PxCorpus | 103 | medical_prescription | "trémétadisine trémétasidine à 20 milligrammes à 3 comprimés par jour pendant 3 semaines" | Tag 49 on "trémétasidine" — undecoded salt qualifier; no regulatory entity taxonomy | OO, IC
- **PXCORPUS-D20**: PxCorpus | 145 | medical_prescription | "lévothyroxine sodique 50 microgrammes 1 comprimé à prendre le matin à jeun pendant 6 semaines" | "sodique" tagged 49 — INN-salt distinction not mapped to ATC or regulatory standard | OO, IC
- **PXCORPUS-D21**: PxCorpus | buffer | — | medical_prescription: 447, negate: 11, replace: 3, none: 39 | Severe class imbalance; `replace` (correction) class underrepresented | OC, OF
- **PXCORPUS-D22**: PxCorpus | 50 | none | "erreur sur le nom du médicament ondonsétron erreur sur la posologie" | System recognition error description — not a regulatory document category | OC
- **PXCORPUS-D23**: PxCorpus | 90 | none | "prononcé 15 milligrammes transcrit 3 milligrammes" | Speech-to-text discrepancy report; no analog in regulatory labeling annotation | OC
- **DIAMED-D1**: DiaMED | 1 | A00-B99 | "Le test rapide VIH était positif, confirmé par la sérologie VIH avec un taux de CD4 à 27/mm3. Les sérologies à cytomégalovirus, toxoplasmose, aspergillaire, hépatite B, hépatite C et syphilitique étaient négatives." | HIV/AIDS case with low CD4 count; Sub-Saharan African disease presentation, not metropolitan French | IC, IO
- **DIAMED-D2**: DiaMED | 2 | C00-D49 | "La sérotonine et la chromogranine plasmatique étaient élevées à respectivement 2320 µg/l et 5820 ng/l." | Carcinoid tumor; oncology chapter confirmed; drug mentions include 5-Fluoro-uracile | IC, IO
- **DIAMED-D3**: DiaMED | 3 | D50-D89 | "keywords: ['Rate', 'abdomen aigu', 'scanner abdominal', 'chirurgie', 'Maroc']" | Moroccan clinical context; geographic mismatch with metropolitan France | IC
- **DIAMED-D4**: DiaMED | 4 | E00-E89 | "Il s'agit d'un enfant de 5ans... ayant consulté aux urgences pour asthénie chronique avec pâleur. L'examen clinique a retrouvé un enfant en bon état général avec des tâches achromiques diffuses" | Piebaldism case assigned to endocrine chapter; illustrates coarse ICD-10 labeling | OO, OC
- **DIAMED-D5**: DiaMED | 5 | F01-F99 | "le diagnostic de pathomimie a été évoqué et retenu. Devant le contexte de dépression, la patiente a été adressée en psychiatrie où ce diagnostic a été confirmé" | Factitious disorder/depression case; confirms mental health chapter coverage | IO
- **DIAMED-D6**: DiaMED | 6 | G00-G99 | "Monsieur Y. O. âgé de 19 ans a été hospitalisé le 03 février 2012 pour une paraplégie évoluant depuis un mois." | Clinical case narrative genre — not regulatory document genre | IO, IC
- **DIAMED-D7**: DiaMED | 7 | H00-H59 | "Il s'agit d'une jeune fille âgée de 17 ans, sans antecedants particuliers, ayant constatée d'elle même une anisocorie sans signes accompagnateurs." | Adie pupil case; confirms ophthalmology chapter | IO
- **DIAMED-D8**: DiaMED | 8 | H60-H95 | "Le diagnostic d'otite externe maligne avait été posé et une antibiothérapie injectable empirique instaurée à base de céphalosporines de troisième génération et de ciprofloxacine" | Drug names with administration routes in clinical context; closest to pharmaceutical vocabulary | IC
- **DIAMED-D9**: DiaMED | 9 | I00-I99 | "Communication interventriculaire ischémique... dans le service de cardiologie du CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" | Explicitly Burkinabé hospital setting — not metropolitan France | IC, OC
- **DIAMED-D10**: DiaMED | 10 | J00-J99 | "En collaboration avec les confrères ORL, la patiente a été mise sous antibiothérapie par voie générale associée à une corticothérapie par voie orale pendant 7 jours" | Generic antibiotic/corticosteroid mention without INN; clinical case genre | IC
- **DIAMED-D11**: DiaMED | 11 | K00-K95 | "Ces douleurs étaient consécutives à une alimentation importante suite à la rupture du jeûn durant le mois de ramadan." | Ramadan context confirms African/North African origin; cultural/geographic mismatch | IC
- **DIAMED-D12**: DiaMED | 12 | L00-L99 | "Elle a reçu une prescription de 200mg de Phénobarbital à prendre en une prise vespérale... Un traitement antipsychotique (Halopéridol 20 mg et Chlorpromazine 400 mg en deux prises par jour)" | Named drugs with dosages in clinical case; keywords include 'Niamey' (Niger) | IC, IO
- **DIAMED-D13**: DiaMED | 13 | M00-M99 | "L'ostéochondrite disséquante du capitellum chez l'adolescent: à propos d'un cas et revue de la littérature" | Clinical case + literature review genre; no regulatory text features | IO, IF
- **DIAMED-D14**: DiaMED | 14 | N00-N99 | "La micro-biopsie a révélé un aspect histologique pouvant évoquer une fibromatose desmoïde sans être exclusif, nous avons complété par une étude immuno-histo-chimique en faveur d'une fibromatose desmoïde." | Clinical case report genre; histopathology language, not regulatory | IC, IO
- **DEFT2021-D1**: DEFT2021/cls | 3 (train) | [6,14,13,19,4] | "Mme J.K. est traitée pour une fibrillation auriculaire depuis deux ans avec le sulfate de quinidine 200 mg trois fois par jour... La prescription de clarithromycine nous semblerait, dans ce cas précis, d'un rapport bénéfice/risque très bas et potentiellement torsadogénique" | Drug interaction case with benefit-risk reasoning; partial overlap with pharmacovigilance language | IC
- **DEFT2021-D2**: DEFT2021/cls | 8 (train) | [20,17,22,13,0,4,19] | "la perfusion de rituximab (375 mg dans 187,5 ml NaCl 0,9 %) débute à une vitesse de 15 mg/heure... le patient se plaint de difficultés respiratoires" | Precise pharmaceutical dosing and adverse reaction documentation | IC
- **DEFT2021-D3**: DEFT2021/ner | 80 (train) | SUBSTANCE | "La patiente était mise sous traitement anti-bacillaire à base de rifampicine – isoniazide – pyrazinamide pendant 6 mois" | Drug names tagged as SUBSTANCE with DURATION; posology annotation | OO
- **DEFT2021-D4**: DEFT2021/cls | 5 (train) | [12,3,20,4,7,5] | (six specialty labels for complex multi-system hepatotoxicity case) | Demonstrates multi-label output consistent with deployment's multi-candidate design | OO, OF
- **DEFT2021-D5**: DEFT2021/ner | 55 (train) | SUBSTANCE/DOSAGE/MODE/FREQ | "Hydrocortisone 300 mg IV immédiatement ; Traitement Hydroxyzine 25 mg par voie orale toutes les 6 heures" | Posology-adjacent annotation of drug, dose, route, frequency | OO
- **DEFT2021-D6**: DEFT2021/ner | 7 (train) | SUBSTANCE/DURATION | "sorti au 5ème jour sous cotrimoxazole pour 10 jours" | Drug name + duration annotated; basic posology entity coverage | IC
- **DEFT2021-D7**: DEFT2021/cls | 1 (train) | [18,4] | "Femme de 73 ans n'ayant eu qu'un seul enfant par césarienne… insuffisance rénale obstructive avec une urée sanguine à 10 mmol/l de sérum" | Standard clinical French prose; confirms register and language match | IF
- **DEFT2021-D8**: DEFT2021/cls | 6 (train) | [12,17,4] | "La néphrostomie a été posée la veille de l'intervention… Au 5ème jour, le malade a fait un choc hémorragique" | Narrative clinical case; no regulatory document structure present | IO, IC
- **DEFT2021-D9**: DEFT2021/cls | 10 (train) | [3] | "Des prélèvements de sérum et d'urine sont réalisés aux fins de «recherche d'alcoolémie»… Du GHB est retrouvé dans l'urine au taux de 4 ug/ml" | Forensic toxicology case; no regulatory labeling context | IO
- **DEFT2021-D10**: DEFT2021/ner | 3 (train) | SUBSTANCE (21/22) | "diphenhydramine et de méthylprednisolone" | Drug names tagged SUBSTANCE with no INN/ATC/excipient distinction | OO
- **DEFT2021-D11**: DEFT2021/ner | 28 (train) | PATHOLOGY | "un carcinome vésical droit, de 3 cm de diamètre, infiltrant (grade II, pT2)" | Clinical pathology staging; no regulatory safety signal mapping | IC
- **DEFT2021-D12**: DEFT2021/cls | 4 (train) | [15,4,3] | "Le patient dira avoir ingéré au moins 20 comprimés de Séresta 50 mg… Il parle également d'injection intraveineuse de poudre «NRG»" | Hearsay drug exposure in clinical narrative; annotation by clinical not regulatory expert | OC
- **DEFT2021-D13**: DEFT2021/cls | 5 (train) | [12,3,20,4,7,5] | (six co-occurring MeSH labels for multi-system hepatotoxicity) | Multi-label clinical annotation; no regulatory-legal ground truth | OC
- **DEFT2021-D14**: DEFT2021/cls | 2 (train) | [4,9,18] | "L'histologie découvrait un oncocytome rénal et l'évolution était favorable avec un recul de 5 ans" | Oncology case; MeSH labels reflect disease classification, not regulatory safety axes | OO
- **DEFT2021-D15**: DEFT2021/cls | 3 (train) | [6,14,13,19,4] | "le pharmacien hésite à lui remettre la prescription… Tableau I : Interactions médicamenteuses dans le cas clinique" | Canadian pharmacy clinical case; register and institutional context differ from metropolitan French regulatory documentation | IC
- **DEFT2021-D16**: DEFT2021/cls | 8 (train) | [20,17,22,13,0,4,19] | "acétaminophène 300 mg par voie orale" | Canadian drug name convention ('acétaminophène' vs French 'paracétamol'); cross-regional register variation | IC
- **CAS-D1**: CAS/cls | 3 | neutral | "l'examen clinique montre un état général conservé." | Standard French clinical examination sentence — confirms register alignment | IF, IC
- **CAS-D2**: CAS/cls | 13 | neutral | "depuis hier soir, je suis essouflé, j'ai des frissons, j'ai mal à la poitrine" | Patient-reported symptom language in French clinical case — confirms clinical register | IF, IC
- **CAS-D3**: CAS/cls | 1 | negation_speculation | "le diagnostic d'ulcère solitaire du rectum était évoqué à tort et une rééducation recto-sphinctérienne réalisée sans succès." | Combined negation + speculation in clinical narrative — demonstrates label complexity | IO, OO
- **CAS-D4**: CAS/cls | 5 | negation_speculation | "il est donc possible que le même résultat clinique aurait été observé chez ce patient sans ajout de la nac." | Speculative treatment outcome claim — relevant to pharmacovigilance reasoning | IO, OO
- **CAS-D5**: CAS/cls | 33 | speculation | "puisque le traitement par la warfarine semble plus problématique, un naco est envisagé." | Drug treatment uncertainty phrasing — closest to regulatory safety language | IC, IO
- **CAS-D6**: CAS/cls | 8 | speculation | "une origine médicamenteuse étant envisagée (avec éventuellement une imputabilité du paracétamol), il était décidé d'arrêter les différents traitements et de remplacer les lavements de pentasa® par du proctocort® (hydrocortisone acétate 90 mg : 1 lavement tous les soirs)." | Contains drug names with dosing — limited regulatory vocabulary present | IC
- **CAS-D7**: CAS/cls | 47 | neutral | "après mise en condition en unité de soins intensifs et administration d'une ampoule de digoxine en intraveineuse" | Drug name with route of administration in clinical narrative | IC
- **CAS-D8**: CAS/ner_neg | 5 | — | tokens: "sans antécédent familial de maladie colique" ner_tags: [0,1,2,2,2,2,...] | Span-level negation scope annotation — BIO tagging of negated content | OO
- **CAS-D9**: CAS/ner_neg | 21 | — | "ne montrait aucune lésion focale" ner_tags: [0,1,0,2,2,0] | Distributed negation scope correctly marked at token level | OO
- **CAS-D10**: CAS/cls | 26 | neutral | "les constantes hémodynamiques étaient stables mais le bilan biologique mettait en évidence une anémie à 5,7 g/100ml d'hb" | Lab-value clinical prose — not representative of SmPC or leaflet structure | IO, IC
- **CAS-D11**: CAS/cls | 44 | neutral | "la masse respectait le plan osseux sacro-coccygien, refoulait la vessie, le rectum et le canal anal qui présentait une infiltration circonférentielle." | Pathology/imaging prose from clinical case — absent in regulatory labeling genres | IO, IC
- **CAS-D12**: CAS/cls | 3 | neutral | "l'examen clinique montre un état général conservé." | Neutral label for factual clinical statement — irrelevant to regulatory entity NER | OO
- **CAS-D13**: CAS/ner_spec | 16 | — | "le diagnostic d'ulcère solitaire du rectum était évoqué à tort" ner_tags: [1,2,2,2,2,2,2,2,...] | Speculation scope marks diagnostic phrase — no counterpart in regulatory NER schema | OO
- **CAS-D14**: CAS/pos | 10 | — | tokens: ['le', 'scanner', 'réalisé', ...] pos_tags: [12, 24, 25, ...] | Automatic POS assignment without full human adjudication — silver-standard risk | OC
- **CAS-D15**: CAS/ner_neg | 22 | — | "administration d'une ampoule de digoxine en intraveineuse" ner_tags: [0,...,0] all zeros | Drug name entirely untagged; NER only captures negation scope, not pharmacological entities | IC, OO
- **CAS-D16**: CAS/cls | buffer | — | negation_speculation: 6, negation: 100, neutral: 368, speculation: 26 | Extreme neutral class dominance — minority safety-critical classes underrepresented | OO, OF
- **CAS-D17**: CAS/cls | 13 | neutral | "depuis hier soir, je suis essouflé, j'ai des frissons, j'ai mal à la poitrine" | Metropolitan France general medicine symptom vocabulary — no tropical disease content | IC
- **ESSAI-D1**: ESSAI/cls | train/1 | negation_speculation | "Evaluer l' hypothèse selon laquelle une chimiothérapie à hautes doses avec une combinaison de Busulfan et de Melphalan (BU-MEL) permettra d' obtenir une survie sans événement à 3 ans supérieure à une consolidation par une association de Carboplatine VP16 et Melphalan chez des patients porteurs d' un neuroblastome à haut risque." | Formal French biomedical prose with drug names in clinical trial objective format | IC, IF
- **ESSAI-D2**: ESSAI/cls | train/12 | speculation | "Cette étude si elle est positive permettra de valider, pour la première fois dans les tumeurs neuroendocrines carcinoïdes bronchiques évoluées, le bénéfice dans le contrôle de la progression tumorale de la prescription du Lanréotide 120 mg par mois." | Includes posology expression (120 mg per month) relevant to drug labeling | IC
- **ESSAI-D3**: ESSAI/ner_neg | train/9 | O (all) | "L' acétate d' abiratérone ou l' enzalutamide sont des traitements assez récents et ainsi appelés « hormonothérapies de nouvelle génération »." | INN-level drug names present but not labeled as drug entities | IC, OO
- **ESSAI-D4**: ESSAI/ner_neg | train/1 | O (all) | "avec la combinaison gemcitabine + abraxane, chez des patients avec un cancer du pancréas." | Drug names appear without entity-type annotation | IC, OO
- **ESSAI-D5**: ESSAI/ner_spec | train/3 | O (all) | "Lorsque la chimiothérapie à base de platine est associée au Caelyx, les perfusions ont lieu tous les quinze jours pendant 6 mois (cycles de 28 jours) puis une maintenance est ensuite instaurée avec le Bevacizumab et l' Atezolizumab ou placebo perfusés toutes les 3 semaines." | Drug names and dosing schedule present but unlabeled as entities | IC
- **ESSAI-D6**: ESSAI/cls | train/2 | negation | "Des traitements de radiothérapie plus courts sur 3 semaines pour des cancers du sein sans atteinte ganglionnaire se sont montrés tout aussi efficace et ne présentent pas plus d' effets secondaires dans différents essais cliniques sur plusieurs milliers de patientes." | Negation of adverse effects — partially relevant to safety claim checking | OO
- **ESSAI-D7**: ESSAI/cls | train/10 | negation | "l' objectif de cette étude de recherche clinique est d' évaluer la sécurité d' emploi et l' efficacité de l' avelumab (MSB0010718C) associé aux meilleurs soins palliatifs chez des patients atteints d' un adénocarcinome de l' estomac ou de la jonction gastroœsophagienne non résécable, récidivant ou métastatique." | Negation of resectability in complex oncology context | IC
- **ESSAI-D8**: ESSAI/cls | train/5 | negation_speculation | "Dans ce contexte, l' étude ESMART a pour objectif d' explorer des nouveaux médicaments, seul ou en association, de chercher quelle est la meilleure dose chez l' enfant, adolescent et jeune adulte, et si des anomalies retrouvées ou non dans la tumeur mènent à un avantage thérapeutique chez ces patients." | Investigational framing absent from approved regulatory document language | IO
- **ESSAI-D9**: ESSAI/ner_spec | train/4 | O (all) | "Cet essai thérapeutique de phase III, multicentrique, randomisé à 3 bras, s' adresse à des patientes atteintes d' un cancer de haut grade de type séreux de l' ovaire, des trompes de Fallope ou du péritoine résistant ou réfractaire au platine." | Trial eligibility criteria, not SmPC/PIL regulatory document structure | IO
- **ESSAI-D10**: ESSAI/ner_neg | train/11 | 0,0,...,2,3,... | "radiothérapie hypofractionnée qui est devenue un standard pour les cancers du sein en l' absence d' atteinte ganglionnaire chez les femmes ménopausées" (atteinte ganglionnaire tagged B/I-NEG) | Only negated clinical finding span tagged; no drug entity labels | OO
- **ESSAI-D11**: ESSAI/ner_spec | train/10 | 0,0,...,2,3,... | "Cette étude vise à déterminer si le traitement par un inhibiteur de PARP, le talazoparib, peut être plus efficace et mieux toléré de la chimiothérapie de référence chez les patients atteints de un cancer du sein métastatique" | Speculated treatment span tagged; drug name (talazoparib) not categorized as drug entity | OO, IC
- **ESSAI-D12**: ESSAI/pos | train/2 | pos_tags=[3,7,...] | "Le MEDI9197 est injecté en intra-tumoral tous les 28j (4 semaines)." | Drug identifier MEDI9197 tagged as NAM (tag 7) by automatic TreeTagger — silver standard | OC, OF
- **ESSAI-D13**: ESSAI/cls | train/9 | negation_speculation | "Ne pas prendre part à un autre projet de recherche sans l' accord de votre médecin, ceci pour vous protéger de tout accident possible pouvant résulter par exemple d' incompatibilités possibles ou d' autres dangers." | Instruction-format negation in patient consent language, not regulatory safety warning | OC
