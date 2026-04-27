I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **MILU: A Multi-task Indic Language Understanding Benchmark** is valid for use in **Hindi-Medium Competitive Exam Aspirants — North India (Central Exams)**.

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

- **Name**: MILU
- **Full Name**: MILU: A Multi-task Indic Language Understanding Benchmark
- **Domain**: Multi-domain Indic language understanding and cultural knowledge evaluation
- **Languages**: hi, bn, gu, kn, ml, mr, or, pn, ta, te, en
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
MILU is structured as a multiple-choice question benchmark spanning 8 domains
and 41 subjects across 11 Indic languages [Q1], encompassing Arts and Humanities,
Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine,
Science, Engineering and Technology, and Business Studies [Q42]. The benchmark
explicitly frames itself as a "multi-domain test of India-specific knowledge"
[Q22] and claims comprehensive evaluation of LLMs "across 11 Indic languages,
spanning diverse domains and culturally relevant subjects" [Q74].

The MCQ-only format [Q33] aligns with the deployment's strict binary correct/incorrect
scoring requirement, and the competitive-exam sourcing methodology (similar to
AGIEVAL) means the task taxonomy is drawn from national and state civil services
exams, government and private organization exams, and regional exams [Q24, Q95,
Q96, Q97]. Regional state exams are explicitly valued for capturing local
knowledge and emphasizing state official languages [Q28]. However, the 41-subject
taxonomy was derived from competitive-exam domains rather than school or university
board syllabi, which creates a potential curricular gap for the Hindi-medium
teacher deployment context targeting UP Board, MP Board, CBSE, and similar
curricula. Subject-level statistics across languages are documented in Table 9
[Q98], but no state-by-state breakdown of which Hindi-belt exams contribute
to the Hindi-language item pool is reported.

Indic-specific LLMs evaluated are primarily adaptations of English base models
rather than natively Indic-trained systems [Q60], a contextual factor relevant
to interpreting Hindi-language performance results.

### Input Content
MILU questions were sourced from over 1,500 competitive exams across India,
scraped from publicly available online exam portals hosting previously released
question papers [Q13, Q25]. The collection explicitly targets an India-first
design that incorporates regional and state-level examinations covering local
history, arts, festivals, and laws alongside standard academic subjects [Q2, Q11,
Q14]. English-language questions with India-specific content are also included,
as such content is "notably missing from existing popular benchmarks" [Q30].

Of approximately 150K questions collected, around 79K are released [Q29, Q46],
with each subject-language pair capped at 500 questions. Critically, 25% of
the released questions are translated from English into the target language
using GPT-4O rather than a specialist translation model [Q44, Q45, Q47]. For
Hindi specifically, translated content may carry a pan-India formal register
rather than the regional academic register familiar to North Indian state-board
teachers and students. A separate validation set of approximately 9,000 questions
supports few-shot evaluation [Q51].

The exam-source distribution across the 40+ exam types [Q27, Q92] spans national
civil services (Table 6 [Q95]), government and private organization exams (Table
7 [Q96]), and state-level civil services exams (Table 8 [Q97]), but no breakdown
by specific Hindi-belt state (UP, MP, Rajasthan, Bihar) is reported in the
paper. For the Hindi-medium teacher deployment, this undocumented sub-national
distribution is a material content validity concern, as under-representation
of a major Hindi-belt state's exam content would leave canonical curricular
framings uncovered. Detailed topic and language distributions are referenced
in Table 9 and Figure 6 [Q93] but subject-level granularity by Hindi-state
source is not reported.

### Input Form
All questions in MILU are text-based MCQs with up to four answer options [Q33].
Reading-comprehension-style questions, image-based questions, and items with
more than four options were explicitly excluded to ensure uniformity [Q33].
Language identification was enforced using INDICLID and Unicode-based filtering
to ensure questions appear in the correct script [Q34], and duplicate removal
was applied [Q35]. Both automated and manual cleaning layers were employed
[Q31, Q32, Q36].

For the Hindi-medium teacher deployment — text-only in Devanagari script — this
format alignment is strong. Hindi is a high-resource language in this context,
and Devanagari is the native script. No modality mismatch exists. The 45% of
questions that arrived pre-tagged with a topic name were accepted as-is; the
remainder were translated into English via INDICTRANS2 and tagged using
GPT-4O-MINI before being tagged and grouped [Q37, Q38]. The K-means clustering
step over tag embeddings [Q40] and manual merging into final subject labels
[Q41] affect item labeling but not the underlying text form of the questions.

### Output Ontology
MILU's output space is a closed set of four multiple-choice options per question
with a single correct answer per item [Q22, Q55], directly matching the binary
correct/incorrect scoring structure of the Hindi-medium teacher deployment.
Culturally relevant subject areas — local history, arts, festivals, and laws —
are explicitly represented within the subject taxonomy alongside traditional
academic subjects like science [Q12, Q42].

Domain-wise analysis shows that models consistently perform worse in Arts &
Humanities, Social Sciences, and Law & Governance than in STEM [Q20, Q62, Q71],
which the authors attribute to training corpora lacking sufficient culturally
specific data [Q72]. For the Hindi-medium teacher deployment, this performance
disparity is directly relevant: the culturally loaded domains where MILU is
hardest are precisely the domains where Hindi-board teachers assess student
responses. The authors explicitly note this as a stated limitation [Q6, Q77].
The coarse aggregation of approximately 20,000 fine-grained tags into 41 subjects
[Q39, Q42] means Hindi-specific literary and cultural subtopics (e.g., Hindi
literature, regional medieval history) may be subsumed within broader "Arts and
Humanities" labels, making item-level granularity for canonical Hindi-board
topics difficult to assess from the paper alone.

### Output Content
Annotation in MILU is substantially delegated to the original exam portals, which
typically tag questions manually with topic names and language details, with subject
experts ensuring answer accuracy [Q26]. Internal manual review was conducted by
AI4Bharat team volunteers through manual audits [Q87], and cluster-level subject
label assignment was done through manual review of the K-means clusters [Q41].

NOT DOCUMENTED: The paper provides no demographic breakdown of annotators —
their regional backgrounds (North vs. South India), language proficiencies,
or familiarity with specific Hindi state-board curricula are not reported.
The institutional concentration at IIT Madras (Chennai) is worth noting as a
potential geographic asymmetry relative to the North Indian Hindi-belt deployment
context. Because the user confirms that evaluation schemas are broadly consistent
across North Indian boards and competitive-exam settings [elicitation Q4], the
annotator-population mismatch risk is assessed as moderate rather than severe,
but the absence of documentation prevents verification. The 25% translated
portion [Q47] adds further uncertainty: translation by GPT-4O rather than by
human annotators familiar with the target Hindi register introduces label
provenance concerns for subject-specific terminology.

### Output Form
MILU evaluates models using accuracy as the primary metric, reported at subject
and domain level across zero-shot, one-shot, and five-shot setups [Q50, Q59,
Q100]. For non-API models, the log-likelihood method via LM-EVALUATION-HARNESS
selects the answer option with the highest conditional log probability [Q52, Q53,
Q54, Q55] — a method that aligns with binary correct/incorrect scoring. API-based
models use a generative approach with structured JSON output due to lack of
log-probability access [Q56, Q57], evaluated only in zero-shot due to cost
constraints [Q58].

The log-likelihood approach may yield different results compared to generation-based
evaluation or chain-of-thought prompting [Q85], and instruct models show
inconclusive behavior under few-shot prompting [Q65, Q66]. Extensive per-model,
per-subject, per-language accuracy tables (Tables 11–54) are provided in the
appendix [Q99–Q132], enabling granular isolation of Hindi-language performance
by domain. Output form is fully aligned with the deployment's binary scoring
requirement; no modality or representation mismatch exists.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge." |
| Q2 | 1 | input_content | "With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science." |
| Q3 | 1 | output_form | "We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q4 | 1 | output_form | "Open multilingual models outperform language-specific fine-tuned models, which perform only slightly better than random baselines." |
| Q5 | 1 | output_form | "Models also perform better in high-resource languages as compared to low-resource ones." |
| Q6 | 1 | output_ontology | "Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM." |
| Q7 | 1 | input_ontology | "To the best of our knowledge, MILU is the first of its kind benchmark focused on Indic languages, serving as a crucial step towards comprehensive cultural evaluation." |
| Q8 | 1 | output_content | "All code, benchmarks, and artifacts will be made publicly available to foster open research." |
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
| Q21 | 2 | output_content | "All the artifacts will be released publicly." |
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
| Q37 | 4 | input_form | "Upon examination, we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information." |
| Q38 | 4 | input_form | "To address this issue, we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question." |
| Q39 | 4 | output_ontology | "Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap." |
| Q40 | 4 | input_form | "To organize them, we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters." |
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
| Q72 | 7 | output_ontology | "This suggests that the training corpora for these models lack sufficient culturally specific data. Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages." |
| Q73 | 7 | output_form | "As most Indic LLMs are built on English base models like LLAMA-2-7B, we assess the impact of language adaptation on their performance. Table 5 compares language-specific models with the original LLAMA-2-7B, and instruction-tuned models with LLAMA-2-7B-CHAT. Our findings show minimal gains, with some models even underperforming post-adaptation." |
| Q74 | 8 | input_ontology | "In this paper, we introduced MILU—Multilingual Indic Language Understanding Benchmark-a comprehensive benchmark specifically designed to evaluate LLMs across 11 Indic languages, spanning diverse domains and culturally relevant subjects." |
| Q75 | 8 | output_form | "We evaluate 45 different LLMs and find that the majority of LLMs struggle on MILU, with GPT4o achieving the highest average accuracy." |
| Q76 | 8 | output_form | "The analysis also shows that models perform significantly better in high-resource languages than low-resource ones, highlighting the need for more robust multilingual strategies." |
| Q77 | 8 | output_ontology | "Additionally, the domain-specific analysis indicates that models perform better in general fields such as STEM while facing challenges in culturally relevant subjects like Arts, Humanities, and Law, highlighting the lack of this knowledge in the current models and datasets." |
| Q78 | 8 | output_form | "We conjecture that limited performance gains may result from small language-specific datasets and reliance on parameter-efficient methods like LoRA (Hu et al., 2022)." |
| Q79 | 8 | output_form | "Another contributing factor could be the lack of diversity in instruction fine-tuning datasets." |
| Q80 | 8 | output_form | "Models like AIRAVATA, which utilize more diverse data (Gala et al., 2024), exhibit noticeably better performance." |
| Q81 | 8 | output_form | "Further investigation is required to fully understand the limitations and opportunities in this area." |
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
name: Hindi-Medium Competitive Exam Aspirants — North India (Central Exams)
abbreviation: IN-HI-COMPEXAM-NORTH
benchmark: milu
deployment_context: Mobile/enterprise application providing Hindi-language feedback
  (correct/incorrect label + explanatory rationale) to graduate students preparing
  for central-level competitive examinations (UPSC, SSC, banking exams) in North India.
geography:
  country: India
  region: North India
  primary_states:
  - Uttar Pradesh
  - Bihar
  - Rajasthan
  - Madhya Pradesh
  scope_note: Deployment is scoped to central-level examinations (UPSC, SSC, banking)
    with pan-India syllabus coverage, not state-level PSCs. Geographic focus reflects
    where the largest Hindi-medium aspirant populations are concentrated, but content
    scope extends to all-India GK.
  urban_rural_mix: Semi-urban and peri-urban aspirants are the primary target; significant
    share from small towns and district headquarters ('kasba' tier). Fully rural share
    is lower due to smartphone and app access requirements.
  urbanization_pct: '[NEEDS VERIFICATION — deferred: below search budget; national
    urbanization ~36% per 2011 census, but state-level semi-urban figures for exam-prep
    cohort not publicly aggregated]'
target_population:
  description: Graduate-level students actively preparing for Indian central government
    competitive examinations (UPSC Civil Services, SSC CGL/CHSL, IBPS/SBI banking
    exams). Likely first-generation or semi-urban exam aspirants from Hindi-medium
    educational backgrounds. Access the system via smartphone (Android-dominant).
    Primary motivation is securing central government employment.
  education_level: Bachelor's degree (required eligibility for UPSC/SSC); many are
    recent graduates or repeat aspirants ('repeaters') in the 21–28 age band.
  age_band: '[NEEDS VERIFICATION — deferred: likely unsearchable (not aggregated publicly);
    estimated 21–28 years based on eligibility requirements and exam culture norms]'
  gender_breakdown: 'Women constitute approximately one-third (~33%) of all UPSC applicants
    and approximately 30% of selected candidates in 2023. Women applicants nearly
    quadrupled over the past 15 years, outpacing total applicant growth. SSC/banking
    gender breakdown is not separately published at this granularity. Coaching institutes
    and study environments remain male-dominated in many districts. Source: The Print
    (Feb 2025) — [WEB-1];
    SleepyClasses (2025) — [WEB-2]'
  occupational_role: Full-time or part-time exam aspirant; may also hold temporary
    employment or be enrolled in coaching institutes ('coaching classes') in cities
    like Prayagraj, Patna, Jaipur, Indore.
  coaching_institute_prevalence: '[NEEDS VERIFICATION — deferred: below search budget;
    likely unsearchable at the quantitative level without specific survey data]'
  first_generation_learner_share: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice); no publicly aggregated figure found for this demographic slice]'
languages:
  primary: Hindi (Devanagari script)
  medium_of_instruction: Hindi-medium schooling and undergraduate education; limited
    formal English-medium exposure.
  code_mixing_tolerance: Moderate code-mixing with English technical/administrative
    terms acceptable; deployment-specified ceiling of approximately 10% English content.
    Heavy English-medium phrasing or Roman-script-dominant questions create construct-irrelevant
    difficulty for this population.
  english_proficiency: Functional reading of English technical terms (e.g., 'GDP',
    'Parliament', 'RBI') common; sustained English-medium text comprehension limited.
  script: Devanagari (Unicode standard; no RTL or capitalization complexity issues)
  dialect_notes: Standard Khari Boli Hindi (Manak Hindi) is the expected register
    for both exam content and AI feedback. Colloquial Bhojpuri, Awadhi, Rajasthani,
    or Malvi dialects are understood by subsets of the population but are not the
    target register.
  minority_languages_in_population:
  - Bhojpuri (Bihar, eastern UP)
  - Awadhi (central UP)
  - Rajasthani / Marwari (Rajasthan)
  - Bundeli / Malvi (MP)
writing_systems:
  scripts:
  - Devanagari (primary — Hindi)
  note: Standard Unicode Devanagari. No RTL concerns. Mixed Devanagari + Latin (for
    English technical terms) is the expected code-mixed form. NLP tokenization for
    Devanagari is mature for high-resource Hindi.
literacy_and_education:
  population_literacy_rate_hindi_states: 'Per 2011 Census (most recent census; 2021
    census pending): Bihar 61.8%, Rajasthan 66.1%, UP 67.7%, MP 70.6% — all below
    the national average of 74.0%. NSO post-census survey estimates (circa 2020) are
    marginally higher: Rajasthan ~69.7%, Bihar ~70.9%. These four states together
    account for nearly half of all Indian illiterates. Caveat: these are general population
    figures; the deployment targets graduate-level aspirants who are near-universally
    literate. Source: Census 2011 via Wikipedia — [WEB-3];
    NSO estimates via FindEasy — [WEB-4]'
  graduate_level_literacy: Near-universal within the target cohort (graduate enrollment
    is an exam eligibility requirement).
  hindi_medium_undergraduate_share: '[NEEDS VERIFICATION — deferred: below search
    budget; no publicly aggregated state-level figure for Hindi-medium college graduates
    found]'
  numeracy_notes: Mathematics and Reasoning are core exam subjects; aspirants have
    completed 10+2 mathematics. Advanced mathematics not required; arithmetic, data
    interpretation, and logical reasoning are the operative skills.
infrastructure_notes:
  device_profile: Android smartphone dominant; budget-to-mid-range handsets prevalent.
    iOS share low among this demographic.
  android_share_pct: '[NEEDS VERIFICATION — deferred: below search budget; nationally
    Android holds ~95%+ smartphone market share in India but state-specific figures
    for this cohort not published]'
  mobile_internet_penetration_target_states: 'IAMAI/Kantar ICUBE 2024 report: Uttar
    Pradesh 46% active internet user penetration, Bihar 43% (share of state population).
    Earlier 2023 ICUBE data showed UP at 41%, Bihar at 37%. Independent estimates
    put Bihar as low as 25–30% and UP at 30–41% depending on methodology and active
    vs. subscriber definition. UP and Bihar are among the largest subscriber bases
    in absolute numbers (73.6M and 69.9M respectively as of Sep 2023) but below-average
    in penetration rate. Caveat: these are general population figures; the exam-aspirant
    cohort (urban/semi-urban, smartphone-owning graduates) will have substantially
    higher internet access than the state average. Source: IAMAI/Kantar Internet in
    India 2024 — [WEB-5];
    Wikipedia Internet in India (TRAI data Sep 2023) — [WEB-6]'
  connectivity: 4G coverage in urban/semi-urban areas adequate; rural connectivity
    patchy. App must be functional under low-bandwidth or intermittent connectivity
    conditions.
  data_cost_sensitivity: High — aspirants in this cohort are cost-sensitive; heavy
    data usage may be a barrier.
  app_modality: Mobile app (primary) and enterprise/web (secondary). Text-only interface;
    no image or audio input required.
  offline_capability_requirement: '[NEEDS VERIFICATION — deferred: below search budget;
    whether offline mode is in deployment scope is a product-level decision, not a
    publicly documented fact]'
exam_ecosystem:
  primary_target_exams:
  - UPSC Civil Services Examination (Prelims + Mains)
  - SSC CGL (Combined Graduate Level)
  - SSC CHSL (Combined Higher Secondary Level)
  - IBPS PO / Clerk (Banking)
  - SBI PO / Clerk (Banking)
  - RRB NTPC (Railway Recruitment)
  exam_scope_note: Central-level examinations only; state-level PSCs (e.g., UPPSC,
    BPSC, RPSC, MPPSC) are explicitly out of scope for this deployment.
  priority_subject_areas:
  - General Knowledge
  - Current Affairs
  - History (Indian and World)
  - Indian Polity and Constitution
  - Mathematics and Quantitative Aptitude
  - Logical Reasoning and Mental Ability
  - Hindi Language Proficiency
  - Geography (Indian and World)
  - Economics and Indian Economy
  north_india_regional_content_within_central_exams: Central exams do test some North
    India–specific content (e.g., North Indian historical figures, land-revenue systems
    like zamindari/ryotwari abolition, festivals such as Chhath Puja, Mughal and medieval
    North Indian history, UP/Bihar administrative geography). AI must handle both
    pan-India GK and this sub-regional layer.
  exam_pattern: MCQ-based Prelims (objective); descriptive Mains for UPSC. The deployment
    targets the objective/MCQ preparation phase with rationale-based feedback.
  current_affairs_currency: Current Affairs questions require up-to-date knowledge;
    benchmark staleness is a validity risk for this subject area.
  upsc_applicant_scale: 'Approximately 13.4 lakh (1.34 million) candidates applied
    for UPSC 2024; roughly 50–55% actually appear for Prelims. Only ~1,000 candidates
    are ultimately selected. Source: PW / Physics Wallah (2024) — [WEB-7]'
  syllabus_documents:
    upsc_syllabus: 'Official UPSC CSE syllabus available at UPSC website: [WEB-8].
      Prelims: GS Paper I (History, Geography, Polity, Economy, Environment, Science)
      + CSAT (Aptitude); Mains: Essay + 4 GS papers + 2 Optional papers + 2 qualifying
      language papers.'
    ssc_cgl_syllabus: '[NEEDS VERIFICATION — deferred: below search budget; current
      SSC CGL syllabus available at SSC official site ssc.gov.in but specific URL
      not retrieved]'
    ibps_syllabus: '[NEEDS VERIFICATION — deferred: below search budget; current IBPS
      PO syllabus available at ibps.in but specific URL not retrieved]'
cultural_norms_notes: '- Exam culture in North India is intensely aspirational; central
  government employment (sarkari naukri) is a primary social mobility pathway, especially
  for first-generation graduates from semi-urban/rural backgrounds.

  - Coaching institute culture is deeply embedded: Prayagraj (formerly Allahabad)
  is the national hub for UPSC prep; Patna, Jaipur, and Indore have large SSC/banking
  coaching ecosystems.

  - Students are accustomed to rote-and-revision learning styles; explanatory feedback
  that mirrors pedagogical conventions of Hindi-medium coaching materials will be
  better received.

  - Social pressure and family investment in exam success are high; failure stigma
  is significant. Feedback tone should be constructive and motivating.

  - North Indian religious and cultural calendar (festivals such as Chhath Puja, Diwali,
  Holi, Navratri) intersects with exam prep cycles; Current Affairs questions may
  reference these.

  - Caste and reservation system (OBC, SC, ST categories) shapes aspirant demographics
  and exam eligibility; some GK questions may touch on reservation policy — culturally
  sensitive area. Per 2023 UPSC results: General 48%, OBC 27%, SC 15% of selected
  candidates.

  - Gender: Female aspirants now constitute approximately one-third of UPSC applicants
  (up from ~25% fifteen years ago), but coaching institutes and study environments
  remain male-dominated in many districts. Source: The Print (Feb 2025) — [WEB-1]

  - Language register: Feedback in simple, clear Manak Hindi (standard Hindi) is preferred
  over literary or highly Sanskritized Hindi, which may alienate Hindi-medium graduates
  from less privileged backgrounds.

  '
pedagogical_context:
  feedback_format_required: Correct/incorrect verdict (label) plus substantive Hindi-language
    explanation of why the answer is right or wrong. Label-only scoring is insufficient
    for deployment goals.
  explanation_register: Plain, accessible Manak Hindi. Avoid heavy English code-mixing
    (>10%), Sanskritized vocabulary, or English-medium textbook conventions.
  explanation_quality_dimensions:
  - Factual accuracy of the rationale
  - Fluency and naturalness in Hindi
  - Pedagogical clarity (does the explanation help the student understand the concept?)
  - Appropriate difficulty level for graduate-level Hindi-medium aspirants
  - Absence of misleading or contradictory information
  benchmark_output_mismatch_note: 'MILU evaluates only MCQ label accuracy; it provides
    no infrastructure for assessing explanatory rationale quality. This is a fundamental
    gap: benchmark scores cannot validate the deployment''s core output.'
  existing_hindi_nlg_evaluation_resources: 'No benchmark specifically evaluating Hindi-language
    explanatory rationale quality for competitive exam content was found. The closest
    relevant resources are: (1) IndicGenBench (2024) — evaluates LLM generation tasks
    (summarization, translation, QA) across 29 Indic languages including Hindi, but
    does not cover exam-explanation quality. Source: arXiv 2404.16816 — [WEB-9].
    (2) Pariksha (2024) — evaluates human vs. LLM agreement on Hindi output quality
    (linguistic acceptability, task quality, hallucination) across health/finance/culture
    prompts; methodology is relevant but domain does not cover competitive exam rationale.
    Source: arXiv 2406.15053 — [WEB-10]. (3) ''Benchmarking
    Hindi LLMs'' (arXiv 2508.19831, 2025) — introduces MT-Bench-Hi for instruction-tuned
    model evaluation in Hindi but targets conversational/instruction-following tasks,
    not exam-explanation generation. Source: [WEB-11].
    (4) A 2025 analysis of Indic LLM capabilities (arXiv 2501.13912) notes that most
    existing Hindi evaluation datasets are translated from English, limiting their
    capture of socio-cultural and domain-specific nuance. Source: [WEB-12].
    Conclusion: No purpose-built Hindi competitive-exam explanation quality benchmark
    exists; this is a genuine gap that represents a net-new evaluation development
    need for this deployment.'
domain_specific_notes:
  general_knowledge_and_current_affairs: Core UPSC/SSC subject. Requires up-to-date
    knowledge; any benchmark with a training cutoff will have stale Current Affairs
    items. Model must be robust to knowledge currency limitations.
  indian_polity_and_constitution: High-priority subject covering constitutional articles,
    amendments, fundamental rights/duties, DPSP, Parliament/judiciary structures,
    and landmark Supreme Court judgments. North Indian land-revenue and administrative
    history (zamindari, panchayati raj) also relevant.
  history: Both medieval (Mughal period, North Indian kingdoms) and modern Indian
    history (independence movement, key leaders from UP/Bihar such as Nehru, Gandhi,
    Bhagat Singh, Lal Bahadur Shastri) are prominent in central exams. Ancient Indian
    history also tested.
  mathematics_and_reasoning: Quantitative aptitude (arithmetic, percentage, ratio,
    data interpretation) and logical/analytical reasoning are heavily tested in SSC
    and banking exams. MILU's coverage of Mathematics/Reasoning in its Hindi subset
    needs verification.
  hindi_language_proficiency: Grammar, comprehension, vocabulary, and idiom questions
    in Hindi are tested in UPSC Mains and SSC exams. The AI's Hindi output quality
    is itself a validity-relevant consideration.
  geography: Physical geography of India (rivers, mountains, states/capitals) and
    North India–specific geography (Ganga-Yamuna doab, Deccan Plateau boundary) are
    relevant.
  economics: Indian economy, Five-Year Plans (historical), budget, monetary policy
    (RBI), and schemes (PM Kisan, MGNREGS, etc.) are standard current affairs/GK intersections.
  legal_and_governance: Indian constitutional law, IPC basics, and governance schemes
    are tested. Sharia or Islamic law is not relevant to this deployment context.
  north_india_sub_regional_knowledge:
    examples:
    - Chhath Puja (Bihar/UP festival — often appears in cultural GK)
    - Land revenue systems (zamindari abolition, ryotwari — UP/Bihar history)
    - Mughal administrative units (subas, sarkars, parganas)
    - North Indian freedom movement figures (Chandrashekhar Azad, Ram Prasad Bismil,
      Lal Bahadur Shastri)
    - UP/Bihar/Rajasthan/MP state capitals, high courts, major rivers
    - 'Administrative units: tehsil, mandal, district, division'
    benchmark_coverage_status: '[NOT FOUND — searched for MILU Hindi subject distribution
      and North India sub-regional content coverage; no published breakdown of MILU
      Hindi item distribution by exam type (UPSC vs. SSC vs. state PSC vs. banking)
      or by sub-regional North India content was found. MILU documents sourcing from
      40+ exam types at national and state levels but does not report intra-Hindi
      regional granularity. This remains an undocumented gap.]'
benchmark_validity_flags:
  central_exam_subject_distribution:
    status: partial_gap
    detail: MILU draws from over 40 exam types including national civil services,
      government and private organization exams, and state-level civil services exams
      [Q27, Q92, Q95, Q96, Q97]. However, the relative proportion of items aligned
      to UPSC/SSC/banking syllabi versus state PSC or regional exams is NOT DOCUMENTED.
      Mathematics/Reasoning and Current Affairs — top-priority subjects for central
      exams — are not explicitly called out as well-covered subject categories within
      the 41-subject taxonomy.
    web_search_target: MILU benchmark Hindi subject distribution UPSC SSC banking
      exam coverage Mathematics Reasoning Current Affairs proportion
    search_result: '[NOT FOUND — no published breakdown of MILU Hindi item proportions
      by exam type (UPSC/SSC/banking vs. state PSC) was found via search. The MILU
      paper documents sourcing from 40+ exam types but does not decompose item counts
      by exam category for the Hindi subset. Gap remains unresolved.]'
  hindi_code_mixing_rate:
    status: full_gap
    detail: MILU documents that approximately 25% of its released questions were translated
      from English using GPT-4O [Q47], introducing risk of elevated English code-mixing
      or unnatural phrasing. INDICLID and Unicode-based filtering were applied to
      remove incorrect language entries [Q34], but no characterization of residual
      English code-mixing frequency in the Hindi item pool is provided. The ~10% code-mixing
      ceiling specified for the deployment is entirely undocumented relative to MILU's
      actual Hindi question composition.
    web_search_target: MILU Hindi benchmark code-mixing English technical terms Devanagari
      item analysis Hindi-medium accessibility
    search_result: '[NOT FOUND — no published analysis of English code-mixing rates
      in MILU Hindi items found. The arXiv analysis of Indic LLM capabilities (2501.13912)
      notes that most Hindi evaluation datasets are translated from English, which
      is consistent with the code-mixing risk, but no quantification of MILU''s specific
      Hindi code-mixing rate was found. Gap remains unresolved.]'
  explanatory_rationale_quality:
    status: full_gap
    detail: MILU has no evaluation infrastructure for open-ended Hindi explanatory
      rationale. This is the deployment's core output and is entirely outside benchmark
      scope.
    web_search_target: Hindi language explanation quality evaluation NLG benchmark
      competitive exam rationale generation UPSC SSC
    search_result: 'No competitive-exam-specific Hindi explanation quality benchmark
      found. Closest relevant resources: IndicGenBench (arXiv 2404.16816) covers Hindi
      generation tasks but not exam rationale; Pariksha (arXiv 2406.15053) evaluates
      Hindi output quality (linguistic acceptability, task quality, hallucination)
      but for health/finance/culture domains; MT-Bench-Hi (arXiv 2508.19831, 2025)
      evaluates Hindi instruction-tuned models on conversational tasks. None cover
      the deployment''s core output type (competitive exam answer explanation in Hindi).
      This is a genuine evaluation gap requiring purpose-built tooling. Sources: [WEB-9];
      [WEB-10]; [WEB-11]'
  north_india_sub_regional_content:
    status: partial_gap
    detail: MILU includes culturally relevant subjects such as local history, arts,
      festivals, and laws [Q2, Q12], and explicitly targets regional state exams to
      capture local knowledge in each language [Q14, Q28]. However, whether Hindi-language
      items specifically cover North India sub-regional content (e.g., Chhath Puja,
      tehsil/mandal administrative structures, UP/Bihar/Rajasthan state-specific history)
      within the central-exam framing is NOT DOCUMENTED. The benchmark aggregates
      across all Indian states and languages without documenting intra-Hindi regional
      granularity.
    web_search_target: MILU Hindi items North India regional knowledge Chhath Puja
      UP Bihar Rajasthan history land revenue systems sub-regional cultural content
    search_result: '[NOT FOUND — no published documentation of MILU''s intra-Hindi
      regional content distribution found. Gap confirmed unresolved.]'
  hindi_medium_difficulty_calibration:
    status: full_gap
    detail: No documentation on whether MILU Hindi items were calibrated for Hindi-medium
      graduates vs. English-medium or bilingual students. Annotator demographics not
      reported.
    web_search_target: MILU benchmark Hindi-medium student accessibility difficulty
      calibration annotator demographics first-generation exam aspirants
    search_result: '[NOT FOUND — no published user study, difficulty calibration report,
      or annotator demographic breakdown for MILU''s Hindi subset found. The arXiv
      2501.13912 analysis notes that most Indic evaluation datasets are translated
      from English with limited socio-cultural grounding — consistent with this gap.
      Gap confirmed unresolved.]'
  output_format_mismatch:
    status: full_gap
    detail: MILU uses MCQ label accuracy (log-likelihood or JSON generative scoring).
      Deployment requires open-ended Hindi rationale generation. Benchmark scores
      cannot directly validate deployment output quality.
    web_search_target: Hindi open-ended text generation evaluation fluency coherence
      pedagogical quality competitive exam AI feedback benchmark
    search_result: Confirmed gap. No Hindi open-ended exam-feedback quality evaluation
      benchmark exists. Pariksha and MT-Bench-Hi are the closest methodological analogs
      but are not domain-matched. See 'explanatory_rationale_quality' above for full
      resource inventory.
regulatory_and_policy_context:
  data_protection: 'Digital Personal Data Protection Act 2023 (DPDPA) — enacted 11
    August 2023 (No. 22 of 2023). Applicable to all digital personal data processing
    within India, including mobile/enterprise edtech apps. Implementing DPDP Rules
    2025 were notified in November 2025; phased compliance with full operational provisions
    expected by May 2027. Penalties up to ₹250 crore for non-compliance. The DPDPA
    applies to the deployment as it processes student response data digitally. Note:
    parental consent provisions (Section 9) apply to users under 18; the deployment''s
    graduate-level target population (21–28) is above this threshold, so standard
    consent requirements (not parental consent) apply. Sources: MEITY official text
    — [WEB-13];
    EY India (Dec 2025) — [WEB-14];
    DLA Piper (Feb 2026) — [WEB-15]'
  ai_governance: 'Two applicable frameworks: (1) MeitY Advisory on AI (15 March 2024)
    — requires intermediaries deploying AI tools to ensure outputs are labelled, not
    unlawfully biased, and compliant with IT Rules 2021; applies to AI platforms from
    immediate effect. Source: Lexology — [WEB-16].
    (2) India AI Governance Guidelines (5 November 2025) — MeitY''s comprehensive
    framework under the IndiaAI Mission, emphasizing safe, inclusive, and responsible
    AI adoption with a sectoral regulatory approach (no standalone AI Act). Chaired
    by Principal Scientific Adviser; relevant to AI deployments in education but not
    yet education-sector specific. Source: NeGD/MeitY — [WEB-17].
    UGC''s NPAI Skilling Framework (2023) addresses AI in higher education curricula
    but does not regulate AI-based edtech tools. No specific MEITY or UGC regulation
    governing AI-assisted competitive exam preparation platforms has been enacted
    as of April 2026; compliance with DPDPA 2023 + MeitY Advisory 2024 represents
    the current operative framework.'
  exam_board_regulations: '[NOT FOUND — searched for UPSC/SSC/IBPS official guidelines
    on AI-assisted exam preparation; no publicly available regulatory restriction
    or guideline specifically addressing AI tools in competitive exam prep was found.
    UPSC and SSC regulate exam conduct but not candidate preparation tools. Gap confirmed:
    this is likely an unsearched/unenacted regulatory space as of April 2026.]'
  right_to_education_act_relevance: Not directly applicable (targets school-age education);
    graduate-level exam prep falls outside RTE scope.
net_new_fields:
  hindi_llm_evaluation_landscape_2024_2025:
    summary: 'The Hindi LLM evaluation ecosystem has grown substantially in 2024–2025
      but remains focused on MCQ accuracy, translation, and summarization — not domain-specific
      explanation quality. Key benchmarks: MILU (2024, ~79K MCQ items from Indian
      competitive exams), IndicGenBench (2024, generation tasks across 29 Indic languages
      including Hindi), IndicMMLU-Pro (2025, MMLU-Pro adapted for Indic languages),
      and ''Benchmarking Hindi LLMs'' suite (2025, five instruction-tuned model benchmarks
      including MT-Bench-Hi). The 2025 arXiv analysis of Indic LLM capabilities notes
      that a majority of Hindi evaluation datasets are direct translations of English
      datasets, limiting socio-cultural coverage — a finding directly relevant to
      MILU''s translated 25% subset. No benchmark covers Hindi competitive-exam explanation
      generation.'
    validity_relevance: Confirms that the output-form gap identified in the assessment
      (no Hindi generative explanation benchmark) is not an oversight — it reflects
      a genuine absence in the research ecosystem. The downstream scorer should weight
      this gap highly.
    sources: arXiv 2501.13912 (Jan 2025) — [WEB-12];
      arXiv 2508.19831 (Aug 2025) — [WEB-11]; arXiv 2404.16816
      (Apr 2024) — [WEB-9]; arXiv 2406.15053 (Jun 2024)
      — [WEB-10]
  indiaai_mission_education_relevance:
    summary: The IndiaAI Mission (launched March 2024, ₹10,371.92 crore over five
      years) includes education as a target sector and supports AI infrastructure
      development. The YuvAI Initiative (MeitY + AICTE) targets 100,000 students/developers
      aged 18–30 for AI capability building. These programs signal government endorsement
      of AI in education but do not yet impose product-level compliance requirements
      on competitive-exam prep tools.
    validity_relevance: Regulatory risk is currently low for this deployment category
      (no specific exam-prep AI regulation), but the landscape is evolving rapidly.
      Deployments should monitor MeitY sectoral guidance as the India AI Governance
      Guidelines implementation progresses.
    sources: PIB (Mar 2026) — [WEB-18];
      SCC Times (Nov 2025) — [WEB-19]
  pariksha_benchmark_methodological_relevance:
    summary: Pariksha (2024, arXiv 2406.15053) is a large-scale investigation of human
      vs. LLM evaluator agreement on Indic language outputs, covering Hindi across
      health, finance, and cultural prompts. It uses Linguistic Acceptability, Task
      Quality, and Hallucination as evaluation dimensions with human annotation. This
      is the closest methodological template for evaluating Hindi explanation quality
      in the deployment context, even though it does not cover competitive exam domains.
    validity_relevance: The Pariksha evaluation framework (LA + TQ + Hallucination,
      with native-speaker human annotation) could serve as a starting point for constructing
      a deployment-specific Hindi explanation quality evaluation protocol. Downstream
      assessment should flag this as an actionable recommendation.
    source: arXiv 2406.15053 — [WEB-10]
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://theprint.in/india/family-support-safety-study-material-a-click-away-whats-driving-more-women-to-take-upsc-exam/1922660/ |
| WEB-2 | https://sleepyclasses.com/discover-how-many-candidates-are-selected-in-upsc-each-year/ |
| WEB-3 | https://en.wikipedia.org/wiki/List_of_Indian_states_and_union_territories_by_literacy_rate |
| WEB-4 | https://www.findeasy.in/indian-states-by-literacy-rate/ |
| WEB-5 | https://www.iamai.in/sites/default/files/research/Kantar_%20IAMAI%20report_2024_.pdf |
| WEB-6 | https://en.wikipedia.org/wiki/Internet_in_India |
| WEB-7 | https://www.pw.live/upsc/exams/how-many-candidates-applied-for-upsc-2024 |
| WEB-8 | https://upsc.gov.in/ |
| WEB-9 | https://arxiv.org/abs/2404.16816 |
| WEB-10 | https://arxiv.org/html/2406.15053v1 |
| WEB-11 | https://arxiv.org/abs/2508.19831 |
| WEB-12 | https://arxiv.org/html/2501.13912v1 |
| WEB-13 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-14 | https://www.ey.com/en_in/insights/cybersecurity/decoding-the-digital-personal-data-protection-act-2023 |
| WEB-15 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-16 | https://www.lexology.com/library/detail.aspx?g=47dda3b5-1111-4b6b-9f87-799ef8066802 |
| WEB-17 | https://negd.gov.in/press_release/meity-unveils-india-ai-governance-guidelines-under-indiaai-mission-to-ensure-safe-inclusive-and-responsible-adoption-of-artificial-intelligence-across-sectors/ |
| WEB-18 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2234853&reg=3&lang=1 |
| WEB-19 | https://www.scconline.com/blog/post/2025/11/06/meity-launches-india-ai-governance-guidelines-under-indiaai-mission-2025/ |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: For a graduate student in North India preparing for competitive job exams (e.g., UPSC, SSC, state PSC, banking exams), which subject areas are most critical — General Knowledge, Current Affairs, Indian Polity & Constitution, Hindi language proficiency, regional history of North Indian states (UP, Bihar, Rajasthan, MP), or Mathematics/Reasoning? Are there specific exam types (Central vs. state-level) that your deployment must prioritize?
A1: The most critical subject areas are General Knowledge, Current Affairs, History, and Mathematics/Reasoning, supplemented by Indian Polity & Constitution and Hindi language proficiency. The deployment is scoped to central-level examinations (UPSC, SSC, banking) rather than state-level PSCs.

Q2 [IC]: Competitive exam questions for North Indian students often draw on culturally specific knowledge — e.g., festivals like Chhath Puja, regional administrative units like tehsils or mandals, state-specific historical figures, or North Indian legal and land-revenue traditions. Does your deployment expect the AI to handle this kind of regionally grounded content, or is the focus on pan-India general knowledge content?
A2: Central competitive examinations cover both North India–specific regional knowledge and pan-India general knowledge, so the AI must handle both. The benchmark's content should reflect this dual scope.

Q3 [OO]: When the AI provides feedback on a student's response, what should that feedback look like — a simple correct/incorrect label, an explanation of why an answer is right or wrong, a hint toward the correct answer, or an encouragement message in Hindi?
A3: The deployment requires both a correct/incorrect label and a substantive explanation of why the answer is right or wrong, delivered in Hindi. A label-only scoring benchmark (MCQ accuracy) does not fully match this deployment's output requirement.

Q4 [IC]: Since the target student has limited English exposure and interacts primarily in Hindi, would it be a problem if some benchmark questions — even in the Hindi portion — contain English technical terms, code-mixed phrasing, or assume familiarity with English-medium textbook conventions?
A4: Moderate code-mixing with English technical terms is acceptable, but should not exceed approximately 10% of the content. Fully English-medium conventions or heavy code-mixing would create a mismatch with the target student's linguistic profile.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | MILU was designed for India with questions sourced from 1500+ national and regional competitive exams, covering domains aligned with the deployment's priority subjects (GK, History, Polity, Reasoning); the main residual gap is verifying adequate coverage of central-exam–specific subject distributions versus state-level content. |
| IC | HIGH | Individual question instances must serve both pan-India GK and North India–specific regional knowledge for central exams, and any content exceeding ~10% English code-mixing or relying on English-medium textbook conventions will be inaccessible to the target Hindi-medium student, creating construct-irrelevant variance. |
| IF | LOWER | The deployment is text-only in Hindi, which matches MILU's text-based input modality; the high-resource Hindi language and standard script (Devanagari) raise no signal-distribution concerns. |
| OO | HIGH | MILU scores MCQ label accuracy, but the deployment requires the model to produce an explanatory rationale in Hindi alongside a correct/incorrect verdict; this is a fundamental mismatch between the benchmark's output ontology and the deployed task. |
| OC | MODERATE | MILU questions were sourced from actual competitive exam papers (objective ground truth), which reduces label-correctness risk; however, explanatory feedback quality — which is what the deployment actually delivers — is not covered by the benchmark's annotation at all, leaving OC partially unassessed. |
| OF | HIGH | The benchmark outputs are MCQ labels, whereas the deployment requires open-ended explanatory feedback in Hindi; this format mismatch means benchmark scores cannot directly validate whether the model's Hindi-language explanations are accurate, coherent, or pedagogically appropriate for the target student. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Findings tagged CRITICAL
should be treated as strong evidence for lower scores on the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Hindi configuration)
**Analysis date:** 2025-01-31
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Dimension |
|----|---------|-----------|-------|---------|-----------|
| D1 | MILU/Hindi | All 245 | is_translated=True | Every single example in the 245-item sample has `is_translated: True` | IC |
| D2 | MILU/Hindi | Ex.69 | option2 (Chemistry) | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल / (b) केवल / (c) केवल" — options reference unlisted items (a)(b)(c) | IC/IF |
| D3 | MILU/Hindi | Ex.86 | option2 (Sociology) | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, C और E / केवल A, B, D और E" — options reference state list not present in question | IC/IF |
| D4 | MILU/Hindi | Ex.56 | option2 (Chemistry) | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें... (1) और (2) केवल" — numbered statements absent from question text | IC/IF |
| D5 | MILU/Hindi | Ex.94 | option4 (Chemistry) | "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? केवल a, d / केवल b, c" — lettered reactions not shown | IC/IF |
| D6 | MILU/Hindi | Ex.95 | option1 (Sports) | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं" — sentences B-F completely absent | IC/IF |
| D7 | MILU/Hindi | Ex.106 | option2 (Chemistry) | "निम्नलिखित पदार्थों को...कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4 / 4 2 3 1" — numbered substances not named in question | IC/IF |
| D8 | MILU/Hindi | Ex.110 | option4 (Agriculture) | "राष्ट्रीय खाद्य सुरक्षा मिशन... (a) राष्ट्रीय खाद्य सुरक्षा मिशन एक फसल विकास योजना है। (b)..." — this item actually includes statements, appears intact | IF |
| D9 | MILU/Hindi | Ex.135 | option3 (Politics) | Option 4 reads "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें" — option4 is a meta-instruction, not an answer | IF |
| D10 | MILU/Hindi | Ex.137 | option4 (Politics) | "ग्राम सभा क्या है: (ख) और (ग) केवल / (ग) और (घ) केवल" — options reference lettered list absent from question | IC/IF |
| D11 | MILU/Hindi | Ex.118 | option2 (Language) | "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें" — no idiom/मुहावरा is given in the question text | IC/IF |
| D12 | MILU/Hindi | Ex.152 | option1 (Language) | "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए सबसे उपयुक्त विकल्प चुनें" — no sentence or underlined portion present | IC/IF |
| D13 | MILU/Hindi | Ex.151 | option1 (Economics) | "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं... कौन सा तर्क मजबूत है?" — statement and arguments completely missing | IC/IF |
| D14 | MILU/Hindi | Ex.143 | option4 (Logical Reasoning) | "निम्नलिखित शब्दों को तार्किक और अर्थपूर्ण क्रम में व्यवस्थित करें: 3,1,5,2,4 / 5,2,3,1,4" — words to order are absent | IC/IF |
| D15 | MILU/Hindi | Ex.145 | option2 (Logical Reasoning) | "कौन सा अक्षर समूह प्रश्न चिह्न (?) को बदलकर दी गई श्रृंखला को पूरा करेगा?" — no series is provided | IC/IF |
| D16 | MILU/Hindi | Ex.188 | option3 (Education) | "नई शिक्षा नीति 2020 में देखा गया है कि... निम्नलिखित में से किन समस्याओं का सामना कर रही है? केवल (a) / केवल (b) / उपरोक्त सभी" — problems (a)(b) not listed | IC/IF |
| D17 | MILU/Hindi | Ex.201 | option4 (Computer Science) | "निम्नलिखित में से कौन सा कथन BIOS के संदर्भ में सही है? केवल I और II / केवल I और III / सभी कथन सही हैं" — statements I, II, III absent | IC/IF |
| D18 | MILU/Hindi | Ex.222 | option2 (Business) | "2022 में फॉर्च्यून 500 सूची में भारतीय कंपनियों के संबंध में निम्नलिखित पर विचार करें: A, B, C और D केवल" — items A-E not enumerated | IC/IF |
| D19 | MILU/Hindi | Ex.7 | option2 (Literature) | "विलियम वर्ड्सवर्थ _________ के कवि हैं" — tests knowledge of English poet; India-relevance absent | IC |
| D20 | MILU/Hindi | Ex.76 | option2 (Language) | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" — English word 'Didactic' asked in Hindi; tests English vocabulary | IC |
| D21 | MILU/Hindi | Ex.90 | option3 (Language) | "शब्द 'grim' का पर्यायवाची लिखें" — English word 'grim' asked in Hindi question | IC |
| D22 | MILU/Hindi | Ex.105 | option4 (Language) | "निर्देश: निम्नलिखित प्रश्न में... शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है... Evangelize" — English word tested in Hindi | IC |
| D23 | MILU/Hindi | Ex.9 | option3 (Language Studies) | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा..." — tests Hindi grammar (indirect speech) directly relevant to deployment | IC/IO |
| D24 | MILU/Hindi | Ex.51 | option2 (Language Studies) | "दिए गए वाक्य का सही सक्रिय रूप चुनें" — active/passive voice in Hindi | IO |
| D25 | MILU/Hindi | Ex.74 | option4 (Economics) | "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी? 7.1 प्रतिशत" — specific historical data point (2018) | OC |
| D26 | MILU/Hindi | Ex.2 | option2 (Sports) | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" | OC |
| D27 | MILU/Hindi | Ex.88 | option1 (Physics) | "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान एक क्षुद्रग्रह पर उतरा... रयुगु" | OC |
| D28 | MILU/Hindi | Ex.242 | option4 (Arts) | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है... चिकनकारी" — UP-specific cultural craft content | IC |
| D29 | MILU/Hindi | Ex.26 | option2 (Earth Sciences) | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — UP-specific geography content | IC |
| D30 | MILU/Hindi | Ex.68 | option2 (Geography) | "राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है?" — Rajasthan state-level content | IC |
| D31 | MILU/Hindi | Ex.193 | option3 (Arts) | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" — Rajasthan state-level cultural content | IC |
| D32 | MILU/Hindi | Ex.115 | option4 (Literature) | "'किस्सा किस्सा लखनऊवा-लखनऊ के आवामी किस्से' के लिए साहित्य अकादमी युवा पुरस्कार 2021" — UP/Lucknow literary content | IC |
| D33 | MILU/Hindi | Ex.28 | option2 (Sociology) | "खेरवार आंदोलन के नेता — भागीरथ मांझी" — Jharkhand/tribal movement, less central-exam prominent | IC |
| D34 | MILU/Hindi | Ex.83 | option1 (Sociology) | Complex ethics scenario about senior civil officer, tribal displacement, old-age home; very long UPSC-style case | IO |
| D35 | MILU/Hindi | Ex.170 | option2 (Business) | "कपड़ा दुकान के मालिक ने क्या खरीदा? कैलकुलेटर" — decontextualized; passage/context missing | IC/IF |
| D36 | MILU/Hindi | Ex.36 | option3 (Logical Reasoning) | "TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______" — letter series with Roman characters in Hindi question | IC |
| D37 | MILU/Hindi | Ex.52 | option2 (History) | "सुंदर पांड्यन — पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया" — South Indian dynasty, less prominent in UPSC Hindi prep | IC |
| D38 | MILU/Hindi | Ex.109 | option4 (Politics) | "छत्तीसगढ़ में नगरपालिकाओं के सभी चुनावों के संचालन के लिए... अनुच्छेद 243 (ख)..." — state-specific (Chhattisgarh) content | IC |
| D39 | MILU/Hindi | Ex.200 | option4 | Correct answer for "पितृसत्तात्मक परिवार" labels patriarchal family; accepted factual answer | OC |

---

### Findings

#### CRITICAL

#### Finding CRITICAL1: Systematic Missing Content in Translated Items — Questions Reference Absent Lists, Statements, and Passages

- **Dimension(s):** IC, IF
- **Observation:** A substantial minority of the 245 sampled items (approximately 15–20 items identified) contain questions that explicitly instruct the model/student to evaluate "the following statements," "the following items (a, b, c, d)," "the given sentence," or "the given idiom" — but the referenced content is entirely absent from the question field. The answer options reference these missing elements (e.g., "केवल A और B," "केवल 1 और 3," "AEDBCF"). This renders the items unanswerable without the original source material, and a model's correct response would be chance-level or based on residual training knowledge rather than the provided content. This pattern appears across multiple subjects including Chemistry, Sociology, Language Studies, Logical Reasoning, Computer Science, and Economics.
- **Potential concern for deployment:** For a system evaluating Hindi-medium students preparing for central competitive exams, these items represent a fundamental data integrity failure. If a model "correctly" answers these questions, it demonstrates memorization of the answer from training data rather than reasoning from presented content — precisely the behavior this benchmark cannot differentiate. Benchmark accuracy scores on these items are not interpretable, inflating or deflating performance measures for the deployment use case in a non-reproducible way.
- **Datapoint citations:**
  - [D2] Example 69 (MILU/Hindi, split=validation, label=option2, Chemistry): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल / (b) केवल / (c) केवल" — options reference items (a)(b)(c) not present in question.
  - [D3] Example 86 (MILU/Hindi, split=validation, label=option2, Sociology): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, C और E" — states A–E never enumerated.
  - [D4] Example 56 (MILU/Hindi, split=validation, label=option2, Chemistry): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें... (1) और (2) केवल" — four statements entirely absent.
  - [D5] Example 94 (MILU/Hindi, split=validation, label=option4, Chemistry): "कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? केवल a, d" — reactions a–d not shown.
  - [D6] Example 95 (MILU/Hindi, split=validation, label=option1, Sports): "वाक्यों B, C, D और E को तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं" — sentences B–F entirely absent.
  - [D7] Example 106 (MILU/Hindi, split=validation, label=option2, Chemistry): "निम्नलिखित पदार्थों को कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4 / 4 2 3 1" — substances 1–4 unnamed.
  - [D10] Example 137 (MILU/Hindi, split=validation, label=option4, Politics): "ग्राम सभा क्या है: (ख) और (ग) केवल / (ग) और (घ) केवल" — definitions (क)(ख)(ग)(घ) absent.
  - [D11] Example 118 (MILU/Hindi, split=validation, label=option2, Language): "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें" — no idiom appears in question.
  - [D12] Example 152 (MILU/Hindi, split=validation, label=option1, Language): "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए..." — no sentence provided.
  - [D13] Example 151 (MILU/Hindi, split=validation, label=option1, Economics): "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं... कौन सा तर्क मजबूत है?" — statement and arguments not present.
  - [D14] Example 143 (MILU/Hindi, split=validation, label=option4, Logical Reasoning): "निम्नलिखित शब्दों को तार्किक और अर्थपूर्ण क्रम में व्यवस्थित करें" — words to order absent.
  - [D15] Example 145 (MILU/Hindi, split=validation, label=option2, Logical Reasoning): "कौन सा अक्षर समूह...दी गई श्रृंखला को पूरा करेगा?" — series not provided.
  - [D16] Example 188 (MILU/Hindi, split=validation, label=option3, Education): "निम्नलिखित में से किन समस्याओं का सामना कर रही है? केवल (a) / केवल (b)" — problems (a)(b) not listed.
  - [D17] Example 201 (MILU/Hindi, split=validation, label=option4, Computer Science): "BIOS के संदर्भ में सही है? केवल I और II" — statements I, II, III absent.
  - [D18] Example 222 (MILU/Hindi, split=validation, label=option2, Business): "फॉर्च्यून 500 सूची में... A, B, C और D केवल" — items A–E not enumerated.

---

#### Finding CRITICAL2: Option-as-Meta-Instruction Format Corruption

- **Dimension(s):** IF, OC
- **Observation:** At least one item has an answer option that is a meta-instruction rather than a substantive answer choice. Example 135, option4 reads "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें" ("Select the correct answer using the code given below") — this is a formatting artifact from a multi-step MCQ format (common in UPSC Prelims) where the original question provided a numbered code table, but the code table has been stripped during dataset processing. The correct answer is option3, meaning a student must choose from options that include one non-answer.
- **Potential concern for deployment:** This indicates systematic stripping of table/code structures during competitive exam scraping and dataset formatting. For central-exam competitive preparation (UPSC GS Paper I heavily uses "which of the following statements is/are correct?" with code tables), this format corruption is particularly consequential: the exact item types most representative of UPSC Prelims are the ones most likely to be corrupt in this dataset.
- **Datapoint citations:**
  - [D9] Example 135 (MILU/Hindi, split=validation, label=option3, Politics and Governance): Option4 = "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें" — a formatting directive appearing as an answer choice, indicating the code table (1/2 only, 2/3 only, etc.) was stripped.

---

#### MAJOR

#### Finding MAJOR1: 100% of Sampled Validation Items Are Machine-Translated from English

- **Dimension(s):** IC, IF
- **Observation:** Every single one of the 245 sampled validation examples carries `is_translated: True`. The benchmark documentation states that only ~25% of released questions are translated, and the remainder are natively sourced. However, the entire validation split sample reviewed here is 100% translated. This is either a property of the validation split specifically (which may have been populated disproportionately with translated items) or a sampling artifact. Either way, any few-shot evaluation using this validation set as the source of in-context examples will expose models exclusively to translated content as exemplars.
- **Potential concern for deployment:** For Hindi-medium competitive exam students, the register and phrasing of natively sourced Hindi exam questions differs substantially from machine-translated content. If few-shot examples are drawn from this validation split (as documented in Q51), models are being primed with translated Hindi that may not reflect the register of actual competitive exam question language. This is a potential construct-irrelevant variance source for deployment evaluation.
- **Datapoint citations:**
  - [D1] All 245 examples (MILU/Hindi, split=validation): `is_translated: True` — 245/245 items in sample are translated from English; no natively sourced Hindi validation items appear in this sample.

---

#### Finding MAJOR2: English Vocabulary Testing Within Hindi Language Studies Items — Exceeds 10% Code-Mixing Threshold

- **Dimension(s):** IC
- **Observation:** Several Language Studies items in the Hindi configuration test vocabulary knowledge of English words directly, asking Hindi-medium students to define English terms like "Didactic," "grim," and "Evangelize." These are not technical terms with standard Hindi equivalents but English literary/rhetorical vocabulary. Additionally, Logical Reasoning items use Roman-alphabet letter sequences (e.g., "TAB, TTZBB, TTBBB..." in Example 36) embedded in Hindi text. While some code-mixing with English technical terms is acceptable per the deployment specification (~10% ceiling), items that require knowledge of English literary vocabulary as the *core* assessment construct go beyond incidental code-mixing.
- **Potential concern for deployment:** Hindi-medium competitive exam aspirants preparing for UPSC/SSC are assessed on Hindi language proficiency (Hindi grammar, idiom, comprehension) not English vocabulary recognition. Items testing "Didactic," "grim," or "Evangelize" definitions create construct-irrelevant difficulty for this population: failure represents English vocabulary deficit, not Hindi language knowledge deficit. This is a direct IC validity concern for the target student population.
- **Datapoint citations:**
  - [D20] Example 76 (MILU/Hindi, split=validation, label=option2, Language Studies): "'डिडैक्टिक' शब्द का अर्थ क्या है? / नैतिक पाठ पढ़ाना" — English word 'Didactic' is the core test construct.
  - [D21] Example 90 (MILU/Hindi, split=validation, label=option3, Language Studies): "शब्द 'grim' का पर्यायवाची लिखें" — 'grim' is an English word; the question tests English synonym knowledge.
  - [D22] Example 105 (MILU/Hindi, split=validation, label=option4, Language Studies): "शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है... Evangelize / उपदेश देना" — English word tested.
  - [D36] Example 36 (MILU/Hindi, split=validation, label=option3, Logical Reasoning): "TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______" — Roman letter series embedded in Hindi question.

---

#### Finding MAJOR3: Output Ontology Fundamental Mismatch — MCQ Label Scoring Cannot Validate Hindi Explanatory Rationale

- **Dimension(s):** OO, OF
- **Observation:** All 245 sampled items follow the MCQ format with a single correct answer and `target` field specifying one of four options. The benchmark provides no rationale, explanation, or annotation of *why* an answer is correct. The deployment requires the AI system to return both a correct/incorrect label *and* a substantive Hindi-language explanation of why the answer is right or wrong.
- **Potential concern for deployment:** MILU benchmark accuracy scores measure only label selection correctness, not explanation quality. A model that achieves high accuracy on MILU MCQs may generate factually incorrect, incoherent, or pedagogically unhelpful Hindi explanations for the same questions. This is a fundamental output form mismatch: benchmark scores cannot be used to validate the deployment's core output, and no proxy measure for explanation quality exists within the benchmark infrastructure. This was anticipated in documentation but the sampled data confirms there is zero annotation supporting rationale assessment.
- **Datapoint citations:**
  - [D2]–[D18]: All examples — none contain a rationale field, explanation, or annotation of reasoning. The `target` field specifies only which option letter is correct. For instance, Example 83 [D34] presents a complex multi-paragraph civil services ethics scenario whose correct answer (option1) requires nuanced reasoning about tribal rights and official duties, yet no explanation is provided in the dataset.

---

#### Finding MAJOR4: Current Affairs Items Are Temporally Dated — Knowledge Currency Risk for Central Exam Deployment

- **Dimension(s):** OC
- **Observation:** Multiple Current Affairs and GK items reference specific events from 2018–2022 that are time-bound fact questions. Examples include India's GDP growth rate for July–September 2018 (Ex.74), the 2020 Archery Asia Cup gold medals won by India (Ex.2), the 2019 Japanese asteroid mission Ryugu (Ex.88), the 2020 Minister of Women and Child Development (Ex.132 — as of 2018), and the 2022 ASSOCHAM President (Ex.123 — December 2020). For a deployment targeting students preparing for current UPSC/SSC exams (2024–2026), questions testing 2018–2022 Current Affairs have limited validity for the "Current Affairs" domain.
- **Potential concern for deployment:** Current Affairs is a top-priority domain for UPSC/SSC/banking exam preparation. Students preparing for 2025–2026 exams need current knowledge; a benchmark evaluating 2018–2022 events cannot validly measure Current Affairs preparedness for the deployment cohort. Model performance on these items may also be inflated due to training data contamination (these events were well-covered in pre-training corpora).
- **Datapoint citations:**
  - [D25] Example 74 (MILU/Hindi, split=validation, label=option4, Economics): "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी? 7.1 प्रतिशत" — 2018 economic data.
  - [D26] Example 2 (MILU/Hindi, split=validation, label=option2, Sports): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022..." — 2022 sports event.
  - [D27] Example 88 (MILU/Hindi, split=validation, label=option1, Physics): "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान... रयुगु" — 2019 space event.

---

#### Finding MAJOR5: Subject Distribution Skewed Toward Engineering/Technology — Mismatch With Central Exam Priority Subjects

- **Dimension(s):** IO
- **Observation:** Among the 245 sampled validation items, there is a notably high concentration of Engineering & Technology domain items (approximately 45–50 items, roughly 18–20% of the sample). These cover topics like DC motor behavior (Ex.1), Half-Wave Rectifiers (Ex.3), Transformer types (Ex.4), AM modulation bandwidth (Ex.16), TDM frame rates (Ex.47), and chopper circuits (Ex.160). Engineering and technical content of this specificity is not tested in UPSC Prelims, SSC CGL, or banking exams. By contrast, Mathematics/Quantitative Aptitude — a top-priority subject for SSC and banking exams — appears to have very limited representation (only the compound interest problem Ex.84 and the weighted average Ex.120 are clearly quantitative aptitude items).
- **Potential concern for deployment:** The deployment targets UPSC, SSC, and banking exam preparation. For SSC CGL and IBPS PO, Quantitative Aptitude is a major paper; for UPSC, General Science (not advanced engineering) is tested. The overrepresentation of advanced Engineering content and underrepresentation of Mathematics/Quantitative Aptitude in this sample suggests the Hindi MILU subset may not adequately cover the most critical subject areas for the central exam deployment.
- **Datapoint citations:**
  - [D2], [D3] above plus: Example 1 (DC series motor — Engineering), Example 3 (Half-wave rectifier — Engineering), Example 4 (Transformer type — Engineering), Example 16 (AM bandwidth — Technology), Example 38 (Form factor — Engineering), Example 47 (TDM frame rate — Technology), Example 49 (Ampere's law — Physics/Engineering), Example 160 (Chopper circuit — Engineering) — approximately 18–20% of sample is advanced Engineering/Technology content not tested in UPSC/SSC/banking exams.
  - [D34] Example 83 (Sociology — Ethics case): Complex civil services ethics scenario; UPSC-style but appears only once in sample vs. numerous engineering items.

---

#### MINOR

#### Finding MINOR1: South India–Specific Content Present in Hindi-Language Items

- **Dimension(s):** IC
- **Observation:** Several items in the Hindi configuration specifically test knowledge of South Indian states, dynasties, cultural works, or current affairs not typically emphasized in central exam preparation from a North Indian Hindi-medium perspective. Examples include: the Pandya king who extended the empire to the Kaveri (Ex.52), Tamil magazine cartoon history (Ex.108), the classical Tamil epic "Silappatikaram" (Ex.232), Kota painting school period (Ex.193 — Rajasthan, North India-relevant), and Bhanda Pather theater of J&K (Ex.48). While some such items appear in UPSC GS, the framing and depth suggest sourcing from South Indian or regional state-level exams.
- **Potential concern for deployment:** Hindi-medium students from North India preparing for central exams would encounter UPSC-standard questions about South India, but questions with very fine-grained knowledge about South Indian literary/historical figures (Sundar Pandyan, Tamil epic authorship, Tamil magazine cartoons) may reflect South Indian regional exam content rather than central exam scope. This is a moderate concern for content validity.
- **Datapoint citations:**
  - [D37] Example 52 (MILU/Hindi, split=validation, label=option2, History):

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
  "benchmark": "MILU",
  "region": "Hindi-Medium Competitive Exam Aspirants — North India (Central Exams)",
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
