I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **LAILA: A Large-Scale Arabic Dataset for Automated Essay Scoring** is valid for use in **Arab High-School Arabic Essay Feedback (Qatar Primary)**.

Analyze the evidence sources below against each of the 6 validity dimensions. For each dimension, assign a score (1-5), provide justification with cited evidence, respond to each checklist item, and identify information gaps.

### Critical Constraints

- **Evidence-grounded only**: Base your analysis ONLY on the three evidence sources provided: (1) benchmark documentation with verbatim quotes, (2) regional context with web-sourced findings, and (3) dataset analysis findings with datapoint citations (if present). Do NOT role-play as a member of the target culture or speculate beyond what these sources support.
- **Cite evidence**: For each finding, cite at least one source — a verbatim quote `[QN]`, a web source `[WEB-N]`, or a dataset citation `DATASET-D{n}`.
- **Flag gaps explicitly**: When none of the three evidence sources addresses a checklist item, say "INSUFFICIENT DOCUMENTATION" and describe what would be needed.
- **Distinguish documentable vs. expert-needed**: Classify each finding as either (a) determinable from documentation, or (b) requiring regional expert verification.
- **Regional specificity**: Evaluate validity *for the specified target region*, not in general.
- **Conservative scoring**: When evidence is ambiguous or insufficient, score lower rather than higher.

### Scoring Rubric

- **1**: Major validity violations identified; benchmark component fundamentally misaligned with target context.
- **2**: Significant concerns; multiple concrete violations or gaps identified.
- **3**: Partially addressed; mixed evidence; some alignment, some gaps.
- **4**: Well addressed; minor concerns or gaps; documentation shows awareness of regional needs.
- **5**: Fully addressed; no concerns identified; documentation demonstrates explicit validity-preserving practices.

### Evidence Sources

The prompt below contains three evidence sources:

1. **Benchmark Documentation** + **Verbatim Quote Registry** — paper content, with authoritative quotes labeled `[QN]`
2. **Regional Context** (YAML) + **Web Source Registry** — deployment context with web research findings cited as `[WEB-N]`
3. **Dataset Analysis Findings** (if present) — empirical observations from the benchmark's HuggingFace data, cited as `DATASET-D{n}`

Citation rules for each source are in your system instructions.

---

## Benchmark Information

- **Name**: laila
- **Full Name**: LAILA: A Large-Scale Arabic Dataset for Automated Essay Scoring
- **Domain**: Automated Essay Scoring (AES) for Arabic high-school writing
- **Languages**: ar
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### 1. Input Ontology
LAILA's task taxonomy is organized around two experimental setups — prompt-specific
and cross-prompt — with research questions targeting overall model comparison and
per-trait performance [Q46]. The benchmark covers 8 prompts spanning only two genres:
3 explanatory and 5 persuasive [Q38]. The CAST rubric used was designed specifically
for persuasive/argumentative writing [Q118], meaning its construct is genre-specific
by design. The nine design principles guiding dataset construction include authenticity,
diversity, and gender balance [Q20], but none of the principles address genre breadth
beyond the explanatory/persuasive axis.

For the deployment scenario, this is a significant ontological gap: the benchmark
explicitly acknowledges that only explanatory and persuasive prompts are covered,
"limiting genre diversity and potentially affecting model robustness across other
styles, such as narrative or descriptive writing" [Q89]. Literary analysis, religious
text commentary, and cultural commentary — genres commonly found in Arab high-school
curricula — are entirely absent. The P1 and P5 explanatory prompts showed additional
interpretive instability, with higher frequencies of REL = 0 and annotator disagreement
attributed to the "greater flexibility in structure and content" characteristic of
explanatory tasks [Q125], further limiting the robustness of the genre-specific
construct even within its own stated scope.

Model evaluation covers three architectural families — feature-based (FB), encoder-based
(AraBERT, AraT5), and Arabic-centric LLMs — under both zero-shot and few-shot paradigms
[Q48, Q51], but the entire output task taxonomy is restricted to numeric trait scoring.
No model generates natural-language revision suggestions, making the benchmark structurally
misaligned with formative feedback applications.

### 2. Input Content
LAILA was collected from 24 Qatari high schools over one academic year through 27 school
visits, drawing essays from 4,372 students under exam-style supervised conditions [Q3, Q27].
Prompts were carefully designed to be "developmentally appropriate for the target age
groups, culturally relevant to the Arabic-speaking context, and free of sensitive topics"
[Q99], with gender balance deliberately pursued [Q23, Q100]. The dataset includes
3,446 explanatory and 4,413 persuasive essays [Q38], and essay lengths average 171 words
[Q133].

The most significant content validity concern for the deployment scenario is geographic
exclusivity: all essays originate from Qatar, grades 10–12 [Q88]. The authors acknowledge
that this "may limit its generalizability to other Arabic-speaking populations due to
diverse educational systems," offering only partial mitigation through Qatar's Arab
expatriate population [Q88]. No cross-national validation of content norms, rhetorical
conventions, or culturally inflected essay topics has been performed. Prompts were varied
across genres to promote cultural relevance and model generalization [Q22], but this
diversity is constrained within the single Qatari institutional ecosystem whose standards
— QUTC, Qatar Ministry of Education, local schools — define what counts as culturally
relevant content.

Two prompts (P3 and P4) also have fewer essays than others, potentially introducing
imbalance [Q90], and the average essay length of 171 words is notably short, restricting
assessment of models on extended academic writing [Q92]. LLM selection was guided by the
Open Arabic LLM Leaderboard [Q178], but the content relevance of that leaderboard's
evaluation corpus to the deployment's target student population is not documented.

### 3. Input Form
LAILA essays are text-only Arabic, written digitally on Microsoft Forms under a 65-minute
timed constraint [Q25, Q26]. The Latin-script mismatch concern does not apply; Arabic
script is the native encoding of the target languages. Essay length distributions show a
unimodal pattern centered at 171 words, concentrated between 150 and 180 words, with
very few essays exceeding 500 words [Q134, Q135]. Shorter essays (11–60 words, totaling
1,061) are also represented, with a minimum of 11 words following cleaning [Q136, Q137].

Model-specific input formats vary: AraT5 receives an instruction plus essay text [Q148];
AraBERT uses max-pooled token representations concatenated with 816 handcrafted features
[Q157]; ProTACT uses CNN/LSTM over POS embeddings with AraVec replacing GloVe [Q167];
MOOSE uses AraBERTv02 for tokenization and AraBERTv01 for scoring [Q173]; and LLMs
operate within a 4,096-token context limit [Q184]. The digital text-based format aligns
well with the deployment's text interaction model; there is no modality mismatch between
benchmark and deployment.

### 4. Output Ontology
LAILA's output schema is built on 7 writing traits — REL, ORG, VOC, STY, DEV, MEC, GRA —
grounded in the CAST rubric from QUTC [Q33, Q34]. Six traits use a 6-point scale (0–5);
REL uses a 3-point scale (0–2) [Q36]. A special rule sets all trait scores to 0 when
REL = 0 [Q37], and a score of 0 also covers below-minimum performance or off-topic
content [Q117]. The CAST rubric is explicitly designed for persuasive/argumentative
writing [Q118], meaning the output ontology — the construct being scored — has a
genre-specific scope.

For the deployment scenario, the critical output ontology misalignment is that the
benchmark validates numeric ordinal scoring exclusively. All benchmarked models "followed
a multitask setup predicting holistic and trait scores jointly" [Q48]; LLMs were tasked
with "generating trait scores in JSON format" [Q181]; AraT5 formulates AES "as a text
generation problem, where the model predicts the trait scores sequentially" [Q147]. There
is no label category in LAILA for revision suggestions, explanation quality, or
pedagogical actionability. The deployment requires models to generate actionable
natural-language explanations for why students lost points — a qualitatively different
output function that the benchmark's scoring taxonomy was not designed to validate.
The narrow REL scale (0–2) further limits ontological granularity, and QWK may
"underrepresent subtle differences in model predictions" on this trait [Q91].

### 5. Output Content
The annotation team comprised 6 annotators and 3 supervisors, all Arabic language
teachers or lecturers, with five holding advanced degrees in the Arabic language [Q30, Q31].
The CAST rubric, provided in Arabic by QUTC [Q114], anchors the annotation in Qatar-specific
institutional standards. Annotation was conducted on the Assessment Gourmet Platform with
annotator blindness to student identity [Q42]. Guidelines were developed by 2 supervisors
and included terminology, exemplars, and annotated practices per prompt type [Q41], with
structured training and moderation sessions before formal annotation [Q102].

Inter-annotator agreement (QWK) was substantial across prompts, averaging 0.66 (P5) to
0.75 (P1) [Q44]. However, P5 showed the lowest agreement and the highest rate of third-
annotator adjudication (23.3%), suggesting interpretive instability on explanatory prompts
[Q45]. The annotation ecosystem is entirely Qatar-institutional: funders (QRDI), rubric
developers (QUTC), annotators, and schools are all within Qatar [Q84, Q85, Q86]. No
cross-national validation of annotation norms has been performed. For deployment across
Egypt, Saudi Arabia, Jordan, Lebanon, and other Arab countries, it is unknown whether
LAILA's labels — particularly for subjective traits like STY and DEV — reflect
broadly shared teacher judgment norms or Qatar-specific institutional conventions.

### 6. Output Form
The benchmark evaluates all models using Quadratic Weighted Kappa (QWK) to measure
agreement between human and model numeric scores [Q58], with Bayesian hyperparameter
optimization [Q59, Q60] and final model selection based on average QWK on the development
set [Q61]. LLM outputs are enforced in JSON format via the outlines library [Q190], and
LLM experiments were repeated three times with different random seeds [Q189]. Holistic
score was computed as the sum of trait scores for LLM experiments [Q182].

The output form mismatch for the deployment is direct and documented: LAILA's output
form is structured numeric scores (and structured JSON equivalents), while the deployment
requires open-ended natural-language revision suggestions and explanations. QWK measures
alignment between model and human numeric scores; it cannot capture whether model outputs
would be pedagogically useful as formative feedback. The benchmark explicitly prohibits
use for "high-stakes educational decisions affecting individual students" [Q104] and
recommends "fairness auditing and stakeholder consultation before real-world application"
[Q106], indicating that the authors themselves do not consider the current output form
sufficient for operational deployment.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "LAILA, the largest publicly available Arabic AES dataset to date, comprising 7,859 essays annotated with holistic and trait-specific scores on seven dimensions: relevance, organization, vocabulary, style, development, mechanics, and grammar." |
| Q2 | 1 | input_content | "The dataset comprises 7,859 essays across 8 distinct prompts making it the most extensive publicly available Arabic resource of its kind." |
| Q3 | 1 | input_content | "Under Institutional Review Board (IRB) approval, we visited 24 high schools in Qatar and collected essays directly from 4,372 students in authentic classroom settings." |
| Q4 | 1 | output_ontology | "Table 1: Brief description of the traits in LAILA." |
| Q5 | 1 | output_content | "Trait-Specific Annotations: We provide de-" |
| Q6 | 1 | output_content | "Annotation Guidelines: We develop and share comprehensive guidelines for data annotation to ensure transparency and reproducibility." |
| Q7 | 1 | output_content | "May Bashendy, Walid Massoud, Sohaila Eltanbouly, Salam Albatarni, Marwan Sayed, Abrar Abir, Houda Bouamor, Tamer Elsayed." |
| Q8 | 1 | output_content | "Computer Science and Engineering Department, Qatar University and Carnegie Mellon University in Qatar." |
| Q9 | 1 | output_content | "IRB Number: QU-IRB 159/2024-EA" |
| Q10 | 1 | input_content | "Arabic AES research faces a significant data scarcity problem, as publicly available annotated datasets remain limited." |
| Q11 | 1 | input_content | "Existing Arabic resources are often small in scale such as QAES (Bashendy et al., 2024), lack trait-specific annotations as in ZAEBAC (Habash and Palfreyman, 2022), or consist solely of unannotated essays such as ALC." |
| Q12 | 2 | input_form | "Table 2: Comparison of LAILA with existing essay datasets. "Len" is average essay length in words; "HOL" indicates holistic scoring; "Eur" covers German, Italian, and Czech; "L1/L2" denotes native or second-language learners; "Public" here means freely available." |
| Q13 | 2 | output_ontology | "tailed trait-specific annotations that capture multiple dimensions of writing proficiency." |
| Q14 | 2 | input_ontology | "We establish baseline AES results for Arabic under two evaluation setups: prompt-specific and cross-prompt." |
| Q15 | 2 | output_form | "We publicly release LAILA, including essays with holistic and trait-specific annotations. We also release the benchmarking code to support replication and future research." |
| Q16 | 2 | input_content | "Section 2 reviews related work and existing AES datasets. Section 3 outlines the data collection design principles, while Section 4 describes the dataset construction process, including school and prompt selection, essay collection, and annotations." |
| Q17 | 2 | input_content | "Research on AES has advanced considerably in English, supported by large-scale, publicly available datasets such as ASAP/ASAP++ (Mathias and Bhattacharyya, 2018), TOEFL11 (Blanchard et al., 2013), ELLIPSE (Crossley et al., 2023a), and PERSUADE (Crossley et al., 2023b)." |
| Q18 | 2 | input_content | "In contrast, other languages have far fewer resources. Some smaller datasets exist, including ACEA (Chinese; annotated but not public) (He et al., 2022), TCFLE-8 (French; public but with only holistic scores) (Wilkens et al., 2023), and MERLIN (German, Italian, and Czech; public but limited to holistic annotations) (Boyd et al., 2014). While useful for AES studies, their limited scale and annotation depth restrict their utility." |
| Q19 | 2 | input_content | "Compared with English and other languages, Arabic AES lacks robust datasets. Few datasets have been developed, both public and proprietary, yet all face limitations in scale, annotation depth, or accessibility." |
| Q20 | 3 | input_ontology | "The development of LAILA was guided by nine core design principles [D1–D9], each reflecting deliberate choices to ensure a high-quality, representative, and ethically sound resource for Arabic AES." |
| Q21 | 3 | input_content | "[D1] Ensuring Data Integrity: We designed LAILA to capture authentic, classroom-produced writing created without external assistance. This design choice preserves genuine linguistic variation, learner errors, and authentic complexities essential for real-world AES applications." |
| Q22 | 3 | input_content | "[D2] Maximizing Diversity: To reflect the breadth of Arabic writing proficiency, LAILA was planned to collect essays from multiple educational institutions and student populations with diverse academic and demographic backgrounds. Prompts were intentionally varied across genres, ensuring cultural relevance and age appropriateness, thereby promoting model generalization and reducing bias." |
| Q23 | 3 | input_content | "[D3] Achieving Gender Balance: We intentionally aimed to balance the number of essays from male and female students to promote fairness, reduce gender-based bias, support inclusive evaluation, and enhance model generalization." |
| Q24 | 3 | output_ontology | "[D4] Supporting Full Trait Coverage: LAILA was built to capture multiple dimensions of writing quality through annotations of relevance, organization, vocabulary, style, development, mechanics, and grammar. This design supports fine-grained assessment and meaningful feedback." |
| Q25 | 3 | input_form | "[D5] Ensuring Authentic Writing Conditions: To emulate real academic or high-stakes testing scenarios, LAILA was designed to collect essays written under timed conditions using a digital submission platform. This setup ensures consis" |
| Q26 | 5 | input_form | "taining one persuasive and one explanatory prompt, along with a unique, pre-generated ID to maintain students' anonymity while enabling metadata tracking [D6]. We also configured a Microsoft Form for digital essay submission, set with a 65-minute time limit to enforce a time-restricted setup [D5]." |
| Q27 | 5 | input_content | "Data collection spanned one academic year through 27 school visits (24 initial, three follow-ups), by nine team members, to meet the target student count." |
| Q28 | 5 | input_content | "Each visit, which lasted around six hours, was supported by at least two team members, an IT teacher, and proctoring teachers." |
| Q29 | 5 | input_form | "The collected essays then underwent a cleaning process to ensure data quality before the annotation phase. First, we resolved duplicate and misidentified submissions, by correcting ID mismatches through manual verification and name cross-referencing. Next, a manual review eliminated submissions lacking meaningful content, e.g., irrelevant personal content. Lastly, essays with 10 or fewer words were excluded for being insufficient for AES analysis." |
| Q30 | 5 | output_content | "The hired annotation team consisted of 6 annotators and 3 supervisors, all of whom were Arabic language teachers or lecturers with educational backgrounds." |
| Q31 | 5 | output_content | "Five members of the team hold advanced degrees (MSc or PhD) in the Arabic language." |
| Q32 | 5 | output_content | "The supervisors oversaw training, quality assurance, and dispute resolution, while the annotators performed the primary scoring tasks." |
| Q33 | 5 | output_ontology | "All essays in LAILA dataset were scored using the Core Academic Skills Test (CAST) rubric [D7], developed by the Qatar University Testing Center (QUTC)." |
| Q34 | 5 | output_ontology | "The rubric covers 7 writing traits [D4]: Relevance (REL), Organization (ORG), Vocabulary (VOC), Style (STY), Development (DEV), Mechanics (MEC), and Grammar (GRA)." |
| Q35 | 5 | output_ontology | "Additionally, a Holistic score (HOL) was computed as the sum of the 7 trait scores." |
| Q36 | 5 | output_ontology | "Six traits (all but REL) were rated on a 6-point scale (0 = lowest, 5 = highest), while REL was rated on a 3-point scale (0 = not relevant, 1 = partially relevant, and 2 = fully relevant)." |
| Q37 | 5 | output_ontology | "Furthermore, if an essay received a REL score of 0, all other trait scores were set to 0, as irrelevant responses are not subject to further evaluation." |
| Q38 | 6 | input_ontology | "LAILA comprises 7,859 essays collected across 8 distinct prompts: 3 explanatory and 5 persuasive (3,446 and 4,413 essays, respectively)." |
| Q39 | 6 | input_form | "Table 3 shows that the number of essays per prompt ranges from 500 to 1,181. Essay lengths demonstrate consistency across prompts, with an average of 171 words and a maximum of 706 words." |
| Q40 | 6 | output_ontology | "Most traits follow a near-normal pattern on the 6-point scale, indicating overall positive essay quality. The REL scores show that 86% of the essays agree strongly with the prompt. In contrast, GRA and VOC show the highest percentage of score 1 at 16%, followed by MEC at 13%, highlighting that these traits pose the greatest challenges." |
| Q41 | 6 | output_content | "To ensure consistency, 2 supervisors developed an annotation guidebook with detailed terminology, exemplars, and annotated practices for each prompt type. Annotators were required to review these materials and complete training sessions before formal annotation. Moderation sessions followed, where discrepancies were discussed and interpretations of the rubric were harmonized." |
| Q42 | 6 | output_content | "The scoring process was conducted using the Assessment Gourmet Platform, which supports large-scale, anonymized essay scoring. The platform ensured that annotators were blinded to student identity [D6], while only supervisors had access to annotator metadata for monitoring purposes." |
| Q43 | 6 | output_content | "The essays were randomly distributed among the annotators to minimize systematic bias, and the scoring sessions were capped to prevent annotators' fatigue. Each essay was independently scored by two annotators across all traits. If the difference in HOL scores between the two annotators was less than 6 points, the mean of the two scores was computed and then rounded down to the nearest integer; this rounded value was adopted as the final score for each trait. However, essays with large discrepancies between annotators (≥ 6 points difference in the HOL score) were flagged and escalated to a supervisor (a third annotator in this case), who provided the final adjudicated score and offered feedback to the annotators to improve alignment and consistency in subsequent batches of essays." |
| Q44 | 6 | output_content | "We compute IAA using Quadratic Weighted Kappa (QWK) (Williamson et al., 2012) to assess agreement between the two main annotators (A1 and A2), prior to adjudication. Table 4 reports QWK per trait and prompt, with agreement strength following Landis and Koch (1977). Overall, IAA was substantial across prompts, with an average QWK ranging from 0.66 (P5) to 0.75 (P1), showing strong consistency." |
| Q45 | 6 | output_content | "However, variability emerges by prompt and trait. In particular, P5 showed the lowest average agreement, noting that it has the highest percentage of essays that require a third annotator (A3: 23.3%; Table 3). This suggests greater initial disagreement" |
| Q46 | 7 | input_ontology | "For each setup, we investigate two research questions in the context of Arabic AES: (RQ1) how do different categories of models compare in overall performance?, and (RQ2) which models achieve the best results across individual traits?." |
| Q47 | 7 | input_ontology | "Model Selection We selected a diverse set of models with varying architectures to establish strong baselines for LAILA. The selection criteria included code availability, ease of implementation, and coverage of SOTA Arabic and English models." |
| Q48 | 7 | output_ontology | "The models fall into three categories: feature-based (FB), encoder-based, and large language models (LLMs). LLMs were evaluated in zero-shot and few-shot settings, and all models followed a multitask setup predicting holistic and trait scores jointly." |
| Q49 | 7 | input_ontology | "We selected 4 FB models: Linear Regression (LR), Random Forest (RF), Extreme Gradient Boosting (XGB), and a feedforward Neural Network (NN)." |
| Q50 | 7 | input_ontology | "For encoder-based models, we fine-tuned two pre-trained SOTA systems: AraBERT (Antoun et al., 2020), combined with handcrafted features (Sayed et al., 2025), and AraT5 (Nagoudi et al., 2022), inspired by the strong performance of T5 in English AES (Do et al., 2024)." |
| Q51 | 7 | input_ontology | "For LLMs, we evaluated three Arabic-centric models: ALLaM (Bari et al., 2025), Command-R7B-Arabic (R7B) (Alnumay et al., 2025), and Fanar (Team et al., 2025), under zero-shot and few-shot (5-shot) settings." |
| Q52 | 7 | output_form | "For the prompt-specific experiments, we used 5-fold cross-validation using the predefined 5 splits. In each cross-validation iteration, one fold (20%) was used as the test set, and the remaining four folds were further split into training (70%) and development (10%) sets, with stratification applied to maintain consistent prompt distributions and ensure consistent evaluation across models." |
| Q53 | 7 | input_ontology | "For encoder-based models, we employ the same AraBERT-based architecture, which performed strongly in Arabic AES (Sayed et al., 2025), along with two SOTA English AES models, ProTACT (Do et al., 2023) and MOOSE (Chen et al., 2025)." |
| Q54 | 8 | input_form | "We implemented the 816 handcrafted features introduced by Sayed et al. (2025) for Arabic AES, encompassing surface, readability, lexical, semantic, and syntactic aspects." |
| Q55 | 8 | input_form | "These features were applied to the FB models, ProTACT, MOOSE, and AraBERT." |
| Q56 | 8 | input_form | "To mitigate noise, we performed feature selection based on Pearson and Spearman correlations (Li and Ng, 2024), retaining features whose absolute correlation with any trait exceeded a predefined threshold for either metric." |
| Q57 | 8 | input_form | "For MOOSE, however, we did not apply this explicit feature selection step." |
| Q58 | 8 | output_form | "We evaluate model performance using QWK to measure agreement between human and model scores." |
| Q59 | 8 | output_form | "Hyperparameters are tuned via Bayesian optimization with the Tree-structured Parzen Estimator algorithm (Bergstra et al., 2011), implemented using Optuna's TPESampler." |
| Q60 | 8 | output_form | "We ran 20 trials with 5 startup trials and a fixed random seed of 11." |
| Q61 | 8 | output_form | "The best configuration, selected based on average QWK on the development set, was used for final evaluation on the test data." |
| Q62 | 9 | output_form | "FB models showed comparable performance, with only a 2-point difference between the top performer (XGB) and the lowest (NN), highlighting consistency of these feature-based approaches." |
| Q63 | 9 | output_form | "Among encoder-based models, ProTACT exhibited the lowest performance overall, suggesting limited transferability from its English architecture, while AraBERT trailed XGB by 4.4 points." |
| Q64 | 9 | output_form | "Notably, MOOSE achieved the highest performance among all evaluated cross-prompt models." |
| Q65 | 9 | output_form | "For LLMs, few-shot prompting improved Fanar and R7B (+19 and +11.6 points), whereas ALLaM dropped by 7 points, indicating high sensitivity to prompt design." |
| Q66 | 9 | output_form | "No single model consistently outperformed the others across individual traits." |
| Q67 | 9 | output_form | "MOOSE performed best in REL, STY, and GRA traits." |
| Q68 | 9 | output_form | "For the remaining traits, RF led in VOC and HOL, XGB in ORG, and Fanar (5) in DEV and MEC." |
| Q69 | 9 | output_form | "Encoder-based models excel in prompt-specific tasks, approaching the IAA (Table 4), which indicates a close reach to the human performance." |
| Q70 | 9 | output_form | "AraBERT exhibits the best performance overall in the prompt-specific setup with an average QWK performance of 0.74." |
| Q71 | 9 | output_form | "However, its cross-prompt performance drops significantly (average QWK: 0.549), underscoring its ability to capture prompt-dependent patterns rather than generalizable features." |
| Q72 | 9 | input_ontology | "We note that the applicability of the prompt-specific setup is relatively limited due to reliance on target prompt essays that are labeled, which is often unavailable in practice." |
| Q73 | 9 | output_form | "In the cross-prompt setup, while MOOSE achieves the highest average performance (average QWK: 0.597), we observe that classical FB models (XGB) remain remarkably competitive." |
| Q74 | 9 | output_form | "This confirms that handcrafted features capture prompt-independent linguistic properties that generalize better in the more challenging and realistic cross-prompt setup than some standard encoders." |
| Q75 | 9 | output_form | "LLMs, specifically Fanar and R7B with few shots, exhibit consistent performance across both setups, indicating they capture general scoring criteria." |
| Q76 | 9 | output_form | "Their relative underperformance in prompt-specific tasks reflects their limited ability to exploit prompt-dependent patterns without fine-tuning." |
| Q77 | 9 | input_ontology | "Overall, the findings of the benchmarking experiments above highlight the need to prioritize future research on cross-prompt AES, which is practically closer to the real world, while best models are still far from human performance." |
| Q78 | 9 | input_content | "While research on automated scoring of English essays began more than 55 years ago, Arabic essay scoring is hindered by the lack of data resources." |
| Q79 | 9 | input_content | "To bridge this gap, this paper introduced LAILA, the first large-scale publicly available dataset for Arabic AES." |
| Q80 | 9 | input_content | "The dataset comprises 7,859 essays written on 8 different prompts by 4,372 high school students, and provides annotations for 7 writing traits as well as a holistic score with substantial inter-annotator agreement." |
| Q81 | 9 | input_content | "This makes it a comprehensive and reliable resource for training models and evaluating writing quality of Arabic essays." |
| Q82 | 9 | output_content | "For reproducibility, we detailed the data collection and annotation process." |
| Q83 | 9 | output_form | "We also benchmarked LAILA using SOTA Arabic and English AES models in both prompt-specific and cross-prompt settings, showing strong baselines for future research." |
| Q84 | 9 | output_content | "We heartily thank our dedicated annotators for their contributions and express our gratitude to Qatar University Testing Center, the Ministry of Education and Higher Education in Qatar (the Arabic Section of the Department Of Educational Supervision in particular), participating schools, and students for making this work possible." |
| Q85 | 9 | output_content | "We also acknowledge the support of Advanced Group for Information Technology (AGI) for providing access to the platform, Assessment Gourmet, which was used to manage and administer the annotation process." |
| Q86 | 9 | output_content | "This work was made possible by NPRP grant NPRP14S-0402-210127 from the Qatar Research Development and Innovation (QRDI) Council." |
| Q87 | 9 | input_content | "While LAILA represents a significant step forward for Arabic AES, it has notable limitations." |
| Q88 | 9 | input_content | "First, LAILA was collected from students in a single country, Qatar, and specific grade levels, grades 10 to 12, which may limit its generalizability to other Arabic-speaking populations due to diverse educational systems. However, this concern is partially mitigated by Qatar's large population of Arab expatriates, resulting in student participants representing a wide variety of Arabic dialects and backgrounds." |
| Q89 | 10 | input_ontology | "Second, LAILA includes only explanatory and persuasive writing prompts, limiting genre diversity and potentially affecting model robustness across other styles, such as narrative or descriptive writing." |
| Q90 | 10 | input_content | "Third, two of the prompts (Prompts 3 and 4) have fewer essays than the rest, which could introduce imbalance and lead to skewed performance in prompt-specific evaluations." |
| Q91 | 10 | output_ontology | "Fourth, the relevance trait is scored on a narrow scale from 0 to 2, which limits the granularity of evaluation and may cause QWK to underrepresent subtle differences in model predictions." |
| Q92 | 10 | input_form | "Fifth, with an average essay length of only 171 words, the dataset lacks extended writing samples, restricting the assessment of models on long-form academic tasks requiring more complex, extended compositions." |
| Q93 | 10 | output_form | "Finally, we acknowledge that the experimental results reported in Table 5 do not aim to exhaustively benchmark state-of-the-art AES models; rather, they serve as baseline performance for LAILA." |
| Q94 | 10 | input_content | "We emphasize that the primary contribution of this work lies in the construction and public release of a large-scale Arabic AES dataset, rather than in proposing novel AES model architectures." |
| Q95 | 10 | output_content | "The collection of LAILA received approval from an Institutional Review Board (IRB Number: QU-IRB 159/2024-EA) and was conducted with informed consent from both students and their legal guardians." |
| Q96 | 10 | input_content | "Essays were written under exam-style supervised conditions, with participation entirely voluntary and independent of students' academic evaluations or grades." |
| Q97 | 10 | input_form | "To protect participant privacy, all submissions were assigned pre-generated anonymous identifiers, and personally identifiable information was systematically removed during data cleaning." |
| Q98 | 10 | output_content | "Annotation was conducted on a platform that prevented annotators from accessing student identities or demographic information." |
| Q99 | 10 | input_content | "Essay prompts were carefully designed to be developmentally appropriate for the target age groups, culturally relevant to the Arabic-speaking context, and free of sensitive topics or potentially harmful content." |
| Q100 | 10 | input_content | "The dataset includes balanced gender representation and covers grades 10-12." |
| Q101 | 10 | output_content | "All annotators were qualified Arabic language educators who received fair compensation at or above local professional rates." |
| Q102 | 10 | output_content | "They completed structured training on annotation guidelines, and inter-annotator disagreements were resolved through systematic adjudication procedures." |
| Q103 | 10 | output_form | "The dataset will be released exclusively for research and educational purposes in Arabic automated essay scoring." |
| Q104 | 10 | output_form | "We explicitly prohibit its use for high-stakes educational decisions affecting individual students." |
| Q105 | 10 | output_form | "Users must commit to: (1) preventing re-identification attempts, (2) avoiding demographic profiling or inference, and (3) refraining from deployment in operational assessment contexts without independent validation." |
| Q106 | 10 | output_form | "We recommend that any system developed using LAILA undergo fairness auditing and stakeholder consultation before real-world application." |
| Q107 | 11 | input_ontology | "TAQEEM 2025: Overview of the first shared task for Arabic quality evaluation of essays in multi-dimensions." |
| Q108 | 11 | output_ontology | "QAES: First publicly-available trait-specific annotations for automated scoring of Arabic essays." |
| Q109 | 11 | input_content | "ZaQQ: A new Arabic dataset for automatic essay scoring via a novel human–ai collaborative framework." |
| Q110 | 11 | input_content | "The English language learner insight, proficiency and skills evaluation (ELLIPSE) corpus." |
| Q111 | 11 | input_content | "A large-scale corpus for assessing written argumentation: PERSUADE 2.0." |
| Q112 | 11 | input_content | "The MERLIN corpus: Learner language and the CEFR." |
| Q113 | 11 | input_content | "TOEFL11: A corpus of non-native English." |
| Q114 | 12 | output_content | "For annotating LAILA, we adopted the rubric from the Core Academic Skills Test (CAST), which is provided in Arabic, developed by the Qatar University Testing Center (QUTC)." |
| Q115 | 12 | output_ontology | "This rubric guided scoring across 7 writing traits: relevance (REL), organization (ORG), vocabulary (VOC), style (STY), development (DEV), mechanics (MEC), and grammar (GRA)." |
| Q116 | 12 | output_ontology | "An English-translated version of the CAST rubric is presented in Table 6." |
| Q117 | 13 | output_ontology | "Note: A score of 0 is assigned if the student does not attempt the task, provides a response that falls below the performance level described for score 1, or submits content that is not relevant to the topic of the given prompt." |
| Q118 | 13 | input_ontology | "Table 6: CAST Persuasive/Argumentative Writing Rubric - English Translation (Bashendy et al., 2024)." |
| Q119 | 14 | output_ontology | "Figure 4 presents the score distributions in LAILA across 8 distinct prompts (P1–P8) and 7 writing traits, including Relevance (REL), Organization (ORG), Vocabulary (VOC), Style (STY), Development (DEV), Mechanics (MEC), and Grammar (GRA), alongside a Holistic (HOL) score representing the sum of all individual traits." |
| Q120 | 14 | output_ontology | "All traits are rated on a scale of 0–5, except REL, which ranges from 0–2." |
| Q121 | 14 | output_form | "Overall, most traits approximate a normal distribution with comparable patterns across prompts, suggesting that essays' quality remains relatively stable regardless of the prompt topic." |
| Q122 | 14 | output_content | "However, variations emerge by prompt and trait." |
| Q123 | 14 | output_ontology | "For REL, distributions are consistently skewed toward score 2 (the highest) across all prompts, indicating that most students successfully addressed the assigned task and produced strongly relevant essays." |
| Q124 | 14 | input_content | "However, P1 and P5 display relatively higher frequencies at score 0, compared to other prompts, suggesting potential ambiguity in prompt wording that may have limited clear interpretation." |
| Q125 | 14 | input_ontology | "Notably, both P1 and P5 are explanatory prompts, which often allow greater flexibility in structure and content." |
| Q126 | 14 | input_content | "This openness may have led to varied interpretations among students and inconsistencies in alignment with the intended prompt focus." |
| Q127 | 14 | output_form | "The distribution of ORG scores varies across prompts but consistently peaks at score 3." |
| Q128 | 14 | output_form | "P2 exhibits a pronounced peak at 3, whereas P3 and P4 show a wider spread toward lower scores, suggesting a weaker organizational structure in these essays." |
| Q129 | 14 | output_form | "P5 and P6 display nearly identical, perfectly bell-shaped distributions, while P7 and P8 are skewed toward higher scores, reflecting stronger organization." |
| Q130 | 14 | output_form | "Similarly, the VOC and STY traits generally follow comparable patterns, clustering around scores 2–3 with a common peak at 3, indicating that these dimensions present moderate challenges for most students." |
| Q131 | 14 | output_form | "The DEV, MEC, and GRA traits exhibit broadly comparable distributions across all prompts, though with subtle variations." |
| Q132 | 14 | output_form | "The DEV trait shows distinct peaks at scores 2, 3, and 4, suggesting that" |
| Q133 | 15 | input_form | "Figure 5 presents the distribution of essay lengths (in words) across all prompts in LAILA dataset, which contains a total of 7,859 essays." |
| Q134 | 15 | input_form | "The data exhibits a unimodal pattern centered around an average essay length of 171 words, with the majority of essays concentrated between 90 and 210 words." |
| Q135 | 15 | input_form | "A pronounced peak occurs in the 150 to 180 word range, where the count reaches its highest at 1,065 essays." |
| Q136 | 15 | input_form | "Shorter essays are also represented, with 1,061 essays falling between 11 and 60 words." |
| Q137 | 15 | input_form | "Notably, the minimum observed length is 11 words, which results from the data cleaning step that excluded essays containing 10 words or fewer." |
| Q138 | 15 | input_form | "Beyond 420 words, the frequency drops sharply, with only a few essays exceeding 500 words, suggesting that longer essays are less common in the dataset." |
| Q139 | 15 | output_form | "In this section, we provide all the details of implementation and hyperparameter tuning for all the models used in the benchmarking experiments." |
| Q140 | 15 | output_form | "All experiments were conducted on two machines: one equipped with an NVIDIA RTX A6000 GPU, and another with two NVIDIA A10 GPUs." |
| Q141 | 15 | output_form | "For the feature-based (FB) models, the architectures and hyperparameter configurations were kept consistent across both the prompt-specific and cross-prompt setups." |
| Q142 | 15 | output_form | "We used the sklearn library for Linear Regression (LR) and Random Forest (RF) models, and the XGBoost library for the Extreme Gradient Boosting (XGB) model." |
| Q143 | 15 | output_form | "The Neural Network (NN) model followed the architecture described by Li and Ng (2024), consisting of two hidden layers with ReLU activations and a sigmoid output layer, implemented in PyTorch." |
| Q144 | 15 | output_form | "For the NN, the number of epochs was fixed at 50 with early stopping, setting patience to 7, and checkpointing the best epoch during hyperparameter tuning for final model training." |
| Q145 | 15 | output_form | "For all the FB models, feature selection was performed on the training set during hyperparameter tuning, with threshold values of [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], where 0 corresponds to using all features." |
| Q146 | 16 | input_ontology | "Motivated by the strong performance of the T5 model in prompt-specific English AES, we finetuned the AraT5 model using a similar setup to the ArTS model (Do et al., 2024)." |
| Q147 | 16 | output_ontology | "The AES task is formulated as a text generation problem, where the model predicts the trait scores sequentially." |
| Q148 | 16 | input_form | "The input to the model consisted of an instruction to score the essay along with the essay text, and the model was fine-tuned to generate the trait names followed by their corresponding scores." |
| Q149 | 16 | input_form | "The prediction order of the traits was aligned with the rubric to reflect the scoring order followed by human annotators." |
| Q150 | 16 | input_form | "Our setup differs from ArTS in data splitting: while their training and testing data included essays from all prompts (with a single model trained on all prompts), we adopted the conventional prompt-specific setup, training a separate model for each prompt using our predefined dataset splits." |
| Q151 | 16 | output_form | "For training, we used Seq2SeqTrainer from the transformers library." |
| Q152 | 16 | output_form | "For hyperparameter tuning, we explored the learning rates in the range [5e-5, 1e-4, 2e-4]." |
| Q153 | 16 | output_form | "Other hyperparameters followed the configuration of (Do et al., 2024), with a batch size of 4 and a maximum of 15 epochs." |
| Q154 | 16 | output_form | "Early stopping was applied based on the average QWK score on the development set." |
| Q155 | 16 | input_ontology | "AraBERT is used as a baseline for the prompt-specific and cross-prompt setups using the same architecture and hyperparameter search space." |
| Q156 | 16 | input_form | "The model is fine-tuned with a custom regression head and combined with handcrafted features for trait scoring." |
| Q157 | 16 | input_form | "The essay and prompt were provided as input to the encoder, with the max-pooled token representation concatenated with the handcrafted features." |
| Q158 | 16 | input_form | "The resulting vector was then fed into eight parallel regression heads, each corresponding" |
| Q159 | 17 | output_form | "Sigmoid activation is used at the output layer to produce values in the range [0, 1], which were subsequently rescaled to the appropriate range for each trait." |
| Q160 | 17 | output_form | "For hyperparameter tuning, the learning rates for the encoder layers and the regression head are tuned separately to better accommodate the larger dataset, with a weight decay of 0.01." |
| Q161 | 17 | output_form | "In addition, we tuned the number of trainable layers, with values of [2, 4, 8, all], where 'all' corresponds to training all encoder layers." |
| Q162 | 17 | output_form | "For the feature selection threshold, we used the same search space as that used with the FB models." |
| Q163 | 17 | input_form | "These configurations were considered better suited to the dataset, mitigating training instabilities." |
| Q164 | 17 | input_ontology | "For ProTACT, we used the official implementation released by the authors." |
| Q165 | 17 | input_form | "Essay representations were constructed using CNNs and LSTMs over Part-of-speech (POS) embeddings, while prompt representations combined POS and pre-trained GloVe embeddings." |
| Q166 | 17 | input_form | "A multi-head attention mechanism was applied to obtain prompt-aware essay representations, which were then concatenated with handcrafted features and passed through a linear layer for scoring." |
| Q167 | 17 | input_form | "The architecture was adapted for Arabic by replacing GloVe with AraVec embeddings (Mohammad et al., 2017)." |
| Q168 | 17 | input_form | "POS embeddings were extracted using Camel Tools." |
| Q169 | 17 | output_form | "For hyperparameter tuning, we adopted the same search spaces for learning rate and feature selection threshold as in the NN model, while additionally tuning the trait similarity loss threshold." |
| Q170 | 17 | output_form | "All other parameters were kept consistent with those reported in the original study, including embedding dimension, maximum essay length, maximum prompt length, LSTM units, self-attention heads, CNN filters, and kernel size." |
| Q171 | 17 | input_ontology | "For MOOSE, we used the official implementation released by the authors." |
| Q172 | 17 | input_form | "The architecture was adapted for Arabic by replacing BERT with AraBERT (Antoun et al., 2020)." |
| Q173 | 17 | input_form | "Specifically, in the preprocessing stage, AraBERTv02 was used only for tokenization and input encoding, while the finetuned model for the scoring task used AraBERTv01." |
| Q174 | 17 | output_form | "This design choice was guided by empirical validation: we experimented with using AraBERTv01 and AraBERTv02 consistently for both preprocessing and modeling, as well as with mixed configurations, and found that using AraBERTv02 for tokenization and input encoding while finetuning AraBERTv01 for scoring yielded the best performance on the development set, thus it was adopted." |
| Q175 | 17 | input_form | "For the incorporated features, We implemented the handcrafted features introduced by Sayed et al. (2025) for Arabic AES, without applying any feature selection step." |
| Q176 | 17 | output_form | "For hyperparameter tuning, the learning rate was tuned over the values 1e-4 and 2e-5, while all other parameters were kept consistent with those reported in the original study." |
| Q177 | 17 | output_form | "Training was performed with a batch size of 8 for a maximum of 14 epochs, and no early stopping was applied." |
| Q178 | 17 | input_content | "The selection of the LLMs was based on the Open Arabic LLM Leaderboard, where we selected" |
| Q179 | 18 | input_ontology | "The selected models are: Fanar, Command R7B Arabic, and ALLaM." |
| Q180 | 18 | input_ontology | "We evaluated the models under zero-shot and few-shot prompting." |
| Q181 | 18 | output_ontology | "In the zero-shot setting, the LLM is tasked with generating trait scores in JSON format, given the prompt text, essay, and trait rubrics." |
| Q182 | 18 | output_ontology | "The holistic score was computed as the sum of the individual trait scores." |
| Q183 | 18 | input_ontology | "In the few-shot setting, the rubric was omitted, as the meaning of the scores could be inferred from the examples." |
| Q184 | 18 | input_form | "The number of examples was fixed to 5, balancing scoring context with the context length limit (4096 tokens)." |
| Q185 | 18 | input_form | "When a prompt exceeded this limit, we iteratively removed examples until it fit." |
| Q186 | 18 | input_form | "Although Command-R7B supports a larger context length, we fixed the number of examples to 5 to ensure fair comparison across LLMs." |
| Q187 | 18 | input_ontology | "In the prompt-specific setup, few-shot examples are selected from the same prompt." |
| Q188 | 18 | input_ontology | "In the cross-prompt setup, examples are selected from different source prompts, ensuring that each comes from a distinct training prompt to expose the model to varied contexts." |
| Q189 | 18 | output_form | "To account for variability in example selection, each experiment was repeated three times with random seeds 1, 11, and 42, and we report the average performance across runs." |
| Q190 | 18 | output_form | "For all the LLM experiments, we used vLLM for inference with the outlines library to enforce the JSON output format." |

---

## Regional Context

```yaml
name: Arab High-School Arabic Essay Feedback (Qatar Primary)
abbreviation: AHS-AEF-QA
assessment_slug: laila
deployment_scope:
  description: AI system providing formative, trait-level feedback on Arabic essay
    drafts written by Grade 10–12 students in Arab countries, with Qatar as the primary
    validated geography. The system produces natural-language revision suggestions
    tied to CAST rubric dimensions (REL, ORG, VOC, STY, DEV, MEC, GRA), not merely
    numeric scores.
  primary_geography: Qatar
  secondary_geographies:
  - Egypt
  - Saudi Arabia
  - Jordan
  - Lebanon
  - Other Arab-world countries (unspecified)
  primary_institution_context: Qatari Ministry of Education and Higher Education public
    and private high schools; partially validated against 24-school LAILA sample
  secondary_institution_context: National Ministry of Education equivalents in Egypt,
    Saudi Arabia, Jordan, Lebanon — unvalidated against benchmark
target_population:
  role: High school students (Grade 10–12) submitting Arabic essay drafts for AI-assisted
    formative feedback before teacher assessment
  age_range: Approximately 15–18 years old
  academic_stage: Late secondary; preparing for national or university-entrance level
    Arabic language examinations
  writing_context: Formative (pre-submission) essay drafts in academic Arabic; written
    under school-assigned prompt conditions
  gender_balance: Intended to serve both male and female students; LAILA benchmark
    was designed with explicit gender balance (design principle D3)
  national_curricula_served:
    qatar:
      curriculum_body: Qatar Ministry of Education and Higher Education (Arabic Section,
        Department of Educational Supervision)
      rubric_anchor: CAST rubric developed by Qatar University Testing Center (QUTC)
      benchmark_coverage: PRIMARY — benchmark essays drawn from 24 Qatari schools,
        grades 10–12
      notes: 'Strongest validity signal; all annotation norms grounded here. Qatar
        operates four school types: government schools (Arabic-medium national curriculum),
        Arabic private schools (also follow Qatari national curriculum), international
        private schools (follow diverse foreign curricula — British, American, French,
        German, etc.), and community schools. As of 2024–2025, there are 278 government
        schools serving ~137,048 students and 351 private schools enrolling ~228,488
        students (629 total), with approximately 60% of secondary students attending
        private schools. There are 23 different curricula in operation in Qatar. Arabic
        language and Islamic studies are mandatory for Qatari and Arab students even
        in private schools. The LAILA sample''s coverage of this school-type diversity
        is undocumented. Sources: Grokipedia/MoEHE data 2024–2025 — [WEB-1];
        Springer chapter on Qatari private school market (Amin & Cochrane 2023) —
        [WEB-2]; TutorChase
        2023 secondary enrollment figure — [WEB-3];
        Consulting Haus 2023 curriculum count — [WEB-4]'
    egypt:
      curriculum_body: 'Ministry of Education (وزارة التربية والتعليم) — responsible
        for Egyptian national curriculum. Since 2018, Egypt has been implementing
        a sweeping curriculum reform initiative aimed at aligning with international
        benchmarks. Source: IMPACT-se 2025 — [WEB-5]'
      rubric_anchor: '[NEEDS VERIFICATION — deferred: no publicly searchable Egyptian
        secondary Arabic writing rubric found; requires direct consultation with Egyptian
        MoE curriculum documents or subject specialists]'
      benchmark_coverage: NOT COVERED — no Egyptian student essays in LAILA
      notes: Potential dialectal MSA influence (Egyptian Arabic lexis/syntax in student
        writing) unaddressed by benchmark. Egypt's 2018+ curriculum reform is ongoing;
        writing assessment norms may be in transition.
    saudi_arabia:
      curriculum_body: 'Ministry of Education (وزارة التعليم / moe.gov.sa). Saudi
        Arabia has historically relied on textbooks to determine what to teach and
        assess, and recently developed a national curriculum framework focused on
        skills and competences under Vision 2030 reforms. Source: OECD review of Saudi
        education — [WEB-6]'
      rubric_anchor: '[NEEDS VERIFICATION — deferred: no publicly searchable Saudi
        secondary Arabic writing rubric found; Saudi assessment relies on centrally
        produced rating tools managed by supervisors; requires direct MoE curriculum
        access]'
      benchmark_coverage: NOT COVERED
      notes: Saudi education is gender-segregated; both sexes follow the same curriculum
        and take the same exams. Arabic is the official language and main medium of
        instruction. Saudi curriculum is actively reforming under Vision 2030, including
        introducing multiple learning pathways at upper secondary level. Scoring norm
        alignment with Qatar CAST rubric is unverified and likely diverges given different
        institutional frameworks.
    jordan:
      curriculum_body: 'Ministry of Education (وزارة التربية والتعليم — Jordan). Jordan''s
        curriculum has been subject to targeted modifications, though some curriculum
        content has been characterized as regressive. Source: IMPACT-se 2025 — [WEB-5]'
      rubric_anchor: '[NEEDS VERIFICATION — deferred: no publicly searchable Jordanian
        secondary Arabic writing rubric found; requires direct consultation with Jordanian
        MoE curriculum documents]'
      benchmark_coverage: NOT COVERED
      notes: Levantine-influenced MSA writing norms likely diverge from Qatar's Gulf
        MSA conventions. Rubric divergence from Qatar CAST unverified and unstudied.
    lebanon:
      curriculum_body: 'Ministry of Education and Higher Education (MEHE / وزارة التربية
        والتعليم العالي). Curriculum is developed by the Centre de Recherche et de
        Développement Pédagogiques (CRDP / المركز التربوي للبحوث والإنماء). The Lebanese
        national curriculum is used in all public and private schools; schools implementing
        foreign curricula (French, English, IB) must simultaneously meet Lebanese
        curriculum requirements. Source: WENR Education in Lebanon 2017 — [WEB-7]'
      rubric_anchor: '[NEEDS VERIFICATION — deferred: no publicly searchable Lebanese
        secondary Arabic writing rubric found; CRDP is the authoritative source but
        Arabic writing assessment criteria are not available in searchable form]'
      benchmark_coverage: NOT COVERED
      notes: 'Lebanon has a mandatory trilingual system: Arabic plus either English
        or French (with English/French as compulsory medium for mathematics and sciences).
        Schools offering foreign curricula must apply both Lebanese and foreign frameworks
        simultaneously. Research documents that many Lebanese students prefer writing
        in English or French over Arabic, and that Arabic ''has to be in the literary
        form, which they do not like'', suggesting potential MSA register avoidance
        that would affect essay quality norms. Levantine Arabic and French-contact
        influence on MSA writing is likely strong and is not accounted for in LAILA''s
        annotation scheme. Sources: Wikipedia Education in Lebanon — [WEB-8];
        Foreign Language Education in Lebanon (Shaaban et al.) — [WEB-9]'
languages:
  primary: Modern Standard Arabic (MSA / الفصحى) — the target language for all student
    essay production and system feedback
  register_note: Students write in MSA, but regional dialect influence on vocabulary,
    syntax, and discourse structure is expected, particularly for non-Qatari populations.
    The degree to which the CAST rubric penalizes regional MSA variation is undocumented
    and requires verification.
  dialect_influence_by_country:
    qatar_gulf: Gulf Arabic influence possible but less pronounced given formal exam
      context; benchmark population partially mitigated by Qatar's Arab expatriate
      diversity
    egypt: 'Egyptian Arabic lexical and syntactic interference in MSA writing documented
      in Arabic NLP literature; [NEEDS VERIFICATION — deferred: LAILA-specific handling
      not documented; likely unsearchable without direct examination of annotation
      guidelines]'
    lebanon: 'Strong Levantine and French-contact influence on MSA register documented;
      Lebanese students frequently code-switch and have been found to prefer writing
      in English/French over Arabic literary form, suggesting reduced MSA register
      fluency. Source: Shaaban & Ghaith (1999) as cited in — [WEB-9]'
    jordan: 'Levantine influence; [NEEDS VERIFICATION — deferred: likely unsearchable
      without dedicated Arabic NLP dialectal interference study for Jordan]'
    saudi_arabia: 'Gulf/Najdi influence; [NEEDS VERIFICATION — deferred: likely unsearchable
      without dedicated Arabic NLP dialectal interference study for Saudi Arabia]'
  system_output_language: Modern Standard Arabic (feedback and revision suggestions
    must be delivered in MSA accessible to G10–12 students)
  diglossia_note: Students are assessed on MSA production but communicate informally
    in regional dialects; the feedback system must remain register-appropriate for
    a formal educational context while remaining comprehensible to adolescent learners
writing_system:
  script: Arabic script (right-to-left)
  rtl_handling: Required for all input display and output rendering; mixed-direction
    text (Arabic + numerals or Latin citations) may appear in student essays
  morphological_note: Arabic root-pattern morphology creates tokenization complexity;
    short vowel diacritics (tashkeel) are typically absent in student prose, which
    affects NLP processing and readability of generated feedback
genre_coverage:
  benchmark_genres:
  - Explanatory (3 prompts)
  - Persuasive/Argumentative (5 prompts)
  deployment_genres_required:
  - Explanatory
  - Persuasive/Argumentative
  - Literary analysis
  - Religious/Quranic text commentary
  - Cultural commentary
  - Narrative (possible, curriculum-dependent)
  - Descriptive (possible, curriculum-dependent)
  genre_gap_severity: HIGH — benchmark covers only 2 of approximately 5–7 genre types
    required by deployment; CAST rubric is explicitly designed for persuasive/argumentative
    writing and its applicability to literary analysis or religious text commentary
    is unvalidated
  genre_gap_notes: 'No Arabic AES dataset or rubric framework covering literary analysis,
    religious text commentary, or cultural commentary genres was found in any existing
    benchmark or shared task. The TAQEEM 2025 shared task — the first Arabic AES shared
    task (ArabicNLP 2025, Suzhou) — introduced 1,265 essays but continued the same
    explanatory and persuasive genre restriction, indicating the field has not yet
    addressed genre breadth. The ZaQQ dataset (2025, MDPI) uses a human–AI collaborative
    framework on 7 traits including Relevance, Organization, Vocabulary, Style, Development,
    Mechanics, and Structure, but also remains confined to standard essay genres.
    No Arabic AES resource for Quranic/religious text commentary or literary analysis
    genre exists in the public literature as of searches conducted May 2026. Sources:
    TAQEEM 2025 ACL Anthology — [WEB-10];
    ZaQQ 2025 MDPI — [WEB-11]'
rubric_and_scoring:
  benchmark_rubric: CAST (Core Academic Skills Test) rubric, developed by Qatar University
    Testing Center (QUTC), provided in Arabic
  traits:
  - id: REL
    name: Relevance
    scale: 0–2 (3-point)
    note: Narrow scale; QWK may underrepresent subtle model prediction differences
  - id: ORG
    name: Organization
    scale: 0–5 (6-point)
  - id: VOC
    name: Vocabulary
    scale: 0–5 (6-point)
  - id: STY
    name: Style
    scale: 0–5 (6-point)
    note: Highly subjective; cross-national norm transferability unverified
  - id: DEV
    name: Development
    scale: 0–5 (6-point)
    note: Highly subjective; cross-national norm transferability unverified
  - id: MEC
    name: Mechanics
    scale: 0–5 (6-point)
  - id: GRA
    name: Grammar
    scale: 0–5 (6-point)
  holistic_score: Sum of all 7 trait scores
  zero_rule: If REL = 0, all other trait scores are set to 0
  rubric_genre_scope: Explicitly designed for persuasive/argumentative writing; applicability
    to other genres in deployment is unvalidated
  cross_national_norm_transferability: '[NOT FOUND — searched Arabic essay scoring
    inter-rater reliability cross-national Arab teacher judgment; no empirical comparison
    of CAST scoring norms against Egyptian, Saudi, Jordanian, or Lebanese teacher
    annotation conventions was found in published literature. This gap is confirmed
    absent from the Arabic AES literature; expert elicitation with teachers from each
    target country is required.]'
  annotator_pool:
    size: 6 annotators + 3 supervisors
    qualification: All Arabic language teachers or lecturers; 5 hold MSc or PhD in
      Arabic language
    institutional_affiliation: Qatar-based (Qatar University / associated institutions)
    iaa_qwk_range: 0.66 (P5) to 0.75 (P1) average across prompts
    adjudication_rate_p5: 23.3% of P5 essays required third-annotator adjudication
    inter_rater_details: '[NEEDS VERIFICATION — deferred: full per-trait IAA breakdown
      and whether any non-Qatari Arab teachers participated are not available in the
      public LAILA paper; requires direct contact with authors or access to supplementary
      annotation materials]'
output_function:
  benchmark_output: Numeric trait scores (ordinal) and holistic score; evaluated by
    Quadratic Weighted Kappa (QWK) against human annotations; LLMs output structured
    JSON scores
  deployment_output_required: Actionable natural-language revision suggestions with
    explanations of why points were lost on each trait dimension, delivered in MSA
    appropriate for G10–12 students
  output_form_mismatch: DIRECT AND DOCUMENTED — benchmark validates scoring fidelity
    only; no model in the benchmark generates natural-language feedback; QWK cannot
    capture pedagogical usefulness or actionability of revision suggestions
  formative_feedback_validity_gap: 'Confirmed gap in Arabic NLP. A 2024 survey on
    deep learning-based AES confirms that ''crucial aspects of writing evaluation,
    such as providing feedback, have often been overlooked'' even in English, and
    that ''building a deep learning-based AES that not only assesses essays but also
    generates insightful feedback holds immense value for formative writing assessments.''
    No Arabic-specific rubric-to-natural-language feedback generation system was found.
    The eRevise system (English) demonstrates one AES-to-formative-feedback architecture
    (score-triggered feedback messages) but has no Arabic equivalent. The AAEE system
    (Beseiso & Alzahrani 2020, Saudi Arabia) provides grade scores and corrected essay
    versions but does not generate trait-grounded revision suggestions. Sources: Springer
    survey on AES and feedback generation 2024 — [WEB-12];
    AAEE Saudi system (ResearchGate) — [WEB-13]'
  student_comprehensibility_requirement: Feedback must be at a register and vocabulary
    level accessible to adolescents (age ~15–18) writing in MSA; overly formal or
    technical language may reduce actionability
  actionability_criteria: Students must understand why they lost points on each trait,
    not just receive a numeric rating — benchmark provides no signal on this dimension
educational_context:
  essay_conditions:
    benchmark: 65-minute timed, digital submission via Microsoft Forms, supervised
      exam-style conditions
    deployment: Pre-submission draft review (formative context); students submit drafts
      voluntarily before teacher grading — less time pressure than benchmark conditions;
      essay quality and length may differ from benchmark distribution
    length_distribution_note: Benchmark essays average 171 words (concentrated 150–180
      words); deployment drafts may be longer or shorter depending on assignment type
      and grade level; benchmark lacks extended writing samples (few essays >500 words)
  within_qatar_school_type_variation:
    benchmark_coverage: 24 schools sampled; school-type breakdown not documented
    gap: 'The LAILA sample''s coverage across Qatar''s four school types (government
      Arabic-medium, Arabic private, international private, community) is not documented.
      As of 2024–2025, approximately 60% of Qatari secondary students attend private
      schools, and 23 distinct curricula are in operation. International private schools
      follow British (45.8% of K-12 schools), American (13.4%), or other foreign curricula;
      Arabic private schools follow the Qatari national curriculum. If LAILA''s 24-school
      sample skews toward government or Arabic private schools, international school
      students — who represent a large share of the secondary population — may be
      systematically underrepresented. Sources: Grokipedia/MoEHE 2024–2025 — [WEB-1];
      Consulting Haus 2023 — [WEB-4]'
    qatar_school_types: 'Four types: (1) government schools — free, Arabic-medium
      national curriculum, serve primarily Qatari nationals; (2) Arabic private schools
      — implement Qatari national curriculum with Arabic as medium of instruction;
      (3) international private schools — follow diverse foreign curricula (British,
      American, French, German, Indian, etc.), though Arabic language/Islamic studies
      remain mandatory for Qatari and Arab students; (4) community schools — serve
      expatriate nationals using home-country curricula. As of 2024–2025: 278 government
      schools (137,048 students), 351 private schools (228,488 students). British
      curriculum leads with 157 K-12 schools (45.8%), followed by American (46 schools,
      13.4%), SEC/Qatari (44 schools, 12.8%), Indian (43 schools, 12.5%). Sources:
      Grokipedia/MoEHE — [WEB-1];
      Springer chapter — [WEB-2];
      Consulting Haus — [WEB-4]'
  prompt_imbalance: Prompts P3 and P4 have fewer essays than others; may produce skewed
    performance estimates in prompt-specific evaluation
  student_motivation_context: Participation in LAILA was voluntary and independent
    of academic grades; deployment use is formative and pre-submission — motivational
    alignment is higher in deployment but writing conditions differ
infrastructure_notes:
  primary_access_mode: School-administered digital platform (web-based essay submission);
    deployment interface unspecified but likely web or LMS-integrated
  device_context: School computer labs assumed for Qatar exam context; deployment
    may include personal devices (tablets, smartphones) for draft editing outside
    class
  arabic_nlp_tooling: Arabic-centric models (AraBERT, AraT5, ALLaM, Command-R7B-Arabic,
    Fanar) are available and benchmarked; Arabic NLP tooling is improving but remains
    behind English for tasks requiring generation quality (relevant for feedback output)
  rtl_rendering: Must be ensured in all UI surfaces delivering feedback to students
  internet_connectivity_qatar: '99% internet penetration in Qatar as of 2024, with
    95.2% social media user rate. This indicates near-universal digital infrastructure
    for web-based deployment in Qatar. Source: Data Reportal 2024, as cited in ResearchGate
    — [WEB-14]'
  internet_connectivity_secondary_geographies: '[NEEDS VERIFICATION — deferred: below
    search budget; comparable figures for Egypt, Jordan, Lebanon, Saudi Arabia secondary
    school students would require ITU/World Bank sub-national data not accessed in
    this pass]'
  lms_integration: 'For Qatari government schools, the official LMS is ''Qatar Education''
    (قطر للتعليم), a mobile application developed by the Ministry of Education and
    Higher Education (MoEHE) for managing classroom activities, assessments, and student
    progress. Private and international schools use varied platforms. The Qatar e-learning
    management system market is fragmented across local providers (Malomatia, Zinger
    Stick Software) and global platforms, with no single dominant private school LMS.
    Saudi Arabia uses ''Madrasati'' (مدرستي) for public schools. Egypt uses the national
    ''iEN'' platform. Jordan and Lebanon do not have a single nationally mandated
    LMS for secondary education identifiable from current search. Sources: Qatar Education
    app (Google Play/App Store) — [WEB-15];
    Mordor Intelligence Qatar LMS market — [WEB-16]'
cultural_and_pedagogical_norms:
  arabic_essay_tradition: Academic Arabic essay writing (إنشاء) is a formal, high-status
    skill in Arab education systems; rhetorical conventions (including classical Arabic
    stylistic expectations) differ from Western essay norms
  religious_and_cultural_content: Essay topics involving religious texts, Quranic
    reference, and Islamic cultural commentary are common in Arab curricula and represent
    a genre gap in the benchmark; feedback systems must handle such content appropriately
  teacher_authority: 'Feedback norms in Arab educational culture tend toward teacher-authoritative
    correction; AI formative feedback as a peer-like or dialogic mechanism may require
    cultural framing for student acceptance. Evidence from Saudi Arabia is mixed:
    one study found Saudi teachers gave AI assessment a mean approval of only 2.26/5
    on a Likert scale, while another found Saudi educators broadly favourable to AI
    in teaching — ''suggesting something of a tension between two national-cultural
    forces'' around Vision 2030 vs. traditional teacher authority. Saudi EFL students
    generally report positive experiences with AI writing tools (valuing prompt responses
    and grammar assistance). No Qatar-specific study of Arabic writing feedback acceptance
    by students or teachers was found. Sources: Saudi teacher attitudes study (Tandfonline
    2024) — [WEB-17];
    Saudi EFL learner perceptions (AWEJ 2025) — [WEB-18]'
  gender_norms_in_schools: Qatar operates gender-segregated public schools; essays
    from male and female students were balanced in LAILA; deployment may need to account
    for single-gender school contexts in feedback framing. Saudi Arabia also operates
    a gender-segregated education system.
  student_age_appropriateness: Prompts in benchmark were designed to be developmentally
    appropriate for G10–12 and free of sensitive topics; deployment feedback generation
    must maintain age-appropriate register and avoid inadvertently penalizing culturally
    normative content
  national_identity_and_curriculum_narratives: Essay prompt topics may reference national
    histories, cultural values, or political identities that vary across Arab countries;
    feedback systems trained on Qatari prompts may reflect Qatar-centric content assumptions
  qatar_national_ai_strategy: 'Qatar launched a National AI Strategy in 2019 with
    education as a key pillar, aiming to make AI a fundamental part of education in
    all grades and subjects; this creates an institutional environment broadly supportive
    of AI-in-education deployment. Source: UNESCO International Forum on AI and Education
    2022 — [WEB-19]'
regulatory_and_ethical_context:
  benchmark_restrictions: LAILA authors explicitly prohibit use for high-stakes educational
    decisions affecting individual students; require fairness auditing and stakeholder
    consultation before real-world deployment
  qatar_data_protection: 'Qatar Law No. 13 of 2016 on Protecting Personal Data Privacy
    (PDPPL), which took effect in January 2017. The PDPPL is the primary data protection
    framework in Qatar; it applies to all personal data processed electronically within
    Qatar. The competent enforcement authority is the National Cyber Governance and
    Assurance Affairs (NCGAA) within the National Cyber Security Agency (NCSA). The
    law is GDPR-aligned in principles (transparency, fairness, consent, breach notification,
    data minimisation) but is not as stringent as GDPR. Penalties for non-compliance
    range from QAR 1,000,000 to QAR 5,000,000. Fourteen regulatory guidelines were
    issued by the Ministry of Transport and Communications in January 2021. Student
    essay data processed by an EdTech system qualifies as electronically processed
    personal data subject to the PDPPL. Sources: NCSA official page — [WEB-20];
    Securiti PDPPL overview — [WEB-21];
    Chambers & Partners 2026 — [WEB-22]'
  secondary_geography_data_protection:
    egypt: '[NEEDS VERIFICATION — deferred: below search budget; Egypt enacted a Personal
      Data Protection Law (Law No. 151 of 2020) but sub-national EdTech applicability
      requires further verification]'
    saudi_arabia: '[NEEDS VERIFICATION — deferred: below search budget; Saudi Arabia
      enacted a Personal Data Protection Law (PDPL) effective September 2023 but specific
      provisions for student/minor data in EdTech require further verification]'
    jordan: '[NEEDS VERIFICATION — deferred: below search budget]'
    lebanon: '[NEEDS VERIFICATION — deferred: below search budget; Lebanon has limited
      data protection legislation and ongoing governance challenges]'
  irb_and_consent_model: LAILA collection covered by Qatar University IRB (QU-IRB
    159/2024-EA) with student and guardian consent; deployment system requires its
    own consent and data governance framework
  minor_student_data: All target users are minors (approximately 15–18); heightened
    data protection obligations apply in all jurisdictions. Qatar PDPPL requires explicit
    consent and additional safeguards for sensitive data; student academic data collected
    by a deployment system would require explicit consent from students and guardians
    as minors.
  fairness_auditing_requirement: Benchmark authors specifically recommend fairness
    auditing before deployment; gender, nationality, and school-type fairness dimensions
    are relevant
flagged_research_gaps:
- gap_id: 1
  label: Cross-national curriculum rubric alignment
  description: It is unknown how much scoring norms for STY, DEV, and other subjective
    traits diverge between Qatar's CAST rubric and writing assessment standards in
    Egypt, Saudi Arabia, Jordan, and Lebanon. No published cross-national comparison
    was found in the Arabic AES literature.
  search_target: Arabic language national curriculum writing rubrics Egypt Saudi Arabia
    Jordan Lebanon; comparison with Qatar CAST AES grading conventions for secondary
    level
  search_status: SEARCHED — no empirical cross-national comparison found. Individual
    national MoE curriculum frameworks exist but published Arabic writing rubrics
    for secondary level are not in the searchable literature. Expert elicitation with
    teachers from each target country is required.
- gap_id: 2
  label: Genre coverage for literary analysis, religious text, and cultural commentary
  description: No benchmark data or rubric covers these genres despite their prevalence
    in Arab secondary curricula. CAST rubric is explicitly persuasive/argumentative.
    TAQEEM 2025 (the first Arabic AES shared task) also remains confined to explanatory
    and persuasive genres, confirming this is a field-wide gap.
  search_target: Arabic AES dataset or rubric framework covering literary analysis,
    Quranic/religious text commentary, cultural commentary; Arab high-school writing
    assessment genre breadth
  search_status: 'SEARCHED — gap confirmed. No Arabic AES dataset or rubric for these
    genres exists. TAQEEM 2025 and ZaQQ 2025 are the most recent resources; both maintain
    the explanatory/persuasive genre restriction. Source: TAQEEM 2025 — [WEB-10]'
- gap_id: 3
  label: Actionable feedback generation validity
  description: No evidence that LAILA's trait-score framework maps onto quality natural-language
    revision suggestions; benchmark validates scoring, not feedback generation. The
    broader AES field acknowledges this gap even in English; no Arabic rubric-to-feedback
    system exists.
  search_target: Arabic automated essay scoring formative feedback natural language
    explanation revision suggestion generation Arabic NLP writing feedback system
  search_status: 'SEARCHED — gap confirmed. The 2024 Springer survey on deep learning-based
    AES explicitly identifies feedback generation as an overlooked area. The AAEE
    Saudi system generates corrected essay versions but not trait-grounded revision
    suggestions. No Arabic system bridges CAST trait scores to actionable natural-language
    feedback for secondary students. Sources: Springer 2024 — [WEB-12];
    AAEE Saudi — [WEB-23]'
- gap_id: 4
  label: Regional MSA variation in student writing
  description: Whether LAILA's annotation scheme penalizes or accommodates Levantine,
    Egyptian, or other dialectal influence on MSA student writing is undocumented.
    Lebanese students are documented to resist formal MSA writing norms.
  search_target: Modern Standard Arabic regional variation in secondary student writing;
    Egyptian Levantine dialect interference in MSA essays; Arabic essay annotation
    rubric treatment of dialectal features
  search_status: SEARCHED — gap confirmed from indirect evidence. Lebanese multilingual
    research documents resistance to MSA literary register among secondary students.
    No direct study of LAILA annotation treatment of regional MSA variation was found.
    Likely unsearchable without direct examination of LAILA annotation guidelines
    by researchers.
- gap_id: 5
  label: Within-Qatar school-type representativeness
  description: LAILA's 24-school sample may not include international schools, private
    Arabic-medium schools, or lower-performing public schools. Qatar has 4 school
    types, 23 distinct curricula, and ~60% of secondary students in private schools
    — school-type breakdown of the LAILA sample is undocumented.
  search_target: 'Qatar secondary school system composition: government, independent,
    international, private school proportions; G10–12 student population distribution
    by school type'
  search_status: 'SEARCHED — Qatar school type landscape verified; LAILA sample breakdown
    remains unresolved (requires authors or data documentation). Qatar school data:
    278 government schools, 351 private schools (2024–2025); ~60% of secondary students
    in private schools; 23 curricula. Sources: [WEB-1];
    [WEB-3]'
- gap_id: 6
  label: Annotator demographics and inter-rater reliability for subjective traits
  description: Whether STY and DEV scores reflect a single institutional norm or broader
    teacher-community consensus is unknown; per-trait IAA details and annotator backgrounds
    need verification.
  search_target: LAILA dataset annotator demographics; per-trait inter-annotator agreement
    statistics for STY and DEV; Arabic essay annotation reliability for style and
    development dimensions
  search_status: 'NEEDS VERIFICATION — deferred: per-trait IAA and annotator nationality/background
    are not in the published LAILA paper''s public-facing sections; requires direct
    contact with authors or access to supplementary data.'
- gap_id: 7
  label: Student and teacher attitudes toward AI formative feedback in Arab educational
    culture
  description: Cultural acceptance of AI-generated feedback in teacher-authoritative
    Arab educational systems is partially characterized for Saudi Arabia (mixed teacher
    attitudes, generally positive student attitudes for EFL writing) but uncharacterized
    for Qatar specifically for Arabic writing feedback.
  search_target: AI writing feedback student teacher attitudes Arab world Qatar Egypt
    Saudi Arabia; EdTech adoption secondary schools MENA; AI feedback cultural acceptance
  search_status: 'SEARCHED — partial evidence found. Saudi teacher attitudes to AI
    assessment: one study found mean approval of 2.26/5; another found broad favourability
    (mixed). Saudi EFL students generally positive about AI writing tools. Jordan:
    one study of 120 undergraduate EFL students found AI feedback comparable to teacher
    feedback for writing improvements. Qatar: one 2025 study of 553 G10–12 students
    (QU-IRB 222-EA/24) measured attitudes toward AI generally (positive), but not
    specifically toward Arabic essay feedback. No Qatar-specific Arabic essay AI feedback
    acceptance study found. Sources: Saudi teacher attitudes — [WEB-17];
    Jordan AI vs teacher feedback — [WEB-24];
    Qatar student AI attitudes — [WEB-25]'
net_new_fields:
  taqeem_2025_shared_task: 'TAQEEM 2025 (First Shared Task for Arabic Quality Evaluation
    of Essays in Multi-dimensions, ArabicNLP 2025, Suzhou) is the first Arabic AES
    shared task and introduces a new dataset of 1,265 essays annotated with holistic
    and trait-specific scores (Relevance, Organization, Vocabulary, Style, Development,
    Mechanics, Grammar). It includes two subtasks: holistic scoring (Task A) and trait-specific
    scoring (Task B). Critically, TAQEEM 2025 continues the explanatory and persuasive
    genre restriction of LAILA and does not address the genre coverage gap for literary
    analysis, religious text, or cultural commentary. The task attracted 11 registered
    teams for Task A and 10 for Task B, with 5 teams submitting final runs. This is
    the most recent community benchmark and confirms genre breadth remains an unsolved
    problem in Arabic AES. Relevance for scoring: confirms that as of late 2025, no
    community benchmark addresses deployment''s genre gap. Source: ACL Anthology —
    [WEB-10]'
  zaqq_2025_dataset: 'ZaQQ (2025, MDPI Data) is a new Arabic AES dataset constructed
    using a human–AI collaborative framework based on QAES, annotated for 7 writing
    traits (Relevance, Organization, Vocabulary, Style, Development, Mechanics, Structure).
    LLMs (including Gemini-Revision) achieved QWK scores of 0.810 on Vocabulary and
    0.700 on Relevance when tested against ZAEBUC and QALB datasets. The dataset addresses
    data scarcity but remains confined to standard essay genres; it does not cover
    religious, literary, or cultural commentary genres. Relevance: provides additional
    Arabic AES validation evidence for trait-level LLM scoring but does not resolve
    the genre or formative feedback gaps. Source: MDPI Data — [WEB-11]'
  qatar_national_ai_strategy_education: 'Qatar launched a National AI Strategy in
    2019 with education as one of its key pillars; the strategy explicitly argues
    that AI should be ''a fundamental part of education in all grades and subjects
    in primary and secondary schools.'' This provides a nationally supportive policy
    environment for AI-in-education deployment, which may lower institutional barriers
    to adoption relative to other Arab countries. Relevance: deployment in Qatar benefits
    from policy tailwinds but must still satisfy PDPPL data protection requirements
    and LAILA''s recommended fairness auditing. Source: UNESCO report citing Qatar''s
    National AI Strategy — [WEB-19]'
  arabic_essay_scoring_data_scarcity_confirmed: 'The Arabic AES literature consistently
    confirms that data scarcity remains the primary challenge: existing Arabic resources
    ''are often small in scale, lack trait-specific annotations, or consist solely
    of unannotated essays.'' The 2025 synthetic data augmentation work (arXiv 2503.17739)
    uses GPT-4o to generate CEFR-aligned Arabic essays to address this gap, but LLM-generated
    data without in-region human validation introduces stereotype risks for scoring
    norm accuracy. Relevance: confirms that any Arabic formative feedback system faces
    both data scarcity and a training-evaluation circularity challenge that the LAILA
    benchmark only partially resolves. Source: arXiv 2025 — [WEB-26]'
  saudi_ai_assessment_teacher_attitudes_caveat: 'A 2024 study of Saudi university
    EFL teachers using AI grading tool CoGrader found that ''the review also showed
    no studies like ours focused specifically on AI powered essay grading in Saudi
    Arabia'' and identified a tension between teacher desire to support Vision 2030
    technology goals and traditional teacher authority norms around assessment. One
    item measuring AI for assessment received a mean approval of only 2.26/5 among
    Saudi teachers. This is the closest available proxy for deployment cultural acceptance
    in an Arab educational context, but it concerns English essay grading by university
    teachers — generalizability to Arabic secondary essay feedback is uncertain. Relevance:
    flags a potential cultural acceptance risk for the deployment''s formative feedback
    framing in Saudi Arabia that warrants in-country stakeholder consultation. Source:
    Tandfonline 2024 — [WEB-17]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://grokipedia.com/page/List_of_schools_in_Qatar |
| WEB-2 | https://link.springer.com/chapter/10.1007/978-981-97-9667-0_11 |
| WEB-3 | https://www.tutorchase.com/blog/the-education-system-in-qatar-explained |
| WEB-4 | https://consulting-haus.com/wp-content/uploads/2023/09/CH_Education_Sector-Overview_September-2023.pdf |
| WEB-5 | https://www.impact-se.org/middle-eastern-curriculum-reform-a-window-into-national-values/ |
| WEB-6 | https://www.moe.gov.sa/ar/education/studies/Documents/Education%20in%20Saudi%20Arabia.pdf |
| WEB-7 | https://wenr.wes.org/2017/05/education-in-lebanon |
| WEB-8 | https://en.wikipedia.org/wiki/Education_in_Lebanon |
| WEB-9 | https://www.researchgate.net/publication/267714826_Foreign_Language_Education_in_Lebanon_A_Context_of_Cultural_and_Curricular_Complexities |
| WEB-10 | https://aclanthology.org/2025.arabicnlp-sharedtasks.134/ |
| WEB-11 | https://www.mdpi.com/2306-5729/10/9/148 |
| WEB-12 | https://link.springer.com/article/10.1007/s10462-024-11017-5 |
| WEB-13 | https://www.researchgate.net/publication/343796441_Automated_students_arabic_essay_scoring_using_trained_neural_network_by_e-jaya_optimization_to_support_personalized_system_of_instruction |
| WEB-14 | https://www.researchgate.net/figure/Total-Number-of-Schools-in-Qatar-Primary-Intermediate-Secondary_fig1_369912994 |
| WEB-15 | https://play.google.com/store/apps/details?id=app.qeducation.edu.gov.qa |
| WEB-16 | https://www.mordorintelligence.com/industry-reports/qatar-e-learning-management-system-market |
| WEB-17 | https://www.tandfonline.com/doi/full/10.1080/2331186X.2024.2430865 |
| WEB-18 | https://awej.org/saudi-efl-learners-perceptions-of-using-artificial-intelligence-and-its-impact-on-their-writing-skills/ |
| WEB-19 | https://unesdoc.unesco.org/ark:/48223/pf0000386162 |
| WEB-20 | https://assurance.ncsa.gov.qa/en/privacy/law |
| WEB-21 | https://securiti.ai/qatar-personal-data-protection-law/ |
| WEB-22 | https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/qatar |
| WEB-23 | https://www.sciencedirect.com/science/article/abs/pii/S0306457319304935 |
| WEB-24 | https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1614673/full |
| WEB-25 | https://journals.sagepub.com/doi/10.1177/21582440251378375 |
| WEB-26 | https://arxiv.org/html/2503.17739v2 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: LAILA was built around 24 schools in Qatar. Does your deployment target students across multiple Arab countries, or is it focused on Qatar? If multi-country, do essay prompts, curricula, and writing conventions differ meaningfully across countries?
A1: The system is intended to support students in multiple Arab countries, but reliability will be strongest for Qatar. Essay prompts and curricula differ across countries, making the benchmark less representative for non-Qatari contexts.

Q2 [OC]: When the system gives feedback on traits like 'style,' 'vocabulary,' or 'development,' whose standards define quality? Would a Jordanian student writing in Levantine-influenced MSA be judged by the same norms as a Qatari student? Do local curriculum bodies in each country apply different scoring conventions?
A2: Different national curriculum bodies and teacher communities exist, but it is unclear how much their scoring conventions diverge from Qatar's. MSA is nominally standard across the Arab world, though the degree of practical divergence in grading norms across countries remains an open empirical question that would need further research.

Q3 [OO]: Does the system need to produce actionable revision suggestions rather than numeric trait scores? Would students find trait-level scores self-explanatory, or do they need natural-language explanations for why they lost points on dimensions like 'mechanics' or 'organization'?
A3: Actionable revision suggestions with natural-language explanations are more helpful than scores alone. Students need to understand *why* they lost points on each trait, not just receive a numeric rating.

Q4 [IC]: Do the essay prompts students actually write to resemble the benchmark prompts (explanatory/persuasive), or do they include genres like literary analysis, religious texts, or cultural commentary?
A4: The benchmark is limited to 8 explanatory or persuasive prompts, which does not cover the full range of essay types students may be assigned — including literary analysis, religious texts, and cultural commentary — creating a meaningful coverage gap for diverse real-world assignments.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark covers only 8 prompts across two genres (explanatory/persuasive), while deployment involves a wider genre range (literary analysis, religious texts, cultural commentary) and students across multiple Arab countries with distinct curricula. |
| IC | HIGH | Essay content norms, rhetorical conventions, and culturally inflected topics (religious, political, literary) vary across Arab countries and genre types not represented in the benchmark, creating construct-irrelevant variance risks. |
| IF | LOWER | Deployment and benchmark are both text-only in Arabic; no modality mismatch exists. |
| OO | HIGH | The benchmark produces numeric trait scores, but the deployment requires natural-language, actionable revision feedback — a qualitatively different output function that the benchmark's scoring rubric was not designed to validate. |
| OC | MODERATE | Ground-truth labels were annotated by in-region Qatari stakeholders (a positive signal), but it is unknown whether annotation conventions for subjective traits like 'style' and 'development' transfer to other Arab national curricula or non-Qatari teacher judgment. |
| OF | HIGH | The benchmark outputs labels and scores, but the deployment requires open-ended natural-language revision suggestions and explanations — a direct output-form mismatch that the benchmark cannot directly validate. |

---

## Framework Dimensions to Evaluate

### Input Ontology

**Definition**: The input data ontology consists of the set of test case categories represented by the benchmark, which should cover the query types that evaluated systems are expected to encounter during deployment (e.g., factual questions, creative writing help, or restaurant recommendations for NLP dialogue systems; pick-and-place tasks, point navigation, or planning for robotics).

**Theoretical Importance**: A misalignment in this taxonomy — whether through the omission of necessary categories (construct underrepresentation) or the inclusion of irrelevant ones (construct-irrelevant variance) — harms the content validity of the benchmark.

**Checklist:**
- [IO-1] Identify test case categories required for regional deployment.
- [IO-2] Check if source benchmark's taxonomy omits regionally-relevant categories.
- [IO-3] Check if source benchmark includes categories irrelevant to regional context.
- [IO-4] Document category gaps that would harm content validity.

### Input Content

**Definition**: Whereas the ontology defines the types of input queries, the content of dataset inputs refers to the explicit instances specified by individual datapoints — an LLM prompt, an image, a database entry, etc.

**Theoretical Importance**: Even when the test case taxonomy provides good coverage, implementation-level details of individual datapoints can introduce construct-irrelevant variance, violating content validity.

**Checklist:**
- [IC-1] Determine if input queries require region-specific cultural, geographic, or dialectal knowledge.
- [IC-2] Assess whether culturally sensitive content aligns with target deployment culture.
- [IC-3] Flag inputs requiring Western-specific knowledge that may not transfer.
- [IC-4] Recruit regional annotators to identify culturally sensitive instances if resources permit.
- [IC-5] Document content issues that would harm content validity.

### Input Form

**Definition**: The form of dataset inputs determines the encoding of the input signal — e.g., text vs. audio for natural language, or camera parameters such as focal length and resolution for visual data.

**Theoretical Importance**: Since machine learning systems are sensitive to signal distributions, a mismatch between the benchmark's input representation and the real-world signals that deployed models would encounter violates the external validity of the evaluation.

**Checklist:**
- [IF-1] Compare signal distributions (e.g., image resolution, MRI field strength) between source and target contexts.
- [IF-2] Check if regional infrastructure supports the same data capture specifications.
- [IF-3] Identify domain-specific form differences relevant to the intended use case.
- [IF-4] Document form mismatches that would harm external validity.

### Output Ontology

**Definition**: A benchmark's output ontology determines the space of outputs an AI system is expected to produce and the decision rules by which those outputs are organized and scored — i.e., the benchmark's criteria. For categorical outputs, the mapping is direct (e.g., safe/unsafe, or object class labels). For free-form outputs, the scoring function must first interpret what the output means before mapping it to a score — and this interpretive step is where validity violations most readily arise, since decision rules can differ across cultural contexts. For instance, an LLM recommending "red wine" for a dinner party may score highly for helpfulness in a Western context but poorly where alcohol consumption is prohibited.

**Theoretical Importance**: A misaligned output taxonomy thus violates structural validity (the construct's structure is misrepresented), content validity (through missing or irrelevant categories), and risks violating external validity (benchmark performance is less likely to generalize to regional settings).

**Checklist:**
- [OO-1] Review output label categories for regional relevance.
- [OO-2] Identify missing categories specific to regional contexts (e.g., autorickshaws in Indian driving data).
- [OO-3] Flag categories that encode non-regional values or assumptions.
- [OO-4] Consider stakeholder-driven taxonomy redesign if significant misalignment exists.
- [OO-5] Document taxonomy issues that would harm structural validity and content validity.

### Output Content

**Definition**: Whereas taxonomic alignment addresses whether abstract decision boundaries reflect regional values, label correctness concerns whether the labels for particular datapoints correlate with the judgments of regional stakeholders.

**Theoretical Importance**: Disagreement between regional and original annotators violates both convergent validity (the labels fail to correlate with regional perspectives on the construct) and external validity (the original judgments do not generalize to the target context).

**Checklist:**
- [OC-1] Determine if ground truth labels reflect regional stakeholder perspectives.
- [OC-2] Assess potential disagreement between original annotators and regional population.
- [OC-3] Review annotator demographics in benchmark documentation (Datasheets, Data Statements).
- [OC-4] Consider label re-annotation by representative regional annotator pool.
- [OC-5] Review aggregation methods for potential erasure of minority perspectives.
- [OC-6] Document label issues that would harm convergent validity and external validity.

### Output Form

**Definition**: The form of dataset outputs pertains to the representation of output signals models are expected to produce.

**Theoretical Importance**: If a benchmark does not evaluate models on the output forms encountered during real-world deployment, this violates the external validity of the evaluation.

**Checklist:**
- [OF-1] Check if expected output modality matches regional deployment needs.
- [OF-2] Assess text-to-speech availability for speech-based output requirements.
- [OF-3] Consider literacy rates and accessibility requirements in target population.
- [OF-4] Document form mismatches that would harm external validity.


---

## Required Output Format

Output a single valid JSON object with this structure:

```json
{
  "benchmark": "laila",
  "region": "Arab High-School Arabic Essay Feedback (Qatar Primary)",
  "dimensions": {
    "input_ontology": {
      "score": "<integer 1-5>",
      "justification": "...",
      "strengths": ["what this dimension captures well for the target context"],
      "checklist_responses": { "IO-1": "...", "IO-2": "..." },
      "evidence_quotes": ["[Q1] 'quote text' (p.7)", ...],
      "evidence_web_sources": ["[WEB-1] literacy rate 96%", ...],
      "evidence_dataset": ["DATASET-D1: observation", ...],
      "evidence_map": { "IO-1": ["Q1", "WEB-3"], "IO-2": ["DATASET-D1"] },
      "confidence": "<high|medium|low>",
      "information_gaps": ["..."],
      "requires_expert_verification": ["..."]
    },
    "input_content": { "..." },
    "input_form": { "..." },
    "output_ontology": { "..." },
    "output_content": { "..." },
    "output_form": { "..." }
  },
  "overall_summary": "...",
  "risk_assessment": "<high|medium|low>",
  "practical_guidance": {
    "what_this_benchmark_measures": "...",
    "construct_depth": "...",
    "supplementation_needed": "..."
  },
  "remediation_suggestions": [
    { "dimension": "...", "gap": "...", "recommendation": "..." }
  ],
  "highest_concern_dimensions": ["..."],
  "strongest_dimensions": ["..."]
}
```
