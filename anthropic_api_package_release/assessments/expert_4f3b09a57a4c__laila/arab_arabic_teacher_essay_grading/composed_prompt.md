I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **LAILA: The Largest Publicly Available Arabic Automated Essay Scoring Dataset** is valid for use in **Arab-Country G10–12 Arabic Teachers: AI Essay Grading Assistance**.

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
- **Full Name**: LAILA: The Largest Publicly Available Arabic Automated Essay Scoring Dataset
- **Domain**: Automated Essay Scoring (AES) for Arabic
- **Languages**: ar
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
LAILA's task taxonomy is organized around the nine design principles [Q20] that
shaped the dataset, with AES evaluated across two experimental setups — prompt-specific
and cross-prompt [Q14] — and two research questions addressing overall model-category
comparison and per-trait model performance [Q46]. The benchmark evaluates a diverse
model taxonomy spanning feature-based (Linear Regression, Random Forest, XGBoost,
Neural Network [Q49]), encoder-based (AraBERT, AraT5 [Q50], ProTACT, MOOSE [Q53]),
and LLM categories (ALLaM, Command-R7B-Arabic, Fanar [Q51]), in zero-shot and
few-shot settings [Q180]. The task is formulated as regression for FB and encoder
models, and as text generation for AraT5, which predicts trait scores sequentially [Q147].
For LLMs, zero-shot prompting requires JSON-format trait score generation given prompt
text, essay, and rubric [Q181]; few-shot prompting omits the rubric and supplies scored
examples [Q183], with examples drawn from the same prompt (prompt-specific) or different
prompts (cross-prompt) [Q187, Q188].

The trait taxonomy covers seven writing dimensions grounded in the QUTC CAST rubric
[Q34, Q118]. However, the ontology is exclusively confined to explanatory and
persuasive essay genres [Q89, Q125]; narrative, descriptive, and other genres are
absent. Critically for multi-country deployment, the seven-trait structure reflects
Qatari curriculum design: the paper does not document whether the trait ontology maps
onto grading frameworks used in Egypt, Jordan, Saudi Arabia, Lebanon, or Morocco.
TAQEEM 2025's shared task citation [Q107] situates LAILA within broader Arabic
AES community interest in multi-dimensional quality evaluation, but no cross-national
curricular alignment analysis is provided. The benchmark's output is exclusively
discrete point-score labels; it does not evaluate confidence estimation, uncertainty
quantification, or rationale generation — functions relevant to teacher-facing deployment.

### Input Content
LAILA's essay content was collected under IRB approval (QU-IRB 159/2024-EA [Q9])
from 4,372 students at 24 schools in Qatar over one academic year across 27 visits
[Q3, Q27]. Collection was designed under explicit diversity principles: prompts were
intentionally varied across genres with cultural relevance to the Arabic-speaking
context and age-appropriateness [Q22, Q99], gender balance among student writers was
targeted [Q23, Q100], and authentic, classroom-produced writing was prioritized to
preserve genuine linguistic variation [Q21]. The dataset spans 3,446 explanatory and
4,413 persuasive essays across 8 prompts, with 500–1,181 essays per prompt [Q38, Q39].

Despite the cultural-relevance design principle, the collection context is exclusively
Qatari: all students attended Qatari schools (grades 10–12), and the prompts were
designed for a Qatari educational context. The paper acknowledges that this may limit
generalizability to other Arabic-speaking populations with different educational systems
[Q88], with partial mitigation attributed to Qatar's large Arab expatriate population.
However, no prompts grounded in Egyptian history, Levantine literary traditions, or
North African social norms are documented. For deployment scenarios where teachers
assign locally grounded prompts, models trained on LAILA may systematically misjudge
relevance and development [Q4, Q22]. The LLM selection was guided by the Open Arabic
LLM Leaderboard [Q178], and comparison datasets include English corpora (ASAP/ASAP++,
PERSUADE [Q17]) and multilingual resources (MERLIN, TOEFL11 [Q112, Q113]), situating
LAILA within the international AES landscape but not within a cross-Arab-country framework.

### Input Form
Essays were collected digitally via Microsoft Forms with a 65-minute time limit [Q26],
emulating high-stakes testing conditions [Q25]. The resulting dataset is exclusively
written Modern Standard Arabic text, with no audio, image, or multi-modal components.
The essay length distribution is unimodal, centered around 171 words on average, with
most essays falling between 90 and 210 words and a peak in the 150–180 word range
[Q134, Q135]. Shorter essays (1,061 between 11–60 words) form a pronounced tail [Q136],
and very few essays exceed 500 words [Q138]; the minimum post-cleaning length is 11
words [Q137]. Personally identifiable information was systematically removed and
pre-generated anonymous identifiers were assigned [Q97]. An English-translated version
of the CAST rubric is provided [Q116], and model inputs for AraT5 consisted of a scoring
instruction concatenated with the essay text [Q148], while AraBERT encoded essay and
prompt together [Q157]. LLM experiments enforced a 4,096-token context limit with
iterative example removal when exceeded [Q184, Q185], and used vLLM with the outlines
library for JSON output [Q190].

The text-only MSA format matches the deployment scenario's modality and script
requirements. No script mismatch, infrastructure incompatibility, or modality gap is
documented. The short average essay length (171 words) is noted as a limitation for
assessing long-form academic tasks [Q92]. The data format comparison table [Q12]
contextualizes LAILA against multilingual AES datasets on length, annotation depth,
and public availability.

### Output Ontology
LAILA's output label schema comprises seven trait scores (REL, ORG, VOC, STY, DEV,
MEC, GRA [Q34, Q115]) plus a holistic score computed as their sum [Q35]. Six traits
use a 6-point scale (0–5); REL uses a 3-point scale (0 = not relevant, 1 = partially
relevant, 2 = fully relevant) [Q36, Q120]. An essay scoring REL = 0 automatically
receives 0 on all other traits [Q37]. Score 0 is assigned for non-attempts, below-minimum
performance, or off-topic content [Q117]. Score distributions across prompts approximate
a normal distribution for most traits, with REL strongly skewed toward score 2 [Q40, Q119,
Q123]; GRA and VOC show the highest proportion of score 1 (16%), and MEC follows at 13%
[Q40]. Detailed rubric descriptors per trait are provided in an English translation of
the CAST rubric [Q118].

From a deployment validity perspective, the output ontology is internally coherent and
grounded in QUTC's CAST rubric but does not document alignment with grading frameworks
used in other Arab countries. The narrow REL scale (0–2) is itself flagged as a
limitation that may cause QWK to underrepresent subtle model prediction differences [Q91].
More critically for the teacher-facing deployment scenario, the benchmark produces only
discrete point-score outputs: it does not evaluate model capacity to express uncertainty,
generate confidence intervals, or provide score rationale — all functions identified as
essential by the deployment use case. The LLM holistic score is computed as the sum
of individual trait scores [Q182], maintaining label-only output form throughout.

### Output Content
Annotation was performed by a team of 6 annotators and 3 supervisors, all Arabic
language teachers or lecturers; five hold advanced degrees (MSc or PhD) in the Arabic
language [Q30, Q31]. Supervisors oversaw training, quality assurance, and dispute
resolution [Q32]; all annotators received fair compensation at or above local professional
rates [Q101] and completed structured training before formal scoring [Q102]. Two
supervisors developed a comprehensive annotation guidebook with terminology, exemplars,
and annotated practice materials for each prompt type, followed by moderation sessions
to harmonize rubric interpretations [Q41]. Scoring was conducted on the Assessment
Gourmet Platform with annotator blindness to student identity [Q42, Q98], essays randomly
distributed to minimize bias, and session lengths capped to prevent fatigue [Q43].

Each essay was independently scored by two annotators; HOL discrepancy < 6 points
led to mean-and-round-down aggregation; discrepancies ≥ 6 points were escalated to
a supervisor [Q43]. IAA measured by QWK ranged from 0.66 (P5) to 0.75 (P1), classified
as substantial [Q44]; P5 showed the highest third-annotator escalation rate (23.3%) [Q45].
Annotation followed the CAST rubric developed by QUTC and provided in Arabic [Q114],
with comprehensive guidelines developed and shared for reproducibility [Q6]. The dataset
received IRB approval with informed consent from students and guardians [Q95].

A key validity concern for cross-country deployment: all annotators appear to be
Qatar-based Arabic educators trained on the QUTC CAST rubric. The paper does not
document whether annotators represented diverse Arab-country backgrounds (Egyptian,
Levantine, North African), meaning implicit Gulf-curriculum expectations may be embedded
in the ground-truth labels. The user's elicitation affirms that pan-Arab MSA standards
reduce this concern for surface linguistic quality, but evaluative judgments on style,
development, and organization may still carry Qatari curricular norms.

### Output Form
The primary evaluation metric for all benchmarking experiments is Quadratic Weighted
Kappa (QWK), measuring agreement between human and model scores [Q58], consistent with
its use for IAA measurement [Q44]. Prompt-specific experiments use 5-fold cross-validation
with stratified 70/10/20 train/dev/test splits [Q52]; hyperparameters are tuned via
Bayesian optimization (Optuna TPESampler, 20 trials, fixed seed [Q59, Q60, Q61]).
Model selection is based on average QWK on the development set [Q61]. LLM experiments
were repeated three times with different random seeds to account for variability [Q189],
and holistic LLM scores were computed as the sum of individual trait scores [Q182].

All model outputs are discrete point-score labels. The benchmark does not evaluate
confidence calibration, uncertainty quantification, score-range prediction, or rationale
generation. The QWK metric captures ordinal agreement with human annotation but does
not assess whether a system can communicate uncertainty to a teacher user. For the
teacher-facing deployment scenario — where the system must flag essays falling between
levels and provide justification — the benchmark's output form is mismatched with the
required deployment output form. The benchmarking experiments cover both prompt-specific
and cross-prompt setups [Q14, Q83], and experiments were run on NVIDIA RTX A6000 and
NVIDIA A10 GPU hardware [Q140].


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
| Q9 | 1 | input_content | "IRB Number: QU-IRB 159/2024-EA" |
| Q10 | 1 | input_ontology | "Arabic AES research faces a significant data scarcity problem, as publicly available annotated datasets remain limited." |
| Q11 | 1 | input_ontology | "Existing Arabic resources are often small in scale such as QAES (Bashendy et al., 2024), lack trait-specific annotations as in ZAEBAC (Habash and Palfreyman, 2022), or consist solely of unannotated essays such as ALC." |
| Q12 | 2 | input_form | "Table 2: Comparison of LAILA with existing essay datasets. "Len" is average essay length in words; "HOL" indicates holistic scoring; "Eur" covers German, Italian, and Czech; "L1/L2" denotes native or second-language learners; "Public" here means freely available." |
| Q13 | 2 | output_ontology | "tailed trait-specific annotations that capture multiple dimensions of writing proficiency." |
| Q14 | 2 | input_ontology | "We establish baseline AES results for Arabic under two evaluation setups: prompt-specific and cross-prompt." |
| Q15 | 2 | output_form | "We publicly release LAILA, including essays with holistic and trait-specific annotations. We also release the benchmarking code to support replication and future research." |
| Q16 | 2 | input_ontology | "Section 2 reviews related work and existing AES datasets. Section 3 outlines the data collection design principles, while Section 4 describes the dataset construction process, including school and prompt selection, essay collection, and annotations." |
| Q17 | 2 | input_content | "Research on AES has advanced considerably in English, supported by large-scale, publicly available datasets such as ASAP/ASAP++ (Mathias and Bhattacharyya, 2018), TOEFL11 (Blanchard et al., 2013), ELLIPSE (Crossley et al., 2023a), and PERSUADE (Crossley et al., 2023b)." |
| Q18 | 2 | input_ontology | "In contrast, other languages have far fewer resources. Some smaller datasets exist, including ACEA (Chinese; annotated but not public) (He et al., 2022), TCFLE-8 (French; public but with only holistic scores) (Wilkens et al., 2023), and MERLIN (German, Italian, and Czech; public but limited to holistic annotations) (Boyd et al., 2014). While useful for AES studies, their limited scale and annotation depth restrict their utility." |
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
| Q38 | 6 | input_content | "LAILA comprises 7,859 essays collected across 8 distinct prompts: 3 explanatory and 5 persuasive (3,446 and 4,413 essays, respectively)." |
| Q39 | 6 | input_form | "Table 3 shows that the number of essays per prompt ranges from 500 to 1,181. Essay lengths demonstrate consistency across prompts, with an average of 171 words and a maximum of 706 words." |
| Q40 | 6 | output_ontology | "Most traits follow a near-normal pattern on the 6-point scale, indicating overall positive essay quality. The REL scores show that 86% of the essays agree strongly with the prompt. In contrast, GRA and VOC show the highest percentage of score 1 at 16%, followed by MEC at 13%, highlighting that these traits pose the greatest challenges." |
| Q41 | 6 | output_content | "To ensure consistency, 2 supervisors developed an annotation guidebook with detailed terminology, exemplars, and annotated practices for each prompt type. Annotators were required to review these materials and complete training sessions before formal annotation. Moderation sessions followed, where discrepancies were discussed and interpretations of the rubric were harmonized." |
| Q42 | 6 | output_content | "The scoring process was conducted using the Assessment Gourmet Platform, which supports large-scale, anonymized essay scoring. The platform ensured that annotators were blinded to student identity [D6], while only supervisors had access to annotator metadata for monitoring purposes." |
| Q43 | 6 | output_content | "The essays were randomly distributed among the annotators to minimize systematic bias, and the scoring sessions were capped to prevent annotators' fatigue. Each essay was independently scored by two annotators across all traits. If the difference in HOL scores between the two annotators was less than 6 points, the mean of the two scores was computed and then rounded down to the nearest integer; this rounded value was adopted as the final score for each trait. However, essays with large discrepancies between annotators (≥ 6 points difference in the HOL score) were flagged and escalated to a supervisor (a third annotator in this case), who provided the final adjudicated score and offered feedback to the annotators to improve alignment and consistency in subsequent batches of essays." |
| Q44 | 6 | output_content | "We compute IAA using Quadratic Weighted Kappa (QWK) (Williamson et al., 2012) to assess agreement between the two main annotators (A1 and A2), prior to adjudication. Table 4 reports QWK per trait and prompt, with agreement strength following Landis and Koch (1977). Overall, IAA was substantial across prompts, with an average QWK ranging from 0.66 (P5) to 0.75 (P1), showing strong consistency." |
| Q45 | 6 | output_content | "However, variability emerges by prompt and trait. In particular, P5 showed the lowest average agreement, noting that it has the highest percentage of essays that require a third annotator (A3: 23.3%; Table 3). This suggests greater initial disagreement" |
| Q46 | 7 | input_ontology | "For each setup, we investigate two research questions in the context of Arabic AES: (RQ1) how do different categories of models compare in overall performance?, and (RQ2) which models achieve the best results across individual traits?." |
| Q47 | 7 | input_ontology | "Model Selection We selected a diverse set of models with varying architectures to establish strong baselines for LAILA. The selection criteria included code availability, ease of implementation, and coverage of SOTA Arabic and English models." |
| Q48 | 7 | input_ontology | "The models fall into three categories: feature-based (FB), encoder-based, and large language models (LLMs). LLMs were evaluated in zero-shot and few-shot settings, and all models followed a multitask setup predicting holistic and trait scores jointly." |
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
| Q77 | 9 | output_form | "Overall, the findings of the benchmarking experiments above highlight the need to prioritize future research on cross-prompt AES, which is practically closer to the real world, while best models are still far from human performance." |
| Q78 | 9 | input_content | "While research on automated scoring of English essays began more than 55 years ago, Arabic essay scoring is hindered by the lack of data resources." |
| Q79 | 9 | input_content | "To bridge this gap, this paper introduced LAILA, the first large-scale publicly available dataset for Arabic AES." |
| Q80 | 9 | input_content | "The dataset comprises 7,859 essays written on 8 different prompts by 4,372 high school students, and provides annotations for 7 writing traits as well as a holistic score with substantial inter-annotator agreement." |
| Q81 | 9 | input_content | "This makes it a comprehensive and reliable resource for training models and evaluating writing quality of Arabic essays." |
| Q82 | 9 | output_content | "For reproducibility, we detailed the data collection and annotation process." |
| Q83 | 9 | output_form | "We also benchmarked LAILA using SOTA Arabic and English AES models in both prompt-specific and cross-prompt settings, showing strong baselines for future research." |
| Q84 | 9 | output_content | "We heartily thank our dedicated annotators for their contributions and express our gratitude to Qatar University Testing Center, the Ministry of Education and Higher Education in Qatar (the Arabic Section of the Department Of Educational Supervision in particular), participating schools, and students for making this work possible." |
| Q85 | 9 | output_content | "We also acknowledge the support of Advanced Group for Information Technology (AGI) for providing access to the platform, Assessment Gourmet, which was used to manage and administer the annotation process." |
| Q86 | 9 | input_content | "This work was made possible by NPRP grant NPRP14S-0402-210127 from the Qatar Research Development and Innovation (QRDI) Council." |
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
| Q116 | 12 | input_form | "An English-translated version of the CAST rubric is presented in Table 6." |
| Q117 | 13 | output_ontology | "Note: A score of 0 is assigned if the student does not attempt the task, provides a response that falls below the performance level described for score 1, or submits content that is not relevant to the topic of the given prompt." |
| Q118 | 13 | output_ontology | "Table 6: CAST Persuasive/Argumentative Writing Rubric - English Translation (Bashendy et al., 2024)." |
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
| Q147 | 16 | input_ontology | "The AES task is formulated as a text generation problem, where the model predicts the trait scores sequentially." |
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
| Q163 | 17 | output_form | "These configurations were considered better suited to the dataset, mitigating training instabilities." |
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
| Q181 | 18 | input_ontology | "In the zero-shot setting, the LLM is tasked with generating trait scores in JSON format, given the prompt text, essay, and trait rubrics." |
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
name: 'Arab-Country G10–12 Arabic Teachers: AI Essay Grading Assistance'
abbreviation: arab-hs-arabic-teachers-aes
benchmark: laila
deployment_scope:
  description: High school Arabic language teachers (grades 10–12) across Arab countries
    who use an AI system to assist in grading student essays written in Modern Standard
    Arabic (MSA). The benchmark dataset (LAILA) was collected in Qatar; the deployment
    population extends to Egypt, Saudi Arabia, Jordan, Lebanon, Morocco, and other
    Arab-country contexts. The system grades essays against a seven-trait rubric (Relevance,
    Organization, Vocabulary, Style, Development, Mechanics, Grammar) derived from
    the Qatar University Testing Center's CAST rubric.
  benchmark_source_country: Qatar
  deployment_countries:
  - Qatar
  - Egypt
  - Saudi Arabia
  - Jordan
  - Lebanon
  - Morocco
  - Algeria
  - Tunisia
  - UAE
  - Other Arab League member states
  geographic_scope_note: Qatar is the benchmark source context; deployment extends
    pan-Arab. Sub-national and country-level variation in curriculum and grading practice
    is explicitly relevant to validity assessment.
target_population:
  occupation: High school Arabic language teachers
  grade_levels_served: Grades 10–12
  role_description: Teachers assign and grade student MSA essays as part of formal
    Arabic language instruction. In the AI-assisted deployment, the system produces
    per-trait scores and justification text; the teacher reviews, overrides, and provides
    feedback to students.
  estimated_population_size: '[NEEDS VERIFICATION — deferred: below search budget;
    total number of G10–12 Arabic language teachers across target Arab countries not
    retrievable from standard sources within budget]'
  typical_professional_background: Undergraduate or postgraduate degree in Arabic
    language, linguistics, or Arabic literature; national teaching certification;
    professional experience in secondary Arabic instruction
  professional_certification_requirements: '[NEEDS VERIFICATION — deferred: per-country
    teacher certification standards for secondary Arabic require ministry-level documentation
    not retrievable within budget; e.g., Egypt''s Naqabat al-Mu''allimin, Saudi Arabia''s
    Teaching Permit, Jordan''s Ministry of Education licensing]'
  familiarity_with_rubric_based_grading: 'Highly variable: teachers in Qatar, Saudi
    Arabia, Jordan, and UAE tend to use structured rubrics; Egyptian teachers predominantly
    use holistic, evaluator-dependent grading without a formal trait structure'
  digital_literacy_level: Highly variable by country and sector. UAE teachers lead
    the Gulf and the world with ~75% actively using AI tools (OECD TALIS 2024 — [WEB-1]).
    Saudi Arabia shows strong national LMS infrastructure (Madrasati, deployed to
    all public K-12 schools), but only ~30% of teachers have received formal AI tool
    training as of recent estimates (Ken Research 2025 — [WEB-2]);
    a study of Saudi early childhood education found AI-based assessment tool use
    at only 8% in public schools vs. 52% in private schools (Qubahan Academic Journal
    2026 — [WEB-3]). No comparable
    survey data found for Egypt, Jordan, Lebanon, or Morocco; those countries should
    be treated as having lower digital readiness than Gulf states.
  language_of_professional_practice: Modern Standard Arabic (primary instructional
    and assessment medium); national spoken Arabic dialect for classroom communication
languages:
  assessment_language: Modern Standard Arabic (MSA / الفصحى)
  register_note: Essays are written in MSA; teachers evaluate MSA writing quality.
    No dialectal variation in the written essay text is expected by design, though
    student interference from regional dialects (Darija, Egyptian Arabic, Levantine
    Arabic) may appear in mechanics and vocabulary errors.
  teacher_interface_language: '[NEEDS VERIFICATION — deferred: whether the AI system
    interface is delivered in MSA, a regional dialect, or a European language such
    as French for North African users; this requires deployment-specific documentation
    not available in open sources]'
  dialectal_interference_risk_countries:
  - country: Morocco
    dialect: Darija (Moroccan Arabic) with heavy French and Berber substrate
    interference_traits_at_risk:
    - Mechanics
    - Vocabulary
    notes: '[NEEDS VERIFICATION — deferred: empirical evidence of Darija/French interference
      patterns in Moroccan student MSA writing; likely unsearchable (lived practice);
      no published Arabic AES study documenting this differential was found in searches]'
  - country: Egypt
    dialect: Egyptian Arabic
    interference_traits_at_risk:
    - Vocabulary
    - Grammar
    notes: '[NEEDS VERIFICATION — deferred: evidence of Egyptian colloquial interference
      in G10–12 MSA essay writing; likely unsearchable (lived practice); no published
      Arabic AES study documenting this differential was found in searches]'
  - country: Lebanon
    dialect: Levantine Arabic with French substrate
    interference_traits_at_risk:
    - Vocabulary
    - Mechanics
    notes: '[NEEDS VERIFICATION — deferred: evidence of French-mediated interference
      in Lebanese student MSA; likely unsearchable (lived practice)]'
  writing_system: Arabic script (right-to-left); standard MSA orthography
  nlp_tooling_note: Arabic NLP tooling (tokenization, morphological analysis, POS
    tagging) is improving but lags behind English; MSA is better resourced than dialectal
    Arabic. Tools used in LAILA baselines include AraBERT, AraT5, CamelTools, AraVec.
country_level_curriculum_variation:
  overview: Each Arab country operates an independent national Arabic language curriculum
    with distinct grading conventions. The LAILA seven-trait ontology (QUTC CAST rubric)
    was designed for the Qatari context and has not been formally mapped to other
    national frameworks.
  countries:
  - country: Qatar
    curriculum_authority: Ministry of Education and Higher Education (MOEHE Qatar)
    grading_approach: Structured rubric-based; CAST rubric used at Qatar University
      Testing Center; traits align with LAILA schema
    rubric_alignment_with_laila: High — LAILA was built on QUTC CAST rubric
    known_trait_mismatches: None documented
    official_rubric_documentation: '[NOT FOUND — searched for public MOEHE Qatar secondary
      Arabic writing assessment rubric; the CAST rubric is documented within the LAILA
      paper itself (Table 6, English translation) but no separate publicly accessible
      ministry URL was found. Source: LAILA paper pp. 12–13]'
  - country: Egypt
    curriculum_authority: Ministry of Education and Technical Education (MOETE); curriculum
      development overseen by the Curriculum and Instructional Materials Development
      Center (CCIMD). A General Framework for General and Technical Education Curricula
      2018/2030 was issued by CCIMD (Education 2.0 Project — [WEB-4]).
    grading_approach: Largely holistic and points-based at the subject level. The
      Thanaweya Amma (Grade 12 national exam) evaluates Arabic as part of five core
      subjects, each out of 100 marks; as of 2024/2025 the structure is 85% multiple-choice
      and 15% essay-style responses with no published multi-trait rubric (Grokipedia/academic
      grading Egypt — [WEB-5]).
      No formal multi-trait essay scoring rubric analogous to LAILA's CAST structure
      has been documented in Egyptian secondary Arabic assessment.
    rubric_alignment_with_laila: Low — the seven-trait ontology has no direct equivalent
      in Egyptian classroom practice; the IO mismatch is flagged as HIGH priority
      in the elicitation
    known_trait_mismatches: All seven traits potentially unmapped; holistic score
      is the operative construct
    official_rubric_documentation: '[NOT FOUND — searched Egyptian MOE (moe.gov.eg)
      and CCIMD for secondary Arabic essay grading guidelines; no public multi-trait
      rubric document found. The Thanaweya Amma Arabic exam is primarily knowledge-based
      (literary analysis, grammar) rather than free-composition trait-scored]'
    validated_arabic_aes_work: '[NOT FOUND — no study was found documenting Arabic
      AES validation against Egyptian national curriculum grading practices specifically;
      the AR-AES dataset (arXiv 2407.11212 — [WEB-6])
      uses undergraduate essays from diverse courses, not Egyptian secondary curriculum]'
  - country: Saudi Arabia
    curriculum_authority: Ministry of Education Saudi Arabia; standardized assessment
      conducted by the National Center for Assessment (Qiyas/ETEC), established by
      Royal Decree and restructured in 2017 under ETEC (Education and Training Evaluation
      Commission — [WEB-7]; Saudipedia — [WEB-8]).
    grading_approach: Qiyas administers a Standardized Test of Arabic Language Skills
      for native speakers as part of its language testing portfolio, focusing on listening,
      reading, and writing using standard Arabic (Wikipedia/NCAHE — [WEB-9]).
      Secondary classroom Arabic assessment details are set by MOE; structured rubric
      use exists at the assessment-center level, but public documentation of a seven-trait
      essay rubric for secondary classroom use was not found.
    rubric_alignment_with_laila: '[NOT FOUND — no public Saudi MOE secondary Arabic
      writing rubric mapping to REL, ORG, VOC, STY, DEV, MEC, GRA traits was found;
      Qiyas focuses on higher-education entry testing rather than G10–12 classroom
      essay rubrics]'
    known_trait_mismatches: '[NEEDS VERIFICATION — deferred: requires access to Saudi
      MOE internal curriculum documents; not publicly available]'
    official_rubric_documentation: '[NOT FOUND — searched etec.gov.sa and Saudi MOE
      for secondary Arabic essay grading rubric; no publicly accessible multi-trait
      rubric document found]'
  - country: Jordan
    curriculum_authority: Ministry of Education Jordan; the Tawjihi (General Secondary
      Education Certificate Examination) is administered by the Ministry and is Jordan's
      national high school exit exam. As of 2024–2025, restructured as a two-year
      program covering Grades 11–12, with Arabic as a mandatory common subject (Wikipedia/Tawjihi
      — [WEB-10]; ACEI — [WEB-11]).
    grading_approach: Tawjihi Arabic exam covers reading, grammar, and literary analysis;
      essay-writing components exist but public documentation of a multi-trait analytical
      rubric was not found. The exam is nationally standardized and high-stakes (scores
      determine university admission), suggesting centralized marking schemes, but
      no publicly available trait-based Arabic writing rubric was located.
    rubric_alignment_with_laila: '[NOT FOUND — no public Tawjihi Arabic essay marking
      scheme mapping to LAILA''s seven traits was found; the Tawjihi Arabic section
      emphasizes literary comprehension and grammar rather than trait-scored free
      composition]'
    known_trait_mismatches: '[NEEDS VERIFICATION — deferred: requires access to Jordanian
      MOE internal marking guidelines; not publicly available]'
    official_rubric_documentation: '[NOT FOUND — searched Jordanian MOE and Tawjihi
      exam resources; no public multi-trait Arabic writing rubric document found]'
  - country: Lebanon
    curriculum_authority: Lebanese Ministry of Education and Higher Education; curriculum
      development historically through Centre de Recherches et de Développement Pédagogiques
      (CRDP).
    grading_approach: '[NEEDS VERIFICATION — deferred: official Lebanese Baccalaureate
      Arabic essay grading method and French curriculum influence on rubric design;
      CRDP documentation not publicly accessible in English or Arabic online]'
    rubric_alignment_with_laila: '[NEEDS VERIFICATION — deferred: whether CRDP Arabic
      writing criteria map onto seven LAILA traits; requires expert elicitation or
      access to Lebanese curriculum documents]'
    known_trait_mismatches: '[NEEDS VERIFICATION — deferred: possible differences
      in ''style'' and ''development'' given Levantine rhetorical traditions; likely
      unsearchable (lived practice)]'
    official_rubric_documentation: '[NEEDS VERIFICATION — deferred: below search budget]'
  - country: Morocco
    curriculum_authority: Ministère de l'Éducation Nationale du Maroc; Arabic language
      curriculum under national framework.
    grading_approach: '[NEEDS VERIFICATION — deferred: Morocco Baccalaureate Arabic
      writing assessment method and French curriculum influence on trait structure;
      requires access to Moroccan MOE documents not available in open sources]'
    rubric_alignment_with_laila: '[NEEDS VERIFICATION — deferred: whether Moroccan
      national Arabic writing rubric uses comparable trait dimensions; below search
      budget]'
    known_trait_mismatches: '[NEEDS VERIFICATION — deferred: possible divergence in
      Vocabulary and Mechanics scoring given Darija and French substrate; likely unsearchable
      (lived practice)]'
    official_rubric_documentation: '[NEEDS VERIFICATION — deferred: below search budget]'
grading_ontology_notes:
  laila_trait_schema:
    traits:
    - Relevance (REL)
    - Organization (ORG)
    - Vocabulary (VOC)
    - Style (STY)
    - Development (DEV)
    - Mechanics (MEC)
    - Grammar (GRA)
    rubric_source: Qatar University Testing Center CAST rubric
    scale: 'REL: 0–2; all other traits: 0–5; Holistic = sum of seven traits'
    genre_coverage: Explanatory and persuasive only; narrative and descriptive genres
      absent
  pan_arab_standards_assessment: The deployment user considers pan-Arab MSA writing
    standards sufficiently uniform that a single scoring standard is appropriate;
    cross-country surface linguistic quality differences are not expected to be substantial.
    However, evaluative judgments on Style, Development, and Organization may carry
    implicit Gulf-curriculum expectations from Qatari annotators.
  holistic_vs_trait_tension: Egypt and potentially other countries rely on holistic
    grading; the seven-trait structure may impose an unfamiliar cognitive framework
    on teachers and produce output categories that do not correspond to their professional
    grading schema. Egypt's Thanaweya Amma Arabic exam (the national high-stakes exit
    assessment) is structured around subject-level percentage scores with no documented
    multi-trait essay rubric (Grokipedia — [WEB-5]).
  io_mismatch_severity: HIGH — documented explicitly in elicitation; Egypt is the
    clearest case but other countries may de-emphasize or re-weight specific traits
  genre_gap: The LAILA benchmark covers only explanatory and persuasive essays. National
    curricula may require narrative or descriptive essays; scoring models trained
    on LAILA may not generalize to these genres.
  genre_distribution_by_country: '[NEEDS VERIFICATION — deferred: proportion of narrative,
    descriptive, argumentative, and explanatory essay tasks in G10–12 Arabic curricula
    of Egypt, Saudi Arabia, Jordan, Lebanon, Morocco; requires access to national
    curriculum documents; below search budget]'
content_domain_notes:
  benchmark_content_origin: All LAILA essays respond to prompts designed for a Qatari
    educational context; all prompts are culturally relevant to the Arabic-speaking
    context broadly but grounded in Qatari institutional design
  cross_national_content_risk: Models trained on LAILA may systematically misjudge
    Relevance and Development scores for essays responding to prompts grounded in
    non-Qatari national history, literary canon, or social norms. This is flagged
    as a HIGH-priority IC gap.
  content_domains_at_risk:
  - country: Egypt
    at_risk_domains:
    - Egyptian national history (Pharaonic, Islamic, modern)
    - Egyptian literary canon (Naguib Mahfouz, Taha Hussein, etc.)
    - Nile Valley social norms and values
    notes: '[NOT FOUND — no study documenting LAILA-trained model misjudgment on Egypt-specific
      essay prompts was found; this cross-national content degradation test has not
      been conducted in the published literature as of searches conducted May 2026]'
  - country: Lebanon
    at_risk_domains:
    - Levantine literary traditions (Gibran Khalil Gibran, Arabic Nahda literature)
    - Lebanese civil conflict history
    - Pluralist religious and political identity
    notes: '[NOT FOUND — no published evidence found; see Egypt note above]'
  - country: Morocco
    at_risk_domains:
    - Maghrebi history and Amazigh cultural heritage
    - Francophone intellectual tradition in Moroccan education
    - North African Islamic scholarly tradition
    notes: '[NOT FOUND — no published evidence found; see Egypt note above]'
  - country: Saudi Arabia
    at_risk_domains:
    - Gulf social norms and Islamic values in Vision 2030 context
    - Arabian Peninsula history and tribal heritage
    - Saudi national literary figures
    notes: '[NOT FOUND — no published evidence found; interestingly, the Gulf curriculum
      context is closest to LAILA''s Qatari origin, so this risk is lower than for
      Egypt or Morocco]'
  laila_genre_limitations: LAILA does not include narrative or descriptive essay prompts;
    these genres are present in multiple Arab national curricula and represent an
    untested content domain for LAILA-trained models
output_requirements_notes:
  benchmark_output_form: Discrete point-score labels per trait; QWK-evaluated; no
    uncertainty quantification, confidence intervals, or natural-language rationale
  deployment_output_requirement: Per-trait score with accompanying confidence signal
    and explanatory justification text so teachers can meaningfully intervene when
    essays fall between score levels
  mismatch_severity: HIGH — the benchmark output form does not satisfy the teacher-facing
    use case; this is flagged as both an OO and OF high-priority gap
  uncertainty_output_gap: 'No Arabic AES system built on LAILA or comparable Arabic
    datasets has been documented with uncertainty quantification or rationale generation
    as of searches conducted May 2026. The broader AES field has active work on rationale-driven
    scoring: the Rationale-based Multiple Trait Scoring (RMTS) framework integrates
    LLM-generated trait-specific rationales into scoring (ResearchGate/RMTS — [WEB-12]),
    and the self-explainable RaDME system generates trait scores with co-produced
    rationales using knowledge distillation (arXiv 2502.20748 — [WEB-13]).
    These are English-language systems; no Arabic-language adaptation with teacher
    evaluation has been documented.'
  rationale_generation_approaches: 'Current state of the art in AES explainability
    (English-focused) includes: (1) Chain-of-Thought prompting with rubric-aligned
    reasoning (QwenScore+, Preprints.org 2025 — [WEB-14]);
    (2) LLM-agent trait-wise rationale generation feeding a smaller scoring model
    (RMTS); (3) knowledge distillation from teacher LLM to student model with co-generated
    rationale (RaDME, arXiv 2502.20748 — [WEB-13]).
    None of these approaches have been applied to the Arabic LAILA or TAQEEM datasets
    as of May 2026. TAQEEM 2025 shared task used Chain-of-Thought prompting with GPT
    variants on Arabic essays but focused on scoring accuracy, not rationale output
    (ACL Anthology — [WEB-15]).'
  teacher_acceptance_of_ai_scores: 'Direct evidence on Arab secondary Arabic teachers''
    acceptance of AI-generated essay scores is not available. Adjacent evidence: a
    survey of 792 UAE Grade 5–12 teachers found that trust in AI-EdTech correlated
    with perceived ownership and workload benefits (Springer/IJAIED 2024 — [WEB-16]);
    a UAE study (n=83 Abu Dhabi science teachers) found AI acceptance associated with
    perceived benefits and ease of use. Approximately 45% of Saudi teachers express
    concerns about transitioning to AI-driven approaches due to fears of losing classroom
    control (Ken Research 2025 — [WEB-2]).
    No study specific to Arabic language teachers and essay-scoring AI was found.'
annotator_pool_notes:
  documented_composition: 6 annotators and 3 supervisors; all Arabic language teachers
    or lecturers; 5 hold MSc or PhD in Arabic language; based at Qatar University;
    trained on QUTC CAST rubric
  nationality_diversity: '[NOT FOUND — searched for LAILA annotator nationality documentation;
    the LAILA paper (arXiv/ACL 2024) does not document annotator nationalities. The
    paper notes that Qatar''s large Arab expatriate population mitigates student-writer
    diversity concerns but makes no parallel claim for annotators. No supplementary
    material documenting annotator backgrounds was found.]'
  gulf_curriculum_bias_risk: MODERATE — Qatari annotator pool may embed implicit Gulf-curriculum
    expectations in holistic judgments on Style, Development, and Organization; acknowledged
    in elicitation as warranting verification rather than dismissal. The absence of
    annotator nationality documentation means this risk cannot be resolved without
    direct inquiry to the LAILA authors.
  iaa_range: QWK 0.66 (P5) to 0.75 (P1); classified as substantial agreement; highest
    escalation rate on P5 (23.3% required third annotator)
infrastructure_notes:
  modality: Text-only MSA; no audio, image, or multimodal components
  deployment_interface: '[NEEDS VERIFICATION — deferred: web-based, LMS-integrated,
    or standalone application; specific platform names or ministry-endorsed systems;
    requires deployment-specific documentation]'
  internet_access_by_country:
    Qatar: '[NEEDS VERIFICATION — deferred: broadband/mobile penetration for school
      teachers; Qatar has near-universal internet access nationally but school-teacher-specific
      figures below search budget]'
    Egypt: '[NEEDS VERIFICATION — deferred: school internet connectivity rates; urban
      vs. rural teacher access; Egypt has significant urban-rural digital divide]'
    Saudi Arabia: Saudi Arabia deployed the Madrasati LMS to all public K-12 schools
      during COVID-19, achieving 92% student attendance via the platform (Rowad Al
      Khaleej — [WEB-17]).
      The platform is described as 'relatively peerless' among nationally developed
      LMS solutions globally (OLC/NELC 2021 — [WEB-18]).
      However, nationwide broadband infrastructure expansion remains a recommendation,
      suggesting rural connectivity gaps.
    Jordan: '[NEEDS VERIFICATION — deferred: Jordan school internet connectivity;
      below search budget]'
    Lebanon: '[NEEDS VERIFICATION — deferred: Lebanon infrastructure disruption context
      makes this particularly important but also particularly variable; below search
      budget]'
    Morocco: '[NEEDS VERIFICATION — deferred: below search budget]'
  device_access: '[NEEDS VERIFICATION — deferred: tablet/laptop/desktop prevalence
    among G10–12 Arabic teachers in target countries; Saudi Arabia data above suggests
    gaps even in a well-resourced Gulf context; Egypt, Jordan, Lebanon, Morocco likely
    worse]'
  infrastructure_mismatch_severity: LOWER — deployment is text-only MSA matching benchmark
    modality; no script mismatch or modality gap anticipated per elicitation
  lms_integration_context: 'Saudi Arabia: Madrasati LMS is the national K-12 platform
    deployed to all public schools, developed by the Saudi Ministry of Education (ResearchGate/Madrasati
    — [WEB-19]).
    Future Madrasati development plans include AI tool integration (Education Saudi
    — [WEB-20]).
    Egypt, Jordan, Lebanon, Morocco: no equivalent national K-12 LMS was identified
    in searches; integration pathway for AI grading tools in these countries is less
    defined.'
regulatory_and_policy_notes:
  data_protection:
    Qatar: Qatar Law No. 13 of 2016 (Personal Data Privacy Protection Law, PDPPL)
      applies to all personal data processed electronically within Qatar. Qatar was
      the first GCC country to enact a comprehensive national data privacy law. The
      PDPPL establishes data subject rights, purpose limitation, and data minimization
      principles; special categories of data (including children's data) require authority
      approval for processing. Supplementary guidelines were issued by the Ministry
      of Transport and Communications in 2021. Student essay data processed by an
      AI grading system would fall within scope. (Securiti — [WEB-21];
      DLA Piper — [WEB-22];
      official text — [WEB-23])
    Egypt: 'Egyptian Personal Data Protection Law No. 151 of 2020 — applicability
      to educational AI grading systems confirmed in principle (law covers electronically
      processed personal data) but specific educational sector guidance has not been
      published. [NEEDS VERIFICATION — deferred: whether Egypt''s Law 151/2020 has
      implementing regulations or educational-sector guidance relevant to AI grading;
      below search budget]'
    Saudi Arabia: 'Saudi Personal Data Protection Law (PDPL), enacted 2021 and effective
      2023, covers personal data processing. No specific educational AI grading guidance
      was found. [NEEDS VERIFICATION — deferred: specific PDPL applicability to student
      data in AI assessment contexts; below search budget]'
    Jordan: '[NEEDS VERIFICATION — deferred: Jordanian data protection framework applicability
      to educational AI; below search budget]'
    Lebanon: '[NEEDS VERIFICATION — deferred: Lebanese data protection legislation
      status; country has had a draft data protection law under discussion but no
      enacted comprehensive law as of last known status; below search budget]'
    Morocco: '[NEEDS VERIFICATION — deferred: Law No. 09-08 on personal data protection
      applicability; below search budget]'
  ai_in_education_policy:
    regional_overview: 'The UAE has the most advanced AI-in-education policy in the
      region: in May 2025, the UAE Ministry of Education announced a national AI curriculum
      for all public school students from KG to Grade 12 (UNESCO Courier — [WEB-24]).
      Saudi Arabia is integrating AI into K-12 and higher education through coordinated
      national frameworks under Vision 2030, led by the Ministry of Education, SDAIA,
      MCIT, and NELC (OnlineEducation.com — [WEB-25]).
      No ministerial guidance specifically addressing AI-assisted essay grading in
      secondary education was found for any target country.'
    Qatar: '[NEEDS VERIFICATION — deferred: MOEHE Qatar policy on AI tools in assessment;
      below search budget]'
    Saudi_Arabia: Saudi MOE has integrated AI into the national education strategy
      under Vision 2030 and plans to expand Madrasati with AI tools. Approximately
      60% of Saudi schools plan to implement AI-based tools (Ken Research 2025 — [WEB-2]).
      No specific policy on AI-assisted essay grading found.
    Egypt: '[NOT FOUND — no Egyptian MOE policy on AI-assisted grading found in searches]'
  laila_usage_restrictions: LAILA dataset is released for research and educational
    purposes only; explicitly prohibited for high-stakes educational decisions affecting
    individual students; systems developed using LAILA must undergo fairness auditing
    and stakeholder consultation before real-world application
  high_stakes_use_warning: The elicitation deployment scenario (assisting teacher
    grading of G10–12 essays) is proximate to high-stakes use; the benchmark's own
    ethics statement warns against deployment in operational assessment contexts without
    independent validation
cultural_and_professional_norms_notes: '- Arabic language teaching in Arab secondary
  schools carries significant cultural prestige; teacher authority over grading decisions
  is a professional norm that AI systems must position themselves as supporting rather
  than replacing.

  - In many Arab education systems, the Arabic language subject is identity-bearing
  and tied to national and Islamic cultural heritage; AI grading assistance may be
  received with heightened sensitivity.

  - Egypt''s holistic grading culture reflects a professional tradition where experienced
  teacher judgment is the authoritative standard; trait-based AI scores may be perceived
  as reductive or misaligned with professional identity.

  - Gulf-country teachers (Qatar, UAE, Saudi Arabia) may be more accustomed to rubric-based
  frameworks given standardized testing infrastructure (QUTC CAST, QIYAS, etc.).

  - In Lebanon and Morocco, French educational influence may shape teacher expectations
  about what structured writing assessment looks like, potentially creating both alignment
  and misalignment with LAILA''s trait schema.

  - Cross-country annotator trust: teachers may scrutinize whether the AI''s implicit
  scoring standard reflects their own national curriculum expectations rather than
  a Gulf-centric norm.

  - UAE teachers'' high AI adoption (~75% using AI tools per OECD TALIS 2024) contrasts
  with Saudi Arabia where ~45% of teachers express concerns about AI-driven approaches;
  this suggests the Gulf itself is not homogeneous in AI readiness.'
flagged_gaps_for_web_search:
- gap_id: 1
  label: Egypt holistic grading vs. LAILA seven-trait structure
  description: Egypt is a major Arab education system where essay grading is rubric-free
    and evaluator-dependent. No Arabic AES work has been documented as validated against
    Egyptian national curriculum grading practices.
  search_target: Arabic automated essay scoring Egypt national curriculum holistic
    grading validation rubric-free secondary Arabic
  search_outcome: 'SEARCHED — confirmed: Egypt''s Thanaweya Amma Arabic assessment
    uses holistic percentage scoring with no documented multi-trait rubric. No Arabic
    AES study validating against Egyptian curriculum grading was found. The AR-AES
    dataset (arXiv 2407.11212) covers undergraduate essays, not Egyptian secondary
    curriculum.'
- gap_id: 2
  label: Non-Qatari prompt content and cross-national relevance/development scoring
    degradation
  description: LAILA prompts are Qatari-context; models may misjudge Relevance and
    Development for essays on Egyptian history, Levantine literature, or North African
    social topics.
  search_target: LAILA Arabic AES cross-national prompt generalization Egypt Levant
    North Africa relevance development scoring degradation
  search_outcome: 'SEARCHED — not found: no study testing LAILA-trained models on
    non-Qatari prompt content was found. This cross-national content degradation test
    has not been conducted in the published literature.'
- gap_id: 3
  label: Confidence/uncertainty output and rationale generation for teacher use
  description: Benchmark produces only discrete scores; deployment requires confidence
    signals and explanatory justification. No Arabic AES system with uncertainty quantification
    or rationale generation has been documented.
  search_target: Arabic automated essay scoring uncertainty quantification confidence
    estimation rationale generation teacher feedback explainability
  search_outcome: 'SEARCHED — partially resolved: rationale generation is an active
    English-language AES research area (RMTS, RaDME, QwenScore+ frameworks all published
    2025). No Arabic-language adaptation with teacher evaluation has been documented.
    TAQEEM 2025 used CoT prompting for Arabic essay scoring but focused on accuracy,
    not rationale output.'
- gap_id: 4
  label: Country-level rubric documentation for Saudi Arabia, Jordan, Lebanon, Morocco
  description: Official rubric structures for secondary Arabic writing assessment
    in these four countries have not been mapped against LAILA's seven-trait schema.
  search_target: Arabic language essay grading rubric Saudi Arabia Jordan Lebanon
    Morocco national curriculum official assessment criteria secondary school
  search_outcome: 'SEARCHED — not found: no public multi-trait Arabic writing rubric
    was found for Saudi Arabia, Jordan, Lebanon, or Morocco. Saudi Arabia''s Qiyas
    focuses on higher-education entry testing. Jordan''s Tawjihi Arabic exam emphasizes
    literary comprehension and grammar rather than free-composition trait scoring.
    Lebanon and Morocco require expert elicitation.'
- gap_id: 5
  label: Annotator pool nationality diversity within Qatar
  description: LAILA annotator nationalities are undocumented; if exclusively Qatari-curriculum
    aligned, ground-truth labels may embed Gulf-curriculum norms.
  search_target: LAILA Arabic AES annotator nationality diversity Gulf curriculum
    bias Qatar University annotator background
  search_outcome: 'SEARCHED — not found: no documentation of LAILA annotator nationalities
    was found in the paper or any supplementary source. Risk remains unresolved; requires
    direct inquiry to LAILA authors.'
- gap_id: 6
  label: Dialectal interference in MSA mechanics and vocabulary scoring
  description: Morocco (Darija/French), Egypt (Egyptian Arabic), and Lebanon (Levantine/French)
    may produce MSA with distinct interference patterns; LAILA has not analyzed scoring
    differential by student dialect background.
  search_target: Arabic MSA essay scoring dialectal interference Moroccan Darija Egyptian
    Arabic Levantine vocabulary mechanics scoring bias high school
  search_outcome: 'NOT SEARCHED — deferred: low marginal information value given no
    published study was expected to exist on this specific intersection; confirmed
    unsearchable (lived practice).'
- gap_id: 7
  label: Genre coverage in Arab national curricula vs. LAILA (explanatory and persuasive
    only)
  description: LAILA excludes narrative and descriptive genres; prevalence of these
    genres in target national curricula is undocumented.
  search_target: Arabic essay genre distribution high school national curriculum Arab
    countries narrative descriptive argumentative writing task types G10–12
  search_outcome: 'NOT SEARCHED — deferred: below search budget; national curriculum
    genre distribution requires access to curriculum documents not available in open
    English-language sources.'
- gap_id: 8
  label: Teacher digital tool adoption and AI grading acceptance in Arab secondary
    schools
  description: No data has been cited on Arab secondary Arabic teachers' familiarity
    with AI grading tools or attitudes toward AI-generated scores.
  search_target: Arab secondary school teacher digital literacy AI grading acceptance
    automated essay scoring Arabic teacher survey
  search_outcome: 'SEARCHED — partially resolved: UAE teachers lead globally (~75%
    using AI, OECD TALIS 2024); Saudi Arabia shows ~30% formal AI training rate and
    ~45% resistance to AI-driven approaches. No Arab-country data specific to Arabic-subject
    teachers and essay-scoring AI was found. See digital_literacy_level and teacher_acceptance_of_ai_scores
    fields for details.'
net_new_fields:
  taqeem_2025_shared_task: TAQEEM 2025 (First Shared Task for Arabic Quality Evaluation
    of Essays in Multi-dimensions) was held at ArabicNLP 2025 (Suzhou, China, November
    2025). It introduced a new dataset of 1,265 Arabic essays annotated with holistic
    and the same seven trait-specific scores used in LAILA (REL, ORG, VOC, STY, DEV,
    MEC, GRA), with Task A on holistic scoring and Task B on trait-specific scoring.
    Eleven teams registered for Task A and 10 for Task B; 5 teams submitted runs.
    This is the first community benchmark for Arabic multi-trait AES beyond LAILA
    itself. Its dataset origin (non-Qatar) is not explicitly documented in available
    abstracts, which is relevant for cross-national validity. (ACL Anthology — [WEB-26])
  ar_aes_dataset_note: The AR-AES dataset (arXiv 2407.11212, published July 2024)
    provides an Arabic AES benchmark of 2,046 undergraduate essays from four diverse
    courses, including rubric-based evaluation guidelines and gender information.
    It differs from LAILA in being undergraduate-level and covering source-dependent
    essay questions rather than free MSA composition. AraBERT achieved the best performance;
    LLMs (including ACEGPT) reached QWK of 0.67. This dataset does not cover secondary-level
    MSA free composition and is not validated against any national Arabic secondary
    curriculum, but it is the closest Arabic AES resource outside LAILA with a rubric-based
    annotation schema. (arXiv — [WEB-6])
  explainable_aes_state_of_art: 'The broader AES field has developed several rationale-generation
    frameworks in 2025 that are relevant to the deployment''s OF gap: (1) RaDME (arXiv
    2502.20748) uses knowledge distillation to train a model that generates both trait
    scores and rationales without requiring LLMs at inference time; (2) RMTS uses
    LLM agents to generate trait-specific rationales that then feed a smaller scoring
    model; (3) QwenScore+ uses rubric-aware Chain-of-Thought prompting with RLHF.
    None have been applied to Arabic or to LAILA/TAQEEM. These frameworks represent
    actionable methodological paths for the deployment team to pursue, but none provide
    validated Arabic teacher-facing rationale output. (arXiv — [WEB-13];
    Preprints.org — [WEB-14])'
  saudi_madrasati_lms: Saudi Arabia's Madrasati ('My School') is the national K-12
    LMS deployed to all public schools (Grades 1–12) by the Ministry of Education;
    it achieved 92% student attendance and is described as 'relatively peerless' among
    nationally developed LMS solutions globally (OLC/NELC 2021 benchmarking). Future
    plans include AI tool integration. This is the most likely integration pathway
    for an AI grading tool in Saudi public schools. Teachers have reported usability
    issues and infrastructure gaps; a study of secondary teachers found usability
    insufficient for current needs. (ResearchGate — [WEB-19];
    IJIET 2025 — [WEB-27])
  qatar_pdppl_student_data: Qatar's PDPPL (Law No. 13 of 2016, effective 2017) applies
    to all electronically processed personal data within Qatar, including student
    essay data. It requires explicit consent for processing children's data, with
    guardian verification. The law is supplemented by 14 MOTC guidelines (2021) and
    NCSA/NCGAA enforcement guidance incorporating GDPR-aligned principles. Processing
    student essays through an AI grading system would require a clear lawful basis
    and likely constitutes processing of minors' data. Qatar was the first GCC country
    to enact a comprehensive national data protection law. (Almeezan official text
    — [WEB-23]; DLA Piper — [WEB-22])
  uae_ai_education_leadership: 'The UAE announced in May 2025 that all public school
    students from KG to Grade 12 would be taught AI as a formal subject beginning
    2025–2026, making the UAE among the first nations to integrate AI into the full
    school curriculum. Approximately 75% of UAE teachers actively use AI tools (OECD
    TALIS 2024), matched globally only by Singapore. This is directly relevant to
    deployment feasibility: UAE teachers are the most AI-ready segment of the deployment
    population. (UNESCO Courier — [WEB-24];
    AGBI — [WEB-1])'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.agbi.com/education/2025/10/uae-teachers-lead-world-in-classroom-ai-adoption/ |
| WEB-2 | https://www.kenresearch.com/saudi-arabia-ai-k12-education-market |
| WEB-3 | https://journal.qubahan.com/index.php/qaj/article/view/2111 |
| WEB-4 | https://edu2-egypt.com/curriculum-frameworks |
| WEB-5 | https://grokipedia.com/page/academic_grading_in_egypt |
| WEB-6 | https://arxiv.org/abs/2407.11212 |
| WEB-7 | https://etec.gov.sa/en/centers/qiyas |
| WEB-8 | https://saudipedia.com/en/article/571/government-and-politics/centers/the-national-center-for-assessment-qiyas |
| WEB-9 | https://en.wikipedia.org/wiki/National_Center_for_Assessment_in_Higher_Education |
| WEB-10 | https://en.wikipedia.org/wiki/Tawjihi |
| WEB-11 | https://acei-global.org/5-things-to-know-about-jordans-tawjihi-examination-a-gateway-to-higher-education/ |
| WEB-12 | https://www.researchgate.net/publication/382302599_Automated_essay_scoring_in_Arabic_a_dataset_and_analysis_of_a_BERT-based_system |
| WEB-13 | https://arxiv.org/html/2502.20748v1 |
| WEB-14 | https://www.preprints.org/manuscript/202504.2338 |
| WEB-15 | https://aclanthology.org/2025.arabicnlp-sharedtasks.135.pdf |
| WEB-16 | https://link.springer.com/article/10.1007/s40593-024-00433-x |
| WEB-17 | https://www.rowad-alkhaleej.edu.sa/en/online-learning-in-saudi-arabia/ |
| WEB-18 | https://olc-wordpress-assets.s3.amazonaws.com/uploads/2021/05/NELC-Phase-2-K-12-Report-Final-1.pdf |
| WEB-19 | https://www.researchgate.net/publication/356918598_Madrasati_e-learning_platform |
| WEB-20 | https://www.education-saudi.com/madrasati-saudi-digital-education-platform-vision-2030/ |
| WEB-21 | https://securiti.ai/qatar-personal-data-protection-law/ |
| WEB-22 | https://www.dlapiperdataprotection.com/countries/qatar/law.html |
| WEB-23 | https://www.almeezan.qa/EnglishLaws//132016.pdf |
| WEB-24 | https://courier.unesco.org/en/articles/ai-goes-school-united-arab-emirates |
| WEB-25 | https://www.onlineeducation.com/features/saudi-arabia-ai-and-online-learning |
| WEB-26 | https://aclanthology.org/2025.arabicnlp-sharedtasks.134/ |
| WEB-27 | https://www.ijiet.org/vol15/IJIET-V15N8-2367.pdf |

---

## Expert Elicitation

## Elicitation Responses

Q1 [OC]: The benchmark essays were scored by annotators in Qatar. For teachers in other Arab countries — such as Egypt, Saudi Arabia, Jordan, Lebanon, or Morocco — would you expect grading standards to differ meaningfully on traits like style, vocabulary, or development? For instance, would a Lebanese teacher apply different expectations for formal register or rhetorical organization than a Qatari one, and should the system's scoring reflect each country's local norms or a pan-Arab standard?
A1: Cross-country grading standards for MSA writing are not expected to differ significantly; the shared goal is well-formed MSA prose and the end product is indistinguishable by nationality. A pan-Arab standard is considered appropriate rather than country-specific norms.

Q2 [IO]: In your deployment, are teachers expected to grade essays on all seven trait dimensions, or do different countries or curricula emphasize a subset? Are there grading criteria important to teachers in target countries that might not be captured by these seven traits?
A2: Different countries may apply different grading criteria. Notably, Egypt does not use a structured rubric — grading is holistic and evaluator-dependent — meaning the seven-trait ontology may not map onto Egyptian classroom practice. Other countries may similarly de-emphasize or re-weight specific traits.

Q3 [OO]: Should the system produce a single score per trait or express uncertainty and provide justification when an essay falls between levels?
A3: The system should express confidence and provide explanatory justification alongside each score so teachers can intervene when essays fall between levels, rather than presenting a single authoritative label. Pure label output is insufficient for the deployment need.

Q4 [IC]: Could essay prompts and expected content knowledge differ enough across Arab countries — e.g., Egyptian history, Gulf social norms, Levantine literary traditions — that a model trained on Qatari prompts might misjudge relevance or development for locally grounded content?
A4: Yes, if the model is unfamiliar with locally grounded content knowledge (history, social norms, literary traditions specific to a non-Qatari context), it may misjudge relevance and development scores for essays written in response to prompts from other national curricula.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The seven-trait rubric ontology does not universally match national curricula — Egypt uses holistic, rubric-free grading — so the benchmark's trait structure may be irrelevant or incomplete for large segments of the target deployment population. |
| IC | HIGH | Benchmark essays use Qatari prompts and cultural/educational contexts; for teachers in Egypt, the Levant, or North Africa, locally grounded content (history, literary canon, social norms) may fall outside the model's training distribution, risking systematic misjudgment of relevance and development. |
| IF | LOWER | Deployment is text-only in MSA, matching the benchmark's modality and script; no infrastructure mismatch is anticipated. |
| OO | HIGH | The benchmark produces discrete trait scores/labels, but the deployment requires confidence estimates and explanatory justification alongside each score; the scoring output ontology as designed does not satisfy the teacher-facing use case. |
| OC | MODERATE | The user considers pan-Arab MSA standards sufficiently uniform to reduce annotator-population mismatch concerns, but Qatari annotators may still embed implicit Gulf-curriculum expectations in holistic judgments; this warrants verification rather than dismissal. |
| OF | HIGH | The benchmark outputs labels/scores, but teachers need uncertainty flagging and score-range or rationale output; the output form mismatch between benchmark and deployment is a direct validity threat for practical use. |

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
  "region": "Arab-Country G10–12 Arabic Teachers: AI Essay Grading Assistance",
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
