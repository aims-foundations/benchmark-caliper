## Dataset Analysis Report

**Benchmark:** DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Domain
**Datasets analyzed:** 11 datasets — QUAERO, FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC, E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI
**Analysis date:** 2025-07-10

---

### Per-Dataset Fit Assessment

#### QUAERO
- **Task:** Token-classification NER (EMEA drug leaflets + MEDLINE biomedical titles), 10 UMLS Semantic Group labels
- **Deployment fit:** Partial — QUAERO provides broad clinical entity vocabulary (DISO, ANAT, PROC, CHEM, LIVB) in French biomedical text, directly serving the deployment's NER function. However, the EMEA register is patient-facing regulatory prose rather than hospital documentation, and the dataset contains no temporal entity labels whatsoever.
- **Key strengths:**
  - Dual-register coverage (drug labels + MEDLINE titles) exercises diverse pharmaceutical and clinical vocabulary relevant to hospital NER (QUAERO-D1, QUAERO-D2, QUAERO-D4, QUAERO-D5)
  - UMLS Semantic Group ontology covers all major clinical entity types needed for pathology and treatment recognition (QUAERO-D10)
  - Medline titles span oncology, cardiology, neurology, and infectious disease, partially covering ICD-10 chapter breadth (QUAERO-D6, QUAERO-D8)
  - Text-only standard French; no modality or script concerns (QUAERO-D9)
- **Key concerns:**
  - EMEA register features parenthetical lay-language glosses absent from clinical notes (QUAERO-D11); document-splitting artefacts visible (QUAERO-D12) — register mismatch is CRITICAL for IC validity
  - Complete absence of temporal entity labels (DATE, DURATION, FREQUENCY, MOMENT) despite temporal expressions appearing in the text (QUAERO-D13, QUAERO-D14) — CRITICAL OO gap
  - MEDLINE titles are extremely short and telegraphic, testing string-matching rather than contextual clinical reasoning (QUAERO-D15, QUAERO-D16); some entries are biographical/historical (QUAERO-D17, QUAERO-D19, QUAERO-D20)
  - No ICD-10/PMSI classification signal; annotator expertise for entity boundary decisions undocumented (QUAERO-D18)

---

#### FrenchMedMCQA
- **Task:** Multiple-choice QA from French pharmacy specialization diploma exams; single and multi-answer (1–5 correct answers per question)
- **Deployment fit:** Weak — The dataset tests pharmacological declarative knowledge retrieval, not NER, POS tagging, multi-label pathology classification, or temporal extraction. Domain (pharmacy exam) diverges substantially from hospital clinical note processing; output structure (answer-set selection) is orthogonal to all deployment output functions.
- **Key strengths:**
  - Standard medical French throughout; no modality or script concerns (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D4)
  - Multi-answer structure exercises some multi-label reasoning logic (FRENCHMEDMCQA-D3, FRENCHMEDMCQA-D5)
  - Some parasitology and tropical pathology coverage in content (FRENCHMEDMCQA-D65, FRENCHMEDMCQA-D67), providing marginal DOM-TOM signal
  - Unambiguous fact-check items have high annotation reliability (FRENCHMEDMCQA-D77)
- **Key concerns:**
  - Domain mismatch is CRITICAL: every sampled example is from a pharmacy exam (subject_name="pharmacie"), covering analytical chemistry, electroanalysis, and health economics with no NLP deployment relevance (FRENCHMEDMCQA-D2, FRENCHMEDMCQA-D23, FRENCHMEDMCQA-D45, FRENCHMEDMCQA-D43)
  - Output ontology mismatch is CRITICAL: discrete answer-set selection from five fixed options has no structural relation to NER spans, POS tags, or ICD-10 code assignment (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D32)
  - No confidence calibration, uncertainty flagging, or ranked-candidate quality evaluation possible (FRENCHMEDMCQA-D20)
  - Some questions reference chemical structure diagrams unavailable in text-only format (FRENCHMEDMCQA-D40)

---

#### DEFT2020
- **Task:** Semantic textual similarity (Task 1: sentence-pair scoring 0–5; Task 2: three-way sentence selection)
- **Deployment fit:** Partial (for biomedical subset only) — The pharmaceutical and systematic review sentence pairs provide useful French biomedical STS signal relevant to entity normalization and clinical summary evaluation. However, approximately 30–40% of content is non-biomedical encyclopedic material, and the STS task format does not directly evaluate NER, classification, or ICD-10 mapping.
- **Key strengths:**
  - Pharmaceutical drug-leaflet and clinical-trial STS pairs represent authentic biomedical French (DEFT2020-D1, DEFT2020-D2, DEFT2020-D4, DEFT2020-D5)
  - Multi-annotator scoring preserves inter-annotator disagreement signal relevant to uncertainty handling (DEFT2020-D6, DEFT2020-D7)
  - Standard written French throughout; no modality concerns (DEFT2020-D8)
- **Key concerns:**
  - CRITICAL IC/IO contamination: 30–40% of examples are off-domain encyclopedic content covering railways, sports, history, and video games (DEFT2020-D9, DEFT2020-D10, DEFT2020-D11, DEFT2020-D12); one example contains non-Latin (Japanese) script (DEFT2020-D13). Aggregate benchmark scores conflate clinical and off-domain performance
  - STS task format (regression/selection) does not measure NER, classification, or ICD-10 mapping (DEFT2020-D14, DEFT2020-D15)
  - Annotator disagreement averaged away in scoring; no calibration metric reported (DEFT2020-D16)
  - No clinical case NER or pathology classification signal present (DEFT2020-D17)

---

#### MORFITT
- **Task:** Multi-label medical specialty classification (12 specialty labels) of PMC Open Access biomedical abstracts
- **Deployment fit:** Partial — MORFITT provides natively multi-label classification directly relevant to the deployment's multi-morbid pathology classification function, and it contains some tropical pathology signal (chikungunya, parasitology). However, the label space (research specialty) diverges from ICD-10/PMSI diagnostic categories, veterinary content is off-domain, and a notable fraction of abstracts originate from non-Metropolitan French settings.
- **Key strengths:**
  - Native multi-label structure with one-hot float32 vectors supports multi-label model evaluation (MORFITT-D4, MORFITT-D6)
  - Some tropical and infectious disease content present, including Chikungunya (MORFITT-D17), parasitology, and MRSA (MORFITT-D8)
  - Standard biomedical French register (MORFITT-D3)
- **Key concerns:**
  - CRITICAL IC: Source is entirely PMC Open Access abstracts — formal experimental prose, not clinical notes (MORFITT-D2, MORFITT-D16); register gap is fundamental
  - MAJOR OO: 12 specialty labels (microbiology, surgery, pharmacology) do not map to ICD-10/PMSI diagnostic axes; specialty routing ≠ diagnostic classification (MORFITT-D11, MORFITT-D21)
  - MAJOR IC/OC: Substantial non-Metropolitan French content (Canadian, Jordanian, Saudi, Arabic populations) (MORFITT-D10, MORFITT-D20, MORFITT-D31, MORFITT-D22)
  - MAJOR IC/IO: Veterinary content (equine, porcine, canine) is entirely off-domain for human hospital deployment (MORFITT-D5, MORFITT-D9, MORFITT-D26, MORFITT-D29)
  - Annotation provenance undocumented; no IAA statistics; confidence calibration not evaluable

---

#### CLISTER
- **Task:** French clinical STS — sentence-pair similarity scoring (0–5 float, averaged multi-annotator)
- **Deployment fit:** Partial — CLISTER provides the most clinically authentic French text register in the benchmark's STS tasks, sourced from clinical case documents in standard hospital prose. However, STS scoring does not directly evaluate NER, classification, or ICD-10 mapping, and annotator expertise is undocumented.
- **Key strengths:**
  - Clinical case register closely mirrors hospital documentation: surgical, oncological, nephrology, psychiatric cases in standard French medical prose (CLISTER-D1, CLISTER-D2)
  - Temporal and medication expressions present and well-represented (CLISTER-D10, CLISTER-D11)
  - Clinical sub-domain breadth across urology, oncology, gynecology, cardiology, psychiatry, pediatrics (CLISTER-D5, CLISTER-D6, CLISTER-D7)
  - Continuous label scale captures semantic gradient more informative than binary labels (CLISTER-D8, CLISTER-D9)
- **Key concerns:**
  - MAJOR OO: STS regression does not measure NER, classification, or ICD-10 mapping functions
  - MAJOR OC: Annotator profiles undocumented; clinically significant distinctions (e.g., lost to follow-up vs. death) may be systematically underweighted by non-specialist annotators (CLISTER-D12, CLISTER-D13)
  - MAJOR IC: All source documents are edited published clinical case PDFs, not raw EHR dictation notes (CLISTER-D18)
  - MINOR IO: Noticeable domain skew toward urology/oncology (CLISTER-D16); some degenerate tabular inputs (CLISTER-D17)

---

#### MANTRAGSC
- **Task:** Multilingual NER (French, German, English, Spanish, Dutch) across EMEA, Medline, and Patents sub-corpora; 10–11 UMLS Semantic Group labels
- **Deployment fit:** Weak-to-partial — The French-specific configs (fr_emea, fr_medline, fr_patents) provide valid French biomedical NER signal in the same UMLS Semantic Group label space as QUAERO, but the corpus is critically small (~100 French training examples), the source registers are non-clinical, and 9 of 12 configs are irrelevant non-French languages.
- **Key strengths:**
  - French biomedical NER in drug regulatory (EMEA), scientific (Medline), and patent text (MANTRAGSC-D1, MANTRAGSC-D2, MANTRAGSC-D5)
  - UMLS Semantic Groups provide ontologically coherent entity types (DISO, ANAT, PROC, CHEM, LIVB)
  - Standard formal French in French-specific configs (MANTRAGSC-D4)
- **Key concerns:**
  - CRITICAL IC: Extremely small French corpus (~100 training examples per config); benchmark results have high variance and CamemBERT models produce only 'O' labels in low-resource conditions (MANTRAGSC-D6)
  - CRITICAL IO: All French examples from regulatory labels, MEDLINE titles, and patent claims — no clinical notes (MANTRAGSC-D7, MANTRAGSC-D8)
  - MAJOR OO: No temporal entity labels whatsoever (MANTRAGSC-D9); DISO is undifferentiated by disease type (MANTRAGSC-D10)
  - MAJOR IC: Non-French configs dominate the dataset structure (MANTRAGSC-D11); evaluation signal must be isolated to French configs only
  - MINOR OC: Annotation authority undocumented; MINOR IO: no tropical pathology coverage (MANTRAGSC-D13)

---

#### E3C
- **Task:** Multilingual clinical NER; French_clinical (binary CLINENTITY), French_temporal (EVENT, ACTOR, BODYPART, TIMEX3, RML)
- **Deployment fit:** Partial — The French_clinical and French_temporal configs provide the most deployment-relevant temporal entity annotation in the benchmark alongside DEFT2021, with authentic clinical case French. However, non-French configs dominate the overall dataset, clinical annotation is coarse and shows evidence of incompleteness, and source material is published case reports rather than raw EHR notes.
- **Key strengths:**
  - French_temporal config directly annotates TIMEX3, EVENT, and clinical entities supporting temporal extraction (E3C-D2, E3C-D3)
  - French clinical case register with complex multi-symptom narratives (E3C-D1)
  - Authentic multilingual corpus structure confirms French examples are genuine clinical narratives, not translations
  - IOB2 annotation compatible with benchmark's SeqEval evaluation protocol (E3C-D5, E3C-D6)
- **Key concerns:**
  - CRITICAL IC/IO: Non-French configs (Basque, English, Italian, Spanish) dominate sampled data; Basque configs entirely irrelevant (E3C-D7, E3C-D8)
  - MAJOR IC: Published case report register, not raw EHR — complete sentences, no shorthand (E3C-D9, E3C-D10)
  - MAJOR OC: Apparent annotation incompleteness in French_clinical — identifiable pathogens and treatments left unlabeled (E3C-D11, E3C-D12)
  - MAJOR IO: Tropical pathology appears only in English config, absent from French subset (E3C-D4, E3C-D13)
  - MINOR OO: Coarse two-class clinical annotation (CLINENTITY vs. O) underspecifies the deployment's multi-type NER requirement (E3C-D14)

---

#### PxCorpus
- **Task:** Spoken drug prescription understanding — 4-class intent classification (medical_prescription, negate, none, replace) + 38-class NER for drug entities and temporal/dosage spans
- **Deployment fit:** Partial — PxCorpus is the benchmark's closest proxy for noisy non-formal clinical language (transcribed speech with hesitations and truncations), and it provides the richest temporal entity annotation for pharmaceutical contexts. However, it covers only drug prescription dialogues rather than general clinical note processing, contains no pathology/diagnosis labels, and has severe class imbalance undermining minority-class evaluation.
- **Key strengths:**
  - Spoken transcription register with hesitation markers, truncations, and ASR artifacts — the closest noise proxy in DrBenchmark to active hospital documentation (PXCORPUS-D1, PXCORPUS-D2, PXCORPUS-D4)
  - Richest temporal NER in the benchmark: FREQUENCY, DURATION, DOSAGE, TIME-OF-DAY entities densely annotated in authentic prescription utterances (PXCORPUS-D5, PXCORPUS-D6, PXCORPUS-D7)
  - Intent labels (negate, replace) support prescription error-detection workflows (PXCORPUS-D8, PXCORPUS-D9, PXCORPUS-D10)
  - Broad pharmaceutical coverage across drug classes and routes (PXCORPUS-D11, PXCORPUS-D12, PXCORPUS-D13)
- **Key concerns:**
  - CRITICAL OO/OF: Extreme class imbalance (medical_prescription ~89%, replace <1%, negate ~2%) — standard accuracy metrics mask minority-class performance on clinically critical correction intents (PXCORPUS-D14, PXCORPUS-D15)
  - MAJOR IO/OO: No pathology/diagnosis entities in NER tag scheme; ICD-10 mapping function cannot be evaluated (PXCORPUS-D16, PXCORPUS-D17)
  - MAJOR OO/OC: The 'none' class is semantically heterogeneous — conflates meta-commentary, system prompts, and filler speech (PXCORPUS-D18, PXCORPUS-D19, PXCORPUS-D20)
  - MAJOR IC/IF: System interaction prompts embedded in clinical NER training data corrupt register (PXCORPUS-D22, PXCORPUS-D23)
  - MINOR IC: Degenerate fragment utterances and ASR artifacts present (PXCORPUS-D24, PXCORPUS-D27, PXCORPUS-D28)

---

#### DiaMED
- **Task:** Multi-class classification — 22 ICD-10 chapter-level labels on clinical case narratives from the Pan African Medical Journal
- **Deployment fit:** Partial — DiaMED is the benchmark's only dataset with direct ICD-10 chapter-level labels and documented IAA with medical expert involvement, making it the strongest single candidate for the deployment's pathology classification function. However, the source is Sub-Saharan and North African clinical cases rather than Metropolitan French hospital documentation, the task is single-label (not multi-label with confidence), and granularity is chapter-level rather than PMSI-code-level.
- **Key strengths:**
  - Only dataset with ICD-10 chapter-level labels directly aligned with deployment's classification ontology (DIAMED-D1, DIAMED-D2)
  - Rich full-length clinical narratives in standard French with dense clinical entities (DIAMED-D3, DIAMED-D4)
  - Coverage across all 22 ICD-10 chapters including rare categories (DIAMED-D5, DIAMED-D6)
  - Only DrBenchmark dataset with documented IAA statistics and explicit medical expert annotator involvement (benchmark Q45, Q46)
- **Key concerns:**
  - CRITICAL IC/OC: Cases originate from Burkina Faso, Morocco, Niger, and other African countries — not Metropolitan French hospitals (DIAMED-D7, DIAMED-D8, DIAMED-D9). PMSI coding conventions and disease prevalence patterns differ systematically from the deployment's target population
  - MAJOR OO/OF: Single-label per case; multi-morbid cases forced into one chapter (DIAMED-D10); no confidence scores or ranked-candidate output
  - MAJOR OO: Chapter-level granularity is far coarser than operational PMSI codes (DIAMED-D11)
  - MAJOR IC: Academic published case write-up register rather than active EHR notes (DIAMED-D12)
  - MINOR OC: Very small dataset (n=739) with severe per-class imbalance for rare ICD-10 chapters

---

#### DEFT2021
- **Task:** Multi-label clinical profile classification (23 MeSH Chapter C axes) + 13-type clinical NER (PATHOLOGY, ANATOMY, TREATMENT, DOSAGE, DURATION, FREQUENCY, MOMENT, DATE, SOSY, etc.)
- **Deployment fit:** Strong (within benchmark) — DEFT2021 provides the most deployment-aligned task structure in DrBenchmark: native multi-label classification with a MeSH ontology partially aligned to ICD-10, AND a rich NER scheme covering all entity types the deployment requires including temporal markers. It is structurally the benchmark's best single-dataset proxy for the deployment's core functions.
- **Key strengths:**
  - Multi-label CLS config with up to 7 concurrent MeSH labels per clinical case directly exercises multi-morbid pathology classification (DEFT2021-D1, DEFT2021-D2)
  - NER scheme covers PATHOLOGY, TREATMENT, ANATOMY, DATE, DURATION, FREQUENCY, MOMENT — complete alignment with deployment's temporal and clinical entity extraction functions (DEFT2021-D3, DEFT2021-D4, DEFT2021-D5)
  - Rich authentic clinical case register with complex diagnostic reasoning and dense laboratory values (DEFT2021-D6, DEFT2021-D7)
  - Breadth of specialties: urology, toxicology, cardiology, nephrology, emergency medicine represented (DEFT2021-D8, DEFT2021-D9)
- **Key concerns:**
  - CRITICAL OO/OF: `specialities_one_hot` is strictly binary 0/1 — no confidence scores, no soft labels, no ranked-candidate quality evaluation possible (DEFT2021-D11)
  - CRITICAL IO: No tropical/DOM-TOM pathology categories in 23 MeSH axes; parasitic content limited to temperate pathogens (DEFT2021-D12, DEFT2021-D13)
  - MAJOR IC: Competition corpus (DEFT 2019) — academic edited register, not raw EHR shorthand (DEFT2021-D14, DEFT2021-D15)
  - MAJOR OC: Annotator PMSI credentials undocumented; MeSH axis choices for complex multi-drug cases may not align with hospital coding specialist conventions (DEFT2021-D16)
  - MAJOR IO: Very small (275 cases) with high per-label variance; some axes have very few positives (DEFT2021-D17)
  - MINOR IC: Some Quebec French terminology (DEFT2021-D20)

---

#### CAS
- **Task:** French clinical case corpus — negation/speculation classification (4 labels), negation/speculation NER (IOB2), and POS tagging (31 classes, automatic Tagex annotations)
- **Deployment fit:** Partial — CAS provides the largest French clinical case corpus in the benchmark with authentic clinical register and useful negation/speculation signal for clinical NLP pipelines. However, the classification labels (negation/speculation modality) are orthogonal to ICD-10 pathology categories, and POS tags are silver-standard automatic annotations.
- **Key strengths:**
  - Largest clinical case corpus; authentic French clinical register with lab values, surgical narratives, and temporal expressions (CAS-D1, CAS-D2, CAS-D3)
  - Temporal expression content directly relevant to deployment's care timeline extraction (CAS-D4, CAS-D5, CAS-D6)
  - Negation/speculation annotation supports downstream accurate pathology coding (CAS-D7, CAS-D8, CAS-D9)
  - Specialty breadth including gastroenterology, obstetrics, cardiology, oncology, infectious disease (CAS-D10, CAS-D11, CAS-D12)
  - POS tagging directly covers deployment's POS tagging pipeline component (CAS-D13)
- **Key concerns:**
  - CRITICAL OC: POS tags are silver-standard automatic (Tagex); no expert clinical annotator involvement documented (CAS-D15)
  - MAJOR OC: No IAA statistics for negation/speculation labels; annotation rationale opaque for some ambiguous cases (CAS-D16, CAS-D17)
  - MAJOR OO: Classification labels (negation/speculation) do not align with ICD-10/PMSI mapping; task is a linguistic modality detector, not a pathology classifier (CAS-D19)
  - MAJOR IO: No tropical/overseas-territory pathologies visible across all sampled examples (CAS-D18)
  - MINOR IC: Register slightly more formal than raw EHR notes (CAS-D20); severe class imbalance in cls config with neutral dominating at ~74% (CAS-D21)

---

#### ESSAI
- **Task:** French clinical trial protocol corpus — negation/speculation classification (4 labels), negation/speculation NER, and POS tagging (36 tags, TreeTagger automatic)
- **Deployment fit:** Weak-to-partial — ESSAI covers an even narrower subdomain than CAS (exclusively oncology clinical trial protocols), provides the same output ontology mismatch (negation/speculation, not ICD-10), and uses automatic POS annotations. Its primary value is as a formal French biomedical prose register, with negation/speculation signal relevant to pipeline preprocessing.
- **Key strengths:**
  - Formal clinical trial French biomedical register; dense oncological treatment and temporal content (ESSAI-D1, ESSAI-D2, ESSAI-D6, ESSAI-D7, ESSAI-D8)
  - Negation and speculation detection coverage including temporal dosing structures (ESSAI-D3, ESSAI-D4, ESSAI-D5)
  - 36-class POS scheme for French biomedical morphology
- **Key concerns:**
  - CRITICAL OO: Classification labels (negation/speculation) have zero overlap with ICD-10/PMSI mapping function (ESSAI-D9)
  - MAJOR IC: Source domain exclusively oncology clinical trial protocols — far narrower than general hospital documentation (ESSAI-D10, ESSAI-D11)
  - MAJOR OC: TreeTagger automatic POS; NER annotation provenance undocumented; no IAA statistics
  - MAJOR OC: Extreme class imbalance with neutral at ~77% (ESSAI-D13); NER annotation is extremely sparse (ESSAI-D14)
  - MINOR IC: No tropical/DOM-TOM pathology content

---

### Cross-Cutting Strengths

**1. Consistent standard written French across all datasets**
Every dataset in the benchmark is text-only in standard French with Latin-diacritical script. No modality, script, or dialect mismatches are present relative to the deployment's text-only clinical NLP pipeline. This uniform IF coverage means the benchmark's signal is entirely within the correct language and modality space (QUAERO-D9, CLISTER-D1, DEFT2021-D1, CAS-D1, ESSAI-D1).

**2. Multi-label classification structure present in three datasets**
DEFT2021, MORFITT, and DiaMED all implement multi-label or multi-class classification directly exercising the deployment's central pathology classification function. DEFT2021's 23 MeSH axes with up to 7 co-occurring labels (DEFT2021-D1, DEFT2021-D2), MORFITT's 12 specialty labels with float32 one-hot vectors (MORFITT-D4, MORFITT-D6), and DiaMED's 22 ICD-10 chapter labels (DIAMED-D1) collectively provide meaningful multi-label evaluation signal for a core deployment function.

**3. Temporal entity annotation coverage**
Three datasets contribute temporal entity signal: E3C's French_temporal config annotates TIMEX3, EVENT, ACTOR, BODYPART, RML (E3C-D2, E3C-D3); DEFT2021's NER scheme includes DATE, DURATION, FREQUENCY, MOMENT, and MOMENT labels explicitly (DEFT2021-D3, DEFT2021-D4, DEFT2021-D5); PxCorpus provides the most densely annotated temporal pharmaceutical expressions in the benchmark (PXCORPUS-D5, PXCORPUS-D6, PXCORPUS-D7). This cross-dataset coverage partially addresses the deployment's temporal entity extraction function.

**4. NER across complementary French biomedical registers**
QUAERO (drug labels + MEDLINE), MANTRAGSC (EMEA + Medline + Patents), E3C (clinical cases), DEFT2021 (competition clinical cases), CAS (clinical cases), and PxCorpus (drug prescriptions) collectively cover regulatory, scientific, and clinical-case registers for French biomedical NER. The UMLS Semantic Group label space shared between QUAERO and MANTRAGSC provides ontological consistency for entity type coverage (QUAERO-D1, MANTRAGSC-D1, MANTRAGSC-D2).

**5. Clinical case register depth in CAS, CLISTER, and DEFT2021**
CAS (3,790 cases), CLISTER (1,000 sentence pairs from clinical cases), and DEFT2021 (275 cases) all use French clinical case text as source material with realistic clinical prose including quantified lab values, surgical narratives, and diagnostic reasoning (CAS-D2, CLISTER-D2, DEFT2021-D7). While all are edited published cases rather than raw EHR notes, they represent the closest available approximation to the deployment's hospital documentation environment.

---

### Cross-Cutting Weaknesses

#### CRITICAL — Benchmark-wide absence of confidence calibration and uncertainty flagging evaluation (OO, OF)
Across all 11 datasets, no evaluation protocol measures confidence calibration, uncertainty flagging, or ranked-candidate list quality. Classification datasets use strictly binary labels (DEFT2021-D11, MORFITT one-hot vectors) and standard F1/accuracy metrics. DiaMED uses single-label forced-choice even for inherently multi-morbid cases (DIAMED-D10). STS datasets (CLISTER, DEFT2020) average annotator scores into a single float value, discarding the disagreement signal that could inform uncertainty evaluation (DEFT2020-D16). The deployment's most architecturally essential behavior — multi-label outputs with calibrated confidence scores and high-uncertainty flagging for clinician adjudication — is structurally unmeasurable across the entire benchmark.

#### CRITICAL — Systematic register gap: edited published sources vs. active hospital EHR notes (IC)
Every dataset in the benchmark sources text from one or more of: clinical trial protocols (ESSAI), competition corpora (DEFT2021, DEFT2020), peer-reviewed case reports (CAS, CLISTER, E3C, DiaMED), drug regulatory documents (QUAERO-EMEA, MANTRAGSC), MEDLINE titles (QUAERO-Medline, MANTRAGSC-Medline), or patent claims (MANTRAGSC-Patents). No dataset uses raw hospital EHR discharge notes, dictation recordings (beyond PxCorpus prescription-domain), or institution-specific documentation. The deployment processes moderately noisy notes with common clinical abbreviations and shorthand. Web search confirms no French raw-EHR benchmark exists. Examples of the formality gap: ESSAI-D11, CAS-D20, E3C-D9, DEFT2021-D14, DEFT2021-D15, DIAMED-D12. PxCorpus provides partial noise signal but only in the drug prescription domain (PXCORPUS-D1, PXCORPUS-D2).

#### CRITICAL — Absence of PMSI coder or hospital coding specialist annotation authority (OC)
Across all 11 datasets, no annotation was performed by practicing PMSI coders or hospital coding specialists. DiaMED is the sole dataset with documented medical expert involvement (one expert annotator), and that expert's PMSI coding credentials are unspecified (benchmark Q45). DEFT2021's multi-label MeSH annotations — the most deployment-relevant classification labels — were produced by academic NLP competition participants with no documented clinical coding credentials (DEFT2021-D16). CAS POS tags are automatic (CAS-D15). This annotation authority gap is confirmed absent benchmark-wide, not merely undocumented.

#### MAJOR — Non-Metropolitan French clinical content misrepresented as deployment-relevant (IC, OC)
DiaMED's 739 clinical cases originate from the Pan African Medical Journal, with examples from Burkina Faso, Morocco, and Niger (DIAMED-D7, DIAMED-D8, DIAMED-D9) — explicitly not Metropolitan French hospital populations. MORFITT contains substantial content from Canadian, Jordanian, Saudi, and Arabic research contexts (MORFITT-D10, MORFITT-D20, MORFITT-D22, MORFITT-D31). These datasets introduce geographic and epidemiological heterogeneity that does not correspond to the Metropolitan French deployment target, potentially distorting performance estimates for the deployment's actual patient documentation.

#### MAJOR — Tropical and overseas-territory pathology coverage absent across all French-language subsets (IO)
No dataset provides French-language clinical text or annotation covering pathologies prevalent in French overseas territories (dengue, chikungunya, Zika, malaria at population scale, leptospirosis, sickle-cell crisis presentations). The only tropical pathology signals appear in non-French dataset subsets: schistosomiasis in E3C's English config (E3C-D4), malaria in FrenchMedMCQA pharmacy questions (FRENCHMEDMCQA-D67), and Chikungunya in a MORFITT abstract (MORFITT-D17). DiaMED's Pan African Medical Journal source introduces some tropical disease proximity via ICD-10 infectious disease chapters, but its cases are not Metropolitan French and the specific DOM-TOM pathology coverage is undocumented. The French-language clinical NER and classification datasets are entirely metropolitan in pathology profile.

#### MAJOR — Output ontology misalignment for multiple datasets (OO)
Four datasets — CAS, ESSAI, FrenchMedMCQA, and DEFT2020 (partially) — have output ontologies entirely orthogonal to the deployment's ICD-10/PMSI classification function. CAS and ESSAI measure negation/speculation modality (CAS-D19, ESSAI-D9). FrenchMedMCQA measures pharmacy exam answer-set selection (FRENCHMEDMCQA-D1). DEFT2020 measures sentence-pair similarity (DEFT2020-D14, DEFT2020-D15). MANTRAGSC and QUAERO measure UMLS Semantic Group NER with no ICD-10 subcategory distinction (MANTRAGSC-D10, QUAERO — no ICD-10 signal). Only DEFT2021, DiaMED, and MORFITT provide classification labels with any ICD-10 or specialty-level alignment.

#### MAJOR — Temporal entity annotation concentrated in few datasets, absent in most (IO, OO)
The majority of DrBenchmark datasets provide no temporal entity labels: QUAERO has no temporal labels despite temporal expressions in text (QUAERO-D13, QUAERO-D14); MANTRAGSC has no temporal labels (MANTRAGSC-D9); MORFITT, CLISTER, CAS (cls), and ESSAI (cls) have no temporal NER. Temporal coverage is limited to E3C French_temporal, DEFT2021 NER, and PxCorpus — a narrow subset of the benchmark's 20 tasks. Given the deployment's explicit requirement for temporal entity extraction for care prioritization, this concentration is a systemic coverage gap.

#### MINOR — Severe class imbalance across multiple classification datasets (OF, OO)
CAS cls neutral class ~74% (CAS-D21); ESSAI cls neutral ~77% (ESSAI-D13); PxCorpus medical_prescription ~89% (PXCORPUS-D15). In all three cases, majority-class baselines achieve high accuracy while being clinically uninformative, and evaluation of the minority classes most relevant to the deployment (negation, speculation, prescription correction, intent replacement) is unreliable.

---

### Content Coverage Summary

**Well-covered domains and registers:**
- Standard written French biomedical prose across regulatory (EMEA drug labels), scientific (MEDLINE, PMC abstracts), clinical case (CAS, CLISTER, E3C, DEFT2021, DiaMED), pharmaceutical patent, and spoken prescription (PxCorpus) registers
- Clinical entity types: pathology, anatomy, procedure, chemical substance, living being — covered by QUAERO, MANTRAGSC, E3C, DEFT2021
- Temporal entity types: DATE, DURATION, FREQUENCY, MOMENT — covered by DEFT2021 NER, E3C French_temporal, PxCorpus
- Negation and speculation detection: CAS, ESSAI
- Multi-label classification: DEFT2021 (23 MeSH axes), MORFITT (12 specialties), DiaMED (22 ICD-10 chapters)
- POS tagging: CAS (31 tags), ESSAI (36 tags)
- Model comparison: 8 state-of-the-art French and French-biomedical MLMs evaluated under unified protocol

**Gaps relative to deployment needs:**
- Raw EHR discharge notes and dictation-sourced text: absent from the entire benchmark; no French raw-EHR clinical NLP benchmark exists
- Confidence calibration and uncertainty flagging evaluation: structurally absent across all 20 tasks
- PMSI-granular code classification (beyond chapter level): absent; DiaMED is the coarsest available proxy
- Hospital coding specialist annotation authority: absent benchmark-wide
- Metropolitan French hospital population pathology profiles: partially represented through metropolitan clinical case corpora (CAS, CLISTER, ESSAI, DEFT2021), but contaminated by non-metropolitan content in DiaMED and MORFITT
- DOM-TOM tropical pathology coverage: absent from all French-language clinical subsets
- Multi-label classification at PMSI code level: absent; MeSH and ICD-10 chapter labels provide coarse alignment only
- Ranked-candidate output evaluation: absent across all classification tasks

---

### Limitations

1. **Sample-based analysis only**: Each per-dataset report analyzed a sample of examples (50–200 per dataset); rare label classes, corner cases, and dataset tails may be underrepresented in the evidence base. Per-class performance statistics were not computed.
2. **Non-French configs not inspectable for deployment purposes**: MANTRAGSC (9/12 configs), E3C (8/10 configs non-French), and MORFITT (non-Metropolitan French abstracts) contain substantial irrelevant content that was identified but not exhaustively characterized.
3. **Internal test set contents unknown**: The benchmark reports held-out test set performance; the per-dataset analyses inspected training/validation examples. Label distribution and content of test sets may differ from training splits.
4. **Annotation provenance beyond the paper**: The per-dataset reports and benchmark YAML provide the primary evidence for annotation authority claims. No independent access to DEFT competition annotation guidelines, CLISTER annotator demographic data, or CAS/ESSAI TreeTagger/Tagex validation methodology was available for direct inspection.
5. **DiaMED full geographic distribution unverified**: The Sub-Saharan and North African clinical origin of DiaMED cases is confirmed from sampled examples, but the full geographic distribution across all 739 cases was not enumerated.
6. **MORFITT annotation protocol**: No HuggingFace card or paper excerpt documenting the specialty annotation process for MORFITT was inspected; annotation authority and IAA are unverifiable beyond the dataset overview.
7. **PxCorpus register contamination extent**: The proportion of system-interaction-contaminated examples relative to total examples could not be quantified from the sample alone.

---

### Cited Evidence

- **QUAERO-D1**: QUAERO/emea | 38 | DISO/PROC | "TYSABRI est utilisé pour traiter la sclérose en plaques (SEP)… troubles de la marche, engourdissement du visage" | Disease/symptom enumeration in EMEA drug label; strong DISO entity density | IO, IC
- **QUAERO-D2**: QUAERO/emea | 46 | DISO/PROC | "les effets indésirables les plus couramment observés sous Tysabri… rhinopharyngite… urticaire… arthralgie… pyrexie (fièvre)" | Multi-entity adverse-event list; confirms NER coverage of pathology vocabulary | IC
- **QUAERO-D3**: QUAERO/medline | 3 | DISO | "Alcool et cancer." | Very short MEDLINE title; confirms text register range in dataset | IC
- **QUAERO-D4**: QUAERO/emea | 1 | CHEM | "Phosphate de sodium, monobasique, monohydraté… Polysorbate 80 (E433)… Eau pour préparation injectable." | Chemical excipient list; confirms pharmaceutical CHEM annotation | IC
- **QUAERO-D5**: QUAERO/emea | 55 | CHEM/DEVI | "TYSABRI 300 mg solution à diluer pour perfusion… chaque flacon de 15 ml de concentré contient 300 mg de natalizumab" | Dosage/container/drug vocabulary; confirms DEVI and CHEM annotation | IC
- **QUAERO-D6**: QUAERO/medline | 98 | DISO/GEOG | "Le paludisme chimiorésistant en France." | Malaria + geographic tag; infectious disease domain coverage | IO, IC
- **QUAERO-D7**: QUAERO/medline | 106 | DISO/LIVB | "Encéphalopathie toxique par ingestion de carambole (Averrhoa carambola)." | Tropical plant toxicity; exotic etiology in MEDLINE corpus | IC
- **QUAERO-D8**: QUAERO/medline | 45 | DISO | "Le syndrome de Noonan et sa dysplasie cardio-vasculaire." | Rare genetic/cardiovascular disorder; confirms ontological breadth | IO
- **QUAERO-D9**: QUAERO/emea | 2 | DISO/PHYS | "Une cirrhose du foie peut également affecter l'excrétion rénale de la lépirudine." | Standard written French medical prose; confirms script/register alignment | IF
- **QUAERO-D10**: QUAERO/emea | 6 | DISO | "Des épisodes de troubles psychiatriques aigus, tels que hallucinations, réactions paranoïdes… psychose et réactions maniaques" | Psychiatric DISO enumeration; tests fine-grained entity boundary detection | OO
- **QUAERO-D11**: QUAERO/emea | 46 | DISO | "rhinopharyngite (inflammation du nez et de la gorge), urticaire (éruption cutanée)" | Patient-leaflet gloss structure absent from clinical notes; register mismatch | IC
- **QUAERO-D12**: QUAERO/emea | 4 | O | "Aucune étude clinique spécifique sur les interactions médicamenteuses n Toutefois…" | Sentence truncation artefact from EMEA document splitting; preprocessing noise | IC
- **QUAERO-D13**: QUAERO/emea | 26 | O | "La durée du traitement est allée d'une heure de perfusion en bolus à une utilisation continue de plus de 6 ans." | Temporal expressions present but unlabeled; confirms absence of temporal NER | OO
- **QUAERO-D14**: QUAERO/emea | 11 | O | "La dose peut être augmentée par intervalles de 1 à 2 jours, voire plus…" | Another unlabeled temporal phrase; reinforces temporal NER gap | OO
- **QUAERO-D15**: QUAERO/medline | 27 | PHYS | "Anoïkis." | Single-token title; zero context, tests only string-matching NER | IC
- **QUAERO-D16**: QUAERO/medline | 3 | DISO | "Alcool et cancer." | Three-token title; minimal clinical context for entity recognition | IC
- **QUAERO-D17**: QUAERO/medline | 61 | O | "LÉON GRIMBERT 1860 - 1931." | Biographical entry; no clinical entities; irrelevant to clinical NLP | IC
- **QUAERO-D18**: QUAERO/emea | 64 | DISO/ANAT | "Si vous avez des perturbations graves du système immunitaire (dues à une maladie, telle que leucémie ou infection à VIH…" | Entity boundary ambiguity; annotation by NLP researchers may differ from clinician judgment | OC
- **QUAERO-D19**: QUAERO/medline | 16 | O | "L'apport des inventaires a la connaissance de la demographie parisienne ancienne: le regne de Francois Ier" | Historical demography; not clinically relevant | IC
- **QUAERO-D20**: QUAERO/medline | 34 | O | "La santé du duc d'Enghien durant ses primes années d'après le journal de son médecin." | Historical biographical text; off-domain for clinical NLP | IC
- **QUAERO-D21**: QUAERO/medline | 137 | DISO/LIVB | "Sensibilité à la pénicilline G des pneumocoques isolés des méningites et implication thérapeutique au CHU de Treichville-Abidjan." | Sub-Saharan institution; non-metropolitan French clinical context in MEDLINE | IC
- **FRENCHMEDMCQA-D1**: FrenchMedMCQA | 1 | 1 | "Au cours de la leucémie lymphoïde chronique, le myélogramme montre: Une population de lymphocytes>30%" | Clinical hematology question in formal medical French | IC, IF
- **FRENCHMEDMCQA-D2**: FrenchMedMCQA | 2 | 2 | "La loi de Beer-Lambert: S'applique aux dosages spectrophotométriques... Est une loi additive" | Analytical chemistry question irrelevant to clinical NLP | IO, OC
- **FRENCHMEDMCQA-D3**: FrenchMedMCQA | 3 | 3 | "Parmi les propriétés suivantes du monoxyde de carbone... correct_answers: [0, 3, 4]" | Multi-label MCQA structure covering CO properties | IO
- **FRENCHMEDMCQA-D4**: FrenchMedMCQA | 4 | 4 | "L'acétylcholine est libérée par: Les neurones sympathiques préganglionnaires" | Pharmacological terminology in standard medical French | IC, IF
- **FRENCHMEDMCQA-D5**: FrenchMedMCQA | 5 | 5 | "Les marqueurs suivants sont présents dans les lymphocytes B matures... correct_answers: [0, 1, 2, 3, 4]" | All-five-correct multi-label answer, showing full label cardinality | IO
- **FRENCHMEDMCQA-D9**: FrenchMedMCQA | 9 | 4 | "L'oeuf d'Enterobius vermicularis: Est incolore, Est asymétrique..." | Parasitology content with partial tropical relevance | IO
- **FRENCHMEDMCQA-D13**: FrenchMedMCQA | 13 | 3 | "Quel est (sont) le(s) diurétique(s) qui provoque(nt) une baisse du potassium sanguin? Chlortalidone, Hydrochlorothiazide, Furosémide" | Drug class knowledge relevant to clinical pharmacology | IC
- **FRENCHMEDMCQA-D14**: FrenchMedMCQA | 14 | 4 | "intoxication par les salicylés... L'administration intraveineuse de bicarbonate de sodium permet de corriger l'acidose métabolique" | Clinical toxicology management scenario | IC
- **FRENCHMEDMCQA-D20**: FrenchMedMCQA | 20 | 5 | "Dans quel(s) cas peut-on parler d'hypertension artérielle selon les critères de l'OMS? correct_answers: [0, 1, 2, 3, 4]" | All-correct answer; no confidence signal available | OO, OF
- **FRENCHMEDMCQA-D23**: FrenchMedMCQA | 23 | 3 | "En électrophorèse capillaire haute performance, le sens de migration de l'analyse dépend: De la nature de la charge de l'analyte" | Analytical chemistry instrumentation; not relevant to clinical NLP | IO
- **FRENCHMEDMCQA-D24**: FrenchMedMCQA | 24 | 4 | "Chez un patient atteint de SIDA... Lymphopénie, Diminution des lymphocytes T4, Adénopathies, Thrombopénie" | AIDS hematological profile; relevant to pathology classification | IC
- **FRENCHMEDMCQA-D32**: FrenchMedMCQA | 32 | 4 | "correct_answers: [0, 1, 3, 4]" | Four-of-five selection; binary gold label, no confidence ranking | OO, OF
- **FRENCHMEDMCQA-D37**: FrenchMedMCQA | 37 | 1 | "Les 3 nucléides de l'hydrogène, H(A=1,Z=1), H(A=2,Z=1) et H(A=3,Z=1) sont: Des isotopes" | Nuclear physics in pharmacy exam; clean French text, no abbreviations | IF
- **FRENCHMEDMCQA-D40**: FrenchMedMCQA | 40 | 4 | "le composé suivant: Est utilisé comme antibactérien... Augmente l'ototoxicité des aminosides" | References implied chemical structure diagram; text-only representation incomplete | IC
- **FRENCHMEDMCQA-D43**: FrenchMedMCQA | 43 | 3 | "L'économie médicale est une économie... Caractérisée par le libre choix des médecins par le malade" | Health economics question; low clinical NLP relevance | IO
- **FRENCHMEDMCQA-D45**: FrenchMedMCQA | 45 | 1 | "Parmi les techniques voltampérométriques, on trouve: La polarographie" | Electroanalytical chemistry; irrelevant to hospital clinical NLP | IO
- **FRENCHMEDMCQA-D61**: FrenchMedMCQA | 61 | 1 | "La certification des établissements de santé: Concerne tous les établissements de santé" | Health system regulation; marginal clinical NLP relevance | IO
- **FRENCHMEDMCQA-D65**: FrenchMedMCQA | 65 | 1 | "le mode habituel de contamination de l'homme dans la bilharziose urinaire: Pénétration trans-cutanée" | Tropical parasitosis; partial DOM-TOM pathology coverage | IO, IC
- **FRENCHMEDMCQA-D67**: FrenchMedMCQA | 67 | 3 | "Quelle est (sont) la (les) parasitose(s) qui présente(nt) un stade hépatique? Giardiase, Paludisme, Fasciolose; correct: [1, 2, 3]" | Malaria and other tropical parasitoses included | IO, IC
- **FRENCHMEDMCQA-D77**: FrenchMedMCQA | 77 | 1 | "Quelle est la base qui n'existe pas dans une molécule d'ADN? Uracile" | Unambiguous factual label, high annotation reliability | OC
- **FRENCHMEDMCQA-D99**: FrenchMedMCQA | 99 | 3 | "Les modifications de structure permettant le passage du composé 1 au composé 2 entraînent: Un élargissement du spectre vers les cocci Gram+" | Structure-comparison question requiring figure; no extractable entities | IO
- **FRENCHMEDMCQA-D117**: FrenchMedMCQA | 117 | 1 | "Un patient de 20 ans est traité par héparine de bas poids moléculaire pour une thrombose iliaque... Activité anti Xa = 2,00 UI/mL" | Clean clinical vignette; structured exam format, not raw clinical note | IC
- **DEFT2020-D1**: DEFT2020/task_1 | Ex.16 | moy=4.0 | "Ce produit peut provoquer un syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après la dernière prise de stupéfiant." | Pharmaceutical drug leaflet sentence about opioid withdrawal; matches clinical register | IC
- **DEFT2020-D2**: DEFT2020/task_1 | Ex.18 | moy=4.6 | "En raison de la présence de lactose, ce médicament est contre-indiqué en cas de galactosémie congénitale, de syndrome de malabsorption du glucose et du galactose ou de déficit en lactase." | Drug contraindication notice; standard French pharmaceutical register | IC
- **DEFT2020-D3**: DEFT2020/task_2 | T2 Ex.22 | correct_cible=0 | "l'utilisation à forte dose d'huile de paraffine expose au risque de suintement anal et parfois d'irritation périanale" | Medical side-effect phrasing; evaluates clinical paraphrase equivalence | IC, OO
- **DEFT2020-D4**: DEFT2020/task_1 | Ex.26 | moy=3.4 | "Pour la comparaison entre blocs neuraxiaux et anesthésie générale, nous avons évalué la qualité des preuves comme très faible pour la mortalité..." | Systematic review evidence-appraisal language; clinical summary register | IC
- **DEFT2020-D5**: DEFT2020/task_1 | Ex.31 | moy=2.7 | "Déterminer l'effet d'une alimentation trophique précoce comparée à un jeûne entéral sur la tolérance à l'alimentation, la croissance et le développement..." | Neonatal intensive care research objective; relevant to temporal entity extraction | IC
- **DEFT2020-D6**: DEFT2020/task_1 | Ex.4 | moy=4.0, scores=[5,2,4,4,5] | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter pendant la durée du traitement." | High inter-annotator variance on near-paraphrase; illustrates uncertainty in clinical STS | OC
- **DEFT2020-D7**: DEFT2020/task_1 | Ex.36 | moy=1.5, scores=[2,4.5,0,1,0] | "Après inspection, elles ont toutes été exclues." | Extreme annotator disagreement (4.5 vs. 0.0); relevant to uncertainty flagging deployment behavior | OC, OF
- **DEFT2020-D8**: DEFT2020/task_1 | Ex.54 | moy=5.0 | "Troubles de l'hémostase à type de maladie de Willebrand (se traduisant par un allongement du TCA, du temps de saignement et une diminution des taux du complexe VIIIC/VWF)." | Specialized hematological terminology; clean standard French; no modality issues | IF, IC
- **DEFT2020-D9**: DEFT2020/task_1 | Ex.1 | moy=0.5 | "Entre Perpignan et Villefranche, il subsiste de très nombreux poteaux caténaires datant des premiers essais en 12 KV 16 2/3 Hz..." | Railway infrastructure content; entirely off-domain for clinical NLP deployment | IC, IO
- **DEFT2020-D10**: DEFT2020/task_1 | Ex.3 | moy=2.1 | "Boris Fiodorovitch Godounov, en russe : Бори́с Фёдорович Годуно́в (v.1551–Moscou, 13 avril 1605)..." | Russian historical figure biography; off-domain and contains Cyrillic script | IC, IO
- **DEFT2020-D11**: DEFT2020/task_1 | Ex.60 | mow=0.8 | "Les Canadiens de Montréal sont une franchise de hockey sur glace professionnel située à Montréal dans la province de Québec au Canada." | Professional hockey franchise; irrelevant to hospital deployment | IC, IO
- **DEFT2020-D12**: DEFT2020/task_2 | T2 Ex.37 | correct_cible=0 | "Lancement du célèbre MMORPG : World of Warcraft." | Video game launch event; entirely off-domain | IC, IO
- **DEFT2020-D13**: DEFT2020/task_2 | T2 Ex.51 | correct_cible=2 | "42 Jeux indémodables ( だれでもアソビ大全 , Daredemo Asobi Taizen au Japon...)" | Japanese script embedded in French text; video game content; off-domain | IC, IO, IF
- **DEFT2020-D14**: DEFT2020/task_1 | schema | — | Fields: id, moy, vote, scores, source, cible | Continuous similarity scoring schema; no entity labels, no ICD-10 classification outputs | OO, OF
- **DEFT2020-D15**: DEFT2020/task_2 | schema | — | Field: correct_cible (0/1/2) | Sentence selection index; not a pathology classification or ICD-10 label | OO, OF
- **DEFT2020-D16**: DEFT2020/task_1 | Ex.36 | moy=1.5, scores=[2,4.5,0,1,0] | "Après inspection, elles ont toutes été exclues." | Annotator disagreement averaged away in scoring; calibration signal lost | OO, OF
- **DEFT2020-D17**: DEFT2020/task_1 | Ex.17 | moy=1.7 | "Les personnes infectées par le virus de l'immunodéficience humaine présentent un risque augmenté de développer une tuberculose (TB) active." | HIV/TB clinical content present as STS pair only; no ICD-10 label, no NER annotation | IO, OC
- **DEFT2020-D18**: DEFT2020/task_1 | Ex.6,7,9,11,12 | moy≈0 | "Certains apiculteurs sélectionnent leurs reines afin de favoriser au mieux la production." | Beekeeping encyclopedia cluster; repeated off-domain topic; no clinical relevance | IC, IO
- **MORFITT-D2**: MORFITT | 2 | [10] | "Dans le cadre d'expériences animales in vivo en aveugle randomisées contrôlées, nous avons étudié les réponses nociceptives induites par une i.pl. de HS chez des souris C57BL/6 (vs CD-1) des deux sexes (n = 240)..." | Structured experimental abstract; not clinical note format — register gap from deployment | IC
- **MORFITT-D3**: MORFITT | 3 | [1] | "Les taux d'AST ( p < 0,001), d'ALT ( p < 0,01), d'amylase ( p < 0,001), de LDH ( p < 0,01), de TNF-α ( p < 0,01), d'IL-1β ( p < 0,001) et d'IL-6 ( p < 0,001)..." | Dense biomedical lab terminology confirming standard French biomedical register | IC
- **MORFITT-D4**: MORFITT | 4 | [8,4] | "La croissance du commerce international a apporté des bénéfices significatifs à l'humanité tout en générant certains coûts. Parmi ceux-ci figure la propagation accrue de parasites et d'agents pathogènes à l'échelle planétaire." | Dual-label (veterinary + genetics) abstract; shows multi-label capability | IO, OO
- **MORFITT-D5**: MORFITT | 5 | [6,8] | "seules des données limitées sont disponibles sur le surfactant chez le cheval... notre objectif était de mener une étude immunocytochimique au microscope optique et électronique sur les poumons normaux du cheval." | Equine veterinary immunology study; off-domain for human hospital deployment | IC, IO
- **MORFITT-D6**: MORFITT | 6 | [6,8,2] | "Le syndrome dysgénésique et respiratoire du porc (SDRP) a un impact énorme sur l'industrie du porc en l'Amérique du Nord." | Porcine veterinary virology abstract; three-label co-occurrence but off-domain | IO, IC
- **MORFITT-D8**: MORFITT | 8 | [0] | "La région du Nord-Ouest de l'Ontario présente un taux élevé et documenté d'infections de la peau et des tissus mous causées par une souche de Staphylococcus aureus méthycillinorésistante d'origine communautaire (SARM-C)." | Canadian infectious disease study (MRSA); relevant microbiology label but non-French geography | IC, OC
- **MORFITT-D9**: MORFITT | 9 | [6,0,8] | "L'otite externe est une maladie multifactorielle fréquente chez le chien... Décrire le microbiote bactérien auriculaire des chiens avec otite externe comparé aux chiens sains." | Canine ear microbiome study; veterinary content off-domain for hospital NLP | IC, IO
- **MORFITT-D10**: MORFITT | 10 | [3] | "L'objectif de cette étude était de documenter les pratiques actuelles de gestion des maladies dans les exploitations apicoles situées au sud-ouest du Québec, Canada." | Canadian beekeeping disease management study; non-Metropolitan French origin | IC, OC
- **MORFITT-D11**: MORFITT | 11 | [1,9] | "Nous rapportons le cas d'une patiente de 71 ans ayant développé un pseudomyxome péritonéal secondaire à un adénocarcinome appendiculaire." | Clinical case abstract with surgery+etiology labels; labels do not map to ICD-10 codes | OO
- **MORFITT-D16**: MORFITT | 16 | [3] | "Nous avons étudié 451 diabétiques et 451 non-diabétiques sans MAC manifeste et avec une perfusion myocardique normale. Le débit sanguin myocardique (DSM) a été calculé sur bases des images TEP/TDM de repos et de stress." | Clinical cardiology study abstract format; not clinical note | IC
- **MORFITT-D17**: MORFITT | 17 | [2] | "L'émergence d'une épidémie d'arbovirose est le plus souvent liée à la convergence d'un ensemble de facteurs... à travers l'étude de l'épidémie de Chikungunya, un alphavirus transmis par Aedes aegypti et Aedes albopictus, survenue dans l'océan Indien en 2004-2007." | Chikungunya virology abstract — tropical pathology relevant to DOM-TOM gap | IO, IC
- **MORFITT-D20**: MORFITT | 20 | [1] | "79 patients au total ont été recrutés à Amman (Jordanie) en 2015." | Jordanian patient population; non-Metropolitan French clinical context | IC, OC
- **MORFITT-D21**: MORFITT | 21 | [1,3,4] | "Bloquer le complément, notamment l'axe C5a-C5aR1, par des thérapies spécifiques représente un espoir thérapeutique dans les formes les plus sévères de la maladie." | COVID-19 immunology; three specialty labels that don't resolve to ICD-10 output | OO
- **MORFITT-D22**: MORFITT | 22 | [11] | "le questionnaire YFAS 2.0-A... peut être utilisée comme équivalent du questionnaire anglais YFAS 2.0 pour étudier l'addiction à la nourriture dans les populations arabophones." | Arabic-population food addiction validation study; non-French population | IC, OC
- **MORFITT-D26**: MORFITT | 26 | [6,8,5] | "Prévalence et caractéristiques morphologiques et moléculaires de Sarcocystis bertrami chez les chevaux en Chine." | Horse parasitology study from China; off-domain for human hospital deployment | IC, IO
- **MORFITT-D29**: MORFITT | 29 | [8] | "La cyclosporine est de plus en plus utilisée en dermatologie des petits animaux." | Small animal dermatology; veterinary content irrelevant to hospital clinical NLP | IC, IO
- **MORFITT-D31**: MORFITT | 31 | [11] | "Un autoquestionnaire envoyé par courrier électronique a été rempli par 191 médecins internes sur 207 travaillant dans différentes spécialités et régions de Riyad." | Saudi Arabian intern survey; non-Metropolitan French context | IC, OC
- **CLISTER-D1**: CLISTER | 7 | 4.0 | "La patiente a été opérée et lors de l'exploration on découvrit qu'il s'agissait d'une tumeur de la veine cave inférieure sus-rénale." | Surgical/oncological clinical case language matching hospital documentation register | IC, IF
- **CLISTER-D2**: CLISTER | 85 | 4.0 | "Le bilan rénal a objectivé une insuffisance rénale avec une créatininémie à 1440 μmol/l, soit une clairance de la créatinine à 6,7 ml/mn/m2, urémie à 2,07 g/l." | Quantified biological workup with clinical abbreviations; representative of standard hospital documentation | IC
- **CLISTER-D3**: CLISTER | 10 | 5.0 | "Une mastectomie était réalisée avec curage axillaire." vs. "Une mastectomie avec curage axillaire ont été réalisés." | Near-identical surgical procedure sentences; tests paraphrase detection for entity normalization | IC
- **CLISTER-D4**: CLISTER | 37 | 5.0 | "Les limites d'exérèse étaient saines." vs. "Les marges chirurgicales étaient saines." | Synonym pair for surgical margin; relevant for clinical entity normalization | IC
- **CLISTER-D5**: CLISTER | 58 | 0.0 | "Concernant la biographie familiale, nous sommes frappés par le nombre de décès par suicides violents (pendaison, noyade, ingestions médicamenteuses)..." | Psychiatric/social history context; shows breadth beyond urology/oncology | IC
- **CLISTER-D6**: CLISTER | 146 | 0.0 | "Cette patiente, suivie en psychiatrie pour des troubles de l'humeur bipolaires, avait arrêté son traitement au lithium (Teralithe LP® 400 mg, deux comprimés par jour)..." | Psychopharmacology context; psychiatric sub-domain coverage | IC
- **CLISTER-D7**: CLISTER | 176 | 0.0 | "Une glande thyroïde hypoplasique a été rapportée à l'échographie cervicale associée à la présence de deux masses..." | Endocrine/imaging case; illustrates specialty breadth | IC
- **CLISTER-D8**: CLISTER | 5 | 2.75 | "Le reste de l'examen échographique ne trouvait aucune autre anomalie." vs. "Le reste de l'examen somatique était sans anomalie." | Intermediate similarity; different exam modality with shared negative finding structure | OO
- **CLISTER-D9**: CLISTER | 75 | 1.25 | "La patiente a bénéficié d'une chimiothérapie adjuvante à base de six cures de paclitaxel et cisplatine." vs. "La patiente avait bénéficié d'une sclérothérapie lors de deux séances..." | Low similarity despite surface parallels; discriminates treatment type | OO
- **CLISTER-D10**: CLISTER | 8 | 1.0 | "Jour 45 - - - - - - - - - 25 μg 0,4 mg" vs. "Jour 53 15,13 12,0 1,58 - - - - - - 25 μg 0,4 mg" | Tabular medication dosing; temporal marker present but content is structured data not free text | IC
- **CLISTER-D11**: CLISTER | 41 | 2.0 | "Métoprolol 50 mg deux fois par jour;" vs. "Metformine 500 mg, 1 comprimé deux fois par jour" | Drug name, dosage, frequency; directly relevant to temporal medication extraction | IC
- **CLISTER-D12**: CLISTER | 93 | 1.0 | "Le patient a été perdu de vue." vs. "Le patient décède à J13." | Outcome divergence (lost to follow-up vs. death on day 13); clinically significant difference potentially underweighted by non-specialist annotators | OC
- **CLISTER-D13**: CLISTER | 126 | 4.0 | "Un patient de 42 ans, a été hospitalisé pour un UB de la main droite." | Clinical abbreviation "UB" (likely Buruli ulcer); domain expertise needed for reliable similarity annotation | OC
- **CLISTER-D14**: CLISTER | 169 | 4.0 | "Craquement douleur oedème + déviation du pénis" vs. "Craquement douleur oedème du pénis et des bourses" | Note-style shorthand, one of few examples resembling informal clinical notation | IC
- **CLISTER-D15**: CLISTER | 191 | 2.0 | "5 mg PO Q 4H PRN X" vs. "10 mg PO Q 4H PRN X X" | Pharmacy shorthand notation (PO=oral, PRN=as needed); structured rather than narrative free text | IC
- **CLISTER-D16**: CLISTER | 9, 29, 55, etc. | various | "lombalgies," "contact lombaire," "PSA," "hématurie," "rein," "uretère" (repeated across many pairs) | High frequency of urological terminology suggesting domain skew toward urology/oncology | IO
- **CLISTER-D17**: CLISTER | 8 | 1.0 | "Jour 45 - - - - - - - - - 25 μg 0,4 mg" | Table row, not a clinical sentence; degenerate STS input | IC
- **CLISTER-D18**: CLISTER | 163 | 5.0 | "Sheldon).\n\nLe patient subissait une chi miothérapie par Méthotrexate - Vinblastine - Endoxan -Cisplatine par voie" | Line-break mid-word artifact ("chi miothérapie"); OCR/PDF extraction noise in source material | IC
- **CLISTER-D19**: CLISTER | 75 | 1.25 | label=1.25 (float) | Non-integer label suggests variable annotator count or averaging artifact; potential label noise at boundary values | OO
- **MANTRAGSC-D1**: fr_emea | d42.u383 | 5 (DISO) | "Même s' il ne permettra pas de guérir la SEP, le traitement par Avonex peut contribuer à éviter que votre état ne s' aggrave." | French EMEA drug label tagging MS (SEP) as disease and Avonex as drug; confirms French biomedical NER coverage | IO, IC
- **MANTRAGSC-D2**: fr_medline | d800967.u1 | 5–6 (DISO), 1 (ANAT) | "Les manifestations oculo-palpébrales du syndrome de Lyell et du syndrome de Stevens-Johnson." | French Medline title labeling eponymous syndromes as DISO; confirms disorder entity coverage | IC, OO
- **MANTRAGSC-D3**: fr_medline | d20337124.u1 | 5 (DISO), 1 (ANAT) | "Paraparésie fébrile chez une Tunisienne : spondylite à cryptocoque avec atteinte médullaire." | French Medline title with disorder/anatomy labeling; mentions North African patient context | IC
- **MANTRAGSC-D4**: fr_emea | d61.u583 | 5–6 (DISO) | "Des symptômes potentiellement liés à l' histamine tels que éruption cutanée étendue, gonflement du visage et/ ou des lèvres, démangeaisons, sensation de chaleur ou difficulté à respirer, ont été rapportés." | Well-formed regulatory French with dense symptom NER; confirms formal register alignment | IF
- **MANTRAGSC-D5**: fr_patents | dEP-2114147-B1.u0020 | 5 (DISO) | "Composition pharmaceutique destinée à être utilisée selon la revendication 18 ou la revendication 19, dans laquelle la maladie ou l' état pathologique est la douleur." | French patent claim tagging disease entity; DISO label on "maladie" and "douleur" | OO
- **MANTRAGSC-D6**: fr_patents | dEP-1835922-B1.u0012 | 2 (CHEM) | "Combinaison selon l' une quelconque des revendications 1 à 7, dans laquelle ladite combinaison comprend 0,25 mg/kg d' agent (a) et 1 mg/kg d' agent (b)." | French patent text with sparse annotation; illustrates critically small training corpus | IC
- **MANTRAGSC-D7**: fr_medline | d5310889.u1 | 5–6 (DISO), 7 (LIVB) | "Accouchement d' une femme atteinte d' une maladie de Willebrand." | Published journal title; highly formal, no clinical shorthand; highlights register gap | IC, IO
- **MANTRAGSC-D8**: fr_emea | d16.u650 | 2 (CHEM), 7 (LIVB) | "Patients de 4 ans et plus dans l' incapacité d' avaler les capsules: la posologie recommandée d' Agenerase solution buvable est de 17 mg (1,1 ml)/ kg trois fois par jour..." | EMEA regulatory language; structured, formal, far from hospital EHR notes | IC
- **MANTRAGSC-D9**: fr_emea | d84.u182 | 13–14 (PROC) | "Traitement En cas d' ingestion récente, l' éventualité de provoquer un vomissement et d' effectuer un lavage gastrique devra être considérée." | Temporal word "récente" present but no temporal NER label exists in Mantra-GSC scheme | OO
- **MANTRAGSC-D10**: fr_medline | d15609920.u1 | 5–6 (DISO) | "Nouveautés dans la dysplasie ventriculaire droite arythmogène." | Single DISO class applied to cardiovascular disorder; no ICD-10 subcategory distinction | OO, OC
- **MANTRAGSC-D11**: de_emea | d42.u384 | 2 (CHEM), 5 (DISO) | "Die Behandlung mit Avonex kann helfen, eine Verschlechterung von MS zu verhindern, jedoch wird die Krankheit nicht geheilt." | German drug label; not relevant to French deployment; illustrates non-French config dominance | IC
- **MANTRAGSC-D12**: fr_medline | d303783.u1 | 1 (ANAT), 11 (PHYS) | "Rôle d' une fraction thymique insoluble dans la différenciation des lymphocytes T." | Anatomical entity labeled without clinical coding authority; illustrates annotation provenance concern | OC
- **MANTRAGSC-D13**: fr_medline | d7569194.u1 | 5–6 (DISO), 7 (LIVB) | "Luxation antérieure ouverte post-traumatique de la hanche chez l'enfant. A propos d'un cas et revue de la littérature." | Metropolitan French orthopedic case; no tropical/overseas pathology signal | IO
- **E3C-D1**: French_clinical | 195 | mixed NER | "Le bilan biologique montrait une cholestase (bilirubine totale a ` 140 mmol/L, bilirubine conjugue à 80 mmol/L, phosphatases alcalines à 700 UI/L) et une cytolyse..." | Dense clinical French with lab values — confirms register alignment with hospital documentation | IC
- **E3C-D2**: French_temporal | 107 | mixed NER | "Il s'agit d'une patiente de 44 ans, sans antécédent médico-chirurgical, qui a présenté depuis un an des céphalées, compliquées 08 mois après de crises d'épilepsies partielles..." | Multi-symptom temporally structured French narrative — confirms temporal extraction alignment | IC, OO
- **E3C-D3**: French_temporal | 107 | TIMEX3 tags | "depuis un an des céphalées, compliquées 08 mois après" (tokens tagged with TIMEX3-type labels) | Temporal duration expressions annotated — supports deployment's temporal entity extraction | OO
- **E3C-D4**: English_clinical | 81 | CLINENTITY | "The presence of terminal spine confirmed Schistosoma haematobium and a diagnosis of schistosomiasis was made." | Tropical parasitic pathology in English config — confirms tropical content structurally absent from French subset | IO, IC
- **E3C-D5**: French_clinical | 54 | B/I CLINENTITY | "Cet aspect évoquait une tumeur solide du péritoine." tokens tagged [0,0,0,0,1,2,0,0,0] | Multi-token pathology span ("tumeur solide") tagged in IOB2 — confirms NER output form alignment | OF, OO
- **E3C-D6**: English_clinical | 4 | B/I CLINENTITY | "As she suffered from acute respiratory distress syndrome and required mechanical ventilation..." tags [0,0,0,0,1,2,2,2,...] | Multi-token disease span annotation in B/I scheme — confirms annotation consistency | OF
- **E3C-D7**: Basque_clinical | 1 | O | "Azken hilabeteetan Ikernek kodeina + ibuprofenoa hartu ditu, baina ez du hobekuntza handirik nabaritu." | Basque language — entirely irrelevant to French deployment context | IO, IC
- **E3C-D8**: Basque_clinical | 13 | O | "Aurrekariak: - Krisi epileptikoa 12 urte zituenean, bere herrialdean tratatua: BOLIBIA." | Basque text referencing Bolivia — not relevant to French metropolitan hospital NLP | IC
- **E3C-D9**: French_clinical | 195 | mixed | "Le bilan biologique montrait une cholestase (bilirubine totale a ` 140 mmol/L..." | Well-formed published case report prose — contrasts with noisy active-hospital EHR shorthand | IC
- **E3C-D10**: French_clinical | 14 (id=253) | all O | "La fonction hépatique s'est améliorée avec un TP à 82% à l'arrêt du traitement." | Standard case report prose — no abbreviations or dictation noise; register mismatch with active EHR | IC
- **E3C-D11**: French_clinical | 2 (id=439) | all O | "La culture a isolé le germe Nocardia asteroides." all tags [0,0,0,0,0,0,0,0,0] | "Nocardia asteroides" (pathogen) not tagged as CLINENTITY — suggests annotation incompleteness | OC
- **E3C-D12**: French_clinical | 12 (id=478) | all O | "Le patient a été mis sous traitement par ciclosporine avec une évolution rapide vers une leucémie aigue myéloblastique." all tags [0,...,0] | Clear pathology and treatment entities untagged — annotation completeness concern | OC
- **E3C-D13**: English_clinical | 6 (id=81) | CLINENTITY | "a diagnosis of schistosomiasis was made" | Tropical disease in English config only; absent from French subset — confirms DOM-TOM pathology gap | IO
- **E3C-D14**: English_clinical | 4 (id=179) | B/I CLINENTITY | "acute respiratory distress syndrome" tagged as single CLINENTITY span, no sub-type | Coarse two-class annotation lacks pathology/anatomy/treatment distinction needed by deployment | OO
- **E3C-D15**: Basque_clinical | 6 (id=80) | O | "." tokens=['.'] ner_tags=[0] | Single-punctuation example — tokenization artifact, quality concern | IC, IF
- **E3C-D16**: Basque_clinical | 9 (id=82) | O | "." tokens=['.'] ner_tags=[0] | Second single-punctuation example — repeated artifact | IC, IF
- **PXCORPUS-D1**: PxCorpus | 75 | medical_prescription | "euh 2 le matin 2 le midi et 2 le soir" | Spoken filler in prescription; illustrates non-formal register | IC, IF
- **PXCORPUS-D2**: PxCorpus | 169 | medical_prescription | "lamotrigine 25 milligrammes euh p/ combien" | Incomplete utterance with filler and truncated word; spoken transcription noise | IC, IF
- **PXCORPUS-D3**: PxCorpus | 3 | none | "/chet" | Single garbled transcription artifact labeled 'none' | IC, IF
- **PXCORPUS-D4**: PxCorpus | 10 | negate | "ne pas tenir compte à midi tous les jours merd/" | Truncated word at end; raw transcription behavior | IC
- **PXCORPUS-D5**: PxCorpus | 5 | medical_prescription | "primperan 10 milligrammes comprimés 1 comprimé en cas de nausée toutes les 8 heures pendant 14 jours" | Dense temporal + drug NER: frequency and duration annotated | IO, OO
- **PXCORPUS-D6**: PxCorpus | 93 | medical_prescription | "becotide 250 milligrammes 2 bouffées à 7 heures 2 bouffées à 11 heures 2 bouffées à 15 heures 2 bouffées à 18 heures pendant 6 mois" | Four specific time-of-day administrations + duration; complex temporal NER | IO, OO
- **PXCORPUS-D7**: PxCorpus | 174 | medical_prescription | "cordarone 3 comprimés par jour pendant 10 jours puis 1 comprimé tous les 2 jours pendant 4 semaines" | Multi-phase temporal prescription with sequential frequency change | IO, OO
- **PXCORPUS-D8**: PxCorpus | 4 | replace | "attention il s'agit de 20 milligrammes et pas 10 milligrammes" | Prescription correction intent; clinically relevant for error detection | IO, OC
- **PXCORPUS-D9**: PxCorpus | 8 | replace | "remplacer 1 comprimé tous les jours par 1 comprimé en cas d'anxiété" | Substitution intent with condition-triggered dosing | IO, OC
- **PXCORPUS-D10**: PxCorpus | 6 | negate | "supprimer à midi tous les jours" | Negation/removal directive for dosing slot | IO, OC
- **PXCORPUS-D11**: PxCorpus | 97 | medical_prescription | "morphine 10 milligrammes toutes les 4 heures pendant 2 mois" | Opioid pain management prescription; broad drug class coverage | IC
- **PXCORPUS-D12**: PxCorpus | 173 | medical_prescription | "aranesp 30 microgrammes 1 injection par semaine en sous-cutanée pendant 4 semaines" | Subcutaneous injectable prescription; route diversity | IC
- **PXCORPUS-D13**: PxCorpus | 190 | medical_prescription | "loxapac ampoules 50 milligrammes 3 ampoules intramusculaire 2 fois par jour pendant 3 jours" | Intramuscular antipsychotic; confirms route coverage | IC
- **PXCORPUS-D14**: PxCorpus | 2 | negate | "c'est 2 pourcent le collyre" | Surface reads like prescription; labeled negate — ambiguity in minority class | OO, OF
- **PXCORPUS-D15**: PxCorpus | buffer | — | negate=11, replace=3 in 500 sampled | Severe class imbalance; majority-class baseline masks minority-class performance | OO, OF
- **PXCORPUS-D16**: PxCorpus | 5 | medical_prescription | NER tags: dose, form, frequency, duration, symptom only | No PATHOLOGY/DIAGNOSIS entity in tag scheme; ICD-10 mapping untestable | IO, OO
- **PXCORPUS-D17**: PxCorpus | 104 | medical_prescription | "en cas d'anxiété" | Anxiety as unlabeled trigger, not classified to ICD-10 axis | IO, OO
- **PXCORPUS-D18**: PxCorpus | 18 | none | "la partie euh posologie est sur 6 ou 8 semaines là il n'est écrit que 8 semaines par contre le qsp 6 semaines a été rajouté en remarque pharmaceutique" | Pharmacist meta-commentary labeled 'none'; heterogeneous class content | OO, OC
- **PXCORPUS-D19**: PxCorpus | 88 | none | "i'll agree come on say avec successes merde je vais roulé faut lui faire un et mettre la rame en mode français" | Mixed French/English system setup dialogue labeled 'none' | OO, IC
- **PXCORPUS-D20**: PxCorpus | 54 | none | "ouah" | Single exclamation labeled 'none'; degenerate example | OO
- **PXCORPUS-D21**: PxCorpus | 33 | none | "perfusion" | Isolated clinical term labeled 'none'; ambiguous classification | OO
- **PXCORPUS-D22**: PxCorpus | 207 | medical_prescription | "teralithe 250 milligrammes / le serveur de dialogue met beaucoup de temps à comprendre votre énoncé veuillez reformuler différemment teralithe 250 milligrammes 2 comprimés matin et soir pendant 1 mois" | System prompt embedded in prescription utterance; corrupts register | IC, IF
- **PXCORPUS-D23**: PxCorpus | 62 | none | "le médicament mais pas le bon le système ne m'a pas compris le bon médicament et le 10 antalvic en gélules" | User commentary about ASR failure; non-clinical register | IC, IF
- **PXCORPUS-D24**: PxCorpus | 34 | medical_prescription | "3 mois" | Duration fragment only; degenerate prescription example | IC
- **PXCORPUS-D25**: PxCorpus | 53 | medical_prescription | "roxithromycine" | Drug name only; no context for full NER | IC
- **PXCORPUS-D26**: PxCorpus | 59 | medical_prescription | "30 jours" | Duration fragment only | IC
- **PXCORPUS-D27**: PxCorpus | 119 | medical_prescription | "tropatepine chloridrate 1o milligrammes 1 comprimé le midi" | "1o" instead of "10" — ASR/OCR artifact in dose quantity | IC
- **PXCORPUS-D28**: PxCorpus | 103 | medical_prescription | "trémétadisine trémétasidine à 20 milligrammes à 3 comprimés par jour pendant 3 semaines" | Probable ASR duplication of drug name | IC
- **DIAMED-D1**: DiaMED | 1 | A00-B99 | "Le test rapide VIH était positif, confirmé par la sérologie VIH avec un taux de CD4 à 27/mm3" | Confirmed HIV infection with CD4 count — supports infectious disease label | OO, IC
- **DIAMED-D2**: DiaMED | 2 | C00-D49 | "L'examen anatomopathologique de la pièce opératoire montrait une prolifération tumorale faite de travées, de cordons" | Histopathological finding of tumoral proliferation — confirms neoplasm label | OO, IC
- **DIAMED-D3**: DiaMED | 9 | I00-I99 | "La troponine I était élevée à quatre fois la normale et les ASAT à 5 fois la normale. La glycémie, l'ionogramme sanguin, l'hémogramme et la créatininémie étaient normaux." | Rich laboratory entities with quantitative values in standard French medical register | IC, IF
- **DIAMED-D4**: DiaMED | 11 | K00-K95 | "L'ionogramme sanguin avait révélé une hypokaliémie à 2,8 mmol/l et une hyponatrémie à 128 mmol/l." | Quantified electrolyte findings — confirms clinical entity density and standard terminology | IC
- **DIAMED-D5**: DiaMED | 8 | H60-H95 | "Le diagnostic d'otite externe maligne avait été posé et une antibiothérapie injectable empirique instaurée" | Ear disease case confirming H60-H95 class representation | IO
- **DIAMED-D6**: DiaMED | 5 | F01-F99 | "Devant le contexte de dépression, la patiente a été adressée en psychiatrie où ce diagnostic a été confirmé" | Psychiatric case confirming mental/behavioral disorder class | IO
- **DIAMED-D7**: DiaMED | 9 | I00-I99 | "Communication interventriculaire ischémique: à propos d'un cas observé dans le service de cardiologie du CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" | Explicitly Burkinabe hospital origin — non-metropolitan French clinical setting | IC, OC
- **DIAMED-D8**: DiaMED | 12 | L00-L99 | "À propos d'un cas clinique … keywords: ['Niamey']" | Niger-based case — sub-Saharan African clinical context, not metropolitan France | IC, OC
- **DIAMED-D9**: DiaMED | 3 | D50-D89 | "keywords: ['Rate', 'abdomen aigu', 'scanner abdominal', 'chirurgie', 'Maroc']" | Moroccan clinical case — North African origin rather than French metropolitan | IC, OC
- **DIAMED-D10**: DiaMED | 11 | K00-K95 | "Le traitement était constitué d'énoxaparine d'antiagrégant plaquettaire, de diurétique de l'anse, de dérivés morphiniques et d'oxygène" | Multi-system case forced into single digestive label — masks multi-morbidity | OO, OF
- **DIAMED-D11**: DiaMED | 1 | A00-B99 | "Maladie de Kaposi à localisation broncho-pulmonaire révélant une infection VIH" | Chapter-level label only; PMSI granular codes (e.g., B21.x) not evaluated | OO
- **DIAMED-D12**: DiaMED | 6 | G00-G99 | "L'examen clinique révélait une paralysie flasque aréflexique avec amyotrophie importante des membres inférieurs. On notait la présence de quelques trépidations épileptoïdes du pied gauche." | Polished academic prose — formal register unlike noisy active-hospital EHR notes | IC
- **DEFT2021-D1**: DEFT2021/cls | 5 (train) | specialities=[12,3,20,4,7,5] | "Un homme de 42 ans était hospitalisé en urgence le 10 décembre 2003 dans le service de gastro-entérologie pour un tableau d'hépatite aiguë" | Multi-morbid hepatology/toxicology/psychiatry case with 6 concurrent MeSH labels | IO, OO
- **DEFT2021-D2**: DEFT2021/cls | 8 (train) | specialities=[20,17,22,13,0,4,19] | "Nous rapportons le cas d'un garçon de huit ans [...] microangiopathie thrombotique secondaire à un syndrome hémolytique urémique (SHU) atypique" | 7-label pediatric multi-morbid case illustrating complex label overlap | IO, OO
- **DEFT2021-D3**: DEFT2021/ner | 7 (train) | TREATMENT+DURATION | "cotrimoxazole pour 10 jours" | Treatment drug with duration span annotated — confirms temporal treatment labeling | IO, OO
- **DEFT2021-D4**: DEFT2021/ner | 55 (train) | TREATMENT+DOSAGE+MODE+FREQUENCY | "Hydrocortisone 300 mg IV immédiatement ; Traitement Hydroxyzine 25 mg par voie orale toutes les 6 heures" | Multiple entity types co-occurring in a single sentence, confirming NER scheme coverage | IO, OO
- **DEFT2021-D5**: DEFT2021/ner | 63 (train) | DATE | "Au jour 42 , une deuxième désensibilisation a eu lieu" | Temporal anchor (relative day) labeled, confirming temporal entity extraction alignment | IO, OO
- **DEFT2021-D6**: DEFT2021/cls | 3 (train) | specialities=[6,14,13,19,4] | "La proarythmie cardiaque constitue l'un des effets indésirables les plus dangereux résultant d'interactions médicamenteuses délétères" | Complex pharmacotherapy reasoning case with rich clinical terminology | IC
- **DEFT2021-D7**: DEFT2021/cls | 5 (train) | specialities=[12,3,20,4,7,5] | "bilan biologique d'entrée révélait une macrocytose avec une thrombopénie, un cytolyse majeure avec des ALAT et des ASAT respectivement à 60 à 450 fois la normale" | Dense laboratory values with quantified severity signals | IC
- **DEFT2021-D8**: DEFT2021/cls | 7 (train) | specialities=[17,4,6] | "B.A., âgé de 20 ans a été admis [...] tuberculose uro-génitale" | Infectious disease + urology multi-specialty case | IO
- **DEFT2021-D9**: DEFT2021/cls | 4 (train) | specialities=[15,4,3] | "un coma inexpliqué, avec un score de Glasgow (GS) à 3/15 [...] injection intraveineuse de poudre 'NRG'" | Emergency medicine + toxicology case | IO
- **DEFT2021-D10**: DEFT2021/ner | 28 (train) | PATHOLOGY (multi-span) | "carcinome urothélial multiple [...] carcinome vésical droit [...] carcinome urétéral multifocal" | Complex oncological case with multiple distinct pathology spans annotated | OO, IF
- **DEFT2021-D11**: DEFT2021/cls | 8 (train) | specialities_one_hot | "[1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0]" | Strictly binary 0/1 label vector — no confidence or soft-label dimension present | OO, OF
- **DEFT2021-D12**: DEFT2021/ner | 56 (train) | PATHOLOGY | "hydatidose" | Parasitic disease labeled, but temperate/Mediterranean — not DOM-TOM tropical pathology | IO, OC
- **DEFT2021-D13**: DEFT2021/cls | 7 (train) | specialities=[17,4,6] | "tuberculose uro-génitale" | Tuberculosis in metropolitan urology context — no DOM-TOM tropical disease specificity | IO
- **DEFT2021-D14**: DEFT2021/ner | 17 (train) | O | "L' ECBU était stérile ." | Standard abbreviation in complete sentence — published case report register, not raw EHR shorthand | IC
- **DEFT2021-D15**: DEFT2021/cls | 9 (train) | specialities=[18,4,13] | "Il s'agit d'une jeune patiente âgée de 18 ans, longiligne et sans antécédents notables admise pour insuffisance rénale chronique terminale secondaire à une néphropathie tubulointerstitielle chronique" | Fully formed syntactic sentence — register cleaner than active hospital notes | IC
- **DEFT2021-D16**: DEFT2021/cls | 3 (train) | specialities=[6,14,13,19,4] | (see D6 excerpt) | Multi-drug cardiac case; annotator PMSI credential unknown — label authority concern | OC
- **DEFT2021-D17**: DEFT2021/cls | 10 (train) | specialities=[3] | "Une femme de 29 ans est victime d'agression sexuelle. Des prélèvements de sérum et d'urine sont réalisés aux fins de 'recherche d'alcoolémie'" | Single-label toxicology case — with 23 axes over 275 cases, some axes have very few positives | IO, OC
- **DEFT2021-D18**: DEFT2021/ner | 23 (train) | O | "Mr ." | Single-token patient initial fragment — no annotatable entity content | IC
- **DEFT2021-D19**: DEFT2021/ner | 31 (train) | O | "O ." | Single-character fragment — degenerate NER example | IC
- **DEFT2021-D20**: DEFT2021/cls | 8 (train) | specialities=[20,17,22,13,0,4,19] | "Au jour 0, le jeune patient reçoit de l'acétaminophène 300 mg par voie orale" | "Acétaminophène" (Quebec French) vs. "paracétamol" (metropolitan French) — minor regional lexical divergence | IC, IF
- **CAS-D1**: CAS/cls | Ex. 3 | neutral | `"l' examen clinique montre un état général conservé ."` | Standard French clinical examination notation | IC, IF
- **CAS-D2**: CAS/cls | Ex. 26 | neutral | `"les constantes hémodynamiques étaient stables mais le bilan biologique mettait en évidence une anémie à 5 , 7 g / 100ml d' hb , une hyponatrémie à 128 meq / l , une acidose métabolique..."` | Dense lab-value notation typical of deployment's severity signal extraction | IC
- **CAS-D3**: CAS/pos | Ex. 7 | — | `"ce patient a présenté de façon brutale , une douleur thoracique aigue à type de constriction associée à une cyanose des extrémités et une hémoptysie de moyenne abondance évoluant vers une syncope ."` | Acute onset clinical narrative with temporal qualifier | IC, IO
- **CAS-D4**: CAS/ner_neg | Ex. 11 | — | `"la dernière prise remontait à sept jours ."` | Relative temporal reference to last medication intake | IC
- **CAS-D5**: CAS/cls | Ex. 29 | neutral | `"le scanner réalisé 1 , 5 mois après , devant la persistance de douleurs abdominales , détectait une image kystique liquidienne de 10 × 7cm accolée à la queue du pancréas"` | Temporal sequencing in imaging diagnosis narrative | IC
- **CAS-D6**: CAS/cls | Ex. 35 | neutral | `"quinze mois après cette cytolyse spontanément résolutive , le bilan hépatique est normal ."` | Follow-up temporal anchor in clinical timeline | IC
- **CAS-D7**: CAS/cls | Ex. 10 | negation | `"les ovaires ne montraient pas d' anomalie ."` | Canonical negation pattern for absent clinical finding | IO, OO
- **CAS-D8**: CAS/cls | Ex. 17 | negation_speculation | `"Les caractères morphologiques et le profil immunohistochimique ne permettaient pas de trancher entre l' hypothèse d' une dissémination péritonéale..."` | Complex combined negation+speculation in oncological differential diagnosis | IO, OC
- **CAS-D9**: CAS/ner_neg | Ex. 14 | tags [0,0,0,1,0,2,2,0] | `"les ovaires ne montraient pas d' anomalie ."` | NER annotation marking negation trigger and scope in IOB2 | OO
- **CAS-D10**: CAS/cls | Ex. 45 | speculation | `"l' atteinte marquée de l' état général , la température à 40 ° c évoquent d' emblée une shigellose ."` | Infectious disease differential (metropolitan pathogen) | IC, IO
- **CAS-D11**: CAS/cls | Ex. 51 | speculation | `"son score chads2 ( insuffisance cardiaque congestive , hypertension , âge ≥ 75 ans , diabète et avc ou accident ischémique transitoire ) est de 3 ."` | Multi-morbidity cardiology risk scoring | IC
- **CAS-D12**: CAS/cls | Ex. 36 | speculation | `"La présence de ces calcosphérites faisait suspecter une carcinomatose péritonéale d' origine ovarienne ."` | Oncological diagnostic reasoning with epistemic hedge | IC
- **CAS-D13**: CAS/pos | Ex. 15 | — | `"Il s' agit d' une patiente âgée de 54 ans ayant des facteurs de risque de transmissions virales hépatiques..."` (full long sequence with pos_tags) | Complex clinical case sentence with full 82-token POS annotation sequence | IO, OF
- **CAS-D14**: CAS/cls | Ex. 38 | neutral | `"depuis hier soir , je suis essouflé , j' ai des frissons , j' ai mal à la poitrine , là en bas à gauche , surtout quand j' inspire à fond ."` | First-person patient narrative with minor spelling error ("essouflé") | IC
- **CAS-D15**: YAML Q42 | — | — | "annotated for POS tagging with 31 classes using automatic annotations through Tagex 3...yielded 98% precision" | Silver-standard label provenance for POS config | OC
- **CAS-D16**: CAS/cls | Ex. 9 | negation_speculation | `"il avait été retrouvé dans la rue , mais il se donne successivement plusieurs professions , semblant ne pas se souvenir de celle qu' il a citée quelques instants avant ."` | Ambiguous negation+speculation requiring expert judgment; no IAA documented | OC
- **CAS-D17**: CAS/cls | Ex. 12 | speculation | `"Cholstat ® 0.1 ."` | Drug name/dosage fragment labeled as speculation with no apparent epistemic marker; annotation rationale opaque | OC, OO
- **CAS-D18**: CAS/ner_neg | Ex. 25 | all-O | `"la coproculture avec ensemencement de milieux sélectifs pour salmonella , shigella et campylobacter spp ."` | Metropolitan enteric pathogen workup; no tropical disease vocabulary present | IO
- **CAS-D19**: HF Metadata | — | — | label_names: ["negation_speculation", "negation", "neutral", "speculation"] | Classification labels measure linguistic modality, not ICD-10 pathology categories | OO
- **CAS-D20**: CAS/cls | Ex. 34 | negation | `"vous êtes appelés au secours d' une infirmière de nuit pour confusion chez un patient bronchopathe chronique , tabagique non sevré à 70 paquets-années ."` | Narrative clinical description; more formal than raw EHR shorthand | IC
- **CAS-D21**: HF Metadata | — | — | buffer: negation_speculation:6, negation:100, neutral:368, speculation:26 | Heavy class imbalance; neutral dominates at ~74% | OO
- **ESSAI-D1**: ESSAI/cls | 1 | negation_speculation | "chimiothérapie à hautes doses avec une combinaison de Busulfan et de Melphalan (BU-MEL) permettra d'obtenir une survie sans événement à 3 ans" | Formal clinical trial protocol language matching deployment register | IC/IF
- **ESSAI-D2**: ESSAI/cls | 10 | negation | "l'objectif de cette étude de recherche clinique est d'évaluer la sécurité d'emploi et l'efficacité de l'avelumab (MSB0010718C) associé aux meilleurs soins palliatifs chez des patients atteints d'un adénocarcinome de l'estomac" | Structured formal French biomedical prose with drug and pathology terms | IC/IF
- **ESSAI-D3**: ESSAI/cls | 6 | negation | "ne présentent pas plus d'effets secondaires dans différents essais cliniques" | Explicit negation of side effects — relevant to safety signal extraction | IO
- **ESSAI-D4**: ESSAI/cls | 36 | speculation | "l'addition de la radiothérapie à la chirurgie semble améliorer le contrôle local des sarcomes rétropéritonéaux" | Speculation marker "semble" on treatment benefit — relevant to claim credibility | IO
- **ESSAI-D5**: ESSAI/cls | 32 | speculation | "le bénéfice de l'association lénalidomide + R-CHOP au rapport au R-CHOP reste à démontrer" | Speculation framing of unproven treatment benefit | IO
- **ESSAI-D6**: ESSAI/ner_neg | 6 | (O-sequence) | "ce traitement qui sera administré toutes les deux semaines sous forme de perfusion d'une heure" | Temporal dosing expression relevant to treatment timeline extraction | IC
- **ESSAI-D7**: ESSAI/ner_spec | 14 | (O-sequence) | "On prévoit de réaliser 6 cycles maximum" | Treatment cycle quantification — temporal entity content | IC
- **ESSAI-D8**: ESSAI/ner_spec | 17 | (O-sequence) | "Des scanners d'évaluation seront réalisés toutes les 8 semaines" | Follow-up scheduling temporal expression | IC
- **ESSAI-D9**: ESSAI/cls | 3 | neutral | "Essai clinique d'immunothérapie évaluant l'association du galunisertib (un facteur de croissance transformant β), avec l'anticorps anti-PD-L1 durvalumab (MEDI4736), dans le cancer du pancréas métastatique" | Rich pathology content labeled only for negation/speculation, not ICD-10 — output ontology mismatch | OO
- **ESSAI-D10**: ESSAI/ner_spec | 10 | (sparse NER) | "traitement par un inhibiteur de PARP, le talazoparib, peut être plus efficace... chez les patients atteints de un cancer du sein métastatique, porteurs de une mutation de BRCA1" | Highly specialized oncogenomics — narrow subdomain not representative of general hospital notes | IC
- **ESSAI-D11**: ESSAI/cls | 20 | speculation | "utilisation de l'oxygène à haut débit humidifié chez les patients immunodéprimés avec un problème respiratoire nécessitant de l'oxygène admis en réanimation" | Clinical trial framing even for ICU content — not raw hospital note register | IC
- **ESSAI-D12**: ESSAI/ner_neg | 11 | NER (sparse) | "en l'absence d'atteinte ganglionnaire chez les femmes ménopausées" (tags: [0,...,2,3,...]) | Only "atteinte ganglionnaire" tagged; annotation completeness and expert authority undocumented | OC
- **ESSAI-D13**: ESSAI/cls | 19 | neutral | "Chaque cycle dure 28 jours" | Trivially neutral sentence — inflates neutral class count, contributing to severe label imbalance | OC
- **ESSAI-D14**: ESSAI/ner_neg | 1–10 | all O | "avec la combinaison gemcitabine + abraxane, chez des patients avec un cancer du pancréas" (and 9 similar) | Consecutive all-zero NER sequences despite clinically relevant content — sparse annotation density | OO
