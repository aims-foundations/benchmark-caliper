I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **LTZGLUE: The First Natural Language Understanding Benchmark for Luxembourgish** is valid for use in **Luxembourg Public Administration — Civil Servant NLU Deployment**.

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

- **Name**: ltzglue
- **Full Name**: LTZGLUE: The First Natural Language Understanding Benchmark for Luxembourgish
- **Domain**: Low-resource NLU evaluation for Luxembourgish
- **Languages**: lb
- **Porting Strategy**: mixed
- **Year**: 2025

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
LTZGLUE assembles eight tasks spanning "binary and multi-class sentence and
token-level classification tasks," including NER, topic classification, and
intent classification [Q2, Q11]. The suite covers "four binary and four
multi-class settings, sentence- and document-level inputs, as well as a
token-level sequence-labelling task" [Q67], placing it in the same general
range as the nine-task original GLUE benchmark [Q68]. A substantial proportion
of tasks are "newly created for LTZ rather than direct translations or simple
repackaging" [Q69].

However, the topic classification taxonomy is drawn from RTL editorial
categories and covers only five classes — SPORTS, CULTURE, TECHNOLOGY,
BUSINESS, and ANIMALS [Q48, Q153] — none of which correspond to Luxembourg-
specific administrative domains such as cross-border worker status, housing,
communal vs. national competency routing, or EU institutional matters. The
intent detection task uses nine labels drawn entirely from a voice-assistant
corpus (alarm, reminder, weather sub-intents) [Q154], with no administrative
intent categories. The benchmark contains no multi-label task formulation
anywhere in its design [Q67], and the RTE task uses a logical entailment
framing [Q59] unrelated to administrative routing decisions. The authors
acknowledge that "no unified benchmark currently exists to evaluate LTZ
language understanding consistently" [Q14] and that the benchmark does not
claim complete coverage for any specific downstream deployment domain.

### Input Content
Textual data across most tasks originates from a narrow set of sources,
principally RTL news articles, with supplementary draws from the Luxembourgish
Online Dictionary (LOD), Wikipedia/Wikidata, and a translated English intent
dataset [Q12, Q16, Q24, Q30, Q34, Q46, Q51]. The NER corpus merges the
automatically constructed JUDGEWEL dataset (Wikipedia/Wikidata) [Q34, Q38]
with a human-annotated corpus from RTL online news comments [Q40]. The
intent detection dataset is a translated version of the English xSID
voice-assistant corpus, using a machine-translated German training set as
a proxy [Q51, Q54]. The construction was "deliberately resource-conscious"
[Q109], and the authors explicitly acknowledge that "LTZ is a small language
community, and linguistic data often originate from a limited set of public
domains" [Q119].

Critically, the authors themselves warn that "most data sources reflect formal
writing or institutional usage and therefore do not fully represent informal
and multilingual contexts" [Q112]. The intent detection source consists of
"user commands for a voice-controlled AI assistant, representing a specialised
spoken register for which there is no equivalent reference corpus in LTZ"
[Q55], and the lack of LTZ references in this register meant "it was not
possible to systematically verify the translated terminology" [Q56]. Code-
switched and orthographically variable Luxembourgish — confirmed as essential
for the deployment — is not documented as a feature of any task's input
datapoints beyond a partial representation in RTL user comments used for NER
[Q41].

### Input Form
All benchmark tasks are text-based, with Luxembourgish as the target language
throughout. The benchmark's register is predominantly formal and edited:
news articles, LOD dictionary examples, politically transcribed speeches, and
translated commands. Pre-training data for LTZ-E1 is broader, including RTL
user comments, webchat, and transcribed podcasts [Q74], but the downstream
task datasets are filtered to remove non-Luxembourgish text (via OpenLID) and
articles outside a 40–400 word length range [Q47]. The BPE tokenizer is
trained on the full pre-training set with vocabulary size 50,368 and a max
sequence length of 1,024 tokens [Q128, Q129]. For the linguistic acceptability
task, sentences come from the LOD and are synthetically manipulated [Q30, Q31].
There is no modality mismatch (deployment is text-only), but the formal,
standardized register of most input datapoints diverges from the colloquial,
orthographically variable, and code-switched inputs expected in real citizen
correspondence. The authors acknowledge this gap directly [Q112] but do not
document any effort to sample or augment task inputs to reflect non-standard
or multilingual writing.

### Output Ontology
The label ontologies across tasks are as follows: headline acceptability —
binary (True/False) [Q148, Q147]; sentiment analysis — three-class (positive,
neutral, negative) [Q149]; linguistic acceptability — binary (correct/incorrect)
or four-class (verb, adjective, syntax, orthographic error) [Q31, Q33]; NER —
BIO tags covering LOC, PER, DATE, ORG, MISC [Q152], with GPE merged into LOC
[Q44]; topic classification — five classes (SPORTS, CULTURE, TECHNOLOGY,
BUSINESS, ANIMALS) [Q48, Q153]; intent detection — nine voice-assistant
intent labels [Q154]; RTE — binary entailment (0/1) [Q155, Q147].

None of these label ontologies map to the administrative routing categories
required by the deployment. The topic classes contain no civic, housing,
transport, cross-border worker, or EU institutional category. The intent labels
are exclusively voice-assistant commands. The sentiment labels do not capture
urgency or frustration intensity. Crucially, all tasks produce a single hard
label per input [Q67], whereas the confirmed deployment logic requires multi-
label outputs with calibrated confidence scores for routing with human fallback
[elicitation Q4]. This represents a fundamental structural mismatch between
the benchmark's output ontology and the deployment's decision architecture.

### Output Content
Annotation practices vary substantially across tasks. Sentiment analysis
(4,583 sentences) was annotated by two native Luxembourgish speakers, with
a Cohen's Kappa of 0.45 [Q25, Q26, Q27, Q28] — moderate agreement — and
disagreements resolved by annotator consensus [Q28]. The human-annotated
NER dataset was "conducted manually, yielding a smaller but high-precision
dataset" [Q42]. The intent detection dataset was translated by a native LTZ
speaker with consultation of additional native speakers in uncertain cases
[Q52]. The JUDGEWEL NER corpus was constructed automatically using LLMs as
judges with "minimal human verification to calibrate quality thresholds" [Q37].
For RTE, ChatGPT-5-mini was used to filter low-quality translations [Q63]
and to verify label correctness, finding nearly 10% incorrect labels [Q64].

No information is provided about annotators' professional background, familiarity
with administrative communication norms, or whether any were drawn from civil-
service or public-administration domains. The Cohen's Kappa of 0.45 [Q27]
represents only moderate agreement, which is concerning when nuanced register
distinctions (formal frustration vs. neutral inquiry) are operationally
significant. The heavy reliance on LLM-assisted annotation for RTE and JUDGEWEL
[Q37, Q63, Q64] introduces uncertainty about whether ground-truth labels
reflect Luxembourgish civil communication norms or model-biased interpretations.
The authors themselves caution against "using benchmark performance as evidence
of cultural or demographic coverage" [Q121] and acknowledge that "models may
reproduce dominant norms while under-representing regional, sociolectal, or
multilingual practices" [Q120].

### Output Form
The primary evaluation metric across all tasks is macro-F1, with full validation
and test results reported per task [Q93, Q96, Q158, Q159]. Encoder-based model
results are averaged over three runs with standard deviations reported [Q89,
Q96]; prompted LLMs are evaluated once [Q96]. Invalid or malformed LLM outputs
are discarded prior to evaluation [Q90, Q91]. Class-balanced loss (beta=0.99)
is used during fine-tuning for imbalanced tasks [Q92]. Hyperparameter selection
uses Bayesian search with early stopping over validation performance, capped at
30 runs per model-task combination [Q136, Q137, Q138].

The benchmark's output format is exclusively single hard-label text classification
or sequence labeling, with F1 as the sole reported metric. This is a standard
and well-documented evaluation methodology for NLU tasks. However, the deployment
requires multi-label outputs with calibrated confidence scores for routing and
escalation logic; this functional requirement is not addressed anywhere in the
benchmark's evaluation design and represents a gap between LTZGLUE's output form
and operational deployment needs.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This paper presents LTZGLUE, the first Natural Language Understanding (NLU) benchmark for Luxembourgish (LTZ) based on the popular GLUE benchmark for English." |
| Q2 | 1 | input_ontology | "Our tasks include common natural language processing tasks in binary and multi-class classification settings, including named entity recognition, topic classification, and intent classification." |
| Q3 | 1 | output_form | "We evaluate various pre-trained language models for LTZ to present an overview of the current capabilities of these models on the LTZ language." |
| Q4 | 1 | input_ontology | "Small and under-researched languages are particularly difficult to evaluate, as is the case with Luxembourgish (LTZ), the national language of Luxembourg, with around 400k speakers." |
| Q5 | 1 | input_content | "LTZ only has a handful of NLU tasks available (Lothritz et al., 2022; Philippy et al., 2024; Plum et al., 2026)." |
| Q6 | 1 | input_content | "As most of these are in the news domain, and the majority of the down-stream tasks comprise less than a thousand instances, model evaluation is not always dependable." |
| Q7 | 1 | input_form | "Additional factors, such as the ongoing standardisation of the language (Gilles, 2019), vast amounts of variation (Lutgen et al., 2025), and decentralised resources, make it extremely challenging to evaluate LTZ language understanding in language models." |
| Q8 | 1 | input_ontology | "Our contributions are: (1) LTZGLUE: the first unified GLUE benchmark for LTZ, with 8 tasks." |
| Q9 | 1 | input_ontology | "(2) LTZ-E1 (mini/base): 2 new encoder language models for LTZ, which achieve competitive performance when fine-tuned on LTZGLUE." |
| Q10 | 1 | output_content | "Alistair Plum1, Felicia Körner2,3, Anne-Marie Lutgen1, Laura Bernardy1, Fred Philippy1, Emilia Milano1, Nils Rehlinger1, Cédric Lothritz4, Tharindu Ranasinghe5, Barbara Plank2,3, Christoph Purschke1 1University of Luxembourg, Luxembourg, 2LMU Munich, Germany 3Munich Center for Machine Learning, Germany 4LIST, Luxembourg, 5Lancaster University, UK" |
| Q11 | 2 | input_ontology | "In this section, we introduce the eight tasks for LTZGLUE. The set spans binary and multi-class sentence and token-level classification tasks. Together, these tasks cover a broad spectrum of linguistic and semantic phenomena and provide the first unified benchmark for evaluating LTZ NLP models." |
| Q12 | 2 | input_content | "Unless stated otherwise, the textual data used across most tasks stems from two main sources: (i)" |
| Q13 | 2 | input_content | "LTZ, the focus of this benchmark, is regarded as under-researched, and research is ongoing. Joshi et al. (2020) classify Luxembourgish as one of the "scraping-by" languages: although some unlabeled data exists, meaningful progress will require coordinated efforts to raise awareness and collect labeled datasets, as such resources are currently almost nonexistent." |
| Q14 | 2 | input_ontology | "Yet progress remains uneven across tasks, and existing resources vary widely in size, domain, and annotation quality. No unified benchmark currently exists to evaluate LTZ language understanding consistently, a gap we aim to fill." |
| Q15 | 3 | input_ontology | "We formulate headline acceptability (HA) as a binary classification task where the model must decide whether a given headline matches the accompanying article body." |
| Q16 | 3 | input_content | "To construct this dataset, we use RTL news articles. We keep only documents from the twenty most frequent categories. We then filter articles by body length and title length, remove exact duplicate titles, randomly shuffle the remaining instances, and retain a fixed subset of 30k examples." |
| Q17 | 3 | input_form | "This subset is split equally, with one half serving as the positive class with original headlines, and the other half providing the article bodies for which we assign swapped headlines." |
| Q18 | 3 | input_form | "We compute TF–IDF representations of the article texts using unigrams and bigrams, an LTZ stopword list, a minimum document frequency of two, and a large feature cap to preserve topical detail." |
| Q19 | 3 | input_form | "For every article body in the negative half, we search its nearest neighbours to identify a donor headline, with a minimum 30-day distance so that we avoid headlines tied to the same event." |
| Q20 | 3 | input_form | "To prevent trivial matches, we reject candidates whose headlines show high positional similarity, measured as the fraction of identical tokens in aligned positions (threshold 0.25)." |
| Q21 | 3 | input_form | "We store original and swapped titles, reshuffle, and split into train (20k), development (3k), and test (6k) sets." |
| Q22 | 3 | input_form | "The resulting negative examples remain topically related but are temporally and structurally mismatched, forcing models to attend to article content rather than surface cues." |
| Q23 | 3 | input_ontology | "We formulate the sentiment analysis (SA) task as a classification task where the model has to predict positive, negative, and neutral sentiment." |
| Q24 | 3 | input_content | "We use articles from RTL, randomly selected from the commentary and letter to the editor sections." |
| Q25 | 3 | output_content | "In total, we extract 4,583 sentences, which are then annotated by two native speakers of LTZ." |
| Q26 | 3 | output_content | "Annotators are instructed to label each sentence, and to use unsure only when they would otherwise randomly use the other labels." |
| Q27 | 3 | output_content | "We calculated Cohen's Kappa at 0.45." |
| Q28 | 3 | output_content | "For the final set, the annotators agree on a label in cases of label disagreement." |
| Q29 | 3 | input_ontology | "We introduce a linguistic acceptability dataset consisting of four distinct linguistic subtypes, which can either be used as a binary (LA (BINARY)) or multiclass (LA (MULTI)) classification dataset." |
| Q30 | 3 | input_content | "The sentences are derived from the Luxembourgish Online Dictionary (LOD) and are manipulated using the tags available in the dataset." |
| Q31 | 3 | output_ontology | "The first class interferes with the subject-verb agreement by changing the conjugated form of the main verb or auxiliary verb. The second class similarly modifies the declined form of the adjective and therefore violates the agreement in case, number, and gender. For the third class, we manipulate the syntax by deleting 2-3 random words from the sentence, depending on the length. The last class impacts the orthography, which is achieved by using data provided by Spellchecker.lu, a semiautomatic spellchecking website frequently used in Luxembourg. We changed one random word in the sentence by using the least frequent variant in the spellchecker data." |
| Q32 | 4 | input_form | "The multiclass dataset and binary dataset have a 70-10-20 split, and the distribution is shown in Table 2." |
| Q33 | 4 | output_ontology | "The binary dataset distinguishes between correct (1) and incorrect (0), for which the label 0 encompasses the categories Verb, Adj, Syntax and Ortho." |
| Q34 | 4 | input_content | "The JUDGEWEL dataset (Plum et al., 2026) introduces an automatically constructed corpus for named entity recognition (NER) in LTZ, derived from Wikipedia and Wikidata." |
| Q35 | 4 | input_form | "Using Wikipedia's hyperlink structure, entities are matched to their corresponding Wikidata types and labelled in BIO format." |
| Q36 | 4 | input_form | "Candidate sentences are selected to maximise diversity, and a set of quality heuristics filters incomplete or overlapping entities." |
| Q37 | 4 | output_content | "The resulting sentences are then evaluated using LLMs acting as judges, with minimal human verification to calibrate quality thresholds." |
| Q38 | 4 | input_content | "The final dataset contains roughly 27k sentences across five entity types (see Table 3)." |
| Q39 | 4 | output_content | "Models trained on JUDGEWEL achieve performance comparable to human-annotated data, demonstrating that automatically constructed resources can provide effective supervision." |
| Q40 | 4 | input_content | "The NER dataset introduced by Lothritz et al. (2022), by contrast, is a fully human-annotated corpus derived from RTL online news comments." |
| Q41 | 4 | input_content | "It covers a wider range of text types and registers, including informal and code-mixed writing, and focuses on four primary entity categories (PER, ORG, LOC, GPE)." |
| Q42 | 4 | output_content | "Annotation was conducted manually, yielding a smaller but high-precision dataset." |
| Q43 | 4 | input_form | "The two datasets are merged to increase both coverage and domain balance." |
| Q44 | 4 | output_ontology | "To ensure compatibility, the tag set is harmonised by merging the GPE and LOC categories into a single location label, while retaining PER, ORG, and MISC unchanged." |
| Q45 | 4 | input_content | "This unified resource thus aligns the structured reliability of JUDGEWEL with the domain and stylistic breadth of the NER set by (Lothritz et al., 2022), providing a large-scale, multi-domain NER dataset for LTZ." |
| Q46 | 4 | input_content | "To construct the news topic classification (TC) dataset, we collected news articles from RTL, which provides content pre-assigned to editorial categories." |
| Q47 | 4 | input_form | "We applied a series of preprocessing steps to ensure data quality. Specifically, we removed articles identified as non-Luxembourgish by OpenLID (Burchell et al., 2023), as well as those containing fewer than 40 words or more than 400 words." |
| Q48 | 4 | output_ontology | "From the available categories, we focused on five principal domains: SPORTS, CULTURE, TECHNOLOGY, BUSINESS, and ANIMALS." |
| Q49 | 4 | input_form | "Given the substantial over-representation of the SPORTS category, we performed downsampling to mitigate class imbalance." |
| Q50 | 4 | input_form | "The resulting dataset was split into training, development, and test sets (category distribution is summarized in Table 4)." |
| Q51 | 4 | input_content | "We constructed a new LTZ dataset for intent detection (ID) by translating the English xSID test and validation datasets (van der Goot et al., 2021)." |
| Q52 | 4 | output_content | "The translations were performed by an LTZ native speaker. In cases of uncertainty, additional native LTZ speakers were consulted." |
| Q53 | 4 | input_form | "Since LTZ is linguistically closely related to German, the German" |
| Q54 | 5 | input_content | "Since this task is originally intended to be crosslingual, we use the machine translated German training set (van der Goot et al., 2021)." |
| Q55 | 5 | input_content | "The main challenge in translating the English dataset stems from its register. The source segments consist of user commands for a voice-controlled AI assistant, representing a specialised spoken register for which there is no equivalent reference corpus in LTZ. This register is marked by domain-specific terminology and collocations (e.g., set an alarm, set a reminder, add to playlist), as well as non-standard spelling (e.g., all lowercase, missing punctuation)." |
| Q56 | 5 | input_content | "Due to the lack of LTZ references in this register, it was not possible to systematically verify the translated terminology." |
| Q57 | 5 | output_form | "After translating the dataset, we transferred the BIO tags by first using token-level fuzzy matching between the LTZ and the German dataset, followed by manual verification." |
| Q58 | 5 | output_ontology | "Table 5 shows the label distribution and size of each data split." |
| Q59 | 5 | input_ontology | "Recognizing Textual Entailment (RTE) (Haim et al., 2006) is a classic NLU task featured in the original GLUE benchmark. Given a pair of texts A and B, the task consists of determining whether A is a logical premise of B." |
| Q60 | 5 | input_content | "Lothritz et al. (2023) released a machine-translated Luxembourgish version of the dataset using Google Translate. However, due to numerous grammar and vocabulary related mistakes introduced in this process, we set out to improve the quality of the dataset." |
| Q61 | 5 | input_form | "Specifically, we first prompted CHATGPT-5.1 to assess and improve the translated sentence pairs unless they were already of very high quality, while explicitly keeping the original meaning to avoid label conflicts (see Appendix 7.4)." |
| Q62 | 5 | output_content | "In addition, we perform two verification steps to make sure that (a) the quality of the improved texts is high enough and (b) that the labels are correct." |
| Q63 | 5 | output_content | "To achieve (a), we prompted CHATGPT-5-MINI to judge the texts in the improved data and label their quality as either low, medium, or high, keeping only data rated at least medium, removing nearly 25% of the entire dataset (see Appendix 7.5)." |
| Q64 | 5 | output_content | "For (b), we prompted CHATGPT-5-MINI to verify whether the dataset labels remained correct after the first translation and improvement, outputting true or false for each sentence pair (see Appendix 7.6). Nearly 10% of the labels were false." |
| Q65 | 5 | output_content | "We found that the quality improvement step often corrected intentional logical contradictions or factual inaccuracies rather than keeping the original semantics. We therefore adjusted the sentences manually such that they corresponded to the ground truth again, while keeping false positives intact." |
| Q66 | 5 | input_content | "The filtering reduced between 22 and 28% of instances in the data, resulting in a final dataset of 1,876, 197, and 626 sentence pairs for the training, development, and test set, respectively." |
| Q67 | 5 | input_ontology | "Together, the eight tasks in LTZGLUE form a broad and balanced evaluation suite, covering four binary and four multi-class settings, sentence- and document-level inputs, as well as a token-level sequence-labelling task." |
| Q68 | 5 | input_ontology | "Despite the low-research status of LTZ, this places LTZGLUE in the same general range as the original English GLUE benchmark, which comprises nine diverse NLU tasks (Wang et al., 2019b)." |
| Q69 | 5 | input_ontology | "In addition, a substantial proportion of the LTZGLUE tasks are newly created for LTZ rather than direct translations or simple repackaging, allowing the benchmark to reflect phenomena and usage patterns specific to the language." |
| Q70 | 6 | input_ontology | "In this landscape, supporting eight tasks for LTZ, including token-level NER and several newly constructed text-level tasks, is a strong indicator of the maturity and breadth of the emerging LTZ NLP ecosystem." |
| Q71 | 6 | input_ontology | "This design allows us to assess current LTZ NLU performance across fundamentally different modelling paradigms, while maintaining a clear separation between task-specific supervision and general-purpose language understanding." |
| Q72 | 6 | input_form | "We train two encoder language models for LTZ: LTZ-E1-mini with 68M and LTZ-E1-base with 110M non-embedding parameters." |
| Q73 | 6 | input_form | "We closely follow the Ettin recipe (Weller et al., 2026), which is based on MODERNBERT (Warner et al., 2025)." |
| Q74 | 6 | input_content | "The pre-training set is compiled from a variety of sources of LTZ. A large portion of the data stems from RTL (see Section 3), including news articles (News), transcribed radio interviews (Radio), and user comments (Comments). We also include transcribed podcasts (Podcasts) and transcribed political speeches and debates from the Chambre des Députés (Chamber). In addition, we use 1M sentences from the web crawl of the Leipzig Collection (Web, this excludes RTL), text crawled from LTZ chat rooms (Webchat), a Wikipedia crawl from October 2023 (Wikipedia), and finally, example sentences from the LOD retrieved in March 2024." |
| Q75 | 6 | input_form | "We filter out sentences containing fewer than three words (as tokenized by whitespace), totalling 11.7M sentences, which corresponds to roughly 233M tokens using our tokenizer." |
| Q76 | 6 | output_form | "We evaluate a set of supervised encoder-based models that explicitly support LTZ, either through direct pre-training or multilingual coverage." |
| Q77 | 6 | output_form | "As a representative baseline, we include multilingual BERT (MBERT-base) (Devlin et al., 2019), which still remains widely used for multilingual transfer and low-resource evaluation." |
| Q78 | 6 | output_form | "We additionally evaluate a more recent multilingual BERT (MMBERT-base) variant with updated pre-training data and tokenisation." |
| Q79 | 6 | output_form | "To complement these general-purpose multilingual models, we include LUXEMBERT, a language-specific model trained on LTZ data (Lothritz et al., 2022), which provides a stronger inductive bias for the language's lexical and orthographic properties." |
| Q80 | 6 | output_form | "Finally, we evaluate XLM-RoBERTa (XLM-R-base) (Conneau et al., 2020), a large-scale multilingual model trained on substantially more data and languages than MBERT-base, and commonly used as a strong reference point for multilingual NLU." |
| Q81 | 6 | output_form | "In addition to supervised encoder-based models, we evaluate a set of LLMs in a prompt-based zero-shot setting. This group includes QWEN3-235B, LLAMA-3.3, GEMMA-3-27B, and GPT5-MINI, which represent a range of model sizes, training regimes, and degrees of multilingual coverage." |
| Q82 | 6 | input_content | "None of these models are fine-tuned on LTZGLUE, although some of the text data (RTL, Wikipedia) is very likely to have been processed during training." |
| Q83 | 6 | output_form | "The models are evaluated using prompts that describe each task, allowing us to assess their ability to generalise to LTZ without task-specific supervision." |
| Q84 | 6 | output_form | "We did not use a Multiple Choice Question Answering (MCQA)-setup, but provided the labels that should be used as output." |
| Q85 | 6 | output_form | "This evaluation setting reflects the growing use of LLMs as general-purpose language understanding systems, particularly in scenarios where annotated data is scarce or unavailable." |
| Q86 | 6 | output_form | "However, prompt-based evaluation introduces additional sources of variability, including prompt sensitivity and differences in instruction-following behaviour across models. As a result, performance should be interpreted as indicative rather than directly comparable to supervised results." |
| Q87 | 6 | output_form | "Nevertheless, including these models provides a complementary perspective on the current capabilities of large-scale multilingual and instruction-tuned systems for LTZ NLU." |
| Q88 | 7 | output_form | "We evaluate the models described in Section 4 across all tasks in the benchmark." |
| Q89 | 7 | output_form | "For encoder-based models, results are reported as averages over multiple runs (see Appendix 7.2 for more details)." |
| Q90 | 7 | output_form | "Prompted LLMs do not always produce well-formed outputs and may return an incorrect number of predictions for a given task; such outputs are discarded prior to evaluation." |
| Q91 | 7 | output_form | "All reported scores are computed on the remaining valid predictions per model." |
| Q92 | 7 | output_form | "For the supervised models, since the linguistic acceptability and sentiment analysis datasets are highly imbalanced, when fine-tuning on these tasks we use class-balanced loss based on effective size (Cui et al., 2019) with a beta of 0.99." |
| Q93 | 7 | output_form | "Table 6 shows F1 scores for all models across all tasks (see Appendix 7.9 for full results)." |
| Q94 | 7 | output_form | "Encoder-based models perform strongly across most settings, particularly on structurally complex and label-sensitive tasks, confirming findings from prior work on multilingual and low-resource NLU (Wu and Dredze, 2019; Conneau et al., 2020)." |
| Q95 | 7 | output_form | "Prompted large language models, by contrast, show more variable behaviour and perform competitively only on a set of semantically coarse-grained tasks, consistent with recent observations that prompting alone is often insufficient for strong performance on structured NLU tasks (Wei et al., 2022; Liu et al., 2023)." |
| Q96 | 8 | output_form | "Table 6: Test F1 scores across all ltzGLUE tasks. Encoder results are averaged over three runs with standard deviations as subscripts. Prompted LLMs were evaluated once; we report macro-F1 only." |
| Q97 | 8 | output_form | "MMBERT-base achieves the highest score with very low variance, indicating both high accuracy and stability." |
| Q98 | 8 | output_form | "In contrast, prompted LLMs perform substantially worse than all fine-tuned encoders." |
| Q99 | 8 | input_ontology | "The topic classification task emerges as the easiest overall. All encoder models achieve very high F1 scores with extremely low variance, indicating a stable and largely language-agnostic task." |
| Q100 | 8 | output_form | "Prompted LLMs perform competitively in this setting: GPT and QWEN approach encoder-level performance in a single run." |
| Q101 | 8 | output_form | "Results on the intent detection task reveal a clear separation between models. Among the encoders, LUXEMBERT achieves the strongest performance with very low variance, highlighting the benefit of language-specific pre-training." |
| Q102 | 8 | output_form | "Prompted LLMs struggle substantially with this task: all LLMs achieve low F1 scores, with GEMMA performing particularly poorly. This suggests that intent classification in LTZ relies on supervised task-specific training." |
| Q103 | 8 | input_ontology | "The recognising textual entailment task is the most challenging overall, with low F1 scores and high variance across encoder models." |
| Q104 | 8 | output_form | "Prompted LLMs perform relatively well in comparison to most encoders: GPT and QWEN achieve strong single-run F1 scores, exceeding all encoder models except MMBERT-base." |
| Q105 | 8 | output_form | "First, MMBERT-base consistently achieves the strongest or near-strongest performance across almost all tasks, combining high mean F1 scores with comparatively low variance, suggesting that broad multilingual pre-training with sufficient LTZ exposure yields stable and transferable representations." |
| Q106 | 8 | output_form | "Second, LTZ-specific encoders such as LUXEMBERT and LTZ-E1-mini are particularly competitive on lexically grounded or task-specific settings (e.g., intent detection and acceptability), but exhibit greater instability on structurally complex inference tasks such as multi-class acceptability and textual entailment." |
| Q107 | 8 | output_form | "Third, prompted LLMs display substantially more task-dependent behaviour and generally underperform fine-tuned encoders, except on semantically coarse-" |
| Q108 | 9 | input_ontology | "This paper makes two central contributions to LTZ NLU. First, we introduce a new benchmark that provides the first comprehensive GLUE-style evaluation suite for LTZ. Second, we present a systematic evaluation of encoder-based models and prompted large language models across all tasks, offering concrete guidance on model choice in such a low-resource setting." |
| Q109 | 9 | input_content | "The construction of the dataset required a deliberately resource-conscious approach. In the absence of large, task-diverse annotated resources, we combine the reuse of existing datasets with the targeted annotation of new data, carefully aligning annotation schemes across tasks, and using large language models as auxiliary tools." |
| Q110 | 9 | input_content | "While LTZGLUE provides the first systematic benchmark for LTZ NLU, the dataset remains constrained by the availability and scope of existing resources. Several tasks rely on relatively small or domain-specific corpora, which limits the ecological validity of the results and restricts the range of linguistic phenomena covered." |
| Q111 | 9 | input_content | "In addition, some of the data sources used in this benchmark may already be included, in whole or in part, in the pre-training corpora of the large language models evaluated in this work. While the exact composition of proprietary pre-training datasets is typically not fully disclosed, this potential overlap cannot be entirely ruled out and may inflate performance estimates." |
| Q112 | 9 | input_content | "Coverage across domains, registers, and demographic varieties may also be limited. LTZ displays substantial orthographic and sociolinguistic variation, yet most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts." |
| Q113 | 9 | output_content | "Although we draw on established GLUE-style tasks, some annotation decisions and class distributions are necessarily influenced by resource constraints. Certain tasks exhibit label imbalance or rely on automatic preprocessing, which may introduce biases that we cannot fully quantify." |
| Q114 | 9 | output_content | "We would like to thank the student assistants for their annotation work." |
| Q115 | 9 | output_content | "This work is supported by the LLMs4EU project, funded by the European Union through the Digital Europe Programme (DIGITAL) under the grant agreement 10119847. FK and BP are supported by the ERC Consolidator Grant DIALECT 101043235." |
| Q116 | 9 | input_form | "The datasets included in this work are derived from publicly accessible sources that permit research use, and all preprocessing avoids the inclusion of directly identifying personal information." |
| Q117 | 10 | output_content | "However, some tasks draw on data originally produced in institutional or media contexts, which may reflect societal biases in representation." |
| Q118 | 10 | output_content | "These patterns can influence model behaviour and should be considered when deploying systems trained on LTZGLUE." |
| Q119 | 10 | input_content | "LTZ is a small language community, and linguistic data often originate from a limited set of public domains." |
| Q120 | 10 | output_content | "As a result, models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices." |
| Q121 | 10 | output_content | "We therefore caution against using benchmark performance as evidence of cultural or demographic coverage." |
| Q122 | 10 | input_content | "Finally, although no sensitive content is intentionally included, automated filtering and preprocessing cannot guarantee the complete removal of harmful or offensive material." |
| Q123 | 10 | output_content | "Researchers using LTZGLUE are encouraged to inspect task-specific subsets and consider downstream implications, especially in public-facing settings." |
| Q124 | 12 | input_ontology | "For demonstration purposes, we present an example for each task in ltzGLUE in Table 7. The examples are intended to illustrate the task formulations and typical model inputs and outputs." |
| Q125 | 12 | input_form | "We follow the Ettin recipe (Weller et al., 2026), based on ModernBERT (Warner et al., 2025), for training hyperpameters and model architecture." |
| Q126 | 12 | input_form | "We train two sizes of LTZ-E1 models, mini and base, with 68M and 110M non-embedding parameters, respectively." |
| Q127 | 12 | input_form | "LTZ-E1-mini has 19 hidden layers, a hidden size of 512, an intermediate size of 768, and 8 attention heads, whereas LTZ-E1-base has 22 hidden layers, a hidden size of 768, an intermediate size of 1152, and 12 attention heads." |
| Q128 | 12 | input_form | "Both models share a GPTNeoXTokenizerFast tokenizer (Black et al., 2022), a BPE-based tokenizer, which we train on the entire pre-training set, using a minimum frequency of two and a vocabulary size of 50,368." |
| Q129 | 12 | input_form | "We use a constant batch size of 1024 packed sequences, where both models have a max sequence length of 1024." |
| Q130 | 12 | input_form | "We follow ModernBERT (Warner et al., 2025) and Ettin (Weller et al., 2026) in using the Warmup-Stable-Decay (WSD) scheduler (Zhai et al., 2022; Hu et al., 2024), though we use a shorter warmup and decay phase of 500 batches each, due to our smaller pre-training dataset size and larger number of epochs (10 vs. one)." |
| Q131 | 12 | input_form | "Again following ModernBERT and Ettin's recipe, we use the StableAdamW optimizer (Wortsman et al., 2023), with a peak learning rate of 3e-3 with a weight decay of 3e-4 for LTZ-E1-mini and 8e-4 with a weight decay of 1e-5 for LTZ-E1-base." |
| Q132 | 12 | input_content | "As our pre-training set is small, we" |
| Q133 | 13 | output_form | "We use a 20GB MIG partition of an NVIDIA A100-SXM4-80GB to pretrain each model, taking 47 hours for LTZ-E1-mini and 76 hours for LTZ-E1-base." |
| Q134 | 13 | output_form | "However, we note that compute times were negatively impacted by concurrent jobs on the server cluster with suboptimal CPU thread management." |
| Q135 | 13 | input_content | "We show pre-training data token counts per source in Table 9, where sources (described in Section 4.1) are: RTL news articles (News), RTL transcribed radio interviews (Radio), RTL user comments (Comments), transcribed podcasts (Podcasts), transcribed political speeches and debates from the Chambre des Députés (Chamber), 1M sentences from the web crawl of the Leipzig Collection (Web), text from Luxembourgish chat rooms (Webchat), a Wikipedia crawl (Wikipedia), and examples from the Luxembourgish Online Dictionary (LOD)." |
| Q136 | 13 | output_form | "Though we do not aim to optimise performance in our evaluation, we conduct basic hyperparameter sweeps for each model and task combination in order to provide a fairer comparison across models." |
| Q137 | 13 | output_form | "For each model and task combination, we select the best hyperparameters based on the validation set, and use those parameters to finetune two additional models with differing seeds, resulting in three runs." |
| Q138 | 13 | output_form | "In order to reduce the computational demand of the sweeps, we use Bayesian search with early stopping after three iterations, and cap each sweep at 30 runs, for 1,440 total runs across all models and tasks (and an additional 96 to finetune the two additional seeds)." |
| Q139 | 13 | output_form | "However, we note again that these ranges were kept simple to keep sweeps computationally feasible, thus, these values should not be seen as optimal hyperparameters." |
| Q140 | 14 | output_form | "We use several 20GB MIG partitions of NVIDIA A100-SXM4-80GB GPUs to conduct the sweeps. Depending on model and task dataset size, multiple runs were conducted in parallel on each partition, totalling 59 days of compute, which includes fine-tuning the additional seeds, as well as evaluation on the validation and test sets." |
| Q141 | 14 | input_content | "Table 9: Token counts (M) per source for pretraining data of LTZ-E1." |
| Q142 | 14 | output_form | "Table 10: Hyperparameter sweep ranges used for all task and model combinations." |
| Q143 | 14 | output_content | "You are an expert for the Luxembourgish language. I am giving you a sentence in Luxembourgish. You have to judge its quality and improve it while keeping the meaning intact. As output, write only the improved sentence or the original sentence if it is of very high quality." |
| Q144 | 14 | output_content | "You are an expert for the Luxembourgish language. I am giving you two texts in Luxembourgish. You have to judge their quality. As output, simply write 'low', 'medium' or 'high' depending on the quality of both sentences, nothing else." |
| Q145 | 14 | output_content | "You are an expert for the Luxembourgish language. I am giving you two texts TEXT1 and TEXT2 in Luxembourgish as well as a LABEL where 1 means that TEXT1 logically entails TEXT2 while 0 means the opposite. You have to check if the labels are correct. As output, simply write 'true' if the label is the correct one or 'false' if the label is incorrect." |
| Q146 | 14 | output_form | "You are a classification and text-processing model specialized in NLP tasks for Luxembourgish (lb). Follow ALL rules strictly: 1. Respond ONLY in valid JSON. 2. Do NOT add explanations, comments or text outside of JSON. 3. Use field: "output": <model_answer>. 4. Use field: "task": "<task_name>". 5. Use field: "input": "<input example text>". 6. Predict only the requested outputs and" |
| Q147 | 15 | output_ontology | "If determined labels are 0 and 1 then 0 is used for False, 1 is used for True." |
| Q148 | 15 | input_ontology | "headline_classification: Decide if the given title/headline fits the text. Output True or False." |
| Q149 | 15 | output_ontology | "sentiment_analysis: Classify sentiment of the text. Allowed labels: positive, neutral, negative." |
| Q150 | 15 | input_ontology | "linguistic_acceptability_binary: Decide whether the sentence is linguistically acceptable in Luxembourgish. Output: 0 or 1." |
| Q151 | 15 | output_ontology | "linguistic_acceptability_multilabel: Detect if the sentence is correct or if some element is wrong. If the sentence is correct, Output: correct. If it is not, Output the label referencing the wrong element: syntax, verb, ortho or adj." |
| Q152 | 15 | output_ontology | "ner: Perform Named Entity Recognition on the given sequence of sentence tokens. Output tags as lists of ner_tags. Allowed Tags: O, B-LOC, I-LOC, B-PER,I-PER, B-DATE, I-DATE,B-ORG, I-ORG, B-MISC, I-MISC." |
| Q153 | 15 | output_ontology | "topic_classification: Classify topic of the document by title and text. Allowed category_names: sports, animals, business, culture, technology." |
| Q154 | 15 | output_ontology | "slot_intent_detection: Detect the intent for the text given. Allowed intents: reminder/show_reminders, weather/find, reminder/set_reminder, reminder/cancel_reminder, alarm/snooze_alarm, alarm/show_alarms, alarm/set_alarm, nalarm/cancel_alarm, nalarm/time_left_on_alarm." |
| Q155 | 15 | output_ontology | "recognizing_textual_entailment: Determine if the information in the second sentence is entailed in the first one. Output: 0 or 1." |
| Q156 | 15 | output_form | "We show full results (validation and test set performance) for each model and task for HA, SA, LA (BINARY), and LA (MULTI) in Table 12 and for NER, TC, ID, and RTE in Table 13." |
| Q157 | 16 | output_form | "Table 11: Best hyperparameters per model for each task." |
| Q158 | 17 | output_form | "Dev and Test F1 scores for Headline Acceptability (HA), Sentiment Analysis (SA) and Linguistic Acceptability (Binary LAB and Multi LAM. Results are averaged over three runs, with standard deviations as subscripts." |
| Q159 | 17 | output_form | "Dev and Test F1 scores for Named Entity Recognition (NER), Topic Classification (TC), Intent Detection (ID) and Textual Entailment (RTE). Results are averaged over three runs, with standard deviations as subscripts." |

---

## Regional Context

```yaml
name: Luxembourg Public Administration — Civil Servant NLU Deployment
abbreviation: LU-PUBADMIN
deployment_context:
  system_function: LLM-based automated classification of citizen correspondence for
    routing to government departments and prioritization of urgent or frustrated messages,
    with human-in-the-loop fallback for low-confidence cases.
  benchmark_evaluated: LTZGLUE
  primary_region: Luxembourg
  governance_levels:
  - national (état)
  - communal (commune)
  institutional_scope: National ministries and communal administrations processing
    digital citizen feedback channels
  eu_dimension: Luxembourg hosts major EU institutions; a non-trivial share of incoming
    correspondence may concern EU-adjacent administrative matters (frontier worker
    regulation, EU residency rights, cross-border social security)
target_population:
  primary_users: Civil servants in Luxembourgish government agencies (national and
    communal levels) reviewing automated routing decisions, auditing system flags,
    and providing real-time feedback on model output quality via the human-in-the-loop
    interface.
  secondary_population: Citizens and residents writing digital correspondence to government
    bodies; includes a significant sub-population of cross-border workers (frontaliers)
    domiciled in France, Belgium, or Germany but employed and administratively active
    in Luxembourg.
  cross_border_worker_salience: Cross-border workers represent approximately 47% of
    total Luxembourg employment (STATEC 2024 — [WEB-1];
    OECD Economic Survey Luxembourg 2025 — [WEB-2]).
    Their administrative queries involve distinct legal, tax, and social-security
    frameworks that differ materially from resident-citizen queries, making this a
    high-priority sub-population for topic classification accuracy.
  civil_servant_profile: Professionally multilingual; expected to work across Luxembourgish,
    French, and German; familiar with both national administrative procedures and
    EU regulatory context; primary consumers of the automated routing dashboard and
    escalation queue.
  citizen_writer_profile: Multilingual residents and non-resident workers; orthographically
    non-standardized Luxembourgish is common; French and German code-switching frequent
    even in formally intended messages; range from highly educated professionals to
    residents with limited formal literacy in Luxembourgish.
country: Luxembourg
languages:
  administrative_official:
  - Luxembourgish (Lëtzebuergesch)
  - French
  - German
  primary_benchmark_language: Luxembourgish (lb / LTZ)
  code_switching_patterns: Citizen correspondence routinely alternates between Luxembourgish,
    French, and German within a single message. French-derived and German-derived
    loanwords for identical administrative concepts coexist (e.g., 'Administratioun'
    vs. 'Verwaltung'); a model trained on standardized Luxembourgish alone will encounter
    significant out-of-distribution input.
  orthographic_status: Luxembourgish orthography is not fully standardized as of the
    benchmark's publication; substantial variation in spelling, punctuation, and capitalization
    norms is attested in citizen-facing text.
  note: The benchmark (LTZGLUE) targets standard written Luxembourgish; the deployment
    input distribution is broader and includes informal, code-switched, and orthographically
    variable text. This divergence is a primary validity risk flagged in the elicitation.
  language_law_constitutional_status: Since 1 July 2023, Luxembourgish has been anchored
    in the Constitution as the national language of the Grand Duchy, alongside French
    and German as administrative languages (Luxembourg Government — [WEB-3]).
    This elevates the political importance of Luxembourgish-language processing in
    public-sector AI tools.
writing_systems:
  scripts:
  - Latin alphabet with diacritics (ä, ë, é, etc. as used in Luxembourgish, French,
    German)
  note: All three administrative languages use Latin script. No script-direction mismatch.
    Mixed-language text is common; tokenizers trained on monolingual Luxembourgish
    corpora may underperform on French- or German-heavy passages within otherwise
    Luxembourgish messages.
population_size:
  luxembourg_total_population: 672,050 as of 1 January 2024 (STATEC — [WEB-4])
  resident_citizens_and_long_term_residents: '[NEEDS VERIFICATION — deferred: below
    search budget; STATEC 2024 brochure exists but sub-national citizen vs. long-term-resident
    breakdown not surfaced in available search results]'
  cross_border_workers_frontaliers: 'Approximately 231,290 cross-border workers in
    Q1 2024 (Paperjam/IGSS data — [WEB-5]),
    representing ~47% of total employment. Origin-country breakdown: approximately
    120,000 from France (majority), ~50,000 from Belgium, ~50,000 from Germany (STATEC
    via alleyesonme.jobs — [WEB-6]).
    OECD 2025 confirms: 50% from France, remaining split evenly between Belgium and
    Germany (OECD Economic Survey Luxembourg 2025 — [WEB-2]).'
  civil_servants_national_level: '[NEEDS VERIFICATION — deferred: below search budget;
    specific national fonctionnaires headcount not surfaced; STATEC ''Luxembourg in
    figures 2024'' (92-page edition) likely contains this but full text not accessible]'
  civil_servants_communal_level: '[NEEDS VERIFICATION — deferred: below search budget;
    communal-level civil servant headcount not found in available sources]'
literacy_and_digital_access:
  general_literacy_rate: '[NEEDS VERIFICATION — deferred: below search budget; Luxembourg
    is a high-income country and adult literacy is effectively universal per OECD
    assessments, but a verifiable formal figure was not surfaced]'
  digital_literacy_civil_servants: Expected high given professional context; civil
    servants operate standard government IT infrastructure.
  citizen_digital_access: 99.0% internet penetration rate as of January 2024, with
    651,700 internet users out of 658,300 total population (DataReportal / Kepios
    analysis 2024 — [WEB-7];
    corroborated by Eurostat/Statista household internet access figure of 99.06% for
    2023 — [WEB-8]).
  mobile_internet_penetration_pct: 886,100 cellular mobile connections active in early
    2024, equivalent to 134.6% of the total population (multiple SIM cards per user),
    with median mobile internet speed of 90.85 Mbps (DataReportal 2024 — [WEB-7]).
  note: Luxembourg is a high-income country with advanced digital infrastructure;
    access disparities are more likely along age and linguistic-background dimensions
    than income dimensions, but sub-population figures should be verified.
cultural_norms_notes: '- Citizens writing to government bodies tend to use a formal
  but often understated register; emotional frustration is typically signaled indirectly
  rather than through explicit negative language, creating a challenge for sentiment
  and urgency classifiers trained on less institutionally constrained text.

  - Code-switching between Luxembourgish, French, and German is socially unmarked
  and does not indicate informality or distress; models should not interpret language-mixing
  as a sentiment signal.

  - The distinction between national-level (ministère) and communal-level (commune)
  competencies is institutionally significant and familiar to residents; misrouting
  between these levels is a culturally salient administrative error.

  - Cross-border workers have a strong community identity and distinct administrative
  concerns; messages about frontier-worker tax status, social security, or cross-border
  transport are a recognizable genre.

  - Luxembourg''s multilingual civic culture means citizens may deliberately choose
  French or German for formal complaints, reserving Luxembourgish for more familiar
  or informal tones — though this norm is not universal.'
administrative_domain_notes:
  topic_taxonomy_requirements: 'The deployment requires a topic taxonomy that is substantially
    more granular than LTZGLUE''s five RTL editorial categories (SPORTS, CULTURE,
    TECHNOLOGY, BUSINESS, ANIMALS). Required administrative categories include at
    minimum: cross-border worker / frontalier issues, housing and cost of living,
    transport and mobility, tax and fiscal matters, social security and benefits,
    EU institutional matters, national identity documents and residency permits, communal
    services, and public health.'
  routing_dimension_state_vs_communal: A core routing requirement is distinguishing
    whether a message concerns a national (state) competency or a communal (commune)
    competency. This distinction is not encoded in any LTZGLUE task and represents
    a deployment-specific classification dimension requiring domain adaptation or
    bespoke annotation.
  cross_border_worker_legal_framework: '[NEEDS VERIFICATION — deferred: below search
    budget; the bilateral tax and social security conventions with France, Belgium
    and Germany governing frontalier status are a specialist legal domain not fully
    surfaced by available search results. Requires expert/stakeholder elicitation
    or legal specialist review.]'
  communal_vs_national_competency_split: '[NEEDS VERIFICATION — deferred: likely unsearchable
    at adequate granularity (lived administrative practice); formal enumeration of
    communal vs. national competencies exists in Luxembourg communal law but was not
    surfaced in available search results at the level of specificity needed for a
    routing taxonomy]'
  politically_sensitive_categories: Housing affordability and cost of living are flagged
    as high-priority and politically sensitive in the elicitation; messages in these
    categories may require elevated urgency scoring and careful sentiment handling.
  eu_institutional_queries: Luxembourg's role as an EU institutional seat means some
    citizen correspondence may address EU-institution-specific procedures (e.g., European
    Court of Justice, European Commission employment, EU staff regulations); these
    are unlikely to appear in any general LTZ benchmark.
legal_and_regulatory_context:
  data_protection_regime: Luxembourg implements GDPR directly with no significant
    national derogations from the Regulation's substantive provisions (Luther Law
    Firm / DataGuidance — [WEB-9]).
    The supervisory authority is the CNPD (Commission Nationale pour la Protection
    des Données — [WEB-10]). DPIAs are mandatory per GDPR
    Article 35; the CNPD has published a list of processing operations that always
    require a DPIA. The CNPD published guidelines on artificial intelligence in 2023
    (CNPD Annual Report 2023 — [WEB-11])
    and is co-launching an AI Community of Practices with the Luxembourg AI Factory
    (CNPD 2025 — [WEB-10]). No specific published CNPD guidance
    on automated processing of citizen correspondence for routing was found; a DPIA
    is highly advisable before deployment.
  automated_decision_making_constraints: EU GDPR Article 22 restricts fully automated
    decisions with significant effects on individuals; the deployment's human-in-the-loop
    fallback is directly relevant to this constraint. Routing and prioritization do
    not constitute final decisions but the boundary should be legally verified.
  applicable_ai_act_classification: The deployment's AI Act risk classification depends
    on whether the system evaluates citizen eligibility for public services or merely
    routes correspondence. EU AI Act Annex III, Category 5(a) classifies as high-risk
    AI systems 'intended to be used by public authorities … to evaluate the eligibility
    of natural persons for essential public assistance benefits and services' (EU
    AI Act Regulation (EU) 2024/1689, official text — [WEB-12]).
    A pure routing/triage system that performs preparatory sorting without determining
    eligibility may qualify for the Article 6(3) exception as 'a preparatory task
    to an assessment', but this must be legally verified. High-risk AI obligations
    under Annex III are scheduled to apply from August 2, 2026, though the Digital
    Omnibus proposal (November 2025) may adjust timelines (European Commission — [WEB-13]).
  public_sector_procurement_standards: '[NEEDS VERIFICATION — deferred: below search
    budget; Luxembourg Ministry of Digitalisation IT procurement guidelines for LLM
    tools not surfaced in available searches; requires direct contact with Ministère
    de la Digitalisation]'
  language_law_obligations: 'Law of 24 February 1984 on the language regime (Loi du
    24 février 1984 sur le régime des langues), as confirmed by the official Legilux
    text and government sources: Article 4 requires the administration, ''dans la
    mesure du possible'', to reply in the language chosen by the petitioner (Luxembourgish,
    French, or German) (official Legilux — [WEB-14];
    Guichet.lu — [WEB-15]).
    In practice, French is the dominant written administrative language; Luxembourgish
    functions as the oral/informal register (Guichet.lu ibid.). Since 1 July 2023,
    Luxembourgish and multilingualism are enshrined in the Constitution (Luxembourg
    Government — [WEB-3]).
    For the deployment, the language-of-input detection module must reliably identify
    the citizen''s language choice to fulfil this legal obligation in any automated
    or human-mediated response.'
infrastructure_notes:
  deployment_modality: Text-only; citizen correspondence submitted via digital channels
    (web forms, email, potentially messaging platforms). No speech or image modality
    in scope.
  expected_input_length: Short to medium-length messages (complaint letters, inquiries,
    feedback forms); likely within LTZGLUE's 40–400 word preprocessing range for some
    inputs, but formal complaint letters may exceed this.
  government_it_environment: '[NEEDS VERIFICATION — deferred: below search budget;
    Luxembourg Ministry of Digitalisation cloud/on-premises hosting requirements for
    citizen-data-processing LLM tools not found in available searches; sovereign cloud
    requirements under GDPR apply but specific LU government policy not surfaced]'
  connectivity: National digital infrastructure is advanced; civil servant workstations
    operate on standard government networks. No low-bandwidth considerations.
  human_in_the_loop_interface: Civil servants interact with a routing dashboard that
    surfaces low-confidence flags and escalated messages; the system collects real-time
    feedback for progressive model alignment.
nlp_tooling_and_model_context:
  luxembourgish_nlp_ecosystem_maturity: Low-resource. Luxembourgish has limited NLP
    tooling relative to French, German, or English. LTZGLUE represents the first unified
    NLU benchmark; available encoder models include LUXEMBERT, LTZ-E1-mini, LTZ-E1-base,
    and multilingual models (mBERT, XLM-R) with partial LTZ coverage.
  benchmark_data_sources: Primarily RTL news articles; supplemented by the Luxembourgish
    Online Dictionary, Wikipedia/Wikidata, and a machine-translated English intent
    corpus. The formal/institutional register of most sources diverges from citizen
    correspondence.
  code_switching_coverage_in_benchmark: Partial — the human-annotated NER sub-corpus
    covers informal and code-mixed writing; other tasks do not systematically represent
    French/German code-switching or non-standard orthography.
  multi_label_format_gap: All LTZGLUE tasks produce single hard labels; the deployment
    requires multi-label classification with calibrated confidence scores. This is
    a structural mismatch requiring model-level adaptation beyond benchmark evaluation
    scope.
  sentiment_task_limitations: 'LTZGLUE sentiment task: 3 classes (positive, neutral,
    negative), Cohen''s Kappa 0.45 (moderate), annotated by two native speakers with
    no documented administrative communication expertise. Does not capture urgency,
    frustration intensity, or the formal-but-understated civil register.'
  intent_detection_task_limitations: LTZGLUE intent labels are exclusively voice-assistant
    commands (alarm, reminder, weather); no administrative intent categories (complaint,
    document request, tax inquiry, urgent escalation) are present.
benchmark_validity_risks_summary:
  input_ontology_gap: LTZGLUE topic and intent taxonomies have no overlap with Luxembourg-specific
    administrative categories required for routing. Domain adaptation or bespoke task
    construction is needed.
  input_content_gap: Benchmark inputs are drawn from formal/standardized sources;
    deployment inputs will include code-switched, orthographically variable, and colloquial
    Luxembourgish. NER sub-corpus provides partial coverage of informal register only.
  output_ontology_gap: Single hard-label format across all tasks is incompatible with
    multi-label routing logic and confidence-based escalation. Sentiment labels do
    not map to urgency/frustration scales needed operationally.
  output_content_gap: Annotator provenance for sentiment task is undocumented with
    respect to administrative register familiarity; moderate inter-annotator agreement
    (κ=0.45) limits label reliability for nuanced civil communication.
  human_in_the_loop_mitigation: The deployment includes a civil-servant feedback mechanism
    for progressive alignment; this partially mitigates OC and OO risks at runtime
    but does not address pre-deployment benchmark validity gaps.
net_new_fields:
  frontalier_employment_share_detail:
    value: ~47% of Luxembourg's 489,000–522,650 employees (depending on reference
      period) are cross-border workers; approximately 231,290 in Q1 2024. French frontaliers
      account for ~44–50% of all cross-border workers and 70% of new commuter growth;
      Belgian and German workers account for ~15% and ~14% respectively of total employment
      (STATEC / Paperjam / OECD 2025 — [WEB-5];
      [WEB-2]).
    validity_relevance: The linguistic and administrative profile of incoming correspondence
      will be heavily influenced by the French-dominant frontalier majority. French-language
      administrative queries are likely overrepresented relative to what a Luxembourgish-only
      benchmark would anticipate.
  luxembourg_language_law_2023_constitutional_update:
    value: Effective 1 July 2023, the Luxembourgish language and multilingualism are
      anchored in the Constitution. The language law of 24 February 1984 (Article
      4) requires the administration to respond, 'dans la mesure du possible', in
      the language chosen by the citizen (Luxembourgish, French, or German). Legislative
      acts must be in French; French is the sole authentic legal text in all administrative
      acts (Legilux official text — [WEB-14];
      Luxembourg Government 40th anniversary note — [WEB-3]).
    validity_relevance: 'Language-of-input detection is not merely a convenience feature:
      it is legally required for correct administrative response. A failure by the
      routing model to correctly identify whether a message is in Luxembourgish, French,
      or German could create legal exposure for the deploying authority.'
  eu_ai_act_timeline_note:
    value: High-risk AI obligations under EU AI Act Annex III are scheduled to apply
      from August 2, 2026 for systems placed on the market after that date, though
      the Digital Omnibus proposal (November 2025) under consideration by the European
      Parliament may adjust this timeline (European Commission FAQ — [WEB-13]).
    validity_relevance: If the routing system is classified as high-risk (Category
      5 / essential services assessment), compliance obligations include risk management
      systems, data governance, human oversight documentation, and a Fundamental Rights
      Impact Assessment — all of which have direct implications for how benchmark
      validity is documented and audit-trailed.
  cnpd_ai_guidelines_2023:
    value: The CNPD published guidelines on artificial intelligence in 2023 and is
      co-launching a RE.M.I. 'Regulation Meets Innovation' AI Community of Practices
      with the Luxembourg AI Factory (CNPD 2025 — [WEB-10];
      CNPD Annual Report 2023 — [WEB-11]).
      No specific published guidance on citizen-correspondence routing NLU was found.
    validity_relevance: The CNPD is the relevant DPA for GDPR compliance review of
      this deployment. Its 2023 AI guidelines and ongoing Community of Practices are
      the primary contact points for pre-deployment regulatory engagement; absence
      of sector-specific guidance means deployers must rely on GDPR Article 35 DPIA
      requirements and GDPR Article 22 constraints directly.
flagged_items_for_web_search:
- item: Current frontalier (cross-border worker) share of Luxembourg total employment
    and origin-country breakdown
  search_target: Luxembourg frontaliers statistics 2024 STATEC cross-border workers
    France Belgium Germany
  resolution_status: RESOLVED — see population_size.cross_border_workers_frontaliers
    and net_new_fields.frontalier_employment_share_detail
- item: CNPD guidance on automated processing of citizen correspondence in public
    sector
  search_target: Luxembourg CNPD GDPR Article 22 automated decision-making public
    sector guidance
  resolution_status: PARTIALLY RESOLVED — CNPD is the supervisory authority; 2023
    AI guidelines published; no sector-specific routing-NLU guidance found. See legal_and_regulatory_context.data_protection_regime
    and net_new_fields.cnpd_ai_guidelines_2023
- item: EU AI Act high-risk classification applicability to public-sector NLU routing
    systems
  search_target: EU AI Act high-risk public administration automated routing citizen
    correspondence classification
  resolution_status: RESOLVED — see legal_and_regulatory_context.applicable_ai_act_classification
    and net_new_fields.eu_ai_act_timeline_note
- item: Luxembourg language law (Law of 24 February 1984) administrative language
    obligations
  search_target: Luxembourg loi du 24 février 1984 régime des langues administration
    obligations réponse
  resolution_status: RESOLVED — see legal_and_regulatory_context.language_law_obligations
    and net_new_fields.luxembourg_language_law_2023_constitutional_update
- item: Formal enumeration of communal vs. national administrative competencies in
    Luxembourg
  search_target: Luxembourg communes compétences nationales distinction loi commune
    état administration
  resolution_status: DEFERRED — likely unsearchable at required granularity; requires
    expert elicitation or legal specialist review
- item: LTZGLUE benchmark data source register documentation and code-switching coverage
  search_target: LTZGLUE Luxembourgish benchmark register code-switching informal
    orthographic variation data sources
  resolution_status: NOT SEARCHED — already well-documented in benchmark YAML verbatim
    quotes (Q112, Q41, Q55); search budget allocated to higher-impact tags
- item: Existing Luxembourgish administrative NLP datasets or topic taxonomies for
    civic/government domains
  search_target: Luxembourgish administrative NLP dataset civic topic classification
    cross-border worker government
  resolution_status: NOT SEARCHED — search budget exhausted; flagged for future pass;
    high prior probability of null result given LTZGLUE's own acknowledgment of near-nonexistent
    LTZ labeled resources
- item: Luxembourg Ministry of Digitalisation IT procurement and cloud policy for
    LLM-based tools
  search_target: Luxembourg Ministry of Digitalisation LLM AI procurement policy government
    cloud citizen data
  resolution_status: DEFERRED — below search budget; see infrastructure_notes.government_it_environment
- item: Current internet and smartphone penetration rates in Luxembourg
  search_target: Luxembourg internet penetration rate 2024 digital access statistics
    STATEC
  resolution_status: RESOLVED — see literacy_and_digital_access.citizen_digital_access
    and literacy_and_digital_access.mobile_internet_penetration_pct
- item: Luxembourg civil servant workforce size at national and communal levels
  search_target: Luxembourg fonctionnaires nombre administration nationale communale
    STATEC 2023 2024
  resolution_status: NOT FOUND — searched STATEC portal and Luxembourg population
    statistics; aggregate public-sector employment growth noted (+3.7% year-on-year
    in 'administration and other public services', STATEC Q1 2025 — [WEB-16])
    but specific national vs. communal civil servant headcounts not published in accessible
    sources
- item: LTZGLUE annotator demographics and professional background for sentiment task
  search_target: LTZGLUE sentiment annotation annotator demographics professional
    background administrative register Luxembourgish
  resolution_status: NOT SEARCHED — benchmark YAML already documents absence of this
    information; search budget allocated to higher-impact tags
- item: Multi-label NLU evaluation approaches for low-resource languages applicable
    to Luxembourgish
  search_target: multi-label classification low-resource NLU confidence calibration
    Luxembourgish benchmark adaptation
  resolution_status: NOT SEARCHED — search budget exhausted; flagged for future pass
- item: Legal and bilateral tax treaty frameworks governing frontalier workers in
    Luxembourg
  search_target: Luxembourg frontaliers bilateral tax convention France Belgium Germany
    social security administrative procedures
  resolution_status: DEFERRED — below search budget; specialist legal domain requiring
    expert elicitation rather than web search
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://statistiques.public.lu/en/publications/series/regards/2025/regards-01-25.html |
| WEB-2 | https://www.oecd.org/en/publications/2025/04/oecd-economic-surveys-luxembourg-2025_3eb782b5/full-report/reviving-productivity-growth_4509ab88.html |
| WEB-3 | https://gouvernement.lu/fr/actualites/toutes_actualites.gouv2024_mcult+fr+actualites+mes-actualites+2024+fevrier+sproochegesetz-40-joer.html |
| WEB-4 | https://statistiques.public.lu/fr/publications/series/en-chiffres/2024/demographie-lux-en-chiffres-2024.html |
| WEB-5 | https://en.paperjam.lu/article/growth-in-number-of-cross-bord |
| WEB-6 | https://media.alleyesonme.jobs/en/article-titles/le-luxembourg-attire-t-il-toujours-les-frontaliers |
| WEB-7 | https://datareportal.com/reports/digital-2024-luxembourg |
| WEB-8 | https://www.statista.com/statistics/377741/household-internet-access-in-luxembourg/ |
| WEB-9 | https://www.luther-lawfirm.com/fileadmin/user_upload/Luxembourg_-_Data_Protection_Overview___Guidance_Note___DataGuidance.pdf |
| WEB-10 | https://cnpd.public.lu/en.html |
| WEB-11 | https://cnpd.public.lu/en/actualites/national/2024/09/rapport-annuel-2023.html |
| WEB-12 | https://artificialintelligenceact.eu/annex/3/ |
| WEB-13 | https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act |
| WEB-14 | https://data.legilux.public.lu/filestore/eli/etat/leg/loi/1984/02/24/n1/jo/fr/html/eli-etat-leg-loi-1984-02-24-n1-jo-fr-html.html |
| WEB-15 | https://guichet.public.lu/fr/citoyens/justice/voies-recours-reglement-litiges/frais-avocat-justice/langues-tribunaux.html |
| WEB-16 | https://statistiques.public.lu/en/actualites/2025/stn20-25-emploi-salarie.html |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Citizen feedback to Luxembourgish government agencies likely spans topics specific to local governance — such as cross-border worker issues, multilingual administrative procedures, housing, transport, or EU institutional matters. Does the topic taxonomy the system needs cover these Luxembourg-specific administrative domains?
A1: The deployment requires fine-grained Luxembourg-specific topic coverage: distinguishing resident vs. cross-border worker status (relevant to nearly half the workforce), flagging cost-of-living and housing as politically sensitive high-priority categories, and differentiating between state and communal competencies to route messages to the correct authority level.

Q2 [IC]: Does the deployment need to handle non-standard Luxembourgish, code-switching with French or German, and informal orthography, or can it assume standard prose?
A2: Standard prose cannot be assumed. The system must handle significant orthographic variation and frequent alternation between French-derived and German-derived loanwords for the same concepts (e.g., "Administratioun" vs. "Verwaltung"). A benchmark trained solely on standardized news or legal texts would not be representative of real administrative feedback, which exhibits colloquial and code-switched characteristics even in formally intended messages.

Q3 [OC]: Were the sentiment and tone labels used in evaluation validated by annotators familiar with Luxembourgish civil communication norms — specifically, the formal and understated register citizens use with government bodies?
A3: Ideal validation would involve annotators deeply familiar with Luxembourg's administrative culture, but given the low-resource status of Luxembourgish, early evaluation data may come from different domains, risking discrepancies in sentiment and urgency detection. The system includes a human-in-the-loop auditing mechanism allowing civil servants to provide real-time feedback on routing flags to align the model progressively with actual administrative norms.

Q4 [OO]: Does the routing logic require more than a single hard label per message — e.g., multi-label or confidence-scored outputs?
A4: Yes. The routing logic requires multi-label classification because a single message can legitimately concern multiple departments or topics. Confidence scores are used to flag uncertainty, and messages that cannot be decisively categorized are escalated to human manual review rather than auto-routed.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark is sourced from a transferred cultural context and the deployment requires highly specific Luxembourg-administrative topic categories — cross-border worker status, state vs. communal competency splits, and politically sensitive housing/cost-of-living domains — that are unlikely to be represented in a general-purpose or transferred NLU benchmark. |
| IC | HIGH | Real citizen messages exhibit orthographic variation, French/German code-switching, and loanword alternation; the user confirmed a benchmark built on standardized texts would not be representative, directly flagging construct-irrelevant variance in the benchmark's concrete datapoints. |
| IF | MODERATE | The deployment is text-only and Luxembourgish is the target language of the benchmark, limiting modality mismatch; however, Luxembourgish is low-resource and the benchmark's text register (likely formal/standardized) diverges from actual input distribution, partially elevating this dimension. |
| OO | HIGH | Routing logic requires multi-label and confidence-scored outputs, whereas LTZGLUE tasks produce single hard labels; the output taxonomy was also designed for general NLU rather than administrative intent-routing, and automated high-stakes decisions amplify the cost of category mismatch. |
| OC | HIGH | Sentiment and urgency labels require familiarity with Luxembourgish formal-but-understated civil communication norms; the benchmark's "transferred cultural context" source strongly suggests annotators were not drawn from the target population, and the user explicitly acknowledged this as a known risk. |
| OF | MODERATE | Both benchmark and deployment use text-to-label format, limiting surface-level mismatch; however, the deployment's operational need for confidence scores and multi-label outputs goes beyond the single-label format LTZGLUE tasks emit, creating a functional output-form gap. |

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
  "benchmark": "ltzglue",
  "region": "Luxembourg Public Administration — Civil Servant NLU Deployment",
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
