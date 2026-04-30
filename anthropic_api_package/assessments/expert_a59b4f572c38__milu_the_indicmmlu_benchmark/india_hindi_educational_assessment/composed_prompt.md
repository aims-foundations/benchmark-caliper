I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **MILU: A Multi-task Indic Language Understanding Benchmark** is valid for use in **North Indian Hindi-Medium Postgraduate Teacher — MCQ Evaluation Deployment**.

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
- **Full Name**: MILU: A Multi-task Indic Language Understanding Benchmark
- **Domain**: Multilingual Indic language understanding (MCQ-based)
- **Languages**: hi, bn, gu, kn, ml, mr, or, pn, ta, te, en
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
MILU defines its test case taxonomy as 8 domains (Arts and Humanities, Social
Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science,
Engineering and Technology, and Business Studies) containing 41 subjects [Q42],
all instantiated exclusively as multiple-choice questions [Q22]. The benchmark is
described as "comprehensive" with an emphasis on India-specific knowledge [Q74],
and subject-level statistics across languages are documented in supplementary
tables [Q98]. However, the taxonomy was derived from competitive exam content
[Q23, Q24] — national civil service, qualification, and state-level entrance
exams [Q27, Q92] — rather than from school or university board syllabi. No
documentation establishes that the 41 subjects and 8 domains adequately represent
the curricular framing used in Hindi state boards (UP, MP, Rajasthan, Bihar) or
CBSE school contexts. Arts & Humanities and Law & Governance subjects are included,
but these are documented as areas of particularly poor model performance [Q6, Q71],
with the paper attributing this to insufficient culturally specific data in model
training corpora [Q72] rather than to any acknowledged gap in the taxonomy itself.
The evaluation of Indic language-specific fine-tuned LLMs is also treated as a
distinct sub-taxonomy [Q60], indicating awareness of the heterogeneity of target
systems.

### Input Content
MILU's questions were sourced from over 1,500 competitive exams [Q13] scraped from
online exam portals [Q25] covering more than 40 exam types at national and state
levels [Q27, Q92]. The benchmark explicitly incorporates state- and region-level
exams to capture local knowledge in each respective language [Q14, Q28], with
national-level, government/private-organization, and state-level civil service exam
sources documented in supplementary tables [Q95, Q96, Q97]. Regional provenance is
affirmed at a high level — MILU was "designed with an India-first perspective" [Q11]
and includes culturally relevant subjects such as local history, arts, festivals,
and laws [Q2, Q12]. English questions are included to address India-specific cultural
content absent from other benchmarks [Q30]. However, approximately 25% of the total
79,000 questions were translated from English using GPT-4O [Q44, Q45, Q47], a method
chosen for task-awareness but not validated for alignment with Hindi-board register or
subject-specific terminology. For subjects with fewer than 100 questions in a given
language, English items were sampled and translated [Q43, Q44], introducing a concrete
surface-level validity risk for Hindi items requiring North Indian academic register.
The paper does not break down exam-source distribution by state for individual
languages [Q97], leaving it undocumented whether Hindi-language items are
proportionally drawn from UP, MP, Rajasthan, and Bihar state-level exams versus
pan-India competitive exams. All data was scraped from publicly available resources
[Q88] and will be released under permissible licenses [Q89, Q90].

### Input Form
MILU is exclusively text-based MCQ, which aligns with the Devanagari-script Hindi
deployment context. Questions with images, reading-comprehension passages, or more
than four answer options were explicitly excluded to enforce uniformity [Q33].
Language verification was performed using INDICLID and Unicode-based filtering to
ensure correct-language assignment [Q34], and duplicate removal was applied [Q35].
Hindi is a high-resource language within MILU's 11-language scope, and the benchmark
documents that models perform better in high-resource languages [Q5], which works
in Hindi's favour. No script mismatch concerns are documented or expected: Devanagari
script is the native representation for Hindi, and MILU's infrastructure is text-only
throughout. Initial and final manual review steps [Q32, Q36] provide additional
quality assurance on input form consistency.

### Output Ontology
Ground-truth labels are single correct answers per MCQ, drawn from exam answer keys
[Q12]. After clustering approximately 20,000 fine-grained tags [Q39] and manual
merging of clusters, 41 distinct subject names organized into 8 domains were
established as the output categorization [Q42]. The label schema is effectively
binary (correct/incorrect) at inference time, which fully aligns with the deployment's
positive/negative marking requirement. No rubric-based or graded output taxonomy is
involved. The paper documents domain-level accuracy as the primary reporting unit,
revealing a consistent pattern of lower performance in culturally specific domains
[Q20, Q71] versus STEM. The paper does not discuss whether any output categories
carry culturally variable correct-answer norms — an absence that is noted, though
not confirmed as a misalignment for the North Indian teacher deployment context,
since the user confirmed that evaluation schemas are broadly consistent across boards
and competitive-exam settings.

### Output Content
Annotation of question-answer pairs relied primarily on subject experts at online
exam portals who manually tagged questions and ensured answer accuracy [Q26].
Additional manual audit was performed by AI4Bharat team volunteers [Q87], and
cluster-to-subject label assignment was done manually [Q41]. NOT DOCUMENTED: the
paper does not provide demographic details about annotators (regional background,
Hindi-medium vs. English-medium background, subject expertise domain), nor does it
report inter-annotator agreement statistics. The absence of annotator demographics
is a moderate validity gap for the deployment context — if annotators were not drawn
from Hindi-medium North Indian educational backgrounds, subtle misalignments in
answer keys for culturally or regionally specific items (e.g., local history, Hindi
literature, regional civics) could remain undetected. The user did note, however,
that evaluation schemas are broadly consistent across boards, reducing the severity
of this concern.

### Output Form
MILU evaluates models using accuracy as the primary metric [Q3, Q15, Q16, Q75].
For non-API models, log-likelihood scoring selects the answer option with the
highest conditional log probability [Q52, Q53, Q54, Q55], implemented via
LM-EVALUATION-HARNESS for reproducibility [Q52]. API-based models are evaluated
generatively in zero-shot setup using structured JSON output prompting [Q56, Q57],
with cost constraints limiting these to zero-shot only [Q58]. Results are reported
at 0-shot, 1-shot, and 5-shot levels [Q50, Q100] with 5-shot accuracy as the
headline figure [Q59]. Per-model, per-subject, per-language result tables are
provided extensively in supplementary materials [Q99–Q132], offering granular
evidence for Hindi-specific performance. The authors acknowledge that the
log-likelihood evaluation method may yield different results compared to
generation-based evaluation or chain-of-thought prompting [Q85], a relevant caveat
if the deployment uses generative inference rather than discriminative scoring.
Output form is otherwise well-matched to the binary MCQ deployment requirement.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge." |
| Q2 | 1 | input_content | "With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science." |
| Q3 | 1 | output_form | "We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q4 | 1 | output_form | "Open multilingual models outperform language-specific fine-tuned models, which perform only slightly better than random baselines." |
| Q5 | 1 | input_ontology | "Models also perform better in high-resource languages as compared to low-resource ones." |
| Q6 | 1 | input_ontology | "Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM." |
| Q7 | 1 | input_ontology | "To the best of our knowledge, MILU is the first of its kind benchmark focused on Indic languages, serving as a crucial step towards comprehensive cultural evaluation." |
| Q8 | 1 | output_form | "All code, benchmarks, and artifacts will be made publicly available to foster open research." |
| Q9 | 1 | output_content | "Sshubam Verma, Mohammed Safi Ur Rahman Khan, Vishwajeet Kumar, Rudra Murthy, Jaydeep Sen" |
| Q10 | 1 | output_content | "Nilekani Centre at AI4Bharat, Indian Institute of Technology, Madras, IBM Research, India" |
| Q11 | 2 | input_content | "We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams." |
| Q12 | 2 | output_ontology | "These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science." |
| Q13 | 2 | input_content | "Following previous efforts (Hendrycks et al., 2021; Zhong et al., 2023), we create this benchmark by collecting questions from over 1500 competitive exams from India." |
| Q14 | 2 | input_content | "We focus on region-specific exams to authentically capture local knowledge in the respective language." |
| Q15 | 2 | output_form | "We evaluate 45 different LLMs - a mix of closed proprietary, open-source, and language-specific models- on MILU." |
| Q16 | 2 | output_form | "Our findings suggest that models struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q17 | 2 | output_form | "Interestingly, open multilingual models outperform language-specific models, which only achieve slightly better than random scores." |
| Q18 | 2 | output_form | "Our analysis of in-context learning reveals that adding more examples improves performance in base models, but the effect on instruct models remains inconclusive." |
| Q19 | 2 | output_form | "We also explore how performance scales with the number of parameters, finding significant improvements as model size increases." |
| Q20 | 2 | output_ontology | "Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM." |
| Q21 | 2 | output_form | "All the artifacts will be released publicly." |
| Q22 | 3 | input_ontology | "MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge." |
| Q23 | 3 | input_ontology | "This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others." |
| Q24 | 3 | input_content | "These questions were sourced following an approach similar to AGIEVAL (Zhong et al., 2023), collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams, among others." |
| Q25 | 3 | input_content | "We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages." |
| Q26 | 3 | output_content | "These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers." |
| Q27 | 3 | input_content | "Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years." |
| Q28 | 3 | input_content | "Regional state exams are particularly valuable as they cover various state-level topics and emphasize the official language of each state." |
| Q29 | 3 | input_content | "In total, we collected more than 150K questions across 11 Indian Languages- Bengali (bn), Gujarati (gu), Hindi (hi), Kannada (kn), Malayalam (ml), Marathi (mr), Odia (or), Punjabi (pn), Tamil (ta), Telugu (te), and English (en)-spanning 41 diverse subjects." |
| Q30 | 3 | input_content | "English questions are also included as these often address Indian culture-specific content, which is notably missing from existing popular benchmarks." |
| Q31 | 4 | input_form | "Despite our best efforts to maintain the quality of questions collected, some amount of noise or errors may still be present. To address potential noise in the questions, we employ multiple layers of manual and automated cleaning filters." |
| Q32 | 4 | input_form | "Initially, we manually review a large sample of questions to detect and eliminate potential sources of noise." |
| Q33 | 4 | input_form | "During the collection process, we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency." |
| Q34 | 4 | input_form | "To remove incorrect language entries, we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering (Khan et al., 2024), ensuring that the questions are in the correct language." |
| Q35 | 4 | input_form | "To further refine the dataset, we remove any duplicate questions to retain only the unique ones." |
| Q36 | 4 | input_form | "As a final step, we manually verify a sample of questions from each language to ensure accuracy and correct any remaining errors." |
| Q37 | 4 | input_content | "Upon examination, we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information." |
| Q38 | 4 | input_content | "To address this issue, we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question." |
| Q39 | 4 | output_ontology | "Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap." |
| Q40 | 4 | output_ontology | "To organize them, we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters." |
| Q41 | 4 | output_content | "We manually review these clusters and assign appropriate subject labels." |
| Q42 | 4 | output_ontology | "Following the manual merging of related clusters, we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies." |
| Q43 | 4 | input_content | "Finally, we observed that some topics in certain languages had less than 100 questions. To ensure thorough evaluation across all subjects and languages, we aimed to have at least 100 questions per subject in each language." |
| Q44 | 4 | input_content | "For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O." |
| Q45 | 4 | input_content | "We chose GPT-4O over specialized translation models for their ability to remain task-aware during translation (Ahuja et al., 2024), ensuring the translated content aligns with the intent of the question." |
| Q46 | 4 | input_content | "In total, we release around 79K questions across 41 subjects across 8 domains in 11 languages, capping each subject-language pair at 500 questions for feasible evaluations." |
| Q47 | 4 | input_content | "Table 2 shows the overall statistics of MILU. Of the total 79K questions, only 25% of questions are translated from English, with the remainder" |
| Q48 | 5 | output_form | "We evaluate 42 different models on MILU, including large proprietary models, open-source multilingual models, and popular fine-tuned models specific to Indic languages." |
| Q49 | 5 | output_form | "Both the base versions and instruction fine-tuned variants of these models, wherever applicable, are evaluated to measure the improvements gained from fine-tuning." |
| Q50 | 5 | output_form | "All models, except for proprietary models and LLAMA-3.1-405B, are tested under 0-shot, 1-shot, and 5-shot setups." |
| Q51 | 5 | input_content | "We maintain a separate validation set of approximately 9,000 questions to serve as examples for few-shot evaluations." |
| Q52 | 5 | output_form | "For non-API-based models, we use the LM-EVALUATION-HARNESS (Gao et al., 2024; Biderman et al., 2024) to ensure clean and reproducible evaluations." |
| Q53 | 5 | output_form | "We use the log-likelihood method, where the probability of a given output string is computed by conditioning it on some provided input (Brown et al., 2020)." |
| Q54 | 5 | output_form | "Specifically, the log-likelihood of an answer (a) given the question (x), i.e., logP(a\|x), is calculated by concatenating the answer (a) with question (x), and then summing up the log probabilities, of each target token." |
| Q55 | 5 | output_form | "For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability, i.e., argmax(logP(a1\|x), ..., logP(ak\|x))." |
| Q56 | 5 | output_form | "The API-based models are evaluated using the generative approach due to the lack of support for prompt log probabilities." |
| Q57 | 5 | output_form | "We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing." |
| Q58 | 5 | output_form | "Due to the high costs involved, these models are evaluated only in the zero-shot setup." |
| Q59 | 6 | output_form | "We report 5-shot accuracies for all open models (except for LLAMA-3.1-70B-INSTRUCT & LLAMA-3.1-405B for which we report 0-shot accuracy) with the accuracy averaged across all the domains per language." |
| Q60 | 6 | input_ontology | "We evaluate around 16 Indic language LLMs on MILU. These models are primarily built by adapting English LLMs, such as LLAMA-2-7B, by first continually pretraining on small amount Indic language data, followed by optionally instruction finetuning them." |
| Q61 | 6 | output_form | "As seen from Table 4, across languages, the models exhibit average performance comparable to random baselines, with minimal variations among them." |
| Q62 | 6 | output_ontology | "When analyzed across domains, the models generally perform worse in Arts, Humanities, and Social Sciences than in STEM subjects." |
| Q63 | 6 | output_form | "We compare the performance of different Base and Instruct models across zero, one, and five-shot setups." |
| Q64 | 6 | output_form | "As shown in Figure 3, the performance of base models consistently improves with an increasing number of in-context examples, with the 5-shot setup yielding the best results." |
| Q65 | 6 | output_form | "In contrast, Instruct models exhibit more varied behavior, where models either stagnate or even degrade in performance." |
| Q66 | 6 | output_form | "This also aligns with expectations, as Instruct models are specifically fine-tuned as conversation assistants and may not respond well to the few-shot in-context examples format." |
| Q67 | 7 | output_form | "Table 4: Evaluation results of all the language-specific fine-tuned models on MILU. We report domain level 5-shot accuracies for all the models on the language supported by the model. Higher values indicate better model performance for the given domain." |
| Q68 | 7 | output_form | "Figure 3: Comparison of Base and Instruct models averaged across all languages for varying number of in-context examples. We plot the average accuracies of the GEMMA and LLAMA series of models, highlighting the performance trend as the number of in-context examples increases." |
| Q69 | 7 | output_form | "We evaluate the LLAMA and GEMMA family of models, ranging from 1B to 405B parameters, to analyze how performance scales with model size." |
| Q70 | 7 | output_form | "Figure 5 shows that the model performance improves significantly with increasing scale. Notably, instruction-tuned models in the LLAMA family show more substantial improvements as compared to those in the GEMMA family." |
| Q71 | 7 | output_ontology | "We analyze the performance of various base and instruct models across multiple domains and languages. Similar trends to those in Section (§5.2) are observed where the open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields." |
| Q72 | 7 | input_content | "This suggests that the training corpora for these models lack sufficient culturally specific data. Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages." |
| Q73 | 7 | output_form | "As most Indic LLMs are built on English base models like LLAMA-2-7B, we assess the impact of language adaptation on their performance. Table 5 compares language-specific models with the original LLAMA-2-7B, and instruction-tuned models with LLAMA-2-7B-CHAT. Our findings show minimal gains, with some models even underperforming post-adaptation." |
| Q74 | 8 | input_ontology | "In this paper, we introduced MILU—Multilingual Indic Language Understanding Benchmark-a comprehensive benchmark specifically designed to evaluate LLMs across 11 Indic languages, spanning diverse domains and culturally relevant subjects." |
| Q75 | 8 | output_form | "We evaluate 45 different LLMs and find that the majority of LLMs struggle on MILU, with GPT4o achieving the highest average accuracy." |
| Q76 | 8 | input_ontology | "The analysis also shows that models perform significantly better in high-resource languages than low-resource ones, highlighting the need for more robust multilingual strategies." |
| Q77 | 8 | output_ontology | "Additionally, the domain-specific analysis indicates that models perform better in general fields such as STEM while facing challenges in culturally relevant subjects like Arts, Humanities, and Law, highlighting the lack of this knowledge in the current models and datasets." |
| Q78 | 8 | output_form | "We conjecture that limited performance gains may result from small language-specific datasets and reliance on parameter-efficient methods like LoRA (Hu et al., 2022)." |
| Q79 | 8 | output_form | "Another contributing factor could be the lack of diversity in instruction fine-tuning datasets." |
| Q80 | 8 | output_form | "Models like AIRAVATA, which utilize more diverse data (Gala et al., 2024), exhibit noticeably better performance." |
| Q81 | 8 | output_ontology | "Further investigation is required to fully understand the limitations and opportunities in this area." |
| Q82 | 9 | input_ontology | "First, we restricted our study to the top 11 languages due to the lack of readily available questions in low-resource languages, which we aim to address in future work." |
| Q83 | 9 | output_form | "Second, limited computational resources prevented a thorough evaluation of larger models, such as LLAMA-3.1-70B-INSTRUCT and LLAMA-3.1-405B." |
| Q84 | 9 | input_content | "Third, the scarcity of questions necessitated translating a portion of the dataset." |
| Q85 | 9 | output_form | "Finally, our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting." |
| Q86 | 9 | output_content | "We would like to thank EkStep Foundation and Nilekani Philanthropies for their generous grant towards building datasets, models, tools and other resources for Indian languages." |
| Q87 | 9 | output_content | "We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits." |
| Q88 | 9 | input_content | "All data described in this work was scraped from publicly available resources." |
| Q89 | 9 | input_content | "The datasets used in this paper will be made available under permissible licenses." |
| Q90 | 9 | input_content | "Additionally, the code used for our evaluations will be made publicly available under the MIT License." |
| Q91 | 10 | output_content | "Sumanth Doddapaneni, Rahul Aralikatte, Gowtham Ramesh, Shreya Goyal, Mitesh M. Khapra, Anoop Kunchukuttan, and Pratyush Kumar. 2023. Towards leaving no Indic language behind: Building monolingual corpora, benchmark and models for Indic languages. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 12402–12426, Toronto, Canada. Association for Computational Linguistics." |
| Q92 | 17 | input_content | "We collected our questions from over 40 exam types ranging from various National and state level civil service examinations to examinations conducted by various government and private organizations." |
| Q93 | 17 | input_form | "Detailed analysis of topic and language distribution across languages can be found in Table 9 and Figure 6" |
| Q94 | 17 | output_form | "Model details about the different models evaluated in this work is present in Table 10." |
| Q95 | 18 | input_content | "Table 6: Overview of various national-level exams and the corresponding years of coverage considered in MILU." |
| Q96 | 18 | input_content | "Table 7: Overview of various government and private organization exams and the corresponding years of coverage considered in MILU." |
| Q97 | 18 | input_content | "Table 8: Overview of various State-level civil services exams and the corresponding years of coverage considered in MILU." |
| Q98 | 20 | input_ontology | "Table 9: Detailed subject level statistics of MILU across different languages." |
| Q99 | 22 | output_form | "Table 11: Detailed subject-wise evaluation for ABHINAND/TAMIL-LLAMA-7B-INSTRUCT-V0.2 on MILU across different languages." |
| Q100 | 22 | output_form | "The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q101 | 23 | output_form | "Table 12: Detailed subject-wise evaluation for AI4BHARAT/AIRAVATA on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q102 | 24 | output_form | "Table 13: Detailed subject-wise evaluation for BHABHAAI/GAJENDRA-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q103 | 25 | output_form | "Table 14: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-BASE-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q104 | 26 | output_form | "Table 15: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q105 | 27 | output_form | "Table 16: Detailed subject-wise evaluation for GENVRADMIN/ARYABHATTA-GEMMAGENZ-VIKAS-MERGED on MILU across different languages." |
| Q106 | 28 | output_form | "Table 17: Detailed subject-wise evaluation for MANISHIITG/OPEN-ADITI-V6-LLAMA3 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q107 | 29 | output_form | "Table 18: Detailed subject-wise evaluation for NICKMALHOTRA/PROJECTINDUS on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q108 | 30 | output_form | "Table 19: Detailed subject-wise evaluation for SARVAMAI/OPENHATHI-7B-HI-V0.1-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q109 | 31 | output_form | "Table 20: Detailed subject-wise evaluation for TENSOIC/KAN-LLAMA-7B-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q110 | 32 | output_form | "Table 21: Detailed subject-wise evaluation for ABHINAND/MALAYALAM-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages." |
| Q111 | 33 | output_form | "Table 22: Detailed subject-wise evaluation for ABHINAND/TELUGU-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q112 | 34 | output_form | "Table 23: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q113 | 35 | output_form | "Table 24: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-BASE-V0.1 on MILU across different languages." |
| Q114 | 36 | output_form | "Table 25: Detailed subject-wise evaluation for TELUGU-LLM-LABS/TELUGU-LLAMA2-7B-V0-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q115 | 37 | output_form | "Table 26: Detailed subject-wise evaluation for GPT-4o on MILU across different languages. The results reported are for 0-shot experiments." |
| Q116 | 38 | output_form | "Table 27: Detailed subject-wise evaluation for GPT-4O-MINI on MILU across different languages. The results reported are for 0-shot experiments." |
| Q117 | 39 | output_form | "Table 28: Detailed subject-wise evaluation for GEMINI-1.5-PRO on MILU across different languages. The results reported are for 0-shot experiments." |
| Q118 | 40 | output_form | "Table 29: Detailed subject-wise evaluation for GEMINI-1.5-FLASH on MILU across different languages. The results reported are for 0-shot experiments." |
| Q119 | 41 | output_form | "Table 30: Detailed subject-wise evaluation for KRUTRIM-SPECTRE-V2 on MILU across different languages. The results reported are for 0-shot experiments." |
| Q120 | 42 | output_form | "Table 31: Detailed subject-wise evaluation for SARVAMAI/SARVAM-1 on MILU across different languages. The results reported are for 5-shot experiments." |
| Q121 | 43 | output_form | "Table 32: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.2-1B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q122 | 43 | output_form | "Table 33: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.2-1B-INSTRUCT on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q123 | 44 | output_form | "Table 34: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q124 | 44 | output_form | "Table 35: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B-IT on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q125 | 46 | output_form | "Table 38: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.2-3B-INSTRUCT on MILU across different languages." |
| Q126 | 47 | output_form | "Table 39: Detailed subject-wise evaluation for NVIDIA/NEMOTRON-4-MINI-HINDI-4B-BASE on MILU across different languages. The results reported are for 5-shot experiments." |
| Q127 | 49 | output_form | "Table 42: Detailed subject-wise evaluation for NEULAB/PANGEA-7B on MILU across different languages. The results reported are for 5-shot experiments." |
| Q128 | 52 | output_form | "Table 47: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-9B-IT on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q129 | 52 | output_form | "Table 48: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-27B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q130 | 55 | output_form | "Table 52: 0-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q131 | 56 | output_form | "Table 53: 1-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q132 | 57 | output_form | "Table 54: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.1-405B on MILU across different languages. The results reported are for 0-shot experiments." |

---

## Regional Context

```yaml
name: North Indian Hindi-Medium Postgraduate Teacher — MCQ Evaluation Deployment
abbreviation: IN-HI-TEACHER-MCQ
deployment_context:
  description: Postgraduate- or PhD-qualified Hindi-medium teachers in North India
    using an LLM-powered mobile or enterprise application to evaluate student responses
    to multiple-choice questions (MCQs), assign scores under positive/negative marking
    schemes, and provide binary correct/incorrect feedback. The benchmark being assessed
    (MILU) is evaluated specifically through its Hindi-language MCQ items against
    this deployment population.
  benchmark: MILU (Multi-task Indic Language Understanding Benchmark)
  primary_use_case: Automated MCQ response evaluation with binary correct/incorrect
    scoring and binary feedback output; no open-ended grading or rubric-based judgment
    required.
  deployment_modality: Mobile application or enterprise desktop application; text-only
    interaction in Hindi (Devanagari script)
geography:
  country: India
  region: North India (Hindi Belt)
  primary_states:
  - Uttar Pradesh
  - Madhya Pradesh
  - Rajasthan
  - Bihar
  - Uttarakhand
  - Haryana
  - Himachal Pradesh
  - Chhattisgarh
  - Jharkhand
  urbanization_note: 'Target population spans urban district headquarters and semi-urban/rural
    towns where government schools and colleges are located; urban-rural split within
    the teacher cohort is [NEEDS VERIFICATION — deferred: below search budget; UDISE+
    data covers schools not teacher residence/work distribution by urban-rural category].'
  state_population_shares:
    uttar_pradesh: '[NEEDS VERIFICATION — deferred: below search budget; census 2011
      figure ~16.5% of India population widely cited but state-board-specific enrolment
      share not verified this pass]'
    madhya_pradesh: '[NEEDS VERIFICATION — deferred: below search budget]'
    rajasthan: '[NEEDS VERIFICATION — deferred: below search budget]'
    bihar: '[NEEDS VERIFICATION — deferred: below search budget]'
    note: 'UP, MP, Rajasthan, and Bihar together account for a majority of Hindi-medium
      school enrolment in India; exact proportions [NEEDS VERIFICATION — deferred:
      below search budget].'
target_population:
  role: Hindi-medium schoolteacher or college lecturer holding a postgraduate or doctoral
    degree, employed under a state or central board institution
  qualification_range: MA/MSc/MCom minimum; PhD holders also in scope; B.Ed. or equivalent
    teacher training likely but not mandatory for all cohorts
  experience_range_years: 0–20+
  institutional_affiliation_types:
  - Government secondary and senior secondary schools (state board)
  - Private aided and unaided schools (state and central board)
  - Government degree colleges
  - Private degree colleges affiliated to state universities
  estimated_cohort_size: '[NEEDS VERIFICATION — deferred: below search budget; likely
    unsearchable at the required precision (postgraduate-qualified Hindi-medium teachers
    specifically across UP, MP, Rajasthan, Bihar)]'
  gender_distribution: '[NEEDS VERIFICATION — deferred: likely unsearchable at required
    sub-national precision for this specific cohort; UDISE+ publishes aggregate teacher
    gender data but not broken down by qualification level and language medium]'
  age_distribution: '[NEEDS VERIFICATION — deferred: below search budget; likely unsearchable
    for this specific cohort]'
languages:
  primary: Hindi (Khari Boli / Modern Standard Hindi — formal written register expected
    for MCQ item language)
  script: Devanagari (Unicode; right-to-left NOT applicable — Devanagari is left-to-right)
  register_notes: Formal academic Hindi (शुद्ध हिंदी / Shuddh Hindi) is the expected
    register for MCQ items and scoring rationale. Regional spoken varieties (Awadhi,
    Bhojpuri, Braj Bhasha, Bundeli, Mewari, Maithili) are mother tongues for many
    teachers but are not the medium of instruction or examination. Subtle lexical
    and orthographic divergences between pan-India Khari Boli examination Hindi and
    local academic Hindi usage in UP, Bihar, or Rajasthan are a flagged validity concern.
  code_switching: Minimal for formal MCQ context; Hindi-English code-mixing may appear
    in technical subject terminology (science, economics, IT)
  english_role: Secondary; English-medium board content may appear in translated form;
    English technical terms are commonly retained in Hindi scientific and economic
    discourse
  other_languages_in_scope: None — deployment is Hindi-only; benchmark items from
    other Indic languages are out of scope for this assessment
writing_system:
  script: Devanagari
  directionality: Left-to-right
  unicode_block: U+0900–U+097F (Devanagari)
  nlp_notes: Hindi is a high-resource Indic language with mature NLP tooling (INDICLID,
    INDICTRANS2, IndicBERT, etc.). Devanagari tokenization is well-supported in major
    LLM frameworks. Morphological complexity (sandhi, vibhakti suffixes, conjunct
    consonants) is lower than for some other Indic scripts but still non-trivial for
    tokenizers trained on Latin-script corpora.
  orthographic_variation_risk: Moderate — spelling conventions for loan words and
    transliterated English terms vary across UP, MP, Rajasthan, and Bihar state board
    textbooks; nukta usage and anusvara/chandrabindu choices may differ from pan-India
    standardized exam Hindi
educational_system:
  board_types_in_scope:
  - UP Board (Uttar Pradesh Madhyamik Shiksha Parishad — UPMSP)
  - MP Board (Madhya Pradesh Board of Secondary Education — MPBSE)
  - Rajasthan Board (Board of Secondary Education Rajasthan — RBSE)
  - Bihar Board (Bihar School Examination Board — BSEB)
  - CBSE (Central Board of Secondary Education) — Hindi-medium stream only
  - State university undergraduate syllabi (for degree-college teacher users)
  board_types_out_of_scope: English-medium board content (CBSE English medium, ICSE,
    IB, IGCSE) unless translated into Hindi and aligned with Hindi-board norms per
    deployment specification
  assessment_format: Strict MCQ — single correct answer per item; positive marks awarded
    for correct selection; negative marks (penalty) deducted for incorrect selection;
    no partial credit; no open-ended or rubric-based grading
  positive_negative_marking_conventions:
    typical_correct_mark: 'Varies by exam type: UPSC Prelims awards +2 marks per question
      (GS Paper I, 100 questions, 200 marks total); SSC CGL and banking exams typically
      use +1 per question; NEET uses +4. State PSC exams vary and candidates should
      verify per notification. Source: multiple Indian competitive exam portals —
      [WEB-1]; [WEB-2]'
    typical_incorrect_penalty: 'UPSC Prelims: −1/3 of marks per question (−0.66 for
      GS Paper I at 2 marks/question); SSC CGL: −0.5 marks per wrong answer; Banking/IBPS
      PO: −0.25 marks per wrong answer; NEET: −1 mark per wrong answer; State PSCs
      vary (typically −1/4 or −1/3). Unattempted questions attract no penalty in any
      standard Indian competitive exam. Source: [WEB-1];
      [WEB-3]; [WEB-2]'
    note: 'Conventions vary by board and exam; the deployment must handle configurable
      mark values. State PSC exams follow different negative marking rules depending
      on exam notification — some use 1/3, others 1/4 or fixed penalties. Source:
      [WEB-1]'
  curricular_domains_in_scope:
  - 'Hindi Language and Literature (including canonical texts: Tulsidas, Premchand,
    Kabir, Mahadevi Varma, Harivansh Rai Bachchan, Rani Lakshmibai biographies, etc.)'
  - History (with emphasis on regional medieval history, freedom movement, North Indian
    historical figures)
  - Geography (with emphasis on North Indian physical and human geography)
  - Civics and Political Science (including state governance structures, Panchayati
    Raj, UP/MP/Rajasthan/Bihar administrative specifics)
  - Science (Physics, Chemistry, Biology — translated into Hindi register)
  - Mathematics
  - Social Science (Economics, Sociology)
  - General Knowledge (India-centric, competitive-exam style)
  state_board_syllabus_vs_competitive_exam_framing: 'A flagged validity gap: MILU
    draws from competitive exams (UPSC, SSC, state civil services) rather than school/university
    board syllabi. The framing of canonical figures (e.g., Tulsidas in a literary
    vs. administrative-GK context) may differ. [NEEDS VERIFICATION — see flagged gap
    1 and 5 in elicitation summary; searches did not surface any published comparison
    between MILU Hindi items and UP/MP/Rajasthan/Bihar board syllabi; this gap remains
    unresolved]'
  cbse_hindi_medium_inclusion: 'CBSE Hindi-medium stream items are in scope; translated
    English-medium CBSE content is in scope only when aligned to Hindi-board norms.
    MILU does not explicitly include translated CBSE/ICSE English-medium content.
    [NEEDS VERIFICATION — deferred: below search budget; no published MILU documentation
    resolves this]'
cultural_norms_notes: '- North Indian Hindi-belt educational culture is strongly shaped
  by examination success orientation (pariksha sanskriti); rote learning and answer-key
  authority are the norm in MCQ contexts

  - Canonical Hindi literary figures (Tulsidas, Kabir, Premchand, Mahadevi Varma)
  hold high cultural authority in the curriculum and are frequently referenced in
  board exams

  - Regional medieval history (Maratha, Mughal, Rajput, Sikh periods) and local freedom-movement
  figures (Rani Lakshmibai, Bhagat Singh) are prominently represented in North Indian
  board syllabi

  - Competitive-exam culture (UPSC, SSC, state PCS) is pervasive and influential;
  teachers are often themselves products of this system and may accept competitive-exam
  keyed answers as authoritative

  - Respect for institutional authority (board answer keys, official textbooks) is
  high; teachers are unlikely to question canonical correct answers

  - Hindi is a marker of regional identity in UP, MP, Rajasthan, and Bihar; Shuddh
  Hindi versus Hindustani register choices can carry cultural significance

  - Panchayati Raj, local governance, and state-specific civics content reflect North
  Indian administrative structures that may not appear in pan-India competitive exams

  - Ramcharitmanas and other devotional literary texts occupy a special position —
  simultaneously literary, religious, and civically significant — requiring sensitive
  and accurate framing in assessment items

  '
infrastructure_notes: '- Mobile-first deployment likely for many users; smartphone
  penetration among postgraduate-educated teachers is high but varies by state and
  rural/urban context

  - Mobile internet penetration in North Indian teacher cohort: Bihar internet penetration
  is among the lowest in India at approximately 43% of the total state population
  (IAMAI/Kantar ICUBE 2024 — [WEB-4]);
  Uttar Pradesh stands at approximately 46% (IAMAI/Kantar ICUBE 2024 — [WEB-4]).
  These are general-population figures; postgraduate-educated teachers are likely
  in higher-penetration segments, but rural school postings in UP and Bihar will face
  meaningful connectivity constraints. Rajasthan and MP figures are not individually
  broken out in the same table but fall in a similar mid-range band. National urban
  internet penetration is approximately 67% vs. 37% in rural areas (TRAI, 2023 — cited
  in [WEB-5]).

  - Typical device tier (budget Android vs. mid-range): [NEEDS VERIFICATION — deferred:
  below search budget; national data shows 74% urban household smartphone ownership
  vs. 45% rural (UDISE+ / TRAI 2023 cited in [WEB-5])
  but teacher-cohort-specific device-tier data is not published]

  - Enterprise desktop application availability in government school settings: Low
  likely — only 22% of rural schools have functional computer labs (UDISE+ 2023 —
  cited in [WEB-5]);
  internet access available in only 18% of rural schools vs. 62% urban schools (UDISE+
  2023 — [WEB-5]).
  Desktop-enterprise deployment will have very limited reach in rural government school
  settings.

  - State government edtech infrastructure (e.g., DIKSHA platform integration, state-specific
  LMS): DIKSHA (Digital Infrastructure for Knowledge Sharing) is the Ministry of Education''s
  national digital platform, multilingual and mobile-friendly, with over 120 million
  learners and 2.5 million teachers across K-12, content in 35+ Indian languages,
  and over 63 lakh teachers completing NISHTHA training via DIKSHA (Ministry of Education
  / roombr.com — [WEB-6];
  ORF — [WEB-7]).
  NEP 2020 mandates technology integration and digital pedagogy for educators. LLM-powered
  assessment tools are not yet integrated into DIKSHA as of 2025; any deployment would
  sit outside DIKSHA unless explicitly integrated.

  - Network connectivity in rural school settings (2G/3G/4G coverage in UP, Bihar,
  Rajasthan rural areas): TRAI reports approximately 95% of Indian villages have 3G/4G
  connectivity as of 2024 (TRAI data cited in [WEB-8]),
  but having coverage does not equate to reliable indoor school connectivity; actual
  usage penetration in Bihar (43%) and UP (46%) remains low at the general population
  level.

  - Hindi Devanagari keyboard availability and input method editor (IME) adoption
  on mobile devices: [NEEDS VERIFICATION — deferred: below search budget; likely unsearchable
  at the required sub-national precision]

  - LLM inference latency tolerance for classroom or evaluation workflow context:
  assumed low (sub-10 seconds preferred)

  '
benchmark_language_specific_notes:
  hindi_resource_level: High-resource within MILU's 11-language scope; MILU documents
    that models perform better in high-resource languages, favouring Hindi performance
  hindi_item_count_in_milu: '[NOT FOUND — searched GitHub, HuggingFace, arXiv abstract,
    and IndiaAI portal for MILU; no per-language item count for Hindi is published
    in any publicly accessible summary. The paper cites a cap of 500 questions per
    subject-language pair across 41 subjects, implying a theoretical maximum of ~20,500
    Hindi test items, but the actual count (accounting for subjects with fewer available
    native questions) is only in supplementary Table 9 of the full paper PDF, which
    is not machine-accessible without authentication. The dataset itself is gated
    on HuggingFace — [WEB-9]. The NAACL
    2025 published version is at [WEB-10].]'
  translation_exposure: 'Approximately 25% of MILU items were translated from English
    using GPT-4O for subjects with fewer than 100 native-language questions; it is
    undocumented what proportion of Hindi items specifically are translated vs. natively
    sourced [NOT FOUND — no source publishes a Hindi-specific translation proportion;
    the 25% figure is a dataset-wide aggregate across all 11 languages. Source: arXiv
    2411.02538 — [WEB-11]]'
  hindi_register_standardisation: MILU applies Unicode/INDICLID filtering but does
    not document intra-Hindi register or dialect standardisation; whether items use
    pan-India Khari Boli or accommodate UP/Bihar/Rajasthan state-board lexical norms
    is undocumented [NOT FOUND — no published MILU documentation addresses intra-Hindi
    register variation; this remains a full gap per the benchmark's own documentation]
  state_wise_exam_source_distribution_for_hindi: '[NOT FOUND — searched GitHub, HuggingFace,
    arXiv HTML, and supplementary materials descriptions; the paper references supplementary
    Table 8 for state-level civil service exams covered (NAACL 2025 paper — [WEB-10])
    but does not publish a language-specific state-wise breakdown in any publicly
    accessible format. The gated dataset structure confirms a Hindi subdirectory exists
    but per-state source metadata is not exposed.]'
  arts_humanities_hindi_literature_framing: '[NOT FOUND — no published MILU source
    specifies whether Arts & Humanities Hindi items frame canonical literary figures
    (Tulsidas, Premchand, Kabir) in a school-literature or competitive-exam GK register;
    the GitHub subject list includes ''Literature and Linguistics'' and ''Arts and
    Culture'' as subject categories (GitHub — [WEB-12])
    but no item-level framing detail is publicly available without dataset access]'
domain_specific_notes:
  hindi_literature_and_language: Hindi literature is a core board subject with specific
    canonical texts. MILU includes Arts & Humanities (with sub-subjects including
    'Literature and Linguistics' and 'Arts and Culture' per GitHub — [WEB-12])
    but sources from competitive exams; the gap between school-literature and administrative-GK
    framings of the same authors is a validity concern. [NOT FOUND — no published
    evidence resolves whether MILU Hindi literature items use school-board or competitive-exam
    register]
  history_and_civics: Regional North Indian history and state-specific civics (UP
    Panchayati Raj structure, state legislature, local administrative geography) may
    be under-represented in pan-India competitive exam sourcing. [NOT FOUND — no sub-national
    state-wise coverage breakdown is publicly available for MILU Hindi items]
  science_and_maths_in_hindi: Scientific terminology in Hindi varies between standardised
    (Vaigyaanik evam Takniki Shabdavali Aayog terms) and anglicised forms; state boards
    differ in which conventions they follow. Translation quality for MILU's GPT-4O-translated
    science items in Hindi is unvalidated. [NOT FOUND — no published validation of
    Hindi-register adequacy for MILU's translated science items found in any source]
  general_knowledge_competitive_exam_alignment: The deployment user confirmed that
    competitive-exam answer keys are broadly compatible with North Indian teacher
    and board norms; this reduces but does not eliminate the risk of framing mismatches
    in culturally specific items.
  annotator_demographics: 'MILU annotators are drawn from AI4Bharat (IIT Madras) volunteers
    and online exam portal subject experts; no documented representation of Hindi-medium
    North Indian educational backgrounds. Demographic details not published. [NOT
    FOUND — no published MILU source provides annotator demographic details or inter-annotator
    agreement statistics; the institutional base (IIT Madras + IBM Research India)
    is confirmed but does not guarantee Hindi-medium North Indian educational representation.
    Source: NAACL 2025 paper — [WEB-10]]'
regulatory_and_institutional_context:
  primary_education_regulator: Ministry of Education, Government of India (central);
    State Education Departments (UP, MP, Rajasthan, Bihar) for state board matters
  state_board_authorities:
    UP: Uttar Pradesh Madhyamik Shiksha Parishad (UPMSP), Prayagraj
    MP: Madhya Pradesh Board of Secondary Education (MPBSE), Bhopal
    Rajasthan: Board of Secondary Education Rajasthan (RBSE), Ajmer
    Bihar: Bihar School Examination Board (BSEB), Patna
  applicable_data_protection_framework: 'The Digital Personal Data Protection Act,
    2023 (DPDPA) was enacted on 11 August 2023. The DPDP Rules 2025 were notified
    by MeitY on 13 November 2025, operationalising the Act in a phased manner with
    full compliance expected by May 2027. The DPDPA applies to all processing of digital
    personal data within India (collected online or offline-then-digitised) and to
    foreign entities offering goods/services to Indian data principals. LLM-powered
    edtech tools that process teacher or student data (e.g., MCQ response records,
    scoring logs) are subject to the Act''s consent, data minimisation, and purpose-limitation
    requirements. Until the core operational provisions are fully effective, the IT
    Act 2000 and IT (SPDI) Rules 2011 continue to govern. No specific DPDPA exemption
    for edtech AI tools has been notified as of April 2026. Source: MeitY official
    text — [WEB-13];
    Hogan Lovells analysis — [WEB-14];
    DLA Piper — [WEB-15]; FPF AI analysis
    — [WEB-16]'
  ai_in_education_policy: NEP 2020 explicitly mandates technology integration in curriculum
    and teacher training and envisions AI, machine learning, and adaptive learning
    tools to enhance teaching and learning (Ministry of Education — [WEB-17]).
    DIKSHA (Digital Infrastructure for Knowledge Sharing) is the central government's
    national digital platform for teachers and students, hosting content in 35+ languages
    with 120 million+ learners and 2.5 million teachers; over 63 lakh teachers have
    completed NISHTHA training via DIKSHA (roombr.com — [WEB-6]).
    As of 2025, no specific UGC, NCTE, or MoE guidelines on LLM-powered assessment
    tools have been published; sector-level calls for such guidelines have been made
    but not fulfilled (educationforallinindia.com — [WEB-18]).
    DPDPA 2023 compliance is explicitly required for all edtech AI products processing
    school data (same source). The National Educational Technology Forum (NETF) exists
    under NEP 2020 but has not yet issued LLM-specific guidance.
  teacher_qualification_standards: '[NEEDS VERIFICATION — deferred: below search budget;
    NCTE norms for PGT/TGT/lecturer qualification (typically MA + B.Ed. for secondary;
    MA for degree college) are established but not verified this pass against current
    NCTE regulations]'
flagged_gaps_for_web_search:
- gap_id: 1
  label: Hindi state-board syllabus coverage vs. competitive-exam framing in MILU
  description: MILU sources from competitive exams rather than school/university board
    syllabi. Downstream search should verify whether MILU Hindi items cover board-level
    curricular content (UP, MP, Rajasthan, Bihar, CBSE Hindi-medium) or skew toward
    entrance/civil-service exam registers.
  search_target: MILU benchmark Hindi language items UP board MP board CBSE school
    syllabus coverage comparison
  search_outcome: NOT FOUND — no published source provides a comparison between MILU
    Hindi items and state-board syllabi. MILU's own documentation confirms sourcing
    exclusively from competitive exams (1,500+ national/state-level exams). The gap
    is structurally confirmed but not quantified.
- gap_id: 2
  label: Intra-Hindi register variation (Khari Boli vs. state-board dialect norms)
  description: MILU does not document intra-Hindi register standardisation. Search
    should check whether MILU Hindi items use a uniform pan-India formal register
    that may disadvantage state-board-aligned content in UP, Bihar, or Rajasthan.
  search_target: Hindi MCQ benchmark register variation Khari Boli dialect UP Bihar
    Rajasthan state board academic language norms
  search_outcome: NOT FOUND — no published source addresses intra-Hindi register standardisation
    in MILU. This is a full gap confirmed by absence of documentation.
- gap_id: 3
  label: Translated English-board content and Hindi-register validation
  description: ~25% of MILU items were GPT-4O translated from English; translation
    adequacy for North Indian academic Hindi register and subject-specific terminology
    is unvalidated.
  search_target: Hindi MCQ benchmark translated English CBSE ICSE content validation
    North India academic register terminology
  search_outcome: NOT FOUND — no published validation of MILU's GPT-4O-translated
    Hindi items found. The 25% translation rate is confirmed as a dataset-wide figure
    (arXiv 2411.02538 — [WEB-11]); the Hindi-specific
    proportion is unknown.
- gap_id: 4
  label: Sub-national state-level exam source distribution for Hindi items
  description: MILU does not publish a state-wise breakdown of Hindi-language item
    sources. Search should determine whether UP, MP, Rajasthan, and Bihar state-level
    exams are proportionally represented.
  search_target: MILU Hindi benchmark state-wise exam source distribution UP Bihar
    Rajasthan Madhya Pradesh coverage breakdown
  search_outcome: NOT FOUND — no publicly accessible source publishes a state-wise
    breakdown of Hindi-language item sources in MILU. The gated HuggingFace dataset
    has a Hindi subdirectory but no per-state source metadata is exposed. The gap
    remains unresolved.
- gap_id: 5
  label: Canonical Hindi literary and historical content framing in MILU
  description: MILU includes Arts & Humanities but from competitive exams. Search
    should determine whether Tulsidas, Premchand, Kabir, and regional medieval history
    appear in school-literature or administrative-GK framings.
  search_target: MILU Arts Humanities Hindi literature questions Tulsidas Premchand
    Kabir school board competitive exam framing
  search_outcome: NOT FOUND — subject categories confirmed as including 'Literature
    and Linguistics' and 'Arts and Culture' (GitHub — [WEB-12])
    but no item-level framing detail is publicly accessible. Dataset is gated.
- gap_id: 6
  label: Annotator demographics for Hindi items
  description: MILU does not publish annotator demographics. Search should determine
    whether any Hindi-medium North Indian educators were involved in annotation or
    audit of Hindi-language items.
  search_target: MILU benchmark annotation demographics Hindi medium annotators North
    India inter-annotator agreement
  search_outcome: NOT FOUND — no published MILU source provides annotator demographic
    details or inter-annotator agreement statistics. The institutional affiliation
    (IIT Madras + IBM Research India, Chennai/Bangalore) does not guarantee Hindi-medium
    North Indian educational representation.
- gap_id: 7
  label: Mobile internet and device infrastructure for North Indian teacher cohort
  description: Deployment is mobile/enterprise; infrastructure adequacy for the postgraduate
    teacher cohort in UP, MP, Rajasthan, Bihar needs verification.
  search_target: smartphone internet penetration teachers North India UP Bihar Rajasthan
    MP rural urban 2023 2024
  search_outcome: PARTIALLY RESOLVED — state-level internet penetration figures for
    Bihar (43%) and UP (46%) obtained from IAMAI/Kantar ICUBE 2024 (general population).
    Rural school computer lab availability (22%) and rural school internet access
    (18%) from UDISE+ 2023. Teacher-cohort-specific device-tier and connectivity data
    remain unresolved. See infrastructure_notes field for detail.
- gap_id: 8
  label: DPDPA and AI-in-education regulatory applicability
  description: The Digital Personal Data Protection Act 2023 and any state or UGC/NCTE
    guidelines on AI-assisted assessment tools may apply to this deployment.
  search_target: India DPDPA 2023 AI education assessment tool LLM teacher school
    regulation UGC NCTE NEP 2020
  search_outcome: RESOLVED — DPDPA 2023 enacted 11 August 2023; DPDP Rules 2025 notified
    13 November 2025; phased compliance required by May 2027. Applies to all digital
    personal data processing including edtech AI tools. No specific LLM-assessment
    guidelines from UGC/NCTE/MoE as of April 2026; NEP 2020 mandates AI integration
    in education broadly but without LLM-specific assessment guidelines. See regulatory_and_institutional_context
    field.
net_new_fields:
  milu_publication_status: 'MILU was published as a long paper at NAACL 2025 (Albuquerque,
    April 2025), confirming peer-reviewed status. The arXiv preprint (2411.02538)
    has three versions, with the final version dated 4 February 2025. The dataset
    is gated on HuggingFace requiring access request approval, which limits independent
    validation of Hindi-specific item statistics. Source: ACL Anthology — [WEB-10];
    arXiv — [WEB-11]'
  milu_total_question_count_discrepancy: 'MILU''s total question count varies across
    sources: the paper states ~79,000 released (capped at 500 per subject-language
    pair); the HuggingFace README and GitHub README state ~80,000 and ~85,000 respectively;
    the GitHub repository (most recently updated) cites ~85,000. The discrepancy likely
    reflects post-publication dataset updates. This matters because the Hindi-specific
    item count cannot be reliably inferred without accessing Table 9 in the full paper.
    Source: HuggingFace — [WEB-9]; GitHub
    — [WEB-12]'
  diksha_platform_relevance: 'DIKSHA (Digital Infrastructure for Knowledge Sharing)
    is India''s national edtech platform for teachers, mobile-friendly and multilingual
    (35+ languages including Hindi), used by 2.5 million teachers and 120 million
    learners K-12. NEP 2020 mandates digital pedagogy through DIKSHA. Any LLM-powered
    MCQ evaluation tool deployed to North Indian teachers will likely need to be compatible
    with or positioned alongside DIKSHA workflows; integration with DIKSHA''s NDEAR
    architecture (open APIs, interoperable) is technically feasible but not documented
    for LLM inference tools as of 2025. Source: Ministry of Education — [WEB-6];
    ORF — [WEB-7]'
  bihar_language_register_note: Bihar's official language is Hindi, but the majority
    of Bihar's population speaks Bhojpuri (24.86%), Maithili (12.55%), or Magahi (10.87%)
    as native languages, with standard Hindi spoken natively by only 25.54% of the
    population (Wikipedia/Census data — [WEB-19]).
    This is relevant because postgraduate-educated Hindi-medium teachers in Bihar
    may have stronger exposure to Bihari varieties than to pan-India Khari Boli, potentially
    amplifying register mismatch risks for MILU's formal Hindi items in this sub-population.
  milu_related_indic_benchmarks: 'MILU is not the only Indic-language LLM benchmark;
    related benchmarks include INDICGLUE (2020), INDICXTREME (2023), INDICGENBENCH
    (2024), INDICQA (2024), and SANSKRITI-BENCH. A recent PARAM-1 model paper (2025)
    explicitly cites MILU as a reference benchmark and notes that India''s linguistic
    diversity (20+ official languages, 100+ dialects, code-switching, diglossia) is
    structurally under-represented in existing evaluations. No benchmark specifically
    targets Hindi-medium North Indian school/board curriculum MCQs as distinct from
    competitive-exam MCQs. Source: ResearchGate/PARAM-1 — [WEB-20];
    aidigitalnews.com — [WEB-21]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://negativemarkingcalculator.in/ |
| WEB-2 | https://testbook.com/upsc-civil-services/negative-marking-in-upsc |
| WEB-3 | https://pwonlyias.com/negative-marking-in-upsc-exam/ |
| WEB-4 | https://www.iamai.in/sites/default/files/research/Kantar_%20IAMAI%20report_2024_.pdf |
| WEB-5 | https://www.amulyacharan.com/2024/12/17/the-digital-divide-in-education-bridging-the-urban-rural-gap/ |
| WEB-6 | https://www.roombr.com/blog/digital-classroom-govt-initiatives-india |
| WEB-7 | https://www.orfonline.org/expert-speak/five-years-of-nep-2020-and-the-promise-of-edtech |
| WEB-8 | https://www.grabon.in/indulge/tech/internet-users-statistics/ |
| WEB-9 | https://huggingface.co/datasets/ai4bharat/MILU |
| WEB-10 | https://aclanthology.org/2025.naacl-long.507/ |
| WEB-11 | https://arxiv.org/abs/2411.02538 |
| WEB-12 | https://github.com/AI4Bharat/MILU |
| WEB-13 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-14 | https://www.hoganlovells.com/en/publications/indias-digital-personal-data-protection-act-2023-brought-into-force- |
| WEB-15 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-16 | https://fpf.org/blog/five-ways-in-which-the-dpdpa-could-shape-the-development-of-ai-in-india/ |
| WEB-17 | https://www.education.gov.in/en/nep/coe-ai-education |
| WEB-18 | https://educationforallinindia.com/artificial-intelligence-in-indian-school-education-use-misuse-and-preventive-measures/ |
| WEB-19 | https://en.wikipedia.org/wiki/Bihar |
| WEB-20 | https://www.researchgate.net/publication/392504733_MILU_A_Multi-task_Indic_Language_Understanding_Benchmark |
| WEB-21 | https://aidigitalnews.com/ai/ai4bharat-and-ibm-research-india-release-new-indic-language-llm-benchmark/ |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Does the assessment context involve open-ended/long-form student answers, structured short answers, or primarily factual single-item MCQ questions?
A1: The deployment involves only MCQs with a single correct answer. Scoring is binary in effect: positive marks for correct selections and negative marks for incorrect ones. No partial credit or rubric-based judgment is required.

Q2 [OO]: Should the AI support graded scoring, binary correct/incorrect judgments, or qualitative rubric-based feedback, and in what Hindi register should scoring rationale be expressed?
A2: Because all questions are MCQ-type with a single correct answer, scoring is straightforwardly binary. Graded or rubric-based output is not needed for this deployment.

Q3 [IC]: Does the deployment target a specific board/institution type, or must the AI handle content across multiple curricula, including culturally specific canonical texts and regional reference points?
A3: The deployment must accommodate all Hindi state and central board syllabi. Questions may also be drawn from English-medium boards, provided they are translated into Hindi and aligned in style with Hindi-board norms. Regional and curriculum-specific content (e.g., Tulsidas, Premchand, regional historical figures) should therefore be in scope.

Q4 [OC]: Are student answers and teacher mark schemes in North India likely to reflect norms that diverge from national competitive-exam keyed answers, such that a regionally specific correct answer might differ from a pan-India standard answer?
A4: No significant divergence is expected. Evaluation schemas across boards and states are described as broadly similar, so competitive-exam-sourced answer keys are considered largely compatible with what North Indian teachers would accept as correct.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | MILU's MCQ format from regional/national competitive exams aligns well with the deployment's strict MCQ requirement, but the benchmark must cover the breadth of Hindi state and central board syllabi (not just competitive-exam domains), leaving a potential gap in curricular coverage. |
| IC | HIGH | The deployment spans all Hindi state and central board syllabi, including culturally loaded content (canonical Hindi literature, regional history, local governance) that may be framed differently in competitive-exam-sourced items than in school or university board contexts; translated English-board content adds further surface-level risk. |
| IF | LOWER | Both benchmark and deployment are text-only in Hindi with Devanagari script, a high-resource language-script pairing; no modality mismatch exists. |
| OO | LOWER | Output is binary correct/incorrect label matching, co-designed for the same India-centric MCQ format; no culturally variable scoring taxonomy is involved. |
| OC | LOWER | The user confirms that evaluation schemas are broadly consistent across North Indian boards and competitive-exam settings, and MILU was designed by the target population (India); annotator-population mismatch is therefore low. |
| OF | LOWER | Benchmark output is a label/answer key and deployment requires the same binary scoring signal; output form is fully aligned. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Hindi config)
**Analysis date:** 2025-01-30
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | MILU/Hindi | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" | DC series motor no-load speed — translated Engineering item | IC, IF |
| D2 | MILU/Hindi | 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? 44वें संविधान संशोधन अधिनियम द्वारा" | Constitutional amendment — Law & Governance item | IO, IC |
| D3 | MILU/Hindi | 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" | William Wordsworth's nationality — translated Arts/Literature item, non-Indian literary content | IC |
| D4 | MILU/Hindi | 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" | Hindi indirect speech conversion — Language Studies item | IC, IF |
| D5 | MILU/Hindi | 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" | Mughal text authorship — History item with India-specific content | IO, IC |
| D6 | MILU/Hindi | 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? अभ्रक" | UP-specific minerals question — North Indian regional geography | IC, IO |
| D7 | MILU/Hindi | 28 | option2 | "निम्नलिखित में से कौन खेरवार आंदोलन के नेता थे? भागीरथ मांझी" | Kherwar movement leader — regional tribal history | IC |
| D8 | MILU/Hindi | 32 | option4 | "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया। इल्तुतमिश" | Completion of Qutub Minar — medieval Indian history | IO, IC |
| D9 | MILU/Hindi | 48 | option3 | "भांड पाथेर थिएटर मुख्य रूप से भारत के निम्नलिखित में से किस राज्य/केंद्र शासित प्रदेश की परंपरा है? जम्मू और कश्मीर" | Bhand Pather theatre tradition — regional Indian arts | IC |
| D10 | MILU/Hindi | 52 | option2 | "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था, वह था सुंदर पांड्यन" | Pandya kingdom history — South Indian dynastic history, not North India | IC |
| D11 | MILU/Hindi | 54 | option3 | "भारत की पहली टेक्नीकलर फिल्म कौन सी है? झांसी की रानी" | First Technicolor Indian film — India GK, Rani Lakshmibai connection | IC |
| D12 | MILU/Hindi | 57 | option4 | "किस राज्य सरकार ने राज्य भर में इलेक्ट्रॉनिक सिगरेट के निर्माण और बिक्री-खरीद पर पूर्ण प्रतिबंध लगाया है? बिहार" | Bihar e-cigarette ban — North Indian state-level policy | IC |
| D13 | MILU/Hindi | 64 | option3 | "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है? सरदार वल्लभभाई पटेल" | Iron Man of India — national GK, competitive exam style | IO, IC |
| D14 | MILU/Hindi | 65 | option4 | "झारखंड की उप राजधानी क्या है? दुमका" | Jharkhand sub-capital — regional Indian geography | IC |
| D15 | MILU/Hindi | 68 | option2 | "निम्नलिखित में से राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है? बीकानेर" | Rajasthan reserved area — North Indian state-specific geography | IC |
| D16 | MILU/Hindi | 76 | option2 | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है? नैतिक पाठ पढ़ाना" | Meaning of English word 'didactic' asked in Hindi — English vocabulary test | IC |
| D17 | MILU/Hindi | 83 | option1 | "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है" | Civil officer ethics scenario — UPSC/civil services ethics framing | IO, IC |
| D18 | MILU/Hindi | 90 | option3 | "शब्द 'grim' का पर्यायवाची लिखें। भयानक" | Synonym of English word 'grim' asked in Hindi | IC |
| D19 | MILU/Hindi | 93 | option2 | "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है? पंचायत समिति" | Three-tier Panchayati Raj — civics, relevant to North Indian governance | IC, IO |
| D20 | MILU/Hindi | 97 | option3 | "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है। का" | Hindi postposition fill-in — language/grammar item | IC, IF |
| D21 | MILU/Hindi | 98 | option1 | "किस प्रसिद्ध कश्मीरी कवि को आमतौर पर 'कश्मीर का जॉन कीट्स' कहा जाता है? रसूल मीर" | Kashmiri poet comparison to John Keats — regional literature | IC |
| D22 | MILU/Hindi | 105 | option4 | "निर्देश: निम्नलिखित प्रश्न में...Evangelize [का अर्थ] उपदेश देना" | English vocabulary 'Evangelize' — meaning tested in Hindi | IC |
| D23 | MILU/Hindi | 108 | option3 | "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए? सी. सुब्रह्मण्य भारती" | First cartoons in Tamil magazine — South Indian literary history | IC |
| D24 | MILU/Hindi | 115 | option4 | "निम्नलिखित लेखकों में से किसने लघु कथाओं के संग्रह 'किस्सा किस्सा लखनऊवा' के लिए साहित्य अकादमी युवा पुरस्कार 2021 जीता? हिमांशु वाजपेयी" | Sahitya Akademi award for Lucknow-themed stories — North Indian literary content | IC |
| D25 | MILU/Hindi | 130 | option4 | "2019 का मैन बुकर पुरस्कार फिक्शन के लिए जीतने वाली पहली अश्वेत महिला कौन बनी हैं? बर्नाडिन एवरिस्टो" | Man Booker Prize winner — international literary GK | IC |
| D26 | MILU/Hindi | 156 | option1 | "2011 की जनगणना के अनुसार राजस्थान की कुल साक्षरता का लगभग प्रतिशत कितना है? 66.11%" | Rajasthan literacy rate — North Indian state statistics | IC |
| D27 | MILU/Hindi | 182 | option1 | "निम्नलिखित में से किस राज्य ने 2011 - 12 में सबसे अधिक दूध उत्पादन दर्ज किया? उत्तर प्रदेश" | Milk production by state — UP-relevant agricultural GK | IC |
| D28 | MILU/Hindi | 190 | option2 | "राजस्थान का आकार है- समचतुर्भुज" | Rajasthan's shape — state-specific geography | IC |
| D29 | MILU/Hindi | 193 | option3 | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है? महाराव उम्मेद सिंह I" | Kota painting school — Rajasthan regional arts | IC |
| D30 | MILU/Hindi | 198 | option2 | "छत्तीसगढ़ के निम्नलिखित विद्रोहों में से किसे 'बस्तर का स्वतंत्रता संग्राम' भी कहा जाता है? लिंगागिरी विद्रोह" | Chhattisgarh tribal revolt — Central Indian regional history | IC |
| D31 | MILU/Hindi | 211 | option3 | "राजस्थान सरकार ने मौसमी और गैर-संचारी रोगों की निगरानी के लिए...कौन सा सॉफ्टवेयर लॉन्च किया है? निदान" | Rajasthan state health software — state-level policy GK | IC |
| D32 | MILU/Hindi | 213 | option1 | "राजतरंगिणी के लेखक कौन हैं? कल्हण" | Rajatarangini author — classical Sanskrit text, competitive-exam GK | IC |
| D33 | MILU/Hindi | 232 | option2 | "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है? इलंगो अडिगल" | Tamil epic Silappatikaram — South Indian literary history | IC |
| D34 | MILU/Hindi | 242 | option4 | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है...चिकनकारी" | UP handicraft Chikankari — North Indian craft, directly relevant | IC, IO |
| D35 | MILU/Hindi | All 245 | — | All 245 examples have `is_translated: True` | Every sampled item is marked as translated from English | IC, IF |
| D36 | MILU/Hindi | 36 | option3 | "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है। TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______." | Letter series with English alphabet labels — Logical Reasoning item | IC, IF |
| D37 | MILU/Hindi | 56 | option2 | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें...केवल (1) और (3)" | Reference to numbered statements not present in the question field — truncated/incomplete item | IC, IF |
| D38 | MILU/Hindi | 69 | option2 | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल" | Options reference (a),(b),(c),(d) labels absent from question stem — truncated item | IC, IF |
| D39 | MILU/Hindi | 86 | option2 | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" | Options reference A,B,C,D,E state labels not named in the question — truncated item | IC, IF |
| D40 | MILU/Hindi | 95 | option1 | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। AEDBCF" | Sentence ordering question where actual sentences B,C,D,E are missing | IC, IF |
| D41 | MILU/Hindi | 106 | option2 | "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" | Ordering question where the numbered substances are not listed | IC, IF |
| D42 | MILU/Hindi | 188 | option3 | "नई शिक्षा नीति 2020 में देखा गया है...निम्नलिखित में से किन समस्याओं का सामना कर रही है? उपरोक्त सभी" | Sub-items (a),(b) not listed in question stem — truncated | IC, IF |
| D43 | MILU/Hindi | 118 | option2 | "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें। अपने काम को बेहतर तरीके से व्यवस्थित करना" | Idiom question with no idiom in the stem — missing content | IC, IF |
| D44 | MILU/Hindi | 151 | option1 | "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं। केवल तर्क I मजबूत है" | Statement and arguments not present in question field — truncated item | IC, IF |
| D45 | MILU/Hindi | 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" | FORTRAN 77 programming — highly specialized computing, unlikely in state board | IO |
| D46 | MILU/Hindi | 104 | option4 | "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" | AM receiver intermediate frequency — specialized electronics | IO |
| D47 | MILU/Hindi | 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" | Archery Asia Cup 2022 results — current affairs, time-sensitive | IC |
| D48 | MILU/Hindi | 34 | option1 | "किस कानून के तहत, विधायिका के सदस्य बजट की आलोचना नहीं कर सकते थे? भारतीय परिषद अधिनियम-1892" | Colonial Indian Council Act — constitutional/legal history | IO, IC |
| D49 | MILU/Hindi | 135 | option3 | "पंचायतों के संबंध में निम्नलिखित में से कौन सा/से सही है/हैं?...नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें:" | Option4 of the MCQ is an instruction ("use the code below"), not an answer — malformed item | OO |
| D50 | MILU/Hindi | 10 | option4 | "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" | Blue Baby Syndrome cause — Health/Medicine competitive-exam item | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Devanagari Hindi script with standard formal register throughout
- **Dimension(s):** IF, IC
- **Observation:** All 245 sampled items are rendered in standard Devanagari Unicode Hindi with a formal, pan-India Khari Boli register appropriate for competitive examinations and board-level assessments. Vocabulary is standard Sanskrit-derived academic Hindi (e.g., "संवैधानिक संशोधन", "पंचायती राज प्रणाली", "सहजीवी संबंध"). No script inconsistencies, romanisation, or Perso-Arabic loanword conflicts were observed.
- **Deployment relevance:** The deployment requires Devanagari script text-only interaction. The consistent formal Hindi register matches what North Indian board teachers and students encounter in official examination materials.
- **Datapoint citations:**
  - [D4] Example 9 (MILU/Hindi, validation, option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — Standard formal Hindi grammatical question, consistent with board-level language items.
  - [D20] Example 97 (MILU/Hindi, validation, option3): "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है। का" — Hindi postposition fill-in, academic register.

#### Strength 2: Strong MCQ structural alignment with deployment format
- **Dimension(s):** IO, OO
- **Observation:** All 245 sampled items are 4-option single-correct-answer MCQs with a single `target` field containing the correct option label. The binary correct/incorrect evaluation schema is structurally identical to the deployment's positive/negative marking requirement. No multi-select, open-ended, or partial-credit items appear in the sample.
- **Deployment relevance:** The deployment requires strict MCQ format with single correct answers and binary scoring. MILU's format is a precise match, reducing any format-translation burden.
- **Datapoint citations:**
  - [D2] Example 6 (MILU/Hindi, validation, option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — Classic 4-option MCQ, single correct answer.
  - [D13] Example 64 (MILU/Hindi, validation, option3): "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है?" — Standard GK MCQ format.

#### Strength 3: Meaningful coverage of India-centric Law & Governance and Civics content
- **Dimension(s):** IO, IC
- **Observation:** Multiple items address Indian constitutional law (constitutional amendments, writs, parliamentary procedure), Panchayati Raj (three-tier system, gram sabha), and India-specific legal provisions (SC/ST Prevention of Atrocities Act, Sati Prevention Act). These subjects align directly with the civics and political science portions of North Indian board syllabi.
- **Deployment relevance:** North Indian state board syllabi (UP, MP, Rajasthan, Bihar) prominently include Indian polity and constitutional studies. Items on Panchayati Raj (Example 93), constitutional writs (Example 33), and constitutional amendments (Example 6, 39, 136) are directly deployable against board-level student assessments.
- **Datapoint citations:**
  - [D19] Example 93 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है? पंचायत समिति" — Panchayati Raj content directly relevant to North Indian civics syllabi.
  - [D2] Example 6 (MILU/Hindi, validation, option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? 44वें संविधान संशोधन अधिनियम द्वारा" — Constitutional amendment knowledge.
  - [D48] Example 34 (MILU/Hindi, validation, option1): "किस कानून के तहत, विधायिका के सदस्य बजट की आलोचना नहीं कर सकते थे? भारतीय परिषद अधिनियम-1892" — Indian legislative history.

#### Strength 4: Meaningful presence of North Indian state-specific geographical and cultural content
- **Dimension(s):** IC
- **Observation:** Several items in the sample are directly anchored to North Indian states: UP minerals (Example 26), Rajasthan's district geography (Example 68, 190), Rajasthan literacy statistics (Example 156), UP milk production (Example 182), Rajasthan health policy (Example 211), and UP's Chikankari craft (Example 242). This confirms that MILU's region-specific exam sourcing does include some Hindi-belt state content.
- **Deployment relevance:** The deployment population of North Indian teachers needs to evaluate students on state-board content about their own states. These items demonstrate that MILU is not exclusively pan-India competitive content.
- **Datapoint citations:**
  - [D6] Example 26 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? अभ्रक" — UP-specific geography question.
  - [D15] Example 68 (MILU/Hindi, validation, option2): "निम्नलिखित में से राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है? बीकानेर" — Rajasthan district-level geography.
  - [D34] Example 242 (MILU/Hindi, validation, option4): "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है...चिकनकारी" — UP handicraft, directly North Indian cultural content.
  - [D28] Example 190 (MILU/Hindi, validation, option2): "राजस्थान का आकार है- समचतुर्भुज" — Rajasthan-specific geographic question.

#### Strength 5: Coverage of Indian medieval and modern history in Hindi
- **Dimension(s):** IO, IC
- **Observation:** History items cover Mughal-era texts (Example 25), medieval construction history (Example 32), Indian freedom movement framing (Example 64, 235), ancient Indian history (Example 158, 237), and colonial-era governance (Example 50, 96). These are standard components of North Indian board history syllabi.
- **Deployment relevance:** History is a core subject in all Hindi state board syllabi. Items on Ashoka (Example 158), the Qutub Minar (Example 32), the Iron Man of India (Example 64), and Harappan cities (Example 237) align with topics examined at secondary level in UP, MP, Rajasthan, and Bihar boards.
- **Datapoint citations:**
  - [D8] Example 32 (MILU/Hindi, validation, option4): "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया। इल्तुतमिश" — Medieval Indian history.
  - [D5] Example 25 (MILU/Hindi, validation, option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" — Mughal historiography.

#### Strength 6: Hindi language and grammar items present in Language Studies subject
- **Dimension(s):** IC, IO
- **Observation:** The sample includes Hindi grammatical exercises covering active/passive voice conversion (Example 51, 91), indirect speech (Example 9), postposition usage (Example 97), and fill-in-the-blank sentence completion (Example 152). These are directly aligned with Hindi language instruction at board level.
- **Deployment relevance:** Hindi Language and Literature is a compulsory subject in all North Indian board curricula. Grammar items on voice, indirect speech, and postpositions are standard components of Class 10–12 Hindi papers.
- **Datapoint citations:**
  - [D4] Example 9 (MILU/Hindi, validation, option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — Indirect speech (reported speech) conversion.
  - [D20] Example 97 (MILU/Hindi, validation, option3): "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है। का" — Hindi postposition fill-in.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: 100% of sampled validation items are marked `is_translated: True`
- **Dimension(s):** IC, IF
- **Observation:** All 245 sampled examples from the Hindi validation split carry `is_translated: True`. The benchmark documentation states that only ~25% of total questions across all 11 languages were translated from English; if Hindi's validation split is entirely composed of translated items, this would substantially exceed the reported dataset-wide average. Even if this is an artifact of the validation split (vs. the test split), an evaluator relying on the validation split for few-shot examples would be drawing exclusively from translated content.
- **Deployment relevance:** Translated items may not reflect the natural Hindi academic register used in North Indian board assessments. GPT-4O translations may produce grammatically correct but register-misaligned Hindi — particularly for subject-specific terminology (science, economics, civics) — that diverges from what UP, MP, Rajasthan, or Bihar board students and teachers would encounter. This is the single highest-risk finding in the sample.
- **Datapoint citations:**
  - [D35] All 245 examples: `is_translated: True` on every record — every item in the validation split is a translation.
  - [D1] Example 1 (MILU/Hindi, validation, option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" — Translated engineering item; technical Hindi vocabulary (e.g., "डीसी सीरीज मोटर") may follow English-derived transliteration rather than standardised Hindi scientific terminology.
  - [D3] Example 7 (MILU/Hindi, validation, option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" — Translated item on a British poet, clearly sourced from English.

---

#### MAJOR

#### MAJOR Concern 1: Numerous items with truncated or missing question stems rendering them unevaluable
- **Dimension(s):** IC, IF
- **Observation:** At least 7–8 items in the 245-item sample have options that reference content (numbered statements, lettered sub-items, named sentences) that is absent from the `question` field. This indicates that the original question included a table, passage, or list that was stripped during scraping, leaving the MCQ shell unanswerable without the missing context.
- **Deployment relevance:** If a deployed LLM encounters these items, it cannot evaluate the question correctly — neither can a teacher using the benchmark for reference. These items inflate measurement error and cannot serve their intended evaluative function.
- **Datapoint citations:**
  - [D37] Example 56 (MILU/Hindi, validation, option2): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें...केवल (1) और (3)" — Four statements referenced but absent from question stem.
  - [D38] Example 69 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल" — Options reference (a),(b),(c),(d) items absent from question.
  - [D39] Example 86 (MILU/Hindi, validation, option2): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" — State labels A–E not identified in the question.
  - [D40] Example 95 (MILU/Hindi, validation, option1): "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। AEDBCF" — The actual sentences are missing.
  - [D41] Example 106 (MILU/Hindi, validation, option2): "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" — Numbered substances not listed.
  - [D43] Example 118 (MILU/Hindi, validation, option2): "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें। अपने काम को बेहतर तरीके से व्यवस्थित करना" — The idiom itself is absent from the question field.
  - [D44] Example 151 (MILU/Hindi, validation, option1): "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं। केवल तर्क I मजबूत है" — Statement and arguments missing from stem.
  - [D42] Example 188 (MILU/Hindi, validation, option3): "नई शिक्षा नीति 2020 में देखा गया है...निम्नलिखित में से किन समस्याओं का सामना कर रही है? उपरोक्त सभी" — Sub-items (a),(b) absent.

#### MAJOR Concern 2: Absence of canonical Hindi literary figures (Tulsidas, Premchand, Kabir, Mahadevi Varma) from the sample
- **Dimension(s):** IC, IO
- **Observation:** No item in the 245-item sample tests knowledge of canonical Hindi-board literary figures — Tulsidas, Premchand, Kabir, Mahadevi Varma, Harivansh Rai Bachchan, or Surdas. The Literature and Linguistics items present are either about: (a) English literary figures (William Wordsworth, Example 7; Man Booker Prize winner, Example 130), (b) South Indian authors (C. Subramania Bharati, Example 108; Silappatikaram, Example 232; Telugu author, Example 126), (c) English vocabulary meanings ('didactic', Example 76; 'grim', Example 90; 'Evangelize', Example 105), or (d) regional/marginal Hindi literary awards (Example 115). While the sample is limited to the validation split and may not reflect test split content, this complete absence is notable.
- **Deployment relevance:** Canonical Hindi literature (Ramcharitmanas, Premchand's Godan, Kabir's dohas) is a required component of every Hindi state board syllabus (UP, MP, Rajasthan, Bihar) at Class 9–12. A benchmark used to evaluate MCQ responses from Hindi-board students that lacks these authors cannot validly assess Hindi literature performance in the deployment context.
- **Datapoint citations:**
  - [D3] Example 7 (MILU/Hindi, validation, option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" — British poet identified instead of Hindi literary canon.
  - [D33] Example 232 (MILU/Hindi, validation, option2): "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है? इलंगो अडिगल" — South Indian Tamil epic, not North Indian Hindi literature.
  - [D22] Example 105 (MILU/Hindi, validation, option4): "निर्देश: निम्नलिखित प्रश्न में...Evangelize [का अर्थ] उपदेश देना" — English vocabulary test embedded in Hindi Language Studies subject.
  - [D16] Example 76 (MILU/Hindi, validation, option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है? नैतिक पाठ पढ़ाना" — English word meaning tested in Hindi Language Studies.

#### MAJOR Concern 3: Competitive-exam framing dominates; minimal school-board syllabus framing visible
- **Dimension(s):** IO, IC
- **Observation:** The vast majority of items in the sample are structured as UPSC/SSC/state civil service GK-style questions — current affairs (Examples 2, 11, 35, 88, 131), government schemes and policies (Examples 82, 102, 122, 148, 239), constitutional/legal facts (Examples 6, 33, 34, 39, 42, 46, 136), and administrative GK (Examples 50, 71, 72, 132, 165). Only a small subset of items (Hindi grammar, some art history, a few biology/chemistry items) resembles the classroom-instruction framing typical of board-level syllabi. Ethics scenario items (Example 83) are explicitly UPSC Civil Services Paper II format.
- **Deployment relevance:** North Indian board teachers assess students on syllabus-aligned content, not current-affairs or civil-service GK. A benchmark skewed toward civil-service exam framing will produce validity estimates that do not reflect whether an LLM can evaluate students on UP Board Class 12 Hindi, History, or Science papers.
- **Datapoint citations:**
  - [D17] Example 83 (MILU/Hindi, validation, option1): "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है..." — Clearly UPSC GS Paper II (Ethics, Integrity and Aptitude) format scenario.
  - [D47] Example 2 (MILU/Hindi, validation, option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — Current affairs sports GK, not a board syllabus topic.
  - [D13] Example 64 (MILU/Hindi, validation, option3): "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है? सरदार वल्लभभाई पटेल" — Standard competitive-exam GK format.

#### MAJOR Concern 4: English-vocabulary questions embedded in Hindi Language Studies subject
- **Dimension(s):** IC, IO
- **Observation:** Multiple items in the Language Studies and Literature and Linguistics subjects test the meaning or synonym of English words, presented in a Hindi instructional frame. Examples include: meaning of 'didactic' (Example 76), synonym of 'grim' (Example 90), meaning of 'Evangelize' (Example 105), and active/passive voice for "क्या आवाज़ ने उसे परेशान किया?" (an English-language structure reframed in Hindi, Example 91). These appear to be translated from English-medium competitive exam language papers.
- **Deployment relevance:** Hindi state board Language Studies papers test Hindi grammar and Hindi literature, not English vocabulary. Items testing synonyms of English words, when labelled as Hindi Language Studies, would produce systematically misleading validity estimates for the deployment — a model that succeeds on these items is being tested on English proficiency, not Hindi Language Studies competence.
- **Datapoint citations:**
  - [D16] Example 76 (MILU/Hindi, validation, option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है? नैतिक पाठ पढ़ाना" — Testing English word meaning within Hindi Language Studies subject.
  - [D18] Example 90 (MILU/Hindi, validation, option3): "शब्द 'grim' का पर्यायवाची लिखें। भयानक" — English synonym tested in Hindi.
  - [D22] Example 105 (MILU/Hindi, validation, option4): "निर्देश: निम्नलिखित प्रश्न में...Evangelize [का अर्थ] उपदेश देना" — English religious term meaning in Hindi Language Studies.

#### MAJOR Concern 5: Malformed answer option — an instruction appearing as an answer choice
- **Dimension(s):** OO, IF
- **Observation:** Example 135 (Panchayats/Politics and Governance) has its fourth option read: "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें:" ("Select the correct answer using the code below:") — a formatting instruction from the original question, not an answer choice. The target is `option3`. This is a scraping artifact where the answer-code table was stripped but the instruction line was retained as an option.
- **Deployment relevance:** If a deployed model encounters this item, it may select option4 (the instruction) as an answer. This is a data quality defect that can corrupt both model evaluation scores and teacher trust in the system.
- **Datapoint citations:**
  - [D49] Example 135 (MILU/Hindi, validation, option3): "पंचायतों के संबंध में...नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें:" — An instruction line masquerading as answer option 4.

---

#### MINOR

#### MINOR Concern 1: Non-North-Indian regional content takes substantial share of Arts & Humanities and History
- **Dimension(s):** IC
- **Observation:** Several Arts & Humanities History and Literature items in the sample concern South Indian history and literature: Pandya kingdom (Example 52), Tamil epic Silappatikaram (Example 232), Tamil magazine cartoons (Example 108), Telugu book authorship (Example 126), Kashmiri poet (Example 98), and Kota painting (Rajasthan, Example 193). While pan-Indian content is appropriate for general competitive exams, it dilutes the North Indian board syllabus alignment for this specific deployment.
- **Deployment relevance:** North Indian board history syllabi emphasise Mughal, Rajput, and North Indian medieval history, and North Indian freedom movement figures. South Indian dynastic history (Pandya, Chola) and Tamil literary history are less emphasized. This is a calibration concern rather than a fundamental misalignment.
- **Datapoint citations:**
  - [D10] Example 52 (MILU/Hindi, validation, option2): "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था, वह था सुंदर पांड्यन" — South Indian Pandya dynasty, not a North Indian board syllabus priority.
  - [D23] Example 108 (MILU/Hindi, validation, option3): "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए? सी. सुब्रह्मण्य भारती" — Tamil literary history.

#### MINOR Concern 2: Time-sensitive current-affairs items create staleness risk
- **Dimension(s):** IC, OC
- **Observation:** Multiple items are tied to specific events from 2018–2022 with exact statistics that become outdated (e.g., India's GDP growth rate in July–September 2018, Example 74; ASSOCHAM president December 2020, Example 123; Minister of WCD in 2018, Example 132; India's first UNDP Youth Climate Champion in January 2022, Example 239). These items have objectively correct answers only at a specific point in time.
- **Deployment relevance:** If teachers use MILU items to create new assessment questions, or if the LLM is evaluated on whether it correctly marks student answers to these current-affairs questions, staleness could cause the system to mark correct historical answers as incorrect if the LLM's training data reflects a different time period.
- **Datapoint citations:**
  - [D47] Example 2 (MILU/Hindi, validation, option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — Time-stamped sports result.
  - Example 132 (MILU/Hindi, validation, option4): "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं? मेनेका गांधी" — Cabinet position tied to a specific year.

#### MINOR Concern 3: Highly specialised Engineering and Tech content unlikely to appear in school-board assessments
- **Dimension(s):** IO
- **Observation:** A substantial number of Engineering & Tech items are highly specialised — FORTRAN 77 programming (Example 8), AM/SSB-SC modulation bandwidth (Example 43, 104), TDM frame rate calculations (Example 47), and timber fibre swelling percentages (Example 12). These are appropriate for polytechnic entrance exams or engineering qualification tests but not for school-board level assessments.
- **Deployment relevance:** The deployment covers all board types including secondary level, where Engineering & Tech content would be introductory at most. The presence of advanced technical content within what is labelled as the Hindi MILU benchmark means the benchmark over-represents post-secondary technical exam difficulty for the school-board teacher deployment.
- **Datapoint citations:**
  - [D45] Example 8 (MILU/Hindi, validation, option1): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" — FORTRAN 77 programming — highly specialised computing, unlikely in any board syllabus.
  - [D46] Example 104 (MILU/Hindi, validation, option4): "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" — AM receiver IF — polytechnic/engineering level.

#### MINOR Concern 4: Logical Reasoning items use English alphabetic sequences
- **Dimension(s):** IC, IF
- **Observation:** Logical Reasoning items in the Science domain use sequences of Latin/English letters (TAB, TTZBB, etc. in Example 36; _q p p_ in Example 44; A, C, F, H, ?, M in Example 124) despite being presented in Hindi. The question wrapper is in Hindi but the reasoning object is English alphanumeric.
- **Deployment relevance:** This is a minor structural concern — Hindi board students are familiar with English alphabetic sequences in reasoning tests, which appear in many competitive exams. However, it does confirm the competitive-exam sourcing of Logical Reasoning items and may introduce a slight English-literacy dependency.
- **Datapoint citations:**
  - [D36] Example 36 (MILU/Hindi, validation, option3): "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है...TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______. TTTTXBBBB" — Latin letter series reasoning.

---

### Content Coverage Summary

The Hindi validation split of MILU (245 items sampled) spans eight domains with notable concentration in Engineering & Tech (approx. 25%), Science (approx. 20%), Environmental Sciences including Geography and Agriculture (approx. 15%), and Arts & Humanities (approx. 20%), with smaller contributions from Business Studies, Law & Governance, Social Sciences, and Health & Medicine. All items are in standard formal Devanagari Hindi. The entire validation sample is marked `is_translated: True`, which is inconsistent with the paper's reported 25% dataset-wide translation rate and represents the most significant data-quality finding from the sample.

Content topics reflect a pan-Indian competitive-exam orientation: UPSC/SSC-style general knowledge, constitutional law, Indian polity, India-centric science GK, and current affairs. India-centric content is genuinely present (North Indian state geography, Panchayati Raj, Chikankari, medieval Indian history), but canonical Hindi board literary figures (Tulsidas, Premchand, Kabir) are entirely absent from the sample, and Hindi Literature and Linguistics items instead test English vocabulary meanings.

Data quality concerns are non-trivial: approximately 3–4% of sampled items have truncated stems where tables, passages, or sub-item lists were lost during scraping, rendering the question unanswerable. One item has a formatting instruction appearing as an answer option.

The register throughout is uniform formal Hindi — appropriate for the deployment — but the framing is overwhelmingly competitive-exam (UPSC/SSC/state civil service) rather than school/university board syllabus instruction.

---

### Limitations

1. **Validation split only:** All 245 examples are from the validation split (812 total items). The test split contains 14,831 Hindi items. The `is_translated: True` finding on all validation items may not generalise to the test split, which likely contains a higher proportion of natively sourced Hindi questions. The canonical Hindi literature absence, truncation defects, and competitive-exam framing findings should be verified against a sample of the test split before drawing strong conclusions.

2. **Sample size relative to total:** 245 items out of 15,643 total Hindi items (~1.6%) limits subject-level inferences. Subjects like Hindi Literature specifically may have more board-aligned items in the test split that did not appear in this sample.

3. **Subject distribution not controllable:** The sample was drawn from the validation split as provided; subject distribution within the sample may over- or under-represent specific subjects relative to the full test split.

4. **Translation quality not auditable from text alone:** While register concerns about GPT-4O translations can be flagged, assessing whether specific technical translations (electronics, chemistry, economics) use the correct Hindi-board terminology (Vaigyaanik evam Takniki Shabdavali Aayog standard terms vs. transliterated English) requires domain-expert review beyond what can be determined from reading the items.

5. **Annotator demographics unverifiable:** The demographic backgrounds of item annotators and the exam-source distribution for Hindi items cannot be determined from the dataset content alone, as this metadata is not exposed in the HuggingFace schema.

6. **Test split gating:** The test split is available via gated access on HuggingFace (auto-gated), meaning independent validation of subject distribution and translation rates for the full Hindi test set requires dataset access approval.

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
  "region": "North Indian Hindi-Medium Postgraduate Teacher — MCQ Evaluation Deployment",
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
