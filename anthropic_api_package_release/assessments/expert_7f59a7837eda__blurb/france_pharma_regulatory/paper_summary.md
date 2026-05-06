```markdown
# Validity Extraction: Domain-Specific Language Model Pretraining for Biomedical Natural Language Processing (BLURB)
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: Domain-Specific Language Model Pretraining for Biomedical Natural Language Processing (BLURB)
- **Authors**: Yu Gu, Robert Tinn, Hao Cheng, Michael Lucas, Naoto Usuyama, Xiaodong Liu, Tristan Naumann, Jianfeng Gao, Hoifung Poon
- **Venue/Year**: Microsoft Research (preprint/publication); year inferred from registry context as ~2021
- **Total Pages**: 24
- **Quotes Extracted**: 206

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

---

### 1. Task Taxonomy / Test Case Categories

BLURB is described as "a comprehensive set of biomedical NLP tasks from publicly available datasets, including named entity recognition (NER), evidence-based medical information extraction (PICO), relation extraction, sentence similarity, document classification, and question answering" [Q48], amounting to thirteen datasets across six task types [Q194]. The benchmark was explicitly inspired by general-domain efforts like GLUE and SuperGLUE [Q36, Q205, Q206] and is positioned as the first leaderboard for biomedical NLP [Q194], building on the earlier BLUE benchmark [Q38] while addressing its limitations [Q39].

On the input side, the benchmark targets PubMed-based biomedical text exclusively [Q46], covering tasks that have evolved "from simple tasks, such as named entity recognition, to more sophisticated tasks, such as relation extraction and question answering" [Q192]. NER is modeled as sequential labeling using BIO or BIOUL tagging schemes [Q107, Q109], while PICO extraction is "akin to slot filling" but formulated as a sequential tagging task [Q111, Q112]. Relation extraction focuses on binary or multi-class classification over entity pairs within sentences [Q114, Q115], and question answering is restricted to yes/no and three-way classification formats [Q124], explicitly excluding more complex list and summary tasks [Q50, Q51].

On the output side, task-specific prediction models are layered atop the pretrained language model [Q93, Q94], with the benchmark score computed as a macro average of per-task-type scores rather than a flat average across all datasets, to avoid over-weighting tasks with many datasets [Q52]. Ablation studies investigate the impact of tagging scheme complexity [Q181], entity representation choices [Q187, Q188, Q189, Q190], and sequential labeling architectures [Q173, Q174], finding that simpler approaches perform comparably with BERT [Q2, Q182].

From a deployment-validity perspective, the benchmark's task ontology presents a significant gap for the target pharmaceutical regulatory use case. Although NER and sentence similarity (STS) tasks are directly represented [Q48], the input categories are anchored in research-oriented biomedical prose (PubMed abstracts) rather than the formulaic, legally constrained language of SmPCs, CTD modules, or patient information leaflets. No regulatory-document genre appears anywhere in the task taxonomy. Furthermore, BLURB's STS task (BIOSSES) is framed around general biomedical semantic proximity [Q201], not regulatory equivalence — a qualitatively different output construct where small lexical variations carry legal consequence, as the deployment context requires.

---

### 2. Data Sources and Collection

The benchmark compiles data exclusively from publicly available datasets [Q1], with all NER, relation extraction, PICO, and QA datasets sourced from PubMed abstracts [Q53, Q54, Q56, Q57, Q58, Q59, Q64, Q68, Q70, Q71, Q77, Q81]. Shared task corpora dominate the collection, including BioCreative, BioNLP, SemEval, and BioASQ datasets [Q191], all of which are well-established in the biomedical NLP community. The pretraining corpus for PubMedBERT itself consists of 14 million PubMed abstracts (3.2 billion words, 21 GB), filtered to exclude abstracts with fewer than 128 words [Q126, Q127]; an experiment adding PubMed Central full-text articles expanded the corpus to 16.8 billion words [Q166] but produced marginal or negative effects [Q167].

Prior biomedical BERT efforts drew on mixed sources: BioBERT used PubMed abstracts and PMC full text [Q18], BlueBERT added MIMIC-III clinical notes [Q18], and SciBERT incorporated computer science text alongside biomedical literature [Q20]. BLURB deliberately excludes MIMIC-based clinical datasets — present in the earlier BLUE benchmark [Q42] — reasoning that "clinical notes differ substantially from biomedical literature" [Q43] and that separate benchmarks for the two domains are preferable [Q44]. The EBM PICO corpus is a notable example of a multi-annotator dataset sourced from PubMed abstracts on clinical trials [Q59, Q198].

For the deployment context, the exclusive reliance on English PubMed abstracts is a critical limitation: French regulatory documents (SmPCs, patient leaflets, ANSM submissions) constitute the target input domain, and no French-language source appears anywhere in BLURB's data sources. Additionally, the regulatory-specific entity types required by the deployment — INNs, ATC codes, excipient nomenclature, posology expressions — are unlikely to appear with sufficient density or systematic annotation in PubMed research abstracts, further widening the construct gap between benchmark data sources and deployment needs.

---

### 3. Data Format and Preprocessing

Input instances are processed through a `TransformInput` module that performs task-specific transformations, including appending special tokens (e.g., `[CLS]`) and dummifying entity mentions for relation extraction [Q99]. Sequence length is managed by padding or truncation: 128 tokens for GAD, 256 tokens for ChemProt and DDI, and 512 tokens for question-answering tasks [Q120, Q125]. For sentence similarity, a `[SEP]` token separates sentence pairs and a `[CLS]` token is prepended [Q122]. For relation extraction, several encoding strategies are compared, including `[CLS]`-based encoding, entity start-token encoding, and concatenated entity mention representations obtained via max pooling [Q118, Q119, Q185].

A key preprocessing distinction concerns vocabulary: continually pretrained models (BioBERT, BlueBERT, ClinicalBERT) retain the original BERT vocabulary derived from Wikipedia and BookCorpus [Q134], which does not represent biomedical terminology well — common terms like *naloxone* are fragmented into four subword pieces and *acetyltransferase* into seven [Q29]. PubMedBERT generates its vocabulary from PubMed text, resulting in shorter tokenized inputs for biomedical text [Q162, Q168]. Training uses whole-word masking at a 15% rate [Q133], and both cased and uncased models were tested with negligible difference [Q132]; training required approximately five days on 16 V100 GPUs [Q131].

Dataset-specific preprocessing choices are documented throughout: pre-processed splits from Crichton et al. are used for several NER datasets [Q55, Q56, Q57, Q58], ChemProt training and development sets are expanded by assigning false labels to unlabeled chemical-protein pairs [Q66], GAD uses semi-automatically generated positive and negative examples [Q72, Q73], and HoC labels are aggregated from sentence-level to abstract-level [Q84, Q85, Q87, Q91]. The cased/uncased and `[CLS]`-encoding decisions [Q132] are made for the English-language domain; for the deployment's French-language text, these preprocessing pipelines would require substantial re-engineering, and the in-domain vocabulary advantage of PubMedBERT would not transfer without retraining on French corpora.

---

### 4. Label Categories and Output Types

The label ontology across BLURB tasks spans several distinct types. For NER, token-level BIO or BIOUL tags are used [Q107, Q109], with BLURB's NER tasks largely collapsed to a single entity type per dataset (e.g., chemical, disease, gene) [Q108]. For relation extraction, ChemProt uses a six-way classification: five high-level chemical-protein interaction types (UPREGULATOR, DOWNREGULATOR, AGONIST, ANTAGONIST, SUBSTRATE) plus a catch-all false class [Q65]. For sentence similarity (BIOSSES), the output is a continuous regression score from 0 (no relation) to 4 (equivalent meanings), with the final annotation taken as the average across five expert annotators [Q74, Q75]. For document classification (HoC), labels are binary indicators for each of ten top-level cancer hallmarks, evaluated via micro F1 [Q78, Q83]. For question answering, PubMedQA uses a three-way label (yes/maybe/no) [Q86], while BioASQ uses binary yes/no labels [Q90].

From the deployment perspective, the label ontology presents two significant validity gaps. First, BLURB's NER label set covers genes, chemicals, diseases, and molecular biology entities — not regulatory-specific categories such as INNs, ATC codes, excipient names, posology expressions, or contraindication qualifiers required by EMA SmPC templates. Second, the BIOSSES regression scoring of semantic similarity [Q75, Q76] operationalizes general biomedical semantic proximity, not regulatory equivalence: under EMA/ANSM standards, small differences in dose thresholds or population qualifiers are legally determinative mismatches, a distinction that a 0–4 continuous scale cannot capture without threshold-sensitive calibration absent from the benchmark design.

---

### 5. Annotation Process

Annotation provenance varies substantially across BLURB's constituent datasets, and documentation is uneven. The EBM PICO dataset has a clearly documented mixed-annotator design: "The training and development sets were labeled by Amazon Mechanical Turkers, whereas the test set was labeled by Upwork contributors with prior medical training" [Q60] — a notable quality stratification between crowdsourced and domain-trained annotators. BIOSSES sentence similarity scores were produced by "five expert-level annotators" [Q74], providing a meaningful inter-annotator basis for the regression labels. The BioASQ corpus is "annotated by biomedical experts" across multiple QA sub-tasks [Q88].

NOT DOCUMENTED in detail: inter-annotator agreement (IAA) statistics, annotator demographics (beyond general descriptors like "biomedical experts" or "Mechanical Turkers"), and structured QA protocols are not systematically reported across the benchmark as a whole. For the deployment context, this absence is a significant validity concern: the deployment's ground-truth authority rests with regulatory affairs specialists and legal experts operating under EMA/ANSM normative frameworks, a population systematically different from the biomedical research community and crowdworkers who produced BLURB's annotations. The user explicitly anticipates "systematic disagreements on borderline cases, where biomedical NLP annotators are likely to prioritize clinical relevance over rigid legal constraints" — a misalignment that the paper provides no basis to quantify.

---

### 6. Evaluation Metrics and Output Modality

The primary summary metric is the BLURB score, defined as "the macro average of average test results for each of the six tasks" [Q150], deliberately grouping datasets by task type before averaging to avoid over-weighting NER [Q52]. Task-specific metrics include entity-level F1 for NER [Q176], word-level F1 per PIO element averaged across elements for PICO [Q61], micro F1 for ChemProt and HoC [Q83], Pearson correlation for BIOSSES [Q76], and accuracy for QA tasks. Models are fine-tuned using cross-entropy loss for classification and mean-square error for regression [Q100], with a slanted triangular learning rate schedule and 0.1 dropout [Q138].

Hyperparameter tuning is conducted on development sets [Q101, Q141], with the search range fixed across models for computational tractability [Q145]. To handle variance from random initialization and dropout — particularly on small datasets like BIOSSES, BioASQ, and PubMedQA — results are averaged over ten runs for those datasets and five runs for others [Q140]. The leaderboard is publicly released with pretrained and task-specific models [Q3, Q196], and comparisons with published results for BioBERT, SciBERT, and BlueBERT are reported as "generally comparable or better" [Q158].

From the deployment perspective, the output modality — text-in / discrete-label-or-continuous-score-out — broadly matches the deployment's NER and STS pipeline, representing a point of surface alignment. However, the deployment introduces a threshold-sensitivity requirement not captured by any BLURB metric: borderline or inconsistent STS scores trigger human review rather than automatic rejection, meaning the benchmark's aggregate Pearson correlation or macro F1 scores do not reveal how a model would behave at operationally critical decision boundaries. The fixed hyperparameter strategy [Q145] and the absence of confidence-calibration metrics further limit direct applicability to a workflow where score reliability at threshold determines regulatory action.

---

### 7. Stated Limitations

The authors articulate numerous limitations, spanning pretraining design, benchmark scope, and experimental methodology. On pretraining, they note that "the majority of general domain text is substantively different from biomedical text, raising the prospect of negative transfer" [Q12], and that continual pretraining may fail to "completely undo suboptimal initialization from the general-domain language model" [Q33]. BERT models using out-of-domain vocabularies are "forced to divert parametrization capacity and training bandwidth to model biomedical terms using fragmented subwords" [Q28, Q29]. Surprisingly, adding PMC full-text articles to PubMed abstracts "generally leads to a slight degradation in performance across the board" [Q167], attributed to distributional differences between full text and abstracts [Q170].

On benchmark scope, the authors acknowledge that BLUE's mixing of PubMed-based and MIMIC-based tasks is problematic [Q42, Q43], and that BLURB itself has limited coverage relative to recent work [Q40], excludes question-answering tasks of greater complexity [Q41, Q50, Q51], and defers clinical and other high-value domains to future work [Q46, Q197]. Prior work on biomedical pretraining "tends to use different tasks and datasets for downstream evaluation" [Q37], making cross-study comparisons difficult — a limitation BLURB partially addresses but does not fully resolve [Q95].

On methodology, the authors note variance instability on small datasets [Q139], acknowledge that "ideally, we would conduct separate hyperparameter tuning for each model on each dataset" but cannot do so due to computational cost [Q142, Q143], and concede that exploration of BERT-LARGE models is deferred [Q136, Q137]. Adversarial pretraining unexpectedly "generally leads to a slight degradation in performance" [Q171], left for future investigation.

For the deployment context, the most consequential limitation is one the authors do not directly address: BLURB is English-only and PubMed-centric, with no acknowledgment of multilingual biomedical NLP or regulatory document genres. The authors do flag that "none of the prior biomedical-related BERT models have been pretrained using purely biomedical text" [Q15] and challenge the mixed-domain pretraining assumption [Q16], but the challenge remains entirely within English-language biomedical research text. The future directions mention "extension of the BLURB benchmark to clinical and other high-value domains" [Q197] but make no mention of regulatory, multilingual, or French-language extensions — gaps directly material to the target deployment.

---

### 8. Authors and Affiliations

All authors are affiliated with Microsoft Research [Q4]: Yu Gu, Robert Tinn, Hao Cheng, Michael Lucas, Naoto Usuyama, Xiaodong Liu, Tristan Naumann, Jianfeng Gao, and Hoifung Poon. The work is positioned as a research contribution to the biomedical NLP community, including release of pretrained models and a public leaderboard [Q196]. The institutional origin is a major U.S.-based technology company research division, with no co-authorship from European regulatory bodies (EMA, ANSM), French academic institutions, or pharmaceutical regulatory affairs organizations — affiliations that would be relevant for a benchmark intended to serve EU regulatory compliance workflows. This affiliation profile signals that the benchmark's design priorities, task selection, and annotator networks are grounded in English-language biomedical research rather than multilingual or regulatory-domain NLP, consistent with the validity gaps identified across other dimensions.
```

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | data_sources | "we compile a comprehensive biomedical NLP benchmark from publicly-available datasets." |
| Q2 | 1 | task_taxonomy | "we discover that some common practices are unnecessary with BERT models, such as using complex tagging schemes in named entity recognition (NER)." |
| Q3 | 1 | evaluation_metrics | "we have released our state-of-the-art pretrained and task-specific models for the community, and created a leaderboard featuring our BLURB benchmark (short for Biomedical Language Understanding & Reasoning Benchmark)." |
| Q4 | 1 | authors_affiliations | "Yu Gu, Robert Tinn, Hao Cheng, Michael Lucas, Naoto Usuyama, Xiaodong Liu, Tristan Naumann, Jianfeng Gao, and Hoifung Poon, Microsoft Research" |
| Q5 | 1 | data_sources | "Existing pretraining work typically focuses on the newswire and Web domains." |
| Q6 | 1 | data_sources | "the original BERT model was trained on Wikipedia and BookCorpus [62], and subsequent efforts have focused on crawling additional text from the Web to power even larger-scale pretraining [39, 50]." |
| Q7 | 2 | task_taxonomy | "In specialized domains like biomedicine, past work has shown that using in-domain text can provide additional gains over general-domain language models [8, 34, 45]." |
| Q8 | 2 | task_taxonomy | "However, a prevailing assumption is that out-domain text is still helpful and previous work typically adopts a mixed-domain approach, e.g., by starting domain-specific pretraining from an existing general-domain language model (Figure 1 top)." |
| Q9 | 2 | task_taxonomy | "We observe that mixed-domain pretraining such as continual pretraining can be viewed as a form of transfer learning in itself, where the source domain is general text, such as newswire and the Web, and the target domain is specialized text such as biomedical papers." |
| Q10 | 2 | task_taxonomy | "Based on the rich literature of multi-task learning and transfer learning [4, 13, 38, 59], successful transfer learning occurs when the target data is scarce and the source domain is highly relevant to the target one." |
| Q11 | 2 | stated_limitations | "For domains with abundant unlabeled text such as biomedicine, it is unclear that domain-specific pretraining can benefit by transfer from general domains." |
| Q12 | 2 | stated_limitations | "In fact, the majority of general domain text is substantively different from biomedical text, raising the prospect of negative transfer that actually hinders the target performance." |
| Q13 | 4 | task_taxonomy | "In this paper, we will use biomedicine as a running example in our study of domain-specific pretraining. In other words, biomedical text is considered in-domain, while others are regarded as out-domain." |
| Q14 | 4 | data_sources | "Intuitively, using in-domain text in pretraining should help with domain-specific applications. Indeed, prior work has shown that pretraining with PubMed text leads to better performance in biomedical NLP tasks [8, 34, 45]." |
| Q15 | 4 | stated_limitations | "The main question is whether pretraining should include text from other domains. The prevailing assumption is that pretraining can always benefit from more text, including out-domain text. In fact, none of the prior biomedical-related BERT models have been pretrained using purely biomedical text [8, 34, 45]." |
| Q16 | 4 | stated_limitations | "Here, we challenge this assumption and show that domain-specific pretraining from scratch can be superior to mixed-domain pretraining for downstream applications." |
| Q17 | 4 | data_sources | "The standard approach to pretraining a biomedical BERT model conducts continual pretraining of a general-domain pretrained model, as exemplified by BioBERT [34]. Specifically, this approach would initialize with the standard BERT model [16], pretrained using Wikipedia and BookCorpus. It then continues the pretraining process with MLM and NSP using biomedical text." |
| Q18 | 4 | data_sources | "In the case of BioBERT, continual pretraining is conducted using PubMed abstracts and PubMed Central full text articles. BlueBERT [45] uses both PubMed text and de-identified clinical notes from MIMIC-III [26]." |
| Q19 | 4 | data_format | "Note that in the continual pretraining approach, the vocabulary is the same as the original BERT model, in this case the one generated from Wikipedia and BookCorpus. While convenient, this is a major disadvantage for this approach, as the vocabulary is not representative of the target biomedical domain." |
| Q20 | 4 | data_sources | "Compared to the other biomedical-related pretraining efforts, SciBERT [8] is a notable exception as it generates the vocabulary and pretrains from scratch, using biomedicine and computer science as representatives for scientific literature. However, from the perspective of biomedical applications, SciBERT still adopts the mixed-domain pretraining approach, as computer science text is clearly out-domain." |
| Q21 | 4 | authors_affiliations | "Gu, Tinn, Cheng, et al." |
| Q22 | 5 | task_taxonomy | "The mixed-domain pretraining approach makes sense if the target application domain has little text of its own, and can thereby benefit from pretraining using related domains." |
| Q23 | 5 | data_sources | "However, this is not the case for biomedicine, which has over thirty million abstracts in PubMed, and adds over a million each year." |
| Q24 | 5 | task_taxonomy | "We thus hypothesize that domain-specific pretraining from scratch is a better strategy for biomedical language model pretraining." |
| Q25 | 5 | task_taxonomy | "A major advantage of domain-specific pretraining from scratch stems from having an in-domain vocabulary." |
| Q26 | 5 | stated_limitations | "BERT models using continual pretraining are stuck with the original vocabulary from the general-domain corpora, which does not contain many common biomedical terms." |
| Q27 | 5 | stated_limitations | "Even for SciBERT, which generates its vocabulary partially from biomedical text, the deficiency compared to a purely biomedical vocabulary is substantial." |
| Q28 | 5 | stated_limitations | "As a result, standard BERT models are forced to divert parametrization capacity and training bandwidth to model biomedical terms using fragmented subwords." |
| Q29 | 5 | stated_limitations | "For example, naloxone, a common medical term, is divided into four pieces ([na, ##lo, ##xon, ##e]) by BERT, and acetyltransferase is shattered into seven pieces ([ace, ##ty, ##lt, ##ran, ##sf, ##eras, ##e]) by BERT." |
| Q30 | 5 | data_sources | "Another advantage of domain-specific pretraining from scratch is that the language model is trained using purely in-domain data." |
| Q31 | 5 | stated_limitations | "For example, SciBERT pretraining has to balance optimizing for biomedical text and computer science text, the latter of which is unlikely to be beneficial for biomedical applications." |
| Q32 | 5 | stated_limitations | "Continual pretraining, on the other hand, may potentially recover from out-domain modeling, though not completely." |
| Q33 | 6 | stated_limitations | "that continual pretraining may not be able to completely undo suboptimal initialization from the general-domain language model." |
| Q34 | 6 | task_taxonomy | "In our experiments, we show that domain-specific pretraining with in-domain vocabulary confers clear advantages over mixed-domain pretraining, be it continual pretraining of general-domain language models, or pretraining on mixed-domain text." |
| Q35 | 6 | task_taxonomy | "The ultimate goal of language model pretraining is to improve performance on a wide range of downstream applications." |
| Q36 | 6 | task_taxonomy | "In general-domain NLP, the creation of comprehensive benchmarks, such as GLUE [56, 57], greatly accelerates advances in language model pretraining by enabling head-to-head comparisons among pretrained language models." |
| Q37 | 6 | stated_limitations | "In contrast, prior work on biomedical pretraining tends to use different tasks and datasets for downstream evaluation, as shown in Table 2." |
| Q38 | 6 | task_taxonomy | "To the best of our knowledge, BLUE [45] is the first attempt to create an NLP benchmark in the biomedical domain." |
| Q39 | 6 | stated_limitations | "We aim to improve on its design by addressing some of its limitations." |
| Q40 | 6 | stated_limitations | "First, BLUE has limited coverage of biomedical applications used in other recent work on biomedical language models, as shown in Table 2." |
| Q41 | 6 | stated_limitations | "For example, it does not include any question-answering task." |
| Q42 | 6 | data_sources | "More importantly, BLUE mixes PubMed-based biomedical applications (six datasets such as BC5, ChemProt, and HoC) with MIMIC-based clinical applications (four datasets such as i2b2 and MedNLI)." |
| Q43 | 6 | stated_limitations | "Clinical notes differ substantially from biomedical literature, to the extent that we observe BERT models pretrained on clinical notes perform poorly on biomedical tasks, similar to the standard BERT." |
| Q44 | 6 | task_taxonomy | "Consequently, it is advantageous to create separate benchmarks for these two domains." |
| Q45 | 6 | task_taxonomy | "To facilitate investigations of biomedical language model pretraining and help accelerate progress in biomedical NLP, we create a new benchmark, the Biomedical Language Understanding & Reasoning Benchmark (BLURB)." |
| Q46 | 6 | task_taxonomy | "We focus on PubMed-based biomedical applications, and leave the exploration of the clinical domain, and other high-value verticals to future work." |
| Q47 | 7 | stated_limitations | "prior work, we prioritize the selection of datasets used in recent work on biomedical language models, and will explore the addition of other datasets in future work." |
| Q48 | 7 | task_taxonomy | "BLURB is comprised of a comprehensive set of biomedical NLP tasks from publicly available datasets, including named entity recognition (NER), evidence-based medical information extraction (PICO), relation extraction, sentence similarity, document classification, and question answering." |
| Q49 | 7 | task_taxonomy | "For question answering, prior work has considered both classification tasks (e.g., whether a reference text contains the answer to a given question) and more complex tasks such as list and summary [42]." |
| Q50 | 7 | stated_limitations | "The latter types often require additional engineering effort that are not relevant to evaluating neural language models." |
| Q51 | 7 | stated_limitations | "For simplicity, we focus on the classification tasks such as yes/no question-answering in BLURB, and leave the inclusion of more complex question-answering to future work." |
| Q52 | 7 | evaluation_metrics | "To compute a summary score for BLURB, the simplest way is to report the average score among all tasks. However, this may place undue emphasis on simpler tasks such as NER for which there are many existing datasets. Therefore, we group the datasets by their task types, compute the average score for each task type, and report the macro average among the task types." |
| Q53 | 7 | data_sources | "The BioCreative V Chemical-Disease Relation corpus [35] was created for evaluating relation extraction of drug-disease interactions, but is frequently used as a NER corpus for detecting chemical (drug) and disease entities." |
| Q54 | 7 | data_sources | "The dataset consists of 1500 PubMed abstracts broken into three even splits for training, development, and test." |
| Q55 | 7 | data_format | "We use a pre-processed version of this dataset generated by Crichton et al. [14], discard the relation labels, and train NER models for chemical (BC5-Chemical) and disease (BC5-Disease) separately." |
| Q56 | 8 | data_sources | "NCBI-Disease. The Natural Center for Biotechnology Information Disease corpus [18] contains 793 PubMed abstracts with 6892 annotated disease mentions linked to 790 distinct disease entities. We use a pre-processed set of train, development, test splits generated by Crichton et al. [14]." |
| Q57 | 8 | data_sources | "BC2GM. The Biocreative II Gene Mention corpus [53] consists of sentences from PubMed abstracts with manually labeled gene and alternative gene entities. Following prior work, we focus on the gene entity annotation. In its original form, BC2GM contains 15000 train and 5000 test sentences. We use a pre-processed version of the dataset generated by Crichton et al. [14], which carves out 2500 sentences from the training data for development." |
| Q58 | 8 | data_sources | "JNLPBA. The Joint Workshop on Natural Language Processing in Biomedicine and its Applications shared task [27] is a NER corpus on PubMed abstracts. The entity types are chosen for molecular biology applications: protein, DNA, RNA, cell line, and cell type. Some of the entity type distinctions are not very meaningful. For example, a gene mention often refers to both the DNA and gene products such as the RNA and protein. Following prior work that evaluates on this dataset [34], we ignore the type distinction and focus on detecting the entity mentions. We use the same train, development, and test splits as in Crichton et al. [14]." |
| Q59 | 8 | data_sources | "EBM PICO. The Evidence-Based Medicine corpus [44] contains PubMed abstracts on clinical trials, where each abstract is annotated with P, I, and O in PICO: Participants (e.g., diabetic patients), Intervention (e.g., insulin), Comparator (e.g., placebo) and Outcome (e.g., blood glucose levels). Comparator (C) labels are omitted as they are standard in clinical trials: placebo for passive control and standard of care for active control. There are 4300, 500, and 200 abstracts in training, development, and test, respectively." |
| Q60 | 8 | annotation_process | "The training and development sets were labeled by Amazon Mechanical Turkers, whereas the test set was labeled by Upwork contributors with prior medical training." |
| Q61 | 8 | evaluation_metrics | "EBM PICO provides labels at the word level for each PIO element. For each of the PIO elements in an abstract, we tally the F1 score at the word level, and then compute the final score as the average among PIO elements in the dataset." |
| Q62 | 8 | stated_limitations | "Occasionally, two PICO elements might overlap with each other (e.g., a participant span might contain within it an intervention span). In EBM-PICO, about 3% of the PIO words are in the overlap." |
| Q63 | 8 | data_format | "Note that the dataset released along with SciBERT appears to remove the overlapping words from the larger span (e.g., the participant span as mentioned above). We instead use the original dataset [44] and their scripts for preprocessing and evaluation." |
| Q64 | 8 | data_sources | "ChemProt. The Chemical Protein Interaction corpus [31] consists of PubMed abstracts annotated with chemical-protein interactions between chemical and protein entities. There are 23 interactions organized in a hierarchy, with 10 high-level interactions (including NONE). The vast majority of relation instances in ChemProt are within single sentences. Following prior work [8, 34], we only consider sentence-level instances." |
| Q65 | 8 | label_categories | "We follow the ChemProt authors' suggestions and focus on classifying five high-level interactions — UPREGULATOR (CPR : 3), DOWNREGULATOR (CPR : 4), AGONIST (CPR : 5), ANTAGONIST (CPR : 6), SUBSTRATE (CPR : 9) — as well as everything else (false)." |
| Q66 | 8 | data_format | "The ChemProt annotation is not exhaustive for all chemical-protein pairs. Following previous work [34, 45], we expand the training and development sets by assigning a false label for all chemical-protein pairs that occur in a training or development sentence, but do not have an explicit label in the ChemProt corpus." |
| Q67 | 8 | stated_limitations | "Note that prior work uses slightly different label expansion of the test data. To facilitate head-to-head comparison, we will provide instructions for reproducing the test set in BLURB from the original dataset." |
| Q68 | 8 | data_sources | "DDI. The Drug-Drug Interaction corpus [21] was created to facilitate research on pharmaceutical information extraction, with a particular focus on pharmacovigilance. It contains sentence-level annotation of drug-drug interactions on PubMed abstracts. Note that some prior work [45, 61] discarded 90 training files that the authors" |
| Q69 | 9 | data_format | "We instead use the original dataset and produce our train/dev/test split of 624/90/191 files." |
| Q70 | 9 | data_sources | "The Genetic Association Database corpus [11] was created semi-automatically using the Genetic Association Archive." |
| Q71 | 9 | data_sources | "Specifically, the archive contains a list of gene-disease associations, with the corresponding sentences in the PubMed abstracts reporting the association studies." |
| Q72 | 9 | data_format | "Bravo et al. [11] used a biomedical NER tool to identify gene and disease mentions, and create the positive examples from the annotated sentences in the archive, and negative examples from gene-disease co-occurrences that were not annotated in the archive." |
| Q73 | 9 | data_format | "We use an existing preprocessed version of GAD and its corresponding train/dev/test split created by Lee et al. [34]." |
| Q74 | 9 | annotation_process | "The Sentence Similarity Estimation System for the Biomedical Domain [54] contains 100 pairs of PubMed sentences each of which is annotated by five expert-level annotators with an estimated similarity score in the range from 0 (no relation) to 4 (equivalent meanings)." |
| Q75 | 9 | label_categories | "It is a regression task, with the average score as the final annotation." |
| Q76 | 9 | evaluation_metrics | "We use the same train/dev/test split in Peng et al. [45] and use Pearson correlation for evaluation." |
| Q77 | 9 | data_sources | "The Hallmarks of Cancer corpus was motivated by the pioneering work on cancer hallmarks [20]." |
| Q78 | 9 | label_categories | "It contains annotation on PubMed abstracts with binary labels each of which signifies the discussion of a specific cancer hallmark." |
| Q79 | 9 | task_taxonomy | "The authors use 37 fine-grained hallmarks which are grouped into ten top-level ones." |
| Q80 | 9 | task_taxonomy | "We focus on predicting the top-level labels." |
| Q81 | 9 | data_sources | "The dataset was released with 1499 PubMed abstracts [6] and has since been expanded to 1852 abstracts [5]." |
| Q82 | 9 | stated_limitations | "Note that Peng et al. [45] discarded a control subset of 272 abstracts that do not discuss any cancer hallmark (i.e., all binary labels are false)." |
| Q83 | 9 | evaluation_metrics | "We instead adopt the original dataset and report micro F1 across the ten cancer hallmarks." |
| Q84 | 9 | data_format | "Though the original dataset provided sentence level annotation, we follow the common practice and evaluate on the abstract level [19, 60]." |
| Q85 | 9 | data_format | "We create the train/dev/test split, as they are not available previously." |
| Q86 | 9 | label_categories | "The PubMedQA dataset [25] contains a set of research questions, each with a reference text from a PubMed abstract as well as an annotated label of whether the text contains the answer to the research question (yes/maybe/no)." |
| Q87 | 9 | data_format | "We use the original train/dev/test split with 450, 50, and 500 questions, respectively." |
| Q88 | 9 | annotation_process | "The BioASQ corpus [42] contains multiple question answering tasks annotated by biomedical experts, including yes/no, factoid, list, and summary questions." |
| Q89 | 9 | task_taxonomy | "Pertaining to our objective of comparing neural language models, we focus on the the yes/no questions (Task 7b), and leave the inclusion of other tasks to future work." |
| Q90 | 9 | label_categories | "Each question is paired with a reference text containing multiple sentences from a PubMed abstract and a yes/no answer." |
| Q91 | 9 | data_format | "We use the official train/dev/test split of 670/75/140 questions." |
| Q92 | 9 | task_taxonomy | "Pretrained neural language models provide a unifying foundation for learning task-specific models." |
| Q93 | 9 | task_taxonomy | "Given an input token sequence, the language model produces a sequence of vectors in the contextual representation." |
| Q94 | 9 | task_taxonomy | "A task-specific prediction model is then layered on top to generate the final output for a task-specific application." |
| Q95 | 10 | stated_limitations | "Prior work on biomedical NLP often adopts different task-specific models and fine-tuning methods, which makes it difficult to understand the impact of an underlying pretrained language model on task performance." |
| Q96 | 10 | task_taxonomy | "In our primary investigation comparing pretraining strategies, we fix the task-specific model architecture using the standard method identifed here, to facilitate a head-to-head comparison among the pretrained neural language models." |
| Q97 | 10 | task_taxonomy | "Subsequently, we start with the same pretrained BERT model, and conduct additional investigation on the impact for the various choices in the task-specific models." |
| Q98 | 10 | evaluation_metrics | "For prior biomedical BERT models, our standard task-specific methods generally lead to comparable or better performance when compared to their published results." |
| Q99 | 10 | data_format | "An input instance is first processed by a TransformInput module which performs task-specific transformations such as appending special instance marker (e.g., [CLS]) or dummifying entity mentions for relation extraction." |
| Q100 | 10 | evaluation_metrics | "We use cross-entropy loss for classification tasks and mean-square error for regression tasks." |
| Q101 | 10 | evaluation_metrics | "We conduct hyperparameter search using the development set based on task-specific metrics." |
| Q102 | 10 | task_taxonomy | "We jointly fine-tune the parameters of the task-specific prediction layer as well as the underlying neural language model." |
| Q103 | 11 | task_taxonomy | "Many NLP applications can be formulated as a classification or regression task, wherein either individual tokens or sequences are the prediction target." |
| Q104 | 11 | task_taxonomy | "Modeling choices usually vary in two aspects: the instance representation and the prediction layer." |
| Q105 | 11 | task_taxonomy | "Given an input text span (usually a sentence), the NER task seeks to recognize mentions of entities of interest." |
| Q106 | 11 | task_taxonomy | "It is typically formulated as a sequential labeling task, where each token is assigned a tag to signify whether it is in an entity mention or not." |
| Q107 | 11 | task_taxonomy | "BIO is the standard tagging scheme that classifies each token as the beginning of an entity (B), inside an entity (I), or outside (O)." |
| Q108 | 11 | task_taxonomy | "The NER tasks in BLURB are only concerned about one entity type (in JNLPBA, all the types are merged into one)." |
| Q109 | 11 | task_taxonomy | "Prior work has also considered more complex tagging schemes such as BIOUL, where U stands for the last word of an entity and L stands for a single-word entity." |
| Q110 | 11 | task_taxonomy | "Classification is done using a simple linear layer or more sophisticated sequential labeling methods such as LSTM or conditional random field (CRF)." |
| Q111 | 11 | task_taxonomy | "Conceptually, evidence-based medical information extraction is akin to slot filling, as it tries to identify the PIO elements in an abstract describing a clinical trial." |
| Q112 | 11 | task_taxonomy | "However, it can be formulated as a sequential tagging task like NER, by classifying tokens belonging to each element." |
| Q113 | 11 | task_taxonomy | "A token may belong to more than one element, e.g., participant (P) and intervention (I)." |
| Q114 | 11 | task_taxonomy | "Existing work on relation extraction tends to focus on binary relations." |
| Q115 | 11 | task_taxonomy | "Given a pair of entity mentions in a text span (typically a sentence), the goal is to determine if the text indicates a relation for the mention pair." |
| Q116 | 11 | task_taxonomy | "There are significant variations in the entity and relation representations." |
| Q117 | 11 | task_taxonomy | "To prevent overfitting by memorizing the entity pairs, the entity tokens are often augmented with start/end markers or replaced by" |
| Q118 | 12 | data_format | "For featurization, the relation instance is either represented by a special [CLS] token, or by concatenating the mention representations." |
| Q119 | 12 | data_format | "In the latter case, if an entity mention contains multiple tokens, its representation is usually produced by pooling those of individual tokens (max or average)." |
| Q120 | 12 | data_format | "For computational efficiency, we use padding or truncation to set the input length to 128 tokens for GAD and 256 tokens for ChemProt and DDI which contain longer input sequences." |
| Q121 | 12 | task_taxonomy | "The similarity task can be formulated as a regression problem to generate a normalized score for a sentence pair." |
| Q122 | 12 | data_format | "By default, a special [SEP] token is inserted to separate the two sentences, and a special [CLS] token is prepended to the beginning to represent the pair." |
| Q123 | 12 | task_taxonomy | "For each text span and category (an abstract and a cancer hallmark in HoC), the goal is to classify whether the text belongs to the category." |
| Q124 | 12 | task_taxonomy | "For the two-way (yes/no) or three-way (yes/maybe/no) question-answering task, the encoding is similar to the sentence similarity task." |
| Q125 | 12 | data_format | "For computational efficiency, we use padding or truncation to set the input length to 512 tokens." |
| Q126 | 12 | data_sources | "For biomedical domain-specific pretraining, we generate the vocabulary and conduct pretraining using the latest collection of PubMed abstracts: 14 million abstracts, 3.2 billion words, 21 GB." |
| Q127 | 12 | data_sources | "The original collection contains over 4 billion words; we filter out any abstracts with less than 128 words to reduce noise." |
| Q128 | 12 | evaluation_metrics | "We use Adam [30] for the optimizer using a standard slanted triangular learning rate schedule with warm-up in 10% of steps and cool-down in 90% of steps." |
| Q129 | 12 | evaluation_metrics | "Specifically, the learning rate increases linearly from zero to the peak rate of 6 × 10−4 in the first 10% of steps, and then decays linearly to zero in the remaining 90% of steps." |
| Q130 | 12 | evaluation_metrics | "Training is done for 62,500 steps with batch size of 8,192, which is comparable to the computation used in previous" |
| Q131 | 13 | data_format | "The training takes about 5 days on one DGX-2 machine with 16 V100 GPUs." |
| Q132 | 13 | data_format | "We find that the cased version has similar performance to the uncased version in preliminary experiments; thus, we focus on uncased models in this study." |
| Q133 | 13 | data_format | "We use whole-word masking (WWM), with a masking rate of 15%." |
| Q134 | 13 | data_format | "BioBERT and BlueBERT conduct continual pretraining from BERT, whereas ClinicalBERT conducts continual pretraining from BioBERT; thus, they all share the same vocabulary as BERT." |
| Q135 | 13 | data_format | "Prior work in biomedical pretraining uses BERT-BASE only." |
| Q136 | 13 | stated_limitations | "BERT-LARGE appears to yield improved performance in some preliminary experiments." |
| Q137 | 13 | stated_limitations | "We leave an in-depth exploration to future work." |
| Q138 | 13 | evaluation_metrics | "For task-specific fine-tuning, we use Adam [30] with the standard slanted triangular learning rate schedule (warm-up in the first 10% of steps and cool-down in the remaining 90% of steps) and a dropout probability of 0.1." |
| Q139 | 13 | stated_limitations | "Due to random initialization of the task-specific model and drop out, the performance may vary for different random seeds, especially for small datasets like BIOSSES, BioASQ, and PubMedQA." |
| Q140 | 13 | evaluation_metrics | "We report the average scores from ten runs for BIOSSES, BioASQ, and PubMedQA, and five runs for the others." |
| Q141 | 13 | evaluation_metrics | "For all datasets, we use the development set for tuning the hyperparameters with the same range: learning rate (1e-5, 3e-5, 5e-5), batch size (16, 32) and epoch number (2–60)." |
| Q142 | 13 | stated_limitations | "Ideally, we would conduct separate hyperparameter tuning for each model on each dataset." |
| Q143 | 13 | stated_limitations | "However, this would incur a prohibitive amount of computation, as we have to enumerate all combinations of models, datasets and hyperparameters, each of which requires averaging over multiple runs with different randomization." |
| Q144 | 13 | stated_limitations | "In practice, we observe that the development performance is not very sensitive to hyperparameter selection, as long as they are in a ballpark range." |
| Q145 | 13 | evaluation_metrics | "Consequently, we focus on hyperparameter tuning using a subset of representative models such as BERT and BioBERT, and use a common set of hyperparameters for each dataset that work well for both out-domain and in-domain language models." |
| Q146 | 14 | task_taxonomy | "In this section, we conduct a thorough evaluation to assess the impact of domain-specific pretraining in biomedical NLP applications." |
| Q147 | 14 | evaluation_metrics | "First, we fix the standard task-specific model for each task in BLURB, and conduct a head-to-head comparison of domain-specific pretraining and mixed-domain pretraining." |
| Q148 | 14 | evaluation_metrics | "Next, we evaluate the impact of various pretraining options such as vocabulary, whole-word masking (WWM), and adversarial pretraining." |
| Q149 | 14 | evaluation_metrics | "Finally, we fix a pretrained BERT model and compare various modeling choices for task-specific fine-tuning." |
| Q150 | 14 | evaluation_metrics | "The BLURB score is the macro average of average test results for each of the six tasks (NER, PICO, relation extraction, sentence similarity, document classification, question answering)." |
| Q151 | 14 | evaluation_metrics | "We compare BERT models by applying them to the downstream NLP applications in BLURB." |
| Q152 | 14 | evaluation_metrics | "For each task, we conduct the same fine-tuning process using the standard task-specific model as specified in subsection 2.4." |
| Q153 | 14 | evaluation_metrics | "By conducting domain-specific pretraining from scratch, PubMedBERT consistently outperforms all the other BERT models in most biomedical NLP tasks, often by a significant margin." |
| Q154 | 14 | stated_limitations | "Models using biomedical text in pretraining generally perform better." |
| Q155 | 14 | stated_limitations | "However, mixing out-domain data in pretraining generally leads to worse performance." |
| Q156 | 14 | stated_limitations | "In particular, even though clinical notes are more relevant to the biomedical domain than general-domain text, adding them does not confer any advantage, as evident by the results of ClinicalBERT and BlueBERT." |
| Q157 | 15 | stated_limitations | "notable exception is PubMedQA, but this dataset is small, and there are relatively high variances among runs with different random seeds." |
| Q158 | 15 | evaluation_metrics | "Compared to the published results for BioBERT, SciBERT, and BlueBERT in their original papers, our results are generally comparable or better for the tasks they have been evaluated on." |
| Q159 | 15 | task_taxonomy | "To assess the impact of pretraining options on downstream applications, we conduct several ablation studies using PubMedBERT as a running example." |
| Q160 | 15 | data_format | "Using the original BERT vocabulary derived from Wikipedia & BookCorpus (by continual pretraining from the original BERT), the results are significantly worse than using an in-domain vocabulary from PubMed." |
| Q161 | 15 | evaluation_metrics | "Additionally, WWM leads to consistent improvement across the board, regardless of the vocabulary in use." |
| Q162 | 15 | data_format | "A significant advantage in using an in-domain vocabulary is that the input will be shorter in downstream tasks, as shown in Table 8, which makes learning easier." |
| Q163 | 15 | stated_limitations | "Furthermore, we found that pretraining on general-domain text provides no benefit even if we use the in-domain vocabulary; see Table 9." |
| Q164 | 15 | stated_limitations | "In sum, general-domain pretraining confers no advantage here in domain-specific pretraining." |
| Q165 | 16 | data_sources | "In our standard PubMedBERT pretraining, we used PubMed abstracts only." |
| Q166 | 16 | data_sources | "We also tried adding full-text articles from PubMed Central (PMC), with the total pretraining text increased substantially to 16.8 billion words (107 GB)." |
| Q167 | 16 | stated_limitations | "Surprisingly, this generally leads to a slight degradation in performance across the board." |
| Q168 | 17 | data_format | "Table 8. Comparison of the average input length in word pieces using general-domain vs in-domain vocabulary." |
| Q169 | 17 | evaluation_metrics | "Table 9. Evaluation of the impact of pretraining corpora and time on the performance on BLURB. In the first two columns, pretraining was first conducted on Wiki & Books, then on PubMed abstracts. All use the same amount of compute (twice as long as original BERT pretraining), except for the third column, which only uses half (same as original BERT pretraining)." |
| Q170 | 17 | evaluation_metrics | "extending pretraining for 60% longer (100K steps in total), the overall results improve and slightly outperform the standard PubMedBERT using only abstracts. We hypothesize that the reason for this behavior is two-fold. First, PMC inclusion is influenced by funding policy and differs from general PubMed distribution, and full texts generally contain more noise than abstracts. As most existing biomedical NLP tasks are based on abstracts, full texts may be slightly out-domain compared to abstracts. Moreover, even if full texts are potentially helpful, their inclusion requires additional pretraining cycles to make use of the extra information." |
| Q171 | 18 | stated_limitations | "Adversarial pretraining has been shown to be highly effective in boosting performance in general-domain applications [37]. We thus conducted adversarial pretraining in PubMedBERT and compared its performance with standard pretraining (Table 11). Surprisingly, adversarial pretraining generally leads to a slight degradation in performance, with some exceptions such as sentence similarity (BIOSSES). We hypothesize that the reason may be similar to what we observe in pretraining with full texts. Namely, adversarial training is most useful if the pretraining corpus is more diverse and relatively out-domain compared to the application tasks. We leave a more thorough evaluation of adversarial pretraining to future work." |
| Q172 | 18 | task_taxonomy | "In the above studies on pretraining methods, we fix the fine-tuning methods to the standard methods described in subsection 2.4. Next, we will study the effect of modeling choices in task-specific fine-tuning, by fixing the underlying pretrained language model to our standard PubMedBERT (WWM, PubMed vocabulary, pretrained using PubMed abstracts)." |
| Q173 | 18 | task_taxonomy | "Prior to the current success of pretraining neural language models, standard NLP approaches were often dominated by sequential labeling methods, such as conditional random fields (CRF) and more recently recurrent" |
| Q174 | 19 | task_taxonomy | "Such methods were particularly popular for named entity recognition (NER) and relation extraction." |
| Q175 | 19 | evaluation_metrics | "Comparison of linear layers vs recurrent neural networks for task-specific fine-tuning in named entity recognition (entity-level F1) and relation extraction (micro F1), all using the standard PubMedBERT." |
| Q176 | 19 | evaluation_metrics | "Comparison of entity-level F1 for biomedical named entity recognition (NER) using different tagging schemes and the standard PubMedBERT." |
| Q177 | 19 | evaluation_metrics | "Comparison of PubMedBERT performance on BLURB using standard and adversarial pretraining." |
| Q178 | 20 | task_taxonomy | "With the advent of BERT models and the self-attention mechanism, the utility of explicit sequential modeling becomes questionable." |
| Q179 | 20 | task_taxonomy | "We find that this is indeed the case for NER and relation extraction, as shown in Table 12." |
| Q180 | 20 | evaluation_metrics | "The use of a bidirectional LSTM (Bi-LSTM) does not lead to any substantial gain compared to linear layer." |
| Q181 | 20 | task_taxonomy | "We thus conducted a head-to-head comparison of the tagging schemes using three biomedical NER tasks in BLURB." |
| Q182 | 20 | evaluation_metrics | "As we can see in Table 13, the difference is minuscule, suggesting that with self-attention, the sequential nature of the tags is less essential in NER modeling." |
| Q183 | 20 | data_format | "With entity dummification, the entity mentions in question are anonymized using entity type tags such as $DRUG or $GENE." |
| Q184 | 20 | data_format | "With entity marker, special tags marking the start and end of an entity are appended to the entity mentions in question." |
| Q185 | 20 | data_format | "Relation encoding is derived from the special [CLS] token appended to the beginning of the text or the special entity start token, or by concatenating the contextual representation of the entity mentions in question." |
| Q186 | 20 | data_format | "It is a common practice to "dummify" entities (i.e., replace an entity with a generic tag such as $DRUG or $GENE)." |
| Q187 | 20 | task_taxonomy | "We thus conducted a systematic evaluation of entity dummification and relation encoding, using two relation extraction tasks in BLURB." |
| Q188 | 20 | task_taxonomy | "For entity marking, we consider three variants: dummify the entities in question; use the original text; add start and end tags to entities in question." |
| Q189 | 20 | task_taxonomy | "For relation encoding, we consider three schemes. In the [CLS] encoding introduced by the original BERT paper, the special token [CLS] is prepended to the beginning of the text span, and its contextual representation at the top layer is used as the input in the final classification." |
| Q190 | 20 | task_taxonomy | "Another standard approach concatenates the BERT encoding of the given entity mentions, each obtained by applying max pooling." |
| Q191 | 21 | data_sources | "There are a plethora of biomedical NLP datasets, especially from various shared tasks such as BioCreative [3, 29, 40, 53], BioNLP [15, 28], SemEval [2, 9, 10, 17], and BioASQ [42]." |
| Q192 | 21 | task_taxonomy | "The focus has evolved from simple tasks, such as named entity recognition, to more sophisticated tasks, such as relation extraction and question answering, and new tasks have been proposed for emerging application scenarios such as evidence-based medical information extraction [44]." |
| Q193 | 21 | stated_limitations | "However, while comprehensive benchmarks and leaderboards are available for the general domains (e.g., GLUE [57] and SuperGLUE [56]), they are still a rarity in biomedical NLP." |
| Q194 | 21 | task_taxonomy | "In this paper, inspired by prior effort towards this direction [45], we create the first leaderboard for biomedical NLP, BLURB — a comprehensive benchmark containing thirteen datasets for six tasks." |
| Q195 | 21 | task_taxonomy | "To facilitate this study, we create BLURB, a comprehensive benchmark for biomedical NLP featuring a diverse set of tasks such as named entity recognition, relation extraction, document classification, and question answering." |
| Q196 | 21 | authors_affiliations | "To accelerate research in biomedical NLP, we release our state-of-the-art biomedical BERT models and setup a leaderboard based on BLURB." |
| Q197 | 22 | stated_limitations | "Future directions include: further exploration of domain-specific pretraining strategies; incorporating more tasks in biomedical NLP; extension of the BLURB benchmark to clinical and other high-value domains." |
| Q198 | 24 | data_sources | "A corpus with multi-level annotations of patients, interventions and outcomes to support language processing for medical literature." |
| Q199 | 24 | evaluation_metrics | "Transfer Learning in Biomedical Natural Language Processing: An Evaluation of BERT and ELMo on Ten Benchmarking Datasets." |
| Q200 | 24 | task_taxonomy | "Results of the Seventh Edition of the BioASQ Challenge." |
| Q201 | 24 | task_taxonomy | "BIOSSES: a semantic sentence similarity estimation system for the biomedical domain." |
| Q202 | 24 | task_taxonomy | "Overview of BioCreative II gene mention recognition." |
| Q203 | 24 | task_taxonomy | "Drug–drug interaction extraction via hierarchical RNNs on sequence and shortest dependency paths." |
| Q204 | 24 | task_taxonomy | "Enhancing clinical concept extraction with contextual embeddings." |
| Q205 | 24 | task_taxonomy | "GLUE: A MULTI-TASK BENCHMARK AND ANALYSIS PLATFORM FOR NATURAL LANGUAGE UNDERSTANDING." |
| Q206 | 24 | task_taxonomy | "Superglue: A stickier benchmark for general-purpose language understanding systems." |

### Category Index
- **task_taxonomy**: Q2, Q7, Q8, Q9, Q10, Q13, Q22, Q24, Q25, Q34, Q35, Q36, Q38, Q44, Q45, Q46, Q48, Q49, Q79, Q80, Q89, Q92, Q93, Q94, Q96, Q97, Q102, Q103, Q104, Q105, Q106, Q107, Q108, Q109, Q110, Q111, Q112, Q113, Q114, Q115, Q116, Q117, Q121, Q123, Q124, Q146, Q159, Q172, Q173, Q174, Q178, Q179, Q181, Q187, Q188, Q189, Q190, Q192, Q194, Q195, Q200, Q201, Q202, Q203, Q204, Q205, Q206
- **data_sources**: Q1, Q5, Q6, Q14, Q17, Q18, Q20, Q23, Q30, Q42, Q53, Q54, Q56, Q57, Q58, Q59, Q64, Q68, Q70, Q71, Q77, Q81, Q126, Q127, Q165, Q166, Q191, Q198
- **data_format**: Q19, Q55, Q63, Q66, Q69, Q72, Q73, Q84, Q85, Q87, Q91, Q99, Q118, Q119, Q120, Q122, Q125, Q131, Q132, Q133, Q134, Q135, Q160, Q162, Q168, Q183, Q184, Q185, Q186
- **label_categories**: Q65, Q75, Q78, Q86, Q90
- **annotation_process**: Q60, Q74, Q88
- **evaluation_metrics**: Q3, Q52, Q61, Q76, Q83, Q98, Q100, Q101, Q128, Q129, Q130, Q138, Q140, Q141, Q145, Q147, Q148, Q149, Q150, Q151, Q152, Q153, Q158, Q161, Q169, Q170, Q175, Q176, Q177, Q180, Q182, Q199
- **stated_limitations**: Q11, Q12, Q15, Q16, Q26, Q27, Q28, Q29, Q31, Q32, Q33, Q37, Q39, Q40, Q41, Q43, Q47, Q50, Q51, Q62, Q67, Q82, Q95, Q136, Q137, Q139, Q142, Q143, Q144, Q154, Q155, Q156, Q157, Q163, Q164, Q167, Q171, Q193, Q197
- **authors_affiliations**: Q4, Q21, Q196
