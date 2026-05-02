I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **ArabicMMLU: Evaluating Language Models on the Arabic Language and its Culture** is valid for use in **Non-Arab Tourists and Expats in Eight Arabic-Speaking Countries (ArabicMMLU Deployment)**.

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

- **Name**: arabicmmlu
- **Full Name**: ArabicMMLU: Evaluating Language Models on the Arabic Language and its Culture
- **Domain**: Arabic language and cultural knowledge understanding
- **Languages**: ar
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
ArabicMMLU represents a deliberate shift from linguistically-centric NLP tasks
(POS tagging, NER) toward knowledge and reasoning evaluation [Q10], framed as
40 tasks spanning school subjects across primary, middle, high school, and
university levels [Q25, Q28]. Subject groups include STEM, Social Science,
Humanities, Arabic Language, and Other [Q107], and several subjects —
history, geography, civics, political science — are explicitly flagged as
likely to contain Arabic-specific content [Q72, Q73]. This design decision
aligns with the deployment's school-curriculum framing for general-knowledge
assistance. However, the taxonomy has structural gaps relevant to deployment:
university-level content comprises only 6% of the dataset [Q71], leaving
higher-complexity knowledge thinly represented; and high school questions are
documented as substantially harder than primary and middle school items [Q68].
The negation-sensitivity analysis [Q84] reveals an additional taxonomic
dimension (linguistic perturbation robustness) that is not integrated into the
main subject taxonomy. Future extensions proposed by the authors — short-answer
questions, multimodal content, larger regional coverage, professional-domain
content [Q88] — all represent current gaps, particularly for deployment
scenarios requiring explanatory or multi-country-scoped responses. Most
critically, the benchmark's single-correct-answer MCQ structure collapses
inherently contested historical and civic questions (e.g., Palestinian history,
pan-Arab political geography) into a forced-choice frame [Q100], meaning the
taxonomy cannot represent the output type — multi-perspective acknowledgment —
that the deployment explicitly requires.

### Input Content
Questions are sourced from authentic school examination materials across eight
countries spanning North Africa (Morocco and Egypt), the Levant (Jordan,
Palestine, and Lebanon), and the Gulf (UAE, Kuwait, and KSA) [Q26], making
ArabicMMLU distinct from prior Arabic benchmarks that relied on English-to-Arabic
translation of MMLU [Q5, Q6]. Data collection was conducted by 10 native
Arabic-speaking workers [Q31] who identified publicly available exam URLs [Q32]
and manually scraped metadata including source, country, subject, level,
question text, options, and answer key [Q33, Q34]. This ground-up collection
approach supports authentic regional grounding in principle. However, geographic
distribution is highly unequal: Jordan contributes over 6,000 questions while
some countries contribute as few as 100 [Q89], driven by differential
digitization of national exams [Q90] and a non-exhaustive internet search [Q91].
The worker pool skews toward Jordanian and Egyptian nationals [Q31], with
acknowledged collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia
[Q96] — but not Morocco or Palestine. Morocco's Maghrebi curriculum and
French-influenced educational tradition, and Palestine's politically distinct
historical narratives, are therefore likely absent or severely underrepresented
in both source documents and the workforce that collected them. The GPT-4
performance gap between translated MMLU (80%) and ArabicMMLU (72.5%) is
attributed to the higher proportion of Arabic-specific content in the latter
[Q64, Q65], supporting construct validity for culturally grounded knowledge
while simultaneously confirming that the content is not a pan-Arabic generalization
but one with differential regional representation.

### Input Form
All 14,575 questions are in Modern Standard Arabic (MSA), text-only format,
with 2–5 candidate answer options per question [Q2, Q27]. The decision to
exclude English-language questions and include only Arabic-language questions
[Q30] reflects the educational reality that public schools in the target
countries use Arabic for instruction and assessment [Q29]. Questions containing
multimodal content (images, videos, tables) were discarded during scraping
[Q37]; contextual passages were retained where dependent questions required
them [Q38]. Arabic negation phrases were used for negation detection in the
analysis [Q85]. Prompts are available in both Arabic and English versions with
structured placeholders [Q49, Q99]. The text-only MSA format aligns with
the deployment's text-based modality [Q93], but creates a signal-distribution
gap for the actual user population: non-native Arabic learners whose input
Arabic may be grammatically imperfect, code-switched, or at learner register
[Q92] — a mismatch that is structural and undocumented as a design trade-off.

### Output Ontology
The label schema is exclusively single-correct-answer MCQ: each question has
2–5 candidate options with exactly one marked correct [Q27]. No partial-credit,
multi-answer, confidence-tier, or open-ended categories are documented anywhere
in the paper. The four prompt configurations tested (Arabic/Arabic, Arabic/English,
English/Arabic, English/English) [Q47] vary only in prompt language and output
script, not in the fundamental label structure. The finding that English prompt
with English alphabetic output yields best overall performance [Q56], while
Arabic-centric models are most robust with Arabic alphabetic output [Q57],
reflects output-form sensitivity but not output-ontology diversity. The
benchmark's inability to evaluate multi-perspective or explanatory responses is
acknowledged only indirectly, via the future-work note proposing short-answer
and essay questions [Q88]. For the deployment scenario, this is the most critical
structural mismatch: the system is required to acknowledge competing national
positions on contested historical and civic questions [Q72, Q73], but the
benchmark's output taxonomy structurally cannot represent or score such responses.

### Output Content
Answer key accuracy was verified by having two native Arabic speakers independently
assess 100 randomly sampled questions using available resources such as search
engines, yielding a 96% match rate [Q42, Q43]. This establishes a practical
accuracy ceiling: up to 4% of questions may carry incorrect ground-truth labels
[Q44]. Workers are native MSA speakers with at least Bachelor's degrees [Q39],
and internal workers are Master's students and Research Assistants in Computer
Science [Q35]; competitive compensation exceeding monthly average wages in each
country was paid [Q36]; and a one-hour onboarding workshop was held before
collection [Q40]. The annotation pool's demographic concentration (3 Jordanian
and 1 Egyptian external workers; internal workers from Jordan, Egypt, Lebanon,
UAE, and KSA) [Q31] means Moroccan and Palestinian cultural perspectives on
historically sensitive content are structurally absent from both collection and
verification. For contested historical questions where the "correct" answer
differs across national curricula, the 96% agreement figure may reflect
Jordanian/Egyptian consensus rather than regional validity. Training data
contamination risk is also acknowledged as unverifiable [Q95].

### Output Form
The benchmark measures performance as percentage accuracy (% correct MCQ answers)
across 35 models in zero-shot and few-shot settings [Q3, Q45]. For open-source
models, answers are determined by the highest token probability among candidate
options, using softmax normalization [Q50, Q79]; for closed-source models, by
regex matching on the first generated token with random assignment if no match
[Q53, Q54]. Additional output-form analyses cover model calibration (r > 0.9
for the three best open-source models) [Q80], question-length vs. confidence
correlation (none found) [Q82], few-shot vs. zero-shot performance trends
[Q75, Q76], and negation sensitivity [Q83, Q84]. The benchmark is text-based
and assesses discrete label accuracy — a form entirely appropriate for literacy-
capable populations [Q93] but fundamentally misaligned with the deployment's
requirement for open-ended, explanatory, multi-perspective natural-language
responses. The benchmark cannot evaluate whether a model provides appropriately
nuanced answers flagging country-specific positions, as this output form is
entirely absent from the evaluation methodology.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we present ArabicMMLU, the first multi-task language understanding benchmark for the Arabic language, sourced from school exams across diverse educational levels in different countries spanning North Africa, the Levant, and the Gulf regions." |
| Q2 | 1 | input_form | "Our data comprises 40 tasks and 14,575 multiple-choice questions in Modern Standard Arabic (MSA) and is carefully constructed by collaborating with native speakers in the region." |
| Q3 | 1 | output_form | "Our comprehensive evaluations of 35 models reveal substantial room for improvement, particularly among the best open-source models." |
| Q4 | 1 | output_form | "Notably, BLOOMZ, mT0, LLaMA2, and Falcon struggle to achieve a score of 50%, while even the top-performing Arabic-centric model only achieves a score of 62.3%." |
| Q5 | 1 | input_content | "Although large language models (LLMs) such as GPT-3.5 (Ouyang et al., 2022), BLOOMZ (Muennighoff et al., 2022), and Jais (Sengupta et al., 2023) have been pretrained with substantial coverage of Modern Standard Arabic (MSA), their reasoning and knowledge assessments are primarily conducted using datasets translated from English to Arabic (Sengupta et al., 2023; Huang et al., 2023), which means there is limited capacity to evaluate content specific to Arabic." |
| Q6 | 1 | input_content | "This reliance on translation systems not only demonstrates an Anglocentric approach (Ramesh et al., 2023; Talat et al., 2022) but also potentially introduces errors and biases." |
| Q7 | 1 | input_content | "Given that Arabic is one of the most widely-spoken languages in the world, with a speaker population of over 400 million people (Shoufan and Alameri, 2015; Diab et al., 2017), it is critically important that datasets be constructed for the language that are regionally- and culturally-localized." |
| Q8 | 1 | output_content | "Fajri Koto, Haonan Li, Sara Shatnawi, Jad Doughman, Abdelrahman Boda Sadallah, Aisha Alraeesi, Khalid Almubarak, Zaid Alyafeai, Neha Sengupta, Shady Shehata, Nizar Habash, Preslav Nakov, Timothy Baldwin" |
| Q9 | 1 | output_content | "Department of Natural Language Processing, MBZUAI; Prince Sattam bin Abdulaziz University; King Fahd University of Petroleum and Minerals; Core42; New York University Abu Dhabi; The University of Melbourne" |
| Q10 | 1 | input_ontology | "The evaluation of language models has increasingly shifted from linguistically-centric tasks, such as part-of-speech (POS) tagging and named entity recognition (NER), towards reasoning and knowledge evaluation." |
| Q11 | 2 | input_content | "Early Arabic pretrained language models typically had less than 2 billion parameters and were primarily monolingual." |
| Q12 | 2 | input_ontology | "These models can be classified into three main categories: encoder-only, decoder-only, and encoder–decoder models." |
| Q13 | 2 | output_content | "The encoder-only models, such as AraBERT (Antoun et al., 2020), CAMeLBERT (Inoue et al., 2021), AraELECTRA (Antoun et al., 2021a), and ARBERT & MARBERT (Abdul-Mageed et al., 2021), are mainly from the BERT family." |
| Q14 | 2 | output_content | "AraGPT2 (Antoun et al., 2021b), on the other hand, is a decoder-only model available in different sizes ranging from 135M to 1.4B parameters." |
| Q15 | 2 | output_content | "Examples of encoder–decoder models include AraT5 (Nagoudi et al., 2022) and AraBART (Kamal Eddine et al., 2022)." |
| Q16 | 2 | output_content | "Jais (Sengupta et al., 2023) and AceGPT (Huang et al., 2023) are two recent Arabic-centric decoder-only models with parameter sizes of up to 30B and 13B, respectively." |
| Q17 | 2 | input_content | "Jais is pretrained on a corpus of 72 billion Arabic tokens, while AceGPT builds upon LLaMA2 and is enhanced with reinforcement learning from AI feedback (Lee et al., 2023) to localize the model to Arabic values and culture." |
| Q18 | 2 | output_content | "Both models are bilingual (English and Arabic), and were fine-tuned on various instruction datasets." |
| Q19 | 2 | input_content | "Arabic is also present in multilingual models." |
| Q20 | 2 | output_form | "This includes earlier models such as mBERT (Devlin et al., 2019) and XLM-R (Conneau et al., 2020), and more recent LLMs such as BLOOMZ (Muennighoff et al., 2022), mT0 (Muennighoff et al., 2022), Falcon (Penedo et al., 2023), GPT-3.5 (Ouyang et al., 2022), and GPT-4 (OpenAI, 2023)." |
| Q21 | 2 | output_form | "In the original papers, only GPT-4 was evaluated in Arabic in terms of its reasoning and knowledge capabilities, using the English–Arabic translated MMLU dataset, reporting an accuracy of 80%." |
| Q22 | 2 | input_content | "Arabic is included in various multilingual benchmarks for natural language understanding and generation, such as XGLUE (Liang et al., 2020), XTREME (Hu et al., 2020), XTREME-R (Ruder et al., 2021) and GEM (Gehrmann et al., 2021)." |
| Q23 | 2 | input_content | "In recent years, several Arabic-centric benchmarks have been released, such as Dolphin (Nagoudi et al., 2023), OCRA (Elmadany et al., 2023), and LAraBench (Abdelali et al., 2024)." |
| Q24 | 2 | input_ontology | "Many tasks in these benchmarks involve classification, such as natural language." |
| Q25 | 3 | input_ontology | "ArabicMMLU is an Arabic multiple-choice question-answering dataset comprising 40 tasks spanning a wide range of subjects and education levels." |
| Q26 | 3 | input_content | "The questions are sourced from eight different countries in North Africa (Morocco and Egypt), the Levant (Jordan, Palestine, and Lebanon), and the Gulf (UAE, Kuwait, and KSA)." |
| Q27 | 3 | output_ontology | "Each question has 2–5 candidate answers, with one correct answer." |
| Q28 | 3 | input_ontology | "The subjects are drawn from different education levels (primary school, middle school, and KSA, prioritize Islamic studies alongside subjects like mathematics, natural science, social science, and geography." |
| Q29 | 3 | input_form | "In public schools, Arabic is commonly used for teaching and assessment, while in international schools, English is the predominant language of instruction for most subjects, following either the UK or USA curriculum." |
| Q30 | 3 | input_form | "When designing ArabicMMLU, we excluded questions in English and only included questions in Arabic." |
| Q31 | 4 | output_content | "The data construction process involved a total of 10 Arabic native speakers from different countries: 6 internal workers (1 Jordanian, 1 Egyptian, 1 Lebanese, 1 from UAE, and 2 from KSA) and 4 external workers (3 Jordanian and 1 Egyptian)." |
| Q32 | 4 | input_content | "During the first stage of data collection, the internal workers were tasked with collecting relevant sources for data collection. These sources were URLs containing the questions, which needed to be publicly available." |
| Q33 | 4 | input_content | "In the second stage, all workers were asked to manually scrape the data within a 2-month period. The task was to collect metadata, including the source (URL of the source document), country, subject, level, question, multiple-choice options, and the correct answer key." |
| Q34 | 4 | input_content | "Each external worker was assigned to gather 2,000 questions, while internal workers were tasked with gathering 1,000–2,000 questions each." |
| Q35 | 4 | output_content | "Our internal workers are Master's students and Research Assistants in Computer Science, while the external workers hold Bachelor's degrees." |
| Q36 | 4 | output_content | "We ensured competitive compensation for the workers, exceeding the monthly average wage in each respective country." |
| Q37 | 4 | input_form | "During manual data scraping, workers were instructed to include only questions accompanied by an answer key, and to discard questions containing multi-modal information (e.g., images, videos, or tables)." |
| Q38 | 4 | input_form | "If a question had additional contextual information (e.g., a passage referenced by several questions), the context was required to be included with each corresponding question." |
| Q39 | 4 | output_content | "While our workers are native speakers of Modern Standard Arabic with at least Bachelor's degrees, we maintain the quality of our dataset construction through meticulous steps." |
| Q40 | 4 | output_content | "Firstly, we conducted a 1-hour workshop before the data collection stage to clarify the process." |
| Q41 | 4 | input_content | "Secondly, we automatically filtered out repetitive questions and those without an answer key, reducing the initial set of over 15,000 questions to 14,575 unique questions." |
| Q42 | 4 | output_content | "Finally, we assessed the accuracy of our data collection by having two native Arabic speakers annotate 100 randomly sampled questions. They were provided with all metadata, including the answer key, and tasked with verifying the correctness of each sample using any available resources (e.g., search engines)." |
| Q43 | 4 | output_content | "We found that 96% of the questions and answer keys match on average, while the remaining could have incorrect answer keys." |
| Q44 | 4 | output_content | "This 96% score is considered to represent the maximum score meaningfully achievable for ArabicMMLU." |
| Q45 | 5 | output_form | "Our experiments focus on zero-shot and few-shot settings across 35 models." |
| Q46 | 5 | output_form | "This includes 22 open-source multilingual models (XGLM (Lin et al., 2022), BLOOMZ (Muennighoff et al., 2022), mT0 (Muennighoff et al., 2022), Falcon (Penedo et al., 2023), and LLaMA2 (Touvron et al., 2023), across various sizes), 11 open-source Arabic-centric models (AraT5 (Nagoudi et al., 2022), AraGPT2 (Antoun et al., 2021b), AceGPT (Huang et al., 2023) and Jais (Sengupta et al., 2023), also across various sizes), and 2 closed-source models (GPT-3.5: gpt-3.5-turbo (Ouyang et al., 2022) and GPT-4: gpt-4-0613 (OpenAI, 2023))." |
| Q47 | 5 | output_form | "We initially conducted experiments with four settings: (1) Arabic prompt and Arabic alphabetic output, (2) Arabic prompt and English (i.e. Latin script) alphabetic output, (3) English prompt and Arabic alphabetic output, and (4) English prompt and English alphabetic output." |
| Q48 | 5 | input_form | "Figure 4 illustrates the Arabic and English prompts." |
| Q49 | 5 | input_form | "The placeholders [SUBJECT], [LEVEL], and [COUNTRY] are replaced with the corresponding Arabic and English words, while the placeholders [INPUT] and [OPTION] are in Arabic." |
| Q50 | 6 | output_form | "Following previous studies (Koto et al., 2023; Li et al., 2023), for open-source models, we determine the answer based on the highest probability among all possible options." |
| Q51 | 6 | output_form | "In the case of English alphabetic output, we measure the probability of the first generated token being A, B, C, D, or E." |
| Q52 | 6 | output_form | "For Arabic, we measure the probability of the first generated token being @, H., h., X, or è." |
| Q53 | 6 | output_form | "For closed-source models, we determine the answer based on the first token generated in the text using a regular expression." |
| Q54 | 6 | output_form | "If there is no match, we assign a random answer." |
| Q55 | 6 | output_form | "To evaluate the influence of prompt language, we initially benchmarked the open-source models using all four prompt settings (Section 4.1), as depicted in Figure 5." |
| Q56 | 6 | output_form | "We observe that the optimal configuration across all models is to use an English prompt and English alphabetic output." |
| Q57 | 6 | output_form | "Predictably, the Arabic-specific LLMs — Jais-chat (30B) and AceGPT-chat (13B) — demonstrate the greatest robustness when employing Arabic alphabetic output." |
| Q58 | 6 | output_form | "For the remaining experiments, we will report based on the setting of English prompt and English alphabetic output." |
| Q59 | 7 | output_form | "As expected, the Arabic-centric model Jais-chat (30B) emerges as the top-performing open-source model, boasting an average score of 62.3%, surpassing GPT-3.5 by 4.6 points." |
| Q60 | 7 | output_form | "Compared to AceGPT-chat (13B), both Jais-chat models (13B and 30B) exhibit substantially higher accuracy in areas including STEM, Social Science, Humanities, and Others." |
| Q61 | 7 | output_form | "For multilingual models such as BLOOMZ (7B) and mT0 (13B), their performance lags behind Jais, with a disparity of more than 14 points." |
| Q62 | 7 | output_form | "XGLM, LLaMA2, and Falcon perform at a level close to random, suggesting their limited proficiency in Arabic." |
| Q63 | 7 | output_form | "GPT-4 achieves the highest accuracy, with a score of 72.5%, surpassing Jais-chat (30B) by 10 points." |
| Q64 | 7 | input_content | "It is noteworthy that in the GPT-4 technical report (OpenAI, 2023), the accuracy of the English-Arabic translated MMLU dataset is reported as 80%, which is 8 points higher than our ArabicMMU results." |
| Q65 | 7 | input_content | "One possible explanation for this difference is that our ArabicMMU presents a greater challenge due to its inclusion of a higher proportion of Arabic-specific content." |
| Q66 | 7 | output_form | "Furthermore, we notice a trend of increasing accuracy with larger models, with the exception of XGLM." |
| Q67 | 7 | output_form | "For example, BLOOMZ (7B) achieves an accuracy 15.9 points higher than BLOOMZ (560M), while mT0 (13B) shows a 13.8-point increase compared to mT0 (300M)." |
| Q68 | 7 | input_ontology | "We observe that ArabicMMU questions are more challenging at the high school level compared to the primary and middle school levels." |
| Q69 | 7 | output_form | "Specifically, for high school questions, GPT-4 achieves a score of only 61.7%, while Jais-chat scores 51.2%." |
| Q70 | 7 | output_form | "Interestingly, we notice that the model accuracy at the university level is higher than for high school." |
| Q71 | 7 | input_ontology | "This could be attributed to the relatively small portion (i.e., 6%) of university-level questions in ArabicMMU, which potentially skews the results." |
| Q72 | 7 | input_ontology | "We present the performance of open-source models on selected subjects that potentially contain Arabic-specific contexts." |
| Q73 | 7 | input_ontology | "These subjects include history, geography, civics, political" |
| Q74 | 8 | output_form | "We focus our more detailed analysis in this section solely on the best open-source models, namely BLOOMZ, AceGPT, and Jais, providing researchers and the community with insights to better understand these models and opportunities for future improvements." |
| Q75 | 8 | output_form | "While all the results in Section 4.2 were based on zero-shot learning, we observe in Figure 7 that when we move to few-shot learning, results for base models improve but those for instruction-tuned models deteriorate." |
| Q76 | 8 | output_form | "Specifically, AceGPT and Jais show an improvement of 2–10 points when using few-shot learning, but the results for BLOOMZ and Jais-chat drop." |
| Q77 | 8 | output_form | "These findings are consistent with prior research over IndoMMIU (Koto et al., 2023) and CMMLU (Li et al., 2023)." |
| Q78 | 8 | output_form | "We analyze whether BLOOMZ, AceGPT, and Jais are well-calibrated in answering ArabicMMLU questions by comparing the probability of the correct answers with the actual accuracy for each task (i.e., subject and level combination)." |
| Q79 | 8 | output_form | "The answer probability is obtained through softmax normalization across the available candidate answers." |
| Q80 | 8 | output_form | "In Figure 8, we observe that the three open-source models are well calibrated with correlation scores r > 0.9." |
| Q81 | 8 | output_form | "Additionally, we investigate the correlation between model confidence and question length in Figure 9." |
| Q82 | 8 | output_form | "We find no correlation between the length of the questions and the model confidence for either Jais or AceGPT." |
| Q83 | 8 | output_ontology | "Despite negation being an absolutely foundational linguistic phenomenon, LLMs have been shown to be worryingly insensitive to its effects in English (Kassner and Schütze, 2020; Hosseini et al., 2021; Truong et al., 2023)." |
| Q84 | 8 | input_ontology | "We thus perform an analysis of LLM performance over questions in ArabicMMLU with and without negation to determine whether this observation ports across to Arabic." |
| Q85 | 8 | input_form | "We utilize specific negation phrases to identify questions containing negations in Arabic." |
| Q86 | 9 | input_ontology | "We introduce ArabicMMLU, the first large-scale multi-task language understanding dataset designed to evaluate real-world knowledge in Arabic." |
| Q87 | 9 | input_content | "Through experiments with over 14K multiple-choice questions spanning various subjects and education levels, we observed that Arabic-centric LLMs outperform multilingual LLMs, albeit with lower accuracy than GPT-4." |
| Q88 | 9 | input_ontology | "For future work, ArabicMMLU can be extended to include short-answer or essay questions, different modalities (i.e., images, audio, video), larger region coverage, and more questions in professional settings." |
| Q89 | 9 | input_content | "ArabicMMLU does not represent all Arabic countries equally. For example, we have collected over 6K multiple-choice questions from Jordan, while other countries are represented with only 100 questions or, in some cases, not at all." |
| Q90 | 9 | input_content | "This is largely due to the availability of publicly-accessible exams in each country; some countries have digitized their exams, but not others." |
| Q91 | 9 | input_content | "Additionally, our search for relevant Arabic content across the internet was not exhaustive." |
| Q92 | 9 | input_form | "The dataset primarily focuses on Modern Standard Arabic (MSA). However, multilingual and Arabic LLMs are often exposed to both MSA and dialectical Arabic." |
| Q93 | 9 | input_form | "ArabicMMLU is focused solely on text-based assessment, and the exploration of multimodal questions is left for future work." |
| Q94 | 9 | output_form | "It is important to emphasize that our experimental results do not provide conclusive answers regarding the performance of LLMs in Arabic." |
| Q95 | 10 | output_content | "to a lack of sufficient information about its training regimen. As such, we cannot assert that the model's pretraining data is free from contamination." |
| Q96 | 10 | input_content | "We extend our gratitude to all collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia who participated in the data collection process." |
| Q97 | 10 | input_content | "We also acknowledge the contributions of Samta Kamboj, Sarah Al Barri, and Onkar Pandit from Core42, who assisted in collecting the Arabic Language question dataset." |
| Q98 | 14 | input_content | "Table 7 presents the distribution of ArabicMMLU data categorized by subject across different education levels." |
| Q99 | 14 | input_form | "Figure 10 illustrates a complete example of prompts used in this study. This example features a Natural Science question with prompts provided in both Arabic and English." |
| Q100 | 14 | output_ontology | "This is a Natural Science question for primary school in Jordan. Select the correct answer!" |
| Q101 | 14 | input_content | "Table 7: The distribution of ArabicMMLU for each subject in different education levels." |
| Q102 | 15 | output_form | "Table 8 presents the detailed zero-shot results across subjects and education levels, while Table 9, Table 10, Table 11 display the results with different prompts and alphabetic outputs (complementing the main result at Table 8)." |
| Q103 | 15 | output_form | "Zero-shot LLM performance (% accuracy) with English prompt and English alphabetic output, for each subject and education level." |
| Q104 | 15 | output_form | "The models are BLOOMZ (7B), AceGPT-chat (13B), Jais-chat (30B), GPT-3.5 (175B), and GPT-4." |
| Q105 | 16 | output_form | "Zero-shot LLM performance (% accuracy) with Arabic prompt and Arabic alphabetic output, combined across subject groups." |
| Q106 | 16 | output_form | ""Average" means the average across all questions in ArabicMMLU." |
| Q107 | 16 | input_ontology | "Table 9 presents results organized by subject groups: STEM, Social Science, Humanities, Arabic Language, and Other." |
| Q108 | 17 | output_form | "Zero-shot LLM performance (% accuracy) with Arabic prompt and English alphabetic output, combined across subject groups." |
| Q109 | 17 | input_ontology | "Table 10: Zero-shot LLM performance (% accuracy) with Arabic prompt and English alphabetic output, combined across subject groups." |
| Q110 | 18 | output_form | "Zero-shot LLM performance (% accuracy) with English prompt and Arabic alphabetic output, combined across subject groups." |
| Q111 | 19 | output_content | "Table 12 lists the sources of pre-trained models used in this study. All models are sourced from Huggingface (Wolf et al., 2020)." |
| Q112 | 19 | output_content | "With the exception of GPT-3.5 and GPT-4, all the models used in this study were sourced from Huggingface (Wolf et al., 2020)." |

---

## Regional Context

```yaml
name: Non-Arab Tourists and Expats in Eight Arabic-Speaking Countries (ArabicMMLU
  Deployment)
abbreviation: arabicmmlu-tourist-expat
benchmark: arabicmmlu
deployment_countries:
- Morocco
- Egypt
- Jordan
- Palestine
- Lebanon
- UAE
- Kuwait
- Saudi Arabia
deployment_regions:
  north_africa:
  - Morocco
  - Egypt
  levant:
  - Jordan
  - Palestine
  - Lebanon
  gulf:
  - UAE
  - Kuwait
  - Saudi Arabia
  note: 'Sub-regional distinctions matter for content validity: Maghrebi, Levantine,
    and Gulf curricula differ in historical framing, language instruction tradition,
    and civic content. Users are international visitors in these countries, not residents
    or nationals.'
target_population_description: Non-Arab tourists and expatriates physically present
  in one or more of the eight listed countries who use an AI assistant to answer school-curriculum-level
  questions about Arabic language, Arab history, and Arab geography. Users are non-native
  Arabic speakers with basic-to-intermediate MSA competence. They are likely varied
  in nationality (European, North American, South/Southeast Asian, etc.) and are using
  the system for educational self-enrichment rather than practical travel assistance.
  Practical logistics, local dialect phrases, tourist etiquette, and real-time customs
  are explicitly out of scope.
user_role: tourists and expats seeking educational-level knowledge about the Arab
  world
user_nativeness: non-native Arabic speakers
expected_arabic_proficiency: basic to intermediate MSA; learner-register Arabic likely;
  possible grammatical imperfection and code-switching
interaction_modality: text-only
languages:
  benchmark_language: Modern Standard Arabic (MSA)
  user_input_register: Learner-level MSA; structurally distinct from the fluent native-speaker
    MSA assumed by the benchmark. Users may produce code-switched or imperfect Arabic.
  other_supported_languages: English and other languages anticipated by the use case
    but outside the current benchmark scope; would require separate cross-lingual
    evaluation
  note: The benchmark is exclusively in MSA. A structural signal-distribution gap
    exists between benchmark-assumed fluent MSA and the actual learner-register Arabic
    produced by the target population.
writing_systems:
  scripts:
  - Arabic script (right-to-left, used in the benchmark)
  - Latin script (likely in learner code-switching and English-language interactions)
  note: RTL rendering and mixed-direction text are relevant for UI/display but not
    assessed by the benchmark. Arabic morphological complexity compounds input-parsing
    challenges for learner-register queries.
sub_regional_curriculum_variation:
  north_africa:
    morocco:
      curriculum_tradition: Maghrebi curriculum with French-influenced educational
        tradition; Darija-adjacent cultural framing
      benchmark_representation: Present in benchmark — Morocco-sourced questions appear
        in Arabic-specific-context subjects (history, geography, civics). However,
        both BLOOMZ and Jais perform notably worse on Morocco-sourced questions compared
        to other countries, suggesting content distinctiveness or data sparsity. No
        Moroccan annotators in the worker pool.
      question_count_estimate: '[NOT FOUND — the paper''s per-country distribution
        figure is not machine-readable from the HTML; the paper states some countries
        contribute as few as ~100 questions. Morocco is confirmed present with country-specific
        questions but exact count not extractable from available sources. GitHub/HuggingFace
        dataset card (ArabicMMLU paper — [WEB-1]) lists
        Jordan, Egypt, Palestine as top-3 sources, implying Morocco is below that
        tier.]'
      notes: 'Model performance analysis in the paper confirms Morocco-sourced questions
        exist and are harder for open-source models: ''BLOOMZ performs less well on
        questions sourced from the UAE and Morocco compared to other countries, while
        Jais performs best overall except in questions sourced from Morocco'' (ArabicMMLU
        paper — [WEB-2]). This suggests Morocco content
        is both present and distinctive, reinforcing the curriculum-mismatch risk.'
    egypt:
      curriculum_tradition: Egyptian national curriculum; well-represented in benchmark
        via Egyptian annotator pool
      benchmark_representation: Moderate to good — Egyptian workers contributed to
        both collection and verification; Egypt is confirmed as one of the top-3 source
        countries.
      question_count_estimate: 'Top-3 source country (Jordan #1, Egypt #2 or #3 alongside
        Palestine — confirmed in GitHub/HuggingFace dataset card and paper HTML —
        [WEB-3]). Exact count not published separately.'
      notes: '[NEEDS VERIFICATION — deferred: subject distribution breakdown for Egyptian-sourced
        questions not separately published; below search budget]'
  levant:
    jordan:
      curriculum_tradition: Jordanian national curriculum; by far the dominant source
        in the benchmark
      benchmark_representation: Over 6,000 questions sourced from Jordan — benchmark
        is substantially Jordan-skewed
      question_count_estimate: ~6,000+ (documented in benchmark paper)
      notes: Jordan-skew means benchmark performance may disproportionately reflect
        Jordanian curriculum framing, including Jordanian perspectives on shared Levantine
        and pan-Arab historical events.
    palestine:
      curriculum_tradition: Palestinian Authority curriculum with politically distinct
        historical narratives (1948 war, occupation, statehood); sensitive civic and
        history content
      benchmark_representation: CONFIRMED as top-3 source country — Jordan, Egypt,
        and Palestine are explicitly named as the top three contributors in the dataset
        documentation (GitHub and HuggingFace dataset card — [WEB-3];
        [WEB-4]). Exact question count
        not published separately. No Palestinian annotators in the worker pool despite
        Palestine being a major source.
      question_count_estimate: Top-3 source country (confirmed in dataset card — [WEB-4]);
        exact count not separately published.
      notes: Palestine being a top-3 contributor is a significant positive finding
        not anticipated by the scaffold. However, the structural MCQ format cannot
        represent Palestinian-specific historical framings, and no Palestinian annotator
        verified Palestinian-sourced questions — the 96% agreement reflects Jordanian/Egyptian
        consensus applied to Palestinian content.
    lebanon:
      curriculum_tradition: Lebanese national curriculum; multilingual educational
        environment (Arabic, French, English)
      benchmark_representation: One Lebanese internal worker acknowledged; contribution
        size unclear
      question_count_estimate: '[NOT FOUND — exact Lebanon question count not published
        in accessible sources; likely below the Jordan/Egypt/Palestine top-3 tier
        given the paper''s statement that some countries contribute ~100 questions
        (ArabicMMLU paper — [WEB-1])]'
      notes: '[NEEDS VERIFICATION — deferred: whether Lebanon''s multi-confessional
        civic framing appears in benchmark content; low impact relative to top-3 gap
        findings already resolved]'
  gulf:
    uae:
      curriculum_tradition: UAE national curriculum; Islamic studies prominent; modern
        multicultural state context
      benchmark_representation: One UAE internal worker acknowledged; BLOOMZ performs
        less well on UAE-sourced questions compared to most other countries (noted
        alongside Morocco in model performance analysis — [WEB-2]),
        suggesting UAE content is present and distinctive.
      question_count_estimate: '[NOT FOUND — exact UAE question count not published
        in accessible sources; below Jordan/Egypt/Palestine top-3 tier]'
      notes: '[NEEDS VERIFICATION — deferred: subject distribution for UAE-sourced
        questions; below search budget]'
    kuwait:
      curriculum_tradition: Kuwaiti national curriculum; Gulf Arabic educational tradition
      benchmark_representation: Listed as source country but no Kuwaiti collaborators
        acknowledged. The paper's figure showing country distribution is not machine-readable;
        Kuwait is not mentioned among top-3 sources (Jordan, Egypt, Palestine) or
        in model performance country-grouped analysis, suggesting it is in the lower-contribution
        tier (~100 questions or fewer).
      question_count_estimate: '[NOT FOUND — Kuwait not cited in any country-specific
        performance analysis or top-contributor list; likely in the ~100-question
        or lower tier per the paper''s general caveat about unequal representation
        (ArabicMMLU paper — [WEB-1]). Absence from country-grouped
        performance table (Table 5) in the paper suggests very low contribution.]'
      notes: Kuwait's absence from the country-grouped Arabic-specific-context performance
        table (which covers Jordan, Egypt, Palestine, Lebanon, UAE, KSA, Morocco)
        in the published paper strongly implies Kuwait's contribution is minimal or
        its questions are categorized under non-country-specific subjects.
    saudi_arabia:
      curriculum_tradition: Saudi national curriculum; Islamic studies heavily integrated;
        geography and history framed through Saudi/Gulf lens
      benchmark_representation: Two Saudi internal workers acknowledged; likely meaningful
        contribution
      question_count_estimate: '[NEEDS VERIFICATION — deferred: exact KSA question
        count not separately published; below search budget]'
      notes: '[NEEDS VERIFICATION — deferred: subject distribution for Saudi-sourced
        questions; below search budget]'
knowledge_domain_scope:
  in_scope:
  - Arabic language (grammar, vocabulary, literary tradition — school-curriculum level)
  - Arab history (ancient, medieval, modern — school-curriculum level)
  - Arab and MENA geography (physical and political — school-curriculum level)
  - Civics and social science where covered by school curricula
  explicitly_out_of_scope:
  - Local dialect phrases and colloquial Arabic
  - Tourist etiquette and religious customs for visitors
  - Practical travel logistics (transport, markets, accommodation)
  - Real-time or current-events knowledge
  - Professional or technical domain knowledge beyond school curriculum
  contested_content_note: History, civics, and political geography questions frequently
    carry contested national or political framings (e.g., 1948 Arab-Israeli war, Palestinian
    statehood, pan-Arab identity, Gulf political structures). The deployment explicitly
    requires multi-perspective acknowledgment of such content; the benchmark's single-correct-answer
    MCQ format structurally cannot evaluate this requirement.
cultural_norms_notes: 'Pan-Arab framing is broadly acceptable for this deployment
  per elicitation guidance, given shared religious and linguistic culture across the
  region. However, the system should flag country-specific content rather than silently
  generalizing it. Key sensitivities include:

  - Palestinian historical narratives and political status — among the most contested
  content in the region

  - Varying national framings of pan-Arab historical events (Nakba, Arab Spring, Gulf
  War)

  - Morocco''s culturally distinct Maghrebi identity and French-educational-tradition
  framing

  - Gulf-state civic content (monarchies, Islamic governance) vs. Levantine republican
  traditions

  - Religious content (Islamic history and practice) is academically relevant at school-curriculum
  level but should not be presented prescriptively to non-Muslim tourists

  - Users are international visitors, so cultural sensitivity framing should be explanatory
  and non-normative'
annotator_pool_notes:
  benchmark_annotators: '10 native Arabic speakers: 1 Jordanian, 1 Egyptian, 1 Lebanese,
    1 UAE, 2 KSA (internal); 3 Jordanian, 1 Egyptian (external)'
  absent_national_perspectives:
  - Morocco
  - Kuwait
  - Palestine (annotator absent despite Palestine being a top-3 source country)
  skew_risk: Jordanian and Egyptian perspectives dominate both collection and verification.
    For historically sensitive content where correct answers differ by national curriculum,
    the 96% agreement rate likely reflects Jordanian/Egyptian consensus rather than
    pan-regional validity. Critically, Palestine is the 3rd largest source country
    but has no Palestinian annotators — Palestinian-sourced questions were verified
    by non-Palestinian workers.
  verification_ceiling: 96% answer-key accuracy per post-hoc verification by 2 independent
    native speakers — practical upper bound for benchmark label quality
output_form_mismatch:
  benchmark_output: Discrete single-correct-answer MCQ labels; scored as % accuracy
    via token probability (open-source) or regex matching (closed-source)
  deployment_required_output: Open-ended, explanatory, multi-perspective natural-language
    responses that explicitly acknowledge contested national positions and flag country-specific
    content
  mismatch_severity: HIGH — this is the most critical structural mismatch. The benchmark
    cannot evaluate whether the system correctly handles the pluralistic framing the
    deployment requires.
  supplementary_evaluation_needed: 'Two relevant emerging frameworks identified:

    1. ''Beyond MCQ: An Open-Ended Arabic Cultural QA Benchmark with Dialect Variants''
    (arXiv 2510.24328, 2024/2025) — first benchmark to unify dialectal Arabic QA,
    open-ended reasoning, and CoT fine-tuning, directly addressing the MCQ-to-OEQ
    gap. Source: [WEB-5]

    2. AraGen benchmark (El Filali et al. 2024) uses LLM-as-judge with 3C3H metric
    (Correctness, Completeness, Conciseness, Helpfulness, Honesty, Harmlessness) for
    open-ended Arabic generation evaluation, included in OALL v2. Source: [WEB-6]

    Neither covers multi-perspective historical/civic content specifically, but both
    represent the closest available supplementary evaluation frameworks.'
input_register_mismatch:
  benchmark_assumption: Fluent native-speaker MSA
  actual_user_register: Learner-level MSA; potentially grammatically imperfect, code-switched,
    or at intermediate proficiency
  mismatch_severity: MODERATE — creates a signal-distribution gap; benchmark scores
    may not predict system robustness for learner-register input
  supplementary_evaluation_needed: '[NOT FOUND — searched for Arabic learner-register
    NLP robustness and non-native MSA evaluation benchmarks; no dedicated benchmark
    for non-native Arabic speaker input robustness found in the literature as of 2025.
    The survey of 40+ Arabic benchmarks (arXiv 2510.13430 — [WEB-6])
    does not list any learner-register robustness benchmark. This is a confirmed documentation
    gap requiring bespoke evaluation design or stakeholder elicitation.]'
cross_lingual_capability:
  benchmark_coverage: Prompt language variants tested (Arabic/English combinations)
    but cross-lingual knowledge transfer to non-Arabic output for non-Arabic-speaking
    users is not evaluated
  deployment_relevance: English and other language interactions anticipated; outside
    current benchmark scope
  supplementary_evaluation_needed: '[NEEDS VERIFICATION — deferred: cross-lingual
    Arabic-English knowledge transfer evaluation for history/geography domains; below
    remaining search budget. Note: ALRAGE (included in OALL v2) targets retrieval-augmented
    Arabic QA and may offer partial cross-lingual signal — [WEB-6]]'
infrastructure_notes:
  deployment_context: International tourists and expats; likely using personal smartphones
    or laptops with reliable connectivity (hotel, coworking, mobile data)
  device_assumption: Mobile-first or laptop; not constrained by low-end hardware or
    poor connectivity as a target-population characteristic
  connectivity: 'No specific AI service access blocks or VPN requirements identified
    for the eight deployment countries based on current regulatory survey. UAE, KSA,
    and Kuwait all have ''business-friendly'' soft-law AI frameworks (no binding content
    restrictions on question-answering assistants identified). UAE''s Federal Decree-Law
    on Fight Against Rumours and Cybercrime applies broadly to AI deployments and
    should be reviewed for edge cases. Source: Pinsent Masons GCC AI Regulation survey
    — [WEB-7];
    Library of Congress FALQs GCC AI — [WEB-8]'
  language_rendering: RTL Arabic text rendering required; mixed-direction display
    (Arabic + Latin) relevant for learner-register users
regulatory_and_political_context:
  content_sensitivity: Historically and politically contested content is inherent
    to the history and civics domains in this region. Systems operating across all
    eight countries must navigate potentially divergent legal and political sensitivities
    about what constitutes acceptable framing of shared historical events.
  country_specific_restrictions: 'GCC countries (UAE, KSA, Kuwait) have adopted soft-law,
    ''business-friendly'' AI frameworks with no binding content-specific restrictions
    on historical or political question-answering identified as of 2024-2025. UAE:
    National AI Strategy 2031, AI Charter (June 2024, non-binding, 12 ethical principles),
    Abu Dhabi AI and Advanced Technology Council (Law No. 3/2024). KSA: SDAIA Generative
    AI Guidelines (Jan 2024) and AI Adoption Framework (Sep 2024) — guidance only,
    not binding regulation. Kuwait: CITRA contributing to AI landscape; no dedicated
    AI regulations yet issued. Source: Library of Congress GCC AI FALQs Parts 1 &
    2 — [WEB-8];
    [WEB-9];
    White & Case UAE tracker — [WEB-10]'
  palestine_legal_status: '[NEEDS VERIFICATION — deferred: how Palestine''s non-UN-member-state
    status affects content moderation obligations or framing norms for AI systems
    deployed there; likely unsearchable (lived regulatory practice in occupied territories)
    and requires legal expert elicitation]'
  data_protection: 'UAE: Federal Decree-Law No. 45 of 2021 on Personal Data Protection.
    KSA: Personal Data Protection Law (PDPL) Royal Decree M/19 of 2024 (in full force).
    Kuwait: Data Privacy Protection Regulation (administrative decision, applicable
    to licensed service providers). Egypt, Morocco, Lebanon, Jordan, Palestine: [NEEDS
    VERIFICATION — deferred: data protection law status for non-Gulf deployment countries;
    below remaining search budget]. Source: University of York AI Regulation Middle
    East analysis — [WEB-11];
    CMS KSA AI laws — [WEB-12]'
benchmark_country_coverage_summary:
  jordan: Over-represented (~6,000+ questions); annotator pool skews Jordanian
  egypt: Represented as top-3 source country; Egyptian annotators in pool (ArabicMMLU
    GitHub — [WEB-3])
  palestine: CONFIRMED top-3 source country alongside Jordan and Egypt (ArabicMMLU
    GitHub and HuggingFace — [WEB-4]);
    no Palestinian annotators despite major contribution — critical gap for contested
    historical content verification
  ksa: Represented; Saudi annotators in pool
  uae: Represented; UAE annotator in pool; model performance notably lower on UAE-sourced
    questions (ArabicMMLU paper — [WEB-2])
  lebanon: Represented; Lebanese annotator in pool; contribution size below top-3
    tier
  morocco: Present with country-specific questions; model performance notably lower
    on Morocco-sourced questions for both BLOOMZ and Jais than most other countries
    (ArabicMMLU paper — [WEB-2]); no Moroccan annotators;
    likely low question count below top-3 tier
  kuwait: Presence ambiguous — not named in top-3 sources, not listed in country-grouped
    model performance analysis (Table 5 covers Jordan, Egypt, Palestine, Lebanon,
    UAE, KSA, Morocco); likely minimal contribution in ~100-question or lower tier
    (ArabicMMLU paper — [WEB-1])
net_new_findings:
  palestine_top3_source_correction: 'The scaffold marked Palestine''s contribution
    as ''undocumented'' and assumed it was small. Multiple independent sources (GitHub
    dataset card, HuggingFace dataset card, arXiv HTML) explicitly state ''Jordan,
    Egypt, and Palestine being the top three sources.'' This materially changes the
    assessment: Palestinian curriculum content is substantially present in the benchmark,
    but the structural MCQ format and absence of Palestinian annotators still prevent
    multi-perspective verification of contested historical content. Source: [WEB-3];
    [WEB-4]'
  beyond_mcq_arabic_benchmark: 'A 2024/2025 benchmark (''Beyond MCQ: An Open-Ended
    Arabic Cultural QA Benchmark with Dialect Variants'', arXiv 2510.24328) directly
    addresses the OO/OF gap by converting MCQs to open-ended questions across five
    dialects (Syrian, Egyptian, Emirati, Saudi, Moroccan) with CoT annotations and
    human review. This is the closest available supplementary evaluation for the deployment''s
    open-ended multi-perspective requirement, though it covers dialect variants rather
    than contested historical content specifically. Source: [WEB-5]'
  aragen_llm_as_judge_arabic: 'AraGen (El Filali et al. 2024b), now part of OALL v2,
    uses LLM-as-judge with a 3C3H metric (Correctness, Completeness, Conciseness,
    Helpfulness, Honesty, Harmlessness) for open-ended Arabic generation quality assessment.
    It is the most established open-ended Arabic evaluation framework and could supplement
    ArabicMMLU for the deployment''s explanatory output requirement, though its cultural
    coverage (40 Arabic books) does not specifically target school-curriculum history/civic
    content. Source: [WEB-6]'
  ilmaam_culturally_aligned_refinement: 'ILMAAM (Nacar et al. 2025) is a culturally
    aligned benchmark that refines ArabicMMLU by ensuring religious sensitivity and
    social norms. Relevant for the deployment''s requirement to handle Islamic-history
    content at school-curriculum level without prescriptive framing. Source: [WEB-6]'
  arabic_llm_benchmark_survey_2025: 'A comprehensive survey of 40+ Arabic LLM benchmarks
    (Alzubaidi et al. 2025, arXiv 2510.13430) identifies ''limited temporal evaluation,
    insufficient multi-turn dialogue assessment, and cultural misalignment in translated
    datasets'' as critical gaps — directly confirming the downstream assessment''s
    validity concerns. No learner-register or non-native Arabic speaker benchmark
    was identified in the survey. Source: [WEB-6]'
  morocco_uae_model_performance_signal: 'The ArabicMMLU paper''s Table 5 (performance
    on Arabic-specific-context subjects by country) shows that both BLOOMZ and Jais
    perform notably worse on Morocco-sourced questions than on questions from other
    countries, with Jais — the best Arabic-centric model — performing worst specifically
    on Morocco. This is a concrete validity signal: Morocco-specific content is present
    but more difficult for current Arabic LLMs, likely reflecting curriculum-content
    distinctiveness and/or lower training data coverage for Maghrebi educational materials.
    Source: ArabicMMLU paper — [WEB-2]'
  gcc_ai_soft_law_framework: 'As of 2024-2025, none of the three Gulf deployment countries
    (UAE, KSA, Kuwait) have enacted binding AI content regulations that would specifically
    restrict historical or political question-answering. All three operate under soft-law
    frameworks (guidelines, principles, strategies). UAE''s cybercrime law is the
    most relevant existing constraint for content deployed in-country. Saudi Arabia''s
    PDPL (Royal Decree M/19/2024) governs data handling. Kuwait has no dedicated AI
    regulations. This reduces (but does not eliminate) the regulatory risk for the
    deployment''s contested-content handling requirement in Gulf countries. Source:
    [WEB-8];
    [WEB-7]'
flagged_gaps_for_downstream_search:
- gap_id: 1
  topic: Morocco curriculum coverage in ArabicMMLU
  search_target: ArabicMMLU Morocco Maghrebi curriculum Arabic benchmark question
    distribution
  resolution_status: PARTIALLY RESOLVED — Morocco confirmed present with country-specific
    questions; model performance distinctively lower on Morocco content; exact question
    count not extractable. No Moroccan annotators confirmed. See net_new_findings.morocco_uae_model_performance_signal.
- gap_id: 2
  topic: Palestine coverage and contested historical content representation in ArabicMMLU
  search_target: Arabic benchmark Palestinian educational content contested history
    1948 NLP evaluation
  resolution_status: 'SUBSTANTIALLY RESOLVED — Palestine confirmed as top-3 source
    country (major positive finding). Structural gap remains: no Palestinian annotators,
    MCQ format cannot represent contested narratives. See net_new_findings.palestine_top3_source_correction.'
- gap_id: 3
  topic: Kuwait question count and subject distribution in ArabicMMLU
  search_target: ArabicMMLU Kuwait question distribution Arabic benchmark Gulf country
    coverage
  resolution_status: INFERRED — Kuwait absent from country-grouped performance table
    and top-source lists; likely minimal contribution (~100 or fewer questions). See
    benchmark_country_coverage_summary.kuwait.
- gap_id: 4
  topic: Multi-perspective and open-ended Arabic evaluation benchmarks
  search_target: Arabic LLM evaluation open-ended multi-perspective civic history
    question answering benchmark
  resolution_status: PARTIALLY RESOLVED — 'Beyond MCQ' benchmark (arXiv 2510.24328)
    and AraGen (3C3H LLM-as-judge) identified as supplementary options. Neither specifically
    targets contested historical content. See net_new_findings.beyond_mcq_arabic_benchmark
    and net_new_findings.aragen_llm_as_judge_arabic.
- gap_id: 5
  topic: Arabic learner-register robustness evaluation
  search_target: Arabic learner register NLP robustness benchmark non-native speaker
    MSA evaluation
  resolution_status: NOT FOUND — confirmed documentation gap. No dedicated benchmark
    for non-native Arabic speaker input robustness exists in 40+ benchmark survey
    as of 2025. Requires bespoke evaluation design.
- gap_id: 6
  topic: Cross-lingual Arabic-English knowledge transfer evaluation
  search_target: cross-lingual Arabic English knowledge transfer evaluation benchmark
    MENA history geography
  resolution_status: DEFERRED — below remaining search budget. ALRAGE (RAG-based Arabic
    QA, in OALL v2) is a partial candidate.
- gap_id: 7
  topic: AI content deployment restrictions in UAE, KSA, Kuwait
  search_target: AI deployment content restrictions UAE Saudi Arabia Kuwait political
    historical content regulation
  resolution_status: RESOLVED — no binding content-specific AI restrictions found
    in Gulf countries as of 2024-2025; soft-law frameworks only. UAE cybercrime law
    is broadest existing constraint. See regulatory_and_political_context.country_specific_restrictions.
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/abs/2402.12840 |
| WEB-2 | https://arxiv.org/html/2402.12840v1 |
| WEB-3 | https://github.com/mbzuai-nlp/ArabicMMLU |
| WEB-4 | https://huggingface.co/datasets/MBZUAI/ArabicMMLU |
| WEB-5 | https://arxiv.org/abs/2510.24328 |
| WEB-6 | https://arxiv.org/abs/2510.13430 |
| WEB-7 | https://www.pinsentmasons.com/out-law/analysis/gulf-governments-approach-to-ai-regulation |
| WEB-8 | https://blogs.loc.gov/law/2024/12/falqs-ai-regulations-in-the-gulf-cooperation-council-member-states-part-one/ |
| WEB-9 | https://blogs.loc.gov/law/2024/12/falqs-ai-regulations-in-the-gulf-cooperation-council-member-states-part-two/ |
| WEB-10 | https://www.whitecase.com/insight-our-thinking/ai-watch-global-regulatory-tracker-uae |
| WEB-11 | https://www.york.ac.uk/assuring-autonomy/news/blog/ai-regulation-middle-east/ |
| WEB-12 | https://cms.law/en/int/expert-guides/ai-regulation-scanner/kingdom-of-saudi-arabia |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Your users are tourists and expats visiting specific countries — Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, and KSA. Should the system handle practical, on-the-ground knowledge that foreigners typically need, such as local dialect phrases, tourist etiquette, religious customs, or navigating local transport and markets? Are there categories of questions you expect frequently that go beyond formal history and geography?
A1: The system is scoped to school-curriculum-level general knowledge (history, geography, Arabic language). Dialectal phrases, tourist etiquette, religious customs, and practical navigation are acknowledged as frequently expected but fall outside the intended scope; other benchmarks (e.g., MADAR) address dialectal Arabic separately.

Q2 [IC]: Does the system need to reflect country-specific cultural nuances accurately, or is a pan-Arab generalized framing acceptable?
A2: Pan-Arab generalized framing is broadly acceptable given shared religious and linguistic culture across the region, but the system should flag content that is country-specific rather than silently generalizing it.

Q3 [OO]: When answering history or geography questions where different countries hold competing official or cultural positions, should the system give a single answer, acknowledge multiple perspectives, or tailor the answer by country?
A3: The system should explicitly acknowledge multiple perspectives and note that different countries hold different positions, signaling to the user that the topic is contested and potentially sensitive.

Q4 [IF]: Will users interact in Arabic or another language, and what is the expected modality distribution?
A4: The benchmark is in Arabic, targeting Arabic learners who will prompt in MSA. English and other languages may be supported but would require separate training and cross-lingual evaluation; this is outside the current benchmark scope.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark covers MSA school-curriculum content, but the deployment spans eight countries including Morocco and Palestine, which have historically distinct educational curricula and are underrepresented or absent in ArabicMMLU's source countries; practical travel knowledge is explicitly out of scope but the school-knowledge framing still leaves coverage gaps for country-specific topics. |
| IC | MODERATE | Pan-Arab framing is acceptable per the user, reducing the risk of country-specific content mismatch, but contested historical content (e.g., Palestinian narratives, 1948 war) and the benchmark's "transferred from different cultural context" sourcing flag introduce some construct-irrelevant variance. |
| IF | MODERATE | The deployment is text-only and the benchmark is text-only, which aligns well; however, users are non-native Arabic speakers interacting in MSA, and the benchmark's MSA register may not match the learner-level Arabic actually produced by tourists, creating a signal-distribution gap. |
| OO | HIGH | The deployment explicitly requires multi-perspective acknowledgment of contested historical and civic questions, but ArabicMMLU uses a single-correct-answer MCQ format — this structural mismatch means the benchmark's output taxonomy cannot capture the pluralistic framing the deployment requires. |
| OC | MODERATE | ArabicMMLU was constructed with native Arabic speaker collaboration across several target countries, which is a positive signal; however, Morocco and Palestine are either absent or underrepresented as source countries, and annotation pools for contested historical content may not reflect the full range of regional stakeholder perspectives. |
| OF | HIGH | The benchmark produces discrete MCQ labels, but the deployment requires open-ended, explanatory, multi-perspective natural-language responses — this is a direct mismatch in output form that the benchmark cannot evaluate as-is. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** MBZUAI/ArabicMMLU
**Analysis date:** 2025-01-31
**Examples reviewed:** ~210 examples across 41 configs (5–8 per config)
**Columns shown:** ID, Source, Country, Group, Subject, Level, Question, Context, Answer Key, Option 1–5, is_few_shot
**Columns skipped (media):** None (text-only dataset; Context field is mostly null in sampled examples)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | History (High School) | ID 3049, Jordan | D | "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين: إتمام وحدة الضفتين عام 1950م / رفضه إعطاء اليهود ممراً إلى حائط البراق / دعوة العرب إلى دعم صندوق الأمة الفلسطيني / رفضه معاهدة سايكس بيكو ووعد بلفور رفضاً قاطعاَ" | Jordan HS history question about King Abdullah I's positions on Zionism and Palestine — framed from Jordanian curriculum perspective | IO, IC, OC |
| D2 | Civics (High School) | ID 14526, Jordan | B | "مثّل ______ العرب في مؤتمر الصلح الذي عقده الحلفاء في باريس: ١-الأمير عبدالله بن الحسين / ٢-الأمير فيصل بن الحسين / ٣-الشريف الحُسين بن علي / ٤-الحُسين بن طلال" | Jordan civics HS: who represented Arabs at Paris Peace Conference — Jordanian Hashemite framing | IC, OC |
| D3 | Civics (High School) | ID 14529, Jordan | C | "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨: تحرر البلاد من قيود فك الانتداب" | Jordan civics HS: primary goal of the 1948 Jordanian-British treaty — Jordanian national framing | IC, OC |
| D4 | Civics (Middle School) | IDs 14291–14327 (5 items), Jordan | various | "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952... القوة العربية من تشكيلات الجيش العربي الأردني... عُدل قانون الأحزاب الأردني" | All 5 sampled Civics Middle School items are exclusively about Jordanian political history | IO, IC |
| D5 | Law (Professional) | IDs 4824, 4843, 4880, 4881, 4652, Morocco | B/C/D/E/C | "يبتدئ أجل الاستئناف... من وزير العدل والسلطة الحكومية المكلفة بالدفاع الوطني" | All 5 sampled Law (Professional) items are from Morocco (Moroccan procedural law) | IO, IC |
| D6 | Geography (Middle School) | ID 8055, Jordan | A | "توجد كنيسة سيدة الجبل في ……. عنجرة" | Jordan middle school geography: location of Lady of the Mountain church in Ajloun, Jordan | IC |
| D7 | Geography (High School) | ID 8529, Jordan | D | "محمية طبيعية في الأردن تشرف عليها إدارة مشتركة بين سلطة المنطقة الاقتصادية الخاصة في العقبة ووزارة السياحة والجمعية الملكية لحماية الطبيعة: وادي رم" | Jordan HS geography: Jordan-specific nature reserve question | IC |
| D8 | History (High School) | ID 2819, Jordan | D | "صدر دستور عام 1952 في عهد جلالة الملك: طلال بن عبدالله" | Jordan HS history: which Jordanian king issued 1952 constitution | IC |
| D9 | History (High School) | ID 2716, Jordan | D | "ترمز الكرة الارضية في شعار المملكة الاردنية الهاشمية إلى: انتشار الاسلام" | Jordan HS history: symbolism in the Hashemite Kingdom's emblem | IC |
| D10 | Social Science (Primary School) | ID 5489, Jordan | D | "تشمل الخدمات الطبية الملكية الحكومية العديد من المؤسسات المتخصصة... مستشفى المدينة الطبية" | Jordan primary social science: Jordan Royal Medical Services institutions | IC |
| D11 | Social Science (Primary School) | ID 5481, Jordan | D | "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" | Jordan primary social science: fact about King Talal's reign — Jordan-specific | IC |
| D12 | Economics (High School) | ID 11412, Jordan | C | "ارسال الشكوى عن طريق الموقع الالكتروني للبنك المركزي وهو: www.cbj.gov.jo" | Jordan HS economics: URL of the Central Bank of Jordan — Jordan-institution specific | IC |
| D13 | Economics (High School) | ID 11561, Jordan | B | "نسبة الأردنيين الذين لا يستطيعون الوصول إلى الخدمات المالية الرسمية: 0.67" | Jordan HS economics: Jordan-specific financial inclusion statistic | IC |
| D14 | Islamic Studies (General) | IDs 165, 385, 46, 157, 54 — Country=null | A/D | "من هو النبي الذي علم منطق الطير؟ سليمان عليه السلام / كم مرة اعتمر النبي صلى الله عليه وسلم؟ أربع عمرات" | Pan-Islamic knowledge questions: no country field — factual hadith/Quran questions | IC, IO |
| D15 | Arabic Language (General) | ID 11728, Country=null | B | "يعود تاريخ العرب إلى آلاف السنين... سُمِّيَ العدنانيون بعرب [فراغ]. الشمال" | Pan-Arab ethnolinguistic history reading comprehension — culturally grounded, no country marker | IC |
| D16 | Arabic Language (Grammar) | ID 12626, Country=null | A | "In the following Quranic verse, what is the correct parsing of the word ــكَ" | Grammar question with English question stem — unexpected language mixing in nominally Arabic benchmark | IF |
| D17 | Geography (Middle School) | ID 8136, Palestine | D | "من الجزر المحيطة بقارة أقيانوسيا: نيوزيلندا / تسمانيا / سلمن / جميع ما ذكر" | Palestine middle school geography: world geography (Oceania islands) — no regional specificity | IC |
| D18 | Geography (Middle School) | ID 8064, Palestine | C | "جمع ما يلي من عناصر الدولة عدا: الشعب / الاقليم / الاحتلال / السيادة" | Palestine MS geography: elements of a state — "occupation" appears as a distractors option | OC |
| D19 | History (Middle School) | ID 2641, Palestine | A | "العلم الذي يبحث في حركات ومواقع النجوم والكواكب: الفلك" | Palestine MS history: astronomy definition — not politically sensitive | IC |
| D20 | Computer Science (Primary School) | IDs 7354–7599, Palestine | various | "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" | Palestine primary CS: binary number systems — STEM, no contested content | IC |
| D21 | Biology (High School) | IDs 9699, 9707, 9834, Palestine | B/B/B | "مقدار تكبير العدسة الزيتية في المجهر الضوئي هو: X100 / إحدى العضيات التالية مسئولة عن تصنيع الليبيدات في الخلية: الشبكة الاندوبلازمية الملساء" | Palestine HS biology: standard cellular biology — culturally neutral STEM | IC |
| D22 | Accounting (University) | IDs 7185–7245, Egypt | A/B | "يفترض أسلوب المراجعة حول الحاسب أنه إذا كانت المدخلات سليمة... فإن عملية التشغيل تكون سليمة بالتبعية: صح" | Egypt university accounting — auditing/financial statements questions | IO |
| D23 | Management (University) | IDs 6174–6175, Egypt | B/C | "درجتة تهييتع الدتلطة بتين الألتخاص... تذتير إلى: ال مركز ة" | Severely garbled OCR text making question almost illegible | IC, OC |
| D24 | Political Science (University) | IDs 7008, 7024, Egypt | D | "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ: كل ما سبق" | Egypt university political science with severe OCR corruption — content partially unreadable | IC, OC |
| D25 | Civics (High School) | ID 14546, Jordan | B | "الدول التي سعت الى اقامة مجلس التعاون الخليجي هي (الامارات العربيه المتحده، قطر، عُمان، اليمن، العراق): لا" | Jordan civics HS: false claim about GCC founding states — correct answer is "No" since Yemen and Iraq were not founders | IO, OC |
| D26 | Driving Test | IDs 687, 695, UAE; 1025, Lebanon; 806, 798, Egypt | various | "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر" | Driving test questions from UAE, Lebanon, Egypt — practical/regulatory, not school-curriculum history/geography | IO |
| D27 | General Knowledge (Primary School) | ID 4381, Jordan | B | "برغي سن الصاج هو: مسمار لولبي الشكل مسلوب من نهايته" | Jordan primary GK: sheet metal screw definition — vocational/practical knowledge | IO |
| D28 | General Knowledge (Middle School) | ID 4556, Jordan | A | "الشامل الأكاديمي يمثل: الأدبي" | Jordan middle school GK: Jordanian academic track system — Jordan-specific educational structure | IC |
| D29 | Arabic Language (Grammar) | ID 12655, Country=null | D | "في الآية القرآنية ﴿إنَّ الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحاتِ﴾، ما هو الإعراب الصحيح لكلمة إنَّ: حرف توكيد ونصب" | Arabic grammar parsing using Quranic verse — MSA grammar directly relevant to deployment | IF |
| D30 | History (High School) | ID 2827, Jordan | A | "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة... القيام بشعائر الأديان" | Jordan HS history/civics: Jordanian constitution rights — Jordan-specific legal framing | IC, OC |
| D31 | Islamic Studies (High School) | ID 14064, Jordan | E | "للتفكير آثار إيجابية عدة: جميع ما ذكر" | Jordan HS Islamic studies: positive effects of thinking (Islamic values framing) — presented as school subject | IC |
| D32 | Social Science (Middle School) | ID 5261, Country=null | D | "أنعم الله على بلادنا العربية بثروات كبيرة من النفط والغاز الطبيعي... يرجع السبب في ذلك إلى: توافره بكميات قليلة" | Pan-Arab social science MS: Arab world natural resources | IC |
| D33 | Geography (Primary School) | ID 7848, Jordan | A | "يمتد الوطن العربي في قارتي: آسيا وأفريقيا" | Jordan primary geography: Arab world spans Asia and Africa — broad pan-Arab framing | IC |
| D34 | History (Primary School) | ID 2437, Jordan | D | "يثرب هو الاسم القديم ل: المدينة المنورة" | Jordan primary history: ancient name of Medina — Islamic history, factual | IC |
| D35 | Arabic Language (General) | ID 12069, Country=null | B | "لا يمكن أنْ يصلي المسلم [فراغ]: بدون وضوء" | Arabic language reading with Islamic ritual context — assumes Muslim reader perspective | IC |
| D36 | Computer Science (University) | IDs 7262–7303, KSA | C/A/B/A | "جميع البرامج التالية تعتبر من التطبيقات باستثناء: نظام التشغيل" | KSA university CS: basic computer science concepts — confirmed KSA source | IO |
| D37 | Geography (Middle School) | ID 8058, Jordan | C | "يوجد متحف التاريخ الطبيعي في: نيويورك" | Jordan MS geography: Natural History Museum location — answer is New York, not the primary one | OC |
| D38 | Natural Science (Middle School) | IDs 1902, 1865 — Country=null | C/B | "قام أحمد بحرق كمية من الماغنيسيوم بالمختبر؛ أي المعادلات التالية تصف التفاعل الذي حصل؟ الماغنيسيوم + أكسجين -> أكسيد الماغنيسيوم" | Natural science MS: chemistry reactions — country-neutral STEM | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Authentic school-curriculum framing directly matches deployment knowledge scope
- **Dimension(s):** IO, IC
- **Observation:** The benchmark is genuinely sourced from national school exam materials, not translated from English. Subjects directly relevant to the deployment — history, geography, civics, Arabic language, Islamic studies, and social science — appear across multiple levels and multiple countries. The sampled data confirms subject labels match the deployment's "school-curriculum level" scope.
- **Deployment relevance:** Tourists seeking educational-level knowledge about Arab history, geography, and language will encounter exactly the types of questions the benchmark tests. This supports construct validity for the core knowledge-testing use case.
- **Datapoint citations:**
  - [D1] History (High School), ID 3049, Jordan, label=D: "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" — Modern Arab history question at HS level, directly in-scope for deployment
  - [D15] Arabic Language (General), ID 11728, null, label=B: "يعود تاريخ العرب إلى آلاف السنين... سُمِّيَ العدنانيون بعرب [فراغ]. الشمال" — Reading comprehension about Arab ethnolinguistic history at appropriate level
  - [D33] Geography (Primary School), ID 7848, Jordan, label=A: "يمتد الوطن العربي في قارتي: آسيا وأفريقيا" — Basic Arab world geography, school-level

#### Strength 2: Palestine confirmed as top-3 source country with substantial curriculum content
- **Dimension(s):** IO, IC
- **Observation:** Multiple samples confirm Palestinian-sourced questions exist across subjects: Biology (high school, multiple items), Computer Science (primary, 5+ items), Math (primary), Physics (high school), Geography (middle school), Social Science (primary), Arabic Language (primary school). This is a stronger regional representation than anticipated by the benchmark YAML's uncertainty.
- **Deployment relevance:** Palestine is a deployment country, and its curriculum content is substantively represented. For STEM and language subjects, Palestinian curriculum questions appear consistent with pan-Arab academic content and do not differ from Jordanian content in ways that would cause validity problems.
- **Datapoint citations:**
  - [D21] Biology (High School), IDs 9699/9707/9834, Palestine, label=B/C/B: "مقدار تكبير العدسة الزيتية في المجهر الضوئي هو: X100" — Palestinian HS biology is standard STEM content
  - [D20] Computer Science (Primary School), IDs 7354–7599, Palestine: "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" — Palestinian primary CS questions
  - [D17] Geography (Middle School), ID 8136, Palestine, label=D: "من الجزر المحيطة بقارة أقيانوسيا: جميع ما ذكر" — Palestinian geography content is globally framed, not locally contested

#### Strength 3: Morocco is present with country-specific legal/professional content
- **Dimension(s):** IO, IC
- **Observation:** The Law (Professional) config consists entirely of Morocco-sourced questions in the sample (all 5 examples, Country=Morocco), drawn from Moroccan procedural law. This confirms Morocco has substantive, country-specific representation in at least one subject area. The legal language is distinctly Moroccan in register and references Moroccan legal institutions.
- **Deployment relevance:** Morocco is a flagged coverage gap in the deployment context. Finding authentic Moroccan-sourced content confirms the country is not entirely absent, though its coverage is concentrated in a subject area (professional law) that is out of scope for the tourist/expat school-knowledge use case.
- **Datapoint citations:**
  - [D5] Law (Professional), ID 4824, Morocco, label=E: "يتم استدعاء الشهود بأحد الطرق التالية... الطريقة الإدارية / جميع الأجوبة صحيحة" — Moroccan procedural law question with five options, distinctly Moroccan legal framing
  - [D5] Law (Professional), ID 4652, Morocco, label=C: "من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" — Moroccan "Gendarmerie Royale" ("الدرك الملكي") referenced — culturally distinctive Moroccan institutional name

#### Strength 4: MSA text-only format aligns with deployment's text modality requirement
- **Dimension(s):** IF
- **Observation:** All sampled questions are in Modern Standard Arabic (Arabic script), text-only, with clear question–option structure. There are no images, audio, or multimodal elements in any sampled example. Contextual passages where present (e.g., Arabic Language General config) are also in MSA prose. The format is consistent across all 41 configs.
- **Deployment relevance:** The deployment is text-only and targets MSA-using Arabic learners. The benchmark's uniform MSA text format matches the interaction modality.
- **Datapoint citations:**
  - [D29] Arabic Language (Grammar), ID 12655, null, label=D: "في الآية القرآنية ﴿إنَّ الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحاتِ﴾، ما هو الإعراب الصحيح لكلمة إنَّ: حرف توكيد ونصب" — Clear MSA grammar question, text-only
  - [D15] Arabic Language (General), ID 11728, null, label=B: full passage in MSA prose about Arab history with comprehension question — demonstrates passage-based reading in MSA

#### Strength 5: Broad multi-subject taxonomy across education levels confirmed in data
- **Dimension(s):** IO
- **Observation:** The sampled data confirms 40 distinct tasks are genuinely populated with level-appropriate content: primary school questions are simpler (e.g., basic arithmetic, vocabulary, animal facts), middle school questions involve more abstract concepts, and high school questions involve analytical reasoning. The taxonomy covers STEM, Humanities, Social Science, Language, and Other as labeled.
- **Deployment relevance:** The broad level distribution allows assessment of whether a system can handle the full range of school-curriculum knowledge a tourist might ask about — from basic facts to higher-level concepts.
- **Datapoint citations:**
  - [D38] Natural Science (Middle School), ID 1902, null, label=C: "قام أحمد بحرق كمية من الماغنيسيوم بالمختبر؛ أي المعادلات التالية تصف التفاعل الذي حصل؟" — Level-appropriate chemistry content
  - [D22] Accounting (University), ID 7245, Egypt, label=A: "يفترض أسلوب المراجعة حول الحاسب أنه إذا كانت المدخلات سليمة..." — University-level auditing/IT question
  - [D34] History (Primary School), ID 2437, Jordan, label=D: "يثرب هو الاسم القديم ل: المدينة المنورة" — Primary-level Islamic history fact

#### Strength 6: KSA content confirmed through university-level source URLs
- **Dimension(s):** IO, IC
- **Observation:** The Computer Science (University) config is sourced entirely from KSA (King Saud University: `faculty.ksu.edu.sa`), confirming KSA's presence in at least the STEM university tier. Saudi internal workers are also represented in the annotator pool per the documentation.
- **Deployment relevance:** KSA is a deployment country. The presence of KSA-sourced university STEM questions confirms some Gulf coverage in the benchmark.
- **Datapoint citations:**
  - [D36] Computer Science (University), ID 7280, KSA, label=C: "الكمبيوتر الدقيق هو عبارة عن: جهاز الكمبيوتر المكتبي" — Sourced from `faculty.ksu.edu.sa`, confirming KSA institutional sourcing

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Output form is entirely MCQ — cannot evaluate multi-perspective acknowledgment required by deployment
- **Dimension(s):** OO, OF
- **Observation:** Every single sampled example uses a single-correct-answer MCQ format (options A–E, one labeled correct). Contested historical and civic questions — such as the question about King Abdullah I's positions on Zionism [D1], or the Jordanian-Palestinian political questions [D2, D3] — are all assigned a single "correct" answer from the Jordanian curriculum perspective. The benchmark cannot evaluate whether a system acknowledges competing Palestinian, Egyptian, or pan-Arab framings of the same events.
- **Deployment relevance:** The deployment explicitly requires the system to "acknowledge multiple perspectives and note that different countries hold different positions." This is the most critical structural mismatch: the benchmark scores only factual recall within one curriculum's framing, not pluralistic or explanatory responses.
- **Datapoint citations:**
  - [D1] History (High School), ID 3049, Jordan, label=D: "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" — A question about Jordanian/Palestinian political history has a single Jordanian-curriculum correct answer, with no mechanism to flag that Palestinian perspectives may frame this history differently
  - [D25] Civics (High School), ID 14546, Jordan, label=B: "الدول التي سعت الى اقامة مجلس التعاون الخليجي هي (الامارات العربيه المتحده، قطر، عُمان، اليمن، العراق): لا" — True/false about GCC founding — correct answer is "No" but only one national framing is tested
  - [D18] Geography (Middle School), ID 8064, Palestine, label=C: "جمع ما يلي من عناصر الدولة عدا: الشعب / الاقليم / الاحتلال / السيادة" — "Occupation" (الاحتلال) appears as a distractor for "elements of a state" — a politically loaded framing that receives a single correct answer without any acknowledgment of the contested status of Palestinian statehood

#### CRITICAL Concern 2: Civics content is overwhelmingly Jordan-specific, not pan-Arab or multi-country
- **Dimension(s):** IO, IC
- **Observation:** All 5 sampled Civics (Middle School) items are exclusively about Jordanian political institutions, Jordanian government history, and Jordanian party law. All 5 sampled Civics (High School) items are also Jordan-centric (Jordanian society, Arab Cooperation Council from Jordanian perspective, Jordanian-British treaty). This confirms the Jordan-skew documented in the YAML extends to the civics domain, which is the most sensitive for the multi-perspective deployment requirement.
- **Deployment relevance:** For tourists in any of the other seven deployment countries (Morocco, Egypt, Palestine, Lebanon, UAE, Kuwait, KSA), civics questions about Jordanian government structures, Jordanian army formations, and Jordanian party law have minimal relevance. More critically, a system trained or evaluated on these civics items may produce Jordanian-framed answers to generic Arab civics questions asked by users in other countries.
- **Datapoint citations:**
  - [D4] Civics (Middle School), IDs 14291–14327, Jordan: "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952 وقد عرفت باسم الحكومة: الوطنية" / "القوة العربية من تشكيلات الجيش العربي الأردني في المرحلة: الأولى" / "عُدل قانون الأحزاب الأردني حيث جاء فيه ألا يقل عدد المؤسسين للحزب عن (500) عضو عام: 2007" — All five civics MS items are Jordanian-specific
  - [D2] Civics (High School), ID 14526, Jordan, label=B: "مثّل ______ العرب في مؤتمر الصلح الذي عقده الحلفاء في باريس: الأمير فيصل بن الحسين" — Presents Hashemite framing of pan-Arab representation without acknowledging other national narratives
  - [D3] Civics (High School), ID 14529, Jordan, label=C: "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨" — Highly Jordan-specific political history content

#### MAJOR

#### MAJOR Concern 3: Jordanian-curriculum framing in contested history questions risks annotation bias
- **Dimension(s):** IC, OC
- **Observation:** The history content sampled is heavily Jordanian in framing. The question about King Abdullah I and Zionism [D1] presents the Jordanian narrative as the sole "correct" answer. The question about the 1952 Jordanian constitution [D8] and Hashemite emblem symbolism [D9] treats Jordan-specific historical facts as the authoritative framing. Since no Palestinian annotators verified Palestinian-sourced questions, and the civics sample confirms Jordan-centric framing, the benchmark's ground-truth for contested historical events may reflect Jordanian national consensus rather than pan-Arab or Palestinian perspectives.
- **Deployment relevance:** A system evaluated well on these items might give Jordanian-framed answers to tourists in Palestine, Lebanon, or Morocco who ask about shared historical events. The deployment requires explicit flagging of country-specific perspectives, but the benchmark labels do not encode this requirement.
- **Datapoint citations:**
  - [D1] History (High School), ID 3049, Jordan, label=D: "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين: رفضه معاهدة سايكس بيكو ووعد بلفور رفضاً قاطعاً" — The "correct" answer (he did NOT reject Balfour unequivocally) reflects Jordanian historical consensus that may be contested by Palestinian historiography
  - [D30] History (High School), ID 2827, Jordan, label=A: "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة... القيام بشعائر الأديان" — Jordanian constitutional framing of religious freedom rights
  - [D11] Social Science (Primary School), ID 5481, Jordan, label=D: "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" — Jordanian royal history presented as school-level social science

#### MAJOR Concern 4: Kuwait is effectively absent from the sampled data
- **Dimension(s):** IO, IC
- **Observation:** Across all 41 sampled configs (approximately 210 examples), no single example has Country=Kuwait. The web search findings confirm Kuwait is absent from the country-grouped model performance table in the paper, and no Kuwaiti collaborators are acknowledged. This absence is confirmed in practice by the sampled data.
- **Deployment relevance:** Kuwait is one of the eight deployment countries. Any system evaluated on ArabicMMLU will have essentially no Kuwaiti curriculum exposure in its evaluation, meaning the benchmark cannot assess whether the system handles Kuwait-specific school knowledge appropriately.
- **Datapoint citations:**
  - Zero instances of Country=Kuwait across all 210 sampled examples — absence constitutes the evidence; no positive citations possible

#### MAJOR Concern 5: OCR/digitization quality issues create illegible questions in some university-level items
- **Dimension(s):** IC, OC
- **Observation:** Multiple university-level items from Egyptian sources show severe OCR corruption that renders question text partially or wholly illegible. Characters are scrambled, words are unreadable, and answer options contain garbled text. This affects at least the Management (University) and Political Science (University) configs and potentially others.
- **Deployment relevance:** A system that answers OCR-corrupted questions "correctly" is exploiting noise rather than demonstrating knowledge. Benchmark scores on corrupted items have no validity for the deployment's knowledge-testing purpose. The 96% answer-key accuracy ceiling documented in the YAML may be overestimated for university-level Egyptian content.
- **Datapoint citations:**
  - [D23] Management (University), ID 6175, Egypt, label=C: "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة فتى السشمستة تذتير إلى: ال مركز ة" — Severely corrupted OCR; question is unreadable without reconstruction
  - [D24] Political Science (University), ID 7008, Egypt, label=D: "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ: كل ما سبق" — OCR corruption throughout; answer options also corrupted

#### MAJOR Concern 6: Morocco's curriculum representation is limited to professional law, absent from school-curriculum subjects
- **Dimension(s):** IO, IC
- **Observation:** While Morocco appears in the Law (Professional) config (all 5 sampled items), no Morocco-sourced questions were found in the school-curriculum subjects (History, Geography, Civics, Social Science, Islamic Studies, Arabic Language) across the sampled data. The Moroccan legal questions reference Moroccan legal procedure and institutions, but the deployment requires school-curriculum knowledge (history, geography, Arabic language), which is where Moroccan curriculum distinctiveness (Maghrebi historical framing, French-influenced educational tradition) would matter most.
- **Deployment relevance:** Tourists visiting Morocco and asking about Moroccan history, geography, or civic life will encounter questions where the benchmark provides no Moroccan-curriculum grounding. A system evaluated only on Jordanian and Egyptian history framing may produce non-Moroccan answers to Moroccan historical questions.
- **Datapoint citations:**
  - [D5] Law (Professional), IDs 4824/4843/4880/4881/4652, Morocco: All five Morocco-sourced samples are procedural law items — none are from history, geography, or school-level curricula
  - [D4] Civics (Middle School), IDs 14291–14327, Jordan: All five civics MS items are Jordan-only — confirms Morocco's absence from this high-priority subject category

#### MAJOR Concern 7: Islamic Studies content assumes internal Muslim religious perspective, not external educational framing
- **Dimension(s):** IC, OC
- **Observation:** The Islamic Studies questions (at all levels) are framed as internal religious knowledge questions — asking about the number of Prophet Muhammad's Umrah pilgrimages, which Quranic surah contains specific stories, and prescribed Islamic ritual practice. The Arabic Language (General) config uses a reading passage that frames Islamic purification practices prescriptively ("لا يمكن أنْ يصلي المسلم بدون وضوء"). These are presented as school-curriculum content for Muslim students, not as culturally informative questions for non-Muslim visitors.
- **Deployment relevance:** The deployment's target population are non-native, non-Arab tourists and expats, many of whom may be non-Muslim. A system evaluated on these items is tested for its ability to reproduce internal Islamic religious knowledge, not for its ability to explain Islamic practices to a non-Muslim visitor in an appropriately explanatory, non-prescriptive register. The benchmark cannot evaluate whether the system frames Islamic content accessibly for outsiders.
- **Datapoint citations:**
  - [D14] Islamic Studies (General), ID 46, null, label=A: "كم مرة اعتمر النبي صلى الله عليه وسلم؟ أربع عمرات" — Internal Islamic knowledge question presupposing Muslim reader
  - [D35] Arabic Language (General), ID 12069, null, label=B: "لا يمكن أنْ يصلي المسلم [فراغ]: بدون وضوء" — Reading passage frames Islamic ritual as prescriptive instruction ("the Muslim cannot pray without wudu") rather than descriptive/educational
  - [D31] Islamic Studies (High School), ID 14064, Jordan, label=E: "للتفكير آثار إيجابية عدة: جميع ما ذكر" — Islamic studies HS question framing positive thinking within Islamic value framework

#### MINOR

#### MINOR Concern 8: Driving Test questions are out-of-scope for school-curriculum knowledge deployment
- **Dimension(s):** IO
- **Observation:** The Driving Test config includes questions about traffic rules, road safety, and vehicle operation from Egypt, UAE, and Lebanon. These are practical regulatory knowledge items, not school-curriculum knowledge about Arab history, geography, or language.
- **Deployment relevance:** The deployment explicitly scopes to "school-curriculum-level general knowledge (history, geography, Arabic language)" with practical travel knowledge explicitly out of scope. Driving test performance scores are not informative for the tourist knowledge-assistant use case, and including this config in aggregate scoring could dilute or mislead benchmark-to-deployment mapping.
- **Datapoint citations:**
  - [D26] Driving Test, ID 687, UAE, label=A: "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر من مركبتك" — Practical traffic safety rule, not school-curriculum knowledge
  - [D26] Driving Test, ID 1025, Lebanon, label=C: "يُحَظَّر على سائق المركبة: يجري مناورة عكس الإتجاه (Demi Tour) وسط الطريق العام" — Note "Demi Tour" (French term) embedded in Arabic text — reflects Lebanon's French-influenced regulatory register

#### MINOR Concern 9: Some General Knowledge items cover vocational and institutional knowledge irrelevant to tourist context
- **Dimension(s):** IO
- **Observation:** General Knowledge (Primary) and General Knowledge (Middle School) samples include items about sheet metal screws, metal welding, Jordanian Royal Medical Services hospital names, and road safety. These are Jordanian school curriculum items that have no relevance to a tourist or expat seeking knowledge about Arab history and culture.
- **Deployment relevance:** These items contribute to benchmark scores but do not test the specific knowledge domains (history, geography, Arabic language) the deployment targets. High performance on vocational GK does not predict performance on culturally relevant questions.
- **Datapoint citations:**
  - [D27] General Knowledge (Primary School), ID 4381, Jordan, label=B: "برغي سن الصاج هو: مسمار لولبي الشكل مسلوب من نهايته" — Sheet metal screw definition — vocational, not culturally relevant
  - [D10] Social Science (Primary School), ID 5489, Jordan, label=D: "تشمل الخدمات الطبية الملكية الحكومية... مستشفى المدينة الطبية" — Jordanian Royal Medical Services hospitals — Jordan-institutional, not pan-Arab knowledge

#### MINOR Concern 10: One Arabic Language Grammar question has an English question stem
- **Dimension(s):** IF
- **Observation:** In Arabic Language (Grammar), example ID 12626, the question stem is in English: "In the following Quranic verse, what is the correct parsing of the word ـكَ" — while the answer options are in Arabic. This is an unexpected language mix in a benchmark that claims to be exclusively in MSA Arabic (excluding English questions by design).
- **Deployment relevance:** This is a minor data quality observation. The question is answerable in Arabic, but the English stem creates an inconsistency in the input form distribution. For a system tested on purely Arabic inputs, this question introduces a signal that may not represent the benchmark's intended register.
- **Datapoint citations:**
  - [D16] Arabic Language (Grammar), ID 12626, null, label=A: "In the following Quranic verse, what is the correct parsing of the word ـكَ: مضاف إليه مجرور وعلامة جره الكسرة" — English question stem with Arabic answer options; unexpected language mixing

#### MINOR Concern 11: Some Geography items ask about global (non-Arab) facts, reducing regional specificity
- **Dimension(s):** IC
- **Observation:** Several Geography items ask about non-Arab global knowledge: Mt. Kilimanjaro in Tanzania, Shanghai as an industrial smog city, the height of the snow line in equatorial regions, cold ocean currents (West Australia Current). While legitimate world geography content, these do not test Arabic/Arab-regional knowledge specifically.
- **Deployment relevance:** For the deployment's focus on "Arab history and geography," these items have lower diagnostic relevance. However, they do represent the type of factual geography knowledge a tourist might ask about.
- **Datapoint citations:**
  - [D] Geography (High School), ID 8189, Jordan, label=B: "يبلغ ارتفاع جبل كلمنجارو في تنزانيا: 5800 م" — Kilimanjaro altitude — global geography, not Arab-specific
  - [D] Geography (High School), ID 8216, Jordan, label=A: "من المدن الصناعية التي يتكون فيها الضباب الدخاني: شنغهاي" — Industrial smog cities — Shanghai as answer, global content

---

### Content Coverage Summary

The sampled data reveals a benchmark that is predominantly Jordanian in its civics and history domains (all 10 sampled civics items across middle and high school are Jordan-only), moderately represented by Egypt (university-level accounting, economics, political science, philosophy), and more lightly populated by Palestine (strong STEM presence at primary-high school level but minimal contested-history items in the sample), KSA (university STEM), Morocco (professional law only), and Lebanon (driving test). No Kuwait-sourced items appear in any sampled config.

The register is consistently MSA — formal written Arabic appropriate for school examinations — with occasional OCR-corruption artifacts particularly in Egyptian university-level items. One grammar item has an English question stem. The content divides roughly into: (a) culturally neutral STEM items (biology, physics, chemistry, math, computer science) sourced mainly from Jordan and Palestine; (b) Jordanian-centric civic and historical items; (c) pan-Islamic religious knowledge items (Islamic Studies across all levels, pan-Islamic Arabic Language reading texts); (d) Jordanian vocational and institutional items (driving, school tracking, hospital names); and (e) a small Moroccan professional law cluster.

For the deployment's school-curriculum tourist knowledge use case, the most relevant content is in History, Geography, Islamic Studies, Arabic Language, and Social Science. Of these, History and Civics are heavily Jordanian-framed, Geography includes both Jordan-specific and world-geography content, and Islamic Studies presents religious practice as internal knowledge rather than cultural explanation. The Arabic Language configs are well-suited to testing MSA grammar and vocabulary in an educational register.

---

### Limitations

1. **Sample size per config**: Only 5–8 examples per config were available. Some patterns (e.g., complete absence of Kuwait, Morocco's concentration in Law) may be sample artifacts rather than true distributional properties, though they are corroborated by the web search findings.

2. **Country field reliability**: A meaningful number of examples have Country=null (especially in Islamic Studies (General), Natural Science, Physics, Social Science Middle School, and Arabic Language configs). It is not possible from the sample to determine whether null-country items are truly country-agnostic (pan-Arab) or reflect metadata collection gaps.

3. **Contested content not reliably identifiable from MCQ alone**: The most critical deployment concern — whether contested historical questions have ground-truth labels that reflect one national perspective — cannot be fully verified by reading MCQ text alone. Deeper subject-matter analysis by area experts in Palestinian, Moroccan, and pan-Arab historiography would be needed.

4. **Inter-config quality variation**: OCR quality appears to vary substantially across sources. The university-level Egyptian social science items show severe digitization artifacts not visible in primary and middle school Jordanian items. The proportion of corrupted items across the full 14,575-question dataset cannot be estimated from this sample.

5. **Kuwait absence**: The inference that Kuwait is absent or minimally present is based on zero appearances in ~210 sampled examples and the absence from named country lists in the paper. This cannot be ruled out as a sampling artifact without examining the full dataset metadata.

6. **Islamic Studies register analysis**: Whether the Islamic Studies content is presented in an internal-community vs. external-educational register is a judgment call requiring expert review; the sample provides suggestive evidence but not a definitive audit.

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
  "benchmark": "arabicmmlu",
  "region": "Non-Arab Tourists and Expats in Eight Arabic-Speaking Countries (ArabicMMLU Deployment)",
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
