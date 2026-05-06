---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | authors_affiliations | "Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy & Samuel R. Bowman" |
| Q2 | 1 | authors_affiliations | "Courant Institute of Mathematical Sciences, New York University; Paul G. Allen School of Computer Science & Engineering, University of Washington; DeepMind" |
| Q3 | 1 | task_taxonomy | "GLUE is a collection of NLU tasks including question answering, sentiment analysis, and textual entailment, and an associated online platform for model evaluation, comparison, and analysis." |
| Q4 | 1 | data_format | "GLUE does not place any constraints on model architecture beyond the ability to process single-sentence and sentence-pair inputs and to make corresponding predictions." |
| Q5 | 1 | data_sources | "For some GLUE tasks, training data is plentiful, but for others it is limited or fails to match the genre of the test set." |
| Q6 | 1 | data_sources | "None of the datasets in GLUE were created from scratch for the benchmark; we rely on preexisting datasets because they have been implicitly agreed upon by the NLP community as challenging and interesting." |
| Q7 | 1 | data_sources | "Four of the datasets feature privately-held test data, which will be used to ensure that the benchmark is used fairly." |
| Q8 | 1 | task_taxonomy | "GLUE also includes a set of hand-crafted analysis examples for probing trained models." |
| Q9 | 1 | task_taxonomy | "This dataset is designed to highlight common challenges, such as the use of world knowledge and logical operators, that we expect models must handle to robustly solve the tasks." |
| Q10 | 1 | evaluation_metrics | "We evaluate baselines based on current methods for transfer and representation learning and find that multi-task training on all tasks performs better than training a separate model per task." |
| Q11 | 1 | stated_limitations | "However, the low absolute performance of our best model indicates the need for improved general NLU systems." |
| Q12 | 2 | label_categories | "All tasks are single sentence or sentence pair classification, except STS-B, which is a regression task. MNLI has three classes; all other classification tasks have two. Test sets shown in bold use labels that have never been made public in any form." |
| Q13 | 2 | stated_limitations | "To better understand the challenged posed by GLUE, we conduct experiments with simple baselines and state-of-the-art sentence representation models. We find that unified multi-task trained models slightly outperform comparable models trained on each task separately. Our best multi-task model makes use of ELMo (Peters et al., 2018), a recently proposed pre-training technique. However, this model still achieves a fairly low absolute score." |
| Q14 | 2 | stated_limitations | "Analysis with our diagnostic dataset reveals that our baseline models deal well with strong lexical signals but struggle with deeper logical structure." |
| Q15 | 2 | task_taxonomy | "In summary, we offer: (i) A suite of nine sentence or sentence-pair NLU tasks, built on established annotated datasets and selected to cover a diverse range of text genres, dataset sizes, and degrees of difficulty. (ii) An online evaluation platform and leaderboard, based primarily on privately-held test data. The platform is model-agnostic, and can evaluate any method capable of producing results on all nine tasks. (iii) An expert-constructed diagnostic evaluation dataset. (iv) Baseline results for several major existing approaches to sentence representation learning." |
| Q16 | 2 | task_taxonomy | "Like GLUE, SentEval relies on a set of existing classification tasks involving either one or two sentences as inputs. Unlike GLUE, SentEval only evaluates sentence-to-vector encoders, making it well-suited for evaluating models on tasks involving sentences in isolation." |
| Q17 | 2 | task_taxonomy | "GLUE is designed to facilitate the development of these methods: It is model-agnostic, allowing for any kind of representation or contextualization, including models that use no explicit vector or symbolic representations for sentences whatsoever." |
| Q18 | 3 | task_taxonomy | "GLUE is centered on nine English sentence understanding tasks, which cover a broad range of domains, data quantities, and difficulties." |
| Q19 | 3 | task_taxonomy | "As the goal of GLUE is to spur development of generalizable NLU systems, we design the benchmark such that good performance should require a model to share substantial knowledge (e.g., trained parameters) across all tasks, while still maintaining some task-specific components." |
| Q20 | 3 | evaluation_metrics | "Unless otherwise mentioned, tasks are evaluated on accuracy and are balanced across classes." |
| Q21 | 3 | data_sources | "The Corpus of Linguistic Acceptability (Warstadt et al., 2018) consists of English acceptability judgments drawn from books and journal articles on linguistic theory." |
| Q22 | 3 | label_categories | "Each example is a sequence of words annotated with whether it is a grammatical English sentence." |
| Q23 | 3 | evaluation_metrics | "Following the authors, we use Matthews correlation coefficient (Matthews, 1975) as the evaluation metric, which evaluates performance on unbalanced binary classification and ranges from -1 to 1, with 0 being the performance of uninformed guessing." |
| Q24 | 3 | data_sources | "We use the standard test set, for which we obtained private labels from the authors." |
| Q25 | 3 | evaluation_metrics | "We report a single performance number on the combination of the in- and out-of-domain sections of the test set." |
| Q26 | 3 | data_sources | "The Stanford Sentiment Treebank (Socher et al., 2013) consists of sentences from movie reviews and human annotations of their sentiment." |
| Q27 | 3 | task_taxonomy | "The task is to predict the sentiment of a given sentence." |
| Q28 | 3 | label_categories | "We use the two-way (positive/negative) class split, and use only sentence-level labels." |
| Q29 | 3 | data_sources | "The Microsoft Research Paraphrase Corpus (Dolan & Brockett, 2005) is a corpus of sentence pairs automatically extracted from online news sources, with human annotations for whether the sentences in the pair are semantically equivalent." |
| Q30 | 3 | evaluation_metrics | "Because the classes are imbalanced (68% positive), we follow common practice and report both accuracy and F1 score." |
| Q31 | 3 | data_sources | "The Quora Question Pairs dataset is a collection of question pairs from the community question-answering website Quora." |
| Q32 | 3 | task_taxonomy | "The task is to determine whether a pair of questions are semantically equivalent." |
| Q33 | 3 | evaluation_metrics | "As in MRPC, the class distribution in QQP is unbalanced (63% negative), so we report both accuracy and F1 score." |
| Q34 | 3 | stated_limitations | "We observe that the test set has a different label distribution than the training set." |
| Q35 | 3 | data_sources | "The Semantic Textual Similarity Benchmark (Cer et al., 2017) is a collection of sentence pairs drawn from news headlines, video and image captions, and natural language inference data. Each pair is human-annotated with a similarity score from 1 to 5; the task is to predict these scores. Follow common practice, we evaluate using Pearson and Spearman correlation coefficients." |
| Q36 | 4 | data_sources | "The Multi-Genre Natural Language Inference Corpus (Williams et al., 2018) is a crowdsourced collection of sentence pairs with textual entailment annotations." |
| Q37 | 4 | task_taxonomy | "Given a premise sentence and a hypothesis sentence, the task is to predict whether the premise entails the hypothesis (entailment), contradicts the hypothesis (contradiction), or neither (neutral)." |
| Q38 | 4 | data_sources | "The premise sentences are gathered from ten different sources, including transcribed speech, fiction, and government reports." |
| Q39 | 4 | data_sources | "We use the standard test set, for which we obtained private labels from the authors, and evaluate on both the matched (in-domain) and mismatched (cross-domain) sections." |
| Q40 | 4 | data_sources | "We also use and recommend the SNLI corpus (Bowman et al., 2015) as 550k examples of auxiliary training data." |
| Q41 | 4 | data_sources | "The Stanford Question Answering Dataset (Rajpurkar et al. 2016) is a question-answering dataset consisting of question-paragraph pairs, where one of the sentences in the paragraph (drawn from Wikipedia) contains the answer to the corresponding question (written by an annotator)." |
| Q42 | 4 | data_format | "We convert the task into sentence pair classification by forming a pair between each question and each sentence in the corresponding context, and filtering out pairs with low lexical overlap between the question and the context sentence." |
| Q43 | 4 | task_taxonomy | "The task is to determine whether the context sentence contains the answer to the question." |
| Q44 | 4 | stated_limitations | "This modified version of the original task removes the requirement that the model select the exact answer, but also removes the simplifying assumptions that the answer is always present in the input and that lexical overlap is a reliable cue." |
| Q45 | 4 | data_format | "This process of recasting existing datasets into NLI is similar to methods introduced in White et al. (2017) and expanded upon in Demszky et al. (2018)." |
| Q46 | 4 | data_sources | "The Recognizing Textual Entailment (RTE) datasets come from a series of annual textual entailment challenges." |
| Q47 | 4 | data_sources | "We combine the data from RTE1 (Dagan et al., 2006), RTE2 (Bar Haim et al., 2006), RTE3 (Giampiccolo et al., 2007), and RTE5 (Bentivogli et al., 2009)." |
| Q48 | 4 | data_sources | "Examples are constructed based on news and Wikipedia text." |
| Q49 | 4 | data_format | "We convert all datasets to a two-class split, where for three-class datasets we collapse neutral and contradiction into not entailment, for consistency." |
| Q50 | 4 | data_sources | "The Winograd Schema Challenge (Levesque et al., 2011) is a reading comprehension task in which a system must read a sentence with a pronoun and select the referent of that pronoun from a list of choices." |
| Q51 | 4 | data_sources | "The examples are manually constructed to foil simple statistical methods: Each one is contingent on contextual information provided by a single word or phrase in the sentence." |
| Q52 | 4 | data_format | "To convert the problem into sentence pair classification, we construct sentence pairs by replacing the ambiguous pronoun with each possible referent." |
| Q53 | 5 | data_sources | "We use a small evaluation set consisting of new examples derived from fiction books that was shared privately by the authors of the original corpus." |
| Q54 | 5 | data_format | "While the included training set is balanced between two classes, the test set is imbalanced between them (65% not entailment)." |
| Q55 | 5 | stated_limitations | "Also, due to a data quirk, the development set is adversarial: hypotheses are sometimes shared between training and development examples, so if a model memorizes the training examples, they will predict the wrong label on corresponding development set example." |
| Q56 | 5 | label_categories | "Labels are entailment (E), neutral (N), or contradiction (C)." |
| Q57 | 5 | evaluation_metrics | "The GLUE benchmark follows the same evaluation model as SemEval and Kaggle." |
| Q58 | 5 | evaluation_metrics | "To evaluate a system on the benchmark, one must run the system on the provided test data for the tasks, then upload the results to the website gluebenchmark.com for scoring." |
| Q59 | 5 | evaluation_metrics | "The benchmark site shows per-task scores and a macro-average of those scores to determine a system's position on the leaderboard." |
| Q60 | 5 | evaluation_metrics | "For tasks with multiple metrics (e.g., accuracy and F1), we use an unweighted average of the metrics as the score for the task when computing the overall macro-average." |
| Q61 | 5 | data_sources | "Drawing inspiration from the FraCaS suite (Cooper et al., 1996) and the recent Build-It-Break-It competition (Ettinger et al., 2017), we include a small, manually-curated test set for the analysis of system performance." |
| Q62 | 5 | data_format | "Each diagnostic example is an NLI sentence pair with tags for the phenomena demonstrated." |
| Q63 | 5 | data_sources | "We ensure the data is reasonably diverse by producing examples for a variety of linguistic phenomena and basing our examples on naturally-occurring sentences from several domains (news, Reddit, Wikipedia, academic papers)." |
| Q64 | 6 | task_taxonomy | "We begin with a target set of phenomena, based roughly on those used in the FraCaS suite (Cooper et al., 1996)." |
| Q65 | 6 | annotation_process | "We construct each example by locating a sentence that can be easily made to demonstrate a target phenomenon, and editing it in two ways to produce an appropriate sentence pair." |
| Q66 | 6 | annotation_process | "We make minimal modifications so as to maintain high lexical and structural overlap within each sentence pair and limit superficial cues." |
| Q67 | 6 | annotation_process | "We then label the inference relationships between the sentences, considering each sentence alternatively as the premise, producing two labeled examples for each pair (1100 total)." |
| Q68 | 6 | annotation_process | "Where possible, we produce several pairs with different labels for a single source sentence, to have minimal sets of sentence pairs that are lexically and structurally very similar but correspond to different entailment relationships." |
| Q69 | 6 | label_categories | "The resulting labels are 42% entailment, 35% neutral, and 23% contradiction." |
| Q70 | 6 | evaluation_metrics | "Since the class distribution in the diagnostic set is not balanced, we use R3 (Gorodkin, 2004), a three-class generalization of the Matthews correlation coefficient, for evaluation." |
| Q71 | 6 | evaluation_metrics | "We reproduce the methodology of Gururangan et al. (2018), training two fastText classifiers (Joulin et al., 2016) to predict entailment labels on SNLI and MNLI using only the hypothesis as input." |
| Q72 | 6 | evaluation_metrics | "The models respectively get near-chance accuracies of 32.7% and 36.4% on our diagnostic data, showing that the data does not suffer from such artifacts." |
| Q73 | 6 | annotation_process | "To establish human baseline performance on the diagnostic set, we have six NLP researchers annotate 50 sentence pairs (100 entailment examples) randomly sampled from the diagnostic set." |
| Q74 | 6 | annotation_process | "Inter-annotator agreement is high, with a Fleiss's κ of 0.73." |
| Q75 | 6 | evaluation_metrics | "The average R3 score among the annotators is 0.80, much higher than any of the baseline systems described in Section 5." |
| Q76 | 6 | stated_limitations | "The diagnostic examples are hand-picked to address certain phenomena, and NLI is a task with no natural input distribution, so we do not expect performance on the diagnostic set to reflect overall performance or generalization in downstream applications." |
| Q77 | 6 | stated_limitations | "Performance on the analysis set should be compared between models but not between categories." |
| Q78 | 6 | stated_limitations | "The set is provided not as a benchmark, but as an analysis tool for error analysis, qualitative model comparison, and development of adversarial examples." |
| Q79 | 6 | authors_affiliations | "We implement our models in the AllenNLP library (Gardner et al., 2017)." |
| Q80 | 6 | evaluation_metrics | "Our simplest baseline architecture is based on sentence-to-vector encoders, and sets aside GLUE's ability to evaluate models with more complex structures." |
| Q81 | 6 | evaluation_metrics | "Taking inspiration from Conneau et al. (2017), the model uses a two-layer, 1500D (per direction) BiLSTM with max pooling and 300D GloVe word embeddings (840B Common Crawl version; Pennington et al., 2014)." |
| Q82 | 6 | evaluation_metrics | "For single-sentence tasks, we encode the sentence and pass the resulting vector to a classifier." |
| Q83 | 6 | evaluation_metrics | "For sentence-pair tasks, we encode sentences independently to produce vectors u, v, and pass [u; v; \|u − v\|; u ∗ v] to a classifier." |
| Q84 | 6 | evaluation_metrics | "The classifier is an MLP with a 512D hidden layer." |
| Q85 | 6 | evaluation_metrics | "We also consider a variant of our model which for sentence pair tasks uses an attention mechanism inspired by Seo et al. (2017) between all pairs of words, followed by a second BiLSTM with max pooling." |
| Q86 | 6 | evaluation_metrics | "By explicitly modeling the interaction between sentences, these models fall outside the sentence-to-vector paradigm." |
| Q87 | 6 | evaluation_metrics | "We augment our base model with two recent methods for pre-training: ELMo and CoVe." |
| Q88 | 6 | evaluation_metrics | "We use existing trained models for both." |
| Q89 | 6 | evaluation_metrics | "ELMo uses a pair of two-layer neural language models trained on the Billion Word Benchmark (Chelba et al., 2013)." |
| Q90 | 6 | evaluation_metrics | "Each word is represented by a contextual embedding, produced by taking a" |
| Q91 | 7 | data_format | "We train our models with the BiLSTM sentence encoder and post-attention BiLSTMs shared across tasks, and classifiers trained separately for each task." |
| Q92 | 7 | data_format | "For each training update, we sample a task to train with a probability proportional to the number of training examples for each task." |
| Q93 | 7 | data_format | "We train our models with Adam (Kingma & Ba, 2015) with initial learning rate 10−4 and batch size 128." |
| Q94 | 7 | evaluation_metrics | "We use the macro-average score as the validation metric and stop training when the learning rate drops below 10−5 or performance does not improve after 5 validation checks." |
| Q95 | 7 | data_format | "We also train a set of single-task models, which are configured and trained identically, but share no parameters." |
| Q96 | 7 | stated_limitations | "To allow for fair comparisons with the multi-task analogs, we do not tune parameter or training settings for each task, so these single-task models do not generally represent the state of the art for each task." |
| Q97 | 7 | task_taxonomy | "Finally, we evaluate the following trained sentence-to-vector encoder models using our benchmark: average bag-of-words using GloVe embeddings (CBoW), Skip-Thought (Kiros et al., 2015), InferSent (Conneau et al., 2017), DisSent (Nie et al., 2017), and GenSen (Subramanian et al., 2018)." |
| Q98 | 7 | data_format | "For these models, we only train task-specific classifiers on the representations they produce." |
| Q99 | 8 | evaluation_metrics | "We train three runs of each model and evaluate the run with the best macro-average development set performance (see Table 6 in Appendix C)." |
| Q100 | 8 | evaluation_metrics | "For single-task and sentence representation models, we evaluate the best run for each individual task." |
| Q101 | 8 | task_taxonomy | "We find that multi-task training yields better overall scores over single-task training amongst models using attention or ELMo." |
| Q102 | 8 | task_taxonomy | "Attention generally has negligible or negative aggregate effect in single task training, but helps in multi-task training." |
| Q103 | 8 | data_format | "We see a consistent improvement in using ELMo embeddings in place of GloVe or CoVe embeddings, particularly for single-sentence tasks." |
| Q104 | 8 | data_format | "Using CoVe has mixed effects over using only GloVe." |
| Q105 | 8 | task_taxonomy | "Among the pre-trained sentence representation models, we observe fairly consistent gains moving from CBoW to Skip-Thought to Infersent and GenSen." |
| Q106 | 8 | stated_limitations | "On WNLI, no model exceeds most-frequent-class guessing (65.1%) and we substitute the model predictions for the most-frequent baseline." |
| Q107 | 8 | stated_limitations | "On RTE and in aggregate, even our best baselines leave room for improvement." |
| Q108 | 8 | stated_limitations | "These early results indicate that solving GLUE is beyond the capabilities of current models and methods." |
| Q109 | 9 | evaluation_metrics | "We analyze the baselines by evaluating each model's MNLI classifier on the diagnostic set to get a better sense of their linguistic capabilities." |
| Q110 | 9 | evaluation_metrics | "Overall performance is low for all models: The highest total score of 28 still denotes poor absolute performance." |
| Q111 | 9 | task_taxonomy | "Performance tends to be higher on Predicate-Argument Structure and lower on Logic, though numbers are not closely comparable across categories." |
| Q112 | 9 | stated_limitations | "Unlike on the main benchmark, the multi-task models are almost always outperformed by their single-task counterparts." |
| Q113 | 9 | evaluation_metrics | "Most models handle universal quantification relatively well." |
| Q114 | 9 | stated_limitations | "Double negation is especially difficult for the GLUE-trained models that only use GloVe embeddings." |
| Q115 | 9 | stated_limitations | "We expect that our platform and diagnostic dataset will be useful for similar analyses in the future, so that model designers can better understand their models' generalization behavior and implicit knowledge." |
| Q116 | 9 | task_taxonomy | "We introduce GLUE, a platform and collection of resources for evaluating and analyzing natural language understanding systems." |
| Q117 | 9 | authors_affiliations | "We thank Ellie Pavlick, Tal Linzen, Kyunghyun Cho, and Nikita Nangia for their comments on this work at its early stages, and we thank Ernie Davis, Alex Warstadt, and Quora's Nikhil Dandekar and Kornel Csernai for providing access to private evaluation data." |
| Q118 | 9 | authors_affiliations | "This project has benefited from financial support to SB by Google, Tencent Holdings, and Samsung Research, and to AW from AdeptMind and an NSF Graduate Research Fellowship." |
| Q119 | 13 | data_sources | "To construct a balanced dataset, we select all pairs in which the most similar sentence to the question was not the answer sentence, as well as an equal amount of cases in which the correct sentence was the most similar to the question, but another distracting sentence was a close second." |
| Q120 | 13 | data_format | "Our similarity metric is based on CBoW representations with pre-trained GloVe embeddings." |
| Q121 | 13 | data_sources | "This approach to converting pre-existing datasets into NLI format is closely related to recent work by White et al. (2017), as well as to the original motivation for textual entailment presented by Dagan et al. (2006)." |
| Q122 | 13 | task_taxonomy | "Both argue that many NLP tasks can be productively reduced to textual entailment." |
| Q123 | 14 | data_format | "We implement our attention mechanism as follows: given two sequences of hidden states u1, u2, . . . , uM and v1, v2, . . . , vN, we first compute matrix H where Hij = ui· vj." |
| Q124 | 14 | data_format | "We scale each task's loss inversely proportional to the number of examples for that task, which we found to improve overall performance." |
| Q125 | 14 | data_format | "We train our models with Adam (Kingma & Ba, 2015) with initial learning rate 10−3, batch size 128, and gradient clipping." |
| Q126 | 14 | evaluation_metrics | "We use macro-average score over all tasks as our validation metric, and perform a validation check every 10k updates." |
| Q127 | 14 | data_format | "We divide the learning rate by 5 whenever validation performance does not improve." |
| Q128 | 14 | data_format | "We stop training when the learning rate drops below 10−5 or performance does not improve after 5 validation checks." |
| Q129 | 14 | task_taxonomy | "We evaluate the following sentence representation models: 1. CBoW, the average of the GloVe embeddings of the tokens in the sentence. 2. Skip-Thought (Kiros et al., 2015), a sequence-to-sequence(s) model trained to generate the previous and next sentences given the middle sentence. 3. InferSent (Conneau et al., 2017), a BiLSTM with max-pooling trained on MNLI and SNLI. 4. DisSent (Nie et al., 2017), a BiLSTM with max-pooling trained to predict the discourse marker (because, so, etc.) relating two sentences on data derived from TBC. 5. GenSen (Subramanian et al., 2018), a sequence-to-sequence model trained on a variety of supervised and unsupervised objectives." |
| Q130 | 14 | data_format | "We train task-specific classifiers on top of frozen sentence encoders, using the default parameters from SentEval." |
| Q131 | 14 | stated_limitations | "The GLUE website limits users to two submissions per day in order to avoid overfitting to the private test data." |
| Q132 | 14 | data_sources | "GLUE's online platform is built using React, Redux and TypeScript." |
| Q133 | 14 | data_sources | "We use Google Firebase for data storage and Google Cloud Functions to host and run our grading script when a submission is made." |
| Q134 | 15 | task_taxonomy | "The dataset is designed to allow for analyzing many levels of natural language understanding, from word meaning and sentence structure to high-level reasoning and application of world knowledge." |
| Q135 | 15 | task_taxonomy | "To make this kind of analysis feasible, we first identify four broad categories of phenomena: Lexical Semantics, Predicate-Argument Structure, Logic, and Knowledge." |
| Q136 | 15 | task_taxonomy | "However, since these categories are vague, we divide each into a larger set of fine-grained subcategories." |
| Q137 | 15 | task_taxonomy | "These categories are not based on any particular linguistic theory, but broadly based on issues that linguists have often identified and modeled in the study of syntax and semantics." |
| Q138 | 15 | stated_limitations | "The dataset is provided not as a benchmark, but as an analysis tool to paint in broad strokes the kinds of phenomena a model may or may not capture, and to provide a set of examples that can serve for error analysis, qualitative model comparison, and development of adversarial examples that expose a model's weaknesses." |
| Q139 | 15 | stated_limitations | "Because the distribution of language is somewhat arbitrary, it will not be helpful to compare performance of the same model on different categories." |
| Q140 | 15 | evaluation_metrics | "Rather, we recommend comparing performance that different models score on the same category, or using the reported scores as a guide for error analysis." |
| Q141 | 15 | label_categories | "Note that some examples may be tagged with phenomena belonging to multiple categories." |
| Q142 | 16 | task_taxonomy | "These phenomena center on aspects of word meaning." |
| Q143 | 16 | task_taxonomy | "Entailment can be applied not only on the sentence level, but the word level." |
| Q144 | 16 | task_taxonomy | "This relationship applies to many types of words (nouns, adjectives, verbs, many prepositions, etc.) and the relationship between lexical and sentential entailment has been deeply explored, e.g., in systems of natural logic." |
| Q145 | 16 | task_taxonomy | "This is a special case of lexical contradiction where one word is derived from the other: from "affordable" to "unaffordable", "agree" to "disagree", etc." |
| Q146 | 16 | task_taxonomy | "Propositions appearing in a sentence may be in any entailment relation with the sentence as a whole, depending on the context in which they appear." |
| Q147 | 16 | task_taxonomy | "In many cases, this is determined by lexical triggers (usually verbs or adverbs) in the sentence." |
| Q148 | 16 | label_categories | "We place all examples involving these phenomena under the label of Factivity." |
| Q149 | 16 | task_taxonomy | "Some propositions denote symmetric relations, while others do not." |
| Q150 | 16 | task_taxonomy | "Whether a relation is symmetric, or admits collecting its arguments into the subject, is often determined by its head word (e.g., "like", "marry" or "meet"), so we classify it under Lexical Semantics." |
| Q151 | 16 | task_taxonomy | "If a word can be removed from a sentence without changing its meaning, that means the word's meaning was more-or-less adequately expressed by the sentence; so, identifying these cases reflects an understanding of both lexical and sentential semantics." |
| Q152 | 17 | task_taxonomy | "Named Entities Words often name entities that exist in the world. There are many different kinds of understanding we might wish to understand about these names, including their compositional structure (for example, the "Baltimore Police" is the same as the "Police of the City of Baltimore") or their real-world referents and acronym expansions (for example, "SNL" is "Saturday Night Live"). This category is closely related to World Knowledge, but focuses on the semantics of names as lexical items rather than background knowledge about their denoted entities." |
| Q153 | 17 | task_taxonomy | "Quantifiers Logical quantification in natural language is often expressed through lexical triggers such as "every", "most", "some", and "no". While we reserve the categories in Quantification and Monotonicity for entailments involving operations on these quantifiers and their arguments, we choose to regard the interchangeability of quantifiers (e.g., in many cases "most" entails "many") as a question of lexical semantics." |
| Q154 | 17 | task_taxonomy | "An important component of understanding the meaning of a sentence is understanding how its parts are composed together into a whole. In this category, we address issues across that spectrum, from syntactic ambiguity to semantic roles and coreference." |
| Q155 | 17 | task_taxonomy | "Syntactic Ambiguity: Relative Clauses, Coordination Scope These two categories deal purely with resolving syntactic ambiguity. Relative clauses and coordination scope are both sources of a great amount of ambiguity in English." |
| Q156 | 17 | task_taxonomy | "Prepositional phrase attachment is a particularly difficult problem that syntactic parsers in NLP systems continue to struggle with. We view it as a problem both of syntax and semantics, since prepositional phrases can express a wide variety of semantic roles and often semantically apply beyond their direct syntactic attachment." |
| Q157 | 17 | task_taxonomy | "Core Arguments Verbs select for particular arguments, particularly subjects and objects, which might be interchangeable depending on the context or the surface form. One example is the ergative alternation: "Jake broke the vase" entails "the vase broke" but "Jake broke the vase" does not entail "Jake broke". Other rearrangements of core arguments, such as those seen in Symmetry/Collectivity, also fall under the Core Arguments label." |
| Q158 | 17 | task_taxonomy | "Alternations: Active/Passive, Genitives/Partitives, Nominalization, Datives All four of these categories correspond to syntactic alternations that are known to follow specific patterns in English: Active/Passive: "I saw him" is equivalent to "He was seen by me" and entails "He was seen". Genitives/Partitives: "the elephant's foot" is the same thing as "the foot of the elephant". Nominalization: "I caused him to submit his resignation" entails "I caused the submission of his resignation". Datives: "I baked him a cake" entails "I baked a cake for him" and "I baked a cake" but not "I baked him"." |
| Q159 | 17 | task_taxonomy | "Ellipsis/Implicits Often, the argument of a verb or other predicate is omitted (elided) in the text, with the reader filling in the gap. We can construct entailment examples by explicitly filling in the gap with the correct or incorrect referents. For example, the premise "Putin is so entrenched within Russias ruling system that many of its members can imagine no other leader" entails "Putin is so entrenched within Russias ruling system that many of its members can imagine no other leader than Putin" and contradicts "Putin is so entrenched within Russias ruling system that many of its members can imagine no other leader than themselves."" |
| Q160 | 17 | task_taxonomy | "This is often regarded as a special case of anaphora, but we decided to split out these cases from explicit anaphora, which is often also regarded as a case of coreference (and attempted to some degree in modern coreference resolution systems)." |
| Q161 | 18 | task_taxonomy | "Coreference refers to when multiple expressions refer to the same entity or event." |
| Q162 | 18 | task_taxonomy | "It is closely related to Anaphora, where the meaning of an expression depends on another (antecedent) expression in context." |
| Q163 | 18 | task_taxonomy | "These two phenomena have significant overlap; for example, pronouns ("she", "we", "it") are anaphors that are co-referent with their antecedents." |
| Q164 | 18 | task_taxonomy | "In this category we only include cases where there is an explicit phrase (anaphoric or not) that is co-referent with an antecedent or other phrase." |
| Q165 | 18 | data_sources | "We construct examples for these in much the same way as for Ellipsis/Implicits." |
| Q166 | 18 | task_taxonomy | "Many modifiers, especially adjectives, allow non-intersective uses, which affect their entailment behavior." |
| Q167 | 18 | task_taxonomy | "Generally, an intersective use of a modifier, like "old" in "old men", is one which may be interpreted as referring to the set of entities with both properties (they are old and they are men)." |
| Q168 | 18 | task_taxonomy | "Intersectivity is related to Factivity." |
| Q169 | 18 | task_taxonomy | "However, we choose to categorize intersectivity under predicate-argument structure rather than lexical semantics, because generally the same word will admit both intersective and non-intersective uses, so it may be regarded as an ambiguity of argument structure." |
| Q170 | 18 | task_taxonomy | "Restrictivity is most often used to refer to a property of uses of noun modifiers." |
| Q171 | 18 | task_taxonomy | "In particular, a restrictive use of a modifier is one that serves to identify the entity or entities being described, whereas a non-restrictive use adds extra details to the identified entity." |
| Q172 | 18 | task_taxonomy | "Modifiers that are commonly used non-restrictively are appositives, relative clauses starting with "which" or "who", and expletives (e.g. "pesky")." |
| Q173 | 18 | task_taxonomy | "With an understanding of the structure of a sentence, there is often a baseline set of shallow conclusions that can be drawn using logical operators and often modeled using the mathematical tools of logic." |
| Q174 | 18 | task_taxonomy | "All of the basic operations of propositional logic appear in natural language, and we tag them where they are relevant to our examples:" |
| Q175 | 19 | task_taxonomy | "Conjunction: "Temperature and snow consistency must be just right" entails "Temperature must be just right"." |
| Q176 | 19 | task_taxonomy | "Disjunction: "Life is either a daring adventure or nothing at all" does not entail, but is entailed by, "Life is a daring adventure"." |
| Q177 | 19 | task_taxonomy | "Conditionals: "If both apply, they are essentially impossible" does not entail "They are essentially impossible"." |
| Q178 | 19 | task_taxonomy | "Conditionals are more complicated because their use in language does not always mirror their meaning in logic." |
| Q179 | 19 | task_taxonomy | "For example, they may be used at a higher level than the at-issue assertion: "If you think about it, it's the perfect reverse psychology tactic" entails "It's the perfect reverse psychology tactic"." |
| Q180 | 19 | task_taxonomy | "Quantifiers are often triggered by words such as "all", "some", "many", and "no"." |
| Q181 | 19 | task_taxonomy | "Universal: "All parakeets have two wings" entails, but is not entailed by, "My parakeet has two wings"." |
| Q182 | 19 | task_taxonomy | "Existential: "Some parakeets have two wings" does not entail, but is entailed by, "My parakeet has two wings"." |
| Q183 | 19 | task_taxonomy | "Monotonicity is a property of argument positions in certain logical systems." |
| Q184 | 19 | task_taxonomy | "In general, it gives a way of deriving entailment relations between expressions that differ on only one subexpression." |
| Q185 | 19 | task_taxonomy | ""a" is upward monotone in its restrictor: an entailment in the restrictor yields an entailment of the whole statement." |
| Q186 | 19 | task_taxonomy | ""no" is downward monotone in its restrictor: an entailment in the restrictor yields an entailment of the whole statement in the opposite direction." |
| Q187 | 19 | task_taxonomy | ""exactly one" is non-monotone in its restrictor: entailments in the restrictor do not yield entailments of the whole statement." |
| Q188 | 19 | task_taxonomy | "In this way, entailments between sentences that are built off of entailments of sub-phrases almost always rely on monotonicity judgments; see, for example, Lexical Entailment." |
| Q189 | 19 | task_taxonomy | "However, because this is such a general class of sentence pairs, to keep the Logic category meaningful we do not always tag these examples with monotonicity." |
| Q190 | 19 | task_taxonomy | "Some higher-level facets of reasoning have been traditionally modeled using logic, such as actual mathematical reasoning (entailments based off of numbers) and temporal reasoning (which is often modeled as reasoning about a mathematical timeline)." |
| Q191 | 19 | task_taxonomy | "Intervals/Numbers: "I have had more than 2 drinks tonight" entails "I have had more than 1 drink tonight"." |
| Q192 | 19 | task_taxonomy | "Temporal: "Mary left before John entered" entails "John entered after Mary left"." |
| Q193 | 20 | task_taxonomy | "Strictly speaking, world knowledge and common sense are required on every level of language understanding for disambiguating word senses, syntactic structures, anaphora, and more." |
| Q194 | 20 | task_taxonomy | "However, in these categories, we gather examples where the entailment rests not only on correct disambiguation of the sentences, but also application of extra knowledge, whether concrete knowledge about world affairs or more common-sense knowledge about word meanings or social or physical dynamics." |
| Q195 | 20 | task_taxonomy | "World Knowledge In this category we focus on knowledge that can clearly be expressed as facts, as well as broader and less common geographical, legal, political, technical, or cultural knowledge." |
| Q196 | 20 | task_taxonomy | "Common Sense In this category we focus on knowledge that is more difficult to express as facts and that we expect to be possessed by most people independent of cultural or educational background." |
| Q197 | 20 | task_taxonomy | "This includes a basic understanding of physical and social dynamics as well as lexical meaning (beyond simple lexical entailment or logical relations)." |

### Category Index
- **task_taxonomy**: Q3, Q8, Q9, Q15, Q16, Q17, Q18, Q19, Q27, Q32, Q37, Q43, Q64, Q97, Q101, Q102, Q105, Q111, Q116, Q122, Q129, Q134, Q135, Q136, Q137, Q142, Q143, Q144, Q145, Q146, Q147, Q149, Q150, Q151, Q152, Q153, Q154, Q155, Q156, Q157, Q158, Q159, Q160, Q161, Q162, Q163, Q164, Q166, Q167, Q168, Q169, Q170, Q171, Q172, Q173, Q174, Q175, Q176, Q177, Q178, Q179, Q180, Q181, Q182, Q183, Q184, Q185, Q186, Q187, Q188, Q189, Q190, Q191, Q192, Q193, Q194, Q195, Q196, Q197
- **data_sources**: Q5, Q6, Q7, Q21, Q24, Q26, Q29, Q31, Q35, Q36, Q38, Q39, Q40, Q41, Q46, Q47, Q48, Q50, Q51, Q53, Q61, Q63, Q119, Q121, Q132, Q133, Q165
- **data_format**: Q4, Q42, Q45, Q49, Q52, Q54, Q62, Q91, Q92, Q93, Q95, Q98, Q103, Q104, Q120, Q123, Q124, Q125, Q127, Q128, Q130
- **label_categories**: Q12, Q22, Q28, Q56, Q69, Q141, Q148
- **annotation_process**: Q65, Q66, Q67, Q68, Q73, Q74
- **evaluation_metrics**: Q10, Q20, Q23, Q25, Q30, Q33, Q57, Q58, Q59, Q60, Q70, Q71, Q72, Q75, Q80, Q81, Q82, Q83, Q84, Q85, Q86, Q87, Q88, Q89, Q90, Q94, Q99, Q100, Q109, Q110, Q113, Q126, Q140
- **stated_limitations**: Q11, Q13, Q14, Q34, Q44, Q55, Q76, Q77, Q78, Q96, Q106, Q107, Q108, Q112, Q114, Q115, Q131, Q138, Q139
- **authors_affiliations**: Q1, Q2, Q79, Q117, Q118
