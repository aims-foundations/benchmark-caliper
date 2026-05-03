## Deployment Context

**Use case:** Translating clinical practice guidelines, vaccination schedules, and maternal-health booklets into Amharic for ministry-of-health distribution
**Target population:** Health workers and patients across Ethiopian regional health bureaus producing and consuming Amharic-language material

# Validity Analysis: afridoc_mt
**Target context:** Ethiopia Ministry of Health — Amharic Clinical Translation Deployment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology | 3 | Moderate gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 4 | Minor gaps | high |
| **Average** | **2.8** | | |

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

AFRIDOC-MT is a thoughtfully constructed ground-up document-level MT benchmark covering Amharic, with strong form match to the Ethiopia MOH deployment (text-only Amharic in Ethiopic script, document-level structure preserved, chrF prioritized for morphological richness, multi-parallel evaluation). However, three of four high-priority dimensions for this deployment have material gaps. Input Content (HIGH priority): the benchmark's WHO-sourced corpus contains substantial geographically remote and Ethiopia-irrelevant content (Afghanistan polio, CCHF, volcanoes, TRIPS), no Ethiopia-specific endemic-disease, calendar, or referral-pathway material, and visible translationese patterns. Output Ontology (HIGH priority): the deployment's primary success criterion — MOH/EFDA glossary compliance — is not operationalized by any benchmark scoring function, and document-level term-consistency is only partially captured. Output Content (HIGH priority): the four named Amharic translators have no documented MOH credentials, clinical backgrounds, or regional affiliations; Krippendorff's α=0.46 for Amharic is the lowest of the five languages; GPT-4o-as-judge is explicitly unreliable for Amharic. The maternal-health and immunization subset of the corpus does provide direct deployment-relevant content [DATASET-D4, D42, D44], and the benchmark's honest documentation of its own limitations (translationese, GPT-4o judge inconsistency, missing document-level QE for Amharic) is itself a significant strength.

## Practical Guidance

### What This Benchmark Measures

AFRIDOC-MT can validly measure (a) general document-level English→Amharic MT fluency and faithfulness on WHO-style health prose using d-chrF/d-BLEU [Q51, Q53], (b) relative model ranking among encoder-decoder NMT and decoder-only LLMs for Amharic [Q4, Q58], and (c) sentence-level vs. pseudo-document tradeoffs revealing that pseudo-document chunking can degrade African-language quality [Q61, Q72]. The benchmark provides a credible signal for whether a system can produce reasonably fluent, faithful Amharic translation of WHO-register health prose at document level.

### Construct Depth

Construct depth is shallow for the deployment's primary criteria. Faithfulness and surface fluency are reasonably well covered through d-chrF, human DA, and CE/fluency dimensions [Q183, Q195]. Document-level discourse phenomena are partially probed via lexical and grammatical cohesion error categories [Q189, Q190], though GPT-4o reliability for these is poor in Amharic [Q99, Q219]. The benchmark does NOT probe institutional terminology compliance, clinical-accuracy validation by MOH-credentialed reviewers, regional Amharic register acceptance, or readability for semi-literate patients — all of which are central to deployment success.

### What Else You Need

Five concrete supplements are needed: (1) MOH/EFDA glossary-conformance scoring against the Academy of Ethiopian Languages Amharic Medical Dictionary [WEB-8] and any EFDA list — addresses OO gap; (2) parallel reference translations or post-editing by MOH-credentialed clinical translators on a held-out Ethiopia MOH-distributed sample — addresses OC gap; (3) Ethiopia-specific extension corpus covering endemic diseases (malaria, TB, kala-azar, trachoma), Ethiopian calendar dates, and tiered-referral language — addresses IC gap; (4) regional bureau acceptance review with stakeholders from Tigray, Oromia, Somali, Amhara bureaus on register acceptability — addresses OC regional-register gap; (5) readability evaluation with a sample of semi-literate patients or HEW-mediated comprehension testing — addresses OO readability calibration gap.

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
AFRIDOC-MT is a ground-up document-level MT benchmark designed for African languages including Amharic, with a health domain category that aligns with the deployment's prose-narrative scope [Q1, Q2, Q15]. The user has explicitly scoped structured document types (tables, timetables, forms) as out-of-scope, which mitigates the most obvious category gap. However, the benchmark mixes a tech-news category (Techpoint Africa) [Q18, Q22] that introduces construct-irrelevant variance for clinical deployments, and within the health category a substantial portion of sampled documents covers topics geographically or substantively distant from Ethiopian MOH clinical priorities (Afghanistan polio, CCHF, volcanoes, Zika, TRIPS policy) [DATASET-D7, D32, D33, D34, D26, D46]. Multi-way translation across 30 directions is supported but the deployment uses only en→am [Q7, Q94, Q101]. Net: the taxonomy partially aligns — document-level MT for Amharic prose health is covered, but the benchmark's category structure does not isolate clinical-guideline / maternal-health / vaccination subgenres that the deployment actually translates.

**Strengths:**
- Ground-up design for African languages including Amharic with document-level MT as a distinct construct from sentence-level MT [Q1, Q15, Q16]
- Health domain category is present and operationalized at document level — the closest existing category match for the deployment [Q2, Q14, DATASET-D4, D15, D42]
- Deployment scope (prose health) aligns with the benchmark's narrative-prose-only corpus structure [Q18, DATASET-D1, D3]

**Checklist:**

- **IO-1**: Required categories for this deployment are clinical practice guidelines (narrative), maternal-health booklets, and vaccination schedule narratives — all prose. Benchmark provides a 'health' category from WHO articles that partially covers these subgenres [Q2, Q18, DATASET-D4, D9, D42]. — _Sources: Q2, Q18, DATASET-D4, DATASET-D9, DATASET-D42_
- **IO-2**: The benchmark does not subdivide health into clinical-guideline / maternal-health / immunization-schedule / endemic-disease subcategories. Ethiopia-specific subgenres (e.g., MOH referral pathways, endemic-disease guidance) are absent — only TICO-19 is mentioned as a comparable health document-level resource and is COVID-restricted [Q14]. The deployment-relevant maternal-child / immunization subset is present but constitutes a minority of sampled health documents [DATASET-D4, D15, D42, D31, D44]. — _Sources: Q14, WEB-10, DATASET-D4, DATASET-D15, DATASET-D42_
- **IO-3**: The benchmark includes a tech-news category (Techpoint Africa, 271 documents) that is irrelevant to clinical translation deployment [Q2, Q18, DATASET-D13, D14, D22, D38, D39]. Within health, a substantial share of sampled WHO documents covers globally generic or non-Ethiopian-relevant topics (Afghanistan polio, CCHF, volcanoes, TRIPS, IHR, Zika) [DATASET-D7, D32, D33, D34, D46, D26]. — _Sources: Q2, Q18, DATASET-D13, DATASET-D14, DATASET-D22, DATASET-D33, DATASET-D7_
- **IO-4**: Two category-level issues harm content validity: (a) inclusion of irrelevant tech-domain category that dilutes any aggregate score [DATASET-D14, D22], and (b) absence of fine-grained clinical-guideline / maternal-health / endemic-disease subcategorization within the health domain, meaning a system can score well on aggregate health while underperforming on the deployment-specific subgenres [DATASET-D7, D33]. — _Sources: DATASET-D14, DATASET-D22, DATASET-D33, DATASET-D7_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'This paper introduces AFRIDOC-MT, a document-level multi-parallel translation dataset covering English and five African languages: Amharic, Hausa, Swahili, Yorùbá, and Zulu.' (p.1)
- [Q2] 'The dataset comprises 334 health and 271 information technology news documents, all human-translated from English to these languages.' (p.1)
- [Q14] 'To the best of our knowledge, only TICO-19, a health domain translation benchmark, has the potential to be used for document-level MT, while it is restricted to topics related to COVID-19.' (p.2)
- [Q15] 'Document-level NMT aims to overcome the limitations of sentence-level systems by translating an entire document as a whole.' (p.2)
- [Q18] 'We scraped English articles from the websites of Techpoint Africa and the World Health Organization (WHO).' (p.3)
- [Q93] 'Africa is home to thousands of indigenous languages... we focused on just five languages.' (p.10)
- [Q94] 'AFRIDOC-MT is a multi-way parallel dataset. However, due to the cost of running inference over three prompts and across all 30 translation directions for all the models evaluated, most of our analysis is limited to translation tasks between English and the five African languages.' (p.10)

*Web sources:*
- [WEB-10] JMIR 2025 scoping review found only 3 Amharic studies of 54 NLP-for-public-health works, confirming sparse subgenre coverage in available benchmarks

*Dataset analysis:*
- DATASET-D4: Amharic complementary feeding article — direct match to maternal-health booklet subgenre
- DATASET-D14: Amharic Techpoint article on Cellulant/NALA — tech-domain content irrelevant to clinical deployment
- DATASET-D33: WHO volcano article — health category but irrelevant to Ethiopian clinical materials
- DATASET-D7: Afghanistan polio campaign article in Amharic — geographically remote from Ethiopia
- DATASET-D42: WHO breastfeeding recommendation in Amharic — high subgenre alignment with maternal-health booklet

</details>

**Information gaps:**
- Proportion of WHO health documents that are clinical-guideline / maternal-health / immunization vs. policy / financing / non-Ethiopian-endemic — not quantified beyond 51-document sample
- Whether vaccination schedule narrative (a deployment subgenre) is meaningfully present in the 334-document health corpus

**Requires expert verification:**
- Whether the AFRIDOC-MT health subgenre distribution adequately represents the document types Ethiopia MOH actually distributes (requires comparison with MOH document inventory)

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark's source content is generic English WHO articles, not Ethiopia-specific clinical material. The user accepts generic coverage as sufficient for current scope, but the deployment serves a context with Ethiopia-specific endemic conditions (kala-azar, trachoma, malaria), the Ethiopian calendar, and tiered referral pathways — all explicitly absent [Q103, Q105]. Dataset analysis confirms a substantial share of sampled health documents cover topics geographically/contextually remote from Ethiopia [DATASET-D7, D32, D33, D34, D26]. The benchmark itself flags translationese risk — translated Amharic sentences may exhibit unnatural syntax, overly literal phrasing, and English-centric structural and cultural framing [Q103, Q104, Q105], and dataset inspection confirms visible English-loanword and parenthetical-acronym patterns in Amharic [DATASET-D43, D47]. With IC marked HIGH priority by the user, these gaps drive a score of 2: significant construct-irrelevant variance from non-Ethiopian topics combined with Ethiopia-specific construct underrepresentation.

**Strengths:**
- WHO-sourced register matches the institutional voice of MOH-distributed health communication materials [Q18, DATASET-D11, D41]
- Maternal-child health and immunization subset (complementary feeding, breastfeeding, vaccination) is directly aligned with deployment document types [DATASET-D4, D15, D42, D44]
- Authors document data-selection ethics with attention to bias minimization and harmful-content screening [Q106, Q107]

**Checklist:**

- **IC-1**: The deployment requires Ethiopia-specific knowledge: endemic diseases (malaria, TB, kala-azar, trachoma), Ethiopian calendar dates, MOH referral pathways, regional health bureau structures. None of these is represented in the benchmark — sampled documents include Afghanistan polio, CCHF, Zika, and volcanoes, none Ethiopia-endemic [DATASET-D7, D32, D26, D33]. Web search confirmed no NLP study has evaluated Amharic MT on Ethiopia-endemic disease terminology [WEB-10]. — _Sources: WEB-10, DATASET-D7, DATASET-D32, DATASET-D26, DATASET-D33_
- **IC-2**: Source documents are publicly available WHO and Techpoint articles described as ethically sourced and screened for harmful content [Q34, Q106, Q107]. Cultural alignment with Ethiopia is partial: WHO health register is broadly compatible, but Ethiopian cultural context (religious diversity, household decision-making, Ethiopian Orthodox / Muslim practices around maternal health) is not specifically reflected. — _Sources: Q34, Q106, Q107_
- **IC-3**: The benchmark explicitly acknowledges potential bias toward English in structure, semantics, and cultural framing [Q105]. Dataset inspection shows English-centric patterns: parenthetical English acronyms (AMR, CCHF), English loanwords ('superbugs'), and direct transliterations of drug names (ribavirin) embedded in Amharic [DATASET-D43, D5, D6, D47]. The tech-domain content is entirely Western/Nigerian/Indian and irrelevant [DATASET-D14, D22, D38]. — _Sources: Q105, DATASET-D43, DATASET-D47, DATASET-D14, DATASET-D22_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the benchmark does not document recruitment of Ethiopian MOH clinical reviewers to vet content for Ethiopian relevance. Translators are named but no review of source-content cultural fit is described. Would need MOH expert review of the 334 health documents against Ethiopia MOH distribution material to confirm content alignment.
- **IC-5**: Two main content-validity harms: (1) construct underrepresentation — Ethiopia-specific clinical content (endemic diseases, calendar, referral pathways) is absent [WEB-10]; (2) construct-irrelevant variance — non-Ethiopian-relevant topics (Afghanistan polio, volcanoes, CCHF) dilute the evaluation signal [DATASET-D7, D32, D33], and translationese effects may produce English-shaped Amharic that scores well against references but reads unnaturally [Q103, DATASET-D43]. — _Sources: Q103, Q105, WEB-10, DATASET-D43, DATASET-D7, DATASET-D33_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q18] 'We scraped English articles from the websites of Techpoint Africa and the World Health Organization (WHO).' (p.3)
- [Q103] 'A potential limitation of our dataset is the influence of translationese... translated sentences in African languages may exhibit patterns such as unnatural syntax or overly literal phrasing.' (p.10)
- [Q104] 'Although we have not conducted an analysis to quantify these effects, prior work suggests that they can affect MT model performance, generalization and evaluation including direct assessment.' (p.10)
- [Q105] 'AFRIDOC-MT may reflect a bias toward English in terms of structure, semantics, and cultural framing.' (p.10)
- [Q106] 'The data sources were selected to represent different cultural perspectives, with a focus on minimizing any potential bias.' (p.10)
- [Q107] 'Efforts were made to ensure the dataset does not include harmful, biased, or offensive content via manual inspection.' (p.10)

*Web sources:*
- [WEB-10] JMIR 2025 scoping review identified only 3 Amharic NLP-for-public-health studies; none evaluated Ethiopia-endemic disease terminology

*Dataset analysis:*
- DATASET-D7: Amharic article on Afghanistan polio campaign — geographically irrelevant to Ethiopia
- DATASET-D32: CCHF article — disease not a primary Ethiopian clinical priority
- DATASET-D33: Volcano article — irrelevant to Ethiopian MOH clinical materials
- DATASET-D43: Amharic AMR article with English loanword 'superbugs' in parentheses — translationese pattern
- DATASET-D47: Amharic CCHF article retaining 'ribavirin' transliterated — drug-name handling unverifiable against EFDA terminology
- DATASET-D4: Amharic complementary feeding article — high deployment relevance
- DATASET-D42: Amharic breastfeeding WHO recommendation — direct match to maternal-health booklet
- DATASET-D14: Amharic tech article (NALA, Cellulant) — entirely irrelevant

</details>

**Information gaps:**
- Quantitative breakdown of how many of the 334 health documents are deployment-relevant (maternal-health / vaccination / clinical-guideline) vs. policy/financing/non-Ethiopian-endemic
- Whether the AFRIDOC-MT 'terminology harmonization' step (Q121) was actually completed and what reference materials were used
- Whether translationese effects in Amharic are systematic enough to bias automated metric scores against systems producing more natural Amharic

**Requires expert verification:**
- MOH clinical-translator review of a sample of AFRIDOC-MT Amharic translations against MOH-distributed materials to assess register alignment
- Comparison of WHO source-document language against actual Ethiopian MOH maternal-health booklets and clinical practice guidelines

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Both benchmark and deployment are text-only Amharic in Ethiopic/Ge'ez script; this is a strong form match. The benchmark explicitly handles Amharic's high token counts due to non-Latin script and increased the Amharic token limit during evaluation [Q47, Q127, Q128, Q161, Q162]. Document-level structure is preserved with NLTK + linguist sentence segmentation [Q19–Q21] and pseudo-document chunking (k=10) [Q48, Q49] to fit model context limits. Dataset inspection confirms full Ethiopic-script Amharic documents are present with multi-paragraph structure [DATASET-D1, D3]. Minor concerns: full-document translation is infeasible for most open LLMs given 8,192-token context [Q88, Q89], imposing a structural ceiling; the benchmark uses CSV with paragraph separator conventions [Q118, Q119, Q122] which may differ from MOH document formats. With IF marked LOWER priority by the user (no modality/script mismatch), these concerns do not warrant a lower score.

**Strengths:**
- Amharic in Ethiopic/Ge'ez script is natively present and structurally accommodated, including increased token limits to handle Amharic's high token counts [Q127, Q128, Q162]
- Document-level structure is preserved with linguist-verified sentence segmentation [Q20, Q21]
- Pseudo-document chunking enables evaluation under realistic context-length constraints [Q48, Q49, DATASET-D1]
- Multi-parallel structure provides English↔Amharic source-target rows directly usable for the deployment direction [DATASET-D12]

**Checklist:**

- **IF-1**: Signal distribution matches: text in Ethiopic script for Amharic. The benchmark documents that Amharic and Yorùbá produce the largest tokenizer counts and adjusted the Amharic token limit accordingly [Q127, Q161, Q162]. Dataset inspection confirms full Ethiopic-script multi-paragraph Amharic [DATASET-D1, D3, D5]. — _Sources: Q127, Q161, Q162, DATASET-D1, DATASET-D3_
- **IF-2**: MOH/Addis Ababa-side infrastructure can support Unicode Ethiopic-script processing; deployment is text-only with print and digital distribution [deployment context]. End-user connectivity (19.4% internet penetration nationally [WEB-11]) is relevant for distribution but not for the MT system's input form. — _Sources: WEB-11_
- **IF-3**: Document-level format with paragraph preservation is supported via CSV with double-empty-row paragraph separators [Q118, Q119, Q122]. However, MOH distribution materials may use formats (Word, PDF, print-ready layouts) requiring additional conversion. The benchmark's full-document translation is infeasible for most open LLMs (8,192-token ceiling) [Q88, Q89], constraining how the system handles longer MOH documents — a real but moderate constraint. — _Sources: Q118, Q119, Q122, Q88, Q89_
- **IF-4**: Minor form mismatches: (1) full-document translation infeasibility for most LLMs forces pseudo-document chunking, which the benchmark itself shows can degrade African-language translation quality vs. sentence-level [Q61, Q72]; (2) CSV-with-paragraph-separator input format differs from typical MOH document formats but is a reasonable proxy for document-level structure. — _Sources: Q61, Q72, Q88, Q89_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q19] 'While our corpus is initially structured at the article level, we aim to make it suitable for sentence-level translation tasks as well.' (p.3)
- [Q20] 'we segmented the raw articles into sentences using NLTK' (p.3)
- [Q21] 'we recruited a linguist and a professional translator to verify the correctness of the segmentation' (p.3)
- [Q47] 'some models were unable to process entire documents due to input length limits, which were exceeded by token counts in some languages (Amharic and Yorùbá).' (p.5)
- [Q88] 'Except for LLama3.1, all other open LLMs have a context length of 8192 tokens' (p.9)
- [Q89] 'This makes it difficult to use the context length beyond a certain limit, making full document translation infeasible.' (p.9)
- [Q127] 'Amharic and Yorùbá—languages with unique characteristics such as non-Latin scripts and diacritics, respectively—had the largest average token counts across the tokenizers.' (p.19)
- [Q162] 'Therefore, we increased the token limit specifically for Amharic.' (p.21)

*Web sources:*
- [WEB-11] Ethiopia internet penetration ~19.4% in early 2024 — affects distribution channel but not MT system input form

*Dataset analysis:*
- DATASET-D1: Full multi-paragraph Amharic WHO document in Ethiopic script with numbers, medical terms, and paragraph structure preserved
- DATASET-D3: Multi-paragraph Amharic disability article — confirms document-level structure
- DATASET-D12: Multi-language parallel row including Amharic — confirms en→am evaluation direction is supported

</details>

**Information gaps:**
- Whether actual MOH source documents fit within the benchmark's pseudo-document (k=10) chunking assumption or routinely exceed it

**Requires expert verification:**
- Confirmation that MOH document formats (Word/PDF/print) can be losslessly converted to the benchmark's text-with-paragraph-separator representation

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark's output ontology operationalizes translation quality via d-BLEU, d-chrF, GPT-4o-as-judge with four explicit quality dimensions (fluency, content errors, lexical cohesion errors, grammatical cohesion errors) [Q179, Q180, Q183, Q184, Q189, Q190], and human DA on 0–100 scale [Q195, Q196]. The deployment's primary success criterion — MOH/EFDA glossary compliance — is not operationalized by any benchmark scoring function: d-BLEU/d-chrF and human DA reward similarity to the AFRIDOC-MT references and are agnostic to institutional terminology lists, and the planned terminology harmonization step (Q121) is not documented as completed. Document-level terminological consistency is partially captured by the lexical cohesion (LE) error category in GPT-4o-as-judge [Q189], but GPT-4o-as-judge is documented as unreliable for Amharic [Q99, Q218, Q219]. Faithfulness (CE) and readability (fluency) are reasonably covered. With OO marked HIGH priority by the user and glossary compliance the deployment's primary criterion, the score is 2: the benchmark's decision rules systematically misrepresent the deployment's central success criterion.

**Strengths:**
- Faithfulness to source meaning is well operationalized via content errors (CE) in GPT-4o-as-judge and human DA [Q183, Q184]
- Cohesion errors taxonomy (lexical and grammatical) explicitly recognizes document-level discourse phenomena [Q187, Q188, Q189, Q190]
- chrF prioritized over BLEU because it captures Amharic morphological richness — a sound choice for the target language [Q53]
- Multiple complementary scoring streams (lexical, neural, GPT-4o judge, human DA, qualitative) provide breadth [Q83, Q98]

**Checklist:**

- **OO-1**: Output categories are continuous/count metrics (d-BLEU, d-chrF, fluency 1–5, CE/LE/GE counts, DA 0–100) [Q180, Q191]. Regional relevance is partial: faithfulness and fluency are universally relevant; cohesion errors capture some terminological consistency; glossary compliance is absent. — _Sources: Q180, Q183, Q189, Q190, Q191_
- **OO-2**: Missing categories specific to the deployment: (a) MOH/EFDA glossary-compliance score — primary deployment success criterion is unoperationalized; (b) document-level term-consistency score that explicitly checks whether the same source term is rendered identically (LE captures vocabulary errors but not term-by-term institutional consistency); (c) readability calibrated for semi-literate patients — fluency 1–5 is not population-calibrated [DATASET CRITICAL Concern 2]; (d) Ethiopia-specific terminology coverage (endemic diseases, calendar, referral pathways). — _Sources: Q121, WEB-8, WEB-9, DATASET-D5, DATASET-D43_
- **OO-3**: The cohesion-error dimensions are operationalized via GPT-4o prompts that compare model output to reference translation [Q185, Q186] — implicitly encoding the AFRIDOC-MT translators' choices as the standard, which may not align with MOH/EFDA approved terminology [DATASET-D5, D43, D47]. Fluency rated by GPT-4o without a reference [Q181] embeds whatever Amharic register GPT-4o has internalized, which may differ from Ethiopian clinical Amharic. — _Sources: Q185, Q186, Q181, DATASET-D43, DATASET-D47_
- **OO-4**: Stakeholder-driven taxonomy redesign would be high value: adding (a) glossary-conformance scoring against MOH/EFDA term lists, (b) explicit term-consistency tracking, (c) MOH-translator-judged faithfulness, and (d) readability for semi-literate audiences would address the most consequential OO gaps. The Academy of Ethiopian Languages Amharic Medical Dictionary [WEB-8] and a multilingual glossary [WEB-9] exist but are not integrated. — _Sources: WEB-8, WEB-9_
- **OO-5**: Structural validity is moderately compromised because the central deployment construct (institutional terminology compliance) is not represented in the scoring functions [DATASET CRITICAL Concern 2]. Content validity is also harmed by missing categories. External validity is at risk: high benchmark scores would not necessarily predict MOH-acceptable outputs. — _Sources: Q121, DATASET-D43_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q121] 'We will provide a list of extracted terminologies soon so that you can harmonize how terminologies are translated.' (p.18)
- [Q179] 'We compared translations performed at the sentence-level and pseudo-document level in terms of fluency, content errors, and cohesion errors—specifically lexical (LE) and grammatical (GE) errors—using the same definitions as Sun et al. (2025).' (p.22)
- [Q180] 'GPT-4o is prompted to rate the fluency of a document on a scale from 1 to 5' (p.22)
- [Q183] 'GPT-4 is prompted to identify and list the mistakes, such as incorrect translations, omissions, additions, and any other errors' (p.22)
- [Q189] 'Lexical Cohesion Mistakes: Issues with vocabulary usage, incorrect or missing synonyms, or overuse of certain words that disrupt the flow.' (p.23)
- [Q190] 'Grammatical Cohesion Mistakes: Problems with pronouns, conjunctions, or grammatical structures that link sentences and clauses.' (p.23)
- [Q191] 'Fluency can only have values between 1 and 5. However, the other metrics, including CE, GE, and LE, do not have a specific range and can take on any value because they are counts.' (p.24)
- [Q53] 'chrF better captures the morphological richness of African languages' (p.5)

*Web sources:*
- [WEB-8] Amharic Dictionary of Medical Terms (Academy of Ethiopian Languages, UN-sponsored) exists but is not integrated into AFRIDOC-MT scoring
- [WEB-9] Multilingual English-Amharic-Oromiffa-Somali-Afar health glossary exists on Scribd but is not integrated

*Dataset analysis:*
- DATASET-D5: 'ፀረ-ተሕዋስያንን መቋቋም(AMR)' — AMR rendered with parenthetical English; conformance to any MOH/EFDA term list is unverifiable
- DATASET-D43: 'ሱፐርበግስ(superbugs)' — translator choice that may not match MOH-approved terminology; benchmark scoring cannot detect this gap
- DATASET-D47: 'ribavirin' transliterated in Amharic — drug-name handling unverifiable against EFDA pharmaceutical terminology

</details>

**Information gaps:**
- Whether the AFRIDOC-MT planned terminology harmonization step [Q121] was completed and what reference list was used
- Whether MOH-distributed terminology in Amharic clinical guidelines is actually formalized as a single canonical list, or whether multiple competing references exist

**Requires expert verification:**
- MOH/EFDA confirmation of which Amharic glossary is the authoritative compliance reference
- Whether AFRIDOC-MT Amharic translators followed any institutional glossary during translation

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Output content (the reference translations and human evaluation labels themselves) raises the most consequential validity concerns. The four named Amharic translators [Q109] are recruited via a language coordinator [Q23, Q24] and attended a domain workshop with short translation guidelines [Q26], but the benchmark documents no MOH credentials, clinical backgrounds, EFDA training, or institutional affiliations — the deployment explicitly designates MOH-trained clinical translators as primary ground-truth authority and Amharic-speaking physicians as fallback. Web search did not find public credentials for these translators or a public MOH clinical translation certification registry [WEB-3 register variation; benchmark_validity_gaps_summary annotator_credentials NOT FOUND]. Inter-annotator agreement for Amharic human DA is α=0.46 [Q211, Q71], the lowest of the five languages, indicating noisy reference quality signal even within the benchmark's own framework. The translators' regional affiliation is undocumented, leaving regional Amharic register variation across Tigray/Oromia/Somali bureaus unaddressed. With OC marked HIGH priority and the user explicitly excluding general translators and academic linguists from authoritative status, the alignment is poor — score 2.

**Strengths:**
- Four expert translators per language with a workshop on domain-specific terminology and short translation guidelines [Q23, Q26]
- Use of MT engines was prohibited and quality assurance described as capable of detection [Q120]
- AfriCOMET-based QE with manual review threshold (0.65) added a layer of automated quality control [Q27, Q28, Q29]
- Translators paid at clearly disclosed rates ($1,250 per 2,500 sentences, $55.15 per 80 documents for evaluators) — transparent compensation [Q31, Q198]
- Dataset analysis confirms specialized clinical terminology is rendered in Ethiopic script across complex topics [DATASET-D5, D43, D47]

**Checklist:**

- **OC-1**: Ground-truth labels (reference translations and human DA scores) likely do NOT reflect the deployment's authoritative regional stakeholder population. The user designates MOH-trained clinical translators as primary and Amharic-speaking physicians as fallback ground-truth; the benchmark documents neither MOH credentials nor clinical/medical backgrounds for the four named Amharic translators [Q109]. No regional bureau affiliation is documented [register_variation web search NOT FOUND]. — _Sources: Q23, Q24, Q109_
- **OC-2**: Substantial disagreement potential between AFRIDOC-MT translators and MOH-credentialed clinical translators is plausible: the benchmark's translators may have used different terminology choices for AMR, drug names, infant feeding terms than MOH/EFDA standards prescribe [DATASET-D5, D43, D47, D44]. The α=0.46 Amharic agreement [Q211] further indicates that even the benchmark's own annotation pool produced noisy quality judgments — the lowest among five languages. — _Sources: Q211, DATASET-D43, DATASET-D47, DATASET-D44, DATASET-D5_
- **OC-3**: Annotator demographics in the benchmark are minimally documented: names of four translators per language [Q109], recruited through a 'language coordinator who is also a native speaker' [Q24]. No professional credentials, institutional affiliations, regions, ages, or clinical backgrounds are disclosed. No formal datasheet/data statement detailing demographics is provided. This is a clear documentation gap relative to standard practice. — _Sources: Q23, Q24, Q26, Q109_
- **OC-4**: Re-annotation by an MOH-credentialed clinical translator pool would be high-value: producing parallel reference translations or post-editing AFRIDOC-MT references to MOH/EFDA standards would yield a deployment-aligned reference set. Rough cost estimate scales from disclosed per-sentence rates [Q31]. — _Sources: Q31, WEB-8_
- **OC-5**: Aggregation methods: the benchmark uses single reference translations per row (one of four translators), and human DA averages three annotators per language [Q69, Q194]. Krippendorff's alpha is reported but no explicit handling of minority-perspective preservation is described. Given α=0.46 for Amharic, averaging may erase substantial annotator-level disagreement. — _Sources: Q69, Q194, Q211_
- **OC-6**: Convergent validity is at risk: AFRIDOC-MT references may not converge with MOH-credentialed translator judgments [DATASET CRITICAL Concern 1]. External validity is at risk: high system scores against AFRIDOC-MT references do not reliably predict MOH-acceptable performance. Construct validity for the regional deployment is materially weakened by both annotator-credentials uncertainty and low Amharic IAA [Q211, DATASET CRITICAL Concern 4]. — _Sources: Q211, DATASET-D43_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q23] 'We translated the extracted 10k English sentences to the 5 African languages through 4 expert translators per language.' (p.3)
- [Q24] 'The translators were recruited through a language coordinator who is also a native speaker of the language.' (p.3)
- [Q26] 'Due to the domain-specific nature of the task, before starting the translation process, we conducted a translation workshop, during which three translation experts shared their experiences in creating terminologies' (p.3)
- [Q27] 'Quality control was conducted using automated quality estimation, followed by manual inspections by our language coordinators.' (p.3)
- [Q29] 'The translators, in collaboration with the language coordinators, were tasked with reviewing instances that had quality estimation scores below 0.65.' (p.3)
- [Q71] 'We obtained Krippendorff's alpha values of ≥ 0.40, which are relatively low due to the fine granularity of the evaluation scale.' (p.8)
- [Q109] 'Amharic: Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, Lidetewold Kebede' (p.11)
- [Q120] 'Use the language field to input the translations. It is essential not to rely on translation engines, as our quality assurance process can detect this.' (p.18)
- [Q121] 'We will provide a list of extracted terminologies soon so that you can harmonize how terminologies are translated.' (p.18)
- [Q194] 'three native speakers of the African languages—primarily translators involved in the dataset creation—were recruited.' (p.24)
- [Q211] '0.46, 0.57, 0.40, and 0.81, and 0.54 for Amharic, Hausa, Swahili, Yorùbá, and Zulu respectively' (p.26)

*Web sources:*
- [WEB-3] Amharic dialects mutually intelligible per Wikipedia, but health-register variation across bureaus is a separate question — unresolved
- [WEB-8] Academy of Ethiopian Languages Amharic Medical Dictionary exists as a potentially relevant terminology reference for re-annotation
- [WEB-17] Walia-LLM (EMNLP Findings 2024) corroborates broader limitations of Amharic NLP evaluation reliability

*Dataset analysis:*
- DATASET-D43: 'ሱፐርበግስ(superbugs)' — translator choice with potential MOH/EFDA term-list mismatch unverifiable from benchmark alone
- DATASET-D47: 'ribavirin' transliterated — drug-name handling pattern unverifiable against EFDA
- DATASET-D44: 'ጨቅላ ህፃናት ከ6 ወር ጀምሮ የተጣራ፣ የተፈጨ' — clinically precise infant feeding instruction; MOH terminology compliance unverified
- DATASET-D5: 'ፀረ-ተሕዋስያንን መቋቋም(AMR)' — AMR descriptive phrasing; conformance to authoritative term list unknown

</details>

**Information gaps:**
- Professional credentials, MOH affiliation, clinical training, and regional location of the four named Amharic translators
- Whether the human DA evaluators (three native speakers per language, primarily drawn from the translation team [Q194]) hold any clinical credentials
- Whether the planned terminology harmonization [Q121] used any MOH/EFDA-aligned source
- Why Amharic IAA (α=0.46) is so much lower than Yorùbá (0.81) — could reflect translation ambiguity, register variation, or fine granularity of the scale

**Requires expert verification:**
- Direct inquiry to AFRIDOC-MT authors (e.g., Israel Abebe Azime, Saarland University) regarding Amharic translator credentials and regional affiliations
- MOH clinical-translator side-by-side review of a sample of AFRIDOC-MT Amharic references to assess alignment with MOH standards
- Stakeholder elicitation from regional health bureau staff (Tigray, Oromia, Somali) on whether AFRIDOC-MT Amharic register is acceptable

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output form is text-only Amharic translation, matching the deployment exactly [Q1, Q44]. The benchmark provides comprehensive output-form scoring infrastructure: d-BLEU and d-chrF with bootstrap CI [Q51, Q52], chrF prioritized for African morphological richness [Q53], full results tables across models/domains/granularities [Q226–Q231], and per-prompt sensitivity analyses [Q236–Q239]. AfriCOMET is excluded from document-level scoring due to its 512-token context limit [Q175, Q176], and the long-context QE model (ModernBERT) showed no meaningful differentiation and lacks Amharic training [Q97, Q98]. GPT-4o-as-judge is explicitly documented as inconsistent for African languages including Amharic [Q99, Q218, Q219], independently corroborated [WEB-17, WEB-18]. With OF marked LOWER priority by the user (modality match), score 4: form is well-matched, but document-level neural QE for Amharic remains an open gap.

**Strengths:**
- Document-level scoring (d-BLEU, d-chrF) with bootstrap-resampling 95% CIs [Q51, Q52]
- chrF prioritized for African morphological richness — sound metric choice for Amharic [Q53]
- Multiple complementary scoring streams (lexical, neural QE, GPT-4o judge, human DA, qualitative analysis) [Q98]
- Honest reporting of GPT-4o-as-judge unreliability for African languages — directs users to human DA where reliable [Q67, Q68, Q99]
- Output text-only format matches deployment's print/digital Amharic distribution requirement

**Checklist:**

- **OF-1**: Output modality (text-only Amharic) matches deployment exactly. The deployment produces Amharic documents for print and digital distribution; benchmark evaluates text-only translation [Q1, Q44, infrastructure_notes]. — _Sources: Q1, Q44, DATASET-D1, DATASET-D12_
- **OF-2**: Text-to-speech is not in scope for this deployment — outputs are text-only. INSUFFICIENT DOCUMENTATION on TTS, but this is not a deployment requirement.
- **OF-3**: Literacy considerations affect end-user readability. Ethiopia adult literacy ~51.8% (2017 UNESCO) [WEB-4] with significant urban-rural and gender gaps [WEB-6, WEB-7]. The benchmark's fluency dimension (1–5) and human DA (0–100) are not specifically calibrated for semi-literate populations — output text may be fluent at expert-translator level but inaccessible to lower-literacy patients. Partial mismatch in scoring calibration relative to deployment audience. — _Sources: WEB-4, WEB-6, WEB-7_
- **OF-4**: External validity for output form is mostly preserved (text-to-text match). Two minor harms: (a) no validated document-level neural QE for Amharic [Q97, Q98, WEB-18], leaving d-chrF and human DA as the only scalable signals; (b) fluency calibration not tied to semi-literate patient comprehension [literacy_profile note]. — _Sources: Q97, Q98, WEB-18_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q51] 'we realigned sentence-level or pseudo-translation outputs into full documents, then computed BLEU (Papineni et al., 2002) and chrF (Popović, 2015) to create document BLEU (d-BLEU) and document chrF (d-chrF).' (p.5)
- [Q52] 'Metrics were computed using SacreBLEU (Post, 2018) with bootstrap resampling (n = 1000) to report 95% confidence intervals.' (p.5)
- [Q53] 'chrF better captures the morphological richness of African languages' (p.5)
- [Q97] 'we evaluated the document-level translation outputs using ModernBERT-base-long-context-qe-v1, trained on the WMT human evaluation dataset across 41 language pairs, including over 20 languages and three African languages (Hausa, Xhosa, and Zulu)' (p.10)
- [Q98] 'However, the scores were nearly identical across all models, offering no meaningful differentiation.' (p.10)
- [Q99] 'While its ratings were consistent for translations into English, the same was not observed for translations into African languages, likely due to the model's limited understanding of these languages.' (p.10)
- [Q175] 'For evaluation, we used BLEU and chrF scores but excluded AfriCOMET due to its backbone model, AfroXLM-R-L (Alabi et al., 2022; Adelani et al., 2024a), having a context length of 512 tokens.' (p.22)
- [Q219] 'These results suggest that using GPT-4o as a translation judge is not yet well-suited for low-resource languages.' (p.26)

*Web sources:*
- [WEB-4] Ethiopia adult literacy ~51.8% (2017 UNESCO) — relevant to readability calibration
- [WEB-6] Significant urban-rural and gender literacy gaps in Ethiopia
- [WEB-17] Walia-LLM corroborates GPT-4o-as-judge unreliability for Amharic
- [WEB-18] arXiv 2402.08015 confirms GPT-4 'lacks ability to evaluate most generation tasks' in Amharic

*Dataset analysis:*
- DATASET-D1: Multi-paragraph Amharic Ethiopic-script output — confirms text-form match
- DATASET-D12: Parallel sentence row in all six languages — confirms en→am output direction

</details>

**Information gaps:**
- Whether deployment requires any TTS or audio output for low-literacy patient channels — unresolved in elicitation
- Whether MOH would require specific document formatting (PDF, Word, print-ready) beyond text

**Requires expert verification:**
- Whether AFRIDOC-MT-style fluency scoring correlates with semi-literate-patient comprehension (could be tested with a small readability study)

---

## Remediation Suggestions

### Output Content ⚠

**Gap:** AFRIDOC-MT Amharic translators have no documented MOH credentials or clinical backgrounds, and α=0.46 Amharic IAA indicates noisy reference signal — a direct mismatch with the deployment's MOH-trained-translator ground-truth authority.

**Recommendation:** Recruit 2–3 MOH-credentialed clinical translators (or Amharic-speaking physicians as fallback) to post-edit a sampled subset (e.g., 50–100 documents) of AFRIDOC-MT Amharic references to MOH/EFDA standards, producing a deployment-aligned evaluation set. Document each post-editor's MOH affiliation, clinical credentials, and regional bureau experience.

### Output Content ⚠

**Gap:** Regional Amharic register variation across Tigray, Oromia, Amhara, and Somali bureaus is unaddressed; benchmark uses single Addis Ababa-centric references whose regional acceptance is unverified.

**Recommendation:** Conduct stakeholder elicitation with regional health bureau staff in at least Oromia, Tigray, and Somali regions to identify any region-specific terminology preferences that would diverge from Addis Ababa-centric references. Document any findings as a register-variation flag set for evaluation.

### Output Ontology ⚠

**Gap:** No benchmark scoring function operationalizes MOH/EFDA glossary compliance — the deployment's primary success criterion is unmeasured.

**Recommendation:** Build a glossary-conformance scorer that extracts source clinical terms, looks them up in the Academy of Ethiopian Languages Amharic Medical Dictionary [WEB-8] and any EFDA-approved list, and scores system outputs on percentage of terms rendered with the institutionally approved Amharic equivalent. Track this metric alongside d-chrF on the Ethiopian-specific evaluation set.

### Output Ontology ⚠

**Gap:** Readability for semi-literate patients is not calibrated by the benchmark — fluency 1–5 reflects expert-translator perception, not patient comprehension.

**Recommendation:** Add a readability evaluation track using either an Amharic readability formula adaptation or HEW-mediated comprehension testing on a small patient sample for maternal-health booklet outputs. Report this as a separate metric alongside fluency scores.

### Input Content ⚠

**Gap:** WHO-sourced content includes substantial geographically remote material (Afghanistan polio, CCHF, volcanoes) and lacks Ethiopia-specific endemic-disease, calendar, and referral-pathway content; translationese effects are visible in Amharic translations.

**Recommendation:** Construct an Ethiopia-specific evaluation supplement of ~50–100 source documents drawn from actual MOH maternal-health booklets, vaccination schedules, and clinical practice guidelines — covering endemic diseases (malaria, TB, kala-azar, trachoma), Ethiopian calendar dates, and tiered-referral terminology. Use AFRIDOC-MT only for general-MT signal and weight Ethiopia-supplement scores higher in deployment decisions.

### Output Form

**Gap:** No validated document-level neural quality estimation metric exists for Amharic; AfriCOMET is sentence-level only and the long-context QE model excludes Amharic.

**Recommendation:** Adopt sentence-level AfriCOMET as a routine quality-control signal at translation-unit level, paired with d-chrF for document-level signal. Treat document-level neural QE as an open research question and avoid relying on GPT-4o-as-judge for Amharic outputs given the benchmark's own and independent corroborating evidence of unreliability [Q219, WEB-18].

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This paper introduces AFRIDOC-MT, a document-level multi-parallel translation dataset covering English and five African languages: Amharic, Hausa, Swahili, Yorùbá, and Zulu." |
| Q2 | 1 | input_ontology | "The dataset comprises 334 health and 271 information technology news documents, all human-translated from English to these languages." |
| Q3 | 1 | input_ontology | "We conduct document-level translation benchmark experiments by evaluating the ability of neural machine translation (NMT) models and large language models (LLMs) to translate between English and these languages, at both the sentence and pseudo-document levels, the outputs being realigned to form complete documents for evaluation." |
| Q4 | 1 | output_form | "Our results indicate that NLLB-200 achieves the best average performance among the standard NMT models, while GPT-4o outperforms general-purpose LLMs." |
| Q5 | 1 | input_ontology | "Fine-tuning selected models leads to substantial performance gains, but models trained on sentences struggle to generalize effectively to longer documents." |
| Q6 | 1 | output_ontology | "Furthermore, our analysis reveals that some LLMs exhibit issues such as under-generation, over-generation, repetition of words and phrases, and off-target translations, specifically for translation into African languages." |
| Q7 | 1 | input_ontology | "In addition, AFRIDOC-MT supports multi-way translation, allowing translations not only between English and the African languages but also between any two of the languages covered." |
| Q8 | 1 | output_form | "We evaluate performance using automatic metrics and compare the results of encoder-decoder models with decoder-only LLMs" |
| Q9 | 1 | output_content | "Jesujoba O. Alabi, Israel Abebe Azime, Miaoran Zhang, Cristina España-Bonet, Rachel Bawden, Dawei Zhu, David Ifeoluwa Adelani, Clement Oyeleke Odoje, Idris Akinade, Iffat Maab, Davis David, Shamsuddeen Hassan Muhammad, Neo Putini, David O. Ademuyiwa, Andrew Caines, Dietrich Klakow" |
| Q10 | 1 | output_content | "Masakhane NLP, Saarland University, Saarland Informatic Campus, DFKI GmbH, Barcelona Supercomputing Center, Inria Paris France, Mila McGill University & Canada CIFAR AI Chair, University of Ibadan Nigeria, National Institute of Informatics Japan, Selcom Tanzania, Imperial College London, University of KwaZulu-Natal, Loughborough University U.K, University of Cambridge U.K." |
| Q11 | 2 | input_content | "There exist several MT evaluation benchmark datasets for African languages." |
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
| Q49 | 5 | input_form | "To select an appropriate chunk size, we conducted initial tests with k = 1 (sentence-level), 5, 10, and 25, choosing k = 10 for our experiments." |
| Q50 | 5 | output_form | "Evaluating document-level translation remains challenging, as existing automatic metrics struggle to capture improvements and account for discourse phenomena (Jiang et al., 2022; Dahan et al., 2024), and embedding-based metrics have not been explored in this context for African languages due to the lack of data." |
| Q51 | 5 | output_form | "Hence, we realigned sentence-level or pseudo-translation outputs into full documents, then computed BLEU (Papineni et al., 2002) and chrF (Popović, 2015) to create document BLEU (d-BLEU) and document chrF (d-chrF)." |
| Q52 | 5 | output_form | "Metrics were computed using SacreBLEU (Post, 2018) with bootstrap resampling (n = 1000) to report 95% confidence intervals." |
| Q53 | 5 | output_form | "We report d-chrF scores for the best prompt per model and language direction in the main text, as chrF better captures the morphological richness of African languages (Adelani et al., 2022), with full results provided in Appendix C." |
| Q54 | 5 | output_form | "We use GPT-4o as a judge to evaluate translation outputs, following recent work showing LLMs' effectiveness in assessing translation quality and analyzing errors (Wu et al., 2024; Sun et al., 2025)." |
| Q55 | 5 | output_form | "Following Sun et al. (2025), we assess each translated document's fluency, content errors (CE), and cohesion errors—specifically lexical (LE) and grammatical (GE) errors—using GPT-4o, with evaluation limited to a few model outputs due to cost constraints (Appendix B.6)." |
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
| Q66 | 7 | output_ontology | "However, when translating into African languages, the results are less consistent." |
| Q67 | 7 | output_form | "These inconsistencies raise concerns about GPT-4o's reliability." |
| Q68 | 7 | output_form | "Consequently, we focus on human evaluation going forward." |
| Q69 | 7 | output_form | "In Table 10 we report average direct assessment (DA) scores (on a scale from 0 to 100) from three annotators per language for the health domain, when translating into four African languages." |
| Q70 | 7 | output_content | "For each language, we used 30 documents across models and both domains to compute inter-annotator" |
| Q71 | 8 | output_content | "We obtained Krippendorff's alpha values of ≥ 0.40, which are relatively low due to the fine granularity of the evaluation scale." |
| Q72 | 8 | output_form | "Human evaluation results align closely with d-chrF, which favors sentence-level translations over pseudo-document translations when translating into African languages." |
| Q73 | 8 | output_form | "Among the models, LLaMAX3-SFT1 receives higher ratings at the sentence-level but is rated lower when translating pseudo-documents." |
| Q74 | 8 | output_form | "In contrast, LLaMAX3-SFT10 receives slightly lower ratings than LLaMAX3-SFT1 at the sentence-level but is rated higher in the pseudo-document setting." |
| Q75 | 8 | output_form | "GPT-3.5 is generally rated as the weakest model across languages, except for Swahili, where its performance is comparatively better." |
| Q76 | 8 | output_content | "Our qualitative analysis, based on feedback from native speakers who are also authors, indicates that GPT-3.5 frequently over-generates in the pseudo-document setup by repeating words and phrases—except in Swahili, where it performs best." |
| Q77 | 8 | output_content | "However, for Yorùbá, it often uses inconsistent or partial diacritics, resulting in inaccuracies." |
| Q78 | 8 | output_form | "LLaMAX3-SFT1 also exhibits repetition in pseudo-document translations, likely due to a length generalization problem (Anil et al., 2022), and does so more than LLaMAX3-SFT10." |
| Q79 | 8 | output_form | "For the other four languages, LLaMAX3-SFT1 with the sentence-level setup was rated higher than other models and configurations, owing to better context preservation and fewer repetitions." |
| Q80 | 9 | input_content | "We introduce AFRIDOC-MT, a document-level translation dataset in the health and tech domains for five African languages." |
| Q81 | 9 | input_ontology | "We benchmarked various models, fine-tuning selected ones." |
| Q82 | 9 | input_form | "Due to context length limits, documents were translated either sentence by sentence or as pseudo-documents." |
| Q83 | 9 | output_form | "Outputs were evaluated using standard MT metrics, GPT-4o as a judge, and human direct assessment." |
| Q84 | 9 | output_form | "NLLB-200 was the strongest built-in MT model, while GPT-4o outperformed general-purpose LLMs." |
| Q85 | 9 | output_form | "However, our DA and qualitative analysis found GPT-4o's judgments inconsistent for African languages, and sentence-by-sentence translation proved more effective for some languages." |
| Q86 | 9 | input_ontology | "We evaluated only a small subset of the numerous multilingual LLMs available." |
| Q87 | 9 | input_form | "Our experiments were also limited by the context length of the LLMs, particularly for open LLMs." |
| Q88 | 9 | input_form | "Except for LLama3.1, all other open LLMs have a context length of 8192 tokens, while encoder-decoder models were primarily based on T5." |
| Q89 | 9 | input_form | "This makes it difficult to use the context length beyond a certain limit, making full document translation infeasible." |
| Q90 | 9 | input_form | "LLMs are prone to variance in performance based on the prompt." |
| Q91 | 9 | input_ontology | "We therefore evaluated them for translation using three different prompts." |
| Q92 | 9 | input_form | "However, it is possible that our prompts were not optimal." |
| Q93 | 10 | input_ontology | "Africa is home to thousands of indigenous languages, many of which exhibit unique linguistic properties. However, due to the high cost of translation using human translators and limited available funding, it is currently impossible to cover all languages. As a result, we focused on just five languages." |
| Q94 | 10 | input_ontology | "AFRIDOC-MT is a multi-way parallel dataset. However, due to the cost of running inference over three prompts and across all 30 translation directions for all the models evaluated, most of our analysis is limited to translation tasks between English and the five African languages." |
| Q95 | 10 | output_form | "While we fine-tuned NLLB-200, LLama3.1 and LLaMAX3 on all 30 directions, we only provide results from NLLB-200 for all directions both before and after fine-tuning for sentence-level and pseudo-document tasks in the Appendix D." |
| Q96 | 10 | output_form | "Quality evaluation in MT is an open and ongoing area of research, especially for document-level translation. Recent works have proposed embedding-based metrics for evaluation at both the sentence and document levels. While this has been well explored for high-resource language pairs, it remains underexplored for African languages, although there is a tool, AfriCOMET, that works for sentence-level evaluation in African languages." |
| Q97 | 10 | output_form | "However, we evaluated the document-level translation outputs using ModernBERT-base-long-context-qe-v1, trained on the WMT human evaluation dataset across 41 language pairs, including over 20 languages and three African languages (Hausa, Xhosa, and Zulu), two of which are included to our work." |
| Q98 | 10 | output_form | "However, the scores were nearly identical across all models, offering no meaningful differentiation. Hence, for our document-level evaluation, in addition to lexical-based metrics, we incorporated three other evaluation approaches: using GPT-4o as a judge, human evaluation, and qualitative analysis." |
| Q99 | 10 | output_form | "GPT-4o was employed to assess and rate the translation outputs of four models. While its ratings were consistent for translations into English, the same was not observed for translations into African languages, likely due to the model's limited understanding of these languages." |
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
| Q119 | 18 | input_form | "Please do not delete double empty rows, as they serve to separate paragraphs. Also, avoid deleting any rows, columns, or provided text." |
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
| Q142 | 20 | input_ontology | "Gemma2 (Gemma Team et al., 2024) is a decoder-only LLM trained on billions of tokens sourced from the web. The training data primarily consists of English-language text, but it also includes code and mathematical content. While Gemma2 has an English-centric focus, it also possesses multilingual capabilities. We evaluate the base Gemma2 model with 9B parameters, as well as its instruction-tuned version." |
| Q143 | 20 | input_ontology | "LLama3.1 (Dubey et al., 2024) is another decoder-only LLM trained on trillions of tokens across multiple languages. It was fine-tuned using existing instruction datasets as well as synthetically generated instruction data to create its instruction-tuned version. One advantage LLama3.1 has over other models is its context window of 128K tokens, the largest among all models considered in this work, making it particularly suitable for document-based tasks such as document-level translation. We evaluate the base LLama3.1 model with 8B parameters, as well as its instruction-tuned version." |
| Q144 | 20 | input_ontology | "LLaMAX3 (Lu et al., 2024) is a multilingual LLM built on the LLama3 with 8B parameters as its base. It was trained on 102 languages, including several African languages, through continued pretraining. Using an English instruction dataset (Alpaca), it was further fine-tuned to create LLaMAX3-Alpaca. We evaluated both models and compared their performance across various tasks." |
| Q145 | 20 | input_form | "We perform supervised fine-tuning to tailor LLMs for translation tasks. To train sentence-level MT systems, we use all parallel sentences from AFRIDOC-MT to construct the training set, enabling the LLMs to translate across multiple directions and domains. Following Zhu et al. (2024b), we augment the parallel data with translation instructions, which are randomly sampled from a predefined set of 31 MT instructions for each training example." |
| Q146 | 21 | input_form | "To train document-level MT systems, we follow the same process, but train on longer segments formed by concatenating multiple sentences." |
| Q147 | 21 | input_form | "When fine-tuning, we use a learning rate of 5e−6 and an effective batch size of 64." |
| Q148 | 21 | input_ontology | "Models are trained for only one epoch, as further training does not result in improvements and may even lead to performance degradation." |
| Q149 | 21 | input_form | "we fine-tuned the 1.3B version of NLLB-200 for sentence and pseudo-document (with 10 sentences) translation using the Fairseq (Ott et al., 2019) codebase." |
| Q150 | 21 | input_content | "We used all the training examples from 30 language directions across both domains." |
| Q151 | 21 | input_form | "The model was fine-tuned for 50k steps using a learning rate of 5e−5, token batch size of 2048 and a gradient accumulation of 2." |
| Q152 | 21 | input_form | "The checkpoint with the lowest validation loss was selected as the best model for evaluation." |
| Q153 | 21 | output_form | "The models were evaluated using different tools. For example, both the NLLB-200 and M2M-100 models were evaluated with the Fairseq codebase, while Toucan and MADLAD-400 were evaluated using the Hugging Face (HF) codebase." |
| Q154 | 21 | output_form | "All other LLMs, including LLama3.1 (both instruction-tuned and SFT models), Gemma, and Aya-101, were evaluated using EleutherAI LM Evaluation Harness (lm-eval) tool (Biderman et al., 2024)." |
| Q155 | 21 | output_form | "In all cases, greedy decoding was used." |
| Q156 | 21 | input_form | "The models evaluated have different context lengths. For encoder-decoder models, M2M-100 and NLLB have a maximum sequence length of 1024 and 512 respectively." |
| Q157 | 21 | output_form | "Aya-101 and MADALAD, based on the T5 architecture, do not have a pre-specified maximum sequence length, so we fixed their maximum sequence length to 1024 for all experiments involving encoder-decoder models." |
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
| Q177 | 22 | output_form | "We use GPT-4o to assess the quality of translation output, as demonstrated by Sun et al. (2025), which shows a correlation with human judgment." |
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
| Q193 | 24 | output_form | "Translation into English was excluded, as existing automatic metrics, including GPT-based evaluations, are already reliable for this direction." |
| Q194 | 24 | output_content | "For the human evaluation, three native speakers of the African languages—primarily translators involved in the dataset creation—were recruited." |
| Q195 | 24 | output_content | "Each annotator was assigned 80 documents to evaluate, tasked with marking as many error spans as possible and rating the overall quality on a scale from 0 to 100." |
| Q196 | 24 | output_form | "This annotation followed the error span annotation (ESA) (Kocmi et al., 2024) protocol as implemented within the Appraise Evaluation Framework (Federmann, 2018)." |
| Q197 | 24 | output_content | "To assess consistency and inter-annotator agreement, 30 of the 80 documents were shared among all three annotators." |
| Q198 | 24 | output_content | "Each annotator was remunerated with $55.15" |
| Q199 | 24 | output_content | "Alongside the human direct assessment of the translation outputs, we shared a subset of the outputs with one author per language, each a native speaker." |
| Q200 | 24 | output_content | "They were tasked with analyzing the outputs to answer two key questions: (1) What common errors or flaws do the models exhibit across different setups? and (2) How fluent are the translation outputs produced by the models across the various settings?" |
| Q201 | 24 | input_form | "Given that AFRIDOC-MT is a document-level translation dataset, and due to the limited context length of most translation models and LLMs, which makes it impossible to translate a full document at once, we opted to translate the sentences within the documents and then merge them back to form the complete document. For document-level evaluation, we split the documents into chunks of 10 sentences and translate these chunks using the different models." |
| Q202 | 25 | output_form | "In Tables 19 and 20 we provide the full results on the merged pseudo-documents using d-chrF and d-BLEU." |
| Q203 | 25 | input_form | "It is important to note that we also trained and evaluated NLLB-200 for pseudo-document translation. However, due to its 512-token maximum sequence length, it is not competitive." |
| Q204 | 25 | output_form | "Our results show that both LLama3.1 and LLaMAX3 models, when fine-tuned on sentences, performed significantly worse on pseudo-document evaluations compared to the same models fine-tuned on pseudo-documents for both domains." |
| Q205 | 25 | input_form | "All these models were trained using a similar setup, with the primary difference being the data used for fine-tuning." |
| Q206 | 25 | output_form | "Overall, no clear trend is observed in MT performance across language family classes. However, Amharic (a non-Latin script language) and Yorùbá (a heavily diacriticitized language) result in the lowest chrF scores, while Swahili—the most widely spoken indigenous African language—performs best." |
| Q207 | 25 | output_form | "In Tables 21 and 22 we present the average GPT-4o evaluation results for four models." |
| Q208 | 25 | output_form | "When translating into African languages, there is no clear pattern: for example, GPT-3.5, despite having the lowest fluency score, also had the fewest content, lexical, and grammatical errors, which is counterintuitive." |
| Q209 | 26 | output_content | "We were able to obtain DA scores from three annotators for all the languages." |
| Q210 | 26 | output_content | "For each language, we calculated inter-annotator agreement using Krippendorff's alpha α over 30 document instances." |
| Q211 | 26 | output_content | "We obtained α scores of 0.46, 0.57, 0.40, and 0.81, and 0.54 for Amharic, Hausa, Swahili, Yorùbá, and Zulu respectively." |
| Q212 | 26 | output_content | "These are relatively low scores, except for Yorùbá." |
| Q213 | 26 | output_form | "We present the average DA scores in Tables 10 and 14 for the health and tech domains, respectively." |
| Q214 | 26 | output_form | "The results show that annotators rate documents translated at the sentence-level as higher quality than those translated at the pseudo-document level." |
| Q215 | 26 | output_form | "Additionally, GPT-3.5 received the lowest ratings among the three models." |
| Q216 | 26 | output_form | "LLaMAX3-SFT1, a model trained on sentence-level data, was rated the best across all languages when evaluated on sentences." |
| Q217 | 26 | output_form | "However, when evaluated on pseudo-documents, its performance was rated lower than that of LLaMAX3-SFT10." |
| Q218 | 26 | output_form | "These findings are consistent with the d-chrF scores for the models, but they do not align with the evaluations from GPT-4o as a judge." |
| Q219 | 26 | output_form | "These results suggest that using GPT-4o as a translation judge is not yet well-suited for low-resource languages." |
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
| Q233 | 33 | output_form | "Table 21: Document-level evaluation in the health domain, judged by GPT-4o." |
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
| WEB-1 | https://regulations.ai/regulations/RAI-ET-NA-PDPPNXX-2024 |
| WEB-2 | https://www.techhiveadvisory.africa/insights/review-of-ethiopias-data-protection-act |
| WEB-3 | https://en.wikipedia.org/wiki/Amharic |
| WEB-4 | https://www.theglobaleconomy.com/Ethiopia/Literacy_rate/ |
| WEB-5 | https://knoema.com/atlas/Ethiopia/topics/Education/Literacy/Adult-literacy-rate |
| WEB-6 | https://zoetalentsolutions.com/education-statistics-for-ethiopia/ |
| WEB-7 | https://countrymeters.info/en/Ethiopia |
| WEB-8 | https://archive.org/details/amharic-dictionary-of-medical-terms-108p-copy |
| WEB-9 | https://www.scribd.com/document/416080918/English-Amharic-Oromiffa-Somali-Afar |
| WEB-10 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11923465/ |
| WEB-11 | https://datareportal.com/reports/digital-2024-ethiopia |
| WEB-12 | https://www.gsma.com/about-us/regions/sub-saharan-africa/wp-content/uploads/2024/10/GSMA_Ethiopia-Report_Oct-2024_v2-1.pdf |
| WEB-13 | https://www.worldbank.org/en/results/2025/06/30/empowering-ethiopians-by-laying-the-digital-foundations-for-afe-economic-growth |
| WEB-14 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10866294/ |
| WEB-15 | https://lastmilehealth.org/2024/05/01/last-mile-health-launches-ethiopias-first-non-communicable-disease-training-for-community-health-workers/ |
| WEB-16 | https://ethiopiahealth.blogs.wm.edu/ethiopian-health-system/ |
| WEB-17 | https://aclanthology.org/2024.findings-emnlp.25/ |
| WEB-18 | https://arxiv.org/abs/2402.08015 |
| WEB-19 | https://link.springer.com/article/10.1007/s44248-025-00077-9 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** masakhane/AfriDocMT
**Analysis date:** 2025-07-12
**Examples reviewed:** 51 total (5 from doc_health train, 5 from doc_health_10 train, 5 from doc_health_25 train, 5 from doc_health_5 train, 5 from doc_tech train, 5 from doc_tech_10 train, 5 from doc_tech_25 train, 5 from doc_tech_5 train, 5 from health train, 6 from tech train, 5 from doc_tech train)
**Columns shown:** am, en, ha, sw, yo, zu
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | doc_health, train | Ex. 1 | health | "የሞቃታማ ዐውሎ ነፋሶች ... ለሞቃታማ አውሎ ነፋሶች፣ እንዲሁም ሀይለኛ አውሎ ነፋስ ወይም አውሎ ነፋሶች ... ኃይለኛ ክብ አውሎ ነፋሶች ... 233 000 ሰዎችን ገድለዋል" | Full Amharic document on tropical cyclones (WHO article), multi-sentence, Ethiopic script, with clinical/epidemiological content and specific numbers | IF, IC |
| D2 | doc_health, train | Ex. 1 | health | "When tropical cyclones cause floods and sea surges, the risk of drowning and water- or vector-borne diseases increase." | WHO English source on tropical cyclones — generic global health content, no Ethiopia-specific epidemiological context | IC |
| D3 | doc_health, train | Ex. 2 | health | "አካል ጉዳተኝነት ሰው የመሆን አካል ነው፡፡ ሁሉም ሰው ማለት ይቻላል በሕይወታቸው ላይ በሆነ ወቅት ጊዚያዊ ወይም ዘላቂ የአካል ጉዳት ያጋጥማቸዋል" | Amharic WHO article on disability — prose narrative, full document preserved | IC, IF |
| D4 | doc_health, train | Ex. 3 | health | "ተጨማሪ ምግብ ማጠቃሊያ፡- በ 6 ወር አካባቢ የሕፃኑ የኃይል ፍላጎት ... ጨቅላ ህፃናት ... ጡት ማጥባት" | Amharic complementary feeding article — maternal-child health topic directly relevant to deployment (maternal-health booklets) | IC, OC |
| D5 | doc_health, train | Ex. 4 | health | "ፀረ-ተሕዋስያንን መቋቋም(AMR) ... ባክቴሪያ፣ ጥገኛ ተውሳኮች፣ ቫይረሶችና በፈንገሶች ምክንያት" | Amharic AMR article — specialized medical terminology in Ethiopic script | OC, IF |
| D6 | doc_health, train | Ex. 5 | health | "ክራይሚያ-ኮንጎ የደም መፍሰስ ትኵሳት ... CCHF ወረርሽኞች ... ከ10-40% ሞት ... ሞቃታማ አውሎ ነፋስ" | Amharic article on CCHF hemorrhagic fever — clinical terminology, disease outside typical Ethiopian endemic profile | IC |
| D7 | doc_health_10, train | Ex. 1 | health | "ነገር ግን፣ በ2023 እስከ ዛሬ 46 ደብሊዉፒቪ1 አዎንታዊ የአካባቢ ናሙናዎች ... ናንጋርሃር እና ኩናር አውራጃዎች ... ሚሊዮን ተመላሾች" | Amharic WHO article on Afghanistan polio — geographic specificity to Afghanistan/Pakistan, not Ethiopia; pseudo-document chunk (10 sentences) | IC, IO |
| D8 | doc_health_10, train | Ex. 2 | health | "የጤና አጠባበቅ አቅራቢዎች ከአካባቢያዊ አስጊ ሁኔታዎች ጋር የተዛመዱ የህጻናት በሽታዎችን ... ከሁለቱም ያደጉ እና በማደግ ላይ ያሉ ሀገራት" | Short Amharic sentence fragment — environment/child health with global framing | IC |
| D9 | doc_health_25, train | Ex. 2 | health | "ዓለም አቀፍ ትብብር የጋራ ዓላማን ለማሳካት ... ዜሮ ዶዝ ... ህፃናት ፈልጎ ማግኘት ... ዶ/ር ጆርጅ ምዊንያ" | Amharic WHO Assembly article about immunization — broad vaccination language relevant to vaccination schedule booklets | IC |
| D10 | doc_health_5, train | Ex. 4 | health | "Malnutrition in the early years of life can have long-lasting impacts on physical and mental development... WHO recommends breastfeeding babies exclusively for 6 months" | English WHO source on malnutrition — maternal-child health content aligned with deployment domain | IC |
| D11 | health, train | Ex. 4 | health (sentence) | "Measures for the prevention of cholera mostly consist of providing clean water and proper sanitation to populations who do not yet have access to basic services, as well as vaccination with Oral Cholera Vaccines." | Sentence-level WHO cholera prevention content — cholera is endemic in Ethiopia but article is generic global | IC, IO |
| D12 | health, train | Ex. 1 | health (sentence) | "OCV ni zana ambayo hutumiwa pamoja na hatua za kudhibiti kipindupindu." (sw) / "OCV jẹ́ ohun èlò fún àfikún àwọn ìlànà fún ṣíṣe àmójútó àrùn onígbá méjì" (yo) | Sentence-level multi-language row — all six languages present including Amharic | IF |
| D13 | doc_tech, train | Ex. 1 | tech | "ፔይ ዴይ ለሽያጭ ? ዛሬ በ ቴክ ፖይንት አፍሪካ ... የናይጄሪያ ፕረዚዳንት ... ፔይ ደይ ... ኦባሲ ኢነ-ኦቦንግ" | Amharic Techpoint Africa tech-news article about Nigerian fintech/genomics — not relevant to Ethiopian MOH deployment | IC, IO |
| D14 | doc_tech, train | Ex. 2 | tech | "ደቡብ አፍሪካ ጎጂ ይዘቶችን በመስመር ላይ ማቆም ትፈልጋለች ... YouTube ... NALA ... Cellulant ... ሴሉላንት 20%" | Long Amharic tech article: South Africa content regulation, YouTube, NALA remittances, Cellulant layoffs — entirely irrelevant to Ethiopian clinical translation | IO, IC |
| D15 | doc_health, train | Ex. 3 | health | "ደህንነቱ የተጠበቀ፡- በንጽህና ተከማችተው እና ተዘጋጅተዋል እንዲሁም ጠርሙሶች እና ፕላስቲኮችን ሳይሆን በንጹህ እቃዎች ... ጡት ማጥባት" | Complementary feeding clinical guidance in Amharic — high relevance (maternal health booklet content) | IC, OC |
| D16 | doc_health, train | Ex. 1 | health | "Tropical cyclones, also known as typhoons or hurricanes, are among the most destructive weather phenomena." | WHO article on tropical cyclones — generic global health emergency content | IC |
| D17 | doc_health_25, train | Ex. 4 | health | "ጡት ማጥባት የማስተዋል አቅም መጨመር፣ የትምህርት ቤት አፈፃፀም ... ጡት ማጥባት ትቁ ብሎ ይመክራሉ" | Amharic infant nutrition article — direct overlap with maternal-health booklet deployment | IC |
| D18 | doc_health, train | Ex. 2 | health | "Disability results from the interaction between individuals with a health condition, such as cerebral palsy, Down syndrome and depression, with personal and environmental factors" | WHO disability article — relevant to health sector but not to primary clinical guideline/maternal-health booklet domain | IC |
| D19 | doc_health_25, train | Ex. 3 | health | "COVID-19 ... Interim position paper: considerations regarding proof of COVID-19 vaccination for international travellers" | COVID-19 international travel advisory — time-limited, globally generic, not Ethiopia-specific | IC |
| D20 | doc_health_25, train | Ex. 5 | health | "ዓለም አቀፍ የጤና ደንቦች ... IHR 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ" | International Health Regulations article — relevant to health systems globally, but highly technical/regulatory, not maternal-clinical prose | IC |
| D21 | doc_health, train | Ex. 4 | health | "Antimicrobial resistance ... AMR threatens the effective prevention and treatment of an ever-increasing range of infections caused by bacteria, parasites, viruses and fungi." | AMR — critical global health topic relevant to clinical settings, within WHO source domain | IC |
| D22 | doc_tech_25, train | Ex. 1 | tech | "Fatanmi identifies is its effect on marketing a business ... Gen Zs ... Building in public..." | Tech article about startup marketing strategy — entirely irrelevant to Ethiopian MOH clinical translation deployment | IO |
| D23 | health, train | Ex. 2 | health (sentence) | "However, what is clear is that health systems need to predominantly rely on public revenue sources: mandatory, pre-paid and pooled" | Health financing sentence — health systems policy, not clinical guideline content | IC |
| D24 | health, train | Ex. 3 | health (sentence) | "Similarly, the development and promotion of WHO international reference standards helps ensure that biological therapeutics are standardized between different manufacturers, countries, and laboratories." | Biological therapeutics standardization — very specialized regulatory content | IC |
| D25 | doc_health_10, train | Ex. 3 | health | "ጤና ስርዓቱ መጠነ ሰፊ ለውጥ ... የቅድመ ክፍያ ፈንድ ... ዘላቂ ልማት ግቦች" | Health financing/health accounts article — health systems economics, not clinical or maternal-health prose | IC |
| D26 | doc_health_10, train | Ex. 4 | health | "ዚካ ቫይረስ ... ፀረ-ተባይ ... Vector control operations framework for Zika virus" | Short Zika virus sentence fragment — topic not endemic to Ethiopia | IC |
| D27 | doc_health_10, train | Ex. 5 | health | "የጤና አካውንት ሥርዓት ... የጤና ወጪን ... SHA 2011" | Health accounts system article — health financing methodology, not clinical guideline content | IC |
| D28 | doc_health_5, train | Ex. 1 | health | "የ ቲአርአይፒኤስ ስምምነት ... TRIPS ... ዓለም ንግድ ድርጅት ... WTO ... WIPO" | TRIPS/intellectual property & medicines article — health policy, not clinical guideline | IC |
| D29 | doc_health_5, train | Ex. 3 | health | "ግብር እና ድጎማ ... ማህበራዊ ሚዲያ ይዘቶቻቸውን ለፖሊሲ ምርጫ" | Health system governance/taxes sentence fragment — health policy tools | IC |
| D30 | doc_health, train | Ex. 3 | health | "Ensuring that infants nutritional needs are met requires that complementary foods be: timely ... adequate ... safe ... properly fed" | WHO complementary feeding — directly matches maternal-health booklet deployment content | IC, OC |
| D31 | doc_health_25, train | Ex. 4 | health | "ጡት ማጥባት … ሞተዋል .... 820,000 ... 40% ..." | Amharic infant nutrition WHO article — directly relevant to maternal-health booklet | OC |
| D32 | doc_health, train | Ex. 5 | health | "Crimean-Congo haemorrhagic fever (CCHF) is a viral haemorrhagic fever usually transmitted by ticks ... CCHF is endemic in all of Africa, the Balkans, the Middle East and in Asia." | CCHF article — hemorrhagic fever not a primary health priority in Ethiopia; tick-borne virus | IC |
| D33 | doc_health_25, train | Ex. 3 | health | "A volcano is a vent in the Earth's crust from which eruptions occur... There are about 1500 potentially active volcanoes worldwide." | Volcanic eruption WHO article — not relevant to Ethiopian clinical translation deployment | IC, IO |
| D34 | doc_health_10, train | Ex. 1 | health | "Afghanistan continues to implement an intense campaign schedule, focusing on improving quality in the endemic zone... massive population movement significantly increases the risk of cross-border poliovirus spread" | WHO Afghanistan polio article — geographically specific to Afghanistan, not Ethiopia | IC |
| D35 | doc_health_5, train | Ex. 2 | health | "ይህ ለሕዝብ ጤና ድንገተኛ አደጋዎች እና ለ አይኤችአር ትግበራ ... WGIHR6 ... PHEIC" | International health regulations/WGIHR process article — technical governance content | IC |
| D36 | doc_health_25, train | Ex. 2 | health | "The WHA evaluated the unique epidemiological opportunity which exists over the next six months to eradicate the remaining chains of endemic wild poliovirus transmission." | WHO Assembly polio article — immunization content indirectly relevant (vaccination schedules), but Afghanistan/global framing not Ethiopia-specific | IC |
| D37 | doc_health_5, train | Ex. 5 | health | "WHO works with Member States to ensure key populations have adequate knowledge about appropriate foods and feeding practices" | WHO complementary feeding counselling — maternal-child health, highly relevant | IC, OC |
| D38 | doc_tech_10, train | Ex. 1 | tech | "የሕንድ ኢድቴክ ኢንዱስትሪ ... ሕንድ ከዩናይትድ ስቴትስ (ዩ ኤስ) ቀጥሎ ... edtech ... Central Square Foundation ... Nigerian Edtech ecosystem" | Indian/Nigerian edtech article — entirely irrelevant to Ethiopian clinical translation | IO |
| D39 | doc_tech_25, train | Ex. 2 | tech | "Nigerian healthtech startup, Clafiya, raises $610,000 in pre-seed funding" | African healthtech/fintech startup news — entirely irrelevant to Ethiopian MOH clinical translation deployment | IO |
| D40 | health, train | Ex. 5 | health (sentence) | "Safe, effective and quality-assured blood products contribute to improving and saving millions of lives every year" | Blood products sentence — health domain but not maternal/clinical guideline focus | IC |
| D41 | doc_health, train | Ex. 1 | health | "WHO helps to restore primary care services so that facilities can deliver essential services, including immunization, basic treatment for common illnesses, acute malnutrition and maternal care" | WHO cyclone response includes immunization + maternal care — partially relevant content | IC, OC |
| D42 | doc_health_25, train | Ex. 4 | health | "የዓለም ጤና ድርጅት ሕፃናትን ለ6 ወራት ብቻ እንዲያጠቡ ይመክራል ... ደህንነቱ የተጠበቀ እና ተጨማሪ ምግብ" | Amharic WHO recommendation on exclusive breastfeeding — direct match for maternal-health booklet content | IC, OC |
| D43 | doc_health, train | Ex. 4 | health | "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ፣ ፀረ-ፈንገስ ... 'ሱፐርበግስ(superbugs)'" | AMR article with English loanword "superbugs" retained in Amharic — illustrates translationese patterns | IC, OC |
| D44 | doc_health, train | Ex. 3 | health | "ጨቅላ ህፃናት ከ6 ወር ጀምሮ የተጣራ፣ የተፈጨ እና ከፊል ጠጣር ምግቦችን መመገብ ይችላሉ" | Amharic instruction for pureed/mashed foods from 6 months — clinically precise maternal-health instruction | OC |
| D45 | doc_health_10, train | Ex. 2 | health | "To allow healthcare providers to better identify and prevent childhood diseases related to environmental risk factors, experts from both developed and developing countries" | Short environmental health sentence — health domain but generic | IC |
| D46 | doc_health_5, train | Ex. 1 | health | "TRIPS Agreement, many resolutions of the World Health Assemblies have requested WHO to address the impact of trade agreements and intellectual property protection on public health and access to medicines" | TRIPS/IP health policy — highly technical policy content | IC |
| D47 | doc_health, train | Ex. 5 | health | "CCHF ወረርሽኞች ቫይረሱ ወደ ወረርሽኞች ሊያመራ ስለሚችል ከፍተኛ የሞት መጠን (ከ10-40%)... ህክምና፡- የክራይሚያ-ኮንጎ ... ፀረ-ቫይረስ መድሃኒት ... ribavirin" | CCHF treatment article in Amharic including "ribavirin" (transliterated drug name) — medical terminology rendering pattern visible | OC |
| D48 | doc_health_25, train | Ex. 4 | health | "ዓለም አቀፍ የጤና ሽፋን ... ዘላቂ የልማት ግቦች ... SDG ... ዘርፈ ብዙ የህዝብ ጤና" | Disability/UHC policy article — health governance framing, not clinical maternal health | IC |
| D49 | doc_health_25, train | Ex. 1 | health | "Continue to support research to improve vaccines that reduce transmission and have broad applicability; to understand the full spectrum, incidence and impact of post COVID-19 condition" | COVID-19 research policy article — time-limited global policy content | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Authentic Amharic Ethiopic-script health translations present throughout
- **Dimension(s):** IF, IC
- **Observation:** All health examples contain Amharic (`am`) column text in Ethiopic/Ge'ez script. The data consistently includes full-document Amharic prose across health topics, with complex multi-sentence Amharic translations demonstrating that the benchmark actually contains the script and language variant required. The documents are narrative prose, matching the user's accepted scope.
- **Deployment relevance:** This directly confirms that the benchmark evaluates the target script and language combination (Amharic, Ethiopic script) for the deployment. The text in [D1] shows a full multi-paragraph Amharic WHO article of the type that would appear in MOH distribution materials, and [D4] and [D5] demonstrate medical terminology rendering in Ethiopic script.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "የሞቃታማ ዐውሎ ነፋሶች ... ኃይለኛ ክብ አውሎ ነፋሶች ... 233 000 ሰዎችን ገድለዋል" — Full-length Amharic health document in Ethiopic script with numbers, medical terms, and multi-paragraph structure.
  - [D5] Example 4 (doc_health, split=train): "ፀረ-ተሕዋስያንን መቋቋም(AMR) ... ባክቴሪያ፣ ጥገኛ ተውሳኮች፣ ቫይረሶችና" — Medical terminology for AMR rendered in Ethiopic script with parenthetical English acronym, showing how clinical terms are handled.
  - [D47] Example 5 (doc_health, split=train): "ህክምና፡- የክራይሚያ-ኮንጎ ... ፀረ-ቫይረስ መድሃኒት ... ribavirin" — Drug name "ribavirin" transliterated alongside Amharic clinical treatment text.

#### Strength 2: Multi-parallel structure enables comparison across all six languages simultaneously
- **Dimension(s):** IF, OO
- **Observation:** Every data row contains parallel translations in all six languages (am, en, ha, sw, yo, zu) from the same source document. This enables evaluation of Amharic translation quality directly against the English source, while also permitting cross-linguistic comparison.
- **Deployment relevance:** The deployment is English→Amharic. The benchmark directly supports this evaluation direction. The parallel structure means one can assess whether a model correctly translates a sentence such as [D2] into Amharic [D1] within the same row.
- **Datapoint citations:**
  - [D12] Example 1 (health, split=train, sentence-level): "OCV wata hanya ce da ake amfani da ita a ƙari a kan hanyar kula da kwalara" (ha) — Each row contains all six translations of the same sentence, enabling direct comparison.

#### Strength 3: Maternal and child health content directly matching deployment domain
- **Dimension(s):** IC, OC
- **Observation:** Several WHO articles in the health corpus directly cover topics central to the MOH deployment scope: complementary feeding (Example 3, doc_health train), infant nutrition including breastfeeding recommendations (doc_health_25, Example 4), and similar maternal-child health topics. These represent the closest thematic match to the stated deployment use case of maternal-health booklets and vaccination schedules.
- **Deployment relevance:** The deployment specifically names maternal-health booklets as a primary document type. The complementary feeding, breastfeeding, and infant nutrition articles are substantively equivalent to maternal-health booklet content, making these the highest-value examples in the corpus for validity assessment.
- **Datapoint citations:**
  - [D4] Example 3 (doc_health, split=train): "ተጨማሪ ምግብ ማጠቃሊያ፡- በ 6 ወር አካባቢ የሕፃኑ የኃይል ፍላጎት ... ጨቅላ ህፃናት" — Full Amharic complementary feeding article directly matching maternal-health booklet content.
  - [D15] Example 3 (doc_health, split=train): "Ensuring that infants nutritional needs are met requires that complementary foods be: timely ... adequate ... safe" — English source for complementary feeding guidelines.
  - [D42] Example 4 (doc_health_25, split=train): "የዓለም ጤና ድርጅት ሕፃናትን ለ6 ወራት ብቻ እንዲያጠቡ ይመክራል ... ደህንነቱ የተጠበቀ እና ተጨማሪ ምግብ" — Amharic WHO breastfeeding recommendation — directly applicable to maternal-health booklet context.
  - [D37] Example 5 (doc_health_5, split=train): "WHO works with Member States to ensure key populations have adequate knowledge about appropriate foods and feeding practices" — maternal-child health domain.

#### Strength 4: Document-level structure preserved, enabling assessment of paragraph-level cohesion
- **Dimension(s):** IF, OO
- **Observation:** The `doc_health` config contains full documents (Example 1 is a complete WHO tropical cyclones article; Example 2 is a full disability article), not isolated sentences. The chunked configs (`doc_health_10`, `doc_health_5`, etc.) preserve multi-sentence pseudo-documents. This means the benchmark can test context-dependent translation phenomena such as pronoun resolution and terminological consistency across paragraphs.
- **Deployment relevance:** Clinical practice guidelines and maternal-health booklets are multi-page documents. The benchmark's document-level structure directly supports evaluation of translation fidelity across longer clinical text units, which is critical for the deployment.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): The Amharic tropical cyclones article contains multiple paragraphs with consistent use of "ዐውሎ ነፋሶች" (tropical cyclones) across sections, demonstrating intra-document terminological consistency.
  - [D3] Example 2 (doc_health, split=train): "አካል ጉዳተኝነት ሰው የመሆን አካል ነው፡፡ ሁሉም ሰው ..." — Full WHO disability article across many paragraphs.

#### Strength 5: WHO-sourced health prose directly equivalent to Ethiopian MOH distribution materials
- **Dimension(s):** IC
- **Observation:** The health corpus is entirely sourced from WHO public health articles. The register, topic range, and structural patterns (overview → impact → WHO response) match the type of narrative prose typical of WHO-aligned MOH health communication materials. Topics such as cholera prevention (D11), AMR (D21), immunization (D36, D9), and maternal-child health (D4, D42) all fall within the scope of clinical guideline and health booklet content distributed by Ministries of Health.
- **Deployment relevance:** The user accepted generic WHO-sourced health prose as sufficient for the current evaluation scope. This is confirmed as a good match: the corpus provides the same institutional register and authorial voice as source documents that Ethiopian MOH materials would be translated from.
- **Datapoint citations:**
  - [D11] Example 4 (health, split=train): "Measures for the prevention of cholera mostly consist of providing clean water and proper sanitation" — WHO cholera prevention sentence; cholera is endemic in Ethiopia, making this directly relevant.
  - [D41] Example 1 (doc_health, split=train): "WHO helps to restore primary care services so that facilities can deliver essential services, including immunization, basic treatment for common illnesses, acute malnutrition and maternal care" — WHO response article encompasses immunization and maternal care, both central to the deployment domain.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Annotator credentials for Amharic reference translations are undocumented and likely do not match deployment ground-truth authority
- **Dimension(s):** OC
- **Observation:** The four named Amharic translators (Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, Lidetewold Kebede, per Q109) appear in data rows containing complex clinical terminology — including AMR, antimicrobials, hemorrhagic fever treatment (ribavirin), and infant nutrition guidance. The benchmark documentation provides no professional credentials, institutional affiliations, or clinical backgrounds for these translators. No MOH certification or EFDA terminology training is documented. The terminology in the Amharic translations (e.g., loanword handling for "superbugs," "ribavirin," drug class names in [D43], [D47]) is visible in the data but cannot be independently verified against any institutional standard.
- **Deployment relevance:** The user explicitly identifies MOH-trained clinical translators or Amharic-speaking physicians as the authoritative ground-truth population. If the benchmark's Amharic reference translations were produced by general-purpose translators without clinical MOH credentials, the reference translations against which system outputs are scored may not reflect the clinical accuracy standards the deployment requires. This is the most consequential OC gap: evaluation scores computed against these references may validate translations that do not meet MOH clinical standards, and vice versa.
- **Datapoint citations:**
  - [D43] Example 4 (doc_health, split=train): "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ ... 'ሱፐርበግስ(superbugs)'" — The transliterated English term "superbugs" in Amharic parentheses suggests a translator choice that may or may not conform to MOH/EFDA approved terminology for this concept.
  - [D47] Example 5 (doc_health, split=train): "ፀረ-ቫይረስ መድሃኒት ... ribavirin" — The drug name "ribavirin" is retained in transliterated form; it is unverifiable whether this matches the EFDA-approved Amharic pharmaceutical terminology for this antiviral.
  - [D44] Example 3 (doc_health, split=train): "ጨቅላ ህፃናት ከ6 ወር ጀምሮ የተጣራ፣ የተፈጨ እና ከፊል ጠጣር ምግቦችን" — Maternal-health guidance translated with specific clinical language; conformance to MOH terminology for infant feeding guidance is unverifiable.

#### CRITICAL Concern 2: No mechanism for evaluating MOH/EFDA glossary compliance — the primary deployment success criterion is entirely unoperationalized
- **Dimension(s):** OO
- **Observation:** The benchmark's scoring functions — d-BLEU, d-chrF, GPT-4o-as-judge, and human DA — are all agnostic to any institutional terminology list. The data rows contain medical terminology choices (clinical vocabulary for AMR, vaccines, infant nutrition, hemorrhagic fever) that would need to be assessed against MOH and EFDA approved glossaries in the deployment context, but the benchmark provides no mechanism to do this. The planned terminology harmonization step for translators (Q121) is not documented as having been completed, and no reference to any Ethiopian-specific glossary is found in the data or documentation.
- **Deployment relevance:** The user states that glossary compliance is a primary success criterion. A system that scores well on d-chrF against AFRIDOC-MT references may nonetheless fail to comply with MOH/EFDA approved Amharic medical terminology. Conversely, a system that correctly uses MOH-approved terminology might score lower if that terminology differs from the benchmark translators' choices. This renders d-chrF and BLEU scores partially construct-invalid as measures of the deployment's primary success criterion.
- **Datapoint citations:**
  - [D5] Example 4 (doc_health, split=train): "ፀረ-ተሕዋስያንን መቋቋም(AMR)" — The Amharic rendering of "antimicrobial resistance" uses a descriptive phrase; whether this matches the Academy of Ethiopian Languages Amharic Medical Dictionary or the MOH/EFDA approved term is unverifiable from the benchmark alone.
  - [D4] Example 3 (doc_health, split=train): "ተጨማሪ ምግብ ማጠቃሊያ" (complementary feeding) — Specific infant feeding terminology in Amharic; compliance with MOH approved nutrition terminology cannot be assessed.
  - [D21] Example 4 (doc_health, split=train): "Antimicrobial resistance ... AMR threatens the effective prevention and treatment of an ever-increasing range of infections" — English source with clinical pharmacology terminology that requires verified EFDA-approved Amharic equivalents.

---

#### MAJOR

#### MAJOR Concern 1: A substantial portion of the health corpus covers topics with low direct relevance to Ethiopian MOH clinical priorities
- **Dimension(s):** IC, IO
- **Observation:** While the health corpus is domain-aligned at the level of "WHO health articles," a significant subset covers topics that are either geographically remote from Ethiopia or substantively distant from clinical practice guidelines, vaccination schedules, and maternal-health booklets. In the sampled data: tropical cyclones (Ex. 1, doc_health — [D1]), Crimean-Congo hemorrhagic fever endemic to the Balkans/Central Asia (Ex. 5, doc_health — [D32]), Afghanistan polio campaigns ([D7], [D34]), volcanic eruptions ([D33]), international health financing mechanisms ([D25], [D27], [D28]), TRIPS/IP policy ([D46]), COVID-19 international travel guidance ([D19]), and IHR process documentation ([D20], [D35]). These topics occupy a substantial share of sampled examples.
- **Deployment relevance:** The deployment translates clinical practice guidelines, vaccination schedules, and maternal-health booklets — all of which involve disease-treatment, preventive care, and patient-facing language. Training or fine-tuning a system on the AFRIDOC-MT health corpus, then evaluating it using these examples, will include substantial signal from topics (disaster preparedness, international health law, health financing) that do not appear in the actual deployment document types.
- **Datapoint citations:**
  - [D33] Example 3 (doc_health_25, split=train): "A volcano is a vent in the Earth's crust from which eruptions occur. There are about 1500 potentially active volcanoes worldwide." — WHO volcanic eruption article; not relevant to Ethiopian MOH clinical materials.
  - [D7] Example 1 (doc_health_10, split=train): "ናንጋርሃር እና ኩናር አውራጃዎች ... 1.7 ሚሊዮን ተመላሾች" — Afghanistan polio returnees article; geographic and contextual mismatch with Ethiopia.
  - [D32] Example 5 (doc_health, split=train): "Crimean-Congo haemorrhagic fever (CCHF) ... CCHF is endemic in all of Africa, the Balkans, the Middle East and in Asia." — CCHF hemorrhagic fever; not a primary Ethiopian clinical guideline topic.
  - [D26] Example 4 (doc_health_10, split=train): "Vector control operations framework for Zika virus" — Zika is not endemic in Ethiopia.

#### MAJOR Concern 2: Significant tech corpus included in the benchmark — entirely irrelevant to MOH clinical deployment
- **Dimension(s):** IO
- **Observation:** Approximately half the benchmark data is the tech corpus (`doc_tech`, `doc_tech_5`, `doc_tech_10`, `doc_tech_25`, `tech`), consisting of Techpoint Africa news articles about Nigerian/African technology startups, fintech, cryptocurrency, content regulation, and product management. The sampled examples include articles on Cellulant layoffs [D14], Nestcoin crypto funding [D13], Nigerian VC investment [D22], South Africa online content regulation, and Indian edtech [D38].
- **Deployment relevance:** The deployment is exclusively concerned with health document translation for MOH distribution. Tech-domain data contributes no valid signal for health translation quality and could introduce domain-specific vocabulary and register patterns into fine-tuning or evaluation that actively degrade health translation performance. If researchers evaluate models on the combined benchmark, tech-domain scores would dilute health-domain signals.
- **Datapoint citations:**
  - [D14] Example 2 (doc_tech, split=train): "South Africa wants to stop harmful content online ... YouTube ... NALA launches payments from UK and EU to Nigeria ... Cellulant to lay off 20% of its workforce" — Entirely irrelevant to clinical translation deployment.
  - [D38] Example 1 (doc_tech_10, split=train): "የሕንድ ኢድቴክ ኢንዱስትሪ ... ሕንድ ከዩናይትድ ስቴትስ ... Central Square Foundation" — Indian edtech article in Amharic; no relevance to Ethiopian MOH.
  - [D22] Example 1 (doc_tech_25, split=train): "One benefit Fatanmi identifies is its effect on marketing a business... Gen Zs ... Building in public" — Startup marketing article; entirely irrelevant.

#### MAJOR Concern 3: GPT-4o-as-judge documented as unreliable for Amharic — deployment cannot use it as scalable quality proxy
- **Dimension(s):** OO, OF
- **Observation:** The benchmark documentation explicitly states that GPT-4o produced inconsistent judgments when translating into African languages (Q66, Q67, Q99, Q218, Q219) and that the benchmark consequently deprioritizes it in favor of human DA for African languages. This is independently corroborated by the Walia-LLM study (EMNLP 2024). The data itself — including long clinical Amharic texts such as [D1], [D5], [D43] — cannot be reliably scored by GPT-4o as a judge.
- **Deployment relevance:** The deployment would benefit from a scalable, automated quality-assessment mechanism to evaluate clinical Amharic translations without requiring human clinical translators for every document. The benchmark confirms that GPT-4o-as-judge cannot fill this role for Amharic, and no validated document-level embedding metric (e.g., long-context AfriCOMET) exists for Amharic. This leaves d-chrF/d-BLEU as the primary scalable metrics, which cannot capture MOH/EFDA terminological compliance.
- **Datapoint citations:**
  - [D43] Example 4 (doc_health, split=train): "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ ... 'ሱፐርበግስ(superbugs)'" — A complex clinical sentence with a mixed Amharic/English term; GPT-4o's inconsistent Amharic capabilities mean it cannot reliably judge whether this rendering is acceptable.
  - [D47] Example 5 (doc_health, split=train): "ህክምና፡- ... ፀረ-ቫይረስ መድሃኒት ... ribavirin" — Drug terminology requiring clinical judgment that GPT-4o cannot reliably provide.

#### MAJOR Concern 4: Inter-annotator agreement for Amharic human evaluation is low (α = 0.46), compounding the annotator-credentials gap
- **Dimension(s):** OC
- **Observation:** Even among the benchmark's own Amharic human evaluators, Krippendorff's alpha is 0.46 — the lowest agreement level among the five languages (Yorùbá achieves 0.81). This means the human DA signal for Amharic is noisy even within the benchmark's own framework, before considering whether those annotators represent the deployment's authoritative population (MOH-trained clinical translators). The data cannot reveal why agreement is low — it could reflect genuine translation ambiguity, annotator background differences, or the fine granularity of the 0-100 scale — but it means that even if benchmarking scores are computed, the human evaluation signal has substantial uncertainty for Amharic specifically.
- **Deployment relevance:** The deployment requires confident quality signals for clinical Amharic translations. An inter-annotator agreement of α = 0.46 implies that even if the benchmark's human evaluators were acceptable proxies for MOH translators (which is unverified), approximately half their quality signal would be noise. This compounds the annotator-credentials concern: the reference translation quality signal for Amharic is both uncertain in provenance and noisy in annotation.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): The complex multi-paragraph Amharic cyclones article — exactly the type of document where annotator disagreement on translation quality would be expected, given the technical register and length.
  - [D44] Example 3 (doc_health, split=train): "ጨቅላ ህፃናት ከ6 ወር ጀምሮ የተጣራ፣ የተፈጨ" — Maternal-health clinical instruction where annotator agreement on the correct Amharic rendering of feeding guidance would matter most for the deployment.

---

#### MINOR

#### MINOR Concern 1: Translationese effects visible in Amharic data — English-centric structural patterns may not reflect natural Amharic clinical register
- **Dimension(s):** IC, OC
- **Observation:** The benchmark explicitly acknowledges translationese risk (Q103–Q105). In the sampled Amharic data, English structural patterns appear clearly: parenthetical acronyms like "(AMR)" and "(CCHF)" embedded in Amharic text [D5, D6], English loanwords like "superbugs" (ሱፐርበግስ) with parentheses [D43], and direct transliterations of drug names like "ribavirin" [D47]. The document-level Amharic text in [D1] follows the WHO article's topic-sentence structure closely, which may not reflect how Amharic health writers would naturally organize health guidance.
- **Deployment relevance:** If a system trained/evaluated on AFRIDOC-MT produces translations with English-centric structural patterns (calqued phrasing, parenthetical acronyms, transliterated drug names), these may be judged acceptable by d-chrF (since they match the references) but may be considered unnatural or confusing by MOH clinical translators or semi-literate patients — the actual end-users.
- **Datapoint citations:**
  - [D43] Example 4 (doc_health, split=train): "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ ... 'ሱፐርበግስ(superbugs)'" — English loanword in Amharic parentheses suggests translated-from-English structural dependency.
  - [D47] Example 5 (doc_health, split=train): "ፀረ-ቫይረስ መድሃኒት ... ribavirin" — Untranslated drug name retained in Amharic text.

#### MINOR Concern 2: Sentence-level health config (`health`) contains highly varied content — some items have marginal clinical relevance
- **Dimension(s):** IC
- **Observation:** The `health` (sentence-level) config contains short, standalone sentences that are contextually disconnected from the document-level clinical narrative. Samples include health financing policy [D23], biological therapeutics standardization [D24], blood products [D40], and OCV sentence fragments [D12]. While individually these are within the "health" domain, their standalone nature removes the document context that makes clinical translation meaningful and assessable.
- **Deployment relevance:** Sentence-level evaluation without document context is less relevant for the deployment (clinical practice guidelines, maternal-health booklets) than document-level evaluation. The `doc_health` and chunked configs are better suited to the deployment's needs than the `health` sentence-level config.
- **Datapoint citations:**
  - [D23] Example 2 (health, split=train): "However, what is clear is that health systems need to predominantly rely on public revenue sources: mandatory, pre-paid and pooled" — Health financing sentence lacking clinical guideline register.
  - [D24] Example 3 (health, split=train): "the development and promotion of WHO international reference standards helps ensure that biological therapeutics are standardized between different manufacturers" — Regulatory/technical sentence without clinical patient-facing relevance.

#### MINOR Concern 3: Regional Amharic register variation across Ethiopia's health bureaus is unaddressed — single national-standard reference
- **Dimension(s):** OC
- **Observation:** The benchmark produces a single Amharic reference translation per document (by four translators working independently, with harmonization planned but not confirmed as completed). No sub-national or regional register variation (Tigray, Oromia, Somali, Amhara bureaus) is represented. The translators are identified by name but no regional affiliation is documented.
- **Deployment relevance:** The deployment serves multiple regional health bureaus where Amharic is used as a lingua franca by non-native speakers (Oromia, Tigray, Somali regions). Whether a single Addis Ababa-centric reference translation would be uniformly accepted as ground truth across all bureaus was not resolved in elicitation. This is a lower-severity concern given that Amharic dialects are mutually intelligible, but health register preferences may diverge, particularly for localized disease terminology or administrative terms.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "የሞቃታማ ዐውሎ ነፋሶች" — A single Amharic rendering of "tropical cyclone" — whether this specific vocabulary choice would be accepted by health workers in Somali or Tigray regions is unverifiable.
  - [D4] Example 3 (doc_health, split=train): "ጨቅላ ህፃናት" (infant) — A single Amharic term for infant used consistently in the complementary feeding article; regional health registers may prefer alternative terminology.

---

### Content Coverage Summary

The sampled data contains a mixture of WHO health articles and Techpoint Africa technology news articles, all originating in English with human translations into Amharic, Hausa, Swahili, Yorùbá, and Zulu. The health corpus includes a wide range of WHO topics: maternal/infant nutrition (complementary feeding, breastfeeding), immunization/vaccination (cholera OCV, polio), disability, antimicrobial resistance, infectious diseases (CCHF, AMR), public health emergencies, and health systems governance (health financing, IHR, TRIPS). Medical terminology is present throughout the Amharic translations in Ethiopic script, including clinical terms, drug names (often transliterated), and health systems vocabulary.

Approximately half the sample is tech-domain (Techpoint Africa news), which is entirely irrelevant to the deployment. Within the health corpus, the most deployment-relevant subset — maternal-child health (complementary feeding, infant nutrition, breastfeeding) and immunization articles — constitutes a minority of the total health samples, with health policy, health financing, emergency preparedness, and globally generic disease topics occupying a substantial share. Document-level configs preserve multi-paragraph health articles; the sentence-level config provides shorter, context-free sentence pairs.

Amharic text quality in the available samples appears generally consistent in terms of script rendering and sentence fluency, but translator credential verification and MOH/EFDA terminology compliance cannot be assessed from the data alone.

---

### Limitations

1. **Sample size**: 51 examples were reviewed across 10 configs. The full benchmark contains 28,201 rows; the health domain has ~10,000 sentences and the tech domain ~10,000. The sampled examples provide directional evidence but cannot characterize the full distribution of topics, terminology choices, or translation quality across the entire corpus.

2. **Annotator credentials unverifiable from data**: The data rows themselves contain no metadata about translator credentials. Verification of MOH certification or clinical training background for the four Amharic translators requires direct contact with AFRIDOC-MT authors.

3. **MOH/EFDA glossary compliance unassessable from data alone**: No reference terminology list is included with the benchmark. Verifying whether specific Amharic term choices in the data conform to MOH/EFDA standards requires comparison against those glossaries, which are not publicly accessible in a verified form.

4. **Inter-annotator variation within the four Amharic translators unobservable in this sample**: The benchmark uses one translator per sentence (distributed equally), so single-document rows do not show variance across all four translators for the same passage. This limits assessment of translation consistency.

5. **Translationese extent not quantifiable from inspection**: Whether the Amharic translations exhibit systematic translationese effects (unnatural syntax, calqued phrase structure) requires native-speaker clinical evaluation beyond what visual inspection of the Ethiopic text can determine.

6. **GPT-4o judge output not directly observable**: The benchmark's GPT-4o evaluation results are reported in the paper but the per-document GPT-4o scores are not included in the HuggingFace dataset release, so the inconsistency documented for Amharic cannot be directly observed in the sampled rows.

