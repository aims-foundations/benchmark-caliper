I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Language** is valid for use in **EU Pharmaceutical Regulatory Affairs Professionals (France / EMA-ANSM Zone)**.

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
- **Full Name**: DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Language
- **Domain**: French biomedical NLP evaluation
- **Languages**: fr
- **Porting Strategy**: ground_up
- **Year**: 2023

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
DrBenchmark covers 20 downstream tasks spanning POS tagging, NER, multi-class
classification, multi-label classification, MCQA, and STS [Q1, Q4, Q18]. The
benchmark explicitly positions itself as the first large French biomedical
benchmark [Q83], drawing comparisons to English predecessors such as BLURB
(13 tasks) [Q13], BLUE (10 tasks) [Q14], and CBLUE (8 tasks) [Q15]. Classical
tasks like NER and POS tagging are included alongside more challenging tasks
such as MCQA and multi-label classification [Q20]. Aggregate results are
grouped into five categories: POS, NER, MCQA, MCC, MLC, and STS [Q81].

For the pharmaceutical regulatory deployment context, the task taxonomy
represents a substantial construct underrepresentation gap. No task in the
benchmark is drawn from EU regulatory document genres — SmPCs, patient
information leaflets, CTD modules, or Risk Management Plans are absent from
the inventory. The MCQA task derives from French pharmacy specialization
diploma exams [Q39], which is the closest analog to regulatory knowledge but
still reflects academic clinical pharmacology rather than compliance-oriented
regulatory workflows. The STS tasks are calibrated for general semantic
proximity in clinical case text [Q22] rather than regulatory equivalence
detection. Authors acknowledge that general benchmarks may not adequately
evaluate in-domain model performance [Q10], which is directly applicable to
this deployment gap.

### Input Content
Data sources span scientific literature, clinical trials, clinical cases, and
speech transcriptions [Q19]. Specific corpora include: PMC Open Access
biomedical abstracts (MorFITT) [Q38]; clinical cases from DEFT-2020 [Q21]
and DEFT-2021 [Q24]; clinical trial protocols (ESSAI) [Q43]; drug leaflets
and MEDLINE/EMEA biomedical titles (QUAERO) [Q33, Q34]; multilingual clinical
cases (E3C) [Q29]; drug prescription transcripts (PxCorpus) [Q44]; and
multilingual NER from Medline abstracts, EMEA drug labels, and patents
(Mantra-GSC) [Q40]. The one dataset created specifically for DrBenchmark
(DiaMed) comprises 739 clinical cases from an open-source journal [Q45].
Licensing for all datasets remains per original source terms and the benchmark
does not redistribute them [Q96].

For the regulatory deployment, the most directly relevant content is found in
QUAERO's EMEA drug labels [Q34] and Mantra-GSC's EMEA and patent subsets [Q40].
However, these are limited subsets within a primarily clinical and academic
corpus. The benchmark's instances are drawn from clinical case reports and
research abstracts where the precise phrasings for INNs, ATC codes, excipient
nomenclature, and EMA-templated posology expressions appear differently or less
frequently than in formal regulatory prose. Only Mantra-GSC touches patent
language [Q40], and even then CamemBERT-based models fail entirely on the
patent subset [Q73], signaling that this content domain is an effective blind
spot in the benchmark's coverage. BigBIO covers only four French corpora [Q16],
and the broader absence of French regulatory genre text represents a systematic
input content gap for the deployment use case.

### Input Form
The benchmark operates exclusively on French text [Q31], fully consistent with
the deployment's language requirement. Latin script with standard diacritics
is native to all benchmark source languages, and no script or modality mismatch
is present. Data is distributed via a HuggingFace Datasets-based toolkit with
normalized loading schemes and predefined splits [Q48]. For datasets lacking
predefined splits, a 70/10/20 random partition was applied [Q32, Q42].
Tokenization is documented as a methodological consideration — different models
employ varying tokenization algorithms [Q90], and average sub-token-per-word
ratios vary across models (FlauBERT 1.43, DrBERT-CP 1.90) [Q78]. QUAERO EMEA
documents exceeding standard maximum input sequence lengths were sentence-split
[Q37]. Tokenization fragmentation is noted as playing a minor role in overall
performance [Q80], though this finding may not generalize to the highly
technical nomenclature of regulatory text. Low-resource experiments varied
training data proportions at 25%, 50%, 75%, and 100% [Q68], with validation
and test sets held constant [Q70]. No modality, script, or infrastructure
mismatch concerns apply to this dimension.

### Output Ontology
The benchmark's label taxonomy is calibrated to clinical and biomedical research
norms. POS tagsets use 31 classes for CAS [Q101] and 36 for ESSAI [Q102]. NER
label sets include UMLS Semantic Group categories for QUAERO (GEOG, PHEN, DISO,
ANAT, OBJC, PHYS, PROC, DEVI, CHEM, LIVB) [Q103], clinical/temporal entities
for E3C (CLINENTITY, EVENT, ACTOR, BODYPART, TIMEX3, RML) [Q104], 12 medical
specialty labels for MorFITT [Q105], and UMLS-derived entity sets for Mantra-GSC
[Q106]. Multi-label classification uses 23 MeSH Chapter C axes [Q107]. PxCorpus
NER covers drug-prescription entities including ANATOMY, DATE, DOSAGE, DURATION,
FREQUENCY, MODE, MOMENT, PATHOLOGY, SOSY, SUBSTANCE, TREATMENT, and VALUE
[Q108]. STS scoring uses a 0–5 similarity scale [Q22], with models evaluated via
Spearman correlation and EDRM [Q54].

For the regulatory deployment, the output ontology mismatch is severe across
both NER and STS components. On NER, no label category explicitly represents
INNs as a distinct class, ATC codes, excipient nomenclature, EMA-standard
contraindication qualifiers, or the legally defined entity types in SmPC
sections. The EMEA-sourced labels in QUAERO [Q103] and Mantra-GSC [Q106] use
broad UMLS semantic groups (e.g., CHEM, DEVI) rather than the fine-grained
regulatory distinctions the deployment requires. On STS, the benchmark's scoring
function measures general semantic proximity on clinical case sentence pairs
[Q41, Q54] — fundamentally different from the regulatory equivalence scoring
needed to detect legally significant micro-differences in dose thresholds or
contraindicated-population qualifiers. The benchmark's aggregate task
categorization into POS, NER, MCQA, MCC, MLC, and STS [Q81] does not
distinguish regulatory from clinical sub-tasks, and no model excels across all
tasks [Q57], with MLMs flagged as potentially suboptimal for some task types
[Q87].

### Output Content
Annotation documentation is uneven across the 20 source datasets. DEFT-2021 was
manually annotated for multi-label classification and NER [Q25]. CLISTER STS
annotations were produced by multiple annotators assigning scores from 0 to 5,
then averaged to a floating-point reference [Q41]. DiaMed was annotated by
several annotators including one medical expert using ICD-10 chapter-level
labels, with inter-annotator agreement computed via Cohen's Kappa and Gwet's
AC1 across two sessions of 15 clinical cases [Q45, Q46]. CAS POS annotations
were produced automatically via Tagex 3 and validated against manual annotations
at 98% precision [Q42]. No annotation process documentation references EMA or
ANSM regulatory standards, pharmacovigilance guidelines, or regulatory affairs
expertise as annotator qualifications.

For the regulatory deployment, this is a critical validity risk. The medical
expert involvement in DiaMed [Q45] is the closest analog to regulatory
expertise, but ICD-10 classification reflects clinical coding norms, not
regulatory compliance standards. CLISTER's STS scores measure general semantic
proximity judged by annotators with clinical or research backgrounds [Q41] —
ground-truth labels will systematically diverge from what a regulatory affairs
specialist would judge as equivalent under EMA SmPC guidelines. The absence of
any annotator demographic documentation for TASS 2020 and several other source
datasets further prevents any assessment of regulatory relevance. Nested entity
simplification in QUAERO resulted in annotation losses of 6.06% (EMEA) and
8.90% (MEDLINE) [Q37], which may disproportionately affect fine-grained
regulatory entity boundaries.

### Output Form
Text-based outputs in French are appropriate for the target deployment population
[Q31]. Sequence labeling tasks use SeqEval with IOB2 format, predicting labels
only on the first token of each word to ensure tokenizer-agnostic evaluation
[Q52, Q53]. STS tasks use Spearman correlation and EDRM [Q54]. Classification
tasks are compared against a majority-class baseline [Q56]. All models are
fine-tuned with the same hyperparameters across tasks, with results averaged
over four runs and statistical significance reported via Student's t-test [Q51].
Hyperparameter configurations are documented in the appendix for reproducibility
[Q49, Q99, Q100]. Domain-specialized French biomedical models achieve top
performance on 75% of tasks [Q62], with DrBERT-FS leading on 8 tasks and
DrBERT-CP on 5. Low-resource robustness differs markedly across model
families [Q74]. No output modality or format mismatch concerns apply to the
deployment context — label and score outputs produced by the benchmark's
evaluation protocol are consistent with the system's consumption format.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "It encompasses 20 diversified tasks, including named-entity recognition, part-of-speech tagging, question-answering, semantic textual similarity, and classification." |
| Q2 | 1 | output_form | "We evaluate 8 state-of-the-art pre-trained masked language models (MLMs) on general and biomedical-specific data, as well as English specific MLMs to assess their cross-lingual capabilities." |
| Q3 | 1 | output_form | "Our experiments reveal that no single model excels across all tasks, while generalist models are sometimes still competitive." |
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
| Q16 | 2 | input_content | "To our knowledge, aside the multilingual benchmark BigBIO (Fries et al., 2022) which includes only 4 corpora for French and is initially intended for generative text completion under zero-shot scenario, no large benchmark specialized in the French biomedical field exists." |
| Q17 | 2 | input_ontology | "Our proposed benchmark comprises 20 French biomedical language understanding tasks, one of which is specifically created for this benchmark." |
| Q18 | 2 | input_ontology | "A variety of tasks with different requirements and objectives: Part-of-Speech (POS) tagging, Multi-class, Multi-label and Intent classification, Named-Entity Recognition (NER), Multiple-Choice Question-Answering (MCQA), and Semantic Textual Similarity (STS)." |
| Q19 | 2 | input_content | "A diverse range of data origins: Scientific literature, clinical trials, clinical cases, speech transcriptions, and more as described in Table 2." |
| Q20 | 2 | input_ontology | "Please note that within DrBenchmark, we include classical tasks like NER and POS tagging, as well as more specific and challenging tasks like MCQA and multi-label classification." |
| Q21 | 3 | input_content | "DEFT-2020 (Cardon et al., 2020) contains clinical cases, encyclopedia and drug labels introduced in the 2020 edition of an annual French Text Mining Challenge, called DEFT, and annotated for two tasks: (i) textual similarity and (ii) multi-class classification." |
| Q22 | 3 | output_ontology | "The first task aims at identifying the degree of similarity within pairs of sentences, from 0 (the less similar) to 5 (the most similar)." |
| Q23 | 3 | output_ontology | "The second task consists in identifying, for a given sentence, the most similar sentence among three sentences provided." |
| Q24 | 3 | input_content | "DEFT-2021 (Grouin et al., 2021) is a subset of 275 clinical cases taken from the 2019 edition of DEFT." |
| Q25 | 3 | output_content | "This dataset is manually annotated in two tasks: (i) multi-label classification and (ii) NER." |
| Q26 | 3 | output_ontology | "The multi-label classification task focuses on identifying the patient's clinical profile based on the diseases, signs, or symptoms mentioned in the clinical cases." |
| Q27 | 3 | output_ontology | "The dataset is annotated with 23 axes from Chapter C of the Medical Subject Headings (MeSH)." |
| Q28 | 3 | output_ontology | "The second task involves fine-grained information extraction for 13 types of entities (more detail in Appendix B.7)." |
| Q29 | 3 | input_content | "E3C (Magnini et al., 2020) is a multilingual dataset of clinical cases annotated for the NER task." |
| Q30 | 3 | output_ontology | "It consists of two types of annotations (more detail in Appendix B.4): (i) clinical entities (e.g., pathologies), (ii) temporal information and factuality (e.g., events)." |
| Q31 | 3 | input_form | "While the dataset covers 5 languages, only the French portion is retained for the benchmark." |
| Q32 | 3 | input_form | "Since the dataset does not come with pre-defined subsets, we performed a 70 / 10 / 20 random split, as described in Table 3." |
| Q33 | 3 | input_content | "The QUAERO French Medical Corpus (Névéol et al., 2014), simply referred to as QUAERO in this paper, contains annotated entities and concepts for NER tasks." |
| Q34 | 3 | input_content | "The dataset covers two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE." |
| Q35 | 3 | output_ontology | "10 entity categories corresponding to the UMLS Semantic Groups (Lindberg et al., 1993) were annotated (more detail in Appendix B.3)." |
| Q36 | 3 | output_content | "In total, 26,409 entity annotations were mapped to 5,797 unique UMLS concepts." |
| Q37 | 3 | output_content | "Due to the presence of nested entities in annotations, we simplified the evaluation process by retaining only annotations at the higher granularity level from the BigBio (Fries et al., 2022) implementation, following the approach described in Touchent et al. (2023), which translates into an average loss of 6.06% of the annotations on EMEA and 8.90% on MEDLINE. Additionally, considering that some documents from EMEA exceed the maximum input sequence length that most current language models can handle, we decided to split these documents into sentences." |
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
| Q54 | 6 | output_ontology | "For STS tasks, the models' performance was assessed using two metrics: (1) the Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM), as defined by the original authors of the DEFT-2020 dataset (Cardon et al., 2020)." |
| Q55 | 6 | input_ontology | "In Section 5.1, we compare the results obtained by each model within DrBenchmark, which permits to position a wide range of state-of-the-art models in the biomedical field across various NLP tasks." |
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
| Q73 | 7 | input_content | "However, all the models based on CamemBERT face difficulties in corpora with limited amount of data, such as MantraGSC Patents, where they fail to generate labels other than 'O'." |
| Q74 | 7 | output_form | "On the other hand, in the same low-resource scenarios, CamemBERTa models exhibit greater robustness and achieve superior performance." |
| Q75 | 8 | input_form | "Tokenizers play a crucial role in MLMs by utilizing size-limited vocabularies to split texts into sub-units, aiming to handle out-of-vocabulary (OOV) words." |
| Q76 | 8 | input_content | "Due to variations in the training data, vocabularies differ across different models, as illustrated in Figure 2." |
| Q77 | 8 | input_form | "So far, there has been a prevailing notion in the community that excessive segmentation of words in tokenization leads to a loss of morphological form and semantic meaning, introducing noise and adversely affecting performance (Church, 2020; Hofmann et al., 2021; Bostrom and Durrett, 2020)." |
| Q78 | 8 | input_form | "However, our experiments, as shown in Table 7, reveal that FlauBERT is the model with the least word segmentation (1.43 in average), while DrBERT-CP tends to have the highest average segmentation (1.90 in average)." |
| Q79 | 8 | input_form | "Surprisingly, when comparing the performance of these two models on the benchmark tasks, we observe that DrBERT-CP outperforms FlauBERT on 16 out of the 20 tasks, thus contradicting previous conclusions drawn by the community." |
| Q80 | 8 | input_form | "Yet, tokenization, as it is currently done in MLMs, seems to play a minor role in the performance of systems." |
| Q81 | 8 | input_ontology | "Table 8 summarizes the results obtained on average by the considered MLMs when aggregating the tasks into one of the five designated categories: POS, NER, MCQA, MCC (Multi-class classification), MLC (Multi-label classification), or STS tasks." |
| Q82 | 8 | output_form | "Upon analyzing the average performance by task category, it becomes evident that the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS." |
| Q83 | 9 | input_ontology | "In this paper, we introduced DrBenchmark, the first large language understanding benchmark tailored for the French biomedical domain." |
| Q84 | 9 | input_ontology | "We conducted a qualitative evaluation of 8 state-of-the-art masked language models (MLMs) on this comprehensive benchmark, encompassing 20 diverse downstream tasks." |
| Q85 | 9 | output_form | "Our findings illuminate the limitations of generalist models in tackling complex biomedical tasks, emphasizing the importance of employing domain-specific models to achieve peak performance." |
| Q86 | 9 | output_form | "We have observed that several biomedical tasks in DrBenchmark exhibit relatively poor performance, even when utilizing specialized biomedical models." |
| Q87 | 9 | output_ontology | "We postulate that the models examined in this study, here state-of-the-art MLMs, may not be the most effective choices for specific tasks such as question-answering or multi-label classification." |
| Q88 | 9 | output_form | "The quantitative study we conducted on the PLMs requires further in-depth analysis to comprehend the impact of different parameters." |
| Q89 | 9 | input_form | "Firstly, we investigated the influence of tokenizers based on the average number of sub-tokens they produce per word." |
| Q90 | 9 | input_form | "Various tokenization algorithms are employed, depending on the model under examination." |
| Q91 | 9 | input_content | "The size of the data has not been thoroughly investigated, particularly the significance of the pre-training data size, especially specialized data in the biomedical field." |
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
name: EU Pharmaceutical Regulatory Affairs Professionals (France / EMA-ANSM Zone)
abbreviation: eu-pharma-regulatory-fr
deployment_context:
  system_description: A document management system that applies French biomedical
    NLP models (STS and fine-grained NER) to verify that drug labeling documents meet
    EU regulatory submission standards. The system flags safety-warning inconsistencies
    and extracts regulatory entities to determine whether documentation requires manual
    revision before official submission.
  benchmark_being_assessed: drbenchmark
  assessment_purpose: Validity analysis of DrBenchmark as a proxy evaluation for NER
    and STS performance in EU pharmaceutical regulatory document processing
geography:
  primary_jurisdiction: France (ANSM — Agence nationale de sécurité du médicament
    et des produits de santé)
  supranational_jurisdiction: European Union regulatory zone (EMA — European Medicines
    Agency)
  relevant_regulatory_bodies:
  - EMA (European Medicines Agency)
  - ANSM (Agence nationale de sécurité du médicament et des produits de santé)
  sub_national_variation: None meaningful. Regulatory submission standards are nationally
    and supranationally harmonized; no province- or region-level procedural variation
    applies to this population.
  key_regulatory_reference_locations:
  - Amsterdam (EMA headquarters post-Brexit)
  - Paris / Saint-Denis (ANSM headquarters)
target_population:
  description: Regulatory affairs specialists, pharmacologists, and legal experts
    working at pharmaceutical companies or government health agencies within the EU
    regulatory zone. These professionals prepare, review, and submit drug labeling
    documents (SmPCs, patient information leaflets, patents, CTD modules) for official
    authorization. They are a highly specialized professional cohort, distinct from
    clinical NLP annotators or biomedical researchers.
  roles:
  - Regulatory affairs specialists
  - Pharmacologists (with regulatory focus)
  - Legal experts / regulatory counsel
  - Medical writers (regulatory documentation)
  organizational_settings:
  - Pharmaceutical companies (large multinational and mid-size)
  - Contract Research Organizations (CROs) with regulatory services
  - Government health agencies (ANSM, national competent authorities)
  - EMA scientific committees and working parties
  professional_training_norms: EU regulatory submissions require deep familiarity
    with EMA guidelines (SmPC guideline, QRD template, ICH CTD format), ANSM circulars,
    and EU pharmaceutical legislation. Annotation norms derive from these legal-regulatory
    frameworks, not clinical or academic biomedical conventions.
  annotation_expertise_gap: Benchmark ground-truth labels produced by clinical or
    biomedical NLP annotators are expected to diverge systematically from this population's
    regulatory judgments on borderline entity and equivalence cases.
languages:
  primary: French (formal, legally constrained regulatory prose)
  register: Regulatory French — template-driven, standardized, legally binding. Distinct
    from clinical French (hospital records), research French (academic abstracts),
    and spoken medical French (prescription transcripts). Characterized by EMA QRD-template
    phrasing, INN-based nomenclature, and ANSM-prescribed contraindication formulations.
  secondary:
  - English (EMA working language; many source guidelines and reference documents
    are English)
  - Latin (pharmaceutical nomenclature, INN stems)
  code_switching_notes: Regulatory French documents frequently embed English-origin
    acronyms (SmPC, CTD, INN, ATC), Latin nomenclature, and numeric posology expressions.
    NLP tokenization must handle this mixed register.
  dialectal_variation: None meaningful within the professional regulatory register;
    standardization is enforced by EMA QRD templates and ANSM requirements.
writing_systems:
  scripts:
  - Latin alphabet with standard French diacritics (é, è, ê, à, â, î, ô, û, ç, œ,
    æ)
  special_notation:
  - Numeric posology expressions (e.g., '500 mg', '2 fois par jour', dose-range brackets)
  - INN stem suffixes and prefixes (IUPAC-derived, often Latinate)
  - ATC code alphanumeric strings (e.g., N02BA01)
  - Chemical formula notation for excipients
  note: No script mismatch with benchmark. However, highly technical nomenclature
    strings (INNs, ATC codes, excipient names) may fragment anomalously under standard
    biomedical tokenizers trained on clinical prose.
document_genres:
  central_to_deployment:
  - genre: Summary of Product Characteristics (SmPC / RCP in French)
    description: EMA-mandated structured label covering indications, posology, contraindications,
      special warnings, interactions, fertility/pregnancy/lactation, undesirable effects,
      pharmacological properties. Highly formulaic; specific section headings are
      legally prescribed.
    benchmark_coverage: Absent as a primary task source. QUAERO EMEA drug labels [Q34]
      and Mantra-GSC EMEA subsets [Q40] provide partial overlap, but as minority subsets
      within a clinical-dominated corpus.
    coverage_risk: HIGH
  - genre: Patient Information Leaflet (PIL / Notice patient)
    description: Consumer-facing regulatory document. Simplified language, but legally
      constrained phrasing for safety warnings and contraindications. EMA QRD template
      governs structure.
    benchmark_coverage: QUAERO includes 'drug leaflets' from EMEA [Q34], representing
      the closest benchmark analog. Proportion and representativeness relative to
      full PIL genre require verification.
    coverage_risk: MEDIUM-HIGH
  - genre: Common Technical Document (CTD) modules
    description: ICH-harmonized dossier format for marketing authorization applications.
      Highly structured; modules 1–5 cover administrative, quality, safety, efficacy,
      and clinical data. Regulatory-specific entity usage throughout.
    benchmark_coverage: Not represented in DrBenchmark task inventory.
    coverage_risk: HIGH
  - genre: Pharmaceutical patent claims
    description: Legally structured claims with distinct entity conventions (compound
      claims, method-of-use claims, Markush structures). Syntactically and semantically
      distinct from clinical or research prose.
    benchmark_coverage: Mantra-GSC patents subset [Q40] exists but CamemBERT-based
      models fail entirely on it [Q73], indicating an effective blind spot.
    coverage_risk: HIGH
  - genre: EU Risk Management Plan (RMP)
    description: Pharmacovigilance document detailing safety concerns and risk minimization
      measures. Combines regulatory and clinical language; safety warning phrasing
      is legally significant.
    benchmark_coverage: Not represented in DrBenchmark task inventory.
    coverage_risk: HIGH
  supplementary_layers_in_deployment: For highly specialized formats like CTD modules,
    the production system applies regulatory-specific templates as a supplementary
    layer on top of the foundational NLP model.
regulatory_framework:
  primary_legislation: 'Currently applicable legislation: Directive 2001/83/EC (as
    amended) and Regulation (EC) No 726/2004. These are being revised under a comprehensive
    reform package: the European Commission proposed new legislation on 26 April 2023
    (COM(2023) 192 and 193); the European Parliament adopted its position in April
    2024; trilogue negotiations ran through late 2025 and a provisional agreement
    was reached on 11 December 2025. The new legislation will replace Directive 2001/83/EC
    and Regulation 726/2004 entirely, but formal adoption and entry into force remain
    pending as of April 2025. Deployments should continue to operate under the current
    2001/83/EC / 726/2004 framework until the new legislation is formally adopted
    and transition deadlines set.

    Sources: EMA reform page — [WEB-1];
    European Parliament Legislative Train — [WEB-2]'
  ema_guidelines_in_scope:
  - 'SmPC guideline (EC Notice to Applicants, Volume 2C, Guideline on Summary of Product
    Characteristics, revision 2 — reference URL: [WEB-3];
    currently the operative content guideline for SmPC drafting, complemented by the
    EMA SmPC Advisory Group implementation plan — [WEB-4])'
  - 'QRD template for human medicines — current operative version is v10.4 (February
    2024), implementing Regulation (EU) 2023/1182 safety-feature requirements. QRD
    v11 draft was released for public consultation (comments due 31 August 2025);
    v11 is not yet in force. Source: EMA QRD templates page — [WEB-5];
    v10.4 template PDF — [WEB-6]'
  - 'ICH E2C pharmacovigilance guideline — [NEEDS VERIFICATION — deferred: below search
    budget; guideline reference number and current revision not confirmed in searches
    conducted]'
  - 'ICH M4 CTD guideline — [NEEDS VERIFICATION — deferred: below search budget; current
    version not confirmed in searches conducted]'
  ansm_specific_requirements: 'ANSM imposes national-specific requirements on top
    of EMA QRD templates for MRP/DCP submissions. For initial MAs, companies must
    submit translations using ANSM''s ''Feuille de style'' template form, which aligns
    with the current QRD template but includes national additions. French-language
    excipient wording must conform to the French version of the EC guideline on excipients
    labeling. The SmPC and PIL text is harmonized EU-wide across member states; however,
    each member state (including France) may require additional national information
    in the ''blue box'' on outer packaging, which can include legal status, pricing/reimbursement,
    MA number, and local representative details. ANSM also runs a national promotional
    materials visa process (four slots per year, two-month review window) that is
    France-specific and separate from EMA procedures.

    Sources: PharmaLex analysis of French regulatory affairs — [WEB-7];
    ANSM national translation recommendations document (June 2022) — [WEB-8];
    CMDh Blue Box requirements (May 2023) — [WEB-9]'
  inn_nomenclature_authority: WHO International Nonproprietary Names (INN) programme;
    French rDCI (dénomination commune internationale recommandée) usage governed by
    ANSM
  atc_classification_authority: WHO Collaborating Centre for Drug Statistics Methodology
    (ATC/DDD system)
  annotation_ground_truth_source: Regulatory affairs specialists and legal experts
    applying EMA SmPC guidelines and ANSM circulars — not clinical annotators
entity_types_in_scope:
  description: The following entity types are the primary extraction targets of the
    deployment system. These are the regulatory-specific entity categories against
    which benchmark NER label coverage must be assessed.
  primary_regulatory_entities:
  - entity_type: International Nonproprietary Name (INN)
    notes: Core active substance identifier. Precise string matching critical; benchmark
      CHEM/SUBSTANCE categories are proxies but do not distinguish INNs from other
      chemical entities.
    benchmark_analog: PxCorpus SUBSTANCE [Q108], QUAERO CHEM [Q103], Mantra-GSC CHEM
      [Q106] — all partial, non-equivalent
  - entity_type: ATC code
    notes: Alphanumeric classification code; distinct from drug name. No DrBenchmark
      dataset includes ATC codes as annotated entities — the NER label sets (QUAERO
      UMLS groups [Q103], Mantra-GSC UMLS groups [Q106], PxCorpus entities [Q108])
      contain no ATC-code category, and the benchmark paper makes no mention of ATC
      annotation. This is a confirmed full gap.
    benchmark_analog: No direct analog identified in DrBenchmark label sets
  - entity_type: Excipient name / excipient with known effect
    notes: EMA requires labeling of excipients with known effects (e.g., lactose,
      benzalkonium chloride). Nomenclature follows Ph.Eur. or INCI standards. EMA
      QRD appendices specify mandatory wording for excipients with known effects;
      ANSM requires French-language excipient wording to match the EU Commission excipients
      guideline annex.
    benchmark_analog: CHEM grouping in QUAERO/Mantra-GSC may capture some, but without
      excipient-specific distinction
  - entity_type: Posology expression (dose, frequency, duration, route)
    notes: EMA-templated phrasing is legally precise. PxCorpus covers DOSAGE, FREQUENCY,
      DURATION, MODE [Q108] from prescription transcripts — register and context differ
      from SmPC posology sections.
    benchmark_analog: PxCorpus NER [Q108] — closest but register mismatch (spoken
      prescription vs. written regulatory)
  - entity_type: Contraindication qualifier (population, condition, dose threshold)
    notes: Micro-differences in population qualifiers (e.g., 'enfants de moins de
      2 ans' vs. 'enfants de moins de 6 ans') are legally significant. Benchmark STS
      scores these as high similarity; deployment must flag as non-equivalent.
    benchmark_analog: No direct analog in NER label sets; STS calibration is fundamentally
      misaligned
  - entity_type: Special warning / precaution statement
    notes: SmPC Section 4.4 phrasing; EMA-templated. Semantic equivalence scoring
      must detect legally significant micro-differences.
    benchmark_analog: STS tasks use general clinical sentence similarity — not calibrated
      for regulatory equivalence
  - entity_type: Therapeutic indication
    notes: Approved indication text; legally binding. May overlap with DISO/PROC UMLS
      categories but at higher specificity.
    benchmark_analog: DISO in QUAERO [Q103], CLINENTITY in E3C [Q104] — coarse approximations
  - entity_type: Marketing Authorization Number
    notes: No DrBenchmark dataset includes EU/national marketing authorization numbers
      as annotated entities. The benchmark's NER label sets (QUAERO, Mantra-GSC, PxCorpus,
      E3C, DEFT-2021) are confirmed to cover UMLS semantic groups, ICD-10 categories,
      and clinical/prescription entities only — no identifier-type annotation for
      MA numbers appears in any dataset description. This is a confirmed full gap.
    benchmark_analog: No identified analog
sts_calibration_requirements:
  deployment_scoring_rule: 'Regulatory equivalence scoring: minor lexical differences
    in dose thresholds, contraindicated-population qualifiers, or safety warning phrasing
    are treated as critical mismatches rather than near-synonymy. General semantic
    proximity is a baseline floor, not the decision criterion.'
  decision_threshold_behavior: Borderline or high-stakes inconsistencies flag documents
    for human review. Automatic rejection is not used.
  benchmark_sts_calibration: DrBenchmark STS tasks (CLISTER, DEFT-2020) use a 0–5
    general semantic proximity scale on clinical case sentence pairs, evaluated via
    Spearman correlation and EDRM [Q41, Q54]. No rubric references legally significant
    micro-differences.
  mismatch_severity: HIGH — the benchmark's STS scoring function is calibrated for
    a fundamentally different decision rule than the deployment requires
  regulatory_sts_benchmark_search_result: '[NOT FOUND — searched for French regulatory
    STS benchmarks, NLP evaluation of SmPC safety-warning equivalence, and pharmaceutical
    labeling paraphrase detection; no published benchmark or evaluation dataset specifically
    targeting regulatory equivalence scoring in French pharmaceutical documents was
    identified. This is a confirmed gap in the literature: no study providing ground-truth
    STS scores calibrated to EMA/ANSM regulatory equivalence standards exists as of
    the searches conducted (April 2025). The closest related work is the MultiADE
    benchmark for adverse drug event extraction (arXiv:2405.18015), which does not
    address STS or French regulatory text.]'
annotation_norms:
  deployment_ground_truth_authority: EMA SmPC guidelines, ANSM circulars, EU pharmaceutical
    legislation, and regulatory affairs expert judgment
  benchmark_annotator_profile: Clinical or biomedical NLP specialists; no documented
    regulatory affairs expertise or EMA/ANSM guideline training in any DrBenchmark
    source dataset [Q25, Q41, Q42, Q45]
  expected_disagreement_pattern: 'Systematic divergence on borderline cases: biomedical
    annotators prioritize clinical relevance; regulatory experts apply rigid legal
    constraints. Core technical entity agreement expected; borderline entity boundary
    and equivalence judgment agreement expected to be low.'
  inter_annotator_agreement_reference: DiaMed IAA documented (Cohen's Kappa, Gwet's
    AC1) [Q45, Q46] — but using ICD-10 clinical coding norms, not regulatory norms.
    No IAA data exists for regulatory-expert annotation of any benchmark subset.
  nested_entity_loss: QUAERO annotation simplification resulted in 6.06% entity loss
    (EMEA) and 8.90% (MEDLINE) [Q37]; disproportionate impact on fine-grained regulatory
    entity boundaries is plausible but unverified.
  independent_benchmark_nlp_french_clinical_ner: 'A March 2024 arXiv evaluation of
    French clinical NER (Bannour et al., arXiv:2403.19726) benchmarks CamemBERT-bio
    and DrBERT against general French models on QUAERO, E3C, and DEFT corpora. It
    confirms that nested entity handling was flattened in prior evaluations (including
    DrBenchmark) and that training data size has more impact on NER performance than
    model choice. All evaluated corpora are clinical; no regulatory document genre
    is included. This corroborates the clinical-only scope of existing French biomedical
    NLP benchmarks.

    Source: arXiv:2403.19726 — [WEB-10]'
infrastructure_notes:
  deployment_modality: Text-based document processing pipeline; no speech, image,
    or multimodal input. Inputs are structured regulatory documents in French.
  language_model_format_compatibility: HuggingFace Datasets toolkit with IOB2 / SeqEval
    for NER, Spearman/EDRM for STS — fully compatible with deployment consumption
    format [Q48, Q52, Q54].
  tokenization_risk: Highly technical nomenclature strings (INN stems, ATC alphanumeric
    codes, excipient IUPAC names, numeric posology expressions) may fragment anomalously
    under tokenizers trained on clinical prose. DrBERT-CP has highest average sub-token
    ratio (1.90) [Q78]; impact on regulatory entity spans unverified.
  sequence_length_handling: QUAERO EMEA documents exceeding max input length were
    sentence-split [Q37]; similar handling required for long CTD module sections in
    deployment.
  it_environment: '[NEEDS VERIFICATION — deferred: below search budget; on-premises
    vs. cloud deployment modality is not determinable from public sources and must
    be confirmed with the deploying organization directly]'
  data_residency_requirements: 'Processing unpublished regulatory submission documents
    in France is subject to multiple overlapping requirements: (1) GDPR (Regulation
    (EU) 2016/679), directly applicable in France; (2) French Loi Informatique et
    Libertés (as amended in 2018); (3) French Hébergeur de Données de Santé (HDS)
    certification — any entity hosting or processing health data in France must use
    an HDS-certified provider, including cloud services and IT platforms. Note: drug
    labeling documents are not patient health data in the clinical sense, but the
    regulatory submission context and the French Public Health Code (Code de la Santé
    Publique) may bring submission-related data into scope depending on content. Additionally,
    regulatory submission dossiers contain commercially confidential information (trade
    secrets, proprietary formulation data) that is protected separately under EU pharmaceutical
    confidentiality rules and contractual obligations, irrespective of GDPR. Cloud
    deployment outside the EEA would require GDPR Chapter V transfer mechanisms (SCCs
    or equivalent).

    Sources: HDS certification framework — [WEB-11];
    GDPR transfer framework — [WEB-12]'
cultural_and_professional_norms_notes: '- Regulatory affairs is a compliance-first
  professional culture; precision and legal defensibility take precedence over general
  biomedical relevance

  - EMA and ANSM operate within EU administrative law; document language is governed
  by official template constraints, not stylistic convention

  - Professional consensus on borderline regulatory questions is established through
  EMA working party guidance and CHMP opinions, not clinical judgment

  - The population is accustomed to version-controlled, auditable document workflows;
  NLP outputs entering this workflow must meet traceability standards

  - French regulatory professionals interact with both ANSM (national) and EMA (supranational)
  submission tracks. For centrally authorised products, the national phase at ANSM
  occurs after CHMP opinion and includes a France-specific ''blue box'' packaging
  step and promotional visa process that are purely national. For MRP/DCP products,
  the CMDh annotated QRD template (updated March 2024) applies. These procedural bifurcations
  create register differences (EMA English-first vs. ANSM French-translated) that
  are relevant to NLP model training scope.

  Sources: PharmaLex — [WEB-7];
  CMDh QRD template page — [WEB-13]

  - No significant cultural sensitivity concerns beyond standard professional norms;
  domain sensitivity is legal/commercial rather than social'
domain_specific_notes:
  regulatory_vs_clinical_nlp_gap: 'The core validity risk for DrBenchmark in this
    deployment is genre and register mismatch: the benchmark is calibrated to clinical
    and research French, while the deployment operates on regulatory French. These
    registers differ in vocabulary standardization, sentence structure, template adherence,
    and the legal weight attached to specific phrasings.'
  ema_ansm_harmonization: 'EMA QRD templates create cross-EU standardization in SmPC
    and PIL structure. ANSM adds French-specific national requirements: a dedicated
    ''Feuille de style'' translation template (aligning with current QRD version),
    mandatory French-language excipient wording per the EC excipients guideline, and
    a ''blue box'' for packaging information. The core SmPC and PIL text content is
    harmonized; the blue-box and promotional materials are national-level additions
    handled separately. The current QRD template v10.4 (February 2024) implements
    Regulation (EU) 2023/1182 safety-feature requirements; QRD v11 is in public consultation
    (deadline August 2025) and not yet operative.

    Sources: EMA QRD templates — [WEB-5];
    ANSM translation recommendations — [WEB-8]'
  patent_language_specificity: 'Patent claim language (Markush structures, ''comprising''
    / ''consisting of'' legal terms, independent and dependent claim numbering) is
    syntactically and semantically distinct from all other document genres in the
    deployment. Benchmark patent coverage exists only in Mantra-GSC [Q40], where CamemBERT
    models fail entirely [Q73]. A 2025 arXiv paper on NLP tools for pharmaceutical
    manufacturing (arXiv:2504.20598) confirms that pharmaceutical patents ''are written
    in such a way that their procedures are difficult to reproduce'' and do not have
    well-defined sections, and that NER models developed for biomedical contexts have
    not been designed for secondary pharmaceutical processing text. This corroborates
    the patent-as-blind-spot assessment.

    Source: arXiv:2504.20598 — [WEB-14]'
  pharmacovigilance_signal_detection: Safety warning equivalence (OO dimension) is
    the highest-stakes output of the system; false equivalence between non-equivalent
    warnings could result in non-compliant submissions. This is the primary driver
    of the regulatory-equivalence STS requirement.
  legal_status_of_nlp_output: NLP outputs are used to flag documents for human review,
    not to make final regulatory decisions. Human review by qualified regulatory affairs
    specialists is the final gate. This limits but does not eliminate the risk of
    benchmark-deployment mismatch propagating into compliance errors.
  eu_pharma_legislation_reform_impact: 'The provisional agreement reached 11 December
    2025 on new EU pharmaceutical legislation (replacing Directive 2001/83/EC and
    Regulation 726/2004) will eventually affect SmPC and labeling requirements, QRD
    template evolution, and submission procedures. However, formal adoption and transition
    timelines have not yet been published. For deployment planning purposes, the current
    legislative framework remains operative. Tracking of the new legislation''s labeling
    and submission provisions is recommended once formally adopted.

    Sources: EMA reform page — [WEB-1];
    European Parliament Legislative Train — [WEB-2]'
net_new_fields:
  independent_french_clinical_ner_benchmark_2024:
    description: 'Bannour et al. (arXiv:2403.19726, March 2024) provides an independent
      evaluation of French biomedical NER models (CamemBERT-bio, DrBERT, CamemBERT,
      FlauBERT, FrALBERT, mBERT) on three publicly available clinical French corpora.
      Key finding relevant to this deployment: prior evaluations including DrBenchmark
      flattened nested entities in QUAERO by keeping only coarse entities; this paper
      attempts extrinsic evaluation and confirms training data size is the dominant
      factor in NER performance across corpora. No regulatory document genre is included.
      The paper is useful as an independent corroboration that existing French biomedical
      NLP benchmarks are clinically scoped only.

      Source: arXiv:2403.19726 — [WEB-10]'
    validity_relevance: 'Corroborates OC gap: nested entity loss in QUAERO EMEA subset
      affects regulatory entity boundary precision; confirms no existing benchmark
      covers regulatory French NER.'
  qrd_v11_revision_status:
    description: 'EMA launched revision of the QRD template in September 2023, primarily
      to improve package leaflet structure. QRD v11 draft was published for public
      consultation; comments were due 31 August 2025. QRD v10.4 (February 2024) remains
      the current operative template implementing Regulation (EU) 2023/1182 safety-feature
      requirements. Deployments should anticipate a v11 transition affecting PIL structure
      but not expected to materially alter SmPC section 4 safety-warning phrasing.

      Source: EMA QRD templates page — [WEB-5]'
    validity_relevance: Signals ongoing template evolution; NLP models trained on
      pre-v11 SmPC/PIL text may require revalidation after v11 adoption, particularly
      for PIL sections.
  hds_certification_france:
    description: 'Health data hosted or processed in France must use an HDS (Hébergeur
      de Données de Santé) certified provider under the Code de la Santé Publique.
      This applies to cloud services, IT platforms, and data centers. Whether unpublished
      regulatory submission dossiers (as opposed to patient health data) trigger HDS
      certification obligations depends on document content and legal interpretation;
      this requires legal review by the deploying organization.

      Source: InCountry HDS overview — [WEB-11]'
    validity_relevance: Shapes IT environment choices (on-premises vs. EU-hosted cloud);
      affects deployment architecture decisions flagged in infrastructure_notes.
flagged_gaps_for_web_search:
- gap_id: 1
  priority: HIGH
  description: Regulatory document genre coverage in DrBenchmark
  search_target: French biomedical NLP benchmark SmPC Summary of Product Characteristics
    EU regulatory NER evaluation dataset QUAERO EMEA subset size proportion
  resolution_status: SEARCHED — confirmed full gap. No DrBenchmark task draws primary
    instances from SmPCs, CTD modules, RMPs, or PILs as distinct genre sources. QUAERO
    EMEA and Mantra-GSC EMEA are minority subsets within clinical-dominated corpus.
    Independent 2024 evaluation (arXiv:2403.19726) corroborates clinical-only scope
    of all existing French biomedical NLP benchmarks.
- gap_id: 2
  priority: HIGH
  description: Regulatory-specific entity type coverage (INNs, ATC codes, excipients,
    EMA posology)
  search_target: INN ATC code NER dataset French regulatory NLP excipient contraindication
    named entity recognition benchmark DrBenchmark PxCorpus QUAERO entity taxonomy
  resolution_status: SEARCHED — confirmed full gap for ATC codes and MA numbers; confirmed
    partial gap for INNs and excipients (subsumed under CHEM category). No published
    French regulatory NER benchmark with INN, ATC, excipient-specific, or MA-number
    entity categories was identified.
- gap_id: 3
  priority: HIGH
  description: STS scoring calibration for regulatory equivalence vs. general semantic
    proximity
  search_target: regulatory equivalence semantic textual similarity scoring EMA SmPC
    safety warning NLP evaluation metric CLISTER DEFT scoring rubric annotator instructions
  resolution_status: SEARCHED — confirmed full gap. No French regulatory STS benchmark
    or scoring rubric calibrated to EMA/ANSM equivalence standards was found. No published
    study on SmPC safety-warning paraphrase detection in French was identified.
- gap_id: 4
  priority: HIGH
  description: Annotator population for NER and STS ground-truth labels and alignment
    with EMA/ANSM standards
  search_target: regulatory affairs annotator pharmaceutical NLP annotation EMA ANSM
    ground truth label clinical vs regulatory expert agreement DrBenchmark CLISTER
    DiaMed annotator qualifications
  resolution_status: 'SEARCHED — confirmed full gap. No DrBenchmark dataset documents
    regulatory affairs specialists or EMA/ANSM-trained annotators. The gap is definitional:
    no published French biomedical NLP benchmark uses regulatory annotation norms.'
- gap_id: 5
  priority: MEDIUM-HIGH
  description: ANSM-specific derogations or additions to EMA QRD templates affecting
    French regulatory French register
  search_target: ANSM circulars French SmPC QRD template national derogations EMA
    harmonization pharmaceutical labeling France 2023 2024
  resolution_status: 'RESOLVED — ANSM requirements confirmed: French-specific ''Feuille
    de style'' translation template, French-language excipient wording per EC excipients
    guideline, blue-box packaging additions, and national promotional materials visa
    process. Core SmPC/PIL text is harmonized; national additions are structurally
    distinct. Sources: PharmaLex — [WEB-7];
    ANSM recommendations document — [WEB-8]'
- gap_id: 6
  priority: MEDIUM-HIGH
  description: Patent and legal text NLP model performance on French pharmaceutical
    patent claims
  search_target: patent NLP French NER biomedical pharmaceutical claim entity recognition
    benchmark evaluation Mantra-GSC CamemBERT failure patent subset
  resolution_status: SEARCHED — corroborated. arXiv:2504.20598 (2025) independently
    confirms that pharmaceutical patent text has distinct NLP challenges (procedure
    obfuscation, non-standard sectioning) and that biomedical NER models are not designed
    for this genre. No new French pharmaceutical patent NER benchmark was identified.
- gap_id: 7
  priority: MEDIUM
  description: Current EMA SmPC guideline version and QRD template version numbers
  search_target: EMA SmPC guideline current version 2024 QRD template human medicines
    current version
  resolution_status: 'RESOLVED — QRD template current operative version: v10.4 (February
    2024). QRD v11 in public consultation (comments due August 2025), not yet in force.
    SmPC content guideline: EC Notice to Applicants Volume 2C, revision 2 (reference
    URL confirmed). Sources: EMA QRD templates page — [WEB-5];
    QRD v10.4 template — [WEB-6]'
- gap_id: 8
  priority: MEDIUM
  description: EU pharmaceutical legislation reform status and applicability to NLP-assisted
    regulatory workflows
  search_target: EU pharmaceutical legislation reform 2023 2024 Directive 2001/83/EC
    revision Regulation 726/2004 update digital submission NLP
  resolution_status: 'RESOLVED — Commission proposed reform on 26 April 2023; European
    Parliament adopted position April 2024; trilogue concluded with provisional agreement
    11 December 2025. New legislation will replace Directive 2001/83/EC and Regulation
    726/2004 entirely. Formal adoption and entry into force pending; current framework
    remains operative for all active submissions. No specific digital submission or
    NLP provisions identified in reform summaries. Sources: EMA — [WEB-1];
    European Parliament — [WEB-2]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.ema.europa.eu/en/about-us/what-we-do/reform-eu-pharmaceutical-legislation |
| WEB-2 | https://www.europarl.europa.eu/legislative-train/theme-a-new-plan-for-europe-s-sustainable-prosperity-and-competitiveness/file-revision-of-the-pharmaceutical-legislation |
| WEB-3 | https://ec.europa.eu/health/system/files/2016-11/smpc_guideline_rev2_en_0.pdf |
| WEB-4 | https://www.ema.europa.eu/en/committees/working-parties-other-groups/chmp/smpc-advisory-group |
| WEB-5 | https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/product-information-requirements/product-information-qrd-templates-human |
| WEB-6 | https://www.ema.europa.eu/en/documents/template-form/qrd-product-information-template-version-104-highlighted_en.pdf |
| WEB-7 | https://www.pharmalex.com/thought-leadership/blogs/the-complex-landscape-of-french-regulatory-affairs/ |
| WEB-8 | https://ansm.sante.fr/uploads/2022/07/01/20220701-amm-pdtaut-doc004a-v01-recommandations-nationales-trad-amm-eng.pdf |
| WEB-9 | https://www.hma.eu/fileadmin/dateien/Human_Medicines/CMD_h_/procedural_guidance/Application_for_MA/CMDh_258_2012_Rev25_2023_05_clean_-_BlueBox_requirements.pdf |
| WEB-10 | https://arxiv.org/abs/2403.19726 |
| WEB-11 | https://incountry.com/blog/french-health-data-compliance-and-how-to-achieve-it/ |
| WEB-12 | https://secureprivacy.ai/blog/data-residency-requirements-eu-vs-us-explained |
| WEB-13 | https://www.hma.eu/human-medicines/cmdh/templates/qrd.html |
| WEB-14 | https://arxiv.org/pdf/2504.20598 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark covers biomedical NER and STS tasks drawn from scientific literature and clinical cases, but pharmaceutical regulatory documents have distinctive text types — SmPCs, patient information leaflets, patent claims, and CTD modules. Are these document genres central to your use case, and does the system need to handle the highly formulaic, legally constrained language specific to EU regulatory submissions rather than clinical or research prose?
A1: Regulatory document genres are central to the use case. While formulaic regulatory language differs from research prose, the underlying extraction tasks (compounds, dosages, safety warnings) are considered consistent enough for the model to function as a foundational engine. For highly specialized formats like CTD modules, regulatory-specific templates are applied as a supplementary layer.

Q2 [IC]: Regulatory drug labeling uses a very specific vocabulary: INNs, ATC codes, excipient nomenclature, posology expressions, and EMA-templated contraindication phrasing. Are these entity types and phrasings representative of what the system must detect, or does labeling work involve categories or patterns that diverge significantly from standard clinical or research text?
A2: Yes — INNs, ATC codes, excipient names, posology expressions, and contraindication phrasing are precisely the entity types the system must detect. There is no significant divergence from this characterization.

Q3 [OO]: For STS in the compliance workflow, two safety warnings may score as semantically equivalent under a general biomedical scorer yet be non-equivalent under EMA/ANSM standards due to small differences in dose thresholds or contraindicated-population qualifiers. Does the system require a scoring function sensitive to regulatory equivalence rather than general semantic proximity, and does a borderline score trigger automatic rejection or human review?
A3: The system is explicitly designed for regulatory equivalence, treating minor lexical discrepancies (dose thresholds, population qualifiers) as critical mismatches rather than near-synonymy. General semantic proximity is a baseline only. Borderline or high-stakes inconsistencies flag documents for human review; automatic rejection is not used.

Q4 [OC]: Ground-truth labels in biomedical benchmarks are typically produced by clinical or research annotators. For regulatory compliance, authoritative judgment may rest with regulatory affairs specialists or legal experts whose norms (EMA SmPC guidelines, ANSM circulars) differ from clinical annotation standards. Are the benchmark's annotation norms likely to align with the team's regulatory standards, or are systematic disagreements expected on borderline cases?
A4: Significant overlap is expected on core technical entities, but systematic disagreements are anticipated on borderline cases — biomedical NLP annotators tend to prioritize clinical relevance over the rigid legal constraints that govern regulatory interpretation.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark draws from scientific literature and clinical cases, but the deployment centers on EU regulatory document genres (SmPCs, leaflets, CTD modules) with formulaic, legally constrained language that is underrepresented or absent in DrBenchmark's task inventory. |
| IC | HIGH | Regulatory entities (INNs, ATC codes, excipient nomenclature, EMA-templated posology) are the exact targets of the system, yet benchmark instances are drawn from clinical and research prose where these precise phrasings and nomenclature conventions are used differently or less frequently. |
| IF | LOWER | Both deployment and benchmark operate on French text; no modality mismatch, non-Latin script issues, or infrastructure gaps are present. |
| OO | HIGH | The STS scoring function in the benchmark is calibrated for general semantic proximity, whereas the deployment requires regulatory equivalence scoring where small lexical differences carry legal consequence — a fundamentally different output decision rule than the benchmark implements. |
| OC | HIGH | Benchmark annotations are produced by clinical or biomedical NLP annotators whose norms diverge systematically from the EMA/ANSM regulatory standards that govern ground-truth judgments in this deployment, particularly on borderline entity and equivalence cases. |
| OF | LOWER | The deployment consumes label and score outputs matching the benchmark's output modalities; no mismatch in output representation format is present. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Findings tagged CRITICAL
should be treated as strong evidence for lower scores on the affected dimensions.

## Dataset Analysis Report

**Benchmark:** DrBenchmark — A Large Language Understanding Benchmark for the Biomedical French Language
**Datasets analyzed:** 11 datasets — QUAERO (EMEA config), FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC (fr_medline config), E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI
**Analysis date:** 2025-07-10

---

### Per-Dataset Fit Assessment

#### DrBenchmark/QUAERO (EMEA config)
- **Task:** NER (token classification, IOB2, 10 UMLS Semantic Group classes)
- **Deployment fit:** Partial — The EMEA configuration is the single dataset in DrBenchmark drawn directly from EU drug approval documents (patient information leaflets and SmPC-style texts), making it the closest available proxy for the deployment genre. Authentic regulatory source text is confirmed by QUAERO-D37 and QUAERO-D51. However, the label schema conflates INNs, excipients, and other chemicals under a single CHEM class (QUAERO-D1, QUAERO-D55), no ATC code entity type exists (QUAERO-D95), and contraindication population qualifiers are largely untagged (QUAERO-D64, QUAERO-D86).
- **Key concerns:**
  - CHEM label conflates INNs, excipients, solvents, and antibodies; downstream INN-vs-excipient distinction required by the deployment is impossible without post-processing (QUAERO-D1, QUAERO-D55)
  - ATC codes referenced in source text but not annotated as entities (QUAERO-D95)
  - Contraindication qualifiers (age thresholds, population conditions) receive no entity label, preventing regulatory-equivalence NER evaluation (QUAERO-D64, QUAERO-D86)
  - Nested entity simplification resulted in 6.06% annotation loss on EMEA subset, likely disproportionately affecting fine-grained regulatory entity boundaries
  - Some examples are uninformative administrative fragments (QUAERO-D15, QUAERO-D41, QUAERO-D84)

#### DrBenchmark/FrenchMedMCQA
- **Task:** Multiple-Choice Question Answering (MCQA) — pharmacy diploma exam questions
- **Deployment fit:** Weak — The deployment requires NER and STS; MCQA is a categorically different task type producing answer-index outputs rather than entity spans or similarity scores. Drug INNs appear only as answer choices in exam format (FRENCHMEDMCQA-D13, FRENCHMEDMCQA-D74), not as extraction targets in regulatory prose.
- **Key concerns:**
  - Fundamental task-type mismatch: output ontology is closed-set answer selection, bearing no relation to IOB2 NER labels or STS scores (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D2)
  - All content is academic clinical pharmacology exam prose, not legally constrained regulatory document text (FRENCHMEDMCQA-D105)
  - SmPC referenced in one answer option as a definitional item, not as source text (FRENCHMEDMCQA-D105)
  - Potential temporal validity concern for policy-adjacent questions (FRENCHMEDMCQA-D94)

#### DrBenchmark/DEFT2020
- **Task:** STS (sentence similarity scoring, 0–5 scale) and sentence selection
- **Deployment fit:** Partial — The STS task type is directly relevant. Some sentence pairs contain drug-label register text with excipient-based contraindications and safety warnings (DEFT2020-D18, DEFT2020-D16, DEFT2020-D52). However, approximately 30–40% of examples are entirely non-biomedical (DEFT2020-D1, DEFT2020-D3, DEFT2020-D5, DEFT2020-D6), and the scoring calibration does not distinguish legally significant micro-differences from general semantic proximity (DEFT2020-D16, DEFT2020-D130).
- **Key concerns:**
  - Large non-biomedical content fraction (beekeeping, railway infrastructure, history, geography) that will skew STS model representations away from regulatory register (DEFT2020-D1, DEFT2020-D3, DEFT2020-D5, DEFT2020-D6)
  - STS scores treat regulatory-relevant scope extensions (additional substance classes, alcohol interactions) as high-similarity rather than flagging them as potential mismatches (DEFT2020-D16, DEFT2020-D130)
  - Obligation modality differences (precautionary framing vs. direct instruction) scored identically under general proximity (DEFT2020-D4)
  - High inter-annotator disagreement on borderline pairs (DEFT2020-D46, DEFT2020-D102), with no regulatory-expert annotation to resolve them

#### DrBenchmark/MORFITT
- **Task:** Multi-label classification of biomedical abstracts by medical specialty (12 classes)
- **Deployment fit:** Weak — Document-level specialty classification is not a deployment task. No regulatory document genres present; all content is PMC Open Access research abstracts. Multiple examples originate from non-EU clinical contexts (MORFITT-D10, MORFITT-D11) and significant veterinary content is present (MORFITT-D12, MORFITT-D13, MORFITT-D14).
- **Key concerns:**
  - Task-type mismatch: document-level specialty classification produces no NER or STS outputs relevant to the deployment (MORFITT-D17)
  - No regulatory entity types present; label taxonomy (12 specialty classes) has no mapping to EMA entity categories (MORFITT-D17)
  - Non-EU geographic origin of multiple abstracts (Saudi Arabia, Jordan, Canada) introduces register and terminology variation inconsistent with EMA/ANSM French (MORFITT-D10, MORFITT-D11)
  - Veterinary content (animal disease, equine parasitology, canine otitis) has no deployment relevance (MORFITT-D12, MORFITT-D13, MORFITT-D14)
  - Translated abstracts from English may not reflect native French regulatory register (MORFITT-D8, MORFITT-D9)

#### DrBenchmark/CLISTER
- **Task:** STS (sentence similarity, 0–5 continuous scale) on clinical case sentence pairs
- **Deployment fit:** Partial — STS task type is relevant. Some pairs contain drug mentions (CLISTER-D2, CLISTER-D3, CLISTER-D4) adjacent to posology expressions. However, all text derives exclusively from clinical case narratives, and the scoring calibration produces critical failures for regulatory equivalence: a 2× quantitative difference in a biomarker value receives a score of 4.0 (CLISTER-D10), and positive vs. negative lab results receive 3.0 (CLISTER-D12).
- **Key concerns:**
  - Exclusively clinical case register; no regulatory document text present (CLISTER-D1 through CLISTER-D8)
  - STS scores are calibrated for clinical narrative proximity, not regulatory equivalence; quantitative differences (2× biomarker, route of administration) are systematically under-penalized (CLISTER-D10, CLISTER-D11, CLISTER-D12)
  - Brand names used alongside INNs in clinical prose, inconsistent with EMA INN-only convention (CLISTER-D6)
  - Some examples contain tabular pharmacokinetic rows or English prescription abbreviations (CLISTER-D15, CLISTER-D16), reducing ecological validity
  - No annotator documentation confirms regulatory expertise

#### DrBenchmark/MANTRAGSC (fr_medline config sampled)
- **Task:** Biomedical NER (IOB2, UMLS Semantic Group classes) across EMEA, MEDLINE, and patent subsets
- **Deployment fit:** Weak for the MEDLINE config sampled; the EMEA and patent configs are more relevant but were not the primary sample. The sampled MEDLINE content is exclusively historical French academic titles with no regulatory genre content (MANTRAGSC-D1, MANTRAGSC-D4). The patent config is a named deployment document type but CamemBERT-based models fail entirely on it. The dataset is critically small (~100 French MEDLINE examples).
- **Key concerns:**
  - Sampled config (fr_medline) contains only historical biomedical MEDLINE titles, not EMEA or patent text (MANTRAGSC-D1, MANTRAGSC-D4)
  - CHEM label conflates pharmaceutical substances with gases, hormones, and other chemicals — no INN-specific granularity (MANTRAGSC-D5, MANTRAGSC-D6)
  - No dosage, route, mode, or posology sub-entity labels (MANTRAGSC-D7, MANTRAGSC-D8)
  - Extremely small dataset size (~100 French MEDLINE training examples) limits statistical reliability (MANTRAGSC-D9, MANTRAGSC-D10)
  - Some content reflects sub-Saharan African epidemiology and veterinary contexts, non-EU register (MANTRAGSC-D11, MANTRAGSC-D12, MANTRAGSC-D13)
  - Patent subset is an effective blind spot: CamemBERT models generate only 'O' labels on MantraGSC Patents

#### DrBenchmark/E3C
- **Task:** Clinical NER — French_clinical (CLINENTITY only) and French_temporal (EVENT, ACTOR, BODYPART, TIMEX3, RML)
- **Deployment fit:** Weak — The NER task type is relevant, but the label schema captures only clinical entities (pathologies, temporal expressions) and explicitly excludes all drug-regulatory entity types. Drug names and dosages appearing in the source text receive O tags throughout (E3C-D3, E3C-D4, E3C-D8), representing the inverse of what the deployment requires.
- **Key concerns:**
  - CLINENTITY schema labels pathologies and symptoms; all drug names, INNs, dosages, and routes present in text receive O tags (E3C-D3, E3C-D4, E3C-D8, E3C-D11)
  - No label corresponds to any deployment-required regulatory entity type (E3C-D6, E3C-D7)
  - Some clinical cases originate from non-EU African settings, introducing geographic and register mismatch (E3C-D9, E3C-D10)
  - Tokenization artifacts (backslash-n tokens) visible in some examples (E3C-D13)

#### DrBenchmark/PxCorpus
- **Task:** Intent classification (4 classes) and NER (38 classes covering prescription entities) on transcribed spoken prescriptions
- **Deployment fit:** Weak — The NER entity types (SUBSTANCE, DOSAGE, MODE, FREQUENCY, DURATION) are conceptually the closest to deployment targets across DrBenchmark's spoken-language datasets. However, the input modality is transcribed speech, introducing pervasive ASR artifacts, dysfluencies, and informal register that are fundamentally incompatible with the formal written regulatory prose of SmPCs, patient leaflets, and CTD modules (PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D6, PXCORPUS-D8).
- **Key concerns:**
  - Critical modality mismatch: all utterances are transcribed spoken language with filler words, truncation artifacts, profanity, and system dialogue prompts embedded (PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D6, PXCORPUS-D8)
  - No ATC codes, excipient nomenclature, EMA-standard contraindication qualifiers, or INN-vs-brand distinction in label schema (PXCORPUS-D12, PXCORPUS-D13)
  - Severe class imbalance: `replace` (most relevant to inconsistency detection) has only 3 examples in the sample (PXCORPUS-D10, PXCORPUS-D11)
  - `none` class contaminated by meta-commentary and simulation artifacts (PXCORPUS-D14, PXCORPUS-D15, PXCORPUS-D16)
  - ASR transcription errors produce non-canonical drug name forms (PXCORPUS-D20, PXCORPUS-D21, PXCORPUS-D22)

#### DrBenchmark/DiaMED
- **Task:** Multi-class classification (ICD-10 chapter-level assignment)
- **Deployment fit:** Weak — ICD-10 chapter classification is a clinical coding task with no structural relationship to the deployment's NER or STS requirements. All source material originates from the Pan African Medical Journal (sub-Saharan African clinical cases), introducing both genre mismatch and geographic register mismatch with EU regulatory French (DIAMED-D2, DIAMED-D9).
- **Key concerns:**
  - Task-type mismatch: ICD-10 chapter classification produces no NER or STS output relevant to the deployment
  - Exclusive geographic origin from Pan African Medical Journal introduces non-EU clinical context and potential terminology inconsistency with EMA/ANSM French register (DIAMED-D2, DIAMED-D9, DIAMED-D12)
  - Drug mentions are informal narrative abbreviations (e.g., "D4T", "3TC"), not INN-formatted regulatory text (DIAMED-D1)
  - Severe class imbalance (Neoplasms: 165 examples; R00-R99: 1 example)
  - Annotation by 4 annotators with ICD-10 clinical coding expertise has no relationship to regulatory annotation standards

#### DrBenchmark/DEFT2021
- **Task:** NER (13 clinical entity types) and multi-label classification on clinical case reports
- **Deployment fit:** Weak — NER task type is relevant, but the schema covers clinical entity types (anatomy, pathology, treatment, temporal) rather than regulatory entity types. Drug names appear throughout the text and receive treatment/substance tags, but without INN-specific granularity, ATC codes, excipient distinction, or regulatory posology structure (DEFT2021-D55, DEFT2021-D158).
- **Key concerns:**
  - Clinical entity schema does not include INN, ATC code, excipient, or contraindication qualifier categories (DEFT2021-D55, DEFT2021-D158)
  - Drug names tagged as generic clinical substance entities identical to other treatment terms, precluding regulatory-grade INN extraction (DEFT2021-D80, DEFT2021-D99)
  - Some case reports originate from non-EU African settings (DEFT2021-D108, DEFT2021-D166)
  - Annotation by DEFT challenge participants with clinical/biomedical NLP expertise; no regulatory affairs specialist involvement documented
  - Sentence-boundary artifacts (punctuation-only tokens) present in sample (DEFT2021-D26, DEFT2021-D31, DEFT2021-D42)

#### DrBenchmark/CAS
- **Task:** POS tagging (31 classes), negation/speculation NER, and negation/speculation classification on clinical cases
- **Deployment fit:** Weak — POS tagging and negation/speculation classification are proxy tasks at best. All content is clinical case narrative. Drug mentions appear incidentally (CAS-D22, CAS-D33) but in informal clinical prose without regulatory structure. No label in any CAS configuration represents a regulatory entity or compliance-relevant category.
- **Key concerns:**
  - Label space (negation/speculation classes, POS tags) captures linguistic properties irrelevant to regulatory entity extraction or compliance verification (CAS task schema)
  - Clinical case genre entirely absent from regulatory document types; no SmPC, leaflet, or CTD content (CAS-D5, CAS-D15)
  - Drug mentions in informal narrative posology format, not EMA-templated expressions (CAS-D22, CAS-D29, CAS-D63)
  - POS annotations produced by automatic tagger (Tagex 3); no regulatory expertise required or applied

#### DrBenchmark/ESSAI
- **Task:** POS tagging (36 classes), negation/speculation NER, and negation/speculation classification on clinical trial protocols
- **Deployment fit:** Weak — Clinical trial protocol text is a distinct genre from regulatory submission documents. Dosage and frequency expressions appear in narrative form (ESSAI-D10, ESSAI-D11) and investigational compound codes (MEDI9197, BMS-986179, CMAK683X2101) dominate drug mentions (ESSAI-D7, ESSAI-D8, ESSAI-D9), which are absent from marketed drug labeling. Patient-addressed informal register appears in some examples (ESSAI-D13, ESSAI-D14).
- **Key concerns:**
  - Investigational compound codes, not INNs, are the dominant drug identifiers; these do not appear in SmPCs or patient leaflets (ESSAI-D7, ESSAI-D8, ESSAI-D9)
  - Clinical trial protocol genre differs structurally from regulatory submission documents; informed-consent second-person register is absent from SmPCs and CTDs (ESSAI-D13, ESSAI-D14)
  - Negation/speculation label taxonomy unrelated to regulatory compliance categories (ESSAI-D12)
  - No patent language, excipient lists, contraindication sections, or SmPC section headers observed across 75 sampled examples

---

### Cross-Cutting Findings

#### CRITICAL

**C1 — Universal regulatory document genre absence across all datasets except QUAERO EMEA**
Every dataset except QUAERO's EMEA configuration is drawn exclusively from clinical case narratives, academic research abstracts, clinical trial protocols, or transcribed spoken prescriptions. No dataset contributes SmPC sections, patient information leaflets, CTD modules, EU Risk Management Plans, or pharmaceutical patent claims as primary source text. This pattern is confirmed across CLISTER-D1 through CLISTER-D8, E3C-D3, DEFT2021-D3, CAS-D5, ESSAI-D1, DIAMED-D2, MORFITT-D4, and MANTRAGSC-D1. The benchmark's single partial coverage point (QUAERO EMEA) itself represents only a minority subset within that dataset, and even there the label schema is insufficient for the deployment's regulatory entity types.

**C2 — Systematic output ontology gap: no benchmark label set encodes regulatory-specific entity types**
Across all NER-bearing datasets (QUAERO, E3C, MANTRAGSC, DEFT2021, PxCorpus), no label explicitly represents INNs as distinct from other chemical entities, ATC codes, excipient nomenclature with Ph.Eur./INCI standards, EMA-templated contraindication qualifiers, or marketing authorization numbers. Drug entities are captured under broad UMLS CHEM/SUBSTANCE categories (QUAERO-D1, QUAERO-D55, MANTRAGSC-D5, MANTRAGSC-D6) or generic treatment/substance clinical tags (DEFT2021-D55, E3C-D3, E3C-D4), none of which enable the regulatory-grade entity discrimination the deployment requires. ATC codes are confirmed as a full gap with no analog in any dataset label set (QUAERO-D95).

**C3 — STS scoring calibration is fundamentally misaligned with regulatory equivalence requirements across both STS datasets**
Both CLISTER and DEFT2020 use a 0–5 general semantic proximity scale annotated by clinical/research annotators without any regulatory equivalence rubric. CLISTER-D10 shows a 2× quantitative biomarker difference scored 4.0 (high similarity); CLISTER-D12 shows positive vs. negative lab results scored 3.0; DEFT2020-D16 shows a safety warning where added substance class specificity is absorbed into a 4.0 score; DEFT2020-D130 shows a scope extension (adding alcohol to sedative interaction warning) scored 3.8. These patterns directly instantiate the benchmark YAML's confirmed "full gap" for STS scoring calibration, meaning models trained or evaluated on these datasets will not learn to treat regulatory micro-differences as critical mismatches.

#### MAJOR

**M1 — Non-biomedical content contamination in DEFT2020 STS training distribution**
Approximately 30–40% of DEFT2020 examples are non-biomedical (DEFT2020-D1, DEFT2020-D3, DEFT2020-D5, DEFT2020-D6). Models trained on this distribution will develop STS representations partly calibrated to general encyclopedic French similarity rather than biomedical or regulatory language, reducing the benchmark's diagnostic validity for the deployment's regulatory equivalence task.

**M2 — Annotator population mismatch across all datasets**
No dataset in DrBenchmark documents regulatory affairs specialists, EMA/ANSM-trained pharmacologists, or legal experts as annotators. The closest documented expertise is one medical expert with ICD-10 clinical coding knowledge (DiaMED) and automated annotation validated by clinical NLP researchers (CAS). This confirmed benchmark-wide gap means that ground-truth labels on borderline entity boundary and equivalence cases systematically reflect clinical biomedical conventions rather than the rigid legal constraints governing regulatory annotation, as anticipated by the elicitation response on OC.

**M3 — Spoken/transcribed modality introduces irreducible register mismatch for PxCorpus**
PxCorpus is the dataset with entity types (SUBSTANCE, DOSAGE, MODE, FREQUENCY, DURATION) most conceptually adjacent to the deployment's NER targets, yet its input modality is transcribed speech with pervasive ASR artifacts, profanity, system dialogue prompts, and dysfluencies (PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D6, PXCORPUS-D8). Models evaluated on PxCorpus performance are being assessed on a fundamentally different input distribution from the formal written regulatory French the system will encounter.

**M4 — Non-EU geographic origin of clinical case content across multiple datasets**
DiaMED (exclusively Pan African Medical Journal; DIAMED-D2, DIAMED-D9), MORFITT (Saudi Arabia, Jordan, Canada; MORFITT-D10, MORFITT-D11), MANTRAGSC (Dakar, Cameroon; MANTRAGSC-D11, MANTRAGSC-D12), DEFT2021 (Africa, Morocco; DEFT2021-D108, DEFT2021-D166), and E3C (Morocco, Africa; E3C-D9, E3C-D10) all contain cases with non-EU clinical contexts. These may introduce terminology conventions, abbreviation norms, or institutional registers inconsistent with EMA/ANSM French regulatory prose, compounding the domain register mismatch.

**M5 — Patent subset remains an effective blind spot despite nominal coverage in MANTRAGSC**
The MantraGSC fr_patents config is the only benchmark asset touching patent language — a named deployment document type — yet CamemBERT-based models generate only 'O' labels on this subset. The fr_medline config was sampled rather than the patent config, confirming the patent genre was not directly inspected. An independent 2025 arXiv study (arXiv:2504.20598) corroborates that pharmaceutical patent text has distinct NLP challenges that biomedical NER models do not address.

**M6 — Investigational compound codes dominate drug mentions in ESSAI, absent from regulatory labeling**
ESSAI contains numerous experimental compound identifiers (MEDI9197, BMS-986179, CMAK683X2101, LY3200882; ESSAI-D7, ESSAI-D8, ESSAI-D9) that do not appear in any marketed drug labeling document. A model evaluated on ESSAI NER performance is being assessed on entities that have no analog in the SmPCs, patient leaflets, or CTD modules the deployment system processes.

#### MINOR

**m1 — Noisy and uninformative examples dilute benchmark quality across multiple datasets**
Administrative fragments (QUAERO-D15, QUAERO-D41, QUAERO-D84), punctuation-only token artifacts (DEFT2021-D26, DEFT2021-D31, DEFT2021-D42), truncated ASR utterances (PXCORPUS-D4, PXCORPUS-D17, PXCORPUS-D18), and all-O entity-free MANTRAGSC examples (MANTRAGSC-D9, MANTRAGSC-D10) are present across datasets. These reduce benchmark signal density without affecting the core validity concerns.

**m2 — Tokenization artifacts visible in E3C and PxCorpus**
Backslash-n escape sequences appear as separate tokens in E3C (E3C-D13), and embedded system dialogue prompts appear in PxCorpus (PXCORPUS-D8). These artifacts are unlikely to affect aggregate performance substantially but could affect IOB2 boundary detection in affected examples.

---

### Confirmed Properties

The following properties are confirmed across datasets by content inspection:

1. **French language throughout, Latin script**: All datasets confirmed as French-language text with standard diacritics. No script mismatch or non-French content. CLISTER-D16 (English abbreviations) is an isolated exception.
2. **Clinical case narrative dominance**: The overwhelming majority of DrBenchmark content across all datasets is clinical case report prose — a register confirmed to be distinct from regulatory French.
3. **UMLS Semantic Groups as the NER ceiling for pharmacological entities**: The most granular drug-entity annotation available across QUAERO, MANTRAGSC, and related datasets is the CHEM Semantic Group, which conflates all pharmaceutical, chemical, and biological entities without regulatory-grade subtyping.
4. **No annotator population with documented regulatory affairs expertise**: Confirmed across all 11 datasets; the closest approximation is one medical expert with ICD-10 expertise (DiaMED) and clinical pharmacology exam authority (FrenchMedMCQA).
5. **QUAERO EMEA as the only direct regulatory genre source**: Content inspection confirms QUAERO EMEA-D37 and QUAERO-D51 as authentic EU regulatory document text; this is the unique regulatory-genre asset within the benchmark.
6. **STS calibration for clinical proximity, not regulatory equivalence**: Confirmed across CLISTER and DEFT2020 by examples showing that quantitative differences, route-of-administration distinctions, and scope extensions in safety language receive high similarity scores inconsistent with regulatory equivalence requirements.

---

### Content Coverage Summary

**What is represented:** DrBenchmark collectively covers French clinical case narratives (CLISTER, CAS, E3C, DiaMED, DEFT2021), biomedical research abstracts (MORFITT), clinical trial protocols (ESSAI), transcribed prescription dialogues (PxCorpus), pharmacy diploma exam questions (FrenchMedMCQA), biomedical MEDLINE titles (MANTRAGSC fr_medline), and a small subset of EU drug label text (QUAERO EMEA). Drug-related content is present in multiple datasets but consistently in clinical or research register rather than regulatory register.

**What is absent relative to deployment needs:**
- **SmPC sections** as primary NER or STS source text: absent except in the QUAERO EMEA minority subset
- **Patient information leaflets** as a distinct, representative corpus: partially present in QUAERO EMEA but uncharacterized as a separate sub-genre
- **CTD module language**: entirely absent
- **EU Risk Management Plans**: entirely absent
- **Pharmaceutical patent claim language**: nominally present in MANTRAGSC fr_patents config but constituting an effective model blind spot
- **ATC codes** as annotated entities: confirmed full gap across all datasets
- **INN-specific NER labels** (distinct from other CHEM entities): confirmed full gap
- **Excipient nomenclature** with Ph.Eur./INCI distinction: confirmed full gap
- **STS pairs annotated for regulatory equivalence**: confirmed full gap; no published benchmark exists
- **Regulatory affairs specialist annotators**: confirmed full gap; no dataset documents this annotator profile

---

### Limitations

1. **Patent config not directly sampled**: MANTRAGSC fr_patents was not the sampled configuration; the confirmed CamemBERT failure and patent-as-blind-spot finding derives from benchmark paper documentation rather than direct content inspection of patent examples.
2. **QUAERO MEDLINE config not sampled**: Only the EMEA configuration was analyzed. The MEDLINE config (biomedical titles) would likely show weaker regulatory fit, but this was not directly verified.
3. **DEFT2020 task_2 not sampled**: Only task_1 (sentence scoring) was analyzed; task_2 (sentence selection) may have a different content distribution.
4. **DEFT2021 classification config not sampled**: Only the NER configuration was analyzed; the multi-label classification config may have different content properties.
5. **CAS configs beyond POS not sampled**: The ner_neg, ner_spec, and cls configs were not directly inspected; the finding that label space is irrelevant to the deployment is confirmed structurally from schema, not from sampled examples of those configs.
6. **Sample-based analysis**: All per-dataset analyses are based on sampled examples (34–234 examples per dataset); rare regulatory-relevant content may be present but unobserved in the samples.
7. **No inspection of QUAERO EMEA proportions**: The fraction of patient information leaflet vs. SmPC-style text within the EMEA config could not be quantified from the sample.
8. **Nested entity loss impact unverifiable**: The 6.06% annotation loss in QUAERO EMEA from nested entity simplification is documented but the specific entity types lost cannot be determined from current sample.

---

### Cited Evidence

- **QUAERO-D1**: 1 | IC, OO | Excipient list from SmPC; CHEM tags conflate with active substance tags
- **QUAERO-D2**: 2 | IC | INN (lépirudine) in drug label context
- **QUAERO-D15**: 15 | IC | Fragmented multilingual address text
- **QUAERO-D34**: 34 | IC, OO | Multi-component excipient; nested entity simplification risk
- **QUAERO-D37**: 37 | IC | EU marketing authorization language confirming regulatory genre
- **QUAERO-D41**: 41 | IC | Near-empty example (tokens=['o', '.'])
- **QUAERO-D51**: 51 | IC, IF | EMEA document header confirming authentic source
- **QUAERO-D55**: 55 | IC, OO | INN and excipients conflated under CHEM
- **QUAERO-D64**: 64 | OO, OC | Contraindication content; population qualifiers largely untagged
- **QUAERO-D84**: 84 | IC | Bare document reference fragment
- **QUAERO-D86**: 86 | OO | Age-based contraindication; qualifier tokens untagged
- **QUAERO-D95**: 95 | IC, OO | ATC code referenced in text but value absent/unlabeled
- **FRENCHMEDMCQA-D1**: 1 | 1 correct | IO/OO | MCQA clinical recall — no NER/STS relevance
- **FRENCHMEDMCQA-D2**: 2 | 2 correct | OO | Output = index selection, not entity spans or scores
- **FRENCHMEDMCQA-D13**: 13 | 3 correct | IC | Drug INNs appear only as answer choices
- **FRENCHMEDMCQA-D50**: 50 | 2 correct | IC | Pharmaceutical manufacturing content, exam format
- **FRENCHMEDMCQA-D70**: 70 | 2 correct | IC | INN+brand in answer options, not regulatory prose
- **FRENCHMEDMCQA-D72**: 72 | 4 correct | IC | Drug-specific pharmacology, exam knowledge recall
- **FRENCHMEDMCQA-D74**: 74 | 2 correct | IC | INN+brand names as classified choices
- **FRENCHMEDMCQA-D94**: 94 | 2 correct | IC | Vaccination policy — potential temporal validity concern
- **FRENCHMEDMCQA-D105**: 105 | 1 correct | IC | SmPC referenced in answer option, not source text
- **DEFT2020-D1**: Example 1 (moy=0.5): Electric railway caténaire content — non-biomedical domain
- **DEFT2020-D3**: Example 3 (moy=2.1): Boris Godunov historical content — non-biomedical domain
- **DEFT2020-D4**: Example 4 (moy=4.0): Breastfeeding contraindication — drug label register, obligation modality difference
- **DEFT2020-D5**: Example 5 (moy=4.2): Caudry municipality — geographic/encyclopedic content
- **DEFT2020-D6**: Example 6 (moy=0.4): Beekeeping/queen selection — non-biomedical content
- **DEFT2020-D16**: Example 16 (moy=4.0): Opioid withdrawal warning — safety timing and substance class specificity difference scored as high similarity
- **DEFT2020-D18**: Example 18 (moy=4.6): Lactose excipient contraindication — SmPC section 4.3-style language
- **DEFT2020-D26**: Example 26 (moy=3.4): Cochrane comparative effectiveness statement — research prose register
- **DEFT2020-D27**: Example 27 (moy=4.4): Methodological quality assessment — research prose register
- **DEFT2020-D46**: Example 46 (moy=2.2, vote=5.0): High annotator disagreement (scores span 0–5)
- **DEFT2020-D52**: Example 52 (moy=4.4): Pharmaceutical tablet description — dosage form SmPC language
- **DEFT2020-D54**: Example 54 (moy=5.0): Von Willebrand hemostasis — identical source/target pair, adverse-event language
- **DEFT2020-D102**: Example 102 (moy=3.2, vote=1.0): Bimodal annotator disagreement on dental prosthetics pair
- **DEFT2020-D130**: Example 130 (moy=3.8): Sedative drug warning — scope extension (alcohol addition) scored as near-equivalent
- **MORFITT-D1**: Ex. 1 | 9 | Cardiology abstract; academic register confirmed
- **MORFITT-D2**: Ex. 19 | 7 | Pharmaceutical stability study; closest to regulatory content
- **MORFITT-D3**: Ex. 33 | 10,7 | Cosmetic/galenic formulation; academic not regulatory
- **MORFITT-D4**: Ex. 2 | 10 | Preclinical analgesic study; academic register
- **MORFITT-D5**: Ex. 21 | 1,3,4 | COVID immunology; no regulatory framing
- **MORFITT-D6**: Ex. 29 | 8 | Cyclosporine in veterinary; no INN/ATC conventions
- **MORFITT-D7**: Ex. 19 | 7 | Sulfadiazine dosage in research context
- **MORFITT-D8**: Ex. 10 | 3 | French translation from English; non-EMA register
- **MORFITT-D9**: Ex. 28 | 3,8 | Translated abstract; veterinary/Canadian context
- **MORFITT-D10**: Ex. 31 | 11 | Saudi Arabia medical intern survey
- **MORFITT-D11**: Ex. 20 | 1 | Jordanian cancer fatigue study
- **MORFITT-D12**: Ex. 4 | 8,4 | Foot-and-mouth disease in livestock
- **MORFITT-D13**: Ex. 9 | 6,0,8 | Canine otitis microbiome
- **MORFITT-D14**: Ex. 26 | 6,8,5 | Equine Sarcocystis parasitology
- **MORFITT-D15**: Ex. 12 | 11 | Psychosocial predictors of depression; non-regulatory
- **MORFITT-D16**: Ex. 22 | 11 | Arabic food addiction scale validation
- **MORFITT-D17**: Ex. 3 | 1 | "Etiology" label; no mapping to regulatory entity taxonomy
- **MORFITT-D18**: Ex. 6 | 6,8,2 | Multi-label PRRSV study; unrelated to regulatory norms
- **CLISTER-D1**: 9 | 0.0 | Clinical treatment narrative, not regulatory posology
- **CLISTER-D2**: 78 | 4.0 | Drug mention in anesthesia context, not SmPC format
- **CLISTER-D3**: 41 | 2.0 | Prescription-style text in clinical case context
- **CLISTER-D4**: 98 | 2.0 | Clinical dosage notation, informal register
- **CLISTER-D5**: 164 | 2.0 | Tabular pharmacokinetic data from clinical case
- **CLISTER-D6**: 146 | 0.0 | Brand name used, not INN-only regulatory convention
- **CLISTER-D7**: 75 | 1.25 | INN in oncology narrative, not regulatory format
- **CLISTER-D8**: 88 | 0.0 | Toxicology context, not contraindication section language
- **CLISTER-D9**: 3 | 3.0 | Adverse reaction scoring under general proximity vs. regulatory equivalence
- **CLISTER-D10**: 188 | 4.0 | 2× quantitative biomarker difference scored 4.0 (high similarity)
- **CLISTER-D11**: 149 | 0.5 | Route of administration difference (oral vs. IV) flagged via general scoring
- **CLISTER-D12**: 36 | 3.0 | Positive vs. negative test result scored 3.0
- **CLISTER-D13**: 10 | 5.0 | Minor grammatical variation correctly scored 5.0
- **CLISTER-D14**: 37 | 5.0 | Synonymous lexical expressions scored 5.0
- **CLISTER-D15**: 8 | 1.0 | Tabular pharmacokinetic rows; fragmented text
- **CLISTER-D16**: 191 | 2.0 | English prescription abbreviations in French corpus
- **MANTRAGSC-D1**: Ex. 1 | DISO | MEDLINE case report title; academic register
- **MANTRAGSC-D2**: Ex. 36 | CHEM (Cefotaxime) | Drug in clinical context, not regulatory format
- **MANTRAGSC-D3**: Ex. 45 | CHEM (testostérone) | Research-register hormone entity
- **MANTRAGSC-D4**: Ex. 41 | GEOG/epidemic | Sub-Saharan epidemiology; non-EU regulatory context
- **MANTRAGSC-D5**: Ex. 36 | CHEM | No INN-specific label granularity
- **MANTRAGSC-D6**: Ex. 53 | CHEM | Gases and drugs share same label as pharmaceutical INNs
- **MANTRAGSC-D7**: Ex. 18 | DEVI | No dosage/route/mode entity layer
- **MANTRAGSC-D8**: Ex. 17 | PROC | Treatment terms without posology sub-entities
- **MANTRAGSC-D9**: Ex. 57 | all-O | Administrative noise in tiny dataset
- **MANTRAGSC-D10**: Ex. 47 | all-O | Anthropological content; no entities
- **MANTRAGSC-D11**: Ex. 43 | DISO | Dakar clinical case; non-EU register
- **MANTRAGSC-D12**: Ex. 41 | GEOG | Central African epidemiology
- **MANTRAGSC-D13**: Ex. 22 | LIVB | Veterinary/avian content
- **E3C-D1**: Ex. 1 | all-O | "cholestase (bilirubine totale à 140 mmol/L...)" | IC, IF
- **E3C-D2**: Ex. 59 | all-O | "thrombolyse intraveineuse par ténectéplase 50 mg" | IO, IC
- **E3C-D3**: Ex. 62 | all-O | "amoxicilline-acide clavulanique à 3g/j, moxifloxacine à 400 mg/j" | IO, IC, OO
- **E3C-D4**: Ex. 79 | all-O | "Isoniazide 5mg/kg, Rifampicine 10 mg/kg, Ethambutol 25 mg/kg" | OO, OC
- **E3C-D5**: Ex. 39 | mixed | "ciclosporine, d'evérolimus et de corticoïdes, une insuffisance rénale" | OO
- **E3C-D6**: Ex. 3 | 0,0,0,0,1,2,0,0,0 | "tumeur solide du péritoine" | OO
- **E3C-D7**: Ex. 53 | ...1,2,2,0 | "état de choc septique" | OO
- **E3C-D8**: Ex. 103 | all-O | "fentanyl (3µg/kg) et de l'étomidate (0,2mg/kg)" | OO, OC
- **E3C-D9**: Ex. 90 | all-O | "rapportée en Afrique noire" | IC
- **E3C-D10**: Ex. 70 | ...1,...,0 | "originaire du Maroc" | IC
- **E3C-D11**: Ex. 112 | all-O | "Le traitement de cotrimoxazole était arrêté" | OC
- **E3C-D12**: Ex. 44 | all-O | "contraception orale au oestro-progestatifs" | OC
- **E3C-D13**: Ex. 5 | ...1,2,... | tokens=['\\','n','La',...] | IF
- **PXCORPUS-D1**: 41 | medical_prescription | IC, IO
- **PXCORPUS-D2**: 47 | medical_prescription | IC, IO
- **PXCORPUS-D3**: 166 | medical_prescription | IC
- **PXCORPUS-D4**: 3 | none | IF, IC
- **PXCORPUS-D5**: 10 | negate | IF, IC
- **PXCORPUS-D6**: 88 | none | IF, IC
- **PXCORPUS-D7**: 75 | medical_prescription | IF
- **PXCORPUS-D8**: 207 | medical_prescription | IF, IC
- **PXCORPUS-D9**: 169 | medical_prescription | IF
- **PXCORPUS-D10**: 4 | replace | IO, OO
- **PXCORPUS-D11**: 8 | replace | IO, OO
- **PXCORPUS-D12**: 9 | medical_prescription | OO
- **PXCORPUS-D13**: 99 | medical_prescription | OO
- **PXCORPUS-D14**: 18 | none | IC, OO
- **PXCORPUS-D15**: 76 | none | IC, OO
- **PXCORPUS-D16**: 64 | none | IC, OO
- **PXCORPUS-D17**: 34 | medical_prescription | IC
- **PXCORPUS-D18**: 59 | medical_prescription | IC
- **PXCORPUS-D19**: 81 | medical_prescription | IC
- **PXCORPUS-D20**: 13 | medical_prescription | IC, IF
- **PXCORPUS-D21**: 119 | medical_prescription | IC, IF
- **PXCORPUS-D22**: 103 | medical_prescription | IC, IF
- **DIAMED-D1**: Example 1 (label=A00-B99): "Le traitement était basé sur les antirétroviraux (Stavudine (D4T), Lamuvidine (3TC), Efavirenz (EFV))..." — Drug names in clinical narrative, not regulatory INN format; Pan African Medical Journal source.
- **DIAMED-D2**: Example 2 (label=C00-D49): Source URL `panafrican-med-journal.com`, published Nov 2015 — confirms non-EU geographic provenance.
- **DIAMED-D3**: Example 3 (label=D50-D89): Keywords include "Maroc" — North African setting.
- **DIAMED-D4**: Example 4 (label=E00-E89): Pan African Medical Journal source — consistent sub-Saharan/African geographic pattern.
- **DIAMED-D5**: Example 5 (label=F01-F99): "Halopéridol 20 mg et Chlorpromazine 400 mg...Phénobarbital" — clinical-narrative drug dosage mentions without regulatory structure.
- **DIAMED-D6**: Example 6 (label=G00-G99): Pan African Medical Journal source — African clinical setting confirmed.
- **DIAMED-D7**: Example 7 (label=H00-H59): Pan African Medical Journal source — no regulatory content.
- **DIAMED-D8**: Example 8 (label=H60-H95): "amphotéricine B par voie intraveineuse...itraconazole par voie orale" — drug names in narrative, no ATC codes or SmPC-style posology.
- **DIAMED-D9**: Example 9 (label=I00-I99): "service de cardiologie du CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" — explicitly West African clinical setting.
- **DIAMED-D10**: Example 10 (label=J00-J99): Pan African Medical Journal source — African clinical setting.
- **DIAMED-D11**: Example 11 (label=K00-K95): "polyglactin 910 (vicryl*2/0)" — trade name mention in surgical narrative, not regulatory INN context.
- **DIAMED-D12**: Example 12 (label=L00-L99): Keywords include "Niamey"; drugs listed as "Phénobarbital 200mg", "Halopéridol 20mg" in narrative — African setting, clinical dosage mentions not in regulatory format.
- **DIAMED-D13**: Example 13 (label=M00-M99): Pan African Medical Journal source — African clinical setting, no drug regulatory content.
- **DIAMED-D14**: Example 14 (label=N00-N99): Pan African Medical Journal source — African clinical setting, no regulatory content.
- **DEFT2021-D3**: Ex. 3 | Clinical narrative drug administration — no regulatory genre
- **DEFT2021-D15**: Ex. 15 | Broad span annotation for macroscopic findings
- **DEFT2021-D26**: Ex. 26 | Single punctuation token artifact
- **DEFT2021-D31**: Ex. 31 | Single initial token artifact
- **DEFT2021-D42**: Ex. 42 | Single initial token artifact
- **DEFT2021-D55**: Ex. 55 | Drug/dose/route annotated as clinical entities, not regulatory INN
- **DEFT2021-D80**: Ex. 80 | Informal clinical drug naming (no ATC/INN)
- **DEFT2021-D81**: Ex. 81 | Detailed chemotherapy in clinical narrative prose
- **DEFT2021-D99**: Ex. 99 | Drug name casually used, no regulatory formatting
- **DEFT2021-D108**: Ex. 108 | Non-EU geographic context in patient history
- **DEFT2021-D158**: Ex. 158 | Excipient/drug mixture annotated as generic substance
- **DEFT2021-D166**: Ex. 166 | Non-EU geographic reference (Madagascar)
- **CAS-D1**: Example 1: "l'examen clinique montre un état général conservé" — Clinical examination report; formal French clinical register
- **CAS-D5**: Example 5: "un homme de 48 ans...rectorragies dues à des polypes du rectum traités par électrocoagulation" — Clinical case presentation format
- **CAS-D13**: Example 13: "depuis hier soir, je suis essouflé...j'ai des frissons" — Patient direct speech; informal register
- **CAS-D15**: Example 15: "Il s'agit d'une patiente âgée de 54 ans...transmissions virales hépatiques" — Clinical case narrative; possible non-metropolitan context
- **CAS-D22**: Example 22: "administration d'une ampoule de digoxine en intraveineuse" — Drug mention in clinical narrative, informal posology
- **CAS-D29**: Example 29: "887,5 mg (12,5 mg/kg/h) administrée sur quatre heures" — Clinical dosage expression, not regulatory format
- **CAS-D33**: Example 33: "cyclophosphamide, vincristine et prednisone...rituximab" — Chemotherapy drugs listed in clinical protocol narrative
- **CAS-D34**: Example 34: "le Betnésol® lavement était progressivement arrêté" — Trade name with dosage form in clinical narrative
- **CAS-D47**: Example 47: "vous êtes appelés au secours d'une infirmière de nuit..." — Educational vignette register
- **CAS-D49**: Example 49: "la malade a été traitée à la norfloxacine" — Drug in casual clinical syntax
- **CAS-D54**: Example 54: "la valeur limite d'exposition autorisée était de 450 ppm soit 2 500 mg/m3" — Occupational exposure context
- **CAS-D63**: Example 63: "Pentasa®...Proctocort® (hydrocortisone acétate 90 mg: 1 lavement tous les soirs)" — Closest to posology expression; embedded in narrative
- **CAS-D80**: Example 80: "Cholstat® 0.1" — Branded drug fragment
- **CAS-D103**: Example 103: Dense lab table (AST, ALT, bilirubine, RNI, créatinine) — Structured numerical data; POS-tagged only
- **ESSAI-D1**: Ex. 3 | pos | "Un tirage au sort…répartira les patientes dans les deux bras de l'étude" | IC, IO
- **ESSAI-D2**: Ex. 6 | pos | "administré toutes les deux semaines sous forme de perfusion d'une heure" | IC
- **ESSAI-D3**: Ex. 37 | pos | "un anticorps anti-CTLA-4 (ipilimumab) et un anticorps anti-PD-1 (nivolumab)" | IC, IO
- **ESSAI-D4**: Ex. 71 | pos | "Ce traitement bénéficie d'une autorisation de mise sur le marché" | IC
- **ESSAI-D5**: Ex. 1 | pos | "la combinaison gemcitabine + abraxane, chez des patients avec un cancer du pancréas" | IC, OO
- **ESSAI-D6**: Ex. 36 | pos | "pemetrexed et cisplatine ou carboplatine, jusqu'à 6 cycles" | IC
- **ESSAI-D7**: Ex. 2 | pos | "Le MEDI9197 est injecté en intra-tumoral tous les 28j" | IC
- **ESSAI-D8**: Ex. 42 | pos | "Le BMS-986179 sera administré par voie veineuse toutes les semaines" | IC
- **ESSAI-D9**: Ex. 16 | pos | "évaluer la tolérance et l'efficacité du CMAK683X2101 (inhibiteur d'EED)" | IC
- **ESSAI-D10**: Ex. 25 | pos | "après 8 jours…toutes les 2 semaines pendant 6 semaines" | IC
- **ESSAI-D11**: Ex. 47 | pos | "donné par voie orale 2 fois par jour, pour une durée de 48 semaines" | IC
- **ESSAI-D12**: HF schema | cls labels | `["negation_speculation","negation","neutral","speculation"]` | OO
- **ESSAI-D13**: Ex. 26 | pos | "Vous serez vus en consultation régulièrement pour évaluer la tolérance" | IC, IF
- **ESSAI-D14**: Ex. 20 | pos | "Le choix de ton traitement est guidé par les anomalies des gènes de ta maladie" | IC, IF


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
  "region": "EU Pharmaceutical Regulatory Affairs Professionals (France / EMA-ANSM Zone)",
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
