## Deployment Context

**Use case:** Use case: Reliability of disaster reporting in news at national/local level, finding alignment with effective and verified information (e.g. noisy vs real signals). The evaluation data could report or not disaster damage.
**Target population:** Policy makers and government agencies in Argentina studying trustiness and reliability of disaster communication across different channels are (e.g news, social media post, press). They would be based in Buenos Aires, speakers of Rioplatense Spanish, with an intermediate to advanced level of English, at least a master's degree, and be part of an upper-middle-class household.

# Validity Analysis: wximpactbench
**Target context:** Argentine Government Disaster Reporting Reliability — Policy Staff
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 3 | Moderate gaps | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ⚠ | 2 | Significant gaps | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 3 | Moderate gaps | medium |
| **Average** | **2.2** | | |

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

WXImpactBench is an English-language, formally-styled, North America-centric benchmark whose six top-level impact categories transfer reasonably to Argentine disaster types but whose content, register, language, annotator pool, and output schema all diverge substantially from the deployment's needs. The most severe validity violations are in input_content (zero Spanish-language, zero Argentine, zero social media content; HIGH priority) and output_ontology (no native credibility scoring — though deliberately handled downstream by user design — and no sub-labels for Argentine-specific granularity; HIGH priority). Input_form is mismatched on register and length, and the paper itself acknowledges formal historical text is easier for LLMs than informal modern text, meaning benchmark scores likely overstate deployment-relevant capability. Output_content carries zero Argentine annotator representation and exhibits empirical labeling inconsistencies on positively-framed chunks. The benchmark may serve as one input to model triage but cannot stand alone as evidence of deployment-readiness for Argentine government disaster reporting reliability assessment.

## Practical Guidance

### What This Benchmark Measures

WXImpactBench measures LLM ability to extract six pre-defined societal impact categories from formal long-form English-language historical journalism, and to retrieve relevant articles given a generated question. For the Argentine deployment, this provides indirect evidence of LLM reasoning over formal press content, particularly across two linguistic registers, and exercises some noise-rejection capability through the chunked dataset's heterogeneous off-topic content [DATASET-D2, D7, D23]. Strongest dimensions for the target context are output_form (functional compatibility for upstream feature use) and input_ontology (six top-level categories applicable per elicitation [A1]).

### Construct Depth

Construct depth is shallow for the deployment's primary need. The benchmark probes formal English long-form impact classification but does not probe (a) Spanish-language disaster content, (b) social media or short-form informal text, (c) credibility/reliability scoring, (d) Argentine institutional actor recognition, (e) slow-onset disaster framing (ENSO drought), or (f) villa miseria social vulnerability framing. The paper's own observation that formal historical style is easier for LLMs [Q83, Q85] caps the upper bound of construct generalization. Empirical labeling inconsistencies [DATASET-D17, D22, D27] further limit confidence in the convergent validity of the impact-classification construct itself.

### What Else You Need

The deployment requires substantial supplementation: (1) a Rioplatense Spanish disaster impact gold-standard test set built with Argentine annotators (no equivalent exists per WEB-14, gap_id 7); (2) a social media short-form evaluation, with HumAID/CrisisBench [WEB-14, WEB-15] as English-language starting points pending cross-lingual transfer validation; (3) a credibility/reliability scoring layer with Argentine source metadata (outlet reach, account verification, AFE/SINAGIR institutional recognition); (4) sub-label refinement for villa miseria infrastructure, agricultural commodity-specific loss, and Argentine partisan-framing political impact; (5) re-annotation of a sample by Argentine emergency management experts to verify whether documented labeling inconsistencies persist under Argentine interpretation.

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The six top-level impact categories (Infrastructural, Political, Financial, Ecological, Agricultural, Human Health) are broadly applicable to Argentine disaster types and the elicitation confirms they 'could accommodate the named disaster types' [A1]. Empirical inspection confirms each category appears in the data with positive examples [DATASET-D14, D16, D18]. However, the ontology is constructed entirely around formal newspaper articles [Q18, Q115], with no task type targeting social media, press releases, or short-form informal content — the deployment's highest-priority input channels. No sub-labels exist within the six categories, a recognized gap for Argentine policy granularity (e.g., villa miseria vs. formal infrastructure). The chunked dataset also includes a high proportion (≈65%) of off-topic zero-label fragments [DATASET-D1, D2, D7, D23] that may dilute the discriminative validity of the ontology for genuine disaster classification. The QA task is closed-retrieval only [Q89], precluding the open-retrieval setting most relevant to a deployment scanning real source streams.

**Strengths:**
- Six top-level categories map cleanly onto Argentine disaster impact types per elicitation [A1, Q11]
- All six labels are empirically present and distinguishable in the data, with both single-label and multi-label positive cases [DATASET-D14, D16, D18]
- Multi-label simultaneous classification design [Q57] matches realistic disaster reports that span multiple impact dimensions

**Checklist:**

- **IO-1**: Argentine deployment requires categories covering: urban flash floods (AMBA), sudestada coastal flooding, pampero windstorms, ENSO-driven Pampa drought, Patagonian wildfire, NOA flood/drought, plus credibility/reliability scoring across formal press, social media, and informal community channels [WEB-1, WEB-5, WEB-7]. — _Sources: WEB-1, WEB-5, WEB-7_
- **IO-2**: Benchmark omits: (a) any task targeting social media or short-form informal content [Q18, Q115], (b) credibility/misinformation/source-reliability scoring (the deployment's core task per A3), (c) sub-labels within the six categories needed for Argentine policy granularity [A1], (d) open-retrieval QA setting [Q89], and (e) Spanish-language task framing. — _Sources: Q18, Q89_
- **IO-3**: No categories appear actively irrelevant to the Argentine context — the six top-level categories are broadly applicable per A1. However, the LDA-derived 15 weather event types [Q101] are not surfaced as evaluation categories, and the chunked dataset contains a high proportion of off-topic content (crosswords, film reviews, stock tables) labeled all-zero [DATASET-D2, D7, D23], which dilutes the ontology's discriminative signal. — _Sources: Q101, DATASET-D2, DATASET-D7, DATASET-D23_
- **IO-4**: Major gaps: (1) no social media / short-form input task type despite this being a HIGH-priority deployment channel; (2) no credibility scoring task; (3) no sub-labels for Argentine-specific granularity (informal settlements, agricultural commodity-specific loss); (4) closed-retrieval QA only. — _Sources: Q18, Q89_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q11] 'six impact categories (infrastructural, political, financial, ecological, agricultural, and human health), which are informed by previous studies (Imran et al., 2016a) and align with modern disaster impact assessment frameworks' (p.2)
- [Q18] 'Climate impact analysis (Thulke et al., 2024) aims to help society make correct decisions about climate-related challenges affecting communities' (p.2)
- [Q57] 'we simultaneously identify all relevant disruptive weather impacts for each input by calling the LLM once' (p.6)
- [Q89] 'The practical open-retrieval setting, i.e., identifying the relevant articles from a huge database, is left for future studies' (p.9)
- [Q101] 'Using Latent Dirichlet Allocation, the dataset was categorized into 15 primary weather event types' (p.14)

*Web sources:*
- [WEB-1] SINAGIR now operates within the AFE created by Decreto 225/25 (March 2025) — institutional taxonomy not represented in benchmark
- [WEB-5] 32.9 million Argentine social media user identities as of October 2025, indicating major deployment input channel absent from benchmark

*Dataset analysis:*
- DATASET-D14: 1894 blizzard chunk correctly labeled infrastructural=1, confirming category is empirically distinguishable
- DATASET-D16: 1887 Montreal snow removal chunk labeled infra=1+political=1+financial=1, demonstrating multi-label realism
- DATASET-D2, D7, D23: crossword puzzles, film reviews, OCR-corrupted stock tables labeled all-zero — high proportion of off-topic chunks dilute ontology signal

</details>

**Information gaps:**
- Whether sub-label schema for villa miseria infrastructure damage could be added without re-annotating the corpus
- Whether credibility scoring could be derived from existing label outputs without dedicated task design

**Requires expert verification:**
- Which Argentine sub-categories within each top-level label matter most for SINAGIR/AFE policy decision-making

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark corpus is exclusively English-language historical Canadian newspaper text from La Presse, La Patrie, and the Montreal Gazette [Q97]. No Spanish-language, Argentine, or Latin American source material is represented, and no Argentine institutional actors (SINAGIR, SMN, AFE), geographic references, or local disaster framing appear. The deployment explicitly handles Rioplatense Spanish across formal press, social media, and informal community channels — none of which are in the benchmark. The paper itself acknowledges 'potential biases in underrepresented historical events and linguistic variations' [Q90] and that 'the interpretation of weather-related disruptions in historical newspapers might be influenced by demographic and contextual factors' [Q96]. Empirically, the dataset contains some non-Canadian wire-service content (China, Mediterranean, Indonesia) [DATASET-D18, D19, D21], which marginally broadens geographic scope but does not include South America or Spanish-language content. Web search confirmed no Argentine Spanish-language disaster NLP benchmark exists [WEB-14, WEB-15] to supplement this gap. Given that input_content is a HIGH-priority dimension per elicitation, this represents a major validity violation.

**Strengths:**
- Some non-Canadian wire-service content (China, Pakistan, Mediterranean, Indonesia) appears in positive examples [DATASET-D18, D19, D21], indicating impact categories are applied beyond strictly Canadian events
- Two temporal periods covered to introduce linguistic variation [Q13]
- Authors explicitly acknowledge potential biases in underrepresented events [Q90]

**Checklist:**

- **IC-1**: Argentine deployment requires Rioplatense Spanish proficiency, recognition of Argentine institutional actors (SINAGIR, AFE, SMN, Prefectura Naval, provincial civil defense), and familiarity with local disaster framing including villa miseria vulnerability — none of which appears in benchmark inputs [Q97]. — _Sources: Q97, WEB-1_
- **IC-2**: Cultural alignment is poor: benchmark content is North American historical journalism [Q97]; elicitation flags that 'informal or social media data carries meaning and communication patterns that are likely not represented in the Canadian-sourced benchmark' [A2]. — _Sources: Q97, DATASET-D14, DATASET-D16_
- **IC-3**: Inputs require Western-specific knowledge: 19th-century Canadian institutional context (Q12, Q14), Montreal civic geography [DATASET-D16], and English-language journalism conventions. None transfers to Spanish-language Argentine social media or AMBA disaster reporting. — _Sources: Q14, Q97, DATASET-D14, DATASET-D16_
- **IC-4**: INSUFFICIENT DOCUMENTATION on regional annotator recruitment for Argentine context; no Argentine annotators were involved per Q110 (annotators specialize in regional Canadian historical climate).
- **IC-5**: Major content issues: zero Spanish-language content; zero Argentine geography; zero villa miseria framing; zero social media content; zero institutional actors relevant to AFE/SINAGIR. Confirmed via web search — no complementary Argentine Spanish disaster benchmark exists [WEB-14, search gap_id 2 and 7]. — _Sources: Q90, WEB-14, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q97] 'Our primary data source is a corpus of three digitized newspapers (La Presse, La Patrie and Montreal Gazette), obtained through collaboration with the McGill University Library and Archives and the Bibliothèque nationale du Québec.' (p.9)
- [Q90] 'it may have potential biases in underrepresented historical events and linguistic variations' (p.9)
- [Q96] 'The interpretation of weather-related disruptions in historical newspapers might be influenced by demographic and contextual factors' (p.9)
- [Q13] 'We extract a sample of articles from two time periods, which cover linguistic and social changes across different eras' (p.2)

*Web sources:*
- [WEB-14] HumAID English-language disaster tweets exists but contains no Argentine events or Spanish content
- [WEB-5] 32.9M Argentine social media identities — deployment-relevant content space absent from benchmark
- [WEB-1] SINAGIR/AFE institutional structure — Argentine disaster authorities not represented in benchmark corpus

*Dataset analysis:*
- DATASET-D18: Chinese flood content labeled — confirms ontology applied to non-Canadian geography
- DATASET-D19: Mediterranean thunderstorm flooding labeled political=1+ecological=1 — European disaster
- DATASET-D21: Indonesian volcanic eruption labeled — but no South American content observed in 31-example sample
- DATASET-D14, D16: Canadian-specific content (Toronto transit, Montreal civic council) requires regional knowledge

</details>

**Information gaps:**
- Whether HumAID/CrisisBench English-language tweets could serve as partial supplements after cross-lingual transfer validation [WEB-14]
- Empirical performance of LLMs on Rioplatense Spanish disaster content (no Argentine benchmark exists for direct measurement)

**Requires expert verification:**
- Whether formal Argentine press content (Clarín, Infobae, La Nación) closely follows transferable journalistic patterns as A2 hypothesizes
- Construction of an Argentine Spanish gold-standard test set for cross-lingual validation

---

### Input Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark is text-only [Q19], which matches the deployment's text-based channels. However, the form characteristics diverge substantially: benchmark inputs are long-form (avg 2,987 tokens) or chunked (avg 781 tokens) [Q109], formally structured historical journalism with 'outdated terminology, spelling variations, and evolving writing conventions' [Q14]. The Argentine deployment includes social media posts (often <280 chars), WhatsApp messages, hashtags, emoji, lunfardo slang, and informal abbreviation — none of which is represented. Critically, the paper itself notes that formal historical narrative style is *easier* for LLMs to classify [Q83, Q85], meaning benchmark performance estimates likely overstate model capability on noisier informal inputs. Web research confirms most LLMs face specific challenges with flood-related social media even in English [WEB-17]. The benchmark is English-only with Latin script; Rioplatense Spanish, while also Latin-script, introduces voseo, yeísmo rehilado lexicon, and Italian-influenced vocabulary not exercised. Empirically, the dataset contains heavily OCR-corrupted financial table chunks [DATASET-D23] which are not analogous to Argentine social media noise but do confirm noise tolerance is partially exercised. Input form is a MODERATE-priority dimension per elicitation; score reflects significant register and length mismatch.

**Strengths:**
- Text modality matches deployment's text channels [Q19]
- Mixed-context chunking (avg 781 tokens) [Q109] is closer to press release length than full historical articles
- Two linguistic registers (historical and modern) exercise some register robustness [DATASET-D14, D18]
- OCR-noisy chunks in dataset [DATASET-D23] provide some test of noise tolerance

**Checklist:**

- **IF-1**: Significant signal mismatch: benchmark long-context avg 2,987 tokens, mixed-context avg 781 tokens [Q109]; deployment includes tweet-length (<280 chars), WhatsApp messages, and government press bulletins. Register mismatch: formal English journalism vs. Rioplatense Spanish informal social media with lunfardo, emoji, hashtags. — _Sources: Q109, Q19, WEB-5_
- **IF-2**: Argentine infrastructure supports text capture: 90.6% national internet penetration, 98.4% mobile broadband [WEB-5], Buenos Aires fixed broadband 41–101 Mbps [WEB-7]. However, rural disaster-zone producers have lower connectivity (three provinces <20 Mbps) [WEB-7, WEB-8], potentially yielding compressed/delayed content not represented in benchmark. — _Sources: WEB-5, WEB-7, WEB-8_
- **IF-3**: Domain-specific form differences: deployment requires handling Twitter/X short-form, WhatsApp messages, emoji, hashtags, code-switching English/Spanish, OCR-absent native digital text — none in benchmark [Q19, Q109]. — _Sources: Q19, Q109_
- **IF-4**: External validity harm is significant: paper explicitly notes formal historical style is easier for LLMs [Q83, Q85], and HumAID-based research shows LLMs struggle with flood social media even in English [WEB-17]. Performance metrics on this benchmark likely overstate Argentine deployment capability on informal channels. — _Sources: Q83, Q85, WEB-17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q19] 'The construction of the dataset aims to obtain high-quality text samples... data collection, post-OCR correction, topic-aware article selection, and manual label annotation.' (p.3)
- [Q109] 'The average number of tokens per article is 2987.4 in long-context settings and 781.3 in mixed-context settings.' (p.15)
- [Q14] 'Historical newspapers often employed more descriptive and elaborate narratives compared to modern reporting styles' (p.2)
- [Q83] 'The reason might be the structured and formal narrative style used to report disruptive weather events in historical periods, which more explicitly highlights cause-and-effect relationships.' (p.8)
- [Q85] 'the language patterns used in historical narrative styles are easier for language models to identify, and thus perform better on classifying disruptive weather impacts.' (p.8)

*Web sources:*
- [WEB-17] Most LLMs face specific challenges processing flood-related social media data even in English (HumAID-based six-LLM analysis)
- [WEB-5] 98.4% Argentine mobile broadband indicates short-form mobile content dominant in deployment
- [WEB-7] Rural-urban digital divide means disaster-zone content carries different noise characteristics than urban Buenos Aires

*Dataset analysis:*
- DATASET-D23: OCR-corrupted financial tables present as test rows — exercises noise tolerance but not analogous to social media noise
- DATASET-D14 (1894) vs D18 (2007): two-period register variation present
- DATASET-D11: literary/figurative storm language [DATASET-D11] tests metaphor distinction, partially relevant to Spanish 'tormenta política' usage

</details>

**Information gaps:**
- Empirical token-length distribution of Argentine disaster reporting across formal press, press releases, and social media
- Quantitative LLM performance gap between formal long-form and informal short-form Spanish disaster content

**Requires expert verification:**
- Whether the mixed-context (~781 token) chunks adequately approximate Argentine government press bulletin length

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The deployment's primary decision-support output — reliability/credibility scoring of disaster reports — is structurally absent from the benchmark output space, which produces only six binary impact labels [Q25, Q33, Q117] and ranking lists [Q36]. The user envisions credibility as a downstream layer aggregating model outputs with external metadata [A3], so this gap is partially mitigated by deployment design. However, even within the impact-labeling output, the binary schema with no sub-labels limits granularity for Argentine policy needs (villa miseria vs. formal infrastructure; soybean/maize vs. Canadian grain framing). Annotation guidelines emphasize 'direct and immediate effects' and 'explicit references' [Q118, Q147], excluding inferred or slow-onset impacts — a meaningful constraint for ENSO-driven Pampa drought assessment. Empirically, dataset analysis identifies labeling inconsistencies on positive-content chunks (1998 Quebec ice storm with 1M+ without power labeled all-zero [DATASET-D17]; 1881 storm with explicit casualties labeled human_health=0 [DATASET-D27]) that suggest the binary output decisions may not be fully reliable. Output ontology is HIGH-priority per elicitation; score reflects the structural absence of the credibility dimension and granularity constraints, partially offset by user's deliberate design to handle credibility downstream.

**Strengths:**
- User explicitly designed deployment to use binary labels as upstream features for downstream credibility aggregation [A3] — output schema is functionally compatible
- Detailed operational criteria provided for each label [Q141–Q146] enable consistent interpretation
- Multi-label simultaneous output [Q57] supports reports spanning multiple impact dimensions
- Six-category schema accepted as broadly applicable to Argentine disasters per elicitation [A1]

**Checklist:**

- **OO-1**: Six output labels (Infrastructural, Political, Financial, Ecological, Agricultural, Human Health) [Q25] are regionally relevant per elicitation [A1] and confirmed empirically present [DATASET-D14, D16, D18, D21]. — _Sources: Q25, DATASET-D14, DATASET-D16_
- **OO-2**: Missing categories: (a) credibility / source-reliability / signal-to-noise dimension — the deployment's core decision output, addressed downstream per A3; (b) sub-labels for villa miseria infrastructure vs. formal infrastructure; (c) sub-labels for slow-onset ecological/agricultural impacts (ENSO drought) — guidelines exclude inferred consequences [Q118, Q147]; (d) misinformation likelihood scoring. — _Sources: Q117, Q118, Q147_
- **OO-3**: Categories themselves do not encode non-Argentine values per elicitation [A4]; however, Political Impact criterion [Q140, Q146] frames responses around 'governmental and policy responses' in a Canadian institutional frame that may not capture Argentine partisan polarization or villa miseria framing. The 'direct and immediate' framing [Q118, Q147] systematically excludes the slow-onset and politically-instrumentalized framings common in Argentine disaster discourse. — _Sources: Q140, Q146, Q147_
- **OO-4**: Stakeholder-driven taxonomy redesign is recommended for sub-label addition (informal settlement vulnerability, agricultural commodity-specific loss, partisan-framing political impact). User indicates failure analysis on Argentine data could inform future sub-labeling [A4].
- **OO-5**: Structural validity is harmed by absence of credibility/reliability output (the deployment's primary need) and absence of sub-labels for Argentine-specific granularity. Empirical labeling inconsistencies [DATASET-D17, D22, D27] additionally raise concern about the structural reliability of the binary outputs. — _Sources: Q117, DATASET-D17, DATASET-D22, DATASET-D27_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'Six vulnerability-related disruptive weather impacts are defined as the labeling categories, including Infrastructural, Political, Financial, Ecological, Agricultural, and Human Health.' (p.4)
- [Q33] 'six ground-truth impacts Yt = {y^i_t}^6_i=1 with binary labels y^i_t ∈ {0, 1}' (p.5)
- [Q117] 'The classification task is binary (true/false), requiring the model to identify whether the text explicitly mentions any of the defined impacts.' (p.16)
- [Q118] 'The guidelines emphasize focusing on direct and immediate effects, ensuring that classifications are based solely on explicit references within the text.' (p.16)
- [Q147] 'Return false for any impact category that is either not present in the text or not related to weather events. Base classifications on explicit mentions in the text. Focus on direct impacts rather than implications.' (p.20)

*Web sources:*
- [WEB-1] SINAGIR/AFE Argentine institutional framework operates with different political accountability structure than Canadian framework
- [WEB-16] Pastel weakly supervised credibility extraction is closest methodological complement but not validated on Spanish disaster content

*Dataset analysis:*
- DATASET-D17: 1998 Quebec ice storm with >1M without power labeled all-zero — potential under-labeling concern for human_health and infrastructural recall
- DATASET-D22: China Yangtze flood + Japan E. coli deaths labeled infra=1 but human_health=0 despite explicit casualties
- DATASET-D27: 1881 storm with skull fracture and child death labeled human_health=0 — labeling inconsistency
- DATASET-D26: Antarctic warming labeled all-zero — slow-onset ecological framing systematically excluded

</details>

**Information gaps:**
- Whether Argentine policy users would accept 'direct and immediate' criterion or require slow-onset assessment for ENSO drought
- Specification of downstream credibility aggregation pipeline that A3 references

**Requires expert verification:**
- Whether the labeling inconsistencies flagged in dataset analysis (D17, D22, D27) constitute systematic errors or chunk-level re-annotation per Q47/Q48

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Annotators are three domain experts from a research group 'specializing in uncovering the history of a region's climate change through the regional historical weather records' [Q110, Q111] — i.e., specialists in Canadian historical climate. No demographic information about annotator nationality, language background, or familiarity with Latin American disaster communication is documented. The paper acknowledges 'the interpretation of weather-related disruptions in historical newspapers might be influenced by demographic and contextual factors' [Q96] but does not mitigate this. The user does not anticipate systematic disagreement on formal press given Argentine reliance on Global North standards [A4], which moderates concern. However, dataset analysis surfaces concrete labeling inconsistencies: 1998 Quebec ice storm (1M+ without power, -30°C) labeled all-zero on infrastructural and human_health [DATASET-D17]; 1881 storm with explicit fatalities labeled human_health=0 [DATASET-D27]; China flood + Japan deaths labeled infra=1 but human_health=0 [DATASET-D22] while a smaller-scale Indonesian eruption is labeled human_health=1 [DATASET-D21]. These inconsistencies raise convergent validity concerns even within the Canadian context, compounded by the absence of any Argentine validation. Output content is MODERATE-priority per elicitation; score reflects the combination of zero Argentine annotator representation and empirical labeling inconsistencies.

**Strengths:**
- Annotation guidelines reviewed by meteorological specialists [Q104]
- Independent chunk-level re-annotation for mixed-context version [Q47, Q48] reduces label inheritance bias
- Topic-aware article selection by historical climate researchers reduces temporal/geographic selection bias [Q95]
- Detailed per-label criteria [Q141–Q146] support reproducibility
- User does not anticipate systematic label disagreement for formal press given Argentine reliance on Global North standards [A4]

**Checklist:**

- **OC-1**: Ground-truth labels reflect Canadian historical-climate research-group perspectives [Q110, Q111]; Argentine stakeholder perspectives are not represented in any annotation step. — _Sources: Q110, Q111_
- **OC-2**: Elicitation suggests minimal expected disagreement on formal press [A4] but acknowledges fluidity for informal/politically charged Argentine content. Empirical labeling inconsistencies [DATASET-D17, D22, D27] suggest within-Canadian-context label noise that compounds any cross-cultural transfer concern. — _Sources: Q96, DATASET-D17, DATASET-D22, DATASET-D27_
- **OC-3**: INSUFFICIENT DOCUMENTATION on annotator demographics: paper specifies only research-group affiliation and meteorological expertise [Q110, Q111, Q104, Q105]; no nationality, language, age, gender, or cultural-context disclosure. No Datasheet or Data Statement equivalent provided.
- **OC-4**: Re-annotation by representative Argentine annotator pool would be necessary to validate transfer; no Argentine Spanish disaster benchmark exists [WEB-14, gap_id 7] to substitute. — _Sources: WEB-14_
- **OC-5**: Aggregation method is not documented (whether single-annotator-per-chunk, majority vote, or adjudication); paper says 'three domain annotators following our guidelines' [Q26] but does not specify inter-annotator agreement or aggregation procedure — INSUFFICIENT DOCUMENTATION on minority-perspective preservation.
- **OC-6**: Convergent validity is at risk: zero Argentine annotator representation, plus empirical labeling inconsistencies on chunks containing explicit casualties or major utility outages [DATASET-D17, D22, D27]. External validity to Argentine context cannot be established without re-annotation. — _Sources: Q96, DATASET-D17, DATASET-D22_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q26] 'Annotation is conducted by three domain annotators following our guidelines (provided in Appendix B.2.2).' (p.4)
- [Q110] 'The annotation process was conducted by members of a research group specializing in uncovering the history of a region's climate change through the regional historical weather records.' (p.15)
- [Q111] 'Their expertise can ensure the accuracy and reliability of annotations.' (p.15)
- [Q96] 'The interpretation of weather-related disruptions in historical newspapers might be influenced by demographic and contextual factors' (p.9)
- [Q47] 'annotations for these smaller chunks are performed independently by the same domain experts rather than automatically inherited from the original articles.' (p.6)

*Web sources:*
- [WEB-14] No complementary Argentine Spanish-language benchmark exists for cross-validation

*Dataset analysis:*
- DATASET-D17: 1998 Quebec ice storm chunk with 1M+ without power, -30°C, labeled all-zero — potential infrastructural and human_health under-labeling
- DATASET-D27: 1881 storm with skull fracture and child death labeled human_health=0
- DATASET-D22: China flood (810,000 homes collapsed) + Japan E. coli deaths labeled infra=1, human_health=0 — inconsistent with D21
- DATASET-D21: Indonesia minor injuries (20 people) labeled human_health=1 — inconsistent threshold vs. D22

</details>

**Information gaps:**
- Annotator nationality, language, and cultural-context demographics
- Inter-annotator agreement statistics and aggregation method
- Whether observed labeling inconsistencies (D17, D22, D27) reflect chunk-level re-annotation policy or genuine errors

**Requires expert verification:**
- Whether Argentine emergency management officials would assign positive labels to chunks like D17 and D27 under the same guideline criteria

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Output form consists of binary label vectors and ranked article lists [Q33, Q36, Q43–Q45, Q50], producing F1, accuracy, row-wise accuracy, Hit@1, nDCG@5, Recall@5, and MRR. These outputs are usable as upstream features for the deployment's downstream credibility aggregation per A3, so the form is functionally compatible. However, the benchmark does not natively produce the credibility/reliability score that constitutes the deployment's primary decision output, and the transformation from binary labels to credibility scores requires non-trivial integration with Argentine source metadata (outlet reach, account verification, institutional affiliation) that is unaddressed. Row-wise accuracy [Q45, Q75] provides a stricter evaluation that more closely approximates aggregation reliability needs. Output form is MODERATE-priority per elicitation; score reflects functional compatibility tempered by the non-trivial transformation gap and the absence of confidence/probability outputs that would be most useful for downstream aggregation.

**Strengths:**
- Binary label vectors and ranked lists are functionally compatible as upstream features for credibility aggregation per A3
- Multiple metrics including stricter row-wise accuracy [Q45] capture different aspects of reliability
- Standard IR metrics (Hit@1, nDCG@5, Recall@5, MRR) [Q50] for the QA task align with retrieval-pipeline evaluation
- Modest computational requirements [Q127, Q128] enable replication on Argentine-relevant content

**Checklist:**

- **OF-1**: Output modality (binary labels + rankings) is text-based and compatible with deployment's text channels; functional for upstream feature use [A3]. However, native credibility/reliability score is absent — the user accepts this and plans downstream aggregation [A3]. — _Sources: Q33, Q43_
- **OF-2**: Text-to-speech is not relevant: target users are policy professionals consuming text-based reports [target_population description]; literacy is near-universal (~99%) [WEB-2, WEB-3] and not a constraint. — _Sources: WEB-2, WEB-3_
- **OF-3**: Literacy and education are not limiting factors (target population holds advanced degrees; national literacy ~99% [WEB-2, WEB-3, WEB-4]). Output form's text-only nature is appropriate. — _Sources: WEB-2, WEB-3, WEB-4_
- **OF-4**: External validity gap: benchmark does not produce probability scores or confidence outputs that would be most useful for downstream credibility aggregation; only binary labels and discrete rankings. Integration with Argentine source metadata (outlet, account verification, institutional affiliation) is not addressed within benchmark scope. — _Sources: Q33, Q43_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'six ground-truth impacts Yt = {y^i_t}^6_i=1 with binary labels y^i_t ∈ {0, 1}' (p.5)
- [Q43] 'For multi-label classification task, we use F1-score, accuracy, and row-wise accuracy as evaluation metrics.' (p.6)
- [Q45] 'the row-wise accuracy is a strict metric that requires more accurate output as the model should correctly classify all six impact labels for a given article.' (p.6)
- [Q50] 'For the ranking-based QA task, we deploy the standard metric that emphasizes the accuracy of top positions for evaluation, including Hit@1, nDCG@5, Recall@5, and MRR.' (p.6)

*Web sources:*
- [WEB-2] Argentina national adult literacy ~99%
- [WEB-3] World Bank/UNESCO confirms literacy >98% since 2001
- [WEB-4] OECD 2025: 19% tertiary qualification among 25–34 year-olds; target cohort holds advanced degrees

*Dataset analysis:*
- DATASET-D16: multi-label output (infra=1, political=1, financial=1) demonstrates the binary-vector format in practice

</details>

**Information gaps:**
- Whether models can produce calibrated probability outputs in addition to binary labels for downstream credibility aggregation
- Specification of the Argentine source-metadata schema for credibility aggregation

**Requires expert verification:**
- Design of the credibility aggregation layer that combines benchmark outputs with Argentine source metadata

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Zero Spanish-language, Argentine, or social media content in benchmark corpus [Q97, WEB-14]

**Recommendation:** Construct an Argentine Spanish disaster impact test set drawing from Clarín, Infobae, La Nación, government press releases, and Twitter/X content covering AMBA flooding, sudestada, Pampa drought, and Patagonian wind events. Use Argentine emergency management experts as annotators. Use HumAID/CrisisBench as methodological reference (not direct content reference) given the English-language gap.

### Output Ontology ⚠

**Gap:** No native credibility/reliability output and no sub-labels for Argentine-specific granularity [Q117, A3]

**Recommendation:** Design and document the downstream credibility aggregation layer that A3 envisions, specifying Argentine source-metadata schema (outlet reach, account verification, AFE/SINAGIR/SMN actor recognition). Add sub-labels for villa miseria infrastructure, agricultural commodity specificity (soybean/maize/wheat), and partisan-framing political impact. Treat WXImpactBench outputs as one of several upstream features.

### Input Form ⚠

**Gap:** Long-form formal register only; deployment includes short-form informal Spanish social media [Q83, Q109, WEB-17]

**Recommendation:** Run a parallel evaluation on Spanish-translated tweet-length disaster content and on Argentine government press bulletins (~100–300 tokens) to quantify performance degradation relative to formal long-form benchmarks. Calibrate downstream credibility scoring to discount benchmark performance on informal channels by the measured gap.

### Output Content ⚠

**Gap:** Zero Argentine annotator representation; empirical labeling inconsistencies on positively-framed chunks [Q110, DATASET-D17, D22, D27]

**Recommendation:** Re-annotate a stratified sample (≥100 chunks) including the flagged inconsistencies (D17 ice storm, D22 China/Japan, D27 1881 storm) using ≥3 Argentine emergency management experts. Compute inter-annotator agreement against original Canadian labels to quantify cross-cultural drift, and use disagreements to inform Argentine-specific sub-label development per A4.

### Input Ontology

**Gap:** No task type for social media or short-form informal content; closed-retrieval QA only [Q18, Q89]

**Recommendation:** Augment evaluation with an open-retrieval QA task and a short-form social-media classification task using Argentine Twitter/X disaster content. Treat WXImpactBench's closed-retrieval scores as an upper-bound proxy and supplement with open-retrieval evaluation against an Argentine source corpus.

### Output Form

**Gap:** Binary labels only; no calibrated probability outputs for downstream credibility aggregation [Q33]

**Recommendation:** Re-run benchmark evaluation extracting model log-probabilities or calibrated confidence scores per label rather than binary outputs. Evaluate whether confidence calibration on WXImpactBench correlates with calibration on the Argentine test set built under remediation 1, to inform the credibility aggregation layer.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we first develop a disruptive weather impact dataset with a four-stage well-crafted construction pipeline." |
| Q2 | 1 | input_ontology | "we propose WXIMPACTBENCH, the first benchmark for evaluating the capacity of LLMs on disruptive weather impacts." |
| Q3 | 1 | input_ontology | "The benchmark involves two evaluation tasks, multi-label classification and ranking-based question answering." |
| Q4 | 1 | input_content | "The climate-related events stored in regional newspapers record how communities adapted and recovered from disasters." |
| Q5 | 1 | input_content | "However, the processing of the original corpus is non-trivial." |
| Q6 | 1 | output_form | "Extensive experiments on evaluating a set of LLMs provide first-hand analysis of the challenges in developing the understanding of disruptive weather impact and climate change adaptation systems." |
| Q7 | 1 | input_content | "Yongan Yu1, Qingchen Hu1, Xianda Du2, Jiayin Wang3, Fengran Mo4∗, Renée Sieber1*" |
| Q8 | 1 | input_content | "1McGill University, 2University of Waterloo, 3Tsinghua University, 4University of Montreal" |
| Q9 | 1 | input_content | "the challenge of identifying impacts and responses often lies in climate-related text processing, which contains period-specific narratives and domain-specific linguistic phenomena." |
| Q10 | 1 | input_ontology | "This polysemy occurs commonly in newspapers and thus requires the system to distinguish the literal weather-related meanings and alternate usages by improving the" |
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
| Q37 | 5 | input_ontology | "This setting could also facilitate RAG systems development in the domain (Mao et al., 2024; Mo et al., 2024c, 2025), where we left the answer span extraction/generation for future studies." |
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
| Q54 | 6 | input_form | "The relatively smaller models (with 7B size) ensure the latency requirements (Sun et al., 2023)." |
| Q55 | 6 | input_form | "The used models for the two tasks cover different sizes and support the input length of at least 8k tokens." |
| Q56 | 6 | input_form | "The multi-label classification is conducted on each evaluated LLM by the same prompt provided in Appendix C.2." |
| Q57 | 6 | input_ontology | "Different from traditional methods that decompose multi-label text classification into multiple binary classification tasks (Boutell et al., 2004; Liu et al., 2017), we simultaneously identify all relevant disruptive weather impacts for each input by calling the LLM once." |
| Q58 | 6 | input_form | "The example of in-context learning in the one-shot setting is handcrafted with a complex sample detailing multiple impacts." |
| Q59 | 6 | input_content | "We employ GPT-4O for pseudo question generation with default hyper-parameters." |
| Q60 | 6 | output_form | "For ranking evaluation, we adopt the sliding window mechanism within LLM-based ranker implementation following the state-of-the-art study (Sun et al., 2023) to reduce the potential negative effect of noisy long contexts." |
| Q61 | 7 | input_form | "Specifically, each article in the candidate pool was segmented into three chunks, and then the initial ranking was performed independently within each chunk." |
| Q62 | 7 | output_form | "To ensure stable results, following previous studies (Chen et al., 2023), all LLMs were evaluated with the temperature set to 0, and the reported performance is the average value of running the experiments three times." |
| Q63 | 7 | output_form | "Table 1 and Table 2 show the performance of the evaluated LLMs on WXIMPACTBENCH for the settings of categorized by six societal impacts with different context lengths, overall row-wise evaluation, and divided into two periods, respectively." |
| Q64 | 7 | output_ontology | "LLMs struggle to understand disruptive weather impacts." |
| Q65 | 7 | output_ontology | "Table 1 shows that the F1-score for multi-label classification remains consistently low across models, especially among the political and ecological categories." |
| Q66 | 7 | output_form | "The financial, agricultural, and human health impacts categories perform slightly better but still exhibit suboptimal results at 55%." |
| Q67 | 7 | output_ontology | "The low performance might be attributed to the challenges in these categories with abstract and context-dependent narratives." |
| Q68 | 8 | output_form | "Table 2 shows row-wise performance, in which the model must identify the given sample correctly for each involved category, the performance of classification drops dramatically due to the more precise requirement." |
| Q69 | 8 | input_content | "Thus, a sophisticated model is expected to understand the complex societal effects of historical narratives via reasoning (Wei et al., 2022; Zhang et al., 2025a,b)." |
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
| Q88 | 9 | output_content | "Notice that the ranking results would contain bias when the evaluated model is used for question generation (GPT-4O in our cases). This is a common phenomenon (Zhou et al., 2023) and needs to be avoided in benchmarking." |
| Q89 | 9 | input_ontology | "The practical open-retrieval setting, i.e., identifying the relevant articles from a huge database, is left for future studies, which could further facilitate knowledge enhancement in understanding disruptive weather impacts." |
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
| Q102 | 14 | output_ontology | "In the absence of standardized impact records (e.g., flood-related property damage, injuries due to ice accumulation, power outages, and road closures), we assessed vulnerabilities and resilience based on the consequences of weather events and how they have changed since the 19th century." |
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
| Q118 | 16 | output_ontology | "The guidelines emphasize focusing on direct and immediate effects, ensuring that classifications are based solely on explicit references within the text." |
| Q119 | 16 | input_ontology | "The ranking-based QA task consists of two key components: question generation (Mo et al., 2023) and candidate ranking (Meng et al., 2024)." |
| Q120 | 16 | input_form | "Figure 6 presents the token length distribution of passages in two versions of our dataset: (a) the Long Context dataset and (b) the Mixed Context dataset used for context-denoising evaluation." |
| Q121 | 16 | input_content | "The Long Context dataset (Figure 6a), which contains 350 articles, exhibits a broader distribution of passage lengths, with a significant portion exceeding 2000 tokens." |
| Q122 | 16 | input_content | "The Mixed Context dataset (Figure 6b), which contains 1,386 articles, is heavily skewed toward shorter passages, with an overwhelming majority containing fewer than 2000 tokens." |
| Q123 | 16 | input_ontology | "GPT-4O, GPT-4 and GPT-3.5-TURBO are provided by OpenAI, the base model API document: https://platform.openai.com/docs/models" |
| Q124 | 16 | input_ontology | "DEEPSEEK-V3-671B is upgraded the DEEPSEEK-CHAT, the base model API" |
| Q125 | 17 | input_form | "Given the following passage about {row['Weather']}, generate a single, focused question that meets these criteria: 1. Can be answered using ONLY the information in this passage 2. Focuses on the {impact_str} impacts mentioned 3. Is detailed and specific to this exact situation 4. Requires understanding the passage's unique context 5. Cannot be answered by other similar passages about {row['Weather']} Passage: {row['Text']}" |
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
| WEB-1 | https://www.argentina.gob.ar/sinagir/institucional |
| WEB-2 | https://countryeconomy.com/demography/literacy-rate/argentina |
| WEB-3 | https://www.macrotrends.net/global-metrics/countries/arg/argentina/literacy-rate |
| WEB-4 | https://gpseducation.oecd.org/CountryProfile?primaryCountry=ARG&treshold=10&topic=EO |
| WEB-5 | https://datareportal.com/reports/digital-2026-argentina |
| WEB-6 | https://www.trade.gov/country-commercial-guides/argentina-digital-economy |
| WEB-7 | https://freedomhouse.org/country/argentina/freedom-net/2024 |
| WEB-8 | https://ts2.tech/en/state-of-internet-access-in-argentina-fiber-5g-and-satellite-in-2025/ |
| WEB-9 | https://oavv.segemar.gob.ar/sinagir/ |
| WEB-10 | https://www.lexology.com/library/detail.aspx?g=d696be0e-4476-4c8c-83f9-6360dd701d70 |
| WEB-11 | https://intellectual-property-helpdesk.ec.europa.eu/news-events/news/draft-law-protection-personal-data-argentina-2024-01-09_en |
| WEB-12 | https://digital.nemko.com/regulations/ai-regulation-argentina |
| WEB-13 | https://www.theworldlawgroup.com/membership/news/news-argentina-releases-guidelines-for-responsible-ai-implementation |
| WEB-14 | https://crisisnlp.qcri.org/humaid_dataset |
| WEB-15 | https://ojs.aaai.org/index.php/ICWSM/article/download/18116/17919/21611 |
| WEB-16 | https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-025-00534-0 |
| WEB-17 | https://www.semanticscholar.org/paper/HumAID:-Human-Annotated-Disaster-Incidents-Data-Alam-Qazi/462cc2046ef4d48d844813b66d8a1ed6dfda3bc0 |
| WEB-18 | https://www.mofo.com/artificial-intelligence/argentina |
| WEB-19 | https://www.jurist.org/commentary/2025/12/why-argentinas-pioneering-privacy-law-is-now-playing-defense-against-ai/ |
| WEB-20 | https://crisisnlp.qcri.org/ |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** Michaelyya/wximpactbench-1386 (mixed-context / chunked version)
**Analysis date:** 2025-07-10
**Examples reviewed:** 31 from `train` split
**Columns shown:** id, date, time_period, weather_type, text, infrastructural_impact, political_impact, financial_impact, ecological_impact, agricultural_impact, human_health_impact
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | wximpactbench-1386 | Ex. 1 (id=198) | all zeros | "John's Cloudy -4 -4 United States Max Min Atlanta Cloudy 17 4 Boston Cloudy 3 -6 Chicago Cloudy 2 2 Dallas Thunderstorms 11 2..." | Weather forecast table with temperature/condition data; no impact content | IO, IC |
| D2 | wximpactbench-1386 | Ex. 2 (id=199) | all zeros | "But the real beneficiaries of the work-at-home trend are the employees themselves... She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9) Down 1, Full of ill-will and disease (9)..." | Non-weather content: work-from-home editorial + crossword puzzle clues | IO, IC |
| D3 | wximpactbench-1386 | Ex. 4 (id=89) | all zeros | "Clarkson was arrested July 16 as he left the Glenora home of Marilyn Tan... Clarkson is currently charged with conspiracy to murder photographer Con Boland." | Crime reporting with no weather content; zero-impact label justified | IO, IC |
| D4 | wximpactbench-1386 | Ex. 5 (id=98) | all zeros | "Polls have suggested that the party still may be able to win the 10 per cent of 12 million votes in eastern Germany that are needed to secure seats in the Bonn parliament." | Post-reunification German politics (East Germany, Berlin Wall anniversary); no weather | IO, IC |
| D5 | wximpactbench-1386 | Ex. 9 (id=82) | all zeros | "Peter Russell, a law professor at the University of Toronto, said the Supreme Court will benefit from Binnie's solid experience in constitutional and international affairs." | Canadian Supreme Court appointment reporting; no weather content | IO, IC |
| D6 | wximpactbench-1386 | Ex. 11 (id=212) | all zeros | "They refused to give any indication as to where they got the silver, but Mr. Dunnuis joined the tribe, married an Indian girl and thus learned their secret." | Historical narrative about Indigenous land/mining; no weather impact | IO, IC |
| D7 | wximpactbench-1386 | Ex. 19 (id=92) | all zeros | "National Lampoon's Van Wilder 2: The Rise of Taj Starring: Kal Penn, Lauren Cohan and Daniel Percival Playing at: AMC, Brossard, Cavendish, Colossus, LaSalle cinemas." | Film review; no weather content at all | IO, IC |
| D8 | wximpactbench-1386 | Ex. 25 (id=83) | all zeros | "His mother, whose maiden name was O'Malley, actually was adopted, Cascarino wrote in his autobiography. Ireland actually does have a regulation that allows offspring of children adopted by Irish parents to assume Irish citizenship." | Sports journalism (soccer eligibility rules); no weather content | IO, IC |
| D9 | wximpactbench-1386 | Ex. 28 (id=88) | all zeros | "'He can get his fastball up to 93 (mph) and averages out at 90-91.'" | Baseball scouting report; no weather content | IO, IC |
| D10 | wximpactbench-1386 | Ex. 29 (id=92) | all zeros | "Kennedy dramatically quit the race after only the second ballot, instantly propelling Dion into first place on the third ballot..." | Canadian Liberal Party leadership race; no weather content | IO, IC |
| D11 | wximpactbench-1386 | Ex. 21 (id=330) | all zeros | "Just two hours before this, in Richmond, the storm so long expected has broken forth in all its fury. Great flashes of blinding lightning intermingled with the grand roar of the thunder from on high..." | Literary/fictional storm passage embedded in historical newspaper; labeled all-zero | OC, IO |
| D12 | wximpactbench-1386 | Ex. 13 (id=213) | all zeros | "Rev. Principal Grant, of Queen's University, Kingston, Ont, lectured on the subject of 'Canada First.'... With regard to unrestricted commercial intercourse between the two countries..." | Political/trade speech; no weather content | IO, IC |
| D13 | wximpactbench-1386 | Ex. 31 (id=214) | all zeros | "The Legislative council has refused to abolish itself. The government bill, enacting abolition, adopted unanimously by the lower House, was referred to the committee of privilege in the council." | Canadian legislative politics; no weather content | IO, IC |
| D14 | wximpactbench-1386 | Ex. 3 (id=26) | infrastructural=1, others=0 | "by six o'clock the electric car services in all the important points west of Toronto had been completely paralyzed... an unprecedented snowfalls and heavy winds." | 1894 blizzard; infrastructure (transit) disruption labeled; North American geography | IO, OC, IC |
| D15 | wximpactbench-1386 | Ex. 17 (id=26) | infrastructural=1, others=0 | "TRAFFIC IS PARALYZED In Western Canadian Cities, and at Many Points In the United States Disasters In England." | Different chunk of same 1894 blizzard article; ads for Montreal-based construction suppliers surround weather content | IC, IF |
| D16 | wximpactbench-1386 | Ex. 14 (id=34) | infra=1, political=1, financial=1 | "Aid Laurent said that there were mountains of snow all over the city. Already $30,000 has been expended in removing it... Seven hundred and fifty men and 450 carters were employed..." | 1887 Montreal snow removal debate in city council; all three labeled labels are plausible | OC, OO |
| D17 | wximpactbench-1386 | Ex. 12 (id=87) | all zeros | "PETER MARTIN, GAZETTE Workers from the Connecticut Light and Power Co were working to reconnect power lines on Oxford Ave in Notre Dame de Grace... Temperatures plummet; today's high minus-15C... more than one million people struggle on without power or heat" | 1998 Quebec ice storm coverage describing power outages and extreme cold; labeled all-zero — potential annotation gap | OC, OO |
| D18 | wximpactbench-1386 | Ex. 23 (id=225) | agricultural=1, human_health=1 | "more than 100,000 homes damaged and crops on about 175,000 hectares of farmland destroyed... death toll in Chongqing in China's southwest rose to 42 people and 12 missing from torrential downpours" | 2007 global flood roundup (England, China, Pakistan) — non-Canadian events used as positive examples | IC, IO |
| D19 | wximpactbench-1386 | Ex. 26 (id=215) | political=1, ecological=1 | "A line of freak thunderstorms rumbling across the northeastern Mediterranean coast from Spain and southern France to the principality of Monaco brought two days of disastrous flash flooding... Raging waters uprooted trees and swept away cars as river levels rose by as much as 3 metres" | Mediterranean flooding; ecological and political labels assigned; non-Canadian geography | IC, OC |
| D20 | wximpactbench-1386 | Ex. 27 (id=101) | ecological=1 | "The Everglades ecosystem is not ranked as an equal partner with agricultural and urban demands... about half the original 1.6-million-hectare swamp filled for development or drained for agriculture" | US ecological/conservation article (Everglades, drought context); ecological impact labeled | IO, OC |
| D21 | wximpactbench-1386 | Ex. 8 (id=138) | infra=1, human_health=1 | "hundreds of houses, schools and other buildings sustained damage when one of the twin peaks of the volcano exploded. At least 20 people sustained minor injuries... The most powerful earthquake to strike western Washington state in 30 years injured four people" | 1999 global disaster roundup (Indonesia, Washington state, NZ, Romania); labeled positive | IC, IO |
| D22 | wximpactbench-1386 | Ex. 7 (id=88) | infrastructural=1 | "Almost 4 million people across China had been cut off by flood waters, 810,000 homes have collapsed and 2.8 million homes have been damaged in eight provinces... Japan struck at young and old yesterday, killing a schoolgirl and an 85-year-old woman" | 1996 China Yangtze floods + Japan E. coli outbreak in same chunk; infrastractural=1 but human_health=0 despite explicit casualties | OC, OO |
| D23 | wximpactbench-1386 | Ex. 16/30/24/1 (id=198, multiple) | all zeros | "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25..." / "Escenvt 115780 298 J80 289 19 Caiunoil 8000 J9 J9 29..." | OCR-corrupted stock market tables; repeated for same article id across multiple rows | IF, IC |
| D24 | wximpactbench-1386 | Ex. 10 (id=304) | all zeros | "After the accident they suffered severely from the cold... All their provisions, anchor, cooking utensils, signal lights, and several other articles which were not lashed to the boat were lost." | 1896 transatlantic rowboat adventure; cold/weather mentioned in passing; long chunk heavily dominated by stock listings and patent medicine ads | IF, IC |
| D25 | wximpactbench-1386 | Ex. 18 (id=197) | all zeros | "The walkout will interrupt regular garbage collection and will affect street and sidewalk cleanup if it snows... Unless nine centimetres or more of snow falls during the walkout, blue-collar workers aren't obliged to clean the streets and sidewalks." | 1991 Montreal labor dispute about snow removal thresholds; weather mentioned indirectly; all-zero label | OC, OO |
| D26 | wximpactbench-1386 | Ex. 22 (id=183) | all zeros | "the peninsula - the tongue of land that juts toward South America - has been hit by greater warming than almost any other area on Earth" | 2009 climate change article about Antarctic Peninsula warming; no direct societal impact labeled despite ecological relevance | OC, OO |
| D27 | wximpactbench-1386 | Ex. 6 (id=252) | all zeros | "A poor lady passenger was dashed to leeward and had her skull fractured. She was landed this morning in a dying state with a coffined child that succumbed last night to its sufferings." | 1881 Atlantic storm with explicit casualties (skull fracture, child death) labeled all-zero | OC, OO |
| D28 | wximpactbench-1386 | Ex. 20 (id=15) | all zeros | "pointing out the impossibility of making satisfactory quotations for New York exchange... the movement of the crops, which, under the present circumstances, will be a most troublesome proceeding" | 1893 banking/financial crisis article; agricultural (crop movement) and financial framing present but labeled all-zero | OC, OO |

---

### Deployment-Relevant Strengths

#### Strength 1: Six impact labels are operationally present and distinguishable in the data
- **Dimension(s):** IO, OO
- **Observation:** The sampled data contains positive examples for infrastructural (Ex. 3, 7, 8, 17), political (Ex. 14, 26), financial (Ex. 14), ecological (Ex. 26, 27), agricultural (Ex. 23), and human health (Ex. 8, 23) impacts, confirming that the benchmark's six label dimensions are not theoretical — they appear with varying frequency across both historical and modern articles.
- **Deployment relevance:** Argentine policy makers assessing disaster impact reports would plausibly use all six of these categories. The fact that real labeled examples exist for each provides a minimum empirical basis for evaluating LLM classification capability across the full output ontology.
- **Datapoint citations:**
  - [D14] Example 3 (train, infrastructural=1): "by six o'clock the electric car services in all the important points west of Toronto had been completely paralyzed" — positive infrastructural label grounded in explicit service disruption text
  - [D16] Example 14 (train, infra=1, political=1, financial=1): "Already $30,000 has been expended in removing it, and they did not know what to do even now" — multi-label case demonstrating simultaneous financial + political + infrastructural assignment
  - [D18] Example 23 (train, agricultural=1, human_health=1): "crops on about 175,000 hectares of farmland destroyed...death toll in Chongqing in China's southwest rose to 42 people" — agricultural and health co-occurrence present in data

#### Strength 2: Negative-example chunks are genuinely diverse and challenging
- **Dimension(s):** IO, IF
- **Observation:** The mixed-context chunking strategy produces a large variety of zero-label examples spanning weather forecast tables (Ex. 1), crossword clues (Ex. 2), film reviews (Ex. 7/19), sports coverage (Ex. 9/28), political reporting (Ex. 5/29/31), legal proceedings (Ex. 4), and stock market tables (Ex. 16/30). These negative examples make the classification task non-trivially hard and prevent models from using simple keyword cues.
- **Deployment relevance:** In the Argentine deployment, the system must distinguish real disaster impact signals from noise across heterogeneous source channels. The benchmark's inclusion of topically diverse negative examples exercises a similar noise-rejection capability.
- **Datapoint citations:**
  - [D2] Example 2 (train, all zeros): "She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9) Down 1, Full of ill-will and disease (9)" — crossword puzzle text that shares no surface features with disaster reporting
  - [D7] Example 19 (train, all zeros): "National Lampoon's Van Wilder 2: The Rise of Taj Starring: Kal Penn, Lauren Cohan and Daniel Percival Playing at: AMC, Brossard, Cavendish, Colossus, LaSalle cinemas." — film review; tests model's resistance to false-positive labeling
  - [D10] Example 29 (train, all zeros): "Kennedy dramatically quit the race after only the second ballot, instantly propelling Dion into first place" — political content that might confuse political impact classification

#### Strength 3: Multi-label complexity provides a realistic evaluation of joint classification difficulty
- **Dimension(s):** OO, OF
- **Observation:** Several examples in the sample exhibit multi-label ground truth (e.g., Ex. 14 with three simultaneous positive labels; Ex. 23 with two), while the majority are all-zero. This mirrors the real task structure that Argentine policy users would face when a single report contains mixed signals across impact types.
- **Deployment relevance:** Disaster reports in Argentina (e.g., AMBA flooding triggering both infrastructure damage and health risks) would require simultaneous multi-label assessment; the benchmark exercises this capability.
- **Datapoint citations:**
  - [D16] Example 14 (train, infra=1, political=1, financial=1): "Aid Laurent said that there were mountains of snow all over the city. Already $30,000 has been expended in removing it" — three-label case
  - [D18] Example 23 (train, agricultural=1, human_health=1): "crops on about 175,000 hectares of farmland destroyed...death toll in Chongqing...rose to 42 people" — two-label case with different category combination

#### Strength 4: Both historical and modern-period articles are present, covering two linguistic registers
- **Dimension(s):** IF, IC
- **Observation:** The sample includes articles dated from 1881 to 2009, with time_period labeled "historical" or "modern." Historical texts (Exs. 3, 6, 10, 14, 17) use ornate 19th-century prose with archaic spelling and syntax; modern texts (Exs. 7, 18, 22, 23) use contemporary journalistic register. This variation exercises LLM linguistic robustness.
- **Deployment relevance:** While neither register matches contemporary Argentine informal social media, the two-period design at least probes whether LLM performance degrades with register shift — a methodologically relevant question for any register-mismatched deployment.
- **Datapoint citations:**
  - [D14] Example 3 (train, historical, 1894): "Sunday evening's despatches brought the news that a very severe blizzard was prevailing in Kansas" — archaic vocabulary and syntax
  - [D18] Example 23 (train, modern, 2007): "Military helicopters have rescued more than 100 people from rooftops, trailer parks and a bridge as well as strips of land cut off by water" — contemporary wire-service register

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Extremely high proportion of zero-label off-topic chunks undermine benchmark relevance signal
- **Dimension(s):** IO, IC
- **Observation:** Of 31 sampled examples, at least 20 (≈ 65%) are all-zero and contain content that is not merely low-impact weather reporting but is entirely unrelated to weather or disaster: crossword puzzles (Ex. 2), film reviews (Ex. 7/19), crime reporting (Ex. 4), sports coverage (Ex. 9/28), stock market tables (Exs. 16, 23, 30), political leadership contests (Exs. 5, 29), and legal proceedings (Ex. 4). These chunks apparently result from the mixed-context segmentation of full newspaper pages, where LDA topic selection operated at the article level but chunking produces segments from adjacent, unrelated page content.
- **Deployment relevance:** For the Argentine policy deployment, the benchmark's headline claim is that it evaluates LLM capability on disaster impact classification. If the majority of test examples are chunks of crossword clues and stock tickers with a trivially correct all-zero label, the benchmark's discriminative validity for impact classification is substantially diluted. A model that outputs all-zero for every input would achieve high accuracy on these examples. This casts doubt on whether benchmark scores reflect genuine disaster-impact understanding.
- **Datapoint citations:**
  - [D2] Example 2 (train, all zeros): "She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9) Down 1, Full of ill-will and disease (9) 2, There's a place for Belgians up in Rumania (5)" — crossword puzzle; no conceivable weather-impact content
  - [D7] Example 19 (train, all zeros): "National Lampoon's Van Wilder 2: The Rise of Taj Starring: Kal Penn, Lauren Cohan and Daniel Percival Playing at: AMC, Brossard, Cavendish, Colossus, LaSalle cinemas. Parents' guide: Sexual content markers." — film review fragment
  - [D9] Example 28 (train, all zeros): "'He can get his fastball up to 93 (mph) and averages out at 90-91.'" — baseball scouting; no weather or disaster relevance
  - [D23] Examples 1/16/24/30 (train, all zeros, same id=198): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25..." — OCR-corrupted stock market tables repeated across multiple rows for the same article id

#### Concern 2: Multiple examples with identical article id across chunks indicate severe data leakage/duplication in the sampled rows
- **Dimension(s):** IF, OC
- **Observation:** Article id=198 (date=19920204) appears in at least four of the 31 sampled rows (Exs. 1, 15/16, 24, 30) with different text fragments but the same metadata. Article id=26 appears in at least two rows (Exs. 3, 17) and id=88 in at least two rows (Exs. 7, 28). This is expected by design (the 350 full articles are chunked into 1,386 segments), but means that a substantial fraction of sampled examples share underlying source article metadata. The id=198 chunks include weather forecast tables (all zeros) and OCR-corrupted stock listings (all zeros), confirming that the segmentation cuts across multiple unrelated page elements.
- **Deployment relevance:** For Argentine policy evaluation, benchmark score interpretability depends on whether positive-labeled chunks and negative-labeled chunks from the same underlying article are truly independent test items. They share OCR artifacts, temporal context, and annotator. Models with memory of earlier chunks from the same article may receive implicit contextual advantage not available in single-document deployment scenarios.
- **Datapoint citations:**
  - [D1] Example 1 (id=198, all zeros): "John's Cloudy -4 -4 United States Max Min Atlanta Cloudy 17 4" — weather table chunk
  - [D23] Example 16 (id=198, all zeros): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25" — stock table chunk from same article id
  - [D14] Example 3 (id=26, infra=1): "by six o'clock the electric car services in all the important points west of Toronto had been completely paralyzed" — positive chunk
  - [D15] Example 17 (id=26, infra=1): "TRAFFIC IS PARALYZED In Western Canadian Cities" — different chunk of same article, same label

---

#### MAJOR

#### Concern 3: Potential annotation errors on positive-content chunks labeled all-zero
- **Dimension(s):** OC, OO
- **Observation:** Several chunks contain content that prima facie warrants positive labels under the benchmark's own annotation guidelines but are labeled all-zero. (a) Ex. 12 (id=87, 1998 Quebec ice storm): describes over one million people without power/heat and temperatures of minus-30°C — which maps directly to the "Infrastructural Impact" criterion (interruptions to utilities; power supply). (b) Ex. 6 (id=252, 1881 Atlantic storm): describes a woman with fractured skull and a dead child after a storm — explicit casualties that map to "Human Health Impact" per criterion Q145 ("direct injuries or fatalities"). (c) Ex. 25 (id=197, 1991 Montreal labor strike): discusses snow removal thresholds and traffic disruption — borderline case but mentions explicit infrastructure service thresholds. These may reflect the independent chunk-level re-annotation policy (Q47), but they raise concerns about annotation consistency.
- **Deployment relevance:** If the benchmark contains systematic under-labeling of positive-content chunks, LLMs that correctly identify these impacts would be penalized as false positives, artificially suppressing recall metrics. For Argentine policy users who care about not missing disaster signals, benchmark recall figures may be underestimated.
- **Datapoint citations:**
  - [D17] Example 12 (train, id=87, all zeros): "more than one million people struggle on without power or heat... overnight lows in Montreal were expected to drop to minus-16 Celsius last night and tumble as far as minus-30C on the South Shore" — explicit utility outage and human exposure to dangerous cold; infra=0 and human_health=0
  - [D27] Example 6 (train, id=252, all zeros): "A poor lady passenger was dashed to leeward and had her skull fractured. She was landed this morning in a dying state with a coffined child that succumbed last night to its sufferings." — explicit casualties from a storm; human_health=0
  - [D25] Example 18 (train, id=197, all zeros): "The walkout will interrupt regular garbage collection and will affect street and sidewalk cleanup if it snows" — snow-triggered service disruption framed as labor context; infra=0

#### Concern 4: Inconsistent human-health labeling across co-occurring disaster content
- **Dimension(s):** OC, OO
- **Observation:** Ex. 7 (id=88, 1996) covers China Yangtze floods (explicitly "810,000 homes have collapsed" and "2.8 million homes have been damaged") alongside Japan E. coli outbreak deaths ("killing a schoolgirl and an 85-year-old woman"). Infrastructural=1 is assigned but human_health=0, despite explicit casualties from both flood and foodborne illness. By contrast, Ex. 8 (id=138, 1999) covering Indonesian volcanic eruption injuries receives human_health=1. The criterion for human health (Q145) includes "direct injuries or fatalities (including cases where zero or more casualties are explicitly mentioned)."
- **Deployment relevance:** Inconsistent health-impact labeling is directly relevant to the Argentine deployment, where human health impacts (flood casualties, disease outbreaks in villas miseria post-flooding) are a primary policy concern. Unreliable health-label ground truth would undermine the benchmark's validity for evaluating whether LLMs can detect this dimension.
- **Datapoint citations:**
  - [D22] Example 7 (train, id=88, infra=1, human_health=0): "Almost 4 million people across China had been cut off by flood waters... the food-poisoning outbreak gripping Japan struck at young and old yesterday, killing a schoolgirl and an 85-year-old woman, and bringing the death toll to seven" — explicit multi-country casualty content; human_health=0
  - [D21] Example 8 (train, id=138, infra=1, human_health=1): "At least 20 people sustained minor injuries, including some who were injured after falling off their motorbikes during the strong quake that accompanied the eruption" — minor injuries (20 people) labeled human_health=1

#### Concern 5: Non-Canadian global disaster content is labeled with benchmark's impact categories without geographic scope limitation
- **Dimension(s):** IC, OC
- **Observation:** Several positively-labeled examples describe disasters in China (Ex. 7: Yangtze floods), Pakistan (Ex. 23: flash floods), England (Ex. 23: flooding), Indonesia (Ex. 8: volcanic eruption), the US Pacific Northwest (Ex. 8: earthquake), and the Mediterranean (Ex. 26: thunderstorm flooding). These are reported in Montreal Gazette articles as international wire-service content. The benchmark's annotation guidelines do not restrict classification to Canadian events, meaning the label ontology has been applied to globally diverse disaster geographies. This partially mitigates the concern about purely Canadian framing — impact categories are applied to South/East Asian and European contexts — but the operationalization still reflects North American institutional annotation perspectives.
- **Deployment relevance:** The presence of non-Canadian labeled examples is actually somewhat positive for the Argentine deployment: it confirms the annotation categories are applied to internationally sourced disasters, not exclusively domestic Canadian events. However, none of the international events represent South American geography, Argentine disaster types, or Spanish-language source content.
- **Datapoint citations:**
  - [D18] Example 23 (train, agricultural=1, human_health=1): "the death toll in Chongqing in China's southwest rose to 42 people and 12 missing from torrential downpours that have affected up to 6.8 million people" — Chinese disaster labeled with benchmark categories
  - [D19] Example 26 (train, political=1, ecological=1): "A line of freak thunderstorms rumbling across the northeastern Mediterranean coast from Spain and southern France to the principality of Monaco brought two days of disastrous flash flooding to the resort region" — Mediterranean European disaster labeled; no North American event
  - [D21] Example 8 (train, infra=1, human_health=1): "Reports from Indonesia's Flores Island tell of moderate damage and minor injuries during the July 1 eruption of Mt. Lewotobi" — Indonesian volcanic event labeled

#### Concern 6: Literary/fictional storm passages and non-weather narrative fragments are present in the dataset
- **Dimension(s):** IO, IC
- **Observation:** Ex. 21 (id=330, historical, Thunder) contains what appears to be a Victorian serialized novel excerpt embedded in the newspaper: "Just two hours before this, in Richmond, the storm so long expected has broken forth in all its fury. Great flashes of blinding lightning intermingled with the grand roar of the thunder from on high; while ever and anon the passionate bursts of rain flung themselves against the window panes of the hotel, almost drowning the gay laughter and merry voices of those within." This is labeled all-zero and weather_type=Thunder, but the "storm" is clearly a literary/metaphorical device in a fictional narrative, not a real weather event. Models that detect the storm language as weather-relevant and assign impact labels would be penalized for false positives.
- **Deployment relevance:** In the Argentine deployment, social media content frequently employs weather metaphors, emotional storm language, or colloquial expressions ("tormenta política," "lluvia de críticas") that are not literal weather events. The presence of literary weather text in this benchmark provides some minimal analog to this figurative language challenge, but it is not the same as Argentine vernacular metaphor — it is 19th-century English Victorian fiction.
- **Datapoint citations:**
  - [D11] Example 21 (train, id=330, all zeros): "Just two hours before this, in Richmond, the storm so long expected has broken forth in all its fury. Great flashes of blinding lightning intermingled with the grand roar of the thunder from on high; while ever and anon the passionate bursts of rain flung themselves against the window panes of the hotel, almost drowning the gay laughter and merry voices of those within" — weather language is fictional narrative, not a real event; model must distinguish literal from literary

---

#### MINOR

#### Concern 7: OCR-corrupted stock market and financial table chunks are present as valid training/test rows
- **Dimension(s):** IF
- **Observation:** Multiple chunks (Exs. 1, 16, 24, 30) from the same article (id=198, 1992-02-04) contain heavily OCR-corrupted financial table data: "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25..."; "Escenvt 115780 298 J80 289 19 Caiunoil 8000 J9 J9 29..." These are not corrected by the post-OCR pipeline — they remain as garbled strings of numbers and partial tokens. They are labeled all-zero, which is correct, but they constitute noise inputs that neither resemble weather articles nor the Argentine deployment's social media/press content.
- **Deployment relevance:** These corrupted table chunks indicate that the post-OCR correction pipeline did not fully clean tabular or numerical page elements, and that such fragments appear in the benchmark as valid test items. This reinforces the concern that benchmark performance metrics are partly driven by trivially correct all-zero classifications of non-text content.
- **Datapoint citations:**
  - [D23] Example 16 (train, id=198, all zeros): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35 -1 Gift sir 14000 33 30 33 1 Aloha gld 10000 85 80 80 5 Clinedev 1600 0 0 0" — OCR garbage from financial tables; still included as benchmark row
  - [D23] Example 30 (train, id=198, all zeros): "Escenvt 115780 298 J80 289 19 Caiunoil 8000 J9 J9 29 Eurkav 6200 JO 18 18 Clgrphy 3100 345 330 345 5 Euroormf 10000 4 4 4" — second corrupted financial table chunk from same article

#### Concern 8: Zero-label climate/environmental context chunks that may matter for Argentine ecological framing
- **Dimension(s):** OC, OO
- **Observation:** Ex. 22 (id=183, 2009) describes Antarctic Peninsula warming with reference to South America: "the peninsula - the tongue of land that juts toward South America - has been hit by greater warming than almost any other area on Earth." This is labeled all-zero (ecological_impact=0). Under the benchmark's annotation criteria (Q143: "Classify as 'true' if the text mentions any effects on natural environments and ecosystems"), this passage describing measurable environmental change at scale plausibly warrants an ecological label, but it lacks an "immediate" weather event trigger. Similarly, Ex. 28 (id=15, 1893) contains agricultural movement context ("the movement of the crops, which, under the present circumstances, will be a most troublesome proceeding") linked to financial crisis, labeled all-zero.
- **Deployment relevance:** For Argentine ENSO-driven drought assessment, ecological and agricultural framing of longer-term climate dynamics (not a single acute event) is a key policy interest. If the annotation guidelines strictly exclude such content as "not direct and immediate," the benchmark may underrepresent the slow-onset disaster assessment tasks Argentine policy users face.
- **Datapoint citations:**
  - [D26] Example 22 (train, id=183, all zeros): "the peninsula - the tongue of land that juts toward South America - has been hit by greater warming than almost any other area on Earth" — large-scale ecological change, all-zero
  - [D28] Example 20 (train, id=15, all zeros): "the movement of the crops, which, under the present circumstances, will be a most troublesome proceeding, easy everywhere" — crop disruption in financial context, agricultural_impact=0

#### Concern 9: weather_type field is populated with "Nan" for a substantial proportion of examples
- **Dimension(s):** IO
- **Observation:** Of 31 sampled examples, 19 have weather_type="Nan" (not a weather type string, but the literal string "Nan" or null). Examples with weather_type populated (Snow, Rain, Drought, Freezing, Thunder, Cold, Deluge) tend to contain more weather-relevant content, but several weather_type="Nan" examples contain genuine weather content (e.g., Ex. 7 on China floods; Ex. 22 on Mediterranean flooding). The weather_type field does not appear to be a reliable metadata indicator of whether the chunk contains weather content.
- **Deployment relevance:** This metadata quality issue is minor for scoring but indicates that the benchmark's topic-modeling article selection (LDA-based, 15 weather event types per Q101) did not translate cleanly into chunk-level weather type metadata. For Argentine deployment validation purposes, this reduces the utility of the weather_type field as a stratification variable.
- **Datapoint citations:**
  - [D22] Example 7 (train, weather_type=Nan, infra=1): "Almost 4 million people across China had been cut off by flood waters" — flood content but weather_type=Nan
  - [D19] Example 26 (train, weather_type=Thunder, political=1, ecological=1): "A line of freak thunderstorms rumbling across the northeastern Mediterranean coast" — weather_type populated and consistent with content
  - [D3] Example 4 (train, weather_type=Nan, all zeros): "Clarkson was arrested July 16 as he left the Glenora home of Marilyn Tan" — no weather; weather_type=Nan correctly absent

---

### Content Coverage Summary

The 31 sampled examples from the mixed-context (1,386-sample) version of WXImpactBench are predominantly all-zero negative examples (≈65%), most of which contain content entirely unrelated to weather or disaster: sports coverage, film reviews, political news, crossword puzzles, and OCR-corrupted financial tables. This is an expected artifact of the chunking strategy — full newspaper pages are segmented into ~250-token chunks regardless of content type, meaning many chunks capture page elements (advertisements, stock tables, crossword grids, crime briefs) that co-occurred on the same page as a weather article selected by LDA.

The positively-labeled examples cover: North American historical blizzards (1894 Montreal/Ontario, labeled infrastructural), 19th-century Montreal snow removal debates (multi-label), 1990s–2000s global disaster round-up articles from the Montreal Gazette (China floods, Mediterranean flooding, Indonesian eruption, Pakistani flash floods), and US ecological articles (Everglades drought). The geographic and event-type diversity in positive examples is broader than "Canadian weather only" — it extends to international wire service content — but no South American, Argentine, or Spanish-language content appears.

Register is uniformly formal English journalism across both periods. Archaic 19th-century prose (ornate syntax, shipping reports, pharmaceutical advertisements) coexists with late-20th-century wire-service brevity. Neither register resembles the informal, social-media, short-form Rioplatense Spanish content that constitutes the Argentine deployment's highest-priority input channel.

Label consistency across positively coded examples raises reviewable questions: explicit casualties in an 1881 storm (fractured skull, child death) are labeled human_health=0; the 1998 Quebec ice storm with one million people without power is labeled infrastructural=0; while minor injuries in an Indonesian volcanic eruption are labeled human_health=1. These patterns are consistent with the chunk-level independent re-annotation design but indicate variability that downstream users should be aware of.

---

### Limitations

1. **Sample size:** 31 examples from a 970-row training split is a small sample (≈3.2%). The proportion of off-topic zero-label chunks observed here may be higher or lower in the full dataset; the rate of potential annotation inconsistencies cannot be reliably estimated from 31 examples.

2. **Train split only:** All sampled examples are from the `train` split. The `validation` and `test` splits (208 examples each) may have different proportions of positive labels or different content distributions; this cannot be assessed from the current sample.

3. **Long-context version not inspected:** Only the mixed-context (chunked, 1,386-sample) version is present in this dataset; the 350-sample long-context version (full articles) is not available here. The long-context version may exhibit fewer off-topic zero-label segments since each row is a complete article rather than a page fragment.

4. **Annotation guidelines not directly verifiable:** The apparent labeling inconsistencies identified (D17, D22, D27) cannot be definitively confirmed as errors without access to the full annotation guidelines and the complete article context for each chunk. Chunk-level re-annotation may have a documented rationale for some of these decisions that is not visible from the text alone.

5. **QA task not inspectable:** The ranking-based QA task (pseudo questions, candidate pools, retrieval scores) is not represented in this dataset; validity assessment of that task component is limited to documentation review.

6. **Non-text columns not reviewed:** The schema contains only text and integer label columns; no image or audio columns exist. Inspectability is complete for this modality.

