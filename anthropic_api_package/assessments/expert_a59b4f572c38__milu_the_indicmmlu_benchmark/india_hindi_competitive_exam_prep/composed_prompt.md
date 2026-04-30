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

- **Name**: milu
- **Full Name**: MILU: A Multi-task Indic Language Understanding Benchmark
- **Domain**: Indic language understanding and culturally grounded knowledge evaluation
- **Languages**: hi, bn, gu, kn, ml, mr, or, pn, ta, te, en
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
MILU structures its task taxonomy around 41 subjects grouped into 8 macro-domains:
Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance,
Health and Medicine, Science, Engineering and Technology, and Business Studies [Q42].
The benchmark explicitly emphasizes India-specific knowledge, covering Science, Social
Sciences, Humanities, Arts, Business Studies, and Law [Q23], and is designed to
evaluate LLMs across diverse domains and culturally relevant subjects [Q74]. Detailed
subject-level statistics across languages are reported in Table 9 [Q98].

For the central-exam deployment context, several domains map meaningfully onto
priority subjects (History → Social Sciences; Polity → Law & Governance; GK → multiple
domains), but the taxonomy does not separately enumerate Mathematics/Reasoning or
Current Affairs as distinct categories — a notable gap for UPSC/SSC/banking syllabi.
MILU also evaluates Indic language LLMs built on English base models [Q60], confirming
its intent to probe knowledge-intensive reasoning across Indic languages. Questions
span over 40 exam types at national and state levels [Q27], meaning central-exam
and state-PSC items are pooled without a published breakdown by exam tier.

### Input Content
MILU's content is grounded in actual Indian competitive examination papers, sourced
from online exam portals that host previously released question papers [Q25], following
an approach analogous to AGIEVAL [Q13]. The source pool includes over 40 exam types
spanning national civil services, government and private organization exams, and
state-level civil services exams [Q92], with dedicated overview tables for each
category [Q95, Q96, Q97]. Regional state exams are explicitly valued for capturing
local knowledge in the respective regional language [Q28], and English-language
questions are included to address Indian culture-specific content absent from existing
benchmarks [Q30]. An India-first design perspective is stated explicitly [Q11], and
the benchmark incorporates culturally relevant subjects such as local history, arts,
festivals, and laws alongside standard academic subjects [Q2].

Of the approximately 79,000 released questions [Q46], roughly 25% were translated
from English to fill language-specific subject gaps [Q47] using GPT-4O [Q44, Q45].
This introduces translation artifact risk for Hindi items: it is undocumented what
fraction of MILU's Hindi questions originated as English items, whether translated
phrasing reflects Hindi-medium vocabulary conventions, and what the code-mixing rate
is across the Hindi subset. Approximately 45% of questions arrived with accurate
topic labels; the rest were labeled via machine translation into English followed by
GPT-4O-MINI topic assignment [Q37, Q38] — a process that may not preserve
Hindi-specific terminology or phrasing fidelity.

A separate validation set of approximately 9,000 questions is maintained for few-shot
examples [Q51], and all data will be released under permissible licenses [Q88, Q89].

### Input Form
MILU is exclusively text-based, with reading-comprehension-style questions,
image-based questions, and items with more than four options explicitly excluded
to ensure uniformity [Q33]. Language identification filtering via INDICLID and
Unicode-based methods ensures questions appear in the correct script and language [Q34],
and duplicate removal [Q35] together with multiple layers of manual and automated
cleaning [Q31, Q32, Q36] further standardize the input signal. For Hindi, Devanagari
script is the native encoding, and no signal-distribution mismatch concerns arise
for a text-based, Hindi-medium student population. The text-only MCQ format aligns
well with the deployment's input modality.

### Output Ontology
MILU's output label set is a closed-form MCQ answer: one correct option selected
from up to four choices [Q33]. The 41 subjects organized into 8 macro-domains [Q42]
provide a hierarchical label ontology for domain-level performance analysis, and
culturally relevant subjects such as local history, arts, festivals, and laws are
explicitly included within this taxonomy [Q12]. However, approximately 20,000
fine-grained topic tags were generated and subsequently merged into the 41-subject
taxonomy [Q39] — these granular tags are not part of the evaluation output schema.

This output ontology is a fundamental mismatch with the deployment context. The
deployment requires a correct/incorrect verdict accompanied by a substantive
Hindi-language explanatory rationale [elicitation Q3], but MILU produces only
MCQ accuracy scores. The benchmark documents no rubric, label set, or scoring
function for rationale quality. Culturally relevant domains (Arts & Humanities,
Social Sciences, Law & Governance) consistently show the weakest model performance
[Q6, Q20, Q62, Q71], directly implicating the benchmark's evaluation scope for
precisely the subjects most relevant to the deployment's priority areas (History,
Polity, GK).

### Output Content
MILU's answer labels are inherited from the online exam portals from which questions
were scraped: subject experts at those portals ensure answer accuracy at source [Q26].
This provides a credible chain of label provenance for the MCQ correct-answer labels,
grounded in India's established competitive exam ecosystem. Internal to MILU, AI4Bharat
volunteers conducted manual audits [Q87], and researchers manually reviewed topic-tag
clusters to assign final subject labels [Q41].

However, the paper does not report annotator demographics, inter-annotator agreement
statistics, or a formal QA protocol beyond manual sampling. It is unknown whether
auditors were Hindi-medium graduates, domain-subject experts, or bilingual researchers
— a gap bearing on whether question difficulty and phrasing were calibrated for the
target Hindi-medium student population. More critically, the deployment's core output
(the Hindi-language explanatory rationale) is wholly outside the scope of MILU's
annotation and label-correctness framework: no ground-truth rationales exist, and
no annotator demographics relevant to rationale quality have been documented.

### Output Form
MILU evaluates models using MCQ accuracy. For non-API models, evaluation uses the
LM Evaluation Harness with a log-likelihood method: the answer string with the
highest conditional log probability given the question is selected [Q52, Q53, Q54, Q55].
API-based proprietary models are evaluated in a zero-shot generative setup using
structured JSON prompts [Q56, Q57], limited to zero-shot due to cost constraints [Q58].
Models are tested under 0-shot, 1-shot, and 5-shot setups where feasible [Q50],
with results reported at domain and subject level across languages [Q59].

The benchmark authors themselves flag that the log-likelihood approach may yield
different results compared to generation-based evaluation and chain-of-thought
prompting [Q85] — a limitation directly relevant to the deployment, which requires
open-ended explanatory generation in Hindi rather than option selection. The output
form mismatch is therefore documented by the paper itself: MCQ label accuracy cannot
directly validate whether a model produces accurate, coherent, or pedagogically
appropriate Hindi-language explanations for competitive exam questions. Extensive
per-model, per-subject evaluation tables spanning pages 22–57 provide fine-grained
accuracy scores [Q99–Q132, Q100], but none capture fluency, correctness, or
cultural appropriateness of Hindi-language free-text output.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge." |
| Q2 | 1 | input_content | "With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science." |
| Q3 | 1 | output_form | "We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q4 | 1 | output_form | "Open multilingual models outperform language-specific fine-tuned models, which perform only slightly better than random baselines." |
| Q5 | 1 | input_ontology | "Models also perform better in high-resource languages as compared to low-resource ones." |
| Q6 | 1 | output_ontology | "Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM." |
| Q7 | 1 | input_ontology | "To the best of our knowledge, MILU is the first of its kind benchmark focused on Indic languages, serving as a crucial step towards comprehensive cultural evaluation." |
| Q8 | 1 | input_content | "All code, benchmarks, and artifacts will be made publicly available to foster open research." |
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
| Q21 | 2 | input_content | "All the artifacts will be released publicly." |
| Q22 | 3 | input_ontology | "MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge." |
| Q23 | 3 | input_ontology | "This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others." |
| Q24 | 3 | input_content | "These questions were sourced following an approach similar to AGIEVAL (Zhong et al., 2023), collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams, among others." |
| Q25 | 3 | input_content | "We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages." |
| Q26 | 3 | output_content | "These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers." |
| Q27 | 3 | input_ontology | "Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years." |
| Q28 | 3 | input_content | "Regional state exams are particularly valuable as they cover various state-level topics and emphasize the official language of each state." |
| Q29 | 3 | input_form | "In total, we collected more than 150K questions across 11 Indian Languages- Bengali (bn), Gujarati (gu), Hindi (hi), Kannada (kn), Malayalam (ml), Marathi (mr), Odia (or), Punjabi (pn), Tamil (ta), Telugu (te), and English (en)-spanning 41 diverse subjects." |
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
| Q46 | 4 | input_ontology | "In total, we release around 79K questions across 41 subjects across 8 domains in 11 languages, capping each subject-language pair at 500 questions for feasible evaluations." |
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
| Q91 | 10 | input_content | "Sumanth Doddapaneni, Rahul Aralikatte, Gowtham Ramesh, Shreya Goyal, Mitesh M. Khapra, Anoop Kunchukuttan, and Pratyush Kumar. 2023. Towards leaving no Indic language behind: Building monolingual corpora, benchmark and models for Indic languages. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 12402–12426, Toronto, Canada. Association for Computational Linguistics." |
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
    urbanization ~36% per Census 2011 but sub-national urban share for semi-urban
    exam aspirant cohort is not a published statistic and would require NSSO/survey
    data]'
target_population:
  description: Graduate-level students actively preparing for Indian central government
    competitive examinations (UPSC Civil Services, SSC CGL/CHSL, IBPS/SBI banking
    exams). Likely first-generation or semi-urban exam aspirants from Hindi-medium
    educational backgrounds. Access the system via smartphone (Android-dominant).
    Primary motivation is securing central government employment.
  education_level: Bachelor's degree (required eligibility for UPSC/SSC); many are
    recent graduates or repeat aspirants ('repeaters') in the 21–28 age band.
  age_band: 'Typically 21–28 years for active preparation phase. UPSC CSE 2024 had
    ~9.9 lakh applicants; the exam requires a minimum age of 21 and upper limit of
    32 for general category. SSC and banking exams have similar 18–30 ranges. (Source:
    UPSC CSE 2024 notification, PIB — [WEB-1];
    general eligibility criteria are stable across exam cycles.)'
  gender_breakdown: 'Women constituted approximately 35% of UPSC CSE selected candidates
    in 2023 (up from 24% in 2019), and roughly one-third of total UPSC applicants
    as of 2021–22 (≈3.37 lakh out of 10.4 lakh). For SSC and banking exams, female
    applicant share is not separately published but is broadly comparable. Source:
    Government of India response to Lok Sabha, December 2025 — [WEB-2];
    The Print analysis of UPSC annual reports — [WEB-3].
    Caveat: these are national selection/applicant figures; North India–specific gender
    breakdowns for the aspirant pool are not published.'
  occupational_role: Full-time or part-time exam aspirant; may also hold temporary
    employment or be enrolled in coaching institutes ('coaching classes') in cities
    like Prayagraj, Patna, Jaipur, Indore.
  coaching_institute_prevalence: '[NEEDS VERIFICATION — deferred: below search budget;
    national estimates vary widely (some studies suggest 60–70%+ of UPSC aspirants
    use some coaching), but a rigorous sub-national figure for North Indian central-exam
    aspirants specifically is not documented online; requires field survey data]'
  first_generation_learner_share: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (no published statistic); field research or coaching-institute surveys would be
    needed]'
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
  population_literacy_rate_hindi_states: 'Census 2011 (most recent national census):
    Bihar 63.8%, Uttar Pradesh 67.7%, Rajasthan 67.1%, Madhya Pradesh 70.6% — all
    below the national average of 74%. More recent PLFS 2023–24 data (Ministry of
    Statistics, published 2025) shows improvement: Bihar ~74.3%, Madhya Pradesh ~75.2%;
    UP and Rajasthan figures trending upward but remain below national average (~80.9%).
    Bihar historically had the lowest literacy among major states; Rajasthan has the
    largest male-female literacy gap. Caveat: these are population-level figures for
    persons aged 7+; the exam-aspirant cohort is graduate-level and near-universally
    literate within the deployment population. Source: Census 2011 via Scroll.in analysis
    — [WEB-4];
    PLFS 2023–24 via Wikipedia Literacy in India — [WEB-5].'
  graduate_level_literacy: Near-universal within the target cohort (graduate enrollment
    is an exam eligibility requirement).
  hindi_medium_undergraduate_share: '[NEEDS VERIFICATION — deferred: below search
    budget; no national or state-level published statistic on Hindi-medium versus
    English-medium undergraduate enrollment in UP, Bihar, Rajasthan, MP; requires
    UGC or AISHE survey data]'
  numeracy_notes: Mathematics and Reasoning are core exam subjects; aspirants have
    completed 10+2 mathematics. Advanced mathematics not required; arithmetic, data
    interpretation, and logical reasoning are the operative skills.
infrastructure_notes:
  device_profile: Android smartphone dominant; budget-to-mid-range handsets prevalent.
    iOS share low among this demographic.
  android_share_pct: '[NEEDS VERIFICATION — deferred: below search budget; national
    Android share in India is approximately 95%+ (StatCounter 2024) but no demographic-specific
    figure for North Indian exam aspirant cohort is published]'
  mobile_internet_penetration_target_states: 'As of Sep 2023 (TRAI data), UP (73.59M
    internet subscribers), Bihar (69.89M), and MP (62.85M) rank among the highest
    by raw subscriber count nationally, but internet density (subscribers per 100
    population) tells a different story: Bihar had the lowest internet density among
    all states and UTs at 35.31% (TRAI Consultation Paper, Dec 2022). IAMAI/Kantar
    ICUBE 2024 data shows internet penetration at approximately 46% for UP and 43%
    for Bihar among active internet users. A separate analysis (IAMAI/Kantar data
    via GrabOn 2026) notes that only ~4 out of 10 people in Bihar use the internet
    — the lowest in India. Rajasthan''s urban penetration is higher (~118 per 100
    urban population) while rural is lower. These are population-level figures; the
    semi-urban exam-aspirant cohort has substantially higher penetration than state
    averages. Source: TRAI Consultation Paper Sep 2023 — [WEB-6];
    Wikipedia Internet in India (TRAI Sep 2023 data) — [WEB-7];
    IAMAI ICUBE 2024 — [WEB-8].'
  connectivity: 4G coverage in urban/semi-urban areas adequate; rural connectivity
    patchy. App must be functional under low-bandwidth or intermittent connectivity
    conditions.
  data_cost_sensitivity: High — aspirants in this cohort are cost-sensitive; heavy
    data usage may be a barrier.
  app_modality: Mobile app (primary) and enterprise/web (secondary). Text-only interface;
    no image or audio input required.
  offline_capability_requirement: '[NEEDS VERIFICATION — deferred: low impact for
    scoring; this is a deployment-scope question (whether offline mode is implemented)
    rather than a verifiable external fact; requires deployment team confirmation]'
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
  upsc_subject_weight_note: 'Current Affairs is one of the most heavily and variably
    weighted areas of UPSC GS Paper 1, with direct current affairs questions ranging
    from 0 to 27 in a single year (2013–2016 data). Economy, History, Geography, Polity,
    Environment/Ecology each typically contribute 10–25 questions per paper. CSAT
    (Paper 2) covers Quantitative Aptitude and Logical Reasoning and is qualifying
    in nature (minimum 33%). SSC CGL Tier 1 covers General Intelligence/Reasoning,
    General Awareness, Quantitative Aptitude, and English Comprehension. Source: Testbook
    UPSC Prelims Weightage analysis — [WEB-9];
    SSC CGL Syllabus 2026 — [WEB-10].'
  syllabus_documents:
    upsc_syllabus: 'Official UPSC CSE Prelims syllabus available at UPSC website:
      [WEB-11]
      — direct PDF link changes annually with notification; see UPSC official site
      for current year.'
    ssc_cgl_syllabus: 'SSC CGL 2026 syllabus covers Tier 1 (General Intelligence,
      Reasoning, General Awareness, Quantitative Aptitude, English Comprehension)
      and Tier 2 (advanced Quantitative Abilities, English Language, Statistics, General
      Studies). Official PDF at ssc.gov.in; third-party summary: [WEB-10].'
    ibps_syllabus: '[NEEDS VERIFICATION — deferred: below search budget; IBPS PO syllabus
      is available at ibps.in but the exact current-year URL changes; the subject
      areas (Reasoning, Quantitative Aptitude, English Language, General Awareness,
      Computer Knowledge) are stable]'
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
  sensitive area. In UPSC CSE 2023, OBC candidates constituted 27% of selections and
  SC candidates 15%. Source: Sleepy Classes analysis of UPSC Annual Report 2022–23
  — [WEB-12].

  - Gender: Female aspirants constituted approximately 35% of UPSC CSE selected candidates
  in 2023 (up from 24% in 2019) and approximately one-third of total applicants as
  of 2021–22 (Source: Careers360/Govt Lok Sabha response — [WEB-2]).
  Women secured top ranks in UPSC CSE 2024 (top two positions). Coaching institutes
  and study environments remain male-dominated in many districts at the ground level.

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
  existing_hindi_nlg_evaluation_resources: 'No Hindi-language NLG evaluation benchmark
    specifically targeting competitive exam explanation quality was found. The closest
    adjacent resources are: (1) IndicGenBench (ACL 2024, Singh et al.) — covers 29
    Indic languages including Hindi for generation tasks (cross-lingual summarization,
    MT, QA), but does not cover exam explanation or pedagogical rationale quality.
    Source: [WEB-13]. (2) A 2025 preprint (''Benchmarking
    Hindi LLMs'', arXiv:2508.19831) introduces Hindi-adapted versions of IFEval, MT-Bench,
    and BFCL with Indian cultural themes, noting that ''benchmarks for critical skills
    like instruction following, conversational ability, and function calling... are
    largely unavailable publicly'' for Hindi instruction-tuned models. Source: [WEB-14].
    (3) Airavata (AI4Bharat, 2024) is a Hindi instruction-tuned LLM, but its evaluation
    uses IndicGenBench tasks rather than exam-explanation quality. No domain-specific
    Hindi exam rationale evaluation rubric or dataset exists; this is a confirmed
    gap requiring custom annotation design.'
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
  mathematics_and_reasoning: 'Quantitative aptitude (arithmetic, percentage, ratio,
    data interpretation) and logical/analytical reasoning are heavily tested in SSC
    and banking exams. UPSC CSAT Paper 2 covers these topics and is qualifying in
    nature (minimum 33%). MILU''s 8 macro-domains do not include Mathematics/Reasoning
    or Current Affairs as named categories; these subjects are either absent or subsumed
    under other domains in MILU''s taxonomy. Source: UPSC CSAT Syllabus — [WEB-15].'
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
    benchmark_coverage_status: '[NOT FOUND — searched for MILU Hindi items specifically
      covering North India sub-regional content (Chhath Puja, UP/Bihar land-revenue,
      zamindari, North Indian figures); no published breakdown of MILU''s Hindi item
      pool by sub-regional versus pan-India content exists. MILU''s paper confirms
      India-first design and culturally relevant subjects (local history, arts, festivals,
      laws) but does not publish granular item-level regional provenance for the Hindi
      partition. This remains an unresolved partial gap requiring examination of MILU''s
      released dataset (available under permissible licenses at AI4Bharat/Hugging
      Face).]'
benchmark_validity_flags:
  central_exam_subject_distribution:
    status: partial_gap
    detail: 'MILU draws from 40+ exam types including national and state exams, but
      proportion of Hindi items aligned to UPSC/SSC/banking versus state PSCs is undocumented.
      Mathematics/Reasoning and Current Affairs coverage in Hindi subset needs verification.
      MILU''s 8 macro-domains (Arts & Humanities, Social Sciences, Environmental Sciences,
      Law & Governance, Health & Medicine, Science, Engineering & Technology, Business
      Studies) do not explicitly list Mathematics/Reasoning or Current Affairs — which
      together constitute a large share of SSC CGL (Tier 1: 4 sections including Quantitative
      Aptitude and Reasoning) and UPSC CSAT Paper 2 content.'
    web_search_target: MILU benchmark Hindi subject distribution UPSC SSC banking
      exam coverage Mathematics Reasoning Current Affairs proportion
  hindi_code_mixing_rate:
    status: full_gap
    detail: No documentation of English code-mixing frequency in MILU Hindi items.
      ~25% of items translated from English via GPT-4O may introduce elevated code-mixing
      above the deployment's ~10% ceiling.
    web_search_target: MILU Hindi benchmark code-mixing English technical terms Devanagari
      item analysis Hindi-medium accessibility
  explanatory_rationale_quality:
    status: full_gap
    detail: 'MILU has no evaluation infrastructure for open-ended Hindi explanatory
      rationale. This is the deployment''s core output and is entirely outside benchmark
      scope. Search confirmed no Hindi-specific exam explanation quality benchmark
      exists; IndicGenBench (ACL 2024) covers generation tasks in Hindi but not exam
      rationale quality. A 2025 Hindi LLM benchmarking preprint (arXiv:2508.19831)
      explicitly notes that Hindi instruction-following and conversational evaluation
      benchmarks are ''largely unavailable publicly''. Source: [WEB-14].'
    web_search_target: Hindi language explanation quality evaluation NLG benchmark
      competitive exam rationale generation UPSC SSC
  north_india_sub_regional_content:
    status: partial_gap
    detail: MILU includes culturally relevant subjects but intra-Hindi regional granularity
      (North India–specific content within central-exam framing) is undocumented.
      No published item-level breakdown exists.
    web_search_target: MILU Hindi items North India regional knowledge Chhath Puja
      UP Bihar Rajasthan history land revenue systems sub-regional cultural content
  hindi_medium_difficulty_calibration:
    status: full_gap
    detail: 'No documentation on whether MILU Hindi items were calibrated for Hindi-medium
      graduates vs. English-medium or bilingual students. Annotator demographics not
      reported. The 2025 Hindi LLM benchmarking preprint (arXiv:2508.19831) notes
      a gap in evaluating instruction-tuned models for Hindi; existing benchmarks
      like MILU ''primarily target pre-trained base models''. Source: [WEB-14].'
    web_search_target: MILU benchmark Hindi-medium student accessibility difficulty
      calibration annotator demographics first-generation exam aspirants
  output_format_mismatch:
    status: full_gap
    detail: MILU uses MCQ label accuracy (log-likelihood or JSON generative scoring).
      Deployment requires open-ended Hindi rationale generation. Benchmark scores
      cannot directly validate deployment output quality.
    web_search_target: Hindi open-ended text generation evaluation fluency coherence
      pedagogical quality competitive exam AI feedback benchmark
regulatory_and_policy_context:
  data_protection: 'The Digital Personal Data Protection Act 2023 (DPDPA) is the applicable
    Indian data protection regulation. It applies to processing of digital personal
    data collected online within India. The associated DPDP Rules 2025 were officially
    notified on January 3, 2025 (per some sources) / November 13, 2025 (per MeitY/DLA
    Piper), with full compliance expected in a phased manner through May 2027. Key
    obligations for the deployment: user consent before processing personal data (with
    limited ''legitimate use'' exceptions), data minimization, and breach notification
    to the Data Protection Board of India. Unlike GDPR, DPDPA does not distinguish
    personal from sensitive personal data — all personal data is under a unified framework.
    Penalties up to ₹250 crore for non-compliance. Note: As of April 2026, the operational
    provisions of DPDPA are being phased in; until full implementation (expected May
    2027), the IT Act 2000 and IT (SPDI) Rules 2011 continue to govern. Source: MeitY
    official DPDPA text — [WEB-16];
    DLA Piper DataProtection.com India — [WEB-17];
    PRS India DPDP Bill analysis — [WEB-18].'
  ai_governance: 'MeitY released the India AI Governance Guidelines on November 5,
    2025, under the IndiaAI Mission — a principle-based, ''lightweight'' regulatory
    framework built on seven ''Sutras'' (Trust; People First; Innovation over Restraint;
    Fairness & Equity; Accountability; Understandable by Design; Safety, Resilience
    & Sustainability). The framework does not enact a dedicated AI law but relies
    on existing statutes with targeted amendments; an AI Governance Group (AIGG) and
    AI Safety Institute (AISI) are established for oversight. No sector-specific binding
    guidelines for AI in competitive exam preparation or edtech have been issued;
    the framework is currently advisory and pro-innovation. UGC''s 2022 undergraduate
    curriculum includes AI components. Source: MeitY PIB release — [WEB-1];
    Saikrishna & Associates analysis — [WEB-19];
    PIB AI in Education — [WEB-20].'
  exam_board_regulations: '[NOT FOUND — searched for UPSC/SSC/IBPS official guidelines
    on AI-assisted exam preparation; no such official restriction or endorsement found
    in public sources as of April 2026. Exam boards regulate the examination process
    itself but have not publicly issued guidance on AI preparation tools. This may
    require direct inquiry to UPSC, SSC, and IBPS.]'
  right_to_education_act_relevance: Not directly applicable (targets school-age education);
    graduate-level exam prep falls outside RTE scope.
net_new_fields:
  hindi_llm_instruction_following_gap:
    description: 'A 2025 preprint (arXiv:2508.19831, ''Benchmarking Hindi LLMs'')
      introduces IFEval-Hi, MT-Bench-Hi, and BFCL-Hi — Hindi-adapted versions of instruction-following
      and conversational benchmarks — noting that such benchmarks for Hindi instruction-tuned
      models were previously ''largely unavailable publicly''. This confirms the full_gap
      assessment for the deployment''s open-ended Hindi rationale output: no established
      Hindi benchmark covers pedagogical explanation quality, instruction adherence,
      or conversational coherence relevant to exam feedback. Relevance: strengthens
      the output_format_mismatch and explanatory_rationale_quality gap flags. Source:
      arXiv:2508.19831 — [WEB-14].'
    dimension: output_form
  indicgenbench_relevance_note:
    description: 'IndicGenBench (ACL 2024, Singh et al.) is the closest available
      Hindi generation evaluation benchmark, covering cross-lingual summarization,
      machine translation, and QA across 29 Indic languages. It is not specific to
      exam content or pedagogical rationale. A performance gap between English and
      Hindi on IndicGenBench tasks has been documented across all major LLMs, confirming
      that Hindi generation quality — even for high-resource Hindi — lags behind English-medium
      evaluation. Relevance: provides baseline evidence that Hindi generation (not
      just comprehension) is a validated risk dimension even for top models. Source:
      ACL Anthology — [WEB-13]; GitHub — [WEB-21].'
    dimension: output_form
  dpdp_rules_2025_compliance_timeline:
    description: 'The DPDP Rules 2025 were notified in November 2025, initiating a
      phased compliance rollout with full implementation expected by May 2027. Deployments
      processing student personal data (responses, performance logs, identity) must
      plan consent mechanisms, data minimization, and breach notification per DPDPA
      Section 4 and DPDP Rules. The 18-month compliance window (from November 2025
      notification) means deployments currently in operation should be actively redesigning
      consent flows. Relevance: exam prep apps collecting student performance data
      are directly within scope. Source: DLA Piper — [WEB-17];
      Captain Compliance DPDPA guide — [WEB-22].'
    dimension: regulatory
  upsc_cse_2024_scale_reference:
    description: 'UPSC CSE 2024 had ~9.92 lakh (992,599) applicants and 583,213 appeared
      for Prelims; 1,009 candidates were finally recommended (725 men, 284 women).
      Total UPSC applicant pool for 2024 is approximately 13.4 lakh registrations.
      This scale contextualizes the size of the target aspirant population; the deployment
      would serve a cohort drawn from this national pool, concentrated in North Indian
      states. Source: PIB UPSC CSE 2024 final result — [WEB-23].'
    dimension: target_population
  bihar_internet_density_caveat:
    description: 'Bihar had the lowest internet density of all Indian states and UTs
      at 35.31% as of TRAI''s Dec 2022 consultation paper, substantially below the
      national average. This is particularly relevant for Bihar-origin aspirants who
      may rely on shared or intermittent connectivity. The semi-urban exam-aspirant
      cohort (kasba/district town level) has higher connectivity than the state average
      but still meaningfully lower than urban peers in Delhi or Mumbai. Reinforces
      the offline_capability_requirement and data_cost_sensitivity flags. Source:
      TRAI Consultation Paper Sep 2023 — [WEB-6].'
    dimension: infrastructure
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2186639 |
| WEB-2 | https://news.careers360.com/womens-share-in-civil-services-up-from-24-35-pc-in-5-years-engineers-over-50-percent-government-data-upsc-ias-ips |
| WEB-3 | https://theprint.in/india/family-support-safety-study-material-a-click-away-whats-driving-more-women-to-take-upsc-exam/1922660/ |
| WEB-4 | https://scroll.in/article/825780/bihar-uttar-pradesh-rajasthan-and-madhya-pradesh-have-worst-literacy-rates-school-outcomes |
| WEB-5 | https://en.wikipedia.org/wiki/Literacy_in_India |
| WEB-6 | https://trai.gov.in/sites/default/files/2024-11/Cons_P_14092023.pdf |
| WEB-7 | https://en.wikipedia.org/wiki/Internet_in_India |
| WEB-8 | https://www.iamai.in/sites/default/files/research/Kantar_%20IAMAI%20report_2024_.pdf |
| WEB-9 | https://testbook.com/ias-preparation/upsc-prelims-subject-wise-weightage |
| WEB-10 | https://www.pw.live/ssc/exams/ssc-cgl-syllabus |
| WEB-11 | https://upsc.gov.in/examinations/active-examinations/civil-services-examination |
| WEB-12 | https://sleepyclasses.com/discover-how-many-candidates-are-selected-in-upsc-each-year/ |
| WEB-13 | https://aclanthology.org/2024.acl-long.595/ |
| WEB-14 | https://arxiv.org/html/2508.19831v1 |
| WEB-15 | https://vajiramandravi.com/upsc-exam/csat-syllabus/ |
| WEB-16 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-17 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-18 | https://prsindia.org/billtrack/digital-personal-data-protection-bill-2023 |
| WEB-19 | https://www.saikrishnaassociates.com/decoding-the-india-ai-governance-guidelines/ |
| WEB-20 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2234853&reg=3&lang=1 |
| WEB-21 | https://github.com/google-research-datasets/indic-gen-bench |
| WEB-22 | https://captaincompliance.com/education/dpdpa-india-the-complete-guide-to-indias-digital-personal-data-protection-act-2023/ |
| WEB-23 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2123422 |

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

**Dataset(s):** ai4bharat/MILU (Hindi config)
**Analysis date:** 2025-01-31
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | MILU/Hindi | 33 | option1 | "______ एक अदालत का आदेश है जो एक अधीनस्थ अदालत या सार्वजनिक प्राधिकरण को एक आधिकारिक कर्तव्य को सही ढंग से निभाने का निर्देश देता है।" | Mandamus writ definition question — Indian constitutional law | IO, IC |
| D2 | MILU/Hindi | 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" | Constitutional amendment adding 'armed rebellion' — Indian Polity | IO, IC |
| D3 | MILU/Hindi | 39 | option3 | "भारत में किस संवैधानिक संशोधन विधेयक द्वारा मतदान की आयु 21 वर्ष से घटाकर 18 वर्ष की गई थी?" | Constitutional amendment lowering voting age — Indian Polity | IO, IC |
| D4 | MILU/Hindi | 42 | option3 | "निम्नलिखित में से कौन मसौदा समिति का सदस्य नहीं था?" | Drafting committee membership — Indian Constitution | IO, IC |
| D5 | MILU/Hindi | 93 | option2 | "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है?" | Three-tier Panchayati Raj middle unit — Indian Governance | IO, IC |
| D6 | MILU/Hindi | 136 | option4 | "भारत के संविधान के अनुसार, संसद का कौन सा सदन संविधान संशोधन विधेयक पारित करता है?" | Which house passes constitutional amendment bill | IO, IC |
| D7 | MILU/Hindi | 50 | option3 | "1882 में भारत में स्थानीय स्वशासन की शुरुआत किसने की?" | Who introduced local self-government in India 1882 | IO, IC |
| D8 | MILU/Hindi | 199 | option4 | "1907 के कांग्रेस सत्र में उदारवादियों और उग्रवादियों के बीच मुख्य अंतर किस विषय पर था?" | 1907 Congress session — moderate vs extremist split | IO, IC |
| D9 | MILU/Hindi | 32 | option4 | "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया।" | Who completed Qutub Minar — Medieval Indian history | IO, IC |
| D10 | MILU/Hindi | 96 | option2 | "कौन सा अधिनियम प्रांतों में द्वैध शासन प्रणाली स्थापित करता है?" | Which act established dyarchy in provinces — Modern India history | IO, IC |
| D11 | MILU/Hindi | 158 | option3 | "'देवानांप्रिय' और 'प्रियदर्शी' वे उपाधियाँ थीं जिन्हें राजा ______ ने अपनाया था।" | Titles 'Devanampiya' and 'Priyadarshi' — Ashoka/Ancient India | IO, IC |
| D12 | MILU/Hindi | 237 | option3 | "मोहनजोदड़ो और हड़प्पा के खंडहर दिखाते हैं कि ये शानदार और अच्छी तरह से योजनाबद्ध ________ थे।" | Harappan civilization characterized as merchant cities | IO, IC |
| D13 | MILU/Hindi | 36 | option3 | "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है। TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______." | Letter series completion — Logical Reasoning | IO |
| D14 | MILU/Hindi | 44 | option2 | "दिए गए अक्षर श्रृंखला के रिक्त स्थानों में क्रमिक रूप से रखे जाने पर श्रृंखला को पूरा करने वाले अक्षरों के संयोजन का चयन करें। _q p p_p p_p p q_" | Letter pattern completion — Logical Reasoning | IO |
| D15 | MILU/Hindi | 84 | option3 | "सूरज ने अजय से एक निश्चित दर पर साधारण ब्याज पर दो वर्षों के लिए एक राशि उधार ली और उसे विनय को उसी दर पर वार्षिक चक्रवृद्धि ब्याज पर दो वर्षों के लिए उधार दिया।" | Simple vs. compound interest calculation — Quantitative Aptitude/Mathematics | IO |
| D16 | MILU/Hindi | 120 | option4 | "किसी कंपनी में सभी कर्मचारियों का औसत वेतन रु. 10500 है। सभी पुरुष कर्मचारियों का औसत वेतन रु. 15000 है।" | Average salary mixture problem — Quantitative Aptitude | IO |
| D17 | MILU/Hindi | 111 | option3 | "आठ लोग दो समानांतर पंक्तियों में बैठे हैं... A के ठीक विपरीत कौन बैठता है?" | Seating arrangement reasoning problem | IO |
| D18 | MILU/Hindi | 208 | option4 | "कथन: I. कुछ पेन कप हैं। II. सभी कप प्लेट हैं। निष्कर्ष: I. सभी पेन प्लेट हैं।" | Syllogism — formal logical reasoning | IO |
| D19 | MILU/Hindi | 74 | option4 | "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी?" | India GDP growth rate Q2 2018-19 — Current Affairs (dated) | IO, IC |
| D20 | MILU/Hindi | 132 | option4 | "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं?" | WCD Ministry head as of 2018 — Current Affairs (dated) | IO, IC |
| D21 | MILU/Hindi | 88 | option1 | "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान एक क्षुद्रग्रह पर उतरा। उस क्षुद्रग्रह का नाम है:" | JAXA asteroid landing 2019 — Current Affairs (dated) | IO, IC |
| D22 | MILU/Hindi | 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" | Archery Asia Cup 2022 India gold medals — Sports Current Affairs (dated) | IO, IC |
| D23 | MILU/Hindi | 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" | Mineral not found in Uttar Pradesh — North India–specific geography | IC |
| D24 | MILU/Hindi | 68 | option2 | "निम्नलिखित में से राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है?" | 'Bajju' reserve forest in Rajasthan — state-specific geography | IC |
| D25 | MILU/Hindi | 156 | option1 | "2011 की जनगणना के अनुसार राजस्थान की कुल साक्षरता का लगभग प्रतिशत कितना है?" | Rajasthan literacy rate 2011 — state-specific GK | IC |
| D26 | MILU/Hindi | 190 | option2 | "राजस्थान का आकार है-" | Shape of Rajasthan state — state-specific geography | IC |
| D27 | MILU/Hindi | 182 | option1 | "निम्नलिखित में से किस राज्य ने 2011-12 में सबसे अधिक दूध उत्पादन दर्ज किया?" | Highest milk production state 2011-12 — UP-specific GK | IC |
| D28 | MILU/Hindi | 242 | option4 | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है, जिसमें शिफॉन, मलमल, ऑर्गेंजा, ऑर्गेंडी और रेशम जैसे कपड़ों पर नाजुक पारंपरिक हाथ कढ़ाई की जाती है।" | Chikankari — UP traditional embroidery craft | IC |
| D29 | MILU/Hindi | 193 | option3 | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" | Kota painting school — Rajasthan art history | IC |
| D30 | MILU/Hindi | 198 | option2 | "छत्तीसगढ़ के निम्नलिखित विद्रोहों में से किसे 'बस्तर का स्वतंत्रता संग्राम' भी कहा जाता है?" | Chhattisgarh tribal rebellion — Central India history (outside North India core states) | IC |
| D31 | MILU/Hindi | 52 | option2 | "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था, वह था" | Pandya kingdom expansion — South Indian history, less relevant to UPSC North India focus | IC |
| D32 | MILU/Hindi | 108 | option3 | "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" | First cartoons in Tamil magazine — Tamil literary history | IC |
| D33 | MILU/Hindi | 126 | option3 | "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" | Telangana literary work — Telangana-specific cultural question | IC |
| D34 | MILU/Hindi | 41 | option1 | "टी-हब तेलंगाना राज्य सरकार की एक पहल है" | T-Hub Telangana tech incubator — state-specific non-central content | IC |
| D35 | MILU/Hindi | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" | DC series motor behavior — Engineering, not UPSC/SSC priority | IO |
| D36 | MILU/Hindi | 3 | option2 | "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" | Half-wave rectifier output — Electrical engineering technical content | IO |
| D37 | MILU/Hindi | 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" | FORTRAN 77 fixed format — specialist programming, not UPSC/SSC priority | IO |
| D38 | MILU/Hindi | 104 | option4 | "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" | Intermediate frequency for AM receivers — electronics engineering specialist content | IO |
| D39 | MILU/Hindi | 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं।" | William Wordsworth's nationality — English literature, minimal India relevance | IC |
| D40 | MILU/Hindi | 76 | option2 | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" | English vocabulary question: 'didactic' meaning — Language Studies, English vocabulary in Hindi context | IC, IF |
| D41 | MILU/Hindi | 90 | option3 | "शब्द 'grim' का पर्यायवाची लिखें।" | Synonym of English word 'grim' — English vocabulary tested in Hindi-labeled context | IC, IF |
| D42 | MILU/Hindi | 105 | option4 | "निर्देश: निम्नलिखित प्रश्न में, चार विकल्पों में से उस शब्द का चयन करें जो दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है। Evangelize" | English word 'Evangelize' meaning — English vocabulary question in Hindi dataset | IC, IF |
| D43 | MILU/Hindi | 56 | option2 | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें और दिए गए विकल्पों में से सही उत्तर चुनें: (1) और (3) केवल" | Ethanol statements question — options reference numbered statements absent from the question | IF |
| D44 | MILU/Hindi | 86 | option2 | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" | Multidimensional poverty states — options reference A/B/C/D/E labels with no list in question | IF |
| D45 | MILU/Hindi | 94 | option4 | "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? (केवल a, d) / (केवल b, c)" | Redox reactions question — options reference a/b/c/d labels absent from question text | IF |
| D46 | MILU/Hindi | 69 | option2 | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (b), (c) और (d)" | Pure substance — options reference items (a)/(b)/(c)/(d) absent from question | IF |
| D47 | MILU/Hindi | 95 | option1 | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं। AEDBCF" | Sentence ordering — sentences B/C/D/E absent from question text | IF |
| D48 | MILU/Hindi | 106 | option2 | "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" | Chronological ordering of substances — substance list absent from question | IF |
| D49 | MILU/Hindi | 109 | option4 | "छत्तीसगढ़ में नगरपालिकाओं के सभी चुनावों के संचालन के लिए पर्यवेक्षण, दिशा और नियंत्रण का प्रावधान किस अनुच्छेद में है? इनमें से कोई नहीं" | Article on municipality elections in Chhattisgarh — answer is 'none of these' suggesting data quality issue | OC |
| D50 | MILU/Hindi | 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" | Author of Mughal text Maasir-i-Alamgiri — Mughal history relevant to UPSC | IC |
| D51 | MILU/Hindi | 64 | option3 | "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है?" | 'Iron Man of India' — Sardar Patel, standard UPSC GK | IC |
| D52 | MILU/Hindi | 100 | option2 | "मध्यकालीन काल की सरकार एक मिश्रित संरचना थी। यह किन तत्वों का समामेलन था? फारसी-अरबी, तुर्को-मंगोल - भारतीय तत्व" | Medieval Indian governance structure — UPSC History topic | IC |
| D53 | MILU/Hindi | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" | is_translated=True — electrical engineering question translated from English | IC |
| D54 | MILU/Hindi | 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" | Indirect speech conversion — Hindi language grammar question | IC, IO |
| D55 | MILU/Hindi | 51 | option2 | "दिए गए वाक्य का सही सक्रिय रूप चुनें। सभी को उसके शानदार नृत्य प्रदर्शन ने मोहित कर दिया।" | Active voice conversion — Hindi grammar | IC, IO |
| D56 | MILU/Hindi | 83 | option1 | "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है... आदिवासी लोग जर्जर झोपड़ियों में रह रहे थे" | Ethics/governance scenario for senior civil officer — UPSC GS Paper IV Ethics | IO, IC |
| D57 | MILU/Hindi | 145 | option2 | "कौन सा अक्षर समूह प्रश्न चिह्न (?) को बदलकर दी गई श्रृंखला को पूरा करेगा? एमएनक्यू / एमओक्यू" | Letter series in Hindi transliteration of English letters — code-mixing in reasoning | IC, IF |
| D58 | MILU/Hindi | 18 | option3 | "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था?" | 1991 economic crisis trigger — Indian Economy/Current Affairs (historical) | IO, IC |
| D59 | MILU/Hindi | 119 | option2 | "आरबीआई के नोट जारी करने वाले विभाग के पास हमेशा न्यूनतम कितने मूल्य का सोना होना चाहिए?" | RBI minimum gold reserve requirement — Indian Economy | IO, IC |
| D60 | MILU/Hindi | 28 | option2 | "निम्नलिखित में से कौन खेरवार आंदोलन के नेता थे? भागीरथ मांझी" | Kherwar movement leader — tribal history in Jharkhand/Bihar context | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Strong Indian Polity and Governance Coverage
- **Dimension(s):** IO, IC
- **Observation:** The sample contains numerous questions directly aligned with UPSC/SSC priority topic of Indian Polity and Constitution — covering constitutional amendments (44th, 42nd), parliamentary procedures, Panchayati Raj, writs, and governance acts.
- **Deployment relevance:** Polity is one of the highest-weight subjects for UPSC GS Paper II and SSC General Awareness; these questions directly serve the deployment's primary subject requirements.
- **Datapoint citations:**
  - [D1] Example 33 (MILU/Hindi, validation, option1): "______ एक अदालत का आदेश है जो एक अधीनस्थ अदालत या सार्वजनिक प्राधिकरण को एक आधिकारिक कर्तव्य को सही ढंग से निभाने का निर्देश देता है।" — Mandamus writ definition, UPSC standard question type
  - [D2] Example 6 (MILU/Hindi, validation, option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — 44th Amendment question, core UPSC Polity
  - [D3] Example 39 (MILU/Hindi, validation, option3): "भारत में किस संवैधानिक संशोधन विधेयक द्वारा मतदान की आयु 21 वर्ष से घटाकर 18 वर्ष की गई थी?" — 61st Amendment, standard Polity question
  - [D5] Example 93 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है?" — Panchayati Raj, UPSC/SSC staple
  - [D6] Example 136 (MILU/Hindi, validation, option4): "भारत के संविधान के अनुसार, संसद का कौन सा सदन संविधान संशोधन विधेयक पारित करता है?" — Constitutional amendment procedure

#### Strength 2: Meaningful Indian History Coverage Including Medieval and Modern Periods
- **Dimension(s):** IO, IC
- **Observation:** The sample includes questions on Mughal history, ancient Indian civilization, modern independence movement, and colonial-era governance acts — all core UPSC History syllabus areas.
- **Deployment relevance:** History is a top-priority subject for central exams; these questions represent standard UPSC Prelims question types.
- **Datapoint citations:**
  - [D9] Example 32 (MILU/Hindi, validation, option4): "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया।" — Medieval Delhi Sultanate history
  - [D10] Example 96 (MILU/Hindi, validation, option2): "कौन सा अधिनियम प्रांतों में द्वैध शासन प्रणाली स्थापित करता है?" — Government of India Act 1919, standard modern history
  - [D11] Example 158 (MILU/Hindi, validation, option3): "'देवानांप्रिय' और 'प्रियदर्शी' वे उपाधियाँ थीं जिन्हें राजा ______ ने अपनाया था।" — Ashoka, Ancient Indian History
  - [D50] Example 25 (MILU/Hindi, validation, option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" — Mughal history, North India–relevant
  - [D52] Example 100 (MILU/Hindi, validation, option2): "मध्यकालीन काल की सरकार एक मिश्रित संरचना थी। यह किन तत्वों का समामेलन था?" — Medieval governance structure
  - [D8] Example 199 (MILU/Hindi, validation, option4): "1907 के कांग्रेस सत्र में उदारवादियों और उग्रवादियों के बीच मुख्य अंतर किस विषय पर था?" — Surat Split, modern Indian history

#### Strength 3: Logical Reasoning Representation in the Dataset
- **Dimension(s):** IO
- **Observation:** The sample contains a meaningful number of logical reasoning question types including seating arrangements, syllogisms, blood relations, letter/number series, and coding-decoding — which together constitute a significant share of SSC CGL and banking exam papers.
- **Deployment relevance:** Mathematics/Reasoning is flagged as a top-priority gap in MILU's documented taxonomy, but the actual data confirms Logical Reasoning is represented as a subject under the Science domain, partially addressing the gap for SSC/banking exam prep.
- **Datapoint citations:**
  - [D13] Example 36 (MILU/Hindi, validation, option3): "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है। TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______." — Letter series completion
  - [D17] Example 111 (MILU/Hindi, validation, option3): "आठ लोग दो समानांतर पंक्तियों में बैठे हैं...A के ठीक विपरीत कौन बैठता है?" — Seating arrangement
  - [D18] Example 208 (MILU/Hindi, validation, option4): "कथन: I. कुछ पेन कप हैं। II. सभी कप प्लेट हैं। निष्कर्ष: I. सभी पेन प्लेट हैं।" — Syllogism reasoning
  - [D14] Example 44 (MILU/Hindi, validation, option2): "दिए गए अक्षर श्रृंखला के रिक्त स्थानों में क्रमिक रूप से रखे जाने पर श्रृंखला को पूरा करने वाले अक्षरों के संयोजन का चयन करें। _q p p_p p_p p q_" — Letter pattern

#### Strength 4: Quantitative Aptitude Content Present
- **Dimension(s):** IO
- **Observation:** Several questions involve arithmetic calculations (simple/compound interest, averages, mixture problems) that are representative of the Quantitative Aptitude sections in SSC and banking exams. While labeled under Business Studies/Economics, these are functional math questions.
- **Deployment relevance:** Mathematics/Reasoning is the most critical undocumented gap in MILU's taxonomy; finding actual arithmetic content in the data partially mitigates this concern for SSC/banking preparation.
- **Datapoint citations:**
  - [D15] Example 84 (MILU/Hindi, validation, option3): "सूरज ने अजय से एक निश्चित दर पर साधारण ब्याज पर दो वर्षों के लिए एक राशि उधार ली...दो वर्षों के अंत में उसे 1230 रुपये का चक्रवृद्धि ब्याज प्राप्त हुआ।" — Simple vs. compound interest problem
  - [D16] Example 120 (MILU/Hindi, validation, option4): "किसी कंपनी में सभी कर्मचारियों का औसत वेतन रु. 10500 है...कंपनी में कुल कर्मचारियों की संख्या कितनी है?" — Mixture/average problem

#### Strength 5: North India–Specific Regional Content Present
- **Dimension(s):** IC
- **Observation:** Several questions address knowledge specifically relevant to North Indian states (UP, Rajasthan) — covering state-specific geography (minerals in UP), traditional crafts (Chikankari embroidery), literacy statistics (Rajasthan Census 2011), Rajasthan geography, and agricultural data (milk production leader UP).
- **Deployment relevance:** The deployment requires the AI to handle both pan-India GK and North India sub-regional content. These examples confirm that some such content is present, partially addressing the documented partial gap.
- **Datapoint citations:**
  - [D23] Example 26 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — UP-specific mineral geography
  - [D28] Example 242 (MILU/Hindi, validation, option4): "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है, जिसमें शिफॉन, मलमल, ऑर्गेंजा, ऑर्गेंडी और रेशम जैसे कपड़ों पर नाजुक पारंपरिक हाथ कढ़ाई की जाती है।" — Chikankari (UP embroidery)
  - [D25] Example 156 (MILU/Hindi, validation, option1): "2011 की जनगणना के अनुसार राजस्थान की कुल साक्षरता का लगभग प्रतिशत कितना है?" — Rajasthan state-specific statistics
  - [D27] Example 182 (MILU/Hindi, validation, option1): "निम्नलिखित में से किस राज्य ने 2011-12 में सबसे अधिक दूध उत्पादन दर्ज किया? उत्तर प्रदेश" — UP agricultural data
  - [D29] Example 193 (MILU/Hindi, validation, option3): "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" — Kota painting school (Rajasthan art)

#### Strength 6: Hindi Grammar and Language Proficiency Questions
- **Dimension(s):** IO, IC
- **Observation:** The dataset contains Hindi language grammar questions (active/passive voice, indirect speech, sentence structure) that align with the Hindi Language Proficiency component of central exams (UPSC Mains Hindi compulsory paper, SSC Hindi sections).
- **Deployment relevance:** Hindi language proficiency is listed as a priority subject area; these questions are in pure Hindi and reflect standard Hindi grammar exercises appropriate for the target student.
- **Datapoint citations:**
  - [D54] Example 9 (MILU/Hindi, validation, option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — Indirect speech conversion
  - [D55] Example 51 (MILU/Hindi, validation, option2): "दिए गए वाक्य का सही सक्रिय रूप चुनें। सभी को उसके शानदार नृत्य प्रदर्शन ने मोहित कर दिया।" — Active voice question

#### Strength 7: Ethics and Governance Scenarios (UPSC-Style)
- **Dimension(s):** IO, IC
- **Observation:** Example 83 presents a complex ethical scenario for a civil officer — a format directly mirroring UPSC GS Paper IV (Ethics, Integrity, Aptitude) case studies.
- **Deployment relevance:** UPSC aspirants must prepare for ethics-based scenario questions; this confirms MILU captures this question type, which is otherwise rare in competitive exam benchmarks.
- **Datapoint citations:**
  - [D56] Example 83 (MILU/Hindi, validation, option1): "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है...आदिवासी लोग जर्जर झोपड़ियों में रह रहे थे।" — UPSC-style ethics scenario

#### Strength 8: Indian Economy and Finance Coverage
- **Dimension(s):** IO, IC
- **Observation:** Questions on the 1991 economic crisis, RBI operations, MSP (Minimum Support Price), Five-Year Plans, PMMY (Pradhan Mantri Mudra Yojana), and banking sector are present — all standard Economics/GK topics in central exams.
- **Deployment relevance:** Indian economy is a consistently tested area in UPSC GS Paper III and SSC/banking exams.
- **Datapoint citations:**
  - [D58] Example 18 (MILU/Hindi, validation, option3): "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था?" — 1991 crisis
  - [D59] Example 119 (MILU/Hindi, validation, option2): "आरबीआई के नोट जारी करने वाले विभाग के पास हमेशा न्यूनतम कितने मूल्य का सोना होना चाहिए?" — RBI operations

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete Output Format Mismatch — No Explanatory Rationale Infrastructure
- **Dimension(s):** OO, OF
- **Observation:** Every example in the sample is structured as a 4-option MCQ with a single correct label (`target`). There are no rationale fields, explanation columns, or any annotation supporting the deployment's core output requirement: a substantive Hindi-language explanation of why an answer is correct or incorrect.
- **Deployment relevance:** The deployment explicitly requires "both a correct/incorrect label and a substantive explanation of why the answer is right or wrong, delivered in Hindi" (Elicitation Q3). MILU's schema (question, option1–4, target, is_translated, language, domain, subject) contains no field for rationale. This is a total mismatch with the deployed task; benchmark accuracy scores cannot validate whether a model produces accurate or coherent Hindi explanations. This is confirmed by the benchmark paper itself (Q85) and by the absence of any explanation field across all 245 reviewed examples.
- **Datapoint citations:**
  - [D1] Example 33 (MILU/Hindi, validation, option1): "______ एक अदालत का आदेश है जो एक अधीनस्थ अदालत..." — Correct answer is option1, but no explanation of why mandamus fits the definition is provided
  - [D15] Example 84 (MILU/Hindi, validation, option3): "सूरज ने अजय से एक निश्चित दर पर साधारण ब्याज पर दो वर्षों के लिए एक राशि उधार ली..." — Math problem with answer only; no worked solution or rationale
  - [D56] Example 83 (MILU/Hindi, validation, option1): "एक वरिष्ठ सिविल अधिकारी के रूप में..." — Ethics scenario answer marked option1 with no reasoning explaining why option1 is preferred over other plausible options

---

#### MAJOR

#### MAJOR Concern 1: Truncated/Self-Referential Questions — Construct-Irrelevant Variance
- **Dimension(s):** IF, OC
- **Observation:** A substantial number of questions (at minimum 5 identified in the 245-sample) have answer options that reference items, statements, or sentences that are absent from the question text itself. Options contain labels like "(a), (b), (c), (d)" or "1 2 3 4" or "AEDBCF" without the corresponding items being present in the question field. These appear to be reading-comprehension or list-based questions from which the source material was stripped during data collection, leaving the MCQ shell without the necessary context.
- **Deployment relevance:** A student interacting with these questions cannot evaluate the answer options without the missing content. Any model evaluated on these items is effectively guessing. For the deployment, presenting such incomplete questions would actively harm the student's learning experience, and benchmark accuracy on these items does not measure genuine knowledge.
- **Datapoint citations:**
  - [D43] Example 56 (MILU/Hindi, validation, option2): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें...विकल्प (1) और (3) केवल" — Options reference statements (1)(2)(3)(4) that are absent from question
  - [D44] Example 86 (MILU/Hindi, validation, option2): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" — Options reference states A/B/C/D/E with no list provided
  - [D45] Example 94 (MILU/Hindi, validation, option4): "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? केवल a, d" — Options reference reactions a/b/c/d absent from question
  - [D46] Example 69 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (b), (c) और (d)" — Options reference items (a)–(d) absent
  - [D48] Example 106 (MILU/Hindi, validation, option2): "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" — Substances to be ordered are absent from question
  - [D47] Example 95 (MILU/Hindi, validation, option1): "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं। AEDBCF" — Sentences B/C/D/E absent from question

#### MAJOR Concern 2: 100% Translation Rate in Observed Sample — Unknown Effect on Hindi Register
- **Dimension(s):** IC, IF
- **Observation:** Every single example in the 245-sample (all 245) has `is_translated=True`. This is the entire validation split reviewed. While the overall dataset is documented to have ~25% translated items, the validation split may have a substantially higher translation rate, or there may be a systematic sampling issue. All translated items were produced by GPT-4O, and the Hindi phrasing varies in naturalness.
- **Deployment relevance:** The deployment specifies a ~10% English code-mixing ceiling for Hindi-medium students. Machine-translated questions may use unnatural Hindi phrasing, Sanskritized vocabulary, or carry over English-medium structural conventions. For example, engineering and computer science questions (DC motor, FORTRAN, rectifier) that are entirely technical/specialist in nature appear translated into Hindi with mixed terminology. This inflates the engineering/technical content proportion and may introduce phrasing patterns foreign to Hindi-medium exam-style content.
- **Datapoint citations:**
  - [D53] Example 1 (MILU/Hindi, validation, is_translated=True): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" — Engineering question translated from English; typical Hindi-medium UPSC/SSC exam aspirants would not encounter DC motor questions
  - [D37] Example 8 (MILU/Hindi, validation, is_translated=True): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" — FORTRAN programming language question, translated; not in UPSC/SSC scope

#### MAJOR Concern 3: English-Language Questions Classified as Hindi Content
- **Dimension(s):** IC, IF
- **Observation:** Multiple questions in the Hindi-labeled dataset are substantively about English vocabulary — testing the meaning of English words ('grim', 'didactic', 'Evangelize') or converting English sentences — rather than being Hindi-medium content questions. These are labeled `language=Hindi` and `subject=Language Studies` but require knowledge of English vocabulary, not Hindi.
- **Deployment relevance:** The target student population has limited English exposure; a ~10% code-mixing ceiling applies. English vocabulary synonym questions embedded in the Hindi benchmark are a direct mismatch. A Hindi-medium student who cannot identify the synonym of 'grim' in English is not being tested on any UPSC/SSC competency — these exams do not test English vocabulary for Hindi-medium candidates. Benchmark performance on these items does not reflect the target student's actual exam competency.
- **Datapoint citations:**
  - [D41] Example 90 (MILU/Hindi, validation, option3): "शब्द 'grim' का पर्यायवाची लिखें।" — Asks for a synonym of the English word 'grim'; answer options are in Hindi, but the knowledge tested is English vocabulary
  - [D40] Example 76 (MILU/Hindi, validation, option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" — English vocabulary meaning question
  - [D42] Example 105 (MILU/Hindi, validation, option4): "निर्देश: निम्नलिखित प्रश्न में, चार विकल्पों में से उस शब्द का चयन करें जो दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है। Evangelize" — English word meaning question; options in Hindi but knowledge is English vocabulary

#### MAJOR Concern 4: Substantial Over-Representation of Engineering/Technical Content Irrelevant to Deployment
- **Dimension(s):** IO
- **Observation:** The sample contains a high density of specialist engineering and computer science questions (electrical engineering, FORTRAN programming, AM/FM modulation, DC motors, TDM frame rates, transfer machines, chopper circuits) that fall outside the scope of UPSC/SSC/banking central exam syllabi. These items appear predominantly translated from English and constitute a significant fraction of the sample.
- **Deployment relevance:** UPSC, SSC CGL, and banking exams do not test specialist engineering knowledge at this level. Benchmark accuracy on these items measures specialized engineering knowledge, not the GK/History/Polity/Reasoning competencies that the deployment targets. High model performance on engineering items inflates overall benchmark scores without corresponding validity for the deployment context.
- **Datapoint citations:**
  - [D35] Example 1 (MILU/Hindi, validation): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" — DC series motor behavior (Engineering)
  - [D36] Example 3 (MILU/Hindi, validation): "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" — Half-wave rectifier (Engineering)
  - [D37] Example 8 (MILU/Hindi, validation): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" — FORTRAN programming (Engineering/Computer Science)
  - [D38] Example 104 (MILU/Hindi, validation): "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" — Intermediate frequency for AM receivers (Engineering)

#### MAJOR Concern 5: Current Affairs Questions Are Significantly Dated
- **Dimension(s):** IC, IO
- **Observation:** Current Affairs is one of the most heavily weighted and dynamic UPSC GS areas. The sample contains multiple Current Affairs questions tied to specific dates in 2018–2022, including GDP growth rates for Q2 2018-19, cabinet minister assignments as of 2018, international events in 2019–2022. These questions would have stale or incorrect answers for students preparing for 2024-2026 exams.
- **Deployment relevance:** UPSC Current Affairs directly covers the preceding year; questions about 2018-2022 events are outdated for students currently preparing. A model evaluated highly on these items may still fail on current 2024-2025 affairs questions, and the benchmark cannot capture this currency dimension at all.
- **Datapoint citations:**
  - [D19] Example 74 (MILU/Hindi, validation, option4): "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी?" — GDP figure from 2018-19; outdated for current exam prep
  - [D20] Example 132 (MILU/Hindi, validation, option4): "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं?" — Ministry head as of 2018; politically outdated
  - [D21] Example 88 (MILU/Hindi, validation, option1): "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान एक क्षुद्रग्रह पर उतरा।" — 2019 space event Current Affairs
  - [D22] Example 2 (MILU/Hindi, validation, option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — 2022 sports event, dated

#### MAJOR Concern 6: Significant South India–Specific Content in Hindi Dataset
- **Dimension(s):** IC
- **Observation:** Several questions in the Hindi-labeled sample test knowledge that is specific to South Indian states (Telangana, Andhra Pradesh, Tamil Nadu) or South Indian literary/cultural heritage — including T-Hub Telangana, Tamil classical texts (Silappathikaram), Telangana book ('Telangana Rastrodayamalu'), Tamil cartoons, and Pandya kingdom history. While pan-India GK may include some of this, the density of Telangana/Tamil-specific items in a Hindi deployment is unexpected.
- **Deployment relevance:** Central exam syllabi do cover pan-India GK, but North India–based Hindi-medium students would not encounter these as high-priority preparation topics. Moreover, the benchmark documents that regional state exam questions are pooled across language partitions via translation — these may originate from Telugu/Tamil state exam questions translated into Hindi, representing a category mismatch for central-exam preparation.
- **Datapoint citations:**
  - [D33] Example 126 (MILU/Hindi, validation, option3): "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" — Telangana-specific literary question
  - [D34] Example 41 (MILU/Hindi, validation, option1): "टी-हब तेलंगाना राज्य सरकार की एक पहल है" — Telangana state government policy
  - [D32] Example 108 (MILU/Hindi, validation, option3): "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" — Tamil literary history question
  - [D31] Example 52 (MILU/Hindi, validation, option2): "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था" — Pandya kingdom (South Indian history)

---

#### MINOR

#### MINOR Concern 1: Reasoning Questions Use Transliterated English Letters, Introducing Mild Code-Mixing
- **Dimension(s):** IC, IF
- **Observation:** Some logical reasoning questions use transliterated English letter names in Hindi script (e.g., "एमएनक्यू", "एमओक्यू" for MNQ, MOQ) rather than Hindi-medium equivalent notation. While this is a minor form of code-mixing, it may create unnatural reading for students accustomed to Hindi-medium reasoning materials.
- **Deployment relevance:** The ~10% code-mixing ceiling is set for content, not isolated letter labels in pattern sequences; this is likely acceptable. However, the transliteration may be less natural than using the Latin letters directly (which Hindi-medium exam books do routinely).
- **Datapoint citations:**
  - [D57] Example 145 (MILU/Hindi, validation, option2): "कौन सा अक्षर समूह प्रश्न चिह्न (?) को बदलकर दी गई श्रृंखला को पूरा करेगा? एमएनक्यू / एमओक्यू" — Transliterated letter group names

#### MINOR Concern 2: Potential Answer Quality Issue — 'None of These' as Correct Answer for Factual Question
- **Dimension(s):** OC
- **Observation:** Example 109 asks about the constitutional article governing municipal election supervision in Chhattisgarh and the correct answer is "इनमें से कोई नहीं" (none of these). The provided options include Articles 243(ख), 243(क), and 241(ग). 'None of these' as the correct answer for a specific constitutional article question raises a potential data quality concern — either the correct article number was not included in the options, or the source portal recorded an ambiguous answer.
- **Deployment relevance:** Questions where 'none of these' is the correct answer are inherently difficult to explain in a rationale-based deployment, and may reflect data quality issues from the scraping pipeline (correct option not included in the option set).
- **Datapoint citations:**
  - [D49] Example 109 (MILU/Hindi, validation, option4): "छत्तीसगढ़ में नगरपालिकाओं के सभी चुनावों के संचालन के लिए पर्यवेक्षण, दिशा और नियंत्रण का प्रावधान किस अनुच्छेद में है? इनमें से कोई नहीं" — 'None of these' as answer to specific constitutional article query

#### MINOR Concern 3: Non-India–Specific Literary Questions with Low Deployment Relevance
- **Dimension(s):** IC
- **Observation:** A small number of questions test knowledge about non-Indian subjects that are tangentially connected to India's GK scope — such as the nationality of William Wordsworth or the 2019 Man Booker Prize winner (Bernadine Evaristo). These may appear in some competitive exam general awareness sections but are at the periphery of UPSC/SSC core content.
- **Deployment relevance:** These items represent minor dilution of deployment-relevant content. Their presence is not harmful but adds noise for the target student population.
- **Datapoint citations:**
  - [D39] Example 7 (MILU/Hindi, validation, option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं।" — Wordsworth's nationality, borderline relevance to central exam GK

---

### Content Coverage Summary

The 245-sample Hindi validation set covers a broad range of subjects with meaningful representation of Indian Polity/Constitution, Indian History (ancient, medieval, and modern), Indian Economy, Environmental Science/Geography, and Health/Medicine. Logical Reasoning (seating arrangements, syllogisms, blood relations, coding-decoding, series completion) is present as a subject under the Science domain, partially addressing the documented taxonomy gap. Quantitative arithmetic questions (simple/compound interest, averages) appear within Business Studies/Economics.

North India–specific content is present but not dominant: examples covering UP minerals, Chikankari (UP embroidery), Rajasthan geography and literacy, Kota painting, and Bihar/UP agricultural data confirm some sub-regional coverage. However, the sample does not include Chhath Puja, zamindari/land-revenue history, or North Indian freedom movement figures beyond Sardar Patel and general mentions.

A notable characteristic is that 100% of the 245 reviewed examples have `is_translated=True`, which may reflect the composition of the validation split specifically. The translated items include heavy representation of specialist Engineering & Technology and Computer Science content (DC motors, FORTRAN, AM/FM modulation, rectifiers) that falls outside UPSC/SSC/banking central exam syllabi. Several questions are structurally incomplete — answer options reference lists, statements, or sentences absent from the question text, likely artifacts of the source portal scraping process.

Current Affairs content is present but dated to 2018–2022, creating a staleness concern for students preparing for 2025–2026 central exams. English vocabulary questions (synonym/meaning of 'grim', 'didactic', 'Evangelize') are labeled as Hindi Language Studies content but test English word knowledge, which is misaligned with Hindi-medium students' target exam requirements.

The benchmark has no rationale or explanation fields — every item is a bare MCQ with a correct label only.

---

### Limitations

1. **Translation rate in validation split**: All 245 reviewed examples have `is_translated=True`. It is unclear whether this reflects the full validation split composition or a systematic ordering in the parquet file. The test split (14,831 examples) likely has a substantially different translation rate and subject distribution; findings about over-representation of engineering content and translation artifacts may not fully generalize.

2. **Sample size relative to total dataset**: 245 examples from a 14,831-example test set and 812-example validation set; topic distribution within the full dataset may differ from the sample. Rare subjects (Chhath Puja, land-revenue systems, specific North Indian historical figures) may be present in the full test set but absent from this sample.

3. **No inspection of test split**: The test set (14,831 examples) was not reviewed. Domain/subject distribution, translation rates, and data quality issues (truncated questions) in the test split are unconfirmed.

4. **Code-mixing cannot be quantified**: While specific English terms (RMS, AM, PCM, RBI, GDP, FORTRAN) appear in questions, a systematic quantitative estimate of English term density per question is not possible from manual review of 245 examples.

5. **Answer correctness not independently verifiable**: The target labels are inherited from exam portal answer keys. For the ~5 structurally truncated questions (where option lists are absent), the correctness of the labeled answer cannot be assessed without the original source.

6. **North India sub-regional coverage**: The sample confirms some UP/Rajasthan content but cannot establish whether Chhath Puja, zamindari abolition, specific North Indian freedom fighters, or Bihar-specific history appear in the test set at deployable density.

7. **Validation split composition uncertainty**: The fact that all 245 validation examples are translated may indicate the validation split was specifically constructed from translated items, or may be a coincidence of sampling order. This cannot be resolved without examining the full split statistics.

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
