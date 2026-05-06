## Deployment Context

**Use case:** In a pharmaceutical setting, a regulatory specialist uses document management software to ensure compliance in French drug labeling and scientific abstracts by applying a model evaluated on semantic textual similarity and fine-grained named-entity recognition. The system identifies over a dozen types of precise entities, such as chemical compounds and dosage modes, while verifying that safety warnings across different leaflets or patents are semantically consistent. These results determine whether pharmacological documentation meets strict professional standards for official submission or requires manual revision to prevent regulatory non-compliance.
**Target population:** Regulatory affairs specialists, pharmacologists, and legal experts at pharmaceutical companies or government health agencies.

# Validity Analysis: blurb
**Target context:** EU/French Pharmaceutical Regulatory NLP — BLURB Assessment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology | 2 | Significant gaps | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ⚠ | 1 | Serious concern | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 3 | Moderate gaps | medium |
| **Average** | **1.8** | | |

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

BLURB is a well-constructed benchmark for English-language PubMed-based biomedical NLP, but it is fundamentally misaligned with the EU/French pharmaceutical regulatory NLP deployment across five of six validity dimensions. The language gap (English-only [Q1, Q126] vs French-language deployment), document-genre gap (PubMed abstracts vs SmPCs/PILs/CTD modules), entity-ontology gap (no INN/ATC/posology/excipient label spaces), STS-construct gap (general biomedical proximity [Q74] vs legally-determinative regulatory equivalence), and annotator-norm gap (biomedical researchers vs EMA/ANSM-aligned regulatory experts) are each rated HIGH severity by the elicitation and confirmed by web research [WEB-9, WEB-10, WEB-12, WEB-23]. Output form is the only dimension with reasonable representational alignment, and even there, the absence of calibration/threshold-sensitivity reporting limits direct utility for a human-review-triggering compliance pipeline. No remediation can be done within BLURB itself; bespoke French regulatory benchmark development against the EMA AI Reflection Paper [WEB-6] normative framework is required.

## Practical Guidance

### What This Benchmark Measures

BLURB measures the relative quality of English biomedical pretrained encoders on PubMed-derived NER, PICO extraction, relation extraction, sentence similarity (BIOSSES), document classification (HoC), and yes/no QA tasks [Q48, Q150]. For the EU/French regulatory deployment it can serve, at most, as an upper-bound sanity check on a French-translated or French-equivalent regulatory pipeline's underlying biomedical NLP competence — and even this only if a French biomedical PLM (DrBERT, CamemBERT-bio, AliBERT [WEB-14, WEB-15, WEB-16]) is the model under evaluation. None of the deployment's HIGH-priority constructs (regulatory NER ontology, regulatory equivalence STS, regulatory-expert annotation norms) is directly measurable through BLURB.

### Construct Depth

BLURB probes generic biomedical NER, RE, STS, and QA constructs at moderate depth on English PubMed text. It does not probe regulatory-document understanding, French-language regulatory phrasing, regulatory-equivalence scoring, cross-document consistency, or calibration at decision boundaries. The five HIGH-priority dimensions in this deployment (IO, IC, IF, OO, OC) are essentially unaddressed by BLURB, and the MODERATE-priority OF dimension is only partially addressed (representation matches; calibration/threshold reporting does not).

### What Else You Need

A complete assessment requires: (1) a French-language regulatory document corpus seeded by QUAERO EMEA [WEB-19, WEB-20] and informed by the DART Italian SmPC precedent [WEB-12]; (2) a regulatory-specific entity ontology (INN, ATC, excipient, posology, EMA-template qualifiers) with annotation guidelines anchored in EMA QRD v10.4 [WEB-1, WEB-2] and ANSM circulars; (3) a regulatory-equivalence STS dataset annotated by EMA/ANSM-trained regulatory affairs specialists, with critical-mismatch sub-categories (dose, population, indication scope); (4) calibration and threshold-sensitivity evaluation framed against the EMA AI Reflection Paper [WEB-6] and EU AI Act high-risk requirements; (5) an IAA study comparing biomedical NLP annotators with regulatory-expert annotators on shared regulatory text to quantify the OC gap.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
BLURB's task taxonomy (NER, PICO, relation extraction, sentence similarity, document classification, QA) is explicitly scoped to PubMed-based biomedical applications [Q46, Q48], with clinical and 'other high-value verticals' deferred to future work [Q46, Q197]. The deployment requires categories for regulatory document genres (SmPCs, PILs, CTD modules, patent claims) and regulatory-specific tasks such as cross-document consistency checking and regulatory equivalence STS — none of which are represented in BLURB's taxonomy. The QA scope is further restricted to yes/no and three-way classification [Q49, Q51, Q124], excluding the kind of structured field-extraction or compliance-verification task structure relevant to regulatory submissions. Web-confirmed: no public regulatory NLP benchmark with these task categories exists for French [WEB-12, WEB-23], reinforcing the structural gap. The taxonomy does include NER, document classification, and STS at an abstract level, which are the surface task types the deployment also uses, so the gap is one of category specificity rather than total absence.

**Strengths:**
- BLURB's six-task structure (NER, RE, document classification, STS, QA, PICO) names the surface task types the deployment also relies on (NER, STS, document classification), providing a generic abstraction layer [Q48, Q195]
- The benchmark explicitly acknowledges that prior biomedical evaluations use heterogeneous task selections [Q37], and offers a stable task-grouped scoring scheme [Q52, Q150] that the deployment could in principle adopt for internal evaluation

**Checklist:**

- **IO-1**: Required categories for the deployment include regulatory NER (INNs, ATC codes, posology, excipients, EMA-template qualifiers), regulatory document classification (SmPC vs PIL vs CTD genre), regulatory equivalence STS (SmPC↔PIL, original↔revised), and cross-document consistency checking. None of these categories is present in BLURB; the closest analogs are generic biomedical NER, BIOSSES-style STS, and HoC-style abstract classification. — _Sources: Q48, WEB-12, WEB-23_
- **IO-2**: Yes — BLURB omits regulatory document genres and regulatory-specific task types entirely. The benchmark explicitly defers 'other high-value verticals' to future work [Q46, Q197]. No public French or EU regulatory NLP benchmark covering these categories was identified [WEB-12, WEB-23]. — _Sources: Q46, Q197, WEB-12, WEB-23_
- **IO-3**: BLURB's PICO task (clinical trial P/I/O extraction) [Q59, Q111] and the molecular biology entity types in JNLPBA (DNA, RNA, cell line, cell type) [Q58] are not directly relevant to the regulatory submission deployment; they consume evaluation weight in the macro-averaged BLURB score [Q52, Q150] without contributing to regulatory-task signal. — _Sources: Q58, Q59, Q52_
- **IO-4**: Content validity is harmed because the benchmark's task taxonomy underrepresents the regulatory-document task constructs the deployment needs to evaluate (genre-specific NER, regulatory equivalence, cross-document consistency) and includes research-oriented categories (PICO, molecular-biology NER) that do not generalize to SmPC/PIL/CTD prose. — _Sources: Q46, Q48_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q46] 'We focus on PubMed-based biomedical applications, and leave the exploration of the clinical domain, and other high-value verticals to future work.' (p.6)
- [Q48] 'BLURB is comprised of a comprehensive set of biomedical NLP tasks from publicly available datasets, including named entity recognition (NER), evidence-based medical information extraction (PICO), relation extraction, sentence similarity, document classification, and question answering.' (p.7)
- [Q49] 'For question answering, prior work has considered both classification tasks ... and more complex tasks such as list and summary' (p.7)
- [Q51] 'For simplicity, we focus on the classification tasks such as yes/no question-answering in BLURB' (p.7)
- [Q197] 'Future directions include: ... extension of the BLURB benchmark to clinical and other high-value domains.' (p.22)

*Web sources:*
- [WEB-12] DART (Italian SmPC NER/RE corpus, 2025) is the closest published regulatory-document NLP resource; no French equivalent exists
- [WEB-23] Practitioner review confirms NLP for EU SmPC/prescribing information remains hybrid with no validated regulatory-specific benchmark

</details>

**Information gaps:**
- Whether any internal EMA tooling (Scientific Explorer, PICROSS, EurEKA) defines a public task taxonomy compatible with BLURB's framing

**Requires expert verification:**
- The full set of regulatory task categories required for ANSM-compliant submission review (e.g., posology consistency, contraindication scope verification) — would benefit from regulatory affairs expert specification

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
BLURB's input content is drawn entirely from PubMed abstracts [Q1, Q53, Q54, Q56, Q57, Q58, Q59, Q64, Q70, Q126, Q127], with the pretraining corpus comprising 14 million abstracts [Q126]. The deployment targets French-language SmPCs, PILs, CTD modules, and patent claims — formulaic, template-governed regulatory documents that are categorically distinct from PubMed research prose. BLURB explicitly excludes even clinical notes on the grounds that they 'differ substantially from biomedical literature' [Q43]; this same logic applies a fortiori to regulatory documents, which differ from research abstracts in genre, register, legal function, and language. No French-language source, no SmPC, no PIL, and no EU regulatory submission document appears anywhere in BLURB's data. Web-confirmed: only the small QUAERO EMEA subcorpus (4 documents) provides any French regulatory NLP content [WEB-19, WEB-20], and even there the entity taxonomy is research-biomedical. The 2025 Frontiers SmPC IDMP study confirms empirically that even current LLMs miss ATC codes and excipient dosages in SmPC extraction [WEB-9], evidencing the magnitude of the content gap.

**Strengths:**
- Chemical-entity content in BC5-Chemical and ChemProt [Q53, Q64] partially overlaps with active-substance vocabulary that also appears in regulatory text, providing some lexical transfer signal for INN-adjacent entities
- The DDI corpus [Q68] addresses pharmacovigilance-adjacent content ('drug-drug interactions ... particular focus on pharmacovigilance'), which is the closest BLURB content to a regulatory information-extraction concern

**Checklist:**

- **IC-1**: Yes — the deployment requires French-language regulatory phrasing, EMA QRD template language [WEB-1, WEB-2], ANSM-jurisdiction conventions, French posology expressions ('deux comprimés par jour'), and EU-specific nomenclature (E-numbers, Ph. Eur. terms). None of this is present in BLURB's English PubMed corpus [Q1, Q126]. — _Sources: Q1, Q126, WEB-1, WEB-9_
- **IC-2**: Not aligned. BLURB content is research-biomedical English prose [Q1]; deployment culture is EU/French regulatory-legal. The content register (formulaic, template-driven) and language are both mismatched. — _Sources: Q1, Q126, WEB-9, WEB-12_
- **IC-3**: Yes — BLURB inputs are entirely English PubMed abstracts [Q126, Q127] reflecting Anglophone biomedical research conventions. The benchmark itself notes that 'general domain text is substantively different from biomedical text' [Q12]; the same mismatch exists between PubMed abstracts and EU regulatory documents. — _Sources: Q126, Q127, Q12_
- **IC-4**: INSUFFICIENT DOCUMENTATION — would require recruitment of French regulatory affairs specialists to review BLURB samples for relevance to SmPC/PIL/CTD content; not addressed in the paper.
- **IC-5**: Content validity is severely harmed: every BLURB datapoint is in the wrong language, wrong document genre, and wrong register relative to the deployment. Construct-irrelevant variance is essentially total at the content level. — _Sources: Q1, Q43, Q126, WEB-9_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we compile a comprehensive biomedical NLP benchmark from publicly-available datasets.' (p.1)
- [Q43] 'Clinical notes differ substantially from biomedical literature, to the extent that we observe BERT models pretrained on clinical notes perform poorly on biomedical tasks' (p.6)
- [Q126] 'For biomedical domain-specific pretraining, we generate the vocabulary and conduct pretraining using the latest collection of PubMed abstracts: 14 million abstracts, 3.2 billion words, 21 GB.' (p.12)
- [Q42] 'BLUE mixes PubMed-based biomedical applications ... with MIMIC-based clinical applications' (p.6)
- [Q68] 'The Drug-Drug Interaction corpus ... was created to facilitate research on pharmaceutical information extraction, with a particular focus on pharmacovigilance.' (p.8)

*Web sources:*
- [WEB-9] 2025 Frontiers in Medicine SmPC IDMP study — ATC codes and excipient dosages frequently missed by LLMs, confirming SmPC content is empirically distinct from biomedical research prose
- [WEB-19] QUAERO French Medical Corpus — only public French regulatory-document NLP resource, very small EMEA subcorpus
- [WEB-20] QUAERO HuggingFace dataset documentation — 4 EMEA documents segmented into 15 sub-documents
- [WEB-1] EMA QRD SmPC Template v10.4 (Feb 2024) — defines the formulaic template language the deployment must process
- [WEB-12] DART Italian SmPC corpus (2025) demonstrates regulatory SmPC content is structurally distinct from research abstracts

</details>

**Information gaps:**
- Quantification of lexical overlap between BLURB chemical/drug vocabulary and INN/ATC nomenclature for the deployment's drug list

**Requires expert verification:**
- Whether the QUAERO EMEA subcorpus is fit-for-purpose as a domain-adaptation seed for the deployment

---

### Input Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
BLURB is exclusively English-language text [Q1, Q46, Q126], with vocabulary generated from PubMed [Q126] and tokenization optimized for English biomedical terminology [Q29, Q162, Q168]. The deployment operates on French-language regulatory documents with French diacritics and French-specific tokenization needs. No multilingual processing, no French-language variant, and no porting strategy is documented in BLURB. The benchmark's own argument that vocabulary mismatch causes performance degradation — 'standard BERT models are forced to divert parametrization capacity and training bandwidth to model biomedical terms using fragmented subwords' [Q28], with examples like 'naloxone' fragmenting into four pieces [Q29] — applies with even greater force across the English↔French boundary. Sequence-length truncations (128/256/512 tokens [Q120, Q125]) were calibrated for PubMed sentence/abstract structure, not for SmPC sections or PIL prose. Web-confirmed French biomedical models (DrBERT, CamemBERT-bio, AliBERT) [WEB-14, WEB-15, WEB-16, WEB-17] exist but are not part of BLURB and have not been fine-tuned on EMA/ANSM regulatory genres. Form mismatch is foundational.

**Strengths:**
- BLURB establishes that in-domain vocabulary and tokenization materially affect performance [Q25, Q28, Q160, Q162], providing a transferable methodological lesson the deployment can apply when training a French regulatory tokenizer
- Standard transformer preprocessing scaffolding (special token insertion, padding/truncation, entity dummification) [Q99, Q120, Q183, Q184] is technology-neutral with respect to language and could be reused in a French regulatory NLP pipeline

**Checklist:**

- **IF-1**: Signal distributions are mismatched: BLURB inputs are English PubMed text tokenized with a PubMed-derived vocabulary [Q126], whereas the deployment requires French regulatory text with French diacritics (é, è, ê, ç, œ) and regulatory-specific tokens (INNs, ATC codes, posology phrases). The benchmark's own demonstration that vocabulary fragmentation harms performance [Q28, Q29] applies to this mismatch. — _Sources: Q126, Q28, Q29, WEB-14_
- **IF-2**: Infrastructure is not the constraint — the deployment population has full enterprise infrastructure. The form mismatch is at the linguistic/encoding level, not the capture level.
- **IF-3**: Yes: regulatory documents have template-driven structure (numbered SmPC sections, PIL headings) that BLURB's flat-abstract preprocessing [Q84] does not model. Sequence-length caps of 128/256/512 tokens [Q120, Q125] may also truncate long SmPC sections or cross-section equivalence pairs. — _Sources: Q84, Q120, Q125_
- **IF-4**: External validity is severely harmed: the benchmark cannot evaluate model behavior on French text, French regulatory tokenization, or template-structured documents — precisely the input form the deployment must handle. — _Sources: Q1, Q126, WEB-17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we compile a comprehensive biomedical NLP benchmark from publicly-available datasets.' (p.1)
- [Q19] 'in the continual pretraining approach, the vocabulary is the same as the original BERT model ... While convenient, this is a major disadvantage for this approach, as the vocabulary is not representative of the target biomedical domain.' (p.4)
- [Q28] 'standard BERT models are forced to divert parametrization capacity and training bandwidth to model biomedical terms using fragmented subwords.' (p.5)
- [Q29] 'naloxone, a common medical term, is divided into four pieces ... acetyltransferase is shattered into seven pieces' (p.5)
- [Q120] 'we use padding or truncation to set the input length to 128 tokens for GAD and 256 tokens for ChemProt and DDI' (p.12)
- [Q126] 'we generate the vocabulary and conduct pretraining using the latest collection of PubMed abstracts: 14 million abstracts, 3.2 billion words' (p.12)

*Web sources:*
- [WEB-14] DrBERT — French biomedical PLM pretrained from scratch (ACL 2023), not part of BLURB
- [WEB-15] CamemBERT-bio — French biomedical continual-pretraining model (LREC-COLING 2024)
- [WEB-16] AliBERT — French biomedical PLM with Unigram tokenizer (BioNLP 2023)
- [WEB-17] DrBenchmark — 20-task French biomedical evaluation suite, separate from BLURB and not regulatory-specific

</details>

**Information gaps:**
- Whether SmPC/PIL section length distributions exceed BLURB's 512-token cap in practice

**Requires expert verification:**
- Optimal French regulatory tokenizer construction strategy (vocabulary scope, treatment of INNs/ATC codes as multi-word units)

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
BLURB's output ontology consists of task-specific label spaces: BIO/BIOUL token tags for NER over chemical/disease/gene/molecular-biology entity types [Q107, Q108, Q109], five-way ChemProt relation classes [Q65], yes/no and yes/maybe/no QA labels [Q86, Q90], binary cancer hallmark indicators [Q78, Q80], and a 0–4 BIOSSES regression score [Q74, Q75]. None of these label spaces accommodates regulatory-specific entity types (INNs, ATC codes, excipient nomenclature, posology expressions, EMA-template contraindication qualifiers) or regulatory-equivalence scoring. The BIOSSES regression operationalizes general biomedical semantic proximity ['estimated similarity score in the range from 0 (no relation) to 4 (equivalent meanings)' Q74] — not the legally determinative dose-threshold/population-qualifier sensitivity the deployment requires. Web-confirmed: no regulatory-equivalence STS benchmark exists [WEB-10], and 2025 SmPC LLM extraction shows ATC codes and excipient dosages are frequently misclassified [WEB-9]. The macro-averaged BLURB summary score [Q52, Q150] does not encode any decision-boundary or human-review-trigger semantics. Some weak structural overlap exists (binary classification, regression scoring) at the abstract level, hence score 2 rather than 1.

**Strengths:**
- BLURB demonstrates that task-specific prediction layers can be cleanly layered atop a shared encoder [Q93, Q94, Q103, Q104], a transferable architectural pattern for regulatory tasks
- BIOSSES provides a concrete sentence-similarity regression schema with expert-derived gold scores [Q74, Q75] that could be structurally adapted into a regulatory-equivalence schema (with re-defined anchors)
- ChemProt's hierarchical relation taxonomy [Q65] is closer to a structured pharmaceutical interaction schema than other BLURB tasks

**Checklist:**

- **OO-1**: Output label categories are research-biomedical: chemical/disease/gene NER tags [Q108], generic chemical-protein relations [Q65], yes/no QA [Q86, Q90], cancer hallmarks [Q78]. None directly map onto regulatory NER categories (INNs, ATC, excipients, posology) or regulatory equivalence categories (dose-threshold mismatch, population-qualifier mismatch). — _Sources: Q65, Q78, Q86, Q108, WEB-9_
- **OO-2**: Missing categories: INN entity type, ATC code entity type, excipient entity type, posology expression entity type, EMA-template contraindication qualifier; and on the STS side, regulatory equivalence with critical-mismatch sub-categories (dose, population, indication scope). The web search confirms no public benchmark covers these for French [WEB-10, WEB-12]. — _Sources: Q108, WEB-10, WEB-12_
- **OO-3**: BLURB's BIOSSES regression encodes 'general semantic proximity' [Q74] as the construct, which is value-laden in the sense that it weights paraphrase/synonymy uniformly — incompatible with the deployment's principle that small lexical differences (e.g., dose thresholds) carry legal weight disproportionate to their lexical distance. — _Sources: Q74, Q75_
- **OO-4**: A stakeholder-driven taxonomy redesign is required: regulatory affairs experts under EMA/ANSM/EU AI Act normative framing [WEB-6, WEB-11] would need to define both the entity ontology and the equivalence-class taxonomy. — _Sources: WEB-6, WEB-11_
- **OO-5**: Structural validity is harmed (the construct's structure — regulatory equivalence as legally-weighted proximity — is misrepresented as uniform semantic proximity); content validity is harmed (regulatory entity categories absent); external validity is at risk because BLURB scores cannot be expected to track regulatory compliance performance. — _Sources: Q74, Q108, WEB-9, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q65] 'we follow the ChemProt authors' suggestions and focus on classifying five high-level interactions' (p.8)
- [Q74] 'The Sentence Similarity Estimation System for the Biomedical Domain ... 100 pairs of PubMed sentences each of which is annotated by five expert-level annotators with an estimated similarity score in the range from 0 (no relation) to 4 (equivalent meanings).' (p.9)
- [Q75] 'It is a regression task, with the average score as the final annotation.' (p.9)
- [Q78] 'It contains annotation on PubMed abstracts with binary labels each of which signifies the discussion of a specific cancer hallmark.' (p.9)
- [Q86] 'an annotated label of whether the text contains the answer to the research question (yes/maybe/no)' (p.9)
- [Q108] 'The NER tasks in BLURB are only concerned about one entity type (in JNLPBA, all the types are merged into one).' (p.11)

*Web sources:*
- [WEB-10] EMA 2024 AI Observatory Report — internal regulatory NLP tools (Scientific Explorer, PICROSS, EurEKA, AERGIA) but no public regulatory-equivalence benchmark
- [WEB-9] 2025 Frontiers SmPC IDMP study — ATC codes and excipient dosages 'frequently missing or misclassified' by LLMs
- [WEB-6] EMA AI Reflection Paper (Oct 2024) — defines normative framework for AI in regulatory product information lifecycle
- [WEB-11] EMA AI page including LLM Guiding Principles (Sep 2024)
- [WEB-12] DART Italian SmPC corpus — includes regulatory-relevant entity types (active substances, routes, pregnancy risk categories) closer to deployment needs

</details>

**Information gaps:**
- Whether the deployment's regulatory equivalence scoring should be ordinal, multi-label (per critical mismatch category), or hierarchical

**Requires expert verification:**
- Definition of EMA/ANSM-aligned critical-mismatch categories and their decision thresholds for human-review triggering

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
BLURB's annotator population is biomedical-research-oriented and heterogeneous: Amazon Mechanical Turkers and Upwork contributors with medical training for EBM PICO [Q60], 'five expert-level annotators' for BIOSSES [Q74], 'biomedical experts' for BioASQ [Q88], and unspecified/varied for the remaining datasets. None are regulatory affairs specialists or legal experts operating under EMA/ANSM normative frameworks. The deployment explicitly anticipates that biomedical NLP annotators will 'prioritize clinical relevance' while regulatory ground truth requires 'rigid legal constraint satisfaction,' producing systematic disagreements on borderline cases (elicitation A4). Web-confirmed: no published IAA study comparing biomedical vs regulatory annotators exists, and no regulatory-expert-annotated French pharmaceutical NER/STS dataset has been identified [WEB-12]. BLURB also does not systematically report IAA, annotator demographics, or annotation protocols across datasets. ChemProt label expansion via assigning false labels to unannotated pairs [Q66] further reflects research-pragmatic conventions that may be inappropriate where unannotated content has legal-evidentiary weight. Some annotation quality signals (BIOSSES expert annotators, EBM PICO test set quality stratification) [Q60, Q74] exist, hence score 2 rather than 1.

**Strengths:**
- BIOSSES uses five expert annotators with documented inter-annotator process [Q74], offering a usable methodological template for setting up regulatory-expert annotation
- BLURB documents the EBM PICO quality stratification (MTurk train/dev vs medically trained Upwork test) [Q60], demonstrating awareness that annotator expertise affects label quality
- BioASQ annotations by 'biomedical experts' [Q88] provide a partial precedent for domain-expert annotation in QA construction

**Checklist:**

- **OC-1**: Ground truth labels do not reflect regional regulatory stakeholder perspectives. Annotators are biomedical/clinical professionals [Q60, Q74, Q88], not regulatory affairs specialists or EMA/ANSM-aligned legal experts. — _Sources: Q60, Q74, Q88, WEB-6_
- **OC-2**: Disagreement is explicitly anticipated by the deployment elicitation (A4) on borderline cases, where biomedical annotators prioritize clinical relevance while regulatory ground truth prioritizes legal constraint satisfaction. No empirical IAA study addresses this gap [WEB-12]. — _Sources: Q60, WEB-12_
- **OC-3**: Annotator demographics are unevenly documented: EBM PICO sources are named [Q60], BIOSSES annotator count and expertise level given [Q74], BioASQ described generically as 'biomedical experts' [Q88]; for most datasets (BC5, NCBI-Disease, BC2GM, JNLPBA, ChemProt, DDI, GAD, HoC, PubMedQA) the paper does not provide annotator demographics or protocols. INSUFFICIENT DOCUMENTATION across most of the benchmark. — _Sources: Q60, Q74, Q88_
- **OC-4**: Re-annotation by EMA/ANSM-trained regulatory affairs specialists would be required for any deployment use, but is not feasible without a French regulatory document corpus to begin with. — _Sources: WEB-12_
- **OC-5**: BLURB uses macro-averaging across task types [Q52, Q150] and averages across multiple runs for small datasets [Q139, Q140] but does not document any aggregation method that preserves minority annotator perspectives — particularly relevant for the BIOSSES five-annotator average [Q75], which collapses disagreement into a single regression target. — _Sources: Q52, Q75, Q139_
- **OC-6**: Convergent validity is harmed (labels do not correlate with regulatory-stakeholder judgments); external validity is harmed (BLURB performance is unlikely to predict performance against EMA/ANSM ground truth). — _Sources: Q60, Q74, WEB-6, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q60] 'The training and development sets were labeled by Amazon Mechanical Turkers, whereas the test set was labeled by Upwork contributors with prior medical training.' (p.8)
- [Q66] 'we expand the training and development sets by assigning a false label for all chemical-protein pairs that occur in a training or development sentence, but do not have an explicit label in the ChemProt corpus.' (p.8)
- [Q74] '100 pairs of PubMed sentences each of which is annotated by five expert-level annotators' (p.9)
- [Q75] 'It is a regression task, with the average score as the final annotation.' (p.9)
- [Q88] 'The BioASQ corpus contains multiple question answering tasks annotated by biomedical experts' (p.9)
- [Q139] 'the performance may vary for different random seeds, especially for small datasets like BIOSSES, BioASQ, and PubMedQA.' (p.13)

*Web sources:*
- [WEB-12] No regulatory-expert-annotated pharmaceutical NLP dataset (French or English) identified; DART Italian corpus does not use regulatory-expert annotators
- [WEB-6] EMA AI Reflection Paper requires AI outputs in product information drafting/review to be 'factually and syntactically correct' under regulatory norms — an annotation authority BLURB does not approximate
- [WEB-10] EMA 2024 AI Observatory Report — internal regulatory NLP tools developed under EMA staff oversight, not represented in any public benchmark

</details>

**Information gaps:**
- Empirical magnitude of disagreement between biomedical and regulatory annotators on shared regulatory text — no IAA study exists [WEB-12]

**Requires expert verification:**
- Whether existing EMA/ANSM internal review checklists could be operationalized as annotation guidelines for a regulatory-grade gold standard

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
BLURB's output forms — categorical labels for classification, BIO/BIOUL sequence tags for NER, regression scores for STS, accuracy for QA, F1 variants for classification/extraction, Pearson correlation for STS [Q76, Q83, Q100, Q176] — broadly match the representational forms the deployment requires (entity tags, similarity/equivalence scores, classification labels). At this representational level the form mismatch is modest, and the deployment elicitation rates OF as MODERATE priority. However, BLURB reports only aggregate metrics: macro-averaged BLURB score [Q52, Q150], task-level F1/accuracy/Pearson, and averages across multiple runs for variance management [Q140]. There are no confidence-calibration metrics, threshold-sensitivity analyses, or human-review-triggering decision boundaries documented [Q150, Q151, Q152] — precisely the output-form information the deployment's human-review flagging workflow requires. The deployment's binary 'flag for human review' decision derives from continuous model outputs, but BLURB does not characterize model behavior at decision boundaries or report calibration. The form match is therefore partial: representational forms align, but evaluation forms (calibration, threshold sensitivity) do not.

**Strengths:**
- Output representational forms (categorical labels, sequence tags, regression scores) [Q100, Q107, Q176] directly map to the deployment's NER and STS output requirements
- BLURB provides standardized task-specific metrics (entity-level F1, micro F1, Pearson) [Q76, Q83, Q176] that are widely used and interpretable, easing methodological reuse
- Public release of pretrained and task-specific models alongside the leaderboard [Q3, Q196] supports reproducibility, which is valuable for any regulatory NLP system that must be auditable

**Checklist:**

- **OF-1**: Output modality (text labels, scores) matches the deployment's enterprise document-management integration; no speech, no mobile-output requirement is in scope. Representational match is good. — _Sources: Q100, Q107, Q176_
- **OF-2**: Not applicable — the deployment is a desktop/server enterprise context with no speech-output requirement.
- **OF-3**: Not applicable — end users are university-educated regulatory professionals; literacy and accessibility are not constraints.
- **OF-4**: External validity is harmed at the evaluation-form level: BLURB does not report confidence calibration or threshold-sensitivity analyses [Q150, Q151], and the human-review flagging workflow requires precisely this information. Aggregate F1/Pearson scores do not characterize model behavior at the decision boundary the deployment uses. — _Sources: Q150, Q151, WEB-6_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'we have released our state-of-the-art pretrained and task-specific models for the community, and created a leaderboard featuring our BLURB benchmark' (p.1)
- [Q76] 'we use the same train/dev/test split in Peng et al. and use Pearson correlation for evaluation.' (p.9)
- [Q83] 'we instead adopt the original dataset and report micro F1 across the ten cancer hallmarks.' (p.9)
- [Q100] 'We use cross-entropy loss for classification tasks and mean-square error for regression tasks.' (p.10)
- [Q150] 'The BLURB score is the macro average of average test results for each of the six tasks' (p.14)
- [Q176] 'Comparison of entity-level F1 for biomedical named entity recognition (NER) using different tagging schemes' (p.19)

*Web sources:*
- [WEB-6] EMA AI Reflection Paper requires human-oversight mechanisms and quality review for AI in product information drafting — implies threshold/calibration characterization the deployment must satisfy

</details>

**Information gaps:**
- Whether the deployment's human-review flagging is implemented as a fixed score threshold or a calibrated probability cutoff

**Requires expert verification:**
- Calibration and threshold-sensitivity reporting requirements implied by EU AI Act high-risk classification for the deployment

---

## Remediation Suggestions

### Input Form ⚠

**Gap:** BLURB is exclusively English with PubMed-derived tokenization [Q126]; the deployment requires French tokenization with regulatory vocabulary support.

**Recommendation:** Adopt a French biomedical PLM (DrBERT, CamemBERT-bio, or AliBERT [WEB-14, WEB-15, WEB-16]) as the encoder and extend its tokenizer with regulatory-specific tokens (INNs, ATC codes, French posology multi-word units), applying BLURB's own in-domain-vocabulary lessons [Q25, Q28].

### Input Content ⚠

**Gap:** BLURB contains zero French-language and zero regulatory-document content; all inputs are English PubMed abstracts [Q1, Q126].

**Recommendation:** Construct a French regulatory corpus using the QUAERO EMEA subcorpus [WEB-19, WEB-20] as a seed, supplemented by EMA-published SmPCs/PILs and ANSM-published French regulatory texts. Treat the DART Italian SmPC corpus [WEB-12] as a development-roadmap precedent.

### Output Ontology ⚠

**Gap:** No label space for regulatory entity types (INN, ATC, excipient, posology, EMA-template qualifiers); BIOSSES regression encodes general semantic proximity, not regulatory equivalence [Q74, Q108].

**Recommendation:** Define a regulatory entity ontology aligned with WHO INN/ATC and EDQM Standard Terms, and define a regulatory-equivalence STS schema with explicit critical-mismatch sub-categories (dose threshold, contraindicated population, indication scope), informed by the deployment's documented critical mismatch list and the EMA AI Reflection Paper [WEB-6].

### Output Content ⚠

**Gap:** No BLURB annotators are regulatory affairs specialists or EMA/ANSM-aligned legal experts; systematic disagreement on borderline cases is anticipated (elicitation A4).

**Recommendation:** Establish a regulatory-expert annotation pool drawn from regulatory affairs and pharmacovigilance specialists, with annotation guidelines anchored in EMA QRD templates [WEB-1] and ANSM procedural documentation. Run a calibrated IAA study comparing regulatory-expert vs biomedical-NLP annotator labels on a shared sample of regulatory text to quantify the gap.

### Input Ontology

**Gap:** BLURB's task taxonomy excludes regulatory document genres and regulatory-specific tasks (regulatory NER, regulatory equivalence STS, cross-document consistency).

**Recommendation:** Build a complementary task suite covering SmPC/PIL/CTD NER, regulatory equivalence STS (SmPC↔PIL, original↔revised), and EMA-template compliance classification. Use BLURB's six-task structure [Q48, Q52] as a reusable scoring scaffold but redefine the underlying task categories against EMA QRD v10.4 [WEB-1, WEB-2].

### Output Form

**Gap:** BLURB reports only aggregate metrics (macro-averaged scores, F1, Pearson) [Q150, Q176] and no calibration or threshold-sensitivity analysis, but the deployment requires confidence-based human-review triggering.

**Recommendation:** Augment evaluation with calibration metrics (ECE, reliability diagrams), threshold-sensitivity sweeps, and decision-boundary characterization against a regulatory-expert gold standard. Document these in line with EMA AI Reflection Paper expectations [WEB-6] and EU AI Act high-risk-system requirements.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we compile a comprehensive biomedical NLP benchmark from publicly-available datasets." |
| Q2 | 1 | input_ontology | "we discover that some common practices are unnecessary with BERT models, such as using complex tagging schemes in named entity recognition (NER)." |
| Q3 | 1 | output_form | "we have released our state-of-the-art pretrained and task-specific models for the community, and created a leaderboard featuring our BLURB benchmark (short for Biomedical Language Understanding & Reasoning Benchmark)." |
| Q4 | 1 | output_content | "Yu Gu, Robert Tinn, Hao Cheng, Michael Lucas, Naoto Usuyama, Xiaodong Liu, Tristan Naumann, Jianfeng Gao, and Hoifung Poon, Microsoft Research" |
| Q5 | 1 | input_content | "Existing pretraining work typically focuses on the newswire and Web domains." |
| Q6 | 1 | input_content | "the original BERT model was trained on Wikipedia and BookCorpus [62], and subsequent efforts have focused on crawling additional text from the Web to power even larger-scale pretraining [39, 50]." |
| Q7 | 2 | input_content | "In specialized domains like biomedicine, past work has shown that using in-domain text can provide additional gains over general-domain language models [8, 34, 45]." |
| Q8 | 2 | input_content | "However, a prevailing assumption is that out-domain text is still helpful and previous work typically adopts a mixed-domain approach, e.g., by starting domain-specific pretraining from an existing general-domain language model (Figure 1 top)." |
| Q9 | 2 | input_content | "We observe that mixed-domain pretraining such as continual pretraining can be viewed as a form of transfer learning in itself, where the source domain is general text, such as newswire and the Web, and the target domain is specialized text such as biomedical papers." |
| Q10 | 2 | input_content | "Based on the rich literature of multi-task learning and transfer learning [4, 13, 38, 59], successful transfer learning occurs when the target data is scarce and the source domain is highly relevant to the target one." |
| Q11 | 2 | input_content | "For domains with abundant unlabeled text such as biomedicine, it is unclear that domain-specific pretraining can benefit by transfer from general domains." |
| Q12 | 2 | input_content | "In fact, the majority of general domain text is substantively different from biomedical text, raising the prospect of negative transfer that actually hinders the target performance." |
| Q13 | 4 | input_content | "In this paper, we will use biomedicine as a running example in our study of domain-specific pretraining. In other words, biomedical text is considered in-domain, while others are regarded as out-domain." |
| Q14 | 4 | input_content | "Intuitively, using in-domain text in pretraining should help with domain-specific applications. Indeed, prior work has shown that pretraining with PubMed text leads to better performance in biomedical NLP tasks [8, 34, 45]." |
| Q15 | 4 | input_content | "The main question is whether pretraining should include text from other domains. The prevailing assumption is that pretraining can always benefit from more text, including out-domain text. In fact, none of the prior biomedical-related BERT models have been pretrained using purely biomedical text [8, 34, 45]." |
| Q16 | 4 | input_content | "Here, we challenge this assumption and show that domain-specific pretraining from scratch can be superior to mixed-domain pretraining for downstream applications." |
| Q17 | 4 | input_content | "The standard approach to pretraining a biomedical BERT model conducts continual pretraining of a general-domain pretrained model, as exemplified by BioBERT [34]. Specifically, this approach would initialize with the standard BERT model [16], pretrained using Wikipedia and BookCorpus. It then continues the pretraining process with MLM and NSP using biomedical text." |
| Q18 | 4 | input_content | "In the case of BioBERT, continual pretraining is conducted using PubMed abstracts and PubMed Central full text articles. BlueBERT [45] uses both PubMed text and de-identified clinical notes from MIMIC-III [26]." |
| Q19 | 4 | input_form | "Note that in the continual pretraining approach, the vocabulary is the same as the original BERT model, in this case the one generated from Wikipedia and BookCorpus. While convenient, this is a major disadvantage for this approach, as the vocabulary is not representative of the target biomedical domain." |
| Q20 | 4 | input_content | "Compared to the other biomedical-related pretraining efforts, SciBERT [8] is a notable exception as it generates the vocabulary and pretrains from scratch, using biomedicine and computer science as representatives for scientific literature. However, from the perspective of biomedical applications, SciBERT still adopts the mixed-domain pretraining approach, as computer science text is clearly out-domain." |
| Q21 | 4 | output_content | "Gu, Tinn, Cheng, et al." |
| Q22 | 5 | input_content | "The mixed-domain pretraining approach makes sense if the target application domain has little text of its own, and can thereby benefit from pretraining using related domains." |
| Q23 | 5 | input_content | "However, this is not the case for biomedicine, which has over thirty million abstracts in PubMed, and adds over a million each year." |
| Q24 | 5 | input_content | "We thus hypothesize that domain-specific pretraining from scratch is a better strategy for biomedical language model pretraining." |
| Q25 | 5 | input_form | "A major advantage of domain-specific pretraining from scratch stems from having an in-domain vocabulary." |
| Q26 | 5 | input_form | "BERT models using continual pretraining are stuck with the original vocabulary from the general-domain corpora, which does not contain many common biomedical terms." |
| Q27 | 5 | input_form | "Even for SciBERT, which generates its vocabulary partially from biomedical text, the deficiency compared to a purely biomedical vocabulary is substantial." |
| Q28 | 5 | input_form | "As a result, standard BERT models are forced to divert parametrization capacity and training bandwidth to model biomedical terms using fragmented subwords." |
| Q29 | 5 | input_form | "For example, naloxone, a common medical term, is divided into four pieces ([na, ##lo, ##xon, ##e]) by BERT, and acetyltransferase is shattered into seven pieces ([ace, ##ty, ##lt, ##ran, ##sf, ##eras, ##e]) by BERT." |
| Q30 | 5 | input_content | "Another advantage of domain-specific pretraining from scratch is that the language model is trained using purely in-domain data." |
| Q31 | 5 | input_content | "For example, SciBERT pretraining has to balance optimizing for biomedical text and computer science text, the latter of which is unlikely to be beneficial for biomedical applications." |
| Q32 | 5 | input_content | "Continual pretraining, on the other hand, may potentially recover from out-domain modeling, though not completely." |
| Q33 | 6 | input_content | "that continual pretraining may not be able to completely undo suboptimal initialization from the general-domain language model." |
| Q34 | 6 | input_content | "In our experiments, we show that domain-specific pretraining with in-domain vocabulary confers clear advantages over mixed-domain pretraining, be it continual pretraining of general-domain language models, or pretraining on mixed-domain text." |
| Q35 | 6 | input_ontology | "The ultimate goal of language model pretraining is to improve performance on a wide range of downstream applications." |
| Q36 | 6 | input_ontology | "In general-domain NLP, the creation of comprehensive benchmarks, such as GLUE [56, 57], greatly accelerates advances in language model pretraining by enabling head-to-head comparisons among pretrained language models." |
| Q37 | 6 | input_ontology | "In contrast, prior work on biomedical pretraining tends to use different tasks and datasets for downstream evaluation, as shown in Table 2." |
| Q38 | 6 | input_ontology | "To the best of our knowledge, BLUE [45] is the first attempt to create an NLP benchmark in the biomedical domain." |
| Q39 | 6 | input_ontology | "We aim to improve on its design by addressing some of its limitations." |
| Q40 | 6 | input_ontology | "First, BLUE has limited coverage of biomedical applications used in other recent work on biomedical language models, as shown in Table 2." |
| Q41 | 6 | input_ontology | "For example, it does not include any question-answering task." |
| Q42 | 6 | input_content | "More importantly, BLUE mixes PubMed-based biomedical applications (six datasets such as BC5, ChemProt, and HoC) with MIMIC-based clinical applications (four datasets such as i2b2 and MedNLI)." |
| Q43 | 6 | input_content | "Clinical notes differ substantially from biomedical literature, to the extent that we observe BERT models pretrained on clinical notes perform poorly on biomedical tasks, similar to the standard BERT." |
| Q44 | 6 | input_ontology | "Consequently, it is advantageous to create separate benchmarks for these two domains." |
| Q45 | 6 | input_ontology | "To facilitate investigations of biomedical language model pretraining and help accelerate progress in biomedical NLP, we create a new benchmark, the Biomedical Language Understanding & Reasoning Benchmark (BLURB)." |
| Q46 | 6 | input_ontology | "We focus on PubMed-based biomedical applications, and leave the exploration of the clinical domain, and other high-value verticals to future work." |
| Q47 | 7 | input_ontology | "prior work, we prioritize the selection of datasets used in recent work on biomedical language models, and will explore the addition of other datasets in future work." |
| Q48 | 7 | input_ontology | "BLURB is comprised of a comprehensive set of biomedical NLP tasks from publicly available datasets, including named entity recognition (NER), evidence-based medical information extraction (PICO), relation extraction, sentence similarity, document classification, and question answering." |
| Q49 | 7 | input_ontology | "For question answering, prior work has considered both classification tasks (e.g., whether a reference text contains the answer to a given question) and more complex tasks such as list and summary [42]." |
| Q50 | 7 | input_ontology | "The latter types often require additional engineering effort that are not relevant to evaluating neural language models." |
| Q51 | 7 | input_ontology | "For simplicity, we focus on the classification tasks such as yes/no question-answering in BLURB, and leave the inclusion of more complex question-answering to future work." |
| Q52 | 7 | output_form | "To compute a summary score for BLURB, the simplest way is to report the average score among all tasks. However, this may place undue emphasis on simpler tasks such as NER for which there are many existing datasets. Therefore, we group the datasets by their task types, compute the average score for each task type, and report the macro average among the task types." |
| Q53 | 7 | input_content | "The BioCreative V Chemical-Disease Relation corpus [35] was created for evaluating relation extraction of drug-disease interactions, but is frequently used as a NER corpus for detecting chemical (drug) and disease entities." |
| Q54 | 7 | input_content | "The dataset consists of 1500 PubMed abstracts broken into three even splits for training, development, and test." |
| Q55 | 7 | input_form | "We use a pre-processed version of this dataset generated by Crichton et al. [14], discard the relation labels, and train NER models for chemical (BC5-Chemical) and disease (BC5-Disease) separately." |
| Q56 | 8 | input_content | "NCBI-Disease. The Natural Center for Biotechnology Information Disease corpus [18] contains 793 PubMed abstracts with 6892 annotated disease mentions linked to 790 distinct disease entities. We use a pre-processed set of train, development, test splits generated by Crichton et al. [14]." |
| Q57 | 8 | input_content | "BC2GM. The Biocreative II Gene Mention corpus [53] consists of sentences from PubMed abstracts with manually labeled gene and alternative gene entities. Following prior work, we focus on the gene entity annotation. In its original form, BC2GM contains 15000 train and 5000 test sentences. We use a pre-processed version of the dataset generated by Crichton et al. [14], which carves out 2500 sentences from the training data for development." |
| Q58 | 8 | input_content | "JNLPBA. The Joint Workshop on Natural Language Processing in Biomedicine and its Applications shared task [27] is a NER corpus on PubMed abstracts. The entity types are chosen for molecular biology applications: protein, DNA, RNA, cell line, and cell type. Some of the entity type distinctions are not very meaningful. For example, a gene mention often refers to both the DNA and gene products such as the RNA and protein. Following prior work that evaluates on this dataset [34], we ignore the type distinction and focus on detecting the entity mentions. We use the same train, development, and test splits as in Crichton et al. [14]." |
| Q59 | 8 | input_content | "EBM PICO. The Evidence-Based Medicine corpus [44] contains PubMed abstracts on clinical trials, where each abstract is annotated with P, I, and O in PICO: Participants (e.g., diabetic patients), Intervention (e.g., insulin), Comparator (e.g., placebo) and Outcome (e.g., blood glucose levels). Comparator (C) labels are omitted as they are standard in clinical trials: placebo for passive control and standard of care for active control. There are 4300, 500, and 200 abstracts in training, development, and test, respectively." |
| Q60 | 8 | output_content | "The training and development sets were labeled by Amazon Mechanical Turkers, whereas the test set was labeled by Upwork contributors with prior medical training." |
| Q61 | 8 | output_form | "EBM PICO provides labels at the word level for each PIO element. For each of the PIO elements in an abstract, we tally the F1 score at the word level, and then compute the final score as the average among PIO elements in the dataset." |
| Q62 | 8 | input_content | "Occasionally, two PICO elements might overlap with each other (e.g., a participant span might contain within it an intervention span). In EBM-PICO, about 3% of the PIO words are in the overlap." |
| Q63 | 8 | input_form | "Note that the dataset released along with SciBERT appears to remove the overlapping words from the larger span (e.g., the participant span as mentioned above). We instead use the original dataset [44] and their scripts for preprocessing and evaluation." |
| Q64 | 8 | input_content | "ChemProt. The Chemical Protein Interaction corpus [31] consists of PubMed abstracts annotated with chemical-protein interactions between chemical and protein entities. There are 23 interactions organized in a hierarchy, with 10 high-level interactions (including NONE). The vast majority of relation instances in ChemProt are within single sentences. Following prior work [8, 34], we only consider sentence-level instances." |
| Q65 | 8 | output_ontology | "We follow the ChemProt authors' suggestions and focus on classifying five high-level interactions — UPREGULATOR (CPR : 3), DOWNREGULATOR (CPR : 4), AGONIST (CPR : 5), ANTAGONIST (CPR : 6), SUBSTRATE (CPR : 9) — as well as everything else (false)." |
| Q66 | 8 | input_form | "The ChemProt annotation is not exhaustive for all chemical-protein pairs. Following previous work [34, 45], we expand the training and development sets by assigning a false label for all chemical-protein pairs that occur in a training or development sentence, but do not have an explicit label in the ChemProt corpus." |
| Q67 | 8 | output_content | "Note that prior work uses slightly different label expansion of the test data. To facilitate head-to-head comparison, we will provide instructions for reproducing the test set in BLURB from the original dataset." |
| Q68 | 8 | input_content | "DDI. The Drug-Drug Interaction corpus [21] was created to facilitate research on pharmaceutical information extraction, with a particular focus on pharmacovigilance. It contains sentence-level annotation of drug-drug interactions on PubMed abstracts. Note that some prior work [45, 61] discarded 90 training files that the authors" |
| Q69 | 9 | input_form | "We instead use the original dataset and produce our train/dev/test split of 624/90/191 files." |
| Q70 | 9 | input_content | "The Genetic Association Database corpus [11] was created semi-automatically using the Genetic Association Archive." |
| Q71 | 9 | input_content | "Specifically, the archive contains a list of gene-disease associations, with the corresponding sentences in the PubMed abstracts reporting the association studies." |
| Q72 | 9 | input_form | "Bravo et al. [11] used a biomedical NER tool to identify gene and disease mentions, and create the positive examples from the annotated sentences in the archive, and negative examples from gene-disease co-occurrences that were not annotated in the archive." |
| Q73 | 9 | input_form | "We use an existing preprocessed version of GAD and its corresponding train/dev/test split created by Lee et al. [34]." |
| Q74 | 9 | output_content | "The Sentence Similarity Estimation System for the Biomedical Domain [54] contains 100 pairs of PubMed sentences each of which is annotated by five expert-level annotators with an estimated similarity score in the range from 0 (no relation) to 4 (equivalent meanings)." |
| Q75 | 9 | output_ontology | "It is a regression task, with the average score as the final annotation." |
| Q76 | 9 | output_form | "We use the same train/dev/test split in Peng et al. [45] and use Pearson correlation for evaluation." |
| Q77 | 9 | input_content | "The Hallmarks of Cancer corpus was motivated by the pioneering work on cancer hallmarks [20]." |
| Q78 | 9 | output_ontology | "It contains annotation on PubMed abstracts with binary labels each of which signifies the discussion of a specific cancer hallmark." |
| Q79 | 9 | output_ontology | "The authors use 37 fine-grained hallmarks which are grouped into ten top-level ones." |
| Q80 | 9 | output_ontology | "We focus on predicting the top-level labels." |
| Q81 | 9 | input_content | "The dataset was released with 1499 PubMed abstracts [6] and has since been expanded to 1852 abstracts [5]." |
| Q82 | 9 | output_content | "Note that Peng et al. [45] discarded a control subset of 272 abstracts that do not discuss any cancer hallmark (i.e., all binary labels are false)." |
| Q83 | 9 | output_form | "We instead adopt the original dataset and report micro F1 across the ten cancer hallmarks." |
| Q84 | 9 | input_form | "Though the original dataset provided sentence level annotation, we follow the common practice and evaluate on the abstract level [19, 60]." |
| Q85 | 9 | input_form | "We create the train/dev/test split, as they are not available previously." |
| Q86 | 9 | output_ontology | "The PubMedQA dataset [25] contains a set of research questions, each with a reference text from a PubMed abstract as well as an annotated label of whether the text contains the answer to the research question (yes/maybe/no)." |
| Q87 | 9 | input_form | "We use the original train/dev/test split with 450, 50, and 500 questions, respectively." |
| Q88 | 9 | output_content | "The BioASQ corpus [42] contains multiple question answering tasks annotated by biomedical experts, including yes/no, factoid, list, and summary questions." |
| Q89 | 9 | input_ontology | "Pertaining to our objective of comparing neural language models, we focus on the the yes/no questions (Task 7b), and leave the inclusion of other tasks to future work." |
| Q90 | 9 | output_ontology | "Each question is paired with a reference text containing multiple sentences from a PubMed abstract and a yes/no answer." |
| Q91 | 9 | input_form | "We use the official train/dev/test split of 670/75/140 questions." |
| Q92 | 9 | input_ontology | "Pretrained neural language models provide a unifying foundation for learning task-specific models." |
| Q93 | 9 | output_ontology | "Given an input token sequence, the language model produces a sequence of vectors in the contextual representation." |
| Q94 | 9 | output_ontology | "A task-specific prediction model is then layered on top to generate the final output for a task-specific application." |
| Q95 | 10 | output_form | "Prior work on biomedical NLP often adopts different task-specific models and fine-tuning methods, which makes it difficult to understand the impact of an underlying pretrained language model on task performance." |
| Q96 | 10 | output_form | "In our primary investigation comparing pretraining strategies, we fix the task-specific model architecture using the standard method identifed here, to facilitate a head-to-head comparison among the pretrained neural language models." |
| Q97 | 10 | output_form | "Subsequently, we start with the same pretrained BERT model, and conduct additional investigation on the impact for the various choices in the task-specific models." |
| Q98 | 10 | output_form | "For prior biomedical BERT models, our standard task-specific methods generally lead to comparable or better performance when compared to their published results." |
| Q99 | 10 | input_form | "An input instance is first processed by a TransformInput module which performs task-specific transformations such as appending special instance marker (e.g., [CLS]) or dummifying entity mentions for relation extraction." |
| Q100 | 10 | output_form | "We use cross-entropy loss for classification tasks and mean-square error for regression tasks." |
| Q101 | 10 | output_form | "We conduct hyperparameter search using the development set based on task-specific metrics." |
| Q102 | 10 | output_form | "We jointly fine-tune the parameters of the task-specific prediction layer as well as the underlying neural language model." |
| Q103 | 11 | output_ontology | "Many NLP applications can be formulated as a classification or regression task, wherein either individual tokens or sequences are the prediction target." |
| Q104 | 11 | output_ontology | "Modeling choices usually vary in two aspects: the instance representation and the prediction layer." |
| Q105 | 11 | input_ontology | "Given an input text span (usually a sentence), the NER task seeks to recognize mentions of entities of interest." |
| Q106 | 11 | output_ontology | "It is typically formulated as a sequential labeling task, where each token is assigned a tag to signify whether it is in an entity mention or not." |
| Q107 | 11 | output_ontology | "BIO is the standard tagging scheme that classifies each token as the beginning of an entity (B), inside an entity (I), or outside (O)." |
| Q108 | 11 | output_ontology | "The NER tasks in BLURB are only concerned about one entity type (in JNLPBA, all the types are merged into one)." |
| Q109 | 11 | output_ontology | "Prior work has also considered more complex tagging schemes such as BIOUL, where U stands for the last word of an entity and L stands for a single-word entity." |
| Q110 | 11 | output_ontology | "Classification is done using a simple linear layer or more sophisticated sequential labeling methods such as LSTM or conditional random field (CRF)." |
| Q111 | 11 | input_ontology | "Conceptually, evidence-based medical information extraction is akin to slot filling, as it tries to identify the PIO elements in an abstract describing a clinical trial." |
| Q112 | 11 | output_ontology | "However, it can be formulated as a sequential tagging task like NER, by classifying tokens belonging to each element." |
| Q113 | 11 | output_ontology | "A token may belong to more than one element, e.g., participant (P) and intervention (I)." |
| Q114 | 11 | input_ontology | "Existing work on relation extraction tends to focus on binary relations." |
| Q115 | 11 | input_ontology | "Given a pair of entity mentions in a text span (typically a sentence), the goal is to determine if the text indicates a relation for the mention pair." |
| Q116 | 11 | output_ontology | "There are significant variations in the entity and relation representations." |
| Q117 | 11 | input_form | "To prevent overfitting by memorizing the entity pairs, the entity tokens are often augmented with start/end markers or replaced by" |
| Q118 | 12 | input_form | "For featurization, the relation instance is either represented by a special [CLS] token, or by concatenating the mention representations." |
| Q119 | 12 | input_form | "In the latter case, if an entity mention contains multiple tokens, its representation is usually produced by pooling those of individual tokens (max or average)." |
| Q120 | 12 | input_form | "For computational efficiency, we use padding or truncation to set the input length to 128 tokens for GAD and 256 tokens for ChemProt and DDI which contain longer input sequences." |
| Q121 | 12 | output_ontology | "The similarity task can be formulated as a regression problem to generate a normalized score for a sentence pair." |
| Q122 | 12 | input_form | "By default, a special [SEP] token is inserted to separate the two sentences, and a special [CLS] token is prepended to the beginning to represent the pair." |
| Q123 | 12 | input_ontology | "For each text span and category (an abstract and a cancer hallmark in HoC), the goal is to classify whether the text belongs to the category." |
| Q124 | 12 | input_ontology | "For the two-way (yes/no) or three-way (yes/maybe/no) question-answering task, the encoding is similar to the sentence similarity task." |
| Q125 | 12 | input_form | "For computational efficiency, we use padding or truncation to set the input length to 512 tokens." |
| Q126 | 12 | input_content | "For biomedical domain-specific pretraining, we generate the vocabulary and conduct pretraining using the latest collection of PubMed abstracts: 14 million abstracts, 3.2 billion words, 21 GB." |
| Q127 | 12 | input_content | "The original collection contains over 4 billion words; we filter out any abstracts with less than 128 words to reduce noise." |
| Q128 | 12 | output_form | "We use Adam [30] for the optimizer using a standard slanted triangular learning rate schedule with warm-up in 10% of steps and cool-down in 90% of steps." |
| Q129 | 12 | output_form | "Specifically, the learning rate increases linearly from zero to the peak rate of 6 × 10−4 in the first 10% of steps, and then decays linearly to zero in the remaining 90% of steps." |
| Q130 | 12 | output_form | "Training is done for 62,500 steps with batch size of 8,192, which is comparable to the computation used in previous" |
| Q131 | 13 | input_form | "The training takes about 5 days on one DGX-2 machine with 16 V100 GPUs." |
| Q132 | 13 | input_form | "We find that the cased version has similar performance to the uncased version in preliminary experiments; thus, we focus on uncased models in this study." |
| Q133 | 13 | input_form | "We use whole-word masking (WWM), with a masking rate of 15%." |
| Q134 | 13 | input_form | "BioBERT and BlueBERT conduct continual pretraining from BERT, whereas ClinicalBERT conducts continual pretraining from BioBERT; thus, they all share the same vocabulary as BERT." |
| Q135 | 13 | input_form | "Prior work in biomedical pretraining uses BERT-BASE only." |
| Q136 | 13 | output_form | "BERT-LARGE appears to yield improved performance in some preliminary experiments." |
| Q137 | 13 | output_form | "We leave an in-depth exploration to future work." |
| Q138 | 13 | output_form | "For task-specific fine-tuning, we use Adam [30] with the standard slanted triangular learning rate schedule (warm-up in the first 10% of steps and cool-down in the remaining 90% of steps) and a dropout probability of 0.1." |
| Q139 | 13 | output_content | "Due to random initialization of the task-specific model and drop out, the performance may vary for different random seeds, especially for small datasets like BIOSSES, BioASQ, and PubMedQA." |
| Q140 | 13 | output_form | "We report the average scores from ten runs for BIOSSES, BioASQ, and PubMedQA, and five runs for the others." |
| Q141 | 13 | output_form | "For all datasets, we use the development set for tuning the hyperparameters with the same range: learning rate (1e-5, 3e-5, 5e-5), batch size (16, 32) and epoch number (2–60)." |
| Q142 | 13 | output_form | "Ideally, we would conduct separate hyperparameter tuning for each model on each dataset." |
| Q143 | 13 | output_form | "However, this would incur a prohibitive amount of computation, as we have to enumerate all combinations of models, datasets and hyperparameters, each of which requires averaging over multiple runs with different randomization." |
| Q144 | 13 | output_form | "In practice, we observe that the development performance is not very sensitive to hyperparameter selection, as long as they are in a ballpark range." |
| Q145 | 13 | output_form | "Consequently, we focus on hyperparameter tuning using a subset of representative models such as BERT and BioBERT, and use a common set of hyperparameters for each dataset that work well for both out-domain and in-domain language models." |
| Q146 | 14 | input_ontology | "In this section, we conduct a thorough evaluation to assess the impact of domain-specific pretraining in biomedical NLP applications." |
| Q147 | 14 | output_form | "First, we fix the standard task-specific model for each task in BLURB, and conduct a head-to-head comparison of domain-specific pretraining and mixed-domain pretraining." |
| Q148 | 14 | output_form | "Next, we evaluate the impact of various pretraining options such as vocabulary, whole-word masking (WWM), and adversarial pretraining." |
| Q149 | 14 | output_form | "Finally, we fix a pretrained BERT model and compare various modeling choices for task-specific fine-tuning." |
| Q150 | 14 | output_form | "The BLURB score is the macro average of average test results for each of the six tasks (NER, PICO, relation extraction, sentence similarity, document classification, question answering)." |
| Q151 | 14 | output_form | "We compare BERT models by applying them to the downstream NLP applications in BLURB." |
| Q152 | 14 | output_form | "For each task, we conduct the same fine-tuning process using the standard task-specific model as specified in subsection 2.4." |
| Q153 | 14 | output_form | "By conducting domain-specific pretraining from scratch, PubMedBERT consistently outperforms all the other BERT models in most biomedical NLP tasks, often by a significant margin." |
| Q154 | 14 | input_content | "Models using biomedical text in pretraining generally perform better." |
| Q155 | 14 | input_content | "However, mixing out-domain data in pretraining generally leads to worse performance." |
| Q156 | 14 | input_content | "In particular, even though clinical notes are more relevant to the biomedical domain than general-domain text, adding them does not confer any advantage, as evident by the results of ClinicalBERT and BlueBERT." |
| Q157 | 15 | output_content | "notable exception is PubMedQA, but this dataset is small, and there are relatively high variances among runs with different random seeds." |
| Q158 | 15 | output_form | "Compared to the published results for BioBERT, SciBERT, and BlueBERT in their original papers, our results are generally comparable or better for the tasks they have been evaluated on." |
| Q159 | 15 | input_ontology | "To assess the impact of pretraining options on downstream applications, we conduct several ablation studies using PubMedBERT as a running example." |
| Q160 | 15 | input_form | "Using the original BERT vocabulary derived from Wikipedia & BookCorpus (by continual pretraining from the original BERT), the results are significantly worse than using an in-domain vocabulary from PubMed." |
| Q161 | 15 | output_form | "Additionally, WWM leads to consistent improvement across the board, regardless of the vocabulary in use." |
| Q162 | 15 | input_form | "A significant advantage in using an in-domain vocabulary is that the input will be shorter in downstream tasks, as shown in Table 8, which makes learning easier." |
| Q163 | 15 | input_content | "Furthermore, we found that pretraining on general-domain text provides no benefit even if we use the in-domain vocabulary; see Table 9." |
| Q164 | 15 | input_content | "In sum, general-domain pretraining confers no advantage here in domain-specific pretraining." |
| Q165 | 16 | input_content | "In our standard PubMedBERT pretraining, we used PubMed abstracts only." |
| Q166 | 16 | input_content | "We also tried adding full-text articles from PubMed Central (PMC), with the total pretraining text increased substantially to 16.8 billion words (107 GB)." |
| Q167 | 16 | input_content | "Surprisingly, this generally leads to a slight degradation in performance across the board." |
| Q168 | 17 | input_form | "Table 8. Comparison of the average input length in word pieces using general-domain vs in-domain vocabulary." |
| Q169 | 17 | output_form | "Table 9. Evaluation of the impact of pretraining corpora and time on the performance on BLURB. In the first two columns, pretraining was first conducted on Wiki & Books, then on PubMed abstracts. All use the same amount of compute (twice as long as original BERT pretraining), except for the third column, which only uses half (same as original BERT pretraining)." |
| Q170 | 17 | input_content | "extending pretraining for 60% longer (100K steps in total), the overall results improve and slightly outperform the standard PubMedBERT using only abstracts. We hypothesize that the reason for this behavior is two-fold. First, PMC inclusion is influenced by funding policy and differs from general PubMed distribution, and full texts generally contain more noise than abstracts. As most existing biomedical NLP tasks are based on abstracts, full texts may be slightly out-domain compared to abstracts. Moreover, even if full texts are potentially helpful, their inclusion requires additional pretraining cycles to make use of the extra information." |
| Q171 | 18 | output_form | "Adversarial pretraining has been shown to be highly effective in boosting performance in general-domain applications [37]. We thus conducted adversarial pretraining in PubMedBERT and compared its performance with standard pretraining (Table 11). Surprisingly, adversarial pretraining generally leads to a slight degradation in performance, with some exceptions such as sentence similarity (BIOSSES). We hypothesize that the reason may be similar to what we observe in pretraining with full texts. Namely, adversarial training is most useful if the pretraining corpus is more diverse and relatively out-domain compared to the application tasks. We leave a more thorough evaluation of adversarial pretraining to future work." |
| Q172 | 18 | output_form | "In the above studies on pretraining methods, we fix the fine-tuning methods to the standard methods described in subsection 2.4. Next, we will study the effect of modeling choices in task-specific fine-tuning, by fixing the underlying pretrained language model to our standard PubMedBERT (WWM, PubMed vocabulary, pretrained using PubMed abstracts)." |
| Q173 | 18 | output_ontology | "Prior to the current success of pretraining neural language models, standard NLP approaches were often dominated by sequential labeling methods, such as conditional random fields (CRF) and more recently recurrent" |
| Q174 | 19 | output_ontology | "Such methods were particularly popular for named entity recognition (NER) and relation extraction." |
| Q175 | 19 | output_form | "Comparison of linear layers vs recurrent neural networks for task-specific fine-tuning in named entity recognition (entity-level F1) and relation extraction (micro F1), all using the standard PubMedBERT." |
| Q176 | 19 | output_form | "Comparison of entity-level F1 for biomedical named entity recognition (NER) using different tagging schemes and the standard PubMedBERT." |
| Q177 | 19 | output_form | "Comparison of PubMedBERT performance on BLURB using standard and adversarial pretraining." |
| Q178 | 20 | output_ontology | "With the advent of BERT models and the self-attention mechanism, the utility of explicit sequential modeling becomes questionable." |
| Q179 | 20 | output_ontology | "We find that this is indeed the case for NER and relation extraction, as shown in Table 12." |
| Q180 | 20 | output_form | "The use of a bidirectional LSTM (Bi-LSTM) does not lead to any substantial gain compared to linear layer." |
| Q181 | 20 | output_ontology | "We thus conducted a head-to-head comparison of the tagging schemes using three biomedical NER tasks in BLURB." |
| Q182 | 20 | output_form | "As we can see in Table 13, the difference is minuscule, suggesting that with self-attention, the sequential nature of the tags is less essential in NER modeling." |
| Q183 | 20 | input_form | "With entity dummification, the entity mentions in question are anonymized using entity type tags such as $DRUG or $GENE." |
| Q184 | 20 | input_form | "With entity marker, special tags marking the start and end of an entity are appended to the entity mentions in question." |
| Q185 | 20 | input_form | "Relation encoding is derived from the special [CLS] token appended to the beginning of the text or the special entity start token, or by concatenating the contextual representation of the entity mentions in question." |
| Q186 | 20 | input_form | "It is a common practice to "dummify" entities (i.e., replace an entity with a generic tag such as $DRUG or $GENE)." |
| Q187 | 20 | output_ontology | "We thus conducted a systematic evaluation of entity dummification and relation encoding, using two relation extraction tasks in BLURB." |
| Q188 | 20 | input_form | "For entity marking, we consider three variants: dummify the entities in question; use the original text; add start and end tags to entities in question." |
| Q189 | 20 | input_form | "For relation encoding, we consider three schemes. In the [CLS] encoding introduced by the original BERT paper, the special token [CLS] is prepended to the beginning of the text span, and its contextual representation at the top layer is used as the input in the final classification." |
| Q190 | 20 | input_form | "Another standard approach concatenates the BERT encoding of the given entity mentions, each obtained by applying max pooling." |
| Q191 | 21 | input_content | "There are a plethora of biomedical NLP datasets, especially from various shared tasks such as BioCreative [3, 29, 40, 53], BioNLP [15, 28], SemEval [2, 9, 10, 17], and BioASQ [42]." |
| Q192 | 21 | input_ontology | "The focus has evolved from simple tasks, such as named entity recognition, to more sophisticated tasks, such as relation extraction and question answering, and new tasks have been proposed for emerging application scenarios such as evidence-based medical information extraction [44]." |
| Q193 | 21 | input_ontology | "However, while comprehensive benchmarks and leaderboards are available for the general domains (e.g., GLUE [57] and SuperGLUE [56]), they are still a rarity in biomedical NLP." |
| Q194 | 21 | input_ontology | "In this paper, inspired by prior effort towards this direction [45], we create the first leaderboard for biomedical NLP, BLURB — a comprehensive benchmark containing thirteen datasets for six tasks." |
| Q195 | 21 | input_ontology | "To facilitate this study, we create BLURB, a comprehensive benchmark for biomedical NLP featuring a diverse set of tasks such as named entity recognition, relation extraction, document classification, and question answering." |
| Q196 | 21 | output_form | "To accelerate research in biomedical NLP, we release our state-of-the-art biomedical BERT models and setup a leaderboard based on BLURB." |
| Q197 | 22 | input_ontology | "Future directions include: further exploration of domain-specific pretraining strategies; incorporating more tasks in biomedical NLP; extension of the BLURB benchmark to clinical and other high-value domains." |
| Q198 | 24 | input_content | "A corpus with multi-level annotations of patients, interventions and outcomes to support language processing for medical literature." |
| Q199 | 24 | output_form | "Transfer Learning in Biomedical Natural Language Processing: An Evaluation of BERT and ELMo on Ten Benchmarking Datasets." |
| Q200 | 24 | input_ontology | "Results of the Seventh Edition of the BioASQ Challenge." |
| Q201 | 24 | output_ontology | "BIOSSES: a semantic sentence similarity estimation system for the biomedical domain." |
| Q202 | 24 | input_ontology | "Overview of BioCreative II gene mention recognition." |
| Q203 | 24 | input_ontology | "Drug–drug interaction extraction via hierarchical RNNs on sequence and shortest dependency paths." |
| Q204 | 24 | input_ontology | "Enhancing clinical concept extraction with contextual embeddings." |
| Q205 | 24 | input_ontology | "GLUE: A MULTI-TASK BENCHMARK AND ANALYSIS PLATFORM FOR NATURAL LANGUAGE UNDERSTANDING." |
| Q206 | 24 | input_ontology | "Superglue: A stickier benchmark for general-purpose language understanding systems." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/product-information-requirements/product-information-qrd-templates-human |
| WEB-2 | https://www.ema.europa.eu/en/documents/template-form/qrd-product-information-template-version-104-highlighted_en.pdf |
| WEB-3 | https://www.ema.europa.eu/en/documents/template-form/quality-review-documents-qrd-annotated-template-v11-draft-public-consultation_en.pdf |
| WEB-4 | https://www.ema.europa.eu/en/about-us/data-protection-privacy-ema |
| WEB-5 | https://rlsciences.com/ema-policy-0070-overview/ |
| WEB-6 | https://www.ema.europa.eu/en/documents/scientific-guideline/reflection-paper-use-artificial-intelligence-ai-medicinal-product-lifecycle_en.pdf |
| WEB-7 | https://www.axeregel.com/blog/45/brexit-impact-updates-on-qrd-templates |
| WEB-8 | https://www.hma.eu/human-medicines/cmdh/templates/qrd.html |
| WEB-9 | https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2025.1598979/full |
| WEB-10 | https://www.ema.europa.eu/en/documents/report/2024-ai-observatory-report_en.pdf |
| WEB-11 | https://www.ema.europa.eu/en/about-us/how-we-work/data-regulation-big-data-other-sources/artificial-intelligence |
| WEB-12 | https://arxiv.org/html/2510.18475 |
| WEB-13 | https://www.chapsvision.com/blog/sovereign-ai-pharma-compliance/ |
| WEB-14 | https://arxiv.org/abs/2304.00958 |
| WEB-15 | https://arxiv.org/abs/2306.15550 |
| WEB-16 | https://aclanthology.org/2023.bionlp-1.19/ |
| WEB-17 | https://aclanthology.org/2024.lrec-main.478/ |
| WEB-18 | https://www.europeanpharmaceuticalreview.com/article/264445/ai-act-data-governance-and-compliance-strategy-implications-in-pharma/ |
| WEB-19 | https://quaerofrenchmed.limsi.fr/ |
| WEB-20 | https://huggingface.co/datasets/DrBenchmark/QUAERO |
| WEB-21 | https://drbenchmark.univ-avignon.fr/ |
| WEB-22 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5756095/ |
| WEB-23 | https://intuitionlabs.ai/articles/nlp-regulatory-labeling |

---

