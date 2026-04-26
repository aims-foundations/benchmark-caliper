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
- **Domain**: Natural Language Understanding for Luxembourgish
- **Languages**: lb
- **Porting Strategy**: mixed
- **Year**: 2025

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
LTZGLUE covers eight tasks — headline acceptability (HA), sentiment analysis (SA), linguistic
acceptability in binary and multi-class forms (LA-BINARY, LA-MULTI), named entity recognition
(NER), news topic classification (TC), intent detection (ID), and recognizing textual entailment
(RTE) — explicitly modelled on the English GLUE benchmark [Q1, Q8, Q68]. The suite is designed
to span "a broad spectrum of linguistic and semantic phenomena" [Q11] and covers "fundamentally
different modelling paradigms" [Q71]. Appendix prompts enumerate exact label sets per task
[Q143–Q155], confirming that all eight tasks emit single hard labels with fixed category sets.

For the deployment use case, the input ontology presents critical gaps. The topic classification
task covers only five editorial categories — SPORTS, CULTURE, TECHNOLOGY, BUSINESS, and
ANIMALS — derived from RTL news [Q48, Q153], with no administrative, civic, housing,
cross-border worker, EU-institutional, or state-vs-communal competency categories. The intent
detection task covers a narrow set of reminder and alarm intents from a voice-assistant corpus
[Q51, Q154], with no citizen-government communication intents. The NER task retains only four
entity types (PER, ORG, LOC, MISC) after tag harmonisation [Q44, Q152], with no administrative
jurisdiction or legal-status categories. Topic classification is reported as the easiest task
with near-encoder-level LLM performance [Q99, Q100], while RTE is the hardest [Q103] — a
difficulty distribution not calibrated to administratively relevant language understanding.
The authors acknowledge these structural limitations: "Coverage across domains, registers, and
demographic varieties may also be limited" [Q112].

### Input Content
The benchmark draws primarily on two main text sources: RTL (a Luxembourgish media outlet)
and the Luxembourgish Online Dictionary (LOD) [Q12], supplemented by Wikipedia, Leipzig
Collection web crawls, transcribed podcasts, transcribed political speeches from the Chambre
des Députés, and Luxembourgish chat rooms [Q74, Q135]. The sentiment analysis data comes from
RTL commentary and letters to the editor [Q24]; NER merges an automatically constructed
Wikipedia/Wikidata corpus (JUDGEWEL) [Q34, Q38] with a human-annotated RTL news comment
corpus [Q40, Q45]; topic classification is drawn from RTL editorial content [Q46]; and the
intent detection task is a human-translated adaptation of the English xSID dataset [Q51], with
a machine-translated German training set [Q54].

For the deployment, this source profile is a serious validity concern. The authors explicitly
acknowledge that "most data sources reflect formal writing or institutional usage and therefore
do not fully represent informal and multilingual contexts" [Q112], and that "linguistic data
often originate from a limited set of public domains" [Q119]. The intent detection register —
user commands for a voice-controlled AI assistant — is acknowledged to have "no equivalent
reference corpus in LTZ," making systematic terminology verification impossible [Q55, Q56].
Code-switched, orthographically variable citizen correspondence — the primary input type in
the deployment — is absent from nearly all task datasets. The RTE dataset was processed
through ChatGPT-5.1 for quality improvement and then filtered, removing 22–28% of instances
[Q60, Q66], introducing model-induced distributional artefacts into the content. The
construction required "a deliberately resource-conscious approach" combining reuse, targeted
annotation, and LLM assistance [Q109], reflecting structural constraints of the low-resource
setting rather than principled domain selection.

### Input Form
All benchmark tasks use plain text inputs in the Luxembourgish language, at sentence or
document level, with BIO-tagged token sequences for NER and intent detection [Q35, Q57].
The benchmark explicitly targets Luxembourgish as the input language [Q1], and the pre-training
tokenizer is a BPE tokenizer trained on the full LTZ pre-training set with a vocabulary of
50,368 tokens and a maximum sequence length of 1,024 [Q128, Q129]. Non-Luxembourgish articles
were filtered using the OpenLID language identifier [Q47], and sentences with fewer than three
words were removed [Q75].

For the deployment, the input form dimension is partially valid: the benchmark is text-based
and targets Luxembourgish, matching the deployment's text-only modality. However, the
benchmark's text form reflects formal, edited prose from news and institutional sources, with
no documented coverage of non-standard orthography, code-switching with French or German, or
loanword alternation — all confirmed features of the target deployment's actual input
distribution [Q7, Q112]. The authors flag "ongoing standardisation of the language" and "vast
amounts of variation" as evaluation challenges [Q7], but the benchmark's preprocessing does
not address these properties. The intent detection source register further diverges from
citizen-correspondence form, using non-standard spelling conventions (all lowercase, missing
punctuation) that were difficult to render in LTZ [Q55].

### Output Ontology
The label ontology across all LTZGLUE tasks is entirely single-label and hard-classification
[Q84]. Binary tasks use True/False or 0/1 encodings [Q147, Q148, Q150, Q155]. Multi-class
tasks include three-class sentiment (positive, neutral, negative) [Q149], five-class linguistic
acceptability (correct, verb, adj, syntax, ortho) [Q151], five-class topic classification
(sports, culture, technology, business, animals) [Q153], a fixed set of reminder/alarm intents
[Q154], and BIO NER tags covering LOC, PER, DATE, ORG, and MISC [Q152]. The benchmark did not
use a multiple choice question answering setup, instead providing explicit label sets for output
[Q84].

For the deployment, the output ontology presents three critical misalignments. First, there
are no administrative, housing, cross-border worker, civic, or EU-institutional categories in
any task taxonomy. Second, all tasks emit single hard labels, whereas the deployment requires
multi-label outputs with calibrated confidence scores for routing — the benchmark produces no
probabilistic or ranked outputs. Third, the sentiment labels (positive/neutral/negative) are
generic and not calibrated to the formal-but-understated register of citizen-government
correspondence. The NER tag set was simplified by merging GPE and LOC into a single location
label [Q44], further reducing the administrative granularity available. The authors caution
against using "benchmark performance as evidence of cultural or demographic coverage" [Q121]
and advise inspecting task-specific subsets before deployment in public-facing settings [Q123].

### Output Content
Annotation practices vary substantially across tasks. The sentiment analysis task was annotated
by two native speakers of Luxembourgish [Q25], instructed to use an "unsure" category only
when they would otherwise assign labels randomly [Q26], yielding a Cohen's Kappa of 0.45 [Q27],
with disagreements resolved by annotator consensus [Q28]. The intent detection dataset was
translated by a single native LTZ speaker with consultation of additional speakers in ambiguous
cases [Q52]. The RTE dataset underwent a two-step LLM-based quality and label verification
process using ChatGPT-5-Mini [Q63, Q64], with manual correction of cases where automatic
improvement inadvertently altered logical contradictions [Q65]. The JUDGEWEL NER dataset relied
on LLMs as judges with minimal human verification [Q37], while the Lothritz et al. NER dataset
was fully human-annotated [Q42]. Annotator details are limited to a brief acknowledgement of
student assistants [Q114], without documentation of linguistic background or domain familiarity.

For the deployment, the annotation validity is a HIGH concern. The sentiment analysis Cohen's
Kappa of 0.45 [Q27] — moderate agreement from only two annotators — falls below standard
reliability thresholds. No annotators are documented as having familiarity with Luxembourgish
administrative communication norms or civil-service registers. The LLM-assisted label
verification for RTE [Q63, Q64] introduces uncertainty about whether labels reflect genuine
Luxembourgish linguistic norms. The authors acknowledge that "some annotation decisions and
class distributions are necessarily influenced by resource constraints" and that "automatic
preprocessing may introduce biases that we cannot fully quantify" [Q113], and flag that "models
may reproduce dominant norms while under-representing regional, sociolectal, or multilingual
practices" [Q120].

### Output Form
All tasks are evaluated using F1 scores [Q93, Q96]. Macro-F1 is reported for prompted LLMs
evaluated once; encoder-based models report averaged F1 over three runs with standard deviations
[Q96, Q89]. Class-balanced loss is applied during fine-tuning for imbalanced tasks [Q92].
Invalid or malformed LLM outputs are discarded prior to evaluation [Q90, Q91]. Hyperparameter
selection is performed via Bayesian search with early stopping, capped at 30 runs per
model-task combination [Q138], with best hyperparameters selected on the validation set [Q137].
Full results across validation and test sets are reported in appendix tables [Q156, Q158, Q159].

For the deployment, the output form dimension has a functional gap: the benchmark produces
single-label hard classifications evaluated with F1, while the deployment operationally requires
confidence-scored and multi-label outputs for routing and escalation logic. The zero-shot LLM
evaluation described [Q83, Q85] is methodologically relevant to the deployment but results
should be treated as indicative only due to prompt sensitivity [Q86, Q87]. The exclusive
reliance on single-label hard F1 scoring [Q84, Q93] means the benchmark provides no calibration
data for the confidence-scored outputs the deployment requires.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This paper presents LTZGLUE, the first Natural Language Understanding (NLU) benchmark for Luxembourgish (LTZ) based on the popular GLUE benchmark for English." |
| Q2 | 1 | input_ontology | "Our tasks include common natural language processing tasks in binary and multi-class classification settings, including named entity recognition, topic classification, and intent classification." |
| Q3 | 1 | output_form | "We evaluate various pre-trained language models for LTZ to present an overview of the current capabilities of these models on the LTZ language." |
| Q4 | 1 | input_ontology | "Small and under-researched languages are particularly difficult to evaluate, as is the case with Luxembourgish (LTZ), the national language of Luxembourg, with around 400k speakers." |
| Q5 | 1 | input_ontology | "LTZ only has a handful of NLU tasks available (Lothritz et al., 2022; Philippy et al., 2024; Plum et al., 2026)." |
| Q6 | 1 | input_content | "As most of these are in the news domain, and the majority of the down-stream tasks comprise less than a thousand instances, model evaluation is not always dependable." |
| Q7 | 1 | input_form | "Additional factors, such as the ongoing standardisation of the language (Gilles, 2019), vast amounts of variation (Lutgen et al., 2025), and decentralised resources, make it extremely challenging to evaluate LTZ language understanding in language models." |
| Q8 | 1 | input_ontology | "Our contributions are: (1) LTZGLUE: the first unified GLUE benchmark for LTZ, with 8 tasks." |
| Q9 | 1 | input_ontology | "(2) LTZ-E1 (mini/base): 2 new encoder language models for LTZ, which achieve competitive performance when fine-tuned on LTZGLUE." |
| Q10 | 1 | output_content | "Alistair Plum1, Felicia Körner2,3, Anne-Marie Lutgen1, Laura Bernardy1, Fred Philippy1, Emilia Milano1, Nils Rehlinger1, Cédric Lothritz4, Tharindu Ranasinghe5, Barbara Plank2,3, Christoph Purschke1 1University of Luxembourg, Luxembourg, 2LMU Munich, Germany 3Munich Center for Machine Learning, Germany 4LIST, Luxembourg, 5Lancaster University, UK" |
| Q11 | 2 | input_ontology | "In this section, we introduce the eight tasks for LTZGLUE. The set spans binary and multi-class sentence and token-level classification tasks. Together, these tasks cover a broad spectrum of linguistic and semantic phenomena and provide the first unified benchmark for evaluating LTZ NLP models." |
| Q12 | 2 | input_content | "Unless stated otherwise, the textual data used across most tasks stems from two main sources: (i)" |
| Q13 | 2 | input_ontology | "LTZ, the focus of this benchmark, is regarded as under-researched, and research is ongoing. Joshi et al. (2020) classify Luxembourgish as one of the "scraping-by" languages: although some unlabeled data exists, meaningful progress will require coordinated efforts to raise awareness and collect labeled datasets, as such resources are currently almost nonexistent." |
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
| Q43 | 4 | input_content | "The two datasets are merged to increase both coverage and domain balance." |
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
| Q57 | 5 | input_form | "After translating the dataset, we transferred the BIO tags by first using token-level fuzzy matching between the LTZ and the German dataset, followed by manual verification." |
| Q58 | 5 | output_ontology | "Table 5 shows the label distribution and size of each data split." |
| Q59 | 5 | input_ontology | "Recognizing Textual Entailment (RTE) (Haim et al., 2006) is a classic NLU task featured in the original GLUE benchmark. Given a pair of texts A and B, the task consists of determining whether A is a logical premise of B." |
| Q60 | 5 | input_content | "Lothritz et al. (2023) released a machine-translated Luxembourgish version of the dataset using Google Translate. However, due to numerous grammar and vocabulary related mistakes introduced in this process, we set out to improve the quality of the dataset." |
| Q61 | 5 | input_content | "Specifically, we first prompted CHATGPT-5.1 to assess and improve the translated sentence pairs unless they were already of very high quality, while explicitly keeping the original meaning to avoid label conflicts (see Appendix 7.4)." |
| Q62 | 5 | output_content | "In addition, we perform two verification steps to make sure that (a) the quality of the improved texts is high enough and (b) that the labels are correct." |
| Q63 | 5 | output_content | "To achieve (a), we prompted CHATGPT-5-MINI to judge the texts in the improved data and label their quality as either low, medium, or high, keeping only data rated at least medium, removing nearly 25% of the entire dataset (see Appendix 7.5)." |
| Q64 | 5 | output_content | "For (b), we prompted CHATGPT-5-MINI to verify whether the dataset labels remained correct after the first translation and improvement, outputting true or false for each sentence pair (see Appendix 7.6). Nearly 10% of the labels were false." |
| Q65 | 5 | output_content | "We found that the quality improvement step often corrected intentional logical contradictions or factual inaccuracies rather than keeping the original semantics. We therefore adjusted the sentences manually such that they corresponded to the ground truth again, while keeping false positives intact." |
| Q66 | 5 | input_content | "The filtering reduced between 22 and 28% of instances in the data, resulting in a final dataset of 1,876, 197, and 626 sentence pairs for the training, development, and test set, respectively." |
| Q67 | 5 | input_ontology | "Together, the eight tasks in LTZGLUE form a broad and balanced evaluation suite, covering four binary and four multi-class settings, sentence- and document-level inputs, as well as a token-level sequence-labelling task." |
| Q68 | 5 | input_ontology | "Despite the low-research status of LTZ, this places LTZGLUE in the same general range as the original English GLUE benchmark, which comprises nine diverse NLU tasks (Wang et al., 2019b)." |
| Q69 | 5 | input_content | "In addition, a substantial proportion of the LTZGLUE tasks are newly created for LTZ rather than direct translations or simple repackaging, allowing the benchmark to reflect phenomena and usage patterns specific to the language." |
| Q70 | 6 | input_ontology | "In this landscape, supporting eight tasks for LTZ, including token-level NER and several newly constructed text-level tasks, is a strong indicator of the maturity and breadth of the emerging LTZ NLP ecosystem." |
| Q71 | 6 | input_ontology | "This design allows us to assess current LTZ NLU performance across fundamentally different modelling paradigms, while maintaining a clear separation between task-specific supervision and general-purpose language understanding." |
| Q72 | 6 | output_form | "We train two encoder language models for LTZ: LTZ-E1-mini with 68M and LTZ-E1-base with 110M non-embedding parameters." |
| Q73 | 6 | output_form | "We closely follow the Ettin recipe (Weller et al., 2026), which is based on MODERNBERT (Warner et al., 2025)." |
| Q74 | 6 | input_content | "The pre-training set is compiled from a variety of sources of LTZ. A large portion of the data stems from RTL (see Section 3), including news articles (News), transcribed radio interviews (Radio), and user comments (Comments). We also include transcribed podcasts (Podcasts) and transcribed political speeches and debates from the Chambre des Députés (Chamber). In addition, we use 1M sentences from the web crawl of the Leipzig Collection (Web, this excludes RTL), text crawled from LTZ chat rooms (Webchat), a Wikipedia crawl from October 2023 (Wikipedia), and finally, example sentences from the LOD retrieved in March 2024." |
| Q75 | 6 | input_form | "We filter out sentences containing fewer than three words (as tokenized by whitespace), totalling 11.7M sentences, which corresponds to roughly 233M tokens using our tokenizer." |
| Q76 | 6 | input_ontology | "We evaluate a set of supervised encoder-based models that explicitly support LTZ, either through direct pre-training or multilingual coverage." |
| Q77 | 6 | output_form | "As a representative baseline, we include multilingual BERT (MBERT-base) (Devlin et al., 2019), which still remains widely used for multilingual transfer and low-resource evaluation." |
| Q78 | 6 | output_form | "We additionally evaluate a more recent multilingual BERT (MMBERT-base) variant with updated pre-training data and tokenisation." |
| Q79 | 6 | output_form | "To complement these general-purpose multilingual models, we include LUXEMBERT, a language-specific model trained on LTZ data (Lothritz et al., 2022), which provides a stronger inductive bias for the language's lexical and orthographic properties." |
| Q80 | 6 | output_form | "Finally, we evaluate XLM-RoBERTa (XLM-R-base) (Conneau et al., 2020), a large-scale multilingual model trained on substantially more data and languages than MBERT-base, and commonly used as a strong reference point for multilingual NLU." |
| Q81 | 6 | output_form | "In addition to supervised encoder-based models, we evaluate a set of LLMs in a prompt-based zero-shot setting. This group includes QWEN3-235B, LLAMA-3.3, GEMMA-3-27B, and GPT5-MINI, which represent a range of model sizes, training regimes, and degrees of multilingual coverage." |
| Q82 | 6 | output_content | "None of these models are fine-tuned on LTZGLUE, although some of the text data (RTL, Wikipedia) is very likely to have been processed during training." |
| Q83 | 6 | output_form | "The models are evaluated using prompts that describe each task, allowing us to assess their ability to generalise to LTZ without task-specific supervision." |
| Q84 | 6 | output_ontology | "We did not use a Multiple Choice Question Answering (MCQA)-setup, but provided the labels that should be used as output." |
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
| Q111 | 9 | output_content | "In addition, some of the data sources used in this benchmark may already be included, in whole or in part, in the pre-training corpora of the large language models evaluated in this work. While the exact composition of proprietary pre-training datasets is typically not fully disclosed, this potential overlap cannot be entirely ruled out and may inflate performance estimates." |
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
| Q126 | 12 | output_form | "We train two sizes of LTZ-E1 models, mini and base, with 68M and 110M non-embedding parameters, respectively." |
| Q127 | 12 | output_form | "LTZ-E1-mini has 19 hidden layers, a hidden size of 512, an intermediate size of 768, and 8 attention heads, whereas LTZ-E1-base has 22 hidden layers, a hidden size of 768, an intermediate size of 1152, and 12 attention heads." |
| Q128 | 12 | input_form | "Both models share a GPTNeoXTokenizerFast tokenizer (Black et al., 2022), a BPE-based tokenizer, which we train on the entire pre-training set, using a minimum frequency of two and a vocabulary size of 50,368." |
| Q129 | 12 | input_form | "We use a constant batch size of 1024 packed sequences, where both models have a max sequence length of 1024." |
| Q130 | 12 | output_form | "We follow ModernBERT (Warner et al., 2025) and Ettin (Weller et al., 2026) in using the Warmup-Stable-Decay (WSD) scheduler (Zhai et al., 2022; Hu et al., 2024), though we use a shorter warmup and decay phase of 500 batches each, due to our smaller pre-training dataset size and larger number of epochs (10 vs. one)." |
| Q131 | 12 | output_form | "Again following ModernBERT and Ettin's recipe, we use the StableAdamW optimizer (Wortsman et al., 2023), with a peak learning rate of 3e-3 with a weight decay of 3e-4 for LTZ-E1-mini and 8e-4 with a weight decay of 1e-5 for LTZ-E1-base." |
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
| Q145 | 14 | output_ontology | "You are an expert for the Luxembourgish language. I am giving you two texts TEXT1 and TEXT2 in Luxembourgish as well as a LABEL where 1 means that TEXT1 logically entails TEXT2 while 0 means the opposite. You have to check if the labels are correct. As output, simply write 'true' if the label is the correct one or 'false' if the label is incorrect." |
| Q146 | 14 | output_ontology | "You are a classification and text-processing model specialized in NLP tasks for Luxembourgish (lb). Follow ALL rules strictly: 1. Respond ONLY in valid JSON. 2. Do NOT add explanations, comments or text outside of JSON. 3. Use field: "output": <model_answer>. 4. Use field: "task": "<task_name>". 5. Use field: "input": "<input example text>". 6. Predict only the requested outputs and" |
| Q147 | 15 | output_ontology | "If determined labels are 0 and 1 then 0 is used for False, 1 is used for True." |
| Q148 | 15 | output_ontology | "headline_classification: Decide if the given title/headline fits the text. Output True or False." |
| Q149 | 15 | output_ontology | "sentiment_analysis: Classify sentiment of the text. Allowed labels: positive, neutral, negative." |
| Q150 | 15 | output_ontology | "linguistic_acceptability_binary: Decide whether the sentence is linguistically acceptable in Luxembourgish. Output: 0 or 1." |
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
abbreviation: LU-CIVSERV
deployment_context:
  country: Luxembourg
  governance_levels:
  - national (État)
  - communal (communes)
  eu_institutional_dimension: Luxembourg hosts major EU institutions (European Court
    of Justice, European Commission DGs, European Parliament secretariat); EU-institutional
    topic categories are operationally relevant to citizen correspondence routing.
  system_purpose: LLM-based automatic classification of citizen feedback by topic,
    named entity detection, intent identification, and sentiment/urgency gauging to
    drive automated routing to government departments and prioritization of correspondence,
    with human-in-the-loop fallback for low-confidence outputs.
target_population:
  primary_users: Civil servants in Luxembourgish government agencies at national and
    communal levels who process, review, and act on digitally routed citizen correspondence.
    They are the direct consumers of the system's classification outputs and the human
    auditors in the escalation loop.
  secondary_users: 'Citizens and residents of Luxembourg submitting feedback or queries
    to government agencies in written digital form. Their messages constitute the
    system''s primary text input. This population includes:

    - Luxembourgish nationals

    - Long-term residents holding Luxembourg nationality or permanent residency

    - Cross-border workers (frontaliers) who commute daily from France, Germany, or
    Belgium and are subject to distinct tax, social security, and labor frameworks

    - EU nationals resident in Luxembourg under freedom-of-movement provisions

    - Third-country nationals with various residency statuses'
  cross_border_worker_subpopulation:
    description: A demographically significant subpopulation of workers residing in
      neighboring countries (primarily France, Belgium, Germany) who cross into Luxembourg
      daily for employment. They generate a distinct class of administrative queries
      relating to frontier-worker tax treaties, cross-border social security coordination,
      healthcare access, and commuter transport.
    estimated_workforce_share: '47% of Luxembourg''s employed workforce (approximately
      216,000–228,000 individuals out of ~489,000 total employees in 2024). Source:
      STATEC Regards 01/25 — [WEB-1];
      corroborated by ODT/LISER Maps and Figures 2023 — [WEB-2]'
    primary_origin_countries:
    - France (~52–53% of cross-border workers)
    - Belgium (~23–24% of cross-border workers)
    - Germany (~23–24% of cross-border workers)
    relevant_administrative_domains:
    - frontier-worker income tax treaties
    - cross-border social security (détachement, affiliation)
    - cross-border healthcare reimbursement
    - commuter transport and rail passes
    - childcare allocation portability
geography:
  country: Luxembourg
  area_km2: 2,586 km² (Luxembourg official government portal — [WEB-3];
    corroborated by multiple sources including alphatrad.co.uk — [WEB-4])
  population: '672,050 as of 1 January 2024; 681,973 as of 1 January 2025 (+1.5% year-on-year).
    Source: STATEC official population statistics — [WEB-5];
    [WEB-6]'
  administrative_divisions:
    description: Luxembourg is divided into communes (municipalities), grouped historically
      into cantons and districts. Responsibility for administrative services is split
      between the national state and individual communes, creating a routing challenge
      the system must resolve.
    number_of_communes: 'Exactly 100 communes, following the mergers of Bous–Waldbredimus
      and Grosbous–Wahl which took effect on 1 September 2023. Source: Luxembourg
      Government official communiqué — [WEB-7];
      confirmed by Luxembourg official elections portal — [WEB-8]'
    state_vs_communal_competency_examples:
      state_competencies:
      - national identity documents (passeport, carte d'identité)
      - income tax
      - social security (CNAP, CNS, CCSS)
      - national police
      - immigration and residency permits
      - labor law enforcement (ITM)
      - EU treaty obligations
      communal_competencies:
      - local urban planning and construction permits
      - communal taxes (taxe foncière)
      - local road maintenance
      - communal social services
      - waste management
      - local event permits
      - birth/death/marriage registration at état civil
  eu_institutional_presence: Luxembourg City hosts the Court of Justice of the European
    Union, the General Court, the European Court of Auditors, the European Investment
    Bank, and multiple European Commission and Parliament administrative bodies. Citizens
    may conflate national and EU-institutional contacts in correspondence.
  cross_border_catchment_regions:
    France: 'Primarily Moselle department (Thionville area, where ~half of French
      cross-border workers reside) and Meurthe-et-Moselle. Source: ODT/LISER employment/mobility
      study 2023 — [WEB-2];
      Paperjam cross-border worker analysis — [WEB-9]'
    Belgium: 'Primarily Province de Luxembourg (Arlon/Gaume region); ~73% of Belgian
      cross-border workers reside in Province de Luxembourg. Source: Paperjam/ASTI
      cross-border worker study — [WEB-9]'
    Germany: 'Primarily Trier region; ~half of German cross-border workers live in
      or around Trier. Source: Paperjam/ASTI cross-border worker study — [WEB-9]'
languages:
  official_languages:
  - Luxembourgish (Lëtzebuergesch)
  - French
  - German
  national_language: Luxembourgish (Lëtzebuergesch / LTZ) — the sole national language
    and primary spoken vernacular of Luxembourgish citizens
  administrative_language_practice: French dominates written administrative law and
    formal government correspondence; German is used in some administrative contexts
    and is the language of instruction in early primary education; Luxembourgish is
    increasingly used in informal and semi-formal government digital channels.
  deployment_target_language: Luxembourgish (lb) — the benchmark (LTZGLUE) and the
    system both target LTZ as the primary processing language.
  code_switching_profile:
    description: Citizens composing digital feedback in Luxembourgish habitually alternate
      between French-derived and German-derived lexical variants for the same administrative
      concepts, and may embed entire French or German phrases within an otherwise
      Luxembourgish message.
    documented_examples:
    - Administratioun (French-derived) vs. Verwaltung (German-derived) for 'administration'
    - Formulaire (French) vs. Formular (German) for 'form'
    - Bréif (Luxembourgish) vs. lettre (French) for 'letter'
    orthographic_variation: Luxembourgish orthographic standardization (Eis Sprooch
      reform and predecessor conventions) is ongoing and unevenly adopted. Citizens
      may apply idiosyncratic or older spelling conventions. No assumption of standard
      OLO (Offiziell Lëtzebuerger Orthografie) compliance is warranted for citizen
      input.
  resident_non_ltz_speaker_fraction: '~47.3% of Luxembourg''s population as of 1 January
    2024 are foreign nationals. The largest group are Portuguese nationals (~14.5%
    of total population, ~92,000–94,000 individuals as of 2023–2024). The CIA World
    Factbook (2021 est.) reports Luxembourgish as first language for 48.9% of residents,
    Portuguese for 15.4%, French for 14.9%, Italian 3.6%, English 3.6%, German 2.9%,
    other 10.8%. A significant share of residents primarily write in French or Portuguese
    rather than Luxembourgish. Source: STATEC population statistics — [WEB-5];
    World Factbook Luxembourg demographics — [WEB-10];
    Wikipedia Portuguese in Luxembourg — [WEB-11]'
  portuguese_community_note: 'Luxembourg has a very large Portuguese-origin resident
    community (~14.5% of total population, ~93,659 Portuguese nationals as of January
    2023, the single largest foreign nationality group). Portuguese is described as
    the second most spoken primary language after Luxembourgish. Their written administrative
    correspondence is likely in French or Portuguese rather than Luxembourgish and
    falls outside the LTZ benchmark scope, but will appear in the deployment input
    stream. Source: Portuguese in Luxembourg Wikipedia — [WEB-11];
    Luxembourg demographics portal — [WEB-3]'
  benchmark_language_note: LTZGLUE processes only Luxembourgish (lb) text; non-Luxembourgish
    content was filtered during benchmark construction using OpenLID. Deployment inputs
    that are French-only or German-only will not be validly classified by a model
    calibrated on LTZGLUE alone.
writing_systems:
  script: Latin alphabet with diacritics used in Luxembourgish (é, ë, ä, etc.)
  directionality: left-to-right
  citizen_orthographic_variance: Citizens may omit diacritics, apply inconsistent
    capitalization (Luxembourgish capitalizes all nouns as in German), and use phonetic
    approximations. Preprocessing pipelines must not over-normalize, as variation
    is meaningful for dialect and register detection.
  nls_note: No right-to-left script considerations; no script-mixing concerns beyond
    Latin diacritics.
demographic_and_literacy_profile:
  general_literacy_rate: '[NEEDS VERIFICATION — deferred: below search budget; Luxembourg''s
    general adult literacy is near-universal by all EU benchmarks but a specific authoritative
    percentage was not retrieved in this pass]'
  digital_literacy_among_civil_servants: Civil servants are the direct users of classification
    outputs, not the text authors; high digital literacy is assumed for this subgroup
    given Luxembourg's advanced e-government infrastructure.
  citizen_digital_literacy: 'Luxembourg consistently ranks among the top EU member
    states in digital skills (DESI). The 2024 DESI analysis identifies Luxembourg
    as among the top three EU countries for ICT specialists as a share of employment
    (8.0%, behind only Sweden at 8.7%), indicating a highly digitally skilled workforce.
    The standalone DESI ranking was discontinued after 2022 and integrated into the
    State of the Digital Decade report from 2023 onwards. Source: DESI 2024 analysis
    — [WEB-12]; EC DESI Luxembourg profile — [WEB-13]'
  internet_penetration: '~99% of Luxembourg households had internet access in 2023,
    one of the highest rates in the EU. Urban household access reached ~99.9%, rural
    household access ~98.3% — both figures among the highest in the EU. Source: Eurostat
    ICT Household Survey 2023 via Statista — [WEB-14];
    Eurostat Urban-Rural Digital Society analysis — [WEB-15]'
  mobile_internet_penetration: '[NEEDS VERIFICATION — deferred: below search budget;
    Luxembourg is consistently a top EU performer in broadband and mobile connectivity
    per DESI data, but a specific 2023/2024 mobile internet penetration percentage
    was not retrieved in this pass]'
  language_skills_in_population: The majority of Luxembourg residents are functionally
    multilingual (Luxembourgish, French, German). Trilingualism is institutionally
    embedded through the educational system. Cross-border workers may be monolingual
    French or German speakers.
  educational_system_note: Luxembourg's educational system uses Luxembourgish as initial
    instruction language, transitioning to German then French. This produces a specific
    pattern of multilingual competence in citizens educated domestically that differs
    from the competence profile of recently arrived residents or cross-border workers.
infrastructure_notes:
  digital_government_maturity: 'Luxembourg has consistently ranked among the top EU
    member states in e-government maturity. It ranked 5th in the DESI 2017 composite
    index and has been described as ''one of the leading countries for connectivity,
    digital skills and Internet usage.'' The standalone DESI index was replaced from
    2023 by the State of the Digital Decade monitoring framework; Luxembourg remains
    a top-tier performer. Source: EC DESI Luxembourg country profile — [WEB-13]'
  key_digital_platforms:
    myguichet: 'MyGuichet.lu — Luxembourg''s primary online administrative portal
      for citizen-government interaction; likely a major channel for digital correspondence
      captured by this deployment. [NEEDS VERIFICATION — deferred: low impact for
      scoring; specific confirmation that MyGuichet.lu is in scope for this deployment
      requires internal deployment documentation not publicly available]'
    government_portal: 'gouvernement.lu [NEEDS VERIFICATION — deferred: low impact
      for scoring; confirmation that gouvernement.lu citizen feedback channels feed
      into this deployment requires internal documentation]'
  connectivity:
    broadband_infrastructure: 'Luxembourg leads EU in Very High Capacity Network (VHCN)
      coverage (≥90% per DESI 2020 data), and internet access across all settlement
      types is near-universal (~99% overall, ~98.3% rural in 2023). Source: DESI 2020
      European analysis — [WEB-16];
      Eurostat 2023 — [WEB-15]'
    mobile_network_coverage: '[NEEDS VERIFICATION — deferred: below search budget;
      Luxembourg is a consistent top performer in EU mobile connectivity benchmarks
      but a specific 4G/5G population coverage figure was not retrieved in this pass]'
  text_processing_environment: Text-only deployment; no audio, image, or multimodal
    input handling required. Inputs arrive as structured digital messages from e-government
    portals.
  system_architecture_note: Multi-label classifier with confidence scoring and human-escalation
    fallback. LTZGLUE emits only single hard labels; the deployment requires model-level
    adaptation beyond benchmark format — specifically calibrated probability outputs
    and multi-label decoding.
administrative_domain_profile:
  topic_taxonomy_requirements:
    description: The routing system requires a Luxembourg-specific administrative
      topic taxonomy that LTZGLUE does not provide. The following categories are deployment-critical
      and absent from LTZGLUE's five-class RTL news taxonomy (SPORTS, CULTURE, TECHNOLOGY,
      BUSINESS, ANIMALS).
    required_topic_categories:
    - category: Cross-border worker / frontalier status
      priority: HIGH
      notes: '47% of Luxembourg''s workforce (489,000 employees, 2024 STATEC); generates
        distinct query types around frontier-worker tax treaties, social security
        affiliation, healthcare portability. LTZGLUE: FULL GAP. Source: STATEC — [WEB-1]'
    - category: Housing and rental market
      priority: HIGH — politically sensitive
      notes: Housing affordability is documented as a major societal challenge in
        Luxembourg, with households spending on average 21.54% of expenditure on housing,
        water, electricity, gas and fuel (STATEC Luxembourg in Figures 2024 — [WEB-17]).
        High cost of living and housing scarcity are widely cited drivers of cross-border
        worker commuting (OECD Economic Survey Luxembourg 2025 — [WEB-18]).
        Housing is a confirmed high-volume citizen concern.
    - category: Cost of living and consumer prices
      priority: HIGH — politically sensitive
      notes: 'Luxembourg has the second-highest median hourly wage in the EU (€24,
        STATEC 2025) but among the highest costs of living; housing expenditure alone
        averages 21.54% of household spending. Cost-of-living and wage-indexation
        queries are a persistent theme in citizen-government interaction. Source:
        STATEC Regards 01/25 — [WEB-1]'
    - category: National identity and residency documents
      priority: HIGH
      notes: Passeport, carte d'identité, certificat de résidence — national state
        competency (Ministère des Affaires étrangères). État civil (births, deaths,
        marriages) is handled at communal level but governed by national law, creating
        a routing ambiguity.
    - category: Income tax and fiscal matters
      priority: HIGH
      notes: 'Administration des contributions directes. Distinct sub-categories for
        residents vs. non-resident frontaliers. Bilateral double taxation agreements
        (DTAs) with France, Belgium, Germany are directly relevant; the 34-day remote
        work threshold under these DTAs is an active policy concern for frontaliers.
        Source: OECD Economic Survey Luxembourg 2025 — [WEB-18]'
    - category: Social security and health insurance
      priority: HIGH
      notes: 'CNS, CNAP, CCSS — national competency. Cross-border healthcare reimbursement
        for frontaliers is a distinct sub-category. Frontaliers generally pay social
        security in Luxembourg but with some benefit portability distinctions. Source:
        Expatica cross-border worker guide — [WEB-19]'
    - category: Urban planning and construction permits
      priority: MODERATE
      notes: Communal competency; routing must identify the relevant commune out of
        100 communes.
    - category: Transport and mobility
      priority: MODERATE
      notes: 'Luxembourg introduced free public transport on 1 March 2020 (effective
        29 February 2020), becoming the first country in the world to do so — buses,
        trains (2nd class), and trams are fare-free; first-class train travel retains
        a fare. Policy remains in force as of 2025. Cross-border tickets are reduced-price
        but not free. This policy generates ongoing citizen queries about eligibility,
        cross-border fares, and service changes. Source: Official Luxembourg government
        transport portal — [WEB-20];
        Mobiliteit.lu fares page — [WEB-21]'
    - category: EU institutional matters
      priority: MODERATE
      notes: Citizen messages may erroneously address national government for EU-institution
        matters or vice versa. Routing system needs a redirect/triage category.
    - category: Labor law and employment
      priority: MODERATE
      notes: Inspection du Travail et des Mines (ITM) — national competency.
    - category: Education and childcare
      priority: MODERATE
      notes: Childcare allocation (chèque-service accueil) is state-managed; school
        enrollment may be communal. Routing split between national and communal for
        specific sub-tasks requires domain knowledge not present in LTZGLUE.
    - category: Immigration and naturalization
      priority: MODERATE
      notes: Direction de l'immigration — national competency.
  state_vs_communal_routing:
    description: A primary routing challenge is distinguishing whether a citizen message
      concerns a national-state competency or a communal competency. No existing NLU
      benchmark encodes this distinction. It requires Luxembourg-specific administrative
      knowledge not present in LTZGLUE.
    ambiguous_boundary_cases:
    - État civil (births, marriages, deaths) — performed by communes but governed
      by national law
    - Social housing — involves both national policy (SNHBM) and communal implementation
    - Road infrastructure — national vs. communal road network split
    benchmark_coverage: FULL GAP — LTZGLUE contains no administrative jurisdiction
      categories of any kind.
  sentiment_and_urgency_norms:
    description: Luxembourgish administrative communication culture is characterized
      by formal, understated expression even when citizens are frustrated or distressed.
      Sentiment classifiers trained on general-purpose or media-domain data will systematically
      underestimate negative sentiment and urgency in citizen correspondence.
    known_benchmark_gap: LTZGLUE sentiment annotation used two native speakers (Cohen's
      Kappa 0.45) annotating RTL commentary/letters-to-editor. No civil-service or
      administrative-correspondence register was included. Annotator familiarity with
      formal civil communication norms is undocumented.
    implications_for_prioritization: The deployment uses sentiment/urgency outputs
      for correspondence prioritization. Underdetection of frustration could cause
      genuinely urgent messages to be deprioritized. The human-in-the-loop audit mechanism
      is critical to recalibrate this progressively.
    cultural_communication_notes: Citizens may express severe dissatisfaction through
      understatement, formal complaint procedures, or legalistic framing rather than
      explicit negative sentiment markers. Urgency may be signaled indirectly through
      references to deadlines, legal rights, or administrative timelines rather than
      emotional language.
legal_and_regulatory_framework:
  data_protection:
    applicable_regulation: EU General Data Protection Regulation (GDPR) — Regulation
      2016/679
    national_implementation: 'Law of 1 August 2018 on the organization of the Commission
      nationale pour la protection des données (CNPD) and the general data protection
      regime. CNPD serves as national supervisory authority. Source: regulations.ai
      Luxembourg AI overview — [WEB-22];
      CMS Expert Guide — [WEB-23]'
    ai_act_considerations: 'Luxembourg is directly subject to EU AI Act (Regulation
      (EU) 2024/1689). Automated public-sector correspondence routing that affects
      service access is likely classifiable as high-risk AI under Annex III (public
      administration provisions). Draft national implementation Bill 8476 was submitted
      to Parliament on 23 December 2024 and designates CNPD as the default market
      surveillance authority and single point of contact for AI Act matters. Most
      high-risk AI obligations apply from August 2026; prohibited AI practices bans
      and AI literacy requirements apply from 2 February 2025. Source: CMS Expert
      Guide Luxembourg AI — [WEB-23];
      Pinsent Masons AI Act enforcement — [WEB-24];
      Arendt bill analysis — [WEB-25];
      CNPD AI Act obligations 2025 — [WEB-26]'
  administrative_law:
    primary_framework: '[NEEDS VERIFICATION — deferred: below search budget; Luxembourg
      administrative procedure law (loi du 1er décembre 1978 and subsequent reforms)
      governs automated administrative decision-support; specific current statutes
      require expert legal review rather than web search]'
    automated_decision_constraints: 'Automated routing that affects citizen rights
      or service access may be subject to administrative law requirements for transparency,
      contestability, and human review. The system''s human-in-the-loop fallback is
      directly relevant to compliance. Under EU AI Act Article 4, deployers must ensure
      staff have sufficient AI literacy; compliance obligations for high-risk AI systems
      (Article 26) include human oversight, data quality checks, and incident logging
      — applicable from August 2026. Source: CNPD AI mastery obligations — [WEB-27]'
    language_rights: '[NEEDS VERIFICATION — deferred: below search budget; Luxembourg
      language law of 24 February 1984 (loi sur le régime des langues) governs which
      languages may be used in administrative correspondence; specific provisions
      require expert legal review]'
  cross_border_worker_legal_framework:
    tax_treaties: 'Bilateral double taxation agreements (DTAs) between Luxembourg
      and France, Belgium, and Germany govern frontalier taxation. A key current provision:
      under these DTAs, the threshold for remote work from abroad is 34 working days
      per year; exceeding this threshold shifts taxation to the country of residence
      rather than Luxembourg. This is an active policy concern generating citizen
      queries. Source: OECD Economic Survey Luxembourg 2025 — [WEB-18];
      Expatica cross-border worker guide — [WEB-19]'
    social_security_coordination: 'EU Regulation 883/2004 on coordination of social
      security systems — governs which country''s social security applies to cross-border
      workers. Most frontaliers pay social security in Luxembourg. A1 certificate
      arrangements apply for seconded workers (up to 2-year maximum). Source: Expatica
      cross-border worker guide — [WEB-19]'
    healthcare: '[NEEDS VERIFICATION — deferred: below search budget; cross-border
      healthcare directive 2011/24/EU implementation and CNS reimbursement procedures
      for frontaliers require specialist review of CNS administrative documentation]'
  free_public_transit:
    policy_description: Luxembourg abolished fares on all public transport nationally
      (buses, trains 2nd class, trams) for all users including tourists. First-class
      train travel retains fares. Cross-border tickets are reduced-price but not free
      (Luxembourg portion is free; foreign-country portion remains payable).
    implementation_date: '1 March 2020 (effective from 29 February 2020). Policy remains
      fully in force as of 2025 with no rollback. Extended tram network and new routes
      added post-2020. Source: Official Luxembourg transport FAQ — [WEB-20];
      Official Luxembourg government portal — [WEB-28];
      Luxembourg Embassy Washington announcement — [WEB-29]'
    relevance: Generates a distinct class of citizen queries; routing category for
      Mobilité (CFL, RGTR, Luxtram operators vs. Ministère de la Mobilité et des Travaux
      publics). Cross-border commuter queries about fare reductions on cross-border
      segments are a related sub-category.
benchmark_validity_concerns_for_this_population:
  input_ontology_gap:
    severity: CRITICAL
    summary: LTZGLUE topic taxonomy (5 RTL news categories) and intent taxonomy (voice-assistant
      reminder/alarm commands) share zero overlap with the deployment's required administrative
      routing categories. The benchmark cannot be used as a direct proxy for topic
      classification performance in this deployment context.
    recommended_investigation: '[NOT FOUND — searched for Luxembourgish civic/administrative
      NLP dataset that could supplement LTZGLUE for topic coverage; no such dataset
      was identified. The LTZGLUE benchmark paper itself (Q5, Q6) notes only a handful
      of LTZ NLU tasks exist (Lothritz et al. 2022; Philippy et al. 2024; Plum et
      al. 2026), none in the administrative domain. This confirms a genuine documentation
      gap for LTZ civic NLP, not a search failure.]'
  output_format_gap:
    severity: CRITICAL
    summary: All LTZGLUE tasks emit single hard labels. The deployment requires multi-label
      classification with calibrated confidence scores. No adaptation path exists
      within the current benchmark format.
    recommended_investigation: '[NEEDS VERIFICATION — deferred: likely unsearchable
      (requires inspection of LTZGLUE code repository or author contact to confirm
      whether evaluation scripts expose logit/probability outputs); no publicly available
      LTZGLUE documentation of probabilistic scoring was found in this pass]'
  input_content_register_gap:
    severity: HIGH
    summary: LTZGLUE data sources are predominantly formal (RTL news, parliamentary
      speeches, Wikipedia, LOD dictionary). Citizen correspondence is colloquial,
      code-switched, and orthographically variable. The partial exception — Lothritz
      et al. NER corpus from RTL news comments — covers informal register in a narrow
      slice of the benchmark.
    recommended_investigation: '[NOT FOUND — no separate Luxembourgish informal/code-switched
      citizen correspondence corpus was identified in searches. This is consistent
      with the LTZGLUE paper''s own acknowledgment (Q112) that ''most data sources
      reflect formal writing or institutional usage.'' The absence confirms the gap
      rather than indicating an undiscovered resource.]'
  annotator_provenance_gap:
    severity: HIGH
    summary: Sentiment annotators are identified only as two native LTZ speakers (Cohen's
      Kappa 0.45). No documentation of familiarity with civil administrative communication
      norms. Student assistants are acknowledged without further background detail.
    recommended_investigation: '[NEEDS VERIFICATION — deferred: not searchable via
      web; requires direct contact with LTZGLUE authors (University of Luxembourg)
      or inspection of supplementary materials for annotator recruitment criteria,
      residency, and occupation]'
  benchmark_size_and_coverage:
    severity: MODERATE
    summary: Low-resource benchmark with small per-task dataset sizes. Rare administrative
      sub-topics (e.g., EU institutional queries, frontalier-specific matters) are
      entirely absent as categories and cannot be assessed for coverage adequacy.
    recommended_investigation: '[NEEDS VERIFICATION — deferred: below search budget;
      per-task test set sizes are reported in LTZGLUE appendix tables (Q156, Q158,
      Q159); requires access to the paper''s appendix to extract exact figures]'
  llm_label_contamination:
    severity: MODERATE
    summary: RTE labels verified by ChatGPT-5-Mini; JUDGEWEL NER labels generated
      with LLM judges and minimal human verification. LLM-induced label artifacts
      may not reflect genuine Luxembourgish administrative or legal linguistic norms.
    recommended_investigation: '[NEEDS VERIFICATION — deferred: below search budget;
      proportion of NER and RTE test data from LLM-annotated vs. human-annotated sources
      requires inspection of LTZGLUE appendix tables and JUDGEWEL dataset documentation]'
cultural_norms_notes: 'Luxembourg''s administrative culture reflects the country''s
  trilingual institutional history and its position as both a small nation-state and
  a major EU hub. Key norms relevant to this deployment:

  - Civil communication with government is traditionally formal and legalistic, even
  in digital channels.

  - Citizens expect responses in the language they wrote in (Luxembourgish, French,
  or German), with French dominant in formal administrative correspondence.

  - Cross-border workers have a distinct civic identity and distinct administrative
  needs; their messages may reference French or German administrative concepts by
  habit.

  - Luxembourg''s high cost of living and housing scarcity generate politically charged
  correspondence that requires careful urgency/frustration calibration.

  - The country''s EU identity means citizens sometimes conflate national and supranational
  administrative channels.

  - Understatement and formal complaint framing may mask genuine urgency or frustration
  in citizen messages — a critical consideration for the sentiment/prioritization
  subsystem.

  - The Portuguese-origin community (~14.5% of total population, ~93,659 Portuguese
  nationals as of January 2023, the largest single foreign nationality group — source:
  Wikipedia Portuguese in Luxembourg — [WEB-11];
  migration policy — [WEB-30])
  primarily interacts in French rather than Luxembourgish, creating a population segment
  whose correspondence may fall outside the LTZ model''s coverage.'
domain_specific_operational_notes:
  routing_architecture: The system routes messages to specific government departments
    and differentiates between national and communal authority levels. A single message
    may legitimately require multi-label routing (e.g., a housing query involving
    both communal urban planning and national social housing allocation). The human-in-the-loop
    fallback handles low-confidence and boundary cases.
  high_stakes_decisions: 'Automated routing in a public administration context constitutes
    a high-stakes application: misrouting delays citizen service delivery, and misclassification
    of urgency/frustration can cause harm through deprioritization of urgent cases.
    Assessment must weight error asymmetries — the cost of missing an urgent/frustrated
    message is higher than the cost of over-escalating to human review.'
  progressive_calibration: 'The deployment includes a civil servant feedback mechanism
    to progressively align model outputs with actual administrative norms. This is
    a critical mitigation for the benchmark''s annotator provenance and sentiment
    calibration gaps, but its effectiveness depends on sufficient volume and diversity
    of civil servant feedback over time. [NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice / internal deployment design); feedback loop mechanism design
    and calibration timeline require internal deployment documentation]'
  luxembourgish_language_standardization: 'The ongoing OLO (Offiziell Lëtzebuerger
    Orthografie) standardization effort affects how Luxembourgish is written in both
    citizen messages and reference data. The benchmark was constructed largely before
    or during early adoption periods. Assessment should account for potential orthographic
    drift between benchmark data and current citizen writing conventions. [NEEDS VERIFICATION
    — deferred: below search budget; OLO adoption timeline and current status require
    specialist linguistic sources not retrieved in this pass]'
net_new_fields:
  ai_act_timeline_note: 'Under EU AI Act (Reg. 2024/1689), the deployment is likely
    classifiable as high-risk AI (Annex III, public administration automated decision-support).
    Key compliance timeline: prohibited AI practices ban and AI literacy (Article
    4) obligations in force since 2 February 2025; high-risk AI notification and general-purpose
    AI model obligations from August 2025; full high-risk AI system obligations from
    August 2026. Luxembourg''s national implementing bill (No. 8476, submitted December
    2024) designates CNPD as the default market surveillance authority. Source: CNPD
    AI Act obligations article — [WEB-26];
    Pinsent Masons — [WEB-24]'
  remote_work_dta_threshold: 'The bilateral DTAs between Luxembourg and France, Belgium,
    and Germany currently set a 34-working-day annual threshold for remote work from
    abroad before taxation shifts to the country of residence. This is a high-salience
    administrative topic for cross-border workers that will generate citizen correspondence
    to tax and labor authorities; it should be included as a routing sub-category
    within the frontalier/income-tax topic class. Source: OECD Economic Survey Luxembourg
    2025 — [WEB-18]'
  portuguese_language_as_second_spoken_language: 'Portuguese is the second most spoken
    primary language in Luxembourg after Luxembourgish (~15.4% of residents per 2021
    CIA World Factbook estimate), ahead of French (~14.9%), reflecting the size of
    the Portuguese community. This means a material share of citizen correspondence
    arriving at government portals may be in Portuguese — a language entirely outside
    the LTZGLUE benchmark scope and outside the three official languages. Source:
    World Factbook Luxembourg — [WEB-10];
    Luxembourg public demographics page — [WEB-3]'
  luxembourg_employment_ratio_context: 'Luxembourg recorded nearly 500,000 jobs in
    2023, yielding an employment-to-population ratio of 0.76 — the highest among European
    countries excluding Monaco. This extreme ratio (workforce substantially larger
    than resident population due to frontaliers) is directly relevant to the deployment:
    a large fraction of citizen correspondence concerns work-related administrative
    matters affecting a workforce that exceeds the resident population by ~75%. Source:
    ODT/LISER Maps and Figures 2023, reported by chronicle.lu — [WEB-2]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://statistiques.public.lu/en/publications/series/regards/2025/regards-01-25.html |
| WEB-2 | https://www.chronicle.lu/category/surveys-reports/54808-cross-border-workers-constitute-47-of-luxembourgs-500k-workforce-in-2023 |
| WEB-3 | https://luxembourg.public.lu/en/society-and-culture/population/demographics.html |
| WEB-4 | https://www.alphatrad.co.uk/news/portuguese-in-luxembourg |
| WEB-5 | https://statistiques.public.lu/en/actualites/2025/stn16-population-2025.html |
| WEB-6 | https://statistiques.public.lu/en/actualites/2024/stn16-population-2024.html |
| WEB-7 | https://gouvernement.lu/en/actualites/toutes_actualites/communiques/2023/02-fevrier/10-100-communes.html |
| WEB-8 | https://elections.public.lu/en/fusion-communes.html |
| WEB-9 | https://en.paperjam.lu/article/delano_understanding-cross-border-worker-phenomenon |
| WEB-10 | https://theworldfactbook.org/country/luxembourg.html |
| WEB-11 | https://en.wikipedia.org/wiki/Portuguese_in_Luxembourg |
| WEB-12 | https://www.mdpi.com/1999-5903/17/6/228 |
| WEB-13 | https://digital-strategy.ec.europa.eu/en/policies/desi-luxembourg |
| WEB-14 | https://www.statista.com/statistics/377741/household-internet-access-in-luxembourg/ |
| WEB-15 | https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Urban-rural_Europe_-_digital_society |
| WEB-16 | https://eufordigital.eu/wp-content/uploads/2020/06/DESI2020Thematicchapters-FullEuropeanAnalysis.pdf |
| WEB-17 | https://statistiques.public.lu/en/publications/series/luxembourg-en-chiffres/2024/luxembourg-en-chiffres-2024.html |
| WEB-18 | https://www.oecd.org/en/publications/2025/04/oecd-economic-surveys-luxembourg-2025_3eb782b5/full-report/reviving-productivity-growth_4509ab88.html |
| WEB-19 | https://www.expatica.com/lu/working/employment-basics/cross-border-worker-in-luxembourg-1063529/ |
| WEB-20 | https://transports.public.lu/en/plus/faq/gratuite-transports-publics.html |
| WEB-21 | https://www.mobiliteit.lu/en/tickets-page/fares/ |
| WEB-22 | https://regulations.ai/regulations/luxembourg-summary |
| WEB-23 | https://cms.law/en/int/expert-guides/ai-regulation-scanner/luxembourg |
| WEB-24 | https://www.pinsentmasons.com/out-law/news/luxembourg-law-addresses-eu-ai-act-enforcement |
| WEB-25 | https://www.arendt.com/news-insights/news/new-luxembourg-bill-designates-national-authorities-under-the-ai-act-the-cnpd-takes-centre-stage/ |
| WEB-26 | https://cnpd.public.lu/en/actualites/national/2025/08/ai-act-un-an.html |
| WEB-27 | https://cnpd.public.lu/en/dossiers-thematiques/intelligence-artificielle/regulation-ia/ria-maitrise-ia.html |
| WEB-28 | https://luxembourg.public.lu/en/living/mobility/public-transport.html |
| WEB-29 | https://washington.mae.lu/en/actualites/2020/free-public-transport-nationwide.html |
| WEB-30 | https://www.migrationpolicy.org/country-resource/luxembourg |

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
