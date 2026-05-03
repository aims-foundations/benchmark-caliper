## Deployment Context

**Use case:** Document-level translation of agricultural input subsidy notices, land-use policy updates, and credit-scheme terms from federal and regional bureaus into Amharic
**Target population:** Farmer cooperative leaders and rural microfinance clients (e.g., ACSI, ADCSI borrowers) in Amhara interpreting government and lender document

# Validity Analysis: afridoc_mt
**Target context:** Amhara Region Agricultural & Microfinance Document Translation — Cooperative and Rural MFI End-Users
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 3 | Moderate gaps | medium |
| **Average** | **2.3** | | |

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

AFRIDOC-MT is a high-quality document-level MT benchmark for five African languages including Amharic in Ethiopic script, but its fitness for evaluating Amharic agricultural and microfinance document translation in Amhara region is severely limited by three convergent gaps: (1) total domain absence — no agricultural, land-tenure, cooperative governance, or credit-scheme content exists in the benchmark, confirmed empirically across all sampled examples and corroborated by web research showing no other Amharic MT benchmark covers these domains either; (2) source-language direction mismatch — the benchmark translates from English to Amharic and exhibits acknowledged translationese, whereas the deployment operates on documents natively authored in Amharic proclamation register; and (3) annotator-authority mismatch — the four named Amharic translators were prepared for health/IT domains with no documented agricultural or legal Amharic expertise, while the user-specified preferred ground-truth authority is federal bureau translators. Output scoring is calibrated for narrative discourse coherence with no metric for terminological consistency — the critical coherence requirement for legal-administrative documents. The benchmark's strongest alignment is on Input Form (text-only Amharic in Ethiopic script with documented tokenization accommodations) and Output Form (text output modality match). Of the three HIGH-priority dimensions (IO, IC, OC), all score 1-2.

## Practical Guidance

### What This Benchmark Measures

AFRIDOC-MT can credibly measure: (a) general document-level MT capability for English-to-Amharic in Ethiopic script using NLLB-200, GPT-4o, and other current systems [Q4, Q41]; (b) basic discourse coherence in narrative health and IT news [Q16, Q55]; (c) fluency-vs-accuracy tradeoffs for Amharic at sentence-level vs. pseudo-document granularities [Q61, Q72]; (d) which model architectures struggle with non-Latin script and morphological richness [Q53, Q127]. The strongest dimensions for the deployment are Input Form (4) and Output Form (3), reflecting that the benchmark technically handles Amharic text in Ethiopic script and produces text outputs at relevant granularities.

### Construct Depth

Construct depth is shallow for the deployment's specific construct (legal-administrative Amharic translation quality). The benchmark probes general document-level MT depth in news domains via a multi-evaluation stack (d-chrF + d-BLEU + GPT-4o-judge + human DA), but the GPT-4o judge is explicitly unreliable for African languages [Q67, Q85, Q219], leaving human DA with Amharic Krippendorff's alpha of only 0.46 [Q71] as the residual signal. No measurement instrument exists for terminological consistency across clauses [WEB-25, WEB-26 confirm metric gap], structural fidelity for numbered clauses, register-appropriateness against Ethiopian proclamation conventions, or accessibility for variable-literacy end-users. Performance on AFRIDOC-MT does not predict performance on deployment-domain documents.

### What Else You Need

Critical supplementation: (1) construct a deployment-domain test set drawing from publicly available Ethiopian proclamation Amharic (e.g., Proclamation 985/2016 [WEB-10], Proclamation 456/2005 [WEB-12]) and ACSI/EABC notices [WEB-3, WEB-5] — closing the IO and IC gaps; (2) recruit federal Ministry of Agriculture or Amhara Regional Bureau translators as annotators for that test set — closing the OC gap; (3) implement a terminology-consistency metric adapted from Semenov-Bojar or HHI [WEB-25, WEB-26] for proclamation-derived term categories — closing the OO gap; (4) add structural-fidelity and plain-language accessibility scoring if format-preserving or oral-mediation use cases are confirmed — closing the OF gap; (5) collect Amharic-source-language examples to address the source-direction mismatch.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark's task taxonomy (document-level and sentence-level MT between English and five African languages, including Amharic) is structurally relevant — the deployment also needs document-level Amharic MT, and the user agreed that document-level structural demands are broadly similar across genres. However, the test-case category distribution covers only health (WHO) and IT news (Techpoint Africa) genres [Q1, Q2, Q80], with zero coverage of agricultural input subsidy notices, land-use policy updates, credit-scheme terms, or cooperative governance documents — the four genres specified for the deployment. The only legally-binding-text instance in the entire dataset is a translation of the WHO International Health Regulations [DATASET-D17], which does not approach the register of Ethiopian federal proclamations. Web research confirms this is a sector-wide gap: no Amharic MT benchmark covers Ethiopian government proclamation, agricultural subsidy, cooperative governance, or legal-administrative domains [WEB-14, WEB-22, WEB-15]. Given the user's HIGH priority weight on IO and the total absence of deployment-relevant test categories, the score is low — but not 1, because the abstract task type (document-level Amharic MT) is correctly represented and supports both sentence-level and pseudo-document subtasks at multiple chunk sizes [Q3, Q35, Q49] that broadly match deployment document length variation.

**Strengths:**
- Document-level MT task is correctly framed and explicitly motivated by context-dependent phenomena (coreference, lexical disambiguation, lexical cohesion) [Q16] that also matter for cross-clause legal documents
- Multiple chunk-size configurations (k=5, 10, 25, full document, sentence-level) [DATASET-D5, Q49] enable evaluation at granularities relevant to bureau document lengths
- Twelve diverse model configurations evaluated [Q41], including African-centric (Toucan), broad-coverage (NLLB-200, MADLAD-400), and decoder-only LLMs, providing a useful map of MT system options for Amharic

**Checklist:**

- **IO-1**: Required deployment categories are: (1) agricultural input subsidy notices, (2) land-use policy updates, (3) credit-scheme terms / loan agreements, (4) cooperative membership and governance notices — all proclamation-derived formal administrative register documents in Amharic. Hybrid genres (e.g., MFI documents combining credit-scheme and subsidy terminology, since ACSI distributes both [WEB-7]) are also relevant. — _Sources: WEB-8, WEB-10, WEB-7_
- **IO-2**: Yes, the benchmark omits all four required categories. Source corpus is exclusively Techpoint Africa (tech news) and WHO (health news) [Q18, Q22], confirmed empirically across all 61 sampled examples [DATASET-D7, DATASET-D8, DATASET-D9, DATASET-D13]. Web research confirms no other Amharic MT benchmark covers these categories either [WEB-14, WEB-22]. — _Sources: Q1, Q2, Q80, WEB-14, WEB-22, DATASET-D7, DATASET-D13_
- **IO-3**: The IT/tech news subset (sports betting commentary [DATASET-D28], crypto/Web3 news [DATASET-D9], African tech entrepreneurship interviews [DATASET-D27]) is largely irrelevant to the deployment context and represents construct-irrelevant variance for an agricultural/microfinance use case. Health news has marginal relevance only via its policy-register subset (IHR, TRIPS) [DATASET-D17, DATASET-D18]. — _Sources: DATASET-D28, DATASET-D9, DATASET-D27, DATASET-D17_
- **IO-4**: Documented gaps: (a) total absence of agricultural proclamation register; (b) total absence of cooperative governance documents per Proclamation 985/2016 [WEB-8, WEB-10]; (c) total absence of land-tenure documents per Proclamation 456/2005 and Amhara Revised Proclamation [WEB-12, WEB-13]; (d) total absence of MFI loan-agreement instances. These constitute construct underrepresentation for the deployment's task category. — _Sources: Q2, WEB-8, WEB-12, WEB-13, WEB-14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'This paper introduces AFRIDOC-MT, a document-level multi-parallel translation dataset covering English and five African languages: Amharic, Hausa, Swahili, Yorùbá, and Zulu.' (p.1)
- [Q2] 'The dataset comprises 334 health and 271 information technology news documents, all human-translated from English to these languages.' (p.1)
- [Q14] 'To the best of our knowledge, only TICO-19, a health domain translation benchmark, has the potential to be used for document-level MT, while it is restricted to topics related to COVID-19.' (p.2)
- [Q80] 'We introduce AFRIDOC-MT, a document-level translation dataset in the health and tech domains for five African languages.' (p.9)
- [Q3] 'We conduct document-level translation benchmark experiments by evaluating the ability of neural machine translation (NMT) models and large language models (LLMs) to translate between English and these languages, at both the sentence and pseudo-document levels' (p.1)

*Web sources:*
- [WEB-14] EthioNLP survey confirms no Amharic MT benchmark covers legal-administrative domains
- [WEB-22] EthioMT parallel corpus is general-domain only
- [WEB-15] EthioLLM/EthioBenchmark covers classification, NER, sentiment, hate speech — not legal-domain MT
- [WEB-8] Cooperative Societies Proclamation 985/2016 establishes the operative cooperative tier structure for the deployment
- [WEB-10] Ministry of Justice official text confirms current cooperative proclamation

*Dataset analysis:*
- DATASET-D7: Tech document is fintech/policy news (PayDay, CBN governor) — no agricultural content
- DATASET-D13: The only 'agriculture' mention in the sample is the name of a fund (SEFAA) inside a fintech news story — not agricultural document content
- DATASET-D17: International Health Regulations is the closest legal-register item but is WHO international law, not Ethiopian proclamation
- DATASET-D5: Pseudo-document chunk (k=10) demonstrates working chunk-size configuration relevant to medium-length bureau documents

</details>

**Information gaps:**
- Whether deployment intermediaries can compose a custom evaluation set drawing from public Ethiopian proclamation Amharic texts to supplement AFRIDOC-MT
- Whether the deployment also includes oral-mediation use cases (extension worker reading aloud) that would alter the input ontology

**Requires expert verification:**
- Confirmation from Amhara Regional Bureau staff that the four listed deployment genres exhaust the operative document categories

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The input content gap is total. All English source documents are scraped from Techpoint Africa and WHO [Q18, Q22], and the Amharic translations were produced from this English source material with explicit acknowledgment of translationese risk [Q103, Q104, Q105]. The deployment requires Amharic content drawn from Ethiopian federal and regional proclamations, agricultural subsidy notices, land-tenure documents, MFI loan agreements, and cooperative governance materials — none of which appear anywhere in the corpus. Critical proclamation-derived term categories (cooperative tier names, land-tenure category labels, subsidy scheme names, MFI credit-scheme terms) are entirely absent, confirmed empirically across all sampled examples [DATASET-D9, DATASET-D4]. The source-language direction is also mismatched: the benchmark translates FROM English [Q103], whereas the deployment operates on documents natively authored in Amharic administrative register [WEB-10]. No public Amharic legal-administrative glossary exists [WEB-14, WEB-15] to serve as an external terminology anchor. Given the user's HIGH priority weight on IC and the empirical confirmation of total content absence, this dimension is at the floor.

**Strengths:**
- WHO health-policy subset includes some legally-binding international-law references (IHR, TRIPS) [DATASET-D17, DATASET-D18] — the only register-adjacent content, useful as a weak analog for numbered-clause discourse structure
- Amharic content is rendered fluently in Ethiopic script by native-speaker translators [Q23, Q24, DATASET-D2]

**Checklist:**

- **IC-1**: Yes — deployment inputs require region-specific knowledge of Ethiopian federal/regional proclamations (985/2016 cooperative; 456/2005 land; Amhara Revised 2006 + 252/2017 amendment) [WEB-8, WEB-10, WEB-12, WEB-13], Amhara-specific institutional vocabulary (ACSI, EABC, primary cooperative unions) [WEB-3, WEB-5], and Amharic administrative register conventions distinct from Addis Ababa standard. The benchmark contains none of this [DATASET concerns 1, 3]. — _Sources: WEB-8, WEB-10, WEB-12, WEB-13, WEB-3, WEB-5, DATASET-D9, DATASET-D4_
- **IC-2**: The benchmark's WHO and Techpoint sources do not align with deployment culture. The user noted contemporary documents draw primarily from federal/regional proclamation-derived terminology, which is absent. Cultural framing of the benchmark is described as English-biased [Q105]; the deployment operates within Ethiopian Orthodox Christian Amhara cultural context [WEB-11, WEB-20] with cooperative-mediated document interaction [WEB-3]. — _Sources: Q105, WEB-11, WEB-20, WEB-3_
- **IC-3**: Tech subset includes Western/global startup vocabulary (venture capital, crypto, Web3) [DATASET-D9, DATASET-D19] and sports betting [DATASET-D28] that do not transfer. Health subset is WHO-globalized rather than Ethiopia-grounded. — _Sources: DATASET-D9, DATASET-D19, DATASET-D28_
- **IC-4**: Not done in the benchmark; required for deployment evaluation. Federal bureau translators are the preferred annotation authority [elicitation Q3] but were not represented in benchmark creation [gap_3 web search]. — _Sources: Q23, Q24_
- **IC-5**: Critical content issues: (a) source-direction mismatch (English→Amharic vs. Amharic-source) [Q103, CRITICAL Concern 2]; (b) total absence of proclamation-derived terminology [CRITICAL Concern 3]; (c) translationese in reference Amharic [Q103, Q104, MAJOR Concern 3]; (d) no ACSI/EABC/cooperative scheme content [WEB-3, WEB-5]; (e) no Amhara region zone-specific administrative vocabulary. — _Sources: Q103, Q104, WEB-3, WEB-5, DATASET-D17, DATASET-D1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q18] 'We scraped English articles from the websites of Techpoint Africa and the World Health Organization (WHO).' (p.3)
- [Q22] 'we selected 334 and 271 English articles/documents from the health and tech domains respectively, which represents 10k sentences each per domain.' (p.3)
- [Q103] 'A potential limitation of our dataset is the influence of translationese... Since all source material translated originates in English, translated sentences in African languages may exhibit patterns such as unnatural syntax or overly literal phrasing.' (p.10)
- [Q105] 'AFRIDOC-MT may reflect a bias toward English in terms of structure, semantics, and cultural framing.' (p.10)
- [Q34] 'The health data is licensed under CC BY-NCSA 3.0, while the tech data is licensed under CC BY-NC-SA 4.0.' (p.4)

*Web sources:*
- [WEB-3] EABC is sole importer of fertilizer; distributes through primary cooperative unions — deployment-critical institutional vocabulary absent from benchmark
- [WEB-5] ACSI serves ~2 million clients across all woredas; key MFI in deployment
- [WEB-8] Cooperative Societies Proclamation 985/2016 defines the operative tier vocabulary
- [WEB-10] Ministry of Justice provides authoritative Amharic terminology for cooperative tiers
- [WEB-12] Land Administration Proclamation 456/2005 defines land-tenure terminology absent from benchmark
- [WEB-13] Amhara Revised Proclamation provides regional land-tenure framework
- [WEB-14] No public Amharic legal-administrative glossary exists
- [WEB-15] EthioLLM resources do not include legal-administrative MT data

*Dataset analysis:*
- DATASET-D9: Crypto/fintech vocabulary (Nestcoin, FTX, pre-seed) — zero overlap with cooperative or subsidy terminology
- DATASET-D4: Antimicrobial medical terminology — zero overlap with land-tenure or cooperative tier vocabulary
- DATASET-D17: IHR Amharic — closest regulatory-register item, still translated from English, not native administrative authoring
- DATASET-D1: Tropical cyclone Amharic exhibits English-influenced subordination — empirical confirmation of translationese risk
- DATASET-D13: Only 'agriculture' mention in entire sample is the SEFAA fund name in a fintech story

</details>

**Information gaps:**
- Whether ACSI loan-agreement Amharic templates and EABC subsidy notice templates are publicly available for use in a supplementary evaluation set
- Whether Amhara Regional Bureau translation unit maintains an internal glossary that could anchor terminology evaluation

**Requires expert verification:**
- Native-speaker assessment of register-distance between AFRIDOC-MT Amharic and federal proclamation Amharic
- Identification of specific Amharic terms most likely to be mistranslated by AFRIDOC-MT-finetuned systems

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form is the most aligned dimension and the user assigned it LOWER priority. Both benchmark and deployment are text-only, and Amharic is explicitly handled in Ethiopic (Ge'ez) script with documented accommodations: token limits were specifically increased for Amharic [Q162] because its non-Latin script produced larger token counts than English [Q127]. The benchmark adopts pseudo-document chunking with k=10 to fit Amharic within model context limits [Q47, Q48, Q128], a practical choice that the deployment will likely also need. Empirically, all sampled Amharic content is rendered consistently in Ethiopic script across all configurations [DATASET-D1, DATASET-D5, Strength 1]. The remaining concern is that the deployment may evolve toward format-preserving or multimodal translation (scanned PDFs, structured documents with tables and signature blocks) — a possibility flagged but unconfirmed in the regional context. Some annotation-workflow infrastructure (CSV/Google Sheets with paragraph-marking empty rows) [Q119, Q122] partially preserves document structure at the corpus level. Score of 4 reflects strong technical alignment on script and tokenization, with a minor gap on structural fidelity that becomes relevant only if deployment expands to format-preserving use cases.

**Strengths:**
- Amharic Ethiopic script is correctly handled across all configurations with explicit token-limit accommodation [Q162, DATASET-D1]
- Multiple chunk-size configurations (k=5, 10, 25, full document, sentence-level) [Q49, DATASET-D5] enable matching deployment document lengths
- Annotation workflow preserves paragraph-separating empty rows at corpus level [Q119]
- Token-length statistics across languages [Q33] demonstrate empirical engagement with Amharic morphological characteristics

**Checklist:**

- **IF-1**: Signal distribution match is good. Both benchmark and deployment are text-only Amharic in Ethiopic script. Deployment delivery channel is print/SMS/WhatsApp [regional context: technology_access], all of which are text representations the benchmark covers. — _Sources: Q127, DATASET-D1_
- **IF-2**: Amharic Ethiopic-script text infrastructure is supported in the benchmark; rural Amhara connectivity issues affect distribution but not the input form the MT system processes [WEB-18 on internet blockages affects delivery, not signal format]. — _Sources: Q162, WEB-18_
- **IF-3**: Domain-specific form differences: (a) deployment may include scanned PDFs requiring OCR [regional context: multimodal_future NEEDS VERIFICATION] — not assessed by AFRIDOC-MT; (b) deployment documents may include numbered clause structures, tables, signature blocks — partially preserved at corpus level [Q119] but no metric assesses preservation [Q57]; (c) Amharic register-specific token patterns of formal proclamation Amharic may differ from health/IT news Amharic — not directly addressed. — _Sources: Q47, Q119, Q33_
- **IF-4**: Form mismatches harming external validity: minor — text-only modality matches; structural fidelity gap is the only documented mismatch and is contingent on multimodal evolution. INSUFFICIENT DOCUMENTATION on whether deployment receives plain text vs. structured documents; would need consultation with Amhara Regional Bureau. — _Sources: Q119_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q47] 'An initial analysis showed that some models were unable to process entire documents due to input length limits, which were exceeded by token counts in some languages (Amharic and Yorùbá).' (p.5)
- [Q127] 'Amharic and Yorùbá—languages with unique characteristics such as non-Latin scripts and diacritics, respectively—had the largest average token counts across the tokenizers.' (p.19)
- [Q128] 'To accommodate both languages in our experiments, we chose pseudo-documents with k=10.' (p.19)
- [Q162] 'Therefore, we increased the token limit specifically for Amharic.' (p.21)
- [Q119] 'Please do not delete double empty rows, as they serve to separate paragraphs.' (p.18)
- [Q33] 'Amharic and Zulu are relatively shorter, reflecting interesting linguistic properties.' (p.4)

*Web sources:*
- [WEB-18] Internet blockages in Amhara region affect document delivery channels but not text-input signal format

*Dataset analysis:*
- DATASET-D1: Amharic Ethiopic-script document rendered consistently across multi-paragraph health content
- DATASET-D5: k=10 pseudo-document chunk in Amharic confirms working configuration
- Strength 1: All sampled Amharic content rendered consistently in Ethiopic script across all 10 configurations

</details>

**Information gaps:**
- Whether deployment receives documents as plain text, structured digital files, or scanned PDFs requiring OCR
- Per-token-count statistics for Amharic proclamation register vs. AFRIDOC-MT health Amharic

**Requires expert verification:**
- Empirical token-length comparison between AFRIDOC-MT Amharic and bureau proclamation Amharic to assess whether the chosen chunk size generalizes

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The output ontology is calibrated for news discourse: GPT-4o-judged fluency (1–5), content errors, lexical cohesion errors, and grammatical cohesion errors [Q54, Q55, Q180, Q191], plus d-chrF and d-BLEU [Q51, Q52] and human direct assessment on a 0–100 scale [Q195]. The benchmark explicitly defines lexical cohesion as 'vocabulary usage, incorrect or missing synonyms' [Q189] — narrative discourse flow, not legal terminological consistency. No rubric component evaluates whether named entities such as cooperative tier designations, land-tenure category labels, or subsidy scheme names are rendered identically across all clauses of a document — the critical coherence requirement for the deployment. Web research confirms terminology-consistency metrics exist (Semenov & Bojar WMT 2022; HHI) but have not been validated for Amharic [WEB-25, WEB-26]. Compounding this, the benchmark itself reports that GPT-4o-as-judge is unreliable for African language translation directions [Q67, Q85, Q99, Q219], leaving human DA as the residual signal — which had Krippendorff's alpha of only 0.46 for Amharic [Q71, Q211]. Given the user's MODERATE priority on OO and the partial match (d-chrF captures morphological richness [Q53], cohesion definitions touch on relevant phenomena), score is 2 rather than 1.

**Strengths:**
- d-chrF is explicitly chosen as primary because it captures morphological richness of African languages [Q53]
- Output ontology engages with discourse-level phenomena (cohesion, fluency) [Q187, Q188] that have some overlap with cross-clause requirements of legal documents
- Benchmark transparently flags GPT-4o judging unreliability for African languages [Q67, Q85, Q99, Q219], enabling informed substitution

**Checklist:**

- **OO-1**: Output label categories (fluency 1-5, CE, LE, GE, d-chrF, d-BLEU, DA 0-100) are partially relevant — fluency and content-error scoring map to deployment quality concerns, but the categories are calibrated to news adequacy rather than legal-administrative precision [Q189, Q190]. — _Sources: Q53, Q55, Q189, Q190_
- **OO-2**: Missing categories specific to the deployment: (a) terminological consistency across clauses for proclamation-derived terms — no metric exists [WEB-25, WEB-26 confirm metric gap for Amharic]; (b) structural fidelity preservation for numbered clauses; (c) register-appropriateness scoring against Ethiopian proclamation register; (d) cross-reference accuracy for proclamation article citations. — _Sources: WEB-25, WEB-26, WEB-27_
- **OO-3**: Categories assume news-discourse decision rules — 'lexical cohesion mistakes involve... overuse of certain words that disrupt the flow' [Q189] explicitly penalizes repetition, which is the opposite of what is needed for legal terminological consistency where identical repeat-rendering is required. — _Sources: Q189_
- **OO-4**: Stakeholder-driven taxonomy redesign is needed: deployment scoring should add (1) terminology-consistency (e.g., HHI-based [WEB-26]) for proclamation terms; (2) register-appropriateness assessed by federal bureau translators [elicitation Q3]; (3) structural-fidelity scoring if format preservation is required. — _Sources: WEB-25, WEB-26_
- **OO-5**: Issues harming structural validity: scoring rubric structurally misrepresents the construct of legal-administrative translation quality (treats consistent term repetition as a defect rather than a virtue [Q189]). Issues harming content validity: missing terminology-consistency, register, and structural categories. External validity at risk: GPT-4o judging shown unreliable for African languages [Q99, Q219]. — _Sources: Q67, Q99, Q219, DATASET-D17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q53] 'we report d-chrF scores... as chrF better captures the morphological richness of African languages' (p.5)
- [Q55] 'we assess each translated document's fluency, content errors (CE), and cohesion errors—specifically lexical (LE) and grammatical (GE) errors—using GPT-4o' (p.5)
- [Q189] 'Lexical Cohesion Mistakes: Issues with vocabulary usage, incorrect or missing synonyms, or overuse of certain words that disrupt the flow.' (p.23)
- [Q67] 'These inconsistencies raise concerns about GPT-4o's reliability.' (p.7)
- [Q99] 'GPT-4o was employed to assess and rate the translation outputs... While its ratings were consistent for translations into English, the same was not observed for translations into African languages, likely due to the model's limited understanding of these languages.' (p.10)
- [Q219] 'These results suggest that using GPT-4o as a translation judge is not yet well-suited for low-resource languages.' (p.26)

*Web sources:*
- [WEB-25] Semenov & Bojar (WMT 2022) terminology-consistency metric exists but not validated for African languages
- [WEB-26] HHI applied to legal corpora terminology consistency — not validated for Amharic
- [WEB-27] JUST-NLP 2025 legal MT shared task uses BLEU/METEOR/COMET only, not for African languages

*Dataset analysis:*
- DATASET-MAJOR Concern 1: Lexical cohesion definition addresses narrative flow, not legal terminological stability
- DATASET-D17: IHR document — no rubric evaluates whether 'PHEIC' is rendered identically across all clauses

</details>

**Information gaps:**
- Whether HHI or Semenov-Bojar terminology-consistency metrics can be implemented for Amharic with available resources
- Whether federal bureau translation units have internal scoring rubrics that could be adopted

**Requires expert verification:**
- Federal bureau translator validation of which output categories matter most for binding legal documents

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Reference Amharic translations were produced by four named native-speaker translators [Q23, Q109] under a controlled workflow with QE filtering at threshold 0.65 [Q28, Q29] and language-coordinator manual inspection [Q27]. However, the user's preferred ground-truth authority is domain-trained federal bureau translators [elicitation Q3], with regional bureau staff or extension workers as acceptable surrogates — and no documentation of institutional affiliation or agricultural/legal domain expertise exists for the four Amharic translators [Q109; gap_3 web search NOT FOUND]. The translators were prepared for health/IT domains via a terminology workshop [Q26], not for proclamation-derived agricultural or financial vocabulary. Inter-annotator agreement for Amharic was Krippendorff's alpha = 0.46 [Q71, Q211], described by the authors as 'relatively low' [Q71], even within the health domain in which translators were specifically prepared. Reference translations also exhibit translationese due to English source provenance [Q103, Q104]. Human evaluation used three native-speaker annotators per language [Q194], primarily drawn from the translation team [Q194], 80 documents each with 30 shared [Q197]. No demographics on annotator regional origin (Amhara region vs. other Amharic-speaking areas) are documented. Given the user's HIGH priority weight on OC and the multiple convergent gaps (annotator domain mismatch, low IAA, translationese, no federal-bureau-translator anchor), score is 2.

**Strengths:**
- Reference translations were produced by named native speakers under controlled workflow with QE [Q23, Q28]
- Pre-translation workshop shared terminology resources [Q26], demonstrating awareness of domain-terminology importance
- Translators worked with full document context [Q25], appropriate for document-level coherence requirements
- Translators were instructed not to use MT engines [Q120], reducing risk of MT-contaminated reference data
- Compensation was disclosed ($1,250 / 2,500 sentences for translators [Q31]; $55.15 for human evaluators [Q198]), enabling labor-conditions transparency

**Checklist:**

- **OC-1**: No — ground-truth labels reflect health/IT translation judgments. The user-specified preferred authority (federal bureau translators with agricultural/legal Amharic training) is unrepresented [elicitation Q3; Q109 lists translator names without institutional affiliation; gap_3 web search confirmed no public information]. — _Sources: Q109, WEB-10_
- **OC-2**: Likely substantial disagreement on domain-specific term choices. Amhara regional bureau staff and federal Ministry of Agriculture translators would apply proclamation-derived standardized terminology [WEB-10, WEB-8]; AFRIDOC-MT translators applied health/IT register translations. Disagreement is structurally expected; the magnitude is not directly measured. — _Sources: WEB-8, WEB-10, WEB-14_
- **OC-3**: Datasheet-level demographics absent. The paper names translators [Q109] and notes they were native speakers recruited via a coordinator [Q23, Q24] but provides no institutional affiliation, regional origin (Amhara-region vs. other), education, or domain training. — _Sources: Q23, Q24, Q109_
- **OC-4**: Required for deployment validity. Re-annotation by Amhara Regional Bureau translation staff or federal Ministry of Agriculture translators on a deployment-domain test set is needed. — _Sources: WEB-3_
- **OC-5**: Aggregation: human DA averages three annotators per language [Q69]. Krippendorff's alpha 0.46 for Amharic [Q71, Q211] indicates substantial inter-annotator divergence; averaging may erase legitimate domain-driven disagreements. Zulu evaluation could not be conducted at all due to recruitment difficulties [Q100], a precedent that flags fragility of the annotator-recruitment pipeline. — _Sources: Q71, Q100, Q211_
- **OC-6**: Issues harming convergent validity: translators' health/IT focus likely fails to correlate with federal bureau translator judgment on agricultural/legal terminology [WEB-14 confirms no Amharic legal-administrative resources exist for cross-validation]. External validity: judgments do not generalize to deployment ground-truth authority. Empirical: low IAA [Q71], translationese [Q103], and no documented domain expertise [DATASET-MAJOR Concern 2]. — _Sources: Q103, Q71, WEB-14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q23] 'We translated the extracted 10k English sentences to the 5 African languages through 4 expert translators per language.' (p.3)
- [Q26] 'we conducted a translation workshop, during which three translation experts shared their experiences in creating terminologies' (p.3)
- [Q71] 'We obtained Krippendorff's alpha values of ≥ 0.40, which are relatively low due to the fine granularity of the evaluation scale.' (p.8)
- [Q100] 'we were unable to recruit annotators for Zulu.' (p.10)
- [Q103] 'translated sentences in African languages may exhibit patterns such as unnatural syntax or overly literal phrasing.' (p.10)
- [Q109] 'Amharic: Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, Lidetewold Kebede' (p.11)
- [Q194] 'three native speakers of the African languages—primarily translators involved in the dataset creation—were recruited.' (p.24)
- [Q211] 'We obtained α scores of 0.46, 0.57, 0.40, and 0.81, and 0.54 for Amharic, Hausa, Swahili, Yorùbá, and Zulu respectively.' (p.26)

*Web sources:*
- [WEB-10] Ministry of Justice provides authoritative Amharic terminology — federal bureau translators are the preferred authority unrepresented in the benchmark
- [WEB-14] No public Amharic legal-administrative glossary resource exists
- [WEB-3] EABC and primary cooperative unions are the institutional terminology anchors for deployment, distinct from health/IT translator preparation

*Dataset analysis:*
- DATASET-MAJOR Concern 2: No documentation of agricultural/legal domain expertise among the four Amharic translators; preferred ground-truth authority entirely absent
- DATASET-Strength 5: Translators produced fluent Amharic with consistent technical terminology within the health domain — quality signal exists for that domain only
- DATASET-D3: Translation displays appropriate WHO pediatric-nutrition register but not transferable to agricultural register

</details>

**Information gaps:**
- Institutional affiliation and domain expertise of the four named Amharic translators
- Regional origin of Amharic translators (Amhara region vs. Addis Ababa vs. diaspora)
- Whether any of the human evaluators had agricultural or legal Amharic exposure

**Requires expert verification:**
- Federal bureau translator judgment on AFRIDOC-MT reference Amharic register-appropriateness for agricultural/legal documents
- Magnitude of expected disagreement between AFRIDOC-MT translators and federal bureau translators on a deployment-domain test set

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Output form is text-only translation [Q8, Q44, Q201], matching the deployment's text-only requirement. Document-level outputs are produced by realigning sentence-level or pseudo-document translations into full documents [Q51, Q57], partially preserving paragraph structure via maintained empty rows [Q119]. However, no metric assesses structural fidelity (preservation of numbered clauses, tables, signature blocks) [regional context: structure_preservation_gap]. The benchmark also reports specific output-form pathologies for African-language translations: under-generation, over-generation, repetition of words and phrases, off-target translations [Q6], and inconsistent diacritics [Q77] — these failure modes would be especially harmful in a legal-administrative deployment where exact term repetition matters. Embedding-based document-level evaluation for African languages remains unavailable [Q50, Q96, Q175, Q176]. Greedy decoding is used [Q155]. Given the user's MODERATE priority on OF and the partial match (text-only ✓; structural fidelity gap; no plain-language accessibility scoring for variable-literacy end-users), score is 3.

**Strengths:**
- Output modality (text in Ethiopic script) directly matches deployment text-only requirement [Q8]
- Paragraph structure preserved at corpus level via empty-row convention [Q119]
- Sentence-to-document realignment supports document-level evaluation [Q51, Q57]
- Output failure modes (under/over-generation, repetition, off-target, diacritic inconsistency) [Q6, Q77] are documented, enabling targeted detection in deployment

**Checklist:**

- **OF-1**: Yes — text output modality matches deployment [Q8, Q44]. Both benchmark and deployment produce Amharic text translations. — _Sources: Q8, Q44_
- **OF-2**: TTS not assessed by the benchmark. The deployment context indicates extension workers read documents aloud to less-literate cooperative members [regional context: oral_tradition_and_document_mediation], creating an implicit TTS-relevant accessibility requirement that AFRIDOC-MT does not address. INSUFFICIENT DOCUMENTATION on whether deployment system itself includes TTS. — _Sources: WEB-16_
- **OF-3**: Literacy considerations: Ethiopia adult literacy is 51.8% (2017) [WEB-16, WEB-17]; Amhara-region-specific and rural-Amhara-specific rates are not publicly available [regional context: NOT FOUND]. The benchmark does not assess accessibility or comprehension of translated output for variable-literacy readers; reading-level / plain-language scoring is absent. End-users are mediated by cooperative leaders and extension workers, partially mitigating the literacy gap. — _Sources: WEB-16, WEB-17_
- **OF-4**: Form mismatches harming external validity: (a) no structural-fidelity scoring for numbered clauses/tables/signature blocks [Q119 partial preservation only]; (b) no plain-language or readability scoring for variable-literacy readers; (c) documented LLM output pathologies (repetition, off-target) [Q6] would be especially harmful for legal terminology stability in deployment. — _Sources: Q6, Q77, Q119_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q6] 'some LLMs exhibit issues such as under-generation, over-generation, repetition of words and phrases, and off-target translations, specifically for translation into African languages.' (p.1)
- [Q8] 'We evaluate performance using automatic metrics and compare the results of encoder-decoder models with decoder-only LLMs' (p.1)
- [Q44] 'Given that our created dataset can be used for sentence-level translation and as a baseline for document-level translation, we evaluate all models on the test splits for each domain.' (p.5)
- [Q51] 'we realigned sentence-level or pseudo-translation outputs into full documents, then computed BLEU... and chrF... to create document BLEU (d-BLEU) and document chrF (d-chrF).' (p.5)
- [Q77] 'for Yorùbá, it often uses inconsistent or partial diacritics, resulting in inaccuracies.' (p.8)
- [Q119] 'Please do not delete double empty rows, as they serve to separate paragraphs.' (p.18)
- [Q175] 'we used BLEU and chrF scores but excluded AfriCOMET due to its backbone model... having a context length of 512 tokens.' (p.22)

*Web sources:*
- [WEB-16] Ethiopia adult literacy 51.8% (2017) — variable-literacy end-users not addressed by benchmark scoring
- [WEB-17] World Bank confirms Ethiopia literacy figure

*Dataset analysis:*
- DATASET-Strength 1: Amharic Ethiopic-script output rendering is consistent across configurations — text-form match confirmed empirically
- DATASET-D27: Tech-domain interview register confirms output-form fluency varies by source register, suggesting deployment register-shift would also affect output fluency

</details>

**Information gaps:**
- Amhara-region and rural-Amhara literacy rates
- Whether deployment system includes TTS or remains text-only
- Whether deployment delivery format requires preservation of numbered-clause / table / signature-block structure

**Requires expert verification:**
- Cooperative leader and extension worker assessment of translation comprehensibility for end-user mediation

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Critical proclamation-derived terminology (cooperative tier names per 985/2016, land-tenure category labels, subsidy scheme names, MFI credit-scheme terms) is entirely absent; source-language direction is mismatched (English→Amharic vs. native Amharic-source documents).

**Recommendation:** Compile a proclamation-terminology glossary using Ministry of Justice Amharic texts [WEB-10] and IGAD land-administration profile [WEB-12] as anchors. Build deployment test items in the deployment's actual source-language direction (Amharic source) rather than relying on AFRIDOC-MT's English source provenance. Document and probe specifically for translationese artifacts when evaluating models that have been exposed to AFRIDOC-MT-like training data.

### Input Ontology ⚠

**Gap:** All four required deployment genres (agricultural input subsidy notices, land-use policy updates, credit-scheme terms, cooperative governance notices) are absent from the benchmark, and no Amharic MT benchmark covers them.

**Recommendation:** Construct a supplementary evaluation set of 50–200 Amharic deployment-domain documents drawn from publicly available federal/regional proclamations (985/2016, 456/2005, Amhara Revised 2006), EABC subsidy notices, and ACSI loan-agreement templates. Treat AFRIDOC-MT scores as a general-MT baseline only and require deployment-domain test scores for go/no-go decisions.

### Input Ontology ⚠

**Gap:** Hybrid genres (e.g., MFI loan agreements bundled with input-subsidy distribution terms via ACSI's dual government-distribution role [WEB-7]) are not anticipated by either the benchmark or by single-genre supplementary sets.

**Recommendation:** Include hybrid ACSI-issued documents (MFI + subsidy) in the supplementary deployment-domain test set, sourced via direct consultation with ACSI or Amhara Regional Bureau partners; do not assume single-genre coverage suffices.

### Output Content ⚠

**Gap:** Reference Amharic translations were produced by translators with no documented agricultural or legal Amharic expertise; user-specified preferred authority (federal bureau translators) is absent; Amharic IAA is 0.46 even within the prepared health domain.

**Recommendation:** For deployment validation, recruit at least two federal Ministry of Agriculture or Amhara Regional Bureau translators to re-annotate a deployment-domain test set. Document annotator institutional affiliation, agricultural/legal Amharic experience, and regional origin. Report Krippendorff's alpha disaggregated by term-category to surface terminology-specific disagreement rather than averaging it away.

### Output Ontology ⚠

**Gap:** No metric evaluates terminological consistency across clauses for proclamation-derived terms; lexical cohesion definition treats term repetition as a defect, opposite to legal-document requirements; GPT-4o judge unreliable for African languages.

**Recommendation:** Implement a term-consistency metric (Semenov-Bojar WMT 2022 [WEB-25] or HHI-based [WEB-26]) over a curated list of 30–80 deployment-critical Amharic terms. Replace GPT-4o-as-judge with native-speaker review by federal bureau translators for any high-stakes evaluation. Add structural-fidelity scoring (numbered-clause preservation) if deployment evolves toward format-preserving translation.

### Output Form

**Gap:** No structural-fidelity scoring for numbered clauses, tables, or signature blocks; no readability/accessibility scoring for variable-literacy end-users mediated by cooperative leaders and extension workers.

**Recommendation:** If deployment delivers structured documents, add a structural-fidelity check (template-preservation rate). Pilot a comprehension test with cooperative leaders and extension workers from one or two woredas (where conflict access permits [WEB-4, WEB-21]) to assess plain-language accessibility of translated output, especially for read-aloud mediation.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This paper introduces AFRIDOC-MT, a document-level multi-parallel translation dataset covering English and five African languages: Amharic, Hausa, Swahili, Yorùbá, and Zulu." |
| Q2 | 1 | input_content | "The dataset comprises 334 health and 271 information technology news documents, all human-translated from English to these languages." |
| Q3 | 1 | input_ontology | "We conduct document-level translation benchmark experiments by evaluating the ability of neural machine translation (NMT) models and large language models (LLMs) to translate between English and these languages, at both the sentence and pseudo-document levels, the outputs being realigned to form complete documents for evaluation." |
| Q4 | 1 | output_form | "Our results indicate that NLLB-200 achieves the best average performance among the standard NMT models, while GPT-4o outperforms general-purpose LLMs." |
| Q5 | 1 | input_ontology | "Fine-tuning selected models leads to substantial performance gains, but models trained on sentences struggle to generalize effectively to longer documents." |
| Q6 | 1 | output_form | "Furthermore, our analysis reveals that some LLMs exhibit issues such as under-generation, over-generation, repetition of words and phrases, and off-target translations, specifically for translation into African languages." |
| Q7 | 1 | input_ontology | "In addition, AFRIDOC-MT supports multi-way translation, allowing translations not only between English and the African languages but also between any two of the languages covered." |
| Q8 | 1 | output_form | "We evaluate performance using automatic metrics and compare the results of encoder-decoder models with decoder-only LLMs" |
| Q9 | 1 | output_content | "Jesujoba O. Alabi, Israel Abebe Azime, Miaoran Zhang, Cristina España-Bonet, Rachel Bawden, Dawei Zhu, David Ifeoluwa Adelani, Clement Oyeleke Odoje, Idris Akinade, Iffat Maab, Davis David, Shamsuddeen Hassan Muhammad, Neo Putini, David O. Ademuyiwa, Andrew Caines, Dietrich Klakow" |
| Q10 | 1 | output_content | "Masakhane NLP, Saarland University, Saarland Informatic Campus, DFKI GmbH, Barcelona Supercomputing Center, Inria Paris France, Mila McGill University & Canada CIFAR AI Chair, University of Ibadan Nigeria, National Institute of Informatics Japan, Selcom Tanzania, Imperial College London, University of KwaZulu-Natal, Loughborough University U.K, University of Cambridge U.K." |
| Q11 | 2 | input_ontology | "There exist several MT evaluation benchmark datasets for African languages." |
| Q12 | 2 | input_ontology | "They can be categorized into two kinds. First, evaluation datasets specifically designed for translating into or from African languages (Ezeani et al., 2020; Azunre et al., 2021; Adelani et al., 2021, 2022, inter alia). Second, benchmark datasets covering many languages, including African languages." |
| Q13 | 2 | input_form | "However, most of these datasets are designed for sentence-level MT, primarily drawn from religious or news domains, although some consist of translated sentences originating from the same document." |
| Q14 | 2 | input_ontology | "To the best of our knowledge, only TICO-19, a health domain translation benchmark, has the potential to be used for document-level MT, while it is restricted to topics related to COVID-19." |
| Q15 | 2 | input_ontology | "Document-level NMT aims to overcome the limitations of sentence-level systems by translating an entire document as a whole." |
| Q16 | 2 | input_ontology | "Both document-level and context-aware MT allow for the possibility of improving translation quality for context-dependent phenomena such as coreference resolution (Müller et al., 2018; Bawden et al., 2018; Voita et al., 2018; Herold and Ney, 2023), lexical disambiguation (Rios Gonzales et al., 2017; Martínez Garcia et al., 2019), and lexical cohesion (Wong and Kit, 2012; Garcia et al., 2014, 2017; Bawden et al., 2018; Voita et al., 2019)." |
| Q17 | 2 | input_ontology | "Various methods have been proposed to extend sentence-level models to capture document-level context (Tiedemann and Scherrer, 2017; Libovický and Helcl, 2017; Bawden et al., 2018; Miculicich et al., 2018; Sun et al., 2022)." |
| Q18 | 3 | input_content | "We scraped English articles from the websites of Techpoint Africa and the World Health Organization (WHO). The articles cover different topics of different lengths with an average length of 30 and 37 sentences for health and tech respectively." |
| Q19 | 3 | input_form | "While our corpus is initially structured at the article level, we aim to make it suitable for sentence-level translation tasks as well." |
| Q20 | 3 | input_form | "To achieve this, we segmented the raw articles into sentences using NLTK (Bird et al., 2009)." |
| Q21 | 3 | input_form | "To ensure high segmentation quality, we recruited a linguist and a professional translator to verify the correctness of the segmentation and make corrections as needed." |
| Q22 | 3 | input_content | "Finally, we selected 334 and 271 English articles/documents from the health and tech domains respectively, which represents 10k sentences each per domain." |
| Q23 | 3 | output_content | "We translated the extracted 10k English sentences to the 5 African languages through 4 expert translators per language." |
| Q24 | 3 | output_content | "The translators were recruited through a language coordinator who is also a native speaker of the language." |
| Q25 | 3 | output_content | "The 10k sentences were distributed equally among the translators and the translations were done in-context (i.e. the translators translated on the sentence level but had access to the whole document)." |
| Q26 | 3 | output_content | "Due to the domain-specific nature of the task, before starting the translation process, we conducted a translation workshop, during which three translation experts shared their experiences in creating terminologies and they also shared existing resources with the translators including short translation guidelines (Appendix A.1)." |
| Q27 | 3 | output_content | "Quality control was conducted using automated quality estimation, followed by manual inspections by our language coordinators." |
| Q28 | 3 | output_content | "We also used Quality Estimation (QE), specifically AfriCOMET (Wang et al., 2024a), Given a translated sentence in any African language and its corresponding source English sentence, AfriCOMET generates a score between 0 and 1, where 0 indicates poor quality and higher values signify better quality." |
| Q29 | 3 | output_content | "The translators, in collaboration with the language coordinators, were tasked with reviewing instances that had quality estimation scores below 0.65." |
| Q30 | 3 | output_content | "Manual inspection indicates that QE scores below 0.65 do not necessarily reflect poor translations, consistent with Adelani et al. (2024b), likely due to" |
| Q31 | 3 | output_content | "Each translator was paid $1, 250 for 2, 500 sentences." |
| Q32 | 4 | input_form | "We created train, development (dev), and test splits for each domain. To prevent data leakage, documents sharing sentences with the same English translation were assigned to the training set. The dev set contains 25–33 documents, and the test set 59–61 documents, drawn from the remaining data." |
| Q33 | 4 | input_form | "Table 4 shows the average number of whitespace-separated tokens per sentence across domains and languages, including English. The health domain has more tokens than tech. Hausa and Yorùbá are longer than English, likely due to their descriptive nature, while Swahili is similar in length. Amharic and Zulu are relatively shorter, reflecting interesting linguistic properties." |
| Q34 | 4 | input_content | "The health data is licensed under CC BY-NCSA 3.0, while the tech data is licensed under CC BY-NC-SA 4.0." |
| Q35 | 4 | input_ontology | "Given the AFRIDOC-MT data, we conducted both sentence- and document-level translation, evaluating two types of models: encoder-decoder and decoder-only models. While the majority of these models are open-source, we also evaluated two proprietary models of the same type." |
| Q36 | 4 | output_form | "Our evaluation primarily focuses on document-level translation, reflecting the availability of our document-level translation corpus. For completeness, we also conduct a series of sentence-level experiments, with the results presented in Appendix C." |
| Q37 | 4 | input_ontology | "We evaluate five kinds of open encoder-decoder model including Toucan (Elmadany et al., 2024; Adebara et al., 2024), M2M-100 (Fan et al., 2020), NLLB200 (NLLB Team et al., 2024), MADLAD400 (Kudugunta et al., 2023), and Aya-101 (Üstün et al., 2024)." |
| Q38 | 4 | input_ontology | "Toucan is an Afro-centric multilingual MT model supporting 150 African language pairs. In comparison, M2M-100, NLLB-200, and MADLAD-400 cover between 100 and 450 language pairs. Aya-101, an instruction-tuned mT5 model (Xue et al., 2021), supports 100 languages and can translate between various languages, including those considered in AFRIDOC-MT." |
| Q39 | 4 | input_ontology | "We also evaluate open and closed decoder-only models. Open models include LLama3.1 (Dubey et al., 2024), Gemma2 (Gemma Team et al., 2024), their instruction-tuned variants, and LLaMAX3 (Lu et al., 2024)—a LLama3-based model further pre-trained on 100+ languages, including several African ones. The closed models include OpenAI GPT models (GPT-3.5 Turbo and GPT-4o) (OpenAI, 2024), which have been shown to have document-level translation ability (Wang et al., 2023)." |
| Q40 | 4 | input_content | "While their language coverage is not well documented, they show some ability to handle African languages (Adelani et al., 2024b; Bayes et al., 2024), though far below their performance in English, their primary training language." |
| Q41 | 4 | input_ontology | "We present the result of 12 models in total, including the 1.2B version of Toucan, 1.3B and 3.3B versions of NLLB-200, 3B and 13B versions of MADLAD-400 and Aya-101 respectively. We also have the 8B instruction tuned version of LLama3.1 (LLama3.1-IT), 9B version of Gemma-2 (Gemma2-IT), and LLaMAX3-Alpaca." |
| Q42 | 4 | input_ontology | "For sentence-level evaluation, we jointly fine-tune NLLB-200 with 1.3B parameters on the 30 language directions and on the two domains to make the models more specialized. Similarly, we did supervised fine-tuning (SFT) on LLaMAX3" |
| Q43 | 5 | input_form | "We perform SFT on LLaMAX3 and LLama3.1 for document-level translation, using pseudo-documents with k=10." |
| Q44 | 5 | output_form | "Given that our created dataset can be used for sentence-level translation and as a baseline for document-level translation, we evaluate all models on the test splits for each domain." |
| Q45 | 5 | output_form | "We evaluate the translation models (M2M-100, NLLB-200, and MADLAD-400) using the Fairseq (Ott et al., 2019) codebase for (M2M-100 and NLLB-200), and the Transformers (Wolf et al., 2020) codebase for MADLAD-400." |
| Q46 | 5 | output_form | "However, for other models including Aya-101, we use the EleutherAI LM Evaluation Harness (lm-eval) tool (Biderman et al., 2024) using the three templates listed in Table 23 of Appendix B.4." |
| Q47 | 5 | input_form | "An initial analysis showed that some models were unable to process entire documents due to input length limits, which were exceeded by token counts in some languages (Amharic and Yorùbá)." |
| Q48 | 5 | input_form | "To address this, we adopted a similar approach to Lee et al. (2022), splitting documents into fixed-size chunks of k sentences to fit within token limits; the final chunk may contain fewer than k sentences." |
| Q49 | 5 | output_form | "To select an appropriate chunk size, we conducted initial tests with k = 1 (sentence-level), 5, 10, and 25, choosing k = 10 for our experiments." |
| Q50 | 5 | output_form | "Evaluating document-level translation remains challenging, as existing automatic metrics struggle to capture improvements and account for discourse phenomena (Jiang et al., 2022; Dahan et al., 2024), and embedding-based metrics have not been explored in this context for African languages due to the lack of data." |
| Q51 | 5 | output_form | "Hence, we realigned sentence-level or pseudo-translation outputs into full documents, then computed BLEU (Papineni et al., 2002) and chrF (Popović, 2015) to create document BLEU (d-BLEU) and document chrF (d-chrF)." |
| Q52 | 5 | output_form | "Metrics were computed using SacreBLEU (Post, 2018) with bootstrap resampling (n = 1000) to report 95% confidence intervals." |
| Q53 | 5 | output_form | "We report d-chrF scores for the best prompt per model and language direction in the main text, as chrF better captures the morphological richness of African languages (Adelani et al., 2022), with full results provided in Appendix C." |
| Q54 | 5 | output_ontology | "We use GPT-4o as a judge to evaluate translation outputs, following recent work showing LLMs' effectiveness in assessing translation quality and analyzing errors (Wu et al., 2024; Sun et al., 2025)." |
| Q55 | 5 | output_ontology | "Following Sun et al. (2025), we assess each translated document's fluency, content errors (CE), and cohesion errors—specifically lexical (LE) and grammatical (GE) errors—using GPT-4o, with evaluation limited to a few model outputs due to cost constraints (Appendix B.6)." |
| Q56 | 5 | output_content | "We also complement this with human evaluation for direct assessment scores (Appendix B.7) and qualitative analysis through manual inspection (Appendix B.8)." |
| Q57 | 5 | output_form | "In Tables 5 and 6 we present d-chrF scores based on the realigned documents, created by merging the translated sentences into their corresponding documents." |
| Q58 | 5 | output_form | "On average the NLLB models obtain scores of 65.4/66.6 and 64.3/65.0 on health and tech domains respectively, with 3.3B outperforming 1.3B except when translating into Yorùbá." |
| Q59 | 5 | output_form | "Furthermore, translating to African languages is significantly worse compared to translating to English for all the models." |
| Q60 | 6 | output_form | "In Tables 7 and 8 we present d-chrF scores based on the best prompt per language for the translation output of the models when evaluated on the realigned documents from pseudo-documents with k =10 sentences per pseudo-document." |
| Q61 | 6 | output_form | "Pseudo-document translation is worse than sentence-level translation when translating into African languages Our results from pseudo-document translation show a performance drop across different models compared to sentence-level translation, especially when translating into African languages." |
| Q62 | 6 | output_form | "However, GPT-4o demonstrates similar and consistent performance in both setups and domains." |
| Q63 | 6 | output_form | "Additionally, we observe that GPT-3.5 is the next best performing decoder-only LLM, which contrasts with its performance in sentence-level translation." |
| Q64 | 7 | output_form | "Table 9 presents average GPT-4o evaluations for fluency and content errors (CE) of realigned outputs from sentence-level and pseudo-document-level tasks (k=10) across four models in the health domain." |
| Q65 | 7 | output_form | "When translating into English, pseudo-document outputs are generally rated as more fluent and show fewer content errors, except for LLaMAX3-SFT1, which, when evaluated on pseudo-documents, shows lower fluency but still fewer content errors—an outcome that is counterintuitive." |
| Q66 | 7 | output_form | "However, when translating into African languages, the results are less consistent." |
| Q67 | 7 | output_ontology | "These inconsistencies raise concerns about GPT-4o's reliability." |
| Q68 | 7 | output_form | "Consequently, we focus on human evaluation going forward." |
| Q69 | 7 | output_content | "In Table 10 we report average direct assessment (DA) scores (on a scale from 0 to 100) from three annotators per language for the health domain, when translating into four African languages." |
| Q70 | 7 | output_content | "For each language, we used 30 documents across models and both domains to compute inter-annotator" |
| Q71 | 8 | output_content | "We obtained Krippendorff's alpha values of ≥ 0.40, which are relatively low due to the fine granularity of the evaluation scale." |
| Q72 | 8 | output_form | "Human evaluation results align closely with d-chrF, which favors sentence-level translations over pseudo-document translations when translating into African languages." |
| Q73 | 8 | output_form | "Among the models, LLaMAX3-SFT1 receives higher ratings at the sentence-level but is rated lower when translating pseudo-documents." |
| Q74 | 8 | output_form | "In contrast, LLaMAX3-SFT10 receives slightly lower ratings than LLaMAX3-SFT1 at the sentence-level but is rated higher in the pseudo-document setting." |
| Q75 | 8 | output_form | "GPT-3.5 is generally rated as the weakest model across languages, except for Swahili, where its performance is comparatively better." |
| Q76 | 8 | output_content | "Our qualitative analysis, based on feedback from native speakers who are also authors, indicates that GPT-3.5 frequently over-generates in the pseudo-document setup by repeating words and phrases—except in Swahili, where it performs best." |
| Q77 | 8 | input_form | "However, for Yorùbá, it often uses inconsistent or partial diacritics, resulting in inaccuracies." |
| Q78 | 8 | output_form | "LLaMAX3-SFT1 also exhibits repetition in pseudo-document translations, likely due to a length generalization problem (Anil et al., 2022), and does so more than LLaMAX3-SFT10." |
| Q79 | 8 | output_form | "For the other four languages, LLaMAX3-SFT1 with the sentence-level setup was rated higher than other models and configurations, owing to better context preservation and fewer repetitions." |
| Q80 | 9 | input_content | "We introduce AFRIDOC-MT, a document-level translation dataset in the health and tech domains for five African languages." |
| Q81 | 9 | input_ontology | "We benchmarked various models, fine-tuning selected ones." |
| Q82 | 9 | input_form | "Due to context length limits, documents were translated either sentence by sentence or as pseudo-documents." |
| Q83 | 9 | output_form | "Outputs were evaluated using standard MT metrics, GPT-4o as a judge, and human direct assessment." |
| Q84 | 9 | output_form | "NLLB-200 was the strongest built-in MT model, while GPT-4o outperformed general-purpose LLMs." |
| Q85 | 9 | output_ontology | "However, our DA and qualitative analysis found GPT-4o's judgments inconsistent for African languages, and sentence-by-sentence translation proved more effective for some languages." |
| Q86 | 9 | input_ontology | "We evaluated only a small subset of the numerous multilingual LLMs available." |
| Q87 | 9 | input_form | "Our experiments were also limited by the context length of the LLMs, particularly for open LLMs." |
| Q88 | 9 | input_form | "Except for LLama3.1, all other open LLMs have a context length of 8192 tokens, while encoder-decoder models were primarily based on T5." |
| Q89 | 9 | input_form | "This makes it difficult to use the context length beyond a certain limit, making full document translation infeasible." |
| Q90 | 9 | output_form | "LLMs are prone to variance in performance based on the prompt." |
| Q91 | 9 | input_ontology | "We therefore evaluated them for translation using three different prompts." |
| Q92 | 9 | output_form | "However, it is possible that our prompts were not optimal." |
| Q93 | 10 | input_ontology | "Africa is home to thousands of indigenous languages, many of which exhibit unique linguistic properties. However, due to the high cost of translation using human translators and limited available funding, it is currently impossible to cover all languages. As a result, we focused on just five languages." |
| Q94 | 10 | input_ontology | "AFRIDOC-MT is a multi-way parallel dataset. However, due to the cost of running inference over three prompts and across all 30 translation directions for all the models evaluated, most of our analysis is limited to translation tasks between English and the five African languages." |
| Q95 | 10 | output_form | "While we fine-tuned NLLB-200, LLama3.1 and LLaMAX3 on all 30 directions, we only provide results from NLLB-200 for all directions both before and after fine-tuning for sentence-level and pseudo-document tasks in the Appendix D." |
| Q96 | 10 | output_form | "Quality evaluation in MT is an open and ongoing area of research, especially for document-level translation. Recent works have proposed embedding-based metrics for evaluation at both the sentence and document levels. While this has been well explored for high-resource language pairs, it remains underexplored for African languages, although there is a tool, AfriCOMET, that works for sentence-level evaluation in African languages." |
| Q97 | 10 | output_form | "However, we evaluated the document-level translation outputs using ModernBERT-base-long-context-qe-v1, trained on the WMT human evaluation dataset across 41 language pairs, including over 20 languages and three African languages (Hausa, Xhosa, and Zulu), two of which are included to our work." |
| Q98 | 10 | output_form | "However, the scores were nearly identical across all models, offering no meaningful differentiation. Hence, for our document-level evaluation, in addition to lexical-based metrics, we incorporated three other evaluation approaches: using GPT-4o as a judge, human evaluation, and qualitative analysis." |
| Q99 | 10 | output_ontology | "GPT-4o was employed to assess and rate the translation outputs of four models. While its ratings were consistent for translations into English, the same was not observed for translations into African languages, likely due to the model's limited understanding of these languages." |
| Q100 | 10 | output_content | "Therefore, we conducted a human evaluation for translations from English to African languages, comparing only three models due to cost constraints. However, we were unable to recruit annotators for Zulu." |
| Q101 | 10 | input_ontology | "While we fine-tuned both NLLB-1.3B and LLaMAX3 models across all 30 language directions, due to computational constraints and the high cost of qualitative evaluation, our detailed analysis focuses only on translation between English and the 5 African languages." |
| Q102 | 10 | output_form | "Nevertheless, we report quantitative results across all 30 directions for NLLB-1.3B. We will make all fine-tuned models publicly available to support future work, and we hope that further research will explore the remaining translation directions in greater depth." |
| Q103 | 10 | input_content | "A potential limitation of our dataset is the influence of translationese (Koppel and Ordan, 2011). Since all source material translated originates in English, translated sentences in African languages may exhibit patterns such as unnatural syntax or overly literal phrasing." |
| Q104 | 10 | input_content | "Although we have not conducted an analysis to quantify these effects, prior work suggests that they can affect MT model performance, generalization and evaluation including direct assessment (Freitag et al., 2019; Edunov et al., 2020)." |
| Q105 | 10 | input_content | "Furthermore, AFRIDOC-MT may reflect a bias toward English in terms of structure, semantics, and cultural framing. We leave a deeper investigation of these issues to future work." |
| Q106 | 10 | input_content | "AFRIDOC-MT was created with the utmost consideration for ethical standards. The English texts translated were sourced from publicly available and ethically sourced materials. The data sources were selected to represent different cultural perspectives, with a focus on minimizing any potential bias." |
| Q107 | 10 | input_content | "Efforts were made to ensure the dataset does not include harmful, biased, or offensive content via manual inspection." |
| Q108 | 10 | output_content | "This work was carried out with support from Lacuna Fund, an initiative co-founded by The Rockefeller Foundation, Google.org, and Canada's International Development Research Centre. This research project has benefited from the Microsoft Accelerate Foundation Models Research (AFMR)" |
| Q109 | 11 | output_content | "Also, we also appreciate the translators whose names we have listed below: 1. Amharic: Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, Lidetewold Kebede 2. Hausa: Junaid Garba, Umma Abubakar, Jibrin Adamu, Ruqayya Nasir Iro 3. Swahili: Mohamed Mwinyimkuu, Laanyu koone, Baraka Karuli Mgasa, Said Athumani Said 4. Yorùbá: Ifeoluwa Akinsola, Simeon Onaolapo, Ganiyat Dasola Afolabi, Oluwatosin Koya 5. Zulu: Busisiwe Pakade, Rooweither Mabuya, Tholakele Zungu, Zanele Thembani" |
| Q110 | 11 | output_content | "Lastly, we thank the human annotators who were not part of the translation team." |
| Q111 | 11 | output_content | "We acknowledge the support of OpenAI for providing API credits through their Researcher Access API programme." |
| Q112 | 11 | output_content | "Jesujoba Alabi acknowledges the support of the BMBF's (German Federal Ministry of Education and Research) SLIK project under the grant 01IS22015C." |
| Q113 | 11 | output_content | "The work has also been partially funded by BMBF through the TRAILS project (grant number 01IW24005)." |
| Q114 | 11 | output_content | "Miaoran Zhang received funding from the DFG (German Research Foundation) under project 232722074, SFB 1102." |
| Q115 | 11 | output_content | "CEB acknowledges her AI4S fellowship within the "Generación D" initiative by Red.es, Ministerio para la Transformación Digital y de la Función Pública, for talent attraction (C005/24-ED CV1), funded by NextGenerationEU through PRTR." |
| Q116 | 11 | output_content | "R. Bawden's participation was partly funded by her chair in the PRAIRIE institute, funded by the French national agency ANR, as part of the "Investissements d'avenir" programme under the reference ANR-19-P3IA-0001 and by the French Agence Nationale de la Recherche (ANR) under the projects TraLaLaM ("ANR-23-IAS1-0006") and MaTOS ("ANR-22-CE23-0033")." |
| Q117 | 11 | output_content | "David Adelani acknowledges the funding of IVADO and the Canada First Research Excellence Fund." |
| Q118 | 18 | input_form | "Each file contains 2500 sentences, and they are named in the format of a serial number followed by your first name." |
| Q119 | 18 | output_form | "Please do not delete double empty rows, as they serve to separate paragraphs. Also, avoid deleting any rows, columns, or provided text." |
| Q120 | 18 | output_content | "Use the language field to input the translations. It is essential not to rely on translation engines, as our quality assurance process can detect this. Depending on such tools may result in potential issues that you would need to address, leading to additional work on your part." |
| Q121 | 18 | output_content | "We will provide a list of extracted terminologies soon so that you can harmonize how terminologies are translated." |
| Q122 | 18 | input_form | "The files are in .csv format, and you can open them using Google Sheets or Microsoft Excel (for offline work)." |
| Q123 | 19 | input_form | "Given that the translated documents vary in length in terms of sentences and tokens, and considering the maximum token length limitations of the different LLMs used, we adopted a chunking approach for document-level evaluation." |
| Q124 | 19 | input_form | "In this approach, documents were divided into smaller pseudo-documents that fit within the maximum length constraints of the models." |
| Q125 | 19 | input_form | "To establish an appropriate chunk size, each document was divided into fixed-size chunks of k sentences, with the possibility that the final chunk may contain fewer than k sentences." |
| Q126 | 19 | input_form | "We conducted an initial analysis, testing different values for k (5, 10, and 25), with k=1 serving as our sentence-level setup." |
| Q127 | 19 | input_form | "Our analysis revealed that Amharic and Yorùbá—languages with unique characteristics such as non-Latin scripts and diacritics, respectively—had the largest average token counts across the tokenizers." |
| Q128 | 19 | input_form | "To accommodate both languages in our experiments, we chose pseudo-documents with k=10." |
| Q129 | 19 | input_form | "However, for the SFT models described in Appendix B.2, we used both k=5 and k=10." |
| Q130 | 19 | input_ontology | "M2M-100 (Fan et al., 2020) is a transformer-based multilingual neural translation model from Meta, trained to translate between 100 languages, including several African languages." |
| Q131 | 19 | input_ontology | "It has three variants of different sizes: 400M parameters, 1.2B parameters, and 12B parameters." |
| Q132 | 19 | input_ontology | "For our experiments, we evaluated the 400M and 1.2B variants." |
| Q133 | 19 | input_ontology | "NLLB (NLLB Team et al., 2024) is a model similar to M2M-100, with broader coverage, trained to translate between just over 200 languages, including more than 50 African languages." |
| Q134 | 19 | input_ontology | "It also has different sizes: 600M, 1.3B, 3.3B, and 54B parameters." |
| Q135 | 19 | input_ontology | "For this work, we evaluated the first three variants." |
| Q136 | 19 | input_ontology | "MADLAD-400 (Kudugunta et al., 2023) is a multilingual translation model based on the T5 architecture (Raffel et al., 2020), covering 450 languages, including many African languages." |
| Q137 | 19 | input_content | "It was trained on data collected from the Common Crawl dataset." |
| Q138 | 19 | input_content | "The dataset underwent a thorough self-audit to filter out noisy content and ensure its quality for training MT models." |
| Q139 | 19 | input_ontology | "Toucan (Elmadany et al., 2024; Adebara et al., 2024) is another multilingual but Afro-centric translation model based on the T5 architecture, covering 150 language pairs of African languages." |
| Q140 | 19 | input_content | "It was first pre-trained on large multilingual texts covering over 500 African languages and then finetuned on translation task covering over 100 language pairs." |
| Q141 | 20 | input_ontology | "Aya-101 (Üstün et al., 2024) is an instruction-tuned mT5 model (Xue et al., 2021) designed to handle both discriminative and generative multilingual tasks. With 13B parameters, it covers 100 languages and is capable of translating between a wide range of languages, including African languages." |
| Q142 | 20 | input_content | "Gemma2 (Gemma Team et al., 2024) is a decoder-only LLM trained on billions of tokens sourced from the web. The training data primarily consists of English-language text, but it also includes code and mathematical content. While Gemma2 has an English-centric focus, it also possesses multilingual capabilities. We evaluate the base Gemma2 model with 9B parameters, as well as its instruction-tuned version." |
| Q143 | 20 | input_form | "LLama3.1 (Dubey et al., 2024) is another decoder-only LLM trained on trillions of tokens across multiple languages. It was fine-tuned using existing instruction datasets as well as synthetically generated instruction data to create its instruction-tuned version. One advantage LLama3.1 has over other models is its context window of 128K tokens, the largest among all models considered in this work, making it particularly suitable for document-based tasks such as document-level translation. We evaluate the base LLama3.1 model with 8B parameters, as well as its instruction-tuned version." |
| Q144 | 20 | input_ontology | "LLaMAX3 (Lu et al., 2024) is a multilingual LLM built on the LLama3 with 8B parameters as its base. It was trained on 102 languages, including several African languages, through continued pretraining. Using an English instruction dataset (Alpaca), it was further fine-tuned to create LLaMAX3-Alpaca. We evaluated both models and compared their performance across various tasks." |
| Q145 | 20 | input_form | "We perform supervised fine-tuning to tailor LLMs for translation tasks. To train sentence-level MT systems, we use all parallel sentences from AFRIDOC-MT to construct the training set, enabling the LLMs to translate across multiple directions and domains. Following Zhu et al. (2024b), we augment the parallel data with translation instructions, which are randomly sampled from a predefined set of 31 MT instructions for each training example." |
| Q146 | 21 | input_form | "To train document-level MT systems, we follow the same process, but train on longer segments formed by concatenating multiple sentences." |
| Q147 | 21 | input_form | "When fine-tuning, we use a learning rate of 5e−6 and an effective batch size of 64." |
| Q148 | 21 | output_form | "Models are trained for only one epoch, as further training does not result in improvements and may even lead to performance degradation." |
| Q149 | 21 | input_form | "we fine-tuned the 1.3B version of NLLB-200 for sentence and pseudo-document (with 10 sentences) translation using the Fairseq (Ott et al., 2019) codebase." |
| Q150 | 21 | input_content | "We used all the training examples from 30 language directions across both domains." |
| Q151 | 21 | input_form | "The model was fine-tuned for 50k steps using a learning rate of 5e−5, token batch size of 2048 and a gradient accumulation of 2." |
| Q152 | 21 | output_form | "The checkpoint with the lowest validation loss was selected as the best model for evaluation." |
| Q153 | 21 | output_form | "The models were evaluated using different tools. For example, both the NLLB-200 and M2M-100 models were evaluated with the Fairseq codebase, while Toucan and MADLAD-400 were evaluated using the Hugging Face (HF) codebase." |
| Q154 | 21 | output_form | "All other LLMs, including LLama3.1 (both instruction-tuned and SFT models), Gemma, and Aya-101, were evaluated using EleutherAI LM Evaluation Harness (lm-eval) tool (Biderman et al., 2024)." |
| Q155 | 21 | output_form | "In all cases, greedy decoding was used." |
| Q156 | 21 | input_form | "The models evaluated have different context lengths. For encoder-decoder models, M2M-100 and NLLB have a maximum sequence length of 1024 and 512 respectively." |
| Q157 | 21 | input_form | "Aya-101 and MADALAD, based on the T5 architecture, do not have a pre-specified maximum sequence length, so we fixed their maximum sequence length to 1024 for all experiments involving encoder-decoder models." |
| Q158 | 21 | input_form | "However, for decoder-only models, Gemma and LLaMAX3 (based on LLama3) have a maximum sequence length of 8192, while LLama3.1 has a maximum sequence length of 128K." |
| Q159 | 21 | output_form | "Since all the decoder-only models were evaluated using LM Evaluation Harness, we used a similar setup for them, selecting the maximum length based on the specific needs of each model." |
| Q160 | 21 | input_form | "These numbers were chosen based on the statistics from Table 11." |
| Q161 | 21 | input_form | "However, for Amharic, when translating pseudo-documents with 25 sentences and full documents, there were instances exceeding the 95th percentile derived from the training statistics." |
| Q162 | 21 | input_form | "Therefore, we increased the token limit specifically for Amharic." |
| Q163 | 21 | output_form | "While the translation models we evaluated do not require prompts, MADLAD-400, requires a prefix of the form <2xx> token, which is prepended to the source sentence." |
| Q164 | 21 | output_form | "Similarly, Toucan uses just the target language ISO-693 code as prefix, which is prepended to the source sentence (e.g., "swa" for Swahili)." |
| Q165 | 21 | output_form | "For other models, including Aya-101, we used three different prompts for sentence-level translation and document translation experiments." |
| Q166 | 21 | output_form | "The main difference between the prompts for these tasks is the explicit mention of "text" or "document" within the prompt, as shown in Table 23." |
| Q167 | 21 | output_form | "For the base models Gemma2, Llama3.1, LLaMAX3, and Aya-101, we prompted them directly using the respective prompts." |
| Q168 | 21 | output_form | "However, for the instruction-tuned versions of Gemma2 and Llama3.1, we used their respective chat templates." |
| Q169 | 21 | output_form | "For all Alpaca-based models, including our SFT models, we used the Alpaca template." |
| Q170 | 21 | output_form | "We evaluate translation quality with BLEU (Papineni et al., 2002) and ChrF (Popović, 2015) using SacreBLEU (Post, 2018)." |
| Q171 | 21 | output_form | "We run significance tests using bootstrap resampling and report the 95%" |
| Q172 | 22 | output_form | "We also use AfriCOMET (Wang et al., 2024a) to evaluate the quality of the translation outputs." |
| Q173 | 22 | output_form | "We report the chrF scores of the best prompt for each model and language direction in the main paper, with all additional results provided in the Appendix C." |
| Q174 | 22 | input_ontology | "For document-level experiments, we evaluated the LLMs using the same three prompts as in the sentence-level experiment." |
| Q175 | 22 | output_form | "For evaluation, we used BLEU and chrF scores but excluded AfriCOMET due to its backbone model, AfroXLM-R-L (Alabi et al., 2022; Adelani et al., 2024a), having a context length of 512 tokens." |
| Q176 | 22 | output_form | "This made it impractical to compute COMET scores for document-level outputs." |
| Q177 | 22 | output_ontology | "We use GPT-4o to assess the quality of translation output, as demonstrated by Sun et al. (2025), which shows a correlation with human judgment." |
| Q178 | 22 | output_form | "Due to the cost of this task, we limited our evaluation to a few selected models, including Aya-101, GPT-3.5, GPT-4o, and LLaMAX3 fine-tuned on AFRIDOC-MT sentences and pseudo-documents of 10 sentences." |
| Q179 | 22 | output_ontology | "We compared translations performed at the sentence-level and pseudo-document level in terms of fluency, content errors, and cohesion errors—specifically lexical (LE) and grammatical (GE) errors—using the same definitions as Sun et al. (2025)." |
| Q180 | 22 | output_ontology | "GPT-4o is prompted to rate the fluency of a document on a scale from 1 to 5, where 5 indicates high fluency and 1 represents low fluency." |
| Q181 | 22 | output_form | "This evaluation is conducted without providing any reference document." |
| Q182 | 22 | output_form | "For the final fluency score, we report the average rating across all documents." |
| Q183 | 22 | output_ontology | "GPT-4 is prompted to identify and list the mistakes, such as incorrect translations, omissions, additions, and any other errors, by comparing the model's output to the reference translation." |
| Q184 | 22 | output_ontology | "After identifying these errors, we count all of them and compute the average across all documents, reporting that as the content error (CE)." |
| Q185 | 23 | output_ontology | "Cohesion: GPT-4 is prompted to rate cohesion-related mistakes, including lexical and grammatical errors, in the model's output, comparing it to the reference translation." |
| Q186 | 23 | output_ontology | "We count each error individually, compute the average across the documents, and report them as lexical errors (LE) and grammatical errors (GE)." |
| Q187 | 23 | output_ontology | "Cohesion refers to how different parts of a text are connected using language structures like grammar and vocabulary." |
| Q188 | 23 | output_ontology | "It ensures that sentences flow smoothly and the text makes sense as a whole." |
| Q189 | 23 | output_ontology | "Lexical Cohesion Mistakes: Issues with vocabulary usage, incorrect or missing synonyms, or overuse of certain words that disrupt the flow." |
| Q190 | 23 | output_ontology | "Grammatical Cohesion Mistakes: Problems with pronouns, conjunctions, or grammatical structures that link sentences and clauses." |
| Q191 | 24 | output_ontology | "Fluency can only have values between 1 and 5. However, the other metrics, including CE, GE, and LE, do not have a specific range and can take on any value because they are counts." |
| Q192 | 24 | output_content | "Beyond using GPT-4o as a judge, we also conduct human evaluation on a subset of outputs from GPT-3.5, LLaMAX3-SFT1, and LLaMAX3-SFT10 for two domains, focusing specifically on translation into five African languages due to cost constraints." |
| Q193 | 24 | output_content | "Translation into English was excluded, as existing automatic metrics, including GPT-based evaluations, are already reliable for this direction." |
| Q194 | 24 | output_content | "For the human evaluation, three native speakers of the African languages—primarily translators involved in the dataset creation—were recruited." |
| Q195 | 24 | output_content | "Each annotator was assigned 80 documents to evaluate, tasked with marking as many error spans as possible and rating the overall quality on a scale from 0 to 100." |
| Q196 | 24 | output_form | "This annotation followed the error span annotation (ESA) (Kocmi et al., 2024) protocol as implemented within the Appraise Evaluation Framework (Federmann, 2018)." |
| Q197 | 24 | output_content | "To assess consistency and inter-annotator agreement, 30 of the 80 documents were shared among all three annotators." |
| Q198 | 24 | output_content | "Each annotator was remunerated with $55.15" |
| Q199 | 24 | output_content | "Alongside the human direct assessment of the translation outputs, we shared a subset of the outputs with one author per language, each a native speaker." |
| Q200 | 24 | output_content | "They were tasked with analyzing the outputs to answer two key questions: (1) What common errors or flaws do the models exhibit across different setups? and (2) How fluent are the translation outputs produced by the models across the various settings?" |
| Q201 | 24 | output_form | "Given that AFRIDOC-MT is a document-level translation dataset, and due to the limited context length of most translation models and LLMs, which makes it impossible to translate a full document at once, we opted to translate the sentences within the documents and then merge them back to form the complete document. For document-level evaluation, we split the documents into chunks of 10 sentences and translate these chunks using the different models." |
| Q202 | 25 | output_form | "In Tables 19 and 20 we provide the full results on the merged pseudo-documents using d-chrF and d-BLEU." |
| Q203 | 25 | output_form | "It is important to note that we also trained and evaluated NLLB-200 for pseudo-document translation. However, due to its 512-token maximum sequence length, it is not competitive." |
| Q204 | 25 | output_form | "Our results show that both LLama3.1 and LLaMAX3 models, when fine-tuned on sentences, performed significantly worse on pseudo-document evaluations compared to the same models fine-tuned on pseudo-documents for both domains." |
| Q205 | 25 | input_form | "All these models were trained using a similar setup, with the primary difference being the data used for fine-tuning." |
| Q206 | 25 | output_form | "Overall, no clear trend is observed in MT performance across language family classes. However, Amharic (a non-Latin script language) and Yorùbá (a heavily diacriticitized language) result in the lowest chrF scores, while Swahili—the most widely spoken indigenous African language—performs best." |
| Q207 | 25 | output_form | "In Tables 21 and 22 we present the average GPT-4o evaluation results for four models." |
| Q208 | 25 | output_ontology | "When translating into African languages, there is no clear pattern: for example, GPT-3.5, despite having the lowest fluency score, also had the fewest content, lexical, and grammatical errors, which is counterintuitive." |
| Q209 | 26 | output_content | "We were able to obtain DA scores from three annotators for all the languages." |
| Q210 | 26 | output_content | "For each language, we calculated inter-annotator agreement using Krippendorff's alpha α over 30 document instances." |
| Q211 | 26 | output_content | "We obtained α scores of 0.46, 0.57, 0.40, and 0.81, and 0.54 for Amharic, Hausa, Swahili, Yorùbá, and Zulu respectively." |
| Q212 | 26 | output_content | "These are relatively low scores, except for Yorùbá." |
| Q213 | 26 | output_form | "We present the average DA scores in Tables 10 and 14 for the health and tech domains, respectively." |
| Q214 | 26 | output_form | "The results show that annotators rate documents translated at the sentence-level as higher quality than those translated at the pseudo-document level." |
| Q215 | 26 | output_form | "Additionally, GPT-3.5 received the lowest ratings among the three models." |
| Q216 | 26 | output_form | "LLaMAX3-SFT1, a model trained on sentence-level data, was rated the best across all languages when evaluated on sentences." |
| Q217 | 26 | output_form | "However, when evaluated on pseudo-documents, its performance was rated lower than that of LLaMAX3-SFT10." |
| Q218 | 26 | output_ontology | "These findings are consistent with the d-chrF scores for the models, but they do not align with the evaluations from GPT-4o as a judge." |
| Q219 | 26 | output_ontology | "These results suggest that using GPT-4o as a translation judge is not yet well-suited for low-resource languages." |
| Q220 | 26 | output_form | "We focus on the sentence-level task and translated across all 30 directions for which the model was trained, evaluating both NLLB-200 (1.3B) and its fine-tuned version using d-chrF." |
| Q221 | 26 | output_form | "The results shows that translating into Yorùbá, which is the direction with the lowest d-chrF score from English among all the languages, benefited the most." |
| Q222 | 26 | input_form | "One major factor contributing to this is the presence of diacritics." |
| Q223 | 26 | output_form | "Furthermore, looking at their actual performances and not just the differences, our results show that translations into Swahili and English—both relatively high-resource languages—yield higher BLEU and chrF scores (see Figures 11 and 12), even after supervised finetuning." |
| Q224 | 26 | output_form | "Hence, there is much to be done to improve translation performance between low-resource language pairs." |
| Q225 | 28 | output_form | "Change (∆) in d-BLEU and d-chrF for sentence evaluation comparing NLLB1.3B before and after supervised finetuning on AFRIDOC-MT" |
| Q226 | 29 | output_form | "Table 15: Performance results of various models on the sentence-level task for the Health domain, measured using document level metric d-BLEU and d-chrF." |
| Q227 | 29 | output_form | "Table 16: Performance results of various models on the sentence-level task for the Tech domain, measured using document level metric d-BLEU and d-chrF." |
| Q228 | 30 | output_form | "Table 17: Performance results of various models on the sentence-level task for the Health domain, measured using sentence level metric s-BLEU, s-CHRF, and s-COMET." |
| Q229 | 31 | output_form | "Performance results of various models on the sentence-level task for the Tech domain, measured using sentence level metric s-BLEU, s-CHRF, and s-COMET." |
| Q230 | 32 | output_form | "Table 19: Performance results of various models on the pseudo-document-level task for the Health domain, measured using document level metric d-BLEU and d-CHRF." |
| Q231 | 32 | output_form | "Table 20: Performance results of various models on the pseudo-document-level task for the Tech domain, measured using document level metric d-BLEU and d-CHRF." |
| Q232 | 33 | output_form | "Table 21: Document-level evaluation in the health domain, judged by GPT-4o. Compares sentence- vs. document-level outputs on Fluency (1–5 scale), Content Errors (CE), Lexical (LE), and Grammatical Cohesion Errors (GE)." |
| Q233 | 33 | output_content | "Table 21: Document-level evaluation in the health domain, judged by GPT-4o." |
| Q234 | 34 | output_form | "Document-level evaluation in the tech domain, judged by GPT-4o. Compares sentence- vs. document-level outputs on Fluency (1–5 scale), Content Errors (CE), Lexical (LE), and Grammatical Cohesion Errors (GE)." |
| Q235 | 35 | input_ontology | "The task prompts used for evaluating LLMs are applied to both sentence-level and document-level translation tasks." |
| Q236 | 37 | output_form | "Figure 19: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into African languages" |
| Q237 | 37 | output_form | "Figure 20: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into African languages" |
| Q238 | 37 | output_form | "Figure 21: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into English" |
| Q239 | 37 | output_form | "Figure 22: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into English" |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.researchgate.net/figure/Administrative-Zones-within-Amhara-Region_fig1_247830953 |
| WEB-2 | https://www.longdom.org/open-access-pdfs/determinants-of-adoption-of-wheat-row-planting-the-case-of-wogera-district-north-gondar-zone-amhara-regional-state-ethiopia.pdf |
| WEB-3 | https://addisstandard.com/sowing-under-shadows-of-violence-amhara-farmers-face-bleak-harvest-as-conflict-deepens-fertilizer-shortages-drives-up-input-prices/ |
| WEB-4 | https://www.gov.uk/government/publications/ethiopia-country-policy-and-information-notes/country-policy-and-information-note-amhara-and-amhara-opposition-groups-ethiopia-june-2025-accessible |
| WEB-5 | https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-case-study-a-review-of-ethiopian-microfinance-institutions-and-their-role-in-poverty-reduction-a-case-study-on-amhara-credit-and-saving-institution-acsi-jan-2011.pdf |
| WEB-6 | https://www.mftransparency.org/microfinance-pricing/ethiopia/002-ACSI/ |
| WEB-7 | https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-paper-subsidizing-microcredit-interest-how-important-is-it-to-the-poor-0-2004.pdf |
| WEB-8 | https://leap.unep.org/en/countries/et/national-legislation/cooperative-societies-proclamation-no-9852016 |
| WEB-9 | https://ethiodata.et/ethiopia-cooperative-societies-proclamation-no-985-2016/ |
| WEB-10 | https://justice.gov.et/en/law/cooperative-societies-proclamation-2/ |
| WEB-11 | https://en.wikipedia.org/wiki/East_Gojjam_Zone |
| WEB-12 | https://land.igad.int/index.php/countries/37-countries/ethiopia/38-ethiopia-profile?start=2 |
| WEB-13 | https://ukgreencitiesandinfrastructure.org/wp-content/uploads/2019/07/ICED-Ethiopia-land-administration-background-paper.pdf |
| WEB-14 | https://github.com/EthioNLP/Ethiopian-Language-Survey |
| WEB-15 | https://aclanthology.org/2024.lrec-main.561.pdf |
| WEB-16 | https://www.theglobaleconomy.com/Ethiopia/Literacy_rate/ |
| WEB-17 | https://data.worldbank.org/indicator/SE.ADT.LITR.ZS?locations=ET |
| WEB-18 | https://www.aljazeera.com/features/2025/3/10/we-just-want-peace-a-pacifist-community-amid-ethiopias-amhara-conflict |
| WEB-19 | https://bmcnutr.biomedcentral.com/articles/10.1186/s40795-025-01013-5 |
| WEB-20 | https://en.wikipedia.org/wiki/North_Wollo_Zone |
| WEB-21 | https://www.unocha.org/publications/report/ethiopia/ethiopia-situation-report-13-december-2024 |
| WEB-22 | https://arxiv.org/html/2403.19365v1 |
| WEB-23 | https://zenodo.org/records/3734260 |
| WEB-24 | https://link.springer.com/article/10.1007/s43621-023-00161-7 |
| WEB-25 | https://aclanthology.org/2022.wmt-1.41/ |
| WEB-26 | https://www.researchgate.net/publication/358368108_Measuring_Terminology_Consistency_in_Translated_Corpora_Implementation_of_the_Herfindahl-Hirshman_Index |
| WEB-27 | https://aclanthology.org/2025.justnlp-main.3.pdf |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** masakhane/AfriDocMT
**Analysis date:** 2025-07-11
**Examples reviewed:** 61 total (doc_health: 5, doc_health_10: 5, doc_health_25: 5, doc_health_5: 5, doc_tech: 5, doc_tech_10: 5, doc_tech_25: 5, doc_tech_5: 5, health: 5, tech: 6)
**Columns shown:** am, en, ha, sw, yo, zu
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | doc_health, train | 1 | health/WHO | "ሞቃታማ አውሎ ነፋሶችን እንዲሁም ሀይለኛ አውሎ ነፋስ ወይም አውሎ ነፋሶች በመባል የሚታወቁት በጣም አጥፊ የአየር ሁኔታ ክስተቶች ናቸው" | Amharic translation of WHO health content on tropical cyclones — health domain, Ethiopic script | IC, IF |
| D2 | doc_health, train | 2 | health/WHO | "አካል ጉዳተኝነት ሰው የመሆን አካል ነው" | Amharic translation: "Disability is part of being human" — WHO health article | IC |
| D3 | doc_health, train | 3 | health/WHO | "በ 6 ወር አካባቢ የሕፃኑ የኃይል ፍላጎት እና የተመጣጠነ ምግብ አቅርቦት በእናት ጡት ወተት ከሚሰጠው በላይ መጨመር የሚጀምር" | Amharic: infant complementary feeding guidance from WHO — health domain | IC |
| D4 | doc_health, train | 4 | health/WHO | "ፀረ-ተሕዋስያንን መቋቋም(AMR) የሚከሰተው ባክቴሪያ፣ ቫይረሶች፣ ፈንገሶች እና ጥገኛ ተህዋሲያን" | Amharic: antimicrobial resistance — health domain, WHO | IC |
| D5 | doc_health_10, train | 1 | health/WHO | "ይህ የሚያሳየው የደብሊውፒቪ1 ስርጭት ከአፍጋኒስታን (ምስራቅ ክልል) እና ፓኪስታን (ደቡብ ኬፒ) ዞኖች" | Amharic: polio surveillance language, mentions sub-national zones and infection control measures | IC, OO |
| D6 | doc_health_10, train | 3 | health/WHO | "ፋይናንስ ማካተት አሁናዊ ሁኔታዎችን ከሚያስፈልጉ ሰዎች ጋር ፍቃደኛ ከሆኑ" [Financial protection discussion] | Amharic: financial protection policy discourse — health financing domain | IC |
| D7 | doc_tech, train | 1 | tech/Techpoint | "ፔይ ደይ ለመሸጥ ይፈልጋል...ናይጄሪያ ፕሬዚዳንት አዲስ CBN ገዥን ሾሙ" | Amharic: African technology news digest — IT/fintech domain, no agricultural or legal content | IO |
| D8 | doc_tech, train | 2 | tech/Techpoint | "ደቡብ አፍሪካ ጎጂ ይዘቶችን በመስመር ላይ ማቆም ትፈልጋለች...ናላ ከ ዩኬ እና የአውሮፓ ህብረት ለናይጄሪያ ክፍያዎችን ይጀምራል" | Amharic: African fintech and content moderation news | IO |
| D9 | doc_tech, train | 3 | tech/Techpoint | "ኔስት ኮይን (Nestcoin) የሂሳብ መዛግብቱን ለማጠናከር እና የአዲሱን ምርት በኦንቦርድ እድገት" | Amharic: crypto/Web3 fintech startup news | IO |
| D10 | doc_tech, train | 4 | tech/Techpoint | "ኤርቴል ኡጋንዳ ለጃማይካዊው ዘፋኝ 180ሺህ ዶላር ለመክፈል...ቲክቶክ በኬንያ ቢሮ ለመክፈት" | Amharic: telecom copyright law and African tech platform expansion news | IO |
| D11 | health, train | 1 | health/WHO-sentence | "OCV wata hanya ce da ake amfani da ita a ƙari a kan hanyar kula da kwalara" | Hausa sentence-level: oral cholera vaccine health terminology | IC |
| D12 | health, train | 2 | health/WHO-sentence | "ሆኖም የጤና ስርአቶች በዋነኛነት በህዝብ የገቢ ምንጮች ላይ መተማመን ያለባቸው" | Amharic sentence: "health systems need to predominantly rely on public revenue sources" | IC |
| D13 | tech, train | 1 | tech/sentence | "Sahel Capital's SEFAA (Social Enterprise Fund for Agriculture in Africa) Fund" | Tech sentence: agriculture-sector investment fund — only agricultural adjacent content in dataset | IO |
| D14 | tech, train | 6 | tech/sentence | "ፍርድ ቤቱን ጠይቋል" / "He also asked the court to order the telco to pay him royalties" | Amharic sentence: legal/court language in tech context — royalties claim against Safaricom | IO |
| D15 | doc_health_25, train | 2 | health/WHO | "WHA evaluated the unique epidemiological opportunity which exists over the next six months to eradicate the remaining chains of endemic wild poliovirus" | Complex administrative/WHO governance language; multi-sentence Amharic document | OO |
| D16 | doc_health_25, train | 4 | health/WHO | "ገቢ የሆነ የህፃናት አመጋገብ ከልደት ጀምሮ እስከ አዋቂነት ድረስ ለልጁ ዘላቂ ጤና መሰረታዊ ነው" | Amharic: infant nutrition health domain, WHO; long document with cross-sentence references | IC, OO |
| D17 | doc_health_25, train | 5 | health/WHO | "አይኤችአር 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ በ196 አገሮች ላይ በሕግ አስገዳጅ የሆነ የዓለም አቀፍ ሕግ መሣሪያ ነው" | Amharic: International Health Regulations — legally-binding international law framework; closest genre to legal-administrative register in the dataset | IO, OO |
| D18 | doc_health_5, train | 1 | health/WHO | "ከ ቲአርአይፒኤስ ስምምነት ከፀደቀበት ጊዜ አንሥቶ የዓለም የጤና ስብሰባዎች ብዙ ውሳኔዎች" | Amharic: TRIPS agreement, intellectual property law in health sector — international health-law language | IO |
| D19 | doc_tech_25, train | 1 | tech/Techpoint | "ቬንቸር ካፒታሊስቶች(Venture capitalists) የ ኩባንያዎችን ማንነት የሚያገኙት" | Amharic: startup/entrepreneurship discourse — tech sector, no agricultural or cooperative content | IO |
| D20 | doc_tech_10, train | 1 | tech/Techpoint | "The edtech industry in India has exploded in the last few years, making it the world's epicentre." | English: edtech industry news — IT domain, no agricultural domain | IO |
| D21 | health, train | 4 | health/WHO-sentence | "Measures for the prevention of cholera mostly consist of providing clean water and proper sanitation" | English: public health measure description — WHO public health register | IC |
| D22 | doc_health, train | 1 | health/WHO | "ጊዜያዊ የስራ መደብ ወረቀት፡ ለአለም አቀፍ ተጓዦች የኮቪድ-19 ክትባት ማረጋገጫን" | Amharic: interim WHO policy paper — policy document register | OO |
| D23 | doc_health_10, train | 4 | health/WHO | "የጤና ባለሥልጣናት የትንኝ ብዛትን እና የበሽታውን ስርጭት ለመቀነስ ላርቪሳይድ" | Amharic: Zika vector control guidance — specific technical health terminology | IC |
| D24 | doc_health_10, train | 5 | health/WHO | "የጤና አካውንት ሥርዓት 2011 (ጤ/አ/ስ 2011) የጤና ወጪን ለመከታተል" | Amharic: System of Health Accounts — health financing framework document | OO |
| D25 | doc_tech_5, train | 1 | tech/Techpoint | "Remittances are typically transfers between individuals...immigrants send home to support their families" | English: diaspora remittances — fintech/financial inclusion domain | IO |
| D26 | doc_health_25, train | 3 | health/WHO | "እሳተ ገሞራ ፍንዳታዎች አጠቃላይ እይታ፦ እሳተ ገሞራ በምድር ቅርፊት ውስጥ የሚገኝ ክፍተት" | Amharic: volcanic eruptions health risk — WHO emergency preparedness | IC |
| D27 | doc_tech, train | 5 | tech/Techpoint | "ፕሮዳክት ዳይቭ እንዴት ነው የተጀመረው...ወደ ምርት አስተዳደር ጉዞ" | Amharic: long-form interview with tech entrepreneur — informal, personal narrative register | IF |
| D28 | tech, train | 3 | tech/sentence | "In dissecting the social impacts, it becomes vital to delve deep into real-life cases that embody both the positive and negative facets of sports betting in Kenya." | English: sports betting social impacts — not directly relevant to deployment context | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Amharic in Ethiopic Script with Multi-Sentence Document Structure
- **Dimension(s):** IF, IC
- **Observation:** All sampled Amharic content is rendered in Ethiopic (Ge'ez) script throughout all configurations, including full-document (doc_health, doc_tech), pseudo-document (10/25/5-sentence chunks), and sentence-level splits. Amharic script rendering is consistent and coherent across documents of varying length. The benchmark explicitly accommodates Ethiopic script tokenization by increasing token limits for Amharic.
- **Deployment relevance:** The deployment system must handle Amharic in Ethiopic script. The benchmark's demonstrated ability to process, segment, and evaluate multi-sentence Amharic documents in Ethiopic script confirms that the language/script dimension is technically addressed. This directly matches the target output modality.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "የሞቃታማ ዐውሎ ነፋሶች የሞቃታማ ዐውሎ ነፋሶች አጠቃላይ እይታ፡-" — Extended Ethiopic-script Amharic document covering multiple paragraphs; confirms multi-sentence Ethiopic document handling at the doc level.
  - [D3] Example 3 (doc_health, split=train): "ተጨማሪ ምግብ ማጠቃሊያ፡- በ 6 ወር አካባቢ..." — Mid-length WHO health article in Amharic, correctly segmented into numbered recommendations with discourse coherence preserved.

#### Strength 2: Multi-Sentence Discourse Phenomena in Amharic Are Present
- **Dimension(s):** IO, OO
- **Observation:** Several sampled Amharic documents contain multi-clause cross-sentence references, numbered recommendations, and conditional structures (e.g., "ካልተሰጡ ወይም ተገቢ ባልሆነ መንገድ ከተሰጡ" — "if not given or given inappropriately"), which mirror the benchmark's explicit aim to capture coreference resolution and lexical cohesion across sentences.
- **Deployment relevance:** The user acknowledged that document-level structural demands are broadly similar across genres. The benchmark captures cross-sentence dependency structures in Amharic, which the deployment will also need MT systems to handle when translating multi-clause legal and agricultural documents.
- **Datapoint citations:**
  - [D16] Example 4 (doc_health_25, split=train): "ምንም እንኳን በህፃናት መብቶች ስምነቱ መሰረት እያንዳንዱ ጨቅላ እና ህጻን ጥሩ አመጋገብ የማግኘት መብት ቢኖረውም" — Cross-clause conditional referencing: "although every infant… has the right… in many countries less than a fourth…"; demonstrates multi-sentence Amharic coherence across a qualifying clause.
  - [D15] Example 2 (doc_health_25, split=train): "WHA ሕዝቡ ጤና ድንገተኛ አደጋ አለም አቀፍ ስጋት… ሀገራት… አሳስበዋል" — Multi-clause WHO governance language in Amharic preserving cross-sentence referential structure.

#### Strength 3: Multiple Evaluation Configurations Including Document- and Sentence-Level Splits
- **Dimension(s):** IO, OF
- **Observation:** The HF dataset provides ten distinct configurations — sentence-level (health, tech), full-document (doc_health, doc_tech), and pseudo-document chunks (k=5, k=10, k=25) for both domains. All configurations include Amharic. This allows evaluation of MT systems at sentence and sub-document granularities that approximate the chunk sizes relevant for processing bureau documents.
- **Deployment relevance:** Bureau documents in the deployment context may range from short notices to multi-page proclamations. The availability of sentence-level and pseudo-document splits (k=5 through full document) enables evaluation across a range of document lengths comparable to those in the deployment.
- **Datapoint citations:**
  - [D11] Example 1 (health, split=train): "OCV wata hanya ce da ake amfani da ita a ƙari" — Short single-sentence health item; confirms that sentence-level granularity is included for all languages including Amharic.
  - [D5] Example 1 (doc_health_10, split=train): "ይህ የሚያሳየው የደብሊውፒቪ1 ስርጭት ከአፍጋኒስታን (ምስራቅ ክልል)..." — 10-sentence pseudo-document chunk in Amharic; demonstrates the k=10 chunking configuration relevant for medium-length document evaluation.

#### Strength 4: Health Domain Includes Some Policy and Regulatory-Adjacent Register
- **Dimension(s):** IC, OO
- **Observation:** A subset of the WHO health content uses formal policy register features: numbered recommendations ("1. …2. …"), cross-references to proclamation-like frameworks (IHR, TRIPS), and governance vocabulary. The International Health Regulations document (D17) explicitly describes a legally-binding international law instrument with numbered state obligations.
- **Deployment relevance:** This is the closest approximation in the benchmark to the formal administrative register of Ethiopian proclamation documents. While the domain mismatch is severe, the presence of multi-clause numbered obligations, legal vocabulary, and policy cross-references in Amharic provides at least a partial analog to the discourse structure of the deployment genre.
- **Datapoint citations:**
  - [D17] Example 5 (doc_health_25, split=train): "አይኤችአር 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ በ196 አገሮች ላይ በሕግ አስገዳጅ የሆነ የዓለም አቀፍ ሕግ መሣሪያ ነው" — "IHR is an instrument of international law that is legally-binding on 196 countries"; formal legal-regulatory register in Amharic with numbered obligations.
  - [D18] Example 1 (doc_health_5, split=train): "ከ ቲአርአይፒኤስ ስምምነት ከፀደቀበት ጊዜ አንሥቶ የዓለም የጤና ስብሰባዎች ብዙ ውሳኔዎች" — TRIPS Agreement reference; international IP law cross-referenced in health-policy Amharic document.

#### Strength 5: Human-Translated Amharic by Named Native-Speaker Translators
- **Dimension(s):** OC
- **Observation:** The benchmark's four named Amharic translators (Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, Lidetewold Kebede) produced translations under a controlled workflow with quality estimation filtering and terminology workshop preparation. The translation process included human review by a native-speaker language coordinator.
- **Deployment relevance:** The target deployment requires high-quality Amharic translations assessable by native speakers. Benchmark reference translations were produced by human translators (not MT), providing a legitimate upper-bound Amharic quality signal in the health domain, even if domain-mismatched for agriculture/legal.
- **Datapoint citations:**
  - [D2] Example 2 (doc_health, split=train): "አካል ጉዳተኝነት ሰው የመሆን አካል ነው" — "Disability is part of being human"; fluent, naturalistically rendered Amharic sentence consistent with human translation quality.
  - [D4] Example 4 (doc_health, split=train): "ፀረ-ተሕዋስያንን መቋቋም(AMR) የሚከሰተው ባክቴሪያ፣ ቫይረሶች፣ ፈንገሶች" — Technical medical terminology rendered with consistent Amharic neologisms across the document (e.g., "ፀረ-ባክቴሪያ" for antibiotic), demonstrating terminological consistency within the health domain.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Total Domain Absence — No Agricultural, Land-Use, Credit-Scheme, or Cooperative Governance Content
- **Dimension(s):** IO, IC
- **Observation:** All 61 sampled examples draw exclusively from two domains: WHO health news and Techpoint Africa IT news. Not a single example contains agricultural input subsidy notices, land-tenure policy language, credit-scheme terms, cooperative membership governance language, or federal proclamation text. The dataset's vocabulary is drawn entirely from these two domains. In the entire sample, the only "agricultural" item is a single sentence naming a fund with "Agriculture in Africa" in its title (D13), which is a fintech story about an agricultural investment fund — not agricultural document content.
- **Deployment relevance:** The deployment's four target document genres (agricultural input subsidy notices, land-use policy updates, credit-scheme terms, cooperative membership notices) are completely unrepresented. This is not a partial gap — it is a total absence confirmed across all sampled configurations. The benchmark cannot be used as a direct domain-validity test for the deployment. Any performance score on AFRIDOC-MT will not predict MT quality on the deployment's actual document types.
- **Datapoint citations:**
  - [D7] Example 1 (doc_tech, split=train): "ፔይ ደይ ለመሸጥ ይፈልጋል...ናይጄሪያ ፕሬዚዳንት አዲስ CBN ገዥን ሾሙ" — Technology news bulletin: PayDay startup, CBN governor appointment — no agricultural content whatsoever.
  - [D8] Example 2 (doc_tech, split=train): "ናላ ከ ዩኬ እና የአውሮፓ ህብረት ለናይጄሪያ ክፍያዎችን ይጀምራል... ሴሉላንት 20% የሚሆነውን የሰው ኃይል ለማሰናበት" — Fintech remittances and tech layoffs news — no cooperative, land, or subsidy content.
  - [D13] Example 1 (tech, split=train): "Sahel Capital's SEFAA (Social Enterprise Fund for Agriculture in Africa) Fund" — The only "agriculture" mention in the entire sample is the name of an investment fund in a tech news story, not agricultural document content.
  - [D25] Example 1 (doc_tech_5, split=train): "Remittances are typically transfers between individuals…immigrants send home to support their families" — Closest fintech-adjacent item to rural microfinance, but purely in context of diaspora remittances, not ACSI loan agreements or cooperative credit schemes.

#### CRITICAL Concern 2: Source Language Direction Mismatch — Benchmark Translates FROM English; Deployment Translates FROM Amharic
- **Dimension(s):** IC, OC
- **Observation:** Every example in the dataset has an English source document and Amharic as the target translation. The benchmark evaluates English→Amharic MT. The deployment translates FROM Amharic government documents INTO a target language (presumably also Amharic, or possibly from Amharic source texts where the output needs to be evaluated in Amharic). More precisely: the deployment produces Amharic translations of documents that originate in Amharic government-register language — effectively evaluating MT quality in a very different structural direction. Even if the deployment were English→Amharic, the benchmark's English sources (WHO health news, Techpoint Africa IT news) are structurally and lexically distant from Ethiopian federal bureau documents.
- **Deployment relevance:** The benchmark's reference Amharic translations exhibit translationese — unnatural syntax and structural patterns influenced by English source texts. Deployment Amharic documents originate in Amharic proclamation register and have no such English structural bias. A model that performs well on AFRIDOC-MT (English health news → Amharic) may not perform well on the deployment's actual source texts.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "Tropical cyclones, also known as typhoons or hurricanes, are among the most destructive weather phenomena. They are intense circular storms that originate over warm tropical oceans..." — The English source is WHO public health news; the Amharic translation follows English syntactic ordering. Ethiopian proclamation documents are natively authored in Amharic with a distinct formal register.
  - [D17] Example 5 (doc_health_25, split=train): "አይኤችአር 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ በ196 አገሮች ላይ" — IHR article translated from English; even the closest regulatory-register content is a translation FROM English, not native Amharic administrative writing.

#### CRITICAL Concern 3: Complete Absence of Proclamation-Derived Agricultural and Financial Terminology
- **Dimension(s):** IC, OC
- **Observation:** The benchmark contains zero instances of the critical term categories identified by the user: input subsidy scheme names, land-tenure category labels (rist-derived terms, usufruct rights, holding certificates), cooperative membership tier designations from Proclamation 985/2016 (ቀዳሚ የሕብረት ሥራ ማኅበር, የሕብረት ሥራ ማህበራት ዩኒዮን), or MFI credit-scheme terms (ACSI group lending terminology). The Amharic vocabulary in the dataset is drawn from health (disease names, medical procedures, nutrition, epidemiology) and IT (startup names, fintech terms, crypto vocabulary) — entirely non-overlapping with the deployment's operative terminology.
- **Deployment relevance:** For the deployment, translation errors on specific legal terms (e.g., misrendering "ቀዳሚ ሕብረት ሥራ ማኅበር" vs. "ሕብረት ሥራ ማህበር ዩኒዮን") have direct legal and financial consequences for cooperative leaders. The benchmark provides no mechanism to evaluate whether an MT system correctly and consistently renders these terms, since they never appear in the data.
- **Datapoint citations:**
  - [D9] Example 3 (doc_tech, split=train): "ኔስት ኮይን (Nestcoin) የሂሳብ መዛግብቱን ለማጠናከር...ሃሺድ ኢመርጀንት" — Crypto/fintech vocabulary (stablecoin, FTX, pre-seed funding) — zero overlap with cooperative proclamation vocabulary or agricultural subsidy terminology.
  - [D4] Example 4 (doc_health, split=train): "ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ፣ ፀረ-ፈንገስ እና ፀረ-ተባይ መድሃኒቶች" — Medical antimicrobial terminology; no connection to land-tenure or cooperative tier vocabulary.
  - [D11] Example 1 (health, split=train): "OCV wata hanya ce da ake amfani da ita a ƙari a kan hanyar kula da kwalara" — Oral cholera vaccine terminology in Hausa; illustrates the exclusively health-domain vocabulary present at sentence level.

#### MAJOR

#### MAJOR Concern 1: No Rubric Component for Terminological Consistency — The Critical Coherence Requirement for Deployment
- **Dimension(s):** OO
- **Observation:** The benchmark's output scoring framework evaluates fluency (GPT-4o 1-5 scale), content errors (CE), lexical cohesion errors (LE), and grammatical cohesion errors (GE). The lexical cohesion error definition ("issues with vocabulary usage, incorrect or missing synonyms, or overuse of certain words that disrupt the flow") addresses narrative discourse flow, not legal terminological consistency. No rubric component tests whether a specific legal term (e.g., a subsidy scheme name or cooperative tier designation) is rendered identically across all clauses of a document. The data examples confirm this: WHO documents are evaluated for narrative coherence, not for whether "Oral Cholera Vaccine" is always rendered the same way throughout.
- **Deployment relevance:** For the deployment, the key quality requirement is not narrative fluency but terminological stability — that "ቀዳሚ የሕብረት ሥራ ማኅበር" is always rendered identically across 50 clauses of a proclamation. This property is not measured by any metric in AFRIDOC-MT. Even if the deployment were adapted to use AFRIDOC-MT scoring, the scores would not capture the critical coherence dimension.
- **Datapoint citations:**
  - [D16] Example 4 (doc_health_25, split=train): "Ó dara jùlọ... abẹ́rẹ́ àjẹsára... ọmọ ọwọ́" — WHO nutrition document evaluated for fluency and cohesion in Yorùbá; assessment concerns narrative flow of infant feeding guidance, not consistent rendering of defined legal categories.
  - [D22] Example 1 (doc_health_5, split=train): "ጊዜያዊ የስራ መደብ ወረቀት፡ ለአለም አቀፍ ተጓዦች የኮቪድ-19 ክትባት ማረጋገጫን" — Interim WHO position paper; the document mentions specific policy concepts (PHEIC, IHR), but the scoring rubric would assess fluency, not consistent cross-document rendering of "PHEIC" as a defined term.

#### MAJOR Concern 2: Annotator Domain Expertise Absent for Agricultural/Legal Amharic
- **Dimension(s):** OC
- **Observation:** The four named Amharic translators produced reference translations for WHO health news and Techpoint Africa IT news. There is no documentation of their institutional affiliation, agricultural translation experience, or legal Amharic background. The preferred ground-truth authority specified by the user (domain-trained federal bureau translators) is entirely absent. The inter-annotator agreement for Amharic (Krippendorff's alpha = 0.46) is already low for the health domain in which the translators were specifically prepared; performance would likely be lower still in the agricultural-legal domain.
- **Deployment relevance:** Any quality judgment derived from AFRIDOC-MT Amharic reference translations — whether for training, evaluation, or benchmarking — reflects the judgments of translators working in health/IT contexts, not the federal bureau translation standard the user specified. Ground-truth misalignment means that high benchmark scores do not predict acceptability to the user's preferred evaluators.
- **Datapoint citations:**
  - [D3] Example 3 (doc_health, split=train): "ተጨማሪ ምግቦቹ በ 6 ወር ጊዜ ውስጥ ካልተሰጡ ወይም ተገቢ ባልሆነ መንገድ ከተሰጡ" — Amharic health translation requiring WHO pediatric nutrition domain expertise; translator preparation was appropriate for this domain but not for agricultural proclamation register.
  - [D5] Example 1 (doc_health_10, split=train): "የቅርብ ጊዜውን እድገት መቀልበስ ነው. መርሃግብሩ ከፍተኛ ጥራት ያላቸውን ዘመቻዎች" — Polio surveillance Amharic document; complex public health vocabulary produced by health-domain translators, not agricultural domain translators.

#### MAJOR Concern 3: Translationese Risk Compounds Domain Gap — Benchmark Amharic Does Not Reflect Native Administrative Register
- **Dimension(s):** IC
- **Observation:** The benchmark explicitly acknowledges that all Amharic reference translations may exhibit "unnatural syntax or overly literal phrasing" due to English source material. The sampled data confirms this: sentences follow English subordination patterns and clause ordering. Amharic federal proclamation documents use a distinct formal register with specific formulaic phrase structures (cross-article reference formulas, numbered subclause templates) that are natively authored in Amharic and absent from any translated text in the benchmark.
- **Deployment relevance:** MT systems fine-tuned or benchmarked on AFRIDOC-MT Amharic may learn English-influenced Amharic sentence structures. These structures may be legible but could fail to match the formal register expectations of rural cooperative leaders and bureau staff, who associate official documents with specific Amharic administrative phrasing.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "ሞቃታማ አውሎ ነፋሶች፣ እንዲሁም ሀይለኛ አውሎ ነፋስ ወይም አውሎ ነፋሶች በመባል የሚታወቁት" — The Amharic renders "also known as typhoons or hurricanes" as a relative clause; this is a structurally English-influenced subordination pattern. Native Amharic administrative documents would likely employ a different grammatical structure.
  - [D27] Example 5 (doc_tech, split=train): "ቶቢ ከ ቴክ ፖይንት አፍሪካ ጋር ያደረጉት ቃለ ምልልስ" — Interview-register Amharic (tech domain): informal, conversational sentence structures that differ markedly from proclamation-register Amharic. Illustrates that even within the dataset, register variation exists that does not approach legal-administrative Amharic.

#### MINOR

#### MINOR Concern 1: Technology Domain Contains Some Legally Adjacent Content but Not Applicable to Deployment
- **Dimension(s):** IO
- **Observation:** Several tech domain documents contain legal or quasi-legal language: copyright infringement claims (D14), telecom regulatory decisions, and securities/investment disclosures. However, this legal language concerns corporate IP law, telecommunications regulation, and fintech compliance — entirely different from Ethiopian agricultural proclamation law, cooperative registration, and land-tenure regulation.
- **Deployment relevance:** These items might superficially appear to close the legal-register gap, but the specific legal vocabulary (royalties, capital markets, exchange rate unification) has no relevance to cooperative proclamations or subsidy scheme terms. The domain-register mismatch persists.
- **Datapoint citations:**
  - [D14] Example 6 (tech, split=train): "ፍርድ ቤቱን ጠይቋል" / "He also asked the court to order the telco to pay him royalties and licensing fees" — Amharic legal vocabulary in a copyright/IP context; not applicable to cooperative membership or land-tenure law.
  - [D10] Example 4 (doc_tech, split=train): "ኤርቴል ኡጋንዳ ለጃማይካዊው ዘፋኝ 180ሺህ ዶላር ለመክፈል... ፍርድ ቤቱ ተከሳሾቹን በቅጂ መብት ጥሰት" — Copyright infringement court ruling in Uganda; Amharic legal vocabulary but in IP/copyright register, not agricultural proclamation register.

#### MINOR Concern 2: Sports Betting and Some Tech Content Irrelevant to Any Deployment Need
- **Dimension(s):** IO
- **Observation:** Two examples in the tech dataset concern sports betting social impacts in Kenya (D28) and extended personal interviews about tech entrepreneurship. These are not only irrelevant to the agricultural deployment but represent the least formal, most conversational Amharic register in the dataset.
- **Deployment relevance:** Minor — these items do not affect the overall domain analysis, but they do further dilute the relevance of the tech domain for any purpose related to the deployment.
- **Datapoint citations:**
  - [D28] Example 3 (tech, split=train): "In dissecting the social impacts, it becomes vital to delve deep into real-life cases that embody both the positive and negative facets of sports betting in Kenya." — Sports betting commentary; no deployment relevance.
  - [D27] Example 5 (doc_tech, split=train): "ቶቢ...ስለ አስተዳደሯ፣ ስለ እምነቷ፣ የምርት ሥራ አስኪያጅ ለመሆን ስላላት መንገድ" — Extended personal interview on tech entrepreneurship; informal, narrative register; no deployment relevance.

---

### Content Coverage Summary

The dataset contains exclusively two content domains confirmed by direct examination: (1) WHO global health news covering topics including tropical cyclones, disability, antimicrobial resistance, complementary feeding, cholera, polio vaccination, COVID-19 policy, and International Health Regulations; and (2) African technology news from Techpoint Africa covering fintech startups, crypto/Web3, African tech ecosystem, mobile money, edtech, and agritech investment (but not agritech content — only investment news about agritech companies).

The Amharic translations are extensive, fluent, and technically handled in Ethiopic script throughout. Document-level examples average 30-37 sentences in length. The health domain employs formal WHO institutional register; the tech domain employs informal news-digest and interview register. The closest approximation to regulatory/legal language in the entire dataset is the International Health Regulations article (legally-binding international law framework) and TRIPS Agreement references — both translated from English and neither approaching Ethiopian agricultural proclamation vocabulary.

The dataset contains zero instances of: Ethiopian government document vocabulary, cooperative membership terminology, land-tenure language, agricultural subsidy scheme names, microfinance loan terms, or Amhara regional administrative vocabulary. The source-language direction is English→Amharic throughout; no Amharic-originating documents are present.

---

### Limitations

1. **Sample size within configurations**: 5-6 examples per configuration were reviewed. With 240-334 training documents per domain, unseen examples might include edge cases. However, given that sources are exclusively WHO.int and Techpoint Africa, additional samples cannot change the domain finding.

2. **Translator background unverifiable**: Web searches for the four named Amharic translators returned no results. It is possible but undocumented that any translator has agricultural or legal Amharic expertise. This cannot be confirmed or excluded from the data alone.

3. **Register quality assessment limited**: Evaluating whether the Amharic translations exhibit procurement-register appropriateness requires native-speaker expert judgment from someone familiar with Ethiopian bureau Amharic. The current analysis can identify structural patterns (clause ordering, subordination) but cannot definitively characterize the full register distance.

4. **Evaluation metric properties not directly observable**: The scoring behavior of d-chrF, d-BLEU, and GPT-4o on out-of-domain text (i.e., agricultural proclamation language) cannot be assessed from the dataset content alone; this would require running evaluation experiments with deployment-domain text.

5. **Amhara sub-regional dialect features**: Whether the Amharic translations reflect Addis Ababa standard or Amhara regional administrative variety cannot be determined from the data. No dialect-distinguishing features are observable in health/IT domain text.

