I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **Measuring Massive Multitask Language Understanding** is valid for use in **North India Competitive Exam Aspirants (Hindi-Medium)**.

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

- **Name**: mmlu
- **Full Name**: Measuring Massive Multitask Language Understanding
- **Domain**: General LLM evaluation / multitask knowledge and reasoning
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2021

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
MMLU covers 57 subjects across STEM, humanities, social sciences, and a residual "other"
category [Q8, Q16], spanning difficulty levels from elementary through advanced professional
[Q1]. Subject areas include US history, US foreign policy, professional law calibrated against
US bar-exam-style questions, and medicine benchmarked against the USMLE [Q17, Q49].
The humanities cluster includes law, philosophy, history, and related disciplines [Q24],
with philosophy covering Western canonical figures and the ETHICS dataset's normative
scenarios [Q26]. The social science cluster covers economics, sociology, politics, geography,
and psychology [Q28, Q31], while STEM encompasses physics, computer science, and mathematics
[Q32]. Security studies are also included as a more esoteric topic [Q30], reflecting US
foreign-policy concerns.

From an Input Ontology standpoint, this taxonomy represents a near-total mismatch for the
North Indian competitive-exam deployment. MMLU contains no subject track for Indian Polity
& Constitution, Indian History (ancient, medieval, or modern), Indian Geography, Hindi language
proficiency, or Current Affairs relevant to India — the exact domains that constitute the core
syllabus of UPSC and SSC examinations. The history component is documented as covering
"a wide range of time periods and geographical locations" [Q27], but the sampled examples
confirm focus on European and US history [Q130, Q140] with no South Asian content. Table 2
summarises all 57 tasks [Q104], and none maps to the Indian curriculum domains that
competitive-exam candidates require [Q93].

### Input Content
Questions were manually collected by graduate and undergraduate students from freely available
online sources, including GRE and USMLE practice materials, undergraduate courses, and Oxford
University Press publications [Q17]. A supplementary legal dataset of approximately 2,000
Professional Law training examples was drawn from US legal corpora, along with 1.6 million
Harvard Law Library case summaries [Q69, Q71]. Most questions originated from PDFs or websites
where questions and answers appear on separate pages [Q101]. Models are assumed to have
acquired requisite knowledge from vast quantities of diverse Internet text [Q60], which for
Hindi-medium or India-centric topics is far sparser than for English-language Western content.

The individual datapoints confirm this cultural anchoring. Sampled questions test US
Congressional history [Q158], Western philosophical canon (Rawls, Mill, Moore) [Q145, Q146,
Q150], US tax law [Q152], and US bar-exam scenarios [Q153]. No questions in the registry
or documented task list address Indian Polity, Panchayati Raj, North Indian land-revenue
traditions, Indian festivals such as Chhath Puja, or regional administrative structures
(tehsils, mandals). The benchmark's implicit framing — that "extensive world knowledge"
means Western world knowledge [Q2] — means that a North Indian competitive-exam context
requiring both pan-India and regionally grounded knowledge is not represented at the item
level.

### Input Form
MMLU is a text-only, multiple-choice benchmark evaluated exclusively in zero-shot and
few-shot settings [Q7]. GPT-3 prompts are constructed with a standardised English-language
preamble ("The following are multiple choice questions (with answers) about [subject]")
followed by up to five English few-shot demonstration examples [Q44]. UnifiedQA uses a
normalised, lowercased English input format [Q91], and format sensitivity is documented as
a real performance concern [Q90, Q92]. The benchmark was deliberately restricted to
text-only format because existing large-scale NLP models did not incorporate multimodal
information at the time of publication [Q59]. Question length is not strongly correlated
with difficulty [Q94].

This is a HIGH-priority validity failure for the Hindi-medium deployment. The entire
benchmark is in English with no Hindi-language version, no Devanagari script rendering,
and no code-mixed variant. The deployment requires Hindi-dominant interaction with at most
approximately 10% English code-mixing; MMLU's input language distribution is fundamentally
misaligned with this requirement. Any LLM score on MMLU therefore provides no evidence
about the model's capacity to comprehend or process Hindi-medium competitive-exam prompts.

### Output Ontology
The benchmark's output schema is a four-class multiple-choice classification: models predict
one of options A, B, C, or D [Q83], and performance is measured as classification accuracy
across all examples [Q34, Q23]. Human baselines are established at two levels: unspecialised
Amazon Mechanical Turk workers at 34.5% and an estimated expert-level ceiling of approximately
89.8% [Q21]. The evaluation format is explicitly noted as not identical to the format in which
information is acquired during pretraining [Q62]. Calibration is assessed by comparing average
model confidence against actual accuracy per subject [Q56, Q58].

This label-only output taxonomy constitutes a HIGH-priority Output Ontology mismatch for the
deployment. The deployment requires the AI to produce both a correct/incorrect verdict and a
substantive Hindi-language explanation of why an answer is right or wrong. MMLU's design does
not support, test, or approximate this output structure. A model's MMLU accuracy score provides
no evidence about its capacity to generate accurate, coherent, or pedagogically appropriate
Hindi explanations — the core output requirement of the deployment.

### Output Content
NOT DOCUMENTED: The paper is entirely silent on annotator demographics, annotator
qualifications, inter-annotator agreement protocols, and quality-assurance procedures for
label validation. No quotes in the registry address these topics. Questions were assembled
by graduate and undergraduate students at US universities [Q17] and validated implicitly
against US-standard answer keys; there is no documented participation by Indian subject-matter
experts, UPSC/SSC exam specialists, or Hindi-medium educators. The paper acknowledges that
models may have encountered test questions during pretraining via Wikipedia [Q100], though
entropy analysis suggests exact memorisation is unlikely [Q98, Q99]. For any India-centric
adaptation, the complete absence of annotator representativeness documentation makes it
impossible to verify whether ground-truth labels would align with what Indian
competitive-exam stakeholders would judge correct. This gap directly undermines the
benchmark's transferability to any non-US deployment context.

### Output Form
The primary metric is classification accuracy (percentage of correct A/B/C/D selections)
computed across all tasks and reported by subject-area cluster [Q34, Q41]. GPT-3 confidence
is compared against accuracy per subject [Q56], with RMS calibration error reported for
individual tasks [Q58]; GPT-3 confidence deviates from actual accuracy by up to 24% in
zero-shot settings [Q57] and up to 14% in few-shot settings [Q96]. The benchmark evaluates
GPT-3 variants (Ada/Babbage/Curie/Davinci) and UnifiedQA (T5-based) as representative
models [Q35, Q36, Q37], with the largest GPT-3 achieving 43.9% few-shot accuracy [Q45]
and UnifiedQA-11B achieving 48.9% [Q47]. Performance is notably lopsided: GPT-3 reaches
nearly 70% on US Foreign Policy but near-random on several STEM subjects [Q12, Q49].

Output form represents a moderate-priority mismatch for the deployment. Both MMLU and the
deployment use text-based MCQ as the interaction vehicle, which is a partial match. However,
MMLU's label-only output form (a single letter prediction) diverges sharply from the
deployment's requirement for Hindi-language explanatory feedback. No metric in the benchmark
evaluates natural-language rationale quality, Hindi fluency, or pedagogical appropriateness
of explanations [Q62], and the calibration failures documented [Q14, Q57] raise further
concerns about whether any confidence signal from MMLU transfers to a Hindi exam-prep context.

### Stated Limitations
The authors acknowledge that models have near-random accuracy on "socially important subjects
such as morality and law" [Q6] and that performance is lopsided across subjects [Q5, Q12].
Calculation-heavy STEM subjects and subjects related to human values are identified as the
weakest areas [Q13, Q50, Q65, Q66]. Calibration failures are noted as a serious concern,
with GPT-3 confidence deviating from accuracy by up to 24% [Q14, Q57]. Multimodal
information is explicitly excluded [Q59]. The authors do not acknowledge the absence of
non-English or non-Western subject coverage as a limitation — a significant validity-relevant
omission for any non-US deployment context.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "We propose a new test to measure a text model's multitask accuracy. The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more." |
| Q2 | 1 | input_content | "To attain high accuracy on this test, models must possess extensive world knowledge and problem solving ability." |
| Q3 | 1 | output_form | "We find that while most recent models have near random-chance accuracy, the very largest GPT-3 model improves over random chance by almost 20 percentage points on average." |
| Q4 | 1 | output_ontology | "However, on every one of the 57 tasks, the best models still need substantial improvements before they can reach expert-level accuracy." |
| Q5 | 1 | output_ontology | "Models also have lopsided performance and frequently do not know when they are wrong." |
| Q6 | 1 | output_ontology | "Worse, they still have near-random accuracy on some socially important subjects such as morality and law." |
| Q7 | 1 | input_form | "We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings." |
| Q8 | 1 | input_ontology | "The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more. It ranges in difficulty from an elementary level to an advanced professional level, and it tests both world knowledge and problem solving ability." |
| Q9 | 1 | input_content | "Dan Hendrycks UC Berkeley, Collin Burns Columbia University, Steven Basart UChicago, Andy Zou UC Berkeley, Mantas Mazeika UIUC, Dawn Song UC Berkeley, Jacob Steinhardt UC Berkeley" |
| Q10 | 2 | input_ontology | "Since our test consists in 57 tasks, it can be used to analyze aggregate properties of models across tasks and to track important shortcomings." |
| Q11 | 2 | output_form | "We find that meaningful progress on our benchmark has only become possible in recent months. In particular, few-shot models up to 13 billion parameters (Brown et al., 2020) achieve random chance performance of 25% accuracy, but the 175 billion parameter GPT-3 model reaches a much higher 43.9% accuracy (see Figure 1b)." |
| Q12 | 2 | output_form | "On the other hand, unlike human professionals GPT-3 does not excel at any single subject. Instead, we find that performance is lopsided, with GPT-3 having almost 70% accuracy for its best subject but near-random performance for several other subjects." |
| Q13 | 2 | output_ontology | "Our results indicate that while recent advances have been impressive, state-of-the-art models still struggle at learning and applying knowledge from pretraining. The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality." |
| Q14 | 2 | output_form | "Worryingly, we also find that GPT-3 does not have an accurate sense of what it does or does not know since its average confidence can be up to 24% off from its actual accuracy." |
| Q15 | 2 | input_ontology | "We comprehensively evaluate the breadth and depth of a model's text understanding by covering numerous topics that humans are incentivized to learn." |
| Q16 | 3 | input_ontology | "We create a massive multitask test consisting of multiple-choice questions from various branches of knowledge. The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn. There are 57 tasks in total, which is also the number of Atari games (Bellemare et al., 2013), all of which are listed in Appendix B." |
| Q17 | 3 | input_content | "The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online. These include practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination. It also includes questions designed for undergraduate courses and questions designed for readers of Oxford University Press books." |
| Q18 | 3 | input_ontology | "Some tasks cover a subject, like psychology, but at a specific level of difficulty, such as "Elementary," "High School," "College," or "Professional." For example, the "Professional Psychology" task draws on questions from freely available practice questions for the Examination for Professional Practice in Psychology, while the "High School Psychology" task has questions like those from Advanced Placement Psychology examinations." |
| Q19 | 3 | input_form | "We collected 15908 questions in total, which we split into a few-shot development set, a validation set, and a test set. The few-shot development set has 5 questions per subject, the validation set may be used for selecting hyperparameters and is made of 1540 questions, and the test set has 14079 questions." |
| Q20 | 3 | input_form | "Each subject contains 100 test examples at the minimum, which is longer than most exams designed to assess people." |
| Q21 | 3 | output_form | "Human-level accuracy on this test varies. Unspecialized humans from Amazon Mechanical Turk obtain 34.5% accuracy on this test. Meanwhile, expert-level performance can be far higher. For example, real-world test-taker human accuracy at the 95th percentile is around 87% for US Medical Licensing Examinations, and these questions make up our "Professional Medicine" task. If we take the 95th percentile human test-taker accuracy for exams that build up our test, and if we make an educated guess when such information is unavailable, we then estimate that expert-level accuracy is approximately 89.8%." |
| Q22 | 3 | output_ontology | "Since our test aggregates different subjects and several levels of difficulty, we measure more than straightforward commonsense or narrow linguistic understanding. Instead, we measure arbitrary" |
| Q23 | 3 | output_ontology | "Consequently, we instead create a simple-to-evaluate test that measures classification accuracy on multiple choice questions." |
| Q24 | 4 | input_ontology | "The humanities is a group of disciplines that make use of qualitative analysis and analytic methods rather than scientific empirical methods. Branches of the humanities include law, philosophy, history, and so on (Appendix B)." |
| Q25 | 4 | input_ontology | "Mastering these subjects requires a variety of skills. For example, legal understanding requires knowledge of how to apply rules and standards to complex scenarios, and also provide answers with stipulations and explanations." |
| Q26 | 4 | input_content | "For philosophy, our questions cover concepts like logical fallacies, formal logic, and famous philosophical arguments. It also covers moral scenarios, including questions from the ETHICS dataset (Hendrycks et al., 2020) that test a model's understanding of normative statements through predicting widespread moral intuitions about diverse everyday scenarios." |
| Q27 | 4 | input_ontology | "Finally, our history questions cover a wide range of time periods and geographical locations, including prehistory and other advanced subjects." |
| Q28 | 4 | input_ontology | "Social science includes branches of knowledge that examine human behavior and society. Subject areas include economics, sociology, politics, geography, psychology, and so on." |
| Q29 | 4 | input_ontology | "Our economics questions include microeconomics, macroeconomics, and econometrics, and cover different types of problems, including questions that require a mixture of world knowledge, qualitative reasoning, or quantitative reasoning." |
| Q30 | 4 | input_ontology | "We also include important but more esoteric topics such as security studies in order to test the boundaries of what is experienced and learned during pretraining." |
| Q31 | 4 | input_ontology | "Social science also includes psychology, a field that may be especially important for attaining a nuanced understanding of humans." |
| Q32 | 4 | input_ontology | "STEM subjects include physics, computer science, mathematics, and more." |
| Q33 | 4 | input_ontology | "Conceptual physics tests understanding of simple physics principles and may be thought" |
| Q34 | 5 | output_form | "To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks." |
| Q35 | 5 | output_form | "We evaluate GPT-3 (Brown et al., 2020) and UnifiedQA (Khashabi et al., 2020)." |
| Q36 | 5 | output_form | "For GPT-3 we use the OpenAI API, which provides access to four model variants, "Ada," "Babbage," "Curie," and "Davinci," which we refer to as "Small" (2.7 billion parameters), "Medium" (6.7 billion), "Large" (13 billion) and "X-Large" (175 billion)." |
| Q37 | 5 | output_form | "UnifiedQA uses the T5 (Raffel et al., 2019) text-to-text backbone and is fine-tuned on previously proposed question answering datasets (Lai et al., 2017), where the prediction is the class with the highest token overlap with UnifiedQA's text output." |
| Q38 | 5 | output_form | "Since UnifiedQA is fine-tuned on other datasets, we evaluate it without any further tuning to assess its transfer accuracy." |
| Q39 | 5 | output_form | "We also fine-tune RoBERTa-base, ALBERT-xxlarge, and GPT-2 on UnifiedQA training data and our dev+val set." |
| Q40 | 5 | output_form | "We primarily focus on UnifiedQA and GPT-3 in the rest of this document, but additional discussion of RoBERTa, ALBERT, and GPT-2 is in Appendix A." |
| Q41 | 5 | output_form | "All values are percentages." |
| Q42 | 5 | output_form | "Some models proposed in the past few months can move several percent points beyond random chance." |
| Q43 | 5 | output_form | "GPT-3 uses few-shot learning and UnifiedQA is tested under distribution shift." |
| Q44 | 6 | input_form | "We feed GPT-3 prompts like that shown in Figure 1a. We begin each prompt with "The following are multiple choice questions (with answers) about [subject]." For zero-shot evaluation, we append the question to the prompt. For few-shot evaluation, we add up to 5 demonstration examples with answers to the prompt before appending the question. All prompts end with "Answer: ". The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction. For consistent evaluation, we create a dev set with 5 fixed few-shot examples for each subject." |
| Q45 | 6 | output_form | "We compare the few-shot accuracy of each GPT-3 size in Table 1. We find that the three smaller GPT-3 models have near random accuracy (around 25%). In contrast, we find that the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%." |
| Q46 | 6 | output_form | "While the smaller models have around 25% zero-shot accuracy, Figure 10 in Appendix A shows that the largest GPT-3 model has a much higher zero-shot accuracy of about 37.7%." |
| Q47 | 6 | output_form | "The largest UnifiedQA model we test has 11 billion parameters, which is slightly smaller than GPT-3 Large. Nevertheless, we show in Table 1 that it attains 48.9% accuracy. This performs better than the few-shot GPT-3 X-Large model, despite UnifiedQA have an order of magnitude fewer parameters." |
| Q48 | 6 | output_form | "We also find that even the smallest UnifiedQA variant, with just 60 million parameters, has approximately 29.3% accuracy. These results suggest that while model size is a key component for achieving strong performance, fine-tuning also helps." |
| Q49 | 6 | input_ontology | "Figure 6 shows the accuracy of GPT-3 (few-shot) and UnifiedQA for all 57 tasks. It shows the both models are below expert-level performance for all tasks, with GPT-3's accuracy ranging from 69% for US Foreign Policy to 26% for College Chemistry. UnifiedQA does best on marketing, with an accuracy of 82.5%." |
| Q50 | 6 | output_ontology | "Overall, models do poorly on highly procedural problems. Figure 6 shows that calculation-heavy STEM subjects tend to have low accuracy compared to verbal subjects. The lowest-accuracy tasks are STEM subjects that emphasize mathematics or calculations. We speculate that is in part because GPT-3 acquires declarative knowledge more readily than procedural knowledge." |
| Q51 | 7 | input_content | "For example, many questions in Elementary Mathematics require applying the order of operations for arithmetic, which is described by the acronym PEMDAS (Parentheses Exponents Multiplication Division Addition Subtraction)." |
| Q52 | 7 | output_ontology | "GPT-3 is aware of the acronym PEMDAS. However, it does not consistently apply PEMDAS to actual problems." |
| Q53 | 7 | output_ontology | "GPT-3 learns about topics in a pedagogically unusual order. GPT-3 does better on College Medicine (47.4%) and College Mathematics (35.0%) than calculation-heavy Elementary Mathematics (29.9%)." |
| Q54 | 7 | output_ontology | "GPT-3 demonstrates unusual breadth, but it does not master a single subject. Meanwhile we suspect humans have mastery in several subjects but not as much breadth. In this way, our test shows that GPT-3 has many knowledge blindspots and has capabilities that are lopsided." |
| Q55 | 7 | output_form | "We should not trust a model's prediction unless the model is calibrated, meaning that its confidence is a good estimate of the actual probability the prediction is correct." |
| Q56 | 7 | output_form | "We evaluate the calibration of GPT-3 by testing how well its average confidence estimates its actual accuracy for each subject." |
| Q57 | 7 | output_form | "GPT-3 is uncalibrated. In fact, its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects." |
| Q58 | 7 | output_form | "Another calibration measure is the Root Mean Squared (RMS) calibration error (Hendrycks et al., 2019a; Kumar et al., 2019). Many tasks have miscalibrated predictions, such as Elementary Mathematics which has a zero-shot RMS calibration error of 19.4%." |
| Q59 | 7 | input_form | "While text is capable of conveying an enormous number of concepts about the world, many important concepts are conveyed mainly through other modalities, such as images, audio, and physical interaction (Bisk et al., 2020). Existing large-scale NLP models, such as GPT-3, do not incorporate multimodal information, so we design our benchmark to capture a diverse array of tasks in a text-only format." |
| Q60 | 7 | input_content | "A major distinction between our benchmark and previous multitask NLP benchmarks is that we do not require large training sets. Instead, we assume that models have acquired the requisite knowledge from reading vast quantities of diverse text from the Internet. For this reason we assess pretrained models in a zero-shot, few-shot, or transfer setting and we provide a dev, val, and test set for each task." |
| Q61 | 8 | output_form | "The dev set is used for few-shot prompts, the val set could be used for hyperparameter tuning, and the test set is used to compute the final accuracy." |
| Q62 | 8 | output_form | "Importantly, the format of our evaluation is not identical to the format in which information is acquired during pretraining." |
| Q63 | 8 | output_content | "This has the benefit of obviating concerns about spurious training set annotation artifacts (Geirhos et al., 2020; Hendrycks et al., 2019b) and is in stark contrast to the previous paradigm of identically distributed training and test sets." |
| Q64 | 8 | output_ontology | "We find that current large-scale Transformers have wide room for improvement." |
| Q65 | 8 | output_ontology | "They are notably poor at modeling human (dis)approval, as evident by the low performance on the Professional Law and Moral Scenarios tasks." |
| Q66 | 8 | output_ontology | "Models also have difficulty performing calculations, so much so that they exhibit poor performance on Elementary Mathematics and many other STEM subjects with "plug and chug" problems." |
| Q67 | 8 | output_form | "Additionally, they do not match expert-level performance (90%) on any subject, so for all subjects it is subhuman." |
| Q68 | 8 | output_form | "On average, models are only now starting to move beyond random-chance accuracy levels." |
| Q69 | 8 | input_content | "We collected approximately 2,000 additional Professional Law training examples." |
| Q70 | 8 | output_form | "After fine-tuning a RoBERTa-base model (Liu et al., 2019) using this custom training set, our model attained 32.8% test accuracy." |
| Q71 | 8 | input_content | "We also had RoBERTa continue pretraining on approximately 1.6 million legal case summaries using Harvard's Law Library case law corpus case.law, but after fine-tuning it only attained 36.1% accuracy." |
| Q72 | 8 | output_form | "This suggests that while additional pretraining on relevant high quality text can help, it may not be enough to substantially increase the performance of current models." |
| Q73 | 8 | output_form | "It is unclear whether simply scaling up existing language models will solve the test." |
| Q74 | 8 | output_form | "Current understanding indicates that a 10× increase in model size must be accompanied by an approximate 5× increase in data (Kaplan et al., 2020)." |
| Q75 | 8 | input_ontology | "We introduced a new test that measures how well text models can learn and apply knowledge encountered during pretraining." |
| Q76 | 8 | input_ontology | "By covering 57 subjects at varying levels of difficulty, the test assesses language understanding in greater breadth and depth than previous benchmarks." |
| Q77 | 9 | output_content | "We would like to thank the following for their helpful comments: Oyvind Tafjord, Jan Leike, David Krueger, Alex Tamkin, Girish Sastry, and Henry Zhu." |
| Q78 | 9 | output_content | "DH is supported by the NSF GRFP Fellowship and an Open Philanthropy Project Fellowship." |
| Q79 | 9 | output_content | "This research was also supported by the NSF Frontier Award 1804794." |
| Q80 | 11 | input_ontology | "This appendix includes figures with sorted results (Figure 9), few-shot examples vs. accuracy (Figure 10), and few-shot calibration (Figure 11). It also includes sections on fine-tuning, error analysis, and format sensitivity." |
| Q81 | 11 | output_form | "We primarily analyzed models with more than 10 billion parameters in the main body of the paper. For this section, we analyze smaller models including RoBERTa-base (125 million parameters) (Liu" |
| Q82 | 11 | output_form | "On the left are GPT-3 few shot accuracies for all of the 57 tasks. On the right are UnifiedQA transfer accuracies for all of the 57 tasks. For both models, capabilities are lopsided." |
| Q83 | 12 | output_ontology | "Models are fine-tuned to predict one of four classes using the UnifiedQA MCQ questions and using our dev+val set. We test on our multitask test set." |
| Q84 | 12 | output_form | "RoBERTa-base attains an overall accuracy of 27.9%, with 27.9% accuracy for the humanities, 28.8% for social sciences, 27.0% for STEM, and 27.7% for other." |
| Q85 | 12 | output_form | "ALBERT-xxlarge attains an accuracy of 27.1%, with 27.2% accuracy for the humanities, 25.7% for the social sciences, 27.7% for STEM, and 27.9% for other." |
| Q86 | 12 | output_form | "GPT-2 attains an accuracy of 32.4%, with 32.8% accuracy for the humanities, 33.3% for the social sciences, 30.2% for STEM, and 33.1% for other." |
| Q87 | 12 | output_form | "UnifiedQA's smallest variant, which has just 60 million parameters and approximately 29.3% accuracy. It obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters. This suggests that its larger pretraining dataset enables higher accuracy." |
| Q88 | 12 | output_form | "UnifiedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy. This again suggests that T5's larger pretraining dataset size (and therefore UnifiedQA's pretraining dataset size) can increase accuracy." |
| Q89 | 12 | output_content | "We qualitatively analyze when GPT-3 makes high confidence mistakes. We find that while many of these mistakes were clearly wrong, many were mistakes that a human might make." |
| Q90 | 12 | input_form | "While different question formatting choices often lead to similar GPT-3 accuracies, we find that UnifiedQA is more sensitive." |
| Q91 | 12 | input_form | "UnifiedQA's input format is of the form QUESTION1 \n (A) CHOICE1 (B) CHOICE2 (C) CHOICE3 (D) CHOICE4</s> where questions and choices are normalized and made lowercase." |
| Q92 | 12 | input_form | "If we remove the </s> from the input, accuracy declines by several percentage points." |
| Q93 | 13 | input_ontology | "We provide analysis of question length and difficulty in Figure 12. We list all tasks and the topics they test in Table 2. We also provide an example for each task starting with Figure 14." |
| Q94 | 13 | input_form | "For questions longer than a tweet (280 characters), the correlation between question length and true label confidence is slightly positive. This shows that longer questions are not necessarily harder." |
| Q95 | 13 | output_content | "Since language models train on vast text corpora, there is some chance that they have seen the exact question and answer during pretraining. If they memorized the exact question and answer, then they would attain higher accuracy than their true ability. Likewise, a question's entropy would be especially low if it were memorized. Memorized questions and answers should have low entropy and" |
| Q96 | 13 | output_form | "While models are more calibrated in a few-shot setting than a zero-shot setting, they are still miscalibrated, with gap between accuracy and confidence reaching up to 14%. Here the correlation between confidence and accuracy is r = 0.81, compared to r = 0.63 in the zero-shot setting." |
| Q97 | 13 | output_form | "As the number of few-shot instruction examples increases, the accuracy monotonically increases. Notably, zero-shot performance is only somewhat lower than 5-shot accuracy." |
| Q98 | 14 | output_content | "However, in Figure 13, we see that accuracy and question entropy are not positively correlated, suggesting that the test's low-entropy questions do not correspond to memorized (and thereby correctly predicted) answers." |
| Q99 | 14 | output_content | "This suggests that our exact questions were not memorized." |
| Q100 | 14 | output_content | "However, during pretraining models encountered text related to our questions through processing Wikipedia." |
| Q101 | 14 | input_content | "We also note that most of our questions came from PDFs or websites where questions and answers are on separate pages." |
| Q102 | 14 | output_content | "To reduce the probability that future models encounter exact questions during test-time, we will provide a list of question sources." |
| Q103 | 14 | output_form | "In the zero-shot question prompt, the correlation between average log probability and accuracy is r = −0.43, and for the few-shot setting the correlation is r = −0.56." |
| Q104 | 15 | input_ontology | "Table 2: Summary of all 57 tasks." |
| Q105 | 16 | input_content | "Find all c in Z₃ such that Z₃[x]/(x² + c) is a field." |
| Q106 | 16 | input_content | "What is the embryological origin of the hyoid bone?" |
| Q107 | 16 | input_content | "Why isn't there a planet where the asteroid belt is located?" |
| Q108 | 16 | input_content | "Three contrasting tactics that CSO's can engage in to meet their aims are which typically involves research and communication, , which may involve physically attacking a company's operations or , often involving some form of ." |
| Q109 | 16 | input_content | "How many attempts should you make to cannulate a patient before passing the job on to a senior colleague?" |
| Q110 | 16 | input_content | "In a given population, 1 out of every 400 people has a cancer caused by a completely recessive allele, b. Assuming the population is in Hardy-Weinberg equilibrium, which of the following is the expected proportion of individuals who carry the b allele but are not expected to develop the cancer?" |
| Q111 | 16 | input_content | "Which of the following statements about the lanthanide elements is NOT true?" |
| Q112 | 17 | input_content | "Consider a computer design in which multiple processors, each with a private cache memory, share global memory using a single bus." |
| Q113 | 17 | input_content | "Let A be a real 2 × 2 matrix. Which of the following statements must be true?" |
| Q114 | 17 | input_content | "In a genetic test of a newborn, a rare genetic disorder is found that has X-linked recessive transmission." |
| Q115 | 17 | input_content | "One end of a Nichrome wire of length 2L and cross-sectional area A is attached to an end of another Nichrome wire of length L and cross- sectional area 2A." |
| Q116 | 17 | input_content | "Why is it that anti-virus scanners would not have found an exploitation of Heartbleed?" |
| Q117 | 17 | input_content | "A model airplane flies slower when flying into the wind and faster with wind at its back." |
| Q118 | 18 | input_content | "Consider the following AR(1) model with the disturbances having zero mean and unit variance yt = 0.2 + 0.4yt−1 + ut The (unconditional) mean of y will be given by (A) 0.2 (B) 0.4 (C) 0.5 (D) 0.33" |
| Q119 | 18 | input_content | "A point pole has a strength of 4π × 10−4 weber. The force in newtons on a point pole of 4π × 1.5 × 10−4 weber placed at a distance of 10 cm from it will be (A) 15 N. (B) 20 N. (C) 7.5 N. (D) 3.75 N." |
| Q120 | 18 | input_content | "A total of 30 players will play basketball at a park. There will be exactly 5 players on each team. Which statement correctly explains how to find the number of teams needed? (A) Add 5 to 30 to find 35 teams. (B) Divide 30 by 5 to find 6 teams. (C) Multiply 30 and 5 to find 150 teams. (D) Subtract 5 from 30 to find 25 teams." |
| Q121 | 18 | input_content | "Determine whether the statements are logically equivalent or contradictory. If neither, determine whether they are consistent or inconsistent. E ⊃ (F · E) and ∼ E · F (A) Logically equivalent (B) Contradictory (C) Neither logically equivalent nor contradictory, but consistent (D) Inconsistent" |
| Q122 | 18 | input_content | "As of 2017, how many of the world's 1-year-old children today have been vaccinated against some disease? (A) 80% (B) 60% (C) 40% (D) 20%" |
| Q123 | 18 | input_content | "Homologous structures are often cited as evidence for the process of natural selection. All of the following are examples of homologous structures EXCEPT (A) the wings of a bird and the wings of a bat (B) the flippers of a whale and the arms of a man (C) the pectoral fins of a porpoise and the flippers of a seal (D) the forelegs of an insect and the forelimbs of a dog" |
| Q124 | 18 | input_content | "From the solubility rules, which of the following is true? (A) All chlorides, bromides, and iodides are soluble (B) All sulfates are soluble (C) All hydroxides are soluble (D) All ammonium-containing compounds are soluble" |
| Q125 | 19 | input_content | "A list of numbers has n elements, indexed from 1 to n. The following algorithm is intended to display the number of elements in the list that have a value greater than 100. The algorithm uses the variables count and position. Steps 3 and 4 are missing." |
| Q126 | 19 | input_content | "Which of the following could be used to replace steps 3 and 4 so that the algorithm works as intended?" |
| Q127 | 19 | input_content | "Figure 34: A High School Computer Science example." |
| Q128 | 19 | input_content | "This question refers to the following information." |
| Q129 | 19 | input_content | "From the passage, one may infer that the English Parliament wished to argue that the Act of Supremacy would" |
| Q130 | 19 | input_content | "Figure 35: A High School European History example." |
| Q131 | 19 | input_content | "During the third stage of the demographic transition model, which of the following is true?" |
| Q132 | 19 | input_content | "Figure 36: A High School Geography example." |
| Q133 | 20 | input_content | "Figure 37: A High School Government and Politics example." |
| Q134 | 20 | input_content | "Figure 38: A High School Macroeconomics example." |
| Q135 | 20 | input_content | "Figure 39: A High School Mathematics example." |
| Q136 | 20 | input_content | "Figure 40: A High School Microeconomics example." |
| Q137 | 20 | input_content | "Figure 41: A High School Physics example." |
| Q138 | 20 | input_content | "Figure 42: A High School Psychology example." |
| Q139 | 21 | input_content | "Figure 43: A High School Statistics example." |
| Q140 | 21 | input_content | "Figure 44: A High School US History example." |
| Q141 | 21 | input_content | "Figure 45: A High School World History example." |
| Q142 | 21 | input_content | "Figure 46: A Human Aging example." |
| Q143 | 22 | input_content | "Morning sickness is typically a problem: (A) during the first trimester (B) during the second trimester (C) during the third trimester (D) all through the pregnancy" |
| Q144 | 22 | input_content | "Would a reservation to the definition of torture in the ICCPR be acceptable in contemporary practice? (A) This is an acceptable reservation if the reserving country's legislation employs a different definition (B) This is an unacceptable reservation because it contravenes the object and purpose of the ICCPR (C) This is an unacceptable reservation because the definition of torture in the ICCPR is consistent with customary international law (D) This is an acceptable reservation because under general international law States have the right to enter reservations to treaties" |
| Q145 | 22 | input_content | "Which position does Rawls claim is the least likely to be adopted by the POP (people in the original position)? (A) The POP would choose equality above liberty. (B) The POP would opt for the 'maximin' strategy. (C) The POP would opt for the 'difference principle.' (D) The POP would reject the 'system of natural liberty.'" |
| Q146 | 22 | input_content | "John Stuart Mill: Each person's happiness is a good to that person, and the general happiness, therefore, a good to the aggregate of all persons. (A) Fallacy of Composition (B) Fallacy of Division (C) Gambler's Fallacy (D) Equivocation" |
| Q147 | 22 | input_content | "A 6-sided die is rolled 15 times and the results are: side 1 comes up 0 times; side 2: 1 time; side 3: 2 times; side 4: 3 times; side 5: 4 times; side 6: 5 times. Based on these results, what is the probability of side 3 coming up when using Add-1 Smoothing? (A) 2/15 (B) 1/7 (C) 3/16 (D) 1/5" |
| Q148 | 22 | input_content | "According to Lewin, Lippet and White's 1939 experiment, which form of leadership produced the most work from participants? (A) Laissez-faire (B) Democratic (C) Authoritarian (D) A mix of laissez-faire and democratic" |
| Q149 | 23 | input_form | "The formatting of this task hinders UnifiedQA performance substantially." |
| Q150 | 24 | input_content | "According to Moore's "ideal utilitarianism," the right action is the one that brings about the greatest amount of: (A) pleasure. (B) happiness. (C) good. (D) virtue." |
| Q151 | 24 | input_content | "Researchers now believe that the decline of the Maya was caused chiefly by: (A) a cataclysm of some kind, such as an earthquake, volcano, or tsunami. (B) ecological degradation resulting from slash-and-burn farming techniques. (C) endless wars between neighboring Mayan city-states. (D) practices of interbreeding that led to a steep rise in congenital disorders." |
| Q152 | 24 | input_content | "Krete is an unmarried taxpayer with income exclusively from wages. By December 31, year 1, Krete's employer has withheld $16,000 in federal income taxes and Krete has made no estimated tax payments. On April 15, year 2, Krete timely filed for an extension request to file her individual tax return, and paid $300 of additional taxes. Krete's year 1 tax liability was $16,500 when she timely filed her return on April 30, year 2, and paid the remaining tax liability balance. What amount would be subject to the penalty for underpayment of estimated taxes? (A) $0 (B) $500 (C) $1,650 (D) $16,500" |
| Q153 | 24 | input_content | "The night before his bar examination, the examinee's next-door neighbor was having a party. The music from the neighbor's home was so loud that the examinee couldn't fall asleep. The examinee called the neighbor and asked her to please keep the noise down. The neighbor then abruptly hung up. Angered, the examinee went into his closet and got a gun. He went outside and fired a bullet through the neighbor's living room window. Not intending to shoot anyone, the examinee fired his gun at such an angle that the bullet would hit the ceiling. He merely wanted to cause some damage to the neighbor's home to relieve his angry rage. The bullet, however, ricocheted off the ceiling and struck a partygoer in the back, killing him. The jurisdiction makes it a misdemeanor to discharge a firearm in public. The examinee will most likely be found guilty for which of the following crimes in connection to the death of the partygoer? (A) Murder. (B) Involuntary manslaughter. (C) Voluntary manslaughter. (D) Discharge of a firearm in public." |
| Q154 | 25 | input_content | "A 63-year-old man is brought to the emergency department because of a 4-day history of increasingly severe left leg pain and swelling of his left calf. He also has a 1-month history of increasingly severe upper midthoracic back pain. During this time, he has had a 9-kg (20-lb) weight loss despite no change in appetite. He has no history of major medical illness. His only medications is ibuprofen. He is 180 cm (5 ft 11 in) tall and weighs 82 kg (180 lb); BMI is 25 kg/m2. His vital signs are within normal limits. On examination, lower extremity pulses are palpable bilaterally. The remainder of the physical examination shows no abnormalities. An x-ray of the thoracic spine shows no abnormalities. A CT scan of the abdomen shows a 3-cm mass in the body of the pancreas; there are liver metastases and encasement of the superior mesenteric artery. Ultrasonography of the left lower extremity shows a femoropopliteal venous clot. Which of the following is the most likely cause of this patient's symptoms?" |
| Q155 | 25 | input_content | "The technique that is most likely to produce an immediate improvement in the behavior of a child who hits others and rips up schoolbooks is" |
| Q156 | 25 | input_content | "You work for a utility company that is building a biomass plant in the community. Your employer asks you to give a series of community talks about the plant and future operations. You visit the plant several hours before you are due to give a speech that has been prepared by your immediate supervisor. During the tour of the plant, you discover several claims in the speech are not true. What do you do?" |
| Q157 | 26 | input_content | "Which of the following statements most closely corresponds with differential association theory?" |
| Q158 | 26 | input_content | "Why did Congress oppose Wilson's proposal for the League of Nations?" |
| Q159 | 26 | input_content | "An observational study in diabetics assesses the role of an increased plasma fibrinogen level on the risk of cardiac events. 130 diabetic patients are followed for 5 years to assess the development of acute coronary syndrome. In the group of 60 patients with a normal baseline plasma fibrinogen level, 20 develop acute coronary syndrome and 40 do not. In the group of 70 patients with a high baseline plasma fibrinogen level, 40 develop acute coronary syndrome and 30 do not. Which of the following is the best estimate of relative risk in patients with a high baseline plasma fibrinogen level compared to patients with a normal baseline plasma fibrinogen level?" |
| Q160 | 27 | input_content | "Figure 70: A World Religions example." |

---

## Regional Context

```yaml
name: North India Competitive Exam Aspirants (Hindi-Medium)
abbreviation: NI-CEA
deployment_context:
  description: Hindi-speaking graduate students in North India (primarily Uttar Pradesh,
    Bihar, Rajasthan, Madhya Pradesh) using a mobile or enterprise AI application
    to prepare for centrally conducted competitive examinations (UPSC, SSC, banking
    exams). The AI evaluates student responses and provides both a correct/incorrect
    verdict and a substantive Hindi-language explanation of why the answer is right
    or wrong.
  primary_exam_targets:
  - UPSC Civil Services Examination (Prelims and Mains)
  - SSC CGL / SSC CHSL
  - SSC MTS and other Staff Selection Commission exams
  - Banking exams (IBPS PO, IBPS Clerk, SBI PO, RBI Grade B)
  - Railway Recruitment Board (RRB) examinations
  explicitly_out_of_scope:
  - State-level PSC examinations (UP PSC, BPSC, RPSC, MPPSC)
  - Judicial services examinations
  - Post-graduate entrance tests (JNU, BHU, etc.)
geography:
  primary_states:
  - Uttar Pradesh
  - Bihar
  - Rajasthan
  - Madhya Pradesh
  secondary_states:
  - Uttarakhand
  - Jharkhand
  - Chhattisgarh
  - Delhi (aspirant migration hub)
  urbanization_note: 'A significant share of competitive exam aspirants migrate to
    coaching hubs such as Prayagraj (Allahabad), Patna, Jaipur, and Delhi''s Mukherjee
    Nagar district. Aspirants from rural and semi-urban backgrounds constitute a large
    fraction of this population. Urban–rural split among UPSC/SSC aspirants: [NEEDS
    VERIFICATION — deferred: below search budget; note that nationally rural India
    surpassed urban areas in total internet users as of 2021 per IAMAI/Kantar 2024,
    suggesting rural aspirants are a fast-growing segment digitally, but aspirant-specific
    urban/rural breakdown is not published by UPSC or SSC]'
  coaching_hub_cities:
  - Prayagraj (Allahabad) — UPSC hub
  - Patna — Bihar PSC and UPSC aspirants
  - Jaipur — Rajasthan aspirants
  - Delhi (Mukherjee Nagar, Karol Bagh) — national UPSC coaching cluster
  - Indore — MP and central India aspirants
languages:
  primary: Hindi (Devanagari script)
  acceptable_code_mixing: Up to approximately 10% English technical terms embedded
    in otherwise Hindi text is acceptable; fully English-medium or heavily code-mixed
    content is a deployment mismatch.
  medium_of_education: Hindi-medium schooling through secondary and undergraduate
    level; limited English reading proficiency typical of this cohort.
  script: Devanagari (primary); Latin script tolerated only for English loan-words
    or established technical terms at the ~10% threshold.
  regional_dialect_note: Standard Khari Boli Hindi (as used in NCERT textbooks and
    Doordarshan broadcasts) is the register expected in the application, not regional
    vernaculars such as Bhojpuri, Awadhi, Braj, Bundeli, or Mewari — though aspirants
    may speak these natively.
  diglossia_note: Aspirants operate between their native dialect at home and standard
    formal Hindi (Manak Hindi) in academic and exam contexts. The application should
    target standard Manak Hindi to mirror exam conventions.
  english_proficiency_distribution: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice); no published breakdown of English reading proficiency levels
    specifically for UPSC/SSC aspirants from Hindi-medium backgrounds is available
    from UPSC, SSC, or national survey sources]'
writing_systems:
  scripts:
  - Devanagari (primary — all Hindi-medium content)
  - Latin/Roman (secondary — English technical terms, acronyms, exam names)
  nlp_handling_notes: 'Devanagari rendering and tokenization must be verified for
    the deployment stack. Hindi morphology (inflection for gender, number, case, tense)
    poses non-trivial NLP challenges. Code-mixed Devanagari-Latin text (Hinglish)
    requires mixed-script tokenization support. Hindi spell-checking and normalization
    tooling is less mature than English equivalents. Research on Hindi-specific LLMs
    (e.g., Nemotron-Mini-Hindi-4B) documents that purely Hindi Devanagari queries
    frequently produce hallucinations, meaningless sentences, and English content
    mixing even in models trained on 20B Hindi tokens — confirming that Devanagari
    tokenization quality is a live deployment risk (Source: Adapting Multilingual
    LLMs to Low-Resource Languages, arXiv:2410.14815 — [WEB-1]).'
literacy_and_education:
  population_literacy_rate_hindi_belt: 'Per NSO Periodic Labour Force Survey 2023–24
    (most recent available as of 2025), overall literacy rate (age 7+) in India is
    80.9%. State-specific recent figures: Bihar ~74.3% (overtaking Andhra Pradesh
    as lowest, per PLFS 2023–24); Uttar Pradesh overall literacy ~67.4% (NFHS-5 2019–21,
    total persons); Rajasthan ~69.7% (NSO data); Madhya Pradesh data not separately
    isolated in searched sources but consistent with national lagging-state averages.
    Caution: these are population-wide figures; the deployment cohort (graduate-level
    aspirants) will have substantially higher literacy by definition. Female literacy
    is notably lower in these states: Rajasthan 75.8%, UP 78.2%, Bihar and MP below
    national female average of 70.3% (NFHS-5 2019–21). Source: NSO/PLFS 2023–24 via
    Wikipedia Literacy in India — [WEB-2];
    NFHS-5 2019–21 India Report — [WEB-3];
    IndiaDataMap 2025 — [WEB-4]'
  graduate_level_assumption: All users in scope have completed undergraduate education
    (Bachelor's degree or equivalent) and are pursuing competitive exam preparation
    at graduate level.
  hindi_medium_education_share: '[NEEDS VERIFICATION — deferred: below search budget;
    no authoritative national-level figure for proportion of undergraduates studying
    through Hindi medium in UP/Bihar/Rajasthan/MP is available from searched sources;
    AISHE data may contain this but was not retrieved]'
  relevant_curriculum_bodies:
  - NCERT (National Council of Educational Research and Training) — standard curriculum
    reference for UPSC/SSC GK
  - CBSE / state boards of UP, Bihar, Rajasthan, MP
  - 'UPSC syllabus documents (current edition) — official syllabus published at upsc.gov.in;
    most recent Civil Services Examination notification is for CSE 2025. Source: upsc.gov.in
    — [WEB-5]'
  - 'SSC CGL/CHSL syllabus documents (current edition) — published at ssc.gov.in for
    each recruitment cycle; SSC CGL 2025 notification released. Source: ssc.gov.in
    — [WEB-6]'
target_subject_domains:
  priority_high:
  - domain: General Knowledge (samanya gyan)
    notes: Broad factual knowledge covering Indian and world geography, science and
      technology, sports, awards, and books — a mainstay of UPSC Prelims and SSC GK
      sections.
  - domain: Current Affairs (samayik ghatnayen)
    notes: Monthly and annual current affairs drawn from national newspapers, PIB,
      and Yojana/Kurukshetra magazines. Highly India-centric and time-sensitive. MMLU
      has no analogue.
  - domain: Indian History (prachin, madhyakalin, adhunik)
    notes: Ancient (Indus Valley through Gupta), medieval (Delhi Sultanate, Mughal),
      and modern (colonial, independence movement) Indian history per NCERT Class
      6–12 and standard UPSC reference books (Bipin Chandra, etc.). MMLU covers no
      South Asian historical content.
  - domain: Indian Polity and Constitution (bhartiya rajvyavastha)
    notes: 'Indian Constitution (Articles, Schedules, Amendments), Parliament, Executive,
      Judiciary, Panchayati Raj, fundamental rights, directive principles, federalism,
      electoral system. Standard reference: M. Laxmikant''s ''Indian Polity''. MMLU
      covers US legal/constitutional content only.'
  - domain: Mathematics and Quantitative Aptitude (ganit aur sankhyatmak yogyata)
    notes: Arithmetic, percentage, ratio-proportion, time-work, time-distance, mensuration,
      data interpretation, and simple/compound interest. Exam style is calculation-heavy
      MCQ, often with numeric answer options.
  - domain: Reasoning (tarkshakti)
    notes: Verbal and non-verbal reasoning, series completion, analogy, coding-decoding,
      syllogism, puzzle, seating arrangement. Present in SSC, banking, and RRB exams;
      lighter in UPSC Prelims.
  priority_moderate:
  - domain: Indian Geography (bhartiya bhugol)
    notes: Physical, political, and economic geography of India including rivers,
      mountains, climate zones, agriculture belts, natural resources, and state-wise
      demographic data.
  - domain: Indian Economy (arthavyavastha)
    notes: National income, planning, banking and financial system, agriculture, industry,
      and trade policy in the Indian context. References RBI reports, Economic Survey,
      and Union Budget.
  - domain: Hindi Language Proficiency (hindi bhasha yogyata)
    notes: Grammar, vocabulary, comprehension, and essay for UPSC Mains Hindi paper
      and SSC Hindi sections. Entirely absent from MMLU.
  - domain: Science and Technology (vigyan evam prodyogiki)
    notes: Basic physics, chemistry, biology (NCERT level), and contemporary science/technology
      developments in India (space, defense, health programs).
  priority_supplementary:
  - domain: North India–specific regional content
    notes: State-specific administrative structures (tehsils, mandals, blocks, panchayats),
      land-revenue traditions (zamindari abolition, UPZA, Bhu-Adhar), regional festivals
      (Chhath Puja, Makar Sankranti traditions, Teej), and historical figures associated
      with UP, Bihar, Rajasthan, MP. Required for both central exams' GK sections
      and for contextually accurate explanatory feedback.
  - domain: Environment and Ecology (paryavaran)
    notes: Environmental issues, biodiversity, climate change policy in the Indian
      context (NAPCC, COP commitments). Growing weight in UPSC Prelims.
output_requirements:
  verdict: Correct/incorrect binary label (sahi/galat) for each MCQ response.
  explanation: Substantive Hindi-language rationale explaining why the chosen option
    is correct or incorrect, and why each distractor is wrong where relevant. Pedagogically
    appropriate for an adult graduate-level learner.
  language_of_output: Hindi (Devanagari script), standard Manak Hindi register, with
    up to ~10% English technical terms permissible.
  output_form_mismatch_with_mmlu: MMLU produces only a predicted label (A/B/C/D).
    It does not test, score, or provide any signal about a model's capacity to generate
    Hindi-language explanatory feedback. This is a HIGH-priority output ontology mismatch.
  explanation_quality_rubric: '[NOT FOUND — searched for rubrics or benchmarks evaluating
    Hindi exam-prep explanation quality, fluency, factual accuracy, and pedagogical
    appropriateness; no dedicated rubric was found. Existing Hindi benchmarks (MILU,
    IndicMMLU-Pro, ParamBench, IndicEval) evaluate MCQ accuracy only and do not score
    free-form Hindi explanatory text quality. The ''Benchmarking Hindi LLMs'' suite
    (arXiv:2508.19831) introduces MT-Bench-Hi for conversational quality but is not
    specific to exam-prep pedagogy. A gap exists for a pedagogical rubric in this
    domain.]'
cultural_norms_notes: '- Competitive examination culture (''sarkari naukri'' aspiration)
  is deeply embedded in North Indian social values, particularly among OBC and general-category
  families from semi-urban and rural backgrounds.

  - Coaching institute ecosystem (Prayagraj, Delhi, Patna) shapes study materials,
  question styles, and expected answer conventions; the AI''s feedback should align
  with UPSC/SSC coaching-center conventions.

  - Hindi-medium aspirants have frequently faced systemic disadvantage in English-dominant
  examination aids and digital tools; the deployment''s Hindi-first design addresses
  a real equity gap.

  - Deference to authoritative text sources (NCERT books, Laxmikant, Bipin Chandra)
  is strong; the AI''s explanations should ideally cite or align with these canonical
  references.

  - Aspirants often study in resource-constrained settings (shared accommodation,
  limited data plans); mobile-optimized, low-bandwidth-friendly interaction is important.

  - Gender dynamics: Women constituted approximately 30% of selected UPSC candidates
  in 2023 (source: SleepyClasses analysis of UPSC data — [WEB-7]);
  more precisely, 34.4% of final UPSC selections are women per the UPSC Annual Report
  (source: Legacy IAS analysis — [WEB-8]).
  The number of women UPSC applicants grew nearly four-fold over 15 years to 3.37
  lakh by 2021–22 (source: The Print — [WEB-9]).
  A gendered UX consideration: online study access has specifically enabled women
  aspirants who face mobility restrictions; mobile-first design also addresses this.
  The gender-share among SSC/banking aspirants is not separately published.

  - Caste and reservation categories (SC/ST/OBC/EWS) affect exam eligibility, attempt
  limits, and cut-off thresholds; the AI should be neutral and accurate on reservation-related
  factual questions.

  '
infrastructure_notes: '- Mobile-first access is dominant; application must perform
  adequately on mid-range Android devices.

  - Mobile internet penetration in UP, Bihar, Rajasthan, MP: Per IAMAI/Kantar ''Internet
  in India 2024'' report, Bihar has 43% internet penetration (among the lowest in
  the country) and Uttar Pradesh has 46% — both in the bottom three nationally. Rajasthan
  and Madhya Pradesh figures are not separately top/bottom-listed but are assumed
  to fall in the 50–60% range, below the national trend. Note: TRAI subscriber counts
  show UP with 73.59 million and Bihar with 69.89 million internet subscribers (as
  of September 2023), making them large in absolute terms but low in penetration rates.
  Source: IAMAI/Kantar Internet in India 2024 — [WEB-10];
  TRAI data via Wikipedia — [WEB-11]; Business
  Standard — [WEB-12]

  - Average mobile data speed in these states: [NEEDS VERIFICATION — deferred: below
  search budget; TRAI publishes state-level speed data but state-specific figures
  for UP/Bihar/MP/Rajasthan were not retrieved; India''s national median mobile download
  speed was reported at 94.62 Mbit/s in November 2023 Speedtest Global Index, but
  this aggregates urban 5G and rural 4G, and rural speeds in these states will be
  substantially lower]

  - Electricity reliability in rural/semi-urban aspirant locations: [NEEDS VERIFICATION
  — deferred: likely unsearchable at granular level; UP and Bihar are documented as
  having persistent rural power supply challenges but quantified outage hours were
  not retrieved]

  - Devanagari font rendering and input method (keyboard) support on Android/iOS:
  generally available via Gboard, SwiftKey Hindi; but IME-related tokenization artifacts
  in LLM inputs should be tested.

  - Offline or low-connectivity mode may be needed for aspirants in areas with poor
  4G coverage. The IAMAI 2024 report notes 1 in 5 internet users access via a shared
  device, with rural shared-device usage growing 24% — relevant for deployment assumptions
  about device ownership.

  - Device distribution (Android vs. iOS, RAM range): [NEEDS VERIFICATION — deferred:
  below search budget; India is predominantly Android (>95% of smartphone market)
  with mid-range devices dominant, but aspirant-specific RAM distribution data is
  not published]

  '
benchmark_fit_summary:
  benchmark: MMLU (Measuring Massive Multitask Language Understanding)
  overall_validity_assessment: MMLU is a near-total mismatch for this deployment across
    all high-priority validity dimensions. Subject coverage, item content, input language,
    output form, and annotator pool are all misaligned with the North Indian Hindi-medium
    competitive exam context.
  dimension_assessments:
  - dimension: Input Ontology (IO)
    priority: HIGH
    verdict: Full gap
    notes: MMLU's 57 subjects cover no Indian Polity, Indian History, Indian Geography,
      Current Affairs, or Hindi language proficiency. The partial match on Mathematics/Reasoning
      is real but undermined by MMLU's documented poor calibration on calculation-heavy
      subjects.
  - dimension: Input Content (IC)
    priority: HIGH
    verdict: Full gap
    notes: Individual MMLU items embed US-default factual assumptions (US Congress,
      US bar exam, Western philosophical canon). No items address Indian administrative
      structures, North Indian regional content, or South Asian history.
  - dimension: Input Form (IF)
    priority: HIGH
    verdict: Full gap
    notes: MMLU is entirely English-medium with no Devanagari variant. The deployment
      requires Hindi-dominant input with ≤10% English code-mixing. MCQ format is a
      partial structural match but language/script mismatch overrides it.
  - dimension: Output Ontology (OO)
    priority: HIGH
    verdict: Full gap
    notes: MMLU scores only label accuracy (A/B/C/D). The deployment requires a verdict
      plus a substantive Hindi-language explanation. MMLU provides zero signal on
      Hindi generative output quality.
  - dimension: Output Content (OC)
    priority: HIGH
    verdict: Full gap
    notes: MMLU labels were validated by US university students with no documented
      Indian subject-matter expert participation. For India-centric GK, Polity, and
      History, label correctness from the Indian exam-standard perspective is unverifiable.
  - dimension: Output Form (OF)
    priority: MODERATE
    verdict: Partial gap
    notes: Both MMLU and the deployment use MCQ as the interaction vehicle (partial
      match). However, MMLU's label-only output metric diverges sharply from the required
      Hindi explanatory feedback, and calibration failures documented in MMLU further
      limit transferability.
flagged_gaps_and_search_targets:
- gap_id: 1
  description: Indian curriculum coverage absence in MMLU
  search_target: IndicMMLU IndiGO Indian benchmark LLM UPSC SSC Indian Polity History
    Geography evaluation
  verification_needed: Whether any MMLU subject can be partially mapped to Indian
    curriculum domains; existence and quality of Indian-origin benchmarks covering
    UPSC/SSC syllabi.
  resolution: 'RESOLVED. Multiple Indian benchmarks now exist that cover UPSC/SSC-relevant
    domains in Hindi: (1) MILU (AI4Bharat/NAACL 2025) — ~80,000 MCQs across 11 Indic
    languages including Hindi, 8 domains, 41 subjects, drawn from Indian competitive
    exams including local governance, arts, and history; GPT-4o achieves highest accuracy
    at 74%, with models performing poorly on culturally relevant areas like Law and
    Governance. Source: ACL Anthology — [WEB-13];
    HuggingFace — [WEB-14]. (2) ParamBench
    (arXiv:2508.16185, Aug 2025) — 17K+ Hindi-language questions from UGC-NET and
    UPSC covering 21 Indic subjects (Indian history, literature, archaeology, law,
    yoga, philosophy, etc.), expert-annotated. Source: arXiv — [WEB-15].
    (3) IndicEval (arXiv:2602.16467, Feb 2026) — bilingual (English/Hindi) benchmark
    using authentic UPSC, JEE, and NEET questions; documents multilingual degradation
    with marked accuracy drops in Hindi vs. English especially under Zero-Shot, and
    lowest accuracy of 39.53% for LLaMA on UPSC Hindi Zero-Shot. Source: arXiv — [WEB-16].
    Critical caveat: none of these benchmarks evaluates Hindi-language explanatory
    feedback quality, which is the core deployment output requirement. MILU and ParamBench
    evaluate MCQ label accuracy only.'
- gap_id: 2
  description: Hindi-language MMLU variant availability and quality
  search_target: Hindi MMLU translation Devanagari dataset community benchmark quality
    evaluation 2023 2024
  verification_needed: Whether a Hindi-translated MMLU dataset exists, who produced
    it, and whether translation quality has been independently evaluated.
  resolution: 'RESOLVED. Multiple Hindi/Indic MMLU variants exist: (1) OpenAI MMMLU
    — professionally translated MMLU test questions across 14 languages including
    Hindi (~15,908 questions per language, 57 subjects). Source: LLM-Stats — [WEB-17].
    (2) IndicMMLU-Pro (arXiv:2501.15747, Jan 2025) — adapts MMLU-Pro to 9 Indic languages
    including Hindi; back-translation chrF++ scores above 74 for Hindi indicate adequate
    semantic preservation but noted phrasing/structural variation from English original.
    Dataset on HuggingFace. Source: arXiv — [WEB-18].
    (3) MMLU-ProX (arXiv:2503.10497, Mar 2025) — extends MMLU-Pro to 29 languages
    including Hindi with LLM translation plus expert review. Source: arXiv — [WEB-19].
    Critical limitation: all three variants translate Western-anchored MMLU content
    into Hindi; they do not introduce Indian curriculum content. Translating US History
    or US bar-exam items into Hindi does not resolve the subject-matter gap. Research
    confirms translated datasets suffer cultural mismatch since many MMLU questions
    (US History, Law) are Western-specific. Source: arXiv:2509.11570 survey — [WEB-20].'
- gap_id: 3
  description: North India–specific and pan-India regional content benchmarks
  search_target: Chhath Puja panchayati raj tehsil North India regional knowledge
    LLM benchmark AI evaluation
  verification_needed: Whether any benchmark covers Indian administrative structures,
    North Indian festivals, land-revenue traditions, and state-wise demographic content
    analogous to UPSC/SSC GK sections.
  resolution: 'PARTIALLY RESOLVED. MILU (AI4Bharat, NAACL 2025) incorporates material
    from regional and state-level examinations covering local history, arts, festivals,
    and laws — making it the closest existing match to UPSC/SSC GK regional content
    needs. It spans 8 domains and 41 subjects with India-centric design. However,
    MILU evaluates MCQ accuracy across all 11 languages and does not isolate North
    India–specific content (Chhath Puja, tehsil structures, land-revenue traditions,
    UP/Bihar/Rajasthan/MP administrative specifics) as a distinct sub-domain. No benchmark
    specifically targeting these North India sub-regional items was found. Source:
    HuggingFace MILU — [WEB-14]; ACL Anthology
    — [WEB-13].'
- gap_id: 4
  description: Hindi explanatory feedback quality benchmarking
  search_target: Hindi explanation quality benchmark LLM exam feedback rubric Devanagari
    generative evaluation pedagogy
  verification_needed: Whether any rubric or benchmark assesses LLM Hindi-language
    explanation quality in educational or exam-prep contexts; whether MMLU-evaluated
    models have been tested for Hindi rationale generation.
  resolution: 'NOT FOUND — searched arXiv and recent Hindi LLM evaluation literature.
    The ''Benchmarking Hindi LLMs'' suite (arXiv:2508.19831, Aug 2025) introduces
    five Hindi evaluation datasets including MT-Bench-Hi for instruction-following/conversational
    quality adapted with Indian cultural themes, but this is not specific to exam-prep
    pedagogical explanation quality. No benchmark evaluating Hindi explanatory rationale
    quality for competitive exam contexts was found. This remains a genuine gap in
    the literature. Source for closest proxy: arXiv:2508.19831 — [WEB-21].'
- gap_id: 5
  description: Code-mixing threshold and Hinglish handling
  search_target: Hinglish code-mixed Hindi LLM evaluation benchmark educational competitive
    exam Devanagari Latin
  verification_needed: Evidence on how leading LLMs handle lightly code-mixed Hindi
    (≤10% English); whether MMLU-translated Hindi prompts preserve acceptable code-mix
    ratios.
  resolution: 'PARTIALLY RESOLVED. Research on Hindi LLM deployment (Nemotron-Mini-Hindi-4B,
    arXiv:2410.14815) explicitly supports Hindi, English, and Hinglish, and was trained
    on 400B Hindi and English tokens with equal proportions — indicating that code-mixed
    Hinglish handling is an active research area but requires deliberate training
    data design. The broader Hindi LLM evaluation literature documents that models
    frequently mix English into purely Hindi Devanagari responses. No benchmark specifically
    measuring the ≤10% code-mix threshold tolerance for the competitive exam context
    was found. Source: arXiv:2410.14815 — [WEB-1].'
- gap_id: 6
  description: Indian annotator representativeness for label validation
  search_target: Indian expert annotator UPSC SSC benchmark label validation Hindi
    subject matter expert annotation quality
  verification_needed: Whether any India-adapted benchmark or MMLU variant used Indian
    UPSC/SSC subject-matter experts for label creation or validation.
  resolution: 'PARTIALLY RESOLVED. ParamBench (arXiv:2508.16185) uses a two-tier annotation
    team and derives questions from official UGC-NET/UPSC papers with human annotators
    manually correcting OCR errors, restoring diacritics, and verifying question-answer
    alignment — representing the strongest Indian expert annotation chain found. MILU
    derives questions from Indian competitive examinations, providing implicit label
    validity through the official exam pipeline. IndicMMLU-Pro uses back-translation
    quality checks but no documented Indian subject-matter expert review for content
    validity. None of the found benchmarks documents UPSC/SSC exam specialists as
    explicit validators in a formal annotation protocol. Source: arXiv:2508.16185
    — [WEB-15]; arXiv:2501.15747 — [WEB-18].'
- gap_id: 7
  description: Current Affairs benchmark for India
  search_target: Indian current affairs AI benchmark LLM evaluation 2023 2024 UPSC
    general knowledge dynamic knowledge
  verification_needed: Whether any benchmark evaluates LLM performance on India-centric
    current affairs; how frequently it is updated.
  resolution: 'PARTIALLY RESOLVED. ParamBench (arXiv:2508.16185) includes a Current
    Affairs subject, with Gemma3-4B achieving 70.7% and Qwen3-4B achieving 63.9% accuracy
    on this sub-domain — indicating measurable but imperfect coverage. MILU also includes
    contemporary India-specific knowledge from competitive exam sources. However,
    both are static benchmarks; no continuously updated Indian current affairs benchmark
    (analogous to the monthly current affairs role of PIB/Yojana in UPSC prep) was
    found. This is a genuine gap: static benchmarks cannot track the rapidly changing
    current-affairs domain that is central to UPSC/SSC. Source: arXiv:2508.16185 —
    [WEB-15].'
- gap_id: 8
  description: State-wise infrastructure and connectivity data for target states
  search_target: Internet penetration mobile data speed UP Bihar Rajasthan MP TRAI
    IAMAI 2024
  verification_needed: Mobile internet penetration rates, average data speeds, and
    device distribution statistics for Uttar Pradesh, Bihar, Rajasthan, and Madhya
    Pradesh.
  resolution: 'RESOLVED (penetration rates). Per IAMAI/Kantar ''Internet in India
    2024'' (ICUBE 2024, base: 886 million active internet users): Bihar internet penetration
    = 43% (bottom 3 nationally, 18% YoY growth); Uttar Pradesh internet penetration
    = 46% (bottom 3 nationally, 15% YoY growth). Rajasthan and Madhya Pradesh are
    not separately listed in bottom-3 or top-3, suggesting mid-range penetration roughly
    between 50–65%. Note: TRAI reports UP with 73.59M and Bihar with 69.89M subscribers
    (Sep 2023) — large absolute numbers but low penetration due to large populations.
    The low penetration in Bihar and UP is a significant deployment risk: a substantial
    fraction of the target population may have intermittent, shared, or no internet
    access. Source: IAMAI/Kantar Internet in India 2024 — [WEB-10];
    Business Standard — [WEB-12];
    TRAI Sep 2023 data via Wikipedia — [WEB-11].'
applicable_regulatory_and_policy_context:
  data_protection: 'RESOLVED. The Digital Personal Data Protection (DPDP) Act, 2023
    is India''s primary data privacy law. The DPDP Rules, 2025 were officially notified
    by MeitY on November 14, 2025, operationalizing the Act. The Rules introduce an
    18-month phased compliance window (full compliance expected by 13 May 2027). The
    framework applies to all digital personal data processed in India and to processing
    outside India that involves offering goods or services to Indian data principals.
    Key requirements for an EdTech AI deployment: free, specific, and informed consent
    for each data processing purpose; explicit privacy notice in plain language (must
    be available in English and all 22 Eighth Schedule languages); data erasure upon
    withdrawal of consent; for children''s data, verifiable parental consent is required
    (with limited exemptions). Penalties: up to ₹250 crore for failure to maintain
    security safeguards; up to ₹200 crore for breach notification failures. Source:
    MeitY/PIB official notification — [WEB-22];
    India-Briefing DPDP Rules 2025 — [WEB-23];
    EY India — [WEB-24].'
  education_technology_policy: 'PARTIALLY RESOLVED. NEP 2020 establishes universal
    foundational literacy and numeracy as a national mission and encourages EdTech
    integration, but does not contain AI-specific binding provisions for deployment.
    MeitY released India Artificial Intelligence Governance Guidelines on November
    5, 2025 (four days before the DPDP Rules notification), signaling a whole-of-government
    AI governance approach. A MeitY Subcommittee on AI Governance & Guidelines Development
    (established November 2023) published recommendations for public consultation
    in early 2025 emphasizing a risk-based, sector-driven framework. No EdTech-specific
    AI deployment mandate with binding force was found as of mid-2025. Source: IAPP
    Asia-Pacific Notes — [WEB-25];
    Truyo AI governance overview — [WEB-26].'
  exam_conducting_body_guidelines:
    UPSC: '[NEEDS VERIFICATION — deferred: below search budget; no UPSC official guidance
      specifically on AI-assisted coaching tools was found; UPSC regulates exam conduct
      but not private coaching/preparation tools]'
    SSC: '[NEEDS VERIFICATION — deferred: below search budget; same situation as UPSC
      — SSC regulates examination conduct, not preparation tools]'
  ai_policy_india: 'PARTIALLY RESOLVED. India''s National AI Strategy (NITI Aayog,
    2018) is the foundational document but predates current LLM deployment contexts.
    The IndiaAI Mission (launched 2024 under MeitY) is the active national AI program;
    it includes focus on AI in education and requires data anonymization for personal
    data used in AI training. MeitY''s India AI Governance Guidelines (released November
    5, 2025) provide a principles-based, activity-specific framework emphasizing transparency,
    accountability, and innovation enablement — but are not yet binding regulation.
    Source: IAPP — [WEB-25];
    Truyo — [WEB-26].'
domain_specific_notes: '- Exam syllabus: UPSC and SSC syllabi are defined documents
  published by the respective bodies. The AI''s knowledge base must be anchored to
  the current official syllabus, not MMLU''s US-academic subject taxonomy.

  - Question bank conventions: UPSC/SSC questions follow specific stylistic conventions
  (statement-based questions with ''Which of the above is/are correct?'', match-the-column,
  chronological ordering) that differ from MMLU''s predominantly direct-question format.

  - Answer key disputes: UPSC and SSC answer keys are officially released after examinations
  and are frequently contested; the AI must handle cases where standard sources conflict
  with official answer keys.

  - Hindi register: Explanatory feedback should use standard sarkari (formal government-style)
  Hindi terminology consistent with NCERT textbooks, not colloquial or regional dialect
  forms.

  - Sensitive content: Questions on caste history, religious minorities, Partition,
  and Indo-Pakistan relations require factually accurate, neutrally framed responses
  consistent with the constitutional and NCERT framework.

  - Scoring conventions: UPSC Prelims uses negative marking (−1/3 for wrong answers);
  the AI''s feedback should acknowledge uncertainty rather than confidently providing
  a wrong explanation, given the cost of incorrect answers.

  '
net_new_fields:
  hindi_llm_performance_on_upsc_domain:
    summary: 'IndicEval (arXiv:2602.16467, Feb 2026) is the first benchmark using
      authentic UPSC examination questions in both English and Hindi. Key finding:
      multilingual degradation is a critical challenge, with marked accuracy drops
      in Hindi vs. English especially under Zero-Shot conditions; LLaMA achieves only
      39.53% on UPSC Hindi Zero-Shot (vs. ~84.88% on UPSC English CoT for Gemini).
      This directly quantifies the Hindi-medium performance penalty and confirms that
      MMLU scores in English do not predict performance on Hindi UPSC content.'
    source: arXiv:2602.16467 IndicEval — [WEB-16]
  translation_artifacts_in_hindi_mmlu_variants:
    summary: Research consistently finds that translating MMLU into Hindi produces
      cultural mismatch because the underlying content (US History, law, Western philosophy)
      remains Western-specific even after translation. Back-translation quality for
      IndicMMLU-Pro Hindi achieves chrF++ above 74 (semantic preservation adequate)
      but phrasing/structural variation is documented. Critically, translation does
      not replace missing Indian-curriculum content — it merely renders Western content
      in Devanagari script.
    source: arXiv:2501.15747 IndicMMLU-Pro — [WEB-18];
      arXiv:2509.11570 survey — [WEB-20]
  milu_law_governance_performance_gap:
    summary: MILU (NAACL 2025) explicitly documents that LLMs perform poorly in culturally
      relevant areas like Arts and Humanities, and Law and Governance, compared to
      general STEM fields — even with GPT-4o at 74% average. For the NI-CEA deployment,
      where Indian Polity and Constitution is a high-priority domain, this finding
      from the most India-grounded available benchmark signals that even frontier
      models struggle on the exact content type this deployment requires.
    source: MILU NAACL 2025 — [WEB-13]; HuggingFace
      — [WEB-14]
  shared_device_access_risk:
    summary: 'IAMAI/Kantar 2024 reports 1 in 5 Indian internet users access via a
      shared device, with rural shared-device usage growing 24% YoY. This is a relevant
      deployment assumption: the AI application may be accessed on devices shared
      among multiple aspirants in a household or study group, with implications for
      session management, personalization, and data privacy (relevant to DPDP consent
      per-individual requirements).'
    source: IAMAI/Kantar Internet in India 2024 — [WEB-10];
      Business Standard — [WEB-12]
  dpdp_rules_language_requirement:
    summary: The DPDP Rules 2025 explicitly require that privacy/consent notices be
      available in English and all 22 languages of the Eighth Schedule of the Indian
      Constitution — which includes Hindi. This means the AI deployment's consent
      flow and data notices must be available in Hindi, creating a regulatory alignment
      with the deployment's Hindi-first design.
    source: Lukmaan IAS DPDP Rules 2025 analysis — [WEB-27];
      PIB official text — [WEB-22]
  women_aspirants_gender_dynamics:
    summary: Women constituted 34.4% of final UPSC selections (UPSC Annual Report
      data); female applicants grew nearly four-fold over 15 years to 3.37 lakh by
      2021–22. Female success rates in the 24–26 age band (31.9%) outperform males
      (27.1%). Online/mobile-first study material has been a documented enabler of
      women's participation in UPSC prep by reducing the need for in-person coaching
      travel. This makes the deployment's mobile-first, Hindi-language design especially
      relevant for female aspirants from conservative households.
    source: The Print — [WEB-9];
      Legacy IAS — [WEB-8]
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/abs/2410.14815 |
| WEB-2 | https://en.wikipedia.org/wiki/Literacy_in_India |
| WEB-3 | https://dhsprogram.com/pubs/pdf/FR375/FR375.pdf |
| WEB-4 | https://indiadatamap.com/2025/08/26/indias-literacy-rate-insights-for-2025/ |
| WEB-5 | https://upsc.gov.in/examinations/active-examination |
| WEB-6 | https://ssc.gov.in/ |
| WEB-7 | https://sleepyclasses.com/discover-how-many-candidates-are-selected-in-upsc-each-year/ |
| WEB-8 | https://www.legacyias.com/upsc-success-rate-2024-best-age-attempt-optional-subject-to-crack-ias/ |
| WEB-9 | https://theprint.in/india/family-support-safety-study-material-a-click-away-whats-driving-more-women-to-take-upsc-exam/1922660/ |
| WEB-10 | https://www.iamai.in/sites/default/files/research/Kantar_%20IAMAI%20report_2024_.pdf |
| WEB-11 | https://en.wikipedia.org/wiki/Internet_in_India |
| WEB-12 | https://www.business-standard.com/industry/news/india-to-exceed-900mn-internet-users-by-2025-125011600669_1.html |
| WEB-13 | https://aclanthology.org/2025.naacl-long.507/ |
| WEB-14 | https://huggingface.co/datasets/ai4bharat/MILU |
| WEB-15 | https://arxiv.org/abs/2508.16185 |
| WEB-16 | https://arxiv.org/abs/2602.16467 |
| WEB-17 | https://llm-stats.com/benchmarks/mmmlu |
| WEB-18 | https://arxiv.org/abs/2501.15747 |
| WEB-19 | https://arxiv.org/abs/2503.10497 |
| WEB-20 | https://arxiv.org/abs/2509.11570 |
| WEB-21 | https://arxiv.org/abs/2508.19831 |
| WEB-22 | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf |
| WEB-23 | https://www.india-briefing.com/news/dpdp-rules-2025-india-data-protection-law-compliance-40769.html/ |
| WEB-24 | https://www.ey.com/en_in/insights/cybersecurity/decoding-the-digital-personal-data-protection-act-2023 |
| WEB-25 | https://iapp.org/news/a/notes-from-the-asia-pacific-region-india-releases-dpdpa-rules-ai-governance-guidelines |
| WEB-26 | https://truyo.com/governing-the-ai-surge-how-india-is-writing-the-rulebook-for-responsible-ai/ |
| WEB-27 | https://blog.lukmaanias.com/2026/04/28/the-digital-personal-data-protection-dpdp-rules-2025/ |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: For a graduate student in North India preparing for competitive job exams (e.g., UPSC, SSC, state PSC, banking exams), which subject areas are most critical — General Knowledge, Current Affairs, Indian Polity & Constitution, Hindi language proficiency, regional history of North Indian states (UP, Bihar, Rajasthan, MP), or Mathematics/Reasoning? Are there specific exam types (Central vs. state-level) that your deployment must prioritize?
A1: The most critical subject areas are General Knowledge, Current Affairs, History, and Mathematics/Reasoning, with supplementary coverage of Indian Polity & Constitution and Hindi language proficiency. The deployment focuses specifically on central government examinations (UPSC, SSC, etc.) rather than state-level PSCs.

Q2 [IC]: Competitive exam questions for North Indian students often draw on culturally specific knowledge — e.g., festivals like Chhath Puja, regional administrative units like tehsils or mandals, state-specific historical figures, or North Indian legal and land-revenue traditions. Does your deployment expect the AI to handle this kind of regionally grounded content, or is the focus on pan-India general knowledge content?
A2: Central competitive examinations require both regionally grounded Indian content (including North India–specific elements) and pan-India general knowledge; the AI must handle both dimensions.

Q3 [OO]: When the AI provides feedback on a student's response, what should that feedback look like — a simple correct/incorrect label, an explanation of why an answer is right or wrong, a hint toward the correct answer, or an encouragement message in Hindi? If the benchmark only scores label accuracy, there may be a mismatch with deployment needs.
A3: The AI must produce both a correct/incorrect label and a substantive explanation of why the answer is right or wrong, and this feedback must be delivered in Hindi. A label-only benchmark output is insufficient for this deployment.

Q4 [IC]: Since the target student has limited English exposure, would it be a problem if some benchmark questions contain English technical terms, code-mixed phrasing, or assume familiarity with English-medium textbook conventions?
A4: Moderate code-mixing with English technical terms is acceptable provided it does not exceed approximately 10% of the content. Fully English-medium question phrasing or heavy reliance on English-medium academic conventions would be a problem.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MMLU's 57 subjects are anchored in a US academic curriculum and contain no coverage of Indian Polity, Indian History, Current Affairs relevant to India, or Hindi language proficiency — the exact domains that central competitive exams prioritise. |
| IC | HIGH | Individual MMLU items embed US-default factual and cultural assumptions (US law, US history, Western civic norms) that are directly irrelevant or misleading for an Indian competitive-exam context requiring both pan-India and North India–specific knowledge. |
| IF | HIGH | MMLU is entirely in English, while the deployment requires Hindi-medium interaction with at most ~10% English code-mixing; the script and language distribution of benchmark inputs do not match deployment reality. |
| OO | HIGH | MMLU scores label accuracy only (A/B/C/D MCQ), whereas the deployment requires the model to produce a correct/incorrect verdict plus a Hindi-language explanatory rationale — a fundamentally different output taxonomy. |
| OC | HIGH | MMLU ground-truth labels were validated by English-speaking, US-educated annotators; for Indian GK, Polity, and regional history items that MMLU does not contain, there is no representative Indian annotator pool, making label correctness for an India-centric use case unverifiable. |
| OF | MODERATE | Both MMLU and the deployment use text-based MCQ as the input vehicle, which is a partial match; however, MMLU's label-only output form diverges from the required Hindi explanatory-feedback output, raising external validity concerns at the output side. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** cais/mmlu
**Analysis date:** 2025-01-30
**Examples reviewed:** ~200 examples across 57 subject configs (5–6 examples per config)
**Columns shown:** question, subject, choices, answer
**Columns skipped (media):** none (text-only dataset)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | high_school_government_and_politics | Ex.1 | A | "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" | US constitutional law question — irrelevant to Indian Polity | IO, IC |
| D2 | high_school_government_and_politics | Ex.4 | D | "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" | US Congress-specific legislation — not Indian constitutional content | IO, IC |
| D3 | high_school_government_and_politics | Ex.5 | A | "What power was granted to the states by the Articles of Confederation but not by the Constitution?" | US Articles of Confederation — no Indian Polity equivalent | IO, IC |
| D4 | high_school_us_history | Ex.2 | B | "John C. Calhoun, 'South Carolina Exposition and Protest,' 1828 … The language of 'protest' that Calhoun used … was similar to the language of which of the following political positions?" | US history question with primary source passage — entirely irrelevant to Indian History | IO, IC |
| D5 | high_school_us_history | Ex.4 | D | "Between 1820 and 1854, the greatest number of immigrants to the United States came from … Ireland" | US immigration history — no relevance to Indian competitive exams | IO, IC |
| D6 | high_school_us_history | Ex.5 | A | "Tonight, the daughter of an immigrant from Italy has been chosen to run for (vice) president … — Geraldine Ferraro, Vice Presidential Nomination Acceptance Address, July 19, 1984" | US political history primary source — alien to UPSC/SSC syllabus | IO, IC |
| D7 | us_foreign_policy | Ex.2 | B | "Why might the 'Philadelphian System' be linked to the idea of American exceptionalism?" | US foreign policy / exceptionalism — irrelevant to Indian deployment | IO, IC |
| D8 | us_foreign_policy | Ex.3 | C | "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" | US Cold War policy — no analogue in UPSC/SSC syllabus | IO, IC |
| D9 | us_foreign_policy | Ex.4 | D | "In American government, the power to declare war rests with … Congress" | US government structure question — not Indian Polity | IO, IC |
| D10 | professional_law | Ex.1 | A | "A truck driver was assigned to drive a huge tractor-trailer loaded with logs … the girl's parents … assert a claim against the lumber company" | US tort law scenario — calibrated against US bar exam, not Indian law | IO, IC |
| D11 | professional_law | Ex.2 | B | "An avid baseball fan … forwarded the club a $50 registration deposit … In a restitutionary action, can the executor of the fan's estate … recover … the $2,500 paid to the club?" | US contract law with baseball cultural context — no Indian law equivalent | IO, IC |
| D12 | high_school_european_history | Ex.1 | A | "The Scribbling-Machines have thrown thousands of your petitioners out of employ … Leeds Woolen Workers Petition, 1786" | British Industrial Revolution primary source — European history with no South Asian content | IO, IC |
| D13 | high_school_european_history | Ex.2 | B | "What is tolerance? … Of all religions, the Christian ought doubtless to inspire the most tolerance … Voltaire, Letters on the English Nation, 1733" | Enlightenment Western philosophy — Western canon, irrelevant to Indian History syllabus | IO, IC |
| D14 | high_school_european_history | Ex.4 | D | "The substitution of Plato for the scholastic Aristotle … Cosimo and Lorenzo de Medici … the Florentine Academy … Neoplatonism" | Italian Renaissance intellectual history — no Indian History coverage | IO, IC |
| D15 | high_school_world_history | Ex.2 | B | "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters … William Howard Russell, My Indian Mutiny Diary, 1860" | 1857 Indian Mutiny from British colonial perspective — if Indian History content appears, it is filtered through colonial framing | IO, IC, OC |
| D16 | philosophy | Ex.1 | A | "According to Parfit, the obligation to give priority to the welfare of one's children is: agent-relative." | Western analytic philosophy (Parfit) — not covered in UPSC/SSC philosophy or ethics sections | IO, IC |
| D17 | philosophy | Ex.2 | B | "Anscombe claims that on Sidgwick's view, the badness of an action must be estimated in light of: its expected consequences." | Western analytic moral philosophy (Sidgwick, Anscombe) — entirely Western canonical tradition | IO, IC |
| D18 | moral_scenarios | Ex.1 | A | "according to ordinary moral standards in the US as of 2020? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot." | Explicitly US-framed moral norms — normative grounding is US-specific | OC, IC |
| D19 | moral_scenarios | Ex.2 | B | "according to ordinary moral standards in the US as of 2020? Scenario 1 | When I went through the road block I gave the policeman my brothers ID." | Again explicitly references US 2020 moral standards — non-transferable to Indian cultural context | OC, IC |
| D20 | human_aging | Ex.3 | C | "The age at which one can receive full benefits from social security … Has been increasing" | US Social Security system — irrelevant to Indian context | IC |
| D21 | human_sexuality | Ex.1 | A | "Which of the following is the most common method of birth control for married couples in the U.S." | Explicitly US-specific demographic question | IC |
| D22 | high_school_geography | Ex.1 | A | "What is the most rapidly growing religion in the United States today? … Islam" | US religion demographics — not Indian Geography content | IO, IC |
| D23 | global_facts | Ex.2 | B | "As of 2017, what fraction of the population in India used the internet in the past three months? … 26%" | One of very few India-referencing questions — but tests dated Western-sourced statistical trivia, not Indian GK curriculum | IC |
| D24 | global_facts | Ex.4 | D | "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … in their country makes it a better place to live … 68%" | India-referencing global survey question — but sourced from Pew/Western pollsters, not Indian exam curriculum | IC |
| D25 | elementary_mathematics | Ex.1 | A | "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel? … 120 miles" | Uses miles (US customary unit) — Indian exams use km; creates construct-irrelevant variance | IC, IF |
| D26 | elementary_mathematics | Ex.5 | A | "A zoo has 15 toucans and 60 parrots. What is the ratio of the number of toucans to the number of parrots at the zoo? … 1:04" | Basic arithmetic ratio — language-neutral content applicable across curricula | IO |
| D27 | high_school_mathematics | Ex.1 | A | "Juan rolls a fair regular octahedral die … What is the probability that the product of the two rolls is a multiple of 3?" | Probability question — content universally applicable regardless of cultural context | IO |
| D28 | college_mathematics | Ex.2 | B | "A total of x feet of fencing is to form three sides of a level rectangular yard. What is the maximum possible area of the yard, in terms of x?" | Uses feet (US customary unit) — minor but consistent US measurement convention | IC |
| D29 | college_computer_science | Ex.2 | B | "Let G = (V, E) be a connected, undirected graph … P_1 can be solved in polynomial time but P_2 is not known to be solvable in polynomial time." | Algorithm complexity theory — culturally neutral STEM content | IO |
| D30 | abstract_algebra | Ex.1 | A | "Find the characteristic of the ring Z_3 x 3Z." | Abstract mathematics — entirely culture-independent | IO |
| D31 | high_school_statistics | Ex.4 | D | "The Hardcore Construction Company has two offices, one in Atlanta and one in New Orleans … Is the 2-sample t-test an appropriate inferential technique?" | Statistical reasoning with US city names as context — content sound but culturally anchored | IC |
| D32 | professional_accounting | Ex.1 | A | "Which of the following procedures does a CPA usually perform when reviewing the financial statements of a nonissuer?" | US CPA (Certified Public Accountant) professional standards — not relevant to Indian accounting exams | IO, IC |
| D33 | jurisprudence | Ex.1 | A | "Bill purchased a can of Sipep from the Ajax Minimart … In a strict product liability tort action against Ajax, Bill must prove …" | US-style product liability tort — uses American legal framework | IC |
| D34 | high_school_world_history | Ex.4 | D | "Kwame Nkrumah, Neo-Colonialism, 1965 … Which of the following most inspired the national plan advanced by Nkrumah in the second paragraph? … Socialism" | Global post-colonial history — partial relevance to Indian modern history via decolonisation themes | IO |
| D35 | world_religions | Ex.2 | B | "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" | Jainism question — one of very few South Asian religious/cultural references in the entire sample | IO, IC |
| D36 | world_religions | Ex.4 | D | "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" | Jainism sect distinction — rare South Asian content, but not an Indian competitive exam priority topic | IO, IC |
| D37 | high_school_psychology | Ex.1 | A | "Jyoti notes the behavior of people as they wait in line for tickets to rock concerts." | Uses Indian name 'Jyoti' but the context is rock concerts (Western cultural setting) — surface-level name inclusion without substantive cultural relevance | IC |
| D38 | auxiliary_train | Ex.1 | A | "Jim watched a liquor store furtively … On a charge of burglary, Jim's best defense would be that … the liquor store was open to the public." | US criminal law (burglary statute) — entirely US legal framework | IO, IC |
| D39 | high_school_macroeconomics | Ex.2 | B | "A nation that must consistently borrow to cover annual budget deficits risks … a decline in net exports as the nation's goods become more expensive to foreign consumers." | General macroeconomic principle — applicable cross-culturally | IO |
| D40 | conceptual_physics | Ex.4 | D | "A wave transfers … energy" | Basic physics principle — universally applicable | IO |
| D41 | high_school_biology | Ex.2 | B | "The sequence of amino acids in hemoglobin molecules of humans is more similar to the hemoglobin of chimpanzees than it is to the hemoglobin of dogs." | Biology/evolution — curriculum-neutral STEM content | IO |
| D42 | virology | Ex.1 | A | "Viruses have encouraged us to change our world, as we have now: Eradicated smallpox" | General science fact — applicable to Indian science GK | IO |
| D43 | international_law | Ex.1 | A | "Which of the following is a treaty-based human rights mechanism? … The UN Human Rights Committee" | International law — partially relevant to UPSC GS II but framed from Western international law perspective | IO |
| D44 | prehistory | Ex.2 | B | "The origins of Chinese civilization can be traced to: chiefdoms and states in numerous regions throughout China." | World history/prehistory — no South Asian prehistoric content visible | IO |
| D45 | miscellaneous | Ex.1 | A | "A flashing red traffic light signifies that a driver should do what? … stop" | US traffic law convention — minor but US-specific | IC |
| D46 | business_ethics | Ex.5 | A | "civil society … in many other countries, such as Russia and China … far less developed than in, for instance, Britain" | Western-centric framing of civil society — India not mentioned as reference | IC |
| D47 | high_school_world_history | Ex.2 | B | "the deed was done by a subject race — by black men who dared to shed the blood of their masters … British journalist William Howard Russell" | 1857 mutiny through British colonial journalist's lens — if Indian content appears at all in MMLU, it is through a colonial/Western perspective | OC, IC |
| D48 | college_medicine | Ex.4 | D | "When preparing for the MCAT exam, a student begins studying electrochemical cells." | References MCAT (US Medical College Admission Test) — US-specific academic context | IC |
| D49 | high_school_statistics | Ex.5 | A | "As reported on CNN, in a May 1999 national poll 43% of high school students expressed fear about going to school." | CNN/US-specific polling context — not Indian curriculum content | IC |
| D50 | security_studies | Ex.1 | A | "In what ways do theories of conventional and critical social constructivism differ?" | IR theory — Western academic framing; partial relevance to UPSC GS II international relations | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Four-option MCQ format structurally matches competitive exam format
- **Dimension(s):** IF
- **Observation:** Every question in MMLU uses a four-option multiple-choice structure (A/B/C/D) with one correct answer and three distractors, which is the identical format used in UPSC Prelims, SSC CGL, and banking exams. The `choices` field consistently contains exactly four options across all 57 subjects sampled.
- **Deployment relevance:** The MCQ format is a genuine structural match, meaning that any component of MMLU used in a format-compatibility test would not introduce format-induced performance variance from input encoding differences.
- **Datapoint citations:**
  - [D26] Example 5 (elementary_mathematics, split=test, label=A): "A zoo has 15 toucans and 60 parrots. What is the ratio of the number of toucans to the number of parrots at the zoo? (A) 1:04 (B) 1:05 (C) 4:01 (D) 4:05" — standard four-option MCQ format identical to Indian competitive exam structure.
  - [D40] Example 4 (conceptual_physics, split=test, label=D): "A wave transfers (A) amplitude (B) wavelength (C) frequency (D) energy" — clean four-option format applicable regardless of deployment context.

#### Strength 2: Culturally neutral STEM content (mathematics, physics, computer science) provides partial proxy signal
- **Dimension(s):** IO
- **Observation:** A substantial fraction of MMLU's items — particularly abstract algebra, college/high school mathematics, conceptual physics, college computer science, and formal logic — contain questions whose correctness is independent of cultural or geographic framing. These items test skills (arithmetic, reasoning, algorithm analysis, probability) that overlap with the quantitative aptitude and reasoning sections of SSC CGL and UPSC Prelims CSAT.
- **Deployment relevance:** For the deployment's Mathematics/Reasoning priority domain, these items constitute a weak but non-zero signal about model competence. UPSC CSAT Paper II and SSC CGL quantitative aptitude share conceptual overlap with MMLU's elementary and college mathematics items.
- **Datapoint citations:**
  - [D27] Example 1 (high_school_mathematics, split=test, label=A): "Juan rolls a fair regular octahedral die marked with the numbers 1 through 8. Then Amal rolls a fair six-sided die. What is the probability that the product of the two rolls is a multiple of 3?" — probability question applicable cross-culturally.
  - [D30] Example 1 (abstract_algebra, split=test, label=A): "Find the characteristic of the ring Z_3 x 3Z." — pure mathematics, culturally neutral.
  - [D29] Example 2 (college_computer_science, split=test, label=B): "P_1 can be solved in polynomial time but P_2 is not known to be solvable in polynomial time." — algorithm complexity, universally applicable.

#### Strength 3: Broad label balance across answer classes
- **Dimension(s):** OF
- **Observation:** Across sampled configs, the distribution of correct answers (A/B/C/D) is reasonably balanced. Buffer counts show roughly 22–31% per class in most subjects, with no systematic bias toward any single letter. This prevents position-bias artifacts from contaminating aggregate accuracy scores.
- **Deployment relevance:** For any comparative evaluation of models on the subset of MMLU items with partial relevance (STEM), balanced answer distribution reduces the risk that accuracy gains reflect position-bias rather than genuine knowledge.
- **Datapoint citations:**
  - [D26] elementary_mathematics buffer: A=79, B=97, C=101, D=101 (n=378) — reasonable balance across four classes.
  - [D27] high_school_mathematics buffer: A=57, B=71, C=71, D=71 (n=270) — no dominant label class.

#### Strength 4: Science and biology content overlaps with Indian GK science sections
- **Dimension(s):** IO
- **Observation:** MMLU's high school biology, college biology, virology, medical genetics, and conceptual physics items cover topics (genetics, evolution, cell biology, basic physics principles) that partially overlap with Indian Class 10–12 NCERT science content tested in UPSC/SSC GK sections. These are not India-specific but are curriculum-neutral science facts.
- **Deployment relevance:** UPSC Prelims General Studies Paper I and SSC CGL GK sections include NCERT-level science questions. MMLU's science content provides weak-but-positive signal in this subdomain.
- **Datapoint citations:**
  - [D41] Example 2 (high_school_biology, split=test, label=B): "The sequence of amino acids in hemoglobin molecules of humans is more similar to the hemoglobin of chimpanzees than it is to the hemoglobin of dogs. This similarity suggests that humans and chimpanzees are more closely related than humans and dogs" — evolution content appearing in NCERT Biology Class 12.
  - [D42] Example 1 (virology, split=test, label=A): "Viruses have encouraged us to change our world, as we have now: Eradicated smallpox" — general science fact tested in Indian GK sections.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Complete absence of Indian Polity, Indian History, and Indian Geography — the core UPSC/SSC subject domains
- **Dimension(s):** IO
- **Observation:** Across all 57 MMLU subject configs and the full sample of ~200 examples, not a single question addresses Indian constitutional law, Panchayati Raj, Indian administrative structures, Indian ancient/medieval/modern history, or Indian physical/political geography. The government and politics config covers exclusively US government. The history configs cover European and US history. No config maps to any of the five priority subject domains in the Indian competitive exam syllabus.
- **Deployment relevance:** Indian Polity and Constitution, Indian History, and Indian Geography are high-priority domains for UPSC Prelims GS Paper I and SSC GK. MMLU provides zero items for these domains. A model achieving high MMLU accuracy could score near-random on UPSC/SSC Indian Polity questions, and MMLU accuracy would provide no predictive information about this.
- **Datapoint citations:**
  - [D1] Example 1 (high_school_government_and_politics, split=test, label=A): "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" — US First Amendment, not Indian constitutional rights.
  - [D3] Example 5 (high_school_government_and_politics, split=test, label=A): "What power was granted to the states by the Articles of Confederation but not by the Constitution?" — US Articles of Confederation, no Indian Polity equivalent.
  - [D4] Example 2 (high_school_us_history, split=test, label=B): "John C. Calhoun, 'South Carolina Exposition and Protest,' 1828 … was similar to the language of which of the following political positions?" — US antebellum history, irrelevant to Indian History syllabus.
  - [D12] Example 1 (high_school_european_history, split=test, label=A): "The Scribbling-Machines have thrown thousands of your petitioners out of employ … Leeds Woolen Workers Petition, 1786" — British Industrial Revolution, no South Asian historical content.

#### Concern 2: All benchmark inputs are in English — zero Hindi or Devanagari content
- **Dimension(s):** IF
- **Observation:** Every single question, answer option, and subject label in the sampled data is in English. The HF metadata confirms `languages: [en]` and `multilinguality: monolingual`. There is no Devanagari script, no Hindi vocabulary, no code-mixed text, and no variant closer to the deployment's required input register (Hindi-dominant with ≤10% English).
- **Deployment relevance:** The deployment requires Hindi-medium interaction. A model's MMLU accuracy measured on English-medium questions provides no evidence whatsoever about its capacity to comprehend Hindi-dominant or Devanagari-script inputs. IndicEval (arXiv:2602.16467) demonstrates a catastrophic Hindi-medium performance penalty: LLaMA achieves only 39.53% on UPSC Hindi Zero-Shot vs. ~84.88% for Gemini on UPSC English CoT. MMLU scores cannot predict this gap.
- **Datapoint citations:**
  - [D10] Example 1 (professional_law, split=test, label=A): "A truck driver was assigned to drive a huge tractor-trailer loaded with logs…" — English-medium, no Hindi content.
  - [D25] Example 1 (elementary_mathematics, split=test, label=A): "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel?" — English-only phrasing, uses US customary units.
  - [D30] Example 1 (abstract_algebra, split=test, label=A): "Find the characteristic of the ring Z_3 x 3Z." — English-only mathematical notation.

#### Concern 3: Output structure is label-only (A/B/C/D) — no Hindi explanatory feedback evaluated
- **Dimension(s):** OO, OF
- **Observation:** Every MMLU example in the dataset has a single scalar `answer` field (ClassLabel 0–3 corresponding to A–D). The benchmark evaluates only whether a model selects the correct letter. There is no field for rationale, explanation, or free-form text output. The benchmark structure makes it architecturally impossible to assess a model's capacity to generate Hindi-language explanatory feedback.
- **Deployment relevance:** The deployment's core output requirement is a substantive Hindi-language explanation of why an answer is correct or incorrect, delivered in standard Manak Hindi register. MMLU accuracy scores provide zero signal on this output dimension. A model could achieve 90% MMLU accuracy while generating incoherent or factually wrong Hindi explanations — or no Hindi output at all.
- **Datapoint citations:**
  - [D1] Schema (all configs): `answer: ClassLabel(4 classes)` with label_names `["A", "B", "C", "D"]` — confirms label-only output structure with no rationale field.
  - [D18] Example 1 (moral_scenarios, split=test, label=A): "Wrong, Wrong" — a two-word answer label; the benchmark evaluates this binary classification with no mechanism for explanatory text.
  - [D26] Example 5 (elementary_mathematics, split=test, label=A): answer=0 (A) — single integer label, no explanation field present.

#### Concern 4: Ground-truth labels reflect US moral and legal norms — not Indian stakeholder perspectives
- **Dimension(s):** OC
- **Observation:** The `moral_scenarios` config explicitly frames every question as measuring "ordinary moral standards in the US as of 2020." The `professional_law` and `high_school_government_and_politics` configs test US legal standards. All labels were validated against US-standard answer keys by US university students. No Indian subject-matter experts, UPSC/SSC exam specialists, or Hindi-medium educators participated in any documented annotation process.
- **Deployment relevance:** For any India-centric GK, Polity, or History question, the US-annotator validation chain is entirely non-representative. More immediately, the moral_scenarios items could produce systematically different correct answers under Indian cultural norms vs. US norms, undermining OC validity for the target population.
- **Datapoint citations:**
  - [D18] Example 1 (moral_scenarios, split=test, label=A): "according to ordinary moral standards in the US as of 2020? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot. Scenario 2 | I popped the ball…" — the explicit US 2020 moral framing makes these labels non-transferable to Indian cultural context.
  - [D19] Example 2 (moral_scenarios, split=test, label=B): "according to ordinary moral standards in the US as of 2020? Scenario 1 | When I went through the road block I gave the policeman my brothers ID." — US legal/moral norm (impersonation at a roadblock) may be evaluated differently under Indian law and social norms.
  - [D15] Example 2 (high_school_world_history, split=test, label=B): "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters … William Howard Russell" — the single instance of 1857 Indian content appears through a colonial British journalist's framing; the correct answer label privileges a colonial historiographic perspective that conflicts with the Indian NCERT/Bipin Chandra narrative taught in Indian competitive exam preparation.

#### MAJOR

#### Concern 5: US-specific cultural assumptions embedded throughout non-STEM items
- **Dimension(s):** IC
- **Observation:** Items across business ethics, human sexuality, human aging, high school geography, marketing, and miscellaneous configs embed US-specific institutional assumptions, demographic statistics, legal conventions, and cultural referents. This is not limited to history or law — it pervades even ostensibly "general" subjects.
- **Deployment relevance:** For a Hindi-medium aspirant from North India, these culturally embedded assumptions constitute construct-irrelevant variance that would depress performance on items even where the underlying conceptual knowledge might be present. More critically, correct answers rely on US-specific factual knowledge that is not part of any Indian competitive exam syllabus.
- **Datapoint citations:**
  - [D20] Example 3 (human_aging, split=test, label=C): "The age at which one can receive full benefits from social security … Has been increasing" — requires knowledge of US Social Security policy; irrelevant to Indian GK.
  - [D21] Example 1 (human_sexuality, split=test, label=A): "Which of the following is the most common method of birth control for married couples in the U.S." — US-specific demographic question; not part of any Indian exam syllabus.
  - [D22] Example 1 (high_school_geography, split=test, label=A): "What is the most rapidly growing religion in the United States today? … Islam" — US religion demographics; Indian Geography covers entirely different content.
  - [D45] Example 1 (miscellaneous, split=test, label=A): "A flashing red traffic light signifies that a driver should do what? … stop" — US traffic law convention; Indian traffic law uses different conventions.
  - [D48] Example 4 (college_medicine, split=test, label=D): "When preparing for the MCAT exam, a student begins studying electrochemical cells." — MCAT is a US-specific standardized test, adding irrelevant institutional framing.

#### Concern 6: Indian content appears only through colonial/Western framing — not from Indian standpoint
- **Dimension(s):** IC, OC
- **Observation:** In the entire sample, the only substantive reference to Indian history occurs in a high_school_world_history example quoting British journalist William Howard Russell's description of the 1857 Sepoy Mutiny/First War of Independence using derogatory racialized colonial language ("a subject race," "black men who dared to shed the blood of their masters"). This colonial framing is antithetical to the Indian nationalist historiography (Bipin Chandra, NCERT textbooks) that UPSC/SSC aspirants study.
- **Deployment relevance:** If this item were used to evaluate a model for the Indian deployment, a model producing an explanation aligned with NCERT's framing of 1857 as the First War of Independence would likely score lower against MMLU's label (which privileges the passage's colonial interpretation). This creates direct OC misalignment for the target population.
- **Datapoint citations:**
  - [D15] Example 2 (high_school_world_history, split=test, label=B): "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters, and that of poor helpless ladies and children … British journalist William Howard Russell, My Indian Mutlny Diary, 1860" — colonial framing of 1857 event; the correct answer ("can be viewed as a reaction to the systemic brute force with which the British governed India") is framed through a second passage by Indian historian Mukherjee, but the question architecture and answer validation remain within a Western academic framework.
  - [D47] Same datapoint — "Violence, it must be emphasized, was an essential component of the British presence in India … Rudrangshu Mukherjee, 'The Kanpur [Cawnpore] Massacres in India in the Revolt of 1857,' 1990" — even the Indian historiographic passage is filtered through a comparative literature framework rather than UPSC's standard national history framing.

#### Concern 7: US customary measurement units appear in mathematics items — potential construct-irrelevant variance
- **Dimension(s):** IC
- **Observation:** Several mathematics and physics items use US customary units (miles, feet, pounds) rather than SI/metric units used in India. Indian competitive exam mathematics uses exclusively metric/SI units and Indian-context word problems.
- **Deployment relevance:** While the mathematical reasoning tested is identical, the appearance of "miles per hour" or "feet of fencing" introduces culturally unfamiliar unit terminology that could create construct-irrelevant difficulty for Hindi-medium aspirants less familiar with US measurement conventions.
- **Datapoint citations:**
  - [D25] Example 1 (elementary_mathematics, split=test, label=A): "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel? … 120 miles" — uses miles; Indian exam arithmetic problems use km/h.
  - [D28] Example 2 (college_mathematics, split=test, label=B): "A total of x feet of fencing is to form three sides of a level rectangular yard. What is the maximum possible area of the yard, in terms of x?" — uses feet; Indian exams use metres.

#### Concern 8: Professional law and accounting items test US-jurisdiction-specific professional standards
- **Dimension(s):** IO, IC
- **Observation:** The `professional_law`, `professional_accounting`, and `jurisprudence` configs contain items that require knowledge of US bar exam standards, US CPA professional conduct rules, and US tort/contract law doctrine. These are inapplicable to Indian competitive exams, which test Indian constitutional law, Indian Evidence Act, Indian Contract Act, and Indian administrative law.
- **Deployment relevance:** These configs constitute dead weight for the deployment — not only do they test irrelevant content, but a model optimized for MMLU professional law performance would be specifically tuned to US legal concepts that directly conflict with Indian legal doctrine (e.g., US "strict product liability" vs. Indian Consumer Protection Act standards).
- **Datapoint citations:**
  - [D10] Example 1 (professional_law, split=test, label=A): "A truck driver was assigned to drive a huge tractor-trailer loaded with logs … the girl's parents … assert a claim against the lumber company" — US tort scenario.
  - [D32] Example 1 (professional_accounting, split=test, label=A): "Which of the following procedures does a CPA usually perform when reviewing the financial statements of a nonissuer?" — US CPA standards, not ICAI (Indian CA) standards.
  - [D33] Example 1 (jurisprudence, split=test, label=A): "Bill purchased a can of Sipep from the Ajax Minimart … In a strict product liability tort action against Ajax, Bill must prove … Ajax is a merchant selling Sipep." — US product liability doctrine.

#### MINOR

#### Concern 9: Surface-level Indian name inclusion without substantive Indian cultural relevance
- **Dimension(s):** IC
- **Observation:** One high_school_psychology example uses the Indian name "Jyoti" in an otherwise Western cultural context (waiting in line for rock concert tickets). This is cosmetic name inclusion that does not constitute genuine India-relevant content.
- **Deployment relevance:** Superficial name substitution without cultural grounding could create a misleading appearance of Indian-context coverage. It does not address any of the actual cultural or content gaps.
- **Datapoint citations:**
  - [D37] Example 1 (high_school_psychology, split=test, label=A): "Jyoti notes the behavior of people as they wait in line for tickets to rock concerts. Which of the following research methods is she using?" — Indian name in a rock concert queue context that is culturally foreign to North Indian aspirants.

#### Concern 10: Rare South Asian religious content (Jainism) present but not aligned with Indian competitive exam priorities
- **Dimension(s):** IO
- **Observation:** Two world_religions items address Jainism specifically — a South Asian religion. This constitutes the clearest South Asian content in the entire sample. However, Jainism represents a minor sub-topic in UPSC/SSC world religions coverage, and the framing is from an academic world religions perspective rather than the NCERT/competitive exam curriculum perspective.
- **Deployment relevance:** While these items demonstrate that MMLU is not entirely devoid of South Asian religious content, their presence does not constitute meaningful coverage of the Indian religions (Hinduism, Buddhism, Jainism, Sikhism) as taught in UPSC GS Paper I Indian Culture section, where the emphasis is on philosophical schools, texts, and historical development within the Indian context.
- **Datapoint citations:**
  - [D35] Example 2 (world_religions, split=test, label=B): "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" — Jainism content, but framed as generic world religions trivia rather than Indian cultural history.
  - [D36] Example 4 (world_religions, split=test, label=D): "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" — Jain sect distinction, minor sub-topic in Indian competitive exam coverage.

#### Concern 11: Global Facts config contains India-referencing items but tests Western-sourced statistical trivia rather than Indian GK curriculum
- **Dimension(s):** IC
- **Observation:** Two global_facts examples reference India — one on internet usage (2017 data) and one on attitudes toward diversity (2018 Pew data). These are not items drawn from Indian GK curriculum sources (PIB, Economic Survey, Census of India) but from international polling organizations using Western survey methodologies.
- **Deployment relevance:** The content format differs from UPSC/SSC GK questions, which draw on official Indian government sources. A model tuned on MMLU global facts would learn to cite Pew/Gallup statistics rather than National Sample Survey Office (NSSO) or Census of India data that appears in competitive exam questions.
- **Datapoint citations:**
  - [D23] Example 2 (global_facts, split=test, label=B): "As of 2017, what fraction of the population in India used the internet in the past three months? … 26%" — Pew Research sourced India statistic; UPSC GK uses TRAI/IAMAI data.
  - [D24] Example 4 (global_facts, split=test, label=D): "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … in their country makes it a better place to live … 68%" — Pew global attitudes survey; not a standard UPSC/SSC GK source format.

---

### Content Coverage Summary

The sampled data confirms MMLU as a coherent, well-structured benchmark anchored entirely in an English-language, US/Western academic tradition. Subject coverage across 57 configs is internally consistent: mathematics and STEM items are culturally neutral; humanities and social science items are systematically US- or Western-centric; professional items (law, accounting, medicine) are calibrated to US professional licensing standards. The benchmark spans genuine breadth in its intended domain but has no subject track — and produces no individual item in the sample — that addresses Indian Polity, Indian History, Indian Geography, Hindi language proficiency, or Current Affairs relevant to India.

The most striking finding from direct content examination is the near-total absence of South Asian content: two Jainism questions in world_religions, one colonial-framed 1857 Mutiny question in world_history, and two Pew-data India-statistic questions in global_facts constitute the entirety of India-referencing content across approximately 200 sampled items. Where India does appear (D15, D47), it is filtered through a Western/colonial academic lens incompatible with the NCERT-aligned nationalist historiography that Indian competitive exam aspirants study.

The language register throughout is formal academic English. Questions range from terse (conceptual_physics, elementary_mathematics) to lengthy multi-paragraph primary-source readings (high_school_european_history, high_school_us_history, high_school_world_history). None of the inputs contains any Devanagari script, Hindi vocabulary, or code-mixed phrasing. The output structure is universally a single integer (0–3) representing the correct answer letter, with no rationale field.

---

### Limitations

1. **Sample size per config:** With 5–6 examples per config, coverage within each subject is limited. Rare India-relevant items within a config (if any exist) may not have appeared in the sample. The absence of South Asian content in the sample is consistent with but not a mathematical proof of complete absence across all 14,079 test items.

2. **Auxiliary train split not fully analyzed:** The auxiliary_train config (professional law focus) was sampled with only 5 examples and confirms US legal content, but its full 1.6M+ legal case summary content was not inspectable.

3. **Hindi translation variants not in scope:** This analysis covers only the original English cais/mmlu dataset. Community-translated Hindi MMLU variants (OpenAI MMMLU, IndicMMLU-Pro) were not sampled and their quality cannot be assessed from this data.

4. **Output quality unverifiable from dataset alone:** The label-only output structure means that any assessment of Hindi explanatory feedback quality must come from external model evaluation, not from the benchmark data itself.

5. **Moral scenarios cultural equivalence unverifiable at scale:** The moral_scenarios config explicitly invokes US 2020 moral standards. Whether the correct answers would align with Indian stakeholder judgments requires systematic cross-cultural annotation that cannot be inferred from reading examples alone.

6. **World religions coverage of Hinduism/Buddhism:** Only 6 world_religions items were sampled. The config may contain more South Asian religious content not captured in the sample, though the subject taxonomy and scoring would still reflect academic comparative religion rather than UPSC Indian Culture curriculum framing.

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
  "benchmark": "mmlu",
  "region": "North India Competitive Exam Aspirants (Hindi-Medium)",
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
