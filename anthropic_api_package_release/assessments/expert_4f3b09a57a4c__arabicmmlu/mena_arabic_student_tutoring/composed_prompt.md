I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **ArabicMMLU: Advancing Rigorous Arabic Language Evaluation** is valid for use in **MENA Multi-Country Arabic Tutoring System — Eight-Country Curriculum Deployment**.

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
- **Full Name**: ArabicMMLU: Advancing Rigorous Arabic Language Evaluation
- **Domain**: Arabic language understanding and knowledge evaluation
- **Languages**: ar
- **Porting Strategy**: ground_up
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
ArabicMMLU covers 40 tasks spanning a wide range of subjects and education
levels [Q25], explicitly framing itself as a shift from classification-heavy
Arabic NLP benchmarks toward reasoning and knowledge evaluation [Q10, Q24].
Subject groups are organized into STEM, Social Science, Humanities, Arabic
Language, and Other [Q107], with education levels spanning primary, middle,
high school, and university. For the tutoring deployment, this taxonomy is
broadly relevant: it covers the educational strata (primary through university)
the system targets and explicitly includes subjects — history, geography,
civics, political science — that carry country-specific content variation [Q72,
Q73]. High school questions are confirmed as meaningfully harder than primary
or middle school questions [Q68], and negation is examined as a distinct
analytical dimension [Q84], indicating the taxonomy captures some linguistic
complexity beyond factual recall.

However, university-level coverage is thin at approximately 6% of all
questions [Q71], which is a significant gap for the deployment's goal of
supporting university students in law, management, economics, and political
science. Future work is proposed to extend ArabicMMLU to include short-answer
and essay formats, different modalities, larger regional coverage, and
professional-setting questions [Q88], but these remain aspirational. The
benchmark is the first of its kind for Arabic [Q1], and its taxonomy does not
include any dialect-specific tasks or French-medium content [Q92].

### Input Content
Questions are sourced from real school examinations across eight countries in
North Africa, the Levant, and the Gulf [Q26], making the benchmark's
content-level regional grounding considerably stronger than translated MMLU
alternatives [Q5, Q6]. Data collection involved 10 native Arabic speakers (6
internal, 4 external) who identified publicly available exam URLs and manually
scraped metadata including source URL, country, subject, level, question text,
answer options, and correct answer key [Q31, Q32, Q33]. Each external worker
collected approximately 2,000 questions; internal workers collected 1,000–2,000
each [Q34].

However, a critical content-level imbalance exists: Jordan alone contributed
over 6,000 questions while other countries contributed as few as 100 or, in
some cases, none at all [Q89], driven by uneven digitization of national exams
[Q90] and non-exhaustive internet search [Q91]. Documented worker nationalities
are exclusively Jordanian, Egyptian, Lebanese, Emirati, and Saudi [Q31],
with no documented collaborators from Kuwait, Palestine, or Morocco [Q96],
raising material questions about whether those national curricula were
systematically identified and collected. The benchmark also explicitly excluded
English-language questions [Q30] and questions lacking answer keys or
containing multimodal content [Q37], further constraining which exam content
was ingested. Prior multilingual benchmarks (XGLUE, XTREME, GEM) and
Arabic-centric benchmarks (Dolphin, OCRA, LAraBench) are acknowledged as
antecedents [Q22, Q23], but ArabicMMLU distinguishes itself by sourcing native
exam content rather than translated material [Q5].

### Input Form
All 14,575 questions are in Modern Standard Arabic (MSA) [Q2], which is the
formal medium of instruction in public schools across all eight target countries
[Q29]. Multimodal content (images, videos, tables) was explicitly excluded [Q37],
making the benchmark entirely text-based. When contextual passages were
required by questions, they were included with each dependent question [Q38].
Prompt templates include country-, subject-, and level-aware placeholders in
both Arabic and English [Q49], as illustrated in the benchmark's prompt figures
[Q48, Q99]. The Arabic negation analysis uses specific Arabic negation phrases
to identify negated questions [Q85], confirming Arabic-script fidelity.

The MSA-only format aligns well with the formal instructional medium of all
eight deployment countries at the school level. However, the benchmark's
exclusive focus on MSA means French-medium Moroccan university content — a
legitimate deployment target — is entirely outside scope [Q92]. Dialectal
Arabic is also absent, though the deployment explicitly excludes Darija, making
this a partial rather than total mismatch.

### Output Ontology
The label schema is a flat single-correct-answer MCQ structure with 2–5
candidate options per question [Q27]. This is directly shared with the
tutoring deployment's MCQ context, reducing output ontology mismatch for
multiple-choice instructional settings. The benchmark organizes results by
subject group (STEM, Social Science, Humanities, Arabic Language, Other [Q107])
and education level, providing a diagnostic output taxonomy with granular
per-subject and per-level breakdowns [Q102, Q103].

However, the flat label structure encodes a single ground-truth answer without
any country-specific branching. For subjects like law or civics where correct
answers may legitimately differ by national jurisdiction — for example, a
question on civil liability sourced from an Egyptian exam may carry an Egyptian
civil-law answer as universal ground truth — the output taxonomy provides no
mechanism to represent jurisdiction-specific correctness. The benchmark notes
this implicitly by observing that Arabic-specific content makes ArabicMMLU
harder than translated MMLU [Q64, Q65], but does not document any country-
stratified label scheme or secondary annotation layer.

### Output Content
Quality assurance involved two native Arabic speakers independently annotating
100 randomly sampled questions, verifying correctness using available resources
including search engines [Q42]; the agreement rate was 96%, designated as the
practical ceiling score for the benchmark [Q43, Q44]. Workers are native MSA
speakers with at least Bachelor's degrees — internal workers are Master's
students and Research Assistants in Computer Science, external workers hold
Bachelor's degrees [Q35, Q39] — and compensation exceeded monthly average
wages in each respective country [Q36]. A one-hour orientation workshop was
conducted before data collection [Q40].

The annotation workforce is geographically limited to Jordanian, Egyptian,
Lebanese, Emirati, and Saudi workers [Q31], with no documented annotators from
Kuwait, Palestine, or Morocco [Q96]. This means ground-truth labels for
questions nominally sourced from Kuwaiti or Palestinian curricula — if such
questions exist — would have been verified by workers potentially unfamiliar
with those national educational contexts. The 96% agreement figure provides
a reasonable but not comprehensive quality signal: no formal inter-annotator
agreement statistic beyond this spot-check figure is reported, and contamination
of model pretraining data cannot be ruled out [Q94, Q95].

### Output Form
The benchmark evaluates models in zero-shot and few-shot settings [Q45] across
35 models [Q46] using accuracy as the primary metric. For open-source models,
the answer is determined by the highest softmax-normalized probability among
candidate options [Q50, Q79]; for closed-source models, the first generated
token is extracted via regular expression with random assignment on failure
[Q53, Q54]. Four prompt-language and output-alphabet combinations were tested
[Q47], with English prompt and English alphabetic output found optimal for most
models [Q56, Q58], though Arabic-centric models show greater robustness to
Arabic alphabetic output [Q57]. Calibration analysis confirms r > 0.9
correlation between answer probability and accuracy for all three analyzed
open-source models [Q80].

The MCQ accuracy-based output form aligns well with the deployment's use case:
the user confirmed that for MCQ tasks, explanation format is not exam-critical
[Q3 in elicitation], and the benchmark does not evaluate explanation quality.
Detailed zero-shot results per subject and education level [Q102, Q103] and per
subject group under all four prompt configurations [Q105, Q106, Q108, Q110]
provide granular diagnostic capability for the deployment context.


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
| Q8 | 1 | input_content | "Fajri Koto, Haonan Li, Sara Shatnawi, Jad Doughman, Abdelrahman Boda Sadallah, Aisha Alraeesi, Khalid Almubarak, Zaid Alyafeai, Neha Sengupta, Shady Shehata, Nizar Habash, Preslav Nakov, Timothy Baldwin" |
| Q9 | 1 | input_content | "Department of Natural Language Processing, MBZUAI; Prince Sattam bin Abdulaziz University; King Fahd University of Petroleum and Minerals; Core42; New York University Abu Dhabi; The University of Melbourne" |
| Q10 | 1 | input_ontology | "The evaluation of language models has increasingly shifted from linguistically-centric tasks, such as part-of-speech (POS) tagging and named entity recognition (NER), towards reasoning and knowledge evaluation." |
| Q11 | 2 | input_content | "Early Arabic pretrained language models typically had less than 2 billion parameters and were primarily monolingual." |
| Q12 | 2 | input_ontology | "These models can be classified into three main categories: encoder-only, decoder-only, and encoder–decoder models." |
| Q13 | 2 | input_content | "The encoder-only models, such as AraBERT (Antoun et al., 2020), CAMeLBERT (Inoue et al., 2021), AraELECTRA (Antoun et al., 2021a), and ARBERT & MARBERT (Abdul-Mageed et al., 2021), are mainly from the BERT family." |
| Q14 | 2 | input_content | "AraGPT2 (Antoun et al., 2021b), on the other hand, is a decoder-only model available in different sizes ranging from 135M to 1.4B parameters." |
| Q15 | 2 | input_content | "Examples of encoder–decoder models include AraT5 (Nagoudi et al., 2022) and AraBART (Kamal Eddine et al., 2022)." |
| Q16 | 2 | input_content | "Jais (Sengupta et al., 2023) and AceGPT (Huang et al., 2023) are two recent Arabic-centric decoder-only models with parameter sizes of up to 30B and 13B, respectively." |
| Q17 | 2 | input_content | "Jais is pretrained on a corpus of 72 billion Arabic tokens, while AceGPT builds upon LLaMA2 and is enhanced with reinforcement learning from AI feedback (Lee et al., 2023) to localize the model to Arabic values and culture." |
| Q18 | 2 | input_content | "Both models are bilingual (English and Arabic), and were fine-tuned on various instruction datasets." |
| Q19 | 2 | input_content | "Arabic is also present in multilingual models." |
| Q20 | 2 | input_content | "This includes earlier models such as mBERT (Devlin et al., 2019) and XLM-R (Conneau et al., 2020), and more recent LLMs such as BLOOMZ (Muennighoff et al., 2022), mT0 (Muennighoff et al., 2022), Falcon (Penedo et al., 2023), GPT-3.5 (Ouyang et al., 2022), and GPT-4 (OpenAI, 2023)." |
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
| Q31 | 4 | input_content | "The data construction process involved a total of 10 Arabic native speakers from different countries: 6 internal workers (1 Jordanian, 1 Egyptian, 1 Lebanese, 1 from UAE, and 2 from KSA) and 4 external workers (3 Jordanian and 1 Egyptian)." |
| Q32 | 4 | input_content | "During the first stage of data collection, the internal workers were tasked with collecting relevant sources for data collection. These sources were URLs containing the questions, which needed to be publicly available." |
| Q33 | 4 | input_form | "In the second stage, all workers were asked to manually scrape the data within a 2-month period. The task was to collect metadata, including the source (URL of the source document), country, subject, level, question, multiple-choice options, and the correct answer key." |
| Q34 | 4 | input_content | "Each external worker was assigned to gather 2,000 questions, while internal workers were tasked with gathering 1,000–2,000 questions each." |
| Q35 | 4 | output_content | "Our internal workers are Master's students and Research Assistants in Computer Science, while the external workers hold Bachelor's degrees." |
| Q36 | 4 | output_content | "We ensured competitive compensation for the workers, exceeding the monthly average wage in each respective country." |
| Q37 | 4 | input_form | "During manual data scraping, workers were instructed to include only questions accompanied by an answer key, and to discard questions containing multi-modal information (e.g., images, videos, or tables)." |
| Q38 | 4 | input_form | "If a question had additional contextual information (e.g., a passage referenced by several questions), the context was required to be included with each corresponding question." |
| Q39 | 4 | output_content | "While our workers are native speakers of Modern Standard Arabic with at least Bachelor's degrees, we maintain the quality of our dataset construction through meticulous steps." |
| Q40 | 4 | output_content | "Firstly, we conducted a 1-hour workshop before the data collection stage to clarify the process." |
| Q41 | 4 | input_form | "Secondly, we automatically filtered out repetitive questions and those without an answer key, reducing the initial set of over 15,000 questions to 14,575 unique questions." |
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
| Q64 | 7 | output_content | "It is noteworthy that in the GPT-4 technical report (OpenAI, 2023), the accuracy of the English-Arabic translated MMLU dataset is reported as 80%, which is 8 points higher than our ArabicMMU results." |
| Q65 | 7 | output_content | "One possible explanation for this difference is that our ArabicMMU presents a greater challenge due to its inclusion of a higher proportion of Arabic-specific content." |
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
| Q83 | 8 | input_ontology | "Despite negation being an absolutely foundational linguistic phenomenon, LLMs have been shown to be worryingly insensitive to its effects in English (Kassner and Schütze, 2020; Hosseini et al., 2021; Truong et al., 2023)." |
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
| Q94 | 9 | output_content | "It is important to emphasize that our experimental results do not provide conclusive answers regarding the performance of LLMs in Arabic." |
| Q95 | 10 | output_content | "to a lack of sufficient information about its training regimen. As such, we cannot assert that the model's pretraining data is free from contamination." |
| Q96 | 10 | input_content | "We extend our gratitude to all collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia who participated in the data collection process." |
| Q97 | 10 | input_content | "We also acknowledge the contributions of Samta Kamboj, Sarah Al Barri, and Onkar Pandit from Core42, who assisted in collecting the Arabic Language question dataset." |
| Q98 | 14 | input_content | "Table 7 presents the distribution of ArabicMMLU data categorized by subject across different education levels." |
| Q99 | 14 | input_form | "Figure 10 illustrates a complete example of prompts used in this study. This example features a Natural Science question with prompts provided in both Arabic and English." |
| Q100 | 14 | input_ontology | "This is a Natural Science question for primary school in Jordan. Select the correct answer!" |
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
| Q111 | 19 | input_content | "Table 12 lists the sources of pre-trained models used in this study. All models are sourced from Huggingface (Wolf et al., 2020)." |
| Q112 | 19 | input_content | "With the exception of GPT-3.5 and GPT-4, all the models used in this study were sourced from Huggingface (Wolf et al., 2020)." |

---

## Regional Context

```yaml
name: MENA Multi-Country Arabic Tutoring System — Eight-Country Curriculum Deployment
abbreviation: mena-tutoring-8country
assessment_slug: arabicmmlu
deployment_context: 'AI tutoring system providing curriculum-aligned MCQ support and
  explanations for students at primary, middle, high school, and university levels
  across eight MENA countries: Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait,
  and Saudi Arabia.'
target_population:
  description: Students enrolled in national educational systems across eight MENA
    countries, ranging from primary school through university level. Includes students
    preparing for high-stakes national examinations (Thanawiyya Amma, Tawjihi, Gulf
    equivalents) and university students studying management, economics, law, CS,
    political science, and accounting. The population is predominantly Sunni Muslim
    across all eight countries.
  geographies:
  - Morocco (North Africa)
  - Egypt (North Africa)
  - Jordan (Levant)
  - Palestine (Levant)
  - Lebanon (Levant)
  - UAE (Gulf)
  - Kuwait (Gulf)
  - Saudi Arabia (Gulf)
  education_levels:
  - Primary school
  - Middle school
  - High school (pre-university / baccalaureate / Tawjihi / Thanawiyya Amma)
  - University (undergraduate)
  occupational_role: Students — exam-preparation and coursework support
  religious_demographic: Predominantly Sunni Muslim across all eight countries; Shia-specific
    fiqh rulings are out of scope for this deployment
languages:
  primary: Modern Standard Arabic (MSA) — formal medium of instruction for school-level
    content across all eight countries
  secondary: French — medium of instruction for science and certain professional/university
    programs in Morocco
  excluded: Moroccan Darija (spoken colloquial Arabic) — explicitly out of scope for
    this deployment
  diglossia_note: 'Diglossia is structurally present across all eight countries: MSA
    governs formal written instruction and assessment; regional colloquials (Gulf
    Arabic, Levantine Arabic, Darija) govern everyday speech. This deployment targets
    MSA exclusively for school contexts, with French as a partial secondary medium
    for Moroccan higher education.'
  french_scope_note: French-medium content applies only to Moroccan university-level
    subjects (sciences, certain professional programs). School-level Moroccan content
    is MSA-compatible. French medium falls entirely outside ArabicMMLU scope.
writing_systems:
  scripts:
  - Arabic script (right-to-left) — primary for all MSA content
  - Latin script (French-medium Moroccan university content)
  rtl_note: Arabic script RTL rendering and Arabic morphological complexity (root-pattern
    system) are relevant NLP considerations for the tutoring system's input processing
    and response generation.
national_curriculum_systems:
- country: Morocco
  curriculum_authority: '[NEEDS VERIFICATION — deferred: below search budget; scaffold
    value ''Ministry of National Education, Preschool and Sports'' is likely correct
    but official Arabic name unverified]'
  exam_system: Baccalauréat (French-influenced system); primary/middle cycle exams
  language_of_instruction: MSA for humanities/Islamic studies/Arabic language; French
    for science and professional university tracks
  distinctive_features: French-influenced baccalaureate structure; bilingual MSA/French
    higher education; Maliki madhab for Islamic studies
  benchmark_coverage_note: 'No Moroccan workers documented in ArabicMMLU data collection
    workforce; benchmark paper explicitly notes some countries contributed ''as few
    as 100 questions or, in some cases, not at all.'' Figure 1 in the paper shows
    Morocco among lower contributors; a bar exam question from Morocco is illustrated
    as an example, suggesting some Moroccan content is present but at uncertain and
    likely low volume. Source: ArabicMMLU paper arXiv:2402.12840 — [WEB-1]'
- country: Egypt
  curriculum_authority: '[NEEDS VERIFICATION — deferred: below search budget; scaffold
    value ''Ministry of Education and Technical Education'' is likely correct but
    unverified]'
  exam_system: Thanawiyya Amma (general secondary certificate)
  language_of_instruction: MSA
  distinctive_features: High-stakes rote-learning culture; centralized national exam
    with standardized answer banks; Egyptian civil law tradition relevant for university
    law content
  benchmark_coverage_note: 'Egyptian workers documented in benchmark workforce (1
    internal Jordanian-Egyptian mix, 1 external Egyptian worker per Q31 in benchmark
    paper). The paper identifies Jordan, Egypt, and Palestine as the top three contributor
    countries by question count (Figure 1 of arXiv:2402.12840 shows Egypt as a high
    contributor). Exact count not published as text-extractable figure. Source: ArabicMMLU
    — [WEB-1]'
- country: Jordan
  curriculum_authority: '[NEEDS VERIFICATION — deferred: below search budget; scaffold
    value ''Ministry of Education'' is likely correct but unverified]'
  exam_system: Tawjihi (General Secondary Certificate Examination)
  language_of_instruction: MSA
  distinctive_features: Tawjihi is high-stakes; Jordan is the dominant contributor
    to ArabicMMLU (over 6,000 questions); Jordanian legal framework relevant for university
    law
  benchmark_coverage_note: 'Over 6,000 questions from Jordan confirmed in ArabicMMLU
    paper — benchmark heavily biased toward Jordanian curriculum content. Jordan,
    Egypt, and Palestine listed as ''top'' three source countries in Figure 1. Source:
    ArabicMMLU arXiv:2402.12840 — [WEB-1]'
- country: Palestine
  curriculum_authority: '[NEEDS VERIFICATION — deferred: below search budget; scaffold
    value ''Palestinian Ministry of Education and Higher Education'' is likely correct
    but unverified]'
  exam_system: '[NEEDS VERIFICATION — deferred: below search budget; likely ''Palestinian
    General Secondary Certificate (Tawjihi)'' but exact official name unverified]'
  language_of_instruction: MSA
  distinctive_features: Distinct national curriculum with Palestinian history and
    civics content not shared with other Levant countries; no Palestinian workers
    documented in ArabicMMLU collection
  benchmark_coverage_note: 'Palestine is listed among the top three contributor countries
    by question count in ArabicMMLU Figure 1 (alongside Jordan and Egypt), which is
    a partial contradiction of the benchmark''s acknowledgment that some countries
    contributed ''as few as 100 or none.'' Social science questions from Palestine
    are illustrated as examples in the paper (Figure 3). However, no Palestinian workers
    are documented as annotators, so Palestinian questions were verified by workers
    from other national curricula. Exact Palestinian question count is not published
    as a text-extractable figure. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
- country: Lebanon
  curriculum_authority: '[NEEDS VERIFICATION — deferred: below search budget; scaffold
    value ''Centre for Educational Research and Development (CERD)'' is likely correct]'
  exam_system: '[NEEDS VERIFICATION — deferred: below search budget]'
  language_of_instruction: MSA (Arabic language subjects); French or English for science
    tracks depending on school type
  distinctive_features: Multi-confessional society; some curricular sensitivity around
    national history and civic identity; Lebanese workers documented in ArabicMMLU
    workforce
  benchmark_coverage_note: 'Lebanese workers present in benchmark collection (1 internal
    worker). Exact question count not published as text-extractable figure; likely
    moderate contributor. AraSTEM (2024) funded by American University of Beirut may
    supplement Lebanese STEM coverage. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1];
    AraSTEM arXiv:2501.00559 — [WEB-2]'
- country: UAE
  curriculum_authority: '[NEEDS VERIFICATION — deferred: below search budget; scaffold
    value ''Ministry of Education UAE'' is likely correct]'
  exam_system: '[NEEDS VERIFICATION — deferred: below search budget]'
  language_of_instruction: MSA for Arabic-medium subjects; English for science/technology
    tracks in many schools
  distinctive_features: UAE legal system (federal civil law with Sharia overlay) distinct
    from Egyptian civil code; large expatriate school population alongside national
    curriculum; UAE workers documented in ArabicMMLU
  benchmark_coverage_note: 'UAE workers present in benchmark (1 internal worker, Aisha
    Alraeesi documented as Emirati). Exact question count not published as text-extractable
    figure. Open-source models perform notably poorly on UAE-sourced questions in
    the benchmark''s country-stratified analysis. Source: ArabicMMLU arXiv:2402.12840
    — [WEB-1]'
- country: Kuwait
  curriculum_authority: '[NEEDS VERIFICATION — deferred: below search budget; scaffold
    value ''Kuwait Ministry of Education'' is likely correct]'
  exam_system: '[NEEDS VERIFICATION — deferred: below search budget]'
  language_of_instruction: MSA
  distinctive_features: Kuwaiti national history and civic education reflects specific
    Gulf/Kuwaiti national narrative; no Kuwaiti workers documented in ArabicMMLU collection;
    Kuwaiti legal system distinct from other Gulf states
  benchmark_coverage_note: 'No Kuwaiti workers documented in ArabicMMLU collection;
    Kuwait not mentioned in acknowledgments. The benchmark''s own statement that ''other
    countries are represented with only 100 questions or, in some cases, not at all''
    combined with the absence of Kuwaiti annotators strongly implies Kuwait is among
    the lowest or zero-count contributors. Exact count not published as text-extractable
    figure. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
- country: Saudi Arabia
  curriculum_authority: '[NEEDS VERIFICATION — deferred: below search budget; scaffold
    value ''Ministry of Education Saudi Arabia'' is likely correct]'
  exam_system: '[NEEDS VERIFICATION — deferred: below search budget; Qiyas standardized
    tests confirmed as separate Saudi aptitude benchmark; GATmath benchmark exists
    for Saudi GAT verbal/quantitative test]'
  language_of_instruction: MSA
  distinctive_features: Islamic studies heavily prioritized; Hanbali madhab normative
    tradition; Vision 2030 curriculum reforms ongoing; two KSA workers documented
    in ArabicMMLU; multiple Saudi-specific benchmarks now exist (ArabLegalEval sourced
    from Saudi legal documents, GATmath for Saudi GAT)
  benchmark_coverage_note: 'KSA workers present in benchmark (2 internal workers).
    Islamic studies questions prioritized in KSA data per benchmark documentation.
    ArabLegalEval (2024) provides Saudi-law-specific legal benchmark as a complement
    to ArabicMMLU''s general law coverage. GATmath benchmarks for Saudi standardized
    tests also exist. Exact KSA question count in ArabicMMLU not published as text-extractable
    figure. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1];
    ArabLegalEval arXiv:2408.07983 — [WEB-3]'
high_stakes_exams:
  egypt:
    name: Thanawiyya Amma (الثانوية العامة)
    notes: Centralized national exam; rote-learning and standardized answer-bank culture;
      divergence from official marking scheme could disadvantage students in open-ended
      formats (mitigated by MCQ focus of deployment)
  jordan:
    name: Tawjihi (التوجيهي)
    notes: High-stakes secondary exam; well-digitized national exam base; primary
      driver of ArabicMMLU question volume
  morocco:
    name: Baccalauréat
    notes: 'French-influenced baccalaureate structure covering both MSA-medium humanities/Islamic
      studies tracks and French-medium science tracks. A bar exam (legal professional
      exam) from Morocco is illustrated as an example question in ArabicMMLU Figure
      3, indicating some Moroccan exam content is present in the benchmark beyond
      school level. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
  palestine:
    name: '[NEEDS VERIFICATION — deferred: below search budget; likely ''Palestinian
      General Secondary Certificate'' (Tawjihi-equivalent)]'
    notes: 'Palestine is listed among top three ArabicMMLU contributor countries (Figure
      1); social science questions from Palestine are used as illustrative examples
      in the paper. However, no Palestinian annotators are documented in the workforce.
      Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
  lebanon:
    name: '[NEEDS VERIFICATION — deferred: below search budget]'
    notes: '[NEEDS VERIFICATION — deferred: below search budget; Lebanese Baccalaureate
      (Brevet and Baccalauréat libanais) most likely official names but unverified]'
  uae:
    name: '[NEEDS VERIFICATION — deferred: below search budget]'
    notes: 'UAE follows a 4-4-4 school structure (unlike the K-12 structure in other
      countries), which is confirmed in the ArabicMMLU paper as a noted exception.
      Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
  kuwait:
    name: '[NEEDS VERIFICATION — deferred: below search budget]'
    notes: '[NEEDS VERIFICATION — deferred: below search budget]'
  saudi_arabia:
    name: '[NEEDS VERIFICATION — deferred: below search budget; Saudi General Secondary
      Certificate plus Qiyas/GAT standardized tests]'
    notes: 'GATmath is a named benchmark specifically targeting Saudi General Aptitude
      Test (GAT) verbal and quantitative content — a complementary resource to ArabicMMLU
      for Saudi-specific evaluation. Source: Arabic LLM Benchmark survey arXiv:2510.13430
      — [WEB-4]'
subject_domain_notes:
  islamic_studies:
    scope: Covered across all eight countries at school level; prioritized in KSA
      data within ArabicMMLU
    madhab_variation: 'Morocco follows Maliki tradition; Saudi Arabia follows Hanbali
      tradition; Jordan, Palestine, Lebanon predominantly Shafi''i or non-specified
      Sunni; UAE and Kuwait [NEEDS VERIFICATION — deferred: likely unsearchable (lived
      curriculum practice); dominant madhab in school Islamic studies curricula not
      documented in accessible official sources]. Deployment user assessed madhab-specific
      divergence as unlikely at school level, but benchmark madhab-calibration is
      undocumented.'
    madhab_benchmark_status: '[NOT FOUND — searched ArabicMMLU paper directly; no
      mention of madhab calibration or school-of-jurisprudence neutrality in any documentation.
      The benchmark treats Islamic studies as a single subject without madhab labeling.
      This remains an unresolved gap requiring expert elicitation from Islamic studies
      curriculum specialists across the deployment countries.]'
  law:
    scope: University-level; country-specific tailoring required per deployment specification
    subject_taxonomy_confirmation: 'Law is confirmed as a subject within the Humanities
      group in ArabicMMLU, alongside accounting, history, philosophy, and Islamic
      studies. ArabLegalEval (2024) reuses ArabicMMLU''s law and political science
      subsets (299 law samples, 195 political science samples) as baselines, confirming
      these subsets exist and are of assessable size. Source: ArabLegalEval arXiv:2408.07983
      — [WEB-3]; ArabicMMLU — [WEB-1]'
    legal_traditions:
      egypt: 'Egyptian Civil Code (French-influenced civil law tradition; dominant
        MENA model). The Egyptian legal system is explicitly based on French legal
        concepts per historical legal analysis. Source: NYU Globalex Egyptian legal
        system overview — [WEB-5]'
      morocco: 'Moroccan law (French-influenced civil law with Maliki personal status
        law). A Moroccan bar exam question is illustrated in ArabicMMLU Figure 3,
        suggesting Moroccan legal content is present in the benchmark at some level.
        MizanQA (mentioned in benchmark survey 2025) is a named Arabic benchmark specifically
        for Moroccan law, offering a complementary resource. Source: ArabicMMLU arXiv:2402.12840
        — [WEB-1]; Arabic LLM benchmark survey arXiv:2510.13430
        — [WEB-4]'
      jordan: '[NEEDS VERIFICATION — deferred: below search budget; Jordanian civil
        law based on Egyptian code influence confirmed in MENA legal literature but
        university curriculum structure unverified]'
      uae: '[NEEDS VERIFICATION — deferred: below search budget]'
      kuwait: '[NEEDS VERIFICATION — deferred: below search budget]'
      saudi_arabia: 'Saudi law (Sharia-based with regulatory codes). ArabLegalEval
        (2024) is sourced exclusively from Saudi legal documents and provides a dedicated
        benchmark for Saudi legal reasoning — the only jurisdiction-specific Arabic
        legal benchmark identified. Source: ArabLegalEval arXiv:2408.07983 — [WEB-3]'
      lebanon: '[NEEDS VERIFICATION — deferred: below search budget; Lebanese law
        French-influenced, confirmed in MENA legal literature]'
      palestine: '[NEEDS VERIFICATION — deferred: below search budget]'
    benchmark_gap: 'ArabicMMLU flat single-correct-answer schema encodes no country-specific
      legal branching. ArabLegalEval''s reuse of ArabicMMLU law questions (299 samples)
      as a baseline confirms the law subset exists and is usable for evaluation, but
      the source jurisdiction(s) of those questions remain undocumented in the ArabicMMLU
      paper. ArabLegalEval itself is Saudi-only and does not fill the multi-jurisdiction
      gap. Source: ArabLegalEval arXiv:2408.07983 — [WEB-3]'
  national_history_and_civics:
    scope: School level; country-specific correct answers expected; high inter-country
      variation
    variation_note: Palestinian history and national narrative content is entirely
      country-specific. Per the benchmark's Figure 1 analysis, Palestine is a top-three
      contributor, so some Palestinian social science content is present. Kuwaiti
      national history is similarly country-specific and Kuwait has no documented
      annotators. Gulf civic education frameworks differ from Levantine frameworks.
    benchmark_gap: 'Jordan-dominant question distribution means civics and history
      ground truth skews toward Jordanian curriculum framing for the majority of questions.
      Open-source models perform notably poorly on UAE- and Morocco-sourced questions
      in the benchmark''s country-stratified analysis, indicating those country-specific
      contexts are harder for current models. Source: ArabicMMLU arXiv:2402.12840
      — [WEB-1]'
  stem:
    scope: All levels; largely curriculum-neutral for factual content
    notes: 'Mathematics, natural science, physics, chemistry, biology — factual answers
      are consistent across jurisdictions; benchmark coverage expected to be more
      reliable here. STEM subjects confirmed in ArabicMMLU taxonomy: natural science,
      math, physics, biology, computer science. Complementary benchmark AraSTEM (2024,
      AUB) provides 11,637 native Arabic STEM MCQs across math, science, physics,
      biology, chemistry, CS, and medicine, spanning elementary to college level,
      offering a supplementary STEM evaluation resource. Source: AraSTEM arXiv:2501.00559
      — [WEB-2]'
  university_level_subjects:
    subjects:
    - Management
    - Economics
    - Law
    - Computer Science
    - Political Science
    - Accounting
    subject_taxonomy_confirmation: 'All six university-level subjects targeted by
      the deployment are confirmed as named subjects within ArabicMMLU''s 40-task
      taxonomy: CS is in STEM; economics and political science are in Social Science;
      law, accounting, and history (relevant for context) are in Humanities; management
      is in ''Other.'' This confirms the subjects exist in the benchmark, though coverage
      depth per country is not documented. Source: ArabicMMLU moonlight.io literature
      review — [WEB-6];
      ArabicMMLU arXiv:2402.12840 — [WEB-1]'
    benchmark_coverage: 'Approximately 6.1% of ArabicMMLU questions are university-level
      (confirmed: ''proportion of university level questions in ArabicMMLU are ...
      6.1%''). Source: ArabicMMLU arXiv:2402.12840 — [WEB-1].
      Professional-setting questions are listed as future benchmark work. At 14,575
      total questions, approximately 889 questions are university-level across all
      subjects combined.'
    law_subset_size: 'ArabLegalEval''s experimental setup uses 299 law samples and
      195 political science samples from ArabicMMLU as baselines after prompt optimization,
      implying the full law and political science subsets are somewhat larger than
      those figures. Source: ArabLegalEval arXiv:2408.07983 — [WEB-3]'
    economics_political_science: Deployment user indicated general Arabic-world framing
      may be acceptable for economics and political science (not requiring country-specific
      tailoring)
    cs_accounting_management: 'CS, accounting, and management are confirmed as named
      subject categories in ArabicMMLU. Exact question counts per subject not published
      in text-extractable form; given the 6.1% university-level share, individual
      subject coverage at university level is expected to be thin. Source: ArabicMMLU
      arXiv:2402.12840 — [WEB-1]'
  arabic_language:
    scope: Dedicated subject group in ArabicMMLU; grammar, rhetoric, comprehension
    notes: Arabic language questions are curriculum-neutral in terms of linguistic
      correctness; regional variation in literary tradition is minor at school level
  french_medium_moroccan_content:
    scope: Moroccan university science and professional programs taught in French
    benchmark_coverage: Full gap — ArabicMMLU is MSA-only; no French-medium content
      exists in benchmark
    companion_benchmark_status: '[NOT FOUND — searched for French-Arabic bilingual
      benchmark for Moroccan higher education. No dedicated French-Arabic bilingual
      benchmark for Moroccan university science content was identified. MizanQA (Moroccan
      law benchmark, mentioned in Arabic LLM survey) exists for Moroccan legal content
      in Arabic but not for French-medium science. This gap remains unaddressed by
      the existing Arabic NLP benchmark ecosystem. Source: Arabic LLM benchmark survey
      arXiv:2510.13430 — [WEB-4]]'
literacy_and_educational_attainment:
  note: The target population (enrolled students) has high literacy by definition;
    population-level literacy rates are less salient than enrollment and digital access
    rates for this deployment.
  primary_secondary_enrollment_rates:
    morocco: '[NEEDS VERIFICATION — deferred: below search budget]'
    egypt: '[NEEDS VERIFICATION — deferred: below search budget]'
    jordan: '[NEEDS VERIFICATION — deferred: below search budget]'
    palestine: '[NEEDS VERIFICATION — deferred: below search budget]'
    lebanon: '[NEEDS VERIFICATION — deferred: below search budget]'
    uae: '[NEEDS VERIFICATION — deferred: below search budget]'
    kuwait: '[NEEDS VERIFICATION — deferred: below search budget]'
    saudi_arabia: '[NEEDS VERIFICATION — deferred: below search budget]'
  university_enrollment_rates:
    note: '[NEEDS VERIFICATION — deferred: below search budget]'
infrastructure_and_access:
  internet_penetration_by_country:
    regional_average: 'Approximately 69% of the Arab States population uses the internet
      as of 2023 (ITU Facts and Figures 2023). Source: ITU — [WEB-7]'
    gulf_states_summary: 'UAE, Saudi Arabia, and Kuwait are among the world''s highest
      internet penetration countries. 2024 World Bank data (via ITU aggregation) shows
      Saudi Arabia and UAE at approximately 100% internet penetration. Kuwait is also
      in the top global tier. Source: World Bank / statisticsoftheworld.com 2024 —
      [WEB-8]'
    morocco: '[NOT FOUND — specific 2023/2024 figure not retrieved; Arab States regional
      average of 69% applies as lower bound; Morocco has been noted as a growing internet
      market with strong mobile penetration. ITU DataHub available for lookup at [WEB-9]]'
    egypt: '[NOT FOUND — specific 2023/2024 figure not retrieved; internet use among
      Egyptian young adults (18–29) is very high per Arab Barometer 2020 digital divide
      analysis. ITU DataHub available for lookup. Source: Arab Barometer 2020 — [WEB-10]]'
    jordan: '[NOT FOUND — specific 2023/2024 percentage not retrieved; Arab Barometer
      data (2020) shows only 16% of Jordanians report never using the internet, implying
      ~84% usage. Source: Arab Barometer 2020 — [WEB-10]]'
    palestine: '[NOT FOUND — specific 2023/2024 percentage not retrieved; Arab Barometer
      data (2020) shows only 17% of Palestinians report never using the internet,
      implying ~83% usage. Note: Palestine is not an ITU Member State per ITU 2025
      Arab States report. Source: Arab Barometer 2020 — [WEB-10];
      ITU 2025 — [WEB-11]]'
    lebanon: '[NOT FOUND — specific 2023/2024 percentage not retrieved; Arab Barometer
      data (2020) shows only 12% of Lebanese report never using the internet, implying
      ~88% usage — highest in Levant sample. Infrastructure disruption from conflict
      and economic crisis is a relevant caveat for current access reliability. Source:
      Arab Barometer 2020 — [WEB-10]]'
    uae: '~100% internet penetration as of 2024 per World Bank/ITU data. Source: statisticsoftheworld.com
      2024 — [WEB-8]'
    kuwait: '~100% internet penetration as of 2024 per World Bank/ITU data (Kuwait
      ranks 6th globally). Source: statisticsoftheworld.com 2024 — [WEB-8]'
    saudi_arabia: '~100% internet penetration as of 2024 per World Bank/ITU data.
      Source: statisticsoftheworld.com 2024 — [WEB-8]'
  mobile_vs_desktop_access:
    general_pattern: Mobile-dominant access across all eight countries, particularly
      in North Africa and Levant; Gulf states have high smartphone penetration
    regional_mobile_ownership: '83% of the Arab States population owned a mobile phone
      as of the latest available year; ownership exceeds 95% in most countries per
      ITU 2025 Arab States digital development report. Source: ITU 2025 — [WEB-11]'
    gulf_states: 'Smartphone penetration near-universal in UAE, Kuwait, KSA; all three
      at ~100% internet penetration indicating near-universal connected device access.
      Source: statisticsoftheworld.com 2024 — [WEB-8]'
    levant_north_africa: 'Mobile internet is dominant access mode; Arab Barometer
      2020 confirms majority online in Lebanon (~88%), Jordan (~84%), Palestine (~83%).
      Morocco and Egypt have strong mobile internet growth trajectories per ITU data.
      Gender gap in internet use remains notable in Arab States (75% men vs 64% women
      online in 2024). Source: ITU 2025 — [WEB-11]'
  platform_context: Tutoring system delivered via text-based interface; no multimodal
    content required (aligns with ArabicMMLU text-only scope)
cultural_and_pedagogical_norms:
  rote_learning_culture: Rote learning and memorization-oriented exam preparation
    is prevalent, particularly in Egypt (Thanawiyya Amma) and Jordan (Tawjihi). Students
    may expect answers that match official marking-scheme phrasing rather than paraphrased
    explanations.
  mcq_format_alignment: MCQ format is standard across national exams in all eight
    countries; deployment's MCQ focus reduces explanation-format mismatch risk
  authority_and_curriculum_trust: Students and families place high trust in official
    curriculum content; tutoring system responses that diverge from national textbook
    content may be perceived as incorrect regardless of objective accuracy
  islamic_values_integration: Islamic studies is a mandatory subject across all eight
    national curricula; Islamic ethical framing may be embedded in social science
    and humanities questions beyond the dedicated Islamic studies subject
  gender_access_notes: 'Gulf states (UAE, Kuwait, KSA) have specific gender-segregated
    educational environments; no direct impact on text-based tutoring content but
    may affect deployment context. ITU 2024 data confirms a gender gap in internet
    use across Arab States (75% men vs 64% women online), though this gap is less
    pronounced in Gulf states. [NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice); gender-specific curriculum variation at school level not documented
    in accessible official sources]'
  exam_season_intensity: 'High-stakes exam periods (Tawjihi, Thanawiyya Amma) create
    concentrated demand spikes; system should be expected to handle peak load during
    May–June examination period [NEEDS VERIFICATION — deferred: below search budget;
    exact per-country exam calendar dates]'
benchmark_country_coverage_summary:
  jordan:
    workforce_documented: true
    estimated_question_share: 'Dominant — over 6,000 questions [benchmark-documented];
      listed as top contributor in Figure 1. Source: ArabicMMLU arXiv:2402.12840 —
      [WEB-1]'
    coverage_risk: LOW for Jordanian curriculum alignment; HIGH risk of benchmark
      over-representing Jordanian framing for other countries
  egypt:
    workforce_documented: true
    estimated_question_count: 'Listed among top three contributor countries in ArabicMMLU
      Figure 1 alongside Jordan and Palestine. Exact count not text-published; expected
      to be the second-largest contributor given workforce presence (1 internal +
      1 external Egyptian worker). Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
    coverage_risk: MODERATE-LOW — Egyptian workers present and Egypt is a top-three
      contributor; Egyptian legal tradition may dominate law questions
  palestine:
    workforce_documented: false
    estimated_question_count: 'Surprisingly listed among top three contributor countries
      in ArabicMMLU Figure 1. This is notable given no Palestinian annotators are
      documented. Social science questions from Palestine are used as illustrative
      examples. However, no Palestinian workers verified these questions, so ground-truth
      labels for Palestinian questions were assessed by workers from other national
      educational contexts. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
    coverage_risk: MODERATE — Palestinian questions appear to be present in meaningful
      volume, but annotation quality for Palestine-specific content is suspect given
      no Palestinian annotators; national narrative and civic content may carry Jordanian
      or general Levantine framing as ground truth
  lebanon:
    workforce_documented: true
    estimated_question_count: 'Lebanese workers present (1 internal worker); exact
      question count not text-published. Likely moderate contributor. AraSTEM (2024,
      AUB) independently provides Lebanese-institution-affiliated STEM benchmark.
      Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
    coverage_risk: MODERATE — Lebanese workers present; actual coverage unverified;
      multi-confessional civic content likely underrepresented
  uae:
    workforce_documented: true
    estimated_question_count: 'UAE workers present (1 internal worker, Aisha Alraeesi);
      exact count not text-published. Models perform notably poorly on UAE-sourced
      questions in country-stratified analysis, consistent with thin but present coverage.
      Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
    coverage_risk: MODERATE-HIGH — UAE workers present but country-stratified performance
      is low; UAE 4-4-4 school structure distinct from other countries; civic/national
      content likely sparse
  saudi_arabia:
    workforce_documented: true
    estimated_question_count: 'KSA workers present (2 internal workers); Islamic studies
      prioritized. Exact count not text-published. Saudi-specific supplementary benchmarks
      available: ArabLegalEval (Saudi law), GATmath (Saudi GAT). Source: ArabicMMLU
      arXiv:2402.12840 — [WEB-1]; ArabLegalEval arXiv:2408.07983
      — [WEB-3]'
    coverage_risk: MODERATE — KSA workers present; Islamic studies content prioritized;
      legal framework gap at university level (ArabLegalEval fills Saudi law specifically
      but not multi-jurisdictional)
  morocco:
    workforce_documented: false
    estimated_question_count: 'No Moroccan workers documented. Paper states some countries
      contributed ''as few as 100 questions or not at all.'' A Moroccan bar exam question
      is used as an illustrative example in Figure 3, suggesting some content is present.
      However, models perform poorly on Morocco-sourced questions in country-stratified
      analysis, consistent with thin coverage. MizanQA (Moroccan law in Arabic) exists
      as an external supplementary benchmark. Source: ArabicMMLU arXiv:2402.12840
      — [WEB-1]; Arabic LLM benchmark survey arXiv:2510.13430
      — [WEB-4]'
    coverage_risk: HIGH — no Moroccan workers documented; open-source models perform
      worst on Morocco-sourced questions among all countries; French-medium university
      content fully absent; Maliki madhab calibration unverified
  kuwait:
    workforce_documented: false
    estimated_question_count: 'No Kuwaiti workers documented; not mentioned in acknowledgments.
      No Kuwait-specific benchmark or dataset identified in the Arabic NLP benchmark
      ecosystem (Arabic LLM benchmark survey covering 40+ benchmarks does not mention
      a Kuwaiti-specific resource). Benchmark''s own statement (''100 questions or
      not at all'') combined with zero annotators strongly implies minimal or zero
      Kuwait coverage. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1];
      Arabic LLM benchmark survey arXiv:2510.13430 — [WEB-4]'
    coverage_risk: HIGH — no Kuwaiti workers documented; not mentioned in acknowledgments;
      civic education and national history coverage highly suspect; no Kuwait-specific
      Arabic NLP benchmark identified anywhere in the ecosystem
flagged_gaps_for_web_search:
- gap_id: 1
  priority: HIGH
  topic: Palestine curriculum coverage in ArabicMMLU
  search_target: ArabicMMLU Palestine Ministry of Education exam questions Palestinian
    curriculum coverage question count
  resolution_status: 'PARTIALLY RESOLVED — Palestine is confirmed among top-three
    contributors in ArabicMMLU Figure 1, and Palestinian social science questions
    are illustrated as examples. However, no Palestinian annotators are documented.
    Exact count requires inspection of paper figures or dataset release files, not
    available as text. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
- gap_id: 2
  priority: HIGH
  topic: Kuwait curriculum coverage in ArabicMMLU
  search_target: ArabicMMLU Kuwait curriculum questions Kuwaiti school exams civic
    education national history Arabic NLP benchmark
  resolution_status: 'PARTIALLY RESOLVED — No Kuwaiti workers documented; Kuwait not
    mentioned in acknowledgments; no Kuwait-specific Arabic NLP benchmark identified
    in any of the 40+ benchmarks surveyed. Strongly implies near-zero coverage. No
    further search value expected. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1]'
- gap_id: 3
  priority: HIGH
  topic: University-level subject distribution in ArabicMMLU (law, CS, management,
    economics, accounting)
  search_target: ArabicMMLU university level subject distribution law economics political
    science CS management accounting Arabic higher education benchmark
  resolution_status: 'RESOLVED — All six subjects confirmed present in ArabicMMLU
    taxonomy: CS (STEM), economics and political science (Social Science), law, accounting,
    and management (Humanities/Other). ArabLegalEval confirms law subset ~299+ questions
    and political science ~195+ questions. University level = 6.1% of 14,575 ≈ 889
    questions total across all subjects. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1];
    ArabLegalEval arXiv:2408.07983 — [WEB-3]'
- gap_id: 4
  priority: HIGH
  topic: Which national legal traditions are represented in ArabicMMLU law questions
  search_target: ArabicMMLU law questions legal tradition Egyptian civil code UAE
    Moroccan Jordanian jurisdiction MENA curriculum
  resolution_status: 'NOT FOUND — ArabicMMLU documentation does not specify which
    national legal traditions are instantiated in the law questions. A Moroccan bar
    exam question is illustrated as one example, but the dominant jurisdiction(s)
    for the ~299+ law questions are undocumented. Given Jordan''s dominant share,
    Jordanian civil law likely features heavily. ArabLegalEval fills Saudi law specifically
    but does not address multi-jurisdiction coverage. Source: ArabicMMLU arXiv:2402.12840
    — [WEB-1]; ArabLegalEval arXiv:2408.07983 — [WEB-3]'
- gap_id: 5
  priority: HIGH
  topic: Actual per-country question counts in ArabicMMLU (Morocco, Egypt, Lebanon,
    UAE, Kuwait, KSA, Palestine)
  search_target: ArabicMMLU per country question distribution Morocco Egypt Lebanon
    UAE Kuwait Saudi Arabia Palestine dataset statistics
  resolution_status: 'PARTIALLY RESOLVED — Confirmed ranking: Jordan >6,000 (dominant);
    Egypt and Palestine are top-three contributors; Morocco, UAE, Lebanon, KSA are
    lower contributors; Kuwait likely minimal/zero. Exact counts per country are shown
    in Figure 1 of the paper but are not published as extractable text. Inspection
    of the HuggingFace dataset release or paper Figure 1 directly would resolve exact
    counts. Source: ArabicMMLU arXiv:2402.12840 — [WEB-1];
    HuggingFace dataset — [WEB-12]'
- gap_id: 6
  priority: MODERATE
  topic: French-Arabic bilingual benchmark for Moroccan higher education
  search_target: French Arabic bilingual benchmark Morocco university higher education
    science NLP evaluation baccalauréat
  resolution_status: 'NOT FOUND — No French-Arabic bilingual benchmark for Moroccan
    university science or professional education exists in the Arabic NLP benchmark
    ecosystem. MizanQA covers Moroccan law in Arabic only. The gap is confirmed as
    unaddressed. Source: Arabic LLM benchmark survey arXiv:2510.13430 — [WEB-4]'
- gap_id: 7
  priority: MODERATE
  topic: ArabicMMLU Islamic studies madhab calibration (Maliki, Hanbali, Shafi'i neutrality)
  search_target: ArabicMMLU Islamic studies madhab Maliki Hanbali Shafi'i school jurisprudence
    Arabic benchmark question calibration neutrality
  resolution_status: NOT FOUND — No documentation of madhab calibration or school-of-jurisprudence
    neutrality found in ArabicMMLU paper or any secondary literature. Islamic studies
    is treated as a single subject. This gap requires expert Islamic studies curriculum
    elicitation, not web search.
- gap_id: 8
  priority: MODERATE
  topic: Rubric alignment between ArabicMMLU ground truth and national marking schemes
    (Thanawiyya Amma, Tawjihi)
  search_target: Arabic educational benchmark marking scheme rubric alignment Egyptian
    Jordanian Thanawiyya Tawjihi national exam answer key validation
  resolution_status: NOT SEARCHED — deferred; below search budget. The MCQ format
    of the deployment mitigates this gap significantly per the elicitation. Deferred
    to human expert follow-up.
- gap_id: 9
  priority: LOWER
  topic: Exact national exam calendars for all eight countries (exam season timing)
  search_target: Thanawiyya Amma Tawjihi Baccalauréat UAE Kuwait KSA secondary exam
    dates schedule 2024 2025
  resolution_status: NOT SEARCHED — deferred; below search budget.
dimension_priority_weights:
  IO:
    priority: HIGH
    rationale: Palestine absent from documented workforce but confirmed as top-three
      contributor by question count — a nuanced finding that partially mitigates but
      does not eliminate the coverage concern; Kuwait likely underrepresented with
      near-zero questions and no annotators; university-level subjects (law, CS, management,
      accounting) confirmed present but constitute only ~6.1% of benchmark (~889 questions
      total); uneven per-country coverage across all eight deployment targets confirmed
  IC:
    priority: HIGH
    rationale: Country-specific legal systems, national history, and civics vary substantially
      across the eight countries; Jordanian-dominant question distribution may impose
      Jordanian framing as universal ground truth for other seven curricula; models
      perform notably poorly on Morocco- and UAE-sourced questions, confirming content-level
      gaps for those deployment countries
  IF:
    priority: MODERATE
    rationale: MSA aligns well for school-level deployment; French-medium Moroccan
      university content falls entirely outside benchmark scope and no companion benchmark
      exists; Darija excluded by deployment design
  OO:
    priority: MODERATE
    rationale: MCQ format shared between benchmark and deployment reduces scoring
      mismatch; flat label schema provides no mechanism for jurisdiction-specific
      correct answers in law/civics; this limitation is documented and unresolved
  OC:
    priority: HIGH
    rationale: Ground-truth labels for Kuwait questions (if any) verified by workers
      from other national educational contexts; Palestine questions verified without
      Palestinian annotators despite being a top-three contributor; 96% agreement
      ceiling established on general sample, not country-stratified; country-stratified
      annotation quality is unknown and likely lower for Kuwait, Morocco, and possibly
      UAE
  OF:
    priority: LOWER
    rationale: Both benchmark and deployment use MCQ output; the user confirmed that
      explanation format is not exam-critical for MCQ contexts; output form mismatch
      is minimal
net_new_fields:
  companion_benchmarks_discovered:
  - name: AraSTEM
    year: 2024
    description: 11,637 native Arabic MCQs in STEM subjects (math, science, physics,
      biology, chemistry, CS, medicine) spanning elementary to college level. Funded
      by American University of Beirut. Complements ArabicMMLU's thinner STEM coverage
      and provides a Levant-affiliated institution perspective.
    relevance: Directly relevant for the deployment's CS and science university-level
      subjects; provides richer STEM evaluation signal than ArabicMMLU's ~6.1% university-level
      slice.
    source: AraSTEM arXiv:2501.00559 — [WEB-2]
  - name: ArabLegalEval
    year: 2024
    description: Multitask Arabic legal benchmark sourced from Saudi legal documents
      and synthesized questions. Evaluates GPT-4 and Jais on Saudi legal reasoning.
      Also reuses ArabicMMLU's law (~299 questions) and political science (~195 questions)
      subsets as baselines.
    relevance: Fills Saudi-specific legal evaluation gap; confirms ArabicMMLU law
      subset size but does not address multi-jurisdiction legal coverage (Egypt, UAE,
      Morocco, Jordan, Lebanon, Palestine, Kuwait). Not a substitute for jurisdiction-specific
      legal tutoring validation.
    source: ArabLegalEval arXiv:2408.07983 — [WEB-3]
  - name: MizanQA
    year: 2025
    description: Arabic benchmark specifically for Moroccan law. Identified in the
      2025 Arabic LLM benchmark survey as a regional-specific resource.
    relevance: Partially fills the Moroccan legal content gap not covered by ArabicMMLU's
      thin Morocco representation. Does not address French-medium Moroccan university
      content.
    source: Arabic LLM benchmark survey arXiv:2510.13430 — [WEB-4]
  - name: ALARB (Arabic Legal Argument Reasoning Benchmark)
    year: 2025
    description: Arabic legal argument reasoning benchmark from a single country's
      commercial law domain. Focuses on verdict generation and legal reasoning tasks
      beyond MCQ.
    relevance: Confirms that Arabic legal NLP evaluation is evolving toward open-ended
      reasoning, but remains single-jurisdiction. Highlights that ArabicMMLU's flat
      MCQ schema is insufficient for legal reasoning evaluation in the deployment
      context.
    source: ALARB arXiv:2510.00694 — [WEB-13]
  - name: Arabic LLM Benchmark Survey (Alzubaidi et al., 2025)
    year: 2025
    description: 'First systematic review of 40+ Arabic LLM evaluation benchmarks
      across NLP tasks, knowledge domains, cultural understanding, and specialized
      capabilities. Identifies critical geographic gaps: North Africa and Levant (excluding
      Jordan) remain underrepresented; multiple Saudi/Gulf-specific benchmarks exist.'
    relevance: Confirms that benchmark geographic bias toward Saudi Arabia and Gulf
      states is a structural feature of the Arabic NLP ecosystem, not just an ArabicMMLU-specific
      limitation. Kuwait remains the most underrepresented of the eight deployment
      countries across all known benchmarks.
    source: Arabic LLM benchmark survey arXiv:2510.13430 — [WEB-4]
  arabicmmlu_country_ranking_clarification:
    finding: The ArabicMMLU paper's Figure 1 shows Jordan, Egypt, and Palestine as
      the top three contributor countries by question count — not Jordan, Egypt, and
      Lebanon as might be inferred from the workforce composition (which lists no
      Palestinian workers). This means Palestine has more questions than any of the
      workforce-documented countries except Jordan and Egypt, but all Palestinian
      questions were verified without Palestinian annotators.
    scoring_implication: This partially upgrades Palestine's Input Content coverage
      estimate (more questions present than initially expected) but simultaneously
      raises Output Content concerns (Palestinian ground truth labels validated without
      Palestinian curriculum expertise).
    source: ArabicMMLU arXiv:2402.12840 — [WEB-1]
  model_performance_country_stratification:
    finding: ArabicMMLU's own analysis shows BLOOMZ performs worse on UAE- and Morocco-sourced
      questions compared to other countries, and Jais performs best overall except
      on Morocco-sourced questions. This empirically confirms that current Arabic
      LLMs have weaker knowledge coverage for Morocco and UAE relative to Jordan and
      Egypt.
    scoring_implication: For the deployment's Morocco and UAE cohorts, current model
      performance on ArabicMMLU-calibrated tasks is expected to be lower than for
      Jordanian or Egyptian students even at the same difficulty level — a deployment
      risk beyond benchmark coverage gaps.
    source: ArabicMMLU arXiv:2402.12840 — [WEB-1]
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/html/2402.12840v1 |
| WEB-2 | https://arxiv.org/abs/2501.00559 |
| WEB-3 | https://arxiv.org/abs/2408.07983 |
| WEB-4 | https://arxiv.org/abs/2510.13430 |
| WEB-5 | https://www.nyulawglobal.org/globalex/egypt.html |
| WEB-6 | https://www.themoonlight.io/en/review/arabicmmlu-assessing-massive-multitask-language-understanding-in-arabic |
| WEB-7 | https://www.itu.int/itu-d/reports/statistics/2023/10/10/ff23-internet-use/ |
| WEB-8 | https://statisticsoftheworld.com/ranking/internet-users |
| WEB-9 | https://datahub.itu.int/ |
| WEB-10 | https://www.arabbarometer.org/2020/09/the-mena-digital-divide/ |
| WEB-11 | https://www.itu.int/dms_pub/itu-d/opb/ind/D-IND-SDDT_ARB-2025-PDF-E.pdf |
| WEB-12 | https://huggingface.co/datasets/MBZUAI/ArabicMMLU |
| WEB-13 | https://arxiv.org/html/2510.00694 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Your deployment spans eight countries with distinct national curricula — for example, Morocco follows a French-influenced baccalaureate system, Egypt has its own Thanawiyya Amma content, and Gulf states have their own civic and religious education frameworks. Does your tutoring system need to align with each country's specific national curriculum, or does it serve a pan-Arab 'common core'? Are there subject areas — such as Islamic studies, national history, or civics — where a Moroccan student's expected answers would differ meaningfully from a Jordanian or Emirati student's?
A1: The system must align with each country's specific national curriculum. For factual questions a single correct answer is expected regardless of country. Islamic studies presents a minor edge case due to different madhabs (schools of jurisprudence) across countries, but this level of specificity is not anticipated at the school level. All eight target countries are majority Sunni, so Shia-specific rulings (relevant in Iraq or Yemen) are not a concern here.

Q2 [IC]: For university-level subjects like law, political science, and economics, the 'correct' answer can depend heavily on which legal tradition or regulatory framework is in scope. Would your system need to tailor its answers to a student's specific country's legal or economic system, or is a general Arabic-world framing acceptable?
A2: The system must tailor legal answers to each country's specific legal system (e.g., Egyptian civil code vs. UAE or Moroccan law). Country-specific tailoring is required for law; the user did not specify the same requirement for economics or political science, implying a more general framing may be acceptable there.

Q3 [OO]: Should correct answers match the exact phrasing or reasoning style of a specific national exam's marking scheme, or is any accurate explanation acceptable? Would a student lose marks if the system's reasoning diverges from the expected answer structure?
A3: For open-ended school questions, divergence from the national marking scheme could disadvantage students who rely on rote Q&A formats (as is common in Egyptian schooling). However, for multiple-choice questions — which is the format ArabicMMLU uses — explanations are not graded, so any correct explanation adequately supports the student's understanding without exam risk.

Q4 [IC]: Would Moroccan students need responses accommodating French-medium content or Darija code-switching, or is Modern Standard Arabic sufficient?
A4: MSA is the formal medium of instruction across all eight countries and is sufficient for school settings. Darija code-switching is informal and out of scope. French may need to be accommodated for subjects taught in French at Moroccan universities (e.g., sciences, certain professional programs).

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark covers eight countries but Palestine is absent from its documented source countries, and university-level subjects (law, CS, management, accounting) may have thin or uneven coverage across all eight distinct national curricula the deployment requires. |
| IC | HIGH | Country-specific legal systems, national history content, and civics vary substantially across the eight countries; individual questions calibrated to one national curriculum (e.g., Egyptian or Jordanian) may carry incorrect or inapplicable ground truth for students in Kuwait, Morocco, or Lebanon. |
| IF | MODERATE | Deployment is text-only and MSA matches the benchmark's language; however, Moroccan students may encounter French-medium university content that falls entirely outside the benchmark's scope, creating a partial modality/language gap. |
| OO | MODERATE | The MCQ output format is shared between benchmark and deployment, which reduces scoring misalignment risk; however, the scoring taxonomy does not capture country-differentiated correct answers (e.g., legal questions with different correct answers per jurisdiction). |
| OC | HIGH | Ground-truth labels sourced from national exams of a subset of countries (Jordan, Egypt, UAE, Lebanon, KSA) may not represent correct answers for Kuwait or Palestine curricula; annotator and source-exam coverage is uneven across the eight deployment targets. |
| OF | LOWER | Both benchmark and deployment use MCQ / label output; the user confirmed that explanation format is not exam-critical for MCQ contexts, so output form mismatch is minimal. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** MBZUAI/ArabicMMLU
**Analysis date:** 2025-01-30
**Examples reviewed:** ~185 examples across 40 subject-level configurations
**Columns shown:** ID, Source, Country, Group, Subject, Level, Question, Context, Answer Key, Option 1–5, is_few_shot
**Columns skipped (media):** None (all text)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | ArabicMMLU | Civics (HS), ID 14501 | A | "من مظاهر التغير التي طرأت على طبيعة المجتمع الاردني الحديث" | "What are the manifestations of change in modern Jordanian society?" — country-specific Jordanian civics | IC |
| D2 | ArabicMMLU | Civics (MS), ID 14291 | C | "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952 وقد عرفت باسم الحكومة:" | "The first coalition government in Jordan in 1952 was known as the ___ government" — Jordanian political history | IC |
| D3 | ArabicMMLU | Civics (MS), ID 14255 | D | "المجلس صاحب الولآية العامة على شؤون الدولة كافة هو ب" with answer "مجلس الوزارء" | "The council with general sovereignty over all state affairs is the Council of Ministers" — specifically Jordanian constitutional structure | OC |
| D4 | ArabicMMLU | History (HS), ID 2827 | A | "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة" | "Rights under the [Jordanian] Kingdom's constitution" — explicitly references the Jordanian Hashemite Kingdom | IC, OC |
| D5 | ArabicMMLU | History (HS), ID 2819 | D | "صدر دستور عام 1952 في عهد جلالة الملك" with options referring to Jordanian kings | "The 1952 constitution was issued during the reign of King [Talal bin Abdullah]" — Jordanian royal history | IC |
| D6 | ArabicMMLU | Economics (HS), ID 11412 | C | "ارسال الشكوى عن طريق الموقع الالكتروني للبنك المركزي وهو: www.cbj.gov.jo" | "Complaints to the Central Bank [of Jordan] via www.cbj.gov.jo" — explicitly references Jordan's central bank | IC |
| D7 | ArabicMMLU | Economics (HS), ID 11561 | B | "نسبة الأردنيين الذين لا يستطيعون الوصول إلى الخدمات المالية الرسمية: 0.67" | "67% of Jordanians cannot access formal financial services" — Jordan-specific statistic as universal economic fact | IC, OC |
| D8 | ArabicMMLU | Law (Prof), ID 4881 | B | "لا يقبل استئناف الأحكام التمهميدية أو الصادرة في نزاع عارض أو دفوع إلا بعد صدور الحكم في جوهر الدعوى" | Moroccan procedural law — appeals rules under Moroccan Code of Civil Procedure | IC, OC |
| D9 | ArabicMMLU | Law (Prof), ID 4652 | C | "يمكن تخويل صفة ضابط الشرطة القضائية للدركيين...بقرار من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" | Moroccan judicial police powers — references "الدرك الملكي" (Royal Gendarmerie of Morocco) | IC, OO |
| D10 | ArabicMMLU | Law (Prof), ID 4843 | C | "إذا تنازل الطرف المدني قبل صدور الحكم: جميع الأجوبة صحيحة" | Moroccan civil party withdrawal in criminal proceedings | IC, OC |
| D11 | ArabicMMLU | Political Science (Univ), ID 6960 | C | "احداث متتابعة قد تكون تعاونیة أو صراعیة ھى: التفاعلات" | "Sequential events, cooperative or conflictual, are called: interactions" — general IR concept | IC |
| D12 | ArabicMMLU | Political Science (Univ), ID 7131 | A | "ﺗﻌﺗﺑر اﻟﺛورة اﻟﻔرﻧﺳﯾﺔ ﻋﺎم 1789 أﺑرز ﻣﺛﺎل ﻟﻠﺛورات اﻟﻛﺑرى اﻟﺗﻲ ﻋززت ﺣﻘوق اﻹﻧﺳﺎن: ﺻﺢ" | "The French Revolution is the foremost example of revolutions that strengthened human rights: True" — all from Egyptian sources (aun.edu.eg) | IC |
| D13 | ArabicMMLU | Accounting (Univ), ID 7245 | A | "يفترض أسموب المراجعة حول الحاسب أنو إذا كانت المدخالت سميمة...فإن عممية التشغيل تكون سميمة بالتبعية" | Computer auditing concept — general accounting principle, from Egyptian source | IC |
| D14 | ArabicMMLU | Management (Univ), ID 6175 | B | "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة...تذتير إلى" | Severely OCR-distorted text about authority distribution in organizations, from Egyptian source | IF |
| D15 | ArabicMMLU | Management (Univ), ID 6174 | C | "ال يعد مثاالً على الخطط دائسة اإلستخدام... الرخرحم ت... الح ً ت." | Severely OCR-corrupted management question with unreadable answer options | IF |
| D16 | ArabicMMLU | Computer Science (Univ), ID 7280 | C | "الكمبيوتر الدقيق هو عبارة عن: جهاز الكمبيوتر المكتبي" | "A microcomputer is a desktop computer" — from KSA source (faculty.ksu.edu.sa) | IC |
| D17 | ArabicMMLU | Islamic Studies (HS), ID 14064 | E | "للتفكير آثار إيجابية عدة: جميع ما ذكر" — Country: Jordan | 5-option Islamic studies question about positive effects of thinking | IO, OO |
| D18 | ArabicMMLU | Islamic Studies (General), ID 165 | D | "قال الرسول صلى الله عليه وسلام: (لا يدخل الجنة قتات)، فمن هو القتات؟ النمام" | "The Prophet said: the 'qattat' shall not enter paradise — who is qattat? A gossip/slanderer" — no country field, generic Islamic trivia source | IC |
| D19 | ArabicMMLU | Arabic Language (Grammar), ID 12626 | A | "In the following Quranic verse, what is the correct parsing of the word ــكَ" | English-language question stem in an Arabic grammar dataset | IF |
| D20 | ArabicMMLU | Social Science (PS), ID 5489 | D | "تشمل الخدمات الطبية الملكية الحكومية العديد من المؤسسات...منها: مستشفى المدينة الطبية" | "Royal Medical Services include: Medical City Hospital" — specifically Jordanian Royal Medical Services | IC |
| D21 | ArabicMMLU | Social Science (PS), ID 5481 | D | "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" | "King Talal bin Hussein's reign ended for health reasons in 1952 — one year" — Jordanian royal history in primary school | IC |
| D22 | ArabicMMLU | Geography (MS), ID 8055 | A | "توجد كنيسة سيدة الجبل في ……. عنجرة" | "Lady of the Mountain Church is in Anjara [Jordan]" — Jordanian religious geography | IC |
| D23 | ArabicMMLU | Computer Science (PS), ID 7354 | A | "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" | "The binary number system is used by computers" — Palestine-sourced primary CS | IC |
| D24 | ArabicMMLU | Biology (HS), ID 9842 | D | "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" | Calvin cycle question — Palestine-sourced biology; universal factual content | IC |
| D25 | ArabicMMLU | Civics (HS), ID 14529 | C | "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨: تحرر البلاد من قيود فك الانتداب" | "The main goal of the 1928 Jordanian-British treaty was liberation from Mandate restrictions" — Jordanian national history | IC |
| D26 | ArabicMMLU | All (Islamic Studies), ID 165–54 | null | All 5 examples: Country = null, Source = folderat.com, Subject = Islamic Studies | Islamic Studies "All" config examples have no country metadata — source appears to be generic Arabic quiz site | IO, OC |
| D27 | ArabicMMLU | Arabic Language (General), ID 11849–11736 | null | All 5 examples: Country = null, Source = madinaharabic.com | Arabic Language General has no country metadata — sourced from online Arabic language learning site | IO |
| D28 | ArabicMMLU | Economics (Univ), ID 11228 | B | "إذا كان حجم الاستثمار المطلوب ١٠٠ر٠٠٠ جنيه...معدل العائد على الأموال المستثمرة هو: % ١٥" | Egyptian currency (جنيه = Egyptian pound) in university economics — Egypt-specific monetary context | IC, OC |
| D29 | ArabicMMLU | Political Science (Univ), ID 7008 | D | "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ" | Severely OCR-distorted Arabic text about conditions for an Islamic ruler — from Egyptian source | IF |
| D30 | ArabicMMLU | Geography (HS), ID 8529 | D | "محمية طبيعية في الأردن تشرف عليها إدارة مشتركة...وادي رم" | "Wadi Rum is a Jordanian nature reserve under joint management" — Jordan-specific geography fact | IC |
| D31 | ArabicMMLU | History (HS), ID 3049 | D | "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" | King Abdullah I's positions on Zionism — highly sensitive political content, Jordanian framing of Palestinian history | IC, OC |
| D32 | ArabicMMLU | Social Science (MS), ID 5261 | D | "أنعم الله على بلادنا العربية بثروات كبيرة من النفط والغاز الطبيعي...يرجع السبب في ذلك إلى: توافره بكميات قليلة" | "Gas is available in limited quantities" — possibly incorrect answer key for general Arab world social science | OC |
| D33 | ArabicMMLU | Computer Science (MS), ID 7333–7343 | all Jordan | All 5 examples: Country = Jordan, Windows OS questions | Middle school CS focuses on Windows OS user interface — likely dated Jordanian curriculum content | IC |
| D34 | ArabicMMLU | Law (Prof), all 5 examples | Morocco | All 5 Law (Professional) examples: Country = Morocco, from single Google Drive PDF | All sampled law questions are exclusively from Morocco — single-source PDF | IC, OC |
| D35 | ArabicMMLU | Driving Test, ID 687, 695 | UAE | "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر" | UAE driving rule (50m warning triangle placement) — country-specific traffic regulation | IO, OO |
| D36 | ArabicMMLU | General Knowledge (MS), ID 4556 | A | "الشامل الأكاديمي يمثل ……. الأدبي" | "The 'comprehensive academic' [track] is the humanities track" — Jordanian secondary school track system | IC |
| D37 | ArabicMMLU | Islamic Studies (Primary), ID 12853 | D | "من آداب تلاوة القرآن الكريم: جميع ما ذكر" — Country: Jordan | Generic Islamic etiquette of Quran recitation — no madhab specificity indicated | IC |
| D38 | ArabicMMLU | Islamic Studies (HS), ID 14042 | D | "فوائد إيراد الأمثال في القرآن الكريم: جميع ما ذكر" — Country: Jordan | Islamic studies question about examples in Quran — Jordanian curriculum framing | IC |
| D39 | ArabicMMLU | Accounting (Univ), ID 7245 | A | Source: http://www.aun.edu.eg/commerce/... | All 5 accounting examples from Assiut University (Egypt) — single Egyptian university source | IC, OC |
| D40 | ArabicMMLU | Economics (University), all 5 | Egypt | Source: http://www.aun.edu.eg — all 5 from same Assiut University Egypt URL | University economics exclusively from Egyptian university source | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Authentic country-sourced exam content in target languages and format
- **Dimension(s):** IC, IF
- **Observation:** The sampled questions demonstrate genuine national exam provenance — questions are clearly drawn from real school assessments, not translations. Arabic language, grammar, STEM, and Islamic studies questions are well-formed MSA suitable for the school tutoring context. The format is entirely MCQ with 2–5 options, directly matching the deployment's primary format.
- **Deployment relevance:** For the deployment's core use case (supporting students with MCQ exam preparation), the native exam origin means content register, vocabulary difficulty, and question structure are authentic to what students encounter in real exams.
- **Datapoint citations:**
  - [D24] Example Biology (HS), ID 9842 (Palestine, test): "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" — Authentic Palestinian high school biology question in proper MSA with scientific terminology.
  - [D37] Example Islamic Studies (PS), ID 12853 (Jordan, test): "من آداب تلاوة القرآن الكريم: جميع ما ذكر" — Primary school Islamic studies question in standard school format.
  - [D25] Example Civics (HS), ID 14529 (Jordan, test): "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨: تحرر البلاد من قيود فك الانتداب" — Tawjihi-style question format.

#### Strength 2: Broad subject taxonomy covering all six deployment university subjects
- **Dimension(s):** IO
- **Observation:** The dataset's 40 configurations directly observed include Accounting (University), Computer Science (University), Economics (University), Management (University), Political Science (University), and Law (Professional) — all six university-level subjects the deployment targets. This is confirmed through direct data inspection, not just paper claims.
- **Deployment relevance:** The deployment specifically requires coverage of law, management, economics, CS, political science, and accounting for university students. All are present as distinct, queryable configurations.
- **Datapoint citations:**
  - [D13] Example Accounting (Univ), ID 7245 (Egypt, test): "يفترض أسموب المراجعة حول الحاسب أنو إذا كانت المدخالت سميمة...فإن عممية التشغيل تكون سميمة بالتبعية" — University accounting question about computer auditing methodology.
  - [D16] Example CS (Univ), ID 7280 (KSA, test): "الكمبيوتر الدقيق هو عبارة عن: جهاز الكمبيوتر المكتبي" — University CS definitional question from Saudi source.
  - [D11] Example Political Science (Univ), ID 6960 (Egypt, test): "احداث متتابعة قد تكون تعاونیة أو صراعیة ھى: التفاعلات" — University-level international relations concept.

#### Strength 3: Moroccan law content is present and confirmed in the data
- **Dimension(s):** IC, IO
- **Observation:** The Law (Professional) configuration — the only university/professional law split — contains exclusively Moroccan questions in the sample (all 5 sampled questions from Morocco, sourced from a single Google Drive PDF of Moroccan procedural law). These cover Moroccan appellate procedures, civil party rules, and judicial police powers under Moroccan law, referencing Morocco-specific institutions (الدرك الملكي — Royal Gendarmerie).
- **Deployment relevance:** The web search found this Moroccan law content was used as an illustrative example in the paper, and the data confirms it is genuinely present. For the deployment's Moroccan law students, some Moroccan-jurisdiction legal content exists.
- **Datapoint citations:**
  - [D8] Example Law (Prof), ID 4881 (Morocco, test): "لا يقبل استئناف الأحكام التمهميدية...إلا بعد صدور الحكم في جوهر الدعوى" — Moroccan Code of Civil Procedure appeal rules.
  - [D9] Example Law (Prof), ID 4652 (Morocco, test): "يمكن تخويل صفة ضابط الشرطة القضائية للدركيين...من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" — Moroccan judicial police appointment procedure referencing Morocco-specific institutions.
  - [D10] Example Law (Prof), ID 4843 (Morocco, test): "إذا تنازل الطرف المدني قبل صدور الحكم: جميع الأجوبة صحيحة" — Moroccan criminal procedure rule.

#### Strength 4: Palestine is substantively present across STEM and language subjects
- **Dimension(s):** IC, IO
- **Observation:** Palestinian-sourced questions appear across multiple configurations: Biology (HS) — 4 of 5 examples from Palestine; Computer Science (Primary) — all 5 examples from Palestine; Math (Primary) — multiple Palestine examples; Arabic Language (Primary) — one Palestine example; Geography (Middle) — 2 Palestine examples; Physics (HS) — 2 Palestine examples. This confirms Palestine is a real contributor, not just a nominal listing.
- **Deployment relevance:** Palestine is a high-priority deployment target. The data shows that for STEM and basic academic subjects, Palestinian curriculum content is genuinely represented.
- **Datapoint citations:**
  - [D23] Example CS (PS), ID 7354 (Palestine, test): "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" — Palestinian primary school CS.
  - [D24] Example Biology (HS), ID 9842 (Palestine, test): "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" — Palestinian HS biology.

#### Strength 5: STEM content is genuinely curriculum-neutral and reliable across countries
- **Dimension(s):** IC, OC
- **Observation:** Math (Primary), Biology (HS), Physics (HS), Natural Science, and CS questions in the data contain factual content that does not vary by national curriculum. The answers are objectively verifiable regardless of student nationality, making ground-truth labels reliable across all eight deployment countries for these subjects.
- **Deployment relevance:** For the large portion of the deployment serving STEM students, the benchmark's content validity is high. Country-specific annotation bias (the major OC concern) does not affect factual STEM questions.
- **Datapoint citations:**
  - [D24] Example Biology (HS), ID 9842 (Palestine, test): "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" — Universal biology fact.
  - [D1] through standard math examples: "ما ناتج جمع 2+ 6 = 8" — universal arithmetic.

#### Strength 6: Multi-level education coverage confirmed in data
- **Dimension(s):** IO
- **Observation:** The data directly confirms questions at Primary, Middle, High School, and University (Univ/Prof) levels across multiple subjects. The Level field is consistently populated for school-level questions, and university-level configurations (Accounting, Economics, Management, CS, Political Science) are separately queryable.
- **Deployment relevance:** The deployment targets all four educational tiers. The benchmark's level-specific configurations allow the tutoring system to select difficulty-appropriate questions.
- **Datapoint citations:**
  - [D13] Example Accounting (Univ), Level=Univ — university-level confirmed.
  - [D21] Example Social Science (PS), ID 5481, Level=Primary — primary level confirmed with Jordanian political content.
  - [D5] Example History (HS), ID 2819, Level=High — high school level confirmed.

#### Strength 7: Driving Test subject provides country-specific coverage for UAE, Egypt, and Lebanon
- **Dimension(s):** IO, IC
- **Observation:** The Driving Test configuration contains questions from UAE, Egypt, and Lebanon with country-specific traffic regulations. The UAE examples reference specific UAE road authority rules (50m warning triangle placement), and Lebanon examples reference Lebanese traffic law.
- **Deployment relevance:** While not a core tutoring subject, this demonstrates the benchmark's actual country-specific rule calibration for at least some subjects beyond academic content.
- **Datapoint citations:**
  - [D35] Example Driving Test, ID 687 (UAE, test): "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر" — UAE-specific driving rule.
  - [D35] Example Driving Test, ID 1025 (Lebanon, test): "يُحَظَّر على سائق المركبة: يجري مناورة عكس الإتجاه (Demi Tour) وسط الطريق" — Lebanese traffic law (note French loan word "Demi Tour").

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Civics and Social Studies are overwhelmingly Jordanian-centric — not pan-Arab
- **Dimension(s):** IC, OC
- **Severity:** CRITICAL
- **Observation:** In the sampled civics, history, social science, geography, and general knowledge data, the vast majority of country-specific content reflects exclusively Jordanian national curriculum content — Jordanian constitutional structure, Jordanian royal history, Jordanian medical institutions, Jordanian party laws, and Jordanian geographic landmarks. This is not a minor imbalance: the content is not presented as Jordanian-specific but as general curriculum knowledge. A Moroccan, UAE, or Kuwaiti student encountering these questions would be tested on Jordanian national content.
- **Deployment relevance:** The deployment requires curriculum-aligned answers for each of the eight countries. Questions about "الملك طلال بن الحسين," "مجلس التعاون الأردني," and Jordan's 1952 constitution are irrelevant or actively misleading for students from Morocco, UAE, Kuwait, or Palestine whose civics exams test entirely different national content. For civics subjects specifically, the benchmark effectively functions as a Jordanian civics test.
- **Datapoint citations:**
  - [D1] Example Civics (HS), ID 14501 (Jordan): "من مظاهر التغير التي طرأت على طبيعة المجتمع الاردني الحديث" — Explicitly asks about Jordanian society; not applicable to students from other eight countries.
  - [D2] Example Civics (MS), ID 14291 (Jordan): "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952 وقد عرفت باسم الحكومة:" — Jordanian political history fact irrelevant to Moroccan or Emirati civics.
  - [D3] Example Civics (MS), ID 14255 (Jordan): "المجلس صاحب الولآية العامة على شؤون الدولة كافة هو ب: مجلس الوزارء" — Framed as a general question but answer is grounded in Jordanian constitutional law.
  - [D21] Example Social Science (PS), ID 5481 (Jordan): "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" — Jordanian royal history taught as primary school social studies.
  - [D36] Example General Knowledge (MS), ID 4556 (Jordan): "الشامل الأكاديمي يمثل ……. الأدبي" — Jordanian secondary school track labeling system specific to Jordan's education structure.

#### CRITICAL Concern 2: University-level content is dominated by a single Egyptian institution
- **Dimension(s):** IC, OC
- **Severity:** CRITICAL
- **Observation:** All 5 sampled Accounting (University) examples, all 5 Economics (University) examples, all 5 Management (University) examples, and all 5 Political Science (University) examples originate from a single source: Assiut University's Faculty of Commerce (aun.edu.eg). The Management examples notably include severely OCR-corrupted text rendering some questions and answer options unreadable. The Computer Science (University) examples all come from a single KSA source (faculty.ksu.edu.sa).
- **Deployment relevance:** The deployment requires university-level content for students in all eight countries. If university-level accounting, management, economics, and political science are sourced almost exclusively from one Egyptian university's question bank, the benchmark is measuring alignment with that specific institution's curriculum framing, not pan-Arab or per-country university education. For university students in Morocco, UAE, Kuwait, Lebanon, or Jordan, these Egyptian university questions may reflect different course structures, textbook traditions, or exam formats.
- **Datapoint citations:**
  - [D39] Examples Accounting (Univ), IDs 7245, 7196, 7215, 7186, 7185 — all Source: http://www.aun.edu.eg/commerce/... — single Egyptian university.
  - [D40] Examples Economics (Univ), all 5 — all Source: http://www.aun.edu.eg — same Egyptian university.
  - [D14] Example Management (Univ), ID 6175 (Egypt): "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة فتى السشمستة تذتير إلى" — OCR-corrupted to the point of being unreadable; correct answer cannot be verified from the text alone.
  - [D15] Example Management (Univ), ID 6174 (Egypt): "ال يعد مثاالً على الخطط دائسة اإلستخدام... الرخرحم ت... الح ً ت." — Answer options are corrupted Arabic OCR artifacts.

#### CRITICAL Concern 3: Law (Professional) is exclusively Moroccan in the observed data — no evidence of multi-jurisdiction coverage
- **Dimension(s):** IC, OO, OC
- **Severity:** CRITICAL
- **Observation:** All 5 sampled Law (Professional) questions come from a single Moroccan source (a single Google Drive PDF of Moroccan procedural law). While this confirms Moroccan law is present, the deployment requires country-specific legal tutoring for Egypt (Egyptian civil code), UAE (federal civil law with Sharia overlay), Jordan (civil law), KSA (Sharia-based), Lebanon, Kuwait, and Palestine. The observed data provides no evidence that other legal jurisdictions are covered. The benchmark's flat single-correct-answer schema cannot encode that the answer to an appellate procedure question differs between Morocco and Egypt.
- **Deployment relevance:** The deployment user explicitly stated that "the system must tailor legal answers to each country's specific legal system." A benchmark where all sampled law questions are Moroccan procedural law cannot validate a tutoring system's legal correctness for Egyptian, UAE, Jordanian, or Saudi students. The jurisdictional ground truth cannot be determined from the flat label schema.
- **Datapoint citations:**
  - [D8] Example Law (Prof), ID 4881 (Morocco): "لا يقبل استئناف الأحكام التمهميدية...إلا بعد صدور الحكم في جوهر الدعوى" — Moroccan appellate rule; rule may differ under Egyptian or UAE procedural law.
  - [D9] Example Law (Prof), ID 4652 (Morocco): "يمكن تخويل صفة ضابط الشرطة القضائية للدركيين...من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" — References "الدرك الملكي" (Morocco's Royal Gendarmerie) — institution does not exist in other deployment countries.
  - [D34] All 5 Law examples — Country = Morocco, single source URL — confirms single-jurisdiction observation.

---

#### MAJOR

#### MAJOR Concern 4: Significant OCR corruption in university-level management and political science questions
- **Dimension(s):** IF, OC
- **Severity:** MAJOR
- **Observation:** Multiple university-level management and political science questions contain severely corrupted Arabic text that appears to result from poor OCR of PDF scan material. Answer options in some management questions are entirely unreadable (e.g., "الرخرحم ت," "الح ً ت," "اليؾام"). Some political science questions have broken Arabic words mid-sentence. This affects ground-truth label reliability — if the question text is corrupted, it is unclear whether annotators could correctly verify the answer.
- **Deployment relevance:** The deployment targets university students including management and political science majors. Questions with corrupted text cannot reliably serve as evaluation items and would confuse or mislead students in a tutoring context.
- **Datapoint citations:**
  - [D15] Example Management (Univ), ID 6174 (Egypt): "ال يعد مثاالً على الخطط دائسة اإلستخدام... الرخرحم ت... الح ً ت. ...اليؾام" — Multiple answer options are OCR artifacts, not valid Arabic words.
  - [D14] Example Management (Univ), ID 6175 (Egypt): "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة فتى السشمستة" — Question text has inserted random Arabic letters/diacritics breaking word boundaries.
  - [D29] Example Political Science (Univ), ID 7008 (Egypt): "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ" — Letters are doubled/tripled throughout, rendering text difficult to parse.

#### MAJOR Concern 5: Islamic Studies has no country metadata in the "General" and "All" configurations, and no madhab labeling anywhere
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** The five sampled Islamic Studies (General/All config) examples all have Country = null and are sourced from a generic Arabic quiz website (folderat.com). These questions cover Hadith-based ethics and Prophetic biography — content that is broadly consistent across Sunni traditions. However, no Islamic Studies question observed across any configuration has any madhab labeling, and the Islamic Studies (HS) questions are all Jordanian-curriculum. For Morocco (Maliki), the specific fiqh rulings and jurisprudential framing that appear in school Islamic studies curricula differ from Jordanian (mixed Shafi'i/unspecified) or Saudi (Hanbali) tradition.
- **Deployment relevance:** While the deployment user assessed madhab-level divergence as unlikely at school level, the actual data shows no mechanism for madhab identification or filtering. If a Moroccan student encounters a Hanbali-framing fiqh question from the Jordanian curriculum, the benchmark provides no flag for this. For the tutoring system to confidently support Moroccan Islamic studies students, this is a latent risk.
- **Datapoint citations:**
  - [D26] Examples Islamic Studies (All), IDs 165, 385, 46, 157, 54 — Country = null, Source = folderat.com — no curriculum attribution; generic Islamic knowledge quiz.
  - [D38] Example Islamic Studies (HS), ID 14042 (Jordan): "فوائد إيراد الأمثال في القرآن الكريم: جميع ما ذكر" — Jordanian high school framing of Quranic analysis; Saudi or Moroccan curricula may frame this differently.
  - [D37] Example Islamic Studies (PS), ID 12853 (Jordan): "من آداب تلاوة القرآن الكريم: جميع ما ذكر" — Practices of Quran recitation etiquette; factually consistent but Jordanian curriculum source only.

#### MAJOR Concern 6: Jordan-specific national content embedded as school-level "social science" and "history" without country-specific flagging
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** Primary and middle school Social Science questions include Jordanian-specific institutional facts (Jordan's Royal Medical Services, King Talal's reign) presented as factual questions without explicit country labels in question text. History questions at all levels heavily feature Jordanian royal history and Jordanian constitutional content. A benchmark user evaluating model performance on "History (Middle School)" or "Social Science (Primary School)" would receive a metric reflecting Jordanian curriculum knowledge, not pan-Arab or country-neutral historical knowledge.
- **Deployment relevance:** For Moroccan, Emirati, Saudi, or Kuwaiti primary and middle school students, the tutoring system evaluated against ArabicMMLU's history/social science subset would be tested on Jordanian-specific knowledge that is irrelevant to their national curriculum. This creates construct-irrelevant variance that could make a model appear stronger or weaker than it truly is for non-Jordanian curricula.
- **Datapoint citations:**
  - [D21] Example Social Science (PS), ID 5481 (Jordan): "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" — Primary school Jordan-specific royal history.
  - [D20] Example Social Science (PS), ID 5489 (Jordan): "تشمل الخدمات الطبية الملكية الحكومية العديد من المؤسسات المتخصصة...مستشفى المدينة الطبية" — Jordan-specific institution.
  - [D4] Example History (HS), ID 2827 (Jordan): "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة" — Explicitly the Jordanian (Hashemite) Kingdom's constitution.
  - [D31] Example History (HS), ID 3049 (Jordan): "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" — Politically sensitive question about King Abdullah I's positions; framing reflects Jordanian historical narrative which may differ from Palestinian national narrative.

#### MAJOR Concern 7: Economics (HS) contains Jordan-specific financial statistics and institutions
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** High school economics questions reference Jordan's Central Bank (CBJ) website and Jordan-specific financial inclusion statistics (67% of Jordanians without access to formal financial services) as factual questions without flagging them as Jordanian-specific. These figures are not cross-nationally applicable.
- **Deployment relevance:** For a UAE or Saudi Arabian high school economics student, a question asking for the Central Bank of Jordan's website address or Jordan-specific financial statistics would be irrelevant and potentially misleading. The benchmark does not distinguish between general economics principles and jurisdiction-specific institutional facts.
- **Datapoint citations:**
  - [D6] Example Economics (HS), ID 11412 (Jordan): "ارسال الشكوى عن طريق الموقع الالكتروني للبنك المركزي وهو: www.cbj.gov.jo" — Jordan-specific institutional URL as exam fact.
  - [D7] Example Economics (HS), ID 11561 (Jordan): "نسبة الأردنيين الذين لا يستطيعون الوصول إلى الخدمات المالية الرسمية: 0.67" — Jordan-specific statistic presented as curriculum fact.

#### MAJOR Concern 8: Egyptian currency denomination used as default in university economics
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** University Economics examples from Assiut University use Egyptian pounds (جنيه) in quantitative finance problems. For students in UAE (using dirhams), Kuwait (dinars), Jordan (dinars), or Morocco (dirhams), the currency denomination embeds Egyptian economic context as a universal fact.
- **Deployment relevance:** For the deployment's university economics students in non-Egyptian countries, correct application of financial formulas requires recognizing this currency context, and any tutor response would need to translate this into local context. The benchmark's ground truth treats Egyptian pound calculations as universally correct.
- **Datapoint citations:**
  - [D28] Example Economics (Univ), ID 11228 (Egypt): "إذا كان حجم الاستثمار المطلوب ١٠٠ر٠٠٠ جنيه...معدل العائد على الأموال المستثمرة هو: % ١٥" — Egyptian pound (جنيه) used in an ROI calculation presented as a general economics problem.

---

#### MINOR

#### MINOR Concern 9: One Arabic grammar question has an English-language question stem
- **Dimension(s):** IF
- **Severity:** MINOR
- **Observation:** In the Arabic Language (Grammar) configuration, one example (ID 12626) has an English question stem: "In the following Quranic verse, what is the correct parsing of the word ــكَ" — while the answer options are in Arabic. This appears to be a data entry anomaly from the madinaharabic.com source.
- **Deployment relevance:** Minor data quality concern; single example unlikely to materially affect aggregate scores, but suggests the data scraping pipeline did not filter out mixed-language question stems consistently.
- **Datapoint citations:**
  - [D19] Example Arabic Language (Grammar), ID 12626 (null country): "In the following Quranic verse, what is the correct parsing of the word ــكَ" — English stem in an Arabic grammar configuration.

#### MINOR Concern 10: Multiple configurations have null Country and null Level fields
- **Dimension(s):** IO, IC
- **Severity:** MINOR
- **Observation:** The Islamic Studies (General), Islamic Studies (All config), Arabic Language (General), Arabic Language (Grammar), and several other configurations have Country = null and Level = null for all sampled examples. These questions come from generic online quiz platforms (folderat.com, madinaharabic.com) rather than national exam sources, meaning they are not tied to any specific national curriculum or education level.
- **Deployment relevance:** Null-country questions cannot be used for country-specific evaluation. For the deployment's diagnostic use case (evaluating model performance per country and per level), these questions contribute noise to aggregate metrics without providing actionable per-country signal.
- **Datapoint citations:**
  - [D26] Examples Islamic Studies (All), IDs 165, 385, 46, 157, 54 — Country = null, Level = null.
  - [D27] Examples Arabic Language (General), IDs 11849–11736 — Country = null, Level = null, Source = madinaharabic.com.

#### MINOR Concern 11: Social Science (Middle School) may contain a questionable ground-truth label
- **Dimension(s):** OC
- **Severity:** MINOR
- **Observation:** Example ID 5261 from Social Science (Middle School) asks why natural gas is an important energy source and provides the answer "توافره بكميات قليلة" ("available in limited quantities") as correct. This appears to be an odd ground truth — natural gas importance is generally attributed to abundance, not scarcity. This could be an exam error carried over from the source, or a printing artifact. The benchmark's 96% accuracy ceiling acknowledges approximately 4% error rate.
- **Deployment relevance:** For a tutoring system, propagating potentially incorrect factual claims to students would be harmful. This single example is unlikely to be more than a data error within the acknowledged 4% noise floor, but it illustrates that some answer keys may be incorrect.
- **Datapoint citations:**
  - [D32] Example Social Science (MS), ID 5261 (null country): "يرجع السبب في ذلك إلى: توافره بكميات قليلة" — Answer states natural gas is important because it is available in limited quantities, which is contrary to standard economic reasoning.

#### MINOR Concern 12: Middle school Computer Science is Windows OS-centric with potentially dated content
- **Dimension(s):** IC
- **Severity:** MINOR
- **Observation:** The Computer Science (Middle School) sample contains multiple questions about Windows desktop interface operations (background images, right-click menus, icon arrangement, Windows system files). This is curriculum-specific to Jordan's circa 2015–2020 ICT curriculum and may not reflect UAE, Egyptian, or Palestinian CS middle school content, which may focus on different platforms or concepts.
- **Deployment relevance:** For a tutoring system supporting all eight countries' CS curricula, a heavily Windows-GUI-focused CS subset may misrepresent what CS knowledge looks like for students in other countries.
- **Datapoint citations:**
  - [D33] Example CS (MS), ID 7340 (Jordan): "لتخصيص صورة تحل محل الخلفية الافتراضية تنقر زر: خلفية سطح المكتب" — "To change the desktop background, click: Desktop Background" — Windows UI tutorial question.
  - [D33] Example CS (MS), ID 7343 (Jordan): "إذا تم حذف ملف من ملفات النظام Windows هل يؤثر ذلك على عمل النظام: يؤثر" — Windows system files question.

---

### Content Coverage Summary

The 185+ examples reviewed span all 40 subject-level configurations and provide a clear picture of the benchmark's content composition:

**Country distribution in sample:** Jordan is the dominant country across school-level humanities, social science, civics, history, geography, Arabic language, economics, general knowledge, and Islamic studies configurations. Palestine appears substantially in STEM subjects (Biology HS, CS Primary/HS, Physics HS, Math Primary, Geography Middle) and some social science. Egypt dominates all university-level non-CS configurations (Accounting, Economics, Management, Political Science). Morocco appears exclusively in Law (Professional). KSA appears in CS (University). UAE appears in Driving Test. Lebanon appears in Driving Test. Kuwait and several other countries have zero observed examples across the sample.

**Register and difficulty:** Questions are appropriate for their labeled educational level — primary questions are simple and short, high school questions involve more complex reasoning, and university questions involve domain-specific terminology. MSA is consistently used throughout, with appropriate formal register for educational contexts.

**Content types observed:** (1) Factual recall of national curriculum content — heavily Jordanian for school level; (2) definitional/conceptual questions in STEM and social science; (3) procedural/institutional knowledge (legal procedures, constitutional facts); (4) quantitative problems in mathematics and applied economics; (5) Arabic language morphology and grammar analysis.

**Quality issues:** OCR corruption is a material concern in some university-level PDFs, particularly management and political science from Egyptian sources. A small number of questions have null answer options (Option 3/4 = null when only 2-3 options provided) which is expected given the 2–5 option range. Some questions have truncated or incomplete text, likely from the original PDF scraping.

**Geographic representation gap confirmed in data:** No Kuwait or UAE examples observed outside the Driving Test. No Moroccan examples outside Law (Professional) and one or two Arabic language items. The Jordan-Egypt-Palestine dominance documented in the paper is directly observable in the data.

---

### Limitations

1. **Sample size per configuration:** Most configurations were sampled at 5–8 examples out of test splits ranging from 50–500+ questions. Individual configurations (especially smaller ones) may be substantially different from what the sample shows. Country distribution within configurations beyond Jordan/Egypt/Palestine is particularly uncertain.

2. **Kuwait coverage unverifiable:** No Kuwaiti examples appeared in any sampled configuration. This is consistent with the documented concern but cannot be definitively confirmed as zero-coverage from this sample alone — a full dataset scan would be needed.

3. **University-level sample is thin:** With ~6.1% of questions at university level (~889 total), each university subject configuration is small. The 5 examples sampled per university configuration may represent a substantial fraction of the total, making these configurations particularly sensitive to source diversity (or lack thereof).

4. **Law (Professional) is the only law configuration:** The sample cannot determine whether other law content is embedded in other humanities configurations. The Moroccan dominance of Law (Professional) in the sample may not generalize to all 299+ law questions identified by ArabLegalEval.

5. **Islamic studies madhab calibration:** The data does not contain any explicit madhab identifiers, and the question content observed does not clearly differentiate between madhab traditions. Confirming whether any questions are madhab-specific would require expert Islamic jurisprudence review, which is outside the scope of this data analysis.

6. **OCR corruption extent:** The Management (University) and Political Science (University) OCR corruption was observed in the sample but the total proportion of corrupted questions in these configurations cannot be estimated from 5-question samples.

7. **No inspection of few-shot split:** The `is_few_shot` field was observed (value = 0 for all sampled test examples), but the dev split (few-shot examples) was not sampled. Few-shot examples may have different country distributions.

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
  "region": "MENA Multi-Country Arabic Tutoring System — Eight-Country Curriculum Deployment",
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
