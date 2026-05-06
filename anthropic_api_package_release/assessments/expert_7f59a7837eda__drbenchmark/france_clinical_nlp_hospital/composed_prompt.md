I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Domain** is valid for use in **French Hospital Clinical NLP — Metropolitan France (DrBenchmark)**.

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
- **Full Name**: DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Domain
- **Domain**: French biomedical NLP evaluation
- **Languages**: fr
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
DrBenchmark covers 20 downstream tasks spanning POS tagging, NER, multi-class
classification, multi-label classification, intent classification, MCQA, and STS [Q1, Q4, Q18].
The benchmark explicitly includes both classical tasks (NER, POS tagging) and more
challenging tasks (MCQA, multi-label classification) [Q20], and aggregated performance
is reported across five designated categories: POS, NER, MCQA, MCC, MLC, and STS [Q81].
Comparative framing against BLURB (13 tasks) [Q13], BLUE (10 tasks) [Q14], and CBLUE
(8 tasks) [Q15] establishes the breadth of the taxonomy. Individual tasks map to distinct
clinical functions: FrenchMedMCQA addresses pharmacy exam QA [Q39], PxCorpus covers
intent classification and NER for drug prescription transcripts [Q44], and DEFT-2021
provides multi-label clinical profile classification [Q26]. However, the benchmark is
designed around metropolitan French academic and clinical sources; the paper does not
document any task category or subcategory targeting tropical or overseas-territory
pathologies. The DiaMed dataset draws from the Pan African Medical Journal [Q45], but
its tropical pathology scope and relevance to French DOM-TOM pathology profiles is
not articulated. The absence of documentation on this gap is the primary ontological
concern, rather than confirmed misalignment within Metropolitan France.

### Input Content
Data origins are explicitly diverse: scientific literature, clinical trials, clinical cases,
and speech transcriptions [Q19]. Individual datasets are sourced from well-characterized
corpora: QUAERO draws from EMEA drug leaflets and MEDLINE biomedical titles [Q33, Q34];
E3C provides multilingual clinical cases with the French subset retained [Q29, Q31];
CAS provides 3,790 clinical cases [Q42]; ESSAI contains clinical trial protocols [Q43];
MorFITT draws from PMC Open Access biomedical abstracts [Q38]; Mantra-GSC covers
biomedical abstracts, drug labels, and patents [Q40]; DEFT-2021 draws from a French
text mining competition corpus [Q24]; and PxCorpus provides spoken drug prescription
recordings [Q44]. All sources appear to originate from metropolitan French academic,
clinical, or regulatory settings. The one newly created dataset, DiaMed, was collected
from the Pan African Medical Journal [Q45], introducing some non-metropolitan signal,
but its scope relative to French overseas-territory pathology profiles is undocumented.
Critically, the benchmark's clinical case sources are published or edited write-ups and
competition corpora rather than raw active-hospital EHR notes. The paper acknowledges
the presence of clinical shorthand in PxCorpus transcripts [Q44] but does not address
the register gap between edited academic case write-ups and the moderately noisy,
shorthand-laden hospital documentation the deployment processes [Q43, Q19]. Licensing
for all constituent datasets remains unchanged from original sources [Q96], and vocabulary
differences across evaluated models reflect the variation in pre-training data [Q76],
indirectly confirming that no single unified corpus underlies the benchmark.

### Input Form
DrBenchmark is exclusively text-based in standard written French [Q31, Q48], implemented
via HuggingFace Datasets, Transformers, and PyTorch [Q48]. The Latin alphabet with
diacritics aligns natively with all target language variants. Tokenization behavior
is investigated through average sub-token counts per word across eight MLMs [Q75, Q89, Q90],
and data-efficiency experiments vary training proportions to probe robustness [Q68].
For QUAERO documents exceeding standard model sequence length limits, documents were
split at the sentence boundary [Q37]. The exclusively text-based, standard-French
written register of the benchmark is well matched to the deployment's text-only clinical
NLP pipeline. No modality mismatch or script incompatibility concerns apply. The register
mismatch between edited clinical case write-ups and active-hospital notes is addressed
under Input Content rather than Input Form, as it reflects data source selection rather
than signal encoding.

### Output Ontology
Label ontologies across DrBenchmark's tasks are rich and domain-specific. POS tagging
uses 31 tags for CAS [Q101] and 36 tags for ESSAI [Q102]. NER label sets include
QUAERO's 10 UMLS Semantic Group categories [Q103], E3C's clinical entity and temporal
labels [Q104], Mantra-GSC's Medline (11 classes) and EMEA/Patents (10 classes) schemes
[Q106], and DEFT-2021's 14 entity types covering anatomy, pathology, temporal markers,
treatment, and dosage [Q108]. Multi-label classification in DEFT-2021 uses 23 MeSH axes
from Chapter C [Q27], and DiaMed maps to 22 ICD-10 chapter-level categories [Q45, Q107].
MorFITT covers 12 medical specialty labels [Q105]. The ICD-10 chapter-level granularity
of DiaMed and the MeSH-axis structure of DEFT-2021 provide ontological alignment with
the deployment's ICD-10/PMSI mapping function, but at a coarser level than granular
PMSI codes. Crucially, scoring across classification tasks uses majority-class baselines
and standard classification metrics [Q56], and the benchmark does not document any
output taxonomy entry for confidence-scored candidate lists, ranked-label outputs, or
uncertainty flagging — the multi-label-with-confidence behavior that is structurally
central to the deployment [Q82, Q87]. The finding that even specialized models perform
poorly on MLC and STS tasks [Q82, Q86] directly implicates the deployment's multi-label
pathology classification function but does not resolve the structural mismatch in output
decision rules.

### Output Content
Annotation practices vary substantially across the 20 constituent datasets. DEFT-2021
is manually annotated for both multi-label classification and NER [Q25], but annotator
identity and clinical expertise are not described. CLISTER was annotated by multiple
annotators who assigned similarity scores averaged into a floating-point value [Q41].
The CAS corpus uses automatic POS annotations via Tagex, validated against manual
annotations at 98% precision [Q42] — meaning at least one benchmark task rests on
automatic rather than expert-human labels. DiaMed is the only dataset for which explicit
inter-annotator agreement statistics and clinical expert involvement are documented: it
was annotated by several annotators including one medical expert, with Cohen's Kappa
and Gwet's AC1 computed across two sessions of 15 clinical cases each [Q45, Q46].
The deployer explicitly frames the system as a "Silver Standard" tool whose ICD-10
mappings may not align with specific hospital coding conventions, and identifies the
gap between academic NLP annotators and practicing hospital coding specialists as a
primary concern. No DrBenchmark dataset documents annotator involvement from PMSI
coders, hospital clinicians, or medical coders — only a single medical expert is
mentioned for DiaMed [Q45]. The heterogeneity of annotation authority across 20 source
datasets means that label validity varies considerably, and for the majority of tasks
the annotation provenance does not reflect hospital coding specialist judgment.

### Output Form
All 20 tasks are scored under a strict unified fine-tuning protocol with results averaged
over four runs and statistical significance assessed via Student's t-test [Q51].
Sequence labeling tasks use SeqEval with IOB2 format, with labels predicted only on the
first token of each word — a tokenizer-agnostic approach [Q52, Q53]. STS tasks report
Spearman correlation and EDRM [Q54]. Classification tasks use majority-class baselines [Q56].
Hyperparameters are documented in an appendix for reproducibility [Q49, Q99, Q100], and
data-efficiency experiments report per-configuration results over four runs [Q69, Q70].
The benchmark's evaluation protocol does not include confidence calibration metrics,
uncertainty flagging, or ranked-candidate list quality assessment. The deployment's
multi-label-with-confidence behavior — where high-uncertainty entities are flagged for
manual review — is not directly measurable within the benchmark's current scoring
framework [Q82, Q87]. The output form is otherwise well matched to the deployment:
text classification and sequence labeling outputs are the natural evaluation targets
for the deployment's NER, POS, and ICD-10 mapping functions.


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
| Q21 | 3 | input_ontology | "DEFT-2020 (Cardon et al., 2020) contains clinical cases, encyclopedia and drug labels introduced in the 2020 edition of an annual French Text Mining Challenge, called DEFT, and annotated for two tasks: (i) textual similarity and (ii) multi-class classification." |
| Q22 | 3 | output_ontology | "The first task aims at identifying the degree of similarity within pairs of sentences, from 0 (the less similar) to 5 (the most similar)." |
| Q23 | 3 | output_ontology | "The second task consists in identifying, for a given sentence, the most similar sentence among three sentences provided." |
| Q24 | 3 | input_content | "DEFT-2021 (Grouin et al., 2021) is a subset of 275 clinical cases taken from the 2019 edition of DEFT." |
| Q25 | 3 | output_content | "This dataset is manually annotated in two tasks: (i) multi-label classification and (ii) NER." |
| Q26 | 3 | input_ontology | "The multi-label classification task focuses on identifying the patient's clinical profile based on the diseases, signs, or symptoms mentioned in the clinical cases." |
| Q27 | 3 | output_ontology | "The dataset is annotated with 23 axes from Chapter C of the Medical Subject Headings (MeSH)." |
| Q28 | 3 | input_ontology | "The second task involves fine-grained information extraction for 13 types of entities (more detail in Appendix B.7)." |
| Q29 | 3 | input_content | "E3C (Magnini et al., 2020) is a multilingual dataset of clinical cases annotated for the NER task." |
| Q30 | 3 | output_ontology | "It consists of two types of annotations (more detail in Appendix B.4): (i) clinical entities (e.g., pathologies), (ii) temporal information and factuality (e.g., events)." |
| Q31 | 3 | input_form | "While the dataset covers 5 languages, only the French portion is retained for the benchmark." |
| Q32 | 3 | input_form | "Since the dataset does not come with pre-defined subsets, we performed a 70 / 10 / 20 random split, as described in Table 3." |
| Q33 | 3 | input_content | "The QUAERO French Medical Corpus (Névéol et al., 2014), simply referred to as QUAERO in this paper, contains annotated entities and concepts for NER tasks." |
| Q34 | 3 | input_content | "The dataset covers two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE." |
| Q35 | 3 | output_ontology | "10 entity categories corresponding to the UMLS Semantic Groups (Lindberg et al., 1993) were annotated (more detail in Appendix B.3)." |
| Q36 | 3 | output_ontology | "In total, 26,409 entity annotations were mapped to 5,797 unique UMLS concepts." |
| Q37 | 3 | input_form | "Due to the presence of nested entities in annotations, we simplified the evaluation process by retaining only annotations at the higher granularity level from the BigBio (Fries et al., 2022) implementation, following the approach described in Touchent et al. (2023), which translates into an average loss of 6.06% of the annotations on EMEA and 8.90% on MEDLINE. Additionally, considering that some documents from EMEA exceed the maximum input sequence length that most current language models can handle, we decided to split these documents into sentences." |
| Q38 | 4 | input_content | "MorFITT (Labrak et al., 2023) is a multi-label dataset annotated with medical specialties. It contains 3,624 biomedical abstracts from PMC Open Access. It has been annotated across 12 medical specialties (more detail in Appendix B.5), for a total of 5,116 annotations." |
| Q39 | 4 | input_ontology | "FrenchMedMCQA (Labrak et al., 2022) is a Multiple-Choice Question-Answering (MCQA) dataset for biomedical domain. It contains 3,105 questions coming from real exams of the French medical specialization diploma in pharmacy, integrating single and multiple answers. The first task consists of automatically identifying the set of correct answers among the 5 proposed for a given question. The second task consists of identifying the number of answers (between 1 and 5) supposedly correct for a given question." |
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
| Q58 | 6 | output_ontology | "Interestingly, most of the models examined manage to secure the top position in at least one of the French biomedical downstream tasks studied." |
| Q59 | 6 | output_form | "The only exception pertains to the cross-lingual generalist model (XLM-RoBERTa), which manages to reach the second-best position on several tasks." |
| Q60 | 6 | output_content | "French biomedical language models (DrBERT-FS, DrBERT-CP, CamemBERT-bio), presumed to be the most aligned with the nature of the data of the benchmark, exhibit indeed superior performance across many tasks." |
| Q61 | 6 | output_form | "More precisely, DrBERT-FS achieves the highest performance in 8 tasks, DrBERT-CP in 5 tasks, and CamemBERT-bio in 2 tasks." |
| Q62 | 6 | output_form | "This indicates that domain and language-specialized models achieve the best performance in up to 75% of the DrBenchmark downstream tasks." |
| Q63 | 6 | output_ontology | "Generalist models (CamemBERT, CamemBERTa, FlauBERT and XLM-RoBERTa) are more suitable for tasks that require extensive linguistic knowledge but may not perform as well as specialized models nor even reach their level of performance." |
| Q64 | 6 | output_form | "We observe that all generalist models obtain better performance only on 4 out of the 20 tasks, but still remain competitive on most tasks." |
| Q65 | 6 | input_content | "Furthermore, our experiments with DrBERT-FS indicate that biomedical models may require less pre-training data compared to generalist ones." |
| Q66 | 6 | input_content | "However, it is important to note that this observation requires further confirmation." |
| Q67 | 6 | input_content | "In some tasks, biomedical models that undergo continual pre-training from a generalist model, such as CamemBERT-bio, can prove to be the most effective, underscoring the value of pre-training on generalist data." |
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
| Q78 | 8 | input_form | "However, our experiments, as shown in Table 7, reveal that FlauBERT is the model with the least word segmentation (1.43 in average), while DrBERT-CP tends to have the highest average segmentation (1.90 in average)." |
| Q79 | 8 | input_form | "Surprisingly, when comparing the performance of these two models on the benchmark tasks, we observe that DrBERT-CP outperforms FlauBERT on 16 out of the 20 tasks, thus contradicting previous conclusions drawn by the community." |
| Q80 | 8 | input_form | "Yet, tokenization, as it is currently done in MLMs, seems to play a minor role in the performance of systems." |
| Q81 | 8 | input_ontology | "Table 8 summarizes the results obtained on average by the considered MLMs when aggregating the tasks into one of the five designated categories: POS, NER, MCQA, MCC (Multi-class classification), MLC (Multi-label classification), or STS tasks." |
| Q82 | 8 | output_ontology | "Upon analyzing the average performance by task category, it becomes evident that the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS." |
| Q83 | 9 | input_ontology | "In this paper, we introduced DrBenchmark, the first large language understanding benchmark tailored for the French biomedical domain." |
| Q84 | 9 | input_ontology | "We conducted a qualitative evaluation of 8 state-of-the-art masked language models (MLMs) on this comprehensive benchmark, encompassing 20 diverse downstream tasks." |
| Q85 | 9 | output_ontology | "Our findings illuminate the limitations of generalist models in tackling complex biomedical tasks, emphasizing the importance of employing domain-specific models to achieve peak performance." |
| Q86 | 9 | output_ontology | "We have observed that several biomedical tasks in DrBenchmark exhibit relatively poor performance, even when utilizing specialized biomedical models." |
| Q87 | 9 | output_ontology | "We postulate that the models examined in this study, here state-of-the-art MLMs, may not be the most effective choices for specific tasks such as question-answering or multi-label classification." |
| Q88 | 9 | output_form | "The quantitative study we conducted on the PLMs requires further in-depth analysis to comprehend the impact of different parameters." |
| Q89 | 9 | input_form | "Firstly, we investigated the influence of tokenizers based on the average number of sub-tokens they produce per word." |
| Q90 | 9 | input_form | "Various tokenization algorithms are employed, depending on the model under examination." |
| Q91 | 9 | input_content | "The size of the data has not been thoroughly investigated, particularly the significance of the pre-training data size, especially specialized data in the biomedical field." |
| Q92 | 9 | output_form | "Although the benchmark is easily reproducible and customizable, it required a substantial amount of computational power to execute all runs." |
| Q93 | 9 | output_form | "We utilized approximately 2,500 hours on V100 GPUs from the Jean-Zay supercomputer to complete the quantitative study." |
| Q94 | 9 | output_form | "According to the Jean Zay supercomputer documentation, the total environmental cost is estimated to be equivalent to 647,500 Wh or 36.9 kgCO2eq/kWh, based on the carbon intensity of the energy grid mentioned in the BLOOM environmental cost study conducted on Jean Zay (Luccioni et al., 2022)." |
| Q95 | 9 | output_form | "All code for DrBenchmark is released under the MIT License." |
| Q96 | 9 | input_content | "The licensing for all datasets remains unchanged from the original sources, and DrBenchmark has no intention of redistributing these datasets." |
| Q97 | 9 | output_form | "This work was performed using HPC resources from GENCI-IDRIS (Grant 2022-AD011013061R1 and 2022-AD011013715) and from CCIPL (Centre de Calcul Intensif des Pays de la Loire)." |
| Q98 | 9 | output_form | "This work was financially supported by ANR MALADES (ANR-23-IAS1-0005), ANR AIBy4 (ANR-20-THIA-0011) and Zenidoc." |
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
name: French Hospital Clinical NLP — Metropolitan France (DrBenchmark)
abbreviation: fr_hospital_clinical_nlp
deployment_context:
  system_function: Unstructured French clinical note processing for POS tagging, NER,
    multi-label pathology classification, and temporal entity extraction. Outputs
    are mapped to ICD-10/PMSI classification axes to auto-generate patient clinical
    profiles supporting clinician care prioritization.
  decision_stakes: Life-critical. Clinicians and nursing staff act on system outputs
    for care prioritization and medical history summarization. System is explicitly
    framed as a Silver Standard support tool; final authority rests with clinicians.
  silver_standard_framing: The deployer acknowledges the system as a Silver Standard
    tool whose ICD-10 mappings may not perfectly align with hospital-specific PMSI
    coding conventions or complex multi-morbid case nuances. Clinician adjudication
    is the intended safeguard.
  output_behavior: Multi-label outputs with associated confidence scores. High-uncertainty
    entities are flagged for manual review. Ranked candidate lists support clinician
    adjudication between plausible classification axes.
primary_geography:
  country: France
  scope: Metropolitan France (mainland hospital settings)
  excluded_scopes: Belgium, Switzerland, Quebec, and French overseas territories (DOM-TOM)
    are explicitly out of scope for current deployment due to divergent terminology
    and coding standards.
  priority_extension: French overseas territories (DOM-TOM) identified as highest-priority
    future extension gap, due to distinct tropical pathology profiles absent from
    mainland training data.
languages:
  primary: French
  register: Standard medical French — formal clinical documentation register with
    moderate presence of common clinical abbreviations and shorthand. Not raw informal
    speech; not highly noisy EHR dictation.
  variants_in_scope: Metropolitan French standard medical register only. Belgian,
    Swiss, or Quebec French medical terminology variants are out of scope.
  note: The deployment language is well-matched to DrBenchmark's French-only text
    corpus. Register mismatch (edited academic sources vs. moderately noisy hospital
    notes) is a flagged gap, not a language variant gap.
writing_systems:
  scripts:
  - Latin alphabet with French diacritics (é, è, ê, ë, à, â, î, ï, ô, û, ù, ü, ç,
    œ, æ)
  note: No script mismatch or RTL concerns. Standard French Unicode character set.
    Tokenization of medical abbreviations and compound clinical terms is a domain-specific
    challenge rather than a script issue.
user_population:
  primary_users: Hospital clinicians (physicians) and nursing staff who consume system
    outputs for clinical decision support — not the patients whose notes are processed.
  secondary_users: Hospital medical coders and PMSI coding specialists who may adjudicate
    ICD-10/PMSI mappings; not directly described as system users but implicated in
    output authority questions.
  user_expertise: High domain expertise (medical professionals). Low expected tolerance
    for erroneous classifications given life-critical decision context. Clinicians
    retain final adjudication authority.
  interaction_model: Clinicians receive synthesized clinical profiles and ranked candidate
    classifications as a starting point for expert review, not as authoritative outputs.
  annotator_vs_user_gap: DrBenchmark labels were produced primarily by academic NLP
    researchers and one medical expert (DiaMed only). Deploying hospital clinicians
    and PMSI coders represent a substantially different and more operationally authoritative
    population for label validation.
patient_documentation_profile:
  documentation_type: Hospital clinical notes — unstructured free text in standard
    medical French.
  cleanliness_level: Moderately clean. Standard medical terminology predominates.
    Common clinical abbreviations and shorthand are present at moderate frequency.
  noise_sources:
  - Common clinical abbreviations
  - Standard shorthand (e.g., antécédents, traitement, prescription shortforms)
  - Occasional dictation artifacts
  - Institution-specific terminology (at some sites)
  out_of_scope_noise: Excessively noisy or institution-specific notes require additional
    pre-processing (custom glossaries, normalization modules) before reliable system
    operation.
  benchmark_register_gap: 'DrBenchmark sources are predominantly edited academic write-ups,
    competition corpora, and clinical trial protocols — a more formally written register
    than active hospital notes. CAS and PxCorpus provide partial signal but are not
    characterized as raw EHR documentation. A NeurIPS 2024 benchmark (EHRNoteQA) specifically
    designed around MIMIC-IV real discharge summaries highlights that existing clinical
    NLP benchmarks typically fail to represent the complexity of raw multi-note EHR
    documentation; no equivalent French-language raw-EHR benchmark is known to exist.
    Source: EHRNoteQA paper (NeurIPS 2024) — [WEB-1]'
clinical_coding_framework:
  primary_classification_system: ICD-10 (International Classification of Diseases,
    10th Revision)
  french_national_coding_system: PMSI (Programme de Médicalisation des Systèmes d'Information)
    — French national hospital activity coding system
  benchmark_alignment: DrBenchmark's DiaMed maps to 22 ICD-10 chapter-level categories;
    DEFT-2021 uses 23 MeSH Chapter C axes. These provide coarse ontological alignment
    but are less granular than operational PMSI codes used in French hospital billing
    and care documentation.
  coding_authority_gap: No DrBenchmark dataset documents annotation by PMSI coders
    or hospital coding specialists. Only DiaMed involves a single medical expert.
    Hospital-specific coding conventions may diverge from benchmark label definitions.
  pmsi_specifics: 'PMSI encodes diagnoses using the French national adaptation of
    ICD-10 (CIM-10 FR), with pathologies described by a principal diagnosis and optional
    secondary and associated significant diagnoses (comorbidities/complications).
    The grouping algorithm assigns stays to Groupes Homogènes de Malades (GHM) via
    Catégories Majeures (CM) which serve as the first-level classification — typically
    aligned with functional systems. Procedures are coded separately using the Classification
    Commune des Actes Médicaux (CCAM). The ATIH (Agence Technique de l''Information
    sur l''Hospitalisation) publishes the annually updated GHM classification manual
    (v2024 available); the French CIM-10 FR version is likewise maintained by ATIH.
    The benchmark''s ICD-10 chapter-level granularity is therefore substantially coarser
    than operational GHM codes, which derive from multi-field RSS (Résumé de Sortie
    Standardisé) records incorporating diagnosis codes, procedures, patient age, and
    length of stay. Source: ATIH GHM Manual 2024 — [WEB-2];
    IJE PMSI resource profile — [WEB-3]'
infrastructure_notes:
  deployment_environment: French hospital IT systems. Text-only pipeline. No modality
    mismatch with DrBenchmark.
  it_infrastructure: '[NEEDS VERIFICATION — deferred: below search budget; confirmed
    EHR vendor landscape (Mediboard, DxCare) is primarily documented via vendor websites
    and procurement records not indexed by web search. The broader context — hospitals
    must align with the Cadre d''Interopérabilité des Systèmes d''Information de Santé
    (CI-SIS) published by ANS — is established but vendor-specific integration norms
    require direct stakeholder inquiry.]'
  data_protection_regulation: 'French clinical NLP deployments processing patient
    health data fall under an interlocking framework: (1) RGPD/GDPR as implemented
    via the Loi Informatique et Libertés; (2) HDS (Hébergeur de Données de Santé)
    certification — mandatory for any entity hosting personal health data on behalf
    of healthcare institutions, updated to HDS v2.0 (published 16 May 2024, mandatory
    for new applicants from 16 November 2024; all existing certified entities must
    migrate to v2.0 by 16 May 2026). HDS v2.0 mandates physical data storage exclusively
    within the EEA and strengthens ISO 27001:2022 alignment; (3) CNIL oversight for
    GDPR compliance and AI-specific guidance — the CNIL published healthcare-specific
    AI recommendations in July 2025 covering annotation practices and model development;
    (4) Health Data Hub (HDH/PDS) access requires CESREES scientific ethics review
    plus CNIL approval. Note: the Health Data Hub is migrating from Microsoft Azure
    to French sovereign cloud provider Scaleway (selected April 2026, migration planned
    end 2026–early 2027), reflecting ongoing data sovereignty requirements. Sources:
    HDS v2.0 framework (Hogan Lovells / Official Journal) — [WEB-4];
    HDS certification detail (Schellman 2024) — [WEB-5];
    Health Data Hub sovereign hosting (Banque des Territoires 2026) — [WEB-6]'
  compute_environment: 'French hospital clinical AI deployments that process personal
    health data must use HDS-certified hosting. Under HDS v2.0 (effective November
    2024), physical health data storage must occur exclusively within the European
    Economic Area (EEA). On-premise hospital compute avoids third-party hosting obligations;
    cloud deployment requires an HDS-certified provider (e.g., OVHcloud, Scaleway,
    Azure with HDS certification — though Microsoft Azure''s CNIL compliance status
    for health data has been contested, leading to the HDH migration). Software vendors
    operating managed services (Activity 5 under HDS) must also be HDS-certified.
    Note: HDS certification covers hosting; it does not substitute for EU AI Act compliance
    obligations for the AI system itself. Sources: HDS v2.0 (Hogan Lovells) — [WEB-4];
    ISO 42001 + HDS guide for AI providers — [WEB-7]'
  nlp_tooling_availability: 'Strong French biomedical NLP tooling ecosystem: DrBERT,
    CamemBERT-bio, CamemBERT, FlauBERT evaluated in DrBenchmark. HuggingFace Datasets/Transformers/PyTorch
    pipeline confirmed as benchmark implementation base.'
regulatory_and_governance_context:
  ai_medical_device_classification: 'This clinical NLP system very likely qualifies
    as Medical Device Software (MDSW) under EU MDR (Regulation 2017/745). Under MDR
    Rule 11 (clarified by MDCG 2019-11 guidance, revised June 2025), software providing
    information used to make diagnostic or therapeutic decisions is classified at
    minimum as Class IIa; higher patient risk conditions can elevate classification
    to Class IIb or III. A clinical decision support system generating ICD-10/PMSI-mapped
    care prioritization profiles for life-critical hospital decisions would almost
    certainly fall under Class IIa at minimum under Rule 11, with possible Class IIb
    designation depending on the clinical severity context. The June 2025 MDCG guidance
    revision sharpened the rule: most diagnostic or treatment decision-support tools
    fall under Class IIa, with Class IIb or III for higher-risk use cases. ANSM is
    the designated French competent authority for medical devices. Sources: MDCG 2019-11
    guidance (EC) — [WEB-8];
    Rule 11 classification overview (obelis.net) — [WEB-9];
    June 2025 MDCG update (Pure Global) — [WEB-10]'
  eu_ai_act_risk_tier: 'The EU AI Act (Regulation 2024/1689) entered into force on
    2 August 2024. Clinical decision support tools, diagnostic aid systems, and patient
    monitoring systems are classified as high-risk AI systems under the Act, subject
    to stringent requirements including risk management systems, training data governance,
    transparency obligations, mandatory human oversight, and post-market monitoring.
    Obligations for high-risk AI systems become fully applicable from 2 August 2027
    (Article 6(1)), giving deployers a compliance window. AI-enabled medical devices
    must comply with both MDR/IVDR and the EU AI Act, as these are complementary frameworks
    governing different dimensions of the same product. In France, ANSM and DGCCRF
    are designated as primary supervisory authorities for AI-enabled medical devices
    under the Act. Sources: G_NIUS AI Act e-health analysis — [WEB-11];
    bluepharm MDR/AI Act analysis — [WEB-12];
    PMC Medicine & AI Act review — [WEB-13]'
  french_health_authority: 'ANSM (Agence nationale de sécurité du médicament et des
    produits de santé) is the French national competent authority for medical devices
    including MDSW, requiring clinical evidence to assess safety and risk. HAS (Haute
    Autorité de Santé) evaluates medical devices and AI systems and develops clinical
    assessment guidelines; HAS collaborated with CNIL on guidance aligning AI Act
    requirements with GDPR for healthcare AI (published 2025). CNIL is the de facto
    lead regulator for AI issues involving personal data, including health data, and
    published healthcare-specific AI recommendations in July 2025. ANS (Agence du
    Numérique en Santé) sets interoperability and cybersecurity frameworks for health
    IT systems and oversees HDS certification. France does not have a single standalone
    AI regulator; oversight is sector-based. Sources: ICLG Digital Health France 2025–2026
    — [WEB-14];
    CMS AI regulations France — [WEB-15];
    French National AI & Health Strategy — [WEB-16]'
  hospital_data_governance: 'The French Espace Numérique de Santé (ENS) framework
    and Mon Espace Santé policy govern patient-facing digital health data access and
    portability, but are primarily directed at patient-facing applications rather
    than hospital-internal clinical NLP pipelines. For hospital research and AI use
    of clinical data at scale, the relevant framework is the Health Data Hub (HDH/Plateforme
    des Données de Santé, PDS), which provides controlled access to the Système National
    des Données de Santé (SNDS) — integrating PMSI, national insurance claims, and
    other sources — subject to CESREES ethics review and CNIL approval. The PDS is
    migrating to sovereign cloud (Scaleway, operational end 2026–early 2027). Hospital-internal
    deployments processing their own patient data for care delivery (not research)
    operate under RGPD/GDPR with CNIL as supervisory authority and HDS certification
    obligations for any third-party hosting. Access delays for HDH data currently
    average 9–12 months and are targeted to fall below 8 months by 2027 under EHDS
    requirements. Sources: French National AI & Health Strategy 2025–2028 — [WEB-16];
    PMC French Health Data Hub overview — [WEB-17]'
  annotation_authority_for_audits: The Silver Standard framing means system outputs
    cannot be presented as clinician-equivalent classifications. Any regulatory audit
    of system performance would likely require validation against labels produced
    by certified PMSI coders or board-certified clinicians, not academic NLP annotators.
pathology_coverage_profile:
  in_scope_metropolitan: 'Pathology profiles typical of Metropolitan French hospital
    populations: cardiovascular disease, oncology, metabolic disorders, respiratory
    conditions, neurological conditions, musculoskeletal disorders, infectious diseases
    prevalent in mainland France.'
  out_of_scope_tropical: Tropical and vector-borne pathologies characteristic of French
    overseas territories are absent from the deployment's current training data and
    from DrBenchmark's documented source corpora.
  dom_tom_gap_pathologies:
  - Dengue fever
  - Chikungunya
  - Zika virus
  - Malaria (Plasmodium falciparum and vivax)
  - Leptospirosis
  - Sickle-cell disease at population scale (particularly Martinique, Guadeloupe,
    French Guiana, Réunion)
  - Tuberculosis at elevated prevalence (French Guiana)
  - '[NEEDS VERIFICATION — deferred: below search budget; tropical pathology prevalence
    per DOM-TOM territory requires epidemiological sources (Santé Publique France,
    InVS territorial bulletins) not targeted in this search pass. The DOM-TOM gap
    is confirmed as a structural absence in DrBenchmark but the per-territory breakdown
    was not verified.]'
  diamedpan_african_signal: DiaMed's Pan African Medical Journal source may introduce
    some tropical pathology signal. The ICD-10 chapter-level labels documented in
    DrBenchmark include 'infections' (infections), 'parasitaires' (parasitology),
    and 'virales' (virology) among its 22 categories, which could in principle capture
    some tropical disease signal. However, the benchmark paper does not document whether
    Pan African Medical Journal cases in DiaMed include tropical/DOM-TOM-relevant
    pathologies, and no independent verification of this was found in targeted searches.
    The gap remains confirmed as 'undocumented' rather than 'confirmed absent.'
benchmark_task_alignment:
  benchmark_name: DrBenchmark
  benchmark_year: 2024
  task_categories_covered:
  - 'POS tagging (CAS: 31 tags; ESSAI: 36 tags)'
  - NER (QUAERO, E3C, Mantra-GSC, DEFT-2021, PxCorpus)
  - 'Multi-label classification (DEFT-2021: 23 MeSH axes; DiaMed: 22 ICD-10 chapters;
    MorFITT: 12 medical specialties)'
  - Multi-class classification
  - Intent classification (PxCorpus)
  - MCQA (FrenchMedMCQA)
  - Semantic Textual Similarity (CLISTER, DEFT-2020)
  deployment_task_coverage:
    pos_tagging: Directly covered. CAS and ESSAI provide French clinical/trial POS
      tagging tasks.
    ner: Directly covered. Multiple NER datasets with clinical entity, temporal, anatomical,
      pathology, and treatment labels. DEFT-2021 NER includes PATHOLOGY, SOSY, DATE,
      DURATION, FREQUENCY, MOMENT — highly relevant to deployment.
    multi_label_pathology_classification: Partially covered. DEFT-2021 (MeSH axes)
      and DiaMed (ICD-10 chapters) provide structural alignment, but at coarser granularity
      than operational PMSI codes. Scoring uses standard F1, not confidence calibration.
    temporal_entity_extraction: Directly covered. E3C temporal labels (EVENT, TIMEX3,
      RML) and DEFT-2021 temporal NER tags provide direct coverage.
    confidence_scored_output: Not covered. DrBenchmark scores classification with
      standard metrics only; no calibration, ranking, or uncertainty-flagging metrics
      are documented.
annotation_authority_profile:
  benchmark_annotator_population: Primarily academic NLP researchers affiliated with
    French universities and research institutions (Nantes Université, Université de
    Lille, Avignon Université, INSERM, CNRS). One medical expert documented for DiaMed
    only.
  clinical_coder_involvement: '[NOT FOUND — searched DrBenchmark paper documentation
    and French biomedical NLP literature; no evidence of PMSI coder or hospital coding
    specialist involvement in DEFT-2021, DEFT-2020, CAS, or other DrBenchmark constituent
    datasets was found. The paper describes annotators exclusively as academic NLP
    researchers, with a single medical expert (not identified as a PMSI coder) documented
    only for DiaMed. This gap is confirmed, not merely unverified.]'
  iaa_documentation: Only DiaMed provides formal inter-annotator agreement statistics
    (Cohen's Kappa, Gwet's AC1). CAS relies on automatic POS annotations validated
    at 98% precision. Most other datasets do not document IAA.
  automatic_annotation_risk: CAS POS annotations are automatically generated (Tagex),
    not fully human-adjudicated. This silver-standard provenance within the benchmark
    mirrors the deployment's own silver-standard framing and compounds label authority
    concerns.
  authority_gap_summary: 'For the deployment''s most consequential function (ICD-10/PMSI
    classification in multi-morbid cases), benchmark labels were not validated by
    the population whose authority matters most to the deployer: practicing PMSI coders
    and hospital clinicians.'
output_evaluation_alignment:
  benchmark_scoring_protocols:
    sequence_labeling: SeqEval with IOB2 format, first-token-only prediction, tokenizer-agnostic.
    classification: Majority-class baseline comparison; standard classification metrics
      (F1 implied); results averaged over 4 runs with Student's t-test.
    sts: Spearman correlation and EDRM.
    confidence_calibration: Not documented. Absent from benchmark protocol.
  deployment_output_requirements:
    multi_label_with_confidence: Required. System outputs ranked candidate labels
      with confidence scores.
    uncertainty_flagging: Required. High-uncertainty entities must be flagged for
      manual clinician review.
    ranked_candidate_lists: Required for multi-morbid case adjudication.
    benchmark_coverage_of_these: None. Structural mismatch. Standard F1 scores will
      not reveal whether a model is well-calibrated for the ranked-confidence output
      behavior the deployment requires.
  mlc_performance_caveat: DrBenchmark results show poor MLC performance even for specialized
    models (DrBERT-FS does not excel on MLC tasks). This directly implicates the deployment's
    most challenging function but does not resolve the calibration gap.
flagged_verification_targets:
- gap: Tropical and DOM-TOM pathology coverage in DrBenchmark
  search_target: French overseas territories DOM-TOM biomedical NLP clinical NER tropical
    pathology benchmark corpus DiaMed Pan African Medical Journal scope
  priority: HIGH
  resolution_status: PARTIALLY RESOLVED — DiaMed's ICD-10 chapter labels include infection,
    parasitology, and virology categories that could in principle capture some tropical
    disease signal, but the benchmark paper provides no documentation of DOM-TOM-specific
    pathology coverage. No independent NLP study on French DOM-TOM clinical corpora
    was found. Gap confirmed as 'undocumented scope' of DiaMed rather than 'verified
    absent.'
- gap: Hospital coding specialist and PMSI coder annotator involvement in DrBenchmark
    datasets
  search_target: DrBenchmark DEFT-2021 annotation protocol clinical coder PMSI ICD-10
    annotator expertise French biomedical NLP
  priority: HIGH
  resolution_status: CONFIRMED ABSENT — No evidence of PMSI coder or hospital coding
    specialist involvement in any DrBenchmark constituent dataset. The annotation
    population is exclusively academic NLP researchers, with one non-PMSI medical
    expert for DiaMed only.
- gap: Multi-label confidence calibration and uncertainty flagging scoring in DrBenchmark
  search_target: DrBenchmark multi-label classification confidence calibration scoring
    uncertainty flagging ranked output French biomedical NLP
  priority: HIGH
  resolution_status: CONFIRMED ABSENT — DrBenchmark's published protocol uses standard
    classification metrics and majority-class baselines only. No calibration, uncertainty,
    or ranked-output metrics are reported. This structural gap is confirmed from the
    benchmark paper itself.
- gap: Raw EHR noise robustness — register match between benchmark sources and active
    hospital notes
  search_target: French clinical NLP benchmark raw EHR discharge notes noise robustness
    abbreviation shorthand hospital documentation CAS DEFT corpus
  priority: HIGH
  resolution_status: 'CONFIRMED GAP — No French-language raw-EHR clinical NLP benchmark
    was found. The closest analogues (EHRNoteQA, NeurIPS 2024) are English-language
    only (MIMIC-IV). Recent meta-analysis of medical LLM benchmarks (2025) confirms
    that a significant number are constructed from academic materials rather than
    authentic clinical data, a systemic flaw directly applicable to DrBenchmark''s
    source composition. Source: arXiv 2508.04325 — [WEB-18]'
- gap: Silver standard label provenance and adjudication methodology across all 20
    DrBenchmark tasks
  search_target: DrBenchmark annotation methodology silver standard expert adjudication
    DEFT NER multi-label French biomedical NLP dataset provenance
  priority: MODERATE
  resolution_status: CONFIRMED PARTIAL — Annotation provenance is documented only
    for a subset of tasks. CAS uses automatic annotations (Tagex). DiaMed is the sole
    task with documented IAA and medical expert involvement. The majority of the 20
    tasks document annotation provenance inadequately for clinical deployment validation
    purposes.
- gap: French regulatory framework for clinical AI (MDR, EU AI Act, ANSM, HAS, CNIL
    health data)
  search_target: France ANSM HAS clinical decision support AI regulation MDR MDSW
    EU AI Act high risk hospital NLP CNIL health data
  priority: MODERATE
  resolution_status: RESOLVED — See regulatory_and_governance_context fields for verified
    values with citations.
- gap: PMSI code structure and granularity vs. ICD-10 chapter level used in DiaMed
  search_target: PMSI Programme Médicalisation Systèmes Information ICD-10 chapter
    granularity French hospital coding 2023 2024
  priority: MODERATE
  resolution_status: RESOLVED — See clinical_coding_framework.pmsi_specifics for verified
    values with citations.
- gap: French hospital EHR system landscape and clinical NLP integration norms
  search_target: France hôpital EHR dossier patient informatisé DPI Mediboard DxCare
    clinical NLP integration standards HDS
  priority: LOWER
  resolution_status: 'DEFERRED — deferred: below remaining search budget. HDS certification
    framework for hosting is resolved in infrastructure_notes. Specific EHR vendor
    landscape requires procurement/vendor sources not readily searchable.'
cultural_and_institutional_norms_notes: '- French hospital system operates under a
  unified national public health framework (Système National de Santé) with strong
  central regulatory oversight via HAS and ANSM.

  - PMSI coding is a nationally standardized but hospital-operationalized practice;
  coding conventions can vary across institutions and clinical specialties.

  - French medical culture emphasizes physician authority; clinical decision support
  tools are expected to augment, not replace, clinician judgment — consistent with
  the Silver Standard framing.

  - Data sovereignty and patient data protection are salient concerns in French hospital
  AI deployment; HDS certification and CNIL compliance are expected baseline requirements.
  The 2024 HDS v2.0 update reinforces EEA-only data residency and data sovereignty
  obligations, reflecting ongoing national political sensitivity about health data
  hosted on US cloud platforms.

  - The French biomedical NLP research community (Nantes, Lille, Avignon, INSERM affiliates)
  overlaps substantially with the DrBenchmark author team, meaning benchmark design
  reflects academic rather than operational hospital priorities.

  - Multimorbidity and polypharmacy are clinically significant in the French hospital
  inpatient population, making multi-label classification fidelity and confidence
  calibration especially consequential.

  - France launched a National Strategy on Data and Artificial Intelligence in Healthcare
  (2025–2028), developed with over 70 stakeholders including hospitals, startups,
  and patient groups. This strategy acknowledges the system as complex and slow, with
  health data access delays averaging 9–12 months and a target to reduce these below
  8 months by 2027. Source: [WEB-16]

  '
domain_specific_notes: '- ICD-10 to PMSI mapping is not a direct 1:1 translation;
  PMSI uses GHM (Groupes Homogènes de Malades) groupings for hospital financing that
  derive from but differ from raw ICD-10 codes. The GHM grouping algorithm (fonction
  groupage) combines ICD-10 principal and secondary diagnoses, CCAM procedure codes,
  patient age, and length of stay. Benchmark alignment at ICD-10 chapter level may
  not capture PMSI-relevant distinctions. The 2024 GHM classification manual is maintained
  by ATIH at [WEB-2].

  - PMSI coding reliability has documented quality concerns: published research on
  PMSI-MCO data notes that ICD coding quality is unequal and that some disease categories
  (e.g., bacterial resistance) cannot be reliably characterized from PMSI coding alone,
  partly due to initial coding errors. This reinforces the Silver Standard framing''s
  concern about the gap between benchmark ICD-10 chapter labels and operational PMSI
  coding practice. Source: PubMed PMSI bacterial resistance study — [WEB-19]

  - Temporal entity extraction is clinically critical for care prioritization (onset
  dates, treatment durations, follow-up schedules). DrBenchmark provides relevant
  temporal labels (DEFT-2021, E3C) but sources are edited academic cases, not time-pressured
  clinical documentation.

  - PxCorpus (spoken drug prescription transcripts) is the benchmark''s closest analogue
  to noisy clinical input, but its domain (pharmacist-patient drug prescription) differs
  from inpatient clinical note authorship.

  - The deployer''s requirement for confidence-scored multi-label outputs is not addressable
  with standard benchmark F1 metrics. A supplementary evaluation protocol (e.g., calibration
  curves, ECE scores, AUROC per label) would be needed to assess deployment-relevant
  performance.

  - French clinical abbreviations (e.g., ATCD for antécédents, TTT for traitement,
  HDJ for hôpital de jour) are common in hospital notes and may not be well-represented
  in DrBenchmark''s more formally edited source corpora.

  - No French-language raw-EHR clinical NLP benchmark analogous to EHRNoteQA (English,
  MIMIC-IV, NeurIPS 2024) exists in the current literature. This is a net-new finding
  confirming a methodological gap: the benchmark-to-deployment register gap cannot
  currently be quantified using publicly available French benchmarks. Source: EHRNoteQA
  — [WEB-1]

  '
net_new_fields:
  french_national_ai_health_strategy_2025_2028: 'France published a National Strategy
    on Data and AI in Healthcare (2025–2028), developed with over 70 stakeholders
    (hospitals, startups, patient groups, agencies). The strategy acknowledges that
    AI certification of health AI devices is lengthy, coordination between agencies
    is challenging, and health data access currently averages 9–12 months. This institutional
    context means new clinical NLP deployments face substantial regulatory lead times.
    Source: frenchexpertinireland.com synthesis — [WEB-16]'
  hds_v2_compliance_deadline: 'HDS v2.0 (Hébergeur de Données de Santé) was published
    16 May 2024 and became mandatory for new certification applicants from 16 November
    2024. All existing HDS-certified entities must migrate to v2.0 by 16 May 2026.
    Key new requirements: mandatory EEA-only physical data storage, ISO 27001:2022
    alignment, and enhanced transparency obligations on data transfers. Software vendors
    providing managed application services (Activity 5) for hospital systems must
    hold HDS certification. This creates a hard compliance deadline for any third-party
    clinical NLP deployment infrastructure. Source: Hogan Lovells HDS v2.0 analysis
    — [WEB-4]'
  eu_ai_act_high_risk_healthcare_timeline: 'EU AI Act (Regulation 2024/1689) entered
    into force 2 August 2024. High-risk AI system obligations (including clinical
    decision support, care prioritization, and patient monitoring tools) become fully
    applicable 2 August 2027. Deployers have a compliance window but must begin conformity
    assessment preparation now. France designated ANSM and DGCCRF as primary national
    supervisors for AI-enabled medical devices under the Act, alongside CNIL for data
    protection. Source: bluepharm EU AI Act medical devices analysis — [WEB-12]'
  pmsi_coding_quality_concern: 'Published research on the PMSI-MCO database has documented
    unequal ICD coding quality across institutions and disease categories. One study
    found inconsistencies between infection types, causative agents, and resistance
    codes attributed to initial coding errors, concluding that certain disease cartographies
    cannot be reliably developed from current PMSI coding. This epidemiologically
    documented coding variability in the very system the deployment maps to reinforces
    the Silver Standard framing and the annotation authority gap identified in the
    benchmark. Source: French PMSI bacterial resistance study (ScienceDirect 2018)
    — [WEB-20]'
  no_french_raw_ehr_benchmark_confirmed: 'As of the search date (May 2026), no French-language
    clinical NLP benchmark using raw hospital EHR discharge notes (analogous to EHRNoteQA
    for English/MIMIC-IV) was identified. This is a confirmed null result, not a search
    failure: recent literature explicitly flags that most clinical NLP benchmarks
    are constructed from academic materials rather than authentic EHR data, and no
    French exception was found. This gap materially affects the IC (Input Content)
    and benchmark register validity dimensions of the assessment. Source: EHRNoteQA
    (NeurIPS 2024) — [WEB-1]; medical benchmark critique
    (arXiv 2508.04325) — [WEB-18]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/abs/2402.16040 |
| WEB-2 | https://www.lespmsi.com/2024/manuel_GHM_2024_volume1_provisoire.pdf |
| WEB-3 | https://academic.oup.com/ije/article/46/2/392/2972209 |
| WEB-4 | https://engage.hoganlovells.com/knowledgeservices/news/health-data-hosting-the-new-french-hds-certification-has-been-released |
| WEB-5 | https://www.schellman.com/blog/compliance/new-hds-framework-2024 |
| WEB-6 | https://www.banquedesterritoires.fr/la-plateforme-des-donnees-de-sante-choisi-son-hebergement-souverain |
| WEB-7 | https://iso42001consultant.com/blog/hds-certification-for-ai-providers/ |
| WEB-8 | https://health.ec.europa.eu/system/files/2020-09/md_mdcg_2019_11_guidance_en_0.pdf |
| WEB-9 | https://www.obelis.net/news/classification-of-medical-devices-software-in-the-european-union/ |
| WEB-10 | https://www.pureglobal.com/news/mdcg-guidance-documents-clarify-rules-on-medical-device-software-in-the-eu |
| WEB-11 | https://gnius.esante.gouv.fr/en/whats-new/news/ai-act-what-new-european-law-means-e-health |
| WEB-12 | https://bluepharm.fr/en/european-artificial-intelligence-act/ |
| WEB-13 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12282355/ |
| WEB-14 | https://iclg.com/practice-areas/digital-health-laws-and-regulations/france |
| WEB-15 | https://cms.law/en/int/expert-guides/ai-regulation-scanner/france |
| WEB-16 | https://www.frenchexpertinireland.com/blog/frances-national-strategy-on-data-and-artificial-intelligence-in-healthcare-2025-2028/ |
| WEB-17 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6697511/ |
| WEB-18 | https://arxiv.org/html/2508.04325 |
| WEB-19 | https://pubmed.ncbi.nlm.nih.gov/29673880/ |
| WEB-20 | https://www.sciencedirect.com/science/article/abs/pii/S0399077X17307072 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark sources clinical cases primarily from metropolitan France. Does the deployment also serve French-speaking health systems outside mainland France — Belgium, Switzerland, Quebec, or French overseas territories — where terminology, coding conventions, or disease prevalence may differ?
A1: The system is currently scoped to Metropolitan France, so off-the-shelf use elsewhere would be risky due to divergent terminology and coding standards. If adaptation were needed, French overseas territories would be the top priority, as they have distinct disease patterns (e.g., tropical pathologies) absent from mainland training data.

Q2 [OC]: The system maps pathologies to standardized classification axes. Would the benchmark's annotators — likely academic biomedical NLP researchers rather than practicing clinicians — be considered authoritative by the hospital staff acting on these outputs, especially for ambiguous or multi-morbid cases?
A2: The system is acknowledged as a "Silver Standard" clinical support tool, not an authoritative classifier. Its ICD-10 mappings may not perfectly align with specific hospital coding conventions or complex case nuances. Physicians and nurses retain final decision-making authority; the system provides a synthesized starting point for their expert adjudication.

Q3 [IC]: Clinical notes in active hospital use often contain heavy abbreviations, dictation errors, and institution-specific shorthand. Does the patient documentation resemble well-formed academic case write-ups, or raw informal clinician notes?
A3: The system performs best on relatively clean, standard-terminology documentation and has moderate resilience to common abbreviations and shorthand. Excessively noisy or institution-specific notes would require additional pre-processing (custom glossaries, normalization modules) before the system can reliably capture severity and temporal signals.

Q4 [OO]: Does the system output a single authoritative label per entity or multiple candidate classifications with confidence signals — and how does the benchmark's scoring align with this behavior?
A4: The system outputs multiple candidate labels with associated confidence scores, allowing clinicians to adjudicate between plausible classification axes. High-uncertainty entities are flagged for manual review. This multi-label-with-confidence behavior is essential for multi-morbid cases but may not be fully reflected in how DrBenchmark scores classification tasks.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | Benchmark is ground-up French biomedical and aligns well with Metropolitan France deployment, but tropical/overseas-territory pathology categories are structurally absent, creating a bounded but real gap. |
| IC | HIGH | The system processes normatively consequential clinical data (severity signals, temporal entities for care prioritization), and benchmark instances drawn from academic/published sources may not represent the moderate-noise, shorthand-laden notes present in active hospital use. |
| IF | LOWER | Both deployment and benchmark are text-only in standard French; no modality mismatch, no low-resource script issues, and infrastructure alignment is assumed within French hospital IT. |
| OO | HIGH | The deployment requires multi-label output with confidence scores and uncertainty flagging, whereas typical benchmark classification scoring uses single-label accuracy or macro-F1 — a structural mismatch that may mask performance on the clinician-adjudication behavior the system actually needs. |
| OC | HIGH | Ground-truth labels carry "Silver Standard" status and were validated by academic NLP annotators rather than practicing hospital clinicians; for ambiguous or multi-morbid mappings, label authority is explicitly questioned by the deployer, and the annotator pool is unlikely to reflect hospital coding specialists. |
| OF | MODERATE | The benchmark outputs labels and scores, which partially matches deployment needs, but the deployment additionally requires ranked candidate lists with calibrated confidence and uncertainty flags — output granularity the benchmark's evaluation protocol does not directly measure. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Benchmark:** DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Domain
**Datasets analyzed:** 11 datasets — QUAERO, FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC, E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI
**Analysis date:** 2025-07-10

---

### Per-Dataset Fit Assessment

#### QUAERO
- **Task:** Token-classification NER (EMEA drug leaflets + MEDLINE biomedical titles), 10 UMLS Semantic Group labels
- **Deployment fit:** Partial — QUAERO provides broad clinical entity vocabulary (DISO, ANAT, PROC, CHEM, LIVB) in French biomedical text, directly serving the deployment's NER function. However, the EMEA register is patient-facing regulatory prose rather than hospital documentation, and the dataset contains no temporal entity labels whatsoever.
- **Key strengths:**
  - Dual-register coverage (drug labels + MEDLINE titles) exercises diverse pharmaceutical and clinical vocabulary relevant to hospital NER (QUAERO-D1, QUAERO-D2, QUAERO-D4, QUAERO-D5)
  - UMLS Semantic Group ontology covers all major clinical entity types needed for pathology and treatment recognition (QUAERO-D10)
  - Medline titles span oncology, cardiology, neurology, and infectious disease, partially covering ICD-10 chapter breadth (QUAERO-D6, QUAERO-D8)
  - Text-only standard French; no modality or script concerns (QUAERO-D9)
- **Key concerns:**
  - EMEA register features parenthetical lay-language glosses absent from clinical notes (QUAERO-D11); document-splitting artefacts visible (QUAERO-D12) — register mismatch is CRITICAL for IC validity
  - Complete absence of temporal entity labels (DATE, DURATION, FREQUENCY, MOMENT) despite temporal expressions appearing in the text (QUAERO-D13, QUAERO-D14) — CRITICAL OO gap
  - MEDLINE titles are extremely short and telegraphic, testing string-matching rather than contextual clinical reasoning (QUAERO-D15, QUAERO-D16); some entries are biographical/historical (QUAERO-D17, QUAERO-D19, QUAERO-D20)
  - No ICD-10/PMSI classification signal; annotator expertise for entity boundary decisions undocumented (QUAERO-D18)

---

#### FrenchMedMCQA
- **Task:** Multiple-choice QA from French pharmacy specialization diploma exams; single and multi-answer (1–5 correct answers per question)
- **Deployment fit:** Weak — The dataset tests pharmacological declarative knowledge retrieval, not NER, POS tagging, multi-label pathology classification, or temporal extraction. Domain (pharmacy exam) diverges substantially from hospital clinical note processing; output structure (answer-set selection) is orthogonal to all deployment output functions.
- **Key strengths:**
  - Standard medical French throughout; no modality or script concerns (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D4)
  - Multi-answer structure exercises some multi-label reasoning logic (FRENCHMEDMCQA-D3, FRENCHMEDMCQA-D5)
  - Some parasitology and tropical pathology coverage in content (FRENCHMEDMCQA-D65, FRENCHMEDMCQA-D67), providing marginal DOM-TOM signal
  - Unambiguous fact-check items have high annotation reliability (FRENCHMEDMCQA-D77)
- **Key concerns:**
  - Domain mismatch is CRITICAL: every sampled example is from a pharmacy exam (subject_name="pharmacie"), covering analytical chemistry, electroanalysis, and health economics with no NLP deployment relevance (FRENCHMEDMCQA-D2, FRENCHMEDMCQA-D23, FRENCHMEDMCQA-D45, FRENCHMEDMCQA-D43)
  - Output ontology mismatch is CRITICAL: discrete answer-set selection from five fixed options has no structural relation to NER spans, POS tags, or ICD-10 code assignment (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D32)
  - No confidence calibration, uncertainty flagging, or ranked-candidate quality evaluation possible (FRENCHMEDMCQA-D20)
  - Some questions reference chemical structure diagrams unavailable in text-only format (FRENCHMEDMCQA-D40)

---

#### DEFT2020
- **Task:** Semantic textual similarity (Task 1: sentence-pair scoring 0–5; Task 2: three-way sentence selection)
- **Deployment fit:** Partial (for biomedical subset only) — The pharmaceutical and systematic review sentence pairs provide useful French biomedical STS signal relevant to entity normalization and clinical summary evaluation. However, approximately 30–40% of content is non-biomedical encyclopedic material, and the STS task format does not directly evaluate NER, classification, or ICD-10 mapping.
- **Key strengths:**
  - Pharmaceutical drug-leaflet and clinical-trial STS pairs represent authentic biomedical French (DEFT2020-D1, DEFT2020-D2, DEFT2020-D4, DEFT2020-D5)
  - Multi-annotator scoring preserves inter-annotator disagreement signal relevant to uncertainty handling (DEFT2020-D6, DEFT2020-D7)
  - Standard written French throughout; no modality concerns (DEFT2020-D8)
- **Key concerns:**
  - CRITICAL IC/IO contamination: 30–40% of examples are off-domain encyclopedic content covering railways, sports, history, and video games (DEFT2020-D9, DEFT2020-D10, DEFT2020-D11, DEFT2020-D12); one example contains non-Latin (Japanese) script (DEFT2020-D13). Aggregate benchmark scores conflate clinical and off-domain performance
  - STS task format (regression/selection) does not measure NER, classification, or ICD-10 mapping (DEFT2020-D14, DEFT2020-D15)
  - Annotator disagreement averaged away in scoring; no calibration metric reported (DEFT2020-D16)
  - No clinical case NER or pathology classification signal present (DEFT2020-D17)

---

#### MORFITT
- **Task:** Multi-label medical specialty classification (12 specialty labels) of PMC Open Access biomedical abstracts
- **Deployment fit:** Partial — MORFITT provides natively multi-label classification directly relevant to the deployment's multi-morbid pathology classification function, and it contains some tropical pathology signal (chikungunya, parasitology). However, the label space (research specialty) diverges from ICD-10/PMSI diagnostic categories, veterinary content is off-domain, and a notable fraction of abstracts originate from non-Metropolitan French settings.
- **Key strengths:**
  - Native multi-label structure with one-hot float32 vectors supports multi-label model evaluation (MORFITT-D4, MORFITT-D6)
  - Some tropical and infectious disease content present, including Chikungunya (MORFITT-D17), parasitology, and MRSA (MORFITT-D8)
  - Standard biomedical French register (MORFITT-D3)
- **Key concerns:**
  - CRITICAL IC: Source is entirely PMC Open Access abstracts — formal experimental prose, not clinical notes (MORFITT-D2, MORFITT-D16); register gap is fundamental
  - MAJOR OO: 12 specialty labels (microbiology, surgery, pharmacology) do not map to ICD-10/PMSI diagnostic axes; specialty routing ≠ diagnostic classification (MORFITT-D11, MORFITT-D21)
  - MAJOR IC/OC: Substantial non-Metropolitan French content (Canadian, Jordanian, Saudi, Arabic populations) (MORFITT-D10, MORFITT-D20, MORFITT-D31, MORFITT-D22)
  - MAJOR IC/IO: Veterinary content (equine, porcine, canine) is entirely off-domain for human hospital deployment (MORFITT-D5, MORFITT-D9, MORFITT-D26, MORFITT-D29)
  - Annotation provenance undocumented; no IAA statistics; confidence calibration not evaluable

---

#### CLISTER
- **Task:** French clinical STS — sentence-pair similarity scoring (0–5 float, averaged multi-annotator)
- **Deployment fit:** Partial — CLISTER provides the most clinically authentic French text register in the benchmark's STS tasks, sourced from clinical case documents in standard hospital prose. However, STS scoring does not directly evaluate NER, classification, or ICD-10 mapping, and annotator expertise is undocumented.
- **Key strengths:**
  - Clinical case register closely mirrors hospital documentation: surgical, oncological, nephrology, psychiatric cases in standard French medical prose (CLISTER-D1, CLISTER-D2)
  - Temporal and medication expressions present and well-represented (CLISTER-D10, CLISTER-D11)
  - Clinical sub-domain breadth across urology, oncology, gynecology, cardiology, psychiatry, pediatrics (CLISTER-D5, CLISTER-D6, CLISTER-D7)
  - Continuous label scale captures semantic gradient more informative than binary labels (CLISTER-D8, CLISTER-D9)
- **Key concerns:**
  - MAJOR OO: STS regression does not measure NER, classification, or ICD-10 mapping functions
  - MAJOR OC: Annotator profiles undocumented; clinically significant distinctions (e.g., lost to follow-up vs. death) may be systematically underweighted by non-specialist annotators (CLISTER-D12, CLISTER-D13)
  - MAJOR IC: All source documents are edited published clinical case PDFs, not raw EHR dictation notes (CLISTER-D18)
  - MINOR IO: Noticeable domain skew toward urology/oncology (CLISTER-D16); some degenerate tabular inputs (CLISTER-D17)

---

#### MANTRAGSC
- **Task:** Multilingual NER (French, German, English, Spanish, Dutch) across EMEA, Medline, and Patents sub-corpora; 10–11 UMLS Semantic Group labels
- **Deployment fit:** Weak-to-partial — The French-specific configs (fr_emea, fr_medline, fr_patents) provide valid French biomedical NER signal in the same UMLS Semantic Group label space as QUAERO, but the corpus is critically small (~100 French training examples), the source registers are non-clinical, and 9 of 12 configs are irrelevant non-French languages.
- **Key strengths:**
  - French biomedical NER in drug regulatory (EMEA), scientific (Medline), and patent text (MANTRAGSC-D1, MANTRAGSC-D2, MANTRAGSC-D5)
  - UMLS Semantic Groups provide ontologically coherent entity types (DISO, ANAT, PROC, CHEM, LIVB)
  - Standard formal French in French-specific configs (MANTRAGSC-D4)
- **Key concerns:**
  - CRITICAL IC: Extremely small French corpus (~100 training examples per config); benchmark results have high variance and CamemBERT models produce only 'O' labels in low-resource conditions (MANTRAGSC-D6)
  - CRITICAL IO: All French examples from regulatory labels, MEDLINE titles, and patent claims — no clinical notes (MANTRAGSC-D7, MANTRAGSC-D8)
  - MAJOR OO: No temporal entity labels whatsoever (MANTRAGSC-D9); DISO is undifferentiated by disease type (MANTRAGSC-D10)
  - MAJOR IC: Non-French configs dominate the dataset structure (MANTRAGSC-D11); evaluation signal must be isolated to French configs only
  - MINOR OC: Annotation authority undocumented; MINOR IO: no tropical pathology coverage (MANTRAGSC-D13)

---

#### E3C
- **Task:** Multilingual clinical NER; French_clinical (binary CLINENTITY), French_temporal (EVENT, ACTOR, BODYPART, TIMEX3, RML)
- **Deployment fit:** Partial — The French_clinical and French_temporal configs provide the most deployment-relevant temporal entity annotation in the benchmark alongside DEFT2021, with authentic clinical case French. However, non-French configs dominate the overall dataset, clinical annotation is coarse and shows evidence of incompleteness, and source material is published case reports rather than raw EHR notes.
- **Key strengths:**
  - French_temporal config directly annotates TIMEX3, EVENT, and clinical entities supporting temporal extraction (E3C-D2, E3C-D3)
  - French clinical case register with complex multi-symptom narratives (E3C-D1)
  - Authentic multilingual corpus structure confirms French examples are genuine clinical narratives, not translations
  - IOB2 annotation compatible with benchmark's SeqEval evaluation protocol (E3C-D5, E3C-D6)
- **Key concerns:**
  - CRITICAL IC/IO: Non-French configs (Basque, English, Italian, Spanish) dominate sampled data; Basque configs entirely irrelevant (E3C-D7, E3C-D8)
  - MAJOR IC: Published case report register, not raw EHR — complete sentences, no shorthand (E3C-D9, E3C-D10)
  - MAJOR OC: Apparent annotation incompleteness in French_clinical — identifiable pathogens and treatments left unlabeled (E3C-D11, E3C-D12)
  - MAJOR IO: Tropical pathology appears only in English config, absent from French subset (E3C-D4, E3C-D13)
  - MINOR OO: Coarse two-class clinical annotation (CLINENTITY vs. O) underspecifies the deployment's multi-type NER requirement (E3C-D14)

---

#### PxCorpus
- **Task:** Spoken drug prescription understanding — 4-class intent classification (medical_prescription, negate, none, replace) + 38-class NER for drug entities and temporal/dosage spans
- **Deployment fit:** Partial — PxCorpus is the benchmark's closest proxy for noisy non-formal clinical language (transcribed speech with hesitations and truncations), and it provides the richest temporal entity annotation for pharmaceutical contexts. However, it covers only drug prescription dialogues rather than general clinical note processing, contains no pathology/diagnosis labels, and has severe class imbalance undermining minority-class evaluation.
- **Key strengths:**
  - Spoken transcription register with hesitation markers, truncations, and ASR artifacts — the closest noise proxy in DrBenchmark to active hospital documentation (PXCORPUS-D1, PXCORPUS-D2, PXCORPUS-D4)
  - Richest temporal NER in the benchmark: FREQUENCY, DURATION, DOSAGE, TIME-OF-DAY entities densely annotated in authentic prescription utterances (PXCORPUS-D5, PXCORPUS-D6, PXCORPUS-D7)
  - Intent labels (negate, replace) support prescription error-detection workflows (PXCORPUS-D8, PXCORPUS-D9, PXCORPUS-D10)
  - Broad pharmaceutical coverage across drug classes and routes (PXCORPUS-D11, PXCORPUS-D12, PXCORPUS-D13)
- **Key concerns:**
  - CRITICAL OO/OF: Extreme class imbalance (medical_prescription ~89%, replace <1%, negate ~2%) — standard accuracy metrics mask minority-class performance on clinically critical correction intents (PXCORPUS-D14, PXCORPUS-D15)
  - MAJOR IO/OO: No pathology/diagnosis entities in NER tag scheme; ICD-10 mapping function cannot be evaluated (PXCORPUS-D16, PXCORPUS-D17)
  - MAJOR OO/OC: The 'none' class is semantically heterogeneous — conflates meta-commentary, system prompts, and filler speech (PXCORPUS-D18, PXCORPUS-D19, PXCORPUS-D20)
  - MAJOR IC/IF: System interaction prompts embedded in clinical NER training data corrupt register (PXCORPUS-D22, PXCORPUS-D23)
  - MINOR IC: Degenerate fragment utterances and ASR artifacts present (PXCORPUS-D24, PXCORPUS-D27, PXCORPUS-D28)

---

#### DiaMED
- **Task:** Multi-class classification — 22 ICD-10 chapter-level labels on clinical case narratives from the Pan African Medical Journal
- **Deployment fit:** Partial — DiaMED is the benchmark's only dataset with direct ICD-10 chapter-level labels and documented IAA with medical expert involvement, making it the strongest single candidate for the deployment's pathology classification function. However, the source is Sub-Saharan and North African clinical cases rather than Metropolitan French hospital documentation, the task is single-label (not multi-label with confidence), and granularity is chapter-level rather than PMSI-code-level.
- **Key strengths:**
  - Only dataset with ICD-10 chapter-level labels directly aligned with deployment's classification ontology (DIAMED-D1, DIAMED-D2)
  - Rich full-length clinical narratives in standard French with dense clinical entities (DIAMED-D3, DIAMED-D4)
  - Coverage across all 22 ICD-10 chapters including rare categories (DIAMED-D5, DIAMED-D6)
  - Only DrBenchmark dataset with documented IAA statistics and explicit medical expert annotator involvement (benchmark Q45, Q46)
- **Key concerns:**
  - CRITICAL IC/OC: Cases originate from Burkina Faso, Morocco, Niger, and other African countries — not Metropolitan French hospitals (DIAMED-D7, DIAMED-D8, DIAMED-D9). PMSI coding conventions and disease prevalence patterns differ systematically from the deployment's target population
  - MAJOR OO/OF: Single-label per case; multi-morbid cases forced into one chapter (DIAMED-D10); no confidence scores or ranked-candidate output
  - MAJOR OO: Chapter-level granularity is far coarser than operational PMSI codes (DIAMED-D11)
  - MAJOR IC: Academic published case write-up register rather than active EHR notes (DIAMED-D12)
  - MINOR OC: Very small dataset (n=739) with severe per-class imbalance for rare ICD-10 chapters

---

#### DEFT2021
- **Task:** Multi-label clinical profile classification (23 MeSH Chapter C axes) + 13-type clinical NER (PATHOLOGY, ANATOMY, TREATMENT, DOSAGE, DURATION, FREQUENCY, MOMENT, DATE, SOSY, etc.)
- **Deployment fit:** Strong (within benchmark) — DEFT2021 provides the most deployment-aligned task structure in DrBenchmark: native multi-label classification with a MeSH ontology partially aligned to ICD-10, AND a rich NER scheme covering all entity types the deployment requires including temporal markers. It is structurally the benchmark's best single-dataset proxy for the deployment's core functions.
- **Key strengths:**
  - Multi-label CLS config with up to 7 concurrent MeSH labels per clinical case directly exercises multi-morbid pathology classification (DEFT2021-D1, DEFT2021-D2)
  - NER scheme covers PATHOLOGY, TREATMENT, ANATOMY, DATE, DURATION, FREQUENCY, MOMENT — complete alignment with deployment's temporal and clinical entity extraction functions (DEFT2021-D3, DEFT2021-D4, DEFT2021-D5)
  - Rich authentic clinical case register with complex diagnostic reasoning and dense laboratory values (DEFT2021-D6, DEFT2021-D7)
  - Breadth of specialties: urology, toxicology, cardiology, nephrology, emergency medicine represented (DEFT2021-D8, DEFT2021-D9)
- **Key concerns:**
  - CRITICAL OO/OF: `specialities_one_hot` is strictly binary 0/1 — no confidence scores, no soft labels, no ranked-candidate quality evaluation possible (DEFT2021-D11)
  - CRITICAL IO: No tropical/DOM-TOM pathology categories in 23 MeSH axes; parasitic content limited to temperate pathogens (DEFT2021-D12, DEFT2021-D13)
  - MAJOR IC: Competition corpus (DEFT 2019) — academic edited register, not raw EHR shorthand (DEFT2021-D14, DEFT2021-D15)
  - MAJOR OC: Annotator PMSI credentials undocumented; MeSH axis choices for complex multi-drug cases may not align with hospital coding specialist conventions (DEFT2021-D16)
  - MAJOR IO: Very small (275 cases) with high per-label variance; some axes have very few positives (DEFT2021-D17)
  - MINOR IC: Some Quebec French terminology (DEFT2021-D20)

---

#### CAS
- **Task:** French clinical case corpus — negation/speculation classification (4 labels), negation/speculation NER (IOB2), and POS tagging (31 classes, automatic Tagex annotations)
- **Deployment fit:** Partial — CAS provides the largest French clinical case corpus in the benchmark with authentic clinical register and useful negation/speculation signal for clinical NLP pipelines. However, the classification labels (negation/speculation modality) are orthogonal to ICD-10 pathology categories, and POS tags are silver-standard automatic annotations.
- **Key strengths:**
  - Largest clinical case corpus; authentic French clinical register with lab values, surgical narratives, and temporal expressions (CAS-D1, CAS-D2, CAS-D3)
  - Temporal expression content directly relevant to deployment's care timeline extraction (CAS-D4, CAS-D5, CAS-D6)
  - Negation/speculation annotation supports downstream accurate pathology coding (CAS-D7, CAS-D8, CAS-D9)
  - Specialty breadth including gastroenterology, obstetrics, cardiology, oncology, infectious disease (CAS-D10, CAS-D11, CAS-D12)
  - POS tagging directly covers deployment's POS tagging pipeline component (CAS-D13)
- **Key concerns:**
  - CRITICAL OC: POS tags are silver-standard automatic (Tagex); no expert clinical annotator involvement documented (CAS-D15)
  - MAJOR OC: No IAA statistics for negation/speculation labels; annotation rationale opaque for some ambiguous cases (CAS-D16, CAS-D17)
  - MAJOR OO: Classification labels (negation/speculation) do not align with ICD-10/PMSI mapping; task is a linguistic modality detector, not a pathology classifier (CAS-D19)
  - MAJOR IO: No tropical/overseas-territory pathologies visible across all sampled examples (CAS-D18)
  - MINOR IC: Register slightly more formal than raw EHR notes (CAS-D20); severe class imbalance in cls config with neutral dominating at ~74% (CAS-D21)

---

#### ESSAI
- **Task:** French clinical trial protocol corpus — negation/speculation classification (4 labels), negation/speculation NER, and POS tagging (36 tags, TreeTagger automatic)
- **Deployment fit:** Weak-to-partial — ESSAI covers an even narrower subdomain than CAS (exclusively oncology clinical trial protocols), provides the same output ontology mismatch (negation/speculation, not ICD-10), and uses automatic POS annotations. Its primary value is as a formal French biomedical prose register, with negation/speculation signal relevant to pipeline preprocessing.
- **Key strengths:**
  - Formal clinical trial French biomedical register; dense oncological treatment and temporal content (ESSAI-D1, ESSAI-D2, ESSAI-D6, ESSAI-D7, ESSAI-D8)
  - Negation and speculation detection coverage including temporal dosing structures (ESSAI-D3, ESSAI-D4, ESSAI-D5)
  - 36-class POS scheme for French biomedical morphology
- **Key concerns:**
  - CRITICAL OO: Classification labels (negation/speculation) have zero overlap with ICD-10/PMSI mapping function (ESSAI-D9)
  - MAJOR IC: Source domain exclusively oncology clinical trial protocols — far narrower than general hospital documentation (ESSAI-D10, ESSAI-D11)
  - MAJOR OC: TreeTagger automatic POS; NER annotation provenance undocumented; no IAA statistics
  - MAJOR OC: Extreme class imbalance with neutral at ~77% (ESSAI-D13); NER annotation is extremely sparse (ESSAI-D14)
  - MINOR IC: No tropical/DOM-TOM pathology content

---

### Cross-Cutting Strengths

**1. Consistent standard written French across all datasets**
Every dataset in the benchmark is text-only in standard French with Latin-diacritical script. No modality, script, or dialect mismatches are present relative to the deployment's text-only clinical NLP pipeline. This uniform IF coverage means the benchmark's signal is entirely within the correct language and modality space (QUAERO-D9, CLISTER-D1, DEFT2021-D1, CAS-D1, ESSAI-D1).

**2. Multi-label classification structure present in three datasets**
DEFT2021, MORFITT, and DiaMED all implement multi-label or multi-class classification directly exercising the deployment's central pathology classification function. DEFT2021's 23 MeSH axes with up to 7 co-occurring labels (DEFT2021-D1, DEFT2021-D2), MORFITT's 12 specialty labels with float32 one-hot vectors (MORFITT-D4, MORFITT-D6), and DiaMED's 22 ICD-10 chapter labels (DIAMED-D1) collectively provide meaningful multi-label evaluation signal for a core deployment function.

**3. Temporal entity annotation coverage**
Three datasets contribute temporal entity signal: E3C's French_temporal config annotates TIMEX3, EVENT, ACTOR, BODYPART, RML (E3C-D2, E3C-D3); DEFT2021's NER scheme includes DATE, DURATION, FREQUENCY, MOMENT, and MOMENT labels explicitly (DEFT2021-D3, DEFT2021-D4, DEFT2021-D5); PxCorpus provides the most densely annotated temporal pharmaceutical expressions in the benchmark (PXCORPUS-D5, PXCORPUS-D6, PXCORPUS-D7). This cross-dataset coverage partially addresses the deployment's temporal entity extraction function.

**4. NER across complementary French biomedical registers**
QUAERO (drug labels + MEDLINE), MANTRAGSC (EMEA + Medline + Patents), E3C (clinical cases), DEFT2021 (competition clinical cases), CAS (clinical cases), and PxCorpus (drug prescriptions) collectively cover regulatory, scientific, and clinical-case registers for French biomedical NER. The UMLS Semantic Group label space shared between QUAERO and MANTRAGSC provides ontological consistency for entity type coverage (QUAERO-D1, MANTRAGSC-D1, MANTRAGSC-D2).

**5. Clinical case register depth in CAS, CLISTER, and DEFT2021**
CAS (3,790 cases), CLISTER (1,000 sentence pairs from clinical cases), and DEFT2021 (275 cases) all use French clinical case text as source material with realistic clinical prose including quantified lab values, surgical narratives, and diagnostic reasoning (CAS-D2, CLISTER-D2, DEFT2021-D7). While all are edited published cases rather than raw EHR notes, they represent the closest available approximation to the deployment's hospital documentation environment.

---

### Cross-Cutting Weaknesses

#### CRITICAL — Benchmark-wide absence of confidence calibration and uncertainty flagging evaluation (OO, OF)
Across all 11 datasets, no evaluation protocol measures confidence calibration, uncertainty flagging, or ranked-candidate list quality. Classification datasets use strictly binary labels (DEFT2021-D11, MORFITT one-hot vectors) and standard F1/accuracy metrics. DiaMED uses single-label forced-choice even for inherently multi-morbid cases (DIAMED-D10). STS datasets (CLISTER, DEFT2020) average annotator scores into a single float value, discarding the disagreement signal that could inform uncertainty evaluation (DEFT2020-D16). The deployment's most architecturally essential behavior — multi-label outputs with calibrated confidence scores and high-uncertainty flagging for clinician adjudication — is structurally unmeasurable across the entire benchmark.

#### CRITICAL — Systematic register gap: edited published sources vs. active hospital EHR notes (IC)
Every dataset in the benchmark sources text from one or more of: clinical trial protocols (ESSAI), competition corpora (DEFT2021, DEFT2020), peer-reviewed case reports (CAS, CLISTER, E3C, DiaMED), drug regulatory documents (QUAERO-EMEA, MANTRAGSC), MEDLINE titles (QUAERO-Medline, MANTRAGSC-Medline), or patent claims (MANTRAGSC-Patents). No dataset uses raw hospital EHR discharge notes, dictation recordings (beyond PxCorpus prescription-domain), or institution-specific documentation. The deployment processes moderately noisy notes with common clinical abbreviations and shorthand. Web search confirms no French raw-EHR benchmark exists. Examples of the formality gap: ESSAI-D11, CAS-D20, E3C-D9, DEFT2021-D14, DEFT2021-D15, DIAMED-D12. PxCorpus provides partial noise signal but only in the drug prescription domain (PXCORPUS-D1, PXCORPUS-D2).

#### CRITICAL — Absence of PMSI coder or hospital coding specialist annotation authority (OC)
Across all 11 datasets, no annotation was performed by practicing PMSI coders or hospital coding specialists. DiaMED is the sole dataset with documented medical expert involvement (one expert annotator), and that expert's PMSI coding credentials are unspecified (benchmark Q45). DEFT2021's multi-label MeSH annotations — the most deployment-relevant classification labels — were produced by academic NLP competition participants with no documented clinical coding credentials (DEFT2021-D16). CAS POS tags are automatic (CAS-D15). This annotation authority gap is confirmed absent benchmark-wide, not merely undocumented.

#### MAJOR — Non-Metropolitan French clinical content misrepresented as deployment-relevant (IC, OC)
DiaMED's 739 clinical cases originate from the Pan African Medical Journal, with examples from Burkina Faso, Morocco, and Niger (DIAMED-D7, DIAMED-D8, DIAMED-D9) — explicitly not Metropolitan French hospital populations. MORFITT contains substantial content from Canadian, Jordanian, Saudi, and Arabic research contexts (MORFITT-D10, MORFITT-D20, MORFITT-D22, MORFITT-D31). These datasets introduce geographic and epidemiological heterogeneity that does not correspond to the Metropolitan French deployment target, potentially distorting performance estimates for the deployment's actual patient documentation.

#### MAJOR — Tropical and overseas-territory pathology coverage absent across all French-language subsets (IO)
No dataset provides French-language clinical text or annotation covering pathologies prevalent in French overseas territories (dengue, chikungunya, Zika, malaria at population scale, leptospirosis, sickle-cell crisis presentations). The only tropical pathology signals appear in non-French dataset subsets: schistosomiasis in E3C's English config (E3C-D4), malaria in FrenchMedMCQA pharmacy questions (FRENCHMEDMCQA-D67), and Chikungunya in a MORFITT abstract (MORFITT-D17). DiaMED's Pan African Medical Journal source introduces some tropical disease proximity via ICD-10 infectious disease chapters, but its cases are not Metropolitan French and the specific DOM-TOM pathology coverage is undocumented. The French-language clinical NER and classification datasets are entirely metropolitan in pathology profile.

#### MAJOR — Output ontology misalignment for multiple datasets (OO)
Four datasets — CAS, ESSAI, FrenchMedMCQA, and DEFT2020 (partially) — have output ontologies entirely orthogonal to the deployment's ICD-10/PMSI classification function. CAS and ESSAI measure negation/speculation modality (CAS-D19, ESSAI-D9). FrenchMedMCQA measures pharmacy exam answer-set selection (FRENCHMEDMCQA-D1). DEFT2020 measures sentence-pair similarity (DEFT2020-D14, DEFT2020-D15). MANTRAGSC and QUAERO measure UMLS Semantic Group NER with no ICD-10 subcategory distinction (MANTRAGSC-D10, QUAERO — no ICD-10 signal). Only DEFT2021, DiaMED, and MORFITT provide classification labels with any ICD-10 or specialty-level alignment.

#### MAJOR — Temporal entity annotation concentrated in few datasets, absent in most (IO, OO)
The majority of DrBenchmark datasets provide no temporal entity labels: QUAERO has no temporal labels despite temporal expressions in text (QUAERO-D13, QUAERO-D14); MANTRAGSC has no temporal labels (MANTRAGSC-D9); MORFITT, CLISTER, CAS (cls), and ESSAI (cls) have no temporal NER. Temporal coverage is limited to E3C French_temporal, DEFT2021 NER, and PxCorpus — a narrow subset of the benchmark's 20 tasks. Given the deployment's explicit requirement for temporal entity extraction for care prioritization, this concentration is a systemic coverage gap.

#### MINOR — Severe class imbalance across multiple classification datasets (OF, OO)
CAS cls neutral class ~74% (CAS-D21); ESSAI cls neutral ~77% (ESSAI-D13); PxCorpus medical_prescription ~89% (PXCORPUS-D15). In all three cases, majority-class baselines achieve high accuracy while being clinically uninformative, and evaluation of the minority classes most relevant to the deployment (negation, speculation, prescription correction, intent replacement) is unreliable.

---

### Content Coverage Summary

**Well-covered domains and registers:**
- Standard written French biomedical prose across regulatory (EMEA drug labels), scientific (MEDLINE, PMC abstracts), clinical case (CAS, CLISTER, E3C, DEFT2021, DiaMED), pharmaceutical patent, and spoken prescription (PxCorpus) registers
- Clinical entity types: pathology, anatomy, procedure, chemical substance, living being — covered by QUAERO, MANTRAGSC, E3C, DEFT2021
- Temporal entity types: DATE, DURATION, FREQUENCY, MOMENT — covered by DEFT2021 NER, E3C French_temporal, PxCorpus
- Negation and speculation detection: CAS, ESSAI
- Multi-label classification: DEFT2021 (23 MeSH axes), MORFITT (12 specialties), DiaMED (22 ICD-10 chapters)
- POS tagging: CAS (31 tags), ESSAI (36 tags)
- Model comparison: 8 state-of-the-art French and French-biomedical MLMs evaluated under unified protocol

**Gaps relative to deployment needs:**
- Raw EHR discharge notes and dictation-sourced text: absent from the entire benchmark; no French raw-EHR clinical NLP benchmark exists
- Confidence calibration and uncertainty flagging evaluation: structurally absent across all 20 tasks
- PMSI-granular code classification (beyond chapter level): absent; DiaMED is the coarsest available proxy
- Hospital coding specialist annotation authority: absent benchmark-wide
- Metropolitan French hospital population pathology profiles: partially represented through metropolitan clinical case corpora (CAS, CLISTER, ESSAI, DEFT2021), but contaminated by non-metropolitan content in DiaMED and MORFITT
- DOM-TOM tropical pathology coverage: absent from all French-language clinical subsets
- Multi-label classification at PMSI code level: absent; MeSH and ICD-10 chapter labels provide coarse alignment only
- Ranked-candidate output evaluation: absent across all classification tasks

---

### Limitations

1. **Sample-based analysis only**: Each per-dataset report analyzed a sample of examples (50–200 per dataset); rare label classes, corner cases, and dataset tails may be underrepresented in the evidence base. Per-class performance statistics were not computed.
2. **Non-French configs not inspectable for deployment purposes**: MANTRAGSC (9/12 configs), E3C (8/10 configs non-French), and MORFITT (non-Metropolitan French abstracts) contain substantial irrelevant content that was identified but not exhaustively characterized.
3. **Internal test set contents unknown**: The benchmark reports held-out test set performance; the per-dataset analyses inspected training/validation examples. Label distribution and content of test sets may differ from training splits.
4. **Annotation provenance beyond the paper**: The per-dataset reports and benchmark YAML provide the primary evidence for annotation authority claims. No independent access to DEFT competition annotation guidelines, CLISTER annotator demographic data, or CAS/ESSAI TreeTagger/Tagex validation methodology was available for direct inspection.
5. **DiaMED full geographic distribution unverified**: The Sub-Saharan and North African clinical origin of DiaMED cases is confirmed from sampled examples, but the full geographic distribution across all 739 cases was not enumerated.
6. **MORFITT annotation protocol**: No HuggingFace card or paper excerpt documenting the specialty annotation process for MORFITT was inspected; annotation authority and IAA are unverifiable beyond the dataset overview.
7. **PxCorpus register contamination extent**: The proportion of system-interaction-contaminated examples relative to total examples could not be quantified from the sample alone.

---

### Cited Evidence

- **QUAERO-D1**: QUAERO/emea | 38 | DISO/PROC | "TYSABRI est utilisé pour traiter la sclérose en plaques (SEP)… troubles de la marche, engourdissement du visage" | Disease/symptom enumeration in EMEA drug label; strong DISO entity density | IO, IC
- **QUAERO-D2**: QUAERO/emea | 46 | DISO/PROC | "les effets indésirables les plus couramment observés sous Tysabri… rhinopharyngite… urticaire… arthralgie… pyrexie (fièvre)" | Multi-entity adverse-event list; confirms NER coverage of pathology vocabulary | IC
- **QUAERO-D3**: QUAERO/medline | 3 | DISO | "Alcool et cancer." | Very short MEDLINE title; confirms text register range in dataset | IC
- **QUAERO-D4**: QUAERO/emea | 1 | CHEM | "Phosphate de sodium, monobasique, monohydraté… Polysorbate 80 (E433)… Eau pour préparation injectable." | Chemical excipient list; confirms pharmaceutical CHEM annotation | IC
- **QUAERO-D5**: QUAERO/emea | 55 | CHEM/DEVI | "TYSABRI 300 mg solution à diluer pour perfusion… chaque flacon de 15 ml de concentré contient 300 mg de natalizumab" | Dosage/container/drug vocabulary; confirms DEVI and CHEM annotation | IC
- **QUAERO-D6**: QUAERO/medline | 98 | DISO/GEOG | "Le paludisme chimiorésistant en France." | Malaria + geographic tag; infectious disease domain coverage | IO, IC
- **QUAERO-D7**: QUAERO/medline | 106 | DISO/LIVB | "Encéphalopathie toxique par ingestion de carambole (Averrhoa carambola)." | Tropical plant toxicity; exotic etiology in MEDLINE corpus | IC
- **QUAERO-D8**: QUAERO/medline | 45 | DISO | "Le syndrome de Noonan et sa dysplasie cardio-vasculaire." | Rare genetic/cardiovascular disorder; confirms ontological breadth | IO
- **QUAERO-D9**: QUAERO/emea | 2 | DISO/PHYS | "Une cirrhose du foie peut également affecter l'excrétion rénale de la lépirudine." | Standard written French medical prose; confirms script/register alignment | IF
- **QUAERO-D10**: QUAERO/emea | 6 | DISO | "Des épisodes de troubles psychiatriques aigus, tels que hallucinations, réactions paranoïdes… psychose et réactions maniaques" | Psychiatric DISO enumeration; tests fine-grained entity boundary detection | OO
- **QUAERO-D11**: QUAERO/emea | 46 | DISO | "rhinopharyngite (inflammation du nez et de la gorge), urticaire (éruption cutanée)" | Patient-leaflet gloss structure absent from clinical notes; register mismatch | IC
- **QUAERO-D12**: QUAERO/emea | 4 | O | "Aucune étude clinique spécifique sur les interactions médicamenteuses n Toutefois…" | Sentence truncation artefact from EMEA document splitting; preprocessing noise | IC
- **QUAERO-D13**: QUAERO/emea | 26 | O | "La durée du traitement est allée d'une heure de perfusion en bolus à une utilisation continue de plus de 6 ans." | Temporal expressions present but unlabeled; confirms absence of temporal NER | OO
- **QUAERO-D14**: QUAERO/emea | 11 | O | "La dose peut être augmentée par intervalles de 1 à 2 jours, voire plus…" | Another unlabeled temporal phrase; reinforces temporal NER gap | OO
- **QUAERO-D15**: QUAERO/medline | 27 | PHYS | "Anoïkis." | Single-token title; zero context, tests only string-matching NER | IC
- **QUAERO-D16**: QUAERO/medline | 3 | DISO | "Alcool et cancer." | Three-token title; minimal clinical context for entity recognition | IC
- **QUAERO-D17**: QUAERO/medline | 61 | O | "LÉON GRIMBERT 1860 - 1931." | Biographical entry; no clinical entities; irrelevant to clinical NLP | IC
- **QUAERO-D18**: QUAERO/emea | 64 | DISO/ANAT | "Si vous avez des perturbations graves du système immunitaire (dues à une maladie, telle que leucémie ou infection à VIH…" | Entity boundary ambiguity; annotation by NLP researchers may differ from clinician judgment | OC
- **QUAERO-D19**: QUAERO/medline | 16 | O | "L'apport des inventaires a la connaissance de la demographie parisienne ancienne: le regne de Francois Ier" | Historical demography; not clinically relevant | IC
- **QUAERO-D20**: QUAERO/medline | 34 | O | "La santé du duc d'Enghien durant ses primes années d'après le journal de son médecin." | Historical biographical text; off-domain for clinical NLP | IC
- **QUAERO-D21**: QUAERO/medline | 137 | DISO/LIVB | "Sensibilité à la pénicilline G des pneumocoques isolés des méningites et implication thérapeutique au CHU de Treichville-Abidjan." | Sub-Saharan institution; non-metropolitan French clinical context in MEDLINE | IC
- **FRENCHMEDMCQA-D1**: FrenchMedMCQA | 1 | 1 | "Au cours de la leucémie lymphoïde chronique, le myélogramme montre: Une population de lymphocytes>30%" | Clinical hematology question in formal medical French | IC, IF
- **FRENCHMEDMCQA-D2**: FrenchMedMCQA | 2 | 2 | "La loi de Beer-Lambert: S'applique aux dosages spectrophotométriques... Est une loi additive" | Analytical chemistry question irrelevant to clinical NLP | IO, OC
- **FRENCHMEDMCQA-D3**: FrenchMedMCQA | 3 | 3 | "Parmi les propriétés suivantes du monoxyde de carbone... correct_answers: [0, 3, 4]" | Multi-label MCQA structure covering CO properties | IO
- **FRENCHMEDMCQA-D4**: FrenchMedMCQA | 4 | 4 | "L'acétylcholine est libérée par: Les neurones sympathiques préganglionnaires" | Pharmacological terminology in standard medical French | IC, IF
- **FRENCHMEDMCQA-D5**: FrenchMedMCQA | 5 | 5 | "Les marqueurs suivants sont présents dans les lymphocytes B matures... correct_answers: [0, 1, 2, 3, 4]" | All-five-correct multi-label answer, showing full label cardinality | IO
- **FRENCHMEDMCQA-D9**: FrenchMedMCQA | 9 | 4 | "L'oeuf d'Enterobius vermicularis: Est incolore, Est asymétrique..." | Parasitology content with partial tropical relevance | IO
- **FRENCHMEDMCQA-D13**: FrenchMedMCQA | 13 | 3 | "Quel est (sont) le(s) diurétique(s) qui provoque(nt) une baisse du potassium sanguin? Chlortalidone, Hydrochlorothiazide, Furosémide" | Drug class knowledge relevant to clinical pharmacology | IC
- **FRENCHMEDMCQA-D14**: FrenchMedMCQA | 14 | 4 | "intoxication par les salicylés... L'administration intraveineuse de bicarbonate de sodium permet de corriger l'acidose métabolique" | Clinical toxicology management scenario | IC
- **FRENCHMEDMCQA-D20**: FrenchMedMCQA | 20 | 5 | "Dans quel(s) cas peut-on parler d'hypertension artérielle selon les critères de l'OMS? correct_answers: [0, 1, 2, 3, 4]" | All-correct answer; no confidence signal available | OO, OF
- **FRENCHMEDMCQA-D23**: FrenchMedMCQA | 23 | 3 | "En électrophorèse capillaire haute performance, le sens de migration de l'analyse dépend: De la nature de la charge de l'analyte" | Analytical chemistry instrumentation; not relevant to clinical NLP | IO
- **FRENCHMEDMCQA-D24**: FrenchMedMCQA | 24 | 4 | "Chez un patient atteint de SIDA... Lymphopénie, Diminution des lymphocytes T4, Adénopathies, Thrombopénie" | AIDS hematological profile; relevant to pathology classification | IC
- **FRENCHMEDMCQA-D32**: FrenchMedMCQA | 32 | 4 | "correct_answers: [0, 1, 3, 4]" | Four-of-five selection; binary gold label, no confidence ranking | OO, OF
- **FRENCHMEDMCQA-D37**: FrenchMedMCQA | 37 | 1 | "Les 3 nucléides de l'hydrogène, H(A=1,Z=1), H(A=2,Z=1) et H(A=3,Z=1) sont: Des isotopes" | Nuclear physics in pharmacy exam; clean French text, no abbreviations | IF
- **FRENCHMEDMCQA-D40**: FrenchMedMCQA | 40 | 4 | "le composé suivant: Est utilisé comme antibactérien... Augmente l'ototoxicité des aminosides" | References implied chemical structure diagram; text-only representation incomplete | IC
- **FRENCHMEDMCQA-D43**: FrenchMedMCQA | 43 | 3 | "L'économie médicale est une économie... Caractérisée par le libre choix des médecins par le malade" | Health economics question; low clinical NLP relevance | IO
- **FRENCHMEDMCQA-D45**: FrenchMedMCQA | 45 | 1 | "Parmi les techniques voltampérométriques, on trouve: La polarographie" | Electroanalytical chemistry; irrelevant to hospital clinical NLP | IO
- **FRENCHMEDMCQA-D61**: FrenchMedMCQA | 61 | 1 | "La certification des établissements de santé: Concerne tous les établissements de santé" | Health system regulation; marginal clinical NLP relevance | IO
- **FRENCHMEDMCQA-D65**: FrenchMedMCQA | 65 | 1 | "le mode habituel de contamination de l'homme dans la bilharziose urinaire: Pénétration trans-cutanée" | Tropical parasitosis; partial DOM-TOM pathology coverage | IO, IC
- **FRENCHMEDMCQA-D67**: FrenchMedMCQA | 67 | 3 | "Quelle est (sont) la (les) parasitose(s) qui présente(nt) un stade hépatique? Giardiase, Paludisme, Fasciolose; correct: [1, 2, 3]" | Malaria and other tropical parasitoses included | IO, IC
- **FRENCHMEDMCQA-D77**: FrenchMedMCQA | 77 | 1 | "Quelle est la base qui n'existe pas dans une molécule d'ADN? Uracile" | Unambiguous factual label, high annotation reliability | OC
- **FRENCHMEDMCQA-D99**: FrenchMedMCQA | 99 | 3 | "Les modifications de structure permettant le passage du composé 1 au composé 2 entraînent: Un élargissement du spectre vers les cocci Gram+" | Structure-comparison question requiring figure; no extractable entities | IO
- **FRENCHMEDMCQA-D117**: FrenchMedMCQA | 117 | 1 | "Un patient de 20 ans est traité par héparine de bas poids moléculaire pour une thrombose iliaque... Activité anti Xa = 2,00 UI/mL" | Clean clinical vignette; structured exam format, not raw clinical note | IC
- **DEFT2020-D1**: DEFT2020/task_1 | Ex.16 | moy=4.0 | "Ce produit peut provoquer un syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après la dernière prise de stupéfiant." | Pharmaceutical drug leaflet sentence about opioid withdrawal; matches clinical register | IC
- **DEFT2020-D2**: DEFT2020/task_1 | Ex.18 | moy=4.6 | "En raison de la présence de lactose, ce médicament est contre-indiqué en cas de galactosémie congénitale, de syndrome de malabsorption du glucose et du galactose ou de déficit en lactase." | Drug contraindication notice; standard French pharmaceutical register | IC
- **DEFT2020-D3**: DEFT2020/task_2 | T2 Ex.22 | correct_cible=0 | "l'utilisation à forte dose d'huile de paraffine expose au risque de suintement anal et parfois d'irritation périanale" | Medical side-effect phrasing; evaluates clinical paraphrase equivalence | IC, OO
- **DEFT2020-D4**: DEFT2020/task_1 | Ex.26 | moy=3.4 | "Pour la comparaison entre blocs neuraxiaux et anesthésie générale, nous avons évalué la qualité des preuves comme très faible pour la mortalité..." | Systematic review evidence-appraisal language; clinical summary register | IC
- **DEFT2020-D5**: DEFT2020/task_1 | Ex.31 | moy=2.7 | "Déterminer l'effet d'une alimentation trophique précoce comparée à un jeûne entéral sur la tolérance à l'alimentation, la croissance et le développement..." | Neonatal intensive care research objective; relevant to temporal entity extraction | IC
- **DEFT2020-D6**: DEFT2020/task_1 | Ex.4 | moy=4.0, scores=[5,2,4,4,5] | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter pendant la durée du traitement." | High inter-annotator variance on near-paraphrase; illustrates uncertainty in clinical STS | OC
- **DEFT2020-D7**: DEFT2020/task_1 | Ex.36 | moy=1.5, scores=[2,4.5,0,1,0] | "Après inspection, elles ont toutes été exclues." | Extreme annotator disagreement (4.5 vs. 0.0); relevant to uncertainty flagging deployment behavior | OC, OF
- **DEFT2020-D8**: DEFT2020/task_1 | Ex.54 | moy=5.0 | "Troubles de l'hémostase à type de maladie de Willebrand (se traduisant par un allongement du TCA, du temps de saignement et une diminution des taux du complexe VIIIC/VWF)." | Specialized hematological terminology; clean standard French; no modality issues | IF, IC
- **DEFT2020-D9**: DEFT2020/task_1 | Ex.1 | moy=0.5 | "Entre Perpignan et Villefranche, il subsiste de très nombreux poteaux caténaires datant des premiers essais en 12 KV 16 2/3 Hz..." | Railway infrastructure content; entirely off-domain for clinical NLP deployment | IC, IO
- **DEFT2020-D10**: DEFT2020/task_1 | Ex.3 | moy=2.1 | "Boris Fiodorovitch Godounov, en russe : Бори́с Фёдорович Годуно́в (v.1551–Moscou, 13 avril 1605)..." | Russian historical figure biography; off-domain and contains Cyrillic script | IC, IO
- **DEFT2020-D11**: DEFT2020/task_1 | Ex.60 | mow=0.8 | "Les Canadiens de Montréal sont une franchise de hockey sur glace professionnel située à Montréal dans la province de Québec au Canada." | Professional hockey franchise; irrelevant to hospital deployment | IC, IO
- **DEFT2020-D12**: DEFT2020/task_2 | T2 Ex.37 | correct_cible=0 | "Lancement du célèbre MMORPG : World of Warcraft." | Video game launch event; entirely off-domain | IC, IO
- **DEFT2020-D13**: DEFT2020/task_2 | T2 Ex.51 | correct_cible=2 | "42 Jeux indémodables ( だれでもアソビ大全 , Daredemo Asobi Taizen au Japon...)" | Japanese script embedded in French text; video game content; off-domain | IC, IO, IF
- **DEFT2020-D14**: DEFT2020/task_1 | schema | — | Fields: id, moy, vote, scores, source, cible | Continuous similarity scoring schema; no entity labels, no ICD-10 classification outputs | OO, OF
- **DEFT2020-D15**: DEFT2020/task_2 | schema | — | Field: correct_cible (0/1/2) | Sentence selection index; not a pathology classification or ICD-10 label | OO, OF
- **DEFT2020-D16**: DEFT2020/task_1 | Ex.36 | moy=1.5, scores=[2,4.5,0,1,0] | "Après inspection, elles ont toutes été exclues." | Annotator disagreement averaged away in scoring; calibration signal lost | OO, OF
- **DEFT2020-D17**: DEFT2020/task_1 | Ex.17 | moy=1.7 | "Les personnes infectées par le virus de l'immunodéficience humaine présentent un risque augmenté de développer une tuberculose (TB) active." | HIV/TB clinical content present as STS pair only; no ICD-10 label, no NER annotation | IO, OC
- **DEFT2020-D18**: DEFT2020/task_1 | Ex.6,7,9,11,12 | moy≈0 | "Certains apiculteurs sélectionnent leurs reines afin de favoriser au mieux la production." | Beekeeping encyclopedia cluster; repeated off-domain topic; no clinical relevance | IC, IO
- **MORFITT-D2**: MORFITT | 2 | [10] | "Dans le cadre d'expériences animales in vivo en aveugle randomisées contrôlées, nous avons étudié les réponses nociceptives induites par une i.pl. de HS chez des souris C57BL/6 (vs CD-1) des deux sexes (n = 240)..." | Structured experimental abstract; not clinical note format — register gap from deployment | IC
- **MORFITT-D3**: MORFITT | 3 | [1] | "Les taux d'AST ( p < 0,001), d'ALT ( p < 0,01), d'amylase ( p < 0,001), de LDH ( p < 0,01), de TNF-α ( p < 0,01), d'IL-1β ( p < 0,001) et d'IL-6 ( p < 0,001)..." | Dense biomedical lab terminology confirming standard French biomedical register | IC
- **MORFITT-D4**: MORFITT | 4 | [8,4] | "La croissance du commerce international a apporté des bénéfices significatifs à l'humanité tout en générant certains coûts. Parmi ceux-ci figure la propagation accrue de parasites et d'agents pathogènes à l'échelle planétaire." | Dual-label (veterinary + genetics) abstract; shows multi-label capability | IO, OO
- **MORFITT-D5**: MORFITT | 5 | [6,8] | "seules des données limitées sont disponibles sur le surfactant chez le cheval... notre objectif était de mener une étude immunocytochimique au microscope optique et électronique sur les poumons normaux du cheval." | Equine veterinary immunology study; off-domain for human hospital deployment | IC, IO
- **MORFITT-D6**: MORFITT | 6 | [6,8,2] | "Le syndrome dysgénésique et respiratoire du porc (SDRP) a un impact énorme sur l'industrie du porc en l'Amérique du Nord." | Porcine veterinary virology abstract; three-label co-occurrence but off-domain | IO, IC
- **MORFITT-D8**: MORFITT | 8 | [0] | "La région du Nord-Ouest de l'Ontario présente un taux élevé et documenté d'infections de la peau et des tissus mous causées par une souche de Staphylococcus aureus méthycillinorésistante d'origine communautaire (SARM-C)." | Canadian infectious disease study (MRSA); relevant microbiology label but non-French geography | IC, OC
- **MORFITT-D9**: MORFITT | 9 | [6,0,8] | "L'otite externe est une maladie multifactorielle fréquente chez le chien... Décrire le microbiote bactérien auriculaire des chiens avec otite externe comparé aux chiens sains." | Canine ear microbiome study; veterinary content off-domain for hospital NLP | IC, IO
- **MORFITT-D10**: MORFITT | 10 | [3] | "L'objectif de cette étude était de documenter les pratiques actuelles de gestion des maladies dans les exploitations apicoles situées au sud-ouest du Québec, Canada." | Canadian beekeeping disease management study; non-Metropolitan French origin | IC, OC
- **MORFITT-D11**: MORFITT | 11 | [1,9] | "Nous rapportons le cas d'une patiente de 71 ans ayant développé un pseudomyxome péritonéal secondaire à un adénocarcinome appendiculaire." | Clinical case abstract with surgery+etiology labels; labels do not map to ICD-10 codes | OO
- **MORFITT-D16**: MORFITT | 16 | [3] | "Nous avons étudié 451 diabétiques et 451 non-diabétiques sans MAC manifeste et avec une perfusion myocardique normale. Le débit sanguin myocardique (DSM) a été calculé sur bases des images TEP/TDM de repos et de stress." | Clinical cardiology study abstract format; not clinical note | IC
- **MORFITT-D17**: MORFITT | 17 | [2] | "L'émergence d'une épidémie d'arbovirose est le plus souvent liée à la convergence d'un ensemble de facteurs... à travers l'étude de l'épidémie de Chikungunya, un alphavirus transmis par Aedes aegypti et Aedes albopictus, survenue dans l'océan Indien en 2004-2007." | Chikungunya virology abstract — tropical pathology relevant to DOM-TOM gap | IO, IC
- **MORFITT-D20**: MORFITT | 20 | [1] | "79 patients au total ont été recrutés à Amman (Jordanie) en 2015." | Jordanian patient population; non-Metropolitan French clinical context | IC, OC
- **MORFITT-D21**: MORFITT | 21 | [1,3,4] | "Bloquer le complément, notamment l'axe C5a-C5aR1, par des thérapies spécifiques représente un espoir thérapeutique dans les formes les plus sévères de la maladie." | COVID-19 immunology; three specialty labels that don't resolve to ICD-10 output | OO
- **MORFITT-D22**: MORFITT | 22 | [11] | "le questionnaire YFAS 2.0-A... peut être utilisée comme équivalent du questionnaire anglais YFAS 2.0 pour étudier l'addiction à la nourriture dans les populations arabophones." | Arabic-population food addiction validation study; non-French population | IC, OC
- **MORFITT-D26**: MORFITT | 26 | [6,8,5] | "Prévalence et caractéristiques morphologiques et moléculaires de Sarcocystis bertrami chez les chevaux en Chine." | Horse parasitology study from China; off-domain for human hospital deployment | IC, IO
- **MORFITT-D29**: MORFITT | 29 | [8] | "La cyclosporine est de plus en plus utilisée en dermatologie des petits animaux." | Small animal dermatology; veterinary content irrelevant to hospital clinical NLP | IC, IO
- **MORFITT-D31**: MORFITT | 31 | [11] | "Un autoquestionnaire envoyé par courrier électronique a été rempli par 191 médecins internes sur 207 travaillant dans différentes spécialités et régions de Riyad." | Saudi Arabian intern survey; non-Metropolitan French context | IC, OC
- **CLISTER-D1**: CLISTER | 7 | 4.0 | "La patiente a été opérée et lors de l'exploration on découvrit qu'il s'agissait d'une tumeur de la veine cave inférieure sus-rénale." | Surgical/oncological clinical case language matching hospital documentation register | IC, IF
- **CLISTER-D2**: CLISTER | 85 | 4.0 | "Le bilan rénal a objectivé une insuffisance rénale avec une créatininémie à 1440 μmol/l, soit une clairance de la créatinine à 6,7 ml/mn/m2, urémie à 2,07 g/l." | Quantified biological workup with clinical abbreviations; representative of standard hospital documentation | IC
- **CLISTER-D3**: CLISTER | 10 | 5.0 | "Une mastectomie était réalisée avec curage axillaire." vs. "Une mastectomie avec curage axillaire ont été réalisés." | Near-identical surgical procedure sentences; tests paraphrase detection for entity normalization | IC
- **CLISTER-D4**: CLISTER | 37 | 5.0 | "Les limites d'exérèse étaient saines." vs. "Les marges chirurgicales étaient saines." | Synonym pair for surgical margin; relevant for clinical entity normalization | IC
- **CLISTER-D5**: CLISTER | 58 | 0.0 | "Concernant la biographie familiale, nous sommes frappés par le nombre de décès par suicides violents (pendaison, noyade, ingestions médicamenteuses)..." | Psychiatric/social history context; shows breadth beyond urology/oncology | IC
- **CLISTER-D6**: CLISTER | 146 | 0.0 | "Cette patiente, suivie en psychiatrie pour des troubles de l'humeur bipolaires, avait arrêté son traitement au lithium (Teralithe LP® 400 mg, deux comprimés par jour)..." | Psychopharmacology context; psychiatric sub-domain coverage | IC
- **CLISTER-D7**: CLISTER | 176 | 0.0 | "Une glande thyroïde hypoplasique a été rapportée à l'échographie cervicale associée à la présence de deux masses..." | Endocrine/imaging case; illustrates specialty breadth | IC
- **CLISTER-D8**: CLISTER | 5 | 2.75 | "Le reste de l'examen échographique ne trouvait aucune autre anomalie." vs. "Le reste de l'examen somatique était sans anomalie." | Intermediate similarity; different exam modality with shared negative finding structure | OO
- **CLISTER-D9**: CLISTER | 75 | 1.25 | "La patiente a bénéficié d'une chimiothérapie adjuvante à base de six cures de paclitaxel et cisplatine." vs. "La patiente avait bénéficié d'une sclérothérapie lors de deux séances..." | Low similarity despite surface parallels; discriminates treatment type | OO
- **CLISTER-D10**: CLISTER | 8 | 1.0 | "Jour 45 - - - - - - - - - 25 μg 0,4 mg" vs. "Jour 53 15,13 12,0 1,58 - - - - - - 25 μg 0,4 mg" | Tabular medication dosing; temporal marker present but content is structured data not free text | IC
- **CLISTER-D11**: CLISTER | 41 | 2.0 | "Métoprolol 50 mg deux fois par jour;" vs. "Metformine 500 mg, 1 comprimé deux fois par jour" | Drug name, dosage, frequency; directly relevant to temporal medication extraction | IC
- **CLISTER-D12**: CLISTER | 93 | 1.0 | "Le patient a été perdu de vue." vs. "Le patient décède à J13." | Outcome divergence (lost to follow-up vs. death on day 13); clinically significant difference potentially underweighted by non-specialist annotators | OC
- **CLISTER-D13**: CLISTER | 126 | 4.0 | "Un patient de 42 ans, a été hospitalisé pour un UB de la main droite." | Clinical abbreviation "UB" (likely Buruli ulcer); domain expertise needed for reliable similarity annotation | OC
- **CLISTER-D14**: CLISTER | 169 | 4.0 | "Craquement douleur oedème + déviation du pénis" vs. "Craquement douleur oedème du pénis et des bourses" | Note-style shorthand, one of few examples resembling informal clinical notation | IC
- **CLISTER-D15**: CLISTER | 191 | 2.0 | "5 mg PO Q 4H PRN X" vs. "10 mg PO Q 4H PRN X X" | Pharmacy shorthand notation (PO=oral, PRN=as needed); structured rather than narrative free text | IC
- **CLISTER-D16**: CLISTER | 9, 29, 55, etc. | various | "lombalgies," "contact lombaire," "PSA," "hématurie," "rein," "uretère" (repeated across many pairs) | High frequency of urological terminology suggesting domain skew toward urology/oncology | IO
- **CLISTER-D17**: CLISTER | 8 | 1.0 | "Jour 45 - - - - - - - - - 25 μg 0,4 mg" | Table row, not a clinical sentence; degenerate STS input | IC
- **CLISTER-D18**: CLISTER | 163 | 5.0 | "Sheldon).\n\nLe patient subissait une chi miothérapie par Méthotrexate - Vinblastine - Endoxan -Cisplatine par voie" | Line-break mid-word artifact ("chi miothérapie"); OCR/PDF extraction noise in source material | IC
- **CLISTER-D19**: CLISTER | 75 | 1.25 | label=1.25 (float) | Non-integer label suggests variable annotator count or averaging artifact; potential label noise at boundary values | OO
- **MANTRAGSC-D1**: fr_emea | d42.u383 | 5 (DISO) | "Même s' il ne permettra pas de guérir la SEP, le traitement par Avonex peut contribuer à éviter que votre état ne s' aggrave." | French EMEA drug label tagging MS (SEP) as disease and Avonex as drug; confirms French biomedical NER coverage | IO, IC
- **MANTRAGSC-D2**: fr_medline | d800967.u1 | 5–6 (DISO), 1 (ANAT) | "Les manifestations oculo-palpébrales du syndrome de Lyell et du syndrome de Stevens-Johnson." | French Medline title labeling eponymous syndromes as DISO; confirms disorder entity coverage | IC, OO
- **MANTRAGSC-D3**: fr_medline | d20337124.u1 | 5 (DISO), 1 (ANAT) | "Paraparésie fébrile chez une Tunisienne : spondylite à cryptocoque avec atteinte médullaire." | French Medline title with disorder/anatomy labeling; mentions North African patient context | IC
- **MANTRAGSC-D4**: fr_emea | d61.u583 | 5–6 (DISO) | "Des symptômes potentiellement liés à l' histamine tels que éruption cutanée étendue, gonflement du visage et/ ou des lèvres, démangeaisons, sensation de chaleur ou difficulté à respirer, ont été rapportés." | Well-formed regulatory French with dense symptom NER; confirms formal register alignment | IF
- **MANTRAGSC-D5**: fr_patents | dEP-2114147-B1.u0020 | 5 (DISO) | "Composition pharmaceutique destinée à être utilisée selon la revendication 18 ou la revendication 19, dans laquelle la maladie ou l' état pathologique est la douleur." | French patent claim tagging disease entity; DISO label on "maladie" and "douleur" | OO
- **MANTRAGSC-D6**: fr_patents | dEP-1835922-B1.u0012 | 2 (CHEM) | "Combinaison selon l' une quelconque des revendications 1 à 7, dans laquelle ladite combinaison comprend 0,25 mg/kg d' agent (a) et 1 mg/kg d' agent (b)." | French patent text with sparse annotation; illustrates critically small training corpus | IC
- **MANTRAGSC-D7**: fr_medline | d5310889.u1 | 5–6 (DISO), 7 (LIVB) | "Accouchement d' une femme atteinte d' une maladie de Willebrand." | Published journal title; highly formal, no clinical shorthand; highlights register gap | IC, IO
- **MANTRAGSC-D8**: fr_emea | d16.u650 | 2 (CHEM), 7 (LIVB) | "Patients de 4 ans et plus dans l' incapacité d' avaler les capsules: la posologie recommandée d' Agenerase solution buvable est de 17 mg (1,1 ml)/ kg trois fois par jour..." | EMEA regulatory language; structured, formal, far from hospital EHR notes | IC
- **MANTRAGSC-D9**: fr_emea | d84.u182 | 13–14 (PROC) | "Traitement En cas d' ingestion récente, l' éventualité de provoquer un vomissement et d' effectuer un lavage gastrique devra être considérée." | Temporal word "récente" present but no temporal NER label exists in Mantra-GSC scheme | OO
- **MANTRAGSC-D10**: fr_medline | d15609920.u1 | 5–6 (DISO) | "Nouveautés dans la dysplasie ventriculaire droite arythmogène." | Single DISO class applied to cardiovascular disorder; no ICD-10 subcategory distinction | OO, OC
- **MANTRAGSC-D11**: de_emea | d42.u384 | 2 (CHEM), 5 (DISO) | "Die Behandlung mit Avonex kann helfen, eine Verschlechterung von MS zu verhindern, jedoch wird die Krankheit nicht geheilt." | German drug label; not relevant to French deployment; illustrates non-French config dominance | IC
- **MANTRAGSC-D12**: fr_medline | d303783.u1 | 1 (ANAT), 11 (PHYS) | "Rôle d' une fraction thymique insoluble dans la différenciation des lymphocytes T." | Anatomical entity labeled without clinical coding authority; illustrates annotation provenance concern | OC
- **MANTRAGSC-D13**: fr_medline | d7569194.u1 | 5–6 (DISO), 7 (LIVB) | "Luxation antérieure ouverte post-traumatique de la hanche chez l'enfant. A propos d'un cas et revue de la littérature." | Metropolitan French orthopedic case; no tropical/overseas pathology signal | IO
- **E3C-D1**: French_clinical | 195 | mixed NER | "Le bilan biologique montrait une cholestase (bilirubine totale a ` 140 mmol/L, bilirubine conjugue à 80 mmol/L, phosphatases alcalines à 700 UI/L) et une cytolyse..." | Dense clinical French with lab values — confirms register alignment with hospital documentation | IC
- **E3C-D2**: French_temporal | 107 | mixed NER | "Il s'agit d'une patiente de 44 ans, sans antécédent médico-chirurgical, qui a présenté depuis un an des céphalées, compliquées 08 mois après de crises d'épilepsies partielles..." | Multi-symptom temporally structured French narrative — confirms temporal extraction alignment | IC, OO
- **E3C-D3**: French_temporal | 107 | TIMEX3 tags | "depuis un an des céphalées, compliquées 08 mois après" (tokens tagged with TIMEX3-type labels) | Temporal duration expressions annotated — supports deployment's temporal entity extraction | OO
- **E3C-D4**: English_clinical | 81 | CLINENTITY | "The presence of terminal spine confirmed Schistosoma haematobium and a diagnosis of schistosomiasis was made." | Tropical parasitic pathology in English config — confirms tropical content structurally absent from French subset | IO, IC
- **E3C-D5**: French_clinical | 54 | B/I CLINENTITY | "Cet aspect évoquait une tumeur solide du péritoine." tokens tagged [0,0,0,0,1,2,0,0,0] | Multi-token pathology span ("tumeur solide") tagged in IOB2 — confirms NER output form alignment | OF, OO
- **E3C-D6**: English_clinical | 4 | B/I CLINENTITY | "As she suffered from acute respiratory distress syndrome and required mechanical ventilation..." tags [0,0,0,0,1,2,2,2,...] | Multi-token disease span annotation in B/I scheme — confirms annotation consistency | OF
- **E3C-D7**: Basque_clinical | 1 | O | "Azken hilabeteetan Ikernek kodeina + ibuprofenoa hartu ditu, baina ez du hobekuntza handirik nabaritu." | Basque language — entirely irrelevant to French deployment context | IO, IC
- **E3C-D8**: Basque_clinical | 13 | O | "Aurrekariak: - Krisi epileptikoa 12 urte zituenean, bere herrialdean tratatua: BOLIBIA." | Basque text referencing Bolivia — not relevant to French metropolitan hospital NLP | IC
- **E3C-D9**: French_clinical | 195 | mixed | "Le bilan biologique montrait une cholestase (bilirubine totale a ` 140 mmol/L..." | Well-formed published case report prose — contrasts with noisy active-hospital EHR shorthand | IC
- **E3C-D10**: French_clinical | 14 (id=253) | all O | "La fonction hépatique s'est améliorée avec un TP à 82% à l'arrêt du traitement." | Standard case report prose — no abbreviations or dictation noise; register mismatch with active EHR | IC
- **E3C-D11**: French_clinical | 2 (id=439) | all O | "La culture a isolé le germe Nocardia asteroides." all tags [0,0,0,0,0,0,0,0,0] | "Nocardia asteroides" (pathogen) not tagged as CLINENTITY — suggests annotation incompleteness | OC
- **E3C-D12**: French_clinical | 12 (id=478) | all O | "Le patient a été mis sous traitement par ciclosporine avec une évolution rapide vers une leucémie aigue myéloblastique." all tags [0,...,0] | Clear pathology and treatment entities untagged — annotation completeness concern | OC
- **E3C-D13**: English_clinical | 6 (id=81) | CLINENTITY | "a diagnosis of schistosomiasis was made" | Tropical disease in English config only; absent from French subset — confirms DOM-TOM pathology gap | IO
- **E3C-D14**: English_clinical | 4 (id=179) | B/I CLINENTITY | "acute respiratory distress syndrome" tagged as single CLINENTITY span, no sub-type | Coarse two-class annotation lacks pathology/anatomy/treatment distinction needed by deployment | OO
- **E3C-D15**: Basque_clinical | 6 (id=80) | O | "." tokens=['.'] ner_tags=[0] | Single-punctuation example — tokenization artifact, quality concern | IC, IF
- **E3C-D16**: Basque_clinical | 9 (id=82) | O | "." tokens=['.'] ner_tags=[0] | Second single-punctuation example — repeated artifact | IC, IF
- **PXCORPUS-D1**: PxCorpus | 75 | medical_prescription | "euh 2 le matin 2 le midi et 2 le soir" | Spoken filler in prescription; illustrates non-formal register | IC, IF
- **PXCORPUS-D2**: PxCorpus | 169 | medical_prescription | "lamotrigine 25 milligrammes euh p/ combien" | Incomplete utterance with filler and truncated word; spoken transcription noise | IC, IF
- **PXCORPUS-D3**: PxCorpus | 3 | none | "/chet" | Single garbled transcription artifact labeled 'none' | IC, IF
- **PXCORPUS-D4**: PxCorpus | 10 | negate | "ne pas tenir compte à midi tous les jours merd/" | Truncated word at end; raw transcription behavior | IC
- **PXCORPUS-D5**: PxCorpus | 5 | medical_prescription | "primperan 10 milligrammes comprimés 1 comprimé en cas de nausée toutes les 8 heures pendant 14 jours" | Dense temporal + drug NER: frequency and duration annotated | IO, OO
- **PXCORPUS-D6**: PxCorpus | 93 | medical_prescription | "becotide 250 milligrammes 2 bouffées à 7 heures 2 bouffées à 11 heures 2 bouffées à 15 heures 2 bouffées à 18 heures pendant 6 mois" | Four specific time-of-day administrations + duration; complex temporal NER | IO, OO
- **PXCORPUS-D7**: PxCorpus | 174 | medical_prescription | "cordarone 3 comprimés par jour pendant 10 jours puis 1 comprimé tous les 2 jours pendant 4 semaines" | Multi-phase temporal prescription with sequential frequency change | IO, OO
- **PXCORPUS-D8**: PxCorpus | 4 | replace | "attention il s'agit de 20 milligrammes et pas 10 milligrammes" | Prescription correction intent; clinically relevant for error detection | IO, OC
- **PXCORPUS-D9**: PxCorpus | 8 | replace | "remplacer 1 comprimé tous les jours par 1 comprimé en cas d'anxiété" | Substitution intent with condition-triggered dosing | IO, OC
- **PXCORPUS-D10**: PxCorpus | 6 | negate | "supprimer à midi tous les jours" | Negation/removal directive for dosing slot | IO, OC
- **PXCORPUS-D11**: PxCorpus | 97 | medical_prescription | "morphine 10 milligrammes toutes les 4 heures pendant 2 mois" | Opioid pain management prescription; broad drug class coverage | IC
- **PXCORPUS-D12**: PxCorpus | 173 | medical_prescription | "aranesp 30 microgrammes 1 injection par semaine en sous-cutanée pendant 4 semaines" | Subcutaneous injectable prescription; route diversity | IC
- **PXCORPUS-D13**: PxCorpus | 190 | medical_prescription | "loxapac ampoules 50 milligrammes 3 ampoules intramusculaire 2 fois par jour pendant 3 jours" | Intramuscular antipsychotic; confirms route coverage | IC
- **PXCORPUS-D14**: PxCorpus | 2 | negate | "c'est 2 pourcent le collyre" | Surface reads like prescription; labeled negate — ambiguity in minority class | OO, OF
- **PXCORPUS-D15**: PxCorpus | buffer | — | negate=11, replace=3 in 500 sampled | Severe class imbalance; majority-class baseline masks minority-class performance | OO, OF
- **PXCORPUS-D16**: PxCorpus | 5 | medical_prescription | NER tags: dose, form, frequency, duration, symptom only | No PATHOLOGY/DIAGNOSIS entity in tag scheme; ICD-10 mapping untestable | IO, OO
- **PXCORPUS-D17**: PxCorpus | 104 | medical_prescription | "en cas d'anxiété" | Anxiety as unlabeled trigger, not classified to ICD-10 axis | IO, OO
- **PXCORPUS-D18**: PxCorpus | 18 | none | "la partie euh posologie est sur 6 ou 8 semaines là il n'est écrit que 8 semaines par contre le qsp 6 semaines a été rajouté en remarque pharmaceutique" | Pharmacist meta-commentary labeled 'none'; heterogeneous class content | OO, OC
- **PXCORPUS-D19**: PxCorpus | 88 | none | "i'll agree come on say avec successes merde je vais roulé faut lui faire un et mettre la rame en mode français" | Mixed French/English system setup dialogue labeled 'none' | OO, IC
- **PXCORPUS-D20**: PxCorpus | 54 | none | "ouah" | Single exclamation labeled 'none'; degenerate example | OO
- **PXCORPUS-D21**: PxCorpus | 33 | none | "perfusion" | Isolated clinical term labeled 'none'; ambiguous classification | OO
- **PXCORPUS-D22**: PxCorpus | 207 | medical_prescription | "teralithe 250 milligrammes / le serveur de dialogue met beaucoup de temps à comprendre votre énoncé veuillez reformuler différemment teralithe 250 milligrammes 2 comprimés matin et soir pendant 1 mois" | System prompt embedded in prescription utterance; corrupts register | IC, IF
- **PXCORPUS-D23**: PxCorpus | 62 | none | "le médicament mais pas le bon le système ne m'a pas compris le bon médicament et le 10 antalvic en gélules" | User commentary about ASR failure; non-clinical register | IC, IF
- **PXCORPUS-D24**: PxCorpus | 34 | medical_prescription | "3 mois" | Duration fragment only; degenerate prescription example | IC
- **PXCORPUS-D25**: PxCorpus | 53 | medical_prescription | "roxithromycine" | Drug name only; no context for full NER | IC
- **PXCORPUS-D26**: PxCorpus | 59 | medical_prescription | "30 jours" | Duration fragment only | IC
- **PXCORPUS-D27**: PxCorpus | 119 | medical_prescription | "tropatepine chloridrate 1o milligrammes 1 comprimé le midi" | "1o" instead of "10" — ASR/OCR artifact in dose quantity | IC
- **PXCORPUS-D28**: PxCorpus | 103 | medical_prescription | "trémétadisine trémétasidine à 20 milligrammes à 3 comprimés par jour pendant 3 semaines" | Probable ASR duplication of drug name | IC
- **DIAMED-D1**: DiaMED | 1 | A00-B99 | "Le test rapide VIH était positif, confirmé par la sérologie VIH avec un taux de CD4 à 27/mm3" | Confirmed HIV infection with CD4 count — supports infectious disease label | OO, IC
- **DIAMED-D2**: DiaMED | 2 | C00-D49 | "L'examen anatomopathologique de la pièce opératoire montrait une prolifération tumorale faite de travées, de cordons" | Histopathological finding of tumoral proliferation — confirms neoplasm label | OO, IC
- **DIAMED-D3**: DiaMED | 9 | I00-I99 | "La troponine I était élevée à quatre fois la normale et les ASAT à 5 fois la normale. La glycémie, l'ionogramme sanguin, l'hémogramme et la créatininémie étaient normaux." | Rich laboratory entities with quantitative values in standard French medical register | IC, IF
- **DIAMED-D4**: DiaMED | 11 | K00-K95 | "L'ionogramme sanguin avait révélé une hypokaliémie à 2,8 mmol/l et une hyponatrémie à 128 mmol/l." | Quantified electrolyte findings — confirms clinical entity density and standard terminology | IC
- **DIAMED-D5**: DiaMED | 8 | H60-H95 | "Le diagnostic d'otite externe maligne avait été posé et une antibiothérapie injectable empirique instaurée" | Ear disease case confirming H60-H95 class representation | IO
- **DIAMED-D6**: DiaMED | 5 | F01-F99 | "Devant le contexte de dépression, la patiente a été adressée en psychiatrie où ce diagnostic a été confirmé" | Psychiatric case confirming mental/behavioral disorder class | IO
- **DIAMED-D7**: DiaMED | 9 | I00-I99 | "Communication interventriculaire ischémique: à propos d'un cas observé dans le service de cardiologie du CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" | Explicitly Burkinabe hospital origin — non-metropolitan French clinical setting | IC, OC
- **DIAMED-D8**: DiaMED | 12 | L00-L99 | "À propos d'un cas clinique … keywords: ['Niamey']" | Niger-based case — sub-Saharan African clinical context, not metropolitan France | IC, OC
- **DIAMED-D9**: DiaMED | 3 | D50-D89 | "keywords: ['Rate', 'abdomen aigu', 'scanner abdominal', 'chirurgie', 'Maroc']" | Moroccan clinical case — North African origin rather than French metropolitan | IC, OC
- **DIAMED-D10**: DiaMED | 11 | K00-K95 | "Le traitement était constitué d'énoxaparine d'antiagrégant plaquettaire, de diurétique de l'anse, de dérivés morphiniques et d'oxygène" | Multi-system case forced into single digestive label — masks multi-morbidity | OO, OF
- **DIAMED-D11**: DiaMED | 1 | A00-B99 | "Maladie de Kaposi à localisation broncho-pulmonaire révélant une infection VIH" | Chapter-level label only; PMSI granular codes (e.g., B21.x) not evaluated | OO
- **DIAMED-D12**: DiaMED | 6 | G00-G99 | "L'examen clinique révélait une paralysie flasque aréflexique avec amyotrophie importante des membres inférieurs. On notait la présence de quelques trépidations épileptoïdes du pied gauche." | Polished academic prose — formal register unlike noisy active-hospital EHR notes | IC
- **DEFT2021-D1**: DEFT2021/cls | 5 (train) | specialities=[12,3,20,4,7,5] | "Un homme de 42 ans était hospitalisé en urgence le 10 décembre 2003 dans le service de gastro-entérologie pour un tableau d'hépatite aiguë" | Multi-morbid hepatology/toxicology/psychiatry case with 6 concurrent MeSH labels | IO, OO
- **DEFT2021-D2**: DEFT2021/cls | 8 (train) | specialities=[20,17,22,13,0,4,19] | "Nous rapportons le cas d'un garçon de huit ans [...] microangiopathie thrombotique secondaire à un syndrome hémolytique urémique (SHU) atypique" | 7-label pediatric multi-morbid case illustrating complex label overlap | IO, OO
- **DEFT2021-D3**: DEFT2021/ner | 7 (train) | TREATMENT+DURATION | "cotrimoxazole pour 10 jours" | Treatment drug with duration span annotated — confirms temporal treatment labeling | IO, OO
- **DEFT2021-D4**: DEFT2021/ner | 55 (train) | TREATMENT+DOSAGE+MODE+FREQUENCY | "Hydrocortisone 300 mg IV immédiatement ; Traitement Hydroxyzine 25 mg par voie orale toutes les 6 heures" | Multiple entity types co-occurring in a single sentence, confirming NER scheme coverage | IO, OO
- **DEFT2021-D5**: DEFT2021/ner | 63 (train) | DATE | "Au jour 42 , une deuxième désensibilisation a eu lieu" | Temporal anchor (relative day) labeled, confirming temporal entity extraction alignment | IO, OO
- **DEFT2021-D6**: DEFT2021/cls | 3 (train) | specialities=[6,14,13,19,4] | "La proarythmie cardiaque constitue l'un des effets indésirables les plus dangereux résultant d'interactions médicamenteuses délétères" | Complex pharmacotherapy reasoning case with rich clinical terminology | IC
- **DEFT2021-D7**: DEFT2021/cls | 5 (train) | specialities=[12,3,20,4,7,5] | "bilan biologique d'entrée révélait une macrocytose avec une thrombopénie, un cytolyse majeure avec des ALAT et des ASAT respectivement à 60 à 450 fois la normale" | Dense laboratory values with quantified severity signals | IC
- **DEFT2021-D8**: DEFT2021/cls | 7 (train) | specialities=[17,4,6] | "B.A., âgé de 20 ans a été admis [...] tuberculose uro-génitale" | Infectious disease + urology multi-specialty case | IO
- **DEFT2021-D9**: DEFT2021/cls | 4 (train) | specialities=[15,4,3] | "un coma inexpliqué, avec un score de Glasgow (GS) à 3/15 [...] injection intraveineuse de poudre 'NRG'" | Emergency medicine + toxicology case | IO
- **DEFT2021-D10**: DEFT2021/ner | 28 (train) | PATHOLOGY (multi-span) | "carcinome urothélial multiple [...] carcinome vésical droit [...] carcinome urétéral multifocal" | Complex oncological case with multiple distinct pathology spans annotated | OO, IF
- **DEFT2021-D11**: DEFT2021/cls | 8 (train) | specialities_one_hot | "[1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0]" | Strictly binary 0/1 label vector — no confidence or soft-label dimension present | OO, OF
- **DEFT2021-D12**: DEFT2021/ner | 56 (train) | PATHOLOGY | "hydatidose" | Parasitic disease labeled, but temperate/Mediterranean — not DOM-TOM tropical pathology | IO, OC
- **DEFT2021-D13**: DEFT2021/cls | 7 (train) | specialities=[17,4,6] | "tuberculose uro-génitale" | Tuberculosis in metropolitan urology context — no DOM-TOM tropical disease specificity | IO
- **DEFT2021-D14**: DEFT2021/ner | 17 (train) | O | "L' ECBU était stérile ." | Standard abbreviation in complete sentence — published case report register, not raw EHR shorthand | IC
- **DEFT2021-D15**: DEFT2021/cls | 9 (train) | specialities=[18,4,13] | "Il s'agit d'une jeune patiente âgée de 18 ans, longiligne et sans antécédents notables admise pour insuffisance rénale chronique terminale secondaire à une néphropathie tubulointerstitielle chronique" | Fully formed syntactic sentence — register cleaner than active hospital notes | IC
- **DEFT2021-D16**: DEFT2021/cls | 3 (train) | specialities=[6,14,13,19,4] | (see D6 excerpt) | Multi-drug cardiac case; annotator PMSI credential unknown — label authority concern | OC
- **DEFT2021-D17**: DEFT2021/cls | 10 (train) | specialities=[3] | "Une femme de 29 ans est victime d'agression sexuelle. Des prélèvements de sérum et d'urine sont réalisés aux fins de 'recherche d'alcoolémie'" | Single-label toxicology case — with 23 axes over 275 cases, some axes have very few positives | IO, OC
- **DEFT2021-D18**: DEFT2021/ner | 23 (train) | O | "Mr ." | Single-token patient initial fragment — no annotatable entity content | IC
- **DEFT2021-D19**: DEFT2021/ner | 31 (train) | O | "O ." | Single-character fragment — degenerate NER example | IC
- **DEFT2021-D20**: DEFT2021/cls | 8 (train) | specialities=[20,17,22,13,0,4,19] | "Au jour 0, le jeune patient reçoit de l'acétaminophène 300 mg par voie orale" | "Acétaminophène" (Quebec French) vs. "paracétamol" (metropolitan French) — minor regional lexical divergence | IC, IF
- **CAS-D1**: CAS/cls | Ex. 3 | neutral | `"l' examen clinique montre un état général conservé ."` | Standard French clinical examination notation | IC, IF
- **CAS-D2**: CAS/cls | Ex. 26 | neutral | `"les constantes hémodynamiques étaient stables mais le bilan biologique mettait en évidence une anémie à 5 , 7 g / 100ml d' hb , une hyponatrémie à 128 meq / l , une acidose métabolique..."` | Dense lab-value notation typical of deployment's severity signal extraction | IC
- **CAS-D3**: CAS/pos | Ex. 7 | — | `"ce patient a présenté de façon brutale , une douleur thoracique aigue à type de constriction associée à une cyanose des extrémités et une hémoptysie de moyenne abondance évoluant vers une syncope ."` | Acute onset clinical narrative with temporal qualifier | IC, IO
- **CAS-D4**: CAS/ner_neg | Ex. 11 | — | `"la dernière prise remontait à sept jours ."` | Relative temporal reference to last medication intake | IC
- **CAS-D5**: CAS/cls | Ex. 29 | neutral | `"le scanner réalisé 1 , 5 mois après , devant la persistance de douleurs abdominales , détectait une image kystique liquidienne de 10 × 7cm accolée à la queue du pancréas"` | Temporal sequencing in imaging diagnosis narrative | IC
- **CAS-D6**: CAS/cls | Ex. 35 | neutral | `"quinze mois après cette cytolyse spontanément résolutive , le bilan hépatique est normal ."` | Follow-up temporal anchor in clinical timeline | IC
- **CAS-D7**: CAS/cls | Ex. 10 | negation | `"les ovaires ne montraient pas d' anomalie ."` | Canonical negation pattern for absent clinical finding | IO, OO
- **CAS-D8**: CAS/cls | Ex. 17 | negation_speculation | `"Les caractères morphologiques et le profil immunohistochimique ne permettaient pas de trancher entre l' hypothèse d' une dissémination péritonéale..."` | Complex combined negation+speculation in oncological differential diagnosis | IO, OC
- **CAS-D9**: CAS/ner_neg | Ex. 14 | tags [0,0,0,1,0,2,2,0] | `"les ovaires ne montraient pas d' anomalie ."` | NER annotation marking negation trigger and scope in IOB2 | OO
- **CAS-D10**: CAS/cls | Ex. 45 | speculation | `"l' atteinte marquée de l' état général , la température à 40 ° c évoquent d' emblée une shigellose ."` | Infectious disease differential (metropolitan pathogen) | IC, IO
- **CAS-D11**: CAS/cls | Ex. 51 | speculation | `"son score chads2 ( insuffisance cardiaque congestive , hypertension , âge ≥ 75 ans , diabète et avc ou accident ischémique transitoire ) est de 3 ."` | Multi-morbidity cardiology risk scoring | IC
- **CAS-D12**: CAS/cls | Ex. 36 | speculation | `"La présence de ces calcosphérites faisait suspecter une carcinomatose péritonéale d' origine ovarienne ."` | Oncological diagnostic reasoning with epistemic hedge | IC
- **CAS-D13**: CAS/pos | Ex. 15 | — | `"Il s' agit d' une patiente âgée de 54 ans ayant des facteurs de risque de transmissions virales hépatiques..."` (full long sequence with pos_tags) | Complex clinical case sentence with full 82-token POS annotation sequence | IO, OF
- **CAS-D14**: CAS/cls | Ex. 38 | neutral | `"depuis hier soir , je suis essouflé , j' ai des frissons , j' ai mal à la poitrine , là en bas à gauche , surtout quand j' inspire à fond ."` | First-person patient narrative with minor spelling error ("essouflé") | IC
- **CAS-D15**: YAML Q42 | — | — | "annotated for POS tagging with 31 classes using automatic annotations through Tagex 3...yielded 98% precision" | Silver-standard label provenance for POS config | OC
- **CAS-D16**: CAS/cls | Ex. 9 | negation_speculation | `"il avait été retrouvé dans la rue , mais il se donne successivement plusieurs professions , semblant ne pas se souvenir de celle qu' il a citée quelques instants avant ."` | Ambiguous negation+speculation requiring expert judgment; no IAA documented | OC
- **CAS-D17**: CAS/cls | Ex. 12 | speculation | `"Cholstat ® 0.1 ."` | Drug name/dosage fragment labeled as speculation with no apparent epistemic marker; annotation rationale opaque | OC, OO
- **CAS-D18**: CAS/ner_neg | Ex. 25 | all-O | `"la coproculture avec ensemencement de milieux sélectifs pour salmonella , shigella et campylobacter spp ."` | Metropolitan enteric pathogen workup; no tropical disease vocabulary present | IO
- **CAS-D19**: HF Metadata | — | — | label_names: ["negation_speculation", "negation", "neutral", "speculation"] | Classification labels measure linguistic modality, not ICD-10 pathology categories | OO
- **CAS-D20**: CAS/cls | Ex. 34 | negation | `"vous êtes appelés au secours d' une infirmière de nuit pour confusion chez un patient bronchopathe chronique , tabagique non sevré à 70 paquets-années ."` | Narrative clinical description; more formal than raw EHR shorthand | IC
- **CAS-D21**: HF Metadata | — | — | buffer: negation_speculation:6, negation:100, neutral:368, speculation:26 | Heavy class imbalance; neutral dominates at ~74% | OO
- **ESSAI-D1**: ESSAI/cls | 1 | negation_speculation | "chimiothérapie à hautes doses avec une combinaison de Busulfan et de Melphalan (BU-MEL) permettra d'obtenir une survie sans événement à 3 ans" | Formal clinical trial protocol language matching deployment register | IC/IF
- **ESSAI-D2**: ESSAI/cls | 10 | negation | "l'objectif de cette étude de recherche clinique est d'évaluer la sécurité d'emploi et l'efficacité de l'avelumab (MSB0010718C) associé aux meilleurs soins palliatifs chez des patients atteints d'un adénocarcinome de l'estomac" | Structured formal French biomedical prose with drug and pathology terms | IC/IF
- **ESSAI-D3**: ESSAI/cls | 6 | negation | "ne présentent pas plus d'effets secondaires dans différents essais cliniques" | Explicit negation of side effects — relevant to safety signal extraction | IO
- **ESSAI-D4**: ESSAI/cls | 36 | speculation | "l'addition de la radiothérapie à la chirurgie semble améliorer le contrôle local des sarcomes rétropéritonéaux" | Speculation marker "semble" on treatment benefit — relevant to claim credibility | IO
- **ESSAI-D5**: ESSAI/cls | 32 | speculation | "le bénéfice de l'association lénalidomide + R-CHOP au rapport au R-CHOP reste à démontrer" | Speculation framing of unproven treatment benefit | IO
- **ESSAI-D6**: ESSAI/ner_neg | 6 | (O-sequence) | "ce traitement qui sera administré toutes les deux semaines sous forme de perfusion d'une heure" | Temporal dosing expression relevant to treatment timeline extraction | IC
- **ESSAI-D7**: ESSAI/ner_spec | 14 | (O-sequence) | "On prévoit de réaliser 6 cycles maximum" | Treatment cycle quantification — temporal entity content | IC
- **ESSAI-D8**: ESSAI/ner_spec | 17 | (O-sequence) | "Des scanners d'évaluation seront réalisés toutes les 8 semaines" | Follow-up scheduling temporal expression | IC
- **ESSAI-D9**: ESSAI/cls | 3 | neutral | "Essai clinique d'immunothérapie évaluant l'association du galunisertib (un facteur de croissance transformant β), avec l'anticorps anti-PD-L1 durvalumab (MEDI4736), dans le cancer du pancréas métastatique" | Rich pathology content labeled only for negation/speculation, not ICD-10 — output ontology mismatch | OO
- **ESSAI-D10**: ESSAI/ner_spec | 10 | (sparse NER) | "traitement par un inhibiteur de PARP, le talazoparib, peut être plus efficace... chez les patients atteints de un cancer du sein métastatique, porteurs de une mutation de BRCA1" | Highly specialized oncogenomics — narrow subdomain not representative of general hospital notes | IC
- **ESSAI-D11**: ESSAI/cls | 20 | speculation | "utilisation de l'oxygène à haut débit humidifié chez les patients immunodéprimés avec un problème respiratoire nécessitant de l'oxygène admis en réanimation" | Clinical trial framing even for ICU content — not raw hospital note register | IC
- **ESSAI-D12**: ESSAI/ner_neg | 11 | NER (sparse) | "en l'absence d'atteinte ganglionnaire chez les femmes ménopausées" (tags: [0,...,2,3,...]) | Only "atteinte ganglionnaire" tagged; annotation completeness and expert authority undocumented | OC
- **ESSAI-D13**: ESSAI/cls | 19 | neutral | "Chaque cycle dure 28 jours" | Trivially neutral sentence — inflates neutral class count, contributing to severe label imbalance | OC
- **ESSAI-D14**: ESSAI/ner_neg | 1–10 | all O | "avec la combinaison gemcitabine + abraxane, chez des patients avec un cancer du pancréas" (and 9 similar) | Consecutive all-zero NER sequences despite clinically relevant content — sparse annotation density | OO


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
  "region": "French Hospital Clinical NLP — Metropolitan France (DrBenchmark)",
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
