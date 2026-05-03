I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **MASSIVE: A 1M-Example Multilingual Natural Language Understanding Dataset with 51 Typologically Diverse Languages** is valid for use in **Ethiopian Intercity Travelers — Amharic-Language Booking Bot**.

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

- **Name**: massive
- **Full Name**: MASSIVE: A 1M-Example Multilingual Natural Language Understanding Dataset with 51 Typologically Diverse Languages
- **Domain**: Multilingual natural language understanding — intent classification and slot filling
- **Languages**: af, am, ar, az, bn, cy, da, de, el, en, es, fa, fi, fr, he, hi, hu, hy, id, is, it, ja, jv, ka, km, kn, ko, lv, ml, mn, ms, my, nb, nl, pl, pt, ro, ru, sl, sq, sv, sw, ta, te, th, tl, tr, ur, vi, zh-CN, zh-TW
- **Porting Strategy**: translation
- **Year**: 2022

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
MASSIVE covers "18 domains, 60 intents, and 55 slots" [Q1] built around global
commercial virtual assistant use cases, designed to "benchmark today's systems" by
aligning with "existing languages available in major virtual assistants" [Q16]. The
task taxonomy focuses on "the general multi-domain NLU task" [Q12], with the corpus
"primarily consist[ing] of interrogatives (i.e., questions) and imperatives (commands
or requests)" [Q30] and "relatively few declarative utterances" [Q31]. The dataset
documents rich typological variation including word order (39 subject-initial languages,
no object-initial languages) [Q34, Q35], verb morphology patterns [Q37], imperative
morphology [Q38], and politeness distinctions (21 languages with two-way formal/informal
distinctions [Q46], 8 with more than two levels [Q47], 7 with avoidance strategies [Q48]).
Slot-level localization decisions — whether workers elected to translate, localize, or
keep values unchanged — are included in metadata [Q58], providing transparency into
which examples underwent cultural adaptation. No Ethiopia-specific intent categories
exist: operator-specific intents (route-closure rebooking, seat-class selection),
Ethiopian holiday surcharge events, or Birr-denominated fare query types are absent
from the 60-intent taxonomy. The labeling schema is "relatively simple when compared
with hierarchical labeling schemata or flat schemata with more intent and slot options"
[Q108], which the paper explicitly acknowledges as a limitation.

### Input Content
Every non-English datapoint in MASSIVE — including Amharic — derives from localizing
"the English-only SLURP dataset" via professional translators [Q2, Q4], tracing back
to "the NLU Evaluation Benchmarking Dataset, with 25k utterances across 18 domains"
[Q9]. The original seed utterances "were originally created through crowd-sourcing,
not from a real virtual assistant, which introduces artificialities" [Q106]. Language
selection combined cost and worker availability constraints [Q15], typological diversity
targets using WALS genera [Q17], and internet-resource proxies (Wikipedia eigenvector
centrality, tweets, book translations) [Q19]. A paraphrased held-out subset was
created for the MMNLU-22 competition, "resulting in new, more challenging utterances,
including 49% more slots per utterance" [Q39]. The dataset was "collected using a
customized workflow powered by Amazon MTurk" with a vendor pool [Q41, Q42].
Crucially, Amharic slot instances are translated from English-origin utterances and
will not contain Ethiopian calendar month references (Meskerem, Tikimt), local city
name variants (Adama/Nazret, Mek'ele), Birr-denominated fares, or intercity transport
terminology. "Allowing the worker to decide on translation versus localization of slot
entities added further noise" [Q107], and per-language data quantities are "relatively
small at 19.5k total records and 11.5k records for training" [Q103]. Mandarin Chinese
was collected twice to capture traditional and simplified character sets [Q22], signaling
attention to orthographic variants, but no analogous split was made for Amharic
speaker sub-populations.

### Input Form
MASSIVE is text-only, with train/dev/test/heldout splits totalling approximately
996k labeled utterances [Q3]. The dataset covers 21 distinct scripts [Q25], with
28 languages (including English) using Latin alphabet variants [Q26]; Arabic script
covers three languages, Cyrillic two, and "the remaining 18 languages have 'unique'
scripts" [Q27]. Amharic's Ethiopic (Ge'ez) script falls in the unique-script category.
Preprocessing for non-space-delimited languages such as Japanese and Chinese involved
inserting spaces between characters [Q80, Q93, Q94, Q96], and Thai's optional spacing
was noted as providing an incidental model advantage [Q91]. The collection system
"did not have a robust method to preserving or denoting native tokenization practices"
[Q109], which "results in potentially easier (larger chunks to predict slot labels)
or harder (each character individually predicted) tasks" [Q110]. For Khmer, "workers
had a difficult time adapting their translations and localizations to properly-slotted
outputs given the space-optional nature of the language" [Q92]. The deployment
context is also text-only smartphone input in Ethiopic script, making the modality
alignment strong — but Amharic-specific tokenization handling is not explicitly
documented. Script diversity was explicitly sought "to drive experimentation in
tokenization and normalization" [Q20], leaving more sophisticated approaches to
future work [Q81].

### Output Ontology
The output label set comprises 60 intents and 55 slot types across 18 domains [Q1].
In text-to-text mode, "the decoder output is a sequence of labels (including the Other
label) for all of the tokens followed by the intent" [Q73]. Judgment metadata —
covering semantic intent match, slot-label match, grammaticality and naturalness,
spelling, and language identification — is included in the dataset [Q63, Q64].
The localization decision (translate/localize/unchanged) per slot is also stored in
metadata [Q58]. The benchmark's output taxonomy was designed for global virtual
assistant coverage and does not include operator-specific slot types relevant to
Ethiopian intercity transport (e.g., `operator_name`, `seat_class`, `route_closure_reason`,
Ethiopian-calendar date expressions). The paper acknowledges the schema is "relatively
simple when compared with hierarchical labeling schemata or flat schemata with more
intent and slot options" [Q108], directly limiting coverage of domain-specific slot
types needed for Sky Bus/Selam/Ride booking contexts.

### Output Content
The annotation workflow used a vendor pool model starting with five vendors reduced
to three based on engagement and resource availability [Q43, Q44, Q45], with worker
qualification via a fluency test (listening-based, multiple-choice) for translators
[Q51] and a three-judgment test for quality raters [Q52], supplemented by a
translator quiz using "customized local-language examples" [Q53]. Workers self-certified
native fluency or high proficiency [Q122]. Quality monitoring included alarms for
high rejection rates, high slot-deletion rates, and high rates of English tokens,
with suspected machine-translation workers removed [Q65, Q66]. Annotator demographics —
specifically whether Amharic translators represent urban Addis speakers,
Amhara-region speakers, or Amharic-as-L2 speakers — are not disclosed. No mechanism
was in place to capture or represent code-switching behavior with Oromo or Tigrinya,
and "some low-quality utterances, both in the seed data and in the translations"
are acknowledged [Q104], addressable through judgment-score filtering [Q105] at
the cost of further reducing dataset size. The paper notes that "the lack of labeled
data for training and evaluation, particularly data that is realistic for the task
and that is natural for each given language" [Q6] is a central challenge the dataset
attempts to address — but its translation-from-English pipeline means Amharic
instances reflect English-language pragmatics translated into Amharic, not
naturalistic Amharic utterances from Ethiopian intercity travelers.

### Output Form
The benchmark reports three primary metrics: "exact match accuracy, intent
classification accuracy, and slot-filling F1 score" [Q5], with slot F1 computed
as micro-averaged across locales [Q84, Q88] and 95% confidence intervals assuming
normal distributions [Q89]. Results are provided for full-dataset and zero-shot
configurations across all three model types (XLM-R, mT5 Encoder-Only, mT5
Text-to-Text) [Q83], with zero-shot exact match "25–37 points worse" than
full-dataset [Q85] and dramatically higher variance (44-point gap between best
and worst locales in mT5 Text-to-Text zero-shot [Q86]). A Pearson correlation of
0.54 between XLM-R pretraining data quantity and zero-shot exact match [Q87]
suggests Amharic — a lower-resource Ethiopic-script language — will fall in the
lower-performance tier, consistent with the finding that "Germanic genera and
Latin scripts performed the best overall" [Q98] and that Icelandic underperformed
due to limited pretraining data [Q100]. Per-language breakdowns are provided for
exact match [Q126], intent accuracy [Q127], and slot-filling F1 [Q128], with
further breakdowns by script, language family, word order, politeness, and
morphological features [Q119, Q129, Q131, Q132]. The output format — intent
label plus slot-filled sequence — directly matches what an intent-classification
and slot-filling booking system requires, representing strong output-form alignment
with the deployment context [Q68, Q69, Q70, Q71, Q72, Q73].

### Stated Limitations
The paper explicitly acknowledges: small per-language training sets [Q103];
low-quality utterances in seed data and translations [Q104]; artificial origins
in crowd-sourced English data [Q106]; noise introduced by worker localization
decisions [Q107]; a simple labeling schema lacking hierarchical or extended slot
options [Q108]; absence of robust native tokenization handling [Q109, Q110];
and potential performance degradation for low-resource and non-Latin-script
languages [Q98, Q100]. The paper does not address Amharic code-switching with
Oromo or Tigrinya, Ethiopian calendar date slot coverage, Ethiopian city name
variants, or Birr fare normalization as limitations.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MASSIVE contains 1M realistic, parallel, labeled virtual assistant utterances spanning 51 languages, 18 domains, 60 intents, and 55 slots." |
| Q2 | 1 | input_content | "MASSIVE was created by tasking professional translators to localize the English-only SLURP dataset into 50 typologically diverse languages from 29 genera." |
| Q3 | 1 | input_form | "With the English seed data included, there are 587k train utterances, 104k dev utterances, 152k test utterances, and 153k utterances currently held out for the MMNLU-22 competition, which will be released after the competition." |
| Q4 | 1 | input_content | "MASSIVE was created by localizing the SLURP NLU dataset (created only in English) in a parallel manner." |
| Q5 | 1 | output_form | "We also present modeling results on XLM-R and mT5, including exact match accuracy, intent classification accuracy, and slot-filling F1 score." |
| Q6 | 1 | output_content | "one difficulty in creating massively multilingual NLU models is the lack of labeled data for training and evaluation, particularly data that is realistic for the task and that is natural for each given language." |
| Q7 | 1 | output_content | "High naturalness typically requires human-based vetting, which is often costly." |
| Q8 | 1 | input_content | "Jack FitzGerald, Christopher Hench, Charith Peris, Scott Mackie, Kay Rottmann, Ana Sanchez, Aaron Nash, Liam Urbach, Vishesh Kakarala, Richa Singh, Swetha Ranganath, Laurie Crist, Misha Britan, Wouter Leeuwis, Gokhan Tur, Prem Natarajan from Amazon, Microsoft, Tripadvisor, and Capital One." |
| Q9 | 2 | input_content | "The first iteration for the foundation of the MASSIVE dataset was the NLU Evaluation Benchmarking Dataset, with 25k utterances across 18 domains (Liu et al., 2019a)." |
| Q10 | 2 | input_form | "The authors updated the dataset and added audio and ASR transcriptions in the release of the Spoken Language Understanding Resource Package (SLURP) (Bastianelli et al., 2020), allowing for full end-to-end Spoken Language Understanding (SLU) evaluation similar to the Fluent Speech Commands dataset (Lugosch et al., 2019) and Chinese Audio-Textual Spoken Language Understanding (CATSLU) (Zhu et al., 2019)." |
| Q11 | 2 | input_ontology | "We release the MASSIVE dataset along with baselines from large pre-trained models fine-tuned on the NLU slot and intent prediction tasks." |
| Q12 | 2 | input_ontology | "This work focuses on the general multi-domain NLU task and builds off the SLURP (Bastianelli et al., 2020) benchmark dataset to extend to an unprecedented 50 new languages." |
| Q13 | 2 | input_ontology | "The Snips datasets (both the original English only and the English and French releases) are most similar to the NLU contained in the MASSIVE dataset, spanning smart home and music domains for a generic voice-based virtual assistant." |
| Q14 | 2 | input_content | "Facebook released a general Intelligent Virtual Assistant (IVA) dataset across the domains of Alarm, Reminder, and Weather (Schuster et al., 2019) created for the purpose of demonstrating cross-lingual transfer learning; and so did not need to be parallel or have an equal number of datapoints, resulting in far fewer examples in Thai (5k) compared to Spanish (7.6k) and English (43k)." |
| Q15 | 3 | input_content | "The languages in MASSIVE were chosen according to the following considerations. First, we acquired cost and worker availability estimates for over 100 languages, providing a constraint to our choices given our fixed budget." |
| Q16 | 3 | input_ontology | "Second, we determined existing languages available in major virtual assistants, such that the dataset could be used to benchmark today's systems." |
| Q17 | 3 | input_content | "Third, we categorized the full pool of languages according to their genera as taken from the World Atlas of Linguistic Structures (WALS) database (Dryer and Haspelmath, 2013), where a genus is a language group that is clear to most linguists without systematic comparative analysis." |
| Q18 | 3 | input_ontology | "Genus is a better indicator of typological diversity, which we sought to maximize, than language family (Dryer, 1989)." |
| Q19 | 3 | input_content | "Fourth, we used the eigenvector centrality of Wikipedia articles, tweets, and book translations (Ronen et al., 2014) as proxies for the internet influence and thus the resource availability of a given language, particularly for self-supervised pretraining applications, and we chose languages spanning the breadth of resource availability." |
| Q20 | 3 | input_form | "Fifth, we examined the script of each language, seeking to increase script diversity to drive experimentation in tokenization and normalization." |
| Q21 | 3 | input_content | "Ultimately, we created 50 new, distinct text corpora, representing 49 different spoken languages." |
| Q22 | 3 | input_content | "Mandarin Chinese was collected twice, once with native speakers who use the traditional set of characters, and once with native speakers who use the modern simplified set of characters." |
| Q23 | 3 | input_content | "There are 14 language families in the dataset." |
| Q24 | 3 | input_ontology | "In MASSIVE, we also include "language isolates" as families. These are languages that have no clear relationship to any known language." |
| Q25 | 3 | input_form | "There are 21 distinct scripts used in the dataset." |
| Q26 | 3 | input_form | "The majority of languages in MASSIVE (28 including English) use some variety of the Latin alphabet, which is also the most widely used script in the world." |
| Q27 | 3 | input_form | "The Arabic script is used for three languages, the Cyrillic script for two languages, and the remaining 18 languages have "unique" scripts, in the sense that only one language in the dataset uses that script." |
| Q28 | 3 | input_form | "Fourteen scripts are unique to a single language, although they may belong to a larger family of writing systems." |
| Q29 | 4 | input_content | "MASSIVE consists of utterances directed at a device, rather than a person, which has some consequences for the type of linguistic patterns it contains." |
| Q30 | 4 | input_ontology | "Specifically, the corpus primarily consists of interrogatives (i.e., questions) and imperatives (commands or requests)." |
| Q31 | 4 | input_ontology | "There are relatively few declarative utterances in the set." |
| Q32 | 4 | input_ontology | "This is in contrast to many large datasets from other sources (e.g., wikipedia, movie scripts, newspapers) which contain a high proportion of declaratives, since the language is collected from situations where humans are communicating with humans." |
| Q33 | 4 | input_content | "In the context of a voice assistant, a user typically asks a device to perform an action or answer a question, so declaratives are less common." |
| Q34 | 4 | input_ontology | "In MASSIVE, 39 languages are subject-initial (24 SVO and 15 SOV), while only three are verb-initial (VSO specifically)." |
| Q35 | 4 | input_ontology | "No object-initial languages are represented." |
| Q36 | 4 | input_ontology | "Five languages are marked in WALS as having no preferred word order, and four do not have any word order data at all." |
| Q37 | 4 | input_ontology | "The majority of them (33) use some kind of verb morphology, such as adding a suffix." |
| Q38 | 4 | input_ontology | "About half of those languages (18) have distinct imperative" |
| Q39 | 5 | input_content | "We randomly sampled a subset of the English seed data which was then paraphrased by professional annotators, resulting in new, more challenging utterances, including 49% more slots per utterance." |
| Q40 | 5 | output_form | "These utterances were localized along with the other splits to be used as a held out evaluation set for the Massively Multilingual NLU-22 competition and workshop." |
| Q41 | 5 | input_content | "The MASSIVE dataset was collected using a customized workflow powered by Amazon MTurk." |
| Q42 | 5 | input_content | "We required a vendor pool with the capability and resources to collect a large multilingual dataset." |
| Q43 | 5 | output_content | "Our original vendor pool consisted of five vendors adjudicated based on previous engagements." |
| Q44 | 5 | output_content | "This vendor pool was reduced to three based on engagement and resource availability." |
| Q45 | 5 | output_content | "Vendors for each language were selected based on their resource" |
| Q46 | 5 | input_ontology | "Nearly half of the languages in MASSIVE (21) make a two-way formal/informal distinction in their second-person pronouns." |
| Q47 | 5 | input_ontology | "A further eight languages have more than two levels of formality, such as informal, formal, and honorific." |
| Q48 | 5 | input_ontology | "Seven languages have an "avoidance" strategy, which means that pronouns are omitted entirely in a polite scenario." |
| Q49 | 5 | input_ontology | "Finally, eleven languages have no data on politeness in WALS at all." |
| Q50 | 6 | input_content | "A majority of languages were supported by a single vendor, while some languages required cross-vendor support to be completed with the required quality and within the required timeline." |
| Q51 | 6 | output_content | "We offered two mechanisms to vendors for evaluating workers to be selected for each language. The first, which was used to select workers for the translation task, was an Amazon MTurk-hosted fluency test where workers listen to questions and statements in the relevant language and were evaluated using a multiple-choice questionnaire." |
| Q52 | 6 | output_content | "The second, which was used to select workers for the judgment task, was a test with a set of three judgments that the vendor could use to assess if workers were able to detect issues in the translated utterances." |
| Q53 | 6 | output_content | "In order to further improve worker selection quality, we created a translator quiz using the Amazon MTurk instructions that were created for translation and judgment tasks, coupled with customized local-language examples." |
| Q54 | 6 | output_content | "Before commencing operations, an initial pilot run of this customized workflow was completed in three languages." |
| Q55 | 6 | input_form | "The collection was conducted by locale on an individual utterance level. Each utterance from the "train," "dev," "test," and "heldout" splits of the SLURP dataset went through two sequential task workflows and a judgment workflow." |
| Q56 | 6 | input_ontology | "The first task is slot translation or localization (see Figure 1). Workers are presented the entire utterance with colored highlighting of the slot values for the utterance (if any) and then presented with each slot value and its corresponding label individually." |
| Q57 | 6 | input_ontology | "The worker is asked to either localize or translate the slot, depending on whether the value should be translated (e.g., "tomorrow") or localized (e.g., the movie "La La Land", which in French is "Pour l'amour d'Hollywood.")" |
| Q58 | 6 | output_ontology | "The metadata of the released dataset includes whether the worker elected to "localize," "translate," or keep the slot "unchanged," primarily for the purposes of researchers evaluating machine translation systems, where it would be unreasonable to expect the system to "localize" to a specific song name the worker selected." |
| Q59 | 6 | input_ontology | "After the slot task, the second worker is asked to translate or localize the entire phrase using the slot task output provided by the first worker (see Figure 2)." |
| Q60 | 6 | input_ontology | "The phrase worker can decide to keep the slot as it was translated, modify it, or remove it entirely if it is not relevant for the language in that scenario." |
| Q61 | 6 | input_ontology | "This worker is also responsible for aligning grammatical genders or prepositional affixes to any of the slots." |
| Q62 | 6 | output_content | "Note that this two-step system alleviates the annotation burden often encountered with such work. Traditionally in such collections, workers would be given a light annotation guide and asked to highlight spans of the slots in a translated or localized utterance." |
| Q63 | 6 | output_form | "The output of the second workflow (the fully localized utterance) is judged by three workers for (1) whether the utterance matches the intent semantically, (2) whether the slots match their labels semantically, (3) grammaticality and naturalness, (4) spelling, and (5) language identification—English or mixed utterances are acceptable if that is natural for the language, but localizations without any tokens in the target language were not accepted." |
| Q64 | 6 | output_ontology | "These judgments are also included in the metadata of the dataset." |
| Q65 | 6 | output_content | "In addition to the workers judging each other's work, the collection system had alarms in place for workers with high rejection rates, high rates of slot deletion, and high rates of English tokens in the translations." |
| Q66 | 6 | output_content | "Workers were also monitored to see if their tasks were primarily machine translated. Such workers were removed from the pool and all of their work was resubmitted to be completed by the other workers." |
| Q67 | 7 | input_ontology | "As initial model benchmarks, we fine-tuned publicly-available pre-trained language models on the MASSIVE dataset and evaluated them on intent classification and slot filling." |
| Q68 | 7 | output_form | "Our models of choice for this exercise were XLM-Roberta (XLM-R; Conneau et al. 2020) and mT5 (Xue et al., 2021)." |
| Q69 | 7 | output_form | "In the case of XLM-R, we utilized the pretrained encoder with two separate classification heads trained from scratch, based on JointBERT (Chen et al., 2019a)." |
| Q70 | 7 | output_form | "The first classification head used the pooled output from the encoder to predict the intent and the second used the sequence output to predict the slots." |
| Q71 | 7 | output_form | "As pooling for the intent classification head, we experimented with using hidden states from the first position, averaged hidden states across the sequence, and the maximally large hidden state from the sequence." |
| Q72 | 7 | output_form | "With mT5, we explored two separate architectures. In one architecture, we only used the pre-trained encoder extracted from mT5, and we trained two classification heads from scratch similarly to the XLM-R setup. We refer to this setup as mT5 Encoder-Only. In the other architecture, we used the full sequence-to-sequence mT5 model in text-to-text mode, where the input is "Annotate:" followed by the unlabeled utterance." |
| Q73 | 7 | output_ontology | "The decoder output is a sequence of labels (including the Other label) for all of the tokens followed by the intent." |
| Q74 | 7 | output_form | "For all models, we used the Base size, which corresponds to 270M parameters for XLM-R, 258M parameters for mT5 Encoder-Only, and 580M parameters for mT5 Text-to-Text, including 192M parameters for embeddings for all three." |
| Q75 | 7 | output_form | "For each model, we performed 128 trials of hyperparameter tuning using the Tree of Parzen Estimators algorithm and Asynchronous Successive Halving Algorithm (ASHA) (Li et al., 2018a) for scheduling, which are both part of the hyperopt library (Bergstra et al., 2013) integrated into the ray[tune] library (Liaw et al., 2018)." |
| Q76 | 7 | output_form | "We trained our models with the Adam optimizer (Kingma and Ba, 2017) and chose the best performing model checkpoint based on overall exact match accuracy across all locales." |
| Q77 | 7 | output_form | "Hyperparameter tuning and fine-tuning was performed using single p3dn.24xlarge instances (8 x Nvidia v100) for XLM-R and mT5 Text-to-Text and a single g4dn.metal instance (8 x Nvidia T4) for mT5 Encoder-Only." |
| Q78 | 7 | output_form | "Hyperparameter tuning times were less than 4 days per model and training times were less than 1 day per model." |
| Q79 | 7 | input_form | "Our dataset includes several languages where white spacing is not used as a word delimiter. In some cases, spaces do occur, but they might serve as phrase delimiters or denote the end of a sentence." |
| Q80 | 7 | input_form | "Three of these written languages, Japanese, Chinese (Traditional), and Chinese (Simplified), do not use spaces anywhere except to identify the end of a sentence. For these languages, we separate each character in the unlabeled input with a whitespace." |
| Q81 | 7 | input_form | "We leave exploration of more sophisticated techniques (such as MeCab for Japanese; Kudo 2005) to future work." |
| Q82 | 7 | input_form | "We use the default spacing provided by annotators for all other languages." |
| Q83 | 7 | output_form | "Zero-shot performance was also assessed, in which the models were trained on English data, validation was performed on all languages, and testing was performed on all non-English locales." |
| Q84 | 7 | output_form | "Table 3 shows the results for each model and training setup, including those for the best performing locale, the worst performing locale, and locale-averaged results for intent accuracy, micro-averaged slot F1 score, and exact match accuracy." |
| Q85 | 7 | output_form | "Zero-shot exact match performance is 25-37 points worse than that of full-dataset training runs." |
| Q86 | 7 | output_form | "Additionally, the variance in task performance across locales is significantly greater for the zero-shot setup than for full-dataset training. For example, there is a 15 point difference in exact match accuracy between the highest and lowest locales for mT5 Text-to-Text when using the full training set, while the gap expands to 44 points with zero-shot." |
| Q87 | 7 | output_form | "We compared the pretraining data quantities by language for XLM-R to its per-language task performance values, and in the zero shot setup, we found a Pearson correlation of 0.54 for exact match" |
| Q88 | 8 | output_form | "Each table includes the highest locale, the lowest locale, and locale-averaged results for intent accuracy, micro-averaged slot F1 score, and exact match accuracy." |
| Q89 | 8 | output_form | "Intervals for 95% confidence are given assuming normal distributions." |
| Q90 | 8 | output_form | "In the full dataset training setup, the correlations decrease to 0.42 for exact match accuracy, 0.47 for intent accuracy, and 0.24 for micro-averaged slot F1 score." |
| Q91 | 8 | input_form | "In Thai, for which spacing is optional, the model can learn from artificial spacing in the input (around where the slots will be) to improve task performance." |
| Q92 | 8 | output_content | "For Khmer, the workers had a difficult time adapting their translations and localizations to properly-slotted outputs given the space-optional nature of the language." |
| Q93 | 8 | input_form | "Additionally, for Japanese and Chinese, we added spaces between all characters when modeling." |
| Q94 | 8 | input_form | "By splitting into single characters, we don't allow the model to the use embeddings learned for chunks of characters." |
| Q95 | 8 | output_form | "This is a likely major cause of the drop in exact match accuracy for Japanese from 58.3% when training on the full dataset to 9.4% for zero shot." |
| Q96 | 8 | input_form | "character spacing was necessary in order to properly assign the slots to the right characters." |
| Q97 | 8 | input_form | "As mentioned in Section 5.1, we leave exploration of more sophisticated spacing techniques for slot filling (such as MeCab; Kudo 2005) to future work." |
| Q98 | 8 | output_form | "Discounting for artificial spacing effects, Germanic genera and Latin scripts performed the best overall (See Appendix E), which is unsurprising given the amount of pretraining data for those genera and scripts, as well as the quantity of Germanic and Latin-script languages in MASSIVE." |
| Q99 | 8 | output_form | "Within the Germanic genera, Swedish, English, Danish, Norwegian, and Dutch all performed comparably (within 95% confidence bounds) for exact match accuracy." |
| Q100 | 8 | output_form | "Icelandic was the lowest-performing Germanic language, likely due to a lack of pretraining data, as well as to its linguistic evolution away from the others due to isolated conditions." |
| Q101 | 8 | input_ontology | "We have released a truly MASSIVE multilingual dataset for NLU spanning 51 typologically diverse languages." |
| Q102 | 9 | input_content | "There are several significant limitations of the MASSIVE dataset and of our modeling." |
| Q103 | 9 | input_content | "Starting with the dataset, the per-language data quantities are relatively small at 19.5k total records and 11.5k records for training." |
| Q104 | 9 | output_content | "Second, there are some low-quality utterances, both in the seed data and in the translations." |
| Q105 | 9 | output_content | "For the most part, these are surfaced through the judgment scores we provide for each record, but if a user does filtering based on these judgments, then the data size decreases even further." |
| Q106 | 9 | input_content | "Third, the data were originally created through crowd-sourcing, not from a real virtual assistant, which introduces artificialities." |
| Q107 | 9 | input_content | "Relatedly, allowing the worker to decide on translation versus localization of slot entities added further noise to the dataset, although we try to store this decision in the metadata." |
| Q108 | 9 | output_ontology | "Fourth, our labeling schema is relatively simple when compared with hierarchical labeling schemata or flat schemata with more intent and slot options." |
| Q109 | 9 | input_form | "Fifth, our collection system did not have a robust method to preserving or denoting native tokenization practices—some languages do not separate with whitespace, while others do but there is no set practice." |
| Q110 | 9 | input_form | "This results in potentially easier (larger chunks to predict slot labels) or harder (each character individually predicted) tasks." |
| Q111 | 9 | output_content | "Sixth, it's possible, though unlikely, that some of our new crowd-sourced records may contain toxic or otherwise objectionable content." |
| Q112 | 9 | output_content | "We performed analyses to check for such malicious activities and did not find any as such." |
| Q113 | 9 | output_form | "Regarding modeling, we have only investigated base-sized models in relatively standard setups, leaving room for much more sophisticated modeling." |
| Q114 | 9 | output_content | "The risks associated with this dataset and work are relatively low, given that we have released a research dataset meant to promote better multilinguality in NLP systems." |
| Q115 | 13 | input_form | "Additional linguistic characteristics of our languages are given in Table 4." |
| Q116 | 13 | input_content | "Screenshots from our collection workflow are given in Figures 1, 2, and 3." |
| Q117 | 13 | output_form | "The hyperparameter search spaces and the chosen hyperparameters are given in Tables 5 and 6." |
| Q118 | 13 | output_form | "Results for all languages are given for exact match accuracy in Table 7, intent accuracy in Table 8, and micro-averaged slot-filling F1 in Table 9." |
| Q119 | 13 | output_form | "We pick our best performing model, mT5 Text-to-Text, and provide a summary of its performance on different language characteristics in Figures 4 and 5." |
| Q120 | 17 | output_content | "How would you rate these sentences?" |
| Q121 | 17 | output_content | "Please respond to the following questions about the TRANSLATED SENTENCE TO RATE." |
| Q122 | 17 | output_content | "By clicking "SUBMIT", I also certify that I am a native speaker or am fluent in the required language" |
| Q123 | 18 | output_form | "The full-dataset hyperparameter search space, the sampling technique, and the chosen hyperparameter for our 3 models." |
| Q124 | 18 | output_form | "The search space for the "quniform" and "qloguniform" sampling techniques is given as [min, max, increment]." |
| Q125 | 19 | output_form | "The zero-shot hyperparameter search space, the sampling technique, and the chosen hyperparameter for our 3 models." |
| Q126 | 20 | output_form | "Exact match accuracy by language for our three models using the full dataset and the zero-shot setup." |
| Q127 | 21 | output_form | "Table 8: Intent accuracy by language for our three models using the full dataset and the zero-shot setup." |
| Q128 | 22 | output_form | "Micro-averaged slot-filling F1 by language for our three models using the full dataset and the zero-shot setup." |
| Q129 | 23 | output_form | "The categories of each language characteristic are sorted by exact match accuracy for readability." |
| Q130 | 23 | input_content | "The number of languages falling into each category is provided in the bar chart in the lowest panel for each characteristic." |
| Q131 | 24 | output_form | "mT5 Text-to-Text performance grouped by Script, Family, Order, Politeness, Imperative Morphology, Imperative Hortative, Optative and Prohibitive." |
| Q132 | 24 | output_form | "As with Figure 4, the categories of each language characteristic are sorted by exact match accuracy for readability." |

---

## Regional Context

```yaml
name: Ethiopian Intercity Travelers — Amharic-Language Booking Bot
abbreviation: ETH-IC-AM
assessment_context:
  benchmark: MASSIVE (Multilingual NLU, 51 languages, intent classification and slot
    filling)
  deployment: Conversational booking bot for Sky Bus, Selam Bus, and Ride intercity
    services, accessed via Android/iOS smartphone apps
  primary_task: Intent classification and slot filling for intercity route queries,
    fare lookups, and seat-change transactions in Amharic
target_population:
  description: Ethiopian intercity commuters and travelers who use Android or iOS
    apps to book long-distance bus or ride-hail trips with operators Sky Bus, Selam
    Bus, and Ride. The population spans urban Addis Ababa residents, rural and regional
    travelers across Amhara Region, Oromia, Tigray, SNNPR, and other regions served
    by intercity routes. A significant share are Amharic-as-L2 speakers from non-Amhara
    ethnic backgrounds who use Amharic as a functional lingua franca for travel.
  primary_language: Amharic
  expected_code_switching_languages:
  - Oromo (especially on Addis–Adama–Hawassa corridor)
  - Tigrinya (especially on Addis–Mekelle corridor)
  - Other Ethiopian languages (Sidama, Somali, Afar — lower frequency)
  l2_speaker_share: '[NEEDS VERIFICATION — deferred: below search budget; likely unsearchable
    from published sources — no national survey isolates intercity-bus-user language
    background. Note: Oromo speakers constitute >40% of Ethiopia''s population (EthioMT
    survey data — [WEB-1]), suggesting L2 Amharic
    share among intercity travelers is substantial but no operator-level figure is
    publicly available.]'
  age_range: '[NEEDS VERIFICATION — deferred: below search budget; operator-level
    app analytics are not published. Note: Ethiopia''s median age is 19.1 years (UN
    World Population Prospects 2024 — [WEB-2]),
    indicating a very young overall population; working-age intercity traveler profile
    likely skews 18–45.]'
  app_platform: Android and iOS smartphone apps (Sky Bus, Selam Bus, Ride)
geography:
  country: Ethiopia
  primary_city: Addis Ababa (largest origin/destination hub)
  key_regions:
  - Addis Ababa City Administration
  - Amhara Region
  - Oromia Region
  - Tigray Region
  - SNNPR (Southern Nations, Nationalities, and Peoples' Region)
  - Afar Region
  - Somali Region
  key_intercity_corridors:
  - Addis Ababa – Adama (Nazret)
  - Addis Ababa – Hawassa
  - Addis Ababa – Bahir Dar
  - Addis Ababa – Gondar
  - Addis Ababa – Mekelle
  - Addis Ababa – Dire Dawa
  - Addis Ababa – Jimma
  - Addis Ababa – Dessie
  urbanization_rate_pct: '~23% urban (CIA World Factbook 2023 figure: 23.2%; UN 2025
    estimate: 22.5%) — Sources: CIA World Factbook 2023 — [WEB-3];
    Worldometer UN 2024 Revision — [WEB-2].
    Caveat: urbanization growing at ~4.4% per year; Addis Ababa is a disproportionate
    share of this urban population. The predominantly rural population profile means
    most intercity travelers originate from rural or peri-urban areas.'
  rural_traveler_share: '[NEEDS VERIFICATION — deferred: below search budget; no published
    breakdown of intercity bus passengers by urban/rural origin exists. Given ~77%
    rural population nationally, a majority of intercity travelers likely originate
    from non-Addis locations, but no operator-level figure confirms this.]'
languages:
  primary_interface_language: Amharic
  script: Ethiopic (Ge'ez script) — fidel syllabary
  script_category_in_massive: Unique script (one of 18 languages with a script used
    by only one MASSIVE locale)
  code_switching_languages:
    oromo:
      script: Latin (since 1991, Qubee orthography)
      relevance: High — Oromia is the largest region by area and population; Addis–Adama–Hawassa
        is a major corridor. User confirmed Oromo code-switching will occur in real
        utterances.
      massive_coverage: Separate MASSIVE locale (no mixed Amharic–Oromo utterances)
    tigrinya:
      script: Ethiopic (same script family as Amharic)
      relevance: Moderate — northern route (Addis–Mekelle) travelers; Tigrinya speakers
        may code-switch especially for place names and route terminology.
      massive_coverage: Separate MASSIVE locale (no mixed Amharic–Tigrinya utterances)
  linguistic_features_relevant_to_nlu:
    morphology: Amharic is a highly morphologically rich, fusional Semitic language
      with root-and-pattern morphology, extensive verb inflection, and cliticization
      of prepositions and conjunctions
    word_order: SOV with significant flexibility; verb-final structure affects slot
      span detection
    script_directionality: Left-to-right (Ethiopic script, unlike Arabic RTL)
    tokenization_notes: Amharic uses spaces as word delimiters, but morphological
      richness means a single token can encode information that requires multiple
      tokens in English. Slot boundary detection may be affected.
    numeral_system: Ethiopic numerals exist (፩፪፫…) alongside Arabic numerals; spoken
      Amharic uses a base-10 system with distinct Amharic number words. Birr amounts
      may appear in either numeral form or as spelled-out Amharic words.
    politeness: '[NEEDS VERIFICATION — deferred: likely unsearchable (lived practice);
      Amharic politeness/register distinctions in booking-bot utterances require in-community
      elicitation rather than web-retrievable documentation. MASSIVE documents 21
      languages with two-way formal/informal distinctions, but whether Amharic''s
      politeness system was fully captured in MASSIVE''s annotation is not confirmed.]'
  amharic_dialect_variation:
    description: Amharic dialects vary across Amhara sub-regions (Gondar, Gojjam,
      Wollo, Shewa) and differ further from L2-speaker usage. Addis Ababa Amharic
      is considered a prestige/standard variety.
    l2_speaker_phrasing: Non-Amhara speakers using Amharic as L2 may exhibit pronunciation-influenced
      spelling, simplified syntax, and Oromo/Tigrinya loanword insertion. These patterns
      are unlikely to appear in translated NLU datasets.
    massive_annotator_dialect_representation: '[NOT FOUND — searched MASSIVE paper
      (arXiv 2204.08582) and Ethiopian NLP literature; MASSIVE does not disclose the
      regional or dialect background of its Amharic translators. No third-party audit
      of MASSIVE''s Amharic annotator demographics was found in the NLP literature
      reviewed.]'
calendar_and_temporal_conventions:
  primary_calendar: 'Ethiopian (Ge''ez) calendar — 13 months: Meskerem, Tikimt, Hidar,
    Tahsas, Tir, Yekatit, Megabit, Miazia, Ginbot, Sene, Hamle, Nehase, Pagume'
  calendar_offset_from_gregorian: 'Approximately 7–8 years behind the Gregorian calendar;
    Ethiopian New Year falls in September (Gregorian). The offset is 8 years from
    January 1 to ~September 10/11, then 7 years for the remainder of the Gregorian
    year. Source: Ethiopian Calendar reference — [WEB-4]'
  date_expression_conventions: Users are expected to express travel dates using Ethiopian
    month names (e.g., 'Meskerem 5' for a date in late September Gregorian). These
    will not appear in MASSIVE's translated date slot values.
  holiday_demand_surges:
  - 'Timkat (Ethiopian Epiphany) — Tir 11 E.C., corresponding to January 19 Gregorian
    (January 20 in Gregorian leap years). Major travel surge. Source: [WEB-5]'
  - 'Meskel (Finding of the True Cross) — Meskerem 17 E.C., corresponding to September
    27 Gregorian (September 28 the year before a Gregorian leap year). Source: [WEB-6]'
  - 'Ethiopian Christmas (Genna/Lidat) — Tahsas 29 E.C., corresponding to January
    7 Gregorian every year. Source: [WEB-6]'
  - 'Ethiopian Easter (Fasika) — movable feast; date varies yearly, calculated using
    ancient Ethiopian Orthodox ecclesiastical rules, distinct from and usually later
    than Western Easter. Source: [WEB-7]'
  - 'Eid al-Fitr and Eid al-Adha — Islamic lunar calendar; dates shift ~10–11 days
    earlier each Gregorian year. Muslim traveler share and surge patterns: [NEEDS
    VERIFICATION — deferred: below search budget; no published operator-level surge
    data found]'
  - 'Ethiopian New Year (Enkutatash) — Meskerem 1 E.C., corresponding to September
    11 Gregorian (September 12 in the Gregorian year before a leap year). Major peak
    travel period. Source: [WEB-6]; [WEB-4]'
  massive_coverage: None — MASSIVE contains no Ethiopian calendar month names, Ge'ez-calendar
    temporal expressions, or holiday-based surcharge slot values
domain_specific_notes:
  intercity_transport_context: Sky Bus, Selam Bus, and Ride are the three named operators.
    Ethiopian intercity bus travel is a primary mode of long-distance transport, especially
    for non-elite travelers. Routes connect Addis Ababa to regional capitals and towns
    across all major corridors.
  fare_and_currency:
    currency: 'Ethiopian Birr (ETB, symbol: ብር or Br)'
    fare_expression_conventions: Fares may be quoted as Arabic numerals (e.g., '450
      birr'), Ethiopic numerals, or verbalized Amharic number words. Informal spoken
      conventions (e.g., rounding, use of 'hundred' as a unit) may differ from formal
      written forms.
    massive_coverage: None — MASSIVE price/fare slots derive from English-origin SLURP
      data and do not address ETB formatting, Amharic numeral verbalization, or spoken-number
      conventions
  operator_specific_slot_types:
    description: The booking domain requires slot types not present in MASSIVE's 55-slot
      taxonomy
    missing_slots:
    - operator_name (Sky Bus, Selam Bus, Ride)
    - 'seat_class (VIP, economy, sleeper — exact classes per operator: [NEEDS VERIFICATION
      — deferred: below search budget; no publicly available operator seat-class taxonomy
      was found in web searches])'
    - route_closure_reason (road closure, weather, security)
    - surcharge_event (holiday, peak-season pricing)
    - trip_change_type (rebook, cancel, upgrade)
    - departure_terminal (bus station name, e.g., Meskel Square, Kality, Autobus Terra)
  city_name_variants:
    description: 'Ethiopian cities are referred to by multiple names in common usage:
      Amharic names, Oromo names, colonial/transliterated English names, abbreviations,
      and demonyms. The booking system must handle all variants as equivalent slot
      values.'
    examples:
    - amharic_name: አዳማ
      common_name: Adama
      alternate_name: Nazret
      massive_coverage: Not present
    - amharic_name: ሐዋሳ
      common_name: Hawassa
      alternate_name: Awassa
      massive_coverage: Not present
    - amharic_name: መቀሌ
      common_name: Mekelle
      alternate_name: Mek'ele
      massive_coverage: Not present
    - amharic_name: ባህር ዳር
      common_name: Bahir Dar
      alternate_name: '[NEEDS VERIFICATION — deferred: low impact; no widely used
        alternate name for Bahir Dar found in reviewed sources]'
      massive_coverage: Not present
    - amharic_name: ጎንደር
      common_name: Gondar
      alternate_name: Gonder (variant transliteration)
      massive_coverage: Not present
    - amharic_name: ድሬ ዳዋ
      common_name: Dire Dawa
      alternate_name: Diredawa (one-word variant used in some official contexts)
      massive_coverage: Not present
    - note: '[NEEDS VERIFICATION — deferred: below search budget; no comprehensive
        operator route + city-name-variant list is publicly available. A full list
        requires direct elicitation from Sky Bus, Selam Bus, and Ride operators.]'
  booking_flow_intents:
    description: The user considers the booking flow broadly generic and compatible
      with MASSIVE's intent set. However, the following intent types relevant to Ethiopian
      intercity bus booking are absent from MASSIVE's 60-intent taxonomy.
    absent_intents:
    - route_query (which buses serve origin–destination pair?)
    - seat_class_query (what classes are available?)
    - operator_query (does Sky Bus / Selam serve this route?)
    - cancel_and_rebook (due to road closure or schedule change)
    - holiday_surcharge_query (is pricing higher for Timkat?)
    - departure_terminal_query (which station does the bus leave from?)
    coverage_note: Generic booking intents (book, reschedule, check availability)
      are partially covered by MASSIVE. Transportation-domain-specific and Ethiopia-specific
      intents are not.
infrastructure_notes:
  device_platform: Android and iOS smartphones (app-based text input)
  android_market_share_pct: '[NEEDS VERIFICATION — deferred: below search budget;
    no Ethiopia-specific Android vs. iOS split was found in reviewed sources. Nationally,
    Android dominates in African markets generally, but no Ethiopia-specific figure
    was retrieved.]'
  smartphone_penetration_pct: '~15% of the population own a smartphone as of 2024
    (gender breakdown: 18% of men, 6% of women). Source: Birr Metrics citing GSMA
    data — [WEB-8].
    Caveat: this is a national aggregate; urban/app-user cohort penetration is significantly
    higher. The low national figure underscores that the deployment population is
    a self-selected subset of higher-digital-literacy users.'
  mobile_internet_penetration_pct: 'Mobile penetration (subscriptions per person)
    reached 61.4% in Q1 2024, up from 36.7% in Q1 2019. 3G+4G subscriptions represent
    61.3% of total mobile subscriptions as of early 2024. Source: Omdia Ethiopia Service
    Provider Market Report 2024 via Connecting Africa — [WEB-9]'
  primary_mobile_operator: 'Ethio Telecom is the dominant operator with ~94.2% market
    share as of 2024, declining toward a projected 78.5% as Safaricom Ethiopia expands.
    Ethio Telecom had 78.3 million active subscribers by end-June 2024; Safaricom
    Ethiopia had 6.1 million active monthly users by mid-2024. Sources: Omdia/Connecting
    Africa 2024 — [WEB-9];
    Astute Analytica/GlobeNewswire 2025 — [WEB-10]'
  average_mobile_data_speed: '[NEEDS VERIFICATION — deferred: below search budget;
    no Ethiopia national average mobile data speed figure was found in reviewed sources.
    Ethio Telecom launched its first commercial 5G network in September 2023 (145
    sites in Addis Ababa), expanding 4G to 45+ cities in 2023. Source: Connecting
    Africa 2024 — [WEB-9]]'
  connectivity_variation_by_region:
    addis_ababa: '5G commercially launched September 2023 (Ethio Telecom, 145 initial
      sites, now expanding). 4G/LTE broadly available. Source: Connecting Africa 2024
      — [WEB-9]'
    amhara_region: '[NEEDS VERIFICATION — deferred: below search budget; no Amhara-specific
      corridor coverage figure found. National 4G expansion reached 45+ cities in
      2023.]'
    oromia_region: '[NEEDS VERIFICATION — deferred: below search budget; Oromia corridor
      coverage not separately documented in reviewed sources.]'
    tigray_region: 'Connectivity was severely disrupted during the 2020–2022 Tigray
      conflict. Recovery is ongoing. The conflict period saw primary school enrollment
      drop from ~85.5% in 2020 to 20.8% in 2021, indicating broad infrastructure disruption.
      Current network status not separately quantified in reviewed sources. Source
      on conflict impact: ZoeTalent/education data — [WEB-11]'
    snnpr: '[NEEDS VERIFICATION — deferred: below search budget; no SNNPR-specific
      connectivity figure found in reviewed sources.]'
  input_modality: Text (on-screen keyboard using Ethiopic/Ge'ez fidel input or phonetic
    Amharic input method)
  keyboard_input_method_notes: Users may input Amharic using a dedicated Ethiopic
    keyboard, a phonetic romanization-to-fidel IME, or may occasionally type Amharic
    words in Latin characters (Amharic romanization). The system should handle fidel
    input as primary but Latin-script Amharic representation is a plausible edge case.
  offline_capability_requirement: '[NEEDS VERIFICATION — deferred: below search budget;
    no public documentation of Sky Bus, Selam Bus, or Ride app offline capabilities
    was found.]'
literacy_and_education:
  national_literacy_rate_pct: '~51.8% adult literacy rate (ages 15+) as of 2017 (latest
    World Bank / UNESCO figure available); male 57.2%, female 44.4%. No more recent
    national survey value has been published. Sources: CIA World Factbook 2023 — [WEB-3];
    UNESCO via TheGlobalEconomy — [WEB-12].
    Caveat: the 2017 figure is the most recent published; actual 2024 literacy is
    likely higher given expanding primary enrollment, but no updated survey has been
    released.'
  amharic_literacy_rate_pct: '[NOT FOUND — searched World Bank, UNESCO, and Ethiopian
    education sources; no Amharic-specific literacy rate (distinct from general literacy)
    is published as a standalone national statistic. General literacy in Ethiopia
    is measured against Amharic or regional-language reading ability, but the Amharic-only
    share is not separately reported.]'
  urban_rural_literacy_gap: 'Significant regional and urban–rural gap documented.
    Urban areas (e.g., Addis Ababa) have substantially higher literacy; pastoralist
    regions (Afar, Somali) have much lower rates. Primary net enrollment in Afar ~46%
    vs. national ~95% in 2018. Source: ZoeTalent/education statistics — [WEB-11].
    Caveat: national figure is a 2017 aggregate; sub-national literacy rates vary
    widely and are not published annually.'
  smartphone_app_literacy: Users are app-literate by virtue of using the booking application,
    but digital literacy levels vary; complex UI or long-form text entry may pose
    friction for some users.
  primary_language_of_education_by_region:
    addis_ababa: Amharic
    amhara_region: Amharic
    oromia_region: Oromo (Afaan Oromoo) — Amharic as second language of instruction
    tigray_region: Tigrinya — Amharic as second language
    snnpr: '[NEEDS VERIFICATION — deferred: likely unsearchable at granular level;
      varies by ethnic group and zone within SNNPR; requires regional education authority
      data or stakeholder elicitation]'
cultural_norms_notes: '- Ethiopian Orthodox Christianity is the majority religion,
  shaping holiday travel demand around Genna, Timkat, Fasika, and Meskel.

  - Islam is the second-largest religion; Eid travel surges are significant.

  - Ethiopian New Year (Enkutatash, Meskerem 1) is a peak travel period.

  - Multi-ethnic national identity: Oromo, Amhara, Tigrinya, Somali, Sidama, and other
  ethnic groups all use intercity transport but may prefer their own language for
  natural utterances.

  - Amharic functions as the working language of the federal government and as a national
  lingua franca, but is an L2 for the majority of Ethiopians by ethnicity.

  - Respect for elders and formal address forms may influence user utterance register,
  especially for older travelers.

  - Informal travel planning often involves social referrals and word-of-mouth; some
  users may be first-time app users.

  - Bus station culture in Ethiopia involves negotiation, informal brokers (dallalas),
  and route knowledge embedded in local practice — not always reflected in formalized
  booking intents.

  '
regulatory_and_operator_context:
  transport_regulatory_body: '[NEEDS VERIFICATION — deferred: below search budget;
    the Ethiopian Ministry of Transport and Logistics is the federal body, but specific
    intercity bus licensing authority (federal vs. regional) was not confirmed in
    reviewed sources]'
  operator_licensing: '[NEEDS VERIFICATION — deferred: below search budget; no publicly
    available Sky Bus, Selam Bus, or Ride route concession framework documentation
    was found]'
  data_protection_regulation: 'Personal Data Protection Proclamation No. 1321/2024
    (PDPP), enacted April 4, 2024, published in the Federal Negarit Gazette July 24,
    2024 (in force). Ethiopia''s first comprehensive data protection law; designates
    the Ethiopian Communications Authority (ECA) as supervisory authority; establishes
    consent-based processing, data subject rights (access, rectification, erasure,
    portability, objection to automated decisions), and data localisation requirements
    (locally collected personal data must be stored on servers in Ethiopia). Penalties
    for violations range from 1–10 years imprisonment and fines of 60,000–600,000
    Birr depending on severity. Sources: CIPIT analysis — [WEB-13];
    full text (English) — [WEB-14];
    Digital Policy Alert — [WEB-15]'
  consumer_protection_framework: '[NEEDS VERIFICATION — deferred: below search budget;
    Ethiopia applies the 2013 Trade Competition and Consumer Protection Proclamation
    to digital services generally. No digital-booking-specific consumer protection
    framework was found. Source (partial): Digital Policy Alert 2025 — [WEB-16]]'
  fare_regulation: '[NEEDS VERIFICATION — deferred: below search budget; whether Ethiopian
    intercity bus fares are government-regulated or market-set was not confirmed in
    reviewed sources. Note: Ethiopia has historically regulated transport tariffs,
    but recent liberalization trends (telecom, trade) suggest market-set fares are
    possible for private operators]'
benchmark_fit_summary:
  dimension_priority_weights:
    IO: MODERATE — MASSIVE's 60 intents cover generic booking flows but omit Ethiopian-specific
      and operator-specific intents
    IC: HIGH — Slot values (Ethiopian calendar dates, local city name variants, Birr
      fares) are absent from translated MASSIVE data
    IF: LOWER — Text-only, Ethiopic-script, modality-aligned; tokenization quality
      for Amharic slot boundaries is a minor open question
    OO: MODERATE — 55-slot taxonomy lacks operator_name, seat_class, route_closure_reason,
      surcharge_event slot types
    OC: HIGH — MASSIVE Amharic data translated from English by fluency-certified workers;
      no code-switching, no L2-speaker phrasing, no Oromo-corridor representation
    OF: LOWER — Intent + slot-filling output format directly matches deployment requirements
  flagged_gaps_requiring_web_search:
  - gap_id: 1
    description: Ethiopian calendar slot coverage in any NLU/slot-filling benchmark
    search_target: Amharic NLU slot filling Ethiopian calendar Ge'ez calendar date
      entity recognition benchmark
    search_result: NOT FOUND — No NLU or slot-filling benchmark including Ethiopian
      calendar temporal expressions (Meskerem, Tikimt, etc.) was identified in searches
      of EthioNLP, EthioLLM/EthioBenchmark (LREC-COLING 2024), or broader Ethiopian
      NLP literature. EthioBenchmark covers news classification, machine translation,
      NER, POS tagging, hate speech detection, and sentiment analysis — not intent
      classification or slot filling with Ethiopian date slots. This confirms a full
      gap with no existing resource to bridge it.
  - gap_id: 2
    description: Ethiopian city name variants and abbreviations in Amharic NER or
      NLU data
    search_target: Ethiopian city name NLP Amharic named entity recognition location
      variants benchmark
    search_result: PARTIAL — Amharic NER datasets exist (ANEC corpus, Yimam et al.
      2021 — 210,000 tokens, CRF-based, publicly available per EthioNLP survey — [WEB-17]).
      However, no NER benchmark specifically targeting intercity transport city name
      variants (Adama/Nazret, Mek'ele/Mekelle) in booking-domain contexts was found.
      General Amharic NER may provide partial transfer, but domain adaptation for
      transport-specific location entities is unsupported.
  - gap_id: 3
    description: Oromo–Amharic code-switching corpora or evaluation sets
    search_target: Amharic Oromo code-switching corpus NLP evaluation dataset Ethiopia
    search_result: 'PARTIAL — A bilingual Amharic–Afaan Oromo code-switching corpus
      exists for hate speech detection, with annotated social-media posts (GitHub:
      michaelmelese/Bilingual-Amharic-Afaan-Oromo-Hate-Speech — [WEB-18]).
      The EthioNLP group also produced a pipeline for code-switched Ethiopian social
      media posts using OSCAR/CommonCrawl corpora augmented with EthioMT back-translation
      ([WEB-19]). However, no code-switching corpus for the
      booking/transport domain exists. The social media code-switching corpus is the
      closest available resource but differs substantially in domain, register, and
      slot structure from booking-bot utterances.'
  - gap_id: 4
    description: Tigrinya–Amharic code-switching corpora or evaluation sets
    search_target: Tigrinya Amharic code-switching NLP Ethiopian language benchmark
    search_result: NOT FOUND — No Tigrinya–Amharic mixed-language NLP corpus or evaluation
      set was identified. EthioLLM/EthioBenchmark covers monolingual Tigrinya tasks
      (MT, POS, hate speech, sentiment), and a hate speech annotation scheme covers
      Amharic + Tigrigna as separate languages on social media ([WEB-20]),
      but no Tigrinya–Amharic code-switching evaluation resource for any domain was
      found. This is a confirmed full gap.
  - gap_id: 5
    description: Amharic-as-L2 speaker phrasing in NLP datasets
    search_target: Amharic L2 speaker NLP evaluation intercity transport Ethiopia
      dialect variation
    search_result: NOT FOUND — No NLP dataset specifically capturing L2-speaker Amharic
      phrasing patterns, pronunciation-influenced spelling, or syntactically simplified
      Amharic from non-Amhara speakers was found. Ethiopian NLP literature (EthioNLP
      survey 2023, EthioLLM 2024) focuses on monolingual standard Amharic. This gap
      requires stakeholder/community elicitation rather than web-searchable resources.
  - gap_id: 6
    description: African or low-resource transport-domain NLU slot types
    search_target: African intercity transport NLU slot filling benchmark bus booking
      sub-Saharan low-resource NLP
    search_result: NOT FOUND — No African or sub-Saharan intercity transport NLU benchmark
      was identified. EthioBenchmark (LREC-COLING 2024) covers only news classification,
      MT, NER, POS tagging, hate speech, and sentiment analysis — no transport or
      booking domain. This is a confirmed full gap across the African NLP ecosystem.
  - gap_id: 7
    description: Amharic numeral verbalization and Birr currency slot normalization
    search_target: Amharic number verbalization Birr currency NLP slot filling numeric
      normalization Ethiopian
    search_result: NOT FOUND — No NLP resource specifically addressing Amharic numeral
      verbalization for currency (Birr) or slot normalization of spoken Amharic number
      words was found. Ethiopian NLP literature does not surface a dedicated numeric
      normalization resource for Amharic. This gap requires domain-specific corpus
      construction.
  - gap_id: 8
    description: Amharic Ethiopic-script tokenization quality for slot boundary detection
    search_target: Amharic Ethiopic script tokenization slot filling NLP Ge'ez word
      boundary
    search_result: PARTIAL — Amharic tokenization tools exist (amseg segmenter/tokenizer,
      Yimam et al. 2021 per EthioNLP survey — [WEB-17]),
      and HornMorpho (rule-based morphological analyzer) is actively used in Ethiopian
      NLP pipelines ([WEB-19]). However, no slot-filling-specific
      evaluation of tokenization quality for Amharic in MASSIVE or any comparable
      benchmark was found. The general tokenizer availability reduces but does not
      eliminate concerns about slot boundary detection for booking-domain Amharic.
  - gap_id: 9
    description: Ethio Telecom and mobile internet penetration current figures
    search_target: Ethiopia mobile internet penetration smartphone usage 2024 Ethio
      Telecom Safaricom market share
    search_result: 'RESOLVED — See infrastructure_notes fields above. Mobile penetration:
      61.4% Q1 2024 (Omdia). Ethio Telecom market share: ~94.2% in 2024. Smartphone
      penetration: ~15% nationally. Sources cited in infrastructure_notes.'
  - gap_id: 10
    description: Ethiopian data protection and digital consumer protection regulatory
      framework
    search_target: Ethiopia Personal Data Protection Proclamation digital services
      regulation 2024
    search_result: RESOLVED — Personal Data Protection Proclamation No. 1321/2024
      enacted April 4, 2024, in force July 24, 2024. See regulatory_and_operator_context.data_protection_regulation
      above.
  - gap_id: 11
    description: Sky Bus, Selam Bus, Ride operator seat class taxonomy and route network
    search_target: Sky Bus Ethiopia Selam Bus seat classes routes VIP economy intercity
      bus
    search_result: NOT FOUND — No publicly available documentation of Sky Bus, Selam
      Bus, or Ride seat class taxonomies or official route networks was found in web
      searches. Operator-level detail requires direct elicitation from the operators.
net_new_fields:
  ethiopian_nlp_ecosystem_note:
    field_type: net-new
    content: 'EthioLLM (2024) introduced the first multilingual LLMs for five Ethiopian
      languages (Amharic, Ge''ez, Afaan Oromo, Somali, Tigrinya) alongside EthioBenchmark,
      a consolidated benchmark for NER, POS tagging, news classification, hate speech
      detection, sentiment analysis, and MT. No intent classification or slot-filling
      tasks are included. EthioBenchmark is the most comprehensive publicly available
      Ethiopian NLP evaluation suite but does not address booking-domain NLU. Source:
      EthioLLM, LREC-COLING 2024 — [WEB-21];
      arXiv — [WEB-22]. Relevance: confirms no existing
      benchmark for the deployment''s primary evaluation need (Amharic intent classification
      + slot filling in transport domain).'
  amharic_oromo_code_switching_corpus_note:
    field_type: net-new
    content: 'A bilingual Amharic–Afaan Oromo hate speech corpus exists (Woldeyohannis
      et al., Journal of Big Data 2024; GitHub: michaelmelese/Bilingual-Amharic-Afaan-Oromo-Hate-Speech).
      It is the only known publicly available Amharic–Oromo code-switched NLP dataset.
      Source: Springer Journal of Big Data — [WEB-18].
      Relevance to benchmark gap 3 (Oromo code-switching): the corpus exists but is
      restricted to hate speech detection on social media; domain mismatch with booking-bot
      utterances is severe. It could serve as a starting point for mixed-language
      tokenization and word-list construction, but not as a direct training or evaluation
      resource for the deployment.'
  ethiopian_social_media_multilingual_hate_speech_corpus:
    field_type: net-new
    content: 'A 2024 fine-grained hate speech annotation scheme and multilingual lexicon
      covering Amharic, Afaan Oromo, English, and Tigrigna was developed for Ethiopian
      social media (X, Telegram, Facebook), including code-switched posts (RAIL 2024
      workshop paper — [WEB-20]). This is the
      most linguistically diverse Ethiopian NLP corpus for code-mixed content. Relevance:
      confirms that Amharic–Oromo–Tigrigna code-switching is empirically documented
      in Ethiopian digital communication, strengthening the validity concern about
      MASSIVE''s monolingual Amharic annotation failing to capture real user utterances
      on Oromia and Tigray corridors.'
  ethiopia_national_ai_policy:
    field_type: net-new
    content: 'Ethiopia has approved a National AI Policy and established the Ethiopian
      AI Institute to guide AI development. The policy operates alongside the PDPP
      2024 data governance framework. Source: Digital Policy Alert 2025 — [WEB-16].
      Relevance: AI deployments in Ethiopia are subject to both the PDPP and the emerging
      AI policy; the booking bot operator should monitor ECA and Ethiopian AI Institute
      guidance as implementing regulations are developed.'
  gsma_digital_gender_gap:
    field_type: net-new
    content: 'GSMA 2024 reports a 40% gender disparity in mobile internet use in Ethiopia;
      only 6% of women own a smartphone vs. 18% of men. Source: GSMA Digital Economy
      Ethiopia Report 2024 (press release) — [WEB-23];
      Birr Metrics 2024 — [WEB-8].
      Relevance: the deployment population (smartphone app users) is likely disproportionately
      male; benchmarking and annotation efforts should account for this cohort skew,
      as female travelers who do access the app may exhibit different utterance patterns.'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/html/2403.19365v1 |
| WEB-2 | https://srv1.worldometers.info/world-population/ethiopia-population/ |
| WEB-3 | https://www.cia.gov/the-world-factbook/about/archives/2023/countries/ethiopia/ |
| WEB-4 | https://ethiocal.com/ |
| WEB-5 | https://www.ethiopiancalendar.net/ethiopian-holidays |
| WEB-6 | https://holidays.ertale.com/ |
| WEB-7 | https://ethiopiancalendars.com/ |
| WEB-8 | https://birrmetrics.com/ethiopia-narrows-mobile-gender-gap-to-24-but-smartphone-access-for-women-remains-just-6/ |
| WEB-9 | https://www.connectingafrica.com/connectivity/ethiopia-s-telecoms-liberalization-makes-progress-omdia |
| WEB-10 | https://www.globenewswire.com/news-release/2025/01/27/3015813/0/en/Ethiopia-Mobile-Value-Added-Services-Market-to-Worth-Over-US-10-23-Billion-By-2033-Astute-Analytica.html |
| WEB-11 | https://zoetalentsolutions.com/education-statistics-for-ethiopia/ |
| WEB-12 | https://www.theglobaleconomy.com/Ethiopia/Literacy_rate/ |
| WEB-13 | https://cipit.org/ethiopias-personal-data-protection-proclamation-of-2024-and-its-budding-digital-identity-regime/ |
| WEB-14 | https://www.metaappz.com/References/ethiopian_laws/federal/pr_1321_2024/en/txt |
| WEB-15 | https://digitalpolicyalert.org/event/24922-implemented-personal-data-protection-proclamation-proclamation-no-13212024-including-data-localisation-requirements |
| WEB-16 | https://digitalpolicyalert.org/digest/dpa-digital-digest-ethiopia |
| WEB-17 | https://github.com/EthioNLP/Ethiopian-Language-Survey |
| WEB-18 | https://link.springer.com/article/10.1186/s40537-024-01044-y |
| WEB-19 | https://ethionlp.github.io/ |
| WEB-20 | https://aclanthology.org/2024.rail-1.13.pdf |
| WEB-21 | https://aclanthology.org/2024.lrec-main.561/ |
| WEB-22 | https://arxiv.org/abs/2403.13737 |
| WEB-23 | https://www.gsma.com/newsroom/press-release/ethiopias-digital-economy-to-contribute-etb-1-3-trillion-to-gdp-by-2028-unlocking-jobs-and-growth-through-telecom-and-policy-reforms/ |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Does the system need to handle intents specific to Ethiopian intercity travel — e.g., route queries between regional Ethiopian cities, demand surges during holidays like Timkat or Meskel, operator-specific seat classes, or intents like 'cancel and rebook due to road closures'?
A1: The user acknowledges that MASSIVE covers general domains, but considers intercity bus booking in Ethiopia broadly similar to generic booking flows. They expect the system to handle all anticipated scenarios without flagging a strong need for Ethiopia-specific intent extensions.

Q2 [IC]: Would users' natural utterances include Ethiopian-specific slot values — Amharic city names or abbreviations, Ethiopian calendar date references (Meskerem, Tikimt), and fares quoted in Birr with local pricing conventions — and must the system extract these correctly?
A2: Yes. The user confirms that these conventions reflect actual user utterances and that correct slot extraction of Ethiopian-calendar dates, local city names, and Birr-denominated fares is a system requirement.

Q3 [OC]: Given that 'native Amharic speaker' spans urban Addis residents, Amhara-region speakers, and Amharic-as-L2 speakers from other ethnic groups, are there systematic phrasing differences — including code-switching with Oromo or Tigrinya — that a single annotator profile might miss?
A3: Yes. The user confirms data is curated by native speakers but explicitly expects code-switching behavior to occur in real user utterances, particularly with Oromo vocabulary.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | The user considers the booking flow broadly generic, reducing the domain-gap concern, but MASSIVE's 60 intents were designed for global virtual assistant tasks and contain no intercity-transport or operator-specific intents (e.g., route-closure rebooking, seat-class selection), leaving partial coverage gaps. |
| IC | HIGH | MASSIVE's Amharic slot instances are translated from English-origin data and will not contain Ethiopian calendar dates, Amharic/local city name variants, Birr fare formats, or road-closure references — all of which the user has confirmed are required slot values. |
| IF | LOWER | Both the benchmark and the deployment are text-only in a language (Amharic) that is included in MASSIVE; no modality or script-infrastructure mismatch is present. |
| OO | MODERATE | MASSIVE's intent and slot taxonomy was designed for generic virtual-assistant domains; while the user views the booking flow as standard, operator-specific slot types (seat class, operator name, trip-change reason) may fall outside the 55 slot types defined in MASSIVE. |
| OC | HIGH | MASSIVE's Amharic data was produced via professional translation from English, not by annotators drawn from the actual Ethiopian intercity traveler population; the user has confirmed code-switching with Oromo occurs, which translated-from-English utterances will not represent. |
| OF | LOWER | The deployment uses intent-classification and slot-filling outputs that match MASSIVE's label/score output format exactly; no modality or format mismatch is present. |

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
  "benchmark": "massive",
  "region": "Ethiopian Intercity Travelers — Amharic-Language Booking Bot",
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
