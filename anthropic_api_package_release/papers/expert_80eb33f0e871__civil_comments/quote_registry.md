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
