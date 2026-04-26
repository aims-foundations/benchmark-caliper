I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **DrBenchmark: A Large Language Understanding Benchmark for French Biomedical Natural Language Processing** is valid for use in **French Pharmaceutical Regulatory NLP — DrBenchmark Assessment**.

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

- **Name**: drbenchmark
- **Full Name**: DrBenchmark: A Large Language Understanding Benchmark for French Biomedical Natural Language Processing
- **Domain**: French biomedical NLP evaluation
- **Languages**: fr
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Test Case Categories (Input Ontology)
DrBenchmark covers 20 downstream tasks aggregated into 6 designated categories:
POS tagging, NER, MCQA, multi-class classification (MCC), multi-label
classification (MLC), and STS [Q81, Q83, Q84]. Within these, the benchmark
explicitly includes both classical tasks (NER, POS) and more challenging ones
(MCQA, multi-label classification) [Q20]. Individual tasks include spoken
drug-prescription intent and NER (PxCorpus [Q44]), pharmacy specialization
exam MCQA (FrenchMedMCQA [Q39]), clinical-case similarity (CLISTER), and
ICD-10 chapter classification (DiaMed [Q45]). The benchmark positions its
breadth by comparison to BLURB (13 tasks [Q13]), BLUE (10 tasks [Q14]), and
CBLUE (8 tasks [Q15]).

From a deployment-validity perspective, the 20-task taxonomy covers clinical
and research NLP genres but contains no tasks derived from EMA-style SmPCs,
patient information leaflets, CTD regulatory modules, or ANSM-format
submissions. PxCorpus (spoken prescriptions [Q44]) and QUAERO (EMEA drug
leaflets [Q34]) approach but do not replicate the formulaic, legally
constrained language of EU regulatory compliance documents. The sole original
task (DiaMed) targets ICD-10 chapter classification of clinical cases from
a Pan African journal [Q45] — a document genre remote from European regulatory
submissions. This structural gap means the benchmark's input ontology does not
cover the primary document genres of the intended deployment context.

General-purpose benchmarks are acknowledged to inadequately evaluate in-domain
model performance [Q10], and the benchmark explicitly notes that the French
biomedical field is under-resourced in evaluation tools [Q5, Q11], but no task
addresses regulatory document compliance, safety-warning consistency, or
EMA/ANSM-specific NLP categories.

### Data Sources and Collection (Input Content)
DrBenchmark draws on a diverse range of origins: scientific literature, clinical
trials, clinical cases, and speech transcriptions [Q19]. Named sources include
EMEA drug leaflets and MEDLINE biomedical titles (QUAERO [Q33, Q34]), PMC Open
Access biomedical abstracts (MorFITT [Q38]), real French pharmacy specialization
exams (FrenchMedMCQA [Q39]), spoken drug prescription recordings (PxCorpus
[Q44]), clinical trial protocols (ESSAI [Q43]), multilingual clinical case
corpora filtered to French (E3C [Q29], Mantra-GSC [Q40]), DEFT competition
data (DEFT-2020 [Q21], DEFT-2021 [Q24]), and the original DiaMed corpus from
the Pan African Medical Journal [Q45]. Licensing for all constituent datasets
remains unchanged from original sources [Q96]; vocabulary differences across
models reflect the heterogeneity of underlying training data [Q76].

While EMEA drug labels and MEDLINE abstracts are included through QUAERO and
Mantra-GSC, these represent pre-existing research NLP corpora rather than live
regulatory submissions with current EMA/ANSM formatting conventions.
Critically, no data sources from French overseas territories (Martinique,
Guadeloupe, French Guiana, Réunion, Mayotte) are identified, and the DiaMed
corpus from the Pan African Medical Journal [Q45], while expanding geographic
reach, does not address tropical pathology vocabulary relevant to French
overseas departments. The absence of curated regulatory data (INNs, ATC codes,
posology templates, contraindication phrasing as normative exemplars) represents
a meaningful content-validity gap relative to the deployment context.

### Input Signal Form (Input Form)
DrBenchmark is exclusively text-based, operating on French biomedical text with
no audio, image, or cross-script considerations. The only modality exception is
PxCorpus, which consists of spoken drug prescription dialogues that were manually
transcribed before inclusion [Q44]; the benchmark thus evaluates text
representations of speech, not audio. Several datasets lacking predefined splits
were assigned 70/10/20 random splits [Q32, Q42]. Tokenization is studied as a
variable: various tokenization algorithms produce differing sub-token rates per
word [Q89, Q90], and the benchmark toolkit is built on HuggingFace Datasets and
Transformers with normalized data loaders [Q48]. The multilingual E3C and
Mantra-GSC datasets were filtered to retain only their French subsets [Q31, Q40].

For the deployment context (metropolitan France, text-only regulatory documents
in high-resource French), the input form is well-matched. There is no script
mismatch, no modality divergence, and no infrastructure incompatibility.
The Latin alphabet with diacritics is consistent across benchmark and deployment.
This dimension represents the lowest validity concern of the six.

### Output Label Categories (Output Ontology)
The benchmark's label ontologies are richly specified in appendices. POS tagging
uses 31 classes for CAS [Q42] and 36 for ESSAI [Q101, Q102]. NER label sets
include 10 UMLS Semantic Group categories for QUAERO [Q35, Q103], clinical
entity and temporal/factuality labels for E3C [Q30, Q104], 12 medical specialty
classes for MorFITT [Q105], 11 (Medline) or 10 (EMEA/Patents) classes for
Mantra-GSC [Q106], and 14 fine-grained entity types for DEFT-2021 NER [Q108].
Multi-label classification uses 23 MeSH Chapter C axes for DEFT-2021 [Q27, Q107]
and ICD-10 chapter-level labels for DiaMed [Q45]. STS tasks produce continuous
similarity scores from 0 to 5 [Q22, Q41].

From a regulatory-deployment perspective, the NER label taxonomies reflect
clinical and research ontologies (UMLS Semantic Groups, MeSH, ICD-10) rather
than regulatory entity types specific to EMA/ANSM submissions. Absent from the
label inventory are INNs, ATC codes, excipient names, posology expressions,
contraindication qualifiers, or EMA SmPC section identifiers. The STS scoring
scale (0–5) reflects general semantic proximity and is not calibrated to
distinguish legally significant small differences — dose threshold changes or
subpopulation qualifiers — that would constitute distinct regulatory meaning
under EMA/ANSM standards. No model excels across all 20 tasks [Q3, Q57], and
DrBERT-FS specifically does not excel on MLC or STS tasks [Q82], underscoring
that the output taxonomy does not support a single unified regulatory scoring
function.

### Annotation Process (Output Content)
Annotation practices vary substantially across constituent datasets. DEFT-2021
was manually annotated for both MLC and NER [Q25], with 23 MeSH axes [Q27].
CLISTER's 1,000 sentence pairs were manually annotated by multiple annotators
assigning similarity scores from 0 to 5, then averaged [Q41]. DiaMed — the sole
original corpus — was manually annotated by several annotators including one
medical expert, using ICD-10 chapter-level labels; inter-annotator agreement
(Cohen's Kappa and Gwet's AC1) was computed over two sessions of 15 clinical
cases each [Q45, Q46]. CAS POS annotations were produced automatically via
Tagex 3 and validated against manual annotations at 98% precision [Q42].

Across all documented annotation processes, annotators are described as clinical
case reviewers, medical experts, or NLP researchers — none are identified as
regulatory affairs specialists, pharmacovigilance officers, or legal experts
applying EMA/ANSM normative frameworks. The silver-standard CAS corpus [Q42]
uses automatic annotation validated at 98% precision, which falls short of
fully adjudicated gold-standard labels. The inter-annotator agreement statistics
for DiaMed [Q45, Q46] cover only 15 cases per session — a narrow validation
base. For the deployment context, where ground-truth label authority rests with
regulatory experts applying EMA SmPC guidelines and ANSM circulars, the
divergence between benchmark annotator expertise and required regulatory
expertise is a direct threat to convergent validity.

### Output Modality and Evaluation Protocol (Output Form)
Sequence labeling tasks (POS, NER) are scored with SeqEval in IOB2 format,
predicting only the first token of each word to achieve tokenizer-agnostic
evaluation [Q52, Q53]. STS tasks are assessed using Spearman correlation and
the EDRM metric from DEFT-2020 [Q54]. Classification tasks use a majority-class
baseline [Q56]. All models are fine-tuned under a strict protocol with identical
hyperparameters, results averaged over four runs, with statistical significance
via Student's t-test [Q51]; hyperparameters are fully documented [Q49, Q99,
Q100]. Low-resource sensitivity is probed by varying training data proportions
across four trials [Q68, Q69, Q70].

The benchmark's text-label and continuous-score output formats align structurally
with the deployment system's multi-candidate confidence-score output and
human-review flagging design. However, the granularity of confidence scoring
and the threshold that should trigger mandatory regulatory review are not
benchmarked. The QUAERO preprocessing limitation — loss of 6.06%–8.90% of
nested annotations and sentence-splitting of long EMEA documents [Q37] —
introduces systematic measurement error particularly relevant for regulatory
text where nested entity structures may carry compliance significance.
Domain-specialized French biomedical models led in up to 75% of tasks [Q62],
but no single model excels uniformly [Q57, Q58], and the evaluation protocol
does not include workflow-calibration metrics tied to the regulatory
human-in-the-loop adjudication design.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "It encompasses 20 diversified tasks, including named-entity recognition, part-of-speech tagging, question-answering, semantic textual similarity, and classification." |
| Q2 | 1 | output_form | "We evaluate 8 state-of-the-art pre-trained masked language models (MLMs) on general and biomedical-specific data, as well as English specific MLMs to assess their cross-lingual capabilities." |
| Q3 | 1 | output_ontology | "Our experiments reveal that no single model excels across all tasks, while generalist models are sometimes still competitive." |
| Q4 | 1 | input_ontology | "These tasks encompass part-of-speech (POS) tagging, named-entity recognition (NER), classification, question-answering (QA), and semantic textual similarity (STS)." |
| Q5 | 1 | input_ontology | "Although the French language is generally considered as well-endowed, it is notably lacking in evaluation resources within the biomedical field." |
| Q6 | 1 | output_form | "We also perform a quantitative study of 8 pre-trained state-of-the-art masked language models" |
| Q7 | 1 | output_content | "Yanis Labrak, Adrien Bazoge, Oumaima El Khettari, Mickael Rouvier, Pacôme Constant dit Beaufils, Natalia Grabar, Béatrice Daille, Solen Quiniou, Emmanuel Morin, Pierre-Antoine Gourraud and Richard Dufour" |
| Q8 | 1 | output_content | "LIA, Avignon Université, Zenidoc, Nantes Université, CHU Nantes, Clinique des données, INSERM, CIC 1413, École Centrale Nantes, CNRS, LS2N, UMR 6004, Service de Neuroradiologie diagnostique et interventionnelle, l'institut du thorax, UMR 8163 – STL CNRS, Université de Lille" |
| Q9 | 1 | input_ontology | "The biomedical field remains an area with relatively few proposed benchmarks, mainly for English and Chinese, facilitating the availability of many biomedical models in these two languages." |
| Q10 | 2 | input_ontology | "In the case of specialized domains, general benchmarks may not adequately evaluate the performance of in-domain models." |
| Q11 | 2 | input_ontology | "Specifically, within the biomedical domain, only few benchmarks have been proposed, and they primarily focus on few languages." |
| Q12 | 2 | input_content | "For instance, platforms like BLURB (Gu et al., 2021) and BLUE (Peng et al., 2019) predominantly offer benchmarks for English, while CBLUE (Zhang et al., 2022a) caters to the Chinese language." |
| Q13 | 2 | input_ontology | "BLURB integrates 13 tasks, including NER, information and relation extraction, sentence similarity, text classification, and QA." |
| Q14 | 2 | input_ontology | "BLUE encompasses 10 tasks, such as NER, sentence similarity, relation extraction, text classification, and inference." |
| Q15 | 2 | input_ontology | "CBLUE covers 8 tasks, including NER, information extraction, text and intent classification, sentence similarity, and query relevance." |
| Q16 | 2 | input_ontology | "To our knowledge, aside the multilingual benchmark BigBIO (Fries et al., 2022) which includes only 4 corpora for French and is initially intended for generative text completion under zero-shot scenario, no large benchmark specialized in the French biomedical field exists." |
| Q17 | 2 | input_ontology | "Our proposed benchmark comprises 20 French biomedical language understanding tasks, one of which is specifically created for this benchmark." |
| Q18 | 2 | input_ontology | "A variety of tasks with different requirements and objectives: Part-of-Speech (POS) tagging, Multi-class, Multi-label and Intent classification, Named-Entity Recognition (NER), Multiple-Choice Question-Answering (MCQA), and Semantic Textual Similarity (STS)." |
| Q19 | 2 | input_content | "A diverse range of data origins: Scientific literature, clinical trials, clinical cases, speech transcriptions, and more as described in Table 2." |
| Q20 | 2 | input_ontology | "Please note that within DrBenchmark, we include classical tasks like NER and POS tagging, as well as more specific and challenging tasks like MCQA and multi-label classification." |
| Q21 | 3 | input_content | "DEFT-2020 (Cardon et al., 2020) contains clinical cases, encyclopedia and drug labels introduced in the 2020 edition of an annual French Text Mining Challenge, called DEFT, and annotated for two tasks: (i) textual similarity and (ii) multi-class classification." |
| Q22 | 3 | output_ontology | "The first task aims at identifying the degree of similarity within pairs of sentences, from 0 (the less similar) to 5 (the most similar)." |
| Q23 | 3 | input_ontology | "The second task consists in identifying, for a given sentence, the most similar sentence among three sentences provided." |
| Q24 | 3 | input_content | "DEFT-2021 (Grouin et al., 2021) is a subset of 275 clinical cases taken from the 2019 edition of DEFT." |
| Q25 | 3 | output_content | "This dataset is manually annotated in two tasks: (i) multi-label classification and (ii) NER." |
| Q26 | 3 | input_ontology | "The multi-label classification task focuses on identifying the patient's clinical profile based on the diseases, signs, or symptoms mentioned in the clinical cases." |
| Q27 | 3 | output_ontology | "The dataset is annotated with 23 axes from Chapter C of the Medical Subject Headings (MeSH)." |
| Q28 | 3 | output_ontology | "The second task involves fine-grained information extraction for 13 types of entities (more detail in Appendix B.7)." |
| Q29 | 3 | input_content | "E3C (Magnini et al., 2020) is a multilingual dataset of clinical cases annotated for the NER task." |
| Q30 | 3 | output_ontology | "It consists of two types of annotations (more detail in Appendix B.4): (i) clinical entities (e.g., pathologies), (ii) temporal information and factuality (e.g., events)." |
| Q31 | 3 | input_form | "While the dataset covers 5 languages, only the French portion is retained for the benchmark." |
| Q32 | 3 | input_form | "Since the dataset does not come with pre-defined subsets, we performed a 70 / 10 / 20 random split, as described in Table 3." |
| Q33 | 3 | input_content | "The QUAERO French Medical Corpus (Névéol et al., 2014), simply referred to as QUAERO in this paper, contains annotated entities and concepts for NER tasks." |
| Q34 | 3 | input_content | "The dataset covers two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE." |
| Q35 | 3 | output_ontology | "10 entity categories corresponding to the UMLS Semantic Groups (Lindberg et al., 1993) were annotated (more detail in Appendix B.3)." |
| Q36 | 3 | input_content | "In total, 26,409 entity annotations were mapped to 5,797 unique UMLS concepts." |
| Q37 | 3 | output_form | "Due to the presence of nested entities in annotations, we simplified the evaluation process by retaining only annotations at the higher granularity level from the BigBio (Fries et al., 2022) implementation, following the approach described in Touchent et al. (2023), which translates into an average loss of 6.06% of the annotations on EMEA and 8.90% on MEDLINE. Additionally, considering that some documents from EMEA exceed the maximum input sequence length that most current language models can handle, we decided to split these documents into sentences." |
| Q38 | 4 | input_content | "MorFITT (Labrak et al., 2023) is a multi-label dataset annotated with medical specialties. It contains 3,624 biomedical abstracts from PMC Open Access. It has been annotated across 12 medical specialties (more detail in Appendix B.5), for a total of 5,116 annotations." |
| Q39 | 4 | input_content | "FrenchMedMCQA (Labrak et al., 2022) is a Multiple-Choice Question-Answering (MCQA) dataset for biomedical domain. It contains 3,105 questions coming from real exams of the French medical specialization diploma in pharmacy, integrating single and multiple answers. The first task consists of automatically identifying the set of correct answers among the 5 proposed for a given question. The second task consists of identifying the number of answers (between 1 and 5) supposedly correct for a given question." |
| Q40 | 4 | input_content | "Mantra-GSC (Kors et al., 2015) is a multilingual dataset annotated for biomedical NER. From the 5 languages covered, we included only the French subset in this benchmark. The dataset is obtained from 3 sources which have been partitioned to be evaluated separately by 2 annotation schemes (more detail in Appendix B.6): Medline (11 classes), and EMEA and Patents (10 classes). The sources cover different types of documents (biomedical abstracts/titles, drug labels and patents). To ensure evaluation consistency, we randomly split the dataset into 3 subsets: 70% for training, 10% for validation, and 20% for testing." |
| Q41 | 4 | output_content | "CLISTER (Hiebel et al., 2022) is a French clinical cases Semantic textual similarity (STS) dataset of 1,000 sentence pairs manually annotated by several annotators, who assigned similarity scores ranging from 0 to 5 to each pair. The scores were then averaged together to obtain a floating-point number representing the overall similarity. The objective of this dataset is to develop models that can automatically predict a similarity score that closely aligns with the reference score based solely on the two sentences provided." |
| Q42 | 4 | output_content | "CAS (Grabar et al., 2018) comprises 3,790 clinical cases that have been annotated for POS tagging with 31 classes using automatic annotations through Tagex 3, with an evaluation conducted by comparing the automatic outputs against manual annotations. This evaluation yielded 98% precision. Since the dataset does not come with predefined subsets, we made the decision to randomly split it into 3 subsets of 70%, 10% and 20% of the total data for training, validation and test respectively." |
| Q43 | 4 | input_content | "ESSAI (Dalloux et al., 2021) contains 7,247 clinical trial protocols annotated in 41 POS tags using TreeTagger (Schmid, 1994). As the dataset was not originally divided into 3 subsets, we applied the same procedure as on the CAS corpus." |
| Q44 | 4 | input_ontology | "PxCorpus (Kocabiyikoglu et al., 2022) is a spoken language understanding dataset in the domain of medical drug prescription transcripts. It includes 4 hours (1,981 recordings) of transcribed and annotated dialogues focused on drug prescriptions. The recordings were manually transcribed and semantically annotated. The first task involves classifying the textual utterances into one of the 4 intent classes (prescribe, replace, negate, none). The second task is a NER task where each word in a sequence is classified into one of 38 classes, such as drug, dose, or mode (more detail in Appendix B.9)." |
| Q45 | 4 | output_content | "DiaMed is an original dataset created specifically for DrBenchmark. It comprises 739 new French clinical cases collected from an open source journal (The Pan African Medical Journal). The cases have been manually annotated by several annotators, one of which is a medical expert, into 22 chapters of the International Classification of Diseases, 10th Revision (ICD-10) (Wor, 2019). These chapters provide a general description of the type of injury or disease. To ease the annotation process, only label at the chapter level were used (more detail in Appendix B.8). The inter-annotator agreement between the 4 annotators has been computed for two annotation sessions (see Table 4), with 15 different clinical cases assessed per session." |
| Q46 | 4 | output_content | "Table 4: Inter-annotator agreement statistics. κ is referring to Kappa Cohen and G to Gwet's AC1." |
| Q47 | 4 | input_form | "To facilitate the adoption of DrBenchmark and ensure consistency in implementations, we have de-" |
| Q48 | 5 | input_form | "We developed a practical toolkit based on the HuggingFace Datasets library (Lhoest et al., 2021). This toolkit includes data loaders that adhere to normalized schemes and predefined data splits. It also provides pre-training and evaluation scripts for each of the tasks, utilizing the HuggingFace Transformers (Wolf et al., 2020) and PyTorch (Paszke et al., 2019) libraries." |
| Q49 | 5 | output_form | "For further guidance, we have integrated all the training details, including hyperparameters, in Appendix A. This information will help users to reproduce and customize the experiments conducted with DrBenchmark." |
| Q50 | 5 | output_form | "To guarantee fair comparison, we focus exclusively on pre-trained masked language models (MLMs) in this study. These MLMs are based on BERT-like architectures (Devlin et al., 2019)." |
| Q51 | 5 | output_form | "All the models are fine-tuned regarding a strict protocol using the same hyperparameters for each downstream task. The reported results are obtained by averaging the scores from four separate runs, thus ensuring robustness and reliability. We also report statistical significance computed using Student's t-test." |
| Q52 | 6 | output_form | "To ensure a fair and consistent comparison among systems for sequence-to-sequence tasks such as POS tagging and NER, we chose the SeqEval (Nakayama, 2018) metric in conjunction with the IOB2 format and the training of all the models to predict only the label on the first token of each word as mentioned by Touchent et al. (2023)." |
| Q53 | 6 | output_form | "It provides a tokenizer-agnostic evaluation and mitigates any correlation between models' performances and the tokenization process." |
| Q54 | 6 | output_form | "For STS tasks, the models' performance was assessed using two metrics: (1) the Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM), as defined by the original authors of the DEFT-2020 dataset (Cardon et al., 2020)." |
| Q55 | 6 | output_form | "In Section 5.1, we compare the results obtained by each model within DrBenchmark, which permits to position a wide range of state-of-the-art models in the biomedical field across various NLP tasks." |
| Q56 | 6 | output_form | "The results of the 8 models are reported in Table 6 and compared to a baseline obtained by considering the majority class for all predictions." |
| Q57 | 6 | output_ontology | "Overall, although we might anticipate certain models to excel in all tasks, we discovered that no single model outperforms the rest in all application scenarios." |
| Q58 | 6 | output_form | "Interestingly, most of the models examined manage to secure the top position in at least one of the French biomedical downstream tasks studied." |
| Q59 | 6 | output_form | "The only exception pertains to the cross-lingual generalist model (XLM-RoBERTa), which manages to reach the second-best position on several tasks." |
| Q60 | 6 | output_form | "French biomedical language models (DrBERT-FS, DrBERT-CP, CamemBERT-bio), presumed to be the most aligned with the nature of the data of the benchmark, exhibit indeed superior performance across many tasks." |
| Q61 | 6 | output_form | "More precisely, DrBERT-FS achieves the highest performance in 8 tasks, DrBERT-CP in 5 tasks, and CamemBERT-bio in 2 tasks." |
| Q62 | 6 | output_form | "This indicates that domain and language-specialized models achieve the best performance in up to 75% of the DrBenchmark downstream tasks." |
| Q63 | 6 | output_form | "Generalist models (CamemBERT, CamemBERTa, FlauBERT and XLM-RoBERTa) are more suitable for tasks that require extensive linguistic knowledge but may not perform as well as specialized models nor even reach their level of performance." |
| Q64 | 6 | output_form | "We observe that all generalist models obtain better performance only on 4 out of the 20 tasks, but still remain competitive on most tasks." |
| Q65 | 6 | output_form | "Furthermore, our experiments with DrBERT-FS indicate that biomedical models may require less pre-training data compared to generalist ones." |
| Q66 | 6 | output_form | "However, it is important to note that this observation requires further confirmation." |
| Q67 | 6 | output_form | "In some tasks, biomedical models that undergo continual pre-training from a generalist model, such as CamemBERT-bio, can prove to be the most effective, underscoring the value of pre-training on generalist data." |
| Q68 | 7 | input_form | "For this purpose, we conducted experiments by varying the amount of training data during the fine-tuning process by randomly choosing four percentages of the training data: 25%, 50%, 75% and 100%." |
| Q69 | 7 | output_form | "To make the experiment as fair as possible, we did four runs for each percentage, model and dataset combination." |
| Q70 | 7 | output_form | "The validation and test sets have not been changed for the sake of comparison." |
| Q71 | 7 | output_form | "We observe that on certain datasets, some models capture information more quickly than others, like in Figures 1b, 1f and 1a." |
| Q72 | 7 | output_form | "Unsurprisingly, in almost all scenarios, having the complete training set yields better results than having only 25% of it." |
| Q73 | 7 | output_form | "However, all the models based on CamemBERT face difficulties in corpora with limited amount of data, such as MantraGSC Patents, where they fail to generate labels other than 'O'." |
| Q74 | 7 | output_form | "On the other hand, in the same low-resource scenarios, CamemBERTa models exhibit greater robustness and achieve superior performance." |
| Q75 | 8 | input_form | "Tokenizers play a crucial role in MLMs by utilizing size-limited vocabularies to split texts into sub-units, aiming to handle out-of-vocabulary (OOV) words." |
| Q76 | 8 | input_content | "Due to variations in the training data, vocabularies differ across different models, as illustrated in Figure 2." |
| Q77 | 8 | input_form | "So far, there has been a prevailing notion in the community that excessive segmentation of words in tokenization leads to a loss of morphological form and semantic meaning, introducing noise and adversely affecting performance (Church, 2020; Hofmann et al., 2021; Bostrom and Durrett, 2020)." |
| Q78 | 8 | output_form | "However, our experiments, as shown in Table 7, reveal that FlauBERT is the model with the least word segmentation (1.43 in average), while DrBERT-CP tends to have the highest average segmentation (1.90 in average)." |
| Q79 | 8 | output_form | "Surprisingly, when comparing the performance of these two models on the benchmark tasks, we observe that DrBERT-CP outperforms FlauBERT on 16 out of the 20 tasks, thus contradicting previous conclusions drawn by the community." |
| Q80 | 8 | input_form | "Yet, tokenization, as it is currently done in MLMs, seems to play a minor role in the performance of systems." |
| Q81 | 8 | input_ontology | "Table 8 summarizes the results obtained on average by the considered MLMs when aggregating the tasks into one of the five designated categories: POS, NER, MCQA, MCC (Multi-class classification), MLC (Multi-label classification), or STS tasks." |
| Q82 | 8 | output_ontology | "Upon analyzing the average performance by task category, it becomes evident that the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS." |
| Q83 | 9 | input_ontology | "In this paper, we introduced DrBenchmark, the first large language understanding benchmark tailored for the French biomedical domain." |
| Q84 | 9 | input_ontology | "We conducted a qualitative evaluation of 8 state-of-the-art masked language models (MLMs) on this comprehensive benchmark, encompassing 20 diverse downstream tasks." |
| Q85 | 9 | output_form | "Our findings illuminate the limitations of generalist models in tackling complex biomedical tasks, emphasizing the importance of employing domain-specific models to achieve peak performance." |
| Q86 | 9 | output_form | "We have observed that several biomedical tasks in DrBenchmark exhibit relatively poor performance, even when utilizing specialized biomedical models." |
| Q87 | 9 | output_ontology | "We postulate that the models examined in this study, here state-of-the-art MLMs, may not be the most effective choices for specific tasks such as question-answering or multi-label classification." |
| Q88 | 9 | output_form | "The quantitative study we conducted on the PLMs requires further in-depth analysis to comprehend the impact of different parameters." |
| Q89 | 9 | input_form | "Firstly, we investigated the influence of tokenizers based on the average number of sub-tokens they produce per word." |
| Q90 | 9 | input_form | "Various tokenization algorithms are employed, depending on the model under examination." |
| Q91 | 9 | output_form | "The size of the data has not been thoroughly investigated, particularly the significance of the pre-training data size, especially specialized data in the biomedical field." |
| Q92 | 9 | output_form | "Although the benchmark is easily reproducible and customizable, it required a substantial amount of computational power to execute all runs." |
| Q93 | 9 | output_form | "We utilized approximately 2,500 hours on V100 GPUs from the Jean-Zay supercomputer to complete the quantitative study." |
| Q94 | 9 | output_form | "According to the Jean Zay supercomputer documentation, the total environmental cost is estimated to be equivalent to 647,500 Wh or 36.9 kgCO2eq/kWh, based on the carbon intensity of the energy grid mentioned in the BLOOM environmental cost study conducted on Jean Zay (Luccioni et al., 2022)." |
| Q95 | 9 | output_content | "All code for DrBenchmark is released under the MIT License." |
| Q96 | 9 | input_content | "The licensing for all datasets remains unchanged from the original sources, and DrBenchmark has no intention of redistributing these datasets." |
| Q97 | 9 | output_content | "This work was performed using HPC resources from GENCI-IDRIS (Grant 2022-AD011013061R1 and 2022-AD011013715) and from CCIPL (Centre de Calcul Intensif des Pays de la Loire)." |
| Q98 | 9 | output_content | "This work was financially supported by ANR MALADES (ANR-23-IAS1-0005), ANR AIBy4 (ANR-20-THIA-0011) and Zenidoc." |
| Q99 | 13 | output_form | "For the experiments, we utilize the following hyperparameters that yield optimal performance from the models." |
| Q100 | 13 | output_form | "To mitigate overfitting, we locally save the best model based on its validation metric." |
| Q101 | 14 | output_ontology | "INT, PRO:DEM, VER:impf, VER:ppre, PRP:det, KON, VER:pper, PRP, PRO:IND, VER:simp, VER:con, SENT, VER:futu, PRO:PER, VER:infi, ADJ, NAM, NUM, PUN:cit, PRO:REL, VER:subi, ABR, NOM, VER:pres, DET:ART, VER:cond, VER:subp, DET:POS, ADV, SYM and PUN." |
| Q102 | 14 | output_ontology | "INT, PRO:POS, PRP, SENT, PRO, ABR, VER:pres, KON, SYM, DET:POS, VER:, PRO:IND, NAM, ADV, PRO:DEM, NN, PRO:PER, VER:pper, VER:ppre, PUN, VER:simp, PREF, NUM, VER:futu, NOM, VER:impf, VER:subp, VER:infi, DET:ART, PUN:cit, ADJ, PRP:det, PRO:REL, VER:cond and VER:subi." |
| Q103 | 14 | output_ontology | "O, GEOG, PHEN, DISO, ANAT, OBJC, PHYS, PROC, DEVI, CHEM and LIVB" |
| Q104 | 14 | output_ontology | "Clinical: O, and CLINENTITY. Temporal: O, EVENT, ACTOR, BODYPART, TIMEX3 and RML" |
| Q105 | 14 | output_ontology | "microbiology, etiology, virology, physiology, immunology, parasitology, genetics, chemistry, veterinary, surgery, pharmacology and psychology" |
| Q106 | 14 | output_ontology | "Medline: ANAT, PROC, CHEM, PHYS, GEOG, DEVI, LIVB, OBJC, DISO, PHEN and O. EMEA and Patents: ANAT, PROC, CHEM, PHYS, DEVI, LIVB, OBJC, DISO, PHEN and O." |
| Q107 | 14 | output_ontology | "Multi-label Classification: immunitaire (immunology), endocriniennes (endocrinology), blessures (injury), chimiques (chemicals), etatsosy (signs and symptoms), nutritionnelles (nutrition), infections (infections), virales (virology), parasitaires (parasitology), tumeur (oncology), osteomusculaires (osteomuscular disorders), stomatognathique (stomatology), digestif (digestive system disorders), respiratoire (respiratory system disorders), ORL (otorhinolaryngologic diseases), nerveux (nervous system disorders), oeil (eye diseases), homme (male genital diseases), femme (female genital diseases), cardiovasculaires (cardiology), hemopathies (hemic and lymphatic diseases), genetique (genertic disorders) and peau (dermatology)." |
| Q108 | 14 | output_ontology | "Named-entity recognition: O, ANATOMY, DATE, DOSAGE, DURATION, MEDICAL EXAM, FREQUENCY, MODE, MOMENT, PATHOLOGY, SOSY, SUBSTANCE, TREATMENT and VALUE" |

---

## Regional Context

```yaml
name: French Pharmaceutical Regulatory NLP — DrBenchmark Assessment
abbreviation: fr-pharma-regulatory
deployment_context:
  primary_country: France (Metropolitan)
  secondary_regions:
  - Martinique
  - Guadeloupe
  - French Guiana
  - Réunion
  - Mayotte
  institutional_setting: Pharmaceutical companies and government health agencies (primarily
    ANSM, secondarily EMA-interface roles)
  system_description: Document management system using NER and semantic textual similarity
    models to verify compliance of drug labeling documents and flag inconsistencies
    in safety warnings. Outputs determine whether documentation meets professional
    standards for official submission or requires manual revision.
  human_in_loop: true
  adjudication_design: Multi-candidate confidence-score output; borderline cases flagged
    for manual review by regulatory affairs specialists or legal experts; physicians
    and nurses retain decision authority in clinical support mode.
  silver_standard_note: System is characterized as a 'Silver Standard' clinical support
    tool, not an authoritative classifier. It maps pathologies to standardized axes
    (e.g., ICD-10 chapters) with acknowledged imperfect alignment to hospital coding
    conventions.
target_population:
  description: Regulatory affairs specialists, pharmacologists, and legal experts
    at pharmaceutical companies or government health agencies in Metropolitan France,
    operating on structured regulatory and biomedical text in French. Secondary users
    may be located in French overseas territories where distinct disease prevalence
    patterns (e.g., tropical pathologies) require system adaptation.
  primary_user_roles:
  - Regulatory affairs specialists
  - Pharmacologists
  - Legal experts (pharma-regulatory)
  - Pharmacovigilance officers
  secondary_user_roles:
  - Physicians (adjudication role)
  - Nurses (adjudication role)
  professional_expertise_level: High — users are domain experts who retain final decision
    authority; system outputs are advisory.
  primary_use_tasks:
  - Compliance verification of patient information leaflets (notices patient)
  - Safety warning consistency checking across labeling documents
  - NER on regulatory and biomedical text (INNs, posology, contraindications, excipients)
  - Semantic textual similarity assessment for regulatory equivalence of safety phrasing
  - Flagging documents requiring manual revision before official submission
  deployment_language: 'French (high-resource, metropolitan standard; secondary: overseas
    territory French variants)'
  population_size_note: 'ANSM itself employs approximately 1,000 staff across multiple
    sites (Source: IAOCR — [WEB-1]);
    some sources cite ~400 employees at ANSM headquarters (Source: Pharmablue — [WEB-2]).
    The broader regulatory affairs workforce across the French pharmaceutical industry
    (private sector companies plus ANSM) is not enumerated in a single authoritative
    source; the Glassdoor market shows active open roles across major pharma employers
    in France (Source: Glassdoor — [WEB-3]).
    [NOT FOUND — no single census-level figure for total regulatory affairs professionals
    employed across French pharma industry and ANSM published by INSEE, LEEM, or ANSM
    in retrievable form; stakeholder survey or industry body (e.g., LEEM) elicitation
    required for a precise count.]'
regulatory_framework:
  primary_national_authority: ANSM (Agence Nationale de Sécurité du Médicament et
    des produits de santé)
  eu_level_authority: EMA (European Medicines Agency)
  key_regulatory_procedures:
    centralized_procedure: EMA centralized marketing authorization — applies to all
      EU Member States including France
    national_procedure: 'ANSM national authorization — France-specific, governed by
      national circulars. ANSM is the competent authority for national, mutual recognition,
      and decentralised procedure MAs valid in France (Source: Lexology — [WEB-4]).'
    ansm_ema_divergence_note: 'For centrally authorized products, SmPC, PIL, and labeling
      text are identical across all EU member states; however, France-specific requirements
      are added via a national ''blue-box'' on outer packaging (CIP codes, name of
      the Exploitant, local prescription and delivery conditions) and a ''Feuille
      de style'' template used for ANSM submission of translated product information.
      France also imposes its own drug classification system (List I / List II) on
      packaging regardless of the EU MA text (Source: PharmaLex — [WEB-5]).
      These national additions are not represented in QUAERO EMEA labels or any DrBenchmark
      corpus, representing a concrete gap for French regulatory NLP. No published
      NLP study was found documenting the divergence in NLP terms; this slot requires
      regulatory affairs expert elicitation for full specification.'
  primary_document_genres:
  - Summary of Product Characteristics (SmPC / RCP in French)
  - Patient Information Leaflets (notice patient / PIL)
  - Clinical Trial Documentation (CTD modules)
  - Patent claims (secondary priority)
  - Pharmacovigilance periodic safety update reports (PSURs)
  key_regulatory_standards:
    EMA_SmPC_guideline: 'Current EMA SmPC template is QRD (Quality Review of Documents)
      template v10.4, published February 2024. The ongoing revision toward QRD v11
      was launched in September 2023, focused on improving PIL structure and content
      under Regulation (EU) 2023/1182. The QRD convention document is EMA/62470/2007
      (rev. 8). SmPC structure follows 12 sections; sections 4.1–4.9 cover clinical
      particulars including indications, dosing, contraindications, warnings, interactions,
      pregnancy, effects on driving, undesirable effects, and overdose. (Source: EMA
      QRD templates page — [WEB-6];
      EMA QRD template v10.4 PDF — [WEB-7])'
    ANSM_circulars: 'ANSM operates under the French Public Health Code (Code de la
      santé publique), specifically Art. L. 5121-8 FPHC for national MA decisions.
      ANSM uses a ''Feuille de style'' template (aligned with current QRD template)
      for French product information submissions. For MRP/DCP procedures, the CMDh
      annotated QRD template (March 2024, corrected September 2025) applies (Source:
      HMA CMDh QRD — [WEB-8];
      PharmaLex France regulatory overview — [WEB-5]).
      Specific ANSM circular references for drug labeling compliance are published
      on the ANSM website in French only and were not individually enumerated in available
      English-language sources; direct retrieval from ansm.sante.fr required.'
    ICH_guidelines: 'The EMA SmPC is tightly aligned with the ICH CTD (Common Technical
      Document) structure. Under ICH M4E (efficacy), SmPC sections should mirror data
      in the clinical overview and clinical summary. ICH M4Q (quality) guides SmPC
      section 2 (composition) and section 6 information. ICH E3 governs clinical study
      reports (CSR) used in CTD Module 5. (Source: PharmaCores SmPC analysis — [WEB-9];
      EMA product information reference documents — [WEB-10])'
  applicable_data_protection_regulation: 'RGPD (GDPR as transposed into French law
    via Loi Informatique et Libertés, Law n° 78-17 of 6 January 1978, as amended).
    For health data hosting, French law additionally requires HDS (Hébergeur de Données
    de Santé) certification under Art. L.1111-8 of the Public Health Code — hosting
    health data without HDS certification is prohibited (Source: CMS Digital Health
    France — [WEB-11];
    IntuitionLabs pharma IT compliance — [WEB-12]).
    ANSM and CNIL jointly oversee AI/health-system compliance (Source: ICLG Digital
    Health France 2025 — [WEB-13]).
    Under the EU AI Act (now in force), pharmaceutical AI decision-support systems
    serving medical purposes are classified as high-risk under Annex III, triggering
    data governance, transparency, human oversight, and accountability obligations
    (Source: European Pharmaceutical Review — [WEB-14]).'
  icd_10_usage: System maps pathologies to ICD-10 chapter axes; alignment with hospital
    coding conventions acknowledged as imperfect in complex multi-morbid cases.
  atc_code_usage: '[NEEDS VERIFICATION — deferred: below search budget; whether ANSM
    mandates ATC code annotation in specific labeling document sections is a detailed
    regulatory procedural question best confirmed directly via ANSM''s published guidelines
    on ansm.sante.fr or expert elicitation.]'
regulatory_entity_vocabulary:
  description: Highly specific, normatively loaded vocabulary required for deployment
    NER tasks — largely absent from DrBenchmark's label taxonomies.
  required_entity_types:
  - International Non-proprietary Names (INNs)
  - ATC (Anatomical Therapeutic Chemical) codes
  - Excipient names (INCI / European Pharmacopoeia nomenclature)
  - Posology expressions (dose, frequency, route of administration per EMA templates)
  - Contraindication qualifiers (population subgroup exclusions, condition-specific
    restrictions)
  - EMA SmPC section identifiers (sections 4.1–4.9 structural markers)
  - Pharmacovigilance signal terms
  - Special warning and precaution phrases
  - MedDRA terminology (per QRD Appendix II, used in SmPC section 4.8 undesirable
    effects)
  benchmark_coverage_of_entity_types: Partial — DEFT-2021 NER includes DOSAGE, MODE,
    SUBSTANCE, TREATMENT categories; PxCorpus NER includes drug, dose, mode. No label
    set enumerates INNs, ATC codes, excipient nomenclature, or EMA-specific contraindication
    qualifier classes.
  crosswalk_to_benchmark_labels: '[NOT FOUND — searched French biomedical NLP benchmark
    literature and EMA/ANSM regulatory NER annotation scheme sources; no published
    crosswalk between EMA/ANSM regulatory annotation guidelines and DrBenchmark NER
    schemas was identified. The closest analogous resource is DART (Drug Annotation
    from Regulatory Texts), a 2024 Italian-language structured corpus of SmPCs from
    AIFA with NER and relation extraction for active substances, administration routes,
    pharmacokinetic mechanisms, and pregnancy risk categories — but this is Italian,
    not French, and no equivalent French regulatory SmPC NER corpus was found (Source:
    arXiv DART — [WEB-15]). This null result is itself
    informative: no French-language regulatory NER annotation scheme crosswalk appears
    to exist in the published literature as of 2024–2025.]'
  net_new_comparable_resource_note: 'DART (2024) — a structured Italian-language corpus
    of ~95 million tokens derived from Italian RCPs (SmPCs) published by AIFA — provides
    the closest existing model for what a French regulatory NLP benchmark would require.
    It covers NER/RE for active substances, administration routes, contraindications,
    adverse drug reactions, and drug-drug interactions, with high section coverage
    (>90% across most SmPC sections). No equivalent French-language resource was identified.
    This gap reinforces the IO/IC validity concerns for the deployment context. (Source:
    arXiv DART paper — [WEB-15])'
languages:
  primary: French (Metropolitan standard)
  secondary_variants:
  - French as used in Martinique
  - French as used in Guadeloupe
  - French as used in French Guiana
  - French as used in Réunion
  - French as used in Mayotte
  regulatory_latin_terminology: Extensive use of Latin-origin pharmaceutical terminology,
    INN stems, IUPAC chemical nomenclature — standard across EU regulatory text regardless
    of language variant.
  note: No diglossia, script mismatch, or major dialectal divergence for the primary
    metropolitan deployment. Overseas territory variants introduce some lexical specificity
    but remain standard French. Regulatory text is highly formulaic and genre-constrained
    rather than dialectally variable.
writing_systems:
  scripts:
  - Latin alphabet with diacritics (é, è, ê, ë, à, â, ô, î, ï, ù, û, ü, ç, œ, æ)
  note: No script mismatch between benchmark and deployment. All regulatory and biomedical
    text in scope uses standard French Latin orthography. Chemical formulae and abbreviations
    (e.g., INN stems) follow IUPAC conventions within the Latin script.
infrastructure_notes:
  deployment_modality: Text-only document processing pipeline; no audio, image, or
    cross-modality considerations.
  it_environment: Institutional pharmaceutical or regulatory agency IT infrastructure
    (metropolitan France). High-reliability enterprise environment expected.
  internet_infrastructure_metropolitan_france: 'France is among Europe''s most digitally
    developed markets. For health data hosting specifically, French law (Art. L.1111-8
    Public Health Code) mandates HDS (Hébergeur de Données de Santé) certification
    for any service hosting personal health data — a France-specific requirement beyond
    GDPR that applies to pharmaceutical AI tools processing patient-linked regulatory
    data (Source: IntuitionLabs — [WEB-12]).
    Enterprise pharma IT infrastructure in France is mature and well-connected; no
    infrastructure bottleneck for the primary metropolitan deployment is anticipated.
    [NOT FOUND — specific enterprise broadband penetration figures for major French
    pharma companies and ANSM were not published in retrievable form; this slot is
    low-impact for scoring.]'
  nlu_tooling_ecosystem: 'French is a high-resource NLP language; French biomedical
    models available (DrBERT-FS, DrBERT-CP, CamemBERT-bio, AliBERT). DrBERT pre-trains
    from scratch on French biomedical data and outperforms continual-pretraining variants
    on classification tasks; CamemBERT-bio (continual pre-training from CamemBERT)
    shows slight advantage on NER tasks (Source: arXiv adaptation study — [WEB-16]).
    A 2024 long-document adaptation study introduced DrLongformer-CP, which achieves
    higher average F1 across all tasks and has advantages for sequences >512 tokens
    — relevant for full SmPC documents (Source: arXiv 2402.16689 — [WEB-16]).
    Regulatory-domain fine-tuned models are not documented in the benchmark.'
  benchmark_toolkit: HuggingFace Datasets + Transformers; PyTorch-based; normalized
    data loaders — compatible with standard institutional ML infrastructure.
  overseas_territory_infrastructure: '[NEEDS VERIFICATION — deferred: below search
    budget; IT infrastructure and connectivity figures for French overseas DROM are
    likely available from INSEE or ARCEP but were not retrieved; low impact for scoring
    given the primary deployment is metropolitan France.]'
document_genre_coverage:
  description: 'Central content-validity dimension: the benchmark''s input taxonomy
    versus the deployment''s primary document genres.'
  benchmark_genres_present:
  - Clinical cases (CAS, DEFT-2021, E3C, DiaMed, CLISTER)
  - Scientific literature abstracts and titles (QUAERO MEDLINE, MorFITT, Mantra-GSC
    Medline)
  - EMEA drug labels — as pre-existing NLP research corpus (QUAERO EMEA, Mantra-GSC
    EMEA, DEFT-2020)
  - Clinical trial protocols (ESSAI)
  - Spoken drug prescriptions — transcribed (PxCorpus)
  - Pharmacy specialization exam questions (FrenchMedMCQA)
  deployment_genres_not_covered:
  - Current-format EMA SmPC documents (RCP) with mandatory section structure 4.1–4.9
    per QRD template v10.4
  - Patient information leaflets conforming to current EMA/ANSM PIL template (QRD
    v10.4, under revision to v11 since September 2023)
  - CTD (Common Technical Document) modules for regulatory submission (ICH M4E/M4Q
    aligned)
  - ANSM-format national authorization dossiers (including 'Feuille de style' and
    blue-box requirements)
  - PSURs / pharmacovigilance periodic reports
  - Patent claims with regulatory relevance
  quaero_emea_caveat: QUAERO EMEA labels are a pre-existing research corpus, not live
    regulatory submissions with current EMA QRD v10.4 formatting conventions; nested
    annotations partially lost in preprocessing (6.06% annotation loss); long EMEA
    documents sentence-split, disrupting document-level regulatory structure. The
    EMEA source documents in QUAERO predate the current QRD template revision cycle
    (v11 revision began September 2023).
  genre_gap_severity: High — the benchmark's primary genres are clinical/research
    NLP; the deployment's primary genres are legally constrained regulatory submissions.
    This is the central content-validity gap identified by the assessment.
  web_search_target: 'Confirmed — no DrBenchmark task derives from current EMA QRD-formatted
    SmPCs, current PIL templates, CTD modules, or ANSM-format national submissions.
    QUAERO EMEA and DEFT-2020 drug labels approach the domain but are pre-existing
    research corpora not aligned to current QRD template conventions. The only existing
    regulatory SmPC NLP corpus identified is DART (Italian, 2024); no French equivalent
    was found (Source: arXiv DrBenchmark — [WEB-17];
    arXiv DART — [WEB-15]).'
sts_scoring_calibration:
  description: Regulatory equivalence scoring requirements versus benchmark STS calibration.
  benchmark_sts_scale: 0–5 Likert continuous similarity score (Spearman correlation
    + EDRM evaluation metrics)
  benchmark_sts_sources: Clinical case sentence pairs (CLISTER), clinical cases /
    encyclopedia / drug labels (DEFT-2020)
  deployment_requirement: Scoring function must distinguish legally significant small-magnitude
    differences (dose thresholds, subpopulation qualifiers, temporal modifiers) that
    constitute distinct regulatory meaning under EMA/ANSM standards — not just general
    semantic proximity.
  gap_assessment: Full gap — benchmark STS scale reflects general semantic proximity;
    no documentation of calibration for regulatory-legal equivalence distinctions.
    DrBERT-FS does not excel on STS tasks, suggesting current scoring functions may
    underperform for fine-grained legal discrimination.
  regulatory_equivalence_threshold: '[NOT FOUND — searched regulatory affairs NLP
    literature and EMA/ANSM guidance sources; no published scoring rubric or threshold
    for EMA/ANSM safety-warning equivalence in NLP contexts was identified. The EMA
    QRD template mandates standard statements ''whenever applicable'' and requires
    case-by-case justification for deviations, but does not specify a numerical paraphrase-distance
    threshold (Source: EMA QRD product information reference docs — [WEB-10]).
    This slot requires regulatory affairs expert or legal elicitation; it is unlikely
    to be documented in machine-readable form.]'
  mandatory_review_threshold: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (system-internal design parameter); the specific confidence-score threshold triggering
    mandatory human regulatory review is a deployment implementation detail not published
    externally.]'
annotation_workforce_and_ground_truth:
  description: Alignment between benchmark annotation expertise and the regulatory
    expertise required for deployment ground truth.
  benchmark_annotator_profiles:
  - Clinical case reviewers
  - Medical experts (one per DiaMed annotation team)
  - NLP researchers
  deployment_ground_truth_authority:
  - Regulatory affairs specialists
  - Pharmacovigilance officers
  - Legal experts applying EMA SmPC guidelines and ANSM circulars
  gap_assessment: Full gap — no benchmark annotation process documentation mentions
    regulatory affairs or legal expertise. The authority structure for what constitutes
    a correct label in the deployment context (EMA/ANSM normative compliance) is categorically
    different from the clinical/research expert judgment used in benchmark annotation.
  inter_annotator_agreement_notes:
    diamed: Cohen's Kappa and Gwet's AC1 computed over two sessions of 15 clinical
      cases each — narrow validation base.
    clister: Scores averaged across multiple annotators (number not specified).
    cas: Automatic annotations at 98% precision — silver standard.
    deft_2021: Manual annotation; no IAA statistics reported in benchmark paper.
    others: '[NOT FOUND — IAA statistics for QUAERO, Mantra-GSC, E3C, MorFITT, ESSAI
      are inherited from original source papers; a 2024 systematic benchmark evaluation
      of French clinical NER (HAL 04523267) confirms that these source papers use
      varying evaluation methodologies (token-level vs. entity-level, with/without
      nested entities), making cross-task IAA comparison unreliable (Source: HAL benchmark
      evaluation — [WEB-18]).]'
  silver_standard_propagation: 'The CAS corpus uses automatic annotations validated
    at 98% precision — a silver standard. A 2024 clinical NER study confirms that
    silver-standard annotations from E3C layer 2 can be useful for training but evaluation
    should use gold-standard layer 1 annotations (Source: HAL 04523267 — [WEB-18]).
    Across the 20 tasks, annotation quality is uneven: DiaMed has the narrowest IAA
    base (15 cases per session); DEFT-2021 reports no IAA; CLISTER averaging methodology
    masks annotator disagreement. No single authoritative gold-standard IAA threshold
    is documented for the full DrBenchmark suite.'
overseas_territory_specifics:
  territories:
  - Martinique
  - Guadeloupe
  - French Guiana
  - Réunion
  - Mayotte
  regulatory_status: 'The five French overseas territories listed (Martinique, Guadeloupe,
    French Guiana, Réunion, Mayotte) are all overseas departments and regions (DROM),
    governed by Article 73 of the French Constitution. Under this article, French
    laws and regulations — including ANSM pharmaceutical regulations and EU pharmaceutical
    law — apply there under the same conditions as in metropolitan France, with the
    possibility of adaptation to local characteristics. They are not separate regulatory
    jurisdictions; ANSM authorization applies identically. (Source: Statista/INSEE
    overseas France overview — [WEB-19];
    Wikipedia DROM — [WEB-20])'
  disease_prevalence_gaps:
    description: French overseas territories have distinct disease prevalence patterns
      not reflected in mainland French biomedical datasets.
    tropical_pathologies_not_covered:
    - Dengue fever (dengue)
    - Chikungunya
    - Paludisme (malaria — relevant to French Guiana)
    - Zika virus disease
    - Leptospirosis
    - Other vector-borne diseases endemic to Caribbean and Indian Ocean territories
    benchmark_coverage: Full gap — no DrBenchmark data sources from overseas territories;
      DiaMed (Pan African Medical Journal) covers sub-Saharan African clinical cases,
      not French overseas department pathologies; tropical disease terminology absent
      from all label sets.
    vocabulary_adaptation_needed: '[NEEDS VERIFICATION — deferred: likely unsearchable
      in searchable form; whether specific regulatory entity vocabulary or safety
      warning phrasing differs for products with tropical-pathology indications in
      French overseas territories requires expert elicitation with ANSM or pharmacovigilance
      specialists covering DOM health authorities (ARS).]'
  population_size_by_territory: 'Approximate populations (recent estimates): Réunion
    ~901,000 (most populous overseas territory); Guadeloupe ~400,000; Martinique ~375,000
    (declining since 2008 due to emigration); French Guiana ~306,000 (fastest-growing,
    >2% growth 2014–2020); Mayotte ~279,000. Combined DROM population approximately
    2.26 million. (Source: WorldAtlas overseas France — [WEB-21];
    LCANews territories overview — [WEB-22];
    Statista INSEE 2024 — [WEB-23])

    Note: These are general population figures. The regulatory affairs professional
    workforce in these territories is a small fraction of total population; no territory-specific
    count of pharma regulatory professionals was found.'
cultural_and_professional_norms:
  professional_culture: Highly formalized regulatory affairs culture governed by EU
    and national pharmaceutical law. Professional norms emphasize precision, legal
    accountability, and documented decision trails. Outputs are used in high-stakes
    submission contexts where errors carry regulatory and legal consequences.
  language_register: Formal, highly technical, legally constrained regulatory French
    — distinct from clinical or research prose. Formulaic section structures mandated
    by EMA/ANSM templates.
  tolerance_for_system_error: Low — system errors that pass non-compliant labeling
    or generate false-positive flags have direct regulatory and patient-safety consequences.
    Human-in-the-loop design reflects this risk intolerance.
  professional_liability_context: 'French pharmaceutical liability is governed by
    Articles 1245 et seq. of the Civil Code (strict product liability regardless of
    authorization), Art. L.1142-1 of the Public Health Code (healthcare professional
    liability), and GDPR/Loi Informatique et Libertés for data processing. AI-enabled
    clinical decision support software in France is subject to: (1) Medical Device
    Regulation (MDR) if it qualifies as a medical device; (2) GDPR for personal data;
    (3) EU AI Act (high-risk classification under Annex III for medical-purpose AI);
    and (4) the 2024 EU Product Liability Directive (EU 2024/2853), which must be
    transposed by December 2026 and expands liability for defective AI-enabled products.
    ANSM and CNIL jointly enforce compliance (Source: ICLG Digital Health France 2025
    — [WEB-13];
    Bird & Bird AI liability France — [WEB-24];
    Chambers Digital Healthcare France 2025 — [WEB-25]).
    For a regulatory document compliance tool (non-clinical, advisory), MDR classification
    as a medical device may not apply, but GDPR and AI Act obligations remain relevant.'
  decision_authority_norms: Physicians and nurses retain final clinical decision authority;
    regulatory affairs specialists and legal experts retain submission compliance
    authority. System operates in advisory capacity only.
model_performance_context:
  best_performing_benchmark_models:
  - DrBERT-FS (highest on 8/20 tasks)
  - DrBERT-CP (highest on 5/20 tasks)
  - CamemBERT-bio (highest on 2/20 tasks)
  sts_performance_concern: DrBERT-FS does not excel on MLC or STS tasks — the two
    task categories most relevant to the deployment's compliance-checking and semantic
    equivalence functions.
  no_single_model_dominates: No single model excels across all 20 tasks; model selection
    for regulatory deployment cannot rely on overall benchmark rank.
  regulatory_domain_finetuning_availability: '[NOT FOUND — no French biomedical language
    model fine-tuned specifically on EMA QRD-format SmPCs or ANSM regulatory submission
    text was identified in the published literature. DrBERT and CamemBERT-bio pre-training
    corpora include drug leaflets (EMEA source), scientific articles, and clinical
    cases, but not current-format regulatory submission documents (Source: CamemBERT-bio
    paper — [WEB-26]; DrBERT paper — [WEB-27]).
    The 2024 long-document adaptation study introduced DrLongformer-CP with advantages
    for sequences >512 tokens, which is relevant for full SmPC documents but was not
    evaluated on regulatory submission text (Source: arXiv 2402.16689 — [WEB-16]).
    This is a confirmed gap: no regulatory-domain fine-tuned French model exists in
    the literature as of 2024–2025.]'
  quaero_preprocessing_artifact: QUAERO EMEA preprocessing in DrBenchmark lost 6.06%–8.90%
    of nested annotations and sentence-split long documents — systematic measurement
    error particularly relevant for regulatory text where nested entity structures
    may carry compliance significance.
  net_new_model_note: 'CamemBERT 2.0 (CamemBERTv2 / CamemBERTav2) was released in
    late 2024 as updated encoder models addressing temporal concept drift in the 2019
    CamemBERT; these were not evaluated in DrBenchmark (2024) and represent a potential
    performance improvement for regulatory NLP tasks (Source: arXiv CamemBERT 2.0
    — [WEB-28]). AliBERT (pre-trained primarily on
    ScienceDirect articles and Sudoc theses) is also available and outperforms CamemBERT
    and FlauBERT on two biomedical downstream tasks but was not evaluated in DrBenchmark
    (Source: CamemBERT-bio paper — [WEB-26]).'
dimension_priority_summary:
  IO:
    priority: HIGH
    rationale: Benchmark genres (clinical notes, research abstracts, clinical trial
      protocols) do not match deployment genres (SmPCs, PILs, CTD modules, ANSM submissions).
      QUAERO EMEA labels approach but do not replicate current QRD v10.4 regulatory
      submission formats. No French regulatory NLP benchmark exists; the closest is
      Italian DART (2024).
  IC:
    priority: HIGH
    rationale: Benchmark NER label inventories (UMLS Semantic Groups, MeSH, ICD-10)
      do not include INNs, ATC codes, excipient nomenclature, or EMA-specific contraindication
      qualifiers. System's own ICD-10 mapping focus suggests further category mismatch
      with regulatory entity vocabulary. MedDRA terminology (required for SmPC section
      4.8) is absent from all benchmark label sets.
  IF:
    priority: LOWER
    rationale: Both benchmark and deployment are text-only, high-resource French,
      Latin script. No modality, script, or infrastructure mismatch. Lowest validity
      concern.
  OO:
    priority: HIGH
    rationale: Benchmark STS 0–5 Likert scale reflects general semantic proximity;
      deployment requires regulatory-equivalence judgments sensitive to legally significant
      small differences. No published regulatory-equivalence scoring rubric exists
      for EMA/ANSM standards in NLP. Full calibration gap confirmed.
  OC:
    priority: HIGH
    rationale: Benchmark annotations produced by clinical/research professionals;
      deployment ground truth requires regulatory affairs and legal expertise applying
      EMA/ANSM normative frameworks. Direct convergent validity threat. IAA quality
      is uneven across the 20 tasks; CAS uses silver-standard labels; DiaMed IAA covers
      only 15 cases per session.
  OF:
    priority: MODERATE
    rationale: Text-label and continuous-score output formats are structurally compatible
      with deployment's multi-candidate confidence-score and human-review flagging
      design. Gap remains in confidence score granularity and mandatory-review threshold
      calibration. EU AI Act high-risk classification adds transparency and auditability
      requirements not benchmarked in DrBenchmark.
flagged_gaps_for_web_search:
- gap_id: 1
  topic: Regulatory document genre coverage in DrBenchmark
  search_target: French biomedical NLP benchmark SmPC patient information leaflet
    EMA regulatory NER evaluation dataset
  resolution_status: RESOLVED — confirmed full gap. No DrBenchmark task derives from
    current EMA QRD-formatted SmPCs or current PIL templates. QUAERO EMEA and DEFT-2020
    drug labels are pre-existing research corpora predating QRD v10.4. No French regulatory
    SmPC NLP corpus found; DART (Italian, 2024) is the closest analogous resource
    in any language.
- gap_id: 2
  topic: Regulatory entity taxonomy alignment (INNs, ATC, excipients, posology, contraindications)
    vs. DrBenchmark NER schemas
  search_target: EMA ANSM regulatory NER annotation scheme INN ATC excipient contraindication
    French NLP benchmark crosswalk
  resolution_status: RESOLVED (null) — no published crosswalk found between EMA/ANSM
    regulatory annotation guidelines and DrBenchmark NER schemas. MedDRA (used in
    SmPC section 4.8) is confirmed absent from all benchmark label sets. DART (Italian)
    provides a model entity schema but has no French equivalent.
- gap_id: 3
  topic: STS scoring calibration for regulatory equivalence
  search_target: semantic textual similarity regulatory equivalence scoring EMA drug
    labeling safety warning French NLP calibration
  resolution_status: RESOLVED (null) — no published scoring rubric or NLP calibration
    for EMA/ANSM safety-warning equivalence found. EMA QRD mandates standard statements
    but specifies no numerical paraphrase threshold.
- gap_id: 4
  topic: Annotation workforce regulatory expertise for DrBenchmark ground truth
  search_target: biomedical NLP annotation regulatory affairs pharmacovigilance ground
    truth EMA ANSM French label quality expert annotator
  resolution_status: RESOLVED — confirmed full gap. No regulatory affairs or legal
    expertise in any benchmark annotation process. IAA variability across tasks confirmed
    by independent 2024 clinical NER benchmark study.
- gap_id: 5
  topic: French overseas territories coverage and tropical disease vocabulary in DrBenchmark
  search_target: French overseas territories biomedical NLP tropical pathology NER
    dataset Martinique Guadeloupe Réunion French Guiana clinical NLP
  resolution_status: RESOLVED (null) — no overseas territory data in DrBenchmark confirmed.
    Population figures resolved. DROM regulatory status (Article 73 — same French/EU
    law applies) resolved.
- gap_id: 6
  topic: ANSM versus EMA normative alignment for safety-warning compliance scoring
  search_target: ANSM vs EMA safety warning divergence France national procedure centralized
    procedure drug labeling compliance NLP evaluation
  resolution_status: 'PARTIALLY RESOLVED — core divergence confirmed: France-specific
    blue-box requirements (CIP codes, Exploitant, List I/II classification) and ''Feuille
    de style'' template add national layer absent from QUAERO EMEA corpus. Full specification
    of ANSM circular requirements requires direct retrieval from ansm.sante.fr or
    expert elicitation.'
- gap_id: 7
  topic: Silver-standard label quality and inter-annotator agreement across DrBenchmark
    tasks
  search_target: DrBenchmark annotation quality inter-annotator agreement NER STS
    gold standard silver standard French biomedical NLP
  resolution_status: PARTIALLY RESOLVED — CAS silver-standard confirmed; IAA variability
    confirmed by independent 2024 evaluation. E3C silver-standard layer confirmed
    as supplementary to gold standard. Cross-task IAA comparison unreliable due to
    methodological heterogeneity.
- gap_id: 8
  topic: French biomedical language models fine-tuned on regulatory text
  search_target: DrBERT CamemBERT-bio fine-tuning SmPC regulatory submission EMA ANSM
    French pharmaceutical NLP
  resolution_status: RESOLVED (null) — no French biomedical LM fine-tuned on EMA SmPC
    or ANSM regulatory submission text found. DrBERT and CamemBERT-bio pre-training
    includes drug leaflets (EMEA source, not current QRD-formatted) but not regulatory
    submissions. CamemBERT 2.0 and AliBERT are net-new models not covered in DrBenchmark.
- gap_id: 9
  topic: Mandatory human-review threshold calibration in regulatory NLP pipelines
  search_target: automated compliance flagging threshold regulatory affairs NLP human
    review pharmaceutical labeling ANSM EMA
  resolution_status: DEFERRED — likely unsearchable (system-internal design parameter);
    EU AI Act transparency requirements for high-risk AI systems create external pressure
    for documenting such thresholds, but no published standard threshold was found.
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://iaocr.com/en/blog/french-regulatory-authority-for-clinical-trials |
| WEB-2 | https://pharma-blue.com/glossary/ansm/ |
| WEB-3 | https://www.glassdoor.com/Job/france-regulatory-affairs-jobs-SRCH_IL.0,6_IN86_KO7,25.htm |
| WEB-4 | https://www.lexology.com/library/detail.aspx?g=9eb5298b-3d96-448a-b563-7135317d423c |
| WEB-5 | https://www.pharmalex.com/thought-leadership/blogs/the-complex-landscape-of-french-regulatory-affairs/ |
| WEB-6 | https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/product-information-requirements/product-information-qrd-templates-human |
| WEB-7 | https://www.ema.europa.eu/en/documents/template-form/qrd-product-information-template-version-104-highlighted_en.pdf |
| WEB-8 | https://www.hma.eu/human-medicines/cmdh/templates/qrd.html |
| WEB-9 | https://pharmacores.com/smpc-summary-of-product-characteristics/ |
| WEB-10 | https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/product-information-requirements/product-information-reference-documents-guidelines-0 |
| WEB-11 | https://cms.law/en/int/expert-guides/cms-expert-guide-to-digital-health-apps-and-telemedicine/france |
| WEB-12 | https://intuitionlabs.ai/articles/compliance-frameworks-pharmaceutical-it-comparative-analysis |
| WEB-13 | https://iclg.com/practice-areas/digital-health-laws-and-regulations/france |
| WEB-14 | https://www.europeanpharmaceuticalreview.com/article/264445/ai-act-data-governance-and-compliance-strategy-implications-in-pharma/ |
| WEB-15 | https://arxiv.org/abs/2510.18475 |
| WEB-16 | https://arxiv.org/html/2402.16689v1 |
| WEB-17 | https://arxiv.org/html/2402.13432 |
| WEB-18 | https://hal.science/hal-04523267 |
| WEB-19 | https://www.statista.com/topics/10409/overseas-france/ |
| WEB-20 | https://en.wikipedia.org/wiki/Overseas_departments_and_regions_of_France |
| WEB-21 | https://www.worldatlas.com/geography/french-overseas-territories.html |
| WEB-22 | https://www.lcanews.com/en/frances-overseas-territories-explained/ |
| WEB-23 | https://www.statista.com/statistics/1320629/population-french-overseas-regions/ |
| WEB-24 | https://www.twobirds.com/en/insights/2026/france/ai-liability-in-light-of-the-new-2024-pld-expanded-liability-challenging-defences-and-new-evidentiar |
| WEB-25 | https://practiceguides.chambers.com/practice-guides/digital-healthcare-2025/france/trends-and-developments |
| WEB-26 | https://arxiv.org/abs/2306.15550 |
| WEB-27 | https://arxiv.org/pdf/2304.00958 |
| WEB-28 | https://arxiv.org/html/2411.08868v1 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark covers biomedical NER and STS tasks drawn from scientific literature and clinical cases, but pharmaceutical regulatory documents have distinctive text types — SmPCs, patient information leaflets, patent claims, and CTD modules. Are these document genres central to your use case, and does the system need to handle highly formulaic, legally constrained language specific to EU regulatory submissions rather than clinical or research prose?
A1: The system is optimized for Metropolitan France and would require adaptation before use in other French-speaking regions. French overseas territories are the highest secondary priority due to distinct disease prevalence patterns (e.g., tropical pathologies) not reflected in mainland datasets. The answer did not directly address regulatory document genres but confirms a mainland-France primary scope and flags regional text variation as a known concern.

Q2 [IC]: Regulatory drug labeling uses specific vocabulary — INNs, ATC codes, excipient nomenclature, posology expressions, EMA-template contraindication phrasing. Are these entity types representative of what the system must detect, or do your labeling tasks involve categories or patterns diverging from standard clinical/research text?
A2: The system is characterized as a "Silver Standard" clinical support tool rather than an authoritative classifier. It maps pathologies to standardized axes (e.g., ICD-10 chapters) but acknowledges imperfect alignment with hospital coding conventions in complex cases. Physicians and nurses retain decision authority. The answer implies the NER targets clinical/diagnostic entity types rather than specifically regulatory labeling vocabulary (INNs, posology templates, EMA phrasing), suggesting a possible category mismatch.

Q3 [OO]: For STS-based compliance checking, small lexical differences (dose thresholds, contraindicated population qualifiers) may have legal significance under EMA/ANSM standards even when a general biomedical STS scorer treats them as equivalent. Does the system require a regulatory-equivalence scoring function, and does a borderline score trigger automatic rejection or only human review?
A3: The system performs best on clean, standard medical documentation. It is resilient to moderate noise (common abbreviations, clinical shorthand) but not designed for highly disorganized or institution-specific shorthand, which would require pre-processing, custom glossaries, and normalization modules. The answer does not directly address whether the STS scoring function distinguishes regulatory-level semantic difference from general semantic proximity, leaving the scoring semantics unconfirmed.

Q4 [OC]: Ground-truth annotations in biomedical benchmarks are typically produced by clinical or research professionals, whereas authoritative regulatory judgment may rest with regulatory affairs specialists or legal experts. Are the annotation norms (e.g., EMA SmPC guidelines, ANSM circulars) likely to align with biomedical NLP annotator labels, or do systematic disagreements on borderline cases occur?
A4: The system outputs multiple candidate labels with confidence scores rather than a single authoritative label, allowing clinicians to adjudicate between plausible categories — especially for multi-morbid cases where a finding may belong to several classification axes. High-uncertainty entities are flagged for manual review. The answer confirms a human-in-the-loop design but does not resolve whether benchmark annotation norms (clinical/research professionals) align with the regulatory-legal standards the deployment context requires.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark draws from scientific literature and clinical cases, while the deployment centers on legally constrained regulatory document genres (SmPCs, leaflets, possibly patent claims) that are structurally and lexically distinct; overseas-territory sub-populations with tropical disease vocabulary add further genre and terminology gaps. |
| IC | HIGH | Regulatory labeling vocabulary (INNs, ATC codes, EMA posology templates, contraindication phrasing) is highly specific and normatively loaded; the user's answers indicate the system targets ICD-10 clinical mapping rather than regulatory entity types, suggesting the benchmark's concrete instances may not represent the actual entity vocabulary the deployment requires. |
| IF | LOWER | Both benchmark and deployment are text-only in high-resource French with no cross-modality or script mismatch, and metropolitan French infrastructure assumptions are consistent. |
| OO | HIGH | The benchmark's STS scoring reflects general biomedical semantic proximity, whereas the deployment requires regulatory-equivalence judgments where minor lexical differences carry legal consequence under EMA/ANSM standards; the user's answers did not confirm that the scoring function is calibrated for this stricter interpretive standard. |
| OC | HIGH | DrBenchmark labels are annotated by clinical and research professionals, but the authoritative ground truth for regulatory compliance rests with regulatory affairs specialists and legal experts applying EMA/ANSM norms; the multi-label confidence output and human adjudication loop confirm that label authority is contested, raising convergent validity concerns. |
| OF | MODERATE | The benchmark outputs labels and scores, which matches the system's multi-candidate confidence-score output and human-review flagging design; however, the granularity of confidence scoring and the threshold that triggers mandatory review are not benchmarked against regulatory workflow requirements. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Findings tagged CRITICAL
should be treated as strong evidence for lower scores on the affected dimensions.

## Dataset Analysis Report

**Benchmark:** DrBenchmark — A Large Language Understanding Benchmark for French Biomedical NLP
**Datasets analyzed:** 11 datasets (QUAERO, FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC, E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI)
**Analysis date:** 2025-07-11

---

### Per-Dataset Fit Assessment

#### DrBenchmark/QUAERO (EMEA config)
- **Task:** NER (token classification) on EMEA drug leaflets and MEDLINE biomedical titles
- **Deployment fit:** Partial — QUAERO is the closest any dataset comes to the deployment's primary document genre (regulatory drug product information). EMEA drug leaflet content is present with characteristic posology, contraindication, excipient list, and ATC code language (QUAERO-D1, QUAERO-D2, QUAERO-D3). However, critical gaps prevent strong fit.
- **Key concerns:**
  - **CRITICAL (IO, OO):** UMLS Semantic Group taxonomy (CHEM, DISO, PROC, etc.) conflates INNs, excipients, ATC codes, and chemical reagents under a single label; no regulatory sub-type distinction exists (QUAERO-D4, QUAERO-D5, QUAERO-D6). ATC codes are textually present but entirely unlabeled.
  - **MAJOR (IF, OF):** Sentence-splitting of long EMEA documents produces null sentences, isolated header fragments, and mixed-content token sequences — systematic preprocessing artifacts that corrupt regulatory document structure (QUAERO-D7, QUAERO-D8, QUAERO-D9, QUAERO-D10). 6.06% of nested annotations are lost per benchmark documentation.
  - **MAJOR (OC, OO):** Safety warnings and contraindications are present (QUAERO-D15, QUAERO-D16) but contraindication relationships and population qualifiers are not captured as distinct entity types; annotations reflect biomedical NLP researcher judgment, not regulatory affairs expertise.
  - **MINOR (IF):** Non-French tokens present from multi-country regulatory leaflet appendices (QUAERO-D11, QUAERO-D12).
  - **MINOR (IC):** Vocabulary coverage is limited to a small set of brand products (Refludan, TYSABRI, Prialt); broader regulatory deployment requires coverage across hundreds of active substances.

#### DrBenchmark/FrenchMedMCQA
- **Task:** Multiple-choice QA from French pharmacy specialization diploma exams
- **Deployment fit:** Weak — the dataset is exclusively MCQA format; it contributes neither NER nor STS task types central to the deployment. Regulatory entity vocabulary (INNs, ATC codes, posology templates, EMA phrasing) does not appear as labeled structured content.
- **Key concerns:**
  - **MAJOR (IO):** MCQA format is irrelevant to the deployment's NER and STS pipeline; no task-type alignment exists.
  - **MAJOR (IC):** Drug names appear only as answer options in pharmacological knowledge questions, not as labeled regulatory entities (FRENCHMEDMCQA-D5, FRENCHMEDMCQA-D6). Single instance of SmPC-adjacent terminology ("résumé des caractéristiques du produit") is definitional only (FRENCHMEDMCQA-D1).
  - **MAJOR (OC):** Ground truth reflects pharmacy licensing exam keys — authoritative for academic pharmacological facts but disconnected from EMA/ANSM compliance judgment (FRENCHMEDMCQA-D9).
  - **MINOR (OC):** Some questions may reflect dated regulatory status (hepatitis B vaccination obligations, WHO hypertension thresholds) (FRENCHMEDMCQA-D7, FRENCHMEDMCQA-D8).

#### DrBenchmark/DEFT2020
- **Task:** Semantic textual similarity (Task 1, 0–5 scale) and multi-class classification (Task 2)
- **Deployment fit:** Partial — DEFT2020 is the most relevant STS dataset for the deployment context because it includes drug labeling text pairs (contraindications, posology warnings, excipient instructions) from the DEFT 2020 challenge. However, the multi-genre design introduces substantial irrelevant content, and the scoring calibration is not suitable for regulatory equivalence.
- **Key concerns:**
  - **MAJOR (IO, IC):** Large fraction of non-medical encyclopedic content (beekeeping, sports, WWII history, railway infrastructure) has zero regulatory relevance (DEFT2020-D6, DEFT2020-D7, DEFT2020-D8, DEFT2020-D9). Drug-label pairs are real and deployment-relevant (DEFT2020-D1, DEFT2020-D2, DEFT2020-D3) but cannot be isolated without filtering.
  - **MAJOR (OO, OC):** The scoring rubric does not distinguish legally significant small differences from surface paraphrases. Omission of "sous stricte surveillance médicale" scores 3.6/5 (DEFT2020-D10); removal of a mechanistic qualifier scores 3.8 (DEFT2020-D11). These represent direct calibration failures for regulatory equivalence scoring.
  - **MAJOR (OC):** High annotator disagreement (>3 point range across 5 annotators) on drug-label pairs is documented (DEFT2020-D14, DEFT2020-D15); annotators are general rather than regulatory specialists.
  - **MAJOR (OO):** The `moy` and `vote` fields diverge substantially on multiple examples (up to 2.8-point gap), creating ambiguity about which score represents ground truth for model training and threshold-setting (DEFT2020-D18, DEFT2020-D19, DEFT2020-D20).

#### DrBenchmark/MORFITT
- **Task:** Multi-label medical specialty classification of biomedical research abstracts (12 specialty classes)
- **Deployment fit:** Weak — the dataset is exclusively scientific research abstracts classified by medical specialty. Neither genre nor label taxonomy aligns with the deployment's NER/STS regulatory compliance tasks.
- **Key concerns:**
  - **CRITICAL (IO, IC):** All content is research literature; no regulatory document genre present (MORFITT-D1, MORFITT-D2, MORFITT-D3).
  - **MAJOR (IC):** Significant international geographic provenance (Canada, Jordan, Egypt, Saudi Arabia, Japan, China) unrepresentative of metropolitan French regulatory text (MORFITT-D4 through MORFITT-D10).
  - **MAJOR (IO):** Veterinary medicine content included (MORFITT-D11, MORFITT-D12, MORFITT-D13, MORFITT-D14); irrelevant to human pharmaceutical regulatory compliance.
  - **MAJOR (OO):** 12-class specialty taxonomy has no alignment with EMA/ANSM regulatory entity types.
  - **MINOR (IF):** Some abstracts are translations from English, introducing register differences from native regulatory French (MORFITT-D16, MORFITT-D17).
  - **INFO:** One Chikungunya abstract relevant to overseas territories is present (MORFITT-D15) but as research content, not regulatory documentation.

#### DrBenchmark/CLISTER
- **Task:** STS on French clinical case sentence pairs (0–5 scale)
- **Deployment fit:** Weak — while CLISTER is an STS task, all content derives from clinical case reports. No regulatory document pairs exist, and the scoring calibration is insensitive to the numeric and lexical differences that carry legal consequence in EMA/ANSM labeling.
- **Key concerns:**
  - **CRITICAL (IO, IC):** All sentence pairs are clinical case prose; zero examples from SmPCs, patient leaflets, or regulatory submissions (CLISTER-D1, CLISTER-D2, CLISTER-D3).
  - **MAJOR (OO):** Scoring scale is insensitive to factually meaningful numeric differences: a twofold difference in a biological value scores 4.0 (CLISTER-D8); a 15-fold PSA difference scores 3.75 (CLISTER-D9); a 2 vs. 4.5 year follow-up difference scores 4.0 (CLISTER-D10). This calibration failure directly undermines regulatory equivalence checking.
  - **MAJOR (OC):** Annotators are clinical/research professionals; no regulatory affairs expertise confirmed. Ground truth does not reflect EMA/ANSM equivalence standards (CLISTER-D12, CLISTER-D13).
  - **MINOR (IC, OF):** Truncated sentences and table fragments introduce noise (CLISTER-D14, CLISTER-D15, CLISTER-D16).

#### DrBenchmark/MANTRAGSC
- **Task:** Biomedical NER (UMLS Semantic Groups, IOB2) across multiple language-source configurations
- **Deployment fit:** Weak — the sampled examples appear exclusively from the `fr_medline` configuration (research titles), not the `fr_emea` configuration (drug labels) that would be more deployment-relevant. NER label taxonomy replicates the same UMLS Semantic Group limitations as QUAERO.
- **Key concerns:**
  - **MAJOR (IO, IC):** Sampled content is entirely MEDLINE-style short clinical/research titles (MANTRAGSC-D1, MANTRAGSC-D2); `fr_emea` configuration — most relevant to deployment — was not represented in the analyzed sample. This is a structural sampling gap affecting interpretation.
  - **MAJOR (OO):** INN/excipient conflated under CHEM label with no sub-typing; no posology, ATC, or contraindication qualifier tags exist (MANTRAGSC-D8, MANTRAGSC-D9, MANTRAGSC-D10).
  - **MINOR (IC):** Non-metropolitan French geographic provenance in several titles (MANTRAGSC-D11, MANTRAGSC-D12); veterinary pathology present (MANTRAGSC-D13).
  - **MAJOR (OC):** Annotation by biomedical NLP researchers; no regulatory affairs expertise in annotation workflow.

#### DrBenchmark/E3C
- **Task:** NER for clinical entities (CLINENTITY) and temporal/factuality entities on French clinical case reports
- **Deployment fit:** Weak — all content is clinical case narrative; drug names and dosages appear extensively but are systematically unlabeled (O-tagged), confirming the label ontology targets pathology/symptom recognition exclusively.
- **Key concerns:**
  - **CRITICAL (IO, IC):** All examples are clinical case reports; no regulatory document genre present (E3C-D1, E3C-D2, E3C-D3).
  - **MAJOR (IO, OO):** Drug names (ciclosporine, vancomycine, fentanyl, metronidazole, isoniazide) appear frequently but are systematically tagged O (E3C-D4, E3C-D5, E3C-D6, E3C-D7). The label set captures pathologies/symptoms, not pharmacological or regulatory entity types.
  - **MAJOR (IC):** Multiple examples reference North African and sub-Saharan African clinical settings (E3C-D8, E3C-D9), not metropolitan French regulatory contexts.
  - **MINOR (IC, IF):** Tokenization artifacts from OCR/copy-paste provenance (E3C-D10, E3C-D11).

#### DrBenchmark/PxCorpus
- **Task:** Intent classification (4 classes) and NER (38 classes) on transcribed spoken drug prescription dictations
- **Deployment fit:** Weak — the spoken-language transcription register is fundamentally misaligned with the written regulatory document genre the deployment targets, despite partial NER label overlap with posology entity types.
- **Key concerns:**
  - **CRITICAL (IF):** All content is transcribed spoken dictation with pervasive spoken-language artifacts: disfluencies ("euh"), code-switching English/French (PXCORPUS-D2), automated system error messages embedded in utterances (PXCORPUS-D3), truncated words (PXCORPUS-D17, PXCORPUS-D18). NER models trained on this corpus are unlikely to transfer to written regulatory text.
  - **MAJOR (IO, IC):** No regulatory submission text, SmPC sections, or EMA-style safety warning language present (PXCORPUS-D9, PXCORPUS-D10). Spoken compliance-checking meta-commentary (PXCORPUS-D11) superficially resembles the deployment task but is a qualitatively different genre.
  - **MINOR (OO):** Severe class imbalance — `replace` class at ~0.6% of sample (PXCORPUS-D12, PXCORPUS-D13); full NER tag ontology (38 classes) not surfaced in HF metadata (PXCORPUS-D14, PXCORPUS-D15).
  - **INFO (IC):** INN/brand name distinction exists in NER label set (tag 10 vs. tag 22) (PXCORPUS-D6, PXCORPUS-D7); this partial overlap with deployment vocabulary does not compensate for the form mismatch.

#### DrBenchmark/DiaMED
- **Task:** Multi-class ICD-10 chapter classification of clinical case reports (22 chapters)
- **Deployment fit:** Weak — DiaMED is the only dataset with a named original contribution to DrBenchmark, but its geographic provenance (exclusively Pan African Medical Journal), its task type (ICD-10 chapter classification), and its annotation base make it poorly aligned with the deployment context.
- **Key concerns:**
  - **CRITICAL (IO, IC):** All examples are clinical case reports from sub-Saharan African clinical settings; no regulatory document genre present (DIAMED-D1, DIAMED-D2). All 14 sampled examples show African institutional provenance (DIAMED-D9, DIAMED-D3, DIAMED-D12).
  - **MAJOR (IC):** Geographic setting is uniformly non-metropolitan France; ICD-10 chapter classification reflects sub-Saharan African disease profiles, not the metropolitan French regulatory population (DIAMED-D9).
  - **MAJOR (OC):** IAA validated on only 30 total cases across 2 sessions (15 per session); narrow validation base for a 739-example corpus. Multi-system boundary cases (DIAMED-D5) may be inconsistently labeled without detection.
  - **MAJOR (OO):** ICD-10 chapter-level labels reflect diagnostic classification, not regulatory compliance; annotators are clinical experts, not regulatory affairs specialists.
  - **MINOR (IF):** Images present in schema but excluded from the NLP task; modality inflation in HF metadata.

#### DrBenchmark/DEFT2021
- **Task:** NER (14-class clinical entity types) and multi-label classification (23 MeSH Chapter C axes) on clinical case reports
- **Deployment fit:** Weak — DEFT2021's NER label set (DOSAGE, SUBSTANCE, TREATMENT) has the closest surface alignment to regulatory entity vocabulary within the benchmark, but the deployment-critical token types are annotated in clinical narrative context, not regulatory labeling structure.
- **Key concerns:**
  - **CRITICAL (IO, IC):** All examples are clinical case reports; no regulatory document genre present (DEFT2021-D4). Drug names and doses appear in clinical narratives (DEFT2021-D2, DEFT2021-D5, DEFT2021-D6) rather than in EMA SmPC-structured posology or contraindication sections.
  - **MAJOR (IC):** DOSAGE and SUBSTANCE/TREATMENT annotations are calibrated for clinical case-report annotation norms, not EMA/ANSM regulatory labeling annotation norms (DEFT2021-D10, DEFT2021-D11). No ATC codes, excipient names, or contraindication qualifiers observed.
  - **MAJOR (IO):** Strong urology/oncology sub-domain bias in sampled cases (DEFT2021-D8) may not represent the breadth of disease categories in regulatory labeling documents.
  - **MAJOR (OC):** No IAA statistics reported in benchmark paper for DEFT2021 NER; no regulatory affairs expertise in annotation workflow.
  - **MINOR (OF):** Some IOB2 annotation inconsistencies visible at entity boundaries (DEFT2021-D13, DEFT2021-D14).

#### DrBenchmark/CAS
- **Task:** POS tagging (31 classes, silver-standard), negation/speculation classification, and NER for negation/speculation on French clinical case reports
- **Deployment fit:** Weak — POS tagging has no direct relevance to the deployment's NER/STS pipeline; negation/speculation classification is a tangentially useful sub-component but is calibrated on clinical case negation patterns, not regulatory safety-warning negation.
- **Key concerns:**
  - **MAJOR (IO, IC):** Exclusively clinical case narrative genre; no regulatory document content present (CAS-D1, CAS-D5). Drug/dose mentions are narrative-embedded, not in regulatory labeling format (CAS-D22, CAS-D63).
  - **MAJOR (OO):** Sampled config is POS tagging — not aligned to NER or STS deployment tasks (CAS-D2).
  - **MAJOR (OC):** Silver-standard annotation at 98% precision introduces systematic noise; annotation by NLP researchers and automated tools, no regulatory expertise.
  - **MINOR (IC):** Possible non-metropolitan French clinical cases in sample (CAS-D15, CAS-D44).

#### DrBenchmark/ESSAI
- **Task:** POS tagging (36-class ESSAI-specific scheme), negation/speculation NER and classification on French clinical trial protocols
- **Deployment fit:** Weak — clinical trial protocol genre is meaningfully distinct from regulatory labeling documents; vocabulary is dominated by experimental drug codes and trial-procedure language rather than approved product labeling vocabulary.
- **Key concerns:**
  - **MAJOR (IO, IC):** Genre is clinical trial protocols (partially patient-facing informed consent documents), not SmPCs or patient leaflets (ESSAI-D4, ESSAI-D5, ESSAI-D6). Regulatory term "autorisation de mise sur le marché" appears only incidentally (ESSAI-D7).
  - **MAJOR (IC):** Drug vocabulary consists primarily of experimental compound codes (BMS-986179, MEDI9197, LY3200882) not representative of approved product labeling (ESSAI-D8, ESSAI-D9). Approved drugs appear in trial arm context only (ESSAI-D10).
  - **MINOR (IC, OO):** Negation/contraindication language present but structurally different from SmPC safety-warning negation (ESSAI-D3, ESSAI-D11); trial-context negation (eligibility criteria) ≠ labeling-context negation.
  - **MINOR (OF):** ESSAI-specific 36-class POS scheme not directly portable to regulatory document tokenization (ESSAI-D14); possible transcription artifact detected (ESSAI-D15).
  - **MAJOR (OC):** Silver-standard TreeTagger annotations; no regulatory affairs expertise in annotation workflow.

---

### Cross-Cutting Findings

#### CRITICAL

**C1 — Universal genre mismatch: clinical/research prose vs. regulatory submission text (IO, IC)**
Every dataset in the benchmark derives from clinical case reports, research abstracts, scientific literature, clinical trial protocols, exam questions, or transcribed speech. Not a single dataset contains examples drawn from current-format EMA SmPCs (QRD template v10.4), patient information leaflets conforming to current PIL templates, CTD modules, or ANSM-format national authorization dossiers. QUAERO EMEA is the closest approximation but its source documents predate the current QRD revision cycle and have been preprocessed in ways that destroy document structure. This gap is confirmed across QUAERO-D7, QUAERO-D8, CLISTER-D1, E3C-D1, DEFT2021-D4, DIAMED-D1, CAS-D1, ESSAI-D4, PxCorpus-D9, MORFITT-D1, MANTRAGSC-D1, DEFT2020-D6.

**C2 — Universal NER label taxonomy misalignment with regulatory entity types (OO)**
Across all NER datasets (QUAERO, MANTRAGSC, E3C, DEFT2021, PxCorpus), the label ontologies use UMLS Semantic Groups (CHEM, DISO, PROC), clinical entity types (CLINENTITY, PATHOLOGY, SOSY), or spoken-prescription categories (drug, dose, mode). No label set distinguishes INNs from excipients from chemical reagents (QUAERO-D4, QUAERO-D5, QUAERO-D6, MANTRAGSC-D8). ATC codes are textually present in QUAERO (QUAERO-D3) but unlabeled. MedDRA terminology (required for SmPC section 4.8) is absent from all label sets. Contraindication qualifiers and EMA SmPC section structural markers are absent from every dataset.

#### MAJOR

**M1 — STS scoring calibration failure for regulatory equivalence (OO)**
Both STS datasets (DEFT2020, CLISTER) use 0–5 Likert averaged similarity scales that are insensitive to legally significant small differences. DEFT2020 scores the omission of "sous stricte surveillance médicale" at 3.6/5 (DEFT2020-D10); omission of a mechanistic qualifier at 3.8 (DEFT2020-D11); addition of an alcohol warning at 3.8 (DEFT2020-D12). CLISTER scores a twofold biological value difference at 4.0 (CLISTER-D8) and a 15-fold PSA difference at 3.75 (CLISTER-D9). This pattern is consistent across both datasets and directly undermines the deployment's requirement for regulatory-equivalence scoring. No published regulatory-equivalence scoring rubric for EMA/ANSM NLP exists to substitute.

**M2 — Annotation workforce has no regulatory affairs expertise across all datasets (OC)**
Every dataset in the benchmark was annotated by clinical case reviewers, NLP researchers, automated tools (CAS/ESSAI — silver standard), or domain-subject-matter experts (one medical expert in DiaMED). No dataset documentation mentions regulatory affairs specialists, pharmacovigilance officers, or legal experts applying EMA SmPC guidelines or ANSM circulars. This is confirmed across QUAERO, DEFT2021 (DEFT2021-D4), CLISTER (CLISTER-D12), DiaMED (DIAMED-D5), CAS, ESSAI. For a deployment where authoritative ground truth rests with regulatory-legal professionals, this is a direct and unmitigated convergent validity threat.

**M3 — High annotator disagreement on drug-label pairs in both STS datasets (OC)**
DEFT2020 shows 5-annotator score ranges of 3+ points on drug-label pairs (DEFT2020-D14, DEFT2020-D15, DEFT2020-D16, DEFT2020-D17). CLISTER uses averaged scores without surfacing individual annotator variance. The DEFT2020 `moy`/`vote` divergence (DEFT2020-D18, DEFT2020-D19, DEFT2020-D20) creates ambiguity about which score should anchor threshold-setting for mandatory regulatory review. Neither dataset provides a definitive, adjudicated ground truth appropriate for regulatory compliance boundary decisions.

**M4 — Silver-standard and narrow IAA across classification/NER tasks (OC)**
CAS POS annotations are auto-generated at 98% precision (CAS-D2, consistent with benchmark documentation). ESSAI uses TreeTagger automatic annotation at 98% precision. DiaMED IAA is validated on only 30 total cases (DIAMED-D5). DEFT2021 reports no IAA statistics. This pattern of uneven and often narrow annotation quality assessment is consistent across tasks. Cross-task IAA comparison is unreliable due to methodological heterogeneity (confirmed by independent 2024 HAL evaluation study).

**M5 — Sub-Saharan African geographic provenance in multiple datasets (IC)**
Several datasets contain examples from African clinical settings that may introduce vocabulary and disease profile distributions unrepresentative of metropolitan French regulatory documents: DiaMED (entirely Pan African Medical Journal: DIAMED-D9), E3C (E3C-D8, E3C-D9), DEFT2021 (DEFT2021-D3, DEFT2021-D12), MANTRAGSC (MANTRAGSC-D11, MANTRAGSC-D12). This is distinct from and does not address the French overseas territory gap.

**M6 — PxCorpus input form fundamentally misaligned with written regulatory text (IF)**
PxCorpus is the only dataset where the IF concern rises to MAJOR/CRITICAL level. Spoken-language transcription artifacts (disfluencies, code-switching, system error messages, truncation) pervade the data (PXCORPUS-D1, PXCORPUS-D2, PXCORPUS-D3, PXCORPUS-D16, PXCORPUS-D17, PXCORPUS-D18) in ways that would impede transfer to written regulatory text NER. This is an isolated finding for this single dataset but represents the most severe IF concern in the benchmark.

**M7 — QUAERO EMEA preprocessing artifacts destroy regulatory document structure (IF, OF)**
The sentence-splitting and nested annotation loss documented in benchmark YAML [Q37] is confirmed in the data: null token/tag sequences (QUAERO-D9), isolated header fragments (QUAERO-D8), excessively long mixed-content sequences (QUAERO-D10). For regulatory compliance NER where nested entity structures may carry compliance significance (e.g., a CHEM entity nested within a PROC entity for a specific route of administration), this 6.06–8.90% annotation loss and document fragmentation is a systematic measurement error affecting the most deployment-relevant dataset.

#### MINOR

**m1 — Non-French tokens in QUAERO EMEA leaflets (IF)**
Czech and German/English organizational names appear in QUAERO examples (QUAERO-D11, QUAERO-D12), reflecting multi-country regulatory leaflet appendices. This is a minor isolated issue but indicates QUAERO is not a clean French-only regulatory corpus.

**m2 — Potentially dated regulatory and clinical standards in FrenchMedMCQA (OC)**
Vaccination obligation rules (FRENCHMEDMCQA-D8) and hypertension thresholds (FRENCHMEDMCQA-D7) may reflect superseded French regulatory status. Temporal validity of exam-derived ground truth warrants review.

**m3 — DEFT2021 NER domain bias toward urology/oncology (IC)**
The sampled DEFT2021 examples cluster in urological and oncological clinical cases (DEFT2021-D8), potentially under-representing the breadth of disease categories appearing in regulatory labeling contraindications and safety warnings.

**m4 — MORFITT includes veterinary medicine content (IO)**
Several MORFITT abstracts cover canine, equine, and avian pathology (MORFITT-D11, MORFITT-D12, MORFITT-D13, MORFITT-D14) under the `veterinary` specialty label — a domain entirely outside human pharmaceutical regulatory compliance.

---

### Confirmed Properties

1. **French text-only, Latin script throughout**: All datasets except PxCorpus (transcribed speech) are written standard French in Latin script with diacritics. No cross-modality, cross-script, or dialect variation relevant to metropolitan France deployment was observed. Input Form is the lowest-concern validity dimension as documented.

2. **Genre taxonomy is clinical/research NLP, not regulatory NLP**: Content inspection across all 12 datasets confirms the benchmark YAML's characterization — clinical cases, research abstracts, clinical trial protocols, exam questions, and transcribed prescriptions are the actual genres represented. QUAERO EMEA and DEFT2020 drug-label subsets are the only partial exceptions.

3. **Drug entities appear in clinical narrative context, not regulatory labeling structure**: Drug names, dosages, and routes of administration appear in multiple datasets (QUAERO, DEFT2021, E3C, CAS, CLISTER, ESSAI, PxCorpus) but consistently in clinical or trial narrative context, not in the formulaic, section-structured format of EMA SmPCs or patient information leaflets.

4. **No French overseas territory content confirmed**: Zero examples from Martinique, Guadeloupe, French Guiana, Réunion, or Mayotte were identified across any dataset. DiaMED's Pan African Journal sourcing does not address this gap. Tropical pathology vocabulary (dengue, chikungunya, paludisme) is absent from all label sets.

5. **No regulatory affairs expertise in any annotation workflow**: Content inspection confirms benchmark YAML documentation — annotators across all datasets are clinical case reviewers, NLP researchers, medical experts, or automated systems. No dataset documentation indicates regulatory affairs specialists or pharmacovigilance officers were involved in annotation.

6. **Best deployment-relevant NER label subset**: DEFT2021's DOSAGE, SUBSTANCE, TREATMENT, FREQUENCY, MODE classes and PxCorpus's drug/dose/mode NER scheme are the closest available approximations to regulatory posology entity typing, but both are calibrated to clinical narrative and spoken prescription contexts respectively — not to EMA SmPC section-structured posology templates.

---

### Content Coverage Summary

**What is collectively represented:** The benchmark assembles strong coverage of French clinical case NLP (CAS, DEFT2021, E3C, DiaMED, CLISTER), research literature NER (QUAERO MEDLINE, MANTRAGSC Medline, MORFITT), clinical trial protocol processing (ESSAI), pharmacy-domain QA (FrenchMedMCQA), drug-prescription spoken NLU (PxCorpus), and mixed-genre STS (DEFT2020). Task type diversity across POS, NER, STS, classification, and MCQA is genuine and broad.

**What gaps remain relative to the deployment:** The benchmark has no tasks or datasets derived from: (1) current-format EMA SmPCs/RCPs (QRD v10.4); (2) patient information leaflets formatted to EMA PIL template; (3) CTD modules or ANSM-format national authorization dossiers; (4) pharmacovigilance periodic safety update reports (PSURs); (5) France-specific packaging regulatory requirements (blue-box, CIP codes, Feuille de style); (6) MedDRA-coded adverse effect terminology (required for SmPC section 4.8); (7) regulatory entity types: INNs as a distinct class, ATC codes, excipient nomenclature by EPC/INCI standards, contraindication qualifiers, EMA SmPC section structural markers. The closest existing comparable resource is the Italian DART corpus (2024) — no French-language regulatory SmPC NLP corpus was identified in the literature.

The benchmark is, in sum, well-suited for evaluating French biomedical language understanding in clinical and research NLP — which is its stated purpose — but the deployment context requires regulatory document NLP, a meaningfully distinct sub-domain for which DrBenchmark provides only incidental and partial coverage through QUAERO EMEA and DEFT2020 drug-label subsets.

---

### Limitations

1. **MANTRAGSC `fr_emea` configuration not inspected**: The analyzed MANTRAGSC sample appears to be entirely `fr_medline`. The `fr_emea` configuration (EMEA drug labels) may be more deployment-relevant but was not represented in the analyzed examples — its fit assessment here is therefore incomplete and warrants separate inspection.

2. **FrenchMedMCQA Task 2 not analyzed**: The count-of-correct-answers sub-task was not separately examined for any additional deployment-relevant content patterns.

3. **DEFT2021 classification config not sampled**: Only the NER config of DEFT2021 was inspected; the 23 MeSH Chapter C multi-label classification config was not directly sampled, limiting assessment of that task's alignment.

4. **CAS negation/speculation NER configs not sampled**: Only the `pos` config was inspected; the `ner_neg`, `ner_spec`, and `cls` configs — which may be more deployment-relevant — were not represented in the analyzed examples.

5. **Exam answer key provenance for FrenchMedMCQA**: The temporal provenance of exam questions is unknown; questions may span multiple exam years, and the currency of ground-truth answers for regulatory/clinical standards that have changed since question creation cannot be assessed without access to exam metadata.

6. **Annotation quality for inherited datasets**: IAA statistics for QUAERO, MANTRAGSC, E3C, and MORFITT are inherited from original source papers with varying methodologies; they were not re-assessed for DrBenchmark. Cross-dataset IAA comparison is unreliable per independent 2024 evaluation (HAL 04523267).

7. **QUAERO MEDLINE config not sampled**: Only the EMEA config was analyzed; the MEDLINE config (biomedical article titles) was not inspected and would likely show even weaker deployment fit.

8. **No access to ANSM-specific circular documentation**: Whether France-specific national requirements (blue-box, Feuille de style, List I/II classification) introduce vocabulary patterns that would appear in any benchmark dataset cannot be assessed from public corpus inspection alone.

---

### Cited Evidence

- **QUAERO-D1**: Example 1 (CHEM): Excipient list in SmPC section 6 format — confirms regulatory genre alignment.
- **QUAERO-D2**: Example 55: Natalizumab concentration/dose disclosure — posology content present.
- **QUAERO-D3**: Example 95: "code ATC" in text — ATC codes textually present but not annotated as entities.
- **QUAERO-D4**: Example 95: ATC code unlabeled — regulatory entity taxonomy gap.
- **QUAERO-D5**: Example 34: Excipients tagged as CHEM — no INN/excipient distinction.
- **QUAERO-D6**: Example 50: INN and excipients share same CHEM label — regulatory sub-type gap.
- **QUAERO-D7**: Example 36: Header fragment in sentence — splitting artifact.
- **QUAERO-D8**: Example 84: Isolated "EMEA/H/C/122 4." — null-content splitting artifact.
- **QUAERO-D9**: Example 98: Empty tokens/tags — null sentence from splitting.
- **QUAERO-D10**: Example 107: Excessively long mixed-content token sequence — inconsistent splitting.
- **QUAERO-D11**: Example 15: Czech-language tokens in dataset — non-French content.
- **QUAERO-D12**: Example 121: German/English organization names — minor language mixing.
- **QUAERO-D13**: Example 129: Posology sentence — relevant content present.
- **QUAERO-D14**: Example 78: Dose threshold sentence — relevant but unannotated as posology entity.
- **QUAERO-D15**: Example 64: Long contraindication passage — contraindication qualifier entities absent from scheme.
- **QUAERO-D16**: Example 23: Pediatric exclusion sentence — population qualifier not captured as distinct entity type.
- **FRENCHMEDMCQA-D1**: Example 105 | simple/1 | IC, IO | Only instance of SmPC-adjacent regulatory terminology ("résumé des caractéristiques du produit")
- **FRENCHMEDMCQA-D2**: Example 70 | multiple/1 | IC | Brand name (DAKTARIN®) in answer option; clinical register, not regulatory normative prose
- **FRENCHMEDMCQA-D5**: Example 6 | simple/1 | IC | Drug names as exam answer options, not as labeled regulatory entities
- **FRENCHMEDMCQA-D6**: Example 50 | multiple/1 | IC | Pharmaceutical container classification as exam knowledge, not regulatory artifact
- **FRENCHMEDMCQA-D7**: Example 20 | multiple/4 | OC | Potentially dated WHO hypertension thresholds — temporal validity concern
- **FRENCHMEDMCQA-D8**: Example 94 | multiple/1 | OC | Hepatitis B vaccination obligation — may reflect superseded French regulatory status
- **FRENCHMEDMCQA-D9**: Example 105 | simple/1 | OC | Definitional exam question about regulatory concept; ground truth is licensure fact, not compliance judgment
- **DEFT2020-D1**: 4 | IC, IO | Breastfeeding contraindication drug label
- **DEFT2020-D2**: 18 | IC, IO | Excipient contraindication drug label
- **DEFT2020-D3**: 16 | OO, OC | Safety warning with time-threshold
- **DEFT2020-D4**: 52 | IC | Pharmaceutical form description
- **DEFT2020-D5**: 121 | IC | Storage instruction
- **DEFT2020-D6**: 6 | IO, IC | Apiculture content, irrelevant genre
- **DEFT2020-D7**: 60 | IO, IC | Sports content
- **DEFT2020-D8**: 76 | IO, IC | WWII military content
- **DEFT2020-D9**: 1 | IO, IC | Railway infrastructure content
- **DEFT2020-D10**: 13 | OO, OC | Missing "stricte surveillance médicale" scored 3.6
- **DEFT2020-D11**: 30 | OO, OC | Missing mechanistic qualifier scored 3.8
- **DEFT2020-D12**: 130 | OO, OC | Alcohol qualifier added, scored 3.8
- **DEFT2020-D13**: 127 | OO | Contradictory sterilization statements scored 0.4
- **DEFT2020-D14**: 4 | OC | Annotator spread [5,2,4,4,5] on breastfeeding pair
- **DEFT2020-D15**: 16 | OC | Annotator spread [5,2,4,4,5] on drug safety pair
- **DEFT2020-D16**: 46 | OC | Annotator spread [5,2,0,3,1] on historical pair
- **DEFT2020-D17**: 109 | OC | Annotator spread [5,4,0,3,0] on clinical pair
- **DEFT2020-D18**: 46 | OO | moy=2.2 vs vote=5.0 discrepancy
- **DEFT2020-D19**: 109 | OO | moy=2.4 vs vote=0.0 discrepancy
- **DEFT2020-D20**: 82 | OO | moy=2.7 vs vote=4.0 discrepancy
- **DEFT2020-D21**: 45 | IC | Health education research, not regulatory
- **DEFT2020-D22**: 26 | IC | Anaesthesia trial abstract
- **MORFITT-D1**: Ex. 1 | 9 | Scientific literature genre, not regulatory
- **MORFITT-D2**: Ex. 19 | 7 | Closest regulatory-adjacent but still research abstract
- **MORFITT-D3**: Ex. 33 | 10,7 | Cosmetic formulation research, not patient leaflet
- **MORFITT-D4**: Ex. 8 | 0 | Canadian geographic provenance
- **MORFITT-D5**: Ex. 10 | 3 | Quebec, Canada provenance
- **MORFITT-D6**: Ex. 20 | 1 | Jordanian patient population
- **MORFITT-D7**: Ex. 22 | 11 | Egyptian student population
- **MORFITT-D8**: Ex. 31 | 11 | Saudi Arabian internship context
- **MORFITT-D9**: Ex. 32 | 0 | Japanese epidemiology data
- **MORFITT-D10**: Ex. 26 | 6,8,5 | Chinese parasitology
- **MORFITT-D11**: Ex. 9 | 6,0,8 | Canine otitis/veterinary
- **MORFITT-D12**: Ex. 28 | 3,8 | Veterinary EEG study
- **MORFITT-D13**: Ex. 29 | 8 | Small animal dermatology
- **MORFITT-D14**: Ex. 5 | 6,8 | Equine pulmonary physiology
- **MORFITT-D15**: Ex. 17 | 2 | Chikungunya/overseas territory relevance
- **MORFITT-D16**: Ex. 6 | 6,8,2 | Translated content, register concern
- **MORFITT-D17**: Ex. 5 | 6,8 | Translated content, register concern
- **CLISTER-D1**: 1 | 0.0 | IO, IC
- **CLISTER-D2**: 6 | 0.0 | IO, IC
- **CLISTER-D3**: 222 | 0.0 | IO, IC
- **CLISTER-D4**: 41 | 2.0 | IC
- **CLISTER-D5**: 116 | 1.0 | IC
- **CLISTER-D6**: 98 | 2.0 | IC
- **CLISTER-D7**: 164 | 2.0 | IC
- **CLISTER-D8**: 188 | 4.0 | OO
- **CLISTER-D9**: 123 | 3.75 | OO
- **CLISTER-D10**: 125 | 4.0 | OO
- **CLISTER-D11**: 8 | 1.0 | OO
- **CLISTER-D12**: 8 + 123 | 1.0/3.75 | OC
- **CLISTER-D13**: 163 | 5.0 | OC
- **CLISTER-D14**: 61 | 0.0 | IC, OF
- **CLISTER-D15**: 131 | 4.0 | IC, OF
- **CLISTER-D16**: 8 | 1.0 | IC, OF
- **MANTRAGSC-D1**: Ex. 1 | DISO | MEDLINE case-report title; not regulatory prose
- **MANTRAGSC-D2**: Ex. 36 | CHEM/DISO | Drug name in clinical title, no posology context
- **MANTRAGSC-D3**: Ex. 41 | GEOG/DISO | Sub-Saharan African context, non-regulatory
- **MANTRAGSC-D4**: Ex. 43 | DISO | Senegalese case series, non-metropolitan
- **MANTRAGSC-D5**: Ex. 7 | O | 3-token title, no NER value
- **MANTRAGSC-D6**: Ex. 34 | O | 2-token title
- **MANTRAGSC-D7**: Ex. 57 | O | Administrative title, no regulatory content
- **MANTRAGSC-D8**: Ex. 36 | CHEM | INN labeled coarsely as chemical
- **MANTRAGSC-D9**: Ex. 45 | CHEM/PHYS | Hormones labeled without posology context
- **MANTRAGSC-D10**: Ex. 18 | DEVI | Medical device, no excipient/regulatory context
- **MANTRAGSC-D11**: Ex. 43 | DISO | Dakar case series
- **MANTRAGSC-D12**: Ex. 41 | GEOG | Cameroonian epidemic
- **MANTRAGSC-D13**: Ex. 22 | DISO | Veterinary pathology
- **MANTRAGSC-D14**: Ex. 50 | CHEM | Vague pharmaceutical reference, ambiguous regulatory status
- **E3C-D1**: Ex. 1 | French clinical prose, well-formed, text-only
- **E3C-D2**: Ex. 59 | Drug in clinical narrative, not regulatory template
- **E3C-D3**: Ex. 62 | Medication dosage in clinical context
- **E3C-D4**: Ex. 79 | Drug names/doses systematically unlabeled
- **E3C-D5**: Ex. 53 | Antibiotics tagged O
- **E3C-D6**: Ex. 103 | Anesthetic agents with doses tagged O
- **E3C-D7**: Ex. 39 | Immunosuppressants tagged O
- **E3C-D8**: Ex. 70 | Patient from Morocco
- **E3C-D9**: Ex. 90 | Explicit sub-Saharan Africa reference
- **E3C-D10**: Ex. 5 | Tokenization artifact (escaped newline)
- **E3C-D11**: Ex. 1 | Backtick artifact from preprocessing
- **E3C-D12**: Ex. 20 | Pathology-focused CLINENTITY labels confirmed
- **E3C-D13**: Ex. 95 | Morphological finding labeling pattern
- **E3C-D14**: Ex. 53 | Multi-token entity boundary labeling
- **PXCORPUS-D1**: Ex. 75 | medical_prescription | IF, IC | INFO
- **PXCORPUS-D2**: Ex. 88 | none | IF, IC | MAJOR
- **PXCORPUS-D3**: Ex. 207 | medical_prescription | IF, IC | MAJOR
- **PXCORPUS-D4**: Ex. 10 | negate | IF | MINOR
- **PXCORPUS-D5**: Ex. 3 | none | IF | MINOR
- **PXCORPUS-D6**: Ex. 5 | medical_prescription | IC, OO | INFO
- **PXCORPUS-D7**: Ex. 41 | medical_prescription | IC | INFO
- **PXCORPUS-D8**: Ex. 166 | medical_prescription | IC | INFO
- **PXCORPUS-D9**: Ex. 21 | none | IO, IC | MAJOR
- **PXCORPUS-D10**: Ex. 18 | none | IO, IC | MAJOR
- **PXCORPUS-D11**: Ex. 76 | none | IO, IC | MAJOR
- **PXCORPUS-D12**: Ex. 4 | replace | OO | MINOR
- **PXCORPUS-D13**: Ex. 12 | replace | OO | MINOR
- **PXCORPUS-D14**: Ex. 103 | medical_prescription | OO | MINOR
- **PXCORPUS-D15**: Ex. 22 | medical_prescription | OO | MINOR
- **PXCORPUS-D16**: Ex. 169 | medical_prescription | IF | CRITICAL
- **PXCORPUS-D17**: Ex. 197 | medical_prescription | IF | CRITICAL
- **PXCORPUS-D18**: Ex. 84 | none | IF | CRITICAL
- **DIAMED-D1**: Example 1 (label=A00-B99): "Maladie de Kaposi à localisation broncho-pulmonaire révélant une infection VIH" — clinical narrative genre; drug mentions as prose; sub-Saharan African disease profile.
- **DIAMED-D2**: Example 8 (label=H60-H95): "amphotéricine B par voie intraveineuse...relais par l'itraconazole" — posology as clinical prose, not regulatory labeling format.
- **DIAMED-D3**: Example 3 (label=D50-D89): keyword "Maroc" — Morocco-based clinical case; non-metropolitan-France provenance.
- **DIAMED-D4**: Example 4 (label=E00-E89): Piebaldisme case — rare pigmentary anomaly; no regulatory labeling content.
- **DIAMED-D5**: Example 5 (label=F01-F99): Pathomimie case with psychiatric and dermatological features — multi-system ambiguity for ICD-10 chapter assignment.
- **DIAMED-D6**: Example 6 (label=G00-G99): Spinal compression case from unspecified African setting — clinical narrative genre confirmed.
- **DIAMED-D7**: Example 7 (label=H00-H59): Adie pupil case — brief clinical report; no regulatory content.
- **DIAMED-D8**: Example 8 (label=H60-H95): Otitis externa maligne — Candida albicans — clinical case with treatment narrative.
- **DIAMED-D9**: Example 9 (label=I00-I99): "CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" — explicit sub-Saharan African institutional origin.
- **DIAMED-D10**: Example 10 (label=J00-J99): Abducens nerve palsy/pansinusitis — clinical case; respiratory/ENT context.
- **DIAMED-D11**: Example 11 (label=K00-K95): Acute gastric dilatation — two cases including one occurring during Ramadan fast; cultural/geographic context outside metropolitan France.
- **DIAMED-D12**: Example 12 (label=L00-L99): keyword "Niamey"; drug toxidermie case — Niger clinical setting; drug names (Phénobarbital, Halopéridol) in narrative prose.
- **DIAMED-D13**: Example 13 (label=M00-M99): Osteochondritis dissecans in adolescent — musculoskeletal clinical case; no regulatory content.
- **DIAMED-D14**: Example 14 (label=N00-N99): Breast fibromatosis labeled N00-N99 — potential ICD-10 boundary ambiguity between genitourinary and neoplasm chapters.
- **DEFT2021-D1**: id=946 | Clinical case surgical narrative; no regulatory genre
- **DEFT2021-D2**: id=140 | Dense chemotherapy dosage annotation; clinical, not regulatory
- **DEFT2021-D3**: id=1450 | Madagascar travel reference; geographic scope note
- **DEFT2021-D4**: id=179 | Drug/dose entities in clinical observation note, not SmPC
- **DEFT2021-D5**: id=546 | Antibiotic drugs as TREATMENT; clinical, not INN/ATC
- **DEFT2021-D6**: id=146 | Topical drug with concentration; clinical prescription, not SmPC
- **DEFT2021-D7**: id=2708 | Vaccination as TREATMENT; non-regulatory
- **DEFT2021-D8**: id=1087 | Detailed urothelial carcinoma; urology bias
- **DEFT2021-D9**: id=1127 | Scleroderma case; rare non-urology example
- **DEFT2021-D10**: id=22 | Morphine dosage in clinical error narrative
- **DEFT2021-D11**: id=20 | Morphine injection dose; clinical protocol, not regulatory
- **DEFT2021-D12**: id=2577 | Africa residence in patient history
- **DEFT2021-D13**: id=1766 | Single-token SOSY annotation
- **DEFT2021-D14**: id=2931 | Punctuation-only sentence fragment
- **CAS-D1**: Example 1: "l'examen clinique montre un état général conservé" — canonical clinical examination prose confirming genre.
- **CAS-D2**: Example 2: pos_tags = [3, 8, 23, 9, ...] — POS integer labels only, no entity/similarity labels.
- **CAS-D5**: Example 5: "un homme de 48 ans…rectorragies dues à des polypes du rectum traités par électrocoagulation" — clinical case narrative structure.
- **CAS-D15**: Example 15: "soins dentaire informels et de points de feux" — possible non-metropolitan context.
- **CAS-D22**: Example 22: "administration d'une ampoule de digoxine en intraveineuse" — drug in narrative, not regulatory format.
- **CAS-D33**: Example 33: "cyclophosphamide, vincristine et prednisone" — chemotherapy listed in case narrative protocol.
- **CAS-D34**: Example 34: "le Betnésol® lavement était progressivement arrêté" — branded drug with trademark, no regulatory structure.
- **CAS-D44**: Example 44: "exposition à l'eau de la rivière" — environmental exposure scenario.
- **CAS-D63**: Example 63: "Proctocort® (hydrocortisone acétate 90 mg : 1 lavement tous les soirs)" — closest instance to posology expression, still narrative-embedded.
- **CAS-D103**: Example 103: Dense AST/ALT/bilirubine lab table — complex clinical notation tokenized as POS sequence.
- **ESSAI-D1**: Ex. 1 | Oncology clinical trial domain confirmed
- **ESSAI-D2**: Ex. 3 | Randomization/trial arm language
- **ESSAI-D3**: Ex. 40 | "contre-indication" in eligibility criterion, not labeling
- **ESSAI-D4**: Ex. 25 | Patient-directed register, not SmPC/leaflet
- **ESSAI-D5**: Ex. 26 | Patient follow-up language
- **ESSAI-D6**: Ex. 33 | Institution-specific (Gustave Roussy)
- **ESSAI-D7**: Ex. 71 | "autorisation de mise sur le marché" incidental mention
- **ESSAI-D8**: Ex. 2 | Experimental drug code (MEDI9197)
- **ESSAI-D9**: Ex. 42 | Alphanumeric drug code (BMS-986179)
- **ESSAI-D10**: Ex. 37 | Approved drugs in trial arm context
- **ESSAI-D11**: Ex. 40 | Negation of contraindication as eligibility criterion
- **ESSAI-D12**: Ex. 5 | Dose optimization objective (trial context)
- **ESSAI-D13**: Ex. 48 | Posology in trial schedule
- **ESSAI-D14**: Ex. 46 | Integer POS tags, 36-class ESSAI-specific scheme
- **ESSAI-D15**: Ex. 75 | Possible transcription artifact ("set" for "est")


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
  "benchmark": "drbenchmark",
  "region": "French Pharmaceutical Regulatory NLP — DrBenchmark Assessment",
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
