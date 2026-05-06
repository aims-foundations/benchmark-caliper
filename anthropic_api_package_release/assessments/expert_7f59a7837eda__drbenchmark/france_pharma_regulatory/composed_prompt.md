I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Domain** is valid for use in **EU Pharmaceutical Regulatory NLP — French**.

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
- **Domain**: French biomedical NLU evaluation
- **Languages**: fr
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis

### 1. Input Ontology
DrBenchmark organizes its 20 tasks into five NLP task categories: POS tagging, NER,
MCQA, multi-class classification (MCC), multi-label classification (MLC), and STS [Q81].
The task inventory spans a clinically and scientifically oriented construct of "French
biomedical language understanding" [Q83], including classical tasks (POS, NER) and more
challenging ones (MCQA, multi-label classification) [Q20]. Sub-tasks within datasets
further differentiate the taxonomy: DEFT-2020 provides a sentence similarity task (0–5
scale) and a most-similar-sentence selection task [Q21, Q22, Q23]; FrenchMedMCQA covers
identifying correct answers among five options and counting the number of correct answers
[Q39]; PxCorpus contributes intent classification and NER over spoken drug prescription
transcripts [Q44].

However, the task taxonomy is calibrated for clinical and research NLP conventions
rather than pharmaceutical regulatory workflow categories. Regulatory document genres
such as SmPCs, EU Risk Management Plans, patient information leaflets, and CTD modules
do not appear as explicit task categories. The benchmark does not address regulatory
equivalence scoring as a distinct output task type. Existing NLP benchmarks for English
(BLURB: 13 tasks; BLUE: 10 tasks) and Chinese (CBLUE: 8 tasks) are noted as antecedents
[Q12, Q13, Q14, Q15], and the paper acknowledges that no large French biomedical
benchmark existed prior to DrBenchmark [Q16]. General benchmarks are noted as potentially
inadequate for specialized domains [Q10], and biomedical benchmarks are described as
scarce and English/Chinese-centric [Q9, Q11].

### 2. Input Content
Data origins are diverse: scientific literature, clinical trials, clinical cases, speech
transcriptions, and additional genres [Q19]. Key corpora include DEFT-2021 (275 clinical
cases) [Q24], E3C (multilingual clinical cases, French subset retained) [Q29], QUAERO
(drug leaflets and biomedical titles from EMEA and MEDLINE, 103,056 words total) [Q33,
Q34], MorFITT (3,624 biomedical abstracts from PMC Open Access) [Q38], Mantra-GSC
(biomedical abstracts/titles, drug labels, and patents from three source types) [Q40],
ESSAI (7,247 clinical trial protocols) [Q43], and DiaMed (739 clinical cases from The
Pan African Medical Journal) [Q45].

For the regulatory deployment context, QUAERO is the most directly relevant source
because it explicitly includes EMEA drug leaflet text [Q34] — one of the document types
in the target deployment. Mantra-GSC's EMEA and Patents subsets [Q40] provide a second
partial overlap with the regulatory genre. However, these sources represent a minority
of the benchmark's data. The majority of content originates from clinical case reports
and research abstracts, which differ substantially from formal EU regulatory submissions
in register, terminology, entity density, and formulaic phrasing. Dataset licensing is
preserved from original sources without redistribution [Q96], requiring independent
acquisition. Training data volume was also varied systematically (25%, 50%, 75%, 100%)
[Q68], and vocabulary differences across models reflect different underlying training
corpora [Q76].

### 3. Input Form
DrBenchmark operates exclusively on French text. Multilingual datasets are filtered to
retain only their French subsets [Q31]. The benchmark is delivered through a HuggingFace
Datasets-based toolkit with normalized loaders and predefined splits [Q48]. For datasets
lacking predefined splits, a 70/10/20 random partition is applied [Q32, Q42, Q40].
Tokenization is a studied variable: average sub-token counts per word are analyzed across
models [Q89, Q90], revealing that DrBERT-CP (highest average segmentation, 1.90) still
outperforms FlauBERT (lowest segmentation, 1.43) on 16 of 20 tasks [Q78], suggesting
tokenization effects are less impactful than previously assumed [Q79, Q80]. Long EMEA
documents were sentence-split to accommodate model input length constraints [Q37].
PxCorpus introduces transcribed speech as a text-format input, covering 4 hours of
spoken drug prescription dialogues [Q44] — the only deviation from written text form.

No script mismatch issues exist. Both deployment and benchmark operate on French text
in Latin script with standard diacritics. The sentence-splitting applied to EMEA
documents [Q37] is directly relevant to the long-form regulatory documents typical of
the deployment environment (SmPCs, CTD modules), though this preprocessing step
introduces a potential structural mismatch for tasks requiring document-level context.

### 4. Output Ontology
The benchmark's output taxonomy spans six task-type categories — POS, NER, MCQA, MCC,
MLC, STS — with results aggregated by category [Q81]. NER entity schemas are corpus-
specific and clinically calibrated: QUAERO uses 10 UMLS Semantic Groups (GEOG, PHEN,
DISO, ANAT, OBJC, PHYS, PROC, DEVI, CHEM, LIVB) [Q35, Q103]; E3C covers CLINENTITY,
EVENT, ACTOR, BODYPART, TIMEX3, RML [Q30, Q104]; Mantra-GSC uses 11 classes for
Medline and 10 for EMEA/Patents [Q106]; PxCorpus NER covers 38 classes including DRUG,
DOSE, and MODE [Q44, Q108]. Multi-label classification targets 23 MeSH Chapter C axes
for DEFT-2021 [Q27, Q107], 12 medical specialties for MorFITT [Q105], and 22 ICD-10
chapters for DiaMed [Q45]. STS uses a continuous 0–5 similarity scale [Q41], evaluated
via Spearman correlation and EDRM [Q54].

For the regulatory deployment context, the STS scoring function reflects general
semantic proximity rather than regulatory equivalence. Small lexical differences in
dose thresholds or contraindicated-population qualifiers — legally critical under
EMA/ANSM standards — are not distinguished from near-synonymy in this scoring schema.
The NER entity schemas are calibrated for clinical entities (pathologies, symptoms,
procedures, anatomical structures) rather than regulatory entity types (INNs, ATC codes,
excipient names, EMA-templated posology expressions, contraindication qualifiers).
SUBSTANCE, DOSAGE, MODE, and TREATMENT appear in PxCorpus [Q108], and CHEM appears
across multiple corpora [Q103, Q106], but these do not map cleanly onto the regulatory
entity set. The leading model (DrBERT-FS) does not excel on MLC or STS tasks [Q82],
which is directly relevant to the deployment's reliance on STS for compliance flagging.

### 5. Output Content
Annotation documentation is limited to three datasets. DEFT-2021 was manually annotated
for multi-label classification and NER [Q25]. CLISTER's 1,000 sentence pairs were
manually annotated by multiple annotators who assigned 0–5 similarity scores, averaged
to produce floating-point reference values [Q41]. DiaMed was manually annotated by
several annotators including one medical expert, using ICD-10 chapters, with inter-
annotator agreement computed via Cohen's Kappa and Gwet's AC1 across two sessions of
15 clinical cases each [Q45, Q46]. CAS's POS annotations were produced automatically
via Tagex 3 and evaluated against manual annotations at 98% precision [Q42].

NOT DOCUMENTED for the majority of corpora: annotator demographics, professional
backgrounds (clinical, research, NLP specialist), or annotation guidelines are not
provided. The paper does not indicate whether any annotation guidelines reference
EMA/ANSM regulatory standards. The one confirmed medical expert (DiaMed) [Q45]
contributed to ICD-10 classification, not to the NER or STS tasks most relevant to
the deployment. The heterogeneity of the 101 source datasets — and the absence of
annotator profile documentation across most — means it is impossible to assess whether
annotation norms reflect regulatory affairs expertise. Systematic disagreement between
benchmark ground-truth labels and regulatory-standard judgments on borderline cases
(e.g., dose threshold qualifiers, contraindication scope) cannot be excluded.

### 6. Output Form
Outputs span text-classification labels, IOB2 sequence labels, multiple-choice
selections, and continuous similarity scores. SeqEval with IOB2 format is used for
POS and NER tasks, with models predicting only the first token label per word to
ensure tokenizer-agnostic evaluation [Q52, Q53]. STS evaluation uses Spearman
correlation and the EDRM metric from DEFT-2020 [Q54]. Classification results are
compared against a majority-class baseline [Q56]. Results are averaged over four
runs with statistical significance via Student's t-test [Q51]. Hyperparameters are
fully documented [Q99], and best models are saved based on validation metrics to
mitigate overfitting [Q100].

Both the deployment and the benchmark consume label and score outputs in compatible
modalities — no output representation mismatch exists. The EDRM metric is specific
to the DEFT-2020 task design [Q54] and has no documented calibration for detecting
legally significant micro-differences in regulatory text equivalence. The benchmark
required approximately 2,500 GPU hours (647,500 Wh / 36.9 kgCO2eq) [Q93, Q94],
raising reproducibility concerns for resource-constrained users [Q92], though the
HuggingFace toolkit and documented hyperparameters [Q49] mitigate this somewhat.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "It encompasses 20 diversified tasks, including named-entity recognition, part-of-speech tagging, question-answering, semantic textual similarity, and classification." |
| Q2 | 1 | output_form | "We evaluate 8 state-of-the-art pre-trained masked language models (MLMs) on general and biomedical-specific data, as well as English specific MLMs to assess their cross-lingual capabilities." |
| Q3 | 1 | output_form | "Our experiments reveal that no single model excels across all tasks, while generalist models are sometimes still competitive." |
| Q4 | 1 | input_ontology | "These tasks encompass part-of-speech (POS) tagging, named-entity recognition (NER), classification, question-answering (QA), and semantic textual similarity (STS)." |
| Q5 | 1 | input_content | "Although the French language is generally considered as well-endowed, it is notably lacking in evaluation resources within the biomedical field." |
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
| Q22 | 3 | input_ontology | "The first task aims at identifying the degree of similarity within pairs of sentences, from 0 (the less similar) to 5 (the most similar)." |
| Q23 | 3 | input_ontology | "The second task consists in identifying, for a given sentence, the most similar sentence among three sentences provided." |
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
| Q36 | 3 | input_content | "In total, 26,409 entity annotations were mapped to 5,797 unique UMLS concepts." |
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
| Q55 | 6 | output_ontology | "In Section 5.1, we compare the results obtained by each model within DrBenchmark, which permits to position a wide range of state-of-the-art models in the biomedical field across various NLP tasks." |
| Q56 | 6 | output_form | "The results of the 8 models are reported in Table 6 and compared to a baseline obtained by considering the majority class for all predictions." |
| Q57 | 6 | output_form | "Overall, although we might anticipate certain models to excel in all tasks, we discovered that no single model outperforms the rest in all application scenarios." |
| Q58 | 6 | output_form | "Interestingly, most of the models examined manage to secure the top position in at least one of the French biomedical downstream tasks studied." |
| Q59 | 6 | output_form | "The only exception pertains to the cross-lingual generalist model (XLM-RoBERTa), which manages to reach the second-best position on several tasks." |
| Q60 | 6 | output_content | "French biomedical language models (DrBERT-FS, DrBERT-CP, CamemBERT-bio), presumed to be the most aligned with the nature of the data of the benchmark, exhibit indeed superior performance across many tasks." |
| Q61 | 6 | output_form | "More precisely, DrBERT-FS achieves the highest performance in 8 tasks, DrBERT-CP in 5 tasks, and CamemBERT-bio in 2 tasks." |
| Q62 | 6 | output_form | "This indicates that domain and language-specialized models achieve the best performance in up to 75% of the DrBenchmark downstream tasks." |
| Q63 | 6 | output_form | "Generalist models (CamemBERT, CamemBERTa, FlauBERT and XLM-RoBERTa) are more suitable for tasks that require extensive linguistic knowledge but may not perform as well as specialized models nor even reach their level of performance." |
| Q64 | 6 | output_form | "We observe that all generalist models obtain better performance only on 4 out of the 20 tasks, but still remain competitive on most tasks." |
| Q65 | 6 | input_content | "Furthermore, our experiments with DrBERT-FS indicate that biomedical models may require less pre-training data compared to generalist ones." |
| Q66 | 6 | input_content | "However, it is important to note that this observation requires further confirmation." |
| Q67 | 6 | output_form | "In some tasks, biomedical models that undergo continual pre-training from a generalist model, such as CamemBERT-bio, can prove to be the most effective, underscoring the value of pre-training on generalist data." |
| Q68 | 7 | input_content | "For this purpose, we conducted experiments by varying the amount of training data during the fine-tuning process by randomly choosing four percentages of the training data: 25%, 50%, 75% and 100%." |
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
| Q81 | 8 | output_ontology | "Table 8 summarizes the results obtained on average by the considered MLMs when aggregating the tasks into one of the five designated categories: POS, NER, MCQA, MCC (Multi-class classification), MLC (Multi-label classification), or STS tasks." |
| Q82 | 8 | output_form | "Upon analyzing the average performance by task category, it becomes evident that the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS." |
| Q83 | 9 | input_ontology | "In this paper, we introduced DrBenchmark, the first large language understanding benchmark tailored for the French biomedical domain." |
| Q84 | 9 | input_ontology | "We conducted a qualitative evaluation of 8 state-of-the-art masked language models (MLMs) on this comprehensive benchmark, encompassing 20 diverse downstream tasks." |
| Q85 | 9 | output_form | "Our findings illuminate the limitations of generalist models in tackling complex biomedical tasks, emphasizing the importance of employing domain-specific models to achieve peak performance." |
| Q86 | 9 | output_form | "We have observed that several biomedical tasks in DrBenchmark exhibit relatively poor performance, even when utilizing specialized biomedical models." |
| Q87 | 9 | output_ontology | "We postulate that the models examined in this study, here state-of-the-art MLMs, may not be the most effective choices for specific tasks such as question-answering or multi-label classification." |
| Q88 | 9 | input_form | "The quantitative study we conducted on the PLMs requires further in-depth analysis to comprehend the impact of different parameters." |
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
name: EU Pharmaceutical Regulatory NLP — French
abbreviation: EU-pharma-regulatory-fr
deployment_context:
  system_description: A document management system that applies French biomedical
    NLP models (semantic textual similarity and fine-grained named-entity recognition)
    to verify that drug labeling documents meet EU regulatory submission standards.
    The system flags inconsistencies in safety warnings and extracts regulatory entities
    to determine whether documentation requires manual revision before official submission.
  primary_function: 'Regulatory compliance verification: NER-based entity extraction
    and STS-based equivalence scoring over EU pharmaceutical submission documents.'
  workflow_role: The NLP engine serves as a foundational extraction layer; regulatory-specific
    templates are applied as a supplementary layer for highly specialized formats
    such as CTD modules. Borderline or high-stakes inconsistencies flag documents
    for human review; automatic rejection is not used.
  jurisdictions:
  - EMA (European Medicines Agency)
  - ANSM (Agence nationale de sécurité du médicament et des produits de santé)
  - EU regulatory zone
target_population:
  description: Regulatory affairs specialists, pharmacologists, and legal experts
    employed at pharmaceutical companies and government health agencies operating
    under EMA/ANSM jurisdiction. This is a highly specialized professional cohort
    distinct from clinical practitioners, biomedical researchers, and NLP annotator
    pools.
  roles:
  - Regulatory affairs specialists
  - Pharmacologists (regulatory function)
  - Legal experts in pharmaceutical IP and compliance
  organizational_settings:
  - Pharmaceutical manufacturers (innovator and generic)
  - Contract research organizations (CROs) with regulatory divisions
  - Government health agencies (ANSM and national competent authorities of EU member
    states)
  - EMA centralized procedure applicants
  geography:
    primary: France
    extended: EU regulatory zone — any EU member state whose regulatory submissions
      fall under EMA centralized or mutual-recognition procedures
    sub_national_variation: No meaningful sub-national variation within France or
      the EU regulatory zone; the professional community operates under uniform EMA/ANSM
      procedural standards.
  population_size_estimate: '[NOT FOUND — searched EMA career pages, EuroPharmaJobs,
    industry recruitment sources, and general EU labor market data; no authoritative
    published count of regulatory affairs professionals active specifically in France
    or the EU pharmaceutical sector was identified. The EMA Secretariat itself employs
    approximately 600 staff (Wikipedia, EMA careers page [WEB-1]),
    but industry-side regulatory professional headcount for France is not publicly
    aggregated. Requires stakeholder or professional association (e.g., GREPRA, TOPRA)
    query for a precise figure.]'
languages:
  primary: French (formal regulatory register)
  register_notes: 'The deployment language is French in a highly constrained, legally
    standardized register: EMA SmPC templates, ANSM circulars, EU Risk Management
    Plan prose, CTD module narrative sections, and patient information leaflet boilerplate.
    This register differs substantially from clinical French (hospital records, case
    reports) and research French (journal abstracts, clinical trial protocols) in
    vocabulary standardization, sentence structure, formulaic phrasing density, and
    abbreviation conventions.'
  other_languages_in_scope:
  - English — EMA centralized procedure documents are often drafted in English and
    translated; the system may encounter parallel-language contexts, but the benchmark
    scope is French only.
  - Latin abbreviations — INN nomenclature and pharmacological Latin are embedded
    in French regulatory prose.
  note: No script mismatch, no RTL concerns, no dialect variation. The primary validity
    risk is register mismatch (regulatory French vs. clinical/research French), not
    language coverage.
writing_systems:
  scripts:
  - Latin alphabet with standard French diacritics (é, è, ê, ë, à, â, î, ï, ô, ù,
    û, ü, ç, œ, æ)
  note: No script-level NLP challenges. Both deployment and benchmark operate on French
    Latin-script text. Regulatory documents use formulaic typographic conventions
    (section numbering, tabular posology, bulleted contraindications) that may create
    tokenization or sentence-boundary edge cases when sentence-splitting long SmPC
    documents.
document_genres:
  primary_deployment_genres:
  - genre: Summary of Product Characteristics (SmPC)
    description: Legally binding, EMA-templated document defining indications, dosage,
      contraindications, and safety warnings for authorized medicinal products. Highly
      formulaic, section-structured.
    regulatory_status: 'Core submission document under EU Directive 2001/83/EC. The
      SmPC is included in Module 1 of the CTD (eCTD format) and supports alignment
      with Modules 2 and 5. Source: EUPATI Open Classroom — [WEB-2]'
    benchmark_coverage: 'QUAERO EMEA subset contains package leaflet (PIL) text, NOT
      SmPC text. The EMEA sub-corpus consists of 3 training + 3 dev + 4 test documents
      (segmented into sub-documents) sourced from EMEA drug leaflets, annotated with
      10 UMLS Semantic Group categories with no SmPC-specific section structure. Source:
      DrBenchmark/QUAERO HuggingFace — [WEB-3];
      QUAERO official corpus page — [WEB-4]. SmPC register
      is NOT documented as covered anywhere in DrBenchmark.'
  - genre: Patient Information Leaflet (PIL / Package Leaflet)
    description: Consumer-facing regulatory document accompanying medicinal products,
      required under EMA guidelines. Simplified register relative to SmPC but still
      legally constrained.
    regulatory_status: Mandatory under EU Directive 2001/83/EC
    benchmark_coverage: 'QUAERO EMEA sub-corpus (DrBenchmark) explicitly contains
      drug leaflet text from EMEA documents — partial coverage confirmed. The EMEA
      documents are segmented patient-facing leaflets, not SmPC prose. Source: QUAERO
      HuggingFace dataset card — [WEB-3].
      Annotation schema uses 10 UMLS Semantic Groups (CHEM, DISO, PROC, ANAT, etc.),
      not regulatory-specific PIL categories.'
  - genre: Common Technical Document (CTD) modules
    description: Structured dossier format for EMA/ICH regulatory submissions, particularly
      Module 1 (administrative), Module 2 (summaries), and Module 5 (clinical study
      reports). Narrative modules combine scientific and legal prose.
    regulatory_status: 'ICH M4 guideline; mandatory for EMA centralized procedure.
      QRD templates align with ICH CTD Module 1 requirements. Source: pharmaregulatory.in
      QRD guide — [WEB-5]'
    benchmark_coverage: 'Not documented as a DrBenchmark data source. No French NLP
      benchmark with confirmed CTD module text was found in searches. [NEEDS VERIFICATION
      — deferred: below search budget; no contradictory evidence found]'
  - genre: EU Risk Management Plan (EU-RMP)
    description: Document specifying pharmacovigilance activities and risk minimization
      measures. Highly structured with safety specification sections.
    regulatory_status: Required under EMA GVP Module V
    benchmark_coverage: 'Not documented as a DrBenchmark data source. [NEEDS VERIFICATION
      — deferred: below search budget; no contradictory evidence found]'
  - genre: Patent claims (pharmaceutical/IP)
    description: 'Legal documents defining intellectual property scope of drug compounds,
      formulations, or methods. Syntactically distinct from biomedical prose: single-sentence
      claims with nested qualifying clauses.'
    regulatory_status: Not EMA/ANSM documents per se; relevant to the deployment's
      IP workflow component
    benchmark_coverage: 'Mantra-GSC Patents subset provides French patent NER [Q40,
      Q106]; low-resource, limited schema, poor model performance on CamemBERT-based
      models [Q73]. The EMEA and Patents subsets share the same 10-class annotation
      schema (ANAT, PROC, CHEM, PHYS, DEVI, LIVB, OBJC, DISO, PHEN, O) [Q106] — no
      drug-specific regulatory entity classes (INN, ATC, excipient) are documented
      as distinct categories in this schema. Source: DrBenchmark paper (ArXiv 2402.13432)
      — [WEB-6]'
  genre_mismatch_risk: 'HIGH — the majority of DrBenchmark content derives from clinical
    cases, research abstracts, and clinical trial protocols, which differ from EU
    regulatory document genres in register, entity density, formulaic phrasing, and
    legal constraint level. The QUAERO EMEA subset contains PIL-register text (not
    SmPC), covering only approximately 10 segmented documents in the train/dev/test
    splits. Source: QUAERO corpus documentation — [WEB-4]'
regulatory_framework:
  primary_authorities:
  - EMA (European Medicines Agency)
  - ANSM (Agence nationale de sécurité du médicament et des produits de santé)
  key_guidelines_and_directives:
  - 'EU Directive 2001/83/EC on medicinal products for human use — legal foundation
    for SmPC and PIL requirements. Source: EMA product information requirements page
    — [WEB-7]'
  - 'EMA SmPC/PIL QRD template, current operational version v10.4 (February 2024),
    revised to address post-Brexit Windsor Framework compliance (removal of ''United
    Kingdom (Northern Ireland)'' from local representatives list). Draft v11 under
    public consultation April–August 2025, focused on package leaflet content/structure
    improvements. Source: EMA QRD templates page — [WEB-7];
    draft v11 PDF — [WEB-8]'
  - 'EMA GVP Module V (Risk Management Systems) — requires EU-RMP for authorized medicinal
    products; the SmPC is explicitly identified as the ''fundamental routine risk
    minimisation measure (RMM) tool.'' Source: EMA GVP Module XVI guidance PDF — [WEB-9]'
  - 'ICH M4 CTD guideline — mandates the Common Technical Document format (5 modules);
    SmPC is placed in Module 1.3 (eCTD format). Source: EUPATI Open Classroom — [WEB-2]'
  - '[NEEDS VERIFICATION — deferred: ANSM-specific circulars or national implementing
    regulations relevant to labeling; likely unsearchable at the level of specific
    circulars without access to ANSM internal documentation portal]'
  equivalence_standard: 'Regulatory equivalence, not general semantic proximity: small
    lexical differences in dose thresholds, contraindicated-population qualifiers,
    or temporal safety modifiers constitute legally critical mismatches under EMA/ANSM
    standards. The deployment treats these as non-equivalent even when general semantic
    similarity scores are high.'
  submission_procedure_types:
  - EMA centralized procedure
  - Mutual recognition procedure (MRP)
  - Decentralized procedure (DCP)
  - ANSM national procedure
  net_new_iris_platform: 'Since January 2025, the EMA IRIS platform is mandatory for
    Article 61(3) notifications — the procedure for updating SmPC and PIL labeling
    information for centrally authorized products. This shifts labeling variation
    workflows to a centralized digital submission portal and may affect document formats
    encountered by the NLP system. Source: informait.com pharmaceutical labeling guide
    — [WEB-10]'
entity_taxonomy:
  deployment_target_entities:
  - entity_type: International Nonproprietary Name (INN)
    description: WHO-assigned generic drug names; the foundational identifier for
      active substances in regulatory documents.
    benchmark_coverage: 'No DrBenchmark NER schema labels INN as a distinct category.
      The CHEM UMLS Semantic Group in QUAERO and Mantra-GSC may subsume INN mentions,
      but INN is not distinguished from brand names, chemical names, or excipients
      as a dedicated class [Q103, Q106]. The EMA QRD v11 draft explicitly requires
      INN inclusion in SmPC Section 1 labeling, confirming its centrality in the target
      domain. Source: EMA QRD v11 draft — [WEB-8]'
  - entity_type: ATC code
    description: Anatomical Therapeutic Chemical classification codes assigned by
      the WHO Collaborating Centre; appear in SmPCs and regulatory submissions.
    benchmark_coverage: 'Not documented as a distinct NER class in any DrBenchmark
      schema. A 2025 study applying LLM-RAG to 81 EMA SmPC documents for IDMP extraction
      found that ATC codes were ''frequently missing or misclassified,'' confirming
      that ATC extraction is an unresolved challenge even for state-of-the-art models
      on this exact document type. Source: Kadi et al. 2025, Frontiers in Medicine
      — [WEB-11]'
  - entity_type: Excipient name
    description: Inactive ingredient names, often following pharmacopoeia or INCI
      nomenclature. Relevant for allergy warnings and excipient-specific contraindications.
    benchmark_coverage: 'Potentially subsumed under CHEM in QUAERO/Mantra-GSC schemas
      [Q103, Q106]; not documented as a distinct regulatory-excipient class. The same
      2025 SmPC extraction study found excipient dosages ''frequently missing or misclassified''
      in LLM output, reinforcing the known difficulty of excipient-specific extraction
      from regulatory text. Source: Kadi et al. 2025 — [WEB-11]'
  - entity_type: Posology expression (EMA-templated)
    description: Dose, frequency, route, and duration expressions following EMA SmPC
      section 4.2 template conventions; includes paediatric dosing sub-specifications.
    benchmark_coverage: 'PxCorpus annotates DOSAGE, FREQUENCY, MODE, DURATION [Q108]
      in spoken prescription context; register and template fidelity differ from SmPC
      posology. EMA QRD template standardizes Section 4.2 posology phrasing with mandatory
      structure; no DrBenchmark corpus is documented as covering this template-constrained
      posology format. [NEEDS VERIFICATION — deferred: below search budget; no contradictory
      evidence surfaced]'
  - entity_type: Contraindication qualifier
    description: Phrases specifying patient populations, dose thresholds, or conditions
      under which a drug is contraindicated; legally critical under EMA SmPC section
      4.3.
    benchmark_coverage: No documented NER class for contraindication qualifiers in
      any DrBenchmark schema. No published French NLP benchmark with contraindication-specific
      annotation was found. [NOT FOUND — searched French NLP regulatory benchmark
      sources; no dedicated contraindication qualifier NER schema identified in any
      public dataset]
  - entity_type: Safety warning / Special warning
    description: Standardized safety statements under EMA SmPC section 4.4; subject
      to STS-based equivalence checking in the deployment.
    benchmark_coverage: 'Not documented as a distinct NER or STS category. STS tasks
      use general clinical sentence pairs [Q41]. The EMA GVP guidance explicitly identifies
      the SmPC (section 4.4) as the primary risk minimisation tool, yet no STS benchmark
      calibrated to safety-warning equivalence was found. Source: EMA GVP Module XVI
      — [WEB-9]'
  benchmark_entity_schema_alignment: 'PARTIAL-TO-LOW — benchmark NER schemas are calibrated
    for clinical entities (pathologies, anatomical structures, procedures, UMLS Semantic
    Groups) and pharmaceutical-in-clinical-context entities (SUBSTANCE, DOSAGE, CHEM).
    Regulatory-specific entity types (INNs as distinct from CHEM, ATC codes, excipient
    names, EMA-templated posology, contraindication qualifiers) are not documented
    as explicit annotation targets. A 2025 LLM extraction study confirms that ATC
    codes and excipient-specific data are among the hardest fields to extract correctly
    from actual SmPC documents, even with RAG-augmented large language models. Source:
    Kadi et al. 2025 — [WEB-11]'
sts_requirements:
  deployment_scoring_mode: 'Regulatory equivalence scoring: small lexical differences
    in dose thresholds or contraindicated-population qualifiers are treated as critical
    mismatches, not near-synonymy. The STS function must be sensitive to legally significant
    micro-differences.'
  benchmark_scoring_mode: General semantic proximity on a continuous 0–5 scale, averaged
    across multiple annotators [Q41], evaluated via Spearman correlation and EDRM
    [Q54]. Calibrated for clinical sentence similarity, not regulatory equivalence.
  mismatch_risk: 'HIGH — a general semantic similarity scorer may rate two safety
    warnings as near-equivalent when they differ in a dose threshold or population
    qualifier that constitutes a legal mismatch under EMA standards. A 2024 analysis
    of FDA drug label NLP tools found that systems designed for general ADE extraction
    ''would need to be modified or reconfigured to lower error rates to support their
    use in a regulatory setting,'' underscoring the known gap between general biomedical
    NLP and regulatory-grade precision. Source: Bayer et al. 2021, Drug Safety — [WEB-12]'
  flagging_behavior: Borderline or high-stakes inconsistencies flag documents for
    human review; automatic rejection is not used.
  benchmark_sts_datasets:
  - dataset: CLISTER
    pairs: 1000
    source_genre: Clinical cases
    scale: 0–5 averaged
  - dataset: DEFT-2020 STS subtask
    pairs: '[NOT FOUND — searched DrBenchmark paper and DEFT-2020 documentation; pair
      count for this subtask is not explicitly stated in the DrBenchmark paper beyond
      ''clinical cases, encyclopedia and drug labels'' [Q21]; the paper cites the
      original DEFT-2020 challenge (Cardon et al., 2020) but does not restate pair
      counts]'
    source_genre: Clinical cases, encyclopedia, drug labels
    scale: 0–5
  regulatory_equivalence_calibration: '[NOT FOUND — searched for published STS rubrics,
    annotation guidelines, and NLP papers addressing dose-threshold sensitivity or
    contraindication-scope sensitivity for regulatory text equivalence; no such resource
    was identified in French or English. The literature on drug label NLP (e.g., LabelComp
    for FDA labeling, ADE Eval) addresses change detection and adverse event extraction
    but not fine-grained regulatory equivalence scoring of the kind required for EMA
    SmPC safety warning comparison. This gap appears to be a genuine absence in the
    field, not a retrieval failure. Sources searched: Drug Safety journal (Bayer et
    al. 2021 — [WEB-12]; Hoffman
    et al. 2024 — [WEB-13])]'
annotation_provenance:
  deployment_ground_truth_source: Regulatory affairs specialists and legal experts
    whose interpretive norms are governed by EMA/ANSM regulatory standards, not clinical
    annotation conventions.
  benchmark_annotation_profiles:
    documented_cases:
    - dataset: CLISTER
      annotators: Multiple annotators (professional background undocumented)
      task: STS 0–5 scoring
    - dataset: DiaMed
      annotators: Several annotators including one medical expert
      task: ICD-10 multi-label classification (not NER or STS)
    - dataset: CAS
      annotators: Automatic (Tagex 3) with manual validation at 98% precision
      task: POS tagging
    undocumented_cases: Annotator demographics, professional backgrounds, and annotation
      guidelines are NOT DOCUMENTED for the majority of DrBenchmark corpora.
    regulatory_expertise_evidence: No annotation guidelines referencing EMA/ANSM regulatory
      standards are mentioned in the benchmark paper. Author affiliations are academic
      NLP and clinical medicine institutions [Q8], not regulatory affairs or pharmacovigilance
      units.
  systematic_disagreement_risk: HIGH — biomedical NLP annotators prioritize clinical
    relevance; regulatory professionals apply rigid legal constraints. Borderline
    cases (dose threshold qualifiers, contraindication scope, population modifiers)
    are expected to yield systematic disagreements between benchmark labels and regulatory-standard
    judgments.
  annotator_alignment_verification: '[NOT FOUND — searched for published studies comparing
    biomedical NLP annotator judgments to regulatory affairs expert judgments on EMA-format
    text; no such comparative annotation study was identified. The closest related
    work (FDA ADE Eval, Bayer et al. 2021 — [WEB-12])
    used pharmacovigilance safety evaluators but addressed adverse event extraction,
    not regulatory equivalence scoring. This appears to be a genuine gap in the published
    literature.]'
infrastructure_notes:
  deployment_environment: Enterprise document management system at pharmaceutical
    companies and health agencies. Desktop/server-side processing of structured regulatory
    documents.
  interface_modality: Text-only, structured-document input (PDFs, Word documents converted
    to text). No speech, image, or multimodal input.
  connectivity: Not applicable — enterprise on-premises or cloud deployment in regulated
    IT environments; no public-internet access constraints relevant to NLP model operation.
  model_serving_constraints: 'Long-document handling is relevant: SmPCs and CTD modules
    exceed standard transformer input length limits. The benchmark addresses this
    via sentence-splitting for EMEA documents [Q37], which may introduce context loss
    for document-level regulatory reasoning.'
  data_protection_regime: 'GDPR (Regulation (EU) 2016/679) applies as the primary
    EU data protection framework for any personal data processed in the workflow.
    For regulatory submission documents specifically, EMA data submission policy and
    EudraLex Volume 2 (Notice to Applicants) govern data handling obligations. The
    IDMP ISO standards (ISO 11615, 11616, 11240, 11239, 11238) define structured data
    exchange requirements for medicinal product identification, increasingly mandatory
    in EU regulatory submissions. Source: EudraLex Volume 2 — [WEB-14];
    IDMP ISO standards overview — [WEB-15]'
  reproducibility_note: DrBenchmark required approximately 2,500 GPU hours [Q93];
    HuggingFace toolkit and documented hyperparameters [Q49] support reproducibility
    for users with HPC access.
cultural_and_professional_norms_notes: '- The target population operates within a
  highly codified professional culture governed by EMA/ANSM procedural norms, not
  general biomedical or clinical conventions.

  - Precision and legal defensibility are paramount: a ''close enough'' semantic match
  is professionally and legally unacceptable if the textual difference carries regulatory
  significance.

  - The community is familiar with EMA template conventions (SmPC sections 4.1–4.9,
  CTD module structure) and treats deviations from template phrasing as meaningful
  signals.

  - Regulatory professionals distinguish between INN (generic) and brand-name references,
  and between posology statements with different legal force (e.g., ''must not be
  used'' vs. ''should be used with caution'').

  - The workflow is pre-submission: errors caught by the system are caught before
  official regulatory authority review, making false negatives (missed mismatches)
  the higher-cost error type.

  - No religious, gender, or socio-cultural audience considerations that diverge from
  general French professional norms.

  '
domain_specific_notes:
  legal_register: 'Regulatory pharmaceutical French is a distinct legal register with
    standardized section headings, mandatory phrasing conventions (derived from EMA
    QRD templates), and precise terminology requirements (INN over brand name, WHO-standard
    posology units). It differs from clinical French in formality, formulaicity, and
    the legal consequences of paraphrase. The EMA QRD template (current v10.4, February
    2024; draft v11 in consultation 2025) mandates that standard statements ''must
    be used whenever they are applicable'' and that deviations require case-by-case
    EMA justification. Source: EUPATI SmPC guidance — [WEB-2]'
  ema_ansm_template_dependency: 'EMA publishes standard SmPC and PIL QRD templates
    that constrain the vocabulary and sentence structure of compliant documents. The
    current operational template is QRD v10.4 (February 2024); a draft v11 template
    is under public consultation (April–August 2025) focused on improving package
    leaflet structure. NLP models trained on free-form clinical text may not correctly
    segment, tokenize, or interpret these template-constrained structures. Source:
    EMA QRD templates page — [WEB-7]'
  pharmacovigilance_overlap: 'Safety warnings subject to STS-based equivalence checking
    are also relevant to pharmacovigilance reporting obligations; the system''s output
    may feed into PSUR/PBRER workflows. The EMA GVP Module XVI explicitly identifies
    the SmPC as the ''fundamental routine risk minimisation measure (RMM) tool.''
    [NEEDS VERIFICATION — deferred: whether the deployment scope explicitly includes
    pharmacovigilance document types beyond safety warning equivalence in SmPC; requires
    clarification from deployment team]'
  patent_domain_specificity: Pharmaceutical patent claims use a syntactically distinct
    legal language (single-sentence claims, Markush structure definitions, 'comprising'
    constructs) that differs from both clinical and regulatory prose. Patent NER in
    Mantra-GSC [Q40] is low-resource and CamemBERT-based models fail to generate non-'O'
    labels [Q73]; this segment of the deployment requires separate validation.
  benchmark_genre_overlap_summary: 'QUAERO EMEA sub-corpus (DrBenchmark) contains
    approximately 10 segmented EMEA drug leaflet documents (PIL register, not SmPC
    register) in total across train/dev/test splits, annotated with 10 UMLS Semantic
    Group categories. Mantra-GSC EMEA and Patents subsets provide a second partial
    overlap. All other DrBenchmark sources (clinical cases, research abstracts, clinical
    trials, spoken prescriptions) represent register mismatches of varying severity.
    No SmPC, CTD module, or EU-RMP text is confirmed as a DrBenchmark data source.
    Source: QUAERO corpus documentation — [WEB-4]; DrBenchmark
    QUAERO HuggingFace dataset — [WEB-3]'
  net_new_smpc_extraction_challenge: 'A 2025 peer-reviewed study (Kadi et al., Frontiers
    in Medicine) applied RAG-augmented LLMs (Claude 3.5 Sonnet, Gemini 1.5 Flash)
    to 81 EMA SmPC documents for IDMP-structured data extraction. Findings directly
    relevant to this deployment: ATC codes and excipient dosage fields were among
    the most frequently missing or misclassified outputs, even with state-of-the-art
    models. This provides direct evidence that regulatory-specific entity extraction
    from real SmPCs remains an unsolved problem, reinforcing the gap assessment for
    INN/ATC/excipient NER in DrBenchmark. Source: Kadi et al. 2025 — [WEB-11]'
  net_new_idmp_regulatory_context: 'EU IDMP (IDentification of Medicinal Products)
    standards — a set of five ISO standards (ISO 11615, 11616, 11240, 11239, 11238)
    — are mandatory for EMA pharmaceutical submissions. IDMP compliance requires structured
    extraction of data attributes (including ATC codes, INN, excipient dosages, therapeutic
    indications) from unstructured SmPC and eCTD documents. Approximately 70% of required
    IDMP data attributes reside in unstructured text. This regulatory data-structuring
    obligation is directly in scope for the deployment system and has no coverage
    in DrBenchmark. Source: IQVIA NLP regulatory affairs factsheet — [WEB-16];
    Linguamatics IDMP blog — [WEB-17]'
flagged_gaps_for_web_search:
- gap_id: 1
  topic: Regulatory document genre coverage in DrBenchmark
  query: DrBenchmark QUAERO EMEA drug leaflet SmPC CTD module NER STS French regulatory
    document genre coverage
  priority: HIGH
  resolution_status: 'RESOLVED — QUAERO EMEA subset contains PIL (package leaflet)
    text only, not SmPC text. Approximately 10 segmented documents in total train/dev/test
    splits. No SmPC, CTD, or EU-RMP text confirmed in any DrBenchmark source. Source:
    [WEB-3]; [WEB-4]'
- gap_id: 2
  topic: INN, ATC code, excipient, and EMA posology NER entity taxonomy in DrBenchmark
  query: INN ATC code excipient NER French regulatory NLP annotation benchmark EMA
    ANSM entity schema
  priority: HIGH
  resolution_status: 'RESOLVED — No DrBenchmark NER schema includes INN, ATC code,
    or excipient as distinct entity classes. CHEM in QUAERO/Mantra-GSC may subsume
    INN mentions but does not distinguish them. External evidence (Kadi et al. 2025)
    confirms ATC and excipient extraction from SmPCs is actively unsolved even with
    LLMs. Source: [WEB-11]'
- gap_id: 3
  topic: STS scoring calibration for regulatory equivalence
  query: regulatory equivalence semantic textual similarity drug labeling EMA scoring
    rubric dose threshold French NLP annotation
  priority: HIGH
  resolution_status: 'RESOLVED (gap confirmed) — No published STS rubric or annotator
    guideline addressing dose-threshold sensitivity for regulatory text equivalence
    was found in French or English NLP literature. Related English-language work on
    FDA drug label change detection (LabelComp, ADE Eval) uses different task formulations
    (change detection, ADE extraction) not applicable to regulatory equivalence scoring.
    This is a genuine field-level gap. Sources: [WEB-12];
    [WEB-13]'
- gap_id: 4
  topic: Annotator profiles and regulatory expertise in DrBenchmark NER/STS labels
  query: DrBenchmark annotator professional background regulatory affairs pharmacologist
    EMA ground truth label quality French biomedical NLP
  priority: HIGH
  resolution_status: RESOLVED (gap confirmed) — No evidence of regulatory affairs
    annotator involvement in any DrBenchmark dataset was found. Benchmark author affiliations
    [Q8] are academic NLP and clinical medicine institutions. No annotation guidelines
    referencing EMA/ANSM standards are documented.
- gap_id: 5
  topic: ANSM and EMA regulatory French language register versus clinical French
  query: ANSM EMA French regulatory language register NLP corpus SmPC legal prose
    clinical French difference terminology
  priority: MEDIUM
  resolution_status: 'PARTIALLY RESOLVED — No French NLP corpus specifically designed
    to capture the EMA regulatory register was found. The QRD template structure mandates
    specific phrasing conventions (standard statements that ''must be used whenever
    applicable,'' deviation requires justification), confirming the register is distinct
    and highly constrained. The distinction from clinical French is well-established
    in the deployment context but is not empirically characterized in any published
    NLP study. Sources: EMA QRD page — [WEB-7];
    EUPATI SmPC guidance — [WEB-2]'
- gap_id: 6
  topic: Patent claims coverage and entity schema in Mantra-GSC Patents subset
  query: Mantra-GSC Patents French NER drug claim regulatory entity recognition benchmark
    performance evaluation
  priority: MEDIUM
  resolution_status: 'RESOLVED — Mantra-GSC EMEA and Patents subsets share an identical
    10-class UMLS annotation schema (no drug-regulatory-specific classes). CamemBERT-based
    models fail to generate non-''O'' labels on this low-resource subset [Q73]. The
    patent entity schema does not include INN/ATC/excipient-specific categories distinct
    from the EMEA annotation scheme. Source: DrBenchmark paper — [WEB-6]'
- gap_id: 7
  topic: Existence of French regulatory NLP benchmarks or datasets outside DrBenchmark
  query: French pharmaceutical regulatory NLP benchmark SmPC EMA ANSM NER STS evaluation
    dataset 2023 2024
  priority: MEDIUM
  resolution_status: RESOLVED (gap confirmed) — No French NLP benchmark specifically
    targeting EU regulatory pharmaceutical text (SmPC, CTD, EU-RMP) was identified
    in searches. The most recent relevant work (Kadi et al. 2025 on SmPC IDMP extraction)
    uses English-language EMA SmPCs and is not a NER/STS benchmark. DrBenchmark remains
    the only large French biomedical NLU benchmark, per its own claim [Q16], which
    searches did not contradict.
- gap_id: 8
  topic: EMA SmPC current template version and section structure
  query: EMA SmPC summary of product characteristics current template version section
    structure 4.1 4.2 4.3 4.4
  priority: LOW
  resolution_status: 'RESOLVED — Current operational QRD template is v10.4 (February
    2024). Draft v11 is in public consultation (April–August 2025), focused on package
    leaflet improvements; SmPC changes in v11 are noted as minor. QRD templates are
    mandatory for all EU centralized, MRP, and DCP submissions. Source: EMA QRD templates
    page — [WEB-7];
    v10.4 template PDF — [WEB-18]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.ema.europa.eu/en/about-us/careers |
| WEB-2 | https://learning.eupati.eu/mod/book/view.php?id=858&chapterid=770 |
| WEB-3 | https://huggingface.co/datasets/DrBenchmark/QUAERO |
| WEB-4 | https://quaerofrenchmed.limsi.fr/ |
| WEB-5 | https://www.pharmaregulatory.in/qrd-templates-explained-ultimate-guide-to-ema-compliant-labelling-formats/ |
| WEB-6 | https://arxiv.org/html/2402.13432v1 |
| WEB-7 | https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/product-information-requirements/product-information-qrd-templates-human |
| WEB-8 | https://www.ema.europa.eu/en/documents/template-form/quality-review-documents-qrd-annotated-template-v11-draft-public-consultation_en.pdf |
| WEB-9 | https://www.ema.europa.eu/en/documents/regulatory-procedural-guideline/guideline-good-pharmacovigilance-practices-gvp-module-xvi-risk-minimisation-measures-rev-3_en.pdf |
| WEB-10 | https://informait.com/news/pharmaceutical-labeling-requirements-a-complete-guide |
| WEB-11 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12380897/ |
| WEB-12 | https://link.springer.com/article/10.1007/s40264-020-00996-3 |
| WEB-13 | https://link.springer.com/article/10.1007/s40264-024-01468-8 |
| WEB-14 | https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-2_en |
| WEB-15 | https://globalforum.diaglobal.org/issue/november-2019/identification-of-medicinal-products/ |
| WEB-16 | https://www.iqvia.com/-/media/iqvia/pdfs/library/fact-sheets/nlp-text-analytics-for-regulatory-affairs.pdf |
| WEB-17 | https://www.linguamatics.com/blog/countdown-idmp-compliance-are-you-ready |
| WEB-18 | https://www.ema.europa.eu/en/documents/template-form/qrd-product-information-template-version-104-highlighted_en.pdf |

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
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Benchmark:** DrBenchmark — A Large Language Understanding Benchmark for the Biomedical French Domain
**Datasets analyzed:** 11 datasets (QUAERO, FrenchMedMCQA, DEFT2020, MORFITT, CLISTER, MANTRAGSC, E3C, PxCorpus, DiaMED, DEFT2021, CAS, ESSAI)
**Analysis date:** 2025-07-14

---

### Per-Dataset Fit Assessment

#### DrBenchmark/QUAERO

- **Task:** Named Entity Recognition (token-level, IOB2), two configs: `emea` (drug leaflets) and `medline` (biomedical titles)
- **Deployment fit:** **Partial** — The `emea` config is the single strongest genre match in the entire benchmark, containing actual EMEA drug leaflet text (patient information leaflet register) with pharmaceutical composition lists, posology expressions, contraindication blocks, and EMA administrative references. However, the `medline` config (~65% of total examples) contains research-register biomedical titles with off-topic content, and the UMLS-based entity schema collapses all chemical entities into a single CHEM class without INN/excipient/ATC distinction.
- **Key strengths:**
  - `emea` config directly contains EU regulatory drug leaflet text in French (QUAERO-D1, QUAERO-D2, QUAERO-D6, QUAERO-D9)
  - Posology expressions and administration routes annotated (QUAERO-D3, QUAERO-D4)
  - Contraindication blocks with population qualifiers present (QUAERO-D5, QUAERO-D6)
  - Brand name and INN co-occurrence annotated as CHEM (QUAERO-D7, QUAERO-D8)
- **Key concerns:**
  - CHEM tag conflates INNs, excipients, and other chemicals with no sub-class distinction (QUAERO-D10, QUAERO-D11) — MAJOR
  - ATC codes, marketing authorization numbers, and regulatory identifiers receive O tag (QUAERO-D12) — MAJOR
  - `medline` config (majority of examples) contains non-regulatory, non-pharmaceutical content including historical and psychosocial topics (QUAERO-D13, QUAERO-D14, QUAERO-D15) — MAJOR
  - Annotation norms are UMLS Semantic Groups, not EMA/ANSM regulatory entity standards; contraindication conditions are tagged by entity type but not as regulatory constructs (QUAERO-D16, QUAERO-D17) — MAJOR
  - Document splitting artifacts produce corrupted sentence fragments (QUAERO-D19, QUAERO-D20) — MINOR

---

#### DrBenchmark/FrenchMedMCQA

- **Task:** Multiple-Choice Question Answering (MCQA), French pharmacy diploma exam questions, 5 options, single or multiple correct answers
- **Deployment fit:** **Weak** — The task type (closed-set answer selection from exam questions) does not match either NER or STS as required by the deployment. Despite containing relevant pharmaceutical vocabulary, no example presents regulatory prose for entity extraction or pairwise sentence comparison.
- **Key strengths:**
  - Dense pharmaceutical terminology: INNs, drug classes, contraindications, and adverse effects appear as answer options (FRENCHMEDMCQA-D1, FRENCHMEDMCQA-D2, FRENCHMEDMCQA-D3)
  - Explicit SmPC reference (RCP) appears at least once (FRENCHMEDMCQA-D7)
  - Pharmaceutical formulation and analytical chemistry content partially overlaps with regulatory CTD Module 3 knowledge domains (FRENCHMEDMCQA-D4, FRENCHMEDMCQA-D5, FRENCHMEDMCQA-D8, FRENCHMEDMCQA-D9)
- **Key concerns:**
  - CRITICAL task type mismatch: MCQA evaluates declarative knowledge retrieval, not NER span extraction or STS pairwise scoring (FRENCHMEDMCQA-D11, FRENCHMEDMCQA-D14)
  - CRITICAL genre mismatch: exam interrogative format vs. declarative regulatory prose (FRENCHMEDMCQA-D12, FRENCHMEDMCQA-D15)
  - Drug names appear as answer options, not as extractable entities in continuous text; ATC codes absent (FRENCHMEDMCQA-D13)
  - Significant fraction of questions covers topics irrelevant to pharmaceutical regulatory work (parasitology, blood group genetics) (FRENCHMEDMCQA-D16, FRENCHMEDMCQA-D17)
  - Ground truth derived from pharmacy exam answer keys, not EMA/ANSM regulatory standards (MINOR OC concern)

---

#### DrBenchmark/DEFT2020

- **Task:** Semantic Textual Similarity (Task 1: 0–5 scored pairs; Task 2: most-similar-sentence MCQA)
- **Deployment fit:** **Partial** — Task 1 directly tests STS in French with genuine drug leaflet content in a meaningful fraction of pairs. However, the scoring calibration reflects general semantic proximity rather than regulatory equivalence, and a large fraction of pairs derives from encyclopedic and non-pharmaceutical content.
- **Key strengths:**
  - Genuine French drug leaflet text in Task 1, including contraindication phrasing, safety warnings, and dose-time threshold language (DEFT2020-D1, DEFT2020-D2, DEFT2020-D3, DEFT2020-D4)
  - Multi-annotator scoring with individual scores available, enabling inter-annotator variance analysis (DEFT2020-D7, DEFT2020-D8)
  - Task 2 tests near-synonym discrimination in drug safety text, structurally analogous to consistency checking (DEFT2020-D12)
  - Regulatory-register French vocabulary appears in drug leaflet pairs (DEFT2020-D9, DEFT2020-D10, DEFT2020-D11)
- **Key concerns:**
  - CRITICAL: Large proportion of pairs from encyclopedic content (beekeeping, sports, history) entirely irrelevant to regulatory deployment (DEFT2020-D13, DEFT2020-D14, DEFT2020-D15)
  - MAJOR: STS scores reflect general semantic proximity; legally critical qualifiers (specific opioid names, "sous stricte surveillance médicale," "potentialisation réciproque") are not penalized at the score level (DEFT2020-D16, DEFT2020-D17, DEFT2020-D18, DEFT2020-D20)
  - MAJOR: No evidence of EMA/ANSM-aligned annotation guidelines; annotators are NLP community members, not regulatory specialists (DEFT2020-D19)
  - MAJOR: Heterogeneous genres (clinical cases, encyclopedia, Cochrane abstracts, drug leaflets) conflated without stratification (DEFT2020-D21, DEFT2020-D22)
  - MINOR: Task 2 distractors include trivially non-medical options, reducing discriminative validity (DEFT2020-D23, DEFT2020-D24)

---

#### DrBenchmark/MORFITT

- **Task:** Multi-label classification of biomedical abstracts into 12 medical specialties
- **Deployment fit:** **Weak** — Abstract-level specialty classification is a different task type from NER and STS, the genre is exclusively PMC research abstracts (not regulatory documents), and a substantial proportion covers veterinary medicine and non-EU geographic contexts.
- **Key strengths:**
  - Pharmacology specialty label present with some drug-adjacent content (MORFITT-D3, MORFITT-D4, MORFITT-D5)
  - Multi-label annotation structure is technically consistent (MORFITT-D6)
- **Key concerns:**
  - CRITICAL task type mismatch: multi-label classification at abstract level vs. NER and STS (MORFITT-D7, MORFITT-D8)
  - CRITICAL genre mismatch: PMC research abstracts only; no regulatory document genre (MORFITT-D9, MORFITT-D10)
  - MAJOR: No regulatory entity annotation whatsoever; drug names appear in text but are unannotated (MORFITT-D11, MORFITT-D12)
  - MAJOR: Substantial non-EU geographic scope (Canada, Japan, Saudi Arabia) diverges from EMA/ANSM deployment (MORFITT-D13, MORFITT-D14, MORFITT-D15, MORFITT-D16)
  - MAJOR: Veterinary content with no human drug regulatory relevance (MORFITT-D17, MORFITT-D18, MORFITT-D19)

---

#### DrBenchmark/CLISTER

- **Task:** Semantic Textual Similarity (STS), 1,000 clinical sentence pairs, 0–5 scale averaged across annotators
- **Deployment fit:** **Partial (with significant OO concern)** — CLISTER directly tests STS in French biomedical language and provides genuine continuous similarity scores with multi-annotator averaging. However, source genre is exclusively clinical case reports (not regulatory documents), and the scoring scheme demonstrates insensitivity to numerically significant differences that would be regulatory-critical mismatches.
- **Key strengths:**
  - French STS with genuine multi-annotator averaged labels (CLISTER-D6, CLISTER-D7)
  - Full 0–5 label range with non-integer values demonstrating continuous distribution (CLISTER-D8, CLISTER-D9)
  - Some pharmaceutical expressions present (drug names, dosage pairs) (CLISTER-D2, CLISTER-D3, CLISTER-D4, CLISTER-D5)
- **Key concerns:**
  - CRITICAL: Source domain exclusively clinical case reports; no SmPC, leaflet, CTD, or EU regulatory document text (CLISTER-D10, CLISTER-D11)
  - CRITICAL: Scoring calibrated for general semantic proximity; quantitative differences of 2×, 14×, and 60× in clinical measurements score 4.0, 3.75, and 3.0 respectively — fundamentally incompatible with regulatory equivalence requirements (CLISTER-D12, CLISTER-D13, CLISTER-D14)
  - MAJOR: Different INNs scored as partially similar (2.0) due to structural template match; regulatory judgment would score 0 (CLISTER-D17, CLISTER-D18)
  - MAJOR: Annotator population not documented; scoring pattern inconsistent with regulatory-standard equivalence norms (CLISTER-D17, CLISTER-D18)
  - MINOR: Tabular data fragments appear as sentence pairs (CLISTER-D19, CLISTER-D20); ceiling dominated by tense-only variations (CLISTER-D21, CLISTER-D22)

---

#### DrBenchmark/MANTRAGSC

- **Task:** Named Entity Recognition (NER, IOB2), multilingual, with French `fr_emea`, `fr_medline`, and `fr_patents` configs
- **Deployment fit:** **Partial** — The `fr_emea` and `fr_patents` configs provide the most direct genre overlap of any NER dataset in the benchmark (actual EMEA drug label text and French patent claims). However, the extremely small size of each French config (test set n=20), the CHEM-conflation problem, and the absence of INN/ATC/excipient-specific schema classes are significant limitations.
- **Key strengths:**
  - `fr_emea` contains genuine EMEA drug label text with posology, contraindications, and INN mentions (MANTRAGSC-D1, MANTRAGSC-D2, MANTRAGSC-D3, MANTRAGSC-D4)
  - INN and salt form co-occurrence present in EMEA examples (MANTRAGSC-D5, MANTRAGSC-D6)
  - `fr_patents` provides French pharmaceutical patent claim language (MANTRAGSC-D7, MANTRAGSC-D8)
  - Adverse event language and SmPC section headers present (MANTRAGSC-D9, MANTRAGSC-D10)
- **Key concerns:**
  - MAJOR: Extremely small French subset (test n=20 per config); no statistically robust NER evaluation possible (MANTRAGSC-D11, MANTRAGSC-D12)
  - MAJOR: CHEM tag conflates INNs, brand names, excipient salt forms — no regulatory entity subclass distinction (MANTRAGSC-D13, MANTRAGSC-D14)
  - MAJOR: `fr_medline` config is non-regulatory research abstract titles (MANTRAGSC-D15, MANTRAGSC-D16)
  - MAJOR: Contraindication and dose-threshold qualifiers not annotated at regulatory granularity; patient population qualifiers tagged LIVB/DISO rather than as contraindication type (MANTRAGSC-D4, MANTRAGSC-D2)
  - MINOR: Patent examples contain highly technical chemical structure notation with sparse annotation (MANTRAGSC-D17)

---

#### DrBenchmark/E3C

- **Task:** Named Entity Recognition (NER), multilingual clinical cases, two annotation layers: clinical (CLINENTITY) and temporal (EVENT/ACTOR/BODYPART/TIMEX3/RML)
- **Deployment fit:** **Weak** — Both annotation schemas capture clinical case entities (pathologies, temporal events, actors) with no pharmaceutical regulatory entity types. Drug names appear in text but are demonstrably unannotated. The genre is exclusively clinical case narrative.
- **Key strengths:**
  - French clinical biomedical language in formal register (E3C-D1, E3C-D3)
  - IOB2 NER format compatible with deployment output format
- **Key concerns:**
  - CRITICAL: Entire dataset is clinical case reports; no regulatory document genre (E3C-D4, E3C-D5)
  - CRITICAL: Neither annotation schema includes any pharmaceutical or regulatory entity type; drug names such as ciclosporine receive O tag (E3C-D2, E3C-D6, E3C-D7)
  - MAJOR: Non-French configs (Basque, English, Spanish, Italian) present in repository and could contaminate evaluation if not filtered (E3C-D8, E3C-D9)
  - MAJOR: Clinical case narrative register fundamentally distinct from regulatory document structure (E3C-D10, E3C-D11)
  - MINOR: High prevalence of all-O examples contributes to annotation sparsity (E3C-D12, E3C-D13)

---

#### DrBenchmark/PxCorpus

- **Task:** Intent classification (4 classes) + NER (38 classes) over transcribed spoken drug prescription utterances
- **Deployment fit:** **Partial (with CRITICAL register caveat)** — PxCorpus has the richest pharmaceutical entity schema in the benchmark (38 NER classes including DRUG, SUBSTANCE, DOSAGE, FREQUENCY, MODE, DURATION) and the `replace` intent class directly captures prescription correction analogous to compliance flagging. However, the entire corpus is transcribed speech with pervasive spoken-language artifacts, making register transfer to formal regulatory documents highly uncertain.
- **Key strengths:**
  - Richest pharmaceutical NER schema in DrBenchmark: 38 classes covering DRUG, SUBSTANCE, DOSAGE, FREQUENCY, MODE, DURATION (PXCORPUS-D1, PXCORPUS-D2, PXCORPUS-D3)
  - INN and brand name co-occurrence with salt form distinctions (PXCORPUS-D8)
  - `replace` intent class captures dosage correction acts directly relevant to compliance flagging (PXCORPUS-D6, PXCORPUS-D7)
  - Dosage unit variety across mg, µg, ml, UI (PXCORPUS-D4)
- **Key concerns:**
  - CRITICAL: Spoken transcription register with ASR artifacts, truncations, code-switching, and informal language entirely absent from regulatory documents (PXCORPUS-D10, PXCORPUS-D11, PXCORPUS-D12, PXCORPUS-D13)
  - CRITICAL: No regulatory document genre present; no SmPC, leaflet, or CTD text (PXCORPUS-D14)
  - MAJOR: NER schema does not capture ATC codes, excipient names, or EMA-templated contraindication qualifiers (PXCORPUS-D15, PXCORPUS-D16)
  - MAJOR: Extreme class imbalance — `replace` class has ~3 examples in 500-item buffer, the most deployment-relevant intent (PXCORPUS-D17, PXCORPUS-D18)
  - MAJOR: No STS task present

---

#### DrBenchmark/DiaMED

- **Task:** Multi-class classification into 22 ICD-10 chapter-level labels, 739 French clinical cases from *The Pan African Medical Journal*
- **Deployment fit:** **Weak** — ICD-10 classification is not NER or STS. The source genre is clinical case narrative, the geographic origin is predominantly Sub-Saharan and North African rather than EU, and no regulatory entity annotation exists. The only distinction from similar datasets is its documented inter-annotator agreement methodology.
- **Key strengths:**
  - Only DrBenchmark dataset with documented inter-annotator agreement (Cohen's Kappa, Gwet's AC1) and one medical expert annotator
  - French clinical prose confirmed across all examples (DIAMED-D1, DIAMED-D8)
  - Drug names and dosages incidentally present in some cases (DIAMED-D1, DIAMED-D2, DIAMED-D12)
- **Key concerns:**
  - CRITICAL: ICD-10 classification task provides no NER or STS signal for the deployment (DIAMED-D6, DIAMED-D9, DIAMED-D13)
  - CRITICAL: Clinical case narrative genre entirely distinct from EU regulatory document prose (DIAMED-D6, DIAMED-D9)
  - CRITICAL: No regulatory entity annotation; drug mentions are incidental and unannotated (DIAMED-D12)
  - MAJOR: Sub-Saharan/North African geographic and clinical context diverges from EMA/ANSM regulatory French (DIAMED-D9, DIAMED-D3, DIAMED-D11)
  - MAJOR: Severely skewed label distribution with near-zero representation for several ICD-10 chapters
  - MINOR: ICD-10 taxonomy only tangentially related to any deployment capability

---

#### DrBenchmark/DEFT2021

- **Task:** Multi-label classification (23 MeSH-C axes) and NER (13 entity types including SUBSTANCE, DOSAGE, MODE, DURATION) over 275 French clinical cases
- **Deployment fit:** **Partial** — The NER config's SUBSTANCE, DOSAGE, and MODE entity types are the closest multi-type clinical NER annotation to the deployment's pharmaceutical entity extraction needs. However, the genre is exclusively clinical case reports, INN/ATC/excipient distinctions are not made, and no regulatory-equivalence STS capability is present.
- **Key strengths:**
  - NER schema includes SUBSTANCE, DOSAGE, MODE, DURATION — partial mapping to deployment's pharmaceutical entity targets (DEFT2021-D3, DEFT2021-D4, DEFT2021-D5)
  - Dense posology expressions with drug names, routes, frequencies in French clinical text (DEFT2021-D1, DEFT2021-D2)
  - Pharmacology and toxicology MeSH specialties present in classification labels (DEFT2021-D6, DEFT2021-D7)
- **Key concerns:**
  - CRITICAL: Genre exclusively clinical case reports; no regulatory document structure (DEFT2021-D8, DEFT2021-D9, DEFT2021-D10)
  - CRITICAL: NER schema dominated by DISO, PROC, ANAT; SUBSTANCE does not distinguish INN from excipient or provide ATC linkage (DEFT2021-D11, DEFT2021-D12, DEFT2021-D13)
  - MAJOR: Annotation norms clinical/biomedical NLP; no EMA/ANSM regulatory standards referenced (DEFT2021-D14, DEFT2021-D15)
  - MAJOR: No STS task present (DEFT2021-D16)
  - MINOR: Small dataset (275 cases) limits generalizability

---

#### DrBenchmark/CAS

- **Task:** Negation/speculation classification and NER (negation/speculation scope), plus POS tagging, over 3,790 French clinical cases
- **Deployment fit:** **Weak** — Negation and speculation scope annotation is linguistically relevant to interpreting safety warnings but does not annotate pharmaceutical entities or regulatory equivalence. Genre is entirely clinical case narrative.
- **Key strengths:**
  - Negation and speculation annotation has indirect relevance to safety-warning interpretation (CAS-D5, CAS-D6)
  - Drug names incidentally present in text (CAS-D2, CAS-D3)
  - Large corpus; French biomedical language confirmed throughout
- **Key concerns:**
  - CRITICAL: Genre exclusively clinical case reports; no regulatory document present (CAS-D8, CAS-D9)
  - CRITICAL: NER schema annotates only negation/speculation scope, not pharmaceutical entities; drug names receive O tag (CAS-D10, CAS-D11)
  - MAJOR: POS annotation is machine-generated (Tagex 3); negation/speculation annotators undocumented; no regulatory expert involvement (CAS-D12)
  - MAJOR: Negation/speculation labels do not distinguish legally critical qualifiers from general clinical hedges
  - MINOR: Severe label imbalance (~70% neutral); negation_speculation rare (CAS-D13)

---

#### DrBenchmark/ESSAI

- **Task:** Negation/speculation classification and NER (negation/speculation scope), plus POS tagging, over 7,247 French clinical trial protocols
- **Deployment fit:** **Weak** — Clinical trial protocol register is closer to regulatory language than clinical case reports, and the drug vocabulary is rich. However, the NER schema annotates linguistic hedging scope rather than pharmaceutical entities, and the genre remains trial protocols rather than EU regulatory submissions.
- **Key strengths:**
  - Rich pharmaceutical vocabulary: INNs and brand names from oncology trials (ESSAI-D1, ESSAI-D2, ESSAI-D14, ESSAI-D15)
  - Dosage and frequency expressions present (ESSAI-D3, ESSAI-D4)
  - Negation/speculation annotation has indirect relevance to safety-warning compliance (ESSAI-D5, ESSAI-D6)
  - Exclusion criteria with organ-function contraindication-like framing (ESSAI-D7, ESSAI-D8)
- **Key concerns:**
  - CRITICAL: Genre is clinical trial protocol summaries; not SmPC, leaflet, CTD, or EU regulatory submission prose (ESSAI-D10, ESSAI-D11)
  - CRITICAL: NER schema annotates hedging scope, not pharmaceutical regulatory entities (ESSAI-D12, ESSAI-D13)
  - MAJOR: No ATC codes, excipient nomenclature, or INN-standardized entries (ESSAI-D14, ESSAI-D15)
  - MAJOR: Negation/speculation labels do not capture regulatory-legal significance of population qualifiers or dose thresholds (ESSAI-D16, ESSAI-D17)
  - MAJOR: POS annotation machine-generated; no regulatory expert involvement documented (ESSAI-D18)
  - MINOR: Oncology domain only; other therapeutic areas absent (ESSAI-D19, ESSAI-D20)

---

### Cross-Cutting Strengths

**1. Consistent French biomedical language across all datasets**
Every dataset in the benchmark delivers French-language text in Latin script with standard diacritics. No modality mismatch, script issue, or dialect problem exists for the deployment's French language requirement. The French biomedical register across QUAERO-D1, MANTRAGSC-D1, DEFT2021-D2, ESSAI-D1, and CLISTER-D1 is consistently professional and technically dense.

**2. Pharmaceutical entity vocabulary is present across multiple datasets**
Drug names (INNs and brand names), dosage expressions, and administration routes appear in text across QUAERO-emea (QUAERO-D3, QUAERO-D7), MANTRAGSC-fr_emea (MANTRAGSC-D2, MANTRAGSC-D3), DEFT2020 (DEFT2020-D4), DEFT2021 (DEFT2021-D1, DEFT2021-D4), PxCorpus (PXCORPUS-D1, PXCORPUS-D8), and ESSAI (ESSAI-D2). This vocabulary coverage provides a foundation for pharmaceutical concept recognition even if not annotated with the regulatory entity distinctions required.

**3. EMEA drug label genre coverage in two NER datasets**
Both QUAERO-emea and MANTRAGSC-fr_emea provide genuine EMEA drug label text — the closest genre match to the deployment's SmPC and patient information leaflet targets. Together they confirm that French regulatory-register pharmaceutical prose does appear in the benchmark (QUAERO-D1, QUAERO-D6, MANTRAGSC-D1, MANTRAGSC-D9, MANTRAGSC-D10). This is the benchmark's most distinctive and deployment-relevant content cluster.

**4. STS task presence in two datasets**
CLISTER and DEFT2020 together provide the only STS capability in the benchmark. DEFT2020 additionally includes drug leaflet sentence pairs (DEFT2020-D1, DEFT2020-D2, DEFT2020-D9) — a subset that meaningfully overlaps with the deployment's safety-warning equivalence task, even if the scoring calibration is insufficient for regulatory purposes.

**5. Negation and speculation annotation across CAS and ESSAI**
Two large corpora (CAS: 3,790 cases; ESSAI: 7,247 protocols) provide negation/speculation scope annotation. While insufficient for regulatory entity NER, this annotation is relevant to the deployment's need to interpret safety warnings that may be negated, hedged, or conditionally qualified. CAS-D5, CAS-D6, ESSAI-D5, ESSAI-D7 demonstrate the coverage.

---

### Cross-Cutting Weaknesses

**CRITICAL — Benchmark-wide absence of EU regulatory document genres (SmPC, CTD, EU-RMP)**
No confirmed instance of SmPC text, CTD module narrative, or EU Risk Management Plan prose appears in any dataset. QUAERO-emea and MANTRAGSC-fr_emea contain patient information leaflet (PIL) text, not SmPC text. The web search findings confirm this explicitly: the QUAERO EMEA subset contains approximately 10 segmented PIL-register documents total across train/dev/test, and no SmPC, CTD, or EU-RMP source is documented anywhere in DrBenchmark. This is the highest-severity validity gap for the deployment: QUAERO-D9, MANTRAGSC-D10 show EMA administrative language, but the formulaic section-structured legal prose of SmPC sections 4.1–4.9 is absent. Every other dataset (MORFITT-D9, MORFITT-D10, E3C-D4, DIAMED-D6, CAS-D8, ESSAI-D10, DEFT2021-D8) confirms clinical case or research abstract genre.

**CRITICAL — Benchmark-wide absence of INN/ATC/excipient-specific NER entity classes**
Across all 11 datasets, no NER schema distinguishes INNs from excipient names, provides ATC code annotation, or captures EMA-templated contraindication qualifiers as a dedicated entity type. The benchmark's best approximations — CHEM in QUAERO and MANTRAGSC — conflate INNs, excipients, and all chemical compounds under one label (QUAERO-D10, QUAERO-D11, MANTRAGSC-D13, MANTRAGSC-D14). DEFT2021's SUBSTANCE tag is the next closest but equally undifferentiated (DEFT2021-D13). The web search findings confirm that ATC code and excipient-specific extraction from real SmPCs remains an unresolved challenge even for state-of-the-art LLMs (Kadi et al. 2025), reinforcing that this is not merely a benchmark gap but a field-level gap that the deployment cannot resolve using this benchmark's evaluation signal.

**CRITICAL — STS scoring calibrated for general semantic proximity, incompatible with regulatory equivalence**
Both STS datasets (CLISTER and DEFT2020) use a 0–5 scale reflecting general semantic similarity. CLISTER-D12 demonstrates a 2× quantitative difference scoring 4.0; CLISTER-D13 shows a 60× difference scoring 3.0; DEFT2020-D16 shows specific opioid names added in a drug safety warning scoring 4.0 without penalization. DEFT2020-D20 shows a mechanism qualifier dropped from an alcohol warning scoring 3.8. The deployment explicitly requires sensitivity to precisely these micro-differences (A3). No published STS rubric calibrated for dose-threshold sensitivity or population-qualifier sensitivity in regulatory text was found in the web search findings — confirming this is a genuine field-level gap.

**CRITICAL — Absence of regulatory affairs annotator expertise across all datasets**
No dataset in DrBenchmark documents involvement of EMA/ANSM regulatory affairs specialists in annotation. The only confirmed medical expert (DiaMED) annotated ICD-10 chapter classification, not NER or STS tasks (DIAMED benchmark YAML Q45). Annotation demographics are undocumented for the majority of corpora. Authors are affiliated with French academic NLP and clinical medicine institutions (benchmark YAML Q8), not regulatory affairs or pharmacovigilance units. This creates a systematic risk: borderline regulatory cases (dose threshold qualifiers, contraindication scope, population modifiers) are expected to yield disagreements between benchmark labels and regulatory-standard judgments (A4), and there is no annotation evidence to calibrate this risk magnitude. CLISTER-D17, CLISTER-D18, DEFT2020-D16, DEFT2020-D17, DEFT2020-D20, MANTRAGSC-D4 all illustrate specific cases where clinical annotation norms diverge from the regulatory equivalence interpretation the deployment requires.

**MAJOR — Regulatory-register French (EMA SmPC/PIL/QRD templates) systematically absent from text content**
Even where pharmaceutical entities appear (DEFT2021-D1, PXCORPUS-D1, ESSAI-D2), the text register is clinical narrative, spoken prescription, or clinical trial protocol. The formulaic, legally constrained register of EMA QRD-template prose ("est contre-indiqué chez les patients présentant…", "la posologie recommandée est de X mg, à administrer par voie…") does not appear in any dataset's content at scale. QUAERO-emea and MANTRAGSC-fr_emea are the only partial exceptions. The web search findings confirm: EMA QRD template v10.4 mandates that "standard statements must be used whenever they are applicable" and deviations require case-by-case EMA justification — phrasing conventions the benchmark does not systematically represent.

**MAJOR — Patent claims language underrepresented and poorly evaluated**
MANTRAGSC-fr_patents is the only French patent NER data in the benchmark. Its test set contains only 20 examples (MANTRAGSC-D12), the NER schema is identical to the EMEA schema (no patent-specific regulatory entity classes), CamemBERT-based models fail to generate non-O labels on this corpus (benchmark YAML Q73), and the patent claim syntax (Markush structures, nested qualifying clauses, "comprising" constructs) is only partially represented (MANTRAGSC-D17). The deployment's patent IP workflow component cannot be adequately evaluated using this subset alone.

**MAJOR — Heterogeneous non-pharmaceutical content dilutes domain signal in two STS datasets**
DEFT2020 mixes drug leaflet pairs with beekeeping, sports, and historical encyclopedic content (DEFT2020-D13, DEFT2020-D14, DEFT2020-D15). MORFITT includes veterinary, Canadian, Japanese, and Saudi Arabian content (MORFITT-D17, MORFITT-D18, MORFITT-D13, MORFITT-D15, MORFITT-D16). This heterogeneity means aggregate benchmark scores conflate performance on deployment-relevant content with performance on entirely off-domain content, reducing the diagnostic value of evaluation metrics.

**MINOR — Document-splitting artifacts from long EMEA text**
Sentence-splitting of long EMEA documents introduces corrupted sentence fragments in QUAERO-emea (QUAERO-D19, QUAERO-D20), potentially affecting annotation quality around document boundaries. This structural limitation applies specifically to the most deployment-relevant content in the benchmark.

**MINOR — Spoken register in PxCorpus incompatible with written regulatory text**
PxCorpus ASR artifacts, code-switching, and informal speech patterns (PXCORPUS-D10, PXCORPUS-D11, PXCORPUS-D12) represent a register entirely absent from regulatory documents. Despite having the richest pharmaceutical NER schema, this dataset's spoken-language origin creates a register transfer gap that is not evaluated by the benchmark.

---

### Content Coverage Summary

**What is well-covered:**
- French biomedical language in standard diacritics and Latin script across all datasets — no IF validity risks
- Clinical NER entity types (pathologies, symptoms, anatomical structures, procedures, events) — robust coverage across E3C, DEFT2021, CAS, QUAERO, MANTRAGSC
- Coarse pharmaceutical substance mentions (CHEM/SUBSTANCE) in EMEA drug label text — QUAERO-emea and MANTRAGSC-fr_emea
- Posology structure (drug + dose + frequency + duration + route) in spoken prescription context — PxCorpus
- STS in French biomedical text — CLISTER and DEFT2020 Task 1
- Negation and speculation scope in clinical and trial text — CAS and ESSAI
- Medical specialty classification — MORFITT and DEFT2021-cls
- ICD-10 disease classification — DiaMED
- Pharmacological knowledge domain (MCQA) — FrenchMedMCQA

**What is absent or insufficiently covered for this deployment:**
- SmPC, CTD module, and EU Risk Management Plan text — not present in any dataset
- INN as a distinct entity class separate from excipients and other CHEM entities — absent from all schemas
- ATC code annotation — absent from all schemas
- Excipient names as a distinct regulatory entity class — absent from all schemas
- EMA-templated contraindication qualifier annotation (population, dose threshold, medical condition) — absent from all schemas
- Safety warning equivalence scoring calibrated for regulatory precision — absent from both STS datasets
- Annotation by regulatory affairs specialists using EMA/ANSM standards — absent from all datasets
- Patent claim language with drug-specific regulatory entity annotation — present only at n=20 test set scale in MANTRAGSC-fr_patents
- EU geographic and institutional context (EMA/ANSM procedural vocabulary) — present only incidentally in QUAERO-D9

The coverage pattern reflects a benchmark designed for clinical NLP evaluation (hospital records, case reports, trial protocols) that partially overlaps with the pharmaceutical regulatory deployment through two EMEA-sourced NER datasets and two STS datasets with drug leaflet subsets. The overlap is real but narrow relative to the full breadth of what the deployment requires.

---

### Limitations

1. **Sample-based analysis**: Per-dataset reports are based on inspected samples, not exhaustive review of all ~50,000+ total examples. The frequency of deployment-relevant content in DEFT2020's drug leaflet subset and QUAERO-emea's full annotation coverage may be higher or lower than the samples suggest.

2. **EMEA document identity**: The specific EMEA drug products represented in QUAERO-emea (natalizumab/Tysabri, lepirudine/Refludan, ziconotide/Prialt) are a small and potentially non-representative sample of the full EMEA drug leaflet universe. Entity vocabulary breadth may be limited (QUAERO-D18).

3. **Inter-annotator agreement unverified for most datasets**: Only DiaMED has documented IAA. For NER and STS datasets where annotation quality directly determines ground-truth validity, agreement estimates are unavailable for CLISTER, QUAERO, MANTRAGSC, DEFT2021-ner, and others.

4. **Regulatory equivalence calibration — field-level gap**: The web search findings confirm that no French or English NLP benchmark with STS annotation calibrated for regulatory equivalence (dose-threshold sensitivity, population-qualifier sensitivity) currently exists. This gap cannot be resolved by adjusting DrBenchmark; it would require creating new resources.

5. **Non-French multilingual configs**: E3C and MANTRAGSC expose non-French configs (Basque, English, Spanish, Italian, German, Dutch) through the same HF repository. Evaluation pipelines that do not filter correctly could incorporate non-French data.

6. **IDMP compliance context**: The EU IDMP mandatory structured data extraction requirement (ISO 11615/11616/11240/11239/11238), which requires extracting approximately 70% of required data attributes from unstructured SmPC/eCTD text, is entirely unaddressed by DrBenchmark. This regulatory obligation is directly in scope for the deployment and has no benchmark analogue.

7. **EMA IRIS platform shift**: Since January 2025, the EMA IRIS platform is mandatory for Article 61(3) SmPC/PIL labeling notifications, potentially altering document formats encountered by the deployment system. Benchmark data predates this change and cannot validate performance on IRIS-formatted submissions.

---

### Cited Evidence

- **QUAERO-D1**: QUAERO/emea | 55 | CHEM/OBJC | "TYSABRI 300 mg solution à diluer pour perfusion natalizumab Chaque flacon de 15 ml de concentré contient 300 mg de natalizumab (20 mg/ml); phosphate de sodium, monobasique, monohydraté; chlorure de sodium; polysorbate 80 (E433) et eau pour préparation injectable." | Pharmaceutical composition list from SmPC-like regulatory text, annotating active substance and excipients | IC, OO
- **QUAERO-D2**: QUAERO/emea | 1 | CHEM | "Phosphate de sodium, monobasique, monohydraté Phosphate de sodium, dibasique, heptahydraté Chlorure de sodium Polysorbate 80 (E433) Eau pour préparation injectable." | Excipient list with E-numbers, as found in SmPC section 6.1 | IC
- **QUAERO-D3**: QUAERO/emea | 32 | PROC/CHEM | "Dans les études cliniques, la dose maximale prévue de ziconotide administré par voie intrarachidienne était de 912 µg/jour après une augmentation posologique sur 7 jours." | Posology expression with dose quantity and administration route annotated | IC, OO
- **QUAERO-D4**: QUAERO/emea | 17 | PROC | "La solution diluée doit être perfusée par voie intraveineuse pendant 1 heure à un débit d'environ 2 ml/minute." | Administration rate and IV route instruction in regulatory text | IC
- **QUAERO-D5**: QUAERO/emea | 23 | CHEM | "Prialt ne doit pas être utilisé chez l'enfant." | Pediatric contraindication in regulatory-register French | IC
- **QUAERO-D6**: QUAERO/emea | 64 | DISO/CHEM | "N'utilisez jamais TYSABRI […] Si vous êtes allergique (hydpersensible) au natalizumab ou à l'un des autres composants contenus dans TYSABRI […] Si vous avez des perturbations graves du système immunitaire (dues à une maladie, telle que leucémie ou infection à VIH…)" | Full contraindication block with population qualifiers, close to EU label format | IC, OO
- **QUAERO-D7**: QUAERO/emea | 51 | CHEM | "EMEA/H/C/122 REFLUDAN… Son principe actif est la lépirudine." | Brand name and INN both tagged CHEM, demonstrates INN extraction capability | IC, OO
- **QUAERO-D8**: QUAERO/emea | 36 | CHEM | "EMEA/H/C/122 Recommandations standard Comme la lépirudine est excrétée et métabolisée en quasi-totalité par le rein" | INN in pharmacokinetic context with EMA document header | IC
- **QUAERO-D9**: QUAERO/emea | 37 | GEOG | "La Commission européenne a délivré une autorisation de mise sur le marché valide dans toute l'Union européenne pour Tysabri à Elan Pharma International Ltd, le 27 juin 2006." | EMA marketing authorization reference in regulatory-genre French | IC, IF
- **QUAERO-D10**: QUAERO/emea | 34 | CHEM | "Contient également: mannitol, hydroxyde de sodium." | Excipients tagged identically to INNs (CHEM), preventing entity sub-class distinction | OO
- **QUAERO-D11**: QUAERO/emea | 50 | CHEM | "Refludan 50 mg en poudre pour solution injectable… le mannitol (E 421) et l'hydroxyde de sodium pour l'ajustement du pH." | Excipient same tag as INN, conflating distinct regulatory entity types | OO
- **QUAERO-D12**: QUAERO/emea | 36 | O | "EMEA/H/C/122" | EMA product number tagged O (no entity), missing key regulatory identifier class | OO, IC
- **QUAERO-D13**: QUAERO/medline | 7 | O | "Le soutien à la parentalité est-il une pierre dans le jardin des parents?" | Psychosocial topic, no regulatory pharmaceutical relevance | IO
- **QUAERO-D14**: QUAERO/medline | 16 | O | "L'apport des inventaires à la connaissance de la démographie parisienne ancienne: le règne de François Ier" | Historical-demographic abstract, outside biomedical regulatory domain | IC, IO
- **QUAERO-D15**: QUAERO/medline | 61 | O | "LÉON GRIMBERT 1860-1931." | Personal name/obituary fragment, no biomedical regulatory content | IC
- **QUAERO-D16**: QUAERO/emea | 43 | LIVB | "Par conséquent, Refludan ne doit pas être administré à la femme enceinte ou qui allaite." | Contraindication clause with pregnancy qualifier — UMLS tags entity type but not regulatory contraindication structure | OC
- **QUAERO-D17**: QUAERO/emea | 2 | DISO | "Une cirrhose du foie peut également affecter l'excrétion rénale de la lépirudine." | Pharmacokinetic safety interaction — DISO tag misses dosing-adjustment regulatory significance | OC
- **QUAERO-D18**: QUAERO/emea | 9 | CHEM | "Vous devez également prévenir votre médecin si jamais vous avez déjà pris du Refludan, une autre hirudine ou un analogue de l'hirudine." | Repeated appearance of same small set of drugs; limited entity vocabulary breadth | IC
- **QUAERO-D19**: QUAERO/emea | 4 | various | "Aucune étude clinique spécifique sur les interactions médicamenteuses n Toutefois, en raison des faibles concentrations plasmatiques du ziconotide…" | Truncated mid-sentence artifact from document splitting | IC, IF
- **QUAERO-D20**: QUAERO/emea | 63 | O | "r." | Single-character fragment, sentence-splitting artifact | IF
- **FRENCHMEDMCQA-D1**: FrenchMedMCQA | 6 | simple | "Parmi les substances suivantes, une seule ne traverse pas la barrière placentaire. Laquelle? Dicoumarine / Glucose / Héparine / Tétracycline / Amplicilline" | Pharmaceutical substance names in safety-relevant context (placental barrier) | IC
- **FRENCHMEDMCQA-D2**: FrenchMedMCQA | 13 | multiple | "Quel est (sont) le(s) diurétique(s) qui provoque(nt) une baisse du potassium sanguin? Chlortalidone / Hydrochlorothiazide / Furosémide / Spironolactone / Amiloride" | INN-style drug names as answer options in pharmacological classification | IC
- **FRENCHMEDMCQA-D3**: FrenchMedMCQA | 44 | multiple | "Peut entraîner des troubles cutanés sévères type syndrome de Lyell... l'association avec le méthotrexate est contre-indiquée" | Adverse effect and drug interaction contraindication language | IC
- **FRENCHMEDMCQA-D4**: FrenchMedMCQA | 100 | multiple | "Parmi les formes solides orales suivantes, indiquer celle(s) qui libère(nt) le principe actif de façon continue : Matrice hydrophile / Comprimé à enrobage par film insoluble..." | Pharmaceutical formulation types relevant to SmPC drug product sections | IC
- **FRENCHMEDMCQA-D5**: FrenchMedMCQA | 50 | multiple | "Parmi les verres suivants, indiquez ceux qui peuvent être utilisés comme conditionnement réutilisable des préparations pour usage parentéral : Verre de type I / Verre de type II..." | Packaging material standards relevant to regulatory CTD Module 3 | IC
- **FRENCHMEDMCQA-D6**: FrenchMedMCQA | 70 | multiple | "Les anti-vitamines K (AVK) sont formellement contre-indiquées avec : Le miconazole (DAKTARIN®) / Les beta-bloquants / Les salicylés à fortes doses..." | Formal contraindication language with brand name — matches regulatory label structure | IC
- **FRENCHMEDMCQA-D7**: FrenchMedMCQA | 105 | simple | "Une utilisation de médicament non conforme aux recommandations du résumé des caractéristiques du produit" | Explicit reference to SmPC (RCP) as regulatory concept — only occurrence across sample | IC, IO
- **FRENCHMEDMCQA-D8**: FrenchMedMCQA | 23 | multiple | "En électrophorèse capillaire haute performance, le sens de migration de l'analyse dépend : De la nature de la charge de l'analyte / Du flux d'électroendosmose..." | Pharmaceutical analytical technique question | IC
- **FRENCHMEDMCQA-D9**: FrenchMedMCQA | 31 | multiple | "La teneur en eau des matières premières est déterminée à l'aide de la méthode de Karl Fisher" | Raw material testing method present in regulatory CTD Module 3 | IC
- **FRENCHMEDMCQA-D10**: FrenchMedMCQA | 72 | multiple | "Parmi les propositions suivantes concernant la ceftriaxone (ROCEPHINE®)... C'est une céphalosporine de 3ème génération / Son importante demi-vie d'élimination est compatible avec une seule administration quotidienne" | INN + brand name + pharmacokinetic reasoning in formal French | IF
- **FRENCHMEDMCQA-D11**: FrenchMedMCQA | 1 | simple | "Au cours de la leucémie lymphoïde chronique, le myélogramme montre:" | MCQA format — tests knowledge retrieval, not NER or STS; task type mismatch | IO, OO
- **FRENCHMEDMCQA-D12**: FrenchMedMCQA | 15 | multiple | "Parmi ces effets indésirables, lesquels résultent du blocage des récepteurs cholinergiques : Sécheresse buccale / Constipation / Dysurie / Troubles de l'accommodation / Trouble de la mémoire" | Interrogative exam format vs. declarative regulatory prose — genre mismatch | IC, IO
- **FRENCHMEDMCQA-D13**: FrenchMedMCQA | 34 | multiple | "Cocher le ou les antibiotique(s) dont l'utilisation est autorisée en fin de grossesse : Ampicilline / Cotrimoxazole / Tétracyclines / Erythromycine / Péfloxacine" | Drug names as answer options — not in NER-extractable continuous text; no ATC codes | IC
- **FRENCHMEDMCQA-D14**: FrenchMedMCQA | 3 | multiple | "Parmi les propriétés suivantes du monoxyde de carbone, indiquer celle(s) qui est (sont) exacte(s)" | Classification of true/false propositions — no STS pairwise similarity signal | OO
- **FRENCHMEDMCQA-D15**: FrenchMedMCQA | 105 | simple | "Une utilisation de médicament non conforme aux recommandations du résumé des caractéristiques du produit" | SmPC reference appears only as a distractor option, not as regulatory prose text | IC, IF
- **FRENCHMEDMCQA-D16**: FrenchMedMCQA | 9 | multiple | "L'oeuf d'Enterobius vermicularis: Est incolore / Est asymétrique / Possède une coque double / Possède une coque lisse / Peut être à l'origine d'une auto-infestation" | Parasitology content with no pharmaceutical regulatory relevance | IC
- **FRENCHMEDMCQA-D17**: FrenchMedMCQA | 19 | multiple | "Parmi les phénotypes suivants, quel(s) est (sont) celui (ceux) que peuvent présenter les enfants issus d'un père AB Rh positif et d'une mère O Rh négatif?" | Blood group genetics with no regulatory relevance | IC
- **DEFT2020-D1**: DEFT2020/task_1 | 18 | moy=4.6 | "En raison de la présence de lactose, ce médicament est contre-indiqué en cas de galactosémie congénitale, de syndrome de malabsorption du glucose et du galactose ou de déficit en lactase." | Contraindication phrasing with excipient (lactose) — directly deployment-relevant regulatory text | IC
- **DEFT2020-D2**: DEFT2020/task_1 | 16 | moy=4.0 | "Ce produit peut provoquer un syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après la dernière prise de stupéfiant." | Drug safety warning with dose-time threshold — deployment-central entity type | IC
- **DEFT2020-D3**: DEFT2020/task_1 | 4 | moy=4.0 | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter pendant la durée du traitement." | Standard SmPC/leaflet precautionary instruction | IC
- **DEFT2020-D4**: DEFT2020/task_1 | 13 | moy=3.6 | "Chez les patients insuffisamment équilibrés par glimepiride arrow à la dose maximale, un traitement par l'insuline peut être associé si nécessaire." | INN (glimepiride) + posology qualifier in drug leaflet register | IC
- **DEFT2020-D5**: DEFT2020/task_2 | Ex.6 | correct_cible=2 | "en cas de traitement concomitant par un autre collyre , attendre 15 minutes entre chaque instillation" | Ophthalmic drug dosing instruction in patient leaflet register | IC
- **DEFT2020-D6**: DEFT2020/task_2 | Ex.22 | correct_cible=0 | "l' utilisation à forte dose d' huile de paraffine expose au risque de suintement anal et parfois d' irritation périanale" | Side-effect with dose qualifier from drug leaflet | IC
- **DEFT2020-D7**: DEFT2020/task_1 | 36 | moy=1.5, scores=[2.0,4.5,0.0,1.0,0.0] | "Après inspection, elles ont toutes été exclues." | High inter-annotator variance on borderline pair — illustrates scoring uncertainty | OO
- **DEFT2020-D8**: DEFT2020/task_1 | 54 | moy=5.0, scores=[5,5,5,5,5] | "Troubles de l'hémostase à type de maladie de Willebrand (se traduisant par un allongement du TCA, du temps de saignement et une diminution des taux du complexe VIIIC/VWF)." | Identical pair, unanimous perfect score — confirms annotator reliability on exact match | OC
- **DEFT2020-D9**: DEFT2020/task_1 | 65 | moy=4.3 | "- Ne pas utiliser chez les personnes présentant des difficultés de déglutition en raison du risque d'inhalation bronchique et de pneumopathie lipoïde." | Contraindication safety warning in EU leaflet formulaic register | IF
- **DEFT2020-D10**: DEFT2020/task_1 | 70 | moy=4.3 | "Prévenir les patients que la voie sublinguale constitue la seule voie efficace et bien tolérée pour l'administration de ce produit." | Administration route instruction in drug leaflet | IC
- **DEFT2020-D11**: DEFT2020/task_2 | Ex.27 | correct_cible=2 | "ce médicament est contre-indiqué dans les cas suivants" | Standard EU patient information leaflet section header | IF
- **DEFT2020-D12**: DEFT2020/task_2 | Ex.46 | correct_cible=0 | "les benzodiazépines et produits apparentés doivent être utilisés avec prudence chez le sujet âgé , en raison du risque de sédation et/ou d' effet myorelaxant qui peuvent favoriser les chutes" | Near-synonym discrimination (sédation vs. somnolence) in drug safety text | OO
- **DEFT2020-D13**: DEFT2020/task_1 | 6,7,9 | moy≈0–0.6 | "Certains apiculteurs sélectionnent leurs reines afin de favoriser au mieux la production." | Beekeeping encyclopedic content — irrelevant to regulatory deployment | IC
- **DEFT2020-D14**: DEFT2020/task_1 | 60 | moy=0.8 | "Les Canadiens de Montréal sont une franchise de hockey sur glace professionnel située à Montréal dans la province de Québec au Canada." | Sports content — zero regulatory relevance | IC
- **DEFT2020-D15**: DEFT2020/task_1 | 3 | moy=2.1 | "Boris Fiodorovitch Godounov, en russe : Бори́с Фёдорович Годуно́в (v.1551–Moscou, 13 avril 1605), gouverne la Russie à partir de 1594…" | Historical encyclopedic content — off-domain for regulatory NLP | IC
- **DEFT2020-D16**: DEFT2020/task_1 | 16 | moy=4.0 | "Ce produit peut provoquer un syndrome de sevrage opiacé s'il est administré à un toxicomane moins de 4 heures après la dernière prise de stupéfiant." | High similarity score despite addition of specific drug names in target — legally significant detail unmarked | OO
- **DEFT2020-D17**: DEFT2020/task_1 | 13 | moy=3.6 | "Chez les patients insuffisamment équilibrés par glimepiride arrow à la dose maximale, un traitement par l'insuline peut être associé si nécessaire." | "sous stricte surveillance médicale" absent in source; critical qualifier not flagged in score | OO
- **DEFT2020-D18**: DEFT2020/task_1 | 4 | moy=4.0 | "En conséquence, par mesure de précaution, il convient d'éviter d'allaiter pendant la durée du traitement." | Precautionary qualifier "par mesure de précaution" not penalized despite regulatory significance | OO
- **DEFT2020-D19**: DEFT2020/task_1 | 54 | moy=5.0 | "Troubles de l'hémostase à type de maladie de Willebrand (se traduisant par un allongement du TCA, du temps de saignement et une diminution des taux du complexe VIIIC/VWF)." | Only exact identity receives 5.0; near-synonyms not systematically distinguished from exact matches | OC
- **DEFT2020-D20**: DEFT2020/task_1 | 30 | moy=3.8 | "L'absorption de boissons alcoolisées est fortement déconseillée pendant le traitement (potentialisation réciproque)." | Mechanism qualifier "(potentialisation réciproque)" dropped in cible; not flagged as regulatory deviation by score | OC
- **DEFT2020-D21**: DEFT2020/task_1 | 26 | moy=3.4 | "Pour la comparaison entre blocs neuraxiaux et anesthésie générale, nous avons évalué la qualité des preuves comme très faible pour la mortalité…" | Cochrane review abstract register — not regulatory document prose | IO
- **DEFT2020-D22**: DEFT2020/task_2 | Ex.15 | correct_cible=2 | "lorsque le traitement ayurvédique…était comparé à la chlorpromazine chez les patients atteints de schizophrénie aiguë, il était équivalent (~10 % d'attrition, n = 36, rr de 0,67, ic entre 0,13 et 3,53)" | Research meta-analysis register with statistics — distinct from regulatory submission language | IO
- **DEFT2020-D23**: DEFT2020/task_2 | Ex.1 | correct_cible=0 | "2008 est une année du calendrier grégorien faisant partie des années 2000 et du XXIe siècle." | Trivially irrelevant distractor — reduces task discriminative validity for regulatory use | OO
- **DEFT2020-D24**: DEFT2020/task_2 | Ex.7 | correct_cible=0 | "Nintendo" | Single-word off-domain distractor — no challenge for regulatory document discrimination | OO
- **MORFITT-D3**: MORFITT | 19 | pharmacology | "Déterminer la stabilité physicochimique et microbiologique de suspensions de sulfadiazine (100 mg/mL)… Les formulations présentaient une concentration en sulfadiazine d'environ 95% au début" | Drug stability abstract with dosage and formulation content — nearest to regulatory pharmaceutical content | IC, IO
- **MORFITT-D4**: MORFITT | 33 | pharmacology, chemistry | "Les eaux thermales sont couramment utilisées comme substances actives dans les formulations cosmétiques… Une eau thermale commerciale a été utilisée comme phase aqueuse dans 5 formulations différentes" | Formulation chemistry abstract; partial overlap with excipient/galenic form vocabulary | IC, IO
- **MORFITT-D5**: MORFITT | 2 | pharmacology | "La morphine intraveineuse a atténué de façon dose-dépendante les réponses nociceptives chez les souris C57BL/6 et CD-1 (DI 50, 0,6 et 2,5 mg·kg−1)" | Drug name, dosage, and route entities present in text but not annotated at token level | IC
- **MORFITT-D6**: MORFITT | 4 | parasitology, genetics | specialities_one_hot [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0] | Multi-label assignment confirmed as genuinely multi-label | OO, OF
- **MORFITT-D7**: MORFITT | 1 | surgery | "La mise en place par cathétérisme d'une valve aortique (TAVI)… Le registre France-TAVI… va inclure plus de 3 000 cas" | Abstract-level classification only; no token-level entity annotations for NER task | IO, OO
- **MORFITT-D8**: MORFITT | 23 | microbiology | "Nous rapportons ici l'histoire d'un patient porteur d'une infection multifocale à Nocardia Farcinica associant des abcès cérébraux, une infection pulmonaire, une endocardite" | Clinical case abstract; no NER ground truth; confirms task type mismatch | IO, OO
- **MORFITT-D9**: MORFITT | 7 | psychology | "Des interventions favorables et ciblées pour les familles sont nécessaires afin d'optimiser l'ajustement parental… Le but de cette revue systématique était de déterminer l'efficacité des interventions" | Systematic review abstract; academic biomedical French; no regulatory register | IO, IC
- **MORFITT-D10**: MORFITT | 34 | surgery | "La vertébroplastie percutanée est utilisée depuis presque 30 ans, ce n'est qu'en 2007 que le premier essai randomisé a été publié" | Clinical trial review; no regulatory document genre present | IO, IC
- **MORFITT-D11**: MORFITT | 29 | veterinary | "Les indications rapportées sont le traitement de la dermatite atopique… Peu d'effets secondaires ont été observés aux doses utilisées" | Drug names and dosage references present in text but unannotated at token level | IC, OO, OC
- **MORFITT-D12**: MORFITT | 19 | pharmacology | "Un test de chromatographie liquide ultra-performante a été développé et validé pour déterminer la stabilité chimique de la sulfadiazine" | Pharmaceutical compound in text; classified only at specialty level, no entity annotation | IC, OO
- **MORFITT-D13**: MORFITT | 8 | microbiology | "La région du Nord-Ouest de l'Ontario présente un taux élevé et documenté d'infections de la peau… causées par une souche de Staphylococcus aureus méthycillinorésistante d'origine communautaire" | Canadian clinical context; jurisdictional mismatch with EMA/ANSM | IC, OC
- **MORFITT-D14**: MORFITT | 13 | genetics | "En 2007 et 2008, 4 423 adultes de Calgary ont répondu à des entrevues au téléphone fixe" | Canadian population study; non-EU context | IC, OC
- **MORFITT-D15**: MORFITT | 32 | microbiology | "Évaluer la charge des maladies d'origine alimentaire au Japon… pour l'année 2011" | Japanese epidemiological study; non-EU regulatory context | IC, OC
- **MORFITT-D16**: MORFITT | 31 | psychology | "La présente étude transversale a étudié les attitudes de médecins internes en Arabie saoudite" | Saudi Arabian medical survey; non-EU jurisdiction | IC, OC
- **MORFITT-D17**: MORFITT | 9 | veterinary | "L'otite externe est une maladie multifactorielle fréquente chez le chien… Décrire le microbiote bactérien auriculaire des chiens avec otite externe" | Canine veterinary content irrelevant to human drug labeling | IO, IC
- **MORFITT-D18**: MORFITT | 26 | veterinary, parasitology, genetics | "Prévalence et caractéristiques morphologiques et moléculaires de Sarcocystis bertrami chez les chevaux en Chine" | Equine parasitology in China; fully outside deployment scope | IO, IC
- **MORFITT-D19**: MORFITT | 10 | genetics | "Le nombre croissant de colonies d'abeilles mellifères et d'apiculteurs au Canada… lutter contre les maladies" | Beekeeping disease management; unrelated to pharmaceutical regulatory deployment | IO, IC
- **CLISTER-D1**: CLISTER | 9 | 0.0 | "Le patient fut donc traité par 1 instillation hebdomadaire intra-vésicale de 81 mg de BCG, pendant 6 semaines." | French clinical prose with dosage and treatment protocol | IC, IF
- **CLISTER-D2**: CLISTER | 41 | 2.0 | "Métoprolol 50 mg deux fois par jour;" / "Metformine 500 mg, 1 comprimé deux fois par jour" | Drug dosage expressions in clinical French notation | IC
- **CLISTER-D3**: CLISTER | 98 | 2.0 | "Acide folinique 15 mg une fois par jour" / "Aspirine 80 mg, 1 comprimé une fois par jour" | Drug-dose pairs structurally similar to posology entries | IC
- **CLISTER-D4**: CLISTER | 116 | 1.0 | "10 à 25 mg une fois par jour" / "Propranolol 40 mg, 1 comprimé deux fois par jour" | Dose-only vs. drug-plus-dose comparison | IC
- **CLISTER-D5**: CLISTER | 168 | 1.0 | "On augmente la dose de phénytoïne à 350 mg par voie intraveineuse une fois par jour." / "La dose maximale de mirtazapine devrait être de 30 mg par jour ou exceptionnellement 45 mg par jour." | Dosage comparison sentence pair | IC
- **CLISTER-D6**: CLISTER | 10 | 5.0 | "Une mastectomie était réalisée avec curage axillaire." / "Une mastectomie avec curage axillaire ont été réalisés." | Near-paraphrase correctly scored maximum | OO
- **CLISTER-D7**: CLISTER | 85 | 4.0 | "Le bilan rénal a objectivé une insuffisance rénale avec une créatininémie à 1440 μmol/l…" / "Le bilan biologique a révélé une insuffisance rénale avec une urée à 2,25g/l…" | Numerically different but semantically related values scored 4.0 | OO
- **CLISTER-D8**: CLISTER | 5 | 2.75 | "Le reste de l'examen échographique ne trouvait aucune autre anomalie." / "Le reste de l'examen somatique était sans anomalie." | Mid-range score for partial semantic overlap | OO
- **CLISTER-D9**: CLISTER | 149 | 0.5 | "Lithium 300 mg x x x x…" / "300 mg IV aux 24 h x x x…" | Near-zero score for tabular entries sharing dose notation | OO
- **CLISTER-D10**: CLISTER | 6 | 0.0 | "La patiente a eu, dans le même temps opératoire, une lithotritie balistique du calcul par voie endoscopique permettant de dénuder le DIU puis de l'extraire par une pince à corps étranger." | Clinical case narrative; not SmPC format | IO, IC
- **CLISTER-D11**: CLISTER | 222 | 0.0 | "CMV : cytomegalovirus; DCI : dénomination commune internationale; HTAP : hypertension artérielle pulmonaire; NR : non renseigné; RGO : reflux gastro-oesophagien" | Abbreviation glossary from clinical case, not regulatory document | IO
- **CLISTER-D12**: CLISTER | 188 | 4.0 | "L'AHG urinaire est à 10 mmol/l." / "L'AHG urinaire est à 20 mmol/l." | 2× quantitative difference scored 4.0 (very similar) | OO, OC
- **CLISTER-D13**: CLISTER | 90 | 3.0 | "Le taux de PSA était de 218 ng/ml (normale ≤ 4ng/ml)." / "Le dosage de PSA était de 13327 ng/ml (normal : < 4 ng/ml)." | 60× magnitude difference scored 3.0 | OO, OC
- **CLISTER-D14**: CLISTER | 123 | 3.75 | "Le taux de PSA était de 4,49 ng/ml." / "Le taux de PSA total était à 66,68 ng/ml." | 14× numeric discrepancy scored near-similar | OO, OC
- **CLISTER-D15**: CLISTER | 4 | 0.0 | "Le testicule gauche est normal." / "Le toucher rectal est normal." | Clinical examination findings; no regulatory entity type | IC, IO
- **CLISTER-D16**: CLISTER | 7 | 4.0 | "La patiente a été opérée et lors de l'exploration on découvrit qu'il s'agissait d'une tumeur de la veine cave inférieure sus-rénale." / "L'examen anatomopathologique de la pièce confirmait qu'il s'agissait d'un léiomyosarcome de la veine cave." | Surgical/pathological reporting; no regulatory relevance | IC
- **CLISTER-D17**: CLISTER | 41 | 2.0 | "Métoprolol 50 mg deux fois par jour;" / "Metformine 500 mg, 1 comprimé deux fois par jour" | Different INNs scored 2.0 due to structural template; regulatory judgment would score near 0 | OC
- **CLISTER-D18**: CLISTER | 164 | 2.0 | "Ésoméprazole 20 mg/jour Hépatique T1/2 = 1,0 – 1,5 h" / "Périndopril 2 mg/jour NR T1/2 = 17 h" | Different INNs and PK profiles scored 2.0; inconsistent with regulatory equivalence | OC
- **CLISTER-D19**: CLISTER | 8 | 1.0 | "Jour 45 - - - - - - - - - 25 μg 0,4 mg" / "Jour 53 15,13 12,0 1,58 - - - - - - 25 μg 0,4 mg" | Table row fragments, not natural-language sentences | IF, OF
- **CLISTER-D20**: CLISTER | 48 | 2.0 | "Jour 91 - - - - - - - - - Fin 0,4 mg" / "Jour 187 1,67 21,2 1,38 - - - - - - - 0,4 mg" | Numeric table rows without natural-language predication | IF, OF
- **CLISTER-D21**: CLISTER | 53 | 5.0 | "Les suites post-opératoires étaient simples." / "Les suites post-opératoires sont simples." | Tense-only variation; negligible linguistic variation | OO
- **CLISTER-D22**: CLISTER | 117 | 5.0 | "Les suites ont été simples." / "Les suites sont simples." | Auxiliary tense variation only; ceiling concentration concern | OO
- **MANTRAGSC-D1**: fr_emea | d335.u292 | CHEM(2) | "Chaque comprimé contient 500 mg de ranolazine." | Drug composition statement with INN annotated CHEM; EMEA register | IC, IO
- **MANTRAGSC-D2**: fr_emea | d16.u650 | CHEM(2), LIVB(7) | "Patients de 4 ans et plus dans l' incapacité d' avaler les capsules: la posologie recommandée d' Agenerase solution buvable est de 17 mg (1,1 ml)/ kg trois fois par jour, sans excéder la dose maximale de 2800 mg par jour" | Full posology expression with patient population qualifier; dose ceiling unannotated | IC, OO
- **MANTRAGSC-D3**: fr_emea | d73.u262 | CHEM(2) | "La dose habituelle de Cholestagel est de 3 comprimés pris deux fois par jour à l' occasion des repas ou de 6 comprimés par jour" | Standard dosage instruction language from EMEA label | IC
- **MANTRAGSC-D4**: fr_emea | d312.u295 | DISO(5) | "Vous ne devez pas prendre Pramipexole Teva si vous allaitez." | Contraindication in patient leaflet register; condition tagged DISO not as contraindication type | OO, OC
- **MANTRAGSC-D5**: fr_emea | d103.u262 | CHEM(2) | "1 ml de solution contient 40 microgrammes de travoprost et 5 mg de timolol (sous forme de maléate de timolol)" | INN and salt excipient form both tagged CHEM; no INN/excipient distinction | OO, IC
- **MANTRAGSC-D6**: fr_emea | d426.u28 | CHEM(2) | "Cette étude a comparé l' efficacité de Tyverb en association avec la capécitabine" | Brand name and INN in same sentence; both CHEM, no proprietary/INN distinction | OO
- **MANTRAGSC-D7**: fr_patents | dEP-1414451-B1.u0019 | CHEM(2) | "Forme posologique orale selon la revendication 1, dans laquelle ledit antagoniste opioïde libérable est la naltrexone et ledit opioïde libérable est la codéine, dans laquelle le rapport de la naltrexone sur la codéine libérable est de 0,005 : 1 à 0,044 : 1." | French patent claim with INNs and dosage ratio; patent claim register confirmed | IC, IO
- **MANTRAGSC-D8**: fr_patents | dEP-1663257-B1.u0006 | CHEM(2) | "L' utilisation selon la revendication 3, où le laxatif osmotique est du glycol de polyéthylène 3350." | Excipient/drug substance in patent claim; CHEM tag does not distinguish excipient from INN | IC, OO
- **MANTRAGSC-D9**: fr_emea | d61.u583 | DISO(5)/PHEN | "Des symptômes potentiellement liés à l' histamine tels que éruption cutanée étendue, gonflement du visage et/ ou des lèvres, démangeaisons, sensation de chaleur ou difficulté à respirer, ont été rapportés." | Adverse reaction listing in SmPC section 4.8 language | IC
- **MANTRAGSC-D10**: fr_emea | d157.u265 | ANAT(1) | "Les effets indésirables, en dehors des cas isolés, sont repris ci-dessous: ils sont classés par organe et par ordre de fréquence" | Standard SmPC adverse effect section header | IC
- **MANTRAGSC-D11**: HF Metadata | fr_emea splits | — | train=70, validation=10, test=20 | Test set of 20 examples is statistically insufficient for robust NER evaluation | IO
- **MANTRAGSC-D12**: HF Metadata | fr_patents splits | — | train=70, validation=10, test=20 | Same size constraint for patent genre evaluation | IO
- **MANTRAGSC-D13**: fr_emea | d103.u262 | CHEM(2) | "travoprost et 5 mg de timolol (sous forme de maléate de timolol)" | INN and salt excipient both tagged CHEM; schema cannot distinguish excipient from active substance | OO
- **MANTRAGSC-D14**: fr_emea | d349.u242 | CHEM(2) | "Renagel 800 mg sevelamer" | Brand name and INN both CHEM; no proprietary/INN label distinction critical for regulatory workflows | OO
- **MANTRAGSC-D15**: fr_medline | d7569194.u1 | DISO(5) | "Luxation antérieure ouverte post-traumatique de la hanche chez l'enfant. A propos d'un cas et revue de la littérature." | Research abstract title; clinical case register; not regulatory prose | IC, IF
- **MANTRAGSC-D16**: fr_medline | d4876372.u1 | PROC(13) | "Le problème de la régulation des naissances: aspects médico-légaux et médico-sociaux." | Non-pharmaceutical medical prose; irrelevant to regulatory NLP | IC
- **MANTRAGSC-D17**: fr_patents | dEP-2137166-B1.u0009 | CHEM(2) | "Composé selon l'une quelconque des revendications 3 à 8, dans lequel R106 est choisi parmi un hydrogène, un alkyle substitué ou insubstitué en C1-C8" | Chemical structure claim; no drug product or INN; sparse annotation on technical nomenclature | IC
- **E3C-D1**: French_clinical | 195 | 1 (CLINENTITY) | "Le bilan biologique montrait une cholestase (bilirubine totale a \`140 mmol/L, bilirubine conjugue à 80 mmol/L, phosphatases alcalines à 700 UI/L)" | Clinical lab results sentence in formal French; `cholestase` annotated as clinical entity | IC
- **E3C-D2**: French_clinical | 111 | all 0 | "Le patient a été mis sous traitement par ciclosporine avec une évolution rapide vers une leucémie aigue myéloblastique." | Drug name `ciclosporine` present but tagged O — pharmaceutical entities not annotated | OO, OC
- **E3C-D3**: French_temporal | 239 | 1 (EVENT) | "Le diagnostic retenu est celui d'une méningo-vascularite bactérienne révélant un adénome hypophysaire à prolactine." | Formal clinical diagnostic statement; shows clinical case register | IC
- **E3C-D4**: French_clinical | 64 | 1 (CLINENTITY) | "La patiente a déjà mené une première grossesse à terme il y a 9 ans, donnant naissance à un petit garçon en bonne santé." | Narrative patient history; typical clinical case format, not regulatory document | IC, IO
- **E3C-D5**: French_clinical | 385 | all 0 | "L'examen ophtalmologique retrouve une semi-mydriase aréflexique gauche avec au fond d'œil montre une occlusion de l'artère centrale de la rétine." | Clinical examination description; narrative register far from regulatory prose | IC
- **E3C-D6**: French_clinical | 54 | 1 (CLINENTITY) | "Cet aspect évoquait une tumeur solide du péritoine." | Pathology annotated as CLINENTITY; no pharmaceutical or regulatory entity layer | OO
- **E3C-D7**: French_clinical | 186 | 1 (CLINENTITY) | "La tomodensitométrie objectivait une formation kystique multicloisonnée, bien limitée de 128x115mm" | Imaging finding annotated; schema contains no drug/dosage/regulatory entity class | OO
- **E3C-D8**: Basque_clinical | 180 | all 0 | "Azken hilabeteetan Ikernek kodeina + ibuprofenoa hartu ditu, baina ez du hobekuntza handirik nabaritu." | Basque text; completely outside French regulatory deployment scope | IF, IC
- **E3C-D9**: English_clinical | 188 | 0 | "A chest radiograph showed right upper lobe consolidation with volume loss, right para-tracheal and left hilar adenopathy" | English clinical text; irrelevant to French deployment | IF
- **E3C-D10**: French_temporal | 107 | 2/7 (ACTOR) | "Il s'agit d'une patiente de 44 ans, sans antécédent médico-chirurgical, qui a présenté depuis un an des céphalées, compliquées 08 mois après de crises d'épilepsies partielles" | Narrative case presentation; temporal entity tagging on clinical events, not regulatory text | IC, OC
- **E3C-D11**: French_temporal | 304 | 1 (EVENT) | "L'examen physique a mis en évidence une volumineuse tuméfaction dorsolombaire gauche ovalaire mesurant 24cm de grand axe et 12cm de petit axe" | Physical examination clinical narrative; structurally absent from regulatory document sections | IC
- **E3C-D12**: Basque_clinical | 6 | 0 | "." | Single punctuation token; degenerate example contributing to sparse annotation | OC
- **E3C-D13**: French_clinical | 89 | all 0 | "Le reste de l'examen est inaccessible." | No entity present; contributes to negative-dominated label distribution | OC
- **PXCORPUS-D1**: PxCorpus | 5 | medical_prescription | "primperan 10 milligrammes comprimés 1 comprimé en cas de nausée toutes les 8 heures pendant 14 jours" | Full prescription structure with drug name, dose, form, frequency, indication, duration | IC, OO
- **PXCORPUS-D2**: PxCorpus | 51 | medical_prescription | "ténofovir 245 milligrammes en comprimés à prendre après les repas 1 comprimé le soir pendant 2 semaines puis stop" | INN drug name with dosage, route instruction, and duration | IC
- **PXCORPUS-D3**: PxCorpus | 97 | medical_prescription | "morphine 10 milligrammes toutes les 4 heures pendant 2 mois" | Controlled substance with frequency interval and duration | IC
- **PXCORPUS-D4**: PxCorpus | 100 | medical_prescription | "oramorph 20 milligrammes par millilitres 5 gouttes en cas de douleur ne pas dépasser 6 gouttes par jour" | Per-unit concentration and maximum-dose ceiling | IC
- **PXCORPUS-D5**: PxCorpus | 38 | none | "la posologie est à 0,0 au lieu de 0,01 25 milligrammes" | Explicit dosage discrepancy reference; relevant to compliance-flagging | IC
- **PXCORPUS-D6**: PxCorpus | 4 | replace | "attention il s'agit de 20 milligrammes et pas 10 milligrammes" | Explicit dosage correction; directly relevant to dose-discrepancy detection | IO, OO
- **PXCORPUS-D7**: PxCorpus | 8 | replace | "remplacer 1 comprimé tous les jours par 1 comprimé en cas d'anxiété" | Frequency/indication substitution captured by replace intent class | IO, OO
- **PXCORPUS-D8**: PxCorpus | 145 | medical_prescription | "lévothyroxine sodique 50 microgrammes 1 comprimé à prendre le matin à jeun pendant 6 semaines" | INN with salt suffix, administration condition, and posology | IC
- **PXCORPUS-D9**: PxCorpus | 119 | medical_prescription | "tropatepine chloridrate 1o milligrammes 1 comprimé le midi" | INN + salt form with minor transcription error ("1o" for "10"), showing ASR noise | IF, IC
- **PXCORPUS-D10**: PxCorpus | 3 | none | "/chet" | Single-token ASR artifact with no lexical content; not regulatory text | IF
- **PXCORPUS-D11**: PxCorpus | 10 | negate | "ne pas tenir compte à midi tous les jours merd/" | Profanity and truncation in spoken transcript; absent from regulatory documents | IF, IC
- **PXCORPUS-D12**: PxCorpus | 88 | none | "i'll agree come on say avec successes merde je vais roulé faut lui faire un et mettre la rame en mode français" | English/French code-switching and informal register unlike regulatory prose | IF, IC
- **PXCORPUS-D13**: PxCorpus | 207 | medical_prescription | "teralithe 250 milligrammes / le serveur de dialogue met beaucoup de temps à comprendre votre énoncé veuillez reformuler différemment" | System dialogue prompt embedded in training example; not a regulatory text pattern | IF, IC
- **PXCORPUS-D14**: PxCorpus | 18 | none | "la partie euh posologie est sur 6 ou 8 semaines là il n'est écrit que 8 semaines par contre le qsp 6 semaines a été rajouté en remarque pharmaceutique" | Closest example to regulatory commentary but spoken, informal, not document-register | IC, IO
- **PXCORPUS-D15**: PxCorpus | 103 | medical_prescription | "trémétadisine trémétasidine à 20 milligrammes à 3 comprimés par jour pendant 3 semaines" | Near-identical drug name variants without ATC linkage or excipient field | OO
- **PXCORPUS-D16**: PxCorpus | 22 | medical_prescription | "sirop de potassium richard 1 cuillerée à soupe matin et soir pendant 1 mois" | "potassium richard" tagged as modifier, not recognized INN or excipient class | OO
- **PXCORPUS-D17**: PxCorpus | 4 | replace | "attention il s'agit de 20 milligrammes et pas 10 milligrammes" | One of only ~3 replace-class examples in 500-example buffer; class severely underrepresented | OC, OO
- **PXCORPUS-D18**: PxCorpus | 12 | replace | "non prendre 150 milligrammes par jour" | Replace class example; rarity limits model reliability for correction-detection task | OC, OO
- **DIAMED-D1**: DiaMED | 1 | A00-B99 | "Le test rapide VIH était positif, confirmé par la sérologie VIH avec un taux de CD4 à 27/mm3." | Confirms dense biomedical vocabulary and clinical register; HIV serology result | IC, IF
- **DIAMED-D2**: DiaMED | 2 | C00-D49 | "4 cures de chimiothérapie palliative selon le protocole LV5 FU2 (5-Fluoro-uracile associé à l'acide folinique)" | Chemotherapy protocol mention with drug name — pharmaceutical entity in clinical narrative | IC
- **DIAMED-D3**: DiaMED | 3 | D50-D89 | "une antibioprophylaxie (association Amoxicilline et acide clavulanique)" | Drug combination mention; keywords include 'Maroc' — non-EU regulatory geographic context | IC, IF
- **DIAMED-D6**: DiaMED | 6 | G00-G99 | "Monsieur Y. O. âgé de 19 ans a été hospitalisé le 03 février 2012 pour une paraplégie évoluant depuis un mois." | Classic clinical case narrative register; entirely distinct from regulatory document genre | IO, IC
- **DIAMED-D8**: DiaMED | 8 | H60-H95 | "une antibiothérapie injectable empirique instaurée à base de céphalosporines de troisième génération et de ciprofloxacine" | Drug class and named drug in clinical treatment narrative; not in EMA SmPC format | IC, IF
- **DIAMED-D9**: DiaMED | 9 | I00-I99 | "Communication interventriculaire ischémique: à propos d'un cas observé dans le service de cardiologie du CHU-Yalgado Ouedraogo de Ouagadougou (Burkina Faso)" | Sub-Saharan African hospital setting; non-EU regulatory context | IC, IF
- **DIAMED-D11**: DiaMED | 11 | K00-K95 | "suture de la rupture gastrique par un surjet au polyglactin 910 (vicryl*2/0)" | Trade name usage in surgical narrative; clinical protocol differs from regulatory document conventions | IC, IF
- **DIAMED-D12**: DiaMED | 12 | L00-L99 | "200mg de Phénobarbital à prendre en une prise vespérale... Halopéridol 20 mg et Chlorpromazine 400 mg en deux prises par jour" | Named drugs with dosages — closest to deployment entity types, but unannotated and embedded in clinical narrative | IC, OO
- **DIAMED-D13**: DiaMED | 13 | M00-M99 | "Il s'agit d'un adolescent âgé de 16 ans, sportif (tennis) qui se plaignait depuis plusieurs mois de douleurs mécaniques du coude droit." | Clinical case narrative about orthopedic condition; no pharmaceutical content | IO
- **DEFT2021-D1**: DEFT2021/cls | 3 | [6,14,13,19,4] | "clarithromycine 500 mg deux fois par jour pendant 10 jours... sulfate de quinidine 200 mg trois fois par jour" | Drug names with explicit dosage and frequency — relevant to deployment NER targets | IC
- **DEFT2021-D2**: DEFT2021/cls | 8 | [20,17,22,13,0,4,19] | "rituximab 375 mg/m2 par voie IV, à raison d'une fois par semaine pendant quatre semaines... mofétil mycophénolate (MMF) 500 mg par voie orale, deux fois par jour" | Dense posology expressions with route and frequency | IC
- **DEFT2021-D3**: DEFT2021/ner | 80 | SUBSTANCE/DURATION | "rifampicine – isoniazide – pyrazinamide pendant 6 mois" | Drug names tagged as SUBSTANCE with duration — partial INN coverage | OO
- **DEFT2021-D4**: DEFT2021/ner | 55 | SUBSTANCE/DOSAGE/MODE | "Hydrocortisone 300 mg IV... Hydroxyzine 25 mg par voie orale toutes les 6 heures" | Drug + dose + route + frequency tagged; matches deployment posology targets | OO, IC
- **DEFT2021-D5**: DEFT2021/ner | 7 | SUBSTANCE/DURATION | "cotrimoxazole pour 10 jours" | Drug and duration extraction; treatment annotation | OO
- **DEFT2021-D6**: DEFT2021/cls | 3 | [6,14,13,19,4] | specialities include pharmacology and cardiovascular; text covers CYP3A4, P-gp, IKr/IKs drug interactions | Pharmacology-relevant classification with named drugs | IO
- **DEFT2021-D7**: DEFT2021/cls | 5 | [12,3,20,4,7,5] | "buprénorphine (Subutex)... lévopromazine (Tercian)... paroxétine (Divarius)... prise d'une quantité importante de Codoliprane" | Toxicology specialty; drug names and overdose context | IO
- **DEFT2021-D8**: DEFT2021/cls | 1 | [18,4] | "Femme de 73 ans n'ayant eu qu'un seul enfant par césarienne, mais présentant depuis plusieurs années un prolapsus de stade III" | Patient narrative format — clinical case, not regulatory document | IO, IC
- **DEFT2021-D9**: DEFT2021/cls | 2 | [4,9,18] | "Mme M.J., âgée de 66 ans consultait pour des lombalgies droites lancinantes" | Clinical consultation narrative; no regulatory register | IO, IC
- **DEFT2021-D10**: DEFT2021/cls | 6 | [12,17,4] | "Monsieur B..., âgé de 36 ans, aux antécédents de gastrite" | Clinical case patient history, entirely clinical genre | IO, IC
- **DEFT2021-D11**: DEFT2021/ner | 28 | DISO | "carcinome vésical droit... carcinome urothélial multiple" | Pathology/disease entity annotation — clinical schema dominant | OO
- **DEFT2021-D12**: DEFT2021/ner | 4 | DISO/PROC | "kyste épidermoïde isolé... analyse anatomo-pathologique" | Clinical entity types; no regulatory entity classes | OO
- **DEFT2021-D13**: DEFT2021/ner | 55 | SUBSTANCE | "Hydrocortisone... Hydroxyzine" tagged as SUBSTANCE without INN/ATC specificity | Drug names captured but undifferentiated from other substances; no ATC linkage | OO, IC
- **DEFT2021-D14**: DEFT2021/cls | 3 | [6,14,13,19,4] | Drug interaction case labeled with MeSH pharmacology axes; no regulatory equivalence structure | Annotation captures clinical specialty, not regulatory compliance | OC
- **DEFT2021-D15**: DEFT2021/ner | 3 | SUBSTANCE/PROC | "diphenhydramine et de méthylprednisolone... prémédication" | Clinical semantic annotation; no regulatory labeling hierarchy | OC
- **DEFT2021-D16**: DEFT2021/cls | schema | — | features: id, document_id, text, specialities, specialities_one_hot | No STS pair structure; classification only; cannot evaluate regulatory equivalence scoring | OO, OF
- **CAS-D2**: CAS/cls | cls/train/467 | neutral | "après mise en condition en unité de soins intensifs et administration d' une ampoule de digoxine en intraveineuse , un bilan radiologique a été réalisé ." | Contains drug name (digoxine) and route of administration in clinical narrative | IC
- **CAS-D3**: CAS/cls | cls/train/49 | speculation | "une origine médicamenteuse étant envisagée ( avec éventuellement une imputabilité du paracétamol ) , il était décidé d' arrêter les différents traitements et de remplacer les lavements de pentasa ® par du proctocort ® ( hydrocortisone acétate 90 mg : 1 lavement tous les soirs ) ." | Multiple drug names, dosage and frequency — highest pharmaceutical entity density in sample, but in clinical not regulatory register | IC
- **CAS-D4**: CAS/cls | cls/train/605 | speculation | "puisque le traitement par la warfarine semble plus problématique , un naco est envisagé ." | Drug class mention (NOAC) under speculation marker; shows hedge around drug choice | IC, OO
- **CAS-D5**: CAS/ner_neg | ner_neg/train/75 | IOB2 negation | tokens: ['sans', 'antécédent', 'familial', 'de', 'maladie', 'colique']; ner_tags: [0, 1, 2, 2, 2, 2] | Negation scope spanning clinical history phrase; shows annotation granularity | OO
- **CAS-D6**: CAS/ner_neg | ner_neg/train/637 | IOB2 negation | "ne montrait aucune lésion focale" with negation tags on "montrait" and "lésion focale" | Dual-cue negation encoded; relevant to safety-warning negation detection | OO
- **CAS-D8**: CAS/cls | cls/train/682 | negation_speculation | "Il s'agit d'une patiente âgée de 63 ans , sans antécédents particuliers , ménopausée depuis 14 ans , célibataire , sans enfants , qui a consulté pour algies pelviennes chroniques..." | Prototypical clinical case narrative register, fundamentally different from regulatory document prose | IO, IC
- **CAS-D9**: CAS/cls | cls/train/128 | neutral | "depuis hier soir , je suis essouflé , j' ai des frissons , j' ai mal à la poitrine , là en bas à gauche , surtout quand j' inspire à fond ." | Patient first-person voice — genre entirely absent from EU regulatory submissions | IO, IC
- **CAS-D10**: CAS/ner_neg | ner_neg/train/467 | all-O | "administration d' une ampoule de digoxine en intraveineuse" — all ner_tags = 0 | Drug name "digoxine" not annotated as any entity; confirms no pharmaceutical entity schema | OO, IC
- **CAS-D11**: CAS/ner_spec | ner_spec/train/84 | IOB2 speculation | tokens: ['le', 'diagnostic', "d'", 'ulcère', 'solitaire', 'du', 'rectum', 'était', 'évoqué']; ner_tags: [1, 2, 2, 2, 2, 2, 2, 2, 0] | Speculation span over diagnostic phrase — schema captures linguistic modality, not entity type | OO
- **CAS-D12**: CAS/ner_neg | ner_neg/train/305 | IOB2 negation | tokens: ['les', 'ovaires', 'ne', 'montraient', 'pas', "d'", 'anomalie']; ner_tags: [0, 0, 0, 1, 0, 2, 2] | Negation cue "ne…pas" tagged with B on verb not on "ne"; annotation boundary decisions undocumented | OC
- **CAS-D13**: CAS/cls | cls/train/176 | speculation | "cholstat ® 0.1 ." | Single drug name + dosage fragment labeled speculation with no visible hedge marker; suggests noisy annotation boundary | OO, OC
- **ESSAI-D1**: ESSAI/pos | 226 | neutral | "avec la combinaison gemcitabine + abraxane, chez des patients avec un cancer du pancréas" | Drug INN + brand name co-occurrence in trial text | IC
- **ESSAI-D2**: ESSAI/cls | 1 | negation_speculation | "chimiothérapie à hautes doses avec une combinaison de Busulfan et de Melphalan (BU-MEL) permettra d'obtenir une survie sans événement à 3 ans supérieure à une consolidation par une association de Carboplatine VP16 et Melphalan" | Multi-drug combination with posology context | IC
- **ESSAI-D3**: ESSAI/ner_neg | 2 | O | "Le MEDI9197 est injecté en intra-tumoral tous les 28j (4 semaines)" | Dosing frequency and administration route in trial protocol | IC
- **ESSAI-D4**: ESSAI/ner_spec | 3 | O | "Lorsque la chimiothérapie à base de platine est associée au Caelyx, les perfusions ont lieu tous les quinze jours pendant 6 mois (cycles de 28 jours) puis une maintenance est ensuite instaurée avec le Bevacizumab et l'Atezolizumab ou placebo perfusés toutes les 3 semaines" | Complex multi-drug dosing schedule | IC
- **ESSAI-D5**: ESSAI/cls | 2 | negation | "se sont montrés tout aussi efficace et ne présentent pas plus d'effets secondaires dans différents essais cliniques sur plusieurs milliers de patientes" | Negation of adverse effects — safety-relevant | OO
- **ESSAI-D6**: ESSAI/cls | 4 | speculation | "Dans les formes inopérables et/ou métastatiques, le seul traitement approuvé depuis 2008 est le sorafenib" | Approval claim with temporal boundary | OO
- **ESSAI-D7**: ESSAI/cls | 21 | negation_speculation | "Absence d'insuffisance hépatique ou rénale — Chimiothérapie pré-opératoire de 2ème ligne à base de platine (soit carboplatine-paclitaxel soit carboplatine-caelix)" | Exclusion criteria with organ-function contraindication framing | IC
- **ESSAI-D8**: ESSAI/cls | 9 | negation_speculation | "Ne pas prendre part à un autre projet de recherche sans l'accord de votre médecin, ceci pour vous protéger de tout accident possible pouvant résulter par exemple d'incompatibilités possibles ou d'autres dangers" | Negation in patient safety instruction context | IC
- **ESSAI-D10**: ESSAI/cls | 3 | neutral | "Essai clinique d'immunothérapie évaluant l'association du galunisertib (un facteur de croissance transformant β), avec l'anticorps anti-PD-L1 durvalumab (MEDI4736), dans le cancer du pancréas métastatique" | Trial objective framing — not SmPC regulatory prose | IO
- **ESSAI-D11**: ESSAI/cls | 20 | speculation | "Dans la recherche proposée, nous allons évaluer si l'utilisation de l'oxygène à haut débit humidifié chez les patients immunodéprimés avec un problème respiratoire nécessitant de l'oxygène admis en réanimation est supérieure à la prise en charge habituelle" | Research hypothesis language — absent from SmPC register | IO
- **ESSAI-D12**: ESSAI/ner_spec | 10 | speculation span | "le traitement par un inhibiteur de PARP, le talazoparib, peut être plus efficace et mieux toléré de la chimiothérapie de référence" | Speculation NER marks hedging scope, not INN entity | OO
- **ESSAI-D13**: ESSAI/ner_neg | 11 | negation span | "en l'absence d'atteinte ganglionnaire chez les femmes ménopausées" | Negation NER marks clinical condition under negation, not regulatory entity | OO
- **ESSAI-D14**: ESSAI/ner_neg | 9 | O | "L'acétate d'abiratérone ou l'enzalutamide sont des traitements assez récents et ainsi appelés «hormonothérapies de nouvelle génération»" | Informal INN usage without ATC code mapping | IC
- **ESSAI-D15**: ESSAI/ner_spec | 12 | O | "Les patients seront traités par nivolumab IV en combinaison avec de l'ipilimumab en IT ou en IV" | Route abbreviations in trial shorthand vs. SmPC-standard format | IC
- **ESSAI-D16**: ESSAI/cls | 28 | speculation | "Les agents alkylants sont des chimiothérapies exposant à un risque de troubles de la fertilité avec insuffisance ovarienne précoce chez les femmes" | Population/adverse-event qualifier captured only as speculation, not regulatory entity | OO, OC
- **ESSAI-D17**: ESSAI/cls | 8 | speculation | "Cette étude est destinée à évaluer le nouveau médicament «cobimetinib» chez l'enfant et adolescent porteur d'une tumeur solide en rechute et/ou réfractaire au précédent traitement" | Pediatric population qualifier subsumed in speculation label | OO
- **ESSAI-D18**: ESSAI/YAML | Q43 | — | "ESSAI contains 7,247 clinical trial protocols annotated in 41 POS tags using TreeTagger" | Machine-generated POS; no human regulatory expert annotation documented | OC
- **ESSAI-D19**: ESSAI/cls | 23 | neutral | "Les gliomes de bas grade (grade I ou II) sont les tumeurs cérébrales les plus fréquemment observées chez les enfants, adolescents et jeunes adultes" | Oncology-only scope; non-oncology therapeutic areas absent | IC
- **ESSAI-D20**: ESSAI/ner_spec | 13 | O | "Les effets secondaires attendus sont mineurs de type ballonnement abdominal, diarrhées, spames digestifs le plus souvent et rarement des cailloux dans les voies biliaires" | Adverse effect listing in oncology trial — not SmPC adverse effects section | IC


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
  "region": "EU Pharmaceutical Regulatory NLP — French",
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
