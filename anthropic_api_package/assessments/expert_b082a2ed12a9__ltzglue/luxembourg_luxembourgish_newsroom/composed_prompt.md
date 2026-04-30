I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **LTZGLUE: The First Natural Language Understanding Benchmark for Luxembourgish** is valid for use in **Luxembourgish Professional Newsroom**.

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
LTZGLUE covers eight NLU tasks spanning binary and multi-class sentence- and
token-level classification [Q11], explicitly mirroring the scope of the original
nine-task English GLUE benchmark [Q68]. The task set spans headline acceptability
(HA), sentiment analysis (SA), binary and multiclass linguistic acceptability (LA),
NER, topic classification (TC), intent detection (ID), and RTE [Q2, Q15, Q23, Q29,
Q59, Q67]. Notably, the headline acceptability task is a novel contribution designed
for Luxembourgish rather than a port [Q69], directly addressing the deployment's
requirement for headline-vs-body consistency checking. Topic classification uses five
domain labels (SPORTS, CULTURE, TECHNOLOGY, BUSINESS, ANIMALS) [Q48] — a set of
standard international news categories, with the unusual inclusion of ANIMALS. The
intent detection task uses alarm and reminder sub-intents drawn from the xSID schema
[Q154], which are operationally irrelevant for a newsroom context. The RTE task is
identified as the most challenging overall [Q103], while topic classification emerges
as the easiest [Q99]. The benchmark explicitly supports all four tasks required by
the target newsroom deployment (HA, LA, TC, NER), and LLM prompt templates for
each are documented in detail [Q143, Q144, Q145, Q146, Q148, Q149, Q150, Q151,
Q152, Q153, Q154, Q155], providing transparent task formulation.

### Input Content
Most LTZGLUE tasks draw on two primary sources [Q12], with RTL — Luxembourg's
dominant media outlet — serving as the principal corpus across headline acceptability
[Q16], sentiment analysis [Q24], topic classification [Q46], and RTL online news
comments for NER [Q40]. The NER component merges the automatically constructed
JUDGEWEL corpus (~27k sentences derived from Wikipedia and Wikidata) [Q34, Q38]
with a human-annotated RTL news comment corpus [Q40, Q45]. The intent detection
task is translated from the English xSID dataset [Q51], and the German machine-
translated training set is used as a proxy [Q54]. The RTE task originates from a
previously machine-translated Luxembourgish version subsequently improved using
ChatGPT-5.1 [Q60, Q61], with 22–28% of instances removed after quality filtering
[Q66]. The authors acknowledge that data sources are concentrated in a limited set
of public domains due to the small language community [Q119], and that most data
reflects formal writing or institutional usage, not fully representing informal and
multilingual contexts [Q112]. Critically, code-switched content — French, German,
or English lexical items embedded within Luxembourgish text — is not documented as
a deliberate feature of the benchmark instances; the NER corpus sourced from RTL
news comments does cover informal and code-mixed writing [Q41], but coverage is
not systematically characterised. The construction strategy is explicitly described
as resource-conscious in response to data scarcity [Q109].

### Input Form
All tasks operate on plain text input [Q17], matching the deployment's text-only
modality. Text data is drawn from written journalistic sources (RTL news articles,
online comments, parliamentary transcripts, chat rooms, Wikipedia) [Q74, Q135] and
from translated or automatically constructed corpora. A BPE tokenizer with vocabulary
size 50,368 is trained on the full pre-training corpus with a 1,024-token maximum
sequence length [Q128, Q129]. The benchmark's text data is filtered to remove non-
Luxembourgish content (using OpenLID) and articles outside a 40–400 word range
[Q47], and preprocessing avoids directly identifying personal information [Q116].
Luxembourgish has historically limited written standardisation and substantial
orthographic and sociolinguistic variation [Q7], yet there is no explicit documentation
of orthographic normalisation across datasets — a moderate validity concern given
the deployment's preference for flexible journalistic register. The language's small
speaker community (~400k) and "scraping-by" resource status [Q4, Q13] constrain
the range and register diversity of available input text.

### Output Ontology
The output label schemas vary across tasks. Headline acceptability is binary
(True/False) [Q148]; sentiment analysis uses three classes (positive, neutral,
negative) [Q149]; linguistic acceptability binary collapses four error types into
correct (1) vs. incorrect (0) [Q33, Q150], while the multiclass variant exposes
four error categories: verb agreement (Verb), adjective agreement (Adj), syntactic
deletion (Syntax), and orthographic variant (Ortho) [Q31, Q151]. NER uses BIO
format over five entity types: LOC, PER, ORG, MISC, DATE [Q152], with GPE merged
into LOC [Q44]. Topic classification uses five domain labels [Q48, Q153]. Intent
detection uses alarm and reminder sub-intents from the xSID schema [Q154]. The
benchmark explicitly applies a label-output (not MCQA) paradigm [Q84], providing
the valid label set directly in prompts. However, the linguistic acceptability
output categories and headline acceptability binary schema were constructed from
formal linguistic error types [Q31] and TF–IDF-based structural mismatches [Q22],
rather than from the professional-journalistic register that the deployment explicitly
targets. The GPE–LOC merge [Q44] reduces entity-type granularity potentially
relevant for cross-border Luxembourg journalism, and the ANIMALS topic category
[Q48] is an unusual inclusion whose relevance to a professional newsroom context
is not justified. Output taxonomies for several tasks are ported from non-Luxembourgish
contexts (xSID, RTE) without explicit validation of their appropriateness for
Luxembourgish norms.

### Output Content
Annotation quality is highly heterogeneous across tasks. For sentiment analysis,
4,583 sentences were annotated by two native Luxembourgish speakers achieving
Cohen's Kappa of 0.45 [Q25, Q27] — a moderate agreement level below the 0.60–0.80
range typically expected for robust NLU annotation — with disagreements resolved
by annotator consensus [Q26, Q28]. For intent detection, translation was performed
by a native Luxembourgish speaker with additional native speakers consulted for
uncertain cases [Q52], but no IAA metric is reported. The JUDGEWEL NER corpus used
LLMs as judges with minimal human verification [Q37]; the contrasting human-annotated
NER corpus is smaller but high-precision [Q42]. For RTE, annotation was predominantly
AI-assisted: ChatGPT-5-MINI was used for quality assessment [Q63] and label
verification [Q64], with manual correction only where the improvement step had
altered ground-truth semantics [Q65]. Annotators beyond sentiment analysis are
described only as "student assistants" [Q114]; there is no documentation indicating
any annotators were professional journalists or editors rather than linguists or
general native speakers. The authors explicitly caution that models may reproduce
dominant norms while under-representing regional, sociolectal, or multilingual
practices [Q120], and warn against using benchmark performance as evidence of
cultural or demographic coverage [Q121]. Societal biases from institutional and
media data sources may influence model behaviour [Q117, Q118], and automatic
preprocessing biases cannot be fully quantified [Q113].

### Output Form
All tasks produce discrete label outputs evaluated by macro-F1 [Q93, Q96], which
is appropriate for the deployment's per-task classification paradigm. For encoder-
based models, results are averaged over three runs with standard deviations reported
[Q89, Q96], using Bayesian hyperparameter search capped at 30 runs [Q138] with
best parameters selected on validation sets [Q137]. Class-imbalanced tasks
(linguistic acceptability and sentiment analysis) use class-balanced loss with
effective size weighting (beta 0.99) [Q92]. For LLMs in zero-shot settings, outputs
that fail to conform to the expected label format are discarded prior to evaluation
[Q90, Q91], and only macro-F1 is reported for a single run [Q96], making LLM
performance estimates less stable. The evaluation does not use a MCQA setup but
provides valid labels directly in the prompt [Q84], more closely mirroring the
deployment's classification framing. Full validation and test results across all
eight tasks and models are provided in appendix tables [Q156, Q158, Q159].
Prompt sensitivity and instruction-following variability mean LLM performance
should be treated as indicative rather than directly comparable to supervised
results [Q86].


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This paper presents LTZGLUE, the first Natural Language Understanding (NLU) benchmark for Luxembourgish (LTZ) based on the popular GLUE benchmark for English." |
| Q2 | 1 | input_ontology | "Our tasks include common natural language processing tasks in binary and multi-class classification settings, including named entity recognition, topic classification, and intent classification." |
| Q3 | 1 | output_form | "We evaluate various pre-trained language models for LTZ to present an overview of the current capabilities of these models on the LTZ language." |
| Q4 | 1 | input_content | "Small and under-researched languages are particularly difficult to evaluate, as is the case with Luxembourgish (LTZ), the national language of Luxembourg, with around 400k speakers." |
| Q5 | 1 | input_content | "LTZ only has a handful of NLU tasks available (Lothritz et al., 2022; Philippy et al., 2024; Plum et al., 2026)." |
| Q6 | 1 | input_content | "As most of these are in the news domain, and the majority of the down-stream tasks comprise less than a thousand instances, model evaluation is not always dependable." |
| Q7 | 1 | input_form | "Additional factors, such as the ongoing standardisation of the language (Gilles, 2019), vast amounts of variation (Lutgen et al., 2025), and decentralised resources, make it extremely challenging to evaluate LTZ language understanding in language models." |
| Q8 | 1 | input_ontology | "Our contributions are: (1) LTZGLUE: the first unified GLUE benchmark for LTZ, with 8 tasks." |
| Q9 | 1 | input_ontology | "(2) LTZ-E1 (mini/base): 2 new encoder language models for LTZ, which achieve competitive performance when fine-tuned on LTZGLUE." |
| Q10 | 1 | input_content | "Alistair Plum1, Felicia Körner2,3, Anne-Marie Lutgen1, Laura Bernardy1, Fred Philippy1, Emilia Milano1, Nils Rehlinger1, Cédric Lothritz4, Tharindu Ranasinghe5, Barbara Plank2,3, Christoph Purschke1 1University of Luxembourg, Luxembourg, 2LMU Munich, Germany 3Munich Center for Machine Learning, Germany 4LIST, Luxembourg, 5Lancaster University, UK" |
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
| Q22 | 3 | input_content | "The resulting negative examples remain topically related but are temporally and structurally mismatched, forcing models to attend to article content rather than surface cues." |
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
| Q35 | 4 | output_ontology | "Using Wikipedia's hyperlink structure, entities are matched to their corresponding Wikidata types and labelled in BIO format." |
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
| Q56 | 5 | output_content | "Due to the lack of LTZ references in this register, it was not possible to systematically verify the translated terminology." |
| Q57 | 5 | input_form | "After translating the dataset, we transferred the BIO tags by first using token-level fuzzy matching between the LTZ and the German dataset, followed by manual verification." |
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
| Q82 | 6 | output_content | "None of these models are fine-tuned on LTZGLUE, although some of the text data (RTL, Wikipedia) is very likely to have been processed during training." |
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
| Q111 | 9 | output_content | "In addition, some of the data sources used in this benchmark may already be included, in whole or in part, in the pre-training corpora of the large language models evaluated in this work. While the exact composition of proprietary pre-training datasets is typically not fully disclosed, this potential overlap cannot be entirely ruled out and may inflate performance estimates." |
| Q112 | 9 | input_content | "Coverage across domains, registers, and demographic varieties may also be limited. LTZ displays substantial orthographic and sociolinguistic variation, yet most data sources reflect formal writing or institutional usage and therefore do not fully represent informal and multilingual contexts." |
| Q113 | 9 | output_content | "Although we draw on established GLUE-style tasks, some annotation decisions and class distributions are necessarily influenced by resource constraints. Certain tasks exhibit label imbalance or rely on automatic preprocessing, which may introduce biases that we cannot fully quantify." |
| Q114 | 9 | output_content | "We would like to thank the student assistants for their annotation work." |
| Q115 | 9 | input_content | "This work is supported by the LLMs4EU project, funded by the European Union through the Digital Europe Programme (DIGITAL) under the grant agreement 10119847. FK and BP are supported by the ERC Consolidator Grant DIALECT 101043235." |
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
| Q145 | 14 | output_ontology | "You are an expert for the Luxembourgish language. I am giving you two texts TEXT1 and TEXT2 in Luxembourgish as well as a LABEL where 1 means that TEXT1 logically entails TEXT2 while 0 means the opposite. You have to check if the labels are correct. As output, simply write 'true' if the label is the correct one or 'false' if the label is incorrect." |
| Q146 | 14 | output_form | "You are a classification and text-processing model specialized in NLP tasks for Luxembourgish (lb). Follow ALL rules strictly: 1. Respond ONLY in valid JSON. 2. Do NOT add explanations, comments or text outside of JSON. 3. Use field: "output": <model_answer>. 4. Use field: "task": "<task_name>". 5. Use field: "input": "<input example text>". 6. Predict only the requested outputs and" |
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
name: Luxembourgish Professional Newsroom
abbreviation: LU-Newsroom
deployment_context:
  country: Luxembourg
  broader_geographic_context: Greater Region (Grande Région / Großregion), encompassing
    cross-border areas of Belgium (Wallonia, Liège), France (Lorraine/Grand Est),
    and Germany (Saarland, Rhineland-Palatinate)
  setting: Professional newsroom — journalists, editors, and digital content managers
    at Luxembourgish media outlets producing news for a local audience
  system_function: LLM-powered editorial pipeline that evaluates articles across four
    tasks (headline acceptability, linguistic acceptability, topic classification,
    NER) to auto-publish or flag content for manual editorial review
  flagging_logic: Per-task confidence scores are computed independently; a threshold
    breach on any single task triggers an editor-visible flag indicating which criterion
    caused the review
  explanation_mode: Human-readable explanations not generated by default; available
    on request for recurring or complex flagged cases
target_population:
  description: Professional journalists, sub-editors, and digital content managers
    employed at Luxembourgish media outlets. Users are trained news professionals
    who produce and edit articles in Luxembourgish for a domestic audience. They interact
    with the system primarily as recipients of automated flagging decisions rather
    than as end-users entering natural-language queries. No sub-national demographic
    variation beyond the shared professional newsroom context.
  occupational_role: Journalists and editors (news production, sub-editing, digital
    publishing)
  organizational_context: Luxembourgish media outlets (broadcast, digital, print)
  audience_served: General Luxembourgish public, including cross-border Greater Region
    readership
primary_media_outlets:
  note: Relevant outlets for understanding the deployment register and audience; readership
    figures from TNS Ilres / Euromedia Ownership Monitor 2022–2023.
  dominant_outlet_in_benchmark: 'RTL Luxembourg (principal data source for LTZGLUE
    headline acceptability, sentiment analysis, topic classification, and NER tasks).
    RTL leads Luxembourg''s media landscape across television (RTL Télé Lëtzebuerg),
    radio (RTL Radio Lëtzebuerg), and web (rtl.lu, ~192,300 daily web visitors in
    2022). Source: Euromedia Ownership Monitor 2023 — [WEB-1]'
  other_significant_outlets: 'Major Luxembourgish print, broadcast, and digital news
    organisations beyond RTL:

    - Luxemburger Wort (Mediahuis Luxembourg): Luxembourg''s largest daily by readership
    (~117,000–137,000 readers), published primarily in German; website wort.lu ~93,100
    daily visitors. Source: Delano/TNS Ilres 2022 — [WEB-2];
    RSF — [WEB-3]

    - L''essentiel: free French-language daily; ~88,300–104,500 readers, ~137,400
    daily web visitors; targets cross-border commuters and younger multilingual audiences.
    Source: Euromedia Ownership Monitor 2023 — [WEB-1]

    - Tageblatt (Editpress, Esch-sur-Alzette): German-language daily with left-wing
    labour union backing; ~25,900–35,800 readers. Source: Delano/TNS Ilres 2022 —
    [WEB-2]

    - radio 100,7 (100komma7.lu): Luxembourg''s public cultural radio station; broadcasts
    primarily in Luxembourgish. Source: Conseil de Presse editor directory — [WEB-4]

    - Delano: English-language business and lifestyle magazine (~10,000 copies, 11
    issues/year) targeting the international community. Source: justarrived.lu — [WEB-5]

    - Paperjam: French-language business/finance magazine (~52,600 readers in 2022).
    Source: Delano/TNS Ilres 2022 — [WEB-2]

    - Le Quotidien: French-language daily covering Luxembourg and the Greater Region
    (~12,300 readers). Source: Euromedia Ownership Monitor 2023 — [WEB-1]

    Note: The print press historically defaulted to German (Luxemburger Wort, Tageblatt);
    radio and television (RTL, 100,7) use Luxembourgish as primary broadcast language.
    This distribution shapes the register diversity that a Luxembourgish-language
    NLP system must handle.'
languages:
  primary_language: 'Luxembourgish (Lëtzebuergesch, ISO 639-1: lb)'
  code_switching_languages:
  - French
  - German
  - English
  code_switching_note: Code-switching is a core operational reality of Luxembourgish
    professional journalism. French, German, and English lexical items, official titles,
    legal terms, and direct quotes are routinely embedded within otherwise Luxembourgish
    article text. The deployment system must handle this dense multilingual mixing;
    it is not an edge case but the default production register.
  language_policy_context: 'Luxembourg''s trilingualism is enshrined in the Law of
    24 February 1984, which made Luxembourgish the national language and recognised
    Luxembourgish, French, and German as the three administrative languages. French
    remains the sole language of legislation (Napoleonic Code legacy). In newsrooms,
    German has historically dominated the written press (Luxemburger Wort, Tageblatt),
    while Luxembourgish predominates in broadcast (RTL, 100,7); French is the language
    of the largest free daily (L''essentiel) and much official communication. Journalists
    writing in Luxembourgish routinely embed French and German terms, official titles,
    and legal vocabulary. Source: Languages of Luxembourg (Wikipedia) — [WEB-6];
    Euromedia Ownership Monitor 2023 — [WEB-1]'
  speaker_population: 'Approximately 400,000 Luxembourgish speakers worldwide (per
    benchmark documentation and Wikipedia). A separate figure often cited is ~285,000
    native speakers maximum. Source: Wikipedia Luxembourgish — [WEB-7]'
  total_luxembourg_population: '672,050 as of 1 January 2024 (52.7% Luxembourgers,
    47.3% foreign nationals). Source: Demographics of Luxembourg (Wikipedia, citing
    official statistics) — [WEB-8]'
  luxembourgish_as_l1_proportion: 'Approximately 41.5% of working-age residents (25–64)
    declared Luxembourgish as their first maternal language (Statec survey); 48.9%
    declared it their main language in the 2021 census (down from 55.8% in 2011).
    Only 61.2% of the total resident population reported speaking Luxembourgish at
    all in 2021. Among Luxembourgish nationals, ~70% speak it as a native language
    per EU survey data; but the proportion is diluted by the ~47% foreign-national
    resident population, most of whom do not speak Luxembourgish. Source: STATEC/Statistics
    Portal Luxembourg 2021 census — [WEB-9];
    Paperjam/Statec report — [WEB-10]'
writing_systems:
  script: Latin alphabet with diacritics standard to Luxembourgish orthography (e.g.,
    é, ë, ä, etc.)
  orthographic_standardisation_status: Ongoing; Luxembourgish has historically limited
    written standardisation and substantial orthographic and sociolinguistic variation.
    The ZLS published a revised comprehensive orthographic standard in November 2019.
    Subsequent updates have been incorporated into new editions of the ZLS orthography
    book. The CPLL advises on spelling, grammar, pronunciation, and usage. Journalistic
    practice permits flexible register that may diverge from the formal 2019 standard.
  official_orthographic_body: 'Zenter fir d''Lëtzebuerger Sprooch (ZLS), established
    by the Law of 20 July 2018 on the promotion of the Luxembourgish language. The
    ZLS sets and publishes orthographic rules, maintains the Lëtzebuerger Online Dictionnaire
    (LOD.lu) and Spellchecker.lu, and advises the government on language standardisation.
    It works in coordination with the Conseil permanent de la langue luxembourgeoise
    (CPLL, established 1998), which validates ZLS spelling and grammar rules. The
    ZLS published its current orthographic standard in November 2019 and operates
    under the Ministry of Culture. Source: ZLS Open Data portal — [WEB-11];
    Luxembourg Education Ministry — [WEB-12];
    CPLL — [WEB-13]'
  journalistic_vs_formal_register_gap: 'Explicitly acknowledged in deployment requirements:
    the system applies a flexible professional-journalistic register rather than strict
    official orthography. Borderline cases exist where a formal language authority
    and an editorial team would disagree. The benchmark''s Ortho error category derives
    from Spellchecker.lu data (a ZLS tool), which encodes the formal standard — potentially
    penalising journalistic variants that the editorial deployment would accept.'
literacy_and_education:
  general_literacy_rate: '[NEEDS VERIFICATION — deferred: below search budget; Luxembourg
    is a high-income EU state and near-universal adult literacy is routinely assumed;
    no deployment-material impact on scoring since target users are professionals]'
  professional_user_literacy: All target users are professional journalists and editors;
    functional literacy and language proficiency in Luxembourgish, French, and German
    are occupational prerequisites
  education_system_language_context: 'Luxembourg operates a formally trilingual school
    system. Luxembourgish is the language of pre-primary socialisation and oral communication
    from age 3–4. Formal literacy instruction begins in German at age 6 (Cycle 2),
    with French introduced orally from Cycle 2 and in writing from Cycle 3. In standard
    secondary education, German remains the main instruction language in lower years;
    French becomes the main instruction language in upper years of the classical lycée
    from age 15. English is a compulsory additional language in all secondary schools.
    Language teaching accounts for approximately 50% of teaching time. A 2022–2025
    ALPHA pilot (extended nationally from 2026/2027) allows French as the initial
    literacy language as an alternative to German. In 2023/2024, fewer than one-third
    of primary school pupils spoke Luxembourgish as their first language. This system
    produces newsroom professionals with deep trilingual competence (Luxembourgish/French/German)
    and strong English, matching the benchmark''s target population profile. Source:
    Luxembourg Ministry of Education — [WEB-14];
    EU Education and Training Monitor 2025 — [WEB-15];
    Wikipedia Education in Luxembourg — [WEB-16]'
sociolinguistic_context:
  multilingualism_character: 'Luxembourg is one of the world''s most multilingual
    national contexts. The professional newsroom population is typically fluent in
    Luxembourgish, French, and German, with high English proficiency. This is not
    incidental multilingualism but a structural feature of Luxembourgish public life
    and journalism. A Statec study found Luxembourgish nationals speak an average
    of 4.3 languages; 9 out of 10 residents speak French. Source: Paperjam/Statec
    — [WEB-10]'
  diglossia_and_register: Luxembourgish occupies a vernacular and increasingly written-standard
    role; French and German serve formal administrative and press functions alongside
    it. The benchmark's primary data source (RTL) represents mainstream Luxembourgish-language
    journalism, which routinely incorporates French and German phraseology. The print
    press historically used German; broadcast uses Luxembourgish; the free daily L'essentiel
    uses French — creating a functionally diglossic (or triglossic) media landscape.
  grande_region_cross_border_relevance: 'Luxembourgish news routinely covers entities,
    officials, and events in the Belgian, French, and German cross-border zones. NER
    in this context must handle multilingual proper nouns and cross-border institutional
    names (EU institutions headquartered in Luxembourg, Belgian/French/German municipalities,
    cross-border transport and policy bodies). L''essentiel and Paperjam explicitly
    position themselves as serving a de-bordered ''Greater Luxembourg'' regional audience
    including cross-border workers. Source: Euromedia Ownership Monitor 2023 — [WEB-1]'
  eu_institutional_context: Luxembourg hosts major EU institutions (European Court
    of Justice, European Court of Auditors, General Secretariat of the European Parliament,
    etc.); EU institutional nomenclature in French, German, and English appears frequently
    in Luxembourgish news copy
infrastructure_notes:
  deployment_modality: Text-only pipeline; no multimodal components
  internet_penetration: '98.8% of population (2024, ITU/World Bank data via TheGlobalEconomy.com).
    Household internet access was ~99.06% in 2023 per Eurostat. Luxembourg ranks among
    the highest globally. Source: TheGlobalEconomy.com citing ITU/World Bank — [WEB-17];
    Statista/Eurostat — [WEB-18]'
  digital_infrastructure_quality: Luxembourg is a high-income EU member state with
    advanced digital infrastructure; enterprise-grade connectivity is assumed in a
    professional newsroom context
  nlp_tooling_availability_for_luxembourgish: Luxembourgish is a low-resource language
    with limited NLP tooling relative to major European languages. LTZGLUE and the
    LTZ-E1 encoder models (68M/110M parameters) represent the current frontier. Multilingual
    models (XLM-RoBERTa, mBERT) provide partial coverage but are not optimised for
    Luxembourgish.
  tokenisation_concern: The LTZGLUE BPE tokenizer (vocabulary size 50,368) is trained
    on a 233M-token Luxembourgish corpus. Orthographic variation in journalistic copy
    and code-switched tokens may not be well-represented in this vocabulary.
domain_specific_notes:
  editorial_taxonomy:
    classification_scheme: Standard international news categories; no bespoke Luxembourg-specific
      sub-categories required by the deployment
    benchmark_topic_labels:
    - SPORTS
    - CULTURE
    - TECHNOLOGY
    - BUSINESS
    - ANIMALS
    animals_category_note: The ANIMALS topic label is an unusual inclusion in a professional
      newsroom taxonomy; its operational relevance should be confirmed with the deploying
      outlet
    missing_categories_risk: Standard categories absent from the benchmark's five-label
      schema (e.g., POLITICS, HEALTH, JUSTICE, LOCAL/MUNICIPAL) are not covered; articles
      falling into these categories may be misclassified or unclassifiable under the
      current taxonomy
  ner_entity_landscape:
    benchmark_entity_types:
    - LOC
    - PER
    - ORG
    - MISC
    - DATE
    gpe_loc_merge_implication: 'GPE (geo-political entity) labels are merged into
      LOC in the benchmark. For Luxembourgish journalism, this reduces granularity
      for cross-border references: a Belgian municipality and a geographic region
      may receive identical tags, limiting utility for editorial systems that need
      to distinguish political-administrative entities.'
    high_frequency_entity_categories_in_lu_journalism:
    - EU institutional names (typically in French or English)
    - Cross-border municipal and regional names (French, German, Luxembourgish variants)
    - Belgian, French, and German political officials and titles
    - Luxembourgish political figures and government bodies
    - Grande Région / Großregion bodies and programmes
    multilingual_proper_noun_challenge: Entity mentions in Luxembourgish news copy
      frequently appear in French, German, or English rather than a Luxembourgish
      form; NER models must resolve cross-lingual surface variation for the same underlying
      entity
  headline_acceptability_task:
    benchmark_construction_method: TF-IDF-based structural mismatch with temporally
      separated donor headlines
    deployment_requirement: Semantic/editorial coherence between headline and article
      body as judged by a professional journalist
    gap: The benchmark's negative examples are topically related but structurally
      and temporally mismatched; this operationalisation may not capture the subtler
      headline–body mismatches (nuance, framing, register) that editorial flagging
      is meant to catch
  linguistic_acceptability_task:
    benchmark_error_taxonomy:
    - Verb agreement (Verb)
    - Adjective agreement (Adj)
    - Syntactic deletion (Syntax)
    - Orthographic variant (Ortho)
    benchmark_data_source: Luxembourgish Online Dictionary (LOD) — formal/normative
      register, maintained by ZLS
    deployment_standard: Flexible professional-journalistic register; the deployment
      explicitly targets this register over formal orthography
    gap: The benchmark's acceptability ground truth derives from a formal ZLS dictionary
      source and formal linguistic error types. The Ortho category specifically uses
      Spellchecker.lu data (another ZLS tool) encoding the November 2019 official
      orthographic standard. This creates systematic divergence from the journalistic
      register the deployment targets, particularly for the Ortho category where journalistic
      practice may legitimately use variants the formal standard would reject.
  annotator_profile:
    benchmark_annotators: Native Luxembourgish speakers described as student assistants;
      no documentation of professional journalism expertise
    inter_annotator_agreement_sentiment: Cohen's Kappa 0.45 (moderate; below the 0.60–0.80
      range typical for robust NLU annotation)
    rte_annotation_method: Predominantly AI-assisted (ChatGPT-5.1 for improvement,
      ChatGPT-5-MINI for quality assessment and label verification)
    deployment_annotation_need: Ground-truth labels for acceptability tasks should
      ideally be produced by professional Luxembourgish journalists/editors applying
      the flexible editorial register — a population absent from the benchmark annotation
      process
  legal_and_regulatory_context:
    press_law: 'The primary Luxembourgish press law is the Loi du 8 juin 2004 sur
      la liberté d''expression dans les médias (amended 11 April 2010), which governs
      freedom of expression and editorial responsibility for both print and broadcast
      media. The Conseil de Presse enforces a deontological code for professional
      journalists. A new comprehensive Draft Bill (No. 8625, presented October 2025)
      is under parliamentary discussion; it would modernise media law with a unified
      technology-neutral framework covering all media formats (TV, radio, print, digital,
      on-demand), transpose the European Media Freedom Act (EU 2024/1083) and the
      Political Advertising Regulation (EU 2024/900), and extend content prohibitions
      to hosted user comments. This bill does not specifically address automated editorial
      systems or auto-publication; editorial responsibility for published content
      continues to rest with the named editor/responsible journalist under the 2004
      law. Source: Conseil de Presse legal texts — [WEB-19];
      Luxembourg government media legislation — [WEB-20];
      DLA Piper analysis of Draft Bill 8625 — [WEB-21]'
    data_protection: 'GDPR (Regulation EU 2016/679) applies directly in Luxembourg.
      The national data protection supervisory authority is the Commission nationale
      pour la protection des données (CNPD). Luxembourg implementing legislation is
      the Law of 1 August 2018 on the CNPD and general data protection regime. Processing
      of article text by an automated editorial pipeline constitutes personal data
      processing where articles contain personal information (e.g., NER entity resolution
      for named individuals). The CNPD also serves as the default AI Act market surveillance
      authority under the proposed national AI Act implementation bill. Source: CNPD
      — [WEB-22];
      CMS Law Luxembourg AI regulation guide — [WEB-23]'
    ai_act_applicability: 'The EU AI Act (Regulation EU 2024/1689), in force from
      August 2024 and broadly applicable from August 2026, applies directly in Luxembourg.
      There is no dedicated national AI law; Luxembourg is implementing the AI Act
      via Draft Bill 8476 (submitted December 2024, still under parliamentary discussion
      as of early 2026), which designates national supervisory authorities: CNPD as
      general reference authority, with ALIA (Autorité luxembourgeoise indépendante
      de l''audiovisuel) as a sectoral authority specifically covering audiovisual
      and media contexts. The automated editorial flagging system is most plausibly
      a limited-risk or minimal-risk AI system under the AI Act''s risk taxonomy (classification
      and flagging tool with human editorial review in the loop), rather than a prohibited
      or high-risk system — but deployers should confirm this classification, particularly
      given ALIA''s sectoral oversight role for media AI systems. Transparency obligations
      (labelling AI-generated or AI-processed content decisions) may apply. Source:
      CMS Law Luxembourg AI regulation guide — [WEB-23];
      Chambre des Députés Bill 8476 summary — [WEB-24];
      Luxembourg Norton Rose Fulbright AI Act overview — [WEB-25]'
cultural_norms_notes: '- Luxembourg''s professional newsroom culture is shaped by
  its trilingual (Luxembourgish/French/German) administrative and educational context;
  journalists routinely switch languages within a single article

  - Cross-border Greater Region identity is reflected in news coverage: Belgian, French,
  and German political and cultural events are treated as local news

  - EU institutional politics and policy are a major domestic beat given Luxembourg''s
  role as an EU host country

  - Luxembourgish editorial norms may diverge from French or German press traditions
  even when French or German vocabulary is borrowed

  - The professional register is pragmatic and code-switching is not stigmatised;
  strict monolingual Luxembourgish articles are less common in practice than mixed-language
  copy

  - Small language community (~400k speakers) means that editorial staff and their
  audience share a high degree of contextual background knowledge, raising the baseline
  for what a ''correct'' or ''acceptable'' headline or article is

  - The print press historically defaulted to German; broadcast (RTL, 100,7) uses
  Luxembourgish as primary language; this creates register and corpus heterogeneity
  that an NLP system must navigate

  - UNESCO listed Luxembourgish as an endangered language in 2019; the proportion
  of native Luxembourgish speakers among residents is declining due to high immigration
  rates (~47% foreign nationals in 2024)

  '
benchmark_alignment_summary:
  tasks_covered_by_benchmark:
  - Headline Acceptability (HA)
  - Linguistic Acceptability binary (LA BINARY)
  - Linguistic Acceptability multiclass (LA MULTI)
  - Named Entity Recognition (NER)
  - Topic Classification (TC)
  tasks_in_deployment_not_well_covered: No deployment task falls entirely outside
    benchmark coverage; however, the quality of coverage for HA and LA is qualified
    by register and annotator mismatch
  tasks_in_benchmark_not_relevant_to_deployment:
  - Sentiment Analysis (SA)
  - Intent Detection (ID)
  - Recognising Textual Entailment (RTE)
  highest_validity_risk_dimensions:
  - OC — annotator-population mismatch (student native speakers vs. professional journalists)
  - IC — code-switching coverage not systematically characterised
  - OO — formal-linguistic output ontology misaligned with journalistic register ground
    truth
flagged_gaps_for_web_search:
- gap_id: 1
  topic: Code-switching coverage in LTZGLUE instances
  search_target: LTZGLUE code-switching French German Luxembourgish NLP benchmark
    evaluation coverage
  priority: HIGH
  search_outcome: '[NEEDS VERIFICATION — deferred: no additional search budget available.
    Benchmark documentation confirms only the human-annotated RTL NER comment corpus
    covers informal/code-mixed writing; systematic quantification of code-switched
    instances across all LTZGLUE tasks remains undocumented and would require direct
    inspection of the dataset. This is the single highest-impact unresolved gap.]'
- gap_id: 2
  topic: Annotator profile for acceptability tasks — professional journalist involvement
  search_target: Luxembourgish journalistic register annotation professional editors
    NLP ground truth LTZGLUE
  priority: HIGH
  search_outcome: '[NEEDS VERIFICATION — deferred: no additional search budget available.
    Benchmark text is unambiguous (student assistants only; no journalists), so further
    web search is unlikely to alter the gap finding. Confirmed full gap: professional
    journalist annotators are absent from the benchmark annotation process.]'
- gap_id: 3
  topic: Orthographic normalisation and register of benchmark text data
  search_target: Luxembourgish orthographic variation journalistic register LOD spellchecker
    professional norms NLP LTZGLUE
  priority: HIGH
  search_outcome: 'Partially resolved via ZLS/CPLL searches. Confirmed: the ZLS published
    the current official orthographic standard in November 2019; the LOD and Spellchecker.lu
    both encode this standard. The benchmark''s LA Ortho category uses Spellchecker.lu
    data, which operationalises the formal ZLS standard. No documentation was found
    that the benchmark applied explicit orthographic normalisation to RTL news input
    text before use, but the formal-register LOD source for LA sentences is confirmed.
    The register gap between ZLS formal standard and journalistic practice remains
    an unresolved risk requiring direct dataset inspection.'
- gap_id: 4
  topic: NER entity taxonomy and cross-border entity coverage
  search_target: Luxembourgish NER cross-border entities EU institutions Grande Region
    named entity recognition benchmark
  priority: MODERATE
  search_outcome: 'Partially resolved via benchmark documentation. Confirmed: NER
    uses LOC/PER/ORG/MISC/DATE with GPE merged into LOC. The RTL news comment corpus
    (Lothritz et al. 2022) does cover informal and code-mixed text including cross-border
    entities. However, the extent to which EU institutional names (typically in French/English)
    and Greater Region administrative entities are represented in the training set
    is not quantified in public documentation. No external cross-border NER benchmark
    for Luxembourgish was identified.'
- gap_id: 5
  topic: Data provenance and LLM-generated content risk in LTZGLUE
  search_target: LTZGLUE data provenance synthetic augmentation LLM-generated Luxembourgish
    benchmark authenticity
  priority: MODERATE
  search_outcome: 'Resolved from benchmark documentation (no additional web search
    needed): JUDGEWEL NER is automatically constructed with minimal human verification;
    RTE was improved by ChatGPT-5.1 and quality-filtered by ChatGPT-5-MINI (removing
    22–28% of instances); German machine-translated xSID training set used for intent
    detection. RTL, Wikipedia, and LOD sources represent authentic text. The LLM-augmented
    provenance is a confirmed moderate risk for RTE and NER (JUDGEWEL) tasks.'
- gap_id: 6
  topic: Headline acceptability operationalisation vs. editorial judgment
  search_target: Luxembourgish headline acceptability editorial norms journalistic
    register linguistic acceptability professional standard evaluation
  priority: MODERATE
  search_outcome: '[NEEDS VERIFICATION — deferred: below search budget. The gap is
    structurally confirmed from benchmark documentation (TF-IDF mismatch method vs.
    semantic/editorial coherence requirement); no external study evaluating Luxembourgish
    headline acceptability from a journalistic perspective was identified. Would require
    stakeholder elicitation with RTL editorial staff.]'
- gap_id: 7
  topic: Luxembourg official language standardisation body and prescriptive scope
  search_target: Zenter fir d'Lëtzebuerger Sprooch ZLS Luxembourgish orthographic
    standardisation official body LOD LNLP
  priority: MODERATE
  search_outcome: Resolved. ZLS established by Law of 20 July 2018; publishes orthographic
    rules (current standard finalised November 2019), maintains LOD.lu and Spellchecker.lu,
    and advises government on language matters. CPLL (established 1998) advises on
    ZLS rules. Both ZLS and CPLL are confirmed authoritative bodies. Sources cited
    in writing_systems.official_orthographic_body field above.
- gap_id: 8
  topic: Applicable press law, data protection, and AI Act obligations for automated
    editorial systems in Luxembourg
  search_target: Luxembourg press law automated editorial AI Act GDPR auto-publication
    content moderation newsroom regulation
  priority: LOWER
  search_outcome: 'Resolved. Key findings: (1) Press law: Loi du 8 juin 2004 sur la
    liberté d''expression dans les médias; Draft Bill 8625 (2025) under discussion
    but does not specifically address automated editorial AI. (2) Data protection:
    GDPR + CNPD. (3) AI Act: applies directly; Luxembourg implementation via Draft
    Bill 8476 (submitted December 2024, still under discussion); CNPD is general supervisory
    authority; ALIA is sectoral authority for audiovisual/media. The automated editorial
    system is likely limited-risk/minimal-risk under AI Act taxonomy given the human-in-the-loop
    editorial review model. Full details in legal_and_regulatory_context fields above.'
net_new_fields:
  luxembourgish_language_endangerment_status: 'UNESCO declared Luxembourgish an endangered
    language in 2019 and added it to the Atlas of the World''s Languages in Danger.
    The proportion of native Luxembourgish speakers among total residents is declining
    due to high immigration rates (47.3% foreign nationals as of 2024). In 2023/2024,
    fewer than one-third of primary school pupils spoke Luxembourgish as their first
    language. This demographic pressure on the language is relevant to benchmark validity
    because it limits the pool of native-speaker annotators and may accelerate register
    change in journalistic Luxembourgish. Sources: Wikipedia Luxembourgish — [WEB-7];
    EU Education and Training Monitor 2025 — [WEB-15]'
  media_language_distribution_in_luxembourg: 'Luxembourg''s media landscape is functionally
    stratified by language: print press (Luxemburger Wort, Tageblatt) historically
    published in German; broadcast (RTL, 100,7) operates primarily in Luxembourgish;
    free daily L''essentiel uses French and targets cross-border commuters. This stratification
    means a Luxembourgish-language NLP system trained on RTL data captures broadcast/online
    Luxembourgish but not the German-dominant written press tradition. Deployers extending
    the system to German-language outlets would face a significant domain shift. Source:
    Euromedia Ownership Monitor 2023 — [WEB-1];
    Newspaper Online Directory — [WEB-26]'
  alia_as_ai_act_sectoral_authority_for_media: 'Under Luxembourg''s Draft Bill 8476
    implementing the EU AI Act, the Autorité luxembourgeoise indépendante de l''audiovisuel
    (ALIA) is designated as the sectoral AI supervisory authority for audiovisual
    and media services. Newsroom AI systems (including automated editorial pipelines)
    may fall under ALIA''s oversight rather than solely CNPD''s. This is deployment-relevant
    because ALIA already regulates editorial independence and content standards under
    Luxembourgish media law. Source: Chambre des Députés Bill 8476 summary — [WEB-24];
    CMS Law Luxembourg AI regulation guide — [WEB-23]'
  luxembourg_new_media_law_draft_bill_8625: 'A major media law reform (Draft Bill
    8625) is currently under parliamentary discussion in Luxembourg (presented October
    2025). If adopted, it would replace the 2004 Loi sur la liberté d''expression
    dans les médias with a unified, technology-neutral framework covering all media
    formats. Key provisions relevant to automated editorial systems include: extended
    content prohibitions now covering hosted user comments; strict advertising transparency
    rules; transposition of the European Media Freedom Act (EU 2024/1083) guaranteeing
    editorial independence. The bill does not create specific obligations for automated
    editorial AI, but the editorial independence provisions and the post-publication
    supervision regime may affect how newsrooms document and justify automated flagging
    decisions. Source: DLA Piper analysis — [WEB-21];
    Luxtoday.lu — [WEB-27]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://media-ownership.eu/2023-edition/findings/countries/luxembourg/ |
| WEB-2 | https://delano.lu/article/paperjam-leads-monthly-luxembo |
| WEB-3 | https://rsf.org/en/country/luxembourg |
| WEB-4 | https://www.press.lu/en/mediatic-landscape-in-luxembourg/editors-in-chief/ |
| WEB-5 | https://www.justarrived.lu/en/medias-telecommunications-luxembourg/medias/ |
| WEB-6 | https://en.wikipedia.org/wiki/Languages_of_Luxembourg |
| WEB-7 | https://en.wikipedia.org/wiki/Luxembourgish |
| WEB-8 | https://en.wikipedia.org/wiki/Demographics_of_Luxembourg |
| WEB-9 | https://statistiques.public.lu/en/recensement/diversite-linguistique.html |
| WEB-10 | https://en.paperjam.lu/article/delano_23-lux-residents-speak-4-or-more-languages |
| WEB-11 | https://data.public.lu/en/organizations/zenter-fir-dletzebuerger-sprooch/ |
| WEB-12 | https://men.public.lu/en/grands-dossiers/systeme-educatif/promotion-langue-luxembourgeoise.html |
| WEB-13 | https://www.cpll.lu/ |
| WEB-14 | https://men.public.lu/en/systeme-educatif/langues-ecole-luxembourgeoise.html |
| WEB-15 | https://op.europa.eu/webpub/eac/education-and-training-monitor/en/country-reports/luxembourg.html |
| WEB-16 | https://en.wikipedia.org/wiki/Education_in_Luxembourg |
| WEB-17 | https://www.theglobaleconomy.com/Luxembourg/Internet_users/ |
| WEB-18 | https://www.statista.com/statistics/377741/household-internet-access-in-luxembourg/ |
| WEB-19 | https://www.press.lu/en/journalists/legal-texts-concerning-the-press-in-luxembourg/ |
| WEB-20 | https://smc.gouvernement.lu/fr/legislation/medias.html |
| WEB-21 | https://www.dlapiper.com/en/insights/publications/2025/10/newsflash-draft-bill-n8625 |
| WEB-22 | https://cnpd.public.lu/fr/actualites/international/2024/07/ai-act.html |
| WEB-23 | https://cms.law/en/int/expert-guides/ai-regulation-scanner/luxembourg |
| WEB-24 | https://www.chd.lu/en/node/3016 |
| WEB-25 | https://www.nortonrosefulbright.com/en-lu/knowledge/publications/a473a1c1/artificial-intelligence-regulation |
| WEB-26 | https://newspapersonline.com/luxembourg-newspapers-online/ |
| WEB-27 | https://luxtoday.lu/en/luxembourg-en/luxembourg-modernises-media-law |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Your system covers headline acceptability, topic classification, linguistic acceptability, and NER. For the topic classification component specifically, does your newsroom's editorial taxonomy map to standard international news categories (e.g., politics, sports, culture, economy), or does it include Luxembourg-specific beats — such as EU institutions and cross-border affairs (Grande Région, Moselle region), multilingual policy coverage, or local municipal politics — that a generic classification scheme might not capture?
A1: The system uses standard international news categories without major Luxembourg-specific sub-categories, so the topic taxonomy does not require bespoke regional classification.

Q2 [IC]: Luxembourgish journalism routinely mixes Luxembourgish with French, German, and sometimes English — proper nouns, official titles, legal terms, and direct quotes often appear in these other languages within an otherwise Luxembourgish article. Would your system need to handle NER and topic classification robustly on such code-switched text, or will the input always be monolingual Luxembourgish?
A2: Code-switching is a core operational requirement; input text will routinely contain French, German, and English lexical items embedded in Luxembourgish articles.

Q3 [OC]: For headline acceptability and linguistic acceptability judgments, whose standard of correctness should the system apply — formal written Luxembourgish as codified in official orthographic guidelines, or the more flexible register that working journalists and editors actually accept as professionally adequate? Would your editorial team and a formal language authority plausibly disagree on borderline cases?
A3: The system should apply the flexible professional-journalistic register rather than strict official orthography. The team acknowledges this creates genuine borderline cases where a formal language authority would disagree with an editorial judgment.

Q4 [OO]: Does your system need a single confidence threshold that triggers flagging, or must each task produce an independent, human-readable verdict so editors can understand exactly which criterion caused a flag and act on it selectively?
A4: Each task generates its own significance score; if any score crosses its pre-defined threshold the article is flagged, and editors can see which criterion triggered the review. Human-readable explanations are not generated by default but can be requested for recurring or complex cases.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | Topic taxonomy aligns with standard international categories (reducing IO risk), but the benchmark's GLUE-ported task set may not include a headline-consistency task or the specific combination of tasks this newsroom requires. |
| IC | HIGH | Code-switching is a core deployment requirement, and benchmark instances drawn from transferred/ported sources are unlikely to reflect the dense French–German–English mixing characteristic of Luxembourgish professional journalism. |
| IF | MODERATE | Deployment is text-only and the benchmark is text-only, which reduces signal-distribution mismatch; however, Luxembourgish is a low-resource language and the benchmark's tokenisation and orthographic conventions may not align with real newsroom copy. |
| OO | HIGH | The benchmark's acceptability and classification output categories were ported from a different cultural/linguistic context, and the deployment explicitly applies a professional-journalistic register rather than formal orthographic standards — creating systematic divergence between benchmark scoring logic and the ground truth the system is expected to approximate. |
| OC | HIGH | Ground-truth labels for acceptability tasks are unlikely to have been annotated by professional Luxembourgish journalists applying the flexible editorial register; annotator-population mismatch with working newsroom staff is a substantial risk, compounded by acknowledged borderline cases between formal and journalistic norms. |
| OF | LOWER | Both the benchmark (label output) and the deployment (per-task score with threshold) operate in a label/classification paradigm; the deployment's additional transparency layer (per-task scores visible to editors) is an enhancement rather than a modality mismatch. |

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
  "region": "Luxembourgish Professional Newsroom",
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
