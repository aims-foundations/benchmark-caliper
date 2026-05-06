I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **Biomedical Language Understanding & Reasoning Benchmark (BLURB)** is valid for use in **EU/French Pharmaceutical Regulatory NLP — BLURB Assessment**.

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

- **Name**: blurb
- **Full Name**: Biomedical Language Understanding & Reasoning Benchmark (BLURB)
- **Domain**: Biomedical natural language processing
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2021

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### 1. Input Ontology
BLURB defines its task taxonomy around six biomedical NLP categories: NER, PICO
extraction, relation extraction, sentence similarity, document classification, and
question answering [Q48, Q194, Q195]. These task types are modeled after general-domain
benchmarks like GLUE and SuperGLUE [Q36, Q205, Q206] and represent the paper's
understanding of core biomedical NLP competencies. Within NER, all entity types are
collapsed to a single class per dataset (e.g., chemical, disease, gene) [Q108]. Relation
extraction focuses on binary or multi-class classification over entity pairs in single
sentences [Q114, Q115]. Question answering is explicitly restricted to yes/no and
three-way classification formats [Q124], with more complex list and summary tasks
excluded [Q49, Q50, Q51]. The benchmark is intentionally scoped to PubMed-based
biomedical applications, deferring clinical and other high-value verticals to future
work [Q46]. Task evolution is acknowledged ("from simple tasks, such as named entity
recognition, to more sophisticated tasks, such as relation extraction and question
answering" [Q192]) but the taxonomy does not include any regulatory document genre
(SmPCs, patient information leaflets, CTD modules, patent claims) or regulatory-specific
task types such as cross-document regulatory consistency checking. The benchmark
further acknowledges limited coverage relative to recent work [Q40] and that prior
studies use heterogeneous task selections, making cross-study comparison difficult [Q37].

### 2. Input Content
All NER, relation extraction, PICO, and QA datasets are drawn from PubMed abstracts
[Q53, Q54, Q56, Q57, Q58, Q59, Q64, Q68, Q70, Q71, Q77, Q81], with the pretraining
corpus itself comprising 14 million PubMed abstracts totaling 3.2 billion words [Q126,
Q127]. Shared-task corpora from BioCreative, BioNLP, SemEval, and BioASQ dominate the
collection [Q191]. BLURB deliberately excludes MIMIC-based clinical notes present in
the earlier BLUE benchmark, on the grounds that "clinical notes differ substantially
from biomedical literature" [Q43] and that separate benchmarks for the two domains are
preferable [Q44]. The EBM PICO corpus sources abstracts specifically from clinical
trials [Q59]; ChemProt covers chemical-protein interactions in research abstracts [Q64];
BIOSSES provides 100 sentence pairs drawn from PubMed [Q74]. An experiment expanding
pretraining to PubMed Central full-text articles increased the corpus to 16.8 billion
words [Q166] but produced marginal or negative effects [Q167], attributed in part to
distributional differences between full texts and abstracts [Q170]. The ChemProt
training and development sets are expanded by assigning false labels to unlabeled
chemical-protein pairs [Q66]. GAD uses semi-automatically generated positive and
negative examples from a gene-disease association archive [Q70, Q71, Q72]. No
French-language source, no regulatory submission document, and no EU pharmaceutical
nomenclature corpus appears anywhere in the data collection.

### 3. Input Form
All inputs are English-language text drawn from PubMed [Q1, Q46, Q126]. Preprocessing
pipelines apply task-specific transformations including special token insertion ([CLS],
[SEP]), entity dummification for relation extraction [Q99, Q183, Q184, Q186], and
sequence-length management via padding or truncation: 128 tokens for GAD, 256 for
ChemProt and DDI, 512 for QA tasks [Q120, Q125]. PubMedBERT generates its vocabulary
from PubMed text rather than general-domain corpora [Q126], producing shorter tokenized
inputs for biomedical terminology relative to BERT [Q162, Q168]; by contrast, continually
pretrained models (BioBERT, BlueBERT, ClinicalBERT) retain the original BERT vocabulary
derived from Wikipedia and BookCorpus [Q134], which fragments common biomedical terms
(e.g., naloxone into four subword pieces, acetyltransferase into seven [Q29]). Whole-word
masking is applied at 15% [Q133]; cased and uncased model variants show negligible
performance difference [Q132]. Training required approximately five days on 16 V100 GPUs
[Q131]. The benchmark is exclusively monolingual English; no multilingual processing,
no non-Latin script handling, and no French-language variant is documented or
contemplated.

### 4. Output Ontology
Task-specific prediction layers are layered atop the pretrained language model [Q93,
Q94]. The label space varies by task: BIO or BIOUL token-level tags for NER [Q107,
Q109]; five-way plus false-class classification for ChemProt relation extraction [Q65];
binary yes/no for BioASQ QA [Q90]; three-way yes/maybe/no for PubMedQA [Q86]; binary
cancer hallmark indicators for HoC [Q78]; and a 0–4 continuous regression score for
BIOSSES sentence similarity [Q75]. The BLURB summary score is the macro average of
per-task-type averages, deliberately grouping datasets by task type before averaging
to avoid over-weighting NER [Q52, Q150]. NER entity categories cover genes, chemicals,
diseases, and molecular biology entities (protein, DNA, RNA, cell line, cell type) [Q58,
Q108], with no label space for regulatory-specific entity types (INNs, ATC codes,
excipient nomenclature, posology expressions, EMA-template contraindication qualifiers).
The BIOSSES regression score operationalizes general biomedical semantic proximity
[Q74, Q75, Q76] — not regulatory equivalence. The output ontology thus reflects
research-oriented biomedical NLP norms with no structural accommodation for the
legal-consequence distinctions (dose thresholds, population qualifiers) that govern
EU regulatory compliance determination.

### 5. Output Content
Annotation provenance varies across datasets and is unevenly documented. The EBM PICO
dataset exhibits a notable quality stratification: "The training and development sets
were labeled by Amazon Mechanical Turkers, whereas the test set was labeled by Upwork
contributors with prior medical training" [Q60]. BIOSSES similarity scores are produced
by "five expert-level annotators" [Q74], providing an inter-annotator basis for the
regression labels. BioASQ annotations are produced "by biomedical experts" [Q88].
Inter-annotator agreement (IAA) statistics, annotator demographics beyond general
descriptors, and structured annotation protocols are not systematically reported across
the benchmark as a whole. Hyperparameter search is conducted on development sets [Q101,
Q141] but is acknowledged to use a common fixed range across models rather than
per-model per-dataset tuning [Q142, Q143, Q145]. Variance instability on small datasets
(BIOSSES, BioASQ, PubMedQA) is addressed by averaging over ten runs rather than
structural annotation design [Q139, Q140]. No annotator population includes regulatory
affairs specialists, legal experts, or individuals operating under EMA/ANSM normative
frameworks; the gap between biomedical research community annotation norms and
regulatory compliance judgments is NOT DOCUMENTED in the paper.

### 6. Output Form
The primary evaluation metric is the BLURB score, defined as "the macro average of
average test results for each of the six tasks" [Q150]. Task-specific metrics include
entity-level F1 for NER [Q176], word-level F1 per PIO element for PICO [Q61], micro
F1 for ChemProt and HoC [Q83], Pearson correlation for BIOSSES [Q76], and accuracy
for QA tasks [Q100]. Models are fine-tuned using cross-entropy loss for classification
and mean-square error for regression [Q100], with a slanted triangular learning rate
schedule and 0.1 dropout [Q138]. Evaluation compares BERT model variants using the
same fine-tuning process for each task [Q151, Q152], and compares favorably to
published BioBERT, SciBERT, and BlueBERT results [Q158]. Ablation studies report
entity-level F1 across tagging schemes [Q176, Q182] and micro F1 across linear vs.
recurrent architectures [Q175, Q180]. All metrics are aggregate text-classification
or regression scores; no confidence-calibration metrics, threshold-sensitivity
analyses, or human-review-triggering decision boundaries are documented. Pretrained
and task-specific models are publicly released alongside the leaderboard [Q3, Q196].


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we compile a comprehensive biomedical NLP benchmark from publicly-available datasets." |
| Q2 | 1 | input_ontology | "we discover that some common practices are unnecessary with BERT models, such as using complex tagging schemes in named entity recognition (NER)." |
| Q3 | 1 | output_form | "we have released our state-of-the-art pretrained and task-specific models for the community, and created a leaderboard featuring our BLURB benchmark (short for Biomedical Language Understanding & Reasoning Benchmark)." |
| Q4 | 1 | output_content | "Yu Gu, Robert Tinn, Hao Cheng, Michael Lucas, Naoto Usuyama, Xiaodong Liu, Tristan Naumann, Jianfeng Gao, and Hoifung Poon, Microsoft Research" |
| Q5 | 1 | input_content | "Existing pretraining work typically focuses on the newswire and Web domains." |
| Q6 | 1 | input_content | "the original BERT model was trained on Wikipedia and BookCorpus [62], and subsequent efforts have focused on crawling additional text from the Web to power even larger-scale pretraining [39, 50]." |
| Q7 | 2 | input_content | "In specialized domains like biomedicine, past work has shown that using in-domain text can provide additional gains over general-domain language models [8, 34, 45]." |
| Q8 | 2 | input_content | "However, a prevailing assumption is that out-domain text is still helpful and previous work typically adopts a mixed-domain approach, e.g., by starting domain-specific pretraining from an existing general-domain language model (Figure 1 top)." |
| Q9 | 2 | input_content | "We observe that mixed-domain pretraining such as continual pretraining can be viewed as a form of transfer learning in itself, where the source domain is general text, such as newswire and the Web, and the target domain is specialized text such as biomedical papers." |
| Q10 | 2 | input_content | "Based on the rich literature of multi-task learning and transfer learning [4, 13, 38, 59], successful transfer learning occurs when the target data is scarce and the source domain is highly relevant to the target one." |
| Q11 | 2 | input_content | "For domains with abundant unlabeled text such as biomedicine, it is unclear that domain-specific pretraining can benefit by transfer from general domains." |
| Q12 | 2 | input_content | "In fact, the majority of general domain text is substantively different from biomedical text, raising the prospect of negative transfer that actually hinders the target performance." |
| Q13 | 4 | input_content | "In this paper, we will use biomedicine as a running example in our study of domain-specific pretraining. In other words, biomedical text is considered in-domain, while others are regarded as out-domain." |
| Q14 | 4 | input_content | "Intuitively, using in-domain text in pretraining should help with domain-specific applications. Indeed, prior work has shown that pretraining with PubMed text leads to better performance in biomedical NLP tasks [8, 34, 45]." |
| Q15 | 4 | input_content | "The main question is whether pretraining should include text from other domains. The prevailing assumption is that pretraining can always benefit from more text, including out-domain text. In fact, none of the prior biomedical-related BERT models have been pretrained using purely biomedical text [8, 34, 45]." |
| Q16 | 4 | input_content | "Here, we challenge this assumption and show that domain-specific pretraining from scratch can be superior to mixed-domain pretraining for downstream applications." |
| Q17 | 4 | input_content | "The standard approach to pretraining a biomedical BERT model conducts continual pretraining of a general-domain pretrained model, as exemplified by BioBERT [34]. Specifically, this approach would initialize with the standard BERT model [16], pretrained using Wikipedia and BookCorpus. It then continues the pretraining process with MLM and NSP using biomedical text." |
| Q18 | 4 | input_content | "In the case of BioBERT, continual pretraining is conducted using PubMed abstracts and PubMed Central full text articles. BlueBERT [45] uses both PubMed text and de-identified clinical notes from MIMIC-III [26]." |
| Q19 | 4 | input_form | "Note that in the continual pretraining approach, the vocabulary is the same as the original BERT model, in this case the one generated from Wikipedia and BookCorpus. While convenient, this is a major disadvantage for this approach, as the vocabulary is not representative of the target biomedical domain." |
| Q20 | 4 | input_content | "Compared to the other biomedical-related pretraining efforts, SciBERT [8] is a notable exception as it generates the vocabulary and pretrains from scratch, using biomedicine and computer science as representatives for scientific literature. However, from the perspective of biomedical applications, SciBERT still adopts the mixed-domain pretraining approach, as computer science text is clearly out-domain." |
| Q21 | 4 | output_content | "Gu, Tinn, Cheng, et al." |
| Q22 | 5 | input_content | "The mixed-domain pretraining approach makes sense if the target application domain has little text of its own, and can thereby benefit from pretraining using related domains." |
| Q23 | 5 | input_content | "However, this is not the case for biomedicine, which has over thirty million abstracts in PubMed, and adds over a million each year." |
| Q24 | 5 | input_content | "We thus hypothesize that domain-specific pretraining from scratch is a better strategy for biomedical language model pretraining." |
| Q25 | 5 | input_form | "A major advantage of domain-specific pretraining from scratch stems from having an in-domain vocabulary." |
| Q26 | 5 | input_form | "BERT models using continual pretraining are stuck with the original vocabulary from the general-domain corpora, which does not contain many common biomedical terms." |
| Q27 | 5 | input_form | "Even for SciBERT, which generates its vocabulary partially from biomedical text, the deficiency compared to a purely biomedical vocabulary is substantial." |
| Q28 | 5 | input_form | "As a result, standard BERT models are forced to divert parametrization capacity and training bandwidth to model biomedical terms using fragmented subwords." |
| Q29 | 5 | input_form | "For example, naloxone, a common medical term, is divided into four pieces ([na, ##lo, ##xon, ##e]) by BERT, and acetyltransferase is shattered into seven pieces ([ace, ##ty, ##lt, ##ran, ##sf, ##eras, ##e]) by BERT." |
| Q30 | 5 | input_content | "Another advantage of domain-specific pretraining from scratch is that the language model is trained using purely in-domain data." |
| Q31 | 5 | input_content | "For example, SciBERT pretraining has to balance optimizing for biomedical text and computer science text, the latter of which is unlikely to be beneficial for biomedical applications." |
| Q32 | 5 | input_content | "Continual pretraining, on the other hand, may potentially recover from out-domain modeling, though not completely." |
| Q33 | 6 | input_content | "that continual pretraining may not be able to completely undo suboptimal initialization from the general-domain language model." |
| Q34 | 6 | input_content | "In our experiments, we show that domain-specific pretraining with in-domain vocabulary confers clear advantages over mixed-domain pretraining, be it continual pretraining of general-domain language models, or pretraining on mixed-domain text." |
| Q35 | 6 | input_ontology | "The ultimate goal of language model pretraining is to improve performance on a wide range of downstream applications." |
| Q36 | 6 | input_ontology | "In general-domain NLP, the creation of comprehensive benchmarks, such as GLUE [56, 57], greatly accelerates advances in language model pretraining by enabling head-to-head comparisons among pretrained language models." |
| Q37 | 6 | input_ontology | "In contrast, prior work on biomedical pretraining tends to use different tasks and datasets for downstream evaluation, as shown in Table 2." |
| Q38 | 6 | input_ontology | "To the best of our knowledge, BLUE [45] is the first attempt to create an NLP benchmark in the biomedical domain." |
| Q39 | 6 | input_ontology | "We aim to improve on its design by addressing some of its limitations." |
| Q40 | 6 | input_ontology | "First, BLUE has limited coverage of biomedical applications used in other recent work on biomedical language models, as shown in Table 2." |
| Q41 | 6 | input_ontology | "For example, it does not include any question-answering task." |
| Q42 | 6 | input_content | "More importantly, BLUE mixes PubMed-based biomedical applications (six datasets such as BC5, ChemProt, and HoC) with MIMIC-based clinical applications (four datasets such as i2b2 and MedNLI)." |
| Q43 | 6 | input_content | "Clinical notes differ substantially from biomedical literature, to the extent that we observe BERT models pretrained on clinical notes perform poorly on biomedical tasks, similar to the standard BERT." |
| Q44 | 6 | input_ontology | "Consequently, it is advantageous to create separate benchmarks for these two domains." |
| Q45 | 6 | input_ontology | "To facilitate investigations of biomedical language model pretraining and help accelerate progress in biomedical NLP, we create a new benchmark, the Biomedical Language Understanding & Reasoning Benchmark (BLURB)." |
| Q46 | 6 | input_ontology | "We focus on PubMed-based biomedical applications, and leave the exploration of the clinical domain, and other high-value verticals to future work." |
| Q47 | 7 | input_ontology | "prior work, we prioritize the selection of datasets used in recent work on biomedical language models, and will explore the addition of other datasets in future work." |
| Q48 | 7 | input_ontology | "BLURB is comprised of a comprehensive set of biomedical NLP tasks from publicly available datasets, including named entity recognition (NER), evidence-based medical information extraction (PICO), relation extraction, sentence similarity, document classification, and question answering." |
| Q49 | 7 | input_ontology | "For question answering, prior work has considered both classification tasks (e.g., whether a reference text contains the answer to a given question) and more complex tasks such as list and summary [42]." |
| Q50 | 7 | input_ontology | "The latter types often require additional engineering effort that are not relevant to evaluating neural language models." |
| Q51 | 7 | input_ontology | "For simplicity, we focus on the classification tasks such as yes/no question-answering in BLURB, and leave the inclusion of more complex question-answering to future work." |
| Q52 | 7 | output_form | "To compute a summary score for BLURB, the simplest way is to report the average score among all tasks. However, this may place undue emphasis on simpler tasks such as NER for which there are many existing datasets. Therefore, we group the datasets by their task types, compute the average score for each task type, and report the macro average among the task types." |
| Q53 | 7 | input_content | "The BioCreative V Chemical-Disease Relation corpus [35] was created for evaluating relation extraction of drug-disease interactions, but is frequently used as a NER corpus for detecting chemical (drug) and disease entities." |
| Q54 | 7 | input_content | "The dataset consists of 1500 PubMed abstracts broken into three even splits for training, development, and test." |
| Q55 | 7 | input_form | "We use a pre-processed version of this dataset generated by Crichton et al. [14], discard the relation labels, and train NER models for chemical (BC5-Chemical) and disease (BC5-Disease) separately." |
| Q56 | 8 | input_content | "NCBI-Disease. The Natural Center for Biotechnology Information Disease corpus [18] contains 793 PubMed abstracts with 6892 annotated disease mentions linked to 790 distinct disease entities. We use a pre-processed set of train, development, test splits generated by Crichton et al. [14]." |
| Q57 | 8 | input_content | "BC2GM. The Biocreative II Gene Mention corpus [53] consists of sentences from PubMed abstracts with manually labeled gene and alternative gene entities. Following prior work, we focus on the gene entity annotation. In its original form, BC2GM contains 15000 train and 5000 test sentences. We use a pre-processed version of the dataset generated by Crichton et al. [14], which carves out 2500 sentences from the training data for development." |
| Q58 | 8 | input_content | "JNLPBA. The Joint Workshop on Natural Language Processing in Biomedicine and its Applications shared task [27] is a NER corpus on PubMed abstracts. The entity types are chosen for molecular biology applications: protein, DNA, RNA, cell line, and cell type. Some of the entity type distinctions are not very meaningful. For example, a gene mention often refers to both the DNA and gene products such as the RNA and protein. Following prior work that evaluates on this dataset [34], we ignore the type distinction and focus on detecting the entity mentions. We use the same train, development, and test splits as in Crichton et al. [14]." |
| Q59 | 8 | input_content | "EBM PICO. The Evidence-Based Medicine corpus [44] contains PubMed abstracts on clinical trials, where each abstract is annotated with P, I, and O in PICO: Participants (e.g., diabetic patients), Intervention (e.g., insulin), Comparator (e.g., placebo) and Outcome (e.g., blood glucose levels). Comparator (C) labels are omitted as they are standard in clinical trials: placebo for passive control and standard of care for active control. There are 4300, 500, and 200 abstracts in training, development, and test, respectively." |
| Q60 | 8 | output_content | "The training and development sets were labeled by Amazon Mechanical Turkers, whereas the test set was labeled by Upwork contributors with prior medical training." |
| Q61 | 8 | output_form | "EBM PICO provides labels at the word level for each PIO element. For each of the PIO elements in an abstract, we tally the F1 score at the word level, and then compute the final score as the average among PIO elements in the dataset." |
| Q62 | 8 | input_content | "Occasionally, two PICO elements might overlap with each other (e.g., a participant span might contain within it an intervention span). In EBM-PICO, about 3% of the PIO words are in the overlap." |
| Q63 | 8 | input_form | "Note that the dataset released along with SciBERT appears to remove the overlapping words from the larger span (e.g., the participant span as mentioned above). We instead use the original dataset [44] and their scripts for preprocessing and evaluation." |
| Q64 | 8 | input_content | "ChemProt. The Chemical Protein Interaction corpus [31] consists of PubMed abstracts annotated with chemical-protein interactions between chemical and protein entities. There are 23 interactions organized in a hierarchy, with 10 high-level interactions (including NONE). The vast majority of relation instances in ChemProt are within single sentences. Following prior work [8, 34], we only consider sentence-level instances." |
| Q65 | 8 | output_ontology | "We follow the ChemProt authors' suggestions and focus on classifying five high-level interactions — UPREGULATOR (CPR : 3), DOWNREGULATOR (CPR : 4), AGONIST (CPR : 5), ANTAGONIST (CPR : 6), SUBSTRATE (CPR : 9) — as well as everything else (false)." |
| Q66 | 8 | input_form | "The ChemProt annotation is not exhaustive for all chemical-protein pairs. Following previous work [34, 45], we expand the training and development sets by assigning a false label for all chemical-protein pairs that occur in a training or development sentence, but do not have an explicit label in the ChemProt corpus." |
| Q67 | 8 | output_content | "Note that prior work uses slightly different label expansion of the test data. To facilitate head-to-head comparison, we will provide instructions for reproducing the test set in BLURB from the original dataset." |
| Q68 | 8 | input_content | "DDI. The Drug-Drug Interaction corpus [21] was created to facilitate research on pharmaceutical information extraction, with a particular focus on pharmacovigilance. It contains sentence-level annotation of drug-drug interactions on PubMed abstracts. Note that some prior work [45, 61] discarded 90 training files that the authors" |
| Q69 | 9 | input_form | "We instead use the original dataset and produce our train/dev/test split of 624/90/191 files." |
| Q70 | 9 | input_content | "The Genetic Association Database corpus [11] was created semi-automatically using the Genetic Association Archive." |
| Q71 | 9 | input_content | "Specifically, the archive contains a list of gene-disease associations, with the corresponding sentences in the PubMed abstracts reporting the association studies." |
| Q72 | 9 | input_form | "Bravo et al. [11] used a biomedical NER tool to identify gene and disease mentions, and create the positive examples from the annotated sentences in the archive, and negative examples from gene-disease co-occurrences that were not annotated in the archive." |
| Q73 | 9 | input_form | "We use an existing preprocessed version of GAD and its corresponding train/dev/test split created by Lee et al. [34]." |
| Q74 | 9 | output_content | "The Sentence Similarity Estimation System for the Biomedical Domain [54] contains 100 pairs of PubMed sentences each of which is annotated by five expert-level annotators with an estimated similarity score in the range from 0 (no relation) to 4 (equivalent meanings)." |
| Q75 | 9 | output_ontology | "It is a regression task, with the average score as the final annotation." |
| Q76 | 9 | output_form | "We use the same train/dev/test split in Peng et al. [45] and use Pearson correlation for evaluation." |
| Q77 | 9 | input_content | "The Hallmarks of Cancer corpus was motivated by the pioneering work on cancer hallmarks [20]." |
| Q78 | 9 | output_ontology | "It contains annotation on PubMed abstracts with binary labels each of which signifies the discussion of a specific cancer hallmark." |
| Q79 | 9 | output_ontology | "The authors use 37 fine-grained hallmarks which are grouped into ten top-level ones." |
| Q80 | 9 | output_ontology | "We focus on predicting the top-level labels." |
| Q81 | 9 | input_content | "The dataset was released with 1499 PubMed abstracts [6] and has since been expanded to 1852 abstracts [5]." |
| Q82 | 9 | output_content | "Note that Peng et al. [45] discarded a control subset of 272 abstracts that do not discuss any cancer hallmark (i.e., all binary labels are false)." |
| Q83 | 9 | output_form | "We instead adopt the original dataset and report micro F1 across the ten cancer hallmarks." |
| Q84 | 9 | input_form | "Though the original dataset provided sentence level annotation, we follow the common practice and evaluate on the abstract level [19, 60]." |
| Q85 | 9 | input_form | "We create the train/dev/test split, as they are not available previously." |
| Q86 | 9 | output_ontology | "The PubMedQA dataset [25] contains a set of research questions, each with a reference text from a PubMed abstract as well as an annotated label of whether the text contains the answer to the research question (yes/maybe/no)." |
| Q87 | 9 | input_form | "We use the original train/dev/test split with 450, 50, and 500 questions, respectively." |
| Q88 | 9 | output_content | "The BioASQ corpus [42] contains multiple question answering tasks annotated by biomedical experts, including yes/no, factoid, list, and summary questions." |
| Q89 | 9 | input_ontology | "Pertaining to our objective of comparing neural language models, we focus on the the yes/no questions (Task 7b), and leave the inclusion of other tasks to future work." |
| Q90 | 9 | output_ontology | "Each question is paired with a reference text containing multiple sentences from a PubMed abstract and a yes/no answer." |
| Q91 | 9 | input_form | "We use the official train/dev/test split of 670/75/140 questions." |
| Q92 | 9 | input_ontology | "Pretrained neural language models provide a unifying foundation for learning task-specific models." |
| Q93 | 9 | output_ontology | "Given an input token sequence, the language model produces a sequence of vectors in the contextual representation." |
| Q94 | 9 | output_ontology | "A task-specific prediction model is then layered on top to generate the final output for a task-specific application." |
| Q95 | 10 | output_form | "Prior work on biomedical NLP often adopts different task-specific models and fine-tuning methods, which makes it difficult to understand the impact of an underlying pretrained language model on task performance." |
| Q96 | 10 | output_form | "In our primary investigation comparing pretraining strategies, we fix the task-specific model architecture using the standard method identifed here, to facilitate a head-to-head comparison among the pretrained neural language models." |
| Q97 | 10 | output_form | "Subsequently, we start with the same pretrained BERT model, and conduct additional investigation on the impact for the various choices in the task-specific models." |
| Q98 | 10 | output_form | "For prior biomedical BERT models, our standard task-specific methods generally lead to comparable or better performance when compared to their published results." |
| Q99 | 10 | input_form | "An input instance is first processed by a TransformInput module which performs task-specific transformations such as appending special instance marker (e.g., [CLS]) or dummifying entity mentions for relation extraction." |
| Q100 | 10 | output_form | "We use cross-entropy loss for classification tasks and mean-square error for regression tasks." |
| Q101 | 10 | output_form | "We conduct hyperparameter search using the development set based on task-specific metrics." |
| Q102 | 10 | output_form | "We jointly fine-tune the parameters of the task-specific prediction layer as well as the underlying neural language model." |
| Q103 | 11 | output_ontology | "Many NLP applications can be formulated as a classification or regression task, wherein either individual tokens or sequences are the prediction target." |
| Q104 | 11 | output_ontology | "Modeling choices usually vary in two aspects: the instance representation and the prediction layer." |
| Q105 | 11 | input_ontology | "Given an input text span (usually a sentence), the NER task seeks to recognize mentions of entities of interest." |
| Q106 | 11 | output_ontology | "It is typically formulated as a sequential labeling task, where each token is assigned a tag to signify whether it is in an entity mention or not." |
| Q107 | 11 | output_ontology | "BIO is the standard tagging scheme that classifies each token as the beginning of an entity (B), inside an entity (I), or outside (O)." |
| Q108 | 11 | output_ontology | "The NER tasks in BLURB are only concerned about one entity type (in JNLPBA, all the types are merged into one)." |
| Q109 | 11 | output_ontology | "Prior work has also considered more complex tagging schemes such as BIOUL, where U stands for the last word of an entity and L stands for a single-word entity." |
| Q110 | 11 | output_ontology | "Classification is done using a simple linear layer or more sophisticated sequential labeling methods such as LSTM or conditional random field (CRF)." |
| Q111 | 11 | input_ontology | "Conceptually, evidence-based medical information extraction is akin to slot filling, as it tries to identify the PIO elements in an abstract describing a clinical trial." |
| Q112 | 11 | output_ontology | "However, it can be formulated as a sequential tagging task like NER, by classifying tokens belonging to each element." |
| Q113 | 11 | output_ontology | "A token may belong to more than one element, e.g., participant (P) and intervention (I)." |
| Q114 | 11 | input_ontology | "Existing work on relation extraction tends to focus on binary relations." |
| Q115 | 11 | input_ontology | "Given a pair of entity mentions in a text span (typically a sentence), the goal is to determine if the text indicates a relation for the mention pair." |
| Q116 | 11 | output_ontology | "There are significant variations in the entity and relation representations." |
| Q117 | 11 | input_form | "To prevent overfitting by memorizing the entity pairs, the entity tokens are often augmented with start/end markers or replaced by" |
| Q118 | 12 | input_form | "For featurization, the relation instance is either represented by a special [CLS] token, or by concatenating the mention representations." |
| Q119 | 12 | input_form | "In the latter case, if an entity mention contains multiple tokens, its representation is usually produced by pooling those of individual tokens (max or average)." |
| Q120 | 12 | input_form | "For computational efficiency, we use padding or truncation to set the input length to 128 tokens for GAD and 256 tokens for ChemProt and DDI which contain longer input sequences." |
| Q121 | 12 | output_ontology | "The similarity task can be formulated as a regression problem to generate a normalized score for a sentence pair." |
| Q122 | 12 | input_form | "By default, a special [SEP] token is inserted to separate the two sentences, and a special [CLS] token is prepended to the beginning to represent the pair." |
| Q123 | 12 | input_ontology | "For each text span and category (an abstract and a cancer hallmark in HoC), the goal is to classify whether the text belongs to the category." |
| Q124 | 12 | input_ontology | "For the two-way (yes/no) or three-way (yes/maybe/no) question-answering task, the encoding is similar to the sentence similarity task." |
| Q125 | 12 | input_form | "For computational efficiency, we use padding or truncation to set the input length to 512 tokens." |
| Q126 | 12 | input_content | "For biomedical domain-specific pretraining, we generate the vocabulary and conduct pretraining using the latest collection of PubMed abstracts: 14 million abstracts, 3.2 billion words, 21 GB." |
| Q127 | 12 | input_content | "The original collection contains over 4 billion words; we filter out any abstracts with less than 128 words to reduce noise." |
| Q128 | 12 | output_form | "We use Adam [30] for the optimizer using a standard slanted triangular learning rate schedule with warm-up in 10% of steps and cool-down in 90% of steps." |
| Q129 | 12 | output_form | "Specifically, the learning rate increases linearly from zero to the peak rate of 6 × 10−4 in the first 10% of steps, and then decays linearly to zero in the remaining 90% of steps." |
| Q130 | 12 | output_form | "Training is done for 62,500 steps with batch size of 8,192, which is comparable to the computation used in previous" |
| Q131 | 13 | input_form | "The training takes about 5 days on one DGX-2 machine with 16 V100 GPUs." |
| Q132 | 13 | input_form | "We find that the cased version has similar performance to the uncased version in preliminary experiments; thus, we focus on uncased models in this study." |
| Q133 | 13 | input_form | "We use whole-word masking (WWM), with a masking rate of 15%." |
| Q134 | 13 | input_form | "BioBERT and BlueBERT conduct continual pretraining from BERT, whereas ClinicalBERT conducts continual pretraining from BioBERT; thus, they all share the same vocabulary as BERT." |
| Q135 | 13 | input_form | "Prior work in biomedical pretraining uses BERT-BASE only." |
| Q136 | 13 | output_form | "BERT-LARGE appears to yield improved performance in some preliminary experiments." |
| Q137 | 13 | output_form | "We leave an in-depth exploration to future work." |
| Q138 | 13 | output_form | "For task-specific fine-tuning, we use Adam [30] with the standard slanted triangular learning rate schedule (warm-up in the first 10% of steps and cool-down in the remaining 90% of steps) and a dropout probability of 0.1." |
| Q139 | 13 | output_content | "Due to random initialization of the task-specific model and drop out, the performance may vary for different random seeds, especially for small datasets like BIOSSES, BioASQ, and PubMedQA." |
| Q140 | 13 | output_form | "We report the average scores from ten runs for BIOSSES, BioASQ, and PubMedQA, and five runs for the others." |
| Q141 | 13 | output_form | "For all datasets, we use the development set for tuning the hyperparameters with the same range: learning rate (1e-5, 3e-5, 5e-5), batch size (16, 32) and epoch number (2–60)." |
| Q142 | 13 | output_form | "Ideally, we would conduct separate hyperparameter tuning for each model on each dataset." |
| Q143 | 13 | output_form | "However, this would incur a prohibitive amount of computation, as we have to enumerate all combinations of models, datasets and hyperparameters, each of which requires averaging over multiple runs with different randomization." |
| Q144 | 13 | output_form | "In practice, we observe that the development performance is not very sensitive to hyperparameter selection, as long as they are in a ballpark range." |
| Q145 | 13 | output_form | "Consequently, we focus on hyperparameter tuning using a subset of representative models such as BERT and BioBERT, and use a common set of hyperparameters for each dataset that work well for both out-domain and in-domain language models." |
| Q146 | 14 | input_ontology | "In this section, we conduct a thorough evaluation to assess the impact of domain-specific pretraining in biomedical NLP applications." |
| Q147 | 14 | output_form | "First, we fix the standard task-specific model for each task in BLURB, and conduct a head-to-head comparison of domain-specific pretraining and mixed-domain pretraining." |
| Q148 | 14 | output_form | "Next, we evaluate the impact of various pretraining options such as vocabulary, whole-word masking (WWM), and adversarial pretraining." |
| Q149 | 14 | output_form | "Finally, we fix a pretrained BERT model and compare various modeling choices for task-specific fine-tuning." |
| Q150 | 14 | output_form | "The BLURB score is the macro average of average test results for each of the six tasks (NER, PICO, relation extraction, sentence similarity, document classification, question answering)." |
| Q151 | 14 | output_form | "We compare BERT models by applying them to the downstream NLP applications in BLURB." |
| Q152 | 14 | output_form | "For each task, we conduct the same fine-tuning process using the standard task-specific model as specified in subsection 2.4." |
| Q153 | 14 | output_form | "By conducting domain-specific pretraining from scratch, PubMedBERT consistently outperforms all the other BERT models in most biomedical NLP tasks, often by a significant margin." |
| Q154 | 14 | input_content | "Models using biomedical text in pretraining generally perform better." |
| Q155 | 14 | input_content | "However, mixing out-domain data in pretraining generally leads to worse performance." |
| Q156 | 14 | input_content | "In particular, even though clinical notes are more relevant to the biomedical domain than general-domain text, adding them does not confer any advantage, as evident by the results of ClinicalBERT and BlueBERT." |
| Q157 | 15 | output_content | "notable exception is PubMedQA, but this dataset is small, and there are relatively high variances among runs with different random seeds." |
| Q158 | 15 | output_form | "Compared to the published results for BioBERT, SciBERT, and BlueBERT in their original papers, our results are generally comparable or better for the tasks they have been evaluated on." |
| Q159 | 15 | input_ontology | "To assess the impact of pretraining options on downstream applications, we conduct several ablation studies using PubMedBERT as a running example." |
| Q160 | 15 | input_form | "Using the original BERT vocabulary derived from Wikipedia & BookCorpus (by continual pretraining from the original BERT), the results are significantly worse than using an in-domain vocabulary from PubMed." |
| Q161 | 15 | output_form | "Additionally, WWM leads to consistent improvement across the board, regardless of the vocabulary in use." |
| Q162 | 15 | input_form | "A significant advantage in using an in-domain vocabulary is that the input will be shorter in downstream tasks, as shown in Table 8, which makes learning easier." |
| Q163 | 15 | input_content | "Furthermore, we found that pretraining on general-domain text provides no benefit even if we use the in-domain vocabulary; see Table 9." |
| Q164 | 15 | input_content | "In sum, general-domain pretraining confers no advantage here in domain-specific pretraining." |
| Q165 | 16 | input_content | "In our standard PubMedBERT pretraining, we used PubMed abstracts only." |
| Q166 | 16 | input_content | "We also tried adding full-text articles from PubMed Central (PMC), with the total pretraining text increased substantially to 16.8 billion words (107 GB)." |
| Q167 | 16 | input_content | "Surprisingly, this generally leads to a slight degradation in performance across the board." |
| Q168 | 17 | input_form | "Table 8. Comparison of the average input length in word pieces using general-domain vs in-domain vocabulary." |
| Q169 | 17 | output_form | "Table 9. Evaluation of the impact of pretraining corpora and time on the performance on BLURB. In the first two columns, pretraining was first conducted on Wiki & Books, then on PubMed abstracts. All use the same amount of compute (twice as long as original BERT pretraining), except for the third column, which only uses half (same as original BERT pretraining)." |
| Q170 | 17 | input_content | "extending pretraining for 60% longer (100K steps in total), the overall results improve and slightly outperform the standard PubMedBERT using only abstracts. We hypothesize that the reason for this behavior is two-fold. First, PMC inclusion is influenced by funding policy and differs from general PubMed distribution, and full texts generally contain more noise than abstracts. As most existing biomedical NLP tasks are based on abstracts, full texts may be slightly out-domain compared to abstracts. Moreover, even if full texts are potentially helpful, their inclusion requires additional pretraining cycles to make use of the extra information." |
| Q171 | 18 | output_form | "Adversarial pretraining has been shown to be highly effective in boosting performance in general-domain applications [37]. We thus conducted adversarial pretraining in PubMedBERT and compared its performance with standard pretraining (Table 11). Surprisingly, adversarial pretraining generally leads to a slight degradation in performance, with some exceptions such as sentence similarity (BIOSSES). We hypothesize that the reason may be similar to what we observe in pretraining with full texts. Namely, adversarial training is most useful if the pretraining corpus is more diverse and relatively out-domain compared to the application tasks. We leave a more thorough evaluation of adversarial pretraining to future work." |
| Q172 | 18 | output_form | "In the above studies on pretraining methods, we fix the fine-tuning methods to the standard methods described in subsection 2.4. Next, we will study the effect of modeling choices in task-specific fine-tuning, by fixing the underlying pretrained language model to our standard PubMedBERT (WWM, PubMed vocabulary, pretrained using PubMed abstracts)." |
| Q173 | 18 | output_ontology | "Prior to the current success of pretraining neural language models, standard NLP approaches were often dominated by sequential labeling methods, such as conditional random fields (CRF) and more recently recurrent" |
| Q174 | 19 | output_ontology | "Such methods were particularly popular for named entity recognition (NER) and relation extraction." |
| Q175 | 19 | output_form | "Comparison of linear layers vs recurrent neural networks for task-specific fine-tuning in named entity recognition (entity-level F1) and relation extraction (micro F1), all using the standard PubMedBERT." |
| Q176 | 19 | output_form | "Comparison of entity-level F1 for biomedical named entity recognition (NER) using different tagging schemes and the standard PubMedBERT." |
| Q177 | 19 | output_form | "Comparison of PubMedBERT performance on BLURB using standard and adversarial pretraining." |
| Q178 | 20 | output_ontology | "With the advent of BERT models and the self-attention mechanism, the utility of explicit sequential modeling becomes questionable." |
| Q179 | 20 | output_ontology | "We find that this is indeed the case for NER and relation extraction, as shown in Table 12." |
| Q180 | 20 | output_form | "The use of a bidirectional LSTM (Bi-LSTM) does not lead to any substantial gain compared to linear layer." |
| Q181 | 20 | output_ontology | "We thus conducted a head-to-head comparison of the tagging schemes using three biomedical NER tasks in BLURB." |
| Q182 | 20 | output_form | "As we can see in Table 13, the difference is minuscule, suggesting that with self-attention, the sequential nature of the tags is less essential in NER modeling." |
| Q183 | 20 | input_form | "With entity dummification, the entity mentions in question are anonymized using entity type tags such as $DRUG or $GENE." |
| Q184 | 20 | input_form | "With entity marker, special tags marking the start and end of an entity are appended to the entity mentions in question." |
| Q185 | 20 | input_form | "Relation encoding is derived from the special [CLS] token appended to the beginning of the text or the special entity start token, or by concatenating the contextual representation of the entity mentions in question." |
| Q186 | 20 | input_form | "It is a common practice to "dummify" entities (i.e., replace an entity with a generic tag such as $DRUG or $GENE)." |
| Q187 | 20 | output_ontology | "We thus conducted a systematic evaluation of entity dummification and relation encoding, using two relation extraction tasks in BLURB." |
| Q188 | 20 | input_form | "For entity marking, we consider three variants: dummify the entities in question; use the original text; add start and end tags to entities in question." |
| Q189 | 20 | input_form | "For relation encoding, we consider three schemes. In the [CLS] encoding introduced by the original BERT paper, the special token [CLS] is prepended to the beginning of the text span, and its contextual representation at the top layer is used as the input in the final classification." |
| Q190 | 20 | input_form | "Another standard approach concatenates the BERT encoding of the given entity mentions, each obtained by applying max pooling." |
| Q191 | 21 | input_content | "There are a plethora of biomedical NLP datasets, especially from various shared tasks such as BioCreative [3, 29, 40, 53], BioNLP [15, 28], SemEval [2, 9, 10, 17], and BioASQ [42]." |
| Q192 | 21 | input_ontology | "The focus has evolved from simple tasks, such as named entity recognition, to more sophisticated tasks, such as relation extraction and question answering, and new tasks have been proposed for emerging application scenarios such as evidence-based medical information extraction [44]." |
| Q193 | 21 | input_ontology | "However, while comprehensive benchmarks and leaderboards are available for the general domains (e.g., GLUE [57] and SuperGLUE [56]), they are still a rarity in biomedical NLP." |
| Q194 | 21 | input_ontology | "In this paper, inspired by prior effort towards this direction [45], we create the first leaderboard for biomedical NLP, BLURB — a comprehensive benchmark containing thirteen datasets for six tasks." |
| Q195 | 21 | input_ontology | "To facilitate this study, we create BLURB, a comprehensive benchmark for biomedical NLP featuring a diverse set of tasks such as named entity recognition, relation extraction, document classification, and question answering." |
| Q196 | 21 | output_form | "To accelerate research in biomedical NLP, we release our state-of-the-art biomedical BERT models and setup a leaderboard based on BLURB." |
| Q197 | 22 | input_ontology | "Future directions include: further exploration of domain-specific pretraining strategies; incorporating more tasks in biomedical NLP; extension of the BLURB benchmark to clinical and other high-value domains." |
| Q198 | 24 | input_content | "A corpus with multi-level annotations of patients, interventions and outcomes to support language processing for medical literature." |
| Q199 | 24 | output_form | "Transfer Learning in Biomedical Natural Language Processing: An Evaluation of BERT and ELMo on Ten Benchmarking Datasets." |
| Q200 | 24 | input_ontology | "Results of the Seventh Edition of the BioASQ Challenge." |
| Q201 | 24 | output_ontology | "BIOSSES: a semantic sentence similarity estimation system for the biomedical domain." |
| Q202 | 24 | input_ontology | "Overview of BioCreative II gene mention recognition." |
| Q203 | 24 | input_ontology | "Drug–drug interaction extraction via hierarchical RNNs on sequence and shortest dependency paths." |
| Q204 | 24 | input_ontology | "Enhancing clinical concept extraction with contextual embeddings." |
| Q205 | 24 | input_ontology | "GLUE: A MULTI-TASK BENCHMARK AND ANALYSIS PLATFORM FOR NATURAL LANGUAGE UNDERSTANDING." |
| Q206 | 24 | input_ontology | "Superglue: A stickier benchmark for general-purpose language understanding systems." |

---

## Regional Context

```yaml
name: EU/French Pharmaceutical Regulatory NLP — BLURB Assessment
abbreviation: eu_pharma_regulatory_fr
deployment_population:
  description: Regulatory affairs specialists, pharmacologists, and legal experts
    at pharmaceutical companies or government health agencies (including ANSM and
    EMA-affiliated bodies) operating under EU and French regulatory frameworks. End
    users are highly trained domain professionals, not the general public. Literacy,
    interface modality, and device access are not concerns; domain-specific precision,
    regulatory normative alignment, and annotation authority are paramount.
  occupational_roles:
  - Regulatory affairs specialist
  - Pharmacologist
  - Legal/regulatory counsel
  - Pharmacovigilance officer
  - Medical writer (regulatory)
  institutional_settings:
  - Pharmaceutical company regulatory affairs departments
  - Contract research organizations (CROs) with regulatory services
  - ANSM (Agence nationale de sécurité du médicament et des produits de santé)
  - EMA (European Medicines Agency) or national competent authority affiliates
  - Hospital or academic pharmaceutical research units with regulatory remit
  geographic_scope: European Union, with primary focus on France (ANSM jurisdiction)
    and EU-wide EMA regulatory context
  primary_country: France
  regulatory_jurisdictions:
  - EMA (centralized EU procedure)
  - ANSM (national French procedure and mutual recognition)
  - EU decentralized procedure NCAs
languages:
  primary_operational_language: French
  secondary_operational_language: English (EMA scientific guidelines, international
    patent claims, CTD modules)
  note: The deployment targets French-language regulatory documents (SmPCs, patient
    information leaflets, French CTD module prose) as primary inputs. The benchmark
    (BLURB) is exclusively English. This language mismatch is a foundational external
    validity problem for every benchmark task. No porting strategy is documented for
    BLURB.
writing_systems:
  scripts:
  - Latin alphabet with French diacritics (é, è, ê, ë, à, â, ù, û, ô, î, ï, ç, œ,
    æ)
  note: Standard Latin-script NLP tooling applies; no RTL or non-Latin script concerns.
    However, French pharmaceutical and regulatory abbreviations, INN transliteration
    conventions, and posology phrasing require French-specific tokenization and vocabulary
    coverage absent from English-trained models.
literacy_and_modality:
  note: End-user population consists of university-educated domain professionals.
    General literacy and interface modality are not assessment concerns. Domain literacy
    (regulatory, legal, pharmacological) is at expert level and constitutes the normative
    standard against which model outputs are evaluated.
regulatory_framework:
  primary_regulations_and_guidelines: 'Current key instruments confirmed as of 2024–2025:
    (1) EMA QRD SmPC Template v10.4 (updated 29 February 2024; v11 draft open for
    public consultation until 31 August 2025) — mandatory for all EU centralized,
    decentralized, and mutual recognition procedure submissions. (2) EU Directive
    2001/83/EC (as amended) — legal foundation for SmPC/PIL content requirements;
    Article 59(4) report triggered the current QRD template revision. (3) Regulation
    (EC) No 726/2004 — governs the centralized marketing authorization procedure.
    (4) ICH CTD M4 series guidelines — govern Common Technical Document format for
    regulatory submissions. (5) EU AI Act (entered into force 1 August 2024) — applies
    to high-risk AI systems used in the pharmaceutical product lifecycle, including
    NLP tools influencing regulatory decisions.

    Sources: EMA QRD templates page — [WEB-1];
    EMA QRD v10.4 document — [WEB-2];
    EMA draft QRD v11 — [WEB-3]'
  key_regulatory_bodies:
  - EMA (European Medicines Agency)
  - ANSM (Agence nationale de sécurité du médicament et des produits de santé)
  - European Commission (marketing authorization decisions)
  - ICH (International Council for Harmonisation — CTD format)
  applicable_data_protection_regulation: 'GDPR (Regulation EU 2016/679) applies to
    all personal data processing in the EU, including pharmaceutical document management
    systems handling personal health data. Within the pharmaceutical regulatory context,
    GDPR intersects with: EMA Policy 0070 (clinical data publication — relaunched
    September 2023), EU Clinical Trials Regulation 536/2014 (which introduces derogations
    to GDPR right-to-be-forgotten for safety data integrity), and EMA CTIS data protection
    notices. For regulatory submission documents (SmPCs, CTD modules), the primary
    data sensitivity concern is commercially confidential information (CCI) rather
    than personal data — governed by EMA Policy 0043 and the CJEU case law on document
    access. The EU AI Act (2024) further imposes requirements on high-risk AI systems
    in the pharmaceutical lifecycle, including NLP tools influencing submission decisions.

    Sources: EMA data protection page — [WEB-4];
    EMA Policy 0070 overview — [WEB-5];
    EMA AI Reflection Paper (October 2024) — [WEB-6]'
  smpc_qrd_template_version_in_force: 'QRD SmPC template version 10.4, updated 29
    February 2024 (current operative version for centralized procedure submissions).
    A draft version 11 was released for public consultation in April 2025, with comments
    due by 31 August 2025; v11 primarily revises the Package Leaflet structure and
    introduces a potential ''Key Information'' section. Marketing Authorization Holders
    are expected to implement v10.4 at the next regulatory procedure affecting SmPC/labelling/PIL.
    The CMDh annotated QRD template for MRP/DCP was updated March 2024 with a correction
    issued September 2025.

    Sources: EMA QRD templates — [WEB-1];
    AxeRegel QRD update summary — [WEB-7];
    CMDh QRD — [WEB-8]'
  ansm_circular_references: '[NEEDS VERIFICATION — deferred: below search budget.
    ANSM-specific procedural circulars governing French-language SmPC and PIL requirements
    are not systematically indexed online; requires direct consultation of ANSM''s
    official publications portal (ansm.sante.fr) or expert elicitation from ANSM regulatory
    affairs practitioners.]'
document_genres_in_scope:
  primary:
  - Summary of Product Characteristics (SmPC) — French-language version under EMA
    QRD template
  - Patient Information Leaflet (PIL / notice patient) — French-language version
  - Common Technical Document (CTD) module prose — applicable modules in French or
    English
  secondary:
  - Patent claims (pharmaceutical, French and European patent office filings)
  - Pharmacovigilance periodic safety update reports (PSURs)
  - Risk management plans (RMPs)
  - Clinical study reports (CSRs) — regulatory submission sections
  note: 'These document genres are characterized by highly formulaic, legally constrained
    language governed by EMA QRD templates and ANSM requirements. They are categorically
    distinct from PubMed research abstracts, which constitute the entirety of BLURB''s
    input corpus. A 2025 Frontiers in Medicine study on LLM-based extraction from
    SmPC documents (English) confirms ATC Codes and specific excipient dosages are
    frequently missed or misclassified even by state-of-the-art LLMs, underscoring
    the specialized difficulty of regulatory NER in this genre. Source: Frontiers/Medicine
    SmPC IDMP extraction study — [WEB-9]'
entity_ontology_in_scope:
  regulatory_ner_entity_types:
  - International Nonproprietary Names (INNs)
  - ATC codes (Anatomical Therapeutic Chemical classification)
  - Excipient nomenclature (INCI names, E-numbers, Ph. Eur. nomenclature)
  - Posology expressions (French-language, e.g., 'deux comprimés par jour', dose ranges,
    weight-based dosing)
  - EMA-template contraindication qualifiers (population specifiers, condition qualifiers)
  - Safety warning phrases (Black Triangle designation, pregnancy category language,
    special warnings)
  - Pharmaceutical form descriptors (tablet, capsule, solution for injection — French
    terminology)
  - Route of administration terms (French regulatory vocabulary)
  - Storage condition expressions
  - Marketing authorization holder (MAH) identifiers
  benchmark_entity_coverage: 'BLURB NER datasets cover: chemical entities (BC5-Chemical),
    disease entities (BC5-Disease, NCBI-Disease), gene/protein mentions (BC2GM, JNLPBA).
    No label space exists for INNs, ATC codes, excipient nomenclature, posology expressions,
    or EMA-template phrasing. Coverage is partial at best for chemical entities only.'
  inn_database_reference: '[NEEDS VERIFICATION — deferred: low impact for scoring
    relative to resolved gaps. WHO INN list and EDQM Standard Terms are the operative
    references for EMA submissions; current versions would require direct verification
    at WHO and EDQM portals. This does not materially change the gap assessment —
    the absence of INN-aware NER in BLURB is structural regardless of the specific
    list version.]'
  atc_code_taxonomy_version: '[NEEDS VERIFICATION — deferred: low impact for scoring.
    WHO ATC/DDD Index is updated annually; current version (2025) would be confirmed
    at WHO Collaborating Centre for Drug Statistics Methodology. The absence of ATC
    code NER in BLURB is the scoring-relevant fact, not the specific index version.]'
  smpc_ner_extraction_evidence: 'A 2025 study applying LLMs with RAG to extract IDMP-compliant
    fields from SmPC documents found that ATC Codes and specific excipient dosages
    were ''frequently missing or misclassified'' and that some fields such as Pharmaceutical
    Product required semantic search to outperform rule-based retrieval, confirming
    the difficulty of regulatory-specific entity extraction even for current LLMs.
    This provides direct empirical support for the entity ontology gap assessment.

    Source: Frontiers in Medicine SmPC IDMP extraction study — [WEB-9]'
sts_and_equivalence_framework:
  description: 'The deployment uses semantic textual similarity (STS) to verify regulatory
    consistency across document versions (e.g., SmPC vs. patient leaflet, original
    vs. revised label). Regulatory equivalence differs from general semantic proximity:
    small lexical differences in dose thresholds, contraindicated population qualifiers,
    or safety warning language carry legal consequence under EMA/ANSM standards.'
  decision_function: Borderline or inconsistent STS scores trigger human review (manual
    revision flag); automatic rejection is not triggered by borderline scores alone.
  critical_mismatch_categories:
  - Dose threshold discrepancies (numerical values, units, frequency)
  - Contraindicated population qualifiers (age bands, renal/hepatic impairment grades,
    pregnancy trimesters)
  - Safety warning scope differences (absolute vs. relative contraindication language)
  - Indication scope modifiers (adult vs. pediatric, specific comorbidity qualifiers)
  benchmark_sts_analog: BIOSSES (100 PubMed sentence pairs, 0–4 similarity score,
    Pearson correlation metric) — structurally analogous but operationalizes general
    biomedical proximity, not regulatory equivalence. Legally determinative lexical
    differences are not modeled in BIOSSES scoring.
  regulatory_equivalence_benchmarks_available: '[NOT FOUND — searched for EMA/ANSM
    annotated consistency-checking corpora, academic regulatory STS datasets, and
    pharmacovigilance literature formalizing regulatory equivalence scoring. No dedicated
    regulatory equivalence STS benchmark was identified. The EMA AI Observatory 2024
    report documents internal regulatory NLP tools (Scientific Explorer, PICROSS,
    EurEKA, AERGIA) but none are framed as public benchmarks for label consistency
    checking. This confirms the gap identified by the scaffold: no publicly available
    regulatory STS benchmark exists as of 2024–2025.

    Source: EMA 2024 AI Observatory Report — [WEB-10];
    EMA AI tools overview — [WEB-11]]'
annotator_population_and_norms:
  deployment_ground_truth_authority: Regulatory affairs specialists and legal experts
    operating under EMA/ANSM normative frameworks; annotation judgments governed by
    regulatory guidelines, not clinical relevance criteria.
  benchmark_annotator_population: Biomedical researchers, Amazon Mechanical Turkers
    (EBM PICO training/dev), Upwork contributors with medical training (EBM PICO test),
    biomedical experts (BioASQ, BIOSSES). No regulatory affairs specialists or legal
    experts.
  anticipated_annotation_norm_mismatch: 'Systematic disagreements expected on borderline
    cases: BLURB-style annotators are likely to prioritize clinical relevance, while
    the deployment''s ground truth prioritizes rigid legal constraint satisfaction
    (EMA/ANSM standard). This mismatch directly undermines label validity for this
    use case.'
  inter_annotator_agreement_studies: '[NOT FOUND — searched for IAA studies comparing
    biomedical NLP annotators vs. regulatory affairs specialists on pharmaceutical
    NER or STS tasks. No published study directly comparing these two annotator populations
    was identified. This absence is itself informative: the regulatory-expert annotator
    population has not been systematically studied in NLP annotation contexts, reinforcing
    the severity of the annotator norm gap flagged by the scaffold.]'
  regulatory_expert_annotated_datasets: '[NOT FOUND — No published NER or STS datasets
    annotated by regulatory affairs professionals under EMA/ANSM frameworks were identified.
    The most relevant parallel is the Italian DART dataset (AIFA-sourced SmPC corpus
    for NER/RE, 2025), which covers regulatory document genres but is Italian-language
    and does not involve regulatory-expert annotators. No French equivalent was found.

    Source: DART Italian SmPC NER dataset paper — [WEB-12]]'
infrastructure_notes:
  deployment_environment: Enterprise pharmaceutical document management system; end
    users are institution-connected professionals with full desktop/server infrastructure.
    No mobile, low-bandwidth, or connectivity constraints.
  system_integration: NER and STS models integrated into document management pipeline;
    outputs trigger either automatic approval for submission or flagging for manual
    revision review.
  model_serving_requirements: 'On-premises or European sovereign cloud deployment
    is strongly preferred in EU pharmaceutical regulatory NLP contexts, based on multiple
    converging factors: (1) regulatory submission documents contain commercially sensitive
    information (CCI) and trade secrets protected under EMA Policy 0043; (2) GDPR
    and EU AI Act compliance requirements create strong data residency pressures;
    (3) EU AI Act classifies AI systems with ''high regulatory impact'' in the pharmaceutical
    lifecycle as requiring special controls; (4) industry practice shows pharmaceutical
    companies consider three models — on-premise data centers, European sovereign
    cloud providers (OVHcloud, Outscale, Scaleway), or US hyperscalers under reinforced
    contractual guarantees. The EMA''s own AI Reflection Paper (October 2024) requires
    MAHs to ensure all AI/ML datasets and pipelines are ''fit for purpose and in line
    with legal, ethical, technical, scientific, and regulatory standards''.

    Sources: EMA AI Reflection Paper — [WEB-6];
    Sovereign AI pharma guide — [WEB-13]'
  data_sensitivity: Regulatory submission documents contain commercially sensitive
    and legally privileged information; data handling must comply with applicable
    confidentiality obligations and GDPR. EMA Policy 0070 governs proactive publication
    of clinical data (relaunched September 2023), but pre-authorization submission
    documents (SmPCs drafts, CTD modules, internal RMPs) remain protected CCI. The
    European Health Data Space (EHDS), which entered into force March 2025, creates
    new secondary-use obligations but clinical trial data will not be subject to EHDS
    provisions until March 2031.
  french_biomedical_nlp_tooling_availability: 'Three principal French biomedical pretrained
    language models are currently available: (1) DrBERT (Labrak et al., ACL 2023)
    — pretrained from scratch on public and private French medical data, highest pretraining
    breadth including drug leaflets and clinical cases; (2) CamemBERT-bio (Touchent
    & de la Clergerie, LREC-COLING 2024) — continual pretraining of CamemBERT on French
    biomedical data, competitive on NER tasks; (3) AliBERT (Berhe et al., BioNLP 2023)
    — pretrained with Unigram-based tokenizer, state-of-the-art on some downstream
    tasks with smaller pretraining footprint. A comprehensive evaluation on DrBenchmark
    (20 French biomedical tasks including NER and STS) shows no single model dominates
    all tasks, and none has been fine-tuned specifically on EMA/ANSM regulatory document
    genres (SmPCs, PILs, CTD modules).

    Sources: DrBERT paper — [WEB-14]; CamemBERT-bio paper
    — [WEB-15]; AliBERT paper — [WEB-16];
    DrBenchmark — [WEB-17]'
domain_specific_notes:
  regulatory_science_context: 'EU pharmaceutical regulation is a highly codified domain
    with explicit template governance (EMA QRD SmPC template, PIL readability guidelines).
    Compliance determination is a legal act, not a clinical judgment. NLP system outputs
    that influence submission decisions carry regulatory and legal liability implications.
    The EMA Reflection Paper on AI (October 2024) explicitly addresses this: AI used
    at the ''marketing-authorisation stage'' to ''draft, compile, translate, or review
    data to be included in the product information of a medicine'' must comply with
    GxP standards and current EMA guidelines, with MAHs retaining full responsibility.

    Source: EMA AI Reflection Paper — [WEB-6]'
  language_register: SmPC and PIL language is formulaic, constrained, and template-driven.
    This differs substantially from both clinical notes (informal, variable) and PubMed
    research prose (argumentative, citation-dense). Formulaic repetition across document
    versions is a feature, not noise — and deviations from formula are precisely what
    the system must detect.
  posology_expression_complexity: French posology expressions combine numerical quantities,
    pharmaceutical form names, route of administration, frequency adverbs, and conditional
    clauses (e.g., patient population qualifiers). These are compositional regulatory
    entities not present in BLURB training data.
  cross_document_consistency_requirement: The deployment requires semantic consistency
    verification across document pairs (SmPC ↔ PIL, original ↔ revised version). BLURB's
    BIOSSES task covers 100 isolated sentence pairs from a single domain with no cross-document
    regulatory consistency framing.
  eudralex_and_ctd_structure: '[NEEDS VERIFICATION — deferred: below search budget.
    EudraLex Volume 2B (Notice to Applicants — CTD format) is the operative reference
    for CTD structure; current version would require verification at the European
    Commission EudraLex portal. The distinction between structured data fields and
    free-text prose amenable to NER/STS is well understood from domain knowledge (Modules
    1–5; Module 1 contains the SmPC/PIL; Modules 2–5 contain scientific summaries
    and study reports), but formal citation was not pursued given budget constraints.]'
  pharmacovigilance_nlp_literature: 'The EMA 2024 AI Observatory Report confirms active
    internal development of pharmacovigilance NLP tools: EurEKA (adverse reaction
    data extraction), AERGIA (automated signal adjudication), and ERATO (generative
    AI-based literature screening for safety signals). The Swedish MPA''s PICROSS
    tool performs semantic cross-referencing of product information. None of these
    are publicly available benchmarks, but their existence confirms that EU regulatory
    bodies are actively deploying NLP/AI for pharmacovigilance — providing institutional
    context for the deployment''s plausibility and raising the bar for validation
    requirements.

    Source: EMA 2024 AI Observatory Report — [WEB-10];
    EMA AI page — [WEB-11]'
  eu_ai_act_applicability: 'The EU AI Act entered into force 1 August 2024. NLP systems
    that influence regulatory submission decisions (classifying whether documents
    meet EMA/ANSM standards for submission) may fall under high-risk AI classification
    if used as safety components of regulated processes. The EMA Reflection Paper
    (October 2024) distinguishes ''high patient risk'' and ''high regulatory impact''
    as the operative risk tiers and requires MAHs to document that all AI pipelines
    are ''fit for purpose.'' France''s CNIL has announced forthcoming guidance tailored
    to AI deployment in healthcare, developed with Haute Autorité de Santé (HAS),
    aimed at aligning AI Act requirements with GDPR for pharmaceutical contexts.

    Sources: EMA AI Reflection Paper — [WEB-6];
    European Pharmaceutical Review AI Act article — [WEB-18]'
benchmark_gap_summary:
  language_gap:
    severity: HIGH — foundational
    description: BLURB is exclusively English. The deployment targets French-language
      documents. No porting strategy exists.
    web_search_target: 'RESOLVED — French biomedical/pharmaceutical NLP benchmarks
      identified:


      (1) QUAERO French Medical Corpus: The primary French biomedical NER benchmark,
      initially developed for entity recognition and normalization, used in CLEF eHealth
      2015 (Task 1b) and 2016 (Task 2). Covers 10 entity categories mapped to UMLS
      Semantic Groups (including Chemical and Drugs) across MEDLINE titles and EMEA
      regulatory documents. The EMEA subcorpus contains regulatory texts directly
      relevant to the deployment, but entity categories are UMLS-based (not INN/ATC/posology-specific)
      and annotation norms reflect biomedical research, not regulatory compliance.

      Sources: QUAERO corpus — [WEB-19]; HuggingFace
      dataset — [WEB-20]


      (2) DrBenchmark (LREC-COLING 2024): The first comprehensive French biomedical
      NLP benchmark, comprising 20 tasks including NER, POS tagging, QA, STS, and
      classification. Evaluates 8 state-of-the-art masked language models (CamemBERT-bio,
      DrBERT, AliBERT, CamemBERT, FlauBERT, FrALBERT, mBERT) on French biomedical
      corpora. Includes STS tasks relevant to the deployment''s semantic consistency
      requirement. Does not include regulatory document genres (SmPCs, PILs) or regulatory-expert
      annotation.

      Source: DrBenchmark paper — [WEB-17];
      DrBenchmark website — [WEB-21]


      (3) CLEF eHealth shared tasks (2015–2016): Provided French biomedical NER evaluation
      infrastructure used to establish QUAERO as a benchmark. Results show high performance
      achievable on French biomedical NER.

      Source: CLEF eHealth 2016 PMC paper — [WEB-22]


      Critical caveat: None of these French benchmarks cover regulatory document genres
      (SmPCs, PILs) or regulatory-specific entity types (INNs, ATC codes, posology).
      The QUAERO EMEA subcorpus is the closest match, but its entity taxonomy and
      annotation norms remain research-biomedical, not regulatory-legal. The French
      language gap in BLURB is confirmed foundational; QUAERO/DrBenchmark partially
      address language form but not regulatory domain gaps.'
  document_genre_gap:
    severity: HIGH — full gap
    description: BLURB contains no SmPCs, PILs, CTD modules, or patent claims. All
      inputs are PubMed research abstracts.
    web_search_target: 'PARTIALLY RESOLVED — No public French-language EU regulatory
      NLP benchmark covering SmPCs or PILs was found. Key findings:


      (1) QUAERO EMEA subcorpus: Contains 4 EMEA regulatory documents (segmented into
      15 sub-documents) with NER annotations. This is the only publicly available
      French regulatory document NLP resource identified, but it is extremely small
      (4 EMEA-source documents), uses UMLS-based entity categories rather than regulatory-specific
      types, and is primarily used as a biomedical NER benchmark rather than a regulatory
      compliance evaluation resource.

      Source: QUAERO HuggingFace dataset documentation — [WEB-20]


      (2) DART (Italian, 2025): A recently published Italian SmPC corpus for NER/RE
      (AIFA-sourced) with regulatory-relevant entity types including active substances,
      administration routes, pharmacokinetic mechanisms, and pregnancy risk categories.
      This is the closest analog to what would be needed for French regulatory NLP,
      but is Italian-language and not validated against regulatory expert annotators.

      Source: DART paper — [WEB-12]


      (3) NLP for regulatory labeling (2025 review): A practitioner review of NLP
      applied to EU SmPC/prescribing information documents confirms that current use
      is ''hybrid: AI assists with retrieval, initial drafts, formatting, and consistency
      checks, while humans perform final authoring, quality control, and regulatory
      compliance checks.'' No validated regulatory-specific benchmark is documented.

      Source: IntuitionLabs NLP regulatory labeling review — [WEB-23]


      Conclusion: The document genre gap remains a full gap for French-language regulatory
      genres. The QUAERO EMEA subcorpus is a marginal partial resource. The DART Italian
      corpus is an informative parallel but not directly applicable.'
  entity_ontology_gap:
    severity: HIGH — partial at best
    description: BLURB NER covers chemical, disease, gene entities. No INN, ATC code,
      excipient, or posology label space exists.
    web_search_target: 'PARTIALLY RESOLVED — No INN-specific, ATC-code-specific, or
      posology-specific French-language NER dataset was identified. Key findings:


      (1) QUAERO ''Chemical and Drugs'' category: Covers chemical/drug entity mentions
      normalized to UMLS CUIs, which partially overlaps with INN recognition but uses
      UMLS categories rather than EMA-specific nomenclature. No ATC code, excipient,
      or posology subtype is annotated.

      Source: QUAERO documentation — [WEB-19]


      (2) SmPC IDMP extraction study (Frontiers in Medicine, 2025): Demonstrates empirically
      that ATC Codes and excipient dosages are ''frequently missing or misclassified''
      by LLMs even in English SmPC extraction, and that fields like Pharmaceutical
      Product require semantic search to outperform rule-based retrieval. This confirms
      the practical severity of the entity ontology gap even for current generation
      models.

      Source: Frontiers SmPC study — [WEB-9]


      (3) DART Italian corpus: Includes active substances, administration routes,
      and pregnancy risk categories as entity types in Italian SmPCs — structurally
      closer to regulatory NER than BLURB, but Italian-language and not covering posology
      or ATC codes as distinct NER targets.

      Source: DART paper — [WEB-12]


      Conclusion: The entity ontology gap is confirmed. No French regulatory NER dataset
      with INN, ATC, excipient, or posology label spaces exists publicly. The gap
      is structural and would require bespoke corpus development under EMA/ANSM annotation
      guidelines.'
  sts_output_construct_gap:
    severity: HIGH — qualitative mismatch
    description: BIOSSES operationalizes general biomedical semantic proximity. The
      deployment requires regulatory equivalence as a legally determinative scoring
      function.
    web_search_target: 'NOT FOUND — No regulatory equivalence STS benchmark, EMA/ANSM
      annotated consistency-checking corpus, or academic formalization of regulatory
      STS distinct from general biomedical STS was identified. The EMA''s internal
      tools (Scientific Explorer, PICROSS) perform some form of semantic matching
      on regulatory documents but are not public benchmarks. DrBenchmark includes
      French STS tasks (DEFT-2020, CLISTER) evaluated with Spearman correlation and
      EDRM metrics, but these cover general biomedical semantic similarity, not regulatory
      equivalence. This confirms the scaffold''s assessment: regulatory equivalence
      STS is an un-benchmarked construct.

      Sources: DrBenchmark — [WEB-17]; EMA
      AI Observatory 2024 — [WEB-10]'
  annotator_norm_gap:
    severity: HIGH — systematic mismatch anticipated
    description: BLURB annotators are biomedical researchers; deployment ground truth
      is regulatory affairs specialists under EMA/ANSM norms. Borderline case disagreements
      are expected.
    web_search_target: 'NOT FOUND — No IAA studies comparing biomedical NLP annotators
      vs. regulatory affairs specialists on pharmaceutical NER or STS tasks were identified.
      No regulatory-expert-annotated pharmaceutical NLP dataset (French or English)
      was found in the literature. The closest analog is the DART Italian SmPC corpus
      (2025), which uses AIFA regulatory document text as source material but does
      not involve regulatory expert annotators or IAA studies comparing regulatory
      vs. biomedical annotator populations. This null result confirms the gap is not
      merely unresolved in BLURB but unaddressed in the NLP literature more broadly.

      Source: DART paper — [WEB-12]'
  threshold_sensitivity_gap:
    severity: MODERATE
    description: BLURB reports aggregate metrics without confidence calibration or
      threshold-sensitivity analysis. The deployment's human-review flagging logic
      requires characterization of model behavior at decision boundaries.
    web_search_target: '[NEEDS VERIFICATION — deferred: below search budget after
      resolving higher-priority gaps. Confidence calibration in biomedical NLP is
      an active research area; threshold-sensitive evaluation for regulatory human-in-the-loop
      workflows has not been specifically searched. This gap is structural to BLURB''s
      metric design and would not be resolved by any currently identified French or
      EU regulatory benchmark.]'
  regulatory_normative_validation_gap:
    severity: HIGH — full gap
    description: BLURB has not been validated against EMA guidelines, ANSM circulars,
      or any EU regulatory normative framework.
    web_search_target: 'PARTIALLY RESOLVED — No NLP benchmark has been validated against
      EMA SmPC guidelines or ANSM circulars. However, the EMA has published the following
      directly relevant normative framework that would govern any such validation:


      (1) EMA Reflection Paper on AI in Medicinal Product Lifecycle (October 2024):
      Establishes that AI tools used in product information drafting/reviewing must
      be ''validated'' under GxP standards and current EMA guidelines, with human
      oversight mechanisms. The paper specifies that ''quality review mechanisms should
      be in place to ensure that AI-generated text (used for drafting, compiling,
      editing, translating, tailoring or reviewing product information) is factually
      and syntactically correct.''


      (2) EMA-HMA Guiding Principles on LLMs (September 2024): Provides regulatory
      network-level guidance on LLM use, covering data security, critical evaluation
      of outputs, and governance structures.


      (3) EMA LLM Guiding Principles note potential use of LLMs for ''processing extensive
      documentation, automating data mining and optimising routine administrative
      tasks'' while acknowledging risks of ''irrelevant or inaccurate responses and
      posing potential data security risks.''


      These documents collectively constitute the normative framework against which
      any regulatory NLP benchmark validation would need to be assessed — and confirm
      that no such benchmark validation has yet been conducted.

      Sources: EMA AI Reflection Paper — [WEB-6];
      EMA AI page (LLM guiding principles) — [WEB-11]'
net_new_fields:
  ema_ai_governance_context:
    description: 'The EMA and HMA published a multi-annual AI workplan (2023–2028)
      and released in September 2024 guiding principles for LLM use by European regulatory
      network staff. In October 2024, EMA adopted a Reflection Paper on AI in the
      Medicinal Product Lifecycle, establishing that AI tools used in product information
      drafting or reviewing must comply with GxP standards and EMA guidelines, with
      MAHs retaining full responsibility for algorithm fitness. This is the directly
      applicable normative framework for the deployment and provides a concrete validation
      standard against which BLURB''s fitness should be assessed. The EMA also operates
      internal NLP tools (Scientific Explorer, EurEKA, AERGIA, ERATO) demonstrating
      institutional commitment to regulatory NLP, but none constitute public benchmarks.

      Source: EMA AI Reflection Paper — [WEB-6];
      EMA AI Observatory 2024 — [WEB-10]'
    validity_dimension: OO, OC — directly affects how regulatory normative validation
      of benchmark outputs should be framed in the assessment
  french_biomedical_nlp_model_landscape:
    description: 'Three French biomedical pretrained language models are available
      as of 2024: DrBERT (from-scratch pretraining on French medical data including
      drug leaflets; ACL 2023), CamemBERT-bio (continual pretraining; LREC-COLING
      2024), and AliBERT (Unigram tokenizer, BioNLP 2023). All three are evaluated
      in DrBenchmark across 20 French biomedical tasks. No model has been fine-tuned
      on EMA/ANSM regulatory document genres. The DrBenchmark paper notes that training
      corpus diversity is limited to publicly available scientific content, and performance
      on private clinical/regulatory data may not be representative. CamemBERT-bio
      shows slight advantage on NER tasks; DrBERT on classification tasks; no dominant
      model across all tasks.

      Sources: DrBERT — [WEB-14]; CamemBERT-bio — [WEB-15];
      AliBERT — [WEB-16]; DrBenchmark — [WEB-17]'
    validity_dimension: IF — resolves the tooling availability question for French
      biomedical NLP adaptation, though regulatory document fine-tuning remains an
      open gap
  quaero_emea_subcorpus:
    description: 'The QUAERO French Medical Corpus includes a small EMEA-document
      subcorpus (4 EMEA documents, segmented into 15 sub-documents) annotated with
      10 UMLS-based entity categories including Chemical and Drugs. This is the only
      publicly identified French-language regulatory document NLP resource. It is
      extremely small and uses UMLS semantic groups rather than EMA-specific regulatory
      entity types (no INN, ATC, posology, or excipient subtypes). It was used in
      CLEF eHealth 2015–2016 shared tasks and is available in BRAT and BioC formats.
      Its relevance is as a starting point for domain adaptation, not as a regulatory
      equivalence benchmark.

      Source: QUAERO corpus — [WEB-19]; HuggingFace —
      [WEB-20]'
    validity_dimension: IC, IF — provides a marginal French regulatory document resource
      for domain adaptation but does not address entity ontology or annotator norm
      gaps
  dart_italian_smpc_corpus_parallel:
    description: 'DART (Drug Annotation from Regulatory Texts), published October
      2025, is the first structured corpus of Italian SmPC documents derived from
      the Italian Medicines Agency (AIFA), covering NER entities including active
      substances, administration routes, pharmacokinetic mechanisms, and pregnancy
      risk categories. It is Italian-language and does not involve regulatory-expert
      annotators, but is the closest structural analog to what would be needed for
      the French deployment context. Its existence demonstrates that national regulatory
      SmPC NER corpus development is technically feasible and may inform a French
      equivalent development roadmap.

      Source: DART paper — [WEB-12]'
    validity_dimension: IC, OC — informative precedent for regulatory SmPC NER corpus
      development; confirms the gap is not inherent to the domain but reflects absence
      of resource investment for French
  qrd_v11_consultation_in_progress:
    description: 'EMA launched a public consultation on QRD SmPC/PIL template version
      11 in April 2025, with comments due 31 August 2025. V11 primarily revises the
      Package Leaflet structure (potential ''Key Information'' section) and clarifies
      SmPC formatting. The current operative version for submissions is v10.4 (February
      2024). Any NLP system trained or evaluated on SmPC/PIL text should account for
      the ongoing template transition: text trained on pre-v10.4 documents may not
      reflect current template requirements, and v11 changes may alter the formulaic
      language patterns that the deployment''s NER/STS models depend on.

      Source: EMA draft QRD v11 consultation — [WEB-3];
      EMA QRD templates page — [WEB-1]'
    validity_dimension: IO, IC — template transitions affect the stability of the
      formulaic language patterns that define regulatory NER/STS targets; a benchmark
      or fine-tuning corpus built on pre-v10.4 data may already be partially obsolete
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/product-information-requirements/product-information-qrd-templates-human |
| WEB-2 | https://www.ema.europa.eu/en/documents/template-form/qrd-product-information-template-version-104-highlighted_en.pdf |
| WEB-3 | https://www.ema.europa.eu/en/documents/template-form/quality-review-documents-qrd-annotated-template-v11-draft-public-consultation_en.pdf |
| WEB-4 | https://www.ema.europa.eu/en/about-us/data-protection-privacy-ema |
| WEB-5 | https://rlsciences.com/ema-policy-0070-overview/ |
| WEB-6 | https://www.ema.europa.eu/en/documents/scientific-guideline/reflection-paper-use-artificial-intelligence-ai-medicinal-product-lifecycle_en.pdf |
| WEB-7 | https://www.axeregel.com/blog/45/brexit-impact-updates-on-qrd-templates |
| WEB-8 | https://www.hma.eu/human-medicines/cmdh/templates/qrd.html |
| WEB-9 | https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2025.1598979/full |
| WEB-10 | https://www.ema.europa.eu/en/documents/report/2024-ai-observatory-report_en.pdf |
| WEB-11 | https://www.ema.europa.eu/en/about-us/how-we-work/data-regulation-big-data-other-sources/artificial-intelligence |
| WEB-12 | https://arxiv.org/html/2510.18475 |
| WEB-13 | https://www.chapsvision.com/blog/sovereign-ai-pharma-compliance/ |
| WEB-14 | https://arxiv.org/abs/2304.00958 |
| WEB-15 | https://arxiv.org/abs/2306.15550 |
| WEB-16 | https://aclanthology.org/2023.bionlp-1.19/ |
| WEB-17 | https://aclanthology.org/2024.lrec-main.478/ |
| WEB-18 | https://www.europeanpharmaceuticalreview.com/article/264445/ai-act-data-governance-and-compliance-strategy-implications-in-pharma/ |
| WEB-19 | https://quaerofrenchmed.limsi.fr/ |
| WEB-20 | https://huggingface.co/datasets/DrBenchmark/QUAERO |
| WEB-21 | https://drbenchmark.univ-avignon.fr/ |
| WEB-22 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5756095/ |
| WEB-23 | https://intuitionlabs.ai/articles/nlp-regulatory-labeling |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark covers biomedical NLP tasks broadly, but pharmaceutical regulatory documents (SmPCs, patient leaflets, patent claims, CTD modules) use highly formulaic, legally constrained language distinct from clinical or research prose. Are these document genres and their specialized language central to the use case?
A1: Regulatory documents are central. The formulaic language of SmPCs and leaflets is handled as a structural baseline, and regulatory-specific templates are applied for highly specialized formats like CTD modules. The underlying extraction tasks (compounds, dosages, safety warnings) are considered consistent across document types.

Q2 [IC]: The system must detect very specific regulatory entity types and phrasings — INNs, ATC codes, excipient nomenclature, posology expressions (including French-language phrasing like "2 comprimés par jour"), and EMA-template-governed contraindication language. Do these diverge significantly from standard clinical or research text?
A2: These specific entity types and phrasing patterns are precisely what the system is designed to detect, confirming close alignment between the deployment's entity ontology and the regulatory vocabulary.

Q3 [OO]: For STS-based compliance checking, regulatory equivalence differs from general semantic proximity — small lexical differences (e.g., dose thresholds, contraindicated population qualifiers) carry legal consequence under EMA/ANSM standards. Does the scoring function need to be sensitive to this, and do borderline scores trigger automatic rejection or human review?
A3: The system is explicitly designed for regulatory equivalence, treating specific discrepancies (dose thresholds, population qualifiers) as critical mismatches rather than minor semantic variation. Borderline or inconsistent scores flag the document for human review but do not trigger automatic rejection.

Q4 [OC]: Ground-truth labels in biomedical benchmarks are annotated by clinical or research professionals. Regulatory compliance judgments are governed by EMA/ANSM guidelines and legal norms, potentially producing systematic disagreements with biomedical NLP annotators on borderline cases. Is this misalignment expected?
A4: Significant overlap is expected for core technical entities, but systematic disagreements are anticipated on borderline cases, where biomedical NLP annotators are likely to prioritize clinical relevance over rigid legal constraints — a meaningful annotation-norm mismatch.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | BLURB covers general biomedical NLP tasks (clinical/research prose) and lacks document-genre categories specific to regulatory submissions (SmPCs, CTD modules, patent claims), which constitute the core input type in this deployment. |
| IC | HIGH | The deployment requires INN nomenclature, ATC codes, posology expressions, and EMA-template phrasing in French — entity types and linguistic patterns unlikely to appear in BLURB's English clinical/research corpora, creating substantial construct-irrelevant variance. |
| IF | HIGH | The deployment operates on French-language regulatory documents, but BLURB is English-only with no porting strategy; this language mismatch is a foundational external validity problem for every benchmark task. |
| OO | HIGH | BLURB's STS scoring reflects general biomedical semantic proximity, whereas the deployment requires a regulatory-equivalence decision function where small lexical differences (dose thresholds, population qualifiers) are legally determinative — a qualitatively different output ontology. |
| OC | HIGH | BLURB annotations are produced by biomedical/clinical professionals whose norms diverge from EMA/ANSM regulatory standards; the user explicitly anticipates systematic disagreements on borderline cases, directly undermining label validity for this use case. |
| OF | MODERATE | Both benchmark and deployment use text-in / label-or-text-out formats, so the representational form broadly matches; however, the deployment's human-review flagging workflow introduces a threshold-sensitivity requirement not captured by standard benchmark scoring metrics. |

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
  "benchmark": "blurb",
  "region": "EU/French Pharmaceutical Regulatory NLP — BLURB Assessment",
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
