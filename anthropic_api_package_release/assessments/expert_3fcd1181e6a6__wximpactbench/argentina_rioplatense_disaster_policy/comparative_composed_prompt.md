I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **CrisisBench: Benchmarking Crisis-related Social Media Datasets for Humanitarian Information Processing** is valid for use in **Argentina — Buenos Aires Policy Maker Cohort (Disaster Reporting Reliability)**.

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

- **Name**: crisisbench
- **Full Name**: CrisisBench: Benchmarking Crisis-related Social Media Datasets for Humanitarian Information Processing
- **Domain**: Crisis/disaster social media classification
- **Languages**: en, es, it
- **Porting Strategy**: none
- **Year**: 2021

### Benchmark Documentation

## Key characteristics relevant to validity analysis

### 1. Input Ontology
CrisisBench organizes its task taxonomy around three canonical crisis-NLP categories:
informativeness (binary: informative vs. not-informative), humanitarian information
types (multi-class, e.g., affected individuals, infrastructure damage), and event types
(e.g., flood, earthquake, fire) [Q3]. Of these, only the first two are implemented and
benchmarked in the current study; event-type classification is explicitly deferred to
future work [Q22, Q23]. The humanitarian task is described as substantially harder than
the binary informativeness task due to its multi-class nature [Q89], and experiments
demonstrate that disaster-specific context shapes performance [Q93]. Class labels deemed
non-humanitarian — such as "animal management" and "not labeled" — are excluded from
consolidated experiments but retained in released data [Q34, Q57, Q58]. Some class
labels have extremely low support (e.g., only 17 "terrorism related" tweets in CrisisNLP
[Q52]; "disease related" appears only in CrisisNLP [Q53]), and heterogeneous training
data from diverse global disaster events may produce suboptimal classifiers [Q80]. The
taxonomy does not include sub-labels for regional Argentine hazard types (pampero
windstorms, ENSO-driven drought, Río de la Plata flooding) or informal-settlement
impact framing — categories explicitly flagged as desirable by deployment users [Q61].
Individual dataset subsets (CrisisLex with six class labels; CrisisNLP with eleven)
illustrate significant variability in categorical granularity across source datasets [Q76].

### 2. Input Content
The benchmark consolidates eight publicly available, human-annotated tweet datasets
yielding 166,100 tweets for informativeness and 141,500 for humanitarian classification
[Q1, Q7, Q10]. Source datasets span disaster events from 2010 through 2017, providing
temporal breadth [Q100, Q105]. Geographic coverage is concentrated in North American
and globally reported events: SWDM2013 and ISCRAM2013 draw from the Joplin, Missouri
tornado (2011) and Hurricane Sandy (2012) [Q27, Q28]; DRD covers events in 2010 and
2012 [Q29]; CrisisMMD covers seven 2017 international disasters [Q31]; and AIDR was
annotated by domain experts across different events [Q32]. No Latin American or
Argentine disaster events are documented as represented. English tweets constitute
94.46% of the informativeness set [Q46], and non-English content is largely confined
to the CrisisLex dataset [Q47], meaning Spanish-language social media content —
especially Rioplatense Spanish informal discourse — is negligibly represented. The
dataset covers time-span 2010–2017 [Q100], which is temporally dated for current
Argentine crisis communication norms. Future research directions acknowledge the
potential value of multilingual pre-trained models on the full multilingual dataset
[Q98], but all current experiments are English-only [Q59]. This English-language,
North America-concentrated content base constitutes the most significant validity gap
for the Argentine social media deployment channel.

### 3. Input Form
The input modality is exclusively Twitter text (tweets). Preprocessing applies a
modified Tweet NLP tokenizer with lowercasing, URL removal, punctuation stripping,
and user-ID removal [Q38]. Near-duplicate detection uses a bag-of-ngrams cosine-
similarity approach with a manually validated threshold of 0.75 [Q39, Q40, Q112],
reducing the dataset by approximately 25% for informativeness and 20% for humanitarian
tasks [Q41]. Although the consolidated dataset retains multilingual content including
Spanish and Italian tweets without explicit language tags [Q42, Q43], the benchmark
assigns language tags via Google Cloud API [Q44, Q45] and restricts all classification
experiments to English [Q59]. Data is split 70/10/20 for train/dev/test [Q60]. The
tweet-length constraint and Twitter-specific preprocessing pipeline mean that
generalization to longer-form news articles, press releases, or institutional
communications — additional channels in the Argentine deployment — is not evaluated
and is not natively supported by the benchmark's input infrastructure. Preprocessing
details for symbol and emoticon removal are also documented [Q74], and duplicate
flagging conventions are reported [Q126, Q127].

### 4. Output Ontology
The label ontology was constructed by manually mapping semantically similar class
labels across eight source datasets into a common schema oriented toward humanitarian
aid relevance [Q18, Q33]. Specific mappings are fully documented (e.g., "building
damaged" → "infrastructure and utilities damage" [Q33]; mapping tables for all
constituent datasets [Q106, Q107, Q108, Q109, Q110, Q123, Q124, Q125]). The output
space is limited to two tasks: binary informativeness and multi-class humanitarian type
[Q12]. Critically, the benchmark does not include a source credibility, misinformation
likelihood, or signal-to-noise reliability dimension. For the Argentine deployment, the
output taxonomy is treated as a necessary but insufficient foundation: policy makers
require a trustworthiness or reliability score, which the user envisions constructing
downstream by combining model outputs with external metadata. The DSM dataset
contributes only a relevant/not-relevant binary [Q109], while CrisisMMD required minor
remapping [Q110], illustrating variation in original label granularity. Class
distributions remain imbalanced even after consolidation, with "not humanitarian"
comprising 37.40% of the humanitarian set [Q55, Q56], and some humanitarian class
labels carry very low support [Q52, Q53, Q54]. Results for individual datasets report
only the classes for which models are able to classify [Q88], further constraining the
reliability of minority-class outputs.

### 5. Output Content
The annotation process is minimally documented in the paper. The single directly
attested fact is that the AIDR dataset was labeled by domain experts using the AIDR
system across different events [Q111]. For the remaining seven source datasets, the
paper cites original publications but does not reproduce annotator demographics,
recruitment methods, inter-annotator agreement (IAA) statistics, or quality assurance
protocols. Social media data is acknowledged as noisy and posing challenges for
labeling and training classifiers [Q94]. The absence of documented annotator backgrounds
makes it impossible to assess how well label judgments reflect Argentine institutional
or journalistic norms for what constitutes a credible or informative disaster signal.
Cross-dataset evaluation reveals substantial performance degradation (14.3% F1 drop
for informativeness when training on CrisisLex and evaluating on CrisisNLP [Q87]),
signaling that label conventions are not fully portable across disaster event contexts —
raising further concern about portability to Argentine discourse. The elicitation
summary flags annotator-population mismatch as a key gap, and the paper provides no
evidence to mitigate this concern.

### 6. Output Form
The benchmark evaluates classifiers using weighted average precision, recall, and
F1-measure; weighting is chosen explicitly to account for class imbalance [Q75]. Three
model families are benchmarked: CNN [Q63], fastText with Common Crawl pre-trained
English embeddings [Q64], and transformer models BERT, DistilBERT, and RoBERTa [Q66].
The best-performing system achieves 0.866 F1 for informativeness and 0.829 F1 for
humanitarian classification on the consolidated English test set [Q84], with transformer
models generally outperforming CNN and fastText [Q90, Q91]. Multilingual experiments
(not the primary benchmark) show an ~8% F1 drop for humanitarian classification using
BERT [Q99]. Event-aware training improves humanitarian classification by 1.3 F1 points
using CNN [Q92]. The output is a discrete classification label; the deployment envisions
an aggregated credibility score combining model output with external metadata [Q2, Q96].
Pre-trained models were primarily trained on non-Twitter text, a limitation the authors
acknowledge [Q65], and transformer model instability requires ten re-runs per experiment
[Q72]. Hyperparameter documentation is fully reported [Q113–Q121]. The gap between the
benchmark's discrete classification output form and the deployment's need for a
continuous or aggregated credibility signal is user-acknowledged as a downstream
construction step, not something the benchmark itself addresses.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "We consolidate eight human-annotated datasets and provide 166.1k and 141.5k tweets for informativeness and humanitarian classification tasks, respectively." |
| Q2 | 1 | output_form | "We provide benchmarks for both binary and multiclass classification tasks using several deep learning architectures including, CNN, fastText, and transformers." |
| Q3 | 1 | input_ontology | "Typical classification tasks in the community include (i) informativeness (i.e., informative vs. not-informative messages), (ii) humanitarian information types (e.g., affected individual reports, infrastructure damage reports), and (iii) event types (e.g., flood, earthquake, fire)." |
| Q4 | 1 | output_form | "First, few efforts have been invested to develop standard datasets (specifically, train/dev/test splits) and benchmarks for the community to compare their results, models, and techniques." |
| Q5 | 1 | input_content | "Secondly, most of the published datasets are noisy, e.g., CrisisLex (Olteanu et al. 2014) contains duplicate and near-duplicate content, which produces misleading classification performance." |
| Q6 | 1 | input_form | "Moreover, some datasets (e.g., CrisisLex) consist of tweets from several languages without any explicit language tag, to separate the data of a particular language of interest." |
| Q7 | 1 | input_content | "We consolidate eight publicly available datasets (see Section 3)." |
| Q8 | 1 | output_ontology | "One of the challenges is the inconsistent class labels across various data sources." |
| Q9 | 1 | output_content | "Firoj Alam, Hassan Sajjad, Muhammad Imran, Ferda Ofli, Qatar Computing Research Institute, HBKU, Qatar" |
| Q10 | 2 | input_content | "We consolidate eight publicly available disaster-related datasets by manually mapping semantically similar class labels, which leads to a larger dataset." |
| Q11 | 2 | input_form | "We carefully cleaned various forms of duplicates, and assigned a language tag to each tweet." |
| Q12 | 2 | input_ontology | "We provide benchmark results on English tweets set using state-of-the-art machine learning algorithms such as Convolutional Neural Networks (CNN), fastText (Joulin et al. 2017) and pre-trained transformer models (Devlin et al. 2019) for two classifications tasks, i.e., Informativeness (binary) and Humanitarian type (multi-class) classification." |
| Q13 | 2 | input_form | "For the research community, we aim to release the dataset in multiple forms as, (i) a consolidated class label mapped version, (ii) exact- and near-duplicate filtered version obtained from previous versions, (iii) a subset of the filtered data used for the classification experiments in this study." |
| Q14 | 2 | input_content | "A major limitation of the work by Alam, Muhammad, and Ferda (2019) is that the issue of duplicate and near-duplicate content have not been addressed when combining the different datasets." |
| Q15 | 2 | input_content | "Kersten et al. (2019) focused only on informativeness classification and combined five different datasets. This study has also not focused on exact- and near-duplicate content, which exist in different datasets." |
| Q16 | 2 | output_form | "A fair comparison of the classification experiment is also difficult with previous studies as their train/dev/test splits are not public, except the dataset by Wiegmann et al. (2020)." |
| Q17 | 2 | input_content | "We address such limitations in this study, i.e., we consolidate the datasets, eliminate duplicates, and release standard dataset splits with benchmark results." |
| Q18 | 2 | output_ontology | "In this study, we use the class labels that are important for humanitarian aid for disaster response tasks, which are common across the publicly available resources." |
| Q19 | 2 | output_form | "The study of (Nguyen et al. 2017) and (Neppalli, Caragea, and Caragea 2018) performed comparative experiments between different classical and deep learning algorithms including Support Vector Machines, Logistic Regression, Random Forests, Recurrent Neural Networks, and Convolutional Neural Networks (CNN)." |
| Q20 | 2 | output_form | "Their experimental results suggest that CNN outperforms other algorithms." |
| Q21 | 2 | output_form | "Though in another study, (Burel and Alani 2018) reports that SVM and CNN can provide very competitive results in some cases." |
| Q22 | 2 | input_ontology | "We only focused on two tasks for this study and we aim to address event types task in a future study." |
| Q23 | 3 | input_ontology | "We consolidate eight datasets that were labeled for different disaster response classification tasks and whose labels can be mapped consistently for two tasks: informativeness and humanitarian information type classification." |
| Q24 | 3 | output_ontology | "In doing so, we deal with two major challenges: (i) discrepancies in the class labels used across different datasets, and (ii) exact- and near-duplicate content that exists within as well as across different datasets." |
| Q25 | 3 | input_content | "CrisisLex is one of the largest publicly-available datasets, which consists of two subsets, i.e., CrisisLexT26 and CrisisLexT6 (Olteanu et al. 2014). CrisisLexT26 comprises data from 26 different crisis events that took place in 2012 and 2013 with annotations for informative vs. not-informative as well as humanitarian categories (six classes) classification tasks among others. CrisisLexT6, on the other hand, contains data from six crisis events that occurred between October 2012 and July 2013 with annotations for related vs. not-related binary classification task." |
| Q26 | 3 | input_content | "CrisisNLP is another large-scale dataset collected during 19 different disaster events that happened between 2013 and 2015, and annotated according to different schemes including classes from humanitarian disaster response and some classes related to health emergencies (Imran, Mitra, and Castillo 2016)." |
| Q27 | 3 | input_content | "SWDM2013 dataset consists of data from two events: (i) the Joplin collection contains tweets from the tornado that struck Joplin, Missouri on May 22, 2011; (ii) The Sandy collection contains tweets collected from Hurricane Sandy that hit Northeastern US on Oct 29, 2012 (Imran et al. 2013a)." |
| Q28 | 3 | input_content | "ISCRAM2013 dataset consists of tweets from two different events occurred in 2011 (Joplin 2011) and 2012 (Sandy 2012). Note that this set of tweets are different than SWDM2013 set even though they are collected from same events (Imran et al. 2013b)." |
| Q29 | 3 | input_content | "Disaster Response Data (DRD) consists of tweets collected during various crisis events that took place in 2010 and 2012. This dataset is annotated using 36 classes that include informativeness as well as humanitarian categories." |
| Q30 | 3 | input_content | "Disasters on Social Media (DSM) dataset comprises 10K tweets collected and annotated with labels related vs. not-related to the disasters." |
| Q31 | 3 | input_content | "CrisisMMD is a multimodal dataset consisting of tweets and associated images collected during seven disaster events that happened in 2017 (Alam et al. 2018). The annotations for this dataset is targeted for three classification tasks: (i) informative vs. not-informative, (ii) humanitarian categories (eight classes) and (iii) damage severity assessment." |
| Q32 | 3 | input_content | "AIDR dataset is obtained from the AIDR system (Imran et al. 2014) that has been annotated by domain experts for different events and made available upon requests. We only retained labeled data that are relevant to this study." |
| Q33 | 3 | output_ontology | "The datasets come with different class labels. We create a set of common class labels by manually mapping semantically similar labels into one cluster. For example, the label "building damaged," originally used in the AIDR system, is mapped to "infrastructure and utilities damage" in our final dataset." |
| Q34 | 3 | output_ontology | "Some of the class labels in these datasets are not annotated for humanitarian aid purposes, therefore, we have not included them in the consolidated dataset. For example, we do not select tweets labeled as "animal management" or "not labeled" that appear in CrisisNLP and CrisisLex26." |
| Q35 | 3 | output_ontology | "This causes a drop in the number of tweets for both informativeness and humanitarian tasks as can be seen in Table 1 (Mapping column). The large drop in the CrisisLex dataset for the informativeness task is due to the 3,103 unlabeled tweets (i.e., labeled as "not labeled")." |
| Q36 | 3 | output_ontology | "The other significant drop for the informativeness task is in the DRD dataset. This is because many tweets were annotated with multiple labels," |
| Q37 | 4 | input_form | "To develop a machine learning model, it is important to design non-overlapping train/dev/test splits. A common practice is to randomly split the dataset into train/dev/test sets. This approach does not work with social media data as it generally contains duplicates and near duplicates. Such duplicate content, if present in both train and test sets, often leads to overestimated test results during classification." |
| Q38 | 4 | input_form | "We first tokenize the text before applying any filtering. For tokenization, we used a modified version of the Tweet NLP tokenizer (O'Connor, Krieger, and Ahn 2010). Our modification includes lowercasing the text and removing URL, punctuation, and user id mentioned in the text. We then filter tweets having only one token." |
| Q39 | 4 | input_form | "We then use a similarity-based approach to remove the near-duplicates. To do this, we first convert the tweets into vectors using bag-of-ngram approach as a vector representation. We use uni- and bi-grams with their frequency-based representations. We then use cosine similarity to compute a similarity score between two tweets and flag them as duplicate if their similarity score is greater than the threshold value of 0.75." |
| Q40 | 4 | input_form | "To determine a plausible threshold value, we manually checked the tweets in different threshold bins (i.e., 0.70 to 1.0 with 0.05 interval) as shown in Figure 1, which we selected from consolidated informativeness dataset. By investigating the distribution and manual checking, we concluded that a threshold value of 0.75 is a reasonable choice." |
| Q41 | 4 | input_form | "As indicated in Table 1, there is a drop after filtering, e.g., ∼25% for informativeness and ∼20% for humanitarian tasks. It is important to note that failing to eradicate duplicates from the consolidated dataset would potentially lead to" |
| Q42 | 5 | input_form | "Some of the existing datasets contain tweets in various languages (i.e., Spanish and Italian) without explicit assignment of a language tag." |
| Q43 | 5 | input_form | "In addition, many tweets have codeswitched (i.e., multilingual) content." |
| Q44 | 5 | input_form | "We decided to provide a language tag for each tweet if it is not available with the respective dataset." |
| Q45 | 5 | input_form | "We used the language detection API of Google Cloud Services for this purpose." |
| Q46 | 5 | input_content | "Among different languages of informativeness tweets, English tweets appear to be highest in the distribution compared to any other language, which is 94.46% of 156,899." |
| Q47 | 5 | input_content | "Note that most of the non-English tweets appear in the CrisisLex dataset." |
| Q48 | 5 | output_ontology | "Distribution of class labels is an important factor for developing the classification model." |
| Q49 | 5 | output_ontology | "It is clear that there is an imbalance in class distributions in different datasets and some class labels are not present." |
| Q50 | 5 | output_ontology | "For example, the distribution of "not informative" class is very low in SWDM2013 and ISCRAM2013 datasets." |
| Q51 | 5 | output_ontology | "For the humanitarian task, some class labels are not present in different datasets." |
| Q52 | 5 | output_ontology | "Only 17 tweets with the label "terrrorism related" are present in CrisisNLP." |
| Q53 | 5 | output_ontology | "Similarly, the class "disease related" only appears in CrisisNLP." |
| Q54 | 5 | output_ontology | "The scarcity of the class labels poses a great challenge to design the classification model using individual datasets." |
| Q55 | 5 | output_ontology | "Even after combining the datasets, the imbalance in class distribution seems to persist (last column in Table 4)." |
| Q56 | 5 | output_ontology | "For example, the distribution of "not humanitarian" is relatively higher (37.40%) than other class labels." |
| Q57 | 5 | output_ontology | "In Table 4, we highlighted some class labels, which we dropped in the rest of the classification experiments conducted in this study." |
| Q58 | 5 | output_ontology | "However, tweets with those class labels will be available in the released datasets." |
| Q59 | 6 | input_form | "Although our consolidated dataset contains multilingual tweets, we only use tweets in English language in our experiments." |
| Q60 | 6 | input_form | "We split data into train, dev, and test sets with a proportion of 70%, 10%, and 20%, respectively, also reported in Table 5." |
| Q61 | 6 | input_ontology | "As mentioned earlier we have not selected the tweets with highlighted class labels in Table 4 for the classification experiments." |
| Q62 | 6 | output_form | "For the experiments, we use CNN, fastText, and pre-trained transformer models." |
| Q63 | 6 | output_form | "The current state-of-the-art disaster classification model is based on the CNN architecture." |
| Q64 | 6 | output_form | "For the fastText (Joulin et al. 2017), we used pre-trained embeddings trained on Common Crawl, which is released by fastText for English." |
| Q65 | 6 | input_content | "Though the pre-trained models are mainly trained on non-Twitter text, we hypothesize that their rich contextualized embeddings would be beneficial for the disaster domain." |
| Q66 | 6 | output_form | "In this work, we choose the pre-trained models BERT (Devlin et al. 2019), DistilBERT (Sanh et al. 2019), and RoBERTa (Liu et al. 2019) for the classification tasks." |
| Q67 | 6 | output_form | "We train the CNN models using the Adam optimizer (Kingma and Ba 2014)." |
| Q68 | 6 | output_form | "The batch size is 128 and maximum number of epochs is set to 1000." |
| Q69 | 6 | output_form | "We use a filter size of 300 with both window size and pooling length of 2, 3, and 4, and a dropout rate 0.02." |
| Q70 | 6 | output_form | "We set early stopping criterion based on the accuracy of the development set with a patience of 200." |
| Q71 | 6 | output_form | "For the experiments with fastText, we used default parameters except: (i) the dimension is set to 300, (ii) minimal number of word occurrences is set to 3, and (iii) number of epochs is 50." |
| Q72 | 6 | output_form | "Due to the instability of the pre-trained models as reported in (Devlin et al. 2019), we perform ten re-runs for each experiment using different seeds, and we select the model that performs best on the dev set." |
| Q73 | 6 | output_form | "For transformer-based models, we used a learning rate of 2e − 5, and a batch size of 8." |
| Q74 | 6 | input_form | "Prior to the classification experiment, we preprocess tweets to remove symbols, emoticons, invisi-" |
| Q75 | 7 | output_form | "To measure the performance of each classifier, we use weighted average precision (P), recall (R), and F1-measure (F1). The rationale behind choosing the weighted metric is that it takes into account the class imbalance problem." |
| Q76 | 7 | input_ontology | "The motivation of these experiments is to investigate whether model trained with consolidated dataset generalizes well across different sets. For the individual dataset classification experiments, we selected CrisisLex and CrisisNLP as they are relatively larger in size and have a reasonable number of class labels, i.e., six and eleven class labels, respectively." |
| Q77 | 7 | input_form | "Note that these are subsets of the consolidated dataset reported in Table 5. We selected them from train, dev and test splits of the consolidated dataset to be consistent across different classification experiments." |
| Q78 | 7 | output_form | "To understand the effectiveness of the smaller datasets, we run experiments by training the model using smaller datasets and evaluating using the consolidated test set." |
| Q79 | 7 | input_content | "The availability of annotated data for a disaster event is usually scarce. One of the advantages of our compiled data is to have identical classes across several disaster events. This enables us to combine the annotated data from all previous disasters for the classification." |
| Q80 | 7 | input_content | "Though this increases the size of the training data substantially, the classifier may result in sub-optimal performance due to the inclusion of heterogeneous data (i.e., a variety of disaster types and occurs in a different part of the world)." |
| Q81 | 7 | input_form | "We append a disaster event type as a token to each annotated tweet ti. More concretely, say tweet ti consists of k words {w1, w2, ..., wk}. We append a disaster event type tag di to each tweet so that ti would become {di, w1, w2, ..., wk}. We repeat this step for all disaster event types present in our dataset." |
| Q82 | 7 | input_ontology | "The event-aware training requires the knowledge of the disaster event type at the time of the test. If we do not provide a disaster event type, the classification performance will be suboptimal due to a mismatch between train and test." |
| Q83 | 7 | input_form | "Instead of appending the disaster event type to all tweets of a disaster, we randomly append disaster event type UNK to 5% of the tweets of every disaster. Note that UNK is now distributed across all disaster event types and is a good representation of an unknown event." |
| Q84 | 8 | output_form | "The model trained using the consolidated dataset achieves 0.866 (F1) for informativeness and 0.829 for humanitarian, which is better than the models trained using individual datasets." |
| Q85 | 8 | output_form | "Between CrisisLex and CrisisNLP, the performance is higher on CrisisLex dataset for both informativeness and humanitarian tasks (1st vs. 4th row in Table 6 for the informativeness, and 10th vs. 13th row for the humanitarian task in the same table.)." |
| Q86 | 8 | input_content | "This might be due to the CrisisLex dataset being larger than the CrisisNLP dataset." |
| Q87 | 8 | output_content | "The cross dataset (i.e., train on CrisisLex and evaluate on CrisisNLP) results shows that there is a drop in performance. For example, there is 14.3% difference in F1 on CrisisNLP data using the CrisisLex model for the informativeness task." |
| Q88 | 8 | output_ontology | "In the humanitarian task, for different datasets in Table 6, we have different number of class labels. We report the results of those classes only for which the model is able to classify." |
| Q89 | 8 | input_ontology | "Note that humanitarian task is a multi-class classification problem, which makes it a much more difficult task than the binary informativeness classification." |
| Q90 | 8 | output_form | "The transformer based models achieve higher performance compared to the CNN and fastText. We used three transformer based models, which varies in the parameter sizes. However, in terms of performance, they are quite similar." |
| Q91 | 8 | output_form | "BERT performs better than or on par with CNN across all classes. More importantly, BERT performs substantially better than CNN in the case of minority classes as highlighted in the table." |
| Q92 | 8 | output_form | "The event-aware training improves the classification performance by 1.3 points (F1) using CNN for the humanitarian task compared to the results without using event information (see Table 6). However, no improvement has been observed for the informativeness task." |
| Q93 | 8 | input_ontology | "The training using event information enables the system to use data of all disasters while preserving the disaster-specific distribution." |
| Q94 | 9 | output_content | "Social media data is noisy and it often poses a challenge for labeling and training classifiers." |
| Q95 | 9 | input_form | "Our analysis on publicly available datasets reveals that one should follow a number of steps before preparing and labeling any social media dataset, not just the dataset for crisis computing. Such steps include (i) tokenization to help in the subsequent phase, (ii) remove exact- and near-duplicates, (iii) check for existing data where the same tweet might be annotated for the same task, and then (iv) labeling." |
| Q96 | 9 | output_form | "For designing the classifier, we postulate checking the overlap between training and test splits to avoid any misleading performance." |
| Q97 | 9 | input_form | "It is important to emphasize the fact that the results reported in this study are reliable as they are obtained on a dataset that has been cleaned from duplicate content, which might have led to misleading performance results otherwise." |
| Q98 | 9 | input_content | "Our initial consolidated datasets (i.e., Table 3 and 4) contains multilingual content with more class labels and different types of content (e.g., disease-related), therefore, an interesting future research could be to try different pre-trained multilingual models to classify tweets in different languages." |
| Q99 | 9 | output_form | "We observe that performance dropped significantly for the humanitarian task compared to English-only dataset. For example, ∼8% drop using BERT model." |
| Q100 | 9 | input_content | "The resulting dataset covers a time-span starting from 2010 to 2017, which can be used to study temporal aspects in crisis scenarios." |
| Q101 | 9 | input_form | "We tried to bridge this gap by consolidating existing datasets, filtering exact- and near-duplicates, and providing benchmarks based on state-of-the-art CNN, FastText, and transformer-based models." |
| Q102 | 9 | input_content | "The developed consolidated labeled dataset is curated from different publicly available sources." |
| Q103 | 10 | input_content | "We release the dataset by maintaining the license of existing resources." |
| Q104 | 11 | input_content | "In Table 11, we report the events associated with the respective datasets such as ISCRAM2013, SWDM2013 CrisisLex and CrisisNLP." |
| Q105 | 11 | input_content | "The time-period is from 2011 to 2015, which is a good representative of temporal aspects." |
| Q106 | 11 | output_ontology | "In Table 12, we report class label mapping for ISCRAM2013, SWDM2013, CrisisLex and CrisisNLP datasets." |
| Q107 | 11 | output_ontology | "Note that all humanitarian class labels also mapped to informative, and not humanitarian labels mapped to not-informative in the data preparation step." |
| Q108 | 11 | output_ontology | "In Table 13, we report the class label mapping for informativeness and humanitarian tasks for DRD dataset." |
| Q109 | 11 | output_ontology | "The DSM dataset only contains tweets labeled as relevant vs not-relevant, which we mapped for informativeness task as shown in Table 14." |
| Q110 | 11 | output_ontology | "The CrisisMMD dataset has been annotated for informativeness and humanitarian task, therefore, very minor label mapping was needed as shown in Table in 15." |
| Q111 | 11 | output_content | "The AIDR data has been labeled by domain experts using AIDR system and has been labeled during different events." |
| Q112 | 11 | input_form | "We have chosen a value of > 0.75 to filter duplicate tweets." |
| Q113 | 11 | output_form | "In this section, we report parameters for CNN and BERT model." |
| Q114 | 11 | output_form | "All experimental scripts will be publicly Hyper-parameters include:" |
| Q115 | 11 | output_form | "Batch size: 8" |
| Q116 | 11 | output_form | "Number of epochs: 10" |
| Q117 | 11 | output_form | "Max seq length: 128" |
| Q118 | 11 | output_form | "Learning rate (Adam): 2e-5" |
| Q119 | 11 | output_form | "BERT (bert-base-uncased): L=12, H=768, A=12, total parameters = 110M; where L is number of layers (i.e., Transformer blocks), H is the hidden size, and A is the number of self-attention heads." |
| Q120 | 11 | output_form | "DistilBERT (distilbert-base-uncased): it is a distilled version of the BERT model consists of 6-layer, 768-hidden, 12-heads, 66M parameters." |
| Q121 | 11 | output_form | "RoBERTa (roberta-large): it is using the BERT-large architecture consists of 24-layer, 1024-hidden, 16-heads, 355M parameters." |
| Q122 | 11 | output_form | "In Table 18 and 19, we provide detail results for different datasets (English Tweets) with different models." |
| Q123 | 13 | output_ontology | "Table 12: Class label mapping and grouping for CrisisLex, CrisisNLP, ISCRAM2013, and SWDM2013 datasets. The symbol (✗) indicates we do not map the tweets with that label for this study." |
| Q124 | 14 | output_ontology | "The symbol (✗) indicates we do not map the tweets with that label for this study." |
| Q125 | 15 | output_ontology | "Table 16: Class label mapping for AIDR system." |
| Q126 | 16 | input_form | "Sim. refers to similarity value. Dup. refers to whether we consider them as duplicate and filtered." |
| Q127 | 16 | input_form | "The symbol (✗) indicates a duplicate, which we dropped and the symbol (✓) indicates a not duplicate, which we have included in our dataset." |

---

## Regional Context

```yaml
name: Argentina — Buenos Aires Policy Maker Cohort (Disaster Reporting Reliability)
abbreviation: ARG-BA-PolicyDisaster
country: Argentina
sub_national_focus: Buenos Aires Metropolitan Area (AMBA), with secondary relevance
  to Pampa/Patagonia agricultural zones, Río de la Plata river basin communities,
  and informal settlement (villa) populations
deployment_use_case: AI-assisted evaluation of disaster-related reporting reliability
  and trustworthiness across news, social media, and press channels, for consumption
  by policy makers and government agencies in Buenos Aires assessing crisis communication
  quality.
target_population:
  description: Argentine policy makers, emergency management officials, and government
    analysts concentrated in the Buenos Aires metropolitan area. This is a high-education,
    professionally specialized cohort (master's degree or above), operating within
    government ministries and emergency management agencies. They consume and evaluate
    crisis communications across formal press, institutional releases, and social
    media channels.
  education_level: Master's degree or above
  socioeconomic_profile: Upper-middle class; institutional professional context
  primary_role: Crisis communication assessment, disaster response policy, emergency
    management analysis
  english_proficiency: Intermediate-to-advanced; comfortable reading English-language
    benchmarks, methodological documentation, and international standards
  geographic_concentration: Buenos Aires Metropolitan Area (AMBA); Ciudad Autónoma
    de Buenos Aires (CABA) and Gran Buenos Aires (GBA)
  secondary_geographic_relevance:
  - Informal settlement zones (villas) within AMBA
  - Pampa agricultural hinterlands
  - Patagonian zones
  - Río de la Plata and Paraná river basin communities
languages:
  primary: Rioplatense Spanish
  variant_notes: Rioplatense Spanish is distinguished by voseo (use of 'vos' instead
    of 'tú'), yeísmo rehilado (distinct /ll/ and /y/ pronunciation), significant Italian
    loanword influence, and distinctive intonation patterns. Argentine Twitter/X discourse
    features heavy use of lunfardo slang, political satire conventions, and code-switching
    with English technical vocabulary in professional contexts.
  secondary: English (intermediate-to-advanced, professional reading proficiency)
  benchmark_language_alignment: CrisisBench experiments are English-only; the deployment
    population reads English but produces and evaluates Spanish-language content.
    Social media and informal channels are Rioplatense Spanish-dominant. Formal press
    content may follow international conventions more closely.
  social_media_register_notes: Argentine social media discourse — particularly Twitter/X
    — features distinctive registers including political satire, institutional irony,
    colloquial Rioplatense vocabulary, and strong intertextual references to local
    political actors and events. These conventions are absent from the benchmark's
    English North American training corpus.
  script: Latin alphabet with standard Spanish diacritics (á, é, í, ó, ú, ü, ñ)
literacy_and_education:
  national_literacy_rate: '98.08% (INDEC Censo 2022 — [WEB-1]).
    Note: the 2022 census did not include a direct literacy question; the figure derives
    from prior INDEC estimates carried forward. The 2010 census reported 1.9% illiteracy.
    Consistently cited at 98–99% by UNESCO and regional sources (e.g., [WEB-2]).'
  target_cohort_literacy: Effectively 100% — master's degree or above professional
    population
  digital_literacy: High within target cohort; intermediate-to-advanced digital and
    media literacy expected among policy professionals
  notes: Literacy gap for informal settlement (villa) populations is relevant as secondary
    context for assessing coverage of impact populations, but the primary analyst
    cohort is uniformly high-literacy. Functional literacy (comprehension-level reading)
    is estimated to be noticeably lower than headline rates, a distinction relevant
    to how crisis communications are designed for general public consumption — though
    not directly affecting the professional analyst cohort.
infrastructure_notes:
  internet_penetration_argentina_national: 88.4% of total population (40.58 million
    internet users) as of January 2024, per DataReportal/CABASE — [WEB-3];
    corroborated by U.S. ITA country guide — [WEB-4].
    Freedom House (2024) reports approximately 38 million mobile internet users and
    8.17 million fixed-line subscriptions as of Q1 2024 — [WEB-5].
    UNESCO CETyS assessment records household penetration at 90% — [WEB-6].
  internet_penetration_buenos_aires_metro: 'AMBA and Buenos Aires province are the
    most connected regions: 71% of fixed-line internet subscriptions nationally are
    concentrated in five jurisdictions — CABA, Buenos Aires province, Córdoba, Santa
    Fe, and Mendoza (CABASE 2023 survey, cited in Freedom House 2024 — [WEB-5]).
    CABA and Buenos Aires province together account for the largest share. Sub-national
    AMBA-specific penetration figure not published separately; national average (88.4%)
    is a floor estimate for AMBA; actual AMBA rate is materially higher given urban
    concentration.'
  mobile_internet_share: Approximately 60% of Argentina's web traffic originates from
    mobile devices; mobile internet users exceed 38 million nationally (Statista 2024
    — [WEB-7]; Freedom
    House 2024 — [WEB-5]).
    62.14 million cellular connections active in early 2024 (135.3% of population),
    reflecting multi-SIM use.
  dominant_devices_target_cohort: Desktop/laptop workstations in government offices;
    smartphones for social media monitoring
  social_media_platforms_relevant:
  - Twitter/X (primary for real-time crisis discourse)
  - WhatsApp (informal inter-agency coordination; difficult to monitor formally)
  - Facebook (broader public communication, older demographics)
  - Instagram (visual disaster documentation)
  - Telegram (institutional channels and civil society)
  news_and_press_channels_relevant:
  - 'Télam — CLOSED/DISSOLVED: Télam (Argentina''s state news agency) was suspended
    in March 2024 by President Milei, officially dissolved by Decree 548/2024 in July
    2024, and transformed into ''Agencia de Publicidad del Estado S.A.U.'' (APE S.A.U.),
    which no longer operates as a news wire service. Source: Wikipedia — [WEB-8];
    official Boletín Oficial Decreto 548/2024 — [WEB-9].
    This is a significant institutional change: Télam was Latin America''s largest
    public news agency and a primary wire source for ~500 daily dispatches. Its absence
    restructures the formal press source landscape for the deployment.'
  - Major national newspapers (e.g., La Nación, Clarín, Infobae, Página 12)
  - Provincial and municipal press offices
  - 'SECOM (Secretaría de Comunicación) official releases — current structure: the
    Secretaría de Comunicación Pública (formerly SECOM) operates under the Jefatura
    de Gabinete de Ministros; Milei''s administration restructured media-subsidy flows
    and halted national advertising expenditure to private media in December 2023
    (Freedom House 2024 — [WEB-5])'
  input_modality_for_deployment: Text-only (tweets, news articles, press releases,
    institutional communications); no multimodal requirement
  connectivity_notes: High broadband and mobile connectivity in AMBA professional
    government settings. Rural and villa populations (relevant as impact subjects,
    not primary system users) have lower connectivity — household connectivity below
    60% in remote northern provinces (Corrientes, Formosa, Santiago del Estero) per
    Freedom House 2024 — [WEB-5].
    AMBA professional context faces no material connectivity constraint.
institutional_and_regulatory_context:
  emergency_management_agencies:
  - 'SINAGIR (Sistema Nacional para la Gestión Integral del Riesgo y la Protección
    Civil) — established by Law 27,287 (2016); comprises the National Council and
    Federal Council for Comprehensive Risk Management and Civil Protection. Operates
    the National Disaster Risk Reduction Plan (PNRRD 2025–2029). Source: MHEWC Argentina
    profile — [WEB-10].'
  - 'AFE (Agencia Federal de Emergencias) — created in 2025 by Decree 225/2025 to
    coordinate disaster response and manage SINAGIR, superseding previous coordination
    arrangements. Source: MHEWC Argentina profile — [WEB-10].
    This is a net-new institutional change post-scaffold.'
  - SENAPRED — [NOT FOUND — 'SENAPRED' appears to be the Chilean agency (Servicio
    Nacional de Prevención y Respuesta ante Desastres); no Argentine agency by this
    name was identified. The scaffold tag may have been a mis-attribution. Argentina's
    equivalent function is covered by SINAGIR/AFE structures above.]
  - 'Buenos Aires Province emergency directorate — [NEEDS VERIFICATION — deferred:
    below search budget; sub-national agency name not confirmed in searches; provincial
    civil defense falls under SINAGIR federal structure]'
  - 'CABA emergency management — [NEEDS VERIFICATION — deferred: below search budget;
    CABA has its own emergency management directorate under the Ministerio de Justicia
    y Seguridad de CABA but specific current structure not confirmed]'
  relevant_data_protection_regulation: 'Argentina''s primary data protection law remains
    Ley 25.326 (2000). Post-2021 developments: Disposición 2/2023 issued non-binding
    ''Recomendaciones para una Inteligencia Artificial Fiable'' covering AI systems
    in the public sector, including data protection requirements. Resolución 161/2023
    (AAIP) established a program on transparency and personal data protection in AI
    use. A 2024 Guide for Public and Private Entities on Transparency and Protection
    of Personal Data for Responsible AI further operationalizes these principles.
    Comprehensive binding AI legislation (Bills 3003-D-2024, Senado 1747/23) remains
    under congressional deliberation as of 2025. Source: Regulations.AI Argentina
    overview — [WEB-11]; Nemko/Digital
    2025 AI regulation guide — [WEB-12].'
  press_freedom_and_media_regulation: ENACOM (Ente Nacional de Comunicaciones) remains
    the regulatory body for media and communications. The Milei government halted
    national advertising expenditure to private media in December 2023 (Freedom House
    2024 — [WEB-5]). Télam's
    dissolution (July 2024) was flagged by Reporters Without Borders as a 'worrisome
    symbolic act' for press freedom (Al Arabiya, July 2024 — [WEB-13]).
    No AI-in-media-specific ENACOM policy identified in searches.
  international_standards_orientation: Argentine policy professionals treat Global
    North (North American, UN/OCHA, IFRC) disaster communication standards as reference
    frameworks. Label agreement with internationally-normed benchmarks is expected
    to be moderate-to-high for formal press content.
  label_norm_alignment: International disaster communication taxonomies (ISCRAM-derived,
    OCHA-derived) are recognized reference points for Argentine emergency management
    professionals, reducing expected systematic label disagreement with CrisisBench
    annotations for formal content. Edge cases arise in Argentine public discourse,
    political framing of government response, and informal-channel content.
  government_ai_policy: 'Argentina has a multi-layered, predominantly non-binding
    AI governance framework as of 2025. Key enacted instruments: Disposición 2/2023
    (''Recomendaciones para una Inteligencia Artificial Fiable'' — non-binding public
    sector guidance); Decisión Administrativa 750/2023 (Interministerial AI Table
    within Jefatura de Gabinete); Resolución 161/2023 AAIP (AI transparency and data
    protection program); Resolución 710/2024 (AI Applied to Security Unit — UIAAS).
    Buenos Aires Province issued Resolución 4/2025 with binding guidelines for generative
    AI use in provincial agencies. Santa Fe issued a provincial decree (2726/2025)
    on generative AI in public administration. Comprehensive national AI legislation
    (Bills 3003-D-2024 and Senado 1747/23) remains under deliberation — both adopt
    EU AI Act-style risk tiers but are not yet enacted. Argentina joined GPAI and
    signed UNESCO AI ethics recommendation. Current Milei administration favors lighter
    regulatory touch to support innovation. Sources: Regulations.AI Argentina — [WEB-11];
    Oxford Institute of Technology and Justice Argentina profile — [WEB-14].'
cultural_norms_notes: '- Argentine public discourse exhibits high political polarization;
  crisis reporting is frequently inflected by political framing of government response,
  which differs from more institutionally neutral North American disaster communication
  norms.

  - Argentine journalism tradition features strong opinion and interpretive reporting
  alongside straight news, which may affect informativeness classification at the
  margins.

  - Social media discourse — particularly Twitter/X — features heavy use of political
  satire, irony, lunfardo slang, and referential humor that may misclassify as ''not
  informative'' under North American annotation norms.

  - Institutional credibility cues in Argentine media differ from those in the benchmark
  training corpus: official government sources carry variable credibility depending
  on political context; international organizations (UN, IFRC, Médicos Sin Fronteras)
  may carry higher perceived credibility than domestic agencies in some contexts.

  - Argentine public strongly uses WhatsApp for informal crisis communication; this
  channel is not captured in the benchmark and presents monitoring challenges.

  - Villas (informal settlements) are a structurally distinct impact population with
  specific communicative norms, community radio and neighborhood association channels,
  and vulnerability profiles not represented in benchmark data.

  - The dissolution of Télam (July 2024) materially alters the formal press source
  landscape: the primary state wire service is gone, creating a gap in nationally
  federated official disaster reporting that was previously fed to ~500 media outlets.'
hazard_and_disaster_context:
  primary_hazard_types_for_deployment:
  - Urban flash floods (Buenos Aires city and AMBA — drainage system failures)
  - Río de la Plata and Paraná river basin flooding (sudestada events)
  - Pampero windstorms (rapid cold front passages affecting AMBA and Pampa region)
  - ENSO-driven droughts (agricultural impact on Pampa/Patagonia hinterlands)
  - Heatwaves (urban heat island effects in AMBA)
  - Industrial and infrastructure accidents (port, petrochemical, rail)
  benchmark_hazard_coverage_gap: CrisisBench covers North American and globally reported
    events (Joplin tornado, Hurricane Sandy, 2017 international disasters). No Argentine
    or Latin American disaster events are documented in the eight constituent datasets.
    Pampero events, sudestada flooding, and ENSO-cycle agricultural impact are absent
    from the taxonomy.
  sub_label_gaps_flagged_by_users:
  - Pampero windstorm events (distinct meteorological signature and impact pattern)
  - ENSO-driven drought cycles affecting Pampa agricultural zones
  - Río de la Plata / Paraná flooding and sudestada events
  - Villa (informal settlement) impact framing — distinct vulnerability profile and
    communicative context
  - Urban flash flood in dense metropolitan AMBA context
  iscram_taxonomy_adaptation_status: '[NOT FOUND — searched ISCRAM, OCHA, and humanitarian
    taxonomy literature; no evidence of a South American or Ibero-American adaptation
    of ISCRAM or OCHA humanitarian classification taxonomies specifically addressing
    Argentine hazard sub-types (pampero, sudestada, ENSO-drought) was identified.
    TREC-IS developed a 25-category ontology in collaboration with emergency management
    practitioners (2018–2021 — [WEB-15]), but coverage is North
    American/European and does not include Argentine hazard types. This absence confirms
    a genuine taxonomy gap rather than a documentation gap.]'
benchmark_alignment_notes:
  benchmark: CrisisBench (2021)
  domain: Crisis/disaster social media classification
  deployment_channel_vs_benchmark_channel: Deployment spans Twitter/X, news articles,
    and press releases. CrisisBench is exclusively tweet-derived. Cross-channel generalization
    to longer-form news and institutional press content is not evaluated in the benchmark
    and represents a structural gap.
  language_alignment: Benchmark experiments are English-only. Deployment primary channel
    is Rioplatense Spanish. Formal press content may tolerate this gap better than
    social media; informal social media content is the highest-risk channel for misclassification.
  spanish_content_in_benchmark: 'CrisisLex (a CrisisBench constituent) does include
    a small Spanish-language subset: approximately 2,100 tweets in Spanish from the
    2010 Chilean earthquake (ChileEarthquakeT1 collection), labeled by six annotators
    for relatedness. Source: CrisisLex data collections — [WEB-16].
    However, this content is: (a) Chilean, not Argentine/Rioplatense Spanish; (b)
    2010 vintage; (c) labeled only for binary relatedness, not humanitarian type;
    and (d) not the primary benchmark split used in CrisisBench classification experiments
    (which are English-only). A 2022 arXiv paper (Sánchez et al., arXiv:2209.02139)
    explicitly studies cross-lingual and cross-domain crisis classification for low-resource
    scenarios, including Spanish, but does not cover Rioplatense-specific conventions
    — [WEB-17]. The Spanish content in CrisisBench is
    thus negligibly relevant to Argentine Rioplatense deployment.'
  output_space_gap: The deployment's core requirement is source credibility and signal-to-noise
    reliability scoring, which is absent from the benchmark's output taxonomy (binary
    informativeness + multi-class humanitarian type). The user intends to construct
    credibility scoring downstream by combining model outputs with external metadata
    (source popularity, institutional affiliation). This represents a user-acknowledged
    but structurally significant gap.
  output_form_gap: Benchmark produces discrete classification labels (weighted F1).
    Deployment envisions an aggregated continuous credibility score. Downstream transformation
    pipeline is required.
  annotator_population_gap: Annotation provenance is minimally documented for six
    of eight source datasets. The CrisisNLP paper (Imran et al. 2016) confirms that
    most datasets used crowdsourced workers with three independent labels per tweet
    required for task finalization — [WEB-18]. Expected
    annotator population is North American/European crowdsourced workers. Argentine
    institutional and journalistic norms for what constitutes a credible or informative
    disaster signal are not represented. Cross-dataset F1 degradation (14.3%) signals
    label conventions are not fully portable across event contexts.
  temporal_gap: CrisisBench events span 2010–2017. Argentine crisis communication
    practices, social media norms, and institutional landscape have evolved since
    2017. Current Twitter/X platform changes (post-2022) are not reflected.
  credibility_scoring_extensions: TREC Incident Streams (TREC-IS, 2018–2021) introduced
    a priority/criticality scoring dimension (Low/Medium/High/Critical) for disaster
    tweets alongside a 25-category information-type ontology, developed in collaboration
    with emergency management practitioners — [WEB-15]; [WEB-19].
    This is the closest existing benchmark extension to the deployment's credibility/priority
    scoring requirement. TREC CrisisFACTS (2022–2023) extends TREC-IS into multi-stream
    (Twitter, Facebook, Reddit, online news) event summarization with fact-based evaluation,
    covering 8–18 crisis events — [WEB-20]. Neither TREC-IS
    nor CrisisFACTS covers Argentine or Latin American events, and both remain primarily
    North American in geographic scope. A 2024 survey (arXiv:2410.21360) systematically
    reviews 175 NLP works on credibility assessment, identifying research fragmentation
    and a lack of integrated multi-signal approaches — [WEB-21].
    No single post-2021 crisis NLP benchmark provides an end-to-end credibility/veracity
    scoring layer directly applicable to the Argentine deployment.
  cross_channel_transfer_studies: No dedicated study was identified that evaluates
    CrisisBench-trained classifiers on news articles or press releases. Domain adaptation
    literature in crisis NLP is primarily cross-event or cross-language (tweet-to-tweet),
    not cross-channel (tweet-to-news-article). TREC CrisisFACTS (2022–2023) incorporates
    multi-stream data including online news alongside social media — [WEB-20]
    — and is the closest available framework for cross-channel crisis NLP, but does
    not provide transfer performance benchmarks between tweet classifiers and news
    article classifiers. This gap remains unresolved in the literature.
  cross_lingual_crisis_classification_note: A 2022 arXiv paper (Sánchez et al., arXiv:2209.02139)
    directly studies cross-lingual and cross-domain crisis classification for low-resource
    scenarios, framing the challenge of applying English-trained models to other languages
    and unseen event types — [WEB-17]. Findings are relevant
    to the Argentine deployment but do not specifically address Rioplatense Spanish
    register, Argentine hazard types, or the political-satire/irony dimensions of
    Argentine social media.
dimension_priority_weights:
  input_ontology:
    priority: MODERATE
    rationale: Top-level disaster categories broadly adequate; absence of Argentine
      hazard sub-labels and informal-settlement impact framing is a coverage gap users
      flagged as desirable to fill but not blocking.
  input_content:
    priority: HIGH
    rationale: Social media channel — central to deployment — carries Rioplatense
      Spanish conventions, political satire, lunfardo register, and Argentine institutional
      credibility cues absent from the benchmark's English North American training
      corpus. The only Spanish content in CrisisBench constituent datasets is a small
      Chilean earthquake collection (~2,100 tweets, 2010), not Rioplatense and not
      used in classification experiments.
  input_form:
    priority: LOWER
    rationale: Deployment is text-only; target cohort has strong English proficiency;
      benchmark is likewise text-only. No signal-distribution mismatch anticipated
      at the input modality level, though cross-channel (tweet vs. news article) generalization
      is an open question with no published benchmark resolution.
  output_ontology:
    priority: HIGH
    rationale: Deployment's core requirement — source credibility and signal-to-noise
      reliability scoring — is not natively present in the benchmark's output taxonomy,
      requiring downstream construction. TREC-IS offers the closest precedent (priority
      criticality labels) but covers no Argentine events and is tweet-only.
  output_content:
    priority: MODERATE
    rationale: Argentine professionals largely accept international disaster communication
      label conventions for formal content, limiting systematic disagreement; informal
      content channels introduce annotator-population mismatch risk at margins. CrisisNLP
      annotation protocol used crowdsourcing with three-annotator agreement threshold
      — annotator demographics not published but almost certainly non-Argentine.
  output_form:
    priority: MODERATE
    rationale: Benchmark's discrete classification label output requires downstream
      transformation to the aggregated credibility score the deployment envisions;
      this gap is user-acknowledged but structurally real.
flagged_gaps_for_web_search:
- gap_id: 1
  dimension: input_content
  description: Spanish-language and Argentine social media content in CrisisBench
  search_target: CrisisBench Spanish-language Argentine disaster tweets Latin America
    crisis NLP benchmark CrisisLex non-English subset
  resolution_status: RESOLVED
  finding: CrisisLex includes a small Chilean earthquake Spanish-language collection
    (~2,100 tweets, 2010) labeled for binary relatedness only, not used in CrisisBench
    classification experiments. No Argentine or Rioplatense Spanish content is present
    in the benchmark. A cross-lingual/cross-domain crisis NLP paper (arXiv:2209.02139,
    2022) addresses low-resource Spanish but not Rioplatense-specific conventions.
    Gap confirmed as full.
- gap_id: 2
  dimension: input_ontology
  description: Sub-label granularity for Argentine hazard types and informal-settlement
    impact framing in ISCRAM or OCHA taxonomies
  search_target: ISCRAM humanitarian taxonomy South America Argentina disaster classification
    pampero flooding informal settlements adaptation
  resolution_status: RESOLVED (not found)
  finding: No South American or Ibero-American adaptation of ISCRAM or OCHA taxonomies
    addressing pampero, sudestada, or ENSO-drought sub-types was found. TREC-IS 25-category
    ontology (developed 2018–2021 with emergency practitioners) does not include Argentine
    hazard types. Gap confirmed as full.
- gap_id: 3
  dimension: output_ontology
  description: Source credibility and reliability scoring dimensions in post-2021
    crisis NLP benchmarks
  search_target: crisis NLP credibility scoring benchmark CREDBANK CrisisMMD TREC-IS
    veracity disaster social media post-2021
  resolution_status: RESOLVED (partial coverage found)
  finding: TREC-IS (2018–2021) introduced priority/criticality labels (Low/Medium/High/Critical)
    for disaster tweets alongside 25 information types — the closest existing benchmark
    extension to the deployment's priority scoring need. TREC CrisisFACTS (2022–2023)
    extends this to multi-stream (social media + news) event summarization. Neither
    covers Argentine events. A 2024 NLP credibility survey (arXiv:2410.21360) documents
    research fragmentation in this space. No single benchmark provides an end-to-end
    credibility/veracity scoring layer applicable to the deployment.
- gap_id: 4
  dimension: output_content
  description: Annotator demographics, inter-annotator agreement, and label provenance
    for CrisisBench constituent datasets
  search_target: CrisisLex CrisisNLP annotator demographics inter-annotator agreement
    crowdsourcing crisis dataset annotation protocol Argentina
  resolution_status: RESOLVED (partial)
  finding: CrisisNLP (Imran et al. 2016, LREC) confirms crowdsourced annotation with
    three-annotator agreement threshold, using volunteers/paid workers via platforms.
    Annotator demographics are not published for any constituent dataset. CrisisLex
    T6 used crowdsourcing workers for relatedness labels. No Argentine annotators
    or Argentine-norm calibration is documented anywhere in the provenance chain.
    Gap confirmed.
- gap_id: 5
  dimension: input_form
  description: Cross-channel generalization from tweets to news articles and press
    releases
  search_target: crisis NLP tweet to news article domain adaptation transfer disaster
    classification press release generalization
  resolution_status: RESOLVED (not found)
  finding: No dedicated study evaluating CrisisBench-trained classifiers on news articles
    or press releases was identified. TREC CrisisFACTS (2022–2023) incorporates multi-stream
    data including news but does not provide cross-channel transfer benchmarks. Cross-channel
    (tweet-to-news) generalization remains an unresolved gap in the crisis NLP literature.
- gap_id: 6
  dimension: output_form
  description: Aggregated credibility score construction combining classification
    outputs with external metadata
  search_target: disaster classification credibility aggregation external metadata
    source popularity institutional affiliation humanitarian NLP policy maker score
  resolution_status: RESOLVED (partial — general credibility aggregation literature
    exists, no disaster-specific pipeline found)
  finding: The 2024 NLP credibility survey (arXiv:2410.21360) reviews 175 works on
    automatic credibility assessment, identifying that aggregating multiple credibility
    signals into a unified score remains fragmented and underspecified. No published
    pipeline specifically combining CrisisBench classification outputs with external
    source metadata (institutional affiliation, popularity) for policy-maker consumption
    was identified. The downstream construction step is user-acknowledged and remains
    a research gap.
- gap_id: 7
  dimension: institutional_context
  description: Current Argentine emergency management agency structure (SINAGIR, SENAPRED)
    and Télam operational status
  search_target: Argentina SINAGIR emergency management structure 2024 Télam news
    agency status ENACOM AI media regulation
  resolution_status: RESOLVED
  finding: SINAGIR (Law 27,287, 2016) remains the national system. AFE (Agencia Federal
    de Emergencias) was created by Decree 225/2025 as the new operational emergency
    response coordinator under SINAGIR. Télam was suspended March 2024 and officially
    dissolved by Decree 548/2024 in July 2024, replaced by APE S.A.U. (Agencia de
    Publicidad del Estado), a state advertising entity with no news-wire function.
    'SENAPRED' is a Chilean agency; no Argentine equivalent by that name exists.
- gap_id: 8
  dimension: institutional_context
  description: Argentine national AI policy and ministry-level guidelines for AI-assisted
    monitoring systems
  search_target: Argentina national AI strategy 2023 2024 ministry government AI adoption
    guidelines crisis communication
  resolution_status: RESOLVED
  finding: 'Argentina has a multi-instrument, primarily non-binding AI governance
    framework. Key enacted: Disposición 2/2023 (public sector AI ethical principles);
    Decisión Administrativa 750/2023 (Interministerial AI Table); Resolución 161/2023
    AAIP (AI transparency program); Resolución 710/2024 (UIAAS security AI unit);
    Buenos Aires Province Resolución 4/2025 (binding generative AI guidelines for
    provincial agencies). Comprehensive binding national AI legislation remains under
    congressional deliberation. The Milei administration favors lighter regulatory
    touch. An AI-assisted disaster communication monitoring system would currently
    be governed primarily by Ley 25.326 data protection, sector-level guidance from
    AAIP, and any applicable provincial Buenos Aires Province resolution.'
net_new_fields:
  telam_dissolution_impact: 'Télam — Argentina''s state news wire, which distributed
    ~500 daily reports to ~300 media subscribers and served as the primary formally-attributed
    institutional source for disaster and emergency reporting — was dissolved in July
    2024 (Decree 548/2024). Its replacement, APE S.A.U., is an advertising agency
    with no news-wire function. This materially changes the formal press source landscape
    the deployment will monitor: a key institutional credibility anchor for official
    disaster communications is absent from post-July 2024 content. Deployment systems
    trained or evaluated on pre-2024 Argentine press content will encounter a structurally
    different source distribution. Source: Boletín Oficial Decreto 548/2024 — [WEB-9];
    IDEA.int March 2024 — [WEB-22].'
  afe_creation_2025: 'The Agencia Federal de Emergencias (AFE) was created by Decree
    225/2025 as the new operational federal emergency response coordinator, responsible
    for deploying disaster response resources and coordinating SINAGIR. This supersedes
    previous fragmented coordination arrangements. Policy makers in the deployment
    context will interact with AFE as the primary federal counterpart for crisis communications,
    replacing older coordination structures. Source: MHEWC Argentina profile — [WEB-10].'
  trec_is_priority_scoring_precedent: 'TREC Incident Streams (2018–2021) is the closest
    existing benchmark to the deployment''s credibility/priority requirement: it classifies
    disaster tweets into 25 information types AND assigns a priority label (Low/Medium/High/Critical)
    evaluated via priority-centric DCG. The dataset spans 98 crisis events with 136,000+
    labeled tweets. However, it covers no Argentine or Latin American events and is
    Twitter-only. TREC CrisisFACTS (2022–2023) extends this to multi-stream (Twitter,
    Reddit, Facebook, online news) summarization with 18 events. Both tracks offer
    reusable ontologies and evaluation frameworks that could inform the deployment''s
    credibility scoring construction. Sources: TREC-IS 2021 — [WEB-15];
    CrisisFACTS — [WEB-20].'
  crisislex_chilean_spanish_subset: 'CrisisLex includes a Chilean earthquake Spanish-language
    collection (ChileEarthquakeT1: ~2,100 tweets, 2010, labeled for binary relatedness
    by six annotators). This is the only Spanish-language South American disaster
    content in the CrisisBench ecosystem. It is not used in CrisisBench classification
    experiments, predates modern Argentine Twitter norms by over a decade, and reflects
    Chilean (not Rioplatense) Spanish. Its presence provides negligible mitigation
    of the Spanish-language input content gap. Source: CrisisLex data collections
    — [WEB-16].'
  cross_lingual_crisis_classification_paper: 'A 2022 arXiv paper (Sánchez et al.,
    ''Cross-Lingual and Cross-Domain Crisis Classification for Low-Resource Scenarios'',
    arXiv:2209.02139) directly addresses the challenge of applying English-trained
    crisis classifiers to low-resource languages and unseen event types, which is
    structurally similar to the Argentine deployment challenge. The paper does not
    specifically address Rioplatense Spanish register or Argentine hazard types, but
    provides methodological grounding for cross-lingual transfer approaches that could
    be adapted for Argentine deployment. Source: [WEB-17].'
  buenos_aires_province_ai_resolution_2025: 'Buenos Aires Province issued Resolución
    4/2025, establishing binding guidelines for generative AI use by provincial government
    agencies. This is directly relevant to the deployment context (AMBA policy makers
    operating within Buenos Aires Province government). Requirements include human
    oversight and data protection safeguards. This resolution constitutes the most
    immediately applicable regulatory instrument for the deployment. Source: Regulations.AI
    Argentina — [WEB-11].'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.perfil.com/noticias/sociedad/el-censo-argentino-arrojo-98-de-alfabetizacion-en-el-pais-pero-no-se-refleja-en-las-aulas.phtml |
| WEB-2 | https://es.theglobaleconomy.com/Argentina/Literacy_rate/ |
| WEB-3 | https://datareportal.com/reports/digital-2024-argentina |
| WEB-4 | https://www.trade.gov/country-commercial-guides/argentina-digital-economy |
| WEB-5 | https://freedomhouse.org/country/argentina/freedom-net/2024 |
| WEB-6 | https://www.unesco.org/en/articles/assessing-internet-development-argentina |
| WEB-7 | https://www.statista.com/topics/6709/internet-usage-in-argentina/ |
| WEB-8 | https://en.wikipedia.org/wiki/T%C3%A9lam |
| WEB-9 | https://www.boletinoficial.gob.ar/detalleAviso/primera/309815/20240701 |
| WEB-10 | https://www.mhewc.org/argentina/ |
| WEB-11 | https://regulations.ai/regulations/argentina-summary |
| WEB-12 | https://digital.nemko.com/regulations/ai-regulation-argentina |
| WEB-13 | https://english.alarabiya.net/News/world/2024/07/02/argentina-government-shuts-state-news-agency-telam |
| WEB-14 | https://www.techandjustice.bsg.ox.ac.uk/research/argentina |
| WEB-15 | https://trecis.github.io/ |
| WEB-16 | https://crisislex.org/data-collections.html |
| WEB-17 | https://arxiv.org/abs/2209.02139 |
| WEB-18 | https://aclanthology.org/L16-1259.pdf |
| WEB-19 | https://www.dcs.gla.ac.uk/~richardm/TREC_IS/2018/Evaluation.html |
| WEB-20 | https://crisisfacts.github.io/ |
| WEB-21 | https://arxiv.org/html/2410.21360v2 |
| WEB-22 | https://www.idea.int/democracytracker/report/argentina/march-2024 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark under assessment provides a fixed set of disaster/impact categories. For disaster reporting reliability in Argentina, are there impact categories that matter to your policy makers but might not appear in a benchmark of this kind — for example, impacts on informal settlements (villas), agricultural disruption in Pampa or Patagonia, or flooding along the Río de la Plata basin? Are there disaster types (e.g., pampero windstorms, ENSO-driven droughts, urban flash floods in Buenos Aires) whose reporting patterns your users need to evaluate?
A1: The existing benchmark labels are broadly sufficient to cover Argentine disaster types; however, sub-labels or finer-grained categories (e.g., distinguishing specific impact populations or regional hazard types) would be valuable but are absent.

Q2 [IC]: The benchmark's input content is drawn from a specific source culture and media environment that may reflect particular disaster framing, infrastructure norms, and institutional actors. For your Argentine policy makers assessing reporting reliability, would culturally embedded assumptions in such data — such as which agencies are cited as authoritative, what counts as 'normal' disaster response, or how agricultural loss is framed — misalign with what Argentine news sources or government communications typically convey?
A2: Cultural embedding is not expected to be problematic for formal press and news articles, but social media and informal content channels likely carry meanings, norms, and communicative conventions not well represented in a benchmark drawn from a different cultural context.

Q3 [OO]: Your deployment centers on distinguishing noisy or unreliable signals from verified disaster reporting — a reliability or trustworthiness judgment — rather than simply classifying impact type or content type. Does your use case require a scoring dimension for source credibility, misinformation likelihood, or signal-to-noise quality, which may not map onto the benchmark's output space and scoring dimensions?
A3: Source credibility scoring is the ideal output, but the user envisions building this on top of the benchmark's existing classification outputs by combining model results with external metadata (e.g., source popularity, institutional affiliation) — so the benchmark's output taxonomy is treated as a necessary but insufficient foundation rather than a direct mismatch.

Q4 [OC]: The benchmark's ground-truth labels were likely produced by annotators familiar with disaster communication norms from a different cultural context than your deployment. For your context, would Argentine policy experts, emergency management officials, or journalists plausibly disagree with those labels — for instance, on whether a given report constitutes a 'real signal' of disaster impact versus noise — especially given differences in how Argentine media covers government response or social vulnerability?
A4: Argentine crisis communication norms are less institutionally settled than in North America/Canada; however, Argentine policy professionals tend to draw on international (Global North) standards as reference points, and local press broadly follows those conventions. Consequently, label disagreement with benchmark annotations derived from that normative context is expected to be limited, though the more fluid Argentine public discourse may produce edge cases.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | Top-level disaster categories are broadly adequate for Argentine hazards, but the absence of sub-labels for region-specific hazards and informal-settlement impacts creates a coverage gap that users explicitly flagged as desirable. |
| IC | HIGH | Social media and informal content — a core channel in the deployment — is expected to carry culturally embedded meanings and communicative norms not represented in benchmark data drawn from a different cultural context, even if formal press content is less affected. |
| IF | LOWER | The deployment is text-only, targets high-resource Rioplatense Spanish speakers with strong English proficiency, and the benchmark is likewise text-only; no signal-distribution mismatch is anticipated. |
| OO | HIGH | The benchmark's output space covers informativeness and humanitarian type classification, but the deployment's core requirement — source credibility and signal-to-noise reliability scoring — is not natively present in that taxonomy, requiring additional construction on top of model outputs. |
| OC | MODERATE | Argentine professionals largely accept international disaster communication label conventions, reducing systematic label disagreement; however, the more fluid Argentine public discourse and informal content channels introduce annotator-population mismatch risk at the margins. |
| OF | MODERATE | The benchmark produces classification labels while the deployment envisions an aggregated credibility score combining model output with external metadata; this downstream transformation is user-acknowledged but represents a structural gap between benchmark output form and operational deployment need. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** QCRI/CrisisBench-all-lang (configs: `humanitarian`, `informativeness`)
**Analysis date:** 2025-01-30
**Examples reviewed:** 131 (humanitarian, train split) + 140 (informativeness, train split) = 271 total
**Columns shown:** id, event, source, text, lang, lang_conf, class_label
**Columns skipped (media):** none (text-only dataset)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | humanitarian | Ex. 19 | displaced_and_evacuations | "El trabajo de la mejor Daniela López que conozco en pantalla grande #mataraunhombe #chile #cinema… http://t.co/asAx6KqNvD" | Spanish tweet about Chilean film, labelled displaced/evacuations — apparent annotation error | OC |
| D2 | humanitarian | Ex. 83 | sympathy_and_support | "RT @FlorrGo: #FuerzaChile ,un 2 de abril ... Que vengan los ingleses a ayudarlos ahora ... A la larga o a la corta ,todo vuelve" | Chilean Spanish earthquake solidarity tweet — not Argentine/Rioplatense | IC |
| D3 | humanitarian | Ex. 106 | sympathy_and_support | "Que lindo saber que en mi ciudad bella #Iquique hay gente con un corazón enorme dispuestos a ayudar... Emocionada" | Chilean Spanish (Iquique city) solidarity tweet — Chilean, not Argentine | IC |
| D4 | informativeness | Ex. 88 | not_informative | "#FuerzaChile jaja y piden ayuda jaja que los ayuden los ingleses manga de traidores" | Chilean Spanish tweet expressing contempt for requesting outside help — not Argentine | IC |
| D5 | informativeness | Ex. 89 | informative | "Declaran tres días de luto nacional por accidente de tren en España: Testigos afirman que el tren… http://t.co/pAcRQGdjFv" | Spanish-language tweet about Spain train crash | IC |
| D6 | informativeness | Ex. 37 | informative | "IMPRESIONANTE terremoto Chile camara de seguridad farmacia - NEW VIDEO E...: http://t.co/bkUElKfFUj vía @YouTube" | Chilean Spanish earthquake tweet — Chilean Spanish, not Rioplatense | IC |
| D7 | informativeness | Ex. 127 | informative | "RT @marieli_d: Nuevamente se incendia #Amuay http://t.co/AiWlhgy3" | Venezuelan Spanish tweet about refinery explosion | IC |
| D8 | humanitarian | Ex. 117 | not_humanitarian | "RT @meteomostoles: El tifón #BOPHA,de cat.4 y 947hPa en su centro,va camino de Filipinas.Lleva vientos sostenidos entre 2010 y 249km/h h ..." | Spanish tweet about Philippines typhoon — meteorological content labelled not_humanitarian | OC |
| D9 | informativeness | Ex. 106 | not_informative | "Ojo con el exceso de ayuda por los efectos del #TerremotoenChile porque puede producir mucho más obstáculos de lo que se cree." | Chilean Spanish warning about over-donation — labelled not_informative despite substantive crisis-relevant content | OC |
| D10 | humanitarian | Ex. 102 | infrastructure_and_utilities_damage | "Middle East right now:\nIS about to seize Ramadi\nAl-Qaeda seizes Yemen airport\nSaudi regime executes Indonesian women\nIran exports terrorism" | Political/conflict tweet from AIDR labelled infrastructure damage — apparent mislabel | OC |
| D11 | informativeness | Ex. 1 | informative | "when the ambushes of this century, hold closes even when life puts you in discomfiture, hold closes even that one of condescends your family, so God will facilitate you shortcoming" | Philosophical/religious text labelled informative — no disaster content | OC |
| D12 | informativeness | Ex. 3 | informative | "Sweater weather indeed 🌂 #RubyPH" | Short weather comment during typhoon labelled informative — minimal disaster signal | OC |
| D13 | informativeness | Ex. 7 | informative | "i hope everyone is safe" | Generic safety wish labelled informative | OC |
| D14 | informativeness | Ex. 83 | informative | "This hurricane thingy is looking pretty scary! I'm kinda excited by insane weather..." | Personal reaction labelled informative | OC |
| D15 | informativeness | Ex. 121 | informative | "one of the boston bombing suspects looks a bit like rob kardashian. do I have to wait for the new series to find out" | Celebrity comparison tweet during crisis labelled informative | OC |
| D16 | humanitarian | Ex. 9 | not_humanitarian | "New saying for the day... RG 3 and out - A #Steelers fan at the bar" | Sports commentary during Hurricane Sandy — clear not_humanitarian example | OO |
| D17 | humanitarian | Ex. 26 | personal_update | "Tornado watch until 3am. Of course we just got our new garage door today. *sigh*" | Personal complaint about tornado watch — Joplin 2011, North American event | IC |
| D18 | humanitarian | Ex. 11 | personal_update | "RT @tarnsnastylad: They need to name hurricanes better!.. superstorm Sandy? Seriously??.. Sounds like a FUCKING gay wrestler!" | Crude personal opinion during Sandy — North American vernacular | IC |
| D19 | humanitarian | Ex. 16 | affected_individual | "Floods kill 3, 75,000 forced from Calgary homes http://t.co/c6OPFjFLkA | AP #news" | News headline about Canadian flood — affected individuals, clear label | OO |
| D20 | humanitarian | Ex. 2 | caution_and_advice | "As many as 100,000 people could be forced from their homes by heavy flooding in western Canada. Water levels peak today at noon." | Factual caution about Canadian floods | OO |
| D21 | humanitarian | Ex. 57 | caution_and_advice | "RT @frankowolf1: il comune di Mirandola cerca ing. e arch. contattare Polizia Municipale: 0535/611039, 800/197197 #terremoto" | Italian tweet seeking engineers after earthquake — non-English caution | IC/IF |
| D22 | humanitarian | Ex. 30 | sympathy_and_support | "Mi è piaciuto un video di @YouTube: http://t.co/l5MttNyHPa Alluvione in Sardegna: commenti idioti" | Italian tweet about Sardinia floods — "liked a video about idiotic comments on flooding" | IC |
| D23 | humanitarian | Ex. 44 | sympathy_and_support | "Lac-Mégantic: Éric Forest sur place pour donner son appui http://t.co/wKSAXEtZWm" | French tweet about Canadian train crash — politician on site | IC |
| D24 | humanitarian | Ex. 113 | sympathy_and_support | "RT @portalR7: Tragédia no RS: Dilma chora ao falar sobre vítimas http://t.co/ybxETDmD #R7 #SantaMaria" | Portuguese tweet about Brazil nightclub fire, Dilma crying | IC |
| D25 | humanitarian | Ex. 95 | infrastructure_and_utilities_damage | "After deadly Brazil nightclub fire, safety questions emerge. http://t.co/ah4JK2v2" | Brazil nightclub fire — closest geographic proximity to Argentina | IO |
| D26 | humanitarian | Ex. 6 | infrastructure_and_utilities_damage | "The flood is feared to submerge the bridge roads leading Larkana and Khairpur districts." | Pakistan flood infrastructure — no Argentine geographic relevance | IC |
| D27 | humanitarian | Ex. 49 | infrastructure_and_utilities_damage | "Torrential rains have damaged Kenya's infrastructure, severing road links between Nairobi and Garissa, where the air base of the World Food Programme (WFP) is located." | Africa infrastructure damage — internationally framed | IC |
| D28 | informativeness | Ex. 34 | not_informative | "A tropical cyclone will affect my area. Winds of greater than 100 kph up to 185 kph may be expected in at least 18 hours. #TyphoonHagupit" | Substantive typhoon warning labelled not_informative — clear label inconsistency | OC |
| D29 | informativeness | Ex. 6 | not_informative | "#sobering Helicopter crash into pub in #glasgow! http://t.co/0uYSOocUvu" | Breaking news tweet labelled not_informative | OC |
| D30 | informativeness | Ex. 52 | not_informative | "Bangladesh:palazzo non era per fabbriche: Il progetto del Rana Plaza prevedeva solo 6 piani non 9 o 10 http://t.co/VG9qCqa3xX" | Italian investigative tweet about Rana Plaza building code — labelled not_informative | OC |
| D31 | humanitarian | Ex. 25 | other_relevant_information | "Update on the fertilizer explosion in West, Texas. Estimated 50 to 60 dead, hundreds injured, half of town flattened." | North American industrial explosion — would fit affected_individuals or injured_dead | OO |
| D32 | humanitarian | Ex. 52 | other_relevant_information | "being in a hurricane inside a house with no lights ..." | Personal experience tweet labelled other_relevant_information | OC |
| D33 | humanitarian | Ex. 111 | other_relevant_information | "Check out these award winning Long Island renovations: #longisland #suffolk https://t.co/wLnIbOENK9" | Completely unrelated home renovations tweet in other_relevant_information | OC |
| D34 | informativeness | Ex. 111 | informative | "RT @cityofcalgary: Acting Fire Chief, Ken Uzeloc, will address the media at Ogden Road and 17 Street S.E. at 10 p.m. #yyc #yycflood" | Official municipal announcement — clear informative label, Canadian context | OO |
| D35 | humanitarian | Ex. 28 | requests_or_needs | "I'M ASKING HELP FOR MY FAMILY WHICH IS VICTIM AND WHICH TAKE REFUGE IN PROVINCE." | Direct help request from disaster victim | OO |
| D36 | humanitarian | Ex. 42 | requests_or_needs | "We have water but we need food. Please in Masson Leogane." | Haiti-context needs request — Global South event | IO |
| D37 | humanitarian | Ex. 90 | requests_or_needs | "Equipped with a power generator and air conditioner, the tents can also house an emergency medical center." | Capability description mislabelled as requests_or_needs — annotation inconsistency | OC |
| D38 | humanitarian | Ex. 98 | requests_or_needs | "AmeriCares solicits donations of medicines, medical supplies, and other relief materials from manufacturers, and delivers them quickly and reliably to indigenous health and welfare professionals in 137 countries around the world." | NGO capability description labelled requests_or_needs — mislabel | OC |
| D39 | humanitarian | Ex. 1 | affected_individual | "@lucilledizon: 517 ilang ilang st. bayanihan vilage cainta rizal, David Bautista +63 905 826 5094. Needs rescue @MMDA @govph #rescuePH" | Tagalog rescue request — non-English, Philippine event, clear label | IF |
| D40 | humanitarian | Ex. 79 | infrastructure_and_utilities_damage | "RT @MoralesForLife: Chocolate Hills, napinsala ng Magnitude 7.2 na lindol #PrayForVisayas Pray For Cebu and Bohol also in Mindanao! http://…" | Tagalog tweet about Philippines earthquake damage | IF |
| D41 | informativeness | Ex. 23 | informative | "#Terremoto: secondo Il Foglio &egrave; un Castigo di Dio - foto http://t.co/GuMvqzl0" | Italian earthquake tweet labelled informative | IF |
| D42 | humanitarian | Ex. 14 | response_efforts | "#Tacloban has 49 evacuation centers now sheltering over 30,000 people + @care is helping respond to #typhoonhagupit http://t.co/ePE9MsdpTh" | Clear response effort tweet — CARE NGO involvement | OO |
| D43 | humanitarian | Ex. 3 | disease_related | "Investors Pump Prospects Of Unproven Ebola Treatments: Drugs in development to treat Ebola virus are far from … http://t.co/hv7lcUzha3" | Ebola treatment investor article — disease_related | OO |
| D44 | humanitarian | Ex. 60 | infrastructure_and_utilities_damage | "Colorado floods shut down hundreds of oil and gas wells; recovery will take time: Colorado's oil and... http://t.co/HivwsVtrc8 #Oil #BRK" | North American oil/gas infrastructure damage | IO |
| D45 | informativeness | Ex. 128 | not_informative | "https://t.co/najVJNt4Ip DEATH TOLL Now under Investigation for COVER UP!!! https://t.co/VuGGPYboIv" | Credibility-ambiguous tweet about death toll cover-up labelled not_informative | OO |
| D46 | humanitarian | Ex. 24 | not_humanitarian | "RT @eclecticbrotha: @AlGiordano Damn, I forgot how much of a shitshow Bernie's Puerto Rico operation was." | Political commentary during Hurricane Maria | IC |
| D47 | informativeness | Ex. 31 | informative | "I was told I'm ignorant to think the Boston Bombing wasn't planned by the government to keep our attention away from schemes being planned." | Conspiracy tweet labelled informative | OC |
| D48 | humanitarian | Ex. 33 | disease_related | "Scientists find MERS virus antibodies that may lead to treatments http://t.co/0YAMcmulxD" | MERS treatment research tweet | OO |

---

### Deployment-Relevant Strengths

#### Strength 1: Broad disaster type coverage across humanitarian labels
- **Dimension(s):** IO, OO
- **Observation:** The 15-class humanitarian label schema covers categories directly relevant to Argentine disaster response triage: `affected_individual`, `infrastructure_and_utilities_damage`, `injured_or_dead_people`, `displaced_and_evacuations`, `requests_or_needs`, `response_efforts`, `caution_and_advice`, and `donation_and_volunteering`. These top-level categories map onto the functional needs of Buenos Aires policy makers assessing disaster communication quality regardless of event geography.
- **Deployment relevance:** Argentine emergency management agencies (SINAGIR, AFE) operate within ISCRAM-derived frameworks that recognise these same broad categories. The label schema is thus sufficiently compatible with the international standards Argentine professionals treat as reference points.
- **Datapoint citations:**
  - [D19] Example 16 (humanitarian, train, affected_individual): "Floods kill 3, 75,000 forced from Calgary homes http://t.co/c6OPFjFLkA | AP #news" — straightforward affected-individuals label, clear annotation.
  - [D20] Example 2 (humanitarian, train, caution_and_advice): "As many as 100,000 people could be forced from their homes by heavy flooding in western Canada. Water levels peak today at noon." — clear actionable caution label.
  - [D35] Example 28 (humanitarian, train, requests_or_needs): "I'M ASKING HELP FOR MY FAMILY WHICH IS VICTIM AND WHICH TAKE REFUGE IN PROVINCE." — unambiguous needs signal.
  - [D42] Example 14 (humanitarian, train, response_efforts): "#Tacloban has 49 evacuation centers now sheltering over 30,000 people + @care is helping respond to #typhoonhagupit http://t.co/ePE9MsdpTh" — clear response-efforts label.
  - [D43] Example 3 (humanitarian, train, disease_related): "Investors Pump Prospects Of Unproven Ebola Treatments: Drugs in development to treat Ebola virus are far from … http://t.co/hv7lcUzha3" — disease-related label functions.

#### Strength 2: Binary informativeness task provides a usable signal-triage foundation
- **Dimension(s):** OO, OF
- **Observation:** The informativeness config cleanly separates clearly off-topic social chatter from disaster-relevant content across a wide range of events. The not_informative examples in the sample include sports commentary, celebrity gossip, spam, and personal chitchat, while informative examples range from official municipal announcements to direct eyewitness reports.
- **Deployment relevance:** For Buenos Aires policy makers whose first-pass task is filtering noisy signals from informative crisis content, the binary informativeness layer provides a deployable triage function. Although it does not natively score credibility, it operationalises the first step in the downstream credibility pipeline the user envisions.
- **Datapoint citations:**
  - [D16] Example 9 (humanitarian, train, not_humanitarian): "New saying for the day... RG 3 and out - A #Steelers fan at the bar" — unambiguous noise example.
  - [D34] Example 111 (informativeness, train, informative): "RT @cityofcalgary: Acting Fire Chief, Ken Uzeloc, will address the media at Ogden Road and 17 Street S.E. at 10 p.m. #yyc #yycflood" — official institutional announcement correctly labelled informative.
  - [D36] Example 42 (humanitarian, train, requests_or_needs): "We have water but we need food. Please in Masson Leogane." — clear needs signal from Global South context.

#### Strength 3: Multi-event, multi-geography training distribution
- **Dimension(s):** IC, IO
- **Observation:** The 131 humanitarian examples span at least 20 named events across Asia, North America, South Asia, Europe, the Middle East, and Africa, including floods, earthquakes, hurricanes, disease outbreaks, industrial accidents, and building collapses. This breadth means classifiers trained on this data have exposure to diverse disaster communication registers, not just a single event type.
- **Deployment relevance:** Argentine disaster scenarios span floods, windstorms, earthquakes (low risk), and industrial accidents. A classifier trained on event-diverse data is less likely to fail categorically on event types that were absent from a narrower training set, even if Argentine-specific events are not present.
- **Datapoint citations:**
  - [D25] Example 95 (humanitarian, train, infrastructure_and_utilities_damage): "After deadly Brazil nightclub fire, safety questions emerge." — industrial accident type represented.
  - [D27] Example 49 (humanitarian, train, infrastructure_and_utilities_damage): "Torrential rains have damaged Kenya's infrastructure, severing road links between Nairobi and Garissa…" — African flood infrastructure — broad geographic spread.
  - [D44] Example 60 (humanitarian, train, infrastructure_and_utilities_damage): "Colorado floods shut down hundreds of oil and gas wells; recovery will take time…" — oil/gas infrastructure damage relevant to Argentine Vaca Muerta industrial context.

#### Strength 4: Presence of some non-English and non-North-American content
- **Dimension(s):** IC, IF
- **Observation:** The sampled examples include Italian (Ex. 30, 44, 57, 131 in informativeness), French (Ex. 44 humanitarian), Portuguese (Ex. 113 humanitarian), Tagalog (Ex. 1, 79, 93, 128 humanitarian), and multiple Spanish tweets (Ex. 19, 83, 106 humanitarian; Ex. 37, 67, 88, 89, 106, 127 informativeness). Language tags are present, enabling filtering. The CrisisMMD 2017 events add international disaster diversity.
- **Deployment relevance:** While none of the Spanish content is Argentine or Rioplatense, its presence demonstrates the dataset is not exclusively US/UK English and that non-Latin-alphabet and Romance-language registers have been annotated. For a deployment that must handle multilingual input streams, the label schema has at least been exposed to non-English content at the margins.
- **Datapoint citations:**
  - [D21] Example 57 (humanitarian, train, caution_and_advice): "RT @frankowolf1: il comune di Mirandola cerca ing. e arch. contattare Polizia Municipale: 0535/611039, 800/197197 #terremoto" — Italian caution/advice tweet correctly labelled.
  - [D39] Example 1 (humanitarian, train, affected_individual): "@lucilledizon: 517 ilang ilang st. bayanihan vilage cainta rizal, David Bautista +63 905 826 5094. Needs rescue @MMDA @govph #rescuePH" — Tagalog rescue request correctly labelled affected_individual.
  - [D5] Example 89 (informativeness, train, informative): "Declaran tres días de luto nacional por accidente de tren en España: Testigos afirman que el tren… http://t.co/pAcRQGdjFv" — Spanish-language disaster tweet labelled informative.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Complete absence of Argentine or Rioplatense Spanish content
- **Dimension(s):** IC, IF
- **Observation:** All 271 sampled examples contain zero instances of Argentine events, Argentine institutional actors, or Rioplatense Spanish. The Spanish-language tweets in the sample are Chilean (events: `2014_chile_earthquake`, `2014_chile_earthquake_esp`), Venezuelan (`2012_venezuela_refinery-explosion`), and Spanish (`2013_spain_train-crash_en-mixed`). No lunfardo register, no Argentine agency names (SINAGIR, AFE, SENAPRED), no Buenos Aires Metropolitan Area geography, no Rioplatense voseo constructions, and no Argentine political framing appear anywhere in the sample.
- **Deployment relevance:** The deployment's core channel — Argentine Twitter/X — features Rioplatense Spanish with distinctive lexical, syntactic, and pragmatic features (voseo, lunfardo, political satire, institutional irony) that are entirely absent from the training distribution. A classifier trained on this benchmark will encounter an out-of-distribution linguistic register on every Spanish-language Argentine social media post it processes. This is the single most consequential alignment gap for the deployment.
- **Datapoint citations:**
  - [D2] Example 83 (humanitarian, sympathy_and_support): "RT @FlorrGo: #FuerzaChile ,un 2 de abril ... Que vengan los ingleses a ayudarlos ahora ... A la larga o a la corta ,todo vuelve" — Chilean Spanish, not Argentine; no Rioplatense register.
  - [D3] Example 106 (humanitarian, sympathy_and_support): "Que lindo saber que en mi ciudad bella #Iquique hay gente con un corazón enorme dispuestos a ayudar... Emocionada" — Iquique is in Chile; no Argentine content.
  - [D6] Example 37 (informativeness, informative): "IMPRESIONANTE terremoto Chile camara de seguridad farmacia - NEW VIDEO E...: http://t.co/bkUElKfFUj vía @YouTube" — Chilean earthquake, Chilean Spanish.
  - [D7] Example 127 (informativeness, informative): "RT @marieli_d: Nuevamente se incendia #Amuay http://t.co/AiWlhgy3" — Venezuelan refinery explosion; Venezuelan Spanish.

#### Concern 2: No credibility, misinformation, or source reliability dimension in the output schema
- **Dimension(s):** OO, OF
- **Observation:** Neither the humanitarian nor informativeness config contains any label, score, or metadata field relating to source credibility, institutional authority, misinformation likelihood, or signal reliability. The schema fields are: id, event, source, text, lang, lang_conf, class_label. The `source` field records dataset provenance (e.g., `crisismmd`, `crisisnlp-cf`), not tweet author credibility. No tweet-level credibility metadata is present.
- **Deployment relevance:** The primary output requirement for the Buenos Aires policy-maker cohort is a trustworthiness or reliability score. The benchmark produces only binary informativeness and multi-class humanitarian type labels. This gap is user-acknowledged as requiring downstream construction, but the data itself provides no foundation for learning source credibility signals. Notably, Example D45 (a "DEATH TOLL Now under Investigation for COVER UP!!!" tweet labelled not_informative) and D47 (a conspiracy tweet labelled informative) illustrate that the existing labels do not align with a credibility axis — credible and non-credible content appear on both sides of the informativeness divide.
- **Datapoint citations:**
  - [D45] Example 128 (informativeness, not_informative): "https://t.co/najVJNt4Ip DEATH TOLL Now under Investigation for COVER UP!!! https://t.co/VuGGPYboIv" — credibility-ambiguous sensationalist content labelled not_informative; offers no credibility signal.
  - [D47] Example 31 (informativeness, informative): "I was told I'm ignorant to think the Boston Bombing wasn't planned by the government to keep our attention away from schemes being planned." — conspiracy content labelled informative, illustrating that informativeness ≠ credibility.
  - [D10] Example 102 (humanitarian, infrastructure_and_utilities_damage): "Middle East right now:\nIS about to seize Ramadi\nAl-Qaeda seizes Yemen airport\nSaudi regime executes Indonesian women\nIran exports terrorism" — political conflict content labelled infrastructure damage; no credibility dimension.

---

#### MAJOR

#### Concern 3: Substantial annotation noise and label inconsistency observable in sample
- **Dimension(s):** OC
- **Observation:** Multiple examples in both configs exhibit annotation patterns that would be inconsistent or incorrect by any reasonable standard, suggesting the label quality the deployment would be training/evaluating against is uneven. Specific problems observed: (a) a Chilean Spanish tweet about a cinema film labelled `displaced_and_evacuations`; (b) an NGO capability description labelled `requests_or_needs`; (c) a tent/generator infrastructure description labelled `requests_or_needs`; (d) a substantive typhoon warning labelled `not_informative`; (e) a Long Island home renovations advertisement in `other_relevant_information`; (f) a political conflict tweet labelled `infrastructure_and_utilities_damage`.
- **Deployment relevance:** For a deployment where policy makers need reliable classification outputs to feed a credibility scoring pipeline, noisy ground-truth labels reduce the trustworthiness of any model trained or evaluated on this benchmark. Cross-dataset F1 degradation (14.3%, noted in the YAML) is at least partially explained by these label inconsistencies. Argentine stakeholders calibrating against this benchmark may encounter a noisy signal floor that undermines the pipeline's practical utility.
- **Datapoint citations:**
  - [D1] Example 19 (humanitarian, displaced_and_evacuations): "El trabajo de la mejor Daniela López que conozco en pantalla grande #mataraunhombe #chile #cinema…" — Chilean film discussion labelled displaced_and_evacuations; likely annotation error.
  - [D37] Example 90 (humanitarian, requests_or_needs): "Equipped with a power generator and air conditioner, the tents can also house an emergency medical center." — capability description, not a request; mislabelled.
  - [D38] Example 98 (humanitarian, requests_or_needs): "AmeriCares solicits donations of medicines, medical supplies, and other relief materials from manufacturers, and delivers them quickly and reliably to indigenous health and welfare professionals in 137 countries around the world." — NGO mission statement labelled requests_or_needs; more accurately donation_and_volunteering or response_efforts.
  - [D28] Example 34 (informativeness, not_informative): "A tropical cyclone will affect my area. Winds of greater than 100 kph up to 185 kph may be expected in at least 18 hours. #TyphoonHagupit" — specific quantitative typhoon warning labelled not_informative.
  - [D33] Example 111 (humanitarian, other_relevant_information): "Check out these award winning Long Island renovations: #longisland #suffolk https://t.co/wLnIbOENK9" — entirely unrelated home renovation content in other_relevant_information.
  - [D10] Example 102 (humanitarian, infrastructure_and_utilities_damage): "Middle East right now:\nIS about to seize Ramadi\nAl-Qaeda seizes Yemen airport…\nIran exports terrorism" — political/conflict listing labelled infrastructure damage.

#### Concern 4: Informativeness label boundaries are culturally unstable for Argentine social media
- **Dimension(s):** OC, IC
- **Observation:** Several examples labelled `informative` in the sample carry minimal disaster-relevant content by any standard, while content with substantive disaster information is sometimes labelled `not_informative`. The observed boundary appears to conflate "crisis-adjacent" with "informative," accepting sympathetic sentiment tweets, celebrity references, and personal reactions as informative. Argentine Twitter/X discourse is characterised by political satire and institutional irony — content that superficially resembles the `not_informative` patterns in the benchmark but may carry genuine crisis signals.
- **Deployment relevance:** If the Argentine deployment system inherits these ambiguous label boundaries, it risks classifying Argentine political commentary on government crisis response as not_informative (missing real signals) or misclassifying satirical content as informative. This is particularly acute given the noted Argentine norm of political framing in crisis coverage and the dissolution of Télam, which has dispersed official crisis communication signals across a more fragmented landscape.
- **Datapoint citations:**
  - [D11] Example 1 (informativeness, informative): "when the ambushes of this century, hold closes even when life puts you in discomfiture, hold closes even that one of condescends your family, so God will facilitate you shortcoming" — philosophical/religious text with no disaster content, labelled informative.
  - [D12] Example 3 (informativeness, informative): "Sweater weather indeed 🌂 #RubyPH" — weather comment during typhoon labelled informative; near-zero disaster signal.
  - [D13] Example 7 (informativeness, informative): "i hope everyone is safe" — generic sentiment, labelled informative.
  - [D14] Example 83 (informativeness, informative): "This hurricane thingy is looking pretty scary! I'm kinda excited by insane weather..." — personal reaction, labelled informative.
  - [D29] Example 6 (informativeness, not_informative): "#sobering Helicopter crash into pub in #glasgow! http://t.co/0uYSOocUvu" — breaking news tweet labelled not_informative despite containing disaster event reference.
  - [D30] Example 52 (informativeness, not_informative): "Bangladesh:palazzo non era per fabbriche: Il progetto del Rana Plaza prevedeva solo 6 piani non 9 o 10 http://t.co/VG9qCqa3xX" — Italian investigative report on building code violation labelled not_informative.

#### Concern 5: North American and North Atlantic event dominance distorts register and cultural framing
- **Dimension(s):** IC
- **Observation:** The personal_update and not_humanitarian categories are dominated by North American vernacular English: American sports references, US political discourse, and North American cultural referents. Personal_update examples include Sandy-era tweets referencing Joplin tornado and North American colloquial register. The social chatter that the benchmark trains models to recognise as "noise" is specifically North American social noise, not Argentine social noise.
- **Deployment relevance:** Argentine social media "noise" differs structurally from US social media noise: it includes political satire of the Milei government's handling of floods, lunfardo-inflected commentary, references to local institutional actors (AMBA prefectura, Buenos Aires province civil defense), and WhatsApp-style forwarded messages. A classifier trained to recognise US sports commentary as not_informative may misclassify Argentine political satire about disaster response — which could carry real signals about institutional credibility — in either direction.
- **Datapoint citations:**
  - [D17] Example 26 (humanitarian, personal_update): "Tornado watch until 3am. Of course we just got our new garage door today. *sigh*" — North American personal complaint about Joplin tornado watch; this is the register the classifier learns as "personal_update."
  - [D18] Example 11 (humanitarian, personal_update): "RT @tarnsnastylad: They need to name hurricanes better!.. superstorm Sandy? Seriously??.. Sounds like a FUCKING gay wrestler!" — North American vernacular during Sandy.
  - [D46] Example 24 (humanitarian, not_humanitarian): "RT @eclecticbrotha: @AlGiordano Damn, I forgot how much of a shitshow Bernie's Puerto Rico operation was." — US political commentary during Hurricane Maria labelled not_humanitarian; analogue Argentine political commentary on AFE crisis response would face the same classification challenge.

#### Concern 6: Spanish-language examples present carry Chilean/Venezuelan register, not Rioplatense, and show annotation inconsistency
- **Dimension(s):** IC, OC
- **Observation:** The Spanish-language examples in the sample are all from Chilean or Venezuelan events and use standard Chilean/Venezuelan register. One Chilean Spanish tweet (Ex. 88, informativeness: "#FuerzaChile jaja y piden ayuda jaja que los ayuden los ingleses manga de traidores") reflects Chilean political sentiment about foreign aid and is labelled not_informative. Another substantive Spanish tweet with disaster hashtags (Ex. 106, informativeness: "Ojo con el exceso de ayuda por los efectos del #TerremotoenChile porque puede producir mucho más obstáculos de lo que se cree.") is also labelled not_informative despite containing a crisis-relevant public warning about aid logistics. This suggests the annotation schema may systematically under-recognise disaster-relevance in Spanish-language content.
- **Deployment relevance:** If Spanish-language disaster warnings are being labelled not_informative in the benchmark, any model trained on this data will be systematically biased against recognising Spanish-language disaster signals — directly undermining the Argentine deployment's core function of triage across Spanish-language social media content.
- **Datapoint citations:**
  - [D9] Example 106 (informativeness, not_informative): "Ojo con el exceso de ayuda por los efectos del #TerremotoenChile porque puede producir mucho más obstáculos de lo que se cree." — crisis-relevant Spanish warning about aid logistics labelled not_informative.
  - [D4] Example 88 (informativeness, not_informative): "#FuerzaChile jaja y piden ayuda jaja que los ayuden los ingleses manga de traidores" — Chilean political sentiment during earthquake, not_informative.
  - [D8] Example 117 (humanitarian, not_humanitarian): "RT @meteomostoles: El tifón #BOPHA,de cat.4 y 947hPa en su centro,va camino de Filipinas.Lleva vientos sostenidos entre 2010 y 249km/h h ..." — Spanish-language meteorological warning about a typhoon labelled not_humanitarian, despite containing specific wind-speed and track data.

---

#### MINOR

#### Concern 7: `other_relevant_information` class is a heterogeneous catch-all with low semantic coherence
- **Dimension(s):** OO, OC
- **Observation:** The `other_relevant_information` class in the humanitarian config functions as a residual bucket containing content ranging from clear factual updates ("PAGASA says typhoon has further weakened") to personal experience tweets ("being in a hurricane inside a house with no lights") to a benefit concert announcement to a completely unrelated home renovations advertisement. This class's semantic incoherence limits its usefulness as a training or evaluation signal.
- **Deployment relevance:** For a deployment trying to classify Argentine crisis communication quality, a 13% catch-all class (166/500 buffer examples are other_relevant_information) that conflates substantive updates with noise will produce unreliable outputs for borderline content — precisely the category most relevant to a credibility scoring task where the interesting cases are not clearly informative or clearly noise.
- **Datapoint citations:**
  - [D32] Example 52 (humanitarian, other_relevant_information): "being in a hurricane inside a house with no lights ..." — personal experience, arguably not crisis-informative.
  - [D31] Example 25 (humanitarian, other_relevant_information): "Update on the fertilizer explosion in West, Texas. Estimated 50 to 60 dead, hundreds injured, half of town flattened." — this appears to be injured_or_dead_people or affected_individual rather than other_relevant_information.
  - [D33] Example 111 (humanitarian, other_relevant_information): "Check out these award winning Long Island renovations: #longisland #suffolk https://t.co/wLnIbOENK9" — entirely unrelated content; should be not_humanitarian.

#### Concern 8: Temporal gap — all events 2010–2017; Argentine institutional landscape has changed materially since 2017
- **Dimension(s):** IC
- **Observation:** All events in the sample span 2010–2017 (oldest: 2011 Joplin tornado; newest: 2017 Hurricane Maria/Irma/Harvey). The Argentine institutional context relevant to the deployment has changed substantially since 2017: Télam was dissolved in July 2024, AFE was created in 2025, and the current political environment (Milei administration) has altered the credibility landscape for official disaster communications.
- **Deployment relevance:** Social media conventions, platform norms (Twitter/X after Musk acquisition), and Argentine institutional credibility signals have all shifted since 2017. A classifier trained on 2010–2017 tweet patterns may misclassify post-2022 content that uses different hashtagging conventions, link formats, and institutional citation patterns.
- **Datapoint citations:**
  - [D17] Example 26 (humanitarian, personal_update): "Tornado watch until 3am." (2011 Joplin) — oldest event; Twitter conventions of 2011 differ from 2024.
  - [D46] Example 24 (humanitarian, not_humanitarian): "RT @eclecticbrotha: @AlGiordano Damn, I forgot how much of a shitshow Bernie's Puerto Rico operation was. https://t.co/DgZMF2qnNl" — 2017 Hurricane Maria, pre-Musk Twitter, pre-Télam dissolution.

#### Concern 9: `lang_conf` field is missing (NA) for many CrisisMMD and AIDR examples, complicating language-stratified filtering
- **Dimension(s):** IF
- **Observation:** A large number of examples from `crisismmd` and `aidr_system` sources have `lang_conf: NA` rather than a numeric confidence score. This means the language detection confidence is unavailable for these examples, making it impossible to filter by language detection reliability. Given that the deployment needs to handle Spanish-language content differently from English content, the absence of confidence scores for a significant subset of examples weakens the language-stratification capability of the dataset.
- **Deployment relevance:** For the Argentine deployment, reliable language identification is prerequisite to routing content to appropriate classifiers (English vs. Spanish models). The NA confidence values in the CrisisMMD and AIDR subsets — which include 2017 events most temporally proximate to the deployment window — reduce confidence in automated language-based routing decisions built on this benchmark's language metadata.
- **Datapoint citations:**
  - [D5] Example 5 (humanitarian, donation_and_volunteering): "#Fox914 encourages you to unite and give to those who are affected... #FloodSL #srilanka #colombo #kandy #lka https://t.co/iLgsSCJ06b" — `lang_conf: NA` from crisismmd source.
  - [D42] Example 14 (humanitarian, response_efforts): "#Tacloban has 49 evacuation centers now sheltering over 30,000 people + @care is helping respond to #typhoonhagupit http://t.co/ePE9MsdpTh" — `lang_conf: NA` from crisisnlp-volunteers source.
  - [D10] Example 102 (humanitarian, infrastructure_and_utilities_damage): "Middle East right now:\nIS about to seize Ramadi…" — `lang_conf: NA` from aidr_system source.

---

### Content Coverage Summary

The 271 sampled examples reveal a dataset that is predominantly English-language (~88% of sampled examples), drawn from North American and global events spanning 2010–2017, with a strong concentration in US hurricanes (Sandy, Harvey, Irma, Maria), Philippines typhoons, Nepal earthquake, Pakistan floods, and Joplin tornado. The humanitarian config represents 15 classes with notable imbalance: `not_humanitarian` and `other_relevant_information` together account for the majority of buffer-sampled examples (366/500), consistent with the documented 37.4% not_humanitarian rate. Non-English content is present but sparse: Italian (3–4 examples), French (1), Portuguese (1), Tagalog (4–5), and Spanish (6–8 examples), all from non-Argentine events. The Spanish content is exclusively Chilean and Venezuelan.

Register is predominantly short-form social media (Twitter), ranging from professional news retweets to personal social chatter, with some longer structured text from the DRD (Figure Eight) dataset representing more formal humanitarian situation reports. The DRD examples are notably different in register from tweets — they read as structured field reports or aid request forms — introducing within-benchmark register heterogeneity. The `other_relevant_information` class functions as a heterogeneous residual category. Label quality is uneven, with observable annotation errors in both configs that reduce confidence in benchmark scores as indicators of real-world classification capability.

No Argentine, Rioplatense Spanish, Buenos Aires-specific, or Pampa/Patagonia/Río de la Plata content appears in the sample. The hazard types represented (North Atlantic hurricanes, South Asian floods, Philippines typhoons, North American tornadoes) do not include pampero windstorms, sudestada events, ENSO-driven droughts, or urban flash floods in dense Latin American metropolitan settings.

---

### Limitations

1. **Sample size per class:** The stratified buffer over 15 humanitarian classes produces small per-class samples (2–25 examples for rare classes like `displaced_and_evacuations`, `missing_and_found_people`, `personal_update`). Annotation quality and label consistency observations for these rare classes are based on 2–4 examples and should be treated as directional, not definitive.

2. **Train split only:** All examples are from the train split. Test and dev split distributions, label quality, and language composition are not directly inspected and may differ.

3. **No access to raw tweet metadata:** The dataset provides text, event, source, lang, and class_label, but not tweet author metadata (account type, follower count, verified status), timestamps, or geolocation — all relevant to the deployment's credibility scoring aspiration. The absence of these fields from the schema is a structural limitation of the dataset, not a sampling artefact.

4. **Language detection accuracy unverified:** The `lang` field relies on Google Cloud Language Detection API. Misdetections (e.g., short tweets, code-switched content) cannot be verified from the text alone for non-Latin-script or mixed-language examples.

5. **CrisisMMD multimodal data:** CrisisMMD was originally a multimodal dataset (tweets + images). The HF dataset appears to contain only the text component. Image-based disaster signals from CrisisMMD are not inspectable or evaluated here.

6. **Informativeness label semantics vary by source dataset:** The informativeness label maps from different original schemas (relevant/not-relevant in DSM; informative/not-informative in CrisisLex). The observed label inconsistencies in the informativeness config may partly reflect this multi-source mapping rather than annotation error within any single source.

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
  "benchmark": "crisisbench",
  "region": "Argentina — Buenos Aires Policy Maker Cohort (Disaster Reporting Reliability)",
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
