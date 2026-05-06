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
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (configs: Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu)
**Analysis date:** 2025-08-01
**Examples reviewed:** 215 total (21 Bengali, 20 English, 24 Gujarati, 26 Hindi, 17 Kannada, 16 Malayalam, 21 Marathi, 21 Odia, 25 Punjabi, 19 Tamil, 25 Telugu) — all from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Hindi, validation | 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? … 44वें संविधान संशोधन अधिनियम द्वारा" | Polity/Constitution question in Hindi, about 44th Constitutional Amendment — UPSC core topic | IC, IO |
| D2 | Hindi, validation | 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? … साकी मुस्तईद खान" | Mughal-period history question in Hindi — directly relevant to North India medieval history | IC, IO |
| D3 | Hindi, validation | 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? … अभ्रक" | State-specific GK question about Uttar Pradesh minerals — North India sub-regional content | IC, IO |
| D4 | Hindi, validation | 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते? … आठ" | Current Affairs question (2022) about archery medal count — time-bounded, may be stale | IC, IO |
| D5 | Hindi, validation | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: … मोटर की गति बहुत अधिक होती है" | Engineering/Physics question in Hindi, `is_translated: True` — not in UPSC/SSC core syllabus | IC, IO |
| D6 | Hindi, validation | 3 | option2 | "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: … पल्सेटिंग डीसी" | Technical engineering question in Hindi, `is_translated: True` — domain not central to UPSC/SSC GS | IC, IO |
| D7 | Hindi, validation | 4 | option2 | "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। … शेल" | Electrical engineering, translated — technical domain not prioritized for Hindi-medium UPSC prep | IO |
| D8 | English, validation | 6 | option3 | "Fill in the gap below with suitable word. Fruit ∶ Reap∶∶ Flower ∶ _____… Bloom" | Logical Reasoning/analogy question in English — confirms presence of reasoning subject | IO |
| D9 | English, validation | 7 | option2 | "If Rs. 4000 becomes Rs. 5760 in 2 years at compound interest … what is the annual rate of interest? … 20 percent" | Mathematics/Quantitative Aptitude question (compound interest) — confirms presence in English partition | IO |
| D10 | Hindi, validation | 17 | option4 | "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? … संपत्ति कर" | Economics/direct tax question in Hindi — Economics is relevant to GK syllabus | IC |
| D11 | Hindi, validation | 13 | option1 | "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? … अरबी भाषा" | General Knowledge question in Hindi (monsoon etymology) — accessible, pan-India GK | IC |
| D12 | Hindi, validation | 19 | option3 | "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? … पाकिस्तान" | Geography GK question in Hindi — relevant to UPSC/SSC syllabus, Devanagari script, no English terms | IC, IF |
| D13 | Hindi (all examples) | all 26 | — | All 26 Hindi examples: is_translated = True | Every Hindi validation example in the sample is machine-translated from English | IC |
| D14 | English, validation | 1 | option3 | "What was the immediate cause for loss of foreign reserves triggering the financial crisis in 1991? … Sharp rise in value of imports of oil & petroleum products" | English original; same question appears in Hindi (D15) and Bengali — confirms translation pipeline | IC |
| D15 | Hindi, validation | 18 | option3 | "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था? … तेल और पेट्रोलियम उत्पादों के आयात के मूल्य में तीव्र वृद्धि" | Hindi translation of D14 — fluent Hindi, but `is_translated: True`, confirms translation pipeline | IC |
| D16 | Hindi, validation | 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है? … एक जंप लेबल या फॉर्मेट लेबल" | Computer Science / Fortran programming question in Hindi — very niche for UPSC/SSC aspirants | IO |
| D17 | Hindi, validation | 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा। … प्रबंधक ने अपने सहायक से कहा कि उसे अगले महीने बोनस मिलेगा।" | Hindi Language Studies question (indirect speech) — tests Hindi grammar directly | IC, IF |
| D18 | Hindi, validation | 22 | option4 | "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? … अमृता शेरगिल" | Arts & Culture GK in Hindi — pan-India Indian art figure | IC |
| D19 | Marathi, validation | 16 | option3 | "हलषष्ठी सण का साजरा केला जातो? … मुलाच्या दीर्घायुष्यासाठी" | Regional festival question in Marathi — culturally specific, regional content (not Hindi/North India) | IC |
| D20 | Gujarati, validation | 16 | option2 | "છત્તીસગઢના નીચેના કયા બળવાઓને 'બસ્તરનો સ્વાતંત્ર્ય સંઘર્ષ' પણ કહેવામાં આવે છે? … લિંગગિરી બળવો" | Chhattisgarh tribal revolt question — regional Indian history, culturally grounded | IC |
| D21 | Hindi, validation | 5 | option1 | "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं … सदाबहार ओक के पेड़ … भूमध्यसागरीय" | Geography question (Mediterranean climate) — translated, pan-India geography, no English code-mixing | IC, IF |
| D22 | English, validation | 3 | option4 | "What was the first capital of the Bahamani Kingdom? … Gulbarga" | India-specific historical knowledge (Deccan Sultanate) — same question appears across all languages | OC |
| D23 | Hindi, validation | 15 | option3 | "1950 में स्थापित, भारतीय रेलवे द्वारा स्वामित्व वाली औद्योगिक इकाइयों में से एक का नाम भारतीय स्वतंत्रता सेनानी के नाम पर रखा गया है: … चित्तरंजन दास" | Indian history/GK — freedom fighter named railway unit; is_translated: True | IC |
| D24 | English, validation | 9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct? … Estimate Committee: All members of this committee are from Assembly only." | State-level (Maharashtra) governance question in English partition — not central exam scope | IO |
| D25 | Punjabi, validation | 5 | option4 | "ਫਰਵਰੀ - ਮਾਰਚ 2022 ਵਿੱਚ ਹੋਈ ਰਾਜ ਵਿਧਾਨਸਭਾ ਚੋਣਾਂ ਵਿੱਚ, ਆਮ ਆਦਮੀ ਪਾਰਟੀ (AAP) ਨੇ … ਪੰਜਾਬ" | Current Affairs (2022 state elections) in Punjabi — politically specific, time-bounded | IC |
| D26 | Hindi, validation | 20 | option3 | "नेत्रगोलक लगभग गोलाकार होता है जिसकी व्यास लगभग कितनी होती है? … 2.3 सेमी" | Biology/Science question in Hindi — `is_translated: True`, basic science fact | IO |
| D27 | Telugu, validation | 25 | option1 | "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? … మొరెనా" | State-level GK (Madhya Pradesh industrial geography) in Telugu — regional, not central exam | IO |
| D28 | Hindi, validation | 24 | option4 | "तंगस्टन तत्व का प्रतीक क्या है? … W" | Chemistry/Science fact question in Hindi, `is_translated: True` — basic science, not UPSC priority | IO |
| D29 | Malayalam, validation | 6 | option1 | "ദേശീയ അടിയന്തരാവസ്ഥ പ്രഖ്യാപിക്കാൻ 'സായുധ കലാപം' എന്ന പദം ഭരണഘടനയിൽ ചേർത്തത് എപ്പോൾ? … 44-ാമത് ഭരണഘടനാ ഭേദഗതി നിയമം വഴി" | Same Constitutional Amendment question appears in Hindi (D1), Tamil, and Malayalam — cross-language duplication | IC, OC |
| D30 | Marathi, validation | 13 | option2 | "प्रांतांमध्ये द्वैधशासन प्रणाली कोणत्या कायद्याने स्थापन केली? … भारत सरकार अधिनियम 1919" | Indian constitutional history question (dyarchy) — India-specific, historically grounded | IC |
| D31 | English, validation | 15 | option3 | "Founded in 1950, one of the industrial units owned by Indian Railways is named after the Indian freedom fighter: … Chittaranjan Das" | India-specific GK, English original — Chittaranjan Das is a pan-India figure relevant to GK | IC |
| D32 | Hindi, validation | 11 | option2 | "संदीप माइकल निम्नलिखित में से किस खेल से जुड़े थे? … हॉकी" | Sports GK in Hindi — niche figure, is_translated: True | IC |
| D33 | Bengali, validation | 5 | option4 | "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) … পাঞ্জাব" | 2022 state elections Current Affairs — AAP, UP, Goa all named; time-bounded content | IC |
| D34 | English, validation | 11 | option2 | "The owner of the textile shop brought a … Calculator" | Incomplete stem — "brought a" with no further context; question appears malformed | IC, OC |
| D35 | Malayalam, validation | 14 | option4 | "ദിശകൾ: മാർബിൾ ഉപയോഗിക്കാവുന്നത് … ശിൽപ്പം" | Incomplete stem ("Directions: marble can be used") — same truncated structure appears across languages | IC, OC |
| D36 | Hindi, validation | 16 | — | "एएम की बैंडविड्थ _________ है। … 1110 kHz" | AM bandwidth engineering question — highly technical, `is_translated: True`; unlikely in UPSC GS | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Core UPSC/SSC Polity and Constitutional Law Coverage in Hindi
- **Dimension(s):** IO, IC
- **Observation:** The Hindi partition includes substantive questions on Indian constitutional law — specifically the 44th Constitutional Amendment (adding 'armed rebellion' for national emergency declaration) and other governance questions. These directly address the high-priority UPSC/SSC subject of Indian Polity & Constitution.
- **Deployment relevance:** For central exam aspirants, constitutional amendment questions are among the most tested areas in UPSC GS Paper 2 and SSC General Awareness. The Hindi rendering is clear and uses correct Devanagari terminology without excessive code-mixing.
- **Datapoint citations:**
  - [D1] Example 6 (Hindi, split=validation, label=option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? … 44वें संविधान संशोधन अधिनियम द्वारा" — UPSC-relevant Polity question in fluent Devanagari, no significant English intrusion.

#### Strength 2: Mughal and North Indian Medieval History Coverage
- **Dimension(s):** IO, IC
- **Observation:** The Hindi partition contains Mughal-period history questions (e.g., the authorship of 'Masir-e-Alamgiri') and pan-India medieval history questions (e.g., who completed the Qutb Minar). These are directly in scope for UPSC GS Paper 1 Indian history, with emphasis on the Delhi Sultanate and Mughal era that is especially prominent in North Indian exam preparation.
- **Deployment relevance:** Mughal administrative history and North Indian medieval landmarks are high-frequency topics in both UPSC and SSC GK sections. The Qutb Minar question also appears consistently across all language partitions, confirming it as a pan-India GK anchor.
- **Datapoint citations:**
  - [D2] Example 25 (Hindi, split=validation, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? … साकी मुस्तईद खान" — Mughal literary history, directly relevant to UPSC GS1.
  - [D22] Example 3 (English, split=validation, label=option4): "What was the first capital of the Bahamani Kingdom? … Gulbarga" — pan-India medieval history, same question appearing in all language partitions.

#### Strength 3: North India–Specific Regional GK Present in Hindi Partition
- **Dimension(s):** IC, IO
- **Observation:** The Hindi sample contains at least one question specifically about Uttar Pradesh's mineral resources, addressing sub-regional content within a central-exam framing. This is the type of India-within-India regional knowledge that the deployment requires the AI to handle.
- **Deployment relevance:** Central exams (UPSC, SSC) occasionally test state-specific geography and resource questions. The presence of a UP-specific item in the Hindi partition confirms that MILU does include some North India sub-regional content, partially addressing the documented gap.
- **Datapoint citations:**
  - [D3] Example 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? … अभ्रक" — UP state GK question in Hindi; directly serves the North India sub-regional layer.

#### Strength 4: Hindi Script Fidelity and Low Code-Mixing in Observed Examples
- **Dimension(s):** IF, IC
- **Observation:** Across all 26 Hindi examples examined, the questions and answer options are written in standard Devanagari. Technical terms are rendered in Hindi transliterations (e.g., "पल्सेटिंग डीसी" for "pulsating DC," "ट्रांसफार्मर" for transformer) or Hindi equivalents. Roman script or English-medium phrasing is minimal — the observed Hindi items do not appear to exceed the deployment's ~10% code-mixing ceiling.
- **Deployment relevance:** The target student population can read standard Devanagari Hindi; the absence of heavy Roman-script intrusion in the observed sample is a positive signal for accessibility.
- **Datapoint citations:**
  - [D12] Example 19 (Hindi, split=validation, label=option3): "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? … पाकिस्तान" — Pure Devanagari, no English terms.
  - [D21] Example 5 (Hindi, split=validation, label=option1): "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं … सदाबहार ओक के पेड़ … भूमध्यसागरीय" — "ओक" (oak) is retained as a transliterated loanword; "भूमध्यसागरीय" (Mediterranean) is a full Sanskrit-Hindi rendering — appropriate register.

#### Strength 5: Breadth of India-Centric General Knowledge Subjects
- **Dimension(s):** IO, IC
- **Observation:** Across the Hindi and English partitions, the sample contains questions spanning Economics (direct tax, 1991 financial crisis), Geography (Radcliffe Line, Mediterranean climate), Biology (eyeball diameter, Blue Baby Syndrome), Arts & Culture (Amrita Shergil), and History — consistent with the multi-domain pan-India GK coverage required for UPSC and SSC.
- **Deployment relevance:** The multi-domain spread matches the general awareness section tested across all central exams, confirming that the benchmark does not over-index on a single domain.
- **Datapoint citations:**
  - [D10] Example 17 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? … संपत्ति कर" — Economics GK in Hindi, UPSC/SSC relevant.
  - [D11] Example 13 (Hindi, split=validation, label=option1): "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? … अरबी भाषा" — GK in Hindi, accessible register.
  - [D18] Example 22 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? … अमृता शेरगिल" — Indian arts culture GK.

#### Strength 6: Presence of Logical Reasoning and Quantitative Questions (in English Partition)
- **Dimension(s):** IO
- **Observation:** The English partition includes both Logical Reasoning (analogy questions, coding-decoding in Telugu) and Quantitative Aptitude (compound interest calculation). These subjects correspond to UPSC CSAT Paper 2 and SSC CGL Tier 1, which are priority areas the deployment must cover.
- **Deployment relevance:** While these appear in the English partition specifically, their presence confirms that MILU's taxonomy does encompass the Reasoning and Mathematics domains that were flagged as potentially absent. The English partition is described as covering Indian-culture-specific content; the presence of reasoning questions here suggests the Hindi partition likely also has them.
- **Datapoint citations:**
  - [D8] Example 6 (English, split=validation, label=option3): "Fill in the gap below with suitable word. Fruit ∶ Reap∶∶ Flower ∶ _____ … Bloom" — Analogy reasoning question confirming domain presence.
  - [D9] Example 7 (English, split=validation, label=option2): "If Rs. 4000 becomes Rs. 5760 in 2 years at compound interest (compounded annually), then what is the annual rate of interest? … 20 percent" — Quantitative aptitude/compound interest.

#### Strength 7: Hindi Grammar and Language Proficiency Questions Present
- **Dimension(s):** IO, IC
- **Observation:** The Hindi partition includes a Hindi Language Studies question testing indirect speech transformation (reported speech) — a topic directly tested in UPSC Hindi language paper and SSC Hindi proficiency sections.
- **Deployment relevance:** Hindi language proficiency is explicitly listed as a priority subject for this deployment, and the benchmark contains at least some questions testing grammatical competence in Hindi.
- **Datapoint citations:**
  - [D17] Example 9 (Hindi, split=validation, label=option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा। … प्रबंधक ने अपने सहायक से कहा कि उसे अगले महीने बोनस मिलेगा।" — Hindi indirect speech transformation, tests Hindi grammatical knowledge.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: 100% Translation Rate in Hindi Validation Sample — No Natively Authored Hindi Questions Observed
- **Dimension(s):** IC
- **Observation:** All 26 Hindi validation examples in the sample carry `is_translated: True`. Not a single natively authored Hindi question appears in this sample. This means every Hindi question observed was originally written in English and translated via GPT-4O. The benchmark documentation states that only ~25% of the total dataset is translated; however, this sample suggests the Hindi validation partition may have a much higher translated proportion than the overall dataset average.
- **Deployment relevance:** This is critical for the deployment. Translated questions may not reflect the vocabulary conventions, sentence structures, or idiomatic phrasing of Hindi-medium competitive exam papers (which have their own established register). Questions authored in Hindi for exams like UPSC Hindi medium, UPPSC, or Hindi SSC papers have characteristic patterns that differ from back-translated English. If the Hindi partition predominantly consists of translated items, the benchmark may poorly represent the linguistic environment of the target student — and models fine-tuned or evaluated on translated Hindi may perform differently on authentically authored Hindi exam content.
- **Datapoint citations:**
  - [D13] All 26 examples (Hindi, split=validation): is_translated = True for all — "जब एक डीसी सीरीज मोटर बिना लोड के चलती है…", "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है…", "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह'…" — every item carries the translated flag.
  - [D15] Example 18 (Hindi, split=validation, label=option3): "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था?" — direct translation of D14 (English: "What was the immediate cause for loss of foreign reserves…"), confirming the translation pipeline.

#### CRITICAL Concern 2: Output Ontology Mismatch — MCQ Labels Only, No Explanatory Rationale Infrastructure
- **Dimension(s):** OO, OF
- **Observation:** Every datapoint in the dataset provides only a `target` field (one of option1–option4) as the ground-truth output. There is no rationale field, explanation field, or any annotation supporting the deployment's required output: a substantive Hindi-language explanation of why an answer is right or wrong.
- **Deployment relevance:** The deployment's core output is a correct/incorrect label **plus** a Hindi-language explanatory rationale (elicitation Q3). MILU benchmark scores measure only whether a model selects the correct MCQ option — they cannot validate whether the model's Hindi explanations are factually accurate, fluent, or pedagogically appropriate. This is a fundamental scope mismatch confirmed by direct inspection of the data schema. The paper's own limitation section acknowledges the log-likelihood evaluation may differ from generation-based approaches (Q85), but even generation-based scoring in MILU only assesses option selection.
- **Datapoint citations:**
  - [D1] Example 6 (Hindi, split=validation, label=option1): target = "option1" — the only output label is the MCQ choice; no rationale, no explanation field exists in the schema.
  - [D9] Example 7 (English, split=validation, label=option2): target = "option2" — compound interest answer with no worked solution or explanation provided; the schema has no field for this.

#### MAJOR

#### MAJOR Concern 1: Heavy Engineering/Technology Domain Skew in Hindi Sample — Misalignment with Central Exam Priority
- **Dimension(s):** IO
- **Observation:** Of the 26 Hindi validation examples, at least 7 are from Engineering & Tech (DC motor behavior, half-wave rectifier, constant current transformer, AM bandwidth, Fortran 77 column labels, wood swelling in timber, Materials Science) and 3 more are from Science (Computer Science, Biology). Together these constitute approximately 38% of the Hindi sample. By contrast, only 1 question is from Law & Governance (the 44th Amendment, D1) and only 2 are from Arts & Humanities with historical content (D2, D23).
- **Deployment relevance:** For UPSC/SSC/banking central exam preparation, Engineering & Tech and advanced Computer Science questions (e.g., Fortran 77 syntax, D16) are low-priority relative to History, Polity, Geography, and Economics. The observed sample distribution suggests the Hindi partition may over-represent technical domains (possibly because English engineering exam content was translated to fill gaps), which does not reflect the actual subject distribution of UPSC GS or SSC General Awareness syllabi.
- **Datapoint citations:**
  - [D5] Example 1 (Hindi, split=validation): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" — Engineering question, is_translated: True.
  - [D6] Example 3 (Hindi, split=validation): "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है" — Engineering question, is_translated: True.
  - [D7] Example 4 (Hindi, split=validation): "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है" — Engineering question, is_translated: True.
  - [D16] Example 8 (Hindi, split=validation): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है" — Niche Computer Science, is_translated: True; not in UPSC/SSC General Studies syllabus.
  - [D36] Example 16 (Hindi, split=validation): "एएम की बैंडविड्थ _________ है। … 1110 kHz" — Electrical engineering bandwidth, is_translated: True.

#### MAJOR Concern 2: Current Affairs Questions Are Time-Bounded and May Be Stale
- **Dimension(s):** IC, IO
- **Observation:** Multiple examples contain Current Affairs questions tied to specific years (2022 state elections, May 2022 archery tournament, 2020 Filmfare Awards, 2021 Padma Awards, Hillary Clinton's June 2014 book). MILU was published in 2024, and these questions reference events from 2014–2022 — meaning a significant portion of "Current Affairs" content is already dated and may not represent the current affairs knowledge tested in 2025–2026 exam cycles.
- **Deployment relevance:** Current Affairs is one of the most heavily weighted and variably tested areas of UPSC GS Paper 1 (confirmed in the web search context). For a deployment serving students preparing for 2025–2026 exam cycles, a benchmark sourced from exams up to ~2023 will have stale current affairs content. Model performance on MILU's Current Affairs items does not predict readiness for current exam cycles.
- **Datapoint citations:**
  - [D4] Example 2 (Hindi, split=validation): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — 2022 sports event; stale for 2025–26 exam prep.
  - [D25] Example 5 (Punjabi, split=validation): "ਫਰਵਰੀ - ਮਾਰਚ 2022 ਵਿੱਚ ਹੋਈ ਰਾਜ ਵਿਧਾਨਸਭਾ ਚੋਣਾਂ ਵਿੱਚ, ਆਮ ਆਦਮੀ ਪਾਰਟੀ (AAP) ਨੇ … ਪੰਜਾਬ" — 2022 election results; dated.

#### MAJOR Concern 3: Cross-Language Item Duplication Reduces Effective Question Pool Size
- **Dimension(s):** OC, IC
- **Observation:** The same factual questions appear identically translated across multiple language partitions. Examples include: the 1991 financial crisis question (Bengali Ex.1, English Ex.1, Hindi Ex.18, Malayalam Ex.1); the Bahamani Kingdom capital (Bengali Ex.3, English Ex.3, Gujarati Ex.3, Malayalam Ex.3, Punjabi Ex.3); the Qutb Minar completion (Bengali Ex.18, English Ex.18, Gujarati Ex.18, Hindi, Kannada Ex.15, Punjabi Ex.18, Tamil Ex.18); the Mediterranean climate question (English Ex.5, Gujarati Ex.5, Hindi Ex.5, Kannada Ex.5, Malayalam Ex.5, Marathi Ex.5, Punjabi, Tamil Ex.5, Telugu Ex.5). This pattern strongly suggests that a significant fraction of MILU consists of the same items translated, not independently sourced questions for each language.
- **Deployment relevance:** If the same items are used across language partitions via translation, the "79,000 questions" figure conflates distinct items with translated copies. For the Hindi partition specifically, the effective number of unique factual scenarios tested may be substantially smaller than the headline count suggests. Additionally, cross-language translation introduces a risk that questions originally designed for one language/exam context (e.g., SSC English) are not genuinely representative of the Hindi-medium exam ecosystem.
- **Datapoint citations:**
  - [D29] Example 6 (Malayalam, split=validation, label=option1): "ദേശീയ അടിയന്തരാവസ്ഥ പ്രഖ്യാപിക്കാൻ 'സായുധ കലാപം' എന്ന പദം ഭരണഘടനയിൽ ചേർത്തത് എപ്പോൾ?" — same 44th Amendment question as D1 (Hindi), D6 (Tamil), confirmed duplicate across Malayalam.
  - [D14] Example 1 (English, split=validation) and [D15] Example 18 (Hindi, split=validation): "What was the immediate cause for loss of foreign reserves…" / "1991 में वित्तीय संकट को ट्रिगर करने वाले…" — literal translation confirmed by is_translated field.

#### MAJOR Concern 4: Incomplete / Truncated Question Stems Observed
- **Dimension(s):** OC, IC
- **Observation:** At least two distinct examples contain severely truncated or incomplete question stems that do not provide enough context for meaningful answering. English Example 11 reads only "The owner of the textile shop brought a" with options including Computer, Calculator, Pencil, and Fountain pen — with no coherent question preceding this stem fragment. The marble/sculpture directions question appears similarly across Malayalam (Ex.14), Marathi (Ex.14), Telugu (Ex.14), Tamil (Ex.14) as "Directions: marble can be used" or equivalent, with options for painting, music, stones, and sculpture. These appear to be reading-comprehension remnants where the passage was stripped but the question fragment survived.
- **Deployment relevance:** Malformed or incomplete items undermine the validity of the benchmark. A model that encounters such items cannot answer based on the question content — any response is essentially random. If such items appear in the test split, they will add noise to accuracy scores in a way that is not informative about model quality. For a deployment context where the AI must explain the reasoning behind an answer, such items are particularly problematic.
- **Datapoint citations:**
  - [D34] Example 11 (English, split=validation, label=option2): "The owner of the textile shop brought a … Calculator" — No coherent question is present; the stem is a sentence fragment.
  - [D35] Example 14 (Malayalam, split=validation, label=option4): "ദിശകൾ: മാർബിൾ ഉപയോഗിക്കാവുന്നത് … ശിൽപ്പം" — Truncated "Directions:" stem without the relevant passage; same pattern in Marathi Ex.14, Telugu Ex.14, Tamil Ex.14.

#### MINOR

#### MINOR Concern 1: State-Level Content Mixed with Central Exam Content Without Labeling
- **Dimension(s):** IO
- **Observation:** Some items clearly pertain to state-level governance rather than central exams — for example, the Maharashtra Legislative Committee question (English Ex.9) and the Madhya Pradesh Banmore industrial area question (Telugu Ex.25). These are not labeled in the metadata as "state-PSC" versus "central exam" items, making it impossible to filter the benchmark for central-exam-only use without manual review.
- **Deployment relevance:** The deployment is explicitly scoped to central-level examinations (UPSC, SSC, banking), not state PSCs. Items about Maharashtra's legislative committee procedures or MP's industrial geography add noise if used for evaluating central-exam readiness but are not identifiable from the `domain` or `subject` metadata.
- **Datapoint citations:**
  - [D24] Example 9 (English, split=validation, label=option2): "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" — state-level governance question, not central exam scope.
  - [D27] Example 25 (Telugu, split=validation, label=option1): "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? … మొరెనా" — State-level (MP) geography question.

#### MINOR Concern 2: North India–Specific Sub-Regional Content Sparse in Observed Hindi Sample
- **Dimension(s):** IC
- **Observation:** Only one question in the Hindi sample (D3, UP minerals) could be classified as specifically North India sub-regional. No questions about Chhath Puja, Bhojpuri culture, zamindari systems, North Indian freedom movement figures (Chandrashekhar Azad, Ram Prasad Bismil), or UP/Bihar/Rajasthan administrative specifics were observed. The Mughal history question (D2) is pan-India/pan-subcontinental rather than specifically North Indian.
- **Deployment relevance:** The deployment must handle both pan-India GK and North India–specific content for central exams. The scarcity of observed North India sub-regional items (1 of 26) suggests this layer may be thinly represented in the Hindi partition, though a 26-item sample is insufficient to make a strong claim.
- **Datapoint citations:**
  - [D3] Example 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — the only observed North India–specific item in the Hindi sample.

#### MINOR Concern 3: Regional/State-Specific Cultural Content Appears Only in Non-Hindi Partitions
- **Dimension(s):** IC
- **Observation:** Culturally specific regional content (the Halashashthi festival in Marathi Ex.16, Lokranjan Mahotsav in Marathi/Gujarati, Chhattisgarh Bastar revolt in Gujarati/Kannada/Punjabi/Telugu, Sindhi poet Vasdev Mohi in Gujarati, Telangana literature in Kannada) appears in non-Hindi partitions. In the Hindi partition, no comparably region-specific Hindi-belt cultural content (festivals, literary traditions specific to Hindi-speaking North India) was observed.
- **Deployment relevance:** This creates a mild concern that MILU's culturally grounded content — which is a stated design strength — may be distributed toward South Indian and West Indian language partitions, where regional state exams provide richer locally sourced material. The Hindi partition, which is most important for this deployment, may rely more heavily on translated pan-India content than on natively sourced culturally specific Hindi exam content.
- **Datapoint citations:**
  - [D19] Example 16 (Marathi, split=validation, label=option3): "हलषष्ठी सण का साजरा केला जातो? … मुलाच्या दीर्घायुष्यासाठी" — Maharashtra-specific festival question; no equivalent Hindi-belt festival question observed.
  - [D20] Example 16 (Gujarati, split=validation, label=option2): "છત્તીસગઢના નીચેના કયા બળવાઓને 'બસ્તરનો સ્વાતંત્ર્ય સંઘર્ષ' … લિંગગિરી બળવો" — Chhattisgarh tribal revolt; this question also appears in Kannada, Punjabi, Telugu but not observed in Hindi.

---

### Content Coverage Summary

The MILU dataset, as observed across 215 examples from the validation split, is a large-scale MCQ benchmark with broad subject coverage across 11 Indic languages. The Hindi partition (26 examples) demonstrates adequate rendering in standard Devanagari with low observed code-mixing, and contains substantive content relevant to UPSC/SSC central exam topics including Indian constitutional law, Mughal history, and general knowledge in Economics and Geography.

However, two structural features substantially limit the benchmark's fit for this deployment. First, the entire Hindi validation sample is machine-translated (`is_translated: True` for all 26 items), raising questions about linguistic authenticity for the target population of Hindi-medium exam aspirants. Second, the observed domain distribution in the Hindi sample is skewed toward Engineering & Technology (DC motors, transformers, AM bandwidth, Fortran 77) — subjects that are peripheral to UPSC GS and SSC General Awareness. This skew likely results from the translation gap-filling strategy (translating English engineering exam questions to meet minimum thresholds) documented in the benchmark paper.

The English partition shows broader subject coverage, including Logical Reasoning and Mathematics questions, confirming these domains exist within MILU's taxonomy — but their representation in the Hindi partition specifically remains unverified from this sample.

Cross-language item duplication is pervasive: the same factual questions (Bahamani Kingdom capital, Qutb Minar, 1991 financial crisis, Mediterranean climate) appear identically translated across all 11 language partitions in the validation split. This is structurally expected for a translated benchmark but means the effective number of unique factual scenarios is smaller than the total item count implies.

Two malformed items with truncated stems were observed across multiple language partitions, suggesting imperfect filtering of reading-comprehension remnants from the scraping process.

The benchmark's output schema (MCQ `target` field only) provides no infrastructure for evaluating the Hindi-language explanatory rationale that constitutes the deployment's core output — a fundamental mismatch that cannot be remedied by data inspection alone.

---

### Limitations

1. **Sample size and representativeness:** Only validation split examples were examined (26 Hindi, 20–25 per other language). The test split contains approximately 6,600–10,000 examples per language config; the observed 100% translation rate in the Hindi validation sample cannot be generalized to the full test split without examining a larger sample. The actual distribution of natively authored vs. translated Hindi items in the test set requires direct inspection.

2. **Subject distribution cannot be quantified from this sample:** The 26 Hindi examples are insufficient to estimate the true proportion of Engineering/Tech vs. History/Polity/GK/Reasoning items in the Hindi test partition. The observed skew may be an artifact of the small validation sample.

3. **No test split content inspected:** All examples are from the validation split, which is used for few-shot examples in the benchmark's evaluation protocol. The test split (which is the actual evaluation set) was not sampled, and subject distributions may differ.

4. **Translation quality unassessable from inspection alone:** While observed Hindi items are fluent Devanagari, the quality of GPT-4O translations for technical domains (especially Electrical Engineering, Computer Science) relative to authentic Hindi exam register cannot be assessed through casual reading — it would require review by a Hindi-medium domain expert.

5. **No audio or image modality:** These are excluded by MILU's design; no inspectability concern applies.

6. **Rationale quality entirely outside data scope:** The deployment's core output (Hindi explanatory rationale) is wholly absent from the dataset schema. No amount of data inspection can assess this dimension; it requires a separate evaluation framework.

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
