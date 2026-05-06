I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **MILU: A Multi-task Indic Language Understanding Benchmark** is valid for use in **Bangladeshi Bengali University Student — Story Generation Thesis Deployment**.

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
- **Domain**: Indic language understanding (multi-domain, culturally grounded MCQ)
- **Languages**: bn, gu, hi, kn, ml, mr, or, pn, ta, te, en
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis

### Input Ontology
MILU's task taxonomy spans 8 domains and 41 subjects explicitly structured around
Indian academic and competitive examination content [Q1, Q17]. The eight domains —
Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance,
Health and Medicine, Science, Engineering and Technology, and Business Studies —
were derived through a semi-automated clustering of topic tags drawn from Indian
exam portals [Q38]. The benchmark is explicitly described as assessing "general
problem-solving abilities and India-specific knowledge" [Q19], and regional state
exams are included specifically to "authentically capture local knowledge in the
respective language" [Q12] — where "local" is operationalized as Indian state-level,
not cross-national. Detailed subject-level statistics across all 11 languages are
documented in appendix tables [Q99], and subject-level model evaluation results
are reported extensively across 42–45 models [Q128]. Critically, the taxonomy
structurally excludes any Bangladeshi-specific domain categories: the 1971
Liberation War framed as a Bangladeshi national event, Bangladeshi national
curriculum exams (SSC/HSC), Bangladeshi universities, and Bangladesh's post-1971
political history have no designated position in the 41-subject ontology. The
authors themselves note that models perform poorly in culturally relevant areas
like Arts & Humanities and Law & Governance [Q6] — exactly the domains where
Bangladesh-specific knowledge would most plausibly appear — and attribute this to
training data lacking "sufficient culturally specific data" [Q69].

### Input Content
All data was collected from over 1,500 Indian competitive examinations scraped from
online exam portals [Q11], explicitly following an "India-first perspective" [Q9].
Sources span national civil service exams, government and private organization
exams, and state-level competitive tests [Q93, Q96, Q97, Q98]. A total of
approximately 79,000 questions are released across 11 languages [Q42], with 25%
translated from English into target languages using GPT-4O [Q40, Q43]. English
questions are included specifically because "these often address Indian
culture-specific content, which is notably missing from existing popular
benchmarks" [Q26]. The benchmark emphasizes that "culturally relevant subjects
such as local history, arts, festivals, and laws" are included [Q10] — but
"local" here is defined by Indian state exam coverage. Regional state exams are
described as valuable because "they cover various state-level topics and emphasize
the official language of each state" [Q24]; the Bengali-language content almost
certainly reflects West Bengali or pan-Indian Bengali-medium exam references.
No Bangladeshi exam sources (SSC/HSC board papers, Dhaka University entrance
exams, or similar) are mentioned anywhere in the documentation. The scarcity of
questions in some language–subject pairs necessitated translation from English,
introducing a further layer of Indian English-origin content into non-Hindi
languages including Bengali [Q84].

### Input Form
MILU is a purely text-based benchmark consisting of multiple-choice questions with
up to four answer options in Indic scripts [Q29]. The data cleaning pipeline used
INDICLID and Unicode-based filtering to ensure correct language and script
assignment [Q30], and reading-comprehension and image-based questions were excluded
to enforce uniformity [Q29]. A final manual verification step was applied to a
sample from each language [Q32]. For a Bangladeshi Bengali deployment, the input
modality (written text in Bangla script) matches the target modality; no script
mismatch exists at the level of writing system. However, the documentation does
not address dialect stratification within Bengali — specifically whether Bengali
items use Bangladeshi Standard Bengali (Cholti register with Arabic/Persian
loanword patterns) or West Bengali Standard Bengali orthographic norms. This
register distinction is NOT DOCUMENTED in the paper.

### Output Ontology
The primary output for each MILU item is a single discrete label — the correct
answer among up to four MCQ options — reflecting the answer format of Indian
competitive examinations [Q29, Q51]. The 41-subject taxonomy functions as a
metadata label space for domain-level analysis rather than as model output targets
[Q38]. Approximately 45% of questions arrived with topic tags from source portals;
the remaining 55% were tagged programmatically using GPT-4O-MINI and K-means
clustering [Q33, Q36], then manually reviewed [Q37]. The correct-answer labels
were validated by the source exam portals' own subject experts [Q22], who are
implicitly operating within Indian knowledge frameworks. For a Bangladesh
deployment targeting open-ended story generation, this output taxonomy is doubly
misaligned: the correct-answer categories encode Indian factual and cultural
standards, and the MCQ label space does not map onto evaluating culturally
grounded narrative generation at all. The authors note that models perform poorly
in culturally relevant domains [Q68], but the benchmark does not provide any
mechanism for distinguishing India-specific from Bangladesh-specific answer
correctness within Bengali items.

### Output Content
MILU's annotation and quality assurance process relied primarily on the source
exam portals, which "manually tag questions with topic names and language details,
and subject experts ensure the accuracy of the answers" [Q22]. Cluster labels were
manually reviewed by the benchmark team [Q37], and AI4Bharat volunteers conducted
manual audits [Q87]. However, no formal inter-annotator agreement statistics,
annotator demographic profiles, or structured annotation protocols are disclosed.
The benchmark team is entirely affiliated with Indian institutions — the Nilekani
Centre at AI4Bharat, IIT Madras, and IBM Research India [Q8] — and funding came
from Indian philanthropies [Q86]. No Bangladeshi reviewers, validators, or
subject-matter experts are mentioned in the documentation. Given that Bengali
items derive entirely from Indian exam sources and were audited by an
Indian-institutional team, the ground-truth labels for Bengali items were
established within an Indian cultural and linguistic frame. This represents a
meaningful annotator-population mismatch for any evaluation targeting Bangladeshi
Bengali speakers. The paper does not explicitly acknowledge this India–Bangladesh
distinction within its Bengali coverage.

### Output Form
MILU evaluates models using accuracy as the primary metric across multiple shot
conditions [Q46, Q55]. For non-API models, the log-likelihood method is used via
LM-EVALUATION-HARNESS, selecting the answer with highest conditional log
probability [Q48, Q49, Q51]; API models use a generative approach with structured
JSON output due to lack of log-probability support [Q52, Q53]. The benchmark
evaluates 0-shot, 1-shot, and 5-shot conditions for open models [Q46], with 5-shot
accuracy as the primary reported figure [Q55]; API models are evaluated zero-shot
only due to cost [Q54]. Extensive per-model, per-subject, per-language result
tables are provided across 54 appendix tables [Q100–Q132]. The authors themselves
note that "evaluation primarily relies on the log-likelihood approach, which may
yield different results compared to other established methods, such as
generation-based evaluation and chain-of-thought (CoT) prompting" [Q85]. For a
Bangladesh deployment targeting open-ended story generation in Bengali, this output
form gap is structural: MILU measures factual recall accuracy on closed-form MCQ
items, while the deployment requires evaluating culturally grounded narrative
generation. Strong MILU accuracy may be a necessary but insufficient precondition
for culturally grounded generation quality, and the benchmark does not provide
a scoring methodology that transfers directly to the deployment target.


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
| Q8 | 1 | output_content | "Sshubam Verma1 Mohammed Safi Ur Rahman Khan1,2 Vishwajeet Kumar3 Rudra Murthy3 Jaydeep Sen3 1Nilekani Centre at AI4Bharat 2Indian Institute of Technology, Madras 3IBM Research, India" |
| Q9 | 2 | input_content | "We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams." |
| Q10 | 2 | output_ontology | "These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science." |
| Q11 | 2 | input_content | "We create this benchmark by collecting questions from over 1500 competitive exams from India." |
| Q12 | 2 | input_content | "We focus on region-specific exams to authentically capture local knowledge in the respective language." |
| Q13 | 2 | output_form | "We evaluate 45 different LLMs - a mix of closed proprietary, open-source, and language-specific models- on MILU." |
| Q14 | 2 | output_form | "Our findings suggest that models struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q15 | 2 | output_form | "Our analysis of in-context learning reveals that adding more examples improves performance in base models, but the effect on instruct models remains inconclusive." |
| Q16 | 2 | input_ontology | "Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM." |
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
| Q33 | 4 | output_content | "Upon examination, we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information." |
| Q34 | 4 | input_form | "To address this issue, we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question." |
| Q35 | 4 | output_ontology | "Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap." |
| Q36 | 4 | output_ontology | "To organize them, we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters." |
| Q37 | 4 | output_content | "We manually review these clusters and assign appropriate subject labels." |
| Q38 | 4 | output_ontology | "Following the manual merging of related clusters, we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies." |
| Q39 | 4 | input_content | "Finally, we observed that some topics in certain languages had less than 100 questions. To ensure thorough evaluation across all subjects and languages, we aimed to have at least 100 questions per subject in each language." |
| Q40 | 4 | input_content | "For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O." |
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
| Q57 | 6 | input_content | "These models are primarily built by adapting English LLMs, such as LLAMA-2-7B, by first continually pretraining on small amount Indic language data, followed by optionally instruction finetuning them." |
| Q58 | 6 | output_form | "As seen from Table 4, across languages, the models exhibit average performance comparable to random baselines, with minimal variations among them." |
| Q59 | 6 | input_ontology | "When analyzed across domains, the models generally perform worse in Arts, Humanities, and Social Sciences than in STEM subjects." |
| Q60 | 6 | output_form | "We compare the performance of different Base and Instruct models across zero, one, and five-shot setups." |
| Q61 | 6 | output_form | "As shown in Figure 3, the performance of base models consistently improves with an increasing number of in-context examples, with the 5-shot setup yielding the best results." |
| Q62 | 6 | output_form | "In contrast, Instruct models exhibit more varied behavior, where models either stagnate or even degrade in performance." |
| Q63 | 6 | output_form | "This also aligns with expectations, as Instruct models are specifically fine-tuned as conversation assistants and may not respond well to the few-shot in-context examples format." |
| Q64 | 7 | output_form | "We evaluate the LLAMA and GEMMA family of models, ranging from 1B to 405B parameters, to analyze how performance scales with model size." |
| Q65 | 7 | output_form | "Figure 5 shows that the model performance improves significantly with increasing scale." |
| Q66 | 7 | output_form | "Notably, instruction-tuned models in the LLAMA family show more substantial improvements as compared to those in the GEMMA family." |
| Q67 | 7 | output_form | "We analyze the performance of various base and instruct models across multiple domains and languages." |
| Q68 | 7 | input_ontology | "Similar trends to those in Section (§5.2) are observed where the open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields." |
| Q69 | 7 | input_content | "This suggests that the training corpora for these models lack sufficient culturally specific data." |
| Q70 | 7 | input_content | "Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages." |
| Q71 | 7 | output_form | "As most Indic LLMs are built on English base models like LLAMA-2-7B, we assess the impact of language adaptation on their performance." |
| Q72 | 7 | output_form | "Table 5 compares language-specific models with the original LLAMA-2-7B, and instruction-tuned models with LLAMA-2-7B-CHAT." |
| Q73 | 7 | output_form | "Our findings show minimal gains, with some models even underperforming post-adaptation." |
| Q74 | 8 | input_ontology | "In this paper, we introduced MILU—Multilingual Indic Language Understanding Benchmark-a comprehensive benchmark specifically designed to evaluate LLMs across 11 Indic languages, spanning diverse domains and culturally relevant subjects." |
| Q75 | 8 | output_form | "We evaluate 45 different LLMs and find that the majority of LLMs struggle on MILU, with GPT4o achieving the highest average accuracy." |
| Q76 | 8 | input_ontology | "The analysis also shows that models perform significantly better in high-resource languages than low-resource ones, highlighting the need for more robust multilingual strategies." |
| Q77 | 8 | input_ontology | "Additionally, the domain-specific analysis indicates that models perform better in general fields such as STEM while facing challenges in culturally relevant subjects like Arts, Humanities, and Law, highlighting the lack of this knowledge in the current models and datasets." |
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
name: Bangladeshi Bengali University Student — Story Generation Thesis Deployment
abbreviation: BD-BN-SGT
deployment_context:
  country: Bangladesh
  primary_city: Dhaka
  geographic_scope: Urban Dhaka as the user's base; deployment content spans rural/village
    Bangladesh, Chittagong Hill Tracts, and river delta regions
  institution_type: Undergraduate university (BSc thesis work)
  task: Bengali story generation with locally grounded Bangladeshi cultural, geographic,
    linguistic, and historical context
  user_role: Undergraduate university student conducting BSc thesis research on LLM
    cultural grounding in Bangladeshi Bengali
target_population_description: Native Bangladeshi Bengali speakers — primarily undergraduate
  university students in Dhaka — who expect LLMs to accurately reproduce Bangladesh-specific
  cultural touchstones, named entities, historical narratives, geographic references,
  and linguistic register. The deployment evaluates how well generic frontier models,
  small LLMs, and region-specific LLMs handle Bangladesh-specific context in open-ended
  Bengali story generation. The population is literate, academically oriented, and
  digitally active, but expects grounding in both urban (Dhaka) and rural/riverine
  Bangladesh contexts.
languages:
  primary: Bangladeshi Standard Bengali (Cholti register)
  register_notes: Bangladeshi Standard Bengali (Cholti) is the required register.
    It is distinguished from West Bengali Standard Bengali by vocabulary, idiom, and
    a higher density of Arabic and Persian loanwords reflecting Bangladeshi Islamic
    cultural heritage. Indian exam-derived Bengali content almost certainly reflects
    West Bengali or pan-Indian orthographic and lexical norms and is considered inadequate
    for this deployment.
  script: Bengali script (Bangla lipi)
  script_notes: Text-only deployment; Bengali script is used throughout. No script
    mismatch with the benchmark at the writing-system level. Routine verification
    of non-Latin script rendering and tokenization behavior in Bengali is still advisable.
  dialect_stratification_in_benchmark: NOT DOCUMENTED in MILU — no dialect or register
    stratification within the Bengali split is disclosed; downstream verification
    required.
  colloquial_variants_relevant:
  - Dhaka urban Bengali (educated Cholti)
  - Rural/village Bengali (regional dialects of Mymensingh, Sylhet, Chittagong, Barisal
    areas)
  - Chittagong Hill Tracts minority language contact varieties
  dialect_bias_research_note: 'A 2026 paper (arXiv:2603.21359) documents a multi-stage
    framework for benchmarking Bengali dialectal bias across 9 Bengali dialects, using
    a 4,000-question dataset, confirming that dialectal variation remains broadly
    underexplored in Bengali NLP evaluation and that standard tokenization metrics
    fail to capture semantic equivalence in dialectal variants. Source: arXiv:2603.21359
    — [WEB-1]'
writing_system:
  script: Bengali script (Bangla lipi)
  directionality: left-to-right
  capitalization: Bengali script has no uppercase/lowercase distinction
  nlp_notes: Bengali script tokenization is generally supported in major NLP toolchains,
    but sub-register differences (Bangladeshi vs. West Bengali orthographic conventions)
    are rarely captured in standard tooling. Arabic/Persian loanword patterns in Bangladeshi
    Bengali may tokenize differently from West Bengali equivalents.
  tokenization_corpus_note: 'Bengali''s allocation in the Sangraha multilingual corpus
    is approximately 30 billion tokens, compared to approximately 2 trillion tokens
    available for English in large-scale multilingual corpora — a gap that constrains
    LLM Bengali performance. Bengali''s alphasyllabary script with diacritics and
    conjunct forms creates tokenization challenges not present in Latin-script languages.
    Source: arXiv:2507.23248 — [WEB-2]'
literacy_and_education:
  target_user_literacy: High — undergraduate university students; fluent literate
    Bangladeshi Bengali speakers
  national_literacy_rate: '74.66% (2022 National Census of Bangladesh). Functional
    literacy rate (age 7+) is 62.92%; general literacy rate 74.23% per BBS Literacy
    Assessment Survey 2020–2023. Urban functional literacy (ages 11–45) is 80.35%
    vs. rural 70.54%. Source: Bangladesh 2022 Census cited in Wikipedia Education
    in Bangladesh — [WEB-3]; BBS
    LAS Survey reported in Dhaka Tribune — [WEB-4].

    Note: a 2025 BBS Health and Morbidity Status Survey found 42.45% of the population
    still below fifth-grade literacy (23.51% never attended school, 18.94% did not
    progress past primary), indicating significant variation around the headline figure;
    the target user cohort (university students) is well above the national average.'
  higher_education_enrollment_rate: '[NEEDS VERIFICATION — deferred: below search
    budget; World Bank tertiary enrollment data for Bangladesh available at https://data.worldbank.org/indicator/SE.TER.ENRR?locations=BD
    but specific figure not retrieved in this pass]'
  key_national_exam_system:
    secondary: SSC (Secondary School Certificate)
    higher_secondary: HSC (Higher Secondary Certificate)
    notes: 'SSC and HSC are the primary national curriculum exams in Bangladesh, administered
      by multiple education boards. These are entirely absent from MILU''s Indian
      exam-sourced content. Note: the JSC (Junior School Certificate) examination
      was last held in November 2024 and is now defunct; PEC was last held in 2019.
      Source: Wikipedia Education in Bangladesh — [WEB-3]'
  key_universities_in_deployment_scope:
  - Dhaka University (DU)
  - Bangladesh University of Engineering and Technology (BUET)
  - Islamic University of Technology (IUT)
  - Dhaka Medical College (DMC)
  - Rajshahi University
  - Shahjalal University of Science and Technology (SUST)
  - BRAC University
  university_representation_in_benchmark: NOT DOCUMENTED — none of these institutions
    are mentioned in MILU documentation; their absence from the benchmark's ontology
    is a confirmed gap.
cultural_norms_and_touchstones:
  overview: The target population expects LLMs to demonstrate fluency with Bangladeshi
    national identity, which is distinct from Indian national identity and draws on
    a specific historical, linguistic, and cultural formation centered on the 1952
    Language Movement, the 1971 Liberation War, and subsequent Bangladeshi state history.
  foundational_national_events:
  - event: 1952 Language Movement (Bhasha Andolan)
    notes: The movement for recognition of Bengali as an official language of Pakistan;
      foundational to Bangladeshi national identity. Commemorated annually on 21 February
      (Shaheed Dibosh / International Mother Language Day). MILU may frame this as
      an Indian or pan-Bengali event rather than a Bangladeshi national narrative
      — framing differences affect answer correctness.
  - event: 1971 Liberation War (Muktijuddho)
    notes: The independence war against Pakistan resulting in the founding of Bangladesh.
      Central to all Bangladeshi cultural, political, and historical discourse. Absent
      from MILU's Indian exam-derived ontology as a Bangladeshi national event.
  - event: Post-1971 political history (1975–2026)
    notes: 'Includes the 1975 coup and assassination of Sheikh Mujibur Rahman, the
      1990 uprising against Ershad, the parliamentary democracy period, and major
      political developments through 2026. 2024 update: In July–August 2024, a student-led
      mass uprising known as the ''July Revolution'' or ''Monsoon Revolution'' (triggered
      by the reinstatement of civil service quotas reserving 30% of posts for descendants
      of 1971 Liberation War freedom fighters) concluded with the resignation and
      exile of Prime Minister Sheikh Hasina on 5 August 2024 after 15 years in power.
      An interim government led by Nobel laureate Muhammad Yunus was formed. The UN
      estimated up to 1,400 people may have been killed during the crackdown. The
      Bangladesh War Crimes Tribunal sentenced Hasina to death in absentia for crimes
      against humanity in November 2025. As of early 2026, general elections are planned
      and a constitutional referendum on the ''July Charter'' is underway. The uprising
      has profoundly influenced popular culture, discourse, and cultural reference
      frames for the target student cohort. Sources: Wikipedia July Revolution (Bangladesh)
      — [WEB-5]; EUAA situation
      update — [WEB-6];
      Chatham House analysis — [WEB-7]'
  cultural_events:
  - event: Ekushe Boi Mela (February Book Fair)
    notes: Annual book fair held at Bangla Academy, Dhaka, in February. Directly linked
      to the Language Movement; a flagship Bangladeshi literary and cultural event
      with no Indian equivalent.
  - event: Pohela Boishakh (Bengali New Year)
    notes: Celebrated on 14 April as the Bangladeshi New Year. The Bangladeshi observance
      — particularly the Mangal Shobhajatra procession in Dhaka — has distinct forms
      from West Bengali celebrations.
  - event: Shaheed Dibosh (21 February)
    notes: Martyrs' Day commemorating the Language Movement; now also International
      Mother Language Day (UNESCO).
  - event: Victory Day (16 December)
    notes: National holiday marking Bangladesh's victory in the 1971 Liberation War.
  literary_and_cultural_figures:
  - figure: Humayun Ahmed
    domain: Novelist, playwright, filmmaker; the most widely read Bangladeshi author
      of the modern era
  - figure: Muhammad Zafar Iqbal
    domain: Science fiction author and educator; major figure in Bangladeshi youth
      literature
  - figure: Selim Al Deen
    domain: Playwright; central figure in Bangladeshi drama tradition
  - figure: Rabindranath Tagore (Bangladeshi reception)
    notes: Tagore is claimed by both Bangladesh and West Bengal; Bangladeshi cultural
      framing of Tagore differs from Indian national framing
  - figure: '[NEEDS VERIFICATION — deferred: likely unsearchable (lived canon); requires
      stakeholder/expert elicitation from Bangladeshi literary scholars to surface
      additional major film, drama, and literary figures expected as reference points
      in story generation contexts]'
  bangladeshi_drama_and_film:
    notes: '[NEEDS VERIFICATION — deferred: likely unsearchable at the level of expected
      granularity (specific BTV drama series, private channel productions, canonical
      film directors); requires expert elicitation or community sourcing from Bangladeshi
      film/media scholars]'
  islamic_cultural_context:
    notes: 'Bangladesh is a majority-Muslim country; Islamic cultural practices, vocabulary
      (Arabic/Persian loanwords in everyday Bengali), and observances (Eid ul-Fitr,
      Eid ul-Adha, Ramadan) are embedded in everyday language and narrative. This
      is distinct from the Hindu-majority or syncretic cultural framing dominant in
      West Bengali content. The BengaliMoralBench (2025) benchmark explicitly grounds
      its moral reasoning scenarios in Bangladeshi traditions including Religious
      Activities (Daily Activities and Religious Activities have the highest country-specific
      content), providing independent evidence that Islamic cultural context is a
      primary differentiator for Bangladeshi Bengali LLM evaluation. Source: arXiv:2511.03180
      — [WEB-8]'
  rural_and_riverine_context:
    notes: A significant share of Bangladeshi narrative tradition is rooted in rural
      and riverine life — the river delta (Padma, Meghna, Jamuna, Buriganga river
      systems), farming communities (paddy cultivation, jute), fishing villages, and
      seasonal flood cycles. These contexts are structurally absent from competitive
      exam content and represent a deployment-critical gap.
    key_ecological_features:
    - River delta agriculture (haor, beel, char lands)
    - Paddy and jute farming traditions
    - Boat culture and riverine transport
    - Seasonal flood (borsha) as cultural and narrative motif
    - Sundarbans mangrove ecosystem (shared Bangladesh/India, but Bangladeshi portion
      is larger)
geographic_scope:
  primary_urban_center: Dhaka
  dhaka_neighborhoods_relevant:
  - Dhanmondi
  - Old Dhaka (Puran Dhaka)
  - Wari
  - Mirpur
  - Gulshan
  - Shahbagh
  - '[NEEDS VERIFICATION — deferred: below search budget; additional Dhaka neighborhoods
    (Badda, Uttara, Mohammadpur, Lalbagh, Shyampur, Rayer Bazar, Banani) are plausible
    candidates but require local expert confirmation of salience in story generation
    contexts]'
  major_rivers:
  - Buriganga (Dhaka)
  - Padma (as it flows through Bangladesh; distinct from Indian section called Ganges)
  - Meghna
  - Jamuna (Bangladeshi name for the Brahmaputra)
  - Surma
  - '[NEEDS VERIFICATION — deferred: below search budget; Karnaphuli (Chittagong),
    Teesta (Rangpur), Kushiyara (Sylhet), Halda (Chittagong) are plausible candidates
    for narrative salience but require local expert confirmation]'
  tourism_and_cultural_sites:
  - Cox's Bazar (world's longest natural sea beach)
  - Rangamati (Chittagong Hill Tracts lake district)
  - Bandarban (Hill Tracts; hill tribe communities)
  - Sajek Valley (Hill Tracts)
  - Sundarbans (mangrove forest, Bangladesh portion)
  - Srimangal (tea gardens)
  - Paharpur (Buddhist ruins, UNESCO site)
  - '[NEEDS VERIFICATION — deferred: below search budget; Kuakata (sea beach, Barisal),
    Mainamati (Buddhist ruins, Comilla), Lalbagh Fort (Old Dhaka), Ahsan Manzil (Pink
    Palace, Old Dhaka), Ratargul Swamp Forest (Sylhet) are plausible candidates]'
  sub_national_regions:
  - region: Chittagong Hill Tracts (CHT)
    notes: Ethnically diverse region; home to Chakma, Marma, Tripuri, and other indigenous
      communities. Distinct cultural and linguistic context from Bengali plains.
  - region: Sylhet Division
    notes: Distinct Sylheti dialect; large diaspora in UK; tea-growing region.
  - region: Barisal Division
    notes: River delta heartland; strong association with riverine rural life and
      narrative tradition.
  - region: Rajshahi Division
    notes: Padma riverside; silk production; Rajshahi University.
  - region: Mymensingh Division
    notes: Agricultural heartland; Bangladesh Agricultural University (BAU) located
      here; haor wetlands in the north (Netrokona, Sunamganj border). Relevant to
      rural narrative contexts.
  - region: Khulna Division
    notes: Gateway to the Sundarbans; industrial city; distinct dialect. The Bangladeshi
      Sundarbans portion falls primarily within this division.
  - region: '[NEEDS VERIFICATION — deferred: below search budget; Rangpur Division
      (northern Bangladesh, Teesta river, Barind Tract) and Comilla/Chattogram Division
      sub-regions are also narratively salient]'
benchmark_alignment_notes:
  benchmark: MILU (Multi-task Indic Language Understanding Benchmark)
  language_coverage: Bengali (bn) is one of MILU's 11 languages, but content derives
    exclusively from Indian competitive examinations. The Bengali split almost certainly
    reflects West Bengali or pan-Indian Bengali-medium exam norms.
  critical_ontological_gaps:
  - 1971 Liberation War as a Bangladeshi national event
  - SSC/HSC national curriculum exams
  - Bangladeshi universities (Dhaka University, BUET, IUT, DMC, BRAC University, etc.)
  - Post-1971 Bangladeshi political history
  - Bangladeshi cultural events (Ekushe Boi Mela, Pohela Boishakh as Bangladeshi observance)
  - Bangladeshi named entities (Dhaka neighborhoods, Bangladeshi rivers, tourism sites)
  - Rural and riverine Bangladesh sub-contexts
  - Bangladeshi literary and cultural figures (Humayun Ahmed, Selim Al Deen, Muhammad
    Zafar Iqbal)
  - 2024 July Uprising and post-uprising political context (entirely post-benchmark)
  register_gap: Bangladeshi Standard Bengali (Cholti register, Arabic/Persian loanword
    patterns) is not documented as the target register in MILU's Bengali split; West
    Bengali norms are presumed dominant.
  annotator_mismatch: MILU's Bengali content was validated entirely within Indian
    institutional frameworks (AI4Bharat, IIT Madras, IBM Research India). No Bangladeshi
    annotators are documented. Native Bangladeshi Bengali speakers are required as
    primary ground truth for this deployment.
  output_form_mismatch: MILU evaluates closed-form MCQ accuracy; the deployment targets
    open-ended Bengali story generation. Benchmark accuracy scores measure factual
    recall, not culturally grounded generative quality.
  language_movement_framing_risk: The 1952 Language Movement may be framed in MILU
    as an Indian or pan-Bengali event rather than a foundational Bangladeshi national
    narrative; this framing difference can affect answer correctness for Bangladeshi
    users.
infrastructure_notes:
  internet_penetration: '44.5% of total population (approximately 77.36 million users)
    as of January 2024, rising slightly to ~77.7 million users by January 2025. However,
    by mid-2024, the BTRC noted mobile internet subscribers declined by ~13.2 million
    in seven months due to increased taxes on mobile services (supplementary duty
    raised from 15% to 20%, total tax burden exceeding 39%), the July 2024 political
    disruption, and rising costs. Over 50% of households had internet access in July–September
    2024 (BBS ICT Access and Use Survey 2024–25). Sources: DataReportal Digital 2024
    Bangladesh — [WEB-9]; The
    Business Standard BTRC data — [WEB-10];
    Prothom Alo BTRC data — [WEB-11]'
  mobile_internet_penetration: '118.49 million mobile internet subscribers recorded
    at end of 2023 per BTRC (Bangladesh Telecommunication Regulatory Commission),
    representing the high-water mark; this figure declined by approximately 13.2 million
    mobile internet users in the seven months to January 2025 due to economic and
    political factors. 3G and 4G network coverage reported at 100% as of 2025. Note:
    national-level figure; urban Dhaka university students are expected to be active
    smartphone users well above the national average. Sources: The Business Standard
    BTRC — [WEB-12];
    ngital.com 2025 analysis — [WEB-13]'
  primary_access_device: 'Mobile-dominant internet access is expected; laptop/desktop
    access common among urban university students. Smartphone usage has risen to 70.1%
    of households as of 2024 (up from 63.3% in 2023). Only 9.2% of households own
    computers. Source: BBS ICT Access and Use Survey 2024–25 via The Business Standard
    — [WEB-10]'
  connectivity_notes: 'Urban Dhaka has relatively good connectivity. Median mobile
    internet connection speed: 23.00 Mbps (January 2024) rising to 28.26 Mbps (January
    2025). Rural Bangladesh connectivity is lower: 46% rural household internet penetration
    vs. 60.3% urban (BBS 2024). A meaningful rural-urban digital divide is confirmed.
    Sources: DataReportal — [WEB-9];
    BBS via The Business Standard — [WEB-10]'
  relevant_platforms: '[NEEDS VERIFICATION — deferred: below search budget; likely
    requires community survey or expert elicitation to identify which Bengali-language
    LLM interfaces (e.g., ChatGPT Bengali, Google Bard/Gemini, local academic platforms)
    are actively used by Bangladeshi university students for thesis work]'
  nlp_infrastructure_notes: 'Bengali is a relatively high-resource Indic language
    for NLP purposes, but tooling predominantly reflects West Bengali norms (e.g.,
    many tokenizers trained on Indian Bengali corpora). Bangladeshi Bengali-specific
    NLP resources are less developed. Recent Bengali-focused models include TituLLM
    (2025), TigerLLM (2025), BanglaGPT, and BanglaBERT. Bengali''s allocation in the
    Sangraha multilingual corpus is ~30 billion tokens vs. ~2 trillion tokens for
    English, posing a significant constraint on model performance. Bengali''s alphasyllabary
    script creates tokenization challenges (diacritics, conjunct forms) not well-handled
    by standard LLM tokenizers. Sources: arXiv:2507.23248 — [WEB-2];
    arXiv:2502.11187 — [WEB-14]'
evaluation_population_requirements:
  primary_ground_truth: Native Bangladeshi Bengali speakers
  acceptable_secondary: Mixed annotator pool including at least a substantial Bangladeshi
    Bengali speaker proportion
  explicitly_insufficient: Indian-only annotator pools, including Indian Bengali (West
    Bengali) speakers evaluating Bangladeshi-specific cultural content
  annotation_criteria: Annotators must be familiar with Bangladeshi national history
    (1971 Liberation War, post-independence political history including the 2024 July
    Uprising), Bangladeshi educational institutions, Bangladeshi cultural events,
    Bangladeshi geography, and Bangladeshi Standard Bengali register including Arabic/Persian
    loanword patterns
  story_generation_evaluation_methodology: 'No validated methodology exists in MILU
    for evaluating culturally grounded open-ended story generation; this is a structural
    gap requiring a purpose-built evaluation rubric. Existing Bengali cultural benchmarks
    (BLUCK, BengaliMoralBench, BanglaSocialBench) use MCQ or binary labeling frameworks;
    none target generative story quality. However, BanglaSocialBench (2026) offers
    a native-speaker-written, context-dependent evaluation methodology that could
    inform rubric design for culturally grounded generation. Sources: arXiv:2505.21092
    — [WEB-15]; arXiv:2603.15949 — [WEB-16];
    arXiv:2511.03180 — [WEB-8]'
domain_specific_notes:
  historical_and_political: 'The 1971 Liberation War is not a peripheral topic — it
    is the foundational national narrative. Any Bengali story generation benchmark
    for Bangladesh must be able to evaluate correct, nuanced representation of this
    event and subsequent political history (1975 coup, 1990 uprising, democratic transitions,
    and the 2024 July Uprising). The July 2024 student-led uprising that ousted PM
    Sheikh Hasina after 15 years is now embedded in the cultural and political consciousness
    of the exact student cohort this deployment targets — it is likely to appear as
    a narrative context in story generation prompts. The interim government led by
    Muhammad Yunus, the ''Students Against Discrimination'' movement, the quota reform
    controversy, and the term ''July 36'' (referring to 5 August 2024) are all live
    cultural references for Bangladeshi university students as of 2025–2026. Sources:
    Wikipedia July Revolution — [WEB-5];
    EUAA situation update — [WEB-6]'
  educational_system: 'The Bangladeshi national curriculum (SSC/HSC) and the specific
    institutions named (Dhaka University, BUET, IUT, DMC, Rajshahi University, SUST,
    BRAC University) are expected cultural reference points in student-centered story
    contexts. These are entirely absent from MILU. Note: PEC and JSC sub-secondary
    examinations are now defunct (last held 2019 and 2024 respectively); SSC and HSC
    remain the primary national benchmark examinations. Source: Wikipedia Education
    in Bangladesh — [WEB-3]'
  religious_and_cultural: 'Islamic cultural context — including vocabulary, observances,
    and values — is woven into everyday Bangladeshi Bengali. Story generation grounding
    requires sensitivity to the Islamic cultural register that distinguishes Bangladeshi
    Bengali from the more Sanskritic West Bengali register. BengaliMoralBench (2025)
    confirms that Bangladeshi-specific moral and religious contexts (religious activities,
    daily life, family) are structurally underserved by current multilingual LLMs.
    Source: arXiv:2511.03180 — [WEB-8]'
  rural_and_environmental: River delta ecology, monsoon seasonality, agricultural
    life, and boat culture are recurring narrative motifs in Bangladeshi literature.
    A model that cannot render these contexts authentically will fail on a significant
    portion of culturally grounded story generation tasks.
  literary_tradition: Bangladeshi literature has a distinct modern tradition (Humayun
    Ahmed's novels, Selim Al Deen's drama, the Ekushe Boi Mela literary ecosystem)
    that is not well represented in Indian competitive exam content. Evaluation of
    story generation quality requires familiarity with this tradition.
flagged_verification_priorities:
- priority: 1
  item: Whether any MILU Bengali items reference Bangladeshi-specific named entities,
    institutions, or historical events
  search_target: MILU Bengali split content analysis Bangladeshi named entities Liberation
    War SSC HSC
  resolution_status: NOT SEARCHED — the existing MILU documentation makes the answer
    structurally clear (all content from Indian exam portals, no Bangladeshi sources
    mentioned). Direct examination of MILU's Bengali question set would require dataset
    access, not web search. Treat as confirmed absent pending dataset audit.
- priority: 2
  item: Whether the MILU Bengali split uses Bangladeshi Standard Bengali (Cholti)
    or West Bengali register
  search_target: Bangladeshi Standard Bengali Cholti register MILU NLP benchmark dialect
  resolution_status: NOT SEARCHED — the documentation gap is confirmed (MILU does
    not disclose dialect stratification). Resolving this definitively requires linguistic
    analysis of MILU's Bengali questions, not web search.
- priority: 3
  item: Whether any Bangladeshi Bengali speakers participated in MILU annotation or
    validation
  search_target: MILU Bengali annotation annotator demographics Bangladeshi Bengali
    speaker
  resolution_status: NOT SEARCHED — MILU documentation confirms exclusively Indian
    institutional affiliation (AI4Bharat, IIT Madras, IBM Research India); no Bangladeshi
    annotators are mentioned. Treat as confirmed absent.
- priority: 4
  item: Existing Bangladeshi Bengali-specific NLP benchmarks or story generation evaluation
    frameworks
  search_target: Bangladesh Bengali NLP benchmark story generation evaluation cultural
    grounding 2023 2024
  resolution_status: 'RESOLVED — see net-new section below. Multiple Bangladesh-specific
    benchmarks now exist: BLUCK (2025), BengaliMoralBench (2025), BanglaSocialBench
    (2026), BnMMLU (2025). None target open-ended story generation; all use MCQ or
    binary labeling. See net-new fields for details.'
- priority: 5
  item: Current internet and mobile penetration statistics for Bangladesh, particularly
    urban Dhaka vs. rural
  search_target: Bangladesh internet penetration mobile usage statistics 2024 Dhaka
    rural
  resolution_status: RESOLVED — see infrastructure_notes above. National internet
    penetration ~44.5% (DataReportal 2024); household internet 50.4% (BBS 2024); urban
    60.3% vs. rural 46%; mobile internet subscriber count at ~118M peak (end 2023)
    declined by ~13.2M by January 2025 due to tax increases and July 2024 political
    disruption.
- priority: 6
  item: How MILU frames the 1952 Language Movement — as Indian, pan-Bengali, or Bangladeshi
    national event
  search_target: MILU Language Movement 1952 Bengali content Indian framing Bangladeshi
  resolution_status: NOT SEARCHED — resolving this requires examining MILU's actual
    Bengali question content, not web search. The structural risk (Indian exam framing)
    remains confirmed as a gap.
- priority: 7
  item: Bangladeshi Bengali NLP resources and tools currently in active use (tokenizers,
    corpora, language models trained on Bangladeshi Bengali)
  search_target: Bangladeshi Bengali NLP resources corpus tokenizer language model
    2024
  resolution_status: PARTIALLY RESOLVED — see infrastructure_notes and net-new NLP
    models section. TituLLM, TigerLLM, BanglaGPT, BanglaBERT are current models; Sangraha
    corpus has ~30B Bengali tokens. Bangladeshi-specific tokenizers or corpora are
    not separately identified in the literature; models are typically trained on mixed
    Bengali corpora dominated by West Bengali norms.
- priority: 8
  item: Post-2024 political developments in Bangladesh relevant to cultural context
    of story generation
  search_target: Bangladesh 2024 political events cultural context student protests
  resolution_status: 'RESOLVED — see foundational_national_events and domain_specific_notes
    above. The July 2024 Uprising (July Revolution / Monsoon Revolution), the fall
    of the Hasina government on 5 August 2024, the interim government under Muhammad
    Yunus, the ''Students Against Discrimination'' movement, and ongoing constitutional
    reform process (July Charter, planned 2026 elections) are all highly salient for
    the target student cohort and likely to appear in story generation prompts. Sources:
    multiple, cited in-place.'
net_new_fields:
  bangladeshi_bengali_nlp_benchmarks:
    overview: As of 2025–2026, a cluster of Bangladesh-specific Bengali NLP benchmarks
      has emerged that is directly relevant to this deployment's validity assessment.
      None targets open-ended story generation, but several provide partial coverage
      of the cultural and linguistic gaps identified above.
    benchmarks:
    - name: BLUCK (Bengali Linguistic Understanding and Cultural Knowledge)
      year: 2025
      description: '2,366 MCQs across 23 categories covering Bangladesh''s culture,
        history, and Bengali linguistics. Sourced from Bangladesh Civil Service (BCS)
        exams, university entrance exams, bar council, and bank job exams — making
        it the first MCQ benchmark centered on native Bangladeshi culture, history,
        and linguistics. Domains include Bangladesh history, Bangladeshi culture,
        Bengali phonetics, and Bengali semantics. GPT-4o achieves ~73% accuracy (0-shot),
        approximately 7% below its English performance. All models struggle with Bengali
        phonetics. Note: MCQ-only; does not address open-ended generation or rural/riverine
        contexts.'
      arxiv: arXiv:2505.21092
      url: '[WEB-15]'
      acl_anthology: '[WEB-17]'
      relevance_to_deployment: HIGH — directly addresses the Bangladesh-specific cultural
        ontology gap in MILU. Sourced from Bangladeshi examinations rather than Indian
        ones. Can serve as a supplementary cultural knowledge evaluation alongside
        the story generation assessment.
    - name: BengaliMoralBench
      year: 2025
      description: 3,000 hand-crafted moral dilemmas grounded in everyday Bangladeshi
        life, covering Daily Activities, Habits, Parenting, Family Relationships,
        and Religious Activities across 50 subtopics. Annotated via native Bangladeshi
        speaker consensus using Virtue, Commonsense, and Justice ethics frameworks.
        52% of instances are country-specific to Bangladesh. Performance varies widely
        (50–91% accuracy) across evaluated LLMs, with consistent failures in cultural
        grounding.
      arxiv: arXiv:2511.03180
      url: '[WEB-8]'
      relevance_to_deployment: MEDIUM — confirms the Islamic cultural context and
        Bangladeshi daily-life register gap. The native Bangladeshi annotator methodology
        is a model for the annotation approach this deployment requires. Does not
        cover story generation or historical/geographic named entities.
    - name: BanglaSocialBench
      year: 2026
      description: 1,719 culturally grounded instances written and verified by native
        Bangla speakers, spanning Bangla Address Terms, Kinship Reasoning, and Social
        Customs. Evaluates sociopragmatic competence in context-dependent language
        use (not factual recall). Finds that current LLMs 'frequently default to overly
        formal address forms, fail to recognize multiple socially acceptable address
        pronouns, and conflate kinship terminology across religious contexts.' Described
        as the first benchmark for sociopragmatic competence in Bangla.
      arxiv: arXiv:2603.15949
      url: '[WEB-16]'
      relevance_to_deployment: HIGH — the three-tiered Bangladeshi pronominal system,
        kinship-based addressing, and social customs evaluated here are directly relevant
        to culturally grounded story generation (character dialogue, narrator register,
        social interaction scenes). The native-speaker-written methodology is the
        closest existing model for a story generation evaluation rubric.
    - name: BnMMLU (Bengali Massive Multitask Language Understanding)
      year: 2025
      description: A comprehensive multitask Bengali benchmark with 41 subjects sourced
        from Bangladeshi educational and professional materials (NCTB-approved textbooks,
        competitive exam guides processed via OCR). Covers STEM, humanities, social
        sciences, and other domains. Explicitly sources from Bangladeshi materials,
        distinguishing it from MILU's Indian exam provenance.
      arxiv: arXiv:2505.18951
      url: '[WEB-18]'
      relevance_to_deployment: HIGH — provides a Bangladeshi-sourced MMLU-style complement
        to MILU for factual knowledge evaluation. The Bangladeshi educational materials
        provenance addresses the core content ontology gap.
    - name: BEnQA
      year: 2024
      description: Official English-Bengali corpus of MCQs sourced from Bangladesh's
        national board exams, focusing on STEM subjects. Cited in BLUCK as an earlier
        Bangladeshi-sourced benchmark.
      relevance_to_deployment: MEDIUM — STEM-only; does not address humanities, culture,
        or story generation contexts, but confirms that Bangladesh national board
        exam sourcing is feasible for NLP benchmarks.
    - name: Bengali Dialectal Bias Benchmark
      year: 2026
      description: 4,000-question benchmark across 9 Bengali dialects (including Barishal,
        Chittagong, Noakhali, Rangpur, Sylhet) for bias evaluation, using a RAG-based
        translation pipeline and RLAIF-inspired evaluation. Confirms that dialectal
        variation is systematically underexplored and that standard BLEU/WER metrics
        fail to capture semantic equivalence in Bengali dialects.
      arxiv: arXiv:2603.21359
      url: '[WEB-1]'
      relevance_to_deployment: MEDIUM — directly relevant to the Bangladeshi dialect
        stratification gap; documents the specific dialects (Barisal, Chittagong,
        Sylhet, Rangpur, Noakhali) relevant to sub-national story generation contexts.
    story_generation_gap_confirmed: No existing benchmark evaluates open-ended culturally
      grounded Bengali story generation. All existing Bangladeshi Bengali benchmarks
      use MCQ, binary label, or short-answer formats. A purpose-built evaluation rubric
      is required for this deployment. BanglaSocialBench's native-speaker-written,
      context-dependent evaluation methodology is the closest methodological precedent.
  bangladeshi_bengali_llm_models:
    overview: Several Bangla-specific LLM families exist that may be relevant to the
      deployment's comparison of frontier vs. regional LLMs.
    models:
    - name: TigerLLM
      year: 2025
      description: A family of Bangla large language models, presented at ACL 2025.
        Aggregates diverse Bengali corpora including educational, literary, and QA
        datasets.
      reference: Raihan and Zampieri (2025), ACL 2025 Short Papers, arXiv:2503.10995
        — [WEB-19]
    - name: TituLLM
      year: 2025
      description: A family of Bangla LLMs with comprehensive benchmarking, including
        a TituLM-Bangla MMLU diagnostic. Presented at ACL 2025 Findings.
      reference: Nahin et al. (2025), ACL 2025 Findings, arXiv:2502.11187 — [WEB-14]
    caveat: Both models are primarily trained on mixed Bengali corpora; whether their
      training data prioritizes Bangladeshi Standard Bengali over West Bengali norms
      is not documented in available sources. This ambiguity parallels the MILU register
      gap and should be investigated before using either as a 'Bangladeshi Bengali-specific'
      baseline in the thesis.
  2024_political_context_for_story_generation:
    summary: 'The July 2024 Uprising (Monsoon Revolution / July Revolution) is now
      a live cultural reference for the target student cohort and is likely to appear
      as a story generation context. Key reference points: the quota reform protests
      (30% job quota for freedom fighters'' descendants), the ''Students Against Discrimination''
      movement, the events of 5 August 2024, the term ''July 36'' (colloquial reference
      to 5 August as a day beyond the calendar), the interim government under Muhammad
      Yunus, and ongoing trials of Sheikh Hasina for crimes against humanity. The
      uprising has been described as ''the world''s first successful Gen Z revolution.''
      The political context also includes a resurgence of Islamist politics (Jamaat-e-Islami
      re-legalization), Bangladesh-India tensions, and an upcoming constitutional
      referendum. Any story generation evaluation rubric for this deployment should
      account for the possibility that students include 2024 political events as story
      contexts, and evaluate whether LLMs can handle this post-training-cutoff material.
      Sources: Wikipedia July Revolution — [WEB-5];
      Chatham House — [WEB-7]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/abs/2603.21359 |
| WEB-2 | https://arxiv.org/abs/2507.23248 |
| WEB-3 | https://en.wikipedia.org/wiki/Education_in_Bangladesh |
| WEB-4 | https://www.dhakatribune.com/bangladesh/education/319301/bbs-functional-literacy-rate-7-above-years-in |
| WEB-5 | https://en.wikipedia.org/wiki/July_Revolution_(Bangladesh) |
| WEB-6 | https://www.euaa.europa.eu/news-events/bangladesh-situation-update-one-year-after-students-protests |
| WEB-7 | https://www.chathamhouse.org/2025/11/sheikh-hasina-verdict-and-bangladeshs-upcoming-referendum-signal-transitional-moment-south |
| WEB-8 | https://arxiv.org/abs/2511.03180 |
| WEB-9 | https://datareportal.com/reports/digital-2024-bangladesh |
| WEB-10 | https://www.tbsnews.net/bangladesh/over-50-households-use-internet-bangladesh-bbs-1032411 |
| WEB-11 | https://en.prothomalo.com/bangladesh/7ifddqcbtf |
| WEB-12 | https://www.tbsnews.net/bangladesh/internet-users-bangladesh-reach-131-million-2023-791442 |
| WEB-13 | https://ngital.com/bangladesh-internet-penetration-2025-data-insights/ |
| WEB-14 | https://arxiv.org/abs/2502.11187 |
| WEB-15 | https://arxiv.org/abs/2505.21092 |
| WEB-16 | https://arxiv.org/abs/2603.15949 |
| WEB-17 | https://aclanthology.org/2025.banglalp-1.14/ |
| WEB-18 | https://arxiv.org/abs/2505.18951 |
| WEB-19 | https://arxiv.org/abs/2503.10995 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Does the deployment require Bangladesh-specific cultural touchstones rather than the Indian cultural references likely present in MILU's Bengali content?
A1: Yes. Required coverage includes: the 1971 Liberation War and subsequent political history through 2026; Bangladeshi educational landmarks (SSC, HSC exams; Dhaka University, BUET, IUT, DMC, Rajshahi University, Shahjalal University, BRAC University); rural/village life and river-area contexts; Bangladeshi drama and film history; cultural events such as Ekushe Boi Mela; and tourism sites including Cox's Bazar, Rangamati, Bandarban, and Sajek. These are largely absent from Indian exam-sourced content.

Q2 [IC]: Are the Bengali datapoints in MILU — sourced from Indian competitive exams — expected to contain Bangladeshi-specific named entities such as Dhaka neighbourhoods, Bangladeshi institutions, political figures, and local geography?
A2: Yes, the deployment expects such Bangladeshi-specific named entities. However, given MILU's Indian exam provenance, the benchmark's concrete references are presumed to be predominantly India-centric, creating a significant gap for this deployment.

Q3 [IC]: Does the deployment require the Bangladeshi Bengali register specifically, and do Indian exam-derived questions adequately reflect that register?
A3: Yes, the Bangladeshi register is specifically required (vocabulary, idiom, Arabic/Persian loanword patterns distinct from West Bengali). Indian exam-derived questions do not adequately reflect this register and are therefore insufficient for evaluating the target deployment.

Q4 [OC]: Whose judgment should serve as ground truth for evaluating locally grounded Bangladeshi story generation, and does annotator mismatch affect score reliability?
A4: Native Bangladeshi Bengali speakers should serve as the primary ground truth; a mixed annotator pool is acceptable as a secondary option. Indian annotator validation of MILU's Bengali content is considered to meaningfully affect the reliability of evaluation scores for this Bangladesh-targeted deployment.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MILU's Bengali content is sourced entirely from Indian state and competitive exams, systematically excluding the Bangladeshi cultural, political, educational, and geographic categories the deployment requires (Liberation War, SSC/HSC, Ekushe Boi Mela, Bangladeshi tourism, rural river life). |
| IC | HIGH | Concrete datapoint-level references — named institutions, political figures, Dhaka neighbourhoods, Bangladeshi rivers — are almost certainly India-centric, and the user explicitly confirmed the need for Bangladesh-specific named entities and register, with Indian exam content deemed inadequate. |
| IF | LOWER | The deployment is text-only in a high-resource Indic script (Bengali) and MILU is also text-only; no modality mismatch exists, though non-Latin script rendering deserves routine verification. |
| OO | MODERATE | MILU uses MCQ label output from Indian exam questions; the output category space (correct exam answers) does not map cleanly onto evaluating culturally grounded story generation quality, though downstream scoring for story generation may differ from benchmark scoring itself. |
| OC | HIGH | MILU's Bengali labels were validated through Indian exam frameworks and likely by Indian annotators; the user confirmed this mismatch degrades reliability, and native Bangladeshi Bengali speakers are required as the primary ground-truth population. |
| OF | MODERATE | MILU produces MCQ labels while the deployment targets open-ended story generation; this format gap means benchmark scores measure recall of factual/cultural knowledge rather than generative cultural grounding, limiting direct transfer of evaluation validity. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Bengali config, with cross-config inspection of English, Hindi, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu)
**Analysis date:** 2025-01-31
**Examples reviewed:** 215 total (21 Bengali validation, 20 English validation, 24 Gujarati, 26 Hindi, 17 Kannada, 16 Malayalam, 21 Marathi, 21 Odia, 25 Punjabi, 19 Tamil, 25 Telugu)
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Bengali validation | Ex. 1 | option3 | "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল? … তেল ও পেট্রোলিয়াম পণ্যের আমদানির মূল্যের তীব্র বৃদ্ধি" | India's 1991 balance-of-payments crisis question, translated from English (is_translated=True) | IC, OC |
| D2 | Bengali validation | Ex. 5 | option4 | "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" | Indian state assembly election (AAP in Punjab, 2022) — exclusively India-centric governance content | IC, IO |
| D3 | Bengali validation | Ex. 9 | option3 | "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" | Removal of India's Election Commissioner — refers to Indian constitutional provisions | IC, OC |
| D4 | Bengali validation | Ex. 12 | option4 | "'মঙ্গল ভারত' কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল … আচার্য বিনোবা ভাবে" | "Mangal Bharat" — Indian national leader Vinoba Bhave; India-specific cultural/literary content | IC |
| D5 | Bengali validation | Ex. 17 | option2 | "৬৫তম ফিল্মফেয়ার অ্যাওয়ার্ডস, ২০২০-এ সেরা সিনেমাটোগ্রাফির জন্য পুরস্কারটি কে জিতেছেন? … জয় ওজা" | 65th Filmfare Awards (Indian film industry awards) — not Bangladeshi film industry | IC, IO |
| D6 | Bengali validation | Ex. 18 | option4 | "_______ দিল্লিতে কুতুব মিনারের নির্মাণ সম্পন্ন করেছিলেন … ইলতুতমিশ" | Qutub Minar, Delhi — India-specific historical monument | IC |
| D7 | Bengali validation | Ex. 3 | option4 | "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল? … গুলবার্গা" | Bahamani Kingdom capital — medieval Indian/Deccan history, not Bangladeshi | IC |
| D8 | Bengali validation | all 21 | various | All 21 Bengali examples show is_translated: True | Every Bengali validation example in sample is translated from English | IC, IF |
| D9 | English validation | Ex. 2 | option3 | "Which state has topped the India Innovation Index - 2019 published by Niti Aayog? … Karnataka" | India Innovation Index — Indian national governance content | IC |
| D10 | English validation | Ex. 9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" | Maharashtra state legislature — India-specific governance at state level | IC |
| D11 | English validation | Ex. 13 | option4 | "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? … Telangana" | Telangana state welfare scheme — Indian state government | IC |
| D12 | English validation | Ex. 15 | option3 | "Founded in 1950, one of the industrial units owned by Indian Railways is named after the Indian freedom fighter … Chittaranjan Das" | Indian Railways industrial unit named after Indian independence figure | IC |
| D13 | Bengali validation | Ex. 2 | option3 | "একটি ক্রিকেট প্রশিক্ষণ শিবিরে ১২০০ জন শিশু প্রশিক্ষণ নিচ্ছে যার মধ্যে ৯০০ জন নির্বাচিত হয়েছে। নির্বাচিত না হওয়া শিশুদের সংখ্যা এবং মোট শিশুদের সংখ্যার অনুপাত কত? … ১ : ৪" | Cricket training camp ratio problem — culturally neutral arithmetic, cricket context | IC |
| D14 | Bengali validation | Ex. 7 | option4 | "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প … জাতীয় খাদ্য সুরক্ষা মিশন আগস্ট ২০০৭ সালে চালু হয়েছিল" | India's National Food Security Mission — Indian government program | IC |
| D15 | Hindi validation | Ex. 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? … 44वें संविधान संशोधन अधिनियम द्वारा" | Indian constitutional amendment — India-specific law and governance | IC |
| D16 | Gujarati validation | Ex. 8 | option3 | "રેડક્લિફ રેખા નીચેના પૈકી કયા દેશ સાથે ભારતની સરહદોને અલગ કરે છે? … પાકિસ્તાન" | Radcliffe Line separating India and Pakistan — Indian national geography/history | IC |
| D17 | Bengali validation | Ex. 4 | option2 | "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। … শেল" | Constant current transformer type question — domain-neutral engineering/STEM | IC |
| D18 | Bengali validation | Ex. 8 | option4 | "নিম্নলিখিত কোনগুলি অক্সিডেশন-রিডাকশন বিক্রিয়া? … উপরের সবগুলি" | Oxidation-reduction reactions — universal science content | IC |
| D19 | Bengali validation | Ex. 10 | option4 | "হৃদয়ের পেসমেকার দ্বারা চিহ্নিত হয়, … এসএ নোড" | SA node as cardiac pacemaker — universal medical content | IC |
| D20 | Bengali validation | Ex. 14 | option3 | "একটি অ্যাসেম্বলার যা একটি মেশিনে চলে কিন্তু অন্য মেশিনের জন্য মেশিন কোড তৈরি করে তাকে কি বলা হয়? … ক্রস-অ্যাসেম্বলার" | Cross-assembler definition — universal computer science | IC |
| D21 | Bengali validation | Ex. 16 | option1 | "দুটি পাত্র আছে X এবং Y। X-এ ১০০ মিলি দুধ … m = n" | Milk-water mixture ratio problem — culturally neutral quantitative reasoning | IC |
| D22 | Odia validation | Ex. 2 | option4 | "ডিসেমবর 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆ… ବାଙ୍ଗ୍ଲାଦେଶ" | Indian Pharmacopoeia — Bangladesh mentioned as a distractor option, not as subject matter | IO |
| D23 | Telugu validation | Ex. 2 | option4 | "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది? … ఆఫ్ఘనిస్తాన్" | India Pharmacopoeia question — Bangladesh listed as distractor option2 | IO |
| D24 | Bengali validation | Ex. 6 | option2 | "নিচের প্রশ্নে, দেওয়া চারটি বিকল্পের মধ্যে থেকে সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে। … শীতল" | Antonym question in Bengali — vocabulary test | IF |
| D25 | Bengali validation | Ex. 13 | option2 | "নিচের বাক্যটির সঠিক সক্রিয় রূপ নির্বাচন করুন। সবাই তার চমৎকার নৃত্য পরিবেশনা দ্বারা মুগ্ধ হয়েছিল। … তার চমৎকার নৃত্য পরিবেশনা সবাইকে মুগ্ধ করেছিল।" | Active voice conversion of Bengali sentence — grammar in written Bengali | IF |
| D26 | Marathi validation | Ex. 16 | option3 | "হলষষ্ঠী সণ কা সাজরা কেলা জাতো? … মুলাচ্যা দীর্ঘায়ুষ্যাসাঠী" | Halshashthi festival (Maharashtra/Hindu calendar) — India-specific cultural festival, not Bangladeshi | IC |
| D27 | Bengali validation | Ex. 11 | option3 | "সিদ্ধান্ত গ্রহণের সাথে যুক্ত সমস্যাগুলি হল: … ভয় এবং মিথ্যা আশা" | Decision-making problems — generic management/psychology content | IC |
| D28 | Bengali validation | Ex. 19 | option1 | "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে … শুধুমাত্র যুক্তি I শক্তিশালী" | Logical argument strength question — generic reasoning | IC |
| D29 | Bengali validation | Ex. 20 | option2 | "জে, কে, এল, এম এবং এন পাঁচজন কাজিন … এম" | Age ordering puzzle with letter-named cousins — culturally neutral logic | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Bengali script is correctly used throughout the Bengali split
- **Dimension(s):** IF
- **Observation:** All 21 Bengali validation examples are rendered in Bangla script with correct Unicode rendering. The questions, options, and answers appear well-formed in Bengali script without visible encoding errors or script contamination from other Indic scripts.
- **Deployment relevance:** The target deployment uses Bangladeshi Bengali in Bangla script. No script mismatch exists at the writing-system level, satisfying the most basic input form requirement for a text-only Bengali evaluation.
- **Datapoint citations:**
  - [D24] Example 6 (Bengali, validation, option2): "নিচের প্রশ্নে, দেওয়া চারটি বিকল্পের মধ্যে থেকে সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে। … শীতল" — Bengali script is correctly rendered; antonym question shows standard written Bengali vocabulary
  - [D25] Example 13 (Bengali, validation, option2): "তার চমৎকার নৃত্য পরিবেশনা সবাইকে মুগ্ধ করেছিল।" — Active voice grammar question shows well-formed Bengali prose sentences

#### Strength 2: Multi-domain coverage including Arts & Humanities, Law & Governance, Science, and Business Studies
- **Dimension(s):** IO
- **Observation:** The sampled Bengali examples span Engineering (Ex. 4, 15, 16, 21), Science (Ex. 8), Health & Medicine (Ex. 10), Business Studies (Ex. 1, 11, 19), Arts & Humanities (Ex. 3, 6, 12, 13, 17, 18), Environmental Sciences (Ex. 7), Social Sciences (Ex. 2, 20), and Law & Governance (Ex. 5, 9). The domain coverage is broad across the 8 MILU domains.
- **Deployment relevance:** The deployment's evaluation of LLMs on cultural knowledge benefits from having multiple non-STEM domains present (Arts & Humanities, Law & Governance) even if their content is India-centric. This enables at least baseline measurement of model cultural knowledge capacity in Bengali, distinguishing models that have zero cultural awareness from those with some.
- **Datapoint citations:**
  - [D2] Example 5 (Bengali, validation, option4): "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" — domain=Law & Governance; confirms that political/governance content exists in Bengali, though content is India-specific
  - [D4] Example 12 (Bengali, validation, option4): "'মঙ্গল ভারত' কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল … আচার্য বিনোবা ভাবে" — domain=Arts & Humanities, subject=Literature and Linguistics; confirms literary content present in Bengali, though referencing Indian figures

#### Strength 3: STEM and universal academic content is present and transferable
- **Dimension(s):** IC
- **Observation:** A substantial portion of Bengali items covers domain-universal content — electrical engineering, chemistry, computer science, biology, mathematics — where the factual answer is culturally neutral and not India-specific. Questions about oxidation-reduction reactions, cardiac pacemakers, cross-assemblers, and mixture ratios have identical correct answers regardless of whether the evaluatee is Indian or Bangladeshi.
- **Deployment relevance:** For a deployment evaluating whether an LLM has general academic competence in Bengali, these universal STEM items provide valid signal. A model that cannot answer basic physics or chemistry questions in Bengali is unlikely to generate high-quality Bengali stories involving these topics either. While not the primary gap area, this represents a genuinely transferable subset.
- **Datapoint citations:**
  - [D18] Example 8 (Bengali, validation, option4): "নিম্নলিখিত কোনগুলি অক্সিডেশন-রিডাকশন বিক্রিয়া? … উপরের সবগুলি" — universal chemistry content; answer identical regardless of national context
  - [D19] Example 10 (Bengali, validation, option4): "হৃদয়ের পেসমেকার দ্বারা চিহ্নিত হয়, … এসএ নোড" — universal medical anatomy; no cultural specificity
  - [D20] Example 14 (Bengali, validation, option3): "একটি অ্যাসেম্বলার যা একটি মেশিনে চলে কিন্তু অন্য মেশিনের জন্য মেশিন কোড তৈরি করে তাকে কি বলা হয়? … ক্রস-অ্যাসেম্বলার" — universal computer science definition
  - [D21] Example 16 (Bengali, validation, option1): "দুটি পাত্র আছে X এবং Y। X-এ ১০০ মিলি দুধ … m = n" — culturally neutral quantitative reasoning

#### Strength 4: Bengali language grammar and vocabulary items present
- **Dimension(s):** IF, IC
- **Observation:** Examples 6 and 13 in the Bengali validation split test Bengali language competence directly — an antonym question and an active/passive voice transformation. These items probe written Bengali language knowledge at the lexical and syntactic level.
- **Deployment relevance:** Story generation quality depends partly on grammatical Bengali competence. These items provide at least some signal about whether a model can manipulate Bengali grammatical structures, even if the specific vocabulary tested may reflect written standard Bengali without dialect stratification.
- **Datapoint citations:**
  - [D24] Example 6 (Bengali, validation, option2): "নিচের প্রশ্নে, দেওয়া চারটি বিকল্পের মধ্যে থেকে সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে। … শীতল" — antonym selection tests Bengali vocabulary
  - [D25] Example 13 (Bengali, validation, option2): "নিচের বাক্যটির সঠিক সক্রিয় রূপ নির্বাচন করুন। সবাই তার চমৎকার নৃত্য পরিবেশনা দ্বারা মুগ্ধ হয়েছিল।" — active/passive voice tests Bengali grammatical competence

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Every sampled Bengali item is translated from English (is_translated=True across all 21 examples)
- **Dimension(s):** IC, IF
- **Observation:** All 21 Bengali validation examples in the sample carry `is_translated: True`. Per MILU documentation, ~25% of questions overall are translated using GPT-4O from English. The Bengali validation split in this sample shows 100% translated items. This means the Bengali content in this sample does not originate from Bengali-medium Indian exams at all — it is translated English content. No item in the Bengali validation sample was organically written in or sourced from a Bengali-language exam.
- **Deployment relevance:** The elicitation explicitly requires Bangladeshi Standard Bengali (Cholti register with Arabic/Persian loanword patterns). GPT-4O translation from English produces Bengali text in a standardized written register that almost certainly does not reflect Bangladeshi Cholti orthographic and lexical norms. The translated questions use vocabulary and phrasing patterns derived from English source content processed through a translation model likely trained on mixed Bengali corpora. This is the most direct form evidence of the register gap flagged in the deployment context.
- **Datapoint citations:**
  - [D8] All 21 Bengali validation examples (Bengali, validation): is_translated=True across the full sample — no organically Bengali-language exam content is present in this split's validation examples; all content is GPT-4O translated from English
  - [D1] Example 1 (Bengali, validation, option3): "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল?" — Indian 1991 crisis question translated into Bengali; vocabulary is formal written Bengali without any markers of Bangladeshi Cholti register

#### Concern 2: All cultural/political content in Bengali sample is exclusively India-centric; zero Bangladeshi cultural touchstones identified
- **Dimension(s):** IC, IO, OC
- **Observation:** Across the 21 Bengali validation examples, every culturally or politically specific item references Indian institutions, events, persons, or geography: India's 1991 financial crisis (Ex. 1), AAP's Punjab election win (Ex. 5), India's Election Commissioner removal procedure (Ex. 9), Indian leader Vinoba Bhave's "Mangal Bharat" (Ex. 12), the 65th Filmfare Awards (Ex. 17), and the Qutub Minar in Delhi (Ex. 18). Zero items reference: the 1971 Liberation War, Bangladeshi political history, Bangladeshi universities, Bangladeshi cultural events (Ekushe Boi Mela, Pohela Boishakh), Bangladeshi geography (Dhaka neighborhoods, Bangladeshi rivers), or Bangladeshi literary/cultural figures. This is consistent with documentation but confirmed empirically.
- **Deployment relevance:** The deployment requires that the benchmark evaluate LLMs on Bangladesh-specific cultural knowledge for Bengali story generation. The total absence of Bangladeshi cultural content means MILU Bengali scores measure performance on Indian cultural knowledge rendered in Bengali script — a fundamentally different construct from what is needed. High MILU Bengali accuracy does not predict Bangladeshi cultural grounding in story generation.
- **Datapoint citations:**
  - [D2] Example 5 (Bengali, validation, option4): "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" — India-specific political knowledge (Indian state elections); no Bangladeshi political equivalent present
  - [D3] Example 9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — Indian constitutional law (removal of India's Election Commissioner); Bangladesh's election commission structure is structurally different and absent
  - [D4] Example 12 (Bengali, validation, option4): "'মঙ্গল ভারত' কাজটি … আচার্য বিনোবা ভাবে" — Indian national movement figure; no Bangladeshi literary/cultural figure appears in any sampled item
  - [D5] Example 17 (Bengali, validation, option2): "৬৫তম ফিল্মফেয়ার অ্যাওয়ার্ডস, ২০২০-এ সেরা সিনেমাটোগ্রাফির জন্য পুরস্কারটি কে জিতেছেন? … জয় ওজা" — Filmfare Awards (Indian film industry); Bangladeshi film industry (Dhallywood, BTV drama) entirely absent
  - [D6] Example 18 (Bengali, validation, option4): "_______ দিল্লিতে কুতুব মিনারের নির্মাণ সম্পন্ন করেছিলেন … ইলতুতমিশ" — Delhi monument history; no Bangladeshi historical sites (Lalbagh Fort, Ahsan Manzil, Paharpur, Mainamati) present

#### Concern 3: Bangladesh appears only as a distractor option in non-Bengali language items — confirming structural absence
- **Dimension(s):** IO, IC
- **Observation:** In the Odia and Telugu validation samples, "Bangladesh" (বাংলাদেশ / బంగ్లాదేశ్) appears in option lists as a wrong-answer distractor in a question about which country first recognized the Indian Pharmacopoeia. This is the only appearance of Bangladesh in the entire 215-item cross-language sample. Bangladesh is not the subject of any question in any language split; it appears solely as a foil answer in India-centric questions.
- **Deployment relevance:** This direct observation confirms that Bangladesh is structurally positioned as a peripheral "foreign country" in MILU's knowledge frame, not as the primary geographic and cultural reference point. For a deployment centered on Bangladeshi Bengali cultural grounding, this framing is fundamentally misaligned.
- **Datapoint citations:**
  - [D22] Example 2 (Odia, validation, option4): "ଡିସେମ୍ବର 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆ… ବାଙ୍ଗ୍ଲାଦେଶ" — Bangladesh listed as option2 (wrong answer) in a question about Indian Pharmacopoeia; Bangladesh is a distractor, not a subject
  - [D23] Example 2 (Telugu, validation, option4): "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది? … బంగ్లాదేశ్" — same question in Telugu; Bangladesh again as distractor option

#### Concern 4: No Bangladeshi Bengali annotators — ground truth reflects Indian knowledge frameworks exclusively
- **Dimension(s):** OC
- **Observation:** Every examined item in the Bengali split carries a ground-truth answer label validated by Indian exam portal subject experts (per documentation) and audited by AI4Bharat (IIT Madras, IBM India). The culturally specific items in the Bengali sample [D2, D3, D4, D5, D6] all have correct answers that presuppose Indian constitutional, electoral, and cultural knowledge. No Bangladeshi institutional or individual validator is documented anywhere. For the governance/law questions (e.g., Election Commissioner removal procedure), the answer is verifiably correct for India but would be wrong if applied to Bangladesh's constitutional framework.
- **Deployment relevance:** The deployment requires native Bangladeshi Bengali speakers as primary ground truth. The benchmark's answer labels for cultural/governance content reflect Indian standards; a Bangladeshi evaluator might contest the framing of questions that appear to be generic ("the election commissioner") but actually encode Indian-specific legal structures.
- **Datapoint citations:**
  - [D3] Example 9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — the answer (President removes on CEC's recommendation) is specific to Indian constitutional law; Bangladesh's Election Commission operates under different provisions that a Bangladeshi annotator would recognize as distinct
  - [D2] Example 5 (Bengali, validation, option4): "আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" — requires knowledge of Indian party politics that is irrelevant to Bangladeshi civic knowledge

#### Concern 5: Output form (MCQ accuracy) fundamentally misaligned with deployment target (open-ended Bengali story generation)
- **Dimension(s):** OF, OO
- **Observation:** Every example across all 215 reviewed items is a closed-form 4-option MCQ. The output space is a discrete label (option1–option4). The deployment requires evaluating open-ended Bengali story generation — a generative task where cultural grounding, register appropriateness, narrative coherence, and accuracy of Bangladeshi named entities, historical events, and social context must be assessed. No mechanism in MILU produces a score that transfers to this task.
- **Deployment relevance:** This is a structural incompatibility: MCQ accuracy scores measure factual recall under forced choice, while story generation evaluation requires assessing fluency, cultural authenticity, register appropriateness, and factual grounding in Bangladeshi context. Strong performance on MILU Bengali (even if culturally recalibrated) would not directly validate culturally grounded story generation ability.
- **Datapoint citations:**
  - [D1] Example 1 (Bengali, validation, option3): "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল?" — The correct answer (option3) is binary pass/fail; this produces no information about whether a model can narratively describe economic history in Bangladeshi Bengali
  - [D19] Example 10 (Bengali, validation, option4): "হৃদয়ের পেসমেকার দ্বারা চিহ্নিত হয়, … এসএ নোড" — Medical MCQ; answering correctly does not predict whether the model can weave medical detail into a culturally authentic Bangladeshi story

---

#### MAJOR

#### Concern 6: Absence of 1971 Liberation War, Language Movement, and post-independence Bangladeshi political history
- **Dimension(s):** IO, IC
- **Observation:** None of the 21 Bengali examples, nor any English examples, reference the 1971 Liberation War, the 1952 Language Movement (Bhasha Andolan), Sheikh Mujibur Rahman, the founding of Bangladesh, or any post-1971 Bangladeshi political event. The History subject in Bengali covers the Bahamani Kingdom (Ex. 3) and Qutub Minar (Ex. 18) — medieval Indian history. The Law & Governance domain covers Indian state elections and Indian constitutional procedure.
- **Deployment relevance:** The 1971 Liberation War is described by the elicitation as "the foundational national narrative" for Bangladeshi Bengali speakers. The 2024 July Uprising — highly salient to the target student cohort — is post-benchmark and entirely absent. Any LLM evaluation intended to assess Bangladeshi cultural grounding must be able to test these topics; MILU provides no signal on them.
- **Datapoint citations:**
  - [D7] Example 3 (Bengali, validation, option4): "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল? … গুলবার্গা" — History subject item covers Deccan medieval Indian kingdom; the equivalent Bangladeshi history items (Liberation War, Language Movement) are absent
  - [D6] Example 18 (Bengali, validation, option4): "_______ দিল্লিতে কুতুব মিনারের নির্মাণ সম্পন্ন করেছিলেন … ইলতুতমিশ" — Delhi monument history; no equivalent Bangladeshi historical landmark questions appear

#### Concern 7: No items referencing Bangladeshi geography, institutions, or named entities
- **Dimension(s):** IC, IO
- **Observation:** Across all 21 Bengali items, no Bangladeshi geographic reference appears (no Dhaka, Cox's Bazar, Buriganga, Padma, Jamuna, Meghna, Rangamati, Sundarbans-Bangladesh). No Bangladeshi institution appears (no Dhaka University, BUET, IUT, BRAC University). The only geographic references in the Bengali sample are Indian: Delhi (Qutub Minar), Punjab (AAP election).
- **Deployment relevance:** The deployment explicitly requires LLM familiarity with Bangladeshi neighborhoods, rivers, universities, and tourism sites as reference points for story generation. MILU Bengali provides no data to evaluate this.
- **Datapoint citations:**
  - [D6] Example 18 (Bengali, validation, option4): "দিল্লিতে কুতুব মিনারের নির্মাণ" — Delhi is the only city named in culturally specific Bengali items; no Dhaka or Bangladeshi city appears
  - [D2] Example 5 (Bengali, validation, option4): "পাঞ্জাব" — Punjab (Indian state) is a named geographic reference; no Bangladeshi geographic equivalent present

#### Concern 8: Bengali register appears to be standardized written form, not Bangladeshi Cholti — no Arabic/Persian loanword patterns observed
- **Dimension(s):** IC, IF
- **Observation:** The Bengali vocabulary in the sampled items uses standard written Bengali orthography. Examining available lexical items: "আর্থিক সংকট" (financial crisis), "তাৎক্ষণিক" (immediate), "মুদ্রার রিজার্ভ" (currency reserves), "নির্বাচন কমিশনার" (election commissioner), "রাষ্ট্রপতি" (president). These are primarily Tatsama (Sanskrit-derived) formal vocabulary forms characteristic of the pan-Indian written Bengali register, not the Arabic/Persian loanword patterns that characterize Bangladeshi Standard Bengali Cholti. Terms like "সরকার" (government, from Persian "sarkar") do appear, but the overall lexical profile shows no distinctive Bangladeshi register markers. Given that all items are GPT-4O translations from English, this is expected.
- **Deployment relevance:** The elicitation identifies Bangladeshi Standard Bengali's Arabic/Persian loanword density as a distinguishing feature. A benchmark using Sanskritic-heavy written Bengali vocabulary would underestimate model performance on Bangladeshi-register text if models have been trained on predominantly Bangladeshi Bengali corpora, or overestimate it if models are stronger on the West Bengali register being tested.
- **Datapoint citations:**
  - [D1] Example 1 (Bengali, validation, option3): "বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ … তেল ও পেট্রোলিয়াম পণ্যের আমদানির মূল্যের তীব্র বৃদ্ধি" — vocabulary: "তাৎক্ষণিক" (tātkṣaṇika, Sanskrit-derived), "আমদানি" (Persian/Arabic "āmdāni"); mixed register with no distinctively Bangladeshi Cholti markers
  - [D25] Example 13 (Bengali, validation, option2): "তার চমৎকার নৃত্য পরিবেশনা সবাইকে মুগ্ধ করেছিল।" — "নৃত্য পরিবেশনা" (nṛtya paribeśanā) uses Sanskrit-derived dance vocabulary; standard written Bengali without Bangladeshi-specific register markers

#### Concern 9: India-specific governance and law content in Bengali may produce false negatives for Bangladeshi users
- **Dimension(s):** OC, OO
- **Observation:** Several Bengali governance items test knowledge of Indian constitutional and electoral procedures that are structurally different in Bangladesh. Example 9 tests removal of India's Election Commissioner (answer: President on CEC's recommendation). Example 5 tests which Indian state AAP won in 2022. A Bangladeshi user who correctly knows Bangladesh's electoral commission structure but answers according to that knowledge would be marked wrong. These items produce false negative scores for Bangladeshi cultural knowledge rather than measuring gaps.
- **Deployment relevance:** For a deployment evaluating Bangladeshi cultural grounding, items that penalize Bangladeshi-specific knowledge while rewarding Indian-specific knowledge produce construct-irrelevant variance that would make MILU Bengali scores misleading as a validity measure for this deployment.
- **Datapoint citations:**
  - [D3] Example 9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — correct only for Indian constitutional law; Bangladesh's equivalent procedure differs
  - [D14] Example 7 (Bengali, validation, option4): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প … জাতীয় খাদ্য সুরক্ষা মিশন আগস্ট ২০০৭ সালে চালু হয়েছিল" — India's National Food Security Mission; a Bangladeshi user has no reason to know this Indian government program

---

#### MINOR

#### Concern 10: Bengali validation split has disproportionately high translation rate compared to documented 25% overall
- **Dimension(s):** IC, IF
- **Observation:** MILU documentation states that ~25% of total questions are translated from English. Yet all 21 Bengali validation examples sampled show `is_translated: True` (100%). While the sample size (21) is small and the validation split may differ from the test split, this suggests the Bengali validation split is predominantly or entirely composed of translated items, not organically sourced Bengali exam content.
- **Deployment relevance:** If the test split for Bengali also has a higher-than-average translation rate, then MILU Bengali performance reflects model ability to read translated English content in Bengali script rather than genuine Bengali-medium cultural knowledge. This further compounds the register gap concern.
- **Datapoint citations:**
  - [D8] All 21 Bengali validation examples (Bengali, validation): is_translated=True — 100% translation rate in the sampled Bengali validation split, compared to documented 25% overall benchmark average

#### Concern 11: Cross-language contamination — identical questions appear verbatim across multiple language splits
- **Dimension(s):** IF
- **Observation:** The 1991 India financial crisis question (D1), Bahamani Kingdom capital question (D7), Qutub Minar question (D6), cross-assembler question (D20), and Mediterranean climate question appear verbatim translated across Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, and Telugu splits. This confirms that a large portion of MILU's multilingual content is parallel translations of the same question set rather than language-specific sourcing.
- **Deployment relevance:** For a Bangladeshi Bengali deployment, this means that MILU's Bengali content does not capture any language-specific cultural knowledge that is unique to Bengali-medium contexts — it is a translation of pan-Indian English exam content. The "regional state exam" value proposition claimed in the documentation does not appear to materialize in the Bengali validation sample.
- **Datapoint citations:**
  - [D7] Example 3 (Bengali, validation, option4): "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল? … গুলবার্গা" — same question appears in Gujarati Ex. 3 ("બહમણી રાજ્યની પ્રથમ રાજધાની"), Hindi (not sampled but implied by cross-config parallel), Malayalam Ex. 3 ("ബഹ്മനി സാമ്രാജ്യത്തിന്റെ ആദ്യ തലസ്ഥാനം"), Punjabi Ex. 3 ("ਬਹਮਨੀ ਰਾਜ ਦਾ ਪਹਿਲਾ ਰਾਜਧਾਨੀ"), Tamil Ex. 18, Telugu (not in sample) — identical content across all languages confirms parallel translation, not language-specific sourcing

#### Concern 12: Rural, riverine, and village life contexts — structurally absent in exam format
- **Dimension(s):** IO
- **Observation:** All 215 reviewed examples are competitive examination questions (civil services, engineering entrance, technical knowledge) targeting urban, academically educated populations. No item invokes agricultural life, river ecology, monsoon seasons, boat culture, fishing villages, or rural Bangladesh contexts. This is a structural feature of the exam-sourced data collection methodology, not a sampling artifact.
- **Deployment relevance:** The deployment explicitly requires coverage of rural/village Bangladesh and riverine contexts as narrative settings for story generation. No MILU item provides evaluation signal for LLMs' ability to generate authentic content in these registers.
- **Datapoint citations:**
  - [D13] Example 2 (Bengali, validation, option3): "একটি ক্রিকেট প্রশিক্ষণ শিবিরে ১২০০ জন শিশু" — the most "everyday" context in the Bengali sample is a cricket training camp, still an organized institutional setting; no rural or riverine reference exists in any sampled item
  - [D27] Example 11 (Bengali, validation, option3): "সিদ্ধান্ত গ্রহণের সাথে যুক্ত সমস্যাগুলি হল: … ভয় এবং মিথ্যা আশা" — management psychology question; the register throughout is urban, academic, and professional

---

### Content Coverage Summary

The Bengali validation split of MILU (21 examples reviewed) consists entirely of translated English exam questions (`is_translated=True` in 100% of the sample), covering: electrical engineering and materials science (Exs. 4, 15, 16, 21), general sciences (Exs. 8, 10, 14), India-specific law and governance (Exs. 5, 9), India-specific history (Exs. 3, 7, 18), India-specific culture and arts (Exs. 12, 17), Indian government programs (Ex. 7), quantitative reasoning (Exs. 2, 16, 20), Bengali language grammar (Exs. 6, 13), management/business (Exs. 1, 11, 19), and environmental science (Ex. 7).

The cultural, political, and geographic content is uniformly India-centric. Named entities include: AAP (Indian party), Punjab (Indian state), the Indian President and Chief Election Commissioner, Vinoba Bhave (Indian nationalist leader), Filmfare Awards (Indian film industry), Qutub Minar (Delhi), and the Bahamani Kingdom (Deccan Sultanate). No Bangladeshi named entity, institution, historical event, geographic location, or cultural figure appears in any Bengali example.

Cross-config inspection confirms that the same questions appear in parallel translation across all 11 language splits, confirming that the Bengali content is not sourced from Bengali-medium Indian state exams (which would produce at least some India-regional Bengali content) but rather from pan-Indian English exam questions translated into Bengali.

Register analysis of the Bengali text shows standard formal written Bengali using primarily Tatsama vocabulary. No distinctive Bangladeshi Cholti register markers or Arabic/Persian loanword density patterns are observed.

The English split confirms the India-centric content origin: state-specific Indian governance (Maharashtra legislative committees, Telangana welfare scheme, Indian Railways named after Indian freedom fighter, Niti Aayog India Innovation Index). These are the source documents from which the Bengali translations derive.

---

### Limitations

1. **Sample size:** Only 21 Bengali validation examples were reviewed. The test split (6,637 examples) may contain a different proportion of translated vs. organically sourced items, and may include items from Bengali-medium Indian state exams that do not appear in the validation split. The 100% translation rate observed in the validation sample should not be assumed to apply to the test split without direct verification.

2. **Register analysis limits:** Determining whether Bengali text reflects Bangladeshi Cholti vs. West Bengali orthographic norms requires systematic lexical analysis by a native Bangladeshi Bengali linguist. The present analysis observes vocabulary patterns but cannot definitively classify register with certainty from a 21-item sample.

3. **Test split not sampled:** The full Bengali test split (6,637 examples) was not inspected. It is possible that organically sourced Bengali-medium exam items in the test split contain some Bangladeshi-relevant content, though the documentation strongly suggests this is unlikely given the Indian exam sourcing.

4. **Domain distribution:** The 21-item validation sample may not reflect the domain distribution of the full test split. The high proportion of STEM-adjacent items with `is_translated=True` may be a validation-split artifact.

5. **No audio or image modalities:** MILU is text-only; no audio or image content was present to inspect. This limitation is alignment-confirming (deployment is text-only) rather than a gap in this analysis.

6. **Annotator demographics not directly inspectable:** The demographic composition of annotators cannot be verified from the dataset itself; this analysis relies on documentation disclosures showing exclusively Indian institutional affiliation.

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
  "region": "Bangladeshi Bengali University Student — Story Generation Thesis Deployment",
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
