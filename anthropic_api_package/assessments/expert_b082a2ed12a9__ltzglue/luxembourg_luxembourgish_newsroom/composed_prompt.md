I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **LTZGLUE: The First Natural Language Understanding Benchmark for Luxembourgish** is valid for use in **Luxembourgish Professional Newsroom — LtzGLUE Assessment**.

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
- **Domain**: Natural Language Understanding for a low-resource language
- **Languages**: lb
- **Porting Strategy**: mixed
- **Year**: 2025

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Test Case Categories (Input Ontology)
LTZGLUE covers eight NLU tasks spanning binary and multi-class sentence- and token-level
classification [Q11], including headline acceptability, sentiment analysis, linguistic
acceptability, NER, topic classification, intent detection, and textual entailment
[Q2, Q67]. The suite explicitly addresses all four tasks required by the target newsroom
deployment (HA, LA, TC, NER) [Q8]. Headline acceptability is formulated as a binary
classification of whether a headline matches the accompanying article body [Q15],
directly confirming this deployment-relevant subtask is in scope. Topic classification
uses five domain labels — SPORTS, CULTURE, TECHNOLOGY, BUSINESS, and ANIMALS [Q48,
Q153] — a deliberately narrow set that the deploying newsroom accepts as adequate given
its use of standard international categories [A1]. Topic classification is the easiest
and most stable task across all models [Q99]; RTE is the most challenging [Q103]. The
authors place LTZGLUE in roughly the same range as the nine-task English GLUE benchmark
[Q68], and emphasise that a substantial proportion of tasks are newly constructed for
LTZ rather than direct translations [Q69, Q70, Q71, Q108]. Prompt templates make task
definitions and label vocabularies explicit for zero-shot LLM evaluation [Q143, Q144,
Q145, Q146, Q148, Q149, Q150, Q151, Q152, Q153, Q154, Q155], and illustrative examples
are provided in Table 7 [Q124]. The intent detection task carries a register caveat:
it targets a voice-assistant domain for which no equivalent LTZ reference corpus exists
[Q55], limiting its relevance for the newsroom scenario.

### Content (Input Content)
Most textual data originate from a small number of publicly accessible Luxembourgish
sources dominated by RTL (news articles, radio transcripts, and user comments) [Q12,
Q16, Q24, Q46, Q74, Q135]; supplementary sources include the Luxembourgish Online
Dictionary (LOD) [Q30], Wikipedia, the Leipzig web crawl, LTZ chat rooms, and transcribed
political speeches from the Chambre des Députés [Q74]. The NER component merges an
automatically constructed Wikipedia/Wikidata corpus (JUDGEWEL) [Q34, Q38] with a
fully human-annotated RTL news-comment corpus [Q40, Q45], providing multi-domain
coverage. The RTE dataset originates from a machine-translated English corpus subsequently
post-edited with LLM assistance [Q60, Q66]; the intent detection dataset was translated
from English xSID using a machine-translated German training set [Q51, Q54]. Critically
for the newsroom deployment, the language community is small and data are concentrated
in a limited set of public domains [Q119]; the construction required a resource-conscious
approach combining dataset reuse with targeted annotation [Q109]. No source in the
registry is described as containing systematically code-switched text (French/German/
English embedded in Luxembourgish), and the language-ID filtering step used in topic
classification preprocessing [Q47] would tend to exclude code-switched sentences —
compounding the gap between benchmark instances and the deployment's core operational
requirement for robust code-switched input handling. The authors explicitly warn that
coverage across registers and demographic varieties is limited, with most sources
reflecting formal writing or institutional usage rather than informal or multilingual
contexts [Q112], and flag that models may reproduce dominant norms while under-
representing multilingual practices [Q120].

### Input Signal Form (Input Form)
All benchmark tasks use text-only inputs, matching the newsroom's text-only pipeline.
The LTZ-E1 encoders use a BPE tokeniser with a vocabulary of 50,368 trained on the
full pre-training set [Q128], with a maximum sequence length of 1,024 [Q129], following
the ModernBERT/Ettin recipe [Q125, Q126, Q127, Q130, Q131]. Pre-training data are
filtered to sentences with at least three whitespace-tokenised words [Q75], yielding
approximately 233M tokens across 11.7M sentences. LLM evaluation uses zero-shot
prompting with explicit label vocabularies rather than multiple-choice format [Q83,
Q84]. No script mismatch arises — Luxembourgish uses the Latin alphabet — but
orthographic variation is noted as extensive [Q7], and the benchmark's normalisation
pipeline (LOD-grounded for LA, OpenLID-filtered for TC) may not match the flexible
journalistic register of newsroom copy. Personal data preprocessing avoids directly
identifying information [Q116].

### Output Categories (Output Ontology)
The label ontologies across LTZGLUE tasks are a mix of purpose-built and ported
schemes. Linguistic acceptability uses four error subtypes — verb agreement, adjective
agreement, syntax deletion, and orthographic substitution — derived from LOD dictionary
data and the Spellchecker.lu resource [Q31], with the binary version collapsing all
error types into incorrect (0) vs. correct (1) [Q33]. Topic classification labels are
restricted to five domains [Q48, Q153]. NER uses a harmonised BIO tag set covering
PER, ORG, LOC (merged from GPE+LOC), DATE, and MISC [Q41, Q44, Q152]; the GPE/LOC
merger loses the distinction relevant for cross-border entities common in Luxembourgish
journalism. Binary label conventions (0 = False, 1 = True) are made explicit for HA
and RTE [Q147]. The LA error taxonomy is grounded in formal grammatical and orthographic
standards (LOD, Spellchecker.lu) [Q31], which the deployment elicitation explicitly
flags as misaligned with the professional-journalistic register the newsroom targets:
borderline cases where a formal language authority and editorial team would disagree
are not reflected in the label ontology. The intent detection label set targets a
voice-assistant domain [Q154, Q58], diverging from the newsroom's production context.

### Annotation Process (Output Content)
Annotation practices are heterogeneous in quality and transparency across tasks. For
sentiment analysis, 4,583 sentences were annotated by two native LTZ speakers, with
inter-annotator agreement at Cohen's Kappa of 0.45 (moderate) [Q25, Q26, Q27, Q28].
Intent detection translation was performed by a single LTZ native speaker with
additional native speakers consulted in uncertain cases [Q52]. The JUDGEWEL NER corpus
used LLMs as judges with minimal human verification [Q37]; the Lothritz et al. NER
dataset was fully human-annotated [Q42]. RTE verification used two LLM-assisted steps:
CHATGPT-5-MINI rated quality (removing ~25% of data) [Q63] and verified label
correctness (finding ~10% false labels) [Q64], with manual correction for cases where
LLM improvements altered semantics [Q65]. A brief acknowledgment of student assistant
annotators appears [Q114] but no demographic or professional-background detail is
provided. Critically, there is no evidence that any headline acceptability or linguistic
acceptability ground-truth labels were produced by professional journalists or editors
applying a journalistic register. The formal-orthographic grounding of the LA error
taxonomy [Q31] suggests the ground truth reflects linguistic prescriptivism rather than
editorial practice — a direct mismatch with the deployment's stated preference for a
flexible professional register. The authors acknowledge annotation decisions and label
distributions were influenced by resource constraints, introducing biases that "cannot
be fully quantified" [Q113].

### Output Modality (Output Form)
Models are evaluated using F1 scores across all eight tasks [Q93, Q96]. Encoder results
are averaged over three runs with standard deviations [Q89, Q96, Q158, Q159], with
Bayesian hyperparameter search and seed selection [Q137, Q138]. Macro-F1 is reported
for prompted LLMs, evaluated once without replication [Q96]. Malformed LLM outputs
are discarded before scoring [Q90, Q91]. Class-balanced loss (effective sample size,
beta 0.99) is applied for fine-tuning on imbalanced tasks (SA and LA) [Q92]. Full
per-task validation and test scores are tabulated [Q156]. The F1-based evaluation
framework maps naturally onto the deployment's per-task threshold-based flagging
architecture, and the benchmark's classification paradigm aligns with the deployment's
label-output mode. The macro-F1-only reporting for LLMs [Q96] may obscure task-level
label imbalance relevant to deployment calibration, and prompt sensitivity introduces
additional variability making LLM results indicative rather than directly comparable
to supervised scores [Q86, Q87].


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
| Q41 | 4 | output_ontology | "It covers a wider range of text types and registers, including informal and code-mixed writing, and focuses on four primary entity categories (PER, ORG, LOC, GPE)." |
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
| Q76 | 6 | input_ontology | "We evaluate a set of supervised encoder-based models that explicitly support LTZ, either through direct pre-training or multilingual coverage." |
| Q77 | 6 | output_form | "As a representative baseline, we include multilingual BERT (MBERT-base) (Devlin et al., 2019), which still remains widely used for multilingual transfer and low-resource evaluation." |
| Q78 | 6 | output_form | "We additionally evaluate a more recent multilingual BERT (MMBERT-base) variant with updated pre-training data and tokenisation." |
| Q79 | 6 | output_form | "To complement these general-purpose multilingual models, we include LUXEMBERT, a language-specific model trained on LTZ data (Lothritz et al., 2022), which provides a stronger inductive bias for the language's lexical and orthographic properties." |
| Q80 | 6 | output_form | "Finally, we evaluate XLM-RoBERTa (XLM-R-base) (Conneau et al., 2020), a large-scale multilingual model trained on substantially more data and languages than MBERT-base, and commonly used as a strong reference point for multilingual NLU." |
| Q81 | 6 | output_form | "In addition to supervised encoder-based models, we evaluate a set of LLMs in a prompt-based zero-shot setting. This group includes QWEN3-235B, LLAMA-3.3, GEMMA-3-27B, and GPT5-MINI, which represent a range of model sizes, training regimes, and degrees of multilingual coverage." |
| Q82 | 6 | output_form | "None of these models are fine-tuned on LTZGLUE, although some of the text data (RTL, Wikipedia) is very likely to have been processed during training." |
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
| Q115 | 9 | output_content | "This work is supported by the LLMs4EU project, funded by the European Union through the Digital Europe Programme (DIGITAL) under the grant agreement 10119847. FK and BP are supported by the ERC Consolidator Grant DIALECT 101043235." |
| Q116 | 9 | input_form | "The datasets included in this work are derived from publicly accessible sources that permit research use, and all preprocessing avoids the inclusion of directly identifying personal information." |
| Q117 | 10 | output_content | "However, some tasks draw on data originally produced in institutional or media contexts, which may reflect societal biases in representation." |
| Q118 | 10 | output_content | "These patterns can influence model behaviour and should be considered when deploying systems trained on LTZGLUE." |
| Q119 | 10 | input_content | "LTZ is a small language community, and linguistic data often originate from a limited set of public domains." |
| Q120 | 10 | output_content | "As a result, models may reproduce dominant norms while under-representing regional, sociolectal, or multilingual practices." |
| Q121 | 10 | output_content | "We therefore caution against using benchmark performance as evidence of cultural or demographic coverage." |
| Q122 | 10 | output_content | "Finally, although no sensitive content is intentionally included, automated filtering and preprocessing cannot guarantee the complete removal of harmful or offensive material." |
| Q123 | 10 | output_content | "Researchers using LTZGLUE are encouraged to inspect task-specific subsets and consider downstream implications, especially in public-facing settings." |
| Q124 | 12 | input_ontology | "For demonstration purposes, we present an example for each task in ltzGLUE in Table 7. The examples are intended to illustrate the task formulations and typical model inputs and outputs." |
| Q125 | 12 | input_form | "We follow the Ettin recipe (Weller et al., 2026), based on ModernBERT (Warner et al., 2025), for training hyperpameters and model architecture." |
| Q126 | 12 | input_form | "We train two sizes of LTZ-E1 models, mini and base, with 68M and 110M non-embedding parameters, respectively." |
| Q127 | 12 | input_form | "LTZ-E1-mini has 19 hidden layers, a hidden size of 512, an intermediate size of 768, and 8 attention heads, whereas LTZ-E1-base has 22 hidden layers, a hidden size of 768, an intermediate size of 1152, and 12 attention heads." |
| Q128 | 12 | input_form | "Both models share a GPTNeoXTokenizerFast tokenizer (Black et al., 2022), a BPE-based tokenizer, which we train on the entire pre-training set, using a minimum frequency of two and a vocabulary size of 50,368." |
| Q129 | 12 | input_form | "We use a constant batch size of 1024 packed sequences, where both models have a max sequence length of 1024." |
| Q130 | 12 | input_form | "We follow ModernBERT (Warner et al., 2025) and Ettin (Weller et al., 2026) in using the Warmup-Stable-Decay (WSD) scheduler (Zhai et al., 2022; Hu et al., 2024), though we use a shorter warmup and decay phase of 500 batches each, due to our smaller pre-training dataset size and larger number of epochs (10 vs. one)." |
| Q131 | 12 | input_form | "Again following ModernBERT and Ettin's recipe, we use the StableAdamW optimizer (Wortsman et al., 2023), with a peak learning rate of 3e-3 with a weight decay of 3e-4 for LTZ-E1-mini and 8e-4 with a weight decay of 1e-5 for LTZ-E1-base." |
| Q132 | 12 | input_form | "As our pre-training set is small, we" |
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
| Q143 | 14 | output_ontology | "You are an expert for the Luxembourgish language. I am giving you a sentence in Luxembourgish. You have to judge its quality and improve it while keeping the meaning intact. As output, write only the improved sentence or the original sentence if it is of very high quality." |
| Q144 | 14 | output_ontology | "You are an expert for the Luxembourgish language. I am giving you two texts in Luxembourgish. You have to judge their quality. As output, simply write 'low', 'medium' or 'high' depending on the quality of both sentences, nothing else." |
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
name: Luxembourgish Professional Newsroom — LtzGLUE Assessment
abbreviation: ltz_newsroom
benchmark: ltzglue
deployment_context:
  system_description: An LLM-powered editorial pipeline at Luxembourgish media outlets
    that evaluates articles across four tasks — headline acceptability (HA), linguistic
    acceptability (LA), topic classification (TC), and named entity recognition (NER)
    — generating per-task confidence scores and triggering a flag visible to editors
    when any single score breaches its pre-defined threshold. Human-readable explanations
    are not generated by default but can be requested for recurring or complex cases.
  decision_stakes: Auto-publish vs. manual editorial review. A false-negative (missed
    flag) passes substandard content to publication; a false-positive (unnecessary
    flag) creates editorial overhead. Both error directions have professional reputational
    consequences.
  primary_country: Luxembourg
  broader_geographic_context: 'Greater Region (Grande Région): cross-border context
    including Saarland (Germany), Lorraine (France), Wallonia and German-speaking
    Community (Belgium). Relevant because Luxembourgish professional journalism routinely
    covers and references cross-border entities, institutions, and persons.'
  deployment_mode: text-only pipeline; no multimodal inputs
target_population:
  description: Professional journalists, editors, and digital content managers employed
    at Luxembourgish media outlets. These are highly educated, media-sector professionals
    producing news primarily for a local Luxembourgish-speaking audience. They operate
    under editorial style standards that are distinct from formal orthographic prescriptivism,
    accepting a flexible professional-journalistic register as the norm.
  occupational_role: Professional newsroom staff (journalists, editors, digital content
    managers)
  institutional_setting: Luxembourgish media outlets (broadcast, print, and online
    news organisations)
  end_beneficiaries: Luxembourgish news-reading/listening public; indirectly, the
    broader Greater Region audience for Luxembourg-based media
  sub_national_variation: No meaningful sub-national demographic variation within
    the target population; variation is professional-contextual (editorial standards,
    outlet style guides) rather than geographic.
  population_size_context: Luxembourg population approximately 672,050 persons as
    of 1 January 2024 (STATEC official figure — [WEB-1]).
    The Luxembourgish-language media sector is small. Exact number of professional
    journalists holding press cards is not publicly aggregated in a single searchable
    figure; the Conseil de Presse issues official press cards and maintains a list
    of accredited journalists, but no aggregate count was found in this search pass.
    [NOT FOUND — searched Conseil de Presse site and Luxembourg media monitoring sources;
    no aggregate journalist headcount published in accessible form. Expert or direct
    Conseil de Presse inquiry required.]
  net_new_journalist_count_note: The Centre for Media Pluralism and Media Freedom
    (2024) notes 'a decrease in the number of journalists in Luxembourg despite the
    press aid scheme,' confirming the sector is under structural pressure (CMPF MPM
    2024 — [WEB-2]). This is deployment-relevant
    because a smaller, under-resourced newsroom population increases reliance on automated
    flagging and raises the cost of false positives.
languages:
  primary_operational_language: 'Luxembourgish (Lëtzebuergesch, ISO 639-1: lb)'
  code_switching_languages:
  - French
  - German
  - English
  code_switching_nature: Core operational requirement. Professional newsroom copy
    routinely embeds French, German, and English lexical items — proper nouns, official
    titles, legal and institutional terminology, direct quotes — within otherwise
    Luxembourgish sentences. This is not occasional but systematic and domain-constitutive.
  language_status: Luxembourgish is a national language of Luxembourg with approximately
    400,000 speakers worldwide. It is classified as a low-resource language in NLP
    research; data scarcity and limited tooling availability are structural constraints.
  co_official_languages_in_country:
  - French
  - German
  - Luxembourgish
  note: Luxembourg's trilingual administrative context directly shapes journalistic
    practice. Official documents, legislation, and EU institutional outputs appear
    in French and/or German, and are frequently cited or paraphrased in Luxembourgish
    articles — producing the code-switching that is the primary validity risk for
    this deployment.
writing_systems:
  script: Latin alphabet with diacritics specific to Luxembourgish (e.g., ë, é, â,
    ô, ê, ä, ü, ï, î, û, ù, à, è)
  orthographic_status: Ongoing standardisation. The current governing body for Luxembourgish
    orthographic standards is the Zenter fir d'Lëtzebuerger Sprooch (ZLS / Centre
    for the Luxembourgish Language), established by the Law of 20 July 2018 on the
    promotion of the Luxembourgish language. The most recent normative orthographic
    document is D'Lëtzebuerger Orthografie, finalised and published in November 2019
    by the ZLS. The ZLS also maintains the Lëtzebuerger Online Dictionnaire (LOD).
    Oversight of spelling and grammar rules is further reviewed by the Conseil permanent
    de la langue luxembourgeoise (CPLL), created in 1998. (Luxembourg Ministry of
    Education — [WEB-3];
    ZLS open data portal — [WEB-4]).
    Journalistic practice accepts a flexible register that deviates from strict prescriptive
    norms. Borderline cases between formal-authority correctness and editorial acceptability
    are acknowledged by the deployment team.
  orthographic_resources_in_benchmark: LTZGLUE's linguistic acceptability task is
    grounded in the Luxembourgish Online Dictionary (LOD) and Spellchecker.lu — formal
    prescriptive sources maintained or aligned with ZLS standards — creating a systematic
    mismatch with the journalistic register this deployment targets.
  rtl_concerns: None — Latin script only.
professional_register_notes: 'The deployment explicitly targets the professional-journalistic
  register rather than formal orthographic correctness. This register tolerates:

  - Orthographic variants accepted by working editors but flagged by formal spellcheckers

  - Code-switched proper nouns and titles left in French, German, or English

  - Headline conventions (sentence-case, punctuation, length norms) specific to Luxembourgish
  newsroom style

  - Direct-quote framing in source languages

  The editorial team acknowledges genuine borderline cases where a formal language
  authority (e.g., applying LOD/Spellchecker.lu standards) would disagree with a journalist''s
  acceptable usage. This divergence is the central OO and OC validity risk for the
  benchmark-to-deployment mapping.'
media_landscape:
  key_outlet_types: National broadcaster, daily newspapers (print and digital), online-only
    news portals, community and municipal media
  major_outlets: 'Key Luxembourgish-language and multilingual outlets confirmed from
    Conseil de Presse editor-in-chief registry and composition data (source: [WEB-5]
    and [WEB-6]):

    - RTL Lëtzebuerg (CLT-UFA SA) — dominant broadcaster and dominant LTZGLUE data
    source

    - Mediahuis Luxembourg S.A. (Luxemburger Wort / d''Wort) — major daily

    - Editpress Luxembourg s.a. (Tageblatt) — major daily (primarily German-language)

    - Edita S.A. (L''essentiel) — free daily (French-language dominant)

    - Lumédia S.A. (Le Quotidien)

    - Lëtzebuerger Journal

    - d''Lëtzebuerger Land

    - Woxx (independent weekly)

    - Zeitung vum Lëtzebuerger Vollek (ZLV)

    - Reporter.lu (online)

    - Radio 100,7 (public service broadcaster)

    - Paperjam (business media)

    Note: Several major outlets (Tageblatt, L''essentiel, Le Quotidien, Luxemburger
    Wort) publish primarily in German or French rather than Luxembourgish; Luxembourgish-primary
    outlets include RTL Lëtzebuerg and radio 100,7.'
  rtl_role_in_benchmark: RTL (RTL Lëtzebuerg) is the dominant data source across multiple
    LTZGLUE tasks (headline acceptability, topic classification, pre-training corpus).
    Benchmark instances are therefore substantially drawn from one outlet's editorial
    conventions, which may not generalise to other newsrooms deploying the system.
  editorial_taxonomy_alignment: The deployment newsroom uses standard international
    news categories (politics, sports, culture, economy, etc.) without Luxembourg-specific
    sub-categories. LTZGLUE's topic classification uses five labels (SPORTS, CULTURE,
    TECHNOLOGY, BUSINESS, ANIMALS) — a narrow subset. This is accepted as adequate
    by the deployment team for TC specifically.
  cross_border_coverage: Luxembourgish journalism regularly covers EU institutional
    affairs (European Parliament, European Commission, European Court of Justice —
    all Luxembourg-adjacent or Luxembourg-resident), Greater Region cross-border politics
    and economics, and municipal affairs in border communes. NER must handle entity
    names from French, German, and Belgian administrative contexts.
  net_new_press_regulation: 'The primary press regulatory framework comprises: (1)
    Law of 8 June 2004 on Freedom of Expression in Media (amended July 2024 to include
    online publications and right of reply); (2) Conseil de Presse (established 1979,
    self-regulatory body issuing press cards and maintaining code of ethics); (3)
    ALIA (Luxembourg Independent Authority for Audiovisual Media), responsible for
    broadcast regulation. The RTL network operates under a public service mandate
    (2024–2030 convention with the Luxembourg State). No AI-in-journalism specific
    guidance from the Conseil de Presse or ALIA was found in this search pass. (CMPF
    MPM 2024 — [WEB-2]; Conseil de Presse legal
    texts — [WEB-7]).'
sociolinguistic_context:
  multilingualism_character: Systemic, not incidental. Luxembourg's society and public
    life are structurally multilingual; Luxembourgish, French, and German each hold
    distinct functional roles (national identity, administration/law, historical/educational).
    English is increasingly present in business and EU contexts. Code-switching in
    journalism mirrors this societal multilingualism.
  language_attitudes: 'Luxembourgish carries strong national identity value. There
    is societal investment in its preservation and standardisation, evidenced by the
    Law of 20 July 2018 on the promotion of the Luxembourgish language, the appointment
    of a Commissioner for the Luxembourgish language (Pierre Reding, from 1 January
    2023), and the ZLS''s 2019 orthographic reform. [NEEDS VERIFICATION — deferred:
    below search budget; confirm current state of any active language policy debates
    affecting newsroom standards specifically, as opposed to general language promotion
    measures already documented]'
  diglossia_or_register_stratification: 'Functional register differentiation rather
    than classic diglossia: Luxembourgish used for national identity and informal/broadcast
    speech; French dominates formal law and official documents; German historically
    in print media (declining). Journalistic Luxembourgish occupies a distinct register
    bridging spoken informality and written formality.'
  standardisation_body: The Zenter fir d'Lëtzebuerger Sprooch (ZLS), established by
    Law of 20 July 2018, is the official body responsible for Luxembourgish orthographic
    standards. It publishes rules on spelling and grammar, maintains the LOD, and
    operates the Ortho-Trainer. The Conseil permanent de la langue luxembourgeoise
    (CPLL, created 1998) provides advisory opinions on ZLS-issued rules. The Institut
    national des langues Luxembourg (INLL), established by Law of 8 March 2023, is
    the national certification centre for Luxembourgish language diplomas (including
    the ZLO orthography certificate) but is distinct from the normative standards-setting
    function held by the ZLS. (Ministry of Education — [WEB-3];
    ZLS — [WEB-8]; INLL — [WEB-9])
infrastructure_notes:
  deployment_environment: Professional newsroom IT infrastructure in Luxembourg. High-reliability
    internet connectivity expected. Text-based pipeline; no mobile/low-bandwidth constraints.
  internet_penetration_luxembourg: 98.8% of total population as of end-2025 (674,000
    internet users out of ~682,000 population); household internet access was 99.06%
    in 2023 per Eurostat. Luxembourg is effectively at universal internet penetration.
    (DataReportal Digital 2026 Luxembourg — [WEB-10];
    Eurostat via Statista 2023 — [WEB-11]).
    This figure is not a deployment constraint; it confirms professional newsroom
    staff operate in a fully connected, high-bandwidth environment.
  digital_infrastructure_quality: Luxembourg is a high-income EU member state with
    advanced digital infrastructure. Internet penetration near-universal at ~99% household
    level (Eurostat 2023 — [WEB-11]).
    Luxembourg is also a major EU data centre hub. No deployment infrastructure constraints
    anticipated.
  nlp_tooling_availability_for_ltz: Limited relative to major European languages.
    LTZGLUE itself represents a landmark resource. Available tools include LuxemBERT,
    LTZ-E1 (mini/base) encoders, and multilingual models with LTZ coverage (mBERT,
    XLM-R). The officially recognised orthographic system (OLO) and associated tools
    (two spellcheckers, a PoS-tagger with tokenizer and lemmatizer, the LOD) are documented
    in the academic literature (Anastasiou, Springer 2023 — [WEB-12]).
    Tokenisation, orthographic normalisation, and code-switching handling remain open
    research problems for Luxembourgish.
  relevant_data_protection_regulation: 'GDPR applies as Luxembourg is an EU member
    state. Luxembourg''s implementing legislation is the Act of 1 August 2018 on the
    organisation of the CNPD and the general data protection framework. No Luxembourg-specific
    additions to the GDPR apply to data processing as such (confirmed: ''No national
    variations from the GDPR'' on most provisions). However, the Luxembourg Data Protection
    Act includes specific provisions for journalism: processing for journalistic purposes
    is partially exempt from data subject access rights, with access exercised through
    the CNPD in the presence of the Chairman of the Press Council (Article 62 of the
    Data Protection Act). The CNPD published guidelines on AI and data protection
    in 2023. The supervisory authority is the Commission nationale pour la protection
    des données (CNPD). (CMS Law Luxembourg — [WEB-13];
    CNPD annual report 2023 — [WEB-14])'
benchmark_task_coverage:
  tasks_required_by_deployment:
  - Headline Acceptability (HA)
  - Linguistic Acceptability (LA)
  - Topic Classification (TC)
  - Named Entity Recognition (NER)
  tasks_present_in_ltzglue:
  - Headline Acceptability (HA) — confirmed, formulated as binary headline-body match
    classification
  - Linguistic Acceptability Binary (LA BINARY) — confirmed
  - Linguistic Acceptability Multi-class (LA MULTI) — confirmed
  - Named Entity Recognition (NER) — confirmed
  - Topic Classification (TC) — confirmed, five-label scheme
  - Sentiment Analysis (SA) — present but not a deployment requirement
  - Intent Detection (ID) — present but not a deployment requirement (voice-assistant
    domain, low deployment relevance)
  - Recognising Textual Entailment (RTE) — present but not a deployment requirement
  task_coverage_verdict: All four deployment-required tasks are represented in LTZGLUE.
    IO coverage gap is lower than initially anticipated; however, coverage in the
    benchmark does not guarantee validity for deployment — see register, annotator,
    and code-switching gaps below.
  headline_acceptability_formulation: 'Binary: does the headline match the accompanying
    article body? Negative examples constructed by TF-IDF-based headline swapping
    with temporal and structural mismatch constraints. Ground truth is algorithmically
    constructed, not annotated by professional journalists.'
  topic_classification_label_set: 'SPORTS, CULTURE, TECHNOLOGY, BUSINESS, ANIMALS
    — five labels. Deployment team accepts this as adequate. Notable absence of POLITICS/GOVERNMENT
    label. [NEEDS VERIFICATION — deferred: below search budget; the absence of a POLITICS
    label in the RTL editorial taxonomy is documented in benchmark construction (RTL
    categories used as source) but the specific editorial decision rationale was not
    found in accessible sources. Low-priority for scoring given deployment team acceptance
    of the five-label set.]'
  ner_entity_taxonomy:
    harmonised_tags:
    - PER
    - ORG
    - LOC (merged GPE+LOC)
    - DATE
    - MISC
    gpe_loc_merger_risk: 'The merger of GPE (geopolitical entity) and LOC (location)
      into a single LOC tag loses the distinction between countries/administrative
      regions (cross-border entities: Belgium, France, Germany, EU institutions) and
      physical locations. This is a meaningful gap for Luxembourgish professional
      journalism, which frequently references cross-border administrative and governmental
      entities.'
    cross_border_entity_coverage: '[NEEDS VERIFICATION — deferred: below search budget;
      determining whether JUDGEWEL/Lothritz NER corpora contain sufficient EU institution
      and Greater Region administrative entity instances requires direct corpus inspection
      not accessible via web search. Requires expert elicitation or corpus access.]'
    multilingual_proper_noun_handling: '[NEEDS VERIFICATION — deferred: likely unsearchable
      (requires corpus inspection); assessing BPE tokeniser handling of French/German/English
      proper nouns in Luxembourgish text requires empirical analysis of the LTZ-E1
      vocabulary and tokenisation outputs, not available via public web search.]'
  la_label_ontology_alignment:
    benchmark_grounding: LOD (Luxembourgish Online Dictionary, maintained by ZLS)
      and Spellchecker.lu — formal prescriptive sources aligned with ZLS's November
      2019 orthographic standard (D'Lëtzebuerger Orthografie)
    deployment_target: Flexible professional-journalistic register; borderline cases
      between formal correctness and editorial acceptability explicitly acknowledged
    alignment_verdict: Systematic misalignment. The benchmark's LA labels operationalise
      formal orthographic correctness per ZLS/LOD standards; the deployment's ground
      truth is editorial acceptability. These diverge on a non-trivial proportion
      of real newsroom copy.
    error_subtypes_in_benchmark:
    - Verb agreement
    - Adjective agreement
    - Syntax deletion
    - Orthographic substitution
    register_relevant_error_types_not_covered: '[NEEDS VERIFICATION — deferred: likely
      unsearchable (lived practice); identifying which journalistic acceptability
      judgements fall outside the four LA error subtypes requires elicitation from
      working journalists and editors, not web-searchable documentation.]'
annotator_population_assessment:
  known_annotator_profiles:
    sentiment_analysis: Two native LTZ speakers; Cohen's Kappa 0.45 (moderate agreement);
      student assistant acknowledgment without demographic detail
    intent_detection: One native LTZ speaker (primary); additional native speakers
      consulted for uncertain cases
    ner_judgewel: LLM judges with minimal human verification
    ner_lothritz: Fully human-annotated (professional background of annotators not
      documented)
    rte: LLM-assisted post-editing and verification; manual correction for semantic
      conflicts
    headline_acceptability: Algorithmically constructed; no human annotation of ground
      truth labels
    linguistic_acceptability: Algorithmically constructed from LOD data and Spellchecker.lu;
      no direct human annotation documented
  professional_journalist_involvement: No evidence that any LTZGLUE ground-truth labels
    — particularly for HA and LA — were produced or validated by professional journalists
    or editors applying a journalistic editorial register. This is the primary OC
    risk for deployment validity.
  annotator_demographic_transparency: Insufficient. No age, professional background,
    regional dialect, or institutional affiliation information provided for any annotator
    group beyond 'native LTZ speaker' or 'student assistant.'
  resource_constraint_bias_acknowledgment: Authors explicitly acknowledge that annotation
    decisions and label distributions were influenced by resource constraints, introducing
    biases that 'cannot be fully quantified.'
code_switching_assessment:
  operational_requirement: HIGH — code-switching (French, German, English within Luxembourgish
    text) is a core, non-optional feature of the deployment input space
  benchmark_coverage: NOT SYSTEMATICALLY DOCUMENTED as present. OpenLID language-ID
    filtering in TC preprocessing actively excludes non-Luxembourgish-identified content,
    which would remove most code-switched sentences from that task's data. Most benchmark
    sources reflect formal/institutional Luxembourgish. The Lothritz et al. NER corpus
    notes coverage of 'informal and code-mixed writing' but this is one sub-component.
  tokenisation_risk: The LTZ-E1 BPE tokeniser (vocabulary size 50,368) was trained
    on the pre-training corpus. Code-switched French/German/English tokens may be
    poorly represented in the vocabulary, leading to aggressive subword fragmentation
    of proper nouns and technical terms embedded in Luxembourgish text.
  language_id_filter_risk: The OpenLID filtering step used in topic classification
    preprocessing would tend to exclude sentences with heavy code-switching, meaning
    TC training/evaluation data is likely more monolingual than real newsroom copy.
  web_search_target: LTZGLUE code-switching Luxembourgish French German NLP benchmark;
    Lothritz 2022 LTZ NER code-mixed corpus coverage
data_provenance_notes:
  primary_benchmark_sources:
  - RTL Lëtzebuerg (news articles, radio transcripts, user comments) — dominant source
  - Luxembourgish Online Dictionary (LOD)
  - Wikipedia (Luxembourgish edition)
  - Leipzig Corpus Collection (web crawl, 1M sentences)
  - Luxembourgish chat rooms (Webchat)
  - Chambre des Députés transcripts (political speeches and debates)
  - Podcasts (transcribed)
  single_outlet_dominance_risk: RTL Lëtzebuerg is the dominant data source across
    HA, TC, SA, and the pre-training corpus. Benchmark instances therefore substantially
    reflect one outlet's editorial conventions, style, and topic distribution. Deploying
    outlets with different editorial norms, topic emphases, or style guides may experience
    systematic performance degradation not captured by benchmark scores. RTL also
    operates under a public service mandate (2024–2030 State convention) confirmed
    by CMPF 2024, which may shape its editorial conventions further — [WEB-2].
  llm_involvement_in_data_construction: 'LLM assistance used for: RTE post-editing
    (ChatGPT-5.1), RTE quality verification (ChatGPT-5-MINI), RTE label correctness
    verification (ChatGPT-5-MINI), JUDGEWEL NER judging. Potential pre-training data
    contamination for evaluated LLMs cannot be ruled out (RTL, Wikipedia likely in
    major LLM pre-training corpora).'
  synthetic_data_risk: MODERATE — primary sources are authentic institutional/journalistic
    texts, reducing wholesale synthetic-data risk; however, LLM-assisted RTE post-editing
    and NER judging introduce synthetic-generation artefacts in specific tasks.
  authentic_newsroom_copy_coverage: '[NEEDS VERIFICATION — deferred: below search
    budget; determining whether non-RTL newsroom copy is represented in LTZGLUE requires
    direct correspondence with benchmark authors or corpus inspection. The Conseil
    de Presse composition data confirms the full range of Luxembourg outlets (Tageblatt,
    Woxx, Reporter.lu, etc.) but none are documented as LTZGLUE data sources.]'
regulatory_and_ethical_context:
  applicable_data_protection_law: 'GDPR (Regulation (EU) 2016/679) applies directly.
    Luxembourg implementing legislation: Act of 1 August 2018 on the organisation
    of the CNPD and the general data protection framework. No national additions to
    core GDPR provisions. Journalism-specific exemption: processing solely for journalistic
    purposes is partially exempt from data subject access rights under the Data Protection
    Act (Article 62); access is exercised through the CNPD in the presence of the
    Press Council Chairman. The CNPD is the competent supervisory authority. DPIA
    required where processing with new technologies poses high risk to data subjects''
    rights and freedoms. (CMS Law Luxembourg — [WEB-13];
    CNPD — [WEB-15])'
  press_regulation: 'Primary regulatory instruments: (1) Law of 8 June 2004 on Freedom
    of Expression in Media (amended July 2024, extending to online publications and
    adding right of reply — CMPF 2024 [WEB-2]);
    (2) Conseil de Presse (self-regulatory body, established 1979, issues press cards,
    maintains Code of Ethics — [WEB-7]);
    (3) ALIA (Luxembourg Independent Authority for Audiovisual Media) regulates broadcast;
    (4) RTL operates under a 2024–2030 public service convention with the State. No
    AI-in-journalism specific guidance from Conseil de Presse or ALIA was found in
    this search pass.'
  ai_in_journalism_standards: The CNPD published guidelines on AI and data protection
    in 2023, covering general principles rather than journalism-sector specifics (CNPD
    Annual Report 2023 — [WEB-14]).
    RTL established an internal ethics committee covering content management (CMPF
    2024). No Luxembourg-specific journalistic code of ethics provision or professional
    standard specifically addressing automated content moderation or AI-assisted editorial
    decisions was found. [NOT FOUND — searched CNPD, Conseil de Presse, and CMPF sources;
    AI-in-journalism guidance appears absent at both Luxembourg and sector-specific
    level as of mid-2024.]
  eu_ai_act_relevance: The EU AI Act (Regulation (EU) 2024/1689, in force 1 August
    2024) applies to Luxembourg as an EU member state. An automated editorial flagging
    system of the type described is unlikely to fall under the Annex III high-risk
    categories (which cover critical infrastructure, employment decisions, biometric
    systems, law enforcement, migration, and democratic processes). The system most
    plausibly falls in the 'limited risk' or 'minimal risk' tier. However, the Commission's
    practical classification guidelines for high-risk vs. non-high-risk use cases
    were due by 2 February 2026 (Article 6(5) — [WEB-16]);
    deployers should verify once those guidelines are published. The AI Act's transparency
    obligation requiring labelling of AI-generated text published to inform the public
    on matters of public interest (Article 50) is potentially relevant if the system
    generates any editorial text (currently it only classifies). High-risk AI rules
    take effect August 2026–2027. (European Commission AI Act overview — [WEB-17])
dimension_risk_summary:
  IC_code_switching:
    priority: HIGH
    assessment: Benchmark instances are not documented as containing systematic code-switching.
      OpenLID filtering in TC actively excludes code-switched text. Deployment input
      space is code-switched by design. This is the largest single validity gap between
      benchmark and deployment.
    flagged_for_web_search: true
  OO_register_label_ontology:
    priority: HIGH
    assessment: LA label ontology grounded in formal prescriptive standards (LOD,
      Spellchecker.lu, both aligned with ZLS's November 2019 D'Lëtzebuerger Orthografie)
      rather than journalistic register. HA labels algorithmically constructed without
      professional editorial validation. Systematic divergence between benchmark scoring
      logic and deployment ground truth is documented and acknowledged.
    flagged_for_web_search: true
  OC_annotator_mismatch:
    priority: HIGH
    assessment: No evidence of professional journalist or editor involvement in any
      LTZGLUE annotation. Prescriptive-linguistic grounding of LA labels implies annotator
      norms are formal-orthographic rather than editorial. Resource-constraint bias
      acknowledged but not quantified.
    flagged_for_web_search: true
  IO_task_coverage:
    priority: MODERATE
    assessment: All four deployment-required tasks (HA, LA, TC, NER) are present in
      LTZGLUE. HA is formulated as headline-body match, directly relevant. TC label
      set is narrow (5 labels) but accepted by deployment team. NER GPE/LOC merger
      creates cross-border entity coverage gap.
    flagged_for_web_search: false
  IF_tokenisation_orthography:
    priority: MODERATE
    assessment: Text-only modality match. BPE tokeniser trained on LTZ corpus but
      may handle code-switched tokens poorly. Benchmark normalisation pipeline (LOD-grounded,
      aligned with ZLS 2019 standards) likely does not match flexible journalistic
      register. Orthographic variation extensively noted.
    flagged_for_web_search: true
  OF_output_modality:
    priority: LOWER
    assessment: Both benchmark (F1/classification) and deployment (per-task score
      with threshold) operate in classification paradigm. Deployment's per-task transparency
      layer is an enhancement, not a modality mismatch. Macro-F1-only LLM reporting
      may obscure label-imbalance effects relevant to threshold calibration.
    flagged_for_web_search: false
flagged_gaps_for_web_search:
- gap_id: 1
  dimension: IC
  priority: HIGH
  description: 'Code-switching coverage in benchmark instances: determine whether
    any LTZGLUE task instances — particularly HA, LA, NER, TC — contain code-switched
    text (French/German/English embedded in Luxembourgish), and whether the OpenLID
    filtering step systematically excluded such instances from TC.'
  search_target: LTZGLUE Luxembourgish code-switching French German English NLP benchmark
    instances evaluation coverage
  search_status: DEFERRED — no targeted search executed on this specific gap in this
    pass. The benchmark documentation itself (Q112, Q120, Q47) provides strong circumstantial
    evidence of systematic exclusion; a targeted arXiv/ACL search for post-publication
    analysis would be the recommended next step.
- gap_id: 2
  dimension: OC
  priority: HIGH
  description: 'Annotator profile for acceptability tasks: determine whether any HA
    or LA ground-truth labels were produced or validated by professional journalists
    or editors, and whether any annotators were applying journalistic rather than
    prescriptive-linguistic standards.'
  search_target: LTZGLUE annotation professional journalists newsroom editors linguistic
    acceptability headline Luxembourgish NLP annotator background
  search_status: DEFERRED — no targeted search executed; benchmark documentation (Q114,
    Q113) already establishes absence of documented professional journalist involvement.
    A direct author inquiry or supplementary materials review would be required.
- gap_id: 3
  dimension: OO
  priority: HIGH
  description: 'Journalistic register vs. formal orthographic standards: document
    the degree of divergence between LOD/Spellchecker.lu prescriptive standards and
    working journalistic Luxembourgish norms; identify whether any style guides or
    editorial standards documents exist for Luxembourgish-language journalism.'
  search_target: Luxembourgish journalistic register orthographic variation professional
    writing norms editorial standards Lëtzebuergesch press style guide
  search_status: PARTIALLY ADDRESSED — the ZLS standardisation body and its normative
    documents (D'Lëtzebuerger Orthografie, November 2019) are now confirmed. No Luxembourgish-specific
    journalism style guide (distinct from the Conseil de Presse Code of Ethics) was
    found. The divergence between ZLS prescriptive norms and journalistic register
    remains unquantified and requires expert elicitation.
- gap_id: 4
  dimension: IC
  priority: HIGH
  description: 'NER entity type coverage for Greater Region and EU institutional context:
    determine whether LTZGLUE NER corpora contain sufficient instances of EU institution
    names, Greater Region administrative entities, and multilingual proper nouns to
    support professional journalism NER.'
  search_target: Luxembourgish NER named entity recognition EU institutions Greater
    Region cross-border entities French German proper nouns JUDGEWEL Lothritz corpus
  search_status: DEFERRED — no targeted search executed; requires direct corpus inspection.
    Cannot be resolved via public web search.
- gap_id: 5
  dimension: IF
  priority: MODERATE
  description: 'Orthographic normalisation pipeline in benchmark: determine whether
    LTZGLUE task data was normalised to a single orthographic standard (LOD-grounded),
    and whether that standard matches or diverges from the flexible register found
    in professional Luxembourgish newsroom copy.'
  search_target: Luxembourgish orthographic variation normalisation LTZGLUE benchmark
    LOD Spellchecker.lu written standards Lëtzebuergesch spelling journalistic register
  search_status: PARTIALLY ADDRESSED — confirmed that ZLS published D'Lëtzebuerger
    Orthografie in November 2019 as the current normative standard, and that the LOD
    is maintained by ZLS. The benchmark's use of LOD/Spellchecker.lu grounds it in
    this standard. Quantification of divergence from journalistic register remains
    unsearchable.
- gap_id: 6
  dimension: IC
  priority: MODERATE
  description: 'Data provenance and RTL outlet dominance: assess whether the dominance
    of RTL Lëtzebuerg as a data source creates systematic style/register/topic biases
    that limit benchmark validity for newsrooms with different editorial conventions.'
  search_target: LTZGLUE RTL Lëtzebuerg data source dominance Luxembourgish NLP benchmark
    representativeness outlet diversity
  search_status: PARTIALLY ADDRESSED — confirmed RTL's role and its public service
    mandate (2024–2030 State convention). Full list of active Luxembourg outlets confirmed
    from Conseil de Presse data. No post-publication analysis of RTL-dominance effects
    on benchmark performance across outlet types was found.
- gap_id: 7
  dimension: OO
  priority: MODERATE
  description: 'Topic classification label set coverage: determine whether the five-label
    TC taxonomy (SPORTS, CULTURE, TECHNOLOGY, BUSINESS, ANIMALS) covers the topic
    distribution of the deploying newsroom''s output, and whether the absence of a
    POLITICS/GOVERNMENT label creates a coverage gap.'
  search_target: LTZGLUE topic classification label set POLITICS GOVERNMENT Luxembourgish
    news RTL editorial categories coverage gap
  search_status: DEFERRED — below search budget. Deployment team has accepted the
    five-label set; gap is acknowledged but not scored as high priority.
net_new_fields:
  zls_normative_document: The current official Luxembourgish orthographic standard
    is D'Lëtzebuerger Orthografie, finalised and published in November 2019 by the
    Zenter fir d'Lëtzebuerger Sprooch (ZLS). All digital tools including the LOD and
    Ortho-Trainer comply with this 2019 standard. This is directly deployment-relevant
    because the LTZGLUE LA task is grounded in LOD data, and the 2019 ZLS standard
    is the prescriptive anchor against which the benchmark's 'correct' labels are
    calibrated — confirming and dating the formal-orthographic mismatch with journalistic
    register. (Luxembourg Ministry of Education — [WEB-3])
  luxembourg_journalist_sector_trend: 'The CMPF Media Pluralism Monitor 2024 notes
    a decrease in the number of journalists in Luxembourg despite the press aid scheme,
    and the Market Plurality area scores in the medium-high risk band. This structural
    pressure on the journalist workforce is deployment-relevant: reduced newsroom
    headcount increases reliance on automated editorial tools and raises the operational
    cost of false positives. (CMPF MPM 2024 — [WEB-2])'
  rtl_ethics_committee: RTL Luxembourg established an internal Ethics Committee composed
    of content managers (news and non-news) and editorial team members in accordance
    with the RTL Luxembourg Journalists' Charter. This is the closest institutional
    structure to an editorial AI governance body at the dominant LTZGLUE data source,
    and may be the relevant stakeholder for deployment validation of benchmark labels
    against journalistic register norms. (CMPF MPM 2024 — [WEB-2])
  cnpd_ai_guidance_2023: The CNPD published guidelines on artificial intelligence
    and data protection in 2023, as part of its annual work programme. These are general-purpose
    AI/GDPR guidance documents rather than media-sector-specific, but they constitute
    the applicable regulatory soft-law framework for AI system deployment in Luxembourg.
    Deployers of the LtzGLUE-based system should review CNPD AI guidance as part of
    any DPIA. The CNPD is also actively developing AI compliance tools (DAAZ platform)
    and participates in the Global Network of AI Supervisory Authorities (GNAIS).
    (CNPD Annual Report 2023 — [WEB-14])
  eu_ai_act_timeline_note: The EU AI Act (Regulation (EU) 2024/1689) entered into
    force 1 August 2024. Rules on prohibited AI practices applied from 2 February
    2025. Rules on general-purpose AI transparency apply from August 2025. Rules on
    high-risk AI systems apply from August 2026 (Annex III systems) and August 2027
    (Annex I systems). The Commission's practical classification guidelines for high-risk
    vs. non-high-risk use cases were due by 2 February 2026. An automated editorial
    classification/flagging system of the type deployed is most likely 'minimal risk'
    under the current framework, but deployers should re-assess once the Commission's
    Article 6 practical guidelines are published. (EU AI Act official overview — [WEB-17];
    Article 6 Service Desk — [WEB-16])
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://statistiques.public.lu/en/actualites/2024/stn16-population-2024.html |
| WEB-2 | https://cmpf.eui.eu/country/luxembourg/ |
| WEB-3 | https://men.public.lu/en/grands-dossiers/systeme-educatif/promotion-langue-luxembourgeoise.html |
| WEB-4 | https://data.public.lu/en/organizations/zenter-fir-dletzebuerger-sprooch/ |
| WEB-5 | https://www.press.lu/en/mediatic-landscape-in-luxembourg/editors-in-chief/ |
| WEB-6 | https://www.press.lu/en/who-we-are/composition-cdp/ |
| WEB-7 | https://www.press.lu/en/journalists/legal-texts-concerning-the-press-in-luxembourg/ |
| WEB-8 | http://zls.lu/ |
| WEB-9 | https://www.inll.lu/en/ |
| WEB-10 | https://datareportal.com/reports/digital-2026-luxembourg |
| WEB-11 | https://www.statista.com/statistics/377741/household-internet-access-in-luxembourg/ |
| WEB-12 | https://link.springer.com/content/pdf/10.1007/978-3-031-28819-7_26.pdf |
| WEB-13 | https://cms.law/en/int/expert-guides/cms-expert-guide-to-data-protection-and-cyber-security-laws/luxembourg |
| WEB-14 | https://cnpd.public.lu/en/actualites/national/2024/09/rapport-annuel-2023.html |
| WEB-15 | https://cnpd.public.lu/en.html |
| WEB-16 | https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6 |
| WEB-17 | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai |

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
  "region": "Luxembourgish Professional Newsroom — LtzGLUE Assessment",
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
