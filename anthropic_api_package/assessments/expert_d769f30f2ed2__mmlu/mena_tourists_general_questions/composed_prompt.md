I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **Measuring Massive Multitask Language Understanding** is valid for use in **Non-Arab Tourists and Expats in Eight Arab Countries**.

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
- **Domain**: General academic knowledge and problem-solving (multitask LLM evaluation)
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2021

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### 1. Input Ontology
MMLU covers 57 subjects spanning STEM, humanities, social sciences, and other areas [Q4],
organized around Western academic curricula rather than regional or cultural taxonomies [Q17].
Humanities subjects include law, philosophy, history, and moral reasoning [Q37], while social
sciences include economics, sociology, politics, geography, and psychology [Q43]. The history
coverage nominally spans "a wide range of time periods and geographical locations, including
prehistory" [Q41], but appended example questions — ranging from US tax law [Q164] to US bar
examination scenarios [Q165] to US Foreign Policy [Q169] — confirm that the taxonomy is
anchored in US and European institutional contexts. The benchmark also covers more esoteric
topics such as security studies [Q45] and world religions [Q171], but no subject category is
dedicated to Arab history, Middle Eastern geography, or Arabic language. The claim that the
benchmark covers "topics that humans are incentivized to learn" [Q17] implicitly treats a
US academic curriculum as universal, creating a structural Input Ontology gap for any
Arab-region deployment. The benchmark's self-described breadth — "greater breadth and depth
than previous benchmarks" [Q90] — does not translate into Arab-region subject coverage.

### 2. Input Content
Questions were manually collected by graduate and undergraduate students from freely available
online sources [Q23], specifically including practice materials for US standardized tests such
as the GRE and USMLE [Q24], undergraduate course materials, and Oxford University Press
publications [Q25]. Supplementary data for the Professional Law subject came from approximately
2,000 additional US law training examples [Q83] and 1.6 million legal case summaries from
Harvard's Law Library [Q85]. The assumption underlying data collection is that models learn
from "massive text corpora including educational books and websites" [Q18], with benchmarking
probing that pretraining knowledge directly [Q72, Q73]. Most questions came from PDFs or
websites where questions and answers appear on separate pages [Q112], reducing contamination
risk but also confirming that all identified source types are products of Anglophone Western
academic institutions. No sources from Arab educational systems, regional universities,
Arabic-language curricula, or Middle Eastern publishing houses are identified anywhere in the
paper. The benchmark's example questions throughout the appendix (Q120–Q171) are overwhelmingly
anchored in US and European academic contexts with no example drawn from Arab history, Islamic
jurisprudence, regional geography, or Arabic linguistics.

### 3. Input Form
The benchmark is exclusively text-based and English-only [Q71], operating in zero-shot and
few-shot settings with four-option multiple-choice questions [Q3, Q27]. GPT-3 prompts follow
a standardized English-language format ending with "Answer: " and are scored on token
probabilities for "A," "B," "C," and "D" [Q56]. UnifiedQA uses a normalized, lowercased
input format [Q104], and sensitivity to minor formatting changes — such as removing a
separator token — can cause multi-percentage-point accuracy swings [Q105], indicating
brittleness to form variation. The authors explicitly note that "many important concepts are
conveyed mainly through other modalities" [Q70] but confine the benchmark to text-only tasks
due to the limitations of evaluated models [Q71]. Question length is not strongly predictive
of difficulty [Q108], and the evaluation format is not identical to the format in which
information is acquired during pretraining [Q76]. For the Arab-region deployment, the
English-only constraint is a moderate concern: the primary interaction language is English,
but Arabic-learning users who prompt in Arabic cannot be evaluated by MMLU at all.

### 4. Output Ontology
The output label schema is a single-answer four-option multiple-choice format (A, B, C, D),
with some subjects further stratified by difficulty level — "Elementary," "High School,"
"College," or "Professional" [Q26]. Performance is measured as classification accuracy across
all examples and tasks [Q49], reported both in aggregate and broken down by the four broad
subject clusters (humanities, social sciences, STEM, other) [Q99, Q100, Q101]. The binary
correct/incorrect scoring is structurally misaligned with deployments requiring nuanced,
multi-perspective responses to contested questions: MMLU's label schema encodes a single
authoritative answer per question, with no mechanism for acknowledging that multiple answers
may be legitimate depending on cultural or national framing. The benchmark's documented
near-random accuracy on "socially important subjects such as morality and law" [Q8] and poor
performance on "subjects related to human values such as law and morality" [Q14] further
signals that the output taxonomy is poorly suited for culturally sensitive domains where
Arab-region values diverge from Western academic norms.

### 5. Output Content
NOT DOCUMENTED: The paper is entirely silent on annotator demographics, annotation process,
inter-annotator agreement, or quality-assurance procedures for verifying collected
question-answer pairs. No quotes in this category exist in the registry. Questions were
collected by graduate and undergraduate students [Q23] from US-origin sources [Q24, Q25],
with no described review by subject-matter experts from diverse cultural or regional
backgrounds. Human baselines are established from Amazon Mechanical Turk workers (34.5%
accuracy) [Q31] and from domain expert performance estimated from 95th-percentile US
test-taker accuracy [Q33, Q34] — neither population represents Arab regional stakeholders.
For Arab history and geography content that may appear within subjects like world history
or global facts, ground-truth labels were determined by Western academic sources, meaning
label correctness as judged by Arab regional stakeholders may diverge substantially from
what MMLU encodes as the single correct answer. The concern about poor model performance on
human values and law [Q79] is especially pertinent given that Arab legal systems are not
represented in MMLU's source materials.

### 6. Output Form
MMLU evaluates text outputs via classification accuracy [Q49], scoring models on whether
their highest-probability token among "A," "B," "C," and "D" matches the ground-truth label
[Q56]. Calibration is assessed using RMS calibration error and confidence-accuracy correlation
[Q65, Q67], revealing that GPT-3's confidence can be up to 24% off from its actual accuracy
[Q66]. The evaluation format is not identical to the format in which information is acquired
during pretraining [Q76], and UnifiedQA's text-to-text backbone evaluates via token overlap
with its text output [Q52]. The MCQ accuracy metric does not capture whether a model can
generate appropriately nuanced, multi-perspective, open-ended explanatory responses — the
output behavior the Arab-region deployment prioritizes. The benchmark comprehensively
evaluates the breadth and depth of academic understanding [Q9] but only within the
constraints of a four-option closed-answer scoring paradigm, which cannot surface the
graduated, context-sensitive output quality relevant to contested historical or political
topics.

### Stated Limitations
The authors acknowledge near-random accuracy on "socially important subjects such as
morality and law" [Q8], that models "do not match expert-level performance on any subject"
[Q81], and that it is "unclear whether simply scaling up existing language models will solve
the test" [Q87]. The benchmark is explicitly text-only [Q71] and does not address
cross-cultural or cross-regional validity limitations anywhere in the documentation.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "We propose a new test to measure a text model's multitask accuracy. The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more." |
| Q2 | 1 | input_ontology | "To attain high accuracy on this test, models must possess extensive world knowledge and problem solving ability." |
| Q3 | 1 | input_form | "We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings." |
| Q4 | 1 | input_ontology | "The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more. It ranges in difficulty from an elementary level to an advanced professional level, and it tests both world knowledge and problem solving ability." |
| Q5 | 1 | output_form | "We find that while most recent models have near random-chance accuracy, the very largest GPT-3 model improves over random chance by almost 20 percentage points on average." |
| Q6 | 1 | output_form | "However, on every one of the 57 tasks, the best models still need substantial improvements before they can reach expert-level accuracy." |
| Q7 | 1 | output_ontology | "Models also have lopsided performance and frequently do not know when they are wrong." |
| Q8 | 1 | output_ontology | "Worse, they still have near-random accuracy on some socially important subjects such as morality and law." |
| Q9 | 1 | output_form | "By comprehensively evaluating the breadth and depth of a model's academic and professional understanding, our test can be used to analyze models across many tasks and to identify important shortcomings." |
| Q10 | 1 | input_content | "Dan Hendrycks, UC Berkeley; Collin Burns, Columbia University; Steven Basart, UChicago; Andy Zou, UC Berkeley; Mantas Mazeika, UIUC; Dawn Song, UC Berkeley; Jacob Steinhardt, UC Berkeley" |
| Q11 | 2 | input_ontology | "Since our test consists in 57 tasks, it can be used to analyze aggregate properties of models across tasks and to track important shortcomings." |
| Q12 | 2 | output_form | "We find that meaningful progress on our benchmark has only become possible in recent months. In particular, few-shot models up to 13 billion parameters (Brown et al., 2020) achieve random chance performance of 25% accuracy, but the 175 billion parameter GPT-3 model reaches a much higher 43.9% accuracy (see Figure 1b)." |
| Q13 | 2 | output_form | "On the other hand, unlike human professionals GPT-3 does not excel at any single subject. Instead, we find that performance is lopsided, with GPT-3 having almost 70% accuracy for its best subject but near-random performance for several other subjects." |
| Q14 | 2 | output_ontology | "Our results indicate that while recent advances have been impressive, state-of-the-art models still struggle at learning and applying knowledge from pretraining. The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality." |
| Q15 | 2 | output_ontology | "This second weakness is particularly concerning because it will be important for future models to have a strong understanding of what is legal and what is ethical." |
| Q16 | 2 | output_form | "Worryingly, we also find that GPT-3 does not have an accurate sense of what it does or does not know since its average confidence can be up to 24% off from its actual accuracy." |
| Q17 | 2 | input_ontology | "We comprehensively evaluate the breadth and depth of a model's text understanding by covering numerous topics that humans are incentivized to learn." |
| Q18 | 2 | input_content | "The dominant paradigm in NLP is to pretrain large models on massive text corpora including educational books and websites." |
| Q19 | 2 | input_ontology | "Many recent benchmarks aim to assess a model's general world knowledge and basic reasoning ability by testing its "commonsense."" |
| Q20 | 3 | input_ontology | "We create a massive multitask test consisting of multiple-choice questions from various branches of knowledge." |
| Q21 | 3 | input_ontology | "The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn." |
| Q22 | 3 | input_ontology | "There are 57 tasks in total, which is also the number of Atari games (Bellemare et al., 2013), all of which are listed in Appendix B." |
| Q23 | 3 | input_content | "The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online." |
| Q24 | 3 | input_content | "These include practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination." |
| Q25 | 3 | input_content | "It also includes questions designed for undergraduate courses and questions designed for readers of Oxford University Press books." |
| Q26 | 3 | output_ontology | "Some tasks cover a subject, like psychology, but at a specific level of difficulty, such as "Elementary," "High School," "College," or "Professional."" |
| Q27 | 3 | input_form | "We collected 15908 questions in total, which we split into a few-shot development set, a validation set, and a test set." |
| Q28 | 3 | input_form | "The few-shot development set has 5 questions per subject, the validation set may be used for selecting hyperparameters and is made of 1540 questions, and the test set has 14079 questions." |
| Q29 | 3 | input_form | "Each subject contains 100 test examples at the minimum, which is longer than most exams designed to assess people." |
| Q30 | 3 | output_content | "Human-level accuracy on this test varies." |
| Q31 | 3 | output_content | "Unspecialized humans from Amazon Mechanical Turk obtain 34.5% accuracy on this test." |
| Q32 | 3 | output_content | "Meanwhile, expert-level performance can be far higher." |
| Q33 | 3 | output_content | "For example, real-world test-taker human accuracy at the 95th percentile is around 87% for US Medical Licensing Examinations, and these questions make up our "Professional Medicine" task." |
| Q34 | 3 | output_content | "If we take the 95th percentile human test-taker accuracy for exams that build up our test, and if we make an educated guess when such information is unavailable, we then estimate that expert-level accuracy is approximately 89.8%." |
| Q35 | 3 | input_ontology | "Since our test aggregates different subjects and several levels of difficulty, we measure more than straightforward commonsense or narrow linguistic understanding." |
| Q36 | 4 | input_ontology | "The humanities is a group of disciplines that make use of qualitative analysis and analytic methods rather than scientific empirical methods." |
| Q37 | 4 | input_ontology | "Branches of the humanities include law, philosophy, history, and so on (Appendix B)." |
| Q38 | 4 | input_ontology | "For example, legal understanding requires knowledge of how to apply rules and standards to complex scenarios, and also provide answers with stipulations and explanations." |
| Q39 | 4 | input_ontology | "For philosophy, our questions cover concepts like logical fallacies, formal logic, and famous philosophical arguments." |
| Q40 | 4 | input_ontology | "It also covers moral scenarios, including questions from the ETHICS dataset (Hendrycks et al., 2020) that test a model's understanding of normative statements through predicting widespread moral intuitions about diverse everyday scenarios." |
| Q41 | 4 | input_ontology | "Finally, our history questions cover a wide range of time periods and geographical locations, including prehistory and other advanced subjects." |
| Q42 | 4 | input_ontology | "Social science includes branches of knowledge that examine human behavior and society." |
| Q43 | 4 | input_ontology | "Subject areas include economics, sociology, politics, geography, psychology, and so on." |
| Q44 | 4 | input_ontology | "Our economics questions include microeconomics, macroeconomics, and econometrics, and cover different types of problems, including questions that require a mixture of world knowledge, qualitative reasoning, or quantitative reasoning." |
| Q45 | 4 | input_ontology | "We also include important but more esoteric topics such as security studies in order to test the boundaries of what is experienced and learned during pretraining." |
| Q46 | 4 | input_ontology | "Social science also includes psychology, a field that may be especially important for attaining a nuanced understanding of humans." |
| Q47 | 4 | input_ontology | "STEM subjects include physics, computer science, mathematics, and more." |
| Q48 | 4 | input_ontology | "Conceptual physics tests understanding of simple physics principles and may be thought" |
| Q49 | 5 | output_form | "To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks." |
| Q50 | 5 | output_form | "We evaluate GPT-3 (Brown et al., 2020) and UnifiedQA (Khashabi et al., 2020)." |
| Q51 | 5 | output_form | "For GPT-3 we use the OpenAI API, which provides access to four model variants, "Ada," "Babbage," "Curie," and "Davinci," which we refer to as "Small" (2.7 billion parameters), "Medium" (6.7 billion), "Large" (13 billion) and "X-Large" (175 billion)." |
| Q52 | 5 | output_form | "UnifiedQA uses the T5 (Raffel et al., 2019) text-to-text backbone and is fine-tuned on previously proposed question answering datasets (Lai et al., 2017), where the prediction is the class with the highest token overlap with UnifiedQA's text output." |
| Q53 | 5 | output_form | "Since UnifiedQA is fine-tuned on other datasets, we evaluate it without any further tuning to assess its transfer accuracy." |
| Q54 | 5 | output_form | "We also fine-tune RoBERTa-base, ALBERT-xxlarge, and GPT-2 on UnifiedQA training data and our dev+val set." |
| Q55 | 5 | output_form | "We primarily focus on UnifiedQA and GPT-3 in the rest of this document, but additional discussion of RoBERTa, ALBERT, and GPT-2 is in Appendix A." |
| Q56 | 6 | input_form | "We feed GPT-3 prompts like that shown in Figure 1a. We begin each prompt with "The following are multiple choice questions (with answers) about [subject]." For zero-shot evaluation, we append the question to the prompt. For few-shot evaluation, we add up to 5 demonstration examples with answers to the prompt before appending the question. All prompts end with "Answer: ". The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction. For consistent evaluation, we create a dev set with 5 fixed few-shot examples for each subject." |
| Q57 | 6 | output_form | "We compare the few-shot accuracy of each GPT-3 size in Table 1. We find that the three smaller GPT-3 models have near random accuracy (around 25%). In contrast, we find that the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%." |
| Q58 | 6 | output_form | "We also find qualitatively similar results in the zero-shot setting. While the smaller models have around 25% zero-shot accuracy, Figure 10 in Appendix A shows that the largest GPT-3 model has a much higher zero-shot accuracy of about 37.7%." |
| Q59 | 6 | output_form | "The largest UnifiedQA model we test has 11 billion parameters, which is slightly smaller than GPT-3 Large. Nevertheless, we show in Table 1 that it attains 48.9% accuracy. This performs better than the few-shot GPT-3 X-Large model, despite UnifiedQA have an order of magnitude fewer parameters." |
| Q60 | 6 | output_form | "We also find that even the smallest UnifiedQA variant, with just 60 million parameters, has approximately 29.3% accuracy." |
| Q61 | 6 | output_form | "These results suggest that while model size is a key component for achieving strong performance, fine-tuning also helps." |
| Q62 | 6 | output_form | "Using our test, we discover that GPT-3 and UnifiedQA have lopsided performance and several substantial knowledge gaps. Figure 6 shows the accuracy of GPT-3 (few-shot) and UnifiedQA for all 57 tasks. It shows the both models are below expert-level performance for all tasks, with GPT-3's accuracy ranging from 69% for US Foreign Policy to 26% for College Chemistry. UnifiedQA does best on marketing, with an accuracy of 82.5%." |
| Q63 | 6 | output_ontology | "Overall, models do poorly on highly procedural problems. Figure 6 shows that calculation-heavy STEM subjects tend to have low accuracy compared to verbal subjects. For GPT-3, 9 out of the 10" |
| Q64 | 7 | output_form | "We should not trust a model's prediction unless the model is calibrated, meaning that its confidence is a good estimate of the actual probability the prediction is correct." |
| Q65 | 7 | output_form | "We evaluate the calibration of GPT-3 by testing how well its average confidence estimates its actual accuracy for each subject." |
| Q66 | 7 | output_form | "Its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects." |
| Q67 | 7 | output_form | "Another calibration measure is the Root Mean Squared (RMS) calibration error (Hendrycks et al., 2019a; Kumar et al., 2019)." |
| Q68 | 7 | output_form | "Elementary Mathematics which has a zero-shot RMS calibration error of 19.4%." |
| Q69 | 7 | output_form | "Models are only somewhat more calibrated in the few-shot setting, as shown in Appendix A." |
| Q70 | 7 | input_form | "While text is capable of conveying an enormous number of concepts about the world, many important concepts are conveyed mainly through other modalities, such as images, audio, and physical interaction (Bisk et al., 2020)." |
| Q71 | 7 | input_form | "Existing large-scale NLP models, such as GPT-3, do not incorporate multimodal information, so we design our benchmark to capture a diverse array of tasks in a text-only format." |
| Q72 | 7 | input_content | "A major distinction between our benchmark and previous multitask NLP benchmarks is that we do not require large training sets." |
| Q73 | 7 | input_content | "Instead, we assume that models have acquired the requisite knowledge from reading vast quantities of diverse text from the Internet." |
| Q74 | 8 | output_form | "For this reason we assess pretrained models in a zero-shot, few-shot, or transfer setting and we provide a dev, val, and test set for each task." |
| Q75 | 8 | output_form | "The dev set is used for few-shot prompts, the val set could be used for hyperparameter tuning, and the test set is used to compute the final accuracy." |
| Q76 | 8 | input_form | "Importantly, the format of our evaluation is not identical to the format in which information is acquired during pretraining." |
| Q77 | 8 | input_form | "This has the benefit of obviating concerns about spurious training set annotation artifacts (Geirhos et al., 2020; Hendrycks et al., 2019b) and is in stark contrast to the previous paradigm of identically distributed training and test sets." |
| Q78 | 8 | output_form | "We find that current large-scale Transformers have wide room for improvement." |
| Q79 | 8 | output_ontology | "They are notably poor at modeling human (dis)approval, as evident by the low performance on the Professional Law and Moral Scenarios tasks." |
| Q80 | 8 | output_ontology | "Models also have difficulty performing calculations, so much so that they exhibit poor performance on Elementary Mathematics and many other STEM subjects with "plug and chug" problems." |
| Q81 | 8 | output_form | "Additionally, they do not match expert-level performance (90%) on any subject, so for all subjects it is subhuman." |
| Q82 | 8 | output_form | "On average, models are only now starting to move beyond random-chance accuracy levels." |
| Q83 | 8 | input_content | "We collected approximately 2,000 additional Professional Law training examples." |
| Q84 | 8 | output_form | "After fine-tuning a RoBERTa-base model (Liu et al., 2019) using this custom training set, our model attained 32.8% test accuracy." |
| Q85 | 8 | input_content | "We also had RoBERTa continue pretraining on approximately 1.6 million legal case summaries using Harvard's Law Library case law corpus case.law, but after fine-tuning it only attained 36.1% accuracy." |
| Q86 | 8 | output_form | "This suggests that while additional pretraining on relevant high quality text can help, it may not be enough to substantially increase the performance of current models." |
| Q87 | 8 | output_form | "It is unclear whether simply scaling up existing language models will solve the test." |
| Q88 | 8 | output_form | "Current understanding indicates that a 10× increase in model size must be accompanied by an approximate 5× increase in data (Kaplan et al., 2020)." |
| Q89 | 8 | input_ontology | "We introduced a new test that measures how well text models can learn and apply knowledge encountered during pretraining." |
| Q90 | 8 | input_ontology | "By covering 57 subjects at varying levels of difficulty, the test assesses language understanding in greater breadth and depth than previous benchmarks." |
| Q91 | 9 | input_content | "We would like to thank the following for their helpful comments: Oyvind Tafjord, Jan Leike, David Krueger, Alex Tamkin, Girish Sastry, and Henry Zhu." |
| Q92 | 9 | input_content | "DH is supported by the NSF GRFP Fellowship and an Open Philanthropy Project Fellowship." |
| Q93 | 9 | input_content | "This research was also supported by the NSF Frontier Award 1804794." |
| Q94 | 11 | input_ontology | "This appendix includes figures with sorted results (Figure 9), few-shot examples vs. accuracy (Figure 10), and few-shot calibration (Figure 11). It also includes sections on fine-tuning, error analysis, and format sensitivity." |
| Q95 | 11 | output_form | "We primarily analyzed models with more than 10 billion parameters in the main body of the paper. For this section, we analyze smaller models including RoBERTa-base (125 million parameters) (Liu" |
| Q96 | 11 | output_form | "On the left are GPT-3 few shot accuracies for all of the 57 tasks. On the right are UnifiedQA transfer accuracies for all of the 57 tasks. For both models, capabilities are lopsided." |
| Q97 | 12 | input_form | "Models are fine-tuned to predict one of four classes using the UnifiedQA MCQ questions and using our dev+val set." |
| Q98 | 12 | output_form | "We test on our multitask test set." |
| Q99 | 12 | output_form | "RoBERTa-base attains an overall accuracy of 27.9%, with 27.9% accuracy for the humanities, 28.8% for social sciences, 27.0% for STEM, and 27.7% for other." |
| Q100 | 12 | output_form | "ALBERT-xxlarge attains an accuracy of 27.1%, with 27.2% accuracy for the humanities, 25.7% for the social sciences, 27.7% for STEM, and 27.9% for other." |
| Q101 | 12 | output_form | "GPT-2 attains an accuracy of 32.4%, with 32.8% accuracy for the humanities, 33.3% for the social sciences, 30.2% for STEM, and 33.1% for other." |
| Q102 | 12 | output_form | "We qualitatively analyze when GPT-3 makes high confidence mistakes." |
| Q103 | 12 | input_form | "While different question formatting choices often lead to similar GPT-3 accuracies, we find that UnifiedQA is more sensitive." |
| Q104 | 12 | input_form | "UnifiedQA's input format is of the form QUESTION1 \\n (A) CHOICE1 (B) CHOICE2 (C) CHOICE3 (D) CHOICE4</s> where questions and choices are normalized and made lowercase." |
| Q105 | 12 | input_form | "If we remove the </s> from the input, accuracy declines by several percentage points." |
| Q106 | 13 | input_ontology | "We provide analysis of question length and difficulty in Figure 12. We list all tasks and the topics they test in Table 2. We also provide an example for each task starting with Figure 14." |
| Q107 | 13 | input_content | "Since language models train on vast text corpora, there is some chance that they have seen the exact question and answer during pretraining. If they memorized the exact question and answer, then they would attain higher accuracy than their true ability. Likewise, a question's entropy would be especially low if it were memorized. Memorized questions and answers should have low entropy and" |
| Q108 | 13 | input_form | "For questions longer than a tweet (280 characters), the correlation between question length and true label confidence is slightly positive. This shows that longer questions are not necessarily harder." |
| Q109 | 14 | input_content | "However, in Figure 13, we see that accuracy and question entropy are not positively correlated, suggesting that the test's low-entropy questions do not correspond to memorized (and thereby correctly predicted) answers." |
| Q110 | 14 | input_content | "This suggests that our exact questions were not memorized." |
| Q111 | 14 | input_content | "However, during pretraining models encountered text related to our questions through processing Wikipedia." |
| Q112 | 14 | input_content | "We also note that most of our questions came from PDFs or websites where questions and answers are on separate pages." |
| Q113 | 14 | input_content | "See Brown et al. (2020) for a previous discussion of contamination showing that the phenomena hardly affects performance." |
| Q114 | 14 | input_content | "To reduce the probability that future models encounter exact questions during test-time, we will provide a list of question sources." |
| Q115 | 14 | output_form | "The average log probability of the question (without answer) is not strongly positively correlated with accuracy, all else equal." |
| Q116 | 14 | output_form | "Each point corresponds to a task." |
| Q117 | 14 | output_form | "Higher log probability indicates higher compression, and especially high log probability would suggest memorization." |
| Q118 | 14 | output_form | "In the zero-shot question prompt, the correlation between average log probability and accuracy is r = −0.43, and for the few-shot setting the correlation is r = −0.56." |
| Q119 | 15 | input_ontology | "Table 2: Summary of all 57 tasks." |
| Q120 | 16 | input_ontology | "Find all c in Z₃ such that Z₃[x]/(x² + c) is a field." |
| Q121 | 16 | input_ontology | "What is the embryological origin of the hyoid bone?" |
| Q122 | 16 | input_ontology | "Why isn't there a planet where the asteroid belt is located?" |
| Q123 | 16 | input_ontology | "Three contrasting tactics that CSO's can engage in to meet their aims are ___ which typically involves research and communication, ___, which may involve physically attacking a company's operations or ___, often involving some form of ___." |
| Q124 | 16 | input_ontology | "How many attempts should you make to cannulate a patient before passing the job on to a senior colleague?" |
| Q125 | 16 | input_ontology | "In a given population, 1 out of every 400 people has a cancer caused by a completely recessive allele, b. Assuming the population is in Hardy-Weinberg equilibrium, which of the following is the expected proportion of individuals who carry the b allele but are not expected to develop the cancer?" |
| Q126 | 16 | input_ontology | "Which of the following statements about the lanthanide elements is NOT true?" |
| Q127 | 17 | input_ontology | "Consider a computer design in which multiple processors, each with a private cache memory, share global memory using a single bus." |
| Q128 | 17 | input_ontology | "Let A be a real 2 × 2 matrix. Which of the following statements must be true?" |
| Q129 | 17 | input_ontology | "In a genetic test of a newborn, a rare genetic disorder is found that has X-linked recessive transmission." |
| Q130 | 17 | input_ontology | "One end of a Nichrome wire of length 2L and cross-sectional area A is attached to an end of another Nichrome wire of length L and cross- sectional area 2A." |
| Q131 | 17 | input_ontology | "Why is it that anti-virus scanners would not have found an exploitation of Heartbleed?" |
| Q132 | 17 | input_ontology | "A model airplane flies slower when flying into the wind and faster with wind at its back." |
| Q133 | 18 | input_ontology | "Consider the following AR(1) model with the disturbances having zero mean and unit variance yt = 0.2 + 0.4yt−1 + ut The (unconditional) mean of y will be given by (A) 0.2 (B) 0.4 (C) 0.5 (D) 0.33" |
| Q134 | 18 | input_ontology | "A point pole has a strength of 4π × 10−4 weber. The force in newtons on a point pole of 4π × 1.5 × 10−4 weber placed at a distance of 10 cm from it will be (A) 15 N. (B) 20 N. (C) 7.5 N. (D) 3.75 N." |
| Q135 | 18 | input_ontology | "A total of 30 players will play basketball at a park. There will be exactly 5 players on each team. Which statement correctly explains how to find the number of teams needed? (A) Add 5 to 30 to find 35 teams. (B) Divide 30 by 5 to find 6 teams. (C) Multiply 30 and 5 to find 150 teams. (D) Subtract 5 from 30 to find 25 teams." |
| Q136 | 18 | input_ontology | "Determine whether the statements are logically equivalent or contradictory. If neither, determine whether they are consistent or inconsistent. E ⊃ (F · E) and ∼ E · F (A) Logically equivalent (B) Contradictory (C) Neither logically equivalent nor contradictory, but consistent (D) Inconsistent" |
| Q137 | 18 | input_content | "As of 2017, how many of the world's 1-year-old children today have been vaccinated against some disease? (A) 80% (B) 60% (C) 40% (D) 20%" |
| Q138 | 18 | input_ontology | "Homologous structures are often cited as evidence for the process of natural selection. All of the following are examples of homologous structures EXCEPT (A) the wings of a bird and the wings of a bat (B) the flippers of a whale and the arms of a man (C) the pectoral fins of a porpoise and the flippers of a seal (D) the forelegs of an insect and the forelimbs of a dog" |
| Q139 | 18 | input_ontology | "From the solubility rules, which of the following is true? (A) All chlorides, bromides, and iodides are soluble (B) All sulfates are soluble (C) All hydroxides are soluble (D) All ammonium-containing compounds are soluble" |
| Q140 | 19 | input_ontology | "A list of numbers has n elements, indexed from 1 to n. The following algorithm is intended to display the number of elements in the list that have a value greater than 100. The algorithm uses the variables count and position. Steps 3 and 4 are missing." |
| Q141 | 19 | input_ontology | "Which of the following could be used to replace steps 3 and 4 so that the algorithm works as intended?" |
| Q142 | 19 | input_content | "This question refers to the following information." |
| Q143 | 19 | input_content | "From the passage, one may infer that the English Parliament wished to argue that the Act of Supremacy would" |
| Q144 | 19 | input_ontology | "During the third stage of the demographic transition model, which of the following is true?" |
| Q145 | 20 | input_ontology | "Figure 37: A High School Government and Politics example." |
| Q146 | 20 | input_ontology | "Figure 38: A High School Macroeconomics example." |
| Q147 | 20 | input_ontology | "Figure 39: A High School Mathematics example." |
| Q148 | 20 | input_ontology | "Figure 40: A High School Microeconomics example." |
| Q149 | 20 | input_ontology | "Figure 41: A High School Physics example." |
| Q150 | 20 | input_ontology | "Figure 42: A High School Psychology example." |
| Q151 | 21 | input_ontology | "Figure 43: A High School Statistics example." |
| Q152 | 21 | input_content | "Figure 44: A High School US History example." |
| Q153 | 21 | input_content | "Figure 45: A High School World History example." |
| Q154 | 21 | input_ontology | "Figure 46: A Human Aging example." |
| Q155 | 22 | input_content | "Morning sickness is typically a problem: (A) during the first trimester (B) during the second trimester (C) during the third trimester (D) all through the pregnancy" |
| Q156 | 22 | input_content | "Would a reservation to the definition of torture in the ICCPR be acceptable in contemporary practice? (A) This is an acceptable reservation if the reserving country's legislation employs a different definition (B) This is an unacceptable reservation because it contravenes the object and purpose of the ICCPR (C) This is an unacceptable reservation because the definition of torture in the ICCPR is consistent with customary international law (D) This is an acceptable reservation because under general international law States have the right to enter reservations to treaties" |
| Q157 | 22 | input_content | "Which position does Rawls claim is the least likely to be adopted by the POP (people in the original position)? (A) The POP would choose equality above liberty. (B) The POP would opt for the 'maximin' strategy. (C) The POP would opt for the 'difference principle.' (D) The POP would reject the 'system of natural liberty.'" |
| Q158 | 22 | input_content | "John Stuart Mill: Each person's happiness is a good to that person, and the general happiness, therefore, a good to the aggregate of all persons. (A) Fallacy of Composition (B) Fallacy of Division (C) Gambler's Fallacy (D) Equivocation" |
| Q159 | 22 | input_ontology | "A 6-sided die is rolled 15 times and the results are: side 1 comes up 0 times; side 2: 1 time; side 3: 2 times; side 4: 3 times; side 5: 4 times; side 6: 5 times. Based on these results, what is the probability of side 3 coming up when using Add-1 Smoothing? (A) 2/15 (B) 1/7 (C) 3/16 (D) 1/5" |
| Q160 | 22 | input_content | "According to Lewin, Lippet and White's 1939 experiment, which form of leadership produced the most work from participants? (A) Laissez-faire (B) Democratic (C) Authoritarian (D) A mix of laissez-faire and democratic" |
| Q161 | 23 | output_form | "Figure 57: A Moral Scenarios example. The formatting of this task hinders UnifiedQA performance substantially." |
| Q162 | 24 | input_content | "According to Moore's "ideal utilitarianism," the right action is the one that brings about the greatest amount of: (A) pleasure. (B) happiness. (C) good. (D) virtue." |
| Q163 | 24 | input_content | "Researchers now believe that the decline of the Maya was caused chiefly by: (A) a cataclysm of some kind, such as an earthquake, volcano, or tsunami. (B) ecological degradation resulting from slash-and-burn farming techniques. (C) endless wars between neighboring Mayan city-states. (D) practices of interbreeding that led to a steep rise in congenital disorders." |
| Q164 | 24 | input_content | "Krete is an unmarried taxpayer with income exclusively from wages. By December 31, year 1, Krete's employer has withheld $16,000 in federal income taxes and Krete has made no estimated tax payments. On April 15, year 2, Krete timely filed for an extension request to file her individual tax return, and paid $300 of additional taxes. Krete's year 1 tax liability was $16,500 when she timely filed her return on April 30, year 2, and paid the remaining tax liability balance. What amount would be subject to the penalty for underpayment of estimated taxes? (A) $0 (B) $500 (C) $1,650 (D) $16,500" |
| Q165 | 24 | input_content | "The night before his bar examination, the examinee's next-door neighbor was having a party. The music from the neighbor's home was so loud that the examinee couldn't fall asleep. The examinee called the neighbor and asked her to please keep the noise down. The neighbor then abruptly hung up. Angered, the examinee went into his closet and got a gun. He went outside and fired a bullet through the neighbor's living room window. Not intending to shoot anyone, the examinee fired his gun at such an angle that the bullet would hit the ceiling. He merely wanted to cause some damage to the neighbor's home to relieve his angry rage. The bullet, however, ricocheted off the ceiling and struck a partygoer in the back, killing him. The jurisdiction makes it a misdemeanor to discharge a firearm in public. The examinee will most likely be found guilty for which of the following crimes in connection to the death of the partygoer? (A) Murder. (B) Involuntary manslaughter. (C) Voluntary manslaughter. (D) Discharge of a firearm in public." |
| Q166 | 25 | input_content | "Published as a conference paper at ICLR 2021" |
| Q167 | 26 | input_ontology | "Figure 66: A Security Studies example." |
| Q168 | 26 | input_ontology | "Figure 67: A Sociology example." |
| Q169 | 26 | input_ontology | "Figure 68: A US Foreign Policy example." |
| Q170 | 26 | input_ontology | "Figure 69: A Virology example." |
| Q171 | 27 | input_ontology | "Figure 70: A World Religions example." |

---

## Regional Context

```yaml
name: Non-Arab Tourists and Expats in Eight Arab Countries
abbreviation: arab-tourist-expat
deployment_context:
  description: An AI assistant helping non-Arab tourists and expats visiting Morocco,
    Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, and Saudi Arabia answer school-level
    general-knowledge questions about Arabic language, Arab history, and regional
    geography. The system is evaluated using MMLU, a US-centric English-language benchmark.
  use_case_scope: School-level educational knowledge (history, geography, language
    basics). Practical on-the-ground guidance (local etiquette, transport, markets,
    dialect phrases) is out of scope for the benchmark evaluation but frequently expected
    by users.
  benchmark: MMLU (Measuring Massive Multitask Language Understanding)
  benchmark_language: English only
  primary_assessment_concern: MMLU's 57 subjects are anchored in US academic curricula
    and contain no dedicated Arab-region subject categories; cultural grounding, label
    validity, and multi-perspective output are structural gaps.
covered_countries:
- Morocco
- Egypt
- Jordan
- Palestine
- Lebanon
- United Arab Emirates
- Kuwait
- Saudi Arabia
sub_regional_clusters:
  north_africa_maghreb:
    countries:
    - Morocco
    distinctive_features: Amazigh (Berber) heritage alongside Arab-Islamic identity;
      Darija (Moroccan Arabic) as dominant spoken vernacular; French administrative
      and educational overlay; Saharan and Atlantic geographic identity; contested
      Western Sahara issue.
    mmlu_blind_spots: Moroccan Amazigh cultural identity, Darija linguistic features,
      and Maghreb-specific history are entirely absent from MMLU's documented subject
      taxonomy.
  nile_valley:
    countries:
    - Egypt
    distinctive_features: Pharaonic heritage as a parallel identity pillar alongside
      Arab-Islamic identity; Coptic Christian minority context; Egyptian Arabic as
      the most widely understood Arabic dialect; center of Arab intellectual and media
      production.
    mmlu_blind_spots: Egyptian Coptic minority history, pharaonic periodization from
      an Arab perspective, and Egyptian dialect features are not documented in MMLU
      content.
  levant:
    countries:
    - Jordan
    - Palestine
    - Lebanon
    distinctive_features: Highly contested political histories (1948 war, Palestinian
      displacement, Lebanese civil war, Jordanian-Palestinian demographic complexity);
      sectarian diversity (Maronites, Druze, Sunni, Shia, Greek Orthodox); Levantine
      Arabic dialects; Palestinian narrative as a politically salient cross-cutting
      theme.
    mmlu_blind_spots: Palestinian historical narrative, 1948 war framing, Lebanese
      Civil War perspectives, and Jordanian-Palestinian demographic history are absent
      or likely framed from Western/Israeli perspectives in MMLU.
  gulf:
    countries:
    - United Arab Emirates
    - Kuwait
    - Saudi Arabia
    distinctive_features: Tribal and monarchical civic identity; large expatriate-to-citizen
      population ratios; kafala system governing labor relations; Vision 2030 and
      national transformation agendas; Gulf Arabic dialects; Islamic governance frameworks;
      oil-based economic identity.
    mmlu_blind_spots: Kafala system, Vision 2030, Gulf tribal governance, and Gulf-specific
      social norms are absent from MMLU's subject taxonomy. Western framing of Gulf
      politics (US Foreign Policy task) does not substitute.
target_user_population:
  description: Non-Arab tourists and expats visiting the eight covered countries,
    seeking general educational knowledge about Arabic language, Arab history, and
    regional geography. Users have limited to no Arabic literacy and arrive from a
    wide diversity of source countries.
  primary_language: English
  secondary_language_cohort: Arabic-learning foreigners who may prompt in Arabic;
    cannot be evaluated by English-only MMLU.
  source_country_diversity: Potentially global; no single dominant source nationality
    specified.
  arabic_literacy_expectation: Low to none for the primary cohort; beginner to intermediate
    for the Arabic-learning sub-cohort.
  prior_regional_knowledge: School-level or tourist-level; not specialist or academic.
  occupation_role: Tourists and expats; general curiosity users, not researchers or
    policymakers.
languages:
  primary_interaction_language: English
  secondary_interaction_language: Arabic (Arabic-learning sub-cohort); specific dialects
    unspecified but Modern Standard Arabic most likely for learners
  arabic_dialect_landscape:
    moroccan_darija: 'Distinct Maghreb Arabic variety with Berber and French influence.
      Mutual intelligibility with other Arabic varieties is low; research confirms
      Maghrebi Arabic is structurally distant from Mashriqi varieties, with comprehension
      dropping sharply across macro-groups. DialectalArabicMMLU (2025) notes Moroccan
      dialect is one of the five major dialects included in its benchmark, and that
      ''structurally distant dialects such as Maghrebi Arabic'' require distinct NLP
      treatment. Source: DialectalArabicMMLU — [WEB-1]'
    egyptian_arabic: 'Most widely understood spoken Arabic variety due to media influence.
      Included as a distinct dialect in DialectalArabicMMLU (2025) and AraDiCE (2025),
      confirming its prominence in dialect NLP benchmarks. Source: DialectalArabicMMLU
      — [WEB-1]'
    levantine_arabic: 'Spoken in Jordan, Palestine, Lebanon; Palestinian, Jordanian,
      and Lebanese sub-varieties. Intra-Levantine variation is acknowledged in the
      NLP literature (Syrian included as distinct variety in DialectalArabicMMLU);
      Jordanian, Palestinian, and Lebanese sub-varieties are not yet individually
      benchmarked in publicly available dialect MMLU-style evaluations. Source: DialectalArabicMMLU
      — [WEB-1]'
    gulf_arabic: 'Spoken in UAE, Kuwait, KSA; notable sub-variation between Kuwaiti,
      Najdi, Hejazi, and Gulf coastal varieties. DialectalArabicMMLU (2025) includes
      Emirati and Saudi as distinct dialects, confirming sub-Gulf variation is benchmarkable
      but Kuwaiti is not yet separately covered. Source: DialectalArabicMMLU — [WEB-1]'
    modern_standard_arabic: Formal/written register used across all eight countries;
      primary target for Arabic-language learners
  benchmark_language_coverage: 'MMLU is English-only; Arabic-language user queries
    cannot be evaluated. ArabicMMLU (ACL 2024) exists as a native-Arabic benchmark
    with 14,575 MSA questions across 40 tasks, sourced from school exams in countries
    spanning North Africa, the Levant, and the Gulf — the closest available substitute
    for Arabic-language secondary-cohort evaluation. Source: ArabicMMLU — [WEB-2]'
  diglossia_relevance: Moderate — users are learning or asking about Arabic language
    basics, so awareness of MSA vs. dialect distinction is deployment-relevant, but
    practical dialect support is out of benchmark scope.
writing_systems:
  arabic_script: Right-to-left; used for Arabic-language prompts from the secondary
    user cohort. RTL rendering and mixed Arabic-Latin text are relevant for interface
    evaluation but not for MMLU scoring.
  latin_script: Used for English primary interaction and for French overlay in Morocco/Lebanon
    contexts.
  tifinagh_script: 'Tifinagh (Neo-Tifinagh) is the officially adopted script for Standard
    Moroccan Amazigh (Tamazight) as chosen by IRCAM in 2003, and appears on Moroccan
    public signage, currency, and in primary school textbooks. However, it is not
    widely used in practice: most Amazigh speakers use Latin or Arabic script in everyday
    writing, and as of 2016 Tifinagh use has been largely confined to public signage
    and culturally conspicuous contexts. Given the deployment''s school-level Arabic/geography/history
    focus, Tifinagh-script content is likely out of scope, but awareness of this script''s
    official status is relevant for Morocco-specific cultural knowledge evaluation.
    Source: Wikipedia Standard Moroccan Amazigh — [WEB-3];
    Constitute Project Morocco 2011 — [WEB-4]'
  benchmark_script_coverage: MMLU is Latin-script English only; no RTL or Arabic-script
    evaluation.
domain_coverage:
  in_scope_for_deployment:
  - 'Arab history (school-level: Islamic Golden Age, Ottoman period, Arab nationalism,
    modern state formation)'
  - Regional geography (physical and political geography of the eight countries and
    the broader Arab world)
  - Arabic language basics (alphabet, grammar fundamentals, MSA vocabulary, script
    introduction)
  - General pan-Arab cultural knowledge (Islamic calendar, major religious practices
    as background knowledge)
  out_of_scope_for_deployment_but_user_expected:
  - Local dialect phrases and conversational Arabic
  - Tourist etiquette and religious customs guidance
  - Transport and market navigation
  - Practical visa, legal, or administrative advice
  mmlu_subject_overlap:
    nominal_overlap:
    - High School World History (nominally covers multiple geographies but Arab-region
      content unverified)
    - High School Geography (social sciences cluster; Arab-region content unverified)
    - World Religions (Islamic content may be present; extent and framing unverified)
    - Global Facts (some Arab-region statistics may appear; extent unverified)
    no_overlap:
    - Arab history (no dedicated subject)
    - Middle Eastern geography (no dedicated subject)
    - Arabic language (no dedicated subject)
    - Islamic jurisprudence or law (no dedicated subject; Professional Law is US bar
      exam)
    arab_region_content_in_mmlu: 'No systematic published audit has been found quantifying
      the proportion of Arab-region content in MMLU''s world history, geography, or
      global facts subjects. The ILMAAM/Nacar et al. (2025) study evaluated the Arabic
      MMLU benchmark (translated version) and found ''significant cultural misalignments
      and biases, particularly in sensitive areas like religion and morality,'' with
      the original Western-sourced content flagged as inadequate for Arabic-speaking
      communities. This provides indirect evidence that Arab-region content is either
      absent or misframed in the MMLU-derived Arabic translation. Dedicated audit
      of original English MMLU for Arab-region content proportion remains unfound.
      Source: ILMAAM/Nacar et al. 2025 — [WEB-5]'
contested_topics_and_political_sensitivities:
  description: Multiple topics covered by the deployment are politically contested
    across and within the eight countries, requiring multi-perspective acknowledgment
    rather than single-answer responses. MMLU's binary MCQ scoring is structurally
    incapable of capturing this requirement.
  key_contested_topics:
  - topic: 1948 Arab-Israeli War / Nakba
    countries_most_affected:
    - Palestine
    - Jordan
    - Lebanon
    framing_variation: Palestinian and Arab sources frame as catastrophe (Nakba) and
      dispossession; Israeli and Western academic sources frame as Israeli War of
      Independence; MMLU likely encodes Western framing if present at all.
    mmlu_label_validity_concern: HIGH
  - topic: Western Sahara territorial status
    countries_most_affected:
    - Morocco
    framing_variation: Morocco claims sovereignty; Sahrawi independence movement and
      Algeria contest this; UN position is unresolved.
    mmlu_label_validity_concern: HIGH
  - topic: Lebanese Civil War causes and responsibility
    countries_most_affected:
    - Lebanon
    framing_variation: Sectarian, Palestinian, Syrian, Israeli, and Western Cold War
      framings differ substantially.
    mmlu_label_validity_concern: MODERATE
  - topic: Ottoman and colonial legacy periodization
    countries_most_affected:
    - All eight countries
    framing_variation: Arab nationalist, Ottoman nostalgic, and Western colonial historiographies
      diverge on periodization and causality.
    mmlu_label_validity_concern: MODERATE
  - topic: Palestinian statehood and borders
    countries_most_affected:
    - Palestine
    - Jordan
    - Lebanon
    framing_variation: UN resolutions, Arab League positions, Israeli government positions,
      and US policy positions differ; MMLU sourced from US academic materials likely
      reflects US policy framing.
    mmlu_label_validity_concern: HIGH
  - topic: Status of Jerusalem
    countries_most_affected:
    - Palestine
    - Jordan
    - Lebanon
    framing_variation: Palestinian, Jordanian (Hashemite custodianship), Israeli,
      and international law framings diverge.
    mmlu_label_validity_concern: HIGH
  deployment_required_behavior: System should acknowledge multiple perspectives and
    explicitly flag when a topic is contested or politically sensitive across countries,
    rather than presenting a single authoritative answer.
  benchmark_alignment: MMLU single-label MCQ scoring is structurally misaligned with
    this required behavior; no mechanism exists in MMLU to credit multi-perspective
    or uncertainty-flagging responses.
country_specific_knowledge_gaps_in_mmlu:
  morocco:
    amazigh_heritage: Tamazight language, Tifinagh script, Berber pre-Islamic history
      — absent from MMLU
    darija: Moroccan Arabic dialect features — absent from MMLU
    french_overlay: Administrative and educational use of French — not covered in
      MMLU Arab-region context
    western_sahara: Contested territorial status — MMLU label validity suspect
    mmlu_coverage_estimate: '[NEEDS VERIFICATION — deferred: below search budget;
      no published per-country MMLU coverage audit found]'
  egypt:
    pharaonic_history: Likely present in MMLU world history but framing perspective
      (Western Egyptology vs. Egyptian national narrative) unverified
    coptic_christianity: 'Coptic minority history and identity — [NEEDS VERIFICATION
      — deferred: below search budget; no specific MMLU audit of Coptic content found]'
    modern_egypt: 'Nasser, Arab nationalism, 1952 revolution, Camp David — [NEEDS
      VERIFICATION — deferred: below search budget]'
    mmlu_coverage_estimate: '[NEEDS VERIFICATION — deferred: below search budget;
      no published per-country MMLU coverage audit found]'
  jordan:
    hashemite_kingdom: 'Hashemite dynasty history, Jordanian-Palestinian demographic
      context — [NEEDS VERIFICATION — deferred: below search budget]'
    trans_jordan_mandate: 'British Mandate period, Transjordan formation — [NEEDS
      VERIFICATION — deferred: below search budget]'
    mmlu_coverage_estimate: '[NEEDS VERIFICATION — deferred: below search budget]'
  palestine:
    nakba_and_1948: Nakba framing almost certainly absent from MMLU; 1948 war likely
      framed from Western/Israeli perspective if present
    oslo_accords: '[NEEDS VERIFICATION — deferred: below search budget]'
    mmlu_coverage_estimate: '[NEEDS VERIFICATION — likely near-zero from Palestinian
      perspective; no published audit found]'
  lebanon:
    civil_war: 'Lebanese Civil War multi-perspective coverage — [NEEDS VERIFICATION
      — deferred: below search budget]'
    phoenician_heritage: 'Pre-Arab Phoenician historical identity — [NEEDS VERIFICATION
      — deferred: below search budget]'
    sectarian_system: 'Confessional political system — [NEEDS VERIFICATION — deferred:
      below search budget]'
    mmlu_coverage_estimate: '[NEEDS VERIFICATION — deferred: below search budget]'
  uae:
    federal_formation: 'UAE federal formation in 1971, Trucial States history — [NEEDS
      VERIFICATION — deferred: below search budget]'
    kafala_system: Labor governance — absent from MMLU documented subjects
    rapid_modernization_narrative: 'Dubai/Abu Dhabi development as national narrative
      — [NEEDS VERIFICATION — deferred: below search budget]'
    mmlu_coverage_estimate: '[NEEDS VERIFICATION — deferred: likely minimal; below
      search budget]'
  kuwait:
    gulf_war: '1990 Iraqi invasion and Gulf War — [NEEDS VERIFICATION — deferred:
      below search budget; likely present in MMLU US Foreign Policy or world history
      but framing unverified]'
    tribal_governance: 'Kuwaiti tribal and dynastic governance — [NEEDS VERIFICATION
      — deferred: below search budget]'
    mmlu_coverage_estimate: '[NEEDS VERIFICATION — deferred: below search budget]'
  saudi_arabia:
    wahhabi_salafi_religious_tradition: 'Religious-political history of Saudi state
      formation — [NEEDS VERIFICATION — deferred: below search budget; framing in
      MMLU world religions unverified]'
    vision_2030: Vision 2030 reform agenda — absent from MMLU (post-2021 and not in
      academic curricula represented)
    two_holy_mosques: Mecca and Medina religious significance — likely present in
      MMLU world religions but extent unverified
    mmlu_coverage_estimate: '[NEEDS VERIFICATION — deferred: below search budget]'
annotation_and_label_validity:
  mmlu_annotator_population: Graduate and undergraduate students at US universities;
    Amazon Mechanical Turk workers for human baseline; no Arab regional stakeholders
    documented.
  label_source_institutions: US standardized tests (GRE, USMLE), US undergraduate
    curricula, Oxford University Press publications; no Arab educational institutions
    represented.
  arab_regional_label_validity: For any Arab history, regional geography, or Islamic
    content questions that appear in MMLU, ground-truth labels encode Western academic
    framing. Divergence from Arab regional stakeholder judgments is expected but unquantified.
  inter_annotator_agreement: NOT DOCUMENTED in MMLU paper.
  arab_expert_review: NOT DOCUMENTED — no subject-matter experts from Arab academic
    institutions are identified in MMLU documentation.
  contested_label_risk: HIGH for Palestinian and Levantine political history; MODERATE
    for Islamic history and general Arab geography; LOW for STEM subjects.
  recommended_supplementary_validation: 'ArabicMMLU (ACL 2024) is the most direct
    available alternative: 14,575 native MSA questions from school exams across eight
    Arab countries, constructed by 10 native speakers (Jordanian, Egyptian, Lebanese,
    UAE, Saudi annotators). However, ArabicMMLU still uses single-answer MCQ scoring
    and does not address contested historical framing. The ILMAAM benchmark (Nacar
    et al. 2025) provides a culturally aligned refinement of ArabicMMLU with annotation
    by 11 experts for fluency, cultural appropriateness, bias, religious sensitivity,
    and social norms — the most relevant model for Arab regional label validation.
    Source: ArabicMMLU GitHub — [WEB-6]; ILMAAM
    — [WEB-5]'
arabic_language_benchmark_gap:
  mmlu_arabic_coverage: None — MMLU is English-only with no Arabic-language questions
    or Arabic-language input evaluation.
  arabic_learning_user_cohort: Cannot be evaluated by MMLU; a separate Arabic-language
    benchmark is required for this sub-cohort.
  existing_arabic_mmlu_variants: 'Three tiers of Arabic MMLU-style benchmarks now
    exist:

    (1) MMLU_ar (OpenAI): a machine-translated version of English MMLU into Arabic;
    widely criticised for linguistic fidelity failures, cultural misalignment, and
    ''Western focus with no Arabic alignment.'' Source: Nacar et al. 2025 — [WEB-5]

    (2) ArabicMMLU (Koto et al., ACL 2024): 14,575 native MSA MCQs sourced from school
    exams across North Africa, Levant, and Gulf, covering 40 tasks; annotated by 10
    Arab native speakers from Jordan, Egypt, Lebanon, UAE, KSA. Includes history questions
    from Jordan, Egypt, UAE, Palestine, and Morocco. Best-performing model is GPT-4
    at 72.5%; Arabic-centric Jais-chat (30B) achieves 62.3%. Limitation: MSA only,
    single-answer MCQ, no explicit contested-history handling. Source: ArabicMMLU
    ACL 2024 — [WEB-2]; GitHub — [WEB-6]

    (3) ILMAAM (Nacar et al. 2025): culturally refined ArabicMMLU variant, with 11-expert
    annotation for cultural appropriateness, bias, religious sensitivity, and social
    norms; addresses the structural flaws identified in ArabicMMLU. Most relevant
    for this deployment''s label validity concerns. Source: ILMAAM — [WEB-5]

    Additional relevant benchmarks: ACVA (AceGPT, 2023): 8,000+ true/false questions
    on Arabic cultural values across 58 areas, generated by GPT-3.5 and reviewed by
    Arab annotators; explicitly excludes Islamic jurisprudence. Source: ACVA HuggingFace
    — [WEB-7]'
  msa_vs_dialect_benchmark_coverage: 'ArabicMMLU covers MSA only. DialectalArabicMMLU
    (2025) is the first human-curated MMLU-style benchmark for five Arabic dialects:
    Syrian, Egyptian, Emirati, Saudi, and Moroccan — covering four of the eight deployment
    countries'' primary dialects. Results show ''substantial performance variation
    across dialects'' and confirm that model performance drops significantly compared
    to MSA. Kuwaiti, Jordanian, Palestinian, and Lebanese dialects are not yet separately
    benchmarked. Source: DialectalArabicMMLU arXiv 2510.27543 — [WEB-1]'
infrastructure_and_access_notes:
  primary_users_are_visitors: Non-Arab tourists and expats; device and connectivity
    profile likely reflects traveler demographics rather than local infrastructure.
    Primary concern is not local connectivity gaps but rather benchmark-to-deployment
    gap.
  interface_modality: Text-based; matches MMLU modality. No multimodal requirements
    documented.
  rtl_rendering: Relevant for Arabic-language sub-cohort interactions; not evaluated
    by MMLU.
  mobile_vs_desktop: '[NEEDS VERIFICATION — deferred: tourist/expat interface preference
    data for the eight-country context not found in available sources; likely unsearchable
    at sub-national precision]'
cultural_norms_relevant_to_evaluation:
  pan_arab_generalization_acceptability: Pan-Arab generalization is acceptable per
    elicitation for shared Islamic and linguistic content, but system must flag country-specific
    distinctions rather than silently universalizing.
  islam_as_shared_framework: Islamic calendar, religious practices, and jurisprudential
    vocabulary are shared reference points across all eight countries, though practice
    and legal application vary significantly (e.g., Saudi Arabia vs. Lebanon).
  gender_norms: 'Significant variation across the eight countries remains, but Saudi
    Arabia has undergone substantial formal change under Vision 2030. Key verified
    changes: driving ban lifted 2018; male guardianship system formally dissolved
    by 2017 Royal Decree; female workforce participation rose from ~22% (2016/2018)
    to 35.4–35.8% by 2024, surpassing Vision 2030''s 30% target. Women can now work
    as lawyers, judges, pilots, military officers. Persistent gaps remain: WEF Global
    Gender Gap Report 2025 ranks KSA 132/146; Human Rights Watch notes continued discrimination
    in marriage/divorce law and repression of activists. The picture for tourist interactions
    is substantially more permissive than pre-2017 norms. Source: Atlantic Council
    2024 — [WEB-8];
    OHCHR CEDAW 2024 — [WEB-9]'
  oral_and_literary_tradition: Rich Arabic literary tradition (classical poetry, Quranic
    linguistic heritage) is part of the educational knowledge domain the system covers;
    likely underrepresented in MMLU.
  ramadan_and_islamic_calendar: '[NEEDS VERIFICATION — deferred: presence in MMLU
    world religions subject not confirmed by available sources; below remaining search
    budget]'
  hospitality_norms: Diyafa (hospitality) tradition is pan-Arab cultural background
    knowledge relevant to tourist users; out of MMLU evaluation scope.
  country_specific_identity_markers:
    moroccan_amazigh_identity: 'Tamazight was officially recognized as a co-official
      language of Morocco in Article 5 of the 2011 Constitution, alongside Arabic
      — the first such constitutional recognition in North Africa. As of 2024, approximately
      24.8% of Moroccans speak Amazigh languages (Tashelhit, Central Atlas Tamazight,
      or Tarifit) natively. Implementation has been gradual: Tamazight is taught in
      primary schools and appears on public signage, but practical application in
      higher education, media, and administration remains limited. The organic law
      implementing Tamazight''s official status was passed in 2019. Source: Moroccan
      Constitution 2011 Art. 5 — [WEB-4];
      Wikipedia Standard Moroccan Amazigh — [WEB-3]'
    egyptian_national_identity: Pharaonic + Arab + Islamic layered identity; strong
      national distinctiveness within Arab world
    levantine_sectarian_pluralism: Christian, Druze, Alawi, Sunni, Shia communities
      with distinct historical narratives in Jordan, Lebanon, Palestine
    gulf_tribal_monarchical_identity: Tribal lineage and dynastic legitimacy as civic
      identity framework in UAE, Kuwait, KSA
dimension_priority_summary:
  input_ontology:
    priority: HIGH
    key_finding: MMLU has no dedicated Arab history, Middle Eastern geography, or
      Arabic language subjects. The 57 subjects are anchored in US academic curricula.
      ArabicMMLU (2024) addresses this with 40 subject tasks from Arab school curricula,
      but does not substitute for MMLU in this deployment's English-language primary
      use case.
    verification_needed: 'Partially resolved: ILMAAM study (2025) confirms significant
      cultural misalignments in Arabic MMLU on religion and morality topics. Quantitative
      audit of original English MMLU for Arab-region content proportion remains deferred.
      Source: ILMAAM — [WEB-5]'
  input_content:
    priority: HIGH
    key_finding: All MMLU data sources are Anglophone Western institutions. No Arab
      educational systems, regional universities, or Arabic curricula are represented.
      ArabicMMLU (ACL 2024) provides culturally grounded content instances from school
      exams across the eight-country deployment region — the most relevant supplement
      identified.
    verification_needed: 'Resolved for Arabic-language variant: ArabicMMLU confirmed
      as best available supplement, with country-level coverage (Jordan, Egypt, UAE,
      Palestine, Morocco) documented via example questions. Source: ArabicMMLU — [WEB-10]'
  input_form:
    priority: MODERATE
    key_finding: Primary English text-based interaction matches MMLU modality. Arabic-language
      sub-cohort cannot be evaluated by MMLU. DialectalArabicMMLU (2025) now provides
      dialect-level evaluation for Moroccan, Egyptian, Emirati, and Saudi dialects
      — directly relevant to four of the eight deployment countries.
    verification_needed: 'Substantially resolved: DialectalArabicMMLU (arXiv 2510.27543)
      covers five dialects including Moroccan and Gulf varieties. Kuwaiti, Jordanian,
      Palestinian, and Lebanese dialects remain unaddressed in published dialect benchmarks.
      Source: DialectalArabicMMLU — [WEB-1]'
  output_ontology:
    priority: HIGH
    key_finding: MMLU's single-answer MCQ label schema is structurally incapable of
      capturing the multi-perspective, uncertainty-flagging output behavior required
      for contested Arab historical and political topics. No Arab-focused benchmark
      using multi-label or free-response scoring for contested historical content
      was identified.
    verification_needed: Searched; not found — no Arab-focused benchmark with multi-label
      or open-ended contested-history scoring identified. ArabicMMLU, ACVA, ILMAAM,
      and PalmX all use MCQ or true/false formats. This remains a genuine gap in the
      Arab NLP evaluation ecosystem.
  output_content:
    priority: HIGH
    key_finding: MMLU ground-truth labels encode Western academic perspectives. ArabicMMLU
      used 10 Arab native speakers (Jordanian, Egyptian, Lebanese, UAE, Saudi) for
      annotation — a significant improvement. ILMAAM extended this with 11 expert
      annotators evaluating cultural appropriateness, bias, and religious sensitivity.
      However, neither benchmark documents inter-annotator agreement or expert review
      for politically contested topics (1948 war, Palestinian statehood).
    verification_needed: 'Partially resolved: Arab annotator demographics confirmed
      for ArabicMMLU and ILMAAM. Specific treatment of politically contested historical
      topics (Palestinian/Levantine history) in these benchmarks is NOT FOUND — contested-topic
      annotation methodology not described in available abstracts. Source: ArabicMMLU
      GitHub — [WEB-6]; ILMAAM — [WEB-5]'
  output_form:
    priority: MODERATE
    key_finding: 'Both MMLU and the deployment use text. MMLU''s MCQ accuracy metric
      cannot evaluate open-ended explanatory or perspective-acknowledging responses.
      The MENAValues benchmark (arXiv 2510.13154, 2025) demonstrates a cross-lingual
      value-shift phenomenon: LLMs give ''drastically different responses based on
      language (Arabic vs. English),'' which affects output form validity for this
      deployment''s bilingual use case.'
    verification_needed: 'Partially resolved via MENAValues benchmark finding. Alternative
      evaluation metrics for open-ended Arab-region knowledge responses remain deferred.
      Source: MENAValues — [WEB-11]'
flagged_verification_targets:
- id: FV1
  topic: Arab-region subject coverage audit in MMLU
  description: Systematic review of MMLU world history, high school geography, global
    facts, and world religions subjects for Arab-region question proportion and framing
    perspective.
  status: 'Searched, not found — no published quantitative audit of original English
    MMLU for Arab-region content proportion was identified. ILMAAM (Nacar et al. 2025)
    evaluated the Arabic translated MMLU and found significant cultural misalignments,
    but did not quantify original English MMLU Arab-region content. Source: [WEB-5]'
- id: FV2
  topic: Arabic-language MMLU variants
  description: Identification and quality assessment of ArabicMMLU, ACVA, or similar
    benchmarks; evaluation of their regional cultural grounding, country-level coverage,
    dialect handling, and contested-history treatment.
  status: 'Resolved — three-tier landscape confirmed: (1) MMLU_ar (translated, culturally
    misaligned); (2) ArabicMMLU (Koto et al., ACL 2024): 14,575 native MSA MCQs, 40
    tasks, 8 Arab countries, 10 Arab native-speaker annotators — best available supplement;
    (3) ILMAAM (Nacar et al. 2025): culturally refined ArabicMMLU with 11-expert annotation
    for cultural, religious, and social norm alignment. ACVA: 8,000+ Arabic cultural
    value true/false questions (GPT-3.5 generated, 2 Arab reviewers). Dialect coverage:
    DialectalArabicMMLU (2025) covers 5 dialects including Moroccan, Egyptian, Emirati,
    Saudi. Contested-history handling: NOT FOUND in any variant. Sources: ArabicMMLU
    — [WEB-2]; ILMAAM — [WEB-5];
    ACVA — [WEB-7];
    DialectalArabicMMLU — [WEB-1]'
- id: FV3
  topic: Palestinian and Levantine historical narrative framing
  description: Evidence on whether any MMLU history questions involve the 1948 war,
    Palestinian history, or Levantine political history, and how ground-truth labels
    are framed.
  status: 'Searched, not found — no published analysis of MMLU''s framing of Palestinian
    or Levantine historical topics was identified. ArabicMMLU includes history questions
    from Jordan, Egypt, UAE, Palestine, and Morocco (confirmed by example figures),
    but no analysis of contested-event framing in these questions is documented in
    available sources. Source: ArabicMMLU abstract — [WEB-10]'
- id: FV4
  topic: Sub-regional Arab diversity benchmarks
  description: Whether any supplementary benchmarks cover Moroccan Amazigh heritage,
    Gulf-specific social norms (kafala, Vision 2030), or Egyptian Coptic minority
    context.
  status: 'Partially resolved — MizanQA covers Moroccan law; ArabLegalEval covers
    Saudi secular law (10,000+ MCQs). Absher benchmark covers Saudi dialect specifically.
    No benchmark covering Amazigh heritage, kafala system, Vision 2030 reforms, or
    Egyptian Coptic minority context was identified. These sub-regional dimensions
    remain genuine benchmark gaps. Sources: Survey of Arabic benchmarks — [WEB-12]'
- id: FV5
  topic: Multi-perspective scoring benchmarks for contested Arab history
  description: Whether any Arab-focused benchmarks use multi-label, open-ended, or
    perspective-attribution scoring for contested historical and political content.
  status: Searched, not found — all identified Arab-region benchmarks (ArabicMMLU,
    ACVA, ILMAAM, PalmX, AraGen, BALSAM) use MCQ or true/false formats. No multi-label
    or open-ended contested-history scoring mechanism was identified in any published
    Arab NLP benchmark as of searches conducted May 2026. This is a confirmed gap
    in the ecosystem.
- id: FV6
  topic: Arab regional expert annotation
  description: Whether any available Arabic or Arab-history benchmarks document annotation
    by Arab regional subject-matter experts, and how label validity is established
    for contested topics.
  status: 'Partially resolved — ArabicMMLU: 10 Arab native speakers (Jordanian, Egyptian,
    Lebanese, UAE, Saudi); ILMAAM: 11 expert annotators for cultural appropriateness,
    bias, religious sensitivity, and social norms; PalmX 2025: two professional linguists
    reviewed all data. However, none of these benchmarks document annotator methodology
    for politically contested topics (1948 war, Palestinian statehood, Lebanese Civil
    War). Sources: ArabicMMLU GitHub — [WEB-6];
    ILMAAM — [WEB-5]; PalmX — [WEB-13]'
- id: FV7
  topic: Gulf-specific knowledge benchmark coverage
  description: Whether UAE, Kuwait, or Saudi-specific knowledge (kafala, Vision 2030,
    tribal governance, Wahhabi-Salafi religious tradition) appears in any evaluated
    benchmark.
  status: 'Partially resolved — ArabicMMLU includes UAE and Saudi exam questions;
    ArabLegalEval covers Saudi secular law; Absher covers Saudi dialect; IslamicMMLU
    (2025) covers Islamic knowledge domains including jurisprudence with madhab bias
    detection (relevant to Wahhabi-Salafi tradition). Kafala system and Vision 2030
    social context are NOT found in any benchmark. Source: ArabLegalEval/survey —
    [WEB-12]; IslamicMMLU — [WEB-14]'
- id: FV8
  topic: Moroccan and Maghreb-specific benchmark coverage
  description: Whether Amazigh/Berber heritage, Darija, or Western Sahara contested
    status appears in any available benchmark with appropriate framing.
  status: 'Partially resolved — ArabicMMLU includes Morocco as one source country
    for school exam questions; MizanQA covers Moroccan law; DialectalArabicMMLU (2025)
    includes Moroccan Arabic as one of five dialects. No benchmark was found covering
    Amazigh/Berber cultural heritage, Darija beyond dialect identification tasks,
    or Western Sahara contested territorial status. The survey of Arabic benchmarks
    (arXiv 2510.13430) explicitly notes ''gaps in coverage of other Arabic-speaking
    regions (North Africa, Levant, Iraq).'' Sources: DialectalArabicMMLU — [WEB-1];
    Arabic benchmarks survey — [WEB-12]'
- id: FV9
  topic: Current constitutional and legal status of Amazigh identity in Morocco
  description: Current status of Tamazight as an official language and Amazigh cultural
    recognition in Moroccan law.
  status: 'Resolved — Article 5 of Morocco''s 2011 Constitution recognizes Tamazight
    as an official language alongside Arabic, stating it is ''common patrimony of
    all Moroccans without exception.'' The organic law implementing this official
    status was approved in 2019. As of 2024, approximately 24.8% of Moroccans speak
    Amazigh languages natively. Tifinagh is the officially designated script (chosen
    by IRCAM 2003) but is primarily used on public signage; most speakers use Latin
    script in practice. Sources: Moroccan Constitution 2011 — [WEB-4];
    Wikipedia Standard Moroccan Amazigh — [WEB-3]'
- id: FV10
  topic: Tourist and expat interface preferences across the eight countries
  description: Whether tourists and expats in these countries predominantly use mobile
    or desktop interfaces, and implications for text rendering (RTL, mixed script).
  status: '[NEEDS VERIFICATION — deferred: likely unsearchable at required precision;
    tourist/expat sub-population device preferences not available in published form;
    national mobile penetration statistics would not capture visitor demographics]'
net_new_fields:
  arab_cultural_bias_in_llms_evidence:
    description: Multiple published studies confirm LLMs exhibit systematic Western/Anglocentric
      bias in Arab cultural contexts. Naous et al. (2024, ACL) demonstrate that 'multilingual
      and Arabic monolingual LLMs exhibit bias towards entities associated with Western
      culture' even when prompted in Arabic. The CAMeL benchmark (20,000+ culturally
      relevant entities) was developed to measure this bias across Arab vs. Western
      cultural entities. Plaza-del-Arco et al. (2024, EMNLP) find Islam faces elevated
      stereotyping and disproportionate refusal rates relative to other faiths. This
      evidence directly supports the assessment's concern that MMLU-trained systems
      will encode Western frames for Arab-region content.
    relevance: Confirms output_content and output_ontology validity concerns as empirically
      grounded, not merely hypothetical.
    sources: Naous et al. 2024 (CAMeL) — [WEB-15];
      IslamicMMLU survey of evidence — [WEB-14]
  cross_lingual_value_shift_phenomenon:
    description: MENAValues benchmark (arXiv 2510.13154, 2025) covering 16 MENA countries
      (including all eight deployment countries) demonstrates 'Cross-Lingual Value
      Shifts' where LLMs give 'drastically different responses based on language (Arabic
      vs. English)' on value-based questions. This means the same system may produce
      culturally divergent outputs depending on whether the user prompts in English
      or Arabic — a specific validity risk for this deployment's bilingual user base.
    relevance: 'Directly impacts IF (Input Form) validity: English MMLU scores may
      not predict behavior on Arabic-language prompts from the secondary user cohort.'
    sources: MENAValues benchmark — [WEB-11]
  palmx_arabic_islamic_culture_benchmark:
    description: 'PalmX 2025 is the first shared task benchmarking LLMs on Arabic
      and Islamic culture, with two subtasks: (1) general Arabic culture MCQs covering
      22 Arab countries, reviewed by professional linguists; (2) Islamic culture including
      rituals, Quranic knowledge, Hadith, and historical developments. The benchmark
      acknowledges country distribution imbalances (Iraq, Algeria underrepresented).
      Relevant to this deployment''s Islamic calendar and religious practices domain.'
    relevance: Most culturally broad Arab-specific benchmark identified; covers all
      eight deployment countries in principle but with uneven country weighting.
    sources: PalmX 2025 — [WEB-13]
  menavalues_benchmark:
    description: MENAValues (2025) is a structured benchmark derived from World Values
      Survey Wave 7 and Arab Opinion Index 2022, covering governance, economics, cultural
      identity, and individual wellbeing across 16 MENA countries — including all
      eight deployment countries. It provides population-level response distributions
      as ground truth and evaluates LLMs across neutral, personalized, and observer
      framings in both English and Arabic.
    relevance: The only benchmark found that directly measures value alignment for
      all eight deployment countries using empirically grounded survey data; relevant
      to OC and OO scoring dimensions.
    sources: MENAValues — [WEB-11]
  arabic_benchmark_ecosystem_rapid_growth:
    description: A 2025 survey catalogues over 40 Arabic NLP benchmarks, with 7 new
      culture/dialect benchmarks released in 2025 alone. The Open Arabic LLM Leaderboard
      (OALL v2, 2025) has transitioned from translated benchmarks to native content
      (ArabicMMLU, ALRAGE, AraTrust, MadinahQA), reflecting community consensus against
      translated evaluation. This rapid ecosystem growth means the benchmark landscape
      for this deployment is evolving quickly and should be re-checked periodically.
    relevance: Assessment conclusions about Arabic benchmark gaps may become outdated
      faster than typical; recommend 6-12 month review cycle.
    sources: Arabic benchmarks survey 2025 — [WEB-12]
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/abs/2510.27543 |
| WEB-2 | https://aclanthology.org/2024.findings-acl.334/ |
| WEB-3 | https://en.wikipedia.org/wiki/Standard_Moroccan_Amazigh |
| WEB-4 | https://www.constituteproject.org/constitution/Morocco_2011 |
| WEB-5 | https://aclanthology.org/2025.loreslm-1.29/ |
| WEB-6 | https://github.com/mbzuai-nlp/ArabicMMLU |
| WEB-7 | https://huggingface.co/datasets/FreedomIntelligence/ACVA-Arabic-Cultural-Value-Alignment |
| WEB-8 | https://www.atlanticcouncil.org/blogs/menasource/vision-2030-women-economy-saudi-arabia/ |
| WEB-9 | https://www.ohchr.org/en/meeting-summaries/2024/10/experts-committee-elimination-discrimination-against-women |
| WEB-10 | https://arxiv.org/abs/2402.12840 |
| WEB-11 | https://arxiv.org/html/2510.13154 |
| WEB-12 | https://arxiv.org/html/2510.13430v1 |
| WEB-13 | https://arxiv.org/html/2509.02550 |
| WEB-14 | https://arxiv.org/html/2603.23750 |
| WEB-15 | https://venturebeat.com/ai/large-language-models-exhibit-significant-western-cultural-bias-study-finds |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Your users are tourists and expats visiting specific countries — Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, and KSA. Should the system handle practical, on-the-ground knowledge that foreigners typically need, such as local dialect phrases, common tourist etiquette, local religious customs, or navigating local transport and markets? Are there categories of questions you expect frequently that go beyond formal history and geography?
A1: Dialectal phrase support would be useful but is out of scope for MMLU; the system focuses on school-level general knowledge (history, geography, language basics). Practical etiquette, religious customs, and transport guidance are frequently expected by users but are outside the intended system scope.

Q2 [IC]: Does the system need to reflect country-specific cultural nuances accurately, or is a pan-Arab generalized framing acceptable?
A2: Pan-Arab generalization is generally acceptable given shared religion and language, but the system should flag and distinguish content that is specific to particular countries rather than silently treating it as universal.

Q3 [OO]: When the system answers history or geography questions where countries hold different official or cultural positions, should it present a single answer, acknowledge multiple perspectives, or tailor its answer to the country visited?
A3: The system should acknowledge multiple perspectives and explicitly note when a topic is contested or politically sensitive across different countries, rather than presenting a single authoritative answer.

Q4 [IF]: Will users interact in English, Arabic, or both? What input-language coverage is needed from the benchmark?
A4: The primary interaction language is English, but Arabic-learning foreigners may prompt in Arabic, making Arabic-language evaluation relevant. Other languages may be supported but would require separate benchmarking of cross-lingual capabilities beyond MMLU's scope.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MMLU's 57 subjects are anchored in US academic curricula and contain minimal coverage of Arab history, regional geography, or Arabic language — the core domains this system serves. |
| IC | HIGH | MMLU's content is US-sourced and culturally transferred with no porting; specific Arab-country historical narratives, contested events (e.g., 1948 war), and country-level distinctions are almost certainly absent or framed from a non-Arab perspective. |
| IF | MODERATE | The deployment is text-only matching MMLU's modality, but a meaningful user sub-cohort will query in Arabic while MMLU is English-only, creating a language-signal mismatch for that cohort. |
| OO | HIGH | MMLU uses single-answer MCQ scoring, but the deployment requires acknowledging multiple valid perspectives on contested historical and political topics; the benchmark's binary correct/incorrect scoring is structurally misaligned with the system's intended output behavior. |
| OC | HIGH | MMLU ground-truth labels were annotated by a US-centric academic population; for Arab history and geography questions, label correctness as judged by regional stakeholders (especially on contested narratives like Palestinian history) may diverge substantially. |
| OF | MODERATE | Both MMLU and the deployment use text-based interaction, but MMLU's MCQ label output does not match the open-ended explanatory responses the deployed system produces, limiting direct transfer of scoring. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** cais/mmlu (57 subject configurations)
**Analysis date:** 2025-01-31
**Examples reviewed:** ~290 examples across 57 subject configs (5–6 per config)
**Columns shown:** question, subject, choices, answer
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | mmlu | high_school_government_and_politics, test, Ex1 | A | "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" | US constitutional law — exclusively US institutional framing | IO, IC |
| D2 | mmlu | high_school_government_and_politics, test, Ex2 | B | "In the majority of cases, federal programs are implemented by state and local governments, by means of federal funding" | US federal governance structure | IO, IC |
| D3 | mmlu | high_school_government_and_politics, test, Ex4 | D | "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" | US-specific legislative history | IO, IC |
| D4 | mmlu | high_school_us_history, test, Ex2 | B | "John C. Calhoun, 'South Carolina Exposition and Protest,' 1828" | US political history — no Arab-region analog | IO, IC |
| D5 | mmlu | high_school_us_history, test, Ex5 | A | "Tonight, the daughter of an immigrant from Italy has been chosen to run for (vice) president… Geraldine Ferraro, Vice Presidential Nomination Acceptance Address, July 19, 1984" | US domestic politics 1984 | IO, IC |
| D6 | mmlu | professional_law, test, Ex1 | A | "A truck driver was assigned to drive a huge tractor-trailer loaded with logs… the girl was struck by the tractor-trailer and was seriously injured" | US tort law scenario | IO, IC, OC |
| D7 | mmlu | professional_law, test, Ex3 | C | "A patient filed a medical malpractice action against a hospital in federal court" | US federal court procedure | IO, IC, OC |
| D8 | mmlu | professional_law, test, Ex5 | A | "A buyer filed a lawsuit against a seller based on a written contract allegedly executed at the time of the sale of the seller's hot dog stand" | US contract law | IO, IC, OC |
| D9 | mmlu | us_foreign_policy, test, Ex3 | C | "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" | US Cold War policy — framed entirely from US perspective | IO, IC, OC |
| D10 | mmlu | us_foreign_policy, test, Ex4 | D | "In American government, the power to declare war rests with Congress." | US constitutional structure | IO |
| D11 | mmlu | us_foreign_policy, test, Ex5 | A | "Revelations that the NSA was monitoring the communications of American citizens without obtaining warrants" | US domestic surveillance scandal | IO, IC |
| D12 | mmlu | moral_scenarios, test, Ex1 | A | "For which of these two scenarios does the main character do something clearly morally wrong, according to ordinary moral standards in the US as of 2020?" | Explicitly frames moral judgment via US 2020 standards | OC, OO |
| D13 | mmlu | moral_scenarios, test, Ex2 | B | "according to ordinary moral standards in the US as of 2020? Scenario 1: When I went through the road block I gave the policeman my brothers ID." | US-anchored moral framing | OC, OO |
| D14 | mmlu | moral_scenarios, test, Ex3 | C | "according to ordinary moral standards in the US as of 2020? Scenario 2: I was due to start work soon, so I went to a baseball game." | US cultural reference (baseball) embedded in moral reasoning | OC, OO, IC |
| D15 | mmlu | high_school_world_history, test, Ex2 | B | "British journalist William Howard Russell, My Indian Mutiny Diary, 1860… 'the deed was done by a subject race — by black men who dared to shed the blood of their masters'" | Colonial-era British framing of Indian revolt | IC, OC |
| D16 | mmlu | high_school_world_history, test, Ex5 | A | "Excerpt from the inscription of Kerdir at Naqsh-e-Rustam, Persia, late third century C.E. … Jews, Buddhists, Hindus, Nasoreans, Christians, Maktak, and Manichaeans in the empire were smitten" | Near Eastern (Persian) source — the only example touching the broader Middle East region | IO, IC |
| D17 | mmlu | world_religions, test, Ex1 | A | "Rome claimed that their bishop (pope) was the direct successor of which leader? … Peter" | Christian ecclesiastical history — no Islamic content in sampled examples | IO, IC |
| D18 | mmlu | world_religions, test, Ex2 | B | "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" | Jainism content | IO |
| D19 | mmlu | world_religions, test, Ex3 | C | "Which are the synoptic Gospels? … Matthew, Mark, Luke" | Christian Biblical content | IO |
| D20 | mmlu | world_religions, test, Ex4 | D | "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" | Jainism content — no Islamic content in sample | IO |
| D21 | mmlu | world_religions, test, Ex5 | A | "What is the most important prayer in Judaism? … The Shema" | Jewish religious content | IO |
| D22 | mmlu | global_facts, test, Ex1 | A | "About what percentage of survey respondents from China report having paid a bribe in the last year to access public services … as of 2017?" | China-focused global facts | IO, IC |
| D23 | mmlu | global_facts, test, Ex2 | B | "As of 2017, what fraction of the population in India used the internet in the past three months? … 26%" | India-focused global facts | IO, IC |
| D24 | mmlu | global_facts, test, Ex3 | C | "As of 2019, which of the following had the lowest life expectancy? … Mexico" | Global health — Latin American and Asian countries featured; no Arab countries | IO, IC |
| D25 | mmlu | global_facts, test, Ex4 | D | "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … makes it a better place to live?" | India-focused survey data | IO, IC |
| D26 | mmlu | global_facts, test, Ex5 | A | "At the time of independence, there were already hundreds of thousands of university graduates in ____, but hardly any at all in ____. … India, Congo" | Development economics — Africa/Asia framing, no Arab countries | IO, IC |
| D27 | mmlu | high_school_geography, test, Ex1 | A | "What is the most rapidly growing religion in the United States today? … Islam" | US-context geography question; Islam mentioned but in US demographic context | IO, IC |
| D28 | mmlu | high_school_geography, test, Ex5 | A | "Which zone contains low-income slums, ethnic ghettos, and general deterioration in Burgess's concentric zone model of urban form?" | US urban sociology model (Burgess) | IO, IC |
| D29 | mmlu | high_school_european_history, test, Ex1 | A | "Leeds Woolen Workers Petition, 1786 … The sentiments expressed by the Leeds woolen workers illustrate which of the following historical trends?" | British industrial history | IO, IC |
| D30 | mmlu | high_school_european_history, test, Ex2 | B | "Voltaire, Letters on the English Nation, 1733 … of all religions, the Christian ought doubtless to inspire the most tolerance" | European Enlightenment philosophy | IO, IC |
| D31 | mmlu | business_ethics, test, Ex5 | A | "civil society is far less developed than in, for instance, _______ … Russia, China, Britain" | Western-centric civil society framing; Arab world absent from options | IC |
| D32 | mmlu | human_aging, test, Ex3 | C | "The age at which one can receive full benefits from social security … Has been increasing" | US social security system | IC |
| D33 | mmlu | human_aging, test, Ex4 | D | "Which of the following groups of Americans have the lowest rate of alcohol abuse? … Asian-American" | US demographic framing | IC |
| D34 | mmlu | human_sexuality, test, Ex1 | A | "Which of the following is the most common method of birth control for married couples in the U.S. … Sterilization" | US-specific reproductive health statistics | IC |
| D35 | mmlu | human_sexuality, test, Ex5 | A | "From 1988 to 1990 among heterosexuals in the US, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women" | US sexual behavior survey data | IC |
| D36 | mmlu | prehistory, test, Ex4 | D | "Archaeological evidence indicates that cattle were first domesticated where and how long ago? … in the Middle East, about 10,500 years ago" | Middle East referenced as origin of cattle domestication — one of very few regional mentions | IO, IC |
| D37 | mmlu | high_school_world_history, test, Ex4 | D | "Kwame Nkrumah, Neo-Colonialism, 1965 … 'A State in the grip of neo-colonialism is not master of its own destiny.'" | African post-colonial context — non-Western source, though not Arab | IC |
| D38 | mmlu | jurisprudence, test, Ex4 | D | "Which of the following statements best describes the postmodernist project? … It rejects the Kantian concern with individual rights, equality, and justice." | Western jurisprudential theory; no Islamic jurisprudence | IO |
| D39 | mmlu | international_law, test, Ex4 | D | "What is the meaning of cultural relativism? … Cultural relativism posits that local culture should validate the existence and practice of all human rights" | International law — potentially relevant to Arab regional norms | IO |
| D40 | mmlu | auxiliary_train, train, Ex1 | B | "Jim watched a liquor store furtively for some time, planning to hold it up … On a charge of burglary, Jim's best defense would be that the liquor store was open to the public." | US criminal law scenario | IO, IC, OC |
| D41 | mmlu | high_school_statistics, test, Ex5 | A | "As reported on CNN, in a May 1999 national poll 43% of high school students expressed fear about going to school" | US-sourced statistics example | IC |
| D42 | mmlu | security_studies, test, Ex2 | B | "Best described as intensification of worldwide social relations and increasing interdependence, globalization is the result of the compression of space and time" | Abstract IR theory — not regionally specific | IO |
| D43 | mmlu | professional_psychology, test, Ex2 | B | "With regard to minority and nonminority clients, psychotherapy is … equally effective" | US psychology research context | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Universal STEM and Formal Reasoning Content
- **Dimension(s):** IO, IC, IF
- **Observation:** A large proportion of MMLU subjects — abstract algebra, anatomy, astronomy, college chemistry, college physics, computer science, electrical engineering, formal logic, elementary mathematics, machine learning — contain questions with no cultural or geographic specificity. These questions test universal scientific and mathematical knowledge equally valid for Arab-region users and non-Arab users alike.
- **Deployment relevance:** The deployment covers school-level general educational knowledge. STEM content that tourists and expats ask about (basic science, geography concepts, math) can be evaluated fairly through MMLU even in an Arab-region deployment. A model scoring well on these subjects demonstrates transferable academic competence.
- **Datapoint citations:**
  - [D1–D43 passim] Abstract algebra (Ex 1–5), anatomy (Ex 1–5), astronomy (Ex 1–5), college chemistry (Ex 1–5), formal logic (Ex 1–5) — all contain culturally neutral mathematical or biological content. For example, abstract algebra Ex3: "Find all zeros in the indicated finite field of the given polynomial with coefficients in that field. x^3 + 2x + 2 in Z_7" — no cultural grounding required.

#### Strength 2: English-Language Text-Only Format Matches Primary Interaction Mode
- **Dimension(s):** IF
- **Observation:** MMLU is exclusively text-based, English-only, and multiple-choice. The deployment's primary user cohort (non-Arab tourists and expats) interacts in English. MMLU's format matches the primary interaction modality.
- **Deployment relevance:** For the majority English-language user cohort, MMLU's format creates no signal-distribution mismatch. Questions are well-formed, unambiguous in structure, and test reading comprehension at an appropriate register for educated adult users.
- **Datapoint citations:**
  - [D6] professional_law, Ex1: "A truck driver was assigned to drive a huge tractor-trailer loaded with logs…" — demonstrates the clear, formal English register used throughout.
  - [D7] professional_law, Ex3: "A patient filed a medical malpractice action against a hospital in federal court" — standard formal English with no dialect or register barriers for educated English speakers.

#### Strength 3: International Law and Human Rights Coverage with Some Global Applicability
- **Dimension(s):** IO, IC
- **Observation:** The `international_law` subject contains questions about treaty-based human rights mechanisms, cultural relativism, and the distinction between public and private acts under international law. These topics have global applicability and touch on norms relevant to all eight deployment countries.
- **Deployment relevance:** Tourists and expats may have general curiosity about human rights frameworks that apply to the Arab world. International law questions are framed abstractly enough to not be exclusively US-anchored.
- **Datapoint citations:**
  - [D39] international_law, Ex4: "What is the meaning of cultural relativism? … Cultural relativism posits that local culture should validate the existence and practice of all human rights" — this question is abstractly framed and relevant to discussions of human rights in Arab-region contexts.
  - [D39] international_law, Ex3: "Is the unlawful homicide committed by Minister of country X abroad an act jure imperii or jure gestionis?" — abstractly framed, not anchored to any specific legal system.

#### Strength 4: Zero-Shot/Few-Shot Evaluation Design Appropriate for Generalization Testing
- **Dimension(s):** OF
- **Observation:** MMLU is designed for zero-shot and few-shot evaluation, probing knowledge acquired during pretraining. For a deployed system that must generalize to novel queries, this evaluation paradigm (rather than fine-tuned task-specific scoring) is more aligned with deployment behavior.
- **Deployment relevance:** Tourists and expats ask unpredictable general knowledge questions. A model evaluated under zero-shot/few-shot conditions demonstrates the same generalization property required for open-domain question answering about Arab history, geography, and language.
- **Datapoint citations:** All sampled examples are zero-shot MCQ without task-specific training — consistent with the deployment's need to evaluate generalization rather than narrow fine-tuned performance.

#### Strength 5: World Religions Subject Nominally Covers Multiple Faith Traditions
- **Dimension(s):** IO
- **Observation:** The `world_religions` subject includes questions on Jainism, Judaism, and Christianity across the six sampled examples. The subject label indicates coverage of multiple world religions, which nominally includes Islam — the dominant religion across all eight deployment countries.
- **Deployment relevance:** Tourists and expats frequently have questions about Islamic practices, the Islamic calendar, and Islamic history, which are core deployment topics. The world_religions subject is the closest available MMLU proxy for this content area.
- **Datapoint citations:**
  - [D17] world_religions, Ex1: "Rome claimed that their bishop (pope) was the direct successor of which leader? … Peter" — Christian content.
  - [D18] world_religions, Ex2: "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" — Jainism content.
  - [D21] world_religions, Ex5: "What is the most important prayer in Judaism? … The Shema" — Jewish content. No Islamic content appeared in the six sampled world_religions examples, but the subject label does not preclude its presence in the full 171-question set.

#### Strength 6: High School World History Includes Some Non-Western Primary Sources
- **Dimension(s):** IC
- **Observation:** The `high_school_world_history` subject includes non-Western and non-European primary sources. Among the five sampled examples, one is drawn from an ancient Persian inscription (Kerdir at Naqsh-e-Rustam), one from an African anti-colonial theorist (Kwame Nkrumah), and one from a British account of Indian colonialism. This demonstrates that the subject does not exclusively cover Western European history.
- **Deployment relevance:** The deployment requires school-level world history knowledge including pre-Islamic Middle Eastern history. The Persian inscription example shows the subject can include content from the broader Middle East/Central Asia region.
- **Datapoint citations:**
  - [D16] high_school_world_history, Ex5: "Excerpt from the inscription of Kerdir at Naqsh-e-Rustam, Persia, late third century C.E. … Jews, Buddhists, Hindus, Nasoreans, Christians, Maktak, and Manichaeans in the empire were smitten" — Near Eastern content, though pre-Islamic and Persian rather than Arab.
  - [D37] high_school_world_history, Ex4: "Kwame Nkrumah, Neo-Colonialism, 1965 … 'A State in the grip of neo-colonialism is not master of its own destiny.'" — African post-colonial perspective, showing non-Western framing is possible.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: No Arab-Region Subject Categories in the 57-Subject Taxonomy
- **Dimension(s):** IO
- **Observation:** Across all 57 MMLU subject configurations, not one is dedicated to Arab history, Middle Eastern geography, Arabic language, Islamic jurisprudence, or any sub-regional Arab topic. The subject list is exhaustively confirmed from the HF metadata: subjects include `high_school_us_history`, `high_school_european_history`, `high_school_government_and_politics` (US-framed), and `us_foreign_policy` — but no Arab history, no MENA geography, no Islamic law or culture.
- **Deployment relevance:** The deployment is specifically designed to answer questions about Arab history, regional geography, and Arabic language across eight Arab countries. The complete absence of dedicated Arab-region subjects means MMLU cannot evaluate whether a model knows anything useful for the core deployment domain. This is a structural gap, not a sampling artifact.
- **Datapoint citations:**
  - [D1] high_school_government_and_politics, Ex1: "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" — one of five government/politics examples, all US-institutional.
  - [D10] us_foreign_policy, Ex4: "In American government, the power to declare war rests with Congress." — The "Foreign Policy" subject is entirely framed from a US perspective with no Arab-country policy questions in the sample.
  - [D3] high_school_government_and_politics, Ex4: "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" — US-specific legislation.

#### CRITICAL Concern 2: Global Facts Subject Excludes Arab Countries in Sampled Questions
- **Dimension(s):** IO, IC
- **Observation:** `global_facts` is the subject most likely to contain Arab-region statistical questions. All five sampled examples reference China (2), India (3), Mexico (1), and an Africa/Korea comparison (1). No Arab country appears in any of the five sampled global_facts questions.
- **Deployment relevance:** The deployment covers general school-level knowledge about the Arab world, including geography and demography. If `global_facts` — the subject most suited to cross-regional factual knowledge — contains no Arab-country questions even in a sample of five, this signals extremely low Arab-region density.
- **Datapoint citations:**
  - [D22] global_facts, Ex1: "About what percentage of survey respondents from China report having paid a bribe…" — China-focused.
  - [D23] global_facts, Ex2: "As of 2017, what fraction of the population in India used the internet…" — India-focused.
  - [D24] global_facts, Ex3: "As of 2019, which of the following had the lowest life expectancy? … Mexico" — Latin American comparison.
  - [D25] global_facts, Ex4: "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … makes it a better place to live?" — India-focused.
  - [D26] global_facts, Ex5: "At the time of independence, there were already hundreds of thousands of university graduates in India, but hardly any at all in Congo" — Africa/Asia comparison.

#### CRITICAL Concern 3: Moral Scenarios Explicitly Anchored to "US Standards as of 2020"
- **Dimension(s):** OC, OO
- **Observation:** Every sampled `moral_scenarios` example contains the explicit phrase "according to ordinary moral standards in the US as of 2020." This is not merely an implicit cultural bias — it is a stated label constraint encoding US moral standards as the ground truth. For users asking about moral or social norms in Arab countries, this labeling scheme encodes a directly contradictory cultural standard.
- **Deployment relevance:** The deployment system serves users in eight Arab countries where moral norms around alcohol, gender relations, family honor, public behavior, and religious observance diverge significantly from "US standards as of 2020." For any Arab-region moral or social knowledge domain, MMLU's moral_scenarios ground-truth labels are categorically misaligned with local stakeholder judgments.
- **Datapoint citations:**
  - [D12] moral_scenarios, Ex1: "For which of these two scenarios does the main character do something clearly morally wrong, according to ordinary moral standards in the US as of 2020? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot." — US moral framing as explicit label criterion.
  - [D13] moral_scenarios, Ex2: "according to ordinary moral standards in the US as of 2020? Scenario 1 | When I went through the road block I gave the policeman my brothers ID." — identity document fraud scenario judged by US standards.
  - [D14] moral_scenarios, Ex3: "according to ordinary moral standards in the US as of 2020? Scenario 2 | I was due to start work soon, so I went to a baseball game." — baseball as a culturally embedded reference in a moral reasoning task.

#### CRITICAL Concern 4: World History Arab-Region Absence; Middle East Appears Only as Ancient Persia and Agricultural Origin
- **Dimension(s):** IO, IC
- **Observation:** Across five sampled `high_school_world_history` examples, the Middle East/Arab region appears exactly once — in a Sasanian Persian inscription from the 3rd century CE (pre-Islamic, non-Arab). No Arab nationalist history, no Ottoman period, no Islamic civilization, no 20th-century Arab state formation, no Palestinian history, and no Levantine, Egyptian, or Gulf-specific content appears. The prehistory subject mentions the Middle East only as the origin of cattle domestication (~10,500 years ago).
- **Deployment relevance:** The deployment's core subject matter includes Arab history from the Islamic Golden Age through modern state formation. The near-complete absence of Islamic and Arab-period history in the world history and prehistory subjects means MMLU cannot assess a model's knowledge of the content tourists and expats most frequently ask about.
- **Datapoint citations:**
  - [D16] high_school_world_history, Ex5: "Excerpt from the inscription of Kerdir at Naqsh-e-Rustam, Persia, late third century C.E." — only Middle East reference in the five world history examples; pre-Islamic, Persian, not Arab.
  - [D36] prehistory, Ex4: "Archaeological evidence indicates that cattle were first domesticated where and how long ago? … in the Middle East, about 10,500 years ago" — Middle East mentioned only as an ancient agricultural origin, no cultural content.
  - [D29] high_school_european_history, Ex1: "Leeds Woolen Workers Petition, 1786" — European industrial history.
  - [D30] high_school_european_history, Ex2: "Voltaire, Letters on the English Nation, 1733" — European Enlightenment.

#### CRITICAL Concern 5: US Foreign Policy Subject Framed Entirely from US Perspective
- **Dimension(s):** IO, IC, OC
- **Observation:** All five sampled `us_foreign_policy` examples are framed from within US institutional and policy perspectives — NSC 68, War Powers Act, NSA surveillance, "Philadelphian System" exceptionalism. For a deployment covering Arab countries where US foreign policy is a contested and politically sensitive topic (Gulf War, Arab-Israeli conflict, Iraq War), the US-centric framing encodes one perspective as the correct answer.
- **Deployment relevance:** Users asking about US foreign policy in the Arab world — a frequent tourist/expat query about why certain regional conditions exist — will receive answers framed from a US perspective that may contradict the perspectives of host-country citizens in Jordan, Palestine, Lebanon, and Egypt.
- **Datapoint citations:**
  - [D9] us_foreign_policy, Ex3: "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" — entirely US institutional framing.
  - [D11] us_foreign_policy, Ex5: "Revelations that the NSA was monitoring the communications of American citizens without obtaining warrants" — US domestic civil liberties framing of surveillance.

---

#### MAJOR

#### MAJOR Concern 1: Professional Law, Jurisprudence, and Human Aging Encode US Institutional Specifics
- **Dimension(s):** IO, IC, OC
- **Observation:** The `professional_law` subject (500 test examples, the largest in MMLU) consists entirely of US common law scenarios — tort law, contract law, evidence rules, DUI statutes, federal court procedure. `human_aging` references US Social Security age thresholds and alcohol abuse rates among "Americans." These questions have no validity for an Arab-region deployment where legal systems are based on civil law (Morocco, Egypt), Islamic law (Saudi Arabia, Kuwait), or mixed systems (Lebanon, Jordan).
- **Deployment relevance:** Tourists and expats may ask general legal questions (e.g., "What are my rights?" or "How does property law work here?"). A model evaluated on MMLU professional law has been tested only on US common law knowledge, which may actively mislead users about Arab legal systems.
- **Datapoint citations:**
  - [D6] professional_law, Ex1: "A truck driver was assigned to drive a huge tractor-trailer loaded with logs…" — US tort law.
  - [D8] professional_law, Ex5: "A buyer filed a lawsuit against a seller based on a written contract allegedly executed at the time of the sale of the seller's hot dog stand" — US contract law.
  - [D32] human_aging, Ex3: "The age at which one can receive full benefits from social security … Has been increasing" — US social security specifics.
  - [D33] human_aging, Ex4: "Which of the following groups of Americans have the lowest rate of alcohol abuse? … Asian-American" — US demographic categories.

#### MAJOR Concern 2: High School Government and Politics Is Exclusively US Government
- **Dimension(s):** IO, IC
- **Observation:** All five sampled `high_school_government_and_politics` questions concern US constitutional structure — First Amendment, federal-state relations, Articles of Confederation, War Powers Act, Congressional representation. There is no comparative government content, no coverage of Arab governance structures (monarchies, tribal councils, military governments), and no non-US political systems.
- **Deployment relevance:** Tourists and expats visiting Arab countries frequently ask about governance structures, political history, and civic life. MMLU's government subject cannot evaluate a model's knowledge of Hashemite monarchy, Gulf tribal governance, Lebanese confessionalism, or Egyptian political history.
- **Datapoint citations:**
  - [D1] high_school_government_and_politics, Ex1: "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" — US constitutional law.
  - [D2] high_school_government_and_politics, Ex2: "In the majority of cases, federal programs are implemented by state and local governments, by means of federal funding" — US federal structure.
  - [D3] high_school_government_and_politics, Ex4: "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" — US-specific legislation.

#### MAJOR Concern 3: World Religions Sample Shows No Islamic Content; Coverage Depth Unknown
- **Dimension(s):** IO, IC
- **Observation:** Six sampled `world_religions` examples include content on Christian ecclesiastical succession, Jainism (2 questions), Jewish prayer, Daoist text, and Christian Gospels. Zero of the six sampled examples cover Islam. While the full 171-question set may include Islamic content, the absence from the sample raises concerns about proportion and framing.
- **Deployment relevance:** Islam is the dominant religion across all eight deployment countries and a primary topic of tourist/expat curiosity (Islamic calendar, Ramadan, prayer practices, mosque etiquette as general knowledge). A model evaluated only on Christian, Jain, and Jewish content will not have been tested on the religious knowledge most relevant to the deployment.
- **Datapoint citations:**
  - [D17] world_religions, Ex1: "Rome claimed that their bishop (pope) was the direct successor of which leader? … Peter" — Christianity.
  - [D18] world_religions, Ex2: "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" — Jainism.
  - [D19] world_religions, Ex3: "Which are the synoptic Gospels? … Matthew, Mark, Luke" — Christian Biblical content.
  - [D20] world_religions, Ex4: "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" — Jainism.
  - [D21] world_religions, Ex5: "What is the most important prayer in Judaism? … The Shema" — Judaism.

#### MAJOR Concern 4: Single-Answer MCQ Label Schema Cannot Accommodate Multi-Perspective Contested Topics
- **Dimension(s):** OO, OC
- **Observation:** MMLU's output schema enforces exactly one correct answer per question (A, B, C, or D). The deployment requirement — to acknowledge multiple perspectives on contested historical/political topics and flag political sensitivity — is structurally incompatible with this scoring paradigm. Across all 290+ sampled examples, every question has exactly one labeled correct answer with no mechanism for flagging contestedness.
- **Deployment relevance:** Key deployment topics — the 1948 war/Nakba framing, Western Sahara status, Lebanese Civil War causes, Palestinian statehood, Ottoman legacy — require multi-perspective responses. MMLU cannot score a model that says "this topic is contested; here are two perspectives" — such a response would score 0% on MMLU regardless of its accuracy for deployment purposes.
- **Datapoint citations:**
  - [D12] moral_scenarios, Ex1 through [D14] moral_scenarios, Ex3: all examples have a single binary label; no partial credit or multi-perspective acknowledgment is possible.
  - [D9] us_foreign_policy, Ex3: "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" — one correct answer asserted; no acknowledgment of contested Cold War historiography.
  - [D15] high_school_world_history, Ex2: "According to the second passage, the Cawnpore Massacre … can be viewed as a reaction to the systemic brute force with which the British governed India" — colonial framing resolved to single answer from secondary source.

#### MAJOR Concern 5: High School Geography Framed Around US Urban Models and US Religious Demographics
- **Dimension(s):** IO, IC
- **Observation:** Five sampled `high_school_geography` questions include: Islam as the "most rapidly growing religion in the United States" (US-contextual framing), a globe/map projection question, pastoralism definition, core-periphery development model, and Burgess's concentric zone model of US urban form. None concern Arab-world physical geography, political geography, or spatial concepts relevant to Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, or KSA.
- **Deployment relevance:** The deployment covers regional geography of eight Arab countries. MMLU's high school geography content evaluates US-anchored urban sociology models and US religious demographics rather than physical or political geography of the Arab world.
- **Datapoint citations:**
  - [D27] high_school_geography, Ex1: "What is the most rapidly growing religion in the United States today? … Islam" — Islam mentioned only in US demographic context.
  - [D28] high_school_geography, Ex5: "Which zone contains low-income slums, ethnic ghettos, and general deterioration in Burgess's concentric zone model of urban form?" — US urban sociology model.

#### MAJOR Concern 6: Human Sexuality and Human Aging Encode US-Specific Survey Data as Ground Truth
- **Dimension(s):** IC, OC
- **Observation:** `human_sexuality` questions cite US statistics (most common US contraceptive method, US heterosexual partner counts 1988–1990), and `human_aging` references US Social Security and US ethnic group alcohol abuse rates. These ground-truth labels reflect US-population norms that diverge substantially from Arab-region norms around sexuality, family planning, gender relations, and social welfare.
- **Deployment relevance:** Tourists and expats may ask general questions about social norms, health practices, and demographics. A model evaluated on US-population ground truths for these topics will have been reinforced with knowledge claims that contradict Arab-region realities (e.g., contraceptive prevalence, attitudes toward sexuality, alcohol norms).
- **Datapoint citations:**
  - [D34] human_sexuality, Ex1: "Which of the following is the most common method of birth control for married couples in the U.S. … Sterilization" — US-specific reproductive health statistic as ground truth.
  - [D35] human_sexuality, Ex5: "From 1988 to 1990 among heterosexuals in the US, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women" — US behavioral survey data.
  - [D33] human_aging, Ex4: "Which of the following groups of Americans have the lowest rate of alcohol abuse? … Asian-American" — alcohol abuse among American ethnic groups.

---

#### MINOR

#### MINOR Concern 1: High School European History Dominates Non-US History Slot
- **Dimension(s):** IO
- **Observation:** MMLU has a dedicated `high_school_european_history` subject but no equivalent for world history outside Europe and the US. The five sampled European history examples cover British industrialization, Voltaire, Pico della Mirandola, Medici-era Neoplatonism, and the Royal Society. This dedicated European history slot confirms that non-European, non-US histories are subordinated to the catch-all `high_school_world_history` subject.
- **Deployment relevance:** Arab history from the Islamic Golden Age, the Ottoman period, or modern state formation has no dedicated subject and must compete with all other non-European world history for representation in a single 237-question subject.
- **Datapoint citations:**
  - [D29] high_school_european_history, Ex1: "Leeds Woolen Workers Petition, 1786 … The sentiments expressed by the Leeds woolen workers illustrate which of the following historical trends?" — British industrial history.
  - [D30] high_school_european_history, Ex2: "Voltaire, Letters on the English Nation, 1733" — French Enlightenment.

#### MINOR Concern 2: Business Ethics Civil Society Question Omits Arab World from Options
- **Dimension(s):** IC
- **Observation:** A `business_ethics` question asks about countries with less developed civil society compared to a more developed example. The correct answer is "Russia, China, Britain" — the Arab world is not even presented as an option in this question about global civil society development.
- **Deployment relevance:** This is a minor individual instance, but it illustrates how MMLU's question design treats Arab countries as outside the scope of even comparative global analysis.
- **Datapoint citations:**
  - [D31] business_ethics, Ex5: "Although the benefit and contribution of civil society in encouraging sustainability … in many other countries, such as _____ and ______ civil society is far less developed than in, for instance, _______. … Russia, China, Britain" — Arab world entirely absent from the answer options for a global civil society comparison question.

#### MINOR Concern 3: Prehistory and Archaeology Show Selective Middle East Coverage
- **Dimension(s):** IC
- **Observation:** The `prehistory` subject contains a question correctly identifying the Middle East as the origin of cattle domestication ~10,500 years ago. However, this represents the region only as a prehistoric agricultural site, not as a culturally meaningful historical location. Other prehistory questions cover Stonehenge, Machu Picchu, Chinese civilization origins, and African butterfly species.
- **Deployment relevance:** For users curious about the deep history of the Arab region, the prehistory subject does contain one relevant data point. However, coverage is incidental rather than systematic, and the framing is archaeological rather than cultural.
- **Datapoint citations:**
  - [D36] prehistory, Ex4: "Archaeological evidence indicates that cattle were first domesticated where and how long ago? … in the Middle East, about 10,500 years ago" — region mentioned as agricultural origin only.

#### MINOR Concern 4: Professional Psychology US-Centric Research Norms
- **Dimension(s):** IC
- **Observation:** `professional_psychology` references US mental health norms (PKU treatment, minority/nonminority client effectiveness, crisis therapy frameworks). These norms reflect US clinical psychology literature and may not transfer to Arab-region mental health contexts or cultural attitudes toward therapy.
- **Deployment relevance:** Minor for this deployment, which focuses on history, geography, and language rather than psychology. However, to the extent users ask general knowledge questions about psychology or mental health, the US-clinical framing introduces cultural mismatch.
- **Datapoint citations:**
  - [D43] professional_psychology, Ex2: "With regard to minority and nonminority clients, psychotherapy is … equally effective" — US racial/ethnic minority framing of clinical effectiveness research.

---

### Content Coverage Summary

The 290+ sampled MMLU examples across 57 subjects confirm the following characterization:

**Dominant content register:** US academic curriculum (high school through professional level), drawing on US standardized tests, US undergraduate course materials, and Western European academic publications. The register is formal, English-only, and assumes familiarity with US institutional structures (federal government, common law, social security, US ethnic demographics).

**Subject concentration relevant to deployment:** Nominally relevant subjects (`high_school_world_history`, `high_school_geography`, `world_religions`, `global_facts`, `international_law`, `security_studies`) contain either no sampled Arab-region content (`global_facts`, `world_religions`, `high_school_geography`) or incidental references to the broader Middle East (`prehistory`: one question; `high_school_world_history`: one Sasanian Persian inscription).

**Subjects with zero Arab-region relevance:** `high_school_us_history`, `high_school_government_and_politics`, `us_foreign_policy`, `professional_law`, `human_sexuality`, `human_aging` — together comprising several hundred questions — are anchored in US-specific institutional, legal, and demographic contexts that transfer nothing meaningful to the Arab-region deployment.

**Moral and social content:** The `moral_scenarios` subject explicitly labels correct answers as "ordinary moral standards in the US as of 2020," creating a direct conflict with Arab-region moral frameworks on topics including alcohol, gender relations, family structures, and religious observance.

**Language:** Entirely English. No Arabic-script content, no dialect questions, no Arabic language instruction questions. The secondary Arabic-learning user cohort is unservable by this benchmark.

**Non-Western content that does appear:** The world history subject contains non-Western sources (Nkrumah, Kerdir inscription), and prehistory touches the Middle East as an agricultural origin point. These are the strongest evidence against total Western monoculture, but they are scattered and do not constitute systematic Arab-region coverage.

---

### Limitations

1. **Sample size per subject:** 5–6 examples per subject from the test split. For subjects with 237 questions (`high_school_world_history`) or 500 questions (`professional_law`, `moral_scenarios`, `professional_psychology`), the sample cannot confirm or rule out rare Arab-region content. It is possible that a small number of world history questions cover Islamic or Arab-period history not captured in the sample.

2. **World religions Islam content:** Six sampled world_religions examples showed no Islamic content. The full 171-question set may contain Islamic questions (possibly covering the Five Pillars, hadith, early Islamic history), but the framing perspective (Western academic vs. Islamic scholarly) cannot be determined from the sample.

3. **Security studies depth:** The security studies subject (245 questions) was sampled at 5 examples, all covering abstract IR theory. This subject might contain questions touching on Middle East security dynamics, but none appeared in the sample.

4. **Miscellaneous subject:** The `miscellaneous` subject (500+ questions) is a catch-all that could contain Arab-region factual questions. The five sampled examples (traffic lights, labor force, geometry, proletariat, material resistance) show no Arab-region content, but coverage uncertainty is high for this heterogeneous category.

5. **Auxiliary train split:** The auxiliary_train examples sampled are all US law scenarios, but this split was not systematically sampled across subjects — it represents only a subset of the training data.

6. **No access to question-level metadata on source:** The dataset does not expose which specific source documents each question came from, preventing confirmation of which questions originated from GRE, USMLE, Oxford Press, etc., vs. other sources that might include non-US content.

7. **Full quantitative coverage audit impossible from sample:** A definitive count of Arab-region questions across all 15,908 MMLU items would require inspecting every question — beyond what a sample-based analysis can provide. The web search finding that no published quantitative audit exists for original English MMLU Arab-region content proportion remains unresolved.

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
  "region": "Non-Arab Tourists and Expats in Eight Arab Countries",
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
