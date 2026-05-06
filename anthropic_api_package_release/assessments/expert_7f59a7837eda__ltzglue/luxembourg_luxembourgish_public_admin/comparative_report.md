## Deployment Context

**Use case:** In a public administration setting, a civil servant uses LLM-powered software to manage Luxembourgish citizen feedback by applying a model evaluated on topic classification, named entity recognition, intent detection, and sentiment analysis. The system automatically categorizes messages by domain and identifies key entities while classifying user intent and gauging sentiment to help detect frustrated users. These outputs enable the automated routing of requests to specific departments and the immediate prioritization of disgruntled or urgent correspondence, ensuring administrative actions are triggered accurately based on the content and tone of the message.
**Target population:** Civil servants in Luxembourgish government agencies who process digital correspondence and citizen inquiries written in the diverse orthographic styles of the Luxembourgish language.

# Validity Analysis: glue
**Target context:** Luxembourgish Public Administration Civil Servants — GLUE Assessment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ⚠ | 1 | Serious concern | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 2 | Significant gaps | high |
| **Average** | **1.2** | | |

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

GLUE is fundamentally invalid as an evaluation benchmark for a Luxembourgish public-administration citizen-correspondence routing system. Five of six dimensions score 1 (major validity violations), with OF scoring 2 only because the surface text-in/label-out modality matches. The mismatches are total along every HIGH-priority dimension: (IO) GLUE's nine English NLU tasks contain zero administrative-routing categories and no national-vs-communal or frontalier-vs-resident classifications [Q3, Q18, WEB-16, WEB-19]; (IC) all 409 sampled examples are English with US-political/cultural dominance, while the deployment input is trilingual lb/fr/de code-switched correspondence with non-standardized Luxembourgish orthography [WEB-11, WEB-12, DATASET-Concern 1]; (IF) GLUE assumes standardized English text input, while Luxembourgish input requires trilingual tokenization and ~21% residual orthographic noise even after best-available normalization [WEB-12]; (OO) hard single-label classification cannot represent multi-label routing with confidence scoring [Q12, DATASET-Concern 4]; (OC) annotator pools are undocumented English-speaking populations with no connection to Luxembourgish administrative register [Q26, Q36, Q73]; (OF) macro-average over nine irrelevant tasks [Q60] is uninformative as a deployment proxy. The strongest reusable value is methodological — GLUE's multi-task structure, diagnostic minimal-pair design [Q65, Q66], and human-baseline reporting [Q73, Q74] are transferable design patterns, not transferable evaluation signal.

## Practical Guidance

### What This Benchmark Measures

GLUE measures generalist English-language NLU competence across nine sentence-level tasks (sentiment, paraphrase, entailment, QA, acceptability, similarity) plus diagnostic linguistic-phenomenon coverage [Q3, Q15, Q18, Q135]. For the Luxembourg deployment, it provides no direct evidence of model capability — input language, content domain, output structure, and annotator perspective all diverge fundamentally. It can serve only as a structural template for designing a custom benchmark suite (multi-task scoring, diagnostic minimal pairs, human-baseline reporting), not as a deployment proxy.

### Construct Depth

GLUE probes English NLU constructs reasonably deeply via its diagnostic set's four broad categories and fine-grained subcategories [Q135, Q136], but the depth is irrelevant to the deployment's constructs (administrative routing, frontalier classification, urgency detection in formal Luxembourgish register). Even the dimensions where GLUE shows methodological strength (OO metric diversity, OC inter-annotator-agreement reporting) cannot compensate for the total absence of language and domain coverage. A model achieving state-of-the-art GLUE performance could plausibly score near-zero on the actual deployment task.

### What Else You Need

Comprehensive supplementation is required — GLUE cannot be remediated, only replaced or augmented. Required additions: (1) a Luxembourgish-language evaluation suite drawing on ltzGLUE [WEB-10] and LuxBorrow [WEB-11] as starting points; (2) a custom administrative-routing benchmark with État/commune competency labels, frontalier classification, and topic taxonomy elicited from CTIE/civil servants; (3) a formal-register sentiment/frustration dataset annotated by Luxembourgish civil servants to address the OC gap; (4) a code-switched lb/fr/de evaluation set covering the trilingual input distribution; (5) a multi-label-plus-confidence scoring framework matching the deployment's output requirements; (6) integration with the deployment's human-in-the-loop calibration mechanism for ongoing label-quality validation.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GLUE's task ontology consists of nine English sentence-understanding tasks — sentiment, paraphrase, entailment, QA, acceptability, similarity [Q3, Q18] — with no administrative-domain categories. The deployment requires routing categories that GLUE does not contain: cross-border worker (frontalier) classification, national vs. communal (État vs. commune) competency routing, housing urgency, social security, immigration, taxation, and public-transport queries (deployment_specific_categories in YAML). The diagnostic set's 'World Knowledge' [Q195] and 'Common Sense' [Q196] categories are general English-language reasoning probes with no jurisdictional specificity. IO is marked HIGH priority and the gap is total — the dataset analysis confirms zero administrative-domain content across 409 sampled examples.

**Strengths:**
- The multi-task structure with per-task scoring plus macro-average [Q15, Q59, Q60] offers a methodological template for designing a Luxembourgish administrative benchmark suite that combines NER, intent classification, sentiment, and routing tasks with separate metrics.
- The diagnostic set's minimal-pair construction methodology [Q65, Q66, Q68] tagged for fine-grained linguistic phenomena [Q135, Q136] is a transferable design pattern for probing model behaviour on negation, quantifier scope, and coreference in administrative text.

**Checklist:**

- **IO-1**: Required categories for the deployment include: cross-border worker / frontalier vs. resident classification, national (État) vs. communal competency routing across 100 communes [WEB-16, WEB-17, WEB-18], housing/cost-of-living urgency, social security, taxation (resident vs. non-resident), immigration, public transport (including the free-transit policy [WEB-20, WEB-21]), civil registration, EU-institutional employment, and local planning. None of these are present in GLUE. — _Sources: WEB-16, WEB-17, WEB-18, WEB-19, WEB-20, WEB-21_
- **IO-2**: GLUE's taxonomy omits every regionally-relevant administrative category. The closest approximation is MNLI's inclusion of 'government reports' as one of ten premise sources [Q38], but this is a stylistic source, not an ontological category, and no government-administrative example appears in the 409-example dataset sample. — _Sources: Q18, Q38, WEB-10_
- **IO-3**: GLUE includes categories irrelevant to the target context: English linguistic acceptability judgments from linguistics journals [Q21], movie-review sentiment [Q26], image-caption semantic similarity (STS-B) [Q35], Winograd pronoun coreference [Q50], and English textual entailment from news/Wikipedia [Q46, Q48]. The dataset analysis (DATASET-D6, DATASET-D8, DATASET-D40) confirms CoLA tests English-specific morphosyntactic phenomena with no transfer value to Luxembourgish/French/German administrative text. — _Sources: Q21, Q26, Q35, Q50, DATASET-D6, DATASET-D8, DATASET-D40_
- **IO-4**: Content-validity gaps are total: the deployment's required test-case categories (administrative routing, frontalier status, État/commune competency) have zero coverage. Construct-irrelevant variance is also high — performance on English movie-review sentiment, Winograd schemas, and image-caption similarity will not predict performance on Luxembourgish administrative routing. — _Sources: Q3, Q18, DATASET-D15, DATASET-D24, DATASET-D36_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'GLUE is a collection of NLU tasks including question answering, sentiment analysis, and textual entailment, and an associated online platform for model evaluation, comparison, and analysis.' (p.1)
- [Q18] 'GLUE is centered on nine English sentence understanding tasks, which cover a broad range of domains, data quantities, and difficulties.' (p.3)
- [Q38] 'The premise sentences are gathered from ten different sources, including transcribed speech, fiction, and government reports.' (p.4)
- [Q195] 'World Knowledge In this category we focus on knowledge that can clearly be expressed as facts, as well as broader and less common geographical, legal, political, technical, or cultural knowledge.' (p.20)

*Web sources:*
- [WEB-16] 100 communes as of 1 September 2023 — confirms the national-vs-communal routing requirement
- [WEB-19] Loi communale 1988 defines autonomous communal competencies — establishes the legal taxonomy GLUE does not cover
- [WEB-20] Free public transit since 29 February 2020 — domain-specific topic absent from GLUE
- [WEB-10] ltzGLUE (April 2025) provides Luxembourgish NER, topic, intent, sentiment, entailment — but its topic taxonomy (sports/animals/business/culture/technology) and voice-assistant intents do not cover administrative domains either

*Dataset analysis:*
- DATASET-D15: 'Who succeeded Newt Gingrich as Speaker?' — illustrates that QA tasks center on US political knowledge, not Luxembourg administrative competency routing
- DATASET-D36: MRPC paraphrase pair on health follow-up examinations — confirms no administrative-routing content in 409 sampled examples
- DATASET-D24: STS-B pair 'A person is boiling noodles.' / 'A woman is boiling noodles in water.' — image-caption similarity has no administrative correspondence relevance
- Concern 2 in dataset analysis: 'Across 409 examples, no example touches any administrative, government, or civic domain relevant to the deployment'

</details>

**Information gaps:**
- The deployment's full required topic taxonomy is itself not fully verified; the YAML notes that ranking categories by correspondence volume requires CTIE/ministerial access that was not available.

**Requires expert verification:**
- Final administrative topic taxonomy and priority ordering should be elicited from CTIE and ministry stakeholders before any custom benchmark construction.

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GLUE's input content is entirely English, drawn from American/British movie reviews [Q26], US/UK news [Q29, Q48], Wikipedia [Q41], Quora [Q31], linguistics journals [Q21], and English-language fiction and transcribed speech [Q38]. The dataset analysis confirms across 409 sampled examples that 'every single example reviewed across all 12 configs is in English' with US-political (Clinton, Bush, Gingrich, Ryan, Tillerson — DATASET-D10, D13, D14, D15, D22, D34), India-specific (DATASET-D16, D18), and US-pop-culture (DATASET-D3) cultural references dominating. The deployment input is trilingual Luxembourgish/French/German code-switched citizen correspondence with non-standardized Luxembourgish orthography [WEB-12, WEB-11], from a population that is 47.3% non-Luxembourgish nationals [WEB-4] with 47% of the workforce being cross-border workers from France, Belgium, and Germany [WEB-6, WEB-7]. The cultural and linguistic distance is total. IC is marked HIGH priority.

**Strengths:**
- MNLI's deliberate genre diversity — ten sources including government reports, transcribed speech, and fiction [Q38] — at least demonstrates a methodological awareness that NLU evaluation should span register variation, a principle transferable to a custom Luxembourgish suite even though GLUE itself does not realize it for the target language.
- The diagnostic set draws on naturally-occurring sentences from multiple domains [Q63], offering a genre-diversity template for a custom Luxembourgish administrative diagnostic.

**Checklist:**

- **IC-1**: Yes — the deployment requires region-specific knowledge including Luxembourgish lexicon and orthographic variation [WEB-12, WEB-15], French/German/Luxembourgish code-switching patterns [WEB-11], frontalier-vs-resident terminology, EU institutional vocabulary, communal-vs-État administrative terminology, and continental-European formal correspondence conventions. None of these are present in GLUE [Q21, Q26, Q29, Q31, Q35, Q41]. — _Sources: WEB-11, WEB-12, WEB-15, Q21, Q26_
- **IC-2**: Cultural alignment is absent. The dominant cultural content is American (US politics, US sports, US movies, US-centric Quora threads — DATASET-D10, D13, D14, D17, D20, D22, D34, D42) with some Indian content (DATASET-D16, D18). No Luxembourgish or even Luxembourg-adjacent (Belgian/French frontalier) administrative content appears in the 409-example sample. — _Sources: DATASET-D10, DATASET-D13, DATASET-D14, DATASET-D17, DATASET-D22_
- **IC-3**: Yes — Western-specific knowledge that does not transfer is pervasive: US presidential history (DATASET-D10, D14), US congressional politics (DATASET-D15, D22), American film criticism conventions (DATASET-D1, D2, D3, D4, D29, D30), antebellum American fiction dialect (DATASET-D11, D28), American telephone-speech register (DATASET-D33), and English-specific morphosyntactic violations (DATASET-D8, D40). — _Sources: DATASET-D8, DATASET-D11, DATASET-D15, DATASET-D33, DATASET-D40_
- **IC-4**: INSUFFICIENT DOCUMENTATION — GLUE does not document recruitment of regional annotators, and no Luxembourgish annotator pool exists in the inherited datasets. The YAML notes that no Luxembourgish administrative-correspondence corpus is publicly available and CTIE access would be required.
- **IC-5**: The content-validity violation is severe: the input distribution shares neither language, script-norm domain, register, nor cultural reference frame with the deployment. Construct-irrelevant variance from US/Indian cultural specificity will dominate any signal a model carries from GLUE. — _Sources: Q21, Q26, Q29, WEB-4, WEB-6, DATASET-Concern 1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q21] 'The Corpus of Linguistic Acceptability (Warstadt et al., 2018) consists of English acceptability judgments drawn from books and journal articles on linguistic theory.' (p.3)
- [Q26] 'The Stanford Sentiment Treebank (Socher et al., 2013) consists of sentences from movie reviews and human annotations of their sentiment.' (p.3)
- [Q29] 'The Microsoft Research Paraphrase Corpus (Dolan & Brockett, 2005) is a corpus of sentence pairs automatically extracted from online news sources...' (p.3)
- [Q38] 'The premise sentences are gathered from ten different sources, including transcribed speech, fiction, and government reports.' (p.4)
- [Q63] 'We ensure the data is reasonably diverse by producing examples for a variety of linguistic phenomena and basing our examples on naturally-occurring sentences from several domains (news, Reddit, Wikipedia, academic papers).' (p.5)

*Web sources:*
- [WEB-4] 47.3% foreign nationals as of 1 January 2024; over 170 nationalities — confirms input population's linguistic diversity
- [WEB-6] ~47% of workforce are cross-border workers (~231,290 frontaliers in 2024) — confirms French/German linguistic input share
- [WEB-11] LuxBorrow corpus documents systematic LU/DE/FR/EN code-switching in Luxembourgish text — empirical evidence of trilingual input characteristic
- [WEB-12] Best neural normalizer for Luxembourgish achieves only ~78.8% accuracy — empirical evidence of orthographic non-standardization absent from GLUE

*Dataset analysis:*
- DATASET-Concern 1: 'Every single example reviewed across all 12 configs is in English. The 409 sampled examples contain no Luxembourgish tokens, no French text, and no German text.'
- DATASET-D10: 'I did not mention Monica in my lecture, but the first question I was asked was how President Clinton could do his job...' — US political scandal dependency
- DATASET-D11: 'Yes, Mistuh Reese, suh?' — antebellum American fiction dialect
- DATASET-D33: 'oh yeah no that's uh that's a that's a real interesting movie...' — American telephone speech, register opposite to formal Luxembourgish administrative correspondence
- DATASET-D16: 'What is the effect of black money on India's macro economy?' — confirms even non-US content is non-Luxembourgish

</details>

**Information gaps:**
- No annotator demographic information is published for the inherited GLUE component datasets, so the regional-annotator question cannot be addressed from documentation.

**Requires expert verification:**
- Sub-national linguistic variation within Luxembourg (Minett, Ardennes, Moselle, Stad Lëtzebuerg) requires sociolinguistic expert elicitation beyond available web sources.

---

### Input Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GLUE inputs are standardized written English text in a single script with consistent orthography, formatted as single sentences or sentence pairs [Q4, Q15]. The deployment input is text in three languages with frequent code-switching at lexical, phrasal, and sentence level [WEB-11], non-standardized Luxembourgish spelling where 'large amount of orthographic variation' and homograph density are documented challenges [WEB-12, WEB-15], and a register requiring trilingual tokenization and normalization that English NLP pipelines do not provide [WEB-2, WEB-13, WEB-14]. GLUE's preprocessing transformations (recasting SQuAD into NLI [Q42], converting Winograd [Q52]) are English-specific and provide no transferable methodology for non-standardized multilingual signals. IF is HIGH priority and the gap is fundamental.

**Strengths:**
- GLUE imposes minimal architectural constraints, requiring only sentence/sentence-pair input [Q4]; this format-agnostic design means a custom Luxembourgish benchmark could in principle adopt the same I/O contract while substituting language-appropriate content.

**Checklist:**

- **IF-1**: Signal distributions are fundamentally mismatched. GLUE inputs are standardized English text [Q4, Q18]; deployment inputs are trilingual lb/fr/de code-switched text with non-standardized Luxembourgish orthography. The LuxBorrow corpus [WEB-11] documents systematic token-level language switching, and the best Luxembourgish neural normalizer achieves only ~78.8% accuracy [WEB-12], indicating ~21% residual orthographic noise that GLUE-trained models would never have encountered. — _Sources: Q4, Q18, WEB-11, WEB-12, DATASET-Concern 1_
- **IF-2**: Luxembourg's digital infrastructure for capturing citizen correspondence (MyGuichet.lu via CTIE [WEB-2]) supports text input and is technically capable of feeding any text-based pipeline; the infrastructural gap is not capture but processing — Luxembourgish NLP tooling (LuxemBERT [WEB-13], LuNa [WEB-14], spellux [WEB-15], ltz-E1 [WEB-10]) is emerging but limited compared to the standardized English NLP stack GLUE assumes. — _Sources: WEB-2, WEB-10, WEB-13, WEB-14, WEB-15_
- **IF-3**: Domain-specific form differences include: (a) trilingual tokenization requirements that English tokenizers do not satisfy; (b) orthographic normalization needs specific to Luxembourgish [WEB-12, WEB-15]; (c) handling of contact-linguistic phenomena [WEB-11]. GLUE's transformations [Q42, Q49, Q52] address none of these. — _Sources: Q42, Q49, Q52, WEB-11, WEB-12_
- **IF-4**: External-validity violation is severe: a model evaluated only on standardized English text input has zero exposure to the non-standard, code-switched, multilingual input form characteristic of Luxembourgish citizen correspondence. The 409-example dataset sample contains no non-English tokens, confirming the form mismatch empirically (DATASET-Concern 1). — _Sources: Q4, DATASET-Concern 1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q4] 'GLUE does not place any constraints on model architecture beyond the ability to process single-sentence and sentence-pair inputs and to make corresponding predictions.' (p.1)
- [Q42] 'We convert the task into sentence pair classification by forming a pair between each question and each sentence in the corresponding context, and filtering out pairs with low lexical overlap...' (p.4)
- [Q49] 'We convert all datasets to a two-class split, where for three-class datasets we collapse neutral and contradiction into not entailment, for consistency.' (p.4)
- [Q52] 'To convert the problem into sentence pair classification, we construct sentence pairs by replacing the ambiguous pronoun with each possible referent.' (p.4)

*Web sources:*
- [WEB-11] LuxBorrow corpus with token-level LID and code-switching annotation across LU/DE/FR/EN — confirms code-switching as systematic input characteristic
- [WEB-12] Neural Text Normalization for Luxembourgish — best ByT5 base achieves ~78.8% accuracy; documents 'large amount of orthographic variation'
- [WEB-15] spellux Python package documents homograph density and orthographic variation as ongoing Luxembourgish NLP challenges
- [WEB-13] LuxemBERT (2022) outperformed mBERT — confirms standardized English models are inadequate baselines for Luxembourgish
- [WEB-2] CTIE operates MyGuichet.lu under Ministry for Digitalisation

*Dataset analysis:*
- DATASET-Concern 1: zero non-English tokens across 409 examples — confirms IF gap empirically
- DATASET-D33: transcribed American spoken English in MNLI — illustrates that GLUE's only register variation is within-English, not cross-lingual

</details>

**Information gaps:**
- Exact distribution of language proportions and code-switching density in actual MyGuichet.lu citizen correspondence is not publicly documented and would require CTIE access.

**Requires expert verification:**
- Whether a normalization preprocessing step (e.g., spellux or ByT5 normalizer) is sufficient to recover GLUE-trained model performance on Luxembourgish input, or whether retraining is required, needs empirical validation.

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GLUE's output ontology is hard single-label classification (binary or three-class) plus one regression task [Q12], scored via accuracy/MCC/F1/Pearson [Q20, Q23, Q30, Q33, Q35] aggregated as a macro-average [Q59, Q60]. The deployment requires multi-label classification (a single citizen message may concern multiple departments simultaneously) plus confidence scoring to flag uncertain cases for human review (elicitation A4). The dataset analysis confirms 'every classification task in the sampled data uses exactly one label per example' and 'no example has multiple labels, soft labels, or confidence scores.' Additionally, the output categories themselves (grammatical/ungrammatical, positive/negative, entailment/neutral/contradiction) have no correspondence to administrative routing categories: no État-vs-commune label, no frontalier-vs-resident label, no department-routing label, no urgency flag. OO is HIGH priority.

**Strengths:**
- GLUE explicitly diversifies metrics across tasks — using MCC for unbalanced binary classification [Q23] and Pearson/Spearman for regression [Q35] — modeling awareness that a single accuracy metric cannot capture all evaluation needs. This metric-diversity principle is transferable to a multi-label, confidence-scored Luxembourgish benchmark.

**Checklist:**

- **OO-1**: Output categories are not regionally relevant. CoLA's grammatical/ungrammatical [Q22], SST-2's positive/negative [Q28], MNLI's entailment/neutral/contradiction [Q56], and RTE's entailment/not-entailment [Q49] do not map to any required deployment output: department routing, urgency flag, frustration flag, frontalier classification, État/commune competency. — _Sources: Q12, Q22, Q28, Q56_
- **OO-2**: Missing categories specific to the regional context include: department-level routing labels across both État ministries and 100 communes [WEB-16, WEB-17], frontalier-vs-resident classification [WEB-6, WEB-8], urgency level (housing political-sensitivity flag, social-security urgency), and intent classes for administrative correspondence (request, complaint, status inquiry, document submission). None exist in GLUE. — _Sources: WEB-6, WEB-16, WEB-17_
- **OO-3**: GLUE's sentiment ontology (positive/negative [Q28]) encodes English movie-review evaluative norms; the deployment requires a frustration/urgency ontology calibrated to understated continental-European formal administrative register, where direct expressions of frustration are rare (cultural_norms_notes). The two label spaces are not compatible. — _Sources: Q28, DATASET-D29, DATASET-D30_
- **OO-4**: Stakeholder-driven taxonomy redesign is not optional but required — GLUE's label spaces cannot be repurposed; a Luxembourg-specific output ontology must be constructed from scratch with civil-servant input. ltzGLUE [WEB-10] provides a closer Luxembourgish-language template (NER, intent, sentiment) but its taxonomies are still non-administrative. — _Sources: WEB-10, Q12_
- **OO-5**: Structural-validity violation is fundamental: the structure of GLUE's output space (single hard labels, no multi-label, no confidence) misrepresents the routing decision structure the deployment requires. Content-validity violation is total: required categories are absent. — _Sources: Q12, DATASET-Concern 4_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'All tasks are single sentence or sentence pair classification, except STS-B, which is a regression task. MNLI has three classes; all other classification tasks have two.' (p.2)
- [Q22] 'Each example is a sequence of words annotated with whether it is a grammatical English sentence.' (p.3)
- [Q28] 'We use the two-way (positive/negative) class split, and use only sentence-level labels.' (p.3)
- [Q56] 'Labels are entailment (E), neutral (N), or contradiction (C).' (p.5)
- [Q148] 'We place all examples involving these phenomena under the label of Factivity.' (p.16)

*Web sources:*
- [WEB-16] 100 communes as of 1 September 2023 — establishes communal-routing label space requirement absent from GLUE
- [WEB-6] ~47% of workforce are frontaliers — establishes the frontalier-vs-resident label requirement
- [WEB-10] ltzGLUE provides Luxembourgish slot-intent and topic labels but for voice-assistant/news domains, not administrative routing

*Dataset analysis:*
- DATASET-Concern 4: 'every classification task in the sampled data uses exactly one label per example... No example has multiple labels, soft labels, or confidence scores.' Schema metadata confirms ClassLabel(2/3 classes) with no probability field.
- DATASET-D21: ax test example with label=-1 confirms hard single-label encoding even for the diagnostic set

</details>

**Information gaps:**
- The exact required output schema (number of routing labels, urgency-flag thresholds, multi-label co-occurrence patterns) is not specified in the elicitation beyond the multi-label-plus-confidence requirement.

**Requires expert verification:**
- Civil-servant stakeholders should define the final routing taxonomy and confidence-threshold rules, including which uncertain cases are escalated to human review.

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Annotator demographics for the main inherited GLUE tasks are not documented in the paper [Q6 establishes the inherited-dataset reliance; no demographic disclosure for SST-2 [Q26] or MNLI crowdworkers [Q36]]. The diagnostic set's annotators are explicitly six NLP researchers [Q73] with high inter-annotator agreement (Fleiss's κ = 0.73 [Q74], R3 = 0.80 [Q75]) — but this is a specialized English-speaking population with no documented connection to Luxembourgish administrative culture or continental-European formal correspondence register. Ground-truth sentiment in SST-2 reflects English movie-review judgments (DATASET-D1 through D5, D29, D30); ground-truth entailment in MNLI/RTE reflects English crowdsourced judgments. The dataset analysis shows SST-2 fragments often labelled in ways that depend entirely on film-criticism context (DATASET-D2, D29, D30). Luxembourg's understated formal administrative register, where frustration is expressed indirectly (cultural_norms_notes), is not represented in any annotator pool. The user explicitly flagged OC as a 'live risk' (elicitation A3). Even ltzGLUE [WEB-10] and the only Luxembourgish sentiment corpus [WEB-25] do not cover administrative register — the latter sources from RTL.lu informal news comments.

**Strengths:**
- GLUE reports inter-annotator agreement (Fleiss's κ = 0.73 [Q74]) and a human baseline (R3 = 0.80 [Q75]) for the diagnostic set, establishing a methodological precedent for human-baseline reporting that any custom Luxembourgish benchmark should follow.
- The diagnostic set was tested for hypothesis-only artifacts using fastText classifiers (near-chance 32.7% / 36.4% [Q72]), demonstrating attention to label-quality verification — a transferable practice.

**Checklist:**

- **OC-1**: No — ground-truth labels reflect English-speaking annotator pools (movie reviewers, crowdworkers, NLP researchers [Q26, Q36, Q73]) with no documented Luxembourgish or continental-European administrative-culture representation. — _Sources: Q26, Q36, Q73_
- **OC-2**: Significant disagreement is expected. Luxembourg administrative correspondence uses understated formal register (cultural_norms_notes); frustration is rarely expressed directly. English movie-review sentiment annotators (DATASET-D1, D3, D29, D30) are calibrated to overt evaluative language. A label of 'positive sentiment' on a fragment like 'at its best moments' (DATASET-D2) has no analogue in formal Luxembourgish administrative messages. — _Sources: DATASET-D1, DATASET-D3, DATASET-D29, DATASET-D30_
- **OC-3**: Annotator demographics are NOT documented for the main benchmark tasks. The paper does not describe SST-2 sentiment annotators [Q26] or MNLI crowdworker demographics [Q36], nor inter-annotator agreement for inherited datasets [Q6]. Only the diagnostic set's annotators are described — six NLP researchers [Q73]. — _Sources: Q6, Q26, Q36, Q73_
- **OC-4**: Re-annotation by Luxembourgish civil servants would be required. The deployment's human-in-the-loop mechanism (elicitation A3) is positioned to produce such corrections post-hoc, but baseline labels in any GLUE-style training/evaluation would still encode the original misalignment. — _Sources: WEB-25, WEB-10_
- **OC-5**: GLUE's aggregation methods are not documented at the per-example level for inherited datasets. The diagnostic set uses majority labelling with high κ [Q74] but only six annotators from a homogeneous population — minority perspectives could be erased without detection. Multi-label phenomena tagging [Q141] is permitted but does not extend to label disagreement modeling. — _Sources: Q73, Q74, Q141_
- **OC-6**: Convergent-validity violation is severe: labels do not correlate with judgments of regional stakeholders in administrative culture. External-validity violation is also severe: judgments of English film reviewers and US crowdworkers will not generalize to Luxembourg civil servants assessing citizen correspondence. — _Sources: DATASET-Concern 3, WEB-25_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q6] 'None of the datasets in GLUE were created from scratch for the benchmark; we rely on preexisting datasets...' (p.1)
- [Q26] 'The Stanford Sentiment Treebank (Socher et al., 2013) consists of sentences from movie reviews and human annotations of their sentiment.' (p.3)
- [Q36] 'The Multi-Genre Natural Language Inference Corpus (Williams et al., 2018) is a crowdsourced collection of sentence pairs with textual entailment annotations.' (p.4)
- [Q73] 'To establish human baseline performance on the diagnostic set, we have six NLP researchers annotate 50 sentence pairs (100 entailment examples) randomly sampled from the diagnostic set.' (p.6)
- [Q74] 'Inter-annotator agreement is high, with a Fleiss's κ of 0.73.' (p.6)

*Web sources:*
- [WEB-25] RTL Corpus Sentiment Annotation Tool (STRIPS) — only known Luxembourgish sentiment resource, sourced from informal RTL news comments rather than administrative register
- [WEB-10] ltzGLUE provides Luxembourgish sentiment (positive/neutral/negative) but not in administrative register

*Dataset analysis:*
- DATASET-D2: 'at its best moments' labelled positive — illustrates that SST-2 labels depend on film-critic register absent from administrative correspondence
- DATASET-D4: 'no lika da' labelled negative — sentiment label nearly uninterpretable without film context
- DATASET-D29: 'the horrors' labelled negative — context-dependent label inappropriate for administrative register
- DATASET-D30: 'heroes' labelled positive — single-word fragment with film-review context dependency
- DATASET-Concern 3 explicit conclusion: 'Labels trained on explicit, colloquial English film criticism sentiment will systematically fail to detect the understated frustration signals in Luxembourgish administrative correspondence.'

</details>

**Information gaps:**
- Demographic composition of MNLI crowdworkers and SST-2 sentiment annotators is not disclosed in the paper.
- Inter-annotator agreement metrics for inherited GLUE component datasets are not reported in the GLUE paper [Q6 implies inheritance without re-reporting].

**Requires expert verification:**
- A pilot re-annotation of administrative-correspondence sentiment by Luxembourgish civil servants would establish empirical disagreement rates and quantify the OC gap.

---

### Output Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
GLUE evaluates text-based outputs only via hard single-label scoring on private test sets [Q57, Q58], with per-task scores aggregated as a macro-average [Q59, Q60] subject to two-submissions-per-day rate limiting [Q131]. The deployment is also text-in/label-out, so the surface-level format aligns — both are written-text pipelines, and OF is correctly marked MODERATE priority (lower than HIGH for the other dimensions). However, GLUE's output form lacks the multi-label structure and confidence scoring the deployment requires (elicitation A4), and the submission-based privately-held test data model [Q7, Q58] prevents the iterative, task-specific calibration a live civil-service deployment requires. The macro-average [Q60] also rewards balanced performance across nine irrelevant English NLU tasks, making the aggregate GLUE score uninformative as a deployment proxy. Score is 2 (not 1) because the underlying text-based output modality matches and the per-task evaluation infrastructure is methodologically reusable, but the specific output-form requirements (multi-label, confidence) are unsatisfied.

**Strengths:**
- Output modality matches: GLUE produces text-based predictions [Q57, Q58], aligned with the deployment's text-in/text-or-label-out pipeline.
- Per-task scoring with task-appropriate metrics (accuracy, F1, MCC, Pearson [Q20, Q23, Q30, Q35]) is methodologically transferable to a custom benchmark suite, even though the specific tasks are not.
- Submission rate-limiting [Q131] models a defensive-evaluation practice (preventing test-set overfitting) potentially adaptable to civil-service contexts.

**Checklist:**

- **OF-1**: Partial match. Output modality (text labels) matches the deployment's text-classification pipeline. However, the specific output form — single hard labels, no multi-label, no confidence scores — does not match the deployment's multi-label-plus-confidence requirement (elicitation A4, DATASET-Concern 4). — _Sources: Q12, Q57, Q58, DATASET-Concern 4_
- **OF-2**: Not applicable — neither GLUE nor the deployment require speech-based output. The deployment is text-classification-only per the elicitation.
- **OF-3**: Not directly relevant to OF for this deployment (the deployment's end-users are civil servants, not citizens; outputs are routing decisions and flags consumed by an internal review interface). Literacy/accessibility considerations would apply to citizen-facing response generation, which is outside the elicited scope.
- **OF-4**: Form mismatches that harm external validity: (a) GLUE's macro-average over nine English tasks [Q59, Q60] is not informative as a deployment proxy; (b) hard single-label scoring [Q12] cannot evaluate multi-label routing; (c) the privately-held test-set submission model [Q7, Q58] prevents task-specific calibration; (d) two-submissions-per-day limit [Q131] is misaligned with iterative civil-service development cycles. — _Sources: Q7, Q12, Q59, Q60, Q131_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q7] 'Four of the datasets feature privately-held test data, which will be used to ensure that the benchmark is used fairly.' (p.1)
- [Q12] 'All tasks are single sentence or sentence pair classification, except STS-B, which is a regression task. MNLI has three classes; all other classification tasks have two.' (p.2)
- [Q57] 'The GLUE benchmark follows the same evaluation model as SemEval and Kaggle.' (p.5)
- [Q58] 'To evaluate a system on the benchmark, one must run the system on the provided test data for the tasks, then upload the results to the website gluebenchmark.com for scoring.' (p.5)
- [Q59] 'The benchmark site shows per-task scores and a macro-average of those scores to determine a system's position on the leaderboard.' (p.5)
- [Q60] 'For tasks with multiple metrics (e.g., accuracy and F1), we use an unweighted average of the metrics as the score for the task when computing the overall macro-average.' (p.5)
- [Q131] 'The GLUE website limits users to two submissions per day in order to avoid overfitting to the private test data.' (p.14)

*Web sources:*
- [WEB-22] EU AI Act Annex III — automated administrative routing systems classified high-risk; requires output-form transparency including confidence-scored decisions

*Dataset analysis:*
- DATASET-Concern 4: schema metadata confirms ClassLabel(2/3 classes) with no probability field — empirical confirmation that GLUE's output form lacks confidence scoring

</details>

**Information gaps:**
- Whether the deployment requires structured output beyond labels + confidence (e.g., extracted entities for NER, span annotations) is mentioned in the deployment description but not detailed in OF terms.

**Requires expert verification:**
- Specific output-schema requirements for the routing API (label space, confidence-threshold rules, NER span format) should be confirmed with deployment engineers.

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** GLUE's task ontology contains no administrative-routing categories, no national-vs-communal competency distinction, and no cross-border-worker classification.

**Recommendation:** Construct a Luxembourg-specific topic and intent taxonomy via stakeholder elicitation with CTIE and ministry staff, covering: État/commune routing across 100 communes, frontalier-vs-resident status, housing urgency, social security, taxation, immigration, public transport, civil registration, and EU-institutional matters. Use ltzGLUE's slot-intent design [WEB-10] as a structural template but rebuild the label space for administrative content.

### Input Content ⚠

**Gap:** GLUE input content is entirely English (US/UK news, movie reviews, Wikipedia, Quora) with no Luxembourgish, French, or German text and no administrative-domain content.

**Recommendation:** Build a Luxembourgish administrative-correspondence corpus from MyGuichet.lu data (with appropriate CTIE access and CNPD/GDPR review), supplementing with LuxBorrow [WEB-11] for code-switching patterns and adapting ltzGLUE's content domains. Ensure the corpus reflects the input population's linguistic diversity (47.3% non-Luxembourgish nationals, ~47% frontalier workforce).

### Input Form ⚠

**Gap:** GLUE assumes standardized English text; deployment requires trilingual lb/fr/de tokenization and Luxembourgish orthographic normalization.

**Recommendation:** Integrate a preprocessing pipeline using spellux [WEB-15] or ByT5-based normalization [WEB-12] for Luxembourgish input, combined with multilingual tokenization (e.g., LuxemBERT [WEB-13] or LuNa [WEB-14] tooling). Empirically validate residual error rates and propagation to downstream tasks before deployment.

### Output Ontology ⚠

**Gap:** GLUE's hard single-label output cannot represent the deployment's required multi-label routing with confidence scoring.

**Recommendation:** Design the evaluation output schema as multi-label classification with per-label confidence scores, plus separate threshold-tuning rules for human-in-the-loop escalation. Adapt GLUE's per-task metric diversity principle [Q23, Q35] by reporting micro/macro F1, label-wise precision/recall, and calibration metrics (e.g., expected calibration error) on the confidence outputs.

### Output Content ⚠

**Gap:** Ground-truth labels in GLUE reflect English-speaking annotator pools with no connection to Luxembourgish administrative register; SST-2 sentiment is calibrated to film criticism, not understated formal correspondence.

**Recommendation:** Recruit Luxembourgish civil servants familiar with administrative correspondence for a custom annotation task, using clear annotation guidelines for understated frustration/urgency signals. Report inter-annotator agreement following GLUE's diagnostic-set methodology [Q73, Q74] but with a representative annotator pool. Use the deployment's human-in-the-loop corrections (elicitation A3) as an ongoing label-validation feedback channel.

### Output Form

**Gap:** GLUE's macro-average over nine English tasks [Q60] is uninformative as a deployment proxy, and the privately-held submission model [Q7, Q58] prevents iterative calibration.

**Recommendation:** Avoid using the GLUE macro-average as any kind of deployment indicator. Build an internal evaluation infrastructure mirroring GLUE's per-task scoring [Q59] but with task-specific thresholds aligned to civil-service operational needs, fewer submission-rate constraints, and integration with EU AI Act high-risk-system documentation requirements [WEB-22].

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | output_content | "Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy & Samuel R. Bowman" |
| Q2 | 1 | output_content | "Courant Institute of Mathematical Sciences, New York University; Paul G. Allen School of Computer Science & Engineering, University of Washington; DeepMind" |
| Q3 | 1 | input_ontology | "GLUE is a collection of NLU tasks including question answering, sentiment analysis, and textual entailment, and an associated online platform for model evaluation, comparison, and analysis." |
| Q4 | 1 | input_form | "GLUE does not place any constraints on model architecture beyond the ability to process single-sentence and sentence-pair inputs and to make corresponding predictions." |
| Q5 | 1 | input_content | "For some GLUE tasks, training data is plentiful, but for others it is limited or fails to match the genre of the test set." |
| Q6 | 1 | input_content | "None of the datasets in GLUE were created from scratch for the benchmark; we rely on preexisting datasets because they have been implicitly agreed upon by the NLP community as challenging and interesting." |
| Q7 | 1 | output_form | "Four of the datasets feature privately-held test data, which will be used to ensure that the benchmark is used fairly." |
| Q8 | 1 | input_ontology | "GLUE also includes a set of hand-crafted analysis examples for probing trained models." |
| Q9 | 1 | input_ontology | "This dataset is designed to highlight common challenges, such as the use of world knowledge and logical operators, that we expect models must handle to robustly solve the tasks." |
| Q10 | 1 | output_form | "We evaluate baselines based on current methods for transfer and representation learning and find that multi-task training on all tasks performs better than training a separate model per task." |
| Q11 | 1 | output_form | "However, the low absolute performance of our best model indicates the need for improved general NLU systems." |
| Q12 | 2 | output_ontology | "All tasks are single sentence or sentence pair classification, except STS-B, which is a regression task. MNLI has three classes; all other classification tasks have two. Test sets shown in bold use labels that have never been made public in any form." |
| Q13 | 2 | output_form | "To better understand the challenged posed by GLUE, we conduct experiments with simple baselines and state-of-the-art sentence representation models. We find that unified multi-task trained models slightly outperform comparable models trained on each task separately. Our best multi-task model makes use of ELMo (Peters et al., 2018), a recently proposed pre-training technique. However, this model still achieves a fairly low absolute score." |
| Q14 | 2 | output_ontology | "Analysis with our diagnostic dataset reveals that our baseline models deal well with strong lexical signals but struggle with deeper logical structure." |
| Q15 | 2 | input_ontology | "In summary, we offer: (i) A suite of nine sentence or sentence-pair NLU tasks, built on established annotated datasets and selected to cover a diverse range of text genres, dataset sizes, and degrees of difficulty. (ii) An online evaluation platform and leaderboard, based primarily on privately-held test data. The platform is model-agnostic, and can evaluate any method capable of producing results on all nine tasks. (iii) An expert-constructed diagnostic evaluation dataset. (iv) Baseline results for several major existing approaches to sentence representation learning." |
| Q16 | 2 | input_ontology | "Like GLUE, SentEval relies on a set of existing classification tasks involving either one or two sentences as inputs. Unlike GLUE, SentEval only evaluates sentence-to-vector encoders, making it well-suited for evaluating models on tasks involving sentences in isolation." |
| Q17 | 2 | input_ontology | "GLUE is designed to facilitate the development of these methods: It is model-agnostic, allowing for any kind of representation or contextualization, including models that use no explicit vector or symbolic representations for sentences whatsoever." |
| Q18 | 3 | input_ontology | "GLUE is centered on nine English sentence understanding tasks, which cover a broad range of domains, data quantities, and difficulties." |
| Q19 | 3 | input_ontology | "As the goal of GLUE is to spur development of generalizable NLU systems, we design the benchmark such that good performance should require a model to share substantial knowledge (e.g., trained parameters) across all tasks, while still maintaining some task-specific components." |
| Q20 | 3 | output_form | "Unless otherwise mentioned, tasks are evaluated on accuracy and are balanced across classes." |
| Q21 | 3 | input_content | "The Corpus of Linguistic Acceptability (Warstadt et al., 2018) consists of English acceptability judgments drawn from books and journal articles on linguistic theory." |
| Q22 | 3 | output_ontology | "Each example is a sequence of words annotated with whether it is a grammatical English sentence." |
| Q23 | 3 | output_form | "Following the authors, we use Matthews correlation coefficient (Matthews, 1975) as the evaluation metric, which evaluates performance on unbalanced binary classification and ranges from -1 to 1, with 0 being the performance of uninformed guessing." |
| Q24 | 3 | input_content | "We use the standard test set, for which we obtained private labels from the authors." |
| Q25 | 3 | output_form | "We report a single performance number on the combination of the in- and out-of-domain sections of the test set." |
| Q26 | 3 | input_content | "The Stanford Sentiment Treebank (Socher et al., 2013) consists of sentences from movie reviews and human annotations of their sentiment." |
| Q27 | 3 | input_ontology | "The task is to predict the sentiment of a given sentence." |
| Q28 | 3 | output_ontology | "We use the two-way (positive/negative) class split, and use only sentence-level labels." |
| Q29 | 3 | input_content | "The Microsoft Research Paraphrase Corpus (Dolan & Brockett, 2005) is a corpus of sentence pairs automatically extracted from online news sources, with human annotations for whether the sentences in the pair are semantically equivalent." |
| Q30 | 3 | output_form | "Because the classes are imbalanced (68% positive), we follow common practice and report both accuracy and F1 score." |
| Q31 | 3 | input_content | "The Quora Question Pairs dataset is a collection of question pairs from the community question-answering website Quora." |
| Q32 | 3 | input_ontology | "The task is to determine whether a pair of questions are semantically equivalent." |
| Q33 | 3 | output_form | "As in MRPC, the class distribution in QQP is unbalanced (63% negative), so we report both accuracy and F1 score." |
| Q34 | 3 | output_content | "We observe that the test set has a different label distribution than the training set." |
| Q35 | 3 | input_content | "The Semantic Textual Similarity Benchmark (Cer et al., 2017) is a collection of sentence pairs drawn from news headlines, video and image captions, and natural language inference data. Each pair is human-annotated with a similarity score from 1 to 5; the task is to predict these scores. Follow common practice, we evaluate using Pearson and Spearman correlation coefficients." |
| Q36 | 4 | input_content | "The Multi-Genre Natural Language Inference Corpus (Williams et al., 2018) is a crowdsourced collection of sentence pairs with textual entailment annotations." |
| Q37 | 4 | input_ontology | "Given a premise sentence and a hypothesis sentence, the task is to predict whether the premise entails the hypothesis (entailment), contradicts the hypothesis (contradiction), or neither (neutral)." |
| Q38 | 4 | input_content | "The premise sentences are gathered from ten different sources, including transcribed speech, fiction, and government reports." |
| Q39 | 4 | output_form | "We use the standard test set, for which we obtained private labels from the authors, and evaluate on both the matched (in-domain) and mismatched (cross-domain) sections." |
| Q40 | 4 | input_content | "We also use and recommend the SNLI corpus (Bowman et al., 2015) as 550k examples of auxiliary training data." |
| Q41 | 4 | input_content | "The Stanford Question Answering Dataset (Rajpurkar et al. 2016) is a question-answering dataset consisting of question-paragraph pairs, where one of the sentences in the paragraph (drawn from Wikipedia) contains the answer to the corresponding question (written by an annotator)." |
| Q42 | 4 | input_form | "We convert the task into sentence pair classification by forming a pair between each question and each sentence in the corresponding context, and filtering out pairs with low lexical overlap between the question and the context sentence." |
| Q43 | 4 | input_ontology | "The task is to determine whether the context sentence contains the answer to the question." |
| Q44 | 4 | output_ontology | "This modified version of the original task removes the requirement that the model select the exact answer, but also removes the simplifying assumptions that the answer is always present in the input and that lexical overlap is a reliable cue." |
| Q45 | 4 | input_form | "This process of recasting existing datasets into NLI is similar to methods introduced in White et al. (2017) and expanded upon in Demszky et al. (2018)." |
| Q46 | 4 | input_content | "The Recognizing Textual Entailment (RTE) datasets come from a series of annual textual entailment challenges." |
| Q47 | 4 | input_content | "We combine the data from RTE1 (Dagan et al., 2006), RTE2 (Bar Haim et al., 2006), RTE3 (Giampiccolo et al., 2007), and RTE5 (Bentivogli et al., 2009)." |
| Q48 | 4 | input_content | "Examples are constructed based on news and Wikipedia text." |
| Q49 | 4 | input_form | "We convert all datasets to a two-class split, where for three-class datasets we collapse neutral and contradiction into not entailment, for consistency." |
| Q50 | 4 | input_content | "The Winograd Schema Challenge (Levesque et al., 2011) is a reading comprehension task in which a system must read a sentence with a pronoun and select the referent of that pronoun from a list of choices." |
| Q51 | 4 | input_content | "The examples are manually constructed to foil simple statistical methods: Each one is contingent on contextual information provided by a single word or phrase in the sentence." |
| Q52 | 4 | input_form | "To convert the problem into sentence pair classification, we construct sentence pairs by replacing the ambiguous pronoun with each possible referent." |
| Q53 | 5 | input_content | "We use a small evaluation set consisting of new examples derived from fiction books that was shared privately by the authors of the original corpus." |
| Q54 | 5 | input_form | "While the included training set is balanced between two classes, the test set is imbalanced between them (65% not entailment)." |
| Q55 | 5 | output_content | "Also, due to a data quirk, the development set is adversarial: hypotheses are sometimes shared between training and development examples, so if a model memorizes the training examples, they will predict the wrong label on corresponding development set example." |
| Q56 | 5 | output_ontology | "Labels are entailment (E), neutral (N), or contradiction (C)." |
| Q57 | 5 | output_form | "The GLUE benchmark follows the same evaluation model as SemEval and Kaggle." |
| Q58 | 5 | output_form | "To evaluate a system on the benchmark, one must run the system on the provided test data for the tasks, then upload the results to the website gluebenchmark.com for scoring." |
| Q59 | 5 | output_form | "The benchmark site shows per-task scores and a macro-average of those scores to determine a system's position on the leaderboard." |
| Q60 | 5 | output_form | "For tasks with multiple metrics (e.g., accuracy and F1), we use an unweighted average of the metrics as the score for the task when computing the overall macro-average." |
| Q61 | 5 | input_content | "Drawing inspiration from the FraCaS suite (Cooper et al., 1996) and the recent Build-It-Break-It competition (Ettinger et al., 2017), we include a small, manually-curated test set for the analysis of system performance." |
| Q62 | 5 | input_form | "Each diagnostic example is an NLI sentence pair with tags for the phenomena demonstrated." |
| Q63 | 5 | input_content | "We ensure the data is reasonably diverse by producing examples for a variety of linguistic phenomena and basing our examples on naturally-occurring sentences from several domains (news, Reddit, Wikipedia, academic papers)." |
| Q64 | 6 | input_ontology | "We begin with a target set of phenomena, based roughly on those used in the FraCaS suite (Cooper et al., 1996)." |
| Q65 | 6 | output_content | "We construct each example by locating a sentence that can be easily made to demonstrate a target phenomenon, and editing it in two ways to produce an appropriate sentence pair." |
| Q66 | 6 | output_content | "We make minimal modifications so as to maintain high lexical and structural overlap within each sentence pair and limit superficial cues." |
| Q67 | 6 | output_content | "We then label the inference relationships between the sentences, considering each sentence alternatively as the premise, producing two labeled examples for each pair (1100 total)." |
| Q68 | 6 | output_content | "Where possible, we produce several pairs with different labels for a single source sentence, to have minimal sets of sentence pairs that are lexically and structurally very similar but correspond to different entailment relationships." |
| Q69 | 6 | output_ontology | "The resulting labels are 42% entailment, 35% neutral, and 23% contradiction." |
| Q70 | 6 | output_form | "Since the class distribution in the diagnostic set is not balanced, we use R3 (Gorodkin, 2004), a three-class generalization of the Matthews correlation coefficient, for evaluation." |
| Q71 | 6 | output_form | "We reproduce the methodology of Gururangan et al. (2018), training two fastText classifiers (Joulin et al., 2016) to predict entailment labels on SNLI and MNLI using only the hypothesis as input." |
| Q72 | 6 | output_content | "The models respectively get near-chance accuracies of 32.7% and 36.4% on our diagnostic data, showing that the data does not suffer from such artifacts." |
| Q73 | 6 | output_content | "To establish human baseline performance on the diagnostic set, we have six NLP researchers annotate 50 sentence pairs (100 entailment examples) randomly sampled from the diagnostic set." |
| Q74 | 6 | output_content | "Inter-annotator agreement is high, with a Fleiss's κ of 0.73." |
| Q75 | 6 | output_form | "The average R3 score among the annotators is 0.80, much higher than any of the baseline systems described in Section 5." |
| Q76 | 6 | output_form | "The diagnostic examples are hand-picked to address certain phenomena, and NLI is a task with no natural input distribution, so we do not expect performance on the diagnostic set to reflect overall performance or generalization in downstream applications." |
| Q77 | 6 | output_form | "Performance on the analysis set should be compared between models but not between categories." |
| Q78 | 6 | output_form | "The set is provided not as a benchmark, but as an analysis tool for error analysis, qualitative model comparison, and development of adversarial examples." |
| Q79 | 6 | output_content | "We implement our models in the AllenNLP library (Gardner et al., 2017)." |
| Q80 | 6 | output_form | "Our simplest baseline architecture is based on sentence-to-vector encoders, and sets aside GLUE's ability to evaluate models with more complex structures." |
| Q81 | 6 | output_form | "Taking inspiration from Conneau et al. (2017), the model uses a two-layer, 1500D (per direction) BiLSTM with max pooling and 300D GloVe word embeddings (840B Common Crawl version; Pennington et al., 2014)." |
| Q82 | 6 | output_form | "For single-sentence tasks, we encode the sentence and pass the resulting vector to a classifier." |
| Q83 | 6 | output_form | "For sentence-pair tasks, we encode sentences independently to produce vectors u, v, and pass [u; v; \|u − v\|; u ∗ v] to a classifier." |
| Q84 | 6 | output_form | "The classifier is an MLP with a 512D hidden layer." |
| Q85 | 6 | output_form | "We also consider a variant of our model which for sentence pair tasks uses an attention mechanism inspired by Seo et al. (2017) between all pairs of words, followed by a second BiLSTM with max pooling." |
| Q86 | 6 | output_form | "By explicitly modeling the interaction between sentences, these models fall outside the sentence-to-vector paradigm." |
| Q87 | 6 | output_form | "We augment our base model with two recent methods for pre-training: ELMo and CoVe." |
| Q88 | 6 | output_form | "We use existing trained models for both." |
| Q89 | 6 | output_form | "ELMo uses a pair of two-layer neural language models trained on the Billion Word Benchmark (Chelba et al., 2013)." |
| Q90 | 6 | output_form | "Each word is represented by a contextual embedding, produced by taking a" |
| Q91 | 7 | input_form | "We train our models with the BiLSTM sentence encoder and post-attention BiLSTMs shared across tasks, and classifiers trained separately for each task." |
| Q92 | 7 | input_form | "For each training update, we sample a task to train with a probability proportional to the number of training examples for each task." |
| Q93 | 7 | input_form | "We train our models with Adam (Kingma & Ba, 2015) with initial learning rate 10−4 and batch size 128." |
| Q94 | 7 | output_form | "We use the macro-average score as the validation metric and stop training when the learning rate drops below 10−5 or performance does not improve after 5 validation checks." |
| Q95 | 7 | input_form | "We also train a set of single-task models, which are configured and trained identically, but share no parameters." |
| Q96 | 7 | output_form | "To allow for fair comparisons with the multi-task analogs, we do not tune parameter or training settings for each task, so these single-task models do not generally represent the state of the art for each task." |
| Q97 | 7 | input_ontology | "Finally, we evaluate the following trained sentence-to-vector encoder models using our benchmark: average bag-of-words using GloVe embeddings (CBoW), Skip-Thought (Kiros et al., 2015), InferSent (Conneau et al., 2017), DisSent (Nie et al., 2017), and GenSen (Subramanian et al., 2018)." |
| Q98 | 7 | input_form | "For these models, we only train task-specific classifiers on the representations they produce." |
| Q99 | 8 | output_form | "We train three runs of each model and evaluate the run with the best macro-average development set performance (see Table 6 in Appendix C)." |
| Q100 | 8 | output_form | "For single-task and sentence representation models, we evaluate the best run for each individual task." |
| Q101 | 8 | input_ontology | "We find that multi-task training yields better overall scores over single-task training amongst models using attention or ELMo." |
| Q102 | 8 | input_ontology | "Attention generally has negligible or negative aggregate effect in single task training, but helps in multi-task training." |
| Q103 | 8 | input_form | "We see a consistent improvement in using ELMo embeddings in place of GloVe or CoVe embeddings, particularly for single-sentence tasks." |
| Q104 | 8 | input_form | "Using CoVe has mixed effects over using only GloVe." |
| Q105 | 8 | input_ontology | "Among the pre-trained sentence representation models, we observe fairly consistent gains moving from CBoW to Skip-Thought to Infersent and GenSen." |
| Q106 | 8 | output_ontology | "On WNLI, no model exceeds most-frequent-class guessing (65.1%) and we substitute the model predictions for the most-frequent baseline." |
| Q107 | 8 | output_form | "On RTE and in aggregate, even our best baselines leave room for improvement." |
| Q108 | 8 | output_form | "These early results indicate that solving GLUE is beyond the capabilities of current models and methods." |
| Q109 | 9 | output_form | "We analyze the baselines by evaluating each model's MNLI classifier on the diagnostic set to get a better sense of their linguistic capabilities." |
| Q110 | 9 | output_form | "Overall performance is low for all models: The highest total score of 28 still denotes poor absolute performance." |
| Q111 | 9 | input_ontology | "Performance tends to be higher on Predicate-Argument Structure and lower on Logic, though numbers are not closely comparable across categories." |
| Q112 | 9 | output_form | "Unlike on the main benchmark, the multi-task models are almost always outperformed by their single-task counterparts." |
| Q113 | 9 | output_ontology | "Most models handle universal quantification relatively well." |
| Q114 | 9 | output_ontology | "Double negation is especially difficult for the GLUE-trained models that only use GloVe embeddings." |
| Q115 | 9 | output_form | "We expect that our platform and diagnostic dataset will be useful for similar analyses in the future, so that model designers can better understand their models' generalization behavior and implicit knowledge." |
| Q116 | 9 | input_ontology | "We introduce GLUE, a platform and collection of resources for evaluating and analyzing natural language understanding systems." |
| Q117 | 9 | output_content | "We thank Ellie Pavlick, Tal Linzen, Kyunghyun Cho, and Nikita Nangia for their comments on this work at its early stages, and we thank Ernie Davis, Alex Warstadt, and Quora's Nikhil Dandekar and Kornel Csernai for providing access to private evaluation data." |
| Q118 | 9 | output_content | "This project has benefited from financial support to SB by Google, Tencent Holdings, and Samsung Research, and to AW from AdeptMind and an NSF Graduate Research Fellowship." |
| Q119 | 13 | input_content | "To construct a balanced dataset, we select all pairs in which the most similar sentence to the question was not the answer sentence, as well as an equal amount of cases in which the correct sentence was the most similar to the question, but another distracting sentence was a close second." |
| Q120 | 13 | input_form | "Our similarity metric is based on CBoW representations with pre-trained GloVe embeddings." |
| Q121 | 13 | input_content | "This approach to converting pre-existing datasets into NLI format is closely related to recent work by White et al. (2017), as well as to the original motivation for textual entailment presented by Dagan et al. (2006)." |
| Q122 | 13 | input_ontology | "Both argue that many NLP tasks can be productively reduced to textual entailment." |
| Q123 | 14 | input_form | "We implement our attention mechanism as follows: given two sequences of hidden states u1, u2, . . . , uM and v1, v2, . . . , vN, we first compute matrix H where Hij = ui· vj." |
| Q124 | 14 | input_form | "We scale each task's loss inversely proportional to the number of examples for that task, which we found to improve overall performance." |
| Q125 | 14 | input_form | "We train our models with Adam (Kingma & Ba, 2015) with initial learning rate 10−3, batch size 128, and gradient clipping." |
| Q126 | 14 | output_form | "We use macro-average score over all tasks as our validation metric, and perform a validation check every 10k updates." |
| Q127 | 14 | input_form | "We divide the learning rate by 5 whenever validation performance does not improve." |
| Q128 | 14 | input_form | "We stop training when the learning rate drops below 10−5 or performance does not improve after 5 validation checks." |
| Q129 | 14 | input_ontology | "We evaluate the following sentence representation models: 1. CBoW, the average of the GloVe embeddings of the tokens in the sentence. 2. Skip-Thought (Kiros et al., 2015), a sequence-to-sequence(s) model trained to generate the previous and next sentences given the middle sentence. 3. InferSent (Conneau et al., 2017), a BiLSTM with max-pooling trained on MNLI and SNLI. 4. DisSent (Nie et al., 2017), a BiLSTM with max-pooling trained to predict the discourse marker (because, so, etc.) relating two sentences on data derived from TBC. 5. GenSen (Subramanian et al., 2018), a sequence-to-sequence model trained on a variety of supervised and unsupervised objectives." |
| Q130 | 14 | input_form | "We train task-specific classifiers on top of frozen sentence encoders, using the default parameters from SentEval." |
| Q131 | 14 | output_form | "The GLUE website limits users to two submissions per day in order to avoid overfitting to the private test data." |
| Q132 | 14 | input_content | "GLUE's online platform is built using React, Redux and TypeScript." |
| Q133 | 14 | input_content | "We use Google Firebase for data storage and Google Cloud Functions to host and run our grading script when a submission is made." |
| Q134 | 15 | input_ontology | "The dataset is designed to allow for analyzing many levels of natural language understanding, from word meaning and sentence structure to high-level reasoning and application of world knowledge." |
| Q135 | 15 | input_ontology | "To make this kind of analysis feasible, we first identify four broad categories of phenomena: Lexical Semantics, Predicate-Argument Structure, Logic, and Knowledge." |
| Q136 | 15 | input_ontology | "However, since these categories are vague, we divide each into a larger set of fine-grained subcategories." |
| Q137 | 15 | input_ontology | "These categories are not based on any particular linguistic theory, but broadly based on issues that linguists have often identified and modeled in the study of syntax and semantics." |
| Q138 | 15 | output_form | "The dataset is provided not as a benchmark, but as an analysis tool to paint in broad strokes the kinds of phenomena a model may or may not capture, and to provide a set of examples that can serve for error analysis, qualitative model comparison, and development of adversarial examples that expose a model's weaknesses." |
| Q139 | 15 | output_form | "Because the distribution of language is somewhat arbitrary, it will not be helpful to compare performance of the same model on different categories." |
| Q140 | 15 | output_form | "Rather, we recommend comparing performance that different models score on the same category, or using the reported scores as a guide for error analysis." |
| Q141 | 15 | output_ontology | "Note that some examples may be tagged with phenomena belonging to multiple categories." |
| Q142 | 16 | input_ontology | "These phenomena center on aspects of word meaning." |
| Q143 | 16 | input_ontology | "Entailment can be applied not only on the sentence level, but the word level." |
| Q144 | 16 | input_ontology | "This relationship applies to many types of words (nouns, adjectives, verbs, many prepositions, etc.) and the relationship between lexical and sentential entailment has been deeply explored, e.g., in systems of natural logic." |
| Q145 | 16 | input_ontology | "This is a special case of lexical contradiction where one word is derived from the other: from "affordable" to "unaffordable", "agree" to "disagree", etc." |
| Q146 | 16 | input_ontology | "Propositions appearing in a sentence may be in any entailment relation with the sentence as a whole, depending on the context in which they appear." |
| Q147 | 16 | input_ontology | "In many cases, this is determined by lexical triggers (usually verbs or adverbs) in the sentence." |
| Q148 | 16 | output_ontology | "We place all examples involving these phenomena under the label of Factivity." |
| Q149 | 16 | input_ontology | "Some propositions denote symmetric relations, while others do not." |
| Q150 | 16 | input_ontology | "Whether a relation is symmetric, or admits collecting its arguments into the subject, is often determined by its head word (e.g., "like", "marry" or "meet"), so we classify it under Lexical Semantics." |
| Q151 | 16 | input_ontology | "If a word can be removed from a sentence without changing its meaning, that means the word's meaning was more-or-less adequately expressed by the sentence; so, identifying these cases reflects an understanding of both lexical and sentential semantics." |
| Q152 | 17 | input_ontology | "Named Entities Words often name entities that exist in the world. There are many different kinds of understanding we might wish to understand about these names, including their compositional structure (for example, the "Baltimore Police" is the same as the "Police of the City of Baltimore") or their real-world referents and acronym expansions (for example, "SNL" is "Saturday Night Live"). This category is closely related to World Knowledge, but focuses on the semantics of names as lexical items rather than background knowledge about their denoted entities." |
| Q153 | 17 | input_ontology | "Quantifiers Logical quantification in natural language is often expressed through lexical triggers such as "every", "most", "some", and "no". While we reserve the categories in Quantification and Monotonicity for entailments involving operations on these quantifiers and their arguments, we choose to regard the interchangeability of quantifiers (e.g., in many cases "most" entails "many") as a question of lexical semantics." |
| Q154 | 17 | input_ontology | "An important component of understanding the meaning of a sentence is understanding how its parts are composed together into a whole. In this category, we address issues across that spectrum, from syntactic ambiguity to semantic roles and coreference." |
| Q155 | 17 | input_ontology | "Syntactic Ambiguity: Relative Clauses, Coordination Scope These two categories deal purely with resolving syntactic ambiguity. Relative clauses and coordination scope are both sources of a great amount of ambiguity in English." |
| Q156 | 17 | input_ontology | "Prepositional phrase attachment is a particularly difficult problem that syntactic parsers in NLP systems continue to struggle with. We view it as a problem both of syntax and semantics, since prepositional phrases can express a wide variety of semantic roles and often semantically apply beyond their direct syntactic attachment." |
| Q157 | 17 | input_ontology | "Core Arguments Verbs select for particular arguments, particularly subjects and objects, which might be interchangeable depending on the context or the surface form. One example is the ergative alternation: "Jake broke the vase" entails "the vase broke" but "Jake broke the vase" does not entail "Jake broke". Other rearrangements of core arguments, such as those seen in Symmetry/Collectivity, also fall under the Core Arguments label." |
| Q158 | 17 | input_ontology | "Alternations: Active/Passive, Genitives/Partitives, Nominalization, Datives All four of these categories correspond to syntactic alternations that are known to follow specific patterns in English: Active/Passive: "I saw him" is equivalent to "He was seen by me" and entails "He was seen". Genitives/Partitives: "the elephant's foot" is the same thing as "the foot of the elephant". Nominalization: "I caused him to submit his resignation" entails "I caused the submission of his resignation". Datives: "I baked him a cake" entails "I baked a cake for him" and "I baked a cake" but not "I baked him"." |
| Q159 | 17 | input_ontology | "Ellipsis/Implicits Often, the argument of a verb or other predicate is omitted (elided) in the text, with the reader filling in the gap. We can construct entailment examples by explicitly filling in the gap with the correct or incorrect referents. For example, the premise "Putin is so entrenched within Russias ruling system that many of its members can imagine no other leader" entails "Putin is so entrenched within Russias ruling system that many of its members can imagine no other leader than Putin" and contradicts "Putin is so entrenched within Russias ruling system that many of its members can imagine no other leader than themselves."" |
| Q160 | 17 | input_ontology | "This is often regarded as a special case of anaphora, but we decided to split out these cases from explicit anaphora, which is often also regarded as a case of coreference (and attempted to some degree in modern coreference resolution systems)." |
| Q161 | 18 | input_ontology | "Coreference refers to when multiple expressions refer to the same entity or event." |
| Q162 | 18 | input_ontology | "It is closely related to Anaphora, where the meaning of an expression depends on another (antecedent) expression in context." |
| Q163 | 18 | input_ontology | "These two phenomena have significant overlap; for example, pronouns ("she", "we", "it") are anaphors that are co-referent with their antecedents." |
| Q164 | 18 | input_ontology | "In this category we only include cases where there is an explicit phrase (anaphoric or not) that is co-referent with an antecedent or other phrase." |
| Q165 | 18 | input_content | "We construct examples for these in much the same way as for Ellipsis/Implicits." |
| Q166 | 18 | input_ontology | "Many modifiers, especially adjectives, allow non-intersective uses, which affect their entailment behavior." |
| Q167 | 18 | input_ontology | "Generally, an intersective use of a modifier, like "old" in "old men", is one which may be interpreted as referring to the set of entities with both properties (they are old and they are men)." |
| Q168 | 18 | input_ontology | "Intersectivity is related to Factivity." |
| Q169 | 18 | input_ontology | "However, we choose to categorize intersectivity under predicate-argument structure rather than lexical semantics, because generally the same word will admit both intersective and non-intersective uses, so it may be regarded as an ambiguity of argument structure." |
| Q170 | 18 | input_ontology | "Restrictivity is most often used to refer to a property of uses of noun modifiers." |
| Q171 | 18 | input_ontology | "In particular, a restrictive use of a modifier is one that serves to identify the entity or entities being described, whereas a non-restrictive use adds extra details to the identified entity." |
| Q172 | 18 | input_ontology | "Modifiers that are commonly used non-restrictively are appositives, relative clauses starting with "which" or "who", and expletives (e.g. "pesky")." |
| Q173 | 18 | input_ontology | "With an understanding of the structure of a sentence, there is often a baseline set of shallow conclusions that can be drawn using logical operators and often modeled using the mathematical tools of logic." |
| Q174 | 18 | input_ontology | "All of the basic operations of propositional logic appear in natural language, and we tag them where they are relevant to our examples:" |
| Q175 | 19 | input_ontology | "Conjunction: "Temperature and snow consistency must be just right" entails "Temperature must be just right"." |
| Q176 | 19 | input_ontology | "Disjunction: "Life is either a daring adventure or nothing at all" does not entail, but is entailed by, "Life is a daring adventure"." |
| Q177 | 19 | input_ontology | "Conditionals: "If both apply, they are essentially impossible" does not entail "They are essentially impossible"." |
| Q178 | 19 | input_ontology | "Conditionals are more complicated because their use in language does not always mirror their meaning in logic." |
| Q179 | 19 | input_ontology | "For example, they may be used at a higher level than the at-issue assertion: "If you think about it, it's the perfect reverse psychology tactic" entails "It's the perfect reverse psychology tactic"." |
| Q180 | 19 | input_ontology | "Quantifiers are often triggered by words such as "all", "some", "many", and "no"." |
| Q181 | 19 | input_ontology | "Universal: "All parakeets have two wings" entails, but is not entailed by, "My parakeet has two wings"." |
| Q182 | 19 | input_ontology | "Existential: "Some parakeets have two wings" does not entail, but is entailed by, "My parakeet has two wings"." |
| Q183 | 19 | input_ontology | "Monotonicity is a property of argument positions in certain logical systems." |
| Q184 | 19 | input_ontology | "In general, it gives a way of deriving entailment relations between expressions that differ on only one subexpression." |
| Q185 | 19 | input_ontology | ""a" is upward monotone in its restrictor: an entailment in the restrictor yields an entailment of the whole statement." |
| Q186 | 19 | input_ontology | ""no" is downward monotone in its restrictor: an entailment in the restrictor yields an entailment of the whole statement in the opposite direction." |
| Q187 | 19 | input_ontology | ""exactly one" is non-monotone in its restrictor: entailments in the restrictor do not yield entailments of the whole statement." |
| Q188 | 19 | input_ontology | "In this way, entailments between sentences that are built off of entailments of sub-phrases almost always rely on monotonicity judgments; see, for example, Lexical Entailment." |
| Q189 | 19 | input_ontology | "However, because this is such a general class of sentence pairs, to keep the Logic category meaningful we do not always tag these examples with monotonicity." |
| Q190 | 19 | input_ontology | "Some higher-level facets of reasoning have been traditionally modeled using logic, such as actual mathematical reasoning (entailments based off of numbers) and temporal reasoning (which is often modeled as reasoning about a mathematical timeline)." |
| Q191 | 19 | input_ontology | "Intervals/Numbers: "I have had more than 2 drinks tonight" entails "I have had more than 1 drink tonight"." |
| Q192 | 19 | input_ontology | "Temporal: "Mary left before John entered" entails "John entered after Mary left"." |
| Q193 | 20 | input_ontology | "Strictly speaking, world knowledge and common sense are required on every level of language understanding for disambiguating word senses, syntactic structures, anaphora, and more." |
| Q194 | 20 | input_ontology | "However, in these categories, we gather examples where the entailment rests not only on correct disambiguation of the sentences, but also application of extra knowledge, whether concrete knowledge about world affairs or more common-sense knowledge about word meanings or social or physical dynamics." |
| Q195 | 20 | input_ontology | "World Knowledge In this category we focus on knowledge that can clearly be expressed as facts, as well as broader and less common geographical, legal, political, technical, or cultural knowledge." |
| Q196 | 20 | input_ontology | "Common Sense In this category we focus on knowledge that is more difficult to express as facts and that we expect to be possessed by most people independent of cultural or educational background." |
| Q197 | 20 | input_ontology | "This includes a basic understanding of physical and social dynamics as well as lexical meaning (beyond simple lexical entailment or logical relations)." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.justarrived.lu/en/emploi-formation-luxembourg/marche-emploi-population-active/ |
| WEB-2 | https://european-language-equality.eu/wp-content/uploads/2022/03/ELE___Deliverable_D1_24__Language_Report_Luxembourgish_.pdf |
| WEB-3 | https://statistiques.public.lu/en/publications/series/en-chiffres/2024/demographie-lux-en-chiffres-2024.html |
| WEB-4 | https://luxembourg.public.lu/en/society-and-culture/population/demographics.html |
| WEB-5 | https://www.migrationpolicy.org/country-resource/luxembourg |
| WEB-6 | https://statistiques.public.lu/en/publications/series/regards/2025/regards-01-25.html |
| WEB-7 | https://www.oecd.org/en/publications/2025/04/oecd-economic-surveys-luxembourg-2025_3eb782b5/full-report/reviving-productivity-growth_4509ab88.html |
| WEB-8 | https://www.leretourdelautruche.com/en/scale-up-en/managing-cross-border-employees-france-luxembourg-complete-hr-guide-2026/ |
| WEB-9 | https://www.ogbl.lu/en/frontaliers/ |
| WEB-10 | https://arxiv.org/abs/2604.17976 |
| WEB-11 | https://arxiv.org/html/2603.10789 |
| WEB-12 | https://arxiv.org/html/2412.09383v1 |
| WEB-13 | https://aclanthology.org/2022.lrec-1.543.pdf |
| WEB-14 | https://sirajzade.github.io/papers/CRC_industrial_paper_84.pdf |
| WEB-15 | https://github.com/questoph/spellux |
| WEB-16 | https://elections.public.lu/en/fusion-communes.html |
| WEB-17 | https://gouvernement.lu/en/actualites/toutes_actualites/communiques/2023/02-fevrier/10-100-communes.html |
| WEB-18 | https://en.wikipedia.org/wiki/Communes_of_Luxembourg |
| WEB-19 | https://www.sng-wofi.org/country_profiles/luxembourg.html |
| WEB-20 | https://luxembourg.public.lu/en/living/mobility/public-transport.html |
| WEB-21 | https://transports.public.lu/en/plus/faq/gratuite-transports-publics.html |
| WEB-22 | https://artificialintelligenceact.eu/annex/3/ |
| WEB-23 | https://artificialintelligenceact.eu/article/6/ |
| WEB-24 | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai |
| WEB-25 | https://aclanthology.org/2020.sltu-1.22.pdf |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** nyu-mll/glue (configs: ax, cola, mnli, mnli_matched, mnli_mismatched, mrpc, qnli, qqp, rte, sst2, stsb, wnli)
**Analysis date:** 2025-01-31
**Examples reviewed:** 26 (ax/test) + 78 (cola/train) + 23 (mnli/train) + 20 (mnli_matched/validation) + 20 (mnli_mismatched/validation) + 18 (mrpc/train) + 17 (qnli/train) + 33 (qqp/train) + 17 (rte/train) + 77 (sst2/train) + 54 (stsb/train) + 26 (wnli/train) = **409 examples total**
**Columns shown:** premise, hypothesis, label, idx (ax/mnli); sentence, label, idx (cola/sst2); sentence1, sentence2, label, idx (mrpc/rte/wnli/stsb); question, sentence, label, idx (qnli); question1, question2, label, idx (qqp)
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | sst2 | idx=383 | negative | "sleepwalk through vulgarities in a sequel you can refuse" | English movie-review fragment; sentiment label calibrated to film criticism register | OC |
| D2 | sst2 | idx=164 | positive | "at its best moments" | Sub-sentential movie-review fragment; context-free without film domain | IC |
| D3 | sst2 | idx=462 | negative | "the weird thing about the santa clause 2 , purportedly a children 's movie , is that there is nothing in it to engage children emotionally ." | Full sentence from American movie review; US pop-culture reference | IC, OC |
| D4 | sst2 | idx=49 | negative | "no lika da" | Non-standard English fragment (phonetic representation); unclear sentiment signal | IC, OC |
| D5 | sst2 | idx=278 | positive | "is a pan-american movie , with moments of genuine insight into the urban heart ." | Movie-review sentence referencing pan-American themes | IC |
| D6 | cola | idx=383 | unacceptable | "The fact that no candidate was elected shows that he was inadequate." | English linguistics acceptability judgment | IO |
| D7 | cola | idx=45 | acceptable | "The wagon rumbled down the road." | Simple English sentence; acceptability=1 from linguistics journal | IO |
| D8 | cola | idx=18 | unacceptable | "They drank the pub." | Idiomatic English usage; grammatical acceptability judgment | IO |
| D9 | mnli | idx=164 | entailment | "do they live close by" / "Is their house near here?" | Spoken-register English NLI pair; casual American dialogue | IC |
| D10 | mnli | idx=53 | neutral | "I did not mention Monica in my lecture, but the first question I was asked was how President Clinton could do his job with all the distractions caused by the Monica Lewinsky affair." | US political context (Clinton/Lewinsky); culturally US-specific | IC |
| D11 | mnli | idx=215 | neutral | "Yes, Mistuh Reese, suh?" | Dialect representation of African American vernacular in fiction | IC |
| D12 | mnli_matched | idx=53 | neutral | "The Celts arrived in the wake of the Roman withdrawal at the end of the fourth century." | European historical content (RTE/Wikipedia domain) | IC |
| D13 | mrpc | idx=184 | equivalent | "Platinum prices soared to 23-year highs earlier this year after President Bush (news - web sites) proposed investing $ 1.2 billion for research on fuel cell-powered vehicles." | US political and financial news paraphrase | IC |
| D14 | mrpc | idx=249 | not_equivalent | "Mr. Bush had sought to store his papers in his father's presidential library, where they would have stayed secret for a half-century." | US presidential politics; US-specific cultural/political context | IC |
| D15 | qnli | idx=164 | entailment | "Who succeeded Newt Gingrich as Speaker?" / "In 1998, with Speaker Newt Gingrich announcing his resignation..." | US political history QA; requires US-specific knowledge | IC, IO |
| D16 | qqp | idx=164 | duplicate | "What is black money and how can it effect the economy of a country?" / "What is the effect of black money on India's macro economy?" | Quora question pair; Indian economic/policy context | IC |
| D17 | qqp | idx=245 | duplicate | "How do mountain ranges form, and what are some of the major mountain ranges in Oklahoma?" / "How do mountain ranges in Oklahoma differ from mountain ranges in Idaho?" | US geography; Quora community context | IC |
| D18 | qqp | idx=228 | duplicate | "Are the notes of Rs. 2000 really embedded with a GPS chip?" / "How does the embedded NGC technology of the Rs. 2000 note works?" | India-specific currency question; non-EU political context | IC |
| D19 | rte | idx=156 | not_entailment | "National currencies will be completely replaced by the euro in within six months after the introduction of euro notes and coins." / "The introduction of the euro has been opposed." | EU-relevant content; textual entailment task with European economic content | IC |
| D20 | rte | idx=383 | entailment | "In-form Rooney's hot goalscoring streak of seven goals in his last four internationals saw him win the vote to be crowned England's Player of the Year for 2008." | British sports news; no Luxembourg administrative relevance | IC |
| D21 | ax | idx=164 | contradiction | "The combination of mentos and diet coke caused the explosion." / "Combining mentos and diet coke caused the explosion." | Diagnostic NLI pair; near-paraphrase with subtle label=-1 anomaly | OO |
| D22 | ax | idx=92 | contradiction | "House Speaker Paul Ryan was facing problems uniquely from fellow Republicans dissatisfied with his leadership." / "House Speaker Paul Ryan was facing problems uniquely from fellow Republicans supportive of his leadership." | US political content in diagnostic set | IC |
| D23 | ax | idx=333 | contradiction | "Poor Irish people could not get food because it was too expensive." / "The problem in Ireland was not lack of food, which was plentiful, but the price of it, which was beyond the reach of the poor." | Historical European content; diagnostic entailment reasoning | OO |
| D24 | stsb | idx=164 | 4.0 | "A person is boiling noodles." / "A woman is boiling noodles in water." | Image-caption pair; STS similarity regression | IO |
| D25 | stsb | idx=383 | 2.25 | "A man is tying on a stenographers machine." / "the man used a stenograph." | Image-caption pair; generic action description | IO |
| D26 | wnli | idx=45 | not_entailment | "Sara borrowed the book from the library because she needs it for an article she is working on. She writes it when she gets home from work." / "She writes the book when she gets home from work." | Winograd pronoun coreference; English fiction-based | IO |
| D27 | cola | idx=303 | unacceptable | "This is a problem that you'll be able to tell the folks up at corporate headquarters to buzz off if you solve." | Colloquial American English; grammaticality judgment from linguistics journal | IC |
| D28 | mnli | idx=8 | neutral | "Yes, Mistuh Reese, suh?" / "The slave spoke to Mr Reece." | Dialect transcription from American fiction (antebellum setting) | IC |
| D29 | sst2 | idx=50 | negative | "the horrors" | Two-word fragment; highly context-dependent sentiment label | OC |
| D30 | sst2 | idx=37 | positive | "heroes" | Single-word fragment; no sentential context | OC |
| D31 | qnli | idx=74 | not_entailment | "Who was at one time Laemmle's personal secretary?" / "Thalberg had been Laemmle's personal secretary..." | Wikipedia QA requiring Hollywood history knowledge | IC |
| D32 | ax | idx=45 | contradiction | "In example (1) it is quite easy to see the exaggerated positive sentiment used in order to convey strong negative feelings." / "In example (1) it is quite straightforward to see the exaggerated positive sentiment used in order to convey strong negative feelings." | Academic NLP paper text in diagnostic set | IC |
| D33 | mnli | idx=368 | neutral | "oh yeah no that's uh that's a that's a real interesting movie and it's got a good historical perspective to it" | Transcribed telephone speech; casual American spoken English | IC, IF |
| D34 | ax | idx=479 | contradiction | "The announcement of Tillerson's departure sent shock waves across the globe." / "People across the globe were prepared for Tillerson's departure." | US political news (Rex Tillerson/Trump administration) in diagnostic set | IC |
| D35 | rte | idx=479 | not_entailment | "Budapest consists of two parts, Buda and Pest, which are situated on opposite sides of the river and connected by a series of bridges." / "Buda is located on the west bank of the Danube." | European geography in news-based RTE; geographically proximate to Luxembourg | IC |
| D36 | mrpc | idx=61 | not_equivalent | "The women then had follow-up examinations after five , 12 and 24 years ." / "The women had follow-up examinations in 1974-75 , 1980-81 and 1992-93 , but were not asked about stress again ." | News paraphrase detection; health domain, no administrative relevance | IO |
| D37 | ax | idx=209 | contradiction | "This means that seeking a word that is similar to x and y but is different from z is mathematically equivalent to solving analogy questions with vector arithmetic." / "This means that solving analogy questions with vector arithmetic is mathematically equivalent to seeking a word that is similar to x and y but is different from z." | NLP academic paper text; symmetry reasoning in diagnostic set | IO |
| D38 | qqp | idx=368 | not_duplicate | "What is it to be a lesbian?" / "How does it feel to be a lesbian?" | Quora social question; identity topic | IC |
| D39 | stsb | idx=45 | 1.0 | "A man is playing the piano." / "A woman is playing the violin." | Image-caption STS; everyday activity scenes | IO |
| D40 | cola | idx=425 | unacceptable | "The children eat all chocolate." | English determiner usage; grammaticality judgment | IO |
| D41 | mnli_mismatched | idx=383 | neutral | "Southern manufacturers had already adopted steam engines for textile production, along with newer and more productive technology." | US historical text; 19th century American industrialization | IC |
| D42 | ax | idx=415 | contradiction | "Grisham did not win the popular vote." / "Grisham almost won the popular vote." | US electoral context in diagnostic set | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Well-balanced binary and three-class label distributions enable class-distribution analysis
- **Dimension(s):** OO
- **Observation:** The sampled data shows balanced label distributions across tasks: SST-2 (241 negative / 259 positive in buffer), MNLI (178/140/182 across three classes), CoLA (171 unacceptable / 329 acceptable), RTE (245/255). This balance is documented as intentional and validated by Matthews Correlation Coefficient for unbalanced cases. The multi-task structure provides a model for designing evaluation suites that separately score multiple capabilities.
- **Deployment relevance:** While GLUE's specific labels are irrelevant to Luxembourgish administrative routing, the framework of measuring each task separately and macro-averaging — demonstrated concretely across 12 configs with distinct schema and label spaces — offers a structural template for a custom Luxembourgish benchmark suite combining NER, intent classification, sentiment, and routing tasks.
- **Datapoint citations:**
  - [D6] cola, split=train, label=unacceptable: "The fact that no candidate was elected shows that he was inadequate." — Representative of clear binary labeling scheme with documented acceptability judgments
  - [D21] ax, split=test, label=contradiction (label=-1): "The combination of mentos and diet coke caused the explosion." / "Combining mentos and diet coke caused the explosion." — Illustrates the NLI three-class schema and how near-paraphrase pairs are distinguished; note the label=-1 encoding for contradiction in the ax config suggests test labels are masked, consistent with documented private test label practice

#### Strength 2: Diagnostic (ax) dataset demonstrates systematic linguistic phenomenon coverage
- **Dimension(s):** IO, OO
- **Observation:** The ax config examples systematically probe quantifier scope, negation, coreference, temporal reasoning, and logical operators (conditionals, disjunction) as documented. The sampled 26 examples show genuine variety across phenomenon types: scalar implication (D5/idx=5, "Some" vs. "Most"), additive modification (idx=443, "father of the nation and the man uniquely equipped"), coreference (idx=289), and world knowledge (idx=333 on Irish famine).
- **Deployment relevance:** The diagnostic set's methodology — constructing minimal-pair sentence sets that differ on exactly one linguistic dimension — is transferable as a design pattern for probing Luxembourgish model capabilities in NER boundary sensitivity, negation in formal correspondence, and temporal reasoning in administrative contexts. This is the single most methodologically reusable element of GLUE for the deployment.
- **Datapoint citations:**
  - [D23] ax, split=test, label=contradiction: "Poor Irish people could not get food because it was too expensive." / "The problem in Ireland was not lack of food, which was plentiful, but the price of it, which was beyond the reach of the poor." — Illustrates world knowledge reasoning probe in diagnostic set; this methodology (minimal edits + phenomenon tagging) is transferable
  - [D37] ax, split=test, label=contradiction: "This means that seeking a word that is similar to x and y but is different from z is mathematically equivalent to solving analogy questions with vector arithmetic." / "This means that solving analogy questions with vector arithmetic is mathematically equivalent to seeking a word that is similar to x and y but is different from z." — Probes symmetry/reversibility reasoning; technique applicable to testing Luxembourgish administrative NLU models on logical inference

#### Strength 3: NLI task structure covers some linguistically universal reasoning patterns
- **Dimension(s):** IO
- **Observation:** Several MNLI and MNLI-matched examples test reasoning patterns that are language-agnostic in principle: set membership, negation, scalar implication, causal inference. These phenomena appear in the sampled data with varied surface forms.
- **Deployment relevance:** An NLU model for Luxembourgish administrative routing must handle negation (e.g., "je ne suis pas frontalier" / "ech sinn kee Frontalier"), scalar implication, and causal chains in citizen correspondence. To the extent that GLUE's NLI tasks exercise these reasoning patterns, a model's GLUE performance provides weak evidence about its general logical reasoning competence, though not its Luxembourgish-specific or domain-specific capabilities.
- **Datapoint citations:**
  - [D9] mnli, split=train, label=entailment: "do they live close by" / "Is their house near here?" — Tests paraphrase/entailment across register variation; logically universal pattern
  - [D1] mnli, split=train, label=entailment (idx=163): "At the heart of the sanctuary, a small granite shrine once held the sacred barque of Horus himself." / "Horus has a shrine." — Tests proposition extraction; logically universal but requires cultural/religious world knowledge

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Complete absence of any Luxembourgish, French, or German language data
- **Dimension(s):** IC, IF
- **Observation:** Every single example reviewed across all 12 configs is in English. The 409 sampled examples contain no Luxembourgish tokens, no French text, and no German text. The HF metadata confirms `"languages": ["en"]` and `"multilinguality:monolingual"`. The benchmark's input signal — standardized written American/British English drawn from news, movie reviews, Wikipedia, and web forums — has zero overlap with the trilingual, code-switched, non-standardized Luxembourgish input the deployed system will process.
- **Deployment relevance:** The elicitation identifies input language as HIGH priority. Even formally intended Luxembourgish citizen correspondence exhibits code-switching between Luxembourgish, French, and German, with non-standardized Luxembourgish spelling (best normalization model achieves only ~78.8% accuracy per web findings). GLUE provides no signal whatsoever about a model's ability to handle this input distribution. A model that achieves high GLUE scores but has never processed Luxembourgish text could score 0% on the actual deployment task.
- **Datapoint citations:**
  - [D1] sst2, split=train, label=negative: "sleepwalk through vulgarities in a sequel you can refuse" — English movie-review fragment; not a single non-English word appears in the entire sampled dataset
  - [D9] mnli, split=train, label=entailment: "do they live close by" / "Is their house near here?" — Casual American spoken English; the contrast with Luxembourgish administrative register (e.g., "Ech wëll eng Fro stellen iwwer mäin Steierstatus als Frontalier") could not be more complete
  - [D33] mnli, split=train, label=neutral: "oh yeah no that's uh that's a that's a real interesting movie and it's got a good historical perspective to it" — Transcribed American telephone speech; this is the input register GLUE trains NLU models on, vs. formal Luxembourgish administrative correspondence

#### Concern 2: Zero administrative domain content — no routing, intent, or government competency categories
- **Dimension(s):** IO
- **Observation:** Across 409 examples, no example touches any administrative, government, or civic domain relevant to the deployment: no housing queries, no cross-border worker status, no national vs. communal routing, no social security, no immigration, no taxation, no public transport. The tasks cover movie sentiment, paraphrase detection among news sentences, QA from Wikipedia, and acceptability judgments from linguistics journals. The closest approximation is MNLI's use of "government reports" as one of ten premise sources, but none of these appear in the sampled examples.
- **Deployment relevance:** The deployment's core function is routing citizen messages to national or communal departments based on topic and intent. GLUE provides no ontological coverage of the required categories: cross-border worker / frontalier status, national vs. communal competency, housing urgency, social security, immigration, or public transport (Luxembourg's notable free-transport policy). IO is marked HIGH priority in the elicitation, and this gap is total.
- **Datapoint citations:**
  - [D15] qnli, split=train, label=entailment: "Who succeeded Newt Gingrich as Speaker?" — US congressional politics; the contrast with the deployment's required categories (e.g., "Is this message about a frontalier's pension entitlement?") illustrates the complete category mismatch
  - [D36] mrpc, split=train, label=not_equivalent: "The women then had follow-up examinations after five , 12 and 24 years ." / "The women had follow-up examinations in 1974-75 , 1980-81 and 1992-93 , but were not asked about stress again ." — Health news paraphrase; no administrative routing relevance
  - [D24] stsb, split=train, label=4.0: "A person is boiling noodles." / "A woman is boiling noodles in water." — Image-caption similarity; completely unrelated to administrative correspondence processing

#### Concern 3: Sentiment labels calibrated to English movie-review register, not Luxembourgish formal administrative correspondence
- **Dimension(s):** OC, IC
- **Observation:** All 77 sampled SST-2 examples are sub-sentential or full-sentence fragments from English movie reviews. Many are decontextualized fragments that depend on film-criticism conventions for their sentiment polarity (e.g., [D2] "at its best moments" = positive; [D30] "heroes" = positive; [D29] "the horrors" = negative). Several fragments are too short to carry unambiguous sentiment signals without film-review context. The annotator pool is not documented, but the domain (film criticism) and language (American English) bear no relation to formal Luxembourgish administrative correspondence, which is characterized by understated register even when expressing urgency or frustration.
- **Deployment relevance:** OC is HIGH priority. The deployment requires sentiment/frustration detection in formal administrative correspondence, where frustration is expressed indirectly through formal language (e.g., "Je me permets de vous contacter une fois de plus concernant ma demande du 15 mars..."). Labels trained on explicit, colloquial English film criticism sentiment will systematically fail to detect the understated frustration signals in Luxembourgish administrative correspondence. The elicitation explicitly flagged this as a "live risk."
- **Datapoint citations:**
  - [D3] sst2, split=train, label=negative: "the weird thing about the santa clause 2 , purportedly a children 's movie , is that there is nothing in it to engage children emotionally ." — US pop-culture movie reference; sentiment label depends on film-criticism knowledge
  - [D4] sst2, split=train, label=negative: "no lika da" — Phonetic/dialectal fragment; sentiment label is nearly uninterpretable without full review context; would be meaningless in any Luxembourgish administrative context
  - [D2] sst2, split=train, label=positive: "at its best moments" — Three-word decontextualized fragment; the annotation assumes the reviewer's film-criticism context, which transfers to no other domain
  - [D29] sst2, split=train, label=negative: "the horrors" — Two-word fragment with implicit film-review context; no transferable signal

#### Concern 4: Output taxonomy is binary/ternary hard classification; no multi-label or confidence scoring
- **Dimension(s):** OO, OF
- **Observation:** Every classification task in the sampled data uses exactly one label per example (binary or three-class). The ax config shows labels encoded as -1 (contradiction) in the test split, confirming that even the diagnostic set uses hard single labels. No example has multiple labels, soft labels, or confidence scores. The schema metadata confirms: `"ClassLabel(3 classes)"` for NLI tasks and `"ClassLabel(2 classes)"` for all others, with no probability or confidence field present.
- **Deployment relevance:** OO is HIGH priority. The deployment requires multi-label classification (a single citizen message may concern housing AND frontalier tax status AND municipal routing simultaneously) plus confidence scores to flag uncertain cases for human review. GLUE's hard single-label paradigm cannot be adapted to this requirement without fundamental restructuring — it is not a matter of threshold-tuning but of ontological incompatibility. The macro-average GLUE score will not predict multi-label routing quality.
- **Datapoint citations:**
  - [D21] ax, split=test, label=contradiction (label=-1): "The combination of mentos and diet coke caused the explosion." / "Combining mentos and diet coke caused the explosion." — label=-1 confirms hard single-label encoding even for the diagnostic set
  - [D26] wnli, split=train, label=not_entailment: "Sara borrowed the book from the library because she needs it for an article she is working on. She writes it when she gets home from work." / "She writes the book when she gets home from work." — Binary label; no provision for partial or uncertain classification

#### Concern 5: US-centric cultural and political content dominates inputs across multiple tasks
- **Dimension(s):** IC
- **Observation:** Multiple tasks contain US-specific political, cultural, and institutional references that would require American background knowledge to fully process: US congressional politics (Newt Gingrich, Paul Ryan — [D15], [D22]), US presidential politics (Clinton/Lewinsky — [D10], Bush — [D13], [D14], Tillerson — [D34]), US legal and financial news (MRPC), US sports (Auburn High School Athletic Hall of Fame — RTE idx=92). The Quora dataset (QQP) also contains India-specific content ([D16], [D18]) but with no Luxembourgish or European administrative content.
- **Deployment relevance:** While a model trained on GLUE develops some general NLU capability, the cultural knowledge required for correct predictions is primarily American. The deployment population's knowledge context is Luxembourgish/European administrative culture. Construct-irrelevant variance from US-specific cultural references will inflate or deflate GLUE scores in ways that do not predict performance on Luxembourg administrative content.
- **Datapoint citations:**
  - [D10] mnli, split=train, label=neutral: "I did not mention Monica in my lecture, but the first question I was asked was how President Clinton could do his job with all the distractions caused by the Monica Lewinsky affair." — US political scandal; requires American political history knowledge for NLI judgment
  - [D22] ax, split=test, label=contradiction: "House Speaker Paul Ryan was facing problems uniquely from fellow Republicans dissatisfied with his leadership." / "House Speaker Paul Ryan was facing problems uniquely from fellow Republicans supportive of his leadership." — US political reference embedded in diagnostic set
  - [D42] ax, split=test, label=contradiction: "Grisham did not win the popular vote." / "Grisham almost won the popular vote." — US electoral context; "popular vote" is a distinctly American electoral concept with no direct Luxembourgish administrative equivalent

#### MAJOR

#### Concern 6: SST-2 fragments are decontextualized and incomplete — many examples carry no reliable sentiment signal
- **Dimension(s):** IC, OC
- **Observation:** A substantial portion of the 77 sampled SST-2 examples are sub-sentential fragments: "at its best moments" (positive), "seem fresh" (positive), "of saucy" (positive), "imax in short" (positive), "sometimes dry" (negative), "the horrors" (negative), "ugly digital video" (negative). These fragments are sentence tree nodes extracted from parsed movie reviews and labeled based on the sentiment of the full review context, not the fragment itself. The sentiment signal in many fragments is ambiguous or absent without the surrounding film-review context.
- **Deployment relevance:** Even if a Luxembourgish administrative correspondence benchmark were to include a sentiment task, this SST-2 methodology — extracting decontextualized sub-sentential fragments and labeling them with film-review sentiment — would be a poor model for labeling formal administrative messages. The fragment-level annotation may actually train models to respond to surface-level evaluative adjectives rather than holistic communicative intent, which is the opposite of what the deployment needs.
- **Datapoint citations:**
  - [D2] sst2, split=train, label=positive: "at its best moments" — Three-word locative-temporal phrase; positive label depends entirely on film-review context
  - [D4] sst2, split=train, label=negative: "no lika da" — Phonetic/colloquial fragment; no clear sentiment without context
  - [D30] sst2, split=train, label=positive: "heroes" — Single-word label; sentiment annotation here is entirely context-dependent

#### Concern 7: CoLA (linguistic acceptability) tests English-specific syntactic phenomena with no transfer value
- **Dimension(s):** IO, IC
- **Observation:** All 78 sampled CoLA examples test English-specific grammaticality: English comparative constructions ("The more people that arrive, the louder it gets" — acceptable; "The harder it rains, how much faster that do you run?" — unacceptable), English pronoun binding, English verb phrase ellipsis, English article usage. These phenomena are specific to English morphosyntax and have no equivalent in Luxembourgish, French, or German grammatical structure.
- **Deployment relevance:** The deployment has no linguistic acceptability classification requirement. More importantly, a model fine-tuned on CoLA will have optimized parameters for English syntactic well-formedness detection, which is not only irrelevant to Luxembourgish administrative NLU but may actively interfere with processing grammatically non-standard Luxembourgish input (non-standard spelling, code-switching) by treating it as "unacceptable."
- **Datapoint citations:**
  - [D8] cola, split=train, label=unacceptable: "They drank the pub." — English-specific argument structure violation (unergative/transitive alternation); no Luxembourgish administrative relevance
  - [D40] cola, split=train, label=unacceptable: "The children eat all chocolate." — English determiner usage; this tests English-specific mass noun determiner constraints
  - [D27] cola, split=train, label=unacceptable: "This is a problem that you'll be able to tell the folks up at corporate headquarters to buzz off if you solve." — Colloquial American English construction; grammaticality judgment presupposes American English native speaker norms

#### Concern 8: STS-B image-caption pairs are semantically trivial and domain-irrelevant
- **Dimension(s):** IO, IC
- **Observation:** The sampled STS-B examples are predominantly image-caption pairs describing simple physical actions: "A person is boiling noodles." / "A woman is boiling noodles in water." (similarity=4.0); "A man is playing the piano." / "A woman is playing the violin." (similarity=1.0); "A woman is riding a motorized scooter down a road." / "A man is riding a motor scooter." (similarity=2.2). These pairs describe concrete physical scenes with no semantic complexity relevant to administrative correspondence.
- **Deployment relevance:** The deployment has no semantic similarity scoring requirement for image-caption pairs. Scores on STS-B measure a model's ability to rate similarity between action descriptions about everyday physical activities, which contributes nothing to predicting performance on assessing semantic similarity between citizen message phrasings or between routing category descriptions in Luxembourgish administrative text.
- **Datapoint citations:**
  - [D24] stsb, split=train, label=4.0: "A person is boiling noodles." / "A woman is boiling noodles in water." — Image caption pair; trivial semantic similarity with no administrative domain relevance
  - [D25] stsb, split=train, label=2.25: "A man is tying on a stenographers machine." / "the man used a stenograph." — Physical action STS pair; no administrative domain relevance

#### Concern 9: MNLI includes fiction and spoken dialogue that misrepresents the target register
- **Dimension(s):** IC
- **Observation:** MNLI premises span ten genre sources including fiction and transcribed speech. The sampled examples include a slave-era dialect quote from fiction ([D11]: "Yes, Mistuh Reese, suh?"), casual American telephone speech ([D33]: "oh yeah no that's uh that's a that's a real interesting movie"), and first-person informal speech. These represent registers extremely distant from formal Luxembourgish administrative correspondence.
- **Deployment relevance:** A model whose NLI representations are partially trained on American vernacular dialogue and antebellum fiction dialects will have learned register-specific features that are unhelpful — and potentially counterproductive — for processing formal Luxembourgish administrative prose written in multiple languages.
- **Datapoint citations:**
  - [D11] mnli, split=train, label=neutral: "Yes, Mistuh Reese, suh?" / "THe slave spoke to Mr Reece." — Antebellum American fiction dialect; no relation to Luxembourgish administrative register
  - [D33] mnli, split=train, label=neutral: "oh yeah no that's uh that's a that's a real interesting movie and it's got a good historical perspective to it" — Transcribed American telephone speech; register opposite of formal administrative correspondence

#### MINOR

#### Concern 10: RTE includes some European content but labels entailment over news paraphrase, not administrative routing
- **Dimension(s):** IO, IC
- **Observation:** A few RTE examples touch European geography ([D35]: Budapest/Danube) and European economic history ([D19]: euro introduction). This is incidental — the task is binary textual entailment derived from news challenge datasets, not administrative classification. The European content does not correlate with Luxembourg-specific administrative topics.
- **Deployment relevance:** The presence of European-context news text in RTE might marginally reduce cultural distance compared to purely US-centric tasks, but this does not constitute meaningful coverage of Luxembourgish administrative domains. The task structure (news-based binary entailment) remains misaligned with the deployment.
- **Datapoint citations:**
  - [D19] rte, split=train, label=not_entailment: "National currencies will be completely replaced by the euro in within six months after the introduction of euro notes and coins." / "The introduction of the euro has been opposed." — European economic news; geographically proximate but task-irrelevant
  - [D35] rte, split=train, label=not_entailment: "Budapest consists of two parts, Buda and Pest, which are situated on opposite sides of the river and connected by a series of bridges." / "Buda is located on the west bank of the Danube." — European geography; not Luxembourgish administrative content

#### Concern 11: QQP contains non-English-speaking-country questions (India) without Luxembourgish coverage
- **Dimension(s):** IC
- **Observation:** The Quora QQP dataset is community-generated and includes questions from Indian users ([D16]: "What is the effect of black money on India's macro economy?"; [D18]: "Are the notes of Rs. 2000 really embedded with a GPS chip?"). This illustrates that even the "diverse" content in GLUE reflects specific online communities (Quora user base) rather than Luxembourgish civic concerns.
- **Deployment relevance:** The QQP content is doubly misaligned — it is neither English-administrative nor Luxembourgish. Its only relevance to the deployment assessment is as further evidence of the total absence of any Luxembourg-relevant content across all benchmark configs.
- **Datapoint citations:**
  - [D16] qqp, split=train, label=duplicate: "What is black money and how can it effect the economy of a country?" / "What is the effect of black money on India's macro economy?" — Indian economic policy question on Quora
  - [D18] qqp, split=train, label=duplicate: "Are the notes of Rs. 2000 really embedded with a GPS chip?" / "How does the embedded NGC technology of the Rs. 2000 note works?" — India-specific currency query

---

### Content Coverage Summary

The 409 sampled examples confirm without ambiguity the complete domain, language, and task mismatch described in the YAML documentation. The content is entirely English-language across all twelve configs, drawn from: (1) English movie review fragments (SST-2 — often sub-sentential and context-dependent); (2) English linguistics journal examples testing English morphosyntax (CoLA); (3) English news paraphrase pairs covering US political and financial news (MRPC); (4) Community Q&A pairs from Quora, skewed toward US and Indian-English topics (QQP); (5) Wikipedia-based QA targeting US and world historical/scientific knowledge (QNLI); (6) English news and Wikipedia textual entailment pairs with some European geography (RTE); (7) Image-caption similarity pairs describing everyday physical actions (STS-B); (8) English fiction-based pronoun coreference (WNLI); (9) Multi-genre English NLI pairs from transcribed speech, fiction, government reports, and travel guides (MNLI); and (10) A diagnostic NLI set drawing on academic NLP papers, news, Reddit, and Wikipedia, probing English syntactic and semantic phenomena.

No example references Luxembourg, Luxembourgish language, French administrative text, German-language content, cross-border worker status, national vs. communal government routing, or any topic from the required administrative taxonomy. Register is predominantly American English informal-to-journalistic; the formal continental European administrative register of Luxembourgish citizen correspondence is entirely unrepresented. The benchmark offers value only as a structural reference for benchmark suite design — its tasks, labels, content, and scoring paradigm do not transfer to the deployment.

---

### Limitations

1. **Sample size per config:** The sampling strategy retrieved 17–78 examples per config depending on class distribution in the buffer. For large configs (MNLI: 393k training examples; QQP: 364k training examples), the sampled examples represent a tiny fraction and may not capture the full topical range. It is possible, though unlikely given the documented source domains, that MNLI's "government report" source contains some European administrative content not represented in the sample.

2. **Test sets not inspectable:** Four configs use privately held test labels (cola, mnli, qqp, sst2). The analysis relied on training and validation splits; test set content distributions may differ marginally, though source domains are fixed and documented.

3. **ax config label anomaly:** The ax (diagnostic) config shows label=-1 for all 26 sampled examples, which is the test split. The documentation states test labels are privately held and the label field encodes -1 for masked test labels. This means all 26 ax examples are from the test split with masked ground truth — the cited labels (D21, D22, D23, etc.) are index-based class assignments, not verified ground truth, and should be interpreted accordingly. This does not affect the linguistic content observations but limits inference about the diagnostic label distribution from the sample.

4. **No audio or image modalities:** GLUE is text-only; this was confirmed by metadata and examples. No media columns were inspected or skipped.

5. **Code-switching and non-standard orthography not assessable from this dataset:** By definition, no Luxembourgish orthographic variation, trilingual code-switching, or non-standard spelling can be observed in a monolingual English dataset. The severity of the IF/IC gaps for the deployment can only be assessed by examining Luxembourgish-language resources (ltzGLUE, LuxBorrow, spellux) — none of which are present here.

