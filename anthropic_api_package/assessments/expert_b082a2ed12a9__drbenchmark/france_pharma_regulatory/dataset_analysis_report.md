## Dataset Analysis Report

**Benchmark:** DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Domain
**Datasets analyzed:** 11 (QUAERO, FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC, E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI)
**Analysis date:** 2025-07-14

---

### Per-Dataset Fit Assessment

#### DrBenchmark/QUAERO

- **Task:** Named Entity Recognition (token classification, UMLS Semantic Groups, 10 classes)
- **Deployment fit:** **Partial** — The EMEA config is the single closest match to the deployment's document genre (EU drug leaflets), with confirmed presence of EMA authorization headers, excipient lists, contraindication statements, and posology expressions. However, critical regulatory entity types (posology as a distinct class, contraindication qualifiers, ATC codes, INN vs. excipient distinction) are absent from the annotation schema.
- **Key strengths:**
  - EMEA config draws from authentic EMA package leaflet text in the exact regulatory register (QUAERO-D1, QUAERO-D2, QUAERO-D3)
  - Excipient names and pharmaceutical formulation vocabulary confirmed present (QUAERO-D4, QUAERO-D5, QUAERO-D6)
  - INNs, brand names, ATC code references appear in text (QUAERO-D7)
  - Contraindication and safety warning language in formulaic patient-leaflet register (QUAERO-D11, QUAERO-D12, QUAERO-D13)
  - EU marketing authorization metadata present (QUAERO-D14)
  - CHEM entity class captures active substances and excipients (QUAERO-D15)
- **Key concerns:**
  - CHEM category conflates INNs, excipients, chemical compounds, and biologics without regulatory-critical subtypes (QUAERO-D16, QUAERO-D17)
  - No DOSAGE/POSOLOGY entity class despite abundant dosage content in text; dose values systematically receive O tags (QUAERO-D18, QUAERO-D19)
  - No contraindication qualifier entity label; contraindication text present but legally critical structure unannotated (QUAERO-D21)
  - Annotators were NLP/biomedical researchers mapping to UMLS Semantic Groups, not regulatory affairs specialists (QUAERO-D20)
  - Tokenization artifacts and multilingual fragments from sentence-splitting of long EMEA documents (QUAERO-D22 through QUAERO-D26)

---

#### DrBenchmark/FrenchMedMCQA

- **Task:** Multiple-Choice Question Answering (5-option, 1–5 correct answers from pharmacy diploma exams)
- **Deployment fit:** **Weak** — The task format (closed-option pharmacy exam QA) is entirely misaligned with the deployment's NER and STS requirements. Pharmaceutical vocabulary is rich but embedded in didactic exam items, not running regulatory document text.
- **Key strengths:**
  - Rich pharmaceutical terminology: INN-level drug names, pharmacological mechanisms, contraindication concepts (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D4, FRENCHMEDMCQA-D7, FRENCHMEDMCQA-D8)
  - One example explicitly references SmPC ("résumé des caractéristiques du produit") (FRENCHMEDMCQA-D5)
  - Pharmaceutical container and formulation specifications present (FRENCHMEDMCQA-D2, FRENCHMEDMCQA-D6)
  - Analytical chemistry content adjacent to CTD quality modules (FRENCHMEDMCQA-D9, FRENCHMEDMCQA-D10)
- **Key concerns:**
  - CRITICAL task type mismatch: MCQA produces index-set outputs, not NER spans or STS scores (FRENCHMEDMCQA-D11, FRENCHMEDMCQA-D12)
  - No regulatory document text whatsoever; all inputs are exam-format question items in didactic register (FRENCHMEDMCQA-D13, FRENCHMEDMCQA-D14)
  - Drug names embedded in exam items, not running text amenable to span extraction (FRENCHMEDMCQA-D15)
  - Clinical and basic science content dominates; regulatory procedural content is rare (FRENCHMEDMCQA-D16, FRENCHMEDMCQA-D17)
  - One example references an absent molecular structure figure (FRENCHMEDMCQA-D19)

---

#### DrBenchmark/DEFT2020

- **Task:** Semantic Textual Similarity (0–5 continuous scale, multi-annotator); secondary multi-class sentence classification
- **Deployment fit:** **Partial** — Some sentence pairs derive from drug leaflet text in a format directly relevant to the deployment's STS compliance-flagging use case. However, a substantial fraction of pairs are off-domain (encyclopedic, geographic), and the scoring function is demonstrably miscalibrated for regulatory equivalence.
- **Key strengths:**
  - Drug leaflet safety instructions, storage conditions, and contraindication pairs confirmed present (DEFT2020-D1, DEFT2020-D2, DEFT2020-D3, DEFT2020-D4, DEFT2020-D5, DEFT2020-D6)
  - Named INNs (capécitabine, glimepiride, clindamycine) in safety instruction context (DEFT2020-D7, DEFT2020-D8, DEFT2020-D9)
  - Multi-annotator scoring with individual scores enabling variance analysis (DEFT2020-D10, DEFT2020-D11)
- **Key concerns:**
  - CRITICAL: Large fraction of pairs are non-biomedical and non-regulatory (beekeeping, historical figures, geography, hockey) (DEFT2020-D13 through DEFT2020-D17)
  - CRITICAL: Scoring calibration treats legally material qualifier differences as near-synonymy — the "congénitale" qualifier drop scored 4.6 (DEFT2020-D18); specific substance name vs. generic term scored 4.3 (DEFT2020-D20)
  - High annotator variance on pharmaceutical pairs (scores spanning 2–5) indicates non-specialist annotation (DEFT2020-D10, DEFT2020-D11, DEFT2020-D22)
  - Sentence-splitting removes document context needed for compliance verification (DEFT2020-D21)

---

#### DrBenchmark/MORFITT

- **Task:** Multi-label specialty classification (12 medical specialties over PMC biomedical abstracts)
- **Deployment fit:** **Weak** — Document-level specialty classification of research abstracts; task type, document genre, geographic scope, and annotation granularity are all misaligned with the deployment's NER and STS requirements.
- **Key strengths:**
  - Pharmacology and chemistry specialty labels provide partial domain proximity (MORFITT-D1, MORFITT-D3)
  - Multi-label annotation structure mirrors multi-dimensional regulatory document categorization (MORFITT-D4, MORFITT-D5)
- **Key concerns:**
  - CRITICAL task type mismatch: multi-label document classification provides no NER spans or STS scores (MORFITT-D6, MORFITT-D7)
  - CRITICAL genre mismatch: all content is PMC biomedical research abstracts, not regulatory documents (MORFITT-D8, MORFITT-D9)
  - No regulatory entity annotations whatsoever (MORFITT-D10)
  - Substantial non-EMA-jurisdiction content: Saudi Arabia, Egypt, Jordan, Canada, veterinary medicine (MORFITT-D11, MORFITT-D12, MORFITT-D13, MORFITT-D14, MORFITT-D15)

---

#### DrBenchmark/CLISTER

- **Task:** Semantic Textual Similarity (0–5 continuous scale, averaged multi-annotator, French clinical sentence pairs)
- **Deployment fit:** **Partial** — Provides a French biomedical STS baseline with graded multi-annotator labels and some pharmaceutical content. However, source domain is exclusively clinical cases, scoring is calibrated for general clinical similarity, and numerical differences that would be regulatory-critical are treated as near-equivalent.
- **Key strengths:**
  - French biomedical language well-represented; consistent clinical medical vocabulary (CLISTER-D1, CLISTER-D2)
  - Some dosage and drug name content present (CLISTER-D3, CLISTER-D4, CLISTER-D5)
  - Full 0–5 similarity spectrum well-populated (CLISTER-D6, CLISTER-D7)
  - Minor lexical additions correctly reduce scores (CLISTER-D9), providing partial dose-addition sensitivity signal
- **Key concerns:**
  - CRITICAL: Entirely from clinical case reports, not regulatory documents; no SmPC, leaflet, or CTD text (CLISTER-D11, CLISTER-D12)
  - CRITICAL: A 2× numerical difference (10 vs. 20 mmol/l) scored 4.0 — near-equivalent under this rubric, potentially critical under EMA standards (CLISTER-D13, CLISTER-D15)
  - Annotators are biomedical NLP specialists, not regulatory affairs experts; no regulatory calibration documented (CLISTER-D16)
  - No INN/ATC/excipient-specific pairs; no contraindication qualifier precision pairs (CLISTER-D17)
  - Structured/tabular data rows produce semantically ambiguous STS judgments (CLISTER-D14, CLISTER-D18)

---

#### DrBenchmark/MANTRAGSC

- **Task:** Biomedical NER (IOB2, UMLS Semantic Groups, 10–11 classes; fr_emea, fr_medline, fr_patents configs)
- **Deployment fit:** **Partial (documented); Weak (sampled)** — The fr_emea and fr_patents configs are documented as deployment-relevant, but all sampled examples derive from fr_medline (research abstracts). The CHEM class provides partial pharmaceutical substance coverage; entity schema has the same fundamental gaps as QUAERO.
- **Key strengths:**
  - CHEM entity class captures pharmaceutical substances including INN-level drug names (MANTRAGSC-D1, MANTRAGSC-D2)
  - fr_emea and fr_patents configs exist (documented in benchmark YAML), covering two deployment-relevant document genres
  - Multilingual architecture supports cross-jurisdictional EU regulatory workflow validation
- **Key concerns:**
  - CRITICAL: All 70 sampled examples are from fr_medline (research abstracts), not fr_emea or fr_patents; no regulatory document genre visible in sample (MANTRAGSC-D4, MANTRAGSC-D5, MANTRAGSC-D6)
  - CRITICAL: No regulatory entity types in sample; single drug name (Cefotaxime) with no dosage, route, or contraindication context (MANTRAGSC-D8)
  - CRITICAL: Register mismatch — all sampled text is academic/clinical publication prose, not regulatory legal prose (MANTRAGSC-D10, MANTRAGSC-D11)
  - Extremely small dataset per config (~70 rows); CamemBERT models fail on Patents config (MANTRAGSC-D13, MANTRAGSC-D14)
  - UMLS Semantic Group schema does not distinguish INNs from general CHEM entities (MANTRAGSC-D15)
  - Some examples from sub-Saharan African and North African clinical contexts, outside EMA jurisdiction (MANTRAGSC-D16, MANTRAGSC-D17)

---

#### DrBenchmark/E3C

- **Task:** Named Entity Recognition (CLINENTITY + temporal/factuality entity layers; French clinical cases)
- **Deployment fit:** **Weak** — Clinical entity and temporal annotation schema systematically excludes all drug/substance/dosage/contraindication entities. Rich pharmaceutical vocabulary in text is entirely unlabeled. Source genre is clinical case reports only.
- **Key strengths:**
  - Rich clinical French vocabulary including INN-level drug names in running prose (E3C-D1, E3C-D2, E3C-D3, E3C-D4, E3C-D5, E3C-D6)
  - Drug names appear with dosage expressions and routes of administration (E3C-D1, E3C-D4)
  - French language with no script or modality mismatch
- **Key concerns:**
  - CRITICAL: NER schema (CLINENTITY/EVENT/ACTOR/BODYPART/TIMEX3/RML) systematically labels O for all drug names, dosages, and pharmaceutical entities — four INN drugs with dosages all O-tagged in a single example (E3C-D7, E3C-D8)
  - CRITICAL: Exclusively clinical case report genre; no regulatory document text (E3C-D11, E3C-D12)
  - CRITICAL: Annotation norms prioritize clinical entities over pharmaceutical entities; drug names present but unlabeled while disease names are labeled (E3C-D9, E3C-D14)
  - No STS task
  - Some examples from sub-Saharan African and North African clinical contexts (E3C-D15, E3C-D16)
  - Very sparse positive labels on pharmaceutical content (E3C-D17, E3C-D18)

---

#### DrBenchmark/PxCorpus

- **Task:** Intent classification (4 classes) + NER (38 classes) over transcribed spoken drug prescription dialogues
- **Deployment fit:** **Weak** — Dense pharmaceutical vocabulary and posology coverage are genuine strengths, but the spoken/transcribed register with disfluencies, off-task speech, and conversational conventions is fundamentally incompatible with formal regulatory document prose. Contraindication qualifiers are absent from the NER schema despite appearing in text.
- **Key strengths:**
  - Dense INN-level drug names, dosages, frequencies, routes of administration in transcribed text (PXCORPUS-D1, PXCORPUS-D2, PXCORPUS-D3)
  - Wide posology expression diversity including conditional renewal and maximum dose constraints (PXCORPUS-D4, PXCORPUS-D6)
  - Replace/negate intents directly analogous to document revision and inconsistency detection (PXCORPUS-D7, PXCORPUS-D8)
  - Route-of-administration and formulation vocabulary consistent with pharmaceutical labeling (PXCORPUS-D9, PXCORPUS-D10)
- **Key concerns:**
  - CRITICAL: Spoken/transcribed register with disfluencies, English fragments, expletives, and system interruption messages absent from regulatory prose (PXCORPUS-D11, PXCORPUS-D12, PXCORPUS-D13, PXCORPUS-D14)
  - CRITICAL: No contraindication qualifier entity class; contraindication-adjacent qualifiers receive O tags (PXCORPUS-D15, PXCORPUS-D16)
  - MAJOR: Severe label class imbalance; only ~3 replace examples in 500-sample buffer (PXCORPUS-D17, PXCORPUS-D18)
  - MAJOR: Brand names predominate over INNs; EU regulatory documents require INN primacy (PXCORPUS-D19, PXCORPUS-D20)
  - No STS task
  - Degenerate utterances (single tokens, interjections) reduce signal quality (PXCORPUS-D21, PXCORPUS-D22, PXCORPUS-D23)

---

#### DrBenchmark/DiaMED

- **Task:** Single-label document classification (22 ICD-10 chapter labels over African clinical case reports)
- **Deployment fit:** **Weak** — ICD-10 chapter-level classification of Pan African Medical Journal clinical cases; task type, document genre, geographic context, and annotation ontology are all misaligned with the deployment's NER and STS requirements.
- **Key strengths:**
  - French biomedical text in professional medical prose register (DIAMED-D1, DIAMED-D8)
  - Transparent annotation with inter-annotator agreement and one medical expert contributor (benchmark documentation)
  - One example involves drug-induced toxic reaction methodology (DIAMED-D12)
- **Key concerns:**
  - CRITICAL: ICD-10 chapter classification produces no NER spans or STS scores (DIAMED-D1 through DIAMED-D14)
  - CRITICAL: All content from Pan African Medical Journal; sub-Saharan African clinical context, not EMA/ANSM jurisdiction (DIAMED-D3, DIAMED-D9)
  - CRITICAL: No regulatory entity types; drug mentions are incidental, not EMA-standardized INN format (DIAMED-D1)
  - African geographic/cultural context diverges from EU regulatory norms (DIAMED-D4, DIAMED-D9)
  - Class imbalance reduces generalization value

---

#### DrBenchmark/DEFT2021

- **Task:** NER (13 clinical entity types) + multi-label classification (23 MeSH Chapter C categories) over French clinical case reports
- **Deployment fit:** **Weak** — Partial drug/dosage NER annotation provides modest pharmaceutical signal, but the entity schema is calibrated for clinical entities, source genre is clinical narratives, and the dataset is very small. MeSH classification has no regulatory utility.
- **Key strengths:**
  - Drug names and dosage values do appear in NER ground truth; treatment (tag 21/22) and dosage (tag 5/6) entity types cover partial pharmaceutical territory (DEFT2021-D1, DEFT2021-D2, DEFT2021-D3)
  - Mode of administration and frequency entity types present (DEFT2021-D4, DEFT2021-D5)
  - Formal clinical French prose register, morphosyntactically similar to regulatory French
- **Key concerns:**
  - CRITICAL: NER schema covers clinical entities (pathologies, anatomy, exam results) — INNs vs. excipients not distinguished, no ATC codes, no contraindication qualifier class (DEFT2021-D5, DEFT2021-D6)
  - CRITICAL: All source text is clinical case reports; no regulatory document genre (DEFT2021-D7, DEFT2021-D8)
  - CRITICAL: Annotation norms calibrated for clinical text mining competition, not EMA/ANSM regulatory standards (DEFT2021-D9)
  - MeSH Chapter C classification ontology has no alignment to regulatory classification schemes (DEFT2021-D10)
  - Very small dataset (4,712 NER rows, 275 classification rows); insufficient for regulatory NER fine-tuning
  - Some examples from African/tropical clinical contexts (DEFT2021-D11)

---

#### DrBenchmark/CAS

- **Task:** POS tagging (31 classes, automatic annotation) + negation/speculation NER and classification over clinical case reports
- **Deployment fit:** **Weak** — Provides French biomedical morphosyntax evaluation and negation detection, both of which have limited downstream value for the deployment's primary NER and STS tasks. No regulatory document text; no regulatory entity annotation.
- **Key strengths:**
  - Drug names and dosage expressions confirmed in text (CAS-D1, CAS-D2, CAS-D3, CAS-D5)
  - Negation detection directly relevant to filtering negated safety conditions (CAS-D6, CAS-D7)
  - Exposure limit language with regulatory-adjacent numerical precision (CAS-D9)
- **Key concerns:**
  - CRITICAL: All content from clinical case narratives; no regulatory document text (CAS-D10, CAS-D11, CAS-D12)
  - CRITICAL: POS annotation provides no regulatory entity labels; drug INNs in text receive only morphosyntactic tags (CAS-D13, CAS-D14)
  - Negation/speculation labels calibrated for clinical linguistic annotation, not regulatory equivalence (benchmark documentation)
  - No STS task
  - Automatic (silver) POS annotations with ~2% error rate

---

#### DrBenchmark/ESSAI

- **Task:** POS tagging (41 classes, automatic annotation) + negation/speculation NER and classification over clinical trial protocols
- **Deployment fit:** **Partial** — Clinical trial protocols contain the densest pharmaceutical vocabulary of any non-QUAERO dataset, with confirmed INNs, posology expressions, and negated contraindication phrases. However, trial protocol genre differs substantially from regulatory labeling, annotation provides no regulatory entity labels, and scoring is miscalibrated for legal compliance.
- **Key strengths:**
  - High density of INN-level drug names, combination regimens, experimental compound codes (ESSAI-D1, ESSAI-D2, ESSAI-D3)
  - Rich posology vocabulary: routes, frequencies, durations in compact form (ESSAI-D4, ESSAI-D5, ESSAI-D6)
  - Negated contraindication phrases confirmed present in text (ESSAI-D7, ESSAI-D8)
  - Patient-addressed sections partially overlap with patient information leaflet register (ESSAI-D13, ESSAI-D24)
- **Key concerns:**
  - CRITICAL: Genre mismatch — clinical trial protocols differ from SmPCs and regulatory labeling in register, structure, and legal constraint level (ESSAI-D12, ESSAI-D13, ESSAI-D14)
  - CRITICAL: POS-only annotation; no entity-level regulatory NER labels despite abundant pharmaceutical content (ESSAI-D18, ESSAI-D19)
  - Experimental compound codes dominate over approved INNs; ATC codes entirely absent (ESSAI-D15, ESSAI-D16, ESSAI-D17)
  - Speculation labels calibrated for clinical trial epistemics, not regulatory legal modality (ESSAI-D20, ESSAI-D21)
  - Oncology domain dominance reduces therapeutic area generalizability (ESSAI-D22)
  - Informal patient-addressed registers atypical of regulatory prose (ESSAI-D25)

---

### Cross-Cutting Strengths

**1. French pharmaceutical vocabulary coverage across multiple datasets**
Despite genre mismatches, the benchmark collectively represents a wide range of INN-level drug names, dosage expressions, and routes of administration in French. QUAERO-D7, DEFT2021-D3, ESSAI-D2, E3C-D1, CAS-D2, and PXCORPUS-D1 all confirm that the lexical field of pharmaceutical entities is broadly present. A model pre-trained on this benchmark will have encountered French pharmaceutical vocabulary in diverse syntactic and semantic contexts, supporting transfer to regulatory text at the word-representation level even without regulatory-specific entity annotations.

**2. EMEA drug leaflet genre authenticity in QUAERO**
QUAERO is the only dataset with confirmed authentic EMA regulatory document provenance. QUAERO-D1 through QUAERO-D14 collectively confirm the presence of EMA authorization headers, full excipient lists with E-numbers, INN nomenclature, contraindication statements in formulaic patient-leaflet French, EU marketing authorization metadata, and SmPC-adjacent posology phrasing. This is a meaningful overlap with the deployment's PIL and SmPC document types, even within the constraints of the UMLS-calibrated annotation schema.

**3. Partial STS coverage for French biomedical text in CLISTER and DEFT2020**
Both CLISTER and DEFT2020 provide French-language STS tasks with graded multi-annotator labels. DEFT2020-D1 through DEFT2020-D9 confirm that drug leaflet pairs with safety instructions, contraindication language, and named INNs are represented. CLISTER-D2 confirms that drug name paraphrases appear at the 5.0 similarity level. Together these datasets establish a French biomedical STS baseline that, while miscalibrated for regulatory equivalence, provides a starting point for model selection.

**4. Negation and speculation detection across CAS and ESSAI**
Both CAS and ESSAI provide negation and speculation scope annotations over clinical text. CAS-D6, CAS-D7, ESSAI-D7, and ESSAI-D8 confirm the presence of negated clinical and contraindication-adjacent statements. This provides a partial linguistic signal for filtering negated safety conditions in a downstream pipeline, even though annotation norms are clinical rather than regulatory.

**5. Consistent French Latin-script text with no modality or script mismatches**
Every dataset (with the partial exception of PxCorpus's transcribed speech) delivers French text in standard Latin script with appropriate diacritics, consistent with the deployment environment. This is confirmed across QUAERO-D1, CLISTER-D1, ESSAI-D9, and all other datasets. No modality conversion, script normalization, or dialect adaptation is required.

---

### Cross-Cutting Weaknesses

**CRITICAL — Regulatory document genre absence across nearly all datasets**
The benchmark's content is overwhelmingly drawn from clinical case reports, research abstracts, clinical trial protocols, and spoken prescription dialogues. SmPCs, CTD modules, EU Risk Management Plans, and patent claims are either entirely absent or represented only marginally. Confirmed across: CLISTER-D11, E3C-D11, E3C-D12, DEFT2021-D7, CAS-D10, ESSAI-D12, MORFITT-D8, DIAMED-D9, MANTRAGSC-D4, FRENCHMEDMCQA-D13. QUAERO's EMEA sub-corpus (approximately 10 segmented documents across train/dev/test splits per web search findings) is the sole confirmed regulatory-genre source, and it covers PILs, not SmPCs.

**CRITICAL — STS scoring calibrated for general clinical similarity, not regulatory equivalence**
Both STS datasets (CLISTER and DEFT2020) demonstrate that their scoring rubrics treat legally material qualifier differences as near-synonymy. A 2× numerical difference in a measured value scores 4.0 in CLISTER (CLISTER-D13); dropping the qualifier "congénitale" from a contraindication scores 4.6 in DEFT2020 (DEFT2020-D18); substituting a specific substance name for a generic term scores 4.3 (DEFT2020-D20). The deployment explicitly requires that such differences be treated as critical mismatches (A3). This is a fundamental OO misalignment for the benchmark's highest-priority task in this deployment.

**CRITICAL — Regulatory entity types absent from all NER schemas**
No dataset's NER annotation schema includes INN as distinct from CHEM, ATC codes, excipient names, EMA-templated posology expressions, or contraindication qualifiers as explicit annotation targets. This is confirmed across QUAERO (QUAERO-D18, QUAERO-D19), E3C (E3C-D7, E3C-D8), MANTRAGSC (MANTRAGSC-D8), DEFT2021 (DEFT2021-D5, DEFT2021-D6), CAS (CAS-D13), and ESSAI (ESSAI-D17, ESSAI-D18). The external evidence (Kadi et al. 2025 on ATC code extraction from SmPCs) confirms this is an unresolved challenge field-wide, not merely a benchmark limitation.

**MAJOR — Annotator populations are systematically misaligned with deployment ground-truth norms**
Across all datasets with documented annotation, annotators are academic NLP researchers, clinical professionals, or automated tools — none are regulatory affairs specialists, pharmacovigilance experts, or EMA/ANSM-qualified reviewers. This is confirmed by: QUAERO-D20, CLISTER-D16, DEFT2020-D10 (annotator variance on pharmaceutical pairs), MORFITT annotation documentation, DiaMED (medical expert contributor was for ICD-10 classification, not NER or STS), and benchmark author affiliations (Q8). The deployment explicitly anticipates systematic disagreements on borderline cases (A4), which cannot be detected from the available benchmark labels.

**MAJOR — Task type misalignment for four of eleven datasets**
FrenchMedMCQA, MORFITT, DiaMED, and CAS/ESSAI (POS-only configs) produce outputs (index sets, specialty labels, ICD-10 codes, POS tag sequences) that are entirely disjoint from the deployment's NER span and STS score requirements. FRENCHMEDMCQA-D11, MORFITT-D6, DIAMED-D1, CAS-D13, ESSAI-D18 collectively illustrate that the benchmark's task inventory extends well beyond the deployment's functional requirements.

**MAJOR — Brand name vs. INN convention mismatch**
PxCorpus predominantly uses brand names rather than INNs (PXCORPUS-D19, PXCORPUS-D20), which is incompatible with EMA regulatory requirements that mandate INN primacy in SmPCs. Clinical datasets similarly mix brand and generic names. Models trained on this distribution may underperform on INN-centric regulatory text.

**MINOR — Non-EMA-jurisdiction content dilutes IC validity**
Multiple datasets contain content from African clinical contexts (DiaMED from Pan African Medical Journal, E3C-D15, E3C-D16, MANTRAGSC-D16, MORFITT-D11, MORFITT-D12, DEFT2021-D11), non-EU geographic references (DEFT2020-D14, MORFITT-D9), and non-French medical practice environments. While linguistically French, these reduce the benchmark's construct validity for EMA/ANSM-specific regulatory tasks.

**MINOR — Sentence-splitting of long regulatory documents removes document-level context**
The preprocessing applied to EMEA documents (Q37) to accommodate transformer input length constraints strips document structure (section headers, cross-references between sections) that is legally and semantically critical in SmPC and CTD compliance verification. DEFT2020-D21 and QUAERO-D22 through QUAERO-D24 illustrate decontextualized fragments that result from this process.

---

### Content Coverage Summary

**What the benchmark collectively represents:**

The benchmark's 11 datasets collectively cover French biomedical text drawn from: EMEA drug leaflets (QUAERO EMEA sub-corpus, ~10 documents), clinical case reports (CLISTER, DEFT2021, E3C, DiaMED, CAS), clinical trial protocols (ESSAI), biomedical research abstracts (MORFITT, MANTRAGSC Medline), pharmacy exam questions (FrenchMedMCQA), and spoken prescription dialogues (PxCorpus). The pharmaceutical vocabulary across these sources is broad at the lexical level, covering drug names, dosage expressions, routes of administration, and some safety-critical language.

**What is well-covered relative to deployment needs:**
- French pharmaceutical lexical field, broadly represented across multiple registers
- EMEA package leaflet (PIL) text in authentic regulatory-register French (QUAERO only)
- French biomedical STS baseline with graded multi-annotator labels (CLISTER, DEFT2020)
- Clinical entity NER schemas that partially overlap with pharmaceutical substance extraction (DEFT2021 treatment/dosage tags, QUAERO CHEM)
- French biomedical language model selection signal (benchmark-level finding from DrBERT-FS, DrBERT-CP, CamemBERT-bio performance profiles)

**What is absent or inadequately covered:**
- SmPC text (EMA Section 4.1–4.9 structure, mandatory phrasing conventions from QRD v10.4 template) — not confirmed as a data source in any dataset
- CTD module narrative sections — not confirmed in any dataset
- EU Risk Management Plan text — not confirmed in any dataset
- Regulatory-specific entity types as distinct annotation targets: INNs (vs. CHEM broadly), ATC codes, excipient names, EMA-templated posology expressions, contraindication qualifier phrases
- STS scoring calibrated for dose-threshold and contraindicated-population-qualifier sensitivity
- Annotations by regulatory affairs specialists or annotators working under EMA/ANSM guideline frameworks
- Patent claims in regulatory/IP context with INN/ATC-specific entity annotation (Mantra-GSC Patents config is low-resource and uses the same general UMLS schema)

---

### Limitations

1. **MANTRAGSC EMEA and Patents configs unsampled:** The analysis of MANTRAGSC was based entirely on fr_medline examples. The fr_emea and fr_patents configs — the most deployment-relevant configs — were not visible in the sample. Deployment fitness assessments for these configs rely on documented properties (schema, size, model performance) rather than direct inspection of instances.

2. **QUAERO MEDLINE config unsampled:** Only the EMEA config was analyzed. The MEDLINE config (biomedical article titles) was not inspected; its properties are inferred from benchmark documentation.

3. **DEFT2020 Task 2 unsampled:** Only Task 1 (STS scoring) was inspected. Task 2 (most-similar-sentence selection) was not directly observed.

4. **CLISTER and DEFT2020 annotator profiles undocumented:** Neither dataset provides annotator professional background documentation. The inference that annotators were non-regulatory specialists is based on the absence of any such documentation and on observed scoring patterns, not direct evidence.

5. **Small sample sizes relative to full datasets:** Some datasets (particularly ESSAI with 28,343 rows, CAS with 15,160 rows) were sampled at a fraction of their total size. Content distributions in unsampled portions may differ.

6. **DiaMED annotation quality partially out of scope:** The reported inter-annotator agreement (ICD-10 classification) applies to the classification task only. NER annotation quality for DiaMED is not separately assessed.

7. **No audio modality inspection:** PxCorpus's original audio recordings were not accessible; only transcribed text was analyzed. Any residual audio-related preprocessing artifacts are not assessed.

8. **IDMP compliance requirements not benchmarkable:** The EU IDMP mandatory structured data extraction obligation (ISO 11615/11616/11240/11239/11238 standards) identified in web search findings has no coverage in any DrBenchmark dataset and cannot be assessed from this benchmark.

---

### Cited Evidence

- **QUAERO-D1**: QUAERO/emea | 51 | CHEM/PROC | `"EMEA / H / C / 122 REFLUDAN Qu' est-ce que Refludan ? [...] Son principe actif est la lépirudine ."` | EMEA authorization header with brand name and INN — canonical SmPC/leaflet structure | IC
- **QUAERO-D2**: QUAERO/emea | 36 | CHEM | `"EMEA / H / C / 122 Recommandations standard Comme la lépirudine est excrétée et métabolisée en quasi-totalité par le rein"` | EMEA document header with pharmacokinetic content | IC
- **QUAERO-D3**: QUAERO/emea | 84 | O | `"EMEA / H / C / 122 4 ."` | EMEA authorization number fragment — confirms regulatory document source | IC
- **QUAERO-D4**: QUAERO/emea | 1 | CHEM | `"Phosphate de sodium , monobasique , monohydraté [...] Polysorbate 80 ( E433 ) Eau pour préparation injectable ."` | Full excipient list with E-numbers in SmPC Section 6 format | IC
- **QUAERO-D5**: QUAERO/emea | 55 | CHEM/DEVI | `"TYSABRI 300 mg solution à diluer pour perfusion natalizumab Chaque flacon de 15 ml de concentré contient 300 mg de natalizumab ( 20 mg / ml ) ; phosphate de sodium [...] polysorbate 80 ( E433 )"` | Dosage, concentration, and full excipient list in SmPC format | IC
- **QUAERO-D6**: QUAERO/emea | 34 | CHEM | `"Contient également : mannitol , hydroxyde de sodium ."` | Excipient disclosure sentence | IC
- **QUAERO-D7**: QUAERO/emea | 95 | CHEM | `"Agent antithrombotique – inhibiteur direct de la thrombine , code ATC : La lépirudine ([ Leu1 , Thr2 ]- 63 - désulfohirudine ) est une hirudine recombinante"` | ATC code reference and INN with chemical description | IC, IO
- **QUAERO-D8**: QUAERO/emea | 32 | PROC/CHEM | `"Dans les études cliniques , la dose maximale prévue de ziconotide administré par voie intrarachidienne était de 912 µg / jour après une augmentation posologique sur 7 jours ."` | Maximum dose, unit, route of administration, and titration schedule | IC
- **QUAERO-D9**: QUAERO/emea | 78 | O | `"La dose quotidienne maximale est de 21 , 6 microgrammes par jour ."` | Maximum daily dose statement — dose value receives no NER label | IC, OO
- **QUAERO-D10**: QUAERO/emea | 17 | PROC/DEVI | `"La solution diluée doit être perfusée par voie intraveineuse pendant 1 heure à un débit d' environ 2 ml / minute ."` | IV infusion rate and duration | IC
- **QUAERO-D11**: QUAERO/emea | 23 | CHEM/LIVB | `"Prialt ne doit pas être utilisé chez l' enfant ."` | Paediatric contraindication statement | IC
- **QUAERO-D12**: QUAERO/emea | 64 | DISO | `"N' utilisez jamais TYSABRI • Si vous êtes allergique ( hydpersensible ) au natalizumab [...] • Si vous êtes âgé ( e ) de moins de 18 ans ."` | Multi-condition contraindication list in patient leaflet format | IC
- **QUAERO-D13**: QUAERO/emea | 43 | CHEM | `"Par conséquent , Refludan ne doit pas être administré à la femme enceinte ou qui allaite ."` | Contraindication for pregnancy and breastfeeding | IC
- **QUAERO-D14**: QUAERO/emea | 37 | GEOG | `"La Commission européenne a délivré une autorisation de mise sur le marché valide dans toute l' Union européenne pour Tysabri à Elan Pharma International Ltd , le 27 juin 2006 ."` | EU marketing authorization reference | IC
- **QUAERO-D15**: QUAERO/emea | 50 | CHEM | `"Refludan 50 mg en poudre pour solution injectable ou pour perfusion Lepirudine Les autres composants sont le mannitol ( E 421 ) et l' hydroxyde de sodium pour l' ajustement du pH ."` | INN, brand name, and excipients all tagged as CHEM | OO
- **QUAERO-D16**: QUAERO/emea | 18 | CHEM/LIVB | `"Le natalizumab est un anticorps anti-α 4 - intégrine humanisé recombinant , produit dans une lignée cellulaire murine par génie génétique ."` | INN and biologic origin tagged under same broad CHEM/LIVB categories — no INN-specific label | OO
- **QUAERO-D17**: QUAERO/emea | 2 | CHEM/DISO | `"Une cirrhose du foie peut également affecter l' excrétion rénale de la lépirudine ."` | INN in pharmacokinetic sentence; CHEM label conflates API with other chemical entities | OO
- **QUAERO-D18**: QUAERO/emea | 78 | O | `"La dose quotidienne maximale est de 21 , 6 microgrammes par jour ."` | Specific dose value and unit are unnanotated (O tags); dosage not a labeled entity class | OO
- **QUAERO-D19**: QUAERO/emea | 32 | PROC | `"Dans les études cliniques , la dose maximale prévue de ziconotide administré par voie intrarachidienne était de 912 µg / jour"` | Max dose quantity unannotated despite critical regulatory relevance | OO
- **QUAERO-D20**: QUAERO/emea | 18 | LIVB | `"produit dans une lignée cellulaire murine par génie génétique ."` | Murine cell line tagged as LIVB; biologic/regulatory classification may differ from UMLS grouping | OC
- **QUAERO-D21**: QUAERO/emea | 64 | LIVB/DISO | `"Si vous avez des perturbations graves du système immunitaire ( dues à une maladie , telle que leucémie ou infection à VIH"` | Contraindication qualifier present but no labeled contraindication entity in schema | IO
- **QUAERO-D22**: QUAERO/emea | 41 | O | `"o ."` | Single-character fragment from sentence splitting | IC
- **QUAERO-D23**: QUAERO/emea | 83 | O | `"europa ."` | URL fragment from EMEA website reference | IC
- **QUAERO-D24**: QUAERO/emea | 118 | O | `"V ."` | Single-character token | IC
- **QUAERO-D25**: QUAERO/emea | 15 | O | `"Č eská republika Biogen Idec ( Czech Republic ) s ."` | Czech-language text embedded in French EMEA document | IC
- **QUAERO-D26**: QUAERO/emea | 117 | DISO | `"Deutschland Biogen Idec GmbH Tel : + 49 [...] Norge Biogen Idec Norway AS Tlf : + 47 [...] Eesti Richter Gedeon Eesti filiaal"` | Multilingual company contact directory embedded in French EMEA document | IC
- **FRENCHMEDMCQA-D1**: FrenchMedMCQA | 70 | multiple | "Les anti-vitamines K (AVK) sont formellement contre-indiquées avec : Le miconazole (DAKTARIN®) / Les salicylés à fortes doses" | Drug interaction contraindication question; relevant to safety warning verification | IC
- **FRENCHMEDMCQA-D2**: FrenchMedMCQA | 100 | multiple | "Parmi les formes solides orales suivantes, indiquer celle(s) qui libère(nt) le principe actif de façon continue : Matrice hydrophile / Comprimé à enrobage par film insoluble / Matrice lipophile" | Modified-release pharmaceutical forms; relevant to SmPC labeling | IC
- **FRENCHMEDMCQA-D3**: FrenchMedMCQA | 59 | multiple | "Vous devez évaluer la biodisponibilité d'un principe actif par voie orale en gélule et en comprimé. Quel(s) paramètre(s) pouvez vous comparer ?" | Pharmacokinetic concepts central to SmPC sections | IC
- **FRENCHMEDMCQA-D4**: FrenchMedMCQA | 44 | multiple | "Peut entraîner des troubles cutanés sévères type syndrome de Lyell / l'association avec le méthotrexate est contre-indiquée" | Adverse effects and contraindication content; deployment-aligned | IC
- **FRENCHMEDMCQA-D5**: FrenchMedMCQA | 105 | simple | "Une utilisation de médicament non conforme aux recommandations du résumé des caractéristiques du produit" | Explicit SmPC reference ("résumé des caractéristiques du produit"); regulatory-register content | IC
- **FRENCHMEDMCQA-D6**: FrenchMedMCQA | 50 | multiple | "Parmi les verres suivants, indiquez ceux qui peuvent être utilisés comme conditionnement réutilisable des préparations pour usage parentéral : Verre de type I / Verre borosilicaté" | Pharmaceutical container specifications for parenteral use | IC
- **FRENCHMEDMCQA-D7**: FrenchMedMCQA | 13 | multiple | "Quel est (sont) le(s) diurétique(s) qui provoque(nt) une baisse du potassium sanguin? Chlortalidone / Hydrochlorothiazide / Furosémide / Spironolactone / Amiloride" | INN-level drug names relevant to entity extraction | IC
- **FRENCHMEDMCQA-D8**: FrenchMedMCQA | 72 | multiple | "la ceftriaxone (ROCEPHINE®) / C'est une céphalosporine de 3ème génération / Son importante demi-vie d'élimination est compatible avec une seule administration quotidienne" | INN with brand name and pharmacokinetic facts relevant to posology labeling | IC
- **FRENCHMEDMCQA-D9**: FrenchMedMCQA | 2 | multiple | "La loi de Beer-Lambert / S'applique aux dosages spectrophotométriques / Est une loi additive" | Pharmaceutical analytical chemistry relevant to CTD quality modules | IC
- **FRENCHMEDMCQA-D10**: FrenchMedMCQA | 31 | multiple | "La teneur en eau des matières premières est déterminée à l'aide de la méthode de Karl Fisher" | Raw material testing method relevant to regulatory dossier quality sections | IC
- **FRENCHMEDMCQA-D11**: FrenchMedMCQA | 1 | simple | "Au cours de la leucémie lymphoïde chronique, le myélogramme montre: Une population de lymphocytes>30%" | Closed-option recall task; no NER span or STS output produced | IO, OO
- **FRENCHMEDMCQA-D12**: FrenchMedMCQA | 48 | multiple | "La distribution tissulaire des médicaments / Détermine le volume apparent de distribution / Est influencée par la liaison du médicament aux protéines plasmatiques" | Pharmacokinetics knowledge question; model output is index set, not regulatory entity | IO, OO
- **FRENCHMEDMCQA-D13**: FrenchMedMCQA | 43 | multiple | "L'économie médicale est une économie / De service de santé / Régie par la loi de l'offre et de la demande" | Health economics exam question; not regulatory document text | IC, IO
- **FRENCHMEDMCQA-D14**: FrenchMedMCQA | 61 | simple | "La certification des établissements de santé / Concerne tous les établissements de santé" | Healthcare administration exam question; outside regulatory submission genre | IC, IO
- **FRENCHMEDMCQA-D15**: FrenchMedMCQA | 8 | multiple | "La trinitrine: Est le trinitrate d'isosorbide / Est un médicament anti-angoreux" | Drug name in exam item context; not running text for NER span extraction | IC
- **FRENCHMEDMCQA-D16**: FrenchMedMCQA | 67 | multiple | "Quelle est (sont) la (les) parasitose(s) qui présente(nt) un stade hépatique? Giardiase / Paludisme / Fasciolose" | Parasitology content; no relevance to regulatory NLP tasks | IC
- **FRENCHMEDMCQA-D17**: FrenchMedMCQA | 19 | multiple | "Parmi les phénotypes suivants, quel(s) est (sont) celui (ceux) que peuvent présenter les enfants issus d'un père AB Rh positif" | Blood group genetics; clinical medicine with no regulatory application | IC
- **FRENCHMEDMCQA-D19**: FrenchMedMCQA | 40 | multiple | "le composé suivant: / Est utilisé comme antibactérien / Est utilisé comme diurétique" | References absent molecular structure figure; implicit visual content stripped | IC
- **DEFT2020-D1**: DEFT2020 | 4 | 4.0 | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter pendant la durée du traitement." | Drug leaflet breastfeeding warning; tests sensitivity to precautionary framing | IC, OO
- **DEFT2020-D2**: DEFT2020 | 18 | 4.6 | "En raison de la présence de lactose, ce médicament est contre-indiqué en cas de galactosémie congénitale, de syndrome de malabsorption du glucose et du galactose ou de déficit en lactase." | Contraindication with excipient (lactose) and qualifying term "congénitale" — scored near-equivalent to version lacking qualifier | IC, OO, OC
- **DEFT2020-D3**: DEFT2020 | 16 | 4.0 | "Ce produit peut provoquer un syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après la dernière prise de stupéfiant." | Opioid withdrawal timing safety statement; tests time-critical dosing language sensitivity | IC, OO
- **DEFT2020-D4**: DEFT2020 | 52 | 4.4 | "Comprimé rond, blanc, biconvexe, gravé 6 sur une face, une flèche étant gravée sur l'autre face." | Pharmaceutical form description from drug leaflet; formulaic SmPC-register French | IC
- **DEFT2020-D5**: DEFT2020 | 70 | 4.3 | "Prévenir les patients que la voie sublinguale constitue la seule voie efficace et bien tolérée pour l'administration de ce produit." | Administration route instruction from drug leaflet | IC
- **DEFT2020-D6**: DEFT2020 | 121 | 4.3 | "A conserver à l'abri de l'humidité." / "Ce médicament doit être conservé à l'abri de l'humidité." | Storage instruction pair; canonical SmPC formulaic phrase | IC, IF
- **DEFT2020-D7**: DEFT2020 | 23 | 4.1 | "La capécitabine a une influence mineure ou modérée sur l'aptitude à conduire des véhicules et à utiliser des machines." | Named INN (capécitabine) in driving/safety warning context | IC
- **DEFT2020-D8**: DEFT2020 | 13 | 3.6 | "Chez les patients insuffisamment équilibrés par glimepiride arrow à la dose maximale, un traitement par l'insuline peut être associé si nécessaire." | Named INN (glimepiride) with dose and treatment association; drug label register | IC
- **DEFT2020-D9**: DEFT2020 | 146 | 3.7 | "Elle impose l'arrêt du traitement et contre-indique toute nouvelle administration de clindamycine." | Contraindication with named INN (clindamycine) | IC
- **DEFT2020-D10**: DEFT2020 | 16 | 4.0 (scores=[5,2,4,4,5]) | "Ce produit peut provoquer un syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après la dernière prise de stupéfiant." | High annotator variance (range 2–5) on opioid timing safety statement | OO, OC
- **DEFT2020-D11**: DEFT2020 | 4 | 4.0 (scores=[5,2,4,4,5]) | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter pendant la durée du traitement." | Same variance pattern on breastfeeding contraindication pair | OO, OC
- **DEFT2020-D12**: DEFT2020 | 26 | 3.4 | "Pour la comparaison entre blocs neuraxiaux et anesthésie générale, nous avons évalué la qualité des preuves comme très faible pour la mortalité..." | Clinical evidence summary; formal French register | IC
- **DEFT2020-D13**: DEFT2020 | 6 | 0.4 | "Certains apiculteurs sélectionnent leurs reines afin de favoriser au mieux la production." | Beekeeping topic; entirely off-domain for pharmaceutical regulatory use case | IO, IC
- **DEFT2020-D14**: DEFT2020 | 3 | 2.1 | "Boris Fiodorovitch Godounov, en russe : Бори́с Фёдорович Годуно́в (v.1551–Moscou, 13 avril 1605)..." | Russian historical figure; irrelevant to biomedical or regulatory domain | IO, IC
- **DEFT2020-D15**: DEFT2020 | 1 | 0.5 | "Entre Perpignan et Villefranche, il subsiste de très nombreux poteaux caténaires datant des premiers essais en 12 KV 16 2/3 Hz..." | Railway catenary electrification; off-domain | IO, IC
- **DEFT2020-D16**: DEFT2020 | 5 | 4.2 | "Caudry est une commune française d'environ 15 000 habitants située dans le sud du département du Nord en région Hauts-de-France." | French commune geography; off-domain | IO, IC
- **DEFT2020-D17**: DEFT2020 | 60 | 0.8 | "Les Canadiens de Montréal sont une franchise de hockey sur glace professionnel située à Montréal dans la province de Québec au Canada." | Ice hockey franchise description; off-domain | IO, IC
- **DEFT2020-D18**: DEFT2020 | 18 | 4.6 | "...contre-indiqué en cas de galactosémie congénitale..." vs. "...ne doit pas être utilisé en cas de galactosémie..." | "Congénitale" qualifier dropped in target; scored 4.6 despite regulatory-material difference | OO, OC
- **DEFT2020-D19**: DEFT2020 | 16 | 4.0 | "...syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après..." | Time-critical dosing language; annotator variance exposes scoring unreliability | OO, OC
- **DEFT2020-D20**: DEFT2020 | 65 | 4.3 | "- Ne pas utiliser chez les personnes présentant des difficultés de déglutition en raison du risque d'inhalation bronchique et de pneumopathie lipoïde." vs. "...inhalation de la paraffine liquide..." | Specific substance name (paraffine liquide) vs. generic term (inhalation bronchique) scored 4.3 — regulatory-material difference treated as near-synonymy | OO, OC
- **DEFT2020-D21**: DEFT2020 | 40 | 3.4 | "En cas de prise le soir, il faut recommander de ne pas s'aliter dans les 2 heures suivant celle-ci et de tenir compte du délai d'action (6-8 heures)." | Posology instruction decontextualized by sentence splitting; section/drug identity lost | IF, IC
- **DEFT2020-D22**: DEFT2020 | 13 | 3.6 (scores=[5,3,3,4,3]) | "Chez les patients insuffisamment équilibrés par glimepiride arrow à la dose maximale..." | Dosage instruction pair; 2-point annotator variance on pharmaceutical content | OC
- **MORFITT-D1**: MORFITT | 19 | pharmacology | "Déterminer la stabilité physicochimique et microbiologique de suspensions de sulfadiazine (100 mg/mL)...Un test de chromatographie liquide ultra-performante a été développé et validé" | Pharmaceutical stability testing abstract; contains drug name and analytical method language adjacent to regulatory vocabulary | IC
- **MORFITT-D2**: MORFITT | 29 | veterinary | "La cyclosporine est de plus en plus utilisée en dermatologie des petits animaux...peu d'effets secondaires ont été observés aux doses utilisées en pratique" | Drug name and dosage language in a veterinary biomedical abstract | IC
- **MORFITT-D3**: MORFITT | 33 | pharmacology/chemistry | "L'absorption cutanée du calcium et du magnésium a été étudiée depuis ces différentes formulations, en utilisant la méthode des cellules de Franz" | Pharmaceutical formulation language; galenic terms (liposomes, émulsions) present | IC
- **MORFITT-D4**: MORFITT | 4 | veterinary/parasitology | "Les échanges internationaux sont responsables de la résurgence de nombreuses maladies affectant le bétail...les risques liés aux échanges varient en fonction de l'espèce" | Multi-label annotation on veterinary/parasitology cross-specialty document | OO
- **MORFITT-D5**: MORFITT | 21 | etiology/physiology/parasitology | "Bloquer le complément, notamment l'axe C5a-C5aR1, par des thérapies spécifiques représente un espoir thérapeutique dans les formes les plus sévères de la maladie" | Three-label annotation on immunological/pharmacological COVID-19 content | OO
- **MORFITT-D6**: MORFITT | 8 | microbiology | "La région du Nord-Ouest de l'Ontario présente un taux élevé...d'infections de la peau et des tissus mous causées par une souche de Staphylococcus aureus méthycillinorésistante d'origine communautaire" | Research abstract with no entity-level or similarity ground truth; supports task-type mismatch concern | IO
- **MORFITT-D7**: MORFITT | 2 | pharmacology | "Nous avons établi la sensibilité du test HS à la morphine en construisant des courbes de dose-réponse et en calculant des doses inhibitrices semi-maximales (DI 50)" | Pharmacological abstract with dosage mention but no NER annotation; confirms absence of regulatory entity labels | IC
- **MORFITT-D8**: MORFITT | 3 | etiology | "Des rats ont été assignés aléatoirement à 1 de 3 groupes : un groupe témoin (n=15), un groupe (n=15) dans lequel la pancréatite aiguë a été induite au moyen de L-arginine" | Animal experimental protocol; research abstract register, not regulatory submission language | IC
- **MORFITT-D9**: MORFITT | 13 | etiology | "En 2007 et 2008, 4 423 adultes de Calgary ont répondu à des entrevues au téléphone fixe portant sur l'activité physique" | Canadian epidemiological survey — non-EMA jurisdiction and non-regulatory genre | IC, OC
- **MORFITT-D10**: MORFITT | 19 | pharmacology | "les échantillons répondaient aux critères de pharmacopée pour la qualité microbiologique après 30 jours, mais seule la sulfadiazine formulée dans du sirop conservé à 25 ºC pouvait être utilisée après une semaine" | Drug name and stability condition present but no entity-level annotation; confirms regulatory entity gap | IC
- **MORFITT-D11**: MORFITT | 31 | psychology | "Perceptions, attitudes et pratiques vis-à-vis de la recherche chez des médecins internes en formation en Arabie saoudite" | Saudi Arabian medical training context; outside EMA/ANSM regulatory scope | IC, OC
- **MORFITT-D12**: MORFITT | 22 | psychology | "Le questionnaire final en arabe (YFAS 2.0-A)...a été rempli par 236 étudiants de médecine égyptiens" | Egyptian Arabic-language study; non-French, non-EMA regulatory context | IC, OC
- **MORFITT-D13**: MORFITT | 20 | etiology | "79 patients au total ont été recrutés à Amman (Jordanie) en 2015" | Jordanian clinical context; outside EU regulatory jurisdiction | IC, OC
- **MORFITT-D14**: MORFITT | 9 | veterinary/microbiology | "L'otite externe est une maladie multifactorielle fréquente chez le chien...Décrire le microbiote bactérien auriculaire des chiens avec otite externe" | Veterinary microbiology abstract; irrelevant to human pharmaceutical regulatory filings | IC, IO
- **MORFITT-D15**: MORFITT | 5 | immunology/veterinary | "Par rapport aux connaissances sur la biologie du surfactant chez les rongeurs et les humains, seules des données limitées sont disponibles sur le surfactant chez le cheval" | Equine pulmonary physiology research; veterinary content irrelevant to deployment | IC
- **CLISTER-D1**: CLISTER | 85 | 4.0 | "Le bilan rénal a objectivé une insuffisance rénale avec une créatininémie à 1440 μmol/l, soit une clairance de la créatinine à 6,7 ml/mn/m2" | Clinical French with quantitative biomedical values; confirms domain register | IC, IF
- **CLISTER-D2**: CLISTER | 163 | 5.0 | "Le patient subissait une chimiothérapie par Méthotrexate - Vinblastine - Endoxan -Cisplatine par voie / Le patient bénéficiait d'une chimiothérapie par voie systémique à base de Métotrexate-Vinblastine-Endoxan Cisplatine." | Near-paraphrase with drug names; relevant to pharmaceutical STS | IC
- **CLISTER-D3**: CLISTER | 41 | 2.0 | "Métoprolol 50 mg deux fois par jour; / Metformine 500 mg, 1 comprimé deux fois par jour" | Dosage expressions for two different drugs; partial pharmaceutical content | IC
- **CLISTER-D4**: CLISTER | 98 | 2.0 | "Acide folinique 15 mg une fois par jour / Aspirine 80 mg, 1 comprimé une fois par jour" | Named drugs with dosage forms; limited regulatory relevance | IC
- **CLISTER-D5**: CLISTER | 168 | 1.0 | "On augmente la dose de phénytoïne à 350 mg par voie intraveineuse une fois par jour. / La dose maximale de mirtazapine devrait être de 30 mg par jour ou exceptionnellement 45 mg par jour." | Posology expressions with route of administration; different drugs, hence low similarity | IC
- **CLISTER-D6**: CLISTER | 5 | 2.75 | "Le reste de l'examen échographique ne trouvait aucune autre anomalie. / Le reste de l'examen somatique était sans anomalie." | Intermediate similarity for structurally parallel clinical statements | OO
- **CLISTER-D7**: CLISTER | 10 | 5.0 | "Une mastectomie était réalisée avec curage axillaire. / Une mastectomie avec curage axillaire ont été réalisés." | Near-identical procedural description scored 5.0; confirms scale calibration | OO
- **CLISTER-D8**: CLISTER | 37 | 5.0 | "Les limites d'exérèse étaient saines. / Les marges chirurgicales étaient saines." | Lexical synonymy correctly scored 5.0 | OO
- **CLISTER-D9**: CLISTER | 22 | 4.0 | "Les suites postopératoires étaient simple. / Les suites postopératoires immédiates étaient simples." | Minor addition of 'immédiates' reduces score to 4.0; good sensitivity to additions | OO
- **CLISTER-D10**: CLISTER | 188 | 4.0 | "L'AHG urinaire est à 10 mmol/l. / L'AHG urinaire est à 20 mmol/l." | Same test, 2× numerical difference → 4.0; regulatory context would flag this as critical mismatch | OO, OC
- **CLISTER-D11**: CLISTER | 6 | 0.0 | "La patiente a eu, dans le même temps opératoire, une lithotritie balistique du calcul par voie endoscopique permettant de dénuder le DIU puis de l'extraire par une pince à corps étranger." | Clinical case narrative with materiovigilance reference; not regulatory template prose | IC
- **CLISTER-D12**: CLISTER | 3 | 3.0 | "Au cours de l'administration du sac no 3, une réaction urticarienne est survenue. / Début de l'administration du sac no 2 aux soins intensifs" | Hospital ICU administration narrative; clinical not regulatory register | IC
- **CLISTER-D13**: CLISTER | 188 | 4.0 | "L'AHG urinaire est à 10 mmol/l. / L'AHG urinaire est à 20 mmol/l." | 2× numerical difference in measured value scored near-equivalent; problematic for dose-threshold regulatory use | OO, OC
- **CLISTER-D14**: CLISTER | 149 | 0.5 | "Lithium 300 mg x x x x x x x x x x x x x x x x / 300 mg IV aux 24 h x x x x x x x x x x x x x x x x" | Structured data rows with dosage; scoring reflects formatting noise, not regulatory semantics | OO, IC
- **CLISTER-D15**: CLISTER | 181 | 4.0 | "Jour 32 30,60 12,0 1,19 - - - - - - 25 μg 0,4 mg / Jour 81 1,81 20,4 1,68 - - - - - - 25 μg 0,4 mg" | Tabular clinical measurement rows with different numeric values scored 4.0 | OO, OC
- **CLISTER-D16**: CLISTER | 83 | 4.0 | "Le sevrage sera obtenu lors d'une hospitalisation au Centre Antipoison de Marseille, avec baisse progressive des doses quotidiennes. / Un sevrage sera effectué après 12 jours d'hospitalisation au Centre Antipoison de Marseille." | Duration detail (progressive vs. 12 days) scored 4.0; regulatory annotator might score lower | OC
- **CLISTER-D17**: CLISTER | 222 | 0.0 | "CMV : cytomegalovirus; DCI : dénomination commune internationale; HTAP : hypertension artérielle pulmonaire; NR : non renseigné" | Abbreviation list including DCI (INN); incidental only, not a regulatory entity comparison | IC
- **CLISTER-D18**: CLISTER | 8 | 1.0 | "Jour 45 - - - - - - - - - 25 μg 0,4 mg / Jour 53 15,13 12,0 1,58 - - - - - - 25 μg 0,4 mg" | Partially filled clinical table rows; STS scoring semantics unclear for structured data | IC, OF
- **CLISTER-D19**: CLISTER | 191 | 2.0 | "5 mg PO Q 4H PRN X / 10 mg PO Q 4H PRN X X" | Dosage notation in French/English abbreviation format; atypical of formal regulatory prose | IC
- **CLISTER-D20**: CLISTER | 27 | 2.0 | "A.E..., âgé de 22 ans, sans antécédents pathologiques particuliers, était admis en urgence le 15 janvier 1982 pour douleur lombaire aigue droite et état de choc." | Informal clinical narrative from 1982; register diverges from formal EMA/ANSM legal prose | IC
- **MANTRAGSC-D1**: MANTRAGSC (fr_medline) | 45 | CHEM | `"testostérone ... prolactine"` | Hormone names annotated as CHEM entities; partial overlap with pharmaceutical substance categories | IC, OO
- **MANTRAGSC-D2**: MANTRAGSC (fr_medline) | 36 | CHEM | `"Traitement des méningites purulentes de l'enfant par Cefotaxime."` | Drug name `Cefotaxime` annotated as CHEM; only drug-name NER example in sample | IC, OO
- **MANTRAGSC-D3**: MANTRAGSC (fr_medline) | 50 | CHEM | `"Examen d'un comateux et recherche de critères d'action des substances dites de réveil."` | Generic substance reference annotated as CHEM; illustrates broad, non-INN-specific CHEM tagging | OO
- **MANTRAGSC-D4**: MANTRAGSC (fr_medline) | 1 | DISO | `"Luxation antérieure ouverte post-traumatique de la hanche chez l'enfant. A propos d'un cas et revue de la littérature."` | Orthopedic case report title; clinical research register, not regulatory document genre | IC, IO
- **MANTRAGSC-D5**: MANTRAGSC (fr_medline) | 3 | DISO/LIVB | `"Paraparésie fébrile chez une Tunisienne: spondylite à cryptocoque avec atteinte médullaire."` | Clinical case abstract; research register distant from EMA/ANSM regulatory prose | IC
- **MANTRAGSC-D6**: MANTRAGSC (fr_medline) | 41 | DISO | `"L'épidémie de choléra du Sultanat de Goulfey. (Nord-Cameroun: Mai-Juin 1971."` | North Cameroon epidemiology report; geographically and generically distant from EU regulatory deployment | IC
- **MANTRAGSC-D7**: MANTRAGSC (fr_medline) | 2 | DISO | `"Les manifestations oculo-palpébrales du syndrome de Lyell et du syndrome de Stevens-Johnson."` | Disease syndrome names as DISO entities; no pharmaceutical/regulatory entity annotation | OO
- **MANTRAGSC-D8**: MANTRAGSC (fr_medline) | 36 | CHEM/DISO | `"Traitement des méningites purulentes de l'enfant par Cefotaxime."` | Single drug name present in 70-example sample; no dosage, route, or contraindication context annotated | IC, OO
- **MANTRAGSC-D9**: MANTRAGSC (fr_medline) | 18 | DEVI/PROC | `"Les pompes à perfusion parentérale: description et étude comparative."` | Device terminology (DEVI); not pharmaceutical regulatory entity types like posology or excipient | OO
- **MANTRAGSC-D10**: MANTRAGSC (fr_medline) | 10 | PROC | `"Le problème de la régulation des naissances: aspects médico-légaux et médico-sociaux."` | Academic discussion framing; register incompatible with EU regulatory submission documents | IC, IO
- **MANTRAGSC-D11**: MANTRAGSC (fr_medline) | 63 | PROC | `"De la complexité d'une prise en charge humaniste dans les structures de soins."` | Reflective clinical prose; no resemblance to SmPC posology section language | IC
- **MANTRAGSC-D12**: MANTRAGSC (fr_medline) | 52 | PROC | `"La chromatographie d'affinité en épuration extra-corporelle ou pour la séparation de molécules d'intérêt biologique: contraintes techniques et réglementaires."` | Scientific methodology abstract; "réglementaires" appears as O-tag, not a labeled regulatory entity | IC, OO
- **MANTRAGSC-D13**: MANTRAGSC (fr_medline) | 60 | O (all) | `"Apparition et maintien de cycles sexuels non saisonniers chez le canard domestique placé pendant plus de trois ans à l'obscurite totale."` | Entirely O-tagged; illustrates low entity density reducing training signal | OF
- **MANTRAGSC-D14**: MANTRAGSC (fr_medline) | 66 | O (all) | `"De la relativité du risque."` | Entirely O-tagged; further illustrates sparse annotation in Medline titles | OF
- **MANTRAGSC-D15**: MANTRAGSC (fr_medline) | 45 | CHEM | `"Effet de la testostérone sur la sécrétion de prolactine."` | Both `testostérone` and `prolactine` tagged identically as CHEM; INN vs. endogenous substance distinction absent | OO, OC
- **MANTRAGSC-D16**: MANTRAGSC (fr_medline) | 43 | DISO | `"Tétanos localisé (à propos de 19 cas observés à Dakar)"` | Sub-Saharan African clinical context; outside EMA/ANSM regulatory jurisdiction | IC
- **MANTRAGSC-D17**: MANTRAGSC (fr_medline) | 41 | DISO | `"L'épidémie de choléra du Sultanat de Goulfey. (Nord-Cameroun: Mai-Juin 1971."` | North Cameroon 1971 epidemiology; temporally and geographically distant from EU regulatory context | IC
- **E3C-D1**: E3C French_clinical | 79 | all O | "Le patient était mis sous anti bacillaires associant Isoniazide 5mg/kg, Rifampicine 10 mg/kg, Ethambutol 25 mg/kg et Pyrazinamide 30 mg/kg" | Four INN drug names with weight-based dosages appear but are unlabeled | IC
- **E3C-D2**: E3C French_clinical | 62 | all O | "d'amoxicilline-acide clavulanique à 3g/j, de moxifloxacine à 400 mg/j et de métronidazole à 1,5 g/j" | Drug names with dose/frequency expressions, all labeled O | IC
- **E3C-D3**: E3C French_clinical | 53 | partial labels | "mis sous antibiothérapie à large spectre (imipenème-vancomycine) et sous catécholamines (noradrénaline)" | INN drug names in parenthetical format, similar to regulatory conventions; unlabeled | IC
- **E3C-D4**: E3C French_clinical | 103 | all O | "par du fentanyl (3µg/kg) et de l'étomidate (0,2mg/kg)" | INN + dosage with units pattern; unlabeled despite pharmaceutical relevance | IC
- **E3C-D5**: E3C French_clinical | 39 | disease entities only | "traitement immunosuppresseur à base de ciclosporine, d'evérolimus et de corticoïdes" | Multiple INN-class drugs present; labeled O while disease entities receive tags | OO, IC
- **E3C-D6**: E3C French_clinical | 59 | all O | "thrombolyse intraveineuse par ténectéplase 50 mg (10000 UI)" | Drug name + dose + unit expression; entirely unlabeled | OO
- **E3C-D7**: E3C French_clinical | 79 | all O | "Isoniazide 5mg/kg, Rifampicine 10 mg/kg, Ethambutol 25 mg/kg et Pyrazinamide 30 mg/kg pendant deux mois" | Confirmatory of D1: INN drugs + dosages all O-tagged | OO
- **E3C-D8**: E3C French_clinical | 62 | all O | "amoxicilline-acide clavulanique à 3g/j, de moxifloxacine à 400 mg/j et de métronidazole à 1,5 g/j" | Confirmatory of D2: clinical pharmacological entities absent from label space | OO
- **E3C-D9**: E3C French_clinical | 39 | mixed | "ciclosporine, d'evérolimus et de corticoïdes" unlabeled; "insuffisance rénale modérée" labeled CLINENTITY | Annotation prioritizes disease over drug entities | OC
- **E3C-D10**: E3C French_clinical | 112 | all O | "Le traitement de cotrimoxazole était arrêté" | Drug name cotrimoxazole receives no annotation | OO
- **E3C-D11**: E3C French_clinical | 20 | mixed | "Nous rapportons ici le cas d'une patiente de 89 ans aux antécédents d'une diverticulose du sigmoïde" | Canonical clinical case reporting register, not regulatory prose | IO
- **E3C-D12**: E3C French_clinical | 34 | mixed | "Patiente âgée de 35 ans, sans antécédents pathologiques notables, présentant depuis un an une masse abdominale" | Patient case history register structurally unlike SmPC language | IO
- **E3C-D13**: E3C French_clinical | 1 | mixed | "cholestase (bilirubine totale a` 140 mmol/L, bilirubine conjugue à 80 mmol/L, phosphatases alcalines à 700 UI/L)" | Lab values unannotated; disease term labeled; regulatory numerical patterns ignored | OC
- **E3C-D14**: E3C French_clinical | 39 | mixed | "ciclosporine, d'evérolimus et de corticoïdes … insuffisance rénale … anémie … hypertension artérielle" | Disease entities labeled, drug names not — clinical vs. regulatory annotator priority gap | OC
- **E3C-D15**: E3C French_clinical | 90 | all O | "Il s'agit de la série de CM la plus importante rapportée en Afrique noire" | Geographic reference to sub-Saharan Africa; non-EU clinical context | IC
- **E3C-D16**: E3C French_clinical | 70 | mixed | "Monsieur F M âgé de 70 ans, originaire du Maroc" | North African patient origin; French text but non-EMA/ANSM jurisdictional context | IC
- **E3C-D17**: E3C French_clinical | 59 | all O | "thrombolyse intraveineuse par ténectéplase 50 mg (10000 UI) vers 14h20, soit 2h20 après le début de l'apparition des symptômes" | Rich pharmaceutical content entirely unannotated | OO
- **E3C-D18**: E3C French_clinical | 79 | all O | "Isoniazide 5mg/kg, Rifampicine 10 mg/kg, Ethambutol 25 mg/kg et Pyrazinamide 30 mg/kg" | Four drug names with doses; zero positive labels despite pharmaceutical content | OO
- **PXCORPUS-D1**: PxCorpus | 5 | medical_prescription | "primperan 10 milligrammes comprimés 1 comprimé en cas de nausée toutes les 8 heures pendant 14 jours" | Full prescription utterance with drug, dose, form, frequency, indication | IC, OO
- **PXCORPUS-D2**: PxCorpus | 99 | medical_prescription | "amlodipine 5 milligrammes 1 comprimé le soir pendant 1 mois" | INN drug name with standard posology | IC
- **PXCORPUS-D3**: PxCorpus | 145 | medical_prescription | "lévothyroxine sodique 50 microgrammes 1 comprimé à prendre le matin à jeun pendant 6 semaines" | INN + salt qualifier + fasting instruction | IC
- **PXCORPUS-D4**: PxCorpus | 43 | medical_prescription | "uvedose 100 mille ui 1 fois à renouveler selon la sévérité de la carence traitement pour 3 semaines" | Conditional renewal instruction; posology diversity | IC
- **PXCORPUS-D5**: PxCorpus | 4 | replace | "attention il s'agit de 20 milligrammes et pas 10 milligrammes" | Dose-correction utterance; relevance to inconsistency detection | IC, IO
- **PXCORPUS-D6**: PxCorpus | 100 | medical_prescription | "oramorph 20 milligrammes par millilitres 5 gouttes en cas de douleur ne pas dépasser 6 gouttes par jour" | Maximum dose constraint; safety-critical posology | IC
- **PXCORPUS-D7**: PxCorpus | 8 | replace | "remplacer 1 comprimé tous les jours par 1 comprimé en cas d'anxiété" | Explicit regimen replacement; analogous to document revision flagging | IO, OO
- **PXCORPUS-D8**: PxCorpus | 6 | negate | "supprimer à midi tous les jours" | Cancellation of scheduled dose | IO
- **PXCORPUS-D9**: PxCorpus | 137 | medical_prescription | "imigrane 6 milligrammes par 0,5 milligrammes solution injuctable pour voie sous-cutanée en seringue préremplie" | Route of administration and formulation vocabulary | IC, IF
- **PXCORPUS-D10**: PxCorpus | 150 | medical_prescription | "discotrine 10 milligrammes patch 1 patch le matin au réveil retirer le patch le soir pendant 1 mois" | Application timing instruction matching patient leaflet style | IC
- **PXCORPUS-D11**: PxCorpus | 88 | none | "i'll agree come on say avec successes merde je vais roulé faut lui faire un et mettre la rame en mode français" | English fragments, expletives, off-task speech; absent from regulatory text | IC, IF
- **PXCORPUS-D12**: PxCorpus | 10 | negate | "ne pas tenir compte à midi tous les jours merd/" | Spoken disfluency with truncated expletive | IF
- **PXCORPUS-D13**: PxCorpus | 207 | medical_prescription | "teralithe 250 milligrammes / le serveur de dialogue met beaucoup de temps à comprendre votre énoncé veuillez reformuler différemment" | System error message transcribed as text; impossible in written regulatory documents | IC, IF
- **PXCORPUS-D14**: PxCorpus | 3 | none | "/chet" | Unintelligible transcription artifact | IF
- **PXCORPUS-D15**: PxCorpus | 210 | medical_prescription | "kardegic 160 milligrammes 1 sachet par jour pendant 1 mois si absence d'ulcère" | Contraindication qualifier ("si absence d'ulcère") tagged O; not in NER schema | OO, IC
- **PXCORPUS-D16**: PxCorpus | 172 | medical_prescription | "en cas d'oubli de la prise de leeloo prendre dès que possible de l'ellaone 30 milligrammes 1 comprimé si rapport à risque moins de 120 heures" | Time-critical safety conditional not annotated as regulatory entity | OO
- **PXCORPUS-D17**: PxCorpus | 4 | replace | "attention il s'agit de 20 milligrammes et pas 10 milligrammes" | One of ~3 replace examples; class severely underrepresented | OO, OF
- **PXCORPUS-D18**: PxCorpus | 12 | replace | "non prendre 150 milligrammes par jour" | Second replace example; reinforces sparsity concern | OO
- **PXCORPUS-D19**: PxCorpus | 91 | medical_prescription | "prozac 20 milligrammes 1 gélule matin et soir pendant 1 mois" | Brand name (Prozac) used instead of INN (fluoxétine); regulatory mismatch | IC, OO
- **PXCORPUS-D20**: PxCorpus | 16 | medical_prescription | "lexomil 6 milligrammes 1 demi-comprimé matin midi et soir pendant 1 semaine" | Brand name (Lexomil) only; INN (bromazépam) absent | IC
- **PXCORPUS-D21**: PxCorpus | 34 | medical_prescription | "3 mois" | Duration fragment with no drug context; degenerate example | IC
- **PXCORPUS-D22**: PxCorpus | 54 | none | "ouah" | Interjection with no pharmaceutical content | IC
- **PXCORPUS-D23**: PxCorpus | 68 | none | "race" | Single-word non-pharmaceutical token | IC
- **DIAMED-D1**: DiaMED | 1 | A00-B99 | "Le traitement était basé sur les antirétroviraux (Stavudine (D4T), Lamuvidine (3TC), Efavirenz (EFV)) et une chimiothérapie (Doxorubicine 50 mg/j en cure tous les 19 jours puis Tamoxifène)" | Drug names with dosage in clinical narrative; informal INN/abbreviation hybrid, not EMA-standardized SmPC format | IC
- **DIAMED-D2**: DiaMED | 2 | C00-D49 | "un aspect de réponse sur quelques lésions hépatiques... la sérotonine et la chromogranine plasmatique avaient légèrement diminué" | Oncology case with biomarker measurements; pharmacological content in clinical register | IC
- **DIAMED-D3**: DiaMED | 3 | D50-D89 | "keywords: ['Rate', 'abdomen aigu', 'scanner abdominal', 'chirurgie', 'Maroc']" | North African clinical context; not EU regulatory domain | IC
- **DIAMED-D4**: DiaMED | 4 | E00-E89 | "L'étude génétique a été proposée pour la famille... mais n'a pas été réalisée par faute de moyens" | Resource-constrained African clinical context irrelevant to EMA/ANSM regulatory workflows | IC
- **DIAMED-D8**: DiaMED | 8 | H60-H95 | "Le traitement a consisté en de l'amphotéricine B par voie intraveineuse pendant 2 semaines avec relais par l'itraconazole par voie orale pendant 10 semaines" | Antifungal treatment with route/duration; closest approach to posology expression in dataset, still clinical narrative register | IC
- **DIAMED-D9**: DiaMED | 9 | I00-I99 | "Communication interventriculaire ischémique: à propos d'un cas observé dans le service de cardiologie du CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" | Sub-Saharan African hospital case; outside EU regulatory jurisdiction and register | IC
- **DIAMED-D12**: DiaMED | 12 | L00-L99 | "le diagnostic de toxidermie médicamenteuse type nécrolyse épidermique toxique ou syndrome de Lyell a été évoqué devant l'apparition de décollements bulleux" | Drug-induced toxic epidermal necrolysis case; pharmacovigilance-adjacent content but in clinical narrative form with no regulatory annotation | IC, OC
- **DEFT2021-D1**: DEFT2021 | 3 | ner_tags=[...21,21,...] | `"on a décidé de devancer la prémédication de diphenhydramine et de méthylprednisolone"` | Drug names annotated as treatment entities; partial pharmaceutical entity coverage | IC, IO
- **DEFT2021-D2**: DEFT2021 | 80 | ner_tags=[...21,...] | `"la patiente était mise sous traitement anti-bacillaire à base de rifampicine – isoniazide – pyrazinamide pendant 6 mois"` | Multiple drug names and treatment duration annotated; supports basic pharmaceutical NER | IC
- **DEFT2021-D3**: DEFT2021 | 81 | ner_tags=[...21,5,6,...] | `"doxorubicine 37,5 mg / m2 / dose en association avec le cisplatin à raison de 60 mg / m2 / dose"` | Dense drug+dosage annotation; closest to posology expression style but in clinical case register | IC, IO
- **DEFT2021-D4**: DEFT2021 | 158 | ner_tags=[...21,22,22,22,22,22,...] | `"La crème de nystatin a été remplacée par une crème de diproprionate de bétaméthasone à 0,05 %, en application topique deux fois par jour pendant dix jours"` | Route of administration and frequency present; resembles drug leaflet posology but not encoded as separate entity types | IC, OO
- **DEFT2021-D5**: DEFT2021 | 55 | ner_tags=[...21,5,6,13,...21,5,6,13,14,11,12,...] | `"Hydrocortisone 300 mg IV immédiatement ; Traitement Hydroxyzine 25 mg par voie orale toutes les 6 heures au besoin"` | Drug + dose + route annotated; no separate contraindication or patient-population qualifier entity type | IC, OO
- **DEFT2021-D6**: DEFT2021 | 158 | ner_tags=[...21,22,22,22,22,22,0,0,13,14,11,12,...] | `"diproprionate de bétaméthasone à 0,05 %, en application topique deux fois par jour"` | Combined treatment span; INN, concentration, route, frequency not decomposed as separate regulatory entity types | OO
- **DEFT2021-D7**: DEFT2021 | 53 | ner_tags=[0,...] | `"Nous rapportons l'observation d'un patient de 70 ans, sans antécédent qui a consulté aux urgences dans les suites immédiates d'une agression par un pit-bull"` | Narrative case report prose; entirely different register from EU regulatory SmPC | IC, IO
- **DEFT2021-D8**: DEFT2021 | 28 | ner_tags=[...17,18,...] | `"un carcinome vésical droit, de 3 cm de diamètre, infiltrant (grade II, pT2)"` | Clinical pathology staging; not regulatory entity phrasing | IC
- **DEFT2021-D9**: DEFT2021 | 7 | ner_tags=[...21,7,8,8,...] | `"le patient est sorti au 5ème jour sous cotrimoxazole pour 10 jours"` | Drug + duration tagged; annotation does not distinguish regulatory posology encoding | OC
- **DEFT2021-D10**: DEFT2021 | 127 | ner_tags=[...17,...17,18,...17,18,18,18,...] | `"était suivi depuis cinq ans pour un myélome, une polyarthrite rhumatoïde, et une amylose rectale et rénale"` | MeSH disease category annotation; no alignment to ATC/EMA regulatory classification | OO
- **DEFT2021-D11**: DEFT2021 | 166 | ner_tags=[0,...] | `"une douleur pubienne irradiant au pénis, survenue au retour d'un voyage à Madagascar"` | Tropical disease/travel context; non-EU patient population context | IC
- **CAS-D1**: DrBenchmark/CAS | 33 | pos | "la malade était incluse dans le protocole lmb 02 comportant une 1re cure de cop ( cyclophosphamide , vincristine et prednisone )" | Full chemotherapy protocol with multiple drug INNs | IC
- **CAS-D2**: DrBenchmark/CAS | 63 | pos | "remplacer les lavements de pentasa ® par du proctocort ® ( hydrocortisone acétate 90 mg : 1 lavement tous les soirs )" | Branded + INN drug names with dosage and frequency | IC, OO
- **CAS-D3**: DrBenchmark/CAS | 22 | pos | "administration d' une ampoule de digoxine en intraveineuse" | Drug name with route of administration | IC
- **CAS-D4**: DrBenchmark/CAS | 49 | pos | "en postopératoire la malade a été traitée à la norfloxacine" | Drug INN in clinical treatment context | IC
- **CAS-D5**: DrBenchmark/CAS | 29 | pos | "elle est suivie de 887 , 5 mg ( 12 , 5 mg / kg / h ) administrée sur quatre heures" | Weight-based dosing with units — posology extraction target | IC
- **CAS-D6**: DrBenchmark/CAS | 14 | pos | "les ovaires ne montraient pas d' anomalie" | Negation of clinical finding, structurally relevant to negated contraindications | IO, OO
- **CAS-D7**: DrBenchmark/CAS | 21 | pos | "ne montrait aucune lésion focale" | Negation structure analogous to safety exclusions | OO
- **CAS-D8**: DrBenchmark/CAS | 9 | pos | "anémie à 5 , 7 g / 100ml d' hb , une hyponatrémie à 128 meq / l" | Numeric value-unit pairs, relevant to dosage patterns | IC
- **CAS-D9**: DrBenchmark/CAS | 54 | pos | "la valeur limite d' exposition autorisée était de 450 ppm soit 2 500 mg / m 3" | Exposure limit with units — closest example to regulatory threshold language | IC
- **CAS-D10**: DrBenchmark/CAS | 15 | pos | "Il s' agit d' une patiente âgée de 54 ans ayant des facteurs de risque de transmissions virales hépatiques" | Canonical clinical case narrative opening — not regulatory register | IC
- **CAS-D11**: DrBenchmark/CAS | 47 | pos | "vous êtes appelés au secours d' une infirmière de nuit pour confusion chez un patient bronchopathe chronique" | Teaching case scenario — informal register absent from regulatory documents | IC, IO
- **CAS-D12**: DrBenchmark/CAS | 88 | pos | "docteur , je suis complètement crevée depuis 5 jours , j' ai des courbatures partout" | Patient direct speech — colloquial register entirely absent from regulatory prose | IC
- **CAS-D13**: DrBenchmark/CAS | 95 | pos | "un traitement empirique de méropénème et de doxycycline est introduit" | Drug INNs present but annotated only for POS, not regulatory entities | OO, OC
- **CAS-D14**: DrBenchmark/CAS | 80 | pos | "Cholstat ® 0.1 ." | Branded drug with dose fragment — no regulatory entity annotation | OO
- **ESSAI-D1**: ESSAI | 9 | pos | "L' acétate d' abiratérone ou l' enzalutamide sont des traitements assez récents et ainsi appelés « hormonothérapies de nouvelle génération »." | Contains approved INNs (abiraterone, enzalutamide) and treatment class; supports IC strength | IC
- **ESSAI-D2**: ESSAI | 36 | pos | "Vous recevrez en parallèle la chimiothérapie classique du mésothéliome pleural avec l' association pemetrexed et cisplatine ou carboplatine , jusqu' à 6 cycles ." | Multiple INNs + cycle count + combination regimen; supports IC strength | IC
- **ESSAI-D3**: ESSAI | 37 | pos | "Tous les patients recevront une combinaison de deux immunothérapies : un anticorps anti-CTLA-4 ( ipilimumab ) et un anticorps anti-PD-1 ( nivolumab ) ." | INN names with mechanism labels; relevant to drug entity extraction | IC
- **ESSAI-D4**: ESSAI | 47 | pos | "L' ENTO ou le placébo est donné par voie orale 2 fois par jour , pour une durée de 48 semaines ." | Route, frequency, duration posology expression; supports IC strength | IC
- **ESSAI-D5**: ESSAI | 48 | pos | "Chacun de ces médicaments est administré en intraveineuse toutes les 2 semaines sur une durée de 30 mn ." | IV route + schedule + duration; posology coverage | IC
- **ESSAI-D6**: ESSAI | 6 | pos | "Tous les patients inclus dans cette étude recevront ce traitement qui sera administré toutes les deux semaines sous forme de perfusion d' une heure ." | Dosing schedule and infusion form | IC
- **ESSAI-D7**: ESSAI | 40 | pos | "Les patients avec cancer biliaire non antérieurement traité par chimiothérapie en situation avancée et ne présentant pas de contre-indication aux traitements de l' étude seront randomisés…" | Negated contraindication phrase; relevant to negation/safety extraction | OO, OC
- **ESSAI-D8**: ESSAI | 31 | pos | "Cependant , une large proportion des patients n' est pas apte à recevoir une chimiothérapie à base de cisplatine associée à la radiothérapie du fait de leur âge…" | Negated eligibility with named INN; negation in clinical trial context | OO
- **ESSAI-D9**: ESSAI | 46 | pos | "Étant donné le rôle émergent des lymphocytes B dans la GVH chronique … l' ENTO , avec une action dose-effet , permet d' induire l' apoptose ex vivo…" | Highly technical immunology prose; confirms professional French biomedical register | IF
- **ESSAI-D10**: ESSAI | 2 | pos | "Le MEDI9197 est injecté en intra-tumoral tous les 28j ( 4 semaines ) ." | Experimental compound code with dosing schedule | IC
- **ESSAI-D11**: ESSAI | 42 | pos | "Le BMS-986179 sera administré par voie veineuse toutes les semaines ." | Drug code with IV route and frequency | IC
- **ESSAI-D12**: ESSAI | 3 | pos | "Un tirage au sort deux tiers / un tiers répartira les patientes dans les deux bras de l' étude : 2 patientes sur 3 auront accès à la nouvelle molécule…" | Randomization arm description; absent genre in regulatory labeling | IO
- **ESSAI-D13**: ESSAI | 25 | pos | "Vous serez vu en consultation avant de débuter le traitement puis après 8 jours , après 15 jours de traitement…" | Patient-addressed visit schedule; not a regulatory labeling construct | IO, IC
- **ESSAI-D14**: ESSAI | 71 | pos | "Ce traitement bénéficie d' une autorisation de mise sur le marché pour les tumeurs de même nature mais de point de départ digestif ." | Mentions marketing authorization contextually, not in SmPC template structure | IC
- **ESSAI-D15**: ESSAI | 64 | pos | "Le LY3200882 est un médicament qui inhibe spécifiquement le TGF-beta…" | Experimental code, not approved INN; no ATC code | IC, OO
- **ESSAI-D16**: ESSAI | 8 | pos | "Ce nouveau traitement , APR 246 est un médicament ciblant spécifiquement la protéine p53…" | Developmental compound, not regulatory nomenclature | IC
- **ESSAI-D17**: ESSAI | 34 | pos | "Patients reçoivent AZACYTIDINE seule ou AZACYTIDINE associée à un inhibiteur spécifique des formes ." | INN present but no ATC code, excipient, or EMA posology template | IC, OO
- **ESSAI-D18**: ESSAI | 10 | pos | "Son avantage est de réduire les effets indésirables tout en continuant la même dose intensité ." | "effets indésirables" and "dose intensité" present but only POS-tagged, not entity-labelled | OO, OF
- **ESSAI-D19**: ESSAI | 5 | pos | "Cette étude sera sa première évaluation chez l' homme et aura pour objectifs de déterminer la dose optimale du médicament…" | Dose-relevant phrase POS-tagged only, no entity annotation | OO
- **ESSAI-D20**: ESSAI | 29 | pos | "De nouveaux médicaments capables d' inhiber ces anomalies pourraient être actifs dans ce cas ." | Modal "pourraient" marks clinical speculation; different legal status in regulatory labeling | OO, OC
- **ESSAI-D21**: ESSAI | 15 | pos | "Une efficacité de cet agent a été rapportée dans quelques cas de carcinomes thymiques , justifiant la présente étude ." | Hedged efficacy claim in trial justification, not regulatory indication format | OO
- **ESSAI-D22**: ESSAI | 21 | pos | "Il s' adresse aux patients atteints de cancer de la prostate , de cancer du sein , de cancer du poumon ." | Representative oncology-heavy topic distribution | IC
- **ESSAI-D24**: ESSAI | 26 | pos | "Vous serez vus en consultation régulièrement pour évaluer la tolérance et l' efficacité du traitement à l' essai ." | Patient-addressed register; not aligned with SmPC prose | IF, IC
- **ESSAI-D25**: ESSAI | 20 | pos | "Le choix de ton traitement est guidé par les anomalies des gènes de ta maladie…" | Informal "ton/ta" address; highly atypical of EU regulatory prose | IF
