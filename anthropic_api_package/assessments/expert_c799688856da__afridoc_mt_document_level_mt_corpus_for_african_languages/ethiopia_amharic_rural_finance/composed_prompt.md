I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **AFRIDOC-MT: A Document-Level Multi-Parallel Translation Dataset for African Languages** is valid for use in **Amhara Region Agricultural & Microfinance Document Translation — Cooperative and Rural MFI End-Users**.

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
AFRIDOC-MT covers a single task type: document-level machine translation
between English and five African languages (plus multi-way translation among
the six languages). The benchmark supports both sentence-level and
pseudo-document-level (fixed-size chunk) translation as subtasks [Q3, Q35].
Document-level translation is motivated by the need to handle context-dependent
phenomena including coreference resolution, lexical disambiguation, and lexical
cohesion [Q16], and the authors situate the benchmark as addressing the gap left
by existing sentence-level MT datasets [Q13, Q15]. The genres evaluated are
exclusively health and information technology news [Q1, Q2, Q80]; no
agricultural, legal, regulatory, administrative, or financial document types are
included. The only competing document-level dataset acknowledged, TICO-19, is
restricted to COVID-19 health topics [Q14], confirming that regulatory and
policy genres remain entirely absent from the benchmarking landscape covered by
this work. Twelve model configurations are evaluated [Q41] spanning five
encoder-decoder systems [Q37] and multiple decoder-only LLMs [Q39], with prompt
sensitivity assessed using three prompts per LLM [Q91].

### Input Content
English source documents were scraped from Techpoint Africa (technology news)
and the World Health Organization (health news), yielding approximately 10,000
English sentences per domain from 334 health and 271 technology articles [Q18,
Q22]. Data is dual-licensed under CC BY-NC-SA 3.0/4.0 and characterized as
ethically sourced from publicly available materials selected to represent
different cultural perspectives and minimize bias [Q34, Q106]. MADLAD-400, one
of the evaluated models, was trained on Common Crawl [Q137]; Toucan was
pre-trained on large multilingual texts covering over 500 African languages [Q140].
The dataset authors acknowledge that since all source material originates in
English, translated African-language sentences may exhibit translationese —
unnatural syntax, overly literal phrasing, and a structural and semantic bias
toward English [Q103, Q104, Q105]. No agricultural proclamation texts,
cooperative membership regulations, land-tenure documents, subsidy scheme
notices, or microfinance credit-scheme terms appear anywhere in the source
corpus.

### Input Form
The benchmark is entirely text-based. Amharic is explicitly present in Ethiopic
(non-Latin) script [Q1, Q127]; Yorùbá uses a Latin-based script with diacritics
[Q77]; the remaining languages (Hausa, Swahili, Zulu) use Latin script. Token
length statistics show meaningful cross-lingual variation: Hausa and Yorùbá
produce longer tokenizations than English, while Amharic and Zulu produce shorter
ones [Q33]. Non-Latin script and diacritics caused Amharic and Yorùbá to exceed
model token limits, requiring chunking into pseudo-documents of k=10 sentences
[Q47, Q48, Q128]; the token limit for Amharic was specifically increased to
accommodate its script properties [Q162]. The annotation workflow used .csv files
in Google Sheets or Excel [Q122], with explicit instructions to preserve
paragraph-separating empty rows [Q119]. No audio, image, or OCR components are
involved.

### Output Ontology
The benchmark's output scoring framework evaluates translation adequacy,
fluency, and discourse coherence. Automated metrics are document-level chrF
(d-chrF) and document-level BLEU (d-BLEU), computed via SacreBLEU with
bootstrap resampling [Q51, Q52]; d-chrF is reported as primary because it
better captures the morphological richness of African languages [Q53]. GPT-4o
evaluates fluency on a 1–5 scale and counts content errors (CE), lexical
cohesion errors (LE), and grammatical cohesion errors (GE) [Q54, Q55, Q180,
Q191]. The benchmark explicitly defines cohesion as how text is connected using
grammar and vocabulary to ensure smooth sentence flow [Q187, Q188], with lexical
cohesion mistakes involving vocabulary usage and synonym issues [Q189] and
grammatical cohesion mistakes involving pronoun, conjunction, and clause-linking
problems [Q190]. Human direct assessment uses a 0–100 continuous quality scale
[Q195] via the ESA protocol in the Appraise framework [Q196]. No rubric
component addresses terminological consistency — the stable cross-clause
rendering of named entities such as subsidy scheme names, land-tenure category
labels, or proclamation-derived legal terms. The label ontology is calibrated
for news discourse adequacy and fluency, not for the regulatory precision
required in legal-administrative translation. GPT-4o's reliability as a judge
for African language translation directions is explicitly questioned [Q67, Q85,
Q219]; human evaluation is ultimately preferred for translations into African
languages [Q68].

### Output Content
Translation was performed by four expert translators per language, recruited
through a native-speaker language coordinator [Q23, Q24]. The 10,000 sentences
per language were distributed equally among translators who worked sentence-by-
sentence with access to full document context [Q25]. A pre-translation workshop
was conducted to share terminology creation experience and existing resources
[Q26]; translators were instructed not to use machine translation engines [Q120],
and a terminology harmonization list was promised during the process [Q121].
Quality control used AfriCOMET quality estimation (threshold 0.65 for manual
review) [Q28, Q29] and manual inspection by language coordinators [Q27]. Human
evaluation for model outputs used three native-speaker annotators per language,
primarily drawn from the translation team [Q194], each evaluating 80 documents
with 30 shared for inter-annotator agreement [Q197]. Inter-annotator agreement
(Krippendorff's alpha) was 0.46, 0.57, 0.40, and 0.54 for Amharic, Hausa,
Swahili, and Zulu respectively — relatively low [Q71, Q211, Q212]. Named
Amharic translators are listed [Q109] but no documentation of their
institutional affiliation, domain expertise, or familiarity with
agricultural/legal Amharic is provided. Human evaluation for Zulu could not
be conducted due to annotator recruitment difficulties [Q100].

### Output Form
The benchmark produces and evaluates text-only translation outputs. All
automated metrics (d-chrF, d-BLEU, s-COMET/chrF/BLEU) and human assessments
operate on plain text [Q51, Q52, Q170, Q172]. Document structure is partially
preserved at the corpus level — paragraph-separating rows are maintained in the
annotation workflow [Q119] and sentence-to-document realignment is performed
for metric computation [Q51, Q57] — but no metric assesses structural fidelity
(preservation of numbered clauses, tables, or signature blocks). Due to context
length limits, full documents are not translated atomically; they are processed
as pseudo-document chunks of k=10 sentences [Q48, Q49] or sentence-by-sentence
[Q201], with outputs merged for evaluation. Embedding-based document-level
metrics for African languages remain unavailable [Q50, Q96, Q176]: AfriCOMET
cannot be applied at document level due to its 512-token backbone limit [Q175],
and ModernBERT-based QE produced undifferentiated scores across all models
[Q97, Q98]. Greedy decoding is used throughout [Q155].


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This paper introduces AFRIDOC-MT, a document-level multi-parallel translation dataset covering English and five African languages: Amharic, Hausa, Swahili, Yorùbá, and Zulu." |
| Q2 | 1 | input_content | "The dataset comprises 334 health and 271 information technology news documents, all human-translated from English to these languages." |
| Q3 | 1 | input_ontology | "We conduct document-level translation benchmark experiments by evaluating the ability of neural machine translation (NMT) models and large language models (LLMs) to translate between English and these languages, at both the sentence and pseudo-document levels, the outputs being realigned to form complete documents for evaluation." |
| Q4 | 1 | output_form | "Our results indicate that NLLB-200 achieves the best average performance among the standard NMT models, while GPT-4o outperforms general-purpose LLMs." |
| Q5 | 1 | input_ontology | "Fine-tuning selected models leads to substantial performance gains, but models trained on sentences struggle to generalize effectively to longer documents." |
| Q6 | 1 | output_form | "Furthermore, our analysis reveals that some LLMs exhibit issues such as under-generation, over-generation, repetition of words and phrases, and off-target translations, specifically for translation into African languages." |
| Q7 | 1 | input_ontology | "In addition, AFRIDOC-MT supports multi-way translation, allowing translations not only between English and the African languages but also between any two of the languages covered." |
| Q8 | 1 | output_form | "We evaluate performance using automatic metrics and compare the results of encoder-decoder models with decoder-only LLMs" |
| Q9 | 1 | output_content | "Jesujoba O. Alabi, Israel Abebe Azime, Miaoran Zhang, Cristina España-Bonet, Rachel Bawden, Dawei Zhu, David Ifeoluwa Adelani, Clement Oyeleke Odoje, Idris Akinade, Iffat Maab, Davis David, Shamsuddeen Hassan Muhammad, Neo Putini, David O. Ademuyiwa, Andrew Caines, Dietrich Klakow" |
| Q10 | 1 | output_content | "Masakhane NLP, Saarland University, Saarland Informatic Campus, DFKI GmbH, Barcelona Supercomputing Center, Inria Paris France, Mila McGill University & Canada CIFAR AI Chair, University of Ibadan Nigeria, National Institute of Informatics Japan, Selcom Tanzania, Imperial College London, University of KwaZulu-Natal, Loughborough University U.K, University of Cambridge U.K." |
| Q11 | 2 | input_ontology | "There exist several MT evaluation benchmark datasets for African languages." |
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
| Q49 | 5 | output_form | "To select an appropriate chunk size, we conducted initial tests with k = 1 (sentence-level), 5, 10, and 25, choosing k = 10 for our experiments." |
| Q50 | 5 | output_form | "Evaluating document-level translation remains challenging, as existing automatic metrics struggle to capture improvements and account for discourse phenomena (Jiang et al., 2022; Dahan et al., 2024), and embedding-based metrics have not been explored in this context for African languages due to the lack of data." |
| Q51 | 5 | output_form | "Hence, we realigned sentence-level or pseudo-translation outputs into full documents, then computed BLEU (Papineni et al., 2002) and chrF (Popović, 2015) to create document BLEU (d-BLEU) and document chrF (d-chrF)." |
| Q52 | 5 | output_form | "Metrics were computed using SacreBLEU (Post, 2018) with bootstrap resampling (n = 1000) to report 95% confidence intervals." |
| Q53 | 5 | output_form | "We report d-chrF scores for the best prompt per model and language direction in the main text, as chrF better captures the morphological richness of African languages (Adelani et al., 2022), with full results provided in Appendix C." |
| Q54 | 5 | output_ontology | "We use GPT-4o as a judge to evaluate translation outputs, following recent work showing LLMs' effectiveness in assessing translation quality and analyzing errors (Wu et al., 2024; Sun et al., 2025)." |
| Q55 | 5 | output_ontology | "Following Sun et al. (2025), we assess each translated document's fluency, content errors (CE), and cohesion errors—specifically lexical (LE) and grammatical (GE) errors—using GPT-4o, with evaluation limited to a few model outputs due to cost constraints (Appendix B.6)." |
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
| Q66 | 7 | output_form | "However, when translating into African languages, the results are less consistent." |
| Q67 | 7 | output_ontology | "These inconsistencies raise concerns about GPT-4o's reliability." |
| Q68 | 7 | output_form | "Consequently, we focus on human evaluation going forward." |
| Q69 | 7 | output_content | "In Table 10 we report average direct assessment (DA) scores (on a scale from 0 to 100) from three annotators per language for the health domain, when translating into four African languages." |
| Q70 | 7 | output_content | "For each language, we used 30 documents across models and both domains to compute inter-annotator" |
| Q71 | 8 | output_content | "We obtained Krippendorff's alpha values of ≥ 0.40, which are relatively low due to the fine granularity of the evaluation scale." |
| Q72 | 8 | output_form | "Human evaluation results align closely with d-chrF, which favors sentence-level translations over pseudo-document translations when translating into African languages." |
| Q73 | 8 | output_form | "Among the models, LLaMAX3-SFT1 receives higher ratings at the sentence-level but is rated lower when translating pseudo-documents." |
| Q74 | 8 | output_form | "In contrast, LLaMAX3-SFT10 receives slightly lower ratings than LLaMAX3-SFT1 at the sentence-level but is rated higher in the pseudo-document setting." |
| Q75 | 8 | output_form | "GPT-3.5 is generally rated as the weakest model across languages, except for Swahili, where its performance is comparatively better." |
| Q76 | 8 | output_content | "Our qualitative analysis, based on feedback from native speakers who are also authors, indicates that GPT-3.5 frequently over-generates in the pseudo-document setup by repeating words and phrases—except in Swahili, where it performs best." |
| Q77 | 8 | input_form | "However, for Yorùbá, it often uses inconsistent or partial diacritics, resulting in inaccuracies." |
| Q78 | 8 | output_form | "LLaMAX3-SFT1 also exhibits repetition in pseudo-document translations, likely due to a length generalization problem (Anil et al., 2022), and does so more than LLaMAX3-SFT10." |
| Q79 | 8 | output_form | "For the other four languages, LLaMAX3-SFT1 with the sentence-level setup was rated higher than other models and configurations, owing to better context preservation and fewer repetitions." |
| Q80 | 9 | input_content | "We introduce AFRIDOC-MT, a document-level translation dataset in the health and tech domains for five African languages." |
| Q81 | 9 | input_ontology | "We benchmarked various models, fine-tuning selected ones." |
| Q82 | 9 | input_form | "Due to context length limits, documents were translated either sentence by sentence or as pseudo-documents." |
| Q83 | 9 | output_form | "Outputs were evaluated using standard MT metrics, GPT-4o as a judge, and human direct assessment." |
| Q84 | 9 | output_form | "NLLB-200 was the strongest built-in MT model, while GPT-4o outperformed general-purpose LLMs." |
| Q85 | 9 | output_ontology | "However, our DA and qualitative analysis found GPT-4o's judgments inconsistent for African languages, and sentence-by-sentence translation proved more effective for some languages." |
| Q86 | 9 | input_ontology | "We evaluated only a small subset of the numerous multilingual LLMs available." |
| Q87 | 9 | input_form | "Our experiments were also limited by the context length of the LLMs, particularly for open LLMs." |
| Q88 | 9 | input_form | "Except for LLama3.1, all other open LLMs have a context length of 8192 tokens, while encoder-decoder models were primarily based on T5." |
| Q89 | 9 | input_form | "This makes it difficult to use the context length beyond a certain limit, making full document translation infeasible." |
| Q90 | 9 | output_form | "LLMs are prone to variance in performance based on the prompt." |
| Q91 | 9 | input_ontology | "We therefore evaluated them for translation using three different prompts." |
| Q92 | 9 | output_form | "However, it is possible that our prompts were not optimal." |
| Q93 | 10 | input_ontology | "Africa is home to thousands of indigenous languages, many of which exhibit unique linguistic properties. However, due to the high cost of translation using human translators and limited available funding, it is currently impossible to cover all languages. As a result, we focused on just five languages." |
| Q94 | 10 | input_ontology | "AFRIDOC-MT is a multi-way parallel dataset. However, due to the cost of running inference over three prompts and across all 30 translation directions for all the models evaluated, most of our analysis is limited to translation tasks between English and the five African languages." |
| Q95 | 10 | output_form | "While we fine-tuned NLLB-200, LLama3.1 and LLaMAX3 on all 30 directions, we only provide results from NLLB-200 for all directions both before and after fine-tuning for sentence-level and pseudo-document tasks in the Appendix D." |
| Q96 | 10 | output_form | "Quality evaluation in MT is an open and ongoing area of research, especially for document-level translation. Recent works have proposed embedding-based metrics for evaluation at both the sentence and document levels. While this has been well explored for high-resource language pairs, it remains underexplored for African languages, although there is a tool, AfriCOMET, that works for sentence-level evaluation in African languages." |
| Q97 | 10 | output_form | "However, we evaluated the document-level translation outputs using ModernBERT-base-long-context-qe-v1, trained on the WMT human evaluation dataset across 41 language pairs, including over 20 languages and three African languages (Hausa, Xhosa, and Zulu), two of which are included to our work." |
| Q98 | 10 | output_form | "However, the scores were nearly identical across all models, offering no meaningful differentiation. Hence, for our document-level evaluation, in addition to lexical-based metrics, we incorporated three other evaluation approaches: using GPT-4o as a judge, human evaluation, and qualitative analysis." |
| Q99 | 10 | output_ontology | "GPT-4o was employed to assess and rate the translation outputs of four models. While its ratings were consistent for translations into English, the same was not observed for translations into African languages, likely due to the model's limited understanding of these languages." |
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
| Q119 | 18 | output_form | "Please do not delete double empty rows, as they serve to separate paragraphs. Also, avoid deleting any rows, columns, or provided text." |
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
| Q142 | 20 | input_content | "Gemma2 (Gemma Team et al., 2024) is a decoder-only LLM trained on billions of tokens sourced from the web. The training data primarily consists of English-language text, but it also includes code and mathematical content. While Gemma2 has an English-centric focus, it also possesses multilingual capabilities. We evaluate the base Gemma2 model with 9B parameters, as well as its instruction-tuned version." |
| Q143 | 20 | input_form | "LLama3.1 (Dubey et al., 2024) is another decoder-only LLM trained on trillions of tokens across multiple languages. It was fine-tuned using existing instruction datasets as well as synthetically generated instruction data to create its instruction-tuned version. One advantage LLama3.1 has over other models is its context window of 128K tokens, the largest among all models considered in this work, making it particularly suitable for document-based tasks such as document-level translation. We evaluate the base LLama3.1 model with 8B parameters, as well as its instruction-tuned version." |
| Q144 | 20 | input_ontology | "LLaMAX3 (Lu et al., 2024) is a multilingual LLM built on the LLama3 with 8B parameters as its base. It was trained on 102 languages, including several African languages, through continued pretraining. Using an English instruction dataset (Alpaca), it was further fine-tuned to create LLaMAX3-Alpaca. We evaluated both models and compared their performance across various tasks." |
| Q145 | 20 | input_form | "We perform supervised fine-tuning to tailor LLMs for translation tasks. To train sentence-level MT systems, we use all parallel sentences from AFRIDOC-MT to construct the training set, enabling the LLMs to translate across multiple directions and domains. Following Zhu et al. (2024b), we augment the parallel data with translation instructions, which are randomly sampled from a predefined set of 31 MT instructions for each training example." |
| Q146 | 21 | input_form | "To train document-level MT systems, we follow the same process, but train on longer segments formed by concatenating multiple sentences." |
| Q147 | 21 | input_form | "When fine-tuning, we use a learning rate of 5e−6 and an effective batch size of 64." |
| Q148 | 21 | output_form | "Models are trained for only one epoch, as further training does not result in improvements and may even lead to performance degradation." |
| Q149 | 21 | input_form | "we fine-tuned the 1.3B version of NLLB-200 for sentence and pseudo-document (with 10 sentences) translation using the Fairseq (Ott et al., 2019) codebase." |
| Q150 | 21 | input_content | "We used all the training examples from 30 language directions across both domains." |
| Q151 | 21 | input_form | "The model was fine-tuned for 50k steps using a learning rate of 5e−5, token batch size of 2048 and a gradient accumulation of 2." |
| Q152 | 21 | output_form | "The checkpoint with the lowest validation loss was selected as the best model for evaluation." |
| Q153 | 21 | output_form | "The models were evaluated using different tools. For example, both the NLLB-200 and M2M-100 models were evaluated with the Fairseq codebase, while Toucan and MADLAD-400 were evaluated using the Hugging Face (HF) codebase." |
| Q154 | 21 | output_form | "All other LLMs, including LLama3.1 (both instruction-tuned and SFT models), Gemma, and Aya-101, were evaluated using EleutherAI LM Evaluation Harness (lm-eval) tool (Biderman et al., 2024)." |
| Q155 | 21 | output_form | "In all cases, greedy decoding was used." |
| Q156 | 21 | input_form | "The models evaluated have different context lengths. For encoder-decoder models, M2M-100 and NLLB have a maximum sequence length of 1024 and 512 respectively." |
| Q157 | 21 | input_form | "Aya-101 and MADALAD, based on the T5 architecture, do not have a pre-specified maximum sequence length, so we fixed their maximum sequence length to 1024 for all experiments involving encoder-decoder models." |
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
| Q177 | 22 | output_ontology | "We use GPT-4o to assess the quality of translation output, as demonstrated by Sun et al. (2025), which shows a correlation with human judgment." |
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
| Q193 | 24 | output_content | "Translation into English was excluded, as existing automatic metrics, including GPT-based evaluations, are already reliable for this direction." |
| Q194 | 24 | output_content | "For the human evaluation, three native speakers of the African languages—primarily translators involved in the dataset creation—were recruited." |
| Q195 | 24 | output_content | "Each annotator was assigned 80 documents to evaluate, tasked with marking as many error spans as possible and rating the overall quality on a scale from 0 to 100." |
| Q196 | 24 | output_form | "This annotation followed the error span annotation (ESA) (Kocmi et al., 2024) protocol as implemented within the Appraise Evaluation Framework (Federmann, 2018)." |
| Q197 | 24 | output_content | "To assess consistency and inter-annotator agreement, 30 of the 80 documents were shared among all three annotators." |
| Q198 | 24 | output_content | "Each annotator was remunerated with $55.15" |
| Q199 | 24 | output_content | "Alongside the human direct assessment of the translation outputs, we shared a subset of the outputs with one author per language, each a native speaker." |
| Q200 | 24 | output_content | "They were tasked with analyzing the outputs to answer two key questions: (1) What common errors or flaws do the models exhibit across different setups? and (2) How fluent are the translation outputs produced by the models across the various settings?" |
| Q201 | 24 | output_form | "Given that AFRIDOC-MT is a document-level translation dataset, and due to the limited context length of most translation models and LLMs, which makes it impossible to translate a full document at once, we opted to translate the sentences within the documents and then merge them back to form the complete document. For document-level evaluation, we split the documents into chunks of 10 sentences and translate these chunks using the different models." |
| Q202 | 25 | output_form | "In Tables 19 and 20 we provide the full results on the merged pseudo-documents using d-chrF and d-BLEU." |
| Q203 | 25 | output_form | "It is important to note that we also trained and evaluated NLLB-200 for pseudo-document translation. However, due to its 512-token maximum sequence length, it is not competitive." |
| Q204 | 25 | output_form | "Our results show that both LLama3.1 and LLaMAX3 models, when fine-tuned on sentences, performed significantly worse on pseudo-document evaluations compared to the same models fine-tuned on pseudo-documents for both domains." |
| Q205 | 25 | input_form | "All these models were trained using a similar setup, with the primary difference being the data used for fine-tuning." |
| Q206 | 25 | output_form | "Overall, no clear trend is observed in MT performance across language family classes. However, Amharic (a non-Latin script language) and Yorùbá (a heavily diacriticitized language) result in the lowest chrF scores, while Swahili—the most widely spoken indigenous African language—performs best." |
| Q207 | 25 | output_form | "In Tables 21 and 22 we present the average GPT-4o evaluation results for four models." |
| Q208 | 25 | output_ontology | "When translating into African languages, there is no clear pattern: for example, GPT-3.5, despite having the lowest fluency score, also had the fewest content, lexical, and grammatical errors, which is counterintuitive." |
| Q209 | 26 | output_content | "We were able to obtain DA scores from three annotators for all the languages." |
| Q210 | 26 | output_content | "For each language, we calculated inter-annotator agreement using Krippendorff's alpha α over 30 document instances." |
| Q211 | 26 | output_content | "We obtained α scores of 0.46, 0.57, 0.40, and 0.81, and 0.54 for Amharic, Hausa, Swahili, Yorùbá, and Zulu respectively." |
| Q212 | 26 | output_content | "These are relatively low scores, except for Yorùbá." |
| Q213 | 26 | output_form | "We present the average DA scores in Tables 10 and 14 for the health and tech domains, respectively." |
| Q214 | 26 | output_form | "The results show that annotators rate documents translated at the sentence-level as higher quality than those translated at the pseudo-document level." |
| Q215 | 26 | output_form | "Additionally, GPT-3.5 received the lowest ratings among the three models." |
| Q216 | 26 | output_form | "LLaMAX3-SFT1, a model trained on sentence-level data, was rated the best across all languages when evaluated on sentences." |
| Q217 | 26 | output_form | "However, when evaluated on pseudo-documents, its performance was rated lower than that of LLaMAX3-SFT10." |
| Q218 | 26 | output_ontology | "These findings are consistent with the d-chrF scores for the models, but they do not align with the evaluations from GPT-4o as a judge." |
| Q219 | 26 | output_ontology | "These results suggest that using GPT-4o as a translation judge is not yet well-suited for low-resource languages." |
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
| Q233 | 33 | output_content | "Table 21: Document-level evaluation in the health domain, judged by GPT-4o." |
| Q234 | 34 | output_form | "Document-level evaluation in the tech domain, judged by GPT-4o. Compares sentence- vs. document-level outputs on Fluency (1–5 scale), Content Errors (CE), Lexical (LE), and Grammatical Cohesion Errors (GE)." |
| Q235 | 35 | input_ontology | "The task prompts used for evaluating LLMs are applied to both sentence-level and document-level translation tasks." |
| Q236 | 37 | output_form | "Figure 19: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into African languages" |
| Q237 | 37 | output_form | "Figure 20: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into African languages" |
| Q238 | 37 | output_form | "Figure 21: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into English" |
| Q239 | 37 | output_form | "Figure 22: d-chrF scores for some LLMs for sentence-level translation using different prompts when translating into English" |

---

## Regional Context

```yaml
name: Amhara Region Agricultural & Microfinance Document Translation — Cooperative
  and Rural MFI End-Users
abbreviation: ETH-AMH-AGRI-MFI
country: Ethiopia
sub_national_scope:
  region: Amhara Region
  administrative_context: One of Ethiopia's major federal regional states; home to
    a large rural farming population organized through agricultural cooperatives and
    served by regional microfinance institutions. Federal and regional bureau documents
    originate from Addis Ababa (federal) and Bahir Dar (Amhara regional capital).
  key_zones_or_woredas: 'Amhara Region comprises ten administrative zones: North Gondar,
    South Gondar, North Wollo, South Wollo, North Shewa, East Gojjam, West Gojjam,
    Awi (Agew Awi), Wag Hemra, and Oromia (special zone), plus Bahir Dar special zone.
    The most agriculturally significant zones for input-subsidy and cooperative-credit
    deployment are East Gojjam (Debre Markos capital; one of the top wheat-producing
    zones), North Shewa, and South Wollo, each producing more than one million quintals
    of wheat; West Gojjam, South Gondar, and North Gondar are also notable wheat producers.
    NOTE: Since April 2023, armed conflict between federal forces and Fano militias
    has severely disrupted agricultural operations, cooperative services, and fertilizer
    distribution across multiple zones, particularly East Gojjam, Central Gondar,
    and West Gojjam, creating acute deployment-context risks (food-security crisis,
    movement restrictions, supply-chain disruption). This conflict context is a material
    deployment validity factor not present at benchmark design time.

    Sources: Amhara Region zones — [WEB-1];
    wheat production zones — [WEB-2];
    conflict impact on agriculture — [WEB-3];
    UK CPIN June 2025 — [WEB-4]'
deployment_population:
  description: Farmer cooperative leaders and rural microfinance clients in Amhara
    region who must correctly interpret binding government and lender documents translated
    into Amharic. Includes cooperative extension workers who mediate document interpretation
    between bureaus and end-users.
  roles:
  - Farmer cooperative leaders (primary decision-makers and signatories for cooperative-level
    subsidy and credit agreements)
  - Rural microfinance clients (individual borrowers under ACSI, ADCSI, or equivalent
    regional MFI schemes)
  - Cooperative extension workers (intermediary interpreters of translated documents
    for less-literate members)
  institutional_context:
    microfinance_institutions:
    - 'ACSI (Amhara Credit and Savings Institution) — the largest MFI in Ethiopia
      by asset size, established 1995/licensed 1997, headquartered in Bahir Dar (Gonder
      Road, Kebele 10), with a primary mission of improving the economic situation
      of low-income productive poor in Amhara region. Serves approximately 2 million
      clients across all woredas of the region; already used by government to disburse
      agricultural input loans. Source: FinDev Gateway case study 2011 — [WEB-5];
      MFTransparency head-office record — [WEB-6]'
    - 'ADCSI (Addis Credit and Savings Institution) — operates primarily in Addis
      Ababa and is NOT the same as ACSI. ADCSI is the Addis Ababa city-based MFI;
      it does not appear to have significant operations in Amhara region rural cooperative
      contexts. The scaffold''s parenthetical note flagging this is confirmed: ADCSI
      is a distinct institution. Source: FinDev Gateway sector assessment 2008 — [WEB-7]'
    - 'Other MFIs active in Amhara region: Savings and Credit Cooperatives (SACCOs/RuSACCOs)
      operate alongside ACSI at kebele level for rural cooperative members. Ethiopia
      had 28 licensed MFIs as of recent counts; government-backed regional MFIs (ACSI,
      DECSI for Tigray, Oromia MFI) hold 25% regional government shareholding. Source:
      FinDev Gateway sector assessment — [WEB-7]'
    government_bureaus:
    - Amhara Regional Bureau of Agriculture
    - Amhara Regional Cooperative Promotion Agency
    - Ethiopian Ministry of Agriculture (federal — issues proclamations operative
      in region)
    - 'Ethiopian Agricultural Business Corporation (EABC) — sole importer of fertilizers
      in Ethiopia; manages procurement and distribution of subsidized fertilizer through
      primary cooperative unions. Source: Addis Standard 2025 — [WEB-3]'
    - 'Federal Cooperative Agency — registers cooperatives at federal level under
      Proclamation 985/2016; regional equivalent organs execute the proclamation at
      regional level. Source: UNEP LEAP — [WEB-8]'
    cooperative_framework: 'The current operative federal cooperative proclamation
      is Cooperative Societies Proclamation No. 985/2016 (Ethiopian calendar 985/2009),
      which supersedes earlier proclamations (147/1998, 274/2001, 317/2003). It establishes
      a tiered structure: Primary Cooperative Society → Cooperative Societies Union
      (formed by two or more primary societies with similar objectives) → Cooperative
      Societies Federation → Cooperative Societies League. Cooperatives may be established
      at different levels from primary up to federation. Registration is by the Federal
      Cooperative Agency or regional-level organs. Source: EthioData summary — [WEB-9];
      UNEP LEAP — [WEB-8];
      Ethiopian Ministry of Justice official text — [WEB-10]'
languages:
  target_output_language: Amharic
  script: Ethiopic (Ge'ez script, non-Latin, left-to-right)
  source_document_language: Amharic or formal Ethiopian government-register Amharic
    (federal and regional proclamation register)
  register_notes: 'Federal and regional proclamations use a distinct formal administrative
    register in Amharic that differs substantially from everyday spoken Amharic and
    from the health/IT-domain Amharic found in AFRIDOC-MT. Key register features include:
    numbered clause structures, cross-reference phrasing between articles, legally
    standardized terminology derived from Ethiopian proclamation drafting conventions,
    and fixed multi-word terms for subsidy scheme names, land-tenure categories, and
    cooperative membership tiers.'
  dialect_and_regional_variation: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice); no NLP studies on Amhara-region sub-national bureau Amharic
    register variation vs. Addis Ababa standard found in search. EthioNLP/EthioLLM
    literature covers Amharic broadly without regional sub-variety distinction. Expert
    elicitation from Amhara Regional Bureau translation staff required.]'
  end_user_spoken_variety: 'Amharic (Amhara region variety); some cooperative members
    may be more fluent in local Amharic dialects than in the formal proclamation register.
    Note: East Gojjam zone reports 99.81% Amharic as first language; North Wollo 99.28%.
    Source: Wikipedia zone articles — [WEB-11]'
  translationese_risk: AFRIDOC-MT Amharic reference translations are produced from
    English source documents, creating potential structural and semantic bias toward
    English. The deployment translates FROM Amharic government documents (not from
    English), reversing the source-language relationship and making the benchmark's
    translationese profile inapplicable.
document_genres:
  deployment_genres:
  - genre: Agricultural input subsidy notice
    description: Federal or regional bureau announcements specifying eligible inputs
      (fertilizer, seeds, pesticides), per-unit subsidy amounts, application periods,
      eligibility conditions, and distribution points. Contain numbered eligibility
      clauses, seasonal deadlines, and scheme-specific proper names.
    linguistic_features: Numbered clause structures, proclamation-derived scheme names,
      itemized eligibility conditions, penalty clauses for misuse, cross-references
      to parent proclamations
  - genre: Land-use policy update
    description: Regional or federal communications on land-tenure rights, usage restrictions,
      and cadastral registration obligations derived from Ethiopian land administration
      proclamations. Reference legally standardized tenure categories.
    linguistic_features: Land-tenure category labels (e.g., rist-derived terms, usufruct
      rights, holding certificates), numbered articles, cross-reference to proclamation
      numbers, administrative zone identifiers
  - genre: Credit-scheme terms and loan agreement
    description: MFI (ACSI/ADCSI) loan-agreement documents specifying interest rate
      schedules, repayment conditions, collateral requirements, penalty clauses, and
      cooperative-guarantee structures. Formally issued documents with signature blocks
      and numbered conditions.
    linguistic_features: Financial and legal terminology, numbered conditions, penalty
      and default clauses, cooperative membership tier references, MFI-specific scheme
      names
  - genre: Cooperative membership and governance notice
    description: Cooperative promotion agency communications on membership tiers,
      rights, obligations, annual meeting requirements, and audit schedules under
      Ethiopian cooperative law.
    linguistic_features: Cooperative proclamation-derived vocabulary, governance and
      quorum terms, membership tier designations, fixed formulaic phrases from proclamation
      templates
  benchmark_genres:
  - Health news (WHO-sourced)
  - Information technology news (Techpoint Africa-sourced)
  genre_alignment: NONE — benchmark contains zero agricultural, land-use, credit-scheme,
    or cooperative governance documents. Domain gap is total for all four deployment
    genres.
terminology:
  critical_term_categories:
  - category: Input subsidy scheme names
    examples: 'The Ethiopian Agricultural Business Corporation (EABC) is the sole
      importer and manages fertilizer procurement and subsidy distribution through
      primary cooperative unions. As of 2024/2025 season, the government procured
      24 million quintals of soil fertilizer at a total cost of $1.3 billion. Distribution
      occurs via ''primary cooperative unions'' (a formal term from Proclamation 985/2016).
      Specific named subsidy scheme terminology for current season requires verification
      from MoA/EABC official notices. Source: Addis Standard 2025 — [WEB-3]'
    translation_risk: Mistranslation or inconsistent rendering of scheme names across
      clauses can cause cooperative leaders to apply under wrong scheme or miss eligibility
      windows — binding legal and financial consequence
  - category: Land-tenure category labels
    examples: 'Key federal land proclamation: Rural Land Administration and Land Use
      Proclamation No. 456/2005 (replacing 89/1997). Amhara region has its own Revised
      Amhara National Regional State Rural Land Administration and Use Proclamation
      (2006), with subsequent amendment Proclamation No. 252/2017. Land tenure in
      Ethiopia is state ownership with usufruct rights for farmers; holding certificates
      are issued to individuals. The term ''rist'' refers to the traditional Amhara
      hereditary land-tenure concept, now largely superseded in formal documents by
      proclamation-derived usufruct and holding-certificate terminology. Source: IGAD
      Land Governance profile — [WEB-12];
      ICED background paper — [WEB-13]'
    translation_risk: Confusion between tenure categories has legal consequence for
      land-use rights and access to credit (land certificate often used as collateral)
  - category: Cooperative membership tiers
    examples: 'Proclamation No. 985/2016 defines the following tiers: Primary Cooperative
      Society (ቀዳሚ የሕብረት ሥራ ማኅበር in Amharic per Ministry of Justice Amharic title)
      → Cooperative Societies Union (የሕብረት ሥራ ማህበራት ዩኒዮን) → Cooperative Societies
      Federation → Cooperative Societies League. A union is formed by two or more
      primary cooperatives with similar objectives. Source: EthioData — [WEB-9];
      UNEP LEAP — [WEB-8]'
    translation_risk: Tier misidentification affects eligibility for collective subsidy
      applications and loan guarantee structures
  - category: MFI credit-scheme terms
    examples: '[NEEDS VERIFICATION — deferred: ACSI product names, specific Amharic
      terms for group lending guarantee, solidarity group, and repayment schedule
      terms require direct consultation of ACSI internal loan documents or Amhara
      Regional Bureau materials; not publicly documented online in requisite detail.
      ACSI is confirmed as operating group loans (self-formed borrower groups with
      collective repayment responsibility) and compulsory-savings schemes alongside
      voluntary savings products.]'
    translation_risk: Misunderstanding of penalty, default, or repayment terms has
      direct financial consequence for borrowers
  - category: Proclamation cross-reference vocabulary
    examples: '[NEEDS VERIFICATION — deferred: likely unsearchable (specialized drafting
      conventions); standard Amharic formulaic phrases for cross-referencing articles
      in proclamations require expert elicitation from Ministry of Justice or federal
      bureau translation unit, not general web search]'
    translation_risk: Failure to maintain consistent rendering of cross-reference
      phrases undermines document coherence across numbered clauses
  terminology_authority:
    preferred: Federal bureau translators with domain training in agricultural or
      legal Amharic (e.g., Ministry of Agriculture translation unit, EABC — Ethiopian
      Agricultural Business Corporation)
    acceptable_surrogate: Amhara Regional Bureau of Agriculture staff; cooperative
      extension workers with document mediation experience
    benchmark_annotator_alignment: NONE documented — AFRIDOC-MT Amharic translators
      have no documented agricultural or legal domain expertise; preferred ground-truth
      authority is entirely absent from the benchmark annotator pool
    amharic_legal_glossary_resources: '[NOT FOUND — searched for Ministry of Agriculture,
      ATA, or regional bureau Amharic terminology glossaries for agricultural/cooperative
      proclamation vocabulary; no publicly accessible official glossary found. The
      EthioNLP survey and EthioLLM/EthioBenchmark resources cover NLP tasks (classification,
      NER, sentiment) but not legal-administrative translation terminology. This resource
      gap is itself a validity concern: no external terminology anchor exists for
      evaluating procurement-domain translation quality. Source: EthioNLP survey —
      [WEB-14]; EthioLLM paper —
      [WEB-15]]'
target_user_characteristics:
  literacy:
    general_literacy_rate_ethiopia: 'Approximately 51.8% adult literacy rate (ages
      15+) as of 2017 (UNESCO/World Bank). Most recent published figure; no post-2017
      nationally representative survey has been published as of search date. Source:
      UNESCO via TheGlobalEconomy — [WEB-16];
      World Bank WDI — [WEB-17]'
    amhara_region_literacy_rate: '[NOT FOUND — searched World Bank, UNESCO, and Ethiopian
      CSA sources; no Amhara-region-specific adult literacy rate figure is available
      in public databases. The 2017 national rate of 51.8% is a national aggregate;
      regional figures would require the Ethiopia DHS or CSA Mini-Census, which are
      not publicly disaggregated at the level required in these searches. National
      figure caveat applies: Amhara rate may differ substantially from national aggregate
      given regional variation documented for educational indicators.]'
    rural_amhara_literacy_rate: '[NOT FOUND — no rural-Amhara-specific literacy rate
      found. Urban-rural gap is documented at the national level (cities like Addis
      Ababa substantially higher than rural areas) but Amhara rural figure not found
      in public databases searched. Requires Ethiopia CSA 2007/2021 census microdata
      or DHS; flag for human follow-up.]'
    functional_literacy_notes: 'End-user population includes cooperative leaders (typically
      higher literacy within cooperative context) and rural microfinance clients (variable
      literacy, potentially low for formal proclamation-register text). Extension
      workers serve as literacy mediators for less-literate members. Benchmark does
      not assess accessibility or comprehension of translated output for variable-literacy
      readers. Note: the 2023–2025 Amhara conflict has further disrupted education
      (approximately 4 million children reportedly out of school due to the violence).
      Source: Al Jazeera 2025 — [WEB-18]'
  prior_document_exposure: Familiar with prior government communications and their
    characteristic administrative vocabulary; subject to proclamation-derived land
    and credit terminology in formal documents rather than traditional local terminology
  technology_access:
    mobile_penetration_amhara_rural: '[NEEDS VERIFICATION — deferred: below search
      budget; ITU and World Bank do not publish Amhara-specific mobile penetration
      figures; national Ethiopia figures would require separate search]'
    smartphone_vs_feature_phone_split: '[NEEDS VERIFICATION — deferred: below search
      budget; likely higher feature-phone share than urban Ethiopia, consistent with
      rural context; precise figure requires GSMA or Ethiopia Telecom data]'
    internet_connectivity_rural_amhara: '[NEEDS VERIFICATION — deferred: below search
      budget; note that the Ethiopian government routinely blocks internet across
      the Amhara region during conflict periods (documented since August 2023), materially
      affecting digital access. Source: Al Jazeera 2025 — [WEB-18]]'
    electricity_access_rural_amhara: 'Rural electrification in Amhara zones is low.
      A 2004 World Bank memorandum found only 8% of East Gojjam inhabitants had electricity
      access, and 6% in North Wollo; these figures predate subsequent rural electrification
      programs and are likely conservative lower bounds, but recent conflict has damaged
      infrastructure. Source: Wikipedia East Gojjam Zone — [WEB-11]'
    primary_access_mode: Translated documents likely received as printed paper copies
      distributed through cooperative offices or MFI branches, or as SMS/WhatsApp
      messages forwarded by extension workers — not direct AI system interaction by
      end-users
  document_interaction_mode: Cooperative leaders and extension workers receive and
    interpret translated documents on behalf of cooperative members; end-users typically
    do not interact with the translation system directly
cultural_and_institutional_norms:
  cooperative_culture: 'Agricultural cooperatives in Amhara region are a primary channel
    for government input delivery and credit access; cooperative leader decisions
    based on misunderstood translated documents affect the entire membership collectively.
    Fertilizer is formally distributed to farmers through primary cooperative unions
    per EABC distribution policy. Source: Addis Standard 2025 — [WEB-3]'
  government_document_authority: Ethiopian government proclamation documents carry
    binding legal authority; translation errors in official notices have enforceable
    legal and financial consequences, not merely informational ones
  trust_and_legitimacy: 'Rural users extend institutional trust to documents appearing
    to come from government bureaus; translation errors that alter meaning may go
    undetected if the output superficially resembles expected administrative language.
    Note: armed conflict since 2023 has documented breakdown of community trust toward
    government institutions in parts of the region. Source: BMC Nutrition 2025 — [WEB-19]'
  oral_tradition_and_document_mediation: Strong oral tradition in rural Amhara; cooperative
    leaders and extension workers typically read documents aloud and explain them
    to less-literate members — translation fluency and naturalness in spoken Amharic
    matters for this mediation function
  language_formality_expectations: End-users expect translated government documents
    to match the formal register of Amharic they associate with official communications;
    overly colloquial or health-news-register Amharic may undermine perceived document
    legitimacy
  religious_and_social_calendar: 'The Amhara region is overwhelmingly Ethiopian Orthodox
    Christian (97.42% in East Gojjam, 82.74% in North Wollo; 17.08% Muslim in North
    Wollo). The Ethiopian Orthodox calendar includes major fasting periods (Lent/Tsome
    Fillseta, Christmas/Genna, Epiphany/Timkat) and feasts that are socially dominant
    and may affect cooperative meeting schedules and document distribution timing.
    These calendar patterns are relevant to subsidy application deadlines but their
    precise seasonal impact on bureau document distribution requires stakeholder input
    rather than web search. Source: Wikipedia East Gojjam Zone — [WEB-11];
    North Wollo Zone — [WEB-20]'
infrastructure_notes:
  distribution_channel: Translated documents distributed through cooperative offices,
    MFI branch offices, woreda-level bureau offices, and extension worker networks
    — print-centric, not digital-first delivery
  translation_system_operator: System operated by federal/regional bureau translation
    staff or a deployment intermediary, not by end-users directly
  format_requirements:
    text_only_deployment: Current deployment is text-only; flowing prose is acceptable
      but structure preservation preferred where feasible
    structure_preservation_gap: AFRIDOC-MT does not evaluate preservation of numbered
      clauses, tables, or signature blocks — a partial gap if deployment evolves toward
      format-preserving or multimodal translation
    multimodal_future: '[NEEDS VERIFICATION — deferred: whether bureau documents are
      supplied as scanned PDFs requiring OCR, structured digital files, or plain text
      cannot be determined from public sources; requires direct consultation with
      Amhara Regional Bureau of Agriculture or deployment intermediary]'
  conflict_impact_on_delivery: 'Since August 2023, the armed conflict in Amhara region
    has disrupted normal cooperative service delivery, agricultural input supply chains
    (fertilizer shortages, price doubling), and humanitarian access. Parts of East
    Gojjam, North Wollo, South Wollo, North Shewa, Central Gondar and West Gojjam
    face IPC Phase 3 (Crisis) food security classification. This directly affects
    the deployment context: document distribution through cooperative offices may
    be intermittent in conflict-affected zones. Source: UK CPIN June 2025 — [WEB-4];
    OCHA Situation Report Dec 2024 — [WEB-21]'
benchmark_alignment_summary:
  benchmark: AFRIDOC-MT
  language_coverage: PRESENT — Amharic is one of five target languages, handled in
    Ethiopic script with documented accommodations for token-length constraints
  domain_coverage: ABSENT — health and IT news only; zero agricultural, land-use,
    cooperative, or credit-scheme documents
  register_coverage: ABSENT — health/IT news register vs. Ethiopian proclamation-derived
    formal administrative register; no overlap
  terminology_coverage: ABSENT — benchmark vocabulary drawn entirely from health/IT
    sources; proclamation-derived agricultural and financial terminology entirely
    unrepresented
  annotator_domain_alignment: ABSENT — no documented agricultural or legal translation
    expertise among AFRIDOC-MT Amharic translators; inter-annotator agreement for
    Amharic was 0.46 (Krippendorff's alpha)
  output_scoring_alignment: PARTIAL — d-chrF captures morphological quality broadly;
    no rubric component for terminological consistency across multi-clause documents;
    GPT-4o-as-judge explicitly unreliable for African language translation directions
  source_language_direction: MISMATCHED — benchmark translates FROM English; deployment
    translates FROM Amharic government-register documents; translationese profile
    is inapplicable
  document_structure_scoring: ABSENT — no metric evaluates preservation of numbered
    clauses, tables, or signature blocks
flagged_gaps_for_web_search:
- gap_id: 1
  description: Agricultural and regulatory domain absence from all Amharic MT benchmarks
  search_target: Amharic machine translation benchmark agricultural legal regulatory
    Ethiopian government proclamation evaluation dataset
  search_result: 'NO BENCHMARK FOUND. Searched arXiv and ACL Anthology; all existing
    Amharic MT benchmarks (Hadgu et al. 2020 evaluation set, EthioMT, AFRIDOC-MT,
    EthioLLM/EthioBenchmark) cover news, Wikipedia, social media, health, IT, and
    general-domain tasks. No benchmark covers Ethiopian government proclamation, agricultural
    subsidy, cooperative governance, or legal-administrative domains in Amharic. This
    is a confirmed documentation gap, not a thin culture. Source: EthioNLP survey
    — [WEB-14]; EthioMT — [WEB-22];
    EthioLLM — [WEB-15]; Hadgu et al. evaluation
    set — [WEB-23]'
- gap_id: 2
  description: Proclamation-register Amharic terminology resources
  search_target: Ethiopian agricultural proclamation Amharic terminology glossary
    Ministry of Agriculture ATA subsidy cooperative land tenure translation resource
  search_result: 'NO PUBLIC GLOSSARY FOUND. No Ministry of Agriculture, ATA, or regional
    bureau Amharic terminology glossary for agricultural or cooperative proclamation
    vocabulary is publicly available online. The EthioNLP ecosystem does not include
    legal-administrative or agricultural terminology resources. This is a high-impact
    gap: absence of an external terminology anchor means there is no public standard
    against which to evaluate translation quality for the deployment''s critical term
    categories.'
- gap_id: 3
  description: AFRIDOC-MT Amharic translator backgrounds and domain expertise
  search_target: AFRIDOC-MT Amharic translators Bereket Tilahun Hana Tamiru Biniam
    Asmlash Lidetewold Kebede institutional affiliation agricultural legal domain
    Ethiopia
  search_result: NOT FOUND. No public information on institutional affiliation or
    domain expertise of the four named Amharic translators (Bereket Tilahun, Hana
    M. Tamiru, Biniam Asmlash, Lidetewold Kebede) surfaced in searches. The AFRIDOC-MT
    paper itself does not document their backgrounds beyond naming them. Domain expertise
    in agricultural/legal Amharic translation cannot be confirmed or excluded.
- gap_id: 4
  description: Amhara sub-regional Amharic register and dialect features relative
    to national standard
  search_target: Amhara region Amharic dialect administrative register variation Ethiopian
    NLP sub-national bureau language
  search_result: NOT FOUND. No NLP studies on Amhara-region sub-national bureau register
    variation vs. Addis Ababa standard exist in the literature surveyed. EthioLLM
    and EthioBenchmark treat Amharic as a single variety. Requires stakeholder/expert
    elicitation from Amhara Regional Bureau translation staff.
- gap_id: 5
  description: ACSI and ADCSI operational scope and Amhara region microfinance landscape
  search_target: ACSI Amhara Credit Savings Institution loan products cooperative
    clients ADCSI Amhara region microfinance Ethiopia rural
  search_result: 'RESOLVED. ACSI confirmed as the dominant MFI in Amhara region: largest
    MFI in Ethiopia by asset size, serves ~2 million clients, operates in all woredas,
    headquartered in Bahir Dar, licensed 1997. Already used by government to disburse
    agricultural input loans. ADCSI is a distinct Addis Ababa-based institution and
    does not operate significantly in Amhara rural contexts. Sources: FinDev Gateway
    — [WEB-5];
    Springer 2023 — [WEB-24]'
- gap_id: 6
  description: Terminological consistency evaluation metrics for legal-administrative
    MT
  search_target: terminological consistency evaluation metric machine translation
    legal administrative documents African languages benchmark
  search_result: 'PARTIALLY RESOLVED. Semenov & Bojar (WMT 2022) proposed an automated
    evaluation metric for terminology consistency in MT, demonstrating scores significantly
    differ from standard automated metrics and correlate with human assessment. The
    Herfindahl-Hirshman Index (HHI) has also been applied to measure terminology consistency
    in translated legal corpora. However, neither metric has been applied to African
    languages or Amharic specifically; no African-language legal-administrative MT
    benchmark with terminology-consistency scoring exists. The JUST-NLP 2025 shared
    task addresses English-to-Hindi legal MT using BLEU, METEOR, COMET — not African
    languages. The gap (no terminology-consistency metric validated for Amharic legal-administrative
    MT) is confirmed. Sources: Semenov & Bojar 2022 — [WEB-25];
    HHI study — [WEB-26];
    JUST-NLP 2025 — [WEB-27]'
- gap_id: 7
  description: Low-literacy end-user accessibility of translated government Amharic
    documents
  search_target: Amharic plain language government document comprehension rural Ethiopia
    cooperative members literacy accessibility
  search_result: NOT SEARCHED — deferred below budget. National adult literacy rate
    (51.8% as of 2017) confirmed from World Bank/UNESCO. Amhara-specific or rural-Amhara
    figure not found. No plain-language Amharic government document comprehension
    studies found in prior searches.
- gap_id: 8
  description: Current Ethiopian federal cooperative and land proclamation operative
    terminology
  search_target: Ethiopian cooperative proclamation Amharic current federal land administration
    proclamation Amhara region holding certificate terminology
  search_result: 'PARTIALLY RESOLVED. Federal Cooperative Societies Proclamation No.
    985/2016 confirmed as current operative proclamation, establishing primary cooperative
    → union → federation → league tier structure. Federal Rural Land Administration
    and Land Use Proclamation No. 456/2005 is the primary federal land framework;
    Amhara region has its own Revised Proclamation (2006) and amendment Proclamation
    No. 252/2017. Land holding is via usufruct right with holding certificates issued
    to individuals. Specific Amharic terminology for these proclamation concepts requires
    Ministry of Justice Amharic text consultation; the Amharic title of Proclamation
    985/2016 visible in Ministry of Justice website is ''የሕብረት ሥራ ማኅበራት አዋጅ''. Sources:
    Ministry of Justice — [WEB-10];
    IGAD land profile — [WEB-12];
    ICED background paper — [WEB-13]'
net_new_fields:
  amhara_conflict_deployment_risk:
    description: 'Since April 2023, armed conflict between Ethiopian federal forces
      and Fano militias has severely disrupted the Amhara region''s agricultural and
      cooperative service delivery infrastructure. As of 2024–2025, East Gojjam, North
      Wollo, South Wollo, North Shewa, Central Gondar, and West Gojjam face IPC Phase
      3 (Crisis) food security conditions, fertilizer shortages, disrupted cooperative
      supply chains, and intermittent internet blockages. This is a material deployment-context
      validity factor: the translation system may be deployed into a context where
      cooperative offices are physically inaccessible, MFI branch operations are disrupted,
      and document distribution channels are unreliable. Assessment should account
      for the possibility that the population of document recipients, the institutional
      intermediaries (cooperative leaders, extension workers), and the physical delivery
      mechanism all face active disruption.

      Source: UK CPIN June 2025 — [WEB-4];
      OCHA Dec 2024 — [WEB-21];
      Addis Standard 2025 — [WEB-3]'
    validity_dimension_impact: IC, OC — disruption of delivery channels and institutional
      intermediaries directly affects whose document-interpretation needs the translation
      serves and whether the preferred ground-truth authority (federal bureau translators)
      can function as annotators.
  amharic_mt_benchmark_landscape:
    description: 'As of the search date, no Amharic MT benchmark covers Ethiopian
      government proclamation, agricultural subsidy, cooperative governance, or legal-administrative
      domains. Existing benchmarks include: (1) Hadgu et al. 2020 evaluation set (news,
      Wikipedia, social media, conversational); (2) EthioMT parallel corpus (English-Ethiopian
      language pairs, general domain); (3) AFRIDOC-MT (health, IT news); (4) EthioLLM/EthioBenchmark
      (classification, NER, sentiment, hate speech — not MT for legal domain). This
      confirms the coverage-gap finding in the benchmark alignment summary: the absence
      of domain-appropriate evaluation data is a known gap in the Ethiopian NLP literature,
      not merely an AFRIDOC-MT limitation.

      Source: EthioNLP survey — [WEB-14];
      EthioMT — [WEB-22]; EthioLLM — [WEB-15]'
    validity_dimension_impact: IO, IC — confirms that no competing benchmark could
      substitute for AFRIDOC-MT in evaluating this deployment; the scoring assessment
      must reflect a total absence of domain-appropriate evaluation infrastructure
      for this deployment context.
  terminology_consistency_metric_gap:
    description: 'Automated metrics for terminological consistency in MT (e.g., Semenov
      & Bojar WMT 2022; HHI-based approaches) exist for high-resource European legal
      corpora but have not been validated for Amharic or any African language. Standard
      MT metrics (chrF, BLEU, COMET) do not capture stable cross-clause rendering
      of named legal terms. This means the critical quality requirement for the deployment
      (consistent rendering of proclamation-derived terms across numbered clauses)
      has no available automated measurement instrument for Amharic.

      Source: Semenov & Bojar 2022 — [WEB-25];
      HHI study — [WEB-26]'
    validity_dimension_impact: OO — no available scoring tool addresses the OO gap
      for terminological consistency in Amharic legal-administrative translation.
  cooperative_proclamation_tier_terminology:
    description: 'Ethiopian Cooperative Societies Proclamation No. 985/2016 (Amharic:
      አዋጅ ቁጥር 985/2009 — የሕብረት ሥራ ማኅበራት አዋጅ) establishes four tiers: Primary Cooperative
      Society, Cooperative Societies Union, Cooperative Societies Federation, and
      Cooperative Societies League. A Cooperative Societies Union is formed by two
      or more primary cooperative societies with similar objectives. Registration
      is by the Federal Cooperative Agency or regional organs. This proclamation supersedes
      Proclamation 147/1998. The Amharic terminology for these tiers, as used in official
      proclamation text, is the operative standard for evaluating translation of cooperative
      governance documents.

      Source: Ministry of Justice official text — [WEB-10];
      UNEP LEAP — [WEB-8];
      EthioData — [WEB-9]'
    validity_dimension_impact: IC, OC — provides the authoritative terminology standard
      for the cooperative membership tier category, enabling ground-truth evaluation
      of translation accuracy for this term category.
  acsi_role_in_input_subsidy_distribution:
    description: 'ACSI is already used by the Ethiopian government to disburse agricultural
      input loans to farmers in Amhara region, making it a dual-role institution:
      both MFI lender and government input-subsidy distribution channel. This means
      ACSI-issued documents may combine MFI credit-scheme terms with agricultural
      input subsidy scheme terminology in a single document — a genre hybrid not anticipated
      by the benchmark design. Source: FinDev Gateway 2008 sector assessment — [WEB-7]'
    validity_dimension_impact: IO, IC — the genre hybrid (MFI + subsidy) is not represented
      in AFRIDOC-MT's strict health/IT news categories; reinforces the full domain-coverage
      gap finding.
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.researchgate.net/figure/Administrative-Zones-within-Amhara-Region_fig1_247830953 |
| WEB-2 | https://www.longdom.org/open-access-pdfs/determinants-of-adoption-of-wheat-row-planting-the-case-of-wogera-district-north-gondar-zone-amhara-regional-state-ethiopia.pdf |
| WEB-3 | https://addisstandard.com/sowing-under-shadows-of-violence-amhara-farmers-face-bleak-harvest-as-conflict-deepens-fertilizer-shortages-drives-up-input-prices/ |
| WEB-4 | https://www.gov.uk/government/publications/ethiopia-country-policy-and-information-notes/country-policy-and-information-note-amhara-and-amhara-opposition-groups-ethiopia-june-2025-accessible |
| WEB-5 | https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-case-study-a-review-of-ethiopian-microfinance-institutions-and-their-role-in-poverty-reduction-a-case-study-on-amhara-credit-and-saving-institution-acsi-jan-2011.pdf |
| WEB-6 | https://www.mftransparency.org/microfinance-pricing/ethiopia/002-ACSI/ |
| WEB-7 | https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-paper-subsidizing-microcredit-interest-how-important-is-it-to-the-poor-0-2004.pdf |
| WEB-8 | https://leap.unep.org/en/countries/et/national-legislation/cooperative-societies-proclamation-no-9852016 |
| WEB-9 | https://ethiodata.et/ethiopia-cooperative-societies-proclamation-no-985-2016/ |
| WEB-10 | https://justice.gov.et/en/law/cooperative-societies-proclamation-2/ |
| WEB-11 | https://en.wikipedia.org/wiki/East_Gojjam_Zone |
| WEB-12 | https://land.igad.int/index.php/countries/37-countries/ethiopia/38-ethiopia-profile?start=2 |
| WEB-13 | https://ukgreencitiesandinfrastructure.org/wp-content/uploads/2019/07/ICED-Ethiopia-land-administration-background-paper.pdf |
| WEB-14 | https://github.com/EthioNLP/Ethiopian-Language-Survey |
| WEB-15 | https://aclanthology.org/2024.lrec-main.561.pdf |
| WEB-16 | https://www.theglobaleconomy.com/Ethiopia/Literacy_rate/ |
| WEB-17 | https://data.worldbank.org/indicator/SE.ADT.LITR.ZS?locations=ET |
| WEB-18 | https://www.aljazeera.com/features/2025/3/10/we-just-want-peace-a-pacifist-community-amid-ethiopias-amhara-conflict |
| WEB-19 | https://bmcnutr.biomedcentral.com/articles/10.1186/s40795-025-01013-5 |
| WEB-20 | https://en.wikipedia.org/wiki/North_Wollo_Zone |
| WEB-21 | https://www.unocha.org/publications/report/ethiopia/ethiopia-situation-report-13-december-2024 |
| WEB-22 | https://arxiv.org/html/2403.19365v1 |
| WEB-23 | https://zenodo.org/records/3734260 |
| WEB-24 | https://link.springer.com/article/10.1007/s43621-023-00161-7 |
| WEB-25 | https://aclanthology.org/2022.wmt-1.41/ |
| WEB-26 | https://www.researchgate.net/publication/358368108_Measuring_Terminology_Consistency_in_Translated_Corpora_Implementation_of_the_Herfindahl-Hirshman_Index |
| WEB-27 | https://aclanthology.org/2025.justnlp-main.3.pdf |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark covers health and IT news documents. Your deployment targets agricultural input subsidy notices, land-use policy updates, and credit-scheme terms — genres with distinctive bureaucratic phrasing, legal terminology, and numbered clause structures. Are there document types in your deployment that combine legal/regulatory language with agricultural or financial jargon in ways that differ substantially from health or tech reporting? For example, do your documents include itemized eligibility conditions, penalty clauses, or seasonal deadlines that require consistent terminology across long stretches of text?
A1: The user acknowledges the domain gap (health/IT vs. agriculture/finance/policy) but believes document-level structural demands are broadly similar across genres. The main concern is that certain agricultural domain-specific terminologies will not be represented in the benchmark's training or evaluation data, even if discourse-coherence requirements are comparable.

Q2 [IC]: Government and lender documents in Amhara often carry culturally specific concepts — such as cooperative membership tiers, traditional land-tenure categories (e.g., rist), or regionally named subsidy schemes. Would your target documents contain terminology like these that requires locally grounded Amharic equivalents rather than direct transliterations or generic terms?
A2: The user agrees that culturally specific concepts exist, but notes that in contemporary Ethiopian agricultural and land-tenure contexts, formal documents draw primarily from federal and regional proclamation-derived terminology rather than traditional local terms. The operative vocabulary is thus legally standardized, though it may still be unfamiliar to rural end-users.

Q3 [OC]: For your deployment, who should be the authority on whether an Amharic translation of a subsidy notice or loan agreement is correct and trustworthy?
A3: The user identifies domain-trained federal bureau translators as the preferred ground-truth authority. In their absence, regional bureau staff and cooperative extension workers are acceptable surrogates. The answer implies a professional-administrative annotator standard rather than end-user farmer judgment, though usability by cooperative leaders remains an implicit requirement.

Q4 [OF]: Do target users need translated output that preserves the original document structure (numbered clauses, tables, signature blocks), or is flowing prose acceptable?
A4: Format requirements are contingent on model modality: multimodal models should preserve tables and document layout; text-only models may produce flowing prose. Structural fidelity is preferred where technically feasible but is not an absolute requirement when the model is text-only.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark's domain coverage (health, IT news) does not include agricultural policy, land-use regulation, or credit-scheme documents, meaning the benchmark's test-case category distribution is systematically misaligned with the deployment's document genres, even if discourse-structural demands are comparable. |
| IC | HIGH | Agricultural proclamation-derived terminology, subsidy scheme names, credit-condition phrasing, and land-tenure vocabulary are absent from health/IT benchmark instances; these specialized terms are the exact content where translation errors have binding legal and financial consequences for end-users. |
| IF | LOWER | Both the benchmark and the deployment are text-only; the target language (Amharic) is present in the benchmark and uses Ethiopic script, which the benchmark explicitly covers; no modality mismatch is introduced. |
| OO | MODERATE | The benchmark's output evaluation is designed around document-level coherence and translation adequacy in health and IT contexts; scoring rubrics may not capture domain-specific terminological consistency (e.g., stable rendering of proclamation terms across clauses), which is the critical coherence requirement for legal-administrative documents. |
| OC | HIGH | The benchmark was designed for health and IT domains with its own annotator pool; ground-truth labels for agricultural/financial Amharic translation would ideally come from federal bureau translators or domain-trained regional staff — a population that almost certainly differs from the benchmark's annotators, risking label mismatch on domain-specific correctness judgments. |
| OF | MODERATE | The benchmark evaluates document-level text translation, which broadly matches the text-only deployment scenario; however, the deployment's preference for structure preservation (tables, numbered clauses) when feasible is not assessed by a text-only benchmark, leaving a partial gap for multimodal or format-sensitive use cases. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** masakhane/AfriDocMT
**Analysis date:** 2025-07-11
**Examples reviewed:** 61 total (doc_health: 5, doc_health_10: 5, doc_health_25: 5, doc_health_5: 5, doc_tech: 5, doc_tech_10: 5, doc_tech_25: 5, doc_tech_5: 5, health: 5, tech: 6)
**Columns shown:** am, en, ha, sw, yo, zu
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | doc_health, train | 1 | health/WHO | "ሞቃታማ አውሎ ነፋሶችን እንዲሁም ሀይለኛ አውሎ ነፋስ ወይም አውሎ ነፋሶች በመባል የሚታወቁት በጣም አጥፊ የአየር ሁኔታ ክስተቶች ናቸው" | Amharic translation of WHO health content on tropical cyclones — health domain, Ethiopic script | IC, IF |
| D2 | doc_health, train | 2 | health/WHO | "አካል ጉዳተኝነት ሰው የመሆን አካል ነው" | Amharic translation: "Disability is part of being human" — WHO health article | IC |
| D3 | doc_health, train | 3 | health/WHO | "በ 6 ወር አካባቢ የሕፃኑ የኃይል ፍላጎት እና የተመጣጠነ ምግብ አቅርቦት በእናት ጡት ወተት ከሚሰጠው በላይ መጨመር የሚጀምር" | Amharic: infant complementary feeding guidance from WHO — health domain | IC |
| D4 | doc_health, train | 4 | health/WHO | "ፀረ-ተሕዋስያንን መቋቋም(AMR) የሚከሰተው ባክቴሪያ፣ ቫይረሶች፣ ፈንገሶች እና ጥገኛ ተህዋሲያን" | Amharic: antimicrobial resistance — health domain, WHO | IC |
| D5 | doc_health_10, train | 1 | health/WHO | "ይህ የሚያሳየው የደብሊውፒቪ1 ስርጭት ከአፍጋኒስታን (ምስራቅ ክልል) እና ፓኪስታን (ደቡብ ኬፒ) ዞኖች" | Amharic: polio surveillance language, mentions sub-national zones and infection control measures | IC, OO |
| D6 | doc_health_10, train | 3 | health/WHO | "ፋይናንስ ማካተት አሁናዊ ሁኔታዎችን ከሚያስፈልጉ ሰዎች ጋር ፍቃደኛ ከሆኑ" [Financial protection discussion] | Amharic: financial protection policy discourse — health financing domain | IC |
| D7 | doc_tech, train | 1 | tech/Techpoint | "ፔይ ደይ ለመሸጥ ይፈልጋል...ናይጄሪያ ፕሬዚዳንት አዲስ CBN ገዥን ሾሙ" | Amharic: African technology news digest — IT/fintech domain, no agricultural or legal content | IO |
| D8 | doc_tech, train | 2 | tech/Techpoint | "ደቡብ አፍሪካ ጎጂ ይዘቶችን በመስመር ላይ ማቆም ትፈልጋለች...ናላ ከ ዩኬ እና የአውሮፓ ህብረት ለናይጄሪያ ክፍያዎችን ይጀምራል" | Amharic: African fintech and content moderation news | IO |
| D9 | doc_tech, train | 3 | tech/Techpoint | "ኔስት ኮይን (Nestcoin) የሂሳብ መዛግብቱን ለማጠናከር እና የአዲሱን ምርት በኦንቦርድ እድገት" | Amharic: crypto/Web3 fintech startup news | IO |
| D10 | doc_tech, train | 4 | tech/Techpoint | "ኤርቴል ኡጋንዳ ለጃማይካዊው ዘፋኝ 180ሺህ ዶላር ለመክፈል...ቲክቶክ በኬንያ ቢሮ ለመክፈት" | Amharic: telecom copyright law and African tech platform expansion news | IO |
| D11 | health, train | 1 | health/WHO-sentence | "OCV wata hanya ce da ake amfani da ita a ƙari a kan hanyar kula da kwalara" | Hausa sentence-level: oral cholera vaccine health terminology | IC |
| D12 | health, train | 2 | health/WHO-sentence | "ሆኖም የጤና ስርአቶች በዋነኛነት በህዝብ የገቢ ምንጮች ላይ መተማመን ያለባቸው" | Amharic sentence: "health systems need to predominantly rely on public revenue sources" | IC |
| D13 | tech, train | 1 | tech/sentence | "Sahel Capital's SEFAA (Social Enterprise Fund for Agriculture in Africa) Fund" | Tech sentence: agriculture-sector investment fund — only agricultural adjacent content in dataset | IO |
| D14 | tech, train | 6 | tech/sentence | "ፍርድ ቤቱን ጠይቋል" / "He also asked the court to order the telco to pay him royalties" | Amharic sentence: legal/court language in tech context — royalties claim against Safaricom | IO |
| D15 | doc_health_25, train | 2 | health/WHO | "WHA evaluated the unique epidemiological opportunity which exists over the next six months to eradicate the remaining chains of endemic wild poliovirus" | Complex administrative/WHO governance language; multi-sentence Amharic document | OO |
| D16 | doc_health_25, train | 4 | health/WHO | "ገቢ የሆነ የህፃናት አመጋገብ ከልደት ጀምሮ እስከ አዋቂነት ድረስ ለልጁ ዘላቂ ጤና መሰረታዊ ነው" | Amharic: infant nutrition health domain, WHO; long document with cross-sentence references | IC, OO |
| D17 | doc_health_25, train | 5 | health/WHO | "አይኤችአር 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ በ196 አገሮች ላይ በሕግ አስገዳጅ የሆነ የዓለም አቀፍ ሕግ መሣሪያ ነው" | Amharic: International Health Regulations — legally-binding international law framework; closest genre to legal-administrative register in the dataset | IO, OO |
| D18 | doc_health_5, train | 1 | health/WHO | "ከ ቲአርአይፒኤስ ስምምነት ከፀደቀበት ጊዜ አንሥቶ የዓለም የጤና ስብሰባዎች ብዙ ውሳኔዎች" | Amharic: TRIPS agreement, intellectual property law in health sector — international health-law language | IO |
| D19 | doc_tech_25, train | 1 | tech/Techpoint | "ቬንቸር ካፒታሊስቶች(Venture capitalists) የ ኩባንያዎችን ማንነት የሚያገኙት" | Amharic: startup/entrepreneurship discourse — tech sector, no agricultural or cooperative content | IO |
| D20 | doc_tech_10, train | 1 | tech/Techpoint | "The edtech industry in India has exploded in the last few years, making it the world's epicentre." | English: edtech industry news — IT domain, no agricultural domain | IO |
| D21 | health, train | 4 | health/WHO-sentence | "Measures for the prevention of cholera mostly consist of providing clean water and proper sanitation" | English: public health measure description — WHO public health register | IC |
| D22 | doc_health, train | 1 | health/WHO | "ጊዜያዊ የስራ መደብ ወረቀት፡ ለአለም አቀፍ ተጓዦች የኮቪድ-19 ክትባት ማረጋገጫን" | Amharic: interim WHO policy paper — policy document register | OO |
| D23 | doc_health_10, train | 4 | health/WHO | "የጤና ባለሥልጣናት የትንኝ ብዛትን እና የበሽታውን ስርጭት ለመቀነስ ላርቪሳይድ" | Amharic: Zika vector control guidance — specific technical health terminology | IC |
| D24 | doc_health_10, train | 5 | health/WHO | "የጤና አካውንት ሥርዓት 2011 (ጤ/አ/ስ 2011) የጤና ወጪን ለመከታተል" | Amharic: System of Health Accounts — health financing framework document | OO |
| D25 | doc_tech_5, train | 1 | tech/Techpoint | "Remittances are typically transfers between individuals...immigrants send home to support their families" | English: diaspora remittances — fintech/financial inclusion domain | IO |
| D26 | doc_health_25, train | 3 | health/WHO | "እሳተ ገሞራ ፍንዳታዎች አጠቃላይ እይታ፦ እሳተ ገሞራ በምድር ቅርፊት ውስጥ የሚገኝ ክፍተት" | Amharic: volcanic eruptions health risk — WHO emergency preparedness | IC |
| D27 | doc_tech, train | 5 | tech/Techpoint | "ፕሮዳክት ዳይቭ እንዴት ነው የተጀመረው...ወደ ምርት አስተዳደር ጉዞ" | Amharic: long-form interview with tech entrepreneur — informal, personal narrative register | IF |
| D28 | tech, train | 3 | tech/sentence | "In dissecting the social impacts, it becomes vital to delve deep into real-life cases that embody both the positive and negative facets of sports betting in Kenya." | English: sports betting social impacts — not directly relevant to deployment context | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Amharic in Ethiopic Script with Multi-Sentence Document Structure
- **Dimension(s):** IF, IC
- **Observation:** All sampled Amharic content is rendered in Ethiopic (Ge'ez) script throughout all configurations, including full-document (doc_health, doc_tech), pseudo-document (10/25/5-sentence chunks), and sentence-level splits. Amharic script rendering is consistent and coherent across documents of varying length. The benchmark explicitly accommodates Ethiopic script tokenization by increasing token limits for Amharic.
- **Deployment relevance:** The deployment system must handle Amharic in Ethiopic script. The benchmark's demonstrated ability to process, segment, and evaluate multi-sentence Amharic documents in Ethiopic script confirms that the language/script dimension is technically addressed. This directly matches the target output modality.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "የሞቃታማ ዐውሎ ነፋሶች የሞቃታማ ዐውሎ ነፋሶች አጠቃላይ እይታ፡-" — Extended Ethiopic-script Amharic document covering multiple paragraphs; confirms multi-sentence Ethiopic document handling at the doc level.
  - [D3] Example 3 (doc_health, split=train): "ተጨማሪ ምግብ ማጠቃሊያ፡- በ 6 ወር አካባቢ..." — Mid-length WHO health article in Amharic, correctly segmented into numbered recommendations with discourse coherence preserved.

#### Strength 2: Multi-Sentence Discourse Phenomena in Amharic Are Present
- **Dimension(s):** IO, OO
- **Observation:** Several sampled Amharic documents contain multi-clause cross-sentence references, numbered recommendations, and conditional structures (e.g., "ካልተሰጡ ወይም ተገቢ ባልሆነ መንገድ ከተሰጡ" — "if not given or given inappropriately"), which mirror the benchmark's explicit aim to capture coreference resolution and lexical cohesion across sentences.
- **Deployment relevance:** The user acknowledged that document-level structural demands are broadly similar across genres. The benchmark captures cross-sentence dependency structures in Amharic, which the deployment will also need MT systems to handle when translating multi-clause legal and agricultural documents.
- **Datapoint citations:**
  - [D16] Example 4 (doc_health_25, split=train): "ምንም እንኳን በህፃናት መብቶች ስምነቱ መሰረት እያንዳንዱ ጨቅላ እና ህጻን ጥሩ አመጋገብ የማግኘት መብት ቢኖረውም" — Cross-clause conditional referencing: "although every infant… has the right… in many countries less than a fourth…"; demonstrates multi-sentence Amharic coherence across a qualifying clause.
  - [D15] Example 2 (doc_health_25, split=train): "WHA ሕዝቡ ጤና ድንገተኛ አደጋ አለም አቀፍ ስጋት… ሀገራት… አሳስበዋል" — Multi-clause WHO governance language in Amharic preserving cross-sentence referential structure.

#### Strength 3: Multiple Evaluation Configurations Including Document- and Sentence-Level Splits
- **Dimension(s):** IO, OF
- **Observation:** The HF dataset provides ten distinct configurations — sentence-level (health, tech), full-document (doc_health, doc_tech), and pseudo-document chunks (k=5, k=10, k=25) for both domains. All configurations include Amharic. This allows evaluation of MT systems at sentence and sub-document granularities that approximate the chunk sizes relevant for processing bureau documents.
- **Deployment relevance:** Bureau documents in the deployment context may range from short notices to multi-page proclamations. The availability of sentence-level and pseudo-document splits (k=5 through full document) enables evaluation across a range of document lengths comparable to those in the deployment.
- **Datapoint citations:**
  - [D11] Example 1 (health, split=train): "OCV wata hanya ce da ake amfani da ita a ƙari" — Short single-sentence health item; confirms that sentence-level granularity is included for all languages including Amharic.
  - [D5] Example 1 (doc_health_10, split=train): "ይህ የሚያሳየው የደብሊውፒቪ1 ስርጭት ከአፍጋኒስታን (ምስራቅ ክልል)..." — 10-sentence pseudo-document chunk in Amharic; demonstrates the k=10 chunking configuration relevant for medium-length document evaluation.

#### Strength 4: Health Domain Includes Some Policy and Regulatory-Adjacent Register
- **Dimension(s):** IC, OO
- **Observation:** A subset of the WHO health content uses formal policy register features: numbered recommendations ("1. …2. …"), cross-references to proclamation-like frameworks (IHR, TRIPS), and governance vocabulary. The International Health Regulations document (D17) explicitly describes a legally-binding international law instrument with numbered state obligations.
- **Deployment relevance:** This is the closest approximation in the benchmark to the formal administrative register of Ethiopian proclamation documents. While the domain mismatch is severe, the presence of multi-clause numbered obligations, legal vocabulary, and policy cross-references in Amharic provides at least a partial analog to the discourse structure of the deployment genre.
- **Datapoint citations:**
  - [D17] Example 5 (doc_health_25, split=train): "አይኤችአር 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ በ196 አገሮች ላይ በሕግ አስገዳጅ የሆነ የዓለም አቀፍ ሕግ መሣሪያ ነው" — "IHR is an instrument of international law that is legally-binding on 196 countries"; formal legal-regulatory register in Amharic with numbered obligations.
  - [D18] Example 1 (doc_health_5, split=train): "ከ ቲአርአይፒኤስ ስምምነት ከፀደቀበት ጊዜ አንሥቶ የዓለም የጤና ስብሰባዎች ብዙ ውሳኔዎች" — TRIPS Agreement reference; international IP law cross-referenced in health-policy Amharic document.

#### Strength 5: Human-Translated Amharic by Named Native-Speaker Translators
- **Dimension(s):** OC
- **Observation:** The benchmark's four named Amharic translators (Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, Lidetewold Kebede) produced translations under a controlled workflow with quality estimation filtering and terminology workshop preparation. The translation process included human review by a native-speaker language coordinator.
- **Deployment relevance:** The target deployment requires high-quality Amharic translations assessable by native speakers. Benchmark reference translations were produced by human translators (not MT), providing a legitimate upper-bound Amharic quality signal in the health domain, even if domain-mismatched for agriculture/legal.
- **Datapoint citations:**
  - [D2] Example 2 (doc_health, split=train): "አካል ጉዳተኝነት ሰው የመሆን አካል ነው" — "Disability is part of being human"; fluent, naturalistically rendered Amharic sentence consistent with human translation quality.
  - [D4] Example 4 (doc_health, split=train): "ፀረ-ተሕዋስያንን መቋቋም(AMR) የሚከሰተው ባክቴሪያ፣ ቫይረሶች፣ ፈንገሶች" — Technical medical terminology rendered with consistent Amharic neologisms across the document (e.g., "ፀረ-ባክቴሪያ" for antibiotic), demonstrating terminological consistency within the health domain.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Total Domain Absence — No Agricultural, Land-Use, Credit-Scheme, or Cooperative Governance Content
- **Dimension(s):** IO, IC
- **Observation:** All 61 sampled examples draw exclusively from two domains: WHO health news and Techpoint Africa IT news. Not a single example contains agricultural input subsidy notices, land-tenure policy language, credit-scheme terms, cooperative membership governance language, or federal proclamation text. The dataset's vocabulary is drawn entirely from these two domains. In the entire sample, the only "agricultural" item is a single sentence naming a fund with "Agriculture in Africa" in its title (D13), which is a fintech story about an agricultural investment fund — not agricultural document content.
- **Deployment relevance:** The deployment's four target document genres (agricultural input subsidy notices, land-use policy updates, credit-scheme terms, cooperative membership notices) are completely unrepresented. This is not a partial gap — it is a total absence confirmed across all sampled configurations. The benchmark cannot be used as a direct domain-validity test for the deployment. Any performance score on AFRIDOC-MT will not predict MT quality on the deployment's actual document types.
- **Datapoint citations:**
  - [D7] Example 1 (doc_tech, split=train): "ፔይ ደይ ለመሸጥ ይፈልጋል...ናይጄሪያ ፕሬዚዳንት አዲስ CBN ገዥን ሾሙ" — Technology news bulletin: PayDay startup, CBN governor appointment — no agricultural content whatsoever.
  - [D8] Example 2 (doc_tech, split=train): "ናላ ከ ዩኬ እና የአውሮፓ ህብረት ለናይጄሪያ ክፍያዎችን ይጀምራል... ሴሉላንት 20% የሚሆነውን የሰው ኃይል ለማሰናበት" — Fintech remittances and tech layoffs news — no cooperative, land, or subsidy content.
  - [D13] Example 1 (tech, split=train): "Sahel Capital's SEFAA (Social Enterprise Fund for Agriculture in Africa) Fund" — The only "agriculture" mention in the entire sample is the name of an investment fund in a tech news story, not agricultural document content.
  - [D25] Example 1 (doc_tech_5, split=train): "Remittances are typically transfers between individuals…immigrants send home to support their families" — Closest fintech-adjacent item to rural microfinance, but purely in context of diaspora remittances, not ACSI loan agreements or cooperative credit schemes.

#### CRITICAL Concern 2: Source Language Direction Mismatch — Benchmark Translates FROM English; Deployment Translates FROM Amharic
- **Dimension(s):** IC, OC
- **Observation:** Every example in the dataset has an English source document and Amharic as the target translation. The benchmark evaluates English→Amharic MT. The deployment translates FROM Amharic government documents INTO a target language (presumably also Amharic, or possibly from Amharic source texts where the output needs to be evaluated in Amharic). More precisely: the deployment produces Amharic translations of documents that originate in Amharic government-register language — effectively evaluating MT quality in a very different structural direction. Even if the deployment were English→Amharic, the benchmark's English sources (WHO health news, Techpoint Africa IT news) are structurally and lexically distant from Ethiopian federal bureau documents.
- **Deployment relevance:** The benchmark's reference Amharic translations exhibit translationese — unnatural syntax and structural patterns influenced by English source texts. Deployment Amharic documents originate in Amharic proclamation register and have no such English structural bias. A model that performs well on AFRIDOC-MT (English health news → Amharic) may not perform well on the deployment's actual source texts.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "Tropical cyclones, also known as typhoons or hurricanes, are among the most destructive weather phenomena. They are intense circular storms that originate over warm tropical oceans..." — The English source is WHO public health news; the Amharic translation follows English syntactic ordering. Ethiopian proclamation documents are natively authored in Amharic with a distinct formal register.
  - [D17] Example 5 (doc_health_25, split=train): "አይኤችአር 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ በ196 አገሮች ላይ" — IHR article translated from English; even the closest regulatory-register content is a translation FROM English, not native Amharic administrative writing.

#### CRITICAL Concern 3: Complete Absence of Proclamation-Derived Agricultural and Financial Terminology
- **Dimension(s):** IC, OC
- **Observation:** The benchmark contains zero instances of the critical term categories identified by the user: input subsidy scheme names, land-tenure category labels (rist-derived terms, usufruct rights, holding certificates), cooperative membership tier designations from Proclamation 985/2016 (ቀዳሚ የሕብረት ሥራ ማኅበር, የሕብረት ሥራ ማህበራት ዩኒዮን), or MFI credit-scheme terms (ACSI group lending terminology). The Amharic vocabulary in the dataset is drawn from health (disease names, medical procedures, nutrition, epidemiology) and IT (startup names, fintech terms, crypto vocabulary) — entirely non-overlapping with the deployment's operative terminology.
- **Deployment relevance:** For the deployment, translation errors on specific legal terms (e.g., misrendering "ቀዳሚ ሕብረት ሥራ ማኅበር" vs. "ሕብረት ሥራ ማህበር ዩኒዮን") have direct legal and financial consequences for cooperative leaders. The benchmark provides no mechanism to evaluate whether an MT system correctly and consistently renders these terms, since they never appear in the data.
- **Datapoint citations:**
  - [D9] Example 3 (doc_tech, split=train): "ኔስት ኮይን (Nestcoin) የሂሳብ መዛግብቱን ለማጠናከር...ሃሺድ ኢመርጀንት" — Crypto/fintech vocabulary (stablecoin, FTX, pre-seed funding) — zero overlap with cooperative proclamation vocabulary or agricultural subsidy terminology.
  - [D4] Example 4 (doc_health, split=train): "ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ፣ ፀረ-ፈንገስ እና ፀረ-ተባይ መድሃኒቶች" — Medical antimicrobial terminology; no connection to land-tenure or cooperative tier vocabulary.
  - [D11] Example 1 (health, split=train): "OCV wata hanya ce da ake amfani da ita a ƙari a kan hanyar kula da kwalara" — Oral cholera vaccine terminology in Hausa; illustrates the exclusively health-domain vocabulary present at sentence level.

#### MAJOR

#### MAJOR Concern 1: No Rubric Component for Terminological Consistency — The Critical Coherence Requirement for Deployment
- **Dimension(s):** OO
- **Observation:** The benchmark's output scoring framework evaluates fluency (GPT-4o 1-5 scale), content errors (CE), lexical cohesion errors (LE), and grammatical cohesion errors (GE). The lexical cohesion error definition ("issues with vocabulary usage, incorrect or missing synonyms, or overuse of certain words that disrupt the flow") addresses narrative discourse flow, not legal terminological consistency. No rubric component tests whether a specific legal term (e.g., a subsidy scheme name or cooperative tier designation) is rendered identically across all clauses of a document. The data examples confirm this: WHO documents are evaluated for narrative coherence, not for whether "Oral Cholera Vaccine" is always rendered the same way throughout.
- **Deployment relevance:** For the deployment, the key quality requirement is not narrative fluency but terminological stability — that "ቀዳሚ የሕብረት ሥራ ማኅበር" is always rendered identically across 50 clauses of a proclamation. This property is not measured by any metric in AFRIDOC-MT. Even if the deployment were adapted to use AFRIDOC-MT scoring, the scores would not capture the critical coherence dimension.
- **Datapoint citations:**
  - [D16] Example 4 (doc_health_25, split=train): "Ó dara jùlọ... abẹ́rẹ́ àjẹsára... ọmọ ọwọ́" — WHO nutrition document evaluated for fluency and cohesion in Yorùbá; assessment concerns narrative flow of infant feeding guidance, not consistent rendering of defined legal categories.
  - [D22] Example 1 (doc_health_5, split=train): "ጊዜያዊ የስራ መደብ ወረቀት፡ ለአለም አቀፍ ተጓዦች የኮቪድ-19 ክትባት ማረጋገጫን" — Interim WHO position paper; the document mentions specific policy concepts (PHEIC, IHR), but the scoring rubric would assess fluency, not consistent cross-document rendering of "PHEIC" as a defined term.

#### MAJOR Concern 2: Annotator Domain Expertise Absent for Agricultural/Legal Amharic
- **Dimension(s):** OC
- **Observation:** The four named Amharic translators produced reference translations for WHO health news and Techpoint Africa IT news. There is no documentation of their institutional affiliation, agricultural translation experience, or legal Amharic background. The preferred ground-truth authority specified by the user (domain-trained federal bureau translators) is entirely absent. The inter-annotator agreement for Amharic (Krippendorff's alpha = 0.46) is already low for the health domain in which the translators were specifically prepared; performance would likely be lower still in the agricultural-legal domain.
- **Deployment relevance:** Any quality judgment derived from AFRIDOC-MT Amharic reference translations — whether for training, evaluation, or benchmarking — reflects the judgments of translators working in health/IT contexts, not the federal bureau translation standard the user specified. Ground-truth misalignment means that high benchmark scores do not predict acceptability to the user's preferred evaluators.
- **Datapoint citations:**
  - [D3] Example 3 (doc_health, split=train): "ተጨማሪ ምግቦቹ በ 6 ወር ጊዜ ውስጥ ካልተሰጡ ወይም ተገቢ ባልሆነ መንገድ ከተሰጡ" — Amharic health translation requiring WHO pediatric nutrition domain expertise; translator preparation was appropriate for this domain but not for agricultural proclamation register.
  - [D5] Example 1 (doc_health_10, split=train): "የቅርብ ጊዜውን እድገት መቀልበስ ነው. መርሃግብሩ ከፍተኛ ጥራት ያላቸውን ዘመቻዎች" — Polio surveillance Amharic document; complex public health vocabulary produced by health-domain translators, not agricultural domain translators.

#### MAJOR Concern 3: Translationese Risk Compounds Domain Gap — Benchmark Amharic Does Not Reflect Native Administrative Register
- **Dimension(s):** IC
- **Observation:** The benchmark explicitly acknowledges that all Amharic reference translations may exhibit "unnatural syntax or overly literal phrasing" due to English source material. The sampled data confirms this: sentences follow English subordination patterns and clause ordering. Amharic federal proclamation documents use a distinct formal register with specific formulaic phrase structures (cross-article reference formulas, numbered subclause templates) that are natively authored in Amharic and absent from any translated text in the benchmark.
- **Deployment relevance:** MT systems fine-tuned or benchmarked on AFRIDOC-MT Amharic may learn English-influenced Amharic sentence structures. These structures may be legible but could fail to match the formal register expectations of rural cooperative leaders and bureau staff, who associate official documents with specific Amharic administrative phrasing.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "ሞቃታማ አውሎ ነፋሶች፣ እንዲሁም ሀይለኛ አውሎ ነፋስ ወይም አውሎ ነፋሶች በመባል የሚታወቁት" — The Amharic renders "also known as typhoons or hurricanes" as a relative clause; this is a structurally English-influenced subordination pattern. Native Amharic administrative documents would likely employ a different grammatical structure.
  - [D27] Example 5 (doc_tech, split=train): "ቶቢ ከ ቴክ ፖይንት አፍሪካ ጋር ያደረጉት ቃለ ምልልስ" — Interview-register Amharic (tech domain): informal, conversational sentence structures that differ markedly from proclamation-register Amharic. Illustrates that even within the dataset, register variation exists that does not approach legal-administrative Amharic.

#### MINOR

#### MINOR Concern 1: Technology Domain Contains Some Legally Adjacent Content but Not Applicable to Deployment
- **Dimension(s):** IO
- **Observation:** Several tech domain documents contain legal or quasi-legal language: copyright infringement claims (D14), telecom regulatory decisions, and securities/investment disclosures. However, this legal language concerns corporate IP law, telecommunications regulation, and fintech compliance — entirely different from Ethiopian agricultural proclamation law, cooperative registration, and land-tenure regulation.
- **Deployment relevance:** These items might superficially appear to close the legal-register gap, but the specific legal vocabulary (royalties, capital markets, exchange rate unification) has no relevance to cooperative proclamations or subsidy scheme terms. The domain-register mismatch persists.
- **Datapoint citations:**
  - [D14] Example 6 (tech, split=train): "ፍርድ ቤቱን ጠይቋል" / "He also asked the court to order the telco to pay him royalties and licensing fees" — Amharic legal vocabulary in a copyright/IP context; not applicable to cooperative membership or land-tenure law.
  - [D10] Example 4 (doc_tech, split=train): "ኤርቴል ኡጋንዳ ለጃማይካዊው ዘፋኝ 180ሺህ ዶላር ለመክፈል... ፍርድ ቤቱ ተከሳሾቹን በቅጂ መብት ጥሰት" — Copyright infringement court ruling in Uganda; Amharic legal vocabulary but in IP/copyright register, not agricultural proclamation register.

#### MINOR Concern 2: Sports Betting and Some Tech Content Irrelevant to Any Deployment Need
- **Dimension(s):** IO
- **Observation:** Two examples in the tech dataset concern sports betting social impacts in Kenya (D28) and extended personal interviews about tech entrepreneurship. These are not only irrelevant to the agricultural deployment but represent the least formal, most conversational Amharic register in the dataset.
- **Deployment relevance:** Minor — these items do not affect the overall domain analysis, but they do further dilute the relevance of the tech domain for any purpose related to the deployment.
- **Datapoint citations:**
  - [D28] Example 3 (tech, split=train): "In dissecting the social impacts, it becomes vital to delve deep into real-life cases that embody both the positive and negative facets of sports betting in Kenya." — Sports betting commentary; no deployment relevance.
  - [D27] Example 5 (doc_tech, split=train): "ቶቢ...ስለ አስተዳደሯ፣ ስለ እምነቷ፣ የምርት ሥራ አስኪያጅ ለመሆን ስላላት መንገድ" — Extended personal interview on tech entrepreneurship; informal, narrative register; no deployment relevance.

---

### Content Coverage Summary

The dataset contains exclusively two content domains confirmed by direct examination: (1) WHO global health news covering topics including tropical cyclones, disability, antimicrobial resistance, complementary feeding, cholera, polio vaccination, COVID-19 policy, and International Health Regulations; and (2) African technology news from Techpoint Africa covering fintech startups, crypto/Web3, African tech ecosystem, mobile money, edtech, and agritech investment (but not agritech content — only investment news about agritech companies).

The Amharic translations are extensive, fluent, and technically handled in Ethiopic script throughout. Document-level examples average 30-37 sentences in length. The health domain employs formal WHO institutional register; the tech domain employs informal news-digest and interview register. The closest approximation to regulatory/legal language in the entire dataset is the International Health Regulations article (legally-binding international law framework) and TRIPS Agreement references — both translated from English and neither approaching Ethiopian agricultural proclamation vocabulary.

The dataset contains zero instances of: Ethiopian government document vocabulary, cooperative membership terminology, land-tenure language, agricultural subsidy scheme names, microfinance loan terms, or Amhara regional administrative vocabulary. The source-language direction is English→Amharic throughout; no Amharic-originating documents are present.

---

### Limitations

1. **Sample size within configurations**: 5-6 examples per configuration were reviewed. With 240-334 training documents per domain, unseen examples might include edge cases. However, given that sources are exclusively WHO.int and Techpoint Africa, additional samples cannot change the domain finding.

2. **Translator background unverifiable**: Web searches for the four named Amharic translators returned no results. It is possible but undocumented that any translator has agricultural or legal Amharic expertise. This cannot be confirmed or excluded from the data alone.

3. **Register quality assessment limited**: Evaluating whether the Amharic translations exhibit procurement-register appropriateness requires native-speaker expert judgment from someone familiar with Ethiopian bureau Amharic. The current analysis can identify structural patterns (clause ordering, subordination) but cannot definitively characterize the full register distance.

4. **Evaluation metric properties not directly observable**: The scoring behavior of d-chrF, d-BLEU, and GPT-4o on out-of-domain text (i.e., agricultural proclamation language) cannot be assessed from the dataset content alone; this would require running evaluation experiments with deployment-domain text.

5. **Amhara sub-regional dialect features**: Whether the Amharic translations reflect Addis Ababa standard or Amhara regional administrative variety cannot be determined from the data. No dialect-distinguishing features are observable in health/IT domain text.

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
  "region": "Amhara Region Agricultural & Microfinance Document Translation — Cooperative and Rural MFI End-Users",
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
