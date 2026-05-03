I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **MILU — A Multi-task Indic Language Understanding Benchmark** is valid for use in **Mymensingh Environmental Scientist — Cross-Regional South Asian Agricultural Knowledge**.

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

- **Name**: milu
- **Full Name**: MILU — A Multi-task Indic Language Understanding Benchmark
- **Domain**: Multilingual Indic language understanding and culturally specific knowledge evaluation
- **Languages**: bn, gu, hi, kn, ml, mr, or, pn, ta, te, en
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
MILU's task taxonomy spans 8 domains and 41 subjects, including Arts and Humanities,
Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine,
Science, Engineering and Technology, and Business Studies [Q38]. The benchmark is
explicitly designed to evaluate "general problem-solving abilities and India-specific
knowledge" [Q19] with emphasis on culturally relevant subjects such as "local history,
arts, festivals, and laws" [Q17]. The 41 subjects were derived by embedding and
K-means clustering approximately 20,000 fine-grained topic tags [Q35, Q36], followed
by manual review [Q37], and detailed subject-level statistics are reported across all
11 languages [Q99]. Evaluated models include frontier proprietary LLMs [Q128] as well
as Indic-language-specific models adapted from English base LLMs [Q57].

The taxonomy's India-centric framing is a structural feature, not incidental: while
an "Environmental Sciences" domain exists, there is no Bangladesh-specific sub-domain,
no haor/beel wetland agricultural category, and no cross-border water-management
subject within the 41-subject taxonomy. The authors themselves acknowledge that
"models perform poorly in culturally relevant areas like Arts & Humanities and Law &
Governance compared to general fields like STEM" [Q6, Q68], attributing this to
insufficient culturally specific data in training corpora [Q69] — a limitation that
extends to the benchmark's own subject taxonomy when viewed from a Bangladeshi
agro-ecological deployment context.

### Input Content
Data collection was designed with "an India-first perspective by collecting questions
from various national, state, and regional exams" [Q9], drawing from "over 1500
competitive exams from India" [Q11] — specifically national civil service exams,
state-level civil service exams, and government and private organization exams
[Q93, Q96, Q97, Q98]. Regional state exams are described as "particularly valuable
as they cover various state-level topics and emphasize the official language of each
state" [Q24]. English questions are included specifically because "these often address
Indian culture-specific content, which is notably missing from existing popular
benchmarks" [Q26]. In total, approximately 79,000 questions were released [Q42],
with a validation set of ~9,000 questions reserved for few-shot evaluation [Q47].
All data was scraped from publicly available resources [Q88], to be released under
permissible licenses [Q89].

The exclusive reliance on Indian competitive exam corpora means that every individual
datapoint reflects Indian educational, cultural, and policy contexts. There is no
representation of Bangladeshi exam institutions, Bangladeshi farming contexts,
Mymensingh dialect terminology, haor wetland ecology, or trans-border river-system
knowledge. The India-centric sourcing is confirmed by the authors as a design choice
[Q2, Q12] and is acknowledged as a scope limitation [Q82].

### Input Form
MILU's input format is exclusively text-based multiple-choice questions (MCQs) with
up to four answer options; the benchmark explicitly excludes "reading-comprehension-
style questions, images-based questions, and those with more than four answer options
to ensure uniformity and consistency" [Q29]. Multiple layers of automated and manual
cleaning were applied, including language identification via INDICLID and Unicode-based
filtering [Q30], deduplication [Q31], and final manual spot-checks per language [Q32].
For subject-language pairs with fewer than 100 questions, GPT-4O was used to translate
English questions into the target language [Q40, Q41]; approximately 25% of total
questions are machine-translated [Q43]. Detailed topic and language distribution
statistics are documented [Q94].

The text-only, standardized MCQ format is broadly compatible with a text-based
deployment environment, but the exam-register phrasing style differs from the natural
query style of a domain expert in Bangladesh. The machine-translation pipeline
introduces an additional risk: Bengali questions translated from English via GPT-4O
may carry Indian Bengali register conventions rather than Bangladeshi Bengali norms.
The authors acknowledge that "the scarcity of questions necessitated translating a
portion of the dataset" as a limitation [Q84].

### Output Ontology
MILU's output label set consists of standard MCQ answer keys derived from Indian
competitive exam corpora. The 41 subject labels and 8 domain categories were
constructed by merging approximately 20,000 fine-grained tags [Q35] into a single
unified taxonomy [Q38]. About 45% of questions arrived pre-tagged from source portals,
while the remainder received automated labels via GPT-4O-MINI [Q33, Q34]. The
benchmark covers "culturally relevant subjects such as local history, arts, festivals,
and laws, alongside traditional academic subjects like science" [Q10].

The output taxonomy is India-derived and validated against Indian educational
standards. For the deployment context, the single-correct-answer MCQ label
structure cannot capture the cross-border pluralism of agro-ecological knowledge
or the multi-perspective reasoning required for India–Bangladesh water-management
questions, where Indian exam answer keys may encode nationally partial perspectives.
Domain-wise analysis confirms poor performance in culturally relevant areas [Q16],
and the authors note that "bridging this gap requires a more inclusive data
distribution that ensures equitable representation of all cultures and languages" [Q70].

### Output Content
The primary annotation pathway relied on Indian exam portals, where "subject experts
ensure the accuracy of the answers" and questions are "tagged manually with topic
names and language details" [Q22]. Additional human annotation occurred during manual
cluster review for subject label assignment [Q37], and AI4Bharat team volunteers
conducted manual audits [Q87]. Approximately 45% of questions arrived pre-labeled
from source portals [Q33]; the remainder received GPT-4O-MINI-generated topic
assignments [Q34].

There is no documentation of inter-annotator agreement metrics, no description of
annotator demographics beyond AI4Bharat affiliation, and no mention of Bangladeshi
subject-matter experts, agronomists, or environmental scientists in the annotation
pool. The annotation pipeline is structurally Indian in origin, and the acknowledged
limitations of model performance in culturally relevant domains [Q68, Q69] suggest
that answer key provenance for arts, humanities, social science, and law questions
reflects Indian educational norms exclusively. For trans-border water-agreement or
Bangladesh-specific agricultural practice questions, no such questions exist in the
dataset to evaluate — and if they did, Indian exam answer keys would not constitute
cross-border authoritative ground truth.

### Output Form
MILU evaluates model performance via accuracy on MCQ tasks. For non-API-based models,
the log-likelihood method is used — selecting the answer option with the highest
conditional log probability via LM-EVALUATION-HARNESS [Q48, Q49, Q50, Q51]. API-
based models are evaluated generatively and "explicitly prompted to generate the
correct response in a structured JSON format to simplify response parsing" [Q53].
Evaluations span 0-shot, 1-shot, and 5-shot setups [Q46], with both base and
instruction-tuned model variants assessed [Q45]. Detailed subject-wise tables are
provided for all evaluated models across all 11 languages [Q100–Q132].

The log-likelihood MCQ scoring methodology is functionally valid for a text-based
deployment but suppresses open-ended agricultural reasoning. The authors acknowledge
that "our evaluation primarily relies on the log-likelihood approach, which may yield
different results compared to other established methods, such as generation-based
evaluation and chain-of-thought (CoT) prompting" [Q85]. For the deployment context,
the MCQ format cannot capture nuanced agro-ecological knowledge or multi-step
environmental reasoning. Instruct models exhibit inconsistent behavior under few-shot
prompting, sometimes degrading rather than improving [Q62, Q63], which is relevant
for deployment scenarios using instruction-tuned regional LLMs.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge." |
| Q2 | 1 | input_content | "With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science." |
| Q3 | 1 | output_form | "We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q4 | 1 | output_form | "Open multilingual models outperform language-specific fine-tuned models, which perform only slightly better than random baselines." |
| Q5 | 1 | output_content | "Models also perform better in high-resource languages as compared to low-resource ones." |
| Q6 | 1 | input_ontology | "Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM." |
| Q7 | 1 | input_ontology | "To the best of our knowledge, MILU is the first of its kind benchmark focused on Indic languages, serving as a crucial step towards comprehensive cultural evaluation." |
| Q8 | 1 | output_content | "Sshubam Verma1 Mohammed Safi Ur Rahman Khan1,2 Vishwajeet Kumar3 Rudra Murthy3 Jaydeep Sen3 1Nilekani Centre at AI4Bharat 2Indian Institute of Technology, Madras 3IBM Research, India" |
| Q9 | 2 | input_content | "We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams." |
| Q10 | 2 | output_ontology | "These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science." |
| Q11 | 2 | input_content | "We create this benchmark by collecting questions from over 1500 competitive exams from India." |
| Q12 | 2 | input_content | "We focus on region-specific exams to authentically capture local knowledge in the respective language." |
| Q13 | 2 | output_form | "We evaluate 45 different LLMs - a mix of closed proprietary, open-source, and language-specific models- on MILU." |
| Q14 | 2 | output_form | "Our findings suggest that models struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q15 | 2 | output_form | "Our analysis of in-context learning reveals that adding more examples improves performance in base models, but the effect on instruct models remains inconclusive." |
| Q16 | 2 | output_ontology | "Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM." |
| Q17 | 3 | input_ontology | "MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge." |
| Q18 | 3 | input_ontology | "This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others." |
| Q19 | 3 | input_ontology | "MILU is designed as a culturally relevant benchmark to assess general problem-solving abilities and India-specific knowledge." |
| Q20 | 3 | input_content | "These questions were sourced following an approach similar to AGIEVAL (Zhong et al., 2023), collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams, among others." |
| Q21 | 3 | input_content | "We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages." |
| Q22 | 3 | output_content | "These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers." |
| Q23 | 3 | input_content | "Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years." |
| Q24 | 3 | input_content | "Regional state exams are particularly valuable as they cover various state-level topics and emphasize the official language of each state." |
| Q25 | 3 | input_content | "In total, we collected more than 150K questions across 11 Indian Languages- Bengali (bn), Gujarati (gu), Hindi (hi), Kannada (kn), Malayalam (ml), Marathi (mr), Odia (or), Punjabi (pn), Tamil (ta), Telugu (te), and English (en)-spanning 41 diverse subjects." |
| Q26 | 3 | input_content | "English questions are also included as these often address Indian culture-specific content, which is notably missing from existing popular benchmarks." |
| Q27 | 4 | input_form | "Despite our best efforts to maintain the quality of questions collected, some amount of noise or errors may still be present. To address potential noise in the questions, we employ multiple layers of manual and automated cleaning filters." |
| Q28 | 4 | input_form | "Initially, we manually review a large sample of questions to detect and eliminate potential sources of noise." |
| Q29 | 4 | input_form | "During the collection process, we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency." |
| Q30 | 4 | input_form | "To remove incorrect language entries, we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering (Khan et al., 2024), ensuring that the questions are in the correct language." |
| Q31 | 4 | input_form | "To further refine the dataset, we remove any duplicate questions to retain only the unique ones." |
| Q32 | 4 | input_form | "As a final step, we manually verify a sample of questions from each language to ensure accuracy and correct any remaining errors." |
| Q33 | 4 | output_ontology | "Upon examination, we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information." |
| Q34 | 4 | input_form | "To address this issue, we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question." |
| Q35 | 4 | output_ontology | "Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap." |
| Q36 | 4 | output_ontology | "To organize them, we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters." |
| Q37 | 4 | output_content | "We manually review these clusters and assign appropriate subject labels." |
| Q38 | 4 | output_ontology | "Following the manual merging of related clusters, we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies." |
| Q39 | 4 | input_form | "Finally, we observed that some topics in certain languages had less than 100 questions. To ensure thorough evaluation across all subjects and languages, we aimed to have at least 100 questions per subject in each language." |
| Q40 | 4 | input_form | "For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O." |
| Q41 | 4 | input_form | "We chose GPT-4O over specialized translation models for their ability to remain task-aware during translation (Ahuja et al., 2024), ensuring the translated content aligns with the intent of the question." |
| Q42 | 4 | input_content | "In total, we release around 79K questions across 41 subjects across 8 domains in 11 languages, capping each subject-language pair at 500 questions for feasible evaluations." |
| Q43 | 4 | input_content | "Table 2 shows the overall statistics of MILU. Of the total 79K questions, only 25% of questions are translated from English, with the remainder" |
| Q44 | 5 | output_form | "We evaluate 42 different models on MILU, including large proprietary models, open-source multilingual models, and popular fine-tuned models specific to Indic languages." |
| Q45 | 5 | output_form | "Both the base versions and instruction fine-tuned variants of these models, wherever applicable, are evaluated to measure the improvements gained from fine-tuning." |
| Q46 | 5 | output_form | "All models, except for proprietary models and LLAMA-3.1-405B, are tested under 0-shot, 1-shot, and 5-shot setups." |
| Q47 | 5 | input_content | "We maintain a separate validation set of approximately 9,000 questions to serve as examples for few-shot evaluations." |
| Q48 | 5 | output_form | "For non-API-based models, we use the LM-EVALUATION-HARNESS (Gao et al., 2024; Biderman et al., 2024) to ensure clean and reproducible evaluations." |
| Q49 | 5 | output_form | "We use the log-likelihood method, where the probability of a given output string is computed by conditioning it on some provided input (Brown et al., 2020)." |
| Q50 | 5 | output_form | "Specifically, the log-likelihood of an answer (a) given the question (x), i.e., logP(a\|x), is calculated by concatenating the answer (a) with question (x), and then summing up the log probabilities, of each target token." |
| Q51 | 5 | output_form | "For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability, i.e., argmax(logP(a1\|x), ..., logP(ak\|x))." |
| Q52 | 5 | output_form | "The API-based models are evaluated using the generative approach due to the lack of support for prompt log probabilities." |
| Q53 | 5 | output_form | "We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing." |
| Q54 | 5 | output_form | "Due to the high costs involved, these models are evaluated only in the zero-shot setup." |
| Q55 | 6 | output_form | "We report 5-shot accuracies for all open models (except for LLAMA-3.1-70B-INSTRUCT & LLAMA-3.1-405B for which we report 0-shot accuracy) with the accuracy averaged across all the domains per language." |
| Q56 | 6 | input_content | "We evaluate around 16 Indic language LLMs on MILU." |
| Q57 | 6 | input_ontology | "These models are primarily built by adapting English LLMs, such as LLAMA-2-7B, by first continually pretraining on small amount Indic language data, followed by optionally instruction finetuning them." |
| Q58 | 6 | output_form | "As seen from Table 4, across languages, the models exhibit average performance comparable to random baselines, with minimal variations among them." |
| Q59 | 6 | output_ontology | "When analyzed across domains, the models generally perform worse in Arts, Humanities, and Social Sciences than in STEM subjects." |
| Q60 | 6 | output_form | "We compare the performance of different Base and Instruct models across zero, one, and five-shot setups." |
| Q61 | 6 | output_form | "As shown in Figure 3, the performance of base models consistently improves with an increasing number of in-context examples, with the 5-shot setup yielding the best results." |
| Q62 | 6 | output_form | "In contrast, Instruct models exhibit more varied behavior, where models either stagnate or even degrade in performance." |
| Q63 | 6 | output_form | "This also aligns with expectations, as Instruct models are specifically fine-tuned as conversation assistants and may not respond well to the few-shot in-context examples format." |
| Q64 | 7 | output_form | "We evaluate the LLAMA and GEMMA family of models, ranging from 1B to 405B parameters, to analyze how performance scales with model size." |
| Q65 | 7 | output_form | "Figure 5 shows that the model performance improves significantly with increasing scale." |
| Q66 | 7 | output_form | "Notably, instruction-tuned models in the LLAMA family show more substantial improvements as compared to those in the GEMMA family." |
| Q67 | 7 | output_form | "We analyze the performance of various base and instruct models across multiple domains and languages." |
| Q68 | 7 | output_ontology | "Similar trends to those in Section (§5.2) are observed where the open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields." |
| Q69 | 7 | output_content | "This suggests that the training corpora for these models lack sufficient culturally specific data." |
| Q70 | 7 | output_content | "Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages." |
| Q71 | 7 | output_form | "As most Indic LLMs are built on English base models like LLAMA-2-7B, we assess the impact of language adaptation on their performance." |
| Q72 | 7 | output_form | "Table 5 compares language-specific models with the original LLAMA-2-7B, and instruction-tuned models with LLAMA-2-7B-CHAT." |
| Q73 | 7 | output_form | "Our findings show minimal gains, with some models even underperforming post-adaptation." |
| Q74 | 8 | input_ontology | "In this paper, we introduced MILU—Multilingual Indic Language Understanding Benchmark-a comprehensive benchmark specifically designed to evaluate LLMs across 11 Indic languages, spanning diverse domains and culturally relevant subjects." |
| Q75 | 8 | output_form | "We evaluate 45 different LLMs and find that the majority of LLMs struggle on MILU, with GPT4o achieving the highest average accuracy." |
| Q76 | 8 | input_form | "The analysis also shows that models perform significantly better in high-resource languages than low-resource ones, highlighting the need for more robust multilingual strategies." |
| Q77 | 8 | output_ontology | "Additionally, the domain-specific analysis indicates that models perform better in general fields such as STEM while facing challenges in culturally relevant subjects like Arts, Humanities, and Law, highlighting the lack of this knowledge in the current models and datasets." |
| Q78 | 8 | output_form | "We conjecture that limited performance gains may result from small language-specific datasets and reliance on parameter-efficient methods like LoRA (Hu et al., 2022)." |
| Q79 | 8 | output_content | "Another contributing factor could be the lack of diversity in instruction fine-tuning datasets." |
| Q80 | 8 | output_content | "Models like AIRAVATA, which utilize more diverse data (Gala et al., 2024), exhibit noticeably better performance." |
| Q81 | 8 | output_form | "Further investigation is required to fully understand the limitations and opportunities in this area." |
| Q82 | 9 | input_ontology | "First, we restricted our study to the top 11 languages due to the lack of readily available questions in low-resource languages, which we aim to address in future work." |
| Q83 | 9 | output_form | "Second, limited computational resources prevented a thorough evaluation of larger models, such as LLAMA-3.1-70B-INSTRUCT and LLAMA-3.1-405B." |
| Q84 | 9 | input_form | "Third, the scarcity of questions necessitated translating a portion of the dataset." |
| Q85 | 9 | output_form | "Finally, our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting." |
| Q86 | 9 | output_content | "We would like to thank EkStep Foundation and Nilekani Philanthropies for their generous grant towards building datasets, models, tools and other resources for Indian languages." |
| Q87 | 9 | output_content | "We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits." |
| Q88 | 9 | input_content | "All data described in this work was scraped from publicly available resources." |
| Q89 | 9 | input_content | "The datasets used in this paper will be made available under permissible licenses." |
| Q90 | 9 | output_form | "Additionally, the code used for our evaluations will be made publicly available under the MIT License." |
| Q91 | 9 | output_content | "We only used ChatGPT for assistance purely with the language of the paper, e.g., paraphrasing, spell-checking, or polishing the author's original content, without suggesting new content." |
| Q92 | 10 | input_content | "Sumanth Doddapaneni, Rahul Aralikatte, Gowtham Ramesh, Shreya Goyal, Mitesh M. Khapra, Anoop Kunchukuttan, and Pratyush Kumar. 2023. Towards leaving no Indic language behind: Building monolingual corpora, benchmark and models for Indic languages. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 12402–12426, Toronto, Canada. Association for Computational Linguistics." |
| Q93 | 17 | input_content | "We collected our questions from over 40 exam types ranging from various National and state level civil service examinations to examinations conducted by various government and private organizations." |
| Q94 | 17 | input_form | "Detailed analysis of topic and language distribution across languages can be found in Table 9 and Figure 6" |
| Q95 | 17 | output_form | "Model details about the different models evaluated in this work is present in Table 10." |
| Q96 | 18 | input_content | "Table 6: Overview of various national-level exams and the corresponding years of coverage considered in MILU." |
| Q97 | 18 | input_content | "Table 7: Overview of various government and private organization exams and the corresponding years of coverage considered in MILU." |
| Q98 | 18 | input_content | "Table 8: Overview of various State-level civil services exams and the corresponding years of coverage considered in MILU." |
| Q99 | 20 | input_ontology | "Table 9: Detailed subject level statistics of MILU across different languages." |
| Q100 | 22 | output_form | "Table 11: Detailed subject-wise evaluation for ABHINAND/TAMIL-LLAMA-7B-INSTRUCT-V0.2 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q101 | 23 | output_form | "Table 12: Detailed subject-wise evaluation for AI4BHARAT/AIRAVATA on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q102 | 24 | output_form | "Table 13: Detailed subject-wise evaluation for BHABHAAI/GAJENDRA-V0.1 on MILU across different languages." |
| Q103 | 24 | output_form | "The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q104 | 25 | output_form | "Table 14: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-BASE-V0.1 on MILU across different languages." |
| Q105 | 26 | output_form | "Table 15: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q106 | 27 | output_form | "Table 16: Detailed subject-wise evaluation for GENVRADMIN/ARYABHATTA-GEMMAGENZ-VIKAS-MERGED on MILU across different languages." |
| Q107 | 28 | output_form | "Table 17: Detailed subject-wise evaluation for MANISHIITG/OPEN-ADITI-V6-LLAMA3 on MILU across different languages." |
| Q108 | 29 | output_form | "Table 18: Detailed subject-wise evaluation for NICKMALHOTRA/PROJECTINDUS on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q109 | 30 | output_form | "Table 19: Detailed subject-wise evaluation for SARVAMAI/OPENHATHI-7B-HI-V0.1-BASE on MILU across different languages." |
| Q110 | 31 | output_form | "Table 20: Detailed subject-wise evaluation for TENSOIC/KAN-LLAMA-7B-BASE on MILU across different languages." |
| Q111 | 32 | output_form | "Table 21: Detailed subject-wise evaluation for ABHINAND/MALAYALAM-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q112 | 33 | output_form | "Table 22: Detailed subject-wise evaluation for ABHINAND/TELUGU-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q113 | 34 | output_form | "Table 23: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-INSTRUCT-V0.1 on MILU across different languages." |
| Q114 | 35 | output_form | "Table 24: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-BASE-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q115 | 36 | output_form | "Table 25: Detailed subject-wise evaluation for TELUGU-LLM-LABS/TELUGU-LLAMA2-7B-V0-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q116 | 37 | output_form | "Table 26: Detailed subject-wise evaluation for GPT-4o on MILU across different languages. The results reported are for 0-shot experiments." |
| Q117 | 38 | output_form | "Table 27: Detailed subject-wise evaluation for GPT-4O-MINI on MILU across different languages. The results reported are for 0-shot experiments." |
| Q118 | 39 | output_form | "Table 28: Detailed subject-wise evaluation for GEMINI-1.5-PRO on MILU across different languages. The results reported are for 0-shot experiments." |
| Q119 | 40 | output_form | "Table 29: Detailed subject-wise evaluation for GEMINI-1.5-FLASH on MILU across different languages. The results reported are for 0-shot experiments." |
| Q120 | 41 | output_form | "The results reported are for 0-shot experiments." |
| Q121 | 42 | output_form | "Table 31: Detailed subject-wise evaluation for SARVAMAI/SARVAM-1 on MILU across different languages. The results reported are for 5-shot experiments." |
| Q122 | 44 | output_form | "Table 34: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B on MILU across different languages." |
| Q123 | 44 | output_form | "Table 35: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B-IT on MILU across different languages." |
| Q124 | 47 | output_form | "Table 39: Detailed subject-wise evaluation for NVIDIA/NEMOTRON-4-MINI-HINDI-4B-BASE on MILU across different languages. The results reported are for 5-shot experiments." |
| Q125 | 48 | output_form | "Table 40: Detailed subject-wise evaluation for META-LLAMA/LLAMA-2-7B-HF on MILU across different languages." |
| Q126 | 48 | output_form | "Table 41: Detailed subject-wise evaluation for META-LLAMA/LLAMA-2-7B-CHAT-HF on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q127 | 49 | output_form | "Table 42: Detailed subject-wise evaluation for NEULAB/PANGEA-7B on MILU across different languages. The results reported are for 5-shot experiments." |
| Q128 | 52 | input_ontology | "Table 47: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-9B-IT on MILU across different languages." |
| Q129 | 52 | output_form | "Table 48: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-27B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q130 | 55 | output_form | "Table 52: 0-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q131 | 56 | output_form | "1-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q132 | 57 | output_form | "Table 54: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.1-405B on MILU across different languages. The results reported are for 0-shot experiments." |

---

## Regional Context

```yaml
name: Mymensingh Environmental Scientist — Cross-Regional South Asian Agricultural
  Knowledge
abbreviation: BGD-MYMENSINGH-AGRI-SCI
assessment_context:
  benchmark: MILU — A Multi-task Indic Language Understanding Benchmark
  benchmark_year: 2024
  deployment_use_case: An environmental scientist based in Mymensingh, Bangladesh
    uses LLMs (both frontier and region-specific small models) to retrieve and reason
    over agricultural and environmental science knowledge spanning South Asian regions
    — including the Bangladeshi delta system, Bangladeshi Bengali-specific farming
    contexts, and contrasting agro-ecological zones in India (Telangana dry-land cropping,
    Andhra Pradesh coastal aquaculture).
  assessment_purpose: Evaluate MILU's validity as an agricultural and environmental
    science knowledge benchmark for this cross-regional, multilingual deployment context.
target_population:
  description: Environmental scientists and agronomists based primarily in Mymensingh
    district, Bangladesh, querying LLMs for professional-grade agricultural and environmental
    science knowledge. The deployment spans sub-national agro-ecological contexts
    in Bangladesh and cross-references Indian agricultural zones (Telangana/Andhra
    Pradesh, West Bengal). Users are likely to query in a mix of Bangladeshi Bengali
    and English, and may also encounter or generate queries in standard Indian Bengali
    or Telugu.
  geography:
    primary_country: Bangladesh
    primary_district: Mymensingh
    sub_national_zones:
    - zone: Brahmaputra-Jamuna floodplain farming belt (Mymensingh district)
      notes: Char-land agriculture, flood-recession cropping, boro and aman rice cultivation;
        floodplain ecology defines dominant agronomic calendar
    - zone: Haor wetland ecology zones (greater Mymensingh / Sylhet border region)
      notes: Beel and haor farming systems; deep-water rice and fisheries; seasonal
        inundation patterns drive distinct crop calendars
    cross_reference_zones:
    - zone: Telangana (India) — dry-land cropping belt
      notes: 'Hot semi-arid Deccan plateau agro-ecological zone (AER-7 in Indian AER
        classification), characterized by red and black soils. Dryland farming is
        dominant practice. Primary kharif crops: cotton (18.13 lakh ha — largest crop
        by area), sorghum (jowar), pigeonpea (red gram), maize, groundnut, and pulses.
        Primary rabi crops: sorghum, safflower, sunflower, gram. The state is divided
        into Northern Telangana Zone (810–1,135 mm rainfall, semiarid moist tropical)
        and Southern Telangana Zone (560–970 mm, semiarid dry tropical). Sources:
        PJTSAU Crops of Telangana — [WEB-1]; Telangana
        SLBC State Profile — [WEB-2]'
    - zone: Andhra Pradesh (India) — coastal aquaculture zone
      notes: 'Andhra Pradesh ranks first in both coastal and freshwater aquaculture
        in India, contributing nearly 40% of total marine aquaculture production.
        Dominant species: Litopenaeus vannamei (Pacific white shrimp, dominant export
        crop), Penaeus monodon (Black Tiger shrimp, growing ~142% 2019–2024), scampi.
        Regulatory framework: Coastal Aquaculture Authority Act 2005 (amended 2023,
        with updated rules effective 9 January 2024) governs farm registration (5-year
        renewable) and SPF L. vannamei culture permissions. State-level body: Andhra
        Pradesh State Aquaculture Development Authority (APSADA Act 2020). Export
        oversight: MPEDA (Marine Products Export Development Authority, est. 1972)
        monitors residues under the National Residue Control Plan and operates quality-control
        labs at Nellore and Bhimavaram, AP. As of 30 October 2024, CAA had 46,976
        registered coastal farms nationally, with AP holding the largest share. Sources:
        CAA official site — [WEB-3]; PIB press release Oct 2024 —
        [WEB-4]; MPEDA state-wise
        production — [WEB-5]'
    - zone: West Bengal (India) — deltaic rice-farming zone
      notes: Shares agro-ecological and linguistic context with Mymensingh; the Indian
        Bengali benchmark corpus primarily reflects West Bengal exam conventions
    transboundary_hydrology: The Ganges–Brahmaputra–Meghna (GBM) river system defines
      the agro-hydrological context. Shared rivers (Ganges/Farakka, Teesta, Brahmaputra)
      and bilateral water-sharing agreements between India and Bangladesh create cross-border
      policy dimensions material to the deployment.
languages:
  primary_query_languages:
  - Bangladeshi Bengali (Mymensingh regional dialect)
  - Standard Bangladeshi Bengali (written/formal register)
  - English (secondary; used for scientific literature queries)
  cross_reference_languages:
  - Standard Indian Bengali (West Bengal variant — the register reflected in MILU's
    Bengali corpus)
  - Telugu (for Telangana/Andhra agro-ecological content)
  dialect_and_register_notes: Mymensingh district Bengali is a distinct regional dialect
    of Bangladeshi Bengali, with phonological, lexical, and grammatical features differing
    from both Standard Bangladeshi Bengali and West Bengal Bengali. Agricultural terminology
    in Mymensingh dialect (local crop names, beel/haor/char land-tenure vocabulary,
    irrigation terms) is not represented in MILU's Bengali corpus, which derives from
    West Bengal and Indian national exam registers. Domain experts in this deployment
    would query in a naturalistic professional register, not the exam-style standardized
    phrasing MILU uses.
  script: Bengali script (Eastern Nagari variant); Telugu script for Telugu-language
    content; Latin script for English queries
  script_notes: Bengali script is shared between Bangladeshi and Indian Bengali, but
    orthographic conventions and exam-register norms differ. MILU's Bengali content
    was sourced and partially machine-translated within Indian Bengali conventions;
    Bangladeshi-register nuances are unrepresented.
  machine_translation_risk: Approximately 25% of MILU questions are machine-translated
    from English into target languages using GPT-4O. For Bengali, translated questions
    likely carry Indian Bengali register conventions rather than Bangladeshi Bengali
    norms, introducing a systematic stylistic and terminological bias for this deployment
    population.
  net_new_bangladeshi_bengali_benchmark: 'BEnQA (arXiv:2403.10900, 2024) is a Bangladeshi
    Bengali science QA benchmark of ~5,161 parallel Bengali–English questions drawn
    from the Bangladeshi national curriculum for grades 8–12, covering physics, chemistry,
    biology, and mathematics. It benchmarks multiple LLMs and documents a significant
    Bengali–English performance gap and benefits of English translation prompting.
    BEnQA is not an agricultural domain benchmark, but it is the closest existing
    Bangladeshi Bengali QA dataset and provides a performance baseline for LLMs on
    Bangladeshi-register Bengali science content — directly relevant for calibrating
    how much the MILU Bengali performance gap reflects language vs. cultural knowledge
    deficits. Source: arXiv 2403.10900 — [WEB-6]'
occupational_cohort:
  role: Environmental scientist / agronomist (professional domain expert)
  institutional_context: 'Key institutions employing environmental scientists in Mymensingh
    include: Bangladesh Agricultural University (BAU, founded 1961), a public university
    with 45 departments across 6 faculties (agriculture, agricultural economics and
    rural sociology, agricultural engineering and technology, animal husbandry, fisheries,
    veterinary science) and over 5,000 undergraduate and ~3,000 postgraduate students
    as of 2024; BAU''s campus also co-hosts Bangladesh Institute of Nuclear Agriculture
    (BINA) and Bangladesh Fisheries Research Institute (BFRI). Other key institutions
    include Bangladesh Agricultural Research Institute (BARI), Bangladesh Rice Research
    Institute (BRRI), Bangladesh Water Development Board (BWDB), and NGO research
    units. Sources: BAU official site — [WEB-7]; Wikipedia — [WEB-8];
    Banglapedia — [WEB-9]'
  professional_knowledge_domains:
  - Agro-ecological systems of the Brahmaputra-Jamuna floodplain
  - Haor and beel wetland ecology and farming systems
  - Boro, aman, and aus rice cultivation calendars specific to Bangladesh
  - Char-land (river-island) agriculture and flood-recession cropping
  - Trans-border river hydrology (GBM system, Farakka Barrage, Teesta)
  - 'Soil science: floodplain alluvial soils, hydromorphic soils of haor zones'
  - Integrated crop-fish farming systems
  - Climate change impacts on deltaic agriculture (sea-level rise, salinity intrusion,
    cyclone frequency)
  - Dry-land cropping systems of Telangana (cross-reference)
  - Coastal aquaculture (Andhra Pradesh) (cross-reference)
  query_behavior: Professional experts query in naturalistic, domain-specific language
    — not in the standardized MCQ exam-register used by MILU. Queries likely blend
    Bengali and English (code-switching), invoke local agricultural terminology, and
    require open-ended or multi-step reasoning rather than single-label MCQ responses.
  llm_usage_pattern: Uses both generic frontier LLMs (e.g., GPT-4o, Gemini) and region-specific
    small Indic LLMs for knowledge retrieval and reasoning over agricultural science
    content.
agro_ecological_systems:
  primary_systems_mymensingh:
  - system: Haor wetland farming
    description: Seasonally flooded bowl-shaped depressions; boro rice is the dominant
      single crop during dry season; deep-water and flash-flooding pose structural
      agronomic constraints
    key_terminology_gap: Haor, beel, boro cycle, flash flood, hoar basin — none represented
      in MILU subject taxonomy
  - system: Brahmaputra-Jamuna char-land agriculture
    description: Shifting river-island agriculture on newly accreted floodplain chars;
      short-cycle crops (mustard, maize, pulses) and flood-recession cropping; highly
      dynamic land tenure
    key_terminology_gap: Char, archar, diluvion/alluvion land rights, flood-recession
      cropping calendar — absent from MILU
  - system: Irrigated floodplain rice farming
    description: Triple-crop rotations (boro-aus-aman) in irrigated lowland areas;
      groundwater irrigation from shallow tubewells; arsenic contamination of irrigation
      water is a regional concern
    key_terminology_gap: '[NEEDS VERIFICATION — deferred: below search budget; verify
      arsenic-irrigation issue coverage in any MILU environmental science questions]'
  cross_reference_systems_india:
  - system: Telangana dry-land cropping
    region: Telangana, India
    description: 'Rain-fed agriculture on Deccan plateau red and black soils (AER-7,
      hot semi-arid). Dominant kharif crops: cotton (18.13 lakh ha, largest crop by
      area), sorghum, pigeonpea, maize, groundnut, soybean, pulses; dominant rabi
      crops: sorghum, safflower, sunflower, gram. Dryland farming is common practice
      in both Northern (moist semiarid) and Southern (dry semiarid) zones. Dryland
      watershed management is a documented policy priority. Sources: PJTSAU — [WEB-1];
      Lotusarise AER classification — [WEB-10]'
    milu_coverage_status: '[NEEDS VERIFICATION — deferred: below search budget; would
      require direct inspection of MILU Telugu question corpus to determine sub-regional
      agro-ecological specificity vs. generic Indian exam content]'
  - system: Andhra Pradesh coastal aquaculture
    region: Andhra Pradesh, India
    description: 'India''s leading coastal and freshwater aquaculture state (~40%
      of national marine aquaculture production). Dominant species: L. vannamei (Pacific
      white shrimp, dominant export commodity) and P. monodon; approximately 100,000
      shrimp farms nationally, majority in AP. Regulatory environment: Coastal Aquaculture
      Authority Act 2005 (amended 2023); CAA Rules 2024 (effective 9 January 2024)
      govern farm registration renewal fees and SPF broodstock import. State body:
      AP State Aquaculture Development Authority (APSADA, est. 2020). Export certification:
      MPEDA (Marine Products Export Development Authority, est. 1972 under MPEDA Act)
      oversees residue monitoring and export standards; labs at Nellore and Bhimavaram.
      Sources: CAA — [WEB-3]; PIB Oct 2024 — [WEB-4];
      MPEDA — [WEB-5]'
    milu_coverage_status: '[NEEDS VERIFICATION — deferred: below search budget; no
      evidence from MILU documentation that Telugu questions include coastal aquaculture
      content at sub-regional AP specificity]'
  - system: West Bengal deltaic rice farming
    region: West Bengal, India
    description: Shares Ganges delta ecology with Bangladesh; aman-boro rice systems;
      the Indian Bengali exam corpus in MILU primarily reflects this zone's agricultural
      context
    milu_coverage_status: Partially covered via West Bengal state-level exam content
      in MILU Bengali corpus; depth of agro-ecological coverage unconfirmed
transboundary_policy_context:
  description: India–Bangladesh shared river systems create a domain where Indian
    exam answer keys may encode nationally partial scientific and policy perspectives.
    This is a high-priority validity concern for the deployment.
  key_shared_rivers:
  - river: Ganges (Padma in Bangladesh)
    treaty: 'Ganges Water Sharing Treaty (GWST), signed 12 December 1996 at New Delhi
      for a 30-year term. The treaty is set to expire on 12 December 2026 with no
      automatic extension — renewal requires fresh mutual consent under Article XII.
      As of May 2026, formal renewal negotiations have been initiated but remain unresolved.
      India is seeking renegotiation on new terms (shorter 10–15 year duration, additional
      water allocation to West Bengal), and the shadow of India''s April 2025 suspension
      of the Indus Waters Treaty with Pakistan has complicated the bilateral environment.
      Bangladesh''s April 2026 diplomatic mission to New Delhi left renewal terms
      unresolved. Sources: The Diplomat, April 2026 — [WEB-11];
      The GeoStrata — [WEB-12];
      GKToday — [WEB-13]'
    dispute_notes: Farakka Barrage flow regulation is a longstanding point of contention;
      downstream impacts on Bangladesh agriculture and delta ecology are well-documented
      in Bangladeshi scientific literature. India's post-Pahalgam posture and West
      Bengal's electoral calendar add further friction. The treaty's expiry and contested
      renewal terms make any Indian exam answer key on Ganges water rights highly
      temporally unstable and nationally partial for 2024–2026 deployment contexts.
  - river: Teesta
    treaty: 'NO FORMAL TREATY EXISTS as of May 2026. A 1983 ad hoc agreement allocated
      39% to India and 36% to Bangladesh but was never made permanent. A 2011 draft
      proposal (India 42.5%, Bangladesh 37.5%) was blocked by West Bengal Chief Minister
      Mamata Banerjee. After the fall of Sheikh Hasina''s government in August 2024,
      Bangladesh''s interim government under Muhammad Yunus has expressed commitment
      to resuming talks. As of early 2025, Bangladesh extended the Teesta Master Plan
      deadline (originally with Chinese firm POWERCHINA) to December 2026. No bilateral
      water-sharing agreement has been concluded. Sources: Wikipedia — [WEB-14];
      Water Diplomat Aug 2025 — [WEB-15];
      TBS News Feb 2025 — [WEB-16]'
    dispute_notes: Teesta water sharing affects boro rice irrigation in northern Bangladesh;
      Indian and Bangladeshi official positions on flow allocation fundamentally differ.
      The dispute has intensified with Chinese infrastructure interest (Teesta River
      Comprehensive Management Project, ~$1 billion, now revived with POWERCHINA under
      the interim government). Indian and Bangladeshi exam corpora would encode categorically
      different authoritative positions on this contested domain.
  - river: Brahmaputra (Jamuna in Bangladesh)
    treaty: '[NEEDS VERIFICATION — deferred: below search budget; no confirmed tripartite
      India–China–Bangladesh formal agreement on Brahmaputra flow data sharing identified]'
    dispute_notes: Chinese dam construction on upper Brahmaputra adds complexity;
      flood early-warning data sharing between India and Bangladesh is a bilateral
      issue
  benchmark_validity_implication: MILU's Law and Governance domain and Environmental
    Sciences domain draw exclusively from Indian exam corpora. For trans-border water
    questions, Indian exam answer keys reflect Indian policy perspectives and may
    not be authoritative for a Bangladeshi environmental scientist's professional
    context. This is a confirmed HIGH-priority validity gap (OC dimension). The heightened
    policy volatility in 2024–2026 (Ganges treaty nearing expiry, Teesta unresolved,
    post-Hasina geopolitical shift) means that even nominally 'scientific' questions
    about river-flow volumes or agricultural water allocation carry nationally contested
    ground-truth dimensions.
benchmark_coverage_profile:
  languages_in_benchmark:
  - bn
  - te
  - en
  - hi
  - gu
  - kn
  - ml
  - mr
  - or
  - pn
  - ta
  deployment_languages_covered:
  - bn (Bengali — West Bengal variant, not Bangladeshi)
  - te (Telugu)
  - en (English)
  deployment_languages_not_covered:
  - Bangladeshi Bengali (Mymensingh dialect)
  - Bangladeshi Standard Bengali as distinct from Indian Bengali
  subject_domains_in_benchmark:
  - Arts and Humanities
  - Social Sciences
  - Environmental Sciences
  - Law and Governance
  - Health and Medicine
  - Science
  - Engineering and Technology
  - Business Studies
  relevant_subject_domains:
  - Environmental Sciences
  - Science
  subject_depth_for_deployment: Surface-level only (confirmed by user). MILU's Environmental
    Sciences domain derives from Indian general competitive exam content; no agro-ecological
    depth, no wetland ecology, no Bangladesh-specific agricultural content.
  question_count_in_relevant_domains: '[NEEDS VERIFICATION — deferred: below search
    budget; Table 9 of the MILU paper (NAACL 2025, pp. 10076–10132) contains subject-level
    statistics across all 11 languages; requires direct access to the paper appendix
    or the AI4Bharat/MILU GitHub repository dataset for exact per-subject per-language
    question counts. The GitHub repository (https://github.com/AI4Bharat/MILU) confirms
    the overall test set is ~85,000 questions across 41 subjects — slightly higher
    than the ~79K in the paper due to dataset updates]'
  bangladesh_specific_content: STRUCTURALLY ABSENT — MILU is India-only by design.
    No Bangladeshi exam institutions, no haor/beel/char-land content, no Bangladeshi
    annotators.
  bengali_corpus_origin: West Bengal state-level and Indian national exams only. Bangladeshi
    Bengali register absent. Machine-translated Bengali questions derived from Indian
    English sources.
  milu_github_note: 'The MILU GitHub repository (AI4Bharat/MILU) confirms the benchmark
    spans 8 domains and 41 subjects across 11 Indic languages with ''India-centric
    design incorporating material from regional and state-level examinations.'' Total
    test set is ~85,000 questions (slightly updated from paper''s ~79K). Source: GitHub
    — [WEB-17]'
dimension_priorities:
  input_ontology:
    priority: HIGH
    rationale: MILU's 41-subject taxonomy has no Bangladesh-specific agro-ecological
      subdomains. The Environmental Sciences domain exists but is surface-level and
      India-scoped. Haor wetland ecology, char-land agriculture, boro/aman rice systems,
      and trans-border river management are structurally absent from the taxonomy.
  input_content:
    priority: HIGH
    rationale: Every datapoint in MILU originates from Indian competitive exams. No
      Bangladeshi farming context, Mymensingh dialect terminology, or cross-border
      hydrological knowledge is represented. Individual Bengali questions carry West
      Bengal exam register conventions.
  input_form:
    priority: MODERATE
    rationale: Text-based, Bengali-script content is technically supported, but exam-register
      MCQ phrasing is misaligned with naturalistic domain-expert queries. Machine-translated
      Bengali content may carry Indian register artifacts.
  output_ontology:
    priority: MODERATE
    rationale: Single-correct-answer MCQ labels cannot capture cross-border pluralism
      in agro-ecological knowledge or multi-perspective reasoning on India–Bangladesh
      water management questions.
  output_content:
    priority: HIGH
    rationale: Ground-truth labels originate entirely from Indian exam corpora and
      reflect Indian educational and policy contexts. No Bangladeshi subject-matter
      experts or agronomists contributed to annotation. For Bangladesh-specific or
      trans-border agricultural/policy questions, Indian exam answer keys are not
      fully authoritative.
  output_form:
    priority: LOWER
    rationale: Both benchmark and deployment are text-based. MCQ format suppresses
      nuanced agricultural reasoning but the modality mismatch per se is minimal.
flagged_gaps_for_web_search:
- gap_id: GAP-1
  title: Bangladesh-specific agricultural knowledge absence in MILU
  description: MILU was constructed entirely from Indian competitive exams. Haor and
    beel wetland farming, boro and aman rice cultivation calendars, char-land agriculture,
    and flood-recession cropping in Mymensingh district are structurally absent.
  web_search_target: MILU benchmark Bangladesh agricultural content haor wetland Bengali
    questions Bangladeshi exam corpus
  verification_question: Does any MILU subject or question set include Bangladeshi
    agricultural content, or is the benchmark structurally India-only?
  resolution: 'CONFIRMED STRUCTURALLY ABSENT. The MILU GitHub repository and paper
    both confirm an exclusively India-centric design sourced from 1,500+ Indian competitive
    exams. No Bangladeshi exam institutions, agro-ecological content, or annotators
    are present. Source: AI4Bharat/MILU GitHub — [WEB-17]'
- gap_id: GAP-2
  title: Mymensingh/Bangladeshi Bengali dialect gap
  description: MILU's Bengali content derives from West Bengal state and Indian national
    exam corpora. Bangladeshi Standard Bengali and Mymensingh regional dialect agricultural
    vocabulary are unrepresented.
  web_search_target: Bangladeshi Bengali NLP benchmark Mymensingh dialect agricultural
    terminology LLM evaluation MILU Bengali subset
  verification_question: Does any MILU Bengali subset include questions authored or
    validated by Bangladeshi institutions or exam bodies?
  resolution: 'NOT FOUND IN MILU. However, a net-new relevant resource was identified:
    BEnQA (arXiv:2403.10900) is a Bangladeshi Bengali science QA benchmark of ~5,161
    parallel Bengali–English questions from the Bangladeshi national curriculum (grades
    8–12). It demonstrates a significant Bengali–English LLM performance gap on Bangladeshi-register
    content. BEnQA is science-focused (not agricultural domain), but provides a useful
    contrast and calibration benchmark. No MILU Bengali content originates from Bangladeshi
    institutions. Source: arXiv — [WEB-6]'
- gap_id: GAP-3
  title: Trans-border water and agricultural policy knowledge
  description: India–Bangladesh water-sharing agreements (Ganges/Farakka, Teesta)
    and jointly managed river systems create a domain where Indian exam answer keys
    may encode nationally partial perspectives.
  web_search_target: India Bangladesh water sharing agreement Teesta Ganges AI benchmark
    cross-border agricultural policy evaluation LLM
  verification_question: Does any MILU documentation address cross-border or politically
    contested agricultural/environmental topics?
  resolution: 'CONFIRMED UNADDRESSED IN MILU. No benchmark or NLP paper addressing
    trans-border India–Bangladesh water policy as a contested knowledge domain was
    found. The policy context has become more volatile in 2024–2026: Ganges treaty
    expires December 2026 with renegotiation actively contested; Teesta remains unresolved
    with no formal agreement. This significantly heightens the OC validity concern.
    Sources: The Diplomat — [WEB-11];
    Wikipedia Teesta — [WEB-14]'
- gap_id: GAP-4
  title: Depth of agricultural science coverage in MILU
  description: The user confirmed MILU's agricultural content is surface-level. The
    actual distribution of questions across the Environmental Sciences domain needs
    quantitative verification.
  web_search_target: MILU benchmark environmental sciences agriculture subject question
    distribution domain statistics Table 9 subject-level
  verification_question: How many MILU questions fall under agriculture, environmental
    science, or related applied science categories in Bengali and Telugu? What is
    the sub-subject breakdown?
  resolution: '[NOT FOUND — Table 9 subject-level statistics require direct access
    to the MILU paper appendix (NAACL 2025, pp. 10076–10132) or the GitHub dataset.
    The paper and GitHub confirm 41 subjects, ~85K questions total, with each subject-language
    pair capped at 500 questions. No external source reproduces the per-subject breakdown.
    The GitHub repository is publicly accessible at [WEB-17]
    and the full paper at [WEB-18] for direct
    inspection.]'
- gap_id: GAP-5
  title: Telugu-speaking zone agricultural coverage (Telangana/Andhra Pradesh)
  description: The deployment targets Telangana dry-land cropping and Andhra coastal
    aquaculture contexts. It is unconfirmed whether MILU's Telugu-language questions
    include regionally specific sub-national agro-ecological content.
  web_search_target: MILU Telugu benchmark Telangana Andhra Pradesh agricultural content
    dry-land cropping aquaculture evaluation subject statistics
  verification_question: Do MILU's Telugu-language questions include Telangana/Andhra-specific
    agricultural content, or do they default to generic Indian exam material?
  resolution: '[NEEDS VERIFICATION — deferred: below search budget; confirmed agro-ecological
    facts for Telangana and AP resolved separately (see cross_reference_zones above),
    but sub-national specificity within MILU Telugu questions remains unverified.
    Would require direct corpus inspection.]'
- gap_id: GAP-6
  title: Absence of Bangladeshi annotators or validators
  description: MILU's annotation pipeline is structurally Indian. No Bangladeshi subject-matter
    experts, agronomists, or environmental scientists contributed to benchmark construction.
  web_search_target: MILU benchmark annotation Bangladeshi validators cross-border
    ground truth agricultural science answer keys AI4Bharat
  verification_question: Does MILU's design documentation mention any cross-border
    or Bangladeshi input into benchmark construction or validation?
  resolution: 'CONFIRMED ABSENT. MILU paper (NAACL 2025) and GitHub confirm all annotation
    was by AI4Bharat volunteers and Indian exam portal subject experts. No Bangladeshi
    input documented. Source: AI4Bharat/MILU GitHub — [WEB-17];
    NAACL paper — [WEB-18]'
- gap_id: GAP-7
  title: Current status of key Bangladesh-India water treaties
  description: The Teesta water-sharing agreement and current Ganges treaty status
    are material to ground-truth validity for trans-border agricultural policy questions.
  web_search_target: Teesta water sharing agreement India Bangladesh 2024 status Ganges
    treaty Farakka agricultural downstream impact
  verification_question: What is the current (2024) status of the Teesta agreement
    and Ganges Water Sharing Treaty, and do any LLM benchmarks address these as contested
    knowledge domains?
  resolution: 'RESOLVED. Ganges treaty: In force until 12 December 2026 (30-year term
    signed 1996); renewal negotiations formally initiated but unresolved as of April
    2026; India seeking renegotiation on new terms. Teesta: No formal treaty has ever
    been concluded; 2011 draft (42.5% India / 37.5% Bangladesh) blocked by West Bengal;
    interim Bangladesh government actively pursuing resolution but no agreement as
    of 2025. No LLM benchmark specifically addresses these as contested knowledge
    domains. Sources: Treaty text — [WEB-19];
    The Diplomat Apr 2026 — [WEB-11];
    Teesta Wikipedia — [WEB-14]'
- gap_id: GAP-8
  title: Bangladesh Agricultural University and BARI representation in Indic NLP
  description: Key Bangladeshi agricultural research institutions (BAU Mymensingh,
    BARI, BRRI) may have produced Bengali-language scientific content relevant to
    benchmark augmentation.
  web_search_target: Bangladesh Agricultural University Mymensingh Bengali NLP dataset
    BARI BRRI agricultural knowledge LLM benchmark
  verification_question: Is there any Bengali-language agricultural science dataset
    or benchmark drawing from Bangladeshi institutional sources (BAU, BARI, BRRI)
    that could supplement or contrast with MILU?
  resolution: '[NOT FOUND — No Bengali-language agricultural NLP dataset or LLM benchmark
    drawing from BAU, BARI, or BRRI institutional sources was identified. BAU (founded
    1961, 45 departments, 6 faculties, ~5,000 undergrad and ~3,000 postgrad students
    as of 2024) and its co-located institutes BINA and BFRI are active research institutions,
    but no digitized Bengali-language agricultural QA corpus from these institutions
    surfaced in searches. This confirms a documentation gap rather than a thin research
    tradition. Sources: BAU official — [WEB-7]; Wikipedia — [WEB-8]]'
infrastructure_and_access_notes:
  internet_access_mymensingh: 'National-level: Bangladesh internet penetration was
    44.5% (77.36 million users) as of January 2024, increasing to ~47% by 2025. Mobile
    internet strongly dominates with 119.29 million subscribers (vs. 14.32 million
    fixed broadband). 4G coverage reached ~100% nationally by 2025. Urban penetration
    reached ~78% vs. ~49% rural (2025). Note: These are national aggregates; Mymensingh
    district data is not separately published, but as a divisional capital and major
    educational center (home to BAU), connectivity is likely above the national rural
    average. Sources: DataReportal Digital 2024 Bangladesh — [WEB-20];
    Wikipedia Internet in Bangladesh — [WEB-21]'
  device_usage: '[NEEDS VERIFICATION — deferred: below search budget; likely unsearchable
    at Mymensingh professional-cohort level; national data strongly suggests mobile-first
    access but device breakdown for research/NGO professional users is not published
    at sub-national level]'
  llm_access_modality: Text-based API or web interface access to both frontier models
    (GPT-4o, Gemini) and regional Indic LLMs; no image or speech modality involved
    in this deployment
  bangladeshi_llm_ecosystem: '[NOT FOUND — No Bangladeshi Bengali-specific LLM or
    agricultural domain-adapted model evaluated or publicly documented as of 2024
    was identified in searches. The BEnQA paper (2024) benchmarks multiple LLMs on
    Bangladeshi Bengali science content but does not describe a Bangladesh-developed
    LLM. This is a documentation gap consistent with Bangladesh''s nascent NLP infrastructure.
    Source: BEnQA arXiv — [WEB-6]]'
  indic_llm_bangla_support: 'Most evaluated Indic LLMs in MILU are adapted from English
    base models (LLAMA-2-7B) with Indic language pretraining. Performance near random
    baseline for many models in non-Hindi languages. Bengali-specific models evaluated
    include models from the AI4Bharat ecosystem (e.g., AIRAVATA). No model in the
    MILU evaluation set is documented as trained on Bangladeshi Bengali data specifically
    — all Bengali data in training corpora is presumed to be dominantly Indian Bengali
    or pan-Bengali web text. The BEnQA study confirms a significant Bengali–English
    performance gap on Bangladeshi-register content across multiple LLMs. Sources:
    AI4Bharat/MILU GitHub — [WEB-17]; BEnQA — [WEB-6]'
cultural_and_institutional_norms_notes: 'The deployment population operates within
  a Bangladeshi scientific and bureaucratic context that differs structurally from
  the Indian institutional context MILU was designed for:

  - Agricultural research and extension in Bangladesh is organized through distinct
  national institutions (BAU, BARI, BRRI, DAE) with Bangladesh-specific crop variety
  releases, policy frameworks, and agronomic recommendations.

  - Bengali agricultural vocabulary in Bangladesh reflects local dialect, land-tenure
  law (khas land, char land allotment), and floodplain ecology that diverges from
  West Bengal conventions.

  - Environmental policy context includes Bangladesh-specific climate adaptation frameworks
  (Bangladesh Delta Plan 2100, BCCTF) not represented in Indian exam content.

  - Professional norms blend South Asian academic formality with international scientific
  English; queries to LLMs likely mix registers.

  - Trans-boundary river issues carry political salience in Bangladesh that differs
  from how they are framed in Indian exam contexts; environmental scientists may hold
  positions informed by Bangladeshi national and scientific perspectives that Indian
  answer keys would not validate.

  - The Ganges treaty''s impending expiry (December 2026) and the Teesta deadlock
  represent live policy flashpoints where benchmark ground truth derived from Indian
  exams is actively diverging from Bangladeshi authoritative positions.'
known_data_sources_for_gap_filling:
  bangladeshi_agricultural_institutions:
  - 'Bangladesh Agricultural University (BAU), Mymensingh — public agricultural university,
    45 departments, 6 faculties; co-hosts BINA and BFRI on campus; active research
    output but no Bengali-language NLP/QA corpus identified. Source: [WEB-7]'
  - 'Bangladesh Agricultural Research Institute (BARI) — [NEEDS VERIFICATION — deferred:
    technical bulletin or exam-question availability not searched]'
  - 'Bangladesh Rice Research Institute (BRRI) — [NEEDS VERIFICATION — deferred: boro/aman
    variety and cultivation guidance in Bengali not searched]'
  - 'Bangladesh Water Development Board (BWDB) — [NEEDS VERIFICATION — deferred: haor
    and floodplain hydrology documentation not searched]'
  relevant_policy_documents:
  - 'Bangladesh Delta Plan 2100 — [NEEDS VERIFICATION — deferred: Bengali-language
    availability and LLM training data inclusion status not searched]'
  - 'Bangladesh Climate Change Strategy and Action Plan (BCCSAP) — [NEEDS VERIFICATION
    — deferred: not searched]'
  - 'Ganges Water Sharing Treaty (1996) — Currently in force; expires 12 December
    2026; renewal negotiations ongoing and unresolved as of April 2026. Full text:
    [WEB-19]'
  - 'Teesta Water Sharing Agreement — NO FORMAL AGREEMENT EXISTS as of May 2026. Draft
    2011 proposal (42.5% India / 37.5% Bangladesh) was never concluded. Interim Bangladesh
    government pursuing resolution; Teesta Master Plan deadline extended to December
    2026. Source: [WEB-14]'
  net_new_bangladeshi_nlp_resource:
    name: BEnQA
    full_name: 'BEnQA: A Question Answering and Reasoning Benchmark for Bengali and
      English'
    year: 2024
    arxiv_id: '2403.10900'
    url: '[WEB-6]'
    description: ~5,161 parallel Bangladeshi Bengali–English science QA questions
      from the national curriculum (grades 8–12), covering physics, chemistry, biology,
      and mathematics. Documents a significant Bengali–English LLM performance gap
      and limited CoT benefits for factual questions. Not an agricultural domain benchmark,
      but the closest existing Bangladeshi-register Bengali QA resource. Useful for
      calibrating language-competence vs. cultural-knowledge contributions to MILU
      Bengali performance gaps for this deployment population.
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://pjtsau.edu.in/crop.html |
| WEB-2 | https://telanganaslbc.com/StateProfile.aspx |
| WEB-3 | https://caa.gov.in/ |
| WEB-4 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2078575 |
| WEB-5 | https://mpeda.gov.in/?page_id=651 |
| WEB-6 | https://arxiv.org/abs/2403.10900 |
| WEB-7 | https://bau.edu.bd/ |
| WEB-8 | https://en.wikipedia.org/wiki/Bangladesh_Agricultural_University |
| WEB-9 | https://en.banglapedia.org/index.php/Bangladesh_Agricultural_University |
| WEB-10 | https://lotusarise.com/agro-ecological-regions-of-india-upsc/ |
| WEB-11 | https://thediplomat.com/2026/04/why-the-india-bangladesh-ganges-treaty-renewal-must-deliver-real-security/ |
| WEB-12 | https://www.thegeostrata.com/post/the-ganga-countdown-time-is-running-out-and-so-is-the-water |
| WEB-13 | https://www.gktoday.in/india-bangladesh-ganga-water-sharing-treaty-renewal-talks-begin/ |
| WEB-14 | https://en.wikipedia.org/wiki/Teesta_Water_Dispute |
| WEB-15 | https://www.waterdiplomat.org/story/2025/08/teesta-river-politics-and-benefit-sharing-getting-yes-without-grand-bargain |
| WEB-16 | https://www.tbsnews.net/features/panorama/teesta-master-plan-and-longstanding-bangladesh-india-water-politics-1072696 |
| WEB-17 | https://github.com/AI4Bharat/MILU |
| WEB-18 | https://aclanthology.org/2025.naacl-long.507/ |
| WEB-19 | https://mowr.nic.in/core/WebsiteUpload/2023/2023011877.pdf |
| WEB-20 | https://datareportal.com/reports/digital-2024-bangladesh |
| WEB-21 | https://en.wikipedia.org/wiki/Internet_in_Bangladesh |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Does MILU's culturally specific subject coverage (local history, arts, festivals, law) adequately represent the agro-ecological, soil, crop, and climate-specific knowledge an environmental scientist targeting South Asian agricultural regions would need?
A1: No. MILU contains only surface-level agricultural content about different parts of India; the depth of subject-specific knowledge required for serious agricultural or environmental science work is largely absent from the benchmark's subject taxonomy.

Q2 [IC]: Do MILU's Bengali-language questions reflect standard Indian Bengali (West Bengal exam corpus) rather than Bangladeshi or Mymensingh dialect conventions, and would dialect-specific agricultural terminology (local crop names, land-tenure terms, irrigation vocabulary) be represented?
A2: The wording is mostly standard across Bengali variants, with potentially slight implicit Indian Bengali stylistic bias. Dialect-specific agricultural terminology from the Bangladeshi/Mymensingh context is absent but would meaningfully improve benchmark robustness.

Q3 [OC]: Would Indian exam-derived answer keys be considered authoritative for environmental/agricultural science questions relevant to Bangladesh (e.g., haor ecology, boro rice cycles, trans-border river management), and are there cases where the correct answer for a Bangladeshi context would differ from what an Indian exam marks correct?
A3: Indian exam answers would generally be considered authoritative by Bangladeshi environmental scientists, with a few notable exceptions around trans-border water agreements and policy — where shared rivers and bilateral treaties can generate legitimately different national perspectives. The more significant gap is the absence of Bangladesh-specific agricultural practice differences and regional knowledge, rather than outright answer-key conflict.

Q4 [IF]: Will the LLMs receive queries in regional Indian languages, Bengali, English, or a mix — and is the Mymensingh scientist expected to query in standard Bengali script, colloquial Bangladeshi Bengali, or English?
A4: Queries will span Indian languages and Bengali as used in both India and Bangladesh. The input modality mix is text-based across these languages, but the benchmark's exam-style standardized prompts may not reflect the natural phrasing style of a domain expert in Bangladesh querying in Bangladeshi Bengali.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark's subject taxonomy covers surface-level Indian agricultural content and culturally-oriented categories (arts, law, festivals) but is confirmed to lack the depth of agro-ecological, soil-science, and crop-specific knowledge the deployment requires, and entirely omits Bangladesh-specific agricultural subdomains. |
| IC | HIGH | Individual datapoints draw from Indian regional competitive exams with no representation of Bangladeshi farming contexts, Mymensingh dialect terminology, haor wetland ecology, or trans-border river-system knowledge — all of which are central to the deployment's content needs. |
| IF | MODERATE | The deployment is text-only and Indic-script text is supported by MILU, but the exam-register query format is misaligned with how a domain expert in Bangladesh would naturally phrase agricultural science questions, and Bangladeshi Bengali as a script/dialect variant is underrepresented. |
| OO | MODERATE | MILU's output taxonomy is MCQ label-selection derived from Indian exam answer keys; the deployment requires knowledge retrieval and reasoning over legitimately pluralistic agro-ecological contexts where a single correct label may not capture cross-border agricultural practice differences. |
| OC | HIGH | Ground-truth labels originate from Indian exam corpora and reflect Indian educational and policy contexts; for Bangladesh-specific agricultural practice, river management, and bilateral water-agreement questions, Indian exam answer keys are not fully authoritative and may marginalize Bangladeshi scientific and practitioner perspectives. |
| OF | LOWER | Both the benchmark and the deployment operate in text-based, label/response format; the output modality mismatch is minimal, though MCQ framing may suppress nuanced agricultural knowledge that an open-ended deployment context would benefit from capturing. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (configs: Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu)
**Analysis date:** 2025-01-31
**Examples reviewed:** 215 total (Bengali: 21, English: 20, Gujarati: 24, Hindi: 26, Kannada: 17, Malayalam: 16, Marathi: 21, Odia: 21, Punjabi: 25, Tamil: 19, Telugu: 25) — all from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Bengali | Ex.7 | option4 | "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... জাতীয় খাদ্য সুরক্ষা মিশন মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" | National Food Security Mission: crop development scheme, soil health restoration — Indian scheme, no Bangladesh context | IO, IC |
| D2 | Bengali | Ex.1 | option3 | "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল?" | India's 1991 foreign reserve crisis — Indian economic history, irrelevant to Bangladesh agricultural deployment | IC |
| D3 | Bengali | Ex.1 | option3 | **is_translated:** True | All 21 Bengali validation examples are machine-translated from English | IF |
| D4 | Bengali | Ex.5 | option4 | "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP)... পাঞ্জাব" | Indian state assembly election — Indian polity, no Bangladesh relevance | IC |
| D5 | Bengali | Ex.9 | option3 | "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে... প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" | Removal of Indian Election Commissioner — Indian constitutional law only | OC |
| D6 | English | Ex.5 | option1 | "A geographic region has the following distinct characteristics: 1. Warm and dry climate 2. Mild and wet winter 3. Evergreen oak trees" | Mediterranean climate region identification — generic geography | IO |
| D7 | English | Ex.10 | option4 | "Which of the following are claimed as advantageous in respect of aerobic sludge digestion as compared to anaerobic sludge digestion?" | Wastewater engineering/environmental science — technically relevant but not agro-ecological | IO |
| D8 | English | Ex.9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" | Maharashtra state governance — India-specific law, not relevant to Bangladesh | IC, OC |
| D9 | English | Ex.13 | option4 | "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? ... Telangana" | Telangana state welfare policy — classified under Geography, reflects generic Indian current affairs | IC, OO |
| D10 | Bengali | Ex.7 | option4 | domain: Environmental Sciences, subject: Agriculture | Agriculture-labeled question about India's National Food Security Mission — only MILU "Agriculture" example in Bengali sample | IO, IC |
| D11 | Kannada | Ex.7 | option4 | "ರಾಷ್ಟ್ರೀಯ ಆಹಾರ ಭದ್ರತಾ ಮಿಷನ್ ಒಂದು ಬೆಳೆ ಅಭಿವೃದ್ಧಿ ಯೋಜನೆ... ಮಣ್ಣಿನ ಆರೋಗ್ಯವನ್ನು ಪುನಃಸ್ಥಾಪಿಸಲು" | National Food Security Mission crop scheme in Kannada — same Indian policy content replicated across languages | IC, IO |
| D12 | Marathi | Ex.7 | option4 | "राष्ट्रीय अन्न सुरक्षा मिशन हे एक पीक विकास योजना आहे... मातीचे आरोग्य पुनर्संचयित करणे" | National Food Security Mission in Marathi — same question across languages confirms India-only policy content | IC |
| D13 | Marathi | Ex.21 | option3 | "राष्ट्रीय मोहरी संशोधन केंद्र कुठे स्थित आहे... सेवर" | Location of National Mustard Research Centre in India — India-specific agricultural institution | IC, IO |
| D14 | Odia | Ex.21 | option4 | "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" | Which Indian company produces agricultural equipment rapidly (Kirloskar) — India-specific corporate knowledge | IC, IO |
| D15 | Punjabi | Ex.7 | option4 | "ਰਾਸ਼ਟਰੀ ਖਾਦ ਸੁਰੱਖਿਆ ਮਿਸ਼ਨ ਇੱਕ ਫਸਲ ਵਿਕਾਸ ਯੋਜਨਾ ਹੈ... ਮਿੱਟੀ ਦੀ ਸਿਹਤ ਨੂੰ ਬਹਾਲ ਕਰਨਾ" | National Food Security Mission in Punjabi — same cross-language India-scoped agriculture question | IC |
| D16 | Telugu | Ex.25 | option1 | "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది?... మొరెనా" | Location of Banmore Industrial Development Centre in Madhya Pradesh — Indian geography | IC |
| D17 | Telugu | Ex.9 | option2 | "క్రింది వాటిలో మహారాష్ట్ర శాసనసభ కమిటీ వ్యవస్థ గురించి ఏ ప్రకటన సరైనది కాదు?" | Maharashtra Legislative Committee system in Telugu — state-specific Indian governance | IC, OC |
| D18 | English | Ex.5 | option1 | domain: Environmental Sciences, subject: Geography | Mediterranean climate question under Environmental Sciences — geographic reasoning, not agro-ecological depth | IO |
| D19 | Bengali | Ex.3 | option4 | "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল?... গুলবার্গা" | First capital of Bahmani Kingdom — medieval Indian history, no agriculture/environment relevance | IC |
| D20 | Bengali | Ex.12 | option4 | "'মঙ্গল ভারত' কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল" | "Mangal Bharat" literary work by Vinoba Bhave — Indian literary/national leader trivia | IC |
| D21 | Odia | Ex.2 | option4 | "ଡିସେମ୍ବର 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆକୁ ପ୍ରଥମେ ଜଣା ଦେଇଥିବା ଦେଶ କେଉଁଟି?... ଆଫଗାନିସ୍ତାନ; option2: ବାଙ୍ଗ୍ଲାଦେଶ" | Which country first reported Indian Pharmacopoeia (Afghanistan) — Bangladesh appears as wrong answer option | IC, OC |
| D22 | Hindi | Ex.10 | option4 | "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है?... नाइट्रेट" | Blue Baby Syndrome caused by excess nitrate in blood — generic health/environmental science | IO |
| D23 | English | Ex.10 | option4 | "Lower BOD concentration in supernatant liquor... Production of a sludge with excellent dewatering propensity... aerobic sludge digestion" | Aerobic vs. anaerobic sludge digestion advantages — environmental engineering question | IO |
| D24 | Bengali | Ex.8 | option4 | "নিম্নলিখিত কোনগুলি অক্সিডেশন-রিডাকশন বিক্রিয়া?" | Oxidation-reduction reactions — basic chemistry | IO |
| D25 | Telugu | Ex.2 | option4 | "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది?... ఆఫ్ఘనిస్తాన్; option2: బంగ్లాదేశ్" | Same Indian Pharmacopoeia question in Telugu — Bangladesh again used only as distractor | IC, OC |
| D26 | Bengali | Ex.2 | option3 | "একটি ক্রিকেট প্রশিক্ষণ শিবিরে ১২০০ জন শিশু... নির্বাচিত না হওয়া শিশুদের সংখ্যা এবং মোট শিশুদের সংখ্যার অনুপাত" | Ratio problem about cricket training camp — numeracy/reasoning, irrelevant to agricultural science | IO |
| D27 | Gujarati | Ex.8 | option3 | "રેડક્લિફ રેખા નીચેના પૈકી કયા દેશ સાથે ભારતની સરહદોને અલગ કરે છે?... પાકિસ્તાન" | Radcliffe Line divides India from Pakistan — Indian partition geography | IC |
| D28 | Hindi | Ex.6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?... 44वें संविधान संशोधन अधिनियम द्वारा" | Indian constitutional amendment for 'armed rebellion' clause — Indian law and governance | IC, OC |
| D29 | Marathi | Ex.16 | option3 | "हलषष्ठी सण का साजरा केला जातो?... मुलाच्या दीर्घायुष्यासाठी" | Halashashthi festival purpose (for son's longevity) — Indian/Hindu cultural practice, Agriculture-labeled but not agricultural | IO |
| D30 | Punjabi | Ex.21 | option3 | "ਰਾਸ਼ਟਰੀ ਸਰੋਂ ਖੋਜ ਕੇਂਦਰ ਕਿੱਥੇ ਸਥਿਤ ਹੈ... ਸੇਵਰ" | Location of National Mustard Research Centre — Indian agricultural institution trivia | IC, IO |
| D31 | Bengali | Ex.4 | option2 | "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। ... শেল" (is_translated: True) | Shell-type constant current transformer — engineering question, machine-translated from English | IF |
| D32 | English | Ex.20 | option2 | "Flower colours of red, pink, blue and purple come mainly from pigments called... Anthocyanins" | Plant pigment biology question — generic botany | IO |
| D33 | Odia | Ex.17 | option1 | "T - Hub ଏକ ତେଲେଙ୍ଗାନା ରାଜ୍ୟ ସରକାରର ପ୍ରୟାସ... ଉଦ୍ୟମିତାକୁ ପ୍ରୋତ୍ସାହନ ଦେବାକୁ ଏକ ପ୍ରଯୁକ୍ତି ଉତ୍ପ୍ରେରଣ କେନ୍ଦ୍ର" | T-Hub Telangana state entrepreneurship tech incubator — Telangana-specific but non-agricultural | IC |
| D34 | Bengali | Ex.6 | option2 | "নিচের প্রশ্নে... সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে" (question body missing the target word) | Antonym question — incomplete stem, illustrates quality issues in translated questions | IF |
| D35 | Bengali | Ex.19 | option1 | "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে" (arguments not shown in question field) | Argument evaluation question — missing argument content, shows data quality gap in translated items | IF |
| D36 | English | Ex.11 | option2 | "The owner of the textile shop brought a... Calculator" | Incomplete question stem — no meaningful question context present | IF |
| D37 | Hindi | Ex.13 | option1 | "'মানসून' শব্দের উৎপত্তি কোন ভাষা থেকে?... আরবি ভাষা" (Hindi): "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है?... अरबी भाषा" | Origin of word 'monsoon' from Arabic — climate vocabulary trivia, tangentially relevant to agricultural climate | IO |
| D38 | Marathi | Ex.13 | option2 | "प्रांतांमध्ये द्वैधशासन प्रणाली कोणत्या कायद्याने स्थापन केली?... भारत सरकार अधिनियम 1919" | Government of India Act 1919 establishing dyarchy — Indian colonial law | IC, OC |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-script Indic language coverage including Bengali
- **Dimension(s):** IF
- **Observation:** The benchmark successfully delivers text-based MCQ content in Bengali script across all 21 sampled Bengali validation examples, as well as Telugu (25 examples), Hindi, and 8 other Indic scripts. The deployment's primary modality — text-based Indic script queries — is technically supported.
- **Deployment relevance:** The environmental scientist's queries in Bengali and Telugu scripts are at least modality-compatible with the benchmark format. Script-level compatibility ensures that model performance scores on MILU reflect at minimum the correct input encoding for the target scripts.
- **Datapoint citations:**
  - [D3] Bengali Ex.1 (Bengali, validation, option3): `is_translated: True` — Confirms Bengali script is fully populated across all sampled examples, though all are machine-translated.
  - [D31] Bengali Ex.4 (Bengali, validation, option2): "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। ... শেল" — Technical content in Bengali script, confirming script rendering is functional even for translated engineering content.

#### Strength 2: Environmental Sciences and Agriculture subject labels present in multiple languages
- **Dimension(s):** IO
- **Observation:** The "Agriculture" subject appears in the Environmental Sciences domain across at least Bengali (Ex.7), Kannada (Ex.7), Marathi (Ex.7, Ex.21), Punjabi (Ex.7, Ex.21), and Odia (Ex.21). A single Agriculture-labeled question also appears in Bengali. The Environmental Sciences domain contributes Geography, Earth Sciences, and Environmental Science sub-subjects as well.
- **Deployment relevance:** The presence of Agriculture-labeled questions across languages demonstrates that the subject taxonomy does include agricultural content, even if surface-level. For an initial screening of whether a model has any agricultural knowledge, these items provide at least minimal signal.
- **Datapoint citations:**
  - [D10] Bengali Ex.7 (Bengali, validation, option4, subject=Agriculture): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" — Only Bengali Agriculture question in sample; concerns soil health but in the context of an Indian national scheme.
  - [D13] Marathi Ex.21 (Marathi, validation, option3, subject=Agriculture): "राष्ट्रीय मोहरी संशोधन केंद्र कुठे स्थित आहे... सेवर" — Agriculture question about location of National Mustard Research Centre.
  - [D14] Odia Ex.21 (Odia, validation, option4, subject=Agriculture): "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" — Agricultural equipment manufacturer in India.

#### Strength 3: Broad domain coverage enabling baseline comparisons across general knowledge areas
- **Dimension(s):** IO, OF
- **Observation:** Across 215 sampled examples, MILU covers Engineering, Science (Physics, Chemistry, Biology, Computer Science, Logical Reasoning), Social Sciences, Arts & Humanities, Law & Governance, Health & Medicine, Business Studies, and Environmental Sciences. This allows a broad model capability baseline.
- **Deployment relevance:** For the scientist's use of both frontier LLMs (GPT-4o, Gemini) and regional small LLMs, MILU's breadth enables diagnosis of whether regional LLMs fail specifically in science/environment or broadly across all domains — a useful comparative signal even if the agricultural domain content is inadequate.
- **Datapoint citations:**
  - [D7] English Ex.10 (English, validation, option4, subject=Environmental Science): "Which of the following are claimed as advantageous in respect of aerobic sludge digestion as compared to anaerobic sludge digestion? (1) Lower BOD concentration in supernatant liquor..." — Technical environmental engineering question, at least adjacent to environmental science professional knowledge.
  - [D22] Hindi Ex.10 (Hindi, validation, option4, subject=Health and Medicine): "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है?... नाइट्रेट" — Nitrate-related health question, tangentially relevant to agro-environmental context (nitrate contamination in agricultural water).

#### Strength 4: Consistent MCQ structure enables cross-language and cross-model comparison
- **Dimension(s):** OF
- **Observation:** All sampled examples follow identical 4-option MCQ structure with `target` field, `is_translated` flag, and domain/subject labels. This structural consistency enables controlled comparison across 11 languages and across model families.
- **Deployment relevance:** If the goal includes benchmarking multiple LLMs (frontier + regional) across Bengali and Telugu, MILU's consistent format allows reproducible, comparable evaluation — a practical strength for the meta-analytic purpose of assessing whether regional Indic LLMs perform adequately on science content before deployment in the agricultural query context.
- **Datapoint citations:**
  - [D6] English Ex.5 (English, validation, option1, subject=Geography): "A geographic region has the following distinct characteristics: 1. Warm and dry climate 2. Mild and wet winter 3. Evergreen oak trees" — Illustrates clean MCQ structure with unambiguous single-correct answer.
  - [D11] Kannada Ex.7 (Kannada, validation, option4, subject=Agriculture): "ರಾಷ್ಟ್ರೀಯ ಆಹಾರ ಭದ್ರತಾ ಮಿಷನ್ ಒಂದು ಬೆಳೆ ಅಭಿವೃದ್ಧಿ ಯೋಜನೆ" — Same question appears in Bengali, Kannada, Marathi, Malayalam, Punjabi, confirming reliable cross-language structural alignment for identical underlying content.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete absence of Bangladesh-specific agricultural content
- **Dimension(s):** IO, IC
- **Observation:** Across all 215 sampled examples, zero questions address Bangladeshi agro-ecological systems. The Agriculture-labeled items that do appear concern Indian national schemes: the National Food Security Mission (NFSM) and the National Mustard Research Centre, and an Indian agricultural equipment company (Kirloskar). No question in the sample touches haor wetlands, beel fisheries, boro or aman rice cultivation, char-land farming, Brahmaputra-Jamuna floodplain management, or any Bangladeshi agricultural institution. This is consistent with the confirmed structural absence documented in the YAML and web search, and is directly observable in the data.
- **Deployment relevance:** The environmental scientist's primary knowledge domain — Bangladeshi delta agro-ecology — is entirely unrepresented. A model that scores well on MILU Agriculture questions has demonstrated knowledge of Indian food policy schemes, not Bangladeshi farming systems. The benchmark provides no discriminative power for the agricultural science retrieval use case as described.
- **Datapoint citations:**
  - [D10] Bengali Ex.7 (Bengali, validation, option4, domain=Environmental Sciences, subject=Agriculture): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" — The only Bengali Agriculture example in the validation sample concerns India's NFSM, not Bangladesh farming.
  - [D13] Marathi Ex.21 (Marathi, validation, option3, subject=Agriculture): "राष्ट्रीय मोहरी संशोधन केंद्र कुठे स्थित आहे... सेवर" — Agriculture question asking for location of Indian Mustard Research Centre in Rajasthan; no agronomic depth, no cross-border relevance.
  - [D14] Odia Ex.21 (Odia, validation, option4, subject=Agriculture): "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" — Agricultural equipment company trivia (Kirloskar); no agro-ecological science content.
  - [D15] Punjabi Ex.7 (Punjabi, validation, option4, subject=Agriculture): "ਰਾਸ਼ਟਰੀ ਖਾਦ ਸੁਰੱਖਿਆ ਮਿਸ਼ਨ ਇੱਕ ਫਸਲ ਵਿਕਾਸ ਯੋਜਨਾ ਹੈ... ਮਿੱਟੀ ਦੀ ਸਿਹਤ ਨੂੰ ਬਹਾਲ ਕਰਨਾ" — Same NFSM policy question replicated in Punjabi; Indian scheme only.

#### CRITICAL Concern 2: Bengali validation sample is 100% machine-translated; no original Bengali-authored questions visible
- **Dimension(s):** IF, IC
- **Observation:** Every one of the 21 Bengali validation examples has `is_translated: True`. This means the Bengali validation set in this sample consists entirely of questions translated from English (presumably Indian English exam content) via GPT-4O. This is consistent with the 25% overall translation rate documented in the paper, but the validation split sampled here shows complete translation saturation. The translated questions adopt standard Bengali script but carry formal translated register, not the naturalistic Bangladeshi Bengali or West Bengal exam register.
- **Deployment relevance:** Bangladeshi Bengali-register competence is a core requirement for the deployment. A benchmark where Bengali performance is assessed entirely on machine-translated questions conflates translation quality with language knowledge. For Mymensingh-dialect users, the register mismatch is compounded: the translation pipeline renders Indian English into what is likely to be a generic, somewhat stilted written Bengali, not the natural phrasing of a Bangladeshi agricultural scientist.
- **Datapoint citations:**
  - [D3] Bengali Ex.1 (Bengali, validation): `is_translated: True` — Confirmed for all 21 sampled Bengali validation examples; no `is_translated: False` observation in this split.
  - [D31] Bengali Ex.4 (Bengali, validation, option2): "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। ... শেল" — Engineering transformer question translated into Bengali; the phrasing is formally correct but exam-register, not naturalistic professional Bengali.
  - [D34] Bengali Ex.6 (Bengali, validation): "নিচের প্রশ্নে... সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে" — Antonym question with the target word missing from the question field entirely; the translated question is incomplete, suggesting translation pipeline quality issues.
  - [D35] Bengali Ex.19 (Bengali, validation): "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে" — Argument evaluation question where Arguments I and II are absent from the question field; answer cannot be verified from the question stem alone.

#### CRITICAL Concern 3: Environmental Sciences domain is surface-level general knowledge, not agro-ecological science
- **Dimension(s):** IO, IC
- **Observation:** The Environmental Sciences examples sampled across languages consistently classify geography questions (Mediterranean climate, Radcliffe Line, state populations) and generic earth science questions under this domain, not agro-ecological or soil science content. Agriculture-labeled questions (when they appear) concern Indian policy schemes or corporate trivia, not technical crop science. Across 215 examples, no question addresses: soil types and crop suitability, water management, wetland ecology, irrigation science, delta morphology, or climate change impacts on agriculture.
- **Deployment relevance:** The user explicitly confirmed that MILU's agricultural content is "surface-level." The data confirms this: the Environmental Sciences and Agriculture subject labels in MILU do not map to the technical depth required by a professional environmental scientist. MILU cannot assess whether a model can answer questions about floodplain hydrology, alluvial soil classification, or wetland rice agronomy — the core knowledge domains in the deployment context.
- **Datapoint citations:**
  - [D18] English Ex.5 (English, validation, option1, domain=Environmental Sciences, subject=Geography): "A geographic region has the following distinct characteristics: 1. Warm and dry climate 2. Mild and wet winter 3. Evergreen oak trees" — Mediterranean climate identification; classified as Environmental Sciences but has no agro-ecological depth.
  - [D6] English Ex.5 (same as D18) — Further confirms that "Environmental Sciences" domain encodes geography trivia, not environmental science.
  - [D29] Marathi Ex.16 (Marathi, validation, option3, domain=Arts & Humanities, subject=Arts and Culture): "हलषष्ठी सण का साजरा केला जातो?... मुलाच्या दीर्घायुष्यासाठी" — A festival question classified under Arts & Culture that in a different taxonomy could be agriculture-adjacent (harvest festivals), but demonstrates how culturally specific Indian content dominates even "Environmental Sciences"-adjacent categories.
  - [D9] English Ex.13 (English, validation, option4, domain=Environmental Sciences, subject=Geography): "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? ... Telangana" — Welfare policy question classified under Environmental Sciences/Geography; illustrates how the domain-subject taxonomy is applied loosely, and that "Telangana" appears in the sample only in a non-agricultural governance context.

---

#### MAJOR

#### MAJOR Concern 4: Indian-centric ground-truth labels for all governance, law, and policy questions; Bangladesh structurally excluded from answer keys
- **Dimension(s):** OC, OO
- **Observation:** Every governance and law question sampled encodes exclusively Indian constitutional, electoral, and policy knowledge as the ground truth. These include Indian Election Commissioner removal procedure (Bengali Ex.9), the 44th Constitutional Amendment (Hindi Ex.6, Malayalam Ex.6, Tamil Ex.6), Maharashtra state legislature committee rules (English Ex.9, Telugu Ex.9), and Indian state election results (Bengali Ex.5, Punjabi Ex.5). Bangladesh appears in two sampled examples solely as a wrong-answer distractor option (Odia Ex.2, Telugu Ex.2), never as the basis for a correct answer.
- **Deployment relevance:** While the user confirmed that Indian exam answer keys are "generally considered authoritative" for environmental science facts, the governance domain is categorically different. For trans-border agricultural policy questions (river-water allocation, bilateral treaty terms), Indian exam answers encode nationally partial perspectives. The current bilateral volatility (Ganges treaty nearing expiry December 2026, Teesta unresolved) makes this more acute. No such questions exist in the sampled data — confirming the structural absence documented in the YAML.
- **Datapoint citations:**
  - [D5] Bengali Ex.9 (Bengali, validation, option3, domain=Law & Governance, subject=Politics and Governance): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে... প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — Answer concerns Indian constitutional procedure; Bangladeshi constitutional norms are categorically different.
  - [D8] English Ex.9 (English, validation, option2, domain=Law & Governance): "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" — Maharashtra-specific state law; no cross-border relevance.
  - [D21] Odia Ex.2 (Odia, validation, option4, domain=Health & Medicine): "ଡିସେମ୍ବର 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆକୁ ପ୍ରଥମେ ଜଣା ଦେଇଥିବା ଦେଶ କେଉଁଟି?... ଆଫଗାନିସ୍ତାନ; option2: ବାଙ୍ଗ୍ଲାଦେଶ" — Bangladesh listed as a wrong answer; correct answer is Afghanistan. Illustrates Bangladesh's role in this benchmark: a distractor, not a knowledge frame.
  - [D25] Telugu Ex.2 (Telugu, validation, option4): "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది?... option2: బంగ్లాదేశ్" — Bangladesh again used as wrong-answer distractor across languages.

#### MAJOR Concern 5: Agriculture-labeled questions are policy trivia and institutional facts, not agronomic science
- **Dimension(s):** IO, OO
- **Observation:** Every Agriculture-subject question identified in the sample falls into one of three categories: (a) Indian government scheme facts (NFSM launch date, objectives), (b) Indian institutional locations (National Mustard Research Centre at Sever, Rajasthan), or (c) Indian corporate knowledge (Kirloskar as agricultural equipment manufacturer). None address agronomic principles, soil science, crop physiology, pest management, irrigation design, or ecosystem dynamics.
- **Deployment relevance:** An environmental scientist using LLMs to retrieve and reason over agricultural and environmental science knowledge requires models that can demonstrate technical depth — understanding soil types and water retention, rice growth stages and water requirements, integrated crop-fish system management. MILU Agriculture questions test Indian bureaucratic and corporate general-knowledge facts, not agronomic science. A model scoring well on these items provides no assurance about agricultural science competence.
- **Datapoint citations:**
  - [D1] Bengali Ex.7 (Bengali, validation, option4, subject=Agriculture): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" — Factual recall about Indian scheme objectives; no agronomy.
  - [D30] Punjabi Ex.21 (Punjabi, validation, option3, subject=Agriculture): "ਰਾਸ਼ਟਰੀ ਸਰੋਂ ਖੋਜ ਕੇਂਦਰ ਕਿੱਥੇ ਸਥਿਤ ਹੈ... ਸੇਵਰ" — Asks the location of India's mustard research centre; pure institutional geography.
  - [D14] Odia Ex.21 (Odia, validation, option4, subject=Agriculture): "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" — Corporate brand identification; not agricultural science.

#### MAJOR Concern 6: Telugu sample shows no Telangana/Andhra agro-ecological content; only general Indian exam material
- **Dimension(s):** IO, IC
- **Observation:** The 25 Telugu examples contain no questions about Telangana dry-land cropping, Andhra coastal aquaculture, or sub-regional agro-ecological specifics. Telangana appears once in the sampled data (English Ex.13 and Gujarati Ex.13) only in a social welfare policy context (pension for single women). The Telugu sample covers engineering, health, history, computer science, geography (generic), economics, and materials science — no regionally specific agricultural content is present.
- **Deployment relevance:** The deployment context explicitly targets Telangana dry-land cropping (cotton, sorghum, pigeonpea, red Deccan soils) and Andhra coastal aquaculture (L. vannamei shrimp farming, MPEDA/CAA regulatory framework) as cross-reference agro-ecological zones. MILU Telugu does not assess model knowledge of these sub-regional systems.
- **Datapoint citations:**
  - [D33] Odia Ex.17 (Odia, validation, option1, subject=Business and Management): "T - Hub ଏକ ତେଲେଙ୍ଗାନା ରାଜ୍ୟ ସରକାରର ପ୍ରୟାସ... ଉଦ୍ୟମିତାକୁ ପ୍ରୋତ୍ସାହନ ଦେବାକୁ ଏକ ପ୍ରଯୁକ୍ତି ଉତ୍ପ୍ରେରଣ କେନ୍ଦ୍ର" — T-Hub Telangana tech incubator; Telangana context appears only in tech entrepreneurship, not agriculture.
  - [D9] English Ex.13 (English, validation, option4, domain=Environmental Sciences): "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? ... Telangana" — Telangana surfaces as a welfare policy answer; no agricultural content.
  - [D16] Telugu Ex.25 (Telugu, validation, option1, domain=Environmental Sciences, subject=Geography): "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది?... మొరెనా" — Madhya Pradesh industrial centre location; Environmental Sciences domain again populated with geography trivia, not ecological content.

#### MAJOR Concern 7: MCQ format with single correct answer cannot accommodate cross-border knowledge pluralism on contested environmental/policy topics
- **Dimension(s):** OO, OF
- **Observation:** MILU enforces a single-correct-answer MCQ format with a definitive `target` field. The deployment includes scenarios — trans-border river management, water-sharing agreement terms, upstream dam impacts on Bangladeshi agriculture — where the "correct" answer is nationally contested and legitimately differs between Indian and Bangladeshi perspectives. No such questions exist in the current corpus, but the format structurally precludes them.
- **Deployment relevance:** Even if MILU were augmented with trans-border content, the MCQ format would force selection of a single answer key (likely Indian-exam-derived) for questions where Bangladeshi scientists hold different scientifically and politically valid positions. This is a structural output ontology constraint, not merely a coverage gap.
- **Datapoint citations:**
  - [D5] Bengali Ex.9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে... প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — Illustrates how Indian constitutional answers are encoded as the single correct response; a parallel Bengali question about Bangladesh's election commission removal would have a categorically different correct answer.
  - [D28] Hindi Ex.6 (Hindi, validation, option1, domain=Law & Governance): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?... 44वें संविधान संशोधन अधिनियम द्वारा" — Indian constitutional amendment as definitive answer; demonstrates how the MCQ single-correct format encodes nationally specific legal facts.

---

#### MINOR

#### MINOR Concern 8: Incomplete question stems visible in translated examples, indicating pipeline quality issues
- **Dimension(s):** IF
- **Observation:** At least two Bengali validation examples have incomplete or truncated question stems: Ex.6 asks for an antonym but the target word is absent; Ex.19 references "Arguments I and II" that are not present in the question field. English Ex.11 ("The owner of the textile shop brought a...") also presents an incomplete sentence with no meaningful context for answering. These truncation artifacts are present in the publicly released dataset.
- **Deployment relevance:** While these are minor quality issues that do not affect the dominant validity concerns, they indicate that the machine-translation and cleaning pipeline introduced some data quality degradation, particularly in Bengali. This slightly undermines confidence in translated Bengali content quality overall.
- **Datapoint citations:**
  - [D34] Bengali Ex.6 (Bengali, validation): "নিচের প্রশ্নে... সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে" — The antonym target word is absent from the question text.
  - [D35] Bengali Ex.19 (Bengali, validation): "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে" — Arguments I and II are referenced but not present in the question field.
  - [D36] English Ex.11 (English, validation, option2): "The owner of the textile shop brought a... Calculator" — Incomplete sentence with no meaningful question context.

#### MINOR Concern 9: Cross-language duplication of identical questions provides inflated coverage illusion
- **Dimension(s):** IO
- **Observation:** The same underlying questions appear across all 11 languages. The National Food Security Mission question (Ex.7 in Bengali, Kannada, Malayalam, Marathi, Punjabi), the cross-assembler definition (Ex.14 across Bengali, English, Kannada, Punjabi, Tamil, Telugu), the Bahmani Kingdom capital (Ex.3 across Bengali, English, Gujarati, Hindi, Malayalam, Punjabi, Tamil), and the Mediterranean climate question appear verbatim across most language configs. These represent translated duplicates of single source items, not independent language-specific questions.
- **Deployment relevance:** The apparent 79,000-question scale of MILU overstates content diversity; the underlying distinct-question count is substantially smaller, and for agricultural content specifically, the number of distinct agronomic questions is very low. A naive count of "Agriculture subject questions" across 11 languages would inflate the perceived agricultural coverage by a factor of up to 11×.
- **Datapoint citations:**
  - [D11] Kannada Ex.7 / [D12] Marathi Ex.7 / [D1] Bengali Ex.7 / [D15] Punjabi Ex.7 — All ask identical NFSM questions in different Indic scripts; same question content replicated across languages.
  - [D19] Bengali Ex.3 / [D27] (implicit in Gujarati, Hindi, Malayalam, Punjabi, Tamil samples) — Bahmani Kingdom capital question identical across multiple language configs.

---

### Content Coverage Summary

The 215 sampled examples span 11 Indic language configs and show a consistent pattern across all of them. Domain distribution in the sample favors Engineering & Technology (frequent), Arts & Humanities (history, language studies, arts/culture), and Business Studies (economics, finance), with Science (physics, chemistry, computer science, logical reasoning) and Social Sciences (sports, sociology) also well-represented. Environmental Sciences appears but is populated almost entirely with geography trivia (climate regions, political boundaries, state-level facts) rather than environmental or agro-ecological science.

The topical content is dominated by Indian competitive exam material: Indian constitutional law, Indian civil service facts, Indian national schemes and institutions, Indian history (medieval and colonial), Indian electoral politics, and Indian corporate/industrial knowledge. All Bengali examples in the validation split are machine-translated from English. South Asian content that appears to be cross-regional (e.g., geographic climate questions, basic physics/engineering) is generic and could have originated from any English-language exam.

Bangladesh appears in the sampled data exclusively as a wrong-answer distractor in two questions (Odia Ex.2, Telugu Ex.2) about Indian Pharmacopoeia recognition. No Bangladeshi agricultural institution, ecological system, land tenure concept, or trans-border water policy appears anywhere in the sample. Telangana and Andhra Pradesh appear only in non-agricultural contexts (tech incubator, welfare pension). The agricultural science vocabulary of the deployment context — haor, beel, boro, aman, char, Farakka, Teesta — has zero representation in the sampled content.

---

### Limitations

1. **Sample is from validation split only.** All 215 examples are drawn from the validation split (~9,000 total questions used for few-shot examples). The test split (~79,000 questions) may have different subject and domain distributions, including potentially more original (non-translated) Bengali questions and more Agriculture/Environmental Sciences content. The 100% translation rate observed in Bengali validation may not hold for the test split.

2. **Sample size per language is small (16–26 examples).** With 16–26 examples per language config, rare subjects (e.g., specific agro-ecological content, if any exists in the test split) would likely not appear in this sample even if present. The absence of Bangladesh-specific content and technical agricultural science in this sample is consistent with structural gaps documented in the YAML, but the sample cannot confirm the exact count of such questions in the full dataset.

3. **Subject distribution within Environmental Sciences is not fully observable.** Table 9 of the MILU paper contains per-subject per-language question counts but was not accessible in this analysis. The sampled data confirms surface-level coverage in Environmental Sciences, but the exact proportion of Agriculture, Environmental Science, Geography, and Earth Sciences sub-subjects in Bengali and Telugu test splits cannot be determined from this sample alone.

4. **Telugu agricultural sub-regional specificity requires corpus-level inspection.** Whether any Telugu test questions address Telangana dry-land cropping or Andhra coastal aquaculture cannot be confirmed or excluded from 25 validation examples. Direct inspection of the Telugu test split subject distribution would be needed.

5. **Machine translation register effects are not directly assessable from this data.** The extent to which GPT-4O translation introduces Indian Bengali register conventions (vs. generic translated register) cannot be assessed from reading translated MCQs alone, as the content of these questions is domain-neutral (engineering, computing, history). Register effects would be most visible in culturally-loaded or dialect-sensitive agricultural terminology, which is absent from the sample.

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
  "benchmark": "milu",
  "region": "Mymensingh Environmental Scientist — Cross-Regional South Asian Agricultural Knowledge",
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
