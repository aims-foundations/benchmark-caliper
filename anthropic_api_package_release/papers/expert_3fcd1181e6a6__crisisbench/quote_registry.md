---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | data_sources | "We consolidate eight human-annotated datasets and provide 166.1k and 141.5k tweets for informativeness and humanitarian classification tasks, respectively." |
| Q2 | 1 | evaluation_metrics | "We provide benchmarks for both binary and multiclass classification tasks using several deep learning architectures including, CNN, fastText, and transformers." |
| Q3 | 1 | task_taxonomy | "Typical classification tasks in the community include (i) informativeness (i.e., informative vs. not-informative messages), (ii) humanitarian information types (e.g., affected individual reports, infrastructure damage reports), and (iii) event types (e.g., flood, earthquake, fire)." |
| Q4 | 1 | stated_limitations | "First, few efforts have been invested to develop standard datasets (specifically, train/dev/test splits) and benchmarks for the community to compare their results, models, and techniques." |
| Q5 | 1 | stated_limitations | "Secondly, most of the published datasets are noisy, e.g., CrisisLex (Olteanu et al. 2014) contains duplicate and near-duplicate content, which produces misleading classification performance." |
| Q6 | 1 | stated_limitations | "Moreover, some datasets (e.g., CrisisLex) consist of tweets from several languages without any explicit language tag, to separate the data of a particular language of interest." |
| Q7 | 1 | data_sources | "We consolidate eight publicly available datasets (see Section 3)." |
| Q8 | 1 | data_format | "One of the challenges is the inconsistent class labels across various data sources." |
| Q9 | 1 | authors_affiliations | "Firoj Alam, Hassan Sajjad, Muhammad Imran, Ferda Ofli, Qatar Computing Research Institute, HBKU, Qatar" |
| Q10 | 2 | data_sources | "We consolidate eight publicly available disaster-related datasets by manually mapping semantically similar class labels, which leads to a larger dataset." |
| Q11 | 2 | data_format | "We carefully cleaned various forms of duplicates, and assigned a language tag to each tweet." |
| Q12 | 2 | task_taxonomy | "We provide benchmark results on English tweets set using state-of-the-art machine learning algorithms such as Convolutional Neural Networks (CNN), fastText (Joulin et al. 2017) and pre-trained transformer models (Devlin et al. 2019) for two classifications tasks, i.e., Informativeness (binary) and Humanitarian type (multi-class) classification." |
| Q13 | 2 | data_format | "For the research community, we aim to release the dataset in multiple forms as, (i) a consolidated class label mapped version, (ii) exact- and near-duplicate filtered version obtained from previous versions, (iii) a subset of the filtered data used for the classification experiments in this study." |
| Q14 | 2 | stated_limitations | "A major limitation of the work by Alam, Muhammad, and Ferda (2019) is that the issue of duplicate and near-duplicate content have not been addressed when combining the different datasets." |
| Q15 | 2 | stated_limitations | "Kersten et al. (2019) focused only on informativeness classification and combined five different datasets. This study has also not focused on exact- and near-duplicate content, which exist in different datasets." |
| Q16 | 2 | stated_limitations | "A fair comparison of the classification experiment is also difficult with previous studies as their train/dev/test splits are not public, except the dataset by Wiegmann et al. (2020)." |
| Q17 | 2 | data_sources | "We address such limitations in this study, i.e., we consolidate the datasets, eliminate duplicates, and release standard dataset splits with benchmark results." |
| Q18 | 2 | label_categories | "In this study, we use the class labels that are important for humanitarian aid for disaster response tasks, which are common across the publicly available resources." |
| Q19 | 2 | evaluation_metrics | "The study of (Nguyen et al. 2017) and (Neppalli, Caragea, and Caragea 2018) performed comparative experiments between different classical and deep learning algorithms including Support Vector Machines, Logistic Regression, Random Forests, Recurrent Neural Networks, and Convolutional Neural Networks (CNN)." |
| Q20 | 2 | evaluation_metrics | "Their experimental results suggest that CNN outperforms other algorithms." |
| Q21 | 2 | evaluation_metrics | "Though in another study, (Burel and Alani 2018) reports that SVM and CNN can provide very competitive results in some cases." |
| Q22 | 2 | stated_limitations | "We only focused on two tasks for this study and we aim to address event types task in a future study." |
| Q23 | 3 | task_taxonomy | "We consolidate eight datasets that were labeled for different disaster response classification tasks and whose labels can be mapped consistently for two tasks: informativeness and humanitarian information type classification." |
| Q24 | 3 | stated_limitations | "In doing so, we deal with two major challenges: (i) discrepancies in the class labels used across different datasets, and (ii) exact- and near-duplicate content that exists within as well as across different datasets." |
| Q25 | 3 | data_sources | "CrisisLex is one of the largest publicly-available datasets, which consists of two subsets, i.e., CrisisLexT26 and CrisisLexT6 (Olteanu et al. 2014). CrisisLexT26 comprises data from 26 different crisis events that took place in 2012 and 2013 with annotations for informative vs. not-informative as well as humanitarian categories (six classes) classification tasks among others. CrisisLexT6, on the other hand, contains data from six crisis events that occurred between October 2012 and July 2013 with annotations for related vs. not-related binary classification task." |
| Q26 | 3 | data_sources | "CrisisNLP is another large-scale dataset collected during 19 different disaster events that happened between 2013 and 2015, and annotated according to different schemes including classes from humanitarian disaster response and some classes related to health emergencies (Imran, Mitra, and Castillo 2016)." |
| Q27 | 3 | data_sources | "SWDM2013 dataset consists of data from two events: (i) the Joplin collection contains tweets from the tornado that struck Joplin, Missouri on May 22, 2011; (ii) The Sandy collection contains tweets collected from Hurricane Sandy that hit Northeastern US on Oct 29, 2012 (Imran et al. 2013a)." |
| Q28 | 3 | data_sources | "ISCRAM2013 dataset consists of tweets from two different events occurred in 2011 (Joplin 2011) and 2012 (Sandy 2012). Note that this set of tweets are different than SWDM2013 set even though they are collected from same events (Imran et al. 2013b)." |
| Q29 | 3 | data_sources | "Disaster Response Data (DRD) consists of tweets collected during various crisis events that took place in 2010 and 2012. This dataset is annotated using 36 classes that include informativeness as well as humanitarian categories." |
| Q30 | 3 | data_sources | "Disasters on Social Media (DSM) dataset comprises 10K tweets collected and annotated with labels related vs. not-related to the disasters." |
| Q31 | 3 | data_sources | "CrisisMMD is a multimodal dataset consisting of tweets and associated images collected during seven disaster events that happened in 2017 (Alam et al. 2018). The annotations for this dataset is targeted for three classification tasks: (i) informative vs. not-informative, (ii) humanitarian categories (eight classes) and (iii) damage severity assessment." |
| Q32 | 3 | data_sources | "AIDR dataset is obtained from the AIDR system (Imran et al. 2014) that has been annotated by domain experts for different events and made available upon requests. We only retained labeled data that are relevant to this study." |
| Q33 | 3 | data_format | "The datasets come with different class labels. We create a set of common class labels by manually mapping semantically similar labels into one cluster. For example, the label "building damaged," originally used in the AIDR system, is mapped to "infrastructure and utilities damage" in our final dataset." |
| Q34 | 3 | label_categories | "Some of the class labels in these datasets are not annotated for humanitarian aid purposes, therefore, we have not included them in the consolidated dataset. For example, we do not select tweets labeled as "animal management" or "not labeled" that appear in CrisisNLP and CrisisLex26." |
| Q35 | 3 | stated_limitations | "This causes a drop in the number of tweets for both informativeness and humanitarian tasks as can be seen in Table 1 (Mapping column). The large drop in the CrisisLex dataset for the informativeness task is due to the 3,103 unlabeled tweets (i.e., labeled as "not labeled")." |
| Q36 | 3 | stated_limitations | "The other significant drop for the informativeness task is in the DRD dataset. This is because many tweets were annotated with multiple labels," |
| Q37 | 4 | data_format | "To develop a machine learning model, it is important to design non-overlapping train/dev/test splits. A common practice is to randomly split the dataset into train/dev/test sets. This approach does not work with social media data as it generally contains duplicates and near duplicates. Such duplicate content, if present in both train and test sets, often leads to overestimated test results during classification." |
| Q38 | 4 | data_format | "We first tokenize the text before applying any filtering. For tokenization, we used a modified version of the Tweet NLP tokenizer (O'Connor, Krieger, and Ahn 2010). Our modification includes lowercasing the text and removing URL, punctuation, and user id mentioned in the text. We then filter tweets having only one token." |
| Q39 | 4 | data_format | "We then use a similarity-based approach to remove the near-duplicates. To do this, we first convert the tweets into vectors using bag-of-ngram approach as a vector representation. We use uni- and bi-grams with their frequency-based representations. We then use cosine similarity to compute a similarity score between two tweets and flag them as duplicate if their similarity score is greater than the threshold value of 0.75." |
| Q40 | 4 | data_format | "To determine a plausible threshold value, we manually checked the tweets in different threshold bins (i.e., 0.70 to 1.0 with 0.05 interval) as shown in Figure 1, which we selected from consolidated informativeness dataset. By investigating the distribution and manual checking, we concluded that a threshold value of 0.75 is a reasonable choice." |
| Q41 | 4 | stated_limitations | "As indicated in Table 1, there is a drop after filtering, e.g., ∼25% for informativeness and ∼20% for humanitarian tasks. It is important to note that failing to eradicate duplicates from the consolidated dataset would potentially lead to" |
| Q42 | 5 | data_format | "Some of the existing datasets contain tweets in various languages (i.e., Spanish and Italian) without explicit assignment of a language tag." |
| Q43 | 5 | data_format | "In addition, many tweets have codeswitched (i.e., multilingual) content." |
| Q44 | 5 | data_format | "We decided to provide a language tag for each tweet if it is not available with the respective dataset." |
| Q45 | 5 | data_format | "We used the language detection API of Google Cloud Services for this purpose." |
| Q46 | 5 | data_sources | "Among different languages of informativeness tweets, English tweets appear to be highest in the distribution compared to any other language, which is 94.46% of 156,899." |
| Q47 | 5 | data_sources | "Note that most of the non-English tweets appear in the CrisisLex dataset." |
| Q48 | 5 | label_categories | "Distribution of class labels is an important factor for developing the classification model." |
| Q49 | 5 | stated_limitations | "It is clear that there is an imbalance in class distributions in different datasets and some class labels are not present." |
| Q50 | 5 | stated_limitations | "For example, the distribution of "not informative" class is very low in SWDM2013 and ISCRAM2013 datasets." |
| Q51 | 5 | stated_limitations | "For the humanitarian task, some class labels are not present in different datasets." |
| Q52 | 5 | stated_limitations | "Only 17 tweets with the label "terrrorism related" are present in CrisisNLP." |
| Q53 | 5 | stated_limitations | "Similarly, the class "disease related" only appears in CrisisNLP." |
| Q54 | 5 | stated_limitations | "The scarcity of the class labels poses a great challenge to design the classification model using individual datasets." |
| Q55 | 5 | stated_limitations | "Even after combining the datasets, the imbalance in class distribution seems to persist (last column in Table 4)." |
| Q56 | 5 | stated_limitations | "For example, the distribution of "not humanitarian" is relatively higher (37.40%) than other class labels." |
| Q57 | 5 | label_categories | "In Table 4, we highlighted some class labels, which we dropped in the rest of the classification experiments conducted in this study." |
| Q58 | 5 | label_categories | "However, tweets with those class labels will be available in the released datasets." |
| Q59 | 6 | data_format | "Although our consolidated dataset contains multilingual tweets, we only use tweets in English language in our experiments." |
| Q60 | 6 | data_format | "We split data into train, dev, and test sets with a proportion of 70%, 10%, and 20%, respectively, also reported in Table 5." |
| Q61 | 6 | task_taxonomy | "As mentioned earlier we have not selected the tweets with highlighted class labels in Table 4 for the classification experiments." |
| Q62 | 6 | evaluation_metrics | "For the experiments, we use CNN, fastText, and pre-trained transformer models." |
| Q63 | 6 | evaluation_metrics | "The current state-of-the-art disaster classification model is based on the CNN architecture." |
| Q64 | 6 | evaluation_metrics | "For the fastText (Joulin et al. 2017), we used pre-trained embeddings trained on Common Crawl, which is released by fastText for English." |
| Q65 | 6 | stated_limitations | "Though the pre-trained models are mainly trained on non-Twitter text, we hypothesize that their rich contextualized embeddings would be beneficial for the disaster domain." |
| Q66 | 6 | evaluation_metrics | "In this work, we choose the pre-trained models BERT (Devlin et al. 2019), DistilBERT (Sanh et al. 2019), and RoBERTa (Liu et al. 2019) for the classification tasks." |
| Q67 | 6 | evaluation_metrics | "We train the CNN models using the Adam optimizer (Kingma and Ba 2014)." |
| Q68 | 6 | evaluation_metrics | "The batch size is 128 and maximum number of epochs is set to 1000." |
| Q69 | 6 | evaluation_metrics | "We use a filter size of 300 with both window size and pooling length of 2, 3, and 4, and a dropout rate 0.02." |
| Q70 | 6 | evaluation_metrics | "We set early stopping criterion based on the accuracy of the development set with a patience of 200." |
| Q71 | 6 | evaluation_metrics | "For the experiments with fastText, we used default parameters except: (i) the dimension is set to 300, (ii) minimal number of word occurrences is set to 3, and (iii) number of epochs is 50." |
| Q72 | 6 | stated_limitations | "Due to the instability of the pre-trained models as reported in (Devlin et al. 2019), we perform ten re-runs for each experiment using different seeds, and we select the model that performs best on the dev set." |
| Q73 | 6 | evaluation_metrics | "For transformer-based models, we used a learning rate of 2e − 5, and a batch size of 8." |
| Q74 | 6 | data_format | "Prior to the classification experiment, we preprocess tweets to remove symbols, emoticons, invisi-" |
| Q75 | 7 | evaluation_metrics | "To measure the performance of each classifier, we use weighted average precision (P), recall (R), and F1-measure (F1). The rationale behind choosing the weighted metric is that it takes into account the class imbalance problem." |
| Q76 | 7 | task_taxonomy | "The motivation of these experiments is to investigate whether model trained with consolidated dataset generalizes well across different sets. For the individual dataset classification experiments, we selected CrisisLex and CrisisNLP as they are relatively larger in size and have a reasonable number of class labels, i.e., six and eleven class labels, respectively." |
| Q77 | 7 | data_format | "Note that these are subsets of the consolidated dataset reported in Table 5. We selected them from train, dev and test splits of the consolidated dataset to be consistent across different classification experiments." |
| Q78 | 7 | evaluation_metrics | "To understand the effectiveness of the smaller datasets, we run experiments by training the model using smaller datasets and evaluating using the consolidated test set." |
| Q79 | 7 | stated_limitations | "The availability of annotated data for a disaster event is usually scarce. One of the advantages of our compiled data is to have identical classes across several disaster events. This enables us to combine the annotated data from all previous disasters for the classification." |
| Q80 | 7 | stated_limitations | "Though this increases the size of the training data substantially, the classifier may result in sub-optimal performance due to the inclusion of heterogeneous data (i.e., a variety of disaster types and occurs in a different part of the world)." |
| Q81 | 7 | data_format | "We append a disaster event type as a token to each annotated tweet ti. More concretely, say tweet ti consists of k words {w1, w2, ..., wk}. We append a disaster event type tag di to each tweet so that ti would become {di, w1, w2, ..., wk}. We repeat this step for all disaster event types present in our dataset." |
| Q82 | 7 | stated_limitations | "The event-aware training requires the knowledge of the disaster event type at the time of the test. If we do not provide a disaster event type, the classification performance will be suboptimal due to a mismatch between train and test." |
| Q83 | 7 | data_format | "Instead of appending the disaster event type to all tweets of a disaster, we randomly append disaster event type UNK to 5% of the tweets of every disaster. Note that UNK is now distributed across all disaster event types and is a good representation of an unknown event." |
| Q84 | 8 | evaluation_metrics | "The model trained using the consolidated dataset achieves 0.866 (F1) for informativeness and 0.829 for humanitarian, which is better than the models trained using individual datasets." |
| Q85 | 8 | evaluation_metrics | "Between CrisisLex and CrisisNLP, the performance is higher on CrisisLex dataset for both informativeness and humanitarian tasks (1st vs. 4th row in Table 6 for the informativeness, and 10th vs. 13th row for the humanitarian task in the same table.)." |
| Q86 | 8 | data_sources | "This might be due to the CrisisLex dataset being larger than the CrisisNLP dataset." |
| Q87 | 8 | evaluation_metrics | "The cross dataset (i.e., train on CrisisLex and evaluate on CrisisNLP) results shows that there is a drop in performance. For example, there is 14.3% difference in F1 on CrisisNLP data using the CrisisLex model for the informativeness task." |
| Q88 | 8 | label_categories | "In the humanitarian task, for different datasets in Table 6, we have different number of class labels. We report the results of those classes only for which the model is able to classify." |
| Q89 | 8 | task_taxonomy | "Note that humanitarian task is a multi-class classification problem, which makes it a much more difficult task than the binary informativeness classification." |
| Q90 | 8 | evaluation_metrics | "The transformer based models achieve higher performance compared to the CNN and fastText. We used three transformer based models, which varies in the parameter sizes. However, in terms of performance, they are quite similar." |
| Q91 | 8 | evaluation_metrics | "BERT performs better than or on par with CNN across all classes. More importantly, BERT performs substantially better than CNN in the case of minority classes as highlighted in the table." |
| Q92 | 8 | evaluation_metrics | "The event-aware training improves the classification performance by 1.3 points (F1) using CNN for the humanitarian task compared to the results without using event information (see Table 6). However, no improvement has been observed for the informativeness task." |
| Q93 | 8 | task_taxonomy | "The training using event information enables the system to use data of all disasters while preserving the disaster-specific distribution." |
| Q94 | 9 | stated_limitations | "Social media data is noisy and it often poses a challenge for labeling and training classifiers." |
| Q95 | 9 | data_format | "Our analysis on publicly available datasets reveals that one should follow a number of steps before preparing and labeling any social media dataset, not just the dataset for crisis computing. Such steps include (i) tokenization to help in the subsequent phase, (ii) remove exact- and near-duplicates, (iii) check for existing data where the same tweet might be annotated for the same task, and then (iv) labeling." |
| Q96 | 9 | evaluation_metrics | "For designing the classifier, we postulate checking the overlap between training and test splits to avoid any misleading performance." |
| Q97 | 9 | data_format | "It is important to emphasize the fact that the results reported in this study are reliable as they are obtained on a dataset that has been cleaned from duplicate content, which might have led to misleading performance results otherwise." |
| Q98 | 9 | data_sources | "Our initial consolidated datasets (i.e., Table 3 and 4) contains multilingual content with more class labels and different types of content (e.g., disease-related), therefore, an interesting future research could be to try different pre-trained multilingual models to classify tweets in different languages." |
| Q99 | 9 | evaluation_metrics | "We observe that performance dropped significantly for the humanitarian task compared to English-only dataset. For example, ∼8% drop using BERT model." |
| Q100 | 9 | data_sources | "The resulting dataset covers a time-span starting from 2010 to 2017, which can be used to study temporal aspects in crisis scenarios." |
| Q101 | 9 | data_format | "We tried to bridge this gap by consolidating existing datasets, filtering exact- and near-duplicates, and providing benchmarks based on state-of-the-art CNN, FastText, and transformer-based models." |
| Q102 | 9 | data_sources | "The developed consolidated labeled dataset is curated from different publicly available sources." |
| Q103 | 10 | data_sources | "We release the dataset by maintaining the license of existing resources." |
| Q104 | 11 | data_sources | "In Table 11, we report the events associated with the respective datasets such as ISCRAM2013, SWDM2013 CrisisLex and CrisisNLP." |
| Q105 | 11 | data_sources | "The time-period is from 2011 to 2015, which is a good representative of temporal aspects." |
| Q106 | 11 | label_categories | "In Table 12, we report class label mapping for ISCRAM2013, SWDM2013, CrisisLex and CrisisNLP datasets." |
| Q107 | 11 | label_categories | "Note that all humanitarian class labels also mapped to informative, and not humanitarian labels mapped to not-informative in the data preparation step." |
| Q108 | 11 | label_categories | "In Table 13, we report the class label mapping for informativeness and humanitarian tasks for DRD dataset." |
| Q109 | 11 | label_categories | "The DSM dataset only contains tweets labeled as relevant vs not-relevant, which we mapped for informativeness task as shown in Table 14." |
| Q110 | 11 | label_categories | "The CrisisMMD dataset has been annotated for informativeness and humanitarian task, therefore, very minor label mapping was needed as shown in Table in 15." |
| Q111 | 11 | annotation_process | "The AIDR data has been labeled by domain experts using AIDR system and has been labeled during different events." |
| Q112 | 11 | data_format | "We have chosen a value of > 0.75 to filter duplicate tweets." |
| Q113 | 11 | evaluation_metrics | "In this section, we report parameters for CNN and BERT model." |
| Q114 | 11 | evaluation_metrics | "All experimental scripts will be publicly Hyper-parameters include:" |
| Q115 | 11 | evaluation_metrics | "Batch size: 8" |
| Q116 | 11 | evaluation_metrics | "Number of epochs: 10" |
| Q117 | 11 | evaluation_metrics | "Max seq length: 128" |
| Q118 | 11 | evaluation_metrics | "Learning rate (Adam): 2e-5" |
| Q119 | 11 | evaluation_metrics | "BERT (bert-base-uncased): L=12, H=768, A=12, total parameters = 110M; where L is number of layers (i.e., Transformer blocks), H is the hidden size, and A is the number of self-attention heads." |
| Q120 | 11 | evaluation_metrics | "DistilBERT (distilbert-base-uncased): it is a distilled version of the BERT model consists of 6-layer, 768-hidden, 12-heads, 66M parameters." |
| Q121 | 11 | evaluation_metrics | "RoBERTa (roberta-large): it is using the BERT-large architecture consists of 24-layer, 1024-hidden, 16-heads, 355M parameters." |
| Q122 | 11 | evaluation_metrics | "In Table 18 and 19, we provide detail results for different datasets (English Tweets) with different models." |
| Q123 | 13 | label_categories | "Table 12: Class label mapping and grouping for CrisisLex, CrisisNLP, ISCRAM2013, and SWDM2013 datasets. The symbol (✗) indicates we do not map the tweets with that label for this study." |
| Q124 | 14 | label_categories | "The symbol (✗) indicates we do not map the tweets with that label for this study." |
| Q125 | 15 | label_categories | "Table 16: Class label mapping for AIDR system." |
| Q126 | 16 | data_format | "Sim. refers to similarity value. Dup. refers to whether we consider them as duplicate and filtered." |
| Q127 | 16 | data_format | "The symbol (✗) indicates a duplicate, which we dropped and the symbol (✓) indicates a not duplicate, which we have included in our dataset." |

### Category Index
- **task_taxonomy**: Q3, Q12, Q23, Q61, Q76, Q89, Q93
- **data_sources**: Q1, Q7, Q10, Q17, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q46, Q47, Q86, Q98, Q100, Q102, Q103, Q104, Q105
- **data_format**: Q8, Q11, Q13, Q33, Q37, Q38, Q39, Q40, Q42, Q43, Q44, Q45, Q59, Q60, Q74, Q77, Q81, Q83, Q95, Q97, Q101, Q112, Q126, Q127
- **label_categories**: Q18, Q34, Q48, Q57, Q58, Q88, Q106, Q107, Q108, Q109, Q110, Q123, Q124, Q125
- **annotation_process**: Q111
- **evaluation_metrics**: Q2, Q19, Q20, Q21, Q62, Q63, Q64, Q66, Q67, Q68, Q69, Q70, Q71, Q73, Q75, Q78, Q84, Q85, Q87, Q90, Q91, Q92, Q96, Q99, Q113, Q114, Q115, Q116, Q117, Q118, Q119, Q120, Q121, Q122
- **stated_limitations**: Q4, Q5, Q6, Q14, Q15, Q16, Q22, Q24, Q35, Q36, Q41, Q49, Q50, Q51, Q52, Q53, Q54, Q55, Q56, Q65, Q72, Q79, Q80, Q82, Q94
- **authors_affiliations**: Q9
