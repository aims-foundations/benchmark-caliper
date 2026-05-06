I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **WXIMPACTBENCH: A Benchmark for Evaluating LLMs on Disruptive Weather Impacts** is valid for use in **Argentine Government Disaster Reporting Reliability — Policy Staff**.

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

- **Name**: wximpactbench
- **Full Name**: WXIMPACTBENCH: A Benchmark for Evaluating LLMs on Disruptive Weather Impacts
- **Domain**: Disruptive weather impact classification and ranking-based QA for LLM evaluation
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2025

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
WXIMPACTBENCH defines its task taxonomy around two evaluation tasks (multi-label classification
and ranking-based QA) and six societal impact categories: Infrastructural, Political, Financial,
Ecological, Agricultural, and Human Health [Q11, Q25]. The six categories are grounded in prior
disaster assessment literature [Q11] and are each defined with granular operational criteria
[Q135, Q136, Q137, Q138, Q139, Q140]. Within each top-level category, no sub-labels or
finer-grained distinctions are provided, a recognized limitation for local policy applications
requiring granular differentiation (e.g., informal settlement vulnerability vs. formal
infrastructure loss). The task ontology is constructed entirely around formal newspaper articles
[Q18], with no task types targeting social media posts, press releases, or short-form informal
content. Topic modeling with LDA identifies 15 primary weather event types for article selection
[Q101], but these types are not surfaced as benchmark evaluation categories. The QA task is
closed-retrieval; the open-retrieval setting is explicitly deferred to future work [Q89].
Both zero-shot and one-shot settings are supported [Q113, Q114], and the benchmark evaluates
whether LLMs can simultaneously classify all six impact categories in a single inference call [Q57].

### Input Content
The benchmark is built entirely from digitized historical Canadian newspaper articles —
specifically La Presse, La Patrie, and the Montreal Gazette — obtained through collaboration
with McGill University Library and Archives and the Bibliothèque nationale du Québec [Q97].
The corpus spans two temporal periods to capture linguistic and social change [Q13] and
comprises 4,018 digitized articles before filtering [Q20], yielding 350 annotated samples in
the long-context version and 1,386 in the mixed-context version [Q49]. Content is noted to
reflect the formal, descriptive narrative style of historical Canadian journalism [Q14, Q83, Q84],
which the paper itself identifies as making impact classification structurally easier than modern
informal text [Q83, Q85]. Authors acknowledge that "the interpretation of weather-related
disruptions in historical newspapers might be influenced by demographic and contextual factors"
[Q96] and that the benchmark "may have potential biases in underrepresented historical events
and linguistic variations" [Q90]. Pseudo questions for the QA task were generated by GPT-4O [Q59],
introducing a further layer of North American institutional framing into the content. No
Spanish-language, Argentine, or Latin American source material is represented anywhere in the corpus.

### Input Form
The benchmark is text-only, processing newspaper articles through OCR correction and delivering
inputs as plain text [Q19]. The long-context version averages approximately 2,987 tokens per
article and the mixed-context (chunked) version averages approximately 781 tokens per chunk [Q109],
with the mixed-context version created by segmenting articles into approximately 250-token segments
[Q46]. Historical articles employ "outdated terminology, spelling variations, and evolving writing
conventions" [Q14] and "more descriptive and elaborate narratives compared to modern reporting
styles" [Q14]. All evaluated models were required to support at least 8k token input lengths [Q55].
The text modality matches the deployment's text-based channels, but the long-form, formally
structured register of digitized historical newspaper content diverges from the short-form, informal,
and potentially noisy social media posts and press releases encountered in the Argentine deployment.
The benchmark's formal narrative style is noted as being actually easier for LLMs to classify [Q83],
suggesting performance estimates may not generalize to noisier informal inputs. The benchmark does
not address any non-English or non-Latin-script input forms.

### Output Ontology
The output space for the multi-label classification task consists of six binary labels per article:
Infrastructural, Political, Financial, Ecological, Agricultural, and Human Health [Q25, Q33, Q116].
Each label is operationalized as a binary true/false judgment based solely on the explicit presence
of direct descriptions of that impact type in the article [Q27, Q117]. The classification schema
does not include any credibility, reliability, trustworthiness, or signal-to-noise dimension [Q3
— elicitation inference; Q147]. Detailed criteria are provided for each label [Q141, Q142, Q143,
Q144, Q145, Q146], and the guidelines emphasize "direct and immediate effects" and "explicit
references within the text" rather than inferred or implied consequences [Q118, Q147]. For the
ranking-based QA task, the output space is a ranking of candidate articles by relevance to a
generated question [Q36]. The six-label output ontology is grounded in North American disaster
assessment frameworks and does not include categories directly addressing source credibility,
misinformation, or Argentine-specific reporting reliability — the core decision-support output
needed in the target deployment.

### Output Content
Annotation was conducted by three domain experts following structured guidelines reviewed by
meteorological specialists [Q26, Q104, Q105]. Annotators are described as members of a research
group "specializing in uncovering the history of a region's climate change through the regional
historical weather records" [Q110], whose expertise is said to "ensure the accuracy and reliability
of annotations" [Q111]. For the mixed-context version, annotations were conducted independently on
each chunk by the same experts [Q47, Q48]. Topic-aware article selection was performed by
researchers specializing in historical climate analysis to reduce temporal and geographic selection
bias [Q95]. The annotation guidelines instruct annotators to assign binary labels based on explicit
textual mentions of direct impacts rather than implications [Q118], and annotators are encouraged
to apply meteorological expertise beyond the provided examples [Q134]. OCR correction quality was
validated against human-annotated corrections on a 50-article sample, yielding high BLEU and
ROUGE agreement [Q98, Q99, Q100]. No demographic information about annotators — including
cultural familiarity with disaster communication norms outside North America — is documented.
The paper acknowledges that "demographic and contextual factors" may influence interpretation [Q96]
but does not address how this limitation was mitigated. All annotators appear to hold expertise
in Canadian/North American historical climate records, with no representation of Argentine,
Latin American, or Spanish-language disaster communication perspectives.

### Output Form
For the multi-label classification task, the benchmark reports F1-score, accuracy, and row-wise
accuracy as primary metrics [Q43, Q44, Q45]. Row-wise accuracy is described as a stricter metric
requiring exact multi-label correctness across all six categories for a given article [Q45, Q75],
and the paper observes that performance drops dramatically under this stricter evaluation [Q68].
For the ranking-based QA task, standard information retrieval metrics — Hit@1, nDCG@5, Recall@5,
and MRR — are used [Q50]. Results are reported at temperature 0, averaged over three runs [Q62].
The benchmark uses the same classification instructions for both human annotators and LLM prompts
[Q106], and the evaluation cost for proprietary models is documented (~$3 for classification,
~$5.5 for QA) [Q126]. The output form consists exclusively of binary label vectors and ranked
article lists — no credibility score, trustworthiness rating, or reliability signal is natively
produced. The benchmark's outputs can serve as upstream features for a downstream credibility
aggregation workflow, but this transformation step is non-trivial and is not addressed within
the benchmark itself.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we first develop a disruptive weather impact dataset with a four-stage well-crafted construction pipeline." |
| Q2 | 1 | input_ontology | "we propose WXIMPACTBENCH, the first benchmark for evaluating the capacity of LLMs on disruptive weather impacts." |
| Q3 | 1 | input_ontology | "The benchmark involves two evaluation tasks, multi-label classification and ranking-based question answering." |
| Q4 | 1 | input_content | "The climate-related events stored in regional newspapers record how communities adapted and recovered from disasters." |
| Q5 | 1 | input_content | "However, the processing of the original corpus is non-trivial." |
| Q6 | 1 | output_form | "Extensive experiments on evaluating a set of LLMs provide first-hand analysis of the challenges in developing the understanding of disruptive weather impact and climate change adaptation systems." |
| Q7 | 1 | input_content | "Yongan Yu1, Qingchen Hu1, Xianda Du2, Jiayin Wang3, Fengran Mo4∗, Renée Sieber1*" |
| Q8 | 1 | input_content | "1McGill University, 2University of Waterloo, 3Tsinghua University, 4University of Montreal" |
| Q9 | 1 | input_content | "the challenge of identifying impacts and responses often lies in climate-related text processing, which contains period-specific narratives and domain-specific linguistic phenomena." |
| Q10 | 1 | input_ontology | "This polysemy occurs commonly in newspapers and thus requires the system to distinguish the literal weather-related meanings and alternate usages by improving the" |
| Q11 | 2 | input_ontology | "The articles are selected by topic modeling, including six impact categories (infrastructural, political, financial, ecological, agricultural, and human health), which are informed by previous studies (Imran et al., 2016a) and align with modern disaster impact assessment frameworks (Silva et al., 2022)." |
| Q12 | 2 | input_content | "We design a four-stage data construction pipeline that begins with a disruptive weather impact dataset in which we correct OCR errors in digitalized newspaper article extraction." |
| Q13 | 2 | input_content | "We extract a sample of articles from two time periods, which cover linguistic and social changes across different eras and increase linguistic complexity due to the different descriptions of weather events in different times (Campbell, 2013)." |
| Q14 | 2 | input_form | "Historical newspapers often employed more descriptive and elaborate narratives compared to modern reporting styles (Bingham, 2010). These narratives frequently included outdated terminology, spelling variations, and evolving writing conventions (Campbell, 2013)." |
| Q15 | 2 | input_ontology | "With our constructed dataset, we develop a benchmark, WXIMPACTBENCH, to investigate the capacity of LLMs to understand disruptive weather impacts with two tasks: i) multi-label classification and ii) ranking-based question-answering." |
| Q16 | 2 | output_ontology | "The multi-label classification task employs the previous six impact categories as labels for each article whose ground-truth is annotated by human labor." |
| Q17 | 2 | input_ontology | "The question and the candidate pools for the ranking-based question-answering task are constructed based on the context and annotation of the multi-label classification task." |
| Q18 | 2 | input_ontology | "Climate impact analysis (Thulke et al., 2024) aims to help society make correct decisions about climate-related challenges affecting communities, e.g., understanding the weather impacts on society." |
| Q19 | 3 | input_form | "The construction of the dataset aims to obtain high-quality text samples. The pipeline overview is presented in Figure 2, which consists of four stages: data collection, post-OCR correction, topic-aware article selection, and manual label annotation." |
| Q20 | 3 | input_content | "The data is obtained through collaboration with a proprietary archive institution covering two temporal periods. The original data stored as digitalized text is obtained through OCR (Cheriet et al., 2007), which contains 4018" |
| Q21 | 3 | input_ontology | "Our WXIMPACTBENCH benchmark aims to evaluate to what extent existing LLMs can understand disruptive weather impacts, which also shows the evolution of vulnerability and resilience strategies from society across various periods. It involves two main stages: i) dataset construction; and ii) task definition and evaluation." |
| Q22 | 3 | input_form | "Extracting and processing historical climate articles in newspapers is challenging due to their non-digital formats, such as scanned images or physical archives. OCR enables their conversion into machine-readable text (Baird, 2004), facilitating large-scale digitization, retrieval, and analysis." |
| Q23 | 3 | input_form | "Although neural OCR correction models (Drobac and Lindén, 2020) improve the quality of the extracted text, the degraded print quality, inconsistent terminology, and irregular column layouts (Binmakhashen and Mahmoud, 2019) cause potential errors, which negatively impact the text understanding and the usage for designing downstream tasks (Bingham, 2010; Spathis and Kawsar, 2024; Wang et al., 2024)." |
| Q24 | 3 | input_content | "Thus, the lack of high-quality resources constrains the development of comprehensive benchmarks for weather impacts." |
| Q25 | 4 | output_ontology | "Six vulnerability-related disruptive weather impacts are defined as the labeling categories, including Infrastructural, Political, Financial, Ecological, Agricultural, and Human Health." |
| Q26 | 4 | output_content | "Annotation is conducted by three domain annotators following our guidelines (provided in Appendix B.2.2)." |
| Q27 | 4 | output_ontology | "According to the guidelines, the annotators should assign binary labels to indicate the presence or absence of direct descriptions of specific impacts within each article." |
| Q28 | 4 | output_ontology | "Unlike previous study (Imran et al., 2016a), however, each sample might correspond to more than one impact." |
| Q29 | 4 | input_ontology | "The overview is shown in Figure 4, which contains two tasks, multi-label classification and ranking-based question-answering, to evaluate the capacity of LLMs to understand disruptive weather impacts." |
| Q30 | 4 | input_ontology | "With the annotated weather impact category for each selected article, the intuitive evaluation task is multi-label classification, which aims to test the ability of LLMs to distinguish the disruptive weather impact for each given article." |
| Q31 | 4 | output_content | "Selected articles with informative weather content are manually reviewed by three domain experts, which result in 350 high-quality samples." |
| Q32 | 5 | input_form | "Different from them, our constructed samples require the models to understand the linguistic shifts between historical and modern texts and address inconsistent styles of narratives across various periods." |
| Q33 | 5 | output_ontology | "Specifically, given an article sample xt corresponding to six ground-truth impacts Yt = {y^i_t}^6_i=1 with binary labels y^i_t ∈ {0, 1}, the evaluated model M is required to maximize the probability of the predicated impact Ŷ_t = {ŷ^i_t}^6_i=1 towards ground-truth." |
| Q34 | 5 | output_form | "The objective function L for the given sample xt of multi-label classification task is formulated as L(Ŷ_t, Yt) = −∑^6_i=1 yi log ŷi, ŷi = M(xt)" |
| Q35 | 5 | input_ontology | "Question-answering (QA) requires the LLMs to reply to the given question based on their parametric knowledge." |
| Q36 | 5 | input_ontology | "We formulate the ranking-based QA task by prompting the models to identify the likelihood of each article containing the correct answer from a candidate pool." |
| Q37 | 5 | input_ontology | "This setting could also facilitate RAG systems development in the domain (Mao et al., 2024; Mo et al., 2024c, 2025), where we left the answer span extraction/generation for future studies." |
| Q38 | 5 | output_content | "To construct an evaluation protocol, the first step is to obtain suitable question pairs with each annotated samples in the multi-label classification task, since the question set is unavailable." |
| Q39 | 5 | input_form | "Thus, we generate pseudo questions qt for each article (xt, Yt) based on its annotated category via a generative LLM G which is formulated as qt = G(xt, Yt)." |
| Q40 | 5 | output_ontology | "The annotated categories Yt, which are the societal impacts brought by the disruptive weather event, will become part of the prompt to ensure the generated question targets one of the specific impact categories (see Figure 4)." |
| Q41 | 5 | input_form | "As a result, we have QA pair (qt, xt) for each sample." |
| Q42 | 5 | input_content | "The next step is to construct the candidate pool for ranking." |
| Q43 | 6 | output_form | "For multi-label classification task, we use F1-score, accuracy, and row-wise accuracy as evaluation metrics." |
| Q44 | 6 | output_form | "The evaluation via F1-score and accuracy are averaged across the six impact categories, historical and modern articles, and the effect of different context lengths." |
| Q45 | 6 | output_form | "Compared to the common F1-score and accuracy, the row-wise accuracy is a strict metric that requires more accurate output as the model should correctly classify all six impact labels for a given article." |
| Q46 | 6 | input_form | "For the long-context impact evaluation, we create an alternate version (mixed context), whose sample length is split into segments with approximately 250 tokens from the original one (long-context version) following (Levy et al., 2024)." |
| Q47 | 6 | output_content | "Note that annotations for these smaller chunks are performed independently by the same domain experts rather than automatically inherited from the original articles." |
| Q48 | 6 | output_content | "This independent annotation process naturally results in some chunks containing no weather impact labels, which serve as valuable negative examples in our evaluation." |
| Q49 | 6 | input_content | "Eventually, we contain 350 and 1,386 samples for the original and mixed context version datasets, respectively." |
| Q50 | 6 | output_form | "For the ranking-based QA task, we deploy the standard metric that emphasizes the accuracy of top positions for evaluation, including Hit@1, nDCG@5, Recall@5, and MRR." |
| Q51 | 6 | input_ontology | "We evaluate a set of off-the-shelf LLMs on WXIMPACTBENCH." |
| Q52 | 6 | input_ontology | "For the multi-label text classification task, we include seven open-source models: DEEPSEEK-V3-671B (DeepSeek-AI, 2024), LLAMA-3.1-8B-INSTRUCT (Llama, 2024), Mistral-7B-Instruct (Jiang et al., 2023), MIXTRAL-8X7B-INSTRUCT (Jiang et al., 2024), MISTRAL-24B-INSTRUCT (Jiang et al., 2024), GEMMA-2-9B-IT (GemmaTeam, 2024), QWEN2.5-7B-INSTRUCT, and QWEN2.5-14B-INSTRUCT (Qwen2.5, 2025); and three closed-source models: GPT-3.5-TURBO, GPT-4 (OpenAI, 2024a), and GPT-4O (OpenAI, 2024b)." |
| Q53 | 6 | input_ontology | "For the ranking-based QA task, we evaluate GPT-3.5-TURBO, QWEN2.5-7B-INSTRUCT, QWEN2.5-14B-INSTRUCT, MISTRAL-7B-INSTRUCT, and LLAMA-3.1-8B-INSTRUCT." |
| Q54 | 6 | input_form | "The relatively smaller models (with 7B size) ensure the latency requirements (Sun et al., 2023)." |
| Q55 | 6 | input_form | "The used models for the two tasks cover different sizes and support the input length of at least 8k tokens." |
| Q56 | 6 | input_form | "The multi-label classification is conducted on each evaluated LLM by the same prompt provided in Appendix C.2." |
| Q57 | 6 | input_ontology | "Different from traditional methods that decompose multi-label text classification into multiple binary classification tasks (Boutell et al., 2004; Liu et al., 2017), we simultaneously identify all relevant disruptive weather impacts for each input by calling the LLM once." |
| Q58 | 6 | input_form | "The example of in-context learning in the one-shot setting is handcrafted with a complex sample detailing multiple impacts." |
| Q59 | 6 | input_content | "We employ GPT-4O for pseudo question generation with default hyper-parameters." |
| Q60 | 6 | output_form | "For ranking evaluation, we adopt the sliding window mechanism within LLM-based ranker implementation following the state-of-the-art study (Sun et al., 2023) to reduce the potential negative effect of noisy long contexts." |
| Q61 | 7 | input_form | "Specifically, each article in the candidate pool was segmented into three chunks, and then the initial ranking was performed independently within each chunk." |
| Q62 | 7 | output_form | "To ensure stable results, following previous studies (Chen et al., 2023), all LLMs were evaluated with the temperature set to 0, and the reported performance is the average value of running the experiments three times." |
| Q63 | 7 | output_form | "Table 1 and Table 2 show the performance of the evaluated LLMs on WXIMPACTBENCH for the settings of categorized by six societal impacts with different context lengths, overall row-wise evaluation, and divided into two periods, respectively." |
| Q64 | 7 | output_ontology | "LLMs struggle to understand disruptive weather impacts." |
| Q65 | 7 | output_ontology | "Table 1 shows that the F1-score for multi-label classification remains consistently low across models, especially among the political and ecological categories." |
| Q66 | 7 | output_form | "The financial, agricultural, and human health impacts categories perform slightly better but still exhibit suboptimal results at 55%." |
| Q67 | 7 | output_ontology | "The low performance might be attributed to the challenges in these categories with abstract and context-dependent narratives." |
| Q68 | 8 | output_form | "Table 2 shows row-wise performance, in which the model must identify the given sample correctly for each involved category, the performance of classification drops dramatically due to the more precise requirement." |
| Q69 | 8 | input_content | "Thus, a sophisticated model is expected to understand the complex societal effects of historical narratives via reasoning (Wei et al., 2022; Zhang et al., 2025a,b)." |
| Q70 | 8 | output_form | "The results in Table 1 show that, when the original long-context is segmented into smaller chunks, the classification accuracy increases in most cases." |
| Q71 | 8 | input_form | "These improvements suggest that smaller chunks help models focus on relevant information and thus minimizing distraction from extraneous content." |
| Q72 | 8 | input_form | "Even the used models are claimed with long-context capacity, more precise split that reduces potential noise is still effective for context de-noising, which is consistent with previous studies (Sun et al., 2024)." |
| Q73 | 8 | output_form | "However, we also find that this trend is not observed with the row-wise accuracy evaluation." |
| Q74 | 8 | output_form | "This is due to the evaluation bias, where the F1-score measures precision and recall per category, and benefits from partial correctness." |
| Q75 | 8 | output_form | "Row-wise accuracy requires an exact match across all labels." |
| Q76 | 8 | output_form | "The small chunks might be helpful to improve the classification of one of the categories but not enough to correct all labels." |
| Q77 | 8 | output_form | "The in-context learning is achieved by providing one demonstration as the one-shot example for model decision." |
| Q78 | 8 | output_form | "Compared zero-shot and one-shot performance in Table 1, we find that providing a single example in the prompt offers limited benefits and might decrease the performance in some cases." |
| Q79 | 8 | output_ontology | "Such a phenomenon implies that the LLMs lack sufficient knowledge to disambiguate disruptive weather impacts even with enhanced examples for knowledge arousing." |
| Q80 | 8 | output_form | "These results indicate that our WXIMPACTBENCH is challenging for LLMs to understand disruptive weather impact." |
| Q81 | 8 | output_form | "The evaluation of different narratives in terms of historical and modern articles is presented in Table 3." |
| Q82 | 8 | output_form | "Surprisingly, the evaluated models perform better on the articles recorded in the historical period." |
| Q83 | 8 | input_form | "The reason might be the structured and formal narrative style used to report disruptive weather events in historical periods, which more explicitly highlights cause-and-effect relationships." |
| Q84 | 8 | input_form | "The observation is revealed by the earlier studies (e.g., Mauch and Pfister, 2009), where the historical narratives emphasize empirical observations over interpretations, offering a more immediate and naturalistic account of events." |
| Q85 | 8 | input_form | "Though the modern text might dominate within the pre-trained corpus, the language patterns used in historical narrative styles are easier for language models to identify, and thus perform better on classifying disruptive weather impacts." |
| Q86 | 9 | output_form | "larger models usually perform better than smaller ones, which is consistent with the scaling law for LLMs (Kaplan et al., 2020)." |
| Q87 | 9 | output_form | "The performance of each evaluated model for ranking-based QA is reported in Table 4." |
| Q88 | 9 | output_content | "Notice that the ranking results would contain bias when the evaluated model is used for question generation (GPT-4O in our cases). This is a common phenomenon (Zhou et al., 2023) and needs to be avoided in benchmarking." |
| Q89 | 9 | input_ontology | "The practical open-retrieval setting, i.e., identifying the relevant articles from a huge database, is left for future studies, which could further facilitate knowledge enhancement in understanding disruptive weather impacts." |
| Q90 | 9 | input_content | "Although WXIMPACTBENCH provides valuable insights (e.g., exhibit the strengths and weaknesses of various society impact understanding) about evaluating LLMs on disruptive weather, it may have potential biases in underrepresented historical events and linguistic variations." |
| Q91 | 9 | input_ontology | "Future work could expand the range of evaluated models, strategies, and designed tasks to further strengthen the evaluations." |
| Q92 | 9 | input_content | "Our primary data source is a corpus of historical digitized newspapers, obtained through collaboration with an official organization, which should be anonymous at this moment." |
| Q93 | 9 | input_content | "This organization preserves the copyright of the newspaper articles and has been granted permission to publish this subset of articles for benchmark build-up to facilitate the research community." |
| Q94 | 9 | input_content | "Thus, the data is publicly available and thus no potential privacy or content safety concerns." |
| Q95 | 9 | output_content | "Topic-aware article selection is conducted by researchers specializing in historical climate analysis to ensure the dataset is not biased on specific time and location." |
| Q96 | 9 | output_content | "The interpretation of weather-related disruptions in historical newspapers might be influenced by demographic and contextual factors, which is similar to other text datasets generated through crowd-sourcing with inherent challenges in ensuring that dataset labels are fully representative of diverse societal perspectives (Talat et al., 2022)." |
| Q97 | 9 | input_content | "Our primary data source is a corpus of three digitized newspapers (La Presse, La Patrie and Montreal Gazette), obtained through collaboration with the McGill University Library and Archives and the Bibliothèque nationale du Québec." |
| Q98 | 14 | output_content | "To assess the effectiveness of our post-OCR correction process, we evaluated GPT-4o's output against human-annotated corrections on a randomly selected sample of 50 articles." |
| Q99 | 14 | output_form | "The results demonstrate the high accuracy of the automated corrections: Metric 1-gram 2-gram 3-gram / L BLEU 0.9115 0.8935 0.8773 ROUGE 0.9476 0.9190 0.9438" |
| Q100 | 14 | output_form | "The consistently high BLEU and ROUGE scores indicate that GPT-4o's corrections closely align with human-edited versions, validating its effectiveness for improving text quality prior to downstream analysis." |
| Q101 | 14 | input_ontology | "Using Latent Dirichlet Allocation, the dataset was categorized into 15 primary weather event types." |
| Q102 | 14 | output_ontology | "In the absence of standardized impact records (e.g., flood-related property damage, injuries due to ice accumulation, power outages, and road closures), we assessed vulnerabilities and resilience based on the consequences of weather events and how they have changed since the 19th century." |
| Q103 | 14 | output_ontology | "To do so, we categorized disruptive weather impacts into six primary groups — Infrastructural, Agricultural," |
| Q104 | 15 | output_content | "To ensure high-quality and consistent annotations, the task was conducted using a set of specific instructions reviewed by meteorological experts." |
| Q105 | 15 | output_content | "The annotation guideline and the categories definition are provided in Table 14 and Table 15, respectively." |
| Q106 | 15 | output_form | "Notably, the same instruction guidance is contained within the prompts for LLMs in Appendix C to perform impact classification, following a binary output approach for each category." |
| Q107 | 15 | output_content | "Annotators are tasked with determining whether an article includes descriptions that correspond to the impact categories defined in Table 15." |
| Q108 | 15 | output_ontology | "Each article is assigned a label based on the presence or absence of relevant descriptions." |
| Q109 | 15 | input_form | "The average number of tokens per article is 2987.4 in long-context settings and 781.3 in mixed-context settings." |
| Q110 | 15 | output_content | "The annotation process was conducted by members of a research group specializing in uncovering the history of a region's climate change through the regional historical weather records." |
| Q111 | 15 | output_content | "Their expertise can ensure the accuracy and reliability of annotations." |
| Q112 | 16 | input_ontology | "The Multi-Label Classification instructions template in Table 16 is designed for both zero-shot and one-shot classification tasks." |
| Q113 | 16 | input_ontology | "Zero-Shot: The model is given only the classification instructions and the input text." |
| Q114 | 16 | input_ontology | "One-Shot for In-Context Learning: The model is provided with a demonstration for predicting a new sample." |
| Q115 | 16 | input_ontology | "Table 16 presents the prompt designed to analyze historical newspaper texts and classify them into six distinct impact categories based on explicit mentions of weather-related events." |
| Q116 | 16 | output_ontology | "The prompt is structured in alignment with the definitions provided in Table 15, which details the scope of each impact category, including Infrastructural, Agricultural, Ecological, Financial, Human Health, and Political impacts." |
| Q117 | 16 | output_ontology | "The classification task is binary (true/false), requiring the model to identify whether the text explicitly mentions any of the defined impacts." |
| Q118 | 16 | output_ontology | "The guidelines emphasize focusing on direct and immediate effects, ensuring that classifications are based solely on explicit references within the text." |
| Q119 | 16 | input_ontology | "The ranking-based QA task consists of two key components: question generation (Mo et al., 2023) and candidate ranking (Meng et al., 2024)." |
| Q120 | 16 | input_form | "Figure 6 presents the token length distribution of passages in two versions of our dataset: (a) the Long Context dataset and (b) the Mixed Context dataset used for context-denoising evaluation." |
| Q121 | 16 | input_content | "The Long Context dataset (Figure 6a), which contains 350 articles, exhibits a broader distribution of passage lengths, with a significant portion exceeding 2000 tokens." |
| Q122 | 16 | input_content | "The Mixed Context dataset (Figure 6b), which contains 1,386 articles, is heavily skewed toward shorter passages, with an overwhelming majority containing fewer than 2000 tokens." |
| Q123 | 16 | input_ontology | "GPT-4O, GPT-4 and GPT-3.5-TURBO are provided by OpenAI, the base model API document: https://platform.openai.com/docs/models" |
| Q124 | 16 | input_ontology | "DEEPSEEK-V3-671B is upgraded the DEEPSEEK-CHAT, the base model API" |
| Q125 | 17 | input_form | "Given the following passage about {row['Weather']}, generate a single, focused question that meets these criteria: 1. Can be answered using ONLY the information in this passage 2. Focuses on the {impact_str} impacts mentioned 3. Is detailed and specific to this exact situation 4. Requires understanding the passage's unique context 5. Cannot be answered by other similar passages about {row['Weather']} Passage: {row['Text']}" |
| Q126 | 17 | output_form | "For the large proprietary models (e.g., GPT-4o), conducting a one-time evaluation on our WXImpactBench costs approximately $3 for multi-label classification tasks and $5.5 for ranking-based QA tasks." |
| Q127 | 17 | output_form | "For all open-source models, evaluations were performed on a system with two NVIDIA A6000 (32GB) GPUs." |
| Q128 | 17 | output_form | "The relatively modest computational requirements highlight the accessibility of our benchmark for researchers with limited computational resources, while still enabling comprehensive evaluation of state-of-the-art models" |
| Q129 | 18 | output_content | "To ensure a high-quality evaluation of historical weather impact analysis, we developed a structured annotation framework for meteorology experts." |
| Q130 | 18 | output_content | "The goal of this annotation is to create a reliable benchmark for assessing the ability of LLMs to understand and classify disruptive weather-related societal and environmental impacts." |
| Q131 | 18 | output_content | "The detailed annotation guidelines are provided in Table 14, outlining the task objectives, category definitions, and better practices for identifying and classifying weather impacts in historical texts." |
| Q132 | 18 | input_content | "Annotators will examine historical newspaper articles documenting disruptive weather events." |
| Q133 | 18 | output_ontology | "The analysis requires the identification of impacts across six categories: infrastructural, agricultural, ecological, financial, human health, and political." |
| Q134 | 18 | output_content | "While specific examples are provided for each impact category, annotators should apply their meteorological expertise to identify and classify impacts beyond these examples, maintaining a comprehensive analytical approach." |
| Q135 | 19 | input_ontology | "Infrastructural Impact: Examines weather-related damage or disruption to physical infrastructure and essential services. Includes structural damage to buildings, roads, and bridges; disruptions to transportation (e.g., railway cancellations, road closures); interruptions to utilities (e.g., power, water supply); failures in communication networks; and industrial facility damage. Both immediate physical damage and service disruptions should be considered." |
| Q136 | 19 | input_ontology | "Agricultural Impact: Focuses on weather-related effects on farming and livestock management. Includes crop yield variations; direct damage to crops, timber, or livestock; modifications to farming schedules; disruptions to food production and supply chains; impacts on farming equipment; and changes in agricultural inputs (e.g., soil conditions, water availability, fertilizers, animal feed). Both immediate and long-term effects should be considered." |
| Q137 | 19 | input_ontology | "Ecological Impact: Examines effects on natural environments and ecosystems. Includes changes in biodiversity; impacts on wildlife populations and behavior; effects on non-agricultural plant life; habitat modifications (e.g., forests, wetlands, water bodies); changes in hydrological systems (e.g., river levels, lake conditions); and urban plant life impact. Immediate environmental changes should be prioritized." |
| Q138 | 19 | input_ontology | "Financial Impact: Analyzes economic consequences of weather events. Includes direct monetary losses; business disruptions requiring financial intervention; market fluctuations; impacts on tourism and local economies; and insurance claims or economic relief measures. The focus should be on explicit financial impacts rather than inferred consequences." |
| Q139 | 19 | input_ontology | "Human Health Impact: Examines both physical and mental health effects. Includes direct injuries or fatalities (including cases where one or more casualties are explicitly mentioned); increased risks of weather-related illnesses; mental health consequences (e.g., stress, anxiety); impacts on healthcare accessibility; and long-term health implications. Both short-term and chronic health effects should be considered." |
| Q140 | 19 | input_ontology | "Political Impact: Evaluates governmental and policy responses to weather events. Includes government decision-making and policy changes; shifts in public opinion or political discourse; effects on electoral processes; international aid and relations; and debates on disaster preparedness and response. Both direct political reactions and policy implications should be analyzed." |
| Q141 | 20 | output_ontology | "Infrastructural Impact: Classify as 'true' if the text mentions any damage or disruption to physical infrastructure and essential services. This includes structural damage to buildings, roads, or bridges; any disruptions to transportation systems such as railway cancellations or road closures; interruptions to public utilities including power and water supply; any failures in communication networks; or damage to industrial facilities. Consider only explicit mentions of physical damage or service disruptions in your classification." |
| Q142 | 20 | output_ontology | "Agricultural Impact: Classify as 'true' if the text mentions any weather-related effects on farming and livestock management operations. This includes yield variations in crops and animal products; direct damage to crops, timber resources, or livestock; modifications to agricultural practices or schedules; disruptions to food production or supply chains; impacts on farming equipment and resources; or effects on agricultural inputs including soil conditions, water availability for farming, and essential materials such as seedlings, fertilizers, or animal feed." |
| Q143 | 20 | output_ontology | "Ecological Impact: Classify as 'true' if the text mentions any effects on natural environments and ecosystems. This includes alterations to local environments and biodiversity; impacts on wildlife populations and behavior patterns; effects on non-agricultural plant life and vegetation; modifications to natural habitats including water bodies, forests, and wetlands; changes in hydrological systems such as river levels and lake conditions; or impacts on urban plant life." |
| Q144 | 20 | output_ontology | "Financial Impact: Classify as 'true' if the text explicitly mentions economic consequences of weather events. This includes direct monetary losses; business disruptions or closures requiring financial intervention; market price fluctuations or demand changes for specific goods; impacts on tourism and local economic activities; or insurance claims or economic relief measures. Focus only on explicit mentions of financial losses or fluctuations." |
| Q145 | 20 | output_ontology | "Human Health Impact: Classify as 'true' if the text mentions physical or mental health effects of weather events on populations. This includes direct injuries or fatalities (including cases where zero or more casualties are explicitly mentioned); elevated risks of weather-related or secondary illnesses; mental health consequences such as stress or anxiety; impacts on healthcare service accessibility; or long-term health implications." |
| Q146 | 20 | output_ontology | "Political Impact: Classify as 'true' if the text mentions governmental and policy responses to weather events. This includes government decision-making and policy modifications in response to events; changes in public opinion or political discourse; effects on electoral processes or outcomes; international relations and aid responses; or debates surrounding disaster preparedness and response capabilities." |
| Q147 | 20 | output_ontology | "Return 'false' for any impact category that is either not present in the text or not related to weather events. Base classifications on explicit mentions in the text. Focus on direct impacts rather than implications. Consider immediate and direct effects." |

---

## Regional Context

```yaml
name: Argentine Government Disaster Reporting Reliability — Policy Staff
abbreviation: ARG-DisasterPolicy
assessment_context:
  benchmark: wximpactbench
  deployment_use_case: An AI system evaluates the reliability and trustworthiness
    of disaster-related reporting across news, social media, and press channels in
    Argentina, distinguishing verified disaster impact signals from noisy or unverified
    content, for use by Argentine policy makers and government agency staff.
  primary_country: Argentina
  primary_city: Buenos Aires
  relevant_sub_national_regions:
  - Buenos Aires metropolitan area (AMBA) — primary deployment context
  - Río de la Plata flooding corridor — key disaster exposure zone
  - Pampa region — agricultural drought and storm exposure
  - Patagonia — pampero windstorm and drought exposure
  - Northwest Argentina (NOA) — ENSO-driven drought and flood exposure
target_population:
  description: Argentine policy makers and government agency staff with emergency
    management or disaster risk reduction responsibilities. Users are highly educated
    (master's degree minimum), upper-middle-class, and based primarily in Buenos Aires.
    They consume disaster communications in both Spanish and English, and they use
    AI-assisted tools to triage and assess the reliability of incoming reporting across
    formal news, social media, and government press channels.
  occupational_profile: Emergency management officials, disaster risk reduction analysts,
    ministry staff, and senior agency personnel. Likely affiliated with or interacting
    with institutions such as SINAGIR (Sistema Nacional para la Gestión Integral del
    Riesgo), SMN (Servicio Meteorológico Nacional), CONAE, INDEC, and provincial civil
    defense bodies.
  institutional_affiliations:
  - 'SINAGIR — Created by Ley 27.287 (2016); comprises the Consejo Nacional, Consejo
    Federal, Secretaría Ejecutiva, and Red GIRCyT. As of March 2025, Decreto 225/25
    created the Agencia Federal de Emergencias (AFE) as a new body under Ministerio
    de Seguridad, with SINAGIR now operating within the AFE''s orbit. Source: argentina.gob.ar/sinagir/institucional
    — [WEB-1]'
  - 'Servicio Meteorológico Nacional (SMN) — [NEEDS VERIFICATION — deferred: below
    search budget; institutional status not expected to have changed materially]'
  - 'CONAE (Comisión Nacional de Actividades Espaciales) — [NEEDS VERIFICATION — deferred:
    below search budget; role in disaster monitoring likely unchanged]'
  - 'Secretaría de Gestión del Riesgo y Protección Civil — [NEEDS VERIFICATION — deferred:
    ministerial home may have shifted under Milei government reorganizations; requires
    Argentina government structure check]'
  - 'Provincial civil defense bodies in Buenos Aires province — [NEEDS VERIFICATION
    — deferred: likely unsearchable at sub-national level; requires stakeholder elicitation]'
  education_level: Advanced (minimum master's degree); domain expertise in emergency
    management, public administration, or related fields
  socioeconomic_profile: Upper-middle class; consistent access to devices, stable
    connectivity, and professional digital infrastructure
  age_range: '[NEEDS VERIFICATION — deferred: no administrative or survey data found
    for this occupational cohort''s age distribution; requires stakeholder elicitation]'
  gender_distribution: '[NEEDS VERIFICATION — deferred: likely unsearchable for this
    specific occupational cohort; requires Argentine civil service statistics]'
languages:
  primary: Rioplatense Spanish
  secondary: English (intermediate-to-advanced proficiency among target users)
  source_content_language: Predominantly Argentine Spanish; English present in international
    press and some government technical documents
  note: Target users operate bilingually for professional tasks. The AI system evaluates
    source content predominantly in Rioplatense Spanish, including informal registers,
    social media abbreviations, and local vernacular. The benchmark is English-only;
    cross-lingual transfer to Spanish is a key validity gap.
  rioplatense_features: Voseo (use of 'vos' instead of 'tú'), yeísmo rehilado (distinctive
    'zh/sh' pronunciation of 'll' and 'y'), River Plate lexicon, Italian-influenced
    vocabulary. Informal social media content may include lunfardo slang and heavy
    abbreviation.
  informal_register_characteristics: Social media posts (Twitter/X, WhatsApp broadcast
    messages, Facebook) may include colloquialisms, hashtags, regional slang, incomplete
    sentences, and OCR-absent text formats that differ substantially from formal journalism.
writing_systems:
  scripts:
  - Latin alphabet (Spanish and English)
  - Standard Spanish orthography with regional conventions
  note: No right-to-left or non-Latin script concerns. Social media content may include
    emoji, non-standard capitalization, and informal punctuation that may affect tokenization
    or classification.
literacy_and_education:
  national_adult_literacy_rate: '~99% (UNESCO UIS; multiple sources converge — countryeconomy.com
    citing UNESCO — [WEB-2];
    Macrotrends/World Bank series — [WEB-3]).
    Note: most recent formal UNESCO survey data is from around 2018; trajectory has
    been consistently above 98% since 2001.'
  target_population_literacy: Near-universal among the professional policy-maker cohort;
    not a deployment constraint
  university_enrollment_rate: '19% of 25–34 year-olds in Argentina held a tertiary
    qualification in 2024 (OECD Education at a Glance 2025 — [WEB-4]).
    Note: this figure reflects the general population, not the target policy-maker
    cohort, which by definition holds advanced degrees.'
  note: Literacy and education are not limiting factors for this user population.
    The relevant challenge is not user literacy but rather the literacy of source
    content being evaluated, which spans professional journalism to informal social
    media.
digital_infrastructure:
  national_internet_penetration_pct: '~90.6% of population using internet as of end-2025
    (41.6 million users); 88.4% as of early 2024. Sources: DataReportal Digital 2026
    Argentina — [WEB-5]; Argentine
    Chamber of Internet (CABASE) via US Trade.gov — [WEB-6]'
  buenos_aires_internet_penetration_pct: 'Buenos Aires City has average fixed-line
    download speeds of 41–101 Mbps (above 40 Mbps band), among the highest in the
    country. 71% of all households with fixed internet connections are concentrated
    in five jurisdictions: Buenos Aires City and provinces of Mendoza, Buenos Aires,
    Córdoba, and Santa Fe. Source: Freedom House Freedom on the Net 2024 — [WEB-7]'
  mobile_internet_penetration_pct: '98.4% of mobile connections in Argentina are broadband
    (3G/4G/5G) as of end-2025. Source: GSMA Intelligence via DataReportal Digital
    2026 Argentina — [WEB-5]'
  smartphone_penetration_pct: '[NEEDS VERIFICATION — deferred: below search budget;
    mobile broadband penetration above is a partial proxy]'
  dominant_device_type: Desktop and laptop for professional policy users in Buenos
    Aires; mobile dominant for source content producers (journalists, social media
    users) whose output the system evaluates
  connectivity_quality_buenos_aires: 'Buenos Aires City: fixed broadband download
    speeds in the 41–101 Mbps range per ENACOM Q3 2023 data. Fixed broadband household
    coverage at ~80% nationally by end-2024; fiber represents ~41% of fixed broadband
    lines. First 5G Standalone core deployed by Telecom Argentina in Buenos Aires
    metropolitan area in late 2023. Sources: Freedom House Freedom on the Net 2024
    — [WEB-7]; ts2.tech state
    of internet access 2025 — [WEB-8]'
  connectivity_quality_interior_provinces: 'Significant urban–rural digital divide
    persists: rural provinces in the North and South have fewer broadband subscribers
    and lower average speeds. Three provinces have average fixed-line speeds below
    20 Mbps; two between 20–40 Mbps; Buenos Aires City and 19 other provinces above
    40 Mbps per ENACOM 2023. Many who lack internet access live in rural areas. Sources:
    Freedom House Freedom on the Net 2024 — [WEB-7];
    ts2.tech — [WEB-8]'
  major_platforms_for_disaster_content:
  - 'Twitter/X — Argentina had 32.9 million social media user identities as of October
    2025 (71.7% of population); 87.4% of adults 18+ use at least one social media
    platform. Twitter/X is a major platform for real-time disaster communication.
    Source: DataReportal Digital 2026 — [WEB-5].
    Argentine usage share specifically during disaster events: [NOT FOUND — searched
    DataReportal and Freedom House; event-specific Twitter share during Argentine
    disasters not published at national level]'
  - 'WhatsApp — [NEEDS VERIFICATION — deferred: below search budget; broadly dominant
    in Argentina but event-specific disaster communication share requires stakeholder
    survey]'
  - 'Facebook — [NEEDS VERIFICATION — deferred: below search budget; social media
    aggregate figures above; platform-specific share during disasters not found]'
  - 'Infobae, Clarín, La Nación, Página 12 — major online news outlets; Buenos Aires–based
    outlets received 67.4% of total national advertising expenditure, confirming dominant
    reach. Source: Freedom House Freedom on the Net 2024 — [WEB-7].
    Relative reach and disaster coverage patterns: [NEEDS VERIFICATION — deferred:
    below search budget; editorial orientation patterns require media-specific research]'
  - 'TELAM (state news agency) — [NEEDS VERIFICATION — deferred: TELAM''s operational
    status under Milei government requires current-status check; agency was subject
    to restructuring discussions in 2024]'
  - 'SMN official channels — [NEEDS VERIFICATION — deferred: below search budget;
    platform presence and follower base not found in searches]'
  note: The deployment explicitly includes social media alongside formal press; the
    AI system must handle content from all these channels. Infrastructure quality
    for the policy-user interface (Buenos Aires) is high; infrastructure quality for
    disaster-zone content producers (interior provinces) is variable.
cultural_norms_notes: '- Argentine political culture is polarized, with strong partisan
  divides between Peronist/Kirchnerist and non-Peronist blocs; disaster reporting
  can be politically instrumentalized, with government response narratives contested
  across ideological lines.

  - Crisis communication norms are less institutionalized than in Canada or the United
  States; the public information space is more fluid and subject to rapid shifts in
  official messaging.

  - Argentine professional officials draw on international (Global North) standards
  for emergency management frameworks, meaning benchmark label categories grounded
  in North American frameworks are not expected to produce systematic label disagreement
  for formal press content.

  - Social media and informal channels carry culturally embedded communication patterns
  — solidarity networks, humor as coping mechanism, distrust of official sources,
  neighborhood-level self-organization (barrio networks) — not represented in formal
  journalism norms.

  - Villas miseria (informal settlements) in the AMBA represent a distinct policy-relevant
  population whose disaster vulnerability and communication practices differ from
  formal urban and rural populations; impacts on this group are a known blind spot
  in North American-derived disaster framing.

  - Institutional actors cited in Argentine disaster reporting differ from Canadian
  equivalents: SINAGIR, SMN, provincial civil defense bodies, municipios, barrio juntas.
  LLMs trained on North American corpora may not reliably recognize these actors as
  authoritative sources.

  - Political sensitivity around ENSO-driven agricultural droughts (Pampa soybean
  and grain production) is high given Argentina''s export-dependent economy and recurring
  fiscal crises.'
disaster_types_and_reporting_ecosystems:
  primary_disaster_types:
  - type: Urban flash floods — Buenos Aires and AMBA
    notes: 'Triggered by intense rainfall overwhelming drainage infrastructure; reporting
      spans SMN alerts, municipal civil defense notices, social media eyewitness posts,
      and mainstream press. Villa miseria neighborhoods face disproportionate impact.
      [NEEDS VERIFICATION — deferred: frequency, recent major events, and key institutional
      response actors require Argentina-specific disaster event database review; below
      search budget]'
  - type: Río de la Plata flooding (sudestada)
    notes: 'Storm surge events driven by sustained southeasterly winds; affects coastal
      Buenos Aires and the Paraná-Plata river system. Distinct institutional reporting
      ecosystem involving Prefectura Naval Argentina and provincial actors. [NEEDS
      VERIFICATION — deferred: recent major events and key reporting actors; below
      search budget]'
  - type: Pampero windstorms
    notes: 'Sudden cold-front wind events affecting the Pampa and Buenos Aires; associated
      with infrastructure damage and agricultural disruption. Reporting patterns may
      differ from major flood events. [NEEDS VERIFICATION — deferred: below search
      budget; likely unsearchable at the level of reporting ecosystem detail required]'
  - type: ENSO-driven agricultural drought (Pampa)
    notes: 'Multi-season droughts affecting soybean, maize, wheat production in Buenos
      Aires, Córdoba, Santa Fe, Entre Ríos provinces; high political and financial
      salience. Reporting ecosystem includes agroindustrial media (Agro Radio, La
      Rural), commodity markets, and INDEC crop reports. [NEEDS VERIFICATION — deferred:
      recent major drought events and reporting patterns; below search budget]'
  - type: Patagonian wind events and wildfire
    notes: 'High-intensity wind events and drought-driven wildfires in Neuquén, Río
      Negro, Chubut, Santa Cruz; less densely covered by national media relative to
      Buenos Aires events. [NEEDS VERIFICATION — deferred: below search budget]'
  - type: Northwest Argentina (NOA) flooding and drought
    notes: 'ENSO-linked events affecting Tucumán, Salta, Jujuy, Santiago del Estero;
      sugarcane, citrus, tobacco agriculture exposed. Reporting ecosystem involves
      provincial governments and is less visible nationally. [NEEDS VERIFICATION —
      deferred: below search budget]'
  note: The benchmark covers no Argentine disaster events or geographic areas; all
    six disaster types listed above are absent from WXImpactBench ground-truth data.
    Sub-national reporting ecosystems differ substantially in institutional actor
    prominence, social media penetration, and informal-versus-formal content mix.
source_content_taxonomy:
  formal_press:
    description: National and regional newspapers, wire services (TELAM), online news
      outlets; structured journalism with editorial standards
    benchmark_alignment: Closest match to benchmark's historical Canadian newspaper
      corpus; cultural and framing differences noted but not expected to produce systematic
      label disagreement
    key_outlets: '[NEEDS VERIFICATION — deferred: confirm current reach and editorial
      orientation of Clarín, Infobae, La Nación, Página 12, Crónica, regional outlets;
      below search budget; Freedom House 2024 confirms Buenos Aires–based outlets
      receive 67.4% of national advertising but does not provide individual outlet
      reach figures]'
  social_media:
    description: Twitter/X posts, Facebook updates, WhatsApp broadcast messages; highly
      variable register, length, and reliability
    benchmark_alignment: No coverage in benchmark; benchmark's formal historical narrative
      style is easier for LLMs to classify, suggesting performance estimates may substantially
      overstate model capability on social media inputs
    key_platforms: 'Argentina has 32.9 million social media user identities (71.7%
      of population) as of October 2025 (DataReportal Digital 2026 — [WEB-5]).
      Argentine platform-specific usage shares during disaster events: [NOT FOUND
      — not published at event-specific level in searched sources]'
  government_press_releases:
    description: Official communications from SMN, SINAGIR, municipal civil defense,
      provincial governments; formal but shorter than newspaper articles
    benchmark_alignment: Partial match in formality but shorter-form; institutional
      actor names unfamiliar to North American-trained models
  informal_community_networks:
    description: Barrio-level social media groups, neighborhood WhatsApp chains, villa-based
      community communicators; high local specificity, low verification
    benchmark_alignment: No coverage in benchmark; represents the highest-noise content
      type in the deployment
regulatory_and_policy_context:
  national_disaster_risk_reduction_framework: 'SINAGIR established by Ley 27.287 (October
    2016); Decreto Reglamentario 383/2017 specifies operational objectives. In March
    2025, Decreto 225/25 created the Agencia Federal de Emergencias (AFE) as a new
    body under Ministerio de Seguridad, with SINAGIR now operating within the AFE''s
    orbit. SINAGIR published the Plan Nacional para la Reducción del Riesgo de Desastres
    (PNRRD 2025-2029) in 2023–2024. Sources: argentina.gob.ar/sinagir/institucional
    — [WEB-1]; SEGEMAR/OAVV — [WEB-9]'
  data_protection_regulation: 'Current governing law is Ley 25.326 (Personal Data
    Protection Act, enacted 2000). As of early 2025, the law has not been replaced;
    multiple reform bills are pending in Congress (including Bills 644-S-2025 and
    1948-D-2025 seeking comprehensive replacement, and Bill 4243-D-2025 on AI-specific
    data protection). No reform has been enacted as of the search date (May 2025).
    Sources: Lexology — [WEB-10];
    EU IP Helpdesk — [WEB-11]'
  ai_governance_framework: 'No enacted AI-specific law as of May 2025. Current framework
    comprises: Provision 2/2023 (ethical principles for AI human oversight and accountability);
    Resolution 161/2023 (national program for responsible AI led by AAIP); AAIP Guide
    for Public and Private Entities on Transparency and Personal Data Protection for
    Responsible AI (September 2024, non-binding). Bill 3003-D-2024 (comprehensive
    risk-based AI framework, introduced June 2024) is pending in Congress but unenacted.
    Sources: digital.nemko.com — [WEB-12];
    World Law Group — [WEB-13]'
  public_information_access_law: '[NEEDS VERIFICATION — deferred: Ley 27.275 (Acceso
    a la Información Pública, 2016) is the likely current framework but current enforcement
    status under Milei administration requires verification; below search budget]'
  emergency_communication_standards: '[NEEDS VERIFICATION — deferred: likely unsearchable
    at required specificity; whether SMN or SINAGIR has codified crisis communication
    protocols requires direct agency consultation]'
  note: Argentine crisis communication norms are noted by elicitation as less institutionalized
    than Canadian equivalents; regulatory instability (including frequent policy changes
    across administrations) means any named regulation should be verified for current
    status. The March 2025 creation of the AFE is a significant structural change
    that deployments should account for when identifying authoritative institutional
    actors.
benchmark_validity_dimensions:
  input_ontology:
    priority: MODERATE
    summary: The six top-level impact categories (Infrastructural, Political, Financial,
      Ecological, Agricultural, Human Health) are broadly applicable to Argentine
      disaster types. Absence of sub-labels is a recognized gap for local policy granularity.
      The benchmark's task ontology covers only formal newspaper articles; social
      media and press release input types are absent.
    key_gaps:
    - No sub-labels within the six categories for Argentine-specific policy needs
      (e.g., informal settlement infrastructure vs. formal, agricultural product-specific
      loss, political framing by Argentine institutional actors)
    - No task type targeting social media posts, short-form press bulletins, or informal
      content
    - Disaster event types in the benchmark (Canadian weather events) do not include
      pampero windstorms, sudestada, ENSO-driven Pampa drought, or Argentine urban
      flash floods
  input_content:
    priority: HIGH
    summary: The benchmark corpus is exclusively English-language historical Canadian
      newspaper text. No Argentine, Latin American, or Spanish-language content is
      represented. Social media and informal channel content — a primary deployment
      data type — is entirely absent from the benchmark. Complementary social media
      disaster benchmarks exist (HumAID, CrisisBench, CrisisNLP) but are predominantly
      English-language and do not cover Argentine events specifically.
    key_gaps:
    - No Spanish-language or Rioplatense Spanish content
    - No social media or informal text
    - No Argentine institutional actors, geographic references, or local disaster
      framing
    - No representation of informal settlement (villa miseria) reporting context
  input_form:
    priority: MODERATE
    summary: Benchmark is text-only, matching the deployment's text modality. However,
      the benchmark's long-form formal historical newspaper register (avg. 2,987 tokens)
      diverges substantially from short-form social media posts and press bulletins
      in the deployment. The benchmark paper notes that formal historical style is
      actually easier for LLMs to classify, suggesting performance estimates may not
      generalize to noisier informal inputs.
    key_gaps:
    - No short-form content evaluation (tweet-length, press bulletin-length)
    - No evaluation of informal register, slang, abbreviations, or emoji
    - No multilingual or code-switched input handling
  output_ontology:
    priority: HIGH
    summary: The deployment's core task — reliability and credibility scoring of disaster
      reports — is structurally absent from the benchmark's output space. The benchmark
      produces six binary impact labels and ranked article lists. The credibility
      layer is envisioned as an external downstream aggregation step, creating a gap
      between benchmark outputs and primary decision-support need. No complementary
      Argentine or Latin American-specific disaster credibility scoring benchmark
      was found in searches.
    key_gaps:
    - No credibility, trustworthiness, or signal-to-noise dimension in benchmark output
    - No misinformation likelihood scoring
    - No source authority scoring
    - Output transformation from binary labels to credibility scores is non-trivial
      and unaddressed in benchmark documentation
  output_content:
    priority: MODERATE
    summary: All benchmark annotators specialize in historical Canadian/North American
      climate records with no representation of Argentine or Latin American disaster
      communication perspectives. The benchmark paper acknowledges that demographic
      and contextual factors may influence annotation but does not address this gap.
      The user does not anticipate systematic label disagreement for formal press,
      but informal and politically charged Argentine content may drift from Canadian
      ground-truth assumptions.
    key_gaps:
    - No annotator familiarity with Argentine institutional actors or regional disaster
      communication norms
    - No representation of social vulnerability framing relevant to Argentine informal
      settlements
    - Potential drift for politically charged or informally framed Argentine disaster
      reports
  output_form:
    priority: MODERATE
    summary: Benchmark outputs (binary label vectors, ranked article lists) are usable
      as upstream inputs to the deployment's credibility aggregation workflow. However,
      the transformation from benchmark output to credibility score requires a non-trivial
      aggregation step with external source metadata, not addressed in the benchmark.
    key_gaps:
    - No native credibility or reliability score produced
    - Output aggregation pipeline design is outside benchmark scope
    - Integration with Argentine source metadata (outlet reach, account verification
      status, institutional affiliation) is not specified
flagged_gaps_for_web_search:
- gap_id: 1
  label: Social media and informal channel content
  search_target: disaster impact classification benchmark social media informal text
    Spanish language Argentina Twitter flood storm
  search_result_summary: 'Searches found multiple English-language social media disaster
    benchmarks (HumAID with ~77K annotated tweets from 19 disaster events 2016–2019;
    CrisisBench; CrisisNLP; CrisisLex). These cover primarily English-language events;
    no Argentina-specific or Rioplatense Spanish social media disaster benchmark was
    found. HumAID and CrisisBench are the best available complementary resources for
    the social media gap, but transfer to Argentine Spanish and local disaster types
    is unvalidated. Source: CrisisNLP — [WEB-14];
    HumAID paper ICWSM 2021 — [WEB-15]'
- gap_id: 2
  label: Rioplatense Spanish and Spanish-language disaster NLP
  search_target: Spanish language disaster NLP benchmark Argentina climate weather
    impact Rioplatense LLM evaluation cross-lingual transfer
  search_result_summary: '[NOT FOUND — no Argentine Spanish-language or Rioplatense-specific
    disaster NLP benchmark found in searches. Cross-lingual crisis classification
    research exists (multilingual BERT achieving ~80% F1 in cross-domain cross-lingual
    settings per ResearchGate), but no Argentina-specific validation. This confirms
    the gap is real and not simply unsearched.]'
- gap_id: 3
  label: Credibility and misinformation scoring infrastructure
  search_target: disaster misinformation detection benchmark credibility scoring source
    reliability Spanish Latin America LLM evaluation
  search_result_summary: 'Searches found general LLM misinformation detection benchmarks
    (Pastel weakly supervised credibility signal extraction, EPJ Data Science 2025;
    MMFakeBench multimodal misinformation; VLDBench). No disaster-specific credibility
    scoring benchmark for Latin America or Spanish-language contexts was found. Pastel
    (weakly supervised LLM credibility signal extraction) is the closest methodological
    complement, but was not validated on Spanish or Argentine content. Source: Pastel
    — [WEB-16]'
- gap_id: 4
  label: Argentine institutional actors and sub-national disaster geography in NLP
    evaluation data
  search_target: Argentina SINAGIR SMN CONAE disaster risk reduction NLP benchmark
    Buenos Aires flood risk evaluation sub-national
  search_result_summary: '[NOT FOUND — no NLP benchmark or evaluation dataset incorporating
    Argentine disaster institutional actors (SINAGIR, SMN, CONAE, AFE) or sub-national
    Argentine geography was found. The gap is real and not simply unsearched. SINAGIR''s
    legal and institutional structure was verified (see regulatory context above).]'
- gap_id: 5
  label: Informal settlement and social vulnerability framing
  search_target: informal settlement disaster vulnerability Argentina villa miseria
    urban flood impact NLP classification benchmark social vulnerability
  search_result_summary: '[NOT FOUND — no NLP benchmark or classification dataset
    addressing informal settlement (villa miseria) disaster vulnerability framing
    in Argentina was found. This confirms a documentation gap, not an absence of the
    cultural phenomenon. Requires stakeholder elicitation and community-sourced data.]'
- gap_id: 6
  label: Short-form and informal register text classification
  search_target: short-form disaster text classification benchmark social media tweet
    length Spanish informal NLP LLM register
  search_result_summary: 'HumAID and CrisisBench provide the closest existing benchmarks
    for short-form (tweet-length) disaster classification, but are English-language.
    Research on LLM performance on flood-related social media data specifically found
    that ''most LLMs face challenges in processing flood-related data'' even in English
    (Semantic Scholar, citing analysis of six LLMs on HumAID). No Spanish-language
    equivalent confirmed. Source: [WEB-17]'
- gap_id: 7
  label: Complementary Spanish-language disaster benchmarks
  search_target: Spanish disaster benchmark NLP Latin America weather climate impact
    text classification evaluation dataset 2023 2024 2025
  search_result_summary: '[NOT FOUND — no Spanish-language or Latin American disaster
    impact classification benchmark comparable to WXImpactBench was identified in
    searches. The absence confirms that WXImpactBench cannot be supplemented with
    a Spanish-language equivalent for cross-lingual validation at this time.]'
- gap_id: 8
  label: Argentine crisis communication norms and institutional standards
  search_target: Argentina crisis communication standards SINAGIR emergency management
    information protocols disaster reporting norms official channels
  search_result_summary: 'SINAGIR''s legal basis (Ley 27.287), structure, and PNRRD
    2025-2029 were confirmed. The March 2025 creation of the AFE as SINAGIR''s new
    institutional home is a significant recent change. No codified crisis communication
    protocol specifically defining authoritative sources for public information was
    found; this is consistent with the elicitation''s characterization of Argentine
    crisis communication norms as less institutionalized than North American equivalents.
    Sources: argentina.gob.ar/sinagir/institucional — [WEB-1]'
domain_specific_notes: '- Emergency management: Argentine institutional actors (SINAGIR,
  SMN, provincial civil defense) are not represented in the benchmark corpus or annotation
  guidelines. LLMs evaluated on WXImpactBench may not reliably recognize these actors
  as authoritative sources when applied to Argentine content. As of March 2025, SINAGIR
  now operates within the newly created Agencia Federal de Emergencias (AFE) under
  Ministerio de Seguridad (Decreto 225/25).

  - Agricultural reporting: Pampa agricultural drought impacts are policy-critical
  given Argentina''s export economy; the benchmark''s Agricultural Impact category
  is broadly applicable but Canadian grain/livestock framing may not map cleanly onto
  Argentine soybean/maize/wheat commodity reporting or INDEC agricultural statistics.

  - Urban flooding: The combination of formal infrastructure damage and informal settlement
  vulnerability (villas miseria) in AMBA flooding events creates a classification
  challenge not represented in the benchmark; the Political Impact category may need
  to capture social vulnerability dimensions absent from the Canadian framing.

  - Social media noise: The deployment explicitly requires distinguishing verified
  signals from noisy or unverified social media content; the benchmark provides no
  tools for this and performs best on formal long-form text — the inverse of the highest-noise
  deployment inputs. Research on six LLMs applied to HumAID confirms that most LLMs
  face specific challenges with flood-related social media data even in English, amplifying
  the concern for Spanish-language informal content.

  - Political polarization: Argentine disaster reporting frequently becomes politically
  instrumentalized across Kirchnerist/non-Kirchnerist lines; Political Impact classification
  in this context may require sensitivity to domestic partisan framing not present
  in the benchmark''s Canadian government-response framing.

  - Credibility aggregation: The downstream credibility scoring layer envisioned by
  the user requires source metadata (outlet reach, account verification, institutional
  affiliation) that is Argentine-specific and not addressed by the benchmark; this
  integration layer represents a significant deployment engineering task beyond benchmark
  application.

  - Complementary benchmark recommendation: HumAID (CrisisNLP/QCRI, ICWSM 2021) is
  the closest available complement for the social media gap, providing ~77K annotated
  English-language disaster tweets across 19 events with humanitarian categories.
  CrisisBench aggregates multiple such datasets. Neither covers Argentine events or
  Spanish; both could serve as development/test resources if cross-lingual transfer
  is validated. Source: [WEB-14]

  '
net_new_fields:
  sinagir_structural_change_2025: 'As of March 2025, Decreto 225/25 created the Agencia
    Federal de Emergencias (AFE) as an organismo desconcentrado under Ministerio de
    Seguridad. SINAGIR now operates within the AFE''s orbit; the AFE is the new autoridad
    de aplicación for Ley 27.287. Deployments should treat the AFE — not a standalone
    SINAGIR secretariat — as the primary national emergency management authority for
    institutional actor recognition. Source: argentina.gob.ar/sinagir/institucional
    — [WEB-1]'
  ai_governance_status_argentina_2025: 'No enacted national AI law as of May 2025.
    Current framework is non-binding: AAIP Provision 2/2023 (ethical principles),
    Resolution 161/2023 (responsible AI program), and AAIP September 2024 Guide for
    Responsible AI (non-binding best practices). Bill 3003-D-2024 (risk-based AI framework
    modeled on EU AI Act) is pending but unenacted. Government AI systems, including
    the proposed disaster reporting AI, currently operate under the general data protection
    framework (Ley 25.326) and non-binding AAIP guidance only. This creates legal
    uncertainty relevant to procurement and liability for government AI deployments.
    Sources: digital.nemko.com — [WEB-12];
    Morrison Foerster AI Library Argentina — [WEB-18]'
  data_protection_reform_status_2025: 'Ley 25.326 (2000) remains the operative data
    protection law; no replacement enacted as of May 2025. Multiple reform bills are
    active (644-S-2025, 1948-D-2025, 4243-D-2025), with several specifically addressing
    AI and automated decision-making. The AAIP issued non-binding AI transparency
    guidelines in September 2024. Government AI systems processing personal data in
    disaster contexts must currently comply with Ley 25.326. Sources: Lexology — [WEB-10];
    JURIST commentary — [WEB-19]'
  humaid_as_complementary_benchmark: 'HumAID (Alam et al., ICWSM 2021) is the most
    relevant publicly available complementary benchmark for the social media gap:
    ~77K human-annotated English-language tweets from 19 disaster events (2016–2019)
    across 11 humanitarian categories. CrisisBench (2021) consolidates HumAID and
    other crisis datasets. Neither covers Argentine events, Spanish language, or impact-type
    classification (vs. humanitarian action categories). Both are English-language
    benchmarks with North American/global event coverage; cross-lingual transfer to
    Argentine Spanish is unvalidated. These benchmarks could be used to test model
    social-media register generalization before deployment, with the caveat that language
    transfer adds a confounding factor separate from cultural transfer. Source: CrisisNLP
    — [WEB-20]; HumAID dataset — [WEB-14]'
  lllm_flood_social_media_performance_caveat: 'An analysis of six LLMs applied to
    HumAID and related crisis datasets found that GPT-4o and GPT-4 offer better generalizability
    across disasters and information types, but most LLMs face specific challenges
    processing flood-related social media data even in English. This finding is directly
    relevant to the AMBA urban flooding use case: benchmark performance on WXImpactBench
    (formal historical text) likely overstates model capability on informal social
    media flood content in any language. Source: Semantic Scholar citing Alam et al.
    follow-up analysis — [WEB-17]'
  connectivity_rural_argentina_policy_implication: 'Argentina''s urban–rural digital
    divide is material to the deployment''s source content ecosystem: disaster events
    in Patagonia, NOA, and rural Pampa regions are reported by producers with lower
    connectivity than Buenos Aires. Three provinces have average fixed-line download
    speeds below 20 Mbps; Buenos Aires City is above 40 Mbps. 71% of fixed internet
    connections are concentrated in five jurisdictions. This means that disaster-zone
    social media content from high-exposure interior regions may carry compression
    artifacts, delayed posting, or rely on mobile-only channels, adding noise characteristics
    not represented in the benchmark. Sources: Freedom House Freedom on the Net 2024
    — [WEB-7]; ts2.tech —
    [WEB-8]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.argentina.gob.ar/sinagir/institucional |
| WEB-2 | https://countryeconomy.com/demography/literacy-rate/argentina |
| WEB-3 | https://www.macrotrends.net/global-metrics/countries/arg/argentina/literacy-rate |
| WEB-4 | https://gpseducation.oecd.org/CountryProfile?primaryCountry=ARG&treshold=10&topic=EO |
| WEB-5 | https://datareportal.com/reports/digital-2026-argentina |
| WEB-6 | https://www.trade.gov/country-commercial-guides/argentina-digital-economy |
| WEB-7 | https://freedomhouse.org/country/argentina/freedom-net/2024 |
| WEB-8 | https://ts2.tech/en/state-of-internet-access-in-argentina-fiber-5g-and-satellite-in-2025/ |
| WEB-9 | https://oavv.segemar.gob.ar/sinagir/ |
| WEB-10 | https://www.lexology.com/library/detail.aspx?g=d696be0e-4476-4c8c-83f9-6360dd701d70 |
| WEB-11 | https://intellectual-property-helpdesk.ec.europa.eu/news-events/news/draft-law-protection-personal-data-argentina-2024-01-09_en |
| WEB-12 | https://digital.nemko.com/regulations/ai-regulation-argentina |
| WEB-13 | https://www.theworldlawgroup.com/membership/news/news-argentina-releases-guidelines-for-responsible-ai-implementation |
| WEB-14 | https://crisisnlp.qcri.org/humaid_dataset |
| WEB-15 | https://ojs.aaai.org/index.php/ICWSM/article/download/18116/17919/21611 |
| WEB-16 | https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-025-00534-0 |
| WEB-17 | https://www.semanticscholar.org/paper/HumAID:-Human-Annotated-Disaster-Incidents-Data-Alam-Qazi/462cc2046ef4d48d844813b66d8a1ed6dfda3bc0 |
| WEB-18 | https://www.mofo.com/artificial-intelligence/argentina |
| WEB-19 | https://www.jurist.org/commentary/2025/12/why-argentinas-pioneering-privacy-law-is-now-playing-defense-against-ai/ |
| WEB-20 | https://crisisnlp.qcri.org/ |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark categories cover infrastructural, political, financial, ecological, agricultural, and human health impacts of weather events. For disaster reporting reliability in Argentina, are there impact categories that matter to your policy makers but might not appear here — for example, impacts on informal settlements (villas), agricultural disruption in Pampa or Patagonia, or flooding along the Río de la Plata basin? Are there disaster types (e.g., pampero windstorms, ENSO-driven droughts, urban flash floods in Buenos Aires) whose reporting patterns your users need to evaluate?
A1: The six top-level categories from the benchmark are broadly applicable to the Argentine context and could accommodate the named disaster types. However, the user noted that sub-labels or more granular categories within those six dimensions would be valuable and are currently absent.

Q2 [IC]: The benchmark is built from historical Canadian newspaper articles, which reflect Northern Hemisphere disaster framing, infrastructure norms, and institutional actors. For your Argentine policy makers assessing reporting reliability, would culturally embedded assumptions in the data — such as which agencies are cited as authoritative, what counts as 'normal' disaster response, or how agricultural loss is framed — misalign with what Argentine news sources or government communications typically convey?
A2: Cultural assumptions in formal press and news articles are not expected to be a major concern, as journalistic norms are relatively transferable. However, informal or social media data carries meaning and communication patterns that are likely not represented in the Canadian-sourced benchmark, and this is where misalignment is anticipated.

Q3 [OO]: Your deployment centers on distinguishing noisy or unreliable signals from verified disaster reporting — a reliability or trustworthiness judgment — rather than simply classifying impact type. The benchmark's output space is multi-label impact classification and ranking. Does your use case require a scoring dimension for source credibility, misinformation likelihood, or signal-to-noise quality, which may not map onto the existing six impact labels or the ranking task?
A3: The ideal deployment would include a source credibility scoring dimension, but the user envisions this as a downstream layer built on top of the benchmark's existing outputs. Policy users would aggregate model results with external metadata (e.g., source popularity/relevance) to construct credibility scores, meaning the benchmark itself does not need to directly output credibility judgments.

Q4 [OC]: The benchmark's ground-truth labels were derived from Canadian newspaper content, likely annotated by annotators familiar with North American disaster communication norms. For your context, would Argentine policy experts, emergency management officials, or journalists plausibly disagree with those labels — for instance, on whether a given report constitutes a 'real signal' of disaster impact versus noise — especially given differences in how Argentine media covers government response or social vulnerability?
A4: Argentina has less institutionalized or stable crisis communication norms than Canada or North America broadly; the public information space is more fluid. However, Argentine policy experts and emergency officials tend to draw on international and Global North communication standards and adapt them locally. Local press similarly follows patterns from those reference contexts. As a result, the user does not expect systematic disagreement with labels applied to Canadian data, and sees model failure analysis as a potential tool for defining more locally specific sub-labels over time.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | The six top-level impact categories are broadly applicable to Argentine disasters, but the absence of sub-labels is a recognized gap for local policy granularity, and informal/social media data types used in deployment fall outside the benchmark's newspaper-only ontology. |
| IC | HIGH | The benchmark relies on historical Canadian newspaper text with North American institutional framing; while formal press may transfer reasonably, the deployment explicitly includes social media and informal channels whose cultural content and noise patterns are not represented in the benchmark corpus. |
| IF | MODERATE | The benchmark is text-only, matching the text-based channels in the deployment; however, the inclusion of social media posts and press releases alongside formal news introduces input surface variation (informal register, short-form text, OCR artifacts) that differs from the benchmark's digitized historical newspaper format. |
| OO | HIGH | The deployment's core task — reliability and credibility scoring — is structurally absent from the benchmark's output space (multi-label impact classification and ranking); the credibility layer is envisioned as external to the model, creating a gap between benchmark outputs and the primary decision-support need. |
| OC | MODERATE | The user does not anticipate systematic label disagreement, given that Argentine professional norms draw on Global North standards; however, the fluid and evolving nature of Argentine crisis communication means label validity for informal or politically charged reporting events could drift from Canadian ground-truth assumptions over time. |
| OF | MODERATE | The benchmark outputs labels, scores, and rankings, which are usable as upstream inputs to the deployment's credibility aggregation workflow; however, the deployment ultimately requires a scoring output that the benchmark does not natively produce, requiring a non-trivial output transformation step. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** Michaelyya/wximpactbench-1386 (mixed-context / chunked version)
**Analysis date:** 2025-07-10
**Examples reviewed:** 31 from `train` split
**Columns shown:** id, date, time_period, weather_type, text, infrastructural_impact, political_impact, financial_impact, ecological_impact, agricultural_impact, human_health_impact
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | wximpactbench-1386 | Ex. 1 (id=198) | all zeros | "John's Cloudy -4 -4 United States Max Min Atlanta Cloudy 17 4 Boston Cloudy 3 -6 Chicago Cloudy 2 2 Dallas Thunderstorms 11 2..." | Weather forecast table with temperature/condition data; no impact content | IO, IC |
| D2 | wximpactbench-1386 | Ex. 2 (id=199) | all zeros | "But the real beneficiaries of the work-at-home trend are the employees themselves... She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9) Down 1, Full of ill-will and disease (9)..." | Non-weather content: work-from-home editorial + crossword puzzle clues | IO, IC |
| D3 | wximpactbench-1386 | Ex. 4 (id=89) | all zeros | "Clarkson was arrested July 16 as he left the Glenora home of Marilyn Tan... Clarkson is currently charged with conspiracy to murder photographer Con Boland." | Crime reporting with no weather content; zero-impact label justified | IO, IC |
| D4 | wximpactbench-1386 | Ex. 5 (id=98) | all zeros | "Polls have suggested that the party still may be able to win the 10 per cent of 12 million votes in eastern Germany that are needed to secure seats in the Bonn parliament." | Post-reunification German politics (East Germany, Berlin Wall anniversary); no weather | IO, IC |
| D5 | wximpactbench-1386 | Ex. 9 (id=82) | all zeros | "Peter Russell, a law professor at the University of Toronto, said the Supreme Court will benefit from Binnie's solid experience in constitutional and international affairs." | Canadian Supreme Court appointment reporting; no weather content | IO, IC |
| D6 | wximpactbench-1386 | Ex. 11 (id=212) | all zeros | "They refused to give any indication as to where they got the silver, but Mr. Dunnuis joined the tribe, married an Indian girl and thus learned their secret." | Historical narrative about Indigenous land/mining; no weather impact | IO, IC |
| D7 | wximpactbench-1386 | Ex. 19 (id=92) | all zeros | "National Lampoon's Van Wilder 2: The Rise of Taj Starring: Kal Penn, Lauren Cohan and Daniel Percival Playing at: AMC, Brossard, Cavendish, Colossus, LaSalle cinemas." | Film review; no weather content at all | IO, IC |
| D8 | wximpactbench-1386 | Ex. 25 (id=83) | all zeros | "His mother, whose maiden name was O'Malley, actually was adopted, Cascarino wrote in his autobiography. Ireland actually does have a regulation that allows offspring of children adopted by Irish parents to assume Irish citizenship." | Sports journalism (soccer eligibility rules); no weather content | IO, IC |
| D9 | wximpactbench-1386 | Ex. 28 (id=88) | all zeros | "'He can get his fastball up to 93 (mph) and averages out at 90-91.'" | Baseball scouting report; no weather content | IO, IC |
| D10 | wximpactbench-1386 | Ex. 29 (id=92) | all zeros | "Kennedy dramatically quit the race after only the second ballot, instantly propelling Dion into first place on the third ballot..." | Canadian Liberal Party leadership race; no weather content | IO, IC |
| D11 | wximpactbench-1386 | Ex. 21 (id=330) | all zeros | "Just two hours before this, in Richmond, the storm so long expected has broken forth in all its fury. Great flashes of blinding lightning intermingled with the grand roar of the thunder from on high..." | Literary/fictional storm passage embedded in historical newspaper; labeled all-zero | OC, IO |
| D12 | wximpactbench-1386 | Ex. 13 (id=213) | all zeros | "Rev. Principal Grant, of Queen's University, Kingston, Ont, lectured on the subject of 'Canada First.'... With regard to unrestricted commercial intercourse between the two countries..." | Political/trade speech; no weather content | IO, IC |
| D13 | wximpactbench-1386 | Ex. 31 (id=214) | all zeros | "The Legislative council has refused to abolish itself. The government bill, enacting abolition, adopted unanimously by the lower House, was referred to the committee of privilege in the council." | Canadian legislative politics; no weather content | IO, IC |
| D14 | wximpactbench-1386 | Ex. 3 (id=26) | infrastructural=1, others=0 | "by six o'clock the electric car services in all the important points west of Toronto had been completely paralyzed... an unprecedented snowfalls and heavy winds." | 1894 blizzard; infrastructure (transit) disruption labeled; North American geography | IO, OC, IC |
| D15 | wximpactbench-1386 | Ex. 17 (id=26) | infrastructural=1, others=0 | "TRAFFIC IS PARALYZED In Western Canadian Cities, and at Many Points In the United States Disasters In England." | Different chunk of same 1894 blizzard article; ads for Montreal-based construction suppliers surround weather content | IC, IF |
| D16 | wximpactbench-1386 | Ex. 14 (id=34) | infra=1, political=1, financial=1 | "Aid Laurent said that there were mountains of snow all over the city. Already $30,000 has been expended in removing it... Seven hundred and fifty men and 450 carters were employed..." | 1887 Montreal snow removal debate in city council; all three labeled labels are plausible | OC, OO |
| D17 | wximpactbench-1386 | Ex. 12 (id=87) | all zeros | "PETER MARTIN, GAZETTE Workers from the Connecticut Light and Power Co were working to reconnect power lines on Oxford Ave in Notre Dame de Grace... Temperatures plummet; today's high minus-15C... more than one million people struggle on without power or heat" | 1998 Quebec ice storm coverage describing power outages and extreme cold; labeled all-zero — potential annotation gap | OC, OO |
| D18 | wximpactbench-1386 | Ex. 23 (id=225) | agricultural=1, human_health=1 | "more than 100,000 homes damaged and crops on about 175,000 hectares of farmland destroyed... death toll in Chongqing in China's southwest rose to 42 people and 12 missing from torrential downpours" | 2007 global flood roundup (England, China, Pakistan) — non-Canadian events used as positive examples | IC, IO |
| D19 | wximpactbench-1386 | Ex. 26 (id=215) | political=1, ecological=1 | "A line of freak thunderstorms rumbling across the northeastern Mediterranean coast from Spain and southern France to the principality of Monaco brought two days of disastrous flash flooding... Raging waters uprooted trees and swept away cars as river levels rose by as much as 3 metres" | Mediterranean flooding; ecological and political labels assigned; non-Canadian geography | IC, OC |
| D20 | wximpactbench-1386 | Ex. 27 (id=101) | ecological=1 | "The Everglades ecosystem is not ranked as an equal partner with agricultural and urban demands... about half the original 1.6-million-hectare swamp filled for development or drained for agriculture" | US ecological/conservation article (Everglades, drought context); ecological impact labeled | IO, OC |
| D21 | wximpactbench-1386 | Ex. 8 (id=138) | infra=1, human_health=1 | "hundreds of houses, schools and other buildings sustained damage when one of the twin peaks of the volcano exploded. At least 20 people sustained minor injuries... The most powerful earthquake to strike western Washington state in 30 years injured four people" | 1999 global disaster roundup (Indonesia, Washington state, NZ, Romania); labeled positive | IC, IO |
| D22 | wximpactbench-1386 | Ex. 7 (id=88) | infrastructural=1 | "Almost 4 million people across China had been cut off by flood waters, 810,000 homes have collapsed and 2.8 million homes have been damaged in eight provinces... Japan struck at young and old yesterday, killing a schoolgirl and an 85-year-old woman" | 1996 China Yangtze floods + Japan E. coli outbreak in same chunk; infrastractural=1 but human_health=0 despite explicit casualties | OC, OO |
| D23 | wximpactbench-1386 | Ex. 16/30/24/1 (id=198, multiple) | all zeros | "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25..." / "Escenvt 115780 298 J80 289 19 Caiunoil 8000 J9 J9 29..." | OCR-corrupted stock market tables; repeated for same article id across multiple rows | IF, IC |
| D24 | wximpactbench-1386 | Ex. 10 (id=304) | all zeros | "After the accident they suffered severely from the cold... All their provisions, anchor, cooking utensils, signal lights, and several other articles which were not lashed to the boat were lost." | 1896 transatlantic rowboat adventure; cold/weather mentioned in passing; long chunk heavily dominated by stock listings and patent medicine ads | IF, IC |
| D25 | wximpactbench-1386 | Ex. 18 (id=197) | all zeros | "The walkout will interrupt regular garbage collection and will affect street and sidewalk cleanup if it snows... Unless nine centimetres or more of snow falls during the walkout, blue-collar workers aren't obliged to clean the streets and sidewalks." | 1991 Montreal labor dispute about snow removal thresholds; weather mentioned indirectly; all-zero label | OC, OO |
| D26 | wximpactbench-1386 | Ex. 22 (id=183) | all zeros | "the peninsula - the tongue of land that juts toward South America - has been hit by greater warming than almost any other area on Earth" | 2009 climate change article about Antarctic Peninsula warming; no direct societal impact labeled despite ecological relevance | OC, OO |
| D27 | wximpactbench-1386 | Ex. 6 (id=252) | all zeros | "A poor lady passenger was dashed to leeward and had her skull fractured. She was landed this morning in a dying state with a coffined child that succumbed last night to its sufferings." | 1881 Atlantic storm with explicit casualties (skull fracture, child death) labeled all-zero | OC, OO |
| D28 | wximpactbench-1386 | Ex. 20 (id=15) | all zeros | "pointing out the impossibility of making satisfactory quotations for New York exchange... the movement of the crops, which, under the present circumstances, will be a most troublesome proceeding" | 1893 banking/financial crisis article; agricultural (crop movement) and financial framing present but labeled all-zero | OC, OO |

---

### Deployment-Relevant Strengths

#### Strength 1: Six impact labels are operationally present and distinguishable in the data
- **Dimension(s):** IO, OO
- **Observation:** The sampled data contains positive examples for infrastructural (Ex. 3, 7, 8, 17), political (Ex. 14, 26), financial (Ex. 14), ecological (Ex. 26, 27), agricultural (Ex. 23), and human health (Ex. 8, 23) impacts, confirming that the benchmark's six label dimensions are not theoretical — they appear with varying frequency across both historical and modern articles.
- **Deployment relevance:** Argentine policy makers assessing disaster impact reports would plausibly use all six of these categories. The fact that real labeled examples exist for each provides a minimum empirical basis for evaluating LLM classification capability across the full output ontology.
- **Datapoint citations:**
  - [D14] Example 3 (train, infrastructural=1): "by six o'clock the electric car services in all the important points west of Toronto had been completely paralyzed" — positive infrastructural label grounded in explicit service disruption text
  - [D16] Example 14 (train, infra=1, political=1, financial=1): "Already $30,000 has been expended in removing it, and they did not know what to do even now" — multi-label case demonstrating simultaneous financial + political + infrastructural assignment
  - [D18] Example 23 (train, agricultural=1, human_health=1): "crops on about 175,000 hectares of farmland destroyed...death toll in Chongqing in China's southwest rose to 42 people" — agricultural and health co-occurrence present in data

#### Strength 2: Negative-example chunks are genuinely diverse and challenging
- **Dimension(s):** IO, IF
- **Observation:** The mixed-context chunking strategy produces a large variety of zero-label examples spanning weather forecast tables (Ex. 1), crossword clues (Ex. 2), film reviews (Ex. 7/19), sports coverage (Ex. 9/28), political reporting (Ex. 5/29/31), legal proceedings (Ex. 4), and stock market tables (Ex. 16/30). These negative examples make the classification task non-trivially hard and prevent models from using simple keyword cues.
- **Deployment relevance:** In the Argentine deployment, the system must distinguish real disaster impact signals from noise across heterogeneous source channels. The benchmark's inclusion of topically diverse negative examples exercises a similar noise-rejection capability.
- **Datapoint citations:**
  - [D2] Example 2 (train, all zeros): "She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9) Down 1, Full of ill-will and disease (9)" — crossword puzzle text that shares no surface features with disaster reporting
  - [D7] Example 19 (train, all zeros): "National Lampoon's Van Wilder 2: The Rise of Taj Starring: Kal Penn, Lauren Cohan and Daniel Percival Playing at: AMC, Brossard, Cavendish, Colossus, LaSalle cinemas." — film review; tests model's resistance to false-positive labeling
  - [D10] Example 29 (train, all zeros): "Kennedy dramatically quit the race after only the second ballot, instantly propelling Dion into first place" — political content that might confuse political impact classification

#### Strength 3: Multi-label complexity provides a realistic evaluation of joint classification difficulty
- **Dimension(s):** OO, OF
- **Observation:** Several examples in the sample exhibit multi-label ground truth (e.g., Ex. 14 with three simultaneous positive labels; Ex. 23 with two), while the majority are all-zero. This mirrors the real task structure that Argentine policy users would face when a single report contains mixed signals across impact types.
- **Deployment relevance:** Disaster reports in Argentina (e.g., AMBA flooding triggering both infrastructure damage and health risks) would require simultaneous multi-label assessment; the benchmark exercises this capability.
- **Datapoint citations:**
  - [D16] Example 14 (train, infra=1, political=1, financial=1): "Aid Laurent said that there were mountains of snow all over the city. Already $30,000 has been expended in removing it" — three-label case
  - [D18] Example 23 (train, agricultural=1, human_health=1): "crops on about 175,000 hectares of farmland destroyed...death toll in Chongqing...rose to 42 people" — two-label case with different category combination

#### Strength 4: Both historical and modern-period articles are present, covering two linguistic registers
- **Dimension(s):** IF, IC
- **Observation:** The sample includes articles dated from 1881 to 2009, with time_period labeled "historical" or "modern." Historical texts (Exs. 3, 6, 10, 14, 17) use ornate 19th-century prose with archaic spelling and syntax; modern texts (Exs. 7, 18, 22, 23) use contemporary journalistic register. This variation exercises LLM linguistic robustness.
- **Deployment relevance:** While neither register matches contemporary Argentine informal social media, the two-period design at least probes whether LLM performance degrades with register shift — a methodologically relevant question for any register-mismatched deployment.
- **Datapoint citations:**
  - [D14] Example 3 (train, historical, 1894): "Sunday evening's despatches brought the news that a very severe blizzard was prevailing in Kansas" — archaic vocabulary and syntax
  - [D18] Example 23 (train, modern, 2007): "Military helicopters have rescued more than 100 people from rooftops, trailer parks and a bridge as well as strips of land cut off by water" — contemporary wire-service register

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Extremely high proportion of zero-label off-topic chunks undermine benchmark relevance signal
- **Dimension(s):** IO, IC
- **Observation:** Of 31 sampled examples, at least 20 (≈ 65%) are all-zero and contain content that is not merely low-impact weather reporting but is entirely unrelated to weather or disaster: crossword puzzles (Ex. 2), film reviews (Ex. 7/19), crime reporting (Ex. 4), sports coverage (Ex. 9/28), stock market tables (Exs. 16, 23, 30), political leadership contests (Exs. 5, 29), and legal proceedings (Ex. 4). These chunks apparently result from the mixed-context segmentation of full newspaper pages, where LDA topic selection operated at the article level but chunking produces segments from adjacent, unrelated page content.
- **Deployment relevance:** For the Argentine policy deployment, the benchmark's headline claim is that it evaluates LLM capability on disaster impact classification. If the majority of test examples are chunks of crossword clues and stock tickers with a trivially correct all-zero label, the benchmark's discriminative validity for impact classification is substantially diluted. A model that outputs all-zero for every input would achieve high accuracy on these examples. This casts doubt on whether benchmark scores reflect genuine disaster-impact understanding.
- **Datapoint citations:**
  - [D2] Example 2 (train, all zeros): "She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9) Down 1, Full of ill-will and disease (9) 2, There's a place for Belgians up in Rumania (5)" — crossword puzzle; no conceivable weather-impact content
  - [D7] Example 19 (train, all zeros): "National Lampoon's Van Wilder 2: The Rise of Taj Starring: Kal Penn, Lauren Cohan and Daniel Percival Playing at: AMC, Brossard, Cavendish, Colossus, LaSalle cinemas. Parents' guide: Sexual content markers." — film review fragment
  - [D9] Example 28 (train, all zeros): "'He can get his fastball up to 93 (mph) and averages out at 90-91.'" — baseball scouting; no weather or disaster relevance
  - [D23] Examples 1/16/24/30 (train, all zeros, same id=198): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25..." — OCR-corrupted stock market tables repeated across multiple rows for the same article id

#### Concern 2: Multiple examples with identical article id across chunks indicate severe data leakage/duplication in the sampled rows
- **Dimension(s):** IF, OC
- **Observation:** Article id=198 (date=19920204) appears in at least four of the 31 sampled rows (Exs. 1, 15/16, 24, 30) with different text fragments but the same metadata. Article id=26 appears in at least two rows (Exs. 3, 17) and id=88 in at least two rows (Exs. 7, 28). This is expected by design (the 350 full articles are chunked into 1,386 segments), but means that a substantial fraction of sampled examples share underlying source article metadata. The id=198 chunks include weather forecast tables (all zeros) and OCR-corrupted stock listings (all zeros), confirming that the segmentation cuts across multiple unrelated page elements.
- **Deployment relevance:** For Argentine policy evaluation, benchmark score interpretability depends on whether positive-labeled chunks and negative-labeled chunks from the same underlying article are truly independent test items. They share OCR artifacts, temporal context, and annotator. Models with memory of earlier chunks from the same article may receive implicit contextual advantage not available in single-document deployment scenarios.
- **Datapoint citations:**
  - [D1] Example 1 (id=198, all zeros): "John's Cloudy -4 -4 United States Max Min Atlanta Cloudy 17 4" — weather table chunk
  - [D23] Example 16 (id=198, all zeros): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25" — stock table chunk from same article id
  - [D14] Example 3 (id=26, infra=1): "by six o'clock the electric car services in all the important points west of Toronto had been completely paralyzed" — positive chunk
  - [D15] Example 17 (id=26, infra=1): "TRAFFIC IS PARALYZED In Western Canadian Cities" — different chunk of same article, same label

---

#### MAJOR

#### Concern 3: Potential annotation errors on positive-content chunks labeled all-zero
- **Dimension(s):** OC, OO
- **Observation:** Several chunks contain content that prima facie warrants positive labels under the benchmark's own annotation guidelines but are labeled all-zero. (a) Ex. 12 (id=87, 1998 Quebec ice storm): describes over one million people without power/heat and temperatures of minus-30°C — which maps directly to the "Infrastructural Impact" criterion (interruptions to utilities; power supply). (b) Ex. 6 (id=252, 1881 Atlantic storm): describes a woman with fractured skull and a dead child after a storm — explicit casualties that map to "Human Health Impact" per criterion Q145 ("direct injuries or fatalities"). (c) Ex. 25 (id=197, 1991 Montreal labor strike): discusses snow removal thresholds and traffic disruption — borderline case but mentions explicit infrastructure service thresholds. These may reflect the independent chunk-level re-annotation policy (Q47), but they raise concerns about annotation consistency.
- **Deployment relevance:** If the benchmark contains systematic under-labeling of positive-content chunks, LLMs that correctly identify these impacts would be penalized as false positives, artificially suppressing recall metrics. For Argentine policy users who care about not missing disaster signals, benchmark recall figures may be underestimated.
- **Datapoint citations:**
  - [D17] Example 12 (train, id=87, all zeros): "more than one million people struggle on without power or heat... overnight lows in Montreal were expected to drop to minus-16 Celsius last night and tumble as far as minus-30C on the South Shore" — explicit utility outage and human exposure to dangerous cold; infra=0 and human_health=0
  - [D27] Example 6 (train, id=252, all zeros): "A poor lady passenger was dashed to leeward and had her skull fractured. She was landed this morning in a dying state with a coffined child that succumbed last night to its sufferings." — explicit casualties from a storm; human_health=0
  - [D25] Example 18 (train, id=197, all zeros): "The walkout will interrupt regular garbage collection and will affect street and sidewalk cleanup if it snows" — snow-triggered service disruption framed as labor context; infra=0

#### Concern 4: Inconsistent human-health labeling across co-occurring disaster content
- **Dimension(s):** OC, OO
- **Observation:** Ex. 7 (id=88, 1996) covers China Yangtze floods (explicitly "810,000 homes have collapsed" and "2.8 million homes have been damaged") alongside Japan E. coli outbreak deaths ("killing a schoolgirl and an 85-year-old woman"). Infrastructural=1 is assigned but human_health=0, despite explicit casualties from both flood and foodborne illness. By contrast, Ex. 8 (id=138, 1999) covering Indonesian volcanic eruption injuries receives human_health=1. The criterion for human health (Q145) includes "direct injuries or fatalities (including cases where zero or more casualties are explicitly mentioned)."
- **Deployment relevance:** Inconsistent health-impact labeling is directly relevant to the Argentine deployment, where human health impacts (flood casualties, disease outbreaks in villas miseria post-flooding) are a primary policy concern. Unreliable health-label ground truth would undermine the benchmark's validity for evaluating whether LLMs can detect this dimension.
- **Datapoint citations:**
  - [D22] Example 7 (train, id=88, infra=1, human_health=0): "Almost 4 million people across China had been cut off by flood waters... the food-poisoning outbreak gripping Japan struck at young and old yesterday, killing a schoolgirl and an 85-year-old woman, and bringing the death toll to seven" — explicit multi-country casualty content; human_health=0
  - [D21] Example 8 (train, id=138, infra=1, human_health=1): "At least 20 people sustained minor injuries, including some who were injured after falling off their motorbikes during the strong quake that accompanied the eruption" — minor injuries (20 people) labeled human_health=1

#### Concern 5: Non-Canadian global disaster content is labeled with benchmark's impact categories without geographic scope limitation
- **Dimension(s):** IC, OC
- **Observation:** Several positively-labeled examples describe disasters in China (Ex. 7: Yangtze floods), Pakistan (Ex. 23: flash floods), England (Ex. 23: flooding), Indonesia (Ex. 8: volcanic eruption), the US Pacific Northwest (Ex. 8: earthquake), and the Mediterranean (Ex. 26: thunderstorm flooding). These are reported in Montreal Gazette articles as international wire-service content. The benchmark's annotation guidelines do not restrict classification to Canadian events, meaning the label ontology has been applied to globally diverse disaster geographies. This partially mitigates the concern about purely Canadian framing — impact categories are applied to South/East Asian and European contexts — but the operationalization still reflects North American institutional annotation perspectives.
- **Deployment relevance:** The presence of non-Canadian labeled examples is actually somewhat positive for the Argentine deployment: it confirms the annotation categories are applied to internationally sourced disasters, not exclusively domestic Canadian events. However, none of the international events represent South American geography, Argentine disaster types, or Spanish-language source content.
- **Datapoint citations:**
  - [D18] Example 23 (train, agricultural=1, human_health=1): "the death toll in Chongqing in China's southwest rose to 42 people and 12 missing from torrential downpours that have affected up to 6.8 million people" — Chinese disaster labeled with benchmark categories
  - [D19] Example 26 (train, political=1, ecological=1): "A line of freak thunderstorms rumbling across the northeastern Mediterranean coast from Spain and southern France to the principality of Monaco brought two days of disastrous flash flooding to the resort region" — Mediterranean European disaster labeled; no North American event
  - [D21] Example 8 (train, infra=1, human_health=1): "Reports from Indonesia's Flores Island tell of moderate damage and minor injuries during the July 1 eruption of Mt. Lewotobi" — Indonesian volcanic event labeled

#### Concern 6: Literary/fictional storm passages and non-weather narrative fragments are present in the dataset
- **Dimension(s):** IO, IC
- **Observation:** Ex. 21 (id=330, historical, Thunder) contains what appears to be a Victorian serialized novel excerpt embedded in the newspaper: "Just two hours before this, in Richmond, the storm so long expected has broken forth in all its fury. Great flashes of blinding lightning intermingled with the grand roar of the thunder from on high; while ever and anon the passionate bursts of rain flung themselves against the window panes of the hotel, almost drowning the gay laughter and merry voices of those within." This is labeled all-zero and weather_type=Thunder, but the "storm" is clearly a literary/metaphorical device in a fictional narrative, not a real weather event. Models that detect the storm language as weather-relevant and assign impact labels would be penalized for false positives.
- **Deployment relevance:** In the Argentine deployment, social media content frequently employs weather metaphors, emotional storm language, or colloquial expressions ("tormenta política," "lluvia de críticas") that are not literal weather events. The presence of literary weather text in this benchmark provides some minimal analog to this figurative language challenge, but it is not the same as Argentine vernacular metaphor — it is 19th-century English Victorian fiction.
- **Datapoint citations:**
  - [D11] Example 21 (train, id=330, all zeros): "Just two hours before this, in Richmond, the storm so long expected has broken forth in all its fury. Great flashes of blinding lightning intermingled with the grand roar of the thunder from on high; while ever and anon the passionate bursts of rain flung themselves against the window panes of the hotel, almost drowning the gay laughter and merry voices of those within" — weather language is fictional narrative, not a real event; model must distinguish literal from literary

---

#### MINOR

#### Concern 7: OCR-corrupted stock market and financial table chunks are present as valid training/test rows
- **Dimension(s):** IF
- **Observation:** Multiple chunks (Exs. 1, 16, 24, 30) from the same article (id=198, 1992-02-04) contain heavily OCR-corrupted financial table data: "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25..."; "Escenvt 115780 298 J80 289 19 Caiunoil 8000 J9 J9 29..." These are not corrected by the post-OCR pipeline — they remain as garbled strings of numbers and partial tokens. They are labeled all-zero, which is correct, but they constitute noise inputs that neither resemble weather articles nor the Argentine deployment's social media/press content.
- **Deployment relevance:** These corrupted table chunks indicate that the post-OCR correction pipeline did not fully clean tabular or numerical page elements, and that such fragments appear in the benchmark as valid test items. This reinforces the concern that benchmark performance metrics are partly driven by trivially correct all-zero classifications of non-text content.
- **Datapoint citations:**
  - [D23] Example 16 (train, id=198, all zeros): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35 -1 Gift sir 14000 33 30 33 1 Aloha gld 10000 85 80 80 5 Clinedev 1600 0 0 0" — OCR garbage from financial tables; still included as benchmark row
  - [D23] Example 30 (train, id=198, all zeros): "Escenvt 115780 298 J80 289 19 Caiunoil 8000 J9 J9 29 Eurkav 6200 JO 18 18 Clgrphy 3100 345 330 345 5 Euroormf 10000 4 4 4" — second corrupted financial table chunk from same article

#### Concern 8: Zero-label climate/environmental context chunks that may matter for Argentine ecological framing
- **Dimension(s):** OC, OO
- **Observation:** Ex. 22 (id=183, 2009) describes Antarctic Peninsula warming with reference to South America: "the peninsula - the tongue of land that juts toward South America - has been hit by greater warming than almost any other area on Earth." This is labeled all-zero (ecological_impact=0). Under the benchmark's annotation criteria (Q143: "Classify as 'true' if the text mentions any effects on natural environments and ecosystems"), this passage describing measurable environmental change at scale plausibly warrants an ecological label, but it lacks an "immediate" weather event trigger. Similarly, Ex. 28 (id=15, 1893) contains agricultural movement context ("the movement of the crops, which, under the present circumstances, will be a most troublesome proceeding") linked to financial crisis, labeled all-zero.
- **Deployment relevance:** For Argentine ENSO-driven drought assessment, ecological and agricultural framing of longer-term climate dynamics (not a single acute event) is a key policy interest. If the annotation guidelines strictly exclude such content as "not direct and immediate," the benchmark may underrepresent the slow-onset disaster assessment tasks Argentine policy users face.
- **Datapoint citations:**
  - [D26] Example 22 (train, id=183, all zeros): "the peninsula - the tongue of land that juts toward South America - has been hit by greater warming than almost any other area on Earth" — large-scale ecological change, all-zero
  - [D28] Example 20 (train, id=15, all zeros): "the movement of the crops, which, under the present circumstances, will be a most troublesome proceeding, easy everywhere" — crop disruption in financial context, agricultural_impact=0

#### Concern 9: weather_type field is populated with "Nan" for a substantial proportion of examples
- **Dimension(s):** IO
- **Observation:** Of 31 sampled examples, 19 have weather_type="Nan" (not a weather type string, but the literal string "Nan" or null). Examples with weather_type populated (Snow, Rain, Drought, Freezing, Thunder, Cold, Deluge) tend to contain more weather-relevant content, but several weather_type="Nan" examples contain genuine weather content (e.g., Ex. 7 on China floods; Ex. 22 on Mediterranean flooding). The weather_type field does not appear to be a reliable metadata indicator of whether the chunk contains weather content.
- **Deployment relevance:** This metadata quality issue is minor for scoring but indicates that the benchmark's topic-modeling article selection (LDA-based, 15 weather event types per Q101) did not translate cleanly into chunk-level weather type metadata. For Argentine deployment validation purposes, this reduces the utility of the weather_type field as a stratification variable.
- **Datapoint citations:**
  - [D22] Example 7 (train, weather_type=Nan, infra=1): "Almost 4 million people across China had been cut off by flood waters" — flood content but weather_type=Nan
  - [D19] Example 26 (train, weather_type=Thunder, political=1, ecological=1): "A line of freak thunderstorms rumbling across the northeastern Mediterranean coast" — weather_type populated and consistent with content
  - [D3] Example 4 (train, weather_type=Nan, all zeros): "Clarkson was arrested July 16 as he left the Glenora home of Marilyn Tan" — no weather; weather_type=Nan correctly absent

---

### Content Coverage Summary

The 31 sampled examples from the mixed-context (1,386-sample) version of WXImpactBench are predominantly all-zero negative examples (≈65%), most of which contain content entirely unrelated to weather or disaster: sports coverage, film reviews, political news, crossword puzzles, and OCR-corrupted financial tables. This is an expected artifact of the chunking strategy — full newspaper pages are segmented into ~250-token chunks regardless of content type, meaning many chunks capture page elements (advertisements, stock tables, crossword grids, crime briefs) that co-occurred on the same page as a weather article selected by LDA.

The positively-labeled examples cover: North American historical blizzards (1894 Montreal/Ontario, labeled infrastructural), 19th-century Montreal snow removal debates (multi-label), 1990s–2000s global disaster round-up articles from the Montreal Gazette (China floods, Mediterranean flooding, Indonesian eruption, Pakistani flash floods), and US ecological articles (Everglades drought). The geographic and event-type diversity in positive examples is broader than "Canadian weather only" — it extends to international wire service content — but no South American, Argentine, or Spanish-language content appears.

Register is uniformly formal English journalism across both periods. Archaic 19th-century prose (ornate syntax, shipping reports, pharmaceutical advertisements) coexists with late-20th-century wire-service brevity. Neither register resembles the informal, social-media, short-form Rioplatense Spanish content that constitutes the Argentine deployment's highest-priority input channel.

Label consistency across positively coded examples raises reviewable questions: explicit casualties in an 1881 storm (fractured skull, child death) are labeled human_health=0; the 1998 Quebec ice storm with one million people without power is labeled infrastructural=0; while minor injuries in an Indonesian volcanic eruption are labeled human_health=1. These patterns are consistent with the chunk-level independent re-annotation design but indicate variability that downstream users should be aware of.

---

### Limitations

1. **Sample size:** 31 examples from a 970-row training split is a small sample (≈3.2%). The proportion of off-topic zero-label chunks observed here may be higher or lower in the full dataset; the rate of potential annotation inconsistencies cannot be reliably estimated from 31 examples.

2. **Train split only:** All sampled examples are from the `train` split. The `validation` and `test` splits (208 examples each) may have different proportions of positive labels or different content distributions; this cannot be assessed from the current sample.

3. **Long-context version not inspected:** Only the mixed-context (chunked, 1,386-sample) version is present in this dataset; the 350-sample long-context version (full articles) is not available here. The long-context version may exhibit fewer off-topic zero-label segments since each row is a complete article rather than a page fragment.

4. **Annotation guidelines not directly verifiable:** The apparent labeling inconsistencies identified (D17, D22, D27) cannot be definitively confirmed as errors without access to the full annotation guidelines and the complete article context for each chunk. Chunk-level re-annotation may have a documented rationale for some of these decisions that is not visible from the text alone.

5. **QA task not inspectable:** The ranking-based QA task (pseudo questions, candidate pools, retrieval scores) is not represented in this dataset; validity assessment of that task component is limited to documentation review.

6. **Non-text columns not reviewed:** The schema contains only text and integer label columns; no image or audio columns exist. Inspectability is complete for this modality.

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
  "benchmark": "wximpactbench",
  "region": "Argentine Government Disaster Reporting Reliability — Policy Staff",
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
