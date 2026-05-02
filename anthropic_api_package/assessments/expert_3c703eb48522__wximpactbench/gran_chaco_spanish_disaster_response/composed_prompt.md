I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **WXIMPACTBENCH: A Benchmark for Evaluating LLMs on Disruptive Weather Impacts** is valid for use in **Gran Chaco Tri-Border Emergency Response Zone**.

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
- **Domain**: Disaster weather impact classification and retrieval
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis

### 1. Input Ontology
WXIMPACTBENCH organizes its evaluation around six societal impact categories —
Infrastructural, Political, Financial, Ecological, Agricultural, and Human Health —
informed by prior disaster impact frameworks [Q11, Q25]. These categories are operationalized
with detailed definitions covering, for example, "structural damage to buildings, roads,
and bridges" under Infrastructural [Q135], "crop yield variations" and "disruptions to
food production" under Agricultural [Q136], and "government decision-making and policy
changes" under Political [Q140]. Topic modeling using LDA was used to categorize the
underlying corpus into 15 primary weather event types before article selection [Q101],
providing a second layer of taxonomic structure. The benchmark supports zero-shot and
one-shot in-context learning variants [Q112, Q113, Q114].

From an input ontology standpoint, these six categories are broad enough to nominally
subsume flooding and fire events, but the taxonomy was designed exclusively for Canadian
weather-impact journalism. Gran Chaco-specific event consequences — locust outbreaks,
cross-border displacement along the Pilcomayo and Bermejo rivers, disruption to
strategic economic routes, or barriers to indigenous community access — are absent from
the definitional scope. The 15 LDA-derived weather event types were derived from
Canadian newspaper content [Q97, Q101] and make no reference to event types characteristic
of South American semi-arid disaster contexts. The benchmark's two evaluation tasks
(multi-label classification and ranking-based QA) [Q3, Q15] are well-specified but
do not include any event categories structured around cross-border dynamics or
indigenous territory access — damage patterns the Gran Chaco deployment explicitly
prioritizes.

### 2. Input Content
The benchmark's data originates from a corpus of three digitized historical Canadian
newspapers — La Presse, La Patrie, and the Montreal Gazette — accessed through
collaboration with the McGill University Library and Archives and the Bibliothèque
nationale du Québec [Q97]. Articles were drawn from two distinct temporal periods to
capture linguistic and social change [Q13], and the full pipeline begins with OCR-extracted
text yielding an initial corpus of 4,018 entries [Q20], filtered to 350 high-quality
annotated samples for the long-context version and 1,386 for the mixed-context version
[Q49, Q121, Q122]. GPT-4O was used for OCR post-correction [Q12] and pseudo-question
generation [Q59], and the benchmark's coverage of climate events was described as
recording "how communities adapted and recovered from disasters" [Q4]. The authors
acknowledge that "WXIMPACTBENCH may have potential biases in underrepresented historical
events and linguistic variations" [Q90] and that "the interpretation of weather-related
disruptions in historical newspapers might be influenced by demographic and contextual
factors" [Q96].

For the Gran Chaco deployment context, this represents a profound input content mismatch.
The benchmark's entire empirical base consists of formal English-language Canadian
newspaper prose [Q14], with no Spanish-language content, no social media text, and no
material reflecting the indigenous-language lexical borrowing (Guaraní, Quechua, Wichí)
that characterizes target deployment inputs. The institutional sources — a Quebec archive
and McGill University Library [Q97] — are geographically and culturally distant from
Northwest Argentina, Paraguay, and South Bolivia. No data from Southern Cone emergency
or disaster reporting contexts is represented anywhere in the corpus, and the stated
limitation on "linguistic variations" [Q90] does not extend to acknowledgment of
non-English or non-Canadian contexts.

### 3. Input Form
The benchmark's input data is English-language text derived from OCR-processed historical
newspaper scans, with historical newspapers described as employing "more descriptive and
elaborate narratives compared to modern reporting styles" with "outdated terminology,
spelling variations, and evolving writing conventions" [Q14]. Models are required to
"understand the linguistic shifts between historical and modern texts" [Q32]. The
long-context version averages 2,987.4 tokens per article and the mixed-context version
averages 781.3 tokens [Q109]; the mixed-context version is created by segmenting articles
into approximately 250-token chunks [Q46]. All evaluated models are required to support
input lengths of at least 8k tokens [Q55], and the structured, formal narrative style of
historical reporting is noted as making cause-and-effect relationships more explicit —
and thus somewhat easier for models to classify [Q83, Q84].

From an input form perspective, this format represents a severe mismatch with the Gran
Chaco deployment. The benchmark processes formal, lengthy English newspaper prose
exclusively, whereas the deployment requires processing informal Rio Platense Spanish
social media posts and local news fragments that may contain platform abbreviations,
indigenous-language place names, code-switching, and non-standard orthography. The token
length distribution [Q120] reflects long-form journalistic texts, not the short,
high-urgency posts typical of active disaster events. No preprocessing or evaluation
framework in the benchmark addresses transliteration, script normalization, or handling
of indigenous-language lexical items within Spanish text.

### 4. Output Ontology
The benchmark defines six binary impact labels — Infrastructural, Agricultural,
Ecological, Financial, Human Health, and Political — applied to each article [Q25, Q103,
Q133]. Each label is binary, indicating presence or absence of direct descriptions of a
specific impact [Q27, Q108], and an article may carry multiple labels simultaneously
[Q28]. Detailed operationalized definitions are provided for each category in both the
annotation guidelines [Q135–Q140] and the LLM prompting instructions [Q141–Q146].
The prompt instructs models to "return 'false' for any impact category that is either
not present in the text or not related to weather events" and to "base classifications
on explicit mentions in the text" [Q147]. The ranking-based QA task uses the same
annotated categories to structure generated questions [Q40].

For the Gran Chaco deployment, output ontology validity is substantially compromised.
The label boundaries reflect Canadian journalistic framing of weather impacts, not the
consequence-framing logic that Gran Chaco national coordinators would apply. The same
event — a flooded dirt road blocking access to an indigenous community — could be
assigned Infrastructural, Human Health, or Agricultural labels depending on the
reported consequences, but the benchmark's definitions emphasize "explicit mentions"
and direct physical effects [Q141–Q145] without a mechanism for consequence-framing
ambiguity. The Political category [Q140, Q146] does not include border integrity or
cross-border displacement as exemplars. No category addresses strategic economic route
disruption or indigenous territory access barriers — damage types the Gran Chaco
deployment explicitly prioritizes. The binary true/false operationalization [Q117] also
does not expose confidence gradations that would help national coordinators assess
ambiguous multi-label cases.

### 5. Output Content
Annotation was conducted by three domain experts following structured guidelines reviewed
by meteorological experts [Q26, Q104, Q105]. Annotators were tasked with determining
whether articles contain descriptions corresponding to each of the six impact categories,
"focusing on direct and immediate effects and explicit references" [Q107, Q118]. The
annotation process was conducted by members of a research group specializing in
"uncovering the history of a region's climate change through the regional historical
weather records" [Q110], whose expertise was considered sufficient to ensure accuracy
and reliability [Q111]. For the mixed-context (chunked) dataset, annotations were
performed independently by the same domain experts [Q47, Q48], and a post-OCR
correction quality check evaluated GPT-4O output against human-annotated corrections
on 50 randomly selected articles [Q98]. The guidelines emphasize applying meteorological
expertise beyond provided examples [Q134], and no inter-annotator agreement statistics
are reported in the paper.

From an output content validity perspective, this annotation process is entirely
disconnected from the Gran Chaco deployment context. The annotators are Canadian academic
researchers specializing in historical climate analysis [Q110], not Southern Cone national
emergency coordinators, gendarmerie, or civil protection practitioners. The user identified
national coordinators in Buenos Aires as the authoritative labelers for the target
deployment — a population with zero representation in the benchmark's annotation process.
The absence of inter-annotator agreement statistics makes it impossible to assess label
reliability even within the Canadian context. The guidelines' emphasis on "explicit
mentions" [Q118] and direct physical effects may not align with the consequence-framing
logic Gran Chaco responders apply, where salience depends on operational implications
for resource allocation rather than textual explicitness.

### 6. Output Form
For the multi-label classification task, the benchmark uses F1-score, accuracy, and
row-wise accuracy as primary metrics [Q43], averaged across the six impact categories,
temporal periods, and context lengths [Q44]. Row-wise accuracy requires correct
classification of all six labels simultaneously [Q45, Q75], and results show classification
performance drops dramatically under this strict metric [Q68]. For the ranking-based QA
task, standard retrieval metrics are used: Hit@1, nDCG@5, Recall@5, and MRR [Q50],
with a sliding window mechanism to reduce noise from long contexts [Q60]. Experimental
results are averages over three runs with temperature set to 0 [Q62], and the same
annotation guidelines used for human labeling are embedded in LLM prompts [Q106].
The binary output format instructs models to return true/false for each category and
base classifications on text-internal evidence [Q147]. Evaluation costs are approximately
$3 for classification and $5.5 for ranking per proprietary model run [Q126], with
open-source models evaluated on dual NVIDIA A6000 GPUs [Q127].

For the Gran Chaco deployment, output form alignment is partial but imperfect. The
multi-label simultaneous classification output [Q57] corresponds to the minimum acceptable
output form identified by the deployment user, who explicitly rejected ranked outputs as
insufficiently reliable for direct operational use. However, the benchmark's scoring
metrics (F1, row-wise accuracy) do not distinguish between the needs of field gendarmes
requiring rapid event-specific lookup and national coordinators requiring aggregate
situational awareness across multiple concurrent events. The evaluation framework reports
no confidence scores or probability distributions, which would be necessary for the
human-review-mediated use the user described as appropriate for ranking outputs. The
ranking task's known self-referential bias — inflated performance when the question
generator and ranker are the same model [Q88] — further complicates interpretation of
QA results.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we first develop a disruptive weather impact dataset with a four-stage well-crafted construction pipeline." |
| Q2 | 1 | input_ontology | "we propose WXIMPACTBENCH, the first benchmark for evaluating the capacity of LLMs on disruptive weather impacts." |
| Q3 | 1 | input_ontology | "The benchmark involves two evaluation tasks, multi-label classification and ranking-based question answering." |
| Q4 | 1 | input_content | "The climate-related events stored in regional newspapers record how communities adapted and recovered from disasters." |
| Q5 | 1 | input_form | "However, the processing of the original corpus is non-trivial." |
| Q6 | 1 | output_form | "Extensive experiments on evaluating a set of LLMs provide first-hand analysis of the challenges in developing the understanding of disruptive weather impact and climate change adaptation systems." |
| Q7 | 1 | output_content | "Yongan Yu1, Qingchen Hu1, Xianda Du2, Jiayin Wang3, Fengran Mo4∗, Renée Sieber1*" |
| Q8 | 1 | output_content | "1McGill University, 2University of Waterloo, 3Tsinghua University, 4University of Montreal" |
| Q9 | 1 | input_form | "the challenge of identifying impacts and responses often lies in climate-related text processing, which contains period-specific narratives and domain-specific linguistic phenomena." |
| Q10 | 1 | input_form | "This polysemy occurs commonly in newspapers and thus requires the system to distinguish the literal weather-related meanings and alternate usages by improving the" |
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
| Q37 | 5 | output_form | "This setting could also facilitate RAG systems development in the domain (Mao et al., 2024; Mo et al., 2024c, 2025), where we left the answer span extraction/generation for future studies." |
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
| Q54 | 6 | output_form | "The relatively smaller models (with 7B size) ensure the latency requirements (Sun et al., 2023)." |
| Q55 | 6 | input_form | "The used models for the two tasks cover different sizes and support the input length of at least 8k tokens." |
| Q56 | 6 | input_form | "The multi-label classification is conducted on each evaluated LLM by the same prompt provided in Appendix C.2." |
| Q57 | 6 | output_ontology | "Different from traditional methods that decompose multi-label text classification into multiple binary classification tasks (Boutell et al., 2004; Liu et al., 2017), we simultaneously identify all relevant disruptive weather impacts for each input by calling the LLM once." |
| Q58 | 6 | input_form | "The example of in-context learning in the one-shot setting is handcrafted with a complex sample detailing multiple impacts." |
| Q59 | 6 | input_content | "We employ GPT-4O for pseudo question generation with default hyper-parameters." |
| Q60 | 6 | output_form | "For ranking evaluation, we adopt the sliding window mechanism within LLM-based ranker implementation following the state-of-the-art study (Sun et al., 2023) to reduce the potential negative effect of noisy long contexts." |
| Q61 | 7 | input_form | "Specifically, each article in the candidate pool was segmented into three chunks, and then the initial ranking was performed independently within each chunk." |
| Q62 | 7 | output_form | "To ensure stable results, following previous studies (Chen et al., 2023), all LLMs were evaluated with the temperature set to 0, and the reported performance is the average value of running the experiments three times." |
| Q63 | 7 | output_form | "Table 1 and Table 2 show the performance of the evaluated LLMs on WXIMPACTBENCH for the settings of categorized by six societal impacts with different context lengths, overall row-wise evaluation, and divided into two periods, respectively." |
| Q64 | 7 | output_form | "LLMs struggle to understand disruptive weather impacts." |
| Q65 | 7 | output_form | "Table 1 shows that the F1-score for multi-label classification remains consistently low across models, especially among the political and ecological categories." |
| Q66 | 7 | output_form | "The financial, agricultural, and human health impacts categories perform slightly better but still exhibit suboptimal results at 55%." |
| Q67 | 7 | output_ontology | "The low performance might be attributed to the challenges in these categories with abstract and context-dependent narratives." |
| Q68 | 8 | output_form | "Table 2 shows row-wise performance, in which the model must identify the given sample correctly for each involved category, the performance of classification drops dramatically due to the more precise requirement." |
| Q69 | 8 | output_ontology | "Thus, a sophisticated model is expected to understand the complex societal effects of historical narratives via reasoning (Wei et al., 2022; Zhang et al., 2025a,b)." |
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
| Q88 | 9 | output_form | "Notice that the ranking results would contain bias when the evaluated model is used for question generation (GPT-4O in our cases). This is a common phenomenon (Zhou et al., 2023) and needs to be avoided in benchmarking." |
| Q89 | 9 | output_form | "The practical open-retrieval setting, i.e., identifying the relevant articles from a huge database, is left for future studies, which could further facilitate knowledge enhancement in understanding disruptive weather impacts." |
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
| Q102 | 14 | input_ontology | "In the absence of standardized impact records (e.g., flood-related property damage, injuries due to ice accumulation, power outages, and road closures), we assessed vulnerabilities and resilience based on the consequences of weather events and how they have changed since the 19th century." |
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
| Q118 | 16 | output_content | "The guidelines emphasize focusing on direct and immediate effects, ensuring that classifications are based solely on explicit references within the text." |
| Q119 | 16 | input_ontology | "The ranking-based QA task consists of two key components: question generation (Mo et al., 2023) and candidate ranking (Meng et al., 2024)." |
| Q120 | 16 | input_form | "Figure 6 presents the token length distribution of passages in two versions of our dataset: (a) the Long Context dataset and (b) the Mixed Context dataset used for context-denoising evaluation." |
| Q121 | 16 | input_content | "The Long Context dataset (Figure 6a), which contains 350 articles, exhibits a broader distribution of passage lengths, with a significant portion exceeding 2000 tokens." |
| Q122 | 16 | input_content | "The Mixed Context dataset (Figure 6b), which contains 1,386 articles, is heavily skewed toward shorter passages, with an overwhelming majority containing fewer than 2000 tokens." |
| Q123 | 16 | output_content | "GPT-4O, GPT-4 and GPT-3.5-TURBO are provided by OpenAI, the base model API document: https://platform.openai.com/docs/models" |
| Q124 | 16 | output_content | "DEEPSEEK-V3-671B is upgraded the DEEPSEEK-CHAT, the base model API" |
| Q125 | 17 | input_ontology | "Given the following passage about {row['Weather']}, generate a single, focused question that meets these criteria: 1. Can be answered using ONLY the information in this passage 2. Focuses on the {impact_str} impacts mentioned 3. Is detailed and specific to this exact situation 4. Requires understanding the passage's unique context 5. Cannot be answered by other similar passages about {row['Weather']} Passage: {row['Text']}" |
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
name: Gran Chaco Tri-Border Emergency Response Zone
abbreviation: GranChaco-TriBorder
deployment_context:
  use_case: AI-assisted disaster damage-type identification from local Spanish-language
    news and social media posts, supporting triage and routing of information during
    active disaster events in the Gran Chaco tri-border region.
  system_role: Multi-label classification of incoming text by societal impact category
    (Infrastructural, Agricultural, Ecological, Financial, Human Health, Political),
    with potential extensions for operational routing.
  benchmark_being_assessed: wximpactbench
geography:
  primary_zone: Gran Chaco tri-border region spanning Northwest Argentina, Gran Chaco
    Paraguay, and South Bolivia
  constituent_jurisdictions:
    argentina:
      provinces:
      - Salta
      - Formosa
      - Chaco
      notes: Salta is the primary provincial hub for Northwest Argentina; Formosa
        and Chaco provinces extend into the lowland Chaco. Sub-national institutional
        structures, infrastructure, and dialect variation across these provinces are
        significant and underdocumented in the benchmark.
    paraguay:
      departments: 'The three Gran Chaco-side departments are Boquerón, Alto Paraguay,
        and Presidente Hayes. Boquerón (capital: Filadelfia) borders Bolivia to the
        north and Argentina (via the Pilcomayo) to the south; it is the largest department
        by area (~91,000 km²) and is home to Mennonite colonies and multiple indigenous
        communities. Alto Paraguay (capital: Fuerte Olimpo) is the most sparsely populated.
        Presidente Hayes (capital: Villa Hayes) borders Formosa province of Argentina
        via the Pilcomayo River and is the most populous of the three. All three departments
        have been declared under national emergency status repeatedly (e.g., Ley Nº
        4615/2012 for flooding, Ley Nº 7222 for drought, and Ley Nº 7471/2025 for
        flooding). The SEN (Secretaría de Emergencia Nacional) is the primary emergency
        authority for all three. Source: Bacn.gov.py — [WEB-1];
        Wikipedia Presidente Hayes Dept — [WEB-2]'
      notes: Paraguayan Chaco is among the most sparsely populated sub-regions; institutional
        presence is thin outside Villa Hayes and Filadelfia. Route No. 12 along the
        Pilcomayo is impassable when raining, directly reflecting the Infrastructural
        impact category for this deployment. SEN has active operations in all three
        departments (Alto Paraguay, Boquerón, Presidente Hayes) for both flood and
        drought events as recently as April–May 2026.
    bolivia:
      departments: 'The relevant South Bolivia departments for the Gran Chaco zone
        are Tarija (containing the Bolivian Chaco lowlands and the Gran Chaco province
        centered on Yacuiba), and the southern fringe of Santa Cruz (Cordillera province).
        Chuquisaca has minimal Chaco footprint. Tarija is the primary hub; Yacuiba
        is the main border town facing Argentina. The Pilcomayo originates in the
        Oruro highlands and the Bermejo forms the Tarija–Argentina border. Source:
        VIDECI/Bolivia disaster documentation — [WEB-3];
        UNISDR Bolivia Document — [WEB-4]'
      notes: Bolivian Chaco includes indigenous Guaraní-speaking communities (Ava
        Guaraní/Chiriguano in Tarija) and is distinct from the Andean Quechua-speaking
        areas also represented in the broader deployment population. VIDECI has departmental
        representations in Tarija covering these Chaco zones.
  settlement_typology:
    semi_urban_provincial_centers: 'Key nodes for information aggregation and institutional
      response (e.g., Salta city, Tartagal, Embarcación in Argentina; Villa Hayes
      and Filadelfia in Paraguayan Chaco; Yacuiba in Bolivian Chaco). Source: IDB
      Gran Chaco PROADAPT — [WEB-5]'
    rural_communities: Dispersed agrarian and ranching settlements connected by dirt
      roads (ripio/tierra); flood-vulnerable and seasonally isolated
    indigenous_territories: Wichí, Guaraní-speaking, and Quechua-speaking communities;
      may have distinct communication channels, languages, and access constraints;
      road access frequently disrupted by flooding events
  key_waterways:
  - Pilcomayo River (Argentina/Paraguay border)
  - Bermejo River (Argentina/Bolivia border)
  border_salience: 'International borders of operational significance: the Pilcomayo
    and Bermejo rivers are both flood corridors and jurisdictional boundaries. Cross-border
    displacement and border integrity are primary disaster news categories for responders
    in this zone.'
  gran_chaco_population_context: 'The Gran Chaco region is home to over 7 million
    people, of whom approximately 8% are indigenous peoples; many engage in agriculture,
    livestock, beekeeping, and handcrafts. The Pilcomayo River basin covers approximately
    50,000 km² in the lower reach alone, making coordinated alert and reporting across
    all communities extremely difficult. Source: WRI — [WEB-6];
    IDB — [WEB-5]'
target_population:
  description: National emergency responders, gendarmerie, civil protection forces,
    and technical practitioners who use the AI system to triage and classify disaster
    damage reports during active events in the Gran Chaco tri-border zone. Users range
    from field gendarmes needing rapid event-specific lookups to national coordinators
    in Buenos Aires requiring aggregate situational awareness across concurrent events.
  user_roles:
    field_gendarmes:
      location: Deployed in the field across Salta, Formosa, Chaco provinces and tri-border
        zone
      output_needs: Fast, event-specific lookup during ongoing incidents (e.g., locating
        stranded vehicles, school buses, flooded communities); needs low latency and
        high precision on individual events
      technical_profile: '[NEEDS VERIFICATION — deferred: likely unsearchable (operational
        security detail); field connectivity in this zone is known to be unreliable
        — see infrastructure_notes.connectivity]'
    national_coordinators:
      location: Buenos Aires (national coordination center) and potentially provincial
        capitals
      output_needs: Aggregate, scalable multi-label output for resource allocation
        decisions across multiple concurrent events; authoritative labelers for ground-truth
        in this deployment
      technical_profile: '[NEEDS VERIFICATION — deferred: low impact for scoring;
        standard government dashboard infrastructure likely, but no public documentation
        found]'
    civil_protection_technicians:
      location: Provincial and departmental offices across the tri-border zone
      output_needs: Intermediate between field gendarmerie and national coordinators;
        may triage incoming social media feeds
      technical_profile: '[NEEDS VERIFICATION — deferred: likely unsearchable (sub-national
        operational detail)]'
  authoritative_labelers: National coordinators in Buenos Aires are designated as
    the authoritative ground-truth labelers for this deployment. This population has
    zero representation in the wximpactbench annotation process.
  english_proficiency: Intermediate English proficiency noted for technical practitioners,
    but the system operates exclusively in Spanish.
languages:
  primary_operational_language: Rio Platense Spanish (Rioplatense dialect, including
    Northwest Argentine regional variation)
  regional_vocabulary_notes: 'The target text corpus is Spanish but routinely includes:

    - Place names (toponyms) derived from Guaraní, Quechua, and Wichí (e.g., Pilcomayo,
    Bermejo, Tartagal, Embarcación, Yacuiba)

    - Common nouns and descriptors borrowed from indigenous languages into regional
    Spanish

    - Platform-specific abbreviations and informal orthography characteristic of social
    media (WhatsApp, Twitter/X, Facebook groups used for community reporting)

    Full code-switching into indigenous languages is not the primary use case, but
    lexical borrowing is routine and must be handled correctly by any evaluated model.'
  rioplatense_distribution_note: 'Rioplatense Spanish is the predominant variety in
    Argentina and Uruguay, centered in major urban areas (Buenos Aires, Rosario) but
    extending to parts of Paraguay and border regions. Northwest Argentine Spanish
    (Salta, Formosa, Chaco) shares voseo and some phonological features but carries
    stronger indigenous-language substrate influence than coastal Rioplatense. Many
    Rioplatense features are shared with varieties spoken in south/east Bolivia and
    Paraguay border regions. Source: Wikipedia Rioplatense Spanish — [WEB-7]'
  indigenous_languages_present_in_region:
    wichi:
      speaker_population: 'Wichí is classified within the Mataco-Mataguaya family
        and is spoken in Formosa, Salta, and Chaco provinces of Argentina. The 1985
        Aboriginal Census of Chaco province recorded 3,143 Wichís; the 1984 Salta
        census recorded 9,143 Wichís. Current estimates are higher but no single authoritative
        post-2010 census figure was found for this specific language. 13 Wichí communities
        are recorded in Formosa and Salta combined. Note: census figures likely underestimate
        speakers due to questionnaire design issues. Source: Indigenous Peoples of
        Argentina (AcademiaLab) — [WEB-8];
        Survey of NLP resources for Argentine indigenous languages (arXiv 2501.09943)
        — [WEB-9]'
      territory: Primarily Northwest Argentina (Salta, Formosa, Chaco provinces)
      relevance_to_system: Wichí place names and occasional vocabulary appear in Spanish-language
        social media posts about events affecting Wichí communities; not a primary
        system input language
    guarani_chaqueno:
      speaker_population: 'In Argentina, Chaco Guaraní varieties include Ava Guaraní
        (Chiriguano), Tapiete, and Mbyá Guaraní, primarily in Formosa, Salta, and
        Jujuy provinces. Paraguayan Guaraní is the national language of Paraguay with
        over 6 million speakers; the Paraguayan Chaco departments have Guaraní-speaking
        indigenous communities alongside mestizo and Mennonite populations. Bolivia''s
        Chaco (Tarija/Gran Chaco province) has Ava Guaraní-speaking communities (Chiriguano).
        No single regional count was found for the tri-border zone; national-level
        figures substantially exceed sub-regional availability. Source: NLP Progress
        in Indigenous Latin American Languages (arXiv 2404.05365) — [WEB-10];
        Survey of Argentine indigenous NLP (arXiv 2501.09943) — [WEB-9]'
      territory: Paraguayan Chaco, South Bolivia, Formosa and Chaco provinces of Argentina
      relevance_to_system: Guaraní-derived place names are ubiquitous across the region;
        Paraguayan sources may include more Guaraní lexical mixing given national
        bilingualism. The Guaraní-Spanish mixed variety ('Jopara') is characteristic
        of Paraguayan informal writing and may appear in social media from Paraguayan
        Chaco sources.
    quechua:
      speaker_population: 'Two Quechua varieties are present in Argentina: Cusco-Bolivian
        Quechua (spoken primarily by Bolivian/Peruvian immigrants) and Santiago del
        Estero Quichua. A Kolla Quechua variety is sometimes cited for Salta/Jujuy.
        The 2026 census data is not yet publicly consolidated; prior provincial censuses
        for Salta are outdated (1984). No authoritative current figure for Quechua
        speakers specifically in the Salta deployment zone was found. Source: Survey
        of Argentine indigenous NLP (arXiv 2501.09943) — [WEB-9]'
      territory: Primarily Salta province Andean areas and South Bolivia highland-lowland
        transition zone
      relevance_to_system: Quechua-derived toponyms and vocabulary appear in reports
        from Andean-adjacent areas of the deployment zone
  nlp_tool_availability:
    rio_platense_spanish: 'General Spanish NLP tools exist. The most directly relevant
      model for the deployment register is RoBERTuito (Pérez et al., LREC 2022), a
      RoBERTa-based model pre-trained on over 500 million Spanish tweets; it outperforms
      general Spanish models on user-generated text tasks and achieves competitive
      results on code-switching benchmarks. However, RoBERTuito is not specific to
      Argentine or Northwest Argentine regional Spanish, and no benchmark specifically
      evaluating LLMs on Rio Platense or Northwest Argentine disaster/emergency social
      media text was found. La Leaderboard (arXiv 2507.00999, public since September
      2024) covers 66 Spanish/Catalan/Basque/Galician datasets but does not specifically
      target Argentine emergency or disaster domains. Source: RoBERTuito (ACL Anthology)
      — [WEB-11]; La Leaderboard (arXiv) — [WEB-12]'
    indigenous_lexical_integration: 'No NLP tools or datasets specifically handling
      Guaraní/Quechua/Wichí lexical borrowing within Spanish disaster text in Argentine
      or Paraguayan contexts were found. Existing NLP resources for these languages
      are primarily machine translation corpora (Guaraní-Spanish parallel corpora
      by Chiruzzo et al. 2020; Góngora et al. 2021 Guaraní news/social media corpus)
      and morphological analyzers, not mixed-language disaster classification tools.
      The 2025 survey of NLP resources for Argentine indigenous languages (arXiv 2501.09943)
      confirms that unified information on speakers and computational tools is currently
      lacking. Source: Survey of Argentine indigenous NLP — [WEB-9];
      NLP Progress in Indigenous Latin American Languages — [WEB-10]'
writing_systems:
  scripts:
  - Latin alphabet (Spanish and written forms of all regional indigenous languages)
  register_variation: 'Target inputs span formal local news articles (structured prose,
    150–800 words estimated) to highly informal social media posts (Twitter/X character-limited
    posts, WhatsApp forwards, Facebook community group reports). Informal posts may
    include:

    - Non-standard spelling and abbreviation

    - Hashtags referencing local place names or event types

    - Mixed-media references (links to photos, voice notes transcribed)

    - Platform-specific shorthand (e.g., ''x eso'', ''q pasa'', ''tmbn'')'
  token_length_profile: 'Social media posts: typically 20–280 tokens. Local news fragments:
    150–600 tokens estimated. Both are substantially shorter than the wximpactbench
    long-context format (avg. 2,987 tokens) and closer to the mixed-context format
    (avg. 781 tokens). [NEEDS VERIFICATION — deferred: below search budget; characterizing
    actual token length distribution of Gran Chaco disaster social media posts would
    require corpus collection from regional platforms]'
disaster_event_ontology:
  primary_event_types_for_deployment:
  - type: Riverine flooding
    key_rivers:
    - Pilcomayo
    - Bermejo
    gran_chaco_specific_consequences:
    - Cross-border displacement along international river borders
    - Cutoff of dirt-road (ripio/tierra) access to indigenous communities
    - Disruption of cattle routes and agrarian supply chains
    - Stranded vehicles, school buses, and isolated settlements
    - Border integrity concerns (Pilcomayo as Argentina/Paraguay border)
    documented_scale: 'The 2018 Pilcomayo flood — the largest in 35 years — displaced
      more than 20,000 inhabitants and caused total loss of goods and cattle at Santa
      Victoria Este; the Paraguayan Chaco departments (Presidente Hayes, Boquerón,
      Alto Paraguay) were declared under national emergency (Ley Nº 7471/2025) again
      in 2025 for precipitation-caused flooding. Source: IDB PROADAPT — [WEB-5];
      WRI — [WEB-6];
      Bacn.gov.py Ley 7471 — [WEB-1]'
  - type: Drought
    gran_chaco_specific_consequences:
    - Livestock mortality and pasture loss
    - Water scarcity in isolated indigenous communities
    - Agricultural supply chain disruption
    documented_scale: 'In 2024, the three Paraguayan Chaco departments were declared
      under national drought emergency (Ley Nº 7222). SEN delivered 303,000 litres
      of water by tanker truck to Presidente Hayes and Boquerón in October 2024. Source:
      Bacn.gov.py Ley 7222 — [WEB-13];
      Ultima Hora SEN — [WEB-14]'
  - type: Locust outbreaks
    coverage_in_benchmark: ABSENT from wximpactbench — not represented in any of the
      15 LDA-derived weather event types
    gran_chaco_specific_consequences:
    - Crop destruction across large semi-arid areas
    - Cross-border spread requiring coordinated response
    - Pastoralist and smallholder livelihood loss
  - type: Chaco fires (incendios)
    gran_chaco_specific_consequences:
    - Destruction of indigenous territorial lands
    - Smoke affecting semi-urban centers
    - Access road closures
    - Wildlife habitat destruction (ecological)
    documented_scale: 'In October 2020, Presidente Hayes Department recorded over
      8,600 distinct fires in 24 hours, the highest in Paraguay. In 2023–2024, most
      Western Region fires occurred in Presidente Hayes. SEN and VIDECI are jointly
      active on cross-border fires near the Bolivia–Paraguay frontier. Source: Wikipedia
      Presidente Hayes Dept — [WEB-2];
      UNDP Bolivia VIDECI — [WEB-15]'
  - type: Infrastructure failure in isolated areas
    gran_chaco_specific_consequences:
    - Loss of bridge access across seasonal rivers
    - Communication blackouts in remote indigenous communities
    - Fuel and supply chain disruption
  - type: Cross-border displacement events
    coverage_in_benchmark: ABSENT from wximpactbench — not represented in any impact
      category definition
    gran_chaco_specific_consequences:
    - Population movement across Argentina/Paraguay or Argentina/Bolivia borders
    - Jurisdictional complexity for response coordination
    - International border integrity as a primary responder concern
  benchmark_ontology_gap_summary: 'The wximpactbench six-category impact ontology
    (Infrastructural, Agricultural, Ecological, Financial, Human Health, Political)
    was derived from Canadian newspaper content and lacks: (1) any cross-border displacement
    or border integrity exemplars in the Political category; (2) any locust or Chaco
    fire event types in the 15 LDA-derived weather types; (3) any mechanism for consequence-framing-dependent
    label assignment as practiced by Gran Chaco national coordinators.'
  consequence_framing_dependency: Label assignment in the Gran Chaco deployment is
    consequence-framing-dependent rather than event-type-determined. The same event
    (e.g., a flooded Pilcomayo-area road) may attract Infrastructural, Human Health,
    or Agricultural labels depending on which downstream consequences are reported
    in the source text (casualties, supply chain disruption, blocked commercial routes).
    This is structurally incompatible with the wximpactbench approach of assigning
    labels based on 'explicit mentions' of direct physical effects.
  no_spanish_disaster_nlp_benchmark_found: 'Searched for Spanish-language disaster
    NLP benchmarks specific to Gran Chaco, Argentina, Paraguay, or Bolivia flooding/locust/fire
    contexts. No such benchmark was found. The gap identified here is confirmed as
    a true documentation gap: no Spanish-language disaster impact classification benchmark
    exists for any Southern Cone or Gran Chaco sub-regional context. This null result
    is itself a significant finding for the validity assessment. Source: search of
    ACL Anthology and arXiv, May 2026 — [NOT FOUND — no Spanish-language disaster
    NLP benchmark for Gran Chaco or Southern Cone contexts surfaced in ACL Anthology
    or arXiv searches]'
infrastructure_notes:
  connectivity:
    semi_urban_centers: '[NEEDS VERIFICATION — deferred: below search budget; ITU
      and INDEC do not publish 4G coverage at the Tartagal/Embarcación level of granularity
      in freely accessible form]'
    rural_areas: '[NEEDS VERIFICATION — deferred: below search budget; likely 2G/3G
      patchwork with significant dead zones based on general Gran Chaco infrastructure
      documentation]'
    indigenous_territories: '[NEEDS VERIFICATION — deferred: likely unsearchable at
      community level; IDB PROADAPT documentation confirms that meteorological stations
      are separated by great distances and connectivity between communities was insufficient
      for coordinated alert prior to the PROADAPT initiative. Source: IDB — [WEB-5]]'
    disaster_conditions: 'Connectivity frequently disrupted during active flood events;
      social media posts may be delayed, geographically misattributed, or transmitted
      via satellite phone or relay. Gran Chaco PROADAPT explicitly relied on pre-existing
      social networks because formal connectivity and alert capacity were insufficient.
      Source: IDB — [WEB-5]'
  device_profile:
    social_media_sources: '[NEEDS VERIFICATION — deferred: below search budget; dominant
      platforms for disaster reporting in this zone are likely Facebook community
      groups and WhatsApp broadcast channels based on regional pattern documented
      in cultural_norms_notes, but no quantitative device/platform data was found
      for Salta or Paraguayan Chaco specifically]'
    responder_devices: '[NEEDS VERIFICATION — deferred: likely unsearchable (operational
      security detail for Gendarmería Nacional)]'
  road_infrastructure: 'Significant proportion of access routes in the deployment
    zone are unpaved (ripio/tierra); seasonal flooding renders these impassable and
    this constitutes a primary category of Infrastructural damage in local reporting.
    Benchmark content does not represent this road type or its consequences. Route
    No. 12 along the Pilcomayo in Presidente Hayes is explicitly documented as impassable
    when raining. Source: Wikipedia Presidente Hayes Dept — [WEB-2]'
  electricity: '[NEEDS VERIFICATION — deferred: below search budget; national-level
    electrification rates for Argentina (~98%), Paraguay (~98%), and Bolivia (~95%)
    are available but sub-national figures for rural Chaco are not readily available
    from a single authoritative source and would likely show substantially lower coverage]'
institutional_and_regulatory_context:
  argentina:
    national_emergency_coordination: 'Argentina''s primary national emergency management
      system is SINAGIR (Sistema Nacional para la Gestión Integral del Riesgo y la
      Protección Civil), created by Ley 27.287 (October 2016). SINAGIR integrates
      national, provincial, and municipal government agencies, NGOs, and civil society
      for risk reduction, crisis management, and recovery. As of March 20, 2025, Decreto
      225/25 created the Agencia Federal de Emergencias (AFE) as a decentralized agency
      under the Ministerio de Seguridad Nacional; SINAGIR now operates within the
      AFE''s orbit. AFE is the current national authority for emergencies and applies
      both Ley 27.287 (SINAGIR) and Ley 26.815 (Manejo del Fuego). The SINAGIR system
      includes the Sistema Nacional de Alerta y Monitoreo de Emergencias (SINAME)
      and coordinates with security forces including Gendarmería Nacional. Source:
      Argentina.gob.ar SINAGIR institucional — [WEB-16];
      Infoleg Decreto 225/25 — [WEB-17]'
    gendarmeria_nacional: Primary Argentine federal security and border force with
      operational presence across the tri-border zone; field gendarmes are a primary
      end-user group for this system
    provincial_civil_defense: '[NEEDS VERIFICATION — deferred: below search budget;
      SINAGIR operates via a federal structure requiring provincial adhesion; provincial
      civil defense directorates in Salta, Formosa, and Chaco operate under SINAGIR
      coordination (Decreto 383/2017 subsidiarity principle) but their specific structures
      were not confirmed in this search round]'
    data_protection_regulation: 'The primary Argentine data protection law is Ley
      25.326 (Protección de los Datos Personales / Hábeas Data), enacted October 4,
      2000, reglamentada by Decreto 1558/2001. As of 2022, the Agencia de Acceso a
      la Información Pública (AAIP) initiated a public consultation process (Anteproyecto
      presented August 30, 2022; public consultation closed October 11, 2022) to update
      Ley 25.326, but no new law has been enacted as of the search date. The current
      applicable law for processing social media content in emergency contexts remains
      Ley 25.326. Caveat: a reform bill has been in development since 2022 and the
      status of enactment should be confirmed before deployment. Source: Argentina.gob.ar
      Ley 25326 — [WEB-18];
      AAIP proyecto ley — [WEB-19]'
  paraguay:
    national_emergency_coordination: 'Paraguay''s national emergency management agency
      is the Secretaría de Emergencia Nacional (SEN), created by Ley Nº 2615, dependent
      on the Presidency of the Republic. SEN''s mandate covers prevention, mitigation,
      response, rehabilitation, and reconstruction for emergencies and disasters.
      It has active departmental and district-level organizational structures, and
      directly coordinates with gobernaciones and municipal intendencias. SEN has
      repeatedly declared national emergency status for the three Chaco departments
      (Presidente Hayes, Boquerón, Alto Paraguay) — most recently Ley Nº 7471/2025
      for 2025 flooding. SEN has an active Twitter/X presence (@senparaguay) used
      for disaster communications. Source: SEN institucional — [WEB-20];
      Ley 2615 — [WEB-21]'
    data_protection_regulation: '[NEEDS VERIFICATION — deferred: below search budget;
      Paraguay does not have a comprehensive data protection law equivalent to Argentina''s
      Ley 25.326 as of last available information, but this should be confirmed for
      the current deployment]'
  bolivia:
    national_emergency_coordination: 'Bolivia''s civil protection authority is the
      Viceministerio de Defensa Civil (VIDECI), operating under the Ministerio de
      Defensa. VIDECI operates under the Risk Management Law No. 602 and coordinates
      the four risk management processes (identification, reduction, emergency response,
      financial protection). VIDECI has departmental representations and activates
      the Comité de Operaciones de Emergencia Nacional (COEN) during declared emergencies.
      VIDECI specifically has identified the Bolivian Chaco (including Tarija/Gran
      Chaco province) as a priority zone due to recurring fires and droughts. Source:
      UNDP Bolivia VIDECI — [WEB-15];
      VIDECI Ministerio Defensa — [WEB-22]; UNISDR Bolivia
      document — [WEB-4]'
    data_protection_regulation: '[NEEDS VERIFICATION — deferred: below search budget;
      Bolivia does not have a comprehensive data protection law equivalent to GDPR
      or Argentina''s Ley 25.326; this should be confirmed for the current deployment]'
  cross_border_coordination:
    existing_mechanisms: 'In March 2007, Argentina, Bolivia, and Paraguay ratified
      the Framework Cooperation Agreement for the Sub-Regional Action Program for
      the Sustainable Development of the Gran Chaco Americano. In addition, Gran Chaco
      PROADAPT (an IDB Lab / Avina Foundation initiative) brought together civil society,
      the private sector, and the governments of Argentina, Paraguay, and Bolivia
      to adapt to climate change; this included shared access to meteorological data
      from 150+ stations across the three countries and the creation of a Master Plan
      for the Integrated Management of the Pilcomayo Basin. These mechanisms represent
      existing tri-border coordination infrastructure relevant to the deployment context.
      Source: IDRC Gran Chaco project — [WEB-23];
      IDB PROADAPT — [WEB-5]'
    border_management_salience: Border integrity and cross-border displacement are
      explicitly prioritized as primary disaster news categories by the deployment
      user. This has no equivalent in the wximpactbench Political impact category
      definitions.
socioeconomic_context:
  primary_livelihoods: 'Cattle ranching (ganado bovino), smallholder agriculture,
    subsistence farming, and seasonal labor in agrarian supply chains. Indigenous
    communities maintain subsistence-oriented land use. Strategic economic routes
    (roads linking agricultural production zones to processing centers) are of primary
    salience to responders. The Mennonite colonies in Paraguayan Boquerón produce
    over 60% of Paraguay''s dairy and meat. Source: Bienvenido a Paraguay — [WEB-24]'
  agrarian_supply_chain_vulnerability: Disruption to dirt-road access and river crossings
    during flood events directly interrupts cattle and crop transport; this type of
    Agricultural/Infrastructural consequence is common in local news and social media
    but absent from wximpactbench's Canadian agricultural framing.
  indigenous_community_access: 'Access to indigenous communities (Wichí, Chaco Guaraní,
    Quechua-adjacent) is a specific operational concern for responders; road cutoffs
    affecting these communities are regularly reported in local media and social media
    and require Human Health and Infrastructural classification. The 2018 Pilcomayo
    flood evacuated more than 10,000 people from Wichí, Toba, Chorote and Tapiete
    communities in Salta. Source: IDB PROADAPT — [WEB-5]'
  poverty_and_marginalization: '[NEEDS VERIFICATION — deferred: below search budget;
    national-level poverty statistics are available for all three countries but sub-national
    figures for rural Chaco and indigenous communities would require INDEC (Argentina),
    INE (Paraguay/Bolivia) sub-national data extraction not attempted in this search
    round]'
cultural_norms_notes: '- Responder culture in Argentine gendarmerie and civil protection
  forces is hierarchical and operationally focused; output formats must match field
  decision-making workflows, not academic classification conventions.

  - Indigenous communities (Wichí, Chaco Guaraní, Quechua-adjacent) have distinct
  land tenure systems and disaster vulnerability profiles that may not be reflected
  in mainstream news coverage but appear in community social media.

  - Regional identity in Northwest Argentina is distinct from Buenos Aires; national
  coordinators based in Buenos Aires may have different framings of Gran Chaco events
  than local field responders.

  - Social media in the region includes community-run Facebook groups and WhatsApp
  broadcast channels as primary informal information channels during disasters; these
  are not equivalent to formal news sources and carry different signal-to-noise characteristics.

  - Cross-border community ties exist across the Argentina/Paraguay and Argentina/Bolivia
  borders; displacement and community support are often reported informally through
  social networks before appearing in formal news.

  - In the Paraguayan Chaco, the Guaraní-Spanish mixed variety (''Jopara'') is characteristic
  of informal written communication and may appear in social media posts from Paraguayan
  Chaco sources. This is a specific lexical mixing pattern that standard Spanish NLP
  tools are not designed to handle.'
output_format_requirements:
  minimum_acceptable_form: Simultaneous multi-label classification across all relevant
    impact categories (matching wximpactbench's classification task structure)
  ranking_task_status: Explicitly rejected by deployment users as insufficiently reliable
    for direct operational use without human review; wximpactbench ranking task results
    are therefore of limited relevance to this deployment
  role_differentiated_needs:
    field_gendarmes: Require rapid, event-specific output with high precision on individual
      events; aggregate metrics are not operationally useful at this level
    national_coordinators: Require aggregate, scalable output supporting resource
      allocation across multiple concurrent events; are the authoritative labelers
      for ground-truth validation
  confidence_scores: Not produced by wximpactbench (binary true/false output only);
    deployment users indicated human review is needed for ambiguous cases, suggesting
    confidence gradations would be valuable
  benchmark_scoring_relevance_to_field_role: The wximpactbench F1/row-wise accuracy
    framework does not distinguish between field gendarme and national coordinator
    use cases; its relevance to the field gendarme rapid-lookup use case is unclear
    and should be assessed separately.
sub_national_variation:
- jurisdiction: Salta province, Argentina
  notes: '[NEEDS VERIFICATION — deferred: below search budget; Salta has a distinct
    Northwest Argentine Spanish variety with strong indigenous substrate influence
    (Quechua, Guaraní, Wichí); SINAGIR/AFE structures apply provincially but no Salta-specific
    disaster corpus or institutional sub-structure documentation was found in this
    search round]'
- jurisdiction: Formosa province, Argentina
  notes: '[NEEDS VERIFICATION — deferred: below search budget; Formosa has the highest
    density of Wichí and Pilagá communities in Argentina (13 Wichí communities documented);
    800 families were evacuated from Formosa city and Clorinda during 2015 flooding;
    connectivity is documented as highly constrained in the province. Source partial:
    ReliefWeb 2015 floods — [WEB-25]]'
- jurisdiction: Chaco province, Argentina
  notes: '[NEEDS VERIFICATION — deferred: below search budget; Chaco province is among
    the top provinces by expected annual flood damage (0.8% of population affected
    annually per World Bank estimates); the 1985 Aboriginal Census recorded 24,528
    indigenous people including 3,143 Wichís. Source partial: World Bank flood exceedance
    report — [WEB-26]]'
- jurisdiction: Boquerón and Alto Paraguay departments, Paraguay
  notes: 'Boquerón (capital Filadelfia; area >91,000 km²) borders Bolivia to the north
    and Argentina via the Pilcomayo to the south; it has 3 districts (Mariscal Estigarribia,
    Loma Plata, Filadelfia) and includes Mennonite colonies, indigenous communities,
    and sparse rural settlement. Alto Paraguay (capital Fuerte Olimpo) is the most
    sparsely populated department in Paraguay. Both have been repeatedly declared
    under national emergency (floods and drought) by SEN. SEN conducts active operations
    in both, including helicopter medical evacuations and food delivery to isolated
    communities. Source: Bacn.gov.py Ley 7471 — [WEB-1];
    Bienvenido a Paraguay — [WEB-24]'
- jurisdiction: Tarija and Chuquisaca departments, Bolivia (Gran Chaco lowlands)
  notes: 'Tarija is the primary Bolivian Chaco department; its Gran Chaco province
    (capital Yacuiba) borders Argentina and contains Ava Guaraní (Chiriguano)-speaking
    indigenous communities. VIDECI has departmental representation in Tarija. VIDECI
    has specifically identified the Bolivian Chaco as a priority zone for fire and
    drought response, and collaborated with PNUD on protocol development for the zone.
    Chuquisaca has a minimal Chaco footprint. Source: UNDP Bolivia VIDECI — [WEB-15];
    VIDECI defensacivil.gob.bo — [WEB-3]'
net_new_fields:
  gran_chaco_proadapt_early_warning_system:
    description: 'Gran Chaco PROADAPT is a tri-national civil society/government/private
      sector initiative (funded by IDB Lab and Nordic Development Fund, run by Avina
      Foundation) that created a flood early-warning system for the Pilcomayo basin,
      integrating data from 150+ meteorological stations across Argentina, Paraguay,
      and Bolivia. It successfully prevented loss of life in the 2018 Pilcomayo flood
      (the largest in 35 years). The system relied heavily on community social networks
      (''a web of social networks that already existed in the Gran Chaco'') rather
      than digital infrastructure, because formal connectivity was insufficient. This
      is deployment-relevant because: (a) it documents the existing social media and
      community network communication channels that the AI system would process, and
      (b) it confirms that informal social network posts are the primary real-time
      disaster information channel in the zone, not formal news. Source: IDB — [WEB-5];
      WRI — [WEB-6]'
    relevance_to_benchmark: 'Directly validates the deployment scenario: informal
      social network communication is the primary disaster information channel in
      this zone. Benchmark content (formal historical newspaper prose) is maximally
      mismatched to this confirmed input type.'
  nlp_resources_for_argentine_indigenous_languages:
    description: 'A 2025 survey (arXiv 2501.09943) systematically documents NLP resources
      for all indigenous languages spoken in Argentina, covering Mapuche, Tupí-Guaraní,
      Guaycurú (including Toba/Qom spoken in Formosa and Chaco), Quechua, Mataco-Mataguaya
      (including Wichí), Aymara, and Chon families. The survey finds that unified
      information on speakers and computational tools is currently lacking for most
      of these languages and notes that Argentine census methodology likely underestimates
      speaker counts. For the deployment, the Guaycurú family (Toba/Qom, spoken in
      Formosa and Chaco) and the Mataco-Mataguaya family (Wichí) are the most directly
      relevant; however, neither family has disaster classification resources, and
      their lexical integration into regional Spanish disaster text has no NLP coverage.
      Source: arXiv 2501.09943 — [WEB-9]'
    relevance_to_benchmark: Confirms that no NLP resources exist specifically for
      handling indigenous-language lexical borrowing within Spanish disaster text
      for the tri-border zone. This is an IF (Input Form) and IC (Input Content) gap
      with no existing tooling to bridge it.
  robertuito_spanish_social_media_model:
    description: 'RoBERTuito (Pérez et al., LREC 2022, ACL Anthology) is the most
      directly relevant existing NLP model for the deployment''s input register: a
      RoBERTa-based model pre-trained on 500M+ Spanish tweets, outperforming general
      Spanish models on user-generated text classification tasks including sentiment,
      hate speech, and irony detection. It achieves competitive results on the LinCE
      code-switching benchmark. However, it was not trained on disaster impact classification
      tasks, does not specifically represent Northwest Argentine or Paraguayan Chaco
      registers, and does not handle indigenous-language lexical integration. No evaluation
      of RoBERTuito or similar models on Gran Chaco disaster content was found. Source:
      ACL Anthology — [WEB-11]; arXiv abstract
      — [WEB-27]'
    relevance_to_benchmark: Confirms a social media Spanish NLP model exists but has
      no disaster impact classification evaluation and no regional specificity for
      this deployment zone. The IF gap for informal Spanish social media register
      is partially addressable via RoBERTuito but not via wximpactbench.
  afe_2025_argentina_emergency_restructuring:
    description: 'As of March 20, 2025, Decreto 225/25 created the Agencia Federal
      de Emergencias (AFE) as a new decentralized national authority under the Ministerio
      de Seguridad Nacional, with SINAGIR now operating within AFE''s orbit. AFE is
      the current Argentine national authority for emergencies and applies Ley 27.287
      (SINAGIR) and Ley 26.815 (Manejo del Fuego). This is a recent institutional
      restructuring that may affect the names and reporting chains of national coordinators
      who would serve as authoritative labelers in this deployment. Source: Argentina.gob.ar
      SINAGIR institucional — [WEB-16]'
    relevance_to_benchmark: Deployment documentation referring to 'SINAGIR' as the
      national coordinator structure should be updated to reflect that the operational
      authority is now AFE (as of March 2025). Annotator recruitment for ground-truth
      validation should target AFE/SINAGIR national coordinators under the current
      institutional structure.
flagged_gaps_for_web_search:
- gap_id: 1
  description: Gran Chaco-specific event ontology
  search_target: Spanish-language disaster NLP benchmark Gran Chaco Argentina Paraguay
    Bolivia flooding locust outbreak Pilcomayo Bermejo
  search_outcome: NOT FOUND — no Spanish-language disaster NLP benchmark exists for
    Gran Chaco or Southern Cone contexts. This null result is a confirmed documentation
    gap, not a search failure.
- gap_id: 2
  description: Rio Platense Spanish register and social media disaster content
  search_target: Rio Platense Spanish NLP benchmark social media disaster emergency
    Argentina Bolivia Paraguay informal register
  search_outcome: PARTIALLY RESOLVED — RoBERTuito (LREC 2022) is the most relevant
    model for Spanish social media NLP but is not disaster-domain-specific and has
    no Gran Chaco regional evaluation. No dedicated benchmark for Rio Platense or
    Northwest Argentine disaster social media was found.
- gap_id: 3
  description: Indigenous-language toponyms and lexical borrowing within Spanish disaster
    text
  search_target: Guaraní Quechua Wichí Spanish NLP lexical borrowing indigenous toponym
    disaster text Argentina Paraguay benchmark
  search_outcome: NOT FOUND — no NLP tools or benchmarks handle indigenous-language
    lexical borrowing within Spanish disaster text for this zone. The 2025 survey
    of Argentine indigenous NLP resources (arXiv 2501.09943) confirms the gap. Guaraní-Spanish
    parallel corpora exist for MT but not for mixed-language disaster classification.
- gap_id: 4
  description: Practitioner-validated label annotation by Southern Cone emergency
    professionals
  search_target: practitioner-validated NLP disaster annotation Argentina emergency
    management gendarmerie civil protection coordinator labeling
  search_outcome: NOT FOUND — no practitioner-validated NLP disaster annotation resource
    involving AFE/SINAGIR coordinators, Gendarmería Nacional, SEN (Paraguay), or VIDECI
    (Bolivia) personnel was found.
- gap_id: 5
  description: Sub-national disaster text corpora for the tri-border zone
  search_target: disaster text corpus Salta Formosa Chaco province Argentina Paraguay
    Boquerón Bolivia department emergency reporting
  search_outcome: NOT FOUND — no sub-national disaster text corpus for Salta, Formosa,
    Chaco provinces or Paraguayan/Bolivian Chaco departments was found.
- gap_id: 6
  description: Cross-border displacement and border integrity as disaster impact categories
    in NLP
  search_target: cross-border displacement disaster impact NLP classification South
    America tri-border Argentina Paraguay Bolivia border integrity
  search_outcome: NOT FOUND — no NLP classification system was found that includes
    cross-border displacement or border integrity as impact categories for South American
    disaster contexts.
- gap_id: 7
  description: Role-differentiated output formats for emergency AI systems
  search_target: role-differentiated disaster AI output format operational emergency
    response field coordinator NLP evaluation situational awareness
  search_outcome: NOT SEARCHED — deferred; below search budget after higher-priority
    gap searches.
- gap_id: 8
  description: Consequence-framing-dependent label assignment in disaster NLP
  search_target: consequence-framing disaster impact classification ambiguous multi-label
    NLP evaluation framing-dependent annotation
  search_outcome: NOT SEARCHED — deferred; below search budget after higher-priority
    gap searches.
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.bacn.gov.py/leyes-paraguayas/12739/ley-n-7471-2025-que-declara-en-situaci-n-de-emergencia-a-los-departamentos-de-presidente-hayes-boquer-n-y-alto-paraguay-y-ampl-a-el-presupuesto-general-de-la-naci-n-para-el-ejercicio-fiscal-2025-aprobado-por-ley-n-7408-de-fecha-30-de-diciembre-de-2024-presidencia-de-la-rep-blica-secretar-a-de-emergencia-nacional |
| WEB-2 | https://en.wikipedia.org/wiki/Presidente_Hayes_Department |
| WEB-3 | https://defensacivil.gob.bo/ |
| WEB-4 | https://www.unisdr.org/files/30755_boldocpais.pdf |
| WEB-5 | https://www.iadb.org/en/staying-ahead-gran-chacos-floods |
| WEB-6 | https://www.wri.org/insights/gran-chaco-communities-build-climate-resilience |
| WEB-7 | https://en.wikipedia.org/wiki/Rioplatense_Spanish |
| WEB-8 | https://academia-lab.com/encyclopedia/indigenous-peoples-of-argentina/ |
| WEB-9 | https://arxiv.org/html/2501.09943v2 |
| WEB-10 | https://arxiv.org/html/2404.05365v1 |
| WEB-11 | https://aclanthology.org/2022.lrec-1.785/ |
| WEB-12 | https://arxiv.org/html/2507.00999v1 |
| WEB-13 | https://www.bacn.gov.py/leyes-paraguayas/12160/ley-n-7222-que-declara-en-situacion-de-emergencia-nacional-a-los-departamentos-presidente-hayes-boqueron-y-alto-paraguay |
| WEB-14 | https://www.ultimahora.com/secretaria-de-emergencia-nacional |
| WEB-15 | https://www.undp.org/es/bolivia/noticias/defensa-civil-actualiza-protocolos-de-atencion-desastres |
| WEB-16 | https://www.argentina.gob.ar/sinagir/institucional |
| WEB-17 | https://servicios.infoleg.gob.ar/infolegInternet/anexos/400000-404999/400480/norma.htm |
| WEB-18 | https://www.argentina.gob.ar/normativa/nacional/ley-25326-64790/actualizacion |
| WEB-19 | https://www.argentina.gob.ar/aaip/datospersonales/proyecto-ley-datos-personales |
| WEB-20 | https://sen.gov.py/institucional/ |
| WEB-21 | https://www.bacn.gov.py/leyes-paraguayas/2410/ley-n-2615-crea-la-secretaria-de-emergencia-nacional-sen |
| WEB-22 | https://www.mindef.gob.bo/node/499 |
| WEB-23 | https://idrc-crdi.ca/en/what-we-do/projects-we-support/project/valuing-water-changing-climate-and-economy-gran-chaco |
| WEB-24 | https://www.bienvenidoaparaguay.com/deptos.php?xmldepto=17 |
| WEB-25 | https://reliefweb.int/disaster/fl-2015-000171-pry |
| WEB-26 | https://documents1.worldbank.org/curated/en/792921620399148269/pdf/Estimating-Flood-Exceedance-Curves-in-Argentina.pdf |
| WEB-27 | https://arxiv.org/abs/2111.09453 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark was built around Canadian historical newspaper content about weather impacts. Your deployment covers Gran Chaco disaster events — which may include flooding from the Pilcomayo and Bermejo rivers, droughts, locust outbreaks, chaco fires, or infrastructure failures in isolated rural areas. Do these event types and their local consequences (e.g., disrupted cattle routes, damage to dirt-road access to indigenous communities, cross-border displacement) map onto the impact categories your responders care about, or are there Gran Chaco-specific damage types that would be missing?
A1: General event types (flooding, fires) overlap and the benchmark may usefully indicate how models capture broad damage descriptions — including what performance is lost when content is translated. However, Gran Chaco-specific consequences diverge: responders prioritize international border integrity and strategic economic routes as primary news items, while social media content reflects a regional socioeconomic context (cross-border displacement, indigenous community access, agrarian supply chains) that the benchmark is unlikely to represent.

Q2 [IC]: The benchmark was constructed from Canadian English-language newspapers. Your source texts are Spanish-language local news and social media from Argentina, Bolivia, and Paraguay — including informal writing, regional slang, code-switching with indigenous languages (Guaraní, Quechua, Wichí), and platform-specific abbreviations. Would your responders consider damage reports written in these registers as representative of what the system needs to handle correctly?
A2: Partially. The system primarily needs to handle Rio Platense Spanish containing regional vocabulary, including place names and proper nouns rooted in indigenous languages. Full code-switching or indigenous-language text is not the primary use case, but lexical borrowing from those languages within Spanish-language content is routine and must be handled correctly.

Q3 [OC]: The benchmark's impact labels (infrastructural, political, financial, ecological, agricultural, human health) were validated against Canadian newspaper content. For your responders in the Gran Chaco, would the boundary between these categories feel natural — for example, would a flooded dirt road that cuts off an indigenous community be classified as infrastructural, ecological, or human health? And who among your users — field gendarmes, civil protection technicians, national coordinators — should be the authoritative judge of correct label assignment in your context?
A3: Label assignment is consequence-framing dependent rather than event-type dependent: the same flooded road could attract infrastructural, human health, or agricultural labels depending on what consequences are reported (casualties, loss of supplies, blocked commercial routes). Events need to cross a news/social-media salience threshold — typically affecting semi-urban or broader rural areas — to be relevant. National coordinators are the designated authoritative labelers for this deployment.

Q4 [OO]: The benchmark outputs are multi-label classifications and ranked answers. Your responders need to quickly identify damage types from incoming news and social media. Does your system need to produce a ranked list of impact types, a simple set of simultaneous labels, a confidence score, or a structured alert that routes information to specific response units? Would the same output format serve a field gendarme in Salta and a national emergency coordinator in Buenos Aires equally well?
A4: Simultaneous multi-label output is the minimum acceptable output form; ranking is considered insufficiently reliable for direct operational use without human review. Output needs diverge by role: field gendarmes need fast, event-specific lookup during ongoing incidents (e.g., locating a specific stranded vehicle or school bus in a flood); national coordinators need aggregate, scalable output for resource allocation decisions across multiple concurrent events. A single output format does not serve both roles equally.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | Benchmark categories were designed for Canadian weather-impact journalism; Gran Chaco-specific damage patterns (border disruption, strategic economic routes, indigenous community access, cross-border displacement) are absent from the source ontology, and the user confirmed the social-media context is poorly covered. |
| IC | HIGH | Benchmark uses historical Canadian English newspaper text; deployment inputs are Rio Platense Spanish social media and local news with indigenous-language toponyms and regional vocabulary — a large lexical and register gap with no community validation of benchmark content against this population. |
| IF | HIGH | Benchmark is English-only text from formal historical newspapers; deployment requires processing informal Spanish-language social media posts, including platform abbreviations and indigenous-language lexical borrowing, representing a significant input distribution mismatch. |
| OO | HIGH | Label boundaries (infrastructural vs. human health vs. agricultural) are consequence-framing-dependent in the Gran Chaco context rather than event-type-determined, and the Canadian validation context does not reflect how regional responders conceptually partition disaster impacts near international borders and indigenous territories. |
| OC | HIGH | Ground-truth labels were validated against Canadian newspaper content; the user identified national coordinators as the authoritative labelers for this deployment, a population entirely absent from the benchmark's annotation process, and label correctness is subjective and framing-dependent. |
| OF | MODERATE | The benchmark's multi-label classification output aligns with the minimum acceptable deployment output (simultaneous labels), but the benchmark also includes ranking tasks that the user explicitly rejected as unreliable; the divergent needs of field gendarmes vs. national coordinators are not addressed by a single benchmark output format. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** Michaelyya/wximpactbench-1386
**Analysis date:** 2025-07-14
**Examples reviewed:** 31 from `train` split
**Columns shown:** id, date, time_period, weather_type, text, infrastructural_impact, political_impact, financial_impact, ecological_impact, agricultural_impact, human_health_impact
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | wximpactbench-1386 | Ex. 1 | all=0 | "John's Cloudy -4 -4 United States Max Min Atlanta Cloudy 17 4 Boston Cloudy 3 -6 Chicago Cloudy 2 2 Dallas Thunderstorms 11 2" | Weather table/tabular data with no narrative — all-zero label, non-event content | IO, IC |
| D2 | wximpactbench-1386 | Ex. 2 | all=0 | "But the real beneficiaries of the work-at-home trend are the employees themselves… She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9)" | Crossword puzzle clues and work-from-home editorial — zero weather impact content | IO, IC |
| D3 | wximpactbench-1386 | Ex. 3 | infra=1 | "by six o'clock the electric car services in all the important points west of Toronto had been completely paralyzed" | 1894 blizzard article: infrastructure disruption to Canadian railway/electric car — exemplary on-target sample | IO, OO |
| D4 | wximpactbench-1386 | Ex. 4 | all=0 | "Police say the aggravated assault charge against Clarkson involves a February attack on Boland in which the celebrity photographer's face and chest were splashed with concentrated sulphuric acid." | Crime report with no weather content — all-zero label | IO, IC |
| D5 | wximpactbench-1386 | Ex. 5 | all=0 | "The decision yesterday followed a 16-hour overnight meeting in Berlin, where debate over how much to give away was sometimes interrupted by the sounds of revellers celebrating the first anniversary of the opening of the Berlin Wall." | Political news about German unification — no weather content | IO, IC |
| D6 | wximpactbench-1386 | Ex. 6 | all=0 | "A poor lady passenger was dashed to leeward and had her skull fractured. She was landed this morning in a dying state with a coffined child that succumbed last night to its sufferings." | Storm narrative with human casualty but annotated all-zero — potential label discrepancy | OC, OO |
| D7 | wximpactbench-1386 | Ex. 7 | infra=1 | "Almost 4 million people across China had been cut off by flood waters, 810,000 homes have collapsed and 2.8 million homes have been damaged" | 1996 Yangtze River flood report from China — not Canadian, annotated for infrastructure | IO, IC |
| D8 | wximpactbench-1386 | Ex. 8 | infra=1, health=1 | "The Jakarta Post reported that hundreds of houses, schools and other buildings sustained damage when one of the twin peaks of the volcano exploded. At least 20 people sustained minor injuries" | Indonesian volcanic eruption and Washington state earthquake — non-Canadian, non-weather-disaster content labeled for infrastructure and health | IO, IC |
| D9 | wximpactbench-1386 | Ex. 12 | all=0 | "residents of southwestern Quebec have been plunged back into the deep freeze Overnight lows in Montreal were expected to drop to minus-16 Celsius last night and tumble as far as minus-30C on the South Shore, where more than one million people struggle on without power or heat" | 1998 Quebec ice storm aftermath — one million without power/heat, annotated all-zero | OC, OO |
| D10 | wximpactbench-1386 | Ex. 14 | infra=1, pol=1, fin=1 | "Residents of the locality were put to great inconvenience by the huge piles of snow now accumulated on the streets… Already $30,000 has been expended in removing it" | 1887 Montreal snow removal municipal debate — multi-label (infra+pol+fin) correctly labeled | OO, OC |
| D11 | wximpactbench-1386 | Ex. 16 | all=0 | "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35" | Stock ticker/financial table — all-zero label, clearly off-topic content | IO, IC, IF |
| D12 | wximpactbench-1386 | Ex. 18 | all=0 | "The walkout will interrupt regular garbage collection and will affect street and sidewalk cleanup if it snows. Unless nine centimetres or more of snow falls during the walkout, blue-collar workers aren't obliged to clean the streets and sidewalks." | Labor dispute/garbage collection strike — weather mentioned incidentally, all-zero label | IO |
| D13 | wximpactbench-1386 | Ex. 19 | all=0 | "Penn refuses to play up the easy nebbish… he does not wear glasses, flood pants or a bow tie" | Film review with only figurative use of "flood" — all-zero label, entirely off-topic | IO, IC |
| D14 | wximpactbench-1386 | Ex. 21 | all=0 | "in Richmond, the storm so long expected has broken forth in all its fury. Great flashes of blinding lightning intermingled with the grand roar of the thunder from on high" | Fictional storm description used metaphorically in a society/romance narrative — all-zero label | IO, IC |
| D15 | wximpactbench-1386 | Ex. 22 | all=0 | "the agency said Christian Lambrechts… said this would expose more of the sea's surface to sunlight, rather than reflect it, contributing to continued and accelerated warming The peninsula - the tongue of land that juts toward South America - has been hit by greater warming than almost any other area on Earth" | Antarctic/climate change science brief — no direct disaster impact, all-zero label | IO |
| D16 | wximpactbench-1386 | Ex. 23 | agri=1, health=1 | "More than 292,000 people have been evacuated in the mountainous region along the Yangtze River, with more than 100,000 homes damaged and crops on about 175,000 hectares of farmland destroyed" | 2007 European/Chinese/Pakistani multi-location disaster report from Montreal Gazette — agricultural and health labeled, but not infrastructural despite 100k homes damaged | OC, OO |
| D17 | wximpactbench-1386 | Ex. 24 | all=0 | "01 SECOND RACE: Trot, I Mile Purse: 11,000 5 Prime Saliora (M. Lalonde) 9.70 5.10 5.70 3 Bidou Fio (R. SimarrJ) 5.30 4.40" | Horse racing results table with unrelated editorial on optometrists' ad — off-topic noise | IO, IC, IF |
| D18 | wximpactbench-1386 | Ex. 26 | pol=1, eco=1 | "A line of freak thunderstorms rumbling across the northeastern Mediterranean coast from Spain and southern France to the principality of Monaco brought two days of disastrous flash flooding… Raging waters uprooted trees and swept away cars as river levels rose by as much as 3 metres" | 1992 Mediterranean flash flood — political and ecological but not infrastructural ("swept away cars," "uprooted trees") — label boundary question | OO, OC |
| D19 | wximpactbench-1386 | Ex. 27 | eco=1 | "With about half the original 1.6-million-hectare swamp filled for development or drained for agriculture, the park includes about 202,000 hectares of marsh experts liken the Everglades to a seriously ill patient" | 1990 Everglades drought/ecosystem article — ecological only; US content | IO, IC |
| D20 | wximpactbench-1386 | Ex. 10 | all=0 | "July 7th they encountered a heavy gale from the west, and had great difficulty in keeping the boat free, the sea continually breaking on board… After the accident they suffered severely from the cold." | 1896 Atlantic rowing voyage encounter with gale — human suffering described but labeled all-zero | OC, OO |
| D21 | wximpactbench-1386 | Ex. 17 | infra=1 | "TRAFFIC IS PARALYZED In Western Canadian Cities, and at Many Points In the United States Disasters In England." | 1894 blizzard chunk (segmented from Ex. 3) — infrastructure label carried over to chunk | IF |
| D22 | wximpactbench-1386 | Ex. 9 | all=0 | "Peter Russell, a law professor at the University of Toronto, said the Supreme Court will benefit from Binnie's solid experience in constitutional and international affairs." | Legal/judicial appointment news — entirely off-topic | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-label simultaneous classification output structure aligns with minimum acceptable deployment form
- **Dimension(s):** OF, OO
- **Observation:** The dataset encodes all six impact categories as simultaneous binary integer labels per row, exactly matching the deployment's minimum acceptable output specification of simultaneous multi-label classification in a single pass. Every sampled example has all six label fields populated.
- **Deployment relevance:** The deployment explicitly requires simultaneous multi-label output rather than ranked or sequential classification. The dataset's schema (six binary int64 fields per example) directly validates this output architecture. National coordinators needing aggregate situational awareness can receive a compact label vector per incoming text, which is operationally viable for resource allocation decisions.
- **Datapoint citations:**
  - [D3] Example 3 (train, infra=1, others=0): "by six o'clock the electric car services in all the important points west of Toronto had been completely paralyzed" — Demonstrates single-pass assignment of one active label among six, with no confusion between co-present categories.
  - [D10] Example 14 (train, infra=1, pol=1, fin=1): "Residents of the locality were put to great inconvenience by the huge piles of snow now accumulated on the streets… Already $30,000 has been expended in removing it" — Demonstrates correct simultaneous multi-label assignment (infrastructure + political + financial) for a single article, proving the scheme supports multi-label outputs in the deployment's required format.

#### Strength 2: Negative examples (all-zero labels) are abundant and structurally necessary
- **Dimension(s):** OO, OF
- **Observation:** A large proportion of the sampled examples carry all-zero labels (approximately 20 of 31 sampled). These include genuinely off-topic texts (crossword puzzles, stock tickers, legal news, sports) as well as weather-adjacent texts where no direct impact was found. This provides a meaningful proportion of true negatives for recall calibration.
- **Deployment relevance:** In an operational disaster triage system, the incoming text stream will include many non-disaster posts. Evaluating model false-positive rates on this large null class is directly relevant to precision in the field, where false alarms generate responder fatigue. The benchmark's mixed-context chunking (which produces label-free negative chunks) replicates a realistic signal distribution.
- **Datapoint citations:**
  - [D2] Example 2 (train, all=0): "She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9)" — Crossword puzzle clues; a strong negative example for any weather impact category.
  - [D12] Example 18 (train, all=0): "The walkout will interrupt regular garbage collection and will affect street and sidewalk cleanup if it snows. Unless nine centimetres or more of snow falls during the walkout" — Weather mentioned incidentally in a labor dispute; correctly labeled all-zero, testing whether models avoid false positives on incidental weather mentions.
  - [D13] Example 19 (train, all=0): "he does not wear glasses, flood pants or a bow tie" — Figurative use of "flood" in a film review; correctly labeled all-zero, testing polysemy handling.

#### Strength 3: Multi-period coverage provides some temporal register variation
- **Dimension(s):** IC, IF
- **Observation:** The dataset spans two temporal periods, with examples from the 1880s–1890s (historical) and from the 1990s–2000s (modern). Within the English-language formal journalistic register, this variation does expose models to somewhat different vocabularies and narrative styles.
- **Deployment relevance:** While the deployment's primary language is Spanish social media, the temporal register variation in the benchmark at least tests whether evaluated LLMs handle internal linguistic variation in their training domain — a minor positive signal for general model robustness. Historical period articles tend to be longer and more explicit about causal chains, which the benchmark's own analysis suggests makes classification somewhat easier.
- **Datapoint citations:**
  - [D3] Example 3 (historical, 18940213): "Sunday evening's despatches brought the news that a very severe blizzard was prevailing in Kansas… electric car services in all the important points west of Toronto had been completely paralyzed" — 1894 formal journalistic prose with archaic vocabulary ("despatches") and elaborated cause-effect structure.
  - [D16] Example 23 (modern, 20070722): "More than 292,000 people have been evacuated in the mountainous region along the Yangtze River, with more than 100,000 homes damaged and crops on about 175,000 hectares of farmland destroyed" — 2007 modern wire service report with compressed, terse disaster description — different register from historical examples.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Language and register are fundamentally mismatched to deployment inputs
- **Dimension(s):** IC, IF
- **Observation:** Every sampled example is English-language formal prose from Canadian newspapers. No Spanish-language text, no social media register, no informal orthography, no platform abbreviations, no indigenous-language toponyms (Pilcomayo, Bermejo, Wichí, Guaraní-derived place names), and no code-switching patterns appear anywhere in the 31 reviewed examples. The benchmark's `languages: en` metadata is confirmed by all examples.
- **Deployment relevance:** The deployment system must process Rio Platense Spanish social media posts and local news fragments that include regional vocabulary with Guaraní, Quechua, and Wichí lexical borrowing. The benchmark provides zero evidence about how any evaluated LLM performs on this input type. Any model performance score obtained on this benchmark is drawn from a language and register distribution with no overlap with the deployment input distribution. Results cannot be validly transferred to predict performance on Gran Chaco Spanish social media content.
- **Datapoint citations:**
  - [D11] Example 16 (train, all=0): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35" — OCR-degraded stock ticker table in English; maximally distant from Spanish social media register.
  - [D2] Example 2 (train, all=0): "She takes a turn at the table in a lay way (5) 29, A good one is of assistance (9)" — Crossword puzzle content in English; confirms that even the negative examples are English formal media, not Spanish social media.
  - [D3] Example 3 (train, infra=1): "Sunday evening's despatches brought the news that a very severe blizzard was prevailing in Kansas" — Historical English narrative style with archaic vocabulary; no feature overlap with informal Rio Platense Spanish.

#### CRITICAL Concern 2: Impact categories were operationalized for Canadian journalistic framing and exclude Gran Chaco-specific damage categories
- **Dimension(s):** IO, OO
- **Observation:** The six impact categories — Infrastructural, Political, Financial, Ecological, Agricultural, Human Health — are operationalized through definitions anchored in Canadian newspaper exemplars. Across all 31 reviewed examples, there is no instance of: cross-border displacement as a political or infrastructural consequence; border integrity as a primary category; locust outbreaks; Chaco fire behavior; dirt-road access disruption to indigenous communities; or agrarian supply chain disruption tied to river crossings. The Political category exemplar in the data (municipal snow removal debate, [D10]) and the ecological exemplar (Everglades drought, [D19]) both reflect North American policy and ecological contexts without any Southern Cone equivalent.
- **Deployment relevance:** The deployment user confirmed that Gran Chaco national coordinators prioritize international border integrity and strategic economic routes as primary news categories, and that cross-border displacement along the Pilcomayo and Bermejo rivers is a primary disaster consequence type. None of these appear in the benchmark's operational definitions or sampled examples. A model trained or evaluated on this benchmark may assign labels that reflect Canadian journalistic salience rather than Gran Chaco responder logic.
- **Datapoint citations:**
  - [D10] Example 14 (train, pol=1, fin=1, infra=1): "Aid. Patrick Kennedy asked the chairman of the Road committee if he could kindly send some men and carts out to Forfar and Conway streets… Already $30,000 has been expended in removing it" — Political label assigned to municipal snow removal budget debate; no analog in Gran Chaco disaster response logic where Political salience concerns border integrity and inter-governmental coordination.
  - [D19] Example 27 (train, eco=1): "With about half the original 1.6-million-hectare swamp filled for development or drained for agriculture, the park includes about 202,000 hectares of marsh experts liken the Everglades to a seriously ill patient" — Ecological label assigned to US Everglades drought/development article; Gran Chaco ecological priorities (Chaco fire, habitat destruction, locust outbreaks) are absent from all reviewed examples.
  - [D18] Example 26 (train, pol=1, eco=1): "Raging waters uprooted trees and swept away cars as river levels rose by as much as 3 metres" — Mediterranean flash flood annotated for political and ecological impacts but not infrastructure ("swept away cars"); the label boundary logic here differs from how Gran Chaco coordinators would classify a road-washing flood event on a critical access route.

#### CRITICAL Concern 3: Ground-truth labels reflect Canadian academic annotators, not Gran Chaco emergency professionals
- **Dimension(s):** OC
- **Observation:** The annotation process used Canadian academic researchers specializing in historical climate analysis; no inter-annotator agreement statistics are available. The reviewed examples reveal several annotation decisions that would likely differ under the consequence-framing logic Gran Chaco national coordinators apply. Example 6 describes a maritime storm in which "a poor lady passenger was dashed to leeward and had her skull fractured" and "a coffined child that succumbed last night to its sufferings" — direct casualties — yet is labeled all-zero. Example 12 describes a million people without power or heat during a Quebec ice storm but is also labeled all-zero. Example 20 describes sailors who "suffered severely from the cold" after a capsizing — also all-zero.
- **Deployment relevance:** The deployment user designated national coordinators in Buenos Aires as the authoritative ground-truth labelers. These annotators apply consequence-framing-dependent logic: the same event attracts different labels depending on which downstream consequences are reported (casualties, supply chain disruption, blocked routes). The benchmark's annotation guidelines emphasize "explicit mentions" and "direct physical effects," but the reviewed examples show that even explicit human casualties can receive all-zero labels (D6, D20), and one million people without power receives all-zero (D9). This annotation philosophy does not match the operational salience logic of Gran Chaco emergency responders.
- **Datapoint citations:**
  - [D6] Example 6 (train, all=0): "A poor lady passenger was dashed to leeward and had her skull fractured. She was landed this morning in a dying state with a coffined child that succumbed last night to its sufferings." — Explicit human casualty from a storm, annotated all-zero; Gran Chaco coordinators would likely assign Human Health=1 for any text reporting casualties caused by weather conditions.
  - [D9] Example 12 (train, all=0): "more than one million people struggle on without power or heat The Weather Network is forecasting a high of only minus-15 today" — Over one million people without power and heat during extreme cold, labeled all-zero; an active infrastructure and human health impact by virtually any emergency responder's framing.
  - [D20] Example 10 (train, all=0): "July 7th they encountered a heavy gale from the west… After the accident they suffered severely from the cold." — Sailors suffering after storm capsizing; direct physical harm from weather, labeled all-zero.

#### MAJOR

#### MAJOR Concern 4: High proportion of non-weather and off-topic content in the mixed-context dataset
- **Dimension(s):** IO, IC
- **Observation:** A substantial proportion of the 31 reviewed examples contain no weather-related content whatsoever and carry all-zero labels. These include: stock ticker tables ([D11], [D17]), horse racing results ([D17]), a film review where "flood pants" appears figuratively ([D13]), a legal/judicial appointment article ([D22]), a fictional/literary storm description ([D14]), a crime report ([D4]), and a political/electoral article ([D5]). These appear to be chunked segments from mixed-context articles where the weather content appeared in a different segment. While they serve as negative examples, they constitute a large portion of the evaluated data.
- **Deployment relevance:** The deployment system processes incoming social media posts and news fragments that are selected because they contain disaster-related keywords or are generated in disaster contexts. The proportion of genuinely irrelevant content in the deployment stream will differ substantially from the benchmark's article-chunk distribution. The benchmark's negative examples include crossword clue fragments and stock tables — types of content that would never appear in a disaster social media triage pipeline — so benchmark precision/recall metrics on this negative class do not translate to the deployment's actual false-positive rate.
- **Datapoint citations:**
  - [D11] Example 16 (train, all=0): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25" — OCR-degraded stock table from the same physical newspaper page as a weather article; artificially generated negative example with no deployment equivalent.
  - [D4] Example 4 (train, all=0): "Police say the aggravated assault charge against Clarkson involves a February attack on Boland in which the celebrity photographer's face and chest were splashed with concentrated sulphuric acid." — Crime report with no weather content; exists as a negative because it was chunked from the same article batch.
  - [D14] Example 21 (train, all=0): "in Richmond, the storm so long expected has broken forth in all its fury. Great flashes of blinding lightning intermingled with the grand roar of the thunder from on high" — Fictional/literary storm description labeled all-zero; tests polysemy handling but represents an unrealistic negative example type for disaster triage.

#### MAJOR Concern 5: Label boundary inconsistencies visible within the sampled data
- **Dimension(s):** OO, OC
- **Observation:** Several examples reveal inconsistent label boundary application. Example 23 (2007 European/Chinese floods) labels agricultural=1 and health=1 for a report that also states "more than 100,000 homes damaged" — a clear infrastructural impact — but infrastructure=0. Example 26 labels a Mediterranean flash flood that "swept away cars" and "uprooted trees" as ecological=1 and political=1 but not infrastructural. Example 6, as noted above, reports human skull fracture and child death from a storm but receives all-zero labels. No inter-annotator agreement statistics are available to assess whether these represent systematic decisions or annotation noise.
- **Deployment relevance:** The deployment requires consistent label assignment because national coordinators will use these labels for resource allocation. If the benchmark's underlying annotation philosophy produces labels that a Gran Chaco coordinator would consider inconsistent (infrastructure present but unlabeled when homes collapse; human health absent when casualties occur), then model performance scores on this benchmark do not validly predict whether a model's outputs will be trusted by the deployment's authoritative labelers.
- **Datapoint citations:**
  - [D16] Example 23 (train, agri=1, health=1): "more than 100,000 homes damaged and crops on about 175,000 hectares of farmland destroyed, Xinhua said" — 100k homes damaged annotated as not infrastructural while agricultural and health labels are positive; boundary logic unclear.
  - [D18] Example 26 (train, pol=1, eco=1): "Raging waters uprooted trees and swept away cars as river levels rose by as much as 3 metres" — Cars swept away and infrastructure-affecting flood labeled ecological and political but not infrastructural.
  - [D6] Example 6 (train, all=0): "A poor lady passenger was dashed to leeward and had her skull fractured. She was landed this morning in a dying state with a coffined child that succumbed last night to its sufferings." — Direct weather-caused fatalities annotated as zero for all categories including human health.

#### MAJOR Concern 6: Geographic scope of labeled content extends beyond Canada but the impact taxonomy remains Canadian-framed
- **Dimension(s):** IO, IC
- **Observation:** Multiple labeled examples describe disasters that occurred in China ([D7], [D16]), Japan ([D7]), Pakistan ([D16]), Indonesia ([D8]), the United States ([D8], [D19]), and Europe ([D18]), not Canada. These appear to be wire service reports from the Montreal Gazette that happened to be selected by the LDA topic model. The benchmark's geographic scope is therefore not strictly Canadian despite being framed as such, but the taxonomy and annotation logic remain Canadian-academic in origin.
- **Deployment relevance:** While the presence of non-Canadian content is a minor positive in that it confirms the benchmark tests general event description, it also reveals that the benchmark's input ontology claim ("designed exclusively for Canadian weather-impact journalism") is overstated. More importantly, none of these non-Canadian examples covers Gran Chaco, South American, or Southern Cone disaster types. The presence of Yangtze River flood content ([D7]) is geographically proximate to a different river-flooding context than Pilcomayo/Bermejo, but the consequences described (urban industrial flooding, military deployment) bear no resemblance to Gran Chaco operational priorities (indigenous community access, dirt-road cutoffs, cross-border displacement).
- **Datapoint citations:**
  - [D7] Example 7 (train, infra=1): "Almost 4 million people across China had been cut off by flood waters, 810,000 homes have collapsed and 2.8 million homes have been damaged in eight provinces as of July 18" — Chinese flood content in a Canadian newspaper; labeled for infrastructure but consequences (urban China scale) are entirely different from Gran Chaco deployment context.
  - [D8] Example 8 (train, infra=1, health=1): "The Jakarta Post reported that hundreds of houses, schools and other buildings sustained damage when one of the twin peaks of the volcano exploded. At least 20 people sustained minor injuries" — Indonesian volcanic eruption content; labeled for infrastructure and health, confirms non-Canadian labeled content exists but does not improve Gran Chaco relevance.
  - [D19] Example 27 (train, eco=1): "With about half the original 1.6-million-hectare swamp filled for development or drained for agriculture, the park includes about 202,000 hectares of marsh" — US Everglades content labeled ecological; confirms US environmental content present in benchmark.

#### MINOR

#### MINOR Concern 7: OCR degradation artifacts persist in mixed-context chunks, creating evaluation noise
- **Dimension(s):** IF
- **Observation:** Several examples contain clearly OCR-degraded text that survived post-correction. Example 16 contains character strings like "Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35 -1 Gift sir 14000 33 30 33 1 Aloha gld 10000 85 80 80 5 Clinedev 1600 0 0 0." Example 17 (a chunk of the same article as Example 3) begins with advertisements including "Q. SIBBALD, 3 WINDSOR HOTEL, MONTREAL Telegraph and Telephone Supplies, STEEL AND IRON BEAMS." Example 30 has heavily degraded financial table content with OCR artifacts.
- **Deployment relevance:** The deployment system processes social media posts where noise takes the form of informal orthography, abbreviations, and code-switching — not OCR artifacts from physical newspaper digitization. Model robustness to OCR noise does not transfer to robustness to social media noise. The specific noise patterns in the benchmark (column layout fragmentation, numerical table corruption) are irrelevant to the deployment input distribution.
- **Datapoint citations:**
  - [D11] Example 16 (train, all=0): "-2 City res y 5000 5 5 5 Aiexavn 8000 50 50 50 Ckearcdnf 835 825 25 JS 1 Almaden 1000 35 35 35 -1 Gift sir 14000 33 30 33 1 Aloha gld 10000 85 80 80" — OCR-degraded financial table with column fragmentation artifacts.
  - [D21] Example 17 (train, infra=1): "Q. SIBBALD, 3 WINDSOR HOTEL, MONTREAL Telegraph and Telephone Supplies, STEEL AND IRON BEAMS MIDDLETON & MEREDITH, 30 St John Street, Montreal" — Mixed-context chunk that begins with advertisement text before the disaster content; OCR column layout artifacts persist.

#### MINOR Concern 8: weather_type field has high missingness and inconsistent values
- **Dimension(s):** IO
- **Observation:** Of the 31 reviewed examples, 20 have `weather_type` of "Nan" (string null) or `*null*`. Only 11 have a labeled weather type. This field was intended to represent the LDA-derived weather event classification, but a large proportion of the mixed-context chunks either inherit no weather type from segmentation or were not classified. This means the benchmark's claimed 15 LDA-derived weather event types are not reliably captured per example in the HF dataset.
- **Deployment relevance:** If downstream users attempted to use the `weather_type` field to filter benchmark examples by event type (e.g., to evaluate model performance on flood-related articles specifically, as the deployment prioritizes), this field is unreliable for doing so. This limits the benchmark's utility for any sub-analysis by event type that might partially approximate Gran Chaco flood-disaster content.
- **Datapoint citations:**
  - [D1] Example 1 (train, weather_type="Nan"): "John's Cloudy -4 -4 United States Max Min Atlanta Cloudy 17 4" — Weather forecast table with no weather_type label assigned despite clear weather content.
  - [D4] Example 4 (train, weather_type="Nan"): "Police say the aggravated assault charge against Clarkson involves a February attack on Boland in which the celebrity photographer's face and chest were splashed with concentrated sulphuric acid." — Crime report with no weather content, also weather_type="Nan"; the field does not distinguish weather-relevant from weather-irrelevant null entries.

---

### Content Coverage Summary

The 31 reviewed examples are drawn from the mixed-context (chunked, ~250-token) version of the dataset. The content spans English-language text from three Canadian newspapers (La Presse, La Patrie, Montreal Gazette) across two time periods (historical: 1880s–1890s; modern: 1990s–2000s). The actual content is considerably more heterogeneous than the benchmark's framing suggests: approximately two-thirds of the reviewed examples contain either no weather content at all (crime reports, stock tables, crossword clues, horse racing results, film reviews, political news) or weather content that has been annotated as having zero impact. This reflects the mixed-context chunking process, which segments full articles into ~250-token pieces and independently annotates each chunk — generating many content-free negative examples.

The labeled positive examples demonstrate that the benchmark can capture broadly defined impact categories (infrastructure disruption from 19th-century blizzards, agricultural and health impacts from large-scale floods), and the multi-label simultaneous annotation scheme is structurally sound. However, content drawn from outside Canada — China, Indonesia, the United States, Europe — is present in the labeled portion of the dataset, indicating the LDA topic model selected some international wire service content from the Montreal Gazette.

The register is uniformly formal English journalistic prose. No Spanish, no social media content, no indigenous-language vocabulary, and no content reflecting Southern Cone geographic or institutional contexts appears in any reviewed example. The annotation logic, as visible in the data, emphasizes textual explicitness of direct physical consequences, sometimes to the exclusion of events that operational emergency professionals would classify as impactful (e.g., weather-caused human casualties labeled all-zero in Examples 6 and 20).

---

### Limitations

1. **Sample size**: 31 examples from the 970-example training split (3.2%) were reviewed. Label distribution patterns, especially for positive examples in rare categories (Political, Ecological), may not be fully represented in this sample. The full test split (208 examples) was not reviewed.

2. **Test split not reviewed**: The benchmark's evaluation uses the test split; the training split reviewed here may have a different proportion of positive examples, different OCR degradation levels, or different geographic source distribution.

3. **Long-context version not reviewed**: The 350-example long-context version (avg. 2,987 tokens per article) is a separate dataset configuration. The chunking artifacts and noise content observed here may be less prevalent in the long-context version where full articles are retained. The HF dataset reviewed (`wximpactbench-1386`) is the mixed-context version only.

4. **Annotation guidelines not directly inspectable**: The annotation guidelines referenced in the benchmark documentation (Tables 14 and 15 of the paper) are described in the YAML but not directly accessible in the HF dataset record. The specific definitional scope of each category and the guidance for edge cases can only be inferred from examples.

5. **No direct access to ranking-based QA data**: The pseudo-questions generated by GPT-4O for the ranking task are not present in the HF dataset reviewed; only the classification labels are available. The QA task's validity for the deployment cannot be assessed from this dataset alone.

6. **Cannot assess inter-annotator agreement**: The HF dataset contains no annotation metadata (annotator IDs, confidence scores, disagreement flags). Label reliability must be inferred from the pattern of observed edge cases.

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
  "region": "Gran Chaco Tri-Border Emergency Response Zone",
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
