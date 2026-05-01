I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding** is valid for use in **Luxembourgish Public Administration Civil Servants — GLUE Assessment**.

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

- **Name**: glue
- **Full Name**: GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding
- **Domain**: General natural language understanding (English multi-task)
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2019

### Benchmark Documentation

## Key characteristics relevant to validity analysis

### 1. Input Ontology
GLUE is organized around nine English sentence-understanding tasks spanning a broad range
of domains, data quantities, and difficulties [Q18], including question answering, sentiment
analysis, and textual entailment [Q3]. The benchmark is explicitly model-agnostic, requiring
only that a model process single-sentence and sentence-pair inputs [Q4]. The stated goal is
to spur development of generalizable NLU systems that share knowledge across tasks [Q19].
Beyond the nine main tasks, a diagnostic dataset probes four broad categories — Lexical
Semantics, Predicate-Argument Structure, Logic, and Knowledge [Q135] — each subdivided into
fine-grained subcategories [Q136] including lexical entailment [Q143], factivity [Q148],
quantifiers [Q153], monotonicity [Q183], coreference [Q161], conditionals [Q177], temporal
reasoning [Q192], world knowledge [Q195], and common sense [Q196]. These categories are
described as "not based on any particular linguistic theory, but broadly based on issues
that linguists have often identified and modeled in the study of syntax and semantics" [Q137].
The diagnostic set is explicitly provided as an analysis tool rather than a benchmark [Q138].

The task ontology contains no administrative domain categories, no intent detection for
government routing, no cross-border worker classification, and no national-vs.-municipal
competency distinction. The "World Knowledge" subcategory [Q195] and "Common Sense"
category [Q196] are framed around general English-language reasoning with no jurisdictional
specificity. Multi-task structure [Q101, Q102] assumes a shared English NLU space with no
structural analogue in a trilingual Luxembourgish government context.

### 2. Input Content
None of the GLUE datasets were created from scratch; the authors explicitly rely on
pre-existing datasets "implicitly agreed upon by the NLP community as challenging and
interesting" [Q6]. Component sources include: CoLA (linguistic acceptability judgments
from linguistics books and journal articles) [Q21]; SST-2 (sentences from English movie
reviews) [Q26]; MRPC (sentence pairs automatically extracted from online news sources)
[Q29]; QQP (question pairs from the Quora community Q&A website) [Q31]; STS-B (sentence
pairs from news headlines, video/image captions, and NLI data) [Q35]; MNLI (crowdsourced
sentence pairs from ten sources including transcribed speech, fiction, and government
reports) [Q36, Q38]; SQuAD (question-paragraph pairs from Wikipedia) [Q41]; RTE (sentence
pairs from annual entailment challenges based on news and Wikipedia) [Q46, Q47, Q48]; and
Winograd (manually constructed reading comprehension examples) [Q50, Q51]. The diagnostic
set draws on naturally occurring sentences from news, Reddit, Wikipedia, and academic
papers [Q63].

All data sources are English-language, drawing on American and British news, web forums,
Wikipedia, academic linguistics journals, and movie reviews. No source involves multilingual,
code-switched, or low-resource language content. The benchmark's instances share neither
script norms, language, nor domain with the Luxembourgish administrative correspondence
context. Four datasets use privately held test data [Q7], and auxiliary SNLI data is
recommended for MNLI training [Q40].

### 3. Input Form
GLUE imposes minimal architectural constraints, requiring only that a model process
single-sentence and sentence-pair inputs [Q4]. The diagnostic examples are formatted as
NLI sentence pairs tagged for demonstrated linguistic phenomena [Q62]. Several datasets
were reformatted for compatibility: SQuAD was recast into sentence-pair classification via
lexical-overlap filtering [Q42]; the RTE datasets were converted to a two-class split by
collapsing neutral and contradiction into "not entailment" [Q49]; and Winograd was converted
by replacing ambiguous pronouns with each possible referent [Q52]. The WNLI test set has an
imbalanced class distribution [Q54]. Multi-task models share a BiLSTM encoder across tasks
with task-specific classifiers [Q91], sampling tasks proportionally to training set size [Q92].
ELMo embeddings show consistent improvements particularly for single-sentence tasks [Q103].

All inputs are standardized written English text. There is no accommodation for
non-standardized orthography, code-switching, low-resource languages, or trilingual
input mixing of the kind present in Luxembourgish citizen correspondence. The
preprocessing transformations (e.g., recasting SQuAD [Q42], converting Winograd [Q52])
are English-specific and provide no transferable methodology for non-standard input signals.

### 4. Output Ontology
All tasks are single-sentence or sentence-pair classification except STS-B, which is a
regression task; MNLI has three classes (entailment, neutral, contradiction [Q56]) and
all other classification tasks have two [Q12]. Specific label spaces include
grammatical/ungrammatical for CoLA [Q22], positive/negative sentiment for SST-2 [Q28],
and entailment/not-entailment for RTE and WNLI. The diagnostic set label distribution is
42% entailment, 35% neutral, and 23% contradiction [Q69], with some examples tagged across
multiple phenomena categories [Q141]. The "Factivity" label groups examples involving
factive and implicative predicates [Q148].

The output label ontology represents a fundamental mismatch with the deployment's
requirements. The deployment requires multi-label classification (a single citizen message
may concern multiple departments) combined with confidence scoring to flag uncertain cases
for human review — structures entirely absent from GLUE's hard single-label paradigm [Q12].
GLUE's sentiment labels (positive/negative [Q28]) were designed for English movie reviews
and are not calibrated for the formal, understated register of Luxembourgish administrative
correspondence. Administrative routing categories — national vs. municipal competency,
cross-border worker issues, housing urgency flags — have no representation in GLUE's
label set.

### 5. Output Content
The diagnostic dataset was constructed by NLP researchers who identified target phenomena,
located naturally occurring sentences, and edited them minimally to produce sentence pairs
with high lexical and structural overlap [Q65, Q66]. Each pair was labeled bidirectionally
to yield 1,100 total examples [Q67], with multiple pairs per source sentence to create
minimal contrastive sets [Q68]. Human baseline performance was established by having six
NLP researchers annotate 50 randomly sampled sentence pairs [Q73], yielding high
inter-annotator agreement with Fleiss's κ = 0.73 [Q74].

Annotator demographics are NOT DOCUMENTED for the main benchmark tasks: the paper does not
describe the demographic composition of MNLI crowdsourced annotators [Q36] or SST-2
sentiment annotators [Q26], nor does it report inter-annotator agreement for those inherited
datasets [Q6]. The diagnostic set's annotators are explicitly NLP researchers [Q73] — a
specialized, English-speaking population with no described connection to Luxembourgish
administrative culture or continental European formal correspondence register. Ground-truth
sentiment labels reflect movie-review annotator judgments; ground-truth entailment labels
reflect crowdsourced English-speaking workers. Neither population is calibrated for the
target deployment's communicative norms.

### 6. Output Form
GLUE follows the SemEval/Kaggle submission model: systems run on provided test data and
upload predictions to gluebenchmark.com for scoring [Q57, Q58], with per-task scores and
a macro-average displayed on a public leaderboard [Q59]. Tasks are generally evaluated on
accuracy with balanced classes [Q20]; exceptions include CoLA (Matthews Correlation
Coefficient [Q23]), MRPC and QQP (accuracy plus F1 [Q30, Q33]), STS-B (Pearson and
Spearman correlation [Q35]), and the diagnostic set (R3, a three-class MCC generalization
[Q70]). For tasks with multiple metrics, an unweighted average is used as the task score
in the overall macro-average [Q60]. The website limits submissions to two per day to
prevent overfitting to private test data [Q131]. Human annotators achieve an average R3
of 0.80 on the diagnostic set [Q75], while all model scores remain low [Q110].

GLUE evaluates text-based outputs only using hard single-label prediction scoring. This
paradigm does not accommodate the confidence-scored, multi-label routing logic the
Luxembourgish deployment requires. The macro-average aggregation [Q59, Q60] rewards
balanced performance across nine English NLU tasks that are irrelevant to the deployment
scenario, making the overall GLUE score an uninformative proxy for Luxembourgish
administrative routing quality. The submission-based, privately-held test data model
[Q7, Q58] also prevents the iterative, task-specific calibration a live civil service
deployment would require.


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

## Regional Context

```yaml
name: Luxembourgish Public Administration Civil Servants — GLUE Assessment
abbreviation: lu-pubadmin-glue
deployment_context:
  description: Civil servants in Luxembourgish national and municipal government agencies
    who process digital citizen correspondence using an LLM-assisted routing and prioritization
    system. The system performs topic classification, named entity recognition, intent
    detection, and sentiment analysis to route messages to appropriate departments
    and flag urgent or frustrated submissions. The benchmark under evaluation is GLUE
    (2019), an English-only, US-context multi-task NLU benchmark.
  system_function: Automated routing of citizen correspondence to national or municipal
    departments, with urgency and frustration flagging; uncertain cases escalated
    to human review via confidence scoring.
  country: Luxembourg
  administrative_level: Both national (État) and communal (commune/Gemeng) — routing
    between these two tiers is a core system requirement.
target_population:
  primary_users: Civil servants in Luxembourgish government agencies responsible for
    reviewing, validating, and acting on automatically routed citizen correspondence.
  role_in_system: 'Human-in-the-loop reviewers who audit model output, correct erroneous
    urgency or frustration flags, and provide feedback that calibrates the routing
    logic over time. Not passive end-users: they exercise corrective authority over
    model decisions.'
  workforce_size: 'Approximately 35,000 government workers employed in the civil service
    across all levels (Source: justarrived.lu labour market data — [WEB-1]).
    This figure covers the État and communal levels combined, but a precise breakdown
    between national and communal administrations was not found in publicly available
    sources.'
  institutional_context: 'Luxembourg''s civil service is divided between État-level
    ministries/agencies and 100 communes (as of 1 September 2023, following mergers
    reducing from 102; see administrative_structure below). Citizen correspondence
    arrives via digital channels including MyGuichet.lu operated by CTIE (Centre des
    technologies de l''information de l''État), which is directly subordinated to
    the Ministry for Digitalisation (Source: European Language Equality report on
    Luxembourgish — [WEB-2]).'
  language_competencies: 'Civil servants typically have working proficiency in Luxembourgish,
    French, and German; many also speak English. Knowledge of all three official state
    languages is a formal requirement for most civil service positions (Source: justarrived.lu
    — [WEB-1]).
    Correspondence processed may arrive in any of these languages or in code-switched
    combinations.'
input_population:
  description: Citizens and residents writing to Luxembourgish government agencies.
    This population is linguistically highly diverse, reflecting Luxembourg's unusual
    demographic profile.
  citizen_demographics:
    total_population: '672,050 as of 1 January 2024, growing by 11,241 (+1.7%) from
      2023 (Source: STATEC Luxembourg Demography in Figures 2024 — [WEB-3];
      confirmed by luxembourg.public.lu — [WEB-4]).'
    nationality_composition: '52.7% Luxembourg nationals, 47.3% foreign nationals
      as of 1 January 2024. Among foreign nationals: Portuguese ~14.5% of total population
      (largest foreign group), French ~7.6%, Italian ~3.7%, Belgian ~3%, German ~2%,
      Spanish ~1.3%, Romanian ~1%, other ~14%. Over 170 nationalities recorded (Sources:
      luxembourg.public.lu — [WEB-4];
      migrationpolicy.org citing 2022 est. — [WEB-5]).'
    cross_border_workers_frontaliers:
      description: Workers who live in France, Belgium, or Germany and commute daily
        into Luxembourg. They constitute a legally distinct category from residents
        and generate a significant share of administrative correspondence, particularly
        on tax, social security, and employment matters.
      share_of_workforce: '47% of Luxembourg''s total workforce as of 2024, representing
        approximately 231,290 frontaliers out of ~489,000 total employees (Source:
        STATEC Regards 01/25 — [WEB-6];
        corroborated by OECD Economic Surveys Luxembourg 2025 — [WEB-7]).'
      primary_origin_countries: 'France (dominant, ~54% of all frontaliers, approximately
        124,160 in 2024), Belgium (~23%), Germany (~23%). In absolute terms: ~124,000
        from France, ~50,000+ from Belgium, ~50,000 from Germany (Sources: STATEC/IGSS
        2025 data cited by leretourdelautruche.com — [WEB-8];
        OGBL 2021 figures — [WEB-9]).'
      languages_likely_used_in_correspondence: French (dominant for French and Belgian
        frontaliers), German (for German frontaliers), possibly Luxembourgish
  input_languages:
    official_administrative_languages:
    - Luxembourgish (Lëtzebuergesch)
    - French
    - German
    de_facto_correspondence_mix: Messages arrive in all three official languages,
      often within a single message (code-switching). English-language correspondence
      from international residents also possible.
    note: Luxembourg has a formal trilingualism enshrined in law. French dominates
      administrative and legal writing; German appears in many official documents;
      Luxembourgish is the national language used in informal and increasingly in
      formal contexts. A single citizen message may mix all three.
languages:
  primary_target_language: Luxembourgish (Lëtzebuergesch)
  iso_codes:
    Luxembourgish: lb / ltz
    French: fr
    German: de
  resource_status:
    Luxembourgish: 'Low-resource. Limited NLP tooling, corpora, and benchmarks. Non-standardized
      orthography in everyday and even formal written use. Approximately 400,000 speakers
      (Source: ltzGLUE paper, arXiv 2604.17976 — [WEB-10]).'
    French: High-resource. Extensive NLP tooling available, but French used in Luxembourg
      administrative contexts may differ from metropolitan French in vocabulary and
      style.
    German: High-resource. Standard German NLP tooling available, though dialect influence
      from Moselle Franconian may appear.
  code_switching_profile: 'Luxembourgish-French-German trilingual code-switching is
    the defining input characteristic. Even formally intended correspondence exhibits
    alternation between French- and German-derived lexical variants for the same concept
    (e.g., ''Administratioun'' vs. ''Verwaltung''). Code-switching occurs at lexical,
    phrasal, and sentence level. The LuxBorrow corpus (University of Luxembourg /
    RTL, 1999–2025) documents token-level language identification and borrowing/code-switching
    labels across LU/DE/FR/EN in Luxembourgish news, providing methodological evidence
    of the scale of contact-linguistic phenomena (Source: LuxBorrow paper, arXiv 2603.10789
    — [WEB-11]).'
  orthographic_standardization:
    Luxembourgish: 'No universally enforced spelling standard in practice. The Lëtzebuerger
      Online Dictionnaire (LOD) and the Zentrum fir d''Lëtzebuerger Sprooch (ZLS)
      provide reference norms, but citizen correspondence will deviate significantly.
      The orthographic reform coincided with the COVID-19 period (2020); corpus data
      written in standard orthography remain scarce because most of the population
      lacks formal orthography training given limited grammar teaching in schools
      until recently (Source: Neural Text Normalization for Luxembourgish, arXiv 2412.09383
      — [WEB-12]).'
    French: Standard spelling expected; occasional influence from Belgian or Luxembourg-specific
      administrative vocabulary.
    German: Standard spelling expected.
  nlp_tooling_availability:
    Luxembourgish: 'Emerging ecosystem. Key resources include: (1) LuxemBERT (2022)
      — a BERT model for Luxembourgish trained with data augmentation from a related
      language, outperforming mBERT on six NLP tasks (Source: LuxemBERT, ACL Anthology
      LREC 2022 — [WEB-13]); (2) spaCy has
      been trained for Luxembourgish (Source: ELE Language Report — [WEB-2]);
      (3) LuNa open toolbox (University of Luxembourg) providing tokenization, POS
      tagging, morphological analysis and a ~20M token corpus including ~10M tokens
      of transcribed parliamentary speeches and ~5M from RTL news (Source: LuNa paper
      — [WEB-14]); (4) spellux
      — Python package for automatic Luxembourgish text normalization (Source: GitHub
      questoph/spellux — [WEB-15]); (5) ltz-E1-mini
      (68M) and ltz-E1-base (110M) encoder language models trained for Luxembourgish
      and evaluated on ltzGLUE (Source: ltzGLUE paper — [WEB-10]).'
    French: Extensive tooling available (spaCy, CamemBERT, etc.)
    German: Extensive tooling available (spaCy, German BERT variants, etc.)
    multilingual_code_switching: 'No dedicated benchmark or tooling for lb/fr/de code-switched
      input was found. The LuxBorrow corpus (2025) contributes token-level LID and
      borrowing/code-switching labels for Luxembourgish news text (LU/DE/FR/EN), which
      is the closest available resource, but it covers professionally edited news
      rather than citizen correspondence and is not an evaluation benchmark (Source:
      LuxBorrow arXiv 2603.10789 — [WEB-11]). No dedicated
      lb/fr/de code-switching NLU benchmark exists as of May 2025.'
writing_systems:
  scripts:
  - Latin alphabet with diacritics for all three languages
  luxembourgish_specific: 'Luxembourgish uses standard Latin characters with some
    diacritic usage (e.g., é in loanwords). The absence of a widely enforced orthographic
    standard means the same word may appear in multiple spellings within a corpus.
    The spellux normalization package documents ''large amount of orthographic variation''
    and ''resulting homograph density'' as ongoing challenges; the best neural normalization
    model (ByT5 base) achieves only ~78.8% accuracy on real-life variation data (Source:
    Neural Text Normalization paper arXiv 2412.09383 — [WEB-12];
    spellux GitHub — [WEB-15]).'
  note: No script mismatch concerns across the three languages. However, non-standardized
    Luxembourgish spelling introduces significant tokenization and normalization challenges
    that differ from both French and German NLP pipelines.
administrative_structure:
  national_level:
    description: État (national government) ministries and agencies covering competencies
      such as immigration, social security, taxation, and EU affairs.
    relevant_ministries: '[NEEDS VERIFICATION — deferred: below search budget; no
      authoritative ranking by correspondence volume found in public sources. Known
      high-volume domains include taxation/STATEC, labour/ADEM, immigration/OLAI,
      and interior/Ministère de l''Intérieur, but volume data require CTIE or ministerial
      access.]'
    digital_platforms: 'MyGuichet.lu is the principal eGovernment platform, operated
      by CTIE (Centre des technologies de l''information de l''État), which is directly
      subordinated to the Ministry for Digitalisation and responsible for setting
      up and developing eGovernment (Source: ELE Language Report on Luxembourgish,
      2022 — [WEB-2]).
      Exact correspondence volume figures are not publicly available and would require
      direct CTIE access.'
  communal_level:
    description: 100 communes (as of 1 September 2023, following mergers of Grosbous+Wahl
      and Bous+Waldbredimus) with competencies over local planning, communal services,
      civil registration, and local taxation.
    number_of_communes: '100 communes as of 1 September 2023, reduced from 102 following
      two mergers approved unanimously by the Chamber of Deputies on 8 February 2023
      — a historic low not seen since at least 1840 (Sources: Luxembourg Official
      Elections website — [WEB-16];
      Luxembourg Government communiqué — [WEB-17];
      Wikipedia Communes of Luxembourg — [WEB-18]).
      NOTE: The scaffold document stated 102; the current verified figure is 100.'
    routing_challenge: 'The system must distinguish whether a message concerns a national
      competency or a communal one, and if communal, which commune. This is a legally
      significant classification with no analogue in general NLU benchmarks. Communal
      competencies are defined by the 1868 Constitution (Chapter IX) and the 1988
      Loi communale (amended 2013), which define communes as autonomous authorities
      managing their own assets and interests (Source: SNG-WOFI Luxembourg country
      profile — [WEB-19]).'
  competency_boundary_complexity: 'National vs. communal competency boundaries are
    defined by Luxembourgish law and are not always transparent to citizens. A single
    message may implicate both levels. The governing statute is the Loi communale
    of 1988 (amended 2013), grounded in the 1868 Constitution Chapter IX on municipalities.
    The law grants communes autonomous powers over education, local roads, public
    health, social security, land-use planning, water/gas/electricity supply, and
    cultural funding, while national competencies cover immigration, taxation, pensions,
    and EU matters (Source: SNG-WOFI Luxembourg country profile — [WEB-19]).'
deployment_specific_categories:
  cross_border_worker_classification:
    description: Legally critical distinction between Luxembourg residents and frontaliers
      (cross-border workers residing in France, Belgium, or Germany). Different tax,
      social security, and administrative rules apply.
    nlp_challenge: The system must detect whether a message is from or about a frontalier
      vs. a resident, as this determines routing and applicable legal framework. No
      existing NLU benchmark contains this category.
    custom_annotation_required: true
    relevant_legal_framework: 'The primary bilateral fiscal frameworks are: the Convention
      fiscale franco-luxembourgeoise (signed 20 March 2018, with avenant of 7 November
      2022); comparable treaties with Belgium and Germany. Social security is governed
      by EU Regulation 883/2004 on social security coordination, implemented nationally
      by the CCSS (Centre commun de la sécurité sociale) and inspected by the IGSS
      (Inspection générale de la sécurité sociale). Remote-work rules for French frontaliers
      include a 34-day threshold for French tax jurisdiction, with employer declaration
      requirements introduced 2024 (Source: leretourdelautruche.com HR guide 2026
      citing STATEC/IGSS/CCSS official sources — [WEB-8]).'
  high_priority_topic_flags:
    housing_and_cost_of_living: Flagged as high political sensitivity in elicitation;
      housing queries should receive elevated urgency score.
    free_public_transit: 'CONFIRMED ACTIVE. Since 29 February 2020, all domestic public
      transport (buses, trains, trams) in Luxembourg is free for all users including
      tourists and frontaliers — Luxembourg was the first country in the world to
      implement nationwide zero-fare public transport. First-class rail seating remains
      paid. Cross-border sections of journeys still require payment. The policy is
      permanent and embedded in the National Mobility Plan 2035 (Source: luxembourg.public.lu
      official government page — [WEB-20];
      transports.public.lu FAQ — [WEB-21]).
      This remains a high-correspondence-volume topic given its novelty, cross-border
      commuter relevance, and ongoing expansion (e.g., pilot extension to French border
      municipalities, April 2024).'
    eu_institutional_matters: 'Luxembourg hosts major EU institutions (European Court
      of Justice since 1952, Court of Auditors, Eurostat, European Investment Bank,
      etc.); more than 14,500 international European civil servants are based in Luxembourg
      (Source: justarrived.lu — [WEB-1]).
      Correspondence relating to EU employment or procedures may require specialist
      routing. Volume and nature of EU-institution-related citizen correspondence
      to Luxembourg public administration (as distinct from EU institutional internal
      correspondence) is [NOT FOUND — this distinction requires CTIE or ministerial
      access; no public dataset found].'
  topic_taxonomy_requirements:
  - Cross-border worker / frontalier status
  - National vs. communal competency routing
  - Housing and rental market
  - Social security and pension
  - Taxation (resident vs. non-resident)
  - Immigration and residence permits
  - Public transport
  - Civil registration and identity documents
  - EU institutional employment matters
  - Local planning and construction permits
  - '[NEEDS VERIFICATION — deferred: confirm and expand based on actual correspondence
    volume data from CTIE or ministry statistics; not publicly available]'
cultural_norms_notes: '- Luxembourgish administrative culture is characterized by
  formal, understated written register; direct expressions of frustration or urgency
  are rare even when the underlying situation is acute.

  - Multilingual identity is central: citizens routinely switch between Luxembourgish,
  French, and German within a single correspondence without this signaling confusion
  or non-standard behavior.

  - Luxembourg''s high proportion of foreign residents (47.3% of population are non-Luxembourgish
  nationals as of 1 January 2024 — Source: STATEC / luxembourg.public.lu — [WEB-4])
  means many correspondents are not native Luxembourgish speakers and may write exclusively
  in French, German, Portuguese, or English.

  - Continental European formal correspondence conventions differ significantly from
  Anglophone norms: salutation and closing formulas are more elaborate; complaints
  are often framed indirectly.

  - Cross-border workers (frontaliers) may have limited familiarity with Luxembourgish
  administrative norms and may write in French or German with different register expectations.

  - Sub-national cultural variation: Luxembourg City and the Minett (southern/former
  industrial belt, with significant Portuguese and Italian heritage community) may
  exhibit different correspondence language patterns from the more rural Ardennes
  north or the Moselle wine region east. [NEEDS VERIFICATION — deferred: sociolinguistic
  studies of regional variation within Luxembourg require expert/stakeholder elicitation;
  not adequately documented in searchable web sources]'
sub_national_variation:
- region: Luxembourg City (Stad Lëtzebuerg)
  notes: 'Highly international population: 70.8% of Luxembourg City''s population
    are foreign nationals (Source: luxembourg.public.lu — [WEB-4]).
    Large share of EU institution employees (~14,500 European civil servants) and
    international finance sector workers. Correspondence likely to include more English
    and French, higher code-switching density. [NEEDS VERIFICATION — deferred: sub-national
    correspondence language distribution requires corpus data not publicly available]'
- region: Minett (Terres Rouges / southern Luxembourg)
  notes: 'Former industrial belt; significant Portuguese, Italian, and Cape Verdean
    heritage communities; historically Luxembourgish-speaking with heavy Romance influence.
    Portuguese community is the largest foreign group nationally (~14.5% of total
    population). May exhibit distinct lexical patterns in correspondence. [NEEDS VERIFICATION
    — deferred: requires sociolinguistic fieldwork; not adequately documented in searchable
    web sources]'
- region: Ardennes / Éislek (northern Luxembourg)
  notes: 'More rural, predominantly Luxembourgish-speaking; fewer international residents
    (communes of Wahl, Useldange, Reckange-sur-Mess, Goesdorf have the lowest proportion
    of foreigners — 20–22%; Source: luxembourg.public.lu — [WEB-4]);
    correspondence may be more monolingual Luxembourgish. [NEEDS VERIFICATION — deferred:
    regional correspondence language distribution not publicly documented]'
- region: Moselle / Grevenmacher (eastern Luxembourg)
  notes: 'Border region with Germany; German-language influence stronger; frontalier
    correspondence from German side expected (~50,000 German frontaliers). [NEEDS
    VERIFICATION — deferred: regional-level frontalier correspondence patterns require
    administrative data]'
- region: '[No additional administratively or linguistically salient sub-regions identified
    beyond the four above]'
  notes: '[NOT FOUND — searched available sociolinguistic and administrative sources;
    the four regions above cover the main documented variation axes. Additional granularity
    would require expert elicitation or access to CTIE/communal correspondence data.]'
infrastructure_notes:
  digital_infrastructure: '[NEEDS VERIFICATION — deferred: Luxembourg''s specific
    internet penetration and fixed/mobile broadband statistics for the assessment
    period were not retrieved within search budget. Luxembourg is consistently rated
    as one of Europe''s most advanced digital economies and scores highly on EU DESI
    indices, but exact current figures require ITU DataHub or Eurostat lookup.]'
  government_digital_platforms: 'MyGuichet.lu is operated by CTIE (Centre des technologies
    de l''information de l''État), directly subordinated to the Ministry for Digitalisation.
    CTIE strategic axes include developing eGovernment and integrating new technologies
    (Source: ELE Language Report — [WEB-2]).
    Annual digital correspondence volume processed via MyGuichet.lu is [NOT FOUND
    — not publicly reported; requires direct CTIE access].'
  model_deployment_environment: 'Cloud or on-premise within Luxembourg government
    IT infrastructure; data sovereignty requirements may apply under Luxembourg/EU
    law. GDPR applies as Luxembourg is an EU member state; the CNPD (Commission nationale
    pour la protection des données) is the national supervisory authority. [NEEDS
    VERIFICATION — deferred: specific data localization or sovereignty requirements
    for citizen correspondence data beyond GDPR baseline require legal expert review].'
  human_in_the_loop_mechanism: Civil servants can correct erroneous urgency/frustration
    flags; corrections feed back into routing calibration. This live feedback loop
    is confirmed by the elicitation as an active design feature.
regulatory_and_legal_context:
  data_protection: 'GDPR (Regulation (EU) 2016/679) applies directly as Luxembourg
    is an EU member state. The CNPD (Commission nationale pour la protection des données)
    serves as the national supervisory authority. Luxembourg-specific implementing
    legislation and any sector-specific provisions for public administration data
    processing would require legal expert review — not retrieved within search budget.
    [NEEDS VERIFICATION — deferred: Luxembourg-specific GDPR implementing acts beyond
    CNPD supervisory role]'
  ai_governance: 'The EU AI Act (Regulation (EU) 2024/1689) entered into force 1 August
    2024 and is fully applicable from 2 August 2026 (with high-risk AI rules for Annex
    III systems applying from August 2026; extended transition until August 2027 for
    AI embedded in regulated products). The citizen correspondence routing system
    likely falls under Annex III Category 5 (''Access to Essential Services'') or
    Category 8 (''Administration of Justice and Democratic Processes''), given its
    role in prioritizing access to public services — both categories are listed as
    high-risk. If the system performs any profiling of natural persons, it is always
    considered high-risk under Article 6(4). Providers who believe their system is
    not high-risk must document their assessment before placing it on the market (Sources:
    EU AI Act official text Annex III — [WEB-22];
    Article 6 — [WEB-23]; EC Digital Strategy
    page — [WEB-24]).
    Luxembourg government AI strategy or CNPD-specific guidance on AI in public sector
    was not retrieved within search budget.'
  administrative_law: '[NEEDS VERIFICATION — deferred: relevant provisions of Luxembourg
    administrative procedure law governing automated routing and prioritization of
    citizen correspondence; legal basis for automated processing; requires legal expert
    review of Luxembourgish administrative law sources not accessible in English-language
    web search]'
  language_law: 'The Loi du 24 février 1984 sur le régime des langues establishes
    Luxembourg''s formal trilingualism (Luxembourgish, French, German) in administrative
    and legal contexts. French is the sole language of legislation. Administrative
    correspondence may be received and answered in any of the three official languages.
    This has direct implications for the routing system: the model must correctly
    identify and process all three languages, and any language-specific routing or
    response obligations must be respected. [NEEDS VERIFICATION — deferred: specific
    obligations for the language of automated responses and their legal basis require
    expert review of the 1984 law and any subsequent amendments]'
  frontalier_legal_framework: 'Primary frameworks confirmed: Convention fiscale franco-luxembourgeoise
    (20 March 2018, amended by avenant 7 November 2022) for France; comparable bilateral
    treaties with Belgium and Germany. EU Regulation 883/2004 on social security coordination
    governs cross-border social security rights. The 34-day remote-work threshold
    for French frontaliers (with new employer declaration requirements since 2024)
    is a key source of administrative correspondence (Source: leretourdelautruche.com
    HR guide citing STATEC/IGSS/CCSS — [WEB-8]).
    Domestic implementing provisions require legal expert review.'
benchmark_mismatch_summary:
  benchmark: GLUE (2019)
  benchmark_language: English only
  benchmark_domain: General NLU — sentiment, paraphrase, textual entailment, QA; sourced
    from English news, movie reviews, Wikipedia, web forums
  deployment_language: Luxembourgish (low-resource, non-standardized orthography),
    French, German, trilingual code-switched input
  deployment_domain: Public administration citizen correspondence routing and prioritization
  critical_mismatches:
  - GLUE is English-only; deployment input is trilingual lb/fr/de code-switched text
    with non-standardized Luxembourgish orthography (IC, IF dimensions — HIGH priority).
  - GLUE task ontology (sentiment, paraphrase, entailment, QA) contains no administrative
    domain categories, no intent detection for government routing, and no cross-border
    worker or national/communal competency distinctions (IO dimension — HIGH priority).
  - GLUE uses hard single-label output; deployment requires multi-label classification
    with confidence scoring (OO, OF dimensions — HIGH/MODERATE priority).
  - GLUE sentiment labels (SST-2 from English movie reviews) not calibrated for Luxembourgish
    formal administrative register; annotator pool has no connection to Luxembourg
    administrative culture (OC dimension — HIGH priority).
  - No GLUE task covers NER, which is a stated deployment requirement.
  - GLUE's submission-based, privately-held test data model prevents the iterative
    calibration a live civil service deployment requires.
flagged_gaps_for_web_search:
- gap_id: 1
  topic: Luxembourgish NLU benchmarks and corpora
  search_target: NLU benchmarks for Luxembourgish (lb/ltz ISO code); University of
    Luxembourg NLP research; LIST (Luxembourg Institute of Science and Technology)
    language resources; ZLS (Zentrum fir d'Lëtzebuerger Sprooch) corpus materials;
    any government-sponsored Luxembourgish annotated corpora
- gap_id: 2
  topic: Trilingual code-switching evaluation resources
  search_target: Benchmarks or evaluation sets for lb/fr/de code-switched input; multilingual
    low-resource evaluation in Romance/Germanic contact zones; code-switching NLP
    tooling
- gap_id: 3
  topic: Luxembourg government digital correspondence datasets
  search_target: MyGuichet.lu NLP resources; CTIE annotated citizen correspondence
    datasets; Luxembourg digital transformation program NLP evaluation materials
- gap_id: 4
  topic: Cross-border worker (frontalier) NLP classification
  search_target: NLP or text classification resources for frontalier vs. resident
    status detection; Luxembourg administrative text annotation; legal status classification
    in administrative NLP
- gap_id: 5
  topic: Sentiment annotation for Luxembourgish administrative register
  search_target: Sentiment or tone datasets annotated by Luxembourgish civil servants
    or individuals familiar with formal European continental administrative register;
    Luxembourg-specific tone annotation resources
- gap_id: 6
  topic: National vs. communal competency taxonomy
  search_target: Luxembourg administrative competency classification resources; loi
    communale provisions; any NLP taxonomy covering État vs. commune routing in Luxembourg
- gap_id: 7
  topic: Sub-national linguistic variation within Luxembourg
  search_target: Sociolinguistic studies of regional linguistic variation within Luxembourg;
    Minett, Ardennes, Moselle dialect and code-switching patterns; corpus evidence
    of sub-regional correspondence language differences
- gap_id: 8
  topic: Luxembourgish orthographic normalization tools
  search_target: Computational tools for Luxembourgish spelling normalization; LOD
    (Lëtzebuerger Online Dictionnaire) API or NLP integration; lb-specific tokenizers
    or spell-checkers
- gap_id: 9
  topic: EU AI Act risk classification for this system
  search_target: EU AI Act Article 6 and Annex III applicability to automated public
    administration correspondence routing; Luxembourg CNPD guidance on AI in public
    sector; Luxembourg government AI strategy
- gap_id: 10
  topic: Multi-label intent classification benchmarks for government correspondence
  search_target: Multi-label intent classification evaluation sets for administrative
    or government domain; confidence-scored routing benchmarks; citizen correspondence
    NLU datasets in any language
net_new_fields:
  ltzGLUE_benchmark:
    name: 'ltzGLUE: Luxembourgish General Language Understanding Evaluation'
    arxiv_id: '2604.17976'
    url: '[WEB-10]'
    published: April 2025
    description: The first NLU benchmark for Luxembourgish (LTZ), explicitly modelled
      on GLUE. Covers eight tasks including named entity recognition (NER with BIO
      tags for LOC, PER, DATE, ORG, MISC), topic classification (sports/animals/business/culture/technology),
      slot-intent detection, sentiment analysis (positive/neutral/negative), linguistic
      acceptability (binary and multiclass), and recognizing textual entailment. Evaluates
      both encoder-based models (ltz-E1-mini at 68M params, ltz-E1-base at 110M params)
      and prompt-based LLMs. Includes a JudgeWEL NER dataset derived from Luxembourgish
      Wikipedia and Wikidata.
    relevance_to_assessment: 'ltzGLUE directly addresses the most critical gap identified
      in the benchmark_mismatch_summary: it provides a Luxembourgish-language NLU
      evaluation framework with NER and intent classification tasks that partially
      overlap the deployment''s requirements. However, ltzGLUE''s topic taxonomy (news
      categories) and intent detection (voice assistant commands) do not cover administrative
      domains, cross-border worker classification, or national/communal competency
      routing — so ltzGLUE is a better reference point than GLUE but still does not
      close the administrative domain gap (IO and IC dimensions). The benchmark''s
      existence confirms that Luxembourgish NLP has reached sufficient maturity to
      support evaluation, which is relevant to feasibility of custom benchmark construction.'
  luxembourgish_sentiment_corpus:
    name: RTL Corpus Sentiment Annotation Tool (STRIPS project, University of Luxembourg)
    url: '[WEB-25]'
    description: A sentiment annotation tool and corpus developed from RTL.lu news
      comments (2008–2018), providing sentence and comment-level sentiment labels
      in Luxembourgish. The LuNa toolbox integrates this resource for topic modelling
      and sentiment detection tasks.
    relevance_to_assessment: 'The only known Luxembourgish sentiment resource, but
      it is sourced from informal online news comments — a register very different
      from formal administrative correspondence. Annotation was done computationally
      with a Sentiment Engine, not by civil servants or administrative domain experts.
      This confirms the OC gap: no sentiment dataset calibrated to formal Luxembourgish
      administrative register exists.'
  luxembourgish_text_normalization:
    name: Neural Text Normalization for Luxembourgish (ByT5-based)
    arxiv_id: '2412.09383'
    url: '[WEB-12]'
    published: December 2024
    description: Paper demonstrating neural approaches to Luxembourgish orthographic
      normalization using real-life spelling variation data from the Spellchecker.lu
      tool. Best model (ByT5 base) achieves ~78.8% accuracy and ERR of 0.26. Identifies
      byte-based models as most suitable for Luxembourgish due to high orthographic
      variation and homograph density.
    relevance_to_assessment: 'Directly addresses the IF dimension gap: a preprocessing
      normalization step is likely required before any NLU model can reliably process
      citizen correspondence in Luxembourgish. The ~21% error rate of the best available
      normalizer means non-trivial noise will propagate to downstream NLU tasks, compounding
      the already-severe construct-irrelevant variance introduced by GLUE''s assumption
      of standardized English input.'
  lux_borrow_corpus:
    name: 'LuxBorrow: 27-Year RTL News Corpus with Code-Switching Annotation'
    arxiv_id: '2603.10789'
    url: '[WEB-11]'
    published: March 2025
    description: A large-scale longitudinal corpus of RTL.lu news articles (1999–2025,
      259,305 articles) annotated with token-level language identification (LU/DE/FR/EN)
      and explicit borrowing/code-switching labels. Documents trilingual contact-linguistic
      phenomena in professionally edited Luxembourgish across six socio-historical
      periods.
    relevance_to_assessment: Provides methodological and empirical evidence for the
      code-switching profile described in the region document. Confirms that lb/fr/de
      multilingual mixing is systematic in Luxembourgish text even in edited contexts.
      However, the corpus reflects editorial register rather than citizen correspondence,
      and models trained on it may 'inherit RTL-specific biases in topic coverage,
      register, and language choices' — limiting direct applicability to administrative
      NLU without domain adaptation.
  frontalier_share_confirmed:
    note: 'The elicitation-cited ~47% frontalier share of the workforce is confirmed
      by multiple STATEC sources for 2023–2024. OECD 2025 survey data now suggests
      the share has grown to approximately 50% of total employment when including
      the most recent count of ~515,000 workers at the beginning of 2024. French frontaliers
      remain dominant at ~50% of all frontaliers (Sources: STATEC Regards 01/25 —
      [WEB-6];
      OECD Economic Surveys Luxembourg 2025 — [WEB-7]).'
```

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

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Citizen feedback to Luxembourgish government agencies likely spans topics specific to local governance — such as cross-border worker issues, multilingual administrative procedures (French/German/Luxembourgish coexistence), housing, transport like the free public transit policy, or EU institutional matters. Does the benchmark's topic coverage address these Luxembourg-specific administrative domains, or does it focus on other areas not typical of local government correspondence?
A1: The deployment requires distinguishing cross-border workers from residents (a legally critical classification), flagging cost-of-living and housing queries as high-priority given current political sensitivity, and differentiating between national and municipal competencies to route messages correctly. None of these topic categories appear in GLUE's task suite, which covers sentiment, paraphrase, textual entailment, and general QA sourced from English-language news and web corpora.

Q2 [IC]: Citizen messages to public administration are often written in non-standard Luxembourgish — code-switching with French or German, informal orthography, or dialect forms. Does your deployment need to handle this kind of mixed or non-standardized language input, or can you assume messages are written in reasonably standard Luxembourgish prose?
A2: Even formally intended correspondence will exhibit significant orthographic variation in Luxembourgish, along with frequent alternation between French- and German-derived lexical variants for the same concept (e.g., "Administratioun" vs. "Verwaltung"). The model must be robust to this mixed-language, non-standardized input. A benchmark built on standardized news or legal English text is therefore not representative of actual input signal the deployed system will encounter.

Q3 [OC]: For sentiment and frustration detection specifically, were the benchmark's sentiment or tone labels validated by people familiar with Luxembourgish civil communication norms — for example, the typically understated or formal register citizens use when writing to government bodies — or were they produced by a broader, potentially non-Luxembourg-resident annotator pool?
A3: The user acknowledges that ground-truth sentiment labels ideally should be validated by annotators familiar with Luxembourg's administrative culture, but concedes that low-resource constraints may force reliance on out-of-domain labels initially. A human-in-the-loop audit mechanism is included so that civil servants can correct erroneous "urgent" or "frustrated" flags, allowing the routing logic to self-calibrate over time. This confirms that OC is a recognized live risk in the deployment.

Q4 [OO]: Your system triggers automated routing and prioritization decisions based on classified intent and sentiment — does the benchmark's assumption of a single hard label per message match your routing logic, or do you require multi-label or confidence-scored outputs?
A4: The routing logic requires multi-label classification, since a single message may concern multiple departments or topics simultaneously. Confidence scores are used to flag uncertain cases for human review rather than forcing a single top-label decision. GLUE's hard single-label scoring paradigm therefore does not match the output structure the deployment needs.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | GLUE's task ontology (paraphrase, entailment, general QA, English news sentiment) contains no categories for Luxembourg-specific administrative domains — cross-border worker status, national vs. municipal routing, housing urgency — identified as the core classification requirements. |
| IC | HIGH | Deployment input is Luxembourgish-French-German code-switched text with non-standardized orthography; GLUE instances are drawn from standardized English corpora with no overlap in script, language, or content type, introducing severe construct-irrelevant variance. |
| IF | HIGH | The target language is low-resource Luxembourgish with non-Latin-norm orthographic variation and frequent trilingual mixing; GLUE is English-only text, creating a fundamental input signal mismatch. |
| OO | HIGH | The deployment requires multi-label outputs with confidence scoring and combined intent-plus-sentiment categorization, while GLUE's scoring assumes single hard labels per task; the output taxonomy is also designed for a culturally unrelated English context. |
| OC | HIGH | Sentiment and urgency ground-truth labels in GLUE were not validated by annotators familiar with Luxembourgish administrative register; the user explicitly flagged this as a live risk, and the target population's understated formal tone norms are not represented in the annotator pool. |
| OF | MODERATE | Both deployment and benchmark use text-in / label-out pipelines, which partially aligns; however, GLUE's hard single-label output format conflicts with the deployment's need for confidence-scored and multi-label outputs, warranting moderate concern. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

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
  "benchmark": "glue",
  "region": "Luxembourgish Public Administration Civil Servants — GLUE Assessment",
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
