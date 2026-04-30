I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Language** is valid for use in **French Pharmaceutical Regulatory Affairs — Document Compliance NLP**.

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
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### 1. Input Ontology
DrBenchmark defines a 20-task taxonomy spanning POS tagging, NER, multi-class
classification (MCC), multi-label classification (MLC), intent classification,
multiple-choice question answering (MCQA), and semantic textual similarity (STS)
[Q1, Q4, Q18]. The benchmark explicitly aims to combine classical tasks (NER, POS)
with more challenging ones (MCQA, multi-label classification) [Q20]. Aggregate
reporting is organized across five designated categories: POS, NER, MCQA, MCC,
MLC, and STS [Q81]. Individual datasets contribute varied subtasks: DEFT-2020
provides both sentence-pair similarity scoring and retrieval-based sentence selection
[Q21, Q22, Q23]; FrenchMedMCQA contributes two MCQA subtasks framed around French
pharmacy specialization diploma examinations [Q39]; and PxCorpus contributes spoken
intent classification and fine-grained NER from drug prescription transcripts [Q44].

From a regulatory deployment standpoint, the taxonomy presents a significant input
ontology gap. None of the 20 tasks are explicitly designed around EU regulatory
submission document genres — SmPCs, patient information leaflets, CTD modules, or
ANSM-specific submission formats. The closest approximations are QUAERO (sourced in
part from EMEA drug leaflets [Q34]) and Mantra-GSC (which includes a drug label
subset [Q40]), but these are used only for NER, not for STS tasks calibrated to
regulatory equivalence. The benchmark does not document whether its task taxonomy
was designed to cover regulatory compliance workflows, and no task explicitly
addresses the legally constrained, formulaic language of EU regulatory submissions.

### 2. Input Content
Data sources are diverse across clinical and research genres: scientific literature,
clinical trials, clinical cases, and speech transcriptions [Q19]. Specific datasets
include QUAERO (EMEA drug leaflets and MEDLINE biomedical titles, 103,056 words)
[Q33, Q34]; E3C (multilingual clinical cases, French subset only) [Q29, Q31];
DEFT-2021 (275 clinical cases) [Q24]; MorFITT (3,624 PMC Open Access biomedical
abstracts) [Q38]; Mantra-GSC (biomedical abstracts, drug labels, and patents, French
subset only) [Q40]; ESSAI (7,247 clinical trial protocols) [Q43]; CAS (3,790
clinical cases) [Q42]; and DiaMed (739 clinical cases from the Pan African Medical
Journal, created specifically for this benchmark) [Q45]. DrBenchmark does not
redistribute datasets and leaves original licensing unchanged [Q96].

From a regulatory vocabulary standpoint, the data instances reflect clinical and
research annotation norms. None of the described sources explicitly cover INNs,
ATC codes, excipient nomenclature, or EMA posology template phrasing as primary
content targets. QUAERO's EMEA drug leaflet subset [Q34] provides the closest
proxy, but the nested entity simplification (losing 6.06% of EMEA annotations and
8.90% of MEDLINE annotations) and sentence-splitting of long EMEA documents for
model input length constraints [Q37] further reduce the fidelity of the regulatory
content representation. The DiaMed dataset, while purpose-built, draws from the Pan
African Medical Journal and targets ICD-10 chapter-level disease classification [Q45],
not regulatory compliance entity types. No data source is described as originating
from French overseas territories; the tropical pathology angle of DiaMed is
incidental to its open-access journal origin rather than a deliberate regional
sampling decision.

### 3. Input Form
DrBenchmark is exclusively text-based, with all inputs consisting of French
biomedical prose [Q31, Q48]. The toolkit is implemented with HuggingFace Datasets,
Transformers, and PyTorch, providing normalized data loaders and predefined splits
[Q48]. Tokenization behavior across models is explicitly analyzed: the average
number of sub-tokens per word ranges from 1.43 (FlauBERT) to 1.90 (DrBERT-CP) [Q78],
and the SeqEval evaluation with IOB2 format is configured to predict labels on
the first sub-token only, providing tokenizer-agnostic evaluation [Q52, Q53].
Datasets lacking predefined splits received a consistent 70/10/20 random split
[Q32, Q40, Q42, Q43]. Data efficiency experiments varied training subset sizes at
25%, 50%, 75%, and 100% [Q68].

The input form is well-matched to the deployment context: both benchmark and
deployment are text-only in standard written French, with no cross-modality or
script mismatch. The Latin alphabet, high French literacy rates, and metropolitan
French text infrastructure assumptions are consistent across benchmark and deployment.
The PxCorpus dataset provides an exception — it originates from spoken-language
transcriptions of drug prescription dialogues [Q44] — but the benchmark inputs
are the transcribed text, not audio, so no signal-level mismatch arises.

### 4. Output Ontology
Label spaces across tasks are extensive. POS tagsets are fine-grained: CAS uses
31 POS classes [Q101] and ESSAI uses 41 POS tags [Q102]. NER label sets include
QUAERO's 10 UMLS Semantic Group categories [Q35, Q103]; E3C's clinical entity
and temporal/factuality annotation layers [Q30, Q104]; Mantra-GSC's Medline scheme
(11 classes) and EMEA/Patents scheme (10 classes) [Q106]; and DEFT-2021's 13
fine-grained entity types [Q28, Q108]. Multi-label classification in DiaMed uses
22 ICD-10 chapter-level classes [Q107]; DEFT-2021 MLC uses 23 MeSH Chapter C axes
[Q27]; and MorFITT uses 12 medical specialty labels [Q105]. STS tasks use
continuous similarity scores from 0 to 5 [Q22, Q41], and performance is reported
with Spearman correlation and EDRM metrics [Q54].

For the regulatory compliance deployment, the STS scoring rubric is the most
critical output ontology concern. The 0–5 coarse similarity scale [Q22] reflects
general semantic proximity and does not distinguish legally significant small-magnitude
differences — altered dose thresholds, contraindicated population qualifiers, or
modified safety warning phrasing — from semantically proximate but legally equivalent
variants. EMA/ANSM regulatory equivalence judgments require sensitivity to precisely
such fine-grained distinctions, and the benchmark provides no evidence that its
scoring rubric is calibrated for this stricter interpretive standard. For NER, the
entity categories (UMLS Semantic Groups, ICD-10 chapters, MeSH axes) reflect
clinical and research ontologies rather than the regulatory labeling ontologies
(INNs, ATC codes, EMA posology templates, contraindication qualifiers) required
for compliance-checking tasks. No leading model excels on both STS and MLC tasks
simultaneously [Q82], further underscoring that the benchmark's output structure
does not converge toward a single regulatory-compliance-relevant decision schema.

### 5. Output Content
Annotation practices vary considerably across the 20 constituent datasets. DEFT-2021
was manually annotated for both MLC and NER tasks [Q25]. CLISTER's 1,000 sentence
pairs were manually annotated by multiple annotators assigning 0–5 scores,
subsequently averaged into a single floating-point reference score [Q41]. DiaMed
was annotated by several annotators including one medical expert, applying 22
ICD-10 chapter-level labels to 739 clinical cases; inter-annotator agreement was
computed across two annotation sessions using Cohen's Kappa and Gwet's AC1 [Q45,
Q46]. CAS POS annotations were produced automatically via Tagex 3 and validated
against manual annotations at 98% precision [Q42] — a silver-standard rather than
gold-standard process.

The annotation workforce across DrBenchmark consists of clinical professionals,
NLP researchers, and in one case a medical expert [Q45], but no annotator with
regulatory affairs expertise — familiarity with EMA SmPC guidelines, ANSM
circulars, or CTD documentation standards — is identified in any described
dataset. Ground-truth labels therefore reflect clinical and research annotation
norms that may systematically diverge from the regulatory-legal standards
constituting authoritative ground truth in the pharmaceutical compliance deployment.
The silver-standard POS labels in CAS [Q42] compound this concern. The benchmark
is presented as a first-of-its-kind resource addressing a documented gap in French
biomedical NLP [Q5, Q9, Q16], but the annotation authority gap relative to
regulatory deployment standards is not flagged as a limitation by the authors.

### 6. Output Form
All evaluated models are pre-trained masked language models fine-tuned under a
consistent hyperparameter protocol, with results averaged over four runs and
statistical significance reported via Student's t-test [Q51]. Sequence labeling
tasks (NER, POS) are scored with SeqEval in IOB2 format [Q52]; STS tasks with
Spearman correlation and EDRM [Q54]; classification tasks against a majority-class
baseline [Q56]. The best model is saved based on validation metric performance
[Q100], and hyperparameter details are documented for reproducibility [Q49, Q99].
Domain- and language-specialized biomedical models lead on up to 75% of tasks [Q62],
with DrBERT-FS achieving top performance on 8 tasks [Q61].

The benchmark's discrete-label and continuous-score output forms are broadly
compatible with the deployment system's multi-candidate confidence-score design
and human-in-the-loop adjudication structure. However, the benchmark does not
evaluate or document confidence calibration, uncertainty quantification, or
the threshold at which a borderline score triggers mandatory human review [Q82].
These are operationally critical parameters for the pharmaceutical compliance
workflow — where a borderline STS score between two posology variants may determine
whether a document is auto-approved or escalated — and their absence constitutes a
moderate output form validity gap relative to the deployment's granularity
requirements.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "It encompasses 20 diversified tasks, including named-entity recognition, part-of-speech tagging, question-answering, semantic textual similarity, and classification." |
| Q2 | 1 | output_form | "We evaluate 8 state-of-the-art pre-trained masked language models (MLMs) on general and biomedical-specific data, as well as English specific MLMs to assess their cross-lingual capabilities." |
| Q3 | 1 | output_form | "Our experiments reveal that no single model excels across all tasks, while generalist models are sometimes still competitive." |
| Q4 | 1 | input_ontology | "These tasks encompass part-of-speech (POS) tagging, named-entity recognition (NER), classification, question-answering (QA), and semantic textual similarity (STS)." |
| Q5 | 1 | input_ontology | "Although the French language is generally considered as well-endowed, it is notably lacking in evaluation resources within the biomedical field." |
| Q6 | 1 | output_form | "We also perform a quantitative study of 8 pre-trained state-of-the-art masked language models" |
| Q7 | 1 | input_content | "Yanis Labrak, Adrien Bazoge, Oumaima El Khettari, Mickael Rouvier, Pacôme Constant dit Beaufils, Natalia Grabar, Béatrice Daille, Solen Quiniou, Emmanuel Morin, Pierre-Antoine Gourraud and Richard Dufour" |
| Q8 | 1 | input_content | "LIA, Avignon Université, Zenidoc, Nantes Université, CHU Nantes, Clinique des données, INSERM, CIC 1413, École Centrale Nantes, CNRS, LS2N, UMR 6004, Service de Neuroradiologie diagnostique et interventionnelle, l'institut du thorax, UMR 8163 – STL CNRS, Université de Lille" |
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
| Q36 | 3 | output_content | "In total, 26,409 entity annotations were mapped to 5,797 unique UMLS concepts." |
| Q37 | 3 | input_content | "Due to the presence of nested entities in annotations, we simplified the evaluation process by retaining only annotations at the higher granularity level from the BigBio (Fries et al., 2022) implementation, following the approach described in Touchent et al. (2023), which translates into an average loss of 6.06% of the annotations on EMEA and 8.90% on MEDLINE. Additionally, considering that some documents from EMEA exceed the maximum input sequence length that most current language models can handle, we decided to split these documents into sentences." |
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
| Q55 | 6 | output_ontology | "In Section 5.1, we compare the results obtained by each model within DrBenchmark, which permits to position a wide range of state-of-the-art models in the biomedical field across various NLP tasks." |
| Q56 | 6 | output_form | "The results of the 8 models are reported in Table 6 and compared to a baseline obtained by considering the majority class for all predictions." |
| Q57 | 6 | output_form | "Overall, although we might anticipate certain models to excel in all tasks, we discovered that no single model outperforms the rest in all application scenarios." |
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
| Q78 | 8 | input_form | "However, our experiments, as shown in Table 7, reveal that FlauBERT is the model with the least word segmentation (1.43 in average), while DrBERT-CP tends to have the highest average segmentation (1.90 in average)." |
| Q79 | 8 | input_form | "Surprisingly, when comparing the performance of these two models on the benchmark tasks, we observe that DrBERT-CP outperforms FlauBERT on 16 out of the 20 tasks, thus contradicting previous conclusions drawn by the community." |
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
| Q91 | 9 | input_content | "The size of the data has not been thoroughly investigated, particularly the significance of the pre-training data size, especially specialized data in the biomedical field." |
| Q92 | 9 | output_form | "Although the benchmark is easily reproducible and customizable, it required a substantial amount of computational power to execute all runs." |
| Q93 | 9 | output_form | "We utilized approximately 2,500 hours on V100 GPUs from the Jean-Zay supercomputer to complete the quantitative study." |
| Q94 | 9 | output_form | "According to the Jean Zay supercomputer documentation, the total environmental cost is estimated to be equivalent to 647,500 Wh or 36.9 kgCO2eq/kWh, based on the carbon intensity of the energy grid mentioned in the BLOOM environmental cost study conducted on Jean Zay (Luccioni et al., 2022)." |
| Q95 | 9 | input_content | "All code for DrBenchmark is released under the MIT License." |
| Q96 | 9 | input_content | "The licensing for all datasets remains unchanged from the original sources, and DrBenchmark has no intention of redistributing these datasets." |
| Q97 | 9 | input_content | "This work was performed using HPC resources from GENCI-IDRIS (Grant 2022-AD011013061R1 and 2022-AD011013715) and from CCIPL (Centre de Calcul Intensif des Pays de la Loire)." |
| Q98 | 9 | input_content | "This work was financially supported by ANR MALADES (ANR-23-IAS1-0005), ANR AIBy4 (ANR-20-THIA-0011) and Zenidoc." |
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
name: French Pharmaceutical Regulatory Affairs — Document Compliance NLP
abbreviation: fr_pharma_regulatory
deployment_context:
  system_description: A document management system using NER and semantic textual
    similarity (STS) models to verify compliance of drug labeling documents and flag
    inconsistencies in safety warnings. Outputs determine whether documentation meets
    professional standards for official submission or requires manual revision.
  operational_mode: Semi-automated compliance screening with human-in-the-loop adjudication
    for borderline cases. The system produces multi-candidate labels with confidence
    scores rather than single authoritative decisions.
  quality_tier: Silver Standard — acknowledged imperfect alignment with authoritative
    regulatory coding conventions in complex cases; not designed as an authoritative
    classifier.
  benchmark_assessed: DrBenchmark (French biomedical NLP, LREC-COLING 2024)
primary_geography:
  country: France
  sub_national_scope: Metropolitan France (primary priority)
  secondary_scope:
    territories:
    - Martinique
    - Guadeloupe
    - French Guiana
    - Réunion
    - Mayotte
    rationale: French overseas territories identified by user as highest secondary
      adaptation priority due to distinct disease prevalence patterns (e.g., tropical
      pathologies) not reflected in mainland datasets.
    constitutional_status_note: 'All five territories are DOM (Départements d''Outre-Mer)
      under Article 73 of the French Constitution and are integral parts of the French
      Republic with representation in Parliament. They are EU outermost regions. Source:
      INSEE — [WEB-1]'
languages:
  primary: French (Metropolitan, written formal register)
  register_notes: The deployment operates exclusively on structured regulatory and
    biomedical text in written French. Informal register, speech transcriptions, and
    cross-lingual inputs are out of scope. Regulatory documents follow highly formulaic,
    legally constrained language conventions distinct from clinical or research prose.
  dialect_variation_relevance: Minimal for primary metropolitan scope. French overseas
    territories may introduce regional terminology and tropical pathology vocabulary
    not present in mainland training and benchmark data — flagged as a known adaptation
    gap by the user.
  language_code: fr
writing_systems:
  scripts:
  - Latin alphabet with French diacritics (é, è, ê, à, â, ù, û, ç, œ, æ)
  note: No script mismatch concerns. All benchmark and deployment text is in standard
    written French using the Latin alphabet. RTL or multi-script handling is not required.
target_user_population:
  professional_roles:
  - Regulatory affairs specialists
  - Pharmacologists
  - Legal experts at pharmaceutical companies
  - Staff at government health agencies (e.g., ANSM)
  institutional_contexts:
  - Pharmaceutical companies operating under French and EU regulatory frameworks
  - French national health agency (ANSM — Agence nationale de sécurité du médicament
    et des produits de santé)
  - EU regulatory submission teams interfacing with EMA centralized procedures
  user_expertise_level: High — users are domain professionals who retain decision
    authority and adjudicate borderline model outputs. The system supports rather
    than replaces expert judgment.
  decision_authority: Regulatory affairs specialists and legal experts hold final
    adjudication authority over borderline cases; clinicians and nurses retain decision
    authority in the clinical support pathway.
  human_in_the_loop_design: Confirmed. High-uncertainty entities and borderline STS
    scores are flagged for manual review. The system outputs multiple candidate labels
    with confidence scores.
document_genres_in_scope:
  primary_targets:
  - Patient information leaflets (notices patient / PILs)
  - Summary of Product Characteristics (SmPC / RCP — Résumé des Caractéristiques du
    Produit)
  - Scientific abstracts relevant to regulatory submissions
  - 'Potentially: CTD (Common Technical Document) modules'
  - 'Potentially: patent claims'
  genre_characteristics: Highly formulaic, legally constrained language following
    EMA template structures. Text is structurally distinct from clinical case narratives
    or research prose — dense with standardized nomenclature, posology expressions,
    contraindication qualifiers, and excipient declarations.
  benchmark_genre_coverage_note: 'QUAERO corpus includes EMEA drug leaflet text for
    NER; Mantra-GSC includes a drug label subset. Neither is used for STS compliance
    tasks. No benchmark task explicitly addresses CTD modules, SmPCs as a compliance-checking
    genre, or ANSM submission formats. Searched DrBenchmark paper (arXiv 2402.13432
    and LREC-COLING 2024 proceedings) and confirmed: no DrBenchmark task uses SmPC
    or CTD text as a compliance-checking genre. The QUAERO EMEA subset (drug leaflets)
    is used only for NER with UMLS Semantic Group labels, not for STS or regulatory
    equivalence tasks. Source: ACL Anthology — [WEB-2];
    arXiv — [WEB-3]'
regulatory_framework:
  primary_national_authority: 'ANSM (Agence nationale de sécurité du médicament et
    des produits de santé) — superseded AFSSAPS on 1 May 2012. Source: Wikipedia —
    [WEB-4]'
  eu_level_authority: EMA (European Medicines Agency)
  relevant_procedures:
  - EMA centralized marketing authorization procedure
  - ANSM national procedure
  - Mutual recognition and decentralized procedures
  key_regulatory_standards:
  - EMA SmPC guideline (QRD template)
  - EMA patient information leaflet template
  - ICH CTD structure (M4)
  - ANSM national circulars and guidance documents
  ansm_ema_divergence_note: 'Partially resolved. France-specific divergences from
    EMA templates are documented and operational: (1) ANSM requires a French-specific
    ''Feuille de style'' submission template aligned to QRD but with national additions;
    (2) packaging must include a ''blue-box'' for French-specific CIP codes, Exploitant
    name, and national prescription/delivery conditions (List I / List II drug classification)
    even where SmPC/PIL text is otherwise EU-harmonized; (3) any packaging wording
    change post-authorization requires a regulatory variation submitted to ANSM or
    EMA depending on MA type. Source: PharmaLex — [WEB-5];
    Alhena Consult — [WEB-6].
    Deeper divergence in safety warning *content* standards (e.g., ANSM-specific contraindication
    phrasing requirements beyond EMA QRD) requires expert elicitation; not fully documented
    in publicly available sources.'
  applicable_data_protection_regulation: 'Resolved. The applicable framework is GDPR
    (RGPD — Règlement (UE) 2016/679) as transposed into French law by the Loi du 20
    juin 2018 relative à la protection des données personnelles (amending Loi Informatique
    et Libertés n°78-17 du 6 janvier 1978). Health data is classified as a special
    category (''données sensibles'') under RGPD Art. 9 and Loi Informatique et Libertés
    Art. 6 and 44, with processing generally prohibited except under specific derogations.
    The CNIL (Commission nationale de l''informatique et des libertés) is the supervisory
    authority and may require prior formalities for health data processing systems.
    Pharmaceutical regulatory document processing systems handling personal health
    data must comply with accountability requirements and may require CNIL notification
    or authorization. Source: CNIL — [WEB-7];
    G_NIUS/ANS — [WEB-8]'
  pharmacovigilance_framework: 'Resolved. EU pharmacovigilance is governed by Regulation
    (EU) No 1235/2010 (amending Regulation (EC) No 726/2004) and Directive 2010/84/EU,
    effective from 2 July 2012. France implements additional ANSM-specific requirements:
    MAHs/Exploitants must report ADRs directly to EudraVigilance and notify ANSM of
    any safety information affecting benefit-risk assessment; off-label use not included
    in RMP must be separately reported to ANSM; a French-specific Pharmacovigilance
    System Master File (PSMF) is required unless the global PSMF covers all national
    activities; additional risk minimization measures (aRMMs) must be validated and
    translated by ANSM; urgent safety signals require ANSM notification within three
    days; pharmacovigilance data must be archived for minimum 10 years. These ANSM-specific
    requirements affect what safety warning content changes trigger compliance review
    obligations. Source: Insuvia — [WEB-9];
    EUR-Lex Regulation 1235/2010 — [WEB-10]'
entity_vocabulary_requirements:
  regulatory_entity_types:
  - International Nonproprietary Names (INNs)
  - ATC (Anatomical Therapeutic Chemical) codes
  - Excipient names and nomenclature
  - Posology expressions (dose, frequency, route of administration)
  - Contraindication qualifiers (population subgroups, conditions)
  - EMA-template safety warning phrases
  - Adverse reaction terms (MedDRA preferred terms)
  benchmark_entity_coverage: Benchmark NER label sets use UMLS Semantic Groups (QUAERO),
    ICD-10 chapter labels (DiaMed), and MeSH Chapter C axes (DEFT-2021) — clinical/research
    ontologies that do not directly map to regulatory labeling entity types. PxCorpus
    NER covers drug, dose, and mode entities for prescription transcripts (38 classes),
    which partially overlaps.
  alignment_gap: 'Confirmed significant gap: user elicitation indicates the system
    targets ICD-10 clinical mapping rather than regulatory entity types, and the benchmark
    does not include INN, ATC code, or EMA posology template phrasing as primary NER
    targets.'
  crosswalk_to_regulatory_ontologies: 'Searched and not found as a published work
    specifically bridging DrBenchmark NER schemas to EMA/ANSM regulatory annotation
    guidelines. However, a directly relevant finding was identified: FDA/MITRE''s
    ADE Eval shared task evaluated NLP systems on extracting adverse event terms from
    drug labels and mapping to MedDRA Preferred Terms, achieving top F1 of 0.79 for
    MedDRA coding — but concluded that NLP tools required modification before regulatory
    use and that tools purpose-built for drug label AE extraction and MedDRA mapping
    are needed. This English-language work has no French equivalent in the literature
    searched. MedDRA is available in French translation (confirmed: BioPortal NCBO
    — [WEB-11]) but no French-language
    NER benchmark targets MedDRA preferred terms. Source for ADE Eval finding: PubMed
    29860093 — [WEB-12]; ScienceDirect — [WEB-13]

    [NOT FOUND — no published crosswalk between DrBenchmark NER schemas and EMA/ANSM
    regulatory annotation guidelines or MedDRA/EDQM nomenclatures found in searched
    sources]'
sts_compliance_requirements:
  deployment_use_of_sts: STS scores are used to assess equivalence of safety warning
    text across document versions — e.g., comparing proposed labeling phrasing against
    approved reference text or between draft and final versions.
  regulatory_equivalence_sensitivity: 'Minor lexical differences (altered dose thresholds,
    modified population subgroup qualifiers, changed contraindication phrasing) carry
    legal significance under EMA/ANSM standards even when a general biomedical STS
    scorer would assign high similarity. Packaging wording changes require formal
    regulatory variation submissions (Type IA, IB, or II), demonstrating that even
    minor text changes have legally operative consequences. Source: Alhena Consult
    — [WEB-6]'
  benchmark_sts_scoring: 'DrBenchmark STS tasks use a coarse 0–5 Likert-style scale
    reflecting general semantic proximity (CLISTER: 1,000 clinical sentence pairs;
    DEFT-2020: similarity + retrieval tasks). No evidence this rubric distinguishes
    legally significant small-magnitude differences from semantically proximate but
    legally equivalent variants.'
  scoring_calibration_gap: 'Fully confirmed gap: benchmark scoring rubric is not calibrated
    for regulatory-equivalence interpretation. The user''s elicitation answers did
    not confirm that the deployment STS function is calibrated for this stricter standard
    either.'
  borderline_score_handling: Borderline STS scores trigger human review rather than
    automatic rejection. The exact score threshold for mandatory escalation is not
    benchmarked against regulatory workflow requirements.
  threshold_documentation: '[NEEDS VERIFICATION — deferred: below search budget; likely
    requires direct system documentation review rather than web search]'
annotation_authority:
  benchmark_annotator_profiles: Clinical professionals, NLP researchers, and one medical
    expert (DiaMed). CAS POS labels are silver-standard (automatic via Tagex 3 with
    98% precision validation). CLISTER STS labels are averaged scores from multiple
    annotators.
  regulatory_authority_gap: No annotator with regulatory affairs expertise, pharmacovigilance
    specialization, or EMA/ANSM submission legal knowledge is identified in any DrBenchmark
    dataset annotation team. Ground-truth labels reflect clinical and research norms
    that may systematically diverge from regulatory-legal compliance standards.
  iaa_documentation: The DrBenchmark paper (Table 4, Q45/Q46) documents inter-annotator
    agreement for DiaMed using Cohen's Kappa and Gwet's AC1 across two annotation
    sessions of 15 clinical cases each with 4 annotators. The specific numerical values
    are reported in Table 4 of the paper but were not retrievable from search results
    (table not rendered in indexed text). The benchmark paper is openly accessible
    at the ACL Anthology for direct retrieval of these values. [NOT FOUND — specific
    IAA kappa values for DiaMed Table 4 not surfaced in search results; available
    in full paper PDF at [WEB-2]]
  silver_vs_gold_standard: 'CAS POS annotations are confirmed silver-standard (automatic
    Tagex 3 + 98% precision validation). DEFT-2021 NER and MLC are manually annotated
    (gold-standard). CLISTER STS is manually annotated by multiple annotators with
    averaged scores. DiaMed classification is manually annotated with IAA measurement.
    ESSAI POS uses TreeTagger (automatic, silver-standard). No additional DrBenchmark
    tasks with explicit silver-standard labeling were identified beyond CAS POS and
    ESSAI POS; the NER tasks (QUAERO, E3C, Mantra-GSC) derive from pre-existing manually
    annotated corpora. Source: arXiv 2402.13432 — [WEB-14]'
infrastructure_notes:
  deployment_modality: Text-based document management system. No audio, image, or
    cross-modal inputs. Standard written French text in structured document formats.
  text_infrastructure: Metropolitan France — high-resource digital infrastructure
    context consistent with benchmark assumptions. Standard Latin script rendering,
    no RTL or bidirectional text concerns.
  model_integration: System integrates NER and STS models (likely fine-tuned masked
    language models such as DrBERT, CamemBERT-bio, or similar). HuggingFace ecosystem
    assumed consistent with DrBenchmark toolkit.
  tokenization_considerations: French biomedical terminology (long compound terms,
    Latin-derived nomenclature, INN strings) may produce high sub-token fragmentation.
    DrBERT-CP shows highest average segmentation (1.90 sub-tokens/word) in benchmark
    experiments — performance impact on regulatory entity spans warrants assessment.
  compute_requirements: '[NEEDS VERIFICATION — deferred: likely unsearchable (on-premises
    vs. cloud decision is internal deployment configuration not publicly documented);
    low impact for scoring]'
  data_sensitivity: 'Pharmaceutical regulatory submissions are commercially sensitive
    and may be subject to trade secret protections in addition to personal data regulations.
    On-premises deployment is probable. Under French law, regulatory documents containing
    personal health data are subject to RGPD/Loi Informatique et Libertés; health
    data hosting must comply with Code de la santé publique Art. L.1111-8 and associated
    hébergeur agréé (certified health data hosting) requirements. Source: G_NIUS/ANS
    — [WEB-8]'
overseas_territory_adaptation:
  priority_territories:
  - Martinique
  - Guadeloupe
  - French Guiana
  - Réunion
  - Mayotte
  tropical_pathology_vocabulary:
  - Dengue
  - Chikungunya
  - Paludisme (malaria)
  - Zika
  - Leptospirose
  - Leishmaniose (French Guiana)
  benchmark_coverage_of_territories: No DrBenchmark data source is described as originating
    from French overseas territories. DiaMed (Pan African Medical Journal) may incidentally
    include tropical pathology cases but was not designed to represent overseas territory
    populations or regulatory needs.
  regulatory_variation_overseas: 'Partially resolved. The five priority territories
    are DOM (Départements d''Outre-Mer) and as integral parts of the French Republic,
    French and EU pharmaceutical law applies to them directly — ANSM has regulatory
    authority over these territories. However, key France-specific packaging requirements
    (CIP codes, Exploitant designation, List I/II drug classification labeling) apply
    uniformly across metropolitan France and DOM. No published ANSM guidance specifically
    modifying safety warning content standards for tropical disease indications in
    overseas territories was found. The territories are EU outermost regions (Article
    349 TFEU), meaning EMA centralized procedure regulations apply, but no documented
    DOM-specific labeling divergence for safety content was identified. Source: INSEE
    DOM definition — [WEB-1]; PharmaLex
    French regulatory overview — [WEB-5]

    [NOT FOUND — no ANSM-published guidance specifically addressing labeling standard
    modifications for tropical disease indications in French overseas territories]'
  disease_prevalence_divergence: User confirmed that overseas territories have distinct
    disease prevalence patterns not reflected in mainland datasets, making direct
    transfer of mainland-trained models unreliable for territory-specific compliance
    checking.
  vocabulary_gap_assessment: Searched and confirmed gap. No DrBenchmark dataset is
    described as including tropical pathology terminology (dengue, chikungunya, paludisme,
    Zika, leptospirose, leishmaniose) as a deliberate coverage target. DiaMed's Pan
    African Medical Journal origin may incidentally include some tropical disease
    cases but this is not documented. The benchmark paper makes no mention of French
    overseas territory vocabulary coverage. QUAERO (EMEA/MEDLINE sources) covers European
    drug regulatory and biomedical literature contexts that would not systematically
    include tropical pathology vocabulary for DOM territories. [NOT FOUND — no evidence
    of tropical pathology vocabulary coverage in DrBenchmark datasets; absence confirmed
    by review of all dataset descriptions in arXiv 2402.13432 — [WEB-3]]
cultural_and_professional_norms:
  professional_culture: French pharmaceutical regulatory affairs operates within a
    highly formalized, rule-bound professional culture shaped by EMA and ANSM procedural
    requirements. Regulatory specialists prioritize legal precision over semantic
    approximation — small wording differences carry material compliance consequences.
  language_formality: All deployment text is formal written French following standardized
    regulatory templates. Informal register, abbreviations, or clinical shorthand
    are out of scope; the system is confirmed to handle common abbreviations and clinical
    shorthand moderately but is not designed for highly disorganized text.
  institutional_hierarchy: Regulatory submissions are subject to multi-level review
    within pharmaceutical companies (regulatory affairs, medical, legal, quality)
    before submission to ANSM or EMA. The NLP system operates as a pre-review screening
    layer, not a final gate.
  liability_sensitivity: Incorrect safety warning classification or false equivalence
    judgments in STS scoring carry potential regulatory, legal, and patient safety
    consequences. This elevates the threshold for acceptable model confidence and
    the importance of human review escalation.
domain_specific_notes:
  regulatory_legal: 'French pharmaceutical regulatory compliance operates under dual
    national (ANSM) and EU (EMA) authority. SmPC and PIL content must conform to EMA
    QRD templates while meeting ANSM national requirements. France-specific divergences
    include: the ''Feuille de style'' submission template; the ''blue-box'' mechanism
    for French-specific packaging elements (CIP codes, Exploitant details, List I/II
    classification); and variation type classification (IA/IB/II) determining which
    text changes require formal regulatory submission. Source: PharmaLex — [WEB-5]'
  pharmacovigilance: 'Safety warnings in labeling documents are subject to ongoing
    revision driven by pharmacovigilance signals. When Periodic Safety Update Reports
    (PSURs) identify new signals, MAHs are legally obligated to update SmPC Sections
    4.8 and potentially 4.4. Delays expose patients to unwarned risks; frequent updates
    create ''label churn'' compliance risks. The compliance checking system must handle
    versioned documents and detect unauthorized or unsubstantiated changes in safety
    warning text between versions. ANSM requires urgent safety signal notification
    within three days. Source: go.pharmazie.com SmPC overview — [WEB-15];
    Insuvia pharmacovigilance France — [WEB-9]

    [NEEDS VERIFICATION — deferred: whether the deployment tracks document versions
    or performs single-document compliance checks requires system documentation review,
    not web search]'
  nomenclature_standards: 'INNs are governed by WHO INN Programme; ATC codes by WHO
    Collaborating Centre for Drug Statistics Methodology; excipient names by European
    Pharmacopoeia (EDQM). These are normatively distinct from clinical ontologies
    (UMLS, ICD-10, MeSH) used in benchmark annotation. No DrBenchmark task explicitly
    targets INN or ATC entity recognition — confirmed by review of all 20 task descriptions
    and entity label sets in the benchmark paper. The closest overlap is PxCorpus
    NER (drug, dose, mode) which is a prescription transcript corpus, not a regulatory
    labeling corpus. Source: arXiv 2402.13432 — [WEB-14]'
  icd10_vs_regulatory_coding: The DiaMed dataset maps clinical cases to ICD-10 chapter-level
    categories — a clinical coding ontology used for hospital reimbursement and epidemiology,
    not for regulatory labeling compliance. The user's elicitation confirmed the system
    performs ICD-10 chapter-level disease classification, which may represent a scope
    narrower than or different from what strict regulatory label compliance checking
    requires.
  meddra_relevance: 'MedDRA (Medical Dictionary for Regulatory Activities) is the
    standard terminology for adverse event and safety warning reporting in EMA submissions;
    it is a subscription-based ICH product used by regulatory authorities and the
    biopharmaceutical industry across the full regulatory lifecycle. MedDRA is available
    in French translation. No DrBenchmark NER schema maps to or is described as compatible
    with MedDRA preferred terms or System Organ Class (SOC) structure. Published English-language
    NLP work (FDA/MITRE ADE Eval) shows that even purpose-built NLP systems for drug
    label AE extraction to MedDRA PTs achieved only F1 ~0.79 and required human intervention,
    underscoring the difficulty of this task and the absence of a French-language
    equivalent benchmark. Source: Wikipedia MedDRA — [WEB-16];
    PubMed ADE Eval — [WEB-12]'
net_new_fields:
  ansm_france_specific_packaging_requirements: 'ANSM requires several France-specific
    elements on product packaging beyond EMA QRD content: (1) CIP codes (national
    registration numbers); (2) Exploitant name and status; (3) List I / List II prescription
    classification labeling; (4) promotional material submission for ANSM approval
    in defined slots (4 per year, 2-month response window). These elements appear
    in the ''blue-box'' on outer packaging for centrally authorized products, or must
    be embedded in nationally submitted packaging for decentralized/national procedures.
    Any change to packaging wording requires a variation (Type IA: minor, no clinical
    consequence; Type IB: moderate; Type II: major clinical/safety impact). This variation
    classification directly determines the compliance threshold for STS-based text
    change detection. Source: PharmaLex — [WEB-5];
    Alhena Consult — [WEB-6]'
  smpc_versioning_and_label_churn: 'Post-market pharmacovigilance signals (via PSURs)
    legally oblige MAHs to update SmPC Section 4.8 (adverse reactions) and Section
    4.4 (special warnings). This creates ongoing document versioning pressure. Frequent
    updates produce ''label churn'' where physical packaging becomes outdated relative
    to the approved SmPC, creating compliance inspection risks. The NLP compliance
    system must be robust to version-tracking scenarios where the reference document
    itself changes over time. Source: go.pharmazie.com — [WEB-15]'
  meddra_french_translation_availability: 'MedDRA is available in French translation,
    confirming that French-language regulatory entity annotation using MedDRA terminology
    is feasible in principle. However, MedDRA is a subscription-based product; no
    open-access French MedDRA NER benchmark exists. A given adverse effect in France''s
    national pharmacovigilance database can be coded under multiple MedDRA terms (a
    French study found the effectiveness of MedDRA standardized queries is highly
    variable depending on the adverse effect), complicating NLP-to-MedDRA mapping.
    Source: BioPortal NCBO — [WEB-11];
    PubMed MedDRA evaluation — [WEB-17]'
  eu_safety_communication_inconsistency: 'A cross-EU study found that national regulators
    (including ANSM) inconsistently disseminate EMA-issued Dear Healthcare Professional
    Communications (DHPCs), with safety DHPCs or withdrawals occurring for 28.6% of
    EMA-approved medicines between 2001–2013 but not uniformly published by all national
    agencies. This documents a real-world EMA–ANSM divergence in safety information
    dissemination that affects what constitutes ''current'' safety warning content
    in French labeling documents at any given time. Source: PMC4204813 — [WEB-18]'
  drbenchmark_publication_venue: 'DrBenchmark was presented at LREC-COLING 2024 (Torino,
    Italy, May 2024), published in the proceedings pages 5376–5390 by ELRA and ICCL.
    The benchmark toolkit is released under CC0 1.0 open-source license; the underlying
    datasets retain their original licenses unchanged. Source: ACL Anthology — [WEB-2];
    HAL — [WEB-19]'
flagged_verification_priorities:
- priority: 1
  gap: Regulatory document genre coverage in DrBenchmark
  search_target: DrBenchmark NER STS tasks SmPC patient information leaflet CTD module
    EMA ANSM regulatory text coverage
  resolution_status: 'RESOLVED — confirmed no SmPC/CTD compliance-checking task exists
    in DrBenchmark; QUAERO EMEA drug leaflets used only for NER. Source: [WEB-2]'
- priority: 2
  gap: Regulatory entity taxonomy alignment (INN, ATC, excipient, MedDRA vs. UMLS/ICD-10/MeSH)
  search_target: NER benchmark INN ATC MedDRA excipient EMA regulatory entity annotation
    French pharmaceutical labeling DrBenchmark crosswalk
  resolution_status: 'RESOLVED (gap confirmed) — no DrBenchmark NER task targets INN,
    ATC, or MedDRA entities; no published crosswalk found. English-language ADE Eval
    benchmark for English drug labels exists but no French equivalent. Source: [WEB-12]'
- priority: 3
  gap: STS scoring calibration for regulatory equivalence
  search_target: semantic textual similarity regulatory equivalence drug labeling
    fine-grained scoring EMA ANSM compliance French NLP dose threshold contraindication
  resolution_status: 'RESOLVED (gap confirmed) — no published STS benchmark calibrated
    for EU regulatory labeling equivalence found; variation type classification (IA/IB/II)
    framework confirms legal significance of small text changes. Source: [WEB-6]'
- priority: 4
  gap: Annotation authority — regulatory affairs and legal expertise in benchmark
    ground truth
  search_target: DrBenchmark annotation protocol regulatory affairs pharmacovigilance
    legal expert annotator EMA SmPC ANSM NLP benchmark
  resolution_status: 'RESOLVED (gap confirmed) — no regulatory affairs expert annotators
    identified in any DrBenchmark dataset annotation team. Source: [WEB-14]'
- priority: 5
  gap: ANSM vs. EMA normative divergence for safety warning standards
  search_target: ANSM EMA divergence safety warning SmPC labeling standards France
    national vs centralized marketing authorization procedure regulatory compliance
  resolution_status: 'PARTIALLY RESOLVED — France-specific packaging/submission requirements
    documented (Feuille de style, blue-box, CIP codes, List I/II, variation types
    IA/IB/II). Specific divergence in safety warning *content* standards between ANSM
    national circulars and EMA QRD requires expert elicitation. Source: [WEB-5]'
- priority: 6
  gap: French overseas territories — benchmark coverage and tropical pathology vocabulary
  search_target: French overseas territories biomedical NLP tropical pathology dengue
    paludisme chikungunya NER benchmark Martinique Réunion Guadeloupe French Guiana
  resolution_status: 'RESOLVED (gap confirmed) — no DrBenchmark dataset covers French
    overseas territories or tropical pathology vocabulary; regulatory framework applies
    uniformly (DOM are integral France); no DOM-specific labeling divergence found.
    Source: [WEB-1]; [WEB-3]'
- priority: 7
  gap: Silver-standard label quality and IAA levels across DrBenchmark tasks
  search_target: DrBenchmark inter-annotator agreement silver standard gold standard
    annotation quality NER STS IAA kappa
  resolution_status: 'PARTIALLY RESOLVED — silver-standard tasks confirmed (CAS POS,
    ESSAI POS via TreeTagger); gold-standard tasks confirmed (DEFT-2021, DiaMed, CLISTER).
    Specific numerical kappa values from DiaMed Table 4 not surfaced in search; available
    in full paper PDF at [WEB-2]. Source:
    [WEB-14]'
- priority: 8
  gap: Confidence calibration and score thresholds for human review escalation
  search_target: confidence calibration uncertainty quantification biomedical NLP
    regulatory compliance human-in-the-loop STS NER threshold French pharmaceutical
  resolution_status: '[NEEDS VERIFICATION — deferred: below search budget; requires
    system documentation review rather than web search; low searchability]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.insee.fr/en/metadonnees/definition/c2316 |
| WEB-2 | https://aclanthology.org/2024.lrec-main.478/ |
| WEB-3 | https://arxiv.org/abs/2402.13432 |
| WEB-4 | https://en.wikipedia.org/wiki/Agence_nationale_de_s%C3%A9curit%C3%A9_du_m%C3%A9dicament_et_des_produits_de_sant%C3%A9 |
| WEB-5 | https://www.pharmalex.com/thought-leadership/blogs/the-complex-landscape-of-french-regulatory-affairs/ |
| WEB-6 | https://alhena-consult.com/how-to-market-a-drug-in-france/ |
| WEB-7 | https://www.cnil.fr/fr/quelles-formalites-pour-les-traitements-de-donnees-de-sante |
| WEB-8 | https://gnius.esante.gouv.fr/en/regulations/what-does-a-health-data-do |
| WEB-9 | https://insuvia.com/insights/pharmacovigilance-regulations-france/ |
| WEB-10 | https://eur-lex.europa.eu/eli/reg/2010/1235/oj/eng |
| WEB-11 | https://bioportal.bioontology.org/ontologies/MEDDRA |
| WEB-12 | https://pubmed.ncbi.nlm.nih.gov/29860093/ |
| WEB-13 | https://www.sciencedirect.com/science/article/pii/S1532046418301060 |
| WEB-14 | https://arxiv.org/html/2402.13432v1 |
| WEB-15 | https://go.pharmazie.com/en/the-strategic-imperative-of-the-summary-of-product-characteristics-smpc-regulatory-frameworks-digital-transformation-and-ai-driven-compliance/ |
| WEB-16 | https://en.wikipedia.org/wiki/MedDRA |
| WEB-17 | https://pubmed.ncbi.nlm.nih.gov/30645835/ |
| WEB-18 | https://pmc.ncbi.nlm.nih.gov/articles/PMC4204813/ |
| WEB-19 | https://hal.science/hal-04470938 |

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
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Benchmark:** DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Language
**Datasets analyzed:** 11 (QUAERO, FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC, E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI)
**Analysis date:** 2025-07-14

---

### Per-Dataset Fit Assessment

#### DrBenchmark/QUAERO (EMEA config)

- **Task:** Named entity recognition (NER), token classification
- **Deployment fit:** Partial — The EMEA configuration is the single dataset in DrBenchmark sourced directly from EU drug leaflets and SmPC-adjacent regulatory documents, making it the closest match to the deployment's primary document genre. However, the UMLS Semantic Group label scheme conflates regulatory-legally distinct entity categories, nested-entity simplification reduces annotation fidelity, and document fragmentation artifacts reduce document-level coherence.
- **Key strengths:**
  - Direct source alignment with EMA drug leaflets and regulatory document genre (QUAERO-D1, QUAERO-D2, QUAERO-D9)
  - Contains INN drug names, excipient lists, E-number entries, posology sentences, and adverse-event sections in the formulaic register of EU regulatory documents (QUAERO-D3, QUAERO-D4, QUAERO-D7, QUAERO-D8)
  - Safety warning and contraindication phrasing present (QUAERO-D5, QUAERO-D6)
  - Formal written metropolitan French regulatory register confirmed by EMEA and European Commission marketing authorization references (QUAERO-D9, QUAERO-D10)
- **Key concerns:**
  - UMLS Semantic Group scheme (CHEM, DISO, PROC…) collapses INN, excipient, brand name, and ATC code under CHEM; ATC code strings themselves are unlabeled (QUAERO-D11, QUAERO-D12, QUAERO-D14) — critical mismatch with regulatory entity taxonomy
  - Nested entity simplification loses 6.06% of EMEA annotations, including clinically and legally significant nested structures (QUAERO-D13)
  - Document splitting produces linguistically vacuous fragment artifacts (QUAERO-D15, QUAERO-D16, QUAERO-D17)
  - At least one apparent annotation error: pharmaceutical company name annotated as DISO (QUAERO-D18)
  - No STS task; contributes nothing to compliance-checking similarity evaluation
  - No tropical disease or French overseas territories content (QUAERO-C6)
  - Annotation by NLP/clinical researchers, not regulatory affairs specialists (QUAERO-C4)

---

#### DrBenchmark/FrenchMedMCQA

- **Task:** Multiple-choice question answering (MCQA), single and multiple correct answers
- **Deployment fit:** Weak — The dataset tests pharmacy knowledge recall in exam format, which is categorically distinct from the NER and STS tasks the deployment requires. Task type mismatch is categorical and irremediable for NER/STS evaluation purposes, though pharmaceutical vocabulary partially overlaps with deployment needs.
- **Key strengths:**
  - Contains French pharmaceutical and pharmacovigilance vocabulary (INNs, drug safety, contraindications, adverse effects) partially overlapping with regulatory labeling vocabulary (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D2, FRENCHMEDMCQA-D6)
  - One correct answer explicitly references the *résumé des caractéristiques du produit* (SmPC), demonstrating regulatory document awareness in the content (FRENCHMEDMCQA-D3)
  - Multi-answer MCQA format tests multi-label discrimination, broadly analogous to multi-label classification tasks (FRENCHMEDMCQA-D9)
  - Consistent formal written French register (FRENCHMEDMCQA-D10)
- **Key concerns:**
  - Categorical task mismatch: MCQA cannot evaluate NER or STS components central to the deployment
  - Exam question format (true/false propositions about biomedical facts) is structurally absent from regulatory document processing workflows (FRENCHMEDMCQA-D11, FRENCHMEDMCQA-D12)
  - No sentence-pair similarity, no entity span annotation
  - Ground-truth answers reflect academic pharmacological consensus, not regulatory-legal compliance standards (FRENCHMEDMCQA-D15)
  - Subset of content peripheral to pharmaceutical regulation (nuclear physics, zoology) (FRENCHMEDMCQA-D16)

---

#### DrBenchmark/DEFT2020

- **Task:** Semantic textual similarity (STS) scoring (Task 1: 0–5 continuous scale; Task 2: retrieval classification)
- **Deployment fit:** Partial — The only STS dataset in DrBenchmark with confirmed drug leaflet sentence pairs, making it the most relevant resource for the compliance-checking STS component. However, a large proportion of pairs derives from encyclopedic non-medical content, the scoring rubric is not calibrated for regulatory-legal equivalence, and annotation authority lacks regulatory expertise.
- **Key strengths:**
  - Drug leaflet and regulatory-adjacent sentence pairs present, covering breastfeeding contraindications, driving-safety warnings, excipient contraindications, storage instructions, and pharmaceutical form descriptions (DEFT2020-D1, DEFT2020-D2, DEFT2020-D3, DEFT2020-D5, DEFT2020-D6)
  - Five-score arrays per pair enable inter-annotator disagreement analysis relevant to human-in-the-loop adjudication design (DEFT2020-D7)
  - Annotator disagreement on pharmaceutical pairs with safety-relevant omissions is empirically visible (DEFT2020-D8, DEFT2020-D16)
  - Standard written French throughout
- **Key concerns:**
  - Large fraction (~40–50% of sample) derives from encyclopedic non-biomedical content (beekeeping, sports, geography, historical figures), diluting domain signal (DEFT2020-D11, DEFT2020-D12, DEFT2020-D13, DEFT2020-D14, DEFT2020-D15) — confirmed by benchmark YAML Q21
  - STS 0–5 scale does not distinguish legally consequential small-magnitude differences: omission of "par mesure de précaution," qualifier loss ("opiacé"), and omission of co-substances (alcohol, hypnotics) are scored as highly similar (DEFT2020-D16, DEFT2020-D17, DEFT2020-D18)
  - No SmPC, CTD module, or ANSM-specific document genre (DEFT2020-D21)
  - Annotation by general (non-regulatory) annotators (DEFT2020-D19)
  - No overseas territory or tropical pathology content

---

#### DrBenchmark/MORFITT

- **Task:** Multi-label medical specialty classification (12 classes)
- **Deployment fit:** Weak — Entirely composed of PMC Open Access research abstracts classified by academic specialty. Task type (multi-label specialty assignment) does not match NER or STS requirements; source genre (scientific abstract) is absent from the deployment's document types; label space (academic specialties) has no overlap with regulatory entity ontology.
- **Key strengths:**
  - Pharmacology-labeled abstracts contain drug dosing and pharmaceutical vocabulary (MORFITT-D3, MORFITT-D4)
  - One abstract covers chikungunya in the Indian Ocean region, providing incidental tropical disease vocabulary (MORFITT-D7)
  - Multi-label annotation scheme demonstrates genuine multi-specialty overlap (MORFITT-D6)
  - Consistent formal French biomedical prose register
- **Key concerns:**
  - No regulatory document genre represented; all content is academic research abstract format (MORFITT-D8, MORFITT-D9)
  - Label space (microbiology, virology, surgery, etc.) is orthogonal to regulatory entity ontology and NER/STS tasks (MORFITT-D10)
  - Substantial proportion of abstracts concern non-metropolitan-France populations (Canada, Egypt, Saudi Arabia, Jordan) (MORFITT-D12, MORFITT-D13, MORFITT-D14, MORFITT-D15)
  - Veterinary medicine content present across multiple labels (MORFITT-D16, MORFITT-D17)
  - No annotation authority documentation or inter-annotator agreement for this dataset

---

#### DrBenchmark/CLISTER

- **Task:** Semantic textual similarity (STS), regression (0–5 continuous score)
- **Deployment fit:** Partial — The only dedicated French clinical STS dataset with 1,000 annotated sentence pairs and a well-distributed scoring range. However, source genre is exclusively clinical case narratives (not regulatory documents), the scoring rubric treats structural similarity as high similarity regardless of numerical or temporal differences that would be legally consequential, and annotation authority lacks regulatory expertise.
- **Key strengths:**
  - Full 0–5 distribution with non-integer averaged scores, confirming genuine inter-annotator variability and a continuous regression target (CLISTER-D1, CLISTER-D2, CLISTER-D3, CLISTER-D4)
  - Drug dosage sentence pairs present, partially relevant to posology vocabulary (CLISTER-D5, CLISTER-D6, CLISTER-D7)
  - Demonstrates sensitivity to some fine-grained numerical differences (CLISTER-D10)
  - Consistent French clinical register throughout (CLISTER-D8)
- **Key concerns:**
  - Exclusively clinical case report genre; no regulatory document text (CLISTER-D11, CLISTER-D12)
  - Scoring rubric treats substantially different follow-up durations (2 years vs. 4.5 years) as highly similar (4.0) (CLISTER-D13); numerical differences that would be legally consequential in posology contexts are not flagged
  - Tabular and fragmented clinical data introduces noise absent from regulatory prose (CLISTER-D19, CLISTER-D20)
  - Annotation authority gap: no regulatory affairs expertise documented (CLISTER-D17)
  - No tropical disease or overseas territory content; isolated Buruli ulcer reference is incidental (CLISTER-D18)

---

#### DrBenchmark/MANTRAGSC

- **Task:** Biomedical NER (token classification), UMLS Semantic Group labels
- **Deployment fit:** Partial (with significant caveats) — Contains a French EMEA drug label subset (`fr_emea`) directly relevant to the deployment, but the sampled split (`fr_medline`) covers historical MEDLINE biomedical titles with clinical-research rather than regulatory content. The EMEA and Patents configurations warrant separate assessment. The shared UMLS Semantic Group label scheme limits regulatory entity granularity across all configurations.
- **Key strengths:**
  - French EMEA drug label and patents subsets exist in the same repository and use the same NER schema, providing the closest available parallel to regulatory NER (MANTRAGSC-S3)
  - Drug/chemical entity annotation present in sampled content (MANTRAGSC-D1, MANTRAGSC-D2)
  - Consistent IOB2/SeqEval evaluation format (MANTRAGSC-S4)
- **Key concerns:**
  - Sampled split (`fr_medline`) consists of historical MEDLINE biomedical titles, not regulatory documents (MANTRAGSC-D5, MANTRAGSC-D6, MANTRAGSC-D7)
  - No regulatory entity types (INNs, ATC codes, posology templates, contraindication qualifiers) in the label scheme (MANTRAGSC-D8, MANTRAGSC-D9)
  - Very small dataset size (~100 examples per configuration); CamemBERT models produce only 'O' labels on small Mantra-GSC splits (benchmark YAML Q73), confirming practical limitations
  - Historical and non-metropolitan French content in sampled split (MANTRAGSC-D10, MANTRAGSC-D11, MANTRAGSC-D13, MANTRAGSC-D14)
  - UMLS Semantic Groups collapse regulatory-legally distinct entity categories (MANTRAGSC-D12, MANTRAGSC-C6)
  - No inter-annotator agreement reported for this dataset

---

#### DrBenchmark/E3C

- **Task:** NER (token classification), clinical entity recognition and temporal/factuality annotation
- **Deployment fit:** Weak — The French clinical NER configuration annotates only CLINENTITY (pathologies, signs, symptoms), systematically leaving drug names, dosages, and administration routes unannotated. All content is clinical case narrative. Several examples suggest non-metropolitan French (North African, sub-Saharan African) clinical contexts.
- **Key strengths:**
  - Drug names and dosages present in text, confirming French biomedical vocabulary exists in the corpus (E3C-D2, E3C-D5, E3C-D6)
  - Multi-pathology clinical entity labeling relevant to clinical NLP (E3C-D3, E3C-D4)
  - Consistent formal written French clinical register
- **Key concerns:**
  - Drug/dosage entities systematically unlabeled (all tagged O); label space restricted to CLINENTITY (E3C-D5, E3C-D6, E3C-D7)
  - All content is clinical case report genre; no regulatory document text (E3C-D8, E3C-D9)
  - Several examples indicate non-metropolitan French clinical contexts (Morocco, sub-Saharan Africa) (E3C-D10, E3C-D11, E3C-D12)
  - Notable annotation gaps visible: disease names tagged O where annotation would be expected (E3C-D13, E3C-D14)
  - Tokenization encoding artifacts in some examples (E3C-D15, E3C-D16)
  - No inter-annotator agreement reported

---

#### DrBenchmark/PxCorpus

- **Task:** Intent classification (4 classes) and NER (38 classes) on drug prescription transcripts
- **Deployment fit:** Partial — Contains the most fine-grained posology NER schema in the benchmark and explicitly models prescription correction operations (replace/negate intents). However, the source genre is spoken prescription dictation transcripts, which are structurally and linguistically incompatible with the formal written regulatory documents the deployment processes; extensive transcription noise pervades the data.
- **Key strengths:**
  - Rich pharmaceutical vocabulary: INNs, brand names, and complete posology expressions (dose + form + route + frequency + duration) co-occur in single utterances (PXCORPUS-D1, PXCORPUS-D2, PXCORPUS-D3)
  - Fine-grained 38-class NER scheme captures posology parameters relevant to detecting labeling inconsistencies (PXCORPUS-D7, PXCORPUS-D8)
  - Intent classes directly model prescription modification and correction operations (PXCORPUS-D9, PXCORPUS-D10, PXCORPUS-D11)
  - Diverse posology patterns: PRN, weight-based, alternating-day, concentration-expressed (PXCORPUS-D4, PXCORPUS-D5, PXCORPUS-D6)
- **Key concerns:**
  - Source genre is spoken dictation transcripts, not written regulatory documents; pervasive transcription noise (ASR artifacts, expletives, code-switching, system prompts) (PXCORPUS-D13, PXCORPUS-D14, PXCORPUS-D15, PXCORPUS-D16, PXCORPUS-D17, PXCORPUS-D22)
  - No STS task
  - Severe class imbalance: `replace` class (most relevant to inconsistency detection) has ~0.6% of examples; `negate` ~2.2% (PXCORPUS-D18)
  - NER scheme does not cover ATC codes, excipient names, contraindication qualifiers, or population-subgroup safety qualifiers (PXCORPUS-D19, PXCORPUS-D20)
  - Annotation reflects training simulation, not authentic clinical or regulatory prescribing (PXCORPUS-D23, PXCORPUS-D24)

---

#### DrBenchmark/DiaMED

- **Task:** Multi-label ICD-10 chapter-level document classification (22 classes)
- **Deployment fit:** Weak — Purpose-built for DrBenchmark but draws from the Pan African Medical Journal, producing clinical cases with geographic provenance predominantly from sub-Saharan Africa. Task type (document classification) does not match NER or STS requirements; ICD-10 chapter labels are clinical diagnostic axes, not regulatory compliance categories.
- **Key strengths:**
  - Full French-language clinical prose with broad ICD-10 chapter coverage (22 classes) (DIAMED-D1, DIAMED-D2)
  - Inter-annotator agreement documented with Cohen's Kappa and Gwet's AC1 — the most rigorously documented annotation process in the benchmark
  - CC-BY 4.0 license with open-access provenance
- **Key concerns:**
  - Pan African provenance confirmed: cases from Burkina Faso, Morocco, Niger, and other sub-Saharan African institutions (DIAMED-D9, DIAMED-D12); disease profiles, formulary conventions, and healthcare infrastructure diverge substantially from metropolitan France
  - No regulatory document genre; all content is clinical case narrative (DIAMED-D3, DIAMED-D7)
  - ICD-10 chapter-level classification does not match NER or STS deployment tasks
  - No tropical disease terminology specifically calibrated to French overseas territories (dengue, chikungunya, paludisme) despite Pan African origin
  - Very small class representation for rare ICD-10 chapters (DIAMED-D5)
  - Annotation by general clinicians and medical expert, no regulatory affairs specialist

---

#### DrBenchmark/DEFT2021

- **Task:** NER (13 entity types including DOSAGE, SUBSTANCE, TREATMENT, PATHOLOGY) and multi-label MeSH classification (23 axes)
- **Deployment fit:** Partial — The NER configuration provides the most clinically fine-grained drug-entity annotation in the benchmark, with SUBSTANCE, DOSAGE, FREQUENCY, MODE, and DURATION tags that partially overlap with regulatory NER requirements. However, all content is clinical case narrative; the NER scheme does not distinguish INN from brand name or cover ATC/excipient categories; and MeSH Chapter C classification labels are clinical disease taxonomy rather than regulatory compliance axes.
- **Key strengths:**
  - Fine-grained 13-class NER scheme covering DOSAGE, DURATION, FREQUENCY, MODE, SUBSTANCE, TREATMENT, PATHOLOGY — closest NER label alignment with regulatory posology entity types (DEFT2021-D2, DEFT2021-D3, DEFT2021-D6)
  - Drug names, dosage expressions, and posology structures densely annotated in authentic clinical French (DEFT2021-D1, DEFT2021-D4)
  - Gold-standard manual annotation (YAML Q25)
  - Medication error case present, demonstrating sensitivity to dose-level distinctions (DEFT2021-D14)
- **Key concerns:**
  - All content is clinical case narrative; no regulatory document genre (DEFT2021-D7, DEFT2021-D8)
  - NER scheme conflates INN and brand names under SUBSTANCE; surgical and pharmacological treatments undistinguished under TREATMENT (DEFT2021-D9, DEFT2021-D10)
  - DOSAGE annotation does not distinguish stated dose, prescribed dose, and safety threshold (DEFT2021-D14)
  - Non-metropolitan French content present (Madagascar travel, African residency references) (DEFT2021-D12, DEFT2021-D13)
  - MLC labels are MeSH Chapter C disease axes, not regulatory compliance categories (DEFT2021-D11)
  - Annotation authority: clinical/NLP professionals, no regulatory affairs expertise

---

#### DrBenchmark/CAS

- **Task:** POS tagging (31 classes, silver-standard), negation/speculation classification (4 classes)
- **Deployment fit:** Weak — Contributes POS tagging and negation/speculation classification on clinical case text. POS labels are silver-standard (automatic). Neither task evaluates regulatory NER entity types or STS compliance scoring. The negation/speculation classification layer has indirect relevance for safety-warning interpretation.
- **Key strengths:**
  - Drug names, dosage expressions, and quantitative clinical values present in French clinical case text (CAS-D3, CAS-D4, CAS-D5, CAS-D7)
  - Negation and speculation classification labels capture linguistically important epistemic modality relevant to flagging negated contraindications (CAS-D10, CAS-D11)
  - Dense, authentic French clinical prose from 3,790 cases, providing large-scale vocabulary coverage
  - Exposure threshold phrasing present, incidentally relevant to safety-related numerical extraction (CAS-D9)
- **Key concerns:**
  - POS labels are silver-standard (automatic Tagex 3, 98% precision validation) — not gold-standard adjudicated (CAS-D16, CAS-D17)
  - No regulatory document genre; clinical case narrative throughout (CAS-D12, CAS-D13)
  - INN/ATC/excipient nomenclature absent from systematic coverage; drug mentions are incidental (CAS-D14, CAS-D15)
  - No STS task
  - Patient-reported speech (informal colloquial register) present alongside clinical prose (CAS-D20, CAS-D21)
  - Some possible non-metropolitan French content (leptospirosis, waterborne exposure) (CAS-D18, CAS-D19)

---

#### DrBenchmark/ESSAI

- **Task:** POS tagging (41 classes, silver-standard), negation/speculation classification (4 classes)
- **Deployment fit:** Partial — Clinical trial protocols constitute a biomedical document genre that is closer to regulatory submissions than clinical case narratives, and the corpus contains rich posology vocabulary with INN drug names, dosing schedules, and patient-addressed language partially resembling PIL text. However, the therapeutic scope is almost exclusively oncology, the annotation is silver-standard, and no STS task exists.
- **Key strengths:**
  - Dense INN drug name and posology vocabulary covering frequency, route, and duration expressions in French (ESSAI-D1, ESSAI-D2, ESSAI-D5, ESSAI-D6, ESSAI-D7)
  - Patient-addressed register ("vous") partially overlaps with patient information leaflet genre (ESSAI-D11, ESSAI-D12)
  - Negation/speculation labels capture contraindication and eligibility criterion signaling (ESSAI-D8, ESSAI-D9, ESSAI-D10)
  - Marketing authorization (AMM) terminology present, the closest regulatory signal in the sample (ESSAI-D13)
- **Key concerns:**
  - Narrow therapeutic scope: virtually all sampled examples concern oncology; non-oncology regulatory vocabulary absent (ESSAI-D18, ESSAI-D19, ESSAI-D20)
  - Clinical trial protocol genre, not SmPC/PIL/CTD regulatory submission format (ESSAI-D14, ESSAI-D15)
  - NER label space (negation/speculation only) does not map to regulatory entity types — drug names present but without INN-specific schema (ESSAI-D16, ESSAI-D17)
  - Silver-standard POS annotation via TreeTagger (ESSAI-D21)
  - No STS task
  - No overseas territory or tropical pathology content

---

### Cross-Cutting Strengths

**1. Formal written French biomedical register is consistent across all datasets**
Every dataset provides standard written French in a biomedical or clinical register, with no cross-script, cross-lingual, or audio modality issues. QUAERO-D9, CLISTER-D8, ESSAI-D11, CAS-D1, and DEFT2021-D5 all confirm that the Input Form (IF) dimension is well-matched to the deployment's metropolitan France text infrastructure. This eliminates an entire validity concern category.

**2. Pharmaceutical and posology vocabulary is substantially represented across multiple datasets**
Drug names (INNs and brand names), dosage expressions, routes of administration, and frequency patterns appear across QUAERO (QUAERO-D7, QUAERO-D8), PxCorpus (PXCORPUS-D1, PXCORPUS-D2), DEFT2021 (DEFT2021-D2, DEFT2021-D3), CAS (CAS-D3, CAS-D7), ESSAI (ESSAI-D5, ESSAI-D6), and DEFT2020 (DEFT2020-D3, DEFT2020-D5). This provides a non-trivial vocabulary signal for pharmaceutical NLP models, even if the entity-typing granularity is insufficient for regulatory compliance.

**3. Drug safety and adverse event content present in multiple datasets**
Contraindication language, adverse reaction listings, drug interaction warnings, and safety-population qualifiers appear across QUAERO (QUAERO-D5, QUAERO-D6), DEFT2020 (DEFT2020-D2, DEFT2020-D3), FrenchMedMCQA (FRENCHMEDMCQA-D6), and DEFT2021 (DEFT2021-D6). This confirms that pharmacovigilance-relevant content is distributed across the benchmark, even if not specifically annotated for regulatory compliance purposes.

**4. Two STS datasets provide baseline similarity scoring infrastructure for French biomedical text**
CLISTER and DEFT2020 together provide approximately 2,010 annotated French biomedical sentence pairs with multi-annotator scores. The existence of inter-annotator score arrays in DEFT2020 (DEFT2020-D7, DEFT2020-D8) enables analysis of annotation disagreement, supporting the deployment's human-in-the-loop adjudication design, even if the scoring rubric is not calibrated for regulatory equivalence.

**5. Negation and speculation classification available in two clinical corpora**
CAS (CAS-D10, CAS-D11) and ESSAI (ESSAI-D8, ESSAI-D9, ESSAI-D10) both provide negation/speculation classification labels on French clinical and trial protocol text. These labels are relevant to detecting negated contraindications and speculative safety claims — sub-tasks within the broader compliance-checking workflow.

---

### Cross-Cutting Weaknesses

#### CRITICAL

**1. Regulatory document genre absent from all STS tasks (IO, OO) — across CLISTER and DEFT2020**
Neither STS dataset contains SmPC, PIL, or CTD module text as a primary source. CLISTER is exclusively clinical case narratives (CLISTER-D11, CLISTER-D12). DEFT2020 contains drug leaflet pairs but they are a minority within a largely encyclopedic dataset (DEFT2020-D11 through DEFT2020-D15). No STS task is framed around the deployment's core use case: comparing safety warning phrasings between document versions for regulatory equivalence. The confirmed variation type classification (IA/IB/II) framework — establishing that even minor text changes in French drug labeling require formal regulatory variation submissions — means this gap is directly operationally consequential.

**2. STS scoring rubric is not calibrated for regulatory-legal equivalence (OO, OC) — across CLISTER and DEFT2020**
Both STS datasets use a coarse 0–5 Likert-style general semantic proximity scale. Empirical evidence across both datasets confirms the rubric cannot distinguish legally consequential small-magnitude differences from stylistic variants: omission of safety qualifiers (DEFT2020-D16, DEFT2020-D17, DEFT2020-D18), substantially different numerical values scored as highly similar (CLISTER-D13), and dose-expression differences scored by ambiguous rubric (CLISTER-D14). This is the central validity gap for the STS compliance-checking component.

**3. NER entity taxonomies across all datasets are misaligned with regulatory labeling ontology (OO, IC) — across QUAERO, MANTRAGSC, E3C, DEFT2021, PxCorpus**
No dataset annotates INNs as distinct from brand names or other CHEM entities; no dataset annotates ATC codes as entities; no dataset covers excipient nomenclature as a target entity type; no dataset annotates EMA contraindication qualifier phrases at the required granularity. This is confirmed across: QUAERO-D11, QUAERO-D12, QUAERO-D14 (UMLS CHEM collapsing regulatory-legally distinct categories); MANTRAGSC-D8 (drug name annotated at semantic-group level only); E3C-D5 (drug names systematically O); DEFT2021-D10 (INN and brand name both tagged SUBSTANCE without distinction); PXCORPUS-D19 (contraindication qualifier untagged). The absence of a published crosswalk between DrBenchmark NER schemas and EMA/ANSM regulatory annotation guidelines further underscores this gap.

**4. Annotation authority lacks regulatory affairs expertise across all datasets (OC)**
No dataset in DrBenchmark identifies regulatory affairs specialists, pharmacovigilance officers, or legal experts with EMA/ANSM submission experience as annotators. Annotation norms reflect clinical, research, and NLP professional judgment throughout: QUAERO-C4, CLISTER-D17, DEFT2020-D19, DEFT2021-D14, DIAMED annotation (YAML Q45). For a deployment where ground truth rests with regulatory-legal standards, this is a systemic convergent validity concern. It is most consequential for STS equivalence scoring and for NER boundary decisions in safety-critical phrasing.

**5. Regulatory document genre (SmPC, PIL, CTD) absent from all NER tasks except QUAERO EMEA (IO, IC)**
With the exception of QUAERO's EMEA configuration (and the unsampled Mantra-GSC `fr_emea` subset), all NER datasets draw exclusively from clinical case narratives, clinical trial protocols, or research abstracts. E3C (E3C-D8, E3C-D9), DEFT2021 (DEFT2021-D7, DEFT2021-D8), CAS (CAS-D12, CAS-D13), and ESSAI (ESSAI-D14, ESSAI-D15) confirm this pattern. The legally constrained, template-driven language of SmPC sections 4.3 (contraindications), 4.4 (special warnings), 4.8 (adverse reactions), and the PIL equivalents are not represented as evaluation targets.

#### MAJOR

**6. Non-metropolitan French content present across multiple datasets (IC, OC) — DiaMED, E3C, DEFT2021, MORFITT**
Sub-Saharan African clinical provenance is confirmed in DiaMED (DIAMED-D9, DIAMED-D12), present in DEFT2021 (DEFT2021-D12, DEFT2021-D13), and strongly suggested in E3C (E3C-D10, E3C-D11, E3C-D12). Non-French populations (Canadian, Egyptian, Saudi, Jordanian) appear in MORFITT (MORFITT-D12, MORFITT-D13, MORFITT-D14, MORFITT-D15). The deployment targets metropolitan France as primary scope, and the benchmark's African-origin clinical content encodes disease profiles, formulary practices, and healthcare infrastructure references diverging from the French regulatory context.

**7. French overseas territory and tropical pathology vocabulary entirely absent across all datasets (IO, IC)**
Despite the deployment's identified secondary priority of French overseas territories, no dataset contains systematic tropical disease vocabulary (dengue, chikungunya, paludisme, leptospirose, leishmaniose). Incidental mentions appear only in MORFITT-D7 (chikungunya in Indian Ocean) and CAS-D18 (leptospirosis serology). DiaMED's Pan African origin does not produce territory-specific overseas France content. This gap is fully confirmed across the benchmark.

**8. Silver-standard annotation in two POS datasets reduces ground-truth reliability for high-stakes deployment (OC) — CAS and ESSAI**
CAS POS labels are silver-standard via Tagex 3 (CAS-D16, CAS-D17); ESSAI POS labels are silver-standard via TreeTagger (ESSAI-D21). For a deployment where annotation errors propagate into compliance decisions, the ~2% precision gap at scale across 3,790 and 7,247 documents respectively introduces non-trivial noise in the POS evaluation signal.

**9. Multiple datasets have very small size, limiting fine-tuning and evaluation reliability (IO)**
Mantra-GSC French configurations (~100 examples per subset, with confirmed model collapse on small splits — YAML Q73), DEFT2021 NER (~2,712 rows), DiaMED (739 examples across 22 classes with 2 examples in some chapters — DIAMED-D5), and PxCorpus's `replace` class (~0.6% of examples — PXCORPUS-D18) all represent underrepresented evaluation conditions.

#### MINOR

**10. Confidence calibration and score thresholds for human review escalation not benchmarked in any dataset (OF)**
No dataset provides probability calibration data, uncertainty quantification metrics, or documentation of score thresholds that should trigger mandatory human review. DEFT2020's score arrays provide some inter-annotator variance information but no escalation threshold semantics. This gap is confirmed across the benchmark and is operationally relevant given the deployment's human-in-the-loop design for borderline cases.

---

### Content Coverage Summary

**What the benchmark collectively represents well for this deployment:**
- Formal written French in standard biomedical and clinical registers, consistent with metropolitan France text infrastructure (universal across datasets)
- Clinical case narratives in French covering a wide range of pathologies, treatments, and patient presentations (CAS, E3C, DEFT2021, DiaMED, CLISTER)
- Drug name vocabulary (INNs and brand names) and posology expressions in conversational/clinical contexts (PxCorpus, DEFT2021, CAS, ESSAI)
- French pharmacy examination knowledge including drug safety, contraindications, and adverse effects (FrenchMedMCQA)
- Clinical trial protocol language with drug names, dosing schedules, and patient-addressed text partially resembling PIL register (ESSAI)
- A baseline STS evaluation infrastructure for French clinical text (CLISTER, DEFT2020)
- Drug leaflet text at the entity-span level for a limited regulatory vocabulary set (QUAERO EMEA)

**What is well-covered relative to deployment needs:**
- Input Form (IF): fully covered — text-only formal written French with no script, modality, or dialect mismatch
- General French biomedical vocabulary: well-covered across clinical domains
- Drug names as recognizable tokens in French text: well-covered

**What gaps remain relative to deployment needs:**
- Regulatory document genres (SmPC, PIL structured sections, CTD modules, ANSM submission formats): underrepresented; only QUAERO EMEA and (unsampled) Mantra-GSC fr_emea provide any coverage, and only for NER not STS
- Regulatory NER entity taxonomy (INNs as distinct from excipients, ATC codes, EMA contraindication qualifier phrases, MedDRA adverse event terms): absent from all datasets' label schemas
- STS scoring calibrated for regulatory-legal equivalence: absent from all STS datasets — confirmed FULL gap
- Annotation authority from regulatory affairs or pharmacovigilance specialists: absent from all datasets — confirmed FULL gap
- French overseas territory and tropical pathology vocabulary: absent — confirmed FULL gap
- ANSM vs. EMA normative divergence documentation in any annotation guideline: entirely undocumented across the benchmark
- MedDRA preferred term NER: absent; no French-language benchmark equivalent to English ADE Eval exists

---

### Limitations

1. **MANTRAGSC fr_emea and fr_patents not sampled:** The per-dataset analysis sampled only the `fr_medline` split. The `fr_emea` configuration — derived from EMEA drug labels and likely the most relevant Mantra-GSC subset for the deployment — was not directly inspected. Its content and annotation quality cannot be characterized from available evidence.

2. **QUAERO MEDLINE configuration not sampled:** Only the EMEA configuration of QUAERO was analyzed. The MEDLINE configuration (biomedical titles) would likely show weaker regulatory document alignment.

3. **FrenchMedMCQA subject diversity not stratified:** All sampled examples carry `subject_name: "pharmacie"` uniformly; sub-domain distribution (pharmacovigilance, regulatory affairs, galenic pharmacy) cannot be assessed from available fields.

4. **DiaMED inter-annotator agreement numerical values not retrieved:** Specific Kappa and Gwet's AC1 values from Table 4 of the benchmark paper were not surfaced in search results; label reliability at the boundary level cannot be quantified.

5. **Confidence calibration data not assessable:** No dataset provides probability calibration or score-threshold documentation; this dimension cannot be assessed through dataset content inspection alone and requires system documentation review.

6. **Sample-based analysis:** Per-dataset analyses examined 70–250 examples per dataset. Findings reflect patterns visible in those samples; rare edge cases, distributional tails, and minority label behavior may not be represented.

7. **ANSM-specific safety warning content standards:** Deeper divergences between ANSM national circulars and EMA QRD requirements at the level of specific contraindication phrasing remain incompletely documented in publicly available sources, limiting the precision of OO and OC validity assessments for this dimension.

---

### Cited Evidence

- **QUAERO-D1**: QUAERO/EMEA | 1 | CHEM | "Phosphate de sodium , monobasique , monohydraté Phosphate de sodium , dibasique , heptahydraté Chlorure de sodium Polysorbate 80 ( E433 ) Eau pour préparation injectable" | Excipient list with E-numbers from drug composition section — confirms regulatory document genre | IC
- **QUAERO-D2**: QUAERO/EMEA | 55 | CHEM/PROC/OBJC | "TYSABRI 300 mg solution à diluer pour perfusion natalizumab Chaque flacon de 15 ml de concentré contient 300 mg de natalizumab ( 20 mg / ml ) ; phosphate de sodium ... polysorbate 80 ( E433 ) et eau pour préparation injectable" | Full SmPC composition section with INN, dosage, excipients | IC
- **QUAERO-D3**: QUAERO/EMEA | 51 | CHEM | "REFLUDAN ... Refludan ... lépirudine" | Brand name and INN co-annotated as CHEM in same document | IC, OO
- **QUAERO-D4**: QUAERO/EMEA | 95 | CHEM | "Agent antithrombotique – inhibiteur direct de la thrombine , code ATC : La lépirudine ... est une hirudine recombinante" | ATC code reference in context; INN tagged CHEM | IC, OO
- **QUAERO-D5**: QUAERO/EMEA | 6 | DISO | "Des épisodes de troubles psychiatriques aigus , tels que hallucinations , réactions paranoïdes , hostilité , délire , psychose et réactions maniaques ont été rapportés chez des patients traités par le ziconotide" | Adverse psychiatric reaction listing in regulatory adverse-event format | IC
- **QUAERO-D6**: QUAERO/EMEA | 64 | DISO/CHEM | "Si vous avez des perturbations graves du système immunitaire ( dues à une maladie , telle que leucémie ou infection à VIH" | Contraindication phrasing in patient-directed leaflet register | IC
- **QUAERO-D7**: QUAERO/EMEA | 32 | CHEM/PROC | "la dose maximale prévue de ziconotide administré par voie intrarachidienne était de 912 µg / jour" | Dose threshold with route of administration — legally sensitive regulatory content | IC, OO
- **QUAERO-D8**: QUAERO/EMEA | 129 | CHEM/PROC | "TYSABRI 300 mg est administré en perfusion intraveineuse une fois toutes les 4 semaines" | Canonical posology sentence with dose, route, and frequency | IC
- **QUAERO-D9**: QUAERO/EMEA | 37 | GEOG | "La Commission européenne a délivré une autorisation de mise sur le marché valide dans toute l ' Union européenne pour Tysabri ... le 27 juin 2006" | EU marketing authorization reference confirming regulatory document genre | IC, IF
- **QUAERO-D10**: QUAERO/EMEA | 12 | GEOG | "informations détaillées sur ce médicament sont disponibles sur le site internet de l ' Agence européenne du médicament ( EMEA )" | EMEA provenance reference | IC
- **QUAERO-D11**: QUAERO/EMEA | 95 | CHEM | "Agent antithrombotique – inhibiteur direct de la thrombine , code ATC : La lépirudine ... est une hirudine recombinante" | ATC code string unlabeled (tag=0); INN and endogenous enzyme both CHEM — scheme collapses regulatory-legally distinct categories | OO
- **QUAERO-D12**: QUAERO/EMEA | 1 | CHEM | "Phosphate de sodium ... Polysorbate 80 ( E433 ) ... Eau pour préparation injectable" | Excipients and solvents all CHEM, indistinguishable from active substance | OO
- **QUAERO-D13**: QUAERO/EMEA | 38 | DISO | "sclérose en plaques ( SEP ) ... troubles de la marche , engourdissement du visage , des bras ou des jambes , problèmes de vue , fatigue" | Long symptom enumeration where nested disease-symptom relationships lost in flat IOB2 | IC, OC
- **QUAERO-D14**: QUAERO/EMEA | 95 | O (for ATC) | "code ATC" | ATC code string itself has tag=0 (unlabeled), indicating regulatory identifier strings not treated as entities | OO, OC
- **QUAERO-D15**: QUAERO/EMEA | 41 | O | "o ." | Single-character fragment artifact from document splitting | IC, IF
- **QUAERO-D16**: QUAERO/EMEA | 92 | O | "4 ." | Section number artifact with no standalone regulatory content | IC, IF
- **QUAERO-D17**: QUAERO/EMEA | 111 | O | "4 et 4 ." | Cross-reference fragment artifact from document splitting | IC, IF
- **QUAERO-D18**: QUAERO/EMEA | 117 | DISO (apparent error) | "Richter Gedeon Eesti filiaal ... Polska Gedeon Richter Plc" | Pharmaceutical company name annotated as DISO — likely annotation error | OC
- **FRENCHMEDMCQA-D1**: FrenchMedMCQA | 11 | simple | "L'AMPHOTERICINE B : Est un antifongique de la famille des polyènes... N'est pas absorbée par la muqueuse digestive... Est néphrotoxique après perfusion au long cours" | Drug safety/pharmacology question covering antifungal classification and nephrotoxicity risk | IC
- **FRENCHMEDMCQA-D2**: FrenchMedMCQA | 70 | multiple | "Les anti-vitamines K (AVK) sont formellement contre-indiquées avec : Le miconazole (DAKTARIN®), Les salicylés à fortes doses" | Formal contraindication language with brand name, resembling SmPC contraindication section | IC
- **FRENCHMEDMCQA-D3**: FrenchMedMCQA | 105 | simple | "Le mésusage est défini comme... Une utilisation de médicament non conforme aux recommandations du résumé des caractéristiques du produit" | Correct answer explicitly references the SmPC (résumé des caractéristiques du produit) — direct regulatory document awareness | IC, OC
- **FRENCHMEDMCQA-D4**: FrenchMedMCQA | 6 | simple | "Parmi les substances suivantes, une seule ne traverse pas la barrière placentaire. Laquelle? Dicoumarine / Glucose / Héparine" | Placental barrier drug penetration — safety content analogous to SmPC section 4.6 (pregnancy) | IC
- **FRENCHMEDMCQA-D5**: FrenchMedMCQA | 34 | multiple | "Cocher le ou les antibiotique(s) dont l'utilisation est autorisée en fin de grossesse : Ampicilline / Tétracyclines / Erythromycine / Péfloxacine" | Pregnancy-safe antibiotic identification — mirrors patient leaflet safety restriction content | IC
- **FRENCHMEDMCQA-D6**: FrenchMedMCQA | 44 | multiple | "Cotrimoxazole: Peut entraîner des troubles cutanés sévères type syndrome de Lyell... l'association avec le méthotrexate est contre-indiquée" | Severe ADR (Lyell syndrome) and drug interaction contraindication — direct pharmacovigilance relevance | IC, OC
- **FRENCHMEDMCQA-D7**: FrenchMedMCQA | 50 | multiple | "Parmi les verres suivants, indiquez ceux qui peuvent être utilisés comme conditionnement réutilisable des préparations pour usage parentéral : Verre de type I / Verre borosilicaté" | Container specification for parenteral preparations — regulatory submission/labeling content | IC
- **FRENCHMEDMCQA-D8**: FrenchMedMCQA | 100 | multiple | "Parmi les formes solides orales suivantes, indiquer celle(s) qui libère(nt) le principe actif de façon continue : Matrice hydrophile / Comprimé à enrobage par film insoluble" | Drug delivery system classification — relevant to formulation sections in regulatory dossiers | IC
- **FRENCHMEDMCQA-D9**: FrenchMedMCQA | 4 | multiple (4 correct) | "L'acétylcholine est libérée par : Les neurones sympathiques préganglionnaires / Les neurones parasympathiques préganglionnaires / Les neurones parasympathiques postganglionnaires / Les motoneurones" | Four-correct-answer item testing multi-label discrimination — format analogous to multi-label classification tasks | OO
- **FRENCHMEDMCQA-D10**: FrenchMedMCQA | 43 | multiple | "L'économie médicale est une économie : De service de santé... Caractérisée par le libre choix des médecins par le malade" | Formal French administrative/medical economics vocabulary — consistent with deployment register | IF
- **FRENCHMEDMCQA-D11**: FrenchMedMCQA | 8 | multiple | "La trinitrine: Est le trinitrate d'isosorbide / Est un médicament anti-angoreux / S'utilise par voie orale dans le traitement de la crise d'angor" | Exam false-statement discrimination task — didactic format categorically different from regulatory prose | IO, IF
- **FRENCHMEDMCQA-D12**: FrenchMedMCQA | 37 | simple | "Les 3 nucléides de l'hydrogène, H(A=1,Z=1), H(A=2,Z=1) et H(A=3,Z=1) sont : Des isotones / Des isobares / Des isotopes" | Nuclear physics exam question — minimal relevance to regulatory labeling compliance | IC
- **FRENCHMEDMCQA-D13**: FrenchMedMCQA | 72 | multiple | "ceftriaxone (ROCEPHINE®): C'est une céphalosporine de 3ème génération... Son importante demi-vie d'élimination est compatible avec une seule administration quotidienne" | INN + brand name in exam context, not as labeled entity in regulatory prose | IC, OO
- **FRENCHMEDMCQA-D14**: FrenchMedMCQA | 118 | multiple | "Les comprimés gastrorésistants pelliculés: Doivent se désagréger en 60 mn au moins à pH 6,8... Doivent répondre à l'essai d'uniformité de masse" | Pharmaceutical quality control content in exam format — not continuous regulatory document prose | IC, IF
- **FRENCHMEDMCQA-D15**: FrenchMedMCQA | 61 | simple | "La certification des établissements de santé: Ne concerne que les établissements de santé publics / Concerne tous les établissements de santé / Est facultative" | French health system certification regulation — exam knowledge item, no regulatory document provenance | OC
- **FRENCHMEDMCQA-D16**: FrenchMedMCQA | 37 | simple | "Les 3 nucléides de l'hydrogène, H(A=1,Z=1), H(A=2,Z=1) et H(A=3,Z=1) sont : Des isotones / Des isotopes / Des isothermes" | Atomic physics — peripheral to pharmaceutical regulation | IC
- **DEFT2020-D1**: DEFT2020 | 192 | 4.0 | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter pendant la durée du traitement." | Drug leaflet breastfeeding safety warning — deployment-relevant regulatory text | IC
- **DEFT2020-D2**: DEFT2020 | 218 | 4.5 | "Il convient d'attirer l'attention des conducteurs ou utilisateurs de machines sur les risques de troubles visuels attachés à l'utilisation de ce médicament." | Canonical driving-safety warning from patient leaflet | IC
- **DEFT2020-D3**: DEFT2020 | 203 | 4.6 | "En raison de la présence de lactose, ce médicament est contre-indiqué en cas de galactosémie congénitale, de syndrome de malabsorption du glucose et du galactose ou de déficit en lactase." | Excipient contraindication with technical regulatory vocabulary | IC
- **DEFT2020-D4**: DEFT2020 | 122 | 4.4 | "Comprimé rond, blanc, biconvexe, gravé 6 sur une face, une flèche étant gravée sur l'autre face." | Pharmaceutical form description typical of drug monographs | IC
- **DEFT2020-D5**: DEFT2020 | 79 | 4.7 | "L'allaitement doit être interrompu en cas de traitement par capécitabine." | Formulaic breastfeeding contraindication from patient leaflet | IC
- **DEFT2020-D6**: DEFT2020 | 10 | 4.3 | "A conserver à l'abri de l'humidité." | Storage instruction paraphrase — drug leaflet compliance STS pair | IC, OO
- **DEFT2020-D7**: DEFT2020 | 192 | 4.0 | "scores: [5.0, 2.0, 4.0, 4.0, 5.0]" | Wide annotator spread on safety instruction; relevant to human adjudication design | OC
- **DEFT2020-D8**: DEFT2020 | 79 (Ex.16) | 4.0 | "Ce produit peut provoquer un syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après la dernière prise de stupéfiant." | Safety-relevant pair with annotator disagreement on specificity of "opiacé" qualifier | OC, OO
- **DEFT2020-D9**: DEFT2020 | 129 | 4.8 | "Deux essais (106 participants) comparaient l'héparine de bas poids moléculaire à un placebo ou à l'absence de traitement." | Clinical trial summary — biomedical register alignment | IC
- **DEFT2020-D10**: DEFT2020 | 48 | 4.3 | "Le phénobarbital pourrait prévenir les lésions ischémiques ou réduire les fluctuations de tension artérielle et du débit sanguin dans le cerveau." | Drug mechanism phrasing — biomedical register | IC
- **DEFT2020-D11**: DEFT2020 | 6 | 0.4 | "Certains apiculteurs sélectionnent leurs reines afin de favoriser au mieux la production." | Beekeeping topic — irrelevant to regulatory deployment | IO, IC
- **DEFT2020-D12**: DEFT2020 | 3 | 2.1 | "Boris Fiodorovitch Godounov...gouverne la Russie à partir de 1594 à la place de Féodor Ier..." | Russian historical figure — irrelevant to regulatory deployment | IO, IC
- **DEFT2020-D13**: DEFT2020 | 60 | 0.8 | "Les Canadiens de Montréal sont une franchise de hockey sur glace professionnel située à Montréal dans la province de Québec au Canada." | Ice hockey franchise — irrelevant to regulatory deployment | IO, IC
- **DEFT2020-D14**: DEFT2020 | 5 | 4.3 | "Caudry est une commune française d'environ 15 000 habitants située dans le sud du département du Nord en région Hauts-de-France." | French commune geography — irrelevant | IO, IC
- **DEFT2020-D15**: DEFT2020 | 1 | 0.5 | "Entre Perpignan et Villefranche, il subsiste de très nombreux poteaux caténaires datant des premiers essais en 12 KV 16 2/3 Hz..." | Railway electrification — irrelevant | IO, IC
- **DEFT2020-D16**: DEFT2020 | 192 | 4.0 | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter..." vs. "Il convient d'éviter d'allaiter pendant la durée du traitement." | Omission of "par mesure de précaution" scored 2–5; regulatory significance not captured | OO
- **DEFT2020-D17**: DEFT2020 | 16 | 4.0 | "Ce produit peut provoquer un syndrome de sevrage opiacé..." vs. "Ce produit peut entraîner un syndrome de sevrage s'il est administré moins de 4 heures après la prise d'un stupéfiant..." | Loss of "opiacé" qualifier averaged as 4.0 — regulatory specificity difference not flagged | OO
- **DEFT2020-D18**: DEFT2020 | 130 | 3.8 | "L'association avec d'autres médicaments sédatifs doit être déconseillée..." vs. "L'association avec d'autres médicaments sédatifs ou hypnotiques, et bien entendu avec l'alcool, est déconseillée..." | Omission of alcohol/hypnotics scored ~3.8; safety-relevant omission not distinguished by scale | OO
- **DEFT2020-D19**: DEFT2020 | 19 | 1.3 | "Ketoderm 2 %, gel en récipient unidose peut donc être utilisé au cours de la grossesse." vs. "Qu'est-ce que ketoderm 2 %, gel en récipient unidose et dans quel cas est -il utilisé." | Safety claim vs. classification question; annotators score 0–2 with no regulatory framing | OC
- **DEFT2020-D20**: DEFT2020 | 54 | 5.0 | "Troubles de l'hémostase à type de maladie de Willebrand (se traduisant par un allongement du TCA, du temps de saignement et une diminution des taux du complexe VIIIC/VWF)." | Exact duplicate pair; unanimous 5.0 confirms anchor point but not discriminative regulatory validity | OC, OF
- **DEFT2020-D21**: DEFT2020 | 65 | 4.3 | "- Ne pas utiliser chez les personnes présentant des difficultés de déglutition en raison du risque d'inhalation bronchique et de pneumopathie lipoïde." | Patient-facing leaflet contraindication — not a structured SmPC section 4.3 entry | IO
- **MORFITT-D3**: MORFITT | 2 | 10 (pharmacology) | "La morphine intraveineuse a atténué de façon dose-dépendante les réponses nociceptives chez les souris C57BL/6 et CD-1 (DI 50, 0,6 et 2,5 mg·kg−1, respectivement; P = 0,41)." | Drug dosing content in pharmacology-labeled abstract; closest to regulatory vocabulary | IC
- **MORFITT-D4**: MORFITT | 19 | 7 (chemistry) | "Un test de chromatographie liquide ultra-performante a été développé et validé pour déterminer la stabilité chimique de la sulfadiazine." | Pharmaceutical stability testing; adjacent to drug formulation regulatory topics | IC
- **MORFITT-D6**: MORFITT | 21 | 1, 3, 4 | "Bloquer le complément, notamment l'axe C5a-C5aR1, par des thérapies spécifiques représente un espoir thérapeutique dans les formes les plus sévères de la maladie." | Multi-label instance; confirms multi-label annotation scheme functions as intended | OO
- **MORFITT-D7**: MORFITT | 17 | 2 (virology) | "l'étude de l'épidémie de Chikungunya, un alphavirus transmis par Aedes aegypti et Aedes albopictus, survenue dans l'océan Indien en 2004-2007." | Tropical arboviral disease content; incidental coverage of French overseas territory diseases | IC
- **MORFITT-D8**: MORFITT | 3 | 1 (etiology) | "Des rats ont été assignés aléatoirement à 1 de 3 groupes : un groupe témoin (n = 15), un groupe (n = 15) dans lequel la pancréatite aiguë a été induite au moyen de L-arginine…" | Experimental animal study genre; entirely absent from regulatory document context | IO
- **MORFITT-D9**: MORFITT | 24 | 1 | "Les bronchectasies non liées à la mucoviscidose font l'objet d'un regain d'intérêt… Grâce à de récentes recommandations de bonne pratique, il est maintenant possible de définir une prise en charge optimale." | Clinical review abstract; no resemblance to EMA posology or safety warning text | IO
- **MORFITT-D10**: MORFITT | schema | — | `specialities: Sequence[ClassLabel]` | 12-class specialty labels; no entity annotations or sentence-pair similarity scores | IO, OO
- **MORFITT-D11**: MORFITT | 29 | 8 (veterinary) | "La cyclosporine est de plus en plus utilisée en dermatologie des petits animaux. Les indications rapportées sont le traitement de la dermatite atopique, du lupus érythémateux cutané…" | Drug named but no INN/ATC annotation; veterinary context irrelevant to regulatory deployment | IC, OO
- **MORFITT-D12**: MORFITT | 8 | 0 (microbiology) | "La région du Nord-Ouest de l'Ontario présente un taux élevé et documenté d'infections de la peau et des tissus mous causées par une souche de Staphylococcus aureus méthycillinorésistante d'origine communautaire (SARM-C)." | Canadian regional epidemiology; non-metropolitan France population | IC, OC
- **MORFITT-D13**: MORFITT | 22 | 11 (psychology) | "le questionnaire final en arabe (YFAS 2.0-A)…a été rempli par 236 étudiants de médecine égyptiens." | Egyptian population study; no metropolitan France relevance | IC, OC
- **MORFITT-D14**: MORFITT | 31 | 11 | "Perceptions, attitudes et pratiques vis-à-vis de la recherche chez des médecins internes en formation en Arabie saoudite." | Saudi Arabia clinical setting; irrelevant to French regulatory context | IC, OC
- **MORFITT-D15**: MORFITT | 20 | 1 | "79 patients au total ont été recrutés à Amman (Jordanie) en 2015." | Jordanian patient cohort; non-French population | IC, OC
- **MORFITT-D16**: MORFITT | 9 | 6, 0, 8 | "L'otite externe est une maladie multifactorielle fréquente chez le chien. La diversité du microbiote cutané chez le chien semble diminuer dans les états pathologiques." | Canine veterinary study; irrelevant to human pharmaceutical regulatory labeling | IO
- **MORFITT-D17**: MORFITT | 10 | 3 (physiology) | "Un enquête a été menée pour décrire les pratiques de régie utilisées par 15 apiculteurs possédant 1824 colonies dans cette région." | Apiculture disease management study; non-human, non-regulatory content | IO
- **CLISTER-D1**: CLISTER | 10 | 5.0 | "Une mastectomie était réalisée avec curage axillaire." / "Une mastectomie avec curage axillaire ont été réalisés." | Near-identical mastectomy description; maximum similarity score | OO
- **CLISTER-D2**: CLISTER | 1 | 0.0 | "Les suites opératoires furent correctes et la patiente est sortie au 16 ème jour post-opératoire." / "Le patient a rapidement été sevré de la méthotriméprazine, qui lui a été retirée." | Unrelated postop discharge vs. drug tapering; minimum similarity | OO
- **CLISTER-D3**: CLISTER | 7 | 4.0 | "La patiente a été opérée et lors de l'exploration on découvrit qu'il s'agissait d'une tumeur de la veine cave inférieure sus-rénale." / "L'examen anatomopathologique de la pièce confirmait qu'il s'agissait d'un léiomyosarcome de la veine cave." | Related surgical/pathology sentences; high but not maximal similarity | IC
- **CLISTER-D4**: CLISTER | 5 | 2.75 | "Le reste de l'examen échographique ne trouvait aucune autre anomalie." / "Le reste de l'examen somatique était sans anomalie." | Partial structural overlap; intermediate score for different exam types | OO
- **CLISTER-D5**: CLISTER | 41 | 2.0 | "Métoprolol 50 mg deux fois par jour;" / "Metformine 500 mg, 1 comprimé deux fois par jour" | Drug + dosage pair; partial similarity due to shared posology format | IC
- **CLISTER-D6**: CLISTER | 98 | 2.0 | "Acide folinique 15 mg une fois par jour" / "Aspirine 80 mg, 1 comprimé une fois par jour" | Two drug posology lines in same format; scored as partly similar | IC
- **CLISTER-D7**: CLISTER | 78 | 4.0 | "2 Maintien : épidurale (bupivicaïne, fentanyl, épimorphine), rémifentanyl et sévoflurane" / "3 Épidurale : bupivicaïne, fentanyl et épimorphine" | Anesthetic drug list pairs; high overlap in drug names | IC
- **CLISTER-D8**: CLISTER | 11 | 4.0 | "La tomodensitométrie abdominale montre des images gazeuses dans la paroi abdominale postérieure, dans l'espace périnéphrétique droit, et dans le rein droit (Figure 1)." | Standard clinical radiology French; confirms register alignment | IF
- **CLISTER-D9**: CLISTER | 90 | 3.0 | "Le taux de PSA était de 218 ng/ml (normale ≤ 4ng/ml)." / "Le dosage de PSA était de 13327 ng/ml (normal : < 4 ng/ml)." | Same test, vastly different numerical results; scored 3.0 | OO
- **CLISTER-D10**: CLISTER | 188 | 4.0 | "L'AHG urinaire est à 10 mmol/l." / "L'AHG urinaire est à 20 mmol/l." | Identical structure, different numerical values; scored 4.0 showing numerical sensitivity | OO
- **CLISTER-D11**: CLISTER | 6 | 0.0 | "La patiente a eu, dans le même temps opératoire, une lithotritie balistique du calcul par voie endoscopique permettant de dénuder le DIU puis de l'extraire par une pince à corps étranger." | Surgical narrative typical of clinical case reports, not regulatory documents | IO
- **CLISTER-D12**: CLISTER | 42 | 1.0 | "Une jeune fille de 17 ans est hospitalisée pour une opération chirurgicale bénigne." / "Une jeune fille de 15 ans s'est fait violer en réunion, après avoir consommé du cannabis." | Clinical case demographics; absent from regulatory labeling contexts | IC
- **CLISTER-D13**: CLISTER | 125 | 4.0 | "Le recul est de 2 ans." / "Le suivie est de 4 ans et demi." | Substantially different follow-up durations scored as highly similar | OO
- **CLISTER-D14**: CLISTER | 149 | 0.5 | "Lithium 300 mg x x x x x x x x x x x x x x x x" / "300 mg IV aux 24 h x x x x x x x x x x x x x x x x" | Tabular drug dosage data; annotation rationale opaque for regulatory equivalence | OO
- **CLISTER-D15**: CLISTER | 116 | 1.0 | "10 à 25 mg une fois par jour" / "Propranolol 40 mg, 1 comprimé deux fois par jour" | Partial dosage without drug name; low regulatory informativeness | IC
- **CLISTER-D16**: CLISTER | 222 | 0.0 | "CMV : cytomegalovirus; DCI : dénomination commune internationale; HTAP : hypertension artérielle pulmonaire; NR : non renseigné; RGO : reflux gastro-oesophagien" | Abbreviation table including INN reference (DCI); incidental, not systematic | IC
- **CLISTER-D17**: CLISTER | 83 | 4.0 | "Le sevrage sera obtenu lors d'une hospitalisation au Centre Antipoison de Marseille, avec baisse progressive des doses quotidiennes." / "Un sevrage sera effectué après 12 jours d'hospitalisation au Centre Antipoison de Marseille." | Clinically similar detox descriptions; dose tapering vs. fixed duration distinction not flagged | OC
- **CLISTER-D18**: CLISTER | 126 | 4.0 | "Un patient de 42 ans, a été hospitalisé pour un UB de la main droite." / "Le patient était resté hospitalisé pour UB de la main." | "UB" (Buruli ulcer) — isolated tropical disease reference, incidental | IC
- **CLISTER-D19**: CLISTER | 8 | 1.0 | "Jour 45 - - - - - - - - - 25 μg 0,4 mg" / "Jour 53 15,13 12,0 1,58 - - - - - - 25 μg 0,4 mg" | Table rows with dash placeholders; structurally unlike regulatory prose | OF
- **CLISTER-D20**: CLISTER | 191 | 2.0 | "5 mg PO Q 4H PRN X" / "10 mg PO Q 4H PRN X X" | Mixed French/English abbreviated medical notation; atypical of standard French regulatory documents | OF
- **MANTRAGSC-D1**: MANTRAGSC/fr_medline | 36 | DISO/CHEM | `"Traitement des méningites purulentes de l'enfant par Cefotaxime."` | Disease + drug entity co-occurrence in French biomedical NER title | IC, OO
- **MANTRAGSC-D2**: MANTRAGSC/fr_medline | 45 | CHEM | `"Effet de la testostérone sur la sécrétion de prolactine."` | Chemical/drug substance annotation in short French biomedical title | IC
- **MANTRAGSC-D3**: MANTRAGSC/fr_medline | 18 | DEVI/CHEM | `"Les pompes à perfusion parentérale: description et étude comparative."` | Device and administration-route vocabulary; pharmaceutical adjacency | IC
- **MANTRAGSC-D4**: MANTRAGSC/fr_medline | 50 | CHEM | `"les substances dites de réveil"` | Substances tagged CHEM, illustrating scope of chemical label | IC, OO
- **MANTRAGSC-D5**: MANTRAGSC/fr_medline | 1 | DISO | `"Luxation antérieure ouverte post-traumatique de la hanche chez l'enfant."` | Orthopedic trauma case report title — clinical prose, not regulatory language | IC, IO
- **MANTRAGSC-D6**: MANTRAGSC/fr_medline | 41 | DISO/GEOG | `"L'épidémie de choléra du Sultanat de Goulfey. (Nord-Cameroun: Mai-Juin 1971."` | 1971 African epidemic case; absent from regulatory genre | IC, IO
- **MANTRAGSC-D7**: MANTRAGSC/fr_medline | 10 | PROC | `"Le problème de la régulation des naissances: aspects médico-légaux et médico-sociaux."` | Medico-legal article; not pharmaceutical compliance text | IO
- **MANTRAGSC-D8**: MANTRAGSC/fr_medline | 36 | CHEM | `"Cefotaxime"` tagged B-CHEM | Drug name tagged at Semantic Group level; no INN/brand/dose distinction | IC, OO
- **MANTRAGSC-D9**: MANTRAGSC/fr_medline | 17 | PROC | `"Traitement antalgique post-opératoire loco-régional par neuro-stimulation électrique transcutanée en chirurgie orthopédique."` | Surgical treatment procedure; no posology or regulatory-template phrasing | IC
- **MANTRAGSC-D10**: MANTRAGSC/fr_medline | 43 | DISO | `"Tétanos localisé (à propos de 19 cas observés à Dakar)"` | Historical African clinical case; non-metropolitan, non-regulatory context | IC
- **MANTRAGSC-D11**: MANTRAGSC/fr_medline | 41 | GEOG | `"L'épidémie de choléra du Sultanat de Goulfey. (Nord-Cameroun: Mai-Juin 1971."` | Confirms historical, non-European content in dataset | IC
- **MANTRAGSC-D12**: MANTRAGSC/fr_medline | 18 | DEVI/PROC | `"pompes à perfusion parentérale"` tagged DEVI; `"parentérale"` tagged PROC | Device/route boundary blurred in ways relevant to regulatory labeling review | OO
- **MANTRAGSC-D13**: MANTRAGSC/fr_medline | 43 | GEOG | `"Tétanos localisé (à propos de 19 cas observés à Dakar)"` | Senegalese clinical context; non-metropolitan French scope | IC
- **MANTRAGSC-D14**: MANTRAGSC/fr_medline | 3 | DISO | `"Paraparésie fébrile chez une Tunisienne: spondylite à cryptocoque avec atteinte médullaire."` | North African patient presentation; non-metropolitan context | IC
- **E3C-D2**: E3C French_clinical | 62 | O | "La patiente était mise sous tri-antibiothérapie probabiliste à base d'amoxicilline-acide clavulanique à 3g/j, de moxifloxacine à 400 mg/j et de métronidazole à 1,5 g/j." | Drug names and dosages present in text but unlabeled; partial vocabulary relevance | IC
- **E3C-D3**: E3C French_clinical | 20 | O/B-CLINENTITY | "une diverticulose du sigmoïde…une occlusion colique en rapport avec un iléus biliaire" | Pathology entities labeled; confirms CLINENTITY scope and clinical annotation norms | OO, IC
- **E3C-D4**: E3C French_clinical | 39 | O/B-CLINENTITY | "une insuffisance rénale modérée, une bicytopénie (anémie et lymphopénie)…une hypertension artérielle…une dyslipidémie traitée par la statine" | Multi-pathology sentence; CLINENTITY labels on diseases, not drugs | OO, IC
- **E3C-D5**: E3C French_clinical | 79 | all O | "Le patient était mis sous anti bacillaires associant Isoniazide 5mg/kg, Rifampicine 10 mg/kg, Ethambutol 25 mg/kg et Pyrazinamide 30 mg/kg" | Drug INN names with per-kg dosages all tagged O; confirms drug/dosage entities absent from label scheme | IO, OO
- **E3C-D6**: E3C French_clinical | 103 | all O | "l'induction de l'anesthésie générale était démarrée par du fentanyl (3µg/kg) et de l'étomidate (0,2mg/kg)" | Drug names with dosages in clinical narrative; unlabeled under CLINENTITY scheme | IC, OO
- **E3C-D7**: E3C French_clinical | 53 | O/B-CLINENTITY | "mis sous antibiothérapie à large spectre (imipenème-vancomycine) et sous catécholamines (noradrénaline) devant l'apparition d'un état de choc septique" | Treatment/drug names unlabeled; only pathology entity labeled; confirms annotation scope restriction | OO, IO
- **E3C-D8**: E3C French_clinical | 20 | O/B-CLINENTITY | "Nous rapportons ici le cas d'une patiente de 89 ans aux antécédents d'une diverticulose du sigmoïde" | Canonical clinical case report framing; no regulatory document genre | IO
- **E3C-D9**: E3C French_clinical | 59 | all O | "Devant la forte suspicion clinique d'AVCi sur le territoire vertébro-basilaire…thrombolyse intraveineuse par ténectéplase 50 mg (10000 UI)" | Clinical narrative with treatment decision; confirms clinical case genre, not regulatory document | IO, IC
- **E3C-D10**: E3C French_clinical | 70 | all O | "Monsieur F M âgé de 70 ans, originaire du Maroc" | Patient origin stated as Morocco; suggests non-metropolitan French clinical context | IC
- **E3C-D11**: E3C French_clinical | 90 | all O | "Il s'agit de la série de CM la plus importante rapportée en Afrique noire." | Reference to Black Africa caseload; indicates sub-Saharan African clinical context | IC
- **E3C-D12**: E3C French_clinical | 59 | all O | "après avis téléphonique auprès d'un médecin neurologue de métropole" | Explicit reference to mainland France as distant authority; positions case outside metropolitan France | IC
- **E3C-D13**: E3C French_clinical | 12 | all O | "Le patient a été mis sous traitement par ciclosporine avec une évolution rapide vers une leucémie aigue myéloblastique." | Clear disease name ("leucémie aigue myéloblastique") tagged O; suggests annotation gaps | OO, OC
- **E3C-D14**: E3C French_clinical | 62 | all O | "La patiente était mise sous tri-antibiothérapie probabiliste à base d'amoxicilline-acide clavulanique à 3g/j" | Full treatment sentence with drug+dosage, no entities labeled; annotation scope confirmed as disease-only | OO
- **E3C-D15**: E3C French_clinical | 1 | O | "bilirubine totale a ` 140 mmol/L" | Backtick artifact replacing accent; minor tokenization quality concern | IF
- **E3C-D16**: E3C French_clinical | 5 | O | `'\', 'n', 'La', 'patiente'` | Escaped newline tokenized as two tokens; encoding artifact in input | IF
- **PXCORPUS-D1**: PxCorpus | 5 | medical_prescription | "primperan 10 milligrammes comprimés 1 comprimé en cas de nausée toutes les 8 heures pendant 14 jours" | Brand drug name with dose, form, PRN indication, frequency, and duration | IC
- **PXCORPUS-D2**: PxCorpus | 47 | medical_prescription | "amoxicilline 1 gramme comprimés dispersibles 1 gramme matin midi et soir pendant 15 jours" | INN with dose, form, multi-timing, duration | IC
- **PXCORPUS-D3**: PxCorpus | 51 | medical_prescription | "ténofovir 245 milligrammes en comprimés à prendre après les repas 1 comprimé le soir pendant 2 semaines puis stop" | Antiretroviral INN with meal-relation administration instruction | IC
- **PXCORPUS-D4**: PxCorpus | 121 | medical_prescription | "cordarone 100 milligrammes 1 comprimé 1 jour sur 2 pendant 1 mois" | Alternating-day dosing schedule | IC
- **PXCORPUS-D5**: PxCorpus | 19 | medical_prescription | "motilium en suspension buvable 1 dose poids de 10 kilogrammes 3 fois par jour si vomissement" | Weight-based pediatric dosing with PRN condition | IC
- **PXCORPUS-D6**: PxCorpus | 100 | medical_prescription | "oramorph 20 milligrammes par millilitres 5 gouttes en cas de douleur ne pas dépasser 6 gouttes par jour" | Concentration-expressed dose with maximum-dose constraint | IC
- **PXCORPUS-D7**: PxCorpus | 93 | medical_prescription | "becotide 250 milligrammes 2 bouffées à 7 heures 2 bouffées à 11 heures 2 bouffées à 15 heures 2 bouffées à 18 heures pendant 6 mois" | Multi-time-point schedule with repeated NER entity tagging | OO
- **PXCORPUS-D8**: PxCorpus | 145 | medical_prescription | "lévothyroxine sodique 50 microgrammes 1 comprimé à prendre le matin à jeun pendant 6 semaines" | INN + salt form + fasting condition tagged | OO
- **PXCORPUS-D9**: PxCorpus | 4 | replace | "attention il s'agit de 20 milligrammes et pas 10 milligrammes" | Explicit dosage correction, relevant to inconsistency detection | IO
- **PXCORPUS-D10**: PxCorpus | 8 | replace | "remplacer 1 comprimé tous les jours par 1 comprimé en cas d'anxiété" | Schedule replacement with PRN substitution | IO
- **PXCORPUS-D11**: PxCorpus | 14 | negate | "attention pas tous les jours seulement si crise" | Negation of schedule with PRN restriction | IO
- **PXCORPUS-D12**: PxCorpus | 75 | medical_prescription | "euh 2 le matin 2 le midi et 2 le soir" | Spoken disfluency with ellipsis — no drug name given | IF
- **PXCORPUS-D13**: PxCorpus | 88 | none | "i'll agree come on say avec successes merde je vais roulé faut lui faire un et mettre la rame en mode français" | Code-switching and expletives from genuine recording transcription | IF
- **PXCORPUS-D14**: PxCorpus | 34 | medical_prescription | "3 mois" | Two-token fragment with no drug name, dose, or form | IO, IC
- **PXCORPUS-D15**: PxCorpus | 3 | none | "/chet" | ASR noise token, not a biomedical term | IF
- **PXCORPUS-D16**: PxCorpus | 66 | none | "/euh mois" | ASR transcription artifact with filler and partial word | IF
- **PXCORPUS-D17**: PxCorpus | 10 | negate | "ne pas tenir compte à midi tous les jours merd/" | Expletive and truncated token in clinical transcription | IF
- **PXCORPUS-D18**: PxCorpus | 12 | replace | "non prendre 150 milligrammes par jour" | One of three replace examples sampled; class severely underrepresented | OO, OC
- **PXCORPUS-D19**: PxCorpus | 210 | medical_prescription | "kardegic 160 milligrammes 1 sachet par jour pendant 1 mois si absence d'ulcère" | Contraindication phrase "si absence d'ulcère" receives no NER tag (O) | OO
- **PXCORPUS-D20**: PxCorpus | 247 | medical_prescription | "nicotine 21 milligrammes sur 24 heures en patch 1 patch en cas de sevrage tabagique changer de patch toutes les 24 heures pendant 3 mois" | Indication ("sevrage tabagique") tagged as risk/condition, not regulatory contraindication category | OO
- **PXCORPUS-D21**: PxCorpus | 169 | medical_prescription | "lamotrigine 25 milligrammes euh p/ combien" | Incomplete prescription with spoken filler and truncated token | IF, IC
- **PXCORPUS-D22**: PxCorpus | 207 | medical_prescription | "teralithe 250 milligrammes / le serveur de dialogue met beaucoup de temps à comprendre votre énoncé veuillez reformuler différemment teralithe 250 milligrammes 2 comprimés matin et soir pendant 1 mois" | System prompt text embedded in prescription transcription | IF
- **PXCORPUS-D23**: PxCorpus | 36 | none | "la remarque à heure fixe n'est pas prise en compte après plusieurs essais" | Participant meta-commentary about the prescription system | OC
- **PXCORPUS-D24**: PxCorpus | 18 | none | "la partie euh posologie est sur 6 ou 8 semaines là il n'est écrit que 8 semaines par contre le qsp 6 semaines a été rajouté en remarque pharmaceutique" | Meta-commentary about a prescription form with internal discrepancy noted | OC
- **DIAMED-D1**: DiaMED | 1 | A00-B99 | "Le test rapide VIH était positif, confirmé par la sérologie VIH avec un taux de CD4 à 27/mm3." | HIV diagnosis confirmed; ARV regimen (Stavudine, Lamuvidine, Efavirenz) reflects African treatment protocols, not French regulatory text | IC
- **DIAMED-D2**: DiaMED | 2 | C00-D49 | "la chromogranine, le N-CAM et la synaptophysine étaient positifs confirmant le diagnostique de tumeur neuroendocrine" | Neuroendocrine tumor confirmed by IHC; demonstrates biomedical vocabulary breadth | IO, IC
- **DIAMED-D3**: DiaMED | 3 | D50-D89 | "La patiente a été opérée après avoir reçu la vaccination anti-pneumococcique et une antibioprophylaxie (association Amoxicilline et acide clavulanique)" | Drug mention in surgical narrative — no regulatory labeling structure or EMA posology template | IO, IC
- **DIAMED-D4**: DiaMED | 4 | E00-E89 | "Une atteinte hypopigmentée triangulaire des cheveux en mi-cuir chevelu frontal ainsi que des tâches de dépigmentation" | Piebaldism case from African clinical setting; clinical case register, not regulatory document | IC
- **DIAMED-D5**: DiaMED | 5 | F01-F99 | "Devant le contexte de dépression, la patiente a été adressée en psychiatrie où ce diagnostic a été confirmé" | One of 2 psychiatric cases; limited class representation | OC
- **DIAMED-D7**: DiaMED | 7 | H00-H59 | "Le test à la pilo diluée à 0.125 est positif...on conclue qu'il s'agit d'une pupille d'adie" | Ophthalmological case; confirms diverse ICD-10 chapter coverage | IO
- **DIAMED-D9**: DiaMED | 9 | I00-I99 | "service de cardiologie du CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" | Explicitly Burkinabé institution; confirms non-metropolitan-France provenance | IC
- **DIAMED-D12**: DiaMED | 12 | L00-L99 | "keywords: ['Toxidermie', 'psychotropes', 'enquête d'imputabilité', 'méthode de Bégaud', 'Niamey']" | Keyword "Niamey" confirms Niger (African) provenance | IC
- **DEFT2021-D1**: DEFT2021 | 3 | ner_tags: [0,0,0,0,0,0,0,0,0,0,0,21,0,21,...] | "Pour les traitements subséquents, on a décidé de devancer la prémédication de diphenhydramine et de méthylprednisolone en la plaçant avant l'administration du premier sac" | Drug premedication names annotated as SUBSTANCE in clinical treatment context | IC
- **DEFT2021-D2**: DEFT2021 | 81 | ner_tags: multi-entity | "Le patient a reçu des cycles de MAP pendant les dix premières semaines (doxorubicine 37,5 mg/m2/dose en association avec le cisplatin à raison de 60 mg/m2/dose pendant deux jours..." | Dense oncology polypharmacy with drug names, dosage, duration co-annotated | IC, OO
- **DEFT2021-D3**: DEFT2021 | 158 | ner_tags: MODE/SUBSTANCE/DOSAGE | "La crème de nystatin a été remplacée par une crème de diproprionate de bétaméthasone à 0,05%, en application topique deux fois par jour pendant dix jours." | Full posology expression annotated: drug name, route, frequency, duration | IC, OO
- **DEFT2021-D4**: DEFT2021 | 80 | ner_tags: TREATMENT/DURATION | "La patiente était mise sous traitement anti-bacillaire à base de rifampicine – isoniazide – pyrazinamide pendant 6 mois." | INN-level drug names with duration annotation in clinical context | IC
- **DEFT2021-D5**: DEFT2021 | 25 | ner_tags: [0,...] | "Une surveillance plus importante de la patiente a été mise en place, d'abord en salle de soins post-interventionnels (SSPI) puis en unité de surveillance continue (USC)... sans qu'il soit nécessaire de mettre en œuvre le protocole NALOXONE." | Clinical abbreviations (SSPI, USC) and drug protocol reference; authentic hospital register | IF
- **DEFT2021-D6**: DEFT2021 | 55 | ner_tags: multi-entity | "Hydrocortisone 300 mg IV immédiatement; Traitement Hydroxyzine 25 mg par voie orale toutes les 6 heures au besoin" | Drug + dosage + route + frequency in a single sequence; relevant to posology inconsistency detection | IC, OO
- **DEFT2021-D7**: DEFT2021 | 4 | ner_tags: [0,9,10,...] | "L'analyse anatomo-pathologique extemporanée a permis de faire le diagnostic de kyste épidermoïde isolé, qui a été confirmé par l'analyse histologique définitive." | Surgical pathology report narrative; not regulatory document format | IO
- **DEFT2021-D8**: DEFT2021 | 37 | ner_tags: [0,23,...] | "Une cystoprostatectomie était réalisée... ainsi une entérocystoplastie était pratiquée." | Operative report syntax; structurally unlike SmPC or PIL regulatory text | IO
- **DEFT2021-D9**: DEFT2021 | 18 | ner_tags: [0,13,14,...,23,24,...] | "Par voie sous costale, il a été réalisé une néphrectomie élargie gauche, une surrénalectomie de principe associée à une splénectomie" | Tag 23 (TREATMENT) applied to surgical procedures — scheme does not distinguish surgical from pharmacological treatment | OO
- **DEFT2021-D10**: DEFT2021 | 3 | ner_tags: [0,...,21,...,21,...] | "diphenhydramine et de méthylprednisolone" | Both INN drug names receive SUBSTANCE-B tag (21); no INN-specific or ATC-code annotation level | OO, IC
- **DEFT2021-D11**: DEFT2021 | metadata | cls config | (MeSH label space from YAML Q27): "immunitaire, infections, tumeur..." | MLC labels are clinical disease taxonomy (MeSH Chapter C), not regulatory compliance categories | OO
- **DEFT2021-D12**: DEFT2021 | 166 | ner_tags: [0,...] | "Un homme de 40 ans a consulté pour une douleur pubienne irradiant au pénis, survenue au retour d'un voyage à Madagascar." | Travel medicine context (Madagascar); disease prevalence not representative of metropolitan France | IC, OC
- **DEFT2021-D13**: DEFT2021 | 108 | ner_tags: [0,...] | "Elle a séjourné plusieurs années en Afrique et fumait à cette époque deux paquets de cigarettes par jour." | African residency history; possible tropical disease context; geographic scope unclear | IC
- **DEFT2021-D14**: DEFT2021 | 65 | ner_tags: [0,...,5,6,...,21,...,5,6,...] | "l'infirmière anesthésiste se rend compte qu'elle a utilisé une ampoule de morphine de 10mg au lieu de 1 mg" | Medication error case; DOSAGE annotation does not distinguish stated vs. prescribed vs. safety-threshold dose | OC
- **DEFT2021-D15**: DEFT2021 | 26 | ner_tags: [0] | "." | Single period token — segmentation artifact with no clinical content | IF
- **DEFT2021-D16**: DEFT2021 | 23 | ner_tags: [0,0,0] | "Mr ." | Patient name initial fragment; no clinical or pharmaceutical content | IF
- **CAS-D1**: CAS | 1 | pos | "l' examen clinique montre un état général conservé ." | Standard French clinical examination sentence; confirms clinical prose register alignment | IC, IF
- **CAS-D2**: CAS | 65 | pos | "l' examen clinique à l' admission était sans particularité , hormis une douleur provoquée à la palpation de la fosse iliaque gauche" | Formal clinical admission examination; confirms register consistency with deployment | IC, IF
- **CAS-D3**: CAS | 63 | pos | "remplacer les lavements de pentasa ® par du proctocort ® ( hydrocortisone acétate 90 mg : 1 lavement tous les soirs )" | Drug brand names with dosage and route in clinical narrative context | IC
- **CAS-D4**: CAS | 33 | pos | "cyclophosphamide , vincristine et prednisone … méthotrexate , cyclophosphamide , vincristine , doxorubicine , prednisone et rituximab" | Multi-drug chemotherapy regimen with named substances | IC
- **CAS-D5**: CAS | 22 | pos | "administration d' une ampoule de digoxine en intraveineuse" | Drug name (digoxin) with route of administration | IC
- **CAS-D6**: CAS | 49 | pos | "en postopératoire la malade a été traitée à la norfloxacine ." | Antibiotic treatment mention in clinical case | IC
- **CAS-D7**: CAS | 29 | pos | "887 , 5 mg ( 12 , 5 mg / kg / h ) administrée sur quatre heures , puis de 443 , 8 mg ( 6 , 25 mg / kg / h ) sur les 67 heures restantes" | Detailed weight-adjusted dosing expression with temporal structure | IC
- **CAS-D8**: CAS | 9 | pos | "anémie à 5 , 7 g / 100ml d' hb , une hyponatrémie à 128 meq / l … créatinine sanguine à 461 micromole / l" | Multiple laboratory values with units, relevant to threshold extraction | IC
- **CAS-D9**: CAS | 54 | pos | "la valeur limite d' exposition autorisée était de 450 ppm soit 2 500 mg / m 3" | Exposure threshold phrasing with quantitative values | IC, OO
- **CAS-D10**: CAS | 14 | pos | "les ovaires ne montraient pas d' anomalie ." | Negated clinical finding; directly relevant to negation classification label | IO, OO
- **CAS-D11**: CAS | 20 | pos | "l' issue n' était pas très claire ." | Speculative hedging in clinical narrative; relevant to speculation label | IO, OO
- **CAS-D12**: CAS | 15 | pos | "Il s' agit d' une patiente âgée de 54 ans ayant des facteurs de risque de transmissions virales hépatiques…" | Clinical case introduction format; structurally unlike SmPC/PIL regulatory text | IC, IO
- **CAS-D13**: CAS | 47 | pos | "vous êtes appelés au secours d' une infirmière de nuit pour confusion chez un patient bronchopathe chronique" | Case-based scenario language; not regulatory document genre | IC
- **CAS-D14**: CAS | 34 | pos | "le betnésol ® lavement était progressivement arrêté ." | Brand name drug mention in narrative; no INN, ATC code, or structured posology | IC
- **CAS-D15**: CAS | 80 | pos | "cholstat ® 0.1 ." | Brand name with numeric; no INN or ATC classification structure | IC
- **CAS-D16**: CAS | 103 | pos | "ast ( 6-35 u / l ) 789 763 710 637 503 385 98. alt ( -45 u / l ) 2001 1905 1853 1953 1583 954 103." | Complex tabular lab data; automatic POS tagging is error-prone here | OC, OF
- **CAS-D17**: CAS | 97 | pos | "- plaquette : 250 000. - crp : 140 mg / l ." | Abbreviated list format; challenging for automatic taggers, silver-label quality concern | OC
- **CAS-D18**: CAS | 68 | pos | "une sérologie leptospirose devient positive … trois semaines après le début des symptômes ." | Leptospirosis serology; pathology with elevated prevalence in tropical/overseas contexts | IC
- **CAS-D19**: CAS | 44 | pos | "le fils de la patiente … présente les premiers symptômes le 4 août 2014 , soit dix jours après l' exposition à l' eau de la rivière" | Waterborne exposure narrative possibly consistent with tropical context | IC
- **CAS-D20**: CAS | 88 | pos | "' docteur , je suis complètement crevée depuis 5 jours , j' ai des courbatures partout ." | Informal colloquial patient speech; register mismatch with regulatory documents | IC, IF
- **CAS-D21**: CAS | 13 | pos | "depuis hier soir , je suis essouflé , j' ai des frissons , j' ai mal à la poitrine" | First-person informal symptom report; not representative of regulatory text | IC, IF
- **ESSAI-D1**: ESSAI | 1 | pos | "avec la combinaison gemcitabine + abraxane , chez des patients avec un cancer du pancréas" | INN + brand name drug combination in trial context | IC
- **ESSAI-D2**: ESSAI | 36 | pos | "la chimiothérapie classique du mésothéliome pleural avec l' association pemetrexed et cisplatine ou carboplatine , jusqu' à 6 cycles" | Drug INNs with dosing cycle count | IC
- **ESSAI-D3**: ESSAI | 9 | pos | "L' acétate d' abiratérone ou l' enzalutamide sont des traitements assez récents et ainsi appelés « hormonothérapies de nouvelle génération »" | Named drugs with therapeutic class label | IC
- **ESSAI-D4**: ESSAI | 66 | pos | "Le lanréotide est un traitement hormonal dont l' effet est médié par une action antiproliférative" | INN with pharmacological mechanism description | IC
- **ESSAI-D5**: ESSAI | 6 | pos | "administré toutes les deux semaines sous forme de perfusion d' une heure" | Dosing frequency + route + duration posology expression | IC
- **ESSAI-D6**: ESSAI | 48 | pos | "administré en intraveineuse toutes les 2 semaines sur une durée de 30 mn" | IV route + frequency + duration triplet | IC
- **ESSAI-D7**: ESSAI | 47 | pos | "L' ENTO ou le placébo est donné par voie orale 2 fois par jour , pour une durée de 48 semaines" | Oral dosing with complete posology schedule | IC
- **ESSAI-D8**: ESSAI | 31 | pos | "une large proportion des patients n' est pas apte à recevoir une chimiothérapie à base de cisplatine" | Negated patient eligibility / contraindication signal | OO
- **ESSAI-D9**: ESSAI | 40 | pos | "ne présentant pas de contre-indication aux traitements de l' étude" | Explicit negated contraindication phrase | OO
- **ESSAI-D10**: ESSAI | 29 | pos | "De nouveaux médicaments capables d' inhiber ces anomalies pourraient être actifs dans ce cas" | Speculative modal (pourraient) for treatment efficacy claim | OO
- **ESSAI-D11**: ESSAI | 25 | pos | "Vous serez vu en consultation avant de débuter le traitement puis après 8 jours , après 15 jours de traitement , puis toutes les 2 semaines" | Patient-addressed monitoring schedule; PIL-adjacent register | IF
- **ESSAI-D12**: ESSAI | 26 | pos | "Vous serez vus en consultation régulièrement pour évaluer la tolérance et l' efficacité du traitement à l' essai" | Patient-facing efficacy/tolerance framing; PIL-adjacent | IF
- **ESSAI-D13**: ESSAI | 71 | pos | "Ce traitement bénéficie d' une autorisation de mise sur le marché pour les tumeurs de même nature" | AMM (marketing authorization) terminology — closest regulatory signal in sample | IC
- **ESSAI-D14**: ESSAI | 3 | pos | "Un tirage au sort deux tiers / un tiers répartira les patientes dans les deux bras de l' étude" | Trial randomization language specific to protocol genre | IO
- **ESSAI-D15**: ESSAI | 19 | pos | "Un tirage au sort répartira de manière équilibrée les patientes dans les deux bras de l' étude" | Further confirms trial protocol (not regulatory submission) genre | IO
- **ESSAI-D16**: ESSAI | 37 | pos | "un anticorps anti-CTLA-4 ( ipilimumab ) et un anticorps anti-PD-1 ( nivolumab )" | Drug INNs present but no INN-specific NER label schema available | OO
- **ESSAI-D17**: ESSAI | 64 | pos | "Le LY3200882 est un médicament qui inhibe spécifiquement le TGF-beta" | Experimental compound code; no regulatory entity label schema | OO
- **ESSAI-D18**: ESSAI | 5 | pos | "le cancer du sein triple négatif , le cancer de l' ovaire et le cancer bronchique à petites cellules" | Oncology-only disease vocabulary | IO
- **ESSAI-D19**: ESSAI | 21 | pos | "Il s' adresse aux patients atteints de cancer de la prostate , de cancer du sein , de cancer du poumon" | Further confirms oncology concentration | IO
- **ESSAI-D20**: ESSAI | 65 | pos | "Cancer indifférencié ou anaplasique de la thyroïde" | Oncology-exclusive disease naming | IO
- **ESSAI-D21**: ESSAI | 2 | pos | "Le MEDI9197 est injecté en intra-tumoral tous les 28j" | Abbreviated dosing interval ("28j") — potential TreeTagger silver-standard tagging error risk | OC


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
  "region": "French Pharmaceutical Regulatory Affairs — Document Compliance NLP",
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
