## Deployment Context

**Use case:** Use Case: Early identification of damage type caused by a disaster and reported in local news and social media posts from Northwest Argentina, Paraguay and South Bolivia (e.g. Gran Chaco regions).
**Target population:** Target population: National emergency responders, gendarmerie, civil forces, technical practitioners in public emergency sector from Argentina, Bolivia or Paraguay. They all would speak and write in Spanish, Andean variety, and would have an intermediate level of English.

# Validity Analysis: wximpactbench
**Target context:** Gran Chaco Tri-Border Emergency Response Zone
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ⚠ | 1 | Serious concern | high |
| Output Ontology | 2 | Significant gaps | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 3 | Moderate gaps | medium |
| **Average** | **1.5** | | |

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

WXIMPACTBENCH was constructed exclusively from English-language Canadian historical newspaper content with annotation by Canadian academic climate-history researchers. The Gran Chaco Tri-Border Emergency Response deployment requires processing Rio Platense Spanish social media and local news with Guaraní/Quechua/Wichí lexical borrowing, applies consequence-framing-dependent label logic, prioritizes cross-border displacement and indigenous community access disruption, and designates AFE/SINAGIR national coordinators as authoritative labelers — none of which are represented in the benchmark. Five of six dimensions show critical or major mismatches; only the output form structure (multi-label simultaneous binary classification) is reusable. Dataset analysis confirms label-boundary inconsistencies even within the Canadian context (explicit human casualties labeled all-zero in multiple cases), suggesting that the annotation philosophy itself does not match emergency-responder operational salience.

## Practical Guidance

### What This Benchmark Measures

WXIMPACTBENCH measures LLM ability to assign six broad weather-impact categories to formal English-language historical newspaper prose under a Canadian-academic annotation philosophy emphasizing 'explicit mentions' of direct physical effects. The strongest dimension for the deployment is Output Form (score 3): the multi-label simultaneous binary classification output structure aligns with the minimum acceptable deployment output, and dataset analysis confirms the schema is operationally usable. The benchmark also provides a documented six-category template that, with significant adaptation, could serve as a starting point for Gran Chaco taxonomy design.

### Construct Depth

Construct depth is shallow for the deployment context. The benchmark probes one slice of disaster-impact understanding — English formal-prose multi-label classification — without addressing input register diversity (Spanish social media), regional language phenomena (indigenous lexical borrowing), regional event types (locust outbreaks, Chaco fires, cross-border displacement), or annotator-population validity (AFE/SINAGIR coordinators absent). Even within its construct, the dataset reveals label-boundary inconsistencies (D6, D9, D16, D18) and missing IAA documentation that limit how confidently any score can be interpreted as a measure of impact-classification competence. The benchmark provides almost no transferable evidence about how a model would perform on the deployment's actual input distribution.

### What Else You Need

The benchmark cannot stand alone for this deployment. Required supplementation: (a) construct a Spanish-language Gran Chaco disaster social media evaluation set with AFE/SINAGIR-coordinator-validated labels (addresses IC, IF, OC); (b) extend or redesign the impact taxonomy to include cross-border displacement, indigenous-community-access disruption, locust outbreaks, and Chaco fires (addresses IO, OO); (c) define role-differentiated evaluation metrics distinguishing field-gendarme precision needs from national-coordinator aggregate recall (addresses OF); (d) evaluate Spanish social-media-tuned models (e.g., RoBERTuito [WEB-11]) alongside multilingual LLMs in the deployment register; (e) document inter-annotator agreement and consequence-framing decision rules for the regional taxonomy.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark's six impact categories (Infrastructural, Political, Financial, Ecological, Agricultural, Human Health) and 15 LDA-derived weather event types were derived exclusively from Canadian newspaper content [Q11, Q101]. The Gran Chaco deployment requires categories that capture cross-border displacement along the Pilcomayo and Bermejo rivers, indigenous community access disruption, locust outbreaks, Chaco fires (incendios), and strategic economic route disruption — none of which are represented in the benchmark's taxonomy or sampled data. The deployment user explicitly identified these as primary disaster news categories, and the regional context confirms locust outbreaks and cross-border displacement are 'ABSENT from wximpactbench'. Dataset analysis confirms the Political category is operationalized via Canadian municipal exemplars (e.g., snow-removal budget debates [D10]) with no border-integrity analog.

**Strengths:**
- Six broad impact categories nominally subsume flooding and fire damage descriptions, providing partial coverage of generic disaster consequences [Q11, Q25]
- Multi-label structure allows a single event to attract multiple labels simultaneously [Q28], which is structurally compatible with consequence-framing-dependent assignment even though the specific labels do not match
- Dataset confirms multi-label co-occurrence works in practice (e.g., infra+pol+fin assigned together [D10])

**Checklist:**

- **IO-1**: Required regional categories include riverine flooding with cross-border displacement, locust outbreaks, Chaco fires, dirt-road access disruption to indigenous communities, agrarian supply chain interruption, and border integrity concerns [WEB-5, WEB-1, WEB-2]. — _Sources: WEB-5, WEB-1, WEB-2, WEB-6_
- **IO-2**: Yes — the regional YAML explicitly identifies locust outbreaks and cross-border displacement as ABSENT from the benchmark's 15 weather event types and impact category definitions. Dataset analysis confirms no Southern Cone or border-integrity exemplars in 31 sampled examples [D10, D18, D19]. — _Sources: Q11, Q101, WEB-5, D10, D18, D19_
- **IO-3**: The 15 LDA-derived weather event types are Canadian-newspaper-derived [Q97, Q101] and include urban North American snowstorm/blizzard event types (e.g., 1894 blizzard [D3], Quebec ice storm [D9], Montreal municipal snow removal [D10]) that are not weather event types relevant to the semi-arid Gran Chaco context. — _Sources: Q97, Q101, D3, D9, D10_
- **IO-4**: Critical content validity gaps: (a) no cross-border displacement category, (b) no locust outbreak event type, (c) no Chaco fire event type, (d) no indigenous-community-access damage type, (e) no consequence-framing mechanism for ambiguous multi-label assignment as practiced by Gran Chaco coordinators. — _Sources: Q140, WEB-5, D10, D18_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q11] 'The articles are selected by topic modeling, including six impact categories (infrastructural, political, financial, ecological, agricultural, and human health), which are informed by previous studies (Imran et al., 2016a) and align with modern disaster impact assessment frameworks (Silva et al., 2022).' (p.2)
- [Q97] 'Our primary data source is a corpus of three digitized newspapers (La Presse, La Patrie and Montreal Gazette), obtained through collaboration with the McGill University Library and Archives and the Bibliothèque nationale du Québec.' (p.9)
- [Q101] 'Using Latent Dirichlet Allocation, the dataset was categorized into 15 primary weather event types.' (p.14)
- [Q140] 'Political Impact: Evaluates governmental and policy responses to weather events. Includes government decision-making and policy changes; shifts in public opinion or political discourse; effects on electoral processes; international aid and relations; and debates on disaster preparedness and response.' (p.19)

*Web sources:*
- [WEB-5] 2018 Pilcomayo flood displaced more than 20,000 inhabitants and triggered cross-border response coordination
- [WEB-1] Paraguayan Chaco departments declared under national emergency Ley Nº 7471/2025 for flooding
- [WEB-2] Route No. 12 along the Pilcomayo is impassable when raining — primary infrastructural concern absent from benchmark
- [WEB-6] Pilcomayo basin spans ~50,000 km² with cross-border community coordination needs

*Dataset analysis:*
- DATASET-D10: Political label operationalized via 1887 Montreal municipal snow-removal budget debate — no border-integrity or cross-border-displacement analog in benchmark exemplars
- DATASET-D19: Ecological label operationalized via US Everglades drought — no Chaco fire or locust ecological exemplar
- DATASET-D18: Mediterranean flash flood labeled political+ecological but not infrastructural despite cars swept away — confirms Canadian-academic boundary logic that diverges from Gran Chaco operational framing

</details>

**Information gaps:**
- No publicly available Spanish-language disaster impact NLP benchmark exists for any Southern Cone context against which to compare wximpactbench's gaps quantitatively

**Requires expert verification:**
- AFE/SINAGIR national coordinators should confirm whether the six categories, even with definitional expansion, are operationally adequate or whether additional categories (e.g., a dedicated Border Integrity category) are required

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark's entire input corpus is English-language formal newspaper prose from three Canadian newspapers (La Presse, La Patrie, Montreal Gazette) accessed via McGill University Library and the Bibliothèque nationale du Québec [Q97]. Dataset analysis confirmed every one of 31 sampled examples is English Canadian newspaper content; no Spanish, no social media, no indigenous-language toponyms, no Southern Cone references. The deployment requires Rio Platense Spanish social media and local news with Guaraní/Quechua/Wichí lexical borrowing [WEB-7, WEB-9, WEB-10]. The benchmark explicitly acknowledges potential biases in 'underrepresented historical events and linguistic variations' [Q90] but does not extend to Spanish-language or Southern Cone content. The regional context confirms no Spanish-language disaster NLP benchmark exists for this region.

**Strengths:**
- Two temporal periods (historical 1880s–1890s; modern 1990s–2000s) provide some intra-corpus register variation [Q13, D3, D16]
- Some non-Canadian wire-service content (China, Indonesia, US, Europe) appears in the labeled data [D7, D8, D16, D19], showing the corpus is not strictly Canadian — though still not Southern Cone

**Checklist:**

- **IC-1**: Yes — deployment inputs require knowledge of Rio Platense Spanish dialectal features, Guaraní/Quechua/Wichí toponyms (Pilcomayo, Bermejo, Tartagal, Yacuiba), and Paraguayan Jopara mixed register [WEB-7, WEB-9]; benchmark provides none of this [D1–D22 all English]. — _Sources: Q97, WEB-7, WEB-9, D1, D3_
- **IC-2**: No — benchmark content reflects North American journalistic culture (e.g., Montreal municipal snow removal [D10], US Everglades policy [D19]) rather than Southern Cone disaster-response culture [Q97]. — _Sources: Q97, D10, D19_
- **IC-3**: Yes — content frequently requires understanding of Canadian/US institutional context (Toronto electric car services [D3], Quebec ice storm [D9], US Supreme Court [D22], Berlin Wall anniversary [D5]) that does not transfer to Gran Chaco deployment. — _Sources: D3, D9, D22, D5_
- **IC-4**: Regional annotator recruitment has not occurred; no AFE/SINAGIR, SEN, VIDECI, or Gendarmería personnel were involved in benchmark construction [Q110]. — _Sources: Q110_
- **IC-5**: Critical content validity violation: zero linguistic, geographic, or cultural overlap between benchmark inputs and deployment input distribution; results from this benchmark cannot be transferred to predict performance on Gran Chaco Spanish social media. — _Sources: Q90, WEB-5, WEB-11, D11_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q97] 'Our primary data source is a corpus of three digitized newspapers (La Presse, La Patrie and Montreal Gazette), obtained through collaboration with the McGill University Library and Archives and the Bibliothèque nationale du Québec.' (p.9)
- [Q90] 'Although WXIMPACTBENCH provides valuable insights... it may have potential biases in underrepresented historical events and linguistic variations.' (p.9)
- [Q13] 'We extract a sample of articles from two time periods, which cover linguistic and social changes across different eras...' (p.2)
- [Q49] 'Eventually, we contain 350 and 1,386 samples for the original and mixed context version datasets, respectively.' (p.6)

*Web sources:*
- [WEB-7] Rio Platense Spanish is the predominant variety in Argentina/Uruguay extending to Paraguay and border regions
- [WEB-9] 2025 survey confirms NLP resources for Argentine indigenous languages (Wichí, Toba/Qom, Guaraní) are lacking
- [WEB-10] No mixed-language disaster classification tools exist for Guaraní/Quechua/Wichí lexical borrowing within Spanish
- [WEB-11] RoBERTuito Spanish social-media model exists but has no disaster-domain or Gran Chaco evaluation
- [WEB-5] Gran Chaco PROADAPT confirms informal social networks are the primary disaster information channel in the zone

*Dataset analysis:*
- DATASET-D1: English-language weather forecast tabular data — register entirely incompatible with Spanish social media
- DATASET-D3: 1894 blizzard article in formal English with archaic vocabulary ('despatches') — no register overlap with Rio Platense Spanish
- DATASET-D11: OCR-degraded English stock ticker confirms even negative examples are English formal media, not Spanish social media
- DATASET-D7: Yangtze River flood content — closest river-flood analog but in English Canadian wire service, with consequences (urban industrial scale) bearing no resemblance to Pilcomayo/Bermejo operational priorities

</details>

**Information gaps:**
- No quantitative characterization of actual Gran Chaco disaster social media token-length and lexical-borrowing distribution exists; would require corpus collection from regional platforms

**Requires expert verification:**
- Regional annotators (AFE/SINAGIR coordinators, SEN, VIDECI personnel) should validate which proportion of routine deployment inputs contain indigenous-language lexical borrowing requiring specialized handling

---

### Input Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Benchmark inputs are English-language OCR-corrected historical newspaper prose averaging 2,987 tokens (long-context) or 781 tokens (mixed-context) [Q109]. Models must support 8k token input lengths [Q55] and handle 'outdated terminology, spelling variations, and evolving writing conventions' [Q14]. Deployment requires processing informal Rio Platense Spanish social media (typically 20–280 tokens per post) with platform abbreviations, hashtags, indigenous-language toponyms, and code-switching [WEB-11, regional YAML register_variation]. The noise patterns in the benchmark (OCR column-fragmentation artifacts [D11, D17, D21]) are unrelated to the noise patterns in the deployment (informal orthography, abbreviations like 'tmbn', 'q pasa'). RoBERTuito-class social-media-tuned Spanish models exist [WEB-11] but the benchmark provides no evaluation in that direction.

**Strengths:**
- Mixed-context version with ~250-token chunks [Q46] is closer to deployment token lengths than long-context version
- Benchmark explicitly acknowledges register/style variation matters [Q14, Q32], even though only English historical→modern variation is tested
- Models evaluated must support 8k+ tokens [Q55], which is more than sufficient for short Spanish social media posts

**Checklist:**

- **IF-1**: Significant signal distribution mismatch: English formal newspaper prose vs. Spanish informal social media; OCR-noise vs. social-media-noise; 781–2,987 token articles vs. 20–280 token posts [Q109, Q120, regional register_variation]. — _Sources: Q109, Q120, WEB-11, D3_
- **IF-2**: Deployment infrastructure does not produce OCR-style inputs; it ingests live Twitter/X, Facebook, WhatsApp text streams [WEB-5, regional cultural_norms_notes]. Connectivity in the Gran Chaco is documented as patchy [WEB-5], which affects input freshness but not input form per se. — _Sources: WEB-5_
- **IF-3**: Domain-specific form differences are severe: benchmark cannot evaluate handling of hashtags, platform abbreviations, voseo, indigenous toponyms, or Jopara code-mixing [WEB-9, WEB-10]. — _Sources: Q14, WEB-9, WEB-11, D11_
- **IF-4**: Critical external validity violation: model performance on benchmark's English long-form OCR-corrected prose cannot predict performance on Spanish short-form informal social media posts. — _Sources: Q14, Q32, D11, D21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q14] 'Historical newspapers often employed more descriptive and elaborate narratives compared to modern reporting styles. These narratives frequently included outdated terminology, spelling variations, and evolving writing conventions.' (p.2)
- [Q109] 'The average number of tokens per article is 2987.4 in long-context settings and 781.3 in mixed-context settings.' (p.15)
- [Q46] 'For the long-context impact evaluation, we create an alternate version (mixed context), whose sample length is split into segments with approximately 250 tokens from the original one...' (p.6)
- [Q55] 'The used models for the two tasks cover different sizes and support the input length of at least 8k tokens.' (p.6)
- [Q32] 'Different from them, our constructed samples require the models to understand the linguistic shifts between historical and modern texts and address inconsistent styles of narratives across various periods.' (p.5)

*Web sources:*
- [WEB-11] RoBERTuito (500M+ Spanish tweets) is the most relevant existing model for the deployment's input register, but is not disaster-domain-specific and not regionally evaluated
- [WEB-5] PROADAPT confirms social network communication (informal, short-form) is the primary disaster information channel in the Gran Chaco
- [WEB-9] No NLP tools handle indigenous-language lexical borrowing within Spanish disaster text

*Dataset analysis:*
- DATASET-D11: OCR-degraded financial table 'Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35' — noise pattern unrelated to social media noise
- DATASET-D21: Mixed-context chunk begins with advertisement OCR artifacts ('Q. SIBBALD, 3 WINDSOR HOTEL') — noise type entirely absent from deployment
- DATASET-D3: 1894 formal English narrative with archaic 'despatches' — no orthographic feature shared with informal Spanish social media

</details>

**Information gaps:**
- Empirical token-length and noise-pattern distribution for Gran Chaco disaster social media has not been characterized

**Requires expert verification:**
- A small Spanish-social-media replication study (e.g., evaluating RoBERTuito on Gran Chaco posts) would directly establish form-mismatch impact

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark uses six binary impact labels [Q25, Q117] with detailed Canadian-anchored operational definitions [Q141–Q146] and a multi-label simultaneous classification structure [Q57] that nominally matches the deployment's minimum acceptable output form. However, the boundary logic is misaligned with the consequence-framing-dependent assignment that Gran Chaco national coordinators apply. Dataset analysis reveals visible label boundary inconsistencies even within the Canadian context: 100,000 homes damaged labeled agricultural+health but not infrastructural [D16]; storm with skull-fracture casualty labeled all-zero [D6]; one million people without power labeled all-zero [D9]. The Political category exemplars (municipal snow removal [D10], policy debates [Q140]) lack any border integrity or cross-border displacement framing. The Agricultural category emphasizes Canadian farm-context exemplars [Q136, Q142] without dirt-road access disruption to indigenous communities. Score is 2 (not 1) because the multi-label binary structure itself is reusable and partially aligned with deployment needs.

**Strengths:**
- Multi-label simultaneous binary structure [Q57, Q117] matches the deployment's minimum acceptable output form
- Each sample may carry multiple labels simultaneously [Q28, D10] — structurally compatible with consequence-framing where one event attracts multiple labels
- Detailed operational definitions exist [Q135–Q146], providing a starting template that could be adapted/expanded for Gran Chaco contexts

**Checklist:**

- **OO-1**: Six labels nominally cover broad disaster consequences but operationalize them via Canadian exemplars [Q141–Q146]; boundary logic does not match Gran Chaco consequence-framing [regional consequence_framing_dependency]. — _Sources: Q25, Q117, Q141, Q147, D10_
- **OO-2**: Missing categories: cross-border displacement (regional-priority, ABSENT), border integrity (ABSENT), indigenous-community-access disruption, strategic economic route disruption, locust outbreaks. Confirmed by [WEB-5, WEB-1] and dataset gap [D10, D18]. — _Sources: WEB-5, WEB-1, D10, D18_
- **OO-3**: Political category encodes North American policy/governance assumptions (municipal budget debates, electoral processes) [Q140, D10]; Ecological category centers North American ecosystems (Everglades [D19]); neither encodes Southern Cone or border-region values. — _Sources: Q140, D10, D19_
- **OO-4**: Stakeholder-driven taxonomy redesign would be required: AFE/SINAGIR, SEN, and VIDECI national coordinators would need to define operational labels reflecting consequence-framing logic [WEB-16, WEB-20, WEB-22]. — _Sources: WEB-16, WEB-20, WEB-22_
- **OO-5**: Structural validity is compromised by the operational definitions; content validity is compromised by missing categories; external validity is compromised by definitional drift between Canadian and Gran Chaco framings. — _Sources: Q57, Q147, D16, D18_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'Six vulnerability-related disruptive weather impacts are defined as the labeling categories, including Infrastructural, Political, Financial, Ecological, Agricultural, and Human Health.' (p.4)
- [Q117] 'The classification task is binary (true/false), requiring the model to identify whether the text explicitly mentions any of the defined impacts.' (p.16)
- [Q140] 'Political Impact: Evaluates governmental and policy responses to weather events...' (p.19)
- [Q141] 'Infrastructural Impact: Classify as 'true' if the text mentions any damage or disruption to physical infrastructure and essential services...' (p.20)
- [Q147] 'Return 'false' for any impact category that is either not present in the text or not related to weather events. Base classifications on explicit mentions in the text. Focus on direct impacts rather than implications.' (p.20)
- [Q57] 'Different from traditional methods that decompose multi-label text classification into multiple binary classification tasks..., we simultaneously identify all relevant disruptive weather impacts for each input by calling the LLM once.' (p.6)

*Web sources:*
- [WEB-5] Cross-border displacement and indigenous community evacuation are primary Gran Chaco disaster consequences (10,000+ Wichí/Toba/Chorote/Tapiete evacuated in 2018)
- [WEB-1] Paraguayan emergency Ley Nº 7471/2025 frames flood emergency at the departmental level — political framing absent from benchmark exemplars
- [WEB-16] AFE/SINAGIR is the current Argentine national authority structure for emergencies — not represented in benchmark

*Dataset analysis:*
- DATASET-D10: Political+Financial+Infrastructural multi-label correctly assigned to municipal snow-removal debate — confirms multi-label mechanics work but exemplifies Canadian-municipal framing
- DATASET-D16: 100,000 homes damaged labeled agricultural+health but not infrastructural — boundary logic that would not match Gran Chaco coordinator framing
- DATASET-D18: Mediterranean flash flood with cars swept away labeled political+ecological but not infrastructural — confirms inconsistent boundary logic
- DATASET-D19: US Everglades drought as the canonical Ecological exemplar — no Chaco fire or locust analog

</details>

**Information gaps:**
- Gran Chaco consequence-framing logic has not been formally documented as an annotation guideline

**Requires expert verification:**
- AFE/SINAGIR national coordinators should review the six-category definitions and propose extensions or replacements

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Annotation was conducted by three Canadian academic researchers from a research group specializing in 'uncovering the history of a region's climate change through the regional historical weather records' [Q110, Q26], reviewed by meteorological experts [Q104]. No inter-annotator agreement statistics are reported. The deployment user designated AFE/SINAGIR national coordinators in Buenos Aires as the authoritative ground-truth labelers — a population with zero representation in the annotation process. The guidelines emphasize 'direct and immediate effects and explicit references' [Q118], an annotation philosophy that produced visible label-correctness concerns in the dataset: explicit weather-caused human casualties labeled all-zero [D6, D20], one million people without power/heat labeled all-zero [D9]. Under Gran Chaco consequence-framing logic [regional consequence_framing_dependency], these would attract Human Health and Infrastructural labels. The benchmark itself acknowledges interpretation 'might be influenced by demographic and contextual factors' [Q96]. Convergent and external validity are severely compromised.

**Strengths:**
- Annotation guidelines were reviewed by meteorological domain experts [Q104, Q105]
- The same guidelines are embedded in LLM prompts [Q106], creating internal consistency between human and model expectations within the Canadian context
- Mixed-context chunks were independently annotated rather than inheriting parent-article labels [Q47, Q48], which is a methodologically careful choice that produces meaningful negative examples

**Checklist:**

- **OC-1**: No — labels reflect Canadian academic historical-climate researchers' interpretations [Q110]; AFE/SINAGIR, SEN, and VIDECI emergency coordinators have zero representation [WEB-16, WEB-20, WEB-22]. — _Sources: Q26, Q110, WEB-16, WEB-20, WEB-22_
- **OC-2**: Substantial disagreement is empirically demonstrable from dataset analysis: D6 (storm casualty labeled all-zero), D9 (1M without power labeled all-zero), D20 (sailors suffering severely from cold labeled all-zero) — all would likely be re-labeled by Gran Chaco emergency coordinators applying operational salience. — _Sources: Q118, D6, D9, D20_
- **OC-3**: Annotator demographics: three domain experts from a research group on regional historical climate [Q110, Q26]; no demographic breakdown beyond academic specialization; no datasheet-style documentation. — _Sources: Q26, Q110_
- **OC-4**: Re-annotation by representative AFE/SINAGIR and SEN coordinators on a Spanish-language regional sample is necessary for any deployment-relevant validity claim. — _Sources: WEB-16, WEB-20_
- **OC-5**: No inter-annotator agreement reported; aggregation method is not described in detail; minority-perspective erasure is unmeasurable. — _Sources: Q47, Q96_
- **OC-6**: Critical convergent validity (labels do not correlate with regional stakeholder perspectives) and external validity (Canadian academic judgments do not generalize to Gran Chaco operational context) violations. — _Sources: Q96, Q118, D6, D9, D16_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q26] 'Annotation is conducted by three domain annotators following our guidelines (provided in Appendix B.2.2).' (p.4)
- [Q104] 'To ensure high-quality and consistent annotations, the task was conducted using a set of specific instructions reviewed by meteorological experts.' (p.15)
- [Q110] 'The annotation process was conducted by members of a research group specializing in uncovering the history of a region's climate change through the regional historical weather records.' (p.15)
- [Q118] 'The guidelines emphasize focusing on direct and immediate effects, ensuring that classifications are based solely on explicit references within the text.' (p.16)
- [Q96] 'The interpretation of weather-related disruptions in historical newspapers might be influenced by demographic and contextual factors, which is similar to other text datasets generated through crowd-sourcing with inherent challenges in ensuring that dataset labels are fully representative of diverse societal perspectives (Talat et al., 2022).' (p.9)
- [Q47] 'Note that annotations for these smaller chunks are performed independently by the same domain experts rather than automatically inherited from the original articles.' (p.6)

*Web sources:*
- [WEB-16] AFE/SINAGIR is the current Argentine national authority — designated as authoritative labelers by deployment user, with zero benchmark representation
- [WEB-20] SEN (Paraguay) coordinates emergencies in all three Chaco departments — also unrepresented
- [WEB-22] VIDECI (Bolivia) operates departmental representation in Tarija — also unrepresented

*Dataset analysis:*
- DATASET-D6: Storm with skull-fractured passenger and child casualty labeled all-zero — explicit casualty annotation gap
- DATASET-D9: 1998 Quebec ice storm with one million people without power/heat labeled all-zero — major infrastructure event missed under 'explicit mentions' interpretation
- DATASET-D20: Sailors suffering severely from cold after capsizing labeled all-zero — direct weather-caused harm not labeled
- DATASET-D16: 100,000 homes damaged labeled agricultural+health but not infrastructural — inconsistent boundary application

</details>

**Information gaps:**
- No inter-annotator agreement statistics; no annotator demographic breakdown beyond research-group specialization

**Requires expert verification:**
- A re-annotation pilot in which AFE/SINAGIR coordinators re-label a sample of benchmark items would empirically establish the convergent-validity gap

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
The benchmark's multi-label simultaneous binary classification output [Q57, Q117] aligns with the deployment's minimum acceptable output form. Dataset analysis confirms the schema produces compact six-binary label vectors per row [D3, D10], operationally usable for national coordinator dashboards. However, the evaluation framework has notable gaps: F1, accuracy, and row-wise accuracy [Q43, Q45] aggregate across categories and do not differentiate field-gendarme rapid-lookup needs from national-coordinator aggregate-situational-awareness needs. The ranking-based QA task — which the deployment user explicitly rejected as insufficiently reliable for direct operational use — is a substantial portion of the benchmark [Q3, Q15] and includes a known self-referential bias when GPT-4O is both question generator and ranker [Q88]. No confidence scores or probability distributions are produced, although the user indicated these would be useful for human-review-mediated workflows. Score is 3 (mixed) because the classification output structure is genuinely usable, but evaluation-framework relevance to the role-differentiated deployment is partial.

**Strengths:**
- Multi-label simultaneous binary output [Q57] is the minimum acceptable form for the deployment
- Dataset confirms compact binary-vector schema works in practice [D3, D10]
- Standard, well-known classification metrics (F1, accuracy) [Q43] are interpretable by the deployment team
- Modest computational requirements [Q126, Q128] make local replication feasible for deployment teams

**Checklist:**

- **OF-1**: Output modality (text-based binary multi-label) matches deployment need for simultaneous classification [Q57], but does not provide confidence scores requested for human-review-mediated workflows. — _Sources: Q57, Q117, D3, D10_
- **OF-2**: Not applicable — speech-based output is not a deployment requirement.
- **OF-3**: Not directly applicable to text-classification output. Literacy of operators is not in question; the user noted intermediate English proficiency for technical practitioners (system operates in Spanish) [regional english_proficiency].
- **OF-4**: Partial external validity gap: F1 and row-wise accuracy [Q43, Q45] do not distinguish field-gendarme rapid-lookup precision needs from national-coordinator aggregate-recall needs; ranking task evaluation is not deployment-relevant per user [regional output_format_requirements]. — _Sources: Q43, Q45, Q50, Q88_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q43] 'For multi-label classification task, we use F1-score, accuracy, and row-wise accuracy as evaluation metrics.' (p.6)
- [Q45] 'Compared to the common F1-score and accuracy, the row-wise accuracy is a strict metric that requires more accurate output as the model should correctly classify all six impact labels for a given article.' (p.6)
- [Q57] 'we simultaneously identify all relevant disruptive weather impacts for each input by calling the LLM once.' (p.6)
- [Q88] 'Notice that the ranking results would contain bias when the evaluated model is used for question generation (GPT-4O in our cases). This is a common phenomenon (Zhou et al., 2023) and needs to be avoided in benchmarking.' (p.9)
- [Q117] 'The classification task is binary (true/false)...' (p.16)
- [Q50] 'For the ranking-based QA task, we deploy the standard metric that emphasizes the accuracy of top positions for evaluation, including Hit@1, nDCG@5, Recall@5, and MRR.' (p.6)

*Dataset analysis:*
- DATASET-D3: Single-label assignment (infra=1) demonstrates compact binary-vector output works
- DATASET-D10: Multi-label assignment (infra+pol+fin) confirms simultaneous multi-label output structure operationally usable

</details>

**Information gaps:**
- Whether benchmark-style F1 scores predict trust-in-output for field gendarmes vs. national coordinators is unmeasured; no role-differentiated evaluation exists

**Requires expert verification:**
- AFE/SINAGIR coordinators should specify whether per-class precision floors or aggregate recall ceilings are operationally binding metrics

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Six categories and 15 weather event types are Canadian-derived; cross-border displacement, locust outbreaks, Chaco fires, and indigenous-community-access disruption are absent.

**Recommendation:** Convene an AFE/SINAGIR–SEN–VIDECI working group to extend the taxonomy with at minimum: a Border Integrity / Cross-Border Displacement category; locust outbreak and Chaco fire weather event types; an indigenous-community-access subdimension within Infrastructural and Human Health categories.

### Input Content ⚠

**Gap:** Zero Spanish-language, social-media, or Southern Cone content; no indigenous-language lexical-borrowing exemplars.

**Recommendation:** Construct a Gran Chaco Spanish-language evaluation corpus from Twitter/X, Facebook community groups, WhatsApp broadcast channels, and local news archives spanning Salta/Formosa/Chaco/Boquerón/Alto Paraguay/Presidente Hayes/Tarija; include an indigenous-toponym/lexical-borrowing test slice.

### Input Form ⚠

**Gap:** Benchmark form is English long-form OCR-corrected prose; deployment form is short Spanish social media with informal orthography and code-mixing.

**Recommendation:** Pilot RoBERTuito and multilingual LLMs on a Spanish social-media disaster classification task, using token-length and noise-pattern distributions matching deployment inputs; report results separately from wximpactbench scores.

### Output Content ⚠

**Gap:** Annotators are Canadian academic climate-history researchers; no AFE/SINAGIR/SEN/VIDECI representation; no IAA reported; visible label-correctness concerns even within Canadian context.

**Recommendation:** Recruit AFE/SINAGIR national coordinators and SEN/VIDECI departmental representatives as authoritative annotators for a regional re-annotation pilot; report inter-annotator agreement statistics; publish a Datasheet documenting annotator demographics and consequence-framing guidelines.

### Output Form

**Gap:** Aggregate F1/row-wise accuracy metrics do not distinguish field-gendarme precision needs from national-coordinator aggregate-recall needs; no confidence scores produced.

**Recommendation:** Define role-differentiated evaluation metrics: per-event precision floors for field gendarme rapid-lookup; aggregate per-category recall and calibrated multi-event coverage for national coordinators; expose model probability distributions to support human-in-the-loop review.

### Output Ontology

**Gap:** Label boundaries operationalized via Canadian exemplars; consequence-framing-dependent assignment is unsupported.

**Recommendation:** Rewrite operational definitions ([Q141–Q146]) with Gran Chaco exemplars elicited from AFE/SINAGIR/SEN/VIDECI coordinators; explicitly document consequence-framing decision rules for ambiguous multi-label cases (e.g., flooded dirt road blocking access to indigenous community).

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we first develop a disruptive weather impact dataset with a four-stage well-crafted construction pipeline." |
| Q2 | 1 | input_ontology | "we propose WXIMPACTBENCH, the first benchmark for evaluating the capacity of LLMs on disruptive weather impacts." |
| Q3 | 1 | input_ontology | "The benchmark involves two evaluation tasks, multi-label classification and ranking-based question answering." |
| Q4 | 1 | input_content | "The climate-related events stored in regional newspapers record how communities adapted and recovered from disasters." |
| Q5 | 1 | input_form | "However, the processing of the original corpus is non-trivial." |
| Q6 | 1 | output_form | "Extensive experiments on evaluating a set of LLMs provide first-hand analysis of the challenges in developing the understanding of disruptive weather impact and climate change adaptation systems." |
| Q7 | 1 | output_content | "Yongan Yu1, Qingchen Hu1, Xianda Du2, Jiayin Wang3, Fengran Mo4∗, Renée Sieber1*" |
| Q8 | 1 | output_content | "1McGill University, 2University of Waterloo, 3Tsinghua University, 4University of Montreal" |
| Q9 | 1 | input_form | "the challenge of identifying impacts and responses often lies in climate-related text processing, which contains period-specific narratives and domain-specific linguistic phenomena." |
| Q10 | 1 | input_form | "This polysemy occurs commonly in newspapers and thus requires the system to distinguish the literal weather-related meanings and alternate usages by improving the" |
| Q11 | 2 | input_ontology | "The articles are selected by topic modeling, including six impact categories (infrastructural, political, financial, ecological, agricultural, and human health), which are informed by previous studies (Imran et al., 2016a) and align with modern disaster impact assessment frameworks (Silva et al., 2022)." |
| Q12 | 2 | input_content | "We design a four-stage data construction pipeline that begins with a disruptive weather impact dataset in which we correct OCR errors in digitalized newspaper article extraction." |
| Q13 | 2 | input_content | "We extract a sample of articles from two time periods, which cover linguistic and social changes across different eras and increase linguistic complexity due to the different descriptions of weather events in different times (Campbell, 2013)." |
| Q14 | 2 | input_form | "Historical newspapers often employed more descriptive and elaborate narratives compared to modern reporting styles (Bingham, 2010). These narratives frequently included outdated terminology, spelling variations, and evolving writing conventions (Campbell, 2013)." |
| Q15 | 2 | input_ontology | "With our constructed dataset, we develop a benchmark, WXIMPACTBENCH, to investigate the capacity of LLMs to understand disruptive weather impacts with two tasks: i) multi-label classification and ii) ranking-based question-answering." |
| Q16 | 2 | output_ontology | "The multi-label classification task employs the previous six impact categories as labels for each article whose ground-truth is annotated by human labor." |
| Q17 | 2 | input_ontology | "The question and the candidate pools for the ranking-based question-answering task are constructed based on the context and annotation of the multi-label classification task." |
| Q18 | 2 | input_ontology | "Climate impact analysis (Thulke et al., 2024) aims to help society make correct decisions about climate-related challenges affecting communities, e.g., understanding the weather impacts on society." |
| Q19 | 3 | input_form | "The construction of the dataset aims to obtain high-quality text samples. The pipeline overview is presented in Figure 2, which consists of four stages: data collection, post-OCR correction, topic-aware article selection, and manual label annotation." |
| Q20 | 3 | input_content | "The data is obtained through collaboration with a proprietary archive institution covering two temporal periods. The original data stored as digitalized text is obtained through OCR (Cheriet et al., 2007), which contains 4018" |
| Q21 | 3 | input_ontology | "Our WXIMPACTBENCH benchmark aims to evaluate to what extent existing LLMs can understand disruptive weather impacts, which also shows the evolution of vulnerability and resilience strategies from society across various periods. It involves two main stages: i) dataset construction; and ii) task definition and evaluation." |
| Q22 | 3 | input_form | "Extracting and processing historical climate articles in newspapers is challenging due to their non-digital formats, such as scanned images or physical archives. OCR enables their conversion into machine-readable text (Baird, 2004), facilitating large-scale digitization, retrieval, and analysis." |
| Q23 | 3 | input_form | "Although neural OCR correction models (Drobac and Lindén, 2020) improve the quality of the extracted text, the degraded print quality, inconsistent terminology, and irregular column layouts (Binmakhashen and Mahmoud, 2019) cause potential errors, which negatively impact the text understanding and the usage for designing downstream tasks (Bingham, 2010; Spathis and Kawsar, 2024; Wang et al., 2024)." |
| Q24 | 3 | input_content | "Thus, the lack of high-quality resources constrains the development of comprehensive benchmarks for weather impacts." |
| Q25 | 4 | output_ontology | "Six vulnerability-related disruptive weather impacts are defined as the labeling categories, including Infrastructural, Political, Financial, Ecological, Agricultural, and Human Health." |
| Q26 | 4 | output_content | "Annotation is conducted by three domain annotators following our guidelines (provided in Appendix B.2.2)." |
| Q27 | 4 | output_ontology | "According to the guidelines, the annotators should assign binary labels to indicate the presence or absence of direct descriptions of specific impacts within each article." |
| Q28 | 4 | output_ontology | "Unlike previous study (Imran et al., 2016a), however, each sample might correspond to more than one impact." |
| Q29 | 4 | input_ontology | "The overview is shown in Figure 4, which contains two tasks, multi-label classification and ranking-based question-answering, to evaluate the capacity of LLMs to understand disruptive weather impacts." |
| Q30 | 4 | input_ontology | "With the annotated weather impact category for each selected article, the intuitive evaluation task is multi-label classification, which aims to test the ability of LLMs to distinguish the disruptive weather impact for each given article." |
| Q31 | 4 | output_content | "Selected articles with informative weather content are manually reviewed by three domain experts, which result in 350 high-quality samples." |
| Q32 | 5 | input_form | "Different from them, our constructed samples require the models to understand the linguistic shifts between historical and modern texts and address inconsistent styles of narratives across various periods." |
| Q33 | 5 | output_ontology | "Specifically, given an article sample xt corresponding to six ground-truth impacts Yt = {y^i_t}^6_i=1 with binary labels y^i_t ∈ {0, 1}, the evaluated model M is required to maximize the probability of the predicated impact Ŷ_t = {ŷ^i_t}^6_i=1 towards ground-truth." |
| Q34 | 5 | output_form | "The objective function L for the given sample xt of multi-label classification task is formulated as L(Ŷ_t, Yt) = −∑^6_i=1 yi log ŷi, ŷi = M(xt)" |
| Q35 | 5 | input_ontology | "Question-answering (QA) requires the LLMs to reply to the given question based on their parametric knowledge." |
| Q36 | 5 | input_ontology | "We formulate the ranking-based QA task by prompting the models to identify the likelihood of each article containing the correct answer from a candidate pool." |
| Q37 | 5 | output_form | "This setting could also facilitate RAG systems development in the domain (Mao et al., 2024; Mo et al., 2024c, 2025), where we left the answer span extraction/generation for future studies." |
| Q38 | 5 | output_content | "To construct an evaluation protocol, the first step is to obtain suitable question pairs with each annotated samples in the multi-label classification task, since the question set is unavailable." |
| Q39 | 5 | input_form | "Thus, we generate pseudo questions qt for each article (xt, Yt) based on its annotated category via a generative LLM G which is formulated as qt = G(xt, Yt)." |
| Q40 | 5 | output_ontology | "The annotated categories Yt, which are the societal impacts brought by the disruptive weather event, will become part of the prompt to ensure the generated question targets one of the specific impact categories (see Figure 4)." |
| Q41 | 5 | input_form | "As a result, we have QA pair (qt, xt) for each sample." |
| Q42 | 5 | input_content | "The next step is to construct the candidate pool for ranking." |
| Q43 | 6 | output_form | "For multi-label classification task, we use F1-score, accuracy, and row-wise accuracy as evaluation metrics." |
| Q44 | 6 | output_form | "The evaluation via F1-score and accuracy are averaged across the six impact categories, historical and modern articles, and the effect of different context lengths." |
| Q45 | 6 | output_form | "Compared to the common F1-score and accuracy, the row-wise accuracy is a strict metric that requires more accurate output as the model should correctly classify all six impact labels for a given article." |
| Q46 | 6 | input_form | "For the long-context impact evaluation, we create an alternate version (mixed context), whose sample length is split into segments with approximately 250 tokens from the original one (long-context version) following (Levy et al., 2024)." |
| Q47 | 6 | output_content | "Note that annotations for these smaller chunks are performed independently by the same domain experts rather than automatically inherited from the original articles." |
| Q48 | 6 | output_content | "This independent annotation process naturally results in some chunks containing no weather impact labels, which serve as valuable negative examples in our evaluation." |
| Q49 | 6 | input_content | "Eventually, we contain 350 and 1,386 samples for the original and mixed context version datasets, respectively." |
| Q50 | 6 | output_form | "For the ranking-based QA task, we deploy the standard metric that emphasizes the accuracy of top positions for evaluation, including Hit@1, nDCG@5, Recall@5, and MRR." |
| Q51 | 6 | input_ontology | "We evaluate a set of off-the-shelf LLMs on WXIMPACTBENCH." |
| Q52 | 6 | input_ontology | "For the multi-label text classification task, we include seven open-source models: DEEPSEEK-V3-671B (DeepSeek-AI, 2024), LLAMA-3.1-8B-INSTRUCT (Llama, 2024), Mistral-7B-Instruct (Jiang et al., 2023), MIXTRAL-8X7B-INSTRUCT (Jiang et al., 2024), MISTRAL-24B-INSTRUCT (Jiang et al., 2024), GEMMA-2-9B-IT (GemmaTeam, 2024), QWEN2.5-7B-INSTRUCT, and QWEN2.5-14B-INSTRUCT (Qwen2.5, 2025); and three closed-source models: GPT-3.5-TURBO, GPT-4 (OpenAI, 2024a), and GPT-4O (OpenAI, 2024b)." |
| Q53 | 6 | input_ontology | "For the ranking-based QA task, we evaluate GPT-3.5-TURBO, QWEN2.5-7B-INSTRUCT, QWEN2.5-14B-INSTRUCT, MISTRAL-7B-INSTRUCT, and LLAMA-3.1-8B-INSTRUCT." |
| Q54 | 6 | output_form | "The relatively smaller models (with 7B size) ensure the latency requirements (Sun et al., 2023)." |
| Q55 | 6 | input_form | "The used models for the two tasks cover different sizes and support the input length of at least 8k tokens." |
| Q56 | 6 | input_form | "The multi-label classification is conducted on each evaluated LLM by the same prompt provided in Appendix C.2." |
| Q57 | 6 | output_ontology | "Different from traditional methods that decompose multi-label text classification into multiple binary classification tasks (Boutell et al., 2004; Liu et al., 2017), we simultaneously identify all relevant disruptive weather impacts for each input by calling the LLM once." |
| Q58 | 6 | input_form | "The example of in-context learning in the one-shot setting is handcrafted with a complex sample detailing multiple impacts." |
| Q59 | 6 | input_content | "We employ GPT-4O for pseudo question generation with default hyper-parameters." |
| Q60 | 6 | output_form | "For ranking evaluation, we adopt the sliding window mechanism within LLM-based ranker implementation following the state-of-the-art study (Sun et al., 2023) to reduce the potential negative effect of noisy long contexts." |
| Q61 | 7 | input_form | "Specifically, each article in the candidate pool was segmented into three chunks, and then the initial ranking was performed independently within each chunk." |
| Q62 | 7 | output_form | "To ensure stable results, following previous studies (Chen et al., 2023), all LLMs were evaluated with the temperature set to 0, and the reported performance is the average value of running the experiments three times." |
| Q63 | 7 | output_form | "Table 1 and Table 2 show the performance of the evaluated LLMs on WXIMPACTBENCH for the settings of categorized by six societal impacts with different context lengths, overall row-wise evaluation, and divided into two periods, respectively." |
| Q64 | 7 | output_form | "LLMs struggle to understand disruptive weather impacts." |
| Q65 | 7 | output_form | "Table 1 shows that the F1-score for multi-label classification remains consistently low across models, especially among the political and ecological categories." |
| Q66 | 7 | output_form | "The financial, agricultural, and human health impacts categories perform slightly better but still exhibit suboptimal results at 55%." |
| Q67 | 7 | output_ontology | "The low performance might be attributed to the challenges in these categories with abstract and context-dependent narratives." |
| Q68 | 8 | output_form | "Table 2 shows row-wise performance, in which the model must identify the given sample correctly for each involved category, the performance of classification drops dramatically due to the more precise requirement." |
| Q69 | 8 | output_ontology | "Thus, a sophisticated model is expected to understand the complex societal effects of historical narratives via reasoning (Wei et al., 2022; Zhang et al., 2025a,b)." |
| Q70 | 8 | output_form | "The results in Table 1 show that, when the original long-context is segmented into smaller chunks, the classification accuracy increases in most cases." |
| Q71 | 8 | input_form | "These improvements suggest that smaller chunks help models focus on relevant information and thus minimizing distraction from extraneous content." |
| Q72 | 8 | input_form | "Even the used models are claimed with long-context capacity, more precise split that reduces potential noise is still effective for context de-noising, which is consistent with previous studies (Sun et al., 2024)." |
| Q73 | 8 | output_form | "However, we also find that this trend is not observed with the row-wise accuracy evaluation." |
| Q74 | 8 | output_form | "This is due to the evaluation bias, where the F1-score measures precision and recall per category, and benefits from partial correctness." |
| Q75 | 8 | output_form | "Row-wise accuracy requires an exact match across all labels." |
| Q76 | 8 | output_form | "The small chunks might be helpful to improve the classification of one of the categories but not enough to correct all labels." |
| Q77 | 8 | output_form | "The in-context learning is achieved by providing one demonstration as the one-shot example for model decision." |
| Q78 | 8 | output_form | "Compared zero-shot and one-shot performance in Table 1, we find that providing a single example in the prompt offers limited benefits and might decrease the performance in some cases." |
| Q79 | 8 | output_ontology | "Such a phenomenon implies that the LLMs lack sufficient knowledge to disambiguate disruptive weather impacts even with enhanced examples for knowledge arousing." |
| Q80 | 8 | output_form | "These results indicate that our WXIMPACTBENCH is challenging for LLMs to understand disruptive weather impact." |
| Q81 | 8 | output_form | "The evaluation of different narratives in terms of historical and modern articles is presented in Table 3." |
| Q82 | 8 | output_form | "Surprisingly, the evaluated models perform better on the articles recorded in the historical period." |
| Q83 | 8 | input_form | "The reason might be the structured and formal narrative style used to report disruptive weather events in historical periods, which more explicitly highlights cause-and-effect relationships." |
| Q84 | 8 | input_form | "The observation is revealed by the earlier studies (e.g., Mauch and Pfister, 2009), where the historical narratives emphasize empirical observations over interpretations, offering a more immediate and naturalistic account of events." |
| Q85 | 8 | input_form | "Though the modern text might dominate within the pre-trained corpus, the language patterns used in historical narrative styles are easier for language models to identify, and thus perform better on classifying disruptive weather impacts." |
| Q86 | 9 | output_form | "larger models usually perform better than smaller ones, which is consistent with the scaling law for LLMs (Kaplan et al., 2020)." |
| Q87 | 9 | output_form | "The performance of each evaluated model for ranking-based QA is reported in Table 4." |
| Q88 | 9 | output_form | "Notice that the ranking results would contain bias when the evaluated model is used for question generation (GPT-4O in our cases). This is a common phenomenon (Zhou et al., 2023) and needs to be avoided in benchmarking." |
| Q89 | 9 | output_form | "The practical open-retrieval setting, i.e., identifying the relevant articles from a huge database, is left for future studies, which could further facilitate knowledge enhancement in understanding disruptive weather impacts." |
| Q90 | 9 | input_content | "Although WXIMPACTBENCH provides valuable insights (e.g., exhibit the strengths and weaknesses of various society impact understanding) about evaluating LLMs on disruptive weather, it may have potential biases in underrepresented historical events and linguistic variations." |
| Q91 | 9 | input_ontology | "Future work could expand the range of evaluated models, strategies, and designed tasks to further strengthen the evaluations." |
| Q92 | 9 | input_content | "Our primary data source is a corpus of historical digitized newspapers, obtained through collaboration with an official organization, which should be anonymous at this moment." |
| Q93 | 9 | input_content | "This organization preserves the copyright of the newspaper articles and has been granted permission to publish this subset of articles for benchmark build-up to facilitate the research community." |
| Q94 | 9 | input_content | "Thus, the data is publicly available and thus no potential privacy or content safety concerns." |
| Q95 | 9 | output_content | "Topic-aware article selection is conducted by researchers specializing in historical climate analysis to ensure the dataset is not biased on specific time and location." |
| Q96 | 9 | output_content | "The interpretation of weather-related disruptions in historical newspapers might be influenced by demographic and contextual factors, which is similar to other text datasets generated through crowd-sourcing with inherent challenges in ensuring that dataset labels are fully representative of diverse societal perspectives (Talat et al., 2022)." |
| Q97 | 9 | input_content | "Our primary data source is a corpus of three digitized newspapers (La Presse, La Patrie and Montreal Gazette), obtained through collaboration with the McGill University Library and Archives and the Bibliothèque nationale du Québec." |
| Q98 | 14 | output_content | "To assess the effectiveness of our post-OCR correction process, we evaluated GPT-4o's output against human-annotated corrections on a randomly selected sample of 50 articles." |
| Q99 | 14 | output_form | "The results demonstrate the high accuracy of the automated corrections: Metric 1-gram 2-gram 3-gram / L BLEU 0.9115 0.8935 0.8773 ROUGE 0.9476 0.9190 0.9438" |
| Q100 | 14 | output_form | "The consistently high BLEU and ROUGE scores indicate that GPT-4o's corrections closely align with human-edited versions, validating its effectiveness for improving text quality prior to downstream analysis." |
| Q101 | 14 | input_ontology | "Using Latent Dirichlet Allocation, the dataset was categorized into 15 primary weather event types." |
| Q102 | 14 | input_ontology | "In the absence of standardized impact records (e.g., flood-related property damage, injuries due to ice accumulation, power outages, and road closures), we assessed vulnerabilities and resilience based on the consequences of weather events and how they have changed since the 19th century." |
| Q103 | 14 | output_ontology | "To do so, we categorized disruptive weather impacts into six primary groups — Infrastructural, Agricultural," |
| Q104 | 15 | output_content | "To ensure high-quality and consistent annotations, the task was conducted using a set of specific instructions reviewed by meteorological experts." |
| Q105 | 15 | output_content | "The annotation guideline and the categories definition are provided in Table 14 and Table 15, respectively." |
| Q106 | 15 | output_form | "Notably, the same instruction guidance is contained within the prompts for LLMs in Appendix C to perform impact classification, following a binary output approach for each category." |
| Q107 | 15 | output_content | "Annotators are tasked with determining whether an article includes descriptions that correspond to the impact categories defined in Table 15." |
| Q108 | 15 | output_ontology | "Each article is assigned a label based on the presence or absence of relevant descriptions." |
| Q109 | 15 | input_form | "The average number of tokens per article is 2987.4 in long-context settings and 781.3 in mixed-context settings." |
| Q110 | 15 | output_content | "The annotation process was conducted by members of a research group specializing in uncovering the history of a region's climate change through the regional historical weather records." |
| Q111 | 15 | output_content | "Their expertise can ensure the accuracy and reliability of annotations." |
| Q112 | 16 | input_ontology | "The Multi-Label Classification instructions template in Table 16 is designed for both zero-shot and one-shot classification tasks." |
| Q113 | 16 | input_ontology | "Zero-Shot: The model is given only the classification instructions and the input text." |
| Q114 | 16 | input_ontology | "One-Shot for In-Context Learning: The model is provided with a demonstration for predicting a new sample." |
| Q115 | 16 | input_ontology | "Table 16 presents the prompt designed to analyze historical newspaper texts and classify them into six distinct impact categories based on explicit mentions of weather-related events." |
| Q116 | 16 | output_ontology | "The prompt is structured in alignment with the definitions provided in Table 15, which details the scope of each impact category, including Infrastructural, Agricultural, Ecological, Financial, Human Health, and Political impacts." |
| Q117 | 16 | output_ontology | "The classification task is binary (true/false), requiring the model to identify whether the text explicitly mentions any of the defined impacts." |
| Q118 | 16 | output_content | "The guidelines emphasize focusing on direct and immediate effects, ensuring that classifications are based solely on explicit references within the text." |
| Q119 | 16 | input_ontology | "The ranking-based QA task consists of two key components: question generation (Mo et al., 2023) and candidate ranking (Meng et al., 2024)." |
| Q120 | 16 | input_form | "Figure 6 presents the token length distribution of passages in two versions of our dataset: (a) the Long Context dataset and (b) the Mixed Context dataset used for context-denoising evaluation." |
| Q121 | 16 | input_content | "The Long Context dataset (Figure 6a), which contains 350 articles, exhibits a broader distribution of passage lengths, with a significant portion exceeding 2000 tokens." |
| Q122 | 16 | input_content | "The Mixed Context dataset (Figure 6b), which contains 1,386 articles, is heavily skewed toward shorter passages, with an overwhelming majority containing fewer than 2000 tokens." |
| Q123 | 16 | output_content | "GPT-4O, GPT-4 and GPT-3.5-TURBO are provided by OpenAI, the base model API document: https://platform.openai.com/docs/models" |
| Q124 | 16 | output_content | "DEEPSEEK-V3-671B is upgraded the DEEPSEEK-CHAT, the base model API" |
| Q125 | 17 | input_ontology | "Given the following passage about {row['Weather']}, generate a single, focused question that meets these criteria: 1. Can be answered using ONLY the information in this passage 2. Focuses on the {impact_str} impacts mentioned 3. Is detailed and specific to this exact situation 4. Requires understanding the passage's unique context 5. Cannot be answered by other similar passages about {row['Weather']} Passage: {row['Text']}" |
| Q126 | 17 | output_form | "For the large proprietary models (e.g., GPT-4o), conducting a one-time evaluation on our WXImpactBench costs approximately $3 for multi-label classification tasks and $5.5 for ranking-based QA tasks." |
| Q127 | 17 | output_form | "For all open-source models, evaluations were performed on a system with two NVIDIA A6000 (32GB) GPUs." |
| Q128 | 17 | output_form | "The relatively modest computational requirements highlight the accessibility of our benchmark for researchers with limited computational resources, while still enabling comprehensive evaluation of state-of-the-art models" |
| Q129 | 18 | output_content | "To ensure a high-quality evaluation of historical weather impact analysis, we developed a structured annotation framework for meteorology experts." |
| Q130 | 18 | output_content | "The goal of this annotation is to create a reliable benchmark for assessing the ability of LLMs to understand and classify disruptive weather-related societal and environmental impacts." |
| Q131 | 18 | output_content | "The detailed annotation guidelines are provided in Table 14, outlining the task objectives, category definitions, and better practices for identifying and classifying weather impacts in historical texts." |
| Q132 | 18 | input_content | "Annotators will examine historical newspaper articles documenting disruptive weather events." |
| Q133 | 18 | output_ontology | "The analysis requires the identification of impacts across six categories: infrastructural, agricultural, ecological, financial, human health, and political." |
| Q134 | 18 | output_content | "While specific examples are provided for each impact category, annotators should apply their meteorological expertise to identify and classify impacts beyond these examples, maintaining a comprehensive analytical approach." |
| Q135 | 19 | input_ontology | "Infrastructural Impact: Examines weather-related damage or disruption to physical infrastructure and essential services. Includes structural damage to buildings, roads, and bridges; disruptions to transportation (e.g., railway cancellations, road closures); interruptions to utilities (e.g., power, water supply); failures in communication networks; and industrial facility damage. Both immediate physical damage and service disruptions should be considered." |
| Q136 | 19 | input_ontology | "Agricultural Impact: Focuses on weather-related effects on farming and livestock management. Includes crop yield variations; direct damage to crops, timber, or livestock; modifications to farming schedules; disruptions to food production and supply chains; impacts on farming equipment; and changes in agricultural inputs (e.g., soil conditions, water availability, fertilizers, animal feed). Both immediate and long-term effects should be considered." |
| Q137 | 19 | input_ontology | "Ecological Impact: Examines effects on natural environments and ecosystems. Includes changes in biodiversity; impacts on wildlife populations and behavior; effects on non-agricultural plant life; habitat modifications (e.g., forests, wetlands, water bodies); changes in hydrological systems (e.g., river levels, lake conditions); and urban plant life impact. Immediate environmental changes should be prioritized." |
| Q138 | 19 | input_ontology | "Financial Impact: Analyzes economic consequences of weather events. Includes direct monetary losses; business disruptions requiring financial intervention; market fluctuations; impacts on tourism and local economies; and insurance claims or economic relief measures. The focus should be on explicit financial impacts rather than inferred consequences." |
| Q139 | 19 | input_ontology | "Human Health Impact: Examines both physical and mental health effects. Includes direct injuries or fatalities (including cases where one or more casualties are explicitly mentioned); increased risks of weather-related illnesses; mental health consequences (e.g., stress, anxiety); impacts on healthcare accessibility; and long-term health implications. Both short-term and chronic health effects should be considered." |
| Q140 | 19 | input_ontology | "Political Impact: Evaluates governmental and policy responses to weather events. Includes government decision-making and policy changes; shifts in public opinion or political discourse; effects on electoral processes; international aid and relations; and debates on disaster preparedness and response. Both direct political reactions and policy implications should be analyzed." |
| Q141 | 20 | output_ontology | "Infrastructural Impact: Classify as 'true' if the text mentions any damage or disruption to physical infrastructure and essential services. This includes structural damage to buildings, roads, or bridges; any disruptions to transportation systems such as railway cancellations or road closures; interruptions to public utilities including power and water supply; any failures in communication networks; or damage to industrial facilities. Consider only explicit mentions of physical damage or service disruptions in your classification." |
| Q142 | 20 | output_ontology | "Agricultural Impact: Classify as 'true' if the text mentions any weather-related effects on farming and livestock management operations. This includes yield variations in crops and animal products; direct damage to crops, timber resources, or livestock; modifications to agricultural practices or schedules; disruptions to food production or supply chains; impacts on farming equipment and resources; or effects on agricultural inputs including soil conditions, water availability for farming, and essential materials such as seedlings, fertilizers, or animal feed." |
| Q143 | 20 | output_ontology | "Ecological Impact: Classify as 'true' if the text mentions any effects on natural environments and ecosystems. This includes alterations to local environments and biodiversity; impacts on wildlife populations and behavior patterns; effects on non-agricultural plant life and vegetation; modifications to natural habitats including water bodies, forests, and wetlands; changes in hydrological systems such as river levels and lake conditions; or impacts on urban plant life." |
| Q144 | 20 | output_ontology | "Financial Impact: Classify as 'true' if the text explicitly mentions economic consequences of weather events. This includes direct monetary losses; business disruptions or closures requiring financial intervention; market price fluctuations or demand changes for specific goods; impacts on tourism and local economic activities; or insurance claims or economic relief measures. Focus only on explicit mentions of financial losses or fluctuations." |
| Q145 | 20 | output_ontology | "Human Health Impact: Classify as 'true' if the text mentions physical or mental health effects of weather events on populations. This includes direct injuries or fatalities (including cases where zero or more casualties are explicitly mentioned); elevated risks of weather-related or secondary illnesses; mental health consequences such as stress or anxiety; impacts on healthcare service accessibility; or long-term health implications." |
| Q146 | 20 | output_ontology | "Political Impact: Classify as 'true' if the text mentions governmental and policy responses to weather events. This includes government decision-making and policy modifications in response to events; changes in public opinion or political discourse; effects on electoral processes or outcomes; international relations and aid responses; or debates surrounding disaster preparedness and response capabilities." |
| Q147 | 20 | output_ontology | "Return 'false' for any impact category that is either not present in the text or not related to weather events. Base classifications on explicit mentions in the text. Focus on direct impacts rather than implications. Consider immediate and direct effects." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.bacn.gov.py/leyes-paraguayas/12739/ley-n-7471-2025-que-declara-en-situaci-n-de-emergencia-a-los-departamentos-de-presidente-hayes-boquer-n-y-alto-paraguay-y-ampl-a-el-presupuesto-general-de-la-naci-n-para-el-ejercicio-fiscal-2025-aprobado-por-ley-n-7408-de-fecha-30-de-diciembre-de-2024-presidencia-de-la-rep-blica-secretar-a-de-emergencia-nacional |
| WEB-2 | https://en.wikipedia.org/wiki/Presidente_Hayes_Department |
| WEB-3 | https://defensacivil.gob.bo/ |
| WEB-4 | https://www.unisdr.org/files/30755_boldocpais.pdf |
| WEB-5 | https://www.iadb.org/en/staying-ahead-gran-chacos-floods |
| WEB-6 | https://www.wri.org/insights/gran-chaco-communities-build-climate-resilience |
| WEB-7 | https://en.wikipedia.org/wiki/Rioplatense_Spanish |
| WEB-8 | https://academia-lab.com/encyclopedia/indigenous-peoples-of-argentina/ |
| WEB-9 | https://arxiv.org/html/2501.09943v2 |
| WEB-10 | https://arxiv.org/html/2404.05365v1 |
| WEB-11 | https://aclanthology.org/2022.lrec-1.785/ |
| WEB-12 | https://arxiv.org/html/2507.00999v1 |
| WEB-13 | https://www.bacn.gov.py/leyes-paraguayas/12160/ley-n-7222-que-declara-en-situacion-de-emergencia-nacional-a-los-departamentos-presidente-hayes-boqueron-y-alto-paraguay |
| WEB-14 | https://www.ultimahora.com/secretaria-de-emergencia-nacional |
| WEB-15 | https://www.undp.org/es/bolivia/noticias/defensa-civil-actualiza-protocolos-de-atencion-desastres |
| WEB-16 | https://www.argentina.gob.ar/sinagir/institucional |
| WEB-17 | https://servicios.infoleg.gob.ar/infolegInternet/anexos/400000-404999/400480/norma.htm |
| WEB-18 | https://www.argentina.gob.ar/normativa/nacional/ley-25326-64790/actualizacion |
| WEB-19 | https://www.argentina.gob.ar/aaip/datospersonales/proyecto-ley-datos-personales |
| WEB-20 | https://sen.gov.py/institucional/ |
| WEB-21 | https://www.bacn.gov.py/leyes-paraguayas/2410/ley-n-2615-crea-la-secretaria-de-emergencia-nacional-sen |
| WEB-22 | https://www.mindef.gob.bo/node/499 |
| WEB-23 | https://idrc-crdi.ca/en/what-we-do/projects-we-support/project/valuing-water-changing-climate-and-economy-gran-chaco |
| WEB-24 | https://www.bienvenidoaparaguay.com/deptos.php?xmldepto=17 |
| WEB-25 | https://reliefweb.int/disaster/fl-2015-000171-pry |
| WEB-26 | https://documents1.worldbank.org/curated/en/792921620399148269/pdf/Estimating-Flood-Exceedance-Curves-in-Argentina.pdf |
| WEB-27 | https://arxiv.org/abs/2111.09453 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** Michaelyya/wximpactbench-1386
**Analysis date:** 2025-07-14
**Examples reviewed:** 31 from `train` split
**Columns shown:** id, date, time_period, weather_type, text, infrastructural_impact, political_impact, financial_impact, ecological_impact, agricultural_impact, human_health_impact
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | wximpactbench-1386 | Ex. 1 | all=0 | "John's Cloudy -4 -4 United States Max Min Atlanta Cloudy 17 4 Boston Cloudy 3 -6 Chicago Cloudy 2 2 Dallas Thunderstorms 11 2" | Weather table/tabular data with no narrative — all-zero label, non-event content | IO, IC |
| D2 | wximpactbench-1386 | Ex. 2 | all=0 | "But the real beneficiaries of the work-at-home trend are the employees themselves… She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9)" | Crossword puzzle clues and work-from-home editorial — zero weather impact content | IO, IC |
| D3 | wximpactbench-1386 | Ex. 3 | infra=1 | "by six o'clock the electric car services in all the important points west of Toronto had been completely paralyzed" | 1894 blizzard article: infrastructure disruption to Canadian railway/electric car — exemplary on-target sample | IO, OO |
| D4 | wximpactbench-1386 | Ex. 4 | all=0 | "Police say the aggravated assault charge against Clarkson involves a February attack on Boland in which the celebrity photographer's face and chest were splashed with concentrated sulphuric acid." | Crime report with no weather content — all-zero label | IO, IC |
| D5 | wximpactbench-1386 | Ex. 5 | all=0 | "The decision yesterday followed a 16-hour overnight meeting in Berlin, where debate over how much to give away was sometimes interrupted by the sounds of revellers celebrating the first anniversary of the opening of the Berlin Wall." | Political news about German unification — no weather content | IO, IC |
| D6 | wximpactbench-1386 | Ex. 6 | all=0 | "A poor lady passenger was dashed to leeward and had her skull fractured. She was landed this morning in a dying state with a coffined child that succumbed last night to its sufferings." | Storm narrative with human casualty but annotated all-zero — potential label discrepancy | OC, OO |
| D7 | wximpactbench-1386 | Ex. 7 | infra=1 | "Almost 4 million people across China had been cut off by flood waters, 810,000 homes have collapsed and 2.8 million homes have been damaged" | 1996 Yangtze River flood report from China — not Canadian, annotated for infrastructure | IO, IC |
| D8 | wximpactbench-1386 | Ex. 8 | infra=1, health=1 | "The Jakarta Post reported that hundreds of houses, schools and other buildings sustained damage when one of the twin peaks of the volcano exploded. At least 20 people sustained minor injuries" | Indonesian volcanic eruption and Washington state earthquake — non-Canadian, non-weather-disaster content labeled for infrastructure and health | IO, IC |
| D9 | wximpactbench-1386 | Ex. 12 | all=0 | "residents of southwestern Quebec have been plunged back into the deep freeze Overnight lows in Montreal were expected to drop to minus-16 Celsius last night and tumble as far as minus-30C on the South Shore, where more than one million people struggle on without power or heat" | 1998 Quebec ice storm aftermath — one million without power/heat, annotated all-zero | OC, OO |
| D10 | wximpactbench-1386 | Ex. 14 | infra=1, pol=1, fin=1 | "Residents of the locality were put to great inconvenience by the huge piles of snow now accumulated on the streets… Already $30,000 has been expended in removing it" | 1887 Montreal snow removal municipal debate — multi-label (infra+pol+fin) correctly labeled | OO, OC |
| D11 | wximpactbench-1386 | Ex. 16 | all=0 | "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35" | Stock ticker/financial table — all-zero label, clearly off-topic content | IO, IC, IF |
| D12 | wximpactbench-1386 | Ex. 18 | all=0 | "The walkout will interrupt regular garbage collection and will affect street and sidewalk cleanup if it snows. Unless nine centimetres or more of snow falls during the walkout, blue-collar workers aren't obliged to clean the streets and sidewalks." | Labor dispute/garbage collection strike — weather mentioned incidentally, all-zero label | IO |
| D13 | wximpactbench-1386 | Ex. 19 | all=0 | "Penn refuses to play up the easy nebbish… he does not wear glasses, flood pants or a bow tie" | Film review with only figurative use of "flood" — all-zero label, entirely off-topic | IO, IC |
| D14 | wximpactbench-1386 | Ex. 21 | all=0 | "in Richmond, the storm so long expected has broken forth in all its fury. Great flashes of blinding lightning intermingled with the grand roar of the thunder from on high" | Fictional storm description used metaphorically in a society/romance narrative — all-zero label | IO, IC |
| D15 | wximpactbench-1386 | Ex. 22 | all=0 | "the agency said Christian Lambrechts… said this would expose more of the sea's surface to sunlight, rather than reflect it, contributing to continued and accelerated warming The peninsula - the tongue of land that juts toward South America - has been hit by greater warming than almost any other area on Earth" | Antarctic/climate change science brief — no direct disaster impact, all-zero label | IO |
| D16 | wximpactbench-1386 | Ex. 23 | agri=1, health=1 | "More than 292,000 people have been evacuated in the mountainous region along the Yangtze River, with more than 100,000 homes damaged and crops on about 175,000 hectares of farmland destroyed" | 2007 European/Chinese/Pakistani multi-location disaster report from Montreal Gazette — agricultural and health labeled, but not infrastructural despite 100k homes damaged | OC, OO |
| D17 | wximpactbench-1386 | Ex. 24 | all=0 | "01 SECOND RACE: Trot, I Mile Purse: 11,000 5 Prime Saliora (M. Lalonde) 9.70 5.10 5.70 3 Bidou Fio (R. SimarrJ) 5.30 4.40" | Horse racing results table with unrelated editorial on optometrists' ad — off-topic noise | IO, IC, IF |
| D18 | wximpactbench-1386 | Ex. 26 | pol=1, eco=1 | "A line of freak thunderstorms rumbling across the northeastern Mediterranean coast from Spain and southern France to the principality of Monaco brought two days of disastrous flash flooding… Raging waters uprooted trees and swept away cars as river levels rose by as much as 3 metres" | 1992 Mediterranean flash flood — political and ecological but not infrastructural ("swept away cars," "uprooted trees") — label boundary question | OO, OC |
| D19 | wximpactbench-1386 | Ex. 27 | eco=1 | "With about half the original 1.6-million-hectare swamp filled for development or drained for agriculture, the park includes about 202,000 hectares of marsh experts liken the Everglades to a seriously ill patient" | 1990 Everglades drought/ecosystem article — ecological only; US content | IO, IC |
| D20 | wximpactbench-1386 | Ex. 10 | all=0 | "July 7th they encountered a heavy gale from the west, and had great difficulty in keeping the boat free, the sea continually breaking on board… After the accident they suffered severely from the cold." | 1896 Atlantic rowing voyage encounter with gale — human suffering described but labeled all-zero | OC, OO |
| D21 | wximpactbench-1386 | Ex. 17 | infra=1 | "TRAFFIC IS PARALYZED In Western Canadian Cities, and at Many Points In the United States Disasters In England." | 1894 blizzard chunk (segmented from Ex. 3) — infrastructure label carried over to chunk | IF |
| D22 | wximpactbench-1386 | Ex. 9 | all=0 | "Peter Russell, a law professor at the University of Toronto, said the Supreme Court will benefit from Binnie's solid experience in constitutional and international affairs." | Legal/judicial appointment news — entirely off-topic | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-label simultaneous classification output structure aligns with minimum acceptable deployment form
- **Dimension(s):** OF, OO
- **Observation:** The dataset encodes all six impact categories as simultaneous binary integer labels per row, exactly matching the deployment's minimum acceptable output specification of simultaneous multi-label classification in a single pass. Every sampled example has all six label fields populated.
- **Deployment relevance:** The deployment explicitly requires simultaneous multi-label output rather than ranked or sequential classification. The dataset's schema (six binary int64 fields per example) directly validates this output architecture. National coordinators needing aggregate situational awareness can receive a compact label vector per incoming text, which is operationally viable for resource allocation decisions.
- **Datapoint citations:**
  - [D3] Example 3 (train, infra=1, others=0): "by six o'clock the electric car services in all the important points west of Toronto had been completely paralyzed" — Demonstrates single-pass assignment of one active label among six, with no confusion between co-present categories.
  - [D10] Example 14 (train, infra=1, pol=1, fin=1): "Residents of the locality were put to great inconvenience by the huge piles of snow now accumulated on the streets… Already $30,000 has been expended in removing it" — Demonstrates correct simultaneous multi-label assignment (infrastructure + political + financial) for a single article, proving the scheme supports multi-label outputs in the deployment's required format.

#### Strength 2: Negative examples (all-zero labels) are abundant and structurally necessary
- **Dimension(s):** OO, OF
- **Observation:** A large proportion of the sampled examples carry all-zero labels (approximately 20 of 31 sampled). These include genuinely off-topic texts (crossword puzzles, stock tickers, legal news, sports) as well as weather-adjacent texts where no direct impact was found. This provides a meaningful proportion of true negatives for recall calibration.
- **Deployment relevance:** In an operational disaster triage system, the incoming text stream will include many non-disaster posts. Evaluating model false-positive rates on this large null class is directly relevant to precision in the field, where false alarms generate responder fatigue. The benchmark's mixed-context chunking (which produces label-free negative chunks) replicates a realistic signal distribution.
- **Datapoint citations:**
  - [D2] Example 2 (train, all=0): "She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9)" — Crossword puzzle clues; a strong negative example for any weather impact category.
  - [D12] Example 18 (train, all=0): "The walkout will interrupt regular garbage collection and will affect street and sidewalk cleanup if it snows. Unless nine centimetres or more of snow falls during the walkout" — Weather mentioned incidentally in a labor dispute; correctly labeled all-zero, testing whether models avoid false positives on incidental weather mentions.
  - [D13] Example 19 (train, all=0): "he does not wear glasses, flood pants or a bow tie" — Figurative use of "flood" in a film review; correctly labeled all-zero, testing polysemy handling.

#### Strength 3: Multi-period coverage provides some temporal register variation
- **Dimension(s):** IC, IF
- **Observation:** The dataset spans two temporal periods, with examples from the 1880s–1890s (historical) and from the 1990s–2000s (modern). Within the English-language formal journalistic register, this variation does expose models to somewhat different vocabularies and narrative styles.
- **Deployment relevance:** While the deployment's primary language is Spanish social media, the temporal register variation in the benchmark at least tests whether evaluated LLMs handle internal linguistic variation in their training domain — a minor positive signal for general model robustness. Historical period articles tend to be longer and more explicit about causal chains, which the benchmark's own analysis suggests makes classification somewhat easier.
- **Datapoint citations:**
  - [D3] Example 3 (historical, 18940213): "Sunday evening's despatches brought the news that a very severe blizzard was prevailing in Kansas… electric car services in all the important points west of Toronto had been completely paralyzed" — 1894 formal journalistic prose with archaic vocabulary ("despatches") and elaborated cause-effect structure.
  - [D16] Example 23 (modern, 20070722): "More than 292,000 people have been evacuated in the mountainous region along the Yangtze River, with more than 100,000 homes damaged and crops on about 175,000 hectares of farmland destroyed" — 2007 modern wire service report with compressed, terse disaster description — different register from historical examples.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Language and register are fundamentally mismatched to deployment inputs
- **Dimension(s):** IC, IF
- **Observation:** Every sampled example is English-language formal prose from Canadian newspapers. No Spanish-language text, no social media register, no informal orthography, no platform abbreviations, no indigenous-language toponyms (Pilcomayo, Bermejo, Wichí, Guaraní-derived place names), and no code-switching patterns appear anywhere in the 31 reviewed examples. The benchmark's `languages: en` metadata is confirmed by all examples.
- **Deployment relevance:** The deployment system must process Rio Platense Spanish social media posts and local news fragments that include regional vocabulary with Guaraní, Quechua, and Wichí lexical borrowing. The benchmark provides zero evidence about how any evaluated LLM performs on this input type. Any model performance score obtained on this benchmark is drawn from a language and register distribution with no overlap with the deployment input distribution. Results cannot be validly transferred to predict performance on Gran Chaco Spanish social media content.
- **Datapoint citations:**
  - [D11] Example 16 (train, all=0): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35" — OCR-degraded stock ticker table in English; maximally distant from Spanish social media register.
  - [D2] Example 2 (train, all=0): "She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9)" — Crossword puzzle content in English; confirms that even the negative examples are English formal media, not Spanish social media.
  - [D3] Example 3 (train, infra=1): "Sunday evening's despatches brought the news that a very severe blizzard was prevailing in Kansas" — Historical English narrative style with archaic vocabulary; no feature overlap with informal Rio Platense Spanish.

#### CRITICAL Concern 2: Impact categories were operationalized for Canadian journalistic framing and exclude Gran Chaco-specific damage categories
- **Dimension(s):** IO, OO
- **Observation:** The six impact categories — Infrastructural, Political, Financial, Ecological, Agricultural, Human Health — are operationalized through definitions anchored in Canadian newspaper exemplars. Across all 31 reviewed examples, there is no instance of: cross-border displacement as a political or infrastructural consequence; border integrity as a primary category; locust outbreaks; Chaco fire behavior; dirt-road access disruption to indigenous communities; or agrarian supply chain disruption tied to river crossings. The Political category exemplar in the data (municipal snow removal debate, [D10]) and the ecological exemplar (Everglades drought, [D19]) both reflect North American policy and ecological contexts without any Southern Cone equivalent.
- **Deployment relevance:** The deployment user confirmed that Gran Chaco national coordinators prioritize international border integrity and strategic economic routes as primary news categories, and that cross-border displacement along the Pilcomayo and Bermejo rivers is a primary disaster consequence type. None of these appear in the benchmark's operational definitions or sampled examples. A model trained or evaluated on this benchmark may assign labels that reflect Canadian journalistic salience rather than Gran Chaco responder logic.
- **Datapoint citations:**
  - [D10] Example 14 (train, pol=1, fin=1, infra=1): "Aid. Patrick Kennedy asked the chairman of the Road committee if he could kindly send some men and carts out to Forfar and Conway streets… Already $30,000 has been expended in removing it" — Political label assigned to municipal snow removal budget debate; no analog in Gran Chaco disaster response logic where Political salience concerns border integrity and inter-governmental coordination.
  - [D19] Example 27 (train, eco=1): "With about half the original 1.6-million-hectare swamp filled for development or drained for agriculture, the park includes about 202,000 hectares of marsh experts liken the Everglades to a seriously ill patient" — Ecological label assigned to US Everglades drought/development article; Gran Chaco ecological priorities (Chaco fire, habitat destruction, locust outbreaks) are absent from all reviewed examples.
  - [D18] Example 26 (train, pol=1, eco=1): "Raging waters uprooted trees and swept away cars as river levels rose by as much as 3 metres" — Mediterranean flash flood annotated for political and ecological impacts but not infrastructure ("swept away cars"); the label boundary logic here differs from how Gran Chaco coordinators would classify a road-washing flood event on a critical access route.

#### CRITICAL Concern 3: Ground-truth labels reflect Canadian academic annotators, not Gran Chaco emergency professionals
- **Dimension(s):** OC
- **Observation:** The annotation process used Canadian academic researchers specializing in historical climate analysis; no inter-annotator agreement statistics are available. The reviewed examples reveal several annotation decisions that would likely differ under the consequence-framing logic Gran Chaco national coordinators apply. Example 6 describes a maritime storm in which "a poor lady passenger was dashed to leeward and had her skull fractured" and "a coffined child that succumbed last night to its sufferings" — direct casualties — yet is labeled all-zero. Example 12 describes a million people without power or heat during a Quebec ice storm but is also labeled all-zero. Example 20 describes sailors who "suffered severely from the cold" after a capsizing — also all-zero.
- **Deployment relevance:** The deployment user designated national coordinators in Buenos Aires as the authoritative ground-truth labelers. These annotators apply consequence-framing-dependent logic: the same event attracts different labels depending on which downstream consequences are reported (casualties, supply chain disruption, blocked routes). The benchmark's annotation guidelines emphasize "explicit mentions" and "direct physical effects," but the reviewed examples show that even explicit human casualties can receive all-zero labels (D6, D20), and one million people without power receives all-zero (D9). This annotation philosophy does not match the operational salience logic of Gran Chaco emergency responders.
- **Datapoint citations:**
  - [D6] Example 6 (train, all=0): "A poor lady passenger was dashed to leeward and had her skull fractured. She was landed this morning in a dying state with a coffined child that succumbed last night to its sufferings." — Explicit human casualty from a storm, annotated all-zero; Gran Chaco coordinators would likely assign Human Health=1 for any text reporting casualties caused by weather conditions.
  - [D9] Example 12 (train, all=0): "more than one million people struggle on without power or heat The Weather Network is forecasting a high of only minus-15 today" — Over one million people without power and heat during extreme cold, labeled all-zero; an active infrastructure and human health impact by virtually any emergency responder's framing.
  - [D20] Example 10 (train, all=0): "July 7th they encountered a heavy gale from the west… After the accident they suffered severely from the cold." — Sailors suffering after storm capsizing; direct physical harm from weather, labeled all-zero.

#### MAJOR

#### MAJOR Concern 4: High proportion of non-weather and off-topic content in the mixed-context dataset
- **Dimension(s):** IO, IC
- **Observation:** A substantial proportion of the 31 reviewed examples contain no weather-related content whatsoever and carry all-zero labels. These include: stock ticker tables ([D11], [D17]), horse racing results ([D17]), a film review where "flood pants" appears figuratively ([D13]), a legal/judicial appointment article ([D22]), a fictional/literary storm description ([D14]), a crime report ([D4]), and a political/electoral article ([D5]). These appear to be chunked segments from mixed-context articles where the weather content appeared in a different segment. While they serve as negative examples, they constitute a large portion of the evaluated data.
- **Deployment relevance:** The deployment system processes incoming social media posts and news fragments that are selected because they contain disaster-related keywords or are generated in disaster contexts. The proportion of genuinely irrelevant content in the deployment stream will differ substantially from the benchmark's article-chunk distribution. The benchmark's negative examples include crossword clue fragments and stock tables — types of content that would never appear in a disaster social media triage pipeline — so benchmark precision/recall metrics on this negative class do not translate to the deployment's actual false-positive rate.
- **Datapoint citations:**
  - [D11] Example 16 (train, all=0): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25" — OCR-degraded stock table from the same physical newspaper page as a weather article; artificially generated negative example with no deployment equivalent.
  - [D4] Example 4 (train, all=0): "Police say the aggravated assault charge against Clarkson involves a February attack on Boland in which the celebrity photographer's face and chest were splashed with concentrated sulphuric acid." — Crime report with no weather content; exists as a negative because it was chunked from the same article batch.
  - [D14] Example 21 (train, all=0): "in Richmond, the storm so long expected has broken forth in all its fury. Great flashes of blinding lightning intermingled with the grand roar of the thunder from on high" — Fictional/literary storm description labeled all-zero; tests polysemy handling but represents an unrealistic negative example type for disaster triage.

#### MAJOR Concern 5: Label boundary inconsistencies visible within the sampled data
- **Dimension(s):** OO, OC
- **Observation:** Several examples reveal inconsistent label boundary application. Example 23 (2007 European/Chinese floods) labels agricultural=1 and health=1 for a report that also states "more than 100,000 homes damaged" — a clear infrastructural impact — but infrastructure=0. Example 26 labels a Mediterranean flash flood that "swept away cars" and "uprooted trees" as ecological=1 and political=1 but not infrastructural. Example 6, as noted above, reports human skull fracture and child death from a storm but receives all-zero labels. No inter-annotator agreement statistics are available to assess whether these represent systematic decisions or annotation noise.
- **Deployment relevance:** The deployment requires consistent label assignment because national coordinators will use these labels for resource allocation. If the benchmark's underlying annotation philosophy produces labels that a Gran Chaco coordinator would consider inconsistent (infrastructure present but unlabeled when homes collapse; human health absent when casualties occur), then model performance scores on this benchmark do not validly predict whether a model's outputs will be trusted by the deployment's authoritative labelers.
- **Datapoint citations:**
  - [D16] Example 23 (train, agri=1, health=1): "more than 100,000 homes damaged and crops on about 175,000 hectares of farmland destroyed, Xinhua said" — 100k homes damaged annotated as not infrastructural while agricultural and health labels are positive; boundary logic unclear.
  - [D18] Example 26 (train, pol=1, eco=1): "Raging waters uprooted trees and swept away cars as river levels rose by as much as 3 metres" — Cars swept away and infrastructure-affecting flood labeled ecological and political but not infrastructural.
  - [D6] Example 6 (train, all=0): "A poor lady passenger was dashed to leeward and had her skull fractured. She was landed this morning in a dying state with a coffined child that succumbed last night to its sufferings." — Direct weather-caused fatalities annotated as zero for all categories including human health.

#### MAJOR Concern 6: Geographic scope of labeled content extends beyond Canada but the impact taxonomy remains Canadian-framed
- **Dimension(s):** IO, IC
- **Observation:** Multiple labeled examples describe disasters that occurred in China ([D7], [D16]), Japan ([D7]), Pakistan ([D16]), Indonesia ([D8]), the United States ([D8], [D19]), and Europe ([D18]), not Canada. These appear to be wire service reports from the Montreal Gazette that happened to be selected by the LDA topic model. The benchmark's geographic scope is therefore not strictly Canadian despite being framed as such, but the taxonomy and annotation logic remain Canadian-academic in origin.
- **Deployment relevance:** While the presence of non-Canadian content is a minor positive in that it confirms the benchmark tests general event description, it also reveals that the benchmark's input ontology claim ("designed exclusively for Canadian weather-impact journalism") is overstated. More importantly, none of these non-Canadian examples covers Gran Chaco, South American, or Southern Cone disaster types. The presence of Yangtze River flood content ([D7]) is geographically proximate to a different river-flooding context than Pilcomayo/Bermejo, but the consequences described (urban industrial flooding, military deployment) bear no resemblance to Gran Chaco operational priorities (indigenous community access, dirt-road cutoffs, cross-border displacement).
- **Datapoint citations:**
  - [D7] Example 7 (train, infra=1): "Almost 4 million people across China had been cut off by flood waters, 810,000 homes have collapsed and 2.8 million homes have been damaged in eight provinces as of July 18" — Chinese flood content in a Canadian newspaper; labeled for infrastructure but consequences (urban China scale) are entirely different from Gran Chaco deployment context.
  - [D8] Example 8 (train, infra=1, health=1): "The Jakarta Post reported that hundreds of houses, schools and other buildings sustained damage when one of the twin peaks of the volcano exploded. At least 20 people sustained minor injuries" — Indonesian volcanic eruption content; labeled for infrastructure and health, confirms non-Canadian labeled content exists but does not improve Gran Chaco relevance.
  - [D19] Example 27 (train, eco=1): "With about half the original 1.6-million-hectare swamp filled for development or drained for agriculture, the park includes about 202,000 hectares of marsh" — US Everglades content labeled ecological; confirms US environmental content present in benchmark.

#### MINOR

#### MINOR Concern 7: OCR degradation artifacts persist in mixed-context chunks, creating evaluation noise
- **Dimension(s):** IF
- **Observation:** Several examples contain clearly OCR-degraded text that survived post-correction. Example 16 contains character strings like "Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35 -1 Gift sir 14000 33 30 33 1 Aloha gld 10000 85 80 80 5 Clinedev 1600 0 0 0." Example 17 (a chunk of the same article as Example 3) begins with advertisements including "Q. SIBBALD, 3 WINDSOR HOTEL, MONTREAL Telegraph and Telephone Supplies, STEEL AND IRON BEAMS." Example 30 has heavily degraded financial table content with OCR artifacts.
- **Deployment relevance:** The deployment system processes social media posts where noise takes the form of informal orthography, abbreviations, and code-switching — not OCR artifacts from physical newspaper digitization. Model robustness to OCR noise does not transfer to robustness to social media noise. The specific noise patterns in the benchmark (column layout fragmentation, numerical table corruption) are irrelevant to the deployment input distribution.
- **Datapoint citations:**
  - [D11] Example 16 (train, all=0): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35 -1 Gift sir 14000 33 30 33 1 Aloha gld 10000 85 80 80" — OCR-degraded financial table with column fragmentation artifacts.
  - [D21] Example 17 (train, infra=1): "Q. SIBBALD, 3 WINDSOR HOTEL, MONTREAL Telegraph and Telephone Supplies, STEEL AND IRON BEAMS MIDDLETON & MEREDITH, 30 St John Street, Montreal" — Mixed-context chunk that begins with advertisement text before the disaster content; OCR column layout artifacts persist.

#### MINOR Concern 8: weather_type field has high missingness and inconsistent values
- **Dimension(s):** IO
- **Observation:** Of the 31 reviewed examples, 20 have `weather_type` of "Nan" (string null) or `*null*`. Only 11 have a labeled weather type. This field was intended to represent the LDA-derived weather event classification, but a large proportion of the mixed-context chunks either inherit no weather type from segmentation or were not classified. This means the benchmark's claimed 15 LDA-derived weather event types are not reliably captured per example in the HF dataset.
- **Deployment relevance:** If downstream users attempted to use the `weather_type` field to filter benchmark examples by event type (e.g., to evaluate model performance on flood-related articles specifically, as the deployment prioritizes), this field is unreliable for doing so. This limits the benchmark's utility for any sub-analysis by event type that might partially approximate Gran Chaco flood-disaster content.
- **Datapoint citations:**
  - [D1] Example 1 (train, weather_type="Nan"): "John's Cloudy -4 -4 United States Max Min Atlanta Cloudy 17 4" — Weather forecast table with no weather_type label assigned despite clear weather content.
  - [D4] Example 4 (train, weather_type="Nan"): "Police say the aggravated assault charge against Clarkson involves a February attack on Boland in which the celebrity photographer's face and chest were splashed with concentrated sulphuric acid." — Crime report with no weather content, also weather_type="Nan"; the field does not distinguish weather-relevant from weather-irrelevant null entries.

---

### Content Coverage Summary

The 31 reviewed examples are drawn from the mixed-context (chunked, ~250-token) version of the dataset. The content spans English-language text from three Canadian newspapers (La Presse, La Patrie, Montreal Gazette) across two time periods (historical: 1880s–1890s; modern: 1990s–2000s). The actual content is considerably more heterogeneous than the benchmark's framing suggests: approximately two-thirds of the reviewed examples contain either no weather content at all (crime reports, stock tables, crossword clues, horse racing results, film reviews, political news) or weather content that has been annotated as having zero impact. This reflects the mixed-context chunking process, which segments full articles into ~250-token pieces and independently annotates each chunk — generating many content-free negative examples.

The labeled positive examples demonstrate that the benchmark can capture broadly defined impact categories (infrastructure disruption from 19th-century blizzards, agricultural and health impacts from large-scale floods), and the multi-label simultaneous annotation scheme is structurally sound. However, content drawn from outside Canada — China, Indonesia, the United States, Europe — is present in the labeled portion of the dataset, indicating the LDA topic model selected some international wire service content from the Montreal Gazette.

The register is uniformly formal English journalistic prose. No Spanish, no social media content, no indigenous-language vocabulary, and no content reflecting Southern Cone geographic or institutional contexts appears in any reviewed example. The annotation logic, as visible in the data, emphasizes textual explicitness of direct physical consequences, sometimes to the exclusion of events that operational emergency professionals would classify as impactful (e.g., weather-caused human casualties labeled all-zero in Examples 6 and 20).

---

### Limitations

1. **Sample size**: 31 examples from the 970-example training split (3.2%) were reviewed. Label distribution patterns, especially for positive examples in rare categories (Political, Ecological), may not be fully represented in this sample. The full test split (208 examples) was not reviewed.

2. **Test split not reviewed**: The benchmark's evaluation uses the test split; the training split reviewed here may have a different proportion of positive examples, different OCR degradation levels, or different geographic source distribution.

3. **Long-context version not reviewed**: The 350-example long-context version (avg. 2,987 tokens per article) is a separate dataset configuration. The chunking artifacts and noise content observed here may be less prevalent in the long-context version where full articles are retained. The HF dataset reviewed (`wximpactbench-1386`) is the mixed-context version only.

4. **Annotation guidelines not directly inspectable**: The annotation guidelines referenced in the benchmark documentation (Tables 14 and 15 of the paper) are described in the YAML but not directly accessible in the HF dataset record. The specific definitional scope of each category and the guidance for edge cases can only be inferred from examples.

5. **No direct access to ranking-based QA data**: The pseudo-questions generated by GPT-4O for the ranking task are not present in the HF dataset reviewed; only the classification labels are available. The QA task's validity for the deployment cannot be assessed from this dataset alone.

6. **Cannot assess inter-annotator agreement**: The HF dataset contains no annotation metadata (annotator IDs, confidence scores, disagreement flags). Label reliability must be inferred from the pattern of observed edge cases.

