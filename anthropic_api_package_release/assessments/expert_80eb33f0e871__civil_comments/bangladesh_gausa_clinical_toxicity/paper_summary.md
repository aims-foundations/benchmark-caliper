```markdown
# Validity Extraction: Nuanced Metrics for Measuring Unintended Bias Against Identity Groups
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: Nuanced Metrics for Measuring Unintended Bias Against Identity Groups
- **Authors**: Daniel Borkan, Lucas Dixon, Jeffrey Sorensen, Nithum Thain, Lucy Vasserman
- **Venue/Year**: Not explicitly documented in registry (inferred from content as ~2019)
- **Total Pages**: 10
- **Quotes Extracted**: 81

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

### 1. Task Taxonomy / Test Case Categories

The benchmark's primary task is measuring *unintended bias* in toxicity classifiers — specifically, whether model performance degrades systematically when text mentions particular identity groups [Q13]. The evaluation is applied to two versions of the Perspective API's toxicity classifier, TOXICITY@1 and TOXICITY@6, where the latter was built using bias mitigation techniques [Q37, Q39]. Results are further stratified by comment length, with short comments (under 100 characters) broken out separately because the known bias mitigation effort between the two model versions specifically targeted short-form text [Q63].

From a deployment-context perspective, the task taxonomy is highly misaligned with the Gazipur use case. The benchmark assesses identity-group-linked bias in the context of *English-language online forum comments*, not health-query-induced toxicity. Categories such as son-preference gender discrimination embedded in a clinical chatbot prompt, superstition-encoded harmful health advice, or caste-coded language would fall entirely outside the scope of what these models and test cases were designed to detect or measure. The taxonomy provides no subtasks corresponding to implicit, contextually embedded toxicity of the type that would naturally arise in patient–chatbot interactions with low-literacy Bangladeshi users.

### 2. Data Sources and Collection

The benchmark draws on two principal test sets. First, a synthetic dataset of approximately 77,000 examples generated from identity-term templates, balanced at 50% toxic and 50% non-toxic across 50 identity terms [Q40, Q44], adapted from earlier work [Q75]. Second, a large human-labeled corpus of 1.8 million online comments sourced from online comment forums, with toxicity labels across all comments and identity labels on a subset of 450,000 [Q56, Q57], described as "one of the first studies of unintended bias based on identity references in text classification on real data" [Q76]. The dataset is to be released under a Creative Commons license to enable further research [Q60].

Both test sets are derived entirely from English-language online comment platforms [Q29, Q30]. There is no representation of Banglish, Roman-script Bangla, phonetically approximated Bangla, or health-domain conversational text. The 50 identity terms used in the synthetic set were manually curated [Q46] and reflect Western online-comment demographics; none of the identity groups relevant to the Gazipur deployment context — such as Muslim/Hindu inter-communal distinctions, caste categories, or colorism-coded language — are documented as present. The sourcing from online comment forums [Q56] further distances the corpus from the peri-urban, low-literacy, health-seeking interaction patterns of the target population.

### 3. Data Format and Preprocessing

The synthetic examples are constructed as simple, clearly toxic or clearly non-toxic sentences built around identity terms, explicitly designed so that toxicity judgment should not depend on the identity term present [Q41, Q42]. The real-data corpus is structured to allow separate analysis by comment length, with a threshold of 100 characters distinguishing "short" from "all" comments [Q62], and identity-labeled subgroups are restricted to those containing more than 100 short-comment examples to ensure statistical meaningfulness [Q64]. The identity label set was designed to balance coverage of identities, crowd rater accuracy, and sufficient example counts per identity [Q52].

From the deployment-context perspective (HIGH priority on IF), the format mismatch is severe. The benchmark assumes clean, standard English text — synthetic examples are deliberately "simple sentences" [Q42]. The Gazipur deployment will encounter systematically degraded input: Roman-script Bangla (Banglish), phonetic ASCII approximations of Bangla words, absent or erratic punctuation, and irregular spacing. No preprocessing pipeline documented in this benchmark is designed to handle such input, and the identity-detection annotations were performed on standard-form English text only. Toxic signals embedded in degraded, code-switched text would be structurally invisible to the data format assumptions underpinning this benchmark.

### 4. Label Categories and Output Types

The benchmark's core output label is a continuous toxicity score, with the ground-truth label for the real dataset derived from a four-point ordinal scale: "Very Toxic," "Toxic," "Hard to Say," and "Not Toxic" [Q54]. The authors acknowledge that toxicity is "an inherently complex and subjective classification task" defined as anything "rude, disrespectful, or unreasonable that would make someone want to leave a conversation" [Q2]. Subtypes of toxicity were also collected from raters but were not used in the analyses reported in this work [Q55].

This label ontology is critically misaligned with the Gazipur deployment on both IO and OO dimensions (both HIGH priority). The single-axis toxicity score does not distinguish health-context harmful content, son-preference discriminatory framing, religiously coded slurs (e.g., "malaun"), colorist remarks, or superstition-driven misinformation — categories that are operationally relevant to the target deployment. The definition of toxicity anchored to "making someone want to leave a conversation" [Q2] is itself culturally situated in the norms of English-language online discourse and may not generalize to the implicit, contextually embedded harms characteristic of health-oriented chatbot interactions in Bangladesh. The "Hard to Say" label [Q54] acknowledges annotator uncertainty but provides no mechanism for capturing the culturally specific judgment calls that would be required for Bangladeshi health-context toxicity.

### 5. Annotation Process

Identity labels were collected via crowd raters who were presented with comments and asked structured questions such as "What genders are referenced in the comment?" and "What races or ethnicities are referenced in the comment?", selecting from a provided list of identity options [Q47, Q48, Q49]. This approach was chosen specifically because "human labeling for identity content allows us to capture nuanced identity content" [Q50]. Some identity-labeled comments were preselected using models from previous identity-labeling iterations to ensure raters frequently encountered identity-relevant content [Q58]. Toxicity labels were collected using the same crowd rating guidelines published by the Perspective API [Q53].

From the Gazipur deployment perspective (HIGH priority on OC), the annotation process has a critical representativeness gap. The paper provides no documentation of annotator demographics, geographic origin, language background, or cultural expertise. Given that the source data is English-language online comments and the rating platform is a commercial crowdsourcing service [Q48], it is highly unlikely that any Bangladeshi or South Asian annotators with clinical or local cultural context participated. The deployment's elicitation guidance explicitly identifies native Bangladeshi annotators who understand local health, religious, and social context as the minimum viable standard — a bar this benchmark almost certainly does not meet. The provided identity category list [Q49] would not have included religiously coded South Asian slurs, caste terminology, or colorism-specific categories, meaning annotators had no mechanism to flag such content even if they encountered it. The high rating redundancy noted in the paper [Q6] mitigates noise but cannot compensate for systematic absence of regionally appropriate judgment.

### 6. Evaluation Metrics and Output Modality

The paper's central contribution is a suite of five threshold-agnostic metrics derived from ROC-AUC, Equality Gap, and Mann-Whitney U statistics [Q11], motivated by the observation that threshold-dependent metrics can "obscure the view of unintended bias and thus be misleading to practitioners" [Q8]. The fairness criterion is grounded in a definition similar to equality of odds: unintended bias is present when model performance varies across designated identity groups [Q5]. The three AUC-based metrics — Subgroup AUC, BPSN AUC, and BNSP AUC — each capture a different type of bias, with Subgroup AUC identifying poor within-group model understanding and BPSN/BNSP AUCs identifying score shifts relative to background data [Q31, Q32]. Two Average Equality Gap (AEG) metrics extend this by quantifying distributional bias even when perfect thresholding is theoretically achievable [Q33], with the Positive AEG defined as the area between the subgroup–background TPR curve and the identity line [Q22], and an analogous Negative AEG defined over true negative rates [Q23].

The threshold-agnostic design is methodologically sound and practically valuable: AUC is robust to class imbalances [Q17], and the metric suite is explicitly designed to be "robust to class imbalances in the dataset" and to provide "more nuanced insight into the types of bias present in the model" [Q16]. The metrics compare subgroup performance against "background" data rather than evaluating the subgroup in isolation [Q14], which improves robustness to real-world data skews [Q18, Q19]. Empirical application to the two Perspective API models confirms that the metrics reveal bias skewing non-toxic identity-mentioning comments toward toxicity scores [Q67, Q68, Q69], a finding that held across both models and comment lengths [Q70, Q71]. The Negative and Positive AEG metrics specifically capture directionality of score shifts [Q34], and their optimal value of 0 corresponds to equality of opportunity across all thresholds [Q26, Q27, Q28].

From a deployment-context perspective (MODERATE priority on OF), the output modality is broadly matched: both the benchmark and the Gazipur chatbot deployment use text-in, continuous-score-out pipelines. However, the score calibration, threshold assumptions, and group-comparison baselines were derived from English-language online comment distributions. Applied to Banglish or phonetic Bengali text, the underlying toxicity scores these metrics evaluate would themselves be unreliable — meaning the metric suite, however well-designed, would be measuring noise rather than meaningful toxicity signal. The metrics correctly flag that "the correct handling of subtle variations in distributions must be decided on a case by case basis" [Q35], which implicitly acknowledges that deployment-context distribution shifts require re-evaluation.

### 7. Stated Limitations

The authors explicitly acknowledge several categories of limitation. The assumption of reliable labels underlying the fairness metric framework is identified as significant and not universally valid [Q6]. Toxicity models are noted to reproduce societal biases, specifically mis-associating identity group names (such as "gay" and "Muslim") with toxicity [Q3], and these biases may stem from the demographic composition of the annotator pool, latent annotator biases, or sampling choices [Q4]. The identity label set is acknowledged as non-comprehensive and not universally representative [Q51], and synthetic test sets are recognized as limited to manually curated identity terms that are "unlikely to capture the true diversity of ways that identities are discussed in real conversation" [Q46]. Real data is noted to reveal more unintended bias than synthetic data, while also being noisier [Q65, Q66].

The paper flags several forward-looking research gaps that are directly relevant to the Gazipur deployment: developing optimal threshold-selection strategies to minimize unintended bias [Q78]; evaluating dataset-based identity detection versus substring matching [Q79]; developing a full taxonomy of bias types [Q81]; and acknowledging that "bias is still present in models that have undergone some bias mitigation" [Q77]. The observation that real data shows lower metric values and more variation across identity subgroups than synthetic data [Q65] is particularly relevant — it suggests that the synthetic benchmark substantially underestimates the bias that would appear in a real-world health-chatbot deployment with a non-English, demographically distinct user population. The acknowledgment that "any suite of metrics…always possible that there is subtle bias that the metrics cannot detect" [Q36], combined with the noted tendency for models to skew identity-mentioning non-toxic text toward toxicity [Q69], has specific operational implications for a health chatbot in which users will frequently mention religious identity, gender, and community membership in non-toxic health queries. The limitation regarding data imbalances across identity subgroups [Q18, Q59] is especially salient given the multi-religious, caste-stratified social context of Gazipur, where some identity groups may have very few examples in any Western-sourced corpus.

### 8. Authors and Affiliations

The paper is authored by Daniel Borkan, Lucas Dixon, Jeffrey Sorensen, Nithum Thain, and Lucy Vasserman [Q9], all affiliated with Jigsaw [Q10], a Google subsidiary focused on online safety and counter-extremism. This affiliation situates the work firmly within a Western, English-language internet-platform context, consistent with the benchmark's design choices around English online comment data, Western identity taxonomies, and commercial crowdsourcing annotation infrastructure. The Jigsaw origin signals that the benchmark's implicit deployment context is large-scale English-language online platforms — a context structurally distant from a peri-urban Bangladeshi clinical chatbot serving low-literacy users in Banglish and phonetic Bengali.
```

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | data_sources | "We also introduce a large new test set of online comments with crowd-sourced annotations for identity references." |
| Q2 | 1 | label_categories | "Toxicity, defined as anything that is rude, disrespectful, or unreasonable that would make someone want to leave a conversation, is an inherently complex and subjective classification task." |
| Q3 | 1 | stated_limitations | "Toxicity models specifically have been shown to capture and reproduce biases common in society, for example mis-associating the names of frequently attacked identity groups (such as "gay", and "muslim" etc.) with toxicity." |
| Q4 | 1 | stated_limitations | "This unintended model bias could be due to the demographic composition of the online user pool, the latent or overt biases of those doing the labelling, or the very selection and sampling process used to choose which items to label." |
| Q5 | 1 | evaluation_metrics | "We use a definition of model fairness similar to equality of odds defined in [10]. As in that work, we assume the existence of a test set with reliable labels across a range of groups. Given such a test set, we consider unintended bias to be present in the model if the model performance, according to relevant performance metrics, varies across the set of designated groups." |
| Q6 | 1 | stated_limitations | "It is important to highlight that the assumption of reliable labels is significant and doesn't hold in all use cases. We mitigate the impact of this assumption by demonstrating our results against both a synthetic test set with labels that are constructed to be reliable and a large human-annotated test set with high rating redundancy." |
| Q7 | 1 | evaluation_metrics | "We propose a suite of threshold agnostic performance metrics to measure the extent of unintended model bias. Many prior methods for measuring unintended bias in classification systems rely on selecting a threshold, a choice that can drastically change results." |
| Q8 | 1 | evaluation_metrics | "For these models, threshold dependant metrics can obscure the view of unintended bias and thus be misleading to practitioners. Threshold agnostic metrics capture the behavior of the underlying model itself, and thus can allow a more comprehensive comparison of the model's performance and limitations." |
| Q9 | 1 | authors_affiliations | "Daniel Borkan, Lucas Dixon, Jeffrey Sorensen, Nithum Thain, and Lucy Vasserman." |
| Q10 | 1 | authors_affiliations | "Jigsaw" |
| Q11 | 2 | evaluation_metrics | "We therefore propose a suite of five metrics, derived from ROC-AUC, Equality Gap, and Mann-Whitney U metrics, each of which captures a different aspect of model performance, and a different potential type of unintended bias." |
| Q12 | 2 | data_sources | "We apply these metrics with two test sets, again making the assumption that the labels are reliable. One is a synthetic test set, identical to the one presented in [5]. The other, introduced in this work, is a new human-labeled dataset of nearly 2 million comments, specifically created for evaluation of unintended bias. This includes 450,000 comments annotated with the identities that are referenced in the text." |
| Q13 | 2 | task_taxonomy | "We demonstrate our proposed metrics and datasets on two publicly accessible models that are trained to detect toxicity in text (provided by the Perspective API [11].) One of these models is claimed to be trained using a bias mitigation technique, as described in [5] and [13]." |
| Q14 | 2 | evaluation_metrics | "Most metrics for unintended bias rely on dividing the test data up by identity or demographic based subgroups and computing metrics for each group. For our metrics, we also divide data by subgroup. However, instead of calculating metrics on the subgroup data exclusively, our metrics compare the subgroup to the rest of the data, which we call the "background" data." |
| Q15 | 2 | evaluation_metrics | "A core benefit of AUC is that it is threshold agnostic." |
| Q16 | 2 | evaluation_metrics | "Our proposed metrics differ from these early approaches because they are threshold agnostic, robust to class imbalances in the dataset, and because they provide more nuanced insight into the types of bias present in the model, as we will see in Section 3.3." |
| Q17 | 3 | evaluation_metrics | "An important quality of the AUC metric is that it is robust to data imbalances in the amount of negative and positive examples in the test set." |
| Q18 | 3 | stated_limitations | "This is especially relevant when measuring unintended bias, because in real-world data, the amount of examples in each identity subgroup, and the balance between negative and positive examples can vary widely across groups (in fact, this variation is often a source of bias)." |
| Q19 | 3 | evaluation_metrics | "Enforcing that for each AUC, either all negative or all positive examples (or both in Subgroup AUC) come from one identity group, means that mis-orderings involving that particular subset cannot be drowned out by results from other groups, ensuring that these metrics are robust to data imbalances likely to occur in real data." |
| Q20 | 3 | evaluation_metrics | "We now introduce two additional threshold agnostic metrics, building from a strict generalization of the Equality Gap metric." |
| Q21 | 3 | evaluation_metrics | "The Equality Gap is the difference between the true positive rates of the subgroup (TPR(Dд)) and the background (TPR(D)), at a specific threshold." |
| Q22 | 3 | evaluation_metrics | "For each threshold, t, if you plot the true positive rate of the subgroup as x(t) and the true positive rate of the background as y(t) then the Positive Average Equality Gap is the area between the curve (x(t),y(t)) and the line y = x, i.e. Positive AEG = ∫₀¹ (y(t) − x(t)) dx(t)" |
| Q23 | 3 | evaluation_metrics | "There is also the analogous definition with true negative rates in place of true positive ones." |
| Q24 | 3 | evaluation_metrics | "These are clearly separate sentences. They are two consecutive but independent statements about the Average Equality Gap metrics.  SEPARATE" |
| Q25 | 4 | evaluation_metrics | "At each of these extremes, it represents a different type of bias where the TPR of the subgroup is consistently higher or lower, respectively, than that of the background." |
| Q26 | 4 | evaluation_metrics | "The optimal value of the Average Equality Gap metric is 0, which means the subgroup and background distributions have identical means." |
| Q27 | 4 | evaluation_metrics | "If Equality of Opportunity holds for every threshold then the Average Equality Gap will be 0." |
| Q28 | 4 | evaluation_metrics | "If the Average Equality Gap is 0 then Equality of Opportunity must hold for some non-trivial threshold 0 < t < 1." |
| Q29 | 5 | data_sources | "We demonstrate this suite of metrics using the publicly available toxicity classifiers provided by the Perspective API ([11])." |
| Q30 | 5 | data_sources | "We use two test sets, 1) a synthetically generated, bias-focused test set following [5] and 2) a large dataset of online comments with human labels for both identity and toxicity." |
| Q31 | 5 | evaluation_metrics | "Overall, Subgroup AUC and BPSN and BNSP AUCs identify any bias significant enough to cause mis-orderings between negative and postive examples, i.e. bias that interferes with selecting a single threshold that works similarly across groups." |
| Q32 | 5 | evaluation_metrics | "Subgroup AUC highlights when those mis-orderings are caused by poor model understanding within the subgroup, and BPSN and BNSP AUCs highlight when the misorderings are caused by score shifts." |
| Q33 | 5 | evaluation_metrics | "The AEGs go beyond the AUCs to identify bias in the distribution itself, even when (non-trivial) perfect thresholding is possible." |
| Q34 | 5 | evaluation_metrics | "Both AEGs and BPSN and BNSP AUCs provide insight into the directionality of score shifts." |
| Q35 | 5 | stated_limitations | "It's important to note that the correct handling of subtle variations in distributions must be decided on case by case basis." |
| Q36 | 5 | stated_limitations | "And, as with any other suite of metrics, it's always possible that there is subtle bias that the metrics cannot detect." |
| Q37 | 6 | task_taxonomy | "Using our metrics, we compare two versions of Perspective API's toxicity classifier, the initial TOXICITY@1 and the latest TOXICITY@6." |
| Q38 | 6 | stated_limitations | "TOXICITY@1 was shown to have significant unintended bias around identity words like "gay" and "transgender", both by independent analysis and by the Perspective team [13]." |
| Q39 | 6 | task_taxonomy | "TOXICITY@6 was built using the bias mitigation techniques presented in [5] and, and therefore we expect to see reduced unintended bias between these two models across our new metrics." |
| Q40 | 6 | data_sources | "The synthetic dataset contains 77k examples generated from templates using 50 identity terms, 50% toxic and 50% non-toxic across all terms." |
| Q41 | 6 | data_format | "These examples are constructed explicitly to measure unintended bias based on identity terms." |
| Q42 | 6 | data_format | "The examples are simple sentences that should be clearly toxic or clearly non-toxic, regardless of identity terms present." |
| Q43 | 6 | evaluation_metrics | "In Table 3, we show Subgroup AUC, BPSN AUC, BNSP AUC, Negative AEG, and Positive AEG for both TOXICITY models on the synthetic dataset." |
| Q44 | 6 | data_sources | "The dataset contains 50 identity terms, here we show results for the lowest performing 20 subgroups." |
| Q45 | 6 | stated_limitations | "Synthetic test sets, while useful for capturing issues not present in real data, may not provide accurate results for real scenarios with different data distributions." |
| Q46 | 6 | stated_limitations | "In addition, synthetic sets are limited to the specific identity terms that are manually curated, and therefore are unlikely to capture the true diversity of ways that identities are discussed in real conversation." |
| Q47 | 6 | annotation_process | "To facilitate unintended bias evaluation on real data, we designed techniques to have humans label the identity content within real data." |
| Q48 | 6 | annotation_process | "We presented crowd raters with a comment and asked a set of questions including, for example, "What genders are referenced in the comment?" and "What races or ethnicities are referenced in the comment?"." |
| Q49 | 6 | annotation_process | "For each question, raters selected the set of identities present in the comment from a provided list." |
| Q50 | 6 | annotation_process | "Using human labeling for identity content allows us to capture nuanced identity content" |
| Q51 | 7 | stated_limitations | "The set of identities labelled by raters is not comprehensive and does not provide universal coverage." |
| Q52 | 7 | data_format | "This set was designed to balance the coverage of identities, crowd rater accuracy, and ensure that each labeled identity has enough examples in the final data set to provide meaningful results." |
| Q53 | 7 | annotation_process | "This data was also labeled for toxicity using the same crowd rating guidelines as published by the Perspective API ([18], [19])." |
| Q54 | 7 | label_categories | "This labeling asks raters to rate the toxicity of a comment, selecting from "Very Toxic", "Toxic", "Hard to Say", and "Not Toxic"." |
| Q55 | 7 | label_categories | "Raters were also asked about several subtypes of toxicity, although these labels were not used for the analysis in this work." |
| Q56 | 7 | data_sources | "Using these rating techniques we created a dataset of 1.8 million comments, sourced from online comment forums, containing labels for toxicity and identity." |
| Q57 | 7 | data_sources | "While all of the comments were labeled for toxicity, and a subset of 450,000 comments was labeled for identity." |
| Q58 | 7 | annotation_process | "Some comments labeled for identity were preselected using models built from previous iterations of identity labeling to ensure that crowd raters would see identity content frequently." |
| Q59 | 7 | stated_limitations | "Table 5 shows the toxicity percentage for a selection of identities, illustrating that there is an imbalance in toxicity between different identities, emphasizing the value of metrics that are robust to these data skews." |
| Q60 | 8 | data_sources | "To enable further research in this field, this entire dataset and annotations will be released under a Creative Commons license at https://git.io/fhpcC." |
| Q61 | 8 | evaluation_metrics | "Applying the AUC and AEG metrics to this real dataset reveals several new insights about the two toxicity models." |
| Q62 | 8 | data_format | "Table 6 compares results for both TOXICITY@1 and TOXICITY@6 on all metrics, for both short comments (less than 100 characters) and all comments." |
| Q63 | 8 | task_taxonomy | "We present results on short comments separately because, according to [13], the bias mitigation implemented between TOXICITY@1 and TOXICITY@6 focused on short comments." |
| Q64 | 8 | data_format | "The identities shown in Table 6 are all identities that contained more than 100 examples of short comments." |
| Q65 | 8 | stated_limitations | "Real data reveals more unintended bias than synthetic data. Comparing the real data results to the synthetic data results in Table 3, we find lower values and more variation across identity subgroups in the real data than we do in synthetic data." |
| Q66 | 8 | stated_limitations | "The synthetic data is intentionally very simple, so it is best at revealing very large discrepancies in performance that are tied very narrowly to specific identity terms, while the real data is much more broad and nuanced, but also potentially noisier." |
| Q67 | 8 | evaluation_metrics | "Bias tends to skew towards toxicity. Across both models and both short and long comments, we see lower values for Subgroup AUC and BPSN AUC and higher values for BNSP AUC." |
| Q68 | 8 | evaluation_metrics | "We also tend to see positive values for Negative AEG and negative values for Positive AEG." |
| Q69 | 8 | stated_limitations | "Together, all of these metrics indicate that the models have a tendency to skew non-toxic comments that discuss identity towards toxicity." |
| Q70 | 8 | evaluation_metrics | "We introduced a new suite of metrics for unintended bias, based on ROC-AUC and Mann-Whitney U scores." |
| Q71 | 8 | evaluation_metrics | "These metrics provide a detailed and nuanced view of the types of bias present in a model and overcome limitations of similar metrics like Equality Gap in that they are threshold agnostic." |
| Q72 | 9 | evaluation_metrics | "We developed and applied an evaluation method for our introduced metrics using a variety of example illustrative distributions." |
| Q73 | 9 | evaluation_metrics | "This highlights the differences in various metric behaviors for different kinds of bias." |
| Q74 | 9 | evaluation_metrics | "We then demonstrated our metrics using existing toxicity classifiers that are provided by the Perspective API [11]." |
| Q75 | 10 | data_sources | "This involved adapting existing synthetic datasets used for unintended bias measurement of text classifiers." |
| Q76 | 10 | data_sources | "Finally we extend beyond the synthetic test set methodology, leveraging the improved nuance of the newly introduced metrics by crowdsourcing a large new corpus of nearly 2 million annotations of comments, providing one of the first studies of unintended bias based on identity references in text classification on real data." |
| Q77 | 10 | stated_limitations | "Our evaluation using this new dataset highlights how the new metrics also reveal new challenges for bias mitigation, highlighting that bias is still present in models that have undergone some bias mitigation." |
| Q78 | 10 | stated_limitations | "Developing effective strategies for choosing optimal thresholds to minimize unintended bias." |
| Q79 | 10 | stated_limitations | "Evaluating the relative benefit of the newly introduced dataset compared to sub-string matching of terms that reference an identity." |
| Q80 | 10 | stated_limitations | "A more systematic definition of the kinds of synthetic distributions that can be used to evaluate and categorize metrics for unintended bias." |
| Q81 | 10 | stated_limitations | "Developing a full taxonomy of different possible biases and a systematic approach for these metrics to be used in their diagnosis." |

### Category Index
- **task_taxonomy**: Q13, Q37, Q39, Q63
- **data_sources**: Q1, Q12, Q29, Q30, Q40, Q44, Q56, Q57, Q60, Q75, Q76
- **data_format**: Q41, Q42, Q52, Q62, Q64
- **label_categories**: Q2, Q54, Q55
- **annotation_process**: Q47, Q48, Q49, Q50, Q53, Q58
- **evaluation_metrics**: Q5, Q7, Q8, Q11, Q14, Q15, Q16, Q17, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q31, Q32, Q33, Q34, Q43, Q61, Q67, Q68, Q70, Q71, Q72, Q73, Q74
- **stated_limitations**: Q3, Q4, Q6, Q18, Q35, Q36, Q38, Q45, Q46, Q51, Q59, Q65, Q66, Q69, Q77, Q78, Q79, Q80, Q81
- **authors_affiliations**: Q9, Q10
