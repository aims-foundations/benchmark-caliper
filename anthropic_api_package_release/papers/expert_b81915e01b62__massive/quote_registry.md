---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | task_taxonomy | "MASSIVE contains 1M realistic, parallel, labeled virtual assistant utterances spanning 51 languages, 18 domains, 60 intents, and 55 slots." |
| Q2 | 1 | data_sources | "MASSIVE was created by tasking professional translators to localize the English-only SLURP dataset into 50 typologically diverse languages from 29 genera." |
| Q3 | 1 | data_format | "With the English seed data included, there are 587k train utterances, 104k dev utterances, 152k test utterances, and 153k utterances currently held out for the MMNLU-22 competition, which will be released after the competition." |
| Q4 | 1 | data_sources | "MASSIVE was created by localizing the SLURP NLU dataset (created only in English) in a parallel manner." |
| Q5 | 1 | evaluation_metrics | "We also present modeling results on XLM-R and mT5, including exact match accuracy, intent classification accuracy, and slot-filling F1 score." |
| Q6 | 1 | stated_limitations | "one difficulty in creating massively multilingual NLU models is the lack of labeled data for training and evaluation, particularly data that is realistic for the task and that is natural for each given language." |
| Q7 | 1 | stated_limitations | "High naturalness typically requires human-based vetting, which is often costly." |
| Q8 | 1 | authors_affiliations | "Jack FitzGerald, Christopher Hench, Charith Peris, Scott Mackie, Kay Rottmann, Ana Sanchez, Aaron Nash, Liam Urbach, Vishesh Kakarala, Richa Singh, Swetha Ranganath, Laurie Crist, Misha Britan, Wouter Leeuwis, Gokhan Tur, Prem Natarajan from Amazon, Microsoft, Tripadvisor, and Capital One." |
| Q9 | 2 | data_sources | "The first iteration for the foundation of the MASSIVE dataset was the NLU Evaluation Benchmarking Dataset, with 25k utterances across 18 domains (Liu et al., 2019a)." |
| Q10 | 2 | data_format | "The authors updated the dataset and added audio and ASR transcriptions in the release of the Spoken Language Understanding Resource Package (SLURP) (Bastianelli et al., 2020), allowing for full end-to-end Spoken Language Understanding (SLU) evaluation similar to the Fluent Speech Commands dataset (Lugosch et al., 2019) and Chinese Audio-Textual Spoken Language Understanding (CATSLU) (Zhu et al., 2019)." |
| Q11 | 2 | task_taxonomy | "We release the MASSIVE dataset along with baselines from large pre-trained models fine-tuned on the NLU slot and intent prediction tasks." |
| Q12 | 2 | task_taxonomy | "This work focuses on the general multi-domain NLU task and builds off the SLURP (Bastianelli et al., 2020) benchmark dataset to extend to an unprecedented 50 new languages." |
| Q13 | 2 | task_taxonomy | "The Snips datasets (both the original English only and the English and French releases) are most similar to the NLU contained in the MASSIVE dataset, spanning smart home and music domains for a generic voice-based virtual assistant." |
| Q14 | 2 | stated_limitations | "Facebook released a general Intelligent Virtual Assistant (IVA) dataset across the domains of Alarm, Reminder, and Weather (Schuster et al., 2019) created for the purpose of demonstrating cross-lingual transfer learning; and so did not need to be parallel or have an equal number of datapoints, resulting in far fewer examples in Thai (5k) compared to Spanish (7.6k) and English (43k)." |
| Q15 | 3 | data_sources | "The languages in MASSIVE were chosen according to the following considerations. First, we acquired cost and worker availability estimates for over 100 languages, providing a constraint to our choices given our fixed budget." |
| Q16 | 3 | task_taxonomy | "Second, we determined existing languages available in major virtual assistants, such that the dataset could be used to benchmark today's systems." |
| Q17 | 3 | data_sources | "Third, we categorized the full pool of languages according to their genera as taken from the World Atlas of Linguistic Structures (WALS) database (Dryer and Haspelmath, 2013), where a genus is a language group that is clear to most linguists without systematic comparative analysis." |
| Q18 | 3 | task_taxonomy | "Genus is a better indicator of typological diversity, which we sought to maximize, than language family (Dryer, 1989)." |
| Q19 | 3 | data_sources | "Fourth, we used the eigenvector centrality of Wikipedia articles, tweets, and book translations (Ronen et al., 2014) as proxies for the internet influence and thus the resource availability of a given language, particularly for self-supervised pretraining applications, and we chose languages spanning the breadth of resource availability." |
| Q20 | 3 | data_format | "Fifth, we examined the script of each language, seeking to increase script diversity to drive experimentation in tokenization and normalization." |
| Q21 | 3 | data_sources | "Ultimately, we created 50 new, distinct text corpora, representing 49 different spoken languages." |
| Q22 | 3 | data_sources | "Mandarin Chinese was collected twice, once with native speakers who use the traditional set of characters, and once with native speakers who use the modern simplified set of characters." |
| Q23 | 3 | data_sources | "There are 14 language families in the dataset." |
| Q24 | 3 | task_taxonomy | "In MASSIVE, we also include "language isolates" as families. These are languages that have no clear relationship to any known language." |
| Q25 | 3 | data_format | "There are 21 distinct scripts used in the dataset." |
| Q26 | 3 | data_format | "The majority of languages in MASSIVE (28 including English) use some variety of the Latin alphabet, which is also the most widely used script in the world." |
| Q27 | 3 | data_format | "The Arabic script is used for three languages, the Cyrillic script for two languages, and the remaining 18 languages have "unique" scripts, in the sense that only one language in the dataset uses that script." |
| Q28 | 3 | data_format | "Fourteen scripts are unique to a single language, although they may belong to a larger family of writing systems." |
| Q29 | 4 | data_sources | "MASSIVE consists of utterances directed at a device, rather than a person, which has some consequences for the type of linguistic patterns it contains." |
| Q30 | 4 | task_taxonomy | "Specifically, the corpus primarily consists of interrogatives (i.e., questions) and imperatives (commands or requests)." |
| Q31 | 4 | stated_limitations | "There are relatively few declarative utterances in the set." |
| Q32 | 4 | stated_limitations | "This is in contrast to many large datasets from other sources (e.g., wikipedia, movie scripts, newspapers) which contain a high proportion of declaratives, since the language is collected from situations where humans are communicating with humans." |
| Q33 | 4 | data_sources | "In the context of a voice assistant, a user typically asks a device to perform an action or answer a question, so declaratives are less common." |
| Q34 | 4 | task_taxonomy | "In MASSIVE, 39 languages are subject-initial (24 SVO and 15 SOV), while only three are verb-initial (VSO specifically)." |
| Q35 | 4 | task_taxonomy | "No object-initial languages are represented." |
| Q36 | 4 | stated_limitations | "Five languages are marked in WALS as having no preferred word order, and four do not have any word order data at all." |
| Q37 | 4 | task_taxonomy | "The majority of them (33) use some kind of verb morphology, such as adding a suffix." |
| Q38 | 4 | task_taxonomy | "About half of those languages (18) have distinct imperative" |
| Q39 | 5 | data_sources | "We randomly sampled a subset of the English seed data which was then paraphrased by professional annotators, resulting in new, more challenging utterances, including 49% more slots per utterance." |
| Q40 | 5 | evaluation_metrics | "These utterances were localized along with the other splits to be used as a held out evaluation set for the Massively Multilingual NLU-22 competition and workshop." |
| Q41 | 5 | data_sources | "The MASSIVE dataset was collected using a customized workflow powered by Amazon MTurk." |
| Q42 | 5 | data_sources | "We required a vendor pool with the capability and resources to collect a large multilingual dataset." |
| Q43 | 5 | annotation_process | "Our original vendor pool consisted of five vendors adjudicated based on previous engagements." |
| Q44 | 5 | annotation_process | "This vendor pool was reduced to three based on engagement and resource availability." |
| Q45 | 5 | annotation_process | "Vendors for each language were selected based on their resource" |
| Q46 | 5 | task_taxonomy | "Nearly half of the languages in MASSIVE (21) make a two-way formal/informal distinction in their second-person pronouns." |
| Q47 | 5 | task_taxonomy | "A further eight languages have more than two levels of formality, such as informal, formal, and honorific." |
| Q48 | 5 | task_taxonomy | "Seven languages have an "avoidance" strategy, which means that pronouns are omitted entirely in a polite scenario." |
| Q49 | 5 | stated_limitations | "Finally, eleven languages have no data on politeness in WALS at all." |
| Q50 | 6 | data_sources | "A majority of languages were supported by a single vendor, while some languages required cross-vendor support to be completed with the required quality and within the required timeline." |
| Q51 | 6 | annotation_process | "We offered two mechanisms to vendors for evaluating workers to be selected for each language. The first, which was used to select workers for the translation task, was an Amazon MTurk-hosted fluency test where workers listen to questions and statements in the relevant language and were evaluated using a multiple-choice questionnaire." |
| Q52 | 6 | annotation_process | "The second, which was used to select workers for the judgment task, was a test with a set of three judgments that the vendor could use to assess if workers were able to detect issues in the translated utterances." |
| Q53 | 6 | annotation_process | "In order to further improve worker selection quality, we created a translator quiz using the Amazon MTurk instructions that were created for translation and judgment tasks, coupled with customized local-language examples." |
| Q54 | 6 | annotation_process | "Before commencing operations, an initial pilot run of this customized workflow was completed in three languages." |
| Q55 | 6 | data_format | "The collection was conducted by locale on an individual utterance level. Each utterance from the "train," "dev," "test," and "heldout" splits of the SLURP dataset went through two sequential task workflows and a judgment workflow." |
| Q56 | 6 | task_taxonomy | "The first task is slot translation or localization (see Figure 1). Workers are presented the entire utterance with colored highlighting of the slot values for the utterance (if any) and then presented with each slot value and its corresponding label individually." |
| Q57 | 6 | task_taxonomy | "The worker is asked to either localize or translate the slot, depending on whether the value should be translated (e.g., "tomorrow") or localized (e.g., the movie "La La Land", which in French is "Pour l'amour d'Hollywood.")" |
| Q58 | 6 | label_categories | "The metadata of the released dataset includes whether the worker elected to "localize," "translate," or keep the slot "unchanged," primarily for the purposes of researchers evaluating machine translation systems, where it would be unreasonable to expect the system to "localize" to a specific song name the worker selected." |
| Q59 | 6 | task_taxonomy | "After the slot task, the second worker is asked to translate or localize the entire phrase using the slot task output provided by the first worker (see Figure 2)." |
| Q60 | 6 | task_taxonomy | "The phrase worker can decide to keep the slot as it was translated, modify it, or remove it entirely if it is not relevant for the language in that scenario." |
| Q61 | 6 | task_taxonomy | "This worker is also responsible for aligning grammatical genders or prepositional affixes to any of the slots." |
| Q62 | 6 | stated_limitations | "Note that this two-step system alleviates the annotation burden often encountered with such work. Traditionally in such collections, workers would be given a light annotation guide and asked to highlight spans of the slots in a translated or localized utterance." |
| Q63 | 6 | evaluation_metrics | "The output of the second workflow (the fully localized utterance) is judged by three workers for (1) whether the utterance matches the intent semantically, (2) whether the slots match their labels semantically, (3) grammaticality and naturalness, (4) spelling, and (5) language identification—English or mixed utterances are acceptable if that is natural for the language, but localizations without any tokens in the target language were not accepted." |
| Q64 | 6 | label_categories | "These judgments are also included in the metadata of the dataset." |
| Q65 | 6 | annotation_process | "In addition to the workers judging each other's work, the collection system had alarms in place for workers with high rejection rates, high rates of slot deletion, and high rates of English tokens in the translations." |
| Q66 | 6 | annotation_process | "Workers were also monitored to see if their tasks were primarily machine translated. Such workers were removed from the pool and all of their work was resubmitted to be completed by the other workers." |
| Q67 | 7 | task_taxonomy | "As initial model benchmarks, we fine-tuned publicly-available pre-trained language models on the MASSIVE dataset and evaluated them on intent classification and slot filling." |
| Q68 | 7 | evaluation_metrics | "Our models of choice for this exercise were XLM-Roberta (XLM-R; Conneau et al. 2020) and mT5 (Xue et al., 2021)." |
| Q69 | 7 | evaluation_metrics | "In the case of XLM-R, we utilized the pretrained encoder with two separate classification heads trained from scratch, based on JointBERT (Chen et al., 2019a)." |
| Q70 | 7 | evaluation_metrics | "The first classification head used the pooled output from the encoder to predict the intent and the second used the sequence output to predict the slots." |
| Q71 | 7 | evaluation_metrics | "As pooling for the intent classification head, we experimented with using hidden states from the first position, averaged hidden states across the sequence, and the maximally large hidden state from the sequence." |
| Q72 | 7 | evaluation_metrics | "With mT5, we explored two separate architectures. In one architecture, we only used the pre-trained encoder extracted from mT5, and we trained two classification heads from scratch similarly to the XLM-R setup. We refer to this setup as mT5 Encoder-Only. In the other architecture, we used the full sequence-to-sequence mT5 model in text-to-text mode, where the input is "Annotate:" followed by the unlabeled utterance." |
| Q73 | 7 | label_categories | "The decoder output is a sequence of labels (including the Other label) for all of the tokens followed by the intent." |
| Q74 | 7 | evaluation_metrics | "For all models, we used the Base size, which corresponds to 270M parameters for XLM-R, 258M parameters for mT5 Encoder-Only, and 580M parameters for mT5 Text-to-Text, including 192M parameters for embeddings for all three." |
| Q75 | 7 | evaluation_metrics | "For each model, we performed 128 trials of hyperparameter tuning using the Tree of Parzen Estimators algorithm and Asynchronous Successive Halving Algorithm (ASHA) (Li et al., 2018a) for scheduling, which are both part of the hyperopt library (Bergstra et al., 2013) integrated into the ray[tune] library (Liaw et al., 2018)." |
| Q76 | 7 | evaluation_metrics | "We trained our models with the Adam optimizer (Kingma and Ba, 2017) and chose the best performing model checkpoint based on overall exact match accuracy across all locales." |
| Q77 | 7 | evaluation_metrics | "Hyperparameter tuning and fine-tuning was performed using single p3dn.24xlarge instances (8 x Nvidia v100) for XLM-R and mT5 Text-to-Text and a single g4dn.metal instance (8 x Nvidia T4) for mT5 Encoder-Only." |
| Q78 | 7 | evaluation_metrics | "Hyperparameter tuning times were less than 4 days per model and training times were less than 1 day per model." |
| Q79 | 7 | data_format | "Our dataset includes several languages where white spacing is not used as a word delimiter. In some cases, spaces do occur, but they might serve as phrase delimiters or denote the end of a sentence." |
| Q80 | 7 | data_format | "Three of these written languages, Japanese, Chinese (Traditional), and Chinese (Simplified), do not use spaces anywhere except to identify the end of a sentence. For these languages, we separate each character in the unlabeled input with a whitespace." |
| Q81 | 7 | stated_limitations | "We leave exploration of more sophisticated techniques (such as MeCab for Japanese; Kudo 2005) to future work." |
| Q82 | 7 | data_format | "We use the default spacing provided by annotators for all other languages." |
| Q83 | 7 | evaluation_metrics | "Zero-shot performance was also assessed, in which the models were trained on English data, validation was performed on all languages, and testing was performed on all non-English locales." |
| Q84 | 7 | evaluation_metrics | "Table 3 shows the results for each model and training setup, including those for the best performing locale, the worst performing locale, and locale-averaged results for intent accuracy, micro-averaged slot F1 score, and exact match accuracy." |
| Q85 | 7 | evaluation_metrics | "Zero-shot exact match performance is 25-37 points worse than that of full-dataset training runs." |
| Q86 | 7 | evaluation_metrics | "Additionally, the variance in task performance across locales is significantly greater for the zero-shot setup than for full-dataset training. For example, there is a 15 point difference in exact match accuracy between the highest and lowest locales for mT5 Text-to-Text when using the full training set, while the gap expands to 44 points with zero-shot." |
| Q87 | 7 | evaluation_metrics | "We compared the pretraining data quantities by language for XLM-R to its per-language task performance values, and in the zero shot setup, we found a Pearson correlation of 0.54 for exact match" |
| Q88 | 8 | evaluation_metrics | "Each table includes the highest locale, the lowest locale, and locale-averaged results for intent accuracy, micro-averaged slot F1 score, and exact match accuracy." |
| Q89 | 8 | evaluation_metrics | "Intervals for 95% confidence are given assuming normal distributions." |
| Q90 | 8 | evaluation_metrics | "In the full dataset training setup, the correlations decrease to 0.42 for exact match accuracy, 0.47 for intent accuracy, and 0.24 for micro-averaged slot F1 score." |
| Q91 | 8 | data_format | "In Thai, for which spacing is optional, the model can learn from artificial spacing in the input (around where the slots will be) to improve task performance." |
| Q92 | 8 | annotation_process | "For Khmer, the workers had a difficult time adapting their translations and localizations to properly-slotted outputs given the space-optional nature of the language." |
| Q93 | 8 | data_format | "Additionally, for Japanese and Chinese, we added spaces between all characters when modeling." |
| Q94 | 8 | data_format | "By splitting into single characters, we don't allow the model to the use embeddings learned for chunks of characters." |
| Q95 | 8 | stated_limitations | "This is a likely major cause of the drop in exact match accuracy for Japanese from 58.3% when training on the full dataset to 9.4% for zero shot." |
| Q96 | 8 | data_format | "character spacing was necessary in order to properly assign the slots to the right characters." |
| Q97 | 8 | stated_limitations | "As mentioned in Section 5.1, we leave exploration of more sophisticated spacing techniques for slot filling (such as MeCab; Kudo 2005) to future work." |
| Q98 | 8 | stated_limitations | "Discounting for artificial spacing effects, Germanic genera and Latin scripts performed the best overall (See Appendix E), which is unsurprising given the amount of pretraining data for those genera and scripts, as well as the quantity of Germanic and Latin-script languages in MASSIVE." |
| Q99 | 8 | evaluation_metrics | "Within the Germanic genera, Swedish, English, Danish, Norwegian, and Dutch all performed comparably (within 95% confidence bounds) for exact match accuracy." |
| Q100 | 8 | stated_limitations | "Icelandic was the lowest-performing Germanic language, likely due to a lack of pretraining data, as well as to its linguistic evolution away from the others due to isolated conditions." |
| Q101 | 8 | task_taxonomy | "We have released a truly MASSIVE multilingual dataset for NLU spanning 51 typologically diverse languages." |
| Q102 | 9 | stated_limitations | "There are several significant limitations of the MASSIVE dataset and of our modeling." |
| Q103 | 9 | stated_limitations | "Starting with the dataset, the per-language data quantities are relatively small at 19.5k total records and 11.5k records for training." |
| Q104 | 9 | stated_limitations | "Second, there are some low-quality utterances, both in the seed data and in the translations." |
| Q105 | 9 | stated_limitations | "For the most part, these are surfaced through the judgment scores we provide for each record, but if a user does filtering based on these judgments, then the data size decreases even further." |
| Q106 | 9 | stated_limitations | "Third, the data were originally created through crowd-sourcing, not from a real virtual assistant, which introduces artificialities." |
| Q107 | 9 | stated_limitations | "Relatedly, allowing the worker to decide on translation versus localization of slot entities added further noise to the dataset, although we try to store this decision in the metadata." |
| Q108 | 9 | stated_limitations | "Fourth, our labeling schema is relatively simple when compared with hierarchical labeling schemata or flat schemata with more intent and slot options." |
| Q109 | 9 | stated_limitations | "Fifth, our collection system did not have a robust method to preserving or denoting native tokenization practices—some languages do not separate with whitespace, while others do but there is no set practice." |
| Q110 | 9 | stated_limitations | "This results in potentially easier (larger chunks to predict slot labels) or harder (each character individually predicted) tasks." |
| Q111 | 9 | stated_limitations | "Sixth, it's possible, though unlikely, that some of our new crowd-sourced records may contain toxic or otherwise objectionable content." |
| Q112 | 9 | stated_limitations | "We performed analyses to check for such malicious activities and did not find any as such." |
| Q113 | 9 | stated_limitations | "Regarding modeling, we have only investigated base-sized models in relatively standard setups, leaving room for much more sophisticated modeling." |
| Q114 | 9 | stated_limitations | "The risks associated with this dataset and work are relatively low, given that we have released a research dataset meant to promote better multilinguality in NLP systems." |
| Q115 | 13 | data_format | "Additional linguistic characteristics of our languages are given in Table 4." |
| Q116 | 13 | data_sources | "Screenshots from our collection workflow are given in Figures 1, 2, and 3." |
| Q117 | 13 | evaluation_metrics | "The hyperparameter search spaces and the chosen hyperparameters are given in Tables 5 and 6." |
| Q118 | 13 | evaluation_metrics | "Results for all languages are given for exact match accuracy in Table 7, intent accuracy in Table 8, and micro-averaged slot-filling F1 in Table 9." |
| Q119 | 13 | evaluation_metrics | "We pick our best performing model, mT5 Text-to-Text, and provide a summary of its performance on different language characteristics in Figures 4 and 5." |
| Q120 | 17 | task_taxonomy | "How would you rate these sentences?" |
| Q121 | 17 | task_taxonomy | "Please respond to the following questions about the TRANSLATED SENTENCE TO RATE." |
| Q122 | 17 | annotation_process | "By clicking "SUBMIT", I also certify that I am a native speaker or am fluent in the required language" |
| Q123 | 18 | data_format | "The full-dataset hyperparameter search space, the sampling technique, and the chosen hyperparameter for our 3 models." |
| Q124 | 18 | data_format | "The search space for the "quniform" and "qloguniform" sampling techniques is given as [min, max, increment]." |
| Q125 | 19 | evaluation_metrics | "The zero-shot hyperparameter search space, the sampling technique, and the chosen hyperparameter for our 3 models." |
| Q126 | 20 | evaluation_metrics | "Exact match accuracy by language for our three models using the full dataset and the zero-shot setup." |
| Q127 | 21 | evaluation_metrics | "Table 8: Intent accuracy by language for our three models using the full dataset and the zero-shot setup." |
| Q128 | 22 | evaluation_metrics | "Micro-averaged slot-filling F1 by language for our three models using the full dataset and the zero-shot setup." |
| Q129 | 23 | evaluation_metrics | "The categories of each language characteristic are sorted by exact match accuracy for readability." |
| Q130 | 23 | data_sources | "The number of languages falling into each category is provided in the bar chart in the lowest panel for each characteristic." |
| Q131 | 24 | task_taxonomy | "mT5 Text-to-Text performance grouped by Script, Family, Order, Politeness, Imperative Morphology, Imperative Hortative, Optative and Prohibitive." |
| Q132 | 24 | evaluation_metrics | "As with Figure 4, the categories of each language characteristic are sorted by exact match accuracy for readability." |

### Category Index
- **task_taxonomy**: Q1, Q11, Q12, Q13, Q16, Q18, Q24, Q30, Q34, Q35, Q37, Q38, Q46, Q47, Q48, Q56, Q57, Q59, Q60, Q61, Q67, Q101, Q120, Q121, Q131
- **data_sources**: Q2, Q4, Q9, Q15, Q17, Q19, Q21, Q22, Q23, Q29, Q33, Q39, Q41, Q42, Q50, Q116, Q130
- **data_format**: Q3, Q10, Q20, Q25, Q26, Q27, Q28, Q55, Q79, Q80, Q82, Q91, Q93, Q94, Q96, Q115, Q123, Q124
- **label_categories**: Q58, Q64, Q73
- **annotation_process**: Q43, Q44, Q45, Q51, Q52, Q53, Q54, Q65, Q66, Q92, Q122
- **evaluation_metrics**: Q5, Q40, Q63, Q68, Q69, Q70, Q71, Q72, Q74, Q75, Q76, Q77, Q78, Q83, Q84, Q85, Q86, Q87, Q88, Q89, Q90, Q99, Q117, Q118, Q119, Q125, Q126, Q127, Q128, Q129, Q132
- **stated_limitations**: Q6, Q7, Q14, Q31, Q32, Q36, Q49, Q62, Q81, Q95, Q97, Q98, Q100, Q102, Q103, Q104, Q105, Q106, Q107, Q108, Q109, Q110, Q111, Q112, Q113, Q114
- **authors_affiliations**: Q8
