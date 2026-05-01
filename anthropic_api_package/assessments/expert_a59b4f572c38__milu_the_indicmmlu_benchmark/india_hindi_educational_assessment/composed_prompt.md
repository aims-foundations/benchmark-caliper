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

**Dataset(s):** ai4bharat/MILU
**Analysis date:** 2025-01-31
**Examples reviewed:** 215 total across 11 language configs (Bengali: 21, English: 20, Gujarati: 24, Hindi: 26, Kannada: 17, Malayalam: 16, Marathi: 21, Odia: 21, Punjabi: 25, Tamil: 19, Telugu: 25); primary focus on Hindi config (26 examples)
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Hindi, validation | Ex. 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: ... मोटर की गति बहुत अधिक होती है" | Engineering question about DC series motor — translated from English | IC, IF |
| D2 | Hindi, validation | Ex. 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? ... अभ्रक" | North Indian state-specific geography: UP minerals question | IC, IO |
| D3 | Hindi, validation | Ex. 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" | Mughal history — competitive-exam GK register | IC |
| D4 | Hindi, validation | Ex. 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? 44वें संविधान संशोधन अधिनियम द्वारा" | Constitutional law MCQ — Law & Governance domain | IO |
| D5 | Hindi, validation | Ex. 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" | Literature question about English poet Wordsworth — not Hindi-board canonical literature | IC |
| D6 | Hindi, validation | Ex. 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा कि उसे अगले महीने बोनस मिलेगा।" | Hindi grammar (indirect speech) — formal Khari Boli register | IF, IC |
| D7 | Hindi, validation | Ex. 13 | option1 | "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? अरबी भाषा" | Hindi-language item about etymology of 'monsoon' — GK-style | IC |
| D8 | Hindi, validation | Ex. 22 | option4 | "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? अमृता शेरगिल" | Indian arts & culture — Amrita Shergil, India-centric | IC |
| D9 | Hindi, validation | Ex. 17 | option4 | "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? संपत्ति कर" | Economics/taxation MCQ — pan-India competitive exam register | IO |
| D10 | Hindi, validation | Ex. 15 | option3 | "1950 में स्थापित, भारतीय रेलवे द्वारा स्वामित्व वाली औद्योगिक इकाइयों में से एक का नाम भारतीय स्वतंत्रता सेनानी के नाम पर रखा गया है: चित्तरंजन दास" | Indian history — Chittaranjan Das/railways — competitive GK | IC |
| D11 | English, validation | Ex. 3 | option4 | "What was the first capital of the Bahamani Kingdom? ... Gulbarga" | Medieval Indian history — source question in English | IC |
| D12 | English, validation | Ex. 9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct? Estimate Committee: All members of this committee are from Assembly only." | Maharashtra state-specific governance question | IC, IO |
| D13 | Hindi, validation | Ex. 3 | option2 | "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" | Electrical engineering MCQ — translated from English | IC |
| D14 | Hindi, validation | Ex. 4 | option2 | "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। शेल" | Engineering transformer question — translated item with 'शेल' (shell) transliteration | IC, IF |
| D15 | Hindi, validation | Ex. 10 | option4 | "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" | Health science MCQ — translated, with 'नाइट्रेट' transliteration retained | IC |
| D16 | Gujarati, validation | Ex. 24 | option3 | "સિંધિ કવિ અને લેખક વસદેવ મોહીનું 2019 માટેના સરસ્વતી સન્માન માટે પસંદગી ... કેકે બિરલા ફાઉન્ડેશન" | Saraswati Samman award question — India-centric literary award | IC |
| D17 | Marathi, validation | Ex. 16 | option3 | "हलषष्ठी सण का साजरा केला जातो? मुलाच्या दीर्घायुष्यासाठी" | Regional Indian festival (Halsashti) — local cultural knowledge | IC |
| D18 | English, validation | Ex. 1 | option3 | "What was the immediate cause for loss of foreign reserves triggering the financial crisis in 1991? Sharp rise in value of imports of oil & petroleum products" | 1991 India economic crisis — same question as Bengali D1 | IC |
| D19 | Hindi, validation | Ex. 18 | option3 | "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था? तेल और पेट्रोलियम उत्पादों के आयात के मूल्य में तीव्र वृद्धि" | Hindi translation of English Ex. 1 — translation quality check | IC |
| D20 | Hindi, validation | Ex. 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते? आठ" | Sports GK — India-centric, recent current affairs | IC |
| D21 | Bengali, validation | Ex. 12 | option4 | ""মঙ্গল ভারত" কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল: আচার্য বিনোবা ভাবে" | Literature: 'Mangal Bharat' work attributed to Vinoba Bhave | IC |
| D22 | Telugu, validation | Ex. 25 | option1 | "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? మొరెనా" | Madhya Pradesh state-specific geography — sub-national knowledge | IC |
| D23 | Hindi, validation | Ex. 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है? एक जंप लेबल या फॉर्मेट लेबल" | Computer science MCQ — translated, technical vocabulary | IC |
| D24 | Hindi, validation | Ex. 5 | option1 | "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं: ... उत्तरी अमेरिका का अटलांटिक तट" | Mediterranean climate geography — translated, no North India content | IC |
| D25 | Hindi, validation | Ex. 19 | option3 | "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? पाकिस्तान" | Partition history — India-centric GK | IC |
| D26 | English, validation | Ex. 17 | option3 | "What is the title of Yashpal Committee Report (1993)? Learning without burden" | India education policy — relevant to teacher deployment | IO |
| D27 | Marathi, validation | Ex. 15 | option1 | "वर्ष 2020 मध्ये, भारत सरकारने राष्ट्रीय शिक्षण धोरण सादर केले. आतापर्यंत किती राष्ट्रीय शिक्षण धोरणे सादर करण्यात आली आहेत? 3" | NEP question — Indian education policy | IO |
| D28 | Hindi, validation | Ex. 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: ... is_translated: True" | is_translated=True flag on all 26 Hindi validation examples reviewed | IC |
| D29 | Gujarati, validation | Ex. 16 | option2 | "છત્તીસગઢના નીચેના કયા બળવાઓને 'બસ્તરનો સ્વાતંત્ર્ય સંઘર્ષ' પણ કહેવામાં આવે છે? લિંગગિરી બળવો" | Chhattisgarh regional history — cross-state cultural knowledge | IC |
| D30 | English, validation | Ex. 11 | option2 | "The owner of the textile shop brought a ... Calculator" | Truncated/incomplete question — possible data quality issue | IF |
| D31 | Punjabi, validation | Ex. 21 | option3 | "ਰਾਸ਼ਟਰੀ ਸਰੋਂ ਖੋਜ ਕੇਂਦਰ ਕਿੱਥੇ ਸਥਿਤ ਹੈ - ਸੇਵਰ" | National Mustard Research Centre location — Rajasthan-specific | IC |
| D32 | Hindi, validation | Ex. 24 | option4 | "तंगस्टन तत्व का प्रतीक क्या है? W" | Chemistry: symbol for tungsten — straightforward science MCQ | IC |
| D33 | Malayalam, validation | Ex. 15 | option2 | "സർക്കസുകളിൽ തൊഴിൽ നിരോധിക്കണമെന്ന് ... ബച്ച്പൻ ബചാവോ ആന്ദോളൻ വേഴ്സസ് യൂണിയൻ ഓഫ് ഇന്ത്യ" | Child labour / constitutional law — Bachpan Bachao Andolan case | IO |
| D34 | Hindi, validation | Ex. 12 | option3 | "आमतौर पर लकड़ी के रेशों की लंबाई के साथ सूजन कितनी होती है: 0.1 से 0.8%" | Materials science MCQ — translated engineering content | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Strict MCQ format with single correct answer — structural alignment with deployment
- **Dimension(s):** IO, OO
- **Observation:** All sampled examples across all 11 language configs are uniformly formatted as single-correct-answer MCQs with exactly four options and a single target label. No reading-comprehension, multi-select, or open-ended items are present in the sample.
- **Deployment relevance:** The deployment requires strict MCQ evaluation with positive/negative marking where one answer is correct. MILU's format is a direct structural match to this requirement.
- **Datapoint citations:**
  - [D1] Hindi Ex. 1 (Hindi, split=validation, label=option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है:" — four options, single target, binary scoring ready.
  - [D6] Hindi Ex. 9 (Hindi, split=validation, label=option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें।" — grammar MCQ, same format, one correct answer.

#### Strength 2: Hindi Devanagari script — correct script and register
- **Dimension(s):** IF
- **Observation:** All Hindi-config items appear in fluent Devanagari script. The language register is formal standard Hindi (Khari Boli), with grammatically complete sentences and standard academic vocabulary. No script mixing or Roman transliteration is observed in the question stems (only in proper nouns and some technical terms).
- **Deployment relevance:** The deployment is text-only, Hindi-medium, Devanagari script. Script alignment is complete.
- **Datapoint citations:**
  - [D6] Hindi Ex. 9 (Hindi, split=validation, label=option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — formal academic Hindi grammar question in clean Devanagari.
  - [D7] Hindi Ex. 13 (Hindi, split=validation, label=option1): "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? अरबी भाषा" — Hindi GK question in standard written Hindi.

#### Strength 3: India-centric general knowledge content with some North Indian regional specificity
- **Dimension(s):** IC
- **Observation:** The Hindi sample includes questions with clear India-specific and North-India-specific content: a UP-minerals geography question, a Mughal history question, a constitutional law question, and an Indian freedom-fighter question. These reflect content broadly familiar to North Indian teachers from competitive-exam contexts.
- **Deployment relevance:** Teachers deploying the system in UP, MP, Rajasthan, and Bihar will encounter questions about subjects directly relevant to their syllabi and general knowledge background.
- **Datapoint citations:**
  - [D2] Hindi Ex. 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? अभ्रक" — UP-specific geographic knowledge directly relevant to North Indian state-board curriculum.
  - [D3] Hindi Ex. 25 (Hindi, split=validation, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" — Mughal history item aligning with North Indian history syllabus.
  - [D25] Hindi Ex. 19 (Hindi, split=validation, label=option3): "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? पाकिस्तान" — partition history, standard North Indian school and competitive-exam content.

#### Strength 4: Multiple subject domains present in Hindi sample — partial curricular breadth
- **Dimension(s):** IO
- **Observation:** The 26 Hindi validation examples span Engineering & Tech (6 items), Environmental Sciences (3), Arts & Humanities (4 — History, Literature, Language Studies, Arts & Culture), Law & Governance (1), Health & Medicine (1), Business Studies (3), and Science (4). This covers all 8 declared domains, providing evidence that domain breadth is not illusory for Hindi.
- **Deployment relevance:** The deployment requires coverage across all Hindi state and central board syllabi; MILU's multi-domain structure at least nominally addresses this, though the depth within each domain varies.
- **Datapoint citations:**
  - [D4] Hindi Ex. 6 (Hindi, split=validation, label=option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — Law & Governance domain present.
  - [D9] Hindi Ex. 17 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? संपत्ति कर" — Business Studies / Economics domain.
  - [D20] Hindi Ex. 2 (Hindi, split=validation, label=option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — Sports & Recreation / Social Sciences domain present.

#### Strength 5: Cross-language answer-key consistency visible in the data
- **Dimension(s):** OC
- **Observation:** A structurally identical question appears in both English (Ex. 1) and Hindi (Ex. 18) with the same correct answer (option3 in both), confirming consistent answer-key application across translations. The deployment user confirmed that competitive-exam answer keys are broadly compatible with North Indian teacher norms.
- **Deployment relevance:** Reduces concern about answer-key divergence between competitive-exam-sourced labels and North Indian board norms.
- **Datapoint citations:**
  - [D18] English Ex. 1 (English, split=validation, label=option3): "What was the immediate cause for loss of foreign reserves triggering the financial crisis in 1991? Sharp rise in value of imports of oil & petroleum products"
  - [D19] Hindi Ex. 18 (Hindi, split=validation, label=option3): "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था? तेल और पेट्रोलियम उत्पादों के आयात के मूल्य में तीव्र वृद्धि" — same item, same answer, consistent key.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: All reviewed Hindi validation examples are machine-translated (is_translated=True)
- **Dimension(s):** IC, IF
- **Observation:** Every single one of the 26 Hindi validation examples in the sample has `is_translated: True`. This is consistent across all items — no natively sourced Hindi item appears in the validation split sample. The benchmark paper states that only ~25% of total questions are translated, but this sample suggests that the validation split for Hindi may disproportionately (or entirely) consist of translated items. If true for the test split as well, the Hindi-language content would not reflect questions drawn from Hindi-language competitive exams but rather English-sourced content machine-translated by GPT-4O.
- **Deployment relevance:** This is critical because: (1) translated items may not reflect the register, phrasing conventions, and topic selection of actual Hindi-medium competitive-exam questions; (2) North Indian Hindi-medium teachers are being assessed on a model that was evaluated on items translated from English rather than native Hindi exam content; (3) subject-specific terminology choices in the translations may not align with state-board conventions.
- **Datapoint citations:**
  - [D28] Hindi Ex. 1 (Hindi, split=validation, label=option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" — is_translated=True; this is an engineering question where the Hindi text is a translation of an English-language technical question.
  - [D14] Hindi Ex. 4 (Hindi, split=validation, label=option2): "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। शेल" — is_translated=True; the answer option 'शेल' is a transliteration of 'shell' rather than a standard Hindi technical term.
  - [D15] Hindi Ex. 10 (Hindi, split=validation, label=option4): "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" — is_translated=True; 'नाइट्रेट' is a transliteration choice that may differ from Vaigyaanik evam Takniki Shabdavali Aayog standardized Hindi science terminology.

---

#### MAJOR

#### MAJOR Concern 1: No canonical Hindi-board literary content visible — competitive-exam GK register dominates Arts & Humanities
- **Dimension(s):** IC, IO
- **Observation:** The Arts & Humanities items in the Hindi sample do not include any questions about canonical Hindi-board literary figures (Tulsidas, Premchand, Kabir, Mahadevi Varma, etc.) or school-syllabus Hindi literature. The one Literature & Linguistics item is about William Wordsworth (an English poet). The History items are about Mughal texts and administrative history — consistent with a UPSC/SSC competitive-exam GK register rather than a school-literature register. No Hindi-medium literature, no doha analysis, no textual comprehension of Ramcharitmanas passages is observed.
- **Deployment relevance:** North Indian Hindi-medium teachers — and the students they evaluate — work with a school-board literature curriculum that foregrounds Hindi authors in a literary register (close reading, aesthetic appreciation) rather than a general-knowledge administrative register. MILU's competitive-exam sourcing produces a different kind of Arts & Humanities content than what a UP Board or CBSE Hindi teacher would encounter in their daily work.
- **Datapoint citations:**
  - [D5] Hindi Ex. 7 (Hindi, split=validation, label=option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" — Literature & Linguistics item asks about an English Romantic poet, not Hindi-board canonical literature.
  - [D3] Hindi Ex. 25 (Hindi, split=validation, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" — History item is administrative/courtly Mughal text authorship — UPSC GK register, not school-syllabus framing.
  - [D8] Hindi Ex. 22 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? अमृता शेरगिल" — Arts & Culture item is factual identification of artist, GK-style.

#### MAJOR Concern 2: Subject coverage in Hindi validation sample skews heavily toward Engineering & Tech, under-representing Civics/Political Science and Social Sciences
- **Dimension(s):** IO
- **Observation:** Of 26 Hindi validation examples, 6 are Engineering & Tech (23%), with only 1 Law & Governance item and no standalone Civics/Political Science or dedicated Social Sciences item (beyond 2 Sports items). Hindi-board curricula in UP, MP, Rajasthan, and Bihar place substantial emphasis on Civics, Panchayati Raj, and Social Sciences — subjects directly assessed in state board exams. The Engineering & Tech items (DC motors, transformers, rectifiers) are more characteristic of polytechnic or engineering entrance exams than school-board or general teacher deployment.
- **Deployment relevance:** If this imbalance persists in the test split, the benchmark may not adequately differentiate LLM performance on the civics and social science domains most relevant to the deployment's North Indian teacher population.
- **Datapoint citations:**
  - [D1] Hindi Ex. 1 (Hindi, split=validation, label=option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" — electrical engineering, likely not in UP Board secondary teacher's core domain.
  - [D13] Hindi Ex. 3 (Hindi, split=validation, label=option2): "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" — second engineering item in sample; both translated.
  - [D4] Hindi Ex. 6 (Hindi, split=validation, label=option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — only Law & Governance item; pertains to constitutional amendment, not Panchayati Raj or state-level civics.

#### MAJOR Concern 3: No sub-national state-board granularity verifiable from item content — potential under-representation of UP/Bihar/Rajasthan state-specific content
- **Dimension(s):** IC, IO
- **Observation:** Only one of the 26 Hindi examples explicitly names a North Indian state in its question (Ex. 26: UP minerals). No items about UP Panchayati Raj structure, Bihar Board history, Rajasthan state administrative geography, or MP-specific civics are visible. Items with state-specific content appear in other language configs (Telugu Ex. 25 mentions Madhya Pradesh; English Ex. 9 mentions Maharashtra), but the Hindi sample shows limited sub-national specificity for the primary Hindi-belt states.
- **Deployment relevance:** The deployment must serve teachers whose students are evaluated on state-board syllabi from UP, MP, Rajasthan, and Bihar specifically. If MILU's Hindi items are drawn primarily from pan-India competitive exams rather than state-level civil service exams, North Indian state-specific curricular content may be structurally absent.
- **Datapoint citations:**
  - [D2] Hindi Ex. 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — the only state-specific Hindi item in the sample, and it is a mineral geography question rather than civics or governance.
  - [D22] Telugu Ex. 25 (Telugu, split=validation, label=option1): "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? మొరెనా" — MP industrial geography appears in Telugu config, not in Hindi.
  - [D12] English Ex. 9 (English, split=validation, label=option2): "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" — state-specific governance in English config (Maharashtra), not Hindi-belt states.

#### MAJOR Concern 4: Translated Hindi items exhibit register and terminology choices not validated for state-board Hindi norms
- **Dimension(s):** IC, IF
- **Observation:** Translated Hindi items retain English technical terms as transliterations rather than using standardized Hindi or Vaigyaanik evam Takniki Shabdavali Aayog equivalents. Examples: 'शेल' (shell type transformer), 'नाइट्रेट' (nitrate), 'पल्सेटिंग डीसी' (pulsating DC), 'जंप लेबल' (jump label), 'स्ट्राइकथ्रू' (strikethrough), 'सुपरस्क्रिप्ट' (superscript). State board science textbooks in Hindi (particularly UP Board and CBSE Hindi medium) often use different terminological conventions — either fully Sanskritized or anglicized in different proportions. This creates a potential register mismatch between MILU's translated vocabulary and what North Indian teachers and students encounter in board textbooks.
- **Deployment relevance:** A teacher evaluating student answers in a Hindi-medium school context will have been trained on a specific terminological register. MILU's translated items may use vocabulary choices that diverge from that register, reducing the ecological validity of benchmark performance as a predictor of deployment performance.
- **Datapoint citations:**
  - [D14] Hindi Ex. 4 (Hindi, split=validation, label=option2): "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। शेल" — 'शेल' is a direct transliteration of 'shell'; standard Hindi technical texts might use 'कोश' or retain 'शेल' differently spelled.
  - [D23] Hindi Ex. 8 (Hindi, split=validation, label=option1): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है? एक जंप लेबल या फॉर्मेट लेबल" — 'जंप लेबल' and 'फॉर्मेट लेबल' are transliterations; CS items in Hindi textbooks vary in how they render these terms.
  - [D15] Hindi Ex. 10 (Hindi, split=validation, label=option4): "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" — 'नाइट्रेट' is transliterated; UP Board biology texts may use 'नाइट्रेट' or 'नत्रज लवण' depending on edition.

---

#### MINOR

#### MINOR Concern 1: One English-config item appears truncated or incomplete
- **Dimension(s):** IF
- **Observation:** English Ex. 11 reads: "The owner of the textile shop brought a" with options Calculator, Computer, Pencil, Fountain pen — the question stem appears incomplete, missing the context that would identify what the shop owner brought. The correct answer (Calculator) is unverifiable from the stem alone.
- **Deployment relevance:** An individual data quality issue; not indicative of a systemic problem given the documented filtering steps, but suggests noise remains in the dataset.
- **Datapoint citations:**
  - [D30] English Ex. 11 (English, split=validation, label=option2): "The owner of the textile shop brought a ... Calculator" — question stem appears to be cut off or missing context, making the correct answer unverifiable from the question alone.

#### MINOR Concern 2: Some items require very recent current-affairs knowledge (2022 sports results, 2020 awards) that may have finite shelf life
- **Dimension(s):** IC
- **Observation:** Several Hindi and non-Hindi items reference very recent events: India's 2022 Archery Asia Cup medals (Hindi Ex. 2), AAP forming government in Punjab in Feb-March 2022 (Bengali Ex. 5, Punjabi Ex. 5), 65th Filmfare Awards 2020 (Bengali Ex. 17, Kannada Ex. 17, Tamil Ex. 17). These items have definite correct answers but become increasingly anomalous as time passes.
- **Deployment relevance:** For a teacher using the system to evaluate students in 2025+, current-affairs items from 2022 may appear dated, and models trained on more recent data may give different performance profiles on these items than at benchmark creation time.
- **Datapoint citations:**
  - [D20] Hindi Ex. 2 (Hindi, split=validation, label=option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते? आठ" — 2022 sports result.
  - [D8] Hindi Ex. 22 (Hindi, split=validation, label=option4): "65वें फिल्मफेयर पुरस्कारों, 2020 में..." — referenced across multiple language configs as a parallel translated item.

#### MINOR Concern 3: Some items across language configs appear to be exact translations of the same English source, suggesting limited native-language diversity
- **Dimension(s):** IC
- **Observation:** The same questions (Bahamani Kingdom capital, Mediterranean climate characteristics, Qutub Minar, Fortran 77, cross-assembler, 1991 financial crisis) appear word-for-word translated across Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, and Telugu. This parallel structure confirms that a significant fraction of the benchmark is a multilingual translation of a shared English-language item pool, not independently sourced native-language questions.
- **Deployment relevance:** For Hindi specifically, this means items that appear to be Hindi-language MCQs may in fact test the model's ability to process translated English content rather than culturally and linguistically native Hindi knowledge — a moderate concern for a deployment aimed at Hindi-medium North Indian teachers whose students encounter native Hindi-register content.
- **Datapoint citations:**
  - [D11] English Ex. 3 (English, split=validation, label=option4): "What was the first capital of the Bahamani Kingdom? Gulbarga" — same question visible in Bengali Ex. 3, Gujarati Ex. 3, Hindi (implicitly), Malayalam Ex. 3, Punjabi Ex. 3.
  - [D24] Hindi Ex. 5 (Hindi, split=validation, label=option1): "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं: ... उत्तरी अमेरिका का अटलांटिक तट" — Mediterranean climate question appears translated across all 11 configs with identical structure.

---

### Content Coverage Summary

The Hindi-config validation sample (26 items) is entirely machine-translated (is_translated=True for all items reviewed), which is the most significant single observation from the data. Subject coverage spans all 8 declared domains, with a clear skew toward Engineering & Tech (23% of sample) and away from Civics/Political Science. The register is formal standard Hindi (Khari Boli) throughout, but technical vocabulary in translated items uses transliteration conventions (शेल, नाइट्रेट, जंप लेबल) that may not align with state-board Hindi textbook norms. Arts & Humanities items in the Hindi sample are in a competitive-exam GK register (factual identification, administrative history) rather than a school-literature register; no canonical Hindi literary figures (Tulsidas, Premchand, Kabir) appear in the sample. One UP-specific geography item provides the only sub-national Hindi-belt state-specific content visible.

Non-Hindi language configs (Bengali, Gujarati, Kannada, Marathi, etc.) also show nearly universal is_translated=True flags in the validation split, and many identical questions appear across all 11 languages, confirming that the validation split is heavily drawn from the translated English item pool. The English config contains genuinely India-centric questions including Maharashtra governance, Indian education policy (Yashpal Committee), and Indian railways history, all non-translated and well-formed. The Marathi config shows regionally specific Indian cultural content (Halsashti festival). Some items have a data quality issue (English Ex. 11 truncated question stem). Current-affairs items from 2020–2022 are present across multiple configs.

---

### Limitations

1. **Sample size per config:** Only 16–26 examples per language config were reviewed; subject-level coverage within each domain cannot be reliably assessed from this sample size. The test split may have a different is_translated distribution than the validation split.

2. **Validation-split translation bias:** The observation that all 26 Hindi validation items are translated may reflect deliberate design (translated items used for few-shot/validation purposes) or a split-level artifact. The test split — which is the primary evaluation set — may contain a higher proportion of natively sourced Hindi items. This cannot be determined from the available sample.

3. **Full subject-level statistics unavailable:** Supplementary Table 9 of the MILU paper (per-language, per-subject item counts) is not publicly accessible without the full PDF; the proportion of Hindi items by subject and whether specific Hindi-board subjects (Hindi Literature, UP History, Rajasthan Polity) are well-represented cannot be assessed from the sample.

4. **No test-split examples reviewed:** All examples are from the validation split. The test split (which would be the deployment evaluation set) was not sampled; its domain, subject, and is_translated distributions may differ.

5. **Annotation quality not directly assessable:** Whether individual answer keys are correct cannot be verified from the data alone without independent subject-matter expertise; the truncated English item (D30) is the only clear quality signal visible.

6. **Register variation within Hindi not assessable from script alone:** Whether MILU's formal Khari Boli register matches UP Board, MP Board, or CBSE Hindi-medium textbook norms requires comparison with those textbooks, which was not possible from the dataset sample.

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
