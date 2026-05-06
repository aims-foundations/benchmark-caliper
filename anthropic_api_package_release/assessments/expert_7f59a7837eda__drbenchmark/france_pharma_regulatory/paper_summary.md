```markdown
# Validity Extraction: DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Domain
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: DrBenchmark: A Large Language Understanding Benchmark for the Biomedical French Domain
- **Authors**: Yanis Labrak, Adrien Bazoge, Oumaima El Khettari, Mickael Rouvier, Pacôme Constant dit Beaufils, Natalia Grabar, Béatrice Daille, Solen Quiniou, Emmanuel Morin, Pierre-Antoine Gourraud and Richard Dufour
- **Venue/Year**: Not explicitly stated in registry (inferred from content as ~2023–2024)
- **Total Pages**: 14 (based on registry page range 1–14)
- **Quotes Extracted**: 108

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

---

### 1. Task Taxonomy / Test Case Categories

DrBenchmark is introduced as "the first large language understanding benchmark tailored for the French biomedical domain" [Q83], comprising 20 diverse downstream tasks [Q84] spanning NER, POS tagging, multi-class and multi-label classification, multiple-choice question-answering (MCQA), and semantic textual similarity (STS) [Q1, Q4, Q18]. The benchmark explicitly includes both foundational tasks (POS, NER) and more challenging ones such as MCQA and multi-label classification [Q20], with at least one dataset — DiaMed — created specifically for DrBenchmark [Q45]. Individual datasets contribute multiple sub-tasks: for instance, DEFT-2020 provides both a sentence similarity task scored 0–5 and a most-similar-sentence identification task [Q21, Q22, Q23], while FrenchMedMCQA covers identifying correct answers among five options and counting the number of correct answers [Q39], and PxCorpus contributes both intent classification and NER over drug prescription transcripts [Q44].

From a deployment validity standpoint (IO dimension, HIGH priority), the task inventory is clinically and scientifically oriented but does not include tasks drawn from EU regulatory document genres. The benchmark's NER and STS tasks derive from clinical cases, biomedical abstracts, clinical trial protocols, and speech transcriptions [Q19], with no mention of SmPCs, patient information leaflets, EU Risk Management Plans, CTD modules, or patent claims as primary text types — even though Mantra-GSC does include a patent subset [Q40], which represents the only partial overlap with the patent genre relevant to regulatory deployment. The broader formulaic, legally constrained language of EMA/ANSM regulatory submissions is therefore structurally absent from the task inventory, constituting a significant input ontology gap for the target deployment. Aggregated task-category results are also reported across POS, NER, MCQA, MCC, MLC, and STS groupings [Q81], which reinforces that the benchmark's organizational logic reflects clinical and research NLP conventions rather than regulatory workflow categories.

---

### 2. Data Sources and Collection

DrBenchmark draws from a diverse range of source types including scientific literature, clinical trials, clinical cases, speech transcriptions, and other genres [Q19]. Specific corpora include: DEFT-2021 (275 clinical cases) [Q24], E3C (multilingual clinical cases, French subset retained) [Q29], QUAERO (drug leaflets and biomedical titles from EMEA and MEDLINE, totaling 103,056 words) [Q33, Q34], MorFITT (3,624 biomedical abstracts from PMC Open Access) [Q38], Mantra-GSC (biomedical abstracts/titles, drug labels, and patents from three sources) [Q40], ESSAI (7,247 clinical trial protocols) [Q43], and DiaMed (739 clinical cases from The Pan African Medical Journal) [Q45]. For framing, the paper notes that existing biomedical benchmarks predominantly serve English (BLURB, BLUE) or Chinese (CBLUE) [Q12], and that no large French biomedical benchmark previously existed [Q16].

From an IC validity perspective, the most deployment-relevant source is QUAERO, which explicitly includes EMEA drug leaflet text [Q34] — one of the document types in the target deployment. Mantra-GSC's patent and EMEA subsets [Q40] also offer partial genre overlap. However, the majority of data originates from clinical cases and research abstracts, which differ substantially in register, entity density, and terminological conventions from formal EU regulatory submissions. The benchmark explicitly does not redistribute datasets and preserves original licensing [Q96], meaning users must source corpora independently.

---

### 3. Data Format and Preprocessing

The benchmark operates exclusively on French text, with multilingual source datasets filtered to retain only French subsets [Q31]. Several datasets lack predefined train/validation/test splits and were randomly divided using a 70/10/20 scheme [Q32, Q42, Q40]. The entire benchmark is delivered via a HuggingFace Datasets-based toolkit with normalized data loaders, predefined splits, and pre-training and evaluation scripts [Q48]. Tokenization is a studied variable: the paper analyzes average sub-token counts per word across models [Q89, Q90], and documents that nested entity annotations in QUAERO were simplified by retaining only higher-granularity annotations, resulting in annotation loss of 6.06% (EMEA) and 8.90% (MEDLINE); long EMEA documents were also sentence-split to accommodate model input length constraints [Q37]. Training-data volume experiments used 25%, 50%, 75%, and 100% subsets of training data [Q68], and QUAERO entity annotations totaled 26,409 mapped to 5,797 unique UMLS concepts [Q36].

For the deployment context (IF dimension, LOWER priority), there is no modality mismatch — the benchmark and deployment both operate on French text. The HuggingFace-based toolkit [Q48] ensures straightforward adoption, and the sentence-splitting preprocessing applied to EMEA documents [Q37] is directly relevant to the long-form regulatory documents (SmPCs, CTD modules) typical of the deployment environment.

---

### 4. Label Categories and Output Types

The benchmark's label ontology spans multiple task types with rich, domain-specific schemas. For POS tagging, CAS uses 31 classes [Q42] with tags such as NOM, VER:pres, ADJ, ADV [Q101], while ESSAI uses 41 tags [Q43] including an extended set [Q102]. NER labels vary by corpus: QUAERO uses 10 UMLS Semantic Group categories (GEOG, PHEN, DISO, ANAT, OBJC, PHYS, PROC, DEVI, CHEM, LIVB) [Q35, Q103]; E3C annotates clinical entities (CLINENTITY) and temporal/factual entities (EVENT, ACTOR, BODYPART, TIMEX3, RML) [Q30, Q104]; Mantra-GSC uses 11 classes for Medline and 10 for EMEA/Patents [Q106]; and PxCorpus NER covers 38 classes including DRUG, DOSE, and MODE [Q44, Q108]. Multi-label classification labels include 23 MeSH Chapter C axes for DEFT-2021 [Q27, Q107], 12 medical specialties for MorFITT [Q38, Q105], and 22 ICD-10 chapters for DiaMed [Q45]. STS tasks use continuous 0–5 similarity scores [Q41].

From an OO and OC validity perspective (both HIGH priority), the NER entity schemas are calibrated for clinical and research biomedical entities — pathologies, symptoms, procedures, anatomical structures — rather than the regulatory entity types central to the deployment (INNs, ATC codes, excipient names, EMA-templated posology expressions, contraindication qualifiers). While SUBSTANCE, DOSAGE, MODE, and TREATMENT appear in PxCorpus's schema [Q108] and CHEM appears across multiple corpora [Q103, Q106], these do not map cleanly onto INN/ATC nomenclature or EMA-standard contraindication phrasing. The STS scoring rubric (0–5 general semantic similarity) [Q41] is not designed to detect the legally significant micro-differences — such as dose threshold shifts or contraindicated-population qualifiers — that define regulatory equivalence in the deployment, representing a fundamental output ontology mismatch.

---

### 5. Annotation Process

Annotation coverage in the registry is limited to three datasets. DEFT-2021 was manually annotated for multi-label classification and NER [Q25]. CLISTER's 1,000 sentence pairs were manually annotated by multiple annotators who assigned similarity scores from 0 to 5, with scores averaged to produce a floating-point reference value [Q41]. DiaMed, the only dataset created specifically for DrBenchmark, was manually annotated by several annotators including one medical expert, using 22 ICD-10 chapters; inter-annotator agreement was computed across two sessions of 15 clinical cases each using Cohen's Kappa and Gwet's AC1 [Q45, Q46].

NOT DOCUMENTED for most corpora: the paper does not provide annotator demographics, professional backgrounds (clinical, research, NLP), or annotation guidelines for the majority of datasets. This absence is validity-relevant for the OC dimension (HIGH priority): the deployment requires ground-truth judgments aligned with EMA/ANSM regulatory standards, and with annotator profiles undocumented across most of the benchmark, it is impossible to assess whether annotation norms reflect regulatory affairs expertise. The one confirmed medical expert contributor (DiaMed) [Q45] pertains to ICD-10 classification rather than regulatory entity or STS labeling. Systematic disagreement on borderline regulatory cases — anticipated in the elicitation — cannot be directly assessed from the available annotation documentation.

---

### 6. Evaluation Metrics and Output Modality

Eight state-of-the-art pre-trained masked language models (MLMs) were evaluated [Q2, Q6], all BERT-like architectures fine-tuned under a strict shared-hyperparameter protocol with results averaged over four runs and statistical significance computed via Student's t-test [Q51]. For sequence labeling tasks (POS, NER), SeqEval with IOB2 format is used, with models predicting only the first-token label per word to ensure tokenizer-agnostic evaluation [Q52, Q53]. STS tasks are evaluated with Spearman correlation and the EDRM (mean relative solution distance accuracy) metric from DEFT-2020 [Q54]. Classification tasks use majority-class baselines for comparison [Q56]. Domain- and language-specialized models (DrBERT-FS, DrBERT-CP, CamemBERT-bio) achieve top performance on 75% of tasks [Q62], with DrBERT-FS leading on 8 tasks and DrBERT-CP on 5 [Q61]. Low-data robustness experiments varied training set size across 25/50/75/100% with four runs per configuration [Q68, Q69, Q70], revealing differential model behavior under data scarcity [Q71, Q72, Q74]. Tokenization analysis showed DrBERT-CP outperforms FlauBERT on 16 of 20 tasks despite higher average segmentation (1.90 vs. 1.43) [Q78]. Hyperparameters are fully documented and best models are selected on validation metrics to mitigate overfitting [Q99, Q100].

For the deployment context, the STS metrics (Spearman correlation and EDRM) measure general semantic proximity, not regulatory equivalence. The EDRM metric is specific to the DEFT-2020 task design [Q54] and has no documented calibration for the deployment's requirement to treat small lexical differences in dose thresholds or contraindicated-population qualifiers as critical mismatches. The aggregate task-category analysis [Q82] does reveal that even the leading model (DrBERT-FS) does not excel on MLC or STS tasks, which is directly relevant to the deployment's reliance on STS for compliance flagging.

---

### 7. Stated Limitations

The authors acknowledge numerous scope and performance limitations. The most structurally significant for the deployment context is that French biomedical NLP resources are sparse [Q5], and that no large French biomedical benchmark existed prior to DrBenchmark [Q16] — establishing the benchmark's novelty but also its pioneer status in an underserved space. General benchmarks are noted as potentially inadequate for specialized domains [Q10], and biomedical benchmarks remain scarce and English/Chinese-centric [Q9, Q11]. The only prior multilingual option (BigBIO) covers just 4 French corpora and was designed for generative zero-shot scenarios [Q16].

On model performance, no single model excels across all tasks [Q3, Q57], generalist models underperform specialized ones on complex biomedical tasks [Q63, Q85] but remain competitive on several [Q64], and XLM-RoBERTa (the cross-lingual model) reaches only second-best on some tasks [Q59]. French biomedical models (DrBERT-FS, DrBERT-CP, CamemBERT-bio) show superior performance across many tasks [Q60], though even specialized models show poor performance on some biomedical tasks [Q86], and MLMs may not be optimal for QA or multi-label classification [Q87]. The relationship between pre-training data size and performance requires further investigation [Q65, Q66, Q91], and CamemBERT-based models struggle in low-resource corpora such as MantraGSC Patents [Q73].

Methodologically, the QUAERO simplification of nested entity annotations results in measurable annotation loss (up to 8.90%) [Q37], and tokenization effects appear less impactful than previously assumed [Q79, Q80], though this finding warrants further analysis [Q88]. The study consumed approximately 2,500 GPU hours and an estimated 647,500 Wh / 36.9 kgCO2eq [Q93, Q94], raising reproducibility concerns for resource-constrained users [Q92]. A broader limitation not explicitly stated by the authors but inferable from the registry: the benchmark does not address the STS scoring calibration needed for regulatory equivalence judgments, nor does it cover the full range of EU regulatory document genres central to the deployment.

---

### 8. Authors and Affiliations

The paper lists eleven authors [Q7] drawn from a cluster of French academic and medical institutions [Q8]: LIA (Avignon Université), Zenidoc, Nantes Université, CHU Nantes / Clinique des données / INSERM CIC 1413, École Centrale Nantes, CNRS LS2N (UMR 6004), Service de Neuroradiologie (l'institut du thorax), and UMR 8163–STL CNRS / Université de Lille. Computational resources were provided by GENCI-IDRIS and CCIPL [Q97], and funding came from ANR MALADES, ANR AIBy4, and Zenidoc [Q98]. The code is released under the MIT License [Q95], and original dataset licenses are preserved without redistribution [Q96].

The affiliations are entirely French, spanning NLP research, clinical medicine (CHU Nantes, neuroradiology), and industry (Zenidoc). This origin confirms strong alignment with French-language biomedical NLP, but the team composition does not include regulatory affairs specialists, pharmacologists, or EMA/ANSM legal experts — the precise professional roles constituting the deployment's target user population. This institutional profile is consistent with a benchmark designed for clinical and research NLP rather than pharmaceutical regulatory compliance, reinforcing the OC concern that ground-truth annotation norms may diverge from regulatory standards on borderline cases.
```

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | task_taxonomy | "It encompasses 20 diversified tasks, including named-entity recognition, part-of-speech tagging, question-answering, semantic textual similarity, and classification." |
| Q2 | 1 | evaluation_metrics | "We evaluate 8 state-of-the-art pre-trained masked language models (MLMs) on general and biomedical-specific data, as well as English specific MLMs to assess their cross-lingual capabilities." |
| Q3 | 1 | stated_limitations | "Our experiments reveal that no single model excels across all tasks, while generalist models are sometimes still competitive." |
| Q4 | 1 | task_taxonomy | "These tasks encompass part-of-speech (POS) tagging, named-entity recognition (NER), classification, question-answering (QA), and semantic textual similarity (STS)." |
| Q5 | 1 | stated_limitations | "Although the French language is generally considered as well-endowed, it is notably lacking in evaluation resources within the biomedical field." |
| Q6 | 1 | evaluation_metrics | "We also perform a quantitative study of 8 pre-trained state-of-the-art masked language models" |
| Q7 | 1 | authors_affiliations | "Yanis Labrak, Adrien Bazoge, Oumaima El Khettari, Mickael Rouvier, Pacôme Constant dit Beaufils, Natalia Grabar, Béatrice Daille, Solen Quiniou, Emmanuel Morin, Pierre-Antoine Gourraud and Richard Dufour" |
| Q8 | 1 | authors_affiliations | "LIA, Avignon Université, Zenidoc, Nantes Université, CHU Nantes, Clinique des données, INSERM, CIC 1413, École Centrale Nantes, CNRS, LS2N, UMR 6004, Service de Neuroradiologie diagnostique et interventionnelle, l'institut du thorax, UMR 8163 – STL CNRS, Université de Lille" |
| Q9 | 1 | stated_limitations | "The biomedical field remains an area with relatively few proposed benchmarks, mainly for English and Chinese, facilitating the availability of many biomedical models in these two languages." |
| Q10 | 2 | stated_limitations | "In the case of specialized domains, general benchmarks may not adequately evaluate the performance of in-domain models." |
| Q11 | 2 | stated_limitations | "Specifically, within the biomedical domain, only few benchmarks have been proposed, and they primarily focus on few languages." |
| Q12 | 2 | data_sources | "For instance, platforms like BLURB (Gu et al., 2021) and BLUE (Peng et al., 2019) predominantly offer benchmarks for English, while CBLUE (Zhang et al., 2022a) caters to the Chinese language." |
| Q13 | 2 | task_taxonomy | "BLURB integrates 13 tasks, including NER, information and relation extraction, sentence similarity, text classification, and QA." |
| Q14 | 2 | task_taxonomy | "BLUE encompasses 10 tasks, such as NER, sentence similarity, relation extraction, text classification, and inference." |
| Q15 | 2 | task_taxonomy | "CBLUE covers 8 tasks, including NER, information extraction, text and intent classification, sentence similarity, and query relevance." |
| Q16 | 2 | stated_limitations | "To our knowledge, aside the multilingual benchmark BigBIO (Fries et al., 2022) which includes only 4 corpora for French and is initially intended for generative text completion under zero-shot scenario, no large benchmark specialized in the French biomedical field exists." |
| Q17 | 2 | task_taxonomy | "Our proposed benchmark comprises 20 French biomedical language understanding tasks, one of which is specifically created for this benchmark." |
| Q18 | 2 | task_taxonomy | "A variety of tasks with different requirements and objectives: Part-of-Speech (POS) tagging, Multi-class, Multi-label and Intent classification, Named-Entity Recognition (NER), Multiple-Choice Question-Answering (MCQA), and Semantic Textual Similarity (STS)." |
| Q19 | 2 | data_sources | "A diverse range of data origins: Scientific literature, clinical trials, clinical cases, speech transcriptions, and more as described in Table 2." |
| Q20 | 2 | task_taxonomy | "Please note that within DrBenchmark, we include classical tasks like NER and POS tagging, as well as more specific and challenging tasks like MCQA and multi-label classification." |
| Q21 | 3 | task_taxonomy | "DEFT-2020 (Cardon et al., 2020) contains clinical cases, encyclopedia and drug labels introduced in the 2020 edition of an annual French Text Mining Challenge, called DEFT, and annotated for two tasks: (i) textual similarity and (ii) multi-class classification." |
| Q22 | 3 | task_taxonomy | "The first task aims at identifying the degree of similarity within pairs of sentences, from 0 (the less similar) to 5 (the most similar)." |
| Q23 | 3 | task_taxonomy | "The second task consists in identifying, for a given sentence, the most similar sentence among three sentences provided." |
| Q24 | 3 | data_sources | "DEFT-2021 (Grouin et al., 2021) is a subset of 275 clinical cases taken from the 2019 edition of DEFT." |
| Q25 | 3 | annotation_process | "This dataset is manually annotated in two tasks: (i) multi-label classification and (ii) NER." |
| Q26 | 3 | task_taxonomy | "The multi-label classification task focuses on identifying the patient's clinical profile based on the diseases, signs, or symptoms mentioned in the clinical cases." |
| Q27 | 3 | label_categories | "The dataset is annotated with 23 axes from Chapter C of the Medical Subject Headings (MeSH)." |
| Q28 | 3 | task_taxonomy | "The second task involves fine-grained information extraction for 13 types of entities (more detail in Appendix B.7)." |
| Q29 | 3 | data_sources | "E3C (Magnini et al., 2020) is a multilingual dataset of clinical cases annotated for the NER task." |
| Q30 | 3 | label_categories | "It consists of two types of annotations (more detail in Appendix B.4): (i) clinical entities (e.g., pathologies), (ii) temporal information and factuality (e.g., events)." |
| Q31 | 3 | data_format | "While the dataset covers 5 languages, only the French portion is retained for the benchmark." |
| Q32 | 3 | data_format | "Since the dataset does not come with pre-defined subsets, we performed a 70 / 10 / 20 random split, as described in Table 3." |
| Q33 | 3 | data_sources | "The QUAERO French Medical Corpus (Névéol et al., 2014), simply referred to as QUAERO in this paper, contains annotated entities and concepts for NER tasks." |
| Q34 | 3 | data_sources | "The dataset covers two text genres (drug leaflets and biomedical titles), consisting of a total of 103,056 words sourced from EMEA or MEDLINE." |
| Q35 | 3 | label_categories | "10 entity categories corresponding to the UMLS Semantic Groups (Lindberg et al., 1993) were annotated (more detail in Appendix B.3)." |
| Q36 | 3 | data_format | "In total, 26,409 entity annotations were mapped to 5,797 unique UMLS concepts." |
| Q37 | 3 | stated_limitations | "Due to the presence of nested entities in annotations, we simplified the evaluation process by retaining only annotations at the higher granularity level from the BigBio (Fries et al., 2022) implementation, following the approach described in Touchent et al. (2023), which translates into an average loss of 6.06% of the annotations on EMEA and 8.90% on MEDLINE. Additionally, considering that some documents from EMEA exceed the maximum input sequence length that most current language models can handle, we decided to split these documents into sentences." |
| Q38 | 4 | data_sources | "MorFITT (Labrak et al., 2023) is a multi-label dataset annotated with medical specialties. It contains 3,624 biomedical abstracts from PMC Open Access. It has been annotated across 12 medical specialties (more detail in Appendix B.5), for a total of 5,116 annotations." |
| Q39 | 4 | task_taxonomy | "FrenchMedMCQA (Labrak et al., 2022) is a Multiple-Choice Question-Answering (MCQA) dataset for biomedical domain. It contains 3,105 questions coming from real exams of the French medical specialization diploma in pharmacy, integrating single and multiple answers. The first task consists of automatically identifying the set of correct answers among the 5 proposed for a given question. The second task consists of identifying the number of answers (between 1 and 5) supposedly correct for a given question." |
| Q40 | 4 | data_sources | "Mantra-GSC (Kors et al., 2015) is a multilingual dataset annotated for biomedical NER. From the 5 languages covered, we included only the French subset in this benchmark. The dataset is obtained from 3 sources which have been partitioned to be evaluated separately by 2 annotation schemes (more detail in Appendix B.6): Medline (11 classes), and EMEA and Patents (10 classes). The sources cover different types of documents (biomedical abstracts/titles, drug labels and patents). To ensure evaluation consistency, we randomly split the dataset into 3 subsets: 70% for training, 10% for validation, and 20% for testing." |
| Q41 | 4 | annotation_process | "CLISTER (Hiebel et al., 2022) is a French clinical cases Semantic textual similarity (STS) dataset of 1,000 sentence pairs manually annotated by several annotators, who assigned similarity scores ranging from 0 to 5 to each pair. The scores were then averaged together to obtain a floating-point number representing the overall similarity. The objective of this dataset is to develop models that can automatically predict a similarity score that closely aligns with the reference score based solely on the two sentences provided." |
| Q42 | 4 | data_format | "CAS (Grabar et al., 2018) comprises 3,790 clinical cases that have been annotated for POS tagging with 31 classes using automatic annotations through Tagex 3, with an evaluation conducted by comparing the automatic outputs against manual annotations. This evaluation yielded 98% precision. Since the dataset does not come with predefined subsets, we made the decision to randomly split it into 3 subsets of 70%, 10% and 20% of the total data for training, validation and test respectively." |
| Q43 | 4 | data_sources | "ESSAI (Dalloux et al., 2021) contains 7,247 clinical trial protocols annotated in 41 POS tags using TreeTagger (Schmid, 1994). As the dataset was not originally divided into 3 subsets, we applied the same procedure as on the CAS corpus." |
| Q44 | 4 | task_taxonomy | "PxCorpus (Kocabiyikoglu et al., 2022) is a spoken language understanding dataset in the domain of medical drug prescription transcripts. It includes 4 hours (1,981 recordings) of transcribed and annotated dialogues focused on drug prescriptions. The recordings were manually transcribed and semantically annotated. The first task involves classifying the textual utterances into one of the 4 intent classes (prescribe, replace, negate, none). The second task is a NER task where each word in a sequence is classified into one of 38 classes, such as drug, dose, or mode (more detail in Appendix B.9)." |
| Q45 | 4 | annotation_process | "DiaMed is an original dataset created specifically for DrBenchmark. It comprises 739 new French clinical cases collected from an open source journal (The Pan African Medical Journal). The cases have been manually annotated by several annotators, one of which is a medical expert, into 22 chapters of the International Classification of Diseases, 10th Revision (ICD-10) (Wor, 2019). These chapters provide a general description of the type of injury or disease. To ease the annotation process, only label at the chapter level were used (more detail in Appendix B.8). The inter-annotator agreement between the 4 annotators has been computed for two annotation sessions (see Table 4), with 15 different clinical cases assessed per session." |
| Q46 | 4 | evaluation_metrics | "Table 4: Inter-annotator agreement statistics. κ is referring to Kappa Cohen and G to Gwet's AC1." |
| Q47 | 4 | stated_limitations | "To facilitate the adoption of DrBenchmark and ensure consistency in implementations, we have de-" |
| Q48 | 5 | data_format | "We developed a practical toolkit based on the HuggingFace Datasets library (Lhoest et al., 2021). This toolkit includes data loaders that adhere to normalized schemes and predefined data splits. It also provides pre-training and evaluation scripts for each of the tasks, utilizing the HuggingFace Transformers (Wolf et al., 2020) and PyTorch (Paszke et al., 2019) libraries." |
| Q49 | 5 | evaluation_metrics | "For further guidance, we have integrated all the training details, including hyperparameters, in Appendix A. This information will help users to reproduce and customize the experiments conducted with DrBenchmark." |
| Q50 | 5 | task_taxonomy | "To guarantee fair comparison, we focus exclusively on pre-trained masked language models (MLMs) in this study. These MLMs are based on BERT-like architectures (Devlin et al., 2019)." |
| Q51 | 5 | evaluation_metrics | "All the models are fine-tuned regarding a strict protocol using the same hyperparameters for each downstream task. The reported results are obtained by averaging the scores from four separate runs, thus ensuring robustness and reliability. We also report statistical significance computed using Student's t-test." |
| Q52 | 6 | evaluation_metrics | "To ensure a fair and consistent comparison among systems for sequence-to-sequence tasks such as POS tagging and NER, we chose the SeqEval (Nakayama, 2018) metric in conjunction with the IOB2 format and the training of all the models to predict only the label on the first token of each word as mentioned by Touchent et al. (2023)." |
| Q53 | 6 | evaluation_metrics | "It provides a tokenizer-agnostic evaluation and mitigates any correlation between models' performances and the tokenization process." |
| Q54 | 6 | evaluation_metrics | "For STS tasks, the models' performance was assessed using two metrics: (1) the Spearman correlation, and (2) the mean relative solution distance accuracy (EDRM), as defined by the original authors of the DEFT-2020 dataset (Cardon et al., 2020)." |
| Q55 | 6 | task_taxonomy | "In Section 5.1, we compare the results obtained by each model within DrBenchmark, which permits to position a wide range of state-of-the-art models in the biomedical field across various NLP tasks." |
| Q56 | 6 | evaluation_metrics | "The results of the 8 models are reported in Table 6 and compared to a baseline obtained by considering the majority class for all predictions." |
| Q57 | 6 | stated_limitations | "Overall, although we might anticipate certain models to excel in all tasks, we discovered that no single model outperforms the rest in all application scenarios." |
| Q58 | 6 | stated_limitations | "Interestingly, most of the models examined manage to secure the top position in at least one of the French biomedical downstream tasks studied." |
| Q59 | 6 | stated_limitations | "The only exception pertains to the cross-lingual generalist model (XLM-RoBERTa), which manages to reach the second-best position on several tasks." |
| Q60 | 6 | stated_limitations | "French biomedical language models (DrBERT-FS, DrBERT-CP, CamemBERT-bio), presumed to be the most aligned with the nature of the data of the benchmark, exhibit indeed superior performance across many tasks." |
| Q61 | 6 | evaluation_metrics | "More precisely, DrBERT-FS achieves the highest performance in 8 tasks, DrBERT-CP in 5 tasks, and CamemBERT-bio in 2 tasks." |
| Q62 | 6 | evaluation_metrics | "This indicates that domain and language-specialized models achieve the best performance in up to 75% of the DrBenchmark downstream tasks." |
| Q63 | 6 | stated_limitations | "Generalist models (CamemBERT, CamemBERTa, FlauBERT and XLM-RoBERTa) are more suitable for tasks that require extensive linguistic knowledge but may not perform as well as specialized models nor even reach their level of performance." |
| Q64 | 6 | evaluation_metrics | "We observe that all generalist models obtain better performance only on 4 out of the 20 tasks, but still remain competitive on most tasks." |
| Q65 | 6 | stated_limitations | "Furthermore, our experiments with DrBERT-FS indicate that biomedical models may require less pre-training data compared to generalist ones." |
| Q66 | 6 | stated_limitations | "However, it is important to note that this observation requires further confirmation." |
| Q67 | 6 | stated_limitations | "In some tasks, biomedical models that undergo continual pre-training from a generalist model, such as CamemBERT-bio, can prove to be the most effective, underscoring the value of pre-training on generalist data." |
| Q68 | 7 | data_format | "For this purpose, we conducted experiments by varying the amount of training data during the fine-tuning process by randomly choosing four percentages of the training data: 25%, 50%, 75% and 100%." |
| Q69 | 7 | evaluation_metrics | "To make the experiment as fair as possible, we did four runs for each percentage, model and dataset combination." |
| Q70 | 7 | evaluation_metrics | "The validation and test sets have not been changed for the sake of comparison." |
| Q71 | 7 | evaluation_metrics | "We observe that on certain datasets, some models capture information more quickly than others, like in Figures 1b, 1f and 1a." |
| Q72 | 7 | evaluation_metrics | "Unsurprisingly, in almost all scenarios, having the complete training set yields better results than having only 25% of it." |
| Q73 | 7 | stated_limitations | "However, all the models based on CamemBERT face difficulties in corpora with limited amount of data, such as MantraGSC Patents, where they fail to generate labels other than 'O'." |
| Q74 | 7 | evaluation_metrics | "On the other hand, in the same low-resource scenarios, CamemBERTa models exhibit greater robustness and achieve superior performance." |
| Q75 | 8 | data_format | "Tokenizers play a crucial role in MLMs by utilizing size-limited vocabularies to split texts into sub-units, aiming to handle out-of-vocabulary (OOV) words." |
| Q76 | 8 | data_sources | "Due to variations in the training data, vocabularies differ across different models, as illustrated in Figure 2." |
| Q77 | 8 | stated_limitations | "So far, there has been a prevailing notion in the community that excessive segmentation of words in tokenization leads to a loss of morphological form and semantic meaning, introducing noise and adversely affecting performance (Church, 2020; Hofmann et al., 2021; Bostrom and Durrett, 2020)." |
| Q78 | 8 | evaluation_metrics | "However, our experiments, as shown in Table 7, reveal that FlauBERT is the model with the least word segmentation (1.43 in average), while DrBERT-CP tends to have the highest average segmentation (1.90 in average)." |
| Q79 | 8 | stated_limitations | "Surprisingly, when comparing the performance of these two models on the benchmark tasks, we observe that DrBERT-CP outperforms FlauBERT on 16 out of the 20 tasks, thus contradicting previous conclusions drawn by the community." |
| Q80 | 8 | stated_limitations | "Yet, tokenization, as it is currently done in MLMs, seems to play a minor role in the performance of systems." |
| Q81 | 8 | task_taxonomy | "Table 8 summarizes the results obtained on average by the considered MLMs when aggregating the tasks into one of the five designated categories: POS, NER, MCQA, MCC (Multi-class classification), MLC (Multi-label classification), or STS tasks." |
| Q82 | 8 | evaluation_metrics | "Upon analyzing the average performance by task category, it becomes evident that the leading model, DrBERT-FS, does not excel in tasks such as MLC or STS." |
| Q83 | 9 | task_taxonomy | "In this paper, we introduced DrBenchmark, the first large language understanding benchmark tailored for the French biomedical domain." |
| Q84 | 9 | task_taxonomy | "We conducted a qualitative evaluation of 8 state-of-the-art masked language models (MLMs) on this comprehensive benchmark, encompassing 20 diverse downstream tasks." |
| Q85 | 9 | stated_limitations | "Our findings illuminate the limitations of generalist models in tackling complex biomedical tasks, emphasizing the importance of employing domain-specific models to achieve peak performance." |
| Q86 | 9 | stated_limitations | "We have observed that several biomedical tasks in DrBenchmark exhibit relatively poor performance, even when utilizing specialized biomedical models." |
| Q87 | 9 | stated_limitations | "We postulate that the models examined in this study, here state-of-the-art MLMs, may not be the most effective choices for specific tasks such as question-answering or multi-label classification." |
| Q88 | 9 | stated_limitations | "The quantitative study we conducted on the PLMs requires further in-depth analysis to comprehend the impact of different parameters." |
| Q89 | 9 | data_format | "Firstly, we investigated the influence of tokenizers based on the average number of sub-tokens they produce per word." |
| Q90 | 9 | data_format | "Various tokenization algorithms are employed, depending on the model under examination." |
| Q91 | 9 | stated_limitations | "The size of the data has not been thoroughly investigated, particularly the significance of the pre-training data size, especially specialized data in the biomedical field." |
| Q92 | 9 | stated_limitations | "Although the benchmark is easily reproducible and customizable, it required a substantial amount of computational power to execute all runs." |
| Q93 | 9 | stated_limitations | "We utilized approximately 2,500 hours on V100 GPUs from the Jean-Zay supercomputer to complete the quantitative study." |
| Q94 | 9 | stated_limitations | "According to the Jean Zay supercomputer documentation, the total environmental cost is estimated to be equivalent to 647,500 Wh or 36.9 kgCO2eq/kWh, based on the carbon intensity of the energy grid mentioned in the BLOOM environmental cost study conducted on Jean Zay (Luccioni et al., 2022)." |
| Q95 | 9 | authors_affiliations | "All code for DrBenchmark is released under the MIT License." |
| Q96 | 9 | data_sources | "The licensing for all datasets remains unchanged from the original sources, and DrBenchmark has no intention of redistributing these datasets." |
| Q97 | 9 | authors_affiliations | "This work was performed using HPC resources from GENCI-IDRIS (Grant 2022-AD011013061R1 and 2022-AD011013715) and from CCIPL (Centre de Calcul Intensif des Pays de la Loire)." |
| Q98 | 9 | authors_affiliations | "This work was financially supported by ANR MALADES (ANR-23-IAS1-0005), ANR AIBy4 (ANR-20-THIA-0011) and Zenidoc." |
| Q99 | 13 | evaluation_metrics | "For the experiments, we utilize the following hyperparameters that yield optimal performance from the models." |
| Q100 | 13 | evaluation_metrics | "To mitigate overfitting, we locally save the best model based on its validation metric." |
| Q101 | 14 | label_categories | "INT, PRO:DEM, VER:impf, VER:ppre, PRP:det, KON, VER:pper, PRP, PRO:IND, VER:simp, VER:con, SENT, VER:futu, PRO:PER, VER:infi, ADJ, NAM, NUM, PUN:cit, PRO:REL, VER:subi, ABR, NOM, VER:pres, DET:ART, VER:cond, VER:subp, DET:POS, ADV, SYM and PUN." |
| Q102 | 14 | label_categories | "INT, PRO:POS, PRP, SENT, PRO, ABR, VER:pres, KON, SYM, DET:POS, VER:, PRO:IND, NAM, ADV, PRO:DEM, NN, PRO:PER, VER:pper, VER:ppre, PUN, VER:simp, PREF, NUM, VER:futu, NOM, VER:impf, VER:subp, VER:infi, DET:ART, PUN:cit, ADJ, PRP:det, PRO:REL, VER:cond and VER:subi." |
| Q103 | 14 | label_categories | "O, GEOG, PHEN, DISO, ANAT, OBJC, PHYS, PROC, DEVI, CHEM and LIVB" |
| Q104 | 14 | label_categories | "Clinical: O, and CLINENTITY. Temporal: O, EVENT, ACTOR, BODYPART, TIMEX3 and RML" |
| Q105 | 14 | label_categories | "microbiology, etiology, virology, physiology, immunology, parasitology, genetics, chemistry, veterinary, surgery, pharmacology and psychology" |
| Q106 | 14 | label_categories | "Medline: ANAT, PROC, CHEM, PHYS, GEOG, DEVI, LIVB, OBJC, DISO, PHEN and O. EMEA and Patents: ANAT, PROC, CHEM, PHYS, DEVI, LIVB, OBJC, DISO, PHEN and O." |
| Q107 | 14 | label_categories | "Multi-label Classification: immunitaire (immunology), endocriniennes (endocrinology), blessures (injury), chimiques (chemicals), etatsosy (signs and symptoms), nutritionnelles (nutrition), infections (infections), virales (virology), parasitaires (parasitology), tumeur (oncology), osteomusculaires (osteomuscular disorders), stomatognathique (stomatology), digestif (digestive system disorders), respiratoire (respiratory system disorders), ORL (otorhinolaryngologic diseases), nerveux (nervous system disorders), oeil (eye diseases), homme (male genital diseases), femme (female genital diseases), cardiovasculaires (cardiology), hemopathies (hemic and lymphatic diseases), genetique (genertic disorders) and peau (dermatology)." |
| Q108 | 14 | label_categories | "Named-entity recognition: O, ANATOMY, DATE, DOSAGE, DURATION, MEDICAL EXAM, FREQUENCY, MODE, MOMENT, PATHOLOGY, SOSY, SUBSTANCE, TREATMENT and VALUE" |

### Category Index
- **task_taxonomy**: Q1, Q4, Q13, Q14, Q15, Q17, Q18, Q20, Q21, Q22, Q23, Q26, Q28, Q39, Q44, Q50, Q55, Q81, Q83, Q84
- **data_sources**: Q12, Q19, Q24, Q29, Q33, Q34, Q38, Q40, Q43, Q76, Q96
- **data_format**: Q31, Q32, Q36, Q42, Q48, Q68, Q75, Q89, Q90
- **label_categories**: Q27, Q30, Q35, Q101, Q102, Q103, Q104, Q105, Q106, Q107, Q108
- **annotation_process**: Q25, Q41, Q45
- **evaluation_metrics**: Q2, Q6, Q46, Q49, Q51, Q52, Q53, Q54, Q56, Q61, Q62, Q64, Q69, Q70, Q71, Q72, Q74, Q78, Q82, Q99, Q100
- **stated_limitations**: Q3, Q5, Q9, Q10, Q11, Q16, Q37, Q47, Q57, Q58, Q59, Q60, Q63, Q65, Q66, Q67, Q73, Q77, Q79, Q80, Q85, Q86, Q87, Q88, Q91, Q92, Q93, Q94
- **authors_affiliations**: Q7, Q8, Q95, Q97, Q98
