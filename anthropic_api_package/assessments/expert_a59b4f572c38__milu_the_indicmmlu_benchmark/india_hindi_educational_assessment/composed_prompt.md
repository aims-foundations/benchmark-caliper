I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **MILU: A Multi-task Indic Language Understanding Benchmark** is valid for use in **North India Hindi-Medium Postgraduate Teacher — MCQ Assessment**.

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
name: North India Hindi-Medium Postgraduate Teacher — MCQ Assessment
abbreviation: NI-HI-PG-TEACHER
benchmark: MILU
assessment_slug: milu-north-india-hindi-pg-teacher
population_description: Postgraduate- or PhD-qualified teachers operating in Hindi-medium
  educational institutions across the Hindi belt of North India (principally Uttar
  Pradesh, Madhya Pradesh, Rajasthan, and Bihar, with adjacent regions). These educators
  use an LLM-powered mobile or enterprise application to evaluate student responses
  to multiple-choice questions, assign scores under a positive/negative marking scheme,
  and deliver binary correct/incorrect judgements. They work across all Hindi state
  board syllabi (UP Board, MP Board, Rajasthan Board, Bihar Board) and the central
  CBSE board; English-medium board content is in scope only when translated into Hindi
  and aligned to Hindi-board norms.
geography:
  country: India
  region: North India — Hindi Belt
  primary_states:
  - Uttar Pradesh
  - Madhya Pradesh
  - Rajasthan
  - Bihar
  adjacent_states_in_scope:
  - Uttarakhand
  - Jharkhand
  - Chhattisgarh
  - Haryana
  - Delhi NCT
  urbanization_note: 'Target population spans both urban centres (Lucknow, Bhopal,
    Jaipur, Patna) and semi-urban/peri-urban towns where state-board institutions
    predominate. Rural postgraduate teachers are a minority but present. [NEEDS VERIFICATION
    — deferred: below search budget; rural vs. urban share of PG-qualified teachers
    by state requires UDISE+ or state education department data not available in general
    search results]'
target_role:
  occupation: Secondary or higher-secondary school teacher; university or college
    lecturer
  qualification_floor: Postgraduate degree (MA/MSc/MCom minimum); PhD holders also
    within scope
  experience_range_years: 0–20+
  subject_domains:
  - Hindi language and literature
  - Social sciences (history, civics, geography, economics)
  - Sciences (physics, chemistry, biology) — when in Hindi medium
  - Mathematics
  - General knowledge and current affairs (competitive exam prep)
  institutional_affiliations:
  - UP Board (Uttar Pradesh Madhyamik Shiksha Parishad)
  - MP Board (Madhya Pradesh Board of Secondary Education)
  - Rajasthan Board (RBSE)
  - Bihar Board (BSEB)
  - CBSE (Central Board of Secondary Education)
  - State universities and degree colleges affiliated to universities in UP, MP, Rajasthan,
    Bihar
  note: 'Teachers in this cohort are expected to hold TET/CTET certification or equivalent
    state eligibility credentials. [NEEDS VERIFICATION — deferred: proportion holding
    CTET vs. state TET vs. neither by state; likely unsearchable without DISE/state
    recruitment board data]'
languages:
  primary: Hindi (Modern Standard Hindi / Khari Boli; Devanagari script)
  register_expected: Formal/standard academic register consistent with state-board
    and CBSE examination language; pan-India formal Khari Boli rather than local colloquial
    varieties
  regional_variety_note: 'Teachers and students in UP, Bihar, and Rajasthan may be
    exposed to local dialectal influences (Awadhi, Bhojpuri, Maithili, Rajasthani/Marwari)
    in everyday speech, but the academic register used in board examinations and MCQ
    items is expected to be standard Khari Boli. Subtle lexical or orthographic deviations
    from pan-India formal Hindi in benchmark items could create a minor but non-trivial
    familiarity gap. [NEEDS VERIFICATION — deferred: likely unsearchable (lived academic
    practice); no published corpus study of lexical divergence between state-board
    question-paper Hindi and standard Khari Boli was found]'
  secondary_languages:
  - English (passive reading for translated content; not primary medium)
  - Sanskrit (relevant for Hindi literature items referencing classical texts)
  minority_or_contact_languages_in_region:
  - Awadhi (UP)
  - Bhojpuri (eastern UP, Bihar)
  - Maithili (Bihar — also Eighth Schedule language)
  - Bundeli (MP)
  - Rajasthani / Marwari dialects (Rajasthan)
  note: These contact languages do not appear in the deployment interface or benchmark
    items, but they inform the cultural and literary background knowledge teachers
    bring (e.g., familiarity with Tulsidas's Awadhi, Kabir's Sadhukkadi).
writing_systems:
  scripts:
  - Devanagari (primary — all Hindi MCQ items and student responses)
  - Latin (marginal — English-origin proper nouns, translated content labels)
  note: 'Devanagari is a left-to-right abugida. Hindi NLP tooling for Devanagari is
    well-developed relative to other Indic scripts, making this a high-resource script-language
    pairing. No RTL or bidirectional rendering issues apply. Unicode normalization
    (NFC vs. NFD; nukta handling) can introduce subtle tokenization variation. [NEEDS
    VERIFICATION — deferred: whether MILU applies consistent Unicode normalization
    across its Hindi item set; low impact for scoring given MILU''s documented Unicode-based
    filtering step (Q34)]'
literacy_and_digital_access:
  population_literacy: 'Per 2011 Census (most recent official census): UP 67.7%, Bihar
    61.8%, Rajasthan 66.1%, MP 70.6% — all below the national average of 74%. NSO
    Periodic Labour Force Survey 2023-24 estimates show improvement: Rajasthan ~69.7%,
    Bihar ~70.9%; a full 2021 Census has not yet been released. These states contain
    approximately 48% of India''s illiterate population. Note: these are general population
    figures; the postgraduate teacher cohort is effectively 100% literate. Source:
    Census 2011 / Scroll.in summary — [WEB-1];
    NSO PLFS 2023-24 summary — [WEB-2]'
  teacher_cohort_literacy: Postgraduate-qualified by definition; effectively 100%
    literate in Hindi and functionally literate in English
  smartphone_penetration_general: 'Internet penetration in the Hindi-belt states lags
    the national average (58% in 2024). Bihar (~25%) and UP (~30%) have among the
    lowest state-level internet penetration rates. By absolute subscriber count, UP
    (73.59M) and Bihar (69.89M) rank among the top five telecom circles by total internet
    subscribers as of September 2023, reflecting large populations rather than high
    per-capita rates. Source: muftinternet.com 2024 summary — [WEB-3];
    Wikipedia/TRAI data — [WEB-4]'
  internet_access_teacher_cohort: 'Expected to be high among postgraduate teachers
    in urban/semi-urban settings; rural connectivity more variable. Internet usage
    is highest among individuals with a college degree or higher (NFHS-5 data). [NEEDS
    VERIFICATION — deferred: proportion of government school teachers in Hindi-belt
    states with reliable mobile data access; requires UDISE+ or state survey data
    not in general search results]'
  device_profile: 'Predominantly Android smartphones; enterprise desktop/laptop access
    variable by institution type. India is projected to reach 1 billion smartphone
    users by 2026 with rural areas driving adoption (Deloitte 2022 report). [NEEDS
    VERIFICATION — deferred: device distribution specifically among government vs.
    private school teachers in Hindi-belt states; below search budget]'
  infrastructure_note: '4G/LTE coverage is widespread in urban UP, MP, Rajasthan,
    Bihar; rural and small-town coverage improving but not universal. Low-bandwidth
    conditions may affect enterprise application responsiveness. UP and Bihar have
    among the largest total internet subscriber bases in India but lowest per-capita
    penetration, indicating significant urban-rural divide. Source: Wikipedia Internet
    in India — [WEB-4]'
curricular_scope:
  boards_in_scope:
  - board: UP Board (Uttar Pradesh Madhyamik Shiksha Parishad)
    abbreviation: UPMSP
    coverage_notes: 'Largest single board in India by enrolment. Hindi is the primary
      medium. Syllabus emphasises Hindi literature (Tulsidas, Premchand, Mahadevi
      Verma), regional history, and civics. [NEEDS VERIFICATION — deferred: current
      UP Board syllabus structure for Classes 9–12 in detail; authoritative source
      would be UPMSP official portal upmsp.edu.in]'
  - board: MP Board (Madhya Pradesh Board of Secondary Education)
    abbreviation: MPBSE
    coverage_notes: '[NEEDS VERIFICATION — deferred: current MP Board Hindi syllabus
      scope and canonical texts; low impact for scoring relative to MILU gap analysis]'
  - board: Rajasthan Board of Secondary Education
    abbreviation: RBSE
    coverage_notes: '[NEEDS VERIFICATION — deferred: current RBSE Hindi syllabus;
      regional history emphasis (Maharana Pratap, Rani Padmini); low impact for scoring]'
  - board: Bihar School Examination Board
    abbreviation: BSEB
    coverage_notes: '[NEEDS VERIFICATION — deferred: current Bihar Board Hindi syllabus;
      Maithili/Bhojpuri-region canonical texts in scope; low impact for scoring]'
  - board: CBSE (Central Board of Secondary Education)
    abbreviation: CBSE
    coverage_notes: 'Pan-India board; Hindi-medium CBSE items are in scope. CBSE Hindi
      syllabus (Classes 9–12) includes prescribed texts from NCERT. NCERT released
      updated textbooks for Classes 3 and 6 in 2024 as part of NEP 2020 implementation;
      updates for Classes 4, 5, 7, 8 planned for 2025–26, meaning syllabus currency
      is actively shifting. Source: iDream Education NEP/NCERT post — [WEB-5].
      [NEEDS VERIFICATION — deferred: CBSE Hindi course A vs. course B scope; NCERT
      prescribed text list current edition for Classes 9–12]'
  english_medium_board_content: Translated English-medium board questions (CBSE English,
    ICSE) are in deployment scope only when rendered in Hindi and aligned to Hindi-board
    norms. Translation adequacy for subject-specific terminology (science, economics)
    in North Indian academic register is an unverified assumption. [NOT FOUND — searched
    for validated Hindi translation of CBSE/ICSE MCQ item banks; no published benchmark
    or validation study for translated CBSE/ICSE Hindi MCQ content targeting North
    Indian academic register was found]
  university_level: 'Degree college and university undergraduate MCQs (for institutions
    affiliated to state universities such as University of Lucknow, BHU, University
    of Rajasthan, Patna University) are potentially in scope for postgraduate teacher
    use. [NEEDS VERIFICATION — deferred: whether the deployment application is explicitly
    targeting school board or also university board contexts; below search budget]'
assessment_format:
  question_type: Multiple-choice questions (MCQ) — single correct answer per item
  answer_options: Up to four options (A, B, C, D)
  scoring_scheme: 'Positive/negative marking: positive marks awarded for correct selection;
    negative marks deducted for incorrect selection; no marks for unanswered items
    (convention may vary by board). MPPSC Prelims applies one-third negative marking
    for wrong answers (confirmed). BPSC Prelims is 150-mark MCQ paper. [NOT FOUND
    — no consolidated published source for the standard negative marking fraction
    specifically across all four Hindi-belt state boards'' MCQ sections and CBSE MCQ
    assessments; MPPSC one-third negative marking confirmed (Drishti IAS — [WEB-6]);
    other boards require direct official portal verification]'
  partial_credit: Not applicable — binary correct/incorrect judgement only
  rubric_based_feedback: Not applicable for this deployment
  output_language_register: Hindi (formal/standard Khari Boli Devanagari); scoring
    rationale if provided should match the academic register familiar to state-board
    teachers
culturally_specific_content:
  canonical_hindi_literary_figures:
  - Tulsidas (Ramcharitmanas — Awadhi, but canonical in UP Board Hindi literature
    curriculum)
  - Premchand (fiction; Godaan, Nirmala — core CBSE and state board texts)
  - Kabir (dohas — Sadhukkadi register; canonical across boards)
  - Mahadevi Verma (Chhayavaad poetry)
  - Jaishankar Prasad (Kamayani)
  - Suryakant Tripathi 'Nirala'
  - Ramdhari Singh Dinkar (Rashtriya Kavita tradition)
  - Munshi Premchand (short stories — Panch Parmeshwar, Idgah)
  canonical_regional_historical_figures:
  - Rani Lakshmibai of Jhansi (UP history)
  - Chandrashekhar Azad (UP; freedom movement)
  - Bhagat Singh (referenced across boards)
  - Maharana Pratap (Rajasthan Board emphasis)
  - Birsa Munda (Jharkhand/Bihar overlap)
  - Dr. B.R. Ambedkar (constitution; CBSE and state boards)
  framing_risk: Competitive-exam (UPSC/SSC) framing of canonical figures often emphasises
    administrative/general-knowledge angles; school-board framing emphasises literary-critical
    or regional-patriotic angles. MILU items sourced from civil services exams may
    not match the pedagogical framing familiar to state-board teachers. [NOT FOUND
    — no item-level framing analysis for MILU Arts & Humanities Hindi items has been
    published; the MILU paper confirms models perform worst in Arts & Humanities and
    Social Sciences (Q20, Q71) but does not report item-level framing analysis]
  religious_and_cultural_context: Hindu religious texts (Ramcharitmanas, Bhagavad
    Gita excerpts) appear in Hindi board literature syllabi as literary — not doctrinal
    — content. Items touching religious themes should be evaluated for framing consistency
    with secular board syllabus norms.
  civic_and_governance_content: Items on Indian Constitution, Panchayati Raj, state
    governance structures, and fundamental rights are standard in Social Sciences
    MCQs across all boards. Regional governance nuances (e.g., UP panchayat structure
    vs. national framework) may produce locally specific correct answers.
benchmark_language_alignment:
  benchmark_hindi_resource_level: 'High-resource — Hindi is a major Indic language
    with substantial NLP tooling. Notably, Hindi ranks only 62nd by number of Wikipedia
    articles despite being the world''s third most-spoken language, indicating a significant
    gap between spoken prevalence and online documentation. Source: Analysis of Indic
    Language Capabilities arXiv 2501.13912 — [WEB-7]'
  script_match: Full — both benchmark and deployment use Devanagari
  register_match: Presumed formal Khari Boli in MILU; consistent with deployment expectation.
    MILU treats Hindi as a single homogeneous language variety with no documented
    register variation across its items. [NOT FOUND — no published study documents
    register variation specifically within MILU's Hindi item set; the MILU paper applies
    Unicode-based filtering and INDICLID for script correctness (Q34) but does not
    address register standardisation]
  translated_proportion: 'Approximately 25% of MILU questions are translated from
    English into Hindi using GPT-4O rather than a specialist translation model (Q44,
    Q45, Q47). Note: the MILU GitHub repository now reports approximately 85,000 total
    questions (vs. ~79K in the published paper), suggesting the dataset has been updated
    post-publication. Source: GitHub AI4Bharat/MILU — [WEB-8]'
  state_source_distribution: '[NOT FOUND — confirmed absent: MILU reports state civil
    services exams as a source category (Table 8, Q97) and explicitly values regional
    exams for local knowledge (Q28), but provides no per-state breakdown of Hindi-language
    item counts for UPPSC, MPPSC, RPSC, or BPSC. The published paper, GitHub repository,
    and Hugging Face dataset card all lack this granularity. This is a full documentation
    gap confirmed by search. Source: arXiv 2411.02538 — [WEB-9];
    GitHub — [WEB-8]]'
exam_source_landscape:
  national_exams_likely_in_milu:
  - UPSC Civil Services Preliminary (Hindi medium)
  - SSC CGL / SSC CHSL (Hindi medium items)
  - NDA / CDS (Hindi medium items)
  - CTET / TET (Hindi language paper)
  state_exams_likely_in_milu:
  - exam: UPPSC (Uttar Pradesh Public Service Commission)
    state: Uttar Pradesh
    notes: '[NOT FOUND — MILU''s Table 8 lists state civil services exams but no per-exam
      confirmation for UPPSC specifically is published. UPPSC prelims question papers
      are widely available on online exam portals (consistent with MILU''s scraping
      methodology), making inclusion plausible but unconfirmed. Source: arXiv 2411.02538
      appendix tables — [WEB-9]]'
  - exam: MPPSC (Madhya Pradesh Public Service Commission)
    state: Madhya Pradesh
    notes: '[NOT FOUND — same documentation gap as UPPSC; MPPSC prelims is a bilingual
      Hindi/English MCQ exam (confirmed), making it a plausible MILU source, but per-exam
      confirmation is absent. MPPSC prelims includes negative marking of one-third
      per wrong answer. Source: Drishti IAS MPPSC pattern — [WEB-6]]'
  - exam: RPSC (Rajasthan Public Service Commission)
    state: Rajasthan
    notes: '[NOT FOUND — same documentation gap; RPSC RAS/RTS exams are bilingual
      and MCQ-based, consistent with MILU sourcing, but unconfirmed]'
  - exam: BPSC (Bihar Public Service Commission)
    state: Bihar
    notes: '[NOT FOUND — same documentation gap; BPSC prelims is a 150-mark MCQ paper
      covering History, Geography, Polity, Economy, and Bihar-specific content (confirmed).
      Source: Sanskriti IAS BPSC pattern — [WEB-10]]'
  school_board_exams: School board annual examinations (Class 10/12) are not competitive
    exams and are unlikely to have been scraped from online exam portals that host
    civil services past papers. Their representation in MILU is unconfirmed and considered
    a gap. [NOT FOUND — no evidence that UP Board, MP Board, RBSE, or BSEB Class 10/12
    papers are included in MILU; the benchmark's design explicitly targets competitive-exam
    portals]
  note: MILU's sourcing methodology targets competitive-exam portals, creating a structural
    gap for school-board syllabus content that is not recycled through competitive
    exam formats.
domain_coverage_priority:
  high_priority_domains:
  - milu_domain: Arts and Humanities
    deployment_relevance: Highest priority — Hindi literature, cultural history, classical
      texts are core to state-board teacher assessment tasks. MILU models perform
      worst here; framing divergence between competitive-exam and school-board is
      greatest.
    gap_risk: HIGH
  - milu_domain: Social Sciences
    deployment_relevance: High priority — history, civics, geography, economics MCQs
      are standard across all Hindi-state boards. Regional historical content is a
      specific concern.
    gap_risk: MODERATE-HIGH
  - milu_domain: Law and Governance
    deployment_relevance: Moderate priority — Indian Constitution and Panchayati Raj
      topics appear in Class 9–12 social science MCQs; state-specific governance differs
      from national competitive-exam framing.
    gap_risk: MODERATE
  lower_priority_domains:
  - milu_domain: Science
    deployment_relevance: Present in Hindi-medium school boards; STEM content is more
      standardised and less susceptible to regional framing differences. MILU models
      perform better here.
    gap_risk: LOW
  - milu_domain: Engineering and Technology
    deployment_relevance: Limited relevance for school-board MCQ teacher assessment
      deployment.
    gap_risk: LOW
  - milu_domain: Business Studies
    deployment_relevance: Moderate for Class 11–12 Commerce stream Hindi-medium teachers.
    gap_risk: LOW-MODERATE
  - milu_domain: Health and Medicine
    deployment_relevance: Low for general school-board MCQ context; relevant only
      for biology sub-topics.
    gap_risk: LOW
  - milu_domain: Environmental Sciences
    deployment_relevance: Low-moderate; environmental studies is a minor component
      of school board curricula.
    gap_risk: LOW
annotator_population_notes:
  benchmark_institution: AI4Bharat / IIT Madras (Chennai, Tamil Nadu — South India)
  geographic_asymmetry: Institutional base is geographically distant from the Hindi-belt
    deployment population. Annotators' familiarity with North Indian board-specific
    canonical framings (UP Board Hindi literature, Bihar Board regional history) is
    undocumented.
  annotation_source: Primarily delegated to original exam portals (subject experts
    verify answers); internal manual audit by AI4Bharat volunteers. No annotator demographic
    breakdown published.
  severity_assessment: Moderate — user confirms evaluation schemas are broadly consistent
    across boards and competitive-exam settings, reducing severity; absence of documentation
    prevents full verification.
  translation_annotation_risk: The 25% GPT-4O-translated portion introduces label
    provenance uncertainty; no human annotators familiar with North Indian Hindi academic
    register are documented as having reviewed translated items.
flagged_gaps_summary:
- gap_id: 1
  label: Hindi state-board syllabus coverage vs. competitive-exam framing
  priority: HIGH
  dimension: Input Content
  search_outcome: 'NOT FOUND — confirmed gap. MILU explicitly sources from 40+ exam
    types including state civil services (Table 8) but provides no per-state breakdown
    for Hindi-belt states. No published study documents which specific state-board
    curricular topics appear in MILU''s Hindi Arts & Humanities items. The structural
    gap between competitive-exam and school-board framing is real but item-level verification
    is not possible without direct inspection of the dataset. Source: arXiv 2411.02538
    — [WEB-9]'
  web_search_target: MILU benchmark Hindi language items state board syllabus UP MP
    Rajasthan Bihar board coverage competitive exam vs school curriculum
- gap_id: 2
  label: Regional Hindi linguistic variation and register in benchmark items
  priority: MODERATE
  dimension: Input Form
  search_outcome: NOT FOUND — no published corpus study of register variation within
    MILU's Hindi item set. MILU applies Unicode filtering and INDICLID for script
    correctness but treats Hindi as a single variety. This gap requires direct dataset
    inspection or expert linguistic review.
  web_search_target: MILU Hindi language register variation Khari Boli formal standard
    North India dialect state board UP Bihar Rajasthan academic vocabulary
- gap_id: 3
  label: Translated English-board content aligned to North Indian Hindi register
  priority: HIGH
  dimension: Input Content
  search_outcome: 'NOT FOUND — no validated Hindi translation of CBSE/ICSE MCQ item
    banks aligned to North Indian academic register was found. The IndicMMLU-Pro benchmark
    (arXiv 2501.15747) translates MMLU-Pro into Hindi using IndicTrans2 with back-translation
    QA, but is English-origin and not school-board aligned. Source: arXiv 2501.15747
    — [WEB-11]'
  web_search_target: Hindi MCQ benchmark translated English CBSE ICSE content Devanagari
    register subject terminology validation North India academic
- gap_id: 4
  label: Sub-national state-exam source distribution for Hindi-belt states
  priority: HIGH
  dimension: Input Content
  search_outcome: 'NOT FOUND — confirmed documentation gap. MILU''s paper, GitHub
    repository, and Hugging Face dataset card all provide subject-language granularity
    but no per-state source breakdown for UPPSC, MPPSC, RPSC, or BPSC. This is a full
    gap that cannot be resolved without direct dataset audit or correspondence with
    the MILU authors. Source: GitHub AI4Bharat/MILU — [WEB-8]'
  web_search_target: MILU Hindi questions state exam source distribution UPPSC MPPSC
    RPSC BPSC Uttar Pradesh Madhya Pradesh Rajasthan Bihar proportion
- gap_id: 5
  label: Canonical Hindi literary and historical content framing (school vs. competitive
    exam)
  priority: HIGH
  dimension: Input Content
  search_outcome: NOT FOUND — no item-level framing analysis for MILU Hindi Arts &
    Humanities items has been published. The MILU paper confirms models perform worst
    in Arts & Humanities (Q20, Q71) but attributes this to training data gaps, not
    item-framing analysis. This gap requires direct dataset inspection.
  web_search_target: MILU Hindi Arts Humanities subject items Tulsidas Premchand Kabir
    Hindi literature canonical board syllabus competitive exam UPSC SSC framing
- gap_id: 6
  label: Annotator regional representativeness for North Indian Hindi-belt norms
  priority: LOWER
  dimension: Output Content
  search_outcome: NOT FOUND — no annotator demographic breakdown is published. IIT
    Madras institutional base confirmed. User elicitation reduces severity to moderate.
    No new evidence changes the scaffold assessment.
  web_search_target: MILU annotation annotator demographics North India Hindi belt
    regional representation IIT Madras AI4Bharat review team
infrastructure_notes: 'The deployment is mobile-first (Android smartphones predominant)
  with enterprise application access in larger institutions. North Indian Hindi-belt
  states have expanding 4G coverage but rural and small-town connectivity remains
  variable. Bihar (~25%) and UP (~30%) have among the lowest state-level internet
  penetration rates in India, though UP and Bihar have large absolute subscriber bases
  (73.6M and 69.9M respectively as of September 2023). The application is text-only
  (Devanagari MCQ items and binary scoring output), making it low-bandwidth by design.
  No image, audio, or video modality is involved. Source: muftinternet.com 2024 summary
  — [WEB-3];
  Wikipedia Internet in India — [WEB-4]'
domain_specific_notes:
  education_system: 'The Hindi-belt states operate under a dual-board structure: state
    boards (UP Board, MP Board, RBSE, BSEB) and CBSE. State boards historically have
    higher enrolment in rural and semi-urban areas; CBSE dominates urban private schools.
    Postgraduate teachers in state-board institutions are recruited through state
    teacher eligibility tests (TET) and public service commissions. [NEEDS VERIFICATION
    — deferred: current state TET qualification requirements by state; requires official
    state recruitment board portals]'
  mcq_culture: 'Competitive examination culture is deeply embedded in North India
    (UPSC, SSC, state PCS, bank exams). Teachers in this cohort are highly familiar
    with MCQ-format assessment from both their own qualifying examinations and classroom
    practice. Positive/negative marking is standard across all major competitive exams.
    MPPSC Prelims confirmed to apply one-third negative marking. BPSC Prelims is a
    150-mark MCQ paper. [NEEDS VERIFICATION — deferred: current UP Board / BSEB policies
    on negative marking in Class 12 MCQ sections; authoritative source would be official
    board notification portals]'
  canonical_text_alignment: A key validity concern for this deployment is whether
    MILU's Hindi items that touch canonical literary texts treat them as literary/pedagogical
    objects (appropriate for school-board teacher assessment) or as general-knowledge
    data points (appropriate for civil services exam preparation). This distinction
    affects the correctness of specific items for the deployment context.
  regulatory_context: 'National Education Policy 2020 (NEP 2020) is being implemented
    in phases nationally. NCERT released updated textbooks for Classes 3 and 6 in
    April–May 2024; updates for Classes 4, 5, 7, 8 are planned for 2025–26. Hindi-belt
    state boards (UP, MP, Bihar, Rajasthan) are implementing NEP in their own timelines
    — NEP language policy is advisory and states retain autonomy. This ongoing curriculum
    revision creates a syllabus currency risk: MILU items sourced from older exam
    papers may not reflect newly revised NCERT/state board content. Source: iDream
    Education NCERT changes post-NEP — [WEB-5];
    Wikipedia NEP 2020 — [WEB-12]'
net_new_fields:
  related_benchmarks:
    IndicMMLU_Pro:
      description: IndicMMLU-Pro (arXiv 2501.15747, January 2025) is a translation-based
        benchmark adapting MMLU-Pro into 9 Indic languages including Hindi, using
        IndicTrans2 with back-translation quality assurance. It covers language comprehension,
        reasoning, and generation tasks but is English-origin and not grounded in
        Indian competitive-exam or school-board content. Hindi achieves the highest
        translation quality score (chrF++ 78.06) among languages evaluated.
      relevance_to_deployment: IndicMMLU-Pro does not address the school-board framing
        gap identified for this deployment — its Hindi content derives from translated
        Western academic tasks, not from UPPSC/MPPSC/RBSE/BSEB or Hindi-board literary
        curricula. It provides a complementary harder reasoning benchmark but is not
        a substitute for MILU's India-sourced items for this deployment context.
      source: arXiv 2501.15747 — [WEB-11]
    Hindi_LLM_benchmark_suite_2025:
      description: A 2025 arXiv preprint (2508.19831) introduces Hindi instruction-following
        benchmarks (IFEval-Hi, MT-Bench-Hi, BFCL-Hi) adapted from English benchmarks
        with Indian cultural themes. It documents a gap in resources for evaluating
        instruction-tuned models in Hindi, distinct from MCQ knowledge benchmarks
        like MILU.
      relevance_to_deployment: Confirms that existing Hindi benchmarks (including
        MILU) primarily target pre-trained base models rather than instruction-tuned
        models; the deployed LLM application likely uses an instruction-tuned model,
        creating an evaluation methodology gap beyond the content gaps already identified.
      source: arXiv 2508.19831 — [WEB-13]
  milu_dataset_version_note: 'The MILU GitHub repository (as of the search date) reports
    approximately 85,000 multiple-choice questions, compared to ~79,000 reported in
    the published NAACL 2025 paper. The Hugging Face dataset card reports ~80,000.
    This discrepancy suggests the dataset has been updated post-publication. Downstream
    assessments should verify which version is being used for evaluation, as question
    counts and coverage may differ from the paper''s reported statistics. Source:
    GitHub AI4Bharat/MILU — [WEB-8]; Hugging Face ai4bharat/MILU
    — [WEB-14]'
  ncert_syllabus_revision_risk: 'NCERT is rolling out revised textbooks under NEP
    2020 in phases (Classes 3 and 6 released April–May 2024; Classes 4, 5, 7, 8 planned
    2025–26). Notably, the 2023 rationalisation removed content on certain historical
    events from NCERT social science texts. MILU items sourced from pre-2023 competitive
    exams may reference content since removed from CBSE/NCERT syllabi, creating item-level
    currency mismatches for the CBSE-aligned subset of the deployment. Source: iDream
    Education — [WEB-5]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://scroll.in/article/825780/bihar-uttar-pradesh-rajasthan-and-madhya-pradesh-have-worst-literacy-rates-school-outcomes |
| WEB-2 | https://www.findeasy.in/indian-states-by-literacy-rate/ |
| WEB-3 | https://muftinternet.com/blog/usage-statistics-internet-and-mobile-users-in-india-2025/ |
| WEB-4 | https://en.wikipedia.org/wiki/Internet_in_India |
| WEB-5 | https://www.idreameducation.org/blog/post-nep-ncert-changes/ |
| WEB-6 | https://www.drishtiias.com/state-pcs/mppsc-exam-pattern |
| WEB-7 | https://arxiv.org/html/2501.13912v1 |
| WEB-8 | https://github.com/AI4Bharat/MILU |
| WEB-9 | https://arxiv.org/abs/2411.02538 |
| WEB-10 | https://www.sanskritiias.com/bpsc/syllabus/bpsc-exam-pattern-and-syllabus |
| WEB-11 | https://arxiv.org/abs/2501.15747 |
| WEB-12 | https://en.wikipedia.org/wiki/National_Education_Policy_2020 |
| WEB-13 | https://arxiv.org/html/2508.19831v1 |
| WEB-14 | https://huggingface.co/datasets/ai4bharat/MILU |

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
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Findings tagged CRITICAL
should be treated as strong evidence for lower scores on the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Hindi configuration)
**Analysis date:** 2025-08-04
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Dimension |
|----|---------|-----------|-------|---------|-----------|
| D1 | MILU/Hindi | All 245 | is_translated=True | Every sampled example has `is_translated: True` | IC |
| D2 | MILU/Hindi | Ex. 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं।" (Arts & Humanities / Literature and Linguistics) | IC |
| D3 | MILU/Hindi | Ex. 76 | option2 | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" (Arts & Humanities / Language Studies) | IC |
| D4 | MILU/Hindi | Ex. 90 | option3 | "शब्द 'grim' का पर्यायवाची लिखें।" (Arts & Humanities / Language Studies) | IC |
| D5 | MILU/Hindi | Ex. 105 | option4 | "निर्देश: निम्नलिखित प्रश्न में...दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है... Evangelize" (Arts & Humanities / Language Studies) | IC |
| D6 | MILU/Hindi | Ex. 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" (Arts & Humanities / Language Studies) | IC, OO |
| D7 | MILU/Hindi | Ex. 51 | option2 | "दिए गए वाक्य का सही सक्रिय रूप चुनें। सभी को उसके शानदार नृत्य प्रदर्शन ने मोहित कर दिया।" (Arts & Humanities / Language Studies) | IC |
| D8 | MILU/Hindi | Ex. 97 | option3 | "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है।" (postposition grammar; Language Studies) | IC |
| D9 | MILU/Hindi | Ex. 195 | option4 | "निर्देश: उस खंड की पहचान करें जिसमें व्याकरण संबंधी त्रुटि है... 'के शासन द्वारा'" | IC |
| D10 | MILU/Hindi | Ex. 118 | option2 | "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें." [question text for the idiom is absent] | IC, IF |
| D11 | MILU/Hindi | Ex. 152 | option1 | "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए सबसे उपयुक्त विकल्प चुनें." [underlined segment missing] | IC, IF |
| D12 | MILU/Hindi | Ex. 56 | option2 | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें..." [statements 1-4 not present in question text] | IC, IF |
| D13 | MILU/Hindi | Ex. 69 | option2 | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल, (b) केवल, (c) केवल" [referents a,b,c,d absent] | IC, IF |
| D14 | MILU/Hindi | Ex. 86 | option2 | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक...राज्यों A,B,C,D,E..." [states not named] | IC, IF |
| D15 | MILU/Hindi | Ex. 94 | option4 | "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? (a), (b), (c), (d)" [reactions not listed] | IC, IF |
| D16 | MILU/Hindi | Ex. 106 | option2 | "निम्नलिखित पदार्थों को...कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4" [substances not named] | IC, IF |
| D17 | MILU/Hindi | Ex. 143 | option4 | "निम्नलिखित शब्दों को तार्किक और अर्थपूर्ण क्रम में व्यवस्थित करने के लिए सही विकल्प चुनें." [words absent] | IC, IF |
| D18 | MILU/Hindi | Ex. 95 | option1 | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है. वाक्य A और F स्थिर हैं." [sentences not present] | IC, IF |
| D19 | MILU/Hindi | Ex. 151 | option1 | "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं...कौन सा तर्क मजबूत है?" [statement/arguments absent] | IC, IF |
| D20 | MILU/Hindi | Ex. 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" (Arts & Humanities / History — Mughal historiography) | IC |
| D21 | MILU/Hindi | Ex. 52 | option2 | "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था" (Arts & Humanities / History — South Indian history) | IC |
| D22 | MILU/Hindi | Ex. 48 | option3 | "भांड पाथेर थिएटर मुख्य रूप से भारत के निम्नलिखित में से किस राज्य/केंद्र शासित प्रदेश की परंपरा है?" (Arts & Humanities / Arts and Culture — Jammu & Kashmir) | IC |
| D23 | MILU/Hindi | Ex. 108 | option3 | "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" (Arts & Humanities / Literature and Linguistics — Tamil-specific) | IC |
| D24 | MILU/Hindi | Ex. 232 | option2 | "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है?" (Arts & Humanities / Literature and Linguistics — Tamil classic) | IC |
| D25 | MILU/Hindi | Ex. 126 | option3 | "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" (Arts & Humanities / Literature and Linguistics — Telugu/Telangana-specific) | IC |
| D26 | MILU/Hindi | Ex. 193 | option3 | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" (Arts & Humanities / Arts and Culture — Rajasthan-specific) | IC |
| D27 | MILU/Hindi | Ex. 198 | option2 | "'बस्तर का स्वतंत्रता संग्राम' भी कहा जाता है?" (Arts & Humanities / History — Chhattisgarh-specific) | IC |
| D28 | MILU/Hindi | Ex. 68 | option2 | "राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है?" (Geography — Rajasthan-specific) | IC |
| D29 | MILU/Hindi | Ex. 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" (Geography — UP-specific) | IC |
| D30 | MILU/Hindi | Ex. 242 | option4 | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है...चिकनकारी" (Arts & Humanities / Arts and Culture — UP-specific) | IC |
| D31 | MILU/Hindi | Ex. 115 | option4 | "किस लेखक ने...किस्सा किस्सा लखनऊवा-लखनऊ के आवामी किस्से के लिए साहित्य अकादमी युवा पुरस्कार 2021 जीता?" (Literature — recent award) | IC |
| D32 | MILU/Hindi | Ex. 64 | option3 | "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है?" (History — national patriotic figure) | IC |
| D33 | MILU/Hindi | Ex. 83 | option1 | "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम..." (Sociology — ethics scenario) | IC, OO |
| D34 | MILU/Hindi | Ex. 142 | option1 | "क्या तेलंगाना सरकार को सभी को मुफ्त शिक्षा प्रदान करनी चाहिए?" (Education — argumentation item) | IC |
| D35 | MILU/Hindi | Ex. 188 | option3 | "नई शिक्षा नीति 2020 में देखा गया है..." [problems (a)(b) not stated] | IC, IF |
| D36 | MILU/Hindi | Ex. 122 | option4 | "प्रधानमंत्री मुद्रा योजना (PMMY) के बारे में निम्नलिखित में से कौन सा कथन सही है? न तो 1 और न ही 2 / दोनों 1 और 2..." [statements 1 and 2 absent] | IC, IF |
| D37 | MILU/Hindi | Ex. 157 | option4 | "पद्म पुरस्कार 2021 के संदर्भ में निम्नलिखित कथनों पर विचार करें. 1...2...3..." (multi-statement item — complete in question) | IC |
| D38 | MILU/Hindi | Ex. 201 | option4 | "BIOS के संदर्भ में निम्नलिखित में से कौन सा कथन सही है? केवल I और II / केवल I और III..." [statements I, II, III absent] | IC, IF |
| D39 | MILU/Hindi | Ex. 222 | option2 | "2022 में फॉर्च्यून 500 सूची में भारतीय कंपनियों के संबंध में निम्नलिखित पर विचार करें: A, B, C, D, E केवल..." [items A-E absent] | IC, IF |
| D40 | MILU/Hindi | Ex. 74 | option4 | "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी?" (Economics — time-stamped current affairs) | IC |
| D41 | MILU/Hindi | Ex. 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022..." (Sports and Recreation — time-stamped current affairs) | IC |
| D42 | MILU/Hindi | Ex. 132 | option4 | "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं?" (Politics — time-stamped) | IC |
| D43 | MILU/Hindi | Ex. 127 | option2 | "भारतीय दंड संहिता किस वर्ष प्रभावी हुई? (target: option2 = 1862)" (Law and Ethics — factual) | OC |

---

### Findings

#### CRITICAL

#### Finding CRITICAL1: All 245 sampled validation examples are marked `is_translated: True` — the translated proportion appears to dominate or constitute the entire validation split

- **Dimension(s):** IC, IF
- **Observation:** Every single one of the 245 sampled examples carries `is_translated: True`. The published paper reports that only ~25% of the released 79K questions are translated from English [Q47], which would predict a minority of translated items in any representative sample. Yet no item in this 245-item sample has `is_translated: False`. This may indicate that the validation split was specifically constructed from translated items (as opposed to the test split which may contain the organically sourced majority), or that the `is_translated` flag has a different semantics than expected.
- **Potential concern for deployment:** If the validation split consists entirely of translated items, few-shot examples drawn from this split (as MILU intends [Q51]) will always be translated-origin content. For the Hindi-medium teacher deployment, this means that in-context examples used to calibrate LLM performance will never reflect organically sourced Hindi-exam register. Translated items may carry GPT-4O translation artifacts — formal but potentially non-idiomatic Khari Boli — and may not match the register of school-board or state-exam question papers. The entire few-shot calibration corpus would then be drawn from a systematically different distribution than the test corpus.
- **Datapoint citations:**
  - [D1] All 245 examples (MILU/Hindi, split=validation): `is_translated: True` on every row — if this is representative of the split, the validation set is 100% translated-origin, sharply at odds with the paper's reported 25% translated figure for the full dataset.

---

#### MAJOR

#### Finding MAJOR1: Pervasive truncated/incomplete question stems — answer options refer to absent content

- **Dimension(s):** IC, IF
- **Observation:** A substantial number of questions in the sample are self-evidently incomplete: the question stem references numbered statements, lettered items, underlined text, or a list of substances/reactions that are not present in the `question` field. Affected examples include at minimum: Ex. 56 (four statements about ethanol not provided), Ex. 69 (substances (a)–(d) absent), Ex. 86 (states A–E not named), Ex. 94 (reactions (a)–(d) not listed), Ex. 95 (sentences B–E absent), Ex. 106 (substances 1–4 not listed), Ex. 118 (idiom text missing), Ex. 122 (statements 1 and 2 absent), Ex. 143 (words to be arranged absent), Ex. 151 (statement and arguments absent), Ex. 152 (underlined segment missing), Ex. 188 (NEP problems (a)(b) absent), Ex. 201 (BIOS statements I–III absent), Ex. 222 (Fortune 500 items A–E absent).
- **Potential concern for deployment:** These items cannot be answered from the `question` field alone. If an LLM is evaluated on these items using only the structured fields provided, it must guess among four options without the necessary referent content — systematically degrading accuracy scores for no construct-valid reason. For the North Indian teacher deployment, where MILU is being assessed as a benchmark for Hindi-medium MCQ evaluation, this data quality issue means a non-trivial fraction of Hindi items are functionally unanswerable and will depress measured accuracy in ways unrelated to language or cultural competence. The fraction of affected items in the validation split appears substantial (at least 14/245 = ~6% confirmed from the sample, likely higher).
- **Datapoint citations:**
  - [D12] Example 56 (MILU/Hindi, split=validation, label=option2): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें और दिए गए विकल्पों में से सही उत्तर चुनें:" — answer options reference statements 1–4 that are not present in the question field.
  - [D13] Example 69 (MILU/Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल, (b) केवल, (c) केवल" — substances (a)–(d) not provided.
  - [D14] Example 86 (MILU/Hindi, split=validation, label=option2): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, C..." — states A–E not identified.
  - [D15] Example 94 (MILU/Hindi, split=validation, label=option4): "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं?" — reactions (a)–(d) absent.
  - [D16] Example 106 (MILU/Hindi, split=validation, label=option2): "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4" — substances 1–4 not named.
  - [D10] Example 118 (MILU/Hindi, split=validation, label=option2): "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें." — the idiom itself is absent.
  - [D11] Example 152 (MILU/Hindi, split=validation, label=option1): "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए सबसे उपयुक्त विकल्प चुनें." — underlined segment not present.
  - [D18] Example 95 (MILU/Hindi, split=validation, label=option1): "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है. वाक्य A और F स्थिर हैं." — sentences not provided.
  - [D19] Example 151 (MILU/Hindi, split=validation, label=option1): "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं...कौन सा तर्क मजबूत है?" — statement and arguments I/II absent.
  - [D35] Example 188 (MILU/Hindi, split=validation, label=option3): "नई शिक्षा नीति 2020 में देखा गया है कि भारत में उच्च शिक्षा प्रणाली निम्नलिखित में से किन समस्याओं का सामना कर रही है? केवल (a) / केवल (b)..." — problems (a)/(b) not stated.
  - [D36] Example 122 (MILU/Hindi, split=validation, label=option4): "प्रधानमंत्री मुद्रा योजना (PMMY) के बारे में निम्नलिखित में से कौन सा कथन सही है? न तो 1 और न ही 2..." — statements 1 and 2 absent.
  - [D38] Example 201 (MILU/Hindi, split=validation, label=option4): "BIOS के संदर्भ में निम्नलिखित में से कौन सा कथन सही है? केवल I और II..." — statements I, II, III absent.
  - [D39] Example 222 (MILU/Hindi, split=validation, label=option2): "2022 में फॉर्च्यून 500 सूची में भारतीय कंपनियों के संबंध में निम्नलिखित पर विचार करें: A, B, C, D, E केवल..." — companies A–E not named.

---

#### Finding MAJOR2: Hindi Arts & Humanities items do not include canonical North Indian literary content (Tulsidas, Premchand, Kabir, Mahadevi Verma)

- **Dimension(s):** IC, IO
- **Observation:** Across 245 sampled Hindi validation items, Arts & Humanities / Literature and Linguistics questions reference Kashmiri poets (Ex. 98: "कश्मीर का जॉन कीट्स"), Tamil classics (Ex. 108: Subramanya Bharati; Ex. 232: Silappatikaram/Ilango Adigal), Telugu literary works (Ex. 126: Telangana Rastrodayamalu), Sindhi writers (Ex. 179: Sahitya Akademi), and William Wordsworth (Ex. 7). No sampled item references Tulsidas, Premchand, Kabir, Mahadevi Verma, Jaishankar Prasad, Nirala, or Dinkar — the canonical Hindi-board literary figures listed as high-priority for the deployment. The History items reference Mughal historiography (Ex. 25: Masir-e-Alamgiri), Pandya kings (Ex. 52), Indus Valley (Ex. 237), and Asoka (Ex. 158), but not figures specifically canonical to North Indian state-board Hindi literature curricula.
- **Potential concern for deployment:** The deployment requires assessment of student responses to MCQs covering canonical Hindi literature as taught in UP, MP, Bihar, and Rajasthan boards. If Hindi Literature and Linguistics items are drawn from competitive-exam general-knowledge framings featuring South Indian, Kashmiri, or international literary figures rather than the canonical Hindi-board authors, the benchmark will not measure what North Indian teachers actually test their students on. This directly instantiates the highest-priority IC gap identified in the coverage gap analysis.
- **Datapoint citations:**
  - [D2] Example 7 (Arts & Humanities / Literature and Linguistics, label=option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं।" — a UK Romantic poet, not part of Hindi board syllabus; no equivalent item found for Tulsidas or Premchand.
  - [D23] Example 108 (Arts & Humanities / Literature and Linguistics, label=option3): "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" — Tamil literary history, not North Indian board Hindi literature.
  - [D24] Example 232 (Arts & Humanities / Literature and Linguistics, label=option2): "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है?" — Tamil classic literature.
  - [D25] Example 126 (Arts & Humanities / Literature and Linguistics, label=option3): "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" — Telugu/Telangana literary topic.
  - [D20] Example 25 (Arts & Humanities / History, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" — Mughal court historiography, competitive-exam framing rather than school-board Hindi literature perspective.

---

#### Finding MAJOR3: English-vocabulary Language Studies items in a Hindi-language benchmark

- **Dimension(s):** IC, IF
- **Observation:** Multiple Language Studies items in the Hindi benchmark ask about English vocabulary or English grammar in a Hindi-translated wrapping: Ex. 76 asks the meaning of 'didactic' in English; Ex. 90 asks for the synonym of 'grim'; Ex. 105 asks the Hindi meaning of 'Evangelize'; Ex. 3 (implicitly) tests English grammar concepts (active/passive voice in Hindi phrasing). These items appear to be translated from English-language verbal-ability competitive-exam questions (SSC, banking exams) where the original task was English vocabulary proficiency, not Hindi language competence.
- **Potential concern for deployment:** North Indian Hindi-medium teachers assess students on Hindi grammar, Hindi literature, and sometimes Sanskrit-origin vocabulary — not on English synonym/antonym or English word definition tasks. Items that test knowledge of English vocabulary words (grim, didactic, evangelize) within the Hindi benchmark do not align with Hindi-medium state-board curricula. A model performing well on these items would be demonstrating English vocabulary knowledge accessed through Hindi translation, not Hindi-medium linguistic competence. This conflation may inflate or distort benchmark scores in ways irrelevant to the deployment context.
- **Datapoint citations:**
  - [D3] Example 76 (Arts & Humanities / Language Studies, label=option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" — Hindi item asking meaning of the English word 'didactic.'
  - [D4] Example 90 (Arts & Humanities / Language Studies, label=option3): "शब्द 'grim' का पर्यायवाची लिखें." — Hindi item asking for synonym of the English word 'grim.'
  - [D5] Example 105 (Arts & Humanities / Language Studies, label=option4): "निर्देश:...दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है और उसके अनुरूप बटन पर क्लिक करें। Evangelize" — Hindi item asking Hindi translation of English 'Evangelize.'

---

#### Finding MAJOR4: Competitive-exam IAS/civil-services framing dominates Social Sciences and Ethics items; school-board register absent

- **Dimension(s):** IC
- **Observation:** The one Ethics/Governance scenario item in the sample (Ex. 83) presents a complex multi-paragraph real-world dilemma cast explicitly from the perspective of "एक वरिष्ठ सिविल अधिकारी" (a senior civil servant) deciding how to respond to tribal displacement by an old-age home. This is textbook UPSC Mains Ethics, Paper IV framing — far from any school-board MCQ context. Similarly, Ex. 142 asks students to evaluate arguments about whether the Telangana government should provide free education to all, a policy-reasoning format typical of state PCS exams but foreign to UP Board Class 10–12 MCQ contexts.
- **Potential concern for deployment:** State-board teachers at the secondary level assess students on factual civics, basic constitutional law, and social science MCQs — not on complex IAS-style ethical reasoning scenarios or multi-paragraph argument evaluation. The presence of such items in the Hindi benchmark means a deployed LLM calibrated on MILU may be optimized for competitive-exam reasoning patterns that teachers in the deployment context never need to evaluate.
- **Datapoint citations:**
  - [D33] Example 83 (Social Sciences / Sociology, label=option1): "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है..." — 4-option scenario question in UPSC Ethics Paper IV register.
  - [D34] Example 142 (Arts & Humanities / Education, label=option1): "क्या तेलंगाना सरकार को सभी को मुफ्त शिक्षा प्रदान करनी चाहिए? तर्क: A: हाँ... B: नहीं..." — argument-strength evaluation item typical of state PCS prelims, not school-board MCQs.

---

#### Finding MAJOR5: Strong South India / non-Hindi-belt regional content bias in Arts & Humanities and Geography

- **Dimension(s):** IC, IO
- **Observation:** A disproportionate share of regionally specific content in the sample is drawn from South India, Eastern India, or states outside the Hindi belt. Arts & Culture items reference: Bhānd Pather theatre (Jammu & Kashmir, Ex. 48), Kota painting school (Rajasthan, Ex. 193 — one of the few Hindi-belt items), Tamil magazine cartoons (Ex. 108), Silappatikaram (Tamil, Ex. 232), Telangana literature (Ex. 126). History items feature Pandya kingdom (Ex. 52), Bastar rebellion/Chhattisgarh (Ex. 198). Geography features Manipur's Imphal Basin (Ex. 186), Jharkhand river origins (Ex. 107). UP/MP/Bihar/Rajasthan-specific content is rare: only Ex. 26 (UP minerals), Ex. 68 (Rajasthan reserved area), Ex. 242 (UP chikankari embroidery) are clearly Hindi-belt specific in this sample.
- **Potential concern for deployment:** The deployment targets North Indian Hindi-belt teachers whose students are assessed on UP/MP/Bihar/Rajasthan regional history, geography, and culture. The apparent under-representation of Hindi-belt regional content and over-representation

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
  "region": "North India Hindi-Medium Postgraduate Teacher — MCQ Assessment",
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
