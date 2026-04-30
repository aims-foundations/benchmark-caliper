## Deployment Context

**Use case:** In a pharmaceutical setting, a regulatory specialist uses document management software to ensure compliance in French drug labeling and scientific abstracts by applying a model evaluated on semantic textual similarity and fine-grained named-entity recognition. The system identifies over a dozen types of precise entities, such as chemical compounds and dosage modes, while verifying that safety warnings across different leaflets or patents are semantically consistent. These results determine whether pharmacological documentation meets strict professional standards for official submission or requires manual revision to prevent regulatory non-compliance.
**Target population:** Regulatory affairs specialists, pharmacologists, and legal experts at pharmaceutical companies or government health agencies.

# Validity Analysis: drbenchmark
**Target context:** EU Pharmaceutical Regulatory NLP — French
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

DrBenchmark is the largest French biomedical NLU benchmark and provides genuine value for general French biomedical model selection [Q83], but it is severely misaligned with the EU pharmaceutical regulatory NLP deployment on the four HIGH-priority dimensions identified in the elicitation. Output Ontology (score 1) is the most critical concern: NER schemas use clinical UMLS Semantic Groups that conflate INN, excipients, and brand names under CHEM (QUAERO-D15, MANTRAGSC-D15), provide no ATC code class [WEB-11], no contraindication qualifier class (QUAERO-D21, PXCORPUS-D15), and systematically O-tag dose values (QUAERO-D18, E3C-D7); STS is calibrated for general semantic proximity rather than regulatory equivalence, demonstrably treating legally material differences as near-synonymy (CLISTER-D13: 2× numeric difference scored 4.0; DEFT2020-D18: dropped 'congénitale' scored 4.6). Input Ontology (score 2) and Input Content (score 2) reflect the absence of SmPC, CTD module, and EU-RMP genres — QUAERO EMEA's ~10 segmented PIL documents [WEB-3, WEB-4] are the only confirmed regulatory-genre source. Output Content (score 2) reflects systematically misaligned annotator populations (academic NLP and clinical, no regulatory-affairs specialists [Q8]) with empirical variance evidence (DEFT2020-D10, DEFT2020-D22). Input Form (score 4) and Output Form (score 4) are well-aligned — both deployment and benchmark are text-only French Latin-script with compatible output representations. The benchmark can support model selection at the foundational French-biomedical-LM level, but cannot validate deployment-grade regulatory NER or regulatory-equivalence STS without substantial supplementation.

## Practical Guidance

### What This Benchmark Measures

DrBenchmark measures general French biomedical language understanding across NER, STS, classification, MCQA, and POS tagging on clinical, research, and pharmacy-exam text. For this deployment, it provides useful signal on (a) which French biomedical MLM has the best general performance profile (DrBERT-FS, DrBERT-CP, CamemBERT-bio per [Q60–Q62]), (b) coarse-grained pharmaceutical NER on EMEA-genre patient leaflets via QUAERO (QUAERO-D1–D15), and (c) baseline French biomedical STS variance behavior via CLISTER and DEFT2020. The strongest dimensions for this deployment are Input Form and Output Form — both at score 4.

### Construct Depth

The benchmark probes general French biomedical NLU constructs at moderate depth, but does not probe the regulatory-specific constructs the deployment requires. NER probes clinical entity recognition (UMLS Semantic Groups, MeSH chapters, ICD-10 chapters) — not regulatory entity recognition (INN as distinct from CHEM, ATC codes, excipient names, EMA-templated posology, contraindication qualifiers). STS probes general clinical sentence similarity — not regulatory equivalence. Empirically, pharmaceutical content is broadly present in the inputs but is systematically unannotated or under-annotated (E3C-D7, QUAERO-D18, CAS-D13). The benchmark's 75% top-task win rate for domain-specialized models [Q62] does not translate to regulatory-grade precision (per [WEB-12]: general biomedical NLP systems require modification for regulatory use).

### What Else You Need

To complete this assessment for regulatory deployment, the user needs: (1) An OO supplement — a regulatory entity schema (INN, ATC, excipient, posology template, contraindication qualifier) and a regulatory-equivalence STS rubric calibrated for dose-threshold and population-qualifier sensitivity; neither exists in published literature (gap_id 3 confirmed). (2) An IO/IC supplement — a held-out evaluation set of authentic SmPC, CTD module narrative, and EU-RMP text under QRD v10.4 [WEB-7], since QUAERO EMEA covers only PIL register and ~10 segmented documents. (3) An OC supplement — re-annotation of a sample of QUAERO EMEA and CLISTER pairs by regulatory-affairs specialists to quantify the gap between biomedical NLP annotation norms and EMA/ANSM judgments (anticipated per A4). (4) Empirical evaluation against the Kadi et al. 2025 SmPC IDMP extraction baseline [WEB-11] for ATC and excipient extraction, which is field-wide unsolved.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
DrBenchmark's task taxonomy (POS, NER, MCQA, MCC, MLC, STS) [Q81] is calibrated for clinical and biomedical research NLP rather than the EU regulatory workflow. The deployment requires NER and STS over EMA/ANSM regulatory document genres (SmPCs, CTD modules, EU-RMPs, PILs), and these document categories do not appear as explicit task categories in the benchmark. While QUAERO EMEA and Mantra-GSC EMEA/Patents provide partial PIL/patent overlap [Q34, Q40], the majority of tasks (FrenchMedMCQA, MORFITT, DiaMED, CAS POS, ESSAI POS, E3C) involve task types or genres orthogonal to the deployment's NER/STS regulatory compliance functions. This is a HIGH-priority dimension per the elicitation, and the gap is substantial — though not total, since QUAERO and CLISTER provide partial NER and STS coverage on biomedical French.

**Strengths:**
- Task inventory does include both NER and STS — the two task types the deployment needs [Q1, Q4, Q18]
- QUAERO EMEA NER provides authentic EMA package leaflet text in regulatory register, the only confirmed regulatory-genre source (QUAERO-D1, QUAERO-D2, QUAERO-D14)
- Mantra-GSC includes EMEA and Patents NER configurations that are documented as deployment-relevant genres [Q40]
- The benchmark's diversity across 20 tasks gives broad signal for French biomedical model selection [Q83]

**Checklist:**

- **IO-1**: The deployment requires NER (entity extraction over INNs, ATC codes, excipients, posology, contraindication qualifiers) and STS (regulatory equivalence scoring for safety warnings) over SmPCs, PILs, CTD modules, and EU-RMPs. These task categories partially exist in the benchmark (NER, STS) but are calibrated for clinical/research text, not regulatory genres [Q81], [WEB-7]. — _Sources: Q81, Q1, Q4, WEB-7_
- **IO-2**: Regulatory document genres (SmPC, CTD, EU-RMP) are absent as explicit task categories. The benchmark's only confirmed regulatory-genre source is QUAERO EMEA (~10 segmented PIL documents) [WEB-3, WEB-4]. SmPC, CTD module, and EU-RMP text are not documented as data sources [Q34]. Regulatory equivalence as a distinct STS sub-task is absent. — _Sources: Q34, WEB-3, WEB-4_
- **IO-3**: Several included tasks are largely orthogonal to the deployment: FrenchMedMCQA (closed-option exam QA) (FRENCHMEDMCQA-D11, FRENCHMEDMCQA-D13), MORFITT (specialty classification of research abstracts) (MORFITT-D6, MORFITT-D8), DiaMED (ICD-10 chapter classification of African clinical cases) (DIAMED-D1, DIAMED-D9), and CAS/ESSAI POS-only configs (CAS-D13, ESSAI-D18). These contribute to benchmark scores but consume evaluation effort without testing deployment-relevant capabilities. — _Sources: FRENCHMEDMCQA-D11, MORFITT-D6, DIAMED-D1, CAS-D13, ESSAI-D18_
- **IO-4**: Documented gaps: no SmPC genre, no CTD module narrative tasks, no EU-RMP tasks, no IDMP-aligned structured-extraction tasks [WEB-16, WEB-17], no regulatory-equivalence STS sub-task. These omit core categories needed for content validity in the EU pharmaceutical regulatory deployment. — _Sources: Q81, WEB-16, WEB-17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q81] 'aggregating the tasks into one of the five designated categories: POS, NER, MCQA, MCC (Multi-class classification), MLC (Multi-label classification), or STS tasks' (p.8)
- [Q83] 'the first large language understanding benchmark tailored for the French biomedical domain' (p.9)
- [Q34] 'two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE' (p.3)
- [Q40] 'Medline (11 classes), and EMEA and Patents (10 classes)' (p.4)

*Web sources:*
- [WEB-3] QUAERO EMEA HuggingFace dataset card confirms PIL register, not SmPC
- [WEB-4] QUAERO official corpus page documents EMEA and MEDLINE as the two source genres
- [WEB-7] EMA QRD templates page confirms SmPC/PIL templates as the regulatory document standard
- [WEB-16] IQVIA NLP regulatory affairs factsheet confirms IDMP structured-extraction requirements
- [WEB-17] Linguamatics IDMP blog confirms ~70% of IDMP attributes reside in unstructured text

*Dataset analysis:*
- FRENCHMEDMCQA-D11: closed-option recall task produces no NER spans or STS scores
- MORFITT-D6: research abstract with no entity-level or similarity ground truth
- DIAMED-D1: ICD-10 chapter classification, not NER or STS
- CAS-D13: drug INNs annotated only for POS, not regulatory entities
- ESSAI-D18: 'effets indésirables' POS-tagged only, not entity-labelled

</details>

**Information gaps:**
- Whether any French NLP benchmark targeting SmPC/CTD/EU-RMP genres exists outside DrBenchmark — searches found none (gap_id 7 RESOLVED as confirmed gap)
- Pair count and source-genre split for DEFT-2020 STS subtask not stated in the paper

**Requires expert verification:**
- Whether the deployment's CTD module supplementary template layer can fully compensate for the absence of CTD-genre evaluation in the benchmark

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
While the benchmark contains broad French pharmaceutical lexical coverage (INNs, dosages, routes, formulations) across multiple datasets (QUAERO-D7, ESSAI-D2, DEFT2021-D3, E3C-D1, CAS-D2), the document genres and registers are predominantly clinical case reports, clinical trial protocols, research abstracts, and spoken prescriptions — all distinct from the formal, QRD-template-constrained EMA regulatory register the deployment targets. QUAERO's EMEA sub-corpus is the only confirmed authentic EMA-document source and covers PILs, not SmPCs (~10 segmented documents) [WEB-3, WEB-4]. Multiple datasets contain non-EMA-jurisdiction content from sub-Saharan Africa, North Africa, Canada, and Middle East (DIAMED-D9, MANTRAGSC-D16, MORFITT-D11, MORFITT-D12, MORFITT-D13, E3C-D15, E3C-D16), introducing construct-irrelevant variance. PxCorpus introduces transcribed-speech artifacts (PXCORPUS-D11, PXCORPUS-D13) that have no analogue in regulatory documents. Brand-name predominance over INNs in PxCorpus (PXCORPUS-D19, PXCORPUS-D20) conflicts with EMA INN-primacy requirements. IC is HIGH priority per the elicitation, and the content register and entity-density profile are systematically misaligned with regulatory prose.

**Strengths:**
- Broad French pharmaceutical vocabulary represented across diverse contexts: INNs, dosages, routes, formulations [Q19], (QUAERO-D7, ESSAI-D2, DEFT2021-D3)
- QUAERO EMEA contains authentic EMA leaflet text with authorization headers, full excipient lists with E-numbers, and contraindication statements (QUAERO-D1, QUAERO-D4, QUAERO-D11, QUAERO-D14)
- ESSAI clinical trial protocols contain dense INN + posology vocabulary closer to regulatory text than other clinical sources (ESSAI-D2, ESSAI-D4)
- DEFT2020 STS includes drug-leaflet sentence pairs with named INNs and safety/contraindication content (DEFT2020-D1, DEFT2020-D2, DEFT2020-D7)

**Checklist:**

- **IC-1**: The deployment requires regulatory French in EMA QRD-templated register; the benchmark predominantly contains clinical and research French. The QRD template mandates standardized phrasing 'whenever they are applicable' [WEB-2, WEB-7], but no DrBenchmark corpus is documented as covering this template-constrained register. Sentence-splitting of EMEA documents [Q37] further removes document-level regulatory context (DEFT2020-D21). — _Sources: Q37, WEB-2, WEB-7, DEFT2020-D21_
- **IC-2**: EMA/ANSM regulatory culture is well-defined and does not raise sensitive-content concerns; however, the cultural fit issue is reversed — the benchmark contains content from non-EU jurisdictions that dilutes IC validity (DIAMED-D9: Burkina Faso; MORFITT-D11: Saudi Arabia; MORFITT-D12: Egypt; MORFITT-D13: Jordan; MANTRAGSC-D16: Dakar; E3C-D16: Morocco). — _Sources: DIAMED-D9, MORFITT-D11, MORFITT-D12, MORFITT-D13, MANTRAGSC-D16, E3C-D16_
- **IC-3**: The deployment is itself within Western/EU regulatory culture, so the standard 'Western knowledge bias' framing inverts here. The relevant concern is whether the benchmark's content reflects EU-specific regulatory framing — and largely it does not, as much content is research/clinical rather than regulatory (CLISTER-D11, E3C-D11, MORFITT-D8). Brand name vs. INN convention also mismatches EMA INN primacy (PXCORPUS-D19). — _Sources: PXCORPUS-D19, CLISTER-D11, E3C-D11, MORFITT-D8_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional regulatory-affairs annotators or reviewers are documented as having validated content for EMA/ANSM register fit. Would need a regulatory-affairs-led review of the QUAERO EMEA subset and any supplementary corpus to confirm representational fit.
- **IC-5**: Content issues harming validity: (a) genre register mismatch (clinical/research vs. regulatory), (b) non-EU-jurisdiction content dilution, (c) brand-over-INN bias in PxCorpus, (d) sentence-splitting context loss for long EMEA documents [Q37], (e) absent SmPC/CTD/EU-RMP source text [WEB-3, WEB-4]. — _Sources: Q37, WEB-3, WEB-4, QUAERO-D1, QUAERO-D4, PXCORPUS-D19_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q19] 'A diverse range of data origins: Scientific literature, clinical trials, clinical cases, speech transcriptions, and more' (p.2)
- [Q34] 'two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE' (p.3)
- [Q37] 'we decided to split these documents into sentences' (p.3)
- [Q44] '4 hours (1,981 recordings) of transcribed and annotated dialogues focused on drug prescriptions' (p.4)

*Web sources:*
- [WEB-2] EUPATI confirms QRD template mandatory standard statements 'must be used whenever applicable'
- [WEB-3] QUAERO HuggingFace confirms EMEA = patient leaflet text
- [WEB-4] QUAERO official corpus page documents 103,056 words across drug leaflets and biomedical titles
- [WEB-7] EMA confirms SmPC/PIL templates as the regulatory document standard

*Dataset analysis:*
- QUAERO-D1: EMEA authorization header with INN — canonical leaflet structure
- QUAERO-D4: full excipient list with E-numbers in SmPC Section 6 format
- ESSAI-D2: pemetrexed/cisplatine/carboplatine combination regimen with cycle count
- PXCORPUS-D19: brand name 'prozac' used instead of INN fluoxétine — EMA convention mismatch
- DIAMED-D9: Burkina Faso clinical case — outside EU regulatory jurisdiction
- MORFITT-D11: Saudi Arabian medical training context — outside EMA scope
- MORFITT-D12: Egyptian Arabic-language study, non-EMA
- E3C-D16: Moroccan patient origin — non-EMA jurisdictional context
- DEFT2020-D21: posology decontextualized by sentence splitting — section/drug identity lost

</details>

**Information gaps:**
- No published study comparing EMA regulatory French register characteristics to clinical French in NLP corpora (gap_id 5 PARTIALLY RESOLVED)
- No regulatory-affairs annotator review of QUAERO EMEA subset for SmPC/PIL register fit

**Requires expert verification:**
- Whether the QUAERO EMEA subset is sufficiently representative of current QRD v10.4 phrasing conventions [WEB-7] for the deployment's needs
- Whether the deployment's supplementary template layer for CTD modules can compensate for the absence of CTD-genre training/evaluation content

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Both the deployment and the benchmark operate on French text in Latin script with standard diacritics; no script, modality, or infrastructure mismatch exists. The benchmark's HuggingFace toolkit and tokenization analysis [Q48, Q89, Q90] support transferability. The minor concerns are (a) sentence-splitting of long EMEA documents [Q37] which strips structural context relevant to long SmPC/CTD documents, and (b) PxCorpus's transcribed-speech register (PXCORPUS-D11, PXCORPUS-D13) which is incompatible with regulatory written prose. IF is LOWER priority per the elicitation, and these issues do not threaten core form-level validity.

**Strengths:**
- French Latin-script text consistent with deployment environment across all datasets [Q31]
- HuggingFace Datasets toolkit with normalized loaders supports reproducibility [Q48]
- Tokenization study shows segmentation differences have minor impact on performance [Q78, Q79, Q80]
- Hyperparameters fully documented for reproducibility [Q49, Q99]

**Checklist:**

- **IF-1**: No signal-distribution mismatch — both deployment and benchmark are written French text in Latin script [Q31]. Tokenization variance was studied and found to have minor impact [Q79, Q80]. — _Sources: Q31, Q79, Q80_
- **IF-2**: Regional infrastructure (EU pharmaceutical companies, ANSM/EMA) is text-only enterprise document processing, fully compatible with the benchmark's text format [Q48]. — _Sources: Q48_
- **IF-3**: Two domain-specific form differences: (a) Long-document handling: SmPCs/CTDs exceed transformer input limits; benchmark mitigates via sentence-splitting [Q37], but this strips section/cross-reference context (DEFT2020-D21, QUAERO-D22, QUAERO-D24). (b) PxCorpus transcribed speech (PXCORPUS-D11, PXCORPUS-D13) introduces disfluencies and English fragments not present in regulatory documents. — _Sources: Q37, PXCORPUS-D11, PXCORPUS-D13, DEFT2020-D21_
- **IF-4**: Form mismatches are minor: sentence-splitting context loss for long regulatory documents, and the PxCorpus speech-transcription register being inapplicable to formal regulatory prose. No script, encoding, or modality issues. — _Sources: Q37, QUAERO-D22, QUAERO-D25_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'only the French portion is retained for the benchmark' (p.3)
- [Q37] 'we decided to split these documents into sentences' (p.3)
- [Q48] 'a practical toolkit based on the HuggingFace Datasets library' (p.5)
- [Q79] 'DrBERT-CP outperforms FlauBERT on 16 out of the 20 tasks, thus contradicting previous conclusions' (p.8)
- [Q80] 'tokenization, as it is currently done in MLMs, seems to play a minor role in the performance of systems' (p.8)

*Dataset analysis:*
- PXCORPUS-D11: English fragments, expletives, off-task speech — absent from regulatory text
- PXCORPUS-D13: transcribed system error message — impossible in written regulatory documents
- DEFT2020-D21: posology decontextualized by sentence splitting
- QUAERO-D22: single-character fragment from sentence splitting
- QUAERO-D25: Czech-language text embedded in French EMEA document due to multilingual leaflet structure

</details>

**Requires expert verification:**
- Whether sentence-splitting context loss materially impairs SmPC/CTD compliance verification in deployment

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
This is the most severely misaligned dimension. The deployment requires (a) NER over regulatory entity types — INN (distinct from CHEM), ATC code, excipient name, EMA-templated posology, contraindication qualifier, safety warning — and (b) STS calibrated for regulatory equivalence sensitive to dose-threshold and contraindicated-population qualifier differences. The benchmark provides neither. NER schemas use clinical UMLS Semantic Groups (QUAERO 10 classes [Q35, Q103]; Mantra-GSC 10–11 classes [Q106]; E3C clinical entities [Q104]; DEFT2021 13 clinical types) and clinical PxCorpus 38 classes [Q44, Q108], none of which include INN-vs-CHEM distinction, ATC codes, or contraindication qualifiers (QUAERO-D16, QUAERO-D17, QUAERO-D21, MANTRAGSC-D15, PXCORPUS-D15). Dose values systematically receive O tags in QUAERO (QUAERO-D18, QUAERO-D19) and E3C (E3C-D7, E3C-D8). STS is calibrated for general semantic proximity [Q41, Q54]; CLISTER scores a 2× numeric difference (10 vs. 20 mmol/l) at 4.0 (CLISTER-D13), DEFT2020 scores a dropped 'congénitale' qualifier at 4.6 (DEFT2020-D18) and a specific-substance vs. generic-term swap at 4.3 (DEFT2020-D20). The deployment explicitly treats such differences as critical mismatches (A3). External evidence (Kadi et al. 2025 [WEB-11]) confirms ATC and excipient extraction from SmPCs is unsolved field-wide. OO is HIGH priority per the elicitation, and the fundamental decision rule for STS and the entity inventory for NER are both misaligned.

**Strengths:**
- QUAERO CHEM class captures pharmaceutical substances including INNs and excipients at a coarse level, providing partial signal (QUAERO-D7, QUAERO-D15)
- PxCorpus NER schema includes DOSAGE, MODE, FREQUENCY, DURATION, SUBSTANCE [Q108] — the closest approach to regulatory posology entity labels
- DEFT2021 NER includes treatment, dosage, mode, and frequency entity types (DEFT2021-D5, DEFT2021-D6) — partial pharmaceutical entity coverage
- STS uses graded 0–5 scale with multiple annotators averaged [Q41], providing variance signal (DEFT2020-D10, DEFT2020-D11) even if calibration is wrong

**Checklist:**

- **OO-1**: Benchmark NER label categories (UMLS Semantic Groups: GEOG, PHEN, DISO, ANAT, OBJC, PHYS, PROC, DEVI, CHEM, LIVB [Q103]; PxCorpus 38 clinical-prescription classes [Q108]) are calibrated for clinical research, not EU regulatory entity extraction. STS is general semantic similarity [Q54], not regulatory equivalence (CLISTER-D13). — _Sources: Q35, Q103, Q108, Q54, CLISTER-D13_
- **OO-2**: Missing categories specific to the regional context: INN as distinct from CHEM (QUAERO-D15, QUAERO-D17, MANTRAGSC-D15), ATC codes [WEB-11], excipient names as distinct from CHEM, EMA-templated posology expressions, contraindication qualifiers (QUAERO-D21, PXCORPUS-D15), safety warning categories. The 2025 Kadi et al. study confirms ATC and excipient extraction from SmPCs is field-wide unresolved [WEB-11]. — _Sources: WEB-8, WEB-11, QUAERO-D15, QUAERO-D21, PXCORPUS-D15, MANTRAGSC-D15_
- **OO-3**: Categories not strictly 'non-regional' since both deployment and benchmark are in EU/French context, but UMLS Semantic Groups encode a clinical-research ontology rather than a regulatory ontology. Conflation of INN with general CHEM (QUAERO-D17) misrepresents regulatory entity distinctions critical under EMA QRD requirements [WEB-8]. — _Sources: QUAERO-D17, WEB-8_
- **OO-4**: Stakeholder-driven taxonomy redesign is required: regulatory-affairs experts would need to define INN/ATC/excipient/posology/contraindication-qualifier entity types and a regulatory-equivalence STS rubric calibrated for dose-threshold and population-qualifier sensitivity. No such schema exists in published French NLP literature (gap_id 3 RESOLVED as confirmed gap). — _Sources: WEB-11_
- **OO-5**: Taxonomy issues harming structural and content validity: (a) NER schemas conflate INN, excipient, brand name under CHEM; (b) no dose/posology entity class in QUAERO despite abundant dose content; (c) no contraindication qualifier class anywhere; (d) STS scoring rubric demonstrably treats legally material differences as near-synonymy (CLISTER-D13, DEFT2020-D18, DEFT2020-D20). — _Sources: Q82, QUAERO-D18, E3C-D7, CLISTER-D13, DEFT2020-D18, DEFT2020-D20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q35] '10 entity categories corresponding to the UMLS Semantic Groups' (p.3)
- [Q103] 'O, GEOG, PHEN, DISO, ANAT, OBJC, PHYS, PROC, DEVI, CHEM and LIVB' (p.14)
- [Q41] 'similarity scores ranging from 0 to 5' (p.4)
- [Q54] 'Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM)' (p.6)
- [Q82] 'the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS' (p.8)
- [Q108] 'O, ANATOMY, DATE, DOSAGE, DURATION, MEDICAL EXAM, FREQUENCY, MODE, MOMENT, PATHOLOGY, SOSY, SUBSTANCE, TREATMENT and VALUE' (p.14)

*Web sources:*
- [WEB-8] EMA QRD v11 draft requires INN inclusion in SmPC Section 1 — confirms INN as central regulatory entity
- [WEB-11] Kadi et al. 2025 confirms ATC codes and excipient dosages 'frequently missing or misclassified' even with state-of-the-art LLMs on EMA SmPCs

*Dataset analysis:*
- QUAERO-D15: INN, brand name, and excipients all tagged as CHEM — INN-specific label absent
- QUAERO-D17: INN in pharmacokinetic sentence; CHEM conflates API with other chemical entities
- QUAERO-D18: dose value '21,6 microgrammes' receives O tag — dosage not a labeled class
- QUAERO-D21: contraindication qualifier present but no contraindication entity in schema
- MANTRAGSC-D15: testostérone and prolactine both tagged CHEM — INN/endogenous distinction absent
- E3C-D7: four INN drugs with dosages all O-tagged
- PXCORPUS-D15: contraindication qualifier 'si absence d'ulcère' tagged O
- CLISTER-D13: 2× numerical difference (10 vs. 20 mmol/l) scored 4.0 — regulatory-critical treated as near-equivalent
- DEFT2020-D18: 'congénitale' qualifier dropped, scored 4.6
- DEFT2020-D20: specific substance name vs. generic term scored 4.3

</details>

**Information gaps:**
- No published STS rubric calibrated for regulatory equivalence in any language (gap_id 3 RESOLVED as confirmed field-wide gap)
- No published comparison of regulatory-affairs annotator judgments vs. biomedical NLP annotator judgments on EMA-format text

**Requires expert verification:**
- Whether the deployment's regulatory-specific template layer can be configured to compensate for the absent INN/ATC/excipient entity types when running the benchmark-trained model as a foundational extraction layer
- Quantitative threshold for STS regulatory-equivalence calibration that the deployment requires

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Annotation provenance is poorly documented across the benchmark. Only three datasets have explicit annotation documentation: DEFT-2021 (manual annotation, no annotator profiles) [Q25], CLISTER (multiple annotators, profiles undocumented) [Q41], and DiaMed (several annotators including one medical expert, but for ICD-10 classification only — not NER or STS) [Q45]. CAS POS was automatically annotated via Tagex 3 [Q42]. Author affiliations are academic NLP and clinical medicine institutions [Q8] — no regulatory-affairs or pharmacovigilance expertise is documented. The deployment explicitly anticipates systematic disagreement between biomedical NLP annotators and regulatory-standard judgments on borderline cases (A4). Empirical evidence in dataset analysis confirms this: high annotator variance on pharmaceutical pairs (DEFT2020-D10: scores [5,2,4,4,5]; DEFT2020-D11; DEFT2020-D22 [5,3,3,4,3]) shows non-specialist annotation; E3C systematically labels disease entities while leaving drug names unlabeled (E3C-D9, E3C-D14); QUAERO annotators were NLP/biomedical researchers mapping to UMLS, not regulatory affairs specialists (QUAERO-D20). OC is HIGH priority per the elicitation. The DiaMed inter-annotator agreement reporting [Q46] is a structural strength but does not address regulatory norms.

**Strengths:**
- DiaMed reports inter-annotator agreement (Kappa Cohen, Gwet's AC1) computed across two annotation sessions [Q45, Q46]
- CLISTER averages multiple annotator scores producing graded ground truth [Q41], enabling variance analysis (DEFT2020-D10)
- CAS POS automatic annotations were validated against manual annotations at 98% precision [Q42]
- DiaMed includes one medical expert annotator [Q45] — partial domain expertise for the ICD-10 task

**Checklist:**

- **OC-1**: Ground truth labels do NOT reflect regional regulatory stakeholder perspectives. No annotation guidelines reference EMA/ANSM regulatory standards. The deployment's authoritative ground truth rests with regulatory-affairs specialists, but no benchmark dataset documents such annotators (QUAERO-D20, CLISTER-D16). — _Sources: Q8, QUAERO-D20, CLISTER-D16_
- **OC-2**: Systematic disagreement is empirically expected: annotator variance on pharmaceutical STS pairs (DEFT2020-D10 [5,2,4,4,5]; DEFT2020-D22 [5,3,3,4,3]) demonstrates non-specialist annotation; E3C consistently labels diseases while leaving drug names O (E3C-D9, E3C-D14) reflects clinical-priority norms divergent from regulatory; A4 from elicitation explicitly anticipates this gap. — _Sources: DEFT2020-D10, DEFT2020-D22, E3C-D9, E3C-D14, WEB-12_
- **OC-3**: Annotator demographics are NOT DOCUMENTED for the majority of corpora. CLISTER says 'multiple annotators' [Q41] without profiles; DiaMed lists 'several annotators including one medical expert' [Q45]; QUAERO, E3C, PxCorpus, ESSAI annotator profiles are not documented in the paper. No Datasheets-style demographic disclosures exist. — _Sources: Q25, Q41, Q45_
- **OC-4**: Re-annotation by regulatory-affairs annotators would be required for deployment-grade label quality. No such re-annotation effort is documented in DrBenchmark or in any published French NLP corpus (gap_id 4 RESOLVED as confirmed gap).
- **OC-5**: Aggregation by averaging in CLISTER [Q41] erases minority/dissenting judgments — visible as variance pattern (DEFT2020-D10). For regulatory equivalence, dissenting annotators flagging legal mismatch would be the signal of interest, but the averaging method suppresses it. — _Sources: Q41, DEFT2020-D10_
- **OC-6**: Label issues harming convergent and external validity: (a) annotator population systematically misaligned with deployment ground-truth source; (b) no EMA/ANSM annotation guidelines documented; (c) variance suppression via averaging in STS; (d) consistent clinical-priority annotation norms in NER (E3C-D9, QUAERO-D18); (e) no documented re-annotation effort exists for regulatory norms. — _Sources: DEFT2020-D18, QUAERO-D18, Q41_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q8] 'LIA, Avignon Université, Zenidoc, Nantes Université, CHU Nantes ... INSERM, CIC 1413, École Centrale Nantes, CNRS' (p.1)
- [Q25] 'manually annotated in two tasks' (p.3)
- [Q41] '1,000 sentence pairs manually annotated by several annotators ... averaged together' (p.4)
- [Q42] 'Tagex 3 ... 98% precision' (p.4)
- [Q45] 'manually annotated by several annotators, one of which is a medical expert' (p.4)
- [Q46] 'Inter-annotator agreement statistics. κ is referring to Kappa Cohen and G to Gwet's AC1' (p.4)

*Web sources:*
- [WEB-12] Bayer et al. 2021 Drug Safety confirms general biomedical NLP systems 'would need to be modified or reconfigured to lower error rates to support their use in a regulatory setting'

*Dataset analysis:*
- QUAERO-D20: annotators were NLP/biomedical researchers mapping to UMLS, not regulatory affairs specialists
- CLISTER-D16: annotators are biomedical NLP specialists, not regulatory affairs experts
- DEFT2020-D10: scores [5,2,4,4,5] on opioid timing safety statement — high variance indicates non-specialist annotation
- DEFT2020-D11: same variance pattern on breastfeeding contraindication pair
- DEFT2020-D22: scores [5,3,3,4,3] — 2-point variance on pharmaceutical dosage instruction
- E3C-D9: drug names unlabeled while disease names labeled — clinical-priority annotation
- E3C-D14: ciclosporine/evérolimus/corticoïdes unlabeled while disease entities labeled
- DEFT2020-D18: 'congénitale' qualifier loss scored 4.6 — regulatory-material difference treated as near-equivalent

</details>

**Information gaps:**
- No published comparison of biomedical NLP annotator vs. regulatory affairs expert judgments on EMA-format text (gap_id 4 RESOLVED as confirmed gap)
- Annotator professional background documentation absent for QUAERO, E3C, ESSAI, PxCorpus, MORFITT, MANTRAGSC, DEFT2020, DEFT2021

**Requires expert verification:**
- Magnitude of expected disagreement between benchmark labels and regulatory-affairs judgments on contraindication-qualifier and dose-threshold borderline cases — would require pilot re-annotation
- Whether DiaMed's medical expert participation translates to any regulatory-affairs annotation norm overlap

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output representations (IOB2 NER labels, multi-label classification, multiple-choice indices, continuous 0–5 STS scores [Q52, Q53, Q54]) match the deployment's consumption modalities. The deployment ingests entity spans and STS scores; both are produced by the benchmark in compatible formats. Statistical reporting (averaging over four runs, Student's t-test [Q51], majority-class baseline [Q56]) supports interpretable results. SeqEval with first-token prediction [Q52, Q53] provides tokenizer-agnostic evaluation. The minor concerns are (a) the EDRM metric's specificity to DEFT-2020 [Q54] without documented calibration for regulatory micro-differences, and (b) the ~2,500 GPU-hour reproducibility cost [Q92, Q93] for users without HPC access. OF is LOWER priority per the elicitation.

**Strengths:**
- Standard NER output via SeqEval IOB2 with tokenizer-agnostic first-token prediction [Q52, Q53]
- Continuous 0–5 STS scores in a format directly consumable by the deployment's compliance flagging logic [Q41, Q54]
- Robust statistical reporting: four runs averaged, Student's t-test [Q51], majority-class baseline [Q56]
- Best-model selection via validation metric mitigates overfitting [Q100]
- Hyperparameters documented for reproducibility [Q49, Q99]

**Checklist:**

- **OF-1**: Output modalities (IOB2 entity spans, classification labels, continuous STS scores) match deployment needs [Q52, Q54]. The deployment ingests entity spans for NER and continuous scores for STS — both are produced by the benchmark. — _Sources: Q52, Q53, Q54_
- **OF-2**: Not applicable — the deployment is text-only enterprise document processing; no text-to-speech requirements (deployment infrastructure_notes).
- **OF-3**: Not applicable — the target population is highly literate professional regulatory affairs specialists; no accessibility constraints relevant to output form.
- **OF-4**: Minor form concerns: (a) EDRM metric specific to DEFT-2020 task design [Q54] has no documented calibration for regulatory equivalence, but this is a calibration concern (OO) rather than a representation mismatch; (b) reproducibility burden of 2,500 GPU hours [Q92, Q93] limits independent re-running but does not affect output-form compatibility. — _Sources: Q54, Q92, Q93_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q52] 'SeqEval (Nakayama, 2018) metric in conjunction with the IOB2 format' (p.6)
- [Q53] 'tokenizer-agnostic evaluation' (p.6)
- [Q54] 'Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM)' (p.6)
- [Q51] 'averaging the scores from four separate runs ... statistical significance computed using Student's t-test' (p.5)
- [Q92] 'a substantial amount of computational power to execute all runs' (p.9)
- [Q93] 'approximately 2,500 hours on V100 GPUs' (p.9)

</details>

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** NER schemas conflate INN, excipients, and brand names under CHEM; no ATC code, contraindication qualifier, or EMA-templated posology entity types; STS scoring treats legally material qualifier differences as near-synonymy.

**Recommendation:** Construct a deployment-side regulatory entity schema (INN distinct from CHEM, ATC, excipient, posology template fields, contraindication qualifier, safety warning) and re-annotate a held-out QUAERO EMEA sample under this schema. Develop a complementary regulatory-equivalence STS rubric with explicit rules for dose-threshold and population-qualifier mismatches, and validate the deployment's STS layer against this rubric rather than against CLISTER/DEFT2020 scores alone.

### Output Ontology ⚠

**Gap:** STS scoring rubric demonstrably treats 2× numerical differences (CLISTER-D13) and dropped legal qualifiers (DEFT2020-D18) as near-synonymy, opposite of the deployment's regulatory-equivalence requirement.

**Recommendation:** Do not rely on CLISTER or DEFT2020 STS scores as the primary signal for the deployment's compliance-flagging layer. Build a small adversarial regulatory-equivalence test set with paired examples differing only in dose threshold, qualifier, or population scope, and use it as a deployment-internal validation gate before relying on any STS-based compliance check.

### Output Content ⚠

**Gap:** No annotation guidelines reference EMA/ANSM standards; annotator populations are academic NLP and clinical, with no documented regulatory-affairs expertise; STS averaging suppresses dissent that would signal regulatory mismatch.

**Recommendation:** Commission a pilot re-annotation of 200–500 regulatory-relevant items (QUAERO EMEA NER, CLISTER and DEFT2020 STS pairs containing dose/contraindication content) by regulatory-affairs specialists. Quantify the disagreement rate with benchmark labels on borderline cases. Use this to bound expected error in deployment and to calibrate the human-review flagging threshold.

### Input Content ⚠

**Gap:** Non-EU-jurisdiction content (sub-Saharan Africa, North Africa, Middle East, Canada) dilutes IC validity; brand-name predominance in PxCorpus conflicts with EMA INN primacy; sentence-splitting strips long-document context.

**Recommendation:** When fine-tuning on DrBenchmark, weight or filter to prioritize the QUAERO EMEA, Mantra-GSC EMEA/Patents, and ESSAI subsets that are closest to EU regulatory content. Consider augmenting with deployment-internal SmPC/CTD/RMP text. Develop a long-document handling strategy beyond simple sentence-splitting (e.g., section-aware chunking) for SmPC/CTD inputs.

### Input Ontology ⚠

**Gap:** SmPC, CTD module, and EU-RMP document genres are absent as task categories; only QUAERO EMEA (~10 segmented PIL documents) provides confirmed regulatory-genre coverage.

**Recommendation:** Use QUAERO EMEA only as a partial sanity check for PIL-register NER. For SmPC/CTD/EU-RMP genres, construct a deployment-internal evaluation corpus from authentic regulatory submissions under current QRD v10.4 [WEB-7] and treat DrBenchmark performance as a model-selection proxy, not a deployment-readiness measure.

### Input Form

**Gap:** Sentence-splitting of long EMEA documents [Q37] strips section structure that is legally and semantically critical in SmPC/CTD compliance verification.

**Recommendation:** When applying DrBenchmark-trained models to deployment SmPC/CTD documents, implement section-aware chunking that preserves QRD section identity (4.1 Indications, 4.2 Posology, 4.3 Contraindications, 4.4 Special warnings) as metadata accompanying each chunk, so downstream regulatory rules can use section context that the benchmark training did not preserve.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "It encompasses 20 diversified tasks, including named-entity recognition, part-of-speech tagging, question-answering, semantic textual similarity, and classification." |
| Q2 | 1 | output_form | "We evaluate 8 state-of-the-art pre-trained masked language models (MLMs) on general and biomedical-specific data, as well as English specific MLMs to assess their cross-lingual capabilities." |
| Q3 | 1 | output_form | "Our experiments reveal that no single model excels across all tasks, while generalist models are sometimes still competitive." |
| Q4 | 1 | input_ontology | "These tasks encompass part-of-speech (POS) tagging, named-entity recognition (NER), classification, question-answering (QA), and semantic textual similarity (STS)." |
| Q5 | 1 | input_content | "Although the French language is generally considered as well-endowed, it is notably lacking in evaluation resources within the biomedical field." |
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
| Q21 | 3 | input_ontology | "DEFT-2020 (Cardon et al., 2020) contains clinical cases, encyclopedia and drug labels introduced in the 2020 edition of an annual French Text Mining Challenge, called DEFT, and annotated for two tasks: (i) textual similarity and (ii) multi-class classification." |
| Q22 | 3 | input_ontology | "The first task aims at identifying the degree of similarity within pairs of sentences, from 0 (the less similar) to 5 (the most similar)." |
| Q23 | 3 | input_ontology | "The second task consists in identifying, for a given sentence, the most similar sentence among three sentences provided." |
| Q24 | 3 | input_content | "DEFT-2021 (Grouin et al., 2021) is a subset of 275 clinical cases taken from the 2019 edition of DEFT." |
| Q25 | 3 | output_content | "This dataset is manually annotated in two tasks: (i) multi-label classification and (ii) NER." |
| Q26 | 3 | input_ontology | "The multi-label classification task focuses on identifying the patient's clinical profile based on the diseases, signs, or symptoms mentioned in the clinical cases." |
| Q27 | 3 | output_ontology | "The dataset is annotated with 23 axes from Chapter C of the Medical Subject Headings (MeSH)." |
| Q28 | 3 | input_ontology | "The second task involves fine-grained information extraction for 13 types of entities (more detail in Appendix B.7)." |
| Q29 | 3 | input_content | "E3C (Magnini et al., 2020) is a multilingual dataset of clinical cases annotated for the NER task." |
| Q30 | 3 | output_ontology | "It consists of two types of annotations (more detail in Appendix B.4): (i) clinical entities (e.g., pathologies), (ii) temporal information and factuality (e.g., events)." |
| Q31 | 3 | input_form | "While the dataset covers 5 languages, only the French portion is retained for the benchmark." |
| Q32 | 3 | input_form | "Since the dataset does not come with pre-defined subsets, we performed a 70 / 10 / 20 random split, as described in Table 3." |
| Q33 | 3 | input_content | "The QUAERO French Medical Corpus (Névéol et al., 2014), simply referred to as QUAERO in this paper, contains annotated entities and concepts for NER tasks." |
| Q34 | 3 | input_content | "The dataset covers two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE." |
| Q35 | 3 | output_ontology | "10 entity categories corresponding to the UMLS Semantic Groups (Lindberg et al., 1993) were annotated (more detail in Appendix B.3)." |
| Q36 | 3 | input_content | "In total, 26,409 entity annotations were mapped to 5,797 unique UMLS concepts." |
| Q37 | 3 | input_form | "Due to the presence of nested entities in annotations, we simplified the evaluation process by retaining only annotations at the higher granularity level from the BigBio (Fries et al., 2022) implementation, following the approach described in Touchent et al. (2023), which translates into an average loss of 6.06% of the annotations on EMEA and 8.90% on MEDLINE. Additionally, considering that some documents from EMEA exceed the maximum input sequence length that most current language models can handle, we decided to split these documents into sentences." |
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
| Q54 | 6 | output_form | "For STS tasks, the models' performance was assessed using two metrics: (1) the Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM), as defined by the original authors of the DEFT-2020 dataset (Cardon et al., 2020)." |
| Q55 | 6 | output_ontology | "In Section 5.1, we compare the results obtained by each model within DrBenchmark, which permits to position a wide range of state-of-the-art models in the biomedical field across various NLP tasks." |
| Q56 | 6 | output_form | "The results of the 8 models are reported in Table 6 and compared to a baseline obtained by considering the majority class for all predictions." |
| Q57 | 6 | output_form | "Overall, although we might anticipate certain models to excel in all tasks, we discovered that no single model outperforms the rest in all application scenarios." |
| Q58 | 6 | output_form | "Interestingly, most of the models examined manage to secure the top position in at least one of the French biomedical downstream tasks studied." |
| Q59 | 6 | output_form | "The only exception pertains to the cross-lingual generalist model (XLM-RoBERTa), which manages to reach the second-best position on several tasks." |
| Q60 | 6 | output_content | "French biomedical language models (DrBERT-FS, DrBERT-CP, CamemBERT-bio), presumed to be the most aligned with the nature of the data of the benchmark, exhibit indeed superior performance across many tasks." |
| Q61 | 6 | output_form | "More precisely, DrBERT-FS achieves the highest performance in 8 tasks, DrBERT-CP in 5 tasks, and CamemBERT-bio in 2 tasks." |
| Q62 | 6 | output_form | "This indicates that domain and language-specialized models achieve the best performance in up to 75% of the DrBenchmark downstream tasks." |
| Q63 | 6 | output_form | "Generalist models (CamemBERT, CamemBERTa, FlauBERT and XLM-RoBERTa) are more suitable for tasks that require extensive linguistic knowledge but may not perform as well as specialized models nor even reach their level of performance." |
| Q64 | 6 | output_form | "We observe that all generalist models obtain better performance only on 4 out of the 20 tasks, but still remain competitive on most tasks." |
| Q65 | 6 | input_content | "Furthermore, our experiments with DrBERT-FS indicate that biomedical models may require less pre-training data compared to generalist ones." |
| Q66 | 6 | input_content | "However, it is important to note that this observation requires further confirmation." |
| Q67 | 6 | output_form | "In some tasks, biomedical models that undergo continual pre-training from a generalist model, such as CamemBERT-bio, can prove to be the most effective, underscoring the value of pre-training on generalist data." |
| Q68 | 7 | input_content | "For this purpose, we conducted experiments by varying the amount of training data during the fine-tuning process by randomly choosing four percentages of the training data: 25%, 50%, 75% and 100%." |
| Q69 | 7 | output_form | "To make the experiment as fair as possible, we did four runs for each percentage, model and dataset combination." |
| Q70 | 7 | output_form | "The validation and test sets have not been changed for the sake of comparison." |
| Q71 | 7 | output_form | "We observe that on certain datasets, some models capture information more quickly than others, like in Figures 1b, 1f and 1a." |
| Q72 | 7 | output_form | "Unsurprisingly, in almost all scenarios, having the complete training set yields better results than having only 25% of it." |
| Q73 | 7 | output_form | "However, all the models based on CamemBERT face difficulties in corpora with limited amount of data, such as MantraGSC Patents, where they fail to generate labels other than 'O'." |
| Q74 | 7 | output_form | "On the other hand, in the same low-resource scenarios, CamemBERTa models exhibit greater robustness and achieve superior performance." |
| Q75 | 8 | input_form | "Tokenizers play a crucial role in MLMs by utilizing size-limited vocabularies to split texts into sub-units, aiming to handle out-of-vocabulary (OOV) words." |
| Q76 | 8 | input_content | "Due to variations in the training data, vocabularies differ across different models, as illustrated in Figure 2." |
| Q77 | 8 | input_form | "So far, there has been a prevailing notion in the community that excessive segmentation of words in tokenization leads to a loss of morphological form and semantic meaning, introducing noise and adversely affecting performance (Church, 2020; Hofmann et al., 2021; Bostrom and Durrett, 2020)." |
| Q78 | 8 | input_form | "However, our experiments, as shown in Table 7, reveal that FlauBERT is the model with the least word segmentation (1.43 in average), while DrBERT-CP tends to have the highest average segmentation (1.90 in average)." |
| Q79 | 8 | input_form | "Surprisingly, when comparing the performance of these two models on the benchmark tasks, we observe that DrBERT-CP outperforms FlauBERT on 16 out of the 20 tasks, thus contradicting previous conclusions drawn by the community." |
| Q80 | 8 | input_form | "Yet, tokenization, as it is currently done in MLMs, seems to play a minor role in the performance of systems." |
| Q81 | 8 | output_ontology | "Table 8 summarizes the results obtained on average by the considered MLMs when aggregating the tasks into one of the five designated categories: POS, NER, MCQA, MCC (Multi-class classification), MLC (Multi-label classification), or STS tasks." |
| Q82 | 8 | output_form | "Upon analyzing the average performance by task category, it becomes evident that the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS." |
| Q83 | 9 | input_ontology | "In this paper, we introduced DrBenchmark, the first large language understanding benchmark tailored for the French biomedical domain." |
| Q84 | 9 | input_ontology | "We conducted a qualitative evaluation of 8 state-of-the-art masked language models (MLMs) on this comprehensive benchmark, encompassing 20 diverse downstream tasks." |
| Q85 | 9 | output_form | "Our findings illuminate the limitations of generalist models in tackling complex biomedical tasks, emphasizing the importance of employing domain-specific models to achieve peak performance." |
| Q86 | 9 | output_form | "We have observed that several biomedical tasks in DrBenchmark exhibit relatively poor performance, even when utilizing specialized biomedical models." |
| Q87 | 9 | output_ontology | "We postulate that the models examined in this study, here state-of-the-art MLMs, may not be the most effective choices for specific tasks such as question-answering or multi-label classification." |
| Q88 | 9 | input_form | "The quantitative study we conducted on the PLMs requires further in-depth analysis to comprehend the impact of different parameters." |
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
| WEB-1 | https://www.ema.europa.eu/en/about-us/careers |
| WEB-2 | https://learning.eupati.eu/mod/book/view.php?id=858&chapterid=770 |
| WEB-3 | https://huggingface.co/datasets/DrBenchmark/QUAERO |
| WEB-4 | https://quaerofrenchmed.limsi.fr/ |
| WEB-5 | https://www.pharmaregulatory.in/qrd-templates-explained-ultimate-guide-to-ema-compliant-labelling-formats/ |
| WEB-6 | https://arxiv.org/html/2402.13432v1 |
| WEB-7 | https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/product-information-requirements/product-information-qrd-templates-human |
| WEB-8 | https://www.ema.europa.eu/en/documents/template-form/quality-review-documents-qrd-annotated-template-v11-draft-public-consultation_en.pdf |
| WEB-9 | https://www.ema.europa.eu/en/documents/regulatory-procedural-guideline/guideline-good-pharmacovigilance-practices-gvp-module-xvi-risk-minimisation-measures-rev-3_en.pdf |
| WEB-10 | https://informait.com/news/pharmaceutical-labeling-requirements-a-complete-guide |
| WEB-11 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12380897/ |
| WEB-12 | https://link.springer.com/article/10.1007/s40264-020-00996-3 |
| WEB-13 | https://link.springer.com/article/10.1007/s40264-024-01468-8 |
| WEB-14 | https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-2_en |
| WEB-15 | https://globalforum.diaglobal.org/issue/november-2019/identification-of-medicinal-products/ |
| WEB-16 | https://www.iqvia.com/-/media/iqvia/pdfs/library/fact-sheets/nlp-text-analytics-for-regulatory-affairs.pdf |
| WEB-17 | https://www.linguamatics.com/blog/countdown-idmp-compliance-are-you-ready |
| WEB-18 | https://www.ema.europa.eu/en/documents/template-form/qrd-product-information-template-version-104-highlighted_en.pdf |

---

### Dataset Analysis

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

