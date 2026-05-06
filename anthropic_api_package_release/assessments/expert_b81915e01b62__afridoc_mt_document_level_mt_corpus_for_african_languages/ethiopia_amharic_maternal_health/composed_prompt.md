I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **AFRIDOC-MT: A Document-Level Multi-Parallel Translation Dataset for African Languages** is valid for use in **Ethiopia Ministry of Health — Amharic Clinical Translation Deployment**.

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

- **Name**: afridoc_mt
- **Full Name**: AFRIDOC-MT: A Document-Level Multi-Parallel Translation Dataset for African Languages
- **Domain**: Document-level machine translation evaluation for African languages
- **Languages**: en, am, ha, sw, yo, zu
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
AFRIDOC-MT covers two domain categories — health (WHO articles) and information
technology news (Techpoint Africa) — with 334 and 271 documents respectively [Q2,
Q80]. Within the health domain, the task is document-level machine translation,
evaluated at both sentence and pseudo-document (chunked) levels [Q3], with
multi-way translation supported across all 30 language direction pairs [Q7].
The benchmark distinguishes document-level NMT from sentence-level MT as a
separate construct, motivated by context-dependent phenomena including coreference
resolution, lexical disambiguation, and lexical cohesion [Q15, Q16]. The model
taxonomy evaluated is broad: five encoder-decoder models (Toucan, M2M-100,
NLLB-200, MADLAD-400, Aya-101) [Q37, Q38] and multiple decoder-only LLMs
including LLaMA3.1, Gemma2, LLaMAX3, GPT-3.5 Turbo, and GPT-4o [Q39], with
fine-tuning experiments for NLLB-200 and LLaMAX3 [Q42] and evaluation across
three distinct prompts per LLM [Q91, Q235]. Coverage is explicitly limited to
five African languages due to cost and funding constraints [Q93], and multi-way
non-English translation directions are evaluated only partially [Q94, Q101].
The task taxonomy does not include structured document types (tables, vaccination
timetables, administrative forms) — the corpus consists entirely of narrative
prose articles [Q18].

### Input Content
English source documents were scraped from two publicly available websites:
WHO (health domain, average 37 sentences/article) and Techpoint Africa
(technology domain, average 30 sentences/article) [Q18, Q22]. Data selection
is described as representing different cultural perspectives with attention to
minimizing bias [Q106], and content was screened to exclude harmful or offensive
material [Q107]. The health domain is licensed CC BY-NCSA 3.0 and the technology
domain CC BY-NC-SA 4.0 [Q34]. Baseline model training data varies:
MADLAD-400 was trained on Common Crawl [Q137], and Toucan was pre-trained on
large multilingual texts covering over 500 African languages [Q140]; fine-tuning
of NLLB-200 and LLaMAX3 used all training examples from 30 language directions
across both domains [Q150]. A critical limitation for deployment contexts
requiring locally grounded health content is that all source documents originate
in English and may exhibit translationese effects — unnatural syntax, overly
literal phrasing, and English-centric structural and semantic framing — in the
translated African-language outputs [Q103, Q104, Q105]. Existing MT datasets for
African languages are primarily drawn from religious or news domains at the
sentence level [Q12, Q13], and AFRIDOC-MT's health focus represents a step toward
deployment-relevant coverage, though institutionally specific content (e.g.,
Ethiopia MOH referral pathways or local endemic disease terminology) is absent.

### Input Form
The benchmark is text-only throughout. The source language is English and target
languages include Amharic (Ethiopic/Ge'ez script), Hausa, Swahili, Yorùbá
(with heavy diacritics), and Zulu [Q1]. Input documents are structured at the
article level, segmented into sentences using NLTK with linguist verification
[Q19, Q20, Q21], and delivered to translators in CSV format with explicit
paragraph-structure preservation instructions [Q118, Q119, Q122]. For model
evaluation, pseudo-document chunking splits documents into k-sentence segments
(k = 10 as primary setting) due to token-length limitations of most models
[Q48, Q49, Q123, Q124, Q125, Q126, Q128]. Amharic and Yorùbá exhibit the
largest average token counts across tokenizers due to non-Latin scripts and
diacritics respectively [Q127], and the Amharic token limit was specifically
increased to accommodate this [Q162]. Full-document translation is infeasible
for most open LLMs given their 8,192-token context ceiling [Q88, Q89]. The
input form thus imposes a structural ceiling on document-level fidelity that
is particularly acute for Amharic.

### Output Ontology
Ground-truth outputs are free-form reference translations produced by human
expert translators. There are no discrete label categories — output quality is
assessed via continuous or count-based metrics derived from comparison against
these references. The GPT-4o-as-judge evaluation defines four explicit quality
dimensions: fluency (rated 1–5) [Q180], content errors (CE — incorrect
translations, omissions, additions) [Q183, Q184], lexical cohesion errors
(LE — vocabulary usage, synonym selection, word overuse) [Q189], and
grammatical cohesion errors (GE — pronoun, conjunction, grammatical structure
problems) [Q190]. These dimensions are operationalized following Sun et al.
(2025) [Q179]. Cohesion is defined as how different parts of a text are
connected using grammar and vocabulary [Q187, Q188], with fluency scores
bounded 1–5 and CE/LE/GE being unbounded counts [Q191]. The output taxonomy
does not operationalize compliance with institutionally approved terminology
lists (e.g., MOH or EFDA glossaries), nor does it define document-level
terminological consistency as a scoreable criterion — a direct construct
gap for deployments where glossary compliance is the primary success criterion.

### Output Content
Human reference translations were produced by four expert translators per
language, recruited through a language coordinator who is also a native speaker
[Q23, Q24]. The 10,000 sentences per domain were distributed equally, with
translation done in-context (sentence level but with full document access) [Q25].
Translators attended a workshop on domain-specific terminology and were given
short translation guidelines [Q26]. Use of machine translation engines was
prohibited and quality assurance was described as capable of detecting such use
[Q120]. A terminology harmonization step was planned [Q121]. Each translator was
paid $1,250 for 2,500 sentences [Q31]. The four named Amharic translators are
Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, and Lidetewold Kebede [Q109];
however, the paper does not document their professional credentials, institutional
affiliations, or clinical backgrounds. It is not stated whether any Amharic
translator holds MOH clinical translation credentials or has been trained under
Ethiopia's Ministry of Health terminology standards. Quality control used
AfriCOMET QE (threshold 0.65 for manual review) [Q27, Q28, Q29], though QE
scores below this threshold do not necessarily reflect poor translations [Q30].
Human evaluation for direct assessment used three native-speaker annotators per
language, rating 80 documents on a 0–100 scale following the ESA protocol in
Appraise [Q194, Q195, Q196]. Krippendorff's alpha values were 0.46 (Amharic),
0.57 (Hausa), 0.40 (Swahili), 0.81 (Yorùbá), and 0.54 (Zulu) [Q211] —
relatively low except for Yorùbá [Q212, Q71]. No Zulu annotators could be
recruited [Q100]. Qualitative analysis was provided by one author per language,
each a native speaker [Q199, Q200].

### Output Form
The benchmark evaluates free-text translation output exclusively. Primary
automatic metrics are document-level BLEU (d-BLEU) and document-level chrF
(d-chrF), computed by realigning sentence or pseudo-document outputs into full
documents before scoring [Q51, Q57], using SacreBLEU with bootstrap resampling
(n = 1,000) for 95% confidence intervals [Q52]. chrF is prioritized over BLEU
because it better captures morphological richness in African languages [Q53].
AfriCOMET is used for sentence-level quality estimation [Q172] but excluded
from document-level scoring due to its 512-token context limit [Q175, Q176].
A long-context neural QE model (ModernBERT-base-long-context-qe-v1, trained on
WMT data including Hausa, Xhosa, and Zulu but not Amharic) produced nearly
identical scores across all models and offered no meaningful differentiation
[Q97, Q98]. GPT-4o-as-judge evaluation was limited to a few models due to cost
[Q178], and its ratings were consistent for translations into English but
inconsistent for African languages [Q99, Q218, Q219]. Human DA evaluation was
conducted for translations into four African languages (Zulu excluded) using
three native-speaker annotators [Q192]. Results tables covering all models,
domains, and evaluation granularities are provided [Q226, Q227, Q228, Q229,
Q230, Q231], along with per-prompt sensitivity figures [Q236, Q237, Q238, Q239].
The output form is fully text-based and well-matched to document translation
deployments; no modality mismatch concerns arise.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This paper introduces AFRIDOC-MT, a document-level multi-parallel translation dataset covering English and five African languages: Amharic, Hausa, Swahili, Yorùbá, and Zulu." |
| Q2 | 1 | input_ontology | "The dataset comprises 334 health and 271 information technology news documents, all human-translated from English to these languages." |
| Q3 | 1 | input_ontology | "We conduct document-level translation benchmark experiments by evaluating the ability of neural machine translation (NMT) models and large language models (LLMs) to translate between English and these languages, at both the sentence and pseudo-document levels, the outputs being realigned to form complete documents for evaluation." |
| Q4 | 1 | output_form | "Our results indicate that NLLB-200 achieves the best average performance among the standard NMT models, while GPT-4o outperforms general-purpose LLMs." |
| Q5 | 1 | input_ontology | "Fine-tuning selected models leads to substantial performance gains, but models trained on sentences struggle to generalize effectively to longer documents." |
| Q6 | 1 | output_ontology | "Furthermore, our analysis reveals that some LLMs exhibit issues such as under-generation, over-generation, repetition of words and phrases, and off-target translations, specifically for translation into African languages." |
| Q7 | 1 | input_ontology | "In addition, AFRIDOC-MT supports multi-way translation, allowing translations not only between English and the African languages but also between any two of the languages covered." |
| Q8 | 1 | output_form | "We evaluate performance using automatic metrics and compare the results of encoder-decoder models with decoder-only LLMs" |
| Q9 | 1 | output_content | "Jesujoba O. Alabi, Israel Abebe Azime, Miaoran Zhang, Cristina España-Bonet, Rachel Bawden, Dawei Zhu, David Ifeoluwa Adelani, Clement Oyeleke Odoje, Idris Akinade, Iffat Maab, Davis David, Shamsuddeen Hassan Muhammad, Neo Putini, David O. Ademuyiwa, Andrew Caines, Dietrich Klakow" |
| Q10 | 1 | output_content | "Masakhane NLP, Saarland University, Saarland Informatic Campus, DFKI GmbH, Barcelona Supercomputing Center, Inria Paris France, Mila McGill University & Canada CIFAR AI Chair, University of Ibadan Nigeria, National Institute of Informatics Japan, Selcom Tanzania, Imperial College London, University of KwaZulu-Natal, Loughborough University U.K, University of Cambridge U.K." |
| Q11 | 2 | input_content | "There exist several MT evaluation benchmark datasets for African languages." |
| Q12 | 2 | input_ontology | "They can be categorized into two kinds. First, evaluation datasets specifically designed for translating into or from African languages (Ezeani et al., 2020; Azunre et al., 2021; Adelani et al., 2021, 2022, inter alia). Second, benchmark datasets covering many languages, including African languages." |
| Q13 | 2 | input_form | "However, most of these datasets are designed for sentence-level MT, primarily drawn from religious or news domains, although some consist of translated sentences originating from the same document." |
| Q14 | 2 | input_ontology | "To the best of our knowledge, only TICO-19, a health domain translation benchmark, has the potential to be used for document-level MT, while it is restricted to topics related to COVID-19." |
| Q15 | 2 | input_ontology | "Document-level NMT aims to overcome the limitations of sentence-level systems by translating an entire document as a whole." |
| Q16 | 2 | input_ontology | "Both document-level and context-aware MT allow for the possibility of improving translation quality for context-dependent phenomena such as coreference resolution (Müller et al., 2018; Bawden et al., 2018; Voita et al., 2018; Herold and Ney, 2023), lexical disambiguation (Rios Gonzales et al., 2017; Martínez Garcia et al., 2019), and lexical cohesion (Wong and Kit, 2012; Garcia et al., 2014, 2017; Bawden et al., 2018; Voita et al., 2019)." |
| Q17 | 2 | input_ontology | "Various methods have been proposed to extend sentence-level models to capture document-level context (Tiedemann and Scherrer, 2017; Libovický and Helcl, 2017; Bawden et al., 2018; Miculicich et al., 2018; Sun et al., 2022)." |
| Q18 | 3 | input_content | "We scraped English articles from the websites of Techpoint Africa and the World Health Organization (WHO). The articles cover different topics of different lengths with an average length of 30 and 37 sentences for health and tech respectively." |
| Q19 | 3 | input_form | "While our corpus is initially structured at the article level, we aim to make it suitable for sentence-level translation tasks as well." |
| Q20 | 3 | input_form | "To achieve this, we segmented the raw articles into sentences using NLTK (Bird et al., 2009)." |
| Q21 | 3 | input_form | "To ensure high segmentation quality, we recruited a linguist and a professional translator to verify the correctness of the segmentation and make corrections as needed." |
| Q22 | 3 | input_content | "Finally, we selected 334 and 271 English articles/documents from the health and tech domains respectively, which represents 10k sentences each per domain." |
| Q23 | 3 | output_content | "We translated the extracted 10k English sentences to the 5 African languages through 4 expert translators per language." |
| Q24 | 3 | output_content | "The translators were recruited through a language coordinator who is also a native speaker of the language." |
| Q25 | 3 | output_content | "The 10k sentences were distributed equally among the translators and the translations were done in-context (i.e. the translators translated on the sentence level but had access to the whole document)." |
| Q26 | 3 | output_content | "Due to the domain-specific nature of the task, before starting the translation process, we conducted a translation workshop, during which three translation experts shared their experiences in creating terminologies and they also shared existing resources with the translators including short translation guidelines (Appendix A.1)." |
| Q27 | 3 | output_content | "Quality control was conducted using automated quality estimation, followed by manual inspections by our language coordinators." |
| Q28 | 3 | output_content | "We also used Quality Estimation (QE), specifically AfriCOMET (Wang et al., 2024a), Given a translated sentence in any African language and its corresponding source English sentence, AfriCOMET generates a score between 0 and 1, where 0 indicates poor quality and higher values signify better quality." |
| Q29 | 3 | output_content | "The translators, in collaboration with the language coordinators, were tasked with reviewing instances that had quality estimation scores below 0.65." |
| Q30 | 3 | output_content | "Manual inspection indicates that QE scores below 0.65 do not necessarily reflect poor translations, consistent with Adelani et al. (2024b), likely due to" |
| Q31 | 3 | output_content | "Each translator was paid $1, 250 for 2, 500 sentences." |
| Q32 | 4 | input_form | "We created train, development (dev), and test splits for each domain. To prevent data leakage, documents sharing sentences with the same English translation were assigned to the training set. The dev set contains 25–33 documents, and the test set 59–61 documents, drawn from the remaining data." |
| Q33 | 4 | input_form | "Table 4 shows the average number of whitespace-separated tokens per sentence across domains and languages, including English. The health domain has more tokens than tech. Hausa and Yorùbá are longer than English, likely due to their descriptive nature, while Swahili is similar in length. Amharic and Zulu are relatively shorter, reflecting interesting linguistic properties." |
| Q34 | 4 | input_content | "The health data is licensed under CC BY-NCSA 3.0, while the tech data is licensed under CC BY-NC-SA 4.0." |
| Q35 | 4 | input_ontology | "Given the AFRIDOC-MT data, we conducted both sentence- and document-level translation, evaluating two types of models: encoder-decoder and decoder-only models. While the majority of these models are open-source, we also evaluated two proprietary models of the same type." |
| Q36 | 4 | output_form | "Our evaluation primarily focuses on document-level translation, reflecting the availability of our document-level translation corpus. For completeness, we also conduct a series of sentence-level experiments, with the results presented in Appendix C." |
| Q37 | 4 | input_ontology | "We evaluate five kinds of open encoder-decoder model including Toucan (Elmadany et al., 2024; Adebara et al., 2024), M2M-100 (Fan et al., 2020), NLLB200 (NLLB Team et al., 2024), MADLAD400 (Kudugunta et al., 2023), and Aya-101 (Üstün et al., 2024)." |
| Q38 | 4 | input_ontology | "Toucan is an Afro-centric multilingual MT model supporting 150 African language pairs. In comparison, M2M-100, NLLB-200, and MADLAD-400 cover between 100 and 450 language pairs. Aya-101, an instruction-tuned mT5 model (Xue et al., 2021), supports 100 languages and can translate between various languages, including those considered in AFRIDOC-MT." |
| Q39 | 4 | input_ontology | "We also evaluate open and closed decoder-only models. Open models include LLama3.1 (Dubey et al., 2024), Gemma2 (Gemma Team et al., 2024), their instruction-tuned variants, and LLaMAX3 (Lu et al., 2024)—a LLama3-based model further pre-trained on 100+ languages, including several African ones. The closed models include OpenAI GPT models (GPT-3.5 Turbo and GPT-4o) (OpenAI, 2024), which have been shown to have document-level translation ability (Wang et al., 2023)." |
| Q40 | 4 | input_content | "While their language coverage is not well documented, they show some ability to handle African languages (Adelani et al., 2024b; Bayes et al., 2024), though far below their performance in English, their primary training language." |
| Q41 | 4 | input_ontology | "We present the result of 12 models in total, including the 1.2B version of Toucan, 1.3B and 3.3B versions of NLLB-200, 3B and 13B versions of MADLAD-400 and Aya-101 respectively. We also have the 8B instruction tuned version of LLama3.1 (LLama3.1-IT), 9B version of Gemma-2 (Gemma2-IT), and LLaMAX3-Alpaca." |
| Q42 | 4 | input_ontology | "For sentence-level evaluation, we jointly fine-tune NLLB-200 with 1.3B parameters on the 30 language directions and on the two domains to make the models more specialized. Similarly, we did supervised fine-tuning (SFT) on LLaMAX3" |
| Q43 | 5 | input_form | "We perform SFT on LLaMAX3 and LLama3.1 for document-level translation, using pseudo-documents with k=10." |
| Q44 | 5 | output_form | "Given that our created dataset can be used for sentence-level translation and as a baseline for document-level translation, we evaluate all models on the test splits for each domain." |
| Q45 | 5 | output_form | "We evaluate the translation models (M2M-100, NLLB-200, and MADLAD-400) using the Fairseq (Ott et al., 2019) codebase for (M2M-100 and NLLB-200), and the Transformers (Wolf et al., 2020) codebase for MADLAD-400." |
| Q46 | 5 | output_form | "However, for other models including Aya-101, we use the EleutherAI LM Evaluation Harness (lm-eval) tool (Biderman et al., 2024) using the three templates listed in Table 23 of Appendix B.4." |
| Q47 | 5 | input_form | "An initial analysis showed that some models were unable to process entire documents due to input length limits, which were exceeded by token counts in some languages (Amharic and Yorùbá)." |
| Q48 | 5 | input_form | "To address this, we adopted a similar approach to Lee et al. (2022), splitting documents into fixed-size chunks of k sentences to fit within token limits; the final chunk may contain fewer than k sentences." |
| Q49 | 5 | input_form | "To select an appropriate chunk size, we conducted initial tests with k = 1 (sentence-level), 5, 10, and 25, choosing k = 10 for our experiments." |
| Q50 | 5 | output_form | "Evaluating document-level translation remains challenging, as existing automatic metrics struggle to capture improvements and account for discourse phenomena (Jiang et al., 2022; Dahan et al., 2024), and embedding-based metrics have not been explored in this context for African languages due to the lack of data." |
| Q51 | 5 | output_form | "Hence, we realigned sentence-level or pseudo-translation outputs into full documents, then computed BLEU (Papineni et al., 2002) and chrF (Popović, 2015) to create document BLEU (d-BLEU) and document chrF (d-chrF)." |
| Q52 | 5 | output_form | "Metrics were computed using SacreBLEU (Post, 2018) with bootstrap resampling (n = 1000) to report 95% confidence intervals." |
| Q53 | 5 | output_form | "We report d-chrF scores for the best prompt per model and language direction in the main text, as chrF better captures the morphological richness of African languages (Adelani et al., 2022), with full results provided in Appendix C." |
| Q54 | 5 | output_form | "We use GPT-4o as a judge to evaluate translation outputs, following recent work showing LLMs' effectiveness in assessing translation quality and analyzing errors (Wu et al., 2024; Sun et al., 2025)." |
| Q55 | 5 | output_form | "Following Sun et al. (2025), we assess each translated document's fluency, content errors (CE), and cohesion errors—specifically lexical (LE) and grammatical (GE) errors—using GPT-4o, with evaluation limited to a few model outputs due to cost constraints (Appendix B.6)." |
| Q56 | 5 | output_content | "We also complement this with human evaluation for direct assessment scores (Appendix B.7) and qualitative analysis through manual inspection (Appendix B.8)." |
| Q57 | 5 | output_form | "In Tables 5 and 6 we present d-chrF scores based on the realigned documents, created by merging the translated sentences into their corresponding documents." |
| Q58 | 5 | output_form | "On average the NLLB models obtain scores of 65.4/66.6 and 64.3/65.0 on health and tech domains respectively, with 3.3B outperforming 1.3B except when translating into Yorùbá." |
| Q59 | 5 | output_form | "Furthermore, translating to African languages is significantly worse compared to translating to English for all the models." |
| Q60 | 6 | output_form | "In Tables 7 and 8 we present d-chrF scores based on the best prompt per language for the translation output of the models when evaluated on the realigned documents from pseudo-documents with k =10 sentences per pseudo-document." |
| Q61 | 6 | output_form | "Pseudo-document translation is worse than sentence-level translation when translating into African languages Our results from pseudo-document translation show a performance drop across different models compared to sentence-level translation, especially when translating into African languages." |
| Q62 | 6 | output_form | "However, GPT-4o demonstrates similar and consistent performance in both setups and domains." |
| Q63 | 6 | output_form | "Additionally, we observe that GPT-3.5 is the next best performing decoder-only LLM, which contrasts with its performance in sentence-level translation." |
| Q64 | 7 | output_form | "Table 9 presents average GPT-4o evaluations for fluency and content errors (CE) of realigned outputs from sentence-level and pseudo-document-level tasks (k=10) across four models in the health domain." |
| Q65 | 7 | output_form | "When translating into English, pseudo-document outputs are generally rated as more fluent and show fewer content errors, except for LLaMAX3-SFT1, which, when evaluated on pseudo-documents, shows lower fluency but still fewer content errors—an outcome that is counterintuitive." |
| Q66 | 7 | output_ontology | "However, when translating into African languages, the results are less consistent." |
| Q67 | 7 | output_form | "These inconsistencies raise concerns about GPT-4o's reliability." |
| Q68 | 7 | output_form | "Consequently, we focus on human evaluation going forward." |
| Q69 | 7 | output_form | "In Table 10 we report average direct assessment (DA) scores (on a scale from 0 to 100) from three annotators per language for the health domain, when translating into four African languages." |
| Q70 | 7 | output_content | "For each language, we used 30 documents across models and both domains to compute inter-annotator" |
| Q71 | 8 | output_content | "We obtained Krippendorff's alpha values of ≥ 0.40, which are relatively low due to the fine granularity of the evaluation scale." |
| Q72 | 8 | output_form | "Human evaluation results align closely with d-chrF, which favors sentence-level translations over pseudo-document translations when translating into African languages." |
| Q73 | 8 | output_form | "Among the models, LLaMAX3-SFT1 receives higher ratings at the sentence-level but is rated lower when translating pseudo-documents." |
| Q74 | 8 | output_form | "In contrast, LLaMAX3-SFT10 receives slightly lower ratings than LLaMAX3-SFT1 at the sentence-level but is rated higher in the pseudo-document setting." |
| Q75 | 8 | output_form | "GPT-3.5 is generally rated as the weakest model across languages, except for Swahili, where its performance is comparatively better." |
| Q76 | 8 | output_content | "Our qualitative analysis, based on feedback from native speakers who are also authors, indicates that GPT-3.5 frequently over-generates in the pseudo-document setup by repeating words and phrases—except in Swahili, where it performs best." |
| Q77 | 8 | output_content | "However, for Yorùbá, it often uses inconsistent or partial diacritics, resulting in inaccuracies." |
| Q78 | 8 | output_form | "LLaMAX3-SFT1 also exhibits repetition in pseudo-document translations, likely due to a length generalization problem (Anil et al., 2022), and does so more than LLaMAX3-SFT10." |
| Q79 | 8 | output_form | "For the other four languages, LLaMAX3-SFT1 with the sentence-level setup was rated higher than other models and configurations, owing to better context preservation and fewer repetitions." |
| Q80 | 9 | input_content | "We introduce AFRIDOC-MT, a document-level translation dataset in the health and tech domains for five African languages." |
| Q81 | 9 | input_ontology | "We benchmarked various models, fine-tuning selected ones." |
| Q82 | 9 | input_form | "Due to context length limits, documents were translated either sentence by sentence or as pseudo-documents." |
| Q83 | 9 | output_form | "Outputs were evaluated using standard MT metrics, GPT-4o as a judge, and human direct assessment." |
| Q84 | 9 | output_form | "NLLB-200 was the strongest built-in MT model, while GPT-4o outperformed general-purpose LLMs." |
| Q85 | 9 | output_form | "However, our DA and qualitative analysis found GPT-4o's judgments inconsistent for African languages, and sentence-by-sentence translation proved more effective for some languages." |
| Q86 | 9 | input_ontology | "We evaluated only a small subset of the numerous multilingual LLMs available." |
| Q87 | 9 | input_form | "Our experiments were also limited by the context length of the LLMs, particularly for open LLMs." |
| Q88 | 9 | input_form | "Except for LLama3.1, all other open LLMs have a context length of 8192 tokens, while encoder-decoder models were primarily based on T5." |
| Q89 | 9 | input_form | "This makes it difficult to use the context length beyond a certain limit, making full document translation infeasible." |
| Q90 | 9 | input_form | "LLMs are prone to variance in performance based on the prompt." |
| Q91 | 9 | input_ontology | "We therefore evaluated them for translation using three different prompts." |
| Q92 | 9 | input_form | "However, it is possible that our prompts were not optimal." |
| Q93 | 10 | input_ontology | "Africa is home to thousands of indigenous languages, many of which exhibit unique linguistic properties. However, due to the high cost of translation using human translators and limited available funding, it is currently impossible to cover all languages. As a result, we focused on just five languages." |
| Q94 | 10 | input_ontology | "AFRIDOC-MT is a multi-way parallel dataset. However, due to the cost of running inference over three prompts and across all 30 translation directions for all the models evaluated, most of our analysis is limited to translation tasks between English and the five African languages." |
| Q95 | 10 | output_form | "While we fine-tuned NLLB-200, LLama3.1 and LLaMAX3 on all 30 directions, we only provide results from NLLB-200 for all directions both before and after fine-tuning for sentence-level and pseudo-document tasks in the Appendix D." |
| Q96 | 10 | output_form | "Quality evaluation in MT is an open and ongoing area of research, especially for document-level translation. Recent works have proposed embedding-based metrics for evaluation at both the sentence and document levels. While this has been well explored for high-resource language pairs, it remains underexplored for African languages, although there is a tool, AfriCOMET, that works for sentence-level evaluation in African languages." |
| Q97 | 10 | output_form | "However, we evaluated the document-level translation outputs using ModernBERT-base-long-context-qe-v1, trained on the WMT human evaluation dataset across 41 language pairs, including over 20 languages and three African languages (Hausa, Xhosa, and Zulu), two of which are included to our work." |
| Q98 | 10 | output_form | "However, the scores were nearly identical across all models, offering no meaningful differentiation. Hence, for our document-level evaluation, in addition to lexical-based metrics, we incorporated three other evaluation approaches: using GPT-4o as a judge, human evaluation, and qualitative analysis." |
| Q99 | 10 | output_form | "GPT-4o was employed to assess and rate the translation outputs of four models. While its ratings were consistent for translations into English, the same was not observed for translations into African languages, likely due to the model's limited understanding of these languages." |
| Q100 | 10 | output_content | "Therefore, we conducted a human evaluation for translations from English to African languages, comparing only three models due to cost constraints. However, we were unable to recruit annotators for Zulu." |
| Q101 | 10 | input_ontology | "While we fine-tuned both NLLB-1.3B and LLaMAX3 models across all 30 language directions, due to computational constraints and the high cost of qualitative evaluation, our detailed analysis focuses only on translation between English and the 5 African languages." |
| Q102 | 10 | output_form | "Nevertheless, we report quantitative results across all 30 directions for NLLB-1.3B. We will make all fine-tuned models publicly available to support future work, and we hope that further research will explore the remaining translation directions in greater depth." |
| Q103 | 10 | input_content | "A potential limitation of our dataset is the influence of translationese (Koppel and Ordan, 2011). Since all source material translated originates in English, translated sentences in African languages may exhibit patterns such as unnatural syntax or overly literal phrasing." |
| Q104 | 10 | input_content | "Although we have not conducted an analysis to quantify these effects, prior work suggests that they can affect MT model performance, generalization and evaluation including direct assessment (Freitag et al., 2019; Edunov et al., 2020)." |
| Q105 | 10 | input_content | "Furthermore, AFRIDOC-MT may reflect a bias toward English in terms of structure, semantics, and cultural framing. We leave a deeper investigation of these issues to future work." |
| Q106 | 10 | input_content | "AFRIDOC-MT was created with the utmost consideration for ethical standards. The English texts translated were sourced from publicly available and ethically sourced materials. The data sources were selected to represent different cultural perspectives, with a focus on minimizing any potential bias." |
| Q107 | 10 | input_content | "Efforts were made to ensure the dataset does not include harmful, biased, or offensive content via manual inspection." |
| Q108 | 10 | output_content | "This work was carried out with support from Lacuna Fund, an initiative co-founded by The Rockefeller Foundation, Google.org, and Canada's International Development Research Centre. This research project has benefited from the Microsoft Accelerate Foundation Models Research (AFMR)" |
| Q109 | 11 | output_content | "Also, we also appreciate the translators whose names we have listed below: 1. Amharic: Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, Lidetewold Kebede 2. Hausa: Junaid Garba, Umma Abubakar, Jibrin Adamu, Ruqayya Nasir Iro 3. Swahili: Mohamed Mwinyimkuu, Laanyu koone, Baraka Karuli Mgasa, Said Athumani Said 4. Yorùbá: Ifeoluwa Akinsola, Simeon Onaolapo, Ganiyat Dasola Afolabi, Oluwatosin Koya 5. Zulu: Busisiwe Pakade, Rooweither Mabuya, Tholakele Zungu, Zanele Thembani" |
| Q110 | 11 | output_content | "Lastly, we thank the human annotators who were not part of the translation team." |
| Q111 | 11 | output_content | "We acknowledge the support of OpenAI for providing API credits through their Researcher Access API programme." |
| Q112 | 11 | output_content | "Jesujoba Alabi acknowledges the support of the BMBF's (German Federal Ministry of Education and Research) SLIK project under the grant 01IS22015C." |
| Q113 | 11 | output_content | "The work has also been partially funded by BMBF through the TRAILS project (grant number 01IW24005)." |
| Q114 | 11 | output_content | "Miaoran Zhang received funding from the DFG (German Research Foundation) under project 232722074, SFB 1102." |
| Q115 | 11 | output_content | "CEB acknowledges her AI4S fellowship within the "Generación D" initiative by Red.es, Ministerio para la Transformación Digital y de la Función Pública, for talent attraction (C005/24-ED CV1), funded by NextGenerationEU through PRTR." |
| Q116 | 11 | output_content | "R. Bawden's participation was partly funded by her chair in the PRAIRIE institute, funded by the French national agency ANR, as part of the "Investissements d'avenir" programme under the reference ANR-19-P3IA-0001 and by the French Agence Nationale de la Recherche (ANR) under the projects TraLaLaM ("ANR-23-IAS1-0006") and MaTOS ("ANR-22-CE23-0033")." |
| Q117 | 11 | output_content | "David Adelani acknowledges the funding of IVADO and the Canada First Research Excellence Fund." |
| Q118 | 18 | input_form | "Each file contains 2500 sentences, and they are named in the format of a serial number followed by your first name." |
| Q119 | 18 | input_form | "Please do not delete double empty rows, as they serve to separate paragraphs. Also, avoid deleting any rows, columns, or provided text." |
| Q120 | 18 | output_content | "Use the language field to input the translations. It is essential not to rely on translation engines, as our quality assurance process can detect this. Depending on such tools may result in potential issues that you would need to address, leading to additional work on your part." |
| Q121 | 18 | output_content | "We will provide a list of extracted terminologies soon so that you can harmonize how terminologies are translated." |
| Q122 | 18 | input_form | "The files are in .csv format, and you can open them using Google Sheets or Microsoft Excel (for offline work)." |
| Q123 | 19 | input_form | "Given that the translated documents vary in length in terms of sentences and tokens, and considering the maximum token length limitations of the different LLMs used, we adopted a chunking approach for document-level evaluation." |
| Q124 | 19 | input_form | "In this approach, documents were divided into smaller pseudo-documents that fit within the maximum length constraints of the models." |
| Q125 | 19 | input_form | "To establish an appropriate chunk size, each document was divided into fixed-size chunks of k sentences, with the possibility that the final chunk may contain fewer than k sentences." |
| Q126 | 19 | input_form | "We conducted an initial analysis, testing different values for k (5, 10, and 25), with k=1 serving as our sentence-level setup." |
| Q127 | 19 | input_form | "Our analysis revealed that Amharic and Yorùbá—languages with unique characteristics such as non-Latin scripts and diacritics, respectively—had the largest average token counts across the tokenizers." |
| Q128 | 19 | input_form | "To accommodate both languages in our experiments, we chose pseudo-documents with k=10." |
| Q129 | 19 | input_form | "However, for the SFT models described in Appendix B.2, we used both k=5 and k=10." |
| Q130 | 19 | input_ontology | "M2M-100 (Fan et al., 2020) is a transformer-based multilingual neural translation model from Meta, trained to translate between 100 languages, including several African languages." |
| Q131 | 19 | input_ontology | "It has three variants of different sizes: 400M parameters, 1.2B parameters, and 12B parameters." |
| Q132 | 19 | input_ontology | "For our experiments, we evaluated the 400M and 1.2B variants." |
| Q133 | 19 | input_ontology | "NLLB (NLLB Team et al., 2024) is a model similar to M2M-100, with broader coverage, trained to translate between just over 200 languages, including more than 50 African languages." |
| Q134 | 19 | input_ontology | "It also has different sizes: 600M, 1.3B, 3.3B, and 54B parameters." |
| Q135 | 19 | input_ontology | "For this work, we evaluated the first three variants." |
| Q136 | 19 | input_ontology | "MADLAD-400 (Kudugunta et al., 2023) is a multilingual translation model based on the T5 architecture (Raffel et al., 2020), covering 450 languages, including many African languages." |
| Q137 | 19 | input_content | "It was trained on data collected from the Common Crawl dataset." |
| Q138 | 19 | input_content | "The dataset underwent a thorough self-audit to filter out noisy content and ensure its quality for training MT models." |
| Q139 | 19 | input_ontology | "Toucan (Elmadany et al., 2024; Adebara et al., 2024) is another multilingual but Afro-centric translation model based on the T5 architecture, covering 150 language pairs of African languages." |
| Q140 | 19 | input_content | "It was first pre-trained on large multilingual texts covering over 500 African languages and then finetuned on translation task covering over 100 language pairs." |
| Q141 | 20 | input_ontology | "Aya-101 (Üstün et al., 2024) is an instruction-tuned mT5 model (Xue et al., 2021) designed to handle both discriminative and generative multilingual tasks. With 13B parameters, it covers 100 languages and is capable of translating between a wide range of languages, including African languages." |
| Q142 | 20 | input_ontology | "Gemma2 (Gemma Team et al., 2024) is a decoder-only LLM trained on billions of tokens sourced from the web. The training data primarily consists of English-language text, but it also includes code and mathematical content. While Gemma2 has an English-centric focus, it also possesses multilingual capabilities. We evaluate the base Gemma2 model with 9B parameters, as well as its instruction-tuned version." |
| Q143 | 20 | input_ontology | "LLama3.1 (Dubey et al., 2024) is another decoder-only LLM trained on trillions of tokens across multiple languages. It was fine-tuned using existing instruction datasets as well as synthetically generated instruction data to create its instruction-tuned version. One advantage LLama3.1 has over other models is its context window of 128K tokens, the largest among all models considered in this work, making it particularly suitable for document-based tasks such as document-level translation. We evaluate the base LLama3.1 model with 8B parameters, as well as its instruction-tuned version." |
| Q144 | 20 | input_ontology | "LLaMAX3 (Lu et al., 2024) is a multilingual LLM built on the LLama3 with 8B parameters as its base. It was trained on 102 languages, including several African languages, through continued pretraining. Using an English instruction dataset (Alpaca), it was further fine-tuned to create LLaMAX3-Alpaca. We evaluated both models and compared their performance across various tasks." |
| Q145 | 20 | input_form | "We perform supervised fine-tuning to tailor LLMs for translation tasks. To train sentence-level MT systems, we use all parallel sentences from AFRIDOC-MT to construct the training set, enabling the LLMs to translate across multiple directions and domains. Following Zhu et al. (2024b), we augment the parallel data with translation instructions, which are randomly sampled from a predefined set of 31 MT instructions for each training example." |
| Q146 | 21 | input_form | "To train document-level MT systems, we follow the same process, but train on longer segments formed by concatenating multiple sentences." |
| Q147 | 21 | input_form | "When fine-tuning, we use a learning rate of 5e−6 and an effective batch size of 64." |
| Q148 | 21 | input_ontology | "Models are trained for only one epoch, as further training does not result in improvements and may even lead to performance degradation." |
| Q149 | 21 | input_form | "we fine-tuned the 1.3B version of NLLB-200 for sentence and pseudo-document (with 10 sentences) translation using the Fairseq (Ott et al., 2019) codebase." |
| Q150 | 21 | input_content | "We used all the training examples from 30 language directions across both domains." |
| Q151 | 21 | input_form | "The model was fine-tuned for 50k steps using a learning rate of 5e−5, token batch size of 2048 and a gradient accumulation of 2." |
| Q152 | 21 | input_form | "The checkpoint with the lowest validation loss was selected as the best model for evaluation." |
| Q153 | 21 | output_form | "The models were evaluated using different tools. For example, both the NLLB-200 and M2M-100 models were evaluated with the Fairseq codebase, while Toucan and MADLAD-400 were evaluated using the Hugging Face (HF) codebase." |
| Q154 | 21 | output_form | "All other LLMs, including LLama3.1 (both instruction-tuned and SFT models), Gemma, and Aya-101, were evaluated using EleutherAI LM Evaluation Harness (lm-eval) tool (Biderman et al., 2024)." |
| Q155 | 21 | output_form | "In all cases, greedy decoding was used." |
| Q156 | 21 | input_form | "The models evaluated have different context lengths. For encoder-decoder models, M2M-100 and NLLB have a maximum sequence length of 1024 and 512 respectively." |
| Q157 | 21 | output_form | "Aya-101 and MADALAD, based on the T5 architecture, do not have a pre-specified maximum sequence length, so we fixed their maximum sequence length to 1024 for all experiments involving encoder-decoder models." |
| Q158 | 21 | input_form | "However, for decoder-only models, Gemma and LLaMAX3 (based on LLama3) have a maximum sequence length of 8192, while LLama3.1 has a maximum sequence length of 128K." |
| Q159 | 21 | output_form | "Since all the decoder-only models were evaluated using LM Evaluation Harness, we used a similar setup for them, selecting the maximum length based on the specific needs of each model." |
| Q160 | 21 | input_form | "These numbers were chosen based on the statistics from Table 11." |
| Q161 | 21 | input_form | "However, for Amharic, when translating pseudo-documents with 25 sentences and full documents, there were instances exceeding the 95th percentile derived from the training statistics." |
| Q162 | 21 | input_form | "Therefore, we increased the token limit specifically for Amharic." |
| Q163 | 21 | output_form | "While the translation models we evaluated do not require prompts, MADLAD-400, requires a prefix of the form <2xx> token, which is prepended to the source sentence." |
| Q164 | 21 | output_form | "Similarly, Toucan uses just the target language ISO-693 code as prefix, which is prepended to the source sentence (e.g., "swa" for Swahili)." |
| Q165 | 21 | output_form | "For other models, including Aya-101, we used three different prompts for sentence-level translation and document translation experiments." |
| Q166 | 21 | output_form | "The main difference between the prompts for these tasks is the explicit mention of "text" or "document" within the prompt, as shown in Table 23." |
| Q167 | 21 | output_form | "For the base models Gemma2, Llama3.1, LLaMAX3, and Aya-101, we prompted them directly using the respective prompts." |
| Q168 | 21 | output_form | "However, for the instruction-tuned versions of Gemma2 and Llama3.1, we used their respective chat templates." |
| Q169 | 21 | output_form | "For all Alpaca-based models, including our SFT models, we used the Alpaca template." |
| Q170 | 21 | output_form | "We evaluate translation quality with BLEU (Papineni et al., 2002) and ChrF (Popović, 2015) using SacreBLEU (Post, 2018)." |
| Q171 | 21 | output_form | "We run significance tests using bootstrap resampling and report the 95%" |
| Q172 | 22 | output_form | "We also use AfriCOMET (Wang et al., 2024a) to evaluate the quality of the translation outputs." |
| Q173 | 22 | output_form | "We report the chrF scores of the best prompt for each model and language direction in the main paper, with all additional results provided in the Appendix C." |
| Q174 | 22 | input_ontology | "For document-level experiments, we evaluated the LLMs using the same three prompts as in the sentence-level experiment." |
| Q175 | 22 | output_form | "For evaluation, we used BLEU and chrF scores but excluded AfriCOMET due to its backbone model, AfroXLM-R-L (Alabi et al., 2022; Adelani et al., 2024a), having a context length of 512 tokens." |
| Q176 | 22 | output_form | "This made it impractical to compute COMET scores for document-level outputs." |
| Q177 | 22 | output_form | "We use GPT-4o to assess the quality of translation output, as demonstrated by Sun et al. (2025), which shows a correlation with human judgment." |
| Q178 | 22 | output_form | "Due to the cost of this task, we limited our evaluation to a few selected models, including Aya-101, GPT-3.5, GPT-4o, and LLaMAX3 fine-tuned on AFRIDOC-MT sentences and pseudo-documents of 10 sentences." |
| Q179 | 22 | output_ontology | "We compared translations performed at the sentence-level and pseudo-document level in terms of fluency, content errors, and cohesion errors—specifically lexical (LE) and grammatical (GE) errors—using the same definitions as Sun et al. (2025)." |
| Q180 | 22 | output_ontology | "GPT-4o is prompted to rate the fluency of a document on a scale from 1 to 5, where 5 indicates high fluency and 1 represents low fluency." |
| Q181 | 22 | output_form | "This evaluation is conducted without providing any reference document." |
| Q182 | 22 | output_form | "For the final fluency score, we report the average rating across all documents." |
| Q183 | 22 | output_ontology | "GPT-4 is prompted to identify and list the mistakes, such as incorrect translations, omissions, additions, and any other errors, by comparing the model's output to the reference translation." |
| Q184 | 22 | output_ontology | "After identifying these errors, we count all of them and compute the average across all documents, reporting that as the content error (CE)." |
| Q185 | 23 | output_ontology | "Cohesion: GPT-4 is prompted to rate cohesion-related mistakes, including lexical and grammatical errors, in the model's output, comparing it to the reference translation." |
| Q186 | 23 | output_ontology | "We count each error individually, compute the average across the documents, and report them as lexical errors (LE) and grammatical errors (GE)." |
| Q187 | 23 | output_ontology | "Cohesion refers to how different parts of a text are connected using language structures like grammar and vocabulary." |
| Q188 | 23 | output_ontology | "It ensures that sentences flow smoothly and the text makes sense as a whole." |
| Q189 | 23 | output_ontology | "Lexical Cohesion Mistakes: Issues with vocabulary usage, incorrect or missing synonyms, or overuse of certain words that disrupt the flow." |
| Q190 | 23 | output_ontology | "Grammatical Cohesion Mistakes: Problems with pronouns, conjunctions, or grammatical structures that link sentences and clauses." |
| Q191 | 24 | output_ontology | "Fluency can only have values between 1 and 5. However, the other metrics, including CE, GE, and LE, do not have a specific range and can take on any value because they are counts." |
| Q192 | 24 | output_content | "Beyond using GPT-4o as a judge, we also conduct human evaluation on a subset of outputs from GPT-3.5, LLaMAX3-SFT1, and LLaMAX3-SFT10 for two domains, focusing specifically on translation into five African languages due to cost constraints." |
| Q193 | 24 | output_form | "Translation into English was excluded, as existing automatic metrics, including GPT-based evaluations, are already reliable for this direction." |
| Q194 | 24 | output_content | "For the human evaluation, three native speakers of the African languages—primarily translators involved in the dataset creation—were recruited." |
| Q195 | 24 | output_content | "Each annotator was assigned 80 documents to evaluate, tasked with marking as many error spans as possible and rating the overall quality on a scale from 0 to 100." |
| Q196 | 24 | output_form | "This annotation followed the error span annotation (ESA) (Kocmi et al., 2024) protocol as implemented within the Appraise Evaluation Framework (Federmann, 2018)." |
| Q197 | 24 | output_content | "To assess consistency and inter-annotator agreement, 30 of the 80 documents were shared among all three annotators." |
| Q198 | 24 | output_content | "Each annotator was remunerated with $55.15" |
| Q199 | 24 | output_content | "Alongside the human direct assessment of the translation outputs, we shared a subset of the outputs with one author per language, each a native speaker." |
| Q200 | 24 | output_content | "They were tasked with analyzing the outputs to answer two key questions: (1) What common errors or flaws do the models exhibit across different setups? and (2) How fluent are the translation outputs produced by the models across the various settings?" |
| Q201 | 24 | input_form | "Given that AFRIDOC-MT is a document-level translation dataset, and due to the limited context length of most translation models and LLMs, which makes it impossible to translate a full document at once, we opted to translate the sentences within the documents and then merge them back to form the complete document. For document-level evaluation, we split the documents into chunks of 10 sentences and translate these chunks using the different models." |
| Q202 | 25 | output_form | "In Tables 19 and 20 we provide the full results on the merged pseudo-documents using d-chrF and d-BLEU." |
| Q203 | 25 | input_form | "It is important to note that we also trained and evaluated NLLB-200 for pseudo-document translation. However, due to its 512-token maximum sequence length, it is not competitive." |
| Q204 | 25 | output_form | "Our results show that both LLama3.1 and LLaMAX3 models, when fine-tuned on sentences, performed significantly worse on pseudo-document evaluations compared to the same models fine-tuned on pseudo-documents for both domains." |
| Q205 | 25 | input_form | "All these models were trained using a similar setup, with the primary difference being the data used for fine-tuning." |
| Q206 | 25 | output_form | "Overall, no clear trend is observed in MT performance across language family classes. However, Amharic (a non-Latin script language) and Yorùbá (a heavily diacriticitized language) result in the lowest chrF scores, while Swahili—the most widely spoken indigenous African language—performs best." |
| Q207 | 25 | output_form | "In Tables 21 and 22 we present the average GPT-4o evaluation results for four models." |
| Q208 | 25 | output_form | "When translating into African languages, there is no clear pattern: for example, GPT-3.5, despite having the lowest fluency score, also had the fewest content, lexical, and grammatical errors, which is counterintuitive." |
| Q209 | 26 | output_content | "We were able to obtain DA scores from three annotators for all the languages." |
| Q210 | 26 | output_content | "For each language, we calculated inter-annotator agreement using Krippendorff's alpha α over 30 document instances." |
| Q211 | 26 | output_content | "We obtained α scores of 0.46, 0.57, 0.40, and 0.81, and 0.54 for Amharic, Hausa, Swahili, Yorùbá, and Zulu respectively." |
| Q212 | 26 | output_content | "These are relatively low scores, except for Yorùbá." |
| Q213 | 26 | output_form | "We present the average DA scores in Tables 10 and 14 for the health and tech domains, respectively." |
| Q214 | 26 | output_form | "The results show that annotators rate documents translated at the sentence-level as higher quality than those translated at the pseudo-document level." |
| Q215 | 26 | output_form | "Additionally, GPT-3.5 received the lowest ratings among the three models." |
| Q216 | 26 | output_form | "LLaMAX3-SFT1, a model trained on sentence-level data, was rated the best across all languages when evaluated on sentences." |
| Q217 | 26 | output_form | "However, when evaluated on pseudo-documents, its performance was rated lower than that of LLaMAX3-SFT10." |
| Q218 | 26 | output_form | "These findings are consistent with the d-chrF scores for the models, but they do not align with the evaluations from GPT-4o as a judge." |
| Q219 | 26 | output_form | "These results suggest that using GPT-4o as a translation judge is not yet well-suited for low-resource languages." |
| Q220 | 26 | output_form | "We focus on the sentence-level task and translated across all 30 directions for which the model was trained, evaluating both NLLB-200 (1.3B) and its fine-tuned version using d-chrF." |
| Q221 | 26 | output_form | "The results shows that translating into Yorùbá, which is the direction with the lowest d-chrF score from English among all the languages, benefited the most." |
| Q222 | 26 | input_form | "One major factor contributing to this is the presence of diacritics." |
| Q223 | 26 | output_form | "Furthermore, looking at their actual performances and not just the differences, our results show that translations into Swahili and English—both relatively high-resource languages—yield higher BLEU and chrF scores (see Figures 11 and 12), even after supervised finetuning." |
| Q224 | 26 | output_form | "Hence, there is much to be done to improve translation performance between low-resource language pairs." |
| Q225 | 28 | output_form | "Change (∆) in d-BLEU and d-chrF for sentence evaluation comparing NLLB1.3B before and after supervised finetuning on AFRIDOC-MT" |
| Q226 | 29 | output_form | "Table 15: Performance results of various models on the sentence-level task for the Health domain, measured using document level metric d-BLEU and d-chrF." |
| Q227 | 29 | output_form | "Table 16: Performance results of various models on the sentence-level task for the Tech domain, measured using document level metric d-BLEU and d-chrF." |
| Q228 | 30 | output_form | "Table 17: Performance results of various models on the sentence-level task for the Health domain, measured using sentence level metric s-BLEU, s-CHRF, and s-COMET." |
| Q229 | 31 | output_form | "Performance results of various models on the sentence-level task for the Tech domain, measured using sentence level metric s-BLEU, s-CHRF, and s-COMET." |
| Q230 | 32 | output_form | "Table 19: Performance results of various models on the pseudo-document-level task for the Health domain, measured using document level metric d-BLEU and d-CHRF." |
| Q231 | 32 | output_form | "Table 20: Performance results of various models on the pseudo-document-level task for the Tech domain, measured using document level metric d-BLEU and d-CHRF." |
| Q232 | 33 | output_form | "Table 21: Document-level evaluation in the health domain, judged by GPT-4o. Compares sentence- vs. document-level outputs on Fluency (1–5 scale), Content Errors (CE), Lexical (LE), and Grammatical Cohesion Errors (GE)." |
| Q233 | 33 | output_form | "Table 21: Document-level evaluation in the health domain, judged by GPT-4o." |
| Q234 | 34 | output_form | "Document-level evaluation in the tech domain, judged by GPT-4o. Compares sentence- vs. document-level outputs on Fluency (1–5 scale), Content Errors (CE), Lexical (LE), and Grammatical Cohesion Errors (GE)." |
| Q235 | 35 | input_ontology | "The task prompts used for evaluating LLMs are applied to both sentence-level and document-level translation tasks." |
| Q236 | 37 | output_form | "Figure 19: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into African languages" |
| Q237 | 37 | output_form | "Figure 20: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into African languages" |
| Q238 | 37 | output_form | "Figure 21: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into English" |
| Q239 | 37 | output_form | "Figure 22: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into English" |

---

## Regional Context

```yaml
name: Ethiopia Ministry of Health — Amharic Clinical Translation Deployment
abbreviation: ETH-MOH-AM-MT
deployment_context:
  description: An AI-powered machine translation system converting English-language
    clinical practice guidelines, vaccination schedules, and maternal-health booklets
    into Amharic for distribution by Ethiopia's Ministry of Health. Primary consumers
    are health workers and patients across Ethiopia's regional health bureaus. Evaluation
    is scoped to prose/narrative health content aligned with WHO-sourced benchmark
    documents; structured document types (tables, timetables, administrative forms)
    are out of scope.
  commissioning_body: Ethiopia Ministry of Health (MOH)
  regulatory_reference_bodies:
  - Ethiopia Ministry of Health (MOH)
  - Ethiopian Food and Drug Authority (EFDA)
  benchmark_used: AFRIDOC-MT (2024)
  data_protection_regulation: 'Personal Data Protection Proclamation No. 1321/2024
    — Ethiopia''s first comprehensive data protection law, passed April 4, 2024 and
    published in the Federal Negarit Gazette July 24, 2024. Designates the Ethiopian
    Communications Authority (ECA) as supervisory authority; requires domestic data
    storage and 72-hour breach notification. Health data qualifies as sensitive personal
    data under the law, requiring enhanced protections. MOH deployments processing
    patient-identifiable data must conduct a Data Protection Impact Assessment (DPIA).
    Source: regulations.ai — [WEB-1];
    TechHive Advisory Africa — [WEB-2]'
geography:
  country: Ethiopia
  sub_national_scope:
  - Tigray Regional Health Bureau
  - Oromia Regional Health Bureau
  - Amhara Regional Health Bureau
  - Somali Regional Health Bureau
  note: Distribution is nationwide through MOH regional bureau network. Translations
    produced centrally (likely Addis Ababa-centric) but consumed across highly diverse
    regional contexts. Whether a single national-standard Amharic register is trusted
    uniformly across all bureaus is an open question not resolved in elicitation.
languages:
  target_translation_language: Amharic
  source_language: English
  writing_system: Ethiopic (Ge'ez) script
  script_notes: Amharic uses the Ethiopic/Ge'ez syllabic script (abugida). This is
    a non-Latin, non-RTL script with distinct tokenization profiles — AFRIDOC-MT documents
    that Amharic produces the largest average token counts across evaluated tokenizers,
    requiring increased token limits for model evaluation.
  amharic_speaker_base: 'Amharic had over 33.7 million mother-tongue speakers in Ethiopia
    in 2020, with more than 25.1 million second-language speakers, totalling over
    58.8 million speakers. It is the official working language of the Ethiopian federal
    government. Source: Wikipedia/Amharic — [WEB-3]'
  amharic_dialect_variation_note: 'Published linguistic sources indicate that Amharic
    dialects are mutually intelligible, with only minor documented variations. However,
    health-register variation across regional bureaus (Tigray, Oromia, Somali) is
    a distinct concern separate from dialect difference — driven by occupational language
    norms, local terminology preferences, and the political dimension of Amharic as
    a lingua franca in non-Amhara regions. This remains a lived-practice gap not resolvable
    by web search; expert/stakeholder elicitation is required. Source: Wikipedia/Amharic
    — [WEB-3]'
  register_variation:
    acknowledged: true
    description: Amharic spoken and written registers vary across Ethiopia's regional
      health bureaus (Tigray, Oromia, Amhara, Somali). Whether Addis Ababa-centric
      clinical Amharic translations are equally trusted and comprehensible across
      all bureaus was not resolved in elicitation. Regional health-terminology preferences
      may diverge.
    resolution_status: '[NEEDS VERIFICATION — deferred: likely unsearchable (lived
      practice); requires stakeholder/expert elicitation from regional health bureau
      staff in Oromia, Tigray, and Somali regions]'
  additional_languages_in_region:
  - Afaan Oromo (Oromia)
  - Tigrinya (Tigray)
  - Somali (Somali region)
  - Afar
  - Sidamo/Sidaama
  note: The deployment targets Amharic as a lingua franca for MOH materials. Many
    health extension workers and patients in Oromia, Somali, and Tigray regions may
    have limited Amharic proficiency, but this is outside the current system scope.
target_population:
  primary_consumers:
  - MOH-trained clinical translators (ground-truth authority for quality evaluation)
  - Amharic-speaking physicians (acceptable fallback ground-truth authority)
  - Community health extension workers (Health Extension Program)
  - Semi-literate patients receiving maternal-health and vaccination materials
  occupational_roles_detail:
    clinical_translators: MOH-credentialed professionals responsible for authoritative
      Amharic rendering of clinical guidelines; designated as primary ground-truth
      judges for translation quality.
    physicians: Amharic-speaking medical doctors serving as fallback quality judges;
      presumed familiar with MOH and EFDA approved terminology.
    health_extension_workers: Community-level frontline health workers operating under
      the Health Extension Program; likely vary in Amharic literacy and clinical training
      depth.
    patients: End recipients of translated materials; may include semi-literate or
      low-literacy individuals, particularly in rural and pastoral communities.
  literacy_profile:
    national_literacy_rate: 'Approximately 51.8% adult literacy rate (ages 15+) as
      of 2017 per UNESCO/World Bank — the most recent nationally representative figure.
      A separate estimate (Knoema, citing national sources) reports 60.5% in 2022,
      but this figure should be treated with caution as it diverges from the UNESCO
      series and may reflect methodological differences. The 2017 UNESCO figure is
      the most widely cited. Source: TheGlobalEconomy.com/UNESCO — [WEB-4];
      Knoema — [WEB-5]'
    urban_rural_gap: 'Significant urban-rural gap documented: Addis Ababa has substantially
      higher literacy and enrollment rates than rural and pastoral regions. Pre-primary
      enrollment as high as 93% in Addis Ababa versus 14–18% in Afar; secondary enrollment
      in Oromia ~3% and Somali region ~4% as of 2022, reflecting severe disparities
      that are proxy indicators for lower adult literacy in regions served by the
      deployment. Gender gap also significant: male literacy ~57%, female ~41% (derived
      from Countrymeters estimates). Source: ZoeTalentSolutions/UNESCO — [WEB-6];
      Countrymeters — [WEB-7]'
    health_worker_literacy_assumption: Assumed high literacy for clinical translators
      and physicians; health extension workers and patients range from moderate to
      low literacy
    note: Semi-literate patients are explicitly named as a target consumer group,
      implying readability for lower-literacy audiences is a deployment success criterion
      alongside MOH/EFDA glossary compliance. National literacy figures are aggregates
      — actual literacy among rural patients in Somali and Afar regions may be substantially
      lower than the national figure.
ground_truth_authority:
  primary: MOH-trained clinical translators
  fallback: Amharic-speaking physicians
  excluded_as_authoritative:
  - General Amharic translators without clinical credentials
  - Academic linguists without MOH affiliation
  - Health extension workers (users, not judges)
  benchmark_annotator_alignment:
    status: UNVERIFIED — CRITICAL GAP
    description: AFRIDOC-MT names four Amharic translators (Bereket Tilahun, Hana
      M. Tamiru, Biniam Asmlash, Lidetewold Kebede) but documents no professional
      credentials, institutional affiliations, clinical backgrounds, or MOH certification.
      It is unknown whether any holds MOH clinical translation credentials or has
      been trained under Ethiopia MOH terminology standards.
    web_search_finding: '[NOT FOUND — searched for credentials of AFRIDOC-MT Amharic
      translators and MOH clinical translation certification pathways; no public documentation
      of individual translator credentials found; no formal MOH clinical translation
      certification registry identified as publicly searchable. This gap remains unresolved
      and requires direct inquiry to AFRIDOC-MT authors or MOH.]'
approved_terminology_resources:
  moh_glossary:
    name: Ethiopia Ministry of Health Amharic Medical Terminology Glossary
    status: 'Existence confirmed via indirect evidence only — no publicly accessible
      MOH-official standalone glossary document was found. The Academy of Ethiopian
      Languages has produced an ''Amharic Dictionary of Medical Terms'' (UN-sponsored,
      available on Internet Archive and Scribd) that serves as a widely referenced
      resource for medical professionals and translators in Ethiopia. A multilingual
      MOH-adjacent glossary covering English, Amharic, Oromiffa, Somali, and Afar
      terms is also documented on Scribd (over 100 medical terms). Neither has been
      confirmed as the current MOH-official compliance reference for this deployment.
      Formal MOH-designated glossary version and public URL remain unverified. Source:
      Internet Archive/Amharic Medical Dictionary — [WEB-8];
      Scribd multilingual glossary — [WEB-9]'
    role_in_deployment: Primary compliance reference; glossary conformance is a required
      success criterion for this deployment
  efda_glossary:
    name: Ethiopian Food and Drug Authority Approved Terminology List
    status: '[NOT FOUND — searched for EFDA approved Amharic medical terminology list;
      no publicly accessible EFDA standalone terminology document was found. EFDA
      (formerly FMHACA) is documented as having developed regulatory standards for
      health facilities under the Ethiopian Health Sector Transformation Plan, but
      no public URL for an EFDA-approved Amharic terminology list was surfaced. Requires
      direct inquiry to EFDA.]'
    role_in_deployment: Co-equal compliance reference alongside MOH glossary
  benchmark_glossary_integration:
    status: NOT IMPLEMENTED — AFRIDOC-MT planned a terminology harmonization step
      for translators but there is no evidence it was completed or that any approved
      Ethiopian institutional glossary was used. Benchmark scoring functions (d-BLEU,
      d-chrF, GPT-4o, human DA) are all agnostic to MOH/EFDA terminology lists.
    gap_severity: HIGH — this is the primary OO construct gap between benchmark scoring
      and deployment success criteria
document_scope:
  in_scope:
  - Prose and narrative health content
  - Clinical practice guidelines (narrative sections)
  - Maternal-health booklets (narrative sections)
  - Vaccination schedule text (narrative descriptions, not timetable grids)
  - WHO-style general health articles
  out_of_scope:
  - Structured document types (tables, dosage grids, immunization timetables)
  - Administrative forms
  - Numbered protocol lists with complex formatting
  - HMIS data entry forms
  benchmark_alignment: Good alignment — AFRIDOC-MT corpus consists entirely of narrative
    prose articles from WHO (health domain) and Techpoint Africa (tech domain), with
    no structured document types included.
  source_document_representativeness:
    note: WHO articles are the benchmark source; downstream search should verify whether
      WHO clinical language and document structures align sufficiently with actual
      Ethiopia MOH distribution materials, or whether key document genres are systematically
      absent.
    web_search_finding: '[NOT FOUND — no comparative study of WHO article language
      register vs. Ethiopia MOH distribution materials was identified; this gap requires
      expert review of actual MOH maternal-health booklets and vaccination schedule
      narrative content against the AFRIDOC-MT WHO corpus sample. A 2025 scoping review
      of NLP for public health in Africa (JMIR) identified only 3 Amharic-language
      studies out of 54 total, confirming the sparse documentation base. Source: JMIR
      2025 scoping review — [WEB-10]]'
success_criteria:
  approach: Multi-metric
  primary_criteria:
  - criterion: MOH/EFDA glossary compliance
    description: Translated terms must conform to MOH and EFDA approved Amharic medical
      terminology lists
    benchmark_operationalization: NOT OPERATIONALIZED — no benchmark scoring function
      captures this criterion
    gap_severity: HIGH
  - criterion: Document-level terminological consistency
    description: The same source term must be rendered identically throughout a translated
      document
    benchmark_operationalization: PARTIALLY — lexical cohesion errors (LE) in GPT-4o-as-judge
      protocol capture vocabulary inconsistency; human DA captures overall quality
      but not term-by-term consistency explicitly
    gap_severity: MODERATE
  - criterion: Faithfulness to source meaning
    description: Translation must not introduce incorrect clinical information, omit
      key content, or add unsupported claims
    benchmark_operationalization: COVERED — content errors (CE) dimension in GPT-4o-as-judge
      protocol captures incorrect translations, omissions, additions; human DA provides
      overall faithfulness signal
    gap_severity: LOW
  - criterion: Automatic MT metric performance
    description: BLEU, chrF, and COMET-class scores serve as proxies for translation
      quality
    benchmark_operationalization: COVERED — d-BLEU, d-chrF with bootstrap CI; chrF
      prioritized for Amharic morphological richness; AfriCOMET available for sentence-level
    gap_severity: LOW
  - criterion: Readability for semi-literate patients
    description: Translations should be comprehensible to lower-literacy end-users
    benchmark_operationalization: PARTIALLY — fluency dimension (1–5 scale) in GPT-4o-as-judge
      and human DA capture surface readability; neither is specifically calibrated
      for semi-literate populations
    gap_severity: MODERATE
infrastructure_notes:
  technology_type: AI-powered machine translation system (software deployment, not
    consumer device)
  output_modality: Text-only Amharic documents for print and digital distribution
  script_processing: Ethiopic/Ge'ez script requires correct Unicode handling; Amharic
    token counts are among the highest of all AFRIDOC-MT languages due to syllabic
    script, requiring increased model token limits
  connectivity_context_for_end_users: 'Internet penetration in Ethiopia stood at approximately
    19.4% (24.83 million users) at the start of 2024, with 80.6% of the population
    offline. 3G networks covered 98% of the population in 2023; 4G coverage was at
    33%. A significant usage gap persists: 76% of the population did not use mobile
    internet despite living within network coverage in 2024. These figures are national
    aggregates — actual connectivity in Tigray, Somali, and rural Oromia regions is
    likely substantially lower. Relevance to the deployment: the MT system operates
    centrally (MOH/Addis Ababa side) and outputs print/digital documents, so end-user
    internet access is not required for document distribution, but digital distribution
    to regional health bureaus does depend on connectivity infrastructure. Source:
    DataReportal Digital 2024 Ethiopia — [WEB-11];
    GSMA Ethiopia Report Oct 2024 — [WEB-12];
    World Bank 2025 — [WEB-13]'
  health_system_infrastructure:
    health_extension_program: 'The Health Extension Program (HEP), launched in 2003,
      deploys more than 40,000 Health Extension Workers (HEWs) across more than 17,000
      health posts nationwide. Two HEWs are assigned per kebele (lowest administrative
      unit, ~5,000 people). As of June 2023, the MOH formally adopted a blended (digital
      + in-person) learning approach for all HEW training, targeting all 40,000 workers.
      The program covers disease prevention, family health services, hygiene, and
      health education. Source: PMC/Ethiopian Journal of Health Sciences 2023 — [WEB-14];
      Last Mile Health 2024 — [WEB-15]'
    regional_bureau_distribution_mechanism: '[NEEDS VERIFICATION — deferred: below
      search budget; distribution logistics from MOH to regional bureaus and down
      to health posts are documented in general terms (Regional Health Bureaus coordinate
      distribution; health centers and health posts are the terminal nodes) but the
      specific mechanism for translated document distribution (print vs. digital,
      frequency, supply chain) is a lived-practice/administrative detail not resolvable
      by web search. Source for structural description: ethiopiahealth.blogs.wm.edu
      — [WEB-16]]'
ethiopia_specific_clinical_context:
  endemic_diseases_of_concern:
    note: While user accepted generic coverage as sufficient for current evaluation,
      real deployment serves a context with Ethiopia-specific endemic conditions.
      Benchmark does not cover these.
    diseases:
    - Malaria (Plasmodium falciparum and vivax, regionally variable)
    - Tuberculosis (high burden country)
    - Kala-azar / visceral leishmaniasis (especially Tigray, Amhara lowlands)
    - Trachoma (leading cause of preventable blindness, endemic in several regions)
    - Neglected tropical diseases
    - Undernutrition / acute malnutrition
    terminology_gap: '[NOT FOUND — searched for Amharic MT evaluation studies specifically
      covering kala-azar, trachoma, or visceral leishmaniasis terminology; no such
      evaluation was found. The 2025 JMIR scoping review of NLP for public health
      in Africa identified only 3 Amharic-language NLP studies out of 54 and none
      specifically addressing endemic disease terminology evaluation. This null result
      itself confirms the gap: no evidence exists that existing Amharic MT benchmarks
      have been tested on Ethiopia-endemic disease terminology. Source: JMIR 2025
      scoping review — [WEB-10]]'
  ethiopian_calendar:
    note: The Ethiopian calendar (Ge'ez calendar) is 7–8 years behind the Gregorian
      calendar and uses 13 months. Clinical documents referencing dates may require
      calendar conversion.
    benchmark_coverage: NOT COVERED — user accepted generic handling as sufficient;
      AFRIDOC-MT WHO source documents use Gregorian dates
    web_search_finding: '[NOT FOUND — no NLP studies specifically evaluating Amharic
      MT failure modes on Ethiopian calendar date expressions were found. This remains
      an uninvestigated gap.]'
  referral_pathways:
    note: Ethiopia's tiered health system (health post → health center → primary hospital
      → referral hospital) involves institution-specific referral language not present
      in WHO-sourced benchmark documents.
    benchmark_coverage: NOT COVERED
    status: Accepted as out-of-scope for current evaluation by user
cultural_norms_notes: '- Amharic is the federal working language of Ethiopia but is
  a native language primarily of the Amhara ethnic group; its use as a clinical lingua
  franca across Oromia, Tigray, and Somali regions has political and social dimensions.

  - Clinical communication norms in Ethiopia may differ from WHO document register;
  health extension workers often use simplified explanatory language with patients.

  - Religious diversity (Ethiopian Orthodox Christianity, Islam, Protestant Christianity,
  traditional beliefs) affects receptiveness to certain health messaging (e.g., family
  planning, vaccination).

  - Community and family decision-making structures influence patient behavior; materials
  may need to address household-level not just individual-level decisions.

  - Age and gender hierarchies affect how health messages are received and acted upon,
  particularly in maternal health contexts.'
benchmark_validity_gaps_summary:
  annotator_credentials:
    priority: HIGH
    description: AFRIDOC-MT Amharic translators are named professionals without documented
      MOH credentials; deployment requires MOH-trained clinical translators as ground-truth
      authority.
    web_search_finding: '[NOT FOUND — no public documentation of AFRIDOC-MT Amharic
      translator credentials or formal MOH clinical translation certification registry
      was identified. Gap remains open; requires direct inquiry to AFRIDOC-MT authors
      (contact: Israel Abebe Azime, Masakhane NLP/Saarland University) or Ethiopia
      MOH.]'
  glossary_compliance_scoring:
    priority: HIGH
    description: No benchmark scoring function operationalizes MOH/EFDA glossary conformance,
      which is the primary deployment success criterion.
    web_search_finding: 'Partially investigated. The Academy of Ethiopian Languages
      has published an Amharic Dictionary of Medical Terms (UN-sponsored), and a multilingual
      English-Amharic-Oromiffa-Somali-Afar health glossary exists on Scribd. No evidence
      was found that any of these resources has been integrated into any MT evaluation
      protocol for Amharic. The AFRIDOC-MT planned terminology harmonization step
      was not completed. Scores remain agnostic to institutional glossary compliance.
      Source: Internet Archive — [WEB-8]'
  regional_register_variation:
    priority: HIGH
    description: Whether a single Addis Ababa-centric reference translation is valid
      across Tigray, Oromia, Amhara, and Somali regional bureaus is unresolved.
    web_search_finding: '[NOT FOUND — searched for documented Amharic health-register
      or dialect variation across Ethiopia''s regional bureaus; no published NLP study
      or health communication study addressing this specific sub-national variation
      was found. Wikipedia confirms Amharic dialects are mutually intelligible, but
      health-register variation is a distinct and uninvestigated question. Requires
      stakeholder elicitation from regional bureau staff. Source: Wikipedia/Amharic
      — [WEB-3]]'
  ethiopia_specific_clinical_content:
    priority: MODERATE
    description: WHO-sourced benchmark documents do not include Ethiopia-endemic disease
      terminology, regional referral pathways, or Ethiopian calendar expressions.
    web_search_finding: 'Confirmed gap. A 2025 JMIR scoping review of NLP for public
      health in Africa (54 studies, data through October 2024) found only 3 Amharic-language
      studies — none specifically evaluating Ethiopia-endemic disease terminology
      or MOH document genres. This sparse landscape confirms that no Amharic NLP benchmark
      has been validated against Ethiopia MOH material registers. Source: JMIR 2025
      scoping review — [WEB-10]'
  gpt4o_judge_reliability_for_amharic:
    priority: MODERATE
    description: AFRIDOC-MT itself documents GPT-4o-as-judge inconsistency for African
      languages including Amharic; deployment cannot rely on this as a scalable quality
      proxy.
    web_search_finding: 'Corroborated by independent 2024 Walia-LLM study (Azime et
      al., EMNLP Findings 2024), which found GPT-4 scores are ''not reproducible in
      every run'' for Amharic tasks and that GPT-4 ''lacks the ability to evaluate
      most generation tasks'' in Amharic. The study recommends GPT-4 coupled with
      human evaluation as the best available approach. This independently confirms
      AFRIDOC-MT''s own finding that GPT-4o-as-judge is unreliable for Amharic. Source:
      Walia-LLM, ACL Anthology — [WEB-17];
      arXiv 2402.08015 — [WEB-18]'
  document_level_embedding_metrics_for_amharic:
    priority: MODERATE
    description: No document-level embedding-based metric is validated for Amharic
      at document level. AfriCOMET is excluded from document-level evaluation due
      to its 512-token limit, and the long-context QE model (ModernBERT-based) excludes
      Amharic.
    web_search_finding: '[NOT FOUND — no 2024–2025 publication was found introducing
      a document-level neural quality estimation metric validated for Amharic. The
      Walia-LLM paper (EMNLP 2024) evaluates Amharic MT with chrF++ at sentence level
      but does not introduce a document-level metric. The gap documented in AFRIDOC-MT
      remains open as of early 2025. Source: Walia-LLM arXiv — [WEB-18]]'
inter_annotator_agreement_note: 'Krippendorff''s alpha for Amharic human direct assessment
  in AFRIDOC-MT is 0.46 — relatively low, meaning even the benchmark''s own human
  evaluation signal for Amharic is noisy. This compounds the annotator-credentials
  gap: even if benchmark annotators were acceptable proxies for MOH-credentialed translators,
  the low agreement suggests substantial annotation uncertainty in the Amharic reference
  quality signal.'
net_new_fields:
  amharic_nlp_ecosystem_note: 'As of 2024, Amharic has more task-specific NLP datasets
    than other Ethiopian languages, but remains a low-resource language with orders
    of magnitude less data than English. Recent work includes Walia-LLM (EMNLP Findings
    2024), an Amharic-fine-tuned LLaMA-2 model, and Amharic LLaMA/LLaVA (arXiv 2024).
    The 2025 Springer survey of Amharic NLP (2015–2024) identifies morphological richness,
    data scarcity, and annotation inconsistency as persistent challenges. None of
    these models or benchmarks are specifically calibrated for clinical translation
    or MOH terminology compliance. Source: Walia-LLM ACL Anthology — [WEB-17];
    Springer Amharic NLP survey 2025 — [WEB-19]'
  african_nlp_public_health_coverage: 'A 2025 JMIR scoping review of NLP for public
    health in Africa (54 studies, Jan 2013–Oct 2024) found Amharic represented in
    only 3 studies — ranking behind English (40), Arabic (8), Kiswahili (7), French
    (4), and Zulu (4). Ethiopia appeared only in the ''fewer than 2 papers'' group
    by author country affiliation. This confirms the extremely sparse NLP-for-public-health
    evidence base for Amharic, meaning the deployment operates in a near-zero-validated
    context for health NLP. Source: JMIR 2025 / PMC — [WEB-10]'
  ethiopia_digital_health_investment_context: 'A 2024 World Bank report notes that
    MOH spending required to enhance digital health in Ethiopia is estimated at USD
    349.7 million, and the Data Protection Proclamation (2024) and Digital ID Proclamation
    (2023) form part of a broader digital governance framework. The MOH has formally
    adopted blended digital learning for HEW training as of June 2023. These investments
    are relevant context for the deployment: the MOH is actively building digital
    health infrastructure, but the primary end-users (HEWs and patients at health
    posts) operate largely in offline or low-connectivity environments. Source: GSMA
    Ethiopia Report Oct 2024 — [WEB-12];
    World Bank 2025 — [WEB-13]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://regulations.ai/regulations/RAI-ET-NA-PDPPNXX-2024 |
| WEB-2 | https://www.techhiveadvisory.africa/insights/review-of-ethiopias-data-protection-act |
| WEB-3 | https://en.wikipedia.org/wiki/Amharic |
| WEB-4 | https://www.theglobaleconomy.com/Ethiopia/Literacy_rate/ |
| WEB-5 | https://knoema.com/atlas/Ethiopia/topics/Education/Literacy/Adult-literacy-rate |
| WEB-6 | https://zoetalentsolutions.com/education-statistics-for-ethiopia/ |
| WEB-7 | https://countrymeters.info/en/Ethiopia |
| WEB-8 | https://archive.org/details/amharic-dictionary-of-medical-terms-108p-copy |
| WEB-9 | https://www.scribd.com/document/416080918/English-Amharic-Oromiffa-Somali-Afar |
| WEB-10 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11923465/ |
| WEB-11 | https://datareportal.com/reports/digital-2024-ethiopia |
| WEB-12 | https://www.gsma.com/about-us/regions/sub-saharan-africa/wp-content/uploads/2024/10/GSMA_Ethiopia-Report_Oct-2024_v2-1.pdf |
| WEB-13 | https://www.worldbank.org/en/results/2025/06/30/empowering-ethiopians-by-laying-the-digital-foundations-for-afe-economic-growth |
| WEB-14 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10866294/ |
| WEB-15 | https://lastmilehealth.org/2024/05/01/last-mile-health-launches-ethiopias-first-non-communicable-disease-training-for-community-health-workers/ |
| WEB-16 | https://ethiopiahealth.blogs.wm.edu/ethiopian-health-system/ |
| WEB-17 | https://aclanthology.org/2024.findings-emnlp.25/ |
| WEB-18 | https://arxiv.org/abs/2402.08015 |
| WEB-19 | https://link.springer.com/article/10.1007/s44248-025-00077-9 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark covers health documents, but clinical practice guidelines, vaccination schedules, and maternal-health booklets have specific structural features — numbered protocols, dosage tables, immunization timetables, warning boxes, and administrative forms. Does your deployment need to handle these structured document types, or is it primarily narrative/prose health content? Are there other document formats common in Ethiopian ministry-of-health materials that you'd consider critical to cover?
A1: The deployment can reasonably be scoped to prose/narrative health content since the benchmark draws from WHO articles; highly structured document types (tables, timetables, administrative forms) are considered out of scope for this evaluation. The user accepts that focus on general health prose is appropriate.

Q2 [IC]: Ethiopian clinical and maternal-health documents often reference locally specific content: Ethiopian calendar dates, endemic diseases prevalent in Ethiopia by region, local nutrition guidance, or Ethiopia-specific referral pathways. Would your source documents contain this kind of Ethiopia-specific clinical content, and would a system trained on more generic health text be expected to handle it correctly?
A2: The benchmark's WHO-sourced documents are unlikely to contain Ethiopia-specific clinical content. The user accepts that generic health-text training should suffice for general translation tasks (including date conversion), and believes models trained on general health corpora can handle endemic-disease terminology translation adequately.

Q3 [OC]: Whose judgment should be authoritative for ground-truth translation quality — MOH-trained clinical translators, Amharic-speaking physicians, health extension workers, or patients? Do regional Amharic registers and health terminology vary enough across bureaus that a single Addis Ababa-based translator's choices would not be trusted equally across Tigray, Oromia, or Somali regions?
A3: MOH-trained clinical translators are the preferred ground-truth authority; Amharic-speaking physicians are an acceptable fallback. Regional register variation across bureaus is implicitly acknowledged but not deeply explored — no clear resolution was offered for whether Addis Ababa-centric translations would be uniformly accepted across all regional bureaus.

Q4 [OO]: Which success criteria govern translation quality — faithfulness to source meaning, terminological consistency across a full document, readability for semi-literate patients, or compliance with MOH-approved glossaries?
A4: The team prioritizes a multi-metric approach combining automatic MT metrics, faithfulness to source meaning, terminological consistency across the document, and compliance with MOH and EFDA approved glossaries. Both MOH and EFDA glossaries exist and are available as reference resources.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | The benchmark was ground-up designed for African languages including Amharic, and the user has scoped deployment to prose health content that aligns with the WHO-sourced benchmark corpus; structured document types are out of scope, reducing the category-coverage gap. |
| IC | HIGH | The benchmark lacks Ethiopia-specific clinical content (local disease patterns, referral pathways, calendar systems), and while the user accepts generic coverage for now, this gap introduces construct-irrelevant variance for a deployment serving real MOH distribution in a highly contextual health environment. |
| IF | LOWER | Both benchmark and deployment are text-only in Amharic, a language the benchmark explicitly includes; no modality or script mismatch is present. |
| OO | HIGH | The deployment requires compliance with MOH/EFDA-approved glossaries and document-level terminological consistency as primary scoring criteria, but the benchmark's scoring functions may not operationalize these institutional standards, creating a mismatch in what "correct translation" means. |
| OC | HIGH | Ground-truth labels in the benchmark may not have been produced by MOH-trained clinical translators or Amharic-speaking physicians; the user explicitly named these as the authoritative population, and annotator-population mismatch in a sensitive health domain poses direct risk to label validity. |
| OF | LOWER | Both the benchmark and deployment use text output; the MCQ-vs-open-ended distinction does not apply here, and the document-level translation format of the benchmark matches the deployment's document translation need. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** masakhane/AfriDocMT
**Analysis date:** 2025-07-12
**Examples reviewed:** 51 total (5 from doc_health train, 5 from doc_health_10 train, 5 from doc_health_25 train, 5 from doc_health_5 train, 5 from doc_tech train, 5 from doc_tech_10 train, 5 from doc_tech_25 train, 5 from doc_tech_5 train, 5 from health train, 6 from tech train, 5 from doc_tech train)
**Columns shown:** am, en, ha, sw, yo, zu
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | doc_health, train | Ex. 1 | health | "የሞቃታማ ዐውሎ ነፋሶች ... ለሞቃታማ አውሎ ነፋሶች፣ እንዲሁም ሀይለኛ አውሎ ነፋስ ወይም አውሎ ነፋሶች ... ኃይለኛ ክብ አውሎ ነፋሶች ... 233 000 ሰዎችን ገድለዋል" | Full Amharic document on tropical cyclones (WHO article), multi-sentence, Ethiopic script, with clinical/epidemiological content and specific numbers | IF, IC |
| D2 | doc_health, train | Ex. 1 | health | "When tropical cyclones cause floods and sea surges, the risk of drowning and water- or vector-borne diseases increase." | WHO English source on tropical cyclones — generic global health content, no Ethiopia-specific epidemiological context | IC |
| D3 | doc_health, train | Ex. 2 | health | "አካል ጉዳተኝነት ሰው የመሆን አካል ነው፡፡ ሁሉም ሰው ማለት ይቻላል በሕይወታቸው ላይ በሆነ ወቅት ጊዚያዊ ወይም ዘላቂ የአካል ጉዳት ያጋጥማቸዋል" | Amharic WHO article on disability — prose narrative, full document preserved | IC, IF |
| D4 | doc_health, train | Ex. 3 | health | "ተጨማሪ ምግብ ማጠቃሊያ፡- በ 6 ወር አካባቢ የሕፃኑ የኃይል ፍላጎት ... ጨቅላ ህፃናት ... ጡት ማጥባት" | Amharic complementary feeding article — maternal-child health topic directly relevant to deployment (maternal-health booklets) | IC, OC |
| D5 | doc_health, train | Ex. 4 | health | "ፀረ-ተሕዋስያንን መቋቋም(AMR) ... ባክቴሪያ፣ ጥገኛ ተውሳኮች፣ ቫይረሶችና በፈንገሶች ምክንያት" | Amharic AMR article — specialized medical terminology in Ethiopic script | OC, IF |
| D6 | doc_health, train | Ex. 5 | health | "ክራይሚያ-ኮንጎ የደም መፍሰስ ትኵሳት ... CCHF ወረርሽኞች ... ከ10-40% ሞት ... ሞቃታማ አውሎ ነፋስ" | Amharic article on CCHF hemorrhagic fever — clinical terminology, disease outside typical Ethiopian endemic profile | IC |
| D7 | doc_health_10, train | Ex. 1 | health | "ነገር ግን፣ በ2023 እስከ ዛሬ 46 ደብሊዉፒቪ1 አዎንታዊ የአካባቢ ናሙናዎች ... ናንጋርሃር እና ኩናር አውራጃዎች ... ሚሊዮን ተመላሾች" | Amharic WHO article on Afghanistan polio — geographic specificity to Afghanistan/Pakistan, not Ethiopia; pseudo-document chunk (10 sentences) | IC, IO |
| D8 | doc_health_10, train | Ex. 2 | health | "የጤና አጠባበቅ አቅራቢዎች ከአካባቢያዊ አስጊ ሁኔታዎች ጋር የተዛመዱ የህጻናት በሽታዎችን ... ከሁለቱም ያደጉ እና በማደግ ላይ ያሉ ሀገራት" | Short Amharic sentence fragment — environment/child health with global framing | IC |
| D9 | doc_health_25, train | Ex. 2 | health | "ዓለም አቀፍ ትብብር የጋራ ዓላማን ለማሳካት ... ዜሮ ዶዝ ... ህፃናት ፈልጎ ማግኘት ... ዶ/ር ጆርጅ ምዊንያ" | Amharic WHO Assembly article about immunization — broad vaccination language relevant to vaccination schedule booklets | IC |
| D10 | doc_health_5, train | Ex. 4 | health | "Malnutrition in the early years of life can have long-lasting impacts on physical and mental development... WHO recommends breastfeeding babies exclusively for 6 months" | English WHO source on malnutrition — maternal-child health content aligned with deployment domain | IC |
| D11 | health, train | Ex. 4 | health (sentence) | "Measures for the prevention of cholera mostly consist of providing clean water and proper sanitation to populations who do not yet have access to basic services, as well as vaccination with Oral Cholera Vaccines." | Sentence-level WHO cholera prevention content — cholera is endemic in Ethiopia but article is generic global | IC, IO |
| D12 | health, train | Ex. 1 | health (sentence) | "OCV ni zana ambayo hutumiwa pamoja na hatua za kudhibiti kipindupindu." (sw) / "OCV jẹ́ ohun èlò fún àfikún àwọn ìlànà fún ṣíṣe àmójútó àrùn onígbá méjì" (yo) | Sentence-level multi-language row — all six languages present including Amharic | IF |
| D13 | doc_tech, train | Ex. 1 | tech | "ፔይ ዴይ ለሽያጭ ? ዛሬ በ ቴክ ፖይንት አፍሪካ ... የናይጄሪያ ፕረዚዳንት ... ፔይ ደይ ... ኦባሲ ኢነ-ኦቦንግ" | Amharic Techpoint Africa tech-news article about Nigerian fintech/genomics — not relevant to Ethiopian MOH deployment | IC, IO |
| D14 | doc_tech, train | Ex. 2 | tech | "ደቡብ አፍሪካ ጎጂ ይዘቶችን በመስመር ላይ ማቆም ትፈልጋለች ... YouTube ... NALA ... Cellulant ... ሴሉላንት 20%" | Long Amharic tech article: South Africa content regulation, YouTube, NALA remittances, Cellulant layoffs — entirely irrelevant to Ethiopian clinical translation | IO, IC |
| D15 | doc_health, train | Ex. 3 | health | "ደህንነቱ የተጠበቀ፡- በንጽህና ተከማችተው እና ተዘጋጅተዋል እንዲሁም ጠርሙሶች እና ፕላስቲኮችን ሳይሆን በንጹህ እቃዎች ... ጡት ማጥባት" | Complementary feeding clinical guidance in Amharic — high relevance (maternal health booklet content) | IC, OC |
| D16 | doc_health, train | Ex. 1 | health | "Tropical cyclones, also known as typhoons or hurricanes, are among the most destructive weather phenomena." | WHO article on tropical cyclones — generic global health emergency content | IC |
| D17 | doc_health_25, train | Ex. 4 | health | "ጡት ማጥባት የማስተዋል አቅም መጨመር፣ የትምህርት ቤት አፈፃፀም ... ጡት ማጥባት ትቁ ብሎ ይመክራሉ" | Amharic infant nutrition article — direct overlap with maternal-health booklet deployment | IC |
| D18 | doc_health, train | Ex. 2 | health | "Disability results from the interaction between individuals with a health condition, such as cerebral palsy, Down syndrome and depression, with personal and environmental factors" | WHO disability article — relevant to health sector but not to primary clinical guideline/maternal-health booklet domain | IC |
| D19 | doc_health_25, train | Ex. 3 | health | "COVID-19 ... Interim position paper: considerations regarding proof of COVID-19 vaccination for international travellers" | COVID-19 international travel advisory — time-limited, globally generic, not Ethiopia-specific | IC |
| D20 | doc_health_25, train | Ex. 5 | health | "ዓለም አቀፍ የጤና ደንቦች ... IHR 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ" | International Health Regulations article — relevant to health systems globally, but highly technical/regulatory, not maternal-clinical prose | IC |
| D21 | doc_health, train | Ex. 4 | health | "Antimicrobial resistance ... AMR threatens the effective prevention and treatment of an ever-increasing range of infections caused by bacteria, parasites, viruses and fungi." | AMR — critical global health topic relevant to clinical settings, within WHO source domain | IC |
| D22 | doc_tech_25, train | Ex. 1 | tech | "Fatanmi identifies is its effect on marketing a business ... Gen Zs ... Building in public..." | Tech article about startup marketing strategy — entirely irrelevant to Ethiopian MOH clinical translation deployment | IO |
| D23 | health, train | Ex. 2 | health (sentence) | "However, what is clear is that health systems need to predominantly rely on public revenue sources: mandatory, pre-paid and pooled" | Health financing sentence — health systems policy, not clinical guideline content | IC |
| D24 | health, train | Ex. 3 | health (sentence) | "Similarly, the development and promotion of WHO international reference standards helps ensure that biological therapeutics are standardized between different manufacturers, countries, and laboratories." | Biological therapeutics standardization — very specialized regulatory content | IC |
| D25 | doc_health_10, train | Ex. 3 | health | "ጤና ስርዓቱ መጠነ ሰፊ ለውጥ ... የቅድመ ክፍያ ፈንድ ... ዘላቂ ልማት ግቦች" | Health financing/health accounts article — health systems economics, not clinical or maternal-health prose | IC |
| D26 | doc_health_10, train | Ex. 4 | health | "ዚካ ቫይረስ ... ፀረ-ተባይ ... Vector control operations framework for Zika virus" | Short Zika virus sentence fragment — topic not endemic to Ethiopia | IC |
| D27 | doc_health_10, train | Ex. 5 | health | "የጤና አካውንት ሥርዓት ... የጤና ወጪን ... SHA 2011" | Health accounts system article — health financing methodology, not clinical guideline content | IC |
| D28 | doc_health_5, train | Ex. 1 | health | "የ ቲአርአይፒኤስ ስምምነት ... TRIPS ... ዓለም ንግድ ድርጅት ... WTO ... WIPO" | TRIPS/intellectual property & medicines article — health policy, not clinical guideline | IC |
| D29 | doc_health_5, train | Ex. 3 | health | "ግብር እና ድጎማ ... ማህበራዊ ሚዲያ ይዘቶቻቸውን ለፖሊሲ ምርጫ" | Health system governance/taxes sentence fragment — health policy tools | IC |
| D30 | doc_health, train | Ex. 3 | health | "Ensuring that infants nutritional needs are met requires that complementary foods be: timely ... adequate ... safe ... properly fed" | WHO complementary feeding — directly matches maternal-health booklet deployment content | IC, OC |
| D31 | doc_health_25, train | Ex. 4 | health | "ጡት ማጥባት … ሞተዋል .... 820,000 ... 40% ..." | Amharic infant nutrition WHO article — directly relevant to maternal-health booklet | OC |
| D32 | doc_health, train | Ex. 5 | health | "Crimean-Congo haemorrhagic fever (CCHF) is a viral haemorrhagic fever usually transmitted by ticks ... CCHF is endemic in all of Africa, the Balkans, the Middle East and in Asia." | CCHF article — hemorrhagic fever not a primary health priority in Ethiopia; tick-borne virus | IC |
| D33 | doc_health_25, train | Ex. 3 | health | "A volcano is a vent in the Earth's crust from which eruptions occur... There are about 1500 potentially active volcanoes worldwide." | Volcanic eruption WHO article — not relevant to Ethiopian clinical translation deployment | IC, IO |
| D34 | doc_health_10, train | Ex. 1 | health | "Afghanistan continues to implement an intense campaign schedule, focusing on improving quality in the endemic zone... massive population movement significantly increases the risk of cross-border poliovirus spread" | WHO Afghanistan polio article — geographically specific to Afghanistan, not Ethiopia | IC |
| D35 | doc_health_5, train | Ex. 2 | health | "ይህ ለሕዝብ ጤና ድንገተኛ አደጋዎች እና ለ አይኤችአር ትግበራ ... WGIHR6 ... PHEIC" | International health regulations/WGIHR process article — technical governance content | IC |
| D36 | doc_health_25, train | Ex. 2 | health | "The WHA evaluated the unique epidemiological opportunity which exists over the next six months to eradicate the remaining chains of endemic wild poliovirus transmission." | WHO Assembly polio article — immunization content indirectly relevant (vaccination schedules), but Afghanistan/global framing not Ethiopia-specific | IC |
| D37 | doc_health_5, train | Ex. 5 | health | "WHO works with Member States to ensure key populations have adequate knowledge about appropriate foods and feeding practices" | WHO complementary feeding counselling — maternal-child health, highly relevant | IC, OC |
| D38 | doc_tech_10, train | Ex. 1 | tech | "የሕንድ ኢድቴክ ኢንዱስትሪ ... ሕንድ ከዩናይትድ ስቴትስ (ዩ ኤስ) ቀጥሎ ... edtech ... Central Square Foundation ... Nigerian Edtech ecosystem" | Indian/Nigerian edtech article — entirely irrelevant to Ethiopian clinical translation | IO |
| D39 | doc_tech_25, train | Ex. 2 | tech | "Nigerian healthtech startup, Clafiya, raises $610,000 in pre-seed funding" | African healthtech/fintech startup news — entirely irrelevant to Ethiopian MOH clinical translation deployment | IO |
| D40 | health, train | Ex. 5 | health (sentence) | "Safe, effective and quality-assured blood products contribute to improving and saving millions of lives every year" | Blood products sentence — health domain but not maternal/clinical guideline focus | IC |
| D41 | doc_health, train | Ex. 1 | health | "WHO helps to restore primary care services so that facilities can deliver essential services, including immunization, basic treatment for common illnesses, acute malnutrition and maternal care" | WHO cyclone response includes immunization + maternal care — partially relevant content | IC, OC |
| D42 | doc_health_25, train | Ex. 4 | health | "የዓለም ጤና ድርጅት ሕፃናትን ለ6 ወራት ብቻ እንዲያጠቡ ይመክራል ... ደህንነቱ የተጠበቀ እና ተጨማሪ ምግብ" | Amharic WHO recommendation on exclusive breastfeeding — direct match for maternal-health booklet content | IC, OC |
| D43 | doc_health, train | Ex. 4 | health | "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ፣ ፀረ-ፈንገስ ... 'ሱፐርበግስ(superbugs)'" | AMR article with English loanword "superbugs" retained in Amharic — illustrates translationese patterns | IC, OC |
| D44 | doc_health, train | Ex. 3 | health | "ጨቅላ ህፃናት ከ6 ወር ጀምሮ የተጣራ፣ የተፈጨ እና ከፊል ጠጣር ምግቦችን መመገብ ይችላሉ" | Amharic instruction for pureed/mashed foods from 6 months — clinically precise maternal-health instruction | OC |
| D45 | doc_health_10, train | Ex. 2 | health | "To allow healthcare providers to better identify and prevent childhood diseases related to environmental risk factors, experts from both developed and developing countries" | Short environmental health sentence — health domain but generic | IC |
| D46 | doc_health_5, train | Ex. 1 | health | "TRIPS Agreement, many resolutions of the World Health Assemblies have requested WHO to address the impact of trade agreements and intellectual property protection on public health and access to medicines" | TRIPS/IP health policy — highly technical policy content | IC |
| D47 | doc_health, train | Ex. 5 | health | "CCHF ወረርሽኞች ቫይረሱ ወደ ወረርሽኞች ሊያመራ ስለሚችል ከፍተኛ የሞት መጠን (ከ10-40%)... ህክምና፡- የክራይሚያ-ኮንጎ ... ፀረ-ቫይረስ መድሃኒት ... ribavirin" | CCHF treatment article in Amharic including "ribavirin" (transliterated drug name) — medical terminology rendering pattern visible | OC |
| D48 | doc_health_25, train | Ex. 4 | health | "ዓለም አቀፍ የጤና ሽፋን ... ዘላቂ የልማት ግቦች ... SDG ... ዘርፈ ብዙ የህዝብ ጤና" | Disability/UHC policy article — health governance framing, not clinical maternal health | IC |
| D49 | doc_health_25, train | Ex. 1 | health | "Continue to support research to improve vaccines that reduce transmission and have broad applicability; to understand the full spectrum, incidence and impact of post COVID-19 condition" | COVID-19 research policy article — time-limited global policy content | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Authentic Amharic Ethiopic-script health translations present throughout
- **Dimension(s):** IF, IC
- **Observation:** All health examples contain Amharic (`am`) column text in Ethiopic/Ge'ez script. The data consistently includes full-document Amharic prose across health topics, with complex multi-sentence Amharic translations demonstrating that the benchmark actually contains the script and language variant required. The documents are narrative prose, matching the user's accepted scope.
- **Deployment relevance:** This directly confirms that the benchmark evaluates the target script and language combination (Amharic, Ethiopic script) for the deployment. The text in [D1] shows a full multi-paragraph Amharic WHO article of the type that would appear in MOH distribution materials, and [D4] and [D5] demonstrate medical terminology rendering in Ethiopic script.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "የሞቃታማ ዐውሎ ነፋሶች ... ኃይለኛ ክብ አውሎ ነፋሶች ... 233 000 ሰዎችን ገድለዋል" — Full-length Amharic health document in Ethiopic script with numbers, medical terms, and multi-paragraph structure.
  - [D5] Example 4 (doc_health, split=train): "ፀረ-ተሕዋስያንን መቋቋም(AMR) ... ባክቴሪያ፣ ጥገኛ ተውሳኮች፣ ቫይረሶችና" — Medical terminology for AMR rendered in Ethiopic script with parenthetical English acronym, showing how clinical terms are handled.
  - [D47] Example 5 (doc_health, split=train): "ህክምና፡- የክራይሚያ-ኮንጎ ... ፀረ-ቫይረስ መድሃኒት ... ribavirin" — Drug name "ribavirin" transliterated alongside Amharic clinical treatment text.

#### Strength 2: Multi-parallel structure enables comparison across all six languages simultaneously
- **Dimension(s):** IF, OO
- **Observation:** Every data row contains parallel translations in all six languages (am, en, ha, sw, yo, zu) from the same source document. This enables evaluation of Amharic translation quality directly against the English source, while also permitting cross-linguistic comparison.
- **Deployment relevance:** The deployment is English→Amharic. The benchmark directly supports this evaluation direction. The parallel structure means one can assess whether a model correctly translates a sentence such as [D2] into Amharic [D1] within the same row.
- **Datapoint citations:**
  - [D12] Example 1 (health, split=train, sentence-level): "OCV wata hanya ce da ake amfani da ita a ƙari a kan hanyar kula da kwalara" (ha) — Each row contains all six translations of the same sentence, enabling direct comparison.

#### Strength 3: Maternal and child health content directly matching deployment domain
- **Dimension(s):** IC, OC
- **Observation:** Several WHO articles in the health corpus directly cover topics central to the MOH deployment scope: complementary feeding (Example 3, doc_health train), infant nutrition including breastfeeding recommendations (doc_health_25, Example 4), and similar maternal-child health topics. These represent the closest thematic match to the stated deployment use case of maternal-health booklets and vaccination schedules.
- **Deployment relevance:** The deployment specifically names maternal-health booklets as a primary document type. The complementary feeding, breastfeeding, and infant nutrition articles are substantively equivalent to maternal-health booklet content, making these the highest-value examples in the corpus for validity assessment.
- **Datapoint citations:**
  - [D4] Example 3 (doc_health, split=train): "ተጨማሪ ምግብ ማጠቃሊያ፡- በ 6 ወር አካባቢ የሕፃኑ የኃይል ፍላጎት ... ጨቅላ ህፃናት" — Full Amharic complementary feeding article directly matching maternal-health booklet content.
  - [D15] Example 3 (doc_health, split=train): "Ensuring that infants nutritional needs are met requires that complementary foods be: timely ... adequate ... safe" — English source for complementary feeding guidelines.
  - [D42] Example 4 (doc_health_25, split=train): "የዓለም ጤና ድርጅት ሕፃናትን ለ6 ወራት ብቻ እንዲያጠቡ ይመክራል ... ደህንነቱ የተጠበቀ እና ተጨማሪ ምግብ" — Amharic WHO breastfeeding recommendation — directly applicable to maternal-health booklet context.
  - [D37] Example 5 (doc_health_5, split=train): "WHO works with Member States to ensure key populations have adequate knowledge about appropriate foods and feeding practices" — maternal-child health domain.

#### Strength 4: Document-level structure preserved, enabling assessment of paragraph-level cohesion
- **Dimension(s):** IF, OO
- **Observation:** The `doc_health` config contains full documents (Example 1 is a complete WHO tropical cyclones article; Example 2 is a full disability article), not isolated sentences. The chunked configs (`doc_health_10`, `doc_health_5`, etc.) preserve multi-sentence pseudo-documents. This means the benchmark can test context-dependent translation phenomena such as pronoun resolution and terminological consistency across paragraphs.
- **Deployment relevance:** Clinical practice guidelines and maternal-health booklets are multi-page documents. The benchmark's document-level structure directly supports evaluation of translation fidelity across longer clinical text units, which is critical for the deployment.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): The Amharic tropical cyclones article contains multiple paragraphs with consistent use of "ዐውሎ ነፋሶች" (tropical cyclones) across sections, demonstrating intra-document terminological consistency.
  - [D3] Example 2 (doc_health, split=train): "አካል ጉዳተኝነት ሰው የመሆን አካል ነው፡፡ ሁሉም ሰው ..." — Full WHO disability article across many paragraphs.

#### Strength 5: WHO-sourced health prose directly equivalent to Ethiopian MOH distribution materials
- **Dimension(s):** IC
- **Observation:** The health corpus is entirely sourced from WHO public health articles. The register, topic range, and structural patterns (overview → impact → WHO response) match the type of narrative prose typical of WHO-aligned MOH health communication materials. Topics such as cholera prevention (D11), AMR (D21), immunization (D36, D9), and maternal-child health (D4, D42) all fall within the scope of clinical guideline and health booklet content distributed by Ministries of Health.
- **Deployment relevance:** The user accepted generic WHO-sourced health prose as sufficient for the current evaluation scope. This is confirmed as a good match: the corpus provides the same institutional register and authorial voice as source documents that Ethiopian MOH materials would be translated from.
- **Datapoint citations:**
  - [D11] Example 4 (health, split=train): "Measures for the prevention of cholera mostly consist of providing clean water and proper sanitation" — WHO cholera prevention sentence; cholera is endemic in Ethiopia, making this directly relevant.
  - [D41] Example 1 (doc_health, split=train): "WHO helps to restore primary care services so that facilities can deliver essential services, including immunization, basic treatment for common illnesses, acute malnutrition and maternal care" — WHO response article encompasses immunization and maternal care, both central to the deployment domain.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Annotator credentials for Amharic reference translations are undocumented and likely do not match deployment ground-truth authority
- **Dimension(s):** OC
- **Observation:** The four named Amharic translators (Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, Lidetewold Kebede, per Q109) appear in data rows containing complex clinical terminology — including AMR, antimicrobials, hemorrhagic fever treatment (ribavirin), and infant nutrition guidance. The benchmark documentation provides no professional credentials, institutional affiliations, or clinical backgrounds for these translators. No MOH certification or EFDA terminology training is documented. The terminology in the Amharic translations (e.g., loanword handling for "superbugs," "ribavirin," drug class names in [D43], [D47]) is visible in the data but cannot be independently verified against any institutional standard.
- **Deployment relevance:** The user explicitly identifies MOH-trained clinical translators or Amharic-speaking physicians as the authoritative ground-truth population. If the benchmark's Amharic reference translations were produced by general-purpose translators without clinical MOH credentials, the reference translations against which system outputs are scored may not reflect the clinical accuracy standards the deployment requires. This is the most consequential OC gap: evaluation scores computed against these references may validate translations that do not meet MOH clinical standards, and vice versa.
- **Datapoint citations:**
  - [D43] Example 4 (doc_health, split=train): "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ ... 'ሱፐርበግስ(superbugs)'" — The transliterated English term "superbugs" in Amharic parentheses suggests a translator choice that may or may not conform to MOH/EFDA approved terminology for this concept.
  - [D47] Example 5 (doc_health, split=train): "ፀረ-ቫይረስ መድሃኒት ... ribavirin" — The drug name "ribavirin" is retained in transliterated form; it is unverifiable whether this matches the EFDA-approved Amharic pharmaceutical terminology for this antiviral.
  - [D44] Example 3 (doc_health, split=train): "ጨቅላ ህፃናት ከ6 ወር ጀምሮ የተጣራ፣ የተፈጨ እና ከፊል ጠጣር ምግቦችን" — Maternal-health guidance translated with specific clinical language; conformance to MOH terminology for infant feeding guidance is unverifiable.

#### CRITICAL Concern 2: No mechanism for evaluating MOH/EFDA glossary compliance — the primary deployment success criterion is entirely unoperationalized
- **Dimension(s):** OO
- **Observation:** The benchmark's scoring functions — d-BLEU, d-chrF, GPT-4o-as-judge, and human DA — are all agnostic to any institutional terminology list. The data rows contain medical terminology choices (clinical vocabulary for AMR, vaccines, infant nutrition, hemorrhagic fever) that would need to be assessed against MOH and EFDA approved glossaries in the deployment context, but the benchmark provides no mechanism to do this. The planned terminology harmonization step for translators (Q121) is not documented as having been completed, and no reference to any Ethiopian-specific glossary is found in the data or documentation.
- **Deployment relevance:** The user states that glossary compliance is a primary success criterion. A system that scores well on d-chrF against AFRIDOC-MT references may nonetheless fail to comply with MOH/EFDA approved Amharic medical terminology. Conversely, a system that correctly uses MOH-approved terminology might score lower if that terminology differs from the benchmark translators' choices. This renders d-chrF and BLEU scores partially construct-invalid as measures of the deployment's primary success criterion.
- **Datapoint citations:**
  - [D5] Example 4 (doc_health, split=train): "ፀረ-ተሕዋስያንን መቋቋም(AMR)" — The Amharic rendering of "antimicrobial resistance" uses a descriptive phrase; whether this matches the Academy of Ethiopian Languages Amharic Medical Dictionary or the MOH/EFDA approved term is unverifiable from the benchmark alone.
  - [D4] Example 3 (doc_health, split=train): "ተጨማሪ ምግብ ማጠቃሊያ" (complementary feeding) — Specific infant feeding terminology in Amharic; compliance with MOH approved nutrition terminology cannot be assessed.
  - [D21] Example 4 (doc_health, split=train): "Antimicrobial resistance ... AMR threatens the effective prevention and treatment of an ever-increasing range of infections" — English source with clinical pharmacology terminology that requires verified EFDA-approved Amharic equivalents.

---

#### MAJOR

#### MAJOR Concern 1: A substantial portion of the health corpus covers topics with low direct relevance to Ethiopian MOH clinical priorities
- **Dimension(s):** IC, IO
- **Observation:** While the health corpus is domain-aligned at the level of "WHO health articles," a significant subset covers topics that are either geographically remote from Ethiopia or substantively distant from clinical practice guidelines, vaccination schedules, and maternal-health booklets. In the sampled data: tropical cyclones (Ex. 1, doc_health — [D1]), Crimean-Congo hemorrhagic fever endemic to the Balkans/Central Asia (Ex. 5, doc_health — [D32]), Afghanistan polio campaigns ([D7], [D34]), volcanic eruptions ([D33]), international health financing mechanisms ([D25], [D27], [D28]), TRIPS/IP policy ([D46]), COVID-19 international travel guidance ([D19]), and IHR process documentation ([D20], [D35]). These topics occupy a substantial share of sampled examples.
- **Deployment relevance:** The deployment translates clinical practice guidelines, vaccination schedules, and maternal-health booklets — all of which involve disease-treatment, preventive care, and patient-facing language. Training or fine-tuning a system on the AFRIDOC-MT health corpus, then evaluating it using these examples, will include substantial signal from topics (disaster preparedness, international health law, health financing) that do not appear in the actual deployment document types.
- **Datapoint citations:**
  - [D33] Example 3 (doc_health_25, split=train): "A volcano is a vent in the Earth's crust from which eruptions occur. There are about 1500 potentially active volcanoes worldwide." — WHO volcanic eruption article; not relevant to Ethiopian MOH clinical materials.
  - [D7] Example 1 (doc_health_10, split=train): "ናንጋርሃር እና ኩናር አውራጃዎች ... 1.7 ሚሊዮን ተመላሾች" — Afghanistan polio returnees article; geographic and contextual mismatch with Ethiopia.
  - [D32] Example 5 (doc_health, split=train): "Crimean-Congo haemorrhagic fever (CCHF) ... CCHF is endemic in all of Africa, the Balkans, the Middle East and in Asia." — CCHF hemorrhagic fever; not a primary Ethiopian clinical guideline topic.
  - [D26] Example 4 (doc_health_10, split=train): "Vector control operations framework for Zika virus" — Zika is not endemic in Ethiopia.

#### MAJOR Concern 2: Significant tech corpus included in the benchmark — entirely irrelevant to MOH clinical deployment
- **Dimension(s):** IO
- **Observation:** Approximately half the benchmark data is the tech corpus (`doc_tech`, `doc_tech_5`, `doc_tech_10`, `doc_tech_25`, `tech`), consisting of Techpoint Africa news articles about Nigerian/African technology startups, fintech, cryptocurrency, content regulation, and product management. The sampled examples include articles on Cellulant layoffs [D14], Nestcoin crypto funding [D13], Nigerian VC investment [D22], South Africa online content regulation, and Indian edtech [D38].
- **Deployment relevance:** The deployment is exclusively concerned with health document translation for MOH distribution. Tech-domain data contributes no valid signal for health translation quality and could introduce domain-specific vocabulary and register patterns into fine-tuning or evaluation that actively degrade health translation performance. If researchers evaluate models on the combined benchmark, tech-domain scores would dilute health-domain signals.
- **Datapoint citations:**
  - [D14] Example 2 (doc_tech, split=train): "South Africa wants to stop harmful content online ... YouTube ... NALA launches payments from UK and EU to Nigeria ... Cellulant to lay off 20% of its workforce" — Entirely irrelevant to clinical translation deployment.
  - [D38] Example 1 (doc_tech_10, split=train): "የሕንድ ኢድቴክ ኢንዱስትሪ ... ሕንድ ከዩናይትድ ስቴትስ ... Central Square Foundation" — Indian edtech article in Amharic; no relevance to Ethiopian MOH.
  - [D22] Example 1 (doc_tech_25, split=train): "One benefit Fatanmi identifies is its effect on marketing a business... Gen Zs ... Building in public" — Startup marketing article; entirely irrelevant.

#### MAJOR Concern 3: GPT-4o-as-judge documented as unreliable for Amharic — deployment cannot use it as scalable quality proxy
- **Dimension(s):** OO, OF
- **Observation:** The benchmark documentation explicitly states that GPT-4o produced inconsistent judgments when translating into African languages (Q66, Q67, Q99, Q218, Q219) and that the benchmark consequently deprioritizes it in favor of human DA for African languages. This is independently corroborated by the Walia-LLM study (EMNLP 2024). The data itself — including long clinical Amharic texts such as [D1], [D5], [D43] — cannot be reliably scored by GPT-4o as a judge.
- **Deployment relevance:** The deployment would benefit from a scalable, automated quality-assessment mechanism to evaluate clinical Amharic translations without requiring human clinical translators for every document. The benchmark confirms that GPT-4o-as-judge cannot fill this role for Amharic, and no validated document-level embedding metric (e.g., long-context AfriCOMET) exists for Amharic. This leaves d-chrF/d-BLEU as the primary scalable metrics, which cannot capture MOH/EFDA terminological compliance.
- **Datapoint citations:**
  - [D43] Example 4 (doc_health, split=train): "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ ... 'ሱፐርበግስ(superbugs)'" — A complex clinical sentence with a mixed Amharic/English term; GPT-4o's inconsistent Amharic capabilities mean it cannot reliably judge whether this rendering is acceptable.
  - [D47] Example 5 (doc_health, split=train): "ህክምና፡- ... ፀረ-ቫይረስ መድሃኒት ... ribavirin" — Drug terminology requiring clinical judgment that GPT-4o cannot reliably provide.

#### MAJOR Concern 4: Inter-annotator agreement for Amharic human evaluation is low (α = 0.46), compounding the annotator-credentials gap
- **Dimension(s):** OC
- **Observation:** Even among the benchmark's own Amharic human evaluators, Krippendorff's alpha is 0.46 — the lowest agreement level among the five languages (Yorùbá achieves 0.81). This means the human DA signal for Amharic is noisy even within the benchmark's own framework, before considering whether those annotators represent the deployment's authoritative population (MOH-trained clinical translators). The data cannot reveal why agreement is low — it could reflect genuine translation ambiguity, annotator background differences, or the fine granularity of the 0-100 scale — but it means that even if benchmarking scores are computed, the human evaluation signal has substantial uncertainty for Amharic specifically.
- **Deployment relevance:** The deployment requires confident quality signals for clinical Amharic translations. An inter-annotator agreement of α = 0.46 implies that even if the benchmark's human evaluators were acceptable proxies for MOH translators (which is unverified), approximately half their quality signal would be noise. This compounds the annotator-credentials concern: the reference translation quality signal for Amharic is both uncertain in provenance and noisy in annotation.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): The complex multi-paragraph Amharic cyclones article — exactly the type of document where annotator disagreement on translation quality would be expected, given the technical register and length.
  - [D44] Example 3 (doc_health, split=train): "ጨቅላ ህፃናት ከ6 ወር ጀምሮ የተጣራ፣ የተፈጨ" — Maternal-health clinical instruction where annotator agreement on the correct Amharic rendering of feeding guidance would matter most for the deployment.

---

#### MINOR

#### MINOR Concern 1: Translationese effects visible in Amharic data — English-centric structural patterns may not reflect natural Amharic clinical register
- **Dimension(s):** IC, OC
- **Observation:** The benchmark explicitly acknowledges translationese risk (Q103–Q105). In the sampled Amharic data, English structural patterns appear clearly: parenthetical acronyms like "(AMR)" and "(CCHF)" embedded in Amharic text [D5, D6], English loanwords like "superbugs" (ሱፐርበግስ) with parentheses [D43], and direct transliterations of drug names like "ribavirin" [D47]. The document-level Amharic text in [D1] follows the WHO article's topic-sentence structure closely, which may not reflect how Amharic health writers would naturally organize health guidance.
- **Deployment relevance:** If a system trained/evaluated on AFRIDOC-MT produces translations with English-centric structural patterns (calqued phrasing, parenthetical acronyms, transliterated drug names), these may be judged acceptable by d-chrF (since they match the references) but may be considered unnatural or confusing by MOH clinical translators or semi-literate patients — the actual end-users.
- **Datapoint citations:**
  - [D43] Example 4 (doc_health, split=train): "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ ... 'ሱፐርበግስ(superbugs)'" — English loanword in Amharic parentheses suggests translated-from-English structural dependency.
  - [D47] Example 5 (doc_health, split=train): "ፀረ-ቫይረስ መድሃኒት ... ribavirin" — Untranslated drug name retained in Amharic text.

#### MINOR Concern 2: Sentence-level health config (`health`) contains highly varied content — some items have marginal clinical relevance
- **Dimension(s):** IC
- **Observation:** The `health` (sentence-level) config contains short, standalone sentences that are contextually disconnected from the document-level clinical narrative. Samples include health financing policy [D23], biological therapeutics standardization [D24], blood products [D40], and OCV sentence fragments [D12]. While individually these are within the "health" domain, their standalone nature removes the document context that makes clinical translation meaningful and assessable.
- **Deployment relevance:** Sentence-level evaluation without document context is less relevant for the deployment (clinical practice guidelines, maternal-health booklets) than document-level evaluation. The `doc_health` and chunked configs are better suited to the deployment's needs than the `health` sentence-level config.
- **Datapoint citations:**
  - [D23] Example 2 (health, split=train): "However, what is clear is that health systems need to predominantly rely on public revenue sources: mandatory, pre-paid and pooled" — Health financing sentence lacking clinical guideline register.
  - [D24] Example 3 (health, split=train): "the development and promotion of WHO international reference standards helps ensure that biological therapeutics are standardized between different manufacturers" — Regulatory/technical sentence without clinical patient-facing relevance.

#### MINOR Concern 3: Regional Amharic register variation across Ethiopia's health bureaus is unaddressed — single national-standard reference
- **Dimension(s):** OC
- **Observation:** The benchmark produces a single Amharic reference translation per document (by four translators working independently, with harmonization planned but not confirmed as completed). No sub-national or regional register variation (Tigray, Oromia, Somali, Amhara bureaus) is represented. The translators are identified by name but no regional affiliation is documented.
- **Deployment relevance:** The deployment serves multiple regional health bureaus where Amharic is used as a lingua franca by non-native speakers (Oromia, Tigray, Somali regions). Whether a single Addis Ababa-centric reference translation would be uniformly accepted as ground truth across all bureaus was not resolved in elicitation. This is a lower-severity concern given that Amharic dialects are mutually intelligible, but health register preferences may diverge, particularly for localized disease terminology or administrative terms.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "የሞቃታማ ዐውሎ ነፋሶች" — A single Amharic rendering of "tropical cyclone" — whether this specific vocabulary choice would be accepted by health workers in Somali or Tigray regions is unverifiable.
  - [D4] Example 3 (doc_health, split=train): "ጨቅላ ህፃናት" (infant) — A single Amharic term for infant used consistently in the complementary feeding article; regional health registers may prefer alternative terminology.

---

### Content Coverage Summary

The sampled data contains a mixture of WHO health articles and Techpoint Africa technology news articles, all originating in English with human translations into Amharic, Hausa, Swahili, Yorùbá, and Zulu. The health corpus includes a wide range of WHO topics: maternal/infant nutrition (complementary feeding, breastfeeding), immunization/vaccination (cholera OCV, polio), disability, antimicrobial resistance, infectious diseases (CCHF, AMR), public health emergencies, and health systems governance (health financing, IHR, TRIPS). Medical terminology is present throughout the Amharic translations in Ethiopic script, including clinical terms, drug names (often transliterated), and health systems vocabulary.

Approximately half the sample is tech-domain (Techpoint Africa news), which is entirely irrelevant to the deployment. Within the health corpus, the most deployment-relevant subset — maternal-child health (complementary feeding, infant nutrition, breastfeeding) and immunization articles — constitutes a minority of the total health samples, with health policy, health financing, emergency preparedness, and globally generic disease topics occupying a substantial share. Document-level configs preserve multi-paragraph health articles; the sentence-level config provides shorter, context-free sentence pairs.

Amharic text quality in the available samples appears generally consistent in terms of script rendering and sentence fluency, but translator credential verification and MOH/EFDA terminology compliance cannot be assessed from the data alone.

---

### Limitations

1. **Sample size**: 51 examples were reviewed across 10 configs. The full benchmark contains 28,201 rows; the health domain has ~10,000 sentences and the tech domain ~10,000. The sampled examples provide directional evidence but cannot characterize the full distribution of topics, terminology choices, or translation quality across the entire corpus.

2. **Annotator credentials unverifiable from data**: The data rows themselves contain no metadata about translator credentials. Verification of MOH certification or clinical training background for the four Amharic translators requires direct contact with AFRIDOC-MT authors.

3. **MOH/EFDA glossary compliance unassessable from data alone**: No reference terminology list is included with the benchmark. Verifying whether specific Amharic term choices in the data conform to MOH/EFDA standards requires comparison against those glossaries, which are not publicly accessible in a verified form.

4. **Inter-annotator variation within the four Amharic translators unobservable in this sample**: The benchmark uses one translator per sentence (distributed equally), so single-document rows do not show variance across all four translators for the same passage. This limits assessment of translation consistency.

5. **Translationese extent not quantifiable from inspection**: Whether the Amharic translations exhibit systematic translationese effects (unnatural syntax, calqued phrase structure) requires native-speaker clinical evaluation beyond what visual inspection of the Ethiopic text can determine.

6. **GPT-4o judge output not directly observable**: The benchmark's GPT-4o evaluation results are reported in the paper but the per-document GPT-4o scores are not included in the HuggingFace dataset release, so the inconsistency documented for Amharic cannot be directly observed in the sampled rows.

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
  "benchmark": "afridoc_mt",
  "region": "Ethiopia Ministry of Health — Amharic Clinical Translation Deployment",
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
